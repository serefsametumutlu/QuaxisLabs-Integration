"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import {
  CandlestickSeries,
  HistogramSeries,
  createChart,
  type IChartApi,
  type ISeriesApi,
  type UTCTimestamp,
} from "lightweight-charts";
import {
  dogrula,
  panelAraligi,
  type ChartSpec,
  type HacimSerisi,
  type MumSerisi,
} from "@/lib/chartspec";
import { ciz, type Cerceve } from "./overlay";
import { pngIndir } from "./png";
import { tokenRengi } from "./roller";

/** Sağ oluk: fibo etiketleri ve son fiyat rozeti burada durur (referans
 *  görselde de fiyat ekseni yerine oran-renkli etiketler var). */
// 186px: en uzun etiket "1.618 (azami risk): 146.00". Dar tutulunca sağdan
// taşıyordu (f4i2 bulgusu). Maketin PAD.r değeriyle de aynı.
const OLUK = 186;
const OLUK_DAR = 104;

/** Görünür aralık seçenekleri. `kurulum` = spec'in tamamını sığdır.
 *
 * **Neden sabit takvim aralığı TEK BAŞINA yetmez:** bir spec yalnız
 * kurulumun etrafındaki barları taşır (Golden Zone'da ~70 bar). "Son 1 yıl"
 * demek o levhada çoğu zaman "hepsi" demektir. Varsayılan bu yüzden
 * `kurulum`: önce kurulum çerçevelenir, kullanıcı isterse geriye açar. */
export const ARALIKLAR = [
  { value: "kurulum", label: "Kurulum", gun: 0 },
  { value: "1a", label: "1A", gun: 30 },
  { value: "3a", label: "3A", gun: 90 },
  { value: "6a", label: "6A", gun: 180 },
  { value: "1y", label: "1Y", gun: 365 },
] as const;

export type Aralik = (typeof ARALIKLAR)[number]["value"];

export type GrafikProps = {
  spec: ChartSpec;
  yukseklik?: number;
  /** Dar levhalarda (çekmece, kart) oluk daralır, etiketler kısalır. */
  dar?: boolean;
  /** Kısa levhalarda merdivenin tamamı yerine yalnız karara değer basamaklar. */
  seviyeler?: "tam" | "vurgulu";
  /** HUD'un ikinci satırı — strateji bağlamı. OHLC satırını sayfa değil
   *  çizici yazar; bağlamı sayfa bilir. */
  hudEk?: React.ReactNode;
};

type Hud = { t: number; acilis: number; yuksek: number; dusuk: number; kapanis: number } | null;

