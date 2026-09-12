# references/ — hedeflenen görsel çıktının tanımı

Bu klasör bir ilham panosu **değil**. Buradaki her görsel, bir stratejinin
K5 (Görsel) kapısında **yan yana konulacak hedeftir**. "Güzel oldu" demek
yerine "bu dosyaya benziyor mu" diye sorulacak.

## Grafik referansları

Kaynak: `Desktop\Teknik Analiz\önemli\` + repo kökündeki örnekler.
Hepsi kullanıcının kendi seçtiği/onayladığı çıktılar.

| Dosya | Karşıladığı strateji görseli |
|---|---|
| `HRhIeAdbcAAL2_B.png` | **XABCD harmonik + fibo merdiveni** — dolgulu XAB/BCD üçgenleri, sağ kenarda oran-renkli fibo seviyeleri (`0.618: 185.00`), `D: 159.40 [TAMAMLANDI]` kutulu etiketi, HH/HL/LH/LL swing etiketleri. **En yüksek çıta budur.** |
| `HRdEu6qaoAEaHIT.png` | A-B-C-D salınımı + teorik/gerçek D; birleşik hover kutusu (`hovermode="x unified"` benzeri) |
| `HRjNKRZWAAAhfSy.png` | Yatay aralık (range box) — destek/direnç + numaralı temaslar |
| `HRihBa2WIAIZjP_.png` | Üçgen — sınır çizgisi temasları **numaralı dairelerle** (`U1,U2,U3` / `L1,L2,L3`) |
| `HRiPy4qbUAA1bKc.png` | Simetrik / alçalan üçgen |
| `HRiOTwUbQAA9WKw.png` | Yükselen/alçalan paralel kanal; `3A / 6A / 1Y / Tümü` zaman aralığı düğmeleri |
| `HRaULXwaEAA60Z5.png` | Bayrak / flama (direk + konsolidasyon + kırılım) |
| `HRhMNlYbwAACrVs.png` | Üç itiş (three drives) — **yalnızca üç etiket, başka hiçbir şey yok** |
| `HRcUk75bgAApv6n.png` | Çift sağlığı (pair health) paneli — normalize fiyat, z-skoru, tutulan dönem gölgeleri |
| `HRb_x7YWYAA750T.png` | Likidite radarı (Corwin–Schultz spread + sigma) |
| `HRt3uuwaEAAWAgK.png` | İstatistik tablosu — METRİK / DEĞER / DURUM, pozitif-negatif satır rengi |
| `ornek1.png` | Piyasa yapısı — HH / LH / HL / LL üçgenleri, BOS / CHoCH |
| `TOBO.png` | OBO / TOBO — boyun çizgisi, hologram, uç üçgenleri |
| `ornek2.png` | **Yapı stratejisi** — arz/talep bölgeleri ve yapı öğeleri bir arada. Kullanıcı notu: birebir hedef değil; **hacim profili ve POC bu görselde YOK**, onlar ikinci turda eklenecek. |
| `yeni strateji.png` | **FVG (Adil Değer Boşluğu)** stratejisi |

### Bu görsellerden çıkarılan ortak kural

Hiçbiri jenerik bir çizicinin çıktısı değil. Her biri **o stratejiye özel
bestelenmiş**: farklı etiket biçimi, farklı vurgu, farklı sadelik derecesi.
Three Drives'ta üç etiketten başka hiçbir şey yokken, harmonikte tam bir fibo
merdiveni var. Bu yüzden mimaride tek renderer değil, **strateji başına
komposer** var (bkz. `docs/karar/ADR-001-yeniden-insa.md`).

## Arayüz referansları

### `luxalgo/` — uygulama ekranları (kullanıcı ekledi)

Dört ekran görüntüsü. Verilen dört pazarlama sitesinin aksine bunlar **gerçek
uygulama yüzeyi** — asıl ihtiyacımız olan referans bu:

- **Grafik ekranı:** dar ikon çubuğu (sol) · sembol + zaman dilimi çipleri + gösterge
  seçici (üst) · sol üstte OHLC HUD'ı · **sağ üstte yoğun durum tablosu**
  (Major Swing Bias / Internal Bias / Structure Power / Next Bull MSB) ·
  sağ kenarda fiyat ekseni + vurgulu son fiyat rozeti · grafik üstünde
  `HH / HL / LH / LL / MSB / CHoCH` küçük etiketleri · sağ kenarda
  `Swing High: 82814.23` biçiminde renkli seviye etiketleri.
- **Kütüphane ekranı:** arama + iki sıra filtre çipi + `874 INDICATORS` sayacı +
  kart ızgarası. Kartın yüzü **gerçek bir grafik görüntüsü**; altında
  `LUXALGO · SEP 9, 2026` meta satırı, başlık, açıklama paragrafı, "View indicator".

Ölçülen kesin değerler (bizim tasarım sistemimize doğrudan giriyor):
`874 INDICATORS` sayacı **11px / ui-monospace / +2.2px tracking / uppercase / #7d7d7d**;
filtre çipi **13px / dolgu 6-14px / tam hap / zemin #0a0a0a / kenarlık 0.8px beyaz %10 /
metin #a0a0a0**.

### Pazarlama siteleri

`referans_token_olcumleri.json` — kullanıcının verdiği dört sitenin
(dovetail.com, slash.com, v7labs.com, luxalgo.com) gerçek `getComputedStyle`
ölçümleri. Sentezi: [`docs/design/TASARIM_DILI.md`](../docs/design/TASARIM_DILI.md).
