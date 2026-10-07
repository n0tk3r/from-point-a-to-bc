// Effects drawn on the <canvas> layer. Canvas is the right tool when hundreds of
// short-lived shapes change every frame; everything else stays in SVG and CSS.
// Effects run on the game clock, so they pause and skip with the rest of the game.

const NEON = ["#5ef2ff", "#ff5ec8", "#b58cff"];

/** The time tunnel: rings rushing past, with dates flying out of the middle.
    Returns a function that stops it. */
export function tunnel(canvas, clock, { dates = [], calm = false } = {}) {
  const ctx = canvas.getContext("2d");
  const W = canvas.width, H = canvas.height, cx0 = W / 2, cy0 = H / 2;
  const u = W / 800;                   // the sizes below are pixels on the 800x600 picture; on a canvas of another size they follow it
  const speed = calm ? 0.25 : 1;       // players who ask for less motion get a slow drift
  let t = 0;
  canvas.classList.add("on");

  const stop = clock.every((dt) => {
    t += (dt / 1000) * speed;
    ctx.globalAlpha = 1;
    ctx.fillStyle = "#07040d";
    ctx.fillRect(0, 0, W, H);

    // streaks of starlight
    for (let i = 0; i < 46; i++) {
      const a = i * 2.399, z = (i * 0.137 + t * 0.9) % 1;
      const r0 = z * z * W * 0.62, r1 = r0 + (5 + z * 32) * u;
      ctx.globalAlpha = z;
      ctx.strokeStyle = "#f6e3b8";
      ctx.lineWidth = (1.25 + z * 1.25) * u;
      ctx.beginPath();
      ctx.moveTo(cx0 + Math.cos(a) * r0, cy0 + Math.sin(a) * r0 * 0.7);
      ctx.lineTo(cx0 + Math.cos(a) * r1, cy0 + Math.sin(a) * r1 * 0.7);
      ctx.stroke();
    }

    // eight-sided rings, far to near
    const rings = 12;
    for (let i = 0; i < rings; i++) {
      const z = (i / rings + t * 0.32) % 1;
      const r = Math.pow(z, 2.3) * W * 0.8 + 4 * u;
      const cx = cx0 + Math.sin(t * 0.9 + z * 4) * 28 * u * (1 - z);
      const cy = cy0 + Math.cos(t * 0.7 + z * 3) * 18 * u * (1 - z);
      ctx.strokeStyle = NEON[i % 3];
      ctx.globalAlpha = 0.12 + z * 0.88;
      ctx.lineWidth = (1.25 + z * 7.5) * u;
      ctx.beginPath();
      for (let k = 0; k <= 8; k++) {
        const a = (k / 8) * Math.PI * 2 + t * (i % 2 ? 0.5 : -0.5) + i;
        const px = cx + Math.cos(a) * r, py = cy + Math.sin(a) * r * 0.72;
        if (k) ctx.lineTo(px, py); else ctx.moveTo(px, py);
      }
      ctx.stroke();
    }

    // the years going by
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillStyle = "#f6e3b8";
    dates.forEach((label, i) => {
      const z = t * 0.26 - i * 0.2;
      if (z <= 0 || z >= 1) return;
      const a = i * 2.1 + 0.6, d = z * z;
      ctx.globalAlpha = Math.min(1, z * 4) * Math.min(1, (1 - z) * 4);
      ctx.font = `${Math.round((12 + d * 80) * u)}px "Koine Road", Georgia, serif`;
      ctx.fillText(label, cx0 + Math.cos(a) * d * W * 0.36, cy0 + Math.sin(a) * d * H * 0.34);
    });

    // the bright middle
    ctx.globalAlpha = 1;
    const core = 58 * u;
    const glow = ctx.createRadialGradient(cx0, cy0, 0, cx0, cy0, core);
    glow.addColorStop(0, "rgba(255,255,255,0.95)");
    glow.addColorStop(0.3, "rgba(94,242,255,0.35)");
    glow.addColorStop(1, "rgba(94,242,255,0)");
    ctx.fillStyle = glow;
    ctx.fillRect(cx0 - core, cy0 - core, core * 2, core * 2);
  });

  return () => {
    stop();
    canvas.classList.remove("on");
    ctx.clearRect(0, 0, W, H);
  };
}
