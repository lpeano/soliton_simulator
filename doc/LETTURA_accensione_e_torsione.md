# DUE LETTURE — **l'accensione del campo** e **la torsione letta dallo spinore**

> **Mandato di Luca, 2026-09-25. SOLA LETTURA, nessuna riga del simulatore. Poi decide Luca.**
> **Il giro di 120 passi resta sospeso.**

Strumenti: `csv/_test_fork/_lettura_tau_a.py` e `csv/_test_fork/_lettura_torsione_spinore.py`.
Referti in `csv/_test_fork/_lettura_tau_a/` e `csv/_test_fork/_lettura_torsione/`.
**Le righe sono del blob corrente; cercare per NOME, non per riga** *(par.0)*.

---

# 1. L'ACCENSIONE DEL CAMPO — `ramp = min(1, eta/TAU_A)` in `_pesi`

## (a) `TAU_A`: **due valori, tre ruoli, nessuno derivato**

### DA DOVE NASCE IL `50`

```
REGIME = "deterministico"        # <-- IL DEFAULT DEL SORGENTE  (`:115`)
if REGIME == "deterministico":
    _TAU_A_REGIME = 50.0         # alta persistenza memoria spinoriale   (`:120`)
else:
    _TAU_A_REGIME = 2.0          # canonico                              (`:125`)
TAU_A = _TAU_A_REGIME                                                    (`:408`)
```

> ### ❗ **IL `50` NON È IL CANONICO: È IL VALORE DI UN REGIME, E QUEL REGIME È IL DEFAULT.**
> Il `2.0` è marcato **«canonico»** nel sorgente stesso.

**E la provenienza è scritta nel repo, nel `help` di `--tau-a`:**
*«`TAU_A = 50` nel ramo deterministico era una **CURA** (per non far divergere `omega`) o una
scelta scaduta? … Il ramo deterministico è già vicino al limite di divergenza (il suo commento
dice: "`1e-4` e `0` divergono"), e `TAU_A` è l'altro parametro dello stesso equilibrio.»*

**Quindi il `50` è dichiarato, dal repo stesso, come un valore messo per tenere in piedi un
equilibrio numerico** — e `--tau-a` esiste **come esperimento**, marcato *«NON È UNA CORREZIONE e
NON si promuove»*.

### I RUOLI, dall'AST *(la funzione, non la riga)*

| riga | funzione | ruolo | che tipo di cosa è |
|--:|---|---|---|
| **`:3537`** | **`_pesi`** | `ramp = min(1, eta/TAU_A)` | **LA RAMPA DEI PESI DEL CAMPO** |
| **`:3334`** | `_passo_spinoriale` | `_tau = TAU_A * max(dens/dens_rif, 0.05)` | **la VITA MEDIA della memoria spinoriale** *(il rilassamento di `omega_s`)* |
| `:3337` | `_passo_spinoriale` | `_tau = TAU_A` | lo stesso, col fallback `TAU_A_LOCALE = False` |
| `:3316` | `_passo_spinoriale` | `_tq *= min(1, eta/TAU_A)` | **la STESSA rampa**, applicata alla coppia sotto `COPPIA_RECIPROCA`; il commento dice *«la STESSA riga di `_pesi()`»* |
| `:7873` | `_applica_flag` | `TAU_A = a.tau_a_over` | l'override sperimentale |
| `:10065/7` | `_applica_regime` | `TAU_A = 50.0 / 2.0` | il regime |

> ### ❗ **DUE RUOLI FISICAMENTE DIVERSI SULLO STESSO NUMERO:**
> **① la VITA MEDIA di una memoria** *(quanto a lungo `omega_s` ricorda)* e
> **② il TEMPO DI ACCENSIONE di un nodo come sorgente di campo** *(quanto ci mette a pesare)*.
> **Non c'è nessuna ragione, scritta da nessuna parte, perché debbano coincidere.**
> Il terzo (`:3316`) **non è un ruolo indipendente**: è ① riusato per coerenza, e il commento lo
> dichiara.
>
> **E il `50` è stato scelto per ①** *(«alta persistenza memoria spinoriale», «per non far
> divergere `omega`»)*. **Il ruolo ② l'ha ereditato.**

