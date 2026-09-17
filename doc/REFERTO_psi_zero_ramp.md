# REFERTO — **`psi = 0` non è mancata inizializzazione: è il RAMP sull'ETÀ.** Il cablaggio autorizzato sarebbe stato inerte.

**Blob:** `69ee540` (byte grezzi `ee0c2a60`). **Nessun codice toccato.**

Il via libera era per: *«calcolare `psi` una volta alla costruzione della scena, prima del primo
`step`»*. **La verifica preliminare dice che è già calcolato, e che non è quello il meccanismo.**

---

## 1. `psi` È GIÀ CALCOLATO ALLA COSTRUZIONE DELLA SCENA

La catena esiste già nel codice:

```
nuova_massa()  ->  semina(..., mass_id=mid)  ->  _registra_concorrenza()  ->  calcola_psi()
```

**Misurato subito dopo `nuova_massa`:**
```
nodi 120   archi 4715
max|psi| = 0        ma  len(psi) == n  ->  psi E' STATO CALCOLATO
```

**Aggiungere una chiamata a `calcola_psi()` lì sarebbe stato INERTE:** avrebbe ricalcolato la stessa
cosa e riottenuto **zero**. *(E sarebbe stata la quinta rete sopra lo stesso buco.)*

---

## 2. LA CAUSA VERA: `ramp = min(1, eta/TAU_A)`, e alla nascita `eta = 0`

```
eta: min 0, max 0           ramp = min(1, eta/TAU_A) = 0
pesi _pesi(): max 0         ->  F = mat(w) @ (...) = 0  ->  psi = 0
```

`_pesi()` costruisce `base = exp(-d/lam) * ramp[i] * ramp[j]`. Con `eta = 0` **tutti i pesi sono
zero**, quindi il campo è zero **qualunque cosa faccia `calcola_psi`**.

**CONTROPROVA, ed è quella che chiude la questione:** forzando `eta = TAU_A` (nodi maturi) e
ricalcolando, **`max|psi| = 8.02`**. Il campo **c'è**: è il **kernel** che lo azzera.

> **Quindi `psi = 0` non è «l'assenza dell'inizializzazione» (A7b): è il valore CORRETTO di una
> legge che dice «un nodo appena nato non pesa ancora».** `eta = 0` alla nascita **non è un
> difetto** — un nodo nasce con età zero. **A7b non si applica**, e l'argomento ③ del guardiano,
> che era il più forte dei tre, **cade insieme agli altri due.**

---

## 3. IL FATTO NUOVO, ed è più grande della domanda che l'ha prodotto

| passo | `eta` mediana | **`ramp` mediano** | `max|psi|` |
|---|---|---|---|
| 1 | 0.01 | **0.0002** | 0 |
| 20 | 0.175 | 0.0035 | 2.8e-04 |
| 60 | 0.531 | **0.0106** | 2.1e-03 |
| 120 | 1.086 | **0.0217** | 5.7e-03 |

`eta` cresce di **~0.009 per passo** *(è `eta += dt_n`, cioè il **tempo proprio**, non il numero di
passi)*, e `TAU_A = 50`:

> **Per `ramp = 1` servono ~5526 passi. I run di questo programma sono 300-500.**
> **A 500 passi `ramp` mediano vale ~0.09: il kernel gira a meno del 10 % della sua ampiezza.**
> **E poiché `base ∝ ramp[i]·ramp[j]`, il peso d'arco tipico è ~1 % di quello maturo.**

**Questo NON è un difetto, ed è importante non chiamarlo così:** `ramp` è una **legge** (la
maturazione dell'arco col tempo proprio del nodo), non una regolarizzazione. **Ma è una condizione
di regime mai dichiarata:** tutte le misure di questo programma sono state prese su un sistema in
cui **il kernel non ha mai finito di accendersi**.

**E non ho misurato le conseguenze.** Dire *«quindi le misure sono sbagliate»* sarebbe esattamente
l'errore di ampiezza-contro-correlazione già catalogato in §9. **Quello che è stabilito è il
regime, non il suo effetto.**

---

## 4. COSA NE È DEI TRE ARGOMENTI CHE AVEVANO PRODOTTO IL VIA LIBERA

| argomento | esito |
|---|---|
| **① la comparabilità è già rotta** | **REGGE**, e resta vero indipendentemente da tutto questo: quattro blob, tre correzioni di legge. *(È l'argomento che ha demolito la mia raccomandazione «dopo la campagna», e la demolizione tiene.)* |
| **② `omega_s` è memoria persistente** | **CADUTO**, misurato: al passo 0 `omega_s` **non cambia di un bit** (campo zero → coppia zero → l'inerzia non conta), e al passo 1 la variazione `0.0059` è **dentro l'intervallo di regime** (0.0060-0.0064) |
| **③ `psi = 0` è un'incoerenza (A7b)** | **CADUTO**: `psi = 0` è il **valore corretto** di `ramp = 0`, e `eta = 0` alla nascita è **giusto** |

**Restava ① a sostenere «prima, non dopo». Ma «prima» era prima di COSA:** di una modifica che, ora
si sa, **non avrebbe cambiato niente.**

---

## 5. COSA RESTA VERO, E COSA CAMBIA

**Resta vero che il transitorio blocca le correzioni che costruiscono rapporti fra grandezze di
stato** (voce **Z6**): ai primi passi `peq` e `rho` sono sotto il minimo di macchina, e ① ha dovuto
gestirlo con un fallback contato. **Ma la causa non è quella che credevamo:** non è
un'inizializzazione mancante, è che **il kernel deve accendersi**, e ci mette il tempo che una legge
gli dà.

**E questo cambia quali cure sono ammissibili.** Forzare `psi` a un valore non nullo alla nascita
significherebbe **scavalcare `ramp`**, cioè **sopprimere una legge** per comodità numerica — la
stessa classe di errore del pavimento `1e-6` sull'inerzia, con segno opposto.

**NON PROPONGO UNA CURA.** Le vie che vedo — accorciare `TAU_A` per il ramp, disaccoppiare `ramp`
dall'età, o accettare il transitorio e continuare a contarlo — **sono tutte decisioni di regime**,
e due su tre toccano una legge. **Vanno decise, non dedotte da me.**
