# PREDIZIONE — la prima misura del settore spinoriale su sistema PULITO

**Scritta PRIMA del run.** Data: 2026-09-15 · Branch `fork-su2` · Blob **`08784685`** (dal disco).
Nessuna modifica alla fisica in questo lavoro.

---

## 0. PERCHÉ È LA PRIMA MISURA VERA

Due difetti silenziosi curati oggi:

| | difetto | frequenza | sigillo |
|---|---|---|---|
| 1 | `_cs_nodo_prev` scartata a ogni mitosi → `tau = d/cs` calcolava `d/CS_M` | **71.88 %** | **5/5** |
| 2 | `_psi_spin_prec` non esteso alla mitosi → il ramo a **4π** scartato | **95.33 %** | **6/6** |

Il secondo, nella formulazione già committata (`CLAUDE.md` §9, `doc/REPERTO_psi_spin_prec.md`):

> `r` **non era stale** — il ramo scalare a `2π` girava sempre. Ciò che non entrava mai in funzione è
> la **sovrascrittura con la versione a 4π**. Le misure **non sono corrotte**: sono misure di un
> **sistema diverso da quello che il flag dichiarava**.

**Conseguenza:** i sei lati su «il settore di spin non si organizza» sono stati presi con la doppia
copertura **inerte**. Non dicono *«l'idea non funziona»*: dicono *«un sistema senza doppia copertura
attiva non produce struttura di spin»*. **Il verdetto sul settore spinoriale vero non è mai stato
preso.**

---

## 1. ⚠ UNA CORREZIONE AL MANDATO, scritta PRIMA dei dati

Il mandato dice che l'esito **(A)** renderebbe *«dicibile»* la frase *«anche con la doppia copertura
attiva lo spin non si organizza»*. **Solo in parte, e la parte che manca va dichiarata adesso**,
altrimenti domani diventa una scusa.

**`theta` resta a ~43 giri/passo: il settore è ALIASATO, e queste due cure non lo risolvono.**
Sotto aliasing, fra un campione e il successivo il Bloch compie decine di giri interi: **due nodi
qualsiasi appaiono scorrelati anche se la dinamica sottostante li sta ordinando.** Quindi:

> **(A) è l'esito che l'aliasing produrrebbe DA SOLO, indipendentemente dalla fisica.**
> Un (A) è compatibile con «non c'è ordine» **e** con «c'è ordine, e non lo vediamo». **Non separa
> le due.** È un negativo **più pulito di prima** — la doppia copertura ora gira davvero — ma
> **non è un negativo conclusivo**, e non va scritto come tale.

**Ciò che (A) renderebbe davvero dicibile, per intero:**
> *«Con la doppia copertura attiva e il settore campionato a ~43 giri/passo, nessuna delle firme
> misurabili si stacca dal valore casuale. Resta indeciso se ciò dipenda dall'assenza di ordine o
> dall'impossibilità di vederlo a questa risoluzione.»*

**(B) e (C), invece, sono conclusivi anche sotto aliasing**, e per una ragione asimmetrica:
**l'aliasing distrugge segnale, non lo crea.** Una firma che **emerge** nonostante il campionamento
grossolano è un segnale **vero e sottostimato**. Un'assenza, no.

---

## 1-bis. ⚠ AGGIORNAMENTO — **DUE BRACCI, non uno** (mandato corretto da Luca, 2026-09-15 sera)

**Il mandato precedente escludeva `--tau-luce`**, mettendolo nella stessa casella del turbo. **Era un
errore di categoria, e lo accolgo:** il turbo **amplifica un parametro** per rendere visibile un
effetto; `--tau-luce` è una **correzione di LEGGE** (il rilassamento legato al tempo-luce `d/cs`
invece che alla densità, coerente con `inerzia = T²`). E soprattutto **è l'unica cosa che abbassa
`theta`**. Escluderlo significava fare la prima misura vera **alla risoluzione peggiore disponibile**.

**Si corregge con due bracci, non con una scelta.**

| braccio | cos'è | `theta` |
|---|---|---|
| **OFF** (`--tau-luce` spento) | la **baseline CERTIFICATA** — i sigilli della FASE 2 non sono passati, il gate **non è ri-timbrato di proposito** | **misurato: 92.8–98.7 giri/passo** |
| **ON** (`--tau-luce` acceso) | la **migliore risoluzione disponibile oggi** | atteso **~43 giri/passo** |

Tutto il resto **identico**: stessa scena, **stessi semi**, `≥ 2` semi, senza turbo / Step 2 /
Kuramoto. **Non è «scegliere il braccio giusto»: è misurare lungo un GRADIENTE DI RISOLUZIONE.**

### ⚠ E una correzione a un numero che avevo scritto io in questo stesso documento

Il §1 diceva *«`theta` resta a ~43 giri/passo»* come se fosse il valore del sistema. **Falso: il 43
è il valore del braccio ON**, cioè **con `--tau-luce` cablato**. Il valore **naturale** è
**92.8–98.7** (misurato, 2 semi). Avevo trasportato un numero da una configurazione a un'altra.
**Non cambia il verso del caveat: lo raddoppia.**

## 3-bis. LA LETTURA A DUE BRACCI — fissata PRIMA del braccio ON