### E TUTTI I NODI NASCONO CON `eta = 0`, SENZA ECCEZIONI

```
:1550  __init__   self.eta = np.zeros(0)
:2645  semina     self.eta = concatenate([self.eta, np.zeros(n)])        <- IL VUOTO INIZIALE
:5831  mitosi     self.eta = concatenate([self.eta, np.zeros(len(sel))])
:5987  mitosi     self.eta = concatenate([self.eta, np.zeros(nc)])        <- ramo Schwinger
:4799  step       self.eta += dt_n
```

**Non esiste nel codice la distinzione fra «nodo dato» e «nodo appena creato»:** `semina` e
`mitosi` scrivono **lo stesso zero**.

---

## (b) LA PROPOSTA DI LUCA — **valutata, non scritta**

### ① I NODI DELLA SEMINA INIZIALE NASCONO MATURI

**Cosa cambierebbe:** una sola cosa, in `semina`: l'`eta` dei nodi nuovi non è `0` ma un valore
per cui `ramp = 1`.
**Chi tocca:** `semina` *(un sito)*. **`_pesi` non cambia**, e questo conta: **la legge resta
identica**, cambia la **condizione iniziale**.
**Cosa NON tocca:** `mitosi` e il ramo Schwinger restano a `0`, che è il punto della proposta.

> **A FAVORE, e non è un'opinione:** oggi l'universo **parte senza campo**. `_pesi` è
> `exp(-d/lam) * ramp[i] * ramp[j]`, quindi **il peso d'arco va come `ramp²`** — e la semina è
> **tutta** a `eta = 0`, quindi **al passo zero il peso di OGNI arco è esattamente zero**
> *(misurato: somma dei pesi `= 0.000000e+00`)*.
> **CONTRO, e va detto:** `semina` è usata **anche** durante la dinamica dalla GUI
> *(`semina_cont`, voce `H` del registro)*. Se i nodi di `semina` nascono maturi, **quel
> percorso creerebbe nodi maturi in volo.** Oggi è inerte in batch, **ma la distinzione
> «iniziale» contro «in volo» non esiste nel codice**: andrebbe introdotta, e **è l'unico pezzo
> nuovo che questa proposta richiede.**

### ② LA RAMPA RESTA SOLO PER I NATI IN DINAMICA, CON UN TEMPO **DERIVATO**

**I due candidati del mandato, misurati nella scena `(ii)` `(b)`:**

| candidato | esiste? | **forma** | valore | **passi per `ramp = 1`** |
|---|---|---|--:|--:|
| **`d/cs` d'arco** — `_tempo_luce_nodo` | **SÌ, già cablato** *(Strato 1)* | **PER NODO** | `p50 = 0.8978` | **`p05 86.6` · `p50 89.8` · `p95 92.2`** |
| **periodo dello spinore** | ingredienti sì, **il periodo NO** | — | — | **non leggibile al passo zero** |

> ### ✅ **`d/cs` È IL CANDIDATO CHE FUNZIONA, E PER TRE RAGIONI MISURATE:**
> 1. **È GIÀ CABLATO** — `_tempo_luce_nodo` è *«l'UNICO punto del file in cui questa relazione è
>    scritta»*, e la usano già lo **Strato 1** e il rilassamento sotto `--tau-luce`. **Nessuna
>    legge nuova.**
> 2. **HA LA FORMA GIUSTA.** ⚠ **E qui avevo scritto una cautela SBAGLIATA, che lascio
>    leggibile:** avevo dedotto *dalla firma* `(self, ii, jj)` che il ritorno fosse **per arco**,
>    e che servisse una riduzione arco→nodo. **Falso:** la shape misurata è **`4252` = i NODI**
>    *(gli archi sono `148 237`)*. Gli indici servono a **costruire** `d_nodo`; **il ritorno è per
>    nodo**, cioè **esattamente la forma di `ramp`**. *(Dedotto dalla firma invece che dal dato:
>    `P1` applicato a me stesso.)*
> 3. **È STRETTO:** `p05 86.6` → `p95 92.2` passi, cioè **±3 %**. Non è un numero che varia di
>    ordini di grandezza da nodo a nodo, quindi **non introduce una nuova dispersione.**
>
> **`89.8` passi contro `5000`: più rapido di un fattore `55.7`.**

