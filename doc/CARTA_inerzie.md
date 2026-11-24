# LE QUATTRO INERZIE, IL COMPOSTO, FH/FT SULLA FASE *(il mandato di Luca [M0149], 2026-11-23 dopo le `01:50`: «lo facciamo ora»; sostituisce [M0133]; scritta PRIMA del codice `doc/referti_l2/inerzia_suite.py`)* [[PROGETTO-MITOSI]]

## 0. Cosa e' gia' fatto *(da [M0133], che mi era arrivato: citato, non rifatto)*

- **S1** il fondo chiuso con la foglia (ii) *(la carta del torneo sez. 14; la sagoma S10)*: bc40a2b2. **S2** S2 riletto *(R_E col compatto `1.1256` c_sol, `1.2138` c_banda, python -c delle 01:40)*: bc40a2b2.
- **S5 in parte:** i calci da `k 1500` di F0, FH, FT *(`k 0` e `k 0.010` asse 1, `fondo_suite_v2.py`, c0abc3e6)* in corsa dalle `01:47`; **le coppie FALLITE sul mio assert** *(a0424002: l'uguaglianza al bit di due `bincount` in ordine diverso)*: si rifanno con il controllo giusto *(sez. 5)*.

## 1. LE PREMESSE DAL CODICE *(lette dalle righe; dove la premessa del mandato cade, lo dico)*

- **Il campo U(1)** *(`csv/_u1_prototipo.Campo`)*: `A`, `E` per arco, **3 archi per nodo** *(`a1 = (1, 0)`, `a2`, `a1 + a2`, in quest'ordine: l'arco `3 v + a`)*; `spinta(f)`: `E -= f forza()` *(il rotore trasposto di `g(B)`)*; `deriva(f)`: `A += f w E`; `u() = e^{i e A}`. **Gauss:** `div E = e (rho - <rho>)` *(`porto.campi`)*; **la sorgente** *(`_u1_prototipo.avvolto`)*: `E -= e J`, `J` il flusso della norma sull'arco *(le due componenti di spin insieme)*. **`scrivi_U`:** `U[:,0,0] = U[:,1,1] = u`.
- ### ⚠ **LA PREMESSA CHE CADE:** il mandato dice «`q` la carica `sigma_z` del mattone». **Nel codice la fase di U entra UGUALE nelle due componenti di spin, e Gauss conta `rho` totale:** **la carica e' `e rho`, non `sigma_z`.** **Quindi `q = e` per unita' di norma** *(per particella)*, e la carica totale del mattone e' `e somma rho` *(con lo sfondo neutralizzante `-e <rho>`)*.

## 2. I2, L'INERZIA DEL CAMPO U

- **Il campo uniforme:** `E_a = E0 (a . x)` *(`x` = l'asse 1, `a1 / |a1|`; sui tre archi `E0`, `E0/2`, `3 E0/2`)*, **aggiunto a `campo.E` dello stato** *(sommato, non al posto)*. **Si dimostra dalle righe che resta:** `div` di un campo uniforme e' zero *(ogni nodo ha tre archi uscenti e tre entranti con le stesse direzioni)*, e la circuitazione su una placchetta di un campo che e' un gradiente e' zero *(`B` non cambia: `forza()` non lo tocca)*: **Gauss resta soddisfatto, `E0` non decade.** **`A` cresce di `w E_a` a tick** *(due `deriva(0.5)`)*, la fase di U su `a1` di `e w E0` a tick: **la spinta per particella e' `dk/dt = e w E0`** *(lo stesso `k` del calcio, che cresce col tempo)*.
- **L'ampiezza** *(mia, dichiarata)*: **`e w E0 = 2.0e-05` per tick** *(il `k` del calcio `0.010` raggiunto a `500` tick: «la spinta dello stesso ordine del calcio»)*; `E0 = 2.0e-05 / (e w)` con `e`, `w` letti dal campo *(se `w` non e' uniforme sugli archi `a1`, lo dico e FERMO)*.
- **Le corse:** `+E0`, `-E0` e `E0 = 0` *(il caso noto: ridà la deriva `v0` del calcio a `k 0` entro `3 sigma`)*, dallo stato compatto *(`tenuta/S1_cima/stato_001500`)*, il tick V0, `1000` tick, il baricentro ogni `10`. **La lettura:** `a` dal fit quadratico lungo l'asse 1 su `k 200 ... 1000`, **meno quello di `E0 = 0`**; **`m_E = (e w E0)/a` col segno** *(+E e -E: due stime)*. **K2:** i baricentri sotto `+E` e `-E` si muovono con segni OPPOSTI e `|a| > 3 sigma`; se no, «m_E non misurabile» e il perche'.

## 3. I3, L'INERZIA DEL TEMPO *(solo lettura)*

- **Le righe del collegamento** *(`caduta_segno_v2.tick_var`, `chi_tick.fase_a`)*: **V3** = la fase (a) `e^{+i e0 (N - 1)/2}` due volte a tick: **un'energia per particella `-e0 (N - 1)`** *(il segno della convenzione `e^{-i E}`)*: **la forza per particella `F_N = e0 |dN/dy|`** *(`epsilon_a = e0`)*; **V2** = `cs = s N` senza la fase: **la forza viene dal tempo proprio**, `F_N = |d omega/dN| |dN/dy|` con `d omega/dN` dall'orologio *(`orologio_mattone.txt`, `Nm` V2 contro `N1`)*.
- **`m_N = F_N/a` col segno**, con `a` della caduta *(`caduta_libera.txt`: `a/(c^2 |dN/dy|)` col verso)*: quindi `m_N = epsilon/(X c^2)` *(`X` il numero del referto, la stessa `c` del referto)*. **Dallo stato LARGO** *(la caduta partiva dallo stampo)*: lo dico.

## 4. I4, L'INERZIA DEL VUOTO; I5, L'OROLOGIO; S4, IL COMPOSTO

- **I4:** il calcio `k 0.010` asse 1 **con `phi` CONGELATO al vuoto fresco** *(dopo ogni tick `phi_h = c(t0 + 1500 + k) phi_v`: l'interruttore di `gravita_fase_F2.tick_F2`)*, **e `k 0` congelato** *(la deriva)*; **il caso noto:** lo stesso script con `phi` libero ridà I1 *(`-18.13`)* entro il `2%`. **K4:** `|Delta m*/m*| > 5%` = «il vuoto partecipa all'inerzia».
- **I5** *(solo lettura)*: `omega_ass/c^2` *(`omega` di F0 compatto `0.625906`, largo `0.62644`)* e `(omega_psi - omega_phi)/c^2` *(`Delta(1)` del vuoto locale da `legge_zeri.txt`)*, con c_sol e c_banda.
- **S4:** il calcio `k 0.010` asse 1 e `k 0` al triangolo **t000** *(`CHI/triangolo/t000/stato_029250.npz`)*, `1000` tick, **il baricentro di tutti e tre**. ### ⚠ **Due cose dalle righe:** (1) **t000 e' girato col tick con `chi`** *(`triangolo_chi_v4.py tronco`)*: qui gira **col tick V0** *(come il mattone)*, `chi` tolto -- dichiarato; (2) **il calcio da' `k` a ogni particella, quindi `m* = k/v` e' PER PARTICELLA:** per tre mattoni additivi `m*_tri = m*_mattone`, non `3 x`. **K5 riletto** *(mio, dichiarato)*: la massa del corpo `M* = m* somma rho`; **additiva se `M*_tri/(3 M*_mattone) = (m*_tri somma rho_tri)/(3 m*_mattone somma rho_mattone)` in `[0.8, 1.2]`** -- con `somma rho_tri = 3 somma rho_mattone` e' `m*_tri/m*_mattone`.

## 5. S5, FH E FT SULLA FASE *(dallo stato a `k 1500` della loro tenuta)*

- **Le coppie a `d 35`:** `fondo_suite_v2.coppia` con **il controllo giusto della traslazione** *(il file nuovo `fondo_suite_v3.py`)*: `nodo[perm] = T[nodo]` esatto; `psi` dei semiarchi permutata esattamente; **`rho` traslata contro `rho` spostata entro `1e-12` relativo** *(stampato)*. FH, FT e il caso noto F0, `delta` `0` e `180`, `2000` tick.
- **5b il calcio** *(gia' in corsa: c0abc3e6)*; **5d la caduta V2** *(`fondo_suite_v2.caduta`)*, rimessa in coda dopo I2, I4, S4.
- **Il caso noto F0** *(K1)*: la coppia in fase contro `-1.26e-06` a `d 39` riscalata a `d 35` come in [M1310-P] *(lo cerco nel referto prima di leggere)*; m* `-18.1` dallo stato compatto; la caduta V2 VIA; entro il `5%`.

## 6. I CRITERI E LE PREVISIONI *(copiati dal mandato)*

- **K1** casi noti: I2 con `E = 0` ridà la deriva del calcio a `k 0` entro `3 sigma`; I4 con `phi` libero ridà I1 *(`-18.13`)* entro il `2%`; S5 con F0 ridà i numeri di ieri entro il `5%`. **K2** I2: segni opposti sotto `+E` e `-E` e `|a| > 3 sigma`. **K3** S16: I1, I2, I3 coincidono entro il `15%`? per ogni coppia il rapporto con l'incertezza; il segno di ciascuna. **K4** `|Delta m*/m*| > 5%`. **K5** additiva in `[0.8, 1.2]` *(riletto: sez. 4)*. **K6** FH e FT: il segno di A e B; D2 ROVESCIATA / UNIVERSALE / COME OGGI; la tabella del giudizio.
- **LE PREVISIONI DEL GUARDIANO:** **P1** K1 passa `80%`; K2 passa `65%` *(«il mattone ha carica netta; se `sigma_z` e' a due segni bilanciati, non si muove: `35%`» -- ### la carica e' `rho`, non `sigma_z`: sez. 1)*. **P2** m_E coincide con I1 entro il `15%` `60%`; m_N NON coincide con I1 `85%`; I5 non si riconcilia con nessuna `75%`. **P3** I4: `|Delta m*/m*| < 5%` `55%`; se partecipa, aumentando `|m*|` `30%`. **P4** S4 additiva entro il `20%` `55%`. **P5** FH: A cambia segno `50%`, B col segno di oggi `60%`; FH e FT m* negativa `85%`, caduta V2 VIA `80%`; giudizio TOPPA o NULLA `70%`, CURA `10%`.
- **L'ordine in coda** *(S6)*: I2, I4, S4, poi S5 *(le coppie, la caduta)*; ogni corsa `<= 2000` tick. ### ⚠ **La ripresa P8:** le corse di questi script salvano la serie alla fine, non lo stato ogni `250`: **se il PC si riavvia in mezzo, la corsa si rifa' da zero** *(durano `<= 30` minuti)* -- non e' cio' che il mandato chiede, lo dico prima.
