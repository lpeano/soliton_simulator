# ESITO — scan del turbo a K = 300 (Step 2 ON vs OFF). **VERDETTO: B**

> Branch `fork-su2`, 2026-09-14. Confronto con la predizione **scritta prima**
> (`doc/PREDIZIONE_step2.md`). Dati: `csv/_test_fork/_vuoto_k300_s2*_s1.vuoto.csv`,
> autocorrelazione in `csv/_test_fork/_autocorr_k300.txt`.

---

## 1. IL VERDETTO IN UNA RIGA

> **Con `cs` forzato fino al 5 % di `CS_M`, lo Step 2 NON muove lo spin.**
> I due bracci sono **indistinguibili** su tutte e tre le firme. È l'**esito B**
> della predizione, e il **sesto lato** dello stesso fatto.

---

## 2. IL DISEGNO — un solo interruttore di differenza

Entrambi i bracci, seme 1, 2000 passi, `exit = 0`, letti dal blocco `# RUN_PARAMS` dei CSV:

`--gamma-turbo 300 --cs-dinamico --fork-su2 --fork-su2-mem --campo-spinoriale
--spinore-vivo --spinore-corretto --deparam-orologio --chi-core --calore-scal --verlet`
con `--nmasse 3 --sep 8 --seed 1 --passi 2000`.

**L'unica differenza fra i due bracci è `--step2-orologio`.** Tutto il resto è identico.

> **Correzione a una nota della relazione precedente:** avevo scritto che nel braccio OFF le
> colonne `cs_*` sarebbero state `NaN`, perché `_cs_nodo_prev` è scritto solo sotto
> `FORK_SU2_MEM` **o** `STEP2_OROLOGIO`. **Entrambi i bracci hanno `--fork-su2-mem`**, quindi
> `cs_*` è popolato **in tutti e due**. La verifica-scala in-run vale per **entrambi**.

---

## 3. IL FORCING HA MORSO — molto più del previsto

Il bersaglio dichiarato era «almeno il dimezzamento di `cs` nei nodi densi». Misurato al passo 2000:

| braccio | `cs_min` | `cs_min / CS_M` | `cs_std` |
|---|---|---|---|
| Step2 **ON** | **0.0947** | **0.047** | 0.315 |
| Step2 **OFF** | **0.0643** | **0.032** | 0.324 |

Nei nodi più densi la velocità metrica è scesa al **3-5 %** di quella del vuoto. Il gradiente di
`cs` c'era, ed era **enorme** — molto oltre il forcing che ci eravamo dati come sufficiente.

Traiettoria del morso (braccio ON): `cs_min` 2.000 → 0.610 (passo 400) → 0.204 (1000) → 0.095 (2000).

---

## 4. LE TRE FIRME — piatte, e **identiche fra i bracci**

Medie su 20 campioni (passi 100…2000), angoli in gradi.

| firma | Step2 **ON** | Step2 **OFF** | nullo statistico |
|---|---|---|---|
| `chi` materia — media | **89.9865** | **89.9941** | **90.000** |
| `chi` materia — range \[min, max\] | \[89.698, 90.096\] | \[89.869, 90.137\] | — |
| `chi` materia — dispersione | 39.199 | 39.196 | **39.171** |
| `chi` **p90** (archi più densi) | **90.0309** | **89.9609** | 90.000 |
| \|⟨n⟩\| in unità di 1/√N | 0.83 (max 1.55) | 1.00 (max 1.96) | ~1 |

La differenza fra i due bracci sulla firma principale è **0.008°**, contro una dispersione di
**39.2°**. Non è piccola: è **niente**.

**Nemmeno `chi_p90` si muove** — e quelli sono esattamente gli archi dove `cs` è crollato.

### La terza firma, quella che discrimina

L'autocorrelazione spaziale `⟨n_i · n_j⟩` è l'unica che separa **domini** da **collasso globale**
da **rumore** (`doc/PREDIZIONE_kuramoto.md` §2). Su 14 bin di distanza, stato finale:

| braccio | N | \|⟨n⟩\| (atteso casuale) | vicino | lontano | calo |
|---|---|---|---|---|---|
| ON | 8865 | 0.01625 (0.0106) | −0.0200 | 0.0032 | −0.0233 |
| OFF | 8237 | 0.01152 (0.0110) | 0.0148 | 0.0014 | 0.0134 |

**Piatta a zero su tutte e 14 le distanze, in entrambi i bracci.** Nessuna scala di dominio.
Il segno del "calo" è pure **opposto** fra i due bracci: è rumore di campionamento, non struttura.

### Una cosa che NON si confronta fra i bracci

