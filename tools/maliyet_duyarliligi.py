"""Maliyet duyarlılığı — bulunan kenar hangi işlem maliyetinde ölüyor?

    python tools/maliyet_duyarliligi.py --katalog "quaxis.teknik.indicators.katalog:KATALOG" \\
        --kosul oynaklik_dusuk --slug golden-zone

Çıktı: `docs/olcum/<slug>-maliyet-duyarliligi-<tarih>.md`

## Neden ayrı bir araç

Koşul taraması tek bir maliyet varsayımıyla koşar (%0.05 komisyon + %0.05
kayma). Ama o varsayım bir **seçim**dir ve bulunan kenar ona duyarlıdır:
maliyetsiz ölçümde +0.069R olan etki, maliyet eklenince +0.038R'ye indi.

Tek bir maliyet düzeyinde "kenar var" demek, o düzeyin doğru olduğunu
varsaymaktır. Doğrusu şudur: **kenarın hangi maliyette sıfırlandığını
söylemek.** Aracı kurum komisyonu, sembol likiditesi ve emir büyüklüğü
kullanıcıdan kullanıcıya değişir; karar verecek olan o eşiği kendi
gerçeğiyle karşılaştırır.

BIST'te tipik aralık: aracı kurum komisyonu taraf başına %0.01–%0.15;
likit olmayan sembollerde spread + kayma bunun katı olabilir.
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

from katmanli_olcum import tara  # noqa: E402
from kosul_taramasi import KOSULLAR, _grup, _islemler  # noqa: E402
from quaxis.teknik.core.types import Market, Timeframe  # noqa: E402
from quaxis.teknik.olcum.bariyer import measure_r  # noqa: E402

OLCUM_KOK = KOK / "docs" / "olcum"

#: Denenen maliyet düzeyleri: (taraf başına komisyon, çıkışta kayma).
#: Gidiş-dönüş yaklaşık maliyet = 2×komisyon + kayma.
DUZEYLER: list[tuple[float, float]] = [
    (0.0000, 0.0000),
    (0.0002, 0.0002),
    (0.0005, 0.0005),
    (0.0010, 0.0010),
    (0.0015, 0.0015),
    (0.0025, 0.0025),
]


def main() -> int:
    ap = argparse.ArgumentParser(description="Maliyet duyarlılığı")
    ap.add_argument("--katalog", required=True)
    ap.add_argument("--gosterge", default="golden_zone")
    ap.add_argument("--slug", default="golden-zone")
    ap.add_argument("--kosul", default=None, help="KOSULLAR anahtarı; yoksa koşulsuz taban")
    ap.add_argument("--zaman-dilimi", default="1D")
    ap.add_argument("--market", default="bist")
    ap.add_argument("--tur", type=int, default=2000)
    ap.add_argument("--evren", default=None)
    ap.add_argument(
        "--grup", type=int, default=None,
        help="0=A (arama) · 1=B (doğrulama). Doğrulanmış bir bulgunun maliyet "
             "eşiği, bulgunun DOĞRULANDIĞI grupta ölçülmeli.",
    )
    a = ap.parse_args()

    market, tf = Market(a.market), Timeframe(a.zaman_dilimi)
    if a.evren:
        evren = [s.strip() for s in a.evren.split(",") if s.strip()]
    else:
        from quaxis.teknik.data.universe import load_universe

        evren = load_universe(market)

    ohlc, sinyaller, _ = tara(a.katalog, a.gosterge, evren, tf, market)
    if a.grup is not None:
        ohlc, sinyaller = _grup(ohlc, a.grup), _grup(sinyaller, a.grup)
        print(f"Grup {'AB'[a.grup]}: {len(sinyaller)} sembol", flush=True)
    kosul = KOSULLAR[a.kosul][1] if a.kosul else None
    hipotez = KOSULLAR[a.kosul][0] if a.kosul else "koşulsuz taban"
    islemler = _islemler(sinyaller, kosul)
    taban_islemler = _islemler(sinyaller, None)

    bariyer = 40
    for liste in islemler.values():
        bariyer = int(liste[0][0].payload.get("zaman_bariyeri", bariyer))
        break

    satirlar = []
    for kom, kay in DUZEYLER:
        gidis_donus = 2 * kom + kay
        r = measure_r(
            ohlc, islemler, max_bars=bariyer, pencere="oos",
            komisyon=kom, kayma=kay, permutations=a.tur,
        )
        t = measure_r(
            ohlc, taban_islemler, max_bars=bariyer, pencere="oos",
            komisyon=kom, kayma=kay, permutations=a.tur,
        )
        satirlar.append(
            f"| %{gidis_donus * 100:.2f} | {r.mean_r:+.3f}R | {r.baseline_mean_r:+.3f}R | "
            f"{r.mean_r - t.mean_r:+.3f}R | {r.p_value:.4f} | "
            f"{'kenar-var' if r.p_value <= 0.05 and r.mean_r > 0 else 'kanıtlanmadı'} |"
        )
        print(f"  gidiş-dönüş %{gidis_donus * 100:.2f} -> {r.mean_r:+.3f}R "
              f"(taban {t.mean_r:+.3f}R) p={r.p_value:.4f}", flush=True)

    OLCUM_KOK.mkdir(parents=True, exist_ok=True)
    hedef = OLCUM_KOK / f"{a.slug}-maliyet-duyarliligi-{dt.date.today().isoformat()}.md"
    hedef.write_text(f"""# {a.slug} — Maliyet Duyarlılığı

**Tarih:** {dt.date.today().isoformat()} · **Koşul:** `{a.kosul or "—"}` ({hipotez})
**Pencere:** OOS · **Grup:** {"AB"[a.grup] if a.grup is not None else "hepsi"} ·
**İşlem:** {sum(len(v) for v in islemler.values())}

Tek bir maliyet düzeyinde "kenar var" demek, o düzeyin doğru olduğunu
varsaymaktır. Bu tablo bunun yerine **kenarın hangi maliyette sıfırlandığını**
söyler; karar verecek olan o eşiği kendi aracı kurum komisyonuyla
karşılaştırır.

| Gidiş-dönüş maliyet | Ort. R | Adil baz | Koşulsuz tabana ΔR | p | Verdikt |
|---|---|---|---|---|---|
{chr(10).join(satirlar)}

> Maliyet **baza da** uygulanır — yalnız gerçek işlemlere uygulamak ölçümü
> stratejinin aleyhine saptırırdı.

## Nasıl okunur

`Ort. R` sıfırın altına indiği düzeyde strateji **para kaybettirir**.
Sıfırın üstünde ama `adil baz`ın altında kaldığı düzeyde kaybettirmez ama
**piyasanın kendi verdiğinin altında** kalır. İkisinin arasındaki aralık,
stratejinin yaşayabileceği maliyet penceresidir.

BIST'te aracı kurum komisyonu taraf başına %0.01–%0.15 arası değişir;
likit olmayan sembollerde spread ve kayma bunun katı olabilir. Tablodaki
eşik **kendi maliyetinle** karşılaştırılmalı.

## Ölçümün sınırları

| | |
|---|---|
| Kayma modeli | Sabit oran. Gerçekte emir büyüklüğüne ve likiditeye
bağlıdır; küçük sembollerde bu tablo iyimserdir. |
| Giriş | Limit emir varsayıldı (bölge seviyesine). Dolmama riski modellenmedi. |
| Vergi/stopaj | yok |
""", encoding="utf-8")
    print(f"\n{hedef.relative_to(KOK)} yazıldı.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
