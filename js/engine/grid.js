// The size of the picture.
//
// The stage is one painted picture, 800 pixels wide and 600 high. Every position in a
// scene file (where someone stands, a clickable area, a walk outline, a base line) is a
// pixel on that picture, and so is every position inside the engine. There is no separate
// layout grid: what a painter measures on the picture is the number that goes in the file.

export const W = 800, H = 600;

/** The grid the kit's first drawings were made on (the old scene backdrops, the close-ups). */
export const OLD = [320, 200];

/**
 * Markup that was drawn on another grid, wrapped so that it is shown in the middle of the
 * picture, as large as will fit. For the old 320x200 drawings that is the band 800 wide and
 * 500 high, 50 pixels down from the top. Whatever falls outside the drawing's own grid is cut off.
 */
export function fit(markup, grid = OLD) {
  const [w, h] = grid, k = Math.min(W / w, H / h);
  return `<svg x="${(W - w * k) / 2}" y="${(H - h * k) / 2}" width="${w * k}" height="${h * k}" viewBox="0 0 ${w} ${h}">${markup}</svg>`;
}
