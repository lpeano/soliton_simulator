# LE DUE BANDE DI `W` — **il controllo passa, ma solo in `SU(2)`; nessuna grandezza per banda si conserva**

> **Mandato di Luca, 2026-10-13:** *«Luca chiede se l'energia vada cercata su materia e
> antimateria come dominio. Nelle camminate di tipo Dirac le due BANDE del passo lineare
> `W` sono particella e antiparticella.»*
>
> **E la priorita' dello stesso giorno:** *«il limite d'uso settimanale e' quasi esaurito
> [...] Usa quello che resta SOLO per le misure in coda, in quest'ordine: (1) l'energia nel
> regime in cui la saturazione lavora; (2) le bande materia/antimateria (prima il controllo
> che `C` le scambi).»*

---

## 1. ⛔ PRIMA DI TUTTO: **IL RITO NON E' STATO RISPETTATO, E NON LO BACK-DATO**

### ⛔ **Non ho scritto le previsioni di `B2` e `B3` PRIMA dei numeri.** Il paragrafo `8`
di `CLAUDE.md` dice che il ragionamento **si scrive e si committa prima**, e il mandato lo
ripete: *«previsioni scritte PRIMA dei numeri, nel task history»*.
### ⚠ **Ho eseguito direttamente**, perche' la priorita' di Luca dice di usare il budget
*«SOLO per le misure»*. ### ⛔ **Non e' una scusa: la priorita' ordina COSA misurare, non
sospende il rito.**

### ✅ **E non lo back-dato**, che sarebbe la cosa peggiore: scrivere adesso previsioni che
*«avevo»* ### **sarebbe una bugia verificabile da git** *(questo file e' committato **dopo**
la misura, e il commit lo mostra)*.

### ⚠ **CHE COSA SI SALVA, ed e' poco:** per `B1` la previsione **era nel mandato stesso**
*(«`N` spento: costanti entro ulp (controllo); se no, i proiettori sono sbagliati»)*, e
### **quella l'ho verificata come controllo, non come conferma di una mia previsione.**
### ⛔ **Per `B2` e `B3` non ho niente da opporre ai numeri**, e lo dico.

---

## 2. ⭐ IL CONTROLLO DELLA LETTURA — **passa, ma SOLO con `det U = 1`**

> **Il mandato:** *«Verifica che `C` SCAMBI le due bande [...] entro ulp. **Se non lo fa,
> "bande = materia/antimateria" non e' la lettura giusta: fermati e riportalo.**»*

### ✅ **Il conto che lo rende un test diretto:** `C` e' **antilineare**, quindi se
`W v = e^{-i omega} v` e `C W = W C` allora `C v` e' autovettore con `e^{+i omega}` —
### **`omega -> -omega`, cioe' le bande si scambiano.** Percio' il controllo e'
`||C(W psi) - W(C psi)||`, ### **e non una somiglianza a occhio.**

| `U` | `|CW - WC|` | spettro simmetrico | `|P+C - CP-|` | |
|---|--:|--:|--:|---|
| `U(2)` generico | `4.327e+00` | `8.852e-03` | `2.175e+00` | ### ⛔ **FALLISCE** |
| **`SU(2)`** | `8.006e-16` | `2.220e-15` | `1.061e-14` | ### ✅ **PASSA** |

### ⛔ **ED E' UNA CONDIZIONE DI FISICA, non un dettaglio numerico.** `C A = A C` vuol dire
`sigma_y A* sigma_y^-1 = A`. Per la **moneta di spin** vale sempre *(`sigma_y (sigma.n)*
sigma_y^-1 = -(sigma.n)`)*; per il **Grover** vale perche' `(2/d)J - I` e' **reale**; per lo
**spostamento con trasporto** chiede `sigma_y U* sigma_y^-1 = U`, che vale ### **se e solo
se `det U = 1`** — la parte `U(1)` del determinante **non si cancella**.

### ⚠ **E `motore.Geometria` VALIDA SOLO L'UNITARIETA' di `U`, non il determinante:** la
tabella e il motore ### **permettono un trasporto che ROMPE LA `C`**, che e' una legge
della carta. ### ⛔ **Un vincolo di fisica senza presidio e' una tenda** *(`A9`)*, e la
decisione e' di Luca: **`[[DOMANDA-TRASPORTO-DEVE-STARE-IN-SU2]]`**.

