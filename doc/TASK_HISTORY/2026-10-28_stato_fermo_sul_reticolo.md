# 2026-10-28 — LO STATO FERMO DI `S1` SUL RETICOLO *([[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il mandato di Luca delle `21:29`, dopo `9aa268c8`)*

> **LIVELLO:** una ricerca dello stato fermo in memoria, un confronto, una corsa *(`s 0.3`, `L 81`, `3000` di tempo fisico)*; nessun file del nucleo.

## 1. LE PREMESSE DAL CODICE

### Il punto `0`: da dove viene lo stato iniziale di `40061005`

| passo | file e righe *(il blob di oggi; si cerca per nome)* | che cosa fa |
|---|---|---|
| `1` | `csv/_congelato_lungo.py` `iniziale` (58-63) | `DC.prepara(S)`, poi `DC.nuovo(rec, scena)` |
| `2` | `csv/_deriva_congelato.py` `prepara` (49-62) | `c` dalla curvatura del ramo basso della coppia a `K` (`STR.c_triangoli`); `MPS.largo(VC.FORMA, c, s, N)` |
| `3` | `csv/_modi_pi_e_solitoni.py` `largo` (307-325) | ripete `GC.profilo` finche' la larghezza non cambia oltre `1e-3` |
| `4` | `csv/_gravita_collettiva.py` `profilo` (367-420) | **l'inviluppo CONTINUO, radiale:** i pesi `2 pi r dr` (379), il laplaciano radiale (381-), il tempo immaginario con la norma fissata (`solve_banded`, 404) |
| `5` | `csv/_energia_del_legame.py` `stato` (63-88) | il profilo `u(r)` sui nodi: `np.interp(rr, r, u) sqrt(AREA_NODO)` (84), per `Q` di `coppia_K` (85) e `exp(2 pi i (m1 + m2)/3)`, rinormalizzato a `N` (87) |

**Il fatto:** lo stato iniziale e' lo stato fermo dell'**inviluppo continuo** di una banda, messo sul reticolo; **non** uno stato fermo del tick sul reticolo.
Un'esplorazione *(non salvata)*: a `L 81` il residuo per tick `|T psi - lambda psi| / |psi|` dello stato iniziale e' `0.034`, `|lambda| = 0.99943`.

### Una correzione alle premesse del mandato

`w0 = 3.1065` archi e' la larghezza di **`S4`** a `s 0.3`, `N 1e7` *(`9e8805ba`)*. Lo stato `S1` di `40061005` ha `w0 = 6.6003` archi, `N 1e6`.

### Il tick

