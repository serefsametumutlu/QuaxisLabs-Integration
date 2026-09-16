# Harmonik (Pesavento) — K4 İstatistik · 1D

**Tarih:** 2026-09-14 · **Evren:** 588 BIST sembolü · **Yön:** long

Ölçüt: **üç bariyerli R** (stop / hedef / zaman). Stop ve hedef stratejinin kendi kuralından geliyor. İşlem maliyeti dahil (taraf başına %0.050 komisyon + %0.050 kayma). **Aynı barda stop ve hedef birlikte vurulduysa STOP sayılır.**

Bağımsız gözlem **sembol**, bar değil. Adil baz: aynı risk yapısıyla rastgele bar/sembol. Aile beş üyeli ve **önceden sabitlendi** — BH-FDR (q=0.05) beşine birden uygulandı.

## Tüm dönem — BİRİNCİL

| künye | işlem | sembol | isabet | beklenen R | adil baz | fark | PF | p |
|---|---|---|---|---|---|---|---|---|
| `abcd·kor` | 2882 | 525 | %32.8 | **+0.152R** | +0.320R | -0.168R | 1.22 | 1.0000 |
| `abcd·teyit` | 921 | 424 | %46.1 | **+0.612R** | +0.346R | +0.266R | 2.20 | 0.0445 |
| `gartley·kor` | 130 | 111 | %36.9 | **+0.115R** | +0.221R | -0.106R | 1.18 | 0.7726 |
| `gartley·teyit` | 43 | 42 | %41.9 | **-0.104R** | +0.190R | -0.294R | 0.82 | 0.9070 |
| `kelebek·kor` | 163 | 132 | %30.7 | **-0.171R** | +0.212R | -0.383R | 0.75 | 1.0000 |
| `kelebek·teyit` | 47 | 46 | %46.8 | **+0.154R** | +0.171R | -0.017R | 1.35 | 0.5012 |
| `uc_surus·kor` | 175 | 145 | %24.6 | **-0.256R** | +0.158R | -0.414R | 0.68 | 1.0000 |
| `uc_surus·teyit` | 52 | 49 | %46.2 | **+0.099R** | +0.121R | -0.022R | 1.21 | 0.4693 |

## OOS — ikincil

| künye | işlem | sembol | isabet | beklenen R | adil baz | fark | PF | p |
|---|---|---|---|---|---|---|---|---|
| `abcd·kor` | 728 | 382 | %41.3 | **+0.444R** | +0.380R | +0.063R | 1.77 | 0.5577 |
| `abcd·teyit` | 356 | 247 | %51.1 | **+0.347R** | +0.349R | -0.002R | 1.77 | 0.3553 |
| `gartley·kor` | 34 | 32 | %38.2 | **+0.115R** | +0.304R | -0.189R | 1.19 | 0.6952 |
| `gartley·teyit` | 20 | 20 | %55.0 | **+0.356R** | +0.271R | +0.085R | 1.85 | 0.3728 |
| `kelebek·kor` | 23 | 23 | %34.8 | **-0.049R** | +0.376R | -0.425R | 0.92 | 0.9075 |
| `kelebek·teyit` | 7 | 7 | %57.1 | **+0.437R** | +0.315R | +0.122R | 2.00 | 0.3783 |
| `uc_surus·kor` | 57 | 53 | %28.1 | **-0.131R** | +0.206R | -0.337R | 0.83 | 0.9140 |
| `uc_surus·teyit` | 25 | 24 | %44.0 | **-0.001R** | +0.212R | -0.213R | 1.00 | 0.6507 |

## IS — ikincil

| künye | işlem | sembol | isabet | beklenen R | adil baz | fark | PF | p |
|---|---|---|---|---|---|---|---|---|
| `abcd·kor` | 2154 | 494 | %29.9 | **+0.053R** | +0.288R | -0.234R | 1.07 | 1.0000 |
| `abcd·teyit` | 565 | 344 | %43.0 | **+0.779R** | +0.361R | +0.417R | 2.42 | 0.0840 |
| `gartley·kor` | 96 | 84 | %36.5 | **+0.115R** | +0.201R | -0.085R | 1.18 | 0.7931 |
| `gartley·teyit` | 23 | 22 | %30.4 | **-0.503R** | +0.131R | -0.634R | 0.30 | 0.9960 |
| `kelebek·kor` | 140 | 116 | %30.0 | **-0.191R** | +0.145R | -0.336R | 0.73 | 0.9975 |
| `kelebek·teyit` | 40 | 39 | %45.0 | **+0.104R** | +0.118R | -0.013R | 1.24 | 0.4828 |
| `uc_surus·kor` | 118 | 106 | %22.9 | **-0.317R** | +0.128R | -0.445R | 0.61 | 0.9990 |
| `uc_surus·teyit` | 27 | 27 | %48.1 | **+0.192R** | +0.126R | +0.066R | 1.43 | 0.3758 |

## BH-FDR (q = 0.05) — tüm dönem, 8 test

| künye | p | FDR eşiğini geçti mi |
|---|---|---|
| `abcd·teyit` | 0.0445 | ✘ |
| `uc_surus·teyit` | 0.4693 | ✘ |
| `kelebek·teyit` | 0.5012 | ✘ |
| `gartley·kor` | 0.7726 | ✘ |
| `gartley·teyit` | 0.9070 | ✘ |
| `abcd·kor` | 1.0000 | ✘ |
| `kelebek·kor` | 1.0000 | ✘ |
| `uc_surus·kor` | 1.0000 | ✘ |

## Teyit katkı yaptı mı (ön kayıt §6, madde 4)

Teyitli varyantın körlemesineden **daha iyi** olması gerekiyor; yoksa teyit 'işe yaradı' denemez.

| formasyon | körlemesine fark | teyitli fark | teyidin katkısı |
|---|---|---|---|
| `abcd` | -0.168R | +0.266R | **+0.434R** |
| `gartley` | -0.106R | -0.294R | **-0.188R** |
| `kelebek` | -0.383R | -0.017R | **+0.366R** |
| `uc_surus` | -0.414R | -0.022R | **+0.392R** |

## Çıkış kırılımı

| formasyon | hedef | stop | zaman | ort. kazanç | ort. kayıp |
|---|---|---|---|---|---|
| `abcd·kor` | %23 | %65 | %12 | +2.54R | -1.01R |
| `abcd·teyit` | %37 | %45 | %18 | +2.43R | -0.95R |
| `gartley·kor` | %32 | %62 | %6 | +2.06R | -1.02R |
| `gartley·teyit` | %35 | %56 | %9 | +1.14R | -1.00R |
| `kelebek·kor` | %20 | %64 | %16 | +1.67R | -0.99R |
| `kelebek·teyit` | %40 | %38 | %21 | +1.26R | -0.82R |
| `uc_surus·kor` | %24 | %75 | %1 | +2.18R | -1.05R |
| `uc_surus·teyit` | %56 | %42 | %2 | +1.22R | -0.86R |

## Örneklem yeterli mi

Pardo s.295: 30–50 işlem asgari kabul edilir. **Sembol sayısı 30'un altındaki satırın sayısı yazılır, verdikti yazılmaz.**

| künye | sembol | yeterli mi |
|---|---|---|
| `abcd·kor` | 525 | ✔ |
| `abcd·teyit` | 424 | ✔ |
| `gartley·kor` | 111 | ✔ |
| `gartley·teyit` | 42 | ✔ |
| `kelebek·kor` | 132 | ✔ |
| `kelebek·teyit` | 46 | ✔ |
| `uc_surus·kor` | 145 | ✔ |
| `uc_surus·teyit` | 49 | ✔ |

