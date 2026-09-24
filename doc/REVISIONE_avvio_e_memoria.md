# REVISIONE — **L'AVVIO E `memoria_hebbiana_moto` USANO UN TEMPO DIVERSO DAL RESTO?**

> **Domanda di Luca, 2026-09-24. SOLA LETTURA, nessuna riga di codice.**
> Blob `49fc54d2`. Tabelle generate da `csv/_test_fork/_revisione_mhm.py` *(AST)* e
> `csv/_test_fork/_revisione_avvio.py` *(sonda pure-read, 4 passi)*. **`P1-ter`.**

---

## RISPOSTA IN UNA RIGA

> ### **SÌ a entrambe.** L'avvio gira **senza tempo proprio** *(al passo 1 `r = 1` per tutti)*;
> ### `memoria_hebbiana_moto` usa `DT` di coordinata e il **cono GLOBALE** in due siti su sei —
> ### e **tre** delle famiglie di difetto che vi compaiono **sono già curate ALTROVE, non lì**.

---

## 1. L'AVVIO

### 1a. `ritmo()` torna `r = 1` per tutti — **UNA volta sola, al passo 1**

```
PASSO 1  ritmo_chiamate=1  ritmo_r1=1  forma_r1=(-1, 2391)
PASSO 2  ritmo_chiamate=2  ritmo_r1=1
PASSO 3  ritmo_chiamate=3  ritmo_r1=1
PASSO 4  ritmo_chiamate=4  ritmo_r1=1
```

**`ritmo_r1` resta `1`: scatta solo alla PRIMA chiamata**, e la forma `(-1, 2391)` dice il
perché — **`_psi_prec` era `None`**, non corto.

> ### ❗ **CONSEGUENZA: al passo 1 TUTTO il sistema gira con `r = 1`, cioè con il tempo di
> ### COORDINATA.** `dt_n = DT·r = DT` e `dt_e = DT·0.5(r_i+r_j) = DT` per **ogni** nodo e
> **ogni** arco. **Non è che l'avvio usi *un altro* tempo proprio: al passo 1 il tempo proprio
> NON ESISTE.**
>
> **⚠ E NON È UN DIFETTO OVVIO:** al passo 1 **non c'è un passato** con cui misurare una fase,
> quindi `r` **non è calcolabile**. La convenzione `1` è *«nessuna dilatazione»*, ed è la stessa
> che `_r_nodo_mitosi` usa *(`CURA 2`)*. **Il difetto, se c'è, è che nessuno lo DICHIARA:** un
> run parte con un passo di fisica a tempo di coordinata e **nessun referto lo dice**.

### 1b. Il fallback `exp(iφ)` dello spinore — **scatta alle invocazioni 1, 2, 3 su 9**

```
1  fallback=True   len(_psi_spinor)=0  n=2391  max|phi|=12.566238  phi_non_zero=2391/2391
2  fallback=True   len(_psi_spinor)=0  n=2391  max|phi|=12.566238
3  fallback=True   len(_psi_spinor)=0  n=2391  max|phi|=12.566238
4  fallback=False  len(_psi_spinor)=2391
TOT invocazioni=9  con fallback=3
```

**Cosa legge `φ` lì: `max|φ| = 12.566238`, contro `4π = 12.566371`.** **`φ` copre già TUTTO il
dominio `4π`**, su **tutti** i `2391` nodi *(nessuno a zero)*.

E il fallback fa:

```python
_psp[:, 0] = np.exp(1j * self.phi[:_n])      # in `calcola_psi`
```

