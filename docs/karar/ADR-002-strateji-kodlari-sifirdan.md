# ADR-002 — Strateji kodları sıfırdan yazılır; faz planı yeniden düzenlenir

**Tarih:** 2026-09-12
**Durum:** KABUL EDİLDİ
**Karar veren:** Şeref Samet Umutlu
**İlişki:** [ADR-001](ADR-001-yeniden-insa.md)'in 2. ve 6. maddelerini **değiştirir**.

---

## Bağlam

ADR-001 "motor taşınır, sıfırdan yazılmaz" diyordu ve faz planı 9 strateji ile
sınırlıydı, ayrıca temel analiz (Faz 10) ve mobil (Faz 11) fazlarını içeriyordu.
Kullanıcı planı inceleyip üç noktada düzeltti:

> *"her bir stratejinin kodunu en baştan doğru olacak şekilde yazmalıyız,
> öncekine aşırı güvenmiyorum... hem gerekli koşullarına göre hem de kitaplardan
> araştırmalar yaparak oluşturacağız, her strateji öncekiyle birebir aynı
> olmayacak."*
>
> *"8-9 falan değil birer birer gideceğiz ve tüm stratejileri veya büyük
> çoğunluğunu ekleyeceğiz, bir sınırlama koyma."*
>
> *"temel analiz ve mobil kısmı buraya yazılacak bir aşama değil, onlar en son,
> belki yapmam bile. Önceliğimiz siteyi mükemmel görseli olacak şekilde kurmak
> ve teknik analiz kısmını entegre etmek."*

Bu düzeltme, Bölüm 2'deki istatistiksel bulguyla da tutarlı: 27 göstergenin
hiçbiri sembol-kümelenmiş, FDR-düzeltmeli bir OOS kenarı kanıtlayamadı. Yani
mevcut gösterge kodlarına duyulan güvensizlik **ölçümle desteklenen** bir
güvensizlik.

## Karar

### 1. Altyapı taşınır, stratejiler sıfırdan yazılır

| Katman | Karar | Gerekçe |
|---|---|---|
| `core` (Signal, IndicatorResult, Registry, params) | **taşınır** | Sözleşme katmanı; strateji mantığı içermez |
| `testing` (repaint testi, lookahead lint) | **taşınır** | Projenin en değerli parçası; strateji-bağımsız |
| `data` (sağlayıcı, önbellek, takvim, resample) | **taşınır** | Strateji-bağımsız boru hattı |
| `scanner` (evren × tf tarama, EOD, SQLite) | **taşınır** | Strateji-bağımsız iş kuyruğu |
| `indicators` (27 gösterge) | **SIFIRDAN** | Kullanıcı kararı; kalibrasyonu ölçümle çürütülmüş |
| `features` (swing, fib, trendline, zone…) | **strateji strateji, seçerek** | Bir stratejinin ihtiyaç duyduğu özellik, o stratejinin pasaportunda yeniden gözden geçirilir; olduğu gibi taşınmaz |
| `viz` | **taşınmaz** | ADR-001 |

`features` için özel not: `build_trendlines` fonksiyonunun aday eşleştirmesinin
CMT'nin "benzer büyüklükteki pivotları birleştir" kuralına uymadığı ve
`price_structure` / `breakouts` / `head_shoulders` / `double_top_bottom`
göstergelerinin hepsini etkilediği önceki projede tespit edilmiş ama
kapatılmamıştı. Bu, `features`'ın olduğu gibi taşınmaması için somut gerekçedir.

### 2. Her strateji K0 kapısında kitaptan yeniden türetilir

Strateji Pasaportu'nun K0 (Kaynak) kapısı artık bir formalite değil, **stratejinin
doğduğu yer**: kural, kitaptan/makaleden sayfa numarasıyla çıkarılır, tüm eşikler
alıntılanır, sonra BIST verisinde kalibre edilir. Eski koda bakılabilir ama
**referans olarak değil, yalnızca karşılaştırma için** — ve farklılık çıkarsa
kitap kazanır.

Kaynaklar: `Quant Playbook\books\` (17 kaynak), `bilanco-radar\bilgi-bankasi\teknik\`
(Pesavento, Carver + 11 bölümlük uygulanabilirlik matrisi), `Desktop\Trading Books\`,
`Desktop\Strateji kaynakları\`.

### 3. Strateji sayısında sınır yok

"9 strateji ile başla" kısıtı **kaldırıldı**. Hedef: tüm stratejiler ya da büyük
çoğunluğu. Sıra bağlayıcı değil, sayı açık uçlu. Tek değişmez kural: **bir
strateji 7 kapının tamamından geçmeden sıradakine geçilmez.**

### 4. Temel analiz ve mobil yol haritasından çıkarıldı

Bu deponun kapsamı: **site + teknik analiz**. Temel analiz entegrasyonu ve mobil
uygulama ileride değerlendirilecek; faz olarak planlanmıyorlar, tarih
verilmiyor. (`packages/temel` klasörü yer tutucu olarak kalır.)

### 5. Sıra değişti: önce site, sonra stratejiler

Kullanıcının önceliği net — *"önceliğimiz siteyi mükemmel görseli olacak şekilde
kurmak."* Yeni plan üç bölüm hâlinde: **A. Site** → **B. Altyapı** → **C.
Stratejiler (birer birer, sınırsız)**. A bölümü kullanıcı onayı almadan B'ye
geçilmez.

## Sonuçlar

**Maliyet:** 8 824 satırlık gösterge katmanı yeniden yazılacak. Strateji başına
1–2 oturum, strateji sayısı açık uçlu.

**Kazanç:** her strateji kitaptan doğrulanmış, BIST'te kalibre edilmiş ve
istatistiksel olarak etiketlenmiş olarak doğar. "Neden bu eşik?" sorusunun
cevabı her zaman pasaport dosyasında yazılı olur.

**Korunan:** non-repaint altyapısı, tarama motoru, veri boru hattı ve bunları
koruyan testler — yani yeniden üretilmesi en pahalı, strateji-bağımsız kısım.
