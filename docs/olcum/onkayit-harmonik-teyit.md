# Ön kayıt — Harmonik teyitli giriş (KURAL-30, "bir bar bekle")

**Yazıldığı tarih:** 2026-09-13
**Durum:** ⏳ sonuç GÖRÜLMEDEN yazıldı ve commit edildi.

> Bu belge, olumsuz bir sonucun ardından yapılan **ikinci** denemedir ve
> tam da bu yüzden var. İlk ölçüm başarısız olduktan sonra yapılan her
> deneme, "geçene kadar dene" olmaya adaydır. Kural, pencere ve aile
> aşağıda **önceden** yazılı; tek deneme, tek karar.

---

## 1. Neden ikinci bir deneme meşru

İlk K4 ölçümü **kitabın yöntemini değil, onun basitleştirilmiş hâlini**
ölçtü: "fiyat D'ye dokununca al."

Pesavento bunu söylemiyor. Kitabın 11. bölümü formasyon tamamlandıktan
sonra ne yapılacağına ayrılmış:

* **KURAL-28** — uyarı işaretleri: CD bacağında gap, tamamlanmaya yakın
  geniş barlar, dik CD.
* **KURAL-29** — teyit işaretleri: cımbız, işlem yönünde gap, kuyruklu
  kapanış / geniş bar.
* **KURAL-30** — **bir bar bekleme tekniği**: uyarı işaretleri varsa bir
  bar fazladan bekle ve ancak teyit gelirse gir.

K0'da bunu "bilinçli sapma" diye yazdık (dedektöre eşik gömmemek için).
Eşik gömmemek doğruydu; **hiç ölçmemek eksikti.**

Bu, López de Prado'nun meta-etiketleme yapısıyla birebir aynı (s.51–53):
yüksek recall'lı birincil model (formasyon), precision'ı düzelten ikincil
katman (teyit).

## 2. Neden TAM OLARAK bu varyant — ve başka hiçbiri

KURAL-29'un işaretlerinin (gap, geniş bar, kuyruklu kapanış) hepsi bir
**eşik** ister ve kitap eşik vermiyor. Eşik uydurup taramak, "geçene kadar
dene"nin ta kendisi olurdu.

KURAL-30'un bekleme tekniğinin ise **hiç serbest parametresi yok**:

> **Teyitli giriş:** fiyat D'ye dokunduğu bar SİNYALDİR ama giriş DEĞİLDİR.
> Bir sonraki barın kapanışı beklenir. O bar **işlem yönünde kapanırsa**
> (boğada `close > open`, ayıda `close < open`) o kapanıştan girilir.
> Kapanmazsa **işlem HİÇ açılmaz.**

Tek bir tanım, sıfır eşik, sıfır tarama. Ölçülen şey kitabın kendi cümlesi.

## 3. Aynı koşuda düzeltilecek GERÇEK hata

Tanı koşusu (2026-09-13) şunu buldu: bariyer yürüyüşü giriş barının BİR
SONRASINDAN başlıyor. Ama giriş D'de bir **limit dolumdur** — o barın
içinde gerçekleşir ve barın kalanı hâlâ canlıdır. Barın dibi stop'un
altındaysa gerçekte **aynı bar stop olunur.**

| formasyon | giriş barında zaten stop olmuş |
|---|---|
| `abcd` | %17.4 |
| `gartley` | %16.2 |
| `kelebek` | %14.4 |
| `uc_surus` | %28.3 |

**Bu hata harmonikleri KAYIRIYOR.** Düzeltilmesi sonucu kötüleştirecek ve
bunu bilerek düzeltiyoruz: doğru ölçüm, lehimize olan ölçüm değildir.

Düzeltme, "aynı barda iki bariyer de vurulursa stop kazanır" kuralının
aynısı: bar içi sıralamayı bilmiyoruz, emin olmadığımız yerde stratejinin
lehine varsaymıyoruz.

**Not:** teyitli varyantta bu sorun kendiliğinden yok oluyor (giriş bir
sonraki barın kapanışı). Yine de körlemesine varyant da bu düzeltmeyle
YENİDEN ölçülecek — yoksa iki varyant farklı kurallarla kıyaslanmış olur.

## 4. Pencere — ve neden bu sefer TÜM dönem

İlk ölçümün birincil penceresi OOS'tu (son %30). Bu sefer **tüm dönem**.

Gerekçe: IS/OOS ayrımı, eşiklerin **getiriye bakarak** seçilmesine karşı
bir korumadır. Bizim eşiklerimiz (`tolerans`, `pivot`, `donus_max_bar`)
K3'te **yalnız aday sayısından** türetildi; R'ye hiç bakılmadı, ölçüm
aracı o koşuda hiç çağrılmadı. Getiri üzerinde arama yapılmadığı için
ayırmanın koruduğu bir şey yok — ayırmanın tek etkisi örneklemi %70
küçültmek.

Ve o küçülme gerçek bir zarar verdi: Gartley'in OOS örneklemi **27
sembole** düştü ve Pardo s.295 gereği verdikt yazılamadı.

**IS ve OOS ayrıca raporlanacak** ve tutarsızlık çıkarsa bu bir bulgu
olarak yazılacak — seçim hakkı olarak değil.

## 5. Aile — ÖNCEDEN sabit

**8 test:** 4 formasyon × 2 varyant (körlemesine / teyitli), 1G, yalnız
alış.

Haftalık (1H) **bu aileye dahil DEĞİL.** Dahil etmek aileyi 16'ya
çıkarırdı ve FDR eşiğini gereksizce zorlaştırırdı; ayrıca haftalıkta
örneklem zaten çok küçük. Haftalık merak ediliyorsa **kendi ön kaydını
hak eder.**

BH-FDR (q = 0.05) bu sekizine birden uygulanır.

## 6. Karar kuralı — dördü birden

Bir formasyonun **teyitli** varyantı "işe yarıyor" sayılması için:

1. Adil baza karşı fark **pozitif**.
2. Permütasyon **p ≤ 0.05** ve **BH-FDR'yi geçiyor**.
3. Bağımsız gözlem **≥ 30 sembol**.
4. Aynı formasyonun **körlemesine** varyantından **daha iyi** — yani
   teyidin kendisi katkı yapmış olmalı. Sadece ikisi birden geçerse teyit
   "işe yaradı" denemez; formasyon zaten çalışıyordu denir.

## 7. Neyi çürütme sayarım

* Hiçbir teyitli varyant FDR'yi geçemezse → **harmonik ailesi
  çürütülmüştür** ve bu dosya son denemedir. Üçüncü bir varyant
  denenmeyecek.
* Teyitli varyant geçer ama körlemesineden **daha kötüyse** → teyit
  katkı yapmıyor demektir; formasyonun kendi sonucu neyse o yazılır.
* Örneklem 30 sembolün altına inerse → sayı yazılır, verdikt yazılmaz.
* Fark pozitif ama işlem maliyeti iki katına çıkarıldığında sıfırlanırsa
  → "uygulanamaz" yazılır.

## 8. Baştan kabul ettiğim şey

Bekleme tekniği **bedava değildir.** Bir bar beklemek girişi kötüleştirir:
boğada, teyit barı yukarı kapandığı için D'den daha YÜKSEK bir fiyattan
girilir. Stop aynı yerde kaldığı için **risk büyür ve ödül/risk oranı
düşer.**

Yani teyit, isabeti bu kaybı telafi edecek kadar artırmak zorunda. Kitabın
iddiası tam olarak budur ve ölçülecek olan da budur.

## 9. Sonuç

*(ölçümden sonra, olduğu gibi eklenecek)*
