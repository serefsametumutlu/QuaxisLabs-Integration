"""Strateji Pasaportu doğrulayıcı — kapıların gerçekten kapı olmasını sağlar.

    python tools/pasaport.py dogrula          # tüm pasaportları denetle
    python tools/pasaport.py dogrula swing-fib-abcd
    python tools/pasaport.py durum            # kim nerede, tek tabloda
    python tools/pasaport.py yeni swing-fib-abcd --ad "Salınım Fibo ABCD" --paket yapi

**Neden var.** Önceki projede süreç bir kontrol listesiydi ve listeye uyulmadı:
K5 (görsel kabul) hiç yapılmadı, K4 (istatistik) en sona bırakıldı ve 27
gösterge kodlandıktan sonra hiçbirinin kenar kanıtlamadığı anlaşıldı. Disiplin
yetmedi. Bu yüzden kapılar artık **denetleniyor**: bir kapıyı "geçti" yazmak
yetmez, kanıtı diskte bulunmak zorunda.

Doğrulayıcının tuttuğu kurallar:

1. **Sıra.** K(n) geçilemez, K(n-1) geçilmeden.
2. **Kanıt.** Her kapının zorunlu kanıt türü vardır; dosya yolu gösteriliyorsa
   dosya GERÇEKTEN var olmalı.
3. **Ezberden sayı yasak.** K0'daki her eşik satırının kaynağı dolu olmalı ve
   ya alıntı ya `K3:` ölçümü olmalı.
4. **Verdikt uydurulamaz.** K4 açılmadan `verdikt` yalnız `olculmedi`
   olabilir; açıldıysa `olculmedi` OLAMAZ.
5. **K5 kullanıcı onayı olmadan kapanmaz** ve en az üç iterasyon karesi ister.
6. **Tek seferde tek strateji.** Aynı anda birden fazla strateji yolda olamaz
   (README madde 4) — biri K6'ya varmadan diğeri K0'ı geçemez.
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re
import sys
from dataclasses import dataclass, field

import yaml

KOK = pathlib.Path(__file__).resolve().parents[1]
PASAPORT_KOK = KOK / "docs" / "strateji"
SABLON = PASAPORT_KOK / "_SABLON.md"

KAPILAR = ("K0", "K1", "K2", "K3", "K4", "K5", "K6")
KAPI_ADI = {
    "K0": "Kaynak",
    "K1": "Sözleşme",
    "K2": "Dedektör",
    "K3": "Kalibrasyon",
    "K4": "İstatistik",
    "K5": "Görsel",
    "K6": "Ürün",
}
VERDIKTLER = ("olculmedi", "kanitlanmadi", "izlenen-aday", "kenar-var")
PAKETLER = ("yapi", "formasyon", "trend", "arbitraj")


@dataclass
class Bulgu:
    slug: str
    kapi: str
    mesaj: str

    def __str__(self) -> str:
        yer = f"{self.slug}/{self.kapi}" if self.kapi else self.slug
        return f"  {yer}: {self.mesaj}"


@dataclass
class Pasaport:
    yol: pathlib.Path
    kunye: dict
    govde: str
    bulgular: list[Bulgu] = field(default_factory=list)

    @property
    def slug(self) -> str:
        return str(self.kunye.get("slug", self.yol.stem))

    @property
    def gecilen(self) -> list[str]:
        kapilar = self.kunye.get("kapilar") or {}
        return [k for k in KAPILAR if (kapilar.get(k) or {}).get("gecildi")]

    @property
    def son_kapi(self) -> str:
        g = self.gecilen
        return g[-1] if g else "—"

    @property
    def bitti(self) -> bool:
        return "K6" in self.gecilen


# ------------------------------------------------------------------ okuma


def oku(yol: pathlib.Path) -> Pasaport:
    ham = yol.read_text(encoding="utf-8")
    if not ham.startswith("---"):
        raise ValueError(f"{yol.name}: künye bloğu (--- ... ---) yok.")
    _, kunye_ham, govde = ham.split("---", 2)
    kunye = yaml.safe_load(kunye_ham) or {}
    return Pasaport(yol=yol, kunye=kunye, govde=govde)


def pasaportlar() -> list[Pasaport]:
    return [
        oku(p)
        for p in sorted(PASAPORT_KOK.glob("*.md"))
        if p.name != "_SABLON.md" and not p.name.startswith("_")
    ]


# -------------------------------------------------------------- doğrulama


def _kanit_var(p: Pasaport, kapi: str) -> list[str]:
    """Kanıt listesindeki her yol diskte var mı? Eksikleri döner."""
    kanitlar = ((p.kunye.get("kapilar") or {}).get(kapi) or {}).get("kanit") or []
    eksik = []
    for k in kanitlar:
        if not (KOK / str(k)).exists():
            eksik.append(str(k))
    return eksik


def _esik_tablosu(govde: str) -> list[tuple[str, str, str]]:
    """K0'daki "Eşikler" tablosunun satırlarını çıkarır."""
    bolum = re.search(r"### Eşikler\s*(.*?)(?=\n###|\n## )", govde, re.S)
    if not bolum:
        return []
    satirlar = []
    for satir in bolum.group(1).splitlines():
        s = satir.strip()
        if not s.startswith("|") or set(s) <= set("|-: "):
            continue
        hucre = [h.strip() for h in s.strip("|").split("|")]
        if len(hucre) < 3 or hucre[0].lower() in ("eşik", "esik"):
            continue
        satirlar.append((hucre[0], hucre[1], hucre[2]))
    return satirlar


