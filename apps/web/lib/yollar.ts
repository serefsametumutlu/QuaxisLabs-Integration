/** Gezinme tablosu — sol ray, üst şerit ve Ctrl+K paleti aynı kaynaktan okur. */

export type Yuzey = {
  ad: string;
  yol: string;
  sayac?: string;
  /** Faz 3'te yalnız iskeleti var; içerik sonraki fazlarda dolacak. */
  hazir?: boolean;
};

export const YUZEYLER: Yuzey[] = [
  { ad: "Tarama", yol: "/tarama", sayac: "47", hazir: true },
  { ad: "Grafik", yol: "/grafik", hazir: true },
  { ad: "Strateji Kütüphanesi", yol: "/stratejiler", sayac: "4", hazir: true },
  { ad: "Tasarım Sistemi", yol: "/tasarim", hazir: true },
];

export const PAKETLER = [
  { ad: "Yapı", sayac: "4", yol: "/stratejiler?paket=yapi" },
  { ad: "Formasyon", sayac: "3", yol: "/stratejiler?paket=formasyon" },
  { ad: "Trend & Momentum", sayac: "2", yol: "/stratejiler?paket=trend" },
  { ad: "İstatistiksel Arbitraj", sayac: "0", yol: "/stratejiler?paket=arbitraj", pasif: true },
];

export const EVREN = [
  { ad: "BIST Tümü", sayac: "648", yol: "/tarama" },
  { ad: "Takip listem", sayac: "21", yol: "/tarama?liste=takip" },
];

export const PAZARLAMA_MENU = [
  { ad: "Tarama", yol: "/tarama" },
  { ad: "Stratejiler", yol: "/stratejiler" },
  { ad: "Grafik", yol: "/grafik" },
  { ad: "Yöntem", yol: "/#yontem" },
];
