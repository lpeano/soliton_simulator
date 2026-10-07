# `A1` — LA MISURA DEL VERSO SULLA FINESTRA GIUSTA *(2026-10-07)*

*(Mandato di Luca del 2026-10-07, punto `2`. ### **Prima azione della parte `A` di
`doc/RIPRESA_2026-10-07.md`.** ### **SOLA LETTURA: nessuna patch al simulatore**, che resta
### **`b8c21049`** *(`sha1` dei ### **byte grezzi**; `git hash-object` dà `e96ca41a`, ed è
l'altra convenzione)*. ### **`doc/ASSIOMI.md` non si tocca.**)*

> ### ⛔ **QUESTO FILE SI COMMITTA PRIMA DI QUALUNQUE MODIFICA AGLI STRUMENTI.** I criteri e
> le previsioni che stanno qui sotto sono ### **pre-registrati**, e l'ordine è
> ### **verificabile da git** — non asserito da me.

---

## 0. I CONTROLLI DI PARTENZA, **fatti**

| | |
|---|---|
| `git pull` | ### **già aggiornato** |
| il blob del simulatore | ### **`b8c21049`** — ### **coincide** con l'atteso |
| l'ultimo commit | ### **`a88f386` è ANTENATO di `HEAD`** *(verificato con `git merge-base --is-ancestor`)* |

### LE VOCI BLOCCANTI, **interrogate col comando del file** *(`python csv/_indice_id.py --blocca SI`)*

### **`12` voci su `941`:**

| id | stato |
|---|---|
| `CLI-1` | `da-decidere` |
| `D03` | `da-decidere` |
| `D31` | `da-decidere` |
| `SCALE-TW` | `da-decidere` |
| ### ⛔ **`U1`** | `da-decidere` |
| `CENS-A1` | `aperto` |
| `CENS-A2` | `aperto` |
| `CENS-A6` | `aperto` |
| `CENS-A7` | `aperto` |
| `CENS-B7` | `aperto` |
| `SCHED-PASSO` | `aperto` |
| `TETTO-CAUSALE-TEMPO-COORDINATO` | `aperto` |

## ⛔ **PERCHE' `A1` SI PUO' FARE CON `U1` APERTA — e non è una scorciatoia**

`U1` dice ### **<<URGENTE, PRIMA DI QUALUNQUE GIRO LUNGO>>**, e `A1` è un giro lungo. Quindi
la ragione va scritta, non sottintesa.

| | |
|---|---|
| **`1`** | ### **`A1` NON PRODUCE VALORI ASSOLUTI: produce un CONFRONTO FRA OPZIONI sulla STESSA corsa.** La legge difettosa che `U1` denuncia — la soglia tarata dentro `massa_critica_collasso` — è ### **LA STESSA in tutti i rami confrontati**, perché ### **le opzioni non sono bracci diversi del simulatore: sono CINQUE LETTURE della stessa corsa.** ### ➜ **Un difetto comune a tutti i termini di un confronto non ne cambia l'ordine.** |
| **`2`** | ### ✔ **E PER QUESTA SCENA `U1` E' ANCORA PIU' LONTANA DI COSI', ed è MISURATO:** `M1` del 2026-10-06 ha trovato ### **`(a) = 0` e `(c) = 0` a tutti e quattro i passi**, col massimo del rapporto ### **`10.7` volte sotto la soglia e IN CALO** *(`0.0932 → 0.0620 → 0.0483`)*. ### ➜ **`chiralita_core_locale` è INERTE per il dipolo**, quindi la soglia di `U1` ### **non entra nemmeno nel meccanismo che `A1` misura.** |
| **`3`** | ### ⛔ **MA `A1` E' IN SOLA LETTURA, e questo è il punto che rende la cosa onesta:** `A1` ### **non scrive nessuna legge** e ### **non chiude nessuna voce.** ### **Serve a SCEGLIERE la cura**, e la scelta è `A3` — ### **di Luca.** |

> ### ⛔ **E IL REFERTO LO DICHIARA IN TESTA**, non in una nota: *«corsa lunga con `U1`
> aperta; serve a scegliere, non a dare valori assoluti»*. ### **`A6` resta dov'è**, e
> ### **non la sto saltando: la sto rinviando con una ragione scritta.**

---

## 1. RAGIONAMENTO PRELIMINARE — *che cosa credo prima di guardare, e che cosa NON so*

### ⚠ **PRIMA DI TUTTO: CHE COSA HO GIA' VISTO**

I passi ### **`1`, `50`, `150`, `230`** sono ### **GIA' MISURATI** *(referto `d60b987`)*.
### ➜ **Per quei passi le mie non sono previsioni, e non le conto come tali.**
### **Le previsioni di questo file riguardano i passi `300`, `400`, `500`, `700`, `1000`** —
cioè ### **oltre il `216`**, dove le nascite ci sono.

### CHE COSA CREDO *(per i passi oltre il `216`)*

| | la previsione |
|---|---|
| **`P1`** | ### **`D` inietta la spinta MINORE** di tutte: il suo dipolo è ### **continuo**, e un `tw` che passa per zero ### **non inietta niente** |
| **`P2`** | ### **`MEM` inietta MENO di `A`**: è una media mobile, e ### **una media mobile salta meno del suo argomento** |
| **`P3`** | ### ⚠ **NON SO l'ordine fra `A` e `perc_geom`, e lo dico.** `A` cambia più spesso *(`0.72 %` contro `0.22 %` dei nodi per passo)*, ### **ma ogni cambio di `perc_geom` tocca `~74` archi** mentre un cambio di `A` ne tocca... ### **gli stessi `~74`.** ### ➜ **Quindi il conto dovrebbe dare `A` sopra, MA i due non contano la stessa cosa** *(`A` è un segno di nodo, `perc_geom` un `int64` di nodo)*: ### **l'ordine lo decide il numero, non io.** |
| **`P4`** | la frazione di archi con ### **`\|tw\| > 2π` CRESCE** e al passo `1000` sta fra ### **`15 %` e `25 %`**. ### ⚠ **E' una STIMA da interpolazione** *(al `1000` la mediana è `3.9151`, `q75 = 5.3748`, `q95 = 6.5578`, e `2π = 6.2832` sta fra `q75` e `q95`)*, ### **non una misura: l'interpolazione fra due quantili non è una misura** |
| **`P5`** | le nascite per `100` passi stanno fra ### **`48` e `150`** *(il riferimento senza il `0.3`)* |
| **`P6`** | ### ⭐ **la base dei cicli CONTINUA A NON CAMBIARE**, cioè ### **`~0 %`** anche a `1000` passi e con migliaia di nascite — perché copre ### **i primi `256` archi IN ORDINE DI INDICE**, e le nascite stanno ### **altrove.** ### **E' la previsione più netta di questo file** |
| **`M5a`** | ### **`phi0` è memoria MORTA**: `Spearman(c0, cδ) < 0.3` sugli archi VUOTO di età `> 2τ_tw`, perché `c0` è ### **congelato e casuale** nel vuoto mentre `cδ` ### **evolve** |
| **`M5b`** | ### **il dipolo NON domina `δ`**: mediana di `\|tw_dip\|/\|tw\|` ### **sotto `0.5`**, perché il dipolo è ### **nullo sul `~98 %` degli archi** *(misurato in `27c10bd`)* |
| **`M5c`** | nel ### **VUOTO** la quota di archi con `c0 < 0` è ### **`~50 %`** *(segni casuali congelati)* e le plaquette frustrate ### **`~50 %`** *(con metà dei segni negativi, un triplo casuale ha probabilità `0.5` di avere un numero DISPARI di negativi)*; in ### **MATERIA** ### **`~0 %`**, perché `_semina_masse_coerenti` pone `phi0 = phi` |
| **`M5d`** | ### ✔ **l'osservazione di Luca REGGE** *(MATERIA sotto un quarto di VUOTO)*, ### **e il meccanismo che lo produce è `τ_tw`, non `tw²`:** `τ_tw = 2π/\|Δω\|`, e in MATERIA i nodi sono ### **coerenti** → `\|Δω\|` piccolo → ### **`τ_tw` GRANDE** → potenza `tw²·dt_e/τ_tw` ### **PICCOLA.** Nel vuoto il contrario |

### ⛔ CHE COSA **NON** SO

1. ### **L'ordine fra `A` e `perc_geom` sulla spinta iniettata** *(`P3`)*. ### **È la
   lettura che il mandato chiama <<il metro giusto>>, e non la prevedo.**
2. ### **Se `MEM` stia sotto o sopra `D`.** `D` è continuo, `MEM` è continuo ### **e
   mediato**: ### **mediare può ridurre O RITARDARE**, e un ritardo può produrre
   ### **escursioni più grandi** se il sistema cambia più in fretta di `τ_tw`.
3. ### **Quanto l'età dell'arco conti in `M5a`.** Il taglio `> 2τ_tw` è ### **del mandato**,
   e non so se `2` sia abbastanza: ### **riporto anche la dipendenza dall'età**, così il
   taglio si può rileggere.
4. ### **Se la coerenza delle masse continui a calare** *(l'`AUC` di `M2`: `0.999 → 0.902`
   in `230` passi)*. ### **A `1000` passi potrebbe stabilizzarsi o crollare**, e
   ### **non ho un modello.**

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO — **le letture si fissano QUI**

