/**
 * ÖRNEK VERİ — gerçek tarama çıktısı DEĞİLDİR.
 *
 * Faz 2'de API, gösterge ve gerçek veri yok. Buradaki her şey deterministik
 * bir üreteçten gelir (aynı tohum = aynı satırlar) ve arayüzde her zaman
 * "örnek veri" etiketiyle gösterilir. README kural 6: ölçülmemiş bir iddia
 * "kanıtlanmış" diye sunulmaz.
 */

/** Kapanış taraması saati. Tek yerde dursun: duyuru şeridi ve üst bar okur. */
export const TARAMA_SAATI = { saat: 18, dakika: 15, metin: "18:15" } as const;

/** Giriş ekranındaki olgu şeridi — hepsi doğrulanabilir sayılar. */
export const OLGULAR = [
  { n: "648", t: "BIST sembolü" },
  { n: "4S + 1G", t: "zaman dilimi" },
  { n: "7", t: "kapılı strateji süreci" },
  { n: "586", t: "sembolde OOS ölçümü" },
] as const;

export type Yon = "up" | "down";
export type Verdikt = "izlenen aday" | "kanıtlanmadı" | "ölçülmedi";

export type TaramaSatiri = {
  id: string;
  sembol: string;
  ad: string;
  paket: string;
  strateji: string;
  yon: Yon;
  durum: string;
  yas: number;
  fiyat: number;
  seviye: number;
  seri: number[];
  verdikt: Verdikt;
};

export const VERDIKT_ACIKLAMA: Record<Verdikt, string> = {
  "izlenen aday": "en az çürütülmüş üçlüden biri",
  "kanıtlanmadı": "FDR eşiğini geçemedi",
  "ölçülmedi": "K4 kapısı henüz açılmadı",
};

/** Maketteki `rng` ile aynı doğrusal eşlenik üreteç — çıktı birebir tekrarlanır. */
function rng(seed: number) {
  let s = seed;
  return () => {
    s = (s * 1664525 + 1013904223) & 0x7fffffff;
    return s / 0x7fffffff;
  };
}

export function yasEtiketi(n: number) {
  return n === 0 ? "son mum" : `${n} mum önce`;
}

function seri(seed: number, yukari: boolean, n = 22) {
  const r = rng(seed);
  let v = 50;
  return Array.from({ length: n }, () => {
    v += (r() - 0.46) * 9 + (yukari ? 0.9 : -0.9);
    return Math.max(1, Math.min(99, v));
  });
}

/** Maketteki tarama tablosunun on satırı — birebir. */
const CEKIRDEK: Omit<TaramaSatiri, "id" | "seri">[] = [
  { sembol: "THYAO", ad: "Türk Hava Yolları", paket: "Yapı", strateji: "Salınım Fibo ABCD", yon: "down", durum: "Tamamlandı", yas: 0, fiyat: 209.1, seviye: 178.45, verdikt: "kanıtlanmadı" },
  { sembol: "ASELS", ad: "Aselsan", paket: "Yapı", strateji: "Arz–Talep Bölgesi", yon: "up", durum: "Onaylandı", yas: 1, fiyat: 78.45, seviye: 74.2, verdikt: "ölçülmedi" },
  { sembol: "EREGL", ad: "Ereğli Demir Çelik", paket: "Formasyon", strateji: "Çift Dip", yon: "up", durum: "Onaylandı", yas: 1, fiyat: 1204.75, seviye: 1180.0, verdikt: "kanıtlanmadı" },
  { sembol: "TUPRS", ad: "Tüpraş", paket: "Trend & Momentum", strateji: "EWMAC", yon: "up", durum: "Onaylandı", yas: 2, fiyat: 142.3, seviye: 139.8, verdikt: "izlenen aday" },
  { sembol: "KCHOL", ad: "Koç Holding", paket: "Yapı", strateji: "Piyasa Yapısı · BOS", yon: "up", durum: "Onaylandı", yas: 2, fiyat: 9.08, seviye: 8.94, verdikt: "ölçülmedi" },
  { sembol: "SISE", ad: "Şişecam", paket: "Formasyon", strateji: "Yükselen Üçgen", yon: "up", durum: "Kırılım", yas: 2, fiyat: 41.66, seviye: 40.9, verdikt: "kanıtlanmadı" },
  { sembol: "BIMAS", ad: "BİM", paket: "Yapı", strateji: "Yatay Aralık", yon: "down", durum: "Temas", yas: 3, fiyat: 512.0, seviye: 524.5, verdikt: "ölçülmedi" },
  { sembol: "FROTO", ad: "Ford Otosan", paket: "Formasyon", strateji: "Bayrak", yon: "up", durum: "Onaylandı", yas: 3, fiyat: 1088.25, seviye: 1061.0, verdikt: "kanıtlanmadı" },
  { sembol: "AKBNK", ad: "Akbank", paket: "Trend & Momentum", strateji: "MA Sistemi", yon: "down", durum: "Onaylandı", yas: 3, fiyat: 68.9, seviye: 70.15, verdikt: "izlenen aday" },
  { sembol: "ENKAI", ad: "Enka İnşaat", paket: "Yapı", strateji: "Salınım Fibo ABCD", yon: "up", durum: "Bölgede", yas: 3, fiyat: 58.44, seviye: 56.8, verdikt: "kanıtlanmadı" },
];

export const ORNEK_TARAMA: TaramaSatiri[] = CEKIRDEK.map((r, k) => ({
  ...r,
  id: `${r.sembol}-${r.strateji}`,
  seri: seri(k * 7919 + 13, r.yon === "up"),
}));

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
    out.push({
      id: `ornek-${i}`,
      sembol: kod,
      ad: `Örnek Ortaklık ${i}`,
      paket: taban.paket,
      strateji: taban.strateji,
      yon,
      durum: DURUMLAR[Math.floor(r() * DURUMLAR.length)],
      yas: Math.floor(r() * 11),
      fiyat,
      seviye: +(fiyat * (0.9 + r() * 0.2)).toFixed(2),
      seri: seri(i * 7919 + 13, yon === "up"),
      verdikt: VERDIKTLER[Math.floor(r() * VERDIKTLER.length)],
    });
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
