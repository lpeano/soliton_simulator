# `2c` — **CREAZIONE DI FACCIA**: valutazione della proposta del guardiano

> **Mandato di Luca, 2026-09-25:** *«Proposta del guardiano, da valutare e NON scrivere: creazione
> di faccia = un nodo nuovo al CENTRO del triangolo, collegato ai tre vertici, con lunghezze =
> raggio circoscritto calcolato dalle tre `d` (niente `pos`); nasce solo se quel raggio `>= LAM`
> (`A13`). Nessun arco da scegliere. Valutane costo e conseguenze.»*
>
> **NON SCRITTA. STOP: sceglie Luca.**

---

## ✅ COSA LA PROPOSTA RISOLVE — **la domanda che ieri avevo dichiarato irrisolvibile**

Ieri ho scritto, come la cosa che bloccava tutto:

> *«Se la mitosi diventa un evento di ciclo, **quale arco del ciclo si divide?** Qualunque
> risposta (il più teso, il più lungo, uno a caso) **è una regola nuova** — cioè esattamente ciò
> che la proposta vuole evitare.»*

**La creazione di faccia la scioglie, e non aggirandola: NON SI DIVIDE NESSUN ARCO.** Il nodo nasce
**al centro** e i tre archi sono **nuovi**. **La domanda non ha più un oggetto.**

## ✅ E LE LUNGHEZZE NON SONO UNA SCELTA: SONO **L'UNICA** ASSEGNAZIONE POSSIBILE

Il centro è **equidistante dai tre vertici** — è la definizione di circocentro — quindi
**le tre lunghezze DEVONO essere uguali, e il loro valore comune È `R`.**

```
R = (a·b·c) / (4·K)          K = area, da Erone: K = sqrt(s(s−a)(s−b)(s−c)),  s = (a+b+c)/2
```

> **Dalle TRE `d` e da nient'altro. Nessun `pos`** — quindi **conforme ad `A3`**, che è il fronte
> per cui `pos` non deve entrare nella geometria.
> **E non è un'approssimazione:** è algebra elementare sui tre lati.

**⚠ E UNA COSA CHE VA DETTA PERCHÉ SEMBRA UN PROBLEMA E NON LO È:** per un triangolo **ottuso** il
circocentro cade **fuori** dal triangolo. In un grafo relazionale **«fuori» non ha significato**:
esistono solo le tre distanze, e restano `R` tutte e tre. **Il caso ottuso non richiede niente.**

## ✅✅ E RISOLVE **`U2`/`M2`** PER QUESTO CANALE — **per costruzione, non per fortuna**

**Oggi la mitosi mette i figli a `d/2`**, e **`_nasce` li porta a `LAM` quando `d < 2 LAM`**:
misurato, **la frazione di archi sotto `2 LAM` è `0.2936`** *(scena `(a)`)* e **`0.2998`** *(`(b)`)*.
**Quasi un terzo delle divisioni FABBRICA LUNGHEZZA.**

> ### **Nella creazione di faccia i tre archi nuovi hanno lunghezza `R`, e `R >= LAM` È LA
> ### CONDIZIONE DI NASCITA. Quindi `_nasce` NON TRONCA MAI su questo canale.**
> **Il secondo motore del gonfiamento si spegne da sé**, senza una regola in più.

## ✅ E UN VANTAGGIO SUL BILANCIO DI `d0`, che non era nel mandato

**La mitosi di oggi RIMUOVE l'arco diviso** *(`keep = ones(...); keep[sel] = False`)* e ne crea
due. **La creazione di faccia non rimuove niente:** aggiunge `1` nodo e `3` archi.
**Un bilancio in cui niente scompare è più facile da chiudere**, ed è il bilancio che `S7` chiede.

---

## ⚠ IL CONTO CHE DECIDE SE IL MECCANISMO VIVE — **derivato, scritto prima della misura**

Per un triangolo **equilatero** di lato `a`:  **`R = a/√3`**. Quindi:

```
R >= LAM   <=>   a >= sqrt(3) · LAM = 1.7321 LAM
```

| lato | `R / LAM` | nasce? |
|--:|--:|---|
| `1.000 LAM` *(il minimo che `A13` ammette)* | `0.5774` | **NO** |
| `1.500 LAM` | `0.8660` | **NO** |
| `1.7321 LAM` | `1.0000` | al limite |
| `2.000 LAM` | `1.1547` | **sì** |
| `2.356 LAM` *(la mediana MISURATA di `d`)* | `1.3602` | **sì** |

> ### ❗ **UN TRIANGOLO DI LATI `LAM` — il più piccolo che `A13` ammette — NON PUÒ PARTORIRE.**
> **Il gate morde**, e morde **dove deve**: la faccia più piccola non genera un nodo che starebbe
> sotto la scala di Planck.
> ### ✅ **MA IL TRIANGOLO TIPICO SÌ:** `mediana(d) = 2.356 LAM` dà `R = 1.36 LAM`. **Il gate non
> ### uccide il meccanismo.**

---

## ⛔ IL BUCO VERO, E NON È L'ARCO: **IL GATE È SOLO DAL BASSO**

Per un triangolo quasi **degenere** *(tre vertici quasi allineati)* si ha `K → 0`, e quindi

```
R = abc/(4K)   ->   R -> +INFINITO
```

