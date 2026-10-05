# REFERTO -- `Z43`: **LA COERENZA DI COMPTON NEL POSTO GIUSTO (`C2`)**

*(correzione del guardiano del 2026-10-05 al mandato `Z43` passo (1). Strumento
**`7b71aa48`**, committato **prima di girare** in
`6bc1cd9`; il referto del passo (1) e' `doc/REFERTO_z43_tempo_proprio_2026-10-05.md`,
in `66a798d`, e ### **non e' stato buttato: e' ANNOTATO.**)*

> ### ⛔ **IL GUARDIANO AVEVA RAGIONE, E CAMBIARE LA GRANDEZZA RIBALTA IL
> ### RISULTATO.**

## IL PERCHE' DI QUESTA MISURA, in tre righe

Il mandato chiamava `C1` *<<l'angolo di rotazione>>*. ### **E' sbagliato, e l'ha
scoperto il COLLAUDO dello strumento** *(`d190dd5`)*: `C1` *(Fubini-Study)* misura lo
### **spostamento del VETTORE DI BLOCH**, e una rotazione **attorno al Bloch stesso**
e' ### **pura FASE** e lascia `C1` a **zero**.
### ⛔ **E l'orologio di Compton E' una fase:** `_phc = exp(-0.5j*_sk*omega_clk*_dts)`
*(`:5971`)*. ### **Vive in `C2`, non in `C1`.**

## ✅ IL RISULTATO: **l'ipotesi nulla e' RIFIUTATA su `C2`** *(era accettata su `C1`)*

| | `C1` *(il posto SBAGLIATO)* | `C2` *(il posto GIUSTO)* |
|---|--:|--:|
| nodi | `13 912` | `13 912` |
| `CV` della grandezza da sola | `3.5824` | `11.7265` |
| `CV` del rapporto con `cs` da `rho_spin` | `4.6944` | `7.9895` |
| ### **`CV(rapporto)/CV(grandezza)`** | ### **`1.3104`** | ### **`0.6813`** |
| l'ipotesi nulla *(`>= 1`)* | ### **ACCETTATA** | ### **RIFIUTATA** |

> ### **IL VALORE SOTTO IPOTESI NULLA ERA SCRITTO PRIMA** *(task history `12ab7f4`)*:
> *<<se le due grandezze sono indipendenti, `CV(rapporto)^2 ~ CV(a)^2 + CV(b)^2`, quindi
> il rapporto delle `CV` e' **`>= 1`**>>*.
> ### ✅ **MISURATO SU `C2`: `0.6813`. E' SOTTO `1`, e l'ipotesi nulla la VIETA.**
> ### **Dividere `C2` per `cs` CANCELLA varianza invece di aggiungerla: la fase e `cs`
> ### raccontano, in parte, la stessa storia.**

### ⚠ **MA NON SCRIVO <<ECCO LA `f0`>>, e il perche' e' nel numero stesso**

La tabella che avevo fissato **prima** aveva tre casi: `>= 1` *(nulla)*, `<< 1`
*(candidato `f0`)*, `~1` *(indeciso)*. ### **`0.6813` NON e' `<< 1`: e' una riduzione del `31.9%`.**
### **Una `f0` vera darebbe una `CV` quasi NULLA** -- qui la `CV` del rapporto resta `7.99`, cioe' ### **ancora enorme in assoluto.**

> ### **LA LETTURA ONESTA: l'indipendenza e' esclusa, la proporzionalita' NON e'
> ### dimostrata.** ### **C'e' una relazione, e non e' quella di una costante.**

### ✅ **E L'AVVERTENZA SULLA SATURAZIONE, che avevo scritto PRIMA, e' ESCLUSA**

Avevo scritto che *<<se le due grandezze saturassero entrambe, il rapporto sarebbe
costante perche' sono due costanti>>*, e che ### **una `CV` bassa per saturazione
sarebbe un FALSO-UNO a favore dell'ipotesi.**

| | mediana | max |
|---|--:|--:|
| `C4` al tetto *(`cs` da `|psi|^2`)* | `0.000000` | `0.000468` |
| `C4s` al tetto *(`cs` da `rho_spin`)* | `0.000000` | `0.000468` |
| `CV` del rapporto, in assoluto | `7.9895` | -- |

### **Le frazioni in saturazione sono `~0`, e la `CV` del rapporto NON e' vicina a
zero.** ### **Il `0.681` non e' saturazione: e'
una relazione.**

## ⛔ **LE DUE DENSITA' DANNO LO STESSO RISULTATO, e questo e' un dato per `(d)` e
## `(d')`**

| `cs` calcolata da | `CV` del rapporto | ### `CV(rapporto)/CV(abs(C2))` |
|---|--:|--:|
| **`|psi|^2`** *(il campo scalare, cio' che il codice usa)* | `7.9842` | ### **`0.6809`** |
| **`rho_spin`** *(la densita' spinoriale)* | `7.9895` | ### **`0.6813`** |

> ### **I due numeri differiscono di `4.6e-04`: SONO LO STESSO RISULTATO.**
> ### **QUALE DENSITA' si usi per `cs` NON cambia la coerenza con la fase.**

### 📌 **E questo si incrocia con un numero del referto del passo (1):** li' le due
densita' davano `cs` con ### **dispersioni molto diverse** *(`p95/p5` `1.871` contro
`1.242`)*. ### **Quindi `rho_spin` da' un `cs` piu' uniforme MA non piu' (ne' meno)
legato alla fase.** ### **Per la via `(d')` sono due fatti separati, e vanno pesati
separatamente: la DISPERSIONE cambia, la COERENZA no.**

## ✅ **QUANTO `C2` SEGUE LA LEGGE CHE L'OROLOGIO GIA' SCRIVE**

    attesa = -0.5 * _sk * omega_clk * _dts / DT  =  -0.5*coerenza*(cs/CS_M)^2*r^2

### **E l'attesa NON e' ricalcolata: e' LETTA dalle variabili della legge** al sito di
`:5971`. ### **Ricalcolarla da `coerenza`, `cs` e `r` sarebbe una SECONDA SCRITTURA**
*(`9-ter`)*, e quella seconda scrittura ### **potrebbe divergere proprio dove il
confronto conta.**

| | correlazione | pendenza |
|---|--:|--:|
| **per nodo** | `0.5249` | `0.3489` |
| ### **IN MEDIA LOCALE** *(la riga pertinente)* | ### **`0.8668`** | ### **`0.6526`** |

### ⛔ **PERCHE' LA SECONDA RIGA E' QUELLA PERTINENTE, e lo avevo dichiarato prima
### di misurare:** `psi_spin = W@(amp*_psi_spinor)/(1+GAMMA*norm)` *(`:6240-6242`)* e'
### **IL CAMPO EMESSO**, cioe' una **somma sui vicini**. ### **La fase che un nodo
mostra NON e' la sua: e' la somma di quelle dei suoi vicini.** ### **Quindi la relazione
per nodo NON PUO' valere, e la media locale e' l'unico confronto sensato.**

> ### ✅ **IN MEDIA LOCALE LA CORRELAZIONE E' `0.867`:** ### **l'orologio spiega la
> ### maggior parte della fase.**
> ### ⚠ **MA LA PENDENZA E' `0.653`, NON `1`:** ### **l'orologio contribuisce, e non e' tutto.** L'altro contributo
> sta nella **rotazione `SU(2)`** *(`omega_tot` a `:5929-5941`)*, che questa misura
> ### **non separa.**

**E LE MEDIANE, che dicono la stessa cosa da un'altra parte:**

| | |
|---|--:|
| attesa dell'orologio, mediana delle mediane | `-7.5834e-03` |
| `C2` misurato, mediana delle mediane | `-3.4130e-03` |
| rapporto | ### **`0.4501`** |

### **Stesso SEGNO** *(entrambe negative, come `exp(-0.5j...)` impone)*, e `C2` e' il
### **`45.0%` dell'attesa in modulo** --
coerente con la pendenza `0.653`.
### **Due vie indipendenti danno lo stesso fattore: non e' un artefatto della
regressione.**

## ✅ L'AGGIUNTA E' INERTE SU CIO' CHE NON TOCCA, e si verifica

| | referto `66a798d` *(`c5ab986a`)* | questa corsa *(`7b71aa48`)* |
|---|--:|--:|
| `FEDELTA'`: nodi confrontati | `1 925 384` | `1 925 384` |
| `FEDELTA'`: differenze | `0` | `0` |
| rapporto dispari/pari di `C0` | `7.185` | `7.185` |
| rapporto dispari/pari di `C1` | `1.081` | `1.081` |
| rapporto dispari/pari di `C2` | `4.276` | `4.276` |

### **Identici.** ### **E non e' una formalita': se l'aggiunta avesse mosso un bit, il
confronto fra il risultato su `C1` e quello su `C2` sarebbe stato fra due corse
diverse** -- e la conclusione *<<cambiare la grandezza ribalta il risultato>>*
### **sarebbe stata indistinguibile da <<cambiare lo strumento ribalta il risultato>>.**

## ⚠ IL LIMITE, lo STESSO del passo (1) e sempre MIO

Il confronto `C2` contro l'attesa esce su ### **`66` passi su `148`**, e la coerenza su `12 813` nodi su `13 912`.
### **IL PERCHE' E' IL DIFETTO CHE HO GIA' DICHIARATO:** gli array che il mio gancio
conserva *(la copia di `cs`, e ora l'attesa della fase)* ### **non si estendono con la
mitosi**, quindi quando `n` cresce fra il sito e `ritmo()` la lunghezza non torna e il
passo si salta.
### **E' la stessa classe di `_cs_nodo_prev` e `_psi_spin_prec` che il file documenta --
l'ho fatta io, in piccolo, DUE VOLTE. VA IN CODA, e ora e' un difetto che si ripete.**
### ✅ **E non falsa il confronto `C4` contro `C4s`, ne' quello con l'attesa:** sono
### **sugli stessi passi e nello stesso istante.**

## CHE COSA QUESTA MISURA **NON** DICE

1. ### **non dimostra una `f0`:** esclude l'indipendenza, ### **non dimostra la
   proporzionalita'** -- `0.681` non e' `<< 1`;
2. ### **non separa l'orologio dalla rotazione `SU(2)`:** la pendenza `0.653` dice che ### **manca un terzo circa**,
   e dove sta ### **non e' misurato qui**;
3. ### **non dice quale esponente sia giusto:** l'attesa e' letta con l'esponente `2`
   che la legge **usa oggi**, e ### **l'esponente resta una DECISIONE DI LUCA**;
4. ### **non riapre il risultato del passo (1):** l'altalena vive nella **base**, e
   quello ### **resta.** ### **Questa misura aggiunge che la FASE -- la parte che
   alterna -- segue l'orologio in media locale.**

## E CHE COSA I DUE REFERTI, INSIEME, DICONO

> ### **Il passo (1): l'altalena NON e' nella rotazione del Bloch (`1.08`), e' nella FASE (`4.28`) e nella BASE (`9.24`).**
> ### **`BRACCIO A`: togliere UNA potenza di `r` dall'orologio la fa sparire** *(`5.28` -> `1.034`)*.
> ### **E questo referto: la FASE segue l'orologio in media locale con correlazione `0.867`.**
> 
> ### ⛔ **I TRE PEZZI COMBACIANO: l'orologio scrive la fase, la fase e' cio' che
> ### alterna, e `ritmo()` legge la fase.**
> ### ⚠ **MA <<combaciano>> NON e' <<quindi la cura e' X>>:** ### **la forma di `r`
> ### resta una DECISIONE DI LUCA**, e le sei vie restano riportate ### **senza che io
> ### ne scelga una.**

## LA PIATTAFORMA E LA CONFIGURAZIONE

`python 3.13.2` · `numpy 2.3.0` · Windows 11 · AMD64. Configurazione: **`81`** booleani, ### **`ZERO` differenze dal driver**.

### ⚠ **E UN FLAG CHE IL REFERTO DEVE DICHIARARE, perche' l'attesa ne dipende:**
`OROLOGIO_SEGNO` e' ### **`False`**, quindi `_sk = 1` per
tutti. ### **Se fosse acceso, `_sk` sarebbe `+/-1` per nodo e l'attesa cambierebbe
segno sulla meta' antimateria.** Lo strumento legge `_sk` **dalla legge**, quindi lo
seguirebbe -- ### **ma il numero qui vale per `_sk = 1`.**
