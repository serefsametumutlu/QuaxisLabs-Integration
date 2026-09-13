---
# ── Makine tarafından okunan künye ────────────────────────────────────────
slug: harmonik-pesavento
ad: Harmonik Formasyonlar (Pesavento)
paket: formasyon
referans: ""

verdikt: olculmedi

durum: aktif

kapilar:
  K0: { gecildi: 2026-09-13, kanit: ["docs/strateji/kaynak/harmonik-pesavento-K0.md"] }
  K1: { gecildi: 2026-09-13, kanit: ["packages/teknik/quaxis/teknik/indicators/harmonik/parametreler.py"] }
  K2: { gecildi: 2026-09-13, kanit: ["packages/teknik/quaxis/teknik/indicators/harmonik/dedektor.py", "packages/teknik/quaxis/teknik/indicators/harmonik/pivotlar.py", "packages/teknik/tests/test_harmonik.py"] }
  K3: { gecildi: null, kanit: [] }
  K4: { gecildi: null, kanit: [] }
  K5: { gecildi: null, kanit: [], onay: null }
  K6: { gecildi: null, kanit: [] }
---

# Harmonik Formasyonlar (Pesavento) — Strateji Pasaportu

> **Bu dosya stratejinin kimliğidir.** Kod, ölçüm ve görsel onay buraya
> bağlanır. Bir kapı geçilmeden sonraki açılmaz.

---

## Bir bakışta

| | |
|---|---|
| **Ne yapar** | Almaşık salınım uçlarından Fibonacci oranlarına uyan bir zincir bulur, `D` diye bir fiyat hedefi hesaplar ve fiyat o seviyeye **dokunduğu anda** sinyal üretir. |
| **Zaman dilimleri** | 4S · 1G · 1H |
| **Yön** | Boğa ve ayı kurulumu da üretilir. Ayı tarafı BIST'te işleme çevrilemez (açığa satış kısıtlı) ama **ölçüm nesnesi** olarak tutulur. |
| **Referans görsel** | henüz yok (K5) |
| **Verdikt** | **ölçülmedi** — K3/K4 açılmadı |
| **Durum** | aktif |

### Aile dört üyeden oluşuyor — ve dördü AYRI ölçülecek

| # | Formasyon | Künye | Nokta | D nerede |
|---|---|---|---|---|
| 1 | AB=CD | `harmonik_abcd` | A·B·C | C'den AB×1.0 kadar öteye |
| 2 | Gartley "222" | `harmonik_gartley` | X·A·B·C | XA'nın .786 geri çekilmesi |
| 3 | Butterfly | `harmonik_kelebek` | X·A·B·C | XA'nın 1.272 uzantısı (X'i AŞAR) |
| 4 | Three Drives | `harmonik_uc_surus` | O·S1·A·S2·C | C'den, son bacağın 1.272 uzantısı |

Tek bir "harmonik" künyesi altında toplanmadılar. Sorulan soru
"harmonikler çalışıyor mu" **değil**, "**hangisi** çalışıyor mu". Tek künye
altında ölçülselerdi birinin kenarı diğerinin gürültüsüyle ortalanır ve
ikisi de görünmez olurdu.

**Dört test = BH-FDR zorunlu.**

### Kalan dört ekol bu turda YOK

Bat · Crab · Shark (Carney), Cypher (Oglesbee), 5-0 (Duddella) **bu kitapta
geçmiyor**. Kaynağı olmayan bir formasyonu bu kitabın altına yazmak K0'ın
tek kuralını çiğnerdi. Kullanıcı kararı (2026-09-13): önce bu dört, sonra
diğer dört — toplam sekiz.

---

## K0 · Kaynak

### Birincil kaynak

| | |
|---|---|
| Eser | Larry Pesavento & Leslie Jouflas, *Trade What You See: How to Profit from Pattern Recognition* (Wiley, 2007) |
| Yer | Böl. 4–7 (formasyonlar), Böl. 11 (uyarı/teyit işaretleri) |
| Dosya | `Temel Analiz/bilanco-radar/bilgi-bankasi/teknik/10_pesavento_twys.md` |

Tam kaynak dosyası:
[`kaynak/harmonik-pesavento-K0.md`](kaynak/harmonik-pesavento-K0.md)

### Eşikler

