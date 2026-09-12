import type { HTMLAttributes, ReactNode } from "react";

type CardProps = HTMLAttributes<HTMLElement> & {
  /** Kartın yüzü — gerçek bir grafik olması beklenir, dekoratif görsel değil. */
  thumb?: ReactNode;
  /** Mono, büyük harf üst satır: kaynak · pasaport kapısı. */
  meta?: ReactNode;
  title: ReactNode;
  children?: ReactNode;
  /** Rozetler ve "Stratejiyi aç →" bağlantısı. */
  foot?: ReactNode;
};

export function Card({ thumb, meta, title, children, foot, className, ...rest }: CardProps) {
  return (
    <article className={className ? `card ${className}` : "card"} {...rest}>
      {thumb ? <div className="thumb">{thumb}</div> : null}
      {meta ? <div className="meta">{meta}</div> : null}
      <h3>{title}</h3>
      {children ? <p>{children}</p> : null}
      {foot ? <div className="foot">{foot}</div> : null}
    </article>
  );
}

/** Kart ızgarası — 1px boşluk, zemin çizgi rengi: ayrım gölgeyle değil alfa ile. */
export function CardGrid({ className, ...rest }: HTMLAttributes<HTMLDivElement>) {
  return <div className={className ? `cards ${className}` : "cards"} {...rest} />;
}
