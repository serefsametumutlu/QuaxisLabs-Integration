---
# ── Makine tarafından okunan künye ────────────────────────────────────────
# `python tools/pasaport.py dogrula` bu bloğu denetler. Elle "geçti" yazmak
# yetmez: her kapının kanıtı DİSKTE bulunmak zorundadır.
slug: golden-zone            # dosya adıyla aynı, küçük harf, tireli
ad: Golden Zone              # kullanıcıya görünen ad
paket: yapi                     # yapi | formasyon | trend | arbitraj
referans: "references/G8es0m9W4AAiTAK.png"   # ANLAMAK için, kopyalamak için değil

# Bu pasaportun KAPSADIĞI gösterge künyeleri (`indicators/katalog.py`).
# Tarama yüzeyindeki verdikt rozeti bu eşlemeden okunur — rozet uydurulmaz.
# `pasaport.py dogrula` katalogdaki her göstergenin TAM BİR pasaport
# tarafından sahiplenildiğini denetler.
gostergeler:
  golden_zone: "Golden Zone"
  golden_zone_r2: "Golden Zone · 2R"

# K4'ün çıktısı. Kapı AÇILMADAN "ölçülmedi" dışında bir değer yazılamaz.
#   olculmedi     — K4 açılmadı, elimizde sayı yok
#   kanitlanmadi  — ölçüldü, FDR sonrası kenar bulunamadı
#   izlenen-aday  — ölçüldü, en az çürütülmüş grupta
#   kenar-var     — ölçüldü, FDR eşiğini geçti
verdikt: kanitlanmadi

# Ürünleştirme durduruldu. Bu üçü BİRLİKTE olmadan `pasaport.py` bunu
# "bitmiş" saymaz — "hepsini durduruldu yaz, yenisine başla" yolu kapalı.
durum: durduruldu
durdurma_gerekcesi: >
  Kenar bulunamadi. 35 kosulluk tarama, cift eksende (zaman + sembol) bolme,
  on kayitli kombinasyon testi, iki zaman dilimi ve likidite/fiyat/sektor
  kirilimi olculdu; isleme maliyeti dahil hicbirinde adil bazi asan kalici
  bir fark cikmadi. Dedektor ve komposer duruyor; ileride baska bir
  stratejinin ek kosulu olarak degerlendirilecek.
  Ozet: docs/olcum/GOLDEN-ZONE-OZET.md

kapilar:
  K0: { gecildi: 2026-09-13, kanit: ["docs/strateji/kaynak/golden-zone-K0.md", "docs/olcum/golden-zone-K3-A.md"] }
  K1: { gecildi: 2026-09-13, kanit: ["packages/teknik/quaxis/teknik/indicators/golden_zone/parametreler.py"] }
  K2: { gecildi: 2026-09-13, kanit: ["packages/teknik/quaxis/teknik/indicators/golden_zone/dedektor.py", "packages/teknik/tests/test_golden_zone.py"] }
  K3: { gecildi: 2026-09-13, kanit: ["docs/olcum/golden-zone-K3-A.md", "docs/olcum/golden-zone-K3-B.md", "docs/olcum/golden-zone-K3-C.md", "docs/olcum/veri-bist-1D-2026-09-13.md"] }
  K4: { gecildi: 2026-09-13, kanit: ["docs/olcum/golden-zone-K4-katmanli-2026-09-17.md", "docs/olcum/golden-zone-r2-K4-katmanli-2026-09-17.md", "docs/olcum/golden-zone-K4-katmanli-2026-09-13.md", "docs/olcum/golden-zone-r2-K4-katmanli-2026-09-13.md"] }
  K5: { gecildi: null, kanit: [], onay: null }
  K6: { gecildi: null, kanit: [] }
---

# Golden Zone — Strateji Pasaportu

