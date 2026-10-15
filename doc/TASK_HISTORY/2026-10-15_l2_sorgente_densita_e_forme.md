# `L2` — TERZO PEZZO: **la sorgente e' la DENSITA'**, e le quattro forme si misurano

> **Decisioni di Luca del 2026-10-15** *(`19:25`–`19:34`)*. Ultimo commit verificato dal
> guardiano: `d9406b6`. ### ⛔ **Il motore NON si tocca.**
>
> ### **E si scrive prima del codice** *(§8)*.

---

## 1. RAGIONAMENTO PRELIMINARE

### ⭐⭐ **LA DERIVAZIONE DEL GUARDIANO LA SO CHIUDERE A MANO, ED E' PIU' FORTE DI COME E'
SCRITTA NEL MANDATO**

Con `N = Lambda · F(x)` e `x = rho/Lambda` *(omogeneo di grado `1`: la scala viene dal
vuoto locale, **nessuna costante**)*:

```
alpha = dN/drho   = F'(x)
beta  = dN/dLambda = F(x) - x F'(x)
beta'(x) = F' - F' - x F'' = - x F''  =  - x alpha'(x)        <- L'IDENTITA'
```

### ⭐ **E la conseguenza NON e' solo asintotica: e' un SE E SOLO SE, e si prende risolvendo
un'equazione differenziale.** Se `beta` e' **esattamente lineare**, `beta = -c x`:

```
F - x F' = -c x        ==>   (F/x)' = (x F' - F)/x^2 = c/x
                       ==>   F/x = c ln x + k
                       ==>   F = c x ln x + k x
                       ==>   alpha = F' = c ln x + (c + k)
```

> ### ⛔⛔ **`beta` ESATTAMENTE LINEARE  <==>  `F = c x ln x + k x`  <==>  `alpha`
> LOGARITMICA.** ### **Non e' <<obbliga>>: e' <<equivale>>.**

