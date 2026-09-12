import Link from "next/link";
import { Eyebrow, Pill } from "@/components/ui";
import { Grafik } from "@/components/grafik/Grafik";
import { THYAO_ALTIN_BOLGE } from "@/lib/ornek-chartspec";
import { HeroForm } from "@/components/kabuk/HeroForm";
import { OLGULAR } from "@/lib/ornek-veri";

/**
 * Giriş ekranı.
 *
 * Kaydırma tetikli açılış animasyonu YOK — sayfa ilk boyamada eksiksiz okunur
 * (TASARIM_DILI §3: referans sitelerin bu alışkanlığı bir tarama aracında
 * kusurdur).
 */
export default function GirisEkrani() {
  return (
    <>
      <section className="hero">
        <Link className="badge" href="/stratejiler/altin-bolge">
          <b>YENİ</b> Altın Bölge stratejisi yayında <span className="dim">→</span>
        </Link>

        <h1>
          Sinyali de gösteririz,
          <br />
          <em>isabetini de.</em>
        </h1>

        <p className="sub">
          BIST&apos;in 648 hissesi her gün kapanışta taranır. Her strateji kitaptan türetilir, tam
          evrende kalibre edilir ve ileriye dönük getirisi ölçülür — sonuç ne çıkarsa o yazar.
        </p>

        <HeroForm />

        <div className="herocta">
          <Link className="btn ghost" href="#yontem">
            Nasıl çalışır
          </Link>
          <Link className="btn solid" href="/stratejiler">
            Strateji kütüphanesi →
          </Link>
        </div>

        <div className="facts">
          {OLGULAR.map((o) => (
            <div className="fact" key={o.t}>
              <div className="n">{o.n}</div>
              <div className="t">{o.t}</div>
            </div>
          ))}
        </div>

        <div className="preview">
          <div className="chartbar">
            <span className="sym">THYAO</span>
            <span className="dim" style={{ fontSize: 12 }}>
              1G
            </span>
            <Pill tone="acc" small>
              altın bölge
            </Pill>
            <Pill tone="down" small>
              SAT
            </Pill>
            <span style={{ marginLeft: "auto" }} />
            <Eyebrow style={{ letterSpacing: "1.4px", fontSize: 10 }}>örnek veri</Eyebrow>
          </div>
          <Grafik spec={THYAO_ALTIN_BOLGE} yukseklik={250} dar seviyeler="vurgulu" />
        </div>
      </section>

      <section className="mkt" id="yontem">
        <header>
          <Eyebrow>Yöntem</Eyebrow>
          <h2>Bir strateji yayına girmeden önce yedi kapıdan geçer.</h2>
          <p>
            Kapılar sırayla açılır; biri geçilmeden sonraki açılmaz ve tamamı geçilmeden sıradaki
            stratejiye geçilmez. Her stratejinin pasaport dosyası{" "}
            <code className="num" style={{ fontSize: 12 }}>
              docs/strateji/
            </code>{" "}
            altında durur.
          </p>
        </header>

        <div className="kapilar">
          {[
            ["K0", "Kaynak", "Kural kitaptan, sayfa numarasıyla çıkarılır. Ezberden eşik yazmak yasak."],
            ["K1", "Sözleşme", "Parametreler frozen dataclass; sonuç params_hash taşır."],
            ["K2", "Dedektör", "Non-repaint kod. Walk-forward eşitlik testi ve lookahead lint'i."],
            ["K3", "Kalibrasyon", "Tam evrende aday sayısı ölçülür; eşikler burada oturur."],
            ["K4", "İstatistik", "Sembol-kümelenmiş OOS, permütasyon, BH-FDR. Ne çıkarsa o."],
            ["K5", "Görsel", "Referansla yan yana, en az üç iterasyon. Onay kullanıcıdan."],
            ["K6", "Ürün", "Kütüphaneye girer, rozetiyle birlikte yayınlanır."],
          ].map(([k, ad, aciklama]) => (
            <div className="kapi" key={k}>
              <div className="k">{k}</div>
              <h4>{ad}</h4>
              <p>{aciklama}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mkt">
        <header>
          <Eyebrow>Ayrım</Eyebrow>
          <h2>Herkes sinyal gösterir. Biz isabetini de gösteririz.</h2>
          <p>
            Rakiplerin gösterge sayfalarında ileriye dönük getiri yoktur. Bizde her stratejinin
            yanında üç rozetten biri durur ve hangisi olduğu ölçüme bağlıdır — pazarlamaya değil.
          </p>
        </header>
        <div className="kapilar">
          <div className="kapi">
            <div className="k">Rozet</div>
            <h4>
              <Pill tone="acc">izlenen aday</Pill>
            </h4>
            <p>Ölçüldü ve en az çürütülmüş grupta. İddia değil, en iyi adaylardan biri.</p>
          </div>
          <div className="kapi">
            <div className="k">Rozet</div>
            <h4>
              <Pill>kanıtlanmadı</Pill>
            </h4>
            <p>Ölçüldü, çoklu-test düzeltmesinden sonra kenar bulunamadı. Gizlemiyoruz.</p>
          </div>
          <div className="kapi">
            <div className="k">Rozet</div>
            <h4>
              <Pill>ölçülmedi</Pill>
            </h4>
            <p>K4 kapısı henüz açılmadı. Elimizde sayı yok, olduğunu da söylemiyoruz.</p>
          </div>
        </div>
      </section>
    </>
  );
}
