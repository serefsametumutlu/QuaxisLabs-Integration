"use client";

import { useState, useSyncExternalStore } from "react";
import { Eyebrow, Pill, Seg } from "@/components/ui";
import { Grafik } from "@/components/grafik/Grafik";
import {
  VITRIN,
  VITRIN_SECENEKLERI,
  odulRisk,
  seviyeSatirlari,
} from "@/lib/vitrin";

/**
 * Grafik yüzeyi — sinyalin nasıl doğduğunun görsel kanıtı.
 *
 * Sayfa artık TEK bir stratejiye gömülü değil. Golden Zone ve dört
 * Pesavento harmoniği arasında geçiş yapılabiliyor; her biri **gerçek
 * veriden** üretilmiş kendi spec'ini, kendi seviyelerini ve kendi K4
 * verdiktini taşıyor.
 *
 * Seçici eklenirken istatistik kutusu da değişti: eskiden `0.62`, `0.705`,
 * `BOS` etiketlerini ELLE taşıyordu, yani Golden Zone'a özeldi. Şimdi
 * spec'in kendi seviye etiketlerinden üretiliyor — ikinci bir strateji
 * eklemek artık o kutuyu kopyalamayı gerektirmiyor ve kopyalanan sayının
 * spec'ten kopma ihtimali kalmıyor.
 *
 * **Beşinin de verdikti `kanıtlanmadı`.** Ölçülmemiş bir strateji vitrine
 * konulmaz; ölçülüp kenar bulunamayan ise ETİKETİYLE konur (README madde
 * 6: eleme değil etiketleme). Kullanıcı formasyonu görür, sistem ona "al"
 * demez.
 */
const VARSAYILAN = "harmonik-gartley";

/** URL'de istenen formasyon. Statik dışa aktarımda sunucu tarafında
 *  `location` yoktur; `useSyncExternalStore` sunucu ve istemci anlık
 *  görüntülerini AYRI verdiği için hidrasyon uyuşmazlığı doğmaz. Etki
 *  içinde `setState` çağırmak (basamaklı render) gerekmiyor. */
function urldekiFormasyon(): string {
  const f = new URLSearchParams(window.location.search).get("f");
  return f && f in VITRIN ? f : VARSAYILAN;
}

/** Hidrasyondan sonra BİR KEZ haber verir.
 *
 * `useSyncExternalStore`, hidrasyonda `getServerSnapshot`ı kullanır ve
 * mağaza haber vermedikçe istemci anlık görüntüsünü **hiç okumaz**. Abone
 * fonksiyonu boş bırakılınca `?f=` sorgusu sayfaya hiç ulaşmıyordu —
 * ölçüldü: URL `?f=harmonik-kelebek` iken levha Gartley çiziyordu.
 */
const ABONE = (bildir: () => void) => {
  const zamanlayici = setTimeout(bildir, 0);
  return () => clearTimeout(zamanlayici);
};

