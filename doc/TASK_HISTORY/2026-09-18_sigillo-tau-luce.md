# TASK HISTORY — **il sigillo di `--tau-luce`: TRE FAIL, TRE NATURE DIVERSE, e nessuno dice «la legge è sbagliata»**

**Data:** 2026-09-18 · **Branch** `fork-su2` · **HEAD alla scrittura** `1bcc11f`
**Blob:** `b9e07c73` *(git blob)* · **byte grezzi:** `2a7207a4` · **albero PULITO**
**Si ripara il SIGILLO, la LEGGE non si tocca.** *(Nessuna promozione, nessun default, nessuna cura di `Z9`.)*

---

## 1. RAGIONAMENTO PRELIMINARE — **§1.2: la natura del fallimento, PRIMA di toccare**

### 1.1 ⚠ **FALLISCE, NON SI SCHIANTA** — e la differenza conta

`csv/_seal_fork/_sigillo_tau_luce_RIGIRO_2026-09-17.txt`: **tutti e cinque i punti girano**, il
verdetto è **leggibile**, `exit code 0`. **Non è la modalità «più facile da non notare».**

```
ESITO: T1=FAIL   T2=FAIL   T3=FAIL   T4=PASS   T5=PASS      (rigiro 2026-09-17)
       T1=PASS   T2=FAIL   T3=FAIL   T4=FAIL   T5=PASS      (originale 2026-09-15, blob 7d484580)
```

> **⚠ E LA TABELLA VA LETTA IN DUE DIREZIONI: `T4` è passato da FAIL a PASS, `T1` da PASS a FAIL.**
> **`T4` si è RIPARATO da solo** — la cura della cache `_cs_nodo_prev` (`C7`, `43e9a47`) ha fatto
> esattamente ciò che il documento del fallimento prevedeva.

### 1.2 **T1 — il criterio è SCADUTO: confronta DUE FISICHE DIVERSE**

```
n_A = 1718   n_B = 1682   ->  NON CONFRONTABILI
```

**Il riferimento è `csv/_seal_fork/_old_sim_pre_tauluce.py`, git blob `f5887254`** *(verificato dal
disco: `sha1` del formato git = `f5887254`, raw = `4bd2e6aa`)* — **ed è COMMITTATO e PRESENTE.**

