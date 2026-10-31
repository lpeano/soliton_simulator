# CHIUDERE LE USCITE *(Luca, `2026-10-31` `00:38`, con `00:44` e `00:50`; SULLA CARTA E SUL TICK LIBERO, NESSUNA CORSA DI SOLITONI; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]])*

> **I conti:** `csv/_chiudere_le_uscite.py` *(sha1-BYTE `1ee42dbe`)*, il referto `doc/referti_l2/chiudere_le_uscite.txt` *(`4/4` DEVE)*. **Il task history:** `doc/TASK_HISTORY/2026-10-31_chiudere_le_uscite.md`. **`eps 0.5` e' il caso principale, `eps 0` il ridotto.**

## IL PRIMO RISULTATO *(Luca `2026-10-31` `15:58`, la lettura (k1); il dettaglio nella sez. `10`)*

> ### **IL SOLITONE SUL MASSIMO DI `B` A `Gamma` REGGE, dove la regola chiude tutte le uscite.** **In `20000` unita' di tempo il cuore non deriva** *(`0.618`-`0.633`, l'alone `0`)*; **il limite superiore del tasso e' `1.1e-4`, `70` volte sotto l'uscita mista**; **regge senza Newton a `N 3e5`, `1e6`, `3e6` e su `L 120`.** **Il solitone su `A` a `K`, dove le uscite sono aperte, nella stessa costruzione si svuota** *(`0.589 -> 0.446` in `3000`)*. ### ⚠ **Lo stato fermo non si trova** *(Newton si ferma a `1.2e-5`)*, **e la causa «energia» e' sostenuta dal contrasto, non provata aprendo un'uscita su `B`.** *(`csv/_consolida_B.py`, `doc/referti_l2/consolida_B.txt`, `20/20`.)*

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

## 8. L'ESITO DELLA PROVA SUL MASSIMO DI `B` A `Gamma` *(Luca `2026-10-31` `11:51`; `csv/_massimo_di_B.py`, `doc/referti_l2/massimo_di_B.txt`, `4/4`)*

