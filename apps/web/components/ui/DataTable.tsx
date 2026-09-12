"use client";

import {
  useCallback,
  useId,
  useLayoutEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react";

export type SiralamaYonu = "asc" | "desc";

export type Kolon<T> = {
  id: string;
  header: ReactNode;
  /** Sayısal kolonlar sağa yaslanır. */
  align?: "left" | "right";
  /** Sabit kolon genişliği ("104px", "18%"). Sanallaştırmada kaymayı önler. */
  width?: string;
  /** Sıralanabilirlik için karşılaştırma değeri. Verilmezse kolon sıralanmaz. */
  sortValue?: (row: T) => string | number;
  cell: (row: T) => ReactNode;
  className?: string;
  /** Ekran okuyucuya kolon başlığını farklı okutmak gerekirse. */
  headerLabel?: string;
};

export type DataTableProps<T> = {
  columns: readonly Kolon<T>[];
  rows: readonly T[];
  rowKey: (row: T) => string;
  /** Tablo başlığı — görsel olarak gizli, ekran okuyucuya okunur. */
  caption: string;
  /** Kaydırma penceresinin yüksekliği (px). Sanallaştırma buna göre çalışır. */
  height?: number;
  rowHeight?: number;
  /** Pencerenin üstünde/altında fazladan çizilecek satır sayısı. */
  overscan?: number;
  /** Satır-üzeri kancası — grafik çekmecesi/önizleme bağlamak için. */
  onRowHover?: (row: T | null) => void;
  /** Enter/Space ya da tıklama. */
  onRowActivate?: (row: T) => void;
  initialSort?: { columnId: string; dir: SiralamaYonu };
  emptyState?: ReactNode;
  /** Alt şerit — satır sayısı, örnek veri uyarısı vb. */
  footNote?: ReactNode;
  /** min-width: dar ekranda yatay kaydırma eşiği. */
  minWidth?: number;
};

const TR = new Intl.Collator("tr", { numeric: true, sensitivity: "base" });

/**
 * DataTable — sıralanabilir kolonlar, sanallaştırma, tabular-nums,
 * satır-üzeri kancası, klavye gezinmesi.
 *
 * Sanallaştırma: satır yüksekliği SABİT; görünen pencere `scrollTop`'tan
 * hesaplanır, üstte ve altta birer dolgu satırı (`tr.pad`) yüksekliği taşır.
 * Gerçek `<table>` korunur — semantik ve kolon hizası bozulmaz.
 *
 * Klavye: gezinen odak (roving tabindex). ↑ ↓ Home End PageUp PageDown ile
 * satır değişir, Enter/Space satırı açar. Odaklı satır pencerenin dışına
 * çıkarsa kaydırılır — odak hiçbir zaman çizilmemiş bir satıra gitmez.
 */
export function DataTable<T>({
  columns,
  rows,
  rowKey,
  caption,
  height = 420,
  rowHeight = 33,
  overscan = 6,
  onRowHover,
  onRowActivate,
  initialSort,
  emptyState,
  footNote,
  minWidth = 980,
}: DataTableProps<T>) {
  const id = useId();
  const scrollRef = useRef<HTMLDivElement>(null);
  const bodyRef = useRef<HTMLTableSectionElement>(null);

  const [sort, setSort] = useState<{ columnId: string; dir: SiralamaYonu } | null>(initialSort ?? null);
  const [scrollTop, setScrollTop] = useState(0);
  const [aktif, setAktif] = useState<number>(-1);
  const [odakIstendi, setOdakIstendi] = useState(false);

  const sirali = useMemo(() => {
    if (!sort) return rows as T[];
    const kolon = columns.find((c) => c.id === sort.columnId);
    if (!kolon?.sortValue) return rows as T[];
    const al = kolon.sortValue;
    const yon = sort.dir === "asc" ? 1 : -1;
    return [...rows].sort((a, b) => {
      const x = al(a);
      const y = al(b);
      if (typeof x === "number" && typeof y === "number") return (x - y) * yon;
      return TR.compare(String(x), String(y)) * yon;
    });
  }, [rows, columns, sort]);

  /**
   * Hücre önbelleği — kaydırmanın asıl maliyeti burada.
   * Pencere her karede kaydığı için `cell(row)` saniyede onlarca kez yeniden
   * koşuyordu (sparkline SVG'leri dahil). `<td>` ELEMANLARI satır nesnesine
   * göre bir kez üretilir; aynı referans geri verilince React o alt ağacı hiç
   * diff'lemez. Sıralama satır nesnelerini değil sırayı değiştirdiği için
   * önbellek sıralamada da geçerli kalır — yalnız satır kümesi ya da kolonlar
   * değişince yeniden kurulur.
   */
  const hucreler = useMemo(() => {
    const harita = new Map<T, ReactNode[]>();
    for (const row of rows) {
      harita.set(
        row,
        columns.map((c) => (
          <td
            key={c.id}
            className={[c.align === "right" ? "r" : null, c.className].filter(Boolean).join(" ") || undefined}
          >
            {c.cell(row)}
          </td>
        )),
      );
    }
    return harita;
  }, [rows, columns]);

  const toplam = sirali.length;
  const ilk = Math.max(0, Math.floor(scrollTop / rowHeight) - overscan);
  const gorunen = Math.ceil(height / rowHeight) + overscan * 2;
  const son = Math.min(toplam, ilk + gorunen);
  const ustDolgu = ilk * rowHeight;
  const altDolgu = Math.max(0, (toplam - son) * rowHeight);

  // Kaydırma olayı bir karede defalarca gelebilir; pencereyi kare başına bir
  // kez güncelleriz. Aksi hâlde tek karede birden fazla React turu doğuyor.
  const kaydirmaBekleyen = useRef(false);
  const kaydir = useCallback(() => {
    if (kaydirmaBekleyen.current) return;
    kaydirmaBekleyen.current = true;
    requestAnimationFrame(() => {
      kaydirmaBekleyen.current = false;
      const el = scrollRef.current;
      if (el) setScrollTop(el.scrollTop);
    });
  }, []);

  /** Sticky <thead> pencerenin üst şeridini kapatır; hesaplara dahil edilir. */
  const baslikYuksekligi = () =>
    (bodyRef.current?.parentElement as HTMLTableElement | null)?.tHead?.offsetHeight ?? 0;

  const siralamayiDegistir = useCallback((kolonId: string) => {
    setSort((s) =>
      s?.columnId === kolonId
        ? s.dir === "asc"
          ? { columnId: kolonId, dir: "desc" }
          : null
        : { columnId: kolonId, dir: "asc" },
    );
    scrollRef.current?.scrollTo({ top: 0 });
    setScrollTop(0);
  }, []);

  /** Odaklı satırı pencereye sokar; çizilmemişse önce oraya kaydırır. */
  const satiraGit = useCallback(
    (hedef: number) => {
      const i = Math.max(0, Math.min(toplam - 1, hedef));
      setAktif(i);
      setOdakIstendi(true);
      const el = scrollRef.current;
      if (!el) return;
      // Satırın içerik koordinatı başlık yüksekliği kadar aşağıdadır; görünür
      // bölge de yapışkan başlığın ALTINDA başlar. İkisi hesaba katılmazsa
      // "End" sonrası odaklı satır pencerenin dışında kalıyordu.
      const bas = baslikYuksekligi();
      const ust = bas + i * rowHeight;
      const alt = ust + rowHeight;
      if (ust < el.scrollTop + bas) el.scrollTop = ust - bas;
      else if (alt > el.scrollTop + el.clientHeight) el.scrollTop = alt - el.clientHeight;
    },
    [toplam, rowHeight],
  );

  // Kaydırma sonrası satır DOM'a girdiğinde odağı ona taşı.
  useLayoutEffect(() => {
    if (!odakIstendi || aktif < 0) return;
    const tr = bodyRef.current?.querySelector<HTMLTableRowElement>(`tr[data-index="${aktif}"]`);
    if (tr) {
      tr.focus({ preventScroll: true });
      setOdakIstendi(false);
    }
  }, [odakIstendi, aktif, scrollTop]);

  // Satır kümesi değişirse gezinen odak sıfırlanır. Efekt değil, RENDER
  // sırasında düzeltme: React'in "prop değişince durumu ayarla" kalıbı —
  // efektle yapılsa fazladan bir boyama turu doğardı.
  const [oncekiToplam, setOncekiToplam] = useState(toplam);
  if (oncekiToplam !== toplam) {
    setOncekiToplam(toplam);
    setAktif(-1);
  }

  /** Olay hedefinden satır sırasını okur. Dinleyiciler satırlarda değil
   *  `<tbody>`'de duruyor: her karede 25 satıra dört kapanış bağlamak
   *  kaydırmayı yavaşlatıyordu. */
  const sira = (e: { target: EventTarget | null }): number => {
    const tr = (e.target as HTMLElement | null)?.closest?.("tr[data-index]");
    const v = tr?.getAttribute("data-index");
    return v == null ? -1 : Number(v);
  };

  const tus = (e: React.KeyboardEvent<HTMLTableSectionElement>) => {
    const index = sira(e);
    if (index < 0) return;
    const row = sirali[index];
    const sayfa = Math.max(1, Math.floor(height / rowHeight) - 1);
    switch (e.key) {
      case "ArrowDown":
        e.preventDefault();
        satiraGit(index + 1);
        break;
      case "ArrowUp":
        e.preventDefault();
        satiraGit(index - 1);
        break;
      case "PageDown":
        e.preventDefault();
        satiraGit(index + sayfa);
        break;
      case "PageUp":
        e.preventDefault();
        satiraGit(index - sayfa);
        break;
      case "Home":
        e.preventDefault();
        satiraGit(0);
        break;
      case "End":
        e.preventDefault();
        satiraGit(toplam - 1);
        break;
      case "Enter":
      case " ":
        e.preventDefault();
        onRowActivate?.(row);
        break;
      default:
    }
  };

  const bosMu = toplam === 0;

  return (
    <div className="dt" style={{ ["--dt-row" as string]: `${rowHeight}px` }}>
      <div
        ref={scrollRef}
        className="dtscroll"
        style={{ maxHeight: height }}
        onScroll={kaydir}
        onMouseLeave={() => onRowHover?.(null)}
      >
        <table style={{ minWidth }} aria-rowcount={toplam}>
          <caption className="sr-only">{caption}</caption>
          <colgroup>
            {columns.map((c) => (
              <col key={c.id} style={c.width ? { width: c.width } : undefined} />
            ))}
          </colgroup>
          <thead>
            <tr>
              {columns.map((c) => {
                const aktifSiralama = sort?.columnId === c.id;
                const th = c.align === "right" ? "r" : "";
                if (!c.sortValue) {
                  return (
                    <th key={c.id} scope="col" className={`static ${th}`.trim()}>
                      {c.header}
                    </th>
                  );
                }
                return (
                  <th
                    key={c.id}
                    scope="col"
                    className={th || undefined}
                    aria-sort={aktifSiralama ? (sort.dir === "asc" ? "ascending" : "descending") : undefined}
                  >
                    <button
                      type="button"
                      className="sorter"
                      onClick={() => siralamayiDegistir(c.id)}
                      aria-label={`${c.headerLabel ?? (typeof c.header === "string" ? c.header : c.id)} kolonuna göre sırala`}
                    >
                      {c.header}
                      <span className="arrow" aria-hidden="true">
                        {aktifSiralama ? (sort.dir === "asc" ? "▲" : "▼") : "▲"}
                      </span>
                    </button>
                  </th>
                );
              })}
            </tr>
          </thead>
          <tbody
            ref={bodyRef}
            onKeyDown={tus}
            // mouseenter kabarmaz; olay devri için mouseover kullanılır.
            onMouseOver={(e) => {
              const i = sira(e);
              if (i >= 0) onRowHover?.(sirali[i]);
            }}
            onFocus={(e) => {
              const i = sira(e);
              if (i >= 0) setAktif(i);
            }}
            onClick={(e) => {
              const i = sira(e);
              if (i >= 0) onRowActivate?.(sirali[i]);
            }}
          >
            {ustDolgu > 0 ? (
              <tr className="pad" aria-hidden="true">
                <td colSpan={columns.length} style={{ height: ustDolgu }} />
              </tr>
            ) : null}

            {sirali.slice(ilk, son).map((row, k) => {
              const index = ilk + k;
              return (
                <tr
                  key={rowKey(row)}
                  data-index={index}
                  data-active={index === aktif ? "true" : undefined}
                  aria-rowindex={index + 2}
                  tabIndex={aktif === -1 ? (k === 0 ? 0 : -1) : index === aktif ? 0 : -1}
                >
                  {hucreler.get(row)}
                </tr>
              );
            })}

            {altDolgu > 0 ? (
              <tr className="pad" aria-hidden="true">
                <td colSpan={columns.length} style={{ height: altDolgu }} />
              </tr>
            ) : null}
          </tbody>
        </table>

        {bosMu ? <div id={`${id}-empty`}>{emptyState}</div> : null}
      </div>

      {footNote ? <div className="dtfoot">{footNote}</div> : null}
    </div>
  );
}
