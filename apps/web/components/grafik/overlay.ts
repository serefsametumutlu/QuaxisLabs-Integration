/**
 * SVG overlay — strateji çizimleri.
 *
 * Mum, hacim, crosshair ve zoom/pan Lightweight Charts'tan gelir; formasyon
 * gövdeleri, fibo merdiveni, köşe rozetleri ve önder çizgili durum rozeti
 * burada çizilir. Sebep (ADR-001 §5): bu işaretlerin tipografisi ve etiket
 * yerleşimi tasarım şartnamesine birebir uymalı, hazır kütüphanelerin
 * sunduğu kaba kontrol yetmiyor.
 *
 * Bu dosya HESAP YAPMAZ: bütün fiyatlar ve zamanlar ChartSpec'ten gelir,
 * bütün renkler rol tablosundan. Katman ayrımı tek yönlüdür.
 */

import type { ChartSpec, MumSerisi } from "@/lib/chartspec";
import { cakismaCoz } from "./yerlesim";
import {
  alanStili,
  cizgiStili,
  etiketTokeni,
  isaretStili,
  rozetStili,
  seviyeStili,
  yonTokeni,
} from "./roller";

export type Cerceve = {
  genislik: number;
  yukseklik: number;
  /** Sağdaki etiket oluğunun genişliği. */
  oluk: number;
  dar: boolean;
  /** "vurgulu": yalnız karara değer seviyeler (0.618 / 0.786 / 1.272).
   *  Kısa levhalarda dokuz basamağın tamamı okunmaz bir yığına dönüşüyor. */
  seviyeler: "tam" | "vurgulu";
  x: (t: number) => number | null;
  y: (fiyat: number) => number | null;
  renk: (token: string) => string;
};

const NS = "http://www.w3.org/2000/svg";

function el<K extends keyof SVGElementTagNameMap>(
  tag: K,
  attrs: Record<string, string | number>,
  metin?: string,
): SVGElementTagNameMap[K] {
  const n = document.createElementNS(NS, tag);
  for (const k in attrs) n.setAttribute(k, String(attrs[k]));
  if (metin != null) n.textContent = metin;
  return n;
}

/**
 * Levhanın üstüne düşen metnin ARKASINA zemin koyar.
 *
 * Bir salınım etiketi yatay bir fibo çizgisinin tam üstüne denk geldiğinde
 * harfler çizgiyle karışıp okunmaz oluyordu (f4 görsel kabul bulgusu).
 *
 * İlk denenen `paint-order: stroke` YETMEDİ: kontur yalnız glif kenarını
 * korur, harflerin ARASINDAN geçen çizgiyi kapatmaz. Metin ölçülüp arkasına
 * gerçek bir dikdörtgen konur — `getBBox()` için öğenin önce DOM'da olması
 * gerektiğinden rect sonradan metnin önüne eklenir.
 */
function zeminEkle(svg: SVGSVGElement, t: SVGTextElement, c: Cerceve, pay = 3): void {
  let { x, y, width, height } = t.getBBox();
  if (!width) {
    // `getBBox()` yerleşim yapılmamış/gizli bir ağaçta 0 döner ve zemin
    // SESSİZCE çizilmez — çıkış etiketi mumların üstünde okunmaz kalıyordu
    // (K5 i4 bulgusu). Metin monospace olduğu için ölçüyü kestirmek
    // yeterince kesin: karakter genişliği punto × 0.6.
    const n = (t.textContent ?? "").length;
    if (!n) return;
    const punto = Number(t.getAttribute("font-size") ?? 11);
    width = n * punto * 0.6;
    height = punto * 1.25;
    const ax = Number(t.getAttribute("x") ?? 0);
    const ay = Number(t.getAttribute("y") ?? 0);
    const hiza = t.getAttribute("text-anchor");
    x = hiza === "middle" ? ax - width / 2 : hiza === "end" ? ax - width : ax;
    y = ay - punto;
  }
  svg.insertBefore(
    el("rect", {
      x: x - pay,
      y: y - 1,
      width: width + pay * 2,
      height: height + 2,
      fill: c.renk("--surface"),
      opacity: 0.9,
    }),
    t,
  );
}

