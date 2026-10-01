# 🧭 **IL PIANO: IL RIORDINO DELLA MITOSI** *(`T3`, passo 2 — 2026-10-01)*

> ### ⚠ **QUESTO E' UN PIANO: NESSUNA RIGA DI CODICE DEL SIMULATORE.** Blob **`62d67675`**.
> **La base e' il REGISTRO DELLE GRANDEZZE**, e la storia e' in `doc/MITOSI_storia.md` *(`e97fc073`)*.
> ### **STOP dopo questo commit**, come da mandato.

**Il numero da cui parte tutto, misurato dall'AST:** `mitosi` e' **549 righe**, scrive **56
attributi** in **79 punti**, e delle **30** grandezze del registro ### **ne scrive 16 qui, 13 in due
funzioni di servizio, e 1 per mutazione in posto.**

---

# **(a) DECISIONE: chi decide la divisione, quando, e cosa legge**

## Com'e' oggi

| | |
|---|---|
| **dove** | dentro `mitosi`, nelle prime ~270 righe |
| **la soglia** | `soglia0 = PHI_CRIT + twist_max` = ### **`3π`** *(`2π` quanto + `π` twist dipolare massimo)*, **oppure `PHI_CRIT`** con `FASE_2PI` |
| **la modulazione** | `soglia = soglia0 * (1 − 0.3·tanh(grad_r))` — ### **il `0.3` e' SCELTO** |
| **cosa legge** | `tw` *(avvolgimento)* · `_r_nodo_mitosi()` *(tempo proprio)* · `_rho_sorgente()` *(densita')* · `peq` · `massa_critica_collasso()` · `_deg` · `pos` *(per lo Schwinger)* |
| **i filtri a valle** | `MITOSI_2LAM` *(OFF)* · `MITMAX` *(0)* · `MITOSI_DIR` *(0.0)* · la **campana** di criticita' |

## Che cosa il riordino fa, e che cosa NON fa

| | |
|---|---|
| ### ✅ **SEPARA la decisione dall'esecuzione** | `decidi_divisione(net) -> (archi_da_dividere, perche')`: ### **legge e NON SCRIVE NIENTE.** Oggi decisione e scrittura sono **intrecciate** per 270 righe, e per questo *«chi decide»* non si puo' nemmeno leggere |
| ### ⛔ **NON cambia la soglia** | `3π` resta **identica**, e il piano lo dichiara: ### **byte-identico**. Ma ### **la soglia E' `D36`** *(acclarato per misura: con `phi` su `2π` gli archi sopra soglia passano da **7047 a ZERO**)*, e ### **un riordino che la tocca cambia la fisica** |
| ### ⛔ **NON cambia il `0.3`** | resta, ### **e si DICHIARA come numero non derivato** nel registro fisica. **Toglierlo e' una cura a se'** |

## 🛑 **Le domande che NON decido io**

| | |
|---|---|
| **1** | ### **la soglia si riscrive ADIMENSIONALE** *(un rapporto a `PHI_CRIT`, cosi' che non dipenda dal dominio di `phi`)*, **oppure resta assoluta e `D36` resta aperta?** |
| **2** | ### **il `0.3` si deriva o si toglie?** Se nessuna grandezza del sistema lo da', ### **`A1` dice di toglierlo** — ma togliere una modulazione **cambia dove nasce la materia** |
| **3** | ### **`massa_critica_collasso()` dentro una legge locale e' `A2`?** *(`U1`: 21 usi dentro leggi.)* E ### **i due pavimenti `1e-6`/`1e-3` da quale errore proteggono** *(`A11`)*? |
| **4** | ### **`MITOSI_DIR`**: il bias direzionale **entra** o si **archivia**? Oggi ### **il commento dice «ATTIVA» e il valore e' `0.0`** |
| **5** | ### **`MITMAX`**: resta un parametro, o diventa un **errore** come `MAX_NODI`? |

### **Criteri, fissati PRIMA dei numeri**

| | |
|---|---|
| ### **deve restare IDENTICO AL BYTE** | **tutto**: quali archi si dividono, quanti, e in quale ordine. ### **La separazione decisione/esecuzione e' una RIORGANIZZAZIONE, non una cura** |
| cosa puo' cambiare | ### **niente.** Un solo bit diverso ⇒ **non e' una separazione, e' una cura non dichiarata** |
| ### **il caso che DEVE fallire** | si **altera la soglia di `1e-12`** in una copia: il sigillo ### **deve vedere un numero di nascite diverso**. Se non lo vede, ### **il sigillo non guarda la decisione** |

---

# **(b) STRUTTURA: come nascono nodi e archi**

## Com'e' oggi

| | come |
|---|---|
| **il nodo** | `pos_figlio = 0.5·(pos[a] + pos[b])` → ### **il PUNTO MEDIO** |
| **gli archi** | l'arco `(a,b)` e' ### **SOSTITUITO** da `(a,m)` e `(m,b)`, lunghi `d/2` *(`keep` toglie lo spezzato)* |
| **`d` e `d0`** | `dh = d[sel]/2`, poi ### **`_nasce(...)` porta a `LAM` cio' che sta sotto** |
| **`tw` dei nuovi** | ### **`0`** *(`zz = zeros(len(sel))`)* |
| **lo Schwinger** | ### **AGGIUNGE** due archi verso `k` **senza togliere** `(aa,bb)`, e ### **`dd` viene da `pos`** |

## ⛔ **Il confine che NON tiene, e lo dico invece di assorbirlo**

> ### **`M2` ① e ②, `U2` e `MITOSI_2LAM` NON si possono separare da questa parte.**
> La parte (b) **e'** *«come nascono `pos`, `d`, `d0`»*, e ### **il punto medio e la fabbricazione di
> lunghezza SONO quella descrizione.** Non sono voci accanto al riordino: ### **sono il riordino.**

| il difetto | la scelta che va DICHIARATA |
|---|---|
| ### **`M2` ①** il figlio a `d/2` da ciascun genitore e' ### **sotto `LAM` se `d < 2·LAM`** → viola **`A13`** | **(i)** si **rifiuta** la divisione *(e' `MITOSI_2LAM`, che esiste ed e' **OFF**)* · **(ii)** si accetta e ### **`A13` non vale alla nascita**, e va **scritto** |
| ### **`M2` ②** due meta' portate a `LAM` danno ### **`2·LAM` al posto di `d`**: **fabbricano lunghezza** | **(i)** `MITOSI_2LAM` ON ⇒ ### **il caso non esiste piu'** · **(ii)** si accetta, e ### **il motore di gonfiamento va DICHIARATO e MISURATO** |

### 🛑 **DECIDE LUCA, e non ne scelgo una.** ### **Ma le due domande stanno DENTRO il piano**, perche'
la parte (b) non si puo' scrivere senza rispondervi. **La mia osservazione, non la mia decisione:**
### **`A13` e la conservazione della lunghezza non possono valere entrambe alla nascita** — una delle
due cede, e il riordino e' il posto giusto per **dire quale**.

### **Criteri, fissati PRIMA dei numeri**

| | |
|---|---|
| ### **con `MITOSI_2LAM` OFF** | ### **byte-identico**: `pos`, `i`, `j`, `d`, `d0`, `tw` dei nati **identici** |
| **con `MITOSI_2LAM` ON** | ### **NON byte-identico, ed e' atteso**: si **misura** quante divisioni vengono **rifiutate** e di quanto cala `n` al passo 72. ### **Il numero si riporta, non si giudica** |
| ### **il caso che DEVE fallire** | una copia in cui `pos_figlio` e' spostato di `1e-9`: il sigillo ### **deve vederlo**. E una in cui `tw` dei nuovi archi e' `1e-12` invece di `0`: ### **deve vederlo** |

---

# **(c) LA NASCITA COME EVENTO UNICO**

> ### **Tutte le grandezze del registro scritte in UN SOLO punto, con UNA regola dichiarata per
> ciascuna. Niente scritture sparse e niente sistemazioni a valle.**

## Il numero di oggi, e il bersaglio

| | oggi | dopo |
|---|---|---|
| posti che scrivono le grandezze della nascita | ### **3** *(`mitosi`, i due `_eredita_*`, piu' la mutazione di `conc_nodi`)* | ### **1** |
| grandezze del registro scritte in `mitosi` | **16 su 30** | ### **30 su 30, nel punto unico** |
| scritture che allungano | **38**, sparse | ### **una per grandezza, in tabella** |

## La forma proposta

```
nascita(net, evento, genitori, quante) -> None
    # per OGNI voce del registro, nell'ordine del registro:
    #   regola = REGOLA_DI_NASCITA[evento][nome]
    #   net.<nome> = regola(net, nome, genitori)
    # e NIENTE ALTRO scrive quelle grandezze.
```

| | |
|---|---|
| **la tabella** | ### **`REGOLE_nascita.tsv` (32 regole) e' il punto di partenza**, ed e' gia' **verificata per ancora** |
| ### **i QUATTRO eventi** | `semina` · `divisione` · `Schwinger` · `allaccio` — ### **decisi da Luca il 2026-09-29** |
| **le regole** | `eredita` · `media` · `zero` · `estrazione nuova` · ### **`eredita INVERTITA`** *(la carica alla Schwinger)* · ### **`derivata dalla definizione`** *(`perc_geom`)* |
| ### **il presidio** | ### **una grandezza del registro che NON compare nella tabella dell'evento ferma il run**: *«regola di nascita non dichiarata per `<nome>` all'evento `<evento>`»*. ### **E' lo stesso disegno del controllo unico, spostato alla nascita** |

### ⚠ **Che cosa questo richiede, e non e' gratis**

| | |
|---|---|
| ### **i due `_eredita_*` SPARISCONO** | le loro 13 grandezze entrano nella tabella. ### **Sono le funzioni nate dalle cure di `C7`/`C11`/`PSI-FLASH`**: il riordino **non le butta**, le **assorbe** — e la storia dice **perche' esistono** |
| ### **`conc_nodi` deve smettere di crescere per MUTAZIONE** | e' l'unica che cresce con `.append`, ### **invisibile all'AST e alla sorveglianza**. ➜ **O entra nel registro con una scrittura vera, o esce dal registro e la sua riparazione si motiva** |
| ### **la riallocazione di `_rep` deve sparire** | `_rep = zeros(...)` quando le lunghezze non tornano ### **butta la memoria in silenzio**, e sta ### **nell'unica finestra che il controllo unico non vede**. Con la nascita in un punto solo ### **quel ramo non ha piu' ragione di esistere** |

### **Criteri, fissati PRIMA dei numeri**

| | |
|---|---|
| ### **byte-identico, scena grande fino al 72, CON nascite** | **grandezze E contatori**, contro il blob di prima. ### **La nascita come evento unico e' una RIORGANIZZAZIONE: non deve cambiare un bit** |
| ### **e il CONTATORE e' il controllo piu' fine** | i rami della nascita **si contano** *(`_rep_realloc`, `_g_eredpsi_*`, `_ritmo_sicurezza`…)*: ### **un contatore che cambia di uno e' un difetto che le grandezze non vedrebbero** — misurato in questa sessione |
| ### **il caso che DEVE fallire** | **tre**, e sono quelli che dimostrano che il sigillo vede un difetto **della nascita**: ### **① si TOGLIE una grandezza dalla tabella** ⇒ deve fermarsi con *«regola non dichiarata»* · ### **② si cambia la regola di UNA grandezza** *(`psi` da `media` a `eredita`)* ⇒ il sigillo **deve vedere la differenza** · ### **③ si lascia una scrittura SPARSA a valle** ⇒ deve essere **impossibile**, cioe' il presidio deve nominarla |

---

# **(d) DERIVATE — generalizzazione 4: le derivate SPORCHE alla nascita**

> ### **Quando nasce un nodo, le derivate sono segnate DA RICALCOLARE; leggerne una sporca e' un
> ERRORE; tornano pulite quando la loro legge le riscrive.**
> ### **E' la regola «letta fra nascita e riscrittura» resa LEGGE DEL SISTEMA** invece di un
> accertamento fatto una volta con una misura.

## Quello che la misura ha gia' detto *(`bd9262f`)*

Nella finestra della nascita, delle **10** derivate *(8 per nodo, 2 per arco)*:

| | |
|---|---|
| **4** | ### **nessuna legge le legge** — `_chi_core_nodi` `_chi_core_rho0` `_chi_core_raggio` `_fatt_cs_ultimo` *(e per l'ultima il codice dichiara «nessun lettore, Z7»)* |
| **4** | la legge le trova ### **GIA' RISCRITTE** — `_chi_geom_nodi` `_r_corrente` `_dt_e_ultimo` `_sin2_vir` |
| ### **2** | ### **AUTO-RINFRESCO**: `_xi_rumore` *(ed **E'** la regola di nascita: il figlio non eredita l'ambiente)* e `_g_rampa_prec` *(diagnostica, disallineamento gia' contato)* |
| ### **BUCHI** | ### **ZERO** |

### ➜ **Quindi oggi la regola e' VERA. Ma e' vera per MISURA, su UNA scena e UNA configurazione** —
ed e' ### **il terzo limite che ho scritto nella scheda.** La generalizzazione 4 la rende **vera per
costruzione**.

## La forma proposta

| | |
|---|---|
| **la marca** | alla nascita, **ogni** voce di `REGISTRO_DERIVATE` entra in `net._sporche` |
| **la pulizia** | la **legge che la riscrive** la **toglie** da `_sporche` — ### **e non lo fa un'altra** |
| ### **la lettura** | leggere una derivata **sporca** ⇒ ### **`DerivataSporca`**, col **nome**, **chi** la legge e **quale legge** dovrebbe pulirla |
| ### ⚠ **il costo, e va detto** | intercettare **la lettura** costa: la sorveglianza di questa sessione ha misurato ### **1 887 282 accessi per passo** sulle sole 43 grandezze. ### **Un controllo su OGNI lettura non e' gratis come uno sui CONFINI delle voci** |

### 🛑 **La domanda che NON decido io**

> ### **La marca si verifica a OGNI LETTURA** *(costoso, e coglie tutto)* ### **oppure ai CONFINI
> DELLE VOCI** *(come il controllo unico: ~30 confronti per voce, e coglie «e' stata riscritta prima
> che la voce finisse»)*?
> **La mia osservazione:** ai confini delle voci ### **la regola diventa «una derivata non puo'
> attraversare un confine di voce sporca»**, che e' piu' debole della lettera del mandato ### **ma ha
> un costo noto e un presidio gia' in piedi.** ### **Decide Luca.**

### **Criteri, fissati PRIMA dei numeri**

| | |
|---|---|
| ### **byte-identico** | la marca **legge e scrive un insieme di nomi**: ### **non tocca una grandezza di fisica** |
| i contatori | ### **i contatori della MARCA sono «del presidio»** e cambiano per costruzione: si **separano per nome e si RIPORTANO**, come gia' fatto per `_g_registro_*` |
| ### **il caso che DEVE fallire** | ### **si rinvia la riscrittura di UNA derivata** *(per esempio non si ricalcola `_deg` in `mitosi`)*: deve alzare **`DerivataSporca`** e ### **nominare `_deg`**. **Se non lo fa, la marca non guarda niente** |

---

# **(3-bis) IL REGISTRO DICHIARATO, non misurato**

> ### **Una grandezza per nodo o per arco NON DICHIARATA ferma il run.**
> E' il ### **terzo limite** della scheda — *«una scena, una configurazione»* — e questo lo toglie.

## Come la trovo

| | |
|---|---|
| **il criterio** | ### **al controllo, si scorrono TUTTI gli attributi della rete** *(`vars(net)`)* e si cercano quelli che sono **array o liste** con ### **primo asse `== n` oppure `== m`** |
| **l'esito** | se il nome ### **non e' nel registro** *(ne' `STATO`, ne' `DERIVATE`, ne' `METRI`)* ⇒ ### **`GrandezzaNonDichiarata`**, col **nome**, la **forma** e il **tipo** trovati |
| ### **perche' vale con QUALUNQUE flag** | non parte da un elenco: ### **parte da cio' che la rete HA.** Un flag che crea una grandezza nuova la fa **comparire**, e il controllo la **nomina** |

## ⚠ **E come EVITO che la regola dipenda dai NOMI o dalla SINTASSI**

### **Questa e' la domanda piu' importante del paragrafo, perche' l'errore l'ho fatto SEI VOLTE in questa sessione:**

| volta | la regola sbagliata | che cosa ha nascosto |
|---|---|---|
| 1 | `full(n,…)` contato come *«estende»* | i siti che sostituivano |
| 2 | la condizione fusa chiamata *«inizializzazione»* | il difetto dentro l'`or` |
| 3 | `==`/`!=` messi *«fuori dal mandato»* | **sette** siti |
| 4 | il ramo degli `IfExp` **invertito** | una *«famiglia»* intera **inesistente** |
| 5 | il filtro per **NOME** che perde gli **alias locali** | 4 siti su 10 senza riga |
| 6 | la lista di **nomi** `semina`/`mitosi`/`_allaccia` al posto del **grafo** | **falsi BUCHI** nel registro |

> ### 📌 **La forma dell'errore e' SEMPRE la stessa: una regola che parte dal NOME o dalla SINTASSI
> invece che da CIO' CHE FA.** E la cura, provata tre volte in questa sessione, e' sempre la stessa:
> ### **non leggere il codice — GUARDARE LA RETE.**

**Quindi il presidio del registro dichiarato:**

| | |
|---|---|
| ### ✅ **parte dal RUNTIME, non dall'AST** | `vars(net)` e il **primo asse**: ### **nessun nome, nessuna sintassi, nessun alias.** Una grandezza si qualifica **per la sua FORMA**, che e' un **fatto**, non una convenzione |
| ### ✅ **e il suo CASO CHE DEVE FALLIRE e' banale e decisivo** | si aggiunge `net.pippo = np.zeros(net.n)` ⇒ ### **deve fermarsi nominando `pippo`.** ### **Se non lo fa, il presidio non guarda la rete** |
| ### ⚠ **il limite che RESTA, e lo dichiaro** | una grandezza con `len` **diverso** da `n` e da `m` ### **non viene vista** *(per esempio una per-faccia o per-ciclo)*. ### **Il presidio copre i due metri che il registro conosce, non tutti i metri possibili** |
| ### ⚠ **e le coincidenze** | se `n == m` i due metri sono **indistinguibili**. Oggi `12802` contro `471564`, ### **e lo strumento lo CONTROLLA e lo dichiara** — ma su una rete piccola potrebbe succedere |

### **Criteri, fissati PRIMA dei numeri**

| | |
|---|---|
| ### **byte-identico** | il presidio **legge** `vars(net)` e **solleva**: ### **non tocca niente** |
| **e il run sano non deve fermarsi** | ⇒ ### **tutte le grandezze per nodo/arco della configurazione del driver devono essere GIA' nel registro.** **Le 43 misurate ci sono**; ### **se ne compare una, e' informazione, non un difetto del presidio** |
| ### **il caso che DEVE fallire** | `net.pippo = zeros(n)` ⇒ **`GrandezzaNonDichiarata: pippo`**. ### **Piu' un secondo: `net.pluto = zeros(m)`** ⇒ deve nominare **`pluto`** e dire **per arco** |

---

# 📋 **L'ORDINE DEI COMMIT: piccoli, uno per cambiamento, ognuno col suo sigillo**

| # | commit | che cosa cambia | sigillo |
|---|---|---|---|
| **1** | ### **registro DICHIARATO** *(3-bis)* | `GrandezzaNonDichiarata`, e il controllo scorre `vars(net)` | byte-identico 72 + ### **`pippo` e `pluto`** |
| **2** | ### **decisione SEPARATA** *(a)* | `decidi_divisione` legge e non scrive. ### **Soglia e `0.3` INVARIATI** | ### **byte-identico, zero bit** + soglia alterata di `1e-12` ⇒ **deve** cambiare le nascite |
| **3** | ### **nascita come EVENTO UNICO** *(c)* | i due `_eredita_*` **assorbiti**, la tabella delle 32 regole, il presidio della **regola non dichiarata** | byte-identico 72, **contatori compresi** + i **tre** casi che devono fallire |
| **4** | ### **derivate SPORCHE** *(d, generalizzazione 4)* | la marca, e `DerivataSporca` | byte-identico + **riscrittura rinviata** ⇒ deve nominare la derivata |
| **5** | ### **STRUTTURA: `pos`, `d`, `d0`** *(b)* | ### **SOLO dopo la decisione di Luca su `M2`/`MITOSI_2LAM`**: con `OFF` byte-identico, con `ON` **misurato** | byte-identico a `OFF`; a `ON` il **calo di `n`** misurato e riportato |
| **6** | `perc_geom` del nato `= −1` | ### **FUORI dal riordino, gia' deciso.** Qui perche' ora il registro e' ### **l'unico posto che scrive una regola di nascita** | byte-identico **tranne** `perc_geom` dei nati, e il **frame-drag** misurato |

### ⚠ **Perche' `1` viene PRIMA di tutto**
Il **registro dichiarato** e' l'unico pezzo che ### **rende impossibile dimenticare una grandezza
mentre si sposta la nascita.** Farlo **dopo** vorrebbe dire riordinare ### **senza la rete di
sicurezza**, ed e' esattamente l'errore che la storia racconta **sette volte**.

### ⚠ **Perche' `5` viene DOPO**
Tocca la **fisica** *(`n` cambia)*. Tutto cio' che lo precede e' ### **byte-identico**, quindi se `5`
fallisce ### **si sa che e' lui**, e non uno dei quattro riordini.

---

# 🛑 **I CONFINI, dichiarati**

| voce | dove sta |
|---|---|
| **`perc_geom` del nato** | ### **commit 6**, dopo il riordino: commit e sigillo **separati**, come deciso |
| `GEOM-SENZA-VERSO` | **dopo**. ### **Il suo primo passo e' una decisione di Luca** *(lo specchio)* |
| `P-EQ-MEDIANA-ARCHI` | **dopo**: e' in `step`, non nella nascita |
| `POTATURA-GUARDIE` | ### **dopo**, per decisione di Luca: il riordino **tocchera' molte di quelle 57 righe** |
| `SCHW-CORTI` | ### **dopo, e SOSPESA** per priorita'. ⚠ **Ma il commit 5 tocca `dd`**: se la struttura si riordina, ### **la domanda «`dd` da `d` o da `pos`» diventa inevitabile** — e allora **si fermera' e si dira'**, non si assorbira' |

### ⛔ **E i DUE confini che NON tengono, ripetuti qui perche' contano**

| | |
|---|---|
| ### **`M2`/`U2`/`MITOSI_2LAM`** | ### **sono la parte (b)**, non una voce accanto. **Il commit 5 non si puo' scrivere senza la decisione di Luca** |
| ### **`D36`/la soglia `3π`** | ### **e' la parte (a)**. Il piano la lascia **invariata** e lo **dichiara**, ### **ma la decisione (a)-1 resta aperta e va risposta** |

---

# ✅ **Che cosa questo piano NON promette**

| | |
|---|---|
| **non promette meno codice** | promette ### **UN POSTO SOLO**. Le 549 righe possono restare 549: ### **il numero che conta e' «3 posti → 1»** |
| **non cura le 12 toppe** | ne ### **DICHIARA** cinque *(la soglia, il `0.3`, i pavimenti, `MITOSI_DIR`, `MITMAX`)* e ne **toglie** due per costruzione *(la riallocazione di `_rep`, la mutazione di `conc_nodi`)*. ### **Le altre restano, con la loro domanda** |
| ### **non toglie la finestra DENTRO una voce** | il controllo unico guarda **i confini**. ### **Dentro `mitosi` la finestra resta** — e il riordino la **riduce** *(un posto solo invece di tre)* **senza chiuderla** |
| ### **e non e' una misura** | e' un **piano**. ### **Ogni numero che contiene e' gia' stato misurato e committato**, e ogni numero che non c'e' ### **e' un criterio, non una previsione** |
