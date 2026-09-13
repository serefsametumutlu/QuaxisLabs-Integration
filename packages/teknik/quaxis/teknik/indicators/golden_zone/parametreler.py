"""Golden Zone (ICT OTE) parametreleri — K1 sözleşmesi.

**Bu dosyadaki sayıların hiçbirinin henüz gerekçesi yok.** ICT literatürü
0.62 / 0.705 / 0.79 diyor; kullanıcı kararı ise "eşiklerin tamamı K3
ölçümünden türetilsin". Yani buradaki değerler *arama noktasıdır*, kural
değil. K3 raporu yazılıp `docs/strateji/golden-zone.md`'nin K0 tablosundaki
`K3:` devirleri kapanana kadar her biri GEÇİCİdir ve öyle etiketlenmiştir.

Bunu yazılı tutmanın sebebi somut: önceki projede eşikler "makul göründüğü"
için seçilmiş, sonra 648 sembolde sıfır aday üretmişti ve bunu kimse fark
etmemişti çünkü hiçbir yerde "bu sayı nereden geldi" yazmıyordu.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from quaxis.teknik.core.params import BaseParams


@dataclass(frozen=True)
class GoldenZoneParams(BaseParams):
    """OTE kurulumunun parametreleri. Frozen: aynı veri + aynı parametre =
    bit bit aynı sonuç (`params_hash` bunu kaydeder)."""

    #: Bölgenin sığ ucu — düzeltmenin ilk geçerli temas seviyesi. GEÇİCİ.
    bolge_sig: float = 0.62
    #: Bölgenin derin ucu — son geçerli giriş. GEÇİCİ.
    bolge_derin: float = 0.79
    #: ICT'nin "sweet spot"u. Sinyal ÜRETMEZ; sadece payload'a yazılır ki
    #: K4 "derin girişler daha mı iyi" sorusunu ölçebilsin. GEÇİCİ.
    tatli_nokta: float = 0.705

    #: Pivot onayı: bir salınım ucunun sağında/solunda kaç bar. Bir pivot
    #: ancak sağındaki `pivot_sag` bar kapandığında BİLİNEBİLİR — sinyalin
    #: non-repaint olmasının temeli budur.
    pivot_sol: int = 3
    pivot_sag: int = 3

    #: Yer değiştirme bacağının asgari boyu, ATR katı cinsinden. Bu eşik
    #: "gürültüyü yapı kırılımı sanmayı" engeller. GEÇİCİ.
    yer_degistirme_atr: float = 1.5
    #: ATR periyodu (Wilder). TA'nın evrensel kısaltması; zaman dilimine
    #: göre ölçeklenmez (bkz. BaseParams._BAR_FIELDS docstring'i).
    atr_periyot: int = 14

    #: Kırılımdan sonra bölgeye dönüş için tanınan azami bar. Aşılırsa
    #: kurulum "süresi doldu" sayılır. GEÇİCİ — takvimsel süre olduğu için
    #: zaman dilimine göre ÖLÇEKLENİR.
    donus_max_bar: int = 20

    #: Stop, %100 çıpasının ne kadar ötesine konur (çıpa mesafesinin oranı).
    #: 0 = tam wick ucu. ICT "beyond this level" diyor ama sayı vermiyor;
    #: bu yüzden 0 başlangıç, gerçek değer K3'ten. GEÇİCİ.
    stop_tamponu: float = 0.0

    #: FVG sayılması için asgari boşluk, ATR katı. GEÇİCİ.
    fvg_min_atr: float = 0.1

    #: Üç bariyerli ölçümde zaman bariyeri (bar). GEÇİCİ.
    zaman_bariyeri: int = 40

    _BAR_FIELDS: ClassVar[frozenset[str]] = frozenset({"donus_max_bar", "zaman_bariyeri"})

    def __post_init__(self) -> None:
        if not 0.0 < self.bolge_sig < self.bolge_derin < 1.0:
            raise ValueError(
                f"bölge 0 ile 1 arasında ve sığ<derin olmalı: "
                f"sig={self.bolge_sig}, derin={self.bolge_derin}"
            )
        if not self.bolge_sig <= self.tatli_nokta <= self.bolge_derin:
            raise ValueError(
                f"tatlı nokta ({self.tatli_nokta}) bölgenin dışında "
                f"[{self.bolge_sig}, {self.bolge_derin}] — ölçülemeyen bir sayı"
            )
        if self.pivot_sol < 1 or self.pivot_sag < 1:
            raise ValueError("pivot kolları en az 1 bar olmalı")
        if self.yer_degistirme_atr <= 0:
            raise ValueError("yer değiştirme eşiği pozitif olmalı")
