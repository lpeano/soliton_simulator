# 2026-11-28 -- [M0026] (DECISIONE DI LUCA 00:26): C LA COPPIA DA k 0 CON chi E LE NASCITE; F N DIPINTO NEL TICK DELLA MITOSI; D-P3; E [[PROGETTO-MITOSI]]

**La lettera:** `origin/guardiano:guardiano/posta/2026-11-28_0026_M0026.md` (`507d28ac`). La ricevuta e' in relazione, `d23e9305`.

## 1. LE PREMESSE DAL CODICE *(prima di guardare i numeri; la mappa e' di un agente di sola lettura, i punti che decidono li ho riletti io)*

- **La corsa `d1`:** `due_corpi_fondo_v6.py corsa --quale d1` (registro `m1446-M2034_d1`, `878b6e5f`, con 2 file non committati al lancio che non so quali sono).
  - **La scena** e' `TC.scena()` (`S162`, `L 162`, `n 26244`). **La partenza** e' `V6.costruisci(Z, 2, STATO_G3)`, con `pi = 0` e **`theta_a = 0` a `k 0`**.
  - **Il ciclo** e' `due_corpi_fondo_v2.ciclo`, che gira dentro `RF.col_nucleo(MV, P0)` e `MV.forma_esplicita("L-1")`. Fa `CV2.tick_chi_v2(Z["z"], C.campo, P, Lp, X)` a ogni tick e `C.residuo()` ogni 250.
  - **Gli stati** salvano le chiavi della scena, `campo_A`, `campo_E`, `chi`, `pi` e `theta_a`.
- **`Theta` nelle corse con `chi`:** `tick_chi_v2` fa `X["theta_a"] += pi (d_i - d_j)`, con `d = dtau cs` e `cs = s exp(-kappa chi_mezzo)`.
  - **E' la stessa riga** di `contatore.ritmo` della mitosi; **cambia il lapse**, `exp(-kappa chi)` contro `1/(1 + rho/rho_c)`.
  - `max |Theta|`: `1.50` a `k 3000`, `2.65` a `6000` (nessun arco oltre `2 pi`), **`11.42` a `d1L/18000`** (1596 archi). **Le nascite dovrebbero cominciare fra `k 6000` e `18000`.**
- **Le nascite:** `Rami.nasci` (`mitosi_rami_v2`) passa per `MR2.regola` -> `candidato` (riga per riga da `mitosi_regola`) -> `MR.applica`.
  - **(i)** `candidato` calcola `H` con `_libro_dei_conti.conti_per_nodo` piu' `K + V`, **senza `chi` e senza pesi `cs`**, e lo stesso fa `energia_corsa`, usata da P9. **Per C-2 serve una copia di `candidato` con l'energia `chi_tick_v2.energia_chi_v2`** sul grafo del candidato (`G` pesata + `Fa` + `K + V` + `H_chi`), e la stessa energia nel P9.
  - **(ii)** `regola` vuole un campo che cresce (`CampoGenerico` o `CampoOrientato`). **Il prototipo `_u1_prototipo.Campo` delle corse con `chi` non puo' crescere**, e va convertito (`MC.campo_generico`).
  - **(iii)** `applica` allunga il grafo, `psi_h`, `phi_h`, `geo`, `U`, `dtau`, `rho`, `Lambda`, `h_int`, `psi`, `cs` (con la legge `rho`), il campo, il contatore (`cont.cresci`) e le posizioni (`PZ.cresci`, che rende `Z["metti"]` RIFIUTATO). **Non allunga `chi`, `pi` e `Lp`.**
- **Il tick della mitosi** (`CorsaSB.passo` -> `p6_bracci.tick_GU`) **non ha un array `N`**: il lapse e' `N(rho)` attraverso `TL.N_di`, con il punto fisso `cs_al_centro`. `caduta_segno_v2.tick_var` prende `N` come array fisso, senza punto fisso ne' reazione.
- **Che cosa NON so:**
  - se `MC.campo_generico` sul prototipo ridia il tick AL BIT. Per K1 la conversione si fa **solo alla prima nascita**, cosi' K1 non la tocca;
  - se `C.residuo()` funzioni con il campo convertito;
  - quanto costi una nascita con l'energia di `chi` (cinque candidati, ciascuno con un motore e `energia_pesata`);
  - se `regola` e `applica` abbiano qualcosa di legato a `L 186`. La mappa dice di no, ma va provato a secco.

