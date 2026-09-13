---
# ── Makine tarafından okunan künye ────────────────────────────────────────
slug: harmonik-pesavento
ad: Harmonik Formasyonlar (Pesavento)
paket: formasyon
referans: ""

verdikt: kanitlanmadi

durum: durduruldu
durdurma_gerekcesi: >
  Dort formasyon + AB=CD'nin ikinci stop varyanti, bes test, BH-FDR
  (q=0.05): HICBIRI gecemedi. Yalniz alis penceresinde abcd +0.459R
  gorunuyor ama ADIL BAZ da +0.367R -- fark +0.092R, p=0.5612. Iki yon
  birlikte olculunce (ornegin buyusun diye) fark +0.05R'ye ve p=0.36'ya
  dusuyor. Tek yonlu "kar" formasyonun degil, BIST'in yukselis
  surukleyisinin. IS penceresi OOS ile CELISIYOR (abcd IS -0.114R).
  IKINCI DENEME (on kayitli, KURAL-30 teyitli giris) da REDDEDILDI:
  en iyi aday abcd.teyit p=0.0685, duz 0.05 esigini bile gecemedi ve
  etkinin TAMAMI IS penceresinde (IS +0.582R, OOS -0.005R). Teyit
  teknigi isabeti %32.8'den %45.3'e cikariyor ama adil bazdan
  ayrilamiyor. On kayit §7 geregi ucuncu varyant denenmeyecek.
  Ozet: docs/olcum/onkayit-harmonik-teyit.md

kapilar:
  K0: { gecildi: 2026-09-13, kanit: ["docs/strateji/kaynak/harmonik-pesavento-K0.md"] }
  K1: { gecildi: 2026-09-13, kanit: ["packages/teknik/quaxis/teknik/indicators/harmonik/parametreler.py"] }
  K2: { gecildi: 2026-09-13, kanit: ["packages/teknik/quaxis/teknik/indicators/harmonik/dedektor.py", "packages/teknik/quaxis/teknik/indicators/harmonik/pivotlar.py", "packages/teknik/tests/test_harmonik.py"] }
  K3: { gecildi: 2026-09-13, kanit: ["docs/olcum/harmonik-pesavento-K3-1D.md", "docs/olcum/harmonik-pesavento-K3-karar-kurali.md"] }
  K4: { gecildi: 2026-09-13, kanit: ["docs/olcum/harmonik-pesavento-K4-1D-long.md", "docs/olcum/harmonik-pesavento-K4-1D-hepsi.md", "docs/olcum/harmonik-pesavento-K4b-teyit-1D-long.md", "docs/olcum/onkayit-harmonik-teyit.md"] }
  K5: { gecildi: 2026-09-14, kanit: ["docs/design/ui/harmonik-pesavento-abcd-koyu-1440-son.png", "docs/design/ui/harmonik-pesavento-gartley-koyu-1440-son.png", "docs/design/ui/harmonik-pesavento-kelebek-koyu-1440-son.png", "docs/design/ui/harmonik-pesavento-uc-surus-koyu-1440-son.png", "docs/design/ui/README.md"], onay: 2026-09-14 }
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
| **Verdikt** | **kanıtlanmadı** — beş testin beşi de BH-FDR'yi geçemedi |
| **Durum** | ⏸ durduruldu (2026-09-13) |

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
| **tolerans** | abcd .02 · gartley .02 · kelebek .02 · üç sürüş **.05** | `K3: docs/olcum/harmonik-pesavento-K3-1D.md` §1, §7 — kitapta yok, ÖLÇÜLDÜ |
| **donus_max_bar** | 55 · 35 · 60 · 25 | `K3: docs/olcum/harmonik-pesavento-K3-1D.md` §3, §7 — dağılımın %90'lık dilimi |
| **pivot kolları** | abcd **5** · diğerleri 4 | `K3: docs/olcum/harmonik-pesavento-K3-1D.md` §2, §7 — Golden Zone'un 3'ü iki formasyonda üst sınırı aştı |
| **AB=CD stop oranı** | 1.272 | `K4: docs/olcum/harmonik-pesavento-K4-1D-long.md` — **K3'te KAPATILAMAZ**: hangi stop mesafesinin doğru olduğu bir getiri sorusu |

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