> ### ⚠ **RICLASSIFICATO — CORREZIONE DI LUCA, `C3`. NON È UN PONTE `INVERSA`.**
>
> **Avevo scritto:** *«è un ponte `INVERSA`, la stessa forma per cui `TW_SPINORE` è bloccato»*.
> **È sbagliato, e la smentita è nel commento DUE RIGHE SOPRA il fallback** *(`:3414`)*:
>
> ```
> Riduzione-al-limite S3: con _psi_spinor=(e^{i phi},0) -> comp 0 == self.psi.
> ```
>
> ### **Il fallback NON è un ponte: È LA CONDIZIONE INIZIALE SCALARE, DICHIARATA.**
> È il **limite `S3`** — *«nel limite in cui lo spinore è la fase pura sull'asse 0, il campo
> spinoriale coincide col campo scalare»* — e il fallback **lo realizza**, invece di violarlo.
> **`TW_SPINORE` è tutt'altro: una LEGGE che a ogni passo fa scrivere allo spinore una
> grandezza che prende la scala da `φ`.** Un **punto di partenza dichiarato** e una **legge
> permanente non dichiarata** non sono la stessa cosa, e **chiamarle insieme era mio.**
>
> ### ❗ **E IL PERIODO `2π` È CERTO PER ALGEBRA, non «da misurare».**
> `exp(iφ)` ha periodo `2π`: `exp(i(φ+2π)) = exp(iφ)`. **Non c'è niente da misurare.**
> Quindi un `φ` su `4π` e il suo ridotto su `2π` **danno lo STESSO spinore iniziale**.
>
> ### ➜ **CONSEGUENZA DA SCRIVERE ORA, PER `CURA 3`:**
> **stesso VALORE, ma i BYTE possono differire all'ultima cifra.** `exp(i·φ)` e
> `exp(i·(φ mod 2π))` sono matematicamente uguali e **numericamente no**: la riduzione cambia
> l'argomento, e l'arrotondamento dell'ultimo bit con esso.
> **IL SIGILLO DI `CURA 3` DEVE PREVEDERLO**: su questo sito **non può chiedere identità di
> byte**. Deve chiedere **uguaglianza entro l'ulp**, e **dichiararlo** — altrimenti produce un
> `FAIL` falso su una cura corretta, che è il difetto già catalogato di `T1` in `E4-LAM`.

### 1c. La semina al passo zero — **`223 380` archi nati ESATTAMENTE a `LAM`**

```
archi=525973  sotto_LAM=0  min/LAM=1.000000  esattamente_LAM=223380
nascite=4  SCALA_MIN=False  SCALA_MIN_PASSO=True
```

`_nasce` *(«il troncone sotto `LAM` si porta A `LAM`»)* è gated su
`SCALA_MIN or SCALA_MIN_PASSO`.

> ### ❗ **IL `42.48 %` DEGLI ARCHI NASCE SUL MURO.**
>
> **⚠ E «SONO GLI STESSI ARCHI» ERA DEDOTTO DA DUE CONTEGGI DIVERSI — `STANDARD 9`, rilievo di
> Luca (`C1`). ORA È PROVATO**, al passo ZERO, un processo per braccio
> *(`csv/_seal_fork/_prova_nasce_identita.py`)*:
>
> ```
> sha1(d_on)             = f24d4d38f9f81f4b        <- il braccio con `_nasce`
> sha1(max(d_off, LAM))  = f24d4d38f9f81f4b        <- il braccio senza, troncato a mano
> IDENTICI BIT A BIT     = True     elementi diversi: 0 su 525973
>
> min(d_off)/LAM         = 0.012098
> archi con d_off < LAM  = 223380 su 525973 (42.47 %)
> archi con d_on == LAM  = 223380                  <- LO STESSO NUMERO
> ```
>
> ### **`_nasce` è `np.maximum(d, LAM)` E NIENT'ALTRO**, e i due conteggi **coincidono**:
> ### `223 380`. **Non è più una deduzione: è un'identità di byte.**
>
> ### **QUINDI `Z148` VA CORRETTO NEL MECCANISMO, NON NEL VERDETTO:** avevo scritto *«il freno
> ### ci appoggia il sistema contro»*. **Non è il freno: è `_nasce`, alla NASCITA.** Il freno li
> ### tiene lì dopo — `min/LAM` passa da `1.000000` a `1.000049` in quattro passi — **ma a
> ### metterli sul muro è la semina.**
>
> **`A11` cor.6:** un limite che morde sul **42 %** della popolazione **non è un limite: è la
> legge.** E qui morde **al passo zero**.

---

## 2. `memoria_hebbiana_moto` — **le sei scritture vere**

*(`:5895-6357`, `462` righe. Undici scritture, di cui **cinque** sono il pavimento `_pav_d0`.)*

