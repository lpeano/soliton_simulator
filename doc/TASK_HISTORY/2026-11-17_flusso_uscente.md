# FC COL RICALCOLO DELLE CACHE; L'ENERGIA DELLA NASCITA DENTRO E FUORI; IL CALORE E' IL FLUSSO USCENTE *(il mandato unico di Luca `2026-11-17` `14:27`)*

> **Il mandato:** **(1)** le tre cache ricalcolate dopo la trasformazione: se tornano, FC presa *(decisione di Luca `14:23`)*; **(2)** l'energia della nascita per anello dentro e fuori dalla materia, scomposta per termine, il confine misurato, le nascite in fila, con U, sul triangolo e sulla coppia; **(3)** il calore = il FLUSSO USCENTE di energia *(le decisioni di Luca `14:23`-`14:27`: lo spazio cresce VICINO alla materia ma FUORI; la crescita e' CONTINUA; paga cio' che ESCE dalla materia)*: la definizione col caso noto, il flusso nel tempo, l'accumulo, l'esaurimento; **(4)** la carta della mitosi; **FERMO.** **Nessun file del nucleo; solo letture e copie.**

## 1. LE PREMESSE DAL CODICE *(cosa credo; cosa NON so)*

- **(1) Le cache** *(letto il `2026-11-17`)*: `motore.elicita` riscrive `h_int` *(`h.fill(0)`, poi la somma di `s.n` per nodo)*; `motore.densita_materia` riscrive `rho`, `motore.densita_vuoto` riscrive `Lambda`. **Il ricalcolo:** sui due lati della prova di `45568f37` *(`Q^N(Theta(Q^N(x)))` e `Theta(x)`)* **si chiamano le tre funzioni del nucleo sullo stato finale**; **mi aspetto l'arrotondamento** *(sono funzioni dello stato dinamico, che coincide entro `3e-14`)* -- **TRANNE `h_int`, che NON e' detto sia invariante:** **`h_int = s . n`, e sotto `Theta` lo spin `s` cambia segno** *(`sigma_y` e il coniugio: il rovesciamento del tempo)* **e i versori `n` dell'inversione anche nel piano** *(la componente `z` no)*. **Se `h_int` dello stato trasformato e' `-h_int` permutato, il confronto giusto e' fra i RICALCOLATI** *(come il mandato chiede)*, **non fra il ricalcolato e il permutato.** **Lo stampo comunque.**
- **(2) La mossa in fila:** `_conto_del_vuoto.nascita` divide **un solo arco fisso** *(`(L/2, L/2) -> +(1,0)`)* **sul toro REGOLARE** *(`_massa_nei_difetti.sdoppia` ricostruisce la topologia da `toro(L)`)*: **le nascite in fila sul grafo che cresce NON si possono fare con quello strumento.** **Scrivo una divisione d'arco GENERICA** *(sul grafo qualunque: i due vertici opposti `k`, `l` = i vicini comuni di `i` e `j`; le posizioni dei nodi tenute a parte, il nodo nuovo al punto medio)* **con la STESSA regola di `nascita`** *(il trasporto delle estremita' dell'arco tolto, D7 sul padre `i`, le estremita' nuove in `k` e `l` a `0`)* **e v4-F3** *(`divisione_vuoto_F3.py`)*. ### **Il caso noto:** **la prima nascita generica = `nascita` di `_conto_del_vuoto` AL BIT** *(`Delta H` e le parti)*.
  - **«L'arco nuovo piu' teso del vicinato»:** **la mia definizione, scritta:** fra gli archi del nodo nato per ultimo, quello col termine d'arco del vuoto `T(a)` piu' alto *(meno negativo)*; **a pari merito l'indice d'arco piu' basso** *(deterministico; NON simmetrico allo specchio: dichiarato, e' una diagnosi)*.
  - **Con U** *(2.4)*: **la carta di `c0bc999e`, sez. `2`**: **l'arco tolto `i -> j` porta `A_a`; `A(n -> j) = A_a/2`, `A(n -> i) = -A_a/2`** *(il cammino `i -> n -> j` porta `A_a`)*; **`A(n -> k)` e `A(n -> l)` perche' ciascuno dei due triangoli vecchi si divida in due META' di flusso**; **`E` sugli archi nuovi da Gauss VERO** *(il laplaciano del grafo nuovo, `div E = e (rho - media)`)*. **Nel conto entra `U = e^{i A}`** *(`_u1_prototipo.scrivi_U`: `U[:,0,0] = U[:,1,1] = campo.u()`)* **e l'energia del campo `E^2/2`**; **l'energia di `B` sui triangoli divisi NON la conto** *(serve la normalizzazione delle placchette di `Campo`: dichiarato)*.
  - **Il motore del conto:** `_conto_del_vuoto.motore` *(`cs` spento, `PAR = {eps: 0}`: la moneta non entra)*; **i termini per famiglia come in `soglia_nascita.py`.**
