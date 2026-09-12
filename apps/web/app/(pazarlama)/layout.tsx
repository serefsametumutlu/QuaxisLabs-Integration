import Link from "next/link";
import { ThemeSegment } from "@/components/ui";
import { Duyuru } from "@/components/kabuk/Duyuru";
import { Marka } from "@/components/kabuk/Marka";
import { PAZARLAMA_MENU } from "@/lib/yollar";

/** Pazarlama düzeni — duyuru şeridi, üst şerit, alt bilgi. Giriş ekranı bunu kullanır. */
export default function PazarlamaDuzeni({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Duyuru />
      <header className="mktbar">
        <Marka />
        <nav>
          {PAZARLAMA_MENU.map((m) => (
            <Link key={m.ad} href={m.yol}>
              {m.ad}
            </Link>
          ))}
        </nav>
        <span className="spacer" />
        <ThemeSegment />
        <Link className="giris" href="/tarama">
          Giriş yap
        </Link>
        <Link className="btn" href="/tarama" style={{ height: 32 }}>
          Kayıt ol
        </Link>
      </header>

      <main>{children}</main>

      <footer className="mktfoot">
        <div className="ic">
          <div className="sut">
            <h5>Ürün</h5>
            <Link href="/tarama">Tarama</Link>
            <Link href="/grafik">Grafik</Link>
            <Link href="/stratejiler">Strateji kütüphanesi</Link>
          </div>
          <div className="sut">
            <h5>Yöntem</h5>
            <Link href="/#yontem">Strateji Pasaportu</Link>
            <Link href="/#yontem">Non-repaint sözleşmesi</Link>
            <Link href="/#yontem">İstatistiksel dürüstlük</Link>
          </div>
          <div className="sut">
            <h5>Tasarım</h5>
            <Link href="/tasarim">Tasarım sistemi</Link>
          </div>
        </div>
        <p className="yasal">
          Bu yazılım yatırım tavsiyesi değildir. Sitedeki bütün veriler bu aşamada{" "}
          <b className="mut">örnektir</b>; gerçek tarama çıktısı değildir.
        </p>
      </footer>
    </>
  );
}
