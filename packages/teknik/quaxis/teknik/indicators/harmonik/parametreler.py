"""Harmonik formasyon parametreleri — K1 sözleşmesi.

Kural ve her sayının kaynağı: `docs/strateji/kaynak/harmonik-pesavento-K0.md`
(Pesavento & Jouflas, *Trade What You See*, 2007).

## Hangi sayı kitaptan, hangisi bizden

Bu ayrımı yazılı tutmak K0'ın en önemli maddesiydi; burada da yazılı:

| Sayı | Kaynak |
|---|---|
| `.382 / .50 / .618 / .786` geri çekilmeler | **kitap** |
| `1.0 / 1.272 / 1.618 / 2.0` uzantılar | **kitap** |
| Gartley'de D = XA'nın `.786`'sı | **kitap** (tüm ticaret örnekleri) |
| Kelebek'te stop = `1.618` | **kitap** |
| `.618` hedef | **kitap** |
| İçerideki AB=CD'nin CD/AB kümesi | **kitap** (AB=CD bölümü) |
| `tolerans` | **KİTAPTA YOK** — GEÇİCİ, K3'ten türetilecek |
| AB=CD'de stop = `1.272` | **kitap formül vermiyor**, gerekçesi aşağıda |
| `donus_max_bar` | **KİTAPTA YOK** — GEÇİCİ |

Kitabın vermediği bir yere sayı uydurmak, o sayıyı sonradan sonuca göre
seçme kapısını açar. Golden Zone'da aynı disiplini uyguladık: eşiklerin
nereden geldiği yazılı olmadığı için önceki projede 648 sembolde sıfır aday
üreten bir kalibrasyon kimsenin gözüne batmamıştı.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from quaxis.teknik.core.params import BaseParams

#: Kitabın geri çekilme oranları (Böl. 3). Hangi bacağın hangi oranı
#: tutturacağı ÖNCEDEN bilinmez; formasyon bunlardan HERHANGİ birine
#: uyuyorsa geçerlidir.
GERI_CEKILME: tuple[float, ...] = (0.382, 0.50, 0.618, 0.786)

#: İÇERİDEKİ AB=CD'nin CD/AB oranları (kitap, AB=CD bölümü): **1.0**
#: vakaların ~%40'ında, **1.27–2.00** ~%60'ında.
#:
#: Bu kümenin önemi ölçülmüş bir hatadan geliyor. "İçinde AB=CD bulunmalı"
#: kuralını önce `CD = AB` (yalnız 1.0) diye kodladım. Kelebek'te bu, D'nin
#: XA'nın 1.272'sinde sabit olmasıyla birleşince AB bacağını **tek bir
#: noktaya** çöktürüyordu (AB=.786 ve BC=.382) — yani kitabın tarif ettiği
#: formasyonların çoğu daha doğmadan eleniyordu. Kitabın kendi AB=CD bölümü
#: uzatılmış CD'yi açıkça sayıyor; doğru okuma bu.
ABCD_ORANLARI: tuple[float, ...] = (1.0, 1.272, 1.618, 2.0)


@dataclass(frozen=True)
class HarmonikParams(BaseParams):
    """Dört formasyonun PAYLAŞTIĞI parametreler."""

    #: Pivot onayı: bir salınım ucunun sağında/solunda kaç bar. Bir uç ancak
    #: sağındaki `pivot_sag` bar kapandığında BİLİNEBİLİR — non-repaint
    #: sözleşmesinin temeli budur. Golden Zone ile aynı değer: iki strateji
    #: farklı pivot tanımı kullanırsa sonuçları kıyaslanamaz.
    pivot_sol: int = 3
    pivot_sag: int = 3

    #: Bir oranın "tuttuğu" sayılması için izin verilen sapma (oran
    #: biriminde; 0.05 = ±5 puan). **KİTAPTA YOK.** Önceki projede kullanılan
    #: ±.05 kitaptan değil Carney'den ödünç alınmıştı.
    #:
    #: Bu TABAN değerdir; her formasyon kendi K3 değerini taşır (aşağıda).
    #: `K3: docs/olcum/harmonik-pesavento-K3-1D.md` §1 ve §7.
    tolerans: float = 0.05

    #: Geri çekilme bacaklarının uyması gereken oran kümesi (kitap, Böl. 3).
    geri_cekilme_oranlari: tuple[float, ...] = GERI_CEKILME

    #: D seviyesi hesaplandıktan sonra fiyata tanınan azami bar. Aşılırsa
    #: kurulum "süresi doldu" sayılır. **KİTAPTA YOK** — kitap bir süre
    #: sınırı vermez. Sınırsız beklemek ölçümü bozar: aylar sonra tesadüfen
    #: dokunulan bir seviye formasyonun sonucu sayılamaz. GEÇİCİ; takvimsel
    #: süre olduğu için zaman dilimine göre ÖLÇEKLENİR.
    #:
    #: TABAN değer; her formasyon kendi K3 değerini taşır. Taranarak değil
    #: DAĞILIMDAN okundu: gerçek dokunuşların %90'ı pencerenin içinde kalır.
    #: `K3: docs/olcum/harmonik-pesavento-K3-1D.md` §3 ve §7.
    donus_max_bar: int = 40

    #: Stop, hesaplanan stop seviyesinin ne kadar ötesine konur (çıpa
    #: bacağının oranı). 0 = tam seviye. Kitap "hemen ötesi" diyor, sayı
    #: vermiyor. GEÇİCİ.
    stop_tamponu: float = 0.0

    #: Hedef: AD salınımının bu oranı kadar geri çekilmesi (kitap: .618,
    #: ikinci hedef .786). Tek hedef ölçüyoruz — kademeli çıkış R dağılımını
    #: iyimser gösterir (bkz. K0 §4).
    hedef_orani: float = 0.618

    #: Üç bariyerli ölçümde zaman bariyeri (bar). GEÇİCİ.
    zaman_bariyeri: int = 40

    #: ATR periyodu (Wilder) — bağlam ölçümleri için; sinyal üretmez.
    atr_periyot: int = 14

    _BAR_FIELDS: ClassVar[frozenset[str]] = frozenset({"donus_max_bar", "zaman_bariyeri"})

    def __post_init__(self) -> None:
        if self.pivot_sol < 1 or self.pivot_sag < 1:
            raise ValueError("pivot kolları en az 1 bar olmalı")
        if not 0.0 < self.tolerans < 0.5:
            raise ValueError(
                f"tolerans 0 ile 0.5 arasında olmalı, alınan: {self.tolerans} — "
                "0.5'te oran kümesinin komşuları çakışır ve 'hangi orana uydu' "
                "sorusu anlamını yitirir"
            )
        if not self.geri_cekilme_oranlari:
            raise ValueError("geri çekilme oran kümesi boş olamaz")
        if any(not 0.0 < r < 1.0 for r in self.geri_cekilme_oranlari):
            raise ValueError(
                f"geri çekilme oranları 0 ile 1 arasında olmalı: "
                f"{self.geri_cekilme_oranlari}"
            )
        if not 0.0 < self.hedef_orani <= 1.0:
            raise ValueError(f"hedef oranı 0 ile 1 arasında olmalı: {self.hedef_orani}")
        if self.stop_tamponu < 0:
            raise ValueError("stop tamponu negatif olamaz")
        if self.donus_max_bar < 1:
            raise ValueError("dönüş penceresi en az 1 bar olmalı")


@dataclass(frozen=True)
class AbcdParams(HarmonikParams):
    """AB=CD — X'siz üç bacak."""

    # --- K3'ten türetilen eşikler · `K3: docs/olcum/harmonik-pesavento-K3-1D.md` §7 ---
    #: Tolerans taramasında 0.05 üst sınırı aştı (sembol başına yılda 3.48
    #: sinyal); iki sınırı sağlayan en dar değer 0.02.
    tolerans: float = 0.02
    #: Pivot kolu: 2 ve 3 üst sınırı aştı, 4 ve 5 geçti; kural ortancayı
    #: seçiyor. Dört formasyon içinde SADECE bunda 5 çıktı — AB=CD üç
    #: bacaklı olduğu için doğal olarak daha sık oluşuyor.
    pivot_sol: int = 5
    pivot_sag: int = 5
    #: Seçilen tolerans+pivot birleşiminde dokunuş süresinin %90'lık dilimi.
    donus_max_bar: int = 55

    #: CD / AB oranı. Kitap: **1.0** vakaların ~%40'ında (simetrik AB=CD),
    #: **1.27–2.00** ~%60'ında. Hangisi olacağı ÖNCEDEN bilinemez; tek bir
    #: seviye seçmek zorundayız çünkü seviyeye dokunma anı sinyalin ta
    #: kendisi — ikinci bir seviyeyi de beklemek, ilkinde açılmış işlemin
    #: üstüne ikinci bir işlem açmak olurdu. 1.0 seçildi: kitabın en çok
    #: örneklediği ve tek başına en sık görülen oran. GEÇİCİ — K3'ten.
    cd_orani: float = 1.0

    #: Stop seviyesinin CD/AB oranı. **Kitap AB=CD için stop formülü
    #: VERMİYOR** ("trader'ın risk toleransı"). Sabit bir puan uydurmak
    #: yerine kitabın KENDİ oran kümesindeki bir sonraki uzantı kullanıldı:
    #: 1.0'da girilir, 1.272'de çıkılır. Kelebek'in ("1.272'de gir, 1.618'de
    #: çık") kuralıyla birebir aynı mantık — o kural kitaptan.
    stop_orani: float = 1.272

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.cd_orani <= 0:
            raise ValueError("CD oranı pozitif olmalı")
        if self.stop_orani <= self.cd_orani:
            raise ValueError(
                f"stop oranı ({self.stop_orani}) giriş oranından ({self.cd_orani}) "
                "büyük olmalı — aksi hâlde stop girişin yanlış tarafına düşer"
            )


