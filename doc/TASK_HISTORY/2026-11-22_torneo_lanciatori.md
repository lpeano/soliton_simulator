# IL TORNEO DELLE FORME, IL PASSO 4 E LE TENUTE (5a): I LANCIATORI, LA SEMINA AL FONDO, LA CODA *(il mandato [M1631]; la carta `doc/CARTA_torneo_nonlinearita.md`, sez. 3, 6, 7 e 10)* [[PROGETTO-MITOSI]]

> **Scritto e committato PRIMA del codice.** Il nucleo con le forme: `90813637`, ricongelato in `e916efca`.

## 1. LE PREMESSE DAL CODICE *(cosa credo prima di guardare, e cosa NON so)*

- **La scena di tutte le misure** *(`triangolo_chi_v4.scena` -> `csv/solitone/mattone.scena`)* **tiene `materia_vuoto.pezzi` sostituito con le S1 di `csv/`** *(misurato: `doc/referti_l2/ripresa_F0_v2_prima.txt`)*: **il lanciatore rimette i `pezzi` del nucleo dentro la scena e sceglie la forma con `MV.forma_esplicita`**. A F0 i due percorsi sono uguali al bit *(misurato, un tick)*.
- **Il tick delle tenute e' quello di V0** *(`caduta_segno_v2.tick_var` con `N = 1`, `cs = s`, senza la fase (a): il tick U di oggi)*, la semina alla cima e' `caduta_libera.prepara` *(lo stampo `L162_MGU_03000`, un francobollo, nessun bordo)*: **la scena di tutte le misure di oggi.**
- **La risposta lineare attorno al vuoto non dipende da `lambda`** *(a `rho = 0` `alpha = 0` per Flambda)*: **l'autovettore del fondo e' lo stesso per tutte le Flambda**; per FH e FT no *(`alpha(0) = -1`, `tanh(-1)`)*, ma FH e FT si seminano alla cima.
- **La banda piu' bassa e' PIATTA** *(1a: `-0.4826761` a ogni `k`)*. ### ⚠ **QUESTO E' UN RISCHIO PER IL CRITERIO, e lo scrivo prima:** una sovrapposizione di stati di una banda piatta **non si allarga nemmeno senza non linearita'**: al fondo «regge» potrebbe essere **la banda piatta, non un solitone**. **Il controllo c'e' gia' nella lista:** `L0` *(nessuna non linearita')* **al fondo**: se `L0` regge al fondo, la tenuta al fondo NON distingue un solitone.
- **Non so:** se a Gamma, K, M la banda piu' bassa e' degenere con un'altra *(se lo e', la scelta dell'autovettore e' ambigua: lo stampo e FERMO su quel caso)*; se `K` sul toro `L 162` e' commensurato *(`162` e' multiplo di `3`: credo di si')*.

## 2. PROGETTAZIONE DEL RAGIONAMENTO

- **(P1) Gli autovettori del fondo:** il file nuovo `doc/referti_l2/torneo_fondo.py`: la risposta lineare di un tick *(le righe di `spettro_gap.bande`)*, `A(k)` a Gamma, K, M; l'autovettore della quasi-energia piu' bassa; **i DEVE:** l'energia `= -0.4826761` entro `1e-6` *(1a)*; il distacco dalla seconda `> 1e-6` *(non degenere)*; `k` commensurato col toro *(`e^{i k . L A_j} = 1`)*. Salva `v(k)` su `E:` *(il dato e' il comando)*.
- **(P2) Il lanciatore:** il file nuovo `doc/referti_l2/torneo_tenuta.py`, `corsa --forma F --semina cima|Gamma|K|M --fino 3000`; gli stati ogni `250` in `E:\soliton_simulator\controllo\M1631\tenuta\<F>_<semina>`. **La semina al fondo** *(sez. 10 della carta)*: `psi_h(x) = sqrt(rho_cima(x)) v(k) e^{i k . d(x)}`, `phi` quello della semina alla cima.
- **(P3) I controlli K1** *(`torneo_tenuta.py controlli`, PRIMA delle corse)*: `lambda = 1` *(costruita in memoria con `_forma_lambda(1.0)`)* **= S1 al bit, lo sha1 a `100` tick**; **il vuoto da solo** *(psi = 0)* **a `100` tick con ogni forma = F0 al bit**; ogni forma diversa da F0 **cambia** lo stato con la materia dopo un tick *(il caso che DEVE differire)*.
- **(P4) La lettura** *(`torneo_tenuta.py lettura`)*: per ogni corsa `w(500)`, `w(3000)`, il numero di pezzi connessi sopra il `10%` del picco; **K-T** come nella carta; **e il caso noto** *(F0 al fondo NON regge; F0 alla cima regge)*.
- **(P5) La coda:** `21` voci a priorita' `0` *(sez. 10)*, poi **[M1446-F2]** a priorita' `1` *(il suo codice e' un pezzo a se', dopo)*.
- **COSA MI FA FERMARE:** un autovettore degenere o un `k` non commensurato; un controllo K1 che fallisce *(F0 non al bit vuol dire che il lanciatore non e' la scena di oggi)*; `L0` al fondo che regge **non** mi ferma *(e' un risultato: lo dico per primo)*.

## 3. TODO DEL NEXT STEP

1. commit di questo file e della sez. 10 della carta;
2. `torneo_fondo.py`: commit, corsa, referto;
3. `torneo_tenuta.py`: commit; `controlli`, referto;
4. le `21` voci nella coda, il dispatcher rilanciato;
5. il codice di [M1446-F2] *(definizioni gia' nella carta di E=mc2, sez. F2)*, le sue voci a priorita' `1`;
6. a corse chiuse: `lettura`, la tabella del torneo (colonna «regge»), poi 5b-5f.
