"""Harmonik formasyon komposeri — `HarmonikSonucu` → `ChartSpec`.

Jenerik bir çizici DEĞİL: Pesavento ekolü için bestelenmiş tek bir komposer.
Kural `docs/strateji/kaynak/harmonik-pesavento-K0.md`'de; grafik o kuralın
**görünür hâlidir**:

  · zikzak bacaklar ve dolgulu formasyon gövdeleri — formasyonun ta kendisi
  · her bacağın üstünde **ölçülen oran** (`.618`, `1.272` …) — formasyonun
    neden formasyon olduğunu gösteren tek şey
  · son bacak (C→D) **kesik çizgi**: o bacak gerçekleşmiş değil, hesaplanmış
  · D · stop · hedef seviyeleri, hepsi fibo rolünde
  · D ile stop arasındaki **dönüş bölgesi** (PRZ) bandı
  · giriş teması, çıkış işareti, durum rozeti

## Son bacak neden kesikli

Harmonik grafiklerin klasik yanıltmacası budur: D'yi diğer köşelerle aynı
düz çizgiyle bağlamak, onu da gerçekleşmiş bir salınım ucu gibi gösterir.
D bir pivot DEĞİL, C onaylandığı anda hesaplanan bir **fiyat hedefidir**.
Kesik çizgi bu farkı görünür kılar — `CizgiRol.PROJEKSIYON` zaten tam bunun
için var.

## Verdikt künyeye yazılır

"Bu formasyon oluştu" ile "bu formasyonun kenar ürettiği kanıtlandı" ayrı
şeylerdir; ikincisi gösterilmezse birincisi ikincisi sanılır. Harmoniklerin
K4 verdikti `kanıtlanmadı` ve grafik bunu saklamaz.

Renk yok, piksel yok: yalnızca ROL ve DEĞER. Nasıl görüneceği çizicinin işi.
"""

from __future__ import annotations

