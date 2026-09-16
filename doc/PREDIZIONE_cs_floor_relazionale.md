# PREDIZIONE — `cs_floor` RELAZIONALE: via `GAMMA`, entra `Lam`

> **Scritta PRIMA del cablaggio e PRIMA dei run.** 2026-09-16, branch `fork-su2`,
> blob **`a44adc31`** (coincide con `HEAD:soliton_simulator.py`, byte grezzi, 0 CRLF).
> **Categoria D — CORREZIONE DI DIFETTO: nessun flag.** Decisione di Luca.
> Numeri calcolati sui **`.pkl` gia' committati** (4 semi del braccio ON, 13 316 nodi): **nessun run
> nuovo per scrivere questa predizione.**

---

## 0. LE TRE VERIFICHE PRELIMINARI — tutte e tre hanno cambiato qualcosa del piano

### 0.1 — `lambda_vuoto` NON va chiamata. E non e' un dettaglio di stile.

`lambda_vuoto(net)` e' `float(np.mean(np.abs(net.psi[:n])**2))` — **esattamente `np.mean(I[:n])`**,
perche' il chiamante passa `I = np.abs(self.psi)**2` (`:3076`).

**Quindi niente ricorsione. Ma ci sono DUE ragioni positive per NON chiamarla:**

1. **`lambda_vuoto` puo' MUTARE lo stato.** Contiene `if len(net.psi) < net.n: net.calcola_psi()`, e
   `calcola_psi()` **scrive `self.psi`** (§9). Chiamarla dentro `_cs_nodo`, che gira **dentro
   `step`**, introdurrebbe una scrittura di stato in un punto di sola lettura.
2. **⚠ AL SECONDO PUNTO DI CHIAMATA LEGGEREBBE UN `psi` DIVERSO.** `_cs_nodo` e' chiamata **due**
   volte: `:3084` con `I` dal `psi` corrente, e **`:2943`** con
   `np.abs(_psi_ct[:n])**2` dove `_psi_ct` e' lo **SNAPSHOT `psi_t`**. `lambda_vuoto(self)` li'
   leggerebbe `self.psi`, **non lo snapshot**: la scala e il numeratore verrebbero da **due stati
   diversi**.

> **DECISIONE: `_Lam = float(np.mean(_I))` dentro la funzione, sugli STESSI dati che il chiamante ha
> passato.** E' `lambda_vuoto` per definizione, **senza** i due difetti. *(Il mandato proponeva
> `_Lam = lambda_vuoto(self)`: questa e' una correzione alla proposta, non un'aggiunta.)*

### 0.2 — ✅ IL GATE DEL §3 E' SUPERATO, e in direzione **opposta** al rischio temuto

Il mandato imponeva: *«se `I/Lam` e' concentrata su 1, la modifica non risolve, e va detto»*.
**Misurato su 19 212 nodi (6 run committati):**

| | p05 | p25 | **mediana** | p75 | p95 | frazione > 1 |
|---|---|---|---|---|---|---|
| `I/Lam` | ~0 | 0.0001 | **0.0004** | ~2.4 | **4.15** | **32 %** |

`media = 1.000000` **per costruzione**, ma la **mediana e' 0.0004**: il nodo tipico sta **2500 volte
sotto** la media. `p95/p05 = 6.3e+05`, `max/min = 1.9e+31`.

> ### **NON e' concentrata su 1. Il rischio §3 NON si materializza, ed e' MISURATO, non argomentato.**
>
> **E la ragione strutturale va scritta, perche' distingue questo caso da C12/X2:**
> il difetto del punto fisso nasce quando si normalizza sulla **MEDIANA** (`_tau/_dens_rif`,
> `ritmo()`, `ZETA_LOC`): li' il rapporto mediano vale **1 per costruzione, sempre**.
> **Qui si normalizza sulla MEDIA**, e su una distribuzione a **coda pesante** media e mediana
> **non coincidono affatto** — differiscono di **2500x**.
> **Normalizzare sulla media non e' normalizzare sulla mediana: solo la seconda ha il punto fisso.**

### 0.3 — ⚠ `R1` COME SCRITTO **NON PUO' PASSARE**. Ma ho trovato la forma che lo fa.

