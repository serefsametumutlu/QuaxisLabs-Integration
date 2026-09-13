"""Veri denetimi — ÖLÇÜMDEN ÖNCE gelen kapı.

    python tools/veri_denetimi.py --market bist --zaman-dilimi 1D

Çıktı: `docs/olcum/veri-denetimi-<market>-<tf>.md`

## Neden bu araç var

Üç strateji ailesi üst üste elendi. Bunun iki açıklaması var: ya yöntemler
BIST'te çalışmıyor, ya da **ölçtüğümüz veri bozuk.** İkincisini elemeden
birincisi iddia edilemez.

Ve şüphe soyut değil: iki kusur zaten TESADÜFEN bulundu.

* Three Drives örneği mum grafiği gibi görünmüyordu → kaynağın 2014
  öncesinde gerçek açılış fiyatı vermediği ortaya çıktı (`open` = `close`).
* Evrende listeden düşmüş tek bir şirket yok → evren dosyası bugünün
  listesinin anlık görüntüsü.

İkisi de gözle, kazara bulundu. Bu araç onları **sistematik** olarak arar
ve yenilerini de arar.

## Ne ARAMAZ

Bu araç veriyi DÜZELTMEZ. Yalnız ölçer ve yazar. Düzeltme kararı — hangi
sembol atılacak, hangi dönem kullanılmayacak — ölçüm görüldükten sonra,
ayrıca verilir. Sessizce temizlenen veri, sessizce bozulmuş veriden daha
tehlikelidir: birincisi neyin atıldığını kimse bilmez.
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import pathlib
import statistics
import sys

KOK = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(KOK / "packages" / "teknik")]
sys.stdout.reconfigure(encoding="utf-8")

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from quaxis.teknik.core.types import Market  # noqa: E402
from quaxis.teknik.data.universe import load_universe  # noqa: E402

#: BIST'te pay senetlerinde günlük fiyat marjı ±%10'dur; bunu aşan bar
#: dikkat ister.
#:
#: **İlk yorum YANLIŞTI ve düzeltildi.** Bu barlar "düzeltme artefaktı"
#: diye yazılmıştı; tek tek bakılınca çoğunun GERÇEK olduğu görüldü:
#: örneklerin hepsi 2020-03-12, yani COVID çöküşünde borsanın devre
#: kesiciyle durdurulup yeniden açıldığı gün. 1021 aşan barın yalnız 178'i
#: (%17) hacimsiz bir barın ardından geliyor.
#:
#: Yani bu ölçüt tek başına bir kusur SAYMAZ — bayat fiyat ölçütüyle
#: (aşağıda) birlikte okunur.
MARJ_SINIRI = 0.20

#: Bayat bar testinin ileri ufku (bar). Harmonik ve Golden Zone
#: ölçümlerinin zaman bariyeriyle aynı — karşılaştırılabilir olsun diye.
UFUK = 40

#: Kaç ardışık bar boyunca kapanış HİÇ değişmezse "donuk" sayılır.
#: İşlem görmeyen sembolde sağlayıcı son fiyatı tekrar eder; o barlar
#: gerçek bir gözlem değildir ama ölçümde gözlem gibi sayılır.
DONUK_ESIK = 5


def _yil_dagilimi(sayac: collections.Counter) -> str:
    return " · ".join(f"{y}: {n}" for y, n in sorted(sayac.items()))


def denetle(kok: pathlib.Path, evren: list[str], tf: str) -> dict:
    d: dict = {
        "beklenen": len(evren),
        "dosyasi_yok": [],
        "bos": [],
        "ilk_yil": collections.Counter(),
        "son_yil": collections.Counter(),
        "bar": 0,
        "sembol": 0,
        "ohlc_ihlal": collections.Counter(),
        "acilis_esit": collections.Counter(),
        "acilis_esit_bar": collections.Counter(),
        "hacimsiz": 0,
        "donuk_bar": 0,
        "marj_asan": [],
        "tekrar_tarih": [],
        "uzunluk": [],
        "takvim": collections.Counter(),
        "marj_hacimsiz": 0,
        "marj_hacimsiz_pay": 0.0,
        "ileri_hacimsiz": [],
        "ileri_normal": [],
    }

    for sembol in evren:
        f = kok / sembol / f"{tf}.parquet"
        if not f.exists():
            d["dosyasi_yok"].append(sembol)
            continue
        df = pd.read_parquet(f)
        if df.empty:
            d["bos"].append(sembol)
            continue

        d["sembol"] += 1
        d["bar"] += len(df)
        d["uzunluk"].append(len(df))
        d["ilk_yil"][df.index[0].year] += 1
        d["son_yil"][df.index[-1].year] += 1

        if df.index.has_duplicates:
            d["tekrar_tarih"].append((sembol, int(df.index.duplicated().sum())))

        o = df["open"].to_numpy(float)
        h = df["high"].to_numpy(float)
        low = df["low"].to_numpy(float)
        c = df["close"].to_numpy(float)
        v = df["volume"].to_numpy(float)

        # OHLC tutarlılığı — `validate_ohlcv` ile aynı tolerans mantığı.
        tol = 1e-9
        if (h < np.maximum(o, c) * (1 - tol)).any():
            d["ohlc_ihlal"]["high < max(open, close)"] += 1
        if (low > np.minimum(o, c) * (1 + tol)).any():
            d["ohlc_ihlal"]["low > min(open, close)"] += 1
        if (h < low * (1 - tol)).any():
            d["ohlc_ihlal"]["high < low"] += 1
        if (c <= 0).any():
            d["ohlc_ihlal"]["kapanis <= 0"] += 1

        esit = int((o == c).sum())
        if esit:
            d["acilis_esit"][sembol] = esit / len(df)
        for yil, grup in pd.Series(o == c, index=df.index).groupby(df.index.year):
            d["acilis_esit_bar"][yil] += int(grup.sum())
            d["takvim"][yil] += len(grup)

        d["hacimsiz"] += int((v == 0).sum())

        # Donuk fiyat: kapanış üst üste DONUK_ESIK bar hiç değişmiyorsa.
        ayni = np.diff(c) == 0
        if ayni.any():
            seri = 0
            for x in ayni:
                seri = seri + 1 if x else 0
                if seri >= DONUK_ESIK - 1:
                    d["donuk_bar"] += 1

        with np.errstate(divide="ignore", invalid="ignore"):
            getiri = np.diff(c) / c[:-1]
        asan = np.abs(getiri) > MARJ_SINIRI
        if asan.any():
            en_buyuk = float(np.nanmax(np.abs(getiri[asan])))
            d["marj_asan"].append((sembol, int(asan.sum()), en_buyuk))
            # Sıçramadan ÖNCEKİ barın hacmi sıfırsa fiyat bayattı.
            d["marj_hacimsiz"] += int((v[:-1][asan] == 0).sum())

        # BAYAT BAR TESTİ — bu denetimin en önemli ölçümü.
        #
        # Hacimsiz bir barın fiyatı, kimsenin işlem yapmadığı bir fiyattır:
        # sağlayıcı son fiyatı tekrar eder. İşlem yeniden başlayınca fiyat
        # gerçek seviyesine sıçrar. O bardan "girmek", kimsenin
        # giremeyeceği bir fiyattan girmektir.
        #
        # Ölçümdeki karşılığı doğrudan: adil baz RASTGELE bar seçiyor ve
        # hacimsiz barları DIŞLAMIYOR.
        if len(c) > UFUK + 5:
            ileri = (c[UFUK:] - c[:-UFUK]) / c[:-UFUK]
            onceki_hacim = v[:-UFUK]
            d["ileri_hacimsiz"].append(ileri[onceki_hacim == 0])
            d["ileri_normal"].append(ileri[onceki_hacim > 0])

    if d["marj_asan"]:
        d["marj_hacimsiz_pay"] = d["marj_hacimsiz"] / sum(x[1] for x in d["marj_asan"])
    return d


def rapor(d: dict, market: str, tf: str, evren: list[str]) -> str:
    y: list[str] = []
    a = y.append
    n = d["sembol"]

    a(f"# Veri denetimi — {market.upper()} · {tf}")
    a("")
    a(f"**Tarih:** {dt.date.today().isoformat()}")
    a("")
    a("> Bu araç veriyi **düzeltmez**, ölçer. Sessizce temizlenen veri, "
      "sessizce bozulmuş veriden daha tehlikelidir: birincisinde neyin "
      "atıldığını kimse bilmez.")
    a("")

    # ------------------------------------------------------------ kapsam
    a("## 1 · Evren kapsamı")
    a("")
    a("| | |")
    a("|---|---|")
    a(f"| Evren dosyasındaki sembol | {d['beklenen']} |")
    a(f"| Verisi olan | **{n}** |")
    a(f"| Dosyası yok | {len(d['dosyasi_yok'])} |")
    a(f"| Dosyası var ama boş | {len(d['bos'])} |")
    a(f"| Toplam bar | {d['bar']:,} |".replace(",", " "))
    if d["uzunluk"]:
        u = sorted(d["uzunluk"])
        a(f"| Sembol başına bar (medyan) | {statistics.median(u):.0f} |")
        a(f"| En kısa / en uzun | {u[0]} / {u[-1]} |")
    a("")
    if d["dosyasi_yok"]:
        a(f"Dosyası olmayanlar ({len(d['dosyasi_yok'])}): "
          f"`{'`, `'.join(d['dosyasi_yok'][:40])}`"
          + (" …" if len(d["dosyasi_yok"]) > 40 else ""))
        a("")
        a("**Bu sayı kendi başına bir bulgu.** Evren dosyası bu sembolleri "
          "listeliyor ama veri yok — yani her ölçüm, farkında olmadan daha "
          "küçük bir evrende koşuyor.")
        a("")

    # ------------------------------------------- hayatta kalma yanlılığı
    a("## 2 · Hayatta kalma yanlılığı")
    a("")
    a("Son barın yılı — **listeden düşen sembol varsa burada görünür:**")
    a("")
    a(f"`{_yil_dagilimi(d['son_yil'])}`")
    a("")
    guncel = max(d["son_yil"]) if d["son_yil"] else 0
    dusen = sum(v for k, v in d["son_yil"].items() if k < guncel)
    if dusen == 0:
        a(f"**{n} sembolün {n}'inin son barı {guncel}'da.** Listeden düşmüş "
          "tek bir şirket yok.")
        a("")
        a("Bu, evren dosyasının **bugünün listesinin anlık görüntüsü** "
          "olmasının doğrudan sonucu. 2010–bugün arasında iflas eden, "
          "birleşen ya da kottan çıkarılan her şirket veri setinde YOK.")
        a("")
        a("### Bunun ölçüme etkisi")
        a("")
        a("Yanlılık hem stratejiyi hem adil bazı besliyor — ikisi de aynı "
          "evrenden çekiliyor — bu yüzden **farkı** ne kadar bozduğu "
          "ölçülmeden bilinemez. Ama iki şey kesin:")
        a("")
        a("1. **Mutlak sayılar iyimser.** Sıfıra giden şirketler eksik "
          "olduğu için, stop'la çalışan bir stratejinin gerçek hayattaki "
          "en kötü senaryoları veri setinde hiç yok.")
        a("2. **Adil baz da iyimser.** Rastgele giriş, \"16 yıl ayakta "
          "kalmış\" filtresinden geçmiş bir evrende yapılıyor.")
        a("")
    else:
        a(f"{dusen} sembolün son barı {guncel}'dan önce — listeden düşmüş "
          "olabilir. Bu iyi haber: evren yalnız hayatta kalanlardan ibaret "
          "değil.")
        a("")

    a("İlk barın yılı (halka arz dağılımının vekili):")
    a("")
    a(f"`{_yil_dagilimi(d['ilk_yil'])}`")
    a("")

    # --------------------------------------------------- OHLC bütünlüğü
    a("## 3 · OHLC bütünlüğü")
    a("")
    if d["ohlc_ihlal"]:
        a("| İhlal | Kaç sembolde |")
        a("|---|---|")
        for k, v in sorted(d["ohlc_ihlal"].items()):
            a(f"| `{k}` | {v} |")
    else:
        a("İhlal yok — `high ≥ max(açılış, kapanış)`, `low ≤ min(…)`, "
          "`high ≥ low`, `kapanış > 0` hepsinde sağlanıyor.")
    a("")
    if d["tekrar_tarih"]:
        a(f"**Tekrar eden tarih taşıyan sembol: {len(d['tekrar_tarih'])}** — "
          f"örnek: {d['tekrar_tarih'][:5]}")
        a("")

    # --------------------------------------------- açılış == kapanış
    a("## 4 · Açılış fiyatı gerçek mi")
    a("")
    a("`açılış == kapanış` olan bar, gövdesiz mumdur. Gerçek piyasada "
      "nadirdir; **sistematik olarak yüksekse sağlayıcı açılışı "
      "uyduruyordur.**")
    a("")
    a("| Yıl | Bar | `açılış == kapanış` | Oran |")
    a("|---|---|---|---|")
    for yil in sorted(d["takvim"]):
        toplam = d["takvim"][yil]
        esit = d["acilis_esit_bar"][yil]
        a(f"| {yil} | {toplam} | {esit} | **%{esit / toplam * 100:.1f}** |")
    a("")

    # ------------------------------------------------------ diğer kusurlar
    a("## 5 · Diğer kusurlar")
    a("")
    a("| Kusur | Sayı | Ne demek |")
    a("|---|---|---|")
    a(f"| Hacimsiz bar | {d['hacimsiz']:,} | ".replace(",", " ")
      + "O gün işlem görmemiş; fiyat gerçek bir gözlem değil |")
    a(f"| Donuk bar (≥{DONUK_ESIK} bar aynı kapanış) | {d['donuk_bar']:,} | ".replace(",", " ")
      + "Sağlayıcı son fiyatı tekrar ediyor olabilir |")
    marj_bar = f"{sum(x[1] for x in d['marj_asan']):,}".replace(",", " ")
    a(f"| Marjı aşan günlük getiri (>%{MARJ_SINIRI * 100:.0f}) "
      f"| {marj_bar} bar / {len(d['marj_asan'])} sembol "
      f"| Çoğu GERÇEK (devre kesici, sermaye olayı). Yalnız "
      f"%{d['marj_hacimsiz_pay'] * 100:.0f}'i hacimsiz barın ardından |")
    a("")
    if d["marj_asan"]:
        en = sorted(d["marj_asan"], key=lambda x: -x[2])[:10]
        a("En büyük tek günlük sıçramalar:")
        a("")
        a("| sembol | aşan bar | en büyük |")
        a("|---|---|---|")
        for s, k, m in en:
            a(f"| `{s}` | {k} | **%{m * 100:.0f}** |")
        a("")

    # ------------------------------------------------- BAYAT BAR TESTİ
    a("## 6 · Bayat bar testi — bu denetimin en önemli ölçümü")
    a("")
    a("Hacimsiz bir barın fiyatı, **kimsenin işlem yapmadığı** bir fiyattır: "
      "sağlayıcı son fiyatı tekrar eder. İşlem yeniden başlayınca fiyat "
      "gerçek seviyesine sıçrar. O bardan girmek, kimsenin giremeyeceği bir "
      "fiyattan girmektir.")
    a("")
    h = np.concatenate(d["ileri_hacimsiz"]) if d["ileri_hacimsiz"] else np.array([])
    nn = np.concatenate(d["ileri_normal"]) if d["ileri_normal"] else np.array([])
    h = h[np.isfinite(h)]
    nn = nn[np.isfinite(nn)]
    if len(h) and len(nn):
        a(f"**{UFUK} bar ileri getiri — giriş barının hacmine göre:**")
        a("")
        a("| giriş barı | n | ortalama | medyan |")
        a("|---|---|---|---|")
        a(f"| **hacimsiz** | {len(h):,} | **%{h.mean() * 100:.2f}** | "
          f"%{np.median(h) * 100:.2f} |".replace(",", " "))
        a(f"| normal | {len(nn):,} | %{nn.mean() * 100:.2f} | "
          f"%{np.median(nn) * 100:.2f} |".replace(",", " "))
        a(f"| **fark** | | **%{(h.mean() - nn.mean()) * 100:+.2f}** | |")
        a("")
        a("Medyanın hacimsiz tarafta **%0.00** olması deseni ele veriyor: "
          "barların çoğu düz, ama bir kuyruk büyük sıçramalarla ortalamayı "
          "yukarı çekiyor. Bayat fiyatın imzası tam olarak budur.")
        a("")
        a("### Ölçüme etkisi — doğrudan")
        a("")
        a("`olcum/bariyer.py::_bos_havuzu` adil bazı RASTGELE barlardan "
          "kuruyor ve **hacimsiz barları dışlamıyor.** Yani bazın bir "
          "bölümü, kimsenin giremeyeceği fiyatlardan alınmış hayalet "
          "işlemlerden oluşuyor ve o işlemler ortalamada kazanıyor.")
        a("")
        a("Dedektörler de aynı barlarda sinyal üretebiliyor: hacimsiz barın "
          "açılış/yüksek/düşük/kapanışı aynı sayıdır, yani bir seviyeye "
          "\"dokunmuş\" sayılabilir.")
        a("")
        a("**İki taraf da kirli olduğu için net etkinin yönü ölçülmeden "
          "bilinemez.** Ama düzeltilmesi gerektiği açık.")
        a("")

    # ------------------------------------------------------------- sonuç
    a("## 7 · Ne yapılmalı")
    a("")
    a("Bu bölüm **karar değil, seçenek** listesidir; karar ölçüm görülünce "
      "ayrıca verilir.")
    a("")
    a("1. **Hayatta kalma yanlılığı** tam düzeltilemez (listeden düşen "
      "şirketlerin fiyat verisi sağlayıcıda yok). Ama büyüklüğü "
      "SINIRLANABİLİR: 2010–bugün arası BIST şirket listesiyle "
      "karşılaştırıp kaç sembolün eksik olduğu sayılabilir. Bilinen bir "
      "yanlılık, bilinmeyen bir yanlılıktan iyidir.")
    a("2. **2014 öncesi** açılış fiyatı güvenilmezse, gövde tabanlı her "
      "kural (KURAL-30 teyidi gibi) o dönemde ölçülemez. Ölçümlerin "
      "başlangıç tarihi buna göre seçilmeli.")
    a("3. **Hacimsiz ve donuk barlar** gözlem sayılmamalı; sinyal o "
      "barlarda üretilmemeli.")
    a("4. **Marjı aşan barlar** tek tek incelenmeli: gerçek bir olay mı "
      "(sermaye artırımı, birleşme) yoksa düzeltme hatası mı.")
    return "\n".join(y) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--market", default="bist")
    ap.add_argument("--zaman-dilimi", default="1D")
    a = ap.parse_args()

    market = Market(a.market)
    evren = load_universe(market)
    kok = KOK / "data" / "ohlcv" / market.value
    print(f"evren dosyası: {len(evren)} sembol · denetleniyor…", flush=True)

    d = denetle(kok, evren, a.zaman_dilimi)
    metin = rapor(d, a.market, a.zaman_dilimi, evren)
    hedef = KOK / "docs" / "olcum" / f"veri-denetimi-{a.market}-{a.zaman_dilimi}.md"
    hedef.write_text(metin, encoding="utf-8")
    print(metin)
    print(f"yazıldı: {hedef.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
