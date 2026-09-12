"use client";

import { useMemo, useRef, useState } from "react";
import {
  Button,
  Chip,
  DataTable,
  EmptyState,
  Eyebrow,
  Pill,
  Sparkline,
  type Kolon,
} from "@/components/ui";
import { VERDIKT_ACIKLAMA, ornekTarama, yasEtiketi, type TaramaSatiri } from "@/lib/ornek-veri";

const SATIR_SAYISI = 500;

const KOLONLAR: Kolon<TaramaSatiri>[] = [
  {
    id: "sembol",
    header: "Sembol",
    className: "sym",
    width: "190px",
    sortValue: (r) => r.sembol,
    cell: (r) => (
      <>
        {r.sembol}
        <span className="sub">{r.ad}</span>
      </>
    ),
  },
  { id: "paket", header: "Paket", width: "150px", className: "mut", sortValue: (r) => r.paket, cell: (r) => r.paket },
  { id: "strateji", header: "Strateji", width: "165px", sortValue: (r) => r.strateji, cell: (r) => r.strateji },
  {
    id: "yon",
    header: "Yön",
    width: "76px",
    sortValue: (r) => r.yon,
    cell: (r) => <Pill tone={r.yon}>{r.yon === "up" ? "AL" : "SAT"}</Pill>,
  },
  { id: "durum", header: "Durum", width: "110px", className: "mut", sortValue: (r) => r.durum, cell: (r) => r.durum },
  {
    id: "yas",
    header: "Yaş",
    align: "right",
    width: "100px",
    className: "num dim",
    sortValue: (r) => r.yas,
    cell: (r) => yasEtiketi(r.yas),
  },
  {
    id: "fiyat",
    header: "Fiyat",
    align: "right",
    width: "96px",
    className: "num",
    sortValue: (r) => r.fiyat,
    cell: (r) => r.fiyat.toFixed(2),
  },
  {
    id: "seviye",
    header: "Seviye",
    align: "right",
    width: "96px",
    className: "num mut",
    sortValue: (r) => r.seviye,
    cell: (r) => r.seviye.toFixed(2),
  },
  {
    id: "seri",
    header: "20 bar",
    width: "84px",
    cell: (r) => <Sparkline points={r.seri} dir={r.yon} />,
  },
  {
    id: "verdikt",
    header: "Tarihsel isabet",
    width: "138px",
    sortValue: (r) => r.verdikt,
    cell: (r) => (
      <Pill tone={r.verdikt === "izlenen aday" ? "acc" : "nötr"} title={VERDIKT_ACIKLAMA[r.verdikt]}>
        {r.verdikt}
      </Pill>
    ),
  },
];

type Olcum = { fps: number; ortalama: number; enKotu: number; kare: number } | null;

/**
 * 500 satırlık DataTable + sanallaştırma ölçümü.
 * Ölçüm, kaydırma sırasındaki gerçek kare aralıklarını (rAF) toplar;
 * sentetik bir sayı değil, tarayıcının o an ürettiği kareler.
 */
