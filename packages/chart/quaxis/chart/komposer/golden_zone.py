"""Golden Zone (ICT OTE) komposeri — `OTESonucu` → `ChartSpec`.

Jenerik bir çizici DEĞİL: bu strateji için bestelenmiş tek bir komposer.
Kural `docs/strateji/kaynak/golden-zone-K0.md`'de; grafik o kuralın
**görünür hâlidir**:

  · yer değiştirme bacağı (çıpalardan geçen çizgi) — bölgenin NEDEN orada
    olduğunu gösteren tek şey
  · kırılan yapı seviyesi (BOS) — kurulumun ön koşulu
  · 0.62–0.79 OTE bandı, içinde 0.705 nişangâhı
  · stop (%100) ve hedef (%0) seviyeleri
  · girişin gerçekleştiği bara temas işareti
  · durum rozeti

**Merdivenin tamamı çizilmez.** Bandın kenarları zaten 0.62 ve 0.79'dur;
ayrıca çizgi olarak koymak dar bandın içinde üç çizgi = okunmaz yığın
demekti (TASARIM_DILI: "kısa levhada merdivenin tamamı okunmaz bir yığına
döner").

**Verdikt künyeye yazılır.** "Bu kurulum oluştu" ile "bu stratejinin kenar
ürettiği kanıtlandı" ayrı şeylerdir; ikincisi gösterilmezse birincisi
ikincisi sanılır. Golden Zone'un K4 verdikti `kanitlanmadi` ve grafik bunu
saklamaz.

Renk yok, piksel yok: yalnızca ROL ve DEĞER. Nasıl görüneceği çizicinin işi.
"""

from __future__ import annotations

from ..roller import AlanRol, CizgiRol, IsaretRol, RozetRol, SeviyeRol, Yon, fib_rol
from ..spec import (
    Bant,
    ChartSpec,
    Cizgi,
    HacimBari,
    HacimSerisi,
    Isaret,
    Katman,
    Kunye,
    Mum,
    MumSerisi,
    Nokta,
    Panel,
    Rozet,
    Seviye,
    YAraligi,
)
from ..tipler import Capa, OTESonucu

#: Gösterge durumu -> rozet rolü. Kapalı küme: tanımsız durum ValueError.
_DURUM_ROL = {
    "bolgede": RozetRol.DURUM_IZLENIYOR,
    "izleniyor": RozetRol.DURUM_IZLENIYOR,
    "onaylandi": RozetRol.DURUM_ONAYLANDI,
    "tamamlandi": RozetRol.DURUM_TAMAMLANDI,
    "gecersiz": RozetRol.DURUM_GECERSIZ,
}

#: Bariyer -> grafikteki metin ve işaret rolü. Sonuç yön bilgisidir;
#: "hedefe ulaştı" ile "stop oldu" aynı renge boyanamaz.
_CIKIS = {
    "hedef": ("hedef ✓", IsaretRol.CIKIS_KAZANC),
    "stop": ("stop ✕", IsaretRol.CIKIS_KAYIP),
    "zaman": ("süre doldu", IsaretRol.TEMAS),
}

#: Seviye oranı -> etiketteki insan okuması.
_SEVIYE_ADI = {
    0.0: "hedef",
    0.62: "giriş",
    0.705: "orta eşik",
    1.0: "stop",
}


