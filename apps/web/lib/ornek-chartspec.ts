/**
 * Örnek ChartSpec — Python komposerinin ÜRETTİĞİ dosya.
 *
 *   packages/chart/uret.py  →  apps/web/ornek/thyao-swing-fib-abcd.chartspec.json
 *
 * Elle kurulmuş bir TypeScript nesnesi değil: sözleşme ancak dil sınırını
 * geçince sözleşmedir. Dosya değişirse `python packages/chart/uret.py` yeniden
 * koşulur; testler (packages/chart/tests) içeriği sabitler.
 *
 * Veri ÖRNEKTİR — `kunye.ornek_mi` bunu taşır ve arayüz kullanıcıya aynen
 * gösterir.
 */

import ham from "@/ornek/thyao-swing-fib-abcd.chartspec.json";
import { dogrula, type ChartSpec } from "./chartspec";

export const THYAO_SWING_FIB_ABCD: ChartSpec = dogrula(ham as unknown);
