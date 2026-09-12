---
# ── Makine tarafından okunan künye ────────────────────────────────────────
# `python tools/pasaport.py dogrula` bu bloğu denetler. Elle "geçti" yazmak
# yetmez: her kapının kanıtı DİSKTE bulunmak zorundadır.
slug: ornek-strateji            # dosya adıyla aynı, küçük harf, tireli
ad: Örnek Strateji              # kullanıcıya görünen ad
paket: yapi                     # yapi | formasyon | trend | arbitraj
referans: ""                    # references/ altındaki hedef görsel (K5 için)

# K4'ün çıktısı. Kapı AÇILMADAN "ölçülmedi" dışında bir değer yazılamaz.
#   olculmedi     — K4 açılmadı, elimizde sayı yok
#   kanitlanmadi  — ölçüldü, FDR sonrası kenar bulunamadı
#   izlenen-aday  — ölçüldü, en az çürütülmüş grupta
#   kenar-var     — ölçüldü, FDR eşiğini geçti
verdikt: olculmedi

kapilar:
  K0: { gecildi: null, kanit: [] }
  K1: { gecildi: null, kanit: [] }
  K2: { gecildi: null, kanit: [] }
  K3: { gecildi: null, kanit: [] }
  K4: { gecildi: null, kanit: [] }
  K5: { gecildi: null, kanit: [], onay: null }
  K6: { gecildi: null, kanit: [] }
---