**Ma fra `f5887254` e il disco ci sono SETTE correzioni di legge sigillate** *(`cs_floor`
relazionale, `_xi_rumore`, il fattore `cs^-2`, Step 2 promosso, `d_arco`, la plasticità causale,
l'inerzia dimensionale)* **più le due cure di questa sessione.**

> **T1 asserisce: «il flag OFF è byte-identico al comportamento PRIMA della modifica».**
> **Ma esegue: «il disco di OGGI è byte-identico al codice di TRE GIORNI FA».**
> **Sono due affermazioni diverse, e la seconda è FALSA PER COSTRUZIONE.**
> **PRIMA LETTURA: il criterio è SCADUTO.**

**⚠ E NON È `Z31`:** il riferimento **esiste, è tracciato da git, e il suo blob è quello giusto.**
**Verificato anche il difetto che il mandato nomina — `pre_src = "" if not os.path.exists(PRE)` —
e in `_sigillo_tau_luce.py` NON C'È.**

### 1.3 **T2 — difetto del TEST**, e il documento lo diceva già

```
n_A = 1682   n_B = 1680   ->  NON CONFRONTABILI
```

Il monkeypatch sostituisce **`Rete._tempo_luce_nodo`**, che è il metodo **CONDIVISO**: lo chiama
**anche `_bloch_ritardato`**, e `--fork-su2-mem` è **attivo** nella config del sigillo
(`ARGS` contiene `--fork-su2-mem`). **Il test cambia DUE meccanismi invece di uno** — contro par.1.

> **PRIMA LETTURA anche qui: il criterio è sbagliato, non la legge.**
> **E il presidio ha funzionato: la riga dei conteggi, stampata PER PRIMA, ha impedito di leggere
> uno zero come identità.**

### 1.4 ⚠ **T3 — il criterio è scaduto, MA c'è un fatto che NON spiego e che non nascondo**

```
                pendenza        2026-09-15 (blob 7d484580)   2026-09-17 (rigiro)
OFF                              -0.1685                      -1.7311
ON                               -0.4265                      -1.2749
criterio: bo < bf - 0.3   ->     -0.4265 < -0.4685  FAIL      -1.2749 < -2.0311  FAIL
```

**Il criterio chiede che la pendenza ON si ALLONTANI da zero rispetto a OFF di almeno `0.3`.**

**La soglia e la DIREZIONE vengono da un'attesa (`-1.03`) calcolata quando `cs` era MORTO**
(`cs_std/cs = 0.0079 %`), cioè quando `d/cs` era di fatto `∝ d`. **Oggi `cs` è VIVO**
(`cs_std/cs = 17.6 %`, `doc/REFERTO_gauge_vuoto.md`), **e la BASELINE `OFF` si è spostata da `-0.17`
a `-1.73`: UN FATTORE 10.** **Una soglia di `0.3` tarata su una baseline di `-0.17` non significa
niente su una baseline di `-1.73`.**

> **PRIMA LETTURA: il criterio è scaduto.**
> **⚠ MA IL FATTO CHE NON SPIEGO, E CHE VA SCRITTO PRIMA DI RISCRIVERE IL CRITERIO:**
> **IL SEGNO DELL'EFFETTO SI È ROVESCIATO.** Nel 2026-09-15 `ON` era **più lontano** da zero di
> `0.258`; oggi è **più VICINO** di `0.456`. **Non ho una misura che lo spieghi, e non la invento.**
> **Riscrivere il criterio in modo che T3 passi sarebbe «aggiustare il criterio finché passa»** —
> **e il rovesciamento va riportato come RISCONTRO APERTO, separato dalla riparazione.**

### 1.5 ⚠ **LA TERZA LETTURA NON SCATTA — e la ragione è `T4`**

```
T4 (rigiro):  d -> 2d  : 2.000000  (atteso 2.000000)
              cs -> 2cs: 0.500000  (atteso 0.500000)      <- ORA SEGUE
              CONTRASTO, legge VECCHIA con d -> 2d: 1.000000  (resta ferma)
T4: PASS - tau SEGUE lo stato da solo: e' una LEGGE
```

> **`tau` segue `d` e `cs` in modo ESATTO, e la legge vecchia non segue affatto.**
> **`T4` è precisamente il test «è una LEGGE o un numero travestito?», e adesso PASSA.**
> **`T5` PASSA** (`|nb| - 1 = 2.2e-16`, zero NaN).
> **QUINDI NON MI FERMO: nessuno dei tre FAIL dice che la legge sia sbagliata.**
> **Due sono criteri scaduti, uno è un difetto del test.**

### 1.6 Il difetto `Z31` **esiste davvero, ma è ALTROVE** — verificato dal disco

```
_sigillo_inerzia.py:29   PRE = os.path.join(SC, "_pre_inerzia.py")     SC = os.environ["SCRATCH"] o HERE
_sigillo_inerzia.py:58   pre_src = open(PRE...).read() if os.path.exists(PRE) else ""   <- DEGRADA
_sigillo_calcpsi_T1.py:32  PRE = os.path.join(SC, "_pre_calcpsi.py")
_sigillo_calcpsi_T2.py:32  PRE = os.path.join(SC, "_pre_T2.py")
_sigillo_rimozione5.py:34  PRE = os.path.join(SC, "_pre_rimozione5.py")
MISURATO: NESSUNO dei quattro file `_pre_*.py` esiste, né in TMP né in csv/_seal_fork/.
```

> **I quattro riferimenti MANCANO davvero, e almeno uno DEGRADA in un confronto contro il vuoto
> invece di rifiutare.** **Ma NON è la causa del fallimento di `--tau-luce`**, che ha il suo
> riferimento committato e giusto. **Lo riporto e lo tengo SEPARATO** *(par.5-quater: non si
> mescolano due fronti)*.

---

## 2. PROGETTAZIONE — *la riparazione, e cosa decide ciascun pezzo*

### 2.1 `T1` — **si ancora alla COPPIA DI BLOB che racchiude il cambiamento**
**`T1a` STORICO:** `f5887254` (pre-cablaggio) contro **`7d484580`** (post-cablaggio, flag OFF).
**Entrambi pinnati, entrambi estratti con `git cat-file -p` IN BINARIO.** Certifica **esattamente**
ciò che T1 asserisce, ed è **riproducibile per sempre**. *(È la lezione di `c818208` rovesciata: lì
il lato NUOVO era andato alla deriva, qui è il lato NUOVO a non dover essere `HEAD`.)*
**`T1b` OGGI, e può fallire sul blob corrente:** con `TAU_LUCE = False` il ramo tau-luce **non deve
essere preso**. **Si CONTA** (P5/A8) quante volte il rilassamento tau-luce viene eseguito a flag
spento → **deve valere ZERO.**

### 2.2 `T2` — **il monkeypatch deve discriminare il CHIAMANTE**
Il wrapper resta **nel sigillo, mai nel simulatore**, e restituisce il `tau` vecchio **solo quando il
chiamante NON è `_bloch_ritardato`** *(`sys._getframe(1).f_code.co_name`)*. **E si CONTANO le due
strade**: se il conteggio verso `_bloch_ritardato` fosse zero, il discriminatore non sta funzionando
e **T2 deve fallire**, non passare.

### 2.3 `T3` — **il criterio si sostituisce, il rovesciamento si RIPORTA**
**`T3` nuovo:** il flag deve produrre un effetto **più grande del NULLO MISURATO**, dove il nullo è
la **dispersione FRA SEMI a flag INVARIATO** (par.9 `C10`: la `SE` interna è ~3 volte troppo piccola;
P3: **servono ≥ 4 semi**). **Il nullo si MISURA dentro il sigillo, non si cita da un'altra campagna.**
**Nessuna direzione prescritta**, perché la direzione veniva dall'attesa con `cs` morto.
**`T3-bis`, RIPORTATO e non giudicato:** segno e valore dello spostamento, **col fatto che si è
rovesciato dal 2026-09-15**, e **senza spiegazione inventata**.

### 2.4 ⚠ COSA MI FA FERMARE
- **`T1a` che NON dà byte-identità** → allora il cablaggio di `--tau-luce` **cambiò** il ramo OFF, e
  **quella sì è una questione di legge: mi fermo e riporto;**
- **il blob della fisica che cambia** → ho toccato il simulatore invece del sigillo: **STOP** (è `T1`
  bloccante del §1.4 del mandato);
- **`T3` nuovo che passa per un margine sottile** → **lo dico**, invece di contarlo come PASS pieno.

---

## 3. TODO DEL NEXT STEP

- [x] blob/branch dal disco · natura del fallimento diagnosticata · `Z31` verificato e SEPARATO
- [ ] **committare il FALLIMENTO com'è, PRIMA di toccarlo** (par.5)
- [ ] riparazione `T1a`/`T1b`, `T2`, `T3` + sigilli **`T1`-`T4` del §1.4** *(byte-identità della fisica BLOCCANTE)*
- [ ] **PARTE 2**: pilota per durata **e per il tasso di `eta`** → `STATO_RUN.md` → previsioni → run
- [ ] referto + registro + relazione **nello stesso commit** + **CHECKPOINT**
- [ ] **⚠ NON toccare:** la legge `--tau-luce`, `TAU_A`, `ramp`, `_pesi()`, nessun default
