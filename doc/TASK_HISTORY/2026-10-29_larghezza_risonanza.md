# 2026-10-29 — LA LARGHEZZA DELLA RISONANZA *(UNA DIAGNOSI, NON UNA CURA; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il mandato di Luca delle `14:51`, dopo `de411167`)*

> **LIVELLO:** uno strumento di diagnosi in `csv/`, mai nel nucleo; `17` corse brevi dallo stato fermo a `s 0.15`.

## 1. LE PREMESSE DAL CODICE

| che cosa | dove | il fatto |
|---|---|---|
| le piatte | `csv/_dove_va_la_materia.py` `autovettori`, `GRUPPI` | ordinate per `ph = -arg(lambda)`: `Ppi` = indici `0-3`, `P0` = `6-9`; `Z(k)` unitaria *(Schur)* |
| lo stato fermo a `s 0.15` | `csv/_modo_al_variare_di_s.py` `carica("S1_s0.150")` | il residuo `1.771e-10`; `mu -0.566022365`; il tasso `0.15108` *(`dfb5ab7e`)* |
| le piatte nello stato fermo | `6d941a4d` | `3.9e-5` della norma *(`s 0.15`: `3.9004e-05`)* |
| **l'errore `n.80` del guardiano** | il mandato precedente, non mandato | spostava le due piatte in direzioni opposte: lo scarto della coppia non cambia |

### La convenzione del segno *(dal codice, prima)*

- `ph = -arg(lambda)` per tick *(`_dove_va_la_materia.autovettori`)*.
- **Lo spostamento:** dopo il tick, le componenti di `psi` sulla piatta `p` *(per impulso, sugli autovettori `Z(k)`)* moltiplicate per `e^{-i delta_p s}`. Allora `lambda -> lambda e^{-i delta_p s}` e `ph_p -> ph_p + delta_p s`: **`+delta_p` per unita' di tempo.**
- **Lo scarto della coppia** `ph_P0 + ph_Ppi - 2 ph_sol`, per unita' di tempo, cambia di `delta_P0 + delta_Ppi`: **`+2 delta` nella stessa direzione, `0` in direzioni opposte, `+delta` con una piatta sola.** Nel cuore a `s 0.15` lo scarto e' `-0.00955` *(`de411167`)*: zero a `delta = +0.0048`.
- **La norma si conserva:** una fase di modulo `1` su una base ortonormale *(`Z(k)` unitaria, la `fft2` unitaria a meno di `L^2`)*.

## 2. I CRITERI

- **Le corse:** `S1` `s 0.15` `L 81`, lo stato fermo di `dfb5ab7e`, `180` unita' di tempo *(`1200` tick)*.
  - la stessa direzione: `delta` in `{0, ±0.025, ±0.05, ±0.1, ±0.2, ±0.4, ±0.8}` per unita' di tempo;
  - le direzioni opposte *(`P0` `+delta`, `Ppi` `-delta`)*: `delta` `0.2`, `0.8`;
  - una piatta sola *(`P0` `delta`)*: `delta` `0.2`, `0.8`.
- **Il riferimento di `D`:** `psi_ref(t)` = lo stato fermo con le sue componenti piatte ruotate dello stesso spostamento, `e^{-i delta_p s t}`; `D(t) = e^{i mu s t} psi(t) - psi_ref(t)`. **A `delta = 0` e' `D` di `dfb5ab7e`.**
- **Il tasso:** la finestra di `dfb5ab7e` *(fra `1e3` volte il residuo e `1e-2`)*; le pendenze locali stampate.
- **DEVE:** lo sha1 dello stato fermo; la norma conservata dallo spostamento entro `1e-10` *(il massimo su tutte le corse)*; `delta = 0` ridà `0.15108` entro `1e-3` relativo.

## 3. LE LETTURE *(di Luca, scritte prima, senza soglie)*

