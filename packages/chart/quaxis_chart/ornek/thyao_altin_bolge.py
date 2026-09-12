"""ÖRNEK fikstür — `references/HRhIeAdbcAAL2_B.png` referansının sayıları.

Gerçek tarama çıktısı DEĞİLDİR. Gösterge katmanı Bölüm C'de sıfırdan
yazılacağı için (ADR-002) komposerin girdisi şimdilik elle kurulan bir
`FibDuzeltmeSonucu`dur. Sayılar referans görselden okundu:

    A = 209.10 (0.0)   X = 170.10 (1.0)   aralık = 39.00
    0.236 = 199.90     0.382 = 194.20     0.500 = 189.60
    0.618 = 185.00     0.786 = 178.45
    1.272 = 159.49 (D hedefi)             1.618 = 146.00 (azami risk)

Barlar, ONAYLANMIŞ maketteki (`docs/design/maket_v1.html`) üreteçle birebir
aynı doğrusal eşlenik üreteçten gelir; aynı tohum aynı seriyi verir. Böylece
Faz 4 çıktısı maketin yanına konup karşılaştırılabilir.
"""

from __future__ import annotations

import datetime as dt

from ..roller import Yon
from ..tipler import Bar, FibDuzeltmeSonucu, FibSeviyesi, Pivot

A_FIYAT = 209.10
X_FIYAT = 170.10
ARALIK = A_FIYAT - X_FIYAT

#: Pivotun onaylanması için gereken sağ bar sayısı (pivot_sag = 5).
PIVOT_SAG = 5

BAR_SAYISI = 140
SON_GUN = dt.date(2026, 9, 11)


def fib(oran: float) -> float:
    return round(A_FIYAT - oran * ARALIK, 2)


#: (bar sırası, fiyat, etiket, yapı)
DONUM = [
    (0, 181.40, None, None),
    (18, X_FIYAT, "X", "HL"),
    (48, A_FIYAT, "A", "LH"),
    (72, fib(0.786), "B", "HL"),
    (100, fib(0.236), "C", "LH"),
    (132, fib(1.272), "D", None),
    (139, 161.80, None, None),
]

SEVIYELER = [
    FibSeviyesi(0.0, fib(0.0), "A"),
    FibSeviyesi(0.236, fib(0.236)),
    FibSeviyesi(0.382, fib(0.382)),
    FibSeviyesi(0.5, fib(0.5)),
    FibSeviyesi(0.618, fib(0.618)),
    FibSeviyesi(0.786, fib(0.786)),
    FibSeviyesi(1.0, fib(1.0), "X"),
    FibSeviyesi(1.272, fib(1.272), "D hedefi"),
    FibSeviyesi(1.618, fib(1.618), "azami risk"),
]


def _uretec(tohum: int):
    """Maketteki JS üretecinin birebir karşılığı.

    JS'te `(seed*1664525 + 1013904223) & 0x7fffffff`; 32 bite kırpma ile 31
    bite maskeleme aynı düşük bitleri verdiği için Python'da tek maske yeter.
    """
    s = tohum

    def sonraki() -> float:
        nonlocal s
        s = (s * 1664525 + 1013904223) & 0x7FFFFFFF
        return s / 0x7FFFFFFF

    return sonraki


def _is_gunleri(son: dt.date, adet: int) -> list[int]:
    """Sondan geriye `adet` iş günü — BIST hafta sonu kapalı."""
    gunler: list[dt.date] = []
    g = son
    while len(gunler) < adet:
        if g.weekday() < 5:
            gunler.append(g)
        g -= dt.timedelta(days=1)
    gunler.reverse()
    return [int(dt.datetime.combine(x, dt.time(0, 0), dt.UTC).timestamp()) for x in gunler]


def barlar() -> list[Bar]:
    r = _uretec(20260912)
    zaman = _is_gunleri(SON_GUN, BAR_SAYISI)
    amp = ARALIK * 0.055
    ham: list[dict] = []

    for i in range(BAR_SAYISI):
        bas, bit = DONUM[0], DONUM[1]
        for k in range(len(DONUM) - 1):
            if DONUM[k][0] <= i <= DONUM[k + 1][0]:
                bas, bit = DONUM[k], DONUM[k + 1]
                break
        f = (i - bas[0]) / max(1, bit[0] - bas[0])
        orta = bas[1] + (bit[1] - bas[1]) * (f * f * (3 - 2 * f))

        salinim = (r() - 0.5) * amp + __import__("math").sin(i * 0.9) * amp * 0.35
        acilis = orta + salinim
        kapanis = orta + (r() - 0.5) * amp * 1.15 + (amp * 0.2 if bit[1] > bas[1] else -amp * 0.2)
        yuksek = max(acilis, kapanis) + r() * amp * 0.75
        dusuk = min(acilis, kapanis) - r() * amp * 0.75
        hacim = 0.35 + r() * 0.65 + (abs(kapanis - acilis) / amp) * 0.3
        ham.append({"o": acilis, "h": yuksek, "l": dusuk, "c": kapanis, "v": hacim})

    # Dönüm barlarını tam pivot fiyatına oturt — grafikte pivot, mumun
    # gövdesinin ortasında değil ucunda durmalı.
    for i, fiyat, etiket, _yapi in DONUM:
        if etiket is None:
            continue
        b = ham[i]
        tepe = etiket in ("A", "C")
        if tepe:
            b["h"] = fiyat
            b["c"] = fiyat - ARALIK * 0.012
            b["o"] = fiyat - ARALIK * 0.03
            b["l"] = b["o"] - ARALIK * 0.02
        else:
            b["l"] = fiyat
            b["c"] = fiyat + ARALIK * 0.012
            b["o"] = fiyat + ARALIK * 0.03
            b["h"] = b["o"] + ARALIK * 0.02

    return [
        Bar(
            t=zaman[i],
            acilis=round(b["o"], 2),
            yuksek=round(b["h"], 2),
            dusuk=round(b["l"], 2),
            kapanis=round(b["c"], 2),
            hacim=round(b["v"] * 1_000_000),
        )
        for i, b in enumerate(ham)
    ]


def sonuc() -> FibDuzeltmeSonucu:
    bs = barlar()
    zaman = [b.t for b in bs]

    pivotlar = [
        Pivot(
            t=zaman[i],
            fiyat=fiyat,
            onay_t=zaman[min(i + PIVOT_SAG, BAR_SAYISI - 1)],
            etiket=etiket,
            yapi=yapi,
        )
        for i, fiyat, etiket, yapi in DONUM
        if etiket is not None
    ]
    d = next(p for p in pivotlar if p.etiket == "D")

    return FibDuzeltmeSonucu(
        sembol="THYAO",
        ad="Türk Hava Yolları",
        zaman_dilimi="1G",
        barlar=bs,
        pivotlar=pivotlar,
        seviyeler=SEVIYELER,
        bolge=(0.618, 0.786),
        yon=Yon.SAT,
        durum="tamamlandı",
        tamamlanma=d,
    )
