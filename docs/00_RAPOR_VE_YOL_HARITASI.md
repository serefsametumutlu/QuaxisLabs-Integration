# QuaxisLabs — Yeniden İnşa Raporu ve Yol Haritası

**Tarih:** 2026-09-12
**Kapsam:** Mevcut üç kod tabanının (teknik / temel / Quaxis mobil), kitap
kaynaklarının ve tüm proje belgelerinin incelenmesi; yeni klasörde sıfırdan
ayağa kaldırma planı.
**Durum:** Kararlar alındı ve uygulanıyor. Bkz. `karar/ADR-001` ve
`karar/ADR-002`. Bölüm 3, 7 ve 9 ADR-002 ile güncellendi; okurken ADR'ler
esas alınmalıdır.

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

> **ADR-002 ile kısmen değiştirildi (2026-09-12).** Aşağıdaki muhakeme
> **altyapı katmanları** (`core`, `testing`, `data`, `scanner`) için geçerliliğini
> koruyor. Ancak kullanıcı kararıyla **`indicators` ve `features` taşınmıyor** —
> her strateji kitaptan yeniden türetilerek sıfırdan yazılacak. Gerekçe:
> `karar/ADR-002-strateji-kodlari-sifirdan.md`.

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

## 7. Strateji sırası ve kapsamı

> **Güncelleme (ADR-002):** "9 strateji ile başla" kısıtı kaldırıldı. Hedef tüm
> stratejiler ya da büyük çoğunluğu; sayı sınırı yok. Ayrıca her stratejinin
> kodu **sıfırdan**, kitaptan türetilerek yazılır — eski koda referans olarak
> değil yalnızca karşılaştırma için bakılır.

Değişmeyen tek kural: **bir strateji 7 kapının tamamından geçmeden sıradakine
geçilmez.** Sıra, Bölüm B bittikten sonra birlikte belirlenecek; ilk adayların
seçim ölçütü şu üçü:

1. **Net bir referans görseli var mı** — K5 kapısı için hedef lazım.
2. **Kitap kaynağı ne kadar somut** — K0 kapısı eşikleri alıntıyla ister.
3. **İstatistiksel olarak henüz çürütülmemiş mi** — önceki ölçümde
   `trend.ewmac`, `structure.golden_zone`, `trend.ma_systems` en az çürütülmüş
   üçlüydü; `harmonic.carney` (−%3.66, n=68) ve `patterns.broadening`
   (−%1.86, n=102) ise negatif taraftaydı.

Referans görseli bulunan aday havuzu (`önemli/` + `images/` klasörlerinden):
fibo merdiveni / altın bölge, piyasa yapısı (HH-HL-LH-LL, BOS/CHoCH), yatay
aralık, paralel kanal, üçgen/kama, bayrak-flama, XABCD harmonikleri, üç itiş,
A-B-C-D salınımı, arz-talep bölgeleri, çift sağlığı, likidite (Corwin-Schultz),
istatistik tablosu.

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

> **Güncelleme (ADR-002):** sıra değişti — **önce site**, sonra altyapı, sonra
> stratejiler. Temel analiz ve mobil bu plandan çıkarıldı.

Her faz **ayrı bir oturumda** başlatılmalı (`/clear` ile).

### BÖLÜM A — SİTE
*Bitiş kriteri: senin "bu site artık istediğim gibi görünüyor" onayın. Bu onay
alınmadan Bölüm B'ye geçilmez.*

**Faz 0 — Kuruluş** ✅ *(bitti)*
Yeni ve temiz git deposu (`.git` 108 KB), monorepo iskeleti, `.gitignore`,
ADR-001 ve ADR-002.

**Faz 1 — Tasarım referansları ve tasarım dili** *(1 oturum)*
- Kullanıcının verdiği 4 referans sitesi gezilir: dovetail.com, slash.com,
  v7labs.com, luxalgo.com.
- Her siteden: ekran görüntüleri + **hesaplanmış tasarım token'ları**
  (font aileleri, renk paleti, yarıçap ölçeği, boşluk ritmi, gölge katmanları).
- Çıktı: `docs/design/TASARIM_DILI.md` — dört sitenin **ortak** dili ve
  QuaxisLabs'a ne alınacağı; `references/` altında kanıt dosyaları.
