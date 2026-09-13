import { notFound } from "next/navigation";
import { Eyebrow, Faq, Pill } from "@/components/ui";
import { STRATEJILER, stratejiBul } from "@/lib/ornek-strateji";
import { OlcumSutunlari } from "./olcum-sutunlari";
import { StratejiGovde } from "./govde";

export function generateStaticParams() {
  return STRATEJILER.map((s) => ({ slug: s.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const s = stratejiBul(slug);
  return { title: s ? `${s.ad} · QuaxisLabs` : "QuaxisLabs" };
}

/**
 * Strateji sayfası — bir stratejinin tam künyesi.
 *
 * İskelet LuxAlgo'nun gösterge sayfasından alındı. İki bölüm bizi ayırıyor:
 * KAYNAK ("bu eşik nereden geldi?") ve ÖLÇÜM ("işe yarıyor mu?"). Rakipler 874
 * gösterge yayınlıyor ve hiçbirinin ileriye dönük getirisini göstermiyor.
 */
export default async function StratejiSayfasi({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const s = stratejiBul(slug);
  if (!s) notFound();

  return (
    <section className="board">
      <header>
        <Eyebrow>Yüzey · Strateji sayfası</Eyebrow>
      </header>

      <div className="stratHead">
        <div>
          <Eyebrow>{s.paket} paketi</Eyebrow>
          <h2>{s.ad}</h2>
          <p>{s.ozet}</p>
        </div>
        <div className="rt">
          {s.rozetler.map((r) => (
            <Pill key={r}>{r}</Pill>
          ))}
          <Pill>{s.verdikt}</Pill>
        </div>
      </div>

      <StratejiGovde strateji={s} />

      {/* ── PARAMETRELER ── */}
      <div className="sect">
        <h3>
          Parametreler <span className="gate">K1 · SÖZLEŞME</span>
        </h3>
        <p className="lede">
          Hepsi <code className="num" style={{ fontSize: 12 }}>frozen dataclass</code> alanı; sonuç
          kaydı bir <code className="num" style={{ fontSize: 12 }}>params_hash</code> taşır. Aynı
          veri + aynı parametre = bit bit aynı sonuç.
        </p>
        <div className="params">
          {s.parametreler.map((g) => (
            <div key={g.baslik}>
              <h4>{g.baslik}</h4>
              <dl>
                {g.alanlar.map((a) => (
                  <div key={a.ad}>
                    <dt>
                      {a.ad} <span className="def">{a.varsayilan}</span>
                    </dt>
                    <dd>{a.aciklama}</dd>
                  </div>
                ))}
              </dl>
            </div>
          ))}
        </div>
      </div>

      {/* ── KAYNAK ── */}
      <div className="sect">
        <h3>
          Kaynak <span className="gate">K0 · KAYNAK</span>
        </h3>
        <p className="lede">
          Her eşiğin nereden geldiği burada yazar. <b>Ezberden sayı yazmak yasak</b> — kitapta
          yoksa, ölçümle türetildiği belirtilir.
        </p>
        <div className="src">
          {s.kaynak.map((k) => (
            <div className={k.acik ? "srcbox gap" : "srcbox"} key={k.etiket}>
              <div className="k">{k.etiket}</div>
              <p>
                {k.kodOnce && k.kod ? (
                  <>
                    <code>{k.kod}</code>{" "}
                  </>
                ) : null}
                {k.govde}
                {!k.kodOnce && k.kod ? (
                  <>
                    {" "}
                    <code>{k.kod}</code>
                  </>
                ) : null}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* ── ÖLÇÜM ── */}
      <div className="sect">
        <h3>
          Ölçüm <span className="gate">K3 · K4</span>
        </h3>
        <p className="lede">
          Bu bölüm rakiplerde yok. Stratejinin işe yarayıp yaramadığı burada yazar — <b>ne çıkarsa o.</b>
        </p>

        {s.olcum ? (
          <div className="measure">
            <div>
              <table className="mtable">
                <thead>
                  <tr>
                    <th colSpan={2}>K4 · Sembol-kümelenmiş OOS testi</th>
                  </tr>
                </thead>
                <tbody>
                  {s.olcum.satirlar.map(([k, v]) => (
                    <tr key={k}>
                      <td>{k}</td>
                      <td>{v}</td>
                    </tr>
                  ))}
                  {s.olcum.kotu ? (
                    <tr>
                      <td>BH-FDR (q=0.05)</td>
                      <td style={{ color: "var(--down)" }}>geçemedi</td>
                    </tr>
                  ) : null}
                </tbody>
              </table>
              <p className="dim" style={{ fontSize: 12, margin: "12px 0 0", lineHeight: 1.55 }}>
                {s.olcum.uyari}
              </p>
            </div>
            <OlcumSutunlari olcum={s.olcum} />
          </div>
        ) : (
          <div className="srcbox gap">
            <div className="k">Ölçüm yok</div>
            <p>
              Bu strateji K4 kapısına gelmedi. <b>Sayı uydurmuyoruz</b>: kutu doldurulana kadar boş
              durur ve kütüphanedeki rozeti “ölçülmedi” kalır.
            </p>
          </div>
        )}
      </div>

      {/* ── SSS ── */}
      <div className="sect">
        <h3>Sık sorulanlar</h3>
        {s.sss.map((f, i) => (
          <Faq key={f.soru} question={f.soru} open={i === 0}>
            {f.cevap}
          </Faq>
        ))}
      </div>
    </section>
  );
}