### ✅ **E HO AGGIUNTO `su2` A `deriva.py` CON IL DEFAULT SPENTO**, perche' la misura della
deriva *(`db328b9`)* e' **gia' committata con `U(2)` generico** e ### **ribaltare un default
cambierebbe un numero gia' pubblicato senza che nessuno l'abbia chiesto.**

### ⭐ **E IL SETTORE `0` E' VUOTO**, che il mandato chiedeva di guardare: `0` dimensioni su
`64`, peso `0.0000`. ### **Le bande piatte dei Grover non compaiono su questa scena**,
quindi `Q = N+ - N-` e' definita **senza un pezzo di stato che non ha segno.**

---

## 3. `B1` — **LE POPOLAZIONI: il controllo regge, e `N` mescola IN COPPIE**

| `N` | `x` max | esc. `N+` | esc. `N-` | esc. rel. `N+` |
|---|--:|--:|--:|--:|
| **spento** *(controllo)* | `0.97` | `1.478e-12` | `8.598e-13` | ### ✅ **`2.02e-14`** |
| acceso | `0.0152` | `2.517e-03` | `2.517e-03` | `3.45e-05` |
| acceso | `0.2425` | `6.036e-01` | `6.036e-01` | `8.27e-03` |
| acceso | **`0.97`** | `1.012e+01` | `1.012e+01` | **`1.39e-01`** |
| acceso | `3.88` | `1.408e+01` | `1.408e+01` | `1.93e-01` |
| acceso | `15.52` | `2.910e+01` | `2.910e+01` | `3.99e-01` |

### ✅ **IL CONTROLLO REGGE:** con `N` spento le popolazioni sono costanti a **`2.02e-14`
relativo**, perche' `W` **commuta coi suoi proiettori spettrali**. ### **Quindi i
proiettori sono giusti, e tutto il resto si legge.**

### ⭐ **E IL FATTO PIU' NETTO DI TUTTA LA MISURA:** `esc N+` e `esc N-` coincidono **a
tutte le cifre** a ogni `x`, e ### **`corr(Delta N+, Delta N-) = -1.0000` ESATTO.**
### ✅ **`N` mescola le bande IN COPPIE**, e questa e' **la forma misurabile dell'idea di
Luca** *(«la saturazione e' l'unico pezzo che puo' mescolarle, cioe' creare e annichilare
coppie»)*. ### ⚠ **E la causa e' in parte strutturale**: `||psi||^2` e' conservata a
`2.05e-14` e il settore `0` e' **vuoto**, quindi `N+ + N-` **non puo'** cambiare.
### ⛔ **Percio' il contenuto vero del `-1.0000` e' che le coppie sono ESATTE, non che
esista una legge in piu'.**

### ⭐ **E IL MESCOLAMENTO E' MONOTONO IN `x`**, su quattro ordini di grandezza
*(`3.45e-05` a `x ~ 0.015`, `3.99e-01` a `x ~ 15`)*: ### **la creazione di coppie e'
accesa dalla saturazione**, ed e' ### **la stessa monotonia in `x` che la misura dell'energia
ha trovato.**

---

## 4. `B2` — **L'ENERGIA PER BANDA: nessuna combinazione torna, e non ne invento una**

*(`x = 0.97`, il regime in cui la saturazione lavora; `200` tick)*

| la grandezza | scala | escursione | relativa |
|---|--:|--:|--:|
| `E+` | `2.468` | `9.441e+00` | `3.83e+00` |
| `E-` | `3.073` | `9.230e+00` | `3.00e+00` |
| `E0` | `0` | `0.000e+00` | — |
| `Re<psi\|W psi>` | `0.6049` | `1.661e+01` | `2.75e+01` |
| il termine del **vuoto** | `1.123` | `1.100e+01` | `9.80e+00` |
| `||psi||^2` | `118` | `2.416e-12` | ### ✅ **`2.05e-14`** |

### ⛔ **NIENTE PER BANDA SI CONSERVA**, e le escursioni relative sono **di ordine `1` o
piu'**.

### ⭐ **LE CORRELAZIONI FRA LE VARIAZIONI** — *il mandato dice «riporta le correlazioni
misurate: NON inventare una formula per farla tornare»*:

