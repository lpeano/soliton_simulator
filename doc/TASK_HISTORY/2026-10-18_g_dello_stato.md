# `G` DELLO STATO — **il primo ordine era NELL'OSSERVABILE, non nello schema**

> ### ⛔⛔ **ERRORE `n.12` DEL GUARDIANO, ed e' un difetto MIO** *(`2026-10-18`)*:
> `energia_pesata.g_pesata` calcola `G` ### **coi pesi di `mot.cs`**, e
> ### **dopo `tick_con_cs` `mot.cs` e' il `cs` del CENTRO del tick appena fatto**, non
> `cs(Lambda)` dello stato di adesso. ### **`G(0)` invece usa il `cs` dello stato
> iniziale** *(`accendi_cs`)*. ### ⚠ **Quindi ogni misura dopo la prima porta uno
> scarto `O(dtau)`, e la pendenza `1` NASCE DA LI'.**

> ### ✅ **E I NUMERI DEL GUARDIANO, dal blob di `880955bb`, stessa scena e stessi
> `dtau`:** ### **`2.091`** *(schema originale, punto medio SPENTO)*,
> ### **`2.019`** *(col punto medio)*, ### **`1.002`** *(l'osservabile di oggi,
> riprodotta)*, ### **`0.044`** *(senza `CAMM-FASE-VUOTO`, con escursione `~36.7`
> COSTANTE in `dtau`)*.

> ### ⛔ **E QUESTO FILE SI COMMITTA PRIMA DEL CODICE.**

---

## 0. LA STELLA POLARE — *le cinque risposte, PRIMA del codice*

### ⛔⛔ **E PRIMA DI TUTTO: QUESTA E' LA CORREZIONE DI UN'OSSERVABILE.**
### **Il passo NON CAMBIA** -- nessuna legge, nessun ordine, nessun peso che il passo usa
-- quindi ### **l'impronta resta `2e7f795d2a52fbe7`** e ### **`M-B1` non ha niente da
dire.** ### ✅ **Cambia soltanto COME LEGGO `G`**, e ### **cio' che so.**

### **`1` — `A14`: conserva energia e carica LOCALMENTE?**

### ⛔ **UN'OSSERVABILE NON CONSERVA NIENTE: MISURA.** ### **Il passo e' quello di
prima**, quindi ### **le norme e l'energia sono quelle di prima** -- cio' che cambia e'
### **che adesso le misuro bene.**
### ⭐⭐ **E LA RISPOSTA VERA A QUESTA DOMANDA E' CAPOVOLTA:** fino a ieri avevo
scritto che ### **il passo con `cs` dinamico conserva `G` solo al PRIMO ordine.**
### **Non era vero: era la mia misura.** ### **Con l'osservabile giusta il passo e' del
SECONDO ordine** *(`2.091`)*, cioe' ### **`A14` sta MEGLIO di come l'avevo
raccontata.**

### **`2` — a quale dei TRE GRADINI arriva il risultato?**

### ✅ **GRADINO `(a)`:** pendenze su `>= 4` dimezzamenti, ### **TRE casi che DEVONO
fallire** *(l'osservabile vecchia, il pezzo togliato, il segno invertito)* e
### **un controllo positivo** che misura ### **`O(dtau)`.**
### ✅ **E GRADINO `(b)`:** con la forma `cs` ### **spenta** i pesi sono `1` e
### **l'osservabile nuova E' quella vecchia** -- cioe' ### **la correzione si puo'
togliere, e si vede dove conta.**
### ⛔ **GRADINO `(c)` NO:** nessun limite noto.

### **`3` — aggiunge un numero o una legge? Di che TIPO?**

### ✅ **NESSUNA LEGGE E NESSUN NUMERO.** `Lambda_c` c'e' gia' *(`mot.lambda_c`)*, e
### **i pesi si calcolano con la FORMA che c'e' gia'** *(`FP.cs`)*.
### ⭐ **E aggiunge UNA FUNZIONE, non una legge:** ### **`g_dello_stato`**, accanto a
`g_pesata`. ### ⚠ **E le due NON si possono fondere**, ed e' il punto: i pezzi del
passo ### **DEVONO usare i pesi del passo** *(altrimenti si cambierebbe la dinamica)*,
e ### **l'osservabile DEVE usare i pesi dello stato** *(altrimenti misura un'altra
cosa)*. ### **Due mestieri, due funzioni, e il docstring lo dice.**

### **`4` — tocca `rho`, `c_s` o il SEGNO? In quale VERSO?**

### ✅ **TOCCA `c_s`, ma SOLO DENTRO L'OSSERVABILE.** ### **La dinamica non la
sfiora:** `mot.cs` ### **resta intatto**, e ### **nessun pezzo cambia il peso che usa.**
### ⛔ **Nessun verso: non e' un accoppiamento, e' un termometro.**

### **`5` — emergente o imposto? Il fenomeno sopravvive togliendo la legge pratica?**

