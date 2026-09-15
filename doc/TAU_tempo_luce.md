# `tau` deve essere il **TEMPO-LUCE `d/cs`**? — FASE 1, criterio scritto **PRIMA**

> **Scritto per Claude web** (regola §5-ter). Branch `fork-su2`, 2026-09-15. Blob **`f5887254`**.
> **Nessuna modifica alla fisica, nessun cablaggio.**
> **Stato: FASE 1 CONCLUSA.** I §§1-6 sono il criterio, committato **prima** dei dati (`288f601`).
> Il §7 è l'esito. **Nessun cablaggio.**

---

## 1. DA DOVE VIENE LA DOMANDA

Il tracing (`doc/TRACING_omega.md`) si è chiuso con **ESITO (I), nessun bug**: la formula d'ingresso
è giusta, ma l'esponente si perde a valle.

```
|omega|_eq = sigma * sqrt(tau/(2 dt))
sigma = coppia/inerzia   pendenza  -1.056   (2781 nodi, r = -0.981)
tau                      pendenza  +1.812
attesa per theta: -1.056 + 1.812/2 = -0.150      misurato -0.113
```

> **Il `−1` della coppia è cancellato dal `+0.91` di `√tau`.** L'aliasing nasce dall'**interazione di
> DUE leggi**, ciascuna ragionevole da sola: `omega = coppia/inerzia` (riga **1918**) e
> `tau = TAU_A·max(dens/dens_rif, 0.05)` (riga **1913**).

## 2. LE DUE RIGHE NON SONO PARI — e la seconda ha già un precedente misurato

**Riga 1918 — non si tocca.** È la meccanica rotazionale standard (`dω/dt = τ/I`), ed è
**dimensionalmente coerente** con la lettura già confermata `inerzia = T²`
(`doc/INERZIA_tempo_quadro.md`).

**Riga 1913 — sospetta, e non per gusto.** Due fatti **misurati**, non opinioni:
1. **non fa quello che dichiara.** È scritta come `tau ∝ dens`, ma misurata dà **`rho^1.81`**
   (e per via indiretta `+1.867`): due strade indipendenti, stesso scarto dall'unità;
2. **il perché è strutturale:** `dens_rif` è la **MEDIANA**, quindi per il nodo mediano
   `dens/dens_rif ≈ 1` **sempre**, a qualunque maturazione — `tau` del nodo tipico è **ancorato a
   `TAU_A` per costruzione** (`CLAUDE.md` §9, rilievo di Luca). È un **punto fisso
   auto-normalizzante**, non un transitorio.

> Una riga che **non fa quello che dichiara** è esattamente la categoria che questo repo ha già
> pagato tre volte in due giorni (riga 2196; «`omega_s` conservativo»; «il calcio alimenta ogni
> passo»).

## 3. L'INCOERENZA DA SANARE, e il candidato **imposto**

> Se `inerzia = T² = (d/cs)²`, allora **il tempo che COSTRUISCE l'inerzia e il tempo che la RILASSA
> devono essere lo stesso.** Oggi ce ne sono **due diversi nella stessa equazione**: `(d/cs)²` al
> numeratore e la **densità** nel rilassamento.

Il candidato è `tau = d/cs`, e non è scelto:

| perché | |
|---|---|
| **causalità** | è il tempo perché l'informazione attraversi la regione: un sistema **non può ricordare più a lungo di quanto impieghi a sapere di sé** |
| **è già cablato** | è il `tau` dello **Strato 1** (`_bloch_ritardato`, `_nb_ret`), messo lì **per la stessa ragione** |
| **zero manopole** | `d` e `cs` esistono già (§3) |

**E il tracer usa la STESSA formula già nel file**, non una nuova: `d_nodo` = media degli archi
incidenti con fallback a `LAM` per i nodi isolati, `cs_nodo` dalla cache `_cs_nodo_prev`. Misurare
la proposta con una formula **diversa** da quella cablata sarebbe stato incoerente col suo stesso
argomento.

---

## 4. IL CRITERIO DI LETTURA — fissato PRIMA

La pendenza di `theta` è **prevedibile senza cablare nulla**:

> **pendenza(theta) = pendenza(sigma) + pendenza(tau)/2 = −1.056 + pendenza(d/cs)/2**

