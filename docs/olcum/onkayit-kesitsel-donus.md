# Ön kayıt — Kesitsel Ortalamaya Dönüş (`kesitsel_donus`)

**Yazıldığı tarih:** 2026-09-13
**Durum:** ✅ **KOŞULDU** (2026-09-13). Belge sonuç görülmeden yazıldı ve
`944bb5a` ile commit edildi; sonuç bölümü sonradan, olduğu gibi eklendi.

> Bu belgenin varlık sebebi: **sonucu gördükten sonra kuralı değiştirme
> imkânını ortadan kaldırmak.** Hipotez, pencere, karar kuralı ve neyin
> çürütme sayılacağı aşağıda önceden yazılı.

---

## 1. Hipotez

BIST'te, son 12 ayın **en çok kaybeden %10'unu** alıp 25 gün tutmak, aynı
dönemde rastgele bir hisse almaktan **daha iyi** getiri verir.

## 2. Nereden geliyor — ve dürüstçe, ne kadarı sonradan

İki kaynağı var ve ikisi farklı ağırlıkta:

**(a) Literatür — önceden var olan hipotez.** Kesitsel ortalamaya dönüş
uydurulmuş bir fikir değil: De Bondt–Thaler'in "aşırı tepki" çalışmasından
beri bilinir, Chan'ın 3–5. bölümleri (s.63–131) bunun üstüne kurulu ve
Chan momentum bölümünde (s.152) açıkça yazar:

> "Hisselerde kesitsel momentum 2008–2009 çöküşünün ardından **kayboldu ve
> yerini güçlü ortalamaya dönüşe bıraktı.**"

**(b) Bizim momentum ölçümümüz — sonradan.** Aynı gün, aynı evrende,
momentum üst %10'un rastgeleden **−%9.98** geride kaldığını ölçtük
(p=1.0000). Bu, ters yönü akla getiren doğrudan sebep.

**Bunu saklamıyorum:** hipotezi test etme kararı kısmen o sonuçtan doğdu.
Bu yüzden aşağıdaki karar kuralı **iki ayrı pencerede birden** geçmeyi
şart koşuyor. Tek pencerede geçen bir sonuç, "tersini dene" refleksinin
kendini doğrulaması olabilir.

## 3. Pencereler — ve neden bu sırayla

| | |
|---|---|
| **Birincil** | **IS penceresi** (ilk %70) |
| **Doğrulama** | OOS penceresi (son %30) |

**IS birincil çünkü hiç bakılmadı.** Momentum ölçümü yalnız OOS'u
raporladı; IS penceresinde ne olduğunu bilmiyorum. Bu stratejide "arama"
diye bir adım yok — tek bir hipotez var — dolayısıyla IS'i doğrudan test
penceresi olarak kullanmak meşru.

**OOS doğrulama çünkü momentum sonucu oradan geldi.** O pencerede
momentumun kötü olduğunu biliyorum; tersinin iyi çıkması kısmen beklenir.
Tek başına kanıt sayılmaz, ama **tutarlılık** için gerekli.

## 4. Karar kuralı — dördü birden sağlanmalı

1. **IS penceresinde** adil baza karşı fark **pozitif** ve **p ≤ 0.05**.
2. **OOS penceresinde** de fark **pozitif** ve **p ≤ 0.05**.
3. Her iki pencerede de bağımsız gözlem **≥ 30 sembol**.
4. İşlem maliyeti **dahil** ölçülmüş olmalı (taraf başına %0.05 komisyon
   + %0.05 kayma) — bu zaten ölçümün varsayılanı.

Aile tek koşuldan ibaret (`kesitsel_donus`), bu yüzden çoklu test
düzeltmesi uygulanmıyor. Aile burada sabitlendi; sonuca bakıp
genişletilmeyecek.

## 5. Neyi çürütme sayarım

* Herhangi bir pencerede fark **negatif** çıkarsa → hipotez reddedilir.
* Fark pozitif ama **yalnız bir** pencerede anlamlıysa → "kanıtlanmadı"
  yazılır. "Diğerinde az kalmıştı" gerekçesiyle geçirilmez.