> ## ⏸ DURDURULDU — 2026-09-13
>
> **Karar:** Ürünleştirme durduruldu. Strateji **silinmedi**; kodu, testleri
> ve ölçümleri yerinde duruyor.
>
> **Gerekçe:** Kenar bulunamadı ve aranması gereken her yer arandı —
> 35 koşulluk tarama, çift eksende (zaman + sembol) bölme, ön kayıtlı
> kombinasyon testi, iki zaman dilimi, likidite/fiyat/sektör kırılımı,
> işlem maliyeti ve maliyet duyarlılığı. Özet:
> [`docs/olcum/GOLDEN-ZONE-OZET.md`](../olcum/GOLDEN-ZONE-OZET.md)
>
> **Neden silinmedi:** Dedektör çalışıyor, non-repaint testinden geçti ve
> sinyal başına zengin bir bağlam üretiyor. İleride **başka bir stratejinin
> ek koşulu** olarak değerlendirilebilir — "fiyat OTE bölgesinde mi" bir
> filtre olarak, tek başına bir kurulum olmaktan daha anlamlı olabilir.
>
> **K5 kapısı AÇIK kaldı:** komposer yazıldı, 11 iterasyonluk görsel kabul
> yapıldı, ama **kullanıcı onayı alınmadı** — onay istenmeden ölçüme geri
> dönüldü. Kapı onaysız kapatılmaz.
>
> **K6 hiç başlamadı.**
>
> **2026-09-17 · Ölçüm yenilendi, karar değişmedi.** Veri düzeltmesinden
> sonra K4 ön kayıt gereği bir kez yeniden koşuldu (evren 543 → 625 sembol).
> Fark altı ölçümün altısında da negatif kaldı; durdurma kararı yerinde
> duruyor.

> **Bu dosya stratejinin kimliğidir.** Kod, ölçüm ve görsel onay buraya
> bağlanır. Bir kapı geçilmeden sonraki açılmaz; yedisi geçilmeden **sıradaki
> stratejiye geçilmez** (README madde 4).
>
> Neden bu kadar katı: önceki projede K5 (görsel kabul) **hiç yapılmadı** —
> 115 test dosyasının hepsi veri yapısı testiydi, kimse çıktının resmine bakıp
> referansla karşılaştırmadı. K4 (istatistik) ise en sona bırakıldı ve 27
> gösterge kodlandıktan **sonra** hiçbirinin kenar kanıtlamadığı anlaşıldı.

---

## Bir bakışta

| | |
|---|---|
| **Ne yapar** | Likidite süpürmesi ve yapı kırılımından sonra fiyatın 0.62–0.79 düzeltme bölgesine dönüşünü arar. |
| **Zaman dilimleri** | 1G · 4S (K3 hangisinin makul aday ürettiğini söyleyecek) |
| **Yön** | İki yönlü |
| **Referans görsel** | `references/G8es0m9W4AAiTAK.png` — **anlamak için**, kopyalamak için değil |
| **Verdikt** | **kanıtlanmadı** — 543 sembol, 8432 işlem (1G) + 1499 (1H), kenar bulunamadı |
| **Durum** | ⏸ durduruldu (2026-09-13) — kod duruyor, ürünleştirme yok |

---

## K0 · Kaynak

> **Bitti kriteri:** kuralın geldiği kitap/makale, **sayfa numarasıyla**; tüm
> eşikler alıntılanmış. **Ezberden sayı yazmak yasak.**
>
> ADR-002: K0 bir formalite değil, **stratejinin doğduğu yer**. Eski koda
> bakılabilir ama referans olarak değil, yalnızca karşılaştırma için — ve
> farklılık çıkarsa **kitap kazanır**.

**Tam kaynak dosyası: [`kaynak/golden-zone-K0.md`](kaynak/golden-zone-K0.md)**

### Birincil kaynak

Golden Zone / OTE bir **uygulayıcı geleneğidir**, akademik makale değil. K0 bu
yüzden iki ayaklı: mekanik kural ICT literatüründen, **ölçüm yöntemi ve neye ne
zaman inanılacağı kitaptan**. Eşikleri meşrulaştıran ayak ikincisidir.

| | |
|---|---|
| Eser (yöntem) | López de Prado, *Advances in Financial Machine Learning* (2018) |
| Yer | s.45 (üç bariyer), s.50–53 (meta-etiketleme) |
| Dosya | `Quant Playbook/books/Group 1…/MD formatı/Advances In Financial Machine Learning.md` |
| Eser (örneklem) | Pardo, *The Evaluation and Optimization of Trading Strategies* (2008) |
| Yer | s.291–293 (serbestlik derecesi), s.295 (asgari işlem sayısı) |
| Dosya | `Quant Playbook/books/Group 4…/MD formatı/The Evaluation And Optimization Of Trading Strategies.md` |
| Eser (mekanik kural) | ICT/SMC uygulayıcı literatürü — ictkillzone.com/ict-ote, innercircletrader.net, forexbee.co |
| Yer | erişim 2026-09-13; bağlantılar kaynak dosyasında |

### Kuralın kendi cümleleriyle alıntısı

Mekanik kural — çıpanın nereye konacağı:

> "anchor must be the sweep wick extreme — not a candle body, not an arbitrary
> preceding swing"

Yöntem — nasıl etiketlenecek:

