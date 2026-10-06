"""Letter skeletons for Koine Road, the papyrus-hand display face.

Units: 1000 per em, baseline at y=0. Capitals are about 636 tall, the
x-height is about 480, ascenders reach about 690 and descenders about -230.
Each stroke is the centre line a reed pen would follow. A stroke may start
with a dict of pen options for that stroke (for example a bar that tapers).

Capitals that exist in the Greek book hand keep that form (alpha-shaped A,
lunate E and C, rounded mu-shaped M, rho-shaped P with a descender,
omega-shaped W, small O). Capitals Greek does not have (F, G, J, L, Q, R, S,
U, V) are drawn with the same pen and the same hooked stroke endings.

The papyri have no lowercase. The small letters here are new, written with
the same pen held a little finer.
"""
import math

T = 588   # top of a normal stem (centre line)
B = 96    # where a stem starts turning into its foot
F = 40    # bottom of a foot

BAR = dict(taper=0.30, end=0.02, start=0.22)      # a bar that runs dry towards its end
THIN = dict(start=0.55, end=0.0)


def arc(cx, cy, rx, ry, a0, a1, n=9):
    pts = []
    for i in range(n):
        a = math.radians(a0 + (a1 - a0) * i / (n - 1))
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    return pts


def stem(x, top=T, foot="l", head=True, bottom=None):
    """A vertical: a small flag at the head, a slight bow, a hooked foot."""
    b = B if bottom is None else bottom + (B - F)
    f = F if bottom is None else bottom
    pts = []
    if head:
        pts += [(x - 40, top - 6), (x - 8, top + 6), (x, top - 34)]
    else:
        pts += [(x, top)]
    pts += [(x - 8, (top + b) / 2), (x - 2, b + 30)]
    if foot == "l":
        pts += [(x - 14, b - 26), (x - 52, f)]
    elif foot == "r":
        pts += [(x + 12, b - 26), (x + 52, f + 2)]
    else:
        pts += [(x, f + 6)]
    return pts


G = {}


def glyph(name, strokes, dots=(), lsb=48, rsb=48, opts=None):
    G[name] = dict(strokes=strokes, dots=list(dots), lsb=lsb, rsb=rsb, opts=opts or {})


# ---- letters ----
glyph("A", [
    [(204, 610), (236, 648), (272, 588), (358, 378), (454, 150), (502, 68), (562, 46)],
    [(292, 528), (202, 330), (64, 104, "c"), (250, 130), (440, 174)],
], lsb=38, rsb=30)

glyph("B", [
    [(96, 656), (128, 674), (136, 640), (130, 380), (134, 74)],
    [(124, 650), (262, 674), (366, 608), (364, 508), (272, 426), (148, 398)],
    [(148, 398), (320, 400), (444, 308), (450, 186), (358, 80), (168, 50)],
    [BAR, (50, 54), (262, 38), (498, 52)],
], lsb=40, rsb=26)

_round = dict(cx=296, cy=314, rx=222, ry=268)
glyph("C", [
    arc(a0=66, a1=304, n=10, **_round),
    [(246, 580), (372, 592), (466, 566), (492, 522)],
], lsb=50, rsb=26)

glyph("D", [
    stem(136, foot=None),
    [(58, 578), (250, 592), (432, 520), (512, 330), (462, 150), (320, 60), (54, 48)],
], lsb=38, rsb=48)

glyph("E", [
    arc(a0=66, a1=304, n=10, **_round),
    [(246, 580), (372, 592), (460, 568), (482, 528)],
    [BAR, (90, 320), (320, 324), (560, 342)],
], lsb=50, rsb=6)

glyph("F", [
    stem(142),
    [BAR, (60, 574), (270, 592), (474, 596), (520, 546)],
    [BAR, (142, 332), (310, 336), (436, 348)],
], lsb=38, rsb=14)

glyph("G", [
    arc(a0=66, a1=298, n=10, **_round),
    [(246, 580), (372, 592), (466, 566), (492, 522)],
    [(346, 294), (498, 298, "c"), (496, 180), (492, 72)],
], lsb=50, rsb=44)