| esito | lettura |
|---|---|
| **struttura in ON e NON in OFF** | **È REALE**, ed è emersa **abbassando l'aliasing**: la firma più forte ottenibile oggi. È anche il **controllo incrociato** che nessun braccio singolo può dare |
| **struttura in ENTRAMBI** | ancora più forte: sopravvive **anche** al campionamento peggiore |
| **niente in nessuno dei due** | **(A) NON conclusivo** — *«nessuna struttura visibile a questa risoluzione»*. La frase *«anche con la doppia copertura attiva lo spin non si organizza»* resta **INDICIBILE** finché `theta` non scende sotto la soglia di aliasing |
| **struttura in OFF e non in ON** | **ANOMALIA.** L'aliasing non crea segnale: sarebbe un **reperto da capire**, non un risultato. Si riporta come tale e **ci si ferma** |

**Le soglie numeriche restano quelle del §2, invariate**, applicate **separatamente a ogni braccio**.

## 2. I TRE ESITI — soglie fissate ADESSO

**Valori sotto ipotesi nulla** (`CLAUDE.md` §9): `chi = 90.000° ± 39.171°` per direzioni di Bloch
casuali; `|<n>| ≈ 1/√N`; autocorrelazione spaziale `≈ 0` a ogni distanza.

**Errore di riferimento:** `SE(chi) = std/√n_archi`. Con `n_archi ~ 5000` e `std ~ 39°`,
**`SE ≈ 0.55°`**. Le soglie sotto sono in unità di `SE`, così non dipendono dalla taglia del run.

### (A) NIENTE CAMBIA — *il negativo, con il suo limite*
Tutte e tre:
- `|chi_media − 90°| < 3·SE` in **materia** e nel **p90**;
- `|<n>| / (1/√N) < 2` in ogni regione;
- autocorrelazione compatibile con 0 in **ogni** bin (`|acorr| < 3·SE_bin`).

→ il verdetto dei sei lati **regge anche col 4π attivo**. **Ma con il caveat del §1**, non senza.

### (B) COMPARE STRUTTURA — *il caso importante, doppio rigore*
**Tutte e tre**, e su **≥ 2 semi**:
- `|chi_media − 90°| > 5·SE` (staccato, non sfiorato);
- **e** l'autocorrelazione decade a una **scala finita**: almeno un bin vicino con
  `acorr > 3·SE_bin`, **e** i bin lontani compatibili con 0 — *né ~0 ovunque, né ~1 ovunque*;
- **e** `|<n>| < 0.5` — **non** collasso.

→ **la doppia copertura era il pezzo mancante.**

### (C) COLLASSO — *da chiamare col suo nome*
- `chi_media` scende **e** `|<n>| > 0.5` **e** autocorrelazione `> 0.5` anche nel bin **più lontano**.

→ **non è struttura: è allineamento globale degenere.** È la lezione già pagata con Kuramoto
(`doc/PREDIZIONE_kuramoto.md`): *un `chi` basso da solo non è ordine.*

---

## 3. LA MIA PREDIZIONE — **(A)**, e con quale fiducia

**Predico (A).** La ragione non è che «lo spin non si organizza», è **aritmetica**: a ~43 giri/passo
il segnale è sotto-campionato di un fattore ~43, e **nessuna firma spaziale sopravvive a quel
campionamento** a meno che l'ordine non sia quasi totale — nel qual caso sarebbe **(C)**, non (B).

**Con quale fiducia: poca.** In questa sessione ho predetto **due** volte e sbagliato **due** volte
(l'effetto della cache `cs`: predetto zero, misurato `z = 3.16` su un seme — e poi non riproducibile;
la *ragione* di quell'errore: argomento di ampiezza su una domanda di correlazione). Lo scrivo perché
**una predizione vale come impegno, non come autorità.**

**E la cosa che renderebbe (B) credibile nonostante la mia predizione:** la **forma**, non il valore.
Un `chi` che scende **insieme** a un'autocorrelazione che decade a **scala finita** è una firma che
l'aliasing **non sa fabbricare**. Se compare, vince sui miei conti.

---

## 4. REGOLE DI LETTURA — dichiarate

- **Il verso e la FORMA decidono, non «chi si abbassa».** Un `chi` basso senza la forma giusta è
  collasso (C), non struttura (B).
- **Nessuna statistica senza `SE`, `r²`, `IC95` e `n`** (§9).
- **E la barra giusta è quella FRA SEMI, non quella interna al run.** Oggi è stato misurato che su
  questo sistema caotico la stessa grandezza cambia da seme a seme **~3 volte** più di quanto dica la
  `SE` interna (`doc/RAMIFICAZIONI.md` **C10**). Uno scarto che supera la `SE` interna ma non la
  dispersione fra semi **non conta**.
- **Non si misurano grandezze NORMALIZZATE per vedere se cambiano.** `median(r)` è inchiodata a `1.0`
  per costruzione (`x = f/median(|f|)`, mappa monotona): si riporta la **dispersione** di `r`, mai la
  mediana. *(Errore commesso stamattina dal sigillo `S4` e registrato come presidio in §9: **prima di
  misurare se qualcosa cambia, verifica che sia LIBERA di cambiare.**)*
- **L'aliasing va detto nella stessa riga del numero**, non in nota.

---

## 5. COSA QUESTA MISURA NON PUÒ DIRE

- **Non dice** se le cure hanno spostato T3: quello è un altro numero, e va riportato **senza
  attribuirlo** (le predizioni su quel divario sono state sbagliate **tre** volte — mandato ~50 %,
  io zero, realtà 16.9 % poi **ritirato** perché era dispersione di run).
- **Non dice** che l'aliasing sia risolto. **Non lo è.**
- **Non chiude** il fronte **R** (l'anello di retroazione: forse è il *bersaglio* `−0.69` a essere
  mal calcolato). Quello richiede di misurare `sigma` **nello stesso run**, e non è questo lavoro.
