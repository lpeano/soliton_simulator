# INDICE `v3`: **l'ultima pulizia** — i `15` segnali che restano, e un presidio nuovo

> **Mandato di Luca del 2026-10-09**, sei punti, **un commit per punto**. Nessuna corsa,
> simulatore `b8c21049` intatto.
>
> ### ⚠ **Si committa e si pusha PRIMA del lavoro** *(par.8)*.

---

## ① RAGIONAMENTO PRELIMINARE — *cosa credo PRIMA di guardare, e cosa NON so*

### ⭐ **LA PRIMA COSA L'HO MISURATA PRIMA DI SCRIVERE QUESTO FILE, e conta**

`F7` e' un ### **ERRORE**, non un segnale: fa ### **fallire la validazione**, quindi il
`pre-commit`. ### ⛔ **Un presidio bloccante che violasse una voce che il mandato non nomina
fermerebbe ogni commit**, e me ne accorgerei ### **solo al momento di committare.** Quindi
l'ho misurato subito:

| `FISICA` / era `1` | quante |
|---|--:|
| `SOSPESA` | `204` |
| `CHIUSA` | `137` |
| ### **`APERTA`** | ### **`4`** |

### ✔ **Le `4` sono ESATTAMENTE `CURA1-CORTO`, `CURA2-CORTO`, `SIGILLO-CURA2`,
`SIGILLO-CURA2-RIPARATO`** — cioe' ### **esattamente quelle che il punto `1` corregge.**
### **`F7` e' sicuro**, e lo e' ### **perche' il punto `1` viene prima**, non per caso.

### ⚠ **E sono le quattro che ho ripristinato IO nel giro scorso**, con uno stato che avevo
letto dall'intestazione *(`## APERTO CURA1-CORTO`)*. ### **Avevo scritto nel referto che
«classe e dominio sono MIEI» e che lo stato «non l'ho scelto: lo dice l'intestazione».**
### ⛔ **Era vero e insufficiente:** l'intestazione dice lo stato ### **nell'era `1`**, e io
l'ho messo nel campo ### **`stato`**, che e' lo stato ### **di oggi.** Il posto giusto era
`stato_era_1`, e ### **il mandato me lo dice.**

### **CHE COSA CREDO, E PUO' RIVELARSI FALSO**

**`a` Il punto `4` mi obbliga a decidere cio' che nel giro scorso ho messo nel «quarto caso».**
`AUTO-MANUTENZIONE`, `F4`, `F5`: il mandato dice *«chiudi con la regola del punto `5` del giro
scorso, ### **voce per voce**»* — cioe' ### **i tre esiti, e basta.** ### **La mia uscita «non
e' nessuno dei tre» non e' piu' disponibile**, e va bene: era una domanda, e la risposta e'
*«decidi»*.
### ✔ **E credo che la via sia l'EREDITA':** `F4` e `F5` sono ### **famiglie di difetti**, e
il testo dice ### **da quale difetto nascono** — `F4` da `D04`, `F5` da `D34`. ### **Una
famiglia prende il dominio del difetto da cui nasce**, e l'ho misurato: `D04` e `D34` sono
### **`FISICA`, era `1`.**

**`b` Gli `11` segnali di `F1` si chiudono tutti con un'eccezione, tranne i due omonimi.** Il
mandato da' la frase da citare per ciascun gruppo: ### **il criterio che VERIFICA** il difetto,
### **il documento che CITA** la regola, ### **la dipendenza.** Credo che le eccezioni siano
`8` *(una per VOCE, non una per segnale: `COER-4PI` e `REGISTRO_FISICA:E3` hanno due segnali
ciascuna)* piu' `2` `meta.omonimo`.

**`c` L'elenco del punto `5` sara' lungo.** `187` voci sono `NON_DEFINITA`, e ### **quelle NON
ci vanno**: il mandato dice *«le voci `DA_CLASSIFICARE` che ### **non sono segnaposto**»*.
Previsione: ### **fra `25` e `45` righe** — gli omonimi *(`D3`-`D6`, `H2`, `S1`, `S3`, `T1`,
`C5`, piu' `M1` e `C4` da questo giro)*, i `20` assiomi *«da confermare»*, le `5` `M-*`, le `3`
del quarto caso, `ENERGIA-NON-DEFINITA`, `B7`/`I1`.

### ⛔ **CHE COSA NON SO, E NON INVENTO**

1. **Se `F7` lasci passare qualcosa che dovrebbe prendere.** `F7` guarda `FISICA`+era `1`;
   ### **non guarda `FISICA`+era `2`, ne' gli altri domini.** Non so se la regola valga anche
   la': ### **il mandato dice `FISICA`/era `1`, e non la allargo da solo.**
2. **Che classe dare ad `AUTO-MANUTENZIONE`.** E' ### **una regola di lavoro** in
   `doc/STORIA_REGOLE.md`. `STANDARD`/`METODO` e' la mia lettura, e ### **va nel referto come
   tale.**
3. **Se le voci `DA_CLASSIFICARE` non-segnaposto siano `2` o piu'.** Ricordo `B7` e `I1` col
   `motivo_dubbio`, ma `B7` l'ho mosso nel blocco `B`: ### **lo conto, non me lo ricordo.**

---

## ② PROGETTAZIONE DEL RAGIONAMENTO — *i passi, cosa decide ciascuno, cosa mi FERMA*

### **L'ORDINE NON E' LIBERO, e questa e' la cosa da scrivere prima**

