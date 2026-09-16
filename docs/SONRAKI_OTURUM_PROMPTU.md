# Sonraki oturum — nerede kaldık

**Son güncelleme:** 2026-09-17 · **Son commit:** `867131b` üzerine
**Depo durumu:** temiz · **287 test yeşil** (+3 `network` deselect) · ruff
temiz · pasaport doğrulayıcı tutarlı

---

## Tek cümleyle

Üç strateji ailesi ölçüldü, üçü de elendi; ölçüm zemini denetlenip ön kayıtla
düzeltildi ve üç ailenin de ölçümü yenilendi — **üçünde de verdikt
değişmedi**. Sonra **gerçek tarama motoru** evrende koştu ve ürün maket
veriden kurtuldu: harmoniklerin **K6 kapısı kapandı**, projenin yedi kapıyı
da geçen **ilk stratejisi**.

---

## Yenileme sonucu (2026-09-17) — ön kayıt §6 kapandı

| Aile | Fark (en güçlü aday) | p | Verdikt |
|---|---|---|---|
| Harmonik (`abcd·teyit`) | +0.266R | 0.0445 (FDR eşiği 0.00625) | `kanıtlanmadı` |
| Golden Zone (A katmanı) | −0.029R | 0.9820 | `kanıtlanmadı` |
| Kesitsel Momentum | −%9.62 | 1.0000 | `kanıtlanmadı` |

Üç ailede de ön kayıt §5'in şartları sağlanmadı. Ayrıntı:
[`onkayit-veri-duzeltme.md`](olcum/onkayit-veri-duzeltme.md) §7–§10.

> **Golden Zone'da bir tuzak var, yazılı:** 13 Eylül'ün katmanlı tablosu
> işlem maliyeti ölçüme girmeden önce üretildi (`b11de50`). Ham `Ort. R`
> sütunları 17 Eylül'ünkiyle yan yana konamaz; karşılaştırılabilen büyüklük
> **fark**tır (strateji − adil baz), o da maliyete neredeyse duyarsızdır.

---

## Gerçek tarama motoru (2026-09-17) — ADR-003

`/tarama` artık maket veri göstermiyor. Karar ve gerekçeler:
[`ADR-003`](karar/ADR-003-tarama-koprusu.md).

```bash
python tools/tarama.py kos            # gün sonu taraması (1G, tüm evren)
python tools/tarama.py ozet           # ne çıktı
python tools/tarama_disaktar.py       # results.db -> apps/web/lib/tarama-verisi.json
```

İlk koşu `bist_2026-09-16`: **625/648 sembol**, 15 dk 44 sn, **2656 güncel
sinyal**, repaint alarmı yok. 23 sembolde sağlayıcı veri döndürmüyor ve bu
arayüzde adlarıyla yazılı.

Rozet artık denetleniyor: pasaport künyelerindeki `gostergeler:` eşlemesi
göstergeyi pasaporta bağlar, `pasaport.py dogrula` sahipsiz gösterge bırakmaz.

**Dikkat:** `apps/web/lib/tarama-verisi.json` ~980 KB ve depoda. Her günün
koşusu commit'lenirse depo şişer — ürün sürümlerinde tazelenmeli.

**Sıradaki iş:** aşağıdaki "açık başlıklar" listesinden seçilir.

---

## Bu turda ne yapıldı (2026-09-13 → 09-16)

### A · Harmonik formasyonlar — K0'dan K6'ya

Pesavento'nun dört formasyonu (AB=CD · Gartley 222 · Butterfly · Three
Drives) sıfırdan yazıldı ve yedi kapıdan geçirildi.

| Kapı | Durum |
|---|---|
| K0 Kaynak | ✅ |
| K1 Sözleşme · K2 Dedektör | ✅ 41 test |
| K3 Kalibrasyon | ✅ eşikler ölçümden türetildi |
| K4 İstatistik | ✅ **`kanıtlanmadı`** — 5 testin 5'i FDR'yi geçemedi |
| K5 Görsel | ✅ **kullanıcı onayı 2026-09-14**, 13 iterasyon |
| K6 Ürün | 🔶 grafik + kütüphane kartı + strateji sayfası hazır; **tarama kolonu açık** (tarama yüzeyi hâlâ maket veriyle çalışıyor) |

İkinci bir ön kayıtlı deneme de yapıldı (KURAL-30 "bir bar bekle"):
isabeti %32.8 → %45.3 çıkardı ama p=0.0685 ile reddedildi.
`abcd·teyit` kuralı **donduruldu** ve ileriye dönük izlemede:
[`ileri-izleme-abcd-teyit.md`](olcum/ileri-izleme-abcd-teyit.md).

### B · Veri denetimi — asıl bulgu burada

[`docs/olcum/veri-denetimi-bist-1D.md`](olcum/veri-denetimi-bist-1D.md)

**1. Bayat barlar adil bazı besliyordu.**