### LA CORSA

| | |
|---|---|
| strumenti | `9a00080a` *(`M1`-`M3`)* · `e2d075f3` *(`M4`)* · `2daca9de` *(generatore)* — ### **più le estensioni di questo lavoro** |
| scena | quella del driver, ### **seme `11`**, ### **`b8c21049`** |
| passi | ### **`1000`**, un braccio, ### **SOLA LETTURA** |
| passi ### **pesanti** | `1`, `150`, `230`, `300`, `400`, `500`, `700`, `1000` ### **più i loro predecessori** *(la stabilità è una differenza fra due passi)* |

### A OGNI PASSO, non solo ai pesanti

| | |
|---|---|
| `1` | la stabilità di ### **`A`**, ### **`D`**, ### **`MEM`** e ### **`perc_geom`** |
| `2` | ### ⛔ **LA SPINTA INIETTATA `Σ\|Δdipolo\|`** che ciascuna opzione produrrebbe — ### **il metro giusto** |
| `3` | la frazione di archi con ### **`\|tw\| > 2π`** |
| `4` | le ### **nascite** |
| `5` | per `M3-C`, la frazione di cicli della base che ### **cambiano** |

### `M5` — **LE MEMORIE**, ai passi pesanti, ### **dentro il presidio che verifica l'impronta di `net`**

