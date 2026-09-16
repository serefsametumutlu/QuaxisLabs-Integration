# ADR-003 — Tarama sonucu web'e derleme anında JSON ile taşınır

**Tarih:** 2026-09-17
**Durum:** KABUL EDİLDİ
**Karar veren:** Şeref Samet Umutlu
**İlişki:** [ADR-001](ADR-001-yeniden-insa.md)'in katman ayrımı kuralını uygular.

---

## Bağlam

Üç strateji ailesi ölçülüp etiketlendi ama ürünün giriş noktası olan tarama
yüzeyi (`/tarama`) hâlâ `apps/web/lib/ornek-veri.ts`'ten **maket satır**
üretiyordu. `ENVANTER.md` bunu zaten işaretlemişti; harmoniklerin K6 kapısı
da tam bu yüzden açık kaldı:

> "Buraya sahte harmonik satırlar eklemek kapıyı kapatırdı ama yalan olurdu:
> kullanıcı gerçek bir tarama sonucu sandığı şeye bakardı."

Depoya bakınca eksiğin **motor olmadığı** görüldü. `scanner/engine.py` ve
`scanner/eod.py` (takvim → veri → kalite → tarama → kalıcılaştırma → diff →
rapor) yazılmıştı; `results.py` sonuçları SQLite'a yazıyor ve
`latest_signals()` docstring'inde açıkça "web/dashboard tüketiciler için" diye
tasarlanmıştı.

Eksik olan iki şeydi:

1. **`run_eod`'u çağıran bir kol yoktu.** Tek çağıran bir
   `@pytest.mark.network` testiydi ve tek sembollük evrenle koşuyordu. Depodaki
   tek EOD raporunda `universe_size: 1` yazıyordu — boru hattı gerçek ölçekte
   hiç koşmamıştı.
2. **Depodan web'e bir köprü yoktu.**

## Karar

### 1. Koşucu: `tools/tarama.py`

`run_eod`'un giriş kapısı. Varsayılan zaman dilimi **yalnız `1d`** (`run_eod`
varsayılanı `4h + 1d + w1` idi): üç stratejinin üçü de 1G'de ölçüldü. 4S'te
sinyal üretip yanına 1G'den gelen verdikt rozetini koymak, rozetin hiçbir şey
bilmediği bir sinyali etiketlemek olurdu. Sağlayıcı saatlik veriyi zaten
yalnız son 2 yıl için veriyor, yani 4S'te ölçüm de yapılamıyor.

### 2. Köprü: derleme anında JSON

`tools/tarama_disaktar.py` → `apps/web/lib/tarama-verisi.json` → `lib/tarama.ts`.

| Seçenek | Neden seçilmedi / seçildi |
|---|---|
| **Derleme anında JSON** | ✅ **seçildi** |
| İstek anında Next API route → `results.db` | ✘ statik dışa aktarımı (`QUAXIS_EXPORT=1`) kırar — görsel kabul döngüsü ona dayanıyor; ayrıca web'i doğrudan motorun deposuna bağlar |

Tarama **günde bir kere** (kapanış sonrası) koşuyor. İstek anında veritabanı
okumak tazelik kazandırmaz; karşılığında mimarideki tek yönlü ok
(`Veri → … → Depo → Görselleştirme`) tersine akmaya başlar.

### 3. Verdikt rozeti pasaporttan okunur — uydurulmaz

Pasaport künyelerine `gostergeler:` eşlemesi eklendi:

```yaml
gostergeler:
  golden_zone: "Golden Zone"
  golden_zone_r2: "Golden Zone · 2R"
```

`tools/pasaport.py dogrula` artık **katalogdaki her göstergenin tam bir
pasaport tarafından sahiplenildiğini** denetliyor. Sahipsiz gösterge =
arayüzde rozetsiz satır; iki kez sahiplenilmiş gösterge = hangi verdiktin
gösterileceği belirsiz. İkisi de bulgu üretir.

Dışa aktarım, haritada olmayan bir gösterge görürse **durur** — rozetsiz satır
üretmektense gürültülü biçimde patlamak yeğdir.

### 4. Elimizde olmayan alan doldurulmaz

Maket satırlarda `ad: "Türk Hava Yolları"` vardı. Evren dosyasında sembol var,
şirket adı yok; başka bir kaynağımız da yok. **Alan kaldırıldı.** Olmayan bir
alanı doldurmak, maket veriyi gerçek diye sunmanın başka bir biçimidir.

