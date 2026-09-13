# Harmonik (Pesavento) — K4 İstatistik · 1D

**Tarih:** 2026-09-13 · **Evren:** 507 BIST sembolü · **Yön:** long

Ölçüt: **üç bariyerli R** (stop / hedef / zaman). Stop ve hedef stratejinin kendi kuralından geliyor. İşlem maliyeti dahil (taraf başına %0.050 komisyon + %0.050 kayma). **Aynı barda stop ve hedef birlikte vurulduysa STOP sayılır.**

Bağımsız gözlem **sembol**, bar değil. Adil baz: aynı risk yapısıyla rastgele bar/sembol. Aile beş üyeli ve **önceden sabitlendi** — BH-FDR (q=0.05) beşine birden uygulandı.

## Tüm dönem — BİRİNCİL

| künye | işlem | sembol | isabet | beklenen R | adil baz | fark | PF | p |
|---|---|---|---|---|---|---|---|---|
| `abcd·kor` | 2413 | 451 | %32.8 | **+0.148R** | +0.323R | -0.176R | 1.22 | 1.0000 |
| `abcd·teyit` | 803 | 362 | %45.3 | **+0.707R** | +0.349R | +0.359R | 2.35 | 0.0685 |
| `gartley·kor` | 108 | 92 | %35.2 | **+0.053R** | +0.240R | -0.187R | 1.08 | 0.8941 |
| `gartley·teyit` | 36 | 36 | %41.7 | **-0.108R** | +0.171R | -0.278R | 0.82 | 0.8926 |
| `kelebek·kor` | 138 | 113 | %30.4 | **-0.195R** | +0.228R | -0.423R | 0.71 | 1.0000 |
| `kelebek·teyit` | 44 | 43 | %45.5 | **+0.174R** | +0.183R | -0.009R | 1.39 | 0.4633 |
| `uc_surus·kor` | 142 | 117 | %24.6 | **-0.256R** | +0.150R | -0.407R | 0.68 | 0.9990 |
| `uc_surus·teyit` | 37 | 35 | %51.4 | **+0.173R** | +0.105R | +0.069R | 1.42 | 0.2499 |

## OOS — ikincil

| künye | işlem | sembol | isabet | beklenen R | adil baz | fark | PF | p |
|---|---|---|---|---|---|---|---|---|
| `abcd·kor` | 622 | 325 | %40.8 | **+0.425R** | +0.367R | +0.059R | 1.73 | 0.7561 |
| `abcd·teyit` | 301 | 207 | %50.2 | **+0.345R** | +0.350R | -0.005R | 1.76 | 0.3953 |
| `gartley·kor` | 29 | 27 | %37.9 | **+0.105R** | +0.318R | -0.212R | 1.17 | 0.6847 |
| `gartley·teyit` | 16 | 16 | %56.2 | **+0.374R** | +0.223R | +0.151R | 1.83 | 0.3128 |
| `kelebek·kor` | 21 | 21 | %33.3 | **-0.112R** | +0.348R | -0.461R | 0.81 | 0.9240 |
| `kelebek·teyit` | 7 | 7 | %57.1 | **+0.437R** | +0.319R | +0.118R | 2.00 | 0.3828 |
| `uc_surus·kor` | 46 | 43 | %26.1 | **-0.197R** | +0.192R | -0.389R | 0.75 | 0.9180 |
| `uc_surus·teyit` | 17 | 16 | %47.1 | **+0.008R** | +0.198R | -0.190R | 1.02 | 0.5747 |

## IS — ikincil

| künye | işlem | sembol | isabet | beklenen R | adil baz | fark | PF | p |
|---|---|---|---|---|---|---|---|---|
| `abcd·kor` | 1791 | 425 | %30.0 | **+0.051R** | +0.297R | -0.246R | 1.07 | 1.0000 |
| `abcd·teyit` | 502 | 298 | %42.4 | **+0.925R** | +0.342R | +0.582R | 2.63 | 0.0780 |
| `gartley·kor` | 79 | 68 | %34.2 | **+0.034R** | +0.214R | -0.180R | 1.05 | 0.9185 |
| `gartley·teyit` | 20 | 20 | %30.0 | **-0.493R** | +0.138R | -0.631R | 0.31 | 0.9975 |
| `kelebek·kor` | 117 | 98 | %29.9 | **-0.210R** | +0.162R | -0.373R | 0.70 | 0.9985 |
| `kelebek·teyit` | 37 | 36 | %43.2 | **+0.124R** | +0.120R | +0.004R | 1.27 | 0.4368 |
| `uc_surus·kor` | 96 | 85 | %24.0 | **-0.285R** | +0.124R | -0.409R | 0.64 | 0.9925 |
| `uc_surus·teyit` | 20 | 20 | %55.0 | **+0.314R** | +0.121R | +0.193R | 1.82 | 0.2534 |

## BH-FDR (q = 0.05) — tüm dönem, 8 test

| künye | p | FDR eşiğini geçti mi |
|---|---|---|
| `abcd·teyit` | 0.0685 | ✘ |
| `uc_surus·teyit` | 0.2499 | ✘ |
| `kelebek·teyit` | 0.4633 | ✘ |
| `gartley·teyit` | 0.8926 | ✘ |
| `gartley·kor` | 0.8941 | ✘ |
| `uc_surus·kor` | 0.9990 | ✘ |
| `abcd·kor` | 1.0000 | ✘ |
| `kelebek·kor` | 1.0000 | ✘ |

## Teyit katkı yaptı mı (ön kayıt §6, madde 4)

Teyitli varyantın körlemesineden **daha iyi** olması gerekiyor; yoksa teyit 'işe yaradı' denemez.

| formasyon | körlemesine fark | teyitli fark | teyidin katkısı |
|---|---|---|---|
| `abcd` | -0.176R | +0.359R | **+0.534R** |
| `gartley` | -0.187R | -0.278R | **-0.091R** |
| `kelebek` | -0.423R | -0.009R | **+0.414R** |
| `uc_surus` | -0.407R | +0.069R | **+0.475R** |

## Çıkış kırılımı

| formasyon | hedef | stop | zaman | ort. kazanç | ort. kayıp |
|---|---|---|---|---|---|
| `abcd·kor` | %23 | %65 | %13 | +2.52R | -1.01R |
| `abcd·teyit` | %35 | %47 | %18 | +2.72R | -0.96R |
| `gartley·kor` | %31 | %64 | %6 | +2.05R | -1.03R |
| `gartley·teyit` | %36 | %58 | %6 | +1.18R | -1.03R |
| `kelebek·kor` | %18 | %65 | %17 | +1.61R | -0.98R |
| `kelebek·teyit` | %36 | %41 | %23 | +1.37R | -0.82R |
| `uc_surus·kor` | %24 | %75 | %1 | +2.17R | -1.05R |
| `uc_surus·teyit` | %59 | %38 | %3 | +1.14R | -0.85R |

## Örneklem yeterli mi

Pardo s.295: 30–50 işlem asgari kabul edilir. **Sembol sayısı 30'un altındaki satırın sayısı yazılır, verdikti yazılmaz.**

| künye | sembol | yeterli mi |
|---|---|---|
| `abcd·kor` | 451 | ✔ |
| `abcd·teyit` | 362 | ✔ |
| `gartley·kor` | 92 | ✔ |
| `gartley·teyit` | 36 | ✔ |
| `kelebek·kor` | 113 | ✔ |
| `kelebek·teyit` | 43 | ✔ |
| `uc_surus·kor` | 117 | ✔ |
| `uc_surus·teyit` | 35 | ✔ |

