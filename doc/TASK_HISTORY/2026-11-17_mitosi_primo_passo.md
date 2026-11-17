# R-QUALITA', IL FILO IN SOSPESO, LA MITOSI PRIMO PASSO *(il mandato unico di Luca `2026-11-17` `09:49`)*

> **Il mandato:** **(0)** la regola R-QUALITA' nella ROTTA; **(A, B)** il filo della ricerca e il censimento nel documento `doc/SOSPESO_2026-11-17_FILO_DELLA_RICERCA.md`; **(C1)** le decisioni della mitosi nell'albero e nell'indice; **(C2)** la prova della simmetria C di G+U; **(C3)** la carta della mitosi `doc/MITOSI_era2_carta.md`; **FERMO.** **Nessun file del nucleo; nessuna corsa lunga; nessun file o stato cancellato; ogni numero dal referto citato** *(se non torna: accanto, e nel commit)*.
> **L'ordine dei mandati** *(PRECEDENZA-IN-CODA)*: **questo SOSTITUISCE quello delle `09:20`**, che e' gia' eseguito *(`980f5f5e`)*: **A e B coincidono con le parti `1`-`7` del documento** *(A1-A5 = parti `1`-`3`, `5`, `6`; B1-B6 = parte `7`)*.

## 1. LE PREMESSE DAL CODICE *(cosa credo prima di guardare; cosa NON so)*

