"""Altın Bölge komposeri — `FibDuzeltmeSonucu` → `ChartSpec`.

Jenerik bir çizici DEĞİL: bu strateji için bestelenmiş tek bir komposer.
Referans görsel `references/HRhIeAdbcAAL2_B.png` neyi gösteriyorsa onu üretir:

  · oran-renkli fibo merdiveni, sağ kenarda etiketli
  · X→A→B ve B→C→D dolgulu gövdeler
  · C→D kesikli izdüşümü
  · köşe işaretleri (X A B C D) ve salınım etiketleri (HH/HL/LH/LL)
  · tamamlanma rozeti, önder çizgiyle D noktasına bağlı
  · 0.618–0.786 altın bölge bandı

Renk yok, piksel yok: yalnızca ROL ve DEĞER. Nasıl görüneceği çizicinin işi.
"""

from __future__ import annotations

from ..roller import AlanRol, CizgiRol, EtiketRol, IsaretRol, RozetRol, SeviyeRol, Yon, fib_rol
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
from ..tipler import FibDuzeltmeSonucu

#: Salınım yapısı -> etiket rolü.
_YAPI_ROL = {
    "HH": EtiketRol.SWING_HH,
    "HL": EtiketRol.SWING_HL,
    "LH": EtiketRol.SWING_LH,
    "LL": EtiketRol.SWING_LL,
}

#: Gösterge durumu -> rozet rolü. Kapalı küme: tanımsız durum ValueError.
_DURUM_ROL = {
    "tamamlandi": RozetRol.DURUM_TAMAMLANDI,
    "onaylandi": RozetRol.DURUM_ONAYLANDI,
    "izleniyor": RozetRol.DURUM_IZLENIYOR,
    "gecersiz": RozetRol.DURUM_GECERSIZ,
}


