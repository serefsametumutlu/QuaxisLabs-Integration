"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Eyebrow } from "@/components/ui";
import { EVREN, PAKETLER, YUZEYLER } from "@/lib/yollar";

/** Sol ray — yüzeyler, paketler, evren. 900px altında gizlenir. */
export function Ray() {
  const yol = usePathname();

  return (
    <aside className="rail">
      <Eyebrow as="h4">Yüzeyler</Eyebrow>
      <nav>
        {YUZEYLER.map((y) => (
          <Link
            key={y.yol}
            href={y.yol}
            aria-current={yol === y.yol || yol.startsWith(`${y.yol}/`) ? "page" : undefined}
          >
            <span className="dot" />
            {y.ad}
            {y.sayac ? <span className="cnt">{y.sayac}</span> : null}
          </Link>
        ))}
      </nav>

      <Eyebrow as="h4">Paketler</Eyebrow>
      <nav>
        {PAKETLER.map((p) => (
          <Link key={p.ad} href={p.yol} className={p.pasif ? "pasif" : undefined}>
            {p.ad}
            <span className="cnt">{p.sayac}</span>
          </Link>
        ))}
      </nav>

      <Eyebrow as="h4">Evren</Eyebrow>
      <nav>
        {EVREN.map((e) => (
          <Link key={e.ad} href={e.yol}>
            {e.ad}
            <span className="cnt">{e.sayac}</span>
          </Link>
        ))}
      </nav>
    </aside>
  );
}
