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
