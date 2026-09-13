# Kesitsel Momentum — K0 Kaynak Dosyası

**Tarih:** 2026-09-13 · **Pasaport:** `docs/strateji/kesitsel-momentum.md`
**Karar:** yalnız **alış** (açığa satış yok) · **sinyal başına** ölçüm

Bu dosya stratejinin **doğduğu yerdir**. Buradaki her kural ya bir kaynağa
ya da bir ölçüme bağlıdır.

---

## 1. Kural — kaynaktan, sayfa numarasıyla

**Ernest Chan, *Algorithmic Trading: Winning Strategies and Their Rationale*
(2013), s.145–146**
(`Quant Playbook/books/Group 1…/Algorithmic Trading - Winning Strategies…md`)

> "Bir grup menkulün 12 aylık getirisini (programda 252 işlem günü) her gün
> sırala, en yüksek getirili olanı **1 ay (25 işlem günü)** al ve tut, en
> düşük getirili olanı aynı süre sat ve tut."

Kitabın örnek kodundaki (s.146, `kentdaniel.m`) parametreler:

```
lookback = 252     % geriye bakış: 12 ay
holddays =  25     % tutuş: 1 ay
topN     =  50     % S&P 500 evreninde üst/alt 50 hisse
```

Asıl çalışma: **Daniel & Moskowitz (2011)**. Chan'ın aktardığına göre bu
strateji "dünya endeksleri, dövizler, uluslararası hisseler ve ABD
hisselerinde — yani güneşin altındaki hemen her şeyde" çalışmış (s.146).

### Bizim sapmamız: yalnız alış

**Karar (2026-09-13): açığa satış yok.** BIST'te açığa satış kısıtlı; kural
yalnız üst dilimi almaya indirgeniyor.

Bu **kaynağın stratejisini zayıflatır ve bunu bilerek yapıyoruz.** Uzun/kısa
kurulum piyasa yönünü nötrler; yalnız alış nötrlemez, BIST'in kendi
sürüklenmesini üstlenir. Dolayısıyla **adil baz bu stratejide her zamankinden
kritiktir**: "yükseldi" ile "yükselenleri seçmek işe yarıyor" ayrı şeyler.

---

## 2. Kaynağın bildirdiği sonuç — ve çöküşü

| | |
|---|---|
| APR | %18, Sharpe 1.37 |
| Dönem | 2005-06-01 – 2007-12-31 (52 emtia vadelisi) |
| **Kriz dönemi** | **APR −%33** (2008-01-02 – 2009-12-31) |

Chan'ın kendi cümlesi (s.146): *"2008–2009 finansal krizi bu momentum
stratejisini mahvetti, tıpkı daha önce anılan S&P DTI göstergesi dahil
diğer birçoğunu mahvettiği gibi."*

### Chan'ın kendi çekinceleri (s.151–153) — K0'a aynen giriyor

**1. Momentum stratejileri kâr etmesi ZOR olanlardır.**

> "Kendi ticaret deneyimimde, kârlı momentum stratejileri yaratmanın daha
> zor olduğunu ve kârlı olanların ortalamaya dönüş stratejilerinden daha
> düşük Sharpe oranlarına sahip olma eğiliminde olduğunu sık sık gördüm."

**2. Sebebi: bağımsız sinyal sayısı az.**

> "Yerleşik momentum stratejilerinin çoğu uzun geriye bakış ve tutuş
> sürelerine sahip. Dolayısıyla bağımsız ticaret sinyallerinin sayısı az ve
> seyrek. (Momentum portföyünü her gün yeniden dengeleyebiliriz ama bu
> ticaret sinyallerini daha bağımsız yapmaz.)"

**Bu cümle ölçüm tasarımımızı doğrudan belirliyor** — bkz. §4.

**3. Momentum çöküşleri krizden SONRA yıllarca sürer.**

> "Daniel ve Moskowitz'in 'momentum çöküşleri' üzerine araştırması, vadeli
> ya da hisse momentum stratejilerinin bir finansal krizden sonra **birkaç
> yıl boyunca** berbat performans gösterme eğiliminde olduğunu gösteriyor."

> "Hisselerde kesitsel momentum da 2008–2009 borsa çöküşünün ardından
> **kayboldu ve yerini güçlü ortalamaya dönüşe bıraktı.**"

---

## 3. Neden bu strateji seçildi

Golden Zone'dan öğrenilenler ışığında:

