# 2026-10-29 — IL DECADIMENTO IN COPPIA *([[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il mandato di Luca delle `13:02`, dopo `6c720842`)*

> **LIVELLO:** conti sugli stati fermi e sul tick libero; due corse col filtro su una piatta sola *(`600` tick)*; Newton ripreso a `s 0.075`; nessun file del nucleo.

## 1. LE PREMESSE DAL CODICE

| che cosa | dove | il fatto |
|---|---|---|
| `x alpha'(x)` di `S1` | `csv/_screening_forme_s3.acc_mano` | `2 x^2 / (1 + x^2)^2`, massimo `1/2` a `x = 1`; lo script lo controlla contro la differenza finita di `_ab` |
| la fase della coppia a `K` | `csv/_triangoli_forza.coppia_K` | il livello di `A` a `K`, `ph = -arg(lambda)` per tick; e' quello del tick libero sul toro *(controllato a `s 0.3` in `9aa268c8`, entro `1e-9`)* |
| il filtro | `csv/_filtro_bande_piatte.py` `Filtro`, `esame` | gli indici `Ppi` = `0-3`, `P0` = `6-9` |
| Newton | `csv/_modo_al_variare_di_s.py` `cerca` | parte dallo stato del risolutore: **per riprendere serve una copia che parta da uno stato dato** |
| lo stato a `s 0.075` | `db/modo_s/fermo_S1_s0.075.npz` | il residuo `9.696e-06`, lo sha1 `9744446c` |

## 2. I CRITERI

