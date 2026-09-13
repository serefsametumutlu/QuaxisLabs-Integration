---
# ── Makine tarafından okunan künye ────────────────────────────────────────
# `python tools/pasaport.py dogrula` bu bloğu denetler. Elle "geçti" yazmak
# yetmez: her kapının kanıtı DİSKTE bulunmak zorundadır.
slug: golden-zone            # dosya adıyla aynı, küçük harf, tireli
ad: Golden Zone              # kullanıcıya görünen ad
paket: yapi                     # yapi | formasyon | trend | arbitraj
referans: "references/G8es0m9W4AAiTAK.png"   # ANLAMAK için, kopyalamak için değil

# K4'ün çıktısı. Kapı AÇILMADAN "ölçülmedi" dışında bir değer yazılamaz.
#   olculmedi     — K4 açılmadı, elimizde sayı yok
#   kanitlanmadi  — ölçüldü, FDR sonrası kenar bulunamadı
#   izlenen-aday  — ölçüldü, en az çürütülmüş grupta
#   kenar-var     — ölçüldü, FDR eşiğini geçti
verdikt: kanitlanmadi

kapilar:
  K0: { gecildi: 2026-09-13, kanit: ["docs/strateji/kaynak/golden-zone-K0.md", "docs/olcum/golden-zone-K3-A.md"] }
  K1: { gecildi: 2026-09-13, kanit: ["packages/teknik/quaxis/teknik/indicators/golden_zone/parametreler.py"] }
  K2: { gecildi: 2026-09-13, kanit: ["packages/teknik/quaxis/teknik/indicators/golden_zone/dedektor.py", "packages/teknik/tests/test_golden_zone.py"] }
  K3: { gecildi: 2026-09-13, kanit: ["docs/olcum/golden-zone-K3-A.md", "docs/olcum/golden-zone-K3-B.md", "docs/olcum/golden-zone-K3-C.md", "docs/olcum/veri-bist-1D-2026-09-13.md"] }
  K4: { gecildi: 2026-09-13, kanit: ["docs/olcum/golden-zone-K4-katmanli-2026-09-13.md", "docs/olcum/golden-zone-r2-K4-katmanli-2026-09-13.md"] }
  K5: { gecildi: null, kanit: [], onay: null }
  K6: { gecildi: null, kanit: [] }
---

# Golden Zone — Strateji Pasaportu

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
| **Verdikt** | **kanıtlanmadı** — 543 sembol, 8432 işlem, kenar bulunamadı |

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
| sweet_spot | 0.705 | `K3: docs/olcum/golden-zone-K3-A.md` |
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
| `tatli_nokta` | float | 0.705 *(geçici)* | ICT'nin "sweet spot"u. **Sinyal üretmez**, yalnızca payload'a yazılır ki K4 "derin girişler daha mı iyi" sorusunu ölçebilsin. |
| `pivot_sol` / `pivot_sag` | int | 3 / 3 | Salınım ucunun onaylanması için sağında/solunda gereken bar. Non-repaint'in temeli: bir uç sağındaki 3 bar kapanmadan BİLİNEMEZ. |
| `yer_degistirme_atr` | float | 1.5 *(geçici)* | Bacağın asgari boyu, ATR katı. Gürültüyü yapı kırılımı sanmayı engeller. |
| `atr_periyot` | int | 14 | Wilder ATR. TA'nın evrensel kısaltması; zaman dilimine göre ölçeklenmez. |
| `donus_max_bar` | int | 20 *(geçici)* | Kırılımdan sonra bölgeye dönüş için tanınan süre. Takvimsel olduğu için zaman dilimine göre ÖLÇEKLENİR. |
| `stop_tamponu` | float | 0.0 *(geçici)* | Stop'un %100 çıpasının ne kadar ötesine konacağı. ICT "beyond this level" diyor ama sayı vermiyor. |
| `fvg_min_atr` | float | 0.1 *(geçici)* | FVG sayılması için asgari boşluk, ATR katı. |
| `zaman_bariyeri` | int | 40 *(geçici)* | K4'ün üç bariyerli ölçümünde zaman bariyeri. Takvimsel — ölçeklenir. |

`__post_init__` üç şeyi reddeder: bölge sınırlarının ters ya da [0,1] dışı
olması, tatlı noktanın bölgenin dışına düşmesi (ölçülemeyen bir sayı olurdu),
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

| | |
|---|---|
| Ölçüm dosyaları | [`golden-zone-K4-katmanli`](../olcum/golden-zone-K4-katmanli-2026-09-13.md) (yapısal hedef) · [`golden-zone-r2-K4-katmanli`](../olcum/golden-zone-r2-K4-katmanli-2026-09-13.md) (sabit 2R) |
| Evren | 543 BIST sembolü, 1G |
| Bağımsız gözlem | **518 sembol** (A katmanı) — bar değil, SEMBOL |
| Pencere | ilk %70 IS / son %30 OOS (~4 yıl) |
| Ufuk | 20 bar (ileri getiri) · 40 bar (zaman bariyeri) |
| Adil baza karşı fark | **%−0.34** (A) — negatif |
| Permütasyon p değeri | 0.7981 (ileri getiri) · 0.9530 (R) |
| BH-FDR (q=0.05) | uygulanmadı — aile tek strateji; hiçbir ham p eşiğin yanından geçmedi |
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
| A · BOS + OTE | 8432 | 518 | %40.5 | **+0.045R** | +0.071R | — | 0.9530 |
| B · + FVG/OB | 6004 | 515 | %39.7 | +0.020R | +0.073R | −0.025R | 0.9960 |
| C · + süpürme | 1056 | 424 | %39.2 | +0.001R | +0.048R | −0.019R | 0.6442 |

Çıkış kırılımı (A): **%37 hedef · %57 stop · %6 zaman.**

Sabit 2R hedefle (`golden_zone_r2`) aynı tablo: A +0.058R (baz +0.080R,
p=0.9270). Sonuç değişmiyor.

| | |
|---|---|
| **Verdikt (R)** | **kanitlanmadi** — üç katmanda da |

### Ne çıkarsa o

**Kenar bulunamadı, üstelik teyit katmanları değer EKSİLTTİ.**

- Sinyaller, aynı risk yapısıyla rastgele barlardan girmekten daha iyi değil.
- FVG/Order Block katmanı işlemlerin %29'unu eledi; **elediği kısım kalandan
  daha kötü değildi.** Meta-etiketleme hipotezi (LdP s.51–53) doğrulanmadı.
- Örneklem mazeret değil: en dar katman bile 1056 işlem / 424 sembol.

**"Kenar yok" ≠ "zarar ettirir".** İşlem başına ortalama R pozitif (+0.045R);
strateji para kaybettirmiyor, **piyasanın kendi verdiğinin altında kalıyor**.
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
| Komposer | `packages/chart/quaxis/chart/komposer/<slug>.py` |
| Referans | *(`references/…png`)* |
| İterasyonlar | *(`docs/design/ui/<slug>-*.png` — en az 3)* |
| Onay | *(kullanıcı onayının tarihi — onay yoksa kapı KAPALI)* |

### İterasyon kaydı

Her turda **ne görüldü, ne düzeltildi**. "Düzeltildi" demek yetmez; neyin
nasıl göründüğü yazılır.

| Tur | Görülen kusur | Yapılan düzeltme |
|---|---|---|
| i1 | | |
| i2 | | |
| i3 | | |

### Referanstan bilinçli sapmalar

*(Referansta olup üretmediğimiz ya da farklı yaptığımız her şey —
gerekçesiyle. Yoksa "yok" yaz.)*

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
