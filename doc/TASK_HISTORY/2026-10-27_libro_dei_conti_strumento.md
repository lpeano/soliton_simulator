# LO STRUMENTO DEL LIBRO DEI CONTI: LA STRADA `A` COME STRUMENTO, LA `B` COME DIAGNOSI, E I SIGILLI `(i)`-`(iv)` *(la parte 2 del mandato delle `12:54`; la scelta di Luca delle `13:46`)*

> **Il mandato:** ### **`doc/LIBRO_DEI_CONTI.md` e' scritto** *(`a4defef0`)*; ### **la scelta di Luca** *(`13:46`, inviata alle `16:05`; [[LIBRO-DEI-CONTI]])*: ### **la strada `A`** *(la corrente NETTA per anelli annidati, tick per tick: i tick in cui l'energia entra e quelli in cui esce, separati, e le loro somme)* ### **come strumento;** ### **la `B`** *(la variazione di ogni conto dopo ogni pezzo)* ### **come DIAGNOSI del va-e-vieni del passo contro i flussi;** ### **con `A` la quadratura e' sul TOTALE** *(la somma dei residui = `Delta H_tot`, entro l'errore del passo misurato a `s 0.3` e `0.15`)*. ### **I sigilli del mandato:** ### **`(i)` le correnti nulle sul vuoto uniforme;** ### **`(ii)` i bilanci per regione di `15df5c63`** *(`N 1e5`, `L 48`, lo zero simmetrico, il tick intero)* ### **entro `1e-6`;** ### **`(iii)` la quadratura;** ### **`(iv)` l'errore del passo come `s^2`** *(il rapporto `4` entro il `20%`)*. ### **Dopo: in `doc/PATTERN_DI_PROVA.md`, ogni misura d'energia usa lo strumento.**
> ### **Nessun file del nucleo.** ### **Lo strumento: `csv/_libro_dei_conti.py`** *(una libreria e, nel suo `main`, i sigilli)*.

**LIVELLO:** uno strumento e i suoi sigilli.

## 0. LA STELLA POLARE

1. **`A14`:** ### **l'energia e' cio' che si conta, conto per conto e regione per regione.** 2. **Il gradino:** ### **i flussi nei due versi nel tempo, non solo i saldi.** 3. **Aggiunge un numero o una legge?** ### **No.** 4. **Tocca `rho`, `c_s` o il segno?** ### **No.** 5. **Emergente o imposto?** ### **Nessuna fisica nuova.**

## 1. CHE COSA CREDO PRIMA DI GUARDARE, E CHE COSA NON SO

- ### **I CONTI PER NODO** ### **sono quelli di `_energia_del_legame.energie`** *(`per_nodo` con l'altro campo a zero; i costituenti `rho e_K(lambda)`; la cinetica per differenza; il legame `S1` = `Lambda F_1(rho/Lambda)`; il vuoto; `+ 2 pi lambda` per unita' di norma)*: ### **lo strumento li IMPORTA, non li copia** *(gli array per nodo prima della somma per regione)*, ### **e somma con `math.fsum`.** ### **Credo che `(ii)` passi a `1e-12` o meglio** *(le stesse funzioni; cambia solo l'ordine della somma)*.
- ### **LA STRADA `A`:** ### **dischi annidati di raggio `1, 2, 3, 4` volte `w_in`** *(`2 w_in` e' il VICINO di `15df5c63`)* ### **e il toro intero;** ### **per ogni disco e ogni tick il guadagno netto `Delta H_tot(disco)`:** ### **positivo = l'energia e' ENTRATA attraverso il bordo, negativo = USCITA** *(piu' la parte del residuo del passo che cade nel disco, che con `A` non si separa: il documento `(c)`, `(d)`)*. ### **Le somme dei tick in entrata e in uscita, separate, prima e dopo la vita.**
- ### **LA STRADA `B`:** ### **da una copia dello stato all'inizio del tick, `tick.percorri_tick(copia, ..., quanti = k)` per `k = 1 .. 14`** *(nessun secondo percorso del tick: il parametro `quanti` del nucleo)*; ### **`Delta_k E_R` = il conto dopo `k` pezzi meno dopo `k - 1`.** ### **IL VA-E-VIENI: `sum_k |Delta_k E_R|` contro `|Delta_tick E_R|`.** ### **Credo che sia molto piu' grande del saldo** *(ordine `s` contro ordine `s^2`: il documento `(c)`, riga `B`)*.
- ### ⚠ **`(iii)` CON `A` NON E' UN CONTROLLO INDIPENDENTE** *(il documento `(d)`)*: ### **la corrente netta e' DEFINITA dalla differenza.** ### **Il sigillo e' quindi:** ### **`(iii-a)` la partizione: la somma delle regioni = il totale** *(ogni conto, ogni tick campionato)*; ### **`(iii-b)` gli anelli** *(le differenze fra dischi consecutivi, piu' il fuori dell'ultimo)* ### **sommati = `Delta H_tot` del toro;** ### **`(iii-c)` `Delta H_tot` del toro sta dentro l'errore del passo misurato in `(iv)`** *(il massimo su `t <= vita` a `s 0.3`)*. ### **Lo dichiaro:** ### **`(iii-a)` e `(iii-b)` sono identita' dell'aritmetica, e `(iii-c)` e' la stessa grandezza di `(iv)`;** ### **cio' che `(iii)` prova e' che lo strumento non perde conti.**
- ### ⚠ **NON SO** ### **se `H_tot` col legame `S1` si conserva come un errore del passo `s^2`** *(`b04ec0d3` l'ha mostrato per i pezzi, non per `S1` sul solitone)*: ### **`(iv)` lo misura;** ### **se il rapporto non e' `4` il residuo non e' solo l'errore del passo, e mi FERMO.**
- ### ⚠ **NON SO** ### **se cambiare `s` cambia altro oltre a `mot.cs`** *(lo stato iniziale si costruisce a `s 0.3`; a `s 0.15` lo stesso stato con `mot.cs = 0.15` e il doppio dei tick)*: ### **lo controllo nella prova di costruzione** *(`mot.cs = 0.3` rimesso a mano deve ridare la corsa di riferimento al bit)*.

