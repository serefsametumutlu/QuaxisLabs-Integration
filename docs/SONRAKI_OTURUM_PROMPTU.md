# Sonraki oturum — nerede kaldık

**Son güncelleme:** 2026-09-16 · **Son commit:** `6041b42`
**Depo durumu:** temiz · 287 test yeşil · ruff/tsc/eslint temiz · pasaport
doğrulayıcı tutarlı

---

## Tek cümleyle

Üç strateji ailesi ölçüldü, üçü de elendi; sonra **ölçüm zemininin kendisi
denetlendi** ve gerçek veri kusurları bulunup düzeltildi. Harmonikler
düzeltilmiş veriyle yeniden ölçüldü — verdikt değişmedi. **Golden Zone ve
Kesitsel Momentum'un yenilenmesi kaldı.**

---

## Sıradaki iş — buradan devam et

Ön kayıt [`docs/olcum/onkayit-veri-duzeltme.md`](olcum/onkayit-veri-duzeltme.md)
§6 **üç ailenin de** yenilenmesini istiyor. Harmonikler koşuldu, ikisi
bekliyor:

```bash
# 1) Golden Zone (katmanlı ölçüm)
python tools/katmanli_olcum.py --katalog "quaxis.teknik.indicators.katalog:KATALOG" \
    --gosterge golden_zone --slug golden-zone --zaman-dilimi 1D

# 2) Kesitsel Momentum
python tools/momentum_olcum.py
```

Sonra ön kaydın **§7 Sonuç** bölümü tamamlanır (harmonik kısmı yazılı,
diğer ikisi eklenecek) ve iki pasaportun K4 bölümü güncellenir.

**Kural:** ön kayıt §6 — *bir kere koşulacak*. Sonuca bakıp ikinci bir
düzeltme turu yapılmayacak.

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
| Harmonik ×4 (Pesavento) | K5 ✅ | `kanıtlanmadı` ⏸ |
| Salınım Fibo ABCD | — | dedektörü yok, yalnız çizimi var |

**Yayınlanmış (K6) strateji: 0.**

---

## Sonrası için açık başlıklar

1. **Golden Zone + Kesitsel Momentum yenilemesi** ← sıradaki
2. **"Geçen yılın kazananlarından uzak dur" filtresi** — kendi
   ölçümümüzden çıkan en güçlü bulgu: momentum üst %10'u rastgeleye göre
   **−%9.98** (p=1.0000). Açığa satılamaz ama **filtre** olarak
   kullanılabilir. Ön kaydı yazılmadı, makine hazır, bir turda biter.
3. **Gerçek tarama motoru** — K6'yı kapatır, üç stratejinin hepsine yarar
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
