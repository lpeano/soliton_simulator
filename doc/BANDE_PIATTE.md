# LE BANDE PIATTE: IL MENU PER LA DECISIONE *([[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il mandato di Luca delle `19:12` del `2026-10-29`)*

> **Il documento NON sceglie: la decisione fra `(A)`, `(B)`, `(C)` e' di Luca.**
> **I numeri:** `doc/referti_l2/bande_piatte.txt` *(`python csv/_bande_piatte.py --referto`, lo script `sha1-BYTE 3d62588b`, `919b610a`; `5/5`)*; il task history `doc/TASK_HISTORY/2026-10-29_bande_piatte_menu.md` *(`c4fe2712`)*.
> **Il quadro:** il tick libero di `S1`, `L 81`, la convenzione `simm` degli strumenti; le energie per unita' di tempo, `-arg(lambda)/s`; `s 0.15` dove non e' detto.

## 0. DA DOVE SI PARTE *(`99b679bc`)*

- Il modo instabile del solitone di `S1` decade in coppia `P0 + Ppi`; il tasso dipende dalla **somma** degli spostamenti delle due piatte *(in direzioni opposte resta `0.1506`)*; nella stessa direzione il modo si spegne fra lo scarto `-0.1` e `-0.4` e fra `+0.4` e `+1.6`; una piatta sola a `+0.8` lo spegne.
- **Un fatto del codice che vale per tutto il filone:** in tutte le scene di `S1` misurate fin qui **`eps = 0`** *(`_solitone_vuoto_congelato.corsa`)*: **la moneta di spin e' spenta**, mentre la tabella ha `eps 0.5`.

## 1. IL PUNTO DI MEZZO: NON E' UNA SIMMETRIA

**Il tick libero della materia** *(dal codice: `composizione.ORDINE`, i pezzi della materia, a `eps 0` la moneta e' l'identita' e il legame lo e' a `rho -> 0`)* e' `T = G S S G`, coi mezzi pezzi `G = exp(-i s (alpha/4)(2 P_u - I))` e `S = exp(-i s (beta/4) R_S)`; **oggi `alpha = beta = pi`.** Il tick ricomposto dai pezzi ridà `A(k)` entro `9.0e-16`.

**Al primo ordine in `s`**, `H1 = (alpha/2)(2 P_u - I) + (beta/2) R_S`:

| che cosa | la formula | misurato *(lo scarto dal primo ordine)* |
|---|---|---|
| `P0`, `Ppi` *(su `ker P_u`)* | `(-alpha ± beta)/2` = `0`, `-pi` | piatte **esatte a ogni `s`**: `7.3e-15`, `7.5e-15` |
| `A`, `B` *(su `span(u, R_S u)`)* | `∓(1/2) sqrt(alpha^2 + 2 alpha beta c(k) + beta^2)` | `4.6e-02`, `1.1e-02`, `2.8e-03` a `s 0.3`, `0.15`, `0.075`: i rapporti `4.07`, `4.02` **(`s^2`)** |
| `c(k)` | l'autovalore di `P_u R_S P_u` | in `[-1/2, 1]`; **`c(K) = c(K') = -1/2`** *(il minimo)*; le due componenti di spin uguali |

**Il punto di mezzo, dalla formula:** `E_A(K) = -mu0`, `mu0 = (1/2) sqrt(alpha^2 - alpha beta + beta^2)`; il mezzo fra le piatte e' `-alpha/2`. **Coincidono se e solo se `beta = alpha`** *(`r = beta/alpha = 1`: il `dtau` dell'arco uguale a quello del nodo)*. Quindi il punto di mezzo e' **`r = 1` piu' `c(K) = -1/2`** *(la geometria del triangolo)*; **il palindromo** rende lo scarto di ordine `s^2` *(`de411167`)*.

**Le prove di simmetria dello spettro** *(a tutte e tre le `s`)*:

| la prova | lo scarto massimo |
|---|---|
| `E(k) = E(-k)` | `≤ 1.9e-14` **(vale)** |
| `E -> -E` senza `Ppi`; `A(k) = -B(k)` | `≤ 1.6e-14` **(vale)**: `A` e `B` speculari rispetto a `P0` |
| `E -> -E` con `Ppi`; `E -> -pi - E` *(stesso `k` e `k -> -k`)* | `3.14` **(non vale)** |

**La conseguenza per la risonanza:** lo scarto libero `E_P0 + E_Ppi - 2 E_A(K) = -alpha + 2 mu0` e' **zero al primo ordine a `r = 1`**: due quanti di `A` a `K` stanno esattamente sulla soglia della coppia `P0 + Ppi`. Misurato: `-0.0884`, `-0.0219`, `-0.0055` a `s 0.3`, `0.15`, `0.075` *(`O(s^2)`)*, uguale a `K` e a `K'`.

## 2. CHE COSA TOCCA