> ### **`R >= LAM` è soddisfatta BANALMENTE dai triangoli più PIATTI**, e quel nodo nascerebbe con
> ### **tre archi lunghissimi**. **La proposta non dice niente su questo caso.**

**DUE STRADE, e la prima è derivata:**

1. **`R <= R_CONN`**, dove `R_CONN = 3·LAM` **esiste già** ed è *«il raggio con cui il vuoto si
   allaccia»*. **Un nodo i cui archi superano `R_CONN` non sarebbe allacciato al vuoto**: non
   sarebbe un nodo del vuoto, sarebbe un nodo isolato con tre fili lunghi.
   **Quindi il limite dall'alto NON è un numero nuovo: è la condizione di appartenenza al grafo.**
   *(Lo propongo come candidato; non lo scrivo.)*
2. **misurare la frazione di triangoli degeneri** e vedere se conta. **Lo strumento di `2b` la
   misura** *(`frazione_degeneri`, `R_p95`, `R_max`)*.

---

## ⛔⛔ E IL PROBLEMA PIÙ GROSSO, che non è né l'arco né il degenere: **MANCA IL TASSO**

**`R >= LAM` è un VINCOLO, non un TASSO.**

- **Oggi la mitosi ha un tasso:** `prob = clip(resp, 0, 1)` *(o `1 − exp(−resp)`)*, e
  `nasce = rng.random(k) < prob`. **Quante divisioni per passo** è deciso da quella probabilità.
- **La creazione di faccia, come formulata, non ha nulla di simile.** Se l'unica condizione è
  `R >= LAM`, e i triangoli misurati sono **`1 697 590`** con mediana `R = 1.36 LAM`, allora
  **nascerebbero milioni di nodi in UN passo.**

> ### **QUESTA È LA DOMANDA APERTA, e non è quella dell'arco: è QUANTO SPESSO una faccia partorisce.**
> E la risposta **non può essere `R >= LAM`**, perché quello dice *se è possibile*, non *quanto
> spesso*. **Serve una grandezza che faccia da tasso**, e le candidate che il codice già ha sono
> **la curvatura del triangolo** *(che è esattamente ciò che `2b` sta misurando)* **o la torsione**
> *(che è la legge che si vuole sostituire)*.
>
> **Se il tasso viene dalla CURVATURA, la proposta si chiude su sé stessa** — la faccia partorisce
> in proporzione alla sua curvatura di Berry, cioè **la stessa grandezza che definisce `tw` nella
> lettura dallo spinore**. **Ed è l'unica via che non introduce un numero.**
> **Ma richiede che la curvatura sia STRUTTURATA e non rumore**, che è esattamente ciò che `2b`
> deve dire. **Quindi `2c` DIPENDE da `2b`, e non è indipendente da esso.**

---

## IL COSTO, in numeri

| | |
|---|--:|
| **triangoli nel grafo** *(scena `(ii)` `(b)`, `4252` nodi, `148 237` archi)* | **`1 697 590`** *(conteggio esatto)* |
| costo dell'enumerazione, `~ Σ deg²/2` con grado medio `~70` | **`~10⁷` operazioni PER PASSO** |
| `R` dalle tre `d` | **`O(1)` per triangolo**, vettorizzabile |
| il nodo nuovo | **grado `3`**, contro un grado medio di **`70`** |
| archi rimossi | **`0`** *(la mitosi ne rimuove `1`)* |

**⚠ E DUE CONSEGUENZE STRUTTURALI:**

1. **il nodo nuovo NON passa da `_allaccia`**: i suoi tre archi sono **imposti**, non trovati per
   raggio. **Quindi non si allaccia al vuoto come tutti gli altri nodi**, e il suo intorno è
   diverso per costruzione. **Va deciso se è voluto.**
2. **i siti che leggono `tw` restano senza ingresso** se `tw` esce: `POLO_MATURO`, `twist_dip`,
   `PLAST_DIN`, la plasticità, e `τ_pp` con i suoi tre lettori. **È lo stesso costo già stimato in
   `doc/LETTURA_accensione_e_torsione.md`, e non cambia.**

---

## IL VERDETTO, e ciò che NON so

> ### ✅ **LA PROPOSTA È MIGLIORE DELLA DOMANDA CHE VOLEVA RISOLVERE.** Toglie la scelta
> ### dell'arco *(che era una regola nuova)*, dà le lunghezze **per algebra**, non tocca `pos`,
> ### e **chiude `U2`/`M2` su questo canale per costruzione.**
>
> ### ⛔ **MA NON HA UN TASSO**, e senza tasso `R >= LAM` farebbe nascere quasi ogni triangolo.
> ### **Il tasso è la vera domanda aperta**, e l'unica risposta che non introduce un numero è
> ### **la curvatura stessa** — che è ciò che `2b` deve dire se è struttura o rumore.
>
> ### ⚠ **E IL GATE VA CHIUSO ANCHE DALL'ALTO.** `R <= R_CONN = 3 LAM` è un candidato
> ### **derivato** *(appartenenza al grafo)*, non scelto. **Non l'ho scritto.**

**COSA NON SO, e non provo a coprire:** se la curvatura di un triangolo sia **abbastanza grande e
abbastanza strutturata** per fare da tasso. **Lo dice `2b`, non io**, e finché non lo dice
**questa proposta è una forma senza una legge.**
