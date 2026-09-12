"""Teknik paketi testleri için ortak ayarlar.

`_ornek_gostergeler.py` bu klasörden düz `import` ile bulunsun diye klasör
`sys.path`'e eklenir — testler paket DEĞİL, dosya olarak toplanır.
"""

from __future__ import annotations

import pathlib
import sys

BURASI = pathlib.Path(__file__).resolve().parent
if str(BURASI) not in sys.path:
    sys.path.insert(0, str(BURASI))


def pytest_configure(config) -> None:
    config.addinivalue_line(
        "markers", "network: ağ erişimi ister; varsayılan koşuda atlanır (-m network ile koşar)"
    )