def _doldurulmus(metin: str) -> bool:
    """Şablondan kalma yer tutucu mu (`*(…)*` ya da boş)?"""
    s = metin.strip()
    return bool(s) and not (s.startswith("*(") and s.endswith(")*"))


def dogrula(p: Pasaport) -> list[Bulgu]:
    b: list[Bulgu] = []
    kapilar = p.kunye.get("kapilar") or {}

    # --- künye ---
    if p.kunye.get("paket") not in PAKETLER:
        b.append(Bulgu(p.slug, "", f"paket geçersiz: {p.kunye.get('paket')!r}; {PAKETLER}"))
    if p.yol.stem != p.slug:
        b.append(Bulgu(p.slug, "", f"slug dosya adıyla uyuşmuyor: {p.yol.name}"))

    verdikt = p.kunye.get("verdikt")
    if verdikt not in VERDIKTLER:
        b.append(Bulgu(p.slug, "", f"verdikt geçersiz: {verdikt!r}; {VERDIKTLER}"))

    eksik_kapi = [k for k in KAPILAR if k not in kapilar]
    if eksik_kapi:
        b.append(Bulgu(p.slug, "", f"künyede eksik kapı: {eksik_kapi}"))
        return b

    gecilen = p.gecilen

    # --- 1. sıra ---
    for i, k in enumerate(KAPILAR):
        if k in gecilen and i > 0 and KAPILAR[i - 1] not in gecilen:
            b.append(
                Bulgu(
                    p.slug, k,
                    f"geçilmiş ama {KAPILAR[i - 1]} ({KAPI_ADI[KAPILAR[i - 1]]}) açık "
                    "— kapı atlanamaz",
                )
            )

    # --- 2. kanıt dosyaları ---
    for k in gecilen:
        for eksik in _kanit_var(p, k):
            b.append(Bulgu(p.slug, k, f"kanıt dosyası yok: {eksik}"))
        if not ((kapilar.get(k) or {}).get("kanit") or []):
            b.append(Bulgu(p.slug, k, "geçilmiş ama hiç kanıt gösterilmemiş"))

    # --- 3. K0: ezberden sayı yasak ---
    if "K0" in gecilen:
        esikler = _esik_tablosu(p.govde)
        if not esikler:
            b.append(Bulgu(p.slug, "K0", "Eşikler tablosu boş — hangi sayı nereden geldi?"))
        for ad, _deger, kaynak in esikler:
            if not _doldurulmus(kaynak):
                b.append(Bulgu(p.slug, "K0", f"'{ad}' eşiğinin kaynağı boş — ezberden sayı yasak"))
            elif re.search(r"s\.\s*\d+", kaynak):
                pass  # sayfa alıntısı
            elif "K3:" in kaynak:
                # "K3:" bir SÖZ değil, bir DOSYADIR. "K3'ten türetilecek"
                # yazıp kapıyı geçmek, ezberden sayı yazmanın kibar hâlidir —
                # K0'ın kapatmak için var olduğu şeyin ta kendisi.
                yollar = re.findall(r"K3:\s*([^\s`,)]+\.md)", kaynak)
                if not yollar:
                    b.append(
                        Bulgu(
                            p.slug, "K0",
                            f"'{ad}' kaynağı 'K3:' diyor ama ölçüm dosyası göstermiyor: "
                            f"{kaynak!r} — söz kanıt değildir",
                        )
                    )
                for y in yollar:
                    if not (KOK / y).exists():
                        b.append(
                            Bulgu(p.slug, "K0", f"'{ad}' eşiğinin K3 ölçüm dosyası diskte yok: {y}")
                        )
            else:
                b.append(
                    Bulgu(
                        p.slug, "K0",
                        f"'{ad}' kaynağı ne sayfa alıntısı ne K3 ölçümü: {kaynak!r}",
                    )
                )

    # --- 4. verdikt ile K4 tutarlılığı ---
    if "K4" in gecilen and verdikt == "olculmedi":
        b.append(Bulgu(p.slug, "K4", "kapı geçilmiş ama verdikt hâlâ 'olculmedi'"))
    if "K4" not in gecilen and verdikt != "olculmedi":
        b.append(
            Bulgu(
                p.slug, "K4",
                f"kapı açılmadan verdikt yazılmış: {verdikt!r} — ölçülmeden etiket konmaz",
            )
        )

    # --- 5. K5: kullanıcı onayı + en az üç iterasyon ---
    if "K5" in gecilen:
        if not (kapilar.get("K5") or {}).get("onay"):
            b.append(Bulgu(p.slug, "K5", "kullanıcı onayı yok — görsel kapısı onaysız kapanmaz"))
        kareler = list((KOK / "docs" / "design" / "ui").glob(f"{p.slug}-*.png"))
        if len(kareler) < 3:
            b.append(
                Bulgu(p.slug, "K5", f"en az 3 iterasyon karesi gerekli, {len(kareler)} bulundu")
            )

    return b


