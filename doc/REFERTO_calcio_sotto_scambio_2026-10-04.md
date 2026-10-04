# REFERTO — **il calcio della mitosi sotto lo scambio `a<->b`, ISOLATO** *(punto 2)*

**Mandato di Luca, 2026-10-04.** *Solo misure: il simulatore `0f060670` non si tocca.*
**Task history** *(committato PRIMA, par.8, con le cinque risposte della stella polare)*:
`doc/TASK_HISTORY/2026-10-04_calcio-sotto-lo-scambio-isolato.md`, in **`8cc578b`**.
**Strumento** *(committato PRIMA di girare, par.5)*: `csv/_test_fork/_calcio_sotto_scambio.py`,
blob **`9edce46c`**.

> ### ⛔ **NON E' UN SIGILLO.** Il mandato dice *«solo misure»* e il punto 3 dice
> ### **NIENTE CURE**: cio' che segue e' **materia per la LEGGE** di
> ### `DIVISIONE-AUTOCONSISTENTE`, che viene **dopo l'energia**. **La forma della cura
> ### la decide Luca.**

---

## IL RISULTATO IN UN NUMERO

```
LO SCARTO DI phi SUI GENITORI, sotto lo scambio a<->b
                   misurato           atteso      mis - att
slot a      2.946490470e-01  2.946490470e-01      3.886e-16
slot b      2.946490470e-01  2.946490470e-01      3.886e-16
```

### ⛔ **IL CALCIO NON E' SIMMETRICO NELLO SCAMBIO, E ORA SI SA DI QUANTO.**

L'attesa **`delta_phi = KICK_TW * sciolta * chi * mod`** era scritta **nel task history**,
committato **prima** dello strumento e **prima** del run: ### **l'ordine e' verificabile
da `git`, non asserito da me.** E torna alla **precisione di macchina**.

### 📌 **E NON SCOPRE NIENTE DI NUOVO: QUANTIFICA.** Il difetto `(iii)` di
`DIVISIONE-AUTOCONSISTENTE` lo dichiarava gia' **dalla lettura del codice** —
*«il genitore `a` riceve `+chi_a` e il genitore `b` riceve `-chi_b` … e se l'arco non ha un
verso fisico dichiarato e' un'ORIENTAZIONE ARBITRARIA CHE ENTRA NELLA FISICA»*.
### **Questa misura gli mette accanto un numero.**

## LA SCOPERTA CHE VALE PIU' DEL NUMERO: **una regolarita' esatta**

> ### **Una grandezza del figlio e' SIMMETRICA sotto `a<->b` se e solo se la sua REGOLA
> ### DI NASCITA e' simmetrica nei due genitori** *(media, derivazione, zero)*.
> ### **E' ASIMMETRICA se la regola NE SCEGLIE UNO.**

E non e' un'impressione: la regola di ciascuna grandezza e' **letta dall'AST** del
simulatore *(il decoratore `_nascita_regola`)*, e messa accanto all'esito **misurato**.

