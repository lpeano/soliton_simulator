# `inerzia` è un **TEMPO²** — la lettura di Luca chiude il buco dimensionale

> **Scritto per Claude web** (regola `CLAUDE.md` §5-ter). Branch `fork-su2`, 2026-09-15.
> Blob sul disco **`f5887254`** (gate §0 su `c0803713`: disallineamento voluto).
> **Nessuna modifica alla fisica.** Derivazione + lettura esaustiva del codice. Nessun run.

---

## 0. I TRE RISULTATI IN TRE RIGHE

1. **L'esponente si deriva: `inerzia ∝ cs⁻²`, cioè `omega ∝ cs²`.**
2. **Il test del verso PASSA**, e con una conferma forte: è **lo stesso esponente** dello Step 2 già
   cablato e sigillato (`omega_clk *= (cs/CS_M)²`), derivato **prima** e **indipendentemente**.
3. **Esito (b): il fattore MANCA.** Zero occorrenze di `cs` in tutto il percorso che costruisce
   `Psi`. Lo slot esiste ed è uno solo: `amp` in `calcola_psi`. **Non l'ho cablato.**

**E un costo da dichiarare:** la lettura chiude il buco alla riga 1918 ma **ne apre due altrove**
(§5). Il modello **non è dimensionalmente chiuso** in nessuna delle due letture.

---

## 1. LA LETTURA, E PERCHÉ CHIUDE ESATTAMENTE

Dal principio fondativo (`CLAUDE.md` §8): *«lo spinore È il tempo proprio della massa»*. Quindi
`Psi` — il campo d'interferenza degli spinori — porta dimensione di **tempo**, e

```
[inerzia] = [|Psi|²] = T²      =>      [correzione/inerzia] = 1/T²
```

che è **esattamente** ciò che serve perché `omega += dt_n·(correzione/inerzia − omega/tau)` produca
un `omega` con `[1/T]` e quindi un `theta = |omega|·dt_n` che è un **angolo**.

> Non è una toppa: **discende dal principio**, e chiude il buco al primo colpo, senza coefficienti.
> **La massa, in questo modello, è il modulo quadro di un tempo proprio.**

---

## 2. FASE 1.1 — QUALE tempo? **Non** quello dell'orologio: sarebbe circolare

Il modello ha due tempi propri. **L'orologio `dt_n = DT·r` è escluso dal codice stesso**, perché `r`
è **derivato da `Psi`** — `ritmo()`:

```python
a = np.angle(self.psi) - np.angle(self._psi_prec)
signed = ((a + np.pi) % (2*np.pi) - np.pi) / DT
...  r = x / np.sqrt(1.0 + x**2) + 1.0e-6
```

(e con `--campo-spinoriale` la stessa cosa su `psi_spin`). Dire `Psi ~ dt_n` sarebbe **circolare**:
`dt_n` è a valle di `Psi`, non a monte.

> Resta il tempo **metrico**, l'unico definito **indipendentemente** da `Psi`.

## 3. FASE 1.2 — Da DOVE potrebbe entrare? **Un solo slot**

```python
F = self._mat(w) @ (amp * np.exp(1j * self.phi))      # riga 2176
```

| pezzo | può portare `T`? | perché |
|---|---|---|
| `w = exp(−d/λ)·ramp·ramp` | **NO** | esponenziale di un **rapporto di lunghezze**, per rapporti di tempi |
| `e^{iφ}` | **NO** | è una fase |
| **`amp = SCALA_AMP`** | **SÌ — è l'unico** | è il **fattore di emissione per nodo**, oggi la costante `1.0` |

> **`w` non può portare `T` in nessun modo, QUALUNQUE COSA FACCIA `d`.** È l'esponenziale di un
> rapporto: è adimensionale **per costruzione**, non per il valore che assume. Argomento rigoroso,
> non una stima — e serve nel §6.

## 4. FASE 1.3 — L'ESPONENTE, derivato

