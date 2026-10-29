# 2026-10-29 — IL MENU PER LA DECISIONE SULLE BANDE PIATTE *(SULLA CARTA E DAL CODICE; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il mandato di Luca delle `19:12`, dopo `99b679bc`)*

> **LIVELLO:** conti sul tick libero, in `csv/`; nessuna corsa lunga; nessun file del nucleo. Il documento `doc/BANDE_PIATTE.md` **non sceglie**.

## 1. LE PREMESSE DAL CODICE

### Il tick libero della materia

| che cosa | dove | il fatto |
|---|---|---|
| l'ordine | `primo_ordine/composizione.ORDINE` | `14` pezzi, palindromo; sulla materia: legame, moneta, Grover, spostamento, *(i pezzi del vuoto)*, spostamento, Grover, moneta, legame, ciascuno a `0.5` |
| i pezzi del vuoto | `_solitone_vuoto_congelato.VUOTO` | `CAMM-GROVER-VUOTO`, `CAMM-SPOSTAMENTO-VUOTO`, `CAMM-FASE-VUOTO`: saltati nel tick congelato; agiscono su `phi`, non su `psi` |
| **la moneta** | `_solitone_vuoto_congelato.corsa`, `par["eps"] = 0.0` | **in tutte le scene di `S1` misurate fin qui `eps = 0`: la moneta e' l'identita'** *(la tabella ha `eps 0.5`)* |
| la convenzione | `_triangoli_bassa_energia.conv("simm")` -> `_zero_simmetrico.convenzione_simmetrica` | gli strumenti usano i pezzi a fase `±theta/2` *(`exp(i theta (I - 2P)/2)`)*; il nucleo usa `0` e `theta`: **una fase globale per pezzo, uguale su tutte le bande** |
| Grover | `motore._grover`, `flussi_parziali.grover` | `G(theta) = P_u + e^{i theta}(I - P_u)`, `theta = pi dtau_nodo/dtau_rif`; `P_u` il vettore uniforme sulle `6` estremita' del nodo, per componente di spin |
| spostamento | `CAMM-SPOSTAMENTO` | `exp(i theta P-)`, `S_U` hermitiana e unitaria sull'arco; `theta = pi dtau_arco/dtau_rif`, `dtau_arco` = la media armonica dei due nodi |
| le componenti | `psi_h` `(6n, 2)` -> `(n, 12)` | `12` = `6` estremita' x `2` spin; a `eps 0` e `U = I` il tick e' `W_su (+) W_giu` *(`doc/PROGETTO_U1.md`)* |

### Una prova esplorativa *(non salvata; `L 81`, `s 0.3`; una copia temporanea in `csv/`, cancellata)*

- il tick ricostruito dai pezzi singoli *(`percorri_tick` con `salta` e `quanti`)* = `A(k)` entro `4.6e-16`;
- la moneta a `eps 0`: tutte le fasi `0`; il mezzo Grover: `±pi/4` per unita' di tempo *(`2` e `10` stati per `k`)*; il mezzo spostamento: `±pi/4` *(`6` e `6`)*;
- le bande per unita' di tempo: `Ppi` `-pi` e `P0` `0` **piatte su tutta la zona**; `A` in `[-pi, -1.5266]`, `B` in `[+1.5266, +pi]`: **`A` tocca `Ppi` a `Gamma`, `P0` e' isolata**;
- `E(k) = E(-k)` entro `5.1e-15`; lo spettro intero **non** e' simmetrico rispetto a `-pi/2` *(lo scarto `1.57`)*.

### Il conto sulla carta *(primo ordine in `s`, la convenzione `simm`; da verificare nello script)*

