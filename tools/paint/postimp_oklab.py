"""Colour arithmetic for the game's paints (postimp_key.py): sRGB <-> OKLab (Bjorn Ottosson's perceptual space), hue
and chroma, and a gamut clip that keeps lightness and hue and gives up chroma.

Everything works on float32 arrays; an image is (h, w, 3) with sRGB values 0..1.
"""

import numpy as np

F32 = np.float32

_M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929],
                [0.2119034982, 0.6806995451, 0.1073969566],
                [0.0883024619, 0.2817188376, 0.6299787005]], dtype=np.float64)
_M2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468],
                [1.9779984951, -2.4285922050, 0.4505937099],
                [0.0259040371, 0.7827717662, -0.8086757660]], dtype=np.float64)
_M2i = np.linalg.inv(_M2)
_M1i = np.linalg.inv(_M1)


def to_linear(c):
    c = np.asarray(c, dtype=F32)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4).astype(F32)


def to_srgb(c):
    c = np.clip(np.asarray(c, dtype=F32), 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(c, 1 / 2.4) - 0.055).astype(F32)


def lin_to_lab(lin):
    lms = lin @ _M1.T.astype(F32)
    lms = np.cbrt(np.maximum(lms, 0))
    return (lms @ _M2.T.astype(F32)).astype(F32)


def lab_to_lin(lab):
    lms = lab @ _M2i.T.astype(F32)
    return ((lms ** 3) @ _M1i.T.astype(F32)).astype(F32)


def rgb_to_lab(rgb):
    return lin_to_lab(to_linear(rgb))


def lab_to_rgb(lab):
    """OKLab -> sRGB, clipped into the gamut by giving up chroma (lightness and hue kept)."""
    return to_srgb(np.clip(lab_to_lin(gamut(lab)), 0, 1))


def in_gamut(lab, eps=1e-4):
    lin = lab_to_lin(lab)
    return np.all((lin >= -eps) & (lin <= 1 + eps), axis=-1)


def gamut(lab, steps=14):
    """Bring colours that sRGB cannot show back inside, along the line of constant lightness and hue
    (a bisection on chroma, per pixel). Colours already inside are returned untouched."""
    lab = np.asarray(lab, dtype=F32)
    shape = lab.shape
    flat = lab.reshape(-1, 3).copy()
    L = np.clip(flat[:, 0], 0, 1)
    flat[:, 0] = L
    bad = ~in_gamut(flat)
    if not bad.any():
        return flat.reshape(shape)
    sub = flat[bad]
    lo = np.zeros(len(sub), F32)
    hi = np.ones(len(sub), F32)
    for _ in range(steps):
        mid = (lo + hi) / 2
        test = sub.copy()
        test[:, 1:] *= mid[:, None]
        ok = in_gamut(test)
        lo = np.where(ok, mid, lo)
        hi = np.where(ok, hi, mid)
    sub[:, 1:] *= lo[:, None]
    flat[bad] = sub
    return flat.reshape(shape)


def hex_to_rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], dtype=F32)


def hex_to_lab(h):
    return rgb_to_lab(hex_to_rgb(h)[None, :])[0]


def rgb_to_hex(c):
    c = np.clip(np.round(np.asarray(c, dtype=np.float64) * 255), 0, 255).astype(int)
    return "#%02x%02x%02x" % tuple(c)


def lab_to_hex(lab):
    return rgb_to_hex(lab_to_rgb(np.asarray(lab, dtype=F32)[None, :])[0])


def chroma(lab):
    return np.hypot(lab[..., 1], lab[..., 2])


def hue(lab):
    return np.arctan2(lab[..., 2], lab[..., 1])