| Eşik | Değer | Kaynak |
|---|---|---|
| geri çekilme kümesi | .382 · .50 · .618 · .786 | `K0: docs/strateji/kaynak/harmonik-pesavento-K0.md#ESIK-GERI-CEKILME` |
| uzantı kümesi | 1.0 · 1.272 · 1.618 · 2.0 | `K0: docs/strateji/kaynak/harmonik-pesavento-K0.md#ESIK-UZANTI` |
| hedef | AD salınımının .618'i | `K0: docs/strateji/kaynak/harmonik-pesavento-K0.md#ESIK-HEDEF` |
| içerideki AB=CD oranı | CD/AB ∈ {1.0, 1.272, 1.618, 2.0} | `K0: docs/strateji/kaynak/harmonik-pesavento-K0.md#ESIK-ABCD-ICERIDE` |
| AB=CD · BC ve CD oranları | BC<1 · CD/AB=1.0 | `K0: docs/strateji/kaynak/harmonik-pesavento-K0.md#FORMASYON-01` |
| Gartley D · stop | .786 XA · X'in ötesi | `K0: docs/strateji/kaynak/harmonik-pesavento-K0.md#FORMASYON-02` |
| Kelebek D · stop · azami | 1.272 · 1.618 · 2.618 | `K0: docs/strateji/kaynak/harmonik-pesavento-K0.md#FORMASYON-03` |
| Three Drives sürüş uzantısı | 1.272 | `K0: docs/strateji/kaynak/harmonik-pesavento-K0.md#FORMASYON-04` |
| **tolerans** | 0.05 | `K3: docs/olcum/harmonik-pesavento-K3-1D.md` — **kitapta yok**, ölçümden türetilecek |
| **donus_max_bar** | 40 | `K3: docs/olcum/harmonik-pesavento-K3-1D.md` — **kitapta yok** |
| **pivot kolları** | 3 / 3 | `K3: docs/olcum/harmonik-pesavento-K3-1D.md` — **kitapta yok**; şimdilik Golden Zone ile aynı |
| **AB=CD stop oranı** | 1.272 | `K3: docs/olcum/harmonik-pesavento-K3-1D.md` — kitap formül vermiyor; başlangıç noktası |

> Sayfa numarası neden yok: kaynak çıkarımında sayfa numarası bulunmuyor,
> bölüm kimlikleri var. `s.123` yazmak uydurma olurdu. Çıpalar `pasaport.py`
> tarafından **diskte açılıp aranarak** doğrulanıyor — bkz.
> [`K0 §7`](kaynak/harmonik-pesavento-K0.md).
>
> Son dört satır `K3:` bekliyor ve o dosya doğana kadar `pasaport.py dogrula`
> **bulgu yazmaya devam edecek.** Kapı açıkken kapalı görünmesin diye.

### Kitaptan sapmalar