- **Il generatore:** `H1 = (alpha/2)(2 P_u - I) + (beta/2) R_S`, `alpha` e `beta` gli angoli per unita' di tempo del nodo e dell'arco *(oggi `alpha = beta = pi`)*, `R_S` la riflessione dello spostamento.
- **Su `ker P_u`:** `E = (-alpha ± beta)/2` -> **le piatte** `0` e `-pi`.
- **Su `span(u, R_S u)`:** `E = ±(1/2) sqrt(alpha^2 + 2 alpha beta c(k) + beta^2)`, `c(k)` l'autovalore di `P_u R_S P_u`; **le bande `A` e `B`, speculari rispetto a `0`.**
- **A `K`:** `c = -1/2` *(il fattore di struttura del triangolo)* -> `E_A(K) = -mu0`, `mu0 = (1/2) sqrt(alpha^2 - alpha beta + beta^2)` *(la formula del guardiano, `2026-10-25_curvatura_parte2.md`)*.
- **Il punto di mezzo** `E_A(K) = -alpha/2` vale **se e solo se `beta = alpha`** *(`r = 1`: `dtau` uniforme)*. **Non e' una simmetria dello spettro:** e' `r = 1` piu' `c(K) = -1/2`.
- **Lo scarto della coppia nel tick libero:** `E_P0 + E_Ppi - 2 E_A(K) = -alpha + 2 mu0` = **`0` a `r = 1`**: la coppia `P0+Ppi` e' **esattamente** alla soglia di due quanti di `A` a `K`; lo scarto misurato *(`-0.00955` a `s 0.15`)* e' `-2 (mu - E_A(K))` piu' `O(s^2)`.
- **Il palindromo** rende lo scarto da `-pi/2` di ordine `s^2` *(`de411167`: i rapporti `0.2475`, `0.2494`, `0.2498`)*.

### Le premesse di Luca, lette contro i referti

- «si spegne fra `+0.4` e `+0.8`»: il punto `+0.8` e' **una piatta sola**; nella stessa direzione il modo c'e' a `+0.4` ed e' spento a `+1.6` *(`99b679bc`)*. Con `k1` le due letture coincidono.
- «banda `A`, anelli `6`-`9`»: e' cosi' a `-0.4` e con una piatta sola; a `+1.6` gli anelli `3`-`6`.

### Cosa NON so

- se le piatte hanno stati compatti, e su quanti nodi;
- quanto spostano le piatte la moneta a `eps 0.5` e un altro ordine dei pezzi;
- per il punto `2`: dove ogni grandezza dipende da `r = 1`, oltre a cio' che dicono i referti citati.

## 2. I CRITERI

- **Lo script** `csv/_bande_piatte.py --referto`: `S1`, `L 81`, il tick libero di `_dove_va_la_materia` *(`AMP 1e-6`)*; nessuna corsa.
- **(1) LA SIMMETRIA DEL PUNTO DI MEZZO**, a `s 0.3`, `0.15`, `0.075`:
  - i pezzi singoli e la ricostruzione *(DEVE `< 1e-12`)*; `P_u` e `R_S` dai mezzi pezzi *(gli autospazi a `+pi/4`)*; `c(k)` per ogni `k`;
  - `A` e `B` contro la formula del primo ordine: lo scarto massimo sulla zona, e il rapporto fra due `s` *(`~4`: `s^2`)*;
  - `c(K)`, `c(K')`, il minimo di `c` sulla zona; `E_A(K) + pi/2`, `E_A(K') + pi/2`;
  - le tre prove di simmetria dello spettro, per `k` e per `-k`: `E -> -E` *(con le piatte e senza)*; `E -> -pi - E`; `A(k)` contro `-B(k)`;
  - lo scarto libero `E_P0 + E_Ppi - 2 E_A(K)` per unita' di tempo, contro `0`.
- **(2) CHE COSA TOCCA:**
  - `Q_S`: `||[A(k), sigma_z]||` a `eps 0` e a `eps 0.5` *(la moneta dal pezzo del codice con `par["eps"] = 0.5`)*;
  - `K` e `K'`: gli stessi conti nelle due valli;
  - `DOMANDA-CHIRALITA` e il cono di `C2`: **dai referti, sulla carta**, nel documento.
- **(3) GLI STATI COMPATTI:** per `P0` *(`E = 0`)* e `Ppi` *(`E = -pi`)* a `s 0.15`: i vettori supportati su un grappolo di nodi *(`1`, il triangolo `3`, il rombo `4`, l'esagono `6`, l'esagono col centro `7`, due anelli `19`)* con `T v = lambda v` esatto *(lo spazio nullo, la soglia `1e-10` sul valore singolare relativo)*; il grappolo minimo e quanti stati; **il rango delle traslazioni**: per ogni `k`, la dimensione dello spazio generato dalle trasformate dei compatti, contro `4`; i `k` dove manca.
- **(4) LA STRADA (B), sul tick libero modificato in `csv/`** *(`T = M G(alpha) S(beta) S(beta) G(alpha) M`, dai generatori per `k`; DEVE: `alpha = beta = pi` ridà `A(k)` entro `1e-10`)*, a `s 0.15`:
  - **(B1) il rapporto nodo/arco:** `alpha` e `beta` con `mu0 = pi/2` fisso *(la famiglia `alpha^2 - alpha beta + beta^2 = pi^2`)*, lo scarto libero a `+0.8` e a `-0.4`; `E_A(K)`, la curvatura di `A` a `K`, le piatte;
  - **(B2) la moneta della tabella** *(`eps 0.5`)*: le piatte *(ancora piatte? la larghezza)*, `E_A(K)`, lo scarto libero;
  - **(B3) un altro ordine palindromo** *(`S G M M G S`, `G M S S M G`)*: lo scarto libero a `s 0.15` e `0.075`;
  - **(B4) la convenzione** *(`oggi` contro `simm`)*: lo scarto libero.
