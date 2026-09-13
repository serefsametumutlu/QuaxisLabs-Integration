# Ön kayıt — Veri düzeltmesi ve ölçümlerin yenilenmesi

**Yazıldığı tarih:** 2026-09-14
**Durum:** ⏳ düzeltme UYGULANMADAN ve sonuçlar GÖRÜLMEDEN yazıldı.

> Bu belge, üç olumsuz verdiktten **sonra** yapılan bir veri düzeltmesini
> tarif ediyor ve tam da bu yüzden var. Olumsuz bir sonucun ardından
> veriye dokunmak, "geçene kadar temizle" olmaya adaydır. Ne
> değiştirileceği, ne değiştirilmeyeceği ve neyin sonucu değiştirmiş
> sayılacağı aşağıda **önceden** yazılı. Tek koşu, tek karar.

---

## 1. Neden düzeltme gerekiyor

Veri denetimi ([`veri-denetimi-bist-1D.md`](veri-denetimi-bist-1D.md)) bir
ölçüm hatası buldu ve bu hata doğrudan **adil bazı** ilgilendiriyor:

| Giriş barı | n | 40 bar ileri getiri |
|---|---|---|
| **hacimsiz** | 40 779 | **%15.31** |
| normal | 1 370 593 | %6.93 |

Hacimsiz barın fiyatı kimsenin işlem yapmadığı bir fiyattır; sağlayıcı son
fiyatı tekrar eder ve işlem yeniden başlayınca fiyat sıçrar. Medyanın
hacimsiz tarafta **%0.00** olması deseni ele veriyor: barların çoğu düz,
bir kuyruk ortalamayı yukarı çekiyor.

`olcum/bariyer.py::_bos_havuzu` adil bazı rastgele barlardan kuruyor ve bu
barları **dışlamıyor.** Yani bazın bir bölümü, kimsenin giremeyeceği
fiyatlardan alınmış hayalet işlemlerden oluşuyor.

Bu bir yorum değil, ölçülmüş bir sayı. Düzeltilmesi sonuçtan bağımsız
olarak doğrudur.

---

## 2. Ne DEĞİŞECEK — dördü, tamamı

### D1 · Hacimsiz bar adil baz havuzundan çıkar

`_bos_havuzu` rastgele bar seçerken `volume == 0` olan barları seçilebilir
kümeden çıkarır.

### D2 · Hacimsiz barda sinyal doğmaz

Dedektörler `volume == 0` olan barda sinyal üretmez. Bu dedektör
tarafında yapılır, ölçüm tarafında değil: **kimsenin işlem yapmadığı bir
fiyattan doğan sinyal, sinyal değildir** — grafikte de görünmemeli.

Hacimsiz barda `açılış = yüksek = düşük = kapanış` olduğu için bir seviyeye
"dokunmuş" sayılabiliyor; kural bunu kapatır.

### D3 · Evren dosyası gerçek evreni gösterir

Dosyada 648 sembol var, verisi olan 544. Bu 104 sembol:

1. Önce yeniden çekilmeye çalışılır.
2. Hâlâ gelmiyorsa evren dosyasından **gerekçesiyle** düşürülür.

Sebep: "648 sembollük evren" diye raporlanan her ölçüm aslında 544'te
koşuyordu. Sayının yanlış olması, sonucun yanlış olmasından ayrı bir
sorundur.

#### ⚠ D3 UYGULAMASI BU PLANDAN SAPTI — sebebiyle

Plan "önce yeniden çek, gelmiyorsa evren dosyasından düş" diyordu. Çünkü
eksikliğin sebebinin **sağlayıcı** olduğunu varsaymıştım.

Denendi ve sebep başka çıktı: **bu semboller sağlayıcıda var, bizim kendi
doğrulayıcımız reddediyor.** `validate_ohlcv` tek bir OHLC ihlalinde
`OHLCVError` fırlatıyor ve `Store.update` o sembolü hiç yazmıyor.
Ölçüldü:

| sembol | bar | ihlalli bar | en büyük sapma | yıl |
|---|---|---|---|---|
| MGROS | 4 284 | **1** (%0.02) | %0.9 | 2012 |
| CCOLA | 4 285 | **1** (%0.02) | %0.2 | 2012 |
| LOGO | 4 284 | **2** (%0.05) | %0.7 | 2011–12 |
| AGHOL | 4 285 | **1** (%0.02) | %0.4 | 2011 |
| SKBNK | 4 284 | **1** (%0.02) | %0.5 | 2013 |

16 yıllık veri, 2012'deki tek bir barın binde dokuzluk sapması yüzünden
çöpe gidiyordu — ve kaybedilenler arasında Migros, Coca-Cola İçecek,
Logo, Anadolu Grubu, Şekerbank var.

Dahası: **ayakta kalan semboller, bozuk barları tesadüfen toleransı
aşmayanlardı.** Hayatta kalma yanlılığının üstüne binen ikinci bir seçim
yanlılığı.

