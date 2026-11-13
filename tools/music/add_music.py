#!/usr/bin/env python3
"""Bring recorded music into the game (MUSIC-24). The whole story is in audio/README.md.

    python3 tools/music/add_music.py               every new or changed track in music-src/
    python3 tools/music/add_music.py egypt         just that one (or several names)
    python3 tools/music/add_music.py --all         every track in music-src/, changed or not
    python3 tools/music/add_music.py --list        what the game has now
    python3 tools/music/add_music.py --remove egypt    take a track out of the game (its files and its entry)

For each master in music-src/ (a WAV, FLAC or AIFF from any music program; an Ogg or Opus with loop tags will do too),
named after the track (egypt.wav), with a text file of the same name beside it (egypt.txt) saying where it loops:

  1. it works out the loop points to the sample: from bars and tempo, from times, from loop points stored in the file
     (a WAV's own loop, or LOOPSTART/LOOPLENGTH tags), or else the whole file loops;
  2. it folds whatever runs past the loop's end (the reverb ringing out) onto the loop's start, and cuts the file there,
     so the seam sounds like the music going round;
  3. it measures the loudness (EBU R128) and sets one gain, so every track sits at the same level (-18 LUFS) with its
     peaks under -1 dB; nothing is compressed;
  4. it makes audio/music/<name>.webm (Opus) and audio/music/<name>.m4a (AAC), and checks both decode to the right length;
  5. it writes js/content/music-files.js, the list the game reads, and says which scenes will play the track.

The masters are never changed, and are not in git (music-src/ is in .gitignore): keep them backed up. A track whose master
is not here (another computer, a fresh copy) keeps its files and its entry untouched.

Needs Python 3 and ffmpeg (Linux: sudo apt install ffmpeg; Mac: brew install ffmpeg; Windows: winget install ffmpeg).
"""

import array
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "music-src")
OUT = os.path.join(ROOT, "audio", "music")
LIST = os.path.join(ROOT, "js", "content", "music-files.js")
RATE = 48000                 # Opus works at 48 kHz: every master is brought to it first, and every loop point counted in it
TARGET = -18.0               # the house loudness of a master (LUFS); sound.js `recordedLevel` sets how loud that plays
CEILING = -1.0               # the highest a true peak may reach (dBTP)
TAIL = 6.0                   # at most this many seconds past the loop's end are folded onto its start (a reverb tail)
PAD = 0.1                    # and the loop's first tenth of a second is copied after its end, so a codec's last frame is not at the seam
KINDS = (".wav", ".flac", ".aif", ".aiff", ".ogg", ".opus", ".mp3", ".m4a")
LOSSY = (".ogg", ".opus", ".mp3", ".m4a")
NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")

HEADER = """// MUSIC-24: the game's recorded music, made by tools/music/add_music.py from the masters in music-src/ (audio/README.md).
// Do not edit by hand: change a track's text file in music-src/ and run the tool again. (The masters are not in git.)
// MUSIC_FILES: name -> { files: { webm, m4a }, seconds, loop: [start, end] or null, volume, fade, ... }
// MUSIC_SCENES: scene id -> the name of the recording made for it (its text file's `scenes:`)

"""


class Stop(Exception):
    """Something about one track that has to be put right before it can go in."""


# ---------------------------------------------------------------- ffmpeg

def need_ffmpeg():
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            sys.exit(f"{tool} is not installed. Linux: sudo apt install ffmpeg   Mac: brew install ffmpeg   Windows: winget install ffmpeg")


def run(cmd, data=None):
    p = subprocess.run(cmd, input=data, capture_output=True)
    if p.returncode:
        raise Stop("ffmpeg said: " + p.stderr.decode("utf-8", "replace").strip().splitlines()[-1][:300])
    return p


def probe(path):
    out = run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
               "stream=sample_rate,channels,duration:stream_tags:format_tags:format=duration", "-of", "json", path]).stdout
    info = json.loads(out)
    if not info.get("streams"):
        raise Stop("there is no sound in it")
    st = info["streams"][0]
    tags = {k.upper(): v for k, v in {**info.get("format", {}).get("tags", {}), **st.get("tags", {})}.items()}
    return int(st.get("sample_rate", RATE)), int(st.get("channels", 2)), tags