| | |
|---|---|
| Ölçüm dosyası | [`harmonik-pesavento-K3-1D.md`](../olcum/harmonik-pesavento-K3-1D.md) |
| Karar kuralı | [`harmonik-pesavento-K3-karar-kurali.md`](../olcum/harmonik-pesavento-K3-karar-kurali.md) — **sonuçlar görülmeden** yazılıp commit edildi |
| Evren | 545 BIST sembolü · 1 437 257 bar · 5 703 sembol-yıl (2010-01-01 → 2026-09-11) |
| Sonuç | Dördü de kalibre edildi; hiçbiri elenmedi |

### Türetilen eşikler

| formasyon | tolerans | pivot kolu | donus_max_bar | sinyal | sembol |
|---|---|---|---|---|---|
| `harmonik_abcd` | 0.02 | **5** | 55 | 6 009 | 506 |
| `harmonik_gartley` | 0.02 | 4 | 35 | 262 | 185 |
| `harmonik_kelebek` | 0.02 | 4 | 60 | 304 | 207 |
| `harmonik_uc_surus` | **0.05** | 4 | 25 | 267 | 199 |

Getiriye **bakılmadı**: karar ölçütü yalnız aday sayısı ve dağılım şekli.
Eşiği getiriye bakarak seçmek, K4'ün ölçeceği şeyi K3'te seçmek olurdu.

### İki taramanın ayrı koştuğu ve bunun nasıl yakalandığı

Tolerans taraması pivot=3 ile, pivot taraması tolerans=0.05 ile koştu.
Seçilen **birleşimler** böylece hiç ölçülmemişti — "tek tek geçmişti"
gerekçesiyle parametreye yazılabilirdi. `--dogrula` bunları ayrıca ölçtü
(rapor §7); dördü de iki sınırı sağladı ve `donus_max_bar` yeniden okundu
(`abcd` 40 → 55, `kelebek` 55 → 60).

### Bulgu: kitabın iki kuralı AB bacağını gerçekten kısıtlıyor

K0 §3.1 cebirsel olarak `AB = r / (k + 1 − BC)` demişti. 2 081 gerçek
Gartley'de ölçülen AB dağılımı:

| AB | pay |
|---|---|
| .382 | %18 |
| .500 | %44 |
| .618 | %38 |
| **.786** | **%0 — hiç görülmedi** |

`.786` sıfır çıkması tesadüf değil, cebirin sonucu: `AB = .786` için
`k = BC` gerekir, ama `k ≥ 1` ve `BC < 1`. **Kitabın kuralları AB=.786'lı
bir Gartley'i imkânsız kılıyor.** Kitap bunu hiçbir yerde yazmıyor.

Kelebek'te tablo terse dönüyor: AB'nin %58'i `.786`. Aynı cebir, farklı
`r` (1.272), farklı çözüm kümesi.

### Bulgu: ayı kurulumu boğadan daha sık

| formasyon | boğa | ayı | boğa oranı |
|---|---|---|---|
| `abcd` | 8 103 | 11 747 | %41 |
| `gartley` | 874 | 1 207 | %42 |
| `kelebek` | 1 014 | 1 184 | %46 |
| `uc_surus` | 197 | 153 | %56 |

BIST nominal olarak yükselen bir piyasa olduğu hâlde **düşüş formasyonları
daha sık oluşuyor.** Bu bir kenar iddiası değil; sinyal sayımı. Ama K4'te
yalnız alış tarafı ölçüleceği için örneklemin yarısından azını
kullanacağımız anlamına geliyor ve bu yazılı olmalı.

## K4 · İstatistik

