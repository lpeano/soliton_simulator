# 2026-10-31 — CHIUDERE LE USCITE *(SULLA CARTA, DAL CODICE E SUL CAMMINO LIBERO; NESSUNA CORSA DI SOLITONI; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il mandato di Luca delle `00:38`, con le aggiunte delle `00:44` e `00:50` sul pezzo «che cos'e' la moneta»)*

> **La voce `27` della MAPPA promossa a lavoro attivo** *(decisione di Luca)*. **`eps 0.5` e' il caso PRINCIPALE, `eps 0` il ridotto.** Il documento: `doc/CHIUDERE_LE_USCITE.md`; i conti: `csv/_chiudere_le_uscite.py`, sul tick libero.

## 1. LE PREMESSE DAL CODICE

### Dal codice *(letto in questa sessione)*

- **Il tick libero, con la moneta:** `_bande_piatte.pezzi(s, eps)` costruisce i mezzi pezzi della prima meta' dell'ordine *(il legame, la moneta, il Grover, lo spostamento)* per `k`, col parametro `eps` passato **in memoria** *(`par["eps"] = eps`)*; `generatori()` da' `X_G` *(il Grover)* e `R_S` *(lo spostamento)*; `ricomposto(X_G, R_S, s, alpha, beta, M)` rifa' il tick palindromo `M G S S G M` coi pesi `alpha = a_n`, `beta = b_a` e la moneta `M` *(il mezzo pezzo a `eps`)*. **Lo spettro:** `E = -arg(lambda)/s`, `12` bande; i gruppi `Ppi` `0-3`, `A` `4-5`, `P0` `6-9`, `B` `10-11` *(per indice ordinato: a `eps 0.5` le «piatte» hanno una larghezza, `b5fd8ecc`: `0.0017`, `0.0029`)*. **Le quasi-energie sono definite modulo `Omega = 2 pi/s = 41.89`:** ogni condizione si controlla anche spostata di `+-Omega`.
- **La moneta** *(`motore._moneta_spin`, `leggi.yaml` `CAMM-MONETA-SPIN`)*: **`exp(-i eps dtau sigma.n)` per ESTREMITA', `n` il versore dell'arco**: lega lo spin alla DIREZIONE del moto; esatta e unitaria. **La misura del `2026-10-15` in `leggi.yaml`:** sotto la coniugazione `C` la moneta resta se stessa *(`C M C^-1 = M`, `0.000e+00`; `= M^-1`: `1.33e-01`)* perche' `sigma_y (sigma.n)^* sigma_y^-1 = -(sigma.n)`: **e' lei a impedire `C W C^-1 = W^-1`**; senza di lei l'uguaglianza e' esatta *(`3.9e-16`)* e compare la degenerazione di Kramers. **L'ordine dei componenti:** `psi_h` ha forma `(n*6, 2)`: per nodo `6` estremita' per `2` di spin, quindi l'indice a `12` e' `2 e + s`; `sigma` agisce sull'ultimo.
- **Il legame:** `alpha(x) = g x^2/(1 + x^2)` sulla densita' TOTALE del nodo *(le `12` componenti)*: **conta le piatte come materia.** **Lo stato fermo di (R)** *(`fermo_R_1e6`)* e la scena di `_livelli_piatti` servono per `(4c)`: **la parte NON LINEARE del tick su `psi0`** *(`T(psi0) - T_lin psi0`, `T_lin` il tick libero di `DV.matrice` applicato in `k`)* **e le sue frazioni di banda: se ha una parte piatta, il legame accoppia il solitone alle piatte.**
- **I punti della banda** *(il reticolo `L 81`)*: `Gamma` `(0, 0)`, `K` `(27, 27)`, `K'` `(54, 54)`; **`M` non e' sul reticolo `81`** *(`L` dispari)*: **il punto piu' vicino `(40, 0)`, dichiarato.** **I punti a velocita' di gruppo zero:** gli estremi e le selle delle bande dispersive, cercati sul reticolo dal gradiente.
- **`W`** *(`99b679bc`)*: `0.05`-`0.2`, asimmetrica; **le condizioni si stampano coi due margini.**