def tek_strateji_kurali(hepsi: list[Pasaport]) -> list[Bulgu]:
    """README madde 4: bir strateji bitmeden sıradakine geçilmez."""
    yolda = [p for p in hepsi if p.gecilen and not p.bitti]
    if len(yolda) > 1:
        adlar = ", ".join(f"{p.slug} ({p.son_kapi})" for p in yolda)
        return [
            Bulgu(
                "(depo)", "",
                f"aynı anda {len(yolda)} strateji yolda: {adlar}. "
                "Biri K6'ya varmadan diğeri başlayamaz.",
            )
        ]
    return []


# ------------------------------------------------------------------ komutlar


def komut_dogrula(slug: str | None) -> int:
    hepsi = pasaportlar()
    if not hepsi:
        print("Henüz pasaport yok. Şablon: docs/strateji/_SABLON.md")
        print("Yeni pasaport: python tools/pasaport.py yeni <slug> --ad <Ad> --paket yapi")
        return 0

    secili = [p for p in hepsi if slug is None or p.slug == slug]
    if slug and not secili:
        print(f"HATA: '{slug}' adlı pasaport yok.", file=sys.stderr)
        return 2

    bulgular: list[Bulgu] = []
    for p in secili:
        bulgular += dogrula(p)
    if slug is None:
        bulgular += tek_strateji_kurali(hepsi)

    for p in secili:
        print(f"{p.slug:<24} {p.son_kapi:<4} {p.kunye.get('verdikt', '?')}")

    if bulgular:
        print(f"\n{len(bulgular)} bulgu:")
        for x in bulgular:
            print(x)
        return 1
    print("\nTüm kapılar tutarlı.")
    return 0


def komut_durum() -> int:
    hepsi = pasaportlar()
    if not hepsi:
        print("Henüz pasaport yok.")
        return 0
    basliklar = ["strateji", *KAPILAR, "verdikt"]
    baslik_satiri = " | ".join(
        f"{b:<12}" if b == "strateji" else f"{b:<4}" for b in basliklar[:-1]
    )
    print(baslik_satiri + " | verdikt")
    for p in hepsi:
        gecilen = set(p.gecilen)
        hucreler = ["✓ " if k in gecilen else "· " for k in KAPILAR]
        print(
            f"{p.slug:<12} | " + " | ".join(f"{h:<4}" for h in hucreler)
            + f" | {p.kunye.get('verdikt', '?')}"
        )
    return 0


def komut_yeni(slug: str, ad: str, paket: str) -> int:
    hedef = PASAPORT_KOK / f"{slug}.md"
    if hedef.exists():
        print(f"HATA: {hedef.name} zaten var.", file=sys.stderr)
        return 2
    yolda = [p for p in pasaportlar() if p.gecilen and not p.bitti]
    if yolda:
        print(
            f"HATA: '{yolda[0].slug}' hâlâ yolda ({yolda[0].son_kapi}). "
            f"Bir strateji bitmeden sıradakine geçilmez (README madde 4).",
            file=sys.stderr,
        )
        return 2

    metin = SABLON.read_text(encoding="utf-8")
    metin = metin.replace("slug: ornek-strateji", f"slug: {slug}")
    metin = metin.replace("ad: Örnek Strateji", f"ad: {ad}")
    metin = metin.replace("paket: yapi", f"paket: {paket}")
    metin = metin.replace("# Örnek Strateji — Strateji Pasaportu", f"# {ad} — Strateji Pasaportu")
    hedef.write_text(metin, encoding="utf-8")
    print(f"{hedef.relative_to(KOK)} oluşturuldu ({dt.date.today().isoformat()}).")
    print("K0 ile başla: kural kitaptan, sayfa numarasıyla.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Strateji Pasaportu doğrulayıcı")
    alt = ap.add_subparsers(dest="komut", required=True)

    d = alt.add_parser("dogrula", help="kapı tutarlılığını denetle")
    d.add_argument("slug", nargs="?", default=None)

    alt.add_parser("durum", help="kim hangi kapıda")

    y = alt.add_parser("yeni", help="şablondan yeni pasaport aç")
    y.add_argument("slug")
    y.add_argument("--ad", required=True)
    y.add_argument("--paket", required=True, choices=PAKETLER)

    a = ap.parse_args()
    if a.komut == "dogrula":
        return komut_dogrula(a.slug)
    if a.komut == "durum":
        return komut_durum()
    return komut_yeni(a.slug, a.ad, a.paket)


if __name__ == "__main__":
    raise SystemExit(main())