## 2. PROGETTAZIONE DEL RAGIONAMENTO

**C, `corpo_fuso_mitosi.py`** (nuovo). Lo scheletro e' quello di `d1` (`V6.costruisci`, `D.parametri`, il ciclo dentro `col_nucleo` e `forma_esplicita("L-1")`, `tick_chi_v2`).
- **Dopo ogni tick:** `scattati = nonzero(|X["theta_a"]| >= 2 pi)`. Se ce n'e' almeno uno, nasce il primo, come in mitosi: uno per tick, gli altri in attesa.
- **Alla prima nascita** il campo si converte in `CampoGenerico`, e lo dichiaro.
- **La nascita:**
  - `candidato_chi` (la copia, con l'energia `energia_chi_v2` sul motore del candidato, con `chi` e `pi` del nato uguali alla media degli estremi dell'arco (C-1) e `Lp` del candidato);
  - `regola` con `candidato_chi`;
  - `MR.applica`;
  - poi `X["chi"]` e `X["pi"]` allungati con la media, `Lp` ricostruito, `X["theta_a"] = cont.theta`;
  - **P9 con `energia_chi_v2`** entro `1e-12`;
  - `DH = H1 - H0` con `H_chi` (C-2), ed `E_persa`.
- **INGOLFAMENTO:** piu' di 500 archi in attesa, o un triangolo degenere (l'assert di `applica`): **FERMO**, dichiarato.
- **Le uscite:** gli stati ogni 250 (le chiavi di `d1`, piu' il grafo, `m1`, `m2` e `campo_vec` dopo la prima nascita), `nascite_*.json`, `serie.json` come `d1`.

**I casi noti, che decidono se si va avanti:**
- **(K-pre)** lo stato costruito a `k 0` = `d1/stato_000000` AL BIT;
- **(K0)** con le nascite spente, i primi 250 tick = `d1/stato_000250` AL BIT;
- **(K1)** con le nascite accese, nessuno scatto fino a `k 6000`, e lo stato a `6000` = `d1/stato_006000` AL BIT. **E' una corsa da 6000 tick, quindi va in coda come prima parte della corsa vera:** la corsa si ferma con FERMO se a `6000` non e' al bit;
- **(K-nascita, a secco, fuori coda)** una nascita forzata su un arco di `d1L/stato_018000`: P9 entro `1e-12`, la lunghezza di `chi`, `pi`, `theta_a` e `Lp` uguale a `n + 1` e `m + 3`, e `chi` del nato uguale alla media AL BIT.
- **Se un caso noto fallisce: FERMO.**

**La corsa C** va in coda: un processo, 18000 tick. Prima del lancio l'impegnabile libero deve superare 8 GB.

**F, `vuoto_lapse_mitosi.py`** (nuovo): `N` dipinto dentro il tick della mitosi, cioe' la via (a) della mappa.
- `TL.N_di` e `TL.Np_di` si sostituiscono in memoria con il seno valutato **nella posizione del nodo**, cosi' il nato lo eredita dalla formula (F-3).
- Lo stesso gradiente `G20`, con `A = G20 L_y / (2 pi kappa)` su `L 186`.
- **Che cosa resta da leggere:** la forma esatta di `N_di(rho, legge)` (la firma) e il termine `N'`, che con un `N` dipinto che non dipende da `rho` va a zero.
- **Il controllo:** `N` piatto = [M0106] AL BIT sui primi 250 tick.

**D-P3** dopo F, con la sua carta.

**Che cosa mi fa fermare:**
- un caso noto che fallisce;
- l'impegnabile sotto 8 GB;
- un DEVE AL BIT che diventa «quasi»;
- una scelta che non e' nella lettera.

## 3. TODO DEL NEXT STEP

- [ ] questo file; commit e push
- [ ] C: la carta in `doc/CARTA_mitosi.md`; `corpo_fuso_mitosi.py` (`noto`: K-pre, K0, K-nascita; `corsa`: con K1 dentro); commit; i casi noti; commit; la coda; commit al lancio
- [ ] F: la carta; `vuoto_lapse_mitosi.py`; il controllo con `N` piatto; la coda dopo C
- [ ] D-P3: la carta; il codice; i casi noti; la coda
- [ ] le letture e i verdetti di C, F e D-P3 a corse chiuse
- [ ] E: il TODO allineato a `CODA.md`; le ricevute di [M2245-27] e [M0026]; le previsioni confrontate; FERMO