| Ölçüt | Kesitsel momentum |
|---|---|
| Kaynakta **kanıt** var mı | ✔ Yayımlanmış APR/Sharpe + akademik asıl çalışma |
| Mekanizma farklı mı | ✔ Grafik kurulumu değil, **kesitsel sıralama** |
| Kalabalık mı | ⚠ Literatürün en bilinen anomalisi — kalabalık olabilir |
| Günlük veriyle ölçülebilir mi | ✔ Yalnız kapanış gerekir |
| Adil baz kurulabilir mi | ✔ Aynı anda rastgele sembol seçmek |

**Çöküş modunun belgeli olması bir artıdır, eksi değil.** "Ne zaman
çalışmaz" sorusunun cevabı önceden yazılıysa, ölçüm onu sınayabilir:
BIST'te 2018 ve 2020 kırılmalarında ne olduğu somut bir soru.

---

## 4. Ölçüm tasarımı — Chan'ın uyarısından türetilmiştir

### Örtüşen sinyaller sayılmaz

Chan (s.151) açıkça söylüyor: her gün yeniden dengelemek sinyalleri
bağımsız yapmaz. 25 günlük tutuşta her gün sinyal üretirsek, aynı sembolün
25 sinyali neredeyse aynı işlemi 25 kez sayar; örneklem sahte büyür ve
p değeri sahte küçülür.

**Kural: bir sembol için yeni sinyal, öncekinin tutuş süresi BİTMEDEN
üretilmez.** Örtüşmeyen sinyal demek, kabaca sembol başına yılda ~10 işlem
demektir.

### Ölçüt R değil, ileri getiri

Kaynakta **stop yok**: pozisyon 25 gün tutulur, sonra kapanır. Zorla bir
stop uydurmak stratejiyi değiştirmek olur. Bu yüzden ölçüt üç bariyerli R
değil, `olcum/ileri_getiri.py`'nin **25 barlık ileri getirisi**.

**İşlem maliyeti yine de düşülür.** Golden Zone'da öğrendik: maliyetsiz
ölçüm her kenarı olduğundan büyük gösterir.

### Adil baz

Aynı barda, aynı sayıda, **rastgele seçilmiş** sembollerin 25 günlük
getirisi. Yalnız alış olduğu için bu baz kritik: BIST'in sürüklenmesi
pozitif ve strateji onu **yenmek** zorunda, ona binmek değil.

---

## 5. Eşikler ve kaynakları

| Eşik | Değer | Kaynak |
|---|---|---|
| geriye_bakis | 252 gün | s.146 kod: `lookback=252` |
| tutus | 25 gün | s.146 kod: `holddays=25` |
| ust_dilim | evrenin üst %10'u | s.146 `topN=50` / 500 = %10; BIST evreninde oransal karşılığı |
| atlama (skip) | ölçülecek | `K3:` türetilecek — bkz. §6 |
| asgari_islem_hacmi | ölçülecek | `K3:` türetilecek |

## 6. Kaynaktan bilinçli sapmalar

| Sapma | Gerekçe |
|---|---|
| **Yalnız alış** | BIST'te açığa satış kısıtlı (kullanıcı kararı). Kaynağın uzun/kısa kurgusu piyasa yönünü nötrlerdi; bizimki nötrlemiyor ve bunu adil bazla ayıklayacağız. |
| **topN oransal** | Kaynak 500 hisseden 50 alıyor (%10). BIST evreni 543; oranı koruyoruz, sayıyı değil. |
| **Örtüşmeyen sinyal** | Kaynak her gün yeniden dengeliyor. Biz ölçüm için örtüşmeyen sinyal alıyoruz — Chan'ın kendi uyarısı gereği (s.151). |
| **Son ay atlanır mı belirsiz** | Akademik momentum literatürü genelde "12-1" kullanır (son ayı atlar, kısa vadeli dönüşü dışlamak için). Chan'ın kodu atlamıyor. **İkisi de ölçülecek**, karar K3'e bırakıldı. |
| Likidite filtresi | Kaynakta yok. BIST'te ince sembollerde momentum sıralaması gürültüdür; eşik K3'ten türetilecek. |

## 7. Ne zaman çürütülmüş sayılır

Ön kayıt niteliğinde, şimdiden yazılı:

* İleri getiri, adil bazın **altında** kalırsa → kenar yok.
* Fark pozitif ama işlem maliyeti düşülünce sıfırlanırsa → uygulanamaz.
* Yalnız belirli bir dönemde (ör. 2020-2021 ralisi) varsa ve diğer
  dönemlerde yoksa → dönem etkisi, strateji değil.

## Kaynaklar

- Chan, E. (2013). *Algorithmic Trading: Winning Strategies and Their
  Rationale*, s.145–146 (kural + kod), s.151–153 (çekinceler).
- Daniel, K. & Moskowitz, T. (2011). "Momentum Crashes" — Chan üzerinden
  atıf; asıl makale depoda yok.