> "I call it the triple-barrier method because it labels an observation
> according to the first barrier touched out of three barriers." (LdP s.45)

Katmanlamanın kitaptaki adı ve reçetesi:

> "First, we build a model that achieves high recall, even if the precision is
> not particularly high. Second, we correct for the low precision by applying
> meta-labeling to the positives predicted by the primary model." (LdP s.51–53)

Ne zaman sayıya inanılır:

> "Thirty to 50 trades is an adequate minimum." (Pardo s.295)

### Eşikler

Her satırın **kaynağı** dolu olmalı. İki geçerli kaynak türü var:
kitaptan **alıntı** (sayfa numarasıyla) ya da **K3 ölçümü** (o zaman K3'ün
ölçüm dosyası gösterilir). Üçüncü bir tür yok.

**Kullanıcı kararı (2026-09-13): "Eşiklerin tamamı K3 ölçümünden türetilsin."**
ICT'nin sayıları aramanın başlangıç noktasıdır, gerekçesi değil.

> **K0, K3 ölçüldükten SONRA kapandı** — planlandığı gibi. Karar "eşiklerin
> tamamı K3'ten türetilsin"di; K1/K2 açıkça geçici varsayılanlarla kodlandı,
> K3 koşuldu, K0 kapandı.
>
> **Ama türetme gerçekleşmedi ve bu tabloda öyle duruyor.** Türetme, ölçümün
> bir yön göstermesini gerektirir — göstermedi (bkz. K4). Kenarın olmadığı
> yerde eşik "optimize etmek" gürültüye eğri uydurmak olurdu (Pardo
> s.291–293). Eşikler kaynaktaki hâliyle kaldı ve sonuç **onlarla**
> raporlandı; her satırın `K3:` dosyası bu kararı ayrıca yazıyor.

| Eşik | Değer | Kaynak |
|---|---|---|
| bolge_sig | 0.62 | `K3: docs/olcum/golden-zone-K3-A.md` |
| bolge_derin | 0.79 | `K3: docs/olcum/golden-zone-K3-A.md` |
| orta_esik | 0.705 | `K3: docs/olcum/golden-zone-K3-A.md` |
| yer_degistirme_atr | 1.5 | `K3: docs/olcum/golden-zone-K3-A.md` |
| supurme (bayrak) | — | `K3: docs/olcum/golden-zone-K3-A.md` |
| fvg_min_atr | 0.1 | `K3: docs/olcum/golden-zone-K3-B.md` |
| donus_max_bar | 20 | `K3: docs/olcum/golden-zone-K3-A.md` |
| stop_tamponu | 0 (wick ucu) | `K3: docs/olcum/golden-zone-K3-A.md` |
| zaman_bariyeri | 40 | `K3: docs/olcum/golden-zone-K3-A.md` |

**`hedef` bir eşik değildir**, kurulumun tanımıdır: ICT'de hedef yer
değiştirmenin ucudur (%0 seviyesi — iç aralık likiditesi). Ayarlanabilir bir
sayı olmadığı için eşik tablosunda yeri yok; kuralı `kaynak/golden-zone-K0.md`
§1.1'de.

### Kitaptan sapmalar

| Sapma | Gerekçe |
|---|---|
| Kill zone (seans) filtresi yok | ICT'nin seans penceresi FX intraday'e özgü; biz BIST/NASDAQ 1G-4S tarıyoruz. Eklenirse ayrı bir katman olarak ÖLÇÜLÜR, sessizce varsayılmaz. |
| "Daily bias" adımı yok | Öznel, kodlanabilir kural değil. Yerine BOS yönü — ölçülebilir ve non-repaint. |
| Kademeli kâr alma yok | Tek stop, tek hedef. Kademeli çıkış R dağılımını iyimser gösterir. |
| Aynı barda stop+hedef → stop | Bar içi sıralama bilinmiyor; belirsizlikte stratejinin lehine varsaymıyoruz. |

### Katmanlı ölçüm planı (kullanıcı kararı: "Golden Zone, katmanlı ölçümle")

Soru katman başına "kenar var mı" değil, **"kenar EKLİYOR mu"**.

| Katman | İçerik | LdP karşılığı |
|---|---|---|
| A | BOS + OTE bölgesi | birincil model (yön) |
| B | A + (FVG veya Order Block) | ikincil model (precision filtresi) |
| C | B + likidite süpürmesi | ikinci precision filtresi |

