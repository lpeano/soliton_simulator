# `H_w` — **LA MISURA CHE SEPARA LE STRADE DI `DOMANDA-QUALE-INVARIANTE-CON-CS`**

> ### 📌 **Mandato del guardiano del `2026-10-17` alle `22:08`, su mandato di
> Luca.** ### ⛔ **NON sceglie fra le letture `(a)` `(b)` `(c)`:** fa una misura che
> le ### **separa**, e registra due candidate nella mappa. ### **`D4` resta bloccato, e
> lo STOP dopo `D3` resta.**

> ### ⛔ **E QUESTO FILE SI COMMITTA PRIMA DEL CODICE**, cosi' l'ordine e'
> ### **verificabile da `git`** invece che asserito da me.

---

## 0. LA STELLA POLARE — *rimanda, e dice PERCHE'*

### ⛔ **QUESTA MISURA NON CAMBIA NESSUNA LEGGE E NON TOCCA IL PASSO:** costruisce
### **una FUNZIONE DI MISURA** *(`H_w`)* e ne guarda la pendenza. ### **Le cinque
risposte sono quelle di `D`**, e una seconda copia potrebbe solo divergere.
### ⚠ **E se `H_w` reggesse, NON ne seguirebbe che il passo va cambiato:** seguirebbe
che ### **esiste un'energia pesata coerente col modo in cui il passo usa `cs`** -- e
### **che cosa farne lo decide Luca.**

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo, e cosa NON so*

### ⭐ **I PESI CHE IL PASSO USA, letti dal codice e non supposti** *(`flussi_parziali`)*:

| il pezzo | che peso legge | dove |
|---|---|---|
| `CAMM-GROVER` *(`psi`)* e `CAMM-GROVER-VUOTO` *(`phi`)* | ### **`s_nodo`** | `FP.grover` -> `z_nodo` |
| `CAMM-MONETA-SPIN` | ### **`dtau_nodo`** per estremita' | `motore._moneta_spin` |
| `CAMM-MATERIA-VUOTO` | ### **`dtau_nodo`** | `materia_vuoto.applica` |
| `CAMM-SPOSTAMENTO` *(`psi`)* e `CAMM-SPOSTAMENTO-VUOTO` *(`phi`)* | ### **`s_arco`**, la media ARMONICA di `B-3` | `FP.hop_psi` / `hop_phi` -> `z_arco` |

### ✅ **Quindi i termini di `h_tot` si dividono in DUE gruppi, e non e' una scelta
mia:** ### **nodo** *(i due Grover, la moneta, l'accoppiamento `N`)* e ### **arco**
*(i due spostamenti)*. ### **E' la mappa pezzo -> peso, letta dal sorgente.**

### ⭐ **COME SI PRENDONO I PESI, e perche' cosi':** ### **dal passo stesso**,
`w_nodo = s_nodo(con cs) / s_nodo(senza cs)` e `w_arco = s_arco(con cs) / s_arco(senza
cs)`. ### ✅ **Non riscrivo la media armonica:** chiamo la stessa funzione che il
passo chiama. ### ⛔ **Una mia copia della formula sarebbe una SECONDA FONTE della
legge**, ed e' quello che `STRUMENTO-LEGGE-DALLA-TABELLA` vieta.
### 📌 **E il rapporto e' esattamente `cs_k` sul nodo e `armonica(cs_i, cs_j)`
sull'arco**, perche' la media armonica e' ### **omogenea di grado `1`** -- ma
### **non lo scrivo come formula: lo misuro col rapporto.**

### ⛔⛔ **CHE COSA CREDO, PRIMA DI GUARDARE**

### `1)` **Credo che `(a)` REGGA, e il motivo e' preciso:** con `cs` ### **CONGELATO** il
generatore ### **non dipende dal tempo** *(`cs` non cambia)*, quindi il passo e' lo
### **Strang di un generatore FISSO** -- e lo Strang di un generatore fisso conserva
### **l'energia DI QUEL generatore** al secondo ordine. ### **La diagnosi di `D3` lo ha
gia' mostrato nel caso uniforme** *(`1.951` e `2.009`)*, e il caso congelato non uniforme
e' ### **lo stesso argomento con pesi diversi.**
### ⚠ **MA NON LO SO, e c'e' una ragione per dubitarne:** il peso dell'arco e'
### **una media armonica dei due capi**, e ### **non e' affatto detto che il generatore
che il passo integra sull'arco sia `w_a` volte il generatore d'arco di `h_tot`.** ### **Se
non lo e', `(a)` cade** -- e quella sarebbe ### **la risposta piu' informativa delle
due.**