Bu yüzden D3, sembolü düşürmek yerine **barı atacak** biçimde uygulandı
(`ohlc_temizle`). Eşik yok: ihlalli bar atılır, sembol her zaman kalır,
kaç bar atıldığı raporlanır.

Bu bir sapmadır ve gizlenmiyor. Planın AMACI ("evren dosyası gerçek
evreni göstersin") korunuyor, aracı değişiyor — ve değişen araç
sembolleri **kaybetmek** yerine **kurtarıyor**. Hiçbir eşiğe, parametreye
ya da strateji kuralına dokunulmadı.

### D4 · Gövde tabanlı kurallar 2014'ten başlar

`açılış == kapanış` oranı 2012'de %96.5, 2010'da %81.6. Kaynak o dönemde
gerçek açılış fiyatı vermiyor.

Mum **gövdesine** bakan her kural (KURAL-30 teyidi, `govde_orani`) için
ölçüm penceresi **2014-01-01**'de başlar. Seviyeye dokunmaya bakan kurallar
(harmonik D, Golden Zone bölgesi) tüm geçmişi kullanmaya devam eder —
onlar açılış fiyatına bakmıyor.

---

## 3. Ne DEĞİŞMEYECEK — ve nedeni

**Hiçbir eşik, parametre, oran ya da pencere dokunulmayacak.** K3'ten
türetilen tolerans, pivot kolu ve dönüş penceresi aynı kalır. Aile aynı
kalır. İşlem maliyeti aynı kalır.

Değişen tek şey **hangi barların gözlem sayıldığı**. Bu ayrım bu belgenin
bel kemiği: veri hatası düzeltmek ile strateji ayarlamak farklı şeylerdir
ve ikincisi burada YASAK.

### Dışlanmayan kusurlar

* **Donuk barlar** (≥5 bar aynı kapanış ama hacim var) dışlanmıyor.
  Hacimsizlik kesin bir ölçüt; "hacim var ama fiyat oynamadı" değil —
  düşük oynaklık gerçek olabilir. Belirsiz olanı dışlamak, dışlamayı
  sonuca göre ayarlama kapısını açar.
* **Hayatta kalma yanlılığı** düzeltilemiyor: kottan çıkan şirketlerin
  fiyat verisi sağlayıcıda yok. Her ölçüm raporuna sabit bir uyarı olarak
  girer. Bilinen bir yanlılık, bilinmeyen bir yanlılıktan iyidir.
* **Marjı aşan barlar** dışlanmıyor: denetim çoğunun GERÇEK olduğunu
  gösterdi (2020-03-12 devre kesici günü).

---

## 4. Beklentimi ÖNCEDEN yazıyorum

Düzeltmenin yönü hakkında tahminim şu ve yanılabilirim:

**Adil baz DÜŞECEK.** Hacimsiz barlar bazın içinden çıkınca, bazın
ortalaması normal barların ortalamasına yaklaşır.

**Stratejilerin kendi sayıları daha az değişecek.** Dedektörler bir
seviyeye dokunma arıyor; hacimsiz barda dört fiyat da aynı sayı olduğu
için böyle bir barın tam olarak seviyeye denk gelmesi seyrek olmalı.

**Dolayısıyla fark (strateji − baz) YÜKSELMELİ.**

Bu tahmin, düzeltmeyi cazip kılan şeydir ve tam da bu yüzden yazıyorum:
sonuç bunu doğrulamazsa, tahmin yanlıştı diye yazacağım; doğrularsa,
"zaten biliyordum" demeyeceğim.

---

## 5. Neyin sonucu değiştirmiş sayılacağı

Yenilenen ölçüm sonrası bir stratejinin verdikti **ancak** şu üçü birden
sağlanırsa değişir:

1. Adil baza karşı fark **pozitif**,
2. Permütasyon **p ≤ 0.05** ve ailesinin **BH-FDR**'sini geçiyor,
3. Bağımsız gözlem **≥ 30 sembol**.

Üçü sağlanmazsa verdikt `kanıtlanmadı` kalır — fark büyüse bile.

### Neyi çürütme sayarım

* Fark büyür ama p eşiği geçmezse → **verdikt değişmez** ve bu
  raporlanır. "Yaklaştı" bir sonuç değildir.
* Düzeltme sonrası fark **küçülürse** → tahminim yanlıştı, öyle yazılır
  ve düzeltme yine de KALIR (doğru olduğu için, sonucu iyileştirdiği için
  değil).
* Sinyal sayısı %20'den fazla düşerse → dedektör kuralı beklenenden çok
  daha fazla sinyali kesiyor demektir; sebebi ayrıca incelenir.

---

## 6. Kaç kere koşulacak

**Bir kere.** Düzeltme uygulanır, üç aile (Golden Zone · Kesitsel Momentum
· Harmonik) yeniden ölçülür, ne çıkarsa yazılır.

Sonuca bakıp ikinci bir düzeltme turu yapılmayacak. Yeni bir veri kusuru
bulunursa kendi ön kaydını hak eder.

---

## 7. Sonuç

*(düzeltme uygulandıktan sonra, olduğu gibi eklenecek)*
