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
from quaxis.teknik.indicators.golden_zone import olustur_r_kati as golden_zone_r_kati
from quaxis.teknik.indicators.golden_zone.dedektor import META_R_KATI
from quaxis.teknik.indicators.kesitsel_momentum import META as KM_META
from quaxis.teknik.indicators.kesitsel_momentum import META_ATLAMALI as KM_META_12_1
from quaxis.teknik.indicators.kesitsel_momentum import olustur as km_olustur
from quaxis.teknik.indicators.kesitsel_momentum import olustur_atlamali as km_olustur_12_1
from quaxis.teknik.indicators.kesitsel_momentum.dedektor import META_DONUS
from quaxis.teknik.indicators.kesitsel_momentum.dedektor import olustur_donus as km_olustur_donus

KATALOG = Catalog.of(
    [
        IndicatorSpec(
            name=GOLDEN_ZONE_META.name,
            category=GOLDEN_ZONE_META.category,
            factory=golden_zone_olustur,
            supported_timeframes=GOLDEN_ZONE_META.supported_timeframes,
        ),
        # Aynı dedektör, hedefi sabit 2R. İki AYRI soru sorduğu için iki
        # ayrı künye: biri kurulumun kendisini, diğeri bölgenin derinlikten
        # arındırılmış öngörü gücünü ölçer.
        IndicatorSpec(
            name=META_R_KATI.name,
            category=META_R_KATI.category,
            factory=golden_zone_r_kati,
            supported_timeframes=META_R_KATI.supported_timeframes,
        ),
        # Evren-geneli: motor sembol başına iş AÇMAZ, evrenin tamamını tek
        # işte verir. Sıralama tanım gereği böyle çalışır.
        IndicatorSpec(
            name=KM_META.name, category=KM_META.category, factory=km_olustur,
            needs_universe=True, supported_timeframes=KM_META.supported_timeframes,
        ),
        # "12-1" varyantı: son ay atlanir. Hangisinin dogru oldugu K3'te
        # olculecek, o yuzden ikisi de AYRI kunye.
        IndicatorSpec(
            name=KM_META_12_1.name, category=KM_META_12_1.category,
            factory=km_olustur_12_1, needs_universe=True,
            supported_timeframes=KM_META_12_1.supported_timeframes,
        ),
        # Ortalamaya dönüş: AYRI bir hipotez, ayrı künye. Momentum'un
        # "tersi" değil — kendi ön kaydı ve kendi karar kuralı var.
        IndicatorSpec(
            name=META_DONUS.name, category=META_DONUS.category,
            factory=km_olustur_donus, needs_universe=True,
            supported_timeframes=META_DONUS.supported_timeframes,
        ),
    ]
)

__all__ = ["KATALOG"]
