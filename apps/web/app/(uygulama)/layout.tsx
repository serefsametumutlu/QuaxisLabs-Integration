import { UstBar } from "@/components/kabuk/UstBar";
import { Ray } from "@/components/kabuk/Ray";

/**
 * Uygulama kabuğu — yapışkan üst şerit + sol ray + içerik.
 * Tarama, grafik, kütüphane, strateji sayfası ve tasarım vitrini bu kabuğu
 * paylaşır; yüzey değişirken kabuk yerinde kalır.
 */
export default function UygulamaDuzeni({ children }: { children: React.ReactNode }) {
  return (
    <>
      <UstBar />
      <div className="shell">
        <Ray />
        <main className="uygmain">{children}</main>
      </div>
    </>
  );
}
