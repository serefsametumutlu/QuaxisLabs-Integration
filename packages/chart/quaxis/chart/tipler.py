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

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
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
    """Salınım Fibo ABCD / fibonacci düzeltme göstergesinin tipli sonucu."""

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


@dataclass(frozen=True)
class Capa:
    """OTE fibonacci çıpası.

    `t` çıpanın kendi barı, `onay_t` çıpanın BİLİNEBİLİR olduğu bar. İkisi
    farklıdır ve grafikte `onay_t` kullanılır — non-repaint sözleşmesinin
    çizim tarafındaki karşılığı budur.
    """

    t: int
    fiyat: float
    onay_t: int
    #: "%100" (bacağın dibi/stop tarafı) ya da "%0" (bacağın ucu/hedef tarafı).
    etiket: str


@dataclass(frozen=True)
class OTESonucu:
    """Golden Zone (ICT OTE) göstergesinin tipli sonucu.

    Harmonik formasyondan farkı: beş köşe yok, **tek bir yer değiştirme
    bacağı** ve onun düzeltme bölgesi var. Bu yüzden kendi tipi ve kendi
    komposeri var — `FibDuzeltmeSonucu`'nu zorlamak iki ayrı stratejiyi aynı
    torbaya koymak olurdu.
    """

    sembol: str
    ad: str
    zaman_dilimi: str
    barlar: Sequence[Bar]
    #: Bacağın iki ucu: %100 (dip/stop tarafı) ve %0 (uç/hedef tarafı).
    capa100: Capa
    capa0: Capa
    #: Yapı kırılımının olduğu bar ve kırılan salınım seviyesi.
    bos_t: int
    kirilan_seviye: float
    #: Çizilecek fibo seviyeleri (giriş, orta eşik, stop, hedef).
    seviyeler: Sequence[FibSeviyesi]
    #: Bölgenin sığ ve derin ucu — oran olarak (0.62, 0.79).
    bolge: tuple[float, float]
    #: Fiyatın bölgeye ilk girdiği bar: sinyalin `detected_at`'i.
    giris_t: int
    giris_fiyat: float
    yon: Yon
    durum: str
    #: K4 verdikti. Grafiğin künyesine AYNEN geçer.
    verdikt: str = ""
    #: Katman bayrakları — FİLTRE değil, ölçüm girdisi (bkz. dedektör).
    teyitler: Mapping[str, bool] = field(default_factory=dict)
    #: Süpürme varsa onun çıpası; yoksa kurulum süpürmesiz demektir.
    supurme: Capa | None = None
    #: Kurulum sonuçlandıysa çıkışın barı, fiyatı ve hangi bariyerin
    #: vurulduğu ("hedef" · "stop" · "zaman"). Sonuçlanmamışsa None.
    #: Bölge ve seviyeler burada BİTER — sonuçlanmış bir kurulumun
    #: seviyelerini sağa uzatmak, artık geçerli olmayan bir bölgeyi hâlâ
    #: varmış gibi göstermektir.
    cikis_t: int | None = None
    cikis_fiyat: float | None = None
    cikis_turu: str = ""

    def seviye(self, oran: float) -> FibSeviyesi:
        for s in self.seviyeler:
            if round(s.oran, 3) == round(oran, 3):
                return s
        raise ValueError(
            f"{oran} seviyesi sonuçta yok. Komposer eksik bir sonuçtan grafik "
            f"uyduramaz — gösterge onu üretmediyse çizilmez."
        )


@dataclass(frozen=True)
class HarmonikSonucu:
    """Pesavento harmonik formasyonunun tipli sonucu.

    Dört formasyon (AB=CD · Gartley · Butterfly · Three Drives) **aynı**
    tipi kullanır çünkü çizim tarafında farkları yalnız nokta sayısı ve
    oranlardır. Dört ayrı tip yazmak, dört ayrı komposer doğururdu ve
    aralarındaki tek fark bir döngünün uzunluğu olurdu.

    Ölçüm tarafında ise dördü AYRI künyedir — orada soru "hangisi
    çalışıyor" ve tek künyede toplamak o soruyu ölçülemez yapardı.
    """

    sembol: str
    ad: str
    zaman_dilimi: str
    barlar: Sequence[Bar]

    #: Formasyonun künyesi: `harmonik_abcd` · `harmonik_gartley` …
    formasyon: str
    #: ONAYLI pivotlar, sırayla. AB=CD'de A·B·C, Gartley/Kelebek'te
    #: X·A·B·C, Three Drives'ta O·S1·A·S2·C. **D burada YOKTUR** — D bir
    #: pivot değil, hesaplanmış bir fiyattır ve ayrı alanda durur.
    noktalar: Sequence[Capa]
    #: D: hesaplanan seviye ve fiyatın ona dokunduğu bar.
    d: Capa

    #: Giriş (= D fiyatı), stop ve hedef; hepsi formasyonun kendi
    #: geometrisinden gelir. `oran` alanı hangi fibo seviyesi olduklarını
    #: söyler, komposer rolü ondan türetir.
    seviyeler: Sequence[FibSeviyesi]

    yon: Yon
    durum: str
    #: K4'ün verdikti. Grafiğin künyesine AYNEN geçer.
    verdikt: str = ""
    #: Bacak oranları (`ab`, `bc`, `abcd`…). Grafikte bacak etiketi olur:
    #: formasyonun NEDEN formasyon olduğunu gösteren tek şey bunlar.
    oranlar: Mapping[str, float] = field(default_factory=dict)

    cikis_t: int | None = None
    cikis_fiyat: float | None = None
    cikis_turu: str = ""

    def seviye(self, ad: str) -> FibSeviyesi:
        for s in self.seviyeler:
            if s.ad == ad:
                return s
        raise ValueError(
            f"{ad!r} seviyesi sonuçta yok. Komposer eksik bir sonuçtan grafik "
            f"uyduramaz — gösterge onu üretmediyse çizilmez."
        )