| | |
|---|---|
| `(a)` | per ogni arco ### **`c0 = cos(phi0_i − phi0_j)`** e ### **`cδ = cos(dph − tw)`**: Spearman, quantili di `cδ − c0`, quota a segno discorde — ### **per classe**, ### **per ORIGINE dell'arco** *(seminato, `_allaccia`, divisione, Schwinger: ricavata con ### **involucri in SOLA LETTURA**)* e ### **per età in unità di `τ_tw`** |
| `(b)` | la parte del dipolo dentro `tw`: un accumulatore ### **PARALLELO** `tw_dip' = tw_dip + Δdipolo − dt_e·tw_dip/τ_tw`, che parte da ### **`0` alla nascita dell'arco**. Si riporta ### **`\|tw_dip\|/\|tw\|`**, anche sugli archi ### **toccati da un salto del dipolo nei `50` passi precedenti** |
| `(c)` | il ### **disordine CONGELATO**: quota di archi con `c0 < 0`, e quota di ### **plaquette frustrate** *(prodotto dei tre segni di `c0` negativo)*, per classe |
| `(d)` | ### **IL BILANCIO DELLA TORSIONE**: la potenza persa nel rilassamento, ### **`Σ tw²·dt_e/τ_tw` per passo**, per classe e ### **per nodo** *(metà a ciascun estremo)* |

### ⛔ **I CRITERI, FISSATI QUI E PRIMA DEI NUMERI**