| | |
|---|---|
| Ölçüm dosyaları | [yalnız alış](../olcum/harmonik-pesavento-K4-1D-long.md) · [iki yön](../olcum/harmonik-pesavento-K4-1D-hepsi.md) |
| Ölçüt | Üç bariyerli R (stop / hedef / zaman), işlem maliyeti dahil |
| Aynı barda stop+hedef | **stop** |
| Bağımsız gözlem | sembol |
| Aile | **5 test**, önceden sabit → BH-FDR (q=0.05) |

### Yalnız alış · OOS (birincil)

| formasyon | işlem | sembol | isabet | beklenen R | **adil baz** | fark | PF | p |
|---|---|---|---|---|---|---|---|---|
| `abcd` stop 1.272 | 622 | 325 | %41.6 | +0.459R | **+0.367R** | +0.092R | 1.80 | 0.5612 |
| `abcd` stop 1.618 | 622 | 325 | %59.3 | +0.317R | **+0.225R** | +0.093R | 2.02 | 0.2619 |
| `gartley` | 29 | 27 | %41.4 | +0.218R | +0.318R | −0.100R | 1.36 | 0.5332 |
| `kelebek` | 21 | 21 | %33.3 | −0.112R | +0.348R | −0.461R | 0.81 | 0.9240 |
| `uc_surus` | 46 | 43 | %32.6 | +0.016R | +0.192R | −0.175R | 1.02 | 0.7051 |

**BH-FDR: beşin beşi de geçemedi.** Gartley ve Kelebek'te OOS sembol sayısı
30'un altında (27 ve 21) — Pardo s.295 gereği o iki satırın **sayısı
yazılır, verdikti yazılmaz**.

### Asıl bulgu: +0.459R'nin ne kadarı formasyonun

`abcd` satırı tek başına iyi bir strateji gibi duruyor: %41.6 isabet,
profit factor 1.80, işlem başına +0.459R. Bu sayı, adil baz olmadan
raporlansaydı "çalışan bir strateji" diye sunulurdu.

**Adil baz +0.367R.** Yani aynı risk yapısıyla (aynı stop mesafesi, aynı
hedef mesafesi) **rastgele barlarda** açılan işlemler de neredeyse aynı
kadar kazanıyor. Geriye kalan +0.092R, p=0.5612 ile tesadüfden ayırt
edilemiyor.

Bunun sebebi iki şeyin çarpımı:

1. **Geometri zaten lehte.** AB=CD'nin ödül/risk oranı ~3.2:1. %25 isabetle
   başabaş olan bir yapıda %41 isabet pozitif R verir — formasyon hiçbir
   şey bilmese bile.
2. **BIST nominal olarak yükseliyor.** Yalnız alış tarafı bu sürüklenişi
   üstleniyor.

### Kanıt: iki yön birlikte ölçülünce ne oluyor

Pasaportta K4'ten ÖNCE yazılmıştı: ayı tarafı BIST'te işleme çevrilemez
ama **ölçüm nesnesi** olarak tutulur. Tutulmasının karşılığı bu tablo.

| formasyon | işlem | sembol | beklenen R | adil baz | fark | p |
|---|---|---|---|---|---|---|
| `abcd` stop 1.272 | 1587 | 435 | −0.025R | −0.076R | +0.051R | 0.3578 |
| `abcd` stop 1.618 | 1587 | 435 | −0.069R | −0.104R | +0.035R | 0.3298 |
| `gartley` | 58 | 53 | +0.071R | +0.016R | +0.055R | 0.4033 |
| `kelebek` | 51 | 50 | −0.139R | −0.027R | −0.112R | 0.6827 |
| `uc_surus` | 71 | 65 | +0.101R | +0.023R | +0.078R | 0.2629 |

Yükseliş sürüklenişi iki yönde birbirini götürünce **hem strateji hem baz
sıfıra iniyor.** Formasyonun kendi katkısı +0.03R ile +0.08R arasında ve
hiçbiri anlamlı değil. Örneklem de artık yeterli: beş satırın beşinde de
sembol sayısı 50'nin üstünde, yani "az veri vardı" mazereti yok.

### IS penceresi OOS'u DOĞRULAMIYOR