export default function GrafikSayfasi() {
  // `?f=harmonik-kelebek` ile doğrudan bir formasyona bağlanılabilir.
  //
  // İki işi birden görüyor. Ürün tarafında: bir kurulumu paylaşmanın yolu.
  // Geliştirme tarafında: görsel kabul döngüsü her formasyonu AYRI
  // yakalayabiliyor — seçiciye tıklayıp ekran görüntüsü almak, sayfanın o
  // an boyanıp boyanmadığına bağlı kırılgan bir ölçümdü.
  const baslangic = useSyncExternalStore(
    ABONE,
    urldekiFormasyon,
    () => VARSAYILAN,
  );
  const [secilen, setSecilen] = useState<string | null>(null);
  const slug = secilen ?? baslangic;
  const setSlug = setSecilen;
  const kayit = VITRIN[slug] ?? VITRIN["golden-zone"];
  const spec = kayit.spec;
  const satirlar = seviyeSatirlari(spec);
  const rr = odulRisk(spec);
  const yukari = spec.kunye.yon === "al";

  return (
    <section className="board">
      <header>
        <Eyebrow>Yüzey · Grafik</Eyebrow>
        <h2>Sinyalin nasıl doğduğunun görsel kanıtı</h2>
        <p>
          Levha bir <code className="num" style={{ fontSize: 12 }}>ChartSpec</code> okuyor. Mum,
          hacim, crosshair ve zoom/pan Lightweight Charts&apos;tan; fibo seviyeleri, formasyon
          gövdeleri, köşeler ve durum rozeti bizim SVG katmanımızdan geliyor. Spec&apos;i Python
          komposeri <b>gerçek veriden</b> üretti — <b>çizici hiçbir seviyeyi kendisi hesaplamaz.</b>
        </p>
      </header>

      <div className="chartframe">
        <div className="chartbar">
          <span className="sym">{spec.kunye.sembol}</span>
          <span className="dim" style={{ fontSize: 12 }}>
            {spec.kunye.zaman_dilimi.toLocaleUpperCase("tr")} · BIST
          </span>
          <Seg
            label="Strateji"
            options={VITRIN_SECENEKLERI}
            value={slug}
            onChange={setSlug}
          />
          <span className="sep" style={{ width: 1, height: 18, background: "var(--line)" }} />
          <Pill tone={yukari ? "up" : "down"}>{yukari ? "AL" : "SAT"}</Pill>
          <Pill>{spec.kunye.durum?.toLocaleUpperCase("tr")}</Pill>
          <span style={{ marginLeft: "auto" }} />
          {spec.kunye.verdikt ? (
            <Pill>tarihsel isabet · {spec.kunye.verdikt}</Pill>
          ) : null}
        </div>

        <div className="chartbody">
          <Grafik
            key={slug}
            spec={spec}
            yukseklik={470}
            hudEk={
              <>
                {/* Dar levhada uzun HUD metni üçüncü satıra sarıyordu
                    (K5 i9, 768 bulgusu); kısa tutuluyor. */}
                {spec.kunye.strateji_adi}
                {rr !== null ? (
                  <>
                    {" "}
                    <span className="dim">·</span>{" "}
                    {/* Sayı ve etiketi BÖLÜNMEZ: dar levhada ikisi ayrı
                        satıra düşüp sayı sahipsiz kalıyordu (K5 i10). */}
                    <span style={{ whiteSpace: "nowrap" }}>
                      ödül/risk <b>{rr.toFixed(2)} : 1</b>
                    </span>
                  </>
                ) : null}
              </>
            }
          />
        </div>

        <div className="statbox">
          {satirlar.map((s) => (
            <div className="r" key={s.ad}>
              <span>{s.ad}</span>
              <span
                style={
                  s.rol === "fib_618"
                    ? { color: "var(--accent)" }
                    : undefined
                }
              >
                {s.deger}
              </span>
            </div>
          ))}
          <div className="r">
            <span>Ödül / risk</span>
            <span>{rr === null ? "—" : `${rr.toFixed(2)} : 1`}</span>
          </div>
        </div>

        <div className="notes">
          {kayit.notlar.map((n) => (
            <div className="note" key={n.baslik}>
              <h5>{n.baslik}</h5>
              <p>{n.govde}</p>
            </div>
          ))}
        </div>

        <div className="verdict">
          <Pill tone="acc">K4 · İSTATİSTİK</Pill>
          <p>
            <b>Kenar kanıtlanmadı.</b> {kayit.verdikt.govde} Sinyal gösterilir, iddia edilmez —{" "}
            <b>
              ölçülmemiş bir stratejiyi &ldquo;çalışıyor&rdquo; diye sunmuyoruz, ölçülmüş olanın
              sonucunu da saklamıyoruz.
            </b>{" "}
            <span className="dim">Ölçüm dosyası: {kayit.verdikt.kanit}</span>
          </p>
        </div>
      </div>
    </section>
  );
}