Il solitone ha lunghezza d'onda `~LAM` (per costruzione del modello) e le onde viaggiano a `cs`.
Quindi il suo **periodo proprio** è una grandezza già nel sistema:

```
T_j = LAM / cs_j
```

Se l'ampiezza di emissione di un solitone **è** il suo tempo proprio (che è la lettura), allora

```
Psi_i  ~  Σ_j  w_ij · (LAM/cs_j) · e^{i φ_j}
inerzia = |Psi|²  ∝  LAM² / cs²
```

> ### **inerzia ∝ cs⁻²   ⟺   omega = coppia/inerzia ∝ cs²**

Nessun esponente scelto: viene dal fatto che il tempo proprio è `lunghezza/velocità` e che l'inerzia
è il **quadrato** di quel tempo. `LAM` e `cs` esistono già (§3, zero manopole).

## 5. FASE 1.4 — IL TEST DEL VERSO: **passa**, e non per costruzione

Con `inerzia ∝ 1/cs²`, nei pozzi densi `cs` è **piccolo** ⇒ inerzia **grande** ⇒ `omega` **piccola**
⇒ **la materia densa ruota più lentamente del vuoto.**

**È il verso giusto?** Tre riscontri concordi:

| riferimento | dice |
|---|---|
| redshift gravitazionale | un orologio nel pozzo **rallenta** |
| orologio di Compton `ω = mc²/ħ` con `c → cs` | `ω ∝ cs²` ⇒ nel pozzo **rallenta** |
| **Step 2 del modello**, già cablato e **sigillato 10/10** | `omega_clk *= (cs/CS_M)²` ⇒ nel pozzo **rallenta** |

> **La cosa che conta: è lo STESSO ESPONENTE dello Step 2**, e lo Step 2 è stato derivato e sigillato
> **prima**, senza alcun riferimento a questa lettura. Due canali **indipendenti** — la **massa**
> (qui) e l'**orologio** (Step 2) — danno entrambi `ω ∝ cs²`.
>
> Non è una coincidenza costruita: è una **consistenza trovata**. Il test del verso **passa**.

---

## 6. FASE 2 — IL CODICE CE L'HA? **No. Esito (b): manca**

Ricerca **esaustiva** di `cs` / `CS_M` / `cs_nodo` / `cs_arco` in tutto il percorso che costruisce
`Psi` e `inerzia`:

| funzione | occorrenze di `cs` |
|---|---|
| `calcola_psi` | **0** |
| `_pesi` | **0** |
| `_lam_archi` | **0** |
| `lambda_nodi` | **0** |
| `_rho_sorgente` | **0** |
| `satura` | **0** |

E `SCALA_AMP` (riga 157, assegnato a riga 4877) viene da `_fattori_coarse(SCALA_B)` = `B^0.5`: è il
fattore di **coarse-graining**, uno **scalare globale**, non un tempo e non una grandezza per nodo.

### 6.1 E la dipendenza **implicita** via `d`? Esiste, ma non può essere quella

`d` **sì** dipende da `cs`: è evolta dall'onda metrica `d'' = cs_arco²·lap(d−d0) + src − beta·vd`.
E `w = exp(−d/λ)`. Quindi **una** dipendenza implicita c'è.

> **Ma non può essere quella derivata, e non per approssimazione: per costruzione.**
> `exp(−d/λ)` è l'esponenziale di un **rapporto di lunghezze**: è adimensionale **qualunque cosa
> faccia `d`**. Non può produrre `T²`. Quindi l'esito **(c) è escluso rigorosamente**, non per stima.

### 6.2 Dove andrebbe il fattore — **e perché NON l'ho cablato**

Lo slot è uno solo: `amp` alla riga **2176**, che diventerebbe **per nodo** invece che scalare —
`amp_j = LAM/cs_j` al posto di `SCALA_AMP`. Non l'ho fatto: il mandato dice di **derivare e
leggere**, e la decisione è di Luca. Sarebbe un **pezzo**, con flag OFF e sigilli, non una patch.