`N` finale: ON 8843, OFF 8206. **Non è una misura**: lo Step 2 cambia le fasi relative, quindi la
forza, quindi la traiettoria — e il sistema è caotico. Divergono perché sono traiettorie diverse,
non perché una produca più materia. Le firme di spin sono **intensive** apposta.

---

## 5. CONTRO LA PREDIZIONE SCRITTA PRIMA

| esito | cosa prevedeva | misurato |
|---|---|---|
| **A** — struttura | `chi` intermedio, \|⟨n⟩\| non → 1, autocorrelazione che **decade** | ✗ |
| **B** — il chiuso regge | spin *frozen-o-noise* come a Step2 OFF | **✓** |
| **C** — artefatto | effetto solo a K estremo, non estrapolabile | ✗ — non c'è **nessun** effetto da estrapolare |

> **ESITO B.**

---

## 6. PERCHÉ LO SCAN SI FERMA QUI (e non costa altre ~40 ore)

La logica asimmetrica dichiarata **prima** di partire, e approvata:

> se al forcing **massimo** le firme sono piatte, l'esito B è indicato e i K minori sono
> **superflui** — nessun effetto a K=300 ⇒ nessuno a K∈{1,30,100}.

Il forcing massimo non ha solo raggiunto il bersaglio: l'ha superato di un ordine di grandezza
(`cs/CS_M = 0.047` contro il dimezzamento richiesto). **Lo scan si chiude.**

---

## 7. IL SESTO LATO

| # | misura | esito |
|---|---|---|
| 1 | teorema di inerzia (Strato 0) | la connessione è uno **specchio** della materia — 1.57e-15 |
| 2 | frozen-o-noise | ciò che rispecchia è **rumore** |
| 3 | Kuramoto | refutato — K-frozen **byte-identico** a OFF; K-noise = NO-rumore |
| 4 | FDT | `E[n′] − n = −a²n`, **dimostrato**, verificato a 1.28e-07 |
| 5 | shake-then-freeze | `chi` deriva di **−0.33°** in 600 passi da stato casuale |
| 6 | **Step 2 con `cs` vivo** | **nessuna differenza ON/OFF a `cs/CS_M = 0.047`** |

Sei misure indipendenti, **un solo fatto**: il settore di spin **non ha** una forza organizzante
emergente, e **non ne acquisisce una** agganciando l'orologio alla metrica.

---

## 8. QUELLO CHE QUESTO **NON** DICE — i due caveat, interi

**1. Un solo seme.** `CLAUDE.md` §2.7: nessuna conclusione su un solo seme. Questo è **screening**,
legittimo come tale, **non** un fatto pubblicabile. Un secondo seme costerebbe ~1.7 ore per braccio.

**2. Il turbo ristretto è un ISOLAMENTO DIAGNOSTICO, non il regime reale.** `GAMMA` è **condiviso**
fra `cs`, `satura()` e la saturazione del campo spinoriale (`doc/REPERTO_gamma_condiviso.md`).
Restringendolo a `_cs_nodo` si **rompe di proposito** quella condivisione. Nel regime reale ad alta
densità cambierebbero **entrambi**.

> La formula onesta è: **«il gradiente di `cs`, IN ISOLAMENTO e fino al 5 % di `CS_M`, non
> retroagisce sullo spin»** — un **condizionale**, non un'affermazione sul regime naturale.

Vale in entrambe le direzioni: qui l'esito è **negativo**, e un negativo in isolamento è **più
debole**, non più forte, di un negativo nel regime vero. Non è una prova che nel regime reale non
succeda nulla; è la prova che **questo canale**, da solo, non basta.

---

## 9. COSA-RICONTROLLARE

1. `:5318` (diaglog) **re-implementa `cs` inline** e non chiama `_cs_nodo`: **sotto turbo quella
   colonna mente**. Non l'ho toccato (decisione di Luca). Le colonne `cs_*` usate qui vengono
   dall'osservatore, che legge `_cs_nodo_prev`, cioè il `cs` **vero** — non dal diaglog.
2. I `.pkl` di stato (20 MB ciascuno) **non sono committati**: restano su disco in
   `csv/_test_fork/`. L'autocorrelazione è riproducibile da lì con seed fisso `20260914`.
3. Il primo tentativo di run K=300 girò **a K=1** per il bug del guard (`cda0931`): quei dati sono
   stati **buttati**, non riciclati. I CSV qui sono del run **dopo** il fix, con la riga
   `[gamma-turbo] ... GAMMA*K = 15` verificata nel log (`_k300_s2on.log`, `_k300_s2off.log`).
