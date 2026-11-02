"""PAINT-21C: the checks of edo-street (the merchant street), as edo_dojima_check.py's.

  python3 edo_street_check.py          -> out/edo-street-check.png, and a line for each check (exit 1 if any fails)
"""

import os
import sys

from edo_dojima_check import HERE, check

STREET = dict(
    marks=["shore", "crossroads", "roadgod", "natsu", "prints", "senzo", "bench", "medicine", "combshop", "yomiuriFrom", "yomiuriTo", "kurataFrom",
           "komuso", "theatre"],
    off_walk=["senzo"],
    things=["roofs", "firetower", "kelpshop", "printshop", "printlines", "toyprints", "bench", "blocks", "baren", "bluepot", "medicine", "combsign",
            "crossroads", "roadgod", "noren", "drumtower", "watervendor", "natsu", "senzo", "yomiuri1", "yomiuri2", "kurata", "tatsu", "komuso"],
)

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    sys.exit(0 if check("edo-street", STREET, os.path.join(HERE, "out", "edo-street-check.png")) else 1)
