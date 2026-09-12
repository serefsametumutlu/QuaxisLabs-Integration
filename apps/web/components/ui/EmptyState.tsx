import type { ReactNode } from "react";

type Props = {
  title: ReactNode;
  children?: ReactNode;
  /** Kullanıcıyı çıkışa götüren eylem — "yakında" yazısı değil. */
  action?: ReactNode;
};

/**
 * EmptyState — sahte veri yok, "yakında" yok. Boşluk neden boş, onu söyler
 * ve bir sonraki hamleyi önerir.
 */
export function EmptyState({ title, children, action }: Props) {
  return (
    <div className="empty">
      <b>{title}</b>
      {children}
      {action ? <div className="act">{action}</div> : null}
    </div>
  );
}
