# REFERTO — ESPERIMENTO `SPIN_FEEDBACK` CON `TAU_A = 2.0`

**Data:** 2026-09-17 · **Branch:** `fork-su2` · **Semi:** **1** (seed 5) · **Passi:** 120
**Driver:** `csv/_test_fork/_esperimento_spin_feedback.py` (versione **corretta**, vedi
`doc/REFERTO_driver_gira.md`) · **Output:** `csv/_test_fork/_esperimento_spin_feedback.txt`

> **`SPIN_FEEDBACK` NON HA UN SIGILLO.** È un esperimento su componente **non certificato**.
> **Nessuna promozione, nessun cablaggio, il default non cambia.**

---

## 0. LA BASE REGGE

Il riferimento a `TAU_A = 50` è stato **verificato dai dati** (`# RUN_PARAMS` di ogni CSV) e dà
**2577 nodi**, lo stesso numero dei CSV di ieri. Il `−32 %` su cui poggia questo A/B **è reale**.
Dettaglio in `doc/REFERTO_driver_gira.md` par.2.

---

## 1. `E4` — IL GATE: il feedback è davvero applicato? **SÌ.**

I contatori A8 messi apposta sulle due guardie che escono restituendo zero:

| contatore | OFF | ON |
|---|---|---|
| `_sfb_chiamate` | — | **126** |
| `_sfb_applicato` | — | **124** (98.4 %) |
| `_sfb_lift_corto` | — | 2 |
| `_sfb_mask_vuota` | — | 0 |

I 2 scatti di `_sfb_lift_corto` sono il **transitorio iniziale** (`_spinor_lift` ancora più corto
di `n`), non un fallback strutturale. **Nessuna traccia della famiglia `_psi_spin_prec`**, che fu
inerte nel 95.33 % delle chiamate per mesi.

**Ampiezza, in forma confrontabile (A3c):**

```
rapporto |feedback| / |coppia|, mediane dello STESSO passo
   MEDIO su 126 passi : 2.706      <- il numero da leggere
   MASSIMO            : 115.1      (un solo passo, non il tipico)
```

**`E4` PASSA: il contributo non è trascurabile. L'esperimento NON è nullo.**

**MA IL NUMERO VA LETTO, NON SOLO USATO COME GATE.** `2.706` non significa *«il feedback
contribuisce»*: significa che **il termine di feedback è quasi TRE VOLTE la coppia su cui
retroagisce.** Un termine chiamato *feedback* che domina il termine primario **non è una
correzione: è il motore.** Questo non invalida l'esperimento — lo qualifica, e va davanti a
qualunque lettura di `E2` ed `E3`.

---

## 2. `E1` — STABILITÀ **[BLOCCANTE]: 4/4 PASS**

| | OFF | ON |
|---|---|---|
| NaN/inf | 0 | **0** |
| `max\| \|nb\|−1 \|` | — | 2.220e-16 |
| `min d0` | — | 0.05 (> 0) |
| `_taup_cfl_max` | 0.5627 | **0.5532** (< 1) |

**Non diverge, e il vincolo causale su `tau_p` regge da entrambi i lati.**

---

## 3. `E2` — IL CONTEGGIO DEI NODI, contro il `−32 %`

```
TAU_A = 50  (riferimento)   : 2577 nodi
TAU_A = 2.0, feedback OFF   : 1754 nodi   -31.9 %
TAU_A = 2.0, feedback ON    : 1833 nodi   -28.9 %
```

**La perdita si riduce di 3.0 punti** (OFF → ON: **+79 nodi, +4.5 %**).

**QUANTO VALE QUESTO 4.5 %? — non lo so, e non lo nascondo.**

CLAUDE.md par.9 registra un nullo misurato per proprio questa grandezza: *«`N = 3164 → 3209` a 150
passi sembrava un effetto del fork: era rumore a 1e-16 amplificato dal caos»* — cioè **+1.4 % di
puro caos** sul conteggio nodi. Il **+4.5 %** qui è circa **3 volte** quel nullo, **ma**:

