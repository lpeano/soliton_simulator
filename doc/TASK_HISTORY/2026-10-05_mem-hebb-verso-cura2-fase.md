# `MEM-HEBB-VERSO`, passo (2) — **LA CURA DEL SITO DELLA FASE (lo SPEGNIMENTO)**, piu' **IL PROGRAMMA CONCORDATO**

## STATO: **INIZIATO il 2026-10-05** *(era `NON INIZIATO`)*

> ### ✅ **PARTE ORA**, dopo che `Z43` passo (1) e' chiuso *(`66a798d`, `9cec5d8`)* e
> che **il programma** e' registrato *(`e04b6bf`)*.

*(Messo al sicuro nel repo il **2026-10-05**, **mentre il mandato `Z43` passo (1) era in
corso**. ### **Nessun lavoro e' stato fatto su questo mandato.**)*

> ### ⛔ **PERCHE' NON PARTE SUBITO, e non e' una mia scelta: e' `L-UN-PROMPT`** — *«un
> prompt alla volta; i rilievi che arrivano durante un lavoro vanno in CODA, non lo
> interrompono»*. ### **E il mandato stesso lo dice:** *«Si esegue DOPO il mandato `Z43`
> passo (1), che e' in coda prima di questo»*.

> ### ⛔ **LA SEZIONE `LA STELLA POLARE` NON E' QUI, E NON PER DIMENTICANZA:** il mandato
> chiede *«task history PRIMA del codice, con `LA STELLA POLARE`»*, e si scrive **quando il
> lavoro parte**. ### **Scritta adesso sarebbe una risposta data prima di aver letto il
> codice, cioe' esattamente la ricostruzione che il par.8 esiste per impedire.**

> ### ⚠ **E IL TESTO QUI SOTTO E' COPIATO PAROLA PER PAROLA**, come per il mandato del
> 2026-10-04: **non e' riassunto ne' riformulato.** Se una riga sembra ambigua,
> l'ambiguita' e' **nell'originale** e va risolta con Luca, non da me.

---

## IL MANDATO, verbatim

MANDATO: MEM-HEBB-VERSO, PASSO (2): LA CURA DEL SITO DELLA FASE (lo SPEGNIMENTO), piu' IL PROGRAMMA CONCORDATO. Si esegue DOPO il mandato Z43 passo (1), che e' in coda prima di questo.

PARTE 1: IL PROGRAMMA, deciso da Luca il 2026-10-05, da scrivere nel "TODO ALLA RIPRESA" di doc/TASK_HISTORY/2026-10-04_mem-hebb-verso-misura.md e da collegare in doc/INDICE_ID.tsv (Z43, MEM-HEBB-VERSO, TETTO-CAUSALE-TEMPO-COORDINATO):
 1. Z43 passo (1), la misura del tempo proprio r (in coda prima di questo).
 2. MEM-HEBB-VERSO passo (2): lo spegnimento del sito della fase (questo mandato).
 3. Decisione di Luca sulla definizione di r, dopo il referto di Z43; poi la cura di r con il suo sigillo.
 4. TETTO-CAUSALE passo (2) e la cura (1) di MEM-HEBB-VERSO (la forma di proj), PENSATI INSIEME perche' toccano la stessa funzione, ma in commit separati, ciascuno col suo sigillo. L'idea da valutare allora: il taglio passo_max = 0.01*mediana(d0) (numero a mano, mediana globale, comanda sul 40-55% degli archi) sostituito dal limite causale c_s*dt_e dell'arco. DECISIONE DI LUCA, da prendere allora.
 IN SOSPESO, da scrivere tale e quale: la decisione (1) (proj = 0.5*(I_i+I_j)/Imed*(m_j-m_i).dir) va RICONFERMATA da Luca prima della sua cura, alla luce di due fatti emersi dopo: (a) mem_mot NON e' una velocita': rilassa verso grad_tw (:9130 su e2940b3c), quindi (m_j-m_i).dir e' circa la curvatura della torsione lungo l'arco, non un moto relativo (le simmetrie restano valide); (b) la forma decisa satura al taglio sul 55% degli archi e cambia la somma di Delta d0 da +6.7e3 a -9.2e4 (referto 2717308).
 Osservazione del guardiano, da registrare: dentro memoria_hebbiana_moto nessun passo usa il tempo proprio (mem_mot si aggiorna per passo senza dt, il taglio su d0 non ha tempo, i tetti usano DT). Va nella voce TETTO-CAUSALE-TEMPO-COORDINATO.

PARTE 2: LA CURA (2), decisione di Luca del 2026-10-04, confermata dal referto 2717308 (il sito scarta il 97.3% dei contributi, scartati/applicati = 36.2): il sito della fase in memoria_hebbiana_moto (phi[ii] = (phi[ii] + shift) % _dphi(), :9531 su e2940b3c, censiscilo dall'AST) si SPEGNE con un FLAG PROPRIO. MEM_MOTO_TUTTO e MEM_MOTO restano come sono, e mem_mot continua ad aggiornarsi.
 - Il flag nuovo, ACCESO, riproduce il comportamento di oggi; SPENTO, il sito non scrive phi. Il default del modulo e il driver lo tengono SPENTO: e' la fisica decisa. Rispetta le regole del repo sui flag (registro dei flag, configurazione dichiarata, P5).
 - FASE-TRASCINAMENTO-3D resta aperta: la legge in 3D NON si scrive ora.
 - Task history PRIMA del codice, con LA STELLA POLARE.
I CRITERI DEL SIGILLO, gia' fissati in b7e5a89 e qui precisati:
 - braccio 0: prima + patch committata = blob nuovo;
 - flag ACCESO: stato identico AL BYTE al blob e2940b3c su 150 passi, scena del driver, seme 11, lockstep su TUTTI gli attributi di net;
 - flag SPENTO: al primo passo le differenze stanno SOLO in phi (il sito e' l'ultima scrittura di memoria_hebbiana_moto, che e' l'ultima voce del passo). Se al passo 1 differisce altro, FERMATI. Dal passo 2 in poi le differenze si propagano: riportane la crescita per attributo, senza giudicarla;
 - CASO CHE DEVE FALLIRE: col flag spento phi DEVE differire al passo 1. Se non differisce, lo spegnimento non spegne niente: FERMATI.
Commit separati, in ordine: programma, task history, codice e strumento del sigillo, corsa e referto, con i blob citati.

NON CHIUDERE IL TURNO A META': ti fermi solo con "FERMO: <motivo>". Chiudi con "PUSHATO: <hash>". STOP.

---

## CHE COSA MANCA, PRIMA CHE QUESTO LAVORO POSSA PARTIRE

*(Nessuna di queste righe interpreta il mandato: sono **cose da fare** che il mandato stesso
elenca, messe in ordine perche' alla ripresa non si debba ri-leggerlo per capire da dove
cominciare.)*

1. ### **il commit del PROGRAMMA** — il `TODO ALLA RIPRESA` di
   `doc/TASK_HISTORY/2026-10-04_mem-hebb-verso-misura.md` e i **collegamenti** nelle tre
   voci d'indice *(`Z43`, `MEM-HEBB-VERSO`, `TETTO-CAUSALE-TEMPO-COORDINATO`)*;
2. **l'`IN SOSPESO` scritto TALE E QUALE:** la decisione `(1)` va ### **RICONFERMATA da
   Luca** prima della sua cura, coi **due fatti emersi dopo**;
3. **l'osservazione del guardiano** nella voce `TETTO-CAUSALE-TEMPO-COORDINATO`;
4. **il task history del passo (2)**, con `LA STELLA POLARE`, **prima del codice**;
5. il **censimento dall'AST** del sito `:9531`;
6. il **flag nuovo**, col **registro dei flag**, il **`README`** *(cosa fa, il **DEFAULT**,
   se e' byte-inerte)* e la **configurazione dichiarata** *(`P5`)*;
7. lo **strumento del sigillo** coi **quattro criteri**, e il **caso che deve fallire**;
8. la **corsa** e il **referto**, coi **blob citati**.

### ⚠ **DUE COSE DEL MANDATO CHE VANNO LETTE DUE VOLTE**

1. ### **IL DEFAULT E' SPENTO, ED E' UN RIBALTAMENTO:** *«il default del modulo e il driver
   lo tengono SPENTO: e' la fisica decisa»*. ### **Quindi il flag ACCESO riproduce oggi, ma
   il default lo SPEGNE** — e il par.6 ② pretende che, ### **nello stesso commit**, si
   cerchino **TUTTI i punti che ottenevano il vecchio comportamento per OMISSIONE.**
2. ### **`FASE-TRASCINAMENTO-3D` RESTA APERTA:** *«la legge in 3D NON si scrive ora»*.
   ### **Spegnere non e' curare**, e la voce non si chiude.

### 📌 **E UNA COSA CHE QUESTO MANDATO CAMBIA RISPETTO A IERI, da non perdere**

Il referto `2717308` chiudeva dicendo che restava a Luca la **riconferma** della decisione
`(1)`. ### **Qui Luca la mette in SOSPESO ESPLICITO, con due fatti nuovi** — e il secondo
*(`(a)`: `mem_mot` **non e' una velocita'**, rilassa verso `grad_tw`, quindi
`(m_j - m_i).dir` e' **circa la curvatura della torsione lungo l'arco**)* ### **non era nel
mio referto: e' una lettura del guardiano, e va registrata come sua.**

---

# LA CURA (2) — **scritto il 2026-10-05, PRIMA del codice**

## IL CENSIMENTO DALL'AST: **il sito, e che cosa gli sta intorno**

### ✅ **`:9531` E' L'UNICA SCRITTURA DI `phi` IN `memoria_hebbiana_moto`**

```python
self.phi[ii] = (self.phi[ii] + shift_fase_dinamico) % self._dphi()
```

**Le scritture di `self.phi` in TUTTO il file, dall'AST** *(10 siti)*: `:1832` e `:2261`
*(le regole di nascita)*, `:3888` *(`__init__`)*, `:4959` *(`semina`)*, `:7757`
*(`step`)*, `:8739-8751` *(`mitosi`, tre siti)*, `:9881`
*(`_semina_masse_coerenti`)*, e ### **`:9531`, che e' l'unico dentro
`memoria_hebbiana_moto`.**

### ✅ **ED E' L'ULTIMA SCRITTURA DI STATO DELLA FUNZIONE**

Le scritture di stato in `memoria_hebbiana_moto` *(`:9080-9533`)*, dall'AST, in ordine:
`:9110` e `:9130` *(`mem_mot`)*, `:9156`, `:9302`, `:9308`, `:9330`, `:9480`, `:9482`
*(`d0`)*, e ### **`:9531` (`phi`), l'ULTIMA.** Dopo di essa restano solo due righe di
traccia *(`TRACCIA_D0`, che e' **`False`** nella configurazione del driver)*.

### ✅ **E `memoria_hebbiana_moto` E' L'ULTIMA LEGGE DELLA COMPOSIZIONE** *(voce 5)*: il
codice lo **dichiara** a `:9534-9541`, e dopo di lei lo **schedulatore** fa `chiudi`
*(il freno su `d0`)* e `verifica_invarianti`.

> ### 📌 **QUESTE TRE COSE INSIEME SONO LA RAGIONE PER CUI IL CRITERIO <<al passo 1 le
> ### differenze stanno SOLO in `phi`>> E' VERIFICABILE**: non c'e' nessuna legge, dopo,
> ### che possa propagare la differenza **dentro lo stesso passo.**
> ### ⚠ **E IL FRENO SU `d0` GIRA DOPO, ma non legge `phi`:** applica `_smorza` alla
> variazione di `d0` dallo snapshot di inizio passo. ### **Se al passo 1 differisse `d0`,
> vorrebbe dire che ho letto male questa catena, e il mandato dice FERMATI.**

## IL FLAG: **`MEM_FASE`**, e perche' questo nome

> ### ⛔ **IL NOME NON E' NEL MANDATO** *(dice solo <<un FLAG PROPRIO>>)*, ### **quindi
> ### lo scelgo io e lo dichiaro.**

| flag | che cosa recinta |
|---|---|
| `MEM_MOTO` | la scrittura della memoria del moto su ### **`d0`** *(il sito `S08_proj`)* |
| ### **`MEM_FASE`** *(nuovo)* | la scrittura della memoria del moto su ### **`phi`** *(il sito `:9531`)* |
| `MEM_MOTO_TUTTO` | ### **l'intero blocco**, i quattro punti |

### **Il nome segue la coppia che esiste gia': `MEM_MOTO` -> `d0`, `MEM_FASE` -> `phi`.**
### **Un nome che non dicesse SU CHE COSA scrive sarebbe un nome peggiore**, ed e' la
ragione per cui non lo chiamo `MEM_DRAG` o `MEM_SHIFT`.

**DOVE VIVE:** fra le ### **costanti di modulo SENZA flag da riga di comando**
*(`README.md` § 9-bis)*, accanto a `MEM_MOTO` e `MEM_MOTO_TUTTO`.
### **Nessuna opzione da riga di comando, come i suoi due fratelli:** *«non devono poter
essere accese per sbaglio da un comando»*.

## ⛔ **IL DEFAULT E' `False`, E QUESTO NON E' UN FLAG BYTE-INERTE**

> ### **Decisione di Luca:** *«Il default del modulo e il driver lo tengono **SPENTO**:
> ### e' la fisica decisa»*.

### ⛔ **E QUINDI VA DETTO FORTE, perche' e' il contrario del caso normale:** quasi tutti
i flag di questo repo nascono ### **OFF e byte-inerti** *(la regola d'oro: «tutti i flag
nuovi OFF di default», e OFF significa **niente cambia**)*.
### **Qui OFF significa CHE LA FISICA CAMBIA**, perche' il flag **recinta una legge che
oggi gira** e il default la **spegne**.

| | |
|---|---|
| `MEM_FASE = True` | riproduce il comportamento di **oggi** — ### **byte-identico a `e2940b3c`** |
| `MEM_FASE = False` *(**il DEFAULT**)* | ### **il sito non scrive `phi`: la fisica cambia** |

### 📌 **LA CONSEGUENZA SU TUTTO IL REPO, che dichiaro ORA e che il par.6 ② pretende:**
### **ogni sigillo e ogni rigiocata che RI-ESEGUE il simulatore dara', da questo commit
in poi, numeri DIVERSI dai suoi referti.** Non e' un difetto: ### **e' la fisica che
cambia, e i referti sono legati al loro BLOB.** *(Par.6: un sigillo si rigira con
`git checkout` del commit che ha sigillato.)*
### ⚠ **E NON C'E' UN <<PUNTO CHE OTTENEVA IL VECCHIO COMPORTAMENTO PER OMISSIONE>> da
cercare**, perche' il flag e' **nuovo**: ### **prima non esisteva, e il vecchio
comportamento era l'UNICO.** ### **Il punto da cercare e' l'opposto: chi vuole il
vecchio comportamento deve ora ACCENDERLO**, e nessuno lo fa — ### **e' esattamente la
decisione di Luca.**

## LA STELLA POLARE — **le cinque risposte, PRIMA del codice** *(`L-STELLA`)*

### **1. `A14`: conserva energia e carica LOCALMENTE?**

### **LA CARICA: non si applica.** Il sito scrive `phi`, che e' una **fase**; `perc_chi`
e `psi` non sono toccati.
### ⚠ **L'ENERGIA: non e' rispondibile, ed e' un fatto del repo** — `ENERGIA-NON-DEFINITA`:
### **il modello non ha un'energia totale.** Non dico <<conserva>>.

> ### 📌 **MA UNA COSA VA DETTA, ed e' il numero del referto `2717308`:** il sito
> ### **scartava il `97.3%` dei contributi che calcolava** *(rapporto moduli
> ### scartati/applicati `36.2`)*, e lo scarto era deciso ### **dall'ORDINE DELL'ARRAY**
> *(`phi[ii] = ...` con `ii` ripetuto: vince l'ultimo)*.
> ### **Quindi spegnerlo NON rompe una conservazione che c'era: toglie un contributo che
> ### NON era una legge**, perche' il suo valore dipendeva da **come gli archi erano
> ### memorizzati.**

### **2. A quale dei TRE GRADINI arriva il risultato?**

| gradino | risposta |
|---|---|
| **(a)** robusto al rumore numerico | ### ✅ **SI', e nella forma piu' forte che esista qui:** col flag **ACCESO** il sigillo pretende ### **l'identita' AL BYTE** con `e2940b3c` su `150` passi. ### **Non <<entro una barra d'errore>>: AL BYTE.** |
| **(b)** regge togliendo la legge pratica | ### ✅ **SI', E L'HO GIA' MISURATO:** la legge pratica del sito e' il taglio `pi/4`, e il referto `2717308` dice che morde sullo ### **`0.0011`**. ### **Cio' che il sito fa NON e' il taglio** — e' <<l'ultimo vince>>, che morde sullo **`0.973`** |
| **(c)** coincide con un limite noto | ### ✅ **SI':** col flag **acceso**, ### **il limite e' il blob di oggi**, e il sigillo lo verifica al byte |

### **3. Aggiunge un numero o una legge?**

### **NESSUN NUMERO: ZERO.** Il flag e' un **booleano**, non un parametro.

**IL CONTO DELLE LEGGI** *(`9-ter`)*: ### **il conto SCENDE DI UNO.** Una legge che
girava **esce dal percorso**, e ### **non ne entra nessuna al suo posto** —
`FASE-TRASCINAMENTO-3D` resta **aperta**, e la legge in 3D ### **NON si scrive ora.**

### ⚠ **E IL FLAG E' UN'ECCEZIONE IN PIU' O IN MENO? Lo dichiaro come IN PIU':** un `if`
nuovo nel percorso e' ### **un ramo in piu' da leggere**, anche se il ramo acceso non
gira mai. ### **Lo accetto perche' e' la forma che il repo usa gia' per `MEM_MOTO` e
`MEM_MOTO_TUTTO`** — ### **la TERZA volta della stessa forma**, non una forma nuova —
### **e perche' il mandato lo chiede esplicitamente** *(«si SPEGNE con un FLAG
PROPRIO»)*.

### **4. Tocca `rho`, `c_s` o il SEGNO?**

### ⚠ **INDIRETTAMENTE SI', E VA DETTO:** `phi` entra in `calcola_psi` *(`F = W@(amp *
exp(1j*phi))`, `:6227`)*, quindi tocca `psi`, quindi `|psi|^2`, quindi ### **`rho` e
`cs`** — ### **dal passo DOPO.** ### **Non e' <<non li tocca>>: e' <<li tocca a
valle>>**, ed e' la ragione per cui il criterio del mandato dice *«dal passo 2 in poi le
differenze si propagano»*.

**IL SEGNO:** `shift_fase_dinamico` ha un **segno** *(da `proiezione_trasversale`)*, e
spegnerlo toglie un contributo **firmato**. ### **Non e' l'asse `EM <-> curvatura`** della
domanda 4: e' **torsione -> fase**.

### **5. Emergente o imposto: il fenomeno sopravvive se si toglie la legge pratica?**

> ### ⛔ **QUESTA E' LA DOMANDA CHE QUESTA CURA HA GIA' RISPOSTO, e la risposta e'
> ### MISURATA:** cio' che il sito produceva era ### **IMPOSTO DALL'ORDINE DELL'ARRAY**,
> non emergente. ### **Il `97.3%` dei contributi spariva in silenzio, e QUALE
> sopravvivesse dipendeva da come gli archi erano ordinati.**
> ### **Un fenomeno che cambia se riordini un array NON e' un fenomeno del sistema.**

### ⚠ **E LA PARTE ONESTA DELLA RISPOSTA:** ### **non so che cosa si perde.** Il `2.7%`
che veniva applicato ### **era un contributo vero alla fase**, e spegnerlo lo toglie.
### **Il sigillo misurera' QUANTO cambia a valle, e il referto lo riportera' SENZA
giudicarlo** — come il mandato prescrive.

## I CRITERI DEL SIGILLO — **fissati e committati PRIMA del codice**

*(Gia' fissati in `b7e5a89`, e qui **precisati dal mandato**.)*

| | che cosa pretende | e se fallisce |
|---|---|---|
| **`0`** | **braccio 0**: *prima* + patch committata = **blob nuovo** | ### **la patch non e' quella dichiarata: FERMO** |
| **`1`** | flag **ACCESO**: ### **stato identico AL BYTE** a `e2940b3c` su `150` passi, scena del driver, seme `11`, lockstep su ### **TUTTI** gli attributi di `net` | ### **il flag NON e' byte-inerte da acceso: FERMO** |
| **`2`** | flag **SPENTO**, ### **al PRIMO passo**: le differenze stanno ### **SOLO in `phi`** | ### ⛔ **se differisce altro, FERMO** |
| **`3`** | ### **CASO CHE DEVE FALLIRE:** col flag spento `phi` ### **DEVE differire al passo 1** | ### ⛔ **se non differisce, lo spegnimento non spegne niente: FERMO** |
| **`4`** | dal passo **2** in poi: ### **riportare la CRESCITA delle differenze per attributo**, ### **senza giudicarla** | — |

### ⛔ **IL CRITERIO `3` E' IL PIU' IMPORTANTE, e lo scrivo ORA perche' e' facile da
### dimenticare:** un flag che spegne un sito ### **potrebbe non cambiare NIENTE** se il
sito scrivesse valori gia' uguali. ### **Qui non dovrebbe succedere** — il referto
`2717308` misura `shift` con mediana `4.26e-03`, non zero — ### **ma <<non dovrebbe>>
non e' <<non succede>>, e il criterio lo pretende.**

### ⚠ **E IL CRITERIO `2` HA UNA TRAPPOLA CHE DICHIARO ORA:** il sito applica anche
### **`% self._dphi()`**, non solo la somma. ### **Spegnerlo toglie ANCHE la
normalizzazione modulo `4pi` su `phi[ii]`.** Il codice lo dichiara a `:9516-9517`:
*«`(phi + 0) % (4 pi)` e' un NO-OP **solo se `phi` sta gia' nel dominio**»*.
### **Quindi se `phi` uscisse dal dominio, la differenza al passo 1 sarebbe piu' grande
di `shift`** — e il sigillo deve ### **riportare la differenza, non solo contarla.**

## L'ORDINE DEI COMMIT

1. ### ✅ **il programma** *(`e04b6bf`)*;
2. ### **questo task history**, pushato **PRIMA** del codice *(par.8)*;
3. **il codice e lo strumento del sigillo**, con il `README`, il blocco dei flag e
   l'**inventario** *(par.6)*;
4. **la corsa e il referto**, ### **coi blob citati.**

## TODO DEL NEXT STEP — **operativo**

1. **commit di questo task history**;
2. il flag **`MEM_FASE = False`** nel blocco delle costanti di modulo, il `README`
   § 9-bis *(cosa fa, **il DEFAULT**, ### **byte-inerte: NO al default**)*, e il
   gate `if MEM_FASE:` attorno a **`:9531` e basta**;
3. la **patch del braccio 0**, ### **estratta dal sorgente curato e non ritrascritta**;
4. lo **strumento del sigillo** coi **cinque criteri**, e il **caso che deve fallire**;
5. la **corsa** e il **referto**, con la **crescita delle differenze per attributo**;
6. **relazione** e **voci d'indice** nello stesso giro *(par.4)*;
7. ### **`FASE-TRASCINAMENTO-3D` RESTA APERTA:** la legge in 3D ### **NON si scrive
   ora.**

### ⛔ **CIO' CHE NON SI FA:** ### **la cura (1)** *(la forma di `proj`)*, che e' al
**punto 4** del programma e ### **la cui decisione resta DA RICONFERMARE da Luca**; e
### **nessuna legge in 3D.**