| | il criterio |
|---|---|
| **`phi0` è memoria MORTA** | `Spearman(c0, cδ)` ### **`< 0.3`** sugli archi ### **VUOTO** di età ### **`> 2τ_tw`** |
| **`phi0 ≈ δ`** | la stessa Spearman ### **`> 0.8`** |
| fra i due | ### **AMBIGUO**, e si dice così |
| **il dipolo DOMINA `δ`** | la ### **mediana** di `\|tw_dip\|/\|tw\|` ### **supera `0.5`** |
| **la dissipazione sta nel VUOTO** | la potenza ### **per nodo MEDIANA** in MATERIA è ### **meno di UN QUARTO** di quella in VUOTO, ### **a TUTTI i passi pesanti dopo il `300`** |

### ⛔ CHE COSA MI FAREBBE **FERMARE**

1. ### **il presidio di sola lettura che non ripristina** *(è già successo: `_g_registro_apparse`)*;
2. ### **la BYTE-INERZIA che fallisce**: `50` passi ### **CON** e ### **SENZA** gli osservatori devono dare stato ### **identico AL BIT**. ### ⛔ **Se non lo danno, la corsa NON PARTE e lo dico** — è il controllo `(c)` dell'ordine dei commit;
3. ### **il conto indipendente delle plaquette che non coincide** *(è già successo: `138313` contro `5534011`)*;
4. ### **`n` che SCENDE** *(i nodi non nascerebbero più in coda)*;
5. ### **archi con `i > j` non gestiti**: ### ✔ **ora la chiave è canonica, quindi NON deve più fermare** — e se fermasse, la cura del 2026-10-06 non ha funzionato;
6. ### **lo scarto dell'olonomia dal multiplo di `4π` che non sia `~0`**;
7. ### **`c_k` fuori da `[0,1]`** o ### **`(c) > (a)`** in `M1`.

---

## 3. ⭐ **LA VALUTAZIONE DELLA REGOLA `L-MEMORIA-PRIMA`** — *per la cura del verso*

> ### 📌 **La regola di Luca pretende i SETTE CAMPI nel task history di ogni cura.**
> ### ⚠ **`A1` NON È una cura — è una misura** — ### **ma la cura che prepara è quella del
> VERSO**, e la valutazione va scritta ### **prima della misura**, non dopo: altrimenti i
> numeri la influenzerebbero.

| il campo | la risposta |
|---|---|
| **quale memoria** | ### **`δ = twp − tw`**, la ### **media mobile esponenziale di `dph_prec`** già dentro `tw`. ### **Vive sull'ARCO.** *(Voce `MEM-VERSO`.)* |
| **hebbiana o d'altro tipo** | ### **MEDIA MOBILE**, ### **non hebbiana**: non si rinforza con l'attività congiunta dei due estremi, ### **inseugue una differenza di fase** |
| **sostituisce o aggiunge** | ### ✔ **SOSTITUISCE**, e non aggiunge ### **nemmeno una variabile**: `twp` e `tw` ### **ci sono già entrambi** |
| **che verso dà** | il verso ### **della media mobile**: *da che parte si stava andando*. ### ⚠ **Ritardato di un passo**, e il ritardo è un ### **costo dichiarato** |
| **a chi cede ciò che dimentica** | ### ✔ **a nessuno di NUOVO**: il termine `−dt_e·tw/τ_tw` ### **esiste già**, e la sua violazione di `A15.3` ### **resta dichiarata dov'è** *(§`3` n.1 del rapporto)*. ### **Il bilancio non cambia di un termine** |
| **da dove viene il suo tempo** | ### **`τ_tw = 2π/\|Δω\|`** — ### **DERIVATO**, ed è ### **l'esempio che `A15.2` cita** |
| **quali altre voci chiuderebbe** | ### **`GEOM-SENZA-VERSO`**. ### ⚠ **E toccherebbe di rimbalzo `SOGLIA-MITOSI-3PI`**, perché la soglia leggerebbe un dipolo diverso |

### ✔ **LE TRE CONDIZIONI DELLA PREFERENZA, verificate una per una**

| | |
|---|---|
| `(1)` non aggiungere stato quando se ne può sostituire uno | ### ✔ **SODDISFATTA per costruzione**: ### **zero stato nuovo** |
| `(2)` relazionale e locale, mai su `pos` né su medie globali | ### ✔ **SODDISFATTA**: ### **un arco, due nodi**, e ### **nessuna lettura di `pos`** |
| `(3)` se aggiunge dissipazione, solo dopo `ENERGIA-NON-DEFINITA` e `VUOTO-LOCALE-DETERMINISTICO` | ### ✔ **NON SI APPLICA**: ### **non aggiunge dissipazione** |

