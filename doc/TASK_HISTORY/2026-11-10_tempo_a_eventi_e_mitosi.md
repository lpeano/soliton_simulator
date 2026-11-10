# IL TEMPO A EVENTI E LA MITOSI: L'ANALISI DEL `2026-11-10` *(Luca `14:05`-`14:24`; solo scrittura)* [[PROGETTO-MITOSI]]

> ### **SOLO SCRITTURA** *(la richiesta di Luca delle `14:24`: «registrare l'analisi per quando si fara' la mitosi»)*: **nessun codice, nessuna corsa, NESSUNA DECISIONE PRESA.**
> **Come si legge:** **le cose dette da Luca sono SUE, con l'orario;** **le proposte del guardiano sono PROPOSTE;** **quello che Luca ha accolto («mi piace») e' un ORIENTAMENTO DI LUCA, non una decisione.**
> **I riferimenti di letteratura li ha indicati il guardiano:** **sono tutti DA VERIFICARE** *(nessuna citazione testuale qui)*. **La corsa lunga in atto** *(`S162`)* **non si tocca.**

## 0. LE PREMESSE *(che cosa c'e' oggi, e che cosa NON so)*

- **Oggi il tick e' un battito globale:** `composizione.ORDINE`, `14` posizioni, tutti i nodi insieme; `cs` e' un parametro per nodo *(F1, sul laterale, lo fa rilassare a ogni confine di tick)*.
- **La mitosi dell'era `2` non c'e':** il progetto e le forme da scegliere stanno in `doc/PROGETTO_MITOSI.md` *(par. `3`, nessuna scelta)*; la voce `21` della MAPPA chiede **«una grandezza che si accumula e scatta a soglia»**.
- **Non so** se il modello di oggi ammetta un flusso di energia fra i nodi «per quanti» *(la domanda della sez. `2`)*: **oggi i flussi sono continui** *(la voce `21`: `7.3e-6` per tick a `s 0.3`)*.

## 1. IL TICK COME SCALINO *(Luca, `14:05`)*