@dataclass(frozen=True)
class GartleyParams(HarmonikParams):
    """Gartley '222' — kitabın en çok üstünde durduğu formasyon."""

    # --- K3'ten türetilen eşikler · `K3: docs/olcum/harmonik-pesavento-K3-1D.md` §7 ---
    tolerans: float = 0.02
    pivot_sol: int = 4
    pivot_sag: int = 4
    donus_max_bar: int = 35

    #: D, XA bacağının bu kadarını geri çeker. Kitap kesin bir aralık
    #: yazmıyor ama **tüm ticaret örneklerinde .786**. Kitaptan.
    d_geri_cekilme: float = 0.786

    #: Formasyonun içinde bir AB=CD bulunması ZORUNLU mu (kitap: evet).
    #: Parametre olmasının sebebi ölçüm: şartın kenar EKLEYİP eklemediği
    #: `abcd_ham` payload alanıyla ayrıca ölçülebilir.
    abcd_sarti: bool = True

    #: İçerideki AB=CD'nin CD/AB oranı bu kümeden birine uymalı.
    abcd_oranlari: tuple[float, ...] = ABCD_ORANLARI

    #: O orana izin verilen sapma. **KİTAPTA YOK** — GEÇİCİ.
    abcd_tolerans: float = 0.10

    def __post_init__(self) -> None:
        super().__post_init__()
        if not 0.0 < self.d_geri_cekilme < 1.0:
            raise ValueError(
                f"D geri çekilmesi 0 ile 1 arasında olmalı: {self.d_geri_cekilme} — "
                "1'i aşarsa D, X'i geçer ve formasyon Kelebek olur"
            )
        if self.abcd_tolerans <= 0:
            raise ValueError("AB=CD toleransı pozitif olmalı")
        if not self.abcd_oranlari:
            raise ValueError("AB=CD oran kümesi boş olamaz")


