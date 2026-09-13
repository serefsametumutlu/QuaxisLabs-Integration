# golden-zone-r2 — K4 Katmanlı Ölçüm

**Tarih:** 2026-09-13 · **Gösterge:** `golden_zone_r2` · **Zaman dilimi:** 1D

Soru katman başına "kenar var mı" değil, **"kenar EKLİYOR mu"**. `ΔR` sütunu
bir önceki katmana göre işlem başına beklenen R değişimidir.

**Pencere:** her iki ölçüm de yalnız **OOS** penceresini sayar (serinin son
%30'i). İki sütun aynı dönemden konuşmazsa tablo sessizce yanıltır.

| Katman | İçerik | İşlem | Sembol | İsabet | Ort. R | Adil baz | ΔR | p (R) | Hedef/Stop/Zaman | İleri getiri | p | Verdikt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | yapı kırılımı + OTE bölgesi | 8432 | 518 | %37.0 | +0.058R | +0.080R | — | 0.9270 | %31 / %60 / %9 | %-0.34 | 0.7981 | kanitlanmadi |
| **B** | A + (FVG veya bölgedeki Order Block) | 6004 | 515 | %36.5 | +0.036R | +0.082R | -0.022R | 0.9935 | %30 / %60 / %10 | %-0.19 | 0.6862 | kanitlanmadi |
| **C** | B + likidite süpürmesi | 1056 | 424 | %36.6 | +0.036R | +0.054R | +0.001R | 0.3513 | %30 / %60 / %10 | %+0.11 | 0.4453 | kanitlanmadi |

## Katman başına aday sayımı (K3)

**A** — MAKUL: sembol başına ortalama 19.2 aday, sembollerin %2'i sıfır.
**B** — MAKUL: sembol başına ortalama 13.7 aday, sembollerin %2'i sıfır.
**C** — MAKUL: sembol başına ortalama 2.4 aday, sembollerin %13'i sıfır.

## Ne çıkarsa o

**Kenar bulunamadı. Bulunamamakla kalmadı — teyit katmanları değer EKSİLTTİ.**

Üç katmanın üçünde de sinyaller, aynı risk yapısıyla rastgele barlardan
girmekten **daha iyi değil**. A katmanında sinyal +0.058R, adil baz +0.080R;
yani bölge, piyasanın kendi verdiğinden azını veriyor. p değerleri 0.05'in
uzağında (0.9270 · 0.9935 · 0.3513) — bu "ölçüm kararsız kaldı" değil, "aranan
yönde iz yok" demek.

Katman ekledikçe durum **iyileşmedi**: ΔR sütunu B'de −0.022R, C'de +0.001R
— FVG/OB katmanı değer eksiltti, süpürme katmanı ise hiçbir şey eklemedi
(+0.001R, ölçüm gürültüsünün içinde). Meta-etiketleme hipotezi (López de
Prado s.51–53) bu veride **doğrulanmadı**.

C katmanının p değeri (0.3513) diğerlerinden düşük ama hâlâ eşiğin yedi
katı — üstelik tek başına bakılmış bir p. Üç katman × iki hedef modu = altı
testin içinden seçilseydi çoklu test düzeltmesi onu daha da yukarı iterdi.

Örneklem küçüklüğü bir mazeret değil: en dar katman olan C bile 1056 işlem
ve 424 sembol taşıyor — Pardo'nun 30 işlemlik tabanının (s.295) çok üstünde.

### Neden kenar yok: çıkış kırılımı

| | A | B | C |
|---|---|---|---|
| Hedefte çıkış | %31 | %30 | %30 |
| Stopta çıkış | %60 | %60 | %60 |
| Zamanda çıkış | %9 | %10 | %10 |

Kurulumun geometrisi lehte (0.62 girişte 1.63:1, 0.705'te 2.39:1) ama isabet
oranı tam olarak o avantajı silecek kadar düşük. %31 hedef × ~1.7R kazanç
eksi %60 stop × 1R kayıp ≈ sıfır. **Asimetri gerçek, ama fiyatlanmış.**

### "Kenar yok" ile "zarar ettirir" aynı şey değil

İşlem başına ortalama R **pozitif** (+0.058R). Strateji para kaybettirmiyor;
**piyasanın kendi verdiğinin altında kalıyor** — aynı dönemde aynı risk
yapısıyla rastgele girmek +0.080R veriyordu. Bulgu şu: *bölgenin kendisi,
girişi rastgeleden ayıran bir bilgi taşımıyor.*

### Bu, "ICT işe yaramaz" demek değil

Ölçtüğümüz şey ICT'nin uyguladığı şey değil ve fark K0'da gerekçesiyle yazılı:

| ICT'nin yaptığı | Bizim ölçtüğümüz |
|---|---|
| FX, intraday (M1–M15) | BIST, **günlük** |
| Kill zone (seans) filtresi | filtre **yok** |
| Öznel "daily bias" | yerine BOS yönü (ölçülebilir) |
| T1'de kısmi + koşucu | **tek hedef, tek stop** |

Burada çürütülen şey, **"OTE bölgesi BIST günlükte tek başına swing
kurulumu olarak kenar üretir"** iddiasıdır — ICT'nin bütünü değil.

## Ölçümün sınırları

| | |
|---|---|
| Dönem | 2010-01-01 – 2026-09-11; ölçüm yalnız **OOS** penceresinde (son %30 — sembol başına ortanca ~1006 bar ≈ 4 yıl) |
| Evren | **543** BIST sembolü ölçüldü. Liste 648; 104'ü veri hatası nedeniyle dışarıda (tam döküm: [`veri-bist-1D-2026-09-13.md`](veri-bist-1D-2026-09-13.md)) |
| Elenen semboller rastgele DEĞİL | 81'i sağlayıcıda bozuk tick (53 high, 28 low), 23'ü borsada yok. Bozuk tick'liler **onarılmadı, elendi** — veriyi sessizce düzeltmek ölçümün zeminini görünmez biçimde değiştirirdi. |
| Hayatta kalma yanlılığı | **VAR.** Evren bugünkü listeden; 2010–2026 arasında kotasyondan çıkmış semboller hiç girmedi. |
| İşlem maliyeti | **yok** — komisyon, spread, kayma hesaba katılmadı. Katılsaydı sonuç daha KÖTÜ olurdu. |
| Fill varsayımı | Giriş, bölge seviyesine limit emir. Fiyat seviyeye dokunduğu için emir dolar varsayıldı; kısmi dolmama modellenmedi. |
| Aynı barda stop+hedef | **stop** sayıldı (iyimserliğe karşı) |
| Eşikler | Hiçbiri optimize EDİLMEDİ; ICT'nin kendi sayıları olduğu gibi kullanıldı. Sonuç aşırı uydurma taşımıyor — ama "hiç aranmadı" da demek. |

> Bağımsız gözlem birimi **sembol**dür, bar değil.
