# 2026-10-29 — IL MODO INSTABILE LETTO DALLA CORSA *([[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il mandato di Luca delle `09:21`, dopo `239def8d`)*

> **LIVELLO:** `600` tick dallo stato fermo di `L 81` *(al bit con `26300537`)*, lo scostamento `D(t)`, la sua forma, una conferma con Arnoldi; nessun file del nucleo.

## 1. LE PREMESSE DAL CODICE

| che cosa | dove | il fatto |
|---|---|---|
| lo stato fermo, il tick, `G` | `csv/_modo_instabile.py` `Mappa` | `G = e^{i mu s} T`; `mu -0.532745112`; il residuo `9.808e-10` |
| la forma | `csv/_modo_instabile.py` `armoniche`, `per_nodo`; `csv/_dove_va_la_materia.py` `pesi`, `GRUPPI` | le armoniche attorno al baricentro dello stato fermo, per anelli larghi `1` |
| la corsa salvata | `doc/referti_l2/stato_fermo/corsa_L81_00000.jsonl` | un punto ogni `10` tick fino a `2000` |
| **l'errore `n.79` del guardiano** | il mandato delle `08:24` | il tasso `~0.2` era letto sulla LARGHEZZA, che per un modo non radiale cambia col QUADRATO di `D` |

## 2. I CRITERI

- **La corsa:** `600` tick col tick di `Mappa`; ogni `10` tick il punto = quello di `26300537` al bit; `D(t) = e^{i mu s t} psi(t) - psi0` salvato ogni `10` tick fra `200` e `600`.
- **Il tasso:** `ln(|D|/|psi0|)` contro `t`; **la finestra:** dal primo `t` con `|D|/|psi0| > 1e3 r` *(`r` il residuo dello stato fermo: sopra il rumore)* all'ultimo con `|D|/|psi0| < 1e-2` *(prima della saturazione)*; la pendenza per minimi quadrati, per tick e per unita' di tempo; e le pendenze locali su `20` tick, stampate.
- **La rotazione:** il coseno reale `Re<D(t), D(t+10)> / (|D(t)| |D(t+10)|)` e il modulo complesso `|<D(t), D(t+10)>| / (...)`; il periodo dai cambi di segno di `Re<D(t), D(450)>` nella finestra *(il doppio della distanza media fra due cambi)*.
- **La forma** a `400`, `450`, `500` *(normalizzata)*: le armoniche `m = 0 .. 12` di `drho = 2 Re(conj(psi0) D)` e della fase `2 Im(...)`; il profilo radiale di `|D|^2`; le bande `A`, `B`, `P0`, `Ppi`.
- **La conferma** *(NON un sigillo)*: Arnoldi su `G^10`, `k = 2`, `ncv = 20`, `tol = 1e-6`, al piu' `20` riavvii, partenza `D(450)` normalizzato; gli autovalori, `ln|lambda| / (10 s)`, la sovrapposizione del sottospazio reale dell'autovettore con `D(450)`.
- **Il punto `5`** *(`N(mu)`)*: solo se il modo e' `m = 0`; uno script a parte.

## 3. LE LETTURE *(di Luca, delle `08:24`, scritte prima)*

- `(a)` `m = 0` in `A`; `(b)` `m >= 1` in `A` *(quale)*; `(c)` peso in `B` o nelle piatte; `(d)` altro *(per esempio un modo di sola fase)*, descritto.

## 4. LE MOTIVAZIONI

- Lo scostamento della corsa, nel regime lineare, e' gia' dominato dal modo che cresce piu' in fretta: non servono numeri nuovi da scegliere.

## 5. TODO

1. questo file, da solo;
2. `csv/_modo_dalla_corsa.py`, commit; il referto; RELAZIONE; MAPPA *(la riga `d`; l'errore `n.79` nella sezione `8`)*; commit.

## 6. ANNOTAZIONE DOPO IL REFERTO *(`doc/referti_l2/modo_dalla_corsa.txt`; lo script `sha1-BYTE e06acad5`, `c780080c`; `2/2`)*

- **Un errore mio:** questo file NON e' stato committato da solo prima dello script: il suo commit e' stato rifiutato perche' ho fatto `git add` e un altro commit mentre i suoi hook giravano; e' entrato nel commit dello script, `c780080c`. Il rito del par. `8` non e' rispettato; lo script resta committato prima di girarlo.

| | `t 400` | `t 450` | `t 500` *(fuori dalla finestra lineare)* |
|---|---|---|---|
| `|D|/|psi0|` | `8.18e-04` | `5.89e-03` | `1.41e-02` |
| `|D|^2` negli anelli `r 12` e `r 13` | `0.3717` + `0.5254` | `0.3592` + `0.5256` | `0.3818` + `0.4028` |
| le bande `P0` / `Ppi` / `A` / `B` | `0.484` / `0.411` / `0.099` / `0.005` | `0.483` / `0.387` / `0.124` / `0.006` | `0.403` / `0.287` / `0.293` / `0.017` |
| le armoniche di `drho`, le tre maggiori | `m8 0.200`, `m12 0.183`, `m11 0.154` | `m4 0.161`, `m8 0.155`, `m12 0.134` | `m0 0.374`, `m4 0.265`, `m6 0.084` |
| `m0` di `drho` | `0.041` | `0.117` | `0.374` |

- **Il tasso:** nella finestra dichiarata *(`t 250`-`470`)* `0.04161` per tick, `0.13870` per unita' di tempo; le pendenze locali `0.042`-`0.044` per tick fra `t 260` e `410`.
- **La rotazione:** fra due istanti a `10` tick la sovrapposizione `|<D, D'>|` e' `0.04`-`0.15`; la proiezione su `D(450)` cambia segno con periodo `36.4` tick *(`10.91` unita' di tempo)*.
- **Arnoldi** *(la conferma, `k 2`, `ncv 20`, `tol 1e-6`, `20` riavvii, partenza `D(450)`)*: **NON converge**, `0` autovalori, `7620` tick.

| lettura *(08:24)* | esito |
|---|---|
| (a) `m = 0` in `A` | **no:** `m0` di `drho` `0.04`-`0.12` nella finestra lineare; il peso in `A` `0.10`-`0.12` |
| (b) `m >= 1` in `A` | **no:** il peso in `A` e' piccolo |
| (c) peso in `B` o nelle piatte | **si', nelle piatte:** `P0` + `Ppi` `0.87`-`0.90`; `B` `0.006` |
| (d) altro | **un modo che oscilla** *(periodo `~36` tick, come il respiro)*, **sul bordo dello stato fermo** *(gli anelli `12`-`13`)*, **con armoniche angolari alte** *(`m 4`, `8`, `11`, `12`)* |

- **Il punto `5`** *(`N(mu)`)* non si esegue: il modo non e' `m = 0`.
