"""Depo kökü pytest yapılandırması.

`packages/*` altındaki her paket kendi köküyle `sys.path`'e eklenir; böylece
`quaxis.chart` ve `quaxis.teknik` tek bir **isim alanı paketi** (PEP 420)
altında birleşir. `quaxis/` klasörlerinde bilerek `__init__.py` YOKTUR —
olsaydı iki paket birbirini gölgelerdi.

Kurulum (`pip install -e`) gerektirmez: depo klonlanır klonlanmaz
`python -m pytest` çalışır.
"""

from __future__ import annotations

import pathlib
import sys

KOK = pathlib.Path(__file__).resolve().parent

for _paket in sorted((KOK / "packages").iterdir()):
    if (_paket / "quaxis").is_dir():
        _yol = str(_paket)
        if _yol not in sys.path:
            sys.path.insert(0, _yol)
