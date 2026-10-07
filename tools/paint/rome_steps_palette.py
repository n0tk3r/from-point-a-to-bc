"""The palette of the temple-steps backdrop: the 160 colors chosen for it when it was first finished.

It is kept here, exactly, instead of being chosen afresh on every run. Choosing a palette looks at the
whole picture, so if it were chosen again after a small retouch every color in the picture would shift
by a hair; with the palette fixed, a retouch changes only the place that was retouched.
(To choose a new one, call finish() in rome_steps.py without `palette`, and print what palette_of returns.)"""

import base64

import numpy as np

_DATA = (
    "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"
)

PALETTE = np.frombuffer(base64.b64decode(_DATA), dtype="<f4").reshape(-1, 3).astype(np.float32)
