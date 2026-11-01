# 2026-11-01 — IL SOLITONE SU `B` A `Gamma` COL TICK INTERO *(IL VUOTO VIVO; UNA PROVA IN `csv/`, NESSUNA MODIFICA AL NUCLEO; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]], [[LIBRO-DEI-CONTI]], [[VUOTO-SUL-FONDO]]; il mandato di Luca delle `22:35` del `2026-10-31`)*

> **Lo script:** `csv/_vuoto_vivo_B.py`. **I dati:** `doc/referti_l2/vuoto_vivo_B/` *(un jsonl per pezzo)*; gli stati di ripresa in `db/vuoto_vivo_B/` *(ignorato)*. **Il referto:** `doc/referti_l2/vuoto_vivo_B.txt`.

## 1. LE PREMESSE DAL CODICE

- **Le due scene nascono dalla STESSA funzione.** `_massimo_di_B.scena` → `_livelli_piatti.scena` → `_diagnosi_s4.iniziale` → `_deriva_congelato.nuovo(rec, "uniforme")` → `_energia_del_legame.stato`, e `scena` mette `z["par"]["eps"] = eps`. **`_deriva_congelato.nuovo(rec, "fondo")`** da' lo stesso stato sul vuoto del fondo *(`_solitone_con_la_buca.vuoto_iniziale("fondo")` = `_solitone_dal_fondo.fondo_con_fasi(..., F0)`, il vuoto di `76eecbf5`)*. **Quindi (U) e (F) si costruiscono cambiando una parola**, e la scena a `s 0.075` con `_diagnosi_s4.configura(FORMA, 0.075, N)` *(il risolutore a quel passo: `DC.prepara`)*.
- **`cs` SPENTO, dal codice:** `_energia_del_legame.stato` mette **`mot.cs = np.full(n, VC.S)`** *(costante, uguale a `s`)* e **`mot.lambda_c = None`**; il passo e' **`tick.percorri_tick`**, non `tick_con_cs`. Cosi' nelle prove del libro dei conti *(`_libro_dei_conti.py`: «cs SPENTO»)* e in `_solitone_dal_fondo`.
- **Il tick INTERO:** `TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))`, **tutti i `14` pezzi, e `phi` NON rimesso** *(il congelato di `74f99039`, `_congelato_lungo.avanza`, salta i pezzi del vuoto e rimette `phi`)*.
- **I due solitoni, dalla costruzione dell'inviluppo** *(quella delle corse di robustezza di `751bca7f`, senza Newton)*:
  - **(BG)** `_consolida_B.inviluppo(z, pK, q, N)`, con `q` la scelta migliore a eps `0.5` *(`_consolida_B.q_migliore`: theta, phi da `griglia.json`, la coppia `q1`, `q2` di `_coppia_di_B.coppia`)*;
  - **(AK)** `pK`, lo stato della scena *(l'inviluppo per `Q_K` e la fase di `K`; `_coppia_di_B.partenza_corsa("AK")`)*.
- **Il libro dei conti:** `_libro_dei_conti.conti_per_nodo(inc, mot, st, e_K, 0.5)` *(la materia `cin`, il vuoto `vuo`, il legame `leg`, `tot` = `H_tot`)*, `e_K` l'energia per norma dello stato uniforme di `A` a `K` *(`_scomposizione_solitone.stato_uniforme`, come `_solitone_dal_fondo.prepara`)*; **la strada `A`:** il guadagno di `H_tot` sul disco `2 w_in`, tick per tick.
- **`matrice` ora ha la guardia** *(`6c5da5e8`)*: la base delle bande e la partenza si misurano senza sporcare la scena.

### Cosa NON so

- **Se la scelta `q` a eps `0.5` (theta, phi di `griglia.json`, trovati a `s 0.15` sul vuoto uniforme) sia ancora la scelta migliore a `s 0.075` e sul vuoto del fondo.** La uso uguale *(dichiarato)*: **la coppia `q1`, `q2` si ricalcola** sulla scena di ogni corsa *(il suo `s`, il suo vuoto)*, theta e phi no.
- **Se `B` a `Gamma` resti la coppia piu' alta col vuoto del fondo:** `coppia` prende le due fasi piu' alte di `A(Gamma)`; **lo stampo** *(`E0`, la separazione)*.
- **Quanto costa:** il tick intero e i conti a ogni tick; lo misuro sul primo pezzo.

## 2. I CRITERI

| il punto | il criterio, scritto prima |
|---|---|
| `0` | **Le scene:** la scena `(U, s 0.15)` costruita da me = `_massimo_di_B.scena`, **AL BIT** *(ogni chiave di `z["st"]`)* — DEVE. `F0` = `_vuoto_sul_fondo.fondo_uniforme` al bit — DEVE. **Il controllo positivo del tick intero:** la MIA corsa sullo stato di `15df5c63` *(eps `0`, vuoto uniforme, `s 0.3`)* da' **la vita `320`** *(ogni `20` tick, il criterio di larghezza e frazione di `_solitoni_triangoli`)* — DEVE. |
| `1` | **Le corse:** `BG-U`, `BG-F`, `AK-U`, `AK-F` a `s 0.15`; poi `BG-U`, `BG-F` a `s 0.075`. **`3000` unita' di tempo** *(`20000` tick a `s 0.15`, `40000` a `s 0.075`)* **o fino alla dissoluzione: `f_liscia` sotto meta' del valore iniziale** *(misurata ogni `10` tick; la corsa si ferma al primo campione sotto)*. A pezzi di `10000` tick, uno per processo, ogni pezzo committato; **la ripresa DEVE essere al bit** *(lo sha1 di OGNI chiave di `z["st"]` = la fine del pezzo prima)*. |
| `2` | **Ogni `10` tick:** il cuore con la finestra **LISCIA** *(peso lineare da `1` a `0` su una lunghezza d'arco attorno a `w_in`, come `_salti_nel_cuore.campione`)* e quella **NETTA** accanto, la larghezza, **l'alone** `1 - f_3w0`, il baricentro; **`Lambda` medio sotto il solitone** *(il disco `2 w_in`)* **e lontano.** **Ogni `20` tick:** le bande di `D = e^{i mu s t} psi - psi0` *(la base di `autovettori(matrice)` sulla scena della corsa, il suo vuoto; `mu` di Rayleigh del tick congelato)*. **Ogni tick:** i conti per nodo, e la strada `A`; **ogni `10`:** materia, vuoto, legame, `H_tot` per regione *(il disco `2 w_in`, fuori, il toro)*. |
| `3` | **DEVE:** `M` e `V` entro `1e-10` in ogni corsa *(come `_solitone_dal_fondo`)*. **DEVE:** `H_tot` conservata a `O(s^2)`: per `BG-U` e `BG-F` il rapporto di `max abs(H_tot - H_tot(0))` fra `s 0.15` e `s 0.075`, **sulla finestra di tempo fisico comune**, fra `3` e `5` *(il `RAPPORTO` dichiarato in `_regime_del_passo.py`, `99eb7a42`)*. |

## 3. LE LETTURE *(di Luca, scritte prima, senza soglie)*

- **(v1)** `BG` regge col vuoto vivo con tutti e due i vuoti, mentre `AK` si scioglie: la protezione vale anche col vuoto, e il problema della riga `1` della sezione `2` era quello delle bande piatte;
- **(v2)** `BG` si scioglie col vuoto uniforme e regge col fondo *(o viceversa)*: il problema del vuoto e' separato da quello delle piatte *(quale vuoto, in che verso va l'energia, dal libro dei conti)*;
- **(v3)** `BG` si scioglie con tutti e due: un'uscita verso il vuoto *(quale: le bande di `D`, l'energia che passa al vuoto)*;
- **(v4)** altro.
- **Per ogni lettura: `s 0.15` contro `s 0.075`.**

## 4. LE MOTIVAZIONI

**Gravita'** *(due solitoni che si attraggono, la caduta, la gobba)* **e mitosi passano dal vuoto:** serve sapere se il solitone protetto regge col vuoto vivo **prima di costruirci sopra**.

## 5. TODO

1. Questo file, committato **DA SOLO**.
2. `csv/_vuoto_vivo_B.py` *(`--controllo`, `--corsa NOME`, `--referto`)* e la riga nell'inventario, committati prima di girare.
3. `--controllo` *(le scene al bit, `F0`, la vita `320`)*: committato; **se un DEVE fallisce, FERMO.**
4. Le corse a pezzi, una alla volta, ogni pezzo committato *(un driver)*; **se la ripresa non e' al bit, FERMO.**
5. `--referto`; `doc/CHIUDERE_LE_USCITE.md`; `RELAZIONE`; `MAPPA` *(la sezione `2` riga `1`; la riga `d` della sezione `3`)*; la sezione `6` qui.
