# IL TEST DI JEANS DEL MODELLO, CON MATERIA UNIFORME DINAMICA

> **Il mandato:** decisione di Luca del `2026-10-19` alle `20:33`. La condizione di Luca:
> ### **«dobbiamo essere sicuri di saper creare la materia»**. ### **Nessun codice di fisica:
> una misura.** ### **`LINEARE` e `Lambda_c` restano FERMI** fino all'esito.
> **Il fatto registrato prima** *(`08a52679`)*: ### **in `D4` la materia era CONGELATA**
> *(`congela = "pezzo"`)*, e lo svuotamento del grumo ### **potrebbe venire dal protocollo.**

**LIVELLO CORRENTE:** `L2`.

## 0. LA STELLA POLARE

1. **`A14`:** ### **non si applica come domanda su una legge**: nessuna cambia. ### **E qui la
   materia NON e' congelata** *(`congela = "no"`)*: `M`, `V` e `G` ### **si misurano** *(`M2`)*,
   invece di essere violati dallo strumento come in `D4`.
2. **Il gradino:** `(a)` le barre fra blocchi, un seme, due `dtau`, il controllo positivo dello
   strumento *(`M4`)*; `(b)` ### **`J2` a `cs` spento e' il riferimento**; `(c)` ### **non
   raggiunto** -- «alla Jeans» e' un confronto di FORMA, non con un limite numerico noto.
3. **Aggiunge un numero o una legge?** ### **No.** Le ampiezze, il seme e la banda sono
   ### **parametri della misura**, dichiarati qui.
4. **Tocca `rho`, `c_s` o il segno?** ### **Misura come `rho` e `Lambda` uniformi, ENTRAMBI
   dinamici, reagiscono a una perturbazione** -- ### **i due versi dell'accoppiamento insieme**,
   per la prima volta su questa scena.
5. **Emergente o imposto?** ### **E' la domanda:** se una perturbazione della materia
   uniforme cresce da sola, la «gravita'» del modello ### **aggrega** -- ### **senza** una
   sorgente fotografata.

## 1. «SAPER CREARE LA MATERIA», prima di qualunque perturbazione *(se una cade: STOP)*