### `2)` **Credo che `(c)` NON regga**, perche' con `cs` dinamico il generatore
### **cambia durante la corsa** e nessuna funzione dello stato e' conservata per
costruzione. ### ⚠ **Ma la pendenza potrebbe essere `1` invece di `0`**, e la
differenza conterebbe: ### **`1` vorrebbe dire <<secondo ordine rotto dalla dinamica>>,
`0` <<nessuna convergenza affatto>>.**

### `3)` **Il caso `(d)` mi aspetto che fallisca FORTE**, perche' la media aritmetica e
quella armonica ### **differiscono solo dove i due capi sono DIVERSI** -- e la scena ha
`cs` da `0.13` a `0.75`, quindi i capi sono molto diversi.
### ⛔ **E se `(d)` NON fallisse, la misura non distinguerebbe i pesi**, cioe'
### **non misurerebbe quello che dice di misurare**: e' il motivo per cui il mandato lo
chiede.

### ⛔ **CIO' CHE NON SO E NON INDOVINO:** `H_w` ha bisogno dei ### **termini di
`h_tot` SEPARATI per nodo e per arco**, e `h_tot` oggi ### **restituisce UN numero.**
### ⚠ **Quindi serve una funzione nuova che li renda a pezzi** -- e
### **`h_tot` NON SI TOCCA**, perche' il suo valore e' ### **il criterio di `M-B2`** e una
somma in ordine diverso ### **cambia i bit.**
### ✅ **La funzione nuova e' una SECONDA FONTE DICHIARATA, e si confronta con
`h_tot` A OGNI CORSA** *(a `cs` uniforme `1`, dove le due devono dare lo stesso numero a
meno dell'ORDINE DELLA SOMMA)* -- come il mandato chiede.

---

## 2. PROGETTAZIONE — *i passi, e i criteri FISSATI QUI*

### ⛔ **NESSUNA BANDA NUOVA:** la soglia della pendenza e' ### **`1.9`, quella di
`M-B2`**, e i dimezzamenti sono ### **`>= 4`** come in `D3`.

| | il braccio | che cosa DECIDE | cosa mi FERMA |
|---|---|---|---|
| `0` | la seconda fonte: a `cs = 1` uniforme `H_w` e' `h_tot` | che `H_w` sia ### **la stessa energia**, non un'altra | una differenza che ### **non si spieghi con l'ordine della somma** |
| `b` | `cs` UNIFORME: le pendenze di `H_w` e di `H_tot` ### **coincidono** e sono `>= 1.9` | il ### **controllo positivo**: senza, un `(a)` verde non direbbe niente | una delle due ### **sotto `1.9`** |
| `a` | `cs` CONGELATO non uniforme: la pendenza di `H_w`, ### **accanto a quella di `H_tot`** | ### **LA DOMANDA DEL MANDATO** | ### **nulla: qualunque numero e' la risposta**, e si riporta |
| `c` | `cs` DINAMICO *(al centro, come `D2`)*: la pendenza di `H_w` | ### **informazione**, non criterio | nulla |
| `d` | il caso che DEVE fallire: ### **media ARITMETICA** sugli archi | che la misura ### **distingua i pesi** | se ### **NON fallisce**, la misura non guarda i pesi: ### **si ferma e si dice** |

### ✅ **LA LETTURA, scritta QUI e non dopo i numeri** *(e' il mandato che la fissa)*:
### ⛔ **se `(a)` REGGE e `(c)` NO**, il pesaggio e' ### **coerente**, e cio' che
rompe e' ### **solo la dinamica di `cs`**;
### ⛔ **se `(a)` NON REGGE**, gia' ### **il modo in cui il passo usa `cs` non
corrisponde a nessuna energia pesata.**
### ⚠ **E in entrambi i casi NON si decide niente:** la scelta fra le cinque strade
e' di Luca.

---

## 3. TODO DEL NEXT STEP

1. `pezzi_di_h` in `_misura_mb2.py` *(i termini per nodo e per arco)*, ### **senza
   toccare `h_tot`**, e il confronto a `cs = 1` come braccio `0`.
2. `_misura_hw.py`: i cinque bracci, con i pesi presi ### **dal passo**.
3. Il referto ### **dal blob committato**, la `RIPRESA`, la relazione.
4. Le due candidate ### **nella mappa** *(`(d)` accoppiamento hamiltoniano, `(e)` rigidita'
   del vuoto)*: ### **si collocano, NON si attuano.**
5. I numeri ### **nella voce**, con le cinque strade e il loro costo. ### **La scelta
   resta a Luca.**
6. ### ⛔ **E un mio commento FALSO da correggere** *(trovato rileggendo il codice per
   questo lavoro)*: in `_collauda_cs_l1.py` ho scritto che il motore ### **azzera `cs` a
   fine tick.** ### **Non e' vero**, e l'ho verificato: `mot.cs` ### **sopravvive al
   tick, intatto.**