| grandezza del figlio | esito | scarto max | la regola, **come il codice la dichiara** | riga |
|---|---|--:|---|--:|
| `_cs_nodo_prev` | ### **ASIMM** | `4.83690e-01` | *eredita dal genitore `a`* | 1769 |
| `_nb` | ### **ASIMM** | `1.35294e+00` | *eredita dal genitore `a`* | 1790 |
| `_nb_prec` | ### **ASIMM** | `1.35294e+00` | *eredita dal genitore `a`* | 1802 |
| `_nb_ret` | ### **ASIMM** | `1.18368e+00` | *eredita dal genitore `a`* | 1815 |
| `_psi_prec` | ### **ASIMM** | `1.00000e+00` | *eredita dal genitore `a`* | 1826 |
| `_psi_spin_prec` | ### **ASIMM** | `2.00000e+00` | *eredita dal genitore `a`* | 1839 |
| `_psi_spinor` | ### **ASIMM** | `2.00000e+00` | *eredita col SEGNO (regola D)* | 1851 |
| `_spinor_lift` | ### **ASIMM** | `2.00000e+00` | *eredita col SEGNO (regola D)* | 1864 |
| `mem_mot` | ### **ASIMM** | `1.35679e-01` | *eredita dal genitore `a`* | 1905 |
| `omega_s` | ### **ASIMM** | `1.11190e+00` | *eredita dal genitore `a`* | 1913 |
| `phi` | **simm a 1e-14** | `8.88178e-16` | *media (fase media dei genitori)* | 1734 |
| `phi0` | **simm a 1e-14** | `8.88178e-16` | *media (come `phi`)* | 1958 |
| `phi_s` | ### **ASIMM** | `7.13876e-01` | *eredita dal genitore `a`* | 1966 |
| `psi_spin` | ### **ASIMM** | `2.00000e+00` | *eredita da `a` (come `phi_s`)* | 2016 |
| `rho_spin` | ### **ASIMM** | `1.14239e+01` | *eredita da `a` (come `psi_spin`)* | 2033 |
| `eta` | **simm** | `0.00000e+00` | *zero* | 1897 |
| `perc_chi` | **simm** | `0.00000e+00` | *eredita la chiralita' del genitore `a`* | 1930 |
| `perc_geom` | **simm** | `0.00000e+00` | *DERIVATA dalla definizione (non eredita)* | 1944 |
| `perc_tw` | **simm** | `0.00000e+00` | *zero* | 1951 |
| `phivel` | **simm** | `0.00000e+00` | *media dei genitori* | 1976 |
| `pos` | **simm** | `0.00000e+00` | *media dei genitori (punto medio)* | 1984 |
| `psi` | **simm** | `0.00000e+00` | *media dei genitori (come `phi`)* | 2001 |


### 📌 **LEGGERE LA COLONNA <<esito>>: `phi` e `phi0` dichiarano *media* e NON
### smentiscono la regolarita'.** Il loro scarto e' **`8.9e-16`**, cioe'
**arrotondamento** -- e fra i due gruppi non c'e' nulla in mezzo: il piu' piccolo
scarto NON banale e' **`5.4e-02`** su `phi_s`, ### **quattordici ordini di grandezza
sopra**. *(Quindi la soglia `1e-14` non DECIDE niente: lo si vede dal salto.)*
Il caso di `fm` ha una sezione sua, qui sotto.

### ⛔ **E L'UNICA ECCEZIONE APPARENTE LA SMENTISCE IL MIO STESSO STRUMENTO: `perc_chi`.**
La sua regola dice *«eredita la chiralita' del genitore `a`»* — quindi **dovrebbe** essere
asimmetrica — e risulta **simmetrica**. ### **Perche' in questo evento
`chi_a == chi_b == 1.000`:** ereditare da `a` o da `b` da' **lo stesso valore**.

> ### 📌 **E' UN `FALSO-ZERO`, e lo strumento lo rende visibile perche' RIPORTA `chi_a` e
> ### `chi_b` arco per arco:** `1` archi su `1` hanno `chi_a == chi_b`.
> ### **Su un arco con `chi_a != chi_b`, `perc_chi` sarebbe asimmetrica anche lei** — e
> questa misura **non lo puo' dire**, perche' quell'arco qui non c'e'.

### ⚠ **E LA STESSA RISERVA VALE SULL'ASIMMETRIA DEL CALCIO:** con `chi_a == chi_b` resta
attiva **solo la prima** delle due sorgenti dichiarate nel task history — il **SEGNO**
*(`+0.5` sullo slot `a`, `-0.5` sullo slot `b`)* — e **non** la seconda, la **chiralita'
letta**. ### **Il numero `2.946490e-01` misura il SEGNO, non le due sorgenti insieme.**

## I DUE CASI IN CUI IL CONTO NON E' QUELLO CHE AVEVO PREVISTO

### ⛔ **① `fm` NON e' simmetrica al bit: lo e' a `8.9e-16`.**

