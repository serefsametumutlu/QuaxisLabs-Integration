"""Koşul taraması — Golden Zone hangi göstergeyle birlikte kenar üretiyor?

    python tools/kosul_taramasi.py --katalog "quaxis.teknik.indicators.katalog:KATALOG" \\
        --gosterge golden_zone --slug golden-zone

Çıktı: `docs/olcum/<slug>-kosul-taramasi-<tarih>.md`

## Neden bu araç var

K4 şunu buldu: Golden Zone **tek başına** kenar üretmiyor (543 sembol, 8432
işlem, +0.045R'ye karşı adil baz +0.071R). Soru şimdi şu: *başka bir
göstergenin koşuluyla birlikte kullanılınca tutarlı hâle geliyor mu?*

Bu, López de Prado'nun meta-etiketleme reçetesinin ta kendisi (s.51–53):
birincil model yönü verir (BOS + OTE bölgesi), ikincil bir katman "gireyim
mi" der. Burada o ikincil katmanın **ne olması gerektiğini arıyoruz**.

## Neden iki eksende birden bölüyoruz

Bir koşulu bütün veride arayıp yine bütün veride doğrulamak, cevabı bildiğin
sınava girmektir. Burada bölme **iki eksende** yapılır:

* **Zaman:** arama ilk %70'te (IS), doğrulama son %30'da (OOS).
* **Sembol:** evren sembol adının hash'iyle A ve B gruplarına ayrılır;
  arama A'da, doğrulama B'de.

Yani doğrulama penceresi arama sırasında ne zaman olarak ne sembol olarak
görülmedi. Hash kullanılır çünkü rastgele bölme "bir daha koşalım belki bu
sefer geçer" kapısını açardı; aynı sembol her koşuda aynı grupta kalır.

## Neden BH-FDR zorunlu

Burada ~15 koşul deneniyor. Düzeltme olmadan **birinin tesadüfen p<0.05
vermesi neredeyse kesindir** — 20 stratejiden birinin şansa geçmesiyle aynı
şey. Benjamini-Hochberg ailenin tamamına uygulanır ve rapor ham p ile
düzeltilmiş kararı YAN YANA gösterir.

## Neden ΔR, "R" değil

Bir koşul kendi başına pozitif R verebilir — ama bölgesiz de verebilirdi.
Ölçülen şey koşulun **eklediği** R: `koşullu R − koşulsuz R`. Ayrıca her
satırda işlem sayısı durur: koşul örneklemi 30'un altına düşürüyorsa sayı
yazılır, verdikt yazılmaz (Pardo s.295).
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import pathlib
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass

KOK = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "packages" / "teknik"))

# Windows konsolu cp1254; "Δ" gibi karakterler UnicodeEncodeError atıp koşuyu
# ÖLDÜRÜYORDU. Rapor dosyası zaten UTF-8 — konsol da öyle olsun.
for akis in (sys.stdout, sys.stderr):
    if hasattr(akis, "reconfigure"):
        akis.reconfigure(encoding="utf-8", errors="replace")

import pandas as pd  # noqa: E402
from katmanli_olcum import ASGARI_ISLEM, tara  # noqa: E402
from quaxis.teknik.core.types import Market, Signal, Timeframe  # noqa: E402
from quaxis.teknik.olcum.bariyer import RResult, measure_r  # noqa: E402
from quaxis.teknik.olcum.ileri_getiri import bh_fdr  # noqa: E402

OLCUM_KOK = KOK / "docs" / "olcum"

#: Piyasa rejimi için kıyas endeksi. Sembolün kendi göstergesi değil,
#: PİYASANIN durumu — tamamen farklı bir eksen ve BIST içinde kalıyor.
ENDEKS = "XU100"


def _var(p: dict, ad: str) -> bool:
    return p.get(ad) is not None


def _ustunde(ad: str, esik: float) -> Callable[[dict], bool]:
    return lambda p: _var(p, ad) and float(p[ad]) > esik


def _altinda(ad: str, esik: float) -> Callable[[dict], bool]:
    return lambda p: _var(p, ad) and float(p[ad]) < esik


def _arasinda(ad: str, alt: float, ust: float) -> Callable[[dict], bool]:
    return lambda p: _var(p, ad) and alt <= float(p[ad]) <= ust


def _dogru(ad: str) -> Callable[[dict], bool]:
    return lambda p: p.get(ad) is True


def endeks_rejimi(market: Market, tf: Timeframe) -> pd.Series | None:
    """Endeksin EMA50'sinin üstünde mi — bar bar, True/False.

    Sinyale bar tarihinden bakılır; ileriye bakış yok. Endeks verisi yoksa
    `None` döner ve rejim koşulları taramadan SESSİZCE düşmez — rapor
    bunu yazar.
    """
    from quaxis.teknik.data.providers.yfinance_provider import YFinanceProvider
    from quaxis.teknik.data.store import Store

    try:
        df = Store(YFinanceProvider()).get(ENDEKS, tf, market)
    except FileNotFoundError:
        return None
    k = df["close"]
    return (k > k.ewm(span=50, adjust=False, min_periods=50).mean())


def _rejim_ekle(sinyaller: dict, rejim: pd.Series | None) -> None:
    """Endeks rejimini her sinyalin payload'ına yazar.

    Bu bir ARAÇ işi, dedektör işi değil: dedektör tek bir sembolün df'sini
    görür, endeksi görmez. İki katmanı birbirine bağlamak aracın görevi
    (README madde 2).
    """
    if rejim is None:
        return
    for liste in sinyaller.values():
        for g in liste:
            try:
                deger = rejim.asof(g.detected_at)
            except (KeyError, TypeError):
                deger = None
            g.payload["endeks_yukselen"] = None if pd.isna(deger) else bool(deger)


#: Denenen koşullar. Her biri bir HİPOTEZ taşır ve hipotez yazılıdır —
#: "bir sürü şey deneyelim tutarsa tutar" bu tablonun yapmadığı şey.
KOSULLAR: dict[str, tuple[str, Callable[[dict], bool]]] = {
    "ema50_uyum": ("Fiyat EMA50'nin doğru tarafında — 'trendle işlem yap'", _dogru("ema50_uyum")),
    "ema200_uyum": ("Fiyat EMA200'ün doğru tarafında — uzun vadeli eğilim", _dogru("ema200_uyum")),
    "ema_egim_uyum": ("EMA50'nin EĞİMİ sinyal yönünde — seviye değil yön", _dogru("ema_egim_uyum")),
    "ema50_ve_egim": (
        "EMA50 hem seviye hem eğim olarak uyumlu",
        lambda p: p.get("ema50_uyum") is True and p.get("ema_egim_uyum") is True,
    ),
    "rsi_notr": ("RSI 40-60 — düzeltme tükenmemiş", _arasinda("rsi14", 40, 60)),
    "rsi_guclu": ("RSI 55 üstü — momentum sinyal yönünde", _ustunde("rsi14", 55)),
    "rsi_zayif": ("RSI 45 altı — derin düzeltme", _altinda("rsi14", 45)),
    "hacim_yuksek": (
        "Kırılım hacmi 20 bar ortalamasının 1.5 katı üstünde",
        _ustunde("hacim_orani", 1.5),
    ),
    "hacim_cok_yuksek": ("Kırılım hacmi 2 kat üstünde", _ustunde("hacim_orani", 2.0)),
    "oynaklik_dusuk": ("ATR14/ATR50 < 1 — sakin rejim", _altinda("atr_rejim", 1.0)),
    "oynaklik_yuksek": ("ATR14/ATR50 > 1.2 — genişleyen oynaklık", _ustunde("atr_rejim", 1.2)),
    "bacak_guclu": ("Yer değiştirme bacağı 3 ATR'den uzun", _ustunde("bacak_atr", 3.0)),
    "donus_hizli": ("Kırılımdan bölgeye 5 barda dönülmüş", _altinda("donus_bar", 5)),
    "donus_yavas": ("Dönüş 10 bardan uzun sürmüş", _ustunde("donus_bar", 10)),
    "derin_giris": ("Bölgeye 0.705'in altına kadar girilmiş", _ustunde("derinlik", 0.705)),
    "fvg": ("Bacakta adil değer boşluğu var", _dogru("fvg")),
    "supurme": ("Kurulum likidite süpürmesiyle başlamış", _dogru("supurme")),
    # --- ikinci tur ---
    "adx_guclu": ("ADX 25 üstü — belirgin trend", _ustunde("adx14", 25)),
    "adx_zayif": ("ADX 20 altı — yatay/sıkışık piyasa", _altinda("adx14", 20)),
    "macd_uyum": ("MACD histogramı sinyal yönünde", _dogru("macd_uyum")),
    "obv_uyum": ("OBV eğimi sinyal yönünde — hacim fiyatı teyit ediyor", _dogru("obv_uyum")),
    "ema20_50_uyum": ("EMA20/EMA50 dizilimi sinyal yönünde", _dogru("ema20_50_uyum")),
    "bb_sikisma": (
        "Bollinger genişliği son 120 barın alt %30'unda", _altinda("bb_yuzdelik", 0.30),
    ),
    "bb_genis": ("Bollinger genişliği üst %30'da", _ustunde("bb_yuzdelik", 0.70)),
    "stok_dusuk": ("Stokastik %K 30 altı — düzeltme derinleşmiş", _altinda("stok14", 30)),
    "stok_yuksek": ("Stokastik %K 70 üstü", _ustunde("stok14", 70)),
    "ema_yakin": (
        "Fiyat EMA50'ye 1 ATR'den yakın — aşırı uzaklaşmamış",
        lambda p: _var(p, "ema50_uzaklik_atr") and abs(float(p["ema50_uzaklik_atr"])) < 1,
    ),
    "ema_uzak": ("Fiyat EMA50'den 2 ATR'den uzak", _ustunde("ema50_uzaklik_atr", 2.0)),
    "govde_guclu": (
        "Sinyal barının gövdesi aralığın %60'ından büyük", _ustunde("govde_orani", 0.6),
    ),
    "aralik_genis": ("Sinyal barının aralığı 1.5 ATR üstü", _ustunde("aralik_atr", 1.5)),
    "likit": ("Ortalama ciro 20 milyon TL üstü", _ustunde("ciro", 20_000_000)),
    "cok_likit": ("Ortalama ciro 100 milyon TL üstü", _ustunde("ciro", 100_000_000)),
    "endeks_yukselen": ("XU100 kendi EMA50'sinin üstünde — piyasa rejimi",
                        _dogru("endeks_yukselen")),
    "endeks_dusen": ("XU100 EMA50'sinin altında",
                     lambda p: p.get("endeks_yukselen") is False),
    "rejim_ve_yon": (
        "Piyasa rejimi sinyal yönüyle uyumlu (yükselen piyasada AL)",
        lambda p: (
            p.get("endeks_yukselen") is not None
            and bool(p["endeks_yukselen"]) == (float(p["hedef"]) > float(p["giris"]))
        ),
    ),
}


@dataclass
class KosulSonucu:
    ad: str
    hipotez: str
    ic: RResult
    dis: RResult | None = None

    @property
    def guvenilir(self) -> bool:
        return self.ic.n_trades >= ASGARI_ISLEM


def sembol_grubu(sembol: str) -> int:
    """Sembolü deterministik olarak A(0) ya da B(1) grubuna atar.

    Rastgele değil HASH: aynı sembol her koşuda aynı grupta kalır, yoksa
    "bir daha koşalım belki bu sefer geçer" kapısı açılırdı.
    """
    return int(hashlib.sha1(sembol.encode()).hexdigest(), 16) % 2


def _grup(d: dict, grup: int | None) -> dict:
    if grup is None:
        return d
    return {k: v for k, v in d.items() if sembol_grubu(k) == grup}


def _islemler(sinyaller: dict[str, Sequence[Signal]], kosul=None):
    out = {}
    for sembol, liste in sinyaller.items():
        secilen = [g for g in liste if kosul is None or kosul(g.payload)]
        if secilen:
            out[sembol] = [
                (g, float(g.payload["stop"]), float(g.payload["hedef"])) for g in secilen
            ]
    return out


def _olc(ohlc, islemler, pencere: str, bariyer: int, turlar: int) -> RResult:
    return measure_r(
        ohlc, islemler, max_bars=bariyer, pencere=pencere, permutations=turlar
    )


def rapor(
    taban_ic: RResult, taban_dis: RResult, sonuclar: list[KosulSonucu],
    fdr: dict[str, bool], slug: str, gosterge: str,
) -> str:
    arama = []
    for k in sorted(sonuclar, key=lambda x: -(x.ic.mean_r - taban_ic.mean_r)):
        d = k.ic.mean_r - taban_ic.mean_r
        not_ = "" if k.guvenilir else " ⚠"
        arama.append(
            f"| `{k.ad}` | {k.hipotez} | {k.ic.n_trades}{not_} | {k.ic.mean_r:+.3f}R | "
            f"{d:+.3f}R | {k.ic.p_value:.4f} | {'geçti' if fdr.get(k.ad) else '—'} |"
        )

    gecenler = [k for k in sonuclar if fdr.get(k.ad) and k.guvenilir]
    if gecenler:
        dogrulama = "\n".join(
            f"| `{k.ad}` | {k.dis.n_trades if k.dis else 0} | "
            f"{k.dis.mean_r:+.3f}R | {k.dis.baseline_mean_r:+.3f}R | "
            f"{k.dis.mean_r - taban_dis.mean_r:+.3f}R | {k.dis.p_value:.4f} | "
            f"{'**kenar-var**' if k.dis and k.dis.p_value <= 0.05 else 'kanıtlanmadı'} |"
            for k in gecenler if k.dis is not None
        )
        dogrulama_bolumu = f"""| Koşul | İşlem | Ort. R | Adil baz | ΔR | p | Verdikt |
