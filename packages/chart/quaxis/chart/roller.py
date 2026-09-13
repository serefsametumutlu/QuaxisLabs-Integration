"""ChartSpec rol kümesi — KAPALI.

ADR-001 §4: "Kapalı bir rol kümesi kullanır — bilinmeyen stil adı sessizce
griye düşmek yerine `ValueError` atar."

Eski mimarinin kanıtlanmış hatalarından biri buydu: jenerik çizici tanımadığı
bir stil adını sessizce varsayılana düşürüyor, grafik "çizildi" görünüyor ama
seviye görünmez oluyordu. Rol adı burada yoksa ChartSpec üretilemez.

Rol ADI sözleşmedir; rolün hangi token'a düştüğü çizici tarafının bilgisidir.
Python tarafı renk bilmez — katman ayrımı kuralı: görselleştirme hesap yapmaz,
hesap da renk seçmez.
"""

from __future__ import annotations

from enum import Enum


class _Rol(str, Enum):
    """Bilinmeyen değerde okunur bir hata veren taban."""

    @classmethod
    def _missing_(cls, value: object):
        gecerli = ", ".join(sorted(u.value for u in cls))
        raise ValueError(
            f"{cls.__name__} için bilinmeyen rol: {value!r}. "
            f"Geçerli roller: {gecerli}. "
            f"Yeni bir rol gerekiyorsa ÖNCE buraya ve çizici tarafındaki rol "
            f"tablosuna eklenmeli — sessizce varsayılana düşmek yasak."
        )


class SeviyeRol(_Rol):
    """Yatay fiyat seviyesi. Fibo oranları oran-renklidir; 0.618 bilinçli
    olarak aksanın kendisidir (TASARIM_DILI §5)."""

    FIB_0 = "fib_0"
    FIB_236 = "fib_236"
    FIB_382 = "fib_382"
    FIB_500 = "fib_500"
    FIB_618 = "fib_618"
    #: ICT'nin "sweet spot"u — 0.62 ile 0.79'un ortası (0.705). Golden Zone'da
    #: karara değer seviye budur; klasik fibo merdiveninde karşılığı yok.
    FIB_705 = "fib_705"
    FIB_786 = "fib_786"
    FIB_1 = "fib_1"
    FIB_1272 = "fib_1272"
    FIB_1618 = "fib_1618"
    SEVIYE = "seviye"
    SON_FIYAT = "son_fiyat"


class AlanRol(_Rol):
    """Dolgulu bölge. Aksan ASLA mum ölçeğinde dolu bir leke değildir —
    bu roller düşük opaklıkta geniş dolgu olarak çizilir."""

    FORMASYON = "formasyon"
    BOLGE_ALTIN = "bolge_altin"
    BOLGE_ARZ = "bolge_arz"
    BOLGE_TALEP = "bolge_talep"


class CizgiRol(_Rol):
    """Nokta-nokta çizgi."""

    PROJEKSIYON = "projeksiyon"
    TREND = "trend"
    BAGLANTI = "baglanti"


class IsaretRol(_Rol):
    """Tek noktaya oturan işaret."""

    KOSE = "kose"
    TEMAS = "temas"
    #: Kurulumun sonucu. Aksan-nötr çizmek, "hedefe ulaştı" ile "stop oldu"yu
    #: aynı renge boyamak olurdu — sonuç YÖN bilgisidir.
    CIKIS_KAZANC = "cikis_kazanc"
    CIKIS_KAYIP = "cikis_kayip"


class EtiketRol(_Rol):
    """Serbest metin etiketi."""

    SWING_HH = "swing_hh"
    SWING_HL = "swing_hl"
    SWING_LH = "swing_lh"
    SWING_LL = "swing_ll"
    NOT = "not"


class RozetRol(_Rol):
    """Önder çizgili kutulu rozet — formasyonun durumu."""

    DURUM_TAMAMLANDI = "durum_tamamlandi"
    DURUM_ONAYLANDI = "durum_onaylandi"
    DURUM_IZLENIYOR = "durum_izleniyor"
    DURUM_GECERSIZ = "durum_gecersiz"


class Yon(_Rol):
    """Yön anlamı taşıyan tek şey. Aksandan BAĞIMSIZ token ailesi."""

    AL = "al"
    SAT = "sat"


#: Fibonacci oranı -> seviye rolü. Komposerler oranı elle role çevirmesin.
FIB_ROL: dict[float, SeviyeRol] = {
    0.0: SeviyeRol.FIB_0,
    0.236: SeviyeRol.FIB_236,
    0.382: SeviyeRol.FIB_382,
    0.5: SeviyeRol.FIB_500,
    0.618: SeviyeRol.FIB_618,
    # ICT 0.62 ve 0.79 yazar; bunlar klasik 0.618 ve 0.786'nın YUVARLANMIŞ
    # hâlidir, ayrı seviyeler değil. Aynı görsel ağırlığı taşırlar.
    0.62: SeviyeRol.FIB_618,
    0.705: SeviyeRol.FIB_705,
    0.786: SeviyeRol.FIB_786,
    0.79: SeviyeRol.FIB_786,
    1.0: SeviyeRol.FIB_1,
    1.272: SeviyeRol.FIB_1272,
    1.618: SeviyeRol.FIB_1618,
}


def fib_rol(oran: float) -> SeviyeRol:
    """Fibonacci oranının rolünü verir; tanımsız oranda ValueError atar."""
    try:
        return FIB_ROL[round(oran, 3)]
    except KeyError:
        gecerli = ", ".join(str(o) for o in sorted(FIB_ROL))
        raise ValueError(
            f"Tanımlı bir fibo oranı değil: {oran}. Tanımlı oranlar: {gecerli}. "
            f"Yeni oran, renk paletiyle birlikte kararlaştırılmadan eklenemez "
            f"(TASARIM_DILI §5: aksan ile çakışma her değişiklikte ölçülür)."
        ) from None
