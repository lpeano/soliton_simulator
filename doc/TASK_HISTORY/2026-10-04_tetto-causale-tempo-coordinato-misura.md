# `TETTO-CAUSALE-TEMPO-COORDINATO`, **PASSO (1): LA MISURA**

*Mandato di Luca, 2026-10-04. Il simulatore **`0f060670` non si tocca**.*
**Primo lavoro di fisica dopo il riordino**, e sotto **congelamento dell'infrastruttura**:
niente presidi nuovi, niente riordini o censimenti d'igiene — ### **i difetti degli
strumenti che NON falsano questa misura si annotano e vanno in coda.**
**Scritto e committato PRIMA di girare** *(par.8)*.

---

## LA STELLA POLARE — **le cinque risposte, PRIMA del lavoro** *(`L-STELLA`)*

**① `A14` — conserva energia e carica LOCALMENTE?**
### **NON SI APPLICA A QUESTO PASSO, perche' non introduco nessuna legge: misuro.** Ma la
domanda **morde il passo (2)**, e la risposta va preparata ora:
### ⛔ **il tetto `c_s * DT` E' GIA' OGGI una violazione dell'invarianza locale**, e la voce
lo dice: *«un tetto `c_s*DT` dove `r` e' molto minore di 1 permette, IN UNITA' LOCALI,
spostamenti OLTRE la velocita' della luce locale»*. ### **Quindi la cura NON aggiunge un
vincolo: ne TOGLIE un riferimento esterno.** E `A14` chiede un bilancio **locale**: un tetto
che usa il tick **globale** e' precisamente un riferimento **non locale** dentro una legge
locale.

**② A quale dei TRE GRADINI arriva il risultato?**
### **Al gradino `(a)`, e solo a quello.** Due ragioni, entrambe limiti:
`(i)` e' un **conteggio su una traiettoria** *(un seme, una scena)*, quindi i numeri assoluti
**dipendono dalla piattaforma** — e la stella polare lo documenta *(`16/14/6/6` su Linux
contro `14/12/4/4` su Windows)*; `(ii)` ### **NON arriva al `(b)`: non tolgo nessuna legge
pratica**, e **non** al `(c)`: non c'e' un limite noto con cui confrontare un conteggio di
archi limitati. ### **Un gradino dichiarato basso e' un risultato, non una scusa.**

**③ Aggiunge un numero o una legge? Di che tipo?**
### **ZERO numeri nuovi nel simulatore: e' una misura.** Lo strumento non introduce soglie.
### 📌 **E LA DOMANDA VERA CADE SU CIO' CHE MISURO, e qui c'e' una cosa che vale la pena
scrivere prima:** il ripiego **`CS_M = 2.0`** e' un **numero a mano** — e non e' una
*costante di accoppiamento*, e' una **toppa**: sostituisce `c_s` locale quando la cache non
c'e'. ### ⚠ **E misurato: `CS_M*DT = 0.02` contro `c_sistema*DT = 0.0113137085`, cioe' il
ripiego e' quasi il DOPPIO del tetto globale.** Un ripiego piu' LARGO del tetto che
sostituisce non e' conservativo. **Lo misuro — quante volte scatta — e lo dichiaro; non lo
curo** *(punto 3 del mandato e congelamento)*.

**④ Tocca `rho`, `c_s` o il SEGNO? In quale verso dell'accoppiamento?**
### **TOCCA `c_s`, ed e' il cuore.** Il tetto e' `c_s * tempo`, e la domanda e' **quale
tempo**. ### **Il verso e' `curvatura -> EM`:** `r` *(il ritmo del tempo proprio, cioe' la
dilatazione)* decide quanto si puo' muovere `d0` *(la metrica dell'arco)*.
### ⚠ **Il verso inverso NON e' in questa misura:** non guardo se `d0` retroagisca su `r`.
### **E il SEGNO non entra:** `r >= 0` e il tetto e' simmetrico *(`clip(-p, +p)`)*.