@dataclass(frozen=True)
class KelebekParams(HarmonikParams):
    """Butterfly — D, X'in ÖTESİNE geçer."""

    # --- K3'ten türetilen eşikler · `K3: docs/olcum/harmonik-pesavento-K3-1D.md` §7 ---
    tolerans: float = 0.02
    pivot_sol: int = 4
    pivot_sag: int = 4
    #: Dört formasyonun en uzunu. Kelebek D'si X'in ÖTESİNDE olduğu için
    #: fiyatın oraya ulaşması daha uzun sürüyor — beklenen bir sonuç.
    donus_max_bar: int = 60

    #: D, XA'nın bu uzantısında tamamlanır. Kitap: 1.272 · 1.618 · 2.00 ·
    #: 2.618. Girişin yapıldığı seviye 1.272 (kitabın 'shaded area'sı).
    d_uzanti: float = 1.272

    #: Stop bu uzantının hemen dışında. **Kitaptan**: '1.272'de girildiyse
    #: 1.618'in hemen dışına'.
    stop_uzanti: float = 1.618

    #: Bunun ötesi formasyon DEĞİLDİR (kitap, geçersizlik koşulu).
    azami_uzanti: float = 2.618

    abcd_sarti: bool = True
    abcd_oranlari: tuple[float, ...] = ABCD_ORANLARI
    abcd_tolerans: float = 0.10

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.d_uzanti <= 1.0:
            raise ValueError(
                f"Kelebek'te D, X'i AŞMALI: uzantı 1.0'dan büyük olmalı, "
                f"alınan {self.d_uzanti}"
            )
        if not self.d_uzanti < self.stop_uzanti <= self.azami_uzanti:
            raise ValueError(
                f"uzantı sırası bozuk: giriş {self.d_uzanti} < stop "
                f"{self.stop_uzanti} <= azami {self.azami_uzanti} olmalı"
            )
        if self.abcd_tolerans <= 0:
            raise ValueError("AB=CD toleransı pozitif olmalı")
        if not self.abcd_oranlari:
            raise ValueError("AB=CD oran kümesi boş olamaz")


