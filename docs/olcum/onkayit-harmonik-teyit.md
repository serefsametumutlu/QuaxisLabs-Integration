# Ön kayıt — Harmonik teyitli giriş (KURAL-30, "bir bar bekle")

**Yazıldığı tarih:** 2026-09-13
**Durum:** ✅ **KOŞULDU** (2026-09-13). Belge sonuç görülmeden yazılıp
`f989bf6` ile commit edildi; sonuç bölümü sonradan, olduğu gibi eklendi.

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

Ölçüm dosyası:
[`harmonik-pesavento-K4b-teyit-1D-long.md`](harmonik-pesavento-K4b-teyit-1D-long.md)

### Tüm dönem (birincil pencere)

| künye | işlem | sembol | isabet | beklenen R | adil baz | **fark** | PF | p |
|---|---|---|---|---|---|---|---|---|
| `abcd·kor` | 2413 | 451 | %32.8 | +0.148R | +0.323R | −0.176R | 1.22 | 1.0000 |
| **`abcd·teyit`** | **803** | **362** | **%45.3** | **+0.707R** | **+0.349R** | **+0.359R** | **2.35** | **0.0685** |
| `gartley·kor` | 108 | 92 | %35.2 | +0.053R | +0.240R | −0.187R | 1.08 | 0.8941 |
| `gartley·teyit` | 36 | 36 | %41.7 | −0.108R | +0.171R | −0.278R | 0.82 | 0.8926 |
| `kelebek·kor` | 138 | 113 | %30.4 | −0.195R | +0.228R | −0.423R | 0.71 | 1.0000 |
| `kelebek·teyit` | 44 | 43 | %45.5 | +0.174R | +0.183R | −0.009R | 1.39 | 0.4633 |
| `uc_surus·kor` | 142 | 117 | %24.6 | −0.256R | +0.150R | −0.407R | 0.68 | 0.9990 |
| `uc_surus·teyit` | 37 | 35 | %51.4 | +0.173R | +0.105R | +0.069R | 1.42 | 0.2499 |

### Karar kuralı (§6) — `abcd·teyit`, en güçlü aday

| Madde | Sonuç |
|---|---|
| 1 · Adil baza karşı fark pozitif | ✔ **+0.359R** |
| 2 · p ≤ 0.05 **ve** BH-FDR | ✘ **p = 0.0685** — düz eşiği bile geçmiyor |
| 3 · ≥ 30 sembol | ✔ 362 |
| 4 · Körlemesine varyanttan daha iyi | ✔ **+0.534R** katkı |

**Dördünden üçü sağlandı, ikincisi sağlanmadı. Kural ikisini de istiyordu.**

### Verdikt: HİPOTEZ REDDEDİLDİ

§7 açıktı: "Hiçbir teyitli varyant FDR'yi geçemezse harmonik ailesi
çürütülmüştür ve bu dosya son denemedir."

Sekiz testin hiçbiri geçemedi. En iyisi p=0.0685 ile **düz 0.05 eşiğini
bile** geçemedi; sekiz test için BH eşiği ise 0.00625'ti.

### Ama KURAL-30 gerçekten bir şey yapıyor

Bunu saklamak sonucu çarpıtmak olurdu. Teyit tekniği dağılımı **belirgin
biçimde** değiştirdi:

| formasyon | isabet (körlemesine → teyitli) | stop oranı | teyidin R katkısı |
|---|---|---|---|
| `abcd` | %32.8 → **%45.3** | %65 → %47 | **+0.534R** |
| `kelebek` | %30.4 → **%45.5** | %65 → %41 | **+0.414R** |
| `uc_surus` | %24.6 → **%51.4** | %75 → %38 | **+0.475R** |
| `gartley` | %35.2 → %41.7 | %64 → %58 | −0.091R |

Dörtte üçünde isabet ~15 puan arttı ve stop oranı ~20 puan düştü.
Pesavento'nun "körlemesine girme, bir bar bekle" tavsiyesi **ölçülebilir
bir etki** taşıyor. Sadece bu etki, adil bazdan ayrılacak kadar büyük ve
kararlı **değil**.

### Neden "az kalmıştı" demiyorum — asıl bulgu burada

`abcd·teyit`'in p=0.0685'i cazip. Ama pencereler ayrıştırılınca etkinin
nerede olduğu ortaya çıkıyor:

| pencere | işlem | fark | p |
|---|---|---|---|
| IS (ilk %70) | 502 | **+0.582R** | 0.0780 |
| **OOS (son %30)** | **301** | **−0.005R** | **0.3953** |

**Etkinin tamamı IS penceresinde.** Görülmemiş dönemde fark **sıfır**.
Tüm dönemin +0.359R'si, IS'in +0.582R'sinin OOS'un sıfırıyla
ortalamasından ibaret.

Ön kayıt §4 tüm dönemi birincil yapmıştı ve bu doğru bir karardı
(örneklem için). Ama §4 aynı zamanda şunu yazmıştı: "tutarsızlık çıkarsa
bu bir BULGU olarak yazılacak — seçim hakkı olarak değil." Çıktı ve
yazılıyor.

Bir etkinin yalnız geçmişte görünüp görülmemiş dönemde kaybolması, o
etkinin gerçek olmadığının en bilinen işaretidir. Eşikleri oynatıp
p'yi 0.05'in altına indirmek burada **kanıt değil, o kayboluşu gizlemek**
olurdu.

### Bu koşuda düzeltilen hata ne yaptı

`giris_bari_riskli` düzeltmesi (giriş barının kendisi de stop için
sayılır) körlemesine varyantı beklendiği gibi kötüleştirdi:

| | önce | sonra |
|---|---|---|
| `abcd·kor` farkı (OOS) | +0.092R | **+0.059R** |
| `abcd·kor` farkı (tüm dönem) | — | **−0.176R** |

Düzeltmeden önceki rakamlar, gerçekte giriş barında stop olmuş %17.4'lük
işlemi canlı sayıyordu.

### Son söz

Bu, ön kayıtta yazıldığı gibi **son denemeydi.** Üçüncü bir varyant
denenmeyecek. Harmonik ailesi `kanıtlanmadı` etiketiyle kapanır.

`abcd·teyit` için tek meşru yol kaldı ve o da **ileriye dönük**: kural
bugün donduruldu; bundan sonra gelecek gerçekten yeni veride izlenebilir.
Geçmişte arama yapmakla gelecekte doğrulamak farklı şeylerdir.
