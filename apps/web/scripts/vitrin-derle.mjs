/**
 * Görsel kabul döngüsü için statik dışa aktarım.
 *
 * `next build`'i QUAXIS_EXPORT=1 ile koşturur; next.config.ts bunu görünce
 * `output: "export"` açar ve `out/` üretir. tools/ekran_goruntusu.py o klasörü
 * kendi içinde servis edip ekran görüntülerini alır — ayrıca bir geliştirme
 * sunucusu açmaya gerek kalmaz.
 */
import { spawn } from "node:child_process";

const cocuk = spawn("npx", ["next", "build"], {
  stdio: "inherit",
  shell: process.platform === "win32",
  env: { ...process.env, QUAXIS_EXPORT: "1" },
});

cocuk.on("exit", (kod) => process.exit(kod ?? 1));
