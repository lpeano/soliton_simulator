# L'INDICE `v2`, FASE `2` — **la classificazione PER CONTENUTO e la bonifica**

> ### ⛔ **I `6` CONTROLLI PASSANO**, e il primo resta quello che conta: ogni ID del vecchio indice sta in ### **UNO E UNO SOLO** posto — ### **`0` persi, `0` doppi**, anche dopo aver spostato `54` segnaposto.
>
> *I numeri ### **prima** escono dal commit `3ef2326` *(la fine della fase `1`)*, quelli ### **dopo** dal disco. Nessuno e' ricopiato a mano.* *(`L-NUMERI`)*

---

# ⭐ `①` **I CONTEGGI, PRIMA E DOPO**

| | prima | ### **dopo** |
|---|--:|--:|
| voci | 867 | ### **813** |
| etichette rimosse | 85 | ### **138** |
| righe di storico *(ogni modifica, col suo motivo)* | 0 | ### **982** |

| `dominio` | prima | ### **dopo** | |
|---|--:|--:|---|
| `DA_CLASSIFICARE` | 664 | ### **179** | ### **-485** |
| `FISICA` | 94 | ### **454** | ### **+360** |
| `METODO` | 79 | ### **114** | ### **+35** |
| `INFRASTRUTTURA` | 30 | ### **43** | ### **+13** |
| `DOCUMENTAZIONE` | 0 | ### **23** | ### **+23** |

| `era` | prima | ### **dopo** | |
|---|--:|--:|---|
| `DA_CLASSIFICARE` | 713 | ### **181** | ### **-532** |
| `1` | 46 | ### **424** | ### **+378** |
| `ENTRAMBE` | 65 | ### **165** | ### **+100** |
| `2` | 43 | ### **43** | = |

| `stato` | prima | ### **dopo** | |
|---|--:|--:|---|
| `DA_CLASSIFICARE` | 480 | ### **181** | ### **-299** |
| `CHIUSA` | 187 | ### **187** | = |
| `SOSPESA` | 46 | ### **246** | ### **+200** |
| `APERTA` | 111 | ### **156** | ### **+45** |
| `AGENDA` | 43 | ### **43** | = |

| `classe` | prima | ### **dopo** | |
|---|--:|--:|---|
| `DIFETTO` | 441 | ### **209** | ### **-232** |
| `FRONTE` | 166 | ### **168** | ### **+2** |
| `CRITERIO` | 91 | ### **95** | ### **+4** |
| `NON_DEFINITA` | 0 | ### **179** | ### **+179** |
| `MISURA` | 54 | ### **54** | = |
| `CURA` | 46 | ### **46** | = |
| `TEORIA` | 51 | ### **0** | ### **-51** |
| `PRESIDIO` | 16 | ### **34** | ### **+18** |
| `STANDARD` | 2 | ### **28** | ### **+26** |

### ⭐ **IL NUMERO CHE RIASSUME:** `dominio DA_CLASSIFICARE` passa da ### **`664`** a ### **`179`**, e `stato DA_CLASSIFICARE` da ### **`480`** a ### **`181`**.

# ⛔ `②` **CHE COSA RESTA `DA_CLASSIFICARE`, E PERCHE'** — *`181` voci*

| gruppo | quante | ### **perche'** |
|---|--:|---|
| ### **CONCETTI DA DEFINIRE** *(classe `NON_DEFINITA`)* | ### **`179`** | erano segnaposto, e ### **il CODICE o i SIGILLI li nominano**: non sono etichette di documento, e non si sa ancora ### **che cosa siano**. Ciascuno porta in `nota_guardiano` ### **dove e' nominato** |
| ### **il DUBBIO dichiarato** | ### **`2`** | il contenuto ### **non basta** a decidere, e sta scritto in `meta.motivo_dubbio` |

### **IL DUBBIO, una per una:**

| id | dominio | ### **perche' non si decide** |
|---|---|---|
| `B7` | `FISICA` | <<i reperti DA RIMISURARE sulla scena nuova | Z43, Z46, Z48-Z52>>: ### E' UN CONTENITORE di piu' reperti, e l'era dipende da CIASCUNO |
| `I1` | `FISICA` | <<IDEA DI LUCA, PER DOPO: costruire UNA massa, farla maturare, leggerne la struttura>>. ### E' FISICA, ma <<per dopo>> non dice SE e' dell'era 2: non sta nelle AGENDA di Luca, e indovinarlo sarebbe in |