| formasyon | OOS farkı | IS farkı |
|---|---|---|
| `abcd` stop 1.272 | **+0.092R** | **−0.114R** |
| `abcd` stop 1.618 | +0.093R | −0.028R |
| `gartley` | −0.100R | −0.097R |
| `kelebek` | −0.461R | −0.233R |
| `uc_surus` | −0.175R | −0.137R |

En iyi görünen satır iki pencerede **ters işaret** taşıyor. Bu, kalan
+0.092R'nin bile kararlı bir şey olmadığını gösteriyor.

### Çıkış kırılımı — neden böyle

| formasyon | hedef | stop | zaman | ort. kazanç | ort. kayıp |
|---|---|---|---|---|---|
| `abcd` stop 1.272 | %29 | %54 | %17 | +2.47R | −0.98R |
| `gartley` | %34 | %59 | %7 | +1.98R | −1.03R |
| `kelebek` | %19 | %52 | %29 | +1.42R | −0.88R |
| `uc_surus` | %33 | %67 | %0 | +2.22R | −1.05R |

Golden Zone'daki tablonun aynısı: **geometri lehte, isabet tam olarak onu
götürüyor.** Kazanan işlem 2.5R getiriyor, kaybeden 1R alıyor, ama kayıp
kazançtan iki kat sık. Çarpım sıfır.

### İkinci deneme — ön kayıtlı, ve o da reddedildi

İlk ölçüm kitabın **yöntemini değil, basitleştirilmiş hâlini** ölçmüştü:
"D'ye dokununca al". Pesavento bunu söylemiyor — KURAL-30 bir bar bekleme
tekniğini tarif ediyor. Bu eksik, ön kayıtlı **tek bir** ikinci denemeyle
kapatıldı: [`onkayit-harmonik-teyit.md`](../olcum/onkayit-harmonik-teyit.md).

Aynı koşuda gerçek bir ölçüm hatası da düzeltildi: bariyer yürüyüşü giriş
barını atlıyordu, ama D'de **limit dolum barın içinde** olur ve barın
kalanı canlıdır. Sinyallerin **%14–28'i** giriş barında zaten stop oluyor
ve ölçüme canlı giriyordu. Düzeltme, beklendiği gibi sonucu **kötüleştirdi**.

**Sonuç: sekiz testin hiçbiri geçemedi.** En iyisi `abcd·teyit`, p=0.0685
— sekiz test için BH eşiği 0.00625 olması bir yana, düz 0.05'i bile
geçemedi.

**Ve "az kalmıştı" diyemememin sebebi:**

| pencere | işlem | fark | p |
|---|---|---|---|
| IS (ilk %70) | 502 | +0.582R | 0.0780 |
| **OOS (son %30)** | 301 | **−0.005R** | 0.3953 |

Etkinin tamamı geçmişte; görülmemiş dönemde **sıfır**.

### KURAL-30 yine de ölçülebilir bir şey yapıyor

| formasyon | isabet | stop oranı | teyidin katkısı |
|---|---|---|---|
| `abcd` | %32.8 → **%45.3** | %65 → %47 | +0.534R |
| `kelebek` | %30.4 → **%45.5** | %65 → %41 | +0.414R |
| `uc_surus` | %24.6 → **%51.4** | %75 → %38 | +0.475R |
| `gartley` | %35.2 → %41.7 | %64 → %58 | −0.091R |

Bu, kitabın "körlemesine girme" tavsiyesinin boş olmadığını gösteriyor.
Ama etki adil bazdan ayrılacak kadar büyük ve kararlı değil.

### İleriye dönük izleme — kalan tek meşru yol

`abcd·teyit` kuralı **2026-09-14'te donduruldu** (`e5556aa`) ve bundan
sonra gelecek veride izlenecek:
[`ileri-izleme-abcd-teyit.md`](../olcum/ileri-izleme-abcd-teyit.md).