Her katman hem ileri getiri hem **R-katsayısı** ile ölçülür; her satırda işlem
sayısı görünür (Pardo s.295 — 30'un altında sayı yazılır, verdikt üretilmez).

---

## K1 · Sözleşme

> **Bitti kriteri:** tipli sonuç dataclass'ı, parametreler (frozen), durum
> makinesi, non-repaint gerekçesi yazılı.

### Parametreler

`packages/teknik/quaxis/teknik/indicators/golden_zone/parametreler.py` —
`frozen dataclass`, sonuç kaydı `params_hash` taşır. Aynı veri + aynı
parametre = bit bit aynı sonuç.

**Varsayılanların hiçbiri henüz gerekçeli değil.** Hepsi K3'ten türetilecek;
tabloda "geçici" diyen her satır K3 raporu yazılınca kapanır.

| Alan | Tip | Varsayılan | Düz Türkçe açıklama |
|---|---|---|---|
| `bolge_sig` | float | 0.62 *(geçici)* | Bölgenin sığ ucu — düzeltmenin ilk geçerli temas seviyesi. Giriş burada olur. |
| `bolge_derin` | float | 0.79 *(geçici)* | Bölgenin derin ucu — son geçerli giriş. Daha derin düzeltme bölgeyi geçersiz kılmaz, sadece kurulum "derin" sayılır. |
| `orta_esik` | float | 0.705 *(geçici)* | ICT'nin "sweet spot"u. **Sinyal üretmez**, yalnızca payload'a yazılır ki K4 "derin girişler daha mı iyi" sorusunu ölçebilsin. |
| `pivot_sol` / `pivot_sag` | int | 3 / 3 | Salınım ucunun onaylanması için sağında/solunda gereken bar. Non-repaint'in temeli: bir uç sağındaki 3 bar kapanmadan BİLİNEMEZ. |
| `yer_degistirme_atr` | float | 1.5 *(geçici)* | Bacağın asgari boyu, ATR katı. Gürültüyü yapı kırılımı sanmayı engeller. |
| `atr_periyot` | int | 14 | Wilder ATR. TA'nın evrensel kısaltması; zaman dilimine göre ölçeklenmez. |
| `donus_max_bar` | int | 20 *(geçici)* | Kırılımdan sonra bölgeye dönüş için tanınan süre. Takvimsel olduğu için zaman dilimine göre ÖLÇEKLENİR. |
| `stop_tamponu` | float | 0.0 *(geçici)* | Stop'un %100 çıpasının ne kadar ötesine konacağı. ICT "beyond this level" diyor ama sayı vermiyor. |
| `fvg_min_atr` | float | 0.1 *(geçici)* | FVG sayılması için asgari boşluk, ATR katı. |
| `zaman_bariyeri` | int | 40 *(geçici)* | K4'ün üç bariyerli ölçümünde zaman bariyeri. Takvimsel — ölçeklenir. |

`__post_init__` üç şeyi reddeder: bölge sınırlarının ters ya da [0,1] dışı
olması, orta eşiknın bölgenin dışına düşmesi (ölçülemeyen bir sayı olurdu),
pivot kolunun 1'den küçük olması.

### Durum makinesi

Kurulum bir dataclass olarak canlı tutulur; `SignalState` yalnızca son
durumu taşır.

```
       yapı kırılımı (BOS)
              │
              ▼
        [KURULUM CANLI] ──── %100 ötesinde GÖVDE kapanışı ──▶ ölür
              │         └─── donus_max_bar aşıldı ──────────▶ ölür
              │
     fiyat 0.62 seviyesine dokundu
              │
              ▼
         SİNYAL (confirmed)
```

| Olay | Geçiş | Kod |
|---|---|---|
| Kapanış onaylı salınım ucunu aşar (ve önceki bar aşmamış — kırılım TAZE) | kurulum doğar | `_kirilim_var_mi` |
| Yeni tepe/dip | %0 çıpası büyür | `_capa0_guncelle` |
| %100 ötesinde **gövde** kapanışı | kurulum ölür | `_yasiyor` |
| `donus_max_bar` aşıldı | kurulum ölür | `_yasiyor` |
| Fiyat bölgenin sığ ucuna dokunur | **sinyal** | `_bolgeye_girdi_mi` |

Aynı yönde ikinci kurulum açılmaz: açılsaydı yükselen her bar ayrı bir
kurulum doğurur ve sinyaller çoğalırdı.

### Non-repaint gerekçesi

Üç çıpanın üçü de sinyal barından **kesinlikle önce** sabitlenir:

| Çıpa | Ne zaman kesinleşir |
|---|---|
| Salınım pivotları | sağındaki `pivot_sag` bar kapandığında — `_Pivot.onay_i` bunu taşır ve `_son_onayli` onaydan önce hiçbir pivotu vermez |
| %100 (bacağın dibi) | kırılım barında; tamamen geçmiş barlardan |
| %0 (bacağın zirvesi) | yalnızca BÜYÜR ve yalnızca `[köken, t]` barlarından hesaplanır; bar *t*'de yeniden hesaplandığında aynı değeri verir |

Bu yüzden `bar_time` (bacağın zirvesinin barı) ile `detected_at` (bölgeye
girilen bar) **farklıdır** ve fark kaydedilir. Bacağın "en iyi" ucunu
sonradan seçmek — ileriye bakıp daha yüksek bir tepe bulunca çıpayı oraya
kaydırmak — repaint'in ta kendisidir.

**Görsel primitifler de aynı kurala tabidir** ve bu bedavaya gelmedi:
walk-forward testi iki gerçek kusur yakaladı. `Level`'lar `start` taşımıyordu
(zamansız seviye "hep vardı" sayılıyordu); kutunun `t0`'ı bacağın
zirvesindeydi, oysa kutu sinyal barında doğuyor — geriye atılmış bir `t0`,
geçmişi kaydıran birine bölgeyi daha bilinemezken çizilmiş gösterirdi.

---

## K2 · Dedektör

> **Bitti kriteri:** kod + birim testler + **walk-forward repaint testi** +
> lookahead lint temiz.

| | |
|---|---|
| Kod | `packages/teknik/quaxis/teknik/indicators/golden_zone/dedektor.py` |
| Parametreler | `packages/teknik/quaxis/teknik/indicators/golden_zone/parametreler.py` |
| Katalog | `quaxis.teknik.indicators.katalog:KATALOG` |
| Testler | `packages/teknik/tests/test_golden_zone.py` — 12 test |
| Repaint testi | **`repaint_test`** (generic) — `test_repaint_yok`, 260 bar / 35 kesim noktası. İstisna yolu (`register_verified_elsewhere`) KULLANILMADI. |
| Lookahead lint | `ruff` temiz |

### Testlerin neyi kilitlediği

| Test | Kilitlediği kural |
|---|---|
| `test_repaint_yok` | Walk-forward eşitlik. Kırılırsa strateji K2'yi geçemez. |
| `test_govde_kapanisi_gecersiz_kilar_wick_kilmaz` | ICT'nin gövde/wick ayrımı. Wick'i de geçersiz saymak sinyal sayısını sessizce yarıya indirirdi. |
| `test_stop_ve_hedef_payloadda` | K4'ün R ölçümü bu iki anahtarı okur; yoksa strateji kendi iddiasını göremeyen bir ölçüme girer. |
| `test_katman_bayraklari_filtre_degil` | Süpürme/FVG/OB elemez, bayrak yazar — katmanlı ölçümün ön koşulu. |
| `test_giris_bolgenin_sig_ucunda` | Giriş 0.62'de; 0.705'e kaydırmak sinyalin yarısını düşürürdü. |
| `test_detected_at_bar_time_ile_ayni_degil` | İkisi aynı bar olsaydı imkânsız bir şey iddia ederdik. |

---

## K3 · Kalibrasyon

> **Bitti kriteri:** tam **648 sembollük** evrende aday sayısı ölçülmüş.
> Sıfıra yakınsa bozuk, on binlerse çok gevşek. Ölçüm dosyası `docs/olcum/`
> altında.

| | |
|---|---|
| Ölçüm dosyaları | [`golden-zone-K3-A.md`](../olcum/golden-zone-K3-A.md) · [`-B`](../olcum/golden-zone-K3-B.md) · [`-C`](../olcum/golden-zone-K3-C.md) |
| Veri kalitesi | [`veri-bist-1D-2026-09-13.md`](../olcum/veri-bist-1D-2026-09-13.md) — 648 listeden **543 sembol** ölçüldü |
| Aday sayısı (A) | sembol başına ortalama **19.2** · toplam 10 417 |
| Aday sayısı (B) | 13.7 · (FVG/OB koşulu %29 eliyor) |
| Aday sayısı (C) | 2.4 · (süpürme koşulu sert eliyor) |
| Aday üretmeyen sembol | A: %2 · B: %2 · C: %13 |
| Teşhis | **MAKUL** (üç katmanda da) — eşik ne evreni boğuyor ne susturuyor |
| Sonuç | **Hiçbir eşik değiştirilmedi.** Ölçüm bir yön göstermediği için türetme yapılamadı; kenarın olmadığı yerde eşik optimize etmek gürültüye eğri uydurmak olurdu (Pardo s.291–293). |

> Önceki projede `breakout_fvg` ve `flag_pennant` 4S'te **648/648 sembolde
> sıfır aday** veriyordu ve bu ancak çok sonra fark edildi. K3 bunun içindir.

---

## K4 · İstatistik

> **Bitti kriteri:** **sembol-kümelenmiş** ileri getiri testi, IS/OOS ayrımı,
> permütasyon + BH-FDR. Sonuç dürüstçe yazılır: *kenar var / yok / belirsiz*.
> **Elenmez — etiketlenir.**

> **Yenilendi 2026-09-17.** Ölçüm zemininde gerçek veri kusurları bulundu
> ([`veri-denetimi-bist-1D.md`](../olcum/veri-denetimi-bist-1D.md)),
> ön kayıtla düzeltildi ([`onkayit-veri-duzeltme.md`](../olcum/onkayit-veri-duzeltme.md))
> ve K4 **bir kez** yeniden koşuldu. Evren 543 → 625 sembole çıktı.
> **Verdikt değişmedi.** Aşağıdaki tablo yenilenmiş ölçümündür; 13 Eylül
> tablosu dosyasında duruyor.

| | |
|---|---|
| Ölçüm dosyaları | [`golden-zone-K4-katmanli`](../olcum/golden-zone-K4-katmanli-2026-09-17.md) (yapısal hedef) · [`golden-zone-r2-K4-katmanli`](../olcum/golden-zone-r2-K4-katmanli-2026-09-17.md) (sabit 2R) |
| Evren | 625 BIST sembolü, 1G (liste 648; 23'ünde sağlayıcı veri yok) |
| Bağımsız gözlem | **599 sembol** (A katmanı) — bar değil, SEMBOL |
| Pencere | ilk %70 IS / son %30 OOS (~4 yıl) |
| Ufuk | 20 bar (ileri getiri) · 40 bar (zaman bariyeri) |
| Adil baza karşı fark | **%−0.39** (A, ileri getiri) · **−0.029R** (A, R) — negatif |
| Permütasyon p değeri | 0.8851 (ileri getiri) · 0.9820 (R) |
| BH-FDR (q=0.05) | uygulanmadı — hiçbir ham p eşiğin yanından geçmedi (en düşüğü 0.2679) |
| **Verdikt** | **kanitlanmadi** |

### R-katsayısı (üç bariyer)

> **Strateji bir stop ve hedef bildiriyorsa bu tablo ZORUNLUDUR.** İleri getiri
> asimetriyi göremez: %35 isabetle 3R kazandıran bir sistem 20 barlık ileri
> getiride sıfır görünür. ICT/SMC kavramlarını "kenar yok" diye bulan en geniş
> çalışma (648 backtest) tam olarak bu hatayı yaptı — zaman bazlı çıkış kullandı,
> stop/hedef koymadı. Aynı barda iki bariyer de vurulduysa **stop** sayılır.

Katmanlı ölçüm — soru "kenar var mı" değil, **"kenar EKLİYOR mu"**:

| Katman | İşlem | Sembol | İsabet | Ort. R | Adil baz | ΔR | p |
|---|---|---|---|---|---|---|---|
| A · BOS + OTE | 9909 | 599 | %40.3 | **+0.016R** | +0.045R | — | 0.9820 |
| B · + FVG/OB | 7081 | 596 | %39.7 | −0.002R | +0.047R | −0.018R | 0.9975 |
| C · + süpürme | 1242 | 497 | %39.5 | −0.016R | +0.024R | −0.014R | 0.6062 |

Çıkış kırılımı (A): **%37 hedef · %57 stop · %6 zaman.**

Sabit 2R hedefle (`golden_zone_r2`) aynı tablo: A +0.032R (baz +0.055R,
p=0.9565). Sonuç değişmiyor.

#### 13 Eylül tablosuyla karşılaştırma — ham R sütunları karşılaştırılamaz

13 Eylül'ün tablosu **işlem maliyeti ölçüme girmeden önce** üretildi
(`2969fa1`); maliyet aynı gün, o rapordan sonra `b11de50` ile girdi. Ham
`Ort. R` yan yana konursa veri düzeltmesinin etkisiyle maliyetin etkisi
birbirine karışır. Karşılaştırılabilen büyüklük **fark**tır (strateji −
adil baz) ve fark maliyete neredeyse duyarsızdır
([maliyet duyarlılığı](../olcum/golden-zone-maliyet-duyarliligi-2026-09-13.md):
altı maliyet düzeyinde p sabit 0.0093).

| Katman | fark · 09-13 | fark · 09-17 |
|---|---|---|
| A | −0.026R | **−0.029R** |
| B | −0.053R | **−0.049R** |
| C | −0.047R | **−0.040R** |

Fark altı ölçümün (üç katman × iki hedef modu) altısında da negatif kaldı.

| | |
|---|---|
| **Verdikt (R)** | **kanitlanmadi** — üç katmanda da |

### Ne çıkarsa o

**Kenar bulunamadı, üstelik teyit katmanları değer EKSİLTTİ.** Düzeltilmiş
veri bunu değiştirmedi.

- Sinyaller, aynı risk yapısıyla rastgele barlardan girmekten daha iyi değil.
- FVG/Order Block katmanı işlemlerin %29'unu eledi; **elediği kısım kalandan
  daha kötü değildi.** Meta-etiketleme hipotezi (LdP s.51–53) doğrulanmadı.
- Örneklem mazeret değil: en dar katman bile 1242 işlem / 497 sembol.
- Ön kayıt §5'in birinci maddesi (*fark pozitif*) sağlanmadığı için ikinci
  ve üçüncü maddeye bakılmadı. "Yaklaştı" bir sonuç değildir.

**"Kenar yok" ≠ "zarar ettirir".** Yapısal hedefte A katmanının işlem başına
ortalama R'si maliyet dahil hâlâ pozitif (+0.016R); strateji para
kaybettirmiyor, **piyasanın kendi verdiğinin altında kalıyor**. Alt
katmanlarda (B −0.002R, C −0.016R) sıfırın altına iniyor.
Kurulumun geometrisi gerçekten lehte (0.62 girişte 1.63:1, 0.705'te 2.39:1)
ama isabet oranı tam o avantajı silecek kadar düşük: %37 hedef × ~1.7R eksi
%57 stop × 1R ≈ sıfır. **Asimetri gerçek, ama fiyatlanmış.**

**Bu "ICT işe yaramaz" demek değil.** Ölçtüğümüz, ICT'nin uyguladığı şey
değil: FX intraday yerine BIST günlük, kill zone filtresi yok, kademeli
çıkış yok. Sapmaların her biri K0'da gerekçeli. Çürütülen iddia şu:
**"OTE bölgesi, BIST günlükte tek başına swing kurulumu olarak kenar
üretir."**

---

## K5 · Görsel

> **Bitti kriteri:** komposer yazılır, gerçek veriyle ekran görüntüsü alınır,
> **referans görselle yan yana konur**, **en az 3 iterasyon**, **kullanıcı
> onayı**.

| | |
|---|---|
| Komposer | `packages/chart/quaxis/chart/komposer/golden_zone.py` |
| Girdi tipi | `quaxis.chart.tipler.OTESonucu` |
| Spec üreteci | `tools/golden_zone_spec.py` — **gerçek** THYAO verisi, fikstür değil |
| Yüzey | `apps/web/app/(uygulama)/grafik/page.tsx` |
| Referans | `references/G8es0m9W4AAiTAK.png` · `G8j_KYOX0AEb8l-.png` — **anlamak için**, kopyalamak için değil (kullanıcının kendi ifadesi) |
| İterasyonlar | **11** (asgari 3) — `docs/design/ui/gz-{koyu,acik,sistem}-{1440,768}-i11.png`, tam kayıt: [`ui/README.md`](../design/ui/README.md) |
| Onay | *(kullanıcı onayının tarihi — onay yoksa kapı KAPALI)* |

### İterasyon kaydı

Her turda **ne görüldü, ne düzeltildi**. "Düzeltildi" demek yetmez; neyin
nasıl göründüğü yazılır.

| Tur | Görülen kusur | Yapılan düzeltme |
|---|---|---|
| i1 | `süpürme` ve `%100` işaretleri TAM aynı noktada, etiketler üst üste binip okunmaz | Kök sebep dedektörde: payload süpürmenin kendi barını taşımıyordu. `supurme_bar`/`supurme_fiyat` eklendi; komposer çakışan çıpada süpürmeyi çizmiyor |
| i1 | "BOS" çizgisi kırılan salınım seviyesi yerine **kırılım barının kapanışını** gösteriyordu — etiket doğru, sayı yanlış | `kirilan_seviye` payload'a eklendi |
| i2 | Bant bacağın ucundan, seviyeler bacağın başından başlıyordu | İkisi de bacak TAMAMLANINCA doğar; `capa0.onay_t`'de birleştirildi |
| i2 | Sonuçlanmış kurulumun bölgesi levhanın sonuna kadar uzuyordu | `Bant`/`Seviye`'ye `bitis` eklendi; çıkış `barrier_outcome` ile (K4'ün AYNI mantığı) hesaplanıyor. Seviyeler bitişten sonra %22 opaklıkla hayalet devam eder — tamamen kesilse sağ oluktaki etiket sahipsiz kalırdı |
| i3 | Çıkış işareti **hiç görünmüyordu**: `hap: false` rollerde çizici metni sessizce düşürüyordu | Hapsız roller de yazıyor, zemini `zeminEkle` ile |
| i3 | Bant etiketi giriş rozetiyle çakışıyordu | "OTE 0.62–0.79" zaten HUD'da ve sağ olukta yazıyor; bant etiketsiz bırakıldı |
| i3 | Çıkış aksan renginde — "hedefe ulaştı" ile "stop oldu" aynı renkte | Sonuç YÖN bilgisidir: `CIKIS_KAZANC`/`CIKIS_KAYIP` rolleri (`--up`/`--down`) |
| i4–i7 | **Mum tuvali SVG katmanının ÜSTÜNDEYDİ.** Faz 4'ten beri vardı, görünmüyordu: o güne kadar çizilen her şey mumların olmadığı boşluklara düşüyordu. "stop ✕ 288.75" mum gövdesiyle kesildi | Lightweight Charts tuvallerine `z-index: 1`/`2` veriyor, sarmal yığınlama bağlamı kurmuyordu. `isolation: isolate` + açık `z-index` katmanları. Teşhis göz kararıyla değil: overlay DOM'u playwright ile gerçek viewport'ta okundu |
| i4 | `getBBox()` 0 dönünce metin zemini sessizce çizilmiyordu | Monospace ölçü kestirimi yedek yol olarak eklendi |
| i7 | HUD metni 0.0 seviyesinin çizgisiyle kesişiyordu | Satır arkasına levhanın zemini (gölge değil, dolgu) |
| i8 | Zemin `inline-block` verilince iki HUD satırı yan yana gelip 768'de sağ oluğa taştı | `display: block; width: fit-content` |
| i10 | 768'de "hedef" ile sayısı ayrı satıra düşüp sayı sahipsiz kalıyordu | `white-space: nowrap` ile bölünmez |

### Referanstan bilinçli sapmalar

| Sapma | Gerekçe |
|---|---|
| Referans görsellerin düzeni taklit edilmedi | İkisi de **anlamak için** verilmişti, kopyalamak için değil. Komposer K0'daki mekanik kuralı çiziyor. |
| Çok zaman dilimli paneller ve el yazısı notlar üretilmedi | Referanslar eğitim amaçlı ekran görüntüleri; ürün yüzeyi değil. |
| Merdivenin tamamı çizilmiyor | Bandın kenarları zaten 0.62 ve 0.79; ayrıca çizgi koymak dar bandın içinde üç çizgi = okunmaz yığın demekti. Çizilen: giriş, orta eşik, stop, hedef. |

### Grafiğin taşıdığı verdikt

Künye `verdikt: kanıtlanmadı` taşıyor ve yüzey bunu **hem çubukta hem
altındaki K4 kutusunda** gösteriyor. "Bu kurulum oluştu" ile "bu stratejinin
kenar ürettiği kanıtlandı" ayrı şeylerdir; ikincisi gösterilmezse birincisi
ikincisi sanılır.

Örnek kurulum **stop'la bitiyor** ve grafik bunu saklamıyor. Sinyali gösterip
sonucunu göstermemek, grafiği reklam yapardı.

---

## K6 · Ürün

> **Bitti kriteri:** tarama tablosunda satır + grafik sayfasında sekme +
> "Nasıl Okunur" metni + alarm kuralı.

| | |
|---|---|
| Kütüphane kartı | *(hangi dosyada)* |
| Strateji sayfası | `/stratejiler/<slug>` |
| Tarama kolonu | *(tarihsel isabet rozeti hangi verdikti gösteriyor)* |
| Alarm kuralı | *(sinyal ne zaman bildirilir)* |

### Nasıl okunur — dört soru

Grafik levhasının altında duran dört not. Düz Türkçe, jargon yok.

| Soru | Cevap |
|---|---|
| Nereye bak | |
| Ne ölçer | |
| Sinyal ne zaman doğar | |
| Değerler ne demek | |

### Sık sorulanlar

*(En az bir soru: "sinyal sonradan kaybolur mu?" — cevabı non-repaint
gerekçesine bağlanır.)*