@dataclass(frozen=True)
class UcSurusParams(HarmonikParams):
    """Three Drives — üç ardışık uzantı sürüşü."""

    # --- K3'ten türetilen eşikler · `K3: docs/olcum/harmonik-pesavento-K3-1D.md` §7 ---
    #: TEK istisna: 0.02 ve 0.03'te sembol sayısı 100'ün ALTINDA kaldı
    #: (16 ve 85 sembol), yani iki sınırı sağlayan en dar değer 0.05.
    #: Üç sürüşün üçü birden dar toleransa uyamıyor.
    tolerans: float = 0.05
    pivot_sol: int = 4
    pivot_sag: int = 4
    donus_max_bar: int = 25

    #: Her sürüş, kendinden önceki geri çekilmenin bu uzantısıdır.
    #: Kitap: 1.272 veya 1.618 (genelde ikisinde de aynı oran).
    surus_uzanti: float = 1.272

    #: Stop, aynı bacağın bu uzantısının ötesinde. Kitap 'son salınım ucunun
    #: ötesi' diyor ama sayı vermiyor; sürüşün kendisi zaten son uç olduğu
    #: için ölçülebilir tek yapısal nokta bir sonraki uzantıdır. Kelebek'in
    #: kitaptan gelen kuralıyla aynı mantık.
    stop_uzanti: float = 1.618

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.surus_uzanti <= 1.0:
            raise ValueError(
                f"sürüş uzantısı 1.0'dan büyük olmalı ({self.surus_uzanti}) — "
                "aksi hâlde sürüş bir öncekini AŞMAZ ve formasyon oluşmaz"
            )
        if self.stop_uzanti <= self.surus_uzanti:
            raise ValueError(
                f"stop uzantısı ({self.stop_uzanti}) giriş uzantısından "
                f"({self.surus_uzanti}) büyük olmalı"
            )
