import type { ReactNode } from "react";

type Props = {
  question: ReactNode;
  children: ReactNode;
  /** İlk boyamada açık gelsin mi. Kaydırma tetikli açılma YASAK olduğu için
   *  içerik zaten DOM'da; bu yalnız görünürlük tercihidir. */
  open?: boolean;
};

/**
 * Faq — yerel `<details>`. Kendi işaretçisi gizlenip yerine aksan renkli
 * `+` / `—` konur; aksanın tek çizgi kalınlığındaki kullanımlarından biri.
 */
export function Faq({ question, children, open }: Props) {
  return (
    <details className="faq" open={open}>
      <summary>{question}</summary>
      <p>{children}</p>
    </details>
  );
}

export function FaqList({ children }: { children: ReactNode }) {
  return <div>{children}</div>;
}
