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
