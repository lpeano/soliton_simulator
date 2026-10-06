# `M1`-`M4` — LA MISURA DEL VERSO E DELLE PLAQUETTE *(2026-10-06)*

*(Mandato di Luca del 2026-10-06 e sua integrazione. ### **Nessuna legge nuova, nessuna
patch al simulatore** (`b8c21049`). ### **`doc/ASSIOMI.md` non si tocca.**)*

> ### ⚠ **UNA DICHIARAZIONE SULL'ORDINE, perche' il `par.8` chiede che il ragionamento si
> committi PRIMA e che l'ordine sia VERIFICABILE DA GIT, non asserito da me.**
>
> ### ⛔ **QUESTO FILE E' SCRITTO DOPO LO STRUMENTO, NON PRIMA.** L'integrazione di Luca e'
> arrivata mentre progettavo `M1`-`M3`, e ho scritto i due strumenti di fila. ### **Quindi
> NON e' vero che la PROGETTAZIONE dello strumento e' pre-registrata:** il commit di questo
> file e' antenato del commit degli strumenti ### **soltanto perche' li committo in
> quest'ordine adesso**, e sarebbe disonesto far finta che significhi altro.
>
> ### ✔ **CIO' CHE E' PRE-REGISTRATO DAVVERO, ed e' quello che conta per la misura:** le
> ### **PREVISIONI** e i ### **CRITERI** del `par. 2` qui sotto, che si committano
> ### **prima della corsa da `230` passi.** ### **Quella corsa non e' ancora partita.**
>
> ### ⚠ **E DICHIARO ANCHE CHE HO GIA' VISTO IL PASSO `1`:** il collaudo su `2` passi
> *(che il mandato chiede)* ha prodotto i numeri del passo `1`. ### **Quindi per il passo
> `1` le mie <<previsioni>> NON sono previsioni, e le marco come GIA' VISTE.** Le previsioni
> vere riguardano i passi ### **`50`, `150` e `230`.**

---

## 1. RAGIONAMENTO PRELIMINARE — *che cosa credo prima di guardare, e che cosa NON so*

### CHE COSA CREDO

| | |
|---|---|
| `M1` | ### **credo che `--chi-core` sia INERTE per il dipolo**, perche' al passo `1` il rapporto massimo e' ### **`0.0639`**, cioe' ### **`15` volte sotto la soglia** |
| `M2` | credo che `c_k` ### **separi MATERIA da VUOTO**: dove c'e' materia le fasi dei vicini sono coerenti e la somma non si cancella |
| `M3-A` | credo che i cambi di segno ### **CALINO** coi passi: `|tw|` cresce *(misurato altrove: `q75 = 5.37` al passo `1000`)*, e un valore lontano da zero cambia segno di rado |
| `M3-C` | credo che la base dei cicli ### **cambi molto** appena cominciano le nascite *(la prima divisione e' al passo `42`)*, perche' `_grado()` invalida la cache |
| `M4` | ### ⛔ **credo che la COERENZA sia BASSA**: con `~1300` plaquette attorno a un nodo, le normali puntano in molte direzioni e i contributi si cancellano |
| `M4(d)` | ### ⛔ **credo che `R_k` e `_nb` siano SCORRELATI**, cioe' distribuiti come il caso — e ### **se e' cosi', `P2` non lega niente** |
| `M4(e)` | credo che `R_k` ruoti ### **di molto** fra due passi, cioe' che ### **non sia stabile** — che sarebbe una cattiva notizia per `P` |

### ⛔ CHE COSA **NON** SO

1. ### **Se il rapporto di `M1` CRESCE con la rete.** Il `0.0639` e' del passo `1`, con
   `tw` ancora a zero e la rete appena seminata. ### **Non ho nessun motivo per credere che
   resti li'** — e se al passo `150` o `230` superasse `1`, ### **tre opzioni su quattro
   cambierebbero lettore.** ### **E' la ragione per cui `(b)` si riporta SEMPRE.**
2. ### **Se la coerenza di `M4(c)` dipende dalla CLASSE.** Potrebbe essere bassa nel vuoto
   e alta nella materia: sarebbe il risultato piu' interessante, e ### **non so prevederlo.**
3. ### **Quanto vale `f'` davvero.** Ho misurato la ### **quota di conteggi** `~1/37`, e
   ### **non e' la derivata**: dipende dalla normalizzazione di `chi_k` e dalla coerenza.
   ### **`M4` non lo misura**, e non pretendo che lo faccia.
4. ### **Se l'olonomia non nulla di `M3-C` resti attorno a meta'.** Al passo `0` e'
   ### **`122` su `256`**, e la previsione del guardiano era *«zero sulla maggior parte dei
   cicli»*. ### **Al passo `0` quella previsione NON e' confermata**, ma `tw` e `phi`
   cambiano, e ### **non so che cosa faccia nei passi veri.**

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO — **le letture si fissano QUI**

### I CRITERI, **fissati prima dei numeri**

| | il criterio |
|---|---|
| **`M1`** | ### ✔ **`(a) = 0` E `(c) = 0` a TUTTI E QUATTRO i passi significa `--chi-core` INERTE per il dipolo.** Altrimenti si riporta ### **dove e quanto** agisce. ### **E `(b)` si riporta sempre**: un massimo a `0.98` e uno a `0.001` danno lo stesso `(a) = 0` e dicono due cose opposte |
| **`M2`** | tre letture, e ### **nessuna sceglie niente**: la distribuzione ### **per classe**, quella ### **per numero di vicini**, e l'### **`AUC` MATERIA contro VUOTO**. ### **`AUC = 0.5` vuol dire NESSUNA separazione** |
| **`M3`** | i cambi ### **per passo** di `A` *(due letture)*, di `C`, di `D`, e di ### **`perc_geom` come RIFERIMENTO** |
| **`M4`** | `(a)` quante e ### **quanto costa**; `(b)` il ### **MODULO** `\|Σ tw\|`; `(c)` la ### **coerenza**; `(d)` il coseno con `_nb` ### **contro il caso NULLO, che e' ANALITICO** *(uniforme su `[-1,1]`: media `0`, frazione oltre `0.5` pari a `0.5`)*; `(e)` l'### **angolo** contro `perc_geom` |

> ### ⛔ **L'UNICA AFFERMAZIONE PERMESSA E' DESCRITTIVA**, e lo dice il mandato: ### **questa
> misura NON sceglie un'opzione.** Il referto ### **non porta raccomandazioni nuove** oltre
> quelle gia' scritte in `doc/GEOM_SENZA_VERSO.md`.

### ⛔ CHE COSA MI FAREBBE **FERMARE**

1. ### **il presidio di sola lettura che non ripristina** — e ### **e' GIA' SUCCESSO**: la
   prima corsa si e' fermata su `_g_registro_apparse`;
2. ### **il conto indipendente delle plaquette che non coincide** con l'enumerazione — e
   ### **e' GIA' SUCCESSO**: `138313` contro `5534011`;
3. ### **`n` che SCENDE**: i nodi non nascerebbero piu' in coda e il confronto per indice
   sarebbe invalido ### **in silenzio**;
4. ### **`c_k` fuori da `[0, 1]`**: l'algebra lo esclude, quindi sarebbe il mio conto a
   essere sbagliato;
5. ### **`(c)` che esce da `(a)`** in `M1`: vorrebbe dire che il mio ricalcolo di `rho0`
   non e' quello della funzione;
6. ### **lo scarto dell'olonomia dal multiplo di `4pi` che non sia `~0`** — e ### **e' GIA'
   SUCCESSO**, ed era la convenzione del `verso` letta male.

### I PASSI

1. ### ✔ **l'annotazione** *(`2a6b95b`)*: l'errore del guardiano e l'opzione `P`;
2. ### ✔ **questo file**, coi criteri, ### **prima della corsa**;
3. **gli strumenti**, ### **committati prima della corsa** *(lo chiede il mandato)*;
4. **la corsa**: `230` passi, un braccio, ### **in background**, interrogata;
5. **il json e il referto GENERATO**, in un commit a se'.

---

## 3. LA STELLA POLARE *(`L-STELLA`)*

> ### ⛔ **NON SI APPLICA, E IL PERCHE' E' PARTE DELLA RISPOSTA:** `L-STELLA` chiede le
> cinque domande ### **nei commit che cambiano la FISICA.** Questi commit
> ### **non cambiano nessuna legge**: il simulatore resta ### **`b8c21049`** e i due
> strumenti sono di ### **SOLA LETTURA**, con un presidio che lo ### **verifica e si ferma**
> se non e' vero.
>
> ### ⚠ **MA UNA DELLE CINQUE VA RISPOSTA COMUNQUE, perche' questa misura ESISTE per
> rispondere a quella:** *«numeri o leggi aggiunti, e di che tipo»*. ### **Questa misura
> non ne aggiunge nessuno** — `BLOCCO` e `PASSO_CAMPIONE` sono la taglia di un buffer e un
> passo di sottocampione, ### **e il collaudo verifica che il risultato NON dipenda dal
> primo** *(con `BLOCCO = 1` i numeri sono identici)*. ### **La legge nuova, se Luca la
> scegliera', e' il passaggio ciclo -> nodo o plaquette -> nodo**, ### **e questa misura
> serve a scegliere su numeri invece che su preferenze.**

---

## 4. TODO DEL NEXT STEP

1. **committare gli strumenti** *(`_misura_verso.py`, `_misura_plaquette.py`)* con le
   ### **voci nell'INVENTARIO**: file, ### **comando verbatim**, cosa misura, ### **blob**;
2. **lanciare la corsa** da `230` passi ### **in background**, interrogarla
   periodicamente, ### **senza chiudere il turno**;
3. **committare il json e il referto** generato dallo strumento, ### **senza
   raccomandazioni nuove**;
4. ### ⛔ **POI FERMARSI:** la scelta fra `A`/`B`/`C`/`D`/`P`, fra `P1`/`P2`/`P3`, e se
   aprire `U1` per `chiralita_core_locale`, ### **sono decisioni di Luca.**