> ### ✔ **IL DUBBIO E' UN ESITO LEGITTIMO**, e il mandato lo dice: *«NON c'e' un numero minimo di voci da classificare»*. ### **Due su `247` non si decidono dal contenuto, e le lascio lì.**

# ⚠ `③` **LE VOCI `da_dividere`, con la PROPOSTA** — *`2`*

| id | dominio / era | ### **perche' sono DUE** | ### **la proposta** |
|---|---|---|---|
| `B6` | `FISICA` / `1` | il testo dice ### **DUE**: <<titolo_breve INTERO: le due cure OFF: COPPIARECIPROCA e GRAVAMPIEZZA | :739 e :732 (entram>> | PROPOSTA: dividere per flag -- una voce per COPPIA_RECIPROCA e una per GRAV_AMPIEZZA, perche' si accendono e si misurano SEPARATAMENTE |
| `M2` | `FISICA` / `1` | il testo dice ### **DUE**: <<titolo_breve INTERO: LA MITOSI — DUE DIFETTI DA ACCLARARE. ① il figlio nasce nel PUNTO MED>> | PROPOSTA: dividere in <<il figlio nasce nel punto medio>> e il secondo difetto elencato, ciascuno con la sua misura |

### ⛔ **LA DIVISIONE LA DECIDE LUCA.** Io ho ### **classificato e marcato**, non diviso.

# ⭐ `④` **I SEGNAPOSTO, PER ESITO** — *`233` da decidere*

| esito | quante | come si e' deciso |
|---|--:|---|
| ### **ALIAS** di una voce vera | ### **`1`** | `CONFIG-1/` → `CONFIG-1`: l'id ### **ripulito dalla punteggiatura finale** coincide con una voce VERA. ### **L'importatore vecchio aveva tagliato male** |
| ### **ETICHETTA DI DOCUMENTO** | ### **`53`** | ### **TUTTE** le citazioni stanno in documenti o in ### **strumenti dell'indice**: sono ### **marcatori di sezione e titoli** |
| ### **CONCETTO DA DEFINIRE** *(resta)* | ### **`179`** | e' citato ### **nel CODICE o nei SIGILLI** — `soliton_simulator.py`, le sue copie `_sim_*`, `csv/_test_fork/`, `csv/_seal_fork/` — quindi ### **il codice stesso lo nomina** |

### **LE ETICHETTE RIMOSSE IN QUESTA FASE, le piu' citate:**

| id | citazioni | che cos'era |
|---|--:|---|
| `DA-DECIDERE` | 20 | (fase2-b2) e' un VALORE della vecchia colonna `stato`, non una voce |
| `AAAA-MM-GG` | 11 | (fase2-b2) e' il FORMATO DI UNA DATA, citato in `CLAUDE.md` e negli script: non e' un ID, e' un segnaposto di formato |
| `GLOBALE-DISEGNO` | 6 | (fase2-b2) TUTTE le citazioni stanno in documenti o in strumenti dell'indice: e' un MARCATORE o un TITOLO, non una voce |
| `FORK-FIRST` | 5 | (fase2-b2) TUTTE le citazioni stanno in documenti o in strumenti dell'indice: e' un MARCATORE o un TITOLO, non una voce |
| `MANDATO-REGISTRO` | 4 | (fase2-b2) TUTTE le citazioni stanno in documenti o in strumenti dell'indice: e' un MARCATORE o un TITOLO, non una voce |
| `POST-HOC` | 4 | (fase2-b2) TUTTE le citazioni stanno in documenti o in strumenti dell'indice: e' un MARCATORE o un TITOLO, non una voce |
| `RI-GIRABILE` | 4 | (fase2-b2) TUTTE le citazioni stanno in documenti o in strumenti dell'indice: e' un MARCATORE o un TITOLO, non una voce |
| `ROMPI-ANELLO` | 4 | (fase2-b2) TUTTE le citazioni stanno in documenti o in strumenti dell'indice: e' un MARCATORE o un TITOLO, non una voce |
| `SOVRA-CORREGGE` | 4 | (fase2-b2) TUTTE le citazioni stanno in documenti o in strumenti dell'indice: e' un MARCATORE o un TITOLO, non una voce |
| `ZZ999` | 4 | (fase2-b2) e' un marcatore di PROVA degli strumenti |
| `ARCHI-PASSO` | 3 | (fase2-b2) TUTTE le citazioni stanno in documenti o in strumenti dell'indice: e' un MARCATORE o un TITOLO, non una voce |
| `AUTO-MANUTENZIONE` | 3 | (fase2-b2) TUTTE le citazioni stanno in documenti o in strumenti dell'indice: e' un MARCATORE o un TITOLO, non una voce |
| `CURE-FINE` | 3 | (fase2-b2) TUTTE le citazioni stanno in documenti o in strumenti dell'indice: e' un MARCATORE o un TITOLO, non una voce |
| `CURE-INIZIO` | 3 | (fase2-b2) TUTTE le citazioni stanno in documenti o in strumenti dell'indice: e' un MARCATORE o un TITOLO, non una voce |

