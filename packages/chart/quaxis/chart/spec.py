"""ChartSpec v1 — çizim kütüphanesinden bağımsız, versiyonlu çizim sözleşmesi.

    gösterge → TİPLİ sonuç → KOMPOSER → ChartSpec (JSON)
                                          ├→ web çizici (etkileşimli)
                                          └→ PNG çizici (rapor/Telegram)

Bu dosya sözleşmenin kendisidir. Eski mimarinin üç kanıtlanmış hatasını
YAPISAL OLARAK imkânsız kılar (ADR-001 §4):

1. **Bilinmeyen rol sessizce griye düşemez.** Roller kapalı bir kümedir
   (`roller.py`); tanınmayan ad `ValueError` atar.
2. **Panel y aralığı keyfi katmanlardan hesaplanamaz.** Varsayılan aralık
   YALNIZCA o panele verilen serilerden gelir. Komposer bilinçli olarak
   genişletmek isterse `y` alanını AÇIKÇA yazar — ve yazdığı aralık serinin
   tamamını içermek zorundadır, yoksa doğrulama düşer. Böylece "bir katman
   grafiği ezdi" hatası sessizce olamaz.
3. **Seriler iki uca indirgenemez.** Her seri tam dizi taşır; nokta sayısı ve
   zaman sırası doğrulanır.

Zaman birimi: **UTC epoch saniye (int)**. Hem motor hem çizici için tek anlamı
olan tek gösterim.
"""

from __future__ import annotations

import dataclasses
import json
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Literal

from .roller import AlanRol, CizgiRol, EtiketRol, IsaretRol, RozetRol, SeviyeRol, Yon

SURUM = "1.0"

# ---------------------------------------------------------------- temel tipler


@dataclass(frozen=True)
class Nokta:
    """Zaman-fiyat noktası. `t` UTC epoch saniye."""

    t: int
    fiyat: float


@dataclass(frozen=True)
class Mum:
    t: int
    acilis: float
    yuksek: float
    dusuk: float
    kapanis: float

    def dogrula(self) -> None:
        govde_alt = min(self.acilis, self.kapanis)
        govde_ust = max(self.acilis, self.kapanis)
        if not (self.dusuk <= govde_alt and self.yuksek >= govde_ust):
            raise ValueError(
                f"Tutarsız mum (t={self.t}): yüksek {self.yuksek} / düşük {self.dusuk} "
                f"açılış {self.acilis} / kapanış {self.kapanis} aralığını kapsamıyor."
            )


@dataclass(frozen=True)
class HacimBari:
    t: int
    hacim: float
    yon: Yon


# ---------------------------------------------------------------------- panel


@dataclass(frozen=True)
class YAraligi:
    """Komposerin BİLİNÇLİ olarak yazdığı fiyat aralığı."""

    alt: float
    ust: float
    #: Neden genişletildi? Doğrulama değil, insan için: ChartSpec okunduğunda
    #: "bu aralık niye böyle" sorusunun cevabı dosyada dursun.
    gerekce: str = ""


@dataclass(frozen=True)
class Panel:
    id: str
    tur: Literal["fiyat", "hacim"]
    #: Levha yüksekliğinin oranı. Panellerin toplamı 1.0 olmalı.
    oran: float
    y: YAraligi | None = None


# --------------------------------------------------------------------- seriler


@dataclass(frozen=True)
class MumSerisi:
    id: str
    panel: str
    veri: Sequence[Mum]
    tur: Literal["mum"] = "mum"


@dataclass(frozen=True)
class HacimSerisi:
    id: str
    panel: str
    veri: Sequence[HacimBari]
    tur: Literal["hacim"] = "hacim"


Seri = MumSerisi | HacimSerisi


# -------------------------------------------------------------------- katmanlar


@dataclass(frozen=True)
class Seviye:
    """Yatay fiyat seviyesi. Sağ kenarda etiketlenir."""

    rol: SeviyeRol
    fiyat: float
    etiket: str
    panel: str = "fiyat"
    #: Seviyenin başladığı bar; None ise levhanın soluna kadar uzanır.
    baslangic: int | None = None
    #: Seviyenin BİTTİĞİ bar; None ise levhanın sağına kadar uzanır.
    #: Sonuçlanmış bir kurulumun seviyelerini sağa uzatmak, artık geçerli
    #: olmayan bir bölgeyi hâlâ varmış gibi göstermektir (K5 i2'de görüldü).
    bitis: int | None = None
    tur: Literal["seviye"] = "seviye"


