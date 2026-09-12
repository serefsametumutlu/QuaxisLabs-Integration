"""DataTable kabul ölçümü — 500 satır.

Dört şeyi ölçer ve raporlar:
  1. Sanallaştırma  — 500 satırın kaçı gerçekten DOM'da?
  2. Kaydırma kare süresi — sayfanın kendi rAF ölçümü (fps / ortalama / en kötü)
  3. Sıralama — kolon başlığı üç durumlu mu, sıra gerçekten değişiyor mu?
  4. Klavye — ok tuşlarıyla odak satır satır ilerliyor mu, pencere dışına
     çıkınca liste kendini kaydırıyor mu?

Önce: cd apps/web && npm run build:vitrin
Sonra: python tools/tablo_olcum.py
"""

from __future__ import annotations

import functools
import http.server
import json
import pathlib
import socketserver
import sys
import threading

from playwright.sync_api import sync_playwright

KOK = pathlib.Path(__file__).resolve().parents[1]

#: Odaklı satırın sırasını döndüren tarayıcı ifadesi.
ODAK_SIRASI = "document.activeElement?.getAttribute('data-index')"
KAYNAK = KOK / "apps" / "web" / "out"


class Sessiz(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def sunucu_ac(dizin: pathlib.Path):
    islem = functools.partial(Sessiz, directory=str(dizin))
    httpd = socketserver.TCPServer(("127.0.0.1", 0), islem)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


def main() -> int:
    if not (KAYNAK / "tasarim.html").exists():
        print("HATA: önce `cd apps/web && npm run build:vitrin`", file=sys.stderr)
        return 2

    httpd, port = sunucu_ac(KAYNAK)
    rapor: dict[str, object] = {}
    try:
        with sync_playwright() as p:
            tarayici = p.chromium.launch()
            ctx = tarayici.new_context(viewport={"width": 1440, "height": 900}, locale="tr-TR")
            sayfa = ctx.new_page()
            sayfa.goto(f"http://127.0.0.1:{port}/tasarim.html?tema=dark", wait_until="networkidle")

            tablo = sayfa.locator("#tasarim-tablo .dt")
            tablo.scroll_into_view_if_needed()
            sayfa.wait_for_timeout(200)

            # 1 — sanallaştırma
            rapor["toplam_satir"] = int(tablo.locator("table").get_attribute("aria-rowcount") or 0)
            rapor["dom_satir"] = tablo.locator("tbody tr:not(.pad)").count()
            rapor["dolgu_satir"] = tablo.locator("tbody tr.pad").count()

            # 2a — taban çizgisi: hiçbir şey yapmadan rAF kare süresi.
            # Başsız tarayıcı yazılımla boyadığı için 60 fps'i kendiliğinden
            # vermez; tablonun sayısı bu tabana göre okunmalı.
            rapor["taban_bos"] = sayfa.evaluate(
                """() => new Promise(ok => {
                  const k = []; let t0 = performance.now(), bas = t0;
                  const adim = t => { k.push(t - t0); t0 = t;
                    if (t - bas > 1500) { const g = k.slice(1);
                      ok({ fps: Math.round(1000 / (g.reduce((a,b)=>a+b,0)/g.length)),
                           ortalama: +(g.reduce((a,b)=>a+b,0)/g.length).toFixed(2) }); }
                    else requestAnimationFrame(adim); };
                  requestAnimationFrame(adim);
                })"""
            )

            # 2b — kaydırma kare süresi (sayfanın kendi ölçümü)
            sayfa.get_by_role("button", name="2 sn kaydır ve ölç").click()
            sayfa.wait_for_timeout(2600)
            olcum = tablo.locator("xpath=../div[@class='olcum']").inner_text()
            rapor["olcum_satiri"] = olcum.replace("\n", " ")
            rapor["kaydirmada_dom_satir"] = tablo.locator("tbody tr:not(.pad)").count()

            # 3 — sıralama: fiyat kolonu artan → azalan → sırasız
            def fiyatlar() -> list[float]:
                ham = tablo.locator("tbody tr:not(.pad) td:nth-child(7)").all_inner_texts()
                return [float(h.replace(" ", "")) for h in ham if h.strip()]

            baslik = tablo.locator("thead th").nth(6)
            dugme = baslik.locator("button.sorter")
            dugme.click()
            sayfa.wait_for_timeout(120)
            artan = fiyatlar()
            rapor["siralama_artan"] = artan == sorted(artan)
            rapor["siralama_aria_1"] = baslik.get_attribute("aria-sort")
            dugme.click()
            sayfa.wait_for_timeout(120)
            azalan = fiyatlar()
            rapor["siralama_azalan"] = azalan == sorted(azalan, reverse=True)
            rapor["siralama_aria_2"] = baslik.get_attribute("aria-sort")
            dugme.click()
            sayfa.wait_for_timeout(120)
            rapor["siralama_aria_3"] = baslik.get_attribute("aria-sort")

            # 4 — klavye: ilk satıra odaklan, 40 kez aşağı
            ilk = tablo.locator("tbody tr:not(.pad)").first
            ilk.focus()
            for _ in range(40):
                sayfa.keyboard.press("ArrowDown")
            rapor["klavye_40_asagi_index"] = sayfa.evaluate(
                "document.activeElement?.getAttribute('data-index')"
            )
            sayfa.keyboard.press("End")
            sayfa.wait_for_timeout(120)
            rapor["klavye_end_index"] = sayfa.evaluate(ODAK_SIRASI)
            rapor["klavye_end_gorunur"] = sayfa.evaluate(
                """() => {
                  const tr = document.activeElement;
                  const kutu = tr?.closest('.dtscroll');
                  if (!tr || !kutu) return false;
                  const a = tr.getBoundingClientRect(), b = kutu.getBoundingClientRect();
                  return a.top >= b.top - 1 && a.bottom <= b.bottom + 1;
                }"""
            )
            sayfa.keyboard.press("Home")
            sayfa.wait_for_timeout(120)
            rapor["klavye_home_index"] = sayfa.evaluate(ODAK_SIRASI)

            ctx.close()
            tarayici.close()
    finally:
        httpd.shutdown()
        httpd.server_close()

    print(json.dumps(rapor, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