from ..roller import AlanRol, CizgiRol, EtiketRol, IsaretRol, RozetRol, Yon, fib_rol
from ..spec import (
    Alan,
    Bant,
    ChartSpec,
    Cizgi,
    Etiket,
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
from ..tipler import Capa, HarmonikSonucu

#: Formasyon künyesi -> kullanıcıya görünen ad. Kapalı küme: tanımsız
#: formasyon `ValueError`. Sessizce "Harmonik" yazmak, hangi formasyonun
#: çizildiğini gizlerdi — dördü ayrı ölçüldüğü için bu bilgi kritik.
FORMASYON_ADI = {
    "harmonik_abcd": "AB=CD",
    "harmonik_gartley": "Gartley 222",
    "harmonik_kelebek": "Butterfly",
    "harmonik_uc_surus": "Three Drives",
}

#: Bariyer -> rozet rolü ve işaret rolü. Sonuç YÖN bilgisidir; "hedefe
#: ulaştı" ile "stop oldu" aynı renge boyanamaz.
_CIKIS_ROL = {
    "hedef": (RozetRol.DURUM_TAMAMLANDI, IsaretRol.CIKIS_KAZANC, "HEDEF"),
    "stop": (RozetRol.DURUM_GECERSIZ, IsaretRol.CIKIS_KAYIP, "STOP"),
    "zaman": (RozetRol.DURUM_IZLENIYOR, IsaretRol.TEMAS, "SÜRE DOLDU"),
}

#: Oran anahtarı -> etiketin oturacağı BACAK.
#:
#: **K5 i1'de yanlıştı ve düzeltildi.** `ab` oranı (A−B)/(A−X) hesabıdır
#: ama TARİF ETTİĞİ şey **A→B bacağıdır**; etiketi X→A bacağına koymak,
#: okuyucuya yanlış bacağın oranını göstermek olurdu. Oran nerede ölçülüyor
#: değil, neyi anlatıyor — etiket onun üstüne oturur.
_ORAN_BACAK = {
    "ab": ("A", "B"),
    "bc": ("B", "C"),
    "cd": ("C", "D"),
    "d": ("C", "D"),
    "a": ("S1", "A"),
    "c": ("S2", "C"),
    "s2_uzanti": ("A", "S2"),
    "s3_uzanti": ("C", "D"),
}

#: Oran etiketi için gereken ASGARİ bacak uzunluğu (bar).
#:
#: K5 i1 bulgusu: B ile C aynı bara düştüğünde `bc` etiketi tam B köşe
#: rozetinin üstüne oturuyordu ve ikisi de okunmaz oluyordu. Kısa bacağın
#: ortası diye bir yer yok. Bacak bu kadar kısaysa oran payload'da kalır,
#: grafikte yazılmaz — okunmayan bir etiket bilgi değil, gürültüdür.
ASGARI_BACAK_BAR = 4


def bestele(sonuc: HarmonikSonucu, *, ornek_mi: bool = False) -> ChartSpec:
    """Tipli sonucu ChartSpec'e çevirir ve doğrulanmış hâlde döner."""
    barlar = list(sonuc.barlar)
    if len(barlar) < 2:
        raise ValueError("Harmonik komposeri en az iki bar ister.")
    noktalar = list(sonuc.noktalar)
    if len(noktalar) < 3:
        raise ValueError(
            f"Harmonik formasyon en az üç onaylı pivot ister, "
            f"{len(noktalar)} geldi — eksik sonuçtan grafik uydurulmaz."
        )
    if sonuc.formasyon not in FORMASYON_ADI:
        gecerli = ", ".join(sorted(FORMASYON_ADI))
        raise ValueError(
            f"Bilinmeyen formasyon: {sonuc.formasyon!r}. Geçerli: {gecerli}."
        )

    ilk_t, son_t = barlar[0].t, barlar[-1].t
    uzun = sonuc.yon is Yon.AL
    katmanlar: list[Katman] = []
    d = sonuc.d
    giris = sonuc.seviye("giriş")
    stop = sonuc.seviye("stop")
    hedef = sonuc.seviye("hedef")

    # --- 1. dönüş bölgesi: D ile stop arası ------------------------------
    # Aksan değil, DÜŞÜK opaklıkta geniş dolgu (TASARIM_DILI §5). Bandın
    # anlamı somut: riskin tamamı bu şeridin içinde.
    katmanlar.append(
        Bant(
            rol=AlanRol.BOLGE_TALEP if uzun else AlanRol.BOLGE_ARZ,
            alt=min(giris.fiyat, stop.fiyat),
            ust=max(giris.fiyat, stop.fiyat),
            etiket="DÖNÜŞ BÖLGESİ",
            # Bant SON PİVOTTAN başlar: dönüş bölgesi C onaylandığı anda
            # bilinir hâle gelir, girişte değil. i2'de D'den başlatılmıştı
            # ama bant o zaman yalnız birkaç bar sürüyor ve etiketi bandın
            # dışına taşıyordu — bilgi hem eksik hem okunmaz oluyordu.
            baslangic=noktalar[-1].onay_t,
            # Kurulum sonuçlandıysa bant orada BİTER: artık geçerli olmayan
            # bir bölgeyi sağa uzatmak onu hâlâ varmış gibi gösterirdi.
            bitis=sonuc.cikis_t,
        )
    )

    # --- 2. seviyeler ----------------------------------------------------
    # Üçü de formasyonun KENDİ geometrisinden geliyor ve üçü de gerçek bir
    # fibo oranı; rolü `fib_rol` türetir, komposer renk seçmez.
    #
    # `baslangic` = son pivotun onay barı. Boş bırakılsaydı walk-forward
    # karşılaştırması seviyeleri "hep vardı" sayardı.
    for s in (hedef, giris, stop):
        katmanlar.append(
            Seviye(
                rol=fib_rol(s.oran),
                fiyat=s.fiyat,
                etiket=f"{s.oran:.3f} ({s.ad}): {s.fiyat:.2f}",
                baslangic=noktalar[-1].onay_t,
                bitis=sonuc.cikis_t,
            )
        )

    # --- 3. formasyon gövdeleri ------------------------------------------
    # Ardışık üçlüler ORTA noktayı paylaşır: (0,1,2), (2,3,4)… Böylece
    # gövdeler formasyonun zikzagını takip eder, üst üste binmez.
    tum = [*noktalar, d]
    for i in range(0, len(tum) - 2, 2):
        katmanlar.append(
            Alan(rol=AlanRol.FORMASYON, noktalar=[_n(p) for p in tum[i : i + 3]])
        )

    # --- 4. bacaklar ------------------------------------------------------
    # Gerçekleşmiş bacaklar düz, SON bacak (→D) kesik: D gerçekleşmiş bir
    # salınım ucu değil, hesaplanmış bir hedef.
    katmanlar.append(
        Cizgi(rol=CizgiRol.TREND, noktalar=[_n(p) for p in noktalar])
    )
    katmanlar.append(
        Cizgi(rol=CizgiRol.PROJEKSIYON, noktalar=[_n(noktalar[-1]), _n(d)])
    )

    # --- 5. köşeler ve oran etiketleri -----------------------------------
    orta = (min(b.dusuk for b in barlar) + max(b.yuksek for b in barlar)) / 2
    for p in tum:
        # D'nin etiketi RİSKİN OLDUĞU tarafa konmaz. D, dönüş bölgesinin
        # kenarında durur (boğada üst kenarında); "levhanın ortasının
        # altındaysa alta yaz" kuralı onu doğrudan bandın içine sokuyor ve
        # "DÖNÜŞ BÖLGESİ" yazısının ortasında kalıyordu (K5 i4, 768
        # bulgusu). Diğer köşeler için ortaya göre kural geçerli — onların
        # altında/üstünde bir bant yok.
        yerlesim = (
            ("ust" if uzun else "alt")
            if p is d
            else ("ust" if p.fiyat >= orta else "alt")
        )
        katmanlar.append(
            Isaret(rol=IsaretRol.KOSE, nokta=_n(p), metin=p.etiket, yerlesim=yerlesim)
        )
    katmanlar += _oran_etiketleri(sonuc, noktalar, d, orta, barlar)

    # --- 6. sonuç ---------------------------------------------------------
    #
    # **K5 i1'de burada İKİ ayrı çakışma vardı ve ikisi de fazlalıktan
    # doğuyordu:**
    #
    # 1. D köşesine hem "D" rozeti hem "GİRİŞ 9.48" teması konuyordu; DOM
    #    ölçümü ikisini 5 piksel arayla gösterdi. Giriş fiyatı zaten sağ
    #    olukta yazılı (`0.786 (giriş): 9.48`), yani temas işareti hiçbir
    #    YENİ bilgi taşımıyordu. Kaldırıldı.
    # 2. Durum rozeti D'nin üstüne konuyor ve formasyon adını tekrar
    #    ediyordu — ad zaten künyede ve HUD'da var. Rozet ÇIKIŞ barına
    #    taşındı: orada taşıdığı bilgi (hangi bariyer vuruldu) başka
    #    hiçbir yerde yok.
    #
    # **K5 i3 (dar levha):** sonuç önce ROZET olarak çiziliyordu. Rozet
    # çapasının SOLUNA ve ALTINA oturur; çıkış barı sağda olduğu için kutu
    # formasyonun üstüne düşüyor ve 768 piksellik levhada B köşesini
    # tamamen kapatıyordu. İşaretin kendi metni (zeminli, kompakt, önder
    # çizgisiz) aynı bilgiyi çakışmadan taşıyor.
    if sonuc.cikis_t is not None and sonuc.cikis_fiyat is not None:
        _, isaret_rol, metin = _CIKIS_ROL[_cikis_anahtari(sonuc.cikis_turu)]
        katmanlar.append(
            Isaret(
                rol=isaret_rol,
                nokta=Nokta(t=sonuc.cikis_t, fiyat=sonuc.cikis_fiyat),
                metin=f"{metin} {sonuc.cikis_fiyat:.2f}",
                yerlesim="ust" if sonuc.cikis_fiyat >= orta else "alt",
            )
        )
    else:
        katmanlar.append(
            Rozet(
                rol=RozetRol.DURUM_IZLENIYOR,
                nokta=Nokta(t=d.t, fiyat=d.fiyat),
                metin=f"D: {d.fiyat:.2f}",
                yon=sonuc.yon,
            )
        )

    # --- 8. paneller ------------------------------------------------------
    fiyat_alt = min(b.dusuk for b in barlar)
    fiyat_ust = max(b.yuksek for b in barlar)
    seviye_alt = min(s.fiyat for s in (hedef, giris, stop))
    seviye_ust = max(s.fiyat for s in (hedef, giris, stop))
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
                    "Kelebek'te stop (1.618 uzantısı) mum aralığının DIŞINDA "
                    "kalır — D zaten X'i aşan bir noktadır. Stop görünmezse "
                    "'ne kadar risk alıyorum' sorusu grafikte cevaplanamaz."
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
                Mum(t=b.t, acilis=b.acilis, yuksek=b.yuksek, dusuk=b.dusuk,
                    kapanis=b.kapanis)
                for b in barlar
            ],
        ),
        HacimSerisi(
            id="hacim",
            panel="hacim",
            veri=[
                HacimBari(
                    t=b.t, hacim=b.hacim,
                    yon=Yon.AL if b.kapanis >= b.acilis else Yon.SAT,
                )
                for b in barlar
            ],
        ),
    ]

    kunye = Kunye(
        sembol=sonuc.sembol,
        ad=sonuc.ad,
        zaman_dilimi=sonuc.zaman_dilimi,
        strateji=sonuc.formasyon.replace("_", "-"),
        strateji_adi=f"Harmonik · {FORMASYON_ADI[sonuc.formasyon]}",
        yon=sonuc.yon,
        durum=sonuc.durum,
        verdikt=sonuc.verdikt,
        ornek_mi=ornek_mi,
    )

    for k in katmanlar:
        b = getattr(k, "baslangic", None)
        if b is not None and not (ilk_t <= b <= son_t):
            raise ValueError(
                f"{k.tur}/{k.rol.value} katmanının başlangıcı seri dışında: {b}"
            )

    return ChartSpec(
        kunye=kunye, paneller=paneller, seriler=seriler, katmanlar=katmanlar
    ).dogrula()


