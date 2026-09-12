import Link from "next/link";

/** Marka işareti — iki halka, yükselen çizgi ve ok. Tek renk: aksan. */
export function MarkaIsareti({ className = "mark" }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" aria-hidden="true">
      <circle cx="12" cy="12" r="10.2" fill="none" stroke="var(--accent)" strokeWidth="1.5" opacity=".45" />
      <circle cx="12" cy="12" r="6.4" fill="none" stroke="var(--accent)" strokeWidth="1.5" opacity=".8" />
      <path
        d="M7 16.4 L10.4 11.6 L13.1 14 L18 6.6"
        fill="none"
        stroke="var(--accent)"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M14.4 6.2 L18.6 6 L18.4 10.2"
        fill="none"
        stroke="var(--accent)"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path d="M13.6 13.4 L18.4 18.6" stroke="var(--accent)" strokeWidth="1.8" strokeLinecap="round" />
    </svg>
  );
}

export function Marka({ href = "/" }: { href?: string }) {
  return (
    <Link className="brand" href={href} aria-label="QuaxisLabs ana sayfa">
      <MarkaIsareti />
      <span className="word">
        QUAXIS<em>LABS</em>
      </span>
    </Link>
  );
}
