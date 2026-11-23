# [M0528] IL LAPSE COME MOLTIPLICATORE (N DAL VINCOLO) -- LA LETTURA E LA TABELLA DEL GIUDIZIO *(i numeri da `lapse_vincolo.txt` e `lapse_vincolo_v2.txt`; le significativita' e i rapporti da un `python -c` del 2026-11-23, `11:14` da `date`)* [[PROGETTO-MITOSI]]

> **Le corse:** `20`, `08:51`-`10:53`, tutte uscita `0` *(il vuoto alla v2: la v1 cadde, `ae6e9b4f`)*. **La configurazione:** `lapse_vincolo.py` *(sha1 dei byte `30469d27`)*, `c2 = 0.25`, `kappa = 2.528944153922671e-4`, la media di `N u` tolta *(D1 a)*, `N = N_imp x N_ris` *(D3 i)*, il punto fisso a `1e-10`. ### **IL GRADIENTE DELLA CADUTA E DI EOTVOS RESTA IMPOSTO** *(D3)*: **la coppia a `d 36` e' il solo caso con la sorgente vera.** **La forma predefinita resta F0.**

## I CRITERI *(K1-K5)*

- **K1 il vuoto: PASSA** *(`N = 1` al bit su `500` tick per le tre righe)*.
- **K1 il mattone: FALLISCE** -- `max|N(2000) - N(1500)|` = V2 `1.716e-3`, V3 `9.737e-4`, V2V3 `2.688e-4` contro `1e-6`. ### **Il controllo di scala, fatto DOPO i numeri** *(la v2)*: **chi con la portata varia di `2.651e-4` allo stesso modo** *(agli anelli)*: V2V3 `1.00 x chi`, V3 `3.66 x`, V2 `6.39 x`. **La soglia `1e-6` non la passa nemmeno chi: il mattone respira** *(S11, S18)*, e `N` lo segue. **Il criterio era sbagliato in partenza** *(non l'ho scritto io, ma l'ho copiato senza controllarlo su chi: errore mio)*; **il fallimento resta scritto.**
- **K1 la norma: V3 FALLISCE** *(`1.16e-12` contro `1e-12`)*. **Dopo i numeri** *(la v2)*: **senza nessun vincolo** [M0908] V0 `1.16e-12`, V3 `1.12e-12`, [M1446] V3 `1.12e-12`; con `cs_N = True` *(V1, V2)* `1e-14`-`8e-14`. **E' del tick senza `cs_N`, non del vincolo.**
- **K1 `N(centro) < 1` con Z1 (V2V3): PASSA** *(`1 - N = +6.198e-3`)*.
- **K2: PASSA** *(il massimo `7` iterazioni nel mattone, ed e' quello del primo tick da freddo; `6` per V2V3)*.
- **K3:** V2 **VIA**, V3 **VERSO**, V2V3 **VIA** *(il segno di [M0908]: il segno della caduta non cambia, come detto in testa alla carta)*. **NATURA per V3, per il criterio scritto** *(VERSO e `omega(centro) < omega(bordo)` a `2.3 sigma`)*. ### ⚠ **Ma l'orologio va AL CONTRARIO di `N` in tutte e tre le righe:** V3 ha `N(centro) > 1` *(l'anti-lapse, `1 - N = -1.119e-2`)* e il centro batte **piu' piano**; V2 e V2V3 hanno `N(centro) < 1` e il centro batte **piu' veloce**. **Il «NATURA» di V3 combina una caduta nel gradiente IMPOSTO con un orologio che contraddice l'`N` RISOLTO:** con la sorgente vera, V3 *(VERSO `N` piu' basso)* cadrebbe **via** dal suo mattone, che ha `N > 1`. **Lo leggo come S6 che resta, non come natura.**
- **K4 Eotvos: `>= 12%` per tutte e tre** -- V2 `+0.120 -> -0.325` *(`|eta| x2.70`, `+3.8 sigma`)*; V3 `+0.138 -> -0.338` *(`x2.45`, `+2.8 sigma`)*; V2V3 `+0.131 -> +0.178` *(`x1.35`, `+2.1 sigma`)*. **Il segno di `eta` si inverte per V2 e V3** *(`-8.2` e `-6.8 sigma`)*: col vincolo **il corpo piu' pesante cade di piu'** *(V2: `|a|` `3.15e-6` a x0.8, `4.37e-6` a x1.2)*. **La lettura** *(mia, dopo i numeri)*: `N_ris` contiene il pozzo **del corpo stesso**, che cresce con la sua massa: **il vincolo aggiunge un'autointerazione che dipende dalla massa**, e questa rompe l'equivalenza.
- **K5 la coppia a `d 36` (la sorgente vera):** in fase `a -9.52e-8 +- 8.4e-9` contro F0 `-1.394e-6` *(`0.068 x`)*; in antifase `+1.200e-6` contro F0 `+2.57e-7` *(`4.67 x`)*. `A` `-6.48e-7` *(`0.784 x` F0)*, **`B` `+5.52e-7` contro F0 `-5.69e-7`** *(**la parte universale cambia segno: ora respinge**)*. **Contro chi** *(solo in fase, S15 riscalato `x 39/36`)*: `Delta a +1.299e-6` contro `+1.322e-6`, **`0.983`**.
- **Fuori dalla sagoma, il profilo** *(V2V3 contro chi, la stessa partenza)*: `1 - N` al centro `x1.089`, la larghezza a meta' `21.98` contro `20.61` *(`x1.066`)*: **piu' largo e piu' profondo**; lontano `1 - N < 0` *(`N > 1`, D1 a)* come chi.

## LE PREVISIONI, CONTRO I NUMERI

| | la previsione | l'esito |
|---|---|---|
| **P1** *(guardiano)* | K1 e K2 passano `75%` | **NO** *(K2 si'; K1 il mattone no, e la norma di V3 no)* |
| | il profilo piu' stretto di chi `60%` | **NO** *(piu' largo, `x1.066`)* |
| **P2** | V2 VIA `70%`; V3 VERSO `65%` | **SI', SI'** *(«natura solo con Z2»: non giudicabile, Z2 non si fa)* |
| **P3** | `eta < 1%` `35%`; `1-12%` `40%`; `>= 12%` `25%` | **`>= 12%`** *(la meno probabile)* |
| **P4** | A e B come F0 entro il `20%` `65%` | **NO** *(A `-21.6%`; B cambia segno)* |
| **P5** | TOPPA o NULLA `55%`; CURA `30%`; DANNO `15%` | **contro chi NULLA; contro F0 DANNO** *(sotto)* |
| **guardiano, con le decisioni** | `eta` cambia `< 20%` relativo `60%`; `< 1%` `10%`; sale `30%` | **NO** *(V2 `-370%`, V3 `-345%`; V2V3 `+35 +- 19%`, `0.8 sigma` sopra il `20%`)*; **`< 1%` NO**; **sale: in modulo si', in tutte e tre** |
| **mie** | il cambio relativo `< 20%` per tutte e tre `70%` | **NO** |
| | `eta` sale con V3 `55%` | **non giudicabile come l'ho scritta** *(non ho detto se in segno o in modulo)*: **in segno NO, in modulo SI'** |
| | il profilo PIU' LARGO di chi `75%` | **SI'** *(`x1.066`: poco)* |
| | V3 da solo `N(centro) > 1` `90%` | **SI'** |
| | il rilassamento semplice non passerebbe K2 `90%` | **NON MISURATO** |

## LA TABELLA DEL GIUDIZIO *(`doc/SAGOMA.md` sez. 4)*

| riga | F0 senza lapse risolto *(il gradiente imposto, [M0908], [M1446]; la coppia [M0326-K])* | chi | il lapse risolto | contro chi | contro F0 |
|---|---|---|---|---|---|
| S1 | gap sopra, m* `-16.1` | -- | non misurato | NON MISURATO | NON MISURATO |
| S2 | R_E `1.19` | -- | non misurato | NON MISURATO | NON MISURATO |
| S3 | `a = -grad omega / m*` | -- | non misurato *(solo il segno e `a`)* | NON MISURATO | NON MISURATO |
| **S4** | `eta` V2 `0.120`, V3 `0.138`, V2V3 `0.131` | **non misurato con chi** | **V2 `-0.325`, V3 `-0.338`, V2V3 `+0.178`** | NON MISURATO | **PEGGIORA** *(`|eta|` `x2.70` a `3.8 sigma`, `x2.45` a `2.8`, `x1.35` a `2.1`)* |
| **S5** | A `-8.25e-7`, B `-5.69e-7`, `abs(A/B) 1.45`; in fase `-1.39e-6` | in fase `Delta a +1.32e-6` *(S15 riscalato)* | A `-6.48e-7`, **B `+5.52e-7`**; in fase `-9.5e-8` | **LASCIA** *(`0.983` in fase; l'antifase di chi non esiste)* | **PEGGIORA** *(la coppia in fase quasi non si avvicina, `0.068 x`; la parte universale B respinge)* |
| S6 | V2 VIA, V3 VERSO; l'orologio opposto | come [M0908] | V2 VIA, V3 VERSO, V2V3 VIA; **l'orologio opposto a `N` in tutte e tre** | NON MISURATO *(l'orologio di chi nel mattone non e' in queste corse)* | **LASCIA** *(la caduta e l'orologio ancora non vanno insieme)* |
| S7-S10 | | | non misurato | NON MISURATO | NON MISURATO |
| S11 | il mattone respira | `N` agli anelli varia `2.65e-4` *(k 1500-2000)* | V2V3 `2.65e-4`, V3 `9.7e-4`, V2 `1.69e-3` | NON MISURATO *(`w` non misurato; `N` segue il respiro: V2V3 come chi)* | NON MISURATO |
| S12-S14 | | | non misurato | NON MISURATO | NON MISURATO |
| **S15** | -- *(senza lapse non c'e' gravita')* | respinge, `+1.22e-6` a `d 39` | respinge, `+1.30e-6` a `d 36` | **LASCIA** *(`0.983`)* | -- *(vedi S5)* |
| S16 | I1 `-16.1`, `m_E -16.61` | -- | non misurato | NON MISURATO | NON MISURATO |
| S17 | FH | -- | non misurato | NON MISURATO | NON MISURATO |
| S18 | il respiro e' del mattone | -- | non misurato *(solo `N`, sopra in S11)* | NON MISURATO | NON MISURATO |

### **IL VERDETTO (K6):**
- **CONTRO CHI: NULLA** *(le righe misurate S5 e S15 LASCIANO: la coppia con la sorgente vera ridà chi al `1.7%`)*. **La risposta alla domanda della carta** *(«un `N` autoconsistente cambia Eotvos?»)*: **contro chi non si sa** *(Eotvos con chi non e' misurato)*; **contro il gradiente imposto si', e in peggio.**
- **CONTRO F0 SENZA LAPSE RISOLTO: DANNO** *(S4 e S5 PEGGIORANO, nessuna riga MIGLIORA)*.
- **Le righe NON MISURATE:** S1-S3, S6 contro chi, S7-S14, S16-S18. **Il criterio K1 della stazionarieta' era fuori scala** *(chi stesso varia `2.65e-4`)*: lo dico, e il fallimento resta.
- ### **Il vincolo non entra nel nucleo. La forma predefinita resta F0. Ogni decisione e' di Luca.**