> ### ⛔ **Il punto `1` DEVE precedere il punto `2`.** `F7` fa ### **fallire la validazione**,
> e la validazione gira ### **dentro `aggiorna-lotto`**: se scrivessi `F7` prima di correggere
> le `4` voci, ### **il lotto del punto `1` non potrebbe piu' essere applicato.**
> ### **Un presidio bloccante si accende DOPO che cio' che blocca e' stato curato**, e il
> mandato li mette in quest'ordine ### **per questo.**

### **I PASSI**

| | il passo | che cosa DECIDE |
|---|---|---|
| `1` | le `4` voci da `APERTA` a `SOSPESA`, e `stato_era_1 = aperto` | ### **la regola in vigore:** la fisica dell'era `1` non chiusa e' `SOSPESA` |
| `2` | `F7`, ### **un ERRORE** in `valida` | d'ora in poi il `pre-commit` ### **impedisce** quella mescolanza |
| `3` | gli `11` di `F1`: `2` omonimi *(`M1`, `C4`)* + `8` eccezioni che ### **citano la frase** | `F1` ### **a zero** |
| `4` | i `3` di `F4`, con la regola dei ### **tre esiti** | `F4` ### **a zero**, e il «quarto caso» ### **si chiude** |
| `5` | `doc/indice/DA_DECIDERE_LUCA.md`, ### **generato** da `indice.py` | ### **un elenco solo**, e non scritto a mano |
| `6` | controlli + referto `doc/REFERTO_indice_v3_pulizia.md` | — |

### **LE LETTURE SI FISSANO QUI, PRIMA DI VEDERE I NUMERI**

| | la lettura |
|---|---|
| dopo il punto `1` | ### **`0`** voci `FISICA`/era `1` con stato diverso da `SOSPESA`/`CHIUSA`. Se non e' `0`, `F7` ### **non si accende** |
| il collaudo di `F7` | ### **DEVE scattare** su `CURA1-CORTO` allo stato di `89784dc` *(in una COPIA)*, ### **NON deve** dopo il punto `1`. Meno di `2` su `2` ⇒ **FERMO** |
| i segnali finali | ### **`F1=0 F2=1 F3=0 F4=0 F6=0`**, e il mandato li scrive. ### **Qualunque altro numero e' un difetto mio, non un dato** |
| il collaudo intero | ### **almeno `22` su `22`** *(i `20` di oggi piu' i `2` di `F7`)* |
| l'elenco del punto `5` | fra `25` e `45` righe |

### ⛔ **CHE COSA MI FA FERMARE**

1. **`F7` scatta su una voce che il punto `1` non nomina** ⇒ la regola copre piu' di quello
   che il mandato dice ⇒ ### **FERMO e lo scrivo**, invece di spostare quella voce.
2. **`F1` o `F4` non arrivano a zero** ⇒ ho letto male un segnale, oppure un'eccezione
   ### **non copre** cio' che credevo ⇒ **FERMO**.
3. **Un'eccezione non passa il controllo della forma** *(il pezzo letterale di `20`
   caratteri)* ⇒ ### **la frase che ho scelto non e' nel testo** ⇒ rileggo, non allargo il
   controllo.
4. **L'elenco del punto `5` risulta scritto a mano** — cioe' se per farlo dovessi
   ### **aggiungere a mano** una riga che il codice non trova ⇒ **FERMO**: il mandato dice
   ### **«generato da `indice.py` e non scritto a mano»**, e un elenco mezzo generato
   ### **e' peggio di nessun elenco**, perche' sembra completo.

### **`L-STELLA`: le cinque domande di `doc/STELLA_POLARE.md`**

### ⛔ **NON SI APPLICA, e il perche' e' parte della risposta:** nessuna legge cambia, il
simulatore non si tocca *(`b8c21049`)*, niente gira. Si cambia ### **lo stato di `4` voci**,
si accende ### **un presidio sul validatore**, si chiudono ### **`14` segnali** e si
### **genera un elenco.** ### **Le cinque domande chiedono di un gradino di robustezza fisica,
di numeri o leggi aggiunti, del verso EM-curvatura e di emergente-contro-imposto: su un
cambiamento che non entra nel simulatore NON HANNO UN SOGGETTO.**

---

## ③ TODO DEL NEXT STEP — *operativo*

- [ ] **`1`** le `4` a `SOSPESA`, `stato_era_1 = aperto`. ### **PRIMA di `F7`.**
- [ ] **`2`** `F7` in `valida` *(ERRORE)*, piu' i `2` bracci di collaudo sulla COPIA a
      `89784dc`.
- [ ] **`3`** `M1` e `C4` → `meta.omonimo`; `8` eccezioni che ### **citano la frase**, col
      marcatore ### **estratto dal testo vivo** come nel punto `3` del giro scorso.
- [ ] **`4`** `AUTO-MANUTENZIONE`, `F4`, `F5` con la regola dei tre esiti. ### **`F4` e `F5`
      ereditano il dominio dal difetto da cui NASCONO** *(`D04`, `D34`: `FISICA`/era `1`)*.
- [ ] **`5`** `indice.py da-decidere` → `doc/indice/DA_DECIDERE_LUCA.md`: `id`, ### **la
      domanda**, ### **la frase.**
- [ ] **`6`** controlli + `doc/REFERTO_indice_v3_pulizia.md`.
- [ ] **par.6** a ogni commit: **inventario** e **par9** *(la regola dello stato, `F7`, il
      comando nuovo)*. ### **FISICA: non si applica.**
- [ ] **`storico-commit`** dopo ogni commit.