> ### ⭐ **E UNA CHE NON HO TOLTO, e merita il suo nome:** `RIDUZIONE-AL-LIMITE` e' la ### **proprieta' dichiarata dello spinore** — *«con `_psi_spinor=(e^{iφ},0)` la componente `0` == campo scalare»* — ed e' ### **il soggetto di `CENS-A1`, una voce BLOCCANTE.** ### **Non e' un'etichetta: e' un concetto che il codice nomina.**

# ✔ `⑤` **LE `51` VOCI `TEORIA`, CORRETTE** — *e la causa era un difetto della migrazione*

### ⛔ **Nessuna delle `51` era una teoria.** Erano ### **`19` assiomi** *(`A1`…`A15`, `A3c`, `A7b`, `P-DECADIMENTO`, `P-MEMORIA`)*, i ### **presidi** *(`H-*`, `L-*`, `P1-*`)*, gli ### **standard** *(`STANDARD-4/6/8/10`, `L-SOGLIA`, `P1-sexies`)*, i ### **criteri di sigillo** *(`K2a`, `K2b`, `T3a`, `T3b`)*, un ### **difetto del driver** *(`M0a`)* e ### **due fronti** *(`GEOMETRIA-DELLA-CRESCITA`, `REVERSIBILITA-LOCALE`)*.

> ### ⭐ **LA CAUSA, e e' un difetto MIO:** nell'indice dell'era `1` ### **`teoria` era uno STATO**, e voleva dire *«questa e' una regola o un assioma, non un difetto»*. ### **La mia migrazione l'ha trasportato come CLASSE.** ### ➜ **Un campo usato per dire un'altra cosa e' esattamente cio' che i vocabolari chiusi esistono per impedire**, e sta ora scritto in `doc/REGOLE/par9.md` perche' non si rifaccia.

### **LA CURA:** la classe viene dal ### **`tipo_era1`**, che e' ### **un campo dichiarato** — `assioma` → `STANDARD`, `presidio` → `PRESIDIO`, `standard` → `STANDARD`, `criterio-locale` → `CRITERIO`, `fronte` → `FRONTE`. ### **Nessuna parola chiave.** E i cinque nominati dal mandato: `K2a` e `K2b` col ### **padre `OSSERVABILE-P1`**, `T3a` e `T3b` col ### **padre `DRIVER-SCENA-II`** *(i padri esistono, verificato prima di scriverli)*, `M0a` → `DIFETTO`/`INFRASTRUTTURA`.

# ⚠ `⑥` **GLI ASSIOMI RICLASSIFICATI: IN ATTESA DI CONFERMA** — *`20` voci*

| dominio | quali |
|---|---|
| ### **FISICA**, era `ENTRAMBE` | `A1` `A10` `A11` `A13` `A14` `A15` `A2` `A3` `A3c` `A4` `A5` `A6` `A7` `A7b` `P-DECADIMENTO` `P-MEMORIA` |
| ### **METODO**, era `ENTRAMBE` | `A12` `A8` `A8b` `A9` |

### ⛔ **Ognuna porta `meta.nota_guardiano` con «da confermare da Luca»**, come il mandato chiede: la ### **`FISICA`** vincola la forma delle leggi o descrive il comportamento del sistema, la ### **`METODO`** parla di ### **come si lavora e si verifica.** ### **Non e' una decisione: e' una proposta in attesa.**

# ⛔ `⑦` **I DISACCORDI CON LE LISTE DEL GUARDIANO**