def bestele(sonuc: OTESonucu, *, ornek_mi: bool = False) -> ChartSpec:
    """Tipli sonucu ChartSpec'e çevirir ve doğrulanmış hâlde döner."""
    barlar = list(sonuc.barlar)
    if len(barlar) < 2:
        raise ValueError("Golden Zone komposeri en az iki bar ister.")

    ilk_t, son_t = barlar[0].t, barlar[-1].t
    katmanlar: list[Katman] = []

    bolge_sig, bolge_derin = sonuc.bolge
    b_sig = sonuc.seviye(bolge_sig).fiyat
    b_derin = sonuc.seviye(bolge_derin).fiyat

    # --- 1. OTE bandı: aksan, DÜŞÜK opaklıkta geniş dolgu -----------------
    # Kurulumun kalbi bu. Band bacağın bittiği bardan başlar: öncesinde
    # bölge diye bir şey YOKTU ve sola uzatmak onu hep varmış gibi gösterir.
    katmanlar.append(
        Bant(
            rol=AlanRol.BOLGE_ALTIN,
            alt=min(b_sig, b_derin),
            ust=max(b_sig, b_derin),
            # Bant ETİKETSİZ: "OTE 0.62–0.79" hem HUD'da hem sağ olukta
            # zaten yazıyordu ve bandın içindeki giriş rozetiyle çakışıyordu
            # (K5 i3 bulgusu). Üçüncü kez yazmak bilgi eklemiyor, sadece
            # çakışma üretiyordu.
            baslangic=sonuc.capa0.onay_t,
            bitis=sonuc.cikis_t,
        )
    )

    # --- 2. yer değiştirme bacağı ----------------------------------------
    # Bölgenin NEDEN orada olduğunu gösteren tek çizgi. Bu olmadan merdiven
    # havada asılı kalır.
    katmanlar.append(
        Cizgi(rol=CizgiRol.TREND, noktalar=[_n(sonuc.capa100), _n(sonuc.capa0)])
    )

    # --- 3. kırılan yapı seviyesi (BOS) -----------------------------------
    # Kurulumun ön koşulu; sessiz bir çizgi olarak durur, bandı bastırmaz.
    katmanlar.append(
        Seviye(
            rol=SeviyeRol.SEVIYE,
            fiyat=sonuc.kirilan_seviye,
            etiket=f"BOS: {sonuc.kirilan_seviye:.2f}",
            baslangic=sonuc.bos_t,
        )
    )

    # --- 4. karara değer seviyeler ---------------------------------------
    # Bandın kenarları ZATEN 0.62 ve 0.79; onları ayrıca çizgi yapmak dar
    # bandın içine üç çizgi koymak olurdu. Çizilen: giriş, orta eşik,
    # stop, hedef.
    for s in sonuc.seviyeler:
        if round(s.oran, 3) == round(bolge_derin, 3):
            continue  # bandın derin kenarı — band zaten gösteriyor
        katmanlar.append(
            Seviye(
                rol=fib_rol(s.oran),
                fiyat=s.fiyat,
                etiket=_seviye_etiketi(s.oran, s.fiyat, s.ad),
                # Bölge ve seviyeleri bacak TAMAMLANINCA doğar; %100'ü
                # bacağın başından uzatmak, henüz tanımlı olmayan bir
                # seviyeyi varmış gibi göstermek olurdu.
                baslangic=sonuc.capa0.onay_t,
                bitis=sonuc.cikis_t,
            )
        )

    # --- 5. çıpalar ve süpürme -------------------------------------------
    katmanlar.append(
        Isaret(
            rol=IsaretRol.KOSE, nokta=_n(sonuc.capa100), metin="%100",
            yerlesim="alt" if sonuc.yon is Yon.AL else "ust",
        )
    )
    katmanlar.append(
        Isaret(
            rol=IsaretRol.KOSE, nokta=_n(sonuc.capa0), metin="%0",
            yerlesim="ust" if sonuc.yon is Yon.AL else "alt",
        )
    )
    # Süpürme çıpası %100 ile AYNI noktadaysa çizilmez: iki etiket üst üste
    # binip okunmaz bir yığın oluyordu (K5 i1'de görüldü).
    ayri_supurme = sonuc.supurme is not None and (
        sonuc.supurme.onay_t != sonuc.capa100.onay_t
        or abs(sonuc.supurme.fiyat - sonuc.capa100.fiyat) > 1e-9
    )
    if ayri_supurme and sonuc.supurme is not None:
        katmanlar.append(
            Isaret(
                rol=IsaretRol.KOSE, nokta=_n(sonuc.supurme), metin="süpürme",
                yerlesim="alt" if sonuc.yon is Yon.AL else "ust",
            )
        )

    # --- 6. giriş rozeti --------------------------------------------------
    # Ayrı bir TEMAS işareti KONMUYOR: rozet zaten önder çizgiyle o bara
    # bağlı ve ikisi aynı noktada üst üste biniyordu (K5 i2'de görüldü).
    katmanlar.append(
        Rozet(
            rol=_durum_rol(sonuc.durum),
            nokta=Nokta(t=sonuc.giris_t, fiyat=sonuc.giris_fiyat),
            metin=f"giriş {sonuc.giris_fiyat:.2f}",
            yon=sonuc.yon,
        )
    )

    # --- 7. çıkış: kurulum ne oldu ----------------------------------------
    # Sinyali gösterip sonucunu göstermemek, grafiği reklam yapar.
    if sonuc.cikis_t is not None and sonuc.cikis_fiyat is not None:
        metin, rol = _CIKIS.get(sonuc.cikis_turu, (sonuc.cikis_turu, IsaretRol.TEMAS))
        katmanlar.append(
            Isaret(
                rol=rol,
                nokta=Nokta(t=sonuc.cikis_t, fiyat=sonuc.cikis_fiyat),
                metin=f"{metin} {sonuc.cikis_fiyat:.2f}",
                yerlesim="alt" if rol is IsaretRol.CIKIS_KAYIP else "ust",
            )
        )

    # --- 8. paneller ------------------------------------------------------
    fiyat_alt = min(b.dusuk for b in barlar)
    fiyat_ust = max(b.yuksek for b in barlar)
    seviye_alt = min(s.fiyat for s in sonuc.seviyeler)
    seviye_ust = max(s.fiyat for s in sonuc.seviyeler)
    pay = (fiyat_ust - fiyat_alt) * 0.04

    paneller = [
        Panel(
            id="fiyat",
            tur="fiyat",
            oran=0.76,
            y=YAraligi(
                alt=min(fiyat_alt, seviye_alt) - pay,
                ust=max(fiyat_ust, seviye_ust) + pay,
                gerekce=(
                    "Stop (%100) ve hedef (%0) seviyeleri mum aralığının kenarında "
                    "duruyor; ikisi birden görünmezse 'ne kadar riske ne kadar "
                    "ödül' sorusu grafikte cevaplanamaz."
                ),
            ),
        ),
        Panel(id="hacim", tur="hacim", oran=0.24),
    ]

    seriler = [
        MumSerisi(
            id="mum",
            panel="fiyat",
            veri=[
                Mum(t=b.t, acilis=b.acilis, yuksek=b.yuksek, dusuk=b.dusuk, kapanis=b.kapanis)
                for b in barlar
            ],
        ),
        HacimSerisi(
            id="hacim",
            panel="hacim",
            veri=[
                HacimBari(t=b.t, hacim=b.hacim, yon=Yon.AL if b.kapanis >= b.acilis else Yon.SAT)
                for b in barlar
            ],
        ),
    ]

    kunye = Kunye(
        sembol=sonuc.sembol,
        ad=sonuc.ad,
        zaman_dilimi=sonuc.zaman_dilimi,
        strateji="golden-zone",
        strateji_adi="Golden Zone",
        yon=sonuc.yon,
        durum=sonuc.durum,
        verdikt=sonuc.verdikt,
        ornek_mi=ornek_mi,
    )

    for k in katmanlar:
        b = getattr(k, "baslangic", None)
        if b is not None and not (ilk_t <= b <= son_t):
            raise ValueError(f"{k.tur}/{k.rol.value} katmanının başlangıcı seri dışında: {b}")

    return ChartSpec(kunye=kunye, paneller=paneller, seriler=seriler, katmanlar=katmanlar).dogrula()