glyph("H", [
    stem(124),
    stem(480, foot="r", head=False),
    [BAR, (124, 326), (304, 336), (480, 340)],
], lsb=40, rsb=36)

# The foot of I only turns a little, so that it is not mistaken for J beside lowercase.
glyph("I", [[(86, 582), (118, 594), (126, 554), (118, 342), (124, 126), (116, 72), (96, 44)]], lsb=44, rsb=50)

glyph("J", [
    [(140, 582), (172, 594), (180, 554), (180, 300), (174, 20), (132, -114), (40, -152)],
], lsb=16, rsb=50)

glyph("K", [
    stem(126),
    [(140, 290), (292, 418), (424, 556), (462, 614)],
    [(198, 350), (324, 202), (466, 70), (546, 44)],
], lsb=40, rsb=16)

glyph("L", [
    stem(130, foot=None),
    [BAR, (54, 56), (284, 38), (510, 58)],
], lsb=36, rsb=20)

glyph("M", [
    [(142, 598), (128, 420), (118, 196), (96, 92), (48, 44)],
    [(142, 598), (170, 410), (232, 232), (330, 150), (428, 232), (490, 410), (518, 598)],
    [(518, 598), (532, 420), (542, 196), (566, 92), (616, 46)],
], lsb=36, rsb=36)

glyph("N", [
    stem(124),
    [(126, 582), (234, 394), (354, 216), (476, 62)],
    [(446, 626), (478, 640), (480, 350), (476, 50)],
], lsb=40, rsb=46)

glyph("O", [arc(206, 316, 158, 172, 100, 478, n=15)], lsb=50, rsb=50)

glyph("P", [
    [(92, 598), (126, 612), (136, 574), (130, 300), (134, -130), (120, -172), (84, -196)],
    [(124, 588), (264, 618), (386, 566), (416, 468), (360, 366), (240, 322), (146, 338)],
], lsb=38, rsb=40)

glyph("Q", [
    arc(246, 318, 180, 200, 100, 478, n=15),
    [(262, 170), (366, 44), (486, -46), (576, -64)],
], lsb=50, rsb=4)

glyph("R", [
    stem(132),
    [(120, 580), (258, 610), (378, 560), (408, 468), (352, 370), (234, 328), (144, 340)],
    [(234, 330), (342, 206), (464, 78), (544, 46)],
], lsb=38, rsb=14)

glyph("S", [
    [(436, 520), (380, 586), (266, 600), (158, 548), (124, 452), (196, 356), (318, 296),
     (410, 210), (396, 108), (300, 46), (170, 54), (88, 126)],
], lsb=50, rsb=48)

glyph("T", [
    [(36, 540), (62, 586), (270, 590), (490, 600), (534, 574)],
    stem(284, top=590, head=False),
], lsb=22, rsb=16)

glyph("U", [
    [(76, 580), (108, 594), (116, 556), (110, 330), (150, 134), (258, 48), (378, 114), (448, 290)],
    stem(456, foot="r", head=False),
], lsb=38, rsb=32)

glyph("V", [
    [(44, 582), (78, 594), (104, 548), (182, 360), (284, 56)],
    [(506, 612), (390, 356), (288, 54)],
], lsb=20, rsb=14)

glyph("W", [
    [(106, 590), (68, 420), (78, 210), (152, 74), (246, 64), (320, 180), (338, 380), (340, 476)],
    [(340, 476), (350, 220), (418, 76), (514, 64), (594, 180), (612, 410), (582, 590)],
], lsb=40, rsb=40)

glyph("X", [
    [(56, 584), (90, 596), (124, 548), (236, 400), (366, 210), (494, 58), (554, 42)],
    [(508, 612), (366, 430), (222, 230), (102, 68), (46, 44)],
], lsb=22, rsb=14)

glyph("Y", [
    [(40, 582), (74, 594), (104, 548), (208, 396), (286, 300)],
    [(516, 614), (368, 410), (286, 300)],
    stem(286, top=306, head=False),
], lsb=20, rsb=12)

glyph("Z", [
    [(62, 552), (92, 588), (270, 592), (492, 588, "c"), (292, 320), (92, 56, "c"), (300, 40), (536, 66)],
], lsb=34, rsb=24)