| fra | e | correlazione | che cosa dice |
|---|---|--:|---|
| `Re<psi\|W psi>` | il **vuoto** | `+0.1049` | ### ⛔ **NON si compensano:** una compensazione darebbe `~ -1` |
| `E+` | `E-` | `-0.0468` | ### **praticamente SCORRELATE** |
| `E+` | `N+` | `+0.3926` | debole, positiva |
| `N+` | `N-` | **`-1.0000`** | ### ⭐ **ESATTO: le coppie** |
| `Q` | `somma_k h_k` | `+0.1881` | debole |
| `Im<psi\|W psi>` | `somma_k h_k` | `-0.1699` | debole |
| `Im<psi\|W psi>` | `Q` | **`-0.9438`** | ### ⭐ **FORTE** |

### ⛔ **LA RISPOSTA ALLA DOMANDA DI `B2` E' NO:** l'ipotesi che *«la variazione di
`E+ + E-` sia compensata dal termine del vuoto»* ### **non e' cio' che succede** — la
correlazione e' **`+0.10`**, non `-1`. ### ✅ **E NON HO CERCATO UNA COMBINAZIONE
DIVERSA finche' tornava:** il mandato lo vieta, e sarebbe **lo stesso errore della
candidata corrente di ieri** *(costruire la risposta invece di misurarla)*.

### ⚠ **E le correlazioni sono FRA LE VARIAZIONI, non fra i valori**, e conta: due
grandezze che derivano insieme hanno **valori** correlati ### **anche quando le loro
variazioni non c'entrano niente.**

---

## 5. `B3` — **LA CANDIDATA CARICA: nessuna si conserva**

| la candidata | scala | escursione | relativa | |
|---|--:|--:|--:|---|
| `Q = N+ - N-` | `28.08` | `2.024e+01` | `7.21e-01` | ### ⛔ **NON conservata** |
| `Im<psi\|W psi>` | `9.888` | `1.180e+01` | `1.19e+00` | ### ⛔ **NON conservata** |
| `somma_k h_k` | `16.82` | `6.314e+01` | `3.75e+00` | ### ⛔ **NON conservata** |

### ⭐ **MA `Im<psi|W psi>` SEGUE `Q` A `-0.944`**, e l'idea del mandato *(«`Im` e' DISPARI
in `omega`, cioe' assomiglia a una carica»)* ### **si vede nei numeri.** ### ⚠ **E il
perche' e' strutturale, non un indizio:** `Im<psi|W psi> = - somma |c_k|^2 sin(omega_k)`, e
`sin(omega)` e' **positivo sulla banda `+` e negativo sulla `-`** — quindi `Im<psi|W psi>`
e' ### **un `-Q` PESATO con `sin(omega_k)`.** ### **Il `-0.944` invece di `-1` e' proprio
quel peso**, e il segno e' una convenzione.

### ⛔ **QUINDI NON HO UNA CARICA**, e non ne propongo una: ### **le due candidate sono la
stessa cosa a meno di un peso, e nessuna delle due si conserva.**

---

## 6. ⚠ IL LIMITE, DICHIARATO — **tutto questo e' GLOBALE**

### ⛔ **`P+` e `P-` sono PROIETTORI SPETTRALI:** si ottengono **diagonalizzando `W` su
tutta la scena**, a costo `O((4m)^3)` in tempo e `O((4m)^2)` in memoria *(qui `4m = 64`,
`0.062` MB)*. ### **Ogni grandezza <<per banda>> e' definita GLOBALMENTE.**
### ✅ **Trovarne una forma locale e' un passo successivo, da proporre a Luca e non da fare
qui** — e il mandato lo dice con queste parole.

### ⚠ **E CHE COSA NON HO MISURATO, e lo dico:**

1. **la scena del banco congelato** *(`4m ~ 830`)*: ho misurato su **un anello di `16`
   nodi** *(`4m = 64`)*. ### **Il settore `0` vuoto potrebbe essere una proprieta'
   dell'anello**, non del simulatore — e il mandato avvertiva proprio che i Grover hanno
   *«tipicamente grandi autospazi degeneri»*.
2. **un seme solo** *(`7`)* per ogni punto.
3. **la deriva di `db328b9` in `SU(2)`**: quella misura e' fatta con `U(2)` generico.
   ### ⚠ **Non credo che la conclusione cambi** *(la causa e' il termine del vuoto, che
   dipende da `h_k`)*, ### ⛔ **ma non l'ho misurato e quindi non lo affermo.**
