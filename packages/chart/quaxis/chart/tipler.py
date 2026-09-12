"""Komposer GİRDİLERİ — göstergelerin tipli sonuçları.

ADR-001 §4'teki zincirin ortası:

    gösterge → **TİPLİ SONUÇ** → o tipe ait komposer → ChartSpec

Buradaki tipler göstergenin ne ÜRETTİĞİNİ tanımlar, nasıl çizileceğini değil.
Çizim kararı komposerin, renk kararı çizicinin işidir.

Göstergelerin kendisi Bölüm C'de sıfırdan yazılacak (ADR-002). Bu dosya o
zaman `packages/teknik` tarafındaki sonuç tipleriyle eşleşecek; şimdilik
komposerin sözleşmesini sabitler ve örnek/fikstür verisiyle çalışır.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from .roller import Yon


@dataclass(frozen=True)
class Bar:
    """Ham OHLCV barı. `t` UTC epoch saniye."""

    t: int
    acilis: float
    yuksek: float
    dusuk: float
    kapanis: float
    hacim: float


@dataclass(frozen=True)
class Pivot:
    """Onaylanmış salınım noktası.

    `t` pivotun KENDİ barıdır; `onay_t` pivotun onaylandığı bardır. Sinyal
    her zaman `onay_t` taşır — non-repaint sözleşmesinin kalbi bu ayrımdır
    (README madde 1).
    """

    t: int
    fiyat: float
    onay_t: int
    etiket: Literal["X", "A", "B", "C", "D"]
    #: Salınım sınıfı: daha yüksek tepe, daha düşük dip…
    yapi: Literal["HH", "HL", "LH", "LL"] | None = None


@dataclass(frozen=True)
class FibSeviyesi:
    oran: float
    fiyat: float
    #: "A", "X", "D hedefi", "azami risk" gibi insan okuması.
    ad: str = ""


@dataclass(frozen=True)
class FibDuzeltmeSonucu:
    """Altın Bölge / fibonacci düzeltme göstergesinin tipli sonucu."""

    sembol: str
    ad: str
    zaman_dilimi: str
    barlar: Sequence[Bar]
    pivotlar: Sequence[Pivot]
    seviyeler: Sequence[FibSeviyesi]
    #: Bölgenin sığ ve derin ucu (0.618 / 0.786 varsayılan).
    bolge: tuple[float, float]
    yon: Yon
    durum: str
    #: Formasyonun tamamlandığı nokta — yoksa formasyon sürüyor demektir.
    tamamlanma: Pivot | None = None

    def pivot(self, etiket: str) -> Pivot:
        for p in self.pivotlar:
            if p.etiket == etiket:
                return p
        raise ValueError(
            f"'{etiket}' pivotu sonuçta yok. Komposer eksik bir sonuçtan grafik "
            f"uyduramaz — gösterge onu üretmediyse çizilmez."
        )