| sito | TEMPO | CONO | GLOBALI | difetti nella chiusura | **curato ALTROVE?** |
|---|---|---|---|---|---|
| **`:5969`** `proj` | — | — | `median` | `A2`/`D01` · `D02` · `A11` | **sì, mai qui** |
| **`:6116`** `spinta · median(d0)` | **`DT`** | **GLOBALE** `c_sistema` | `median`, `mean` | `D18` · `A2`/`D01` · `D02` · `A11` | **sì, mai qui** |
| **`:6122`** `grav · median(d0)` | **`DT`** | **GLOBALE** `c_sistema` | `median` | `D18` · `A2`/`D01` · `A11` | **sì, mai qui** |
| **`:6145`** `flusso` | — | — | `median` | `A2`/`D01` | **sì, mai qui** |
| **`:6296`** `_delta_coes` | **`DT`** | **LOCALE** `cs_arco` | — | **metà curato** *(vedi §3)* | `C4`, **a metà** |
| **`:6298`** `coesione_relazionale` | **`DT`** | **LOCALE** `cs_arco` | — | `A11` *(clip)* | `C4`, **a metà** |

> **⚠ IL METODO E IL SUO LIMITE, dichiarati:** la chiusura è **sintattica** e si ferma al bordo
> della funzione. **Non legge dentro i metodi chiamati** — `_sd0`, `_pav_d0`, `_smorza`,
> `_traccia_d0`, `pozzo_grafo`, `_nb_grav` e gli altri sono **elencati nel referto generato**,
> così il buco è visibile. **È un LIMITE INFERIORE: ciò che trova c'è; ciò che non trova può
> esserci lo stesso.**

### ❗ LE TRE FAMIGLIE **GIÀ CURATE ALTROVE E NON QUI**

| famiglia | dov'è curata | dove NON lo è |
|---|---|---|
| **cono LOCALE invece che globale** *(`D18`)* | **`COES_CAUSALE` `C4`** | **`spinta` `:6116` e `gravità` `:6122`** — entrambe su `c_sistema = LAM·√K_C` |
| **scala LOCALE invece della mediana globale** *(`A2`, `D01`)* | **`PEQ_NASCITA_LOCALE` `C2`**, **`SCALA_P` `Z67`** | **quattro siti su sei**, che moltiplicano per `median(d0[mask])` |
| **forma ESATTA invece dell'Eulero / niente clip** *(`A11`)* | **`PEQ_ESATTO` `C1`**, **`ANOM_SIMM` `C1-bis`** | `:6298`, che clippa `coesione_relazionale` |

---

## 3. `DT` DOVE IL TEMPO UNICO VORREBBE `dt_e`

**`30` usi di `DT` in `10` funzioni.** Non tutti sono difetti — il conteggio dei sottopassi CFL
e la **costruzione di `dt_e` stessa** devono usarlo.

| funzione | usi |
|---|--:|
| `step` | `10` |
| **`memoria_hebbiana_moto`** | **`5`** |
| `_applica_flag` | `3` |
| `ritmo` | `3` |
| `mitosi` | `2` |
| `_bloch_ritardato` | `2` |
| `_passo_spinoriale` | `2` |
| `_fattore_tempo_arco` | `1` *(legittimo: costruisce `dt_e/DT`)* |

### ❗ E DOVE `DT` INCONTRA UN CONO — **è lì che il tempo unico lo vuole**

```
:6057  memoria_hebbiana_moto   passo_causale = c_sistema * DT
:6113  memoria_hebbiana_moto   passo_causale = c_sistema * DT
:6253  memoria_hebbiana_moto   _passo_causale = _csa * DT        <- COES_CAUSALE
```

> ### **`COES_CAUSALE` HA CURATO METÀ DEL CONO.**
> Un tetto causale è **velocità × tempo**. `C4` ha reso **LOCALE la velocità** *(`_csa` =
> `cs_arco`)* e ha lasciato **GLOBALE il tempo** *(`DT`)*.
> **Il risultato è un ibrido: `cs` del luogo × orologio di nessun luogo.**
>
> **È il rilievo di Luca, ed è esatto.** E la forma della cura **esiste già**: è quella di
> `CURA 2` — `dt_e` al posto di `DT`.

---

## 4. PROPOSTA ORDINATA — **NESSUN CODICE. Decide Luca.**

### ✅ A. **ESTENSIONI** — stessa forma, stessa cura, stesso sigillo. **Non sono leggi nuove.**