|---|---|---|---|---|---|---|
{dogrulama}"""
    else:
        dogrulama_bolumu = (
            "**Arama penceresinde BH-FDR'yi geçen koşul olmadı.** Doğrulanacak "
            "bir aday yok — bu, taramanın başarısızlığı değil sonucudur."
        )

    return f"""# {slug} — Koşul Taraması

**Tarih:** {dt.date.today().isoformat()} · **Gösterge:** `{gosterge}`

K4 şunu bulmuştu: Golden Zone **tek başına** kenar üretmiyor. Bu tarama
sorunun devamını yanıtlıyor: *başka bir göstergenin koşuluyla birlikte
tutarlı hâle geliyor mu?*

| | |
|---|---|
| Denenen koşul | {len(sonuclar)} |
| Arama | **A grubu sembol + IS penceresi** (ilk %70) —
{taban_ic.n_trades} işlem, {taban_ic.n_symbols} sembol |
| Doğrulama | **B grubu sembol + OOS penceresi** (son %30) —
{taban_dis.n_trades} işlem, {taban_dis.n_symbols} sembol |
| Koşulsuz taban (IS) | {taban_ic.mean_r:+.3f}R (adil baz {taban_ic.baseline_mean_r:+.3f}R) |
| Koşulsuz taban (OOS) | {taban_dis.mean_r:+.3f}R (adil baz {taban_dis.baseline_mean_r:+.3f}R) |