### Cosa NON so

- **Dove sta `mu` per un solitone su un punto `E0` qualunque:** dai casi misurati `mu - E0 = +0.4957` *(X1, (R), `g 0.5`)* e `+0.99384` *(`r 1`, `g 1`)*: **`mu` in `[E0, E0 + g]`** *(Luca)*. **Per un `E0` che e' un MINIMO di banda, `mu` sopra `E0` cade DENTRO la banda** *(non e' legato)*: **lo scrivo come uscita `(n0)`, `mu` in una banda dispersiva.**
- **Se `M` dipende dai pesi:** l'angolo della moneta e' `eps dtau_nodo`; **assumo che `dtau_nodo` non dipenda da `a_n`, `b_a`** *(DEVE: `ricomposto` coi pesi di oggi e `M` = `T` di `pezzi` entro `1e-10`)*.
- **La rotazione del reticolo sui `12` componenti** non l'ho costruita: **il comportamento della moneta sotto le rotazioni lo dico DAL CODICE** *(`sigma.n` con `n` che ruota)*, non da una misura.

## 2. I CRITERI

| il punto | il criterio, scritto prima |
|---|---|
| `1` | **chiusa dall'energia su `E0`** se per NESSUN `mu` in `[E0, E0 + g]` e nessun `alpha` in `[0, g]` vale una delle condizioni, col margine `W`: **(n0)** `mu` in una banda dispersiva; **(n1)** `mu - F` in `[0, g]`; **(n2)** `2 mu - F_i - F_j` in `[0, 2 g]`; **(n2-misto)** `[2 mu - F - g, 2 mu - F]` tocca una banda dispersiva. **A `eps 0.5` le `F` sono INTERVALLI** *(il min e il max della banda quasi piatta)*. Tutto modulo `Omega`. **DEVE: (R) col mio conto da' la mista con `A` aperta, `r 1` la coppia sul bordo.** |
| `2` | `r 1`, `g 1`, `eps 0.5` e `0`: per ogni punto critico delle bande `A` e `B` *(`Gamma`, `K`, `K'`, il quasi-`M`, gli estremi trovati)*: le uscite, aperte o chiuse, coi margini. |
| `3` | il piano `a_n/pi` x `b_a/pi` *(`0.25 .. 2`)* per `g` in `{0.25, 0.5, 1, 1.5, 2}`, `eps 0.5` e `0`: **i punti chiusi** *(per almeno un `E0`)*; il costo: la curvatura a `E0` *(la massa)*, la velocita' di gruppo massima di `A`. **Se vuota: l'uscita che resta sempre aperta.** |
| `4a` | per `Q_AB`, `Q_S`, la valle, la chiralita' `m mod 3`: **conservata dal tick libero?** *(`[T(k), O] = 0`; per `Q_AB` e la valle e' banale: il tick libero e' lineare e invariante per traslazioni)*; **dal tick col legame?** *(dal codice: `alpha(rho)`)* |
| `4b` | la tabella delle uscite con le cariche, prima e dopo; quali uscite ciascuna vieterebbe. |
| `4c` | **la parte non lineare del tick su `psi0` di (R): la sua frazione nelle piatte. NON NULLA = il legame accoppia il solitone alle piatte** *(e lo spiega)*. |
| `4d` | **la localita' dei proiettori di banda:** `max |P_g(R)|` per distanza, `eps 0` e `0.5`; **locale se decade esponenzialmente** *(il fit di `ln max|P|` contro `|R|`)*. |
| `5` | `v_max` delle due bande quasi piatte a `eps 0.5` *(il gradiente sul reticolo)*; il tempo per lasciare il bordo `~2/v_max` contro `1/0.151`, `1/0.061`, `1/0.008`. |
| `5c`, la moneta | che cosa mescola *(dal codice)*; **lo spettro a `K` e a `Gamma`, `eps 0` contro `0.5`: se apre un gap** *(la distanza fra i livelli che a `eps 0` sono degeneri)*; **l'elicita' `<sigma.k^>` degli stati di `A` vicino a `Gamma`: se separa le bande per elicita'**; le traslazioni *(per costruzione: `T(k)` esiste)*; `sigma_z`: `||[T(k), sigma_z]||`. |

