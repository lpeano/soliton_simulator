# CHIUDERE LE USCITE *(Luca, `2026-10-31` `00:38`, con `00:44` e `00:50`; SULLA CARTA E SUL TICK LIBERO, NESSUNA CORSA DI SOLITONI; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]])*

> **I conti:** `csv/_chiudere_le_uscite.py` *(sha1-BYTE `1ee42dbe`)*, il referto `doc/referti_l2/chiudere_le_uscite.txt` *(`4/4` DEVE)*. **Il task history:** `doc/TASK_HISTORY/2026-10-31_chiudere_le_uscite.md`. **`eps 0.5` e' il caso principale, `eps 0` il ridotto.**

## 0. PERCHE'

La vita di un solitone e' `ln(soglia/seme)/gamma` *(`795d2c81`, `45cc48d8`)*. **Con un'uscita aperta `gamma` e' dell'ordine del legame, e la vita `10^2`-`10^3` periodi interni; la materia vera vive `~10^49` periodi.** Vite cosi' vengono solo da uscite **CHIUSE**: dall'energia, da una carica conservata, da una simmetria.

## 1. LA CONDIZIONE INDIPENDENTE DAL SOLITONE *(in forma chiusa)*

**Il solitone su un punto `E0` di una banda dispersiva ha `mu` in `[E0, E0 + g]`** *(dai casi misurati: `mu - E0 = +0.4957` a `g 0.5`, `+0.99384` a `g 1`)*; **il legame sposta i livelli di `alpha` in `[0, g]`.** **Le piatte `F`** sono, a `eps 0`, punti; **a `eps 0.5` INTERVALLI** `[F_min, F_max]` *(`P0` larga `0.0029`, `Ppi` `0.0017`)*. **Le bande dispersive** `A = [A_min, A_max]`, `B = [B_min, B_max]`. **Tutte le uguaglianze valgono modulo `Omega = 2 pi/s`** *(`41.89` a `s 0.15`)*.

**Il cammino CHIUDE LE USCITE DALL'ENERGIA su `E0` se, per nessun `mu` in `(E0, E0 + g]`, vale:**

| l'uscita | la condizione | aperta se |
|---|---|---|
| **(n0)** il solitone non e' legato | `mu` in una banda dispersiva | `(E0, E0 + g]` tocca `A` o `B` |
| **(n1)** una piatta | `F + alpha = mu` | `[E0 - F_max, E0 + g - F_min]` tocca `[0, g]` |
| **(n2)** due piatte | `(F_i + alpha) + (F_j + alpha) = 2 mu` | `[2 E0 - F_i,max - F_j,max, 2 E0 + 2 g - F_i,min - F_j,min]` tocca `[0, 2 g]` |
| **(n2-misto)** una piatta + un'onda | `(F + alpha) + E_c = 2 mu`, `E_c` in `A` o `B` | `[2 E0 - F_max - g, 2 E0 + 2 g - F_min]` tocca la banda |

**Col margine `W`** *(`99b679bc`: `0.05`-`0.2`)*: «chiusa» se la distanza supera `W`. **I pesi** `a_n`, `b_a` e la moneta `eps` entrano **solo attraverso lo spettro** `E(k)`; **`g` entra due volte**: nell'intervallo di `mu` e in quello di `alpha`.

### ⚠ Che cosa NON contiene

- **le uscite con tre o piu' quanti** *(`n >= 3`)*; **le uscite in due onde dispersive** *(`2 mu = E_c + E_c'`)*: **non controllate.**
- **la larghezza `W` come funzione di `g`:** e' quella misurata a `g 1` *(l'indizio delle `16:26`: `W` forse scala con `g`)*.

## 2. LO SPETTRO DI OGGI *(`r 1`, `g 1`)*

| `eps` | le bande | `A` al massimo *(`K`, `K'`)* | `A` a `M~` | **`B` al massimo** *(`Gamma`)* |
|---|---|---|---|---|
| **`0.5`** | `Ppi [-3.218, -3.216]`, `A [-3.178, -1.640]`, `P0 [+0.076, +0.079]`, `B [+1.636, +3.178]` | **APERTE:** (n2-misto) `P0 + A`, (n2-misto) `Ppi + B`, (n2) `P0 + Ppi` | APERTE | ### **TUTTE CHIUSE, margine `2.099`** |
| `0` | `Ppi -3.1416`, `A [-3.142, -1.560]`, `P0 0`, `B [+1.560, +3.142]` | **APERTE:** le stesse | APERTE | ### **TUTTE CHIUSE, margine `2.142`** |

