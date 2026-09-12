import Link from "next/link";
import { Card, CardGrid, Eyebrow, Pill } from "@/components/ui";
import { StratejiKucukResim } from "@/components/strateji-kucuk-resim";
import { ORNEK_KARTLAR, VERDIKT_ACIKLAMA } from "@/lib/ornek-veri";
import { STRATEJILER } from "@/lib/ornek-strateji";

/** Kütüphanedeki kartın strateji sayfası varsa oraya, yoksa kendine bağlanır. */
function yol(ad: string) {
  const s = STRATEJILER.find((x) => x.ad === ad);
  return s ? `/stratejiler/${s.slug}` : null;
}

export default function KutuphaneSayfasi() {
  return (
    <section className="board">
      <header>
        <Eyebrow>Yüzey · Strateji Kütüphanesi</Eyebrow>
        <h2>Her strateji, kaynağıyla ve ölçümüyle birlikte</h2>
        <p>
          Kartın yüzü gerçek bir grafik olacak (Faz 4). Altında kaynağı (hangi kitap, hangi sayfa),
          7 kapılık pasaportunun nerede olduğu ve istatistik verdikti.
        </p>
      </header>

      <CardGrid>
        {ORNEK_KARTLAR.map((k) => {
          const hedef = yol(k.ad);
          return (
            <Card
              key={k.ad}
              thumb={<StratejiKucukResim tip={k.tip} />}
              meta={`${k.kaynak} · ${k.kapi}`}
              title={k.ad}
              foot={
                <>
                  <Pill tone="acc">{k.paket}</Pill>
                  <Pill title={VERDIKT_ACIKLAMA[k.verdikt]}>{k.verdikt}</Pill>
                  {hedef ? (
                    <Link href={hedef}>Stratejiyi aç →</Link>
                  ) : (
                    <span className="dim" style={{ marginLeft: "auto", fontSize: 12.5 }}>
                      sayfası yok
                    </span>
                  )}
                </>
              }
            >
              {k.ozet}
            </Card>
          );
        })}
      </CardGrid>

      <p className="dim" style={{ fontSize: 12, margin: "12px 0 0", maxWidth: "80ch", lineHeight: 1.55 }}>
        Örnek kartlar. Kütüphane, Bölüm C&apos;de strateji strateji dolacak; her kartın arkasında 7
        kapıdan geçmiş bir pasaport dosyası olacak. Kapı geçilmeden kart yayına girmez.
      </p>
    </section>
  );
}
