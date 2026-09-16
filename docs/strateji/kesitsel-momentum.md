---
# ── Makine tarafından okunan künye ────────────────────────────────────────
# `python tools/pasaport.py dogrula` bu bloğu denetler. Elle "geçti" yazmak
# yetmez: her kapının kanıtı DİSKTE bulunmak zorundadır.
slug: kesitsel-momentum            # dosya adıyla aynı, küçük harf, tireli
ad: Kesitsel Momentum              # kullanıcıya görünen ad
paket: trend                     # yapi | formasyon | trend | arbitraj
referans: ""                    # references/ altındaki hedef görsel (K5 için)

# K4'ün çıktısı. Kapı AÇILMADAN "ölçülmedi" dışında bir değer yazılamaz.
#   olculmedi     — K4 açılmadı, elimizde sayı yok
#   kanitlanmadi  — ölçüldü, FDR sonrası kenar bulunamadı
#   izlenen-aday  — ölçüldü, en az çürütülmüş grupta
#   kenar-var     — ölçüldü, FDR eşiğini geçti
verdikt: kanitlanmadi

durum: durduruldu
durdurma_gerekcesi: >
  Momentum ust %10, rastgele hisseye gore -%9.98 geride (p=1.0000, 163
  sembol). 12-1 varyanti da ayni yonde (-%7.96). Ters hipotez (alt %10)
  ON KAYITLA sinandi ve REDDEDILDI: IS -%0.95 (p=0.57), OOS -%0.25
  (p=0.51). Etki simetrik degil -- kaybedenler rastgeleden ayirt
  edilemiyor, kazananlar geride. Sonuc bir strateji degil bir FILTRE
  hipotezi uretti ve o kendi on kaydini bekliyor.
  Ozet: docs/olcum/onkayit-kesitsel-donus.md

kapilar:
  K0: { gecildi: 2026-09-13, kanit: ["docs/strateji/kaynak/kesitsel-momentum-K0.md", "docs/olcum/kesitsel-momentum-K3K4-1D-2026-09-13.md"] }
  K1: { gecildi: 2026-09-13, kanit: ["packages/teknik/quaxis/teknik/indicators/kesitsel_momentum/parametreler.py"] }
  K2: { gecildi: 2026-09-13, kanit: ["packages/teknik/quaxis/teknik/indicators/kesitsel_momentum/dedektor.py", "packages/teknik/tests/test_kesitsel_momentum.py"] }
  K3: { gecildi: 2026-09-13, kanit: ["docs/olcum/kesitsel-momentum-K3K4-1D-2026-09-13.md"] }
  K4: { gecildi: 2026-09-13, kanit: ["docs/olcum/kesitsel-momentum-K3K4-1D-oos-2026-09-17.md", "docs/olcum/kesitsel-momentum_12_1-K3K4-1D-oos-2026-09-17.md", "docs/olcum/kesitsel-momentum-K3K4-1D-2026-09-13.md", "docs/olcum/kesitsel-momentum_12_1-K3K4-1D-2026-09-13.md"] }
  K5: { gecildi: null, kanit: [], onay: null }
  K6: { gecildi: null, kanit: [] }
---

# Kesitsel Momentum — Strateji Pasaportu

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
| **Ne yapar** | Evrendeki hisseleri son 12 ayın getirisine göre sıralar, üst dilimi alır ve 1 ay tutar. |
| **Zaman dilimleri** | 1G |
| **Yön** | **Yalnız alış** — BIST'te açığa satış kısıtlı (kullanıcı kararı, 2026-09-13) |
| **Referans görsel** | yok — bu bir grafik kurulumu değil, kesitsel sıralama |
| **Verdikt** | **kanıtlanmadı** — ve güçlü biçimde TERS yönde (−%9.98) |
| **Durum** | ⏸ durduruldu (2026-09-13) — ters hipotez de ön kayıtla reddedildi |
| **Ters varyant** | `kesitsel_donus` — [`onkayit-kesitsel-donus.md`](../olcum/onkayit-kesitsel-donus.md): REDDEDİLDİ |

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

Tam kaynak dosyası: [`kaynak/kesitsel-momentum-K0.md`](kaynak/kesitsel-momentum-K0.md)

> **K0 K3 ölçüldükten sonra kapandı.** Likidite eşiği ölçümden türetildi:
> kalibrasyon MAKUL çıktığı için filtreye gerek kalmadı (0 = kapalı).
>
> Eski not: Kuralın kendisi ve üç eşiği kaynaktan
> sayfa numarasıyla geliyor; ama likidite eşiği kaynakta YOK ve ölçümden
> türetilecek. `pasaport.py dogrula` o dosyayı diskte arayıp bulamadıkça
> bulgu yazar — bu bir hata değil, kapının kendisi.