export function BuyukTablo() {
  const satirlar = useMemo(() => ornekTarama(SATIR_SAYISI), []);
  const [uzerinde, setUzerinde] = useState<TaramaSatiri | null>(null);
  const [acilan, setAcilan] = useState<TaramaSatiri | null>(null);
  const [olcum, setOlcum] = useState<Olcum>(null);
  const [kosuyor, setKosuyor] = useState(false);
  const [bos, setBos] = useState(false);
  const sarmal = useRef<HTMLDivElement>(null);

  const olc = () => {
    const kutu = sarmal.current?.querySelector<HTMLDivElement>(".dtscroll");
    if (!kutu || kosuyor) return;
    setKosuyor(true);
    setOlcum(null);

    const enUst = kutu.scrollHeight - kutu.clientHeight;
    const sure = 2000;
    const kareler: number[] = [];
    let onceki = performance.now();
    const basla = onceki;

    const adim = (t: number) => {
      kareler.push(t - onceki);
      onceki = t;
      const ilerleme = (t - basla) / sure;
      if (ilerleme >= 1) {
        kutu.scrollTop = 0;
        // ilk kare ölçüme girmesin (rAF'ın kendi ısınması)
        const g = kareler.slice(1);
        const ortalama = g.reduce((a, b) => a + b, 0) / g.length;
        setOlcum({
          fps: Math.round(1000 / ortalama),
          ortalama: +ortalama.toFixed(2),
          enKotu: +Math.max(...g).toFixed(2),
          kare: g.length,
        });
        setKosuyor(false);
        return;
      }
      // ileri-geri: tek yönde bitmeyip aynı mesafeyi iki kez kat etsin
      const d = ilerleme < 0.5 ? ilerleme * 2 : (1 - ilerleme) * 2;
      kutu.scrollTop = enUst * d;
      requestAnimationFrame(adim);
    };
    requestAnimationFrame(adim);
  };

  return (
    <div ref={sarmal}>
      <DataTable
        columns={KOLONLAR}
        rows={bos ? [] : satirlar}
        rowKey={(r) => r.id}
        caption={`${SATIR_SAYISI} satırlık örnek tarama sonucu; kolonlar sıralanabilir, liste sanallaştırılmıştır.`}
        height={420}
        initialSort={{ columnId: "yas", dir: "asc" }}
        onRowHover={setUzerinde}
        onRowActivate={setAcilan}
        emptyState={
          <EmptyState
            title="Bu filtreye uyan sinyal yok."
            action={
              <Button variant="ghost" size="sm" onClick={() => setBos(false)}>
                Filtreyi gevşet
              </Button>
            }
          >
            Sahte veri üretmiyoruz; boşsa boş görünür.
          </EmptyState>
        }
        footNote={
          <>
            <span>
              <span className="num">{bos ? 0 : satirlar.length}</span> satır ·{" "}
              <span className="num">{KOLONLAR.length}</span> kolon
            </span>
            <span className="ayrac" />
            <span>
              satır üzeri:{" "}
              <span className="num">{uzerinde ? uzerinde.sembol : "—"}</span>
            </span>
            <span className="ayrac" />
            <span>
              açılan: <span className="num">{acilan ? acilan.sembol : "—"}</span>
            </span>
            <span style={{ marginLeft: "auto" }} />
            <Chip pressed={bos} onClick={() => setBos((b) => !b)}>
              Boş durum
            </Chip>
          </>
        }
      />

      <div className="olcum">
        <Eyebrow>Sanallaştırma ölçümü</Eyebrow>
        <Button size="sm" variant="ghost" onClick={olc} disabled={kosuyor || bos}>
          {kosuyor ? "Ölçülüyor…" : "2 sn kaydır ve ölç"}
        </Button>
        <span className="ayrac" />
        {olcum ? (
          <>
            <span>
              <span className="deger">{olcum.fps}</span> fps
            </span>
            <span>
              ortalama kare <span className="deger">{olcum.ortalama.toFixed(2)}</span> ms
            </span>
            <span>
              en kötü kare <span className="deger">{olcum.enKotu.toFixed(2)}</span> ms
            </span>
            <span className="dim">
              (<span className="num">{olcum.kare}</span> kare)
            </span>
          </>
        ) : (
          <span>
            {SATIR_SAYISI} satır yüklü; DOM&apos;da yalnızca görünen pencere + taşma payı çizilir.
          </span>
        )}
        <span style={{ marginLeft: "auto" }} />
        <Eyebrow style={{ letterSpacing: "1.4px", fontSize: 10 }}>örnek veri</Eyebrow>
      </div>

      <p className="mut" style={{ fontSize: 12, margin: "10px 0 0", maxWidth: "78ch", lineHeight: 1.55 }}>
        Satır üzerine gelmek <b style={{ fontWeight: 500 }}>onRowHover</b> kancasını tetikler — Faz
        3&apos;te sağdan açılan grafik çekmecesi buna bağlanacak. Klavye:{" "}
        <b style={{ fontWeight: 500 }}>↑ ↓ Home End PageUp PageDown</b> satır değiştirir,{" "}
        <b style={{ fontWeight: 500 }}>Enter</b> satırı açar; odak pencere dışına
        çıkarsa liste kendini kaydırır. Kolon başlıkları üç durumlu: artan → azalan → sırasız.
      </p>
    </div>
  );
}
