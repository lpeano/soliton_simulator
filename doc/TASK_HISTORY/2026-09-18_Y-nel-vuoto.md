# TASK HISTORY — **la Y nel VUOTO, e nella VARIAZIONE**

**Data:** 2026-09-18 · **Branch** `fork-su2` · **HEAD alla scrittura** `40e9b37`
**Blob:** `a1ae5090` — **e non cambierà. NESSUN RUN NUOVO: i sei `.pkl` esistono.**

---

## 1. RAGIONAMENTO PRELIMINARE

### 1.1 Il rilievo è giusto, e la sonda ha fatto quello che le era stato chiesto

**`Z50` ha misurato `A_m` sui nodi con `rho_spin` SOPRA soglia — il DENSO.** **Se i bracci sono
CIANO, cioè interferenza distruttiva, cioè `|psi|` BASSO, allora stavano nel complemento.**
**La sonda ha cercato la Y dove non poteva esserci.** **`Z50` resta valida per la regione densa, e
si QUALIFICA.**

### 1.2 ⚠ E la misura ② è più forte di ①, per una ragione che scrivo prima

**① guarda DOVE il campo è basso; ② guarda DOVE CRESCE.**
**Un canale di condensazione è una cosa che ACCADE, non uno stato** — e `Z49` ha già misurato che
l'accensione interna è di **cinque ordini** (`rho_spin` `3.7e-07 → 5.6e-02`).
**Se la Y è il tracciato lungo cui il campo si accende, deve comparire nella VARIAZIONE anche se
nello stato istantaneo è già annegata.**

> **② è la misura che risponde davvero, e ①/③ la incorniciano.**

### 1.3 ⚠ IL PESO SUL VUOTO — un problema che ho solo io, e va deciso prima

Su nodi **rarefatti**, pesare per `rho_spin` significa **pesare per una quantità uniformemente
minuscola**: i pesi sarebbero tutti quasi uguali e **non porterebbero informazione**.

**Scelta, dichiarata:** **per il vuoto uso `A_m` NON PESATO** — `|Σ e^{imθ}| / N`, nullo `1/√N`.
**È la forma standard, e il nullo è quello vero.**
**E come controllo riporto anche la versione pesata sul DEFICIT** `(mediana − rho_spin)`, cioè
*«quanto è vuoto»*: **se le due concordano, il risultato non dipende dalla scelta del peso.**

### 1.4 ⚠ La `Δ` va calcolata solo sui nodi PRESENTI IN ENTRAMBI

`n` va da `2391` a `8018`: i nuovi si **appendono in coda**, quindi **i primi `min(n1,n2)` indici
sono gli stessi nodi**. **Userò quelli, e dichiarerò quanti entrano nel confronto.**
*(È la stessa approssimazione già dichiarata in `K7` e in `Z46`.)*

### 1.5 ⚠ E l'ispezione visiva **non si conferma**: si mette alla prova

**«Ciano» è un colore della colormap** *(`CMAP_INTERF`: distruzione ciano ← nero → materia fuoco)*,
**e il giallo è SATURAZIONE, non un valore.** **Il fatto che tre bracci si vedano non è un dato.**
**Questa misura serve a falsificarla, e se esce piatta lo scrivo.**

### 1.6 Cosa NON so

- **se il vuoto interno abbia una struttura a tre** — non l'ha mai guardato nessuno;
- **se la variazione sia isotropa o incanalata**;
- **e non ho una predizione mia**: l'osservazione è di Luca, ed è visiva.

**⚠ Una cosa però la noto, e la scrivo prima perché non diventi una scoperta a posteriori:**
**`Z50` ha trovato `A_1` dominante nel denso** *(`0.400` contro nullo `0.120`)*. **Se `A_1`
dominasse ANCHE nel vuoto e nella variazione, allora il dipolo non è un dettaglio del denso: è la
struttura del sistema** — **e la domanda diventerebbe da dove venga un dipolo in una configurazione
a tre.** **È la terza lettura del mandato, ed è quella che mi aspetterei se dovessi scommettere —
ma non scommetto.**

---

## 2. PROGETTAZIONE

**① il VUOTO:** `A_1, A_2, A_3, A_6` sui nodi con `rho_spin < k·mediana` *(k = 1 e k = 0.1)*, **solo
regione interna** (`r < R_anello/2`, `R_anello` misurato), **NON pesato** + controllo pesato sul
deficit, **col nullo `1/√N_eff` e `N_eff` stampato.**

**② la VARIAZIONE:** `Δ = rho_spin(t2) − rho_spin(t1)` sui nodi comuni, `A_m` pesato sui `Δ > 0`,
regione interna, col nullo. **Cinque intervalli.**

**③ IL TEMPO:** `A_1` e `A_3` ai sei istanti, **denso e vuoto**, col nullo a ciascuno.

**LE LETTURE, FISSATE ADESSO** *(le quattro del mandato)*:
- **`A_3` alto sul VUOTO ai frame precoci E sulla VARIAZIONE** → **la Y esiste come struttura del
  campo rarefatto e come canale di accensione. È un risultato.**
- **`A_3` al nullo in tutte e tre le varianti** → **artefatto della colormap: l'osservazione visiva
  era sbagliata, e `Z50` resta la conclusione.**
- **`A_1` domina anche sul vuoto e sulla variazione** → **il dipolo è la struttura vera, e la domanda
  cambia.**
- **`N_eff` troppo basso** → **non si legge, e si dichiara.**

**COSA MI FA FERMARE:** nulla di tecnico. **Nessuna identificazione, e nessuna conferma dell'ispezione
visiva senza il nullo accanto.**

---

## 3. TODO DEL NEXT STEP

- [ ] **①** il vuoto · **②** la variazione · **③** l'andamento nel tempo
- [ ] **verdetto contro le quattro letture** + **`Z50` QUALIFICATA** *(«vale per la regione densa»)*
- [ ] referto + registro + relazione **nello stesso commit** + **CHECKPOINT**
- [ ] **⚠ NON toccare:** nessun run nuovo, nessuna soglia scelta, nessuna identificazione
