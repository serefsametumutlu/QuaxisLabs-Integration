# QuaxisLabs — Yeniden İnşa Raporu ve Yol Haritası

**Tarih:** 2026-09-12
**Kapsam:** Mevcut üç kod tabanının (teknik / temel / Quaxis mobil), kitap
kaynaklarının ve tüm proje belgelerinin incelenmesi; yeni klasörde sıfırdan
ayağa kaldırma planı.
**Durum:** Karar bekliyor — Bölüm 11'deki 4 soru cevaplanmadan kod yazılmayacak.

---

## 1. Ne buldum — dürüst envanter

Üç ayrı yerde, birbirinden habersiz üç proje var. Hiçbiri çöp değil; ama
hiçbiri de "ürün" değil.

### 1.1 Teknik analiz — `Desktop\Teknik Analiz\` (paket adı `tlab`)

Beklediğimden **çok daha olgun**. Sayılarla:

| Katman | Satır | Durum |
|---|---:|---|
| `tlab/core` (Signal, IndicatorResult, Registry) | 843 | sağlam |
| `tlab/data` (sağlayıcı, önbellek, takvim, resample) | 799 | sağlam |
| `tlab/features` (swing, fib, trendline, zone, hacim profili, likidite) | 2 849 | sağlam |
| `tlab/indicators` (27 gösterge) | 8 824 | çalışıyor, kalibrasyonu şüpheli |
| `tlab/scanner` (evren × tf × gösterge tarama, EOD, SQLite) | 1 579 | çalışıyor |
| `tlab/testing` (repaint testi, lookahead lint) | 555 | **projenin en değerli parçası** |
| `tlab/viz` (ESKİ jenerik çizici) | 10 475 | **ölü — atılacak** |
| `tlab/chart` (YENİ tipli komposerler, 23 dosya) | ~3 000 | yarı yolda |
| `web/` (Next.js 16 + FastAPI, 2 sayfa) | ~2 900 | iskelet |
| `tests/` | 14 552 | **1008 test yeşil** |

