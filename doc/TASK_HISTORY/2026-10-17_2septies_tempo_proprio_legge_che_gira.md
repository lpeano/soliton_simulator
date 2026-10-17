# `2-septies` — **IL TEMPO PROPRIO GUARDA UNA LEGGE CHE NON GIRA**

*(punto `3` del mandato unico del guardiano del `2026-10-17`, su mandato di Luca.
Base: `c98f5721`. E' il `3` dell'ordine nuovo, dopo il `2-sexies`.)*

> ### ⛔ **QUESTO FILE SI COMMITTA PRIMA DEL CODICE** *(`CLAUDE.md` §8)*.

---

## 1. RAGIONAMENTO PRELIMINARE — *e il difetto e' un FALSO-UNO per META'*

### ⭐ **CHE COSA GIA' FA BENE, e va detto prima del difetto**

Il ciclo principale di `_collauda_tempo_proprio.py` ### **percorre `CM.ORDINE`** e misura
`|psi(dtau) - psi(dtau/2)|` ### **per ogni pezzo che gira.** ### ✅ **Quella parte legge
DALLA TABELLA**, ed e' giusta.

### ⛔⛔ **IL DIFETTO E' SOLO NEL BRACCIO `(2)`, e ne basta un pezzo**

```
buoni = [x for x in ("CAMM-MONETA-SPIN", "CAMM-SATURAZIONE") if x not in visti]
esito("### (2) DEVE DIPENDERE: la moneta di spin e la saturazione", len(buoni) == 2, ...)
```

> ### ⛔ **`visti` sono I VIOLATORI**, cioe' i pezzi che ### **NON dipendono da `dtau`**.
> ### **E `CAMM-SATURAZIONE` non e' nell'ordine**, quindi ### **non viene MAI misurata**,
> quindi ### **non e' mai fra i violatori** — ### **e il braccio la conta BUONA.**
> ### ⛔⛔ **Cioe' META' DEL BRACCIO E' SODDISFATTA DALL'ASSENZA:** il braccio dice
> *«la saturazione dipende da `dtau`»* ### **senza averlo misurato.** ### **E' un
> falso-uno.**

### ⭐⭐ **E A CHE SERVIVA IL BRACCIO `(2)`: e' il CONTROLLO POSITIVO del `(1)`**

Il braccio `(1)` dice *«i violatori sono ### **esattamente quelli attesi»*, e oggi gli
attesi sono ### **ZERO.** ### ⚠ **Quindi `(1)` passa in DUE casi:** ### ① nessun pezzo
viola *(la verita')*, e ### ② ### **`dipende_da_dtau` non sa VEDERE una violazione** —
per esempio se tornasse sempre un numero grande.
### ⛔ **Il braccio `(2)` dovrebbe escludere il caso `②`, e NON lo fa:** dire *«questi due
dipendono da `dtau`»* ### **e' la stessa affermazione del `(1)`, non il suo controllo.**

### ✅ **IL CONTROLLO VERO E' QUELLO CHE IL MANDATO CHIEDE:** ### **un pezzo dell'ordine
reso INDIPENDENTE da `dtau` deve essere VISTO come violatore.** ### **Quello si', esclude
il caso `②`.**

### ⭐ **CHE COSA CREDO, PRIMA DI GUARDARE**

| | credo che… | e ### **NON LO SO** |
|---|---|---|
| `a` | si possa rendere un pezzo indipendente da `dtau` ### **in memoria**, fissando `mot.dtau` dopo aver costruito la scena *(e' un array per nodo)* | ### ⚠ **non so se l'operatore legga `mot.dtau` SEMPRE**: se se lo fosse copiato alla costruzione, fissarlo dopo ### **non cambierebbe niente**, e il braccio sarebbe ### **vacuo** |
| `b` | i pezzi ### **distinti** dell'ordine siano `6`, e che ### **tutti** dipendano da `dtau` | — |
| `c` | togliere i due `import saturazione` morti faccia diventare ### **ORFANE** `3` eccezioni di `[[P-TAB]]` *(`energia.py`, `_misura_mb2.py`, e `_collauda_tempo_proprio.py` quando il braccio non la nomina piu')* | ### ⚠ **non so se siano `3` o `2`**: `_misura_mb2.py` nomina l'`id` ### **anche in `ORDINE_VECCHIO`**, che e' ### **legittimo e resta** |

### ⛔ **E SE `(a)` E' FALSO, MI FERMO E LO DICO:** un braccio che *«deve fallire»* e non
fallisce ### **non si aggiusta abbassando la soglia** — si cerca ### **un'altra via per
rendere il pezzo indipendente**, e se non c'e' ### **si riferisce.**

---

## 2. PROGETTAZIONE — *i passi, i criteri, e cosa mi FERMA*

| | il passo | il criterio |
|---|---|---|
| `1` | il braccio `(2)` ### **riscritto sui pezzi CHE GIRANO**, letti dalla tabella: ### **tutti** i pezzi distinti dell'ordine dipendono da `dtau` | il ### **minimo** fra le distanze misurate e' ### **`>= CAMBIA_MIN`** *(`1e-9`, la soglia di oggi, ### **non si tocca**)* |
| `2` | ### ⛔ **il caso che DEVE fallire:** un pezzo dell'ordine reso ### **indipendente da `dtau`** *(`mot.dtau` FISSO, in memoria)* deve risultare ### **violatore** | la distanza misurata ### **`< CAMBIA_MIN`**; se non ci riesco, ### **STOP e relaziono** |
| `3` | i due `import saturazione` ### **morti** togliati *(`energia.py`, `_misura_mb2.py`)* | ### **nessun uso di `SAT.` resta** in quei due file |
| `4` | le eccezioni di `[[P-TAB]]` diventate ### **ORFANE** togliate ### **nello stesso commit** | `P-TAB` a ### **`0` errori** |
| `5` | la suite | ### **`56` su `56`**, e il `pre-commit` nel budget |

### ⚠ **E UNA COSA CHE NON FARO':** non tolgo `CAMM-SATURAZIONE` da `ORDINE_VECCHIO` di
`_misura_mb2.py` — ### **e' un confronto STORICO dichiarato**, e un confronto storico
### **deve** nominare l'ordine di allora.

---

## 3. TODO

1. `primo_ordine/_collauda_tempo_proprio.py`: il braccio `(2)` ### **dalla tabella**, e il
   ### **caso che deve fallire.**
2. `primo_ordine/energia.py` e `primo_ordine/_misura_mb2.py`: gli ### **import morti.**
3. `csv/_strumento_dalla_tabella.py`: le eccezioni ### **orfane.**
4. il referto, la relazione, la RIPRESA e la riga della coda.