**IL CANDIDATO 2 NON È DISPONIBILE, e la ragione è strutturale:** `omega_clk` **non esiste come
attributo prima del primo passo**. Un tempo di rampa che serve **alla nascita** non può venire da
una grandezza che **nasce dopo**. *(E `ritmo()` al passo zero vale `1` esatto su tutti i nodi —
`p05 = p50 = p95 = 1` — che è il punto fisso della normalizzazione sulla mediana, `C12`: su quello
non si misura nulla.)*

**⚠ E UNA COSA CHE LA PROPOSTA NON RISOLVE, e va detta:** `d/cs` **cambia con la maturazione**. Un
nodo nato al passo `1000` avrebbe una rampa diversa da uno nato al passo `10`. **È coerente con una
legge locale** *(è il punto della proposta)*, **ma significa che la rampa non è più una costante del
sistema**, e ogni confronto fra istanti va fatto con questo in mente.

---

## (c) LA CONSEGUENZA — **tutti i giri da 120 passi hanno girato con il campo SPENTO**

```
ramp(k) = k*DT/TAU_A = k/5000                (con r ~ 1)
   passo    1   ramp = 0.000200      peso d'arco ~ ramp^2 = 4.0e-08
   passo    8   ramp = 0.001600                             2.6e-06
   passo   30   ramp = 0.006000                             3.6e-05
   passo   60   ramp = 0.012000                             1.4e-04
   passo  120   ramp = 0.024000                             5.76e-04
   passo 1230   ramp = 0.246000                             6.05e-02
   passo 5000   ramp = 1.000000                             1.00
```

> ### ⛔ **`ramp` ENTRA COME `ramp[i]*ramp[j]`: IL PESO D'ARCO VA COME `ramp²`.**
> **Al passo `120` il peso di un arco è `5.76e-04` del suo valore maturo — UNA PARTE SU 1736.**
> Non «il campo è al 2.4 %»: **il campo è al 2.4 %, e il PESO che lo costruisce allo 0.06 %.**

### LE CONCLUSIONI CHE NE DIPENDONO, nominate una per una

| | conclusione | dove | perché dipende |
|---|---|---|---|
| **1** | **LA FORMA DEL FRENO-LEGGE, `(d−LAM)·(1+tanh(dx/d))`** — decisa perché `max \|dx\|/d = 0.0531` e *«la saturazione non si presenta MAI»* | `V8`/`V9`, dal giro corto di `CURA 2`, `120` passi, seme `42`, `125 731 076` campioni | **`dx` è mosso dalle forze, e le forze vengono dal campo.** Un massimo di `0.0531` misurato con il peso d'arco a `5.76e-04` **non dice che la saturazione non si presenti con il campo maturo**: dice che **non si presenta a campo spento**. **La DECISIONE è già presa; la sua base va rifatta.** |
| **2** | **LA SOGLIA DI `P-GONFIA`, `< +23.64 %`** — metà della crescita di `CURA 2`, `med vivi 0.938570 → 1.382321` = `+47.2795 %` | scheda ⑫ | **il riferimento è misurato nello stesso regime**, quindi la soglia è *«metà di una crescita a campo spento»*. **Non è invalida, è ANCORATA a quel regime**, e va dichiarato. |
| **3** | **`S7` di `SEMINA_LAM`** — *«la mitosi viva, il bilancio di `d0` CHIUDE»* | scheda ⑫ | è **il solo criterio che può bocciare la cura**, ed è **già sospeso** per la soglia della mitosi. Ora ha **una seconda ragione**. |
| **4** | **le approvazioni di `CURA 1` e `CURA 2`** | `E1a` e `B` | poggiano sui loro giri corti, **tutti a `ramp ≤ 0.024`**. |
| **5** | **`T5` di `CURA 2`** — il confronto `_cura2_corto` contro `_cura1_corto` | `REPERTO_sigillo_cura2_T5` | **entrambi i bracci** sono a campo spento: il confronto **resta valido fra loro** *(stesso regime)*, e **non si trasporta** al regime maturo. |

