# 2026-10-31 — LA PROVA: IL SOLITONE SUL MASSIMO DI `B` A `Gamma` *(UNA PROVA IN `csv/`, NESSUNA MODIFICA AL NUCLEO; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il mandato di Luca delle `11:51`, sull'esito di `e92a7f9c`)*

> **Lo script:** `csv/_massimo_di_B.py`. **I dati:** `doc/referti_l2/massimo_di_B/` *(i `.json`, con lo sha1 di ogni stato)*; gli stati in `db/massimo_di_B/` *(ignorato: il dato E' il comando)*. **Il referto:** `doc/referti_l2/massimo_di_B.txt`. **`eps 0.5` e' il caso PRINCIPALE, `eps 0` il ridotto.**

## 1. LE PREMESSE DAL CODICE

### Da `e92a7f9c` *(`doc/CHIUDERE_LE_USCITE.md`, `chiudere_le_uscite.txt`)*

- Ai pesi di oggi *(`r 1`, `g 1`)*, sul massimo di `B` a `Gamma` tutte le uscite fino a `n = 2` sono chiuse dall'energia, a `eps 0.5` *(`E0 +3.17818`, margine `2.0990`)* e a `eps 0` *(`E0 +3.14159`, margine `2.1416`)*; la curvatura `-0.0032` *(`A` a `K`: `-0.0031`)*. **Sul massimo di `A` a `K`, il solitone di tutto il filone, tre uscite sono aperte.**
- **Il massimo di `B` a `Gamma` e' DOPPIO** *(`B[10]` e `B[11]` allo stesso `E0`, a tutti e due gli `eps`)*, come la coppia di `A` a `K`.
- **Le riserve di `e92a7f9c`:** le uscite con `n >= 3` e le coppie di onde dispersive non controllate; il solitone legato su `B` a `Gamma` mai cercato. **La nota del guardiano:** la chiusura vale finche' `+pi` *(il massimo di `B`)* e `-pi` *(`Ppi`)* non coincidono modulo `2 pi/s` *(a `s 0.15`: `41.9`)*.

### Dal codice *(letto in questa sessione)*

- **Lo stato di `A` a `K`** *(`_energia_del_legame.stato`, chiamato da `_deriva_congelato.nuovo` e quindi da `_diagnosi_s4.iniziale`)*: `g(r) = interp(r, profilo_u(S1, c, s, N, LAM0_TRI, w0)) sqrt(AREA_NODO)`, **lo stato `g[:, None] Q[None, :] e^{2 pi i (m1 + m2)/3}`** con `Q = coppia_K(0, s)[0]["Q"][:, 0]` *(la PRIMA colonna di una base QR della coppia: la scelta dentro la coppia e' gia' arbitraria li')*, normalizzato a `N`. **La scena ha `par["eps"] = 0.0`:** ### **tutti i solitoni del filone sono stati a `eps 0`.**
- **Lo stato su `B` a `Gamma`, scritto dal codice:** **l'inviluppo** = la norma per nodo dello stato di `A` a `K` della stessa scena *(`|Q| = 1`: e' `|g|`)*; **lo stato di Bloch** = la coppia del livello piu' alto di `A(Gamma)` *(la matrice del tick di `DV.matrice` sulla scena, a quell'`eps`)*, base QR, **la prima colonna**, come per `K`; **la fase di `Gamma` e' `1`.** ### **La differenza e' SOLO lo stato di Bloch.**
- **L'`eps` della scena:** `z["par"]["eps"]` *(il tick: `MS.tick` -> `CL.avanza` -> `DC.tick_congelato` -> `percorri_tick(..., z["par"], ...)`, il congelato vero di `74f99039`: i pezzi del vuoto saltati, `phi` rimesso a `phi0`)*; `DV.matrice` usa lo stesso. ### **Si mette IN MEMORIA dopo la scena** *(come `_bande_piatte.pezzo`)*.
- **Newton:** `_livelli_piatti.newton`, invariato *(il metodo di `_strada_b_r.cerca`; il criterio di `26300537`: `TOLL_RES 1e-9`, `MAX_NEWTON 30`)*, con la scena a `eps` sostituita **in memoria** al posto di `LP.scena` *(e rimessa all'uscita)*; `configurazione(1, 1)` *(i fattori `1.0`: al bit, `_livelli_piatti` `(0)`)*.
- **Le misure:** `CL.punto` *(`w`, il cuore `f_win` entro `w_in`, `f_3w0`, il picco)*; `SL.anelli` *(`alpha` del cuore, anello `0`)*; `ML.Bande`, `ML.analizza` *(le bande e le rotazioni di `D`)*; `LP.forma_pendenze` *(il criterio aggiunto della forma, collaudato `5/5`)*.

### Le tolleranze della scatola *(Luca `11:51`, sulla `80df9ab9`)*

- I due DEVE che fallivano *(il residuo e `mu` fra `L 81` e `L 120`, differenze `9e-16` e `6e-12`)* avevano tolleranze mie, non derivate. **Le nuove, di Luca:** `|Delta mu| <= il residuo` *(il residuo di `L 120`)*; **il residuo entro `1e-3` relativo.** Un commit a se', col referto rifatto; ### **la lettura (s1) non cambia** *(DEVE: le altre righe del referto identiche)*.

### Cosa NON so

- **Se esiste un legato su `B` a `Gamma`:** l'inviluppo e' quello di `A` a `K`; la curvatura e' la stessa entro il `3%`, ma **la struttura del legame** *(`alpha` sulla densita' TOTALE del nodo)* **vede lo spinore di `B`, non di `A`**, e non so se il profilo regge.
- **Dove cade `mu`:** dai casi di `A` a `K`, `mu - E0` `+0.99384` a `g 1`. **Se `mu - E0` e' piccolo, la coppia `B + B` di onde libere e' sul bordo:** il margine e' `2 (mu - E0)`.
- **Quale vettore dentro la coppia di `Gamma`:** la prima colonna QR, arbitraria come a `K`; **non so se la scelta conta.** Lo scrivo, non lo provo.