- **Il solitone misurato sta sul massimo di `A` a `K`: li' tre uscite sono aperte**, a `eps 0.5` come a `0`.
- ### **Il massimo di `B` a `Gamma` chiude tutte le uscite (fino a `n = 2`) col margine `~2.1`**, ai pesi di oggi. **Il perche':** le piatte stanno **SOTTO** il massimo di `B` *(`P0` a `~0`, `Ppi` a `~-pi`)*: il partner `2 mu - F` cade **sopra** `B`, nel gap fino all'immagine di `Ppi` a `-pi + Omega`; mentre sul massimo di `A` le piatte `P0` stanno SOPRA e il partner cade dentro `A`. **`B` e' la banda speculare di `A` rispetto a `P0`** *(`E_B(k) = -E_A(k)`, `b5fd8ecc`): **il massimo di `B` a `Gamma` e' l'immagine del MINIMO di `A` a `Gamma`.**
- **La curvatura al massimo di `B`:** `-0.0032` *(quella di `A` a `K`: `-0.0030`, `-0.0031`)*: **la stessa massa, all'ordine di grandezza.**

## 3. LA REGIONE *(il piano `a_n/pi` x `b_a/pi` in `0.25 .. 2`, `g` in `0.25 .. 2`)*

| `eps` | i casi chiusi *(su `2560`: punto x `E0` x `g`)* | oltre `W 0.2` | il massimo di `B` a `Gamma` | il massimo di `A` a `K` / `K'` |
|---|---|---|---|---|
| **`0.5`** | **`680`** | `630` | **`574`** *(ogni `g`; margine `0.001`-`6.0`)* | `69` / `37` *(`g <= 1.5`; perlopiu' `a < b`)* |
| `0` | `672` | `628` | `576` *(margine `0.07`-`6.0`)* | `58` / `38` |

- ### **La regione NON e' vuota: (u1).** **Due strade:** **(i) il solitone sul massimo di `B` a `Gamma`, ai pesi di oggi**; **(ii) il solitone sul massimo di `A` a `K`, coi pesi `a_n < b_a` e `g <= 1.5`** *(la lista nel referto)*.
- **Le uscite aperte piu' spesso:** (n1) `Ppi`, (n2) `Ppi + Ppi`, (n2-misto) `Ppi + A` *(`~850` su `2560`)*; poi `P0 + Ppi` e `P0 + A` *(`~650`-`700`)*.
- **Il costo che non so dire:** **se un solitone LEGATO esiste sul massimo di `B` a `Gamma`** *(Newton non l'ha mai cercato li')*; **la velocita' massima della materia** e' quella della banda *(`v_max` di `A` stampata per i pesi chiusi)*.

## 4. LA CARICA DI MATERIA

| la carica | dal tick LIBERO | dal tick COL LEGAME di oggi |
|---|---|---|
| **`Q_AB = N_A - N_B`** *(le piatte a `0`)* | **conservata** *(lineare, invariante per traslazioni: ogni stato di Bloch prende una fase)* | **NO**: `alpha(rho)` mescola le bande |
| **`Q_S` (`sigma_z`)** | **`eps 0`: conservata** *(`[T, sigma_z] = 0`)*; **`eps 0.5`: NO** *(`1.46e-1`)* | come il libero *(il legame e' una fase per nodo)* |
| **la valle `K`/`K'`** | conservata *(il momento)* | il momento cristallino si conserva modulo il reticolo reciproco: **`3K = 0`, la valle no** |
| **la chiralita' `m mod 3`** | **non misurata** *(la rotazione sui `12` componenti non e' costruita)* | -- |

- **(4b) le uscite con `Q_AB`** *(il solitone: due quanti di `A`, `Q_AB = +2`)*: (n1) `2 -> 1`; (n2) `2 -> 0`; (n2-misto) con `A` `2 -> 1`, con `B` `2 -> -1`: **`Q_AB` conservata le vieterebbe TUTTE.** **`sigma_z` non ne vieta nessuna** *(il solitone e le uscite misurate sono tutte spin su)*; **la valle nemmeno** *(`2K = k_1 + k_2`, la riflessione misurata)*.
- **(4c) perche' oggi non protegge:** il legame dipende da `rho = sum |psi|^2` sulle `12` componenti, **che conta le piatte come materia.** **Il termine di ordine zero** *(`T(psi0) - T_lin psi0` su `psi0` di (R))* **ha frazione piatta `7.6e-5`, quella di `psi0` stesso `4.6e-5`: dello stesso ordine.** **L'accoppiamento che fa decadere e' quello di COPPIA** *(`psi0^2 D^*` sulle piatte)*, **non misurato qui; che esista lo dice il decadimento misurato** *(`795d2c81`)*.
- **(4d) il legame sulla densita' di carica** *(`rho_A - rho_B`, o `rho` senza le piatte)*: **conserverebbe `Q_AB` solo se il legame fosse diagonale nelle bande**; **e' locale solo se i proiettori lo sono.** **La misura:** `max |P_g(R)|` per distanza, la pendenza di `ln` fra `2` e `20`:

| | `Ppi` | `A` | `P0` | `B` |
|---|---|---|---|---|
| **`eps 0.5`** | `-0.567` | `-0.567` | `-1.711` | `-1.719` |
| `eps 0` | **`-0.183`** | **`-0.186`** | `-1.656` | `-1.672` |

  ### **A `eps 0` i proiettori di `Ppi` e di `A` hanno una coda lunga** *(`7.6e-5` a distanza `32`)*: **le due bande si toccano a `Gamma`** *(il gap `0`)*. ### **A `eps 0.5` la moneta apre a `Gamma` un gap di `0.0397` fra `Ppi` e `A`, e tutti e quattro i proiettori decadono esponenzialmente** *(`9.9e-10` a distanza `32`)*: **un legame sulla densita' di carica sarebbe LOCALE a `eps 0.5`, non a `eps 0`.** **Che cosa cambierebbe nel resto del modello** *(il vuoto, la gravita' collettiva, il libro dei conti)*: **non calcolato**; e' una legge nuova, quindi una decisione di Luca *(`9-ter`)*.

## 5. LE PIATTE CHE SI MUOVONO, E LA MONETA

- **(5a) a `eps 0.5`:** `v_max` di `Ppi` `2.97e-3`, di `P0` `1.26e-3` archi per unita' di tempo; **per lasciare il bordo** *(`~2` archi)* **`673` e `1589` unita' di tempo, contro `1/gamma` `7`, `16`, `125`.** ### **Non basta a trasformare il decadimento in una perdita lenta** *(come stimava Luca)*.
- **(5c) CHE COS'E' LA MONETA** *(dal codice: `motore._moneta_spin`, `CAMM-MONETA-SPIN`)*: **`exp(-i eps dtau sigma.n)` per ESTREMITA', `n` il versore dell'arco: mescola i due stati di SPIN di ogni estremita' con un asse che e' la DIREZIONE del moto.** **Commuta con le traslazioni** *(per costruzione: `T(k)` esiste)*; **non con le sole rotazioni del reticolo, ma con la rotazione INSIEME dello spazio e dello spin** *(`sigma.n` e' invariante se `n` e lo spin ruotano insieme)*: **conserva il momento angolare TOTALE, non `sigma_z`** *(dal codice, non misurato)*. **La misura del `2026-10-15`** *(`leggi.yaml`)*: **e' lei a impedire `C W C^-1 = W^-1`**; senza, la degenerazione di Kramers.
- **Lo spettro, `eps 0.5` contro `0`:** **a `Gamma` si apre un gap `0.0397` fra `Ppi` e `A`** *(zero a `eps 0`)*; **a `K` i due livelli di `A` restano degeneri** *(`4e-15`)*, quelli di `P0` si separano di `2.9e-3`; **`A` si sposta di `-0.08`.** **L'elicita' `<sigma.k^>` dei due stati di `A`:** **vicino a `K` di segno opposto, `+-0.01` .. `+-0.43` secondo la direzione**; **vicino a `Gamma` `<= 0.06`**.
- ### **LA LETTURA della moneta: (e4) dal codice** *(un accoppiamento spin-direzione)*; **dallo spettro NON e' un `sigma.p` di Weyl pulito** *(l'elicita' non e' `+-1`, ed e' anisotropa)*; **apre un gap a `Gamma`, come una massa, ma fra una piatta e una dispersiva.** **Quale delle due** *(elicita' o spin-orbita)* **non e' deciso da questi numeri.** **L'errore `n.85` del guardiano:** aveva proposto solo (e1) e (e2).

## 6. LE LETTURE *(di Luca, scritte prima)*

- ### **(u1), con riserva: ESISTE una regione con tutte le uscite chiuse dall'energia, fino a `n = 2`:** **il massimo di `B` a `Gamma`, ai pesi di oggi, a `eps 0.5` e a `0`** *(margine `~2.1`)*; **e il massimo di `A` a `K` per `a_n < b_a`, `g <= 1.5`.** **La riserva:** `n >= 3` e le coppie di onde dispersive non controllate; **l'esistenza del solitone legato su `B` a `Gamma` non e' provata.**
- **(u3) in parte:** **`Q_AB` conservata vieterebbe tutte le uscite**; **un legame su `rho_A - rho_B` sarebbe LOCALE a `eps 0.5`** *(i proiettori decadono)*, **non a `eps 0`**; che cosa cambierebbe nel resto del modello non e' calcolato.
- **(u5) la moneta accesa NON cambia quali uscite sono aperte** *(lo stesso schema, conti simili: `680` contro `672` chiusi)*; **cambia la LOCALITA' dei proiettori** *(il gap a `Gamma`)*, **quindi la strada (u3)**; **e le piatte si muovono troppo piano per contare.**
- **(u2) no; (u4) no** *(la strada (A) resta possibile, ma non e' l'unica)*.

## 7. CHE COSA DECIDE LUCA

1. **Una prova: Newton sul massimo di `B` a `Gamma`** *(il solitone c'e'? la sua vita?)*: **la candidata piu' diretta**, senza cambiare i pesi.
2. **La strada del legame sulla carica** *(`rho_A - rho_B`, locale a `eps 0.5`)*: una legge nuova *(`9-ter`)*.
3. **La moneta** *(la decisione `7`)*: in questo lavoro `eps 0.5` cambia la localita', non le uscite.
