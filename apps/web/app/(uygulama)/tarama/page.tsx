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
  SERI_BAR,
  TARAMA,
  VERDIKT_ACIKLAMA,
  seri,
  yasEtiketi,
  type TaramaSatiri,
} from "@/lib/tarama";

const TAZELIK = [
  { value: "1", label: "Son 1 mum" },
  { value: "3", label: "Son 3 mum" },
  { value: "10", label: "Son 10 mum" },
  { value: "hepsi", label: "Tümü" },
] as const;

/** Zaman dilimi seçenekleri KOŞUDAN gelir, elle yazılmaz. Taranmamış bir
 *  zaman dilimini seçenek olarak sunmak, boş listeyi "sinyal yok" diye
 *  gösterirdi — oysa doğrusu "orada hiç bakılmadı". */
const TF = TARAMA.kunye.zamanDilimleri.map((z) => ({ value: z.kod, label: z.ad }));

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
    width: "84px",
    sortValue: (r) => r.sembol,
    cell: (r) => r.sembol,
  },
  { id: "paket", header: "Paket", width: "152px", className: "mut", sortValue: (r) => r.paket, cell: (r) => r.paket },
  { id: "strateji", header: "Strateji", width: "188px", sortValue: (r) => r.strateji, cell: (r) => r.strateji },
  {
    id: "yon",
    header: "Yön",
    width: "66px",
    sortValue: (r) => r.yon,
    cell: (r) => <Pill tone={r.yon}>{r.yon === "up" ? "AL" : "SAT"}</Pill>,
  },
  { id: "durum", header: "Durum", width: "92px", className: "mut", sortValue: (r) => r.durum, cell: (r) => r.durum },
  {
    id: "yas",
    header: "Yaş",
    align: "right",
    width: "86px",
    className: "num dim",
    // Yaşı bilinmeyen satır (eski run'dan gelen kayıt) en sona düşsün —
    // "0" saymak onu en taze satır gibi gösterirdi.
    sortValue: (r) => r.yas ?? Number.MAX_SAFE_INTEGER,
    cell: (r) => yasEtiketi(r.yas),
  },
  {
    id: "fiyat",
    header: "Fiyat",
    align: "right",
    width: "82px",
    className: "num",
    sortValue: (r) => r.fiyat,
    cell: (r) => r.fiyat.toFixed(2),
  },
  {
    id: "seviye",
    header: "Seviye",
    align: "right",
    width: "82px",
    className: "num mut",
    sortValue: (r) => r.seviye ?? 0,
    cell: (r) => (r.seviye === null ? "—" : r.seviye.toFixed(2)),
  },
  {
    id: "seri",
    header: `${SERI_BAR} bar`,
    // 84px: sparkline 62px + 2×12px hücre dolgusu. 76px'te SVG hücreyi
    // 4 piksel taşıyordu.
    width: "84px",
    cell: (r) => <Sparkline points={seri(r)} dir={r.yon} />,
  },
  {
    id: "verdikt",
    header: "Tarihsel isabet",
    width: "150px",
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
  const kunye = TARAMA.kunye;
  const [tazelik, setTazelik] = useState<string>("3");
  const [tf, setTf] = useState<string>(TF[0]?.value ?? "");
  const [yon, setYon] = useState<string>("hepsi");
  const [acilan, setAcilan] = useState<TaramaSatiri | null>(null);

  const satirlar = useMemo(() => {
    const esik = tazelik === "hepsi" ? Infinity : Number(tazelik);
    return TARAMA.satirlar.filter(
      (r) =>
        r.zamanDilimi === tf &&
        (r.yas === null ? tazelik === "hepsi" : r.yas < esik) &&
        (yon === "hepsi" || r.yon === yon),
    );
  }, [tazelik, tf, yon]);

  const yukari = satirlar.filter((r) => r.yon === "up").length;

  /** En üretken paket — elle "Yapı" yazmak yerine sayılır. */
  const enUretkenPaket = useMemo(() => {
    const sayim = new Map<string, number>();
    for (const r of satirlar) sayim.set(r.paket, (sayim.get(r.paket) ?? 0) + 1);
    const en = [...sayim.entries()].sort((a, b) => b[1] - a[1])[0];
    return en ? en[0] : "—";
  }, [satirlar]);

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
            label="Filtreye uyan sinyal"
            value={satirlar.length}
            hint={<span>{kunye.eslesen} sinyalin içinden</span>}
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
          <StatTile
            label="En üretken paket"
            value={enUretkenPaket}
            textValue
            hint="bu filtredeki çoğunluk"
          />
          <StatTile
            label="Tarama süresi"
            value={
              kunye.sureSn === null ? (
                "—"
              ) : (
                <>
                  {Math.floor(kunye.sureSn / 60)}
                  <Unit>dk</Unit> {kunye.sureSn % 60}
                  <Unit>sn</Unit>
                </>
              )
            }
            textValue={kunye.sureSn === null}
            hint={`${kunye.taranan} sembol · ${kunye.zamanDilimleri.map((z) => z.ad).join(" + ")}`}
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
          caption={`${kunye.tarih} kapanış taraması — gerçek çıktı; kolonlar sıralanabilir, liste sanallaştırılmıştır.`}
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
                <span className="num">{satirlar.length}</span> sinyal ·{" "}
                <span className="num">{kunye.taranan}</span> sembol tarandı
              </span>
              <span className="ayrac" />
              <span>satıra tıkla → grafik çekmecesi</span>
              <span style={{ marginLeft: "auto" }} />
              <Chip onClick={() => setTazelik("3")}>Filtreleri sıfırla</Chip>
            </>
          }
        />

        <p className="dim" style={{ fontSize: 12, margin: "10px 0 0", maxWidth: "80ch", lineHeight: 1.55 }}>
          <b className="mut">{kunye.runId}</b> koşusunun gerçek çıktısı ·{" "}
          <span className="num">{kunye.taranan}</span>/
          <span className="num">{kunye.evren ?? "—"}</span> sembol ·{" "}
          {kunye.zamanDilimleri.map((z) => z.ad).join(" + ")} · kod{" "}
          <span className="num">{kunye.gitSha ?? "—"}</span>.{" "}
          {kunye.verisiGelmeyen.length > 0 && (
            <>
              <span className="num">{kunye.verisiGelmeyen.length}</span> sembolde sağlayıcı veri
              döndürmedi ve o sembollere <b className="mut">hiç bakılmadı</b>:{" "}
              <span className="mut">{kunye.verisiGelmeyen.join(", ")}</span>.{" "}
            </>
          )}
          <b className="mut">Tarihsel isabet</b> kolonu K4 (istatistik) kapısının çıktısını taşır ve
          satırın göstergesini sahiplenen pasaporttan okunur — uydurulmaz; ölçülmemiş bir strateji
          burada “ölçülmedi” görünür, gizlenmez.{" "}
          {kunye.kesilen > 0 && (
            <>
              Satır sınırı yüzünden <span className="num">{kunye.kesilen}</span> sinyal bu listeye
              girmedi.{" "}
            </>
          )}
          {kunye.veriYok > 0 && (
            <>
              <span className="num">{kunye.veriYok}</span> sinyal, fiyat serisi okunamadığı için
              atlandı.{" "}
            </>
          )}
          Şirket adı kolonu yok: evren dosyasında sembol var, ad yok — elimizde olmayan bir alanı
          doldurmuyoruz.
        </p>
      </section>

      <Cekmece satir={acilan} kapat={() => setAcilan(null)} />
    </>
  );
}