# ------------------------------------------------------------------ yardımcı


def _n(c: Capa) -> Nokta:
    """Çıpayı noktaya çevirir — çıpa ONAYLANDIĞI barda durur, kendi barında
    değil. Non-repaint sözleşmesinin çizim tarafındaki karşılığı budur."""
    return Nokta(t=c.onay_t, fiyat=c.fiyat)


def _seviye_etiketi(oran: float, fiyat: float, ad: str) -> str:
    """`0.705 (orta eşik): 12.34` biçimi. Tam sayı oranlar tek ondalık
    (`0.0`, `1.0`), diğerleri üç — merdiven sütun gibi hizalansın."""
    bas = f"{oran:.1f}" if oran in (0.0, 1.0) else f"{oran:.3f}"
    etiket = ad or _SEVIYE_ADI.get(round(oran, 3), "")
    return f"{bas}{f' ({etiket})' if etiket else ''}: {fiyat:.2f}"


def _durum_rol(durum: str) -> RozetRol:
    anahtar = (
        durum.lower()
        .replace("ı", "i")
        .replace("ğ", "g")
        .replace("ş", "s")
        .replace("ç", "c")
        .replace("ö", "o")
        .replace("ü", "u")
    )
    try:
        return _DURUM_ROL[anahtar]
    except KeyError:
        gecerli = ", ".join(sorted(_DURUM_ROL))
        raise ValueError(
            f"Bilinmeyen kurulum durumu: {durum!r}. Geçerli durumlar: {gecerli}."
        ) from None