## 1. Arama (IS penceresi)

`ΔR` koşulun **eklediği** R: koşullu R eksi koşulsuz taban. ⚠ işareti
{ASGARI_ISLEM} işlemin altını gösterir — sayı yazılır, verdikt yazılmaz.

| Koşul | Hipotez | İşlem | Ort. R | ΔR | ham p | BH-FDR (q=0.05) |
|---|---|---|---|---|---|---|
{chr(10).join(arama)}

> **Ham p'ye tek başına bakmak yanıltır.** {len(sonuclar)} koşul denendi;
> düzeltme olmadan birinin tesadüfen 0.05'in altına düşmesi neredeyse
> kesindir. Karar sütunu BH-FDR'dir.

## 2. Doğrulama (OOS penceresi)

Yalnız BH-FDR'yi geçen ve örneklemi yeterli olan koşullar buraya iner.
**Rapora giren sayı budur**; arama penceresininki değil.

{dogrulama_bolumu}

## Ne çıkarsa o

*(Hiçbir koşul geçmediyse bu da bir sonuçtur ve öyle yazılır: "Golden Zone,
denenen {len(sonuclar)} koşulun hiçbiriyle birlikte kenar üretmedi." Geçen
varsa, OOS sayısı IS sayısından belirgin düşükse bu aşırı uydurmanın
imzasıdır ve belirtilir.)*

