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
import hamGz from "@/ornek/thyao-golden-zone.chartspec.json";
import { dogrula, type ChartSpec } from "./chartspec";

export const THYAO_SWING_FIB_ABCD: ChartSpec = dogrula(ham as unknown);

/**
 * Golden Zone (ICT OTE) — **gerçek** veriden üretilmiş spec.
 *
 *   tools/golden_zone_spec.py  →  apps/web/ornek/thyao-golden-zone.chartspec.json
 *
 * `kunye.ornek_mi` FALSE: bu gerçek bir THYAO kurulumu, uydurulmuş bir
 * fikstür değil. `kunye.verdikt` K4'ün çıktısını taşır ve arayüz onu
 * kullanıcıya AYNEN gösterir — "kurulum oluştu" ile "kenar kanıtlandı"
 * birbirine karışmasın.
 */
export const THYAO_GOLDEN_ZONE: ChartSpec = dogrula(hamGz as unknown);

/* ------------------------------------------------------------------ harmonik
 *
 * Dört Pesavento formasyonu, **gerçek** BIST verisinden üretilmiş specler:
 *
 *   tools/harmonik_spec.py --formasyon <ad> --en-iyi
 *
 * Örnekleri seçen ölçüt GETİRİ DEĞİL, okunaklılıktır (bkz. o aracın
 * `_okunaklilik` fonksiyonu). Sonuç kendiliğinden karışık çıktı — biri
 * hedefe ulaştı, ikisi stop oldu, biri süre doldu. Kârlı örnek seçmek,
 * verdikti gizlemenin görsel hâli olurdu.
 *
 * **Örnekler 2014 SONRASINDAN seçiliyor** ve bunun sebebi ölçülmüş bir
 * veri kusuru: kaynak, BIST için 2014 öncesinde gerçek açılış fiyatı
 * vermiyor, `open` alanını `close` ile dolduruyor. Three Drives örneği
 * önce BURVA 2011'den seçilmişti ve 106 barın **106'sı** gövdesiz
 * çıkıyordu — levha mum grafiği gibi görünmüyordu. Yeni örnekte
 * (EMKEL 2026) bu oran %5.
 */
import hamAbcd from "@/ornek/rtalb-abcd.chartspec.json";
import hamGartley from "@/ornek/dogub-gartley.chartspec.json";
import hamKelebek from "@/ornek/srvgy-kelebek.chartspec.json";
import hamUcSurus from "@/ornek/emkel-uc_surus.chartspec.json";

export const HARMONIK_ABCD: ChartSpec = dogrula(hamAbcd as unknown);
export const HARMONIK_GARTLEY: ChartSpec = dogrula(hamGartley as unknown);
export const HARMONIK_KELEBEK: ChartSpec = dogrula(hamKelebek as unknown);
export const HARMONIK_UC_SURUS: ChartSpec = dogrula(hamUcSurus as unknown);