> ### ❗ **LA DISTINZIONE CHE CONTA, E NON È LA STESSA PER TUTTE:**
> **① è una DECISIONE DI FORMA presa su una misura** → la misura va rifatta.
> **②③④⑤ sono CONFRONTI INTERNI allo stesso regime** → restano validi **fra loro**, e vanno
> **marcati con il regime**, non ritirati.
> **È la regola `9-bis`: ogni numero porta la sua EPOCA. Questi numeri hanno un'epoca in più di
> quella che dichiarano, e non è il blob: è `ramp`.**

**⚠ E CIÒ CHE NON HO MISURATO, per non farlo passare:** **non ho misurato come `\|dx\|/d` scali con
`ramp`.** Che il massimo cresca non è provato, è **atteso** — e l'attesa non è una misura. **Il
criterio per deciderlo esiste e costa poco: rigirare `V8`/`V9` con i nodi maturi.**

---

# 2. LA TORSIONE LETTA DALLO SPINORE

## (a) COSA ESISTE GIÀ — **più di quanto il mandato supponesse**

| pezzo | stato | che cosa dà |
|---|---|---|
| **`_link_su2_N`** | **`staticmethod`, dichiarato PURE-READ** | `N_ij = (1 + n_i·n_j) I + i (n_i × n_j)·σ` |
| **l'identità sigillata** | `csv/_seal_fork/_sigillo_N.py` | **`N_ij = 2 cos(χ/2) U_ij`**, con `U_ij = exp(−i(χ/2) m̂·σ)` la **connessione di Berry unitaria** |
| **`_bloch_ritardato`** | esiste *(Strato 1)* | i Bloch a `t − τ`, con `τ = d/cs` |
| **`circolazione_topologica`** | esiste, **passiva per dichiarazione** | **`berry_spin`**: *«prodotto ciclico degli overlap tra spinori sul ciclo; **curvatura non-abeliana SU(2), gauge-invariante**»* — **SUI CICLI** |
| **`chiralita_core_locale`** | esiste | l'identità materia/vuoto |
| **`_nb`** | **PRESENTE coi default** *(`SPINORE_VIVO = True`)* | il Bloch per nodo |

> ### ✅ **LA ROTAZIONE DEL TRASPORTO NON VA COSTRUITA: È GIÀ `χ = arccos(n_i·n_j)`**, e
> ### l'identità che lo dice **è già sigillata**.
> ### ✅ **E LA CURVATURA SUI CICLI È GIÀ CALCOLATA**, e il codice la chiama con il nome esatto
> ### che la proposta usa: *«curvatura non-abeliana SU(2)»*.
>
> **Si legge coi default**: `_nb` c'è, `_link_su2_N` è pure-read. **Non serve accendere `FORK_SU2`
> per MISURARE** — serve solo per farla agire nella forza.

## ⛔ MA C'È UN CONTO CHE DECIDE, E NON È UNA MISURA

**`arccos` sta in `[0, π]`.** Quindi l'angolo `SU(2)` del trasporto **su un arco** è **al massimo
`π`** — **un quarto** del ricoprimento `4π`.

> ### **SE IL QUANTO DEVE ESSERE `4π`, NON PUÒ VIVERE SU UN ARCO: DEVE VIVERE SU UN CICLO.**
> Non è un limite del regime: **è il codominio di `arccos`.** Nessuna maturazione lo cambia.
> **E il ciclo c'è già**, con la sua curvatura già calcolata: **`berry_spin` su `n_cicli`.**

## LA MISURA — scena `(ii)` `(b)`, **dopo UN passo**, **4 semi**

