/**
 * Grafik yüzeyinin gösterdiği stratejiler — spec + okuma notları + verdikt.
 *
 * Neden bir kayıt defteri: grafik sayfası önce tek bir stratejiye (Golden
 * Zone) gömülüydü ve istatistik kutusu `0.62`, `0.705`, `BOS` gibi O
 * stratejiye ait etiketleri **elle** taşıyordu. İkinci bir strateji
 * eklenince o kutunun kopyalanması gerekirdi ve kopyalanan sayılar
 * spec'ten kopardı.
 *
 * Şimdi istatistik kutusu spec'in KENDİ seviye etiketlerinden üretiliyor;
 * burada yalnız stratejiye özgü METİN duruyor.
 *
 * **Verdikt metinleri ölçüm dosyalarından gelir**, tahminden değil. Her
 * satırın kaynağı `docs/olcum/` altında adıyla yazılı.
 */

import {
  HARMONIK_ABCD,
  HARMONIK_GARTLEY,
  HARMONIK_KELEBEK,
  HARMONIK_UC_SURUS,
  THYAO_GOLDEN_ZONE,
} from "./ornek-chartspec";
import type { ChartSpec } from "./chartspec";

export type VitrinNotu = { baslik: string; govde: string };

export type VitrinKaydi = {
  /** Seçicideki kısa ad. */
  etiket: string;
  spec: ChartSpec;
  /** Levhanın altındaki üç not — TASARIM_DILI §7. */
  notlar: VitrinNotu[];
  /** K4 kutusu. `kanit` ölçüm dosyasının adıdır; uydurma sayı yasak. */
  verdikt: { govde: string; kanit: string };
};

/** Harmoniklerin dördü de aynı ölçüm koşusundan gelir. */
const HARMONIK_KANIT = "docs/olcum/harmonik-pesavento-K4-1D-long.md";

/**
 * Dört formasyonun PAYLAŞTIĞI iki not. Üçüncüsü formasyona özgü.
 *
 * Ortak tutulmasının sebebi: dördü de aynı mekanizmayla çalışıyor ve
 * kullanıcının öğrenmesi gereken şey o mekanizma. Her formasyona ayrı
 * "sinyal ne zaman doğar" yazmak, dördünü dört ayrı şey gibi gösterirdi.
 */
const HARMONIK_ORTAK: VitrinNotu[] = [
  {
    baslik: "Sinyal ne zaman doğar",
    govde:
      "Fiyat D seviyesine dokunduğu anda. D bir pivot DEĞİL: son köşe (C) onaylandığında hesaplanan bir fiyattır. Bu yüzden kesik çizgiyle çizilir — o bacak henüz gerçekleşmedi, hesaplandı.",
  },
  {
    baslik: "Sinyal sonradan kaybolur mu",
    govde:
      "Hayır. Köşeler kendi barlarından üç–beş bar sonra kesinleşir ve bir daha değişmez; D onlardan hesaplanır. C onaylanmadan fiyat D'ye inerse sinyal HİÇ üretilmez — o an formasyonun varlığını bilmiyorduk.",
  },
];

