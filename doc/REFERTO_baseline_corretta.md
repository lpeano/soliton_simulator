# REFERTO — LA BASELINE DEL SISTEMA CORRETTO

> **2026-09-16.** Blob **`c57800c1`** (taglio spettrale cablato+OFF, `_xi_rumore` **non** ereditato,
> fattore **`cs^-2`** nell'inerzia), verificato sui **byte grezzi**.
> **4 run · 2 bracci x 2 semi · 500 passi · `--cs-dinamico` su tutti.**
> Osservatore sigillato **6/6 PASS** su questa versione. **MISURA F: 0 campioni falliti su 44.**
> Dati: `csv/_test_fork/_vuoto_base_{OFF,ON}_s{1,2}.vuoto.csv` · verdetto:
> `csv/_test_fork/_verdetto_baseline.txt` · script: `_verdetto_baseline.py`.
>
> ### ⚠ LA BARRA, prima dei numeri
> **Due semi per braccio: `t(0.025,1) = 12.706`, e la dev.std ha UN grado di liberta'.**
> **NESSUN IC95 qui dentro decide alcunche'.** Si legge il **segno** e l'**ordine di grandezza**.
> E' lo stesso presidio gia' scritto (`CLAUDE.md` §9): *il segno concorde su 2 semi non e' una
> prova, e' un'ipotesi da rifare con 4*.
> **CONFORMITA' P6: 4/4 PASS**, letta dai dati — blob, seme, `TAU_LUCE`, `CS_DINAMICO`, `cs_std`
> vivo, `KURAMOTO`, `STEP2`, `GAMMA_TURBO`, `SPIN_LARMOR`, `TW_SPINORE`.

---

## 1. ⚠⚠ IL RISULTATO CHE SMENTISCE IL MECCANISMO DEL MANDATO

Il mandato motivava il fattore `cs^-2` cosi': *«alla mitosi il figlio riceve un'inerzia nuova e il
padre non ne perde: `L_tot` cresce a ogni divisione»*. **I dati dicono il contrario.**

| run | passi **con** mitosi | `dL/L` con | passi **senza** | `dL/L` **senza** |
|---|---|---|---|---|
| OFF s1 | 404 | **+0.0273** | 95 | **+0.0792** |
| OFF s2 | 347 | **+0.0229** | 152 | **+0.1591** |
| ON s1 | 412 | **+0.0176** | 87 | **+0.1372** |
| ON s2 | 381 | **+0.0189** | 118 | **+0.0668** |

> ### **`L_tot` cresce DI PIU' nei passi SENZA nascite che in quelli CON nascite. Su tutti e quattro i run, da 3 a 7 volte.**
> **LA VIOLAZIONE DELLA CONSERVAZIONE NON E' GUIDATA DALLA MITOSI.**

**Il conteggio regge:** 347-412 passi con mitosi contro 87-152 senza — entrambi i gruppi hanno
campioni abbondanti, non e' una coda di pochi eventi.

**Cosa NON dico:** quale sia la causa. Il meccanismo proposto (la mitosi che non ripartisce
l'inerzia) **esiste** — `M1` del sigillo lo ha visto — ma **non e' il termine dominante**.
Attribuire la crescita a un'altra causa senza misurarla sarebbe esattamente l'errore che P1
vieta. **E' un fronte aperto, e ora ha una direzione: guardare i passi SENZA nascite.**

---

## 2. ⚠ E UN NUMERO CHE SMENTISCE LA MIA PREDIZIONE DI UN'ORA FA

In `doc/PREDIZIONE_turbo_cs2.md` ho scritto: *«`fatt_cs_frac_oltre_1pc` nella baseline vale
0.000»*. **Falso, e il valore veniva da uno smoke test a 60 passi.**

| | passo 50 | **passo 500** |
|---|---|---|
| `cs_std / cs` | `6-9e-5` | **`1.9-2.4e-3`** (= 0.19-0.24 %) |
| frazione di nodi col fattore **oltre l'1 %** | **0.0000** | **0.057 - 0.161** |
| fattore **massimo** | ~1 | **1.0174 - 1.0194** |

> **A 500 passi il 6-16 % dei nodi ha gia' il fattore `(CS_M/cs)^2` oltre l'1 %.**
> La mediana resta **1.000020**, quindi il *nodo tipico* non lo sente — **ma la coda si',
> e la coda non era nella mia stima.**

*(`cs_std/cs = 0.19-0.24 %` a 500 passi **coincide con C13**, che riportava «~0.21 % al passo 500».
Il numero non e' nuovo: era la mia citazione a essere presa dall'istante sbagliato — esattamente
il presidio §9 «una soglia su un sistema che cresce va dichiarata con l'istante in cui si misura»,
che ho scritto io e ho appena violato.)*

**Conseguenza per il turbo:** l'esperimento **non parte da zero**. La baseline ha gia' una coda
non banale, e il confronto col turbo dovra' essere **contro questi numeri**, non contro `0.000`.

---

## 3. ⚠ IL CONTRASTO `S2` NON SOPRAVVIVE ALLE CORREZIONI — e cambia SEGNO

`chi` materia, contro il nullo **90.000 +- 39.171**:

| | campagna precedente (`08784685`, **4 semi**) | **baseline corretta** (`c57800c1`, 2 semi) |
|---|---|---|
| **OFF** | **89.872** (sd 0.094) — *sotto 90* | **90.130** (90.133, 90.128) — **sopra 90** |
| **ON** | **90.049** (sd 0.034) — *sopra 90* | **89.984** (90.046, 89.921) |
| **contrasto ON - OFF** | **+0.177**, IC95 escludeva lo zero | **-0.146** |

> ### **Il contrasto ha cambiato SEGNO.** La voce `S2` — *«`--tau-luce` sposta `chi` di +0.18 gradi»* — **non si riproduce** sul sistema corretto.
> Il braccio **OFF** si e' spostato di **+0.26 gradi**, cioe' **2.7 volte** la sua dispersione fra
> semi precedente (0.094). **E' il cambiamento piu' grande prodotto dalle tre correzioni.**

**⚠ E NON DICHIARO UNA FIRMA NELL'ALTRO VERSO.** L'IC95 di OFF e' `[90.097, 90.164]` e **esclude
90** — ma **i due semi concordano a 0.004 gradi**, e con **1 grado di liberta'** una coincidenza
fra due punti produce un intervallo **spuriamente stretto**. E' il caso limite che il presidio
§9 descrive. **Serve `>= 4 semi`**, come per `S`.

**Cosa e' stabilito, e basta:** *il contrasto `+0.177` misurato sul sistema precedente **non si
riproduce** su quello corretto.* Che ci sia un contrasto opposto **non lo e'**.

---

## 4. `theta` — LE DUE CONVENZIONI, e il settore resta ALIASATO

| | OFF s1 | OFF s2 | ON s1 | ON s2 |
|---|---|---|---|---|
| `theta_COORD` giri/passo | 134.2 | 113.7 | 33.8 | 23.9 |
| **`theta_PROP`** giri/passo | **101.0** | **91.7** | **21.8** | **12.6** |
| frazione oltre il giro | 0.984 | 0.995 | 0.823 | 0.728 |
| `omega/sqrt(n)` | 1370 | 1350 | 346 | 271 |

**Gradiente di risoluzione ON/OFF: `96.4 -> 17.2` = 5.6x** (in `theta_PROP`, media fra semi).
**Ma il braccio migliore resta a ~17 giri/passo con il 78 % dei nodi oltre il giro intero:**
**il settore e' ALIASATO in entrambi i bracci**, e ogni esito negativo qui e' quello che
l'aliasing produrrebbe da solo (**C14**).

**`omega/sqrt(n)`** e' **costante entro l'1.5 %** nei due semi OFF (1370, 1350) e entro il **24 %**
nei due ON (346, 271): **nessun segnale di uscita dal regime di random walk**, che e' cio' che
quel numero serve a sorvegliare.

---

## 5. `|<n>|` e autocorrelazione — compatibili col nullo

`|<n>|` in unita' di `1/sqrt(N)`, contro il nullo **empirico** `0.9213 +- 0.3888` (**C15**):
**OFF 0.473 / 0.835 · ON 0.893 / 0.959**. **Tutti dentro.** L'isotropia regge.

---

## 6. `r` STRATIFICATO PER ETA' — c'e' una stratificazione, e ha SEGNO OPPOSTO fra i bracci

| | q1 (giovani) | q4 (maturi) | neonati |
|---|---|---|---|
| **OFF** | 0.693 / 0.944 | 1.224 / 1.070 | 0.146 / 1.093 |
| **ON** | 1.047 / 1.061 | 0.742 / 1.000 | 0.658 / 0.161 |

**Nel braccio OFF i giovani hanno `r` PIU' BASSO dei maturi; nell'ON e' rovesciato.**
E i **neonati** danno valori estremi e discordi fra semi (0.146 contro 1.093): **e' la grandezza
piu' rumorosa del lotto**, coerente con l'ipotesi che il primo `r` di un figlio confronti la
propria fase con quella **del padre** (eredita `_psi_prec`).
**Con 2 semi non si conclude nulla**, ma la misura ora **esiste**: prima non c'era.

---

## 7. IL FATTORE `(CS_M/cs)^2` — lo stato della baseline, per il confronto col turbo

| | OFF s1 | OFF s2 | ON s1 | ON s2 |
|---|---|---|---|---|
| mediano | 1.0000198 | 1.0000252 | 1.0000205 | 1.0000260 |
| massimo | 1.0194 | 1.0173 | 1.0178 | 1.0183 |
| frazione oltre l'1 % | 0.0625 | 0.1607 | 0.0570 | 0.1310 |
| `cs_std/cs` | 1.94e-3 | 2.38e-3 | 1.86e-3 | 2.36e-3 |

**Sono questi i numeri contro cui va letto il turbo**, non lo `0.000` che avevo scritto.

---

## 8. COSA QUESTA BASELINE NON DICE

1. **Non dice che `chi` si sia staccato dal casuale**: due semi non lo stabiliscono, e il presidio
   §9 e' esplicito.
2. **Non dice che lo spin si organizzi o non si organizzi**: `theta` resta **oltre il giro per
   passo** in entrambi i bracci (**C14**).
3. **Non dice cosa causi la crescita di `L_tot`**: dice solo che **non e' la mitosi**, contro il
   meccanismo che il mandato dava per assodato.
4. **Non dice nulla sul regime a densita' vera**: `cs_std/cs` resta sotto l'1 %, quindi
   `tau = d/cs` e' ancora `tau ∝ d` (**C13**).