- **(3) Il flusso:** **`energia.corrente(st, mot, par, None)`** *(letto)*: **`J[k]` e' l'energia che lo SPOSTAMENTO DELLA MATERIA porta sull'arco `k`, positiva da `ii` a `jj`** *(dopo la moneta e il Grover, col trasporto `U`)*: **e' la corrente di energia della MATERIA**; **quella del vuoto non c'e'** *(dichiarato)*. **Il flusso uscente attraverso l'anello `R`:** sugli archi che lo attraversano *(un capo dentro, uno fuori, dal baricentro della materia)*, `J` col segno del verso uscente; **solo la parte positiva conta** *(il mandato)*; accanto il netto.
  - **Gli stati di `L 186`** *(la fase `0`, `E:/soliton_simulator/mattone/scatola5_L186_*.npz`)*: **SOLO SEI: `k 950, 1000, 1950, 2000, 2950, 3000`**: **il flusso «nel tempo» e' su sei istanti**, e **l'accumulo e' un INTEGRALE APPROSSIMATO** *(il trapezio fra gli istanti: dichiarato)*. **La scena:** `convergenza.scena_L(186, R_A)` e `prova_scatola5.carica` *(i campi A ed E salvati)*.

## 2. LE PREVISIONI DEL GUARDIANO *(copiate dal mandato, PRIMA delle parti 2-3)*

- **P-E1:** il termine della materia scende sotto l'`1%` del `Delta H` entro `1.5` raggi della materia *(circa `19` nodi)*.
- **P-E2:** le nascite in fila all'anello del confine cambiano segno entro `20` *(la crescita si frena da sola)*.
- **P-E3:** il flusso uscente e' positivo a tutti gli anelli `15`-`45` attorno al mattone e non si esaurisce entro `3000` tick *(cala meno della meta')*.
- **P-E4:** nel vuoto F3 puro il flusso uscente e' `0` all'arrotondamento.
- ### **LE MIE, accanto** *(dai numeri gia' nel repo)*: **P-E1:** all'anello `59.81` la materia vale `-2.70e-03` su `+17.26`, lo `0.016%`; all'anello `13.81` il `101%`: **il confine c'e', e il guardiano lo mette a `19` nodi: lo credo fra `20` e `30`** *(R_ogg al `5%` del mattone e' `25`)*. **P-E4:** **vero per costruzione se `psi = 0`** *(`J` e' della materia)*: **un FALSO-ZERO** -- **lo scrivo come tale** *(la prova non puo' fallire)*. **P-E3:** **non lo so**; **la massa che il bordo assorbe** *(la fase `0`: `oltre R_A` piccolo)* **dice che qualcosa esce, ma `J` e' energia, non massa.**

## 3. PROGETTAZIONE DEL RAGIONAMENTO

1. **Parte 1:** lo script `simmetria_CPT_cache.py` *(come `simmetria_CPT.py`, `N = 10` e `100`, i due stati; i ricalcolati sui due lati)*; **la lettura:** le tre cache ricalcolate entro `1e-12` relativo *(e `h_int` col suo segno, stampato)*: **FC presa** *(la nota nell'albero, `presa: true`, `valida`)*; **se no, FERMO.**
2. **Parte 2:** lo script `nascita_dentro_fuori.py` *(il caso noto prima)*.
3. **Parte 3:** lo script `flusso_uscente.py` *(il caso noto: un pacchetto che si allontana da un punto da' flusso uscente positivo, uno che si avvicina negativo)*.
4. **Parte 4:** la carta della mitosi, sez. `11`; **FERMO.**

## 4. TODO DEL NEXT STEP

1. questa carta *(con le previsioni)*: commit;
2. la parte 1: lo script, la corsa, il referto, FC; commit;
3. la parte 2 e la parte 3: gli script *(commit)*, le corse, i referti; commit;
4. la carta; commit; **FERMO.**

## 5. L'ESITO *(e le annotazioni alle premesse)*

- **Parte 1** *(`simmetria_CPT_cache.txt`)*: **PASSA**: le cache ricalcolate sui due lati coincidono *(`h_int` `<= 3.8e-14`, `rho` `<= 1.5e-14`, `Lambda` `<= 3.1e-14`)*, la dinamica come in `45568f37` *(il peggiore E `2.817e-12` a `N = 100`)*. **ANNOTAZIONE alla premessa (1):** **`h_int` NON cambia segno sotto `Theta`** *(il ricalcolato sul trasformato = il permutato a `3.2e-16`; contro il permutato col segno meno `2.0`)*: **lo spin e i versori cambiano segno insieme.** **FC PRESA** *(la decisione di Luca delle `14:23`)*.
- **Parte 2** *(`nascita_dentro_fuori.txt`)*: **il caso noto al bit**; **il confine a `23.81` nodi = `1.92` raggi della materia**; dentro negativo *(la materia)*, fuori positivo *(il vuoto)*; **in fila al confine nessun cambio di segno; a `13.81` uno solo** *(la `15`a)*; **con U cambia alla quarta cifra.** **P-E1 e P-E2 CADONO.**
- **Parte 3** *(`flusso_uscente.txt`)*: **il caso noto passa** *(e mostra l'onda all'indietro: il pacchetto con la fase verso fuori va dentro)*; **il flusso uscente positivo a `15`-`45`, non si esaurisce** *(P-E3 regge)*; **P-E4 vera per costruzione** *(falso zero, dichiarato prima)*; **l'accumulo: il primo arco dopo circa `2515` tick, `0.50` nascite per tick al ritmo medio** -- **un MASSIMO** *(la parte positiva raddrizza le oscillazioni)*.
- **Parte 4:** la carta della mitosi, sez. `11`; **FERMO.**