| | scarto misurato |
|---|--:|
| `phi` del figlio *(cioe' `fm`)* | **`8.88178e-16`** |
| `pos` del figlio | **`0.00000e+00`** — ### **IDENTICA AL BIT** |

Il task history prevedeva `fm` **simmetrica** a `t = 0.5`, col conto: sotto lo scambio
`D -> -D`, quindi `fm' = (phi[b] + 0.5*D) % dphi`, e poiche' `phi[b] = phi[a] - D` si ha
`fm' = phi[a] - 0.5*D = fm`. ### **Il conto e' giusto in ALGEBRA e non in ARITMETICA:** le
due espressioni sono `(phi[a] - 0.5*D) % dphi` e `(phi[b] + 0.5*D) % dphi`, cioe' **due
cammini di arrotondamento diversi**.

### ✅ **E IL CONFRONTO CON `pos` LO DIMOSTRA, invece di lasciarlo supporre:** `pos` a
`t = 0.5` e' **identica al bit**, perche' `0.5*x + 0.5*y` contro `0.5*y + 0.5*x` e' **la
stessa somma** *(l'addizione IEEE-754 e' commutativa)*. Il simulatore lo dichiara gia' per
`pos` *(«identica al bit a `0.5*(x+y)`, 0 differenze su 2 000 000»)*: ### **questa misura
lo conferma e aggiunge che per `fm` NON vale.**

> ### ⚠ **E LA DISTINZIONE NON E' ACCADEMICA: un sigillo che chiedesse l'identita' AL BIT
> ### su `fm` FALLIREBBE**, e fallirebbe per arrotondamento, non per fisica.

### ⛔ **② IL VELENO DEL `COMMIT 4` SI SCAMBIA FRA I DUE ARCHI FIGLI.**

Tre grandezze riportano **scarto `0.0` con elementi diversi**, e il motivo e' che gli
elementi sono **NON FINITI**: lo scarto si calcola **solo sui finiti**, quindi non li
misura. ### **Lo strumento ora ne stampa i VALORI, e il quadro e' inequivoco:**

| evento | grandezza | `pos 0` BASE / SCAMBIO | `pos 1` BASE / SCAMBIO |
|---|---|---|---|
| divisione | `_sin2_vir` | `0.0057085209267975336` / `nan` | `nan` / `0.0057085209267975336` |
| schwinger | `_dt_e_ultimo` | `0.0062105321832223361` / `nan` | `nan` / `0.0062105321832223361` |
| schwinger | `_sin2_vir` | `0.14077152702241497` / `nan` | `nan` / `0.14077152702241497` |

### 📌 **I VALORI SONO SCAMBIATI FRA I DUE ARCHI FIGLI:** uno eredita un valore **finito**
e l'altro riceve il **veleno `NaN`**, e ### **QUALE DEI DUE dipende dall'orientamento**
`(i,j)`. ### **E' la stessa famiglia del difetto `(iii)`: un'orientazione arbitraria che
decide qualcosa.**

### ⚠ **MA NON VA SOPRAVVALUTATA, e lo dico io invece di lasciarlo scoprire:** il
simulatore **dichiara il veleno INERTE** per queste grandezze, perche'
`memoria_hebbiana_moto` riscrive `_sin2_vir` **INTERA** nello stesso passo, **dopo**
`mitosi`. ### **Quindi e' un'asimmetria della CONTABILITA', su un valore che viene
sovrascritto prima di essere letto** — non un'asimmetria della dinamica.

## LE CONDIZIONI DI VALIDITA': **soddisfatte, e non assunte**

| | divisione | schwinger |
|---|---|---|
| passo **trovato** *(atteso)* | **50** *(42)* | **60** *(70)* |
| stato del **generatore** identico | **True** | **True** |
| la **selezione** e' invariante allo scambio | **True** | **True** |
| nati BASE / SCAMBIO | **1** / **1** | **1** / **1** |
| archi nuovi: BASE / SCAMBIO / **accoppiati** / spaiati | 2 / 2 / **2** / 0 | 4 / 4 / **4** / — |
| archi nuovi **attesi** se sola divisione | **2** | — |
| ### `per_arco_valido` | ### **True** | — |
| archi sul **taglio** di `_wphi` *(`|D| = dphi/2`)* | **0** | — |

### ⛔ **E NON SONO RISULTATI: sono il PERMESSO di leggere il resto.** Se il generatore
differisse, ogni scarto sarebbe **rumore**; se le due copie dividessero archi **diversi**,
il confronto sarebbe fra **due eventi diversi**. ### **Lo strumento si ferma su entrambe.**

### ✅ **E `0 spaiati` con `2 accoppiati` su `2` attesi dice che l'accoppiamento PER
### INSIEME DEGLI ESTREMI ha funzionato** — che non e' scontato, perche' con la regola
sbagliata *(gli archi nuovi cercati **per indice**)* lo stesso confronto dava
**`0 accoppiati`**. *(Il reperto di quel giro resta:
`_misura.FALLITA.strumento-995b77a1.txt`.)*

## IL CONTEGGIO, e che cosa si tiene FUORI

| | divisione | schwinger |
|---|--:|--:|
| grandezze **confrontate** | 69 | 69 |
| **simmetriche** | 49 | 48 |
| **asimmetriche** | **18** | **21** |
| di cui **`ASIM(ATTESA)`** *(tautologiche)* | 2 | ### ⚠ **non classificate** |

### ⛔ **`i` e `j` DEGLI ARCHI NUOVI NON SONO FISICA: sono una TAUTOLOGIA DEL METODO.**
Gli archi si accoppiano **per insieme degli estremi**, e sotto lo scambio i due archi nuovi
si scambiano **ruolo e orientamento** — ### **`i` e `j` DEVONO differire.** *(E
`orientamento conservato = 0 su 2` lo conferma: entrambi invertiti.)*

