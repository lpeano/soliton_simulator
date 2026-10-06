# 🧭 **`GEOM-SENZA-VERSO`** *(voce nuova, 2026-09-29)*

> # ⭐ **LA STELLA POLARE** *(principio guida, **DECISO DA LUCA** il 2026-09-29)*
>
> ## **A. LE LEGGI SONO SIMMETRICHE, GLI STATI SCELGONO.**
> ### **Nessuna legge deve preferire un verso di rotazione.** Se un verso prevale, deve
> ### **EMERGERE dall'evoluzione** *(rottura **SPONTANEA**)*, **non essere scritto nella legge**.
>
> ## **B. UNA ROTTURA ESPLICITA E' AMMESSA SOLO COME POSTULATO DICHIARATO**
> **un solo termine**, **nominato**, **col suo peso**, **accendibile e spegnibile**,
> **confrontabile**. ### ⛔ **Mai come effetto collaterale di un valore assoluto.**
>
> ## **C. TRE GRANDEZZE, TRE MESTIERI, MAI MESCOLATI**
>
> | grandezza | il suo mestiere | da dove viene |
> |---|---|---|
> | `perc_geom` | ### **«avvolto si' o no»** — **DOVE** c'e' materia avvolta | l'**INTENSITA'** `\|tw\|` |
> | *(oggi non esiste)* | ### **VERSO DI ROTAZIONE** del nucleo — orario / antiorario | il ### **SEGNO della circolazione** della torsione |
> | `perc_chi` | ### **CARICA** — materia / antimateria | il **foglio della doppia copertura** dello spinore |
>
> ## **D. LA DIREZIONE SCELTA E' LA STRADA (ii)**
> `perc_geom` **resta si'/no**; la **catena della rotazione** *(frame-drag, chiralita' del core,
> `TORS_4PI`)* ### **legge il verso dalla CIRCOLAZIONE CON SEGNO**.
>
> | | |
> |---|---|
> | ### ⛔ **(i) scartata** | rimetterebbe **due informazioni in una variabile**: ### **l'errore GIA' CORRETTO con `CHI_COOP`** |
> | **(iii)** | resta **solo se la misura mostra che il problema non esiste** |

> ### ⚠ **SOLO REGISTRAZIONE. Nessun codice di fisica, nessuna misura ancora fatta.**
> **Mandato di Luca:** *«DA FARE DOPO il sigillo del controllo unico.»* ### **In coda, dichiarata**
> *(`L-UN-PROMPT`)*. ### **E nessun codice di fisica finche' Luca non decide.**

### ✅ **La lettura del guardiano e' VERIFICATA SUL CODICE, e le righe sono quelle di `9cf6fb07`**

⚠ **Le righe del mandato venivano da un blob precedente** *(`:5894` `:5921` `:5715` `:5860`)*: il
mio ha **~200 righe in piu'**, quindi ho cercato **per nome**, non per riga *(par.2)*.

| che cosa | dove, su `9cf6fb07` | verificato |
|---|---|---|
| la **definizione** di `perc_geom` | `:6076`-`:6083`: `twabs = abs(_tw_src)`, accumulata sui **due** estremi, divisa per `_deg`, poi `where(twn > soglia, 1, -1)` | ### ✅ **e' la MEDIA di `|tw|` sugli archi del nodo, contro una soglia** |
| la soglia | `PHI_CRIT = 2*np.pi` *(`:516`)*, **locale, non la mediana globale** | ### ✅ **un QUANTO di olonomia: un giro compiuto** |
| `perc_chi` = **carica** | `:6110`, `where(real(_ov) >= 0, 1, -1)`: ### **il foglio della doppia copertura, dal segno dell'overlap spinoriale** | ### ✅ |
| `perc_geom` riscritta **per tutti** i nodi a ogni passo | `:6083`, dentro `chi_basc` con `CHI_COOP` | ### ✅ **non si conserva, non e' una carica** |
| `twist_dip` **con segno** | `:6061`: `pi * 0.5 * (chi_torsione[i] - chi_torsione[j])`, e `chi_torsione` viene da `perc_geom` *(`:6049`-`:6051`)* | ### ✅ |
| ### **l'ORDINE nel passo** | i lettori della catena stanno a `:5908` e `:5917`, ### **PRIMA** della riscrittura a `:6083` | ### ✅ **il frame-drag legge il valore del passo PRECEDENTE** |

## ⛔ Il problema, in una frase

> ### **`tw` HA UN SEGNO — il verso in cui la differenza di fase si avvolge — e `perc_geom` lo
> ### BUTTA VIA, perche' nasce da `|tw|`. Poi la catena della torsione la usa COME SE avesse un
> ### verso.**