export function ciz(svg: SVGSVGElement, spec: ChartSpec, c: Cerceve): void {
  svg.replaceChildren();
  if (c.genislik <= 0 || c.yukseklik <= 0) return;

  svg.setAttribute("width", String(c.genislik));
  svg.setAttribute("height", String(c.yukseklik));
  svg.setAttribute("viewBox", `0 0 ${c.genislik} ${c.yukseklik}`);

  const mono = c.renk("--f-mono") || "monospace";
  const sag = c.genislik - c.oluk; // çizim alanının sağ kenarı
  const katmanlar = spec.katmanlar ?? [];

  // Çizim sırası anlam taşır: geniş dolgular altta, ince çizgiler ve
  // metinler üstte. Aksan hiçbir zaman en üstteki dolu leke değildir.
  /** Sağ olukta yazılacak etiketler; çakışmaları en sonda çözülür. */
  const olukEtiketleri: { y: number; sabit?: boolean; metin: string; token: string }[] = [];

  const sirali = [
    ...katmanlar.filter((k) => k.tur === "bant"),
    ...katmanlar.filter((k) => k.tur === "alan"),
    ...katmanlar.filter((k) => k.tur === "seviye"),
    ...katmanlar.filter((k) => k.tur === "cizgi"),
    ...katmanlar.filter((k) => k.tur === "isaret"),
    ...katmanlar.filter((k) => k.tur === "etiket"),
    ...katmanlar.filter((k) => k.tur === "rozet"),
  ];

  for (const k of sirali) {
    switch (k.tur) {
      case "bant": {
        const s = alanStili(k.rol);
        const y1 = c.y(k.ust);
        const y2 = c.y(k.alt);
        if (y1 == null || y2 == null) break;
        const x0 = k.baslangic != null ? (c.x(k.baslangic) ?? 0) : 0;
        // Sonuçlanmış kurulumun bandı sağa uzamaz: artık geçerli olmayan
        // bir bölgeyi hâlâ varmış gibi göstermek olurdu.
        const x1 = k.bitis != null ? (c.x(k.bitis) ?? sag) : sag;
        svg.appendChild(
          el("rect", {
            x: x0,
            y: Math.min(y1, y2),
            width: Math.max(0, x1 - x0),
            height: Math.abs(y2 - y1),
            fill: c.renk(s.token),
            opacity: s.dolgu,
          }),
        );
        // Bant DAR ise etiket yazılmaz. Harmonik dönüş bölgesi son
        // pivottan çıkışa kadar sürüyor; 768 piksellik levhada bu birkaç
        // bar ediyordu ve "DÖNÜŞ BÖLGESİ" metni bandın dışına taşıp D köşe
        // rozetinin İÇİNDEN geçiyordu (K5 i3 bulgusu). Sığmayan etiket
        // bilgi değil, gürültüdür.
        const genis = x1 - x0 >= (k.etiket?.length ?? 0) * 6.2 + 18;
        if (k.etiket && genis) {
          // Bant inceyse etiket içine sığmaz ve alt çizginin üstüne biner
          // (f4i6 bulgusu); o zaman bandın ÜSTÜNE yazılır.
          const h = Math.abs(y2 - y1);
          const ustY = Math.min(y1, y2);
          const t = el(
            "text",
            {
              x: x0 + 8,
              y: h >= 24 ? ustY + h / 2 + 3.5 : ustY - 5,
              fill: c.renk(s.token),
              "font-family": mono,
              "font-size": 10,
              "letter-spacing": 1.4,
            },
            k.etiket,
          );
          svg.appendChild(t);
          zeminEkle(svg, t, c);
        }
        break;
      }

      case "alan": {
        const s = alanStili(k.rol);
        const nok = k.noktalar.map((n) => [c.x(n.t), c.y(n.fiyat)] as const);
        if (nok.some(([x, y]) => x == null || y == null)) break;
        const p = nok.map(([x, y]) => `${x},${y}`).join(" ");
        svg.appendChild(
          el("polygon", {
            points: p,
            fill: c.renk(s.token),
            opacity: s.dolgu,
            stroke: c.renk(s.token),
            "stroke-width": s.kenar,
            "stroke-opacity": s.kenarOpaklik,
          }),
        );
        break;
      }

      case "seviye": {
        const s = seviyeStili(k.rol);
        if (c.seviyeler === "vurgulu" && !s.vurgulu) break;
        const y = c.y(k.fiyat);
        if (y == null) break;
        const x0 = k.baslangic != null ? (c.x(k.baslangic) ?? 0) : 0;
        const xs = k.bitis != null ? (c.x(k.bitis) ?? sag + 4) : sag + 4;
        // Seviye bittikten SONRA çok soluk devam eder. Tamamen kesilirse
        // sağ oluktaki etiket neye ait olduğu belirsiz kalır; tam opak
        // devam ederse artık geçerli olmayan bir seviye hâlâ aktif görünür
        // (K5 i3 bulgusu). Hayalet uç ikisinin arasını tutar.
        if (k.bitis != null && xs < sag) {
          svg.appendChild(
            el("line", {
              x1: xs,
              x2: sag + 4,
              y1: y,
              y2: y,
              stroke: c.renk(s.token),
              "stroke-width": s.kalinlik,
              "stroke-dasharray": s.kesik,
              opacity: s.opaklik * 0.22,
            }),
          );
        }
        svg.appendChild(
          el("line", {
            x1: x0,
            x2: xs,
            y1: y,
            y2: y,
            stroke: c.renk(s.token),
            "stroke-width": s.kalinlik,
            "stroke-dasharray": s.kesik,
            opacity: s.opaklik,
          }),
        );
        olukEtiketleri.push({
          y,
          metin: c.dar ? kisalt(k.etiket) : k.etiket,
          token: s.token,
        });
        break;
      }

      case "cizgi": {
        const s = cizgiStili(k.rol);
        const nok = k.noktalar.map((n) => [c.x(n.t), c.y(n.fiyat)] as const);
        if (nok.some(([x, y]) => x == null || y == null)) break;
        const token = s.yonDuyarli && spec.kunye.yon ? yonTokeni(spec.kunye.yon) : s.token;
        svg.appendChild(
          el("polyline", {
            points: nok.map(([x, y]) => `${x},${y}`).join(" "),
            fill: "none",
            stroke: c.renk(token),
            "stroke-width": s.kalinlik,
            "stroke-dasharray": s.kesik,
            opacity: s.opaklik,
          }),
        );
        break;
      }

      case "isaret": {
        const s = isaretStili(k.rol);
        const x = c.x(k.nokta.t);
        const y = c.y(k.nokta.fiyat);
        if (x == null || y == null) break;
        const token = c.renk(s.token);
        svg.appendChild(
          el("circle", {
            cx: x,
            cy: y,
            r: s.yaricap,
            fill: token,
            stroke: c.renk("--surface"),
            "stroke-width": 1.4,
          }),
        );
        // Metni yalnız `hap` rollerinde çizmek, metin TAŞIYAN bir işaretin
        // metnini sessizce düşürüyordu: çıkış işareti ("stop ✕") 3 piksellik
        // görünmez bir noktaya iniyordu (K5 i3 bulgusu). Hapsız roller de
        // yazar — zemini `zeminEkle` ile, mumların üstünde okunsun diye.
        // HUD (sol üstteki sembol/strateji bloğu) bir HTML katmanı; SVG
        // onu göremez. Three Drives'ın `O` köşesi levhanın sol üstünde
        // duruyor ve rozeti tam HUD metninin İÇİNE düşüyordu (K5 i12).
        // Etiket o bölgeye denk gelirse noktanın altına yazılır.
        const hudIci = x < 230 && y < 104;
        if (!s.hap && k.metin) {
          const dy = hudIci || k.yerlesim === "alt" ? 15 : -13;
          const t = el(
            "text",
            {
              x,
              y: y + dy,
              fill: token,
              "font-family": mono,
              "font-size": 11,
              "font-weight": 500,
              "text-anchor": "middle",
            },
            k.metin,
          );
          svg.appendChild(t);
          zeminEkle(svg, t, c);
        }
        if (s.hap && k.metin) {
          const dy = hudIci || k.yerlesim === "alt" ? 16 : -16;
          svg.appendChild(
            el("rect", {
              x: x - 9,
              y: y + dy - 9,
              width: 18,
              height: 18,
              rx: 9,
              fill: token,
              opacity: 0.16,
              stroke: token,
              "stroke-width": 1,
              "stroke-opacity": 0.6,
            }),
          );
          svg.appendChild(
            el(
              "text",
              {
                x,
                y: y + dy + 4,
                fill: token,
                "font-family": mono,
                "font-size": 11,
                "font-weight": 500,
                "text-anchor": "middle",
              },
              k.metin,
            ),
          );
        }
        break;
      }

      case "etiket": {
        const x = c.x(k.nokta.t);
        const y = c.y(k.nokta.fiyat);
        if (x == null || y == null) break;
        const dy = k.yerlesim === "alt" ? 34 : -34;
        const t = el(
          "text",
          {
            x,
            y: y + dy,
            fill: c.renk(etiketTokeni(k.rol)),
            "font-family": mono,
            "font-size": 9.5,
            "text-anchor": "middle",
          },
          k.metin,
        );
        svg.appendChild(t);
        zeminEkle(svg, t, c);
        break;
      }

      case "rozet": {
        // Çapası görünür alanın dışındaysa rozet çizilmez. Kenara
        // sıkıştırmak onu ait olmadığı bir bara bağlarmış gibi gösterirdi
        // (i2, "1A" aralığı bulgusu).
        {
          const cx = c.x(k.nokta.t);
          if (cx == null || cx < 0 || cx > sag) break;
        }
        const s = rozetStili(k.rol);
        const x = c.x(k.nokta.t);
        const y = c.y(k.nokta.fiyat);
        if (x == null || y == null) break;
        const token = c.renk(s.yonDuyarli ? yonTokeni(k.yon) : s.token);
        const g = 11 + k.metin.length * 6.6;
        // Rozet noktanın soluna ve altına oturur; önder çizgi ikisini bağlar.
        const bx = Math.min(Math.max(4, x - g - 22), sag - g - 4);
        const by = y + 46;
        svg.appendChild(
          el("line", { x1: x, y1: y + 6, x2: bx + g, y2: by - 7, stroke: token, "stroke-width": 1, opacity: 0.6 }),
        );
        svg.appendChild(
          el("rect", {
            x: bx,
            y: by - 16,
            width: g,
            height: 22,
            rx: 2,
            fill: c.renk("--surface"),
            stroke: token,
            "stroke-width": 1,
            "stroke-opacity": 0.7,
          }),
        );
        svg.appendChild(
          el("text", { x: bx + 9, y: by, fill: token, "font-family": mono, "font-size": 11 }, k.metin),
        );
        break;
      }
    }
  }

  sonFiyatRozeti(svg, spec, c, sag, mono, olukEtiketleri);
  olugaYaz(svg, c, sag, mono, olukEtiketleri);
}