## 2. I CRITERI

| il punto | il criterio, scritto prima |
|---|---|
| `0` | **sul tick libero** *(`_chiudere_le_uscite.Libero`)*, per `eps 0.5` e `0`: `E0`, `J = [E0, E0 + g]`, le piatte; **(n1), (n2), (n2-misto)** come in `e92a7f9c`; **(n3)** `3 mu - F_i - F_j - F_k` in `[0, 3 g]`; **le coppie di onde dispersive** *(`c`, `c'` in `A`, `B`)*: **(c0)** le due libere, `2 mu` nella somma degli intervalli; **(c1)** una col legame *(`alpha` in `[0, g]`)*: `2 mu - alpha`; **(c2)** tutte e due: `2 mu - 2 alpha` -- ### **(c2) `B + B` E' IL SOLITONE STESSO** *(`alpha = mu - E0` su due quanti di `B` a `Gamma`)*: **esclusa per costruzione, come la (n0) della sua banda, e dichiarata.** Tutto modulo `Omega`, coi margini e `W`. **Prima per ogni `mu` in `J`; dopo Newton, al `mu` misurato.** ### **PREVISIONE: nessun modo esponenziale.** |
| `1` | **DEVE (il controllo positivo):** l'inviluppo per `Q_K e^{2 pi i (m1 + m2)/3}` rifa' lo stato di `A` a `K` della scena entro `1e-12` relativo. **DEVE:** `A(Gamma) Q_B = e^{-i E0 s} Q_B` entro `1e-10`; `E0` = quello di `chiudere_le_uscite` entro `1e-5`; la coppia degenere entro `TOLL_DEG 1e-7`. **DEVE:** lo stato di partenza ha la norma `N` entro `1e-12`. |
| `2` | **FERMO** se il residuo `< 1e-9` entro `30` passi; altrimenti lo stato migliore, **dichiarato con la storia**. **LARGO** se `w > L/6` *(`13.5`)*: la ricerca si rifa' a `L 120` dalla stessa costruzione; ### **se anche li' `w > L/6` o non converge: nessun legato (b3).** Ogni stato **committato appena trovato** *(il `.json` con lo sha1)*. |
| `3` | `300` unita' di tempo *(`2000` tick)* da ogni stato fermo: **la forma col criterio aggiunto** *(`LP.forma_pendenze`)*; le bande di `D` *(`ML.analizza`)*; **le rotazioni per banda se cresce.** **DEVE:** `Q_S` e `M` entro `1e-10`. |
| `4` | **solo se la breve a `eps 0.5` NON e' esponenziale:** `40000` tick *(`6000` unita' di tempo)* a pezzi di `4000` tick, **ogni pezzo committato**; ogni `10` tick il cuore, la larghezza, l'alone *(`1 - f_3w0`)*; ogni `20` tick `|D|/|psi0|` e le bande di `D`. **La vita:** il primo `tau` con `|D|/|psi0| >= 1e-2`; **se non arriva, il limite superiore del tasso** `gamma < ln(1e-2/seme)/6000`, coi due semi *(il primo campione, `1e-9` di Luca)*: ### **vale il piu' largo dei due.** **DEVE:** `M` entro `1e-10`; ogni pezzo riparte dallo stato di fine del precedente, sha1. |

