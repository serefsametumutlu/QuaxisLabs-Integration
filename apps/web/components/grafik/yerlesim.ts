/**
 * Sağ oluktaki etiketlerin dikey çakışmasını çözer.
 *
 * Fibo merdiveninin iki basamağı birbirine yaklaştığında ya da son fiyat
 * rozeti bir seviyenin üstüne denk geldiğinde etiketler üst üste biner ve
 * ikisi de okunmaz olur — referans kalitesinde bir grafikte kabul edilemez.
 *
 * Yöntem: sabit öğe (son fiyat rozeti) yerinde kalır, diğerleri ondan uzağa
 * itilir. Sıra korunur — etiketler birbirinin önüne geçmez, yalnız aralarındaki
 * boşluk açılır. Çizici, kayan etiketi çizgisine ince bir bağla bağlar.
 */

export type OlukOgesi = {
  /** Doğal y — çizgisinin bulunduğu yer. */
  y: number;
  /** Son fiyat rozeti gibi kaymaması gerekenler. */
  sabit?: boolean;
};

export type Secenek = { aralik?: number; alt?: number; ust?: number };

export function cakismaCoz<T extends OlukOgesi>(
  ogeler: T[],
  { aralik = 14, alt = 0, ust = Infinity }: Secenek = {},
): (T & { yerlesikY: number })[] {
  const n = ogeler.length;
  if (n === 0) return [];

  const sira = ogeler.map((_, i) => i).sort((a, b) => ogeler[a].y - ogeler[b].y);
  const y = ogeler.map((o) => o.y);
  const sabit = sira.findIndex((i) => ogeler[i].sabit);
  const cikis = sabit >= 0 ? sabit : 0;

  for (let k = cikis + 1; k < n; k++) {
    y[sira[k]] = Math.max(y[sira[k]], y[sira[k - 1]] + aralik);
  }
  for (let k = cikis - 1; k >= 0; k--) {
    y[sira[k]] = Math.min(y[sira[k]], y[sira[k + 1]] - aralik);
  }

  // Levhanın dışına taşarsa tüm grubu birlikte kaydır — sıra bozulmasın.
  const tasmaUst = alt - Math.min(...y);
  if (tasmaUst > 0) for (let i = 0; i < n; i++) y[i] += tasmaUst;
  const tasmaAlt = Math.max(...y) - ust;
  if (tasmaAlt > 0) for (let i = 0; i < n; i++) y[i] -= tasmaAlt;

  return ogeler.map((o, i) => ({ ...o, yerlesikY: y[i] }));
}
