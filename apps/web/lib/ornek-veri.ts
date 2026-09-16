/**
 * ÖRNEK VERİ — gerçek tarama çıktısı DEĞİLDİR. Yalnız **tasarım vitrini**
 * için: bileşenleri 500 satırda göstermek, boş durumu denemek, üç temayı yan
 * yana çizmek.
 *
 * Ürünün tarama yüzeyi artık buradan okumuyor — gerçek veri
 * [`tarama.ts`](./tarama.ts)'de ve `tools/tarama_disaktar.py` üretiyor.
 * Satır TİPİ oradan alınır: iki ayrı şekil tutmak, vitrinde çalışan bir
 * kolonun üründe kırılması demekti.
 *
 * Deterministik üreteç (aynı tohum = aynı satırlar) ve her yüzeyde
 * "örnek veri" etiketi korunur. README kural 6: ölçülmemiş bir iddia
 * "kanıtlanmış" diye sunulmaz.
 */

import type { TaramaSatiri, Verdikt, Yon } from "./tarama";

export type { TaramaSatiri, Verdikt, Yon };
export { OLGULAR, TARAMA_SAATI, VERDIKT_ACIKLAMA, yasEtiketi } from "./tarama";

/** Maketteki `rng` ile aynı doğrusal eşlenik üreteç — çıktı birebir tekrarlanır. */
function rng(seed: number) {
  let s = seed;
  return () => {
    s = (s * 1664525 + 1013904223) & 0x7fffffff;
    return s / 0x7fffffff;
  };
}

function seri(seed: number, yukari: boolean, n = 22) {
  const r = rng(seed);
  let v = 50;
  return Array.from({ length: n }, () => {
    v += (r() - 0.46) * 9 + (yukari ? 0.9 : -0.9);
    return Math.max(1, Math.min(99, v));
  });
}

/** Maketteki tarama tablosunun on satırı — birebir.
 *
 * Şirket adı alanı YOK: gerçek satırlarda da yok (evren dosyasında sembol
 * var, ad yok). Vitrindeki kolon düzeni üründekiyle aynı kalsın diye. */
const CEKIRDEK: Omit<
  TaramaSatiri,
  "id" | "seriAnahtari" | "zamanDilimi" | "gosterge" | "pasaport" | "stop" | "hedef"
>[] = [
  { sembol: "THYAO", paket: "Yapı", strateji: "Salınım Fibo ABCD", yon: "down", durum: "Tamamlandı", yas: 0, fiyat: 209.1, seviye: 178.45, verdikt: "kanıtlanmadı" },
  { sembol: "ASELS", paket: "Yapı", strateji: "Arz–Talep Bölgesi", yon: "up", durum: "Onaylandı", yas: 1, fiyat: 78.45, seviye: 74.2, verdikt: "ölçülmedi" },
  { sembol: "EREGL", paket: "Formasyon", strateji: "Çift Dip", yon: "up", durum: "Onaylandı", yas: 1, fiyat: 1204.75, seviye: 1180.0, verdikt: "kanıtlanmadı" },
  { sembol: "TUPRS", paket: "Trend & Momentum", strateji: "EWMAC", yon: "up", durum: "Onaylandı", yas: 2, fiyat: 142.3, seviye: 139.8, verdikt: "izlenen aday" },
  { sembol: "KCHOL", paket: "Yapı", strateji: "Piyasa Yapısı · BOS", yon: "up", durum: "Onaylandı", yas: 2, fiyat: 9.08, seviye: 8.94, verdikt: "ölçülmedi" },
  { sembol: "SISE", paket: "Formasyon", strateji: "Yükselen Üçgen", yon: "up", durum: "Kırılım", yas: 2, fiyat: 41.66, seviye: 40.9, verdikt: "kanıtlanmadı" },
  { sembol: "BIMAS", paket: "Yapı", strateji: "Yatay Aralık", yon: "down", durum: "Temas", yas: 3, fiyat: 512.0, seviye: 524.5, verdikt: "ölçülmedi" },
  { sembol: "FROTO", paket: "Formasyon", strateji: "Bayrak", yon: "up", durum: "Onaylandı", yas: 3, fiyat: 1088.25, seviye: 1061.0, verdikt: "kanıtlanmadı" },
  { sembol: "AKBNK", paket: "Trend & Momentum", strateji: "MA Sistemi", yon: "down", durum: "Onaylandı", yas: 3, fiyat: 68.9, seviye: 70.15, verdikt: "izlenen aday" },
  { sembol: "ENKAI", paket: "Yapı", strateji: "Salınım Fibo ABCD", yon: "up", durum: "Bölgede", yas: 3, fiyat: 58.44, seviye: 56.8, verdikt: "kanıtlanmadı" },
];

