# 2026-10-29 — LA LARGHEZZA DELLA RISONANZA CON LO STATO FERMO DI OGNI MAPPA SPOSTATA *(UNA DIAGNOSI, NON UNA CURA; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il mandato di Luca delle `17:15`, dopo `22458a37`)*

> **LIVELLO:** lo strumento di `22458a37` *(`csv/_larghezza_risonanza.py`)*, esteso; `8` ricerche di Newton e `9` corse a `s 0.15`; nessun file del nucleo.

## 1. LE PREMESSE DAL CODICE

| che cosa | dove | il fatto |
|---|---|---|
| lo spostamento | `csv/_larghezza_risonanza.Spostamento` | dopo il tick, le componenti su `P0` *(indici `6-9`)* e `Ppi` *(`0-3`)* per `e^{-i delta_p s}`; la norma si conserva a `8.9e-16` *(`22458a37`)* |
| Newton | `csv/_modo_al_variare_di_s.cerca`; ripreso in `csv/_decadimento_in_coppia.cerca` | `F = (T psi - e^{-i mu s} psi, |psi|^2 - N)`; GMRES con `J v` a differenza centrale *(`H_REL 1e-5`)*; il precondizionatore `(A(k) e^{-i alpha(0) s} - e^{-i mu s})^{-1}`; `MAX_NEWTON 30`, `TOLL_RES 1e-9`; il `mu` iniziale dal quoziente di Rayleigh sulla mappa |
| lo stato a `delta 0` | `db/modo_s/fermo_S1_s0.150.npz`, `doc/referti_l2/modo_s/cerca_S1_s0.150.json` | il residuo `1.771e-10`, `22` passi, `2680` s; `mu -0.566022365` |
| dove stanno gli stati | `.gitignore` *(`db/`)* | ogni `.npz` precedente sta in `db/`, **ignorato**; nel repo va il `.json` con lo sha1, `mu`, la storia |
| l'esame | `csv/_filtro_bande_piatte.esame` | il tasso *(la finestra fra `1e3` volte il residuo e `1e-2`)*, il periodo dai cambi di segno della proiezione, gli anelli e le bande di `D`: il metodo di `dfb5ab7e` |
| **l'errore `n.81` del guardiano** | il mandato delle `14:51` | non chiedeva lo stato fermo di ogni mappa spostata, e io non l'ho segnalato prima di girare |

## 2. I CRITERI

- **La mappa spostata:** `T_delta psi = Spostamento(tick(psi))`. **Il precondizionatore:** per ogni `k`, `Z diag(f) Z^H A(k) e^{-i alpha(0) s}` meno `e^{-i mu s}`, invertita *(`f` = le fasi dello spostamento)*.
- **Gli `8` spostamenti e la continuazione** *(la partenza: lo stato convergito piu' vicino, in distanza euclidea su `(delta_P0, delta_Ppi)`, fra `delta 0` e gli stati gia' risolti DELLA STESSA CATENA)*:

| la catena | gli stati, in ordine | la partenza prevista |
|---|---|---|
| `piu` | stessa `+0.05`, `+0.2`, `+0.8`; poi solo `P0` `+0.8` | `0` -> `+0.05` -> `+0.2`; solo `P0` `+0.8` da stessa `+0.2` *(distanza `0.63`; da `+0.8`: `0.80`)* |
| `meno` | stessa `-0.05`, `-0.2`, `-0.8` | `0` -> `-0.05` -> `-0.2` |
| `opposte` | `P0` `+0.8`, `Ppi` `-0.8` | `delta 0` *(distanza `1.13`, la minima)* |

- **Le tre catene girano in parallelo, uno stato per processo** *(`--cerca <nome>`)*: finito un processo, si committa il suo `.json` e si lancia il successivo della catena. **Un riavvio:** lo script legge gli stati dal disco; uno stato col `.json` presente non si ricalcola.
- **Il salvataggio:** il `.npz` in `db/larghezza/` *(ignorato come tutti gli stati precedenti; un riavvio non lo cancella)*; il `.json` in `doc/referti_l2/larghezza/` *(lo sha1 dello stato, `mu`, la storia, la partenza)*, **committato subito**.
- **Se Newton non converge in `30` passi:** il `.json` con la storia e `convergito: false`; la catena prosegue dallo stato convergito piu' vicino.
- **Per ogni stato:** `mu`; la distanza `1 - |<a|b>|^2` *(normalizzati)* dallo stato a `delta 0`.
- **La corsa** *(`--referto`)*: da ogni stato convergito, e da `delta 0` con la mappa non spostata; `1200` tick *(`180` unita' di tempo)* con la mappa spostata; `D(t) = e^{i mu s t} psi(t) - psi_delta`; l'esame di `dfb5ab7e` *(`_filtro_bande_piatte.esame`, `D` ogni `3` unita' di tempo da `60`)*.
- **DEVE:** lo sha1 di ogni stato = il suo `.json`; la norma conservata dalla mappa entro `1e-10` *(il massimo su tutte le corse)*; `delta 0` ridà `0.15108` entro `1e-3` relativo.

## 3. LE LETTURE *(di Luca, scritte prima, senza soglie)*

- `(w1)` nella stessa direzione il tasso cala con `|delta|` e si spegne: la larghezza *(dichiarata dai dati, contro `x alpha'` `0.27` e `mu`)*;
- `(w2)` non cala fino a `0.8`; `(w3)` cala per un segno e cresce per l'altro; `(w4)` altro.
- `(k1)` in direzioni opposte il tasso resta `~0.151`, e una piatta sola a `0.8` equivale alla stessa direzione a `0.4` *(qui: fra `0.2` e `0.8`)*: il meccanismo e' la coppia; `(k2)` no.

## 4. LE MOTIVAZIONI

- `22458a37`: il riferimento ruotato non e' fermo nella mappa spostata; lo scostamento iniziale copriva il modo.
- La decisione di Luca sulle piatte dipende da quanto bisogna spostarle.

## 5. TODO

1. questo file, DA SOLO, e aspettare il push;
2. `csv/_larghezza_risonanza.py` esteso *(`--cerca <nome>`, `--referto`)*, la voce d'inventario, commit;
3. le tre catene; un commit per ogni `.json`;
4. `--referto` -> `doc/referti_l2/larghezza_stati_fermi.txt`; RELAZIONE; MAPPA *(la riga `d`; l'errore `n.81`)*; questo file annotato; commit.
