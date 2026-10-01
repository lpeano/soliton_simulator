# **PIANO: `DIVISIONE-AUTOCONSISTENTE` E IL CALORE LOCALE**

*(Mandato del guardiano del 2026-10-01, su priorita' di Luca: «qua si gioca veramente la dinamica
pulita di tutto». **Nessuna riga di codice del simulatore in questo giro.**)*

> ### 📌 **LA FORMA BREVE `:Mn`, DICHIARATA UNA VOLTA: in questo documento `:M0` ... `:M7` stanno
> ### per `DIVISIONE-AUTOCONSISTENTE:M0` ... `:M7`.**
> ### ⚠ **E il namespace NON e' cosmetico:** nell'indice ### **`M1`, `M2`, `M3`, `M4` esistono
> gia' come id**, e `M2` e' *«LA MITOSI — il figlio nasce nel PUNTO MEDIO»*, cioe' ### **lo stesso
> argomento**: ### **la forma NUDA risolverebbe al difetto sbagliato.** E' la famiglia della
> collisione `P3`/`P5` curata dal prefisso `H-`. *(L'ha trovata `H-INDICE`, rifiutando un commit.)*

> ### ⚠ **PERCHE' UN FILE NUOVO E NON UNA SEZIONE DI `doc/PIANO_riordino_mitosi.md`**
> Quel piano e' il piano di un **RIORDINO**: ogni suo commit e' **byte-inerte o byte-identico**, e
> la sua forza sta tutta li' — ### **«il valore non cambia di un bit, cambia DOVE VIVE».**
> Questo e' **FISICA NUOVA**: due bilanci, una grandezza di stato in piu', una legge che sostituisce
> un termostato. ### **Mescolarli cancellerebbe la distinzione su cui poggia tutto il riordino**, e
> il primo che legge non saprebbe piu' quale commit puo' cambiare un numero e quale no.
> *(E il riordino e' gia' a 523 righe: il criterio non e' la lunghezza, ma la lunghezza conferma.)*

---

## 0. LO STATO DI PARTENZA, **misurato** *(non supposto)*

| misura | esito | dove sta il referto |
|---|---|---|
| **`DIVISIONE-AUTOCONSISTENTE:M0`** | ### **NON esiste un'energia totale**, e un'energia di **stato** non puo' esistere | `csv/_test_fork/_misure_calore/` |
| **`:M2`** | ### **il verso dell'arco ENTRA NELLA FISICA**, e il luogo e' `memoria_hebbiana_moto` | `csv/_test_fork/_verso_archi/` |
| **`:M5`** | ### **`pos` e' FISICA**, non disegno: **5 leggi** la leggono | `csv/_test_fork/_pos_contro_d/` |
| ### **`:M1`** | ### **ogni divisione distrugge `1.17` AVVOLGIMENTI** *(mediano; min `0.60`, max `1.33`)*, ma in relativo sulla rete solo `5.36e-05` | `csv/_test_fork/_misure_calore/` |
| ### **`:M3`** | il termostato ### **RIFORNISCE in 56 passi su 72**; il clip `±2` ### **non scatta mai**; `T_target` salirebbe del ### **+1.68 %** con la mediana di tutti gli archi | idem |
| ### **`:M4`** | ### **il calcio NON FA LAVORO**: `0` genitori con `phivel` mosso, cinetica di fase sui preesistenti ### **esattamente zero** | idem |
| ### **`:M6`** | il vuoto immette ### **52 volte** cio' che immette `step`, ed e' ### **positivo in 72 passi su 72**; torsione immessa ### **ZERO ESATTO** | idem |

---

# **(A) IL REGIME: la decisione di Luca, e la cura PROPOSTA**

## ✅ **IL SISTEMA DI RIFERIMENTO, dichiarato una volta per tutte** *(decisione di Luca)*

> ### **`REGIME` deterministico DAL MODULO · `SCUOTIMENTO = True` · SENZA `--regime`.**
> **E' quello che girano TUTTI i sigilli**, e da qui in avanti *«il sistema»* significa questo.

## ⛔ **IL DIFETTO: `--regime` crea un SECONDO sistema con lo STESSO nome** *(`REGIME-DUE-SISTEMI`)*

| dove | che cosa fa |
|---|---|
| il **ramo di modulo** *(sempre eseguito)* | `_SCUOTIMENTO_REGIME = True` ### **in ENTRAMBI i rami** |
| `_applica_regime` *(solo con `--regime`)* | ### **`SCUOTIMENTO = False`** per il deterministico |

### ➜ **E il vuoto acceso o spento non e' un dettaglio: e' il TERMOSTATO e la SORGENTE DI
ASIMMETRIA.** Due run che si chiamano **entrambi** *«regime deterministico»* ### **non sono lo
stesso sistema**, e un confronto fra misure prese nei due modi ### **non e' a variabile singola.**

## 🔧 **LE DUE VIE, e dico quale preferisco e perche'**

| | la via | il prezzo |
|---|---|---|
| **①** | **allineare `_applica_regime` al modulo** *(`SCUOTIMENTO = True` anche col flag)* | ### ⛔ **DISTRUGGE la misura `O2`**, che e' un A/B a variabile singola costruito **PROPRIO** su quella differenza: `--regime deterministico` cambia **solo** `SCUOTIMENTO`. Togliere la differenza ### **toglie lo strumento** |
| ### **②** | ### **RINOMINARE CIO' CHE PRODUCE**: `--regime` non tocca piu' `SCUOTIMENTO`, e il sistema col vuoto spento si chiede con un flag **suo** *(per esempio `--senza-scuotimento`)* | va cambiato **chi chiama** `O2`, e i suoi referti vanno **marcati** |

### ✅ **PREFERISCO LA ②**, e la ragione e' una sola: ### **non distrugge una misura esistente e
chiama le cose col loro nome.** Un sistema diverso **deve avere un nome diverso** — ed e' la stessa
regola che ha chiuso `A3` *(era tre voci)* e `P3`/`P5`.

## 📋 **I REFERTI PRODOTTI SUL SISTEMA «ALTRO»: si MARCANO, NON si riscrivono** *(decisione di Luca, par.9)*

| referto | perche' e' sul sistema «altro» |
|---|---|
| `csv/_test_fork/_sigillo_osservatore.py` *(braccio `O2`)* | passa ### **`--regime deterministico`**, quindi gira con `SCUOTIMENTO = False` |
| `csv/_test_fork/_osserva_vuoto.py` *(flag `--regime-det`)* | **idem**: il braccio OFF e' il sistema col vuoto **spento** |

### ⚠ **E LA MARCATURA NON E' UNA NOTA A PIEDE DI PAGINA:** va **nel referto**, perche' chi lo
legge fra tre giorni ### **non ha questa pagina.** La forma: una riga in testa che dice ### **«questo
referto e' del sistema CON `--regime`, cioe' `SCUOTIMENTO = False`: NON e' il sistema di
riferimento»**.

## 🧪 **LA MISURA CHE SERVE PRIMA DI SCEGLIERE** *(e che il mandato chiede)*

> ### **Di quanto differiscono i due sistemi su 72 passi?**

**Strumento:** `csv/_test_fork/_regime_due_sistemi.py` *(da scrivere e committare prima di girare)*.
**Come:** due reti identiche dalla **stessa** scena di riferimento, una **senza** `--regime` e una
**con** `--regime deterministico`, ### **confronto PASSO PER PASSO** sulle grandezze di stato e
sui contatori — lo stesso schema del braccio `B` del sigillo del controllo unico.
### ✅ **LA MISURA E' FATTA, E LA VIA ① E' ESCLUSA** *(72 passi, scena grande, seme 11)*

| | `A` = riferimento | `B` = con `--regime` |
|---|---|---|
| si separano | ### **al passo 1**, su **16** grandezze e **15** contatori | |
| ### **nodi / archi al 72** | **12812** / **471575** | ### **12802 / 471564: NESSUNA NASCITA** |
| ### **`_nb`** *(Bloch)* | `1.905e+04` | ### **`1.2802e+04` = `n` ESATTO** -> spin ### **mai inclinati** |
| ### **`eta`** | `8.748e-01` | ### **`0.000000e+00`** |
| `d` / `d0` | | relativo `2.80e-03` / `4.35e-03` |

### ➜ **Non e' una deriva: sono DUE FISICHE.** ### **Il confine fra un sistema che genera materia e
uno che non la genera.** Quindi la via ① ### **cancellerebbe un sistema che qualcuno ha misurato**,
e resta la ② — ### **come avevo scritto PRIMA di vedere il numero.**

### ⭐ **E LA MISURA HA DATO UN FATTO IN REGALO: `SCUOT-INNESCO`**
### **Lo scuotimento del vuoto e' L'INNESCO.** `_nb` somma `= n` esatto vuol dire ### **ogni Bloch
e' lo stesso versore**: ### **la simmetria non si rompe mai.** Con `:M6` *(il vuoto immette **52
volte** cio' che immette `step`, positivo in **72 passi su 72**)* il quadro si chiude: ### **il
vuoto non e' un disturbo da tollerare, e' il MOTORE.**
### ⚠ **E questo pesa sulla decisione 4:** se il vuoto e' l'innesco, ### **il calore locale non
puo' SOSTITUIRLO** — al massimo puo' **riceverne** l'energia e condurla.

## 🗄 **E DUE COSE NELLO STESSO GIRO DELLA CURA**

1. ### **La stringa di help di `--tau-a`** — dice *«il `2.0` e' il valore 'canonico', ma il canonico
   vuole anche `G_PH = 0.15`»*, e usa **«canonico»** nel senso del regime. Il **commit 0-bis** non
   l'ha toccata perche' e' un ### **LITERAL e avrebbe rotto la byte-inerzia**: va qui.
2. ### **Il ramo STOCASTICO si ARCHIVIA come `MITOSI_DIR`** *(decisione di Luca)*, in un **commit a
   se', piu' avanti**: nessuno lo gira, **nessun sigillo lo copre**, e `RAMI-OFF-CURA2` dice come —
   ### **archiviato COPIATO dal sorgente, non cancellato.**

---

# **(A-bis) LA VISIONE DI LUCA, e che cosa cambia in questo piano** *(2026-10-01)*

*(Registrata in `doc/REGISTRO_FISICA.md` con la data. Qui sta solo **cio' che cambia nel piano**.)*

| | |
|---|---|
| **(a)** | la nascita ha ### **TRE esiti**: **spazio** · **materia** · **materia e antimateria**; ### **`peq` e' il riferimento che li separa** |
| **(b)** | ### **si conserva ESATTAMENTE solo la CARICA** |
| **(c)** | ### **l'energia GLOBALE non si conserva** *(uno spaziotempo in espansione non la conserva)*; resta il ### **bilancio LOCALE** |

## ⛔ **LA (c) SCIOGLIE IL RISCHIO CHE AVEVO DICHIARATO IRRISOLTO**

Avevo scritto, come **il rischio vero** della temperatura per nodo: *«senza un «fuori» il sistema
puo' SOLO PERDERE»*.
### ➜ **Se l'energia globale non DEVE conservarsi, quello non e' un difetto da evitare: e' una
POSSIBILITA' LEGITTIMA.** Cio' che resta da chiedere e' ### **il bilancio LOCALE: ogni variazione
ha una causa dichiarata.** ### **Era il mio ostacolo piu' grosso, e non era un ostacolo: era una
mia assunzione.**

## ⛔ **E RIBALTA LA MIA LETTURA DI `:M1`, non la raffina**

Avevo scritto che `:M1` mostrava ### **«una carica che svanisce, evento per evento»**.
### **`tw` NON E' LA CARICA.** La misura resta — `1.17` avvolgimenti per arco diviso — ### **ma non
e' una violazione: e' un PREZZO NON SCRITTO.**

---

# **(B) I DUE BILANCI, e NON sono simmetrici**

> ### **La CARICA si conserva esattamente. L'AVVOLGIMENTO no, e non deve. L'ENERGIA nemmeno,
> ### globalmente — ma OGNI VARIAZIONE HA UNA CAUSA DICHIARATA.**

| | ### **la CARICA** | ### **l'AVVOLGIMENTO `tw`** | ### **l'ENERGIA** |
|---|---|---|---|
| **si conserva?** | ### **SI', ESATTAMENTE** *(l'unica conservazione stretta del modello)* | ### **NO, e non deve** | ### **NO globalmente**; ### **SI' localmente**, come bilancio con causa |
| **la forma** | `N(+1) − N(−1)` **invariante**, e la materia carica nasce ### **solo a coppie** *(criterio 8)* | ### **«LA TORSIONE PAGA LO SPAZIO»**: una **conversione** col suo **tasso scritto** | prima = figli + calcio + calore, ### **piu' i flussi dichiarati** |
| ### **com'e' OGGI** | ### **NON si conserva** *(`:G4`)* e ### **non e' nemmeno persistente** *(`:G1`)* | ### **sparisce senza legge**: `1.17` avvolgimenti per arco diviso *(`:M1`)* | il calcio ### **non fa lavoro** *(`:M4`)*, e un addendo ### **non e' definibile** *(`:M0`)* |

## ⭐ **DECISIONE 1 DI LUCA, nella sua forma definitiva: «LA TORSIONE PAGA LO SPAZIO»**

| | |
|---|---|
| **che cosa NON e'** | ### **non e' una carica che svanisce** — era la mia lettura, ed era sbagliata |
| **che cosa e'** | ### **una CONVERSIONE** avvolgimento -> spazio, e una conversione ### **si scrive col suo tasso** |
| ### **cosa la rende legge** | ### **il bilancio DEVE essere scritto**: quanto `tw` per quanto spazio. ### **Senza il tasso non e' una legge, e' ancora una perdita** |
| **il dato di partenza** | `1.17` avvolgimenti per arco diviso *(min `0.60`, max `1.33`)* — ### **il DATO, non il tasso** |

| | ### **BILANCIO DELL'AVVOLGIMENTO** | ### **BILANCIO DELL'ENERGIA** |
|---|---|---|
| **la grandezza** | `tw`, contato su `±4π` | le quattro forme di `M0` |
| **la forma** | ### **prima = figli + quanto si scioglie in rotazione**, ### **e ogni perdita DICHIARATA** | ### **prima = figli + calcio + calore** |
| **conservata?** | ### **LO DECIDE LUCA** *(decisione 1)* | ### **NO, e non puo' esserlo**: il sistema ha sorgenti e pozzi espliciti |
| **la sorgente, MISURATA** | ### **`step`: `+1.27e+06`** *(e `:M6` misura che lo scuotimento immette ### **ZERO ESATTO** avvolgimento)* | ### **lo scuotimento: `+8.25e+04`**, cioe' ### **52 volte** il netto di `step` *(`+1.58e+03`)*; piu' il **termostato** quando `xi < 0` |
| **il pozzo, MISURATO** | ### **la divisione: `−6.79e+01` su 72 passi**, cioe' ### **`1.17` avvolgimenti per arco diviso** | l'attrito `beta·vd`, e il freno di `chiudi` su `Q2`: `−4.93e+04` |

## ⛔ **E IL CALCIO NON FA LAVORO: il BILANCIO ENERGETICO DEL CALCIO NON SI PUO' NEMMENO PORRE**

`:M4` misura, **attorno alla voce** e **sui soli nodi preesistenti**: ### **`0` genitori con
`phivel` mosso**, e la cinetica di fase dei preesistenti varia di ### **`+0.000000e+00` esatto.**
### ➜ **Il calcio sposta SOLO le fasi**, quindi agisce sul **termine di interferenza** — ed e'
### **esattamente il pezzo che `:M0` dice NON ESSERE una funzione di stato** *(connessione dal
Bloch ritardato)*.
### ⚠ **Quindi la riga «prima = figli + calcio + calore» ha un addendo che OGGI NON E' DEFINIBILE.**
Non e' un dettaglio del piano: ### **e' il primo ostacolo da togliere**, e si toglie **solo**
decidendo che cosa sia l'energia *(la proposta di `:M0`)*. ### **Scriverla prima sarebbe scrivere
un'equazione con un simbolo che non esiste.**

### ⚠ **E IL FATTO CHE LE DUE SORGENTI SIANO DIVERSE E' MISURATO, non assunto**
`scuoti_vuoto` scrive ### **solo `net.phivel`**: immette **energia** e ### **non immette
avvolgimento.** ### ➜ **Quindi i due bilanci non si possono fondere in uno**, e un'unica *«legge di
conservazione»* sarebbe **falsa su entrambi i lati.**

---

# **(B-bis) GLI SCOSTAMENTI FRA LA VISIONE E IL CODICE, punto per punto e con la misura**

*(Ognuno ha la sua misura. ### **Nessuno e' una mia impressione.**)*

| la visione dice | il codice fa | la misura |
|---|---|---|
| **(a)** `peq` separa i tre esiti | ### **`peq` NON entra** nella creazione di coppie: `COPPIA_DENSITA = False` *(esplorativo)* | ### **`:G3`** |
| **(a)** esiste l'esito *«materia e antimateria»* | ### **per il campo l'antinodo E' il genitore**: `anti = phi + 2π` su un dominio di `4π`, e il campo legge `exp(i·phi)` -> `|Δ| = 2.13e-15` | ### **`:G2`** *(`D35`)* |
| **(b)** la carica si conserva **esattamente** | ### **NON si conserva alle nascite**: eventi neutri ### **0/8**, **3/10**, **0/83**; e nel run lungo `d_somma` ### **sempre POSITIVA** | ### **`:G4`** |
| **(b)** la carica e' **una grandezza** | ### **e' una CONVENZIONE**: il segno dipende dal rappresentante canonico, e cambiare gauge ribalta ### **il 100 % delle cariche** *(12812/12812, 12782/12782, 14000/14000)* | ### **`:G1`** |
| **(b)** materia **contro** antimateria | ### **l'antimateria si forma TARDI e resta una minoranza**: nodi `−1` da **0** al passo 1 a ### **467 su 14000** al passo 150 *(3.34 %)* | ### **`:G1`**, run lungo |
| la materia carica nasce **a coppie** *(criterio 8)* | ### **lo Schwinger crea UN SOLO nodo**, accanto a un genitore che c'era gia' | ### **`:G4`** |
| la neutralita' di una coppia | ### **e' un CASO, non una legge**: sul seme 12 i `d_n = +2` danno `d_somma = 0` in **3** casi e `+2` in **2**, secondo le cariche dei **genitori** | ### **`:G4`** |

### ⚠ **E DUE SCOSTAMENTI SI CURANO INSIEME O LA CURA NON SI VEDE**
### **`SCHWINGER-UN-NODO` e `CARICA-DI-GAUGE`:** anche facendo nascere le coppie **neutre per
costruzione**, ### **la carica resterebbe riscritta ogni passo da un segno di gauge** — quindi la
conservazione sarebbe ### **invisibile un passo dopo.**

---

# **(B-ter) `D36` E' PROMOSSA: e' il PREREQUISITO DELL'ANTIMATERIA** *(decisione del guardiano)*

> ### **La catena: soglia adimensionale (`D36`) -> fase su `2π` (`FASE_2PI`) -> antiparticella
> ### VERA (`D35`).**

| | |
|---|---|
| perche' e' una **catena** | con `phi` su `4π` l'antifase `+2π` ### **non e' un'antifase** *(`:G2`, misurato)*. Per averne una vera serve ### **`FASE_2PI`**, cioe' `phi` su `2π` — e `FASE_2PI` ### **dipende da `D36`**, la soglia **adimensionale** |
| ### **che cosa cambia nel piano** | ### **`D36` non e' piu' «in coda»: e' un PREREQUISITO.** Senza di lei l'esito *«materia e antimateria»* della visione (a) ### **non e' rappresentabile**, e il criterio 8 ### **non si puo' nemmeno provare** |
| **l'ordine che ne segue** | `D36` ### **prima** di qualunque legge sull'antimateria; il criterio 8 ### **dopo** |

---

# **(C) IL CALORE LOCALE: la proposta**

## ⛔ **PERCHE' IL NOSE-HOOVER NON PUO' RESTARE COM'E'**

| | |
|---|---|
| ### **e' un BAGNO GLOBALE** | `E_cin` e' una ### **MEDIA su tutta la rete**, `P_eq` una ### **MEDIANA**, `xi_termo` ### **UN SOLO numero per tutto il sistema**. ### **E' `A2`: una statistica globale dentro una legge locale** |
| ### **non sa DA DOVE viene l'energia** | frena o rifornisce ### **tutti i nodi allo stesso modo**, qualunque sia il luogo in cui l'energia e' nata o si e' persa |
| ### **e il suo bersaglio dipende da una FETTA ARBITRARIA** | `P_eq = median(d0[:n])`: i **primi `n` archi su `m`** *(12802 su 471575)*, ordinati **per creazione**. E' `P-EQ-MEDIANA-ARCHI`, e ### **`:M3` lo misura: con la mediana di TUTTI gli archi `T_target` salirebbe del `+1.68 %`** *(mediano; min `+0.87 %`, max `+2.24 %`)* ### **su tutto il sistema** — e il rapporto di `T_target` ### **E' ESATTAMENTE quello di `P_eq`**, perche' `cs_rappr` non cambia: ### **non e' una stima, e' un'identita'** |
| ### **e un suo LIMITE non scatta MAI** | il **clip `±2`** di `xi_termo`: ### **0 volte su 72 passi.** E' `A9` — ### **un limite che non limita** — e `A11` chiede di cercare **l'errore** da cui proteggeva |

### ⚠ **MA IL TERMOSTATO C'E' PER UNA RAGIONE, e va detta prima di proporre di toglierlo**
### **Senza di lui il sistema si SPEGNE o ESPLODE.** `xi < 0` ### **RIFORNISCE**: e' il meccanismo
per cui il regime e' ### **AUTOSOSTENUTO** — e ### **`:M3` misura che e' il caso NORMALE: 56 passi
su 72 rifornisce**, 16 frena. ### ➜ **Qualunque sostituzione deve dimostrare di tenere il sistema
vivo**, e il criterio sta nel par. **(E)**.

> ### ⚠ **E UNA MISURA CHE MANCA, e la dichiaro invece di aggirarla**
> ### **Non so QUANTA energia il termostato rifornisce in assoluto.** `:M6` dice che lo scuotimento
> immette `+8.25e+04` e che il **netto** della voce `step` e' `+1.58e+03` — ### **ma dentro `step`
> ci sono INSIEME la coppia, l'attrito `beta`, e il termostato**, e il netto non li separa.
> ### ➜ **Finche' quel termine non e' misurato DA SOLO, la decisione 4 non ha il suo numero**: si
> puo' dire che il vuoto immette **52 volte** il netto di `step`, ### **non che il vuoto COPRE il
> termostato.** La misura e' ### **`:M7`, da fare**: la potenza del solo termine `−xi·phivel`.

## ➜ **LA PROPOSTA: UNA TEMPERATURA PER NODO**

> ### **`T_nodo`: una grandezza di STATO, nel REGISTRO, per nodo.**

| | la regola |
|---|---|
| ### **nasce dove si DISSIPA** | la **divisione** *(l'energia che la rottura non consegna ai figli ne' al calcio)* e l'**attrito** *(`beta·vd`, `xi·phivel`)* |
| ### **si CONDUCE lungo gli archi** | e **solo** lungo gli archi: nessun salto, nessuna media globale |
| ### **agita la FASE localmente** | dove `T_nodo` e' alta la fase e' piu' agitata — ### **al posto del bagno globale** |
| ### **il totale globale e' la SOMMA delle locali** | ### **nessuna variabile globale, nessun «fuori»**, e il bilancio e' ### **CHIUSO PER COSTRUZIONE** |
| ### **la REGOLA DI NASCITA** *(serve al registro del commit 1)* | ### **media dei genitori + il calore liberato dalla divisione** |

### ✅ **CHE COSA SOSTITUISCE DEL NOSE-HOOVER, punto per punto**

| il Nose-Hoover fa | `T_nodo` fa |
|---|---|
| `E_cin` = media globale di `phivel²` | ### **`T_nodo` E' GIA' la misura locale**: non serve una media |
| `T_target = cs²·P_eq`, con `P_eq` da una **fetta arbitraria** | ### **il bersaglio diventa LOCALE** e la fetta **sparisce** — e con lei `P-EQ-MEDIANA-ARCHI` |
| `xi_termo` unico, `clip(±2)` | ### **nessun numero scelto**: l'agitazione e' il **contenuto** di `T_nodo`, non un attrito tarato |
| rifornisce **da fuori** | ### **non c'e' un fuori**: cio' che agita la fase e' stato ### **dissipato prima da qualcosa** |

### ⚠ **E QUI STA IL RISCHIO VERO, e lo dico adesso invece di scoprirlo dopo**
### **Se non c'e' un «fuori», il sistema puo' SOLO PERDERE.** Il Nose-Hoover **rifornisce** perche'
pesca da un serbatoio che non esiste in natura; `T_nodo` ### **non puo' farlo**, e ### `:M3`
**misura che oggi il termostato RIFORNISCE** *(`xi < 0`)*.
### ➜ **Quindi la proposta e' incompleta finche' non si dice DA DOVE viene l'energia che oggi
arriva dal serbatoio.** ### **La risposta candidata e' lo SCUOTIMENTO** *(`:M6` misura che immette,
ed e' **locale**)*, e ### **questa e' la decisione 4.**

## 🔗 **COME SI RAPPORTA ALLO SCUOTIMENTO** *(`:M6`)*

Lo scuotimento e' ### **gia' un'agitazione LOCALE**: ampiezza **per nodo**, dallo **stress locale**
modulato dalla **coerenza locale**. ### ➜ **Quindi non e' un concorrente del calore locale: e' il
suo PARENTE PIU' PROSSIMO.** Le tre possibilita', e ### **la scelta e' di Luca**:

| | |
|---|---|
| **(a) il calore lo SOSTITUISCE** | lo scuotimento diventa **un caso** del calore: *«dove c'e' stress, c'e' calore»* |
| **(b) il calore lo RICEVE** | lo scuotimento resta la **sorgente** *(il vuoto)*, e il calore e' ### **cio' che ne resta e si conduce** |
| **(c) si AFFIANCANO** | due meccanismi distinti — ### **e allora va detto perche' due** *(`9-ter`)* |

---

# **(C-bis) TRE CORREZIONI A COSE CHE AVEVO SCRITTO** *(rilievi del guardiano, 2026-10-01)*

## ⛔ **① LA DIVISIONE NON SCATTA «SOPRA `3π`»: E' UNA PROBABILITA' A CAMPANA**

La soglia non e' netta: e' ### **`segno = −tanh(3·(pos − centro))`** attorno a `pos_soglia`, cioe'
### **una campana**, non un gradino.
### ✅ **E `:M1` LO MOSTRA DA SE':** fra gli otto archi divisi ce n'e' uno con ### **`|tw| = 3.79`**,
cioe' ### **mezzo giro SOTTO `2π`** e ### **molto sotto `3π`.** ### **Un gradino a `3π` non
l'avrebbe mai diviso.**
### ➜ **Va corretto QUI e nella STORIA DELLA MITOSI**, dove la soglia e' descritta come netta. E il
### **`3.0` dentro la `tanh` entra nell'elenco del criterio 2**: ### **e' un numero scelto a mano.**

## ⛔ **② `dir_laterale` NON E' SIMMETRICA, e la mia «verifica» era sbagliata**

Avevo scritto, fra le *«verifiche fatte prima di accusare»*, che `dir_laterale` ### **«nasce dal
punto medio»**. A `:8040`:
```
v_rel        = self.pos[jj] - self.pos[ii]
dir_radiale  = v_rel / |v_rel|
dir_laterale = (-dir_radiale[1], dir_radiale[0], 0)
```
### **Nasce da `pos[jj] − pos[ii]`: SI INVERTE col verso.** Avevo letto `_rmid` di un ### **ALTRO
blocco** della stessa funzione e gliel'avevo attribuito.
### ➜ **Il sito ② di `MEM-HEBB-VERSO` ha TRE dipendenze dal verso, non due.** ### **Il verdetto di
`:M2` non cambia; la mia verifica si'** — e si ### **ANNOTA**, non si riscrive (par.8).

## ⭐ **③ IL CRITERIO «NON ESPLODE» ERA SBAGLIATO, NON IL SISTEMA** *(`FINESTRA-DEL-PICCO`)*

| | |
|---|---|
| a **72** passi | `K_fase` cresce in ### **72 passi su 72** ed e' al ### **100 % del suo massimo** *(× 85.1)*, a volume quasi fermo *(`sum(d)` × 1.0095)* |
| a **150** passi | il massimo e' ### **al passo 88**, e la fine e' al ### **77.7 % del massimo**; cresce in ### **95 passi su 150** |

### ➜ **IL SISTEMA NON ESPLODE: sale, passa per un PICCO, e scende.** E da una finestra di 72 passi
### **«cresce senza fermarsi» e' INDISTINGUIBILE da «sta salendo verso un picco».**
### ✅ **Quindi il criterio del par. `(E)` si riscrive:** ### **non «non esplode», ma «NON CRESCE
SENZA TETTO su una finestra CHE CONTIENE IL PICCO»**, e ### **la finestra minima e' un DATO da
misurare, non da scegliere.**
### ⚠ **E vale per ogni sigillo che gira a 72 passi:** `72` e' la lunghezza scelta per la
### **byte-identita'**, dove il picco non c'entra — ### **ma non e' una lunghezza adatta a
giudicare una DINAMICA.**

---

# **(D) I CRITERI, fissati ORA, prima di qualunque numero e di qualunque legge**

| | il criterio | perche' |
|---|---|---|
| ### **1 — SIMMETRIA DELLA LEGGE, non del risultato** | ### **ogni legge su un arco e' UNA funzione, chiamata per i DUE estremi coi ruoli scambiati** | ### **`:M2` ha misurato che oggi non e' cosi'**: `self.phi[ii] += shift` applica a **un solo** estremo. Una simmetria *«che viene fuori»* dai numeri ### **non e' una simmetria: e' una coincidenza** |
| ### **2 — NESSUN COEFFICIENTE SCELTO A MANO** | `KICK_TW` · lo **`0.5`** del calcio chirale · il **`clip(±2)`** di `xi_termo` · il **pavimento `1e-6`** di `Tt` · il **`clip(±π/4)`** dello shift di fase · ### **il `3.0` dentro la `tanh` della soglia di divisione** · la **velocita' di conduzione** del calore · l'**accoppiamento calore-fase** | ### **`A1`: la legge, non il numero.** Ognuno ### **derivato oppure DICHIARATO** come scelto — e un numero dichiarato scelto e' un **difetto aperto**, non una soluzione |
| ### **3 — LOCALITA'** | nessuna media, mediana o somma **globale** dentro una legge locale | ### **`A2`**, ed e' il difetto per cui il Nose-Hoover va sostituito |
| ### **4 — BILANCIO CHIUSO, e sono DUE** | avvolgimento **e** energia, ### **separati**, e ### **ogni perdita DICHIARATA** | ### **`A8` applicato a una carica**: un avvolgimento che sparisce senza una riga che lo dica e' ### **un ripiego silenzioso DI FISICA** |
| ### **5 — STABILITA' DELLA CONDUZIONE rispetto al `dt`** | la conduzione del calore e' una **diffusione**: ha un **limite di stabilita'** che dipende da `dt` e dal grafo | ### **si collega a `DT-CONVERGENZA`**: una legge nuova che diverge a `dt` piccolo ### **non e' una legge, e' un artefatto dell'integratore**. ⚠ **E la forma esatta esiste gia' nel repo** *(`peq-esatto`: combinazione convessa, `exp(-dt/tau)`)*, ### **quindi non si usa un Eulero esplicito** |
| ### **6 — PER OGNI CAMBIAMENTO, IL CASO CHE DEVE FALLIRE** | scritto **prima** di girare | ### **`P1-sexies`**: senza il caso che deve fallire un sigillo non misura la cura, ### **misura se stesso** |

## ⭐ **CRITERIO 8 DI LUCA: LA DIVISIONE CREA SOLO SPAZIO NEUTRO** *(2026-10-01)*

> ### **La divisione da sola crea SOLO SPAZIO NEUTRO. La materia CARICA nasce solo A COPPIE: due
> ### nodi nuovi, uno `+1` e uno `−1`, LOCALMENTE — cosi' la carica totale NON CAMBIA.**

| | |
|---|---|
| ### **«per costruzione», non «per coincidenza»** | oggi la neutralita' ### **dipende dalle cariche dei genitori** *(`:G4`: `0` in 3 casi, `+2` in 2, sugli stessi `d_n = +2`)*. Il criterio chiede che sia ### **una proprieta' della LEGGE** |
| ### **due nodi NUOVI** | oggi lo Schwinger ne crea ### **UNO**, accanto a un genitore che c'era gia' *(`SCHWINGER-UN-NODO`)* |
| **localmente** | i due nodi nascono ### **vicini**, non uno qui e uno altrove: la carica si conserva ### **anche in una regione**, non solo in totale |
| ### ⚠ **e non si puo' provare prima di `D36`** | senza `FASE_2PI` l'antinodo ### **e' il genitore per il campo** *(`:G2`)*, quindi *«uno `+1` e uno `−1`»* ### **non e' distinguibile dal campo.** ### **`D36` viene PRIMA** |

## 📐 **E UN CRITERIO IN PIU' CHE `:M2` HA RESO NECESSARIO**

> ### **7 — NESSUNA SCRITTURA CON INDICI RIPETUTI E ASSEGNAZIONE SEMPLICE.**

`self.phi[ii] = (...)` con `ii` che contiene **ripetizioni** fa ### **vincere l'ultimo**, e scarta
tutti gli altri **in silenzio**. ### **Se la legge somma, si usa `np.add.at`; se scegli, si dichiara
il criterio della scelta.** ### **Il default di numpy non e' una legge fisica.**

---

# **(E) COME SI VERIFICA CHE IL REGIME RESTI AUTOSOSTENUTO**

### **E' la ragione per cui il termostato esiste, quindi e' il criterio che la sostituzione deve
passare.** Tre prove, e le soglie si fissano **qui**, prima dei numeri:

> ### ⚠ **RISCRITTO il 2026-10-01 dopo `FINESTRA-DEL-PICCO`:** la versione di prima diceva
> *«non esplode»* su **72 passi**, e ### **il sistema di riferimento NON l'avrebbe passata** —
> perche' a 72 passi e' al **100 % del suo massimo**. ### **Era il criterio a essere sbagliato.**

| prova | che cosa guarda | che cosa la fa FALLIRE |
|---|---|---|
| ### **(i) NON SI SPEGNE** | `K_fase` *(= `0.5·Σ phivel²`)* su una finestra ### **che contiene il picco** | ### **un decadimento monotono** verso zero: se `K_fase` cala in **ogni** sottofinestra, il sistema si sta spegnendo |
| ### **(ii) NON CRESCE SENZA TETTO** *(non piu' «non esplode»)* | la stessa serie, ### **e dove sta il MASSIMO** | ### **il massimo ALLA FINE della finestra**, che vuol dire ### **finestra troppo corta e giudizio impossibile**; oppure una crescita che ### **non ha massimo** su una finestra che per il riferimento lo contiene; oppure ### **un solo invariante violato** |
| ### **(0) LA FINESTRA, e si misura PRIMA** | la **lunghezza minima** che contiene il picco del **riferimento** | ### **misurata: il picco e' al passo 88**, quindi ### **72 passi NON BASTANO e 150 si'.** Una prova di dinamica su 72 passi ### **non e' una prova** |
| ### **(iii) IL CONTO TORNA** | ### **il bilancio dell'energia, voce per voce** | ### **un residuo non dichiarato**: cio' che entra meno cio' che esce meno il calore ### **deve fare zero entro la precisione**, e il residuo si **riporta** |

### ⚠ **E LA PROVA (iii) SI PUO' FARE SOLO CON L'IMBRAGATURA DEL COMMIT 1**
Il controllo del registro gira ### **dopo OGNI voce**, quindi una **spia** su di esso rende ogni
confine di voce ### **un punto di misura** — ed e' come `:M1`, `:M4` e `:M6` sono state misurate.
### **Senza quell'attribuzione per voce, «il conto torna» non e' verificabile**: si vedrebbe solo
un totale a fine passo.

---

# **(F) LA DIPENDENZA DAL RIORDINO: quando si puo' scrivere la legge nuova**

> ### **La legge nuova si scrive SOLO DOPO IL COMMIT 3** *(la nascita come EVENTO UNICO)*.

**Perche' il 3 e' obbligatorio:** il calore **nasce alla divisione**, e oggi la nascita e'
### **sparsa in piu' punti** con ordini di estrazione casuale non dichiarati. ### **Una regola di
nascita per `T_nodo` scritta prima del commit 3 andrebbe scritta IN PIU' POSTI**, e due copie
divergono — ### **e' lo stesso argomento di `_cs_arco_da_nodo`.**

## ❓ **E SERVE ANCHE IL `6a`? SI', E LA RAGIONE E' MISURATA**

### **Il `6a` rende esplicita la frazione `t`**, e `T_nodo` alla nascita e' ### **«media dei
genitori + il calore liberato»** — ### **ma «media» e' il caso `t = 0.5`.** Appena `t ≠ 0.5` la
media giusta e' ### **pesata su `t`** *(il figlio sta a `t·d` da `a` e a `(1−t)·d` da `b`)*.
### ➜ **Senza il `6a`, `t` vive in QUATTRO formule indipendenti** e la regola di nascita del calore
### **diventerebbe la quinta.** ### **Con il `6a`, `t` e' in un posto solo e la regola la legge da
li'.**
### ⚠ **E c'e' un secondo motivo, piu' forte:** `:M5` ha misurato che ### **`pos` e' FISICA**
*(5 leggi la leggono)*. Quindi `t` ### **non e' un dettaglio di resa**: decide **una posizione che
la fisica legge**, e il calore che nasce *«in mezzo»* ### **nasce in un punto che conta.**

---

# **(G) LE DECISIONI PER LUCA, una per una**

> ### **Non ne prendo nessuna.** Ognuna ha ### **cosa esattamente la deciderebbe**, perche' *«una
> voce senza criterio non e' un fronte: e' un desiderio»* (par.4).

| | la decisione | che cosa la decide |
|---|---|---|
| ### **1** | ### **L'AVVOLGIMENTO SI CONSERVA O SI SCIOGLIE?** I figli ereditano la loro parte di `tw`, oppure una parte ### **si scioglie in rotazione** *(e allora il calcio ai genitori e' quella parte)* | ### **`:M1` E' MISURATA, E DA' DUE LETTURE OPPOSTE** — e vanno lette **insieme**: ### **in relativo sulla rete e' `5.36e-05`**, trascurabile — ### **ma solo perche' le divisioni sono OTTO in 72 passi**; ### **per evento sparisce `1.17` AVVOLGIMENTI INTERI** *(min `0.60`, max `1.33`, con `PHI_CRIT = 2π` esatto)*, cioe' ### **tutto l'avvolgimento dell'arco**. ### ➜ **Non e' un arrotondamento: e' una carica che svanisce, e il pozzo cresce col RITMO delle divisioni** |
| ### **2** | ### **IL NOSE-HOOVER SI SOSTITUISCE O SI AFFIANCA IN PROVA?** | il rischio del par. **(C)**: ### **senza un «fuori» il sistema puo' solo perdere.** ### **Affiancare permette un A/B a variabile singola**; sostituire e' piu' pulito ma ### **se sbaglia, spegne il sistema** |
| ### **3** | ### **QUALE GRANDEZZA DECIDE `t`?** I candidati che lo stato offre: `tw`, la **densita'**, `psi`, il **tempo proprio** | ### **non ne propongo uno.** Il vincolo e' il criterio **1** del par. **(D)**: `f(a,b) = 1 − f(b,a)` |
| ### **4** | ### **IL RUOLO DELLO SCUOTIMENTO:** sostituito, sorgente, o affiancato *(le tre vie del par. **(C)**)* | ### **`:M6` E' MISURATA**: `+1.22e+03` per passo *(mediano)*, ### **positivo in 72 passi su 72**, e ### **torsione ZERO ESATTO**. ⚠ **Ma il confronto che deciderebbe NON e' ancora possibile:** serve ### **`:M7`** *(la potenza del solo `−xi·phivel`)*, perche' il netto di `step` ### **non separa il termostato dall'attrito e dalla coppia** |
| ### **5** | ### **`MEM-HEBB-VERSO` BLOCCA IL RUN BASE?** | e' nell'indice come ### **`DA-DECIDERE`**: curarlo ### **cambia la fisica di OGNI passo**, non solo quella delle nascite. ### **E' la decisione piu' urgente delle cinque**, perche' finche' non e' presa ### **ogni misura nuova nasce su un sistema che dipende dall'ordine di memorizzazione degli archi** |

---

# **(G-bis) I FRONTI APERTI DA QUESTO GIRO, che non appartengono al calore**

*(Si scrivono qui perche' sono nati misurando, e ### **un riscontro non relazionato e' un riscontro
perso** (par.4). ### **Nessuno di questi si cura in questo giro.**)*

| | il fronte |
|---|---|
| ### **`MEM-HEBB-VERSO`** | il verso dell'arco entra nella fisica, in **due siti** di `memoria_hebbiana_moto`. ### **E' la decisione 5**, ed e' la piu' urgente |
| ### **«stesso path vince l'ultimo», forma nuova** | `self.phi[ii] = (...)` con `ii` **ripetuto**: ### **vince l'ultimo arco**, gli altri sono scartati in silenzio. ### **E' il criterio 7** |
| ### **`MEM-HEBB-PIANO-XY`** | `dir_laterale` ruota di 90 gradi ### **nel solo piano `xy`** e azzera `z`: ### **un piano preferito** in una legge che dovrebbe essere isotropa. ### **Non misurato** |
| ### **il clip `±2` di `xi_termo`** | ### **non scatta mai** *(`:M3`)*: `A9` + `A11` — si cerca **l'errore** da cui proteggeva, e se non c'e' **esce** |
| ### **UNA SOLA funzione per «confronta due stati»** | la trappola dei **non finiti** *(`inf − inf = NaN`)* mi e' costata ### **DUE volte in una sessione, in due file diversi**, e la distanza **ciclica** di `phi` una terza. ### **Oggi ogni strumento ha il suo confronto**, e ### **ognuno sbaglia per conto suo**: la regola di confronto *(non finiti, cicliche, assenti in entrambi, antisimmetriche)* ### **merita UN posto solo** (`9-ter`) |

---

# **(H) CHE COSA QUESTO PIANO NON PROMETTE**

| | |
|---|---|
| ### **non introduce un'energia** | `M0` dice che **non esiste**, e la forma naturale e' ### **PROPOSTA**. Introdurla e' una decisione di fisica, ### **non una conseguenza di questo piano** |
| ### **non cura `MEM-HEBB-VERSO`** | lo **misura** e lo **registra**. ### **La cura cambia la fisica di ogni passo** e vuole il suo commit, il suo sigillo e la decisione **5** |
| **non dice quale legge** | dice ### **la FORMA** *(una legge sola, due bilanci, locale, simmetrica, senza numeri a mano)*. ### **La legge la decide Luca** |
| ### **e non e' una misura** | e' un **piano**. ### **Ogni numero che contiene e' misurato e committato**, e ogni numero che non c'e' ### **e' un criterio, non una previsione** |
| ### **e UNA MISURA LA DICHIARA MANCANTE** | ### **`:M7`**, la potenza del solo termine del termostato. ### **Senza di lei la decisione 4 non ha il suo numero**, e ### **lo dico invece di stimarla** |