**Kayda değer varlıklar:**
- **Non-repaint sözleşmesi** — `signal(t)` yalnızca `t` ve öncesiyle hesaplanır
  ve sonradan değişmez. Üç mekanizmayla korunuyor: `detected_at` vs `bar_time`
  ayrımı, walk-forward eşitlik testi (registry'ye kayıt şartı), statik lookahead
  lint'i. Bu, piyasadaki çoğu "tarayıcı"nın sahip olmadığı şey ve **yeniden
  yazılması haftalar sürer**.
- **648 sembollük gerçek BIST evreni** + 121 MB yerel OHLCV önbelleği (4H + 1D).
- 27 gösterge: `patterns.*` (7), `structure.*` (4), `trend.*` (4),
  `momentum.*` (2), `pair.*` (2), `harmonic.*` (8 ekol).
- Her fazın kararları ve bulunan gerçek hatalar `CLAUDE.md` + `PROGRESS_LOG.md`
  içinde (333 KB) kayıtlı.

### 1.2 Temel analiz — `Desktop\Temel Analiz\bilanco-radar\`

- Python + SQLAlchemy/SQLite, Telegram botu, Jinja2+Playwright kart üretimi.
  LLM **yalnızca yorum metni** yazıyor, sayı üretmiyor — doğru karar.
- Kitap çıkarımı: 6 kitabın **3'ü** tamamlandı (Graham, Buffett, Damodaran) →
  **682 İLKE, 249 FORMÜL, 164 KIRMIZI BAYRAK**, kesintisiz numaralandırılmış
  ve script ile doğrulanmış. Fisher/Lynch/Schilit ertelendi.
- 4 mercek (Değer/Kalite/Büyüme/Güvenlik) + bileşik skor spec'i **taslak**.
- Evren: BIST 643 şirket (tam), NASDAQ 4352 keşfedilmiş / 1442 zenginleştirilmiş.
- **En büyük yapısal açık:** 10+ yıllık kazanç/temettü serisi yok (`trends.py`
  12 çeyrekle sınırlı). Graham'ın 7 kriterinin 3'ü bu yüzden hesaplanamıyor —
  kitap çıkarımlarında **5 kez** tekrarlandı.

### 1.3 Quaxis mobil — `Desktop\Quaxis\`

Ayrı bir ürün: Flutter + FastAPI + Postgres/TimescaleDB portföy takip
uygulaması (BIST + TEFAS + döviz/altın). **Bu projeyle karıştırılmamalı**, ama
"ileride app'a dönüştürmek" hedefi için hazır bir mobil iskelet ve
`design_handoff_quaxis_ui_v2/` altında iki HTML prototipi var — ileride
yeniden kullanılabilir.

### 1.4 Kaynaklar

- `Quant Playbook\books\` — 17 kaynak, 4 grup (ML/algoritmik çerçeveler,
  kantitatif temeller & zaman serisi, mikroyapı & HFT, backtest/optimizasyon/
  risk). Çoğu `.md`'ye çevrilmiş (Chan, Jansen, Kestner, Kissell, Carr,
  Rachev…).
- `bilanco-radar\bilgi-bankasi\teknik\` — Pesavento (`10_`), Carver (`11_`)
  çıkarımları + `kod/` altında 11 bölümlük uygulanabilirlik matrisi
  (trend, pairs, arbitraj, HFT, ML, oynaklık, opsiyon, makro, portföy,
  performans).
- Referans görseller: `Teknik Analiz\önemli\` (11 PNG), `images\` (10 PNG),
  `ornek1/ornek2/yeni strateji/TOBO.png`. Bunlar hedeflenen görsel dilin
  tanımı.

---

## 2. En kritik bulgu — bunu önce konuşmalıyız

Bu raporun en önemli cümlesi:

> **27 göstergenin hiçbiri şu anda istatistiksel olarak kanıtlanmış bir
> piyasa kenarına (edge) sahip değil.**

Bu benim tahminim değil; senin kendi projenin **iki tur ölçümünün** sonucu
(`docs/KALAN_ISLER.md` madde 1.7 ve 1.8):

- **1. tur (2026-09-11):** 586 sembol, 23 gösterge, IS/OOS ayrımı, 3000
  tekrarlı permütasyon, Benjamini-Hochberg FDR. 3 gösterge "anlamlı" çıktı
  (`broadening` +%30, `wedge` +%79, `five_zero` +%68) — **üçü de sahte.**
  `wedge`'in 10 "sinyali" aslında 2 hisse; `broadening`'in 57'si 10 hisse;
  ANELE tek başına aynı +%232'lik hareketi 5 kez tekrarlıyor.
- **2. tur (2026-09-12, sembol-düzeyi kümeleme):** bir sembolün tüm sinyalleri
  **tek gözlem** sayılınca ilk turun "en güvenilir" ikilisi de çöktü:
  `trend.breakouts` p=0.027 → **0.721**; `trend.weekly_channel` p=0.016 →
  **0.181** ve işaret **ters döndü** (+%0.57 → −%0.92).

En az çürütülmüş üç aday: `trend.ewmac` (n=559 sembol, +%1.59, p=0.034),
`structure.golden_zone`, `trend.ma_systems` — ama hiçbiri FDR eşiğini geçmiyor.
Ayrıca `trend.breakouts`'un kalite skoru ile 20-bar getiri arasında
Spearman ρ=**0.0008** (p=0.90) — yani "en yüksek skorlu kırılımı seç" kuralı
rastgele seçmekten ölçülebilir şekilde daha iyi değil.

**Bunun anlamı ve benim önerim.** "Sinyaller hatasız kodlanmalı" dediğinde iki
ayrı şeyden bahsediyorsun: (a) kod doğru çalışsın, (b) sinyal işe yarasın.
(a) büyük ölçüde tamam. (b) **şu an hayır**, ve bu bir kodlama hatası değil —
kitaplardaki kuralların BIST'te bu parametrelerle çalışmaması. Güzel bir site
kurup bu sinyalleri listelemek, çalışmayan bir motoru cilalı bir kaportaya
koymak olur.

Bu yüzden aşağıdaki planda **her strateji için istatistiksel kapı zorunlu** —
ama sonucu "bu strateji elenecek" demek değil; sonucu **dürüstçe göstermek**.
Sitede her stratejinin yanında "tarihsel isabet: ölçüldü / ölçülmedi /
kanıtlanmadı" rozeti olacak. Bu, rakiplerin yapmadığı ve senin
`SITE_TASARIM_YOL_HARITASI.md`'de zaten "en güçlü kozumuz" dediğin şey.

---

## 3. Asıl karar: "sıfırdan klasör" evet, "sıfırdan kod" hayır

Senin isteğin haklı ve ben de **yeni klasörü destekliyorum** — ama sebebi
"kod berbat" değil, ve bu ayrım planın tamamını belirliyor.

### Neden yeni klasör DOĞRU

1. **Git durumu bozuk.** Şu anki git deposunun kökü `C:\Users\Samet` — yani
   tüm ev dizinin. `.git` 4 GB (geçmişte kitap PDF'leri commit edilmiş).
   GitHub'daki gerçek `QuaxisLabs` deposuyla **ilişkisiz bir commit
   geçmişi** var; push etmek için her seferinde `git worktree` + `git archive`
   içeren 5 adımlık bir el hilesi gerekiyor. Bu tek başına yeni depo açmak
   için yeterli sebep.
2. **İki proje iki ayrı yerde.** Teknik ve temel analiz birleşecekse tek
   depoda olmalılar; şu an biri `Teknik Analiz\`, diğeri
   `Temel Analiz\bilanco-radar\`, ortak hiçbir şey paylaşmıyorlar.
3. **Psikolojik temizlik gerçek bir kazanç.** 333 KB'lık bir PROGRESS_LOG ve
   14 farklı yol haritası belgesi arasında hangisinin geçerli olduğunu
   bulmak bile iş. Yeni depo tek bir geçerli belge setiyle başlar.

### Neden "sıfırdan kod" YANLIŞ olur

Motoru atarsan şunları yeniden yazman gerekir ve her biri haftalar sürer:

- Non-repaint walk-forward test altyapısı + lookahead lint'i.
- Pivot onay/kesinleşme zinciri (`detected_at` ≠ `bar_time` ayrımı).
- `pattern_id` kimliği — bu hata **1 milyondan fazla sahte "kaybolan sinyal"**
  üretiyordu; kök nedeni (konumsal `bar_idx` kullanımı) bulunup 10 dosyada
  düzeltildi.
- Zaman dilimi ölçekleme tuzağı — `breakout_fvg` ve `flag_pennant` 4H'te
  **648 sembolün 648'inde sıfır aday** veriyordu; oran parametreleri
  ölçeklenmediği için eşik matematiksel olarak ulaşılamazdı. Ölçülüp
  düzeltildi (0 → 913 aday).
- Harmonik geometri (8 ekol), Bulkowski/Lo-Mamaysky-Wang formasyon ölçütleri,
  eşbütünleşme testleri, Corwin-Schultz spread.
- 1008 test.

Bunların hiçbiri "eski kod" değil — **öğrenilmiş ders**. Sıfırdan yazarsan
aynı hataları aynı sırayla tekrar yaparsın.

### Karar önerim

> **Yeni depo `Desktop\QuaxisLabs\` — evet.**
> İçine **motor taşınır** (`core`, `data`, `features`, `indicators`,
> `scanner`, `testing` + testleri), **`tlab/viz` hiç gelmez** (10 475 satır
> silinir), **`tlab/chart` yeni sözleşmeyle yeniden yazılır**, **web sıfırdan
> tasarlanır**, **temel analiz motoru 2. aşamada taşınır**.
>
> Taşıma bir "kopyala-yapıştır" değil: her modül yeni depoya girerken
> testleri yeşil olmak zorunda, ve `tlab` adı `quaxis.teknik` olur.

---

## 4. Hedef mimari

```
QuaxisLabs/
├─ apps/
│  ├─ web/                  # Next.js 16 + React 19 + TS + Tailwind 4
│  └─ mobile/               # (Faz 9) Flutter — Quaxis iskeletinden
├─ services/
│  └─ api/                  # FastAPI — teknik + temel TEK kapı
├─ packages/
│  ├─ teknik/               # tlab motoru (taşınır)
│  │   ├─ core/ data/ features/ indicators/ scanner/ testing/
│  ├─ temel/                # bilanco-radar motoru (Faz 8'de taşınır)
│  ├─ chart/                # ChartSpec üreticileri (komposerler)
│  └─ ortak/                # semboller, takvim, tipler, TR etiketler
├─ docs/
│  ├─ strateji/             # HER strateji için 1 pasaport dosyası
│  ├─ design/               # tasarım şartnamesi + referans görseller
│  ├─ karar/                # ADR (mimari karar kayıtları)
│  └─ olcum/                # istatistiksel doğrulama raporları
├─ references/              # mobbin şemaları, ekran görüntüleri
├─ tools/                   # görsel kabul döngüsü, snapshot, karşılaştırma
└─ .claude/
   ├─ agents/               # 6 özel agent (Bölüm 8)
   └─ skills/               # mimari + tasarım sistemi skill'leri
```

### 4.1 Tek en önemli sözleşme: `ChartSpec`

Eski sistemin çöküş noktası şuydu: **tek jenerik çizici, 24 strateji.** Her
gösterge `Line`/`Box`/`Marker` torbası üretiyordu, 3 055 satırlık tek bir
renderer hepsini aynı biçimde basıyordu. Referans görsellerin hiçbiri jenerik
bir çizicinin çıktısı değil — her biri o stratejiye **özel bestelenmiş**.

Yeni sözleşme:

```
gösterge → TİPLİ sonuç (ör. XabcdPattern) → o tipe ait KOMPOSER → ChartSpec (JSON)
                                                                      ├→ web renderer (etkileşimli)
                                                                      └→ PNG renderer (rapor/Telegram)
```

`ChartSpec` **çizim kütüphanesinden bağımsız**, versiyonlu bir JSON: panel
tanımları, seriler, ve tipli çizim öğeleri (`fib_ladder`, `polygon_fill`,
`pill_badge`, `numbered_touch`, `leader_line`, `zone_band`, `right_edge_label`).
Kütüphane değiştirmek isterse tek bir renderer değişir, 24 komposer değişmez.

Bu, eski mimarinin üç kanıtlanmış hatasını **yapısal olarak imkânsız** kılar:
- Her `Line` iki uca indirgeniyordu → ChartSpec'te seri tam dizi taşır.
- Alt panellerin y aralığı tüm geçmişten ölçekleniyordu → panel kendi y'sini
  kendi serilerinden hesaplar.
- Eksik stil adı sessizce griye düşüyordu → rol kümesi **kapalı**, bilinmeyen
  ad `ValueError` atar.

---

## 5. Grafik motoru kararı (senin kararın gerekiyor)

Senin iki isteğin var ve bunlar farklı yönlere çekiyor:

1. *"imleç nereye giderse o noktada bilgiler gelsin"* — canlı etkileşim.
2. Referans görsellerdeki **birebir** görünüm: dolgulu XAB/BCD üçgenleri, sağ
   kenarda renkli fibo merdiveni, hap biçimli rozetler, numaralı temas
   daireleri, çakışmayan etiketler.

| Seçenek | Artı | Eksi |
|---|---|---|
| **A. Plotly.js finance** (mevcut planın yolu) | Hover/crosshair/zaman aralığı düğmeleri hazır; referans görsellerin bir kısmı **zaten Plotly çıktısı**; Python tarafı figürü doğrudan üretebilir | Tipografi ve etiket yerleşiminde ince kontrol zayıf; hap rozet/önder çizgi için hile gerekiyor; 350 KB |
| **B. TradingView Lightweight Charts v5 + SVG overlay** | Mum/hacim/crosshair TradingView kalitesinde ve **45 KB**; çok hızlı; strateji çizimleri bizim SVG katmanımızda → tasarım şartnamesine **birebir** uyulabilir | İki katmanı koordinat olarak senkronlamak gerekir; overlay'i biz yazacağız |
| **C. Tamamen özel SVG/Canvas** | Şartnameye %100 uyum | Hover/crosshair/zoom/pan'i sıfırdan yazmak = haftalar |

**Önerim: B.** Gerekçe: senin şikayetinin merkezi "grafikler kötü duruyor" —
bu, mumların değil **strateji çizimlerinin** sorunu. B, mumları/etkileşimi
bedava verip tüm kontrolü tam da sorunun olduğu yerde bize bırakıyor. Ayrıca
`ChartSpec` sözleşmesi sayesinde bu karar geri alınabilir kalıyor.

**Not:** `packages/chart` Python'da ChartSpec üretmeye devam eder; PNG çıktısı
(rapor/Telegram/paylaşım) aynı spec'ten `resvg` ile basılır. Tek tanım, iki çıktı.

---

## 6. "Karışıklık" sorununun çözümü: Strateji Pasaportu

Senin en net isteğin buydu: *"her strateji tek tek tamamlanmalı, karışıklık
olmadan."* Bunun bir sürece bağlanması gerekiyor, yoksa tekrar aynı yere
geliriz. Öneri: her strateji için `docs/strateji/<ad>.md` adında bir **pasaport**
dosyası ve **7 kapı**. Bir kapı geçilmeden sonraki açılmaz; tüm kapılar
geçilmeden **sıradaki stratejiye geçilmez**.

| Kapı | Adı | Bitti kriteri |
|---|---|---|
| **K0** | **Kaynak** | Kuralın geldiği kitap/makale, sayfa numarasıyla; tüm eşikler alıntılanmış. Ezberden sayı yazmak yasak. |
| **K1** | **Sözleşme** | Tipli sonuç dataclass'ı, parametreler (frozen), durum makinesi (pending→confirmed→…), non-repaint gerekçesi yazılı. |
| **K2** | **Dedektör** | Kod + birim testler + **walk-forward repaint testi** + lookahead lint temiz. |
| **K3** | **Kalibrasyon** | Tam 648 sembollük evrende aday sayısı ölçülmüş. Sıfıra yakınsa bozuk, on binlerse çok gevşek. Ölçüm dosyası `docs/olcum/` altında. |
| **K4** | **İstatistik** | **Sembol-kümelenmiş** ileri getiri testi, IS/OOS ayrımı, permütasyon + BH-FDR. Sonuç dürüstçe yazılır: *kenar var / yok / belirsiz*. Elenmez — etiketlenir. |
| **K5** | **Görsel** | Komposer yazılır, gerçek veriyle ekran görüntüsü alınır, **referans görselle yan yana konur**, en az 3 iterasyon, **senin onayın**. |
| **K6** | **Ürün** | Tarama tablosunda satır + grafik sayfasında sekme + "Nasıl Okunur" metni + alarm kuralı. |

**Neden bu işe yarar:** eski süreçte K5 hiç yoktu — *"hiç kimse çıktının
resmine bakıp referansla karşılaştırmadı. 115 test dosyası vardı ama hepsi
veri yapısı testiydi."* Ve K4 en sona bırakıldığı için 27 gösterge kodlandıktan
**sonra** hiçbirinin işe yaramadığı anlaşıldı.

**Tek bir strateji için tahmini süre:** 1–2 oturum (K4'ün tam evren ölçümü
tek başına ~1.5 saat makine zamanı).

---

## 7. Strateji sırası

27 göstergenin tamamı gelmeyecek — **9'u ile başlayıp** kalanları ölçüm
sonuçlarına göre alacağız. Sıra üç ölçüte göre: (a) net bir referans görseli
var mı, (b) istatistiksel olarak henüz çürütülmemiş mi, (c) ürünün temel
hikâyesini taşıyor mu.

| # | Strateji | Referans | İstatistik durumu | Neden bu sırada |
|---|---|---|---|---|
| 1 | `structure.golden_zone` + fib retracement | `HRhIeAdbcAAL2_B` | en az çürütülmüş 3'ten biri | En net referans görsel; baskın-swing kararı **zaten backtest edilmiş** (%86.7 vs %59.3). Pilot için ideal. |
| 2 | `structure.market_structure` (HH/HL/LH/LL + BOS/CHoCH) | `ornek1.png` | ölçülmedi | Diğer her şeyin altyapısı; görsel dili basit. |
| 3 | `structure.range_box` (yatay aralık) | `HRjNKRZWAAAhfSy` | ölçülmedi | Komposeri **zaten bitti** (4 tur görsel doğrulama geçti). |
| 4 | `trend.channel` (paralel kanal, CMT kuralı) | `HRiOTwUbQAA9WKw` | ölçülmedi | Fon tarafıyla kesişimin ana aracı. |
| 5 | `trend.ewmac` | — | **en güçlü aday** (n=559, p=0.034) | Görsel olarak sade ama sayısal olarak en umut verici; K4'ü ilk geçme ihtimali en yüksek. |
| 6 | `patterns.head_shoulders` / `double_top_bottom` | `TOBO.png` | ölçülmedi | Kullanıcıların en çok tanıdığı formasyonlar; hologram + boyun çizgisi işi zaten yapıldı. |
| 7 | `harmonic.*` (Carney + Pesavento ile başla) | `HRhIeAdbcAAL2_B`, `HRhMNlYbwAACrVs` | `carney` −%3.66 (n=68) — **dikkat** | En zor görsel; 8 ekolün hepsi değil, önce 2'si. |
| 8 | `structure.supply_demand` | kullanıcı koyu tema kutusu | ölçülmedi | Basit, popüler. |
| 9 | `pair.relative_momentum` + Pair Health | `HRcUk75bgAApv6n` | 17 çiftte çalışıyor | Ayrı bir ürün paketi; en son. |

Kalan 18'i (broadening, wedge, triangle, flag_pennant, breakout_fvg,
five_zero, nenstar, navarro200, gilmore, cypher, three_drives, weekly_channel,
ma_systems, breakouts, price_structure, swing_fib_abcd, alpha_rank,
momentum_rank, vol_harvest) **arşive** alıyoruz — kodları duruyor, siteye
çıkmıyorlar. Sırası gelince aynı 7 kapıdan geçerler.

---

## 8. İhtiyacımız olan agent'lar, skill'ler ve araçlar

Sorduğun için ayrı bölüm. Şu an elimizde `grafik-tasarimcisi` agent'ı ve
`grafik-tasarim-sistemi` + `tlab-mimari` skill'leri var — bunlar taşınacak ve
genişletilecek.

### 8.1 Agent'lar (yeni depoda `.claude/agents/`)

| Agent | İşi | Kapı |
|---|---|---|
| `kaynak-okuyucu` | Kitaplardan (books/ + bilgi-bankasi/) kuralı sayfa numarasıyla çıkarır; eşik uydurmaz | K0 |
| `strateji-kodlayici` | Dedektör + tipli sonuç + non-repaint testleri | K1, K2 |
| `olcum-uzmani` | Kalibrasyon + sembol-kümelenmiş istatistik + FDR + Deflated Sharpe | K3, K4 |
| `grafik-tasarimcisi` (mevcut, genişletilir) | Komposer + **zorunlu görsel doğrulama döngüsü**: render → ekran görüntüsü → referansla karşılaştır → düzelt ×3 | K5 |
| `arayuz-tasarimcisi` (**yeni**) | Web tasarım sistemi, bileşen kütüphanesi, sayfa düzeni; Mobbin referanslarını okur | Faz 2 |
| `seytanin-avukati` (mevcut global `devils-advocate-risk-finder`) | Her kapı geçişinde "bu gerçekten bitti mi" denetimi | tüm kapılar |

### 8.2 Skill'ler

- `quaxis-mimari` — katman ayrımı, non-repaint kuralları, yasak API listesi,
  `ChartSpec` sözleşmesi. **Her teknik işten önce okunur.**
- `strateji-pasaportu` — 7 kapının tanımı ve şablon dosyası.
- `grafik-tasarim-sistemi` (mevcut) — 3 tema, token kuralı, etiket yerleşimi,
  zorunlu görsel döngü.
- `web-tasarim-sistemi` (**yeni**) — renk/tipografi token'ları, bileşen
  envanteri, yoğun veri tablosu kuralları, erişilebilirlik eşikleri.

### 8.3 Araçlar — elimizde olanlar

| Araç | Ne için | Durum |
|---|---|---|
| **Mobbin MCP** | `search_screens` / `search_flows` / `search_sections` — arayüz referansı aramak | ✅ bağlı |
| **Browser (in-app)** | Siteyi canlı açıp ekran görüntüsü almak, hover davranışını doğrulamak | ✅ bağlı |
| **TradingView MCP** | Pine ile strateji çapraz-doğrulaması, gerçek grafikle karşılaştırma, ekran görüntüsü | ✅ bağlı (78 araç) |
| **Playwright/Chromium** | Görsel kabul döngüsü (otomatik snapshot + karşılaştırma) | ✅ kurulu |
| **Artifact** | Kod yazmadan önce tasarım maketini yayınlayıp onayını almak | ✅ |
| Figma / Canva / Notion / Linear MCP | — | ⚠️ **yetkilendirme gerekiyor** (claude.ai bağlayıcı ayarlarından) |
| GitHub MCP | PR/issue yönetimi | ❌ bağlanamadı ("dynamic client registration" desteklenmiyor) — `gh` CLI ile çalışırız |

### 8.4 Senin sağlaman gerekenler

1. **Mobbin şemaları** — bahsettiğin kaydettiğin şemaları diskte bulamadım.
   Ya `references/` klasörüne indir, ya da Mobbin MCP ile hangi uygulamaları
   referans aldığını söyle, ben çekerim.
2. **Veri sağlayıcı kararı** — şu an tek kaynak `yfinance`; önceki oturumda
   kurumsal ağda 403 verdi ve BIST verisi için de ideal değil. Alternatif:
   İş Yatırım / Fintables / KAP (temel tarafta zaten fetcher'lar var).
3. **API anahtarları** — Gemini (yorum metni için, zaten kullanılıyor).

---

## 9. Faz planı — adım adım

Her faz **ayrı bir oturumda** başlatılmalı (`/clear` ile) — bu senin kendi
çalışma kuralın ve token açısından da doğru.

### Faz 0 — Kuruluş *(1 oturum)*
- `Desktop\QuaxisLabs\` altında **yeni, temiz git deposu** (`git init`),
  ev dizinindeki 4 GB'lık depodan tamamen bağımsız.
- Monorepo iskeleti (Bölüm 4), `pyproject.toml`, `package.json`, `Makefile`,
  `.gitignore` (veri/önbellek/PDF **kesinlikle** hariç), pre-commit.
- GitHub'da yeni depo mu, `QuaxisLabs`'ı sıfırlamak mı — **senin kararın**
  (Bölüm 11, Soru 3).
- `docs/karar/ADR-001-yeniden-insa.md` — bu raporun özeti, kalıcı kayıt.
- **Bitti kriteri:** `git log` tek commit, `.git` < 5 MB.

### Faz 1 — Sözleşmeler *(1 oturum)*
- `packages/ortak/` — `Signal`, `IndicatorResult`, `ChartSpec` v1 şeması
  (JSON Schema + Python dataclass + TS tipi, tek kaynaktan üretilir).
- `docs/strateji/_SABLON.md` — pasaport şablonu, 7 kapı.
- `.claude/skills/quaxis-mimari` + `strateji-pasaportu` yazılır.
- **Bitti kriteri:** ChartSpec'in TS ve Python tarafı aynı örnek dosyayı
  doğruluyor.

### Faz 2 — Tasarım sistemi ve kabuk *(2 oturum)*
- Mobbin referansları toplanır → `references/`.
- **Önce Artifact olarak maket**, senin onayın, sonra kod.
- `apps/web`: 3 tema token seti, `next/font` ile yerel fontlar (Türkçe glif
  testi zorunlu), 13 bileşen (`Card`, `DataTable` sanallaştırılmış, `StatTile`,
  `Pill`, `Tab`, `Skeleton`, `EmptyState`…), `/tasarim` iç vitrin sayfası.
- Kabuk: sol ray (4 ürün paketi), üst şerit, **⌘K komut paleti**, yükleme/boş/
  hata durumları.
- **Bitti kriteri:** 3 tema × 2 genişlik ekran görüntüleri alınmış, **gözle
  incelenmiş**, en az 3 iterasyon; `npm run build` temiz.

### Faz 3 — Motor göçü *(2 oturum)*
- `tlab/{core,data,features,indicators,scanner,testing}` → `packages/teknik/`,
  ad `quaxis.teknik`. `tlab/viz` **gelmez**.
- 1008 test yeni depoda yeşil olmadan faz bitmez.
- Veri önbelleği (121 MB) depo dışında, `data/` git-ignore.
- FastAPI iskeleti: `/api/tarama`, `/api/grafik`, `/api/katalog`.
- **Bitti kriteri:** `pytest -q` yeşil, `tlab eod --market bist` yeni depoda
  koşuyor.

### Faz 4 — İlk strateji uçtan uca *(2 oturum)* ⭐
**Pilot: `structure.golden_zone`.** 7 kapının tamamı. Bu faz bittiğinde
elinde çalışan bir ürün var: tarama sayfasında sinyal listesi → tıkla →
grafik açılıyor → sinyalin nasıl oluştuğu referans görsel kalitesinde
çizilmiş → yanında "nasıl okunur" ve dürüst bir istatistik rozeti.

Bu fazı **kesinlikle acele etmiyoruz** — süreç burada kanıtlanıyor. Sonraki
8 strateji bu kalıbın tekrarı olacak.

### Faz 5–8 — Strateji strateji *(strateji başına 1–2 oturum)*
Bölüm 7'deki sırayla, 2'den 9'a.

### Faz 9 — Tarama, alarm, evren yüzeyleri *(2 oturum)*
- Tazelik filtresi (son 1/3/10 mum), satır-üzeri grafik önizlemesi,
  kaydedilmiş taramalar, karşılaştırma.
- Alarm motoru (`packages/teknik/alerts/`) + Telegram kanalı (bot zaten var)
  + "bu kural son 30 günde N kez tetiklenirdi" canlı önizlemesi.
- Evren yüzeyi: sektör rotasyonu, piyasa genişliği, momentum ısı haritası.

### Faz 10 — Temel analiz entegrasyonu *(3–4 oturum)*
- `bilanco-radar` motoru `packages/temel/`e taşınır.
- Kalan 3 kitap (Fisher, Lynch, Schilit) çıkarımı.
- **10+ yıllık seri veri açığı kapatılır** (KAP XBRL / İş Yatırım kalem kodları).
- 4 mercek + bileşik skor → ortak tarama yüzeyinde teknik sinyalle **aynı
  tabloda**: "temel skoru yüksek + teknik sinyal taze" kesişim taraması.
  **Projenin asıl fikri bu kesişim.**

### Faz 11 — Mobil *(ayrı bir iş)*
`Desktop\Quaxis\mobile` Flutter iskeleti temel alınır.

**Toplam kaba tahmin:** Faz 0–9 arası **18–24 oturum**. Faz 10 ayrı **3–4**.

---

## 10. Riskler ve dürüst uyarılar

1. **Sinyaller çalışmayabilir.** K4 kapısı 9 stratejinin çoğunu "kenar
   kanıtlanmadı" olarak etiketleyebilir. Buna hazırlıklı ol — ürünün değeri o
   zaman "kanıtlanmış kâr" değil, **"dürüst, tekrarlanabilir, görselleştirilmiş
   tarama"** olur. Bu da satılabilir bir şey, ama farklı bir vaat.
2. **Görsel kabul döngüsü pahalıdır.** Her strateji için en az 3 tur render +
   inceleme. Kısa kesersen eski duruma döneriz — bu döngünün yokluğu aylarca
   kaybedilen şeydi.
3. **Veri sağlayıcı tek nokta.** `yfinance` kırılgan; BIST için kurumsal
   kaynak (İş Yatırım/Fintables) daha sağlıklı.
4. **Mobbin'in görsel kimliği kopyalanamaz** — yoğunluk dili ve yüzey düzeni
   alınır, marka/renk/tipografi bizim. Hem hukuken doğru hem zaten 3 temalı
   kendi şartnamen var.
5. **"Yatırım tavsiyesi değildir"** uyarısı her sayfada kalmalı.

---

## 11. Senden gereken 4 karar

Bunlar cevaplanmadan Faz 0'a başlamıyorum.

**Soru 1 — Motor taşınsın mı, sıfırdan mı?**
Önerim: taşınsın (Bölüm 3). Sıfırdan istersen de yaparım ama tahminen 6–8
oturum ek maliyet ve aynı hataları tekrar bulma riski.

**Soru 2 — Grafik motoru: A (Plotly), B (Lightweight Charts + SVG overlay),
C (tam özel)?**
Önerim: B (Bölüm 5).

**Soru 3 — GitHub deposu:** mevcut `QuaxisLabs` deposunu sıfırlayıp yeniden mi
kullanalım, yoksa yeni bir depo mu açalım (ör. `quaxislabs-v2`)? Mevcut depo
ev dizini karmaşasıyla ilişkili — temiz başlangıç için yeni depo öneriyorum,
eskisi arşiv olarak kalır.

**Soru 4 — Mobbin şemaları nerede?** Diskte bulamadım. İndirip
`QuaxisLabs\references\` içine koyar mısın; yoksa hangi uygulamaları referans
aldığını söyle, Mobbin MCP ile ben çekeyim.

---

## Ek — İncelenen kaynaklar

Bu rapor şu dosyaların okunmasıyla yazıldı:

- `Teknik Analiz\` — `README.md`, `docs/KARAR_VE_YENIDEN_INSA.md`,
  `docs/SITE_TASARIM_YOL_HARITASI.md`, `docs/SON_DURUM.md`,
  `docs/KALAN_ISLER.md`, `CLAUDE.md` (yapı), `.claude/skills/*`,
  tüm `tlab/` ve `web/` modül ağacı, referans görseller
  (`önemli/HRhIeAdbcAAL2_B.png`, `docs/design/intem/bat_xabcd_4h.png`)
- `Temel Analiz\bilanco-radar\` — `bilgi-bankasi/_ilerleme.md`, `src/` ağacı,
  `bilgi-bankasi/teknik/`
- `Quant Playbook\books\` — 17 kaynağın envanteri
- `Desktop\Quaxis\` — `README.md`, mobil/backend iskeleti
- Hafıza dosyaları (proje durumu, git tehlikeleri, çalışma tercihleri)