### ⚠ **E UN'INCOERENZA DEL MIO REFERTO, che dichiaro invece di spendere un terzo run:**
lo strumento classifica le tautologiche **nella parte 1 e non nella parte 2**. Quindi il
**`21`** dello Schwinger **comprende `i` e `j`**, e il numero confrontabile col
**`18`** della divisione e' **`19`**. *(Voce di coda: la classificazione va portata in
`misura_schwinger`.)*

## DUE DEVIAZIONI DAI NUMERI DEL MANDATO, con la causa letta dal codice

| | il mandato | misurato |
|---|--:|--:|
| passo della **divisione** | 42 | **50** |
| passo dello **Schwinger** | 70 | **60** |

**LA CAUSA:** lo strumento avanza con `_passo.passo_pieno`, che esegue **il passo INTERO**
— **`mitosi()` compresa**. Quindi:

1. le divisioni **avvengono** mentre si avanza: al punto di misura `n` era gia' passato da
   **12802** a **12804** *(nati: mitosi **2**, schwinger **0**)*;
2. la sonda chiede *«ci sono candidati ADESSO, a passo finito?»*, cioe' **dopo** che la
   `mitosi` di quel passo ha **consumato i suoi**. ### **Il `42` dei fatti e' *dentro* il
   passo 42; il mio e' *a passo finito*. Sono due istanti diversi.**

### ⛔ **QUINDI LO STATO MISURATO NON E' *«PRIMA DELLA PRIMA DIVISIONE»*:** e' uno stato
con una divisione **pendente**, che e' l'**intenzione** del mandato.
### **Lo dichiaro invece di far passare `50` per `42`.**

## IL CONTROLLO CHE PUO' FALLIRE

| frazione | esito | che cosa ha trovato |
|---|---|---|
| **`0.4`** *(quella del mandato)* | ### ✅ **OK** | `pos` **e** `phi` asimmetriche — **lo strumento NON e' cieco** |
| `0.3` *(aggiunta da me)* | ### ⚠ **INCONCLUSO** | **nessun candidato** entro 80 passi |

### ✅ **IL CRITERIO DEL MANDATO PASSA.** A `t = 0.4` `pos` risulta asimmetrica con
**`2.82311e-01`** dove a `t = 0.5` e' **`0.0`**, e `d`/`d0` con **`4.20514e-01`** dove a
`0.5` sono **`0.0`**. ### **Il controllo e la misura si parlano: la stessa grandezza e'
simmetrica a `0.5` e asimmetrica a `0.4`, che e' esattamente la forma convessa.**