## 3. LE LETTURE *(di Luca, scritte prima, senza soglie)*

- **(b1)** il solitone sul massimo di `B` esiste, non ha modi esponenziali nella corsa lunga, e il cuore regge: **la prima uscita chiusa dall'energia confermata** *(il tasso: il limite superiore)*;
- **(b2)** esiste ma decade: **quale uscita** *(dalle bande e dalle rotazioni di `D`)*, cioe' quale termine manca alla regola;
- **(b3)** non esiste un legato su `B` a `Gamma` con `S1` *(perche': Newton, la larghezza)*;
- **(b4)** altro.
- **`eps 0` contro `eps 0.5`:** le stesse letture, e la differenza.
- ### ⚠ **«Il cuore regge» non ha soglia** *(Luca)*: **stampo il cuore all'inizio e alla fine, e lo metto accanto a quello di `A` a `K`** *(`26300537`: `0.630 -> 0.454` in `3000`)*; la parola la scrivo con quei numeri accanto.

## 4. LE MOTIVAZIONI

La vita della materia vera *(`~10^49` periodi)* vuole uscite **chiuse**; **la regola dice che sul massimo di `B` a `Gamma` lo sono gia', ai pesi di oggi, senza leggi nuove.** E' la prova piu' diretta, **prima di ogni modifica del legame** *(la strada della carica)* **o dei pesi**.

## 5. TODO

1. Questo file, committato **DA SOLO**.
2. **La scatola:** `csv/_scatola.py` con le tolleranze di Luca *(un commit, con la riga dell'inventario)*; poi `--referto` e il referto rifatto *(un commit)*; il task history della scatola annotato.
3. `csv/_massimo_di_B.py` e la sua riga nell'inventario, **committati prima di girare**.
4. `--previsioni` *(il punto `0`)*, committato.
5. `--cerca e05`, poi `--cerca e0` *(un processo alla volta)*, ciascuno committato appena trovato; `L 120` se largo.
6. `--breve e05`, `--breve e0`, committati.
7. `--lunga` a pezzi *(se la breve a `eps 0.5` non e' esponenziale)*, ogni pezzo committato.
8. `--referto`; `doc/CHIUDERE_LE_USCITE.md` *(l'esito)*; `RELAZIONE`; `MAPPA` *(la riga `d`; le tolleranze della scatola)*; la sezione `6` qui.