| Giriş barı | n | 40 bar ileri getiri |
|---|---|---|
| hacimsiz | 40 779 | **%15.31** |
| normal | 1 370 593 | %6.93 |

Stratejiler o barlarda neredeyse hiç sinyal üretmiyordu (%0.04) ama baz
%2.8 oranında oradan çekiyordu. **Baz kirli, stratejiler temizdi.**

**2. Kendi doğrulayıcımız 104 sembolü atıyordu.** Tek bir OHLC ihlali
`OHLCVError` fırlatıyor ve `Store` sembolü hiç yazmıyordu. MGROS 4 284
barın **1'i** bozuk diye 16 yıllık veri çöpe gidiyordu — Migros,
Coca-Cola İçecek, Logo, Anadolu Grubu, Şekerbank dahil.

**3. Hayatta kalma yanlılığı.** 625 sembolün 625'inin son barı 2026'da.
Evren dosyası bugünün listesinin anlık görüntüsü. **Düzeltilemiyor** —
kottan çıkan şirketlerin verisi sağlayıcıda yok. Artık evren dosyasında ve
her raporda yazılı.

**4. 2014 öncesi açılış fiyatı yok.** `açılış == kapanış` oranı 2012'de
%96.5 → 2024'te %3.2.

### C · Uygulanan düzeltmeler (ön kayıtlı)

| | Ne |
|---|---|
| D1 | Hacimsiz bar adil baz havuzundan çıktı |
| D2 | Hacimsiz barda sinyal doğmuyor (harmonik + golden_zone) |
| D3 | OHLC ihlalinde **bar** atılıyor, sembol değil → **544 → 625 sembol** |
| D4 | Gövde tabanlı kurallar 2014'ten başlıyor |

> D3 ön kayıttan **saptı** ve sebebi belgede yazılı: eksikliğin sebebini
> sağlayıcı sanmıştım, kendi doğrulayıcımız çıktı.

---

## Strateji envanteri

| Strateji | Kapı | Verdikt |
|---|---|---|
| Golden Zone (ICT OTE) | K4 | `kanıtlanmadı` ⏸ |
| Kesitsel Momentum | K4 | `kanıtlanmadı` ⏸ |
| Harmonik ×4 (Pesavento) | **K6 ✅** | `kanıtlanmadı` — yayında, etiketli |
| Salınım Fibo ABCD | — | dedektörü yok, yalnız çizimi var |

**Yayınlanmış (K6) strateji: 1** (harmonikler). Yayınlanmış olmak "işe
yarıyor" demek değil: verdikt `kanıtlanmadı`, ürün formasyonu gösteriyor ama
sistem kimseye "al" demiyor ve alarm kurulmuyor.

---

## Sonrası için açık başlıklar

1. **"Geçen yılın kazananlarından uzak dur" filtresi** ← en güçlü bulgu.
   Momentum üst %10'u rastgeleye göre düzeltilmiş veride de **−%9.62**
   (p=1.0000). Açığa satılamaz ama **filtre** olarak kullanılabilir. Ön
   kaydı yazılmadı, makine hazır, bir turda biter.
2. **Gerçek tarama motoru** — K6'yı kapatır, üç stratejinin hepsine yarar
3. **Strateji kütüphanesi eksik** — `golden-zone` ve `kesitsel-momentum`
   pasaportları var ama `lib/ornek-strateji.ts`'te kaydı yok. Tarama
   tablosunda görünüp kütüphanede görünmüyorlar; kartların üçü de hâlâ maket.
4. **Hayatta kalma yanlılığını sınırlamak** — KAP'tan 2010–2026 BIST
   şirket listesi çekip kaç sembolün eksik olduğunu saymak
5. **Kalan dört harmonik ekol** (Bat/Crab/Shark · Cypher · 5-0) — ayrı
   kitaplar, ayrı K0. **Beklenen değeri en düşük iş.**

---

## Çalışma disiplini — yeni oturumun bilmesi gerekenler

* **Ölçmeden iddia yok.** Her eşik ya kitaptan sayfa/bölüm alıntısıyla ya
  da K3 ölçümünden gelir. `tools/pasaport.py dogrula` bunu denetler.
* **Olumsuz sonuçtan sonra yapılan her deneme ön kayıt ister.** Kural,
  pencere, aile ve neyin çürütme sayılacağı **sonuç görülmeden** yazılıp
  commit edilir.
* **Eleme değil etiketleme.** Kenar bulunamayan strateji silinmez;
  `kanıtlanmadı` etiketiyle üründe durur ve grafiğinin künyesinde
  "tarihsel isabet: kanıtlanmadı" yazar.
* **Sessiz temizlik yasak.** Atılan veri raporlanır.
* Depoda `.claude/skills/` altında dört skill var: `quaxis-mimari`,
  `strateji-pasaportu`, `grafik-tasarim-sistemi`, `web-tasarim-sistemi`.
  Koda dokunmadan önce ilgilisini oku.
