"""Paket kökü ve yapılandırma dizini — tek yerde.

Eski depoda her modül `Path(__file__).resolve().parents[2]` gibi kendi
derinlik sayısını taşıyordu; dosya bir dizin aşağı taşınınca sessizce yanlış
klasöre bakıyordu. Derinlik artık burada bir kez hesaplanır.

`QUAXIS_TEKNIK_CONFIG` ortam değişkeni verilirse yapılandırma oradan okunur —
testler ve farklı dağıtımlar için kaçış kapısı.
"""

from __future__ import annotations

import os
from pathlib import Path

#: `packages/teknik` — bu dosya `packages/teknik/quaxis/teknik/yollar.py`.
PAKET_KOK = Path(__file__).resolve().parents[2]

#: Motorun kendi yapılandırması (evren listesi, tatil takvimi, ayarlar).
#: Uygulama yapılandırması DEĞİL: motor tek başına da koşabilmeli.
CONFIG_KOK = Path(os.environ.get("QUAXIS_TEKNIK_CONFIG", PAKET_KOK / "config"))

#: OHLCV parquet önbelleğinin kökü.
#:
#: Ortam değişkeni olması bir kolaylık değil ZORUNLULUK: tarama motorunun
#: işçileri AYRI SÜREÇLERDE koşar ve `Store`'u kendileri kurar. Testlerde
#: `monkeypatch` süreç sınırını geçmez, `os.environ` geçer — veri kökü ancak
#: böyle yönlendirilebilir. Aynı sebeple üretimde de tek anahtarla taşınır.
VERI_KOK = Path(os.environ.get("QUAXIS_TEKNIK_DATA", "data/ohlcv"))