### ⛔ **E PERCHE' LA MEMORIA POTREBBE NON ESSERE LA CURA GIUSTA — che la regola pretende**

| | |
|---|---|
| `1` | ### ⛔ **`δ` È SPORCATA DAL DIPOLO** *(ogni salto inietta un gradino che persiste `~τ_tw`)*: c'è un anello ### **`tw → dipolo → δ → verso → dipolo`**, e ### **`M5b` misura quanto grande è lo sporco.** ### **Se il dipolo dominasse `δ`** *(mediana `> 0.5`)*, ### **`MEM-VERSO` leggerebbe se stessa** e ### **non sarebbe una cura: sarebbe un anello** |
| `2` | ### ⚠ **IL RITARDO**: se il sistema cambia più in fretta di `τ_tw`, il verso mediato ### **punta dove il sistema ERA.** ### **È `A1` a dire se succede** |
| `3` | ### ⛔ **E `P` resta un'alternativa VIVA**, con un vantaggio che `MEM` non ha: ### **è CANONICA** *(non dipende dalla numerazione né da un albero)*. ### **`MEM` è locale e senza stato nuovo; `P` è canonica e dà un asse.** ### **Non si sceglie qui** |

> ### ⛔ **LA SCELTA FRA `A`/`B`/`C`/`D`/`P`/`MEM` È `A3`, ED È DI LUCA.** ### **Questa
> valutazione dice che `MEM` è ammissibile per la regola, NON che sia la cura.**

---

## 4. LA STELLA POLARE *(`L-STELLA`)*

> ### ⛔ **NON SI APPLICA, e il perché è parte della risposta:** `L-STELLA` chiede le cinque
> domande ### **nei commit che cambiano la FISICA**, e `A1` ### **non cambia nessuna
> legge**: il simulatore resta `b8c21049` e gli strumenti sono ### **di sola lettura**, con
> un presidio che lo ### **verifica e si ferma.**
>
> ### ⚠ **MA DUE DELLE CINQUE VANNO RISPOSTE COMUNQUE**, perché `A1` esiste per loro:
>
> | | |
> |---|---|
> | *«numeri o leggi aggiunti»* | ### **ZERO.** Le estensioni degli strumenti sono ### **letture**; i criteri di questo file sono ### **soglie di LETTURA**, non di legge, e ### **le dichiaro come mie** |
> | *«emergente o imposto»* | ### ⭐ **è LA domanda di `A1`**: se il verso che serve ### **emerge da una memoria che il sistema ha già** *(`MEM`)* oppure ### **va imposto** *(una legge nuova per nodo o per plaquette)*. ### **`A1` non risponde: dà i numeri su cui Luca risponde** |

---

## 5. TODO DEL NEXT STEP — **l'ordine dei commit, uno per cosa**

| | |
|---|---|
| ### ✔ **`a`** | ### **questo file**, coi criteri e le previsioni, ### **PRIMA di qualunque modifica agli strumenti** |
| `b` | le ### **estensioni degli strumenti** *(spinta iniettata, `MEM`, `M5`)*, col ### **collaudo** e ### **un caso che DEVE fallire**, ### **PRIMA della corsa** |
| `c` | la ### **BYTE-INERZIA**: `50` passi ### **CON** e ### **SENZA** gli osservatori, stato ### **identico al bit**. ### ⛔ **Se non lo è, la corsa NON PARTE** |
| `d` | il ### **collaudo a `2` passi** |
| `e` | la ### **corsa**: in background, ### **interrogata**, ### **senza chiudere il turno**. ### **Se una guardia la ferma: commit del fallimento, cura in un commit a parte, rilancio** |
| `f` | ### **json e referto** dal generatore, con la ### **tavola delle previsioni contro i numeri**, e la ### **dichiarazione che è una corsa lunga con `U1` aperta** |
| `g` | l'### **aggiornamento di `doc/MEMORIE_MANCANTI.md`** coi numeri di `M5`, ### **per ANNOTAZIONE e non riscrittura** |