| Eşik | Değer | Kaynak |
|---|---|---|
| geriye_bakis | 252 gün | s.146 kod: `lookback=252` |
| tutus | 25 gün | s.146 kod: `holddays=25` |
| ust_dilim | %10 | s.146 kod: `topN=50` (500 hisseden) |
| atlama_ay | 0 ve 1 (ikisi de ölçülecek) | s.146 atlamıyor; literatür "12-1" kullanır — karar K3'e |
| asgari_ciro | 0 (filtre kapalı) | `K3: docs/olcum/kesitsel-momentum-K3K4-1D-2026-09-13.md` — kalibrasyon MAKUL çıktı, sembollerin %0'ı sıfır sinyal verdi; filtreye gerek kalmadı |
| asgari_evren | 20 | `K3: docs/olcum/kesitsel-momentum-K3K4-1D-2026-09-13.md` — ölçüm sırasında bulundu: tek sembollü barda sıralama yapılıyordu |

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

> **Yenilendi 2026-09-17.** Ölçüm zemininde gerçek veri kusurları bulundu
> ([`veri-denetimi-bist-1D.md`](../olcum/veri-denetimi-bist-1D.md)), ön
> kayıtla düzeltildi
> ([`onkayit-veri-duzeltme.md`](../olcum/onkayit-veri-duzeltme.md)) ve K4
> **bir kez** yeniden koşuldu. **Verdikt değişmedi.** Aşağıdaki tablo
> yenilenmiş ölçümündür; 13 Eylül tablosu dosyasında duruyor.

| | |
|---|---|
| Ölçüm dosyaları | [`kesitsel-momentum-K3K4-1D-oos`](../olcum/kesitsel-momentum-K3K4-1D-oos-2026-09-17.md) · [`kesitsel-momentum_12_1-K3K4-1D-oos`](../olcum/kesitsel-momentum_12_1-K3K4-1D-oos-2026-09-17.md) |
| Evren | 625 BIST sembolü taranıyor; **221**'i en az bir sinyal verdi |
| Bağımsız gözlem | **200 sembol** — bar değil, SEMBOL |
| Pencere | ilk %70 IS / son %30 OOS; ölçüm yalnız **OOS** |
| Ufuk | 25 bar (stratejinin kendi tutuş süresi — araç uydurmadı) |
| Sinyal getirisi | **%+0.20** |
| Adil baz (rastgele sembol) | **%+9.82** |
| Adil baza karşı fark | **%−9.62** — negatif |
| Permütasyon p değeri | **1.0000** (2000 tur) |
| BH-FDR (q=0.05) | uygulanmadı — ham p boş dağılımın en alt ucunda |
| **Verdikt** | **kanitlanmadi** |

### R-katsayısı (üç bariyer) — bu stratejide YOK, sebebiyle

> **Strateji bir stop ve hedef bildiriyorsa bu tablo ZORUNLUDUR.**

Kesitsel momentumda **stop yok**: pozisyon `tutus` bar tutulur ve kapanır
(Chan s.146). Zorla bir stop uydurmak stratejiyi değiştirmek olurdu; o
yüzden ölçüt üç bariyerli R değil, stratejinin kendi tutuş süresi kadar
**ufuk getirisi**dir. Bu bir atlama değil, sözleşmenin sonucu — ve ayrı bir
koşucuyla (`tools/momentum_olcum.py`) uygulanır.

### Son ayı atlamak (12-1) düzeltmiyor

| | ana varyant | 12-1 varyantı |
|---|---|---|
| Bağımsız gözlem | 200 | 220 |
| Sinyal getirisi | %+0.20 | %+1.75 |
| Adil baz | %+9.82 | %+9.14 |
| **Fark** | **%−9.62** | **%−7.39** |
| p | 1.0000 | 1.0000 |

Akademik standart olan "son ayı atla" varyantı farkı yumuşatıyor, **yönünü
değiştirmiyor**.

### Düzeltme öncesi/sonrası

Karşılaştırma temiz: 13 Eylül'ün ölçümü de işlem maliyetini içeriyordu,
araç değişmedi. Değişen tek şey hangi barların ve sembollerin gözlem
sayıldığı.

| | Önce (09-13) | Sonra (09-17) |
|---|---|---|
| Bağımsız gözlem | 163 | **200** |
| Fark | %−9.98 | **%−9.62** |
| p | 1.0000 | **1.0000** |

### Ne çıkarsa o

**Momentum kenar üretmedi — üstelik güçlü biçimde TERS yönde.** Bu "işe
yaradığına dair kanıt yok" değil; **ters yönde net bir fark var**: p=1.0000,
gözlenen fark boş dağılımın en alt ucunda.

Son 12 ayın en çok kazanan %10'unu alıp 25 gün tutmak, aynı dönemde
rastgele bir hisse almanın 9.6 puan gerisinde kaldı. Kaynağın kendi uyarısı
(Chan s.152 — momentum 2008–2009 sonrası kayboldu, yerini ortalamaya dönüşe
bıraktı) BIST'te birebir gerçekleşiyor.

Ön kayıt §5'in birinci maddesi (*fark pozitif*) sağlanmadığı için ikinci ve
üçüncü maddeye bakılmadı.

**Ters varyant ayrı bir hipotezdir.** "Tersini yap" demek sonuca bakıp yön
çevirmek olurdu; o yüzden `kesitsel_donus` kendi ön kaydıyla ölçüldü ve
**reddedildi**: [`onkayit-kesitsel-donus.md`](../olcum/onkayit-kesitsel-donus.md).
Bu turda ona dokunulmadı.

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
