"""`validate_ohlcv`'nin high/low toleransı — iki yönü de kilitli.

**Ölçülmüş gerçek hata (2026-09-13).** BIST evreninin ~%30'u
"high >= max(open, close) ihlali" ile reddediliyordu. AKBNK, AEFES, AGESA
gibi en likit bankalar/holdingler bile eleniyordu — "bozuk veri" değildi.

Sebep ölçüldü: yfinance `auto_adjust=True` ile OHLC'yi bir düzeltme
katsayısıyla ÇARPIYOR. Ham veride birbirine EŞİT olan `high` ve `close`,
çarpımdan sonra double'ın son bitinde ayrışıyor — AKBNK'te göreli fark
1.2e-16, AEFES'te 1.6e-16. Yani tam bir ULP.

Tolerans buradan gevşetilirse kapı ardına kadar açılır; o yüzden testin
İKİ yönü de var: ULP gürültüsü geçmeli, gerçek bir hata (AGHOL'ün ölçülen
4.1e-3 göreli low ihlali) geçmemeli.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from quaxis.teknik.core.errors import OHLCVError
from quaxis.teknik.core.types import validate_ohlcv


def _df(o, y, d, k) -> pd.DataFrame:
    idx = pd.date_range("2024-01-01", periods=len(k), freq="1D", tz="UTC")
    return pd.DataFrame(
        {"open": o, "high": y, "low": d, "close": k, "volume": np.ones(len(k))},
        index=idx, dtype=float,
    )


def test_ulp_gurultusu_reddedilmez() -> None:
    """Bir ULP'lik high sapması veriyi bozmaz; reddetmek evrenin üçte birini
    atmak demekti."""
    kapanis = 47.83
    df = _df([47.0], [np.nextafter(kapanis, 0.0)], [46.0], [kapanis])
    validate_ohlcv(df)  # fırlatmamalı


def test_ulp_gurultusu_low_tarafinda_da_reddedilmez() -> None:
    acilis = 12.615
    df = _df([acilis], [13.0], [np.nextafter(acilis, np.inf)], [12.9])
    validate_ohlcv(df)


def test_gercek_high_ihlali_hala_reddedilir() -> None:
    """%0.4'lük bir sapma aritmetik artığı değil, veri hatasıdır."""
    with pytest.raises(OHLCVError, match="high >= max"):
        validate_ohlcv(_df([100.0], [100.0], [99.0], [100.4]))


def test_gercek_low_ihlali_hala_reddedilir() -> None:
    """AGHOL'de ölçülen gerçek hata bu büyüklükteydi (4.1e-3 göreli)."""
    with pytest.raises(OHLCVError, match="low <= min"):
        validate_ohlcv(_df([100.0], [101.0], [100.41], [100.0]))


def test_hata_mesaji_sapmanin_buyuklugunu_soyler() -> None:
    """"İhlal var" yetmez: ULP gürültüsü mü gerçek hata mı, mesajdan
    anlaşılmalı — yoksa bir dahaki sefere yine ölçmek gerekir."""
    with pytest.raises(OHLCVError, match=r"göreli sapma .*tolerans"):
        validate_ohlcv(_df([100.0], [100.0], [99.0], [105.0]))