`_deriva_congelato.tick_congelato` con `VC.VUOTO` saltati e `phi` rimesso; la forma `S1`; `BE.conv("simm")`. Deterministico; `st` ha anche `psi`, `Lambda`, `rho`, `h_int`, ricalcolati dal tick *(lo stesso `psi_h` da' lo stesso risultato)*.

## 2. I CRITERI

- **Il metodo: Newton sulla mappa del tick.** Le incognite: `psi` *(parte reale e immaginaria)* e `mu`. Le equazioni: `(T psi - e^{-i mu s} psi)/sqrt(N) = 0` e `(|psi|^2 - N)/N = 0`.
  Il sistema lineare di ogni passo con GMRES *(senza matrice: `J v` per differenze finite del tick)*; il passo dimezzato se il residuo non cala. La fase globale resta libera.
- **La partenza:** lo stato iniziale di `40061005`, `mu` dalla fase di `<psi, T psi>`.
- **Il criterio di arresto, PRIMA:** il residuo `r = |T psi - e^{-i mu s} psi| / |psi| < 1e-9`, al piu' `30` passi di Newton. Se non si raggiunge: la lettura `(c)`, col residuo e la storia dei passi.
- **Il confronto:** il profilo radiale per anelli e la frazione entro `w_in` *(stato fermo, tick `0`, tick `10000`)*; la distanza `1 - |<a|b>|^2/(|a|^2 |b|^2)` per le tre coppie; `mu` dello stato fermo contro la fase per tick dello stato iniziale e contro `mu` del risolutore.
- **La corsa:** lo stato fermo di `L 81`, il congelato vero, `10000` tick; ogni `10` tick la larghezza, il cuore, l'alone, il picco *(le grandezze di `_congelato_lungo.punto`)*; la lettura per finestre di `500`.
- **I controlli:** `T` deterministica; a `psi` piccolo il tick = `A(k)` di `9aa268c8` *(gia' controllato li')*; la norma dello stato fermo = `N` entro `1e-12`; i pezzi della corsa al bit; `M` entro `1e-10`.

## 3. LE LETTURE *(di Luca, scritte prima, senza soglie)*

- `(a)` lo stato fermo e' piu' largo dell'iniziale, piu' vicino al finale, e evoluto il cuore regge: lo svuotamento era l'assestamento di uno stato iniziale non fermo;
- `(b)` lo stato fermo esiste ma evoluto si svuota: l'instabilita' e' vera, VK sbaglia sul reticolo *(dove)*;
- `(c)` lo stato fermo non si trova con la norma data: che cosa succede;
- `(d)` altro, descritto.

## 4. LE MOTIVAZIONI

- Newton converge anche verso uno stato fermo instabile: la stabilita' la decide la corsa, non il metodo.

## 5. TODO

1. questo file, da solo;
2. `csv/_stato_fermo.py`, commit; `--cerca 81`, `--cerca 120`; `--pezzo` (5 volte); `--referto`; RELAZIONE; MAPPA; commit.

## 6. ANNOTAZIONE PRIMA DELLO SCRIPT *(le sezioni sopra restano come erano)*

| prova nello scratchpad *(non committata; i numeri li rifa' lo script)* | esito |
|---|---|
| Newton, GMRES senza precondizionatore, `30` passi | il residuo cala lento; GMRES non arriva alla sua tolleranza in nessun passo |
| lo stesso, GMRES piu' largo *(`restart 200`)* | GMRES ristagna |
| il precondizionatore `(A(k) - lambda)^{-1}` del tick libero *(`9aa268c8`)* | i primi passi rapidi; poi ristagna |
| il precondizionatore e la differenza centrata per `J v` | lo stesso pavimento: non e' la differenza finita |

- **Tutte le varianti si fermano fra `2e-6` e `6e-6`**, con `mu` fermo alla settima cifra; il criterio `1e-9` non si raggiunge.
- **Lo script usa la variante col precondizionatore e la differenza centrata**, `30` passi, lo stesso criterio.
- **Se il criterio non si raggiunge:** il confronto del punto `2` si fa sullo stato QUASI FERMO, dichiarato come tale; **la corsa del punto `3` non parte** *(`--pezzo` lo rifiuta)*: evolvere uno stato non fermo e' una decisione di Luca.

## 7. ANNOTAZIONE DOPO IL REFERTO *(`doc/referti_l2/stato_fermo.txt`; lo script `sha1-BYTE 444e371d`, `b61dea8e`; `12/12`)*

- **La sezione `6` va letta cosi':** le prove nella cartella di lavoro si erano fermate al passo `12` o prima; lo script, coi `30` passi del criterio, ha raggiunto `9.808e-10` *(`L 81`, `15` passi)* e `1.431e-10` *(`L 120`, `16` passi)*.

| `L 81` | `w/w_in` | il cuore `f_win` | il picco per nodo | distanza dal finale di `40061005` |
|---|---|---|---|---|
| lo stato iniziale *(l'inviluppo continuo)* | `1.0000` | `0.58583` | `5088` | `7.743e-02` |
| lo stato FERMO *(residuo `9.808e-10`)* | `0.9645` | `0.63001` | `5616` | `1.087e-01` |
| il finale di `40061005` *(tick `10000`)* | `1.3277` | `0.45858` | `3651` | `0` |

| la corsa dello stato fermo, finestre di `500` | `0`-`500` | `500`-`1000` | `1000`-`1500` | `1500`-`2000` | `2000`-`2500` | `2500`-`3000` |
|---|---|---|---|---|---|---|
| il cuore, dallo stato fermo | `0.630` -> `0.584` | -> `0.522` | -> `0.486` | -> `0.466` | -> `0.458` | -> `0.454` |
| il cuore, da `40061005` | `0.586` -> `0.551` | -> `0.511` | -> `0.489` | -> `0.480` | -> `0.459` | -> `0.459` |
| `w/w_in`, dallo stato fermo, alla fine della finestra | `1.055` | `1.176` | `1.246` | `1.285` | `1.309` | `1.331` |

| lettura *(di Luca, scritta prima)* | esito |
|---|---|
| (a) lo stato fermo piu' largo dell'iniziale, piu' vicino al finale, e evoluto regge | **NO:** e' piu' STRETTO *(`w/w_in 0.9645`, il cuore `0.630`)* e piu' lontano dal finale *(`0.109` contro `0.077`)* |
| (b) esiste ma evoluto si svuota | **SI':** il cuore `0.630` -> `0.454` a `3000`; gia' `-0.046` nella prima finestra. Un residuo di `1e-9` per tick, sommato linearmente, resta molti ordini sotto: lo scostamento CRESCE |
| (c) non si trova | no: si trova a `L 81` e `L 120`, `mu -0.532745112` a tutte e due |
| dove *(la saturazione del cuore, il margine `dN/dmu`)* | **non si separa da questi dati:** lo stato fermo ha il cuore piu' saturo dell'iniziale *(il picco `5616` contro `5088`)*; la corsa arriva allo stesso stato di `40061005` *(`w/w_in 1.331` contro `1.328`; il cuore `0.454` contro `0.459`)* |
