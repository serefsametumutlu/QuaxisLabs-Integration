"use client";

import { useMemo, useState } from "react";
import {
  Button,
  Chip,
  ChipGroup,
  DataTable,
  EmptyState,
  Eyebrow,
  Pill,
  Sparkline,
  StatTile,
  StatTileGrid,
  Unit,
  type Kolon,
} from "@/components/ui";
import { Cekmece } from "@/components/kabuk/Cekmece";
import {
  ORNEK_TARAMA,
  VERDIKT_ACIKLAMA,
  ornekTarama,
  yasEtiketi,
  type TaramaSatiri,
} from "@/lib/ornek-veri";

const TAZELIK = [
  { value: "1", label: "Son 1 mum" },
  { value: "3", label: "Son 3 mum" },
  { value: "10", label: "Son 10 mum" },
  { value: "hepsi", label: "Tümü" },
] as const;

const TF = [
  { value: "1g", label: "1G" },
  { value: "4s", label: "4S" },
] as const;

const YON = [
  { value: "hepsi", label: "Tümü" },
  { value: "up", label: "AL" },
  { value: "down", label: "SAT" },
] as const;

const KOLONLAR: Kolon<TaramaSatiri>[] = [
  {
    id: "sembol",
    header: "Sembol",
    className: "sym",
    width: "176px",
    sortValue: (r) => r.sembol,
    cell: (r) => (
      <>
        {r.sembol}
        <span className="sub">{r.ad}</span>
      </>
    ),
  },
  { id: "paket", header: "Paket", width: "126px", className: "mut", sortValue: (r) => r.paket, cell: (r) => r.paket },
  { id: "strateji", header: "Strateji", width: "150px", sortValue: (r) => r.strateji, cell: (r) => r.strateji },
  {
    id: "yon",
    header: "Yön",
    width: "76px",
    sortValue: (r) => r.yon,
    cell: (r) => <Pill tone={r.yon}>{r.yon === "up" ? "AL" : "SAT"}</Pill>,
  },
  { id: "durum", header: "Durum", width: "104px", className: "mut", sortValue: (r) => r.durum, cell: (r) => r.durum },
  {
    id: "yas",
    header: "Yaş",
    align: "right",
    width: "94px",
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
    width: "88px",
    className: "num mut",
    sortValue: (r) => r.seviye,
    cell: (r) => r.seviye.toFixed(2),
  },
  { id: "seri", header: "20 bar", width: "72px", cell: (r) => <Sparkline points={r.seri} dir={r.yon} /> },
  {
    id: "verdikt",
    header: "Tarihsel isabet",
    width: "130px",
    sortValue: (r) => r.verdikt,
    cell: (r) => (
      <Pill tone={r.verdikt === "izlenen aday" ? "acc" : "nötr"} title={VERDIKT_ACIKLAMA[r.verdikt]}>
        {r.verdikt}
      </Pill>
    ),
  },
];