- Kritik ilke: dördü **birlikte** incelenir, tek tek yamalanmaz.

**Faz 2 — Tasarım sistemi ve bileşen kütüphanesi** *(2 oturum)*
- Önce **Artifact olarak maket**, senin onayın, sonra kod.
- `apps/web`: tema token setleri, `next/font` ile yerel fontlar (Türkçe glif
  testi zorunlu: İ ı Ğ ğ Ş ş Ç ç Ö ö Ü ü).
- Bileşenler: `Card`, `Panel`, `SectionLabel`, `Pill`, `Badge`, `Tab`,
  `StatTile`, `DataTable` (sanallaştırılmış, 500+ satırda 60 fps),
  `Sparkline`, `EmptyState`, `Skeleton`.
- `/tasarim` iç vitrin sayfası — gelecekteki her tasarım işinin referansı.

**Faz 3 — Uygulama kabuğu ve sayfa iskeletleri** *(1-2 oturum)*
- Sol ray (ürün paketleri), üst şerit, **⌘K komut paleti**, tema seçici.
- Sayfa iskeletleri: Tarama, Grafik, Strateji Kütüphanesi.
- Yükleme / boş / hata durumlarının üçü de tasarlanmış olmalı.
- Doğrulama: 3 tema × 2 genişlik (1440/768) ekran görüntüsü, **gözle
  incelenmiş**, en az 3 iterasyon.

**Faz 4 — `ChartSpec` v1 ve grafik motoru** *(2 oturum)*
- `ChartSpec` şeması: JSON Schema + Python dataclass + TypeScript tipi, tek
  kaynaktan üretilir.
- Web renderer: Lightweight Charts v5 (mum/hacim/crosshair/zoom) + kendi SVG
  overlay katmanımız (fibo merdiveni, dolgulu poligon, hap rozet, numaralı
  temas, önder çizgi, sağ kenar etiketi).
- **Kabul kriteri:** referans görsellerden en az üçü, elle yazılmış bir
  `ChartSpec` ile **birebir** yeniden üretilir. Gerçek gösterge kodu henüz yok —
  bu fazda çizim katmanı tek başına kanıtlanır.

### BÖLÜM B — ALTYAPI

**Faz 5 — Altyapı göçü** *(2 oturum)*
- `core`, `testing`, `data`, `scanner` → `packages/teknik/` (ad `quaxis.teknik`).
- **Gösterge taşınmaz.** `features` de taşınmaz; strateji strateji gelecek.
- Bu katmanların testleri yeni depoda yeşil olmadan faz bitmez.
- FastAPI: `/api/tarama`, `/api/grafik`, `/api/katalog`.
- Veri sağlayıcı kararı burada uygulanır (bkz. Bölüm 11, açık konu).

**Faz 6 — Strateji Pasaportu süreci** *(1 oturum)*
- `docs/strateji/_SABLON.md` — 7 kapı, doldurulacak alanlar, kanıt yerleri.
- `.claude/agents/`: `kaynak-okuyucu`, `strateji-kodlayici`, `olcum-uzmani`,
  `grafik-tasarimcisi`, `arayuz-tasarimcisi`.
- `.claude/skills/`: `quaxis-mimari`, `strateji-pasaportu`,
  `grafik-tasarim-sistemi`, `web-tasarim-sistemi`.
- `tools/`: görsel kabul döngüsü (render → ekran görüntüsü → referansla
  karşılaştır), kalibrasyon ve istatistik koşucuları.

### BÖLÜM C — STRATEJİLER *(birer birer, sayı sınırı yok)*

Her strateji kendi fazı: **Faz 7.1, 7.2, 7.3, …**
Her biri K0 → K6. Bir strateji bitmeden sıradakine geçilmez. Strateji başına
tahmini 1–2 oturum (K4'ün tam evren ölçümü tek başına ~1.5 saat makine zamanı).

### Kapsam dışı (bu depoda planlanmıyor)
Temel analiz entegrasyonu ve mobil uygulama. `packages/temel` yer tutucu olarak
kalır; sırası gelirse ayrı bir ADR ile planlanır.

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
