# 2026-11-22 -- LA CADUTA LIBERA: DA CHE PARTE CADE UN MATTONE IN UN TEMPO CHE RALLENTA *(il mandato di Luca [M0908], `09:08`)* [[PROGETTO-MITOSI]]

> **Le regole di questo file:** cio' che dice Luca e' scritto come SUO; le letture del guardiano sono IPOTESI; **le premesse non si riscrivono quando si rivelano sbagliate: si annotano.** **Nessuna fisica cambia nelle corse in corso**; il nucleo non si tocca; i file sono nuovi.

## 1. [M0908-L] LA LETTURA DEL SEGNO *(scritta PRIMA del codice `doc/referti_l2/caduta_segno.py` e dei suoi numeri)*

### 1.1 Le premesse dal codice *(che cosa ho letto PRIMA di scrivere questa carta: lo dichiaro, perche' cercare la riga della carta dove la forma (a) fu decisa E' parte del mandato, e l'ho fatto prima)*

- **La fase (a) nel tick di `chi`** *(`chi_tick.fase_a`, usata da `chi_tick_v2.tick_chi_v2` mezza prima e mezza dopo il palindromo)*: `psi_h *= exp(0.5j e0 (N - 1))` per nodo, `N = exp(- kappa chi)`. **Nell'energia** *(`energia_chi`, `energia_chi_v2`)* il termine `Fa = - e0 somma (N - 1) rho`. **`e0 = 0.4767266286`** *(il meta dello stato `k 3000` di `chi-mattone-v2`; e' `eps_top` di T-L4b, `s5_coppia_lapse.eps_top_tl4b`)*.
- **La convenzione delle quasi-energie nel repo:** `csv/solitone/s5_caduta_segno.py` *(T-L4b)* scrive `E = -np.angle(lam)`, cioe' **gli autovalori del tick sono `e^{-i E}`**: `psi <- e^{-i H dtau} psi`. **Con questa convenzione la fase `e^{+i e0 (N - 1)}` per tick e' un potenziale `V_a = - e0 (N - 1)` per unita' di norma: POSITIVO dove `N < 1`.** E' coerente con `Fa`.
- **Dove fu decisa la forma (a)** *(`doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `31.22`, «LA FORMA (a) (del guardiano)»)*: **«l'energia della materia contata DALLA CIMA della sua banda»**, `E_N = somma N_k h_k - eps_top somma (N_k - 1) rho_k`, **col vincolo (iv): «il peso della materia, `h - eps_top rho`, e' `<= 0` nella banda: il segno dell'inerzia»**. La prova: **T-L4b** *(`f16cadf8`, il referto `doc/referti_l2/s5_caduta_segno.txt`)*. **Il passaggio a `chi`:** **D-CHI-FORMA-A = (fa1)** *(Luca `2026-11-21` `16:05`, `doc/TASK_HISTORY/2026-11-21_lapse_u.md`)*: «la forma (a) era accesa in tutte le corse G+U legate» *(`p6_bracci.tick_GU`, `eps_a = e0`)*.
- ### ⚠ **QUELLO CHE L'IPOTESI DEL MANDATO NON CONTIENE, ed e' gia' MISURATO:**
  - **T-L4** *(stesso referto)*: **la banda dei solitoni sta in CIMA**, `d2 eps/dk2 = -5.923e-02`: **una massa efficace NEGATIVA**. **Con la sola `cs = s N` il pacchetto va verso `N` piu' ALTO** *(`a = +2.19e-05` a `gamma +0.01`)*.
  - **T-L4b:** **con la forma (a) i pacchetti vanno verso `N` piu' BASSO**, `~670` volte piu' piano *(`s d eps/d cs = 0.475826` contro `eps_top = 0.476727`: la differenza `-9.0e-04`)*: **la forma (a) e' stata costruita per CANCELLARE quasi tutto l'effetto di `cs = s N` e lasciare il segno dell'inerzia.**
  - **G1** *(`f0affd34`, `doc/referti_l2/s5_caduta_solitone.txt`)*: **il solitone VERO, con la forma (a), va verso `N` piu' ALTO** *(`+5.14e-06` a `gamma 0.01`)*; il suo cuore sta `0.1493` SOPRA la cima della banda.
- **Quindi la mia premessa, PRIMA dei numeri:** **P-C6 e' vera alla lettera** *(l'energia del termine (a) e' positiva nel pozzo)*, **ma l'ipotesi della lente non regge per i pacchetti**: con la massa efficace negativa un potenziale piu' alto nel pozzo ATTIRA, e la camminata piu' lenta RESPINGE. **Il segno della caduta e' il PRODOTTO di due segni** *(l'energia e l'inerzia)*, non il primo da solo.

### 1.2 Che cosa NON so

- **Se la cima della banda nel vuoto della scena di `chi`** *(S162, il vuoto fresco MGU, il campo `U`, `g_e = 0`)* **e' la stessa di T-L4** *(un'altra scena, `L 81`)*: `e0` fu copiato da li'.
- **Se il mattone `L162_MGU_03000` si comporta come il pacchetto o come il solitone di G1.**
- **Il segno della frequenza del vuoto da UN tick:** una fase per tick e' definita a meno di `2 pi`; **a `~pi` per tick, `+omega` e `-(2 pi - omega)` danno lo stesso numero.** **Da un tick si legge solo `e^{-i omega}`, non il segno di `omega`:** lo scrivo prima, e la prova lo deve mostrare.

### 1.3 La progettazione *(`caduta_segno.py`, sola lettura, nessuna corsa lunga)*

1. **Le righe del codice**, stampate dai sorgenti *(non ricopiate)*: `chi_tick.fase_a`, la riga di `Fa`, la riga `E = -np.angle` di T-L4b, e le righe delle carte sopra *(cercate per testo, coi numeri di riga di OGGI)*.
2. **(a) Il vuoto, UN tick:** sulla scena di `chi` *(`triangolo_chi_v4.scena`, `mattone.vuoto_fresco`, `porto.campi`, `g_e = 0`)*, il tick U con `cs = s` *(`gravita_due_corpi.tick_U`)*; `e^{-i omega} = <phi_0, phi_1> / |.|`; **stampo `omega` e `omega - 2 pi`.**
3. **(b) L'onda piana, la risposta lineare di UN tick** *(il metodo di T-L4b, le stesse costanti importate da `s5_caduta_segno`: `A_IMP`, `DK`, `H_CS`)*: `12` impulsi `+-` su `psi` in un nodo; `A(k) = somma_x R(x) e^{-i k.d(x)}`; **la coppia piu' alta a `Gamma`, `E = -angle`**, `d2 E/dk2` lungo `B_0`; **la C-linearita'** *(la risposta a `i e_j` contro `i R e_j`)*.
4. **(c) Le varianti a `N` uniforme `1 - H_CS`**, la risposta di un tick per ciascuna: **V2** *(`cs = s N`)*, **V3** *(la sola fase)*, **V1** *(tutte e due)*, **V4** *(`cs = s N`, la fase col segno opposto)*: `dE_top/dN` di ognuna.
5. **La lettura, fissata QUI:** con `d2 E/dk2 < 0` un pacchetto va verso `E_top` piu' ALTO; **`dE_top/dN < 0` = verso `N` piu' basso** *(VERSO)*, `> 0` = VIA.

**Che cosa mi farebbe FERMARE:** la coppia piu' alta a `Gamma` lontana da `e0` piu' del `5%` *(il vuoto della scena di `chi` non e' quello di T-L4: `e0` andrebbe riletto, e lo decide Luca)*; la C-linearita' rotta sopra `1e-6` *(il metodo non vale)*.

**Le previsioni del guardiano, prima dei numeri:** `d2 E/dk2 < 0` *(85%)*; `dE/dN`: V2 `~ +0.476`, V3 `-0.477`, V1 `~ -1e-03`, V4 `~ +0.95` *(70%: il vuoto e' diverso, i numeri possono spostarsi)*.

### 1.4 TODO

- [ ] committare questa sezione e `caduta_segno.py` *(il codice prima della corsa)*;
- [ ] girarlo, il referto `doc/referti_l2/caduta_segno.txt`, commit e push col referto e la relazione;
- [ ] poi [M0908-C]: le previsioni di Luca P-C0 ... P-C6 riconciliate con T-L4/T-L4b/G1 **scritte accanto, non al posto**.