**⑤ Emergente o imposto: sopravvive se si toglie la legge pratica?**
### **LA LEGGE PRATICA SOSPETTA HA UN NOME: `COES_CAUSALE`**, che e' **la cura parziale gia'
fatta** — prende il `c_s` del nodo **piu' lento** invece della costante di modulo.
### ⛔ **QUINDI IL FENOMENO CHE MISURO E' IN PARTE GIA' CURATO, e questo e' il fatto piu'
importante da scrivere prima:** `COES_CAUSALE` ha reso **locale la `c_s`** e ha lasciato
**coordinato il tempo**. ### **La misura deve separare i due pezzi**, altrimenti attribuisco
al tempo cio' che la `c_s` locale fa gia'. **Il modo: i contatori `_g_cct_stringe` e
`_g_cct_allarga` esistono gia' e misurano l'effetto della `c_s` locale** — il mio strumento
misura l'effetto del **tempo**, a `c_s` fissata.

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo PRIMA di guardare*

### **IL CENSIMENTO DAI SITI, FATTO DALL'AST** *(par.2: mai per riga)*

Il mandato nomina **quattro** siti. ### ⛔ **L'AST ne trova CINQUE**, e il quinto non e' un
errore del mandato: e' il **confronto `_glob`**, che il mandato chiede **a parte**.