```
chi = arccos(n_i . n_j), l'angolo di rotazione del trasporto SU(2), per ARCO:
   p05  0.001806 rad = 0.000575 pi        (SE fra semi 8.05e-06)
   p50  0.006619 rad = 0.002107 pi        (SE 2.73e-05)
   p95  0.013763 rad = 0.004381 pi        (SE 3.85e-05)
   max  0.028423 rad = 0.009047 pi        (SE 8.24e-04)
   overlap di spin |N|/2 = cos(chi/2), mediano: 0.999995
   frazione di archi con chi > pi/2  : 0.000000      con chi > 0.9 pi : 0.000000

I CICLI, e la curvatura che il codice calcola GIA':
   n_cicli                   = 256.0 +- 0.0
   |berry_spin| mediano      = 1.16e-05 +- 2.9e-06
   |berry_spin| max          = 5.92e-05 +- 1.1e-05
   olonomia di FASE max      = 35.2437 +- 9.1          (4 pi = 12.566)
   olonomia di FASE media |.|= 11.4222 +- 3.8
```

> ### ⚠ **A UN PASSO LA CURVATURA SU(2) È `1e-5`: CINQUE ORDINI SOTTO QUALUNQUE QUANTO.**
> **Ma questo NON è un verdetto sulla proposta**, ed è importante dirlo: **il settore di spin non
> è maturo a un passo.** I Bloch sono quasi allineati *(overlap `0.999995`)* perché non hanno
> ancora avuto tempo di decorrelare.
>
> **E il valore a maturità È GIÀ MISURATO, nel par.9, e non da me:** `spin_ovl = 0.5` e
> `χ ≈ 90° ± 39°` a `800` passi — **cioè esattamente i valori di direzioni di Bloch CASUALI.**
> **Quindi a maturità `χ` per arco vale `~0.5 π`** — **il doppio di quanto serve per arrivare a
> `π`, e ancora un OTTAVO di `4π`.** Il conto del codominio resta.

### ❗ E UN NUMERO CHE VA NELLA DIREZIONE OPPOSTA: **l'olonomia di FASE supera già `4π`**

`max = 35.24` contro `4π = 12.566`: **`2.8` volte il ricoprimento**, e la media assoluta `11.42`
è **già dell'ordine di `4π`**. **Sui cicli, un quanto di `4π` È RAGGIUNGIBILE** — **per la fase.**
**Per la curvatura di Berry, oggi, non lo è di cinque ordini**, e **quanto lo diventi a maturità
NON L'HO MISURATO** *(richiederebbe il giro sospeso)*.

## (c) I QUATTRO RUOLI DI `tw` — **da dove verrebbero nella proposta**

| ruolo | oggi | **nella proposta** | costo |
|---|---|---|---|
| **creazione** *(mitosi, Schwinger)* | `\|tw\| >= soglia0 = 3π` | **un quanto della rotazione del trasporto** — e per il conto sopra **deve essere l'OLONOMIA di un CICLO**, non di un arco | **il pezzo vero**: la mitosi è per ARCO, l'olonomia è per CICLO. **Serve una mappa ciclo→arco che oggi non esiste** |
| **identità** `chi_basc` | `tw` via `:5092`, gated su `CHI_BASC and (CHI_COOP or not CHI_DA_SPINORE)` | **`CHI_DA_SPINORE`, che ESISTE GIÀ** | **zero legge nuova**: il ramo alternativo è già cablato, oggi `False` |
| **corrente** in `circolazione_topologica` | `tw` come 1-forma orientata | **`berry_spin`, che è GIÀ calcolato nella stessa funzione** | **zero**: il numero è già lì, accanto |
| **orologio** `τ_pp = 1 + \|tw\|/PHI_CRIT` | `tw` come energia che dilata il tempo | **ESCE**: l'orologio unico è `r` | **il secondo pezzo vero**: `τ_pp` è letto da `mitosi`, dal gradiente di soglia e dal tempo proprio d'arco |