- **(1a)** per anello *(gli stati fermi a `s 0.3` e `s 0.15`)*: `x alpha'(x)` medio sui nodi, `x = rho/Lambda` del nodo; il massimo e l'anello; contro gli anelli del modo *(`12`-`13`, `dfb5ab7e`)*.
- **(1b)** `ph_A(K) / s` a `s 0.3`, `0.15`, `0.075`, `0.0375`, contro `-pi/2`; lo scarto e il suo rapporto fra due `s` successivi.
- **(1c)** `2 - pi - 2 mu` *(la condizione `c2` `P0+Ppi` nel cuore, `alpha = 1`, per unita' di tempo)* a `s 0.3`, `0.15`; e a `s 0.075` col `mu` non convergito, dichiarato tale; e col `mu` di Newton ripreso, se converge.
- **(2)** `S1` `s 0.3`, lo stato fermo di `26300537`, `600` tick: (i) togliendo solo `P0`; (ii) togliendo solo `Ppi`; l'esame di `6d941a4d` *(rispetto allo stato fermo filtrato una volta)*: il tasso, la norma tolta per tick, le bande di `D`.
- **(3)** Newton ripreso dallo stato di `dfb5ab7e`, al piu' `60` passi, lo stesso criterio *(`1e-9`)*; se converge: la corsa di `180` unita' di tempo e il tasso con la finestra di `dfb5ab7e` *(fra `1e3` volte il residuo e `1e-2`)*. **Gira in parallelo agli altri punti; nel referto e' l'ultimo.**
- **DEVE:** `acc_mano` = la differenza finita di `_ab` entro `1e-6`; lo sha1 degli stati; `M` nelle corse non filtrate entro `1e-10`.

## 3. LE LETTURE *(di Luca, scritte prima, senza soglie)*

- `(p1)` togliendo una sola piatta il modo non cresce, in tutti e due i casi: il decadimento e' in coppia `P0+Ppi`;
- `(p2)` solo una delle due spegne il modo: un processo di una banda *(quale)*;
- `(p3)` nessuna delle due da sola: serve toglierle insieme, un altro meccanismo; `(p4)` altro.
- `(q1)` il massimo di `x alpha'(x)` cade negli anelli del modo; `(q2)` altrove.
- `(b)` `ph_A(K)/s` tende a `-pi/2` per `s` piccolo, o no.
- Il punto `3`: il tasso a `s 0.075` contro `0.139` e `0.151` *(se il decadimento e' risonante, il tasso e' massimo dove `2 - pi - 2 mu` passa per lo zero)*.

## 4. LE MOTIVAZIONI

- L'ipotesi di Luca: due quanti del solitone in uno di `P0` e uno di `Ppi`, risonante nel cuore, accoppiato dove `alpha` cambia con `rho`.

## 5. TODO

1. questo file, DA SOLO, e aspettare il push;
2. `csv/_decadimento_in_coppia.py`, commit; `--cerca` in parallelo; `--referto`; RELAZIONE; MAPPA; commit.

## 6. ANNOTAZIONE DOPO IL REFERTO INTERMEDIO *(`doc/referti_l2/decadimento_in_coppia.txt`; lo script `sha1-BYTE fc59d7a1`, `e38289a3`; `3/3`; il punto `3` in corsa)*

| il conto | `s 0.3` | `s 0.15` | `s 0.075` | `s 0.0375` |
|---|---|---|---|---|
| `x alpha'(x)` massimo per anello *(l'anello)*; negli anelli `12`, `13` | `0.2668` *(`13`)*; `0.0160`, `0.2668` | `0.2560` *(`13`)*; `0.0149`, `0.2560` | -- | -- |
| `ph_A(K)/s`; lo scarto da `-pi/2` | `-1.52661`; `+4.42e-02` | `-1.55986`; `+1.09e-02` | `-1.56807`; `+2.73e-03` | `-1.57011`; `+6.81e-04` |
| `2 - pi - 2 mu` per unita' di tempo | `-0.07610` | `-0.00955` | `+0.00692` *(`mu` NON fermo)* | -- |

| il filtro *(`S1` `s 0.3`, `600` tick)* | il tasso per unita' di tempo | la norma tolta per tick *(alla fine)* |
|---|---|---|
| nessuno *(`dfb5ab7e`)* | `0.13870` | -- |
| solo `P0` | `0.00557` | `4.55e-06` |
| solo `Ppi` | `0.00592` | `2.75e-06` |
| `P0` e `Ppi` insieme *(`6d941a4d`)* | `0.00067` | `7.33e-06` |

| lettura *(di Luca, scritta prima)* | esito |
|---|---|
| (p1) togliendo una sola piatta il modo non cresce, in tutti e due i casi: in coppia `P0+Ppi` | **SI':** `0.0056` e `0.0059` contro `0.139` |
| (p2) / (p3) | no |
| (q1) il massimo di `x alpha'` negli anelli del modo | **SI':** l'anello `13`, a tutte e due le `s` |
| (b) `ph_A(K)/s` tende a `-pi/2` | **SI':** lo scarto cala di `~4` volte a ogni dimezzamento di `s` *(i rapporti `0.2475`, `0.2494`, `0.2498`)* |
| il punto `3` *(`s 0.075`)* | **IN CORSA:** Newton ripreso dallo stato di `dfb5ab7e` |

## 7. ANNOTAZIONE DOPO IL REFERTO FINALE *(il referto rigenerato; lo stesso script `sha1-BYTE fc59d7a1`; `6/6`)*

| `S1`, `L 81`, `N 1e6` | `s 0.3` | `s 0.15` | `s 0.075` |
|---|---|---|---|
| lo stato fermo *(residuo, passi)* | `9.8e-10`, `15` | `1.8e-10`, `22` | `3.6e-10`, `23` **ripresi** dallo stato di `dfb5ab7e` |
| `mu` | `-0.532745112` | `-0.566022365` | `-0.574239118` |
| `2 - pi - 2 mu` per unita' di tempo | `-0.07610` | `-0.00955` | `+0.00689` |
| il tasso per unita' di tempo | `0.13870` | `0.15108` | `0.14998` |
| il periodo | `11.45` | `11.45` | `11.45` |
| `|D|^2` negli anelli `12` / `13`, al primo istante | `0.355` / `0.545` | `0.503` / `0.418` | `0.523` / `0.403` |
| le piatte `P0` + `Ppi`, al primo istante | `0.481` + `0.417` | `0.503` + `0.417` | `0.496` + `0.430` |

| lettura | esito |
|---|---|
| (A1) il tasso converge al calare di `s` *(il mandato delle `10:00`)* | **SI':** `0.139` -> `0.151` -> `0.150` |
| il tasso massimo dove `2 - pi - 2 mu` passa per lo zero *(il punto `3` delle `13:02`)* | **compatibile, debole:** `2 - pi - 2 mu` passa per lo zero fra `s 0.15` e `s 0.075`; il tasso li' e' `0.151` e `0.150`, la differenza e' lo `0.7%` |
| il periodo | `11.45` a tutte e tre le `s`; non segue `2 pi/|mu|` |