# A full-height O. The small O is the manuscript form and stays the default;
# the font swaps this one in when a capital O starts a word in lowercase ("Oh").
glyph("O.cap", [arc(290, 314, 216, 270, 100, 478, n=17)], lsb=50, rsb=50)

# ---- lowercase ----
# The papyri have one case only, so these are new letters written with the
# same pen. Where a Greek letter looks like ours it lends its shape: a from
# alpha, e the rounded epsilon, w from omega. First stems hook left at the
# foot and last strokes flick right, as in the capitals.
XT = 432    # top of the x-height (centre line)
ASC = 640   # top of an ascender
LC = dict(wscale=0.82, start=0.28, end=0.20, pool=6.5)   # a finer pen keeps the small counters open

_bowl = [(340, 394), (262, 434), (166, 410), (96, 320), (84, 196), (136, 90), (222, 48), (300, 92), (348, 220)]
_lround = dict(cx=244, cy=239, rx=166, ry=193)

glyph("a", [
    list(_bowl),
    stem(354, top=XT, foot="r", head=False),
], lsb=40, rsb=24, opts=LC)

glyph("b", [
    stem(120, top=ASC, foot=None),
    [(120, 290), (190, 400), (280, 434), (372, 372), (400, 240), (352, 104), (250, 46), (158, 64), (118, 120)],
], lsb=40, rsb=40, opts=LC)

glyph("c", [
    arc(a0=62, a1=304, n=10, **_lround),
    [(206, 428), (300, 438), (372, 412), (392, 374)],
], lsb=42, rsb=18, opts=LC)

glyph("d", [
    [(350, 330), (300, 410), (220, 434), (130, 384), (84, 252), (120, 110), (214, 46), (298, 80), (350, 168)],
    [(250, 652), (276, 600), (326, 470), (352, 320), (354, 136), (372, 70), (432, 46)],
], lsb=40, rsb=22, opts=LC)

glyph("e", [
    arc(a0=62, a1=304, n=10, **_lround),
    [(206, 428), (300, 438), (366, 414), (386, 378)],
    [BAR, (86, 246), (250, 250), (440, 266)],
], lsb=42, rsb=4, opts=LC)

glyph("f", [
    [(338, 606), (286, 648), (214, 640), (164, 570), (152, 420), (150, 250), (152, 110), (138, 70), (100, 40)],
    [BAR, (56, 402), (200, 412), (336, 420)],
], lsb=30, rsb=8, opts=LC)

glyph("g", [
    list(_bowl),
    [(354, 436), (354, 200), (352, 0), (330, -104), (256, -168), (150, -166), (84, -114)],
], lsb=40, rsb=40, opts=LC)

glyph("h", [
    stem(120, top=ASC, foot="l"),
    [(122, 290), (196, 400), (282, 434), (350, 384), (362, 260), (362, 126), (378, 66), (436, 44)],
], lsb=40, rsb=22, opts=LC)

glyph("i", [stem(116, top=XT, foot="r")], dots=[(112, 604, 50)], lsb=40, rsb=22, opts=LC)

glyph("j", [
    [(74, 414), (108, 434), (120, 396), (120, 200), (116, -20), (88, -120), (4, -160)],
], dots=[(118, 604, 50)], lsb=-40, rsb=44, opts=LC)

glyph("k", [
    stem(120, top=ASC, foot="l"),
    [(134, 206), (240, 308), (336, 404), (368, 446)],
    [(186, 258), (284, 150), (388, 64), (452, 42)],
], lsb=40, rsb=10, opts=LC)

glyph("l", [stem(118, top=ASC, foot="r")], lsb=40, rsb=22, opts=LC)

glyph("m", [
    stem(118, top=XT, foot="l"),
    [(120, 290), (176, 396), (240, 432), (300, 392), (316, 280), (316, 60)],
    [(318, 290), (376, 396), (440, 432), (500, 392), (514, 280), (514, 126), (530, 66), (588, 44)],
], lsb=40, rsb=22, opts=LC)

glyph("n", [
    stem(118, top=XT, foot="l"),
    [(120, 290), (188, 400), (268, 434), (334, 386), (348, 260), (348, 126), (364, 66), (422, 44)],
], lsb=40, rsb=22, opts=LC)

