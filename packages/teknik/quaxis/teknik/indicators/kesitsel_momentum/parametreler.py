"""Kesitsel Momentum parametreleri — K1 sözleşmesi.

Üç eşiğin üçü de **kaynaktan**, sayfa numarasıyla (Chan 2013, s.146'daki
`kentdaniel.m` kodu). Golden Zone'da hiçbir eşiğin gerekçesi yoktu; burada
tersine, ölçümden türetilecek tek şey likidite filtresi — o da kaynakta
hiç yok ve BIST'e özgü bir gereklilik.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from quaxis.teknik.core.params import BaseParams


@dataclass(frozen=True)
class KesitselMomentumParams(BaseParams):
    """Frozen: aynı veri + aynı parametre = bit bit aynı sonuç."""

    #: Geriye bakış penceresi. Kaynak: `lookback=252` (12 ay).
    geriye_bakis: int = 252

    #: Tutuş süresi. Kaynak: `holddays=25` (1 ay).
    #: **Ölçümde sinyal örtüşmesini de bu belirler** — bkz. dedektör.
    tutus: int = 25

    #: Evrenin üst dilimi. Kaynak: `topN=50`, S&P 500'de %10.
    #: BIST evreni farklı büyüklükte olduğu için SAYI değil ORAN korunur.
    ust_dilim: float = 0.10

    #: Sıralamadan önce atlanan son ay (21 gün).
    #:
    #: Akademik momentum literatürü genelde "12-1" kullanır: son ay
    #: atlanır, çünkü kısa vadeli **dönüş** etkisi momentumun tersine
    #: çalışır ve sinyali kirletir. Chan'ın kodu atlamıyor.
    #: **İkisi de ölçülecek**; karar K3'e bırakıldı (K0 §6).
    atlama_gun: int = 0

    #: Sıralamaya girmek için asgari ortalama ciro (TL).
    #: **Kaynakta YOK.** BIST'e özgü: ince sembolde 12 aylık getiri
    #: sıralaması fiyat değil gürültü sıralar. Eşik K3'ten türetilecek;
    #: 0 = filtre kapalı.
    asgari_ciro: float = 0.0

    #: Ciro ortalamasının penceresi.
    ciro_penceresi: int = 20

    #: Sıralamanın yapılabilmesi için o barda veri veren asgari sembol sayısı.
    #:
    #: **Ölçülmüş hata (2026-09-13).** Bu eşik yokken, yalnız 1 sembolün
    #: işlem gördüğü bir tarihte o sembolün yüzdelik sırası 1.0 çıkıyor ve
    #: OTOMATİK olarak "üst %10"a giriyordu. Tek sembollü bir kesitte
    #: sıralama diye bir şey yoktur; strateji o gün seçim YAPMAMALIDIR.
    #: Böyle tarihler BIST verisinde var (yarım günler, veri artıkları).
    asgari_evren: int = 20

    _BAR_FIELDS: ClassVar[frozenset[str]] = frozenset(
        {"geriye_bakis", "tutus", "atlama_gun", "ciro_penceresi"}
    )

    def __post_init__(self) -> None:
        if self.geriye_bakis < 2:
            raise ValueError("geriye bakış en az 2 bar olmalı")
        if self.tutus < 1:
            raise ValueError("tutuş en az 1 bar olmalı")
        if not 0.0 < self.ust_dilim <= 1.0:
            raise ValueError(f"üst dilim (0, 1] aralığında olmalı, alınan: {self.ust_dilim}")
        if self.atlama_gun < 0:
            raise ValueError("atlama negatif olamaz")
        if self.atlama_gun >= self.geriye_bakis:
            raise ValueError(
                f"atlama ({self.atlama_gun}) geriye bakıştan ({self.geriye_bakis}) "
                f"küçük olmalı — aksi hâlde ölçülecek pencere kalmaz"
            )
        if self.asgari_ciro < 0:
            raise ValueError("asgari ciro negatif olamaz")
        if self.asgari_evren < 2:
            raise ValueError(
                "asgari evren en az 2 olmalı — tek sembollü bir kesitte sıralama yoktur"
            )
