# IL RESPIRO COME OROLOGIO SENZA ZERO: LO SPECCHIO ALLA PROVA *(Luca, 2026-11-23, [M1640]; scritta PRIMA del codice e dei numeri, `16:56`-`17:10` da `date`; [M1633] NON si fa: la precedenza in coda, e il mandato lo dice mal posto)* [[PROGETTO-MITOSI]]

## 0. GLI ERRORI DEL GUARDIANO, DICHIARATI *(dal mandato)*

- **n.238:** `omega` contata in assoluto quando andava contata dal vuoto.
- **n.239:** [M1633] *(il Pound-Rebka della luce)* era mal posto: in un `N` statico la frequenza di U in tick si conserva, `z = 0` per costruzione.

## 1. LA LETTURA ALLO SPECCHIO *(Luca, 16:28; i numeri dove li trovo)*

Cambiando segno a `omega` *(leggere il tempo al contrario: `rho` e le traiettorie non cambiano)*: la cima della banda diventa fondo con curvatura `+0.059`; la materia e' un solitone sotto il fondo a massa positiva; il vuoto gira a `+pi s` e la materia sta `1.1` sotto di lui. **Con V3 e le energie contate dal vuoto:** l'orologio va come `N` -- **`legge_zeri.txt`, V3, lo zero `omega(1) + e0`: `d ln Delta/dN = +1.00000`** *(con lo zero simmetrico `0`: `-0.76101`; col vuoto locale `-0.43129`)*; rallenta nel pozzo; la coppia attratta e' piu' lenta *(la sagoma S6: il Pound-Rebka G+U `+1.26e-4`, «l'attratto piu' veloce», che allo specchio cambia segno; Luca scrive `-1.25e-4`)*; V3 cade VERSO. **Restano sbagliate e invarianti sotto lo specchio:** Eotvos *(`eta` `0.138` in V3)* e la fase *(`A cos delta`)*.

## 2. LE LENTI, E PERCHE' IL RESPIRO NON HA ZERO

- **Le etichette di `omega` passano per tre lenti** che `rho` non vede: **il verso del passo**, **lo zero simmetrico `e^{-i pi s}`**, **il segno della fase (a)**. Ognuna cambia segno o zero a `omega` e lascia `rho(k)` com'e'.
- **Il respiro del mattone** *(S11, S18: `w` va da `~6` a `~16` e torna)* **e' una frequenza di `rho`**, quindi di un battimento: **nessuna delle tre lenti lo tocca.** Allo stesso modo la **differenza** di due frequenze locali *(il centro e `r 10`)*: l'offset comune si cancella. **Sono gli orologi senza zero.**

## 3. LE RIGHE DEL TICK *(lette dal codice alle `16:56`)*

- **`caduta_segno_v2.tick_var(z, campo, s, e0, N, cs_N, segno)`:** `campo.spinta(1/2)`; **`mot.cs = s N`** se `cs_N` *(V2)*, se no `s`; **se `segno`:** `chi_tick.fase_a(mot, st, segno e0, N)` *(V3)*; il palindromo `percorri_tick` avvolto; di nuovo `fase_a`; `campo.spinta(1/2)`.
- **`chi_tick.fase_a`:** `psi_h *= e^{i e0 (N - 1)/2}` per nodo. **Con `N` uniforme e' una fase COSTANTE su `psi`** *(due volte per tick: `e^{i e0 (N - 1)}`)*. ### ⚠ **Ma SOLO su `psi`, non sul vuoto `phi`:** e' una fase GLOBALE della fisica solo se il tick e' invariante sotto `psi -> e^{i alpha} psi` **a `phi` fermo**. **Non lo so: lo misura K2.**
- **V2:** `cs = s N` entra **solo nel cammino**; `campo.spinta`, le fasi del vuoto e del legame **non** portano `N`. **Che un `N` uniforme riscali il tempo di TUTTA la dinamica e' l'ipotesi del mandato da misurare**, non un fatto. **L'indizio:** `legge_zeri.txt`, V2 a `N` uniforme `0.9965`: `omega_psi - omega_vuoto` = `1.093838` contro `1.097676 N = 1.093834` *(lo scarto `3.2e-6`)*.

## 4. LE SCELTE *(S1-S4 del mandato, con le righe)*

