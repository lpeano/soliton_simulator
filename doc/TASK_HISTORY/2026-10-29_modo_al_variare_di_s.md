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
