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
import { tokenRengi } from "./roller";

/** Sağ oluk: fibo etiketleri ve son fiyat rozeti burada durur (referans
 *  görselde de fiyat ekseni yerine oran-renkli etiketler var). */
// 186px: en uzun etiket "1.618 (azami risk): 146.00". Dar tutulunca sağdan
// taşıyordu (f4i2 bulgusu). Maketin PAD.r değeriyle de aynı.
const OLUK = 186;
const OLUK_DAR = 104;

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
  const [cizimHatasi, setCizimHatasi] = useState<string | null>(null);
  const [hud, setHud] = useState<Hud>(null);

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
      chart.remove();
      svg.replaceChildren();
    };
  }, [spec, yukseklik, dar, seviyeler]);

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
  );
}
