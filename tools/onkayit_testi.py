"""Ön kayıtlı test koşucusu — belgede yazan neyse onu ölçer, fazlasını değil.

    python tools/onkayit_testi.py --katalog "quaxis.teknik.indicators.katalog:KATALOG" \\
        --kayit docs/olcum/onkayit-macd-oynaklik.md \\
        --aile macd_ve_oynaklik,macd_uyum,oynaklik_dusuk \\
        --test macd_ve_oynaklik --grup 0 --pencere oos

Çıktı: ön kayıt belgesinin **Sonuç** bölümünü doldurur.

## Neden ayrı bir araç

`kosul_taramasi.py` ARAR: onlarca koşulu tarar, en iyisini bulur. Aramanın
doğası gereği çoklu test sorunu taşır ve düzeltmesi de ona göredir.

Bu araç aramaz. **Önceden yazılmış tek bir soruyu** önceden seçilmiş bir
pencerede ölçer. Aile küçüktür çünkü soru tektir; pencere sabittir çünkü
belgede öyle yazar. Sonuç ne çıkarsa belgeye o yazılır.

İkisini ayrı tutmak kasıtlı: aynı araca hem "ara" hem "doğrula" dedirtmek,
er geç aramanın sonucuna göre doğrulamanın kuralını esnetmekle biter.
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import sys

KOK = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "packages" / "teknik"))

for akis in (sys.stdout, sys.stderr):
    if hasattr(akis, "reconfigure"):
        akis.reconfigure(encoding="utf-8", errors="replace")

from katmanli_olcum import ASGARI_ISLEM, tara  # noqa: E402
from kosul_taramasi import (  # noqa: E402
    KOSULLAR,
    _grup,
    _islemler,
    _rejim_ekle,
    endeks_rejimi,
)
from quaxis.teknik.core.types import Market, Timeframe  # noqa: E402
from quaxis.teknik.olcum.bariyer import measure_r  # noqa: E402
from quaxis.teknik.olcum.ileri_getiri import bh_fdr  # noqa: E402

#: Karar kuralının 4. maddesi: bu maliyette hâlâ pozitif olmalı.
MALIYET_ESIGI = (0.0015, 0.0015)  # taraf başına %0.15 -> gidiş-dönüş %0.45


def main() -> int:
    ap = argparse.ArgumentParser(description="Ön kayıtlı test")
    ap.add_argument("--katalog", required=True)
    ap.add_argument("--kayit", required=True, help="ön kayıt belgesinin yolu")
    ap.add_argument("--aile", required=True, help="virgülle ayrılmış koşul adları")
    ap.add_argument("--test", required=True, help="ailedeki hangi koşul TEST ediliyor")
    ap.add_argument("--grup", type=int, required=True, help="0=A · 1=B")
    ap.add_argument("--pencere", default="oos", choices=["is", "oos"])
    ap.add_argument("--gosterge", default="golden_zone")
    ap.add_argument("--zaman-dilimi", default="1D")
    ap.add_argument("--market", default="bist")
    ap.add_argument("--tur", type=int, default=2000)
    ap.add_argument("--evren", default=None)
    a = ap.parse_args()

    aile = [x.strip() for x in a.aile.split(",") if x.strip()]
    bilinmeyen = set(aile) - set(KOSULLAR)
    if bilinmeyen:
        ap.error(f"bilinmeyen koşul: {sorted(bilinmeyen)}")
    if a.test not in aile:
        ap.error("--test ailenin içinde olmalı")

    kayit = pathlib.Path(a.kayit)
    if not kayit.exists():
        ap.error(f"ön kayıt belgesi yok: {kayit}. Test KOŞULMADAN ÖNCE yazılmalıydı.")

    market, tf = Market(a.market), Timeframe(a.zaman_dilimi)
    if a.evren:
        evren = [s.strip() for s in a.evren.split(",") if s.strip()]
    else:
        from quaxis.teknik.data.universe import load_universe

        evren = load_universe(market)

    ohlc, sinyaller, _ = tara(a.katalog, a.gosterge, evren, tf, market)
    _rejim_ekle(sinyaller, endeks_rejimi(market, tf))
    ohlc, sinyaller = _grup(ohlc, a.grup), _grup(sinyaller, a.grup)
    print(f"Grup {'AB'[a.grup]} · pencere {a.pencere.upper()} · {len(sinyaller)} sembol",
          flush=True)

    bariyer = 40
    for liste in _islemler(sinyaller).values():
        bariyer = int(liste[0][0].payload.get("zaman_bariyeri", bariyer))
        break

    def olc(kosul=None, kom=0.0005, kay=0.0005):
        return measure_r(
            ohlc, _islemler(sinyaller, kosul), max_bars=bariyer, pencere=a.pencere,
            komisyon=kom, kayma=kay, permutations=a.tur,
        )

    taban = olc()
    print(f"Koşulsuz taban: {taban.mean_r:+.3f}R ({taban.n_trades} işlem)", flush=True)

    sonuc = {}
    for ad in aile:
        r = olc(KOSULLAR[ad][1])
        sonuc[ad] = r
        print(f"  {ad:20} {r.n_trades:5} işlem · {r.mean_r:+.3f}R "
              f"(Δ {r.mean_r - taban.mean_r:+.3f}R) · p={r.p_value:.4f}", flush=True)

    fdr = bh_fdr({ad: r.p_value for ad, r in sonuc.items()}, q=0.05)
    test = sonuc[a.test]
    d_test = test.mean_r - taban.mean_r
    digerleri = {ad: sonuc[ad].mean_r - taban.mean_r for ad in aile if ad != a.test}

    maliyetli = olc(KOSULLAR[a.test][1], *MALIYET_ESIGI)
    print(f"  %0.45 maliyette: {maliyetli.mean_r:+.3f}R", flush=True)

    kural = {
        "1 · ΔR her iki bileşenden büyük": all(d_test > d for d in digerleri.values()),
        "2 · üçlü ailede BH-FDR geçti": bool(fdr.get(a.test)),
        f"3 · en az {ASGARI_ISLEM} işlem": test.n_trades >= ASGARI_ISLEM,
        "4 · %0.45 maliyette hâlâ pozitif": maliyetli.mean_r > 0,
    }
    gecti = all(kural.values())

    satir = "\n".join(
        f"| `{ad}` | {r.n_trades} | {r.mean_r:+.3f}R | {r.mean_r - taban.mean_r:+.3f}R | "
        f"{r.p_value:.4f} | {'geçti' if fdr.get(ad) else '—'} |"
        for ad, r in sonuc.items()
    )
    kural_satir = "\n".join(
        f"| {k} | {'✔' if v else '✘'} |" for k, v in kural.items()
    )

    metin = kayit.read_text(encoding="utf-8")
    bas = metin.index("## 7. Sonuç")
    metin = metin[:bas] + f"""## 7. Sonuç

**Koşuldu:** {dt.date.today().isoformat()} ·
**Pencere:** {'AB'[a.grup]} grubu + {a.pencere.upper()} · {len(sinyaller)} sembol ·
**Koşulsuz taban:** {taban.mean_r:+.3f}R ({taban.n_trades} işlem)

| Koşul | İşlem | Ort. R | ΔR | p | Aile BH-FDR |
|---|---|---|---|---|---|
{satir}

### Karar kuralının dört maddesi

| Madde | Sonuç |
|---|---|
{kural_satir}

### Verdikt

**{"KOMBİNASYON BİLEŞENLERİNDEN DAHA İYİ" if gecti else "KOMBİNASYON DAHA İYİ DEĞİL"}**

*(Yorum aşağıya elle yazılır — sayılar yukarıda, olduğu gibi.)*
"""
    kayit.write_text(metin, encoding="utf-8")
    print(f"\n{'GEÇTİ' if gecti else 'GEÇEMEDİ'} — {kayit.relative_to(KOK)} güncellendi.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