### ✅ **E il verso inverso dell'implicazione:** se `alpha` e' **limitata e Lipschitz**
*(cioe' `alpha'` limitata)*, allora `beta' = -x alpha' -> 0` per `x -> 0`, quindi
### **`beta` NON puo' essere lineare fino a zero.** ### 📌 **L'ipotesi <<Lipschitz>> la
dichiaro:** con `alpha` limitata ma `alpha'` che oscilla come `1/x` il conto non si chiude,
e ### **non voglio enunciare un teorema piu' largo di quello che dimostro.**

### ⚠ **Quindi il <<non esiste una `F` che dia entrambe>> del mandato e' VERO, con quella
ipotesi** — e lo verifico **con `sympy`**, non a mano soltanto.

### ⭐ **E CON `rho` AL POSTO DI `h` IL FLUSSO SU `psi` CAMBIA NATURA**

`rho = somma_h |psi_h|^2`, quindi `dN/dpsi_h^* = alpha · psi_h` ⟹

```
dpsi_h/dt = -i alpha psi_h        <-  UNA FASE, non una rotazione attorno a n
```

### ✅ **E una fase NON cambia `rho`:** ### **la sorgente e' conservata dal termine che la
usa.** ### ⚠ **Con `h` invece `dh/dpsi^* = (sigma.n) psi`, cioe' una ROTAZIONE** — ed e'
cio' che il motore fa oggi *(`_ruota_attorno_a_n`)*.

### ⛔ **CIO' CHE NON SO**

1. **se `S4` ha una `F` in forma chiusa.** `alpha = pi - 2pi/(1+x^p)` ⟹
   `F = pi x - 2pi integrale_0^x dt/(1+t^p)`, e quell'integrale e' **ipergeometrico**:
   `x · 2F1(1, 1/p; 1+1/p; -x^p)`. ### **Lo verifico contro una quadratura numerica**, e
   se non torna uso la quadratura.
2. **se il verso resta OPPOSTO con `rho`.** Il pezzo precedente l'ha misurato con `h`;
   ### **cambiare sorgente puo' cambiare il segno**, e non lo so prima.
3. **dove il cono morde.** `alpha` di `S2` e `S3` **diverge** per `rho -> 0`, quindi
   `|alpha| dtau` supera `pi` **da qualche parte**: ### **la domanda e' se la' lo STATO
   cambia tanto**, e il mandato dice di misurare **entrambe** le cose.
4. **se la figura tiene di piu'.** La letteratura ha soluzioni localizzate stabili per
   l'equazione logaritmica, ### **ma io misuro SOLO la larghezza nel tempo** e
   ### **non dichiaro nessun legame.**

---

## 2. PROGETTAZIONE — *i passi, cosa decide ciascuno, cosa mi FERMA*

| | il passo | **che cosa decide** | **cosa mi FERMA** |
|---|---|---|---|
| `1` | **`_deriva_forme_l2.py`**: `sympy` verifica `alpha`, `beta`, **l'identita'** `beta' = -x alpha'`, e il **se e solo se** del logaritmo | se la derivazione regge | l'identita' che non torna → **tutto il resto cade** |
| `2` | le **quattro forme** `S1`–`S4` derivate e tabulate, con gli **attesi del mandato** verificati | le formule da usare nella misura | un atteso che non torna *(per es. `S4` non `~x^1.64`)* → lo riporto, non lo aggiusto |
| `3` | **la sostituzione a runtime del termine**, con `rho` al posto di `h` e **una FASE** su `psi` | la misura | ### ⛔ **il motore NON si tocca:** si sostituisce `mot.operatori[...]`, come si e' fatto col segno di `beta` |
| `4` | **il VERSO** `E` con la barra, `>= 3` barre | il verso per ogni forma | — |
| `5` | **l'INDIPENDENZA DALLO SPIN**: `+1`, `-1`, isotropo **alla stessa densita'** | se la sorgente `rho` ripara cio' che `h` rompeva | una differenza fuori barra → la sorgente `rho` **non** basta, e lo dico |
| `6` | **l'ESPONENTE** su `x = 0.01 .. 2` | la linearita' | — |
| `7` | **IL CONO, nei DUE modi**: `|alpha| dtau` contro `pi`, **e** `max|dpsi|`, `somma|dpsi|^2` | se il cono morde **davvero** | — |
| `8` | **la LARGHEZZA del grumo** nel tempo | se la figura tiene | — |
| `9` | il **controllo nullo**: termine spento → `dLambda = 0` esatto | che la misura non guardi rumore | `!= 0` → la misura e' rotta |

### ⛔ **LE TRE COSE CHE NON FACCIO**
1. **non tocco il motore** *(il mandato lo dice due volte)*;
2. **non decido la forma**: `S1`–`S4` si **misurano**, e la scelta e' di Luca;
3. **non dichiaro nessun legame** fra la larghezza del grumo e la letteratura: ### **misuro
   la larghezza, e basta.**

---

## 3. LA STELLA POLARE — **cinque risposte, PRIMA del codice**

| | la risposta |
|---|---|
| **1. `A14`, conserva localmente?** | ### ⭐ **E con `rho` c'e' una cosa NUOVA e buona: il termine conserva LA SUA SORGENTE.** Il flusso su `psi` e' **una fase**, e una fase **non cambia `rho`** — mentre con `h` il flusso era **una rotazione**, che `h` **lo cambia**. ### ✅ **Lo verifico come braccio:** `rho` invariante all'ulp sotto il solo termine. ### ⚠ **E il vuoto TOTALE resta conservato dalla camminata**, come nei pezzi prima. |
| **2. a quale GRADINO arriva?** | **`(a)`**, e il punto `1` arriva piu' in alto: ### **una verifica SIMBOLICA** *(`sympy`)*, che non e' una misura ma **un conto controllato da una macchina.** ### ⛔ **NON `(c)`**, e l'esponente serve proprio a dire **quanto si e' lontani** dal lineare. |
| **3. aggiunge un numero o una legge?** | ### ⚠⚠ **QUI VA DETTA UNA COSA CHE NON MI PIACE:** `S2`, `S3` e `S4` **non sono la saturazione di oggi** — sono **forme NUOVE**, e metterne una in tabella vorrebbe dire **cambiare una legge.** ### ✅ **In QUESTO pezzo non ne metto nessuna:** vivono **dentro lo script**, come sostituzioni a runtime, e ### **la tabella non si tocca.** ### 📌 **E `S4` ha una SCELTA dentro: la FORMA `tanh`.** La scala viene da `pi` *(il cono)*, ma **la forma e' una scelta**, e Luca lo dichiara: ### **la registro come tale, non come derivazione.** |
| **4. tocca `rho`, `c_s` o il SEGNO?** | ### **Tocca `rho` DIRETTAMENTE: la decisione e' che `rho` E' la sorgente.** E tocca il **SEGNO** perche' il verso si rimisura. ### ⛔ **`cs` NON e' ancora accoppiato a `Lambda`.** |
| **5. emergente o imposto?** | ### ⭐⭐ **La cosa piu' importante del pezzo e' che IL PRINCIPIO DI LINEARITA' E' UN REQUISITO IMPOSTO DA FUORI**, non un risultato: Luca lo chiede **perche' una figura deve gravitare per la sua MASSA e non per la sua struttura** *(«guarda la luna, non il dito»)*. ### ⛔ **E il conto del punto `1` dice che quel requisito HA UN PREZZO: `alpha` logaritmica.** ### **Non si puo' avere la linearita' E un `alpha` limitata** — e questo **non e' emergente ne' imposto: e' una COSTRIZIONE**, cioe' la cosa piu' utile che un conto possa dare. |

---

## 4. TODO DEL NEXT STEP

1. `primo_ordine/_deriva_forme_l2.py`: `sympy` per l'identita', il **se e solo se** del
   logaritmo, e le quattro forme con gli attesi del mandato.
2. `primo_ordine/_misura_forme_l2.py`: la sostituzione a runtime *(il motore resta com'e')*,
   il verso, l'indipendenza dallo spin, l'esponente, **il cono nei due modi**, la larghezza.
3. I referti **nuovi** in `doc/referti_l2/`, accanto ai vecchi; `RIPRESA` e mappa.
   Poi **STOP**: la forma e' una decisione di Luca.