| sito | che cos'e' | guardia *(dall'AST)* | gira col driver? |
|---|---|---|---|
| **`:9146`** | `passo_causale = c_sistema * DT` | `GRAV_BIFASE and len(proj)` | **SI** |
| **`:9202`** | lo **stesso** ricalcolato | `+ VIRIALE` | **SI** |
| **`:9203`** | ### **`clip(spinta, -p, +p)`** | `+ VIRIALE` | ### **SI — e' IL CLIP che gira** |
| **`:9209`** | `clip(grav, -p, +p)` | **`ELSE` di `VIRIALE`** | ### **NO** *(`VIRIALE = True`)* |
| **`:9340`** | `_passo_causale = _csa * DT` | `len(mask)`, `COES_ADIM`, `COES_CAUSALE` | **SI** |
| **`:9341`** | `_glob = LAM*sqrt(K_C)*DT` *(**confronto**)* | idem | **SI** |
| **`:9351`** | `_passo_causale = LAM*sqrt(K_C)*DT` | **`ELSE` di `COES_CAUSALE`** | ### **NO** |

**La configurazione del driver, letta dal CLI** *(mai a mano: `H-P3`)*:
`TAU_LOC = 1.0` · `TEMPO_SEGNO = False` · `COES_CAUSALE = True` · `COES_ADIM = True` ·
`VIRIALE = True` · `GRAV_BIFASE = True` · `CS_DINAMICO = True` · `CS_M = 2.0` ·
`LAM = 0.8` · `K_C = 2.0` · `DT = 0.01`.

> ### ✅ **E `TAU_LOC = 1.0` E' LA PRIMA COSA CHE HO VERIFICATO, perche' se fosse `0` tutto il
> ### mandato sarebbe un no-op:** `ritmo()` restituisce `None` **solo** se `TAU_LOC == 0.0`, e
> in quel caso `dt_e = DT` **esattamente** — la cura non cambierebbe un bit.
> ### **Vale `1.0`, quindi `r` e' un array e la misura ha oggetto.**

### ⛔ **LA DISTINZIONE CHE CAMBIA LA MISURA, e non era nel mandato: i due siti che girano
### hanno NATURA DIVERSA.**

| | `:9203` | `:9340` |
|---|---|---|
| cono | **GLOBALE** `LAM*sqrt(K_C)` | **LOCALE** `min(c_s[i], c_s[j])` |
| come agisce | ### **CLIP**: `spinta = clip(spinta, ±p)` | ### **SCALA**: `_delta_coes = p * _F_adim` |
| *«quanti archi LIMITA»* | **ben definito**: `|spinta| > p` | ### **NON SI APPLICA** |

**`|_F_adim| <= 1` per costruzione** *(`tanh * filtro_portata`)*, quindi al sito `:9340`
### **il tetto non limita: lo FISSA.** Cambiare `DT -> dt_e` li' **moltiplica `_delta_coes`
per `dt_e/DT` su OGNI arco**, non su quelli *«limitati»*.
### 📌 **Quindi le due domande giuste sono DUE:** per `:9203` **quanti archi cambiano stato**
*(limitato ↔ non limitato)*; per `:9340` ### **la distribuzione di `dt_e/DT`**, piu' il
conteggio di `|_F_adim| > 0.99` — che e' l'analogo di *«al tetto»* per un fattore di scala, e
### **il contatore `_g_coes_satura` lo misura GIA'.**
### ⚠ **Misurarli con la stessa domanda sarebbe un errore che produce numeri, non un errore
che si vede.**

### ⛔ **E IL FATTO STRUTTURALE CHE HO TROVATO LEGGENDO, e che decide il passo (2)**

`dt_e` nasce in **`step`**, in **entrambi** i rami dell'orologio, e si porta su `self`:
`self._dt_e_ultimo = dt_e`. **L'ordine delle voci di un passo, letto da `_passo.ordine()`:**

```
1 scuoti_vuoto   2 step   3 mitosi   4 rilassa_disegno   5 memoria_hebbiana_moto
```

> ### ⛔ **QUINDI `_dt_e_ultimo` E' DELLO STESSO PASSO -- MA FRA CHI LO SCRIVE E CHI LO
> ### LEGGEREBBE C'E' `mitosi`, CHE CREA ARCHI.**
> E `_dt_e_ultimo` e' **una delle grandezze AVVELENATE del `COMMIT 4`**, dichiarata inerte
> con la motivazione *«la legge la trova GIA' RISCRITTA (`step`)»* — ### **che e' vero per il
> `step` del passo DOPO, non per `memoria_hebbiana_moto` dello STESSO passo.**
> ### **Una cura che facesse leggere `_dt_e_ultimo` a `memoria_hebbiana_moto` leggerebbe
> `NaN` sugli archi nati in quel passo, e il veleno smetterebbe di essere inerte.**

### ✅ **E NON E' UNA CONGETTURA: e' esattamente il caso che `VELENO-ORIENTATO` ha previsto
### ieri**, col suo criterio di chiusura — *«se un giorno una voce leggesse `_sin2_vir` fra
`mitosi` e `memoria_hebbiana_moto`, l'orientamento entrerebbe nella dinamica»*.
### **Qui la voce esiste, la grandezza e' `_dt_e_ultimo`, e il passo (2) la creerebbe.**
**Lo misuro: quanti archi per passo hanno `NaN` in `_dt_e_ultimo` quando
`memoria_hebbiana_moto` gira.**

### **COSA NON SO, e non voglio indovinare**

1. ### **Se `dt_e/DT` sia tipicamente `< 1` o `> 1`.** `ritmo()` col ramo attivo
   *(`TEMPO_SEGNO = False`)* ancora alla **mediana globale** come gauge, quindi mi **aspetto
   una distribuzione centrata vicino a `1`** — ma la voce cita `r` fra **`2e-5` e `1.41`**,
   cinque ordini di grandezza. ### **Se la mediana e' `~1` e la coda scende a `1e-5`, la cura
   STRINGE su pochi archi e ALLARGA su altrettanti, e il verso NETTO non e' prevedibile dal
   segno di nulla: va contato.**
2. **Quante volte scatta il ripiego `CS_M`** *(`_g_cct_salti`)*: con `CS_DINAMICO = True` la
   cache dovrebbe esserci, ma la guardia e' `len(_csn) >= self.n` e ### **`mitosi` cambia
   `self.n` fra `step` e qui** — la stessa forma del problema di `_dt_e_ultimo`.
3. **Se `spinta` tocchi davvero il tetto a `:9203`**, e su quanti archi. ### ⚠ **Se non lo
   toccasse mai, il clip sarebbe INERTE e il sito non meriterebbe la cura** — e sarebbe un
   risultato, non una delusione.

### 📌 **E IL PRESIDIO DI LETTURA CHE MI RIGUARDA, da `FATTI_dal_codice.md`:**
*«prima di leggere una statistica riassuntiva, chiediti che valore avrebbe se non ci fosse
niente»*. ### **I valori sotto ipotesi nulla, scritti ORA:**
**`archi limitati = 0`** se il tetto e' inerte; **`archi che cambiano stato = 0`** se il tempo
proprio e' `1` ovunque; **`mediana(dt_e/DT) = 1`** se il gauge della mediana e' esatto.
### **Se misurassi `mediana ~ 1` non avrei scoperto niente: e' il valore atteso per
costruzione del gauge.** Cio' che informa e' **la CODA**, non il centro.

### ⚠ **E IL SECONDO PRESIDIO, che morde il controllo:** *«`max|A-B| = 0` puo' significare
NESSUN CONFRONTO»*. ### **Il controllo a `r = 1` DEVE dichiarare su quanti archi ha
confrontato**, altrimenti la coincidenza al bit e' vacua.

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *i passi, e cosa decide ciascuno*

| | il passo | che cosa DECIDE | che cosa mi FERMA |
|---|---|---|---|
| **1** | scena del **driver** *(`nmasse`, `sep` dall'**argv**)*, seme `11` | che sia la scena del mandato | `nmasse`/`sep` a mano: e' `H-P3`, il difetto del `6b` |
| **2** | **UNA** corsa di **150 passi**, letta a **72** e a **150** | i due orizzonti | — |
| **3** | la misura vive in una **COPIA PATCHATA** del sorgente, coi punti di registrazione **ai siti** | esattezza | se la patch non attacca: ancora non unica, `P1-quater` |
| **4** | si registra **ai siti**, non si ricostruisce | — | ### **ricostruire `spinta` fuori sarebbe una SECONDA scrittura della stessa legge** |
| **5** | `:9203`: `|spinta|` contro `p_oggi` e contro `p_cura` | **quanti archi cambiano stato, e in che VERSO** | — |
| **6** | `:9340`: distribuzione di `dt_e/DT`, e `\|_F_adim\| > 0.99` | l'effetto sul **fattore di scala** | — |
| **7** | `NaN` in `_dt_e_ultimo` sugli archi di `mask` | ### **se il passo (2) risveglierebbe il veleno** | — |
| **8** | ### **il controllo a `r = 1`, sui VALORI VERI di `c_s`** | la **validita'** | ### ⛔ **se non coincidono al bit: FERMO** |

### **PERCHE' LA PATCH SU UNA COPIA, e non un gancio**

Le alternative le ho scartate **per ragioni scritte**, non per gusto:
`(a)` il gancio `_ferma_se_registro_incoerente` da' lo stato **ai CONFINI DI VOCE**, e il
tetto vive **dentro** la funzione; `(b)` ricostruire `spinta` fuori significa **riscrivere
~60 righe di legge** — e *«una seconda scrittura della stessa legge e' due leggi che possono
divergere»* e' scritto **nel simulatore stesso**, accanto a `_dt_e_ultimo`;
`(c)` ri-chiamare `self.ritmo()` ### **HA EFFETTI COLLATERALI** *(tocca `_ritmo_chiamate`, e
puo' riscrivere `_psi_prec`)*. ### ✅ **Quindi: patch su una COPIA, `r` registrato da `step`
dove nasce, e il simulatore vero intatto.**

### **IL CONTROLLO CHE PUO' FALLIRE, e perche' NON lo faccio con `TAU_LOC = 0`**

Con `r = 1` ovunque, `dt_e = DT * 0.5 * (1 + 1) = DT * 1.0 = DT` **esattamente** *(`0.5*(1+1)`
e' `1.0` al bit, e `DT*1.0` e' `DT` al bit)*: i due tetti **devono coincidere su ogni arco**.
### ⛔ **E NON lo faccio spegnendo `TAU_LOC`**, che farebbe restituire `None` a `ritmo()` e
prendere il ramo `dt_e = DT` **scalare**: ### **coinciderebbe senza mai eseguire l'aritmetica
che sto controllando.** ### **Sarebbe un `FALSO-ZERO` del controllo.**
### ✅ **Lo faccio sui VALORI VERI di `_csa` e sul VERO numero di archi, con `r` forzato a
`1`**, cosi' il cammino `DT*0.5*(r_i+r_j)` **viene percorso**.
### ⚠ **E riporta SU QUANTI ARCHI ha confrontato** *(il presidio: `0` differenze su `0` archi
non e' un'identita')*.

## 3. TODO DEL NEXT STEP

1. lo **strumento** in `csv/_test_fork/`, con `_presidio.avvia`, la patch su una **copia**, e
   il **collaudo** *(che include il caso `r = 1` su dati sintetici, prima di spendere un run)*;
2. **la voce d'inventario nello stesso commit** *(par.6 ①)*, col blob;
3. **commit PRIMA di girare** *(par.5)*;
4. il **run**, staccato e non bufferizzato, **150 passi**;
5. il **referto**: per passo e per sito, i conteggi, le distribuzioni, il verso, la fonte di
   `dt_e`, il `NaN` del veleno, e che cosa diventerebbero **`CS_M`** e **`_glob`**;
6. ### **NIENTE CURE, e niente presidi nuovi:** congelamento dell'infrastruttura. I difetti
   degli strumenti che non falsano la misura **vanno in coda**.

### ⚠ **E UNA COSA CHE NON FARO', per non ripetere ieri:** non daro' per equivalenti
*«uguale in algebra»* e *«uguale al bit»*. ### **Ieri il conto su `fm` era giusto in algebra e
sbagliato in aritmetica di `8.9e-16`.** Qui l'affermazione *«`DT*0.5*(1+1)` e' `DT` al bit»*
e' un'affermazione **sull'aritmetica**, e il controllo la **verifica** invece di assumerla.

---

## STATO AL 2026-10-04 23:00:38

*(richiesta di stato di Luca. **Niente e' stato interrotto**: la corsa in volo non e'
stata fermata ne' rilanciata, e **nessuno dei suoi file di uscita e' stato toccato**.)*

### 1. I PROCESSI, letti DAL SISTEMA e non a memoria

**`Get-CimInstance Win32_Process -Filter "Name='python.exe'"`** e **`tasklist /v`**
*(da PowerShell: in Git Bash `/v` viene convertito in un percorso e il comando
**fallisce**)*.

| | |
|---|---|
| **PID** | **`30712`** |
| **CommandLine** | `C:\Users\lpeano\AppData\Local\Programs\Python\Python313\python.exe -u csv/_test_fork/_tetto_causale_tempo.py --passi=150` |
| **avvio** | `2026-10-04 22:54:46` |
| **trascorso** | `352 s` *(CPU `284 s`)* alle `23:00:38` |
| **file di uscita** | `<scratchpad>/run150.log` *(fuori dal repo: e' il log del processo)* |
| sessione / memoria | `Console 3` / `629 320 K` |

**Le ultime 5 righe del file di uscita** *(35 righe in tutto)*:

```
  c_sistema*DT = 0.0113137085     CS_M*DT = 0.0200000000

========================================================================================
IL RUN: 150 passi (il referto riporta anche il taglio a 72)
========================================================================================
```

### ⚠ **IL PASSO RAGGIUNTO E' UNA STIMA, NON UNA LETTURA, e il perche' e' un limite
### del MIO strumento:** non stampa nessun battito per passo *(accumula in `P` e scrive
`_corsa.txt` **solo alla fine**)*. ### **Quindi il log non dice a che passo sia, e lo
dichiaro invece di presentare una stima come una misura.**

**IL CONTO DA CUI RICAVO LA STIMA:**

| | |
|---|---|
| costruzione della scena | **`17.8 s`** *(misurato dalla sonda di fattibilita')* |
| un passo pieno **senza** i ganci | **`2.74 s`** *(misurato dalla stessa sonda)* |
| i ganci | **non misurati a parte.** `q3` chiama `np.median`, e il simulatore dichiara `0.0053 s` per una mediana su `471564` float: con ~10 chiamate per passo sono `~0.05 s`, piu' i confronti -> **stimo `+0.1 .. 0.3 s` per passo** |
| ### e gli archi **CRESCONO** | i nodi nascono, quindi ### **i passi tardi costano PIU' dei primi**: una stima lineare **sovrastima** i passi fatti |

`(352 - 17.8) / 2.9 ~ 115` · `(352 - 17.8) / 3.3 ~ 101`

> ### **PASSO STIMATO: fra `100` e `115` su `150`.**
> ### **FINE STIMATA: fra le `23:02` e le `23:04`** *(`~40` passi a `~3.2 s`)*.
> ### ⚠ **E la stima e' un intervallo perche' il termine che non ho misurato -- il
> costo dei ganci -- entra al denominatore.**

### ✅ **E UNA VERIFICA CHE CONFERMA CHE LA CORSA NON HA ANCORA SCRITTO NIENTE:** i file
di referto in `csv/_test_fork/_tetto_causale_tempo/` portano `22:51:50`, cioe' **la sonda
a 2 passi di prima**; solo `_sim_misura_tetto.py` porta `22:54:46`, ### **l'istante di
avvio della corsa, perche' lo strumento RIGENERA la copia patchata a ogni giro.**
### **Quindi il referto che e' committato ora e' della SONDA, non della corsa.**

### 2. LO STATO DEL LAVORO

| | |
|---|---|
| **mandato** | `TETTO-CAUSALE-TEMPO-COORDINATO`, **passo (1): LA MISURA** |
| **passo raggiunto** | task history committato · strumento committato **due volte** *(la seconda col controllo rifatto)* · **corsa a 150 passi IN VOLO** · referto **da scrivere** |
| **ultimo commit pushato** | **`0cfb460`** -- *IL CONTROLLO ERA UN FALSO-UNO, e l'ha trovato il guardiano* |
| **in sincronia con origin** | si' *(`## fork-su2...origin/fork-su2`, senza divergenze)* |

**`git status --short` INTERO:**

```
(vuoto)
```

### ✅ **Niente e' fatto-e-non-committato.** L'unica cosa non committata e' **cio' che la
corsa non ha ancora scritto.**

### **IL PROSSIMO PASSO, e la condizione che lo sblocca**

| | |
|---|---|
| **prossimo passo** | il **referto** della corsa, in un commit a se' *(par.5)* |
| **condizione** | ### **che la corsa finisca** *(il guardiano di sfondo `bw36s4vlz` notifica all'uscita del processo)* |

### ⛔ **E UNA CONDIZIONE CHE PUO' FERMARMI, fissata PRIMA di vedere i numeri:**
`(A)` del controllo deve trovare **zero differenze** sugli archi confrontati. Se ne trova,
**la misura su quei passi e' INVALIDA**: dichiaro **quanti** passi e **quali**, e mi fermo
### **prima di trarre conclusioni**, come il mandato prescrive.

### ⚠ **E UN ESITO POSSIBILE CHE NON E' UN FALLIMENTO, e lo scrivo ora per non
### interpretarlo dopo:** se `r == 1` su **ogni** passo, allora `(A)` e `(B)` sono
**vacui** -- `dt_e` e' costante e nessuna permutazione e' rilevabile -- e lo strumento
esce con **`FERMO`** dichiarando **due fatti distinti**: `(i)` l'allineamento **non e'
verificabile** su questa traiettoria, e `(ii)` i due tetti **coincidono** perche'
`dt_e == DT`, cioe' per **`r` degenere e non per la legge**.
### **Sono due cose, e andranno scritte entrambe.**

### 3. I MANDATI IN CODA, ricevuti e NON ancora iniziati

| | mandato | la prima riga |
|---|---|---|
| **1** | **`MEM-HEBB-VERSO`, passo (1)** | *«MANDATO: MEM-HEBB-VERSO, PASSO (1): DECISIONE REGISTRATA E MISURA. Il simulatore 0f060670 NON si tocca.»* |

### ✅ **E l'ordine non l'ho scelto io: lo dice quel mandato stesso** -- *«Se il mandato
TETTO-CAUSALE passo (1) e' in coda prima di questo, fallo prima: sono due commit
separati, in ordine»* -- e coincide con `L-UN-PROMPT`.

**Nessun altro mandato e' in attesa.** Le altre voci aperte *(`VELENO-ORIENTATO`,
`CONTA-RIGHE`, `PIATTAFORMA-NON-TIMBRATA`, `INVENTARIO-SIGILLI-SENZA-COMMIT`)* sono
**voci d'indice**, non mandati, e stanno sotto **congelamento dell'infrastruttura**.

### 4. I DEBITI DI QUESTO STRUMENTO, in coda e NON curati *(congelamento)*

1. ### **nessun battito per passo**: il log non dice a che passo sia una corsa, ed e'
   la ragione per cui il punto 1 di questo stato e' una **stima**;
2. il costo dei **ganci** non e' misurato a parte, quindi la stima ha un intervallo;
3. le **tautologiche** non classificate nella parte 2 dello strumento del *calcio*
   *(debito di ieri, non di questo)*.