# Örnek Strateji — Strateji Pasaportu

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
| **Ne yapar** | *(bir cümle — kullanıcıya görünecek özet)* |
| **Zaman dilimleri** | *(4S · 1G gibi)* |
| **Yön** | *(alış / satış / iki yönlü)* |
| **Referans görsel** | *(`references/…png` — K5'in hedefi)* |
| **Verdikt** | *(K4 çıktısı; açılmadıysa "ölçülmedi")* |

---

## K0 · Kaynak

> **Bitti kriteri:** kuralın geldiği kitap/makale, **sayfa numarasıyla**; tüm
> eşikler alıntılanmış. **Ezberden sayı yazmak yasak.**
>
> ADR-002: K0 bir formalite değil, **stratejinin doğduğu yer**. Eski koda
> bakılabilir ama referans olarak değil, yalnızca karşılaştırma için — ve
> farklılık çıkarsa **kitap kazanır**.

### Birincil kaynak

| | |
|---|---|
| Eser | *(yazar, kitap/makale adı, baskı)* |
| Yer | *(sayfa / bölüm)* |
| Dosya | *(depodaki yolu — `Quant Playbook/books/…`, `bilgi-bankasi/teknik/…`)* |

### Kuralın kendi cümleleriyle alıntısı

> *(kitaptan birebir alıntı — parafraz değil)*

### Eşikler

Her satırın **kaynağı** dolu olmalı. İki geçerli kaynak türü var:
kitaptan **alıntı** (sayfa numarasıyla) ya da **K3 ölçümü** (o zaman K3'ün
ölçüm dosyası gösterilir). Üçüncü bir tür yok.

| Eşik | Değer | Kaynak |
|---|---|---|
| *(parametre adı)* | *(değer)* | *(s.NN alıntısı **veya** `K3: docs/olcum/…md`)* |

### Kitaptan sapmalar

*(Kitapta olmayan ya da kitaptan farklı yaptığımız her şey — gerekçesiyle.
Yoksa "yok" yaz, boş bırakma.)*

---

## K1 · Sözleşme

> **Bitti kriteri:** tipli sonuç dataclass'ı, parametreler (frozen), durum
> makinesi, non-repaint gerekçesi yazılı.

### Parametreler

`packages/teknik/quaxis/teknik/indicators/<…>/params.py` — `frozen dataclass`,
sonuç kaydı `params_hash` taşır. Aynı veri + aynı parametre = bit bit aynı
sonuç.

| Alan | Tip | Varsayılan | Düz Türkçe açıklama |
|---|---|---|---|
| | | | |

### Durum makinesi

*(pending → confirmed → invalidated … Hangi olay hangi geçişi tetikler?)*

### Non-repaint gerekçesi

*(Sinyal neden **onaylandığı barın** tarihini taşır? Pivot kaç bar sonra
kesinleşir? Açık bar neden sinyal üretemez? Bu bölüm, K2'deki walk-forward
testinin neyi kanıtlaması gerektiğini tarif eder.)*

---

## K2 · Dedektör

> **Bitti kriteri:** kod + birim testler + **walk-forward repaint testi** +
> lookahead lint temiz.

| | |
|---|---|
| Kod | *(dosya yolu)* |
| Testler | *(test dosyası yolu)* |
| Repaint testi | *(`repaint_test` ile mi, `register_verified_elsewhere` ile mi? İkincisiyse **neden** generic teste giremediği burada yazılı olmak zorunda.)* |
| Lookahead lint | *(temiz / bulgular)* |

---

## K3 · Kalibrasyon

> **Bitti kriteri:** tam **648 sembollük** evrende aday sayısı ölçülmüş.
> Sıfıra yakınsa bozuk, on binlerse çok gevşek. Ölçüm dosyası `docs/olcum/`
> altında.

| | |
|---|---|
| Ölçüm dosyası | `docs/olcum/<slug>-K3-<tarih>.md` |
| Evren | *(kaç sembol)* |
| Aday sayısı | *(sembol başına ortalama + toplam)* |
| Aday üretmeyen sembol | *(kaç tanesi sıfır aday verdi — hepsi sıfırsa gösterge bozuktur)* |
| Sonuç | *(eşikler oturdu mu, hangi parametre değiştirildi)* |

> Önceki projede `breakout_fvg` ve `flag_pennant` 4S'te **648/648 sembolde
> sıfır aday** veriyordu ve bu ancak çok sonra fark edildi. K3 bunun içindir.

---

## K4 · İstatistik

> **Bitti kriteri:** **sembol-kümelenmiş** ileri getiri testi, IS/OOS ayrımı,
> permütasyon + BH-FDR. Sonuç dürüstçe yazılır: *kenar var / yok / belirsiz*.
> **Elenmez — etiketlenir.**

| | |
|---|---|
| Ölçüm dosyası | `docs/olcum/<slug>-K4-<tarih>.md` |
| Evren | *(kaç sembol)* |
| Bağımsız gözlem | *(kaç sembol — bar değil, SEMBOL)* |
| Pencere | *(IS/OOS oranı)* |
| Ufuk | *(kaç bar ileri)* |
| Adil baza karşı fark | *(%)* |
| Permütasyon p değeri | |
| BH-FDR (q=0.05) | *(geçti / geçemedi)* |
| **Verdikt** | *(künyedeki `verdikt` alanıyla AYNI olmalı)* |

### R-katsayısı (üç bariyer)

> **Strateji bir stop ve hedef bildiriyorsa bu tablo ZORUNLUDUR.** İleri getiri
> asimetriyi göremez: %35 isabetle 3R kazandıran bir sistem 20 barlık ileri
> getiride sıfır görünür. ICT/SMC kavramlarını "kenar yok" diye bulan en geniş
> çalışma (648 backtest) tam olarak bu hatayı yaptı — zaman bazlı çıkış kullandı,
> stop/hedef koymadı. Aynı barda iki bariyer de vurulduysa **stop** sayılır.

| | |
|---|---|
| İşlem sayısı | *(kaç işlem / kaç sembol)* |
| İsabet | *(%)* |
| **İşlem başına beklenen R** | |
| Adil baz (aynı risk, rastgele bar) | |
| Stop / hedef / zaman çıkış oranı | |
| Permütasyon p değeri | |
| **Verdikt (R)** | |

### Ne çıkarsa o

*(Sonuç olumsuzsa da burada aynı açıklıkla yazılır. "Zarar ettiriyor" ile
"işe yaradığına dair kanıt yok" farklı şeylerdir — hangisi olduğunu yaz.)*

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