### 5. Sessiz kırpma yasak

Satır sınırı yüzünden JSON'a girmeyen sinyal sayısı (`kesilen`) ve fiyat
serisi okunamadığı için atlanan sinyal sayısı (`veriYok`) künyeye yazılır ve
arayüzün altında gösterilir.

### 6. Sayaçlar sayılır, yazılmaz

`lib/yollar.ts`'te elle yazılı olan `sayac: "47"`, `Yapı 4 · Formasyon 3 ·
Trend 2` ve `Takip listem 21` kaldırıldı. Tarama sayacı gerçek koşudan, paket
sayaçları strateji kayıt defterinden geliyor. **"Takip listem" tamamen
kaldırıldı** — öyle bir özellik yok; olmayan bir yüzeye sayaçlı bağlantı
koymak maket satır göstermenin başka bir biçimiydi.

Giriş ekranındaki olgu şeridi de düzeltildi: "4S + 1G zaman dilimi"
taranmayan bir zaman dilimini sayıyordu, "586 sembolde OOS ölçümü" ise veri
düzeltmesinden önceki evrendi.

### 7 · Yalnız taranacak zaman diliminin ham verisi çekilir

İlk tam koşu 50 dakikada hâlâ veri çekiyordu. Sebep `run_eod`'daydı: taranan
zaman dilimi ne olursa olsun her koşuda **H1 + D1** çekiliyordu. 4S H1'den
türetilir, W1 D1'den; yalnız 1G tarayan bir koşu H1'i **hiç** kullanmıyor.
648 sembolde H1 saf israftı.

`run_eod` artık taranacak zaman dilimlerinin dayandığı ham veriyi çekiyor.
Aynı iş **15 dk 44 sn**'ye indi.

## İlk gerçek koşu — `bist_2026-09-16`

| | |
|---|---|
| Evren | 648 sembol · **gerçekten taranan 625** |
| Zaman dilimi | 1G |
| Süre | 15 dk 44 sn (veri güncelleme dahil) |
| Gösterge işi | 3891 |
| Yazılan sinyal | 28 673 · **güncel durum 2656** |
| Repaint alarmı | yok |

Gösterge başına güncel sinyal:

| gösterge | sinyal |
|---|---|
| `golden_zone` / `golden_zone_r2` | 615 / 615 |
| `harmonik_abcd` | 531 |
| `kesitsel_donus` | 283 |
| `kesitsel_momentum_12_1` | 234 |
| `kesitsel_momentum` | 220 |
| `harmonik_uc_surus` · `gartley` · `kelebek` | 66 · 50 · 42 |

**207 tarama hatası = 23 verisiz sembol × 9 gösterge.** Kayıp değil, aynı 23
sembol; `data_quality` tablosunda adlarıyla duruyor ve arayüzün künyesinde
tek tek yazılı. Koşu raporu yalnız `n_errors: 207` diyordu — o sayı gösterge
başına çarpılmış hâli ve tek başına yanıltıcı; `ResultsStore.data_quality_summary`
bu yüzden eklendi.

## Sonuçlar

**İyi:** Harmoniklerin K6 kapısındaki "tarama kolonu" gerekçesi ortadan
kalktı ve **kapı 2026-09-17'de kapandı** — projenin K6'ya ulaşan ilk
stratejisi. Tarama yüzeyi artık gerçek çıktı gösteriyor ve her satırın rozeti
denetlenen bir eşlemeden geliyor.

**Bedeli:** İki tane.

1. Veri günde bir kere tazeleniyor; kullanıcı gün içinde koşmuş bir tarama
   göremez. Kabul edilen bedel — tarama zaten gün sonu taramasıdır.
2. `tarama-verisi.json` **~980 KB** ve depoya giriyor (derleme onu okuyor).
   Fiyat serisi satıra değil sembole bağlanarak (2656 satır → 616 seri) ve
   girintisiz yazılarak küçültüldü, ama hâlâ büyük. **Her günün koşusu
   commit'lenirse depo şişer**; bu dosya ürün sürümlerinde tazelenmeli,
   her gün değil.

**Açık kalan:** Strateji kütüphanesi (`lib/ornek-strateji.ts`) hâlâ üç kayıt
taşıyor; `golden-zone` ve `kesitsel-momentum` pasaportları var ama kütüphanede
yok. Tarama tablosunda görünüp kütüphanede görünmeyen strateji bir tutarsızlık
— ayrı bir iş olarak duruyor.
