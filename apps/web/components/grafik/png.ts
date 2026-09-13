/**
 * Levhayı PNG olarak indirme.
 *
 * Levha İKİ katmandan oluşuyor: mumlar/hacim bir `<canvas>` üzerinde
 * (Lightweight Charts), fibo seviyeleri ve rozetler bizim SVG katmanımızda.
 * Tek başına hiçbiri grafiğin tamamı değil — ikisi birleştirilmeli.
 *
 * Sıra önemli: zemin → tuval → SVG. Ekrandaki yığınlama sırasıyla AYNI
 * (bkz. `grafik.css`'teki `isolation: isolate` notu); farklı olsaydı
 * indirilen görüntü ekranda görünenden başka bir şey olurdu.
 *
 * SVG'yi resme çevirmek için serileştirip `data:` URI yapıyoruz. Bu,
 * SVG'nin KENDİ KENDİNE YETER olmasını gerektirir: dış CSS'e, değişkene
 * ya da fonta bağımlı olamaz. Overlay zaten token'ları gerçek renk
 * değerlerine çözüp yazıyor (bkz. `roller.ts::tokenRengi`), font ailesi
 * de satır içi veriliyor — bu yüzden çalışıyor.
 */
import type { IChartApi } from "lightweight-charts";
import type { ChartSpec } from "@/lib/chartspec";

/** `ad.png` — sembol, strateji ve tarih. Dosya adı ne olduğunu söylesin. */
function dosyaAdi(spec: ChartSpec): string {
  const tarih = new Date().toISOString().slice(0, 10);
  const parca = [spec.kunye.sembol, spec.kunye.strateji, spec.kunye.zaman_dilimi, tarih]
    .filter(Boolean)
    .join("-");
  return `${parca.toLocaleLowerCase("tr")}.png`;
}

function svgResmi(svg: SVGSVGElement, genislik: number, yukseklik: number): Promise<HTMLImageElement> {
  const kopya = svg.cloneNode(true) as SVGSVGElement;
  kopya.setAttribute("xmlns", "http://www.w3.org/2000/svg");
  kopya.setAttribute("width", String(genislik));
  kopya.setAttribute("height", String(yukseklik));
  kopya.setAttribute("viewBox", `0 0 ${genislik} ${yukseklik}`);

  const metin = new XMLSerializer().serializeToString(kopya);
  const uri = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(metin)}`;
  return new Promise((coz, at) => {
    const img = new Image();
    img.onload = () => coz(img);
    img.onerror = () => at(new Error("SVG katmanı resme çevrilemedi."));
    img.src = uri;
  });
}

/**
 * İndirilen görüntüye künyeyi yazar.
 *
 * Ekrandaki künye bir HTML katmanı (HUD); tuvale de SVG'ye de girmiyor.
 * Onsuz indirilen PNG **neyin grafiği olduğunu söylemiyordu** — paylaşılan
 * bir görüntü için bu kabul edilemez.
 *
 * Verdikt de buraya yazılır ve bu bir tercih değil zorunluluk: "kurulum
 * oluştu" ile "bu stratejinin kenar ürettiği kanıtlandı" ayrı şeyler.
 * Verdikti taşımayan bir grafik, paylaşıldığında ikincisini ima eder.
 */
const KUNYE_YUKSEKLIK = 26;

function kunyeYaz(
  ctx: CanvasRenderingContext2D,
  spec: ChartSpec,
  genislik: number,
): void {
  const k = spec.kunye;
  const stil = getComputedStyle(document.documentElement);
  const mono = stil.getPropertyValue("--f-mono").trim() || "monospace";
  const metin = stil.getPropertyValue("--text").trim() || "#111";
  const soluk = stil.getPropertyValue("--text-3").trim() || "#888";

  const sol = [k.sembol, k.zaman_dilimi, k.strateji_adi ?? k.strateji]
    .filter(Boolean)
    .join("  ·  ");
  const taban = KUNYE_YUKSEKLIK - 9;
  ctx.font = `500 12px ${mono}`;
  ctx.fillStyle = metin;
  ctx.textAlign = "left";
  ctx.fillText(sol, 12, taban);

  const sag: string[] = [];
  if (k.verdikt) sag.push(`tarihsel isabet: ${k.verdikt}`);
  if (k.ornek_mi) sag.push("ÖRNEK VERİ");
  if (sag.length) {
    ctx.font = `400 11px ${mono}`;
    ctx.fillStyle = soluk;
    ctx.textAlign = "right";
    ctx.fillText(sag.join("  ·  "), genislik - 12, taban);
  }
  // İnce ayraç: künye bandı ile levha birbirine karışmasın.
  const cizgi = stil.getPropertyValue("--line").trim();
  if (cizgi) {
    ctx.fillStyle = cizgi;
    ctx.fillRect(0, KUNYE_YUKSEKLIK - 1, genislik, 1);
  }
}

export async function pngIndir(
  chart: IChartApi,
  svg: SVGSVGElement,
  sarmal: HTMLElement,
  spec: ChartSpec,
  oluk: number,
): Promise<void> {
  const genislik = sarmal.clientWidth;
  const yukseklik = sarmal.clientHeight;
  // Retina'da 1:1 kaydetmek metinleri bulanık bırakırdı.
  const olcek = Math.min(window.devicePixelRatio || 1, 2);

  // Künye bandı levhanın ÜSTÜNE eklenir, üstüne YAZILMAZ: levhanın içine
  // yazılınca sağ oluktaki fiyat etiketleriyle çakışıyordu (i3 bulgusu) —
  // ekrandaki araç şeridinde yaşanan sorunun aynısı.
  const hedef = document.createElement("canvas");
  hedef.width = Math.round(genislik * olcek);
  hedef.height = Math.round((yukseklik + KUNYE_YUKSEKLIK) * olcek);
  const ctx = hedef.getContext("2d");
  if (!ctx) throw new Error("2D bağlamı alınamadı — PNG üretilemiyor.");
  ctx.scale(olcek, olcek);

  // Zemin: levhanın kendi rengi. Saydam bırakılırsa PNG koyu temada
  // okunmaz olur (çoğu görüntüleyici saydamı beyaza basar).
  const zemin = getComputedStyle(document.documentElement)
    .getPropertyValue("--surface")
    .trim();
  ctx.fillStyle = zemin || "#ffffff";
  ctx.fillRect(0, 0, genislik, yukseklik + KUNYE_YUKSEKLIK);

  kunyeYaz(ctx, spec, genislik);
  ctx.translate(0, KUNYE_YUKSEKLIK);

  // Tuval katmanı: oluk kadar içeride durur (ekrandaki gibi).
  const tuval = chart.takeScreenshot();
  ctx.drawImage(tuval, 0, 0, Math.max(0, genislik - oluk), yukseklik);

  // SVG katmanı: tam genişlik, tuvalin ÜSTÜNE.
  ctx.drawImage(await svgResmi(svg, genislik, yukseklik), 0, 0, genislik, yukseklik);

  const blob: Blob = await new Promise((coz, at) =>
    hedef.toBlob((b) => (b ? coz(b) : at(new Error("PNG üretilemedi."))), "image/png"),
  );
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = dosyaAdi(spec);
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}
