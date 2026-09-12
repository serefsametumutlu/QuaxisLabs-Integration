# ADR-001 — Yeniden inşa: yeni depo, taşınan motor, yeni çizim katmanı

**Tarih:** 2026-09-12
**Durum:** KABUL EDİLDİ
**Karar veren:** Şeref Samet Umutlu
**Dayanak:** [`docs/00_RAPOR_VE_YOL_HARITASI.md`](../00_RAPOR_VE_YOL_HARITASI.md)

---

## Bağlam

Teknik analiz tarafı (`Desktop\Teknik Analiz\`, paket adı `tlab`) 27 gösterge,
15 400 satırlık motor ve 1008 yeşil testle olgun bir hâle geldi; ancak üç
sorun birikti:

1. **Çizim katmanı çöktü.** 10 475 satırlık tek bir jenerik çizici 24 stratejiyi
   aynı primitif torbasıyla basıyordu. Referans görsellerin hiçbiri jenerik bir
   çizicinin çıktısı değil — her biri o stratejiye özel bestelenmiş. Sonuç:
   okunamayan, üst üste binen, sessizce griye düşen grafikler.
2. **Görsel kabul döngüsü hiç kurulmadı.** 115 test dosyasının tamamı veri
   yapısı testiydi; "bu grafik referansa benziyor mu" diye soran tek bir adım
   yoktu. "Düzeltildi" denen şeyler düzelmemiş görünebildi çünkü kimse bakmıyordu.
3. **Git durumu bozuk.** Deponun kökü `C:\Users\Samet` (tüm ev dizini), `.git`
   4 GB (geçmişte kitap PDF'leri commit edilmiş) ve GitHub'daki depoyla
   ilişkisiz bir commit geçmişi taşıyor. Push için 5 adımlık `git worktree` +
   `git archive` el hilesi gerekiyordu.

Ayrıca 2026-09-11/12 tarihli iki turluk istatistiksel doğrulama, **27
göstergenin hiçbirinin FDR-düzeltmeli, sembol-kümelenmiş bir OOS kenarı
kanıtlamadığını** gösterdi.

## Karar

### 1. Yeni depo açılır
`Desktop\QuaxisLabs\`, kendi `.git`'iyle, ev dizini deposundan tamamen
bağımsız. Remote: `https://github.com/serefsametumutlu/QuaxisLabs-Integration`.
Eski `QuaxisLabs` deposu **arşiv olarak korunur**, hiçbir şey silinmez.

### 2. Motor taşınır, sıfırdan yazılmaz
`core`, `data`, `features`, `indicators`, `scanner`, `testing` ve testleri
`packages/teknik/` altına taşınır (ad: `quaxis.teknik`). Faz 3'te 1008 test
yeni depoda yeşil olmadan faz kapanmaz.

**Gerekçe:** bu katmanlarda yeniden üretilmesi haftalar sürecek öğrenilmiş
dersler var — non-repaint walk-forward test altyapısı, `detected_at` ≠
`bar_time` ayrımı, `pattern_id`'nin konumsal `bar_idx` yerine zaman damgasından
üretilmesi (1M+ sahte "kaybolan sinyal" hatasının kök nedeni), zaman dilimi
ölçekleme tuzağı (`breakout_fvg`/`flag_pennant` 4H'te 648/648 sembolde sıfır
aday veriyordu), harmonik geometri, Bulkowski/Lo-Mamaysky-Wang ölçütleri.

### 3. `tlab/viz` taşınmaz
10 475 satır yeni depoya **hiç girmez**. Yerine `packages/chart/` gelir.

### 4. Yeni çizim sözleşmesi: `ChartSpec`
```
gösterge → TİPLİ sonuç → o tipe ait KOMPOSER → ChartSpec (JSON)
                                                  ├→ web renderer (etkileşimli)
                                                  └→ PNG renderer (rapor/Telegram)
```
`ChartSpec`, çizim kütüphanesinden bağımsız ve versiyonlu bir JSON'dur.
Kapalı bir rol kümesi kullanır — bilinmeyen stil adı sessizce griye düşmek
yerine `ValueError` atar. Panel y aralığı yalnızca o panele verilen serilerden
hesaplanır. Seriler tam dizi taşır (iki uca indirgenmez). Eski mimarinin üç
kanıtlanmış hatası böylece **yapısal olarak imkânsız** hâle gelir.

### 5. Grafik motoru: TradingView Lightweight Charts + SVG overlay
Mum, hacim, crosshair, zoom/pan Lightweight Charts v5'ten (45 KB) gelir;
strateji çizimleri (dolgulu XAB/BCD üçgenleri, sağ kenar fibo merdiveni, hap
biçimli rozetler, numaralı temas daireleri, önder çizgiler) bizim SVG
overlay katmanımızda çizilir ve tasarım şartnamesine birebir uyar.

**Değerlendirilen alternatifler:** Plotly.js finance (hover/crosshair hazır ama
tipografi ve etiket yerleşiminde ince kontrol zayıf, 350 KB) ve tamamen özel
SVG/Canvas (şartnameye %100 uyum ama etkileşimi sıfırdan yazmak haftalar alır).

### 6. Strateji Pasaportu — 7 kapı
Her strateji için `docs/strateji/<ad>.md`. Bir kapı geçilmeden sonraki
açılmaz; tüm kapılar geçilmeden **sıradaki stratejiye geçilmez**.

`K0 Kaynak` → `K1 Sözleşme` → `K2 Dedektör` → `K3 Kalibrasyon` →
`K4 İstatistik` → `K5 Görsel (kullanıcı onayı)` → `K6 Ürün`

27 gösterge yerine **9 strateji** ile başlanır; kalanlar arşivde bekler.

### 7. İstatistiksel dürüstlük ilkesi
K4 kapısı bir eleme değil, bir **etiketleme** kapısıdır. Sonuç ne çıkarsa
sitede o gösterilir: *kenar var / yok / belirsiz*. Ölçülmemiş bir strateji
"kanıtlanmış" diye sunulmaz.

## Sonuçlar

**Kazanılan:** temiz git geçmişi, tek depoda teknik + temel, yeniden
kullanılabilir çizim sözleşmesi, tekrarlanabilir bir strateji tamamlama süreci.

**Ödenen bedel:** motorun taşınması ve testlerin yeşile alınması ~2 oturum;
web katmanı tamamen yeniden yazılıyor (~4 oturum).

**Kabul edilen risk:** K4 kapısı 9 stratejinin çoğunu "kenar kanıtlanmadı"
olarak etiketleyebilir. Bu durumda ürünün vaadi "kanıtlanmış kâr" değil,
**"dürüst, tekrarlanabilir, görselleştirilmiş tarama"** olur.