| misura | lettura |
|---|---|
| **\|pendenza(d/cs)\| ≤ 0.3** | `theta` tornerebbe a **≈ −1.0**: **la cancellazione si rompe**, la sostituzione risolve il problema di scala — **e lo si sa senza cablare** |
| **pendenza(d/cs) ≈ +1.8** (come l'attuale) | **non cambia nulla**: la sostituzione resta più coerente ma **NON risolve**. Va detto così, e **non venduto come cura** |
| valori intermedi | si riporta il numero e la pendenza attesa, **senza forzare** |

## 5. IL CAVEAT DI AMPIEZZA — da riportare **comunque**, anche se il criterio è favorevole

`tau` passa da `~44` unità di tempo (≈ 4425·`DT`) a `~d/cs` (≈ 0.25). Poiché
**`|omega|_eq ∝ √tau`**, il fattore è ~`√(0.25/44)` ≈ **1/13**.

> Da **112 giri/passo** si scenderebbe a **~9**. **Un ordine di grandezza nella direzione giusta,
> NON la soluzione dell'aliasing.** Questo va scritto **nella stessa riga** in cui si dà il numero,
> non in una nota a piè di pagina.

## 7. ⚑ ESITO DELLA FASE 1 — la cancellazione **si rompe**, ma prima una correzione a me stesso

### 7.1 PRIMA DI TUTTO: la formula predittiva **non chiude**, e il numero che avevo dato ieri era fragile

Il criterio poggia su `pendenza(theta) = pendenza(sigma) + pendenza(tau)/2`. **Va verificata sul caso
attuale prima di usarla per estrapolare** — e non regge:

| | `sigma` | `tau` | attesa | misurata | **scarto** |
|---|---|---|---|---|---|
| run 400 passi, `tau` su **20 nodi** | −1.056 | **+1.812** | −0.150 | −0.113 | **0.037** |
| run 300 passi, `tau` su **2195 nodi** | −1.078 | **+1.176** | −0.490 | −0.152 | **0.338** |

> **Le due misure di `pendenza(tau)` NON coincidono: +1.812 su 20 nodi, +1.176 su 2195.**
> La seconda ha **110 volte** i campioni e `r = +0.796`: **è quella affidabile.**
>
> **Correzione a `doc/TRACING_omega.md` §6.3 e al commit `9713ddb`:** lì avevo scritto che la catena
> «si chiude» con scarto **0.037**. Quel numero usava la pendenza di `tau` misurata su **20 nodi**.
> Con la misura buona lo **scarto sale a 0.338**: **la catena NON si chiude.** Il meccanismo
> qualitativo resta (√`tau` cancella **parte** del −1), ma **il conto quantitativo no**, e resta un
> **residuo di ~0.34 nell'esponente che non so spiegare.**

Lo scrivo per primo perché è una correzione a un mio risultato di poche ore fa, ed era proprio il
numero che avevo presentato come «la catena si chiude».

> ### ⚠⚠ CORREZIONE DELLA CORREZIONE (stesso giorno, `doc/BARRE_ERRORE_pendenze.md`)
> **L'attribuzione qui sopra è SBAGLIATA.** La differenza fra `+1.812` e `+1.176` **non** è
> 20-vs-2195 nodi: è **passo 400 vs passo 300**. A parità di passo le due strade concordano
> (300: +1.176 contro +1.178, scarto **0.002**; 400: +1.812 contro +1.867, scarto **0.055**).
> **La causa vera è il TRANSITORIO:** lo scarto cala da **0.979** (passo 50) a **0.010** (passo 400),
> perché `tau ≈ 4425-6500 passi` e il run ne ha 300-400 — meno di un decimo di un rilassamento.
> **Al passo 400 la catena CHIUDE**, e **non c'è nessun residuo da spiegare.**
> La tabella e il testo sopra sono conservati com'erano: documentano come ci sono arrivato.

### 7.2 La misura che il criterio chiedeva

```
pendenza di tau_ATTUALE (TAU_A*dens/dens_rif)  = +1.176   (r = +0.796, 2195 nodi)
pendenza di tau_LUCE    (d/cs)                 = +0.097   (r = +0.351, 2195 nodi)
sigma = coppia/inerzia                         = -1.078
```

> **`d/cs` è PIATTO contro l'inerzia: +0.097.** Cade nella prima banda del criterio (`|p| ≤ 0.3`),
> **fissata prima di misurare**. Un `tau` piatto **non può cancellare niente**, qualunque sia la
> relazione precisa fra le grandezze.

### 7.3 Quanto tornerebbe `theta` — due stime, e la differenza fra loro va dichiarata

| stima | pendenza attesa di `theta` |
|---|---|
| **naive** (solo la formula) | **−1.030** |
| **corretta**, se il residuo di 0.338 resta | **−0.692** |
| **oggi, misurato** | **−0.152** |

**La stima onesta è −0.69, non −1.03.** La formula sovrastima, e non ho motivo di credere che il
residuo sparisca cambiando `tau`. Ma in **entrambe** le stime:

> ### **La cancellazione si rompe.** Da −0.15 a fra −0.69 e −1.03: un fattore **4.5-7** sull'esponente.

### 7.4 L'ampiezza — il caveat, con i numeri misurati

```
tau_attuale/DT = 6500 passi      tau_luce/DT = 66.5 passi      rapporto 0.0102
|omega|_eq ∝ sqrt(tau)  ->  fattore 0.101
theta da 4.56e4 a 4612 gradi/passo   =   da 126.7 a 12.8 GIRI per passo
```

> **Da 127 a 13 giri per passo. Un ordine di grandezza nella direzione giusta —
> e il settore resta ALIASATO** (13 giri per tick sono ancora 13 giri per tick).
> **Non è la soluzione dell'aliasing, e non va venduta come tale.**

### 7.5 Cosa resta aperto, e che questa fase NON ha risolto

1. **Il residuo di 0.338 nell'esponente**, che nessuna delle due letture di `tau` spiega. È la
   ragione per cui la stima onesta è −0.69 e non −1.03, e **andrebbe stanato** prima di fidarsi di
   qualunque predizione quantitativa su questa catena.
2. **L'aliasing resterebbe** (13 giri/passo). Sanare l'incoerenza di `tau` è un guadagno di
   **coerenza**, e un fattore 10 di ampiezza — **non una cura**.

---

## 6. COSA QUESTA FASE NON FA

Non cabla niente. Non tocca la riga 1918, né `inerzia`, né la **forma** del termine dissipativo — e
in particolare **non** apre la questione se `−omega/tau` debba invece essere un termine di
allineamento LLG `−lambda·n×(n×B)`: è **separata e aperta**, e mescolarla renderebbe inattribuibile
qualunque risultato (§1, un interruttore alla volta).

Il cablaggio (flag `TAU_LUCE`, OFF di default, sigilli T1-T4) parte **solo** dopo il via libera di
Luca e **solo** se la FASE 1 è coerente.