/** Vitrin satırları gerçek satırla AYNI şekli taşır — eksik alanlar burada
 * açıkça doldurulur, `as` ile kaçamak yapılmaz. */
/** Vitrin serileri — gerçek tarafta olduğu gibi satırdan AYRI bir sözlükte. */
const ORNEK_SERILER: Record<string, number[]> = {};

/** Vitrin satırının fiyat serisi. */
export function ornekSeri(satir: TaramaSatiri): number[] {
  return ORNEK_SERILER[satir.seriAnahtari] ?? [];
}

function vitrinSatiri(r: (typeof CEKIRDEK)[number], id: string, tohum: number): TaramaSatiri {
  const seriAnahtari = `${id}|1D`;
  ORNEK_SERILER[seriAnahtari] = seri(tohum, r.yon === "up");
  return {
    ...r,
    id,
    zamanDilimi: "1D",
    gosterge: "ornek",
    pasaport: "ornek",
    stop: null,
    hedef: null,
    seriAnahtari,
  };
}

export const ORNEK_TARAMA: TaramaSatiri[] = CEKIRDEK.map((r, k) =>
  vitrinSatiri(r, `${r.sembol}-${r.strateji}`, k * 7919 + 13),
);

const EKLER = ["A", "B", "C", "D", "E", "F", "G", "H", "İ", "K", "L", "M", "N", "O", "Ö", "P", "R", "S", "Ş", "T", "U", "Ü", "V", "Y", "Z"];
const DURUMLAR = ["Onaylandı", "Tamamlandı", "Kırılım", "Temas", "Bölgede"];
const VERDIKTLER: Verdikt[] = ["izlenen aday", "kanıtlanmadı", "ölçülmedi"];

/**
 * Sanallaştırma ölçümü için N satırlık deterministik örnek küme.
 * Semboller uydurmadır; gerçek BIST sembolleriyle karıştırılmasın diye
 * dört harfli türetilmiş kodlar kullanılır.
 */
export function ornekTarama(n: number): TaramaSatiri[] {
  if (n <= ORNEK_TARAMA.length) return ORNEK_TARAMA.slice(0, n);
  const r = rng(20260912);
  const out = [...ORNEK_TARAMA];
  for (let i = ORNEK_TARAMA.length; i < n; i++) {
    const taban = CEKIRDEK[i % CEKIRDEK.length];
    const kod =
      EKLER[Math.floor(r() * EKLER.length)] +
      EKLER[Math.floor(r() * EKLER.length)] +
      EKLER[Math.floor(r() * EKLER.length)] +
      EKLER[Math.floor(r() * EKLER.length)];
    const yon: Yon = r() > 0.42 ? "up" : "down";
    const fiyat = +(2 + r() * 1400).toFixed(2);
    out.push(
      vitrinSatiri(
        {
          sembol: kod,
          paket: taban.paket,
          strateji: taban.strateji,
          yon,
          durum: DURUMLAR[Math.floor(r() * DURUMLAR.length)],
          yas: Math.floor(r() * 11),
          fiyat,
          seviye: +(fiyat * (0.9 + r() * 0.2)).toFixed(2),
          verdikt: VERDIKTLER[Math.floor(r() * VERDIKTLER.length)],
        },
        `ornek-${i}`,
        i * 7919 + 13,
      ),
    );
  }
  return out;
}

