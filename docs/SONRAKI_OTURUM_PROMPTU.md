# Sonraki oturum promptu — Faz 2 (kod)

Aşağıdaki bloğu **olduğu gibi kopyalayıp** temiz bir oturuma (`/clear` sonrası)
yapıştır. Çalışma dizini `C:\Users\Samet\Desktop\QuaxisLabs` olmalı.

---

```
QuaxisLabs projesinde Faz 2'nin kod kısmına başlıyoruz.

ÖNCE ŞUNLARI OKU (sırayla, tamamını):
1. docs/karar/ADR-001-yeniden-insa.md
2. docs/karar/ADR-002-strateji-kodlari-sifirdan.md
3. docs/design/TASARIM_DILI.md   (7 bölümün hepsi — ölçülmüş token'lar,
   9 ortak ilke, turkuaz aksan kararı, sayfa yapıları, strateji sayfası iskeleti)
4. docs/design/maket_v1.html     (ONAYLANMIŞ maket — token sistemi, bileşenler,
   beş yüzey. Bu dosya şartnamedir, ilham panosu değil.)
5. README.md                     (müzakereye kapalı 7 kural + faz tablosu)

DURUM:
- Faz 0 (depo, iskelet, ADR'ler) ve Faz 1 (tasarım dili) bitti ve push edildi.
- Maket kullanıcı tarafından onaylandı. Aksan turkuaz #2ED3C0, koyu tema
  varsayılan, üç tema desteklenecek.
- apps/web şu an boş bir klasör.

GÖREV — Faz 2'nin kod kısmı: apps/web kurulumu ve tasarım sistemi.

1. apps/web altına Next.js 16 + React 19 + TypeScript + Tailwind 4 projesi kur
   (App Router, src dizini yok, import alias @/*).

2. maket_v1.html'in <style> bloğundaki TOKEN SİSTEMİNİ globals.css'e taşı.
   BİREBİR taşı, yeniden yorumlama. Üç durum da korunacak: bare :root (koyu,
   varsayılan), @media (prefers-color-scheme: light) içinde
   :root:not([data-theme="dark"]), ve :root[data-theme="light"].
   data-accent varyantları da gelecek.

3. Fontlar next/font ile YEREL: Archivo (display), Inter (arayüz),
   JetBrains Mono (sayı + eyebrow). CDN bağımlılığı OLMAYACAK.
   Türkçe glifleri (İ ı Ğ ğ Ş ş Ç ç Ö ö Ü ü) üç fontta da ekran görüntüsü
   alıp GÖZLE doğrula.

4. components/ui/ altına maketteki bileşenleri React'e çevir:
   Eyebrow, Pill, Chip, ChipGroup, Button, Card, Panel, StatTile, DataTable,
   Sparkline, EmptyState, Skeleton, ThemeSegment (sistem/açık/koyu),
   Tab/Seg, Faq(details).
   DataTable ZORUNLU: sıralanabilir kolonlar, sanallaştırma (500+ satırda
   60fps), tabular-nums, satır-üzeri kancası, klavye gezinmesi.

5. /tasarim iç vitrin sayfası: tüm bileşenleri üç temada yan yana gösterir.
   Gelecekteki her tasarım işinin referansı bu sayfa olacak.

KURALLAR (README.md'den, müzakereye kapalı):
- Gölge YOK. Yüzeyler bir tık açık zemin + beyaz alfa kenarlıkla ayrılır.
- Ağırlık 400 varsayılan; 500 yalnızca vurgu. 700 kullanma.
- Hiyerarşi boyutla değil OPAKLIKLA (%100 / %62 / %34).
- Panel/kart yarıçapı 2px, kontrol tam hap. Ara değer yalnızca medya kutusunda.
- Aksan ASLA mum ölçeğinde dolu bir leke değil. Yön renkleri her zaman dolu.
- Her sayı mono + font-variant-numeric: tabular-nums.
- Kaydırma tetikli açılış animasyonu YASAK — sayfa ilk boyamada eksiksiz okunur.
  prefers-reduced-motion her zaman saygı görür.
- Hardcoded renk YASAK; her renk token'dan gelir.

BU TURDA YAPMA:
- Grafik motoru (Lightweight Charts + SVG overlay) Faz 4'ün işi.
- Gerçek veri, API, gösterge kodu YOK. Bileşenler maketteki örnek veriyle
  beslenecek ve "örnek veri" olarak işaretlenecek.
- packages/teknik'e dokunma — motor göçü Faz 5.

DOĞRULAMA (ZORUNLU):
- npm run build ve npm run lint temiz.
- /tasarim sayfasının 3 temada, 2 genişlikte (1440 ve 768) ekran görüntüsünü al,
  docs/design/ui/ altına kaydet, Read ile AÇ VE GÖR, sorunları madde madde yaz,
  düzelt, tekrarla. EN AZ 3 İTERASYON.
- DataTable'ı 500 satırla ölç ve raporla.

BİTTİ KRİTERİ:
apps/web derleniyor, 15 bileşen var, /tasarim üç temada çalışıyor, ekran
görüntüleri görülmüş ve en az 3 iterasyondan geçmiş, README'deki faz tablosu
güncellenmiş, commit edilip push edilmiş.

Her parça bitince commit + push et (kullanıcının kalıcı tercihi), oturum
sonunu bekleme.
```

---

## Sonraki fazlar (bu oturumdan sonra)

| Faz | İş | Ön koşul |
|---|---|---|
| 3 | Uygulama kabuğu + sayfa iskeletleri (tarama, grafik, strateji sayfası) | Faz 2 |
| 4 | `ChartSpec` v1 + grafik motoru (Lightweight Charts + SVG overlay) | Faz 3 |
| — | **Kullanıcı onayı: "site artık istediğim gibi"** | Faz 4 |
| 5 | Altyapı göçü: `core` + `testing` + `data` + `scanner` | onay |
| 6 | Strateji Pasaportu süreci: şablon, agent'lar, skill'ler | Faz 5 |
| 7.x | Stratejiler — birer birer, 7 kapı, sayı sınırı yok | Faz 6 |
