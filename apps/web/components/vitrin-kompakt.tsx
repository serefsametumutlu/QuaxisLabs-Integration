"use client";

import { useState } from "react";
import {
  Button,
  Card,
  CardGrid,
  Chip,
  ChipGroup,
  DataTable,
  EmptyState,
  Eyebrow,
  Faq,
  Panel,
  Pill,
  Seg,
  SkeletonBlock,
  Sparkline,
  StatTile,
  StatTileGrid,
  Tabs,
  Unit,
  type Kolon,
} from "@/components/ui";
import { ORNEK_KARTLAR, ORNEK_TARAMA, VERDIKT_ACIKLAMA, ornekSeri, yasEtiketi, type TaramaSatiri } from "@/lib/ornek-veri";
import { StratejiKucukResim } from "@/components/strateji-kucuk-resim";

const TAZELIK = [
  { value: "1", label: "Son 1 mum" },
  { value: "3", label: "Son 3 mum" },
  { value: "10", label: "Son 10 mum" },
] as const;

const TF = [
  { value: "1g", label: "1G" },
  { value: "4s", label: "4S" },
] as const;

const GORUNUM = [
  { value: "grafik", label: "Grafik" },
  { value: "kaynak", label: "Kaynak" },
] as const;

const KOLONLAR: Kolon<TaramaSatiri>[] = [
  {
    id: "sembol",
    header: "Sembol",
    className: "sym",
    width: "34%",
    sortValue: (r) => r.sembol,
    cell: (r) => r.sembol,
  },
  {
    id: "yon",
    header: "Yön",
    width: "20%",
    sortValue: (r) => r.yon,
    cell: (r) => <Pill tone={r.yon}>{r.yon === "up" ? "AL" : "SAT"}</Pill>,
  },
  {
    id: "fiyat",
    header: "Fiyat",
    align: "right",
    width: "26%",
    className: "num",
    sortValue: (r) => r.fiyat,
    cell: (r) => r.fiyat.toFixed(2),
  },
  {
    id: "seri",
    header: "20 bar",
    width: "20%",
    cell: (r) => <Sparkline points={ornekSeri(r)} dir={r.yon} width={54} height={16} />,
  },
];

/**
 * Bir temanın altında tüm bileşenleri gösteren kompakt vitrin.
 * /tasarim sayfasında üç kez, üç farklı `data-theme` kapsamında çizilir.
 */
