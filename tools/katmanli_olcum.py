"""K3+K4 katmanlı ölçüm koşucusu — "kenar var mı" değil, "kenar EKLİYOR mu".

    python tools/katmanli_olcum.py --katalog "quaxis.teknik.indicators.katalog:KATALOG" \\
        --gosterge golden_zone --slug golden-zone --zaman-dilimi 1D

Çıktı: `docs/olcum/<slug>-K3-<katman>.md` (her katman için aday sayımı) ve
`docs/olcum/<slug>-K4-katmanli-<tarih>.md` (tek tabloda karşılaştırma).

## Neden katman

Dedektör süpürme/FVG/Order Block'u FİLTRELEMİYOR, payload'a bayrak yazıyor.
Katmanlar dedektörün içinde sabitlenseydi hangi katmanın kenar *eklediği*
ölçülemezdi — yalnızca hepsi birlikte ölçülebilirdi. López de Prado'nun
meta-etiketleme reçetesi (s.51–53) bunun tersini söyler: önce yüksek
recall'lı birincil model, sonra precision'ı düzelten ikincil katman.

| Katman | İçerik | Rolü |
|---|---|---|
| A | yapı kırılımı + OTE bölgesi | birincil model (yön) |
| B | A + (FVG veya bölgedeki Order Block) | precision filtresi |
| C | B + likidite süpürmesi | ikinci precision filtresi |

## Neden her satırda işlem sayısı var

Her teyit katmanı bir kural, bir serbestlik derecesi ve daha küçük bir
örneklem demektir (Pardo s.291–293). Katman ekledikçe "iyileşen" bir
ölçüt, iyileşmeyi kenardan değil örneklem küçülmesinden alıyor olabilir.
**30 işlemin altına düşen katmanın sayısı yazılır, verdikti yazılmaz**
(Pardo s.295: "Thirty to 50 trades is an adequate minimum").
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import sys
from collections.abc import Sequence
from dataclasses import dataclass

KOK = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "packages" / "teknik"))

import pandas as pd  # noqa: E402
from quaxis.teknik.core.types import Market, Signal, Timeframe  # noqa: E402
from quaxis.teknik.data.providers.yfinance_provider import YFinanceProvider  # noqa: E402
from quaxis.teknik.data.store import Store  # noqa: E402
from quaxis.teknik.olcum.bariyer import RResult, measure_r  # noqa: E402
from quaxis.teknik.olcum.ileri_getiri import ForwardReturnResult, measure  # noqa: E402
from quaxis.teknik.olcum.kalibrasyon import CalibrationResult, calibrate  # noqa: E402
from quaxis.teknik.scanner import engine  # noqa: E402

OLCUM_KOK = KOK / "docs" / "olcum"

BASLIK = (
    "| Katman | İçerik | İşlem | Sembol | İsabet | Ort. R | Adil baz | ΔR "
    "| p (R) | İleri getiri | p | Verdikt |"
)

#: Pardo s.295. Altına düşen katman sayı üretir, VERDİKT üretmez.
ASGARI_ISLEM = 30


def _ob_bolgede(p: dict) -> bool:
    """Order Block bölgenin İÇİNDE mi? Bölgenin dışındaki bir OB teyit değil,
    tesadüftür — 'yakınlarda bir yerde vardı' diyerek katman şişirmek
    ölçümü kendi lehine çevirmenin en kolay yoludur."""
    ob = p.get("order_block")
    if ob is None:
        return False
    alt, ust = sorted((float(p["bolge_derin"]), float(p["giris"])))
    return alt <= float(ob) <= ust


KATMANLAR: dict[str, tuple[str, object]] = {
    "A": ("yapı kırılımı + OTE bölgesi", lambda p: True),
    "B": ("A + (FVG veya bölgedeki Order Block)", lambda p: bool(p.get("fvg")) or _ob_bolgede(p)),
    "C": ("B + likidite süpürmesi", lambda p: (bool(p.get("fvg")) or _ob_bolgede(p))
          and bool(p.get("supurme"))),
}


@dataclass
class KatmanSonucu:
    ad: str
    aciklama: str
    kalibrasyon: CalibrationResult
    ileri: ForwardReturnResult
    r: RResult

    @property
    def guvenilir(self) -> bool:
        return self.r.n_trades >= ASGARI_ISLEM

    @property
    def verdikt(self) -> str:
        if not self.guvenilir:
            return f"örneklem yetersiz (n={self.r.n_trades})"
        return self.r.verdict


def tara(katalog: str, gosterge: str, evren: list[str], tf: Timeframe, market: Market):
    """Taramayı BİR KEZ koşar; katmanlar aynı sinyal kümesinden süzülür."""
    scan = engine.run(
        run_id=f"katman_{gosterge}_{dt.date.today().isoformat()}",
        universe=evren, timeframes=[tf], indicator_names=[gosterge],
        market=market, catalog=katalog, workers=1,
    )
    store = Store(YFinanceProvider())
    ohlc: dict[str, pd.DataFrame] = {}
    sinyaller: dict[str, list[Signal]] = {}
    hatali = 0
    for r in scan.results:
        if r.error or r.result is None:
            hatali += 1
            continue
        try:
            ohlc[r.symbol] = store.get(r.symbol, tf, market)
        except FileNotFoundError:
            hatali += 1
            continue
        sinyaller[r.symbol] = list(r.result.signals)
    return ohlc, sinyaller, hatali


def katman_olc(
    ad: str, aciklama: str, kosul, ohlc: dict[str, pd.DataFrame],
    sinyaller: dict[str, Sequence[Signal]], gosterge: str, tf: Timeframe,
    ufuk: int, hatali: int, turlar: int,
) -> KatmanSonucu:
    suzulmus = {s: [g for g in liste if kosul(g.payload)] for s, liste in sinyaller.items()}
    kalib = calibrate(
        gosterge, tf.value, {s: len(v) for s, v in suzulmus.items()}, error_symbols=hatali
    )
    ileri = measure(
        {s: df["close"] for s, df in ohlc.items()}, suzulmus, horizon=ufuk, permutations=turlar
    )
    islemler = {
        s: [(g, float(g.payload["stop"]), float(g.payload["hedef"])) for g in liste]
        for s, liste in suzulmus.items() if liste
    }
    # Zaman bariyeri STRATEJİNİN kendi parametresidir; ölçüm uydurmaz.
    bariyer = 40
    for liste in islemler.values():
        bariyer = int(liste[0][0].payload.get("zaman_bariyeri", bariyer))
        break
    r = measure_r(ohlc, islemler, max_bars=bariyer, permutations=turlar)
    return KatmanSonucu(ad, aciklama, kalib, ileri, r)


def rapor(katmanlar: list[KatmanSonucu], slug: str, gosterge: str, tf: Timeframe) -> str:
    satir = []
    onceki: KatmanSonucu | None = None
    for k in katmanlar:
        delta = "—" if onceki is None else f"{k.r.mean_r - onceki.r.mean_r:+.3f}R"
        satir.append(
            f"| **{k.ad}** | {k.aciklama} | {k.r.n_trades} | {k.r.n_symbols} | "
            f"%{k.r.win_rate * 100:.1f} | {k.r.mean_r:+.3f}R | {k.r.baseline_mean_r:+.3f}R | "
            f"{delta} | {k.r.p_value:.4f} | %{k.ileri.mean_difference * 100:+.2f} | "
            f"{k.ileri.p_value:.4f} | {k.verdikt} |"
        )
        onceki = k
    tablo = "\n".join(satir)

    zayif = [k.ad for k in katmanlar if not k.guvenilir]
    uyari = (
        f"\n> **Örneklem uyarısı:** {', '.join(zayif)} katmanı {ASGARI_ISLEM} işlemin "
        f"altında. Sayıları yukarıda duruyor ama **verdikt üretmiyorlar** "
        f"(Pardo s.295).\n" if zayif else ""
    )

    oos = (katmanlar[0].r.oos_ratio if katmanlar else 0.30) * 100
    return f"""# {slug} — K4 Katmanlı Ölçüm