Il mandato chiede: con `Lam` forzato a `1/GAMMA^2 = 400`, byte-identita' `0.000e+00`.
**Verificato: due ostacoli numerici, entrambi invisibili a occhio.**

1. **`1.0/GAMMA**2` NON vale 400.** Vale `399.99999999999994316`: `0.05` non e' rappresentabile in
   binario. Il sigillo deve forzare il **letterale `400.0`**.
2. **`sqrt(I/400)` NON e' bit-identico a `0.05*sqrt(I)`**: differiscono di **1 ulp** su
   **19.8 %** degli elementi, `max|d| = 3.469e-18`. Su 150 passi il caos lo amplifica: R1 sarebbe
   **FALLITO per una ragione numerica, non fisica** — la classe di falso FAIL del §9.

**LA FORMA CHE RISOLVE, trovata per misura:**

```
sqrt(I/scala)              -> max|d| = 3.469e-18   NON identica   (4601 elementi diversi)
sqrt(I)/sqrt(scala)        -> max|d| = 3.469e-18   NON identica   (4477 elementi diversi)
sqrt(I) * sqrt(1.0/scala)  -> max|d| = 0.000e+00   ** IDENTICA **  (0 elementi diversi)
```

perche' **`np.sqrt(1.0/400.0) == 0.05` ESATTAMENTE**. **Si cabla quella forma**, e `R1` torna a
essere una byte-identita' vera invece di un criterio impossibile.

---

## 1. LA FORMA CABLATA

```python
_I  = np.maximum(I[:n], 0.0)
_Lam = float(np.mean(_I))                      # == lambda_vuoto, sugli stessi dati (§0.1)
_scala = max(_Lam, 1e-30) / (GAMMA_TURBO * GAMMA_TURBO)
cs_floor = CS_M / (1.0 + np.sqrt(_I) * np.sqrt(1.0 / _scala))
cs_floor = np.minimum(cs_floor, CS_M)          # INVARIATO
```

- **`GAMMA` sparisce da qui e SOLO da qui** (`satura()` e la saturazione spinoriale intatte).
- **Turbo:** a `GAMMA_TURBO = 1.0`, `x/(1.0*1.0) == x` **esatto** -> byte-identico alla forma senza
  turbo. Per `K > 1` la scala **scende**, quindi `cs_floor` **scende**: comportamento invariato.
- **`1e-30` e' una protezione di divisione, non un parametro**, e scatta solo se `Lam = 0`
  (sistema vuoto). **Lo dichiaro come chiede il mandato.**

---

## 2. LE PREDIZIONI, coi numeri e col falsificatore

Calcolate sui 13 316 nodi dei 4 semi ON, applicando le due formule agli **stessi** `I`.

| | `cs_floor` VECCHIA | `cs_floor` NUOVA |
|---|---|---|
| mediana | 1.999718 | **1.963194** |
| p05 | 1.967230 | **0.622761** |
| minimo | 1.950005 | **0.454161** |
| **std/media** | 0.00614 | **0.36338** |
| frazione sotto `0.99 · CS_M` | 20.6 % | **71.3 %** |

**Dispersione del floor: ×59.1.**

> ### **P1 — `cs_std/cs` DEVE SALIRE. Predico l'ORDINE DEL 10 %** (oggi **0.2216 %**).
> Stima per scalatura diretta: `0.2216 % × 59.1 = 13.1 %`. **Dichiaro l'intervallo `3 %–30 %`**,
> perche' `cs = cs_floor + (CS_M − cs_floor)·transizione` e `transizione` **non e' toccata**, quindi
> la scalatura non e' esatta.
> **FALSIFICATORE, non prorogabile: se `cs_std/cs` resta SOTTO l'1 %, la modifica NON ha
> funzionato** — l'1 % e' la soglia sotto la quale `d/cs` e' indistinguibile da `d` (C13).

