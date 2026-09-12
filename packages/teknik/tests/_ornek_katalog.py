"""Test kataloğu ve sentetik veri sağlayıcısı.

Faz 5'in kapanma ölçütü **altyapının tek bir gösterge olmadan yeşil olması**.
Eski depoda tarama motorunun uçtan uca testi gerçek göstergelere ve gerçek
parquet önbelleğine bağlıydı; önbellek yoksa test ATLANIYORDU — yani çoğu
makinede hiçbir şey kanıtlamıyordu.

Burada motor, `_ornek_gostergeler.py`'deki sahte göstergelerle ve bellekte
üretilen sentetik OHLCV ile koşar: ağ yok, önbellek yok, atlama yok.

`KATALOG` modül seviyesinde SABİT bir nesnedir; motorun işçi süreçleri onu
`"_ornek_katalog:KATALOG"` adresinden kendi içlerinde çözer (fabrikalar
pickle edilemez, adres edilebilir).
"""

from __future__ import annotations

from datetime import datetime

import numpy as np
import pandas as pd
from _ornek_gostergeler import (  # noqa: E402  (conftest sys.path'i kurar)
    CenteredIndicator,
    CheatingIndicator,
    HonestIndicator,
    RankIndicator,
)
from quaxis.teknik.core.catalog import Catalog, IndicatorSpec
from quaxis.teknik.core.types import Market, Timeframe
from quaxis.teknik.data.providers.base import DataProvider

KATALOG_ADRESI = "_ornek_katalog:KATALOG"

KATALOG = Catalog.of(
    [
        IndicatorSpec(
            name="test.honest_sma_cross",
            category="testing",
            factory=HonestIndicator,
            supported_timeframes=(Timeframe.D1, Timeframe.H4),
        ),
        IndicatorSpec(
            name="test.centered_pivot",
            category="testing",
            factory=CenteredIndicator,
            supported_timeframes=(Timeframe.D1,),
        ),
        IndicatorSpec(
            name="test.rank",
            category="testing",
            factory=RankIndicator,
            needs_universe=True,
            supported_timeframes=(Timeframe.D1,),
        ),
    ]
)

#: Repaint testinden BİLEREK geçemeyen gösterge — registry'nin kapıyı gerçekten
#: tuttuğunu göstermek için ayrı katalogda durur.
HILELI_KATALOG = Catalog.of(
    [IndicatorSpec(name="test.cheating_pivot", category="testing", factory=CheatingIndicator)]
)


def sentetik_ohlcv(
    tohum: int = 7,
    bar: int = 320,
    baslangic_fiyat: float = 100.0,
    tf: Timeframe = Timeframe.D1,
    market: Market = Market.BIST,
) -> pd.DataFrame:
    """Deterministik OHLCV — kısa gürültülü baş + UZUN düz kuyruk.

    Düz kuyruk kasıtlı: `repaint_test`'in penceresi (son barlar) "artık yeni
    bir şeyin doğmadığı" bölgeye denk gelsin ki aday havuzu zamanlaması
    yanlış alarm üretmesin. Eski depodaki `_quiet_tailed_ohlcv` ile aynı
    gerekçe.
    """
    rng = np.random.default_rng(tohum)
    bas_n = min(100, bar // 3)
    bas = baslangic_fiyat + np.cumsum(rng.normal(0, 0.8, bas_n))
    kuyruk = np.full(bar - bas_n, bas[-1])
    close = np.concatenate([bas, kuyruk])

    open_ = np.empty_like(close)
    open_[0] = close[0]
    open_[1:] = close[:-1]
    high = np.maximum(open_, close) + 0.05
    low = np.minimum(open_, close) - 0.05
    volume = np.full(len(close), 1000.0)

    freq = {Timeframe.D1: "1D", Timeframe.H4: "4h", Timeframe.H1: "1h", Timeframe.W1: "1W"}[tf]
    tz = "Europe/Istanbul" if market is Market.BIST else "America/New_York"
    index = pd.date_range("2024-01-02", periods=len(close), freq=freq, tz=tz)
    return pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close, "volume": volume}, index=index
    )


class SentetikSaglayici(DataProvider):
    """Ağa çıkmayan sağlayıcı: her sembol için deterministik bir seri üretir.

    Sembol adından tohum türetilir, böylece aynı sembol her zaman aynı seriyi
    verir — deterministiklik kuralı testlerde de geçerlidir.
    """

    def __init__(self, bar: int = 320) -> None:
        self._bar = bar

    def fetch(
        self,
        symbol: str,
        market: Market,
        timeframe: Timeframe,
        start: datetime,
        end: datetime,
    ) -> pd.DataFrame:
        tohum = sum(ord(c) for c in symbol)
        df = sentetik_ohlcv(
            tohum=tohum,
            bar=self._bar,
            baslangic_fiyat=50.0 + (tohum % 40),
            tf=timeframe,
            market=market,
        )
        return self._finalize(df, market)