| la grandezza | dipende dal punto `1`? | il fatto |
|---|---|---|
| **`Q_S`** e la moneta `eps` | **no** | `[T, sigma_z] = 0` esatto a `eps 0`; `1.46e-1` a `eps 0.5` *(misurato qui; `doc/PROGETTO_U1.md`: `3.2e-15` e `6.3e-2` col tick intero)*. `Q_S` dipende da `eps` e dalla `U` diagonale, non da `r` |
| **la coppia `K`/`K'`** | **si', allo stesso modo** | `c(K) = c(K') = -1/2`; `A(K) = A(K')`; `E(k) = E(-k)`: le due valli hanno lo stesso punto di mezzo e la stessa soglia |
| **`DOMANDA-CHIRALITA`** | **il candidato `(b)` si'** | `(b)` e' il salto della coppia a `K`, `mu0 = (1/2) sqrt(alpha^2 - alpha beta + beta^2)` *(`2026-10-25_curvatura_parte2.md`)*: **e' la stessa grandezza** che con `r = 1` mette `A(K)` a meta'. `(a)` *(la moneta)* e' la strada `(B2)`; `(c)` *(le valli)* sta in `c(k)`, cioe' nella geometria |
| **il cono di luce di `C2`** | **si', attraverso `r`** | il rapporto fra la `c` della materia e quella della luce in `A1` e' `pi/(4 sqrt(r))` *(`b0edae62`)*; la materia nuda a `r = 1` va a `pi/4` della luce *([[DOMANDA-CONO-EMERGENTE]])* |

## 3. LE PIATTE HANNO STATI COMPATTI

| la piatta | il grappolo minimo | gli stati | le traslazioni *(gli stati di due anelli, `19` nodi)* | il proiettore |
|---|---|---|---|---|
| **`P0`** *(isolata: `A` e `B` a distanza `≥ 1.56`)* | **il triangolo, `3` nodi** | `2` *(uno per spin)* | rango **`4` a ogni `k`** | **esiste locale** *(analitico in `k`: decade esponenzialmente; non compatto)* |
| **`Ppi`** *(tocca `A` a `Gamma`)* | **il triangolo, `3` nodi** | `4` | rango `4` a ogni `k` **tranne `Gamma`** *(`2`)* | **non locale da sola:** a `Gamma` mancano `2` stati, quelli dove tocca `A` |

*(Ogni stato trovato soddisfa `T v = lambda v` entro `1.7e-15`; un nodo solo non ne porta nessuno.)*

## 4. LE TRE STRADE, CON IL COSTO *(il documento NON sceglie)*

### (A) TENERLE COME FISICA

- **Che cosa vuol dire:** il modello ha `8` bande piatte su `12`; il solitone fermo e' instabile per il decadimento in coppia, e **il solitone stabile e' lo stato che respira** *(la lista d'attesa `13`: due corse da stati diversi finiscono nello stesso stato largo)*.
- **Il costo:** nessuna legge cambia; **la soglia e' nel modello a `r = 1`**, quindi **ogni oggetto con un livello vicino a `A(K)` vi e' esposto**. La domanda `13` *(lo stato finale comune)* diventa il lavoro.

### (B) ALLONTANARLE ALLA WILSON *(sul tick libero ricomposto in `csv/`)*

> ### ⛔ **FUORI DAL MENU COME CURA** *(decisione di Luca, `2026-10-30` `09:09`: **niente taratura dei pesi del nodo e dell'arco per stabilizzare `S1`**, perche' dipenderebbe da `mu`, dalla forma, da `N`)*; ### **resta scritta come diagnosi.**

| la modifica | lo scarto libero a `K` | `A(K)` | il costo nel punto `2` |
|---|---|---|---|
| **(B1) il rapporto nodo/arco**, `mu0 = pi/2` fisso: `alpha 2.3416`, `beta 3.5702` *(`r 1.5247`)* | **`+0.806`** | `-3.1e-03`; la curvatura di `A` a `K` da `-3.14e-3` a `-2.66e-3` | **un numero nuovo** *(`A1`: `r` non derivato; la somma delle frazioni di una legge non e' piu' `1`)*; il cono *(`pi/(4 sqrt r)`)* cambia con `r`; `mu0` di `(b)` resta `pi/2` per costruzione, ma `alpha` e `beta` cambiano; `Q_S` e le valli intatti |
| idem, `alpha 3.5416`, `beta 2.4508` *(`r 0.6920`)* | **`-0.395`** | `-2.5e-03`; curvatura `-2.76e-3` | idem |
| **(B2) la moneta della tabella**, `eps 0.5` | `+0.161` *(non arriva a `+0.8`)* | **`-7.96e-02`** *(si muove `A`, non la somma delle piatte)* | `Q_S` rotta *(`1.46e-1`)*; le piatte quasi piatte *(larghezze `0.0017`, `0.0029`)*; e' il candidato `(a)` della chiralita' |
| **(B3) un altro ordine palindromo** *(`S G G S`)* | **`0`** *(`< 1e-14`, a `s 0.15` e `0.075`)* | `0` | nessuno, **e non sposta niente:** con due soli pezzi ogni ordine palindromo e' una rotazione ciclica, cioe' lo stesso spettro |
| **(B4) la convenzione** *(`oggi` contro `simm`)* | **`0`** | sposta tutto di `-pi` | nessuno, **e non sposta niente:** una fase globale per pezzo |

- **Quante modifiche minime esistono:** **una famiglia sola, `(B1)`**, che sposta la somma delle piatte di `+0.8` o `-0.4` tenendo `A(K)` entro `3e-3`. `(B2)` sposta soprattutto `A`; `(B3)` e `(B4)` non spostano niente.
- **Il costo di `(B1)`:** un numero *(`r != 1`)* da derivare; tocca il cono di `C2` e il candidato `(b)` della chiralita'; non tocca `Q_S` ne' le valli.

### (C) CAMBIARE IL LEGAME SULLE PIATTE, RESTANDO LOCALE

- **Il fatto del punto `3`:** `P0` ha stati compatti su un triangolo che generano tutta la banda, quindi **un proiettore locale** *(esponenziale, non compatto)*; `Ppi` no, a `Gamma`.
- **La forma, se Luca la sceglie:** il legame `exp(-i alpha(rho/Lambda) dtau)` che sulle componenti `P0` agisce con una fase diversa. **Basta una piatta:** il tasso dipende dalla somma *(`99b679bc`: `P0` sola a `+0.8` spegne il modo)*.
- **Il costo:** una legge nuova *(9-ter: una cura che aggiunge una legge deve dire perche' non si poteva togliere niente)*; **un proiettore a coda esponenziale non e' compatto** *(la scala minima e' un arco, `A13`)*; su `Ppi` la stessa forma non e' locale.

## 5. LA LEZIONE GENERALE: LA REGOLA DEI TRE INCROCI *(Luca, `2026-10-30` `09:09`; ### **UNA REGOLA DA VERIFICARE, NON UNA LEGGE**)*

> **I numeri:** `doc/referti_l2/modo_lento.txt` *(`python csv/_modo_lento.py --referto`, lo script `sha1-BYTE 36ff91ba`, `a3e7100d`; `8/8`)*; il task history `doc/TASK_HISTORY/2026-10-30_lezione_e_modo_lento.md` *(`f2271150`)*. **Nessuna corsa per questa sezione:** il conto lungo il profilo degli stati gia' trovati.

**L'argomento.** `K` sta a meta' fra le piatte *(`r = 1` e `c(K) = -1/2`, `b5fd8ecc`; sezione `1`)*. Un legame **scalare per nodo** che va da `0` *(coda)* a `alpha_max` *(cuore)* sposta **tutte** le bande di ogni valore in `[0, alpha_max]` lungo il profilo. Un oggetto legato a `K` ha `mu = -mu0 + alpha_max + d` *(`d` piccolo)*. Le tre condizioni

- la coppia `(P0 + alpha) + (Ppi + alpha) - 2 mu`,
- c1 su `P0`: `P0 + alpha - mu`,
- c1 su `Ppi`: `Ppi + alpha - mu`

scorrono lungo il profilo per un tratto lungo `alpha_max` *(la coppia `2 alpha_max`)*. **Nel cuore la coppia vale `-a_n + 2 mu0 - 2 d`: a `r = 1` e' `-2 d`, QUALUNQUE sia `alpha_max`**, perche' il legame sposta l'oggetto e la coppia della stessa quantita'. **Quindi, A `r = 1`, per QUALUNQUE oggetto legato a `K` con questo legame la coppia sta sullo zero nel cuore** *(entro `2 d` e la larghezza della risonanza)*. **Fuori da `r = 1` nessuna delle tre incrocia solo se `J` sta fuori dai livelli piatti e dalle loro medie** *(sotto, la regola delle `09:31`)*.

**Il conto sugli stati trovati** *(`S1`, `s 0.15`; `alpha` della coda `0`, del cuore `1.00000`)*:

| `r` | `mu`, `d` | la coppia, coda -> cuore | c1 su `P0` | c1 su `Ppi` | che cosa si misura |
|---|---|---|---|---|---|
| `1` | `-0.566022`, `+0.00477` | `-2.0095 -> -0.0096` *(nessun incrocio: **tocca lo zero nel cuore, a `-2 d`**)* | `+0.566 -> +1.566` | `-2.576 -> -1.576` | **decade**: il tasso `0.139` *(`s 0.3`)*, `D` in `P0 + Ppi` agli anelli `12`-`13` *(`5f06dbfb`; qui al bit)* |
| `0.65` | `-0.568754`, `+0.00204` | `-2.437 -> -0.437` | **`-0.057 -> +0.943`, fra gli anelli `14`-`15`** | `-2.380 -> -1.380` | **`D` in `P0` agli anelli `14`-`15`** *(`ea8ace8f`)* |
| `1.5247` | `-0.568613`, `+0.00218` | **`-1.204 -> +0.796`, fra gli anelli `12`-`13`** | `+1.183 -> +2.183` | `-2.387 -> -1.387` | **il modo lento** *(sotto)* |
| `0.69` *(la fettina TARATA)* | `-0.568234`, `+0.00256` | `-2.407 -> -0.407` | `+0.019 -> +1.019` *(nessun incrocio, a `0.019` dallo zero)* | `-2.426 -> -1.426` | **non misurato** *(la corsa lunga e' in lista d'attesa: tolta come taratura)* |

**Il modo lento a `r 1.5247`** *(`4400` tick dallo stato fermo, al bit con la corsa lunga di `ea8ace8f`)*: la finestra `377`-`621` unita' di tempo, **il tasso `0.0331`** *(nelle sole piatte `0.0310`)*. A `450` e a `535.5` **`D` sta per il `92%` e il `90%` in `P0 + Ppi`, agli anelli `12` e `13`**; all'ultimo istante *(`621`, `|D|/|psi0|` `9.8e-3`, vicino alla saturazione)* la banda `A` pesa `0.507` e entrano gli anelli `7`-`11`. **Le rotazioni delle due parti danno `alpha* = 0.638` *(da `P0`)* e `0.604` *(da `Ppi`)*, contro `0.602` dove la coppia si annulla:** il modo sta dove la coppia incrocia. **La lettura scritta prima chiedeva i tre istanti: ALLA LETTERA `(m2)`** *(il terzo istante non passa)*; i primi due sono `(m1)`. **La decisione su che cosa vuol dire e' di Luca.**

**Le conservazioni nel decadimento** *(il `2bis` delle `09:16`, sui `D` salvati; a `r 1` i `D` di `5f06dbfb` rigenerati al bit)*:

| la grandezza | `r 1.5247` | `r 1` |
|---|---|---|
| **`Q_S`** *(`sigma_z`, `eps 0`)* | `psi0` e' **tutto spin su** *(`q = 1` esatto)*: `N_giu = 0` si conserva, e `D` resta tutto su *(`q(D) - 1` `<= 4e-13`)*. **Il test e' banale.** Alla lettera **TORNA** | stesso fatto *(`q(D) - 1` `<= 8e-9`)*; alla lettera **NON TORNA**: la dispersione fra gli istanti `8.2e-7` e' sotto lo scarto delle parti proiettate, **un artefatto del proiettore** *(`Ppi` `-3e-6`..`-5e-6`, `A` `-6e-6`..`-2e-5`, dove `Ppi` tocca `A` in `Gamma`; `P0`, isolata, `<= 2e-8`)*. **Il criterio era mal fatto; non lo cambio** |
| **la quasi-energia** *(la coppia: le due parti ruotano in verso opposto)* | `P0 +1.821`, `Ppi -1.783`; **la somma `+0.037 ± 0.11`: TORNA** | `P0 +1.527`, `Ppi -1.540`; **la somma `-0.013 ± 0.066`: TORNA** |
| **il quasi-impulso** *(non e' una conservazione della mappa non lineare)* | le valli di `D_P0` e `D_Ppi` quasi uniformi *(`~1/3` ciascuna)*: **non distinguono** | la riflessione per `K` e l'identita' accoppiano meglio *(`0.06`-`0.14`)* degli spostamenti di `±K` *(`0.28`-`0.37`)*; nessuna lettura |

**Quindi `(n1)` per la quasi-energia** *(e per `Q_S` nel fatto, banale: alla lettera `(n2)` a `r 1` per l'artefatto)*: **il decadimento e' permesso dalle conservazioni del modello, come un atomo eccitato.**

**Un fatto di metodo che esce da qui:** il periodo vero di `D` a `r 1` e' **`4.07`-`4.10` unita' di tempo**. **Il «`10.91`» di `5f06dbfb` e l'«`11.45` a ogni `s`» di `de411167` sono compatibili con un ALIAS del campionamento ogni `3` unita' di tempo** *(il conto: `11.20`-`11.39`)*: **l'«indipendente da `s`» viene dal passo, non dal modo.** A `r 1.5247` i due metodi non coincidono *(`3.49` dalle rotazioni, `4.96` dai cambi di segno, con `~2.3` campioni per mezzo periodo)*: non risolto.

**Quello che la regola NON dice:** «incrocia» e' stato visto diventare «decade» su `r 1`, `0.65`, `1.5247`; **su un caso dove nessuna incrocia non c'e' misura** *(`r 0.69`: lista d'attesa)*. Sulla carta, a pesi liberi, esistono punti dove nessuna incrocia *(`085ffb27`, sez. `1`)*. **AGGIORNATO** *(Luca, `10:06`)*: **non sono tarature in quanto tali.** **Una TARATURA sceglie i pesi per un solitone dato** *(il suo `mu`, la sua forma, la sua `N`)*; **la REGOLA qui sotto e' una disuguaglianza generale:** vale **per ogni solitone su quel punto della banda**, con la legge **`U_max <= margine`**, e si prova su tre `N` e con due controlli che la violano. **La decisione delle `09:09`** *(niente taratura dei pesi per stabilizzare `S1`)* **resta.**

### LA REGOLA DEI LIVELLI PIATTI *(del guardiano, Luca `09:31`; ### **DA VERIFICARE**: la prova e' `doc/TASK_HISTORY/2026-10-30_livelli_piatti.md`)*

Un solitone costruito sul punto `E0` della banda *(oggi `A` a `K`, `E0 = -mu0`)* ha una frequenza locale nuda `mu - U(r)` che percorre **`J = [E0, E0 + U_max]`**, con `U_max` il massimo spostamento del legame *(per `S1` la saturazione `g`, oggi `1`)*, **per qualunque quantita' di materia**. **Le uscite esponenziali sono quelle i cui prodotti non si propagano** *(le piatte: togliere una piatta sola spegneva il modo anche con la banda `A` disponibile, `6d941a4d`, `de411167`)*.

> **LA REGOLA:** nessun livello piatto `F` *(`P0 = (b_a - a_n)/2`, `Ppi = -(a_n + b_a)/2`)* e nessuna media di due livelli piatti *(`(P0 + Ppi)/2 = -a_n/2`, `P0`, `Ppi`)* cade in `J` allargato di `W` *(la larghezza della risonanza, `99b679bc`: lo spegnimento fra `0.05` e `0.2` per quanto, a `g 1`; **ASIMMETRICA**: `0.2`-`0.8` dall'altro lato)*. **Le uscite con un prodotto che si propaga danno solo una perdita lenta** *(da verificare)*.

**E' la stessa cosa delle tre condizioni qui sopra:** c1 e' `F = mu - alpha` in `J`, la coppia e' `(F_i + F_j)/2 = mu - alpha` in `J`; **in piu' ci sono la larghezza `W` e la legge `U_max <= margine`.**

**Il controllo sui casi gia' misurati:**

| `r` | dove sta `J` rispetto ai livelli | che cosa si e' misurato |
|---|---|---|
| `1` | **la coppia sul bordo di `J`** | decade, `0.15` |
| `0.65` | **`P0` dentro `J`** | la risonanza di `P0` *(`ea8ace8f`)* |
| `1.5247` | **la coppia dentro `J`** | il modo lento, `0.0331`, agli anelli `12`-`13` *(`03142636`)* |
| `0.69` | **al limite** | non misurato |

### LA FORMA GENERALE *(Luca `09:33`; ### **IPOTESI DEL GUARDIANO DA VERIFICARE, NON LEGGE**)*

Con `omega` la frequenza del solitone, `V(x)` in `[0, V_max]` lo spostamento locale del legame, `F_j` i livelli dei modi a velocita' di gruppo zero *(le piatte)*: **per ogni ordine `n` permesso dal legame, `n (omega - V) != F_j1 + ... + F_jn` per ogni `V` in `[0, V_max]`, con margine `n W`** *(le quasienergie modulo `2 pi/s`; nel limite `s -> 0` senza modulo)*. `n = 1`: una piatta; `n = 2`: la coppia; `n >= 3` solo se il legame ha termini di ordine piu' alto. **Il riferimento:** la condizione di non risonanza dei breather discreti *(MacKay e Aubry, `1994`: `n omega` fuori dallo spettro lineare)*. **Le differenze qui:** (i) il pericolo esponenziale viene solo dai modi fermi *(i modi che si propagano danno una perdita lenta: da verificare)*; (ii) `V` varia lungo il profilo, quindi la condizione vale su un intervallo, non su un valore. **`W` e' empirica** *(`99b679bc`)*; la sua legge *(per esempio con `x alpha'(x)`)* non e' nota.

*(Una nota del codice: `alpha(x) = g x^2/(1 + x^2)` non e' un polinomio, ma **la stabilita' lineare vede solo `D` e `conj(D)`: `n = 1` e `n = 2`.** `n >= 3` non si verifica con queste corse.)*

**L'esito della prova** *(`doc/referti_l2/livelli_piatti.txt`, sha1-BYTE dello script `367d8549`; ### **LA LETTURA `p1`-`p3` NON SI FA**)*:

- **Solo uno stato su cinque e' fermo: (R) `N 1e6`** *(residuo `4.7e-10`)*. `R_3e5` *(`1.06e-3` anche con la tappa a `N 6e5`)*, `R_3e6` *(`2.42e-4` con la tappa a `N 2e6`)*, `X1` *(`2.05e-7` coi `10` passi in piu')*, `X2` *(`4.8e-5`)* **non convergono**; nessuno si allarga verso il bordo del toro *(`w/L` `0.074`-`0.096`)*. **Da `R_3e5`, `R_3e6`, `X2` la deriva del residuo porta `|D|` sopra `1e-2` (o quasi) gia' nei primi campioni: la forma non si giudica.**
- **(R) `N 1e6`, la corsa breve:** **il criterio aggiunto dice LINEARE** *(`b 1.061 +- 0.004`, `gamma t_ultimo -0.07`)*, **il vecchio, alla lettera, ESPONENZIALE** *(l'intercetta negativa)*. **Nessun modo esponenziale in `300` unita' di tempo.**
- **(R) `N 1e6`, la corsa lunga fino a `tau 3000`:** **il cuore regge AL BIT fino a `tau ~2000`** *(`0.56291`)*, poi **si svuota lentamente** *(`0.53619` a `3000`; `w/w_in` `1.045 -> 1.084`)*: `|D|` a fine finestra `1.96e-6`, `4.58e-6`, `2.04e-5`, `1.13e-3`, `2.11e-2`, `8.68e-2`. **`D` sta in `A` all'inizio** *(`0.999` a `500`)*, **poi `P0` sale a meta'** *(`0.463` a `1500`, `0.493` a `2000`)*, **e alla fine torna in `A`** *(`0.860` a `3000`)*. **Contro `r 1` di `26300537`** *(cuore `0.630 -> 0.454`)* **e `r 1.5247`** *(`0.663 -> 0.510`)* **il cuore perde molto meno, ma NON e' stabile.** ### **`(p4)` alla lettera: si svuota lentamente, e `D` va in `A` e in `P0`.**
- **(X1):** **ESPONENZIALE con entrambi i criteri, col modo previsto** *(la coppia `P0 + Ppi` agli istanti prima della saturazione: `0.50 + 0.46`, anelli `15`-`16`; il periodo dalle rotazioni `4.019`, `D` ogni `0.75`)*. ### **Da annotare (Luca `16:26`): il tasso `0.061` contro `0.151` a `g 1`, `r 1`: un indizio che `W` scali col legame `g`.**
- **(X2):** dallo stato non fermo `|D|` parte da `1.0e-3` e cresce come la deriva *(`v / attesa 1.29`)*: **il modo previsto non si vede in `300` unita' di tempo; la lettura non si fa.**
- **Il criterio aggiunto della forma ha fallito il suo collaudo su un caso** *(la retta con intercetta negativa: `t^2`)*: **la sua decisione e' di Luca** *(la relazione, `9e7dc1d7`)*. **Sui dati veri di `R_1e6` dice LINEARE, coi `98` campioni.**

### IL MODO DI (R) *(Luca `20:46`; il referto `doc/referti_l2/modo_di_R.txt`, sha1-BYTE `82a627e9`, `12/12`)*

- **La corsa lunga riletta:** la finestra del criterio di `5f06dbfb` *(da `10` volte la deriva a `1e-2`)* e' **`tau 1620 .. 2301`, il tasso `0.00792`** *(la finestra del guardiano `1500 .. 2200`: `0.00810`)*; **dentro la finestra `D` e' `A 0.486`, `P0 0.496`, `Ppi 0.018`**; prima, in media, `A 0.914`, `P0 0.082`. **`(p2)` confermata: l'uscita mancante e' `P0 + A`.**
- **La corsa rifatta** *(AL BIT coi pezzi a `2000` .. `14000`)*: **le rotazioni rispetto a `mu`: `P0` `+0.744 +- 0.031`, `A` `-0.728 +- 0.017`; la somma `+0.016 +- 0.041`: ZERO** *(una coppia)*; ogni tick e ogni `5` coincidono *(nessun alias)*.
- ### **LA FREQUENZA E IL POSTO, che decidono:** **la parte `A` ha `E = -1.607`, DENTRO la banda `A` libera** *(`-2.513 .. -1.365`)*, **ed e' DIFFUSA** *(raggio medio `22.2` contro `psi0` `5.8` e l'uniforme `29.9`)*: **e' RADIAZIONE.** ### **La parte `P0` ha `E = -0.138`, FUORI da ogni banda (nel gap), `0.49` SOPRA il livello piatto libero `-0.628`, ed e' LOCALIZZATA sugli anelli `13`-`14`** *(il bordo del solitone: `psi0` finisce fra `12` e `14`)*. 
- ### **LA LETTURA ALLA LETTERA: (i2)** *(la parte `A` e' diffusa: radiazione)*; ### **la crescita viene da un modo di `P0` TRATTENUTO al bordo del solitone, il cui livello il solitone SPOSTA dal piatto libero, in coppia con la radiazione in `A`:** `E_P0 + E_A = -1.745` contro `2 mu = -1.737`. **Col livello piatto LIBERO** *(`-0.628`)* **il partner cadeva a `2 mu + 0.628 = -1.109`, nel gap sopra `A`: la regola diceva «sicuro»; col livello SPOSTATO** *(`-0.138`)* **il partner cade a `-1.599`, DENTRO `A`: e' l'uscita che la regola non vedeva.** *(Calcolo del guardiano coi numeri del referto, non stampato dallo script.)*

### LA REGOLA ESTESA *(Luca `20:46`)* -- ### **SMENTITA dalla lettura (i2) di `795d2c81`, SOSTITUITA qui sotto** *(Luca `22:11`)*

*(Diceva: i livelli `F` sono quelli dei modi che non lasciano il solitone, le piatte E i modi interni della banda `A`. In (R) la parte `A` di `D` e' radiazione, non un modo interno.)*

### LA REGOLA CON L'USCITA MISTA *(Luca `22:11`; ### **IPOTESI DEL GUARDIANO DA VERIFICARE, NON LEGGE**)*

**Le uscite:**
- **(n1)** una piatta: `F + alpha = mu`;
- **(n2)** due piatte: `(F_i + alpha) + (F_j + alpha) = 2 mu`;
- **(n2-misto)** una piatta trattenuta e un'onda che si propaga: `(F + alpha) + E_c = 2 mu`, con `E_c` in una banda DISPERSIVA libera *(`A` o `B`)*.

**Per `alpha` in `[0, g]` il partner percorre `[2 mu - F - g, 2 mu - F]`: se tocca una banda dispersiva, l'uscita mista e' aperta.** **Lo «spostamento» `+0.491` della parte `P0` in (R)** *(`795d2c81`)* **e' `alpha` del cuore** *(`0.5000`, `g 0.5`)*: **il livello trattenuto e' `F + alpha`.**

**Il controllo** *(`doc/referti_l2/scatola/uscite.txt`, nessuna corsa; ### **CORRETTO il `2026-10-31` (Luca `00:21`): la riga di `r 1.5247` di `c6ad04ac` usava i pesi della famiglia SBAGLIATA** *(`a_n = pi`, `b_a = r pi`: `P0 +0.824`)*; **ora ogni riga coi pesi del SUO stato, e un DEVE lo verifica** *(il residuo del tick dello stato coi pesi della riga = quello della sua ricerca; coi pesi sbagliati `7.9e-2` contro `1.7e-10`)*)*:

| il caso | `mu` | (n2-misto) `P0`: il partner | `A` libera | (n2) `P0 + Ppi`: `2 mu - F_i - F_j` contro `[0, 2g]` | il tasso misurato, l'uscita |
|---|---|---|---|---|---|
| `r 1` *(`g 1`)* | `-0.56602` | `[-2.132, -1.132]`: **APERTA** | `[-3.142, -1.560]` | `+2.00955` contro `[0, 2]`: `0.0096` fuori | `0.151`, la coppia di piatte |
| `r 1.5247` *(`g 1`; ### **i pesi di `_strada_b_r`**: `a 2.3416`, `b 3.5702`, `mu0 = pi/2`)* | `-0.56861` | `[-2.752, -1.752]`: **APERTA** | `[-2.956, -1.563]` | ### **`+1.20437` DENTRO `[0, 2]`: APERTA, ad `alpha 0.602`** *(il modo misurato agli anelli `12`-`13`, dove `alpha ~0.6`: `03142636`)* | `0.033`, la coppia di piatte |
| `X1` *(`g 0.5`)* | `-1.06418` | `[-2.628, -2.128]`: **APERTA** | `[-3.142, -1.560]` | `+1.01323` contro `[0, 1]`: `0.0132` fuori | `0.061`, la coppia di piatte |
| (R) *(`g 0.5`)* | `-0.86850` | `[-1.609, -1.109]`: **APERTA** *(misurato: `-1.607`)* | `[-2.513, -1.365]` | `+1.40460` contro `[0, 1]`: `0.405` fuori | `0.0079`, **la mista** |

- **La mista `P0 + A` e' aperta in tutti e quattro.** ### **La coppia di piatte `P0 + Ppi`:** **per `r 1` e `X1` e' SUL BORDO** *(`0.0096` e `0.0132` fuori da `[0, 2g]`: entro `W`, la larghezza di `99b679bc`)*; **per `r 1.5247` e' APERTA DENTRO l'intervallo** *(`1.204` in `[0, 2]`, ad `alpha 0.602`)*; **per (R) e' lontana** *(`0.405` fuori)*. **Dove la coppia e' aperta o entro `W`, domina** *(`0.033`-`0.151`)*; **dove e' lontana resta la mista, piu' lenta** *(`0.0079`)*. *(La frase di `c6ad04ac`, «la coppia chiusa ovunque ma entro `W`», era sbagliata per `r 1.5247`: correzione di Luca `00:21`.)*
- **I tassi per tipo di uscita:** **coppia di piatte** `0.151`, `0.061`, `0.033`; **mista** `0.0079`.
- **La prova della scatola** *(se `0.0079` e' fisico o del toro)*: sotto.

### L'ESITO DELLA SCATOLA *(Luca `22:11`; `doc/referti_l2/scatola.txt`, sha1-BYTE `10d10378`)*

- **Lo stato su `L 120`:** lo stato di `L 81` messo al centro; **Newton converge al passo `0`** *(residuo `4.719e-10`, `mu -0.868496535`: identici a `L 81`)*.
- **La corsa** *(`9` pezzi, fino a `tau 2700`)*: **la stessa uscita** -- nella finestra `D` e' `A 0.487`, `P0 0.495`, `Ppi 0.018` *(`L 81`: `0.486`, `0.496`, `0.018`)*; **la somma delle rotazioni `P0 + A` torna `~0`** *(`-0.0065 +- 0.036` e `-0.0027 +- 0.033` nei pezzi `10000` e `12000`)*; `E_A -1.60`, dentro `A`; `E_P0 -0.14`, nel gap; **`D_A` diffusa** *(raggio medio `27.5` contro `psi0` `5.8` e l'uniforme `44.5`)*, **`D_P0` agli anelli `13`-`14`**.
- ### **Il tasso: `L 120` `0.00741 +- 0.00053`, `L 81` `0.00792 +- 0.00039`; la differenza `-0.00051` contro `3 sigma` combinati `0.00197`. LA LETTURA ALLA LETTERA: (s1), il tasso uguale entro gli errori: il decadimento misto e' FISICO, non della scatola.**
- ⚠ **Quanto e' forte la prova:** l'errore viene dalle **due meta' della finestra** *(`L 120`: `0.00779` e `0.00673`; `L 81`: `0.00819` e `0.00741`)*: **il tasso cala dentro la finestra** in tutti e due i tori; la `sigma` del fit *(`0.00002`)* lo sottostimerebbe di `20`-`25` volte. **Con questo errore una differenza fino a `~25 %` passerebbe per (s1).** **La vita:** `2445` su `L 120`, `2304` su `L 81` *(`+6 %`)*.

### LA SINTESI *(Luca `00:21`; solo scrittura)*

- **La regola con le tre uscite (n1, n2, n2-misto) spiega i casi misurati:** `r 1`, `X1`, `r 1.5247` decadono per la coppia di piatte *(aperta o entro `W`)*; (R), dove la coppia e' lontana, per la mista `P0 + A`.
- **I tassi per tipo di uscita:** **coppia di piatte `0.03`-`0.15`; mista `~0.008`.**
- **Il decadimento misto e' FISICO:** `L 81` e `L 120` danno lo stesso tasso entro gli errori *(la scatola, `(s1)`)*.
- ### **Per un solitone molto longevo serve chiudere ANCHE l'uscita mista: un vincolo sullo spettro del cammino** *(il partner `[2 mu - F - g, 2 mu - F]` fuori dalle bande dispersive)*. **E' una voce in lista d'attesa** *(la MAPPA, `29`)*, **collegata alla decisione sulle piatte** *(`25`)* **e alla vita richiesta** *(`27`)*.

## 6. LA VITA DEL SOLITONE *(Luca, `2026-10-30` `20:41` e `20:46`)*

> **La materia e' metastabile: non si cerca un solitone stabile per sempre, ma uno che vive abbastanza per l'esperimento.**

**`t_vita ~ ln(soglia/seme)/gamma`**, con `gamma` il tasso del modo piu' rapido, **il seme** l'ampiezza iniziale della perturbazione, **la soglia** dove il cuore cambia in modo visibile *(`|D|/|psi0| = 1e-2`)*.

### **LA SOGLIA, DECISA** *(Luca `22:11`, sulla raccomandazione del guardiano)*: **`t_vita` si misura al PRIMO `tau` con `|D|/|psi0| >= 1e-2`** *(la definizione di `795d2c81`)*.

**Il controllo sui casi misurati** *(`doc/referti_l2/modo_di_R.txt`, sezione `5`; l'osservato e' il primo `tau` con `|D|/|psi0| >= 1e-2`)*:

| il caso | `gamma` | previsto col seme `1e-9` | col primo campione | col seme EFFICACE *(`e^a` del fit)* | **osservato** |
|---|---|---|---|---|---|
| `r 1` *(`s 0.3`)* | `0.13901` | `116` | `111` *(`1.96e-9`)* | `139` *(`4.3e-11`)* | **`142.2`** |
| `r 1.5247` | `0.03311` | `487` | `492` *(`8.4e-10`)* | `611` *(`1.6e-11`)* | **`621.8`** |
| `R_1e6` | `0.00792` | `2035` | `1752` *(`9.4e-9`)* | `2278` *(`1.5e-10`)* | **`2304.0`** |

- **Col seme `1e-9` la formula da' l'ordine giusto e sbaglia per DIFETTO del `18`-`22 %`.** **Col seme efficace torna entro il `2 %`**, ma **e' quasi una tautologia** *(il seme efficace viene dallo stesso fit)*: **dice solo che il modo parte da un seme `~45`-`65` volte piu' piccolo del primo campione di `|D|`** *(la proiezione del residuo sul modo; rapporti del guardiano dalla tabella: `46`, `52`, `64`)*.
- ### ⚠ **L'osservato di Luca per `r 1.5247` era `450`-`480`; qui `621.8`:** **due definizioni** *(il cambio visibile del cuore contro `|D| = 1e-2`)*. **La soglia va fissata una volta** *(decisione di Luca)*. *(Per `r 1` col tasso `0.151` di Luca, `dfb5ab7e` a `s 0.15`: `107`.)*
- **La nota:** in un sistema con altri solitoni e radiazione **il seme e' molto piu' grande** *(per esempio `1e-3`: `ln ~2.3`, la vita sette volte piu' corta)*. **La regola dei livelli piatti serve a stimare `gamma`, cioe' a scegliere la vita, non a dire stabile si' o no.**
