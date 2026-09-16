# PREDIZIONE — il ri-sigillo dello STRATO 1 con `--cs-dinamico`

> **Scritta e committata PRIMA di eseguire.** 2026-09-16, blob `08784685`, branch `fork-su2`.
> Mandato: §6.2 del TODO del 2026-09-16 — *«I 23/23 sono del blob `2277e9a0` e senza
> `--cs-dinamico`: la dipendenza da `cs` nel `tau` non e' stata esercitata per due vie (flag
> mancante E cache scartata a ogni mitosi). Rilancia con blob `08784685` e `--cs-dinamico`, resto
> identico. Passano -> marchio rimosso. Uno fallisce -> reperto.»*

---

## 0. LA CORREZIONE AL MANDATO, PRIMA DI ESEGUIRE (P1)

**«Resto identico» non e' possibile, e il mandato non poteva saperlo.** Fra il blob di riferimento
del sigillo — `968fba34`, il codice **pre-Strato 1** — e il blob attuale `08784685` ci sono **due
cure committate** che **non sono dietro `FORK_SU2_MEM`**. Una delle due **cambia la fisica del
braccio OFF per costruzione**:

| cura | dove | e' gated su MEM? | tocca S1a/S1b? |
|---|---|---|---|
| **C7** — `_cs_nodo_prev` ereditato alla mitosi | `_eredita_spinore_figli`, `:1190-1192` | la cache esiste solo sotto `CS_DINAMICO and (FORK_SU2_MEM or STEP2_OROLOGIO)` -> con MEM OFF **non esiste** | **NO**, e' un no-op esatto |
| **C11** — `_psi_spin_prec` esteso alla mitosi | `_eredita_spinore_figli`, `:1229-1231` | **NO**: gira in ogni run `--campo-spinoriale` | **SI'** |

**Percio' S1a e S1b NON POSSONO passare, e il loro fallimento NON sarebbe un reperto:**
la guardia ESATTA di `ritmo()` (`len(_psi_spin_prec) == n`) **passa nel codice NUOVO e falliva nel
VECCHIO**. Nel vecchio l'orologio a 4pi era **inerte nel 95.33 % delle chiamate** (C11); nel nuovo
e' attivo. Due orologi diversi danno due `r` diversi, quindi due `dt_n` diversi, quindi
**traiettorie diverse**. **Byte-identita' con un blob che ha un orologio diverso sarebbe una
CONTRADDIZIONE, non un successo.**

> **Questo va detto PRIMA**, perche' altrimenti domani si legge «il sigillo dello Strato 1 e'
> passato da 23/23 a N/23» e si conclude una **regressione** dove c'e' invece **una cura che ha
> fatto il suo mestiere**. E' la stessa forma dell'errore che `doc/AUDIT_misurato_vs_asserito.md`
> ha gia' trovato nel corpus: un numero letto senza la condizione che lo ha prodotto.

---

## 1. E C'E' UNA SECONDA COSA CHE IL MANDATO NON POTEVA SAPERE

**Aggiungere `--cs-dinamico` all'argv NON basta a esercitare la dipendenza da `cs`.**
Verificato dal disco: nei sigilli **in-process** (S2..S7) la cache e' impostata a mano, e vale
**`None`** oppure **`np.full(nodi, cs)`** (`:224`, `:330`). **E' COSTANTE.**

> **Un `cs` costante non esercita `tau = d/cs`: lo rende indistinguibile da `tau ∝ d`.**
> `--cs-dinamico` cambia solo i **tre run veri** (S1a, S1b, e il run con memoria che alimenta S4);
> S7, che e' il presidio piu' fine del lotto, misura la dipendenza da **`r`**, non da **`cs`**.
> **Quindi rilanciare il sigillo cosi' com'e' avrebbe lasciato il marchio esattamente dov'era.**

**Percio' e' stato aggiunto un sigillo nuovo, `S8`, che e' l'unico del lotto che fallirebbe se `cs`
fosse ignorato:** quattro nodi con **`cs = 1, 2, 4, 8`**, **tutto il resto identico** (stessa `d`,
`r = 1` su tutti — l'opposto esatto di S7, che varia `r` e tiene `cs` fisso), e si verifica che
`alpha` segua `1 - exp(-dt_n * cs / d)` **nodo per nodo**.

---

## 2. LA PREDIZIONE, numero per numero

| sigillo | previsto | perche' |
|---|---|---|
| **S1.0** | **PASS** | verifica solo il blob del file estratto |
| **S1a** *(fork ON, MEM OFF vs pre-Strato 1)* | **FAIL — ATTESO E LEGITTIMO** | C11: orologio 4pi attivo nel nuovo, inerte nel vecchio |
| **S1b** *(baseline, fork OFF)* | **FAIL — ATTESO E LEGITTIMO** | idem: C11 non e' gated nemmeno sul fork |
| **S2 / S2b** *(tau -> 0)* | **PASS** | in-process, riduzione al limite: non tocca l'orologio |
| **S3.0 / S3** *(la forza cambia)* | **PASS** | in-process su stati sintetici |
| **S4a-d** *(norme, NaN, runaway)* | **PASS** | stabilita', indipendente dall'orologio |
| **S5** *(somma coppia ~ 0)* | **PASS** | antisimmetria della coppia, algebrica |
| **S6 / S6b / S6c** *(a riposo)* | **PASS** | riduzione a riposo |
| **S7 / S7b / S7c / S7d** *(tempo proprio)* | **PASS**, con `r=2 / r=1` ancora **1.9753** | dipende da `r`, non da `cs` |
| **S8 / S8b / S8c / S8d** *(NUOVO: `tau` segue `cs`)* | **PASS** | se fallisce, `cs` e' ignorato nel ritardo: **sarebbe il reperto grosso** |
| **S3b / S3b2** *(ciclo dinamico reale)* | **PASS** | |

**Numeri attesi per S8** (`LAM` e `CS_M` dal modulo, `DT = 0.01`): `tau = LAM/cs`, e
`alpha_i = 1 - exp(-DT * cs_i / LAM)`. **Il rapporto `cs=8 / cs=1` deve essere DIVERSO da 1**;
se `cs` fosse ignorato varrebbe **esattamente 1.000000000**, come il `r=2/r=1` col bug del `DT`
nudo valeva esattamente 1.

---

## 3. COME SI LEGGE L'ESITO — deciso PRIMA

- **S8 PASSA e tutto il resto passa tranne S1a/S1b** -> **il marchio si toglie**, e si toglie per
  la ragione GIUSTA: la dipendenza da `cs` e' ora **esercitata e verificata**, non solo dichiarata.
  S1a/S1b restano FAIL **con la spiegazione scritta qui sopra**, e il sigillo va riportato come
  **«N/M PASS + 2 FAIL ATTESI»**, mai come «23/23».
- **S8 FALLISCE** -> **reperto grosso**: `tau = d/cs` non segue `cs` nemmeno quando `cs` varia.
  Si committa il fallimento e **ci si ferma** (§5).
- **Un sigillo diverso da S1a/S1b fallisce** -> **reperto**: e' una regressione vera, e va trattata
  come tale. Si committa e ci si ferma.

**E quello che l'esito NON dira' in nessun caso:** che `tau = d/cs` sia **fisicamente** distinguibile
da `tau ∝ d` nei run veri. **Non lo e'** (C13: `cs_std/cs` fra **0.0086 %** e **0.24 %**, sempre
sotto l'1 %). S8 prova che la **LEGGE e' cablata e viva**; **C13 dice che alle densita' simulabili
quella legge ha poco da dire.** Sono due affermazioni diverse e nessuna delle due sostituisce
l'altra.
