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
