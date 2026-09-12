---
name: strateji-pasaportu
description: Bir stratejiyi yedi kapıdan geçirme süreci (K0 Kaynak → K6 Ürün) — her kapının bitti kriteri, kanıtın nereye konacağı ve doğrulayıcının neyi reddettiği. QuaxisLabs'ta yeni bir strateji yazarken, mevcut bir stratejinin kapısını açarken ya da "bu strateji hangi aşamada" sorusunda kullan.
---

# Strateji Pasaportu — yedi kapı

Her strateji `docs/strateji/<slug>.md` dosyasında yaşar. **Bir kapı geçilmeden
sonraki açılmaz; yedisi geçilmeden sıradaki stratejiye geçilmez.**

```bash
python tools/pasaport.py yeni <slug> --ad "<Ad>" --paket yapi
python tools/pasaport.py dogrula          # kapı tutarlılığı
python tools/pasaport.py durum            # kim nerede
```

> **Neden bu kadar katı.** Önceki projede süreç bir kontrol listesiydi ve
> listeye uyulmadı: K5 (görsel kabul) **hiç yapılmadı** — 115 test dosyasının
> hepsi veri yapısı testiydi, kimse çıktının resmine bakıp referansla
> karşılaştırmadı. K4 (istatistik) en sona bırakıldı ve 27 gösterge
> kodlandıktan **sonra** hiçbirinin kenar kanıtlamadığı anlaşıldı.
>
> Disiplin yetmediği için kapılar artık **denetleniyor**: "geçti" yazmak
> yetmez, kanıtı diskte bulunmak zorunda.

## Kapılar

| Kapı | Bitti kriteri | Kanıt nerede |
|---|---|---|
| **K0 Kaynak** | Kural kitaptan, **sayfa numarasıyla**. Tüm eşikler alıntılanmış. | Pasaportun Eşikler tablosu; her satırın kaynağı dolu |
| **K1 Sözleşme** | Tipli sonuç, frozen params, durum makinesi, non-repaint gerekçesi | `indicators/<…>/params.py`, pasaportta tablo |
| **K2 Dedektör** | Kod + birim test + **walk-forward repaint** + lookahead lint temiz | test dosyası yolu |
| **K3 Kalibrasyon** | Tam evrende aday sayısı ölçülmüş | `docs/olcum/<slug>-K3-<tarih>.md` |
| **K4 İstatistik** | Sembol-kümelenmiş OOS + permütasyon + BH-FDR | `docs/olcum/<slug>-K4-<tarih>.md` |
| **K5 Görsel** | Komposer + referansla karşılaştırma + **≥3 iterasyon** + **kullanıcı onayı** | `docs/design/ui/<slug>-*.png` |
| **K6 Ürün** | Kütüphane kartı + strateji sayfası + "nasıl okunur" + alarm | web dosyaları |

## Doğrulayıcının reddettikleri

Bunlar tahmin değil, `tools/tests/test_pasaport.py`'de sabitlenmiş davranış:

- **Kapı atlama.** K2 geçilmiş ama K1 açıksa düşer.
- **Kanıtsız kapı.** "Geçti" yazıp kanıt göstermemek düşer; gösterilen dosya
  diskte yoksa düşer.
- **Ezberden sayı.** Eşiğin kaynağı boşsa ya da "genel kabul" gibi bir şeyse
  düşer. Yalnız iki geçerli kaynak var: sayfa alıntısı (`s.44`) ya da
  `K3: docs/olcum/…md`.
- **Ölçülmeden etiket.** K4 açılmadan `verdikt` `olculmedi` dışında olamaz;
  açıldıktan sonra `olculmedi` kalamaz.
- **Onaysız görsel kapısı.** K5, kullanıcı onayı ve en az üç iterasyon karesi
  olmadan kapanmaz.
- **İki strateji birden.** Biri K6'ya varmadan diğeri K0'ı geçemez.

## Kapı kapı ne yapılır

### K0 · Kaynak — stratejinin doğduğu yer

ADR-002: K0 formalite değil. Kural **kitaptan** çıkarılır, eşikler
**alıntılanır**, sonra BIST verisinde kalibre edilir. Eski koda bakılabilir ama
**referans olarak değil, yalnız karşılaştırma için** — farklılık çıkarsa
**kitap kazanır**.

Kaynaklar: `Quant Playbook/books/` (17 kaynak) ·
`bilanco-radar/bilgi-bankasi/teknik/` (Pesavento, Carver + uygulanabilirlik
matrisi) · `Desktop/Trading Books/` · `Desktop/Strateji kaynakları/`

Kitapta olmayan bir eşik varsa iki seçenek: ya kaynak bulunur, ya
`K3: <ölçüm dosyası>` yazılır ve **K3'te gerçekten ölçülür**. Üçüncü yol yok.

### K1 · Sözleşme

`frozen dataclass` parametreler, `params_hash`, durum makinesi
(`pending → confirmed → …`). **Non-repaint gerekçesi** burada yazılır: pivot
kaç bar sonra kesinleşir, açık bar neden sinyal üretemez. Bu metin, K2'deki
testin neyi kanıtlaması gerektiğini tarif eder.

### K2 · Dedektör

Kod + birim testler + `repaint_test` + `lint_lookahead` temiz.

`repaint_test` yerine `register_verified_elsewhere` kullanılıyorsa **neden**
generic teste giremediği pasaportta yazılı olmak zorunda. Bu bir kaçış kapısı
değil, belgelenmiş istisnadır.

### K3 · Kalibrasyon

Tam evrende aday sayısı. **Sıfıra yakınsa gösterge bozuk, on binlerse çok
gevşek.** Önceki projede `breakout_fvg` ve `flag_pennant` 4S'te 648/648
sembolde **sıfır aday** veriyordu ve bu çok sonra fark edildi.

### K4 · İstatistik — eleme değil ETİKETLEME

Sembol-kümelenmiş ileri getiri testi (bağımsız gözlem **bar değil sembol**),
IS/OOS ayrımı, permütasyon + BH-FDR. Sonuç ne çıkarsa pasaporta o yazılır ve
sitede o gösterilir.

Dört verdiktten biri: `olculmedi` · `kanitlanmadi` · `izlenen-aday` ·
`kenar-var`. "Zarar ettiriyor" ile "işe yaradığına dair kanıt yok" farklı
şeylerdir; hangisi olduğu yazılır.

### K5 · Görsel — kullanıcı onayı olmadan kapanmaz

Komposer yazılır (`packages/chart/quaxis/chart/komposer/<slug>.py`), gerçek
veriyle render edilir, ekran görüntüsü alınır, **referans görselle yan yana
konur**, düzeltilir — **en az 3 tur**. Her turda *ne görüldü, ne düzeltildi*
pasaporta yazılır; "düzeltildi" demek yetmez.

Araçlar: `tools/ekran_goruntusu.py`, `tools/kirp.py`, `tools/gorsel_kucult.py`.
Ayrıntı için `grafik-tasarim-sistemi` skill'i.

### K6 · Ürün

Kütüphane kartı, strateji sayfası, tarama kolonundaki verdikt rozeti, "nasıl
okunur" dört sorusu, alarm kuralı.

## Sıra seçimi

Bir sonraki stratejiyi seçerken üç ölçüt:

1. **Net bir referans görseli var mı** — K5'in hedefi lazım.
2. **Kitap kaynağı ne kadar somut** — K0 alıntı ister.
3. **İstatistiksel olarak henüz çürütülmemiş mi** — önceki ölçümde
   `trend.ewmac`, `structure.golden_zone`, `trend.ma_systems` en az çürütülmüş
   üçlüydü.
