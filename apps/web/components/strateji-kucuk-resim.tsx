/**
 * Kart yüzü — ÖRNEK. Gerçek grafik motoru Faz 4'ün işi (Lightweight Charts +
 * SVG overlay). Buradaki mumlar deterministik bir üreteçten gelir ve yalnızca
 * kartın görsel ağırlığını doğru ölçmek için var.
 *
 * Kural: aksan ASLA mum ölçeğinde dolu bir leke değildir — bölge %10-22
 * opaklıkta geniş dolgu, seviyeler 1px çizgi. Yön renkleri her zaman dolu.
 */
type Tip = "fib" | "ms" | "zone" | "fvg";

function rng(seed: number) {
  let s = seed;
  return () => {
    s = (s * 1664525 + 1013904223) & 0x7fffffff;
    return s / 0x7fffffff;
  };
}

const FIB_TOKEN = ["--fib-236", "--fib-382", "--fib-500", "--accent"];

export function StratejiKucukResim({ tip, w = 300, h = 118 }: { tip: Tip; w?: number; h?: number }) {
  const r = rng(tip.length * 977 + 31);
  const n = 34;
  const bw = w / n;
  const noktalar: number[] = [];
  let v = h * 0.55;
  for (let i = 0; i < n; i++) {
    v += (r() - 0.5) * h * 0.12 + (tip === "fib" ? h * 0.006 : -h * 0.004);
    v = Math.max(h * 0.2, Math.min(h * 0.82, v));
    noktalar.push(v);
  }

  return (
    <svg viewBox={`0 0 ${w} ${h}`} aria-hidden="true">
      {tip === "fib" &&
        [0.28, 0.38, 0.48, 0.58].map((f, k) => (
          <line
            key={k}
            x1={w * 0.35}
            x2={w}
            y1={h * f}
            y2={h * f}
            stroke={`var(${FIB_TOKEN[k]})`}
            strokeWidth={1}
            strokeDasharray="4 3"
            opacity={0.75}
          />
        ))}
      {tip === "fib" && (
        <rect x={w * 0.35} y={h * 0.48} width={w * 0.65} height={h * 0.1} fill="var(--accent)" opacity={0.12} />
      )}

      {tip === "ms" && (
        <polyline
          fill="none"
          stroke="var(--accent)"
          strokeWidth={1.4}
          opacity={0.8}
          points={`${w * 0.08},${h * 0.72} ${w * 0.28},${h * 0.34} ${w * 0.46},${h * 0.54} ${w * 0.66},${h * 0.24} ${w * 0.86},${h * 0.46}`}
        />
      )}

      {tip === "zone" && (
        <>
          <rect x={0} y={h * 0.3} width={w} height={h * 0.11} fill="var(--down)" opacity={0.16} />
          <rect x={0} y={h * 0.62} width={w} height={h * 0.11} fill="var(--up)" opacity={0.16} />
        </>
      )}

      {tip === "fvg" && (
        <>
          <rect x={w * 0.42} y={h * 0.4} width={w * 0.52} height={h * 0.09} fill="var(--accent)" opacity={0.22} />
          <rect x={w * 0.2} y={h * 0.58} width={w * 0.3} height={h * 0.07} fill="var(--accent)" opacity={0.12} />
        </>
      )}

      {noktalar.map((c, i) => {
        const x = i * bw + bw / 2;
        const o = i ? noktalar[i - 1] : c;
        const yukari = c <= o;
        const ust = Math.min(c, o);
        const alt = Math.max(c, o);
        const col = yukari ? "var(--up)" : "var(--down)";
        return (
          <g key={i}>
            <line x1={x} x2={x} y1={ust - h * 0.05} y2={alt + h * 0.05} stroke={col} strokeWidth={0.8} opacity={0.9} />
            <rect
              x={x - bw * 0.27}
              y={ust}
              width={bw * 0.54}
              height={Math.max(1, alt - ust)}
              fill={col}
              opacity={0.9}
            />
          </g>
        );
      })}
    </svg>
  );
}
