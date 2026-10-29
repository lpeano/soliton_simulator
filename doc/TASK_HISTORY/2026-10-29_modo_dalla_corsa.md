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