> ### **P2 — la TRAIETTORIA nel tempo diventa PIATTA. E' la predizione piu' informativa.**
> Con la forma vecchia `cs_std/cs` **CRESCEVA**: `0.0086 %` al passo 50 -> `0.24 %` al passo 500,
> **20 volte in 450 passi** (C-soglia, §9), perche' `GAMMA·sqrt(I)` ha una **scala fissa** e `I`
> cresce di nove ordini mentre il campo si accende.
> **`I/Lam` e' ADIMENSIONALE e SCALE-FREE:** quando il campo si accende, `I` e `Lam` crescono
> **insieme**, e la distribuzione del rapporto resta la stessa.
> **PREDICO: `cs_std/cs` sostanzialmente PIATTA** (variazione **< ×3** fra passo 50 e passo 500),
> contro il ×20 della forma vecchia.
> **FALSIFICATORE: se cresce come prima (×10 o piu'), la scala non e' diventata relazionale.**

> ### **P3 — `theta`, `L_tot` e le firme di spin CAMBIERANNO, e il cambiamento NON sara' attribuibile.**
> `cs` vivo tocca **tre** cose insieme: `tau = d/cs` (Strato 1), l'**inerzia** (fattore `cs^-2`) e lo
> **Step 2** (`omega_clk *= (cs/CS_M)^2`). **Lo dichiaro ORA:** qualunque spostamento di `theta` o di
> `L_tot` **non e' attribuibile a uno dei tre**, e chi lo leggera' fra un mese deve saperlo.
> *(Non e' una violazione del par.1: e' UNA modifica, ma con tre canali a valle. La differenza va
> detta, non nascosta.)*

---

## 3. ⚠ L'OBIEZIONE CHE DEVO SOLLEVARE (P1), e che NON blocca il lavoro

**`Lam = np.mean(I)` su TUTTI i nodi e' una statistica GLOBALE.** Con questa modifica la velocita'
metrica locale di un nodo dipende dalla densita' media **dell'intero universo** — e §4 vieta
esplicitamente le scorciatoie non-locali. **Due giorni fa ho escluso `ZETA_LOC` (voce X2) anche per
questo.** Sarebbe disonesto non dirlo.

**Perche' nondimeno la modifica e' un MIGLIORAMENTO, e procedo:**

1. **Cio' che sostituisce e' PEGGIO sullo stesso asse.** `GAMMA` implica una densita' critica
   **`I = 400`**: una costante **universale, fissa e arbitraria**. Si passa da *«globale **e**
   arbitraria»* a *«globale **e derivata dal sistema**»*. **Su §3 e' un guadagno netto; su §4 e'
   neutro, non un peggioramento.**
2. **`Lam` e' gia' usata cosi' nel codice, due volte** (`:534`, `:1986`: `sqrt(Lam)/(1+I2/Lam)`), e
   la sua docstring la chiama *«l'analogo della costante cosmologica»*. **Una costante cosmologica e'
   globale per natura:** e' un **gauge di scala**, non un accoppiamento fra nodi.
3. **E il difetto di C12/X2 qui NON c'e'**, ed e' misurato (§0.2): quello nasce dalla **mediana**,
   non dalla media.

> **RESTA APERTO, e va nel registro:** esiste un'alternativa **strettamente locale** gia' calcolata
> **dentro la stessa funzione** — `media_vicini` (`:2601`), la media di `I` sui vicini topologici.
> `sqrt(I/media_vicini)` sarebbe relazionale **e** locale. **Non la propongo adesso** per due
> ragioni oneste: (a) sarebbe `u_nodo`, che gia' pilota `transizione`, e `cs_floor` e `transizione`
> diventerebbero funzioni **della stessa variabile** — un collasso da verificare, non da assumere;
> (b) **non l'ho misurata**, e §9 vieta di scrivere un criterio da un modello mentale.
> **E' un fronte, non una proposta.**

---

## 4. LA CONFIGURAZIONE DEI RUN — e perche' **`--tau-luce` CI VA** (integrazione di Luca)

> **DECISIONE DI LUCA, 2026-09-16: `--tau-luce` VA USATA — e ACCESA IN TUTTI E QUATTRO I RUN.**
> I quattro run sono quindi **4 SEMI di un unico braccio** (`--tau-luce` sempre ON), non un 2x2.
>
> **COSA SI GUADAGNA:** la barra **fra semi** con **4 semi** e `t(3) = 3.182`, invece dei 2 semi per
> braccio del 2x2 (dove `t(0.025,1) = 12.706` rende l'IC95 inutilizzabile — P3).
> **COSA SI PERDE, e va detto:** **non c'e' braccio di controllo interno.** L'effetto del tempo-luce
> **non e' separabile** da quello del `cs_floor` nuovo in questa campagna.
>
> **PERCHE' LA PERDITA E' MINORE DI QUANTO SEMBRI:** le due predizioni che decidono — **P1**
> (`cs_std/cs` sopra l'1 %) e **P2** (traiettoria piatta) — sono **misure ASSOLUTE con soglia
> assoluta**, non contrasti: **non hanno bisogno di un braccio OFF.** E **P3** dichiarava gia' che
> gli spostamenti di `theta` e `L_tot` **non sarebbero stati attribuibili** (tre canali a valle da
> una sola modifica). **Quindi si perde un'attribuzione che P3 aveva gia' dichiarato impossibile.**
>
> **IL CONFRONTO COL PASSATO NON VALE COME CONTROLLO:** i run precedenti sono su un **blob diverso**
> e con `--tau-luce` OFF. Si possono **citare**, non **sottrarre**.

**E non e' una ripetizione di ieri: e' la prima volta che quel braccio ha senso.** `--tau-luce`
sostituisce `_tau = TAU_A*max(dens/dens_rif, 0.05)` col **tempo-luce `d/cs`**. Finora quel braccio
**non testava il tempo-luce**, e §9 lo registra senza mezzi termini:

> *«`cs_std/cs` = 0.0086 %–0.24 %, sempre sotto l'1 %. Quindi `tau = d/cs` E' `tau ∝ d`, e tutto il
> ramo `--tau-luce` e' — in questo regime — un ramo su `tau ∝ d`: distanza contro densita', non
> tempo-luce contro densita'. E' un confronto sensato, ma NON e' quello che il nome del flag dice.»*

**Con `cs_std/cs` previsto all'ordine del 10 %** (§2, P1) **quella condizione cade**: `cs` smette di
essere quasi-costante e `d/cs` diventa **distinguibile** da `d`. §9 diceva anche **quando** sarebbe
stato testabile — *«solo con `cs` VIVO»* — e indicava come unica strada il **turbo**, che pero' e'
un **esperimento**. **Questa correzione lo rende vivo senza turbo, cioe' come FISICA.**

> **CONSEGUENZA DA SCRIVERE ORA:** se `P1` regge, **il braccio ON di questi quattro run e' il primo
> che misura davvero il tempo-luce**, e le conclusioni dei quattro bracci precedenti restano
> **valide per quel che erano** (`tau ∝ d`) ma **non sono confrontabili** con questi.

**IL MARCHIO, che resta e va detto:** il sigillo di `--tau-luce` e' **FALLITO** (`T2`/`T3`/`T4`, voce
**A** del registro, *«il collo di bottiglia del programma»*). **Il braccio ON gira su un ramo NON
CERTIFICATO**, ed e' §5 a imporre di dirlo nel documento che lo usa. **Non lo escludo** — e' la
decisione di Luca, ed e' motivata — **ma il braccio ON va letto con quel marchio sopra.** *(E se
questi run lo rendessero finalmente testabile, la voce **A** cambia natura: da «sigillo fallito» a
«sigillo da riscrivere su un regime diverso».)*

## 4-bis. UNA NOTA SUL RESTO DELLA CONFIGURAZIONE

La config chiede **`--rumore-colorato`**. **Va dichiarato**: il suo sigillo **non e' completo** —
`N2` FAIL e il sigillo si era schiantato a `N7` (voce **D** del registro). **Non lo escludo** (e' una
decisione di Luca, e il flag e' nella lista), **ma i quattro run portano il marchio**: girano con un
ramo **non certificato**, esattamente come si dichiara per `--tau-luce`. *(§5: «un run su un ramo non
certificato va detto nel documento che lo usa».)*

---

## 5. COSA QUESTA MODIFICA NON PUO' DIRE

1. **Non dice che `tau = d/cs` diventi TESTABILE.** Dice che `cs` si muove di piu'. Se `cs_std/cs`
   arriva al 10 %, `d/cs` diventa **distinguibile** da `d` — ma la distinzione va poi **misurata**,
   non dedotta da questo numero.
2. **Non tocca l'ALIASING.** `theta ~ 97.8 giri/passo` e il **99.11 %** dei nodi oltre il giro: `cs`
   piu' vivo **non risolve** il settore di spin, e nessuna predizione qui lo promette.
3. **Non dice nulla a regime:** 500 passi restano **un decimo** della maturazione.