> ### ❗ **DUE DEI QUATTRO RUOLI COSTANO ZERO** *(l'identità e la corrente: il codice ha già il
> ### sostituto, nello stesso posto)*. **Due costano davvero:** la **creazione** *(che cambia
> ### granularità: da arco a ciclo)* e **l'uscita dell'orologio** *(che ha tre lettori)*.

## (d) I CRITERI, SCRITTI ORA

| | criterio | cosa boccia |
|---|---|---|
| **`TS-1`** | **la soglia è raggiungibile nel regime `A13`**: frazione di archi *(o cicli)* oltre il quanto **`> 0` su 4 semi** | **boccia la proposta** se è `0`, come oggi è `0` per `3π` |
| **`TS-2`** | **`tw = 0` e `tw = 4π` danno lo STESSO passo, byte per byte** | **boccia** qualunque residuo di lettura «accumulo» |
| **`TS-3`** | **nessun `φ` nella formula**: verifica dall'**AST**, non da un `grep` sul testo | **boccia** se `dph` sopravvive |
| **`TS-4`** | **nessuna perdita**: con incremento a media nulla la grandezza **si conserva** | **boccia** se resta un `− dt/τ` |
| **`TS-5`** | **caso che DEVE fallire** *(`P1-sexies`)*: con il quanto messo a **zero** la creazione **deve scattare su OGNI** ciclo | **boccia il criterio**, non la legge, se non scatta |
| **`TS-6`** | **flag OFF = byte-identico**, firma dei byte, un processo per braccio | è il presidio |

**`TS-1` è quello che oggi si può già valutare in parte**, e la risposta provvisoria è **NO per
gli archi** *(codominio di `arccos`)*, **DA MISURARE per i cicli** *(serve il giro sospeso)*.

## (e) IL COSTO — **quante righe, quanti siti, cosa si rompe**

| | | |
|---|--:|---|
| **la grandezza da leggere** | **`0` righe nuove** | `χ` e `berry_spin` **esistono già** |
| **l'identità** `chi_basc` | **`0`** | `CHI_DA_SPINORE` esiste, va messo a `True` |
| **la corrente** | **`0`** | `berry_spin` è già nella stessa funzione |
| **l'uscita dell'orologio** `τ_pp` | **`3` siti** | `mitosi` *(soglia)*, il gradiente di soglia, il tempo proprio d'arco |
| **la creazione su CICLI** | **il pezzo grosso** | oggi `mitosi` seleziona **archi**; servirebbe **ciclo → arco da dividere**. La macchina dei cicli esiste *(`parent`, `parent_e`, `:1656`-`:1689`)*, la **mappa non c'è** |
| **cosa si rompe subito** | | **`tw` è letto da `POLO_MATURO`, dal `twist_dip`, da `PLAST_DIN` e dalla plasticità**: tolto `tw`, quei siti restano **senza ingresso** |

> ### **IL VERDETTO DI COSTO, onesto:** *«meno lavoro di quanto sembri»* **è vero per tre dei
> ### quattro ruoli.** Il quarto — **la creazione** — **non è meno lavoro: è un cambio di
> ### GRANULARITÀ**, da arco a ciclo, e la mappa di ritorno non esiste nel codice.
>
> **E c'è una cosa che NON so, e non la copro:** se la mitosi diventa un evento **di ciclo**,
> **quale arco del ciclo si divide?** Qualunque risposta *(il più teso, il più lungo, uno a
> caso)* **è un numero o una regola NUOVA**, cioè esattamente ciò che la proposta vuole evitare.
> **Questa è la domanda che va risolta prima, e non la risolvo io.**

---

## ⛔ STOP — **sceglie Luca**

**Ciò che il mandato chiedeva è qui.** Le due cose che, secondo me, vanno decise **prima** di
qualunque riga di codice:

1. **per l'accensione:** se `semina` deve distinguere *«iniziale»* da *«in volo»* — **è l'unico
   pezzo nuovo** che la proposta ① richiede;
2. **per la torsione:** **quale arco di un ciclo si divide** — perché senza quella risposta la
   proposta sostituisce un numero tarato con **una regola nuova**.