- **A e B sono fatte** *(`980f5f5e`)*, **tranne B4: le considerazioni delle `11:47` del `2026-11-16`.** **Il testo di quel mandato non e' nel repo ne' nelle trascrizioni delle mie sessioni** *(cercato il `2026-11-17`; la carta `2026-11-17_sospeso_filo.md`, sez. `4`)*. **Il mandato di oggi lo richiede di nuovo «col testo di quel mandato»: senza il testo NON si scrive** *(Q-A1, che questo stesso mandato introduce)*. **Resta aperto, nel messaggio finale.**
- **L'albero** *(`doc/ALBERO_era2.yaml`, letto oggi)*: **QC (`DEC-QC-CONSERVATA`) e' GIA' `presa: true`** *(Luca `2026-10-16`: la norma della materia e la norma del vuoto esattamente; l'energia al secondo ordine)*; **D6f (`DEC-D6F-FORME-VUOTO`) e' GIA' `presa: true`**; **FC (`DEC-FC-COESIONE`) `presa: false`** *(dipende da QC)*; **D7 (`DEC-D7-DIVISIONE`) `presa: false`, dipende da D6f e FC** *(e la scelta di Luca del `2026-10-26`, «la via (3)», la tiene non presa per la parte del VUOTO: con D7 applicata a `phi` la nascita libera `8.548` e il vuoto uniforme non la assorbe, `d999cca7`)*; **D9 (`DEC-D9-GEOMETRIA`) `presa: false`**; **la decisione `10`** *(il calore paga la nascita, la soglia e' il bilancio)* **NON e' un nodo: e' citata come PRESA in `3e8375b6`.**
- ### **QUINDI C1 NON PRENDE NESSUNA DECISIONE NUOVA, tranne FC con la sua condizione.** **Cio' che scrivo:** il CONTENUTO del guardiano nelle note dei nodi *(QC: la carica di U accanto alla norma; D6f: le forme di oggi; D7: i tre vincoli e dove nasce; D9: la via (B) e la coerenza col tempo)*; **FC: presa SOLO se C2 passa.** ### **D7 NON la porto a presa anche se FC passa:** il motivo di Luca del `2026-10-26` *(la parte del vuoto)* **non dipende da C2**: **lo scrivo, e la via e' sua.**
- **Le voci dell'indice:** `COESIONE-TERMINE-O-CAMPO` e `PROPOSTA-FASE-DISPARI-COESIONE` **a `SUPERATA` col perche'** *(il mandato: «scritto perche', non cancellate»)*, **con `python csv/indice.py aggiorna`** -- **NON so ancora** se lo strumento accetta `SUPERATA` senza `superata_da`: si vede al primo comando.
- **C2, l'operatore** *(dal codice, `csv/solitone/mattone.py`, `Campi.tick`; `doc/referti_l2/mattone/specchio_carta.py`)*: **lo stato e' `psi_h` `(6n, 2)`** *(uno spinore a `2` componenti per estremita': le «`12` componenti» di un nodo sono `6` estremita' x `2`)*, **`phi_h` `(6n,)`, `campo_A` e `campo_E` per arco `(3n,)`.** **C:** `psi_h -> T conj(psi_h)` per estremita' *(nessuna permutazione dei nodi)*, `A -> s A`, `E -> s E`, `phi_h -> f(phi_h)`, il lapse invariato.
- ### **TRE COSE CHE IL CODICE MI DICE PRIMA DEI NUMERI:**
  1. **IL BORDO ROMPE C PER COSTRUZIONE:** **la correzione del bordo** *(`self.campo.E += gauss(e * drho)`)* **non cambia segno con `E`, e `BO.assorbi` tira verso il vuoto di riferimento `phi_v`, che C non trasforma.** **Il confronto vero e' ENTRO `40` nodi dal mattone** *(lontano dal bordo, come lo specchio)*; **sul toro intero si stampa, ma non decide.**
  2. **GAUSS:** `Campi.residuo` misura `div E - e (rho - media)`; **con `E -> -E` e `rho` invariato lo stato coniugato NON soddisfa piu' Gauss con carica `+e`**: **lo soddisfa con carica `-e`** -- che e' esattamente cio' che C deve fare *(la carica cambia segno)*. **La dinamica nel tick** *(se fa solo Ampere, `E` col segno della corrente)* **lo porta avanti coerente.** **Lo dichiaro: la prova misura la COMMUTAZIONE, non il residuo di Gauss del coniugato.** **NON so** se `PBR.tick_GU` risolve Gauss dentro il tick con `e (rho - media)`: **se lo fa, C con `E -> -E` si rompe in quel termine, e la lettura lo dira'** *(e il candidato giusto sarebbe con `e -> -e`)*.
  3. **I TERMINI NON LINEARI:** **una fase non lineare `exp(-i N dt)` coniugata diventa `exp(+i N dt)`**: **commuta con C solo se `N` e' DISPARI sotto C** *(e' la storia di `PROPOSTA-FASE-DISPARI-COESIONE`: la fase pari rompe C di `1e-1`)*. **Se il nucleo ha un termine di fase PARI** *(funzione di `rho` o di `Lambda`)*, **C NON commuta, e la previsione del guardiano cade.** **Non so dal solo codice letto se ce n'e' uno nel tick di G+U: e' la domanda che la prova fa.**

## 2. PROGETTAZIONE DEL RAGIONAMENTO

### 2.1 Parte 0 -- R-QUALITA' nella ROTTA *(il testo del guardiano, una sezione nuova, permanente)*.

### 2.2 C1 -- le note e le voci *(i numeri del guardiano controllati: se non tornano, accanto)*; **FC con la condizione**; **P-ALB deve passare** *(`python csv/indice.py valida`)*.

### 2.3 C2 -- LA PROVA DELLA SIMMETRIA C *(lo script `doc/referti_l2/simmetria_C.py`, sul modello di `specchio_carta.py`; il referto `doc/referti_l2/simmetria_C.txt`)*

- **I CANDIDATI** *(quanti e quali, scritti PRIMA)*: **`T` in `{I, sigma_x, sigma_y, sigma_z}`** *(`sigma_x` e' quello di `PROPOSTA-FASE-DISPARI-COESIONE`)*, **`psi_h` sempre coniugato** *(C e' antiunitaria)*; **`phi_h` in `{phi, -phi, conj(phi), -conj(phi)}`**; **`(A, E)` per `+1` o `-1`**: **`4 x 4 x 2 = 32` candidati.**
- **Q-A4, IL CASO NOTO, prima:** **(K1) C due volte = l'identita'** sullo stato del mattone *(al bit per `I`, `sigma_x`, `sigma_z`; `sigma_y` da' `-1`, una fase globale: dichiarato)*; **(K2) il vortice `+1` costruito a mano** *(come `segni_vortice.py`, `eebb2f39`)* **coniugato da' il giro della somma `-1`, L dalla corrente di fase col segno opposto.** **DEVE FALLIRE:** il vortice **NON** coniugato *(T = I senza coniugio)* **ha il giro `+1`, non `-1`.**
- **LA PROVA:** **dal mattone `L162_MGU_03000`** *(la scena S162, `MT.scena(MT.CORSA_162, MT.T_162)`, i campi `MGU` col lapse pieno, `e = PB.E_DECISO`)* **e da UNO STATO A CASO** *(seme `11`: `psi_h` del mattone con una fase casuale per estremita' e componente; `A`, `E` del mattone piu' un rumore `1e-3` del loro massimo; `phi_h` della scena)*: **`C(tick^N(x))` contro `tick^N(C(x))`**; **`1` tick per tutti i `32`, `10` tick per i due migliori**; **la differenza relativa per chiave** *(`psi_h`, `phi_h`, `A`, `E`)* **entro `40` nodi dal centro del mattone e sul toro intero.**
- ### **LA PREVISIONE DEL GUARDIANO** *(scritta prima)*: **G+U commuta con C entro l'arrotondamento: sotto `1e-12` dopo `10` tick** *(entro `40` nodi)*. ### **LA MIA, accanto** *(dal codice, sez. `1`)*: **non so se c'e' un termine di fase pari; se c'e', C cade, e la prova dice di quanto e in quale chiave.**
- **LA LETTURA** *(fissata prima)*: **C ESISTE se il migliore dei candidati, dopo `10` tick, sta sotto `1e-12` entro `40` nodi PER ENTRAMBI gli stati.** **Se cade:** quale chiave rompe per prima *(dopo `1` tick)*, e di quanto; **un secondo passo diagnostico** *(se serve)*: lo stesso confronto col solo **MU** *(la U(1) senza il lapse)* **e col solo MG** *(il lapse senza la U(1))*, **per dire quale meta' del tick rompe.**
- **FC presa o no:** **presa se C esiste; se no, aperta col perche'.**

### 2.4 C3 -- la carta della mitosi *(solo carta; i fatti dal codice raccolti da un agente in sola lettura e ricontrollati da me sul sorgente)*.

- **Cosa mi farebbe FERMARE:** un caso noto che non passa *(l'operatore e' sbagliato: niente prova)*; **una prova che passa per costruzione** *(FALSO-UNO: per esempio uno stato senza U, dove `A -> -A` non conta)* -- **per questo lo stato a caso ha `A` ed `E` non nulli.**

## 3. TODO DEL NEXT STEP

1. questa carta: commit e push;
2. la Parte 0 nella ROTTA: commit;
3. una riga nel documento SOSPESO *(il mandato unico lo riprende; B4 ancora senza testo)*: con la Parte 0;
4. C1 nelle note dell'albero e nell'indice; `valida`; commit;
5. C2: lo script, commit; la corsa *(breve, una «breve» nel registro)*; il referto; FC; commit;
6. C3: la carta; commit;
7. **FERMO per Luca.**
