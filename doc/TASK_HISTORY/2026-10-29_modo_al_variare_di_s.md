# 2026-10-29 — IL MODO INSTABILE AL VARIARE DI `s`, E PER `S4` *([[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il mandato di Luca delle `10:00`, dopo `5f06dbfb`)*

> **LIVELLO:** tre stati fermi sul reticolo *(`S1` a `s 0.15` e `0.075`; `S4` a `s 0.3`)*, una corsa breve da ciascuno, lo stesso esame di `5f06dbfb` senza Arnoldi; nessun file del nucleo.

## 1. LE PREMESSE DAL CODICE

| che cosa | dove | il fatto |
|---|---|---|
| forma, `s`, `N` in memoria | `csv/_diagnosi_s4.py` `configura`, `iniziale` | `VC.FORMA`, `VC.S`, `DC.N`, rimessi alla fine; lo stato del risolutore sul toro `L` |
| Newton | `csv/_stato_fermo.py` `cerca` | il metodo e il criterio di `26300537`, ma con `s 0.3` e `S1` scritti nel modulo: **serve una copia con forma, `s`, `N` come argomenti** |
| il precondizionatore | `csv/_dove_va_la_materia.py` `matrice` | il tick libero *(`S1` a ampiezza `1e-6`)*; **per `S4`** il legame a densita' piccola mette la fase `exp(-i alpha(0) dtau)`, `alpha_4(0) = -pi` *(`primo_ordine/materia_vuoto.applica`: `al * dtau * f`)*: il precondizionatore di `S4` e' `e^{-i alpha(0) s} A(k)`; **cambia solo la velocita' di Newton, non il criterio** |
| l'esame | `csv/_modo_dalla_corsa.py`, `csv/_modo_instabile.py` | il tasso, la rotazione, la forma *(anelli, bande, armoniche `m 0..12`)* |

## 2. I CRITERI

- **I casi:** `S1`, `N 1e6`, `L 81`, `s 0.15` e `s 0.075`; `S4`, `N 1e7`, `L 81`, `s 0.3`. E `S1` `s 0.3` dai dati di `5f06dbfb` *(non rifatto)*.
- **Newton:** il residuo per tick `< 1e-9`, al piu' `30` passi; lo stesso GMRES, differenza centrata, precondizionatore.
- **Le corse, lo stesso TEMPO FISICO:** `180` unita' *(`1200` tick a `s 0.15`, `2400` a `0.075`, `600` a `0.3`)*; `D(t)` ogni `round(3/s)` tick dal tempo `60` *(come `10` tick da `200` a `s 0.3`)*.
- **Il tasso:** la finestra fra `1e3` volte il residuo e `1e-2`, come in `5f06dbfb`; per unita' di tempo.
- **Il periodo:** dai cambi di segno della proiezione su `D` al centro della finestra; in unita' di tempo; contro `2 pi / |mu|` e contro il respiro della corsa lunga *(`11.1`)*.
- **La forma, a tre istanti dichiarati dai dati:** il primo campione con `|D|/|psi0| >= 1e-4`, il primo con `>= 1e-3`, l'ultimo della finestra; anelli, bande, armoniche.
- **Il bordo** *(per `B1`)*: il profilo per anelli dello stato fermo; la pendenza massima `|rho(k+1) - rho(k)|` divisa per il picco, e l'anello dove sta.
- **DEVE:** il criterio di Newton per ogni stato *(se `S4` non lo raggiunge: si scrive con la storia, i punti `1`-`2` restano)*; lo sha1 dello stato salvato; `M` conservata nelle corse entro `1e-10`.

## 3. LE LETTURE *(di Luca, scritte prima, senza soglie)*

- `(A1)` il tasso per unita' di tempo converge al calare di `s`: un'instabilita' del modello a tempo continuo;
- `(A2)` il tasso cambia molto con `s`: una risonanza col passo *(come cambia)*;
- `(B1)` `S4` non ha il modo *(o molto piu' lento)*: il colpevole e' il bordo ripido di `S1` *(la pendenza al bordo, le due forme)*;
- `(B2)` `S4` ha lo stesso modo: del solitone sul reticolo, non della forma;
- `(C)` il periodo segue `2 pi / |mu|` a ogni `s`, o no;
- `(D)` altro, descritto.

## 4. LE MOTIVAZIONI

- La regola di `PATTERN_DI_PROVA`: un numero e' fisico solo se converge raffinando `s`.

## 5. TODO

1. questo file, DA SOLO, e aspettare il push;
2. `csv/_modo_al_variare_di_s.py`, commit; `--cerca` e `--corsa` per i tre casi; `--referto`; RELAZIONE; MAPPA; commit.

## 6. ANNOTAZIONE DOPO IL REFERTO *(`doc/referti_l2/modo_al_variare_di_s.txt`; lo script `sha1-BYTE 65fa0bd3`, `364ffe5d`; `8/10`)*

| | `S1` `s 0.3` | `S1` `s 0.15` | `S1` `s 0.075` | `S4` `s 0.3` |
|---|---|---|---|---|
| Newton *(criterio `1e-9`, `30` passi)* | `9.808e-10`, `15` passi | `1.771e-10`, `22` passi | **FALLISCE:** `9.696e-06`, cala lento | **FALLISCE:** `1.422e-03`, quasi fermo |
| `mu`; `2 pi / |mu|` | `-0.532745`; `11.794` | `-0.566022`; `11.101` | -- | -- |
| il tasso per unita' di tempo *(la finestra)* | `0.13870` *(tempo `75`-`141`)* | `0.15108` *(tempo `66`-`138`)* | -- | -- |
| il periodo | `11.45` | `11.45` | -- | -- |
| `|D|^2` negli anelli, al primo istante | `r 13 0.545`, `r 12 0.355` | `r 12 0.503`, `r 13 0.418` | -- | -- |
| le bande `P0` / `Ppi` / `A`, al primo istante | `0.481` / `0.417` / `0.096` | `0.503` / `0.417` / `0.078` | -- | -- |
| la pendenza massima del profilo / picco *(anelli)* | `0.1223` *(5-6)* | `0.1222` *(5-6)* | -- | -- |

| lettura *(di Luca, scritta prima)* | esito |
|---|---|
| (A1) il tasso converge al calare di `s` / (A2) cambia molto | **non si decide con due passi:** `0.139` -> `0.151` *(`+9%`)*; il terzo passo, `s 0.075`, non ha lo stato fermo |
| (B1) / (B2) `S4` ha o no il modo | **non si decide:** lo stato fermo di `S4` non si trova col criterio *(`1.4e-3`)* |
| (C) il periodo segue `2 pi / |mu|` | **no:** il periodo e' `11.45` a tutte e due le `s`; `2 pi / |mu|` va da `11.794` a `11.101` |
| (D) altro | la forma del modo e' la stessa alle due `s`: il bordo *(anelli `12`-`13`)*, le piatte *(`0.90`-`0.92`)* |

- **Due DEVE falliti** *(Newton a `S1` `s 0.075` e a `S4`)*: lo stato e il fallimento committati; **FERMO** su questi due *(par. `5`)*.
