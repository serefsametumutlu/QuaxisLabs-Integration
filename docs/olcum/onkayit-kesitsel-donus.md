# Ön kayıt — Kesitsel Ortalamaya Dönüş (`kesitsel_donus`)

**Yazıldığı tarih:** 2026-09-13
**Durum:** ⏳ **TEST HENÜZ KOŞULMADI.** Bu belge sonuç görülmeden yazıldı ve
sonucu görmeden commit edildi.

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

*(Koşu sonrası doldurulacak — ne çıkarsa.)*