export function Grafik({
  spec: hamSpec,
  yukseklik = 470,
  dar = false,
  seviyeler = "tam",
  hudEk,
}: GrafikProps) {
  const sarmalRef = useRef<HTMLDivElement>(null);
  const tuvalRef = useRef<HTMLDivElement>(null);
  const svgRef = useRef<SVGSVGElement>(null);
  // Grafik nesnesi EFEKTİN DIŞINDAN da lazım: aralık değişince grafiği
  // yeniden kurmak zoom/pan durumunu ve aboneleri çöpe atardı.
  const chartRef = useRef<IChartApi | null>(null);
  const [cizimHatasi, setCizimHatasi] = useState<string | null>(null);
  const [hud, setHud] = useState<Hud>(null);
  const [aralik, setAralik] = useState<Aralik>("kurulum");
  const [indiriliyor, setIndiriliyor] = useState(false);

  // Doğrulama SAF bir iş: render sırasında yapılır, efekt içinde durum
  // kurcalanmaz. Çizici kaynağına güvenerek çizmez — ChartSpec dosya olarak
  // da elden ele geçebilir.
  const { spec, sozlesmeHatasi } = useMemo(() => {
    try {
      return { spec: dogrula(hamSpec), sozlesmeHatasi: null as string | null };
    } catch (e) {
      return { spec: null, sozlesmeHatasi: e instanceof Error ? e.message : String(e) };
    }
  }, [hamSpec]);

  useEffect(() => {
    const tuval = tuvalRef.current;
    const svg = svgRef.current;
    const sarmal = sarmalRef.current;
    if (!tuval || !svg || !sarmal || !spec) return;

    const kok = document.documentElement;
    const oluk = dar ? OLUK_DAR : OLUK;
    const mumSeri = spec.seriler.find((s): s is MumSerisi => s.tur === "mum");
    const hacimSeri = spec.seriler.find((s): s is HacimSerisi => s.tur === "hacim");
    if (!mumSeri) return;
    const fiyatPanel = spec.paneller.find((p) => p.id === mumSeri.panel)!;
    const aralik = panelAraligi(spec, fiyatPanel.id);

    const renk = (t: string) => tokenRengi(kok, t);

    const chart: IChartApi = createChart(tuval, {
      height: yukseklik,
      autoSize: true,
      layout: {
        background: { color: "transparent" },
        textColor: renk("--text-3"),
        fontFamily: renk("--f-mono") || "monospace",
        fontSize: 10,
        attributionLogo: false,
      },
      grid: {
        vertLines: { color: renk("--grid") },
        horzLines: { color: renk("--grid") },
      },
      crosshair: {
        mode: 0,
        vertLine: { color: renk("--text-3"), width: 1, style: 2, labelVisible: false },
        horzLine: { color: renk("--text-3"), width: 1, style: 2, labelVisible: false },
      },
      // Fiyat ekseni GİZLİ: sağ olukta oran-renkli fibo etiketleri var, ayrıca
      // bir sayı sütunu levhayı kalabalıklaştırırdı (referans görsel de öyle).
      rightPriceScale: { visible: false },
      leftPriceScale: { visible: false },
      timeScale: {
        borderColor: renk("--line"),
        rightOffset: 2,
        barSpacing: 6,
        minBarSpacing: 0.5,
      },
      handleScale: { axisPressedMouseMove: { price: false } },
      localization: { locale: "tr-TR" },
    });

    const mum: ISeriesApi<"Candlestick"> = chart.addSeries(CandlestickSeries, {
      upColor: renk("--up"),
      downColor: renk("--down"),
      wickUpColor: renk("--up"),
      wickDownColor: renk("--down"),
      borderVisible: false,
      priceLineVisible: false,
      lastValueVisible: false,
      // Panel oranı ChartSpec'ten gelir; hacim alttaki payı kaplar.
      autoscaleInfoProvider: () => ({ priceRange: { minValue: aralik.alt, maxValue: aralik.ust } }),
    });
    mum.priceScale().applyOptions({ scaleMargins: { top: 0.04, bottom: 1 - fiyatPanel.oran + 0.02 } });
    mum.setData(
      mumSeri.veri.map((m) => ({
        time: m.t as UTCTimestamp,
        open: m.acilis,
        high: m.yuksek,
        low: m.dusuk,
        close: m.kapanis,
      })),
    );

    let hacim: ISeriesApi<"Histogram"> | null = null;
    if (hacimSeri) {
      const hacimPanel = spec.paneller.find((p) => p.id === hacimSeri.panel);
      hacim = chart.addSeries(HistogramSeries, {
        priceScaleId: "hacim",
        priceLineVisible: false,
        lastValueVisible: false,
      });
      hacim.priceScale().applyOptions({
        scaleMargins: { top: 1 - (hacimPanel?.oran ?? 0.24) + 0.02, bottom: 0 },
      });
      const ust = renk("--up");
      const alt = renk("--down");
      hacim.setData(
        hacimSeri.veri.map((h) => ({
          time: h.t as UTCTimestamp,
          value: h.hacim,
          color: h.yon === "al" ? ust : alt,
        })),
      );
    }

    chartRef.current = chart;
    chart.timeScale().fitContent();

    // ---------------------------------------------------------- overlay çizimi
    const cerceve = (): Cerceve => ({
      genislik: sarmal.clientWidth,
      yukseklik: sarmal.clientHeight,
      oluk,
      dar,
      seviyeler,
      x: (t) => chart.timeScale().timeToCoordinate(t as UTCTimestamp),
      y: (f) => mum.priceToCoordinate(f),
      renk,
    });

    const cizdir = () => {
      try {
        ciz(svg, spec, cerceve());
      } catch (e) {
        setCizimHatasi(e instanceof Error ? e.message : String(e));
      }
    };

    cizdir();
    const zamanAbone = chart.timeScale().subscribeVisibleLogicalRangeChange(cizdir);

    chart.subscribeCrosshairMove((p) => {
      const d = p.seriesData.get(mum) as
        | { open: number; high: number; low: number; close: number }
        | undefined;
      if (!d || p.time === undefined) setHud(null);
      else
        setHud({
          t: p.time as number,
          acilis: d.open,
          yuksek: d.high,
          dusuk: d.low,
          kapanis: d.close,
        });
    });

    const gozlemci = new ResizeObserver(() => cizdir());
    gozlemci.observe(sarmal);

    // Tema ya da aksan değişince token'lar yeniden okunur.
    const temaGozlemci = new MutationObserver(() => {
      chart.applyOptions({
        layout: { textColor: renk("--text-3") },
        grid: { vertLines: { color: renk("--grid") }, horzLines: { color: renk("--grid") } },
        crosshair: { vertLine: { color: renk("--text-3") }, horzLine: { color: renk("--text-3") } },
        timeScale: { borderColor: renk("--line") },
      });
      mum.applyOptions({
        upColor: renk("--up"),
        downColor: renk("--down"),
        wickUpColor: renk("--up"),
        wickDownColor: renk("--down"),
      });
      if (hacim && hacimSeri) {
        const u = renk("--up");
        const a = renk("--down");
        hacim.setData(
          hacimSeri.veri.map((h) => ({
            time: h.t as UTCTimestamp,
            value: h.hacim,
            color: h.yon === "al" ? u : a,
          })),
        );
      }
      cizdir();
    });
    temaGozlemci.observe(kok, { attributes: true, attributeFilter: ["data-theme", "data-accent"] });
    // Tema "sistem" ise nitelik değişmez; işletim sistemi değişimini ayrıca dinle.
    const sistemTema = window.matchMedia("(prefers-color-scheme: dark)");
    sistemTema.addEventListener("change", cizdir);

    return () => {
      chart.timeScale().unsubscribeVisibleLogicalRangeChange(zamanAbone as never);
      sistemTema.removeEventListener("change", cizdir);
      gozlemci.disconnect();
      temaGozlemci.disconnect();
      chartRef.current = null;
      chart.remove();
      svg.replaceChildren();
    };
  }, [spec, yukseklik, dar, seviyeler]);

  // Aralık değişince yalnız görünür pencere güncellenir. Grafiği yeniden
  // kurmak zoom/pan durumunu ve tüm aboneleri çöpe atardı.
  useEffect(() => {
    const chart = chartRef.current;
    const mumSeri = spec?.seriler.find((x): x is MumSerisi => x.tur === "mum");
    if (!chart || !mumSeri || mumSeri.veri.length === 0) return;

    const secim = ARALIKLAR.find((x) => x.value === aralik);
    if (!secim || secim.gun === 0) {
      chart.timeScale().fitContent();
      return;
    }
    const son = mumSeri.veri[mumSeri.veri.length - 1].t;
    const ilk = mumSeri.veri[0].t;
    // İstenen pencere serinin başından geriye taşıyorsa tamamı gösterilir:
    // olmayan barlara doğru boş alan açmak levhayı yalancı yapar.
    const bas = Math.max(ilk, son - secim.gun * 86400);
    if (bas <= ilk) {
      chart.timeScale().fitContent();
      return;
    }
    chart.timeScale().setVisibleRange({
      from: bas as UTCTimestamp,
      to: son as UTCTimestamp,
    });
  }, [aralik, spec]);

  const indir = async () => {
    const chart = chartRef.current;
    const svg = svgRef.current;
    const sarmal = sarmalRef.current;
    if (!chart || !svg || !sarmal || !spec) return;
    setIndiriliyor(true);
    try {
      await pngIndir(chart, svg, sarmal, spec, dar ? OLUK_DAR : OLUK);
    } catch (e) {
      setCizimHatasi(e instanceof Error ? e.message : String(e));
    } finally {
      setIndiriliyor(false);
    }
  };

  const hata = sozlesmeHatasi ?? cizimHatasi ?? (spec ? null : "ChartSpec okunamadı.");
  if (hata) {
    return (
      <div className="qgrafik-hata" role="alert">
        <b>Grafik çizilemedi.</b>
        <p>{hata}</p>
        <p className="dim">
          Sessizce boş bir levha göstermiyoruz: sözleşme ihlali görünür olmalı.
        </p>
      </div>
    );
  }

  const son = hud;
  const yukari = son ? son.kapanis >= son.acilis : true;

  return (
    <>
      {/* Araç şeridi levhanın İÇİNDE değil ÜSTÜNDE. İçindeyken sağ oluktaki
          fibo etiketlerinin üstüne biniyor ve "0.0 (hedef): 335.00" gibi
          sayıları kapatıyordu (i1 bulgusu). PNG'ye de girmiyor — indirilen
          görüntüde arayüz düğmesi işi yok. */}
      <div className="qgrafik-araclar">
        <div className="qgrafik-aralik" role="group" aria-label="Görünür aralık">
          {ARALIKLAR.map((x) => (
            <button
              key={x.value}
              type="button"
              className={x.value === aralik ? "etkin" : undefined}
              aria-pressed={x.value === aralik}
              onClick={() => setAralik(x.value)}
            >
              {x.label}
            </button>
          ))}
        </div>
        <button
          type="button"
          className="qgrafik-indir"
          onClick={indir}
          disabled={indiriliyor}
          title="Levhayı PNG olarak indir"
        >
          {indiriliyor ? "…" : "PNG"}
        </button>
      </div>
    <div
      className="qgrafik"
      ref={sarmalRef}
      style={{ height: yukseklik, ["--oluk" as string]: `${dar ? OLUK_DAR : OLUK}px` }}
    >
      <div className="qgrafik-tuval" ref={tuvalRef} />
      <svg className="qgrafik-overlay" ref={svgRef} aria-hidden="true" />
      <div className="qgrafik-hud">
        <div className="num l1">
          {/* Dar levhada sembol zaten çubukta yazılı; tekrar etmez. */}
          {dar ? null : (
            <>
              {spec?.kunye.sembol} <span className="dim">·</span> {spec?.kunye.zaman_dilimi}
            </>
          )}
          {son ? (
            <>
              {"  "}
              <span className="dim">A</span> {son.acilis.toFixed(2)} <span className="dim">Y</span>{" "}
              {son.yuksek.toFixed(2)} <span className="dim">D</span> {son.dusuk.toFixed(2)}{" "}
              <span className="dim">K</span>{" "}
              <b style={{ color: yukari ? "var(--up)" : "var(--down)" }}>
                {son.kapanis.toFixed(2)} {yukari ? "▲" : "▼"}
              </b>
            </>
          ) : null}
        </div>
        {hudEk ? <div className="l2">{hudEk}</div> : null}
      </div>
    </div>
    </>
  );
}
