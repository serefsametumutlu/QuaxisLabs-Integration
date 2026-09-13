"""Gösterge kataloğu — motorun bu paketi tanımadan çalıştırabildiği künyeler.

Bağımlılık yönü: motor yalnızca `core/catalog.py`'deki ARAYÜZÜ bilir;
somut göstergeler kendi kataloglarını kurup motora verir. Tarayıcı
işçileri ayrı süreçlerde koştuğu için katalog bir NESNE olarak değil,
`"modul.yolu:NITELIK"` adresi olarak geçirilir — fabrikalar süreç sınırını
turşulanarak geçemez.

    python tools/kalibrasyon.py --katalog "quaxis.teknik.indicators.katalog:KATALOG" \\
        --gosterge golden_zone --slug golden-zone
"""

from __future__ import annotations

from quaxis.teknik.core.catalog import Catalog, IndicatorSpec
from quaxis.teknik.indicators.golden_zone import META as GOLDEN_ZONE_META
from quaxis.teknik.indicators.golden_zone import olustur as golden_zone_olustur

KATALOG = Catalog.of(
    [
        IndicatorSpec(
            name=GOLDEN_ZONE_META.name,
            category=GOLDEN_ZONE_META.category,
            factory=golden_zone_olustur,
            supported_timeframes=GOLDEN_ZONE_META.supported_timeframes,
        ),
    ]
)

__all__ = ["KATALOG"]
