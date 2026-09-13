# Ön kayıt — `macd_uyum` + `oynaklik_dusuk` kombinasyonu

**Yazıldığı tarih:** 2026-09-13
**Durum:** ⏳ **TEST HENÜZ KOŞULMADI.** Bu belge sonuç görülmeden yazıldı ve
sonucu görmeden commit edildi. Sonuç bölümü sonradan, olduğu gibi eklenecek.

> Bu belgenin varlık sebebi tek bir şey: **sonucu gördükten sonra kuralı
> değiştirme imkânını ortadan kaldırmak.** Hipotez, pencere, aile, karar
> kuralı ve neyin çürütme sayılacağı aşağıda önceden yazılı.

---

## 1. Hipotez

Golden Zone (BOS + OTE bölgesi) kurulumunda, **MACD histogramının sinyal
yönünde olması** ile **kısa vadeli oynaklığın uzun vadeli ortalamasının
altında olması** koşulları **birlikte**, tek başlarına olduğundan daha
büyük bir kenar üretir.

Gerekçe: ikisi farklı şeyleri ölçüyor. `macd_uyum` momentumun yönünü,
`oynaklik_dusuk` gürültü seviyesini. Bağımsız iki bilgi, birlikte daha
keskin bir filtre verebilir.

**Karşı hipotez (ve neden ciddiye alınıyor):** ikisi de aynı altta yatan
şeyin (sakin, yönlü piyasa) ölçüsü olabilir. O hâlde birleştirmek yeni
bilgi katmaz, sadece örneklemi küçültür ve ΔR gürültüyle şişer.

## 2. Test penceresi — ve neden bu

| | |
|---|---|
| **Birincil test** | **A grubu sembol + OOS penceresi** |
| İkincil (tutarlılık) | B grubu sembol + OOS penceresi |

**A/OOS seçildi çünkü hiçbir şey için kullanılmadı.** Arama A grubunda ama
yalnız **IS** penceresinde yapıldı; A sembollerinin OOS dönemine bu projede
hiç bakılmadı.

**B/OOS birincil OLAMAZ:** `macd_uyum` ve `oynaklik_dusuk` bileşenleri tam
orada doğrulandı. Bileşenleri doğrulanmış bir pencerede kombinasyonlarının
iyi çıkması **kısmen kurgu gereğidir**; bağımsız kanıt sayılmaz. Bu yüzden
B/OOS yalnızca *tutarlılık kontrolü* olarak raporlanacak, kanıt olarak
değil.

## 3. Aile ve düzeltme

Aynı pencerede ölçülecek **üç** koşul:

1. `macd_ve_oynaklik` (kombinasyon — test edilen)
2. `macd_uyum` (tek başına — kıyas)
3. `oynaklik_dusuk` (tek başına — kıyas)

BH-FDR bu **üçlü aileye** uygulanır (q=0.05). Aile burada sabitlendi;
sonuca bakıp genişletilmeyecek ya da daraltılmayacak.

## 4. Karar kuralı — dördü birden sağlanmalı

Kombinasyon "bileşenlerinden daha iyi" sayılır **ancak ve ancak**:

1. **ΔR üstünlüğü:** A/OOS'ta kombinasyonun koşulsuz tabana göre ΔR'si,
   `macd_uyum`'unkinden **ve** `oynaklik_dusuk`'unkinden büyük olmalı.
2. **Anlamlılık:** kombinasyonun p değeri üçlü ailede BH-FDR'yi geçmeli.
3. **Örneklem:** kombinasyon en az **30 işlem** taşımalı (Pardo s.295).
   Altına düşerse sayı yazılır, verdikt yazılmaz.
4. **Maliyet dayanıklılığı:** gidiş-dönüş **%0.45** maliyette hâlâ pozitif
   ortalama R vermeli. (`macd_uyum` tek başına bu eşiği geçiyor; kombinasyon
   geçemezse "daha iyi" denemez.)

## 5. Neyi çürütme sayarım

* Kombinasyonun ΔR'si `macd_uyum`'unkinin **altında** kalırsa → karşı
  hipotez doğrulanmış olur: ikisi aynı şeyi ölçüyor, birleştirmek sadece
  örneklem harcıyor.
* İşlem sayısı 30'un altına inerse → sonuç ne olursa olsun **verdikt
  verilmez**.
* ΔR büyür ama p ailede geçmezse → "kanıtlanmadı" yazılır; "az kalmıştı"
  diye geçirilmez.

## 6. Ölçüm ayarları (önceden sabit)

| | |
|---|---|
| Ölçüm | üç bariyerli R (`olcum/bariyer.py`) |
| Zaman bariyeri | 40 bar (stratejinin kendi parametresi) |
| İşlem maliyeti | taraf başına %0.05 komisyon + çıkışta %0.05 kayma |
| Permütasyon | 2000 tur |
| Aynı barda stop+hedef | stop |
| Bağımsız gözlem | sembol |

---

## 7. Sonuç

*(Koşu sonrası doldurulacak — ne çıkarsa.)*