- quel nullo è di una **configurazione diversa** (altro regime, 150 passi, `TAU_A = 50`);
- **`SPIN_FEEDBACK` non è una perturbazione a 1e-16**: è un termine che vale 2.7 volte la coppia,
  quindi il confronto col nullo del rumore numerico **non è nemmeno quello giusto**;
- **e soprattutto: UN SOLO SEME.** P3 chiede `>= 4` semi per una barra fra semi, e su questo
  sistema *«la pendenza trasversale cambia di 0.03 a codice INVARIATO»*.

**VERDETTO SU `E2`: il segno è quello atteso, l'ampiezza NON è stabilita.** Si scrive come dice il
presidio sui risultati nulli, al rovescio: **«la perdita di nodi si riduce di 3.0 punti su un seme;
il nullo di questa differenza non è misurato»** — non «il feedback recupera il 4.5 % dei nodi».

---

## 4. `E3` — `psi`, `d0`, `ramp`

| grandezza | `TAU_A=50` | OFF | ON |
|---|---|---|---|
| `psi` max | 0.0641 | 5.834 (**×91**) | **7.206 (×112)** |
| `d0` max | 2.878 | 50.22 (**×17.5**) | **77.83 (×27)** |
| `ramp` mediana | — | 0.4704 | 0.4661 |
| `omega_s` max | — | 4.664e+04 | 3.441e+04 |
| `phivel` max | — | 63.35 | 50.66 |

**E QUESTA È LA PARTE CHE NON VA MINIMIZZATA: gli indicatori di stress PEGGIORANO con il feedback
acceso.** `psi` da ×91 a **×112**; `d0` da ×17.5 a **×27**. Sono le stesse due grandezze che ieri
avevano fatto scrivere *«"non diverge" non è "sta bene"»*, e con `SPIN_FEEDBACK` acceso **stanno
peggio, non meglio**.

`omega_s` e `phivel` invece **calano** (4.66e4 → 3.44e4; 63.4 → 50.7). Il quadro **non è
monotono**: il feedback sposta lo stress da un canale all'altro, non lo riduce.

`ramp` è **indistinguibile** fra i due bracci (0.4704 contro 0.4661): come atteso, `ramp` dipende da
`eta/TAU_A` e `TAU_A` è identico nei due bracci. **È il controllo negativo interno dell'A/B, ed è
utile che sia piatto.**

---

## 5. VERDETTO CONTRO LE QUATTRO LETTURE FISSATE PRIMA

Le quattro letture erano: *(a)* perdita si riduce **in modo netto** → ipotesi regge; *(b)* perdita
uguale → ipotesi cade, candidato Z10; *(c)* peggiora/diverge → reperto; *(d)* contributo
trascurabile → esperimento nullo.

**`(d)` è escluso** da `E4`: l'esperimento **non è nullo**.
**`(c)` è escluso** da `E1`: non diverge.
**Fra `(a)` e `(b)` NON scelgo, e la ragione è che la parola era «NETTO».**

- Sul **conteggio nodi** la direzione è quella di `(a)`, ma **su un seme e senza nullo misurato**:
  «netto» **non è dimostrato**.
- Sulle **grandezze di stress** il risultato è **contrario** ad `(a)`: `psi` e `d0` peggiorano.

**Quindi: ESITO MISTO, e lo si riporta come tale invece di sceglierne uno.** Un'ipotesi che guadagna
3 punti sul conteggio nodi mentre peggiora di 21 punti percentuali il picco di `d0` **non ha
«retto»**: ha spostato il problema.

**COSA SERVIREBBE PER DECIDERE, in ordine:**
1. **un sigillo per `SPIN_FEEDBACK`** — byte-identità a OFF, riduzione al limite, e un controllo
   positivo. Senza, si sta misurando un ramo non certificato (par.10);
2. **>= 4 semi** su `E2`, per avere una barra fra semi invece di un singolo numero (P3);
3. **`Z10`** — separare le due leggi che `TAU_A` governa. Finché `TAU_A` è **insieme** la scala del
   `ramp` e la vita media della memoria spinoriale, *«cosa ha fatto `TAU_A = 2.0`»* non ha una
   risposta unica, e questo A/B ci poggia sopra.

**NESSUNA PROMOZIONE. NESSUN CABLAGGIO. IL DEFAULT NON CAMBIA.**
