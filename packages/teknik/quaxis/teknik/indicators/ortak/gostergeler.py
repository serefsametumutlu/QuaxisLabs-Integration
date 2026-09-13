"""Ortak teknik göstergeler — tek bir stratejiye ait DEĞİL.

Bu fonksiyonlar Golden Zone dedektörü için yazılmıştı ve orada duruyordu.
Harmonik dedektörler de aynı bağlam ölçümlerini yazıyor; ikinci bir kopya
çıkarmak yerine buraya taşındı. Kopyalanmış bir ATR'nin iki yerde ayrışması
ölçüm sonuçlarını sessizce bozar.

**Hiçbiri sinyal üretmez.** Hepsi payload'a yazılan bağlam değerleridir;
hangisinin kenar eklediği K4'te ölçülür.

Isınma dolmadan hepsi NaN döner — ısınmayı sıfır saymak stratejiyi kayırır.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def atr(df: pd.DataFrame, periyot: int) -> np.ndarray:
    """Wilder ATR. İlk `periyot` bar NaN kalır — ısınma dolmadan eşik
    uygulanmaz; ısınmayı sıfır saymak stratejiyi kayırır."""
    y, d, k = (df["high"].to_numpy(float), df["low"].to_numpy(float),
               df["close"].to_numpy(float))
    onceki = np.concatenate(([np.nan], k[:-1]))
    tr = np.maximum(y - d, np.maximum(np.abs(y - onceki), np.abs(d - onceki)))
    wilder = pd.Series(tr).ewm(alpha=1.0 / periyot, adjust=False, min_periods=periyot)
    return wilder.mean().to_numpy()


def ema(kapanis: np.ndarray, periyot: int) -> np.ndarray:
    """Üstel hareketli ortalama. Isınma dolmadan NaN."""
    return pd.Series(kapanis).ewm(span=periyot, adjust=False, min_periods=periyot).mean().to_numpy()


def rsi(kapanis: np.ndarray, periyot: int = 14) -> np.ndarray:
    """Wilder RSI."""
    fark = np.diff(kapanis, prepend=np.nan)
    kazanc = pd.Series(np.where(fark > 0, fark, 0.0))
    kayip = pd.Series(np.where(fark < 0, -fark, 0.0))
    ag = kazanc.ewm(alpha=1.0 / periyot, adjust=False, min_periods=periyot).mean()
    al_ = kayip.ewm(alpha=1.0 / periyot, adjust=False, min_periods=periyot).mean()
    with np.errstate(divide="ignore", invalid="ignore"):
        rs = ag / al_
    return (100.0 - 100.0 / (1.0 + rs)).to_numpy()


def adx(df: pd.DataFrame, periyot: int = 14) -> np.ndarray:
    """Wilder ADX — trendin GÜCÜ (yönü değil)."""
    y, d = df["high"].to_numpy(float), df["low"].to_numpy(float)
    k = df["close"].to_numpy(float)
    up, dn = np.diff(y, prepend=np.nan), -np.diff(d, prepend=np.nan)
    art_dm = np.where((up > dn) & (up > 0), up, 0.0)
    eks_dm = np.where((dn > up) & (dn > 0), dn, 0.0)
    onceki = np.concatenate(([np.nan], k[:-1]))
    tr = np.maximum(y - d, np.maximum(np.abs(y - onceki), np.abs(d - onceki)))

    def _w(x):
        return pd.Series(x).ewm(alpha=1.0 / periyot, adjust=False, min_periods=periyot).mean()

    atr_ = _w(tr)
    with np.errstate(divide="ignore", invalid="ignore"):
        art_di = 100 * _w(art_dm) / atr_
        eks_di = 100 * _w(eks_dm) / atr_
        dx = 100 * (art_di - eks_di).abs() / (art_di + eks_di)
    return _w(dx.to_numpy()).to_numpy()


def macd_histogram(kapanis: np.ndarray) -> np.ndarray:
    """MACD(12,26,9) histogramı — momentumun ivmesi."""
    hizli = pd.Series(kapanis).ewm(span=12, adjust=False, min_periods=26).mean()
    yavas = pd.Series(kapanis).ewm(span=26, adjust=False, min_periods=26).mean()
    cizgi = hizli - yavas
    sinyal = cizgi.ewm(span=9, adjust=False, min_periods=9).mean()
    return (cizgi - sinyal).to_numpy()


def bollinger_genislik(kapanis: np.ndarray, periyot: int = 20) -> np.ndarray:
    """Bollinger bant genişliği / orta bant — sıkışma ölçüsü."""
    s = pd.Series(kapanis)
    orta = s.rolling(periyot, min_periods=periyot).mean()
    sapma = s.rolling(periyot, min_periods=periyot).std(ddof=0)
    with np.errstate(divide="ignore", invalid="ignore"):
        return ((4 * sapma) / orta).to_numpy()


def stokastik(df: pd.DataFrame, periyot: int = 14) -> np.ndarray:
    """%K — barın N barlık aralıktaki yeri."""
    y = pd.Series(df["high"].to_numpy(float)).rolling(periyot, min_periods=periyot).max()
    d = pd.Series(df["low"].to_numpy(float)).rolling(periyot, min_periods=periyot).min()
    k = pd.Series(df["close"].to_numpy(float))
    with np.errstate(divide="ignore", invalid="ignore"):
        return (100 * (k - d) / (y - d)).to_numpy()


def obv_egim(df: pd.DataFrame, periyot: int = 20) -> np.ndarray:
    """OBV'nin N barlık eğimi — hacim fiyatı teyit ediyor mu."""
    k = df["close"].to_numpy(float)
    h = df["volume"].to_numpy(float)
    yon = np.sign(np.diff(k, prepend=k[0]))
    obv = np.cumsum(yon * h)
    s = pd.Series(obv)
    return (s - s.shift(periyot)).to_numpy()


def guvenli(x: float) -> float | None:
    """NaN'ı None'a çevirir: ısınma dolmamış bir göstergeyi sayı gibi
    raporlamak, olmayan bilgiyi varmış gibi göstermektir."""
    return None if x is None or np.isnan(x) else float(x)