> **E una cosa da sapere PRIMA di decidere:** a densità attuali `cs ≈ CS_M` (cs è "morto",
> `CLAUDE.md` §6). Quindi il fattore varrebbe **una costante**, `LAM/CS_M = 0.4`, e `inerzia`
> cambierebbe di `0.16`. **Non risolverebbe il `1e-7`** — quello resta **ETÀ** (`ramp`), come
> misurato in `doc/INERZIA_massa_o_frazione.md`. **Sono due cose separate e vanno tenute separate.**
> Per vedere l'effetto servirebbe il turbo, o densità reali.

---

## 7. IL COSTO DELLA LETTURA — due buchi nuovi, dichiarati

La lettura chiude il buco alla riga 1918. **Applicata al resto del file, ne apre due.** Va detto,
perché una lettura si giudica sulla sua consistenza **globale**, non su un punto solo.

Sotto la lettura, `Lam = mean(|psi|²) ~ T²`, quindi `sqrt(Lam) ~ T`:

| riga | cosa fa | problema |
|---|---|---|
| **1847** | `self._nb = self._nb + normal()*amp`, con `amp = sqrt(Lam)/(1+I2/Lam) ~ T` | somma un **T** a un **versore adimensionale** |
| **534** (`scuoti_vuoto`) | `ampiezza ~ T`, poi `net.phivel += calcio*ampiezza` | `phivel` è una velocità di fase, **1/T**: si somma `T` a `1/T` |

E una che la lettura **non** causa — c'era già, ed è incoerente sotto **entrambe** le letture:

| riga | cosa fa | problema |
|---|---|---|
| `lambda_nodi` | `rho_c = Ncrit/((4/3)π·LAM³)`, poi `u = rho/rho_c` | confronta `\|psi\|²` con un **conteggio per volume** |

> **Conclusione onesta: il modello non è dimensionalmente chiuso in NESSUNA delle due letture.**
> La lettura di Luca chiude **quello che conta di più** — il buco che produce i 112 giri per passo —
> ma **non è globalmente consistente com'è il codice oggi**. Non è un'obiezione alla lettura: è la
> lista di cosa andrebbe sistemato se la si adotta.

### 7.1 Un riscontro **a favore** della lettura

Sotto la lettura, `GAMMA` deve valere `1/T`. Verificato: lo è **coerentemente in tutti e tre** i suoi
usi di fisica — `satura(f) = f/(1+GAMMA|f|)`, `cs = CS_M/(1+GAMMA√I)`, e
`psi_spin = _Fs/(1+GAMMA·norm)`. **Nessuna contraddizione**, e coerente col fatto — già registrato in
`doc/REPERTO_gamma_condiviso.md` — che `GAMMA` sia **condiviso** fra quei tre punti.

---

## 8. FASE 3 — LA PISTA, REGISTRATA E NON APERTA

Se il fattore c'è (esito **b**), allora:

> **`cs` entra nel settore di spin ATTRAVERSO LA MASSA, non attraverso l'orologio.**

È un **canale mai testato**. Le sei misure riguardano lo **Step 2**, che agisce come **fase globale**
e lascia il Bloch invariante (misurato **3.3e-16**): **nessuna di esse esclude questo canale**, perché
nessuna lo ha toccato.

**Registrata, non aperta.** E con l'avvertenza del §6.2: a densità attuali sarebbe comunque **inerte**
(`cs ≈ CS_M`), quindi aprirla richiederebbe il turbo o densità alte — cioè di nuovo il ramo
diagnostico, coi suoi caveat.

---

## 9. COSA NON È STATO TOCCATO

`soliton_simulator.py` **non è stato modificato**: blob `f5887254`, `git status` pulito. **Nessun
run** è stato lanciato: questo lavoro è derivazione più lettura del sorgente. Nessun esponente
scelto, nessun fattore cablato, nessun tetto su `omega`, nessuna riparametrizzazione.

**E il `1e-7` NON è dichiarato risolto:** la lettura spiega le **dimensioni**, non il **valore
numerico**. Quello resta **ETÀ**, come misurato.