- ### **LE PAROLE DI LUCA:** **il tick non e' un orologio che gira: e' la misura continua di uno SCALINO, di una differenza nel fluire delle energie.** **Scatta come un INTERRUPT a ogni differenziale; la frequenza non e' costante.**
- **La lettura del guardiano:** **il tempo come conteggio degli eventi** *(«il tempo e' il cambiamento contato»)*. **I parenti indicati** *(da verificare)*: **Aristotele** *(il tempo come «numero del movimento»)*; **Barbour**; **il tempo termico di Connes-Rovelli**; **il neurone integrate-and-fire**; **il mucchio di sabbia di Bak-Tang-Wiesenfeld** *(1987)*.
- ### **DUE LEGAMI COL PROGETTO** *(PROPOSTE del guardiano)*:
  - **(a) `cs` potrebbe diventare la FREQUENZA DEGLI SCATTI di un nodo,** invece di un parametro: **tick e `cs` diventerebbero una cosa sola;**
  - **(b) e' lo stesso meccanismo cercato per la mitosi** *(la MAPPA, voce `21`: «una grandezza che si accumula e scatta a soglia»)*.

## 2. COME SI SIMULA UN FLUIRE SENZA BATTITO *(analisi del guardiano)*

- **Il calcolatore ha sempre un battito:** **il punto e' che non conti per la fisica.**
- **TRE MODI:**
  - **(i) A EVENTI, con un ORDINE CAUSALE al posto del tempo:** una coda dei nodi pronti a scattare;
  - **(ii) il tempo come PARAMETRO DI SERVIZIO:** il prossimo scatto calcolato esattamente *(come la dinamica delle sfere rigide)*;
  - **(iii) il tempo come CORRELAZIONE in uno stato fermo** *(Page-Wootters, 1983; da verificare)*.
- ### **IL CRITERIO, MISURABILE:** **le grandezze fisiche non devono dipendere dall'ordine in cui si elaborano gli eventi INDIPENDENTI** *(la «covarianza generale discreta» della crescita sequenziale di Rideout-Sorkin, 2000; da verificare)*.
- ### ❓ **LA CONDIZIONE DA CUI DIPENDE TUTTO, UNA DOMANDA APERTA PER LUCA:** **fra uno scatto e l'altro, l'energia scorre in modo CONTINUO** *(allora serve di nuovo un parametro sotto, e la simulazione ESATTA e' impossibile)* **o solo PER QUANTI, negli scatti dei vicini** *(allora si simula col modo (i))*?
- **NON i cicli della CPU** *(non riproducibili, legati alla macchina)*: **il tempo del modello e' il NUMERO DEI SUOI SCATTI.** **I parenti** *(da verificare)*: **Zuse, «Rechnender Raum»** *(1969)*; **il progetto di fisica di Wolfram** *(2020)*.

## 3. DUE SPECIE DI EVENTI *(Luca, `14:18`: «al numero degli aggiornamenti mancano gli eventi di mitosi»)*

- **LO SCAMBIO:** un nodo passa un quanto ai vicini. **Cambia cio' che c'e'; REVERSIBILE.**
- **LA NASCITA:** un nodo si divide. **Cambia lo spazio stesso; IRREVERSIBILE** *(i nodi crescono soltanto)*.
- **Le conseguenze** *(analisi del guardiano)*:
  - **(a) la FRECCIA DEL TEMPO verrebbe dalla crescita dello spazio** *(Sorkin: «la crescita e' il passare del tempo»; da verificare)*, **mentre gli scambi restano reversibili** *(`G6`)*;
  - **(b) il conteggio GLOBALE accelera con l'espansione; ogni nodo vive solo i SUOI scatti;**
  - **(c) con le nascite l'UNITARIETA' ESATTA del tick globale si perde:** **la norma si conserva con un'IMMERSIONE in uno spazio che cresce, e la reversibilita' diventa solo LOCALE.**

## 4. L'ETA' DI UN NODO APPENA NATO *(PROPOSTA del guardiano; accolta da Luca alle `14:22` come ORIENTAMENTO, non come decisione)*

- **La nascita e' uno SCATTO DEL PADRE** *(lo decide la sua grandezza accumulata)*, **non un evento a se'.**
- **I due figli EREDITANO il conteggio del padre, `+1`.**
- ### **IL PRINCIPIO UNICO:** **il tempo di un nodo = il numero di eventi nel suo PASSATO CAUSALE.** **L'eredita' segue senza una regola apposta** *(negli insiemi causali l'eta' di un elemento e' la grandezza del suo passato; da verificare)*.
- **«Nascere a zero» reintrodurrebbe un ISTANTE ASSOLUTO:** **e' scartato per questo motivo.**
- **E' coerente con `D7`** *(`psi/sqrt 2` a padre e figlio, con la stessa fase)*: **stessa fase e stessa eta'.** **I figli sono GEMELLI, che poi invecchiano diversamente secondo cio' che accade intorno.**

## 5. LA CONSERVAZIONE LOCALE DELL'ENERGIA *(Luca, `14:22`: «l'energia deve essere conservata localmente»: un REQUISITO)*

- ### **IL BILANCIO DELLA NASCITA, LOCALE:** **energia del padre** *(coi suoi archi)* **= energia dei due figli + energia dell'arco nuovo + energia del pezzo di vuoto nuovo.**
- **La materia:** **a posto con `D7`** *(la somma di `rho` conservata)*.
- **Il vuoto, con O1:** **ogni nodo porta un'energia del vuoto fissa `epsilon_v`.** **Il nodo nuovo la porta con se', e la PAGA IL PADRE con quanto ha accumulato dagli scambi** *(coerente con l'orientamento di Luca del `2026-10-25`: «l'energia della nascita di un nodo va scambiata col vuoto»)*.
- ### **LA CONSEGUENZA** *(PROPOSTA del guardiano)*: **lo scalino della mitosi NON e' un parametro scelto** *(`A1`)*: **e' il COSTO LOCALE DI UN NODO NUOVO** *(`epsilon_v` piu' l'arco nuovo)*, **quindi DERIVATO dalla conservazione.** **Il tasso `Gamma` di O-ESP seguirebbe da quanto velocemente l'energia affluisce ai nodi.**
- ### **LE CONSEGUENZE SCOMODE** *(scritte come PREVISIONI del modello, non come difetti)*:
  - **(a) con la conservazione locale stretta LO SPAZIO NUOVO NON E' GRATIS:** **un'espansione esponenziale spontanea del vuoto** *(de Sitter)* **non c'e', se il vuoto non ha una riserva da cui pagare.** *(Nota: nella relativita' generale l'energia del vuoto di un universo che si espande non si conserva globalmente, e il bilancio torna con la pressione negativa.)*
  - **(b) l'espansione sarebbe PIU' LENTA dove non c'e' niente e PIU' RAPIDA dove c'e' flusso, vicino alla materia.**
- ### **LA SCELTA DELLO ZERO DECIDE IL PREZZO DELLO SPAZIO:** **con O1 la nascita costa `epsilon_v` a nodo; con O4** *(lo zero locale)* **il vuoto uniforme ha energia zero e la nascita costa SOLO l'arco nuovo.** **E' un motivo in piu' per le misure M1-M4** *(`doc/TASK_HISTORY/2026-11-08_zero_del_vuoto.md`, sez. `4`)* **prima della scelta fra O1 e O4.**

## 6. LE DOMANDE APERTE *(per Luca, quando si fara' la mitosi; il criterio di chiusura: la sua risposta, registrata qui)*

1. **Il flusso fra gli scatti: CONTINUO o PER QUANTI** *(la sez. `2`)*.
2. **Lo scalino: UNO per tutto l'universo, o UNO PER NODO** *(domanda posta alle `14:05`, senza risposta)*.
3. **Le regole per gli scatti SIMULTANEI di nodi vicini.**
4. **`cs` come frequenza degli scatti:** **da scrivere come proposta, con le sue conseguenze per F1-F4** *(la linea del laterale)*.
5. **Il bilancio della sez. `5` scritto per esteso nell'era `2`** *(quali termini dell'energia, quali archi)*.

## 7. TODO

1. **Questo file; i rimandi in `doc/PROGETTO_MITOSI.md`** *(una sezione nuova, le forme del par. `3` come sono)*, **`doc/MAPPA.md`** *(voci `21` e `35`)*, **`doc/TASK_HISTORY/2026-11-08_zero_del_vuoto.md`** *(una riga in O-ESP)*; **un paragrafo nella relazione.** **Nessuna voce dell'indice cambia stato.**
2. **Niente altro finche' Luca non apre la mitosi.**