- `(w1)` nella stessa direzione il tasso cala con `|delta|` e si spegne entro un `delta` dichiarato dai dati: la larghezza *(contro `x alpha'` `0.27` e `mu`)*;
- `(w2)` il tasso non cala fino a `0.8`; `(w3)` cala per un segno e cresce per l'altro; `(w4)` altro.
- `(k1)` in direzioni opposte il tasso resta `~0.151`, e una piatta sola a `delta` equivale alla stessa direzione a `delta/2`: il meccanismo e' la coppia; `(k2)` no.

## 4. LE MOTIVAZIONI

- La decisione di Luca sulle piatte *(tenerle; allontanarle alla Wilson; cambiare il legame su di esse)* dipende da quanto bisogna spostarle.

## 5. TODO

1. questo file, DA SOLO, e aspettare il push;
2. `csv/_larghezza_risonanza.py`, commit; `--referto`; RELAZIONE; MAPPA *(la riga `d`; le quattro voci della lista d'attesa; l'errore `n.80`)*; commit.

## 6. ANNOTAZIONE DOPO IL REFERTO *(`doc/referti_l2/larghezza_risonanza.txt`; lo script `sha1-BYTE 3f68bf99`, `e679e2ea`; `3/3`)*

| la corsa *(`s 0.15`)* | lo scarto | il tasso | `|D|` a tempo `60` / `120` / `180` |
|---|---|---|---|
| `delta 0` | `0` | **`0.15108`** | `1.1e-07` / `8.5e-04` / `3.4e-02` |
| stessa `+0.025` / `-0.025` | `+0.05` / `-0.05` | -- / -- | `2.9e-02` / `8.5e-02` / `1.4e-01`; `2.1e-02` / `5.0e-02` / `7.4e-02` |
| stessa `+0.1` / `-0.1` | `+0.2` / `-0.2` | -- / *(`2` campioni)* | `3.9e-02` / `8.7e-02` / `1.6e-01`; `7.6e-03` / `2.1e-02` / `3.5e-02` |
| stessa `+0.4` / `-0.4` | `+0.8` / `-0.8` | -- / *(non esponenziale)* | `1.2e-02` / `4.0e-02` / `8.5e-02`; `9.0e-03` / `1.4e-02` / `1.8e-02` |
| stessa `+0.8` / `-0.8` | `+1.6` / `-1.6` | *(non esponenziale)* / -- | `1.4e-02` / `1.3e-02` / `1.3e-02`; `6.6e-02` / `1.5e-01` / `2.7e-01` |
| opposte `0.2` / `0.8` | `0` / `0` | -- / -- | `3.4e-02` / `6.7e-02` / `9.5e-02`; `4.1e-02` / `6.7e-02` / `9.2e-02` |
| solo `P0` `0.2` / `0.8` | `+0.2` / `+0.8` | -- / -- | `4.0e-02` / `8.8e-02` / `1.6e-01`; `1.1e-02` / `2.9e-02` / `7.3e-02` |

- **I DEVE passano** *(`3/3`)*: la norma conservata *(`8.9e-16`)*; `delta 0` = `0.15108`.
- **Il tasso a `delta != 0` NON si misura col metodo dichiarato:** `|D|` e' gia' `7.6e-03`-`6.6e-02` al tempo `60`; la finestra e' vuota o di pochi campioni senza un tratto esponenziale. **Il riferimento dichiarato** *(lo stato fermo con la sua parte piatta ruotata)* **non e' uno stato fermo della mappa spostata:** lo scostamento iniziale viene da li', non dal modo.
- **Le letture `w1`-`w4`, `k1`-`k2`: non si decidono.**
- **La correzione proposta** *(non eseguita; una decisione di Luca)*: per ogni `delta`, lo stato fermo della mappa spostata con Newton *(partendo dallo stato fermo a `delta 0`)*, poi la corsa e il tasso come in `dfb5ab7e`.