**Tarih:** {dt.date.today().isoformat()} · **Gösterge:** `{gosterge}` · **Zaman dilimi:** {tf.value}

Soru katman başına "kenar var mı" değil, **"kenar EKLİYOR mu"**. `ΔR` sütunu
bir önceki katmana göre işlem başına beklenen R değişimidir.

**Pencere:** her iki ölçüm de yalnız **OOS** penceresini sayar (serinin son
%{oos:.0f}'i). İki sütun aynı dönemden konuşmazsa tablo sessizce yanıltır.

{BASLIK}
|---|---|---|---|---|---|---|---|---|---|---|---|
{tablo}
{uyari}
## Katman başına aday sayımı (K3)

{chr(10).join(f"**{k.ad}** — {k.kalibrasyon.diagnosis}" for k in katmanlar)}

## Ne çıkarsa o

*(Katman ekledikçe R artıyorsa bu tek başına kanıt DEĞİLDİR: örneklem de
küçülüyor. Artış hem ΔR'de hem p değerinde görünmeli, ve işlem sayısı
{ASGARI_ISLEM}'un üstünde kalmalı. Aksi halde iyileşme kenardan değil
serbestlik derecesinden geliyordur — Pardo s.291-293.)*

## Ölçümün sınırları

| | |
|---|---|
| Dönem | *(hangi tarih aralığı)* |
| Evren | *(kaç sembol, neden)* |
| İşlem maliyeti | **yok** — komisyon/spread hesaba katılmadı |
| Hayatta kalma yanlılığı | *(evren bugünkü listeden geliyorsa belirt)* |
| Aynı barda stop+hedef | **stop** sayıldı (iyimserliğe karşı) |

> Bağımsız gözlem birimi **sembol**dür, bar değil.
"""


def k3_raporu(k: KatmanSonucu, slug: str, tf: Timeframe, donem: str) -> str:
    """Katman başına K3 kalibrasyon raporu.

    Pasaportun K0 eşik tablosu bu dosyaları `K3:` kaynağı olarak gösterir;
    doğrulayıcı dosyayı DİSKTE arar. Yazılmazsa K0 kapanamaz — bu kasıtlı.
    """
    c = k.kalibrasyon
    return f"""# {slug} — K3 Kalibrasyon · Katman {k.ad}

**Tarih:** {dt.date.today().isoformat()} · **Gösterge:** `{c.indicator}`
**Zaman dilimi:** {c.timeframe}

**Katman {k.ad}:** {k.aciklama}

| Ölçüt | Değer |
|---|---|
| Evren | {c.universe} sembol |
| Toplam aday | {c.total_candidates} |
| **Sıfır aday veren sembol** | **{c.zero_candidate_symbols}** (%{c.zero_ratio * 100:.1f}) |
| Veri hatası alan sembol | {c.error_symbols} |
| Sembol başına ortalama | {c.per_symbol_mean:.2f} |
| Sembol başına ortanca | {c.per_symbol_median:.1f} |
| Sembol başına en çok | {c.per_symbol_max} |
| Dönem | {donem} |

## Teşhis

{c.diagnosis}

## Eşikler bu ölçümden nasıl türetildi

*(K0'ın eşik tablosundaki her `K3:` devri burada kapanır. Hangi sayı hangi
gözlemden geldi — "makul göründü" bir gerekçe değildir.)*

| Eşik | Değer | Bu ölçümden türetilişi |
|---|---|---|
| bolge_sig | | |
| bolge_derin | | |
| yer_degistirme_atr | | |
| donus_max_bar | | |

> "Veri çekilemedi" ile "aday bulunamadı" AYRI sayılır. Önceki projede
> 648/648 sembolde sıfır aday çıkmıştı ve kimse kaçının veri hatası
> olduğunu bilmiyordu.
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Katmanlı K3+K4 koşucusu")
    ap.add_argument("--katalog", required=True)
    ap.add_argument("--gosterge", required=True)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--zaman-dilimi", default="1D")
    ap.add_argument("--market", default="bist")
    ap.add_argument("--ufuk", type=int, default=20)
    ap.add_argument("--tur", type=int, default=2000, help="permütasyon turu")
    ap.add_argument("--evren", default=None)
    a = ap.parse_args()

    market = Market(a.market)
    tf = Timeframe(a.zaman_dilimi)
    if a.evren:
        evren = [s.strip() for s in a.evren.split(",") if s.strip()]
    else:
        from quaxis.teknik.data.universe import load_universe

        evren = load_universe(market)

    print(f"Tarama: {len(evren)} sembol · {tf.value}", flush=True)
    ohlc, sinyaller, hatali = tara(a.katalog, a.gosterge, evren, tf, market)
    toplam = sum(len(v) for v in sinyaller.values())
    print(f"Veri: {len(ohlc)} sembol hazır, {hatali} hata · ham sinyal: {toplam}", flush=True)
    if toplam == 0:
        print("Hiç sinyal yok — ölçüm yapılamaz. K3 raporu yine de yazılıyor.")

    sonuclar = []
    for ad, (aciklama, kosul) in KATMANLAR.items():
        print(f"  katman {ad} ölçülüyor…", flush=True)
        sonuclar.append(
            katman_olc(ad, aciklama, kosul, ohlc, sinyaller, a.gosterge, tf, a.ufuk, hatali, a.tur)
        )
        s = sonuclar[-1]
        print(
            f"  {ad}: {s.r.n_trades} işlem · {s.r.mean_r:+.3f}R "
            f"(baz {s.r.baseline_mean_r:+.3f}R) · p={s.r.p_value:.4f} · {s.verdikt}",
            flush=True,
        )

    OLCUM_KOK.mkdir(parents=True, exist_ok=True)
    donem = "—"
    if ohlc:
        ilk = min(df.index[0] for df in ohlc.values())
        son = max(df.index[-1] for df in ohlc.values())
        donem = f"{ilk.date()} – {son.date()}"
    for k in sonuclar:
        k3 = OLCUM_KOK / f"{a.slug}-K3-{k.ad}.md"
        k3.write_text(k3_raporu(k, a.slug, tf, donem), encoding="utf-8")
        print(f"{k3.relative_to(KOK)} yazıldı.")

    hedef = OLCUM_KOK / f"{a.slug}-K4-katmanli-{dt.date.today().isoformat()}.md"
    hedef.write_text(rapor(sonuclar, a.slug, a.gosterge, tf), encoding="utf-8")
    print(f"\n{hedef.relative_to(KOK)} yazıldı.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