| | |
|---|---|
| ### **la divisione `METODO`/`INFRASTRUTTURA`** *(punto `1 d`)* | ### ✔ **NESSUN DISACCORDO: ho applicato tutte e nove.** Parlano della ### **validita' delle misure**, non del codice come strumento, e il mio giudizio di prima era ### **piu' grossolano** |
| ### **le tre liste `L1` `L2` `L3`** | ### ✔ **non cambiano**, e il controllo `C3` lo verifica — ### **con le correzioni `(c)` e `(d)` dentro**, altrimenti rifiutava una correzione ### **chiesta** |
| ### ⚠ **ma UNA correzione MIA alle liste, e la dichiaro** | ### **`Z87` `Z90` `Z91` `Z92`** erano finite in ### **`AGENDA`** per un ### **mio** errore: avevo letto `[EPOCA 2]` come l'### **era `2` dello schema**. ### ⛔ **Falso:** le epoche `1`-`2`-`3` sono ### **fasi di lavoro sul SECONDO ordine** *(`Z91`: «`SCALA_MIN` frena ogni scrittura»)*, mentre l'era `2` e' ### **la riscrittura al primo ordine**, cioe' la ### **lista `L2`**. ### ➜ **Corrette, e `AGENDA` ora e' `43` = ESATTAMENTE la lista `L2`** |

# ⛔ `⑧` **IL DIFETTO PIU' GRAVE DI QUESTO GIRO, ED E' MIO**

> ### ⛔ **IL CONTROLLO `C4` -- l'IDEMPOTENZA -- VERIFICAVA RILANCIANDO LA MIGRAZIONE.** E la migrazione ### **riscrive `voci.jsonl` PARTENDO DAL TAG.** ### ➜ **Finita la fase `1` era un controllo innocuo; dopo la fase `2` era DISTRUTTIVO, e mi ha cancellato `867` classificazioni in un colpo** *(`dominio DA_CLASSIFICARE` da `233` a `664`, `classe TEORIA` da `0` a `51`)*.

| | |
|---|---|
| ### **come l'ho preso** | `C4` diceva *«FALLISCE — diversi: `voci.jsonl`»*, e ho guardato i conteggi ### **subito dopo**: quel *«diversi»* ### **non era un difetto dell'idempotenza — era il DANNO** |
| ### **il ripristino** | `git checkout` di `doc/indice` e delle viste. ### **Tutto il lavoro era COMMITTATO**, e l'unico passo perso e' stato quello dei segnaposto, rifatto |
| ### ✔ **la cura `1`** | la migrazione ### **conta le righe di `storico.jsonl`**: la migrazione ### **non scrive storico**, quindi ogni riga e' ### **lavoro di dopo** — e allora ### **si ferma**, a meno di `--forza`. ### **Provato: con `803` righe si ferma** |
| ### ✔ **la cura `2`** | `C4` ### **non rilancia piu'** se c'e' lavoro di dopo: dichiara l'idempotenza ### **verificata al suo commit** *(`6b8cb90`)*, dove l'ha davvero provata |

### ⚠ **E sta scritto nel SORGENTE di entrambi, non solo qui:** ### **un controllo che distrugge cio' che controlla e' il difetto piu' facile da rifare.**

---

# ⛔ **CHE COSA QUESTO REFERTO NON DICE**

| | |
|---|---|
| che l'indice sia ### **finito** | ### ⛔ **no: `181` voci restano `DA_CLASSIFICARE`**, e `179` di loro sono ### **concetti che il codice nomina** e che nessuno ha ancora definito |
| che la classificazione sia ### **verificata** | ### ⚠ **no: la verifica voce per voce la fa IL GUARDIANO.** Io ho scritto, per ognuna, ### **un motivo che CITA il testo** — `982` righe di storico |
| che gli ### **assiomi** siano a posto | ### ⛔ **sono una PROPOSTA**, e ogni voce porta *«da confermare da Luca»* |
| che le ### **`da_dividere`** siano divise | ### ⛔ **no: sono MARCATE**, con la proposta. ### **La divisione la decide Luca** |
| che le ### **regole** usate siano infallibili | ### ⚠ **una l'ho SCARTATA** *(fonte `doc/REGISTRO_FISICA.md` → `FISICA`)* perche' lì stanno ### **sia** criteri di fisica ### **sia** criteri di ### **verifica**: quelle `55` le ho ### **lette**, e `13` sono finite in `METODO` |
