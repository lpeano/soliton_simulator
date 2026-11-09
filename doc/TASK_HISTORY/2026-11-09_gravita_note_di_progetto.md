# LA GRAVITA' NEL MODELLO: NOTE DI PROGETTO *(Luca `2026-11-09` `09:59`-`10:17`: «segniamocelo sul repo»)* [[PIANO-2D-3D]] [[PUNTO-FISSO-CS-SOLITONE]]

> ### **SOLA DOCUMENTAZIONE:** **nessun codice, nessuna corsa, nessuna decisione presa.** **Sul ramo principale** *(la regola `2` dei due rami)*. **Le attivita' in corso non cambiano.**
> **I rimandi:** la voce `35` della MAPPA *(le idee)*, la riga `5-PF` *(`cs` col solitone)*, il task history di D0-D4 sul laterale *(`doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, una riga che rimanda qui)*.

## 1. LE PREMESSE *(cosa e' un fatto, cosa e' da riconfermare, cosa non so)*

- ### **G1 e' un calcolo del GUARDIANO, non mio, e non e' ancora riconfermato dal repo:** **lo riconfermano R1-R3 dell'integrazione a (r-D5)** *(sul laterale, sez. `13`: il profilo radiale di `Lambda` e di `cs/s` alle quattro scene di `TBS`)*.
- **G2-G6 sono ragionamenti, non misure:** **le analogie sono analogie**, **e la fisica in `2+1` dimensioni e' quella nota dei libri, non una misura del modello.**
- ### **NON SO:** **se la direzione instabile del punto fisso di `cs` sta sul guscio** *(R2 lo dira')*; **se una `cs` che si diffonde risolverebbe il punto fisso** *(nessuna prova)*.

## 2. LE NOTE

### G1. IL FATTO DEL GUSCIO *(dal guardiano, da riconfermare con R1-R3)*

- **Dalle mappe leggere di `TB3`** *(`doc/referti_l2/campo_TB3/mappe_leggere.npz`, `Lambda = 6 + dLambda`)*: **il ritmo che la legge `cs = Lambda / (Lambda + 34)` darebbe al vuoto di ogni istante, diviso per `s = 0.15`.** ### **NON e' una corsa con `cs` acceso:** **e' l'orologio senza la sua reazione.**
- **Al centro del solitone `cs/s` e' `~1`** *(fino a `~2`: il tempo un po' piu' veloce)*.
- ### **Il rallentamento e' un GUSCIO sul bordo dell'esagono, a `~17`-`20` nodi dal centro:** **`cs/s` minimo `0.063` a `t 3000`, `0.030` a `t 30000`** *(il guscio si approfondisce con l'eta')*; **fuori dal guscio torna subito `1`.**
- **La fonte visiva:** il video del guardiano **`orologio_locale_TB3.mp4`** *(NON nel repo: una fonte esterna)*.
- **Coerente con D1 di `1cf4ecb4`** *(il `70%` dello scarto del punto fisso fra `w` e `2 w`)*.

### G2. COME FISICA DEI SOLITONI, E' PLAUSIBILE *(un'analogia, non una prova)*

- **Un interno omogeneo, e gli scambi col vuoto sulla PELLE.** **I paralleli:**
  - **la goccia** *(la tensione superficiale)*;
  - **il modello a goccia dei nuclei, col termine di superficie**;
  - **le Q-ball a parete sottile**;
  - **il modello a sacca degli adroni.**

### G3. COME GRAVITA', E' STRANA -- E IL MOTIVO E' STRUTTURALE

- **In relativita' generale il tempo rallenta di piu' al CENTRO di un corpo**, **e fuori il rallentamento si attenua come un potenziale che si estende lontano.**
- ### **Nel modello `cs` dipende SOLO da `Lambda` nel nodo, e `Lambda` e' MEMORIA:** **non si propaga** *(il ramo `Z` piatto)*.
- ### **Una legge puramente locale cosi' non puo' dare un effetto che sente tutta la materia intorno: il guscio ne e' il segno.**

### G4. PERCHE' LA `U(1)` DA' IL MECCANISMO MA NON LA GRAVITA'

- **La `U(1)` si propaga e, con Gauss, SOMMA i contributi di tutta la carica** *(un potenziale di tipo Poisson)*: ### **e' il meccanismo che manca a `cs`.**
- **Ma non e' gravita', per tre ragioni:**
  - **cariche uguali si respingono** *(la gravita' attira sempre)*;
  - **la sorgente e' la carica** *(la gravita' sente l'energia, tutta)*;
  - **il potenziale elettrico non rallenta il tempo.**
- ### **Legare `cs` al potenziale `U(1)` darebbe un orologio che dipende dal SEGNO della carica: non gravita'.**

### G5. LE STRADE POSSIBILI PER UNA GRAVITA' *(SOLO COME PROGETTO: nessuna scelta)*

1. **Un campo che si propaga come la `U(1)`, ma con l'ENERGIA come sorgente e ATTRATTIVO.** **Il piu' semplice:** uno scalare senza massa con un'equazione di tipo Poisson *(la gravita' di Nordstrom, storica)*. ### **Nel modello: un `Lambda` che si PROPAGA invece di essere memoria.**
2. **La CURVATURA:** **la `U` dinamica `SU(2)`**, l'alternativa (c) del progetto della `U` dinamica.
3. ### **Il collegamento con la cura del punto fisso di `cs`:** **una `cs` che e' una memoria che si DIFFONDE nello spazio** *(`A15` piu' un termine di diffusione)*, **invece di un valore puramente locale, potrebbe risolvere INSIEME il punto fisso e la mancanza di portata.** **Da valutare dopo (r-D5).**

### G6. IL LIMITE DELLE DUE DIMENSIONI *(un VINCOLO di progetto, non una decisione; [[PIANO-2D-3D]])*

- ### **In `2+1` dimensioni la relativita' generale NON ha attrazione fra masse ferme, ne' onde gravitazionali:** **una massa crea un DIFETTO CONICO** *(lo spazio e' piatto tranne un angolo mancante)*, **non un pozzo.**
- **Quindi una gravita' come la nostra, con un potenziale che si estende lontano, in `2D` non c'e' nemmeno nella teoria di Einstein.**
- ### **Una gravita' «vera» nel modello potrebbe richiedere il passaggio a TRE dimensioni.** **Si lega al piano `doc/PIANO_2D_3D.md`** *(«`2D` per le proprieta' locali del passo, `3D` per le leggi globali»)*: **la gravita' e' una legge globale.**

### G7. LE DOMANDE APERTE, A LUCA *(il criterio di chiusura: la sua risposta, registrata qui)*

1. **Quale strada per la gravita'?** *(un `Lambda` che si propaga; la curvatura `SU(2)`; altro)*
2. **Quando affrontare il passaggio a `3D`?**
3. **La cura del punto fisso di `cs` deve gia' andare nella direzione di una memoria che si DIFFONDE?** *(oggi (r-D5) e' solo una diagnosi, e non sceglie)*

### G8. LA DECISIONE DI LUCA DEL `2026-11-09` `11:17`: **IL PIANO 2D, POI 3D**

- ### **Prima LA FISICA DEL 2D (`2+1`) fino in fondo, con le leggi che il 2D permette; poi il 3D (`3+1`) e la fisica del 3D.** **Non sono due modelli rivali: il 2D e' la prima tappa.**
- ### **Nel 2D la gravita' NON puo' essere quella di Einstein** *(in `2+1` non attrae a distanza: spazio piatto fuori dalla materia, solo difetti conici; G6)*.
  - **Nel 2D la gravita' del modello si cerca come un campo che SI PROPAGA, con l'ENERGIA come sorgente e ATTRATTIVO** *(la strada scalare: Nordstrom, o un `Lambda` che si propaga; G5.1)*, **con un potenziale LOGARITMICO atteso.**
  - ### **E' una DIREZIONE, non ancora una legge:** **la forma si progetta DOPO la cura del punto fisso di `cs`.**
- **Nel 3D, piu' avanti: la gravita' di Einstein diventa possibile** *(maree, onde, attrazione `1/r`)*. **Nessun lavoro sul 3D ora.**
- ### **LE DIFFERENZE ATTESE FRA 2D E 3D, scritte come PREVISIONI** *(cosi' il passaggio a 3D e' un confronto, non una sorpresa)*:

| | **2D (`2+1`)** | **3D (`3+1`)** |
|---|---|---|
| **il potenziale di una massa** *(un campo scalare che si propaga, sorgente l'energia)* | **logaritmico**, `~ ln r` *(la forza `~ 1/r`)* | **`~ 1/r`** *(la forza `~ 1/r^2`)* |
| **la gravita' di Einstein** | **nessuna attrazione fra masse ferme:** spazio piatto fuori dalla materia, un difetto conico | **possibile:** l'attrazione `1/r`, le maree, le onde |
| **il fotone** *(la `U(1)`)* | **una polarizzazione** | **due polarizzazioni** |
| **le maree nel vuoto** | **nessuna** *(per la gravita' di Einstein; per lo scalare del 2D: da derivare)* | **si'** |
| **le onde gravitazionali** | **nessuna** *(per Einstein)* | **si'** |

- **Per G7:** **le domande 1 e 2 hanno una risposta di Luca** *(la strada nel 2D e' lo scalare che si propaga; il 3D dopo il 2D)*; **resta la 3** *(se la cura del punto fisso di `cs` deve gia' andare verso una memoria che si diffonde)*.

## 3. TODO

- **Niente da fare finche' Luca non risponde a G7.** **G1 si aggiorna col referto di (r-D5)** *(R1-R3)*, **con una riga qui.**