# ------------------------------------------------------------------ yardımcı


def _n(p: Capa) -> Nokta:
    """Çıpayı noktaya çevirir — pivot ONAYLANDIĞI barda durur, kendi
    barında değil. Non-repaint sözleşmesinin çizim tarafındaki karşılığı."""
    return Nokta(t=p.onay_t, fiyat=p.fiyat)


def _oran_etiketleri(
    sonuc: HarmonikSonucu, noktalar: list[Capa], d: Capa, orta: float, barlar: list
) -> list[Katman]:
    """Her bacağın ortasına ölçülen oranı yazar.

    Oranlar olmadan grafik "bir zikzak" gösterir; oranlarla birlikte
    **formasyonu** gösterir. Kullanıcının "bu neden Gartley" sorusunun
    cevabı burada.
    """
    yer = {p.etiket: p for p in [*noktalar, d]}
    zaman = [b.t for b in barlar]
    out: list[Katman] = []
    for anahtar, deger in sonuc.oranlar.items():
        bacak = _ORAN_BACAK.get(anahtar)
        if bacak is None:
            continue  # `abcd_ham`, `bc_ham` — tanı değerleri, grafik değil
        a, b = (yer.get(bacak[0]), yer.get(bacak[1]))
        if a is None or b is None:
            continue
        if _bar_araligi(zaman, a.onay_t, b.onay_t) < ASGARI_BACAK_BAR:
            continue  # kısa bacağın "ortası" yok — bkz. ASGARI_BACAK_BAR
        fiyat = (a.fiyat + b.fiyat) / 2
        out.append(
            Etiket(
                rol=EtiketRol.NOT,
                nokta=Nokta(t=_orta_bar(zaman, a.onay_t, b.onay_t), fiyat=fiyat),
                metin=f"{deger:.3f}",
                # Yükselen bacağın etiketi ÜSTE, alçalanınki ALTA: etiket
                # bacağın kendi çizgisinin üstüne oturmasın.
                yerlesim="ust" if b.fiyat >= a.fiyat else "alt",
            )
        )
    return out