> ### ⛔ **POI FERMARSI.** ### **Non toccare il simulatore, non scegliere un'opzione, non
> scrivere nessuna memoria come legge, non passare ad `A2`.**

---

## ⭐ **AGGIUNTA DEL 2026-10-07, A CORSA IN VOLO** *(`par.8`: è un'AGGIUNTA, non una modifica delle previsioni)*

> ### ⛔ **UN CONTROLLO IN PIÙ, GRATIS, E UN ERRORE DEL GUARDIANO CHE IL GUARDIANO
> RICONOSCE.**

**IL RILIEVO:** la byte-inerzia di `d01cc2a` è stata fatta su ### **`50` passi**, cioè
### **PRIMA della prima nascita (`216`).** ### ➜ **Gli involucri sulle funzioni di nascita
*(`_allaccia`, la mitosi, lo Schwinger)* NON SONO MAI STATI ESERCITATI MENTRE LAVORANO.**

> ### ⚠ **Il guardiano aveva chiesto `50` passi, e lo riconosce.** ### **Io l'ho eseguito
> senza notare che `50 < 216`** — ed è ### **la stessa trappola della finestra** che ha
> fatto rifare questa misura.

### ✔ **LA VERIFICA NON COSTA UNA CORSA: il riferimento ESISTE GIÀ**

`csv/_test_fork/_mitosi_zero_dove/amp0.json` è il braccio ### **`_AMP = 0`** su
### **`1000` passi**, e la catena che lo rende valido per `b8c21049` è:

| | |
|---|---|
| `amp0.json` | blob ### **`cf2a1ac8`** con la modulazione del `0.3` ### **annullata** |
| `S1` del sigillo `6d7107b` | ### **`30e18cdd`** riproduce `amp0.json` ### **AL BIT su `230` passi** |
| il sigillo `35044cc` | ### **`b8c21049`** differisce da `30e18cdd` ### **solo per DUE STRINGHE**, codice compilato ### **IDENTICO** |

### ⛔ **IL CRITERIO, FISSATO ORA E PRIMA DI GUARDARE** *(è di Luca)*

> ### **Zero differenze su tutti i `1000` passi = gli osservatori, involucri di nascita
> compresi, NON cambiano la dinamica.**
>
> ### **Una differenza = il primo passo diverso e il campo vanno nel referto, e i numeri di
> `A1` DOPO quel passo NON VALGONO finché non si trova la causa.**

### ⚠ **E DUE COSE CHE VANNO DICHIARATE PRIMA, perché cambiano la lettura**

| | |
|---|---|
| ### **i campi che `A1` NON registra** | ### **`nati_tot`, `schwinger_tot`, `q_tw`.** ### ⛔ **E NON si aggiungono ORA:** il `par.5` vieta di toccare un file del percorso in uso, e la corsa è ### **in volo.** Si confronta ### **`n` e `archi`**, e gli altri ### **si dichiarano** |
| ### ⚠ **una trappola di CONVENZIONE** | nel riferimento ### **`n` viene da `chiudi` (POST-passo)** e ### **`archi` dal gancio della torsione (METÀ passo)**: al passo `216` si legge ### **`n = 12804` con `archi` ancora `471564`.** ### ➜ **Un disallineamento di UN passo su `archi` sarebbe una CONVENZIONE, non una differenza di dinamica.** ### ✔ **Lo strumento prova ENTRAMBI gli allineamenti e DICHIARA quale combacia** |

> ### ⚠ **E `n` E `archi` A OGNI PASSO NON SONO POCO:** `n` è ### **il conto delle nascite
> integrato**, e `archi` risente ### **sia della mitosi** *(`−1 +2`)* ### **sia dello
> Schwinger** *(`+2`)*. ### **Uno spostamento di UNA nascita di UN passo si vedrebbe in
> entrambi.**

**LO STRUMENTO:** `csv/_seal_fork/_inerzia_nascite.py`, e ### **gira alla fine della corsa
`A1`.**

---

# ⛔ **AGGIUNTA DEL 2026-10-07, DOPO LA CADUTA — e NON è una modifica delle previsioni**