### ⛔ **E IL MIO PRIMO VERDETTO SU `0.3` ERA UN `FALSO-UNO`:** diceva **`CIECO`** dove la
verita' e' *«nessun evento da guardare»*. ### **La causa non e' un'anomalia:** il cancello
di `A13` e' `t*d >= LAM` **e** `(1-t)*d >= LAM`, quindi serve `d >= LAM/t` —
**`2.00*LAM`** a `0.5`, **`2.50*LAM`** a `0.4`, **`3.33*LAM`** a `0.3`: ### **piu' stretto
il cancello, piu' tardi il candidato**, e `MAX_PASSI = 80` era un numero che non veniva da
questo conto. **Curato con tre esiti** — `OK`, `CIECO`, **`INCONCLUSO`**.

### ⚠ **QUINDI LA PROVA DELLA VISTA POGGIA SU UN VALORE SOLO, e lo dico invece di
### presentare due controlli dove ce n'e' uno.** *(Voce di coda: rigirare `0.3` con
`--max-passi` piu' alto.)*

## LA CONFIGURAZIONE

| | |
|---|---|
| piattaforma | python **3.13.2** / numpy **2.3.0** / Windows 11 / AMD64 |
| simulatore | **`0f060670`** *(sha1 dei byte grezzi, **non toccato**)* |
| strumento | **`9edce46c`**, `tracciato=True`, `dirty=False` |
| scena | `nmasse = 3`, `sep = 6.1158` — ### **dall'ARGV**, mai scritti a mano *(`H-P3`)* |
| rete alla semina | **12802** nodi, **471564** archi |
| nomi verificati **prima** dei passi | 8 globali + 13 su `Rete` |

### ✅ **`MITOSI_DIR = 0` e `ANTIFASE_ADD = False`**, e il perche' sta nella **quinta
risposta** della stella polare: `MITOSI_DIR` e' **per costruzione asimmetrica in `a`/`b`**,
quindi con la legge pratica **accesa** un'asimmetria sarebbe **imposta**; spenta, e' nel
calcio **stesso**. E `ANTIFASE_ADD` spento esclude un ribaltamento di `fm` di mezzo dominio.

## CHE COSA QUESTO REFERTO **NON** DICE

1. ### **Non e' un sigillo** e non c'e' un verdetto: il mandato dice *«solo misure»*.
2. ### **Non dice NIENTE su che cosa fare.** Punto 3 del mandato: **niente cure**. Le
   asimmetrie vanno in `DIVISIONE-AUTOCONSISTENTE` come **materia per la legge**, che
   viene **dopo l'energia** perche' deve rispettare `A14`.
3. ### **Non separa le due sorgenti dell'asimmetria del calcio**, perche' su questo arco
   `chi_a == chi_b`: misura il **SEGNO**, non la **chiralita' letta**.
4. ### **Non vale per `FRAZ_NASCITA != 0.5`**, ne' per `MITOSI_DIR != 0`, ne' per
   `ANTIFASE_ADD = True`.
5. ### **E' UN SOLO ARCO, UN SOLO EVENTO, UN SOLO SEME.** `1` arco selezionato, `1`
   figlio. ### **Non e' una statistica: e' un'identita' algebrica verificata su un caso**,
   e il gradino e' quello dichiarato nella stella polare — **`(a)`, robusto al rumore
   numerico**, e **solo** quello.

---

**Comandi, verbatim:**

```
python -u csv/_test_fork/_calcio_sotto_scambio.py --collaudo
python -u csv/_test_fork/_calcio_sotto_scambio.py
```

**I reperti dei giri che NON sono arrivati in fondo restano**, col blob dello strumento nel
nome: `_collaudo.FALLITO.strumento-af05e86b.txt` *(il crash su `_wphi`)* e
`_misura.FALLITA.strumento-995b77a1.txt` *(il nome oscurato e gli archi nuovi per indice)*.
### **Cinque difetti di questo strumento sono stati trovati e curati in giornata, e
ciascuno ha il suo reperto.**
