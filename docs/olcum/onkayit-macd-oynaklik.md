# Ön kayıt — `macd_uyum` + `oynaklik_dusuk` kombinasyonu

**Yazıldığı tarih:** 2026-09-13
**Durum:** ✅ **KOŞULDU** (2026-09-13). Belge sonuç görülmeden yazıldı ve
`71aa9cf` ile commit edildi; sonuç bölümü sonradan, olduğu gibi eklendi.

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

**Koşuldu:** 2026-09-13 ·
**Pencere:** A grubu + OOS · 272 sembol ·
**Koşulsuz taban:** -0.001R (4150 işlem)

| Koşul | İşlem | Ort. R | ΔR | p | Aile BH-FDR |
|---|---|---|---|---|---|
| `macd_ve_oynaklik` | 1078 | +0.134R | +0.135R | 0.0500 | — |
| `macd_uyum` | 2186 | +0.067R | +0.068R | 0.8166 | — |
| `oynaklik_dusuk` | 2129 | +0.029R | +0.029R | 0.1329 | — |

### Karar kuralının dört maddesi

| Madde | Sonuç |
|---|---|
| 1 · ΔR her iki bileşenden büyük | ✔ |
| 2 · üçlü ailede BH-FDR geçti | ✘ |
| 3 · en az 30 işlem | ✔ |
| 4 · %0.45 maliyette hâlâ pozitif | ✔ |

### Verdikt

**KOMBİNASYON DAHA İYİ DEĞİL**

### Yorum

**Kombinasyon en büyük ΔR'yi verdi (+0.135R) ve yine de geçemedi.** Kural
önceden yazılmıştı: üçlü ailede BH-FDR eşiği 0.05×1/3 = 0.0167; ölçülen
p=0.0500 bunun üç katı. Madde 1, 3 ve 4 sağlandı, madde 2 sağlanmadı.

Ön kaydın işini yaptığı yer tam burası. Kural önceden yazılmasaydı
"+0.135R, üçünün en büyüğü, p=0.05" tablosuna bakıp **geçti derdim.**

### Asıl bulgu: `macd_uyum` gruplar arasında kararsız

Bu koşu, ilan ettiğim bir önceki bulguyu ciddi biçimde zayıflatıyor:

| Pencere | `macd_uyum` | p | Koşulsuz taban |
|---|---|---|---|
| **B grubu + OOS** | +0.133R | **0.0025** | +0.037R |
| **A grubu + OOS** | +0.067R | **0.8166** | −0.001R |

Aynı pencere türü, aynı dönem, **farklı semboller** — ve p 0.0025'ten
0.8166'ya çıkıyor. Bu, bir kenarın sembol grubuna göre ikiye katlanıp
kaybolması demek. Gerçek ve kararlı bir etki böyle davranmaz.

İki açıklama mümkün ve ikisini de ayırt edemiyorum:

1. `macd_uyum`'un B/OOS'taki gücü kısmen şanstı. Aday olarak seçilmesinin
   sebebi zaten orada iyi çıkmasıydı; seçim yanlılığı bu yönde çalışır.
2. Etki gerçek ama sembol bileşimine duyarlı (sektör, likidite, fiyat
   ölçeği). O hâlde "BIST'te işe yarar" değil "bazı BIST sembollerinde işe
   yarar" demek gerekir — ki bu çok daha zayıf bir iddiadır.

**Sonuç olarak `macd_uyum` bulgusunu "doğrulandı" saymaktan geri
çekiliyorum.** İki OOS penceresinden birinde güçlü, diğerinde yok.

### Ne öğrendik

* Kombinasyon, bileşenlerinden **daha büyük ΔR** veriyor — bu tutarlı bir
  işaret ve boşa atılmamalı.
* Ama hiçbiri yeterince **kararlı** değil. Kararsızlığın kaynağı sembol
  bileşimi gibi görünüyor.
* Sıradaki doğru soru "hangi gösterge" değil, **"hangi sembollerde"**:
  likidite, fiyat ölçeği ve sektör kırılımında etkinin nasıl değiştiğini
  ölçmek. Bu, yeni bir ön kayıt ister.

### Ölçümün sınırları

| | |
|---|---|
| Grup dengesi | A/OOS tabanı −0.001R, B/OOS tabanı +0.037R. Gruplar arasındaki fark yalnız koşuldan değil, **tabandan** da geliyor. |
| Tek bölme | A/B bölmesi tek bir hash bölmesi. Çoklu bölme (tekrarlı) daha güvenilir olurdu; yapılmadı. |
| Dönem | Her iki OOS de AYNI takvim dönemi. Dönem etkisi ayrıştırılamadı. |
