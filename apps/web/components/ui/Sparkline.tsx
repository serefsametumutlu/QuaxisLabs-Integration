type Props = {
  /** Ham seri; en az iki nokta. Ölçekleme bileşen içinde yapılır. */
  points: readonly number[];
  /** Yön rengi: yükseliş/düşüş. Aksan ASLA yön anlamı taşımaz. */
  dir?: "up" | "down";
  width?: number;
  height?: number;
  /** Ekran okuyucu için; verilmezse süs sayılır. */
  label?: string;
};

/**
 * Sparkline — tablo satırında 20 barlık seyir. Dolgu yok, 1.2px çizgi:
 * satır yüksekliğinde leke oluşturmaz.
 */
export function Sparkline({ points, dir = "up", width = 62, height = 18, label }: Props) {
  const n = points.length;
  if (n < 2) return null;

  const min = Math.min(...points);
  const max = Math.max(...points);
  const span = max - min || 1;
  const pad = 1.6;
  const d = points
    .map((v, i) => {
      const x = pad + (i / (n - 1)) * (width - pad * 2);
      const y = height - pad - ((v - min) / span) * (height - pad * 2);
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");

  return (
    <svg
      className="spark"
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      role={label ? "img" : "presentation"}
      aria-label={label}
      aria-hidden={label ? undefined : true}
    >
      <polyline
        fill="none"
        stroke={dir === "up" ? "var(--up)" : "var(--down)"}
        strokeWidth={1.2}
        strokeLinejoin="round"
        strokeLinecap="round"
        points={d}
      />
    </svg>
  );
}
