/**
 * GrafikYeri — grafik motorunun YERİ, motorun kendisi değil.
 *
 * Faz 4'te buraya `ChartSpec` + Lightweight Charts v5 + SVG overlay gelecek:
 * fibo merdiveni, dolgulu X-A-B-C-D gövdesi, rozetler, crosshair, HUD.
 * Şimdilik yalnız deterministik örnek mumlar ve hacim şeridi çizilir — sayfa
 * kompozisyonu (levha yüksekliği, HUD ve durum kutusunun yerleşimi, notların
 * altına oturması) ancak dolu bir levhayla değerlendirilebilir.
 *
 * Bilinçli olarak YOK: gösterge çizimi, seviye hesabı, etkileşim. Hiçbiri bu
 * bileşende hesaplanmaz — katman ayrımı kuralı: görselleştirme hesap yapmaz.
 */

function rng(seed: number) {
  let s = seed;
  return () => {
    s = (s * 1664525 + 1013904223) & 0x7fffffff;
    return s / 0x7fffffff;
  };
}

type Bar = { o: number; h: number; l: number; c: number; v: number };

function barlar(seed: number, n: number): Bar[] {
  const r = rng(seed);
  const out: Bar[] = [];
  let mid = 0.5;
  for (let i = 0; i < n; i++) {
    mid += (r() - 0.5) * 0.05 + Math.sin(i * 0.07) * 0.012;
    const o = mid + (r() - 0.5) * 0.022;
    const c = mid + (r() - 0.5) * 0.022;
    out.push({ o, c, h: Math.max(o, c) + r() * 0.02, l: Math.min(o, c) - r() * 0.02, v: 0.3 + r() * 0.7 });
  }
  return out;
}

type Props = {
  /** Farklı sembol/levha = farklı ama TEKRARLANABİLİR seri. */
  seed?: number;
  w?: number;
  h?: number;
  bar?: number;
  /**
   * Son fiyat rozeti. Yön ÇAĞIRANDAN gelir: bir tarama aracında rozetin rengi
   * "yön" demektir, rastgele bir serinin son barına bırakılamaz — sayfadaki
   * AL/SAT rozetiyle çelişirse okuyucuyu yanıltır.
   */
  son?: { fiyat: number; yon: "up" | "down" };
  /**
   * HUD ve durum kutusu levhanın ÜSTÜNE binen katmanlardır; seri onların
   * altında kalmasın diye üstte ve sağda pay bırakılır. Pay bırakılmadığında
   * son barlar durum kutusunun arkasında kalıyordu (f3i2 bulgusu) — bir
   * tarama aracında en önemli barlar tam da onlar.
   */
  padUst?: number;
  padSag?: number;
  label: string;
};

export function GrafikYeri({
  seed = 20260912,
  w = 1180,
  h = 420,
  bar = 130,
  son,
  padUst = 14,
  padSag = 92,
  label,
}: Props) {
  const veri = barlar(seed, bar);

  const ustPay = padUst;
  const altPay = 26;
  const sagPay = padSag;
  const hacimOran = 0.24;

  const govde = h - ustPay - altPay;
  const fiyatH = govde * (1 - hacimOran) - 10;
  const hacimUst = ustPay + govde * (1 - hacimOran) + 8;
  const hacimH = govde * hacimOran - 8;

  // Fiyat ekseni seriye OTURUR. Sabit aralık verilirse rastgele yürüyüş
  // panelin ortasında ince bir şerit olarak kalıyordu (f3i1 bulgusu).
  const lo = Math.min(...veri.map((b) => b.l));
  const hi = Math.max(...veri.map((b) => b.h));
  const pay = (hi - lo) * 0.06 || 0.01;
  const y = (p: number) => ustPay + ((hi + pay - p) / (hi - lo + pay * 2)) * fiyatH;

  const bw = (w - 14 - sagPay) / bar;
  const x = (i: number) => 14 + (i + 0.5) * bw;
  const vMax = Math.max(...veri.map((b) => b.v));

  const sonBar = veri[bar - 1];
  const sonYon = son?.yon ?? (sonBar.c >= sonBar.o ? "up" : "down");
  const sonRenk = sonYon === "up" ? "var(--up)" : "var(--down)";
  const sonMetin = (son?.fiyat ?? 100 + sonBar.c * 100).toFixed(2);

  return (
    <svg viewBox={`0 0 ${w} ${h}`} role="img" aria-label={label}>
      {[0.2, 0.4, 0.6, 0.8].map((g) => (
        <line
          key={g}
          x1={14}
          x2={w - sagPay}
          y1={ustPay + g * fiyatH}
          y2={ustPay + g * fiyatH}
          stroke="var(--grid)"
          strokeWidth={1}
        />
      ))}

      {veri.map((b, i) => {
        const yukari = b.c >= b.o;
        const renk = yukari ? "var(--up)" : "var(--down)";
        const ust = y(Math.max(b.o, b.c));
        const alt = y(Math.min(b.o, b.c));
        return (
          <g key={i}>
            <line x1={x(i)} x2={x(i)} y1={y(b.h)} y2={y(b.l)} stroke={renk} strokeWidth={1} />
            <rect
              x={x(i) - bw * 0.32}
              y={ust}
              width={bw * 0.64}
              height={Math.max(1, alt - ust)}
              fill={renk}
              opacity={yukari ? 0.9 : 1}
            />
            <rect
              x={x(i) - bw * 0.32}
              y={hacimUst + hacimH - (b.v / vMax) * hacimH}
              width={bw * 0.64}
              height={(b.v / vMax) * hacimH}
              fill={renk}
              opacity={0.34}
            />
          </g>
        );
      })}

      <text
        x={16}
        y={hacimUst - 5}
        fill="var(--text-3)"
        fontFamily="var(--f-mono)"
        fontSize={10}
        letterSpacing="1.4"
      >
        HACİM
      </text>

      {/* son fiyat: yön rengi, dolu — yön renkleri her zaman dolu ve net */}
      <line
        x1={14}
        x2={w - sagPay}
        y1={y(sonBar.c)}
        y2={y(sonBar.c)}
        stroke={sonRenk}
        strokeWidth={1}
        strokeDasharray="1 3"
        opacity={0.8}
      />
      <rect x={w - sagPay + 2} y={y(sonBar.c) - 8.5} width={78} height={17} rx={2} fill={sonRenk} />
      <text
        x={w - sagPay + 10}
        y={y(sonBar.c) + 3.6}
        fill="var(--surface)"
        fontFamily="var(--f-mono)"
        fontSize={10.5}
      >
        {sonMetin}
      </text>

      <text x={16} y={h - 8} fill="var(--text-3)" fontFamily="var(--f-mono)" fontSize={10}>
        Mar 2026 — Eyl 2026
      </text>
    </svg>
  );
}

/**
 * Levha çubuğuna konan kesikli hap: bu levhanın içi henüz motor değil.
 * Grafiğin üstüne bindirmek yerine çubuğa konur — bindirme mumları ve hacmi
 * kapatıyordu (f3i1 bulgusu).
 */
export function Faz4Isareti() {
  return <span className="faz4">ChartSpec katmanı · Faz 4</span>;
}