- **S1:** `fondo_suite_v2.carica(Z, "F0", 1500)` *(il compatto, la forma S1 del nucleo, come `fh_suite.tenuta_lunga`)*; **un ciclo mio, riga per riga quello di `fondo_suite_v2._tick_loop`** *(che chiama `tick_var` col segno `0`: non sa fare V3)* **con `(cs_N, segno)` per riga:** V2 `(True, 0)`, V3 `(False, +1)`; `N` = un vettore costante. **Sei corse da `20000` tick:** **N1** *(`N = 1`)*, **V2 `0.99`**, **V2 `1.01`**, **V3 `0.99`**, **V3 `1.01`**, ### **e CTRL** *(`N = 1`, con `psi_h` moltiplicato UNA volta a `k 0` per `e^{i e0 (0.99 - 1)}`: la stessa fase di un tick di V3 `0.99`)*. **CTRL e' mia, il mandato non la nomina:** separa l'arrotondamento dalla fisica *(sez. 5)*. **Gli stati ogni `250`, la ripresa P8.**
- **S2, gli orologi:** ogni `50` tick `w` e il picco *(`torneo_tenuta.lisciata`, la definizione di `torneo_tenuta.misura`)*; a ogni tick `omega` globale, **`omega_c`** *(i mezzi archi dei nodi a `r < 5` dal centro)* e **`omega_10`** *(`9 <= r < 11`)*, `omega = -arg somma conj(psi_prima) psi_dopo`; **il centro:** il nodo del picco della `rho` lisciata a `k 0`, fisso. **Il fit del respiro, dichiarato qui:** su `k 2000-20000`, `w(k) = a + b k + A sin(2 pi k / T + phi)`, minimi quadrati non lineari *(`scipy.optimize.curve_fit`)*, `T` iniziale dal picco dello spettro, `sigma_T` dalla covarianza scalata col `chi2` ridotto; lo stesso per il picco. **Il battimento:** la media di `omega_c - omega_10` su `k 2000-20000`, `sigma` da `20` blocchi.
- **S3, il controllo di `rho`:** `rho = somma |psi_h|^2` per nodo a `k 5000, 10000, 20000`, **contro N1, al bit** *(`np.array_equal` e lo sha1 dei byte di `rho`)*; e lo scarto `max|drho|/max rho`.
- **S4, il verdetto per forma:** `T(0.99)/T(1.01)` contro `1.0202` *(V2)* e `1.0000` *(V3)*.

## 5. TRE PREMESSE DEL MANDATO CHE VANNO DETTE PRIMA DEI NUMERI

- ### **K1 «a `N = 1` il periodo ridà `5125` entro l'`1%`»:** **`5125` non e' un periodo misurato, e' il centro di un bin dello spettro** *(`41` campioni su `10250` tick: il bin vicino e' `~3417` o `~10250`; S18 lo dice)*. **Un fit su `20000` tick contro il centro di un bin:** il confronto e' fuori scala *(come la soglia `1e-6` di n.237)*. **Lo giudico come scritto e lo dico.**
- ### **K2 «gli sha1 degli stati»:** **lo stato contiene `psi_h`, che in V3 e' ruotato di una fase: gli sha1 sono DIVERSI per costruzione.** Il confronto si fa su **`rho`**. **E anche `rho` al bit e' quasi certamente impossibile in virgola mobile:** `|psi e^{i alpha}|^2` non e' `|psi|^2` all'ultimo bit, e una dinamica non lineare puo' far crescere l'arrotondamento. **Per questo CTRL:** se V3 si allontana da N1 **quanto CTRL**, la fase e' globale *(e il «non al bit» e' arrotondamento)*; se si allontana **molto di piu'**, la fase NON e' globale *(una riga del tick vede `psi` contro `phi`)*. **Il DEVE al bit resta come scritto**; la lettura col controllo e' dichiarata qui, prima.
- **K3 a `0.003`:** `T` va misurato allo `0.15%` *(`3.6` cicli in `18000` tick)*: **non so se il fit ci arriva.** Se `sigma` del rapporto supera `0.003`, lo dico: K3 non decide.

## 6. I CRITERI *(copiati)* E LE PREVISIONI

- **K1** a `N = 1` il periodo ridà `5125` entro l'`1%`; la norma a `1e-12`; le corse arrivano a `20000`. **Il caso noto in piu' (mio):** **N1 ridà al bit gli stati della tenuta S1 di [M0326-T]** *(`E:/soliton_simulator/controllo/M0326/tenuta_lunga_S1`, fino a `k 10000`)*. **K2** in V3 `rho(k)` a `0.99` e `1.01` al bit con `N = 1` a `k 5000, 10000, 20000`: DEVE. **K3** V2: `T(0.99)/T(1.01) = 1.0202` entro `0.003`: DEVE. **K4** ETICHETTA se K2 e K3 passano; FISICA se V3 rallenta il respiro come `N`; **se V2 non riscala, FERMO.**
- **DEL GUARDIANO** *(copiate)*: P1 K1 `85%`; K2 al bit `85%`; K3 `85%`. P2 ETICHETTA `80%`, FISICA `10%`, FERMO `10%`. P3 il battimento come il respiro per V2 entro l'`1%` `70%`.
- **LE MIE** *(prima dei numeri)*: **N1 = la tenuta S1 al bit `95%`**; **K1 `5125` entro l'`1%` `35%`** *(il bin)*; **K2 al bit `15%`** *(l'arrotondamento)*, **ma V3 entro `10 x` CTRL `70%`**; **K3 `60%`** *(`cs` solo nel cammino; l'indizio di `legge_zeri` a `3e-6` e' per `omega`, non per il respiro)*; **`sigma` del rapporto sotto `0.003` `50%`**; **il verdetto ETICHETTA `60%`**.

## 7. LE RISORSE

Sei corse da `1` filo, a priorita' `0` in `coda_m1446`, nel tetto dei `10` col freno a `4 GB`. **Il PC si riavvia fra mezzanotte e le due:** le corse riprendono dall'ultimo stato *(P8)*.
