# 2026-10-28 — DOVE VA LA MATERIA CHE IL CUORE PERDE *([[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; le risposte di Luca delle `20:52` a `383e68c2`)*

> **LIVELLO:** un'analisi degli stati salvati; nessuna corsa nuova; nessun file del nucleo.

## 0. LE RISPOSTE DELLE `20:52`

| | la risposta |
|---|---|
| 1 | la causa dello svuotamento di `S1` si cerca fuori dall'inviluppo |
| 2 | il 3D di `S1`: non ancora |
| 3 | nessuna forma nuova |
| 4 | `S4`: la diagnosi si chiude *(`s 0.3` il cuore regge, `0.579` -> `0.572`-`0.575`; `s 0.99` no, `0.622` -> `0.502`)*; i suoi stati finali sono il caso di controllo |
| 5 | la discontinuita' di `S4` a `rho = 0`: una nota |

## 1. LE PREMESSE DAL CODICE

| che cosa | dove | il fatto |
|---|---|---|
| lo stato | `_energia_del_legame.stato`, `_deriva_congelato.ampiezze` | `psi_h.reshape(n, 12)`: `12` componenti di materia per nodo; il nodo `v` ha `m1 = v // L`, `m2 = v % L` |
| lo stato iniziale | `_energia_del_legame.stato` | `g(r) Q exp(2 pi i (m1 + m2)/3)`, `Q` = la colonna `0` del livello `-0.458` di `TF.coppia_K(0, s)` |
| il tick | `_deriva_congelato.tick_congelato`, `VC.VUOTO` saltati | il congelato vero |
| gli stati salvati | `db/congelato_lungo/`, `db/diagnosi_s4/` | `S1` `s 0.3` `L 81`, `120` (tick `10000`); `S4` `s 0.3` `L 81`, `120` (`10000`), `s 0.99` `L 81` (`3030`); gli iniziali si ricostruiscono. **Stati `S1` a `s 0.075`: non esistono** |
| il tick libero sul toro `L 81`, `s 0.3` *(un'esplorazione)* | le risposte a un impulso di ampiezza `1e-6` | unitario entro `1.8e-15`; `12` bande: `4` piatte a `-pi s`, `4` piatte a `0`, `2` dispersive in `[-pi s, -0.458]`, `2` in `[0.458, pi s]`; a `K` e `K'` i livelli doppi `-0.458`, `+0.458` = `coppia_K`; lo stato iniziale ha il picco a `k = (27, 27)` |

## 2. I CRITERI

- **Il riferimento:** il tick congelato con la forma `S1` a ampiezza `1e-6` *(`x ~ 1e-13`: il legame spento)*, sulla scena di ogni stato *(`L`, `s`, il vuoto fermo)*; `A(k)` dalle `12` risposte a un impulso, `fft2`; gli autovettori dalla decomposizione di Schur, ordinati per fase. Lo stesso riferimento anche per gli stati `S4`.
- **Le BANDE** *(per indice ordinato di fase)*: `A` = le due che a `K` fanno il livello `-0.458` *(la coppia dell'inviluppo; `A-basso` e `A-alto` fuori dal punto `K`, dove sono degeneri)*; `B` = le due del livello `+0.458` *(l'altra della coppia)*; `P0` = le `4` piatte a `0`; `Ppi` = le `4` piatte a `-pi s`.
- **Le VALLI:** ogni `k` va al punto piu' vicino fra `Gamma`, `K`, `K'` *(con le immagini periodiche)*: nessun numero scelto.
- **Lo spettro radiale:** il peso di `A` nella valle `K` per anelli di `|k - K|` larghi un passo della griglia.
- **Le FINESTRE spaziali:** dal baricentro, `W_cuore = 1/(1 + e^{(r - w_in)/1})`, `W_anello = 1/(1 + e^{(r - 3 w0)/1}) - W_cuore` *(lo spessore `1` arco: la grana)*; e lo stato intero.
- **I controlli** *(DEVE)*: `A(k)` unitaria entro `1e-12`; lineare *(ampiezza `1e-6` e `2e-6` entro `1e-9`)*; le fasi a `K` = `coppia_K` entro `1e-9`; `Q` sta nel sottospazio `A` a `K` entro `1e-12`; i pesi sommano a `|psi|^2` entro `1e-12`; un tick dello stato iniziale scalato a norma piccola = `A(k)` applicata entro `1e-9`; uno stato col `Q` di `+0.458` sta in `B` piu' che in `A`.

## 3. LE LETTURE *(scritte prima, senza soglie)*

- (i) la materia persa sta in `B` o nelle piatte: il mescolamento fra bande;
- (ii) sta nella valle `K'`;
- (iii) sta in `A`, valle `K`, a `|k - K|` piu' grande: la dispersione oltre la curvatura;
- (iv) altro, descritto;
- `S1` contro `S4` a `s 0.3`: che cosa ha `S1` che `S4` non ha.

## 4. LE MOTIVAZIONI

- L'inviluppo vede una sola banda vicino a `K`: la decomposizione sugli autovettori del tick vede tutte e `12`.

## 5. TODO

1. questo file, da solo;
2. `csv/_dove_va_la_materia.py`, commit; il referto; la RELAZIONE; la MAPPA; commit.

## 6. ANNOTAZIONE DOPO IL REFERTO *(`doc/referti_l2/dove_va_la_materia.txt`; lo script `sha1-BYTE 31870035`, `7a40636f`; `30/30`; le sezioni sopra restano come erano)*

| fine - inizio, frazioni di `|psi|^2` dello stato intero | `S1` `s 0.3` `L 81` | `S1` `s 0.3` `L 120` | `S4` `s 0.3` `L 81` | `S4` `s 0.3` `L 120` | `S4` `s 0.99` `L 81` |
|---|---|---|---|---|---|
| cuore, banda `A` | `-0.112` | `-0.087` | `-0.019` | `-0.022` | `-0.071` |
| anello, banda `A` | `+0.119` | `+0.085` | `+0.008` | `+0.010` | `+0.009` |
| anello, `|k - K|` medio in `A` | `-0.045` | `-0.034` | `-0.016` | `-0.017` | `-0.037` |
| intero, banda `A` | `-0.0155` | `-0.0135` | `-0.0203` | `-0.0204` | `-0.0942` |
| intero, `B` / `P0` / `Ppi` | `+0.0040` / `+0.0061` / `+0.0055` | `+0.0045` / `+0.0058` / `+0.0031` | `+0.0097` / `+0.0090` / `+0.0015` | `+0.0096` / `+0.0095` / `+0.0013` | `+0.0146` / `+0.0330` / `+0.0466` |
| intero, `A` nella valle `K'` / `Gamma` | `+0.0021` / `+0.0013` | `+0.0047` / `+0.0017` | `+0.0011` / `+0.0007` | `+0.0012` / `+0.0008` | `+0.0060` / `+0.0048` |

| lettura | esito |
|---|---|
| (i) la materia persa in `B` o nelle piatte | `S1`: **no** per il cuore *(l'anello: `B` `+0.001`, `P0` `+0.004`, `Ppi` `+0.002`, contro `A` `+0.119`)*; il mescolamento sullo stato intero e' `1.5%`. `S4` `s 0.99`: **si'** *(`P0` `+0.033`, `Ppi` `+0.047`)* |
| (ii) nella valle `K'` | **no** *(`+0.002`-`+0.005`)* |
| (iii) in `A`, valle `K`, a `|k - K|` piu' grande | **no**: `|k - K|` medio dell'anello **cala** *(`-0.045`, `-0.034`)* |
| (iv) altro | `S1`: **la materia che il cuore perde resta nella banda `A`, valle `K`, e va nell'anello a `|k - K|` piu' piccolo** |
| `S1` contro `S4` a `s 0.3` | il mescolamento fra bande e valli c'e' in tutte e due *(`1.5%` e `2.0%`)*; `S1` ha in piu' il passaggio cuore -> anello nella stessa banda *(`0.112` contro `0.019`)* |

- **La divisione `A-basso` / `A-alto`** per indice di fase dello stesso stato iniziale cambia fra `L 81` e `L 120` *(`0.583` / `0.335` contro `0.326` / `0.634`)*: non si legge; si legge il gruppo `A`.