def _orta_bar(zaman: list[int], a: int, b: int) -> int:
    """İki barın TAM ORTASINDAKİ barın zamanı.

    **K5 i2 bulgusu — sessiz kaybolma.** Önce `(a + b) // 2` yazılmıştı:
    iki epoch damgasının aritmetik ortalaması. O an çoğu zaman **hiçbir
    barın zamanı değildir** (hafta sonu, tatil, seans dışı). Çizici böyle
    bir zamanı ekrana çeviremeyince katmanı sessizce atıyordu — DOM'da
    etiket vardı, ekranda yoktu.

    Ortası bar İNDEKSİNDEN alınır: takvim değil, seri esastır.
    """
    try:
        i, j = zaman.index(a), zaman.index(b)
    except ValueError:
        return a
    return zaman[(i + j) // 2]


def _bar_araligi(zaman: list[int], a: int, b: int) -> int:
    """İki zaman damgası arasındaki BAR sayısı.

    Takvim farkı değil bar farkı: hafta sonu ve tatiller barı yoktur ama
    saniyeyi vardır; gün farkına bakmak kısa bacağı uzun sanmaya yol
    açardı.
    """
    try:
        return abs(zaman.index(b) - zaman.index(a))
    except ValueError:
        return ASGARI_BACAK_BAR  # bilinmiyorsa engelleme


def _cikis_anahtari(tur: str) -> str:
    if tur not in _CIKIS_ROL:
        gecerli = ", ".join(sorted(_CIKIS_ROL))
        raise ValueError(
            f"Bilinmeyen çıkış türü: {tur!r}. Geçerli türler: {gecerli}."
        )
    return tur