/** Etiketleri çakışmayı çözerek sağ oluğa yazar; hangi satıra kaydıysa
 *  çizgisine ince bir bağ çizer ki hangi seviyenin etiketi olduğu kaybolmasın. */
function olugaYaz(
  svg: SVGSVGElement,
  c: Cerceve,
  sag: number,
  mono: string,
  ogeler: { y: number; sabit?: boolean; metin: string; token: string; rozet?: boolean }[],
): void {
  // 18px: son fiyat rozeti 17px yüksekliğinde bir kutu; 14px aralık onu
  // komşu etiketin altında bırakıyordu (f4i2 bulgusu).
  const yerlesik = cakismaCoz(ogeler, { aralik: c.dar ? 16 : 20, alt: 10, ust: c.yukseklik - 10 });
  for (const o of yerlesik) {
    if (o.rozet) continue; // son fiyat rozeti kendi kutusuyla çizildi
    const kaydi = Math.abs(o.yerlesikY - o.y) > 1;
    if (kaydi) {
      svg.appendChild(
        el("path", {
          d: `M ${sag + 4} ${o.y} L ${sag + 9} ${o.yerlesikY}`,
          stroke: c.renk(o.token),
          "stroke-width": 1,
          fill: "none",
          opacity: 0.45,
        }),
      );
    }
    svg.appendChild(
      el(
        "text",
        {
          x: sag + 12,
          y: o.yerlesikY + 3.4,
          fill: c.renk(o.token),
          "font-family": mono,
          "font-size": c.dar ? 9 : 10.5,
          "text-anchor": "start",
        },
        o.metin,
      ),
    );
  }
}