## 2. LA PROGETTAZIONE *(i sigilli fissati qui, prima dei numeri)*

| | il sigillo | il tipo |
|---|---|---|
| `(i)` | ### **il vuoto UNIFORME senza materia** *(la scena di `N 1e5` `L 48` con la materia a zero, lo zero simmetrico, `200` tick)*: ### **il guadagno netto di ogni disco a ogni tick entro `1e-12` volte `sum_k |e_tot,k|`** *(l'arrotondamento)* | DEVE |
| `(ii)` | ### **i conti per regione** *(vicino, lontano, totale; i costituenti, la cinetica, il legame, il vuoto, `H_tot`, `M`, `V`)* ### **= `energia_del_legame.jsonl`** *(`N 1e5` `L 48` simm intero)* ### **a ogni tick campionato fino a `T_MAX 2000`, entro `1e-6` di `N |e_K(0)|`** | DEVE |
| `(iii)` | ### **`(a)` la somma delle regioni = il totale, e `(b)` gli anelli sommati = `Delta H_tot`, entro `1e-12` di `N |e_K(0)|`** *(ogni conto, ogni tick campionato)*; ### **`(c)` `max_{t <= vita} |Delta H_tot|` = l'errore del passo a `s 0.3`** *(lo stesso numero di `(iv)`: un'identita', dichiarata)* | DEVE |
| `(iv)` | ### **l'errore del passo:** ### **`max |H_tot(t) - H_tot(0)|` sullo stesso tempo fisico** *(`s t <= 0.3 x 140`, la vita di `N 1e5`)* ### **a `s 0.3` e a `s 0.15`: il rapporto entro `4 +- 20%`** | DEVE |
| `(B)` | ### **la quadratura di `B`: dopo `14` pezzi la copia = il tick intero AL BIT** *(lo stato)* | DEVE |

- ### **LE LETTURE** *(nessuna soglia)*: ### **`A` sulla corsa di `(ii)`** *(`2000` tick)*: ### **per ogni disco le somme dei tick in entrata e in uscita, separate, prima e dopo la vita;** ### **il disco `2 w_in` e' la risposta alla domanda di `15df5c63`** *(dopo la rottura, il vuoto lontano rimanda energia dentro?)*; ### **`B` sui primi `200` tick ogni `10`:** ### **il va-e-vieni per conto e regione contro il saldo del tick e contro il flusso di `A`.**

### **Mi FERMO** ### **se un DEVE fallisce** *(la correzione e' un commit a se')*.

## 2-bis. ANNOTAZIONE, PRIMA DELLA CORSA *(la prova di costruzione: `T_MAX 60`, la vita `20`, `10` tick di vuoto, `20` di `B`; NON il referto)*

- ### **LETTO DAL CODICE, PRIMA DI `(iv)`:** ### **ogni pezzo legge il passo da `flussi_parziali.dtau_nodo = dtau cs`** *(l'accoppiamento `materia_vuoto.applica`, la camminata via `s_arco`/`z_arco`; il legame `S1` in memoria cambia solo `alpha`, `beta`)*, ### **e `energia_pesata.termini_di_h` NON dipende da `cs`:** ### **quindi `mot.cs = 0.15` col doppio dei tick e' un raffinamento dello STESSO flusso, e `H_tot` si misura allo stesso modo.**
- ### ⚠ **I NUMERI GIA' VISTI, DICHIARATI:** ### **`(i)` il guadagno massimo `4.4e-11` contro la soglia `4.3e-8`;** ### **`(ii)` `9.0e-17`;** ### **`(iii-a)` `6.2e-17`, `(iii-b)` `0`, `(iii-c)` uguali;** ### **`(B)` la copia = il tick al bit;** ### ⛔ **`(iv)` sul tempo fisico `6`** *(`20` tick a `0.3`, `40` a `0.15`)*: ### **la deviazione di `H_tot` `97.4` a `s 0.3` e `158.3` a `s 0.15`: il rapporto `0.62`, NON `4`.** ### **Il sigillo vero e' sul tempo fisico `42`:** ### **se fallisce anche li', `H_tot` col legame `S1` non si conserva come un errore del passo, e mi FERMO.** ### **La diagnosi `B` nella prova:** ### **in VICINO il va-e-vieni di `H_tot` e' `336` volte il saldo dei tick.**
- ### **LE SOGLIE NON CAMBIANO.**

## 3. TODO

1. questo task history, da solo; 2. lo script, committato prima della corsa; 3. la corsa; 4. il referto, la relazione, l'indice (`LIBRO-DEI-CONTI`); 5. `doc/PATTERN_DI_PROVA.md`: ogni misura d'energia usa lo strumento.