def decode(path, channels):
    """The master as 32-bit floats at 48 kHz, interleaved (soxr if this ffmpeg has it)."""
    base = ["ffmpeg", "-v", "error", "-i", path, "-vn", "-map", "0:a:0", "-ac", str(channels), "-ar", str(RATE)]
    tail = ["-f", "f32le", "-acodec", "pcm_f32le", "pipe:1"]
    try:
        raw = run(base + ["-af", "aresample=resampler=soxr:precision=28"] + tail).stdout
    except Stop:
        raw = run(base + tail).stdout
    a = array.array("f")
    a.frombytes(raw[: len(raw) - len(raw) % 4])
    if sys.byteorder == "big":
        a.byteswap()
    return a


def loudness(raw_path, channels):
    """Integrated loudness (LUFS) and true peak (dBFS) of 48 kHz float audio."""
    err = run(["ffmpeg", "-nostats", "-f", "f32le", "-ar", str(RATE), "-ac", str(channels), "-i", raw_path,
               "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr.decode("utf-8", "replace")
    i = re.findall(r"I:\s+(-?[\d.]+|-inf) LUFS", err)
    pk = re.findall(r"Peak:\s+(-?[\d.]+|-inf) dBFS", err)
    val = lambda s: -99.0 if not s or s[-1] == "-inf" else float(s[-1])
    return val(i), val(pk)


def length_of(path, channels):
    """How many samples (at 48 kHz) a made file decodes to."""
    raw = run(["ffmpeg", "-v", "error", "-i", path, "-ac", str(channels), "-ar", str(RATE), "-f", "f32le", "pipe:1"]).stdout
    return len(raw) // (4 * channels)


# ---------------------------------------------------------------- loop points stored in a master

def wav_loop(path):
    """A WAV's own loop (its `smpl` chunk): (start, end) in samples at its own rate, end exclusive; or None."""
    try:
        with open(path, "rb") as f:
            head = f.read(12)
            if head[:4] != b"RIFF" or head[8:12] != b"WAVE":
                return None
            while True:
                h = f.read(8)
                if len(h) < 8:
                    return None
                cid, size = h[:4], struct.unpack("<I", h[4:])[0]
                body = f.read(size + (size & 1))
                if cid == b"smpl" and size >= 36:
                    n = struct.unpack("<I", body[28:32])[0]
                    if n >= 1 and size >= 36 + 24:
                        start, end = struct.unpack("<II", body[36 + 8:36 + 16])
                        return start, end + 1
                    return None
    except OSError:
        return None


def tag_loop(tags):
    """LOOPSTART with LOOPLENGTH or LOOPEND (in samples), as RPG Maker's and other engines' Ogg files carry them."""
    try:
        if "LOOPSTART" not in tags:
            return None
        start = int(float(tags["LOOPSTART"]))
        if "LOOPLENGTH" in tags:
            return start, start + int(float(tags["LOOPLENGTH"]))
        if "LOOPEND" in tags:
            return start, int(float(tags["LOOPEND"]))
    except ValueError:
        return None
    return None


# ---------------------------------------------------------------- the text file beside a master

def read_notes(path):
    notes = {}
    if not os.path.exists(path):
        return notes
    for n, line in enumerate(open(path, encoding="utf-8-sig"), 1):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        if ":" not in line:
            raise Stop(f"{os.path.basename(path)}, line {n}: write it as  key: value  (for example  loop: 32 bars)")
        key, value = line.split(":", 1)
        notes[" ".join(key.lower().split())] = value.strip()
    return notes


def yes(value):
    return str(value).strip().lower() in ("yes", "y", "true", "on", "1")


def seconds_of(text, rate, bar):
    """A length or a time: '4 bars', '0:11.43', '1:02:03.5', '11.43', '11.43 s', '548571 samples' (at the master's rate)."""
    t = text.strip().lower()
    m = re.fullmatch(r"([\d.]+)\s*bars?", t)
    if m:
        if not bar:
            raise Stop(f"'{text}' is in bars: give the tempo too (bpm: 84, and meter: 4 for four beats in a bar)")
        return float(m.group(1)) * bar
    m = re.fullmatch(r"(\d+)\s*samples?", t)
    if m:
        return int(m.group(1)) / rate
    m = re.fullmatch(r"(?:(\d+):)?(?:(\d+):)?([\d.]+)\s*s?", t)
    if m:
        parts = [p for p in m.groups() if p is not None]
        total = 0.0
        for p in parts:
            total = total * 60 + float(p)
        return total
    raise Stop(f"'{text}' is not a time I can read (try 0:11.43, 11.43, 4 bars or 548571 samples)")


def loop_points(notes, rate, total_s, stored):
    """(start, end) in seconds, or None for a piece that plays once; and where the numbers came from."""
    bar = None
    if "bpm" in notes:
        try:
            bpm = float(notes["bpm"].split()[0])
            beats = float(notes.get("meter", "4").split("/")[0].split()[0])
        except (ValueError, IndexError):
            raise Stop("bpm and meter must be numbers (bpm: 84, meter: 4)")
        bar = beats * 60.0 / bpm
    downbeat = seconds_of(notes["downbeat"], rate, None) if "downbeat" in notes else 0.0
    loop = notes.get("loop", "").strip().lower()
    if loop in ("none", "no", "off"):
        return None, "plays once (loop: none)"
    if "loop start" in notes or "loop end" in notes:
        start = seconds_of(notes.get("loop start", "0"), rate, bar)
        end = seconds_of(notes["loop end"], rate, bar) if "loop end" in notes else total_s
        return (start, end), "loop start / loop end"
    if "intro" in notes or loop not in ("", "whole"):
        # both count from the downbeat (the first bar's first beat: the file's start unless `downbeat:` says otherwise)
        intro = notes.get("intro", "").strip().lower()
        start = downbeat + (0.0 if intro in ("", "none", "no", "0") else seconds_of(intro, rate, bar))
        end = start + seconds_of(loop, rate, bar) if loop not in ("", "whole") else total_s
        return (start, end), "intro / loop"
    if stored:
        return (stored[0] / rate, stored[1] / rate), "the loop stored in the file"
    return (0.0, total_s), "the whole file (no loop given)"


# ---------------------------------------------------------------- the game's scenes, for the report

def scene_facts():
    def read(p):
        try:
            return open(os.path.join(ROOT, p), encoding="utf-8").read()
        except OSError:
            return ""
    index = read("js/content/scenes/index.js")
    block = index[index.find("sceneIds"): index.find("];", index.find("sceneIds"))]
    ids = re.findall(r'"([a-z0-9-]+)"', block)
    eras = {m.group(1): m.group(2) for m in re.finditer(r'^\s*(\w+):\s*\{[^\n]*?\bmusic:\s*"([\w-]+)"', read("js/content/world.js"), re.M)}
    sound = read("js/content/sound.js")
    music_block = sound[sound.find("  music: {"):sound.find("\n  loops: {")]
    themes = set(re.findall(r'^\s{4}"?([a-z][\w-]*)"?: \{', music_block, re.M))
    scenes = {}
    for sid in ids:
        text = read(f"js/content/scenes/{sid}.js")
        era = re.search(r'\bera:\s*"(\w+)"', text)
        story = re.search(r"\bmusic:\s*(\(|function|async|[a-z]\w*\s*=>)", text)
        own = re.search(r'\bmusic:\s*"([\w-]+)"', text)
        scenes[sid] = {"era": era.group(1) if era else None, "story": bool(story), "own": own.group(1) if own else None}
    return ids, eras, themes, scenes


def heard_in(name, eras, scenes, table):
    """The scenes where a track of this name is heard, as the game decides (a scene the story decides is left out)."""
    out = []
    for sid, s in scenes.items():
        if s["story"]:
            continue
        m = table.get(sid) or s["own"] or eras.get(s["era"])
        if m == name:
            out.append(sid)
    return out


# ---------------------------------------------------------------- the list the game reads

def read_list():
    try:
        text = open(LIST, encoding="utf-8").read()
    except OSError:
        return {}
    m = re.search(r"export const MUSIC_FILES = (\{.*?\});\s*\n", text, re.S)
    return json.loads(m.group(1)) if m else {}


def write_list(tracks):
    scenes = {}
    for name in sorted(tracks):
        for sid in tracks[name].get("scenes", []):
            if sid in scenes and scenes[sid] != name:
                raise Stop(f"two tracks are made for {sid}: {scenes[sid]} and {name}. Take it out of one text file's scenes:")
            scenes[sid] = name
    text = (HEADER + "export const MUSIC_FILES = " + json.dumps(tracks, indent=1, sort_keys=True) + ";\n\n"
            + "export const MUSIC_SCENES = " + json.dumps(dict(sorted(scenes.items())), indent=1) + ";\n")
    tmp = LIST + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(tmp, LIST)


def digest(*paths):
    h = hashlib.sha256()
    for p in paths:
        if p and os.path.exists(p):
            with open(p, "rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    h.update(chunk)
        h.update(b"|")
    return h.hexdigest()[:16]


def stamp_of(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:10]


def clock(s):
    return f"{int(s // 60)}:{s % 60:06.3f}"


# ---------------------------------------------------------------- one track

def make(name, master, notes_path, facts, table):
    ids, eras, themes, scenes = facts
    notes = read_notes(notes_path)
    rate, chans, tags = probe(master)
    channels = 1 if chans == 1 else 2
    stored = wav_loop(master) if master.lower().endswith(".wav") else tag_loop(tags)
    pcm = decode(master, channels)
    total = len(pcm) // channels
    if total < RATE // 2:
        raise Stop("it is shorter than half a second")
    warn = []
    if master.lower().endswith(LOSSY):
        warn.append("the master is already compressed: a WAV or FLAC export sounds better")
    loop, how = loop_points(notes, rate, total / RATE, stored)

    # the loop, in samples at 48 kHz; the tail folded onto its start; the file cut at its end
    if loop:
        ls, le = round(loop[0] * RATE), round(loop[1] * RATE)
        if le > total and le - total <= RATE // 1000:
            le = total
        if not 0 <= ls < le <= total:
            raise Stop(f"the loop ({clock(ls / RATE)} to {clock(le / RATE)}) does not fit in the file ({clock(total / RATE)} long)")
        if le - ls < RATE // 2:
            raise Stop("the loop is shorter than half a second")
        after = total - le
        fold = min(after, round(TAIL * RATE), le - ls)
        if after < RATE // 4:
            warn.append("nothing runs past the loop's end to fold back (fine if it ends dry; otherwise export a few seconds more)")
        if after > fold:
            rest = pcm[(le + fold) * channels:]
            if rest and max(abs(min(rest)), abs(max(rest))) > 0.01:
                warn.append(f"the file goes on {clock(after / RATE)} past the loop's end; only the first {TAIL:.0f} s were folded back (a reverb tail), the rest left out")
        for i in range(fold * channels):
            pcm[ls * channels + i] += pcm[le * channels + i]
        del pcm[le * channels:]
        pcm.extend(pcm[ls * channels:(ls + min(round(PAD * RATE), le - ls)) * channels])     # (never played: the game loops at le)
        length = len(pcm) // channels
    else:
        ls = le = None
        length = total

    with tempfile.TemporaryDirectory() as tmp:
        raw = os.path.join(tmp, "cut.f32")
        with open(raw, "wb") as f:
            out = array.array("f", pcm)
            if sys.byteorder == "big":
                out.byteswap()
            f.write(out.tobytes())
        lufs, peak = loudness(raw, channels)
        gain = 0.0 if lufs <= -70 else TARGET - lufs
        if peak + gain > CEILING:
            held = peak + gain - CEILING
            gain -= held
            if held > 1.0:
                warn.append(f"its peaks hold it {held:.1f} dB under the house loudness (raise `volume:` if it sounds quiet)")
        # where the sound first rises above -50 dBFS (at the level it is made at): the game checks the same in what the browser
        # decodes, and if it comes later there (a codec's start-up silence left in), moves the loop points by as much
        floor = 0.00316 / (10 ** (gain / 20))
        onset = next((i // channels for i, v in enumerate(pcm) if v >= floor or v <= -floor), 0)
        high = str(notes.get("quality", "")).lower().startswith("high")
        inp = ["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(RATE), "-ac", str(channels), "-i", raw, "-af", f"volume={gain:.2f}dB"]
        meta = ["-metadata", f"title={notes.get('title', name)}"] + (["-metadata", f"artist={notes['by']}"] if notes.get("by") else [])
        webm, m4a = os.path.join(tmp, name + ".webm"), os.path.join(tmp, name + ".m4a")
        run(inp + meta + ["-c:a", "libopus", "-b:a", "128k" if high else "96k", "-vbr", "on", "-compression_level", "10", "-application", "audio", "-f", "webm", webm])
        run(inp + meta + ["-c:a", "aac", "-b:a", "160k" if high else "128k", "-movflags", "+faststart", m4a])
        # the Opus copy must decode to the exact length; the AAC copy may decode a little longer here (ffmpeg keeps the last
        # frame's padding, which browsers trim), never shorter
        got = length_of(webm, channels)
        if abs(got - length) > RATE // 1000:
            warn.append(f"{name}.webm decodes to {got - length:+d} samples: its loop may be a little off")
        got = length_of(m4a, channels)
        if not 0 <= got - length <= 2048 + RATE // 1000:
            warn.append(f"{name}.m4a decodes to {got - length:+d} samples: its loop may be a little off in browsers that take it")
        os.makedirs(OUT, exist_ok=True)
        for made in (webm, m4a):
            shutil.copyfile(made, os.path.join(OUT, os.path.basename(made)))

    files = {ext: f"audio/music/{name}.{ext}?v={stamp_of(os.path.join(OUT, f'{name}.{ext}'))}" for ext in ("webm", "m4a")}
    entry = {
        "title": notes.get("title", name),
        "files": files,
        "seconds": round(length / RATE, 6),
        "onset": round(onset / RATE, 6),
        "loop": [round(ls / RATE, 6), round(le / RATE, 6)] if loop else None,
        "channels": channels,
        "volume": float(notes.get("volume", "1").split()[0]),
        "fade": float(notes.get("fade", "1.2").split()[0].rstrip("s")),
        "lufs": round(lufs, 1),
        "gain": round(gain, 2),
        "bytes": {ext: os.path.getsize(os.path.join(OUT, f"{name}.{ext}")) for ext in ("webm", "m4a")},
        "source": {"file": os.path.basename(master), "digest": digest(master, notes_path)},
    }
    for key in ("by", "license"):
        if notes.get(key):
            entry[key] = notes[key]
    if "bpm" in notes:
        entry["bpm"] = float(notes["bpm"].split()[0])
        entry["meter"] = float(notes.get("meter", "4").split("/")[0].split()[0])
    if "downbeat" in notes:
        entry["downbeat"] = round(seconds_of(notes["downbeat"], rate, None), 6)
    if yes(notes.get("resume", "no")):
        entry["resume"] = True
    if yes(notes.get("stream", "no")):
        entry["stream"] = True
    wanted = [s.strip() for s in notes.get("scenes", "").replace(";", ",").split(",") if s.strip()]
    for sid in wanted:
        if sid not in ids:
            raise Stop(f"scenes: there is no scene called {sid} (js/content/scenes/index.js lists them)")
        if scenes[sid]["story"]:
            warn.append(f"{sid}: its story decides its music, so listing it changes nothing there (name the track after the theme it plays instead)")
    if wanted:
        entry["scenes"] = wanted
    return entry, how, warn


# ---------------------------------------------------------------- all of them

def masters():
    found = {}
    if not os.path.isdir(SRC):
        return found
    for f in sorted(os.listdir(SRC)):
        stem, ext = os.path.splitext(f)
        if ext.lower() in KINDS:
            if stem in found:
                print(f"  {f}: there is another master called {stem} here; using {os.path.basename(found[stem])}")
                continue
            found[stem] = os.path.join(SRC, f)
    return found


def show(tracks, facts):
    ids, eras, themes, scenes = facts
    table = {sid: name for name, t in tracks.items() for sid in t.get("scenes", [])}
    if not tracks:
        print("The game has no recorded music yet: every theme is synthesized.")
        return
    print(f"{'track':18s} {'length':>9s} {'loop':>19s} {'webm':>7s} {'m4a':>7s}  heard in")
    for name in sorted(tracks):
        t = tracks[name]
        loop = f"{clock(t['loop'][0])}-{clock(t['loop'][1])}" if t.get("loop") else "plays once"
        where = heard_in(name, eras, scenes, table)
        print(f"{name:18s} {clock(t['seconds']):>9s} {loop:>19s} {t['bytes']['webm'] / 1e6:6.2f}M {t['bytes']['m4a'] / 1e6:6.2f}M  "
              + (", ".join(where) if where else "(no scene yet: a cut-scene or a script may still ask for it)"))
    waiting = sorted(themes - set(tracks))
    if waiting:
        print("Still synthesized: " + ", ".join(waiting))


def main(argv):
    need_ffmpeg()
    facts = scene_facts()
    tracks = read_list()
    if "--list" in argv:
        show(tracks, facts)
        return 0
    if "--remove" in argv:
        names = [a for a in argv if not a.startswith("--")]
        for name in names:
            if name not in tracks:
                print(f"  {name}: the game has no recording of that name")
                continue
            del tracks[name]
            for ext in ("webm", "m4a"):
                p = os.path.join(OUT, f"{name}.{ext}")
                if os.path.exists(p):
                    os.remove(p)
            print(f"  {name}: taken out (its master in music-src/, if any, is untouched; take it out of there too, or it comes back next run)")
        write_list(tracks)
        return 0
    found = masters()
    named = [a for a in argv if not a.startswith("--")]
    for name in named:
        if name not in found:
            print(f"  {name}: no master called {name} in music-src/ (a .wav, .flac, .aif, .ogg or .opus)")
    todo = [n for n in found if (not named or n in named)]
    if not found:
        print(f"Nothing in {os.path.relpath(SRC, ROOT)}/ yet. Put a WAV there (named after the track, e.g. egypt.wav) with a text file beside it (egypt.txt): audio/README.md.")
    made, failed = 0, 0
    for name in todo:
        master = found[name]
        notes_path = os.path.splitext(master)[0] + ".txt"
        if not NAME.match(name):
            print(f"  {os.path.basename(master)}: rename it with lowercase letters, digits and hyphens only (egypt.wav, edo-sea.wav): the name is the track's")
            failed += 1
            continue
        if not named and "--all" not in argv and tracks.get(name, {}).get("source", {}).get("digest") == digest(master, notes_path) \
                and all(os.path.exists(os.path.join(OUT, f"{name}.{e}")) for e in ("webm", "m4a")):
            continue
        print(f"  {name}: {os.path.basename(master)}{' + ' + os.path.basename(notes_path) if os.path.exists(notes_path) else ' (no text file: the whole file loops)'}")
        try:
            entry, how, warn = make(name, master, notes_path, facts, tracks)
        except Stop as err:
            print(f"    NOT ADDED: {err}")
            failed += 1
            continue
        tracks[name] = entry
        loop = f"intro {clock(entry['loop'][0])}, loop to {clock(entry['loop'][1])}" if entry["loop"] else "plays once"
        print(f"    {loop} ({how}); {entry['lufs']} LUFS, set {entry['gain']:+.1f} dB; "
              f"{entry['bytes']['webm'] / 1e6:.2f} MB webm, {entry['bytes']['m4a'] / 1e6:.2f} MB m4a")
        if name in facts[2]:
            print(f"    replaces the synthesized theme \"{name}\"")
        for w in warn:
            print(f"    note: {w}")
        made += 1
    if made or not os.path.exists(LIST):
        try:
            write_list(tracks)
        except Stop as err:
            print(f"NOT WRITTEN: {err}")
            return 1
    print()
    show(tracks, facts)
    if made:
        print(f"\n{made} track(s) made. Listen on tools/music.html (python3 tools/serve.py, then http://localhost:8000/tools/music.html), then commit audio/music/ and js/content/music-files.js.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