Geçmişte arama yapmak bitti. Bir kuralın çalıştığını gösteren tek meşru
yol, kural donduktan SONRA gelen veride ölçmektir — çünkü o veriye
bakarak kimse hiçbir seçim yapmadı. Eşik **30 sembol**; dolana kadar
rapor boş kalır ve **boş kalması doğru davranıştır.**

### Verdikt

**kanıtlanmadı.** Dört formasyonun hiçbiri, iki stop varyantının hiçbiri
BH-FDR'yi geçemedi. Bu "zarar ettiriyor" demek DEĞİL — `abcd` mutlak
olarak pozitif. Bu, **"formasyonun kendisinin bilgi taşıdığına dair kanıt
yok"** demek: aynı risk yapısını rastgele barlara koysanız da aynı sonucu
alıyorsunuz.

Kitabın Gartley için ~%70 isabet iddiası **doğrulanmadı**: ölçülen %41.4
(yalnız alış, n=29) ve %36.2 (iki yön, n=58).

## K5 · Görsel

| | |
|---|---|
| Komposer | [`komposer/harmonik.py`](../../packages/chart/quaxis/chart/komposer/harmonik.py) |
| Spec üretici | [`tools/harmonik_spec.py`](../../tools/harmonik_spec.py) — gerçek BIST verisi |
| Örnekler | `rtalb-abcd` · `dogub-gartley` · `srvgy-kelebek` · `burva-uc_surus` |
| İterasyonlar | **13** (`docs/design/ui/harmonik-pesavento-*-koyu-1440-son.png`) |
| İterasyon kaydı | [`docs/design/ui/README.md`](../design/ui/README.md) |
| Onay | ✅ **2026-09-14 · kullanıcı onayladı** |

### Kapı nasıl kapandı

13 iterasyon, dört formasyonun dördü de 1440 ve 768 genişlikte ayrı ayrı
yakalandı. Kusurların çoğu **gözle değil DOM ve piksel ölçümüyle** bulundu;
tam kayıt [`docs/design/ui/README.md`](../design/ui/README.md).

Son engel olan ölçek hatası (fiyat aralığının ucundaki köşe mumlarından 43
piksel uzağa düşüyordu) i13'te çözüldü — fark **2 piksele** indi.

**Kullanıcı onayı: 2026-09-14.**

### Örnekler nasıl seçildi

Seçim ölçütü **getiri değil okunaklılık**. Sonuç kendiliğinden karışık
çıktı: biri hedefe ulaştı, ikisi stop oldu, biri süre doldurdu. Kârlı
örnek seçmek, verdikti gizlemenin görsel hâli olurdu.

Örnekler ayrıca **2014 sonrasından** seçiliyor: kaynak, BIST için 2014
öncesinde gerçek açılış fiyatı vermiyor (`open` = `close`). İlk Three
Drives örneğinde (BURVA 2011) 106 barın 106'sı gövdesizdi ve levha mum
grafiği gibi görünmüyordu. K4 verdikti bundan etkilenmedi — OOS
pencereleri en erken 2020-08-31'de başlıyor.

### Grafiğin taşıdığı en önemli ayrım

Son bacak (→D) **kesik çizgi**, diğerleri düz. Harmonik grafiklerin klasik
yanıltmacası D'yi diğer köşelerle aynı çizgiyle bağlamaktır; o zaman D de
gerçekleşmiş bir salınım ucu gibi görünür. D bir pivot değil, C
onaylandığında **hesaplanan** bir fiyattır.

## K6 · Ürün

| | |
|---|---|
| Grafik yüzeyi | ✅ `/grafik` — strateji seçicide dört formasyon; `?f=harmonik-<ad>` derin bağlantısı |
| Kütüphane kartı | ✅ `lib/ornek-veri.ts` — dört kart, gerçek kaynak ve verdiktle |
| Strateji sayfası | *(bekliyor)* — `/stratejiler/harmonik-pesavento` |
| Tarama kolonu | *(bekliyor)* |
| Alarm kuralı | *(bekliyor)* — verdikt `kanıtlanmadı` olduğu için alarm **önerilmiyor** |

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