* Gözlem sayısı 30'un altına inerse → sayı yazılır, verdikt yazılmaz.
* Fark pozitif ama **momentum'un negatifinden küçükse** (yani −(−%9.98)
  = %9.98'in belirgin altındaysa), bu simetrik bir etki değil demektir;
  sonuç raporlanır ama "momentumun aynası" diye sunulmaz.

## 6. Ölçüm ayarları (önceden sabit)

| | |
|---|---|
| Gösterge | `kesitsel_donus` (alt %10) |
| Ölçüt | 25 barlık ileri getiri (stratejinin kendi tutuş süresi) |
| Evren | 543 BIST sembolü, günlük |
| Geriye bakış | 252 gün (son ay atlanmaz — temel varyantla aynı) |
| Örtüşmeyen sinyal | evet (Chan s.151) |
| Permütasyon | 2000 tur |
| Bağımsız gözlem | sembol |

## 7. Baştan kabul edilen sınır

Yalnız alış olduğu için bu strateji BIST'in kendi sürüklenmesini
üstleniyor. Adil baz (aynı pencerede rastgele sembol) bunu ayıklıyor —
ama **mutlak getiri ile kenar aynı şey değil.** Fark pozitif çıksa bile
bu, stratejinin "kazandırdığı" değil, "rastgeleden iyi olduğu" anlamına
gelir.

---

## 8. Sonuç

| Pencere | Sembol | Sinyal | Strateji | Adil baz | **Fark** | p |
|---|---|---|---|---|---|---|
| **IS** (birincil) | 39 | 87 | %+1.12 | %+2.06 | **−%0.95** | 0.5697 |
| **OOS** (doğrulama) | 213 | 832 | %+3.49 | %+3.74 | **−%0.25** | 0.5142 |

### Karar kuralı

| Madde | Sonuç |
|---|---|
| 1 · IS'te fark pozitif ve p ≤ 0.05 | ✘ (fark **negatif**) |
| 2 · OOS'ta fark pozitif ve p ≤ 0.05 | ✘ (fark **negatif**) |
| 3 · Her iki pencerede ≥ 30 sembol | ✔ |
| 4 · İşlem maliyeti dahil | ✔ |

### Verdikt

**HİPOTEZ REDDEDİLDİ.** Kural açıktı: "herhangi bir pencerede fark
negatif çıkarsa hipotez reddedilir." İki pencerede de negatif.

### Asıl bulgu: etki SİMETRİK DEĞİL

Momentum ölçümüyle yan yana koyunca tablo netleşiyor:

| Kimi alırsan | Rastgeleye karşı fark |
|---|---|
| Üst %10 (geçen yılın kazananları) | **−%9.98** |
| Alt %10 (geçen yılın kaybedenleri) | **−%0.25** |

Kaybedenler rastgeleden **ayırt edilemiyor** (p=0.51). Kazananlar ise
belirgin biçimde **geride**. Yani bu "ortalamaya dönüş var" değil,
**"geçmişin kazananlarından uzak dur"** demek.

Ön kayıttaki 5. maddenin son şıkkı tam bunu öngörmüştü: fark
momentumun negatifinin belirgin altındaysa "momentumun aynası" diye
sunulmaz. Sunmuyorum — ayna değil.

### Bunun pratik karşılığı

Kendi başına bir strateji değil ama **bir filtre**: hangi kurulum olursa
olsun, son 12 ayın en çok kazanan %10'undaki hisselerde uygulamamak
ölçülebilir bir fark yaratıyor gibi görünüyor. Bu bir hipotez ve **kendi
ön kaydını hak ediyor** — bu belgede ölçülmedi.

### IS penceresinin küçüklüğü

IS'te yalnız 39 sembol/87 sinyal var; OOS'ta 213/832. Sebep yapısal:
252 günlük geriye bakış + BIST'te sembollerin çoğunun son yıllarda
listelenmesi, erken dönemde sıralanacak sembol bırakmıyor. Kural
"≥30 sembol" eşiğini geçiyor ama IS sonucunun güven aralığı geniştir;
karar zaten iki pencerenin **ikisinde de** negatif olmasına dayanıyor.