def bestele(sonuc: FibDuzeltmeSonucu, *, ornek_mi: bool = False) -> ChartSpec:
    """Tipli sonucu ChartSpec'e çevirir ve doğrulanmış hâlde döner."""
    barlar = list(sonuc.barlar)
    if len(barlar) < 2:
        raise ValueError("Altın Bölge komposeri en az iki bar ister.")

    ilk_t, son_t = barlar[0].t, barlar[-1].t
    katmanlar: list[Katman] = []

    # --- 1. altın bölge bandı: aksan, DÜŞÜK opaklıkta geniş dolgu ----------
    bolge_alt, bolge_ust = sonuc.bolge
    b_alt = _seviye_fiyati(sonuc, bolge_alt)
    b_ust = _seviye_fiyati(sonuc, bolge_ust)
    A = sonuc.pivot("A")
    katmanlar.append(
        Bant(
            rol=AlanRol.BOLGE_ALTIN,
            alt=min(b_alt, b_ust),
            ust=max(b_alt, b_ust),
            etiket="ALTIN BÖLGE",
            baslangic=A.onay_t,
        )
    )

    # --- 2. fibo merdiveni -------------------------------------------------
    for s in sonuc.seviyeler:
        katmanlar.append(
            Seviye(
                rol=fib_rol(s.oran),
                fiyat=s.fiyat,
                etiket=_seviye_etiketi(s.oran, s.fiyat, s.ad),
                baslangic=A.onay_t if s.oran <= 1.0 else None,
            )
        )

    # --- 3. formasyon gövdeleri: X→A→B ve B→C→D ---------------------------
    X, B = sonuc.pivot("X"), sonuc.pivot("B")
    katmanlar.append(Alan(rol=AlanRol.FORMASYON, noktalar=[_n(X), _n(A), _n(B)]))

    D = sonuc.tamamlanma
    C = _varsa(sonuc, "C")
    if C is not None and D is not None:
        katmanlar.append(Alan(rol=AlanRol.FORMASYON, noktalar=[_n(B), _n(C), _n(D)]))
        # C→D izdüşümü: yön taşır, o yüzden kesikli ve yön renginde
        katmanlar.append(Cizgi(rol=CizgiRol.PROJEKSIYON, noktalar=[_n(C), _n(D)]))

    # --- 4. köşe işaretleri ve salınım etiketleri --------------------------
    for p in sonuc.pivotlar:
        ustte = p.fiyat >= (b_alt + b_ust) / 2
        katmanlar.append(
            Isaret(
                rol=IsaretRol.KOSE,
                nokta=_n(p),
                metin=p.etiket,
                yerlesim="ust" if ustte else "alt",
            )
        )
        if p.yapi:
            katmanlar.append(
                Etiket(
                    rol=_YAPI_ROL[p.yapi],
                    nokta=_n(p),
                    metin=p.yapi,
                    yerlesim="ust" if ustte else "alt",
                )
            )

    # --- 5. tamamlanma rozeti ---------------------------------------------
    if D is not None:
        katmanlar.append(
            Rozet(
                rol=_durum_rol(sonuc.durum),
                nokta=_n(D),
                metin=f"D: {D.fiyat:.2f}  [{sonuc.durum.upper()}]",
                yon=sonuc.yon,
            )
        )

    # --- 6. paneller: y aralığı AÇIK, çünkü merdiven seriden taşıyor -------
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
                    "1.618 (azami risk) seviyesi mum aralığının dışında kalıyor; "
                    "merdivenin tamamı görünmezse 'nereye kadar düşebilir' sorusu "
                    "grafikte cevaplanamaz."
                ),
            ),
        ),
        Panel(id="hacim", tur="hacim", oran=0.24),
    ]

    seriler = [
        MumSerisi(
            id="mum",
            panel="fiyat",
            veri=[Mum(t=b.t, acilis=b.acilis, yuksek=b.yuksek, dusuk=b.dusuk, kapanis=b.kapanis) for b in barlar],
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
        strateji="altin-bolge",
        strateji_adi="Altın Bölge",
        yon=sonuc.yon,
        durum=sonuc.durum,
        ornek_mi=ornek_mi,
    )

    # `baslangic` seri aralığının dışına taşmasın (doğrulama zaten yakalar,
    # ama komposer kendi çıktısını temiz üretmeli).
    for k in katmanlar:
        b = getattr(k, "baslangic", None)
        if b is not None and not (ilk_t <= b <= son_t):
            raise ValueError(f"{k.tur}/{k.rol.value} katmanının başlangıcı seri dışında: {b}")

    return ChartSpec(kunye=kunye, paneller=paneller, seriler=seriler, katmanlar=katmanlar).dogrula()


# ------------------------------------------------------------------ yardımcı


def _n(p) -> Nokta:
    """Pivotu noktaya çevirir — sinyal ONAYLANDIĞI barda durur, kendi barında
    değil. Non-repaint sözleşmesinin çizim tarafındaki karşılığı budur."""
    return Nokta(t=p.onay_t, fiyat=p.fiyat)


def _varsa(sonuc: FibDuzeltmeSonucu, etiket: str):
    try:
        return sonuc.pivot(etiket)
    except ValueError:
        return None


def _seviye_fiyati(sonuc: FibDuzeltmeSonucu, oran: float) -> float:
    for s in sonuc.seviyeler:
        if round(s.oran, 3) == round(oran, 3):
            return s.fiyat
    raise ValueError(f"Bölge sınırı {oran} seviyeler arasında yok; gösterge onu üretmemiş.")


def _seviye_etiketi(oran: float, fiyat: float, ad: str) -> str:
    """Referans görseldeki biçim: `0.618: 185.00`, `1.272 (D hedefi): 159.49`.
    Tam sayı oranlar tek ondalık (`0.0`, `1.0`), diğerleri üç (`0.500`) —
    merdiven sütun gibi hizalansın."""
    bas = f"{oran:.1f}" if oran in (0.0, 1.0) else f"{oran:.3f}"
    return f"{bas}{f' ({ad})' if ad else ''}: {fiyat:.2f}"


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
            f"Bilinmeyen formasyon durumu: {durum!r}. Geçerli durumlar: {gecerli}."
        ) from None
