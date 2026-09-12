type Props = {
  /** CSS genişliği — "58%", "120px". */
  width?: string;
  height?: number;
};

/** Skeleton — tek satırlık yükleme şeridi. `prefers-reduced-motion` altında
 *  parıltı durur (bilesenler.css'teki genel kural). */
export function Skeleton({ width = "100%", height = 11 }: Props) {
  return <div className="skel" style={{ width, height }} aria-hidden="true" />;
}

/** Birkaç satırlık, farklı genişliklerde yükleme bloğu. */
export function SkeletonBlock({ lines = 3, label = "Yükleniyor" }: { lines?: number; label?: string }) {
  const genislik = ["58%", "86%", "72%", "64%", "91%"];
  return (
    <div className="stack" role="status" aria-live="polite" aria-label={label}>
      {Array.from({ length: lines }, (_, i) => (
        <Skeleton key={i} width={genislik[i % genislik.length]} />
      ))}
    </div>
  );
}