### ⭐⭐ **E QUI C'E' LA COSA CHE CONTA:** il *«fenomeno»* di ieri --
### **<<`G` deriva al primo ordine>>** -- ### **NON SOPRAVVIVE a una misura fatta
bene.** ### **Era un artefatto della mia osservabile**, e ### **sparisce.**
### ⛔ **E il fenomeno VERO sopravvive al suo controllo:** togliendo
`CAMM-FASE-VUOTO` la pendenza ### **crolla a `0.044`** con un'escursione
### **che non cala con `dtau`** -- cioe' ### **il secondo ordine viene DAL TERMINE**, e
non da come lo guardo.

---

## 1. RAGIONAMENTO PRELIMINARE — *che cosa ho sbagliato, e come ho fatto a non vederlo*

### ⛔⛔ **IL DIFETTO, in una riga:** `g_pesata` chiama `pesi(mot)`, che legge
### **`mot.cs`** -- e ### **`mot.cs` dopo un tick e' il `cs` DEL CENTRO di quel tick**,
non quello dello stato in cui mi trovo. ### **Quindi confrontavo `G` calcolata con pesi
di ISTANTI DIVERSI**, e la differenza e' `O(dtau)`.

### ⚠⚠ **E COME HO FATTO A NON VEDERLO: avevo GIA' trovato e curato un difetto
della STESSA FAMIGLIA** -- la ### **linea di base** di `_misura_hw` *(che calcolava `G(0)`
a forma SPENTA)*. ### **L'ho curato sulla linea di base e NON ho guardato le misure
DOPO.** ### ⛔ **Era la stessa domanda -- <<con quali pesi sto leggendo?>> -- e me la
sono fatta una volta sola.**

### ⭐ **E C'ERA UN SEGNALE CHE AVREI POTUTO LEGGERE:** il pezzo `8` del palindromo
risultava ### **ESATTO** *(`3.2e-16`)* nella tabella dell'ostacolo, e gli altri `13`
tutti ### **uguali** *(`1.15e-1`)*. ### ⚠ **Un difetto <<fisico>> non da' una
struttura cosi' pulita: quella era la firma di un CONFRONTO FRA DUE ISTANTI**, e
### **l'ho letta come una proprieta' dello schema.**

### ⛔⛔ **E DUE DIAGNOSI DA RITIRARE PER ISCRITTO** *(il punto `5` del
mandato)*: ### **<<l'ostacolo sono i pesi congelati nel pezzo>>** *(`5403638`)* e
### **<<l'ostacolo e' il peso di nodo>>** *(`2c95af13`)*. ### **Erano entrambe
artefatti della stessa osservabile sbagliata**, e ### **i referti vecchi restano, con una
nota di rimando.**

---

## 2. PROGETTAZIONE — *i passi, e i criteri FISSATI QUI*

| | il passo | cosa DECIDE | cosa mi FERMA |
|---|---|---|---|
| `1` | `g_dello_stato` in `energia_pesata`, e ### **`mot.cs` INTATTO** | l'osservabile giusta | se toccasse `mot.cs`, ### **cambierebbe il passo** -> STOP |
| `2` | il ### **CENSIMENTO CONTATO** di chi legge `mot.cs` dopo un tick | ### **quante** misure sono da correggere | -- |
| `3` | `C1` col passo di default *(punto medio SPENTO)* | se la strada `(d)` ### **regge** | `C1 < 1.9` -> commit e STOP |
| `4` | i ### **TRE casi che DEVONO fallire** e il controllo positivo | che il `2.09` ### **non sia un altro artefatto** | uno che non fallisce -> ### **FALSO-UNO**, STOP |
| `5` | `C2`, `C5`, `D3`, `C4` | che niente altro si rompa | il VERSO di `C4` -> STOP |

### ⛔ **I CRITERI, dal mandato:** ### **`C1 >= 1.9`**; ### **la `G` vecchia deve
ridare `1.002 +- 0.01`**; ### **senza `CAMM-FASE-VUOTO` pendenza `< 0.5` con
un'escursione che NON cala con `dtau`**; ### **il segno di `Omega` invertito deve
cadere**; ### **il controllo positivo: `|cs(stato) - mot.cs|` dopo un tick e'
`O(dtau)`.**
### ✅ **E `D4` si sblocca SOLO se `C1 >= 1.9` E tutti i casi che devono fallire
falliscono.** ### ⛔ **Altrimenti commit dell'osservazione e STOP.**

---

## 3. TODO DEL NEXT STEP

1. `g_dello_stato`, col docstring che distingue ### **i pesi del PASSO** dai
   ### **pesi dello STATO.**
2. Il censimento ### **contato**, e ### **tutte** le misure corrette.
3. `C1`, i tre casi che DEVONO fallire, il controllo positivo.
4. `C2`, `C5`, i quattro di `D3`, `C4`.
5. I referti ### **dal blob committato**, le ### **ritirazioni** *(referti vecchi,
   `RIPRESA`, relazione)*, la ### **mappa sez. `26`** e lo ### **STOP in coda.**