glyph("o", [arc(222, 239, 160, 193, 100, 478, n=15)], lsb=42, rsb=42, opts=LC)

glyph("p", [
    [(74, 414), (108, 434), (120, 396), (118, 150), (120, -110), (106, -152), (68, -182)],
    [(120, 290), (190, 400), (280, 434), (372, 372), (400, 240), (352, 104), (250, 46), (158, 64), (118, 120)],
], lsb=40, rsb=40, opts=LC)

glyph("q", [
    list(_bowl),
    [(354, 436), (354, 200), (356, -100), (372, -150), (424, -180)],
], lsb=40, rsb=14, opts=LC)

glyph("r", [
    stem(118, top=XT, foot="l"),
    [(120, 290), (176, 392), (244, 432), (312, 424), (346, 392)],
], lsb=40, rsb=10, opts=LC)

glyph("s", [
    [(330, 374), (290, 422), (214, 436), (132, 402), (110, 322), (160, 258), (250, 218), (320, 162),
     (312, 92), (250, 46), (150, 50), (82, 106)],
], lsb=42, rsb=40, opts=LC)

glyph("t", [
    [(132, 566), (152, 540), (150, 300), (160, 130), (198, 62), (268, 44), (332, 74)],
    [BAR, (48, 408), (190, 418), (330, 428)],
], lsb=26, rsb=14, opts=LC)

glyph("u", [
    [(74, 414), (108, 434), (120, 396), (114, 200), (150, 92), (230, 46), (308, 96), (350, 220)],
    stem(356, top=XT, foot="r", head=False),
], lsb=40, rsb=22, opts=LC)

glyph("v", [
    [(44, 416), (78, 434), (102, 394), (158, 240), (226, 54)],
    [(402, 444), (310, 230), (230, 52)],
], lsb=20, rsb=14, opts=LC)

glyph("w", [
    [(96, 430), (66, 300), (74, 150), (130, 64), (206, 54), (262, 140), (276, 280), (278, 352)],
    [(278, 352), (286, 160), (340, 64), (416, 54), (478, 140), (492, 300), (470, 430)],
], lsb=36, rsb=36, opts=LC)

glyph("x", [
    [(50, 418), (84, 434), (112, 396), (206, 270), (306, 132), (388, 54), (444, 42)],
    [(402, 444), (298, 300), (188, 150), (98, 62), (46, 44)],
], lsb=22, rsb=14, opts=LC)

glyph("y", [
    [(44, 416), (78, 434), (102, 394), (158, 240), (228, 70)],
    [(402, 444), (318, 240), (230, 44), (168, -86), (98, -150), (34, -160)],
], lsb=-10, rsb=14, opts=LC)

glyph("z", [
    [(58, 398), (86, 430), (216, 434), (366, 430, "c"), (228, 240), (78, 54, "c"), (228, 40), (396, 62)],
], lsb=30, rsb=22, opts=LC)

# ---- figures ----
glyph("zero", [arc(240, 314, 164, 274, 100, 478, n=15)], lsb=50, rsb=50)
glyph("one", [[(90, 466), (216, 596), (220, 330), (218, B), (184, F)]], lsb=38, rsb=56)
glyph("two", [[(96, 468), (150, 566), (268, 600), (386, 548), (404, 440), (304, 290),
               (96, 58, "c"), (296, 42), (486, 62)]], lsb=46, rsb=32)
glyph("three", [
    [(98, 556), (248, 600), (378, 546), (384, 440), (276, 350), (184, 338)],
    [(184, 338), (316, 326), (428, 232), (398, 108), (270, 42), (104, 80)],
], lsb=48, rsb=46)
glyph("four", [
    [(356, 598), (216, 400), (62, 214, "c"), (286, 212), (524, 222)],
    stem(366, top=598, head=False),
], lsb=32, rsb=22)
glyph("five", [
    [(466, 594), (286, 598), (150, 590, "c"), (136, 352, "c"), (264, 392), (406, 334),
     (438, 206), (354, 82), (224, 42), (98, 88)],
], lsb=46, rsb=36)
glyph("six", [[(406, 584), (266, 560), (148, 424), (102, 250), (156, 100), (264, 46), (384, 100),
               (418, 222), (344, 332), (234, 352), (132, 288)]], lsb=48, rsb=46)
