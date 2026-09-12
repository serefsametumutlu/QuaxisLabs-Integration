/**
 * Yerel fontlar — CDN bağımlılığı yok.
 *
 * Üç yüz de Google Fonts deposundaki değişken (variable) TTF'lerden
 * latin + latin-ext + gerekli sembollere alt kümelenip woff2'ye sıkıştırıldı;
 * dosyalar `app/fonts/` altında depoyla birlikte taşınır.
 *
 * Alt küme, Türkçe glifleri (İ ı Ğ ğ Ş ş Ç ç Ö ö Ü ü) ve `tnum` (tabular-nums)
 * OpenType özelliğini KORUYACAK şekilde üretildi — sayı kolonlarının hizası
 * buna bağlı.
 */
import localFont from "next/font/local";

/** Display — başlıklar, marka. Negatif tracking ile kullanılır. */
export const archivo = localFont({
  src: "./fonts/Archivo.woff2",
  variable: "--font-display",
  weight: "100 900",
  display: "swap",
  fallback: ["Segoe UI", "system-ui", "sans-serif"],
});

/** Arayüz — gövde metni, etiketler, düğmeler. */
export const inter = localFont({
  src: "./fonts/Inter.woff2",
  variable: "--font-ui",
  weight: "100 900",
  display: "swap",
  fallback: ["Segoe UI", "system-ui", "sans-serif"],
});

/** Mono — HER sayı, eyebrow ve kod. */
export const jetbrainsMono = localFont({
  src: "./fonts/JetBrainsMono.woff2",
  variable: "--font-mono",
  weight: "100 800",
  display: "swap",
  fallback: ["ui-monospace", "Cascadia Mono", "monospace"],
});

export const fontVariables = [archivo.variable, inter.variable, jetbrainsMono.variable].join(" ");