- **DEVE:** la ricostruzione; `alpha = beta = pi` ridà `A(k)`; il primo ordine entro `O(s^2)` *(il rapporto fra `s 0.15` e `s 0.075` fra `3` e `5`)*.

## 3. LE LETTURE *(di Luca, scritte prima, senza soglie)*

- per ciascun punto, il fatto trovato;
- per la strada `(B)`: quante modifiche minime esistono, e il loro costo nel punto `2`.

## 4. LE MOTIVAZIONI

- La decisione di Luca fra `(A)`, `(B)`, `(C)`, dopo `99b679bc`: la risonanza si spegne spostando la somma delle due piatte.

## 5. TODO

1. questo file, DA SOLO, e aspettare il push;
2. `csv/_bande_piatte.py`, la voce d'inventario, commit;
3. `--referto` -> `doc/referti_l2/bande_piatte.txt`;
4. `doc/BANDE_PIATTE.md` *(i quattro punti, le tre strade col costo; non sceglie)*; RELAZIONE; MAPPA *(la riga `d`; le due voci della lista d'attesa)*; questo file annotato; commit.

## 6. ANNOTAZIONE DOPO IL REFERTO *(`doc/referti_l2/bande_piatte.txt`; lo script `sha1-BYTE 3d62588b`, `919b610a`; `5/5`; il documento `doc/BANDE_PIATTE.md`)*

| punto | il fatto *(`doc/referti_l2/bande_piatte.txt`, `5/5`)* |
|---|---|
| (1) il punto di mezzo | **non e' una simmetria dello spettro** *(`E -> -pi - E` scarta `3.14`)*; **e' `r = 1` piu' `c(K) = -1/2`**: le piatte `(-alpha ± beta)/2`, `A` e `B` = `∓(1/2) sqrt(alpha^2 + 2 alpha beta c + beta^2)`, entro `O(s^2)` *(i rapporti `4.07`, `4.02`)*; valgono `E(k) = E(-k)` e `A(k) = -B(k)` *(`≤ 1.9e-14`)*; **lo scarto libero della coppia e' zero al primo ordine** *(`-0.0219` a `s 0.15`, `O(s^2)`)* |
| (2) che cosa tocca | `Q_S`: no *(`[T, sigma_z]` `0` a `eps 0`, `1.46e-1` a `eps 0.5`)*; `K`/`K'`: si', uguali; `DOMANDA-CHIRALITA` `(b)` *(`mu0`)*: si'; il cono di `C2`: si', attraverso `r` |
| (3) gli stati compatti | `P0` e `Ppi` su un triangolo *(`2` e `4` stati)*; `P0`: le traslazioni generano la banda a ogni `k` *(un proiettore locale)*; `Ppi`: a `Gamma` mancano `2` stati *(tocca `A`)* |
| (4) la strada (B) | **una famiglia sola, `(B1)` il rapporto nodo/arco**: `+0.806` *(`r 1.5247`)* e `-0.395` *(`r 0.6920`)*, `A(K)` entro `3.1e-3`, **un numero nuovo**; `(B2)` `eps 0.5`: `+0.161`, sposta `A` di `-0.080`, rompe `Q_S`; `(B3)` un altro ordine e `(B4)` la convenzione: `0` |

- **Il conto sulla carta della sezione 1 regge:** il primo ordine e lo scarto libero zero a `r = 1`.
- **La prova a vuoto** *(una copia temporanea, prima del commit dello script)* aveva il rango di `P0` dal grappolo minimo *(`2` a ogni `k`)*; lo script committato lo prende dal grappolo piu' grande.