| | estensione | da | a | perché è un'estensione e non una cura nuova |
|--:|---|---|---|---|
| **A1** | il **tempo** del cono | `CURA 2` *(`dt_e` invece di `DT`)* | `:6253` `_passo_causale = _csa · DT` | `C4` ha già localizzato la **velocità**; manca **l'altra metà della stessa formula**. Sigillo: quello di `C4`, con un test in più |
| **A2** | il **cono** | `COES_CAUSALE` `C4` | `:6057` e `:6113` *(spinta e gravità)* | la forma locale **esiste già ed è sigillata `5/5`**. Qui si applica dove non è stata applicata |
| **A3** | la **scala locale** | `PEQ_NASCITA_LOCALE` `C2` / `SCALA_P` `Z67` | i quattro siti con `median(d0[mask])` | `Z67` ha già sostituito una mediana globale con un **pozzo locale**, con sigillo `5/5` |

> **Perché queste tre prima:** **non introducono nessuna legge nuova**, hanno **già un sigillo
> di riferimento**, e ognuna **toglie** un difetto catalogato invece di aggiungerne uno.

### ⚠ B. **DIFETTI NUOVI** — non hanno una cura altrove da estendere

| | difetto | prova | nota |
|--:|---|---|---|
| **B1** | **al passo 1 il tempo proprio NON ESISTE**: `ritmo()` torna `r = 1` per tutti, e **nessun referto lo dichiara** | `_ritmo_sicurezza = 1`, forma `(-1, 2391)` | **non è curabile** *(senza passato `r` non è calcolabile)*: è **da DICHIARARE**, non da curare. Il presidio naturale è una riga in `CONFIGURAZIONE.txt` |
| ~~**B2**~~ | ~~il fallback `exp(iφ)` è un ponte `INVERSA`~~ **RITIRATO** *(`C3`, Luca)*: è la **condizione iniziale scalare DICHIARATA** a `:3414` *(limite `S3`)*, non un ponte | `3` invocazioni su `9` | **non è un difetto.** Resta la **conseguenza per `CURA 3`**: il periodo `2π` è certo per algebra, quindi **stesso valore ma byte diversi all'ultima cifra** → **il sigillo deve prevederlo** |
| **B5** | **`_nasce` è gated su `SCALA_MIN or SCALA_MIN_PASSO`** *(`:3850`)*: **la legge `d >= LAM` è VERIFICATA sempre ma FATTA RISPETTARE da un'opzione** | `223 380` archi nascono sotto `LAM` coi default del sorgente | **`D38`**, e **è lo schema che `E4-LAM` ha TOLTO al controllo**: *il controllo è legge, chi la fa rispettare alla nascita è un'opzione* |
| **B3** | **il `42.48 %` degli archi NASCE sul muro** *(`_nasce`)* | `223 380` su `525 973` esattamente a `LAM` al passo `0` | **`A11` cor.6.** È il **gemello di `D31` alla NASCITA**, e `D31` parla del **freno**. **Corregge il meccanismo che avevo scritto in `Z148`** |
| **B4** | **`D02` — legge `pos` (il DISEGNO) invece di `d`** | compare nella chiusura di `:5969` e `:6116` | **mai curato da nessuna parte**, e non ha una cura da estendere |

### ❗ E L'ORDINE CHE PROPONGO, con la ragione

0. **`B3` + `B5` INSIEME — ed è la decisione `D-b` di Luca: si parte da qui, come CURA DELLA
   SEMINA.** *«Non deve nascere un arco sotto `LAM`. Il troncone `_nasce` resta come
   PRESIDIO.»* **Sono lo stesso difetto visto da due lati:** `B3` dice *quanti* nascono sul
   muro, `B5` dice *che a tenerli lì è un'opzione*;
1. ~~**`B3`**~~ *(assorbito nel punto 0)*;
2. **`A1`** — perché è **due caratteri di formula** su una cura già sigillata, e chiude il
   rilievo di Luca sull'ibrido `cs` locale × `DT` globale;
3. **`A2`**, poi **`A3`** — per **grandezza dell'effetto misurato** *(`A12`)*: il cono tocca due
   siti, la scala quattro, ma il cono è un **tetto causale** e la scala un **fattore**;
4. **`B1`** e **`B2`** — **dichiarazioni prima che cure**: `B1` non è curabile e `B2` va deciso
   da Luca, perché tocca la condizione iniziale dello spinore;
5. **`B4`** per ultimo, perché è il solo che **non ha una forma di cura già scritta**.

> **⚠ E `CURA 3` NON È IN QUESTA LISTA, di proposito:** la revisione era **sola lettura** e non
> la ordina. **Se venga prima o dopo, e se il freno-legge la preceda, è il CHECKPOINT di Luca.**