### ⭐ **COME SI COSTRUISCE LA MATERIA UNIFORME, dichiarato qui, e PERCHE' resta uniforme:**
la scena di `D4` *(`scena_l2`: toro `31x31`, `U = I`, `n` geometrici: per ogni nodo **quattro
estremita'** con `n = +x, -x, +y, -y`, la moneta `eps = 0.5`)*. ### **Uno STESSO spinore su
tutte le estremita' NON e' stazionario**: la moneta `exp(-i eps dtau sigma.n_h)` ruota diverso
ogni tipo di estremita'. ### **Il «modo `k = 0`» e' allora lo stato INVARIANTE PER
TRASLAZIONE:** ### **su ogni estremita' lo spinore ALLINEATO col suo `n`**
*(`scena_l2.spinore_allineato`, autovettore `+1` di `sigma.n`, fase `0`)*, con ampiezza
### **`sqrt(x)`** -- cosi' `rho_k = 4 x = x * Lambda_medio` *(`Lambda_medio = 4`)*. ### **E' il
grumo di `D4` steso su tutto il toro.**
### ✅ **PERCHE' `rho_k` e `Lambda_k` restano UNIFORMI e COSTANTI:** il passo e' ### **invariante
per traslazione** *(toro, `U = I`, `n` per tipo d'estremita', `cs` e le fasi uniformi su
uno stato uniforme)*, quindi ### **lo stato resta nel sottospazio invariante per traslazione**
-- `rho_k = M/N` e `Lambda_k = V/N` per ogni `k`, ### **costanti perche' `M` e `V` si
conservano.** ### ⚠ **NON e' un autostato di `psi`:** dentro il nodo i `4 x 2` numeri ruotano
ancora *(la moneta, Grover, la fase)*; ### **e' stazionario per le DENSITA', che e' cio' che
`M1` misura.**

| | la prova | il criterio |
|---|---|---|
| `M1` | ### **EQUILIBRIO:** materia uniforme a `x` in `{0.01, 0.1, 1}`, vuoto uniforme, ### **SENZA perturbazione**, `cs` acceso, rapporto `1`, `2000` tick | ### **`max_k,t |rho_k(t) - rho_m|` e `|Lambda_k(t) - Lambda_m|` entro la BANDA**: ### **`256` ulp ogni `64` tick** *(la banda delle norme, `_collauda_cs_l1.ULP_NORME`, alla scala di `D3` -- `64` tick)*, cioe' ### **`256 * (t/64)` ulp della scala** a `t` tick |
| `M2` | ### **CONSERVAZIONE**, negli stessi bracci, ### **NESSUN congelamento** | `M` e `V` ### **entro la stessa banda**; ### **`G` *(`energia_pesata.g_dello_stato`)* si RIPORTA** *(`max|G - G0|/|G0|`)*: e' conservata al ### **secondo ordine**, non al bit, e un criterio al bit sarebbe sbagliato |
| `M3` | ### **SPETTRO:** la FFT 2D, sul toro, di ogni componente di `psi` per tipo d'estremita' | ### **potenza fuori da `k = 0` NULLA** *(`<= 256` ulp della potenza a `k = 0`)*; ### **e col toro DISPARI (`31`) un modo a `k = pi` esatto non esiste** -- ### **lo dico** |
| `M4` | ### **CONTROLLO POSITIVO DELLO STRUMENTO DI FIT:** una successione sintetica `exp(gamma t)(1 + 0.01 n_t)` *(`n_t` normale, seme `20261019`)*, con `gamma` in `{1e-3, 1e-2}` per tick, passata ### **alla stessa funzione** *(`_instabilita_vuoto.gamma_del_tratto`)* | ### **restituisce `gamma` entro `3` barre**. ### ⚠ **Nel test di ieri sera questo controllo NON c'era:** lo strumento era lo stesso, ### **e questa prova vale anche per lui, a posteriori** |

## 2. I BRACCI, rapporto `Lambda_c/Lambda_medio = 1` se non detto

- ### **LA PERTURBAZIONE, che conserva `M` e `V`:** come nel test di ieri sera per `phi`
  *(`phi_h *= sqrt(1 + a r_h)`, `r` a media pesata nulla)*, ### **e la stessa per `psi`**
  *(con `w = |psi_h|^2`, un secondo `r` dallo stesso generatore)*; ### **`a = 1e-6`, seme
  `20261019`**. ### **Le fasi non cambiano.**

| | il braccio | che cosa dice |
|---|---|---|
| `J1` | materia uniforme, ### **`x` in `{0.01, 0.1, 1}`**, perturbazione su `psi` e `phi`, `dtau 0.5`, `2000` tick, `congela = "no"` | cresce? e ### **`gamma` cresce con `rho_m`?** |
| `J2` | come `J1` a `x = 0.1`, ### **`cs` SPENTO** | ### **il riferimento** |
| `J3` | come `J1` a `x = 0.1`, ### **`dtau 0.25`, `4000` tick** | ### **fisica o numerica** |
| `J4` | ### **LA PROVA DEL PROTOCOLLO:** il braccio di `D4` a rapporto `1`, `x = 0.01` *(stesso grumo, stessa accensione `T_SCAN = 100`, `1200` tick, `dtau 0.5`)*, ### **con `congela = "no"`** | ### **lo svuotamento del grumo, contro quello CONGELATO di `963535bc`** |

## 3. LA MISURA

- `J1`-`J3`: ### **`gamma` di `max|delta rho|` e di `max|delta Lambda|`**, col tratto e le
  barre del test di ieri sera *(`T0 = 20`, fino a `1e-2` della scala, `5` blocchi)*, in tick e
  in tempo proprio; ### **la lunghezza d'onda** del modo dominante *(la FFT 2D al tick `T1`)*;
  e ### **`gamma(k)`**: per ogni `k`, `ln(P_k(T1)/P_k(T0))/(2 (T1 - T0))`, ### **mediato per
  anelli di `|k|`** con la barra *(deviazione / `sqrt(n)` dell'anello)*. ### **La lunghezza
  MINIMA, se esiste, e' il `lambda` piu' corto il cui `gamma(k)` supera `3` barre.**
- `J4`: ### **`<delta Lambda>` nel grumo per blocco** *(`delta` contro `Lambda_medio = 4`: la
  base senza sorgente e' uniforme al bit, `D4`)* e ### **`rho` del grumo nel tempo**; e i
  numeri congelati letti da `doc/referti_l2/d4_bracci.jsonl` *(`963535bc`)*.

## 4. I CRITERI

- ### **«instabile» se `gamma > 0` con `>= 3` barre**; `J2` e' il riferimento; `J3` dice
  fisica/numerica *(`gamma` in tempo proprio entro `3` barre combinate)*.
- ### **«alla Jeans»: `gamma` CRESCENTE con `rho_m`** *(i tre `x` di `J1`)* ### **e una
  lunghezza minima.** ### **Nessun verdetto di fisica oltre questi: i numeri.**
- ### **Se il punto fisso di `cs` non converge:** si registra e si va avanti, senza cure.
- ### **SE `M1`-`M4` NON PASSANO: STOP**, prima di leggere `J1`-`J4`.

**ANNOTAZIONE DEL 2026-10-19 SERA, PRIMA DEL CODICE (decisione di Luca delle 21:45 sullo STOP di `82b2e79f`: i BRACCI DIAGNOSTICI).** *(Si annota, non si riscrive.)* ### **Errore `n.18` del guardiano:** `M1` *(«senza perturbazione `rho` e `Lambda` restano costanti per tutta la corsa»)* ### **confondeva «so creare la materia» con «la materia e' stabile»**, che e' la domanda stessa del test. ### **Se esiste un'instabilita', nessuno stato uniforme puo' restare uniforme al bit.**

- ### **`M1` RIDEFINITA: l'EQUILIBRIO AL TICK `0`.** La variazione di `rho_k` e `Lambda_k` nel ### **PRIMO tick** sta entro ### **`256` ulp della scala** *(`rho_m`, `Lambda_m`: la banda delle norme, `_collauda_cs_l1.ULP_NORME`)*. ### **Che poi resti uniforme o no e' il RISULTATO, non una precondizione.**
- ### **LE BARRE DEL FIT (`M4`):** «`3` barre» resta il ### **`99.73%`**, ma la soglia si prende ### **dalla `t` di Student coi gradi di liberta' veri** *(`5` blocchi: `4`)*, ### **calcolata dallo strumento** *(`scipy.stats.t.ppf`)*: con `4` gradi e' ### **circa `6.6` barre**. ### **Nessun numero nuovo.** ### **`M4` si ripete sui semi `0`..`199`** *(dichiarati)* e la copertura ### **deve essere `99.73%` entro `3` deviazioni binomiali** *(`sqrt(p(1-p)/200)`)*. ### **E si riportano i verdetti del test di ieri sera** *(`c2dd6453`)* **con la soglia corretta.**
- ### **I BRACCI DIAGNOSTICI**, tutti ### **dalla materia uniforme col SOLO rumore d'arrotondamento** *(nessuna perturbazione aggiunta)*, `x = 0.1` e rapporto `1` se non detto, `dtau 0.5`, `2000` tick:

| | il braccio | che cosa dice |
|---|---|---|
| `D1` | il riferimento: `cs` acceso, ### **`x` in `{0.01, 0.1, 1}`** | `gamma` e la sua dipendenza da `x` |
| `D2` | ### **`cs` SPENTO** | cresce ancora? |
| `D3` | ### **`dtau 0.25`, `4000` tick** | ### **`gamma` in tempo proprio uguale entro la soglia: FISICA; altrimenti NUMERICA** |
| `D4'` | ### **senza `CAMM-FASE-VUOTO`** | quale legge alimenta la crescita |
| `D5` | ### **la deriva di `G` nella SOLA fase esponenziale** *(fino a quando `max|delta rho|` supera l'`1%` di `rho_m`)*, con `g_dello_stato`, in ogni braccio | ### **resta al livello del secondo ordine o cresce con la perturbazione?** Si riporta ### **il rapporto fra la deriva relativa di `G` e `max|delta rho|/rho_m`** alla fine della fase |
| `J4` | ### **la prova del protocollo** *(il braccio di `D4` a materia dinamica)*, come gia' fissato | lo svuotamento contro quello congelato |

- **Per ogni braccio:** `gamma` *(in tick e in tempo proprio)*, la lunghezza d'onda del modo che cresce, ### **la lunghezza minima** *(il `lambda` piu' corto il cui `gamma(k)` supera la soglia di Student)*, e ### **`gamma` contro `x`** *(`D1`)*.
- ### **«instabile» se `gamma >= t_(99.73%, 4) * barra`**; e la stessa soglia per `D3` *(sulle barre combinate)*.
- ### **Se il punto fisso di `cs` non converge, il braccio si chiude li'** *(tick, `Lambda` min, `Lambda_c`)*, senza cure.
- ### **Nessun verdetto di fisica oltre a fisica/numerica e alla legge che alimenta la crescita.** ### **`LINEARE` e `Lambda_c` FERMI.**

## 5. TODO

1. `csv/_jeans_del_modello.py`, un processo per braccio, i risultati scritti mentre corrono;
   commit prima della corsa.
2. la corsa dal blob pulito; il referto; la relazione.