## 3. LE LETTURE *(di Luca, scritte prima, senza soglie)*

- **(u1)** esiste una regione di cammini con tutte le uscite chiuse dall'energia, per ogni solitone su un punto della banda: le strade, coi costi *(a `eps 0.5` e a `eps 0`)*;
- **(u2)** la regione e' vuota: quale uscita resta sempre aperta e perche';
- **(u3)** una carica *(quale)* conservata con un legame locale sulla densita' di carica vieterebbe tutte le uscite: come, e che cosa cambia;
- **(u4)** nessuna delle due: il decadimento e' strutturale nel modello *(la strada (A): il solitone metastabile, la vita si sceglie col legame)*;
- **(u5)** la moneta accesa cambia la risposta *(quale uscita, perche')*.
- **La moneta:** **(e1)** come un campo magnetico uniforme; **(e2)** come il termine di massa di Dirac; **(e3)** altro; **(e4)** *(Luca `00:50`)* **un accoppiamento spin-direzione** *(elicita', di tipo `sigma.p` di Weyl/Dirac, o spin-orbita)*: **dire quale, dallo spettro vicino a `K` e a `Gamma` a `eps 0.5`** *(se separa gli stati per elicita'; se apre un gap)*. ### **L'errore `n.85` del guardiano:** aveva proposto solo (e1) e (e2).

## 4. LE MOTIVAZIONI

La vita richiesta *(MAPPA `27`)* per la materia vera e' `~10^49` periodi interni: **nessun tasso piccolo ci arriva, servono uscite CHIUSE** *(dall'energia, da una carica conservata, da una simmetria)*. Il lavoro decide fra le strade (A), (B strutturale), (C di principio) di `doc/BANDE_PIATTE.md`; riprende le cariche *(voci `9`, `10`, `14`)* e la chiralita' *(`11`)*; prepara la decisione `7` sulla moneta. **Vale come premessa per il 3D** *(`28`)*.

## 5. TODO

1. Questo file, committato **DA SOLO**.
2. `csv/_chiudere_le_uscite.py` *(il tick libero a `eps 0` e `0.5`; i punti `1`-`5`)* e la sua riga nell'inventario, committati prima di girare.
3. Il referto `doc/referti_l2/chiudere_le_uscite.txt` *(un processo)*.
4. `doc/CHIUDERE_LE_USCITE.md` *(le disuguaglianze in forma chiusa; le letture)*; `RELAZIONE`; `MAPPA` *(la `27` promossa; `9`, `10`, `11`, `14` collegate; la decisione `7` annotata; la riga `d`; l'errore `n.85`)*; la sezione `6` qui.


## 6. L'ESITO *(`chiudere_le_uscite.txt`, `4/4`; il documento `doc/CHIUDERE_LE_USCITE.md`)*

- **(1)-(3):** **(u1) con riserva** -- il massimo di `B` a `Gamma` chiude tutte le uscite fino a `n = 2` ai pesi di oggi *(margine `~2.1`, `eps 0.5` e `0`)*; il massimo di `A` a `K` solo per `a_n < b_a`, `g <= 1.5`.
- **(4):** `Q_AB` le vieterebbe tutte; i proiettori locali solo a `eps 0.5` *(il gap `0.0397` a `Gamma`)*. **(5):** le piatte troppo lente; la moneta (e4) dal codice, il tipo non deciso dallo spettro.
- **Le premesse che cadono:** «il solitone si costruisce dove sta oggi» *(il punto di oggi, `A` a `K`, e' quello con le uscite aperte; il massimo di `B` a `Gamma` no)*; **(4c) come l'avevo pensato** *(il termine di ordine zero non distingue: serve l'accoppiamento di coppia)*.
- **Gli errori miei:** il margine `0` del primo giro *(la n0 della banda stessa)*, corretto a parte.