@dataclass(frozen=True)
class Alan:
    """Dolgulu çokgen ya da yatay bant. En az üç nokta."""

    rol: AlanRol
    noktalar: Sequence[Nokta]
    panel: str = "fiyat"
    etiket: str = ""
    tur: Literal["alan"] = "alan"


@dataclass(frozen=True)
class Bant:
    """İki fiyat arasındaki yatay bant (altın bölge gibi)."""

    rol: AlanRol
    alt: float
    ust: float
    panel: str = "fiyat"
    etiket: str = ""
    baslangic: int | None = None
    #: Bandın BİTTİĞİ bar; None ise levhanın sağına kadar uzanır.
    bitis: int | None = None
    tur: Literal["bant"] = "bant"


@dataclass(frozen=True)
class Cizgi:
    rol: CizgiRol
    noktalar: Sequence[Nokta]
    panel: str = "fiyat"
    tur: Literal["cizgi"] = "cizgi"


@dataclass(frozen=True)
class Isaret:
    rol: IsaretRol
    nokta: Nokta
    metin: str = ""
    yerlesim: Literal["ust", "alt"] = "ust"
    panel: str = "fiyat"
    tur: Literal["isaret"] = "isaret"


@dataclass(frozen=True)
class Etiket:
    rol: EtiketRol
    nokta: Nokta
    metin: str
    yerlesim: Literal["ust", "alt"] = "ust"
    panel: str = "fiyat"
    tur: Literal["etiket"] = "etiket"


@dataclass(frozen=True)
class Rozet:
    """Önder çizgili kutulu rozet — formasyonun durumu."""

    rol: RozetRol
    nokta: Nokta
    metin: str
    yon: Yon
    panel: str = "fiyat"
    tur: Literal["rozet"] = "rozet"


Katman = Seviye | Alan | Bant | Cizgi | Isaret | Etiket | Rozet


# ------------------------------------------------------------------- chartspec


@dataclass(frozen=True)
class Kunye:
    sembol: str
    ad: str
    zaman_dilimi: str
    strateji: str
    strateji_adi: str
    yon: Yon | None = None
    durum: str = ""
    #: K4'ün verdikti. Grafiğin üstünde DURUR çünkü "bu kurulum oluştu" ile
    #: "bu stratejinin kenar ürettiği kanıtlandı" ayrı şeylerdir ve ikincisi
    #: gösterilmezse birincisi ikincisi sanılır. Boş = henüz ölçülmedi.
    #: SÜRÜM 1.0'da kalır: alan isteğe bağlı ve eklemeli, eski spec'ler geçerli.
    verdikt: str = ""
    #: Veri gerçek mi örnek mi — arayüz bunu kullanıcıya AYNEN gösterir.
    ornek_mi: bool = False