export function VitrinKompakt() {
  const [tazelik, setTazelik] = useState<string>("3");
  const [tf, setTf] = useState<string>("1g");
  const [gorunum, setGorunum] = useState<string>("grafik");
  const [bos, setBos] = useState(false);

  return (
    <>
      <div className="vblok">
        <p className="vb">Düğme · Çip · Rozet</p>
        <div className="row">
          <Button>Bugünü tara</Button>
          <Button variant="ghost">Dışa aktar</Button>
          <Button variant="solid" size="sm">
            Kütüphane →
          </Button>
        </div>
        <div className="row" style={{ marginTop: 10 }}>
          <ChipGroup label="Tazelik" options={TAZELIK} value={tazelik} onChange={setTazelik} />
        </div>
        <div className="row" style={{ marginTop: 10 }}>
          <Pill tone="up">AL</Pill>
          <Pill tone="down">SAT</Pill>
          <Pill tone="acc">yapı</Pill>
          <Pill>ONAYLANDI</Pill>
          <Chip disabled>Devre dışı</Chip>
        </div>
      </div>

      <div className="vblok">
        <p className="vb">Segment · Sekme · Tema anahtarı</p>
        <div className="row">
          <Seg label="Zaman dilimi" options={TF} value={tf} onChange={setTf} mono />
        </div>
        <div style={{ marginTop: 10 }}>
          <Tabs label="Görünüm" options={GORUNUM} value={gorunum} onChange={setGorunum}>
            <p className="spec-note mut" style={{ margin: 0, fontSize: 12.5 }}>
              {gorunum === "grafik"
                ? "Sekme bir PANELİ değiştirir — bu yüzden gerçek tablist semantiği ve ok tuşu gezinmesi var."
                : "Kaynak sekmesi K0 kapısının çıktısını taşıyacak: hangi kitap, hangi sayfa, hangi eşik."}
            </p>
          </Tabs>
        </div>
      </div>

      <StatTileGrid style={{ gridTemplateColumns: "repeat(2, minmax(0,1fr))" }}>
        <StatTile
          label="Yeni sinyal"
          value="47"
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
          label="Tarama süresi"
          value={
            <>
              6<Unit>dk</Unit> 22<Unit>sn</Unit>
            </>
          }
          hint="648 sembol · 4S + 1G"
        />
      </StatTileGrid>

      <Panel
        padded={false}
        head={
          <>
            <span className="sym">THYAO</span>
            <Pill tone="acc" small>
              fibo abcd
            </Pill>
            <Pill tone="down" small>
              SAT
            </Pill>
            <span style={{ marginLeft: "auto" }} />
            <Eyebrow style={{ letterSpacing: "1.4px", fontSize: 10 }}>örnek veri</Eyebrow>
          </>
        }
      >
        <DataTable
          columns={KOLONLAR}
          rows={bos ? [] : ORNEK_TARAMA}
          rowKey={(r) => r.id}
          caption="Örnek tarama sonuçları — dört kolon"
          height={200}
          minWidth={0}
          initialSort={{ columnId: "sembol", dir: "asc" }}
          emptyState={
            <EmptyState
              title="Son 3 mumda bu filtreye uyan sinyal yok."
              action={
                <Button variant="ghost" size="sm" onClick={() => setBos(false)}>
                  Tazeliği gevşet
                </Button>
              }
            >
              Tazeliği “son 10 mum”a gevşetmeyi deneyebilirsin.
            </EmptyState>
          }
          footNote={
            <>
              <span>
                <span className="num">{bos ? 0 : ORNEK_TARAMA.length}</span> satır · örnek veri
              </span>
              <span style={{ marginLeft: "auto" }} />
              <Chip pressed={bos} onClick={() => setBos((b) => !b)}>
                Boş durumu göster
              </Chip>
            </>
          }
        />
      </Panel>

      <CardGrid style={{ gridTemplateColumns: "1fr" }}>
        <Card
          thumb={<StratejiKucukResim tip={ORNEK_KARTLAR[0].tip} />}
          meta={`${ORNEK_KARTLAR[0].kaynak} · ${ORNEK_KARTLAR[0].kapi}`}
          title={ORNEK_KARTLAR[0].ad}
          foot={
            <>
              <Pill tone="acc">{ORNEK_KARTLAR[0].paket}</Pill>
              <Pill title={VERDIKT_ACIKLAMA[ORNEK_KARTLAR[0].verdikt]}>{ORNEK_KARTLAR[0].verdikt}</Pill>
              <a href="#tasarim-kartlar">Stratejiyi aç →</a>
            </>
          }
        >
          {ORNEK_KARTLAR[0].ozet}
        </Card>
      </CardGrid>

      <div className="vblok">
        <p className="vb">Yükleniyor · Boş durum</p>
        <SkeletonBlock lines={3} />
        <div style={{ marginTop: 12 }}>
          <EmptyState title="Bu pakette henüz ölçülmüş strateji yok.">
            K4 kapısı açılınca burada isabet rozeti belirir.
          </EmptyState>
        </div>
      </div>

      <div className="vblok">
        <p className="vb">Sık sorulanlar</p>
        <Faq question="Sinyal sonradan kaybolur mu?" open>
          Hayır. Sinyal, pivotun oluştuğu barın değil <b>onaylandığı barın</b> tarihini taşır ve
          geçmişe dönük hiçbir zaman değişmez.
        </Faq>
        <Faq question="“Kanıtlanmadı” rozeti ne demek?">
          Çoklu-test düzeltmesinden sonra sıfırdan ayırt edilebilir bir kenar bulunamadı. “Zarar
          ettiriyor” demek değil; elimizde kanıt yok demek.
        </Faq>
      </div>

      <div className="vblok">
        <p className="vb">Metin kademesi · Sayı dizgisi</p>
        <div className="stack" style={{ gap: 4 }}>
          <span>Birincil — sinyalin kendisi</span>
          <span className="mut">İkincil — bağlam ve açıklama</span>
          <span className="dim">Üçüncül — etiket, birim, zaman damgası</span>
        </div>
        <ul className="scale num" style={{ marginTop: 11 }}>
          {ORNEK_TARAMA.slice(0, 4).map((r) => (
            <li key={r.id}>
              <span>{r.sembol}</span>
              <span>
                {r.fiyat.toFixed(2)} <span className="dim">{yasEtiketi(r.yas)}</span>
              </span>
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}