export const VITRIN: Record<string, VitrinKaydi> = {
  "golden-zone": {
    etiket: "Golden Zone",
    spec: THYAO_GOLDEN_ZONE,
    notlar: [
      {
        baslik: "Neden bölge burada",
        govde:
          "Fibonacci, süpürme ucundan (%100) yer değiştirmenin ucuna (%0) çekilir. Bölge o bacağın 0.62–0.79 düzeltmesidir — grafikteki kesik çizgi bacağın kendisi.",
      },
      {
        baslik: "Asimetri nereden geliyor",
        govde:
          "Düzeltme tepeden ölçülür: derine girmek stop'u küçültür, hedefi uzaklaştırmaz. 0.62'de ödül/risk 1.63, 0.705'te 2.39, 0.79'da 3.76.",
      },
      {
        baslik: "Geçersizlik",
        govde:
          "%100 seviyesinin ötesinde GÖVDE kapanışı kurulumu bitirir. Wick geçebilir — wick'i de geçersiz saymak sinyal sayısını sessizce yarıya indirirdi.",
      },
    ],
    verdikt: {
      govde:
        "543 BIST sembolü, 8432 işlem, sembol-kümelenmiş, IS/OOS ayrımlı, üç bariyerli R ölçümü: işlem başına +0.045R, aynı risk yapısıyla rastgele girişin bazı +0.071R (p=0.95). Teyit katmanları (FVG / order block / süpürme) değer eklemedi, eksiltti.",
      kanit: "docs/olcum/golden-zone-K4-katmanli-2026-09-13.md",
    },
  },

  "harmonik-abcd": {
    etiket: "AB=CD",
    spec: HARMONIK_ABCD,
    notlar: [
      {
        baslik: "Üç bacak, X yok",
        govde:
          "BC bacağı AB'yi geri çeker (.382–.786), CD bacağı AB kadar uzar. D bu iki ölçüden hesaplanır. BC, AB'yi aşarsa formasyon geçersizdir.",
      },
      ...HARMONIK_ORTAK,
    ],
    verdikt: {
      govde:
        "2413 işlem, 451 sembol. İşlem başına +0.148R — ama aynı risk yapısıyla rastgele girişin bazı +0.323R. Fark NEGATİF (−0.176R). Ödül/risk ~3.2:1 olduğu için %25 isabet başabaştır; ölçülen %32.8 pozitif R verir ama rastgele giriş de aynısını veriyor.",
      kanit: HARMONIK_KANIT,
    },
  },

  "harmonik-gartley": {
    etiket: "Gartley 222",
    spec: HARMONIK_GARTLEY,
    notlar: [
      {
        baslik: "D neden tam .786'da",
        govde:
          "Kitabın bütün ticaret örneklerinde D, XA bacağının .786 geri çekilmesidir. Stop X'in hemen ötesine konur — yani risk XA'nın %21.4'ü kadardır.",
      },
      ...HARMONIK_ORTAK,
    ],
    verdikt: {
      govde:
        "Kitap Gartley için ~%70 isabet iddia ediyor. Ölçülen: %35.2 (108 işlem, 92 sembol). İşlem başına +0.053R, adil baz +0.240R — fark negatif. İddia doğrulanmadı.",
      kanit: HARMONIK_KANIT,
    },
  },

  "harmonik-kelebek": {
    etiket: "Butterfly",
    spec: HARMONIK_KELEBEK,
    notlar: [
      {
        baslik: "D neden X'in ötesinde",
        govde:
          "Kelebek bir uzantı formasyonudur: D, XA'nın 1.272 uzantısında tamamlanır ve X'i AŞAR. Stop 1.618'in dışındadır. 2.618'i aşan bir D formasyon sayılmaz.",
      },
      ...HARMONIK_ORTAK,
    ],
    verdikt: {
      govde:
        "138 işlem, 113 sembol. İşlem başına −0.195R, adil baz +0.228R — dört formasyonun en kötüsü (fark −0.423R). Kaynak da uyarıyor: Kelebek başarısız olduğunda hızlı ve büyük hareketle başarısız olur.",
      kanit: HARMONIK_KANIT,
    },
  },

  "harmonik-uc-surus": {
    etiket: "Three Drives",
    spec: HARMONIK_UC_SURUS,
    notlar: [
      {
        baslik: "Üç ardışık sürüş",
        govde:
          "Her sürüş, kendinden önceki geri çekilmenin 1.272 uzantısıdır; aradaki geri çekilmeler .618/.786 olur. Üçüncü sürüşün tamamlanma seviyesi D'dir.",
      },
      ...HARMONIK_ORTAK,
    ],
    verdikt: {
      govde:
        "142 işlem, 117 sembol. İşlem başına −0.256R, adil baz +0.150R. Stop oranı %75 — dördünün en yükseği. Kaynak bu formasyonun başarısız örneklerinin geriye dönük bakıldığında bile fark edilmesinin zor olduğunu söylüyor; hayatta kalma yanlılığı riski en yüksek olan bu.",
      kanit: HARMONIK_KANIT,
    },
  },
};

export const VITRIN_SIRASI = [
  "golden-zone",
  "harmonik-abcd",
  "harmonik-gartley",
  "harmonik-kelebek",
  "harmonik-uc-surus",
] as const;

/** Seçici seçenekleri — sıra kayıt defterinden gelir, elle yazılmaz. */
export const VITRIN_SECENEKLERI = VITRIN_SIRASI.map((slug) => ({
  value: slug,
  label: VITRIN[slug].etiket,
}));

/**
 * Spec'in seviye katmanlarını istatistik satırlarına çevirir.
 *
 * Etiketi spec'in KENDİSİ taşıyor (`0.786 (giriş): 12.34`) — komposer onu
 * zaten üretmiş durumda. Burada yeniden biçimlendirmek aynı sayıyı iki
 * yerde yazmak olurdu ve ikisi er geç ayrışırdı.
 */
export function seviyeSatirlari(
  spec: ChartSpec,
): { ad: string; deger: string; rol: string }[] {
  return (spec.katmanlar ?? [])
    .filter((k) => k.tur === "seviye")
    .map((k) => {
      const parca = k.etiket.split(": ");
      return {
        ad: parca[0] ?? k.etiket,
        deger: parca[1] ?? "",
        rol: k.rol,
      };
    });
}

/** Ödül/risk — seviyelerden TÜRETİLİR, elle yazılmaz. */
export function odulRisk(spec: ChartSpec): number | null {
  const bul = (ara: string) =>
    (spec.katmanlar ?? []).find(
      (k) => k.tur === "seviye" && k.etiket.includes(`(${ara})`),
    );
  const g = bul("giriş");
  const s = bul("stop");
  const h = bul("hedef");
  if (!g || !s || !h) return null;
  if (g.tur !== "seviye" || s.tur !== "seviye" || h.tur !== "seviye") return null;
  const risk = Math.abs(g.fiyat - s.fiyat);
  return risk > 0 ? Math.abs(h.fiyat - g.fiyat) / risk : null;
}