## Ölçümün sınırları

| | |
|---|---|
| Çoklu test | BH-FDR uygulandı; yine de OOS doğrulaması TEK bir pencerede |
| Eşikler | Koşul eşikleri (EMA50, RSI 40-60, hacim 1.5×…) **denenmiş
değerlerdir**, optimize EDİLMEDİ — optimize edilseydi aşırı uydurma riski
katlanırdı |
| İşlem maliyeti | **dahil** — taraf başına %0.05 komisyon + çıkışta %0.05 kayma |
| Aynı barda stop+hedef | **stop** sayıldı |

> Bağımsız gözlem birimi **sembol**dür, bar değil.
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Golden Zone koşul taraması")
    ap.add_argument("--katalog", required=True)
    ap.add_argument("--gosterge", default="golden_zone")
    ap.add_argument("--slug", default="golden-zone")
    ap.add_argument("--zaman-dilimi", default="1D")
    ap.add_argument("--market", default="bist")
    ap.add_argument("--tur", type=int, default=2000)
    ap.add_argument("--evren", default=None)
    a = ap.parse_args()

    market, tf = Market(a.market), Timeframe(a.zaman_dilimi)
    if a.evren:
        evren = [s.strip() for s in a.evren.split(",") if s.strip()]
    else:
        from quaxis.teknik.data.universe import load_universe

        evren = load_universe(market)

    print(f"Tarama: {len(evren)} sembol · {tf.value}", flush=True)
    ohlc, sinyaller, _ = tara(a.katalog, a.gosterge, evren, tf, market)

    rejim = endeks_rejimi(market, tf)
    if rejim is None:
        print(f"UYARI: {ENDEKS} verisi yok — rejim koşulları ölçülemeyecek.", flush=True)
    _rejim_ekle(sinyaller, rejim)
    print(f"Veri: {len(ohlc)} sembol · ham sinyal: {sum(len(v) for v in sinyaller.values())}",
          flush=True)

    # ARAMA A grubunda + IS penceresinde; DOĞRULAMA B grubunda + OOS'ta.
    # İki eksen birden bağımsız: doğrulama penceresi arama sırasında ne
    # zaman olarak ne sembol olarak görülmedi.
    a_sinyal, b_sinyal = _grup(sinyaller, 0), _grup(sinyaller, 1)
    a_ohlc, b_ohlc = _grup(ohlc, 0), _grup(ohlc, 1)
    print(f"Arama grubu A: {len(a_sinyal)} sembol · Doğrulama grubu B: {len(b_sinyal)} sembol",
          flush=True)

    tum = _islemler(sinyaller)
    bariyer = 40
    for liste in tum.values():
        bariyer = int(liste[0][0].payload.get("zaman_bariyeri", bariyer))
        break

    taban_ic = _olc(a_ohlc, _islemler(a_sinyal), "is", bariyer, a.tur)
    taban_dis = _olc(b_ohlc, _islemler(b_sinyal), "oos", bariyer, a.tur)
    print(f"Taban  IS: {taban_ic.mean_r:+.3f}R ({taban_ic.n_trades} işlem) · "
          f"OOS: {taban_dis.mean_r:+.3f}R ({taban_dis.n_trades} işlem)", flush=True)

    sonuclar: list[KosulSonucu] = []
    for ad, (hipotez, kosul) in KOSULLAR.items():
        r = _olc(a_ohlc, _islemler(a_sinyal, kosul), "is", bariyer, a.tur)
        sonuclar.append(KosulSonucu(ad, hipotez, r))
        print(f"  {ad:18} {r.n_trades:5} işlem · {r.mean_r:+.3f}R "
              f"(Δ {r.mean_r - taban_ic.mean_r:+.3f}R) · p={r.p_value:.4f}", flush=True)

    fdr = bh_fdr({k.ad: k.ic.p_value for k in sonuclar if k.guvenilir}, q=0.05)

    for k in sonuclar:
        if fdr.get(k.ad) and k.guvenilir:
            k.dis = _olc(
                b_ohlc, _islemler(b_sinyal, KOSULLAR[k.ad][1]), "oos", bariyer, a.tur
            )
            print(f"  DOĞRULAMA {k.ad}: OOS {k.dis.mean_r:+.3f}R · p={k.dis.p_value:.4f}",
                  flush=True)

    OLCUM_KOK.mkdir(parents=True, exist_ok=True)
    hedef = OLCUM_KOK / f"{a.slug}-kosul-taramasi-{dt.date.today().isoformat()}.md"
    hedef.write_text(rapor(taban_ic, taban_dis, sonuclar, fdr, a.slug, a.gosterge),
                     encoding="utf-8")
    print(f"\n{hedef.relative_to(KOK)} yazıldı.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