> ### ⭐ **LE PREVISIONI E I CRITERI QUI SOPRA RESTANO INTATTI.** Questa sezione registra
> ### **che la prima corsa non è arrivata a misurarli**, e perché. ### **Nessun criterio è
> stato toccato dopo aver visto un numero.**

## CHE COSA È SUCCESSO

La corsa è ### **caduta al passo `216`**, la ### **prima nascita**, dopo `1425.8` secondi.
### **Il difetto era mio, nello strumento**, e il simulatore non c'entra: `b8c21049`
### **non è stato toccato.**

### **LA PREMESSA SBAGLIATA:** avevo avvolto `REGOLE_NASCITA[("divisione", "i")]`, cioè la
regola che scrive ### **SOLO `net.i`.** Quando quella regola ritorna, ### **`net.i` ha
`471565` voci e `net.j` ancora `471564`**: ### ⛔ **l'arco non esiste ancora come COPPIA, e
la sua chiave non è formabile lì.** ### **L'ordine si legge dal simulatore:** `i` è alla
posizione ### **`1`** di `ORDINE_DI_NASCITA`, `j` alla ### **`2`.**

### ⚠ **Quindi l'involucro non era «fragile»: era IMPOSSIBILE**, e sarebbe caduto alla prima
nascita di ### **qualunque** corsa. ### **Non c'è nessuna finestra in cui funzionava.**

## ⭐ **E IL CONTROLLO CHE LUCA AVEVA CHIESTO HA PAGATO PRIMA DI GIRARE**

Il rilievo era: *«la byte-inerzia di `d01cc2a` è stata fatta su `50` passi, cioè PRIMA della
prima nascita (`216`)»*. ### **Esatto, e il difetto è uscito prima ancora che il confronto
con `amp0.json` si potesse fare.**

### ⛔ **E IL CONTROLLO POSITIVO DI QUEL SIGILLO ERA UN `FALSO-UNO`, SCRITTO DA ME:**
chiedeva *«origini registrate `> 0`»* e passava ### **sempre** — i `471564` `seminato` li
scrive ### **l'installazione** degli involucri, con un giro che ### **non passa da nessun
involucro.** ### **La corsa caduta lo ha provato col numero:** `seminato 471564 |
divisione 0 | schwinger 0` su `216` passi.

## CHE COSA CAMBIA NEL MODO DI LEGGERE `A1`

| | |
|---|---|
| le previsioni | ### **invariate**, e ### **nessun numero oltre il `216` è stato visto** |
| i numeri della corsa caduta | ### **tutti sotto il `216`**, cioè nella finestra ### **già vista** in `d60b987`: ### **non rispondono a nessuna previsione di `A1`** |
| la finestra della byte-inerzia | ### **`50` → `220`**, perché `220` ### **contiene** una nascita |
| il controllo positivo | ### **`origini_da_nascita > 0`**, che su `50` passi ### **NON PUÒ essere soddisfatto** |
| gli involucri installati | ### **`3` → `1`**, sul punto unico `nascita` |

> ### ⛔ **E LA CONDIZIONE DEL MANDATO RESTA QUELLA:** se la byte-inerzia su `220` passi
> ### **fallisce, la corsa NON parte, e lo dico.**

## ⚠ **UNA COSA CHE AVEVO DICHIARATO E CHE ORA SI PUÒ FARE**

Qui sopra avevo scritto che i campi `nati_tot`, `schwinger_tot` e `q_tw` ### **non si
aggiungono ORA**, perché il `par.5` vieta di toccare un file del percorso in uso ### **e la
corsa era in volo.** ### **La corsa è caduta: quel vincolo non c'è più.**

### ✔ **MA NON LI AGGIUNGO LO STESSO, e il motivo è dichiarato:** aggiungerli ora
### **cambierebbe lo strumento fra le previsioni e la misura**, e il confronto con
`amp0.json` resta ### **valido su `n` e `archi`** — che sono il conto delle nascite
integrato e il conto degli archi, cioè ### **già sensibili a uno spostamento di UNA nascita
di UN passo.** ### ⛔ **Un campo in più non vale una variabile in più fra la previsione e il
numero.** ### **Se servirà, sarà un lavoro suo, dopo `A1`.**