/** Son kapanış: levha kromu, strateji çizimi değil. Yön künyeden gelir. */
function sonFiyatRozeti(
  svg: SVGSVGElement,
  spec: ChartSpec,
  c: Cerceve,
  sag: number,
  mono: string,
  oluk: { y: number; sabit?: boolean; metin: string; token: string; rozet?: boolean }[],
): void {
  const mum = spec.seriler.find((s): s is MumSerisi => s.tur === "mum");
  const son = mum?.veri.at(-1);
  if (!son) return;
  const y = c.y(son.kapanis);
  if (y == null) return;

  const tokenAdi = yonTokeni(spec.kunye.yon ?? (son.kapanis >= son.acilis ? "al" : "sat"));
  const token = c.renk(tokenAdi);
  const g = c.dar ? 62 : 74;
  // Rozet SABİT: fibo etiketleri ondan kaçar, o yerinden oynamaz —
  // son fiyat grafiğin en çok bakılan sayısıdır.
  oluk.push({ y, sabit: true, metin: son.kapanis.toFixed(2), token: tokenAdi, rozet: true });
  svg.appendChild(
    el("line", {
      x1: 0,
      x2: sag + 4,
      y1: y,
      y2: y,
      stroke: token,
      "stroke-width": 1,
      "stroke-dasharray": "1 3",
      opacity: 0.8,
    }),
  );
  svg.appendChild(el("rect", { x: sag + 4, y: y - 8.5, width: g, height: 17, rx: 2, fill: token }));
  svg.appendChild(
    el(
      "text",
      {
        x: sag + 11,
        y: y + 3.6,
        fill: c.renk("--surface"),
        "font-family": mono,
        "font-size": 10.5,
      },
      son.kapanis.toFixed(2),
    ),
  );
}

/** Dar levhada "0.618 (A): 185.00" -> "0.618: 185.00". */
function kisalt(etiket: string): string {
  return etiket.replace(/\s*\([^)]*\)/, "");
}