### ➜ **Due nuclei avvolti in versi OPPOSTI ricevono la STESSA etichetta `+1`.**
Il *«verso»* che la catena produce dice **«da un nodo avvolto verso uno non avvolto»** *(dal centro
verso fuori)*, ### **non «orario o antiorario»**. ### **La fisica della rotazione — trascinamento,
chiralita' del core — non puo' distinguere il verso di rotazione di un nucleo.**
**E la grandezza CON verso esiste:** il **segno di `tw`**, e `perc_chi` *(che pero' e' la **carica**,
un'altra cosa)*.

## 🔁 L'anello

```
tw  ->  |tw|  ->  perc_geom  ->  twist_dip  ->  tw
```

### **La torsione alimenta un'etichetta SENZA verso che rientra nella torsione come se lo avesse.**
Va descritto in `doc/REGISTRO_FISICA.md` **come legge**, col suo **ordine nel passo**.

## 📐 LA MISURA — **criteri fissati ORA, prima dei numeri**

**Scena GRANDE** *(`nmasse 3`, `sep 6.1158` **da `a`**)*, seme `11`, **argv del driver**, ai passi
**30**, **60** e **72**.

| | |
|---|---|
| **(a)** | **verso di avvolgimento per nodo**: la somma **FIRMATA** di `tw` sui suoi archi, ### ⚠ **orientando ogni arco USCENTE dal nodo** — `+tw` se il nodo e' `i`, `-tw` se e' `j`. ### **Il segno di `tw` e' relativo all'orientamento `(i, j)`: senza orientarlo la somma non ha senso** |
| **(b)** | **verso di circolazione sui cicli**, con `_base_cicli_topologici` e `circolazione_topologica` *(esistono gia')*: da' il verso ai nuclei ### **in modo INDIPENDENTE da (a)** |
| **(c)** | per i nodi con `perc_geom = +1`: **istogramma** del verso (a) e della circolazione (b) |

### Gli esiti, decisi prima

| | |
|---|---|
| ### **DIFETTO DIMOSTRATO** | esistono nuclei avvolti in **ENTRAMBI** i versi che ricevono la stessa etichetta — ### **almeno il 10 % nel gruppo minoritario, su almeno uno dei due metodi** |
| **DIFETTO DI PRINCIPIO, NON ATTIVO** | tutti i nuclei hanno **lo stesso** verso. Allora va capito ### **PERCHE' nascono tutti cosi'** — possibile **rottura di simmetria introdotta proprio da questa catena** — e si riporta |
| ### 🛑 **SI FERMA E SI DICE** | se **(a)** e **(b)** ### **non concordano fra loro**: allora ### **il verso non e' ben definito cosi'**, e non si va avanti |

## ⛔ **IL SOSPETTO DA VERIFICARE, ed e' la motivazione di `A`**

> ### **Specchiando il sistema** *(fasi invertite)* **`tw` cambia segno, ma `|tw|` NO — quindi
> ### `perc_geom` no — quindi `twist_dip = pi/2 (chi_i - chi_j)` NON cambia segno.**

### ➜ **La legge aggiunge alla torsione LO STESSO contributo nel mondo specchiato: e' una rottura
ESPLICITA della simmetria, probabilmente INVOLONTARIA.**
### **E se i nuclei risultassero tutti dello stesso verso, potrebbe essere QUESTO TERMINE e non
fisica emergente.**

⚠ **La riga:** il mandato cita `:5872`; su `fc9ef41c` `twist_dip` sta a ### **`:6061`** — le righe
**shiftano fra i blob**, e ho cercato **per nome** *(par.2)*.

---

## 🪞 **AGGIUNTA 7 — LA PROVA DELLO SPECCHIO** *(dopo la misura del par. precedente)*

| | |
|---|---|
| ### **(a) PRIMA di girare** | ### **PROPORRE A LUCA la trasformazione di specchio COMPLETA** per questo modello: **quali grandezze cambiano segno e quali no** *(`phi`, `phi0`, `phivel`, `tw`, `twp`, lo **spinore e le sue cache**, `omega_s`, `_nb`, `perc_chi`, ed eventuali altre)*, ### **con la RAGIONE per ciascuna**. ### ⛔ **Non si gira finche' Luca non approva: definire lo specchio e' una scelta di FISICA** |
| **(b)** | scena **grande**, seme `11`, stato al passo **30**; copia **A** normale, copia **B** **specchiata**; **N** passi pieni su entrambe, con ### **N scelto e DICHIARATO prima** |
| ### **(c) il CRITERIO, fissato ORA** | se le leggi sono simmetriche, per **ogni** grandezza lo stato di **B** deve essere ### **lo specchio di quello di A entro l'errore numerico**. Si riporta ### **la PRIMA grandezza e il PRIMO passo in cui lo specchio si rompe, e la RIGA che lo produce** |
| ### **(d) il caso che DEVE fallire** | con `twist_dip` **com'e' adesso**, lo specchio ### **DEVE rompersi** se il sospetto e' giusto. ### **Se NON si rompe, il sospetto CADE — e si dice.** |

---

## 🛑 LE TRE STRADE — **decide Luca, non io: qui solo pro e contro**

| | la strada | pro | contro |
|---|---|---|---|
| **(i)** | `perc_geom` **a tre valori**: `+1`/`-1` secondo il **verso** se il giro e' compiuto, **`0`** se non lo e' | ### **il verso c'e', e l'intensita' resta**: una sola grandezza dice entrambe le cose | **cambia il dominio** di una variabile che oggi e' `±1`, e ### **`0` e' un valore NUOVO** per tutti i suoi lettori |
| **(ii)** | la catena della rotazione **legge il verso da `tw` o dalla circolazione**, e `perc_geom` resta *«giro compiuto si'/no»* | ### **ogni grandezza fa UN lavoro**, e il verso viene da dove il verso **esiste** | tocca **piu' lettori** *(frame-drag, chiralita' del core, `TORS_4PI`)* |
| **(iii)** | **lasciare tutto com'e'**, se e' una scelta di fisica **voluta** | **zero rischio**, zero righe | ### **allora va SCRITTO nel registro PERCHE' un'intensita' vale come chiralita'** — e oggi non c'e' scritto |

> ### 📌 **`9-ter`:** la **(ii)** *«toglie un'eccezione»* — una variabile, un lavoro — ma va misurato
> **sulle leggi**, non sui rami del programma. La **(i)** ### **non aggiunge una legge, cambia un
> dominio**. La **(iii)** ### **non aggiunge codice ma aggiunge una DICHIARAZIONE**, che e' il suo
> costo vero.

## 🔗 Il collegamento con la decisione **gia' presa**

**`perc_geom` del NATO = `-1`**, *derivata dalla definizione*, perche' gli archi nuovi hanno
`tw = 0` *(divisione e Schwinger)*. ### ✅ **Resta valida con QUALUNQUE strada: un nodo con torsione
zero non ha compiuto il giro.** *(Quella e' una voce a se', con commit e sigillo separati.)*

## La consegna, nell'ordine chiesto

1. **task history PRIMA** *(par.8: si committa prima del lavoro)*;
2. **lo strumento della misura, committato PRIMA di girare**;
3. **il referto**;
4. **la voce nell'indice** *(questa)*;
5. ### **STOP, e i numeri a Luca.**

---

# ANNOTAZIONE *(2026-10-06 — `par.8`: si ANNOTA, non si riscrive)*

## **LA PROPOSTA DI PROGETTO PER LA STRADA `(ii)`**

*(Mandato di Luca del 2026-10-06, dopo il referto `27c10bd`. ### ⛔ **SOLO UNA PROPOSTA:
nessun codice di fisica, e la forma esatta della legge e' una decisione di Luca.**)*

---

## ① IL MECCANISMO E' CONFERMATO, e non e' piu' un sospetto

Il referto `27c10bd` *(due bracci, `1000` passi)* ha misurato:

| | `_AMP = 0` | `_AMP = 0.3` |
|---|--:|--:|
| frazione della spinta oltre `π` con la componente di ### **dipolo** | ### **`0.9935`** | ### **`0.9704`** |
| `Spearman`(cambi di `chi_torsione`, archi oltre `4π`) | ### **`0.9090`** | ### **`0.6961`** |

> ### ✔ **L'anello `tw → |tw| → perc_geom → dipolo → tw` NON e' piu' un'ipotesi:** il `97`-`99 %`
> della spinta oltre `π` passa dal ### **dipolo**, e il dipolo cambia ### **solo** quando
> `chi_torsione` cambia.
>
> ### ⚠ **E la correlazione e' su una serie BUCATA** *(`392` e `731` passi esclusi su `1000`,
> `CHI-TORS-ZERO-FALSO`)*: ### **la gamba solida e' la FRAZIONE, non la correlazione.**

**E il meccanismo e' esatto nel codice:** `twist_dip = π·0.5·(chi_torsione[i] − chi_torsione[j])`
sta in `{−π, 0, +π}`, quindi ### **un nodo che attraversa `2π` cambia il dipolo di `±π` su
TUTTI i suoi archi in un colpo** — e con la legge curata il dipolo entra ### **come
VARIAZIONE**, quindi quel `±π` ### **entra in `tw` per intero, in un passo solo.**

---

## ② ⛔ `U1` ENTRA NEL DIPOLO, **e la risposta cambia la forma della cura**

*(Integrazione chiesta da Luca. ### **Verificato col comando**, non assunto.)*

### IL FATTO, letto dal codice

`chiralita_core_locale` calcola:

```
try:    rho_c = massa_critica_adattiva(self) / ((4/3)·π·LAM_BASE³)
except: rho_c = massa_critica_collasso()    / ((4/3)·π·LAM_BASE³)
...
rapporto = rho0[k] / max(rho_c, 1e-12)
r        = lam_loc[k] · log(rapporto)  if rapporto > 1.0  else 0.0
if r <= 0.0:  continue          # ### il nodo NON ha core: chi_core[k] resta chi[k]
```

> ### ⛔ **E IL RAMO ADATTIVO NON SFUGGE A `U1`:** `massa_critica_adattiva` ### **chiama la
> STESSA `massa_critica_collasso`**, solo con `s` misurato dal campo. ### **La legge rotta e'
> nel percorso di ENTRAMBI i rami.**

### LA RISPOSTA ALLE TRE DOMANDE DI LUCA

**① *Quanto di cio' che il dipolo legge dipende dalla soglia irraggiungibile di `U1`?***

Con `--chi-core` **e** `--chi-coop` accesi, `chi_torsione` e' ### **`_chi_geom_nodi`**, prodotto
da `chiralita_core_locale(perc_geom, geom=True)`. E quella funzione ### **cambia `chi` SOLO per
i nodi con `rapporto > 1`.**

**Se nessun nodo superasse `rapporto > 1`, il ciclo farebbe `continue` per tutti e
`chiralita_core_locale` restituirebbe `chi` ### **immutata**: `_chi_geom_nodi == perc_geom`, e
### **`--chi-core` sarebbe INERTE per il dipolo.**

> ### ⛔ **MA QUESTO NON SEGUE DAL `48×` DI `U1`, E IO L'AVEVO DEDOTTO COSI'.** In
> `ff94e70` ho scritto *«se la soglia e' `48×` irraggiungibile, `chiralita_core_locale` e'
> un no-op»*: ### **e' un NON SEQUITUR, e lo ha trovato Luca.**
>
> | | |
> |---|---|
> | il `48×` di `U1` | un conto ### **in NODI**: `621` chiesti in una palla che ne contiene `13` |
> | il test qui | `rho0 = max |ψ|²` nel vicinato contro `rho_c = massa_critica_adattiva / volume`, cioe' ### **una DENSITA'** |
>
> ### ⛔ **Sono due scale diverse.** Che `rapporto` superi `1` o no ### **dipende dalla
> scala di `|ψ|²`**, che il `48×` ### **non dice.** ### **Il ragionamento sul
> codice resta giusto** *(`chi_core` resta `chi` dove `rapporto <= 1`)*; ### **la conclusione
> NON si deduce: SI MISURA.**
>
> ### ⚠ **E l'errore ha una forma che conosco: ho preso un numero vero di una voce e l'ho
> portato in un posto dove misurava un'altra cosa** — la stessa famiglia del *«per passo»*
> che stampava una somma.

**Un indizio, e lo riporto per quello che vale:** nel giro corto a `4` passi di
`_mitosi_zero_dove` i cambi di `chi_torsione` e quelli di `perc_geom` erano ### **ESATTAMENTE
gli stessi `6419`** — ### **compatibile con un no-op, e NIENTE DI PIU'.** Sui `1000` passi
i due numeri divergono *(`13786` contro `23363`; `6592` contro `74685`)*, ### **ma
`cambi_chi_tors` e' sottocontato dal falso-zero di `CHI-TORS-ZERO-FALSO`**, quindi ### **quei
numeri NON decidono.**

### ⛔ **IL PRIMO PASSO DI TUTTO IL PROGETTO E' QUESTA MISURA** *(mandato di Luca)*

**Sulla scena delle corse di oggi** *(argv del driver, seme `11`, simulatore ### **`30e18cdd`**
— quello ### **dopo** <<via il `0.3`>>)*, ai passi ### **`1`, `50`, `150`, `230`**, si
chiama `chiralita_core_locale(perc_geom, geom=True)` ### **in SOLA LETTURA** e si contano
### **tre numeri:**

| | che cosa si conta |
|---|---|
| **`(a)`** | i nodi con ### **`rapporto > 1`**, cioe' con `r > 0` |
| **`(b)`** | il ### **MASSIMO** di `rapporto` |
| **`(c)`** | quanti elementi di `_chi_geom_nodi` sono ### **diversi** da `perc_geom` |

### ⛔ **IL CRITERIO, FISSATO ORA E PRIMA DELLA CORSA**

| | la lettura |
|---|---|
| ### **`(a) = 0` E `(c) = 0` a TUTTI i passi** | ### **`--chi-core` e' INERTE per il dipolo**: il dipolo legge `perc_geom` ### **direttamente**, e `U1` esce dal percorso |
| altrimenti | si riporta ### **DOVE e QUANTO agisce**: il numero di nodi, il massimo di `rapporto`, e i passi |

> ### ⚠ **E `(b)` SERVE ANCHE SE `(a)` E' ZERO**, ed e' la ragione per cui lo chiedo: un
> massimo di `rapporto` a ### **`0.98`** e uno a ### **`0.001`** danno lo stesso `(a) = 0` ma
> dicono due cose ### **opposte** su quanto il sistema sia ### **vicino** ad accendere quel
> ramo. ### **Uno zero senza la sua distanza dalla soglia e' un'informazione a meta'.**

### ⛔ **E NON SI LEGGONO I DIAGNOSTICI `_chi_core_*`** *(verificato nel codice e nel suo
docstring)*: il ramo `geom=True` scrive ### **SOLO `_chi_geom_nodi`**, mentre
`_chi_core_rho0`, `_chi_core_rhoc` e `_chi_core_raggio` ### **li scrive il ramo
`geom=False`.** ### **Leggerli darebbe i valori di UN ALTRO RAMO**, cioe' un numero giusto
che risponde alla domanda sbagliata.

> ### ✔ **LO STRUMENTO SI COMMITTA PRIMA DELLA CORSA**, e ### **la corsa si fa SOLO DOPO
> che il sigillo di <<via il `0.3`>> ha finito E PASSATO** *(il sigillo confronta il file del
> simulatore)*. ### **E' una corsa CORTA: `230` passi, un braccio.**

### ➕ **E ALLA STESSA CORSA SI AGGIUNGE LA MISURA DI `c_k`** *(mandato di Luca,
`MASSA-CRITICA-LOCALE`)*

### **Stessa corsa corta** — scena di oggi, seme `11`, `30e18cdd`, passi `1`/`50`/`150`/
`230`, ### **sola lettura**, dopo che il sigillo e' passato — e si misura la
### **coerenza locale**

```
D_k = satura( amp * somma_j |W_kj| )        <- il denominatore, SATURATO come il numeratore
c_k = |psi_k|^2 / |D_k|^2
```

> ### ⛔ **E IL DENOMINATORE VA SATURATO, non lasciato nudo:** `satura` e'
> ### **monotona** e ### **satura a `1/GAMMA`**, quindi un numeratore saturato diviso un
> denominatore nudo ### **renderebbe `c = 1` IRRAGGIUNGIBILE** dove la somma supera
> `~1/GAMMA`. ### **Con entrambi saturati, `c = 1` ⇔ fasi tutte allineate, ESATTO.**
> *(Verificato da me su `calcola_psi`, `satura` e `_mat`: il dettaglio in
> `doc/STATO_RUN.md::MASSA-CRITICA-LOCALE`.)*

### ⛔ **I CRITERI, FISSATI ORA E PRIMA DELLA CORSA**

| | che cosa si riporta |
|---|---|
| **`(a)`** | la ### **distribuzione** di `c_k` ### **e del denominatore `D_k`**, separata per classe ### **`MATERIA` / `BORDO` / `VUOTO`** |
| **`(b)`** | le stesse, ### **per NUMERO DI VICINI** — cosi' il difetto del ### **nodo isolato** *(un vicino ⇒ `c = 1` per costruzione)* ### **si VEDE invece di essere ricordato** |
| **`(c)`** | ### **se `c_k` separa le classi:** l'### **`AUC`** o la ### **sovrapposizione** delle distribuzioni ### **`MATERIA` contro `VUOTO`** |

> ### ⛔ **E' UNA MISURA, NON UNA LEGGE: NON DECIDE NIENTE.** Serve a sapere
> ### **se `c_k` ha il potere di separare** prima che qualcuno ci costruisca sopra una
> soglia. ### **E il denominatore si riporta SEMPRE accanto a `c_k`**, perche' il difetto
> `(a)` del guardiano dice che ### **`c` da solo non basta.**

**② *Una cura di `GEOM-SENZA-VERSO` che non tocca `U1` sarebbe costruita sopra una legge
rotta?***

> ### ⚠ **SI', MA IN DUE MODI DIVERSI, e la differenza decide la risposta:**
>
> | se `chiralita_core_locale` e' | allora la cura del verso |
> |---|---|
> | ### **un NO-OP** *(### **da MISURARE**, non dedotto dal `48×`)* | ### **NON e' costruita sopra `U1`**: il dipolo legge `perc_geom` ### **direttamente**, e `U1` e' irrilevante ### **per questo cammino.** ### ⚠ **Ma allora `--chi-core` e' un flag che NON FA NIENTE, ed e' un `A8` da registrare** |
> | ### **ATTIVA su qualche nodo** | ### **SI', e su quei nodi il verso nuovo passerebbe per una soglia sbagliata di `48×`** |
>
> ### ⛔ **Quindi la domanda NON si risponde in astratto: si risponde con la misura del
> punto sopra**, e ### **rispondere senza misurarla sarebbe esattamente il modo in cui
> si cura alla cieca.**

**③ *La cura va fatta INSIEME a `U1`, per la sola `chiralita_core_locale`, PRIMA o DOPO?***

### ✔ **LA MIA RACCOMANDAZIONE: PRIMA la misura, POI `U1` per la sola `chiralita_core_locale`, POI il verso.** E motivo l'ordine:

1. ### **la misura `_chi_geom_nodi` vs `perc_geom` viene PRIMA DI TUTTO**, perche' costa poco e
   ### **puo' cancellare l'intera questione:** se e' un no-op, `U1` esce dal percorso del
   dipolo e la cura del verso si fa ### **da sola**;
2. ### **se NON e' un no-op, `U1` viene PRIMA della cura del verso**, e la ragione non e'
   prudenza: ### **la cura del verso si MISURA**, e misurarla su un sistema in cui la soglia
   sbaglia di `48×` vorrebbe dire ### **leggere i numeri di una legge nuova attraverso una
   legge rotta.** ### **Il confronto fra bracci reggerebbe, i valori assoluti no** — ed e'
   esattamente la distinzione che ho dovuto scrivere per le corse di oggi;
3. ### **e `U1` si fa PER LA SOLA `chiralita_core_locale`**, come Luca chiede: *«### **non si
   ritara con un numero: si ricava di nuovo o si toglie, LEGGE PER LEGGE**»*. ### **Una legge
   alla volta e' anche la regola d'oro del `par.3`**, e toccarne cinque in un colpo
   renderebbe ### **inattribuibile** qualunque risultato.

> ### ⚠ **E DICHIARO IL COSTO DELLA MIA RACCOMANDAZIONE:** mette ### **due lavori** davanti
> alla cura del verso, e ### **il verso e' il difetto che il referto ha confermato.** Se Luca
> preferisse curare il verso prima, ### **il risultato resterebbe leggibile come CONFRONTO** e
> ### **non come valore assoluto** — e ### **basterebbe dichiararlo.** ### **Non e' una
> scelta fra giusto e sbagliato: e' fra due ordini, e il secondo costa una dichiarazione.**

---

## ③ LE OPZIONI CONCRETE PER IL VERSO, **e il censimento di cio' che ESISTE GIA'**

### IL CENSIMENTO, col comando

| funzione | che cos'e' | per CICLO o per NODO? |
|---|---|---|
| `_base_cicli_topologici(massimo=256)` *(`:4071`)* | una base di cicli fondamentali ### **da SOLA topologia** — *«non legge `pos`, `d`, embedding o coordinate»*; ogni ciclo e' una sequenza di ### **`(indice_arco, verso)`**; la cache la invalida `_grado()` | ### **per CICLO** |
| `circolazione_topologica()` *(`:4634`)* | diagnostica ### **deliberatamente PASSIVA**: la circolazione della corrente, ### **l'OLONOMIA DI FASE** *(`Σ w4(φ_i − φ_j)` sul ciclo)* e la ### **fase di BERRY** | ### **per CICLO** |
| `olonomia_lift_ciclo(ciclo)` *(`:4310`)* | il prodotto ciclico degli overlap del lift | ### **per CICLO** |

> ### ⛔ **E QUESTO E' IL NODO DEL PROBLEMA, letteralmente:** ### **tutto cio' che ha un VERSO
> nel codice e' per CICLO**, e ### **`perc_geom` e' per NODO.** La strada `(ii)` chiede di
> portare un segno ### **da un ciclo a un nodo**, e ### **quel passaggio e' la legge nuova**,
> non un dettaglio implementativo.

### LE QUATTRO OPZIONI

| | la definizione del verso | chi la legge | cosa cambia nel dipolo | locale? | numeri a mano? | e con la legge CURATA? |
|---|---|---|---|---|---|---|
| **`A`** | ### **il SEGNO della somma di `tw` sugli archi del nodo** — `sign(Σ tw)` invece di `Σ|tw|` | frame-drag, `chiralita_core_locale`, `TORS_4PI` | il dipolo diventa ### **`±π` secondo il verso vero** | ### ✔ **SI'**, solo gli archi del nodo | ### ✔ **ZERO** | ### ⛔ **il rischio piu' alto: `Σ tw` puo' CAMBIARE SEGNO spesso**, e ogni cambio ### **inietta `±π`** |
| **`B`** | il segno della ### **circolazione di `tw` sui cicli che contengono il nodo**, dai cicli di `_base_cicli_topologici` | idem | idem | ### ⚠ **NO**: un ciclo puo' essere lungo | ### ✔ **zero**, ma c'e' ### **`massimo=256`**, che e' un numero | ### ✔ **piu' stabile**: una circolazione su un anello cambia segno ### **meno** di una somma locale |
| **`C`** | il segno dell'### **OLONOMIA DI FASE** `Σ w4(φ_i − φ_j)`, gia' calcolata | idem | idem | ### ⚠ **NO**, per ciclo | ### ✔ **zero** | ### ✔ **la piu' stabile**: e' un ### **invariante topologico**, cambia solo con un difetto |
| **`D`** | ### **si toglie il passaggio per NODO:** il dipolo si definisce ### **dall'arco**, dalla sua torsione con segno | ### **solo `TORS_4PI`** | il dipolo ### **non e' piu' `±π` ma CONTINUO** | ### ✔ **SI'**, massimamente | ### ✔ **zero** | ### ✔ **NIENTE PIU' SALTI `±π`**: la variazione diventa ### **continua** |

### ⛔ **IL CRITERIO CHE LE SEPARA NON E' LA CORRETTEZZA: E' LA STABILITA'**

> Con la legge curata il dipolo entra ### **come VARIAZIONE.** Quindi:
>
> ### **un verso GIUSTO ma che OSCILLA inietterebbe `±π` esattamente come adesso**, e
> ### **la cura non curerebbe niente.** ### **E' il punto che il mandato chiede di pesare, ed
> e' quello che ribalta la graduatoria:** `A` e' la piu' ### **locale** e la piu'
> ### **instabile**; `C` e' la ### **meno locale** e la piu' ### **stabile**; `D`
> ### **toglie il salto invece di sceglierne il verso.**

---

## ④ I CONTROLLI CHE SERVIREBBERO PER SIGILLARLA

| | che cosa pretende | perche' |
|---|---|---|
| **`S0`** | la copia di prima ### **+ la patch** e' byte-identica al blob nuovo, e i due girano con ### **tutti gli attributi di `net` identici** finche' il verso ### **non cambia niente** | il braccio `0` di sempre |
| **`S-verso`** | sui nodi dove il verso vecchio *(`sign` da `|tw|`, cioe' sempre il confronto con `2π`)* e quello nuovo ### **coincidono**, il dipolo e' ### **identico al bit** | che la cura cambi ### **solo dove deve** |
| **`S-dominio`** | il verso nuovo sta in ### **`{−1, +1}`** e ### **mai `0`**, oppure ### **il `0` e' dichiarato** e tutti i lettori lo gestiscono | il `0` e' ### **un valore NUOVO** per i lettori, ed e' il contro della strada `(i)` |
| **`S-stabilita`** | ### ⛔ **il controllo che conta:** quante volte il verso ### **cambia** per nodo e per passo, ### **prima e dopo** | ### **se il verso nuovo oscilla di piu', la cura PEGGIORA la cosa che vuole curare** |
| **`S-deve-fallire`** | su una rete costruita con ### **un vortice noto**, il verso nuovo deve dare ### **il segno giusto**, e quello vecchio ### **no** | senza questo il sigillo ### **non ha potere** |

## ⑤ LA MISURA CHE DIREBBE SE L'ACCELERAZIONE RESIDUA SPARISCE

> **Due bracci, `1000` passi, scena di sempre, ### **senza il `0.3`** *(che ora e' uscito)*,
> legge curata: ### **verso vecchio contro verso nuovo.** E le grandezze sono gia' tutte
> strumentate da `_mitosi_zero_dove` *(`c206bd4b`)*:
>
> | | la lettura |
> |---|---|
> | ### **nascite per `100` passi** | ### **stabile o in accelerazione?** Col `0.3` tolto il braccio di riferimento da' `48`-`150`: ### **se il verso nuovo scendesse ancora, l'accelerazione residua e' sua** |
> | ### **la frazione di spinta oltre `π` dal DIPOLO** | oggi `0.97`-`0.99`: ### **deve CALARE** |
> | ### **`Σ |Δdipolo|`** | ### **la grandezza piu' diretta**: se il verso e' stabile, ### **crolla** |
> | ### **`spinta_pi_esatto`** | oggi `0`: ### **se salisse, i salti `±π` sarebbero solo SPOSTATI**, non tolti |
> | gli archi oltre `4π` | il sintomo di `ARCHI-OLTRE-4PI`: ### **da riportare, non da indagare** |
>
> ### ⛔ **E IL CRITERIO VA FISSATO PRIMA DELLA CORSA, nel suo task history** — come per
> `R`, il dipolo e il dove. ### **Non lo fisso io qui: la soglia e' una decisione di Luca.**

---

## ⑥ LA RACCOMANDAZIONE, **motivata**

> ### ✔ **RACCOMANDO LA `C`** *(il verso dal segno dell'OLONOMIA DI FASE)*, con la `D` come
> ### **alternativa da considerare seriamente**, e ### **sconsiglio la `A`.**

**Il perche', in tre righe:**

1. ### **la `A` e' la piu' tentante e la piu' pericolosa:** e' locale, e' a costo zero, e
   ### **`Σ tw` cambia segno ogni volta che gli archi si bilanciano.** Con il dipolo che entra
   come variazione, ### **ogni cambio e' un `±π`** — ### **curerebbe il SEGNO e lascerebbe
   il SALTO**, che e' il difetto vero;
2. ### **la `C` e' l'unica che porta un verso GIA' TOPOLOGICO:** l'olonomia di fase e'
   ### **un invariante**, cambia ### **solo quando nasce o muore un difetto**, e
   ### **esiste gia' calcolata** in `circolazione_topologica` — ### **zero numeri nuovi, e il
   `massimo=256` e' una cache diagnostica, non una legge**, quindi ### **va alzato o tolto, e
   quello e' un numero da dichiarare;**
3. ### **la `D` e' la piu' `9-ter` di tutte** — ### **toglie una variabile invece di
   ripararla** — ma ### **cambia il dipolo da `±π` a continuo**, cioe' ### **cambia la FISICA
   piu' delle altre tre**, e ### **la sua riduzione al limite va mostrata.**

> ### ⛔ **E LA COSA CHE RACCOMANDO PIU' DI TUTTE: la misura `_chi_geom_nodi` vs `perc_geom`
> PRIMA DI SCEGLIERE.** Se `chiralita_core_locale` e' un no-op, ### **tre delle quattro
> opzioni cambiano lettore** *(non `chi_torsione` ma `perc_geom` direttamente)*, e
> ### **scegliere prima di saperlo vorrebbe dire progettare su un cammino che non e'
> percorso.**

## ⑦ LA STELLA POLARE *(`A` / `B` / `C` / `D` del documento)*

| | |
|---|---|
| **`A`** *(il sospetto da verificare)* | ### ✔ **VERIFICATO e CONFERMATO** dal referto `27c10bd`: `97`-`99 %` della spinta oltre `π` viene dal dipolo. ### **Non e' piu' un sospetto.** |
| **`B`** *(la prova dello specchio)* | ### **NON FATTA.** Resta il controllo che dice se il verso e' una ### **chiralita' vera** o un artefatto dell'orientamento del grafo |
| **`C`** *(le tre strade)* | la `(ii)` e' ### **scelta da Luca**; questa proposta ne specifica ### **quattro forme concrete**, e raccomanda la `C` |
| **`D`** *(la direzione scelta)* | ### **confermata**: `perc_geom` resta ### **si'/no**, e il verso viene dalla circolazione ### **con segno** |

> ### ⛔ **E QUI MI FERMO: la forma esatta della legge e' una decisione di Luca.**

---

# ANNOTAZIONE *(2026-10-06 — `par.8`: si ANNOTA, non si riscrive)*

## ⛔ **LE TRE OBIEZIONI DEL GUARDIANO ALLA RACCOMANDAZIONE `C`** — *e le ho verificate tutte e tre sul codice*

*(Mandato di Luca. ### **Nessuna legge nuova, nessuna patch al simulatore** (`b8c21049`).)*

> ### ⛔ **TUTTE E TRE REGGONO**, e due di esse ### **ribaltano la mia raccomandazione.** Qui
> sotto distinguo ### **cio' che ho VERIFICATO** da ### **cio' che resta da MISURARE.**

---

## `(a)` ⛔ **LA BASE DEI CICLI DIPENDE DALLA NUMERAZIONE DEI NODI** — *verificato*

**Dal codice di `_base_cicli_topologici`** *(letto, non assunto)*:

| | il codice | la conseguenza |
|---|---|---|
| le radici | `for radice in range(n)` | ### **in ordine di INDICE**, a partire da `0` |
| l'albero | DFS con una pila, sull'ordine di `adiacenza`, che segue ### **l'ordine degli ARCHI** | ### **l'albero dipende dalla NUMERAZIONE** |
| i cicli | risalgono `parent` fino al ### **LCA** | ### **possono essere lunghi quanto l'albero**, cioe' quanto la rete |
| il taglio | `if len(cicli) >= massimo: break`, con `massimo = 256` | ### **tronca**, e tiene ### **i primi `256` archi non-albero IN ORDINE DI INDICE** |

> ### ⛔ **QUINDI IL VERSO DI UN NODO DIPENDEREBBE DA UNA SCELTA GLOBALE E ARBITRARIA:** la
> radice `0`, l'ordine di visita, e ### **quali `256` cicli sono sopravvissuti al taglio.**
>
> ### ⛔ **E' CONTRO `A2`** *(una legge locale decisa da una statistica globale)* ### **e
> contro `A4`/`A5`** *(informazione da nodi lontani nello stesso istante)*.
>
> ### ⚠ **E <<non locale>> NELLA MIA TABELLA ERA TROPPO DEBOLE.** *«Non locale»* suona come
> un costo; ### **questo e' un VIZIO: due numerazioni diverse della STESSA rete darebbero
> versi diversi.** ### **Non e' una legge.**

---

## `(b)` ⛔ **<<INVARIANTE TOPOLOGICO>> NON VUOL DIRE STABILE QUI** — *verificato*

**① La cache si invalida a ogni nascita.** `_grado()` fa ### **`self._cicli_topologici =
None`** *(verificato col comando)*, e `_grado()` gira ### **a ogni mitosi e a ogni Schwinger.**

> ### ⛔ **Con `3496` divisioni e `1265` Schwinger in `1000` passi** *(`27c10bd`)*, la base
> ### **si ricostruisce da capo migliaia di volte** — e ### **ogni ricostruzione puo' dare
> cicli DIVERSI**, per il punto `(a)`. ### **Un invariante su una base che cambia non e' un
> invariante stabile: e' un invariante di un'altra base.**

**② L'olonomia e' un multiplo intero di `4π`.** ### **Verificato per algebra**, non assunto:

```
su un ciclo CHIUSO la somma di (phi_i - phi_j) TELESCOPIA a 0 ESATTO
w4(x) = x - 4pi*k(x),  k intero        ->   somma w4 = 0 - 4pi*(somma k) = 4pi*intero
```

*(`_w4(a) = (a + 2π) % 4π − 2π`, e `FASE_2PI = False` ⟹ il dominio di `φ` e' `4π`.)*

> ### ⛔ **QUINDI L'OLONOMIA E' `0` o `±4π` o `±8π`…, MAI UN VALORE INTERMEDIO.** Se e' `0`
> ### **il verso NON ESISTE**, e il `sign` darebbe ### **`0`** — cioe' ### **il valore NUOVO**
> che il `contro` della strada `(i)` dichiarava come il suo costo. ### **`S-dominio`
> fallirebbe, o il `0` andrebbe dichiarato e gestito da TUTTI i lettori.**

> ### ⚠ **E <<zero sulla maggior parte dei cicli>> E' L'UNICO PEZZO CHE NON HO VERIFICATO:**
> dipende da quanti ### **vortici di fase** ci sono, e ### **non lo so.** ### **E' una
> PREVISIONE del guardiano, e `M3` la misura** *(la frazione dei cicli della base con olonomia
> diversa da zero)*. ### **Lo scrivo come da misurare, non come fatto.**

---

## `(c)` ⛔ **`A`, `B` e `C` SONO TUTTE UN SEGNO DISCRETO: il salto di `π` resta**

> ### ⛔ **E QUESTO E' IL PUNTO CHE RIBALTA LA MIA RACCOMANDAZIONE.** Avevo scritto che il
> criterio e' ### **la stabilita'**, e poi ho raccomandato la `C` ### **perche' cambia di
> RADO** — ma ### **quando cambia, cambia di `±π` come tutte le altre.** ### **Avevo scelto
> la MENO frequente invece di quella che TOGLIE IL SALTO.**
>
> ### ✔ **SOLO `D` LO TOGLIE ALLA RADICE**, ### **ed e' anche la piu' LOCALE.**

### ⚠ **MA `D` HA DUE COSTI, e vanno scritti**

**① `D` CONTRADDICE LA STELLA POLARE.** Il punto `D` di questo documento dice:

> *«la catena della rotazione ### **legge il verso dalla CIRCOLAZIONE CON SEGNO**»*

e l'opzione `D` ### **non usa nessuna circolazione**: prende il dipolo ### **dalla torsione
con segno DELL'ARCO STESSO.** ### **E' una direzione DIVERSA da quella scelta il 2026-09-29**,
e ### **adottarla sarebbe cambiare la decisione, non attuarla.** ### **E' una decisione di
Luca.**

**② `D` CREA UN ANELLO SULLO STESSO ARCO:** `tw → dipolo → tw`.

Con il dipolo che entra ### **come variazione**, se `twist_dip = f(tw_arco)`:

```
dtw = P + f(tw + dtw) - f(tw)  ~  P + f'*dtw        ->      dtw = P / (1 - f')
```

> ### ⛔ **LA CONDIZIONE DI STABILITA' E': `sup |f'| < 1`**, e il ### **guadagno e'
> `1/(1 − f')`** — che ### **DIVERGE per `f' → 1`.**

### ✔ **LA FORMA CHE PROPONGO, e soddisfa la condizione PER COSTRUZIONE**

```
twist_dip = PI * tanh( tw / PHI_CRIT )
```

| | |
|---|---|
| ### **`f'(tw) = (π/2π)·sech²(tw/2π)`**, quindi ### **`sup|f'| = 1/2`** | ### ✔ **stabile**, col guadagno ### **`≤ 2`** |
| il codominio e' ### **`(−π, +π)`** | ### ✔ **lo STESSO intervallo del dipolo di oggi** *(`{−π, 0, +π}`)*: ### **nessun dominio nuovo** |
| le due costanti | ### **`π = twist_max`** e ### **`2π = PHI_CRIT`**, ### **gia' nel sistema** |

> ### ✔ **ZERO NUMERI NUOVI**, e ### **la riduzione al limite si vede:** per `|tw| ≫ 2π` la
> `tanh` satura a ### **`±π`**, cioe' ### **il valore di oggi**; e per `tw → 0` il dipolo va a
> `0`, ### **come oggi su un arco senza torsione.**
>
> ### ⚠ **E IL `1/2` NON E' UNA SCELTA: e' `π/(2π)`**, cioe' ### **il rapporto fra le due
> costanti che la forma usa gia'.** Se un giorno si volesse `f'` piu' piccolo, ### **si
> cambierebbe la SCALA, e quello sarebbe un numero da dichiarare.**

---

## ⛔ **DOVE MI LASCIANO QUESTE TRE OBIEZIONI**

| | prima | dopo |
|---|---|---|
| `A` | sconsigliata | ### **sconsigliata** *(invariata)* |
| `B` | non raccomandata | ### **peggiora**: eredita `(a)` e `(b)` dalla base dei cicli |
| `C` | ### **RACCOMANDATA** | ### ⛔ **NON PIU':** `(a)` la rende ### **non una legge** *(dipende dalla numerazione)*, `(b)` le toglie ### **sia la stabilita' sia il dominio** |
| `D` | *«alternativa da considerare seriamente»* | ### ✔ **l'unica che TOGLIE IL SALTO**, con ### **due costi DICHIARATI** |

> ### ⛔ **E NON RACCOMANDO `D` AL POSTO DI `C`: dichiaro che la mia raccomandazione e'
> CADUTA e che `D` ha un costo che NON posso decidere io** — ### **contraddice una direzione
> che Luca ha gia' scelto.**
>
> ### ✔ **Quello che posso fare e' DARE I NUMERI**, ed e' `M3`: quante volte per passo
> cambiano ### **il segno di `A`**, ### **l'olonomia di `C`**, ### **il segno di `tw` per
> `D`**, e ### **`perc_geom` di oggi** come riferimento. ### **La scelta e' di Luca.**