/** Tarama — ürünün giriş noktası. Tazelik birinci sınıf filtre. */
export default function TaramaSayfasi() {
  const [tazelik, setTazelik] = useState<string>("3");
  const [tf, setTf] = useState<string>("1g");
  const [yon, setYon] = useState<string>("hepsi");
  const [acilan, setAcilan] = useState<TaramaSatiri | null>(null);

  const tumu = useMemo(() => ornekTarama(160), []);

  const satirlar = useMemo(() => {
    const esik = tazelik === "hepsi" ? Infinity : Number(tazelik);
    return tumu.filter((r) => r.yas < esik && (yon === "hepsi" || r.yon === yon));
  }, [tumu, tazelik, yon]);

  const yukari = satirlar.filter((r) => r.yon === "up").length;

  return (
    <>
      <section className="board">
        <header>
          <Eyebrow>Yüzey · Tarama</Eyebrow>
          <h2>Bugün hangi hissede hangi strateji sinyal verdi</h2>
          <p>
            Ürünün giriş noktası. Tazelik birinci sınıf filtre, varsayılan <b>son 3 mum</b>. Satıra
            tıklayınca sağdan grafik çekmecesi açılır — sayfa değişmez.
          </p>
        </header>

        <StatTileGrid>
          <StatTile
            label="Yeni sinyal"
            value={satirlar.length}
            hint={
              <>
                <Pill tone="up" small>
                  +12
                </Pill>
                <span>önceki koşuya göre</span>
              </>
            }
          />
          <StatTile
            label="Yön dağılımı"
            value={
              <>
                <span style={{ color: "var(--up)" }}>{yukari}</span>
                <span className="dim"> / </span>
                <span style={{ color: "var(--down)" }}>{satirlar.length - yukari}</span>
              </>
            }
            hint="alış / satış"
          />
          <StatTile label="En üretken paket" value="Yapı" textValue hint="sinyallerin çoğunluğu" />
          <StatTile
            label="Tarama süresi"
            value={
              <>
                6<Unit>dk</Unit> 22<Unit>sn</Unit>
              </>
            }
            hint="648 sembol · 4S + 1G"
          />
        </StatTileGrid>

        <div className="filters">
          <ChipGroup label="Tazelik" options={TAZELIK} value={tazelik} onChange={setTazelik} />
          <span className="sep" />
          <ChipGroup label="Zaman dilimi" options={TF} value={tf} onChange={setTf} />
          <span className="sep" />
          <ChipGroup label="Yön" options={YON} value={yon} onChange={setYon} />
          {/* İki eylem tek grupta: ayrı ayrı bırakılınca sarma sırasında
              biri alt satıra tek başına düşüyordu (f3i1 bulgusu). */}
          <span className="row" style={{ marginLeft: "auto", gap: 8 }}>
            <Button variant="ghost">Taramayı kaydet</Button>
            <Button>Bugünü tara</Button>
          </span>
        </div>

        <DataTable
          columns={KOLONLAR}
          rows={satirlar}
          rowKey={(r) => r.id}
          caption="Bugünün tarama sonuçları — örnek veri; kolonlar sıralanabilir, liste sanallaştırılmıştır."
          height={520}
          initialSort={{ columnId: "yas", dir: "asc" }}
          onRowActivate={setAcilan}
          emptyState={
            <EmptyState
              title={`Son ${tazelik} mumda bu filtreye uyan sinyal yok.`}
              action={
                <Button variant="ghost" size="sm" onClick={() => setTazelik("hepsi")}>
                  Tazeliği gevşet
                </Button>
              }
            >
              Sahte veri üretmiyoruz; boşsa boş görünür.
            </EmptyState>
          }
          footNote={
            <>
              <span>
                <span className="num">{satirlar.length}</span> sinyal · <span className="num">648</span>{" "}
                sembol tarandı
              </span>
              <span className="ayrac" />
              <span>satıra tıkla → grafik çekmecesi</span>
              <span style={{ marginLeft: "auto" }} />
              <Chip onClick={() => setTazelik("3")}>Filtreleri sıfırla</Chip>
            </>
          }
        />

        <p className="dim" style={{ fontSize: 12, margin: "10px 0 0", maxWidth: "80ch", lineHeight: 1.55 }}>
          Örnek veri — gerçek tarama çıktısı değil.{" "}
          <b className="mut">Tarihsel isabet</b> kolonu K4 (istatistik) kapısının çıktısını taşır;
          ölçülmemiş bir strateji burada “ölçülmedi” görünür, gizlenmez. İlk{" "}
          <span className="num">{ORNEK_TARAMA.length}</span> satır gerçek BIST sembolleriyle, kalanı
          türetilmiş örnek kodlarla.
        </p>
      </section>

      <Cekmece satir={acilan} kapat={() => setAcilan(null)} />
    </>
  );
}
