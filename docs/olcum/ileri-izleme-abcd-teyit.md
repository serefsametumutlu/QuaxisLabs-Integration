# İleriye dönük izleme — `abcd·teyit`

**Koşu tarihi:** 2026-09-14 · **Kuralın donduğu an:** 2026-09-14

Kural `docs/olcum/onkayit-harmonik-teyit.md`'de donduruldu ve `e5556aa` ile commit edildi. Bu rapor **yalnızca o tarihten sonra doğan** sinyalleri sayar.

> Geçmişte arama yapmak bitti. Bir kuralın çalıştığını gösteren tek
> meşru yol, kural donduktan SONRA gelen veride ölçmektir — o veriye
> bakarak kimse hiçbir seçim yapmadı.

| | |
|---|---|
| Evren | 507 BIST sembolü, 1G |
| Veri son barı | 2026-09-11 |
| Dondurmadan sonraki sinyal | **0** |
| Bağımsız gözlem | **0** sembol |
| Verdikt için gereken | 30 sembol (Pardo s.295) |

## Durum: **VERDİKT YOK**

Birikmiş gözlem 0 sembol, eşik 30. Sayı yazılır, verdikt yazılmaz.

Bu bir arıza değil, tasarım: kural bugün donduruldu ve veri henüz o tarihten sonrasını içermiyor. Eşik dolana kadar bu rapor boş kalacak ve **boş kalması doğru davranıştır.**