/** Kütüphane kartları.
 *
 * **Dördü maket, beşi GERÇEK.** Harmonik kartlar ile Golden Zone kartı
 * ölçülmüş stratejilerdir: `kaynak` alanı kitabı, `kapi` alanı pasaportun
 * gerçekten geçtiği kapıyı, `verdikt` alanı K4'ün çıktısını taşır. Maket
 * kartların (`Piyasa Yapısı`, `Arz–Talep`, `Adil Değer Boşluğu`) arkasında
 * kod yoktur ve verdiktleri `ölçülmedi`dir — ikisi karışmasın diye bu not
 * burada duruyor.
 */
export type StratejiKarti = {
  ad: string;
  kaynak: string;
  kapi: string;
  tip: "fib" | "ms" | "zone" | "fvg";
  ozet: string;
  paket: string;
  verdikt: Verdikt;
};

export const ORNEK_KARTLAR: StratejiKarti[] = [
  {
    ad: "Harmonik · AB=CD",
    kaynak: "PESAVENTO · TWYS BÖL.4",
    kapi: "PASAPORT K4",
    tip: "fib",
    ozet:
      "Üç bacak, X yok. BC bacağı AB'yi geri çeker, CD bacağı AB kadar uzar; D bu iki ölçüden HESAPLANIR ve fiyat oraya dokununca sinyal doğar.",
    paket: "Formasyon",
    verdikt: "kanıtlanmadı",
  },
  {
    ad: "Harmonik · Gartley 222",
    kaynak: "PESAVENTO · TWYS BÖL.5",
    kapi: "PASAPORT K4",
    tip: "fib",
    ozet:
      "D, XA bacağının .786 geri çekilmesi; stop X'in hemen ötesi. Kitap ~%70 isabet iddia ediyor — 543 sembolde ölçülen %35.2.",
    paket: "Formasyon",
    verdikt: "kanıtlanmadı",
  },
  {
    ad: "Harmonik · Butterfly",
    kaynak: "PESAVENTO · TWYS BÖL.6",
    kapi: "PASAPORT K4",
    tip: "fib",
    ozet:
      "Uzantı formasyonu: D, XA'nın 1.272 uzantısında tamamlanır ve X'i AŞAR. Dört formasyonun ölçümde en kötüsü.",
    paket: "Formasyon",
    verdikt: "kanıtlanmadı",
  },
  {
    ad: "Harmonik · Three Drives",
    kaynak: "PESAVENTO · TWYS BÖL.7",
    kapi: "PASAPORT K4",
    tip: "fib",
    ozet:
      "Üç ardışık sürüş, her biri bir öncekinin 1.272 uzantısı. Stop oranı %75 — dördünün en yükseği.",
    paket: "Formasyon",
    verdikt: "kanıtlanmadı",
  },
  {
    ad: "Salınım Fibo ABCD",
    kaynak: "PESAVENTO · S.41-58",
    kapi: "PASAPORT K5",
    tip: "fib",
    ozet:
      "Baskın salınımın 0.618–0.786 düzeltme bandı. Fiyat bölgeye dönüp tutamazsa X seviyesinin altı hedeflenir.",
    paket: "Yapı",
    verdikt: "kanıtlanmadı",
  },
  {
    ad: "Piyasa Yapısı",
    kaynak: "SMC / ICT LİTERATÜRÜ",
    kapi: "PASAPORT K2",
    tip: "ms",
    ozet:
      "HH / HL / LH / LL zinciri ve bunların kırıldığı noktalar: BOS (yapı kırılımı) ve CHoCH (karakter değişimi).",
    paket: "Yapı",
    verdikt: "ölçülmedi",
  },
  {
    ad: "Arz–Talep Bölgesi",
    kaynak: "ORNEK2 REFERANSI",
    kapi: "PASAPORT K1",
    tip: "zone",
    ozet:
      "Pivot çıpalı bölge tespiti, birleştirme ve tazelik takibi. Hacim profili ikinci turda eklenecek.",
    paket: "Yapı",
    verdikt: "ölçülmedi",
  },
  {
    ad: "Adil Değer Boşluğu",
    kaynak: "YENİ STRATEJİ REFERANSI",
    kapi: "PASAPORT K0",
    tip: "fvg",
    ozet:
      "Üç barlık ardışık boşluk ve sonrasındaki konsolidasyondan kırılım. Kalibrasyon K3 kapısında ölçülecek.",
    paket: "Yapı",
    verdikt: "ölçülmedi",
  },
];