glyph("seven", [[(64, 552), (94, 588), (264, 596), (470, 590, "c"), (358, 400), (260, 200), (214, 50)]],
      lsb=36, rsb=22)
glyph("eight", [[(270, 334), (158, 420), (146, 520), (266, 600), (386, 522), (374, 420), (270, 334),
                 (134, 222), (146, 100), (268, 42), (394, 100), (408, 224), (270, 334)]], lsb=48, rsb=48)
glyph("nine", [[(420, 420), (316, 312), (198, 302), (112, 400), (126, 522), (256, 600), (384, 542),
                (428, 400), (396, 200), (298, 70), (152, 46)]], lsb=48, rsb=46)

# ---- punctuation ----
glyph("period", [], dots=[(108, 62, 66)], lsb=46, rsb=46)
glyph("periodcentered", [], dots=[(108, 312, 60)], lsb=62, rsb=62)
glyph("comma", [[(122, 96), (134, 40), (88, -90)]], lsb=42, rsb=46, opts=THIN)
glyph("quotesingle", [[(122, 652), (130, 600), (90, 488)]], lsb=42, rsb=46, opts=THIN)
glyph("quotedbl", [[(122, 652), (130, 600), (90, 488)], [(290, 652), (298, 600), (258, 488)]],
      lsb=42, rsb=46, opts=THIN)
# opening quotes: the same mark turned round, heavy at the foot
glyph("quoteleft", [[(98, 494), (90, 548), (130, 658)]], lsb=42, rsb=46, opts=THIN)
glyph("quotedblleft", [[(98, 494), (90, 548), (130, 658)], [(266, 494), (258, 548), (298, 658)]],
      lsb=42, rsb=46, opts=THIN)
glyph("hyphen", [[(58, 300), (214, 316), (372, 306)]], lsb=46, rsb=46)
glyph("exclam", [[(134, 630), (132, 420), (130, 240)]], dots=[(130, 62, 66)], lsb=54, rsb=54)
glyph("question", [[(82, 500), (142, 592), (264, 614), (368, 546), (356, 440), (258, 352), (240, 240)]],
      dots=[(240, 62, 66)], lsb=42, rsb=42)
glyph("colon", [], dots=[(108, 62, 66), (108, 388, 60)], lsb=54, rsb=54)
glyph("semicolon", [[(122, 96), (134, 40), (88, -90)]], dots=[(118, 388, 60)], lsb=42, rsb=54, opts=THIN)
glyph("slash", [[(54, -40), (212, 310), (370, 668)]], lsb=30, rsb=30)
glyph("parenleft", [[(266, 708), (136, 500), (100, 300), (138, 100), (266, -98)]], lsb=46, rsb=16)
glyph("parenright", [[(74, 708), (204, 500), (240, 300), (202, 100), (74, -98)]], lsb=16, rsb=46)

glyph("emdash", [[BAR, (50, 300), (330, 318), (640, 308)]], lsb=40, rsb=40)
glyph("ellipsis", [], dots=[(108, 62, 62), (330, 60, 62), (552, 62, 62)], lsb=46, rsb=46)
glyph("ampersand", [
    [(470, 300), (410, 160), (300, 62), (180, 52), (104, 130), (112, 240), (210, 340), (310, 440),
     (336, 530), (280, 600), (200, 590), (160, 510), (190, 410), (300, 250), (420, 110), (500, 44)],
], lsb=46, rsb=30)

CMAP = {
    ".": "period", ",": "comma", "'": "quotesingle", "’": "quotesingle", "‘": "quoteleft",
    '"': "quotedbl", "“": "quotedblleft", "”": "quotedbl", "-": "hyphen", "–": "hyphen",
    "!": "exclam", "?": "question", ":": "colon", ";": "semicolon", "/": "slash", "(": "parenleft",
    ")": "parenright", "·": "periodcentered", "—": "emdash", "…": "ellipsis", "&": "ampersand",
    "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six",
    "7": "seven", "8": "eight", "9": "nine",
}
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER = "abcdefghijklmnopqrstuvwxyz"