- **Le riserve della sez. `6`, sciolte sulla carta:** **le (n3) sono chiuse** *(la piu' vicina `P0 + P0 + P0`, `6.30` a `eps 0.5`)*; **delle coppie di onde dispersive, la (c1) `B + B`** *(un quanto di `B` col legame, `alpha` in `[0, g]`, e uno libero)* **e' APERTA sull'intervallo generico** *(dentro di `1.0`: `2 mu - alpha` scende a `2 E0`)*, ### **ma al `mu` misurato e' CHIUSA, margine `0.988`** *(`mu - E0 ~0.994 > g/2`)*. **La (c2) `B + B` e' il solitone stesso, esclusa per costruzione.** ### **Al `mu` misurato TUTTE le uscite controllate sono chiuse, a tutti e due gli `eps`.**
- ### **Lo stato fermo NON si trova:** Newton *(il metodo e il criterio di `26300537`, `30` passi)* **ristagna a `2.4e-3` (`eps 0.5`) e a `3.0e-4` (`eps 0`, un plateau dal passo `13`)**. **Lo stato migliore resta stretto** *(`w 6.44`, `6.65` contro `6.64` della partenza; il cuore `0.613`, `0.589`)* **con `mu - E0 = +0.994`**, lo stesso spostamento di `A` a `K`. **Non si allarga.**
- ### **La lettura: (b3) per il criterio scritto** *(nessuno stato fermo)*, **ma NON separata da un limite del metodo** *(la coppia degenere a `Gamma`, il plateau)*. **Le corse brevi e la lunga non sono partite:** partono dagli stati FERMI, e con questi residui la deriva satura `1e-2` in `< 1` e `~5` unita' di tempo. ### **La prima uscita chiusa dall'energia NON e' ne' confermata ne' smentita.**
- **`eps 0` contro `0.5`:** le stesse cose; a `eps 0` Newton arriva piu' in basso *(`3.0e-4` contro `2.4e-3`)*.

## 9. LA SCELTA DENTRO LA COPPIA E LA CORSA LUNGA *(Luca `2026-10-31` `13:52`; `csv/_coppia_di_B.py`, `doc/referti_l2/coppia_di_B.txt`, `3/3`)*

- ### **(q1) NO:** a `eps 0.5` il residuo dipende dalla scelta *(`3.2947e-2 .. 3.2958e-2`, contro il rumore `s0 1.4e-17`)*; **Newton dalla migliore** *(`theta pi/4`, `phi 5 pi/4`)* **scende a `6.806e-5` e si ferma**: la scelta aiuta *(`35` volte meglio di `ab7226e7`)* **ma non basta.**
- ### **(q2), SENZA VINCOLO:** a `eps 0` `q1`, `q2` sono spin su e giu' puri *(`sigma_z +-1`, elicita' `0`, `1/6` per estremita' della cella)* e **il residuo e' lo stesso su tutta la griglia** *(`3.3028e-2`)*: ### **la rotazione dentro la coppia e' una direzione LIBERA** *(spiega il plateau di `ab7226e7`)*. **Il vincolo che la fisserebbe non lo scelgo io.**
- ### **(q3): il cuore di `B` a `Gamma` RESTA, quello di `A` a `K` SI SVUOTA** *(`eps 0.5`, `20000` tick, `3000` unita' di tempo; `M` entro `1.2e-11`, `1.1e-11`)*. **I numeri accanto:**
  - **`B`:** il cuore `0.62039 -> 0.62850`, **sempre fra `0.619` e `0.632`**; le pendenze per finestra di `500` **di tutti e due i segni** *(`+9.3e-6 -1.8e-6 +3.7e-6 -1.8e-6 +2.6e-6 +5.2e-6`)*; `w/w_in 0.968 -> 0.961`; **l'alone `0.00000`**; il picco medio `5430`-`5455`.
  - **`AK`:** il cuore `0.58919 -> 0.44565`; le pendenze **tutte negative** *(`-1.2e-4 -5.8e-5 -1.9e-5 -1.1e-5 -1.5e-5 -2.0e-5`)*; `w/w_in 1.000 -> 1.274`; l'alone `0 -> 0.00485`; il picco medio `4588 -> 3632`. **`D` per lo piu' in `A`** *(con `P0`, `Ppi`)*.
- ### ⚠ **LA RISERVA: le due partenze NON sono costruite allo stesso modo** *(dichiarato prima)*: `B` parte dallo stato migliore di Newton *(gia' rilassato)*, `AK` dall'inviluppo. **La prima finestra di `AK`** *(`-1.2e-4`)* **contiene il rilassamento; le finestre dopo `1000` no, e scendono ancora** *(`-1e-5 .. -2e-5`)*. **E il contesto** *(`26300537`, `A` a `K` DALLO STATO FERMO, `s 0.3`, `eps 0`)* **si svuota lo stesso** *(`0.630 -> 0.454` a `3000`)*. ### **Il confronto pulito vuole `A` a `K` dal suo stato fermo a `eps 0.5`, `s 0.15`: non fatto.**
- ### **`D` in `B`: cresce LINEARE, tutto nella banda `B`** *(`3.7e-2 -> 1.79e-1`, `~6e-5` per unita' di tempo; `B 1.000` in ogni finestra)*, **e la rotazione di `B` va a `-0.0002`** *(`E +4.1720`, il `mu` `+4.1721`)*: ### **la differenza resta DENTRO la banda del solitone** *(lo stato non fermo che si ridistribuisce dentro `B`)*, **nessuna uscita.** ### **Il MIO errore:** avevo scritto che `D` avrebbe saturato `1e-2` in `~20` unita' di tempo *(`3836bd03`)*: **`D` non cresce esponenziale, e a `3000` e' `0.18`.**
- ### **Che cosa decide Luca:** il vincolo per la direzione libera a `eps 0`; se il plateau a `6.8e-5` merita una ricerca *(un'altra direzione quasi libera?)*; **la corsa di `A` a `K` dal suo stato fermo a `eps 0.5`, `s 0.15`** *(il confronto costruito allo stesso modo)*.

## 10. IL CONSOLIDAMENTO DEL SOLITONE SU `B` A `Gamma` *(Luca `2026-10-31` `15:58`; `csv/_consolida_B.py`, `doc/referti_l2/consolida_B.txt`, `20/20`)*

- ### **(k1), per le letture scritte prima: REGGE IN TUTTE LE PROVE, e il limite superiore del tasso e' sotto quello dell'uscita mista** *(`eps 0.5`, `S1`, `s 0.15`, `r 1`, `g 1`; il referto `doc/referti_l2/consolida_B.txt`, `20/20`)*.
- **La corsa lunga** *(dallo stato migliore di Newton, `6.8e-5`; `133334` tick, `tau 20000`, al bit dalla fine di `a8e0e43b`; `M` entro `7.8e-11`)*: ### **il cuore `0.62039 -> 0.62367`, sempre fra `0.618` e `0.633`, nessuna deriva** *(le pendenze delle `40` finestre di `500` dei due segni, al piu' `1.1e-5`)*; `w/w_in 0.958`-`0.969`; **l'alone `0.00000` per tutta la corsa.** `D` tutto in `B`; **le rotazioni delle altre bande a fine pezzo vanno verso `0`** *(`A -0.048 -> -0.010`)*.
- ### **Il limite superiore del tasso, aggiornato a `tau 20000`:** **piatte `1.13e-4`** *(`70` volte sotto la mista `0.0079`, `1236` sotto la coppia di piatte `0.139`)*; **`A` `1.09e-4`** *(`72` volte sotto)*. L'ampiezza nelle piatte `8.7e-5 -> 8.2e-4`; la pendenza di `ln a` sulla seconda meta' `4.8e-5`. *(A `tau 3000`: `4.5e-4`, `4.2e-4`. Il limite e' quello di una crescita lineare: scende come `1/T`.)*
- **La robustezza** *(dall'inviluppo, SENZA Newton, `tau 3000`)*: ### **il cuore resta per ogni `N` e ogni `L`:** `N 3e5` *(`L 81`, `w 4.96`)* `0.605 -> 0.593` *(fra `0.573` e `0.608`)*, `w/w_in 1.014`, l'alone `<= 0.0010`; `N 3e6` *(`L 81`, `w 8.70`)* `0.592 -> 0.589`, `w/w_in 1.001`, l'alone `<= 0.0002`; `N 1e6` su `L 120` `0.592 -> 0.604`, `w/w_in 1.010`, l'alone `<= 0.0005`; **il controllo `N 1e6` su `L 81`** `0.592 -> 0.599`, `w/w_in 1.001`, l'alone `<= 0.0005`. ### **Contro `A` a `K` della stessa costruzione** *(`a8e0e43b`)*: `0.589 -> 0.446`, `w/w_in 1.27`, l'alone `0.005` in crescita.
- ### ⚠ **LA RISERVA SUL LIMITE DELLE CORSE ROBUSTE:** dall'inviluppo **`D` parte gia' per l'`80`-`93 %` nelle piatte** *(la partenza non e' pura `B`: il suo contenuto piatto BATTE, `|e^{i Delta t} - 1|`)*; **l'ampiezza nelle piatte non supera MAI quella del primo campione** *(`N 3e5` `0.126 -> 0.086`)*, e il minimo a `tau 6` e' il battimento. ### **Il limite dichiarato** *(`2.9e-4`-`4.7e-4`, il piu' grande `N 3e6` piatte, `17` volte sotto la mista)* **viene da quel minimo: e' un limite largo, non una misura.** **E in `A` la frazione di `D` sale a `0.21`-`0.26`** *(a `tau 1185`-`2331`)* **e poi ridiscende:** il resto della partenza che si ridistribuisce; **l'alone resta `<= 0.001`.**
- ### **Lo stato fermo NON si trova nemmeno col vincolo:** a `eps 0.5` `1.16e-5` *(contro `6.8e-5`)*, a `eps 0` `1.12e-4`, **dove il vincolo non lavora** *(il tick lascia invariato lo spin su: il peso di spin giu' `6e-24`)*. **Che cosa ferma Newton resta aperto.**
- ### **«Protetto dall'energia»: e' la lettura (k1) di Luca, e i numeri la soddisfano;** **la causa e' sostenuta, non separata:** le uscite sono chiuse sulla carta *(sez. `8`)* e il caso con le uscite aperte *(`A` a `K`)* decade; ### **ma nessuna prova qui apre un'uscita su `B` a `Gamma` per vedere il decadimento tornare.**
- ### **Che cosa decide Luca:** che cosa ferma Newton *(non la sola rotazione dentro la coppia)*; **se aprire un'uscita su `B` a `Gamma`** *(per esempio spostando le piatte)* **per separare la causa**; **la convenzione materia/antimateria** *(la nota sulla voce `9` della MAPPA)*.