@dataclass(frozen=True)
class ChartSpec:
    kunye: Kunye
    paneller: Sequence[Panel]
    seriler: Sequence[Seri]
    katmanlar: Sequence[Katman] = field(default_factory=tuple)
    surum: str = SURUM

    # ------------------------------------------------------------ doğrulama
    def dogrula(self) -> ChartSpec:
        """Sözleşmeyi zorlar. Hatalıysa `ValueError`. Kendini döner ki
        `spec = ChartSpec(...).dogrula()` yazılabilsin."""
        if self.surum != SURUM:
            raise ValueError(
                f"Desteklenmeyen ChartSpec sürümü: {self.surum!r} (beklenen {SURUM!r})."
            )

        if not self.paneller:
            raise ValueError("En az bir panel gerekli.")

        panel_idler = [p.id for p in self.paneller]
        if len(set(panel_idler)) != len(panel_idler):
            raise ValueError(f"Panel id'leri benzersiz olmalı: {panel_idler}")

        toplam = sum(p.oran for p in self.paneller)
        if abs(toplam - 1.0) > 1e-6:
            raise ValueError(f"Panel oranlarının toplamı 1.0 olmalı, {toplam:.4f} bulundu.")

        if not self.seriler:
            raise ValueError("En az bir seri gerekli — ChartSpec boş levha tanımlayamaz.")

        seri_idler = [s.id for s in self.seriler]
        if len(set(seri_idler)) != len(seri_idler):
            raise ValueError(f"Seri id'leri benzersiz olmalı: {seri_idler}")

        for s in self.seriler:
            if s.panel not in panel_idler:
                raise ValueError(f"'{s.id}' serisi tanımsız panele bağlı: {s.panel!r}")
            if len(s.veri) < 2:
                raise ValueError(
                    f"'{s.id}' serisi {len(s.veri)} nokta taşıyor. Seriler TAM DİZİ taşır; "
                    f"iki uca indirgenmiş seri eski mimarinin hatasıydı (ADR-001 §4)."
                )
            zamanlar = [n.t for n in s.veri]
            if zamanlar != sorted(zamanlar):
                raise ValueError(f"'{s.id}' serisinin zamanları artan sırada değil.")
            if len(set(zamanlar)) != len(zamanlar):
                raise ValueError(f"'{s.id}' serisinde yinelenen zaman damgası var.")
            if isinstance(s, MumSerisi):
                for m in s.veri:
                    m.dogrula()

        ilk = min(n.t for s in self.seriler for n in s.veri)
        son = max(n.t for s in self.seriler for n in s.veri)

        for k in self.katmanlar:
            if k.panel not in panel_idler:
                raise ValueError(f"{k.tur} katmanı tanımsız panele bağlı: {k.panel!r}")
            for n in _katman_noktalari(k):
                if not (ilk <= n.t <= son):
                    raise ValueError(
                        f"{k.tur}/{k.rol.value} katmanı seri aralığının dışında: "
                        f"t={n.t}, seri [{ilk}, {son}]. Katmanlar kendi ekseninde yüzemez."
                    )
            if isinstance(k, Alan) and len(k.noktalar) < 3:
                raise ValueError(f"Alan katmanı en az üç nokta ister, {len(k.noktalar)} verildi.")
            if isinstance(k, Cizgi) and len(k.noktalar) < 2:
                raise ValueError(f"Çizgi katmanı en az iki nokta ister, {len(k.noktalar)} verildi.")
            if isinstance(k, Bant) and not (k.alt < k.ust):
                raise ValueError(f"Bant alt sınırı üst sınırdan küçük olmalı: {k.alt} / {k.ust}")

        for p in self.paneller:
            _panel_dogrula(p, self.seriler)

        return self

    # ----------------------------------------------------------- serileştirme
    def sozluk(self) -> dict[str, Any]:
        return _sadelestir(dataclasses.asdict(self))

    def json(self, *, girinti: int | None = 2) -> str:
        return json.dumps(self.sozluk(), ensure_ascii=False, indent=girinti) + "\n"


def _katman_noktalari(k: Katman) -> list[Nokta]:
    if isinstance(k, (Alan, Cizgi)):
        return list(k.noktalar)
    if isinstance(k, (Isaret, Etiket, Rozet)):
        return [k.nokta]
    return []  # Seviye ve Bant yataydır; zaman ekseninde noktası yok.


def _panel_dogrula(p: Panel, seriler: Sequence[Seri]) -> None:
    """Panel y aralığı yalnızca O PANELE verilen serilerden hesaplanır.

    Komposer açık bir aralık yazdıysa, o aralık serinin tamamını içermek
    zorundadır: aksi hâlde grafik sessizce veri kırpar."""
    kendi = [s for s in seriler if s.panel == p.id]
    if not kendi:
        raise ValueError(f"'{p.id}' paneline hiçbir seri bağlı değil.")
    if p.y is None:
        return

    if not (p.y.alt < p.y.ust):
        raise ValueError(f"'{p.id}' paneli için geçersiz y aralığı: {p.y.alt} / {p.y.ust}")

    alt = min(_seri_alt(s) for s in kendi)
    ust = max(_seri_ust(s) for s in kendi)
    if p.y.alt > alt or p.y.ust < ust:
        raise ValueError(
            f"'{p.id}' paneli için açık y aralığı [{p.y.alt}, {p.y.ust}] serinin "
            f"[{alt}, {ust}] aralığını kırpıyor. Aralık genişletilebilir, DARALTILAMAZ — "
            f"veri sessizce kaybolmaz."
        )


def _seri_alt(s: Seri) -> float:
    if isinstance(s, MumSerisi):
        return min(m.dusuk for m in s.veri)
    return min(b.hacim for b in s.veri)


def _seri_ust(s: Seri) -> float:
    if isinstance(s, MumSerisi):
        return max(m.yuksek for m in s.veri)
    return max(b.hacim for b in s.veri)


_ROL_TIPLERI = (SeviyeRol, AlanRol, CizgiRol, IsaretRol, EtiketRol, RozetRol, Yon)


def _sadelestir(x: Any) -> Any:
    """Rolleri değerine indirger; boş alanları JSON'a hiç yazmaz."""
    if isinstance(x, _ROL_TIPLERI):
        return x.value
    if isinstance(x, dict):
        return {k: _sadelestir(v) for k, v in x.items() if v is not None and v != ""}
    if isinstance(x, (list, tuple)):
        return [_sadelestir(v) for v in x]
    return x
