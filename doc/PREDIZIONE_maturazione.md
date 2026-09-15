# PREDIZIONE — l'aliasing sparisce da solo? (scritta **PRIMA** della misura)

> Branch `fork-su2`, 2026-09-15. Blob sul disco **`f5887254`**. **Nessuna modifica alla fisica,
> nessun cablaggio.** Questa è **una misura sola**, e serve a stabilire **se un problema esiste
> ancora** prima di ripararlo.
>
> **Scritta prima di lanciare il run**, così non si adatta al risultato. Il commit che la contiene
> precede il commit dei dati.

---

## 1. IL CONTO CHE MOTIVA LA MISURA

Catena stabilita: `inerzia ~ 1e-7` → `omega` esplode → **112 giri/passo** → il settore di spin è
**aliasato** → i Bloch sono casuali **per risoluzione, non per fisica**.

Ma il `1e-7` è **ETÀ**, non normalizzazione (`doc/INERZIA_massa_o_frazione.md` §4.1):

```
ramp = min(1, eta/TAU_A)     TAU_A = 50 (deterministico)     eta += dt_n (~0.01) per passo
=> peso pieno solo dopo ~5000 passi
```

E la catena delle potenze si deriva:

| grandezza | come scala | perché |
|---|---|---|
| `w = exp(−d/λ)·ramp_i·ramp_j` | **∝ ramp²** | due fattori `ramp`, uno per estremo |
| `abs(F) = abs(Σ w e^{iφ})` | **∝ ramp²** | fasi incoerenti ⇒ somma a random walk (`w·√k`) |
| `psi = satura(F) ≈ F` | **∝ ramp²** | `GAMMA·abs(F) << 1`: la saturazione non morde |
| **`inerzia = abs(psi)²`** | **∝ ramp⁴** | il quadrato |
| `coppia = abs(cross(B,nb))` | **∝ ramp⁰** | `B = Σw·nb/Σw` è una **media pesata**: la scala di `w` si cancella |
| **`omega = coppia/inerzia`** | **∝ ramp⁻⁴** | |

> Da `ramp ≈ 0.03` (passo 150) a `ramp = 1` (passo 5000) sono **33×**, quindi `inerzia` × **1.2·10⁶**
> e `omega` ÷ **1.2·10⁶**: da **112 giri/passo** a **~1e-4 giri/passo**.
> **L'aliasing sparirebbe da solo, per pura maturazione.**

## 2. IL DETTAGLIO CHE DECIDE *QUANDO* — il pavimento `1e-6`

```python
inerzia = np.maximum(self._rho_sorgente(), 1e-6)      # riga 1891
```

Finché la densità è **sotto** `1e-6`, l'inerzia è **bloccata sul pavimento** e la maturazione
**non ha alcun effetto** su `omega`. Misurato finora: densità mediana **1.21e-7** al passo 60, con
il pavimento attivo sul **99.7 %** dei nodi.

> **Predizione derivata:** `theta` **non** scenderà con continuità fin dall'inizio. Resterà piatto
> finché la densità mediana non **attraversa `1e-6`**, e solo **dopo** comincerà a cadere come
> `ramp⁻⁴`. **Il grafico deve mostrare un ginocchio, non una discesa uniforme.** Se scende subito e
> dolcemente, una delle due letture (pavimento o `ramp⁴`) è sbagliata.

Stima di quando: `Lam` (media) vale **4.37e-5** al passo 60 e **1.32e-4** al passo 150, mentre la
**mediana** è ~360× più bassa (distribuzione a coda pesante). Estrapolando, la mediana dovrebbe
attraversare `1e-6` **poco dopo il passo 150-300**. Quindi **il ginocchio è atteso presto**, non a
5000 passi.

---

## 3. I TRE ESITI — la regola, scritta prima

| esito | firma | significato |
|---|---|---|
| **(A) MATURA E RESTA CASUALE** | `theta` scende sotto ~30 gradi/passo **e** `chi` resta a 90.000 ± 39.171 | lo spin **non si ordina davvero**: i sei lati reggono **anche a risoluzione piena**. **Verdetto pulito e definitivo.** |
| **(B) MATURA E L'ORDINE COMPARE** | `theta` scende **e** `chi` si stacca da 90° (materia o p90) oltre l'errore | **c'era ordine, nascosto dall'aliasing**: tutte le misure precedenti hanno misurato uno **sfarfallio**. **Il caso che cambia tutto.** |
| **(C) NON MATURA** | `theta` **non** scende | la mitosi rigenera nodi immaturi più in fretta di quanto i vecchi maturino ⇒ **l'aliasing è STRUTTURALE, non transitorio**. Allora sì, serve una riparazione — e si saprà **quale** problema si sta risolvendo. |

### 3.1 Il presidio anti-illusione, dichiarato prima

> La **mediana** può scendere mentre una **coda** di nodi giovani resta aliasata.
> Quindi si riporta anche **la frazione di nodi con `theta > 30 gradi/passo`** nel tempo.
> **Se la mediana scende ma la frazione resta alta, è l'esito (C) mascherato**, non (A) né (B).

Il motivo per cui questo è probabile e va guardato: **i figli della mitosi nascono con `eta = 0`**
(riga 3119; antinodi 3236). Con mitosi continua esiste **sempre** una popolazione giovane. La
domanda quantitativa è se la sua **frazione** cala o si stabilizza.

### 3.2 Regola statistica, dichiarata prima

- **(A)** o **(C)** con un seme: lecito come **screening**, e va dichiarato tale (§2.7).
- **(B)**: è il caso importante ⇒ **non si dichiara su un solo seme.** Servono **≥ 2 semi** prima di
  affermare qualunque cosa.

---

## 4. LA SECONDA MISURA — solo se `theta` scende

Se e solo se `theta` passa sotto soglia: si rimisura `chi` e `abs(<n>)` **nella zona matura** (ultimi
campioni, e/o solo i nodi con `ramp > 0.9`), con l'osservatore **già sigillato**, separando
**materia / vuoto / p90**, e col **valore-null sempre accanto**: `chi = 90.000 ± 39.171`,
`abs(<n>) ~ 1/√N`.

**`chi` si stacca da 90° oltre l'errore statistico?** Si riporta **il numero**, non l'impressione.

---

## 5. COSA QUESTA MISURA NON FA

Non ripara niente. Non cabla il fattore `cs⁻²`, non tocca il ritardo o lo Strato 1, non aggiunge
tetti su `omega` né sottopassi per lo spin, **non tocca `TAU_A` né il regime** — che è esattamente
la scala di maturazione che si sta misurando.

> **Cablare mentre il sistema è aliasato darebbe un risultato inattribuibile.** È il motivo per cui
> questa misura viene prima di ogni cura.