| Sapma | Gerekçe |
|---|---|
| Kademeli çıkış yok | Tek stop, tek hedef. Kademeli çıkış R dağılımını iyimser gösterir (Golden Zone'da aynı karar). |
| "Shaded" limit emir yok | Tam seviyeden dolum varsayılıyor; kayma işlem maliyetine yazılıyor. |
| KURAL-30 (1 bar bekleme) dedektöre girmedi | Kitap "uyarı işareti varsa bekle" diyor ama "büyük gap"/"geniş bar" için **eşik vermiyor**. İşaretler payload'a **sayı** olarak yazılıyor; bekleme tekniği K4'te ön kayıtla sınanacak. |
| Three Drives'a `O` noktası eklendi | Kitap "A geri çekilmesi" derken bir önceki bacağa göre ölçüyor; o bacağın başlangıcı olmadan oran hesaplanamazdı. |
| Three Drives dahil edildi | Önceki projede Pesavento ekolüne kodlanmamıştı. Kitapta var. |

---

## K1 · Sözleşme

### Parametreler

`packages/teknik/quaxis/teknik/indicators/harmonik/parametreler.py` —
`frozen dataclass`, sonuç `params_hash` taşır.

| Alan | Varsayılan | Düz Türkçe |
|---|---|---|
| `pivot_sol` / `pivot_sag` | 3 / 3 | Bir salınım ucunun solunda/sağında kaç bar olmalı |
| `tolerans` | 0.05 | Bir oranın "tuttu" sayılması için izin verilen sapma |
| `geri_cekilme_oranlari` | .382/.50/.618/.786 | Geri çekilme bacaklarının uyacağı oranlar |
| `donus_max_bar` | 40 | D'ye dokunmak için tanınan azami süre |
| `hedef_orani` | 0.618 | Hedef, AD salınımının bu kadarını geri çeker |
| `stop_tamponu` | 0.0 | Stop seviyesinin ne kadar ötesine konur |
| `zaman_bariyeri` | 40 | Üç bariyerli ölçümün zaman bariyeri |
| `cd_orani` (AB=CD) | 1.0 | CD bacağının AB'ye oranı — D'yi belirler |
| `stop_orani` (AB=CD) | 1.272 | Stop'un CD/AB oranı |
| `d_geri_cekilme` (Gartley) | 0.786 | D, XA'nın bu kadarını geri çeker |
| `abcd_sarti` | True | İçeride AB=CD aranıyor mu |
| `d_uzanti` / `stop_uzanti` (Kelebek) | 1.272 / 1.618 | Giriş ve stop uzantıları |
| `surus_uzanti` / `stop_uzanti` (Three Drives) | 1.272 / 1.618 | Sürüş ve stop uzantıları |

`donus_max_bar` ve `zaman_bariyeri` **takvimsel** sürelerdir; `_BAR_FIELDS`
üzerinden zaman dilimine göre ölçeklenir (4S'te 120 bar, 1H'de 8).

### Durum makinesi

```
pivot zinciri değişti
        │
        ├─ oranlar tutmuyor ─────────────► (kurulum yok)
        │
        └─ tutuyor → KURULUM (D hesaplandı)
                        │
                        ├─ D, C'nin onayından ÖNCE vurulmuş ──► açılmaz
                        ├─ C'nin ötesinde gövde kapanışı ─────► geçersiz
                        ├─ donus_max_bar doldu ───────────────► süresi doldu
                        └─ fiyat D'ye dokundu ────────────────► SİNYAL (confirmed)
```

### Non-repaint gerekçesi

Üç ayrı savunma var:

1. **Pivotlar onay barında kullanılır.** Bir uç, sağındaki `pivot_sag` bar
   kapanmadan bilinemez (`Pivot.onay_i`).
2. **D bir pivot değil, hesaplanmış bir fiyattır.** Harmonik dedektörlerin
   klasik repaint kaynağı D'yi "sonradan oluşmuş bir dip" olarak aramaktır;
   öyle arandığında D ancak birkaç bar sonra bilinir ve grafiğe geriye
   dönük çizilir.
3. **C'nin onayına kadar geçen barlarda D vurulduysa kurulum AÇILMAZ.** O
   aralıkta formasyonun varlığını bilmiyorduk; dokunuşu sinyal saymak
   gerçekte verilemeyecek bir emri ölçüme eklemek olurdu.

Bu yüzden `bar_time` (C'nin barı) ile `detected_at` (D'ye dokunulan bar)
**farklıdır** ve fark kaydedilir.

---

## K2 · Dedektör

| | |
|---|---|
| Kod | [`indicators/harmonik/dedektor.py`](../../packages/teknik/quaxis/teknik/indicators/harmonik/dedektor.py) · [`pivotlar.py`](../../packages/teknik/quaxis/teknik/indicators/harmonik/pivotlar.py) |
| Testler | [`tests/test_harmonik.py`](../../packages/teknik/tests/test_harmonik.py) — 41 test |
| Repaint testi | **İkisi de:** jenerik `repaint_test` (katalog kaydı sırasında) **ve** hedefli walk-forward testi (seri 7 barlık adımlarla kesilip sinyaller birebir karşılaştırılıyor) |
| Lookahead lint | temiz |

### Testlerin kilitlediği şeyler

* Dört formasyonun her biri, kitabın oranlarıyla kurulmuş sentetik bir
  "ders kitabı" örneğinde **tam olarak bir kez** bulunuyor.
* Fiyat serisi aynalanınca aynı formasyon **ters yönde** ve seviyeleri
  birebir aynalanmış olarak bulunuyor (x-uzayı dönüşümünün kilidi).
* Boğada `stop < giriş < hedef` — Golden Zone'da riski sıfırlayıp +48R
  baz üreten hatanın kilidi.
* Aynı pivot dizisinden ikinci bir kurulum doğmuyor.
* Tolerans daraldıkça sinyal sayısı azalıyor (monotonluk) — "toleransı
  ölçümle seç" kararının anlamlı olması bunu gerektiriyor.

---

## K3 · Kalibrasyon

> **Bitti kriteri:** tam BIST evreninde aday sayısı ölçülmüş. Sıfıra yakınsa
> bozuk, on binlerse çok gevşek.

| | |
|---|---|
| Ölçüm dosyası | *(bekliyor)* |
| Evren | 545 BIST sembolü, 1G |
| Aday sayısı | *(bekliyor)* |
| Sonuç | *(bekliyor)* |

**K3'ün burada cevaplaması gereken iki özel soru var:**

1. `tolerans` kaç olmalı? Kitap vermiyor; sinyal sayısının toleransa göre
   nasıl değiştiği ölçülüp karar verilecek.
2. Gartley'in AB bacağı gerçekten **.49–.65 bandında** mı yoğunlaşıyor?
   Kitabın iki kuralı (D=.786 XA + içeride AB=CD) bu bandı matematiksel
   olarak dayatıyor (bkz. K0 §3.1). Ölçüm bandın dışında yoğunluk
   gösterirse kurallar birbiriyle çelişiyor demektir.

---

## K4 · İstatistik

> **Bitti kriteri:** sembol-kümelenmiş test, IS/OOS, permütasyon + BH-FDR.

| Formasyon | İşlem | Sembol | İsabet | Beklenen R | Adil baz | p | FDR |
|---|---|---|---|---|---|---|---|
| `harmonik_abcd` | | | | | | | |
| `harmonik_gartley` | | | | | | | |
| `harmonik_kelebek` | | | | | | | |
| `harmonik_uc_surus` | | | | | | | |

### Baştan yazılan beklenti

Önceki projenin ölçümünde `harmonic.carney` **−%3.66 (n=68)** ile negatif
taraftaydı. O ölçüm bu makineyle yapılmadı, n çok küçük ve formasyonların
nasıl kodlandığı bilinmiyor — **kanıt değil**. Ama harmoniklerin önceki
turda üstte değil altta çıktığı bir gerçek ve bu pasaport onu saklamıyor.

Kitabın Gartley için ~**%70 isabet** iddiası bir **kitap iddiasıdır**.
Ölçeceğimiz tam olarak budur.

### Ne zaman çürütülmüş sayılır

* R, adil bazın altında kalırsa → kenar yok.
* Dört formasyonun hiçbiri BH-FDR'yi geçemezse → aile çürütülmüş sayılır.
* Bir formasyon geçer ama işlem maliyeti eşiğinde sıfırlanırsa →
  uygulanamaz.
* Sembol başına gözlem 30'un altına inerse → sayı yazılır, verdikt yazılmaz
  (Pardo s.295).

---

## K5 · Görsel

| | |
|---|---|
| Komposer | *(bekliyor)* — `packages/chart/quaxis/chart/komposer/harmonik.py` |
| Referans | *(bekliyor)* |
| İterasyonlar | *(bekliyor — en az 3)* |
| Onay | *(kapı KAPALI)* |

Dedektör çizim primitiflerini şimdiden üretiyor: formasyon bacakları
`Line`, her nokta `Marker` (X/A/B/C/D), giriş·stop·hedef `Level`. Hepsi
`start=tespit_t` taşıyor — `start` boş bırakılırsa walk-forward
karşılaştırması seviyeleri "hep vardı" sayar ve sonradan doğan her seviye
repaint görünür.

---

## K6 · Ürün

| | |
|---|---|
| Kütüphane kartı | *(bekliyor)* |
| Strateji sayfası | `/stratejiler/harmonik-pesavento` |
| Tarama kolonu | *(bekliyor)* |
| Alarm kuralı | *(bekliyor)* |

### Nasıl okunur — dört soru

| Soru | Cevap |
|---|---|
| Nereye bak | Birbirini izleyen salınım uçlarını birleştiren zikzağa ve en sağdaki `D` seviyesine. |
| Ne ölçer | Zikzağın bacakları arasındaki oranların Fibonacci sayılarına uyup uymadığını. |
| Sinyal ne zaman doğar | Fiyat `D` seviyesine **dokunduğu anda**. `D` daha önceden hesaplanmıştır; dokunuş beklenen andır. |
| Değerler ne demek | `X/A/B/C` formasyonun köşeleri, `D` giriş seviyesi. Stop ve hedef formasyonun kendi geometrisinden çıkar. |

### Sık sorulanlar

**Sinyal sonradan kaybolur mu?** Hayır. `D` son pivot onaylandığında
hesaplanır ve bir daha değişmez; fiyat ona dokunduğunda sinyal doğar ve
geriye dönük hiçbir nokta kaydırılmaz. Formasyon **oluşmadan önce** de
grafikte görünmez — bekleyen kurulum çizilmez, yalnız tamamlanan çizilir.

**C onaylanmadan fiyat D'ye dokunursa ne olur?** Sinyal **üretilmez**. O
anda formasyonun varlığını bilmiyorduk; kaçan kaçmıştır.
