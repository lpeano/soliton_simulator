# LE LEGGI PROVATE SUL LATERALE *(`zero-nel-nucleo`)* [[PIANO-2D-3D]] [[PUNTO-FISSO-CS-SOLITONE]]

> **Il mandato:** Luca, `2026-11-11` `23:42`-`23:45` *(S5.3, punto T)*. **Si aggiorna a ogni prova.**
> **Le fonti:**
> - il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md` *(le sezioni citate)*;
> - i referti in `doc/referti_l2/`.
>
> **I commit sono quelli del CODICE che ha girato** *(«a `<hash>`»)*, **salvo dove e' scritto «il referto a».**

**GLI STATI:**
- **CANDIDATA** = si prova ancora;
- **SCARTATA** = le prove la escludono;
- **PRONTA PER IL NUCLEO** = la decisione di Luca per l'ingresso.

### ⚠ **Dove lo stato NON e' una decisione di Luca, e' scritto «(proposto)»: la decisione resta sua.**

## 1. LA LEGGE DI `cs` DA `Lambda`, A PUNTO FISSO *(la legge di oggi; con e senza la reazione)*

- **La forma:** **`cs = s Lambda / (Lambda + Lambda_c)`** *(`FP.cs`)*, **col punto fisso al centro del palindromo** *(`tick.cs_al_centro`)*. **Con la reazione** *(V-R)*: **la fase `Omega` per nodo dalla derivata dell'energia pesata.**
- **Il codice:**
  - **nel nucleo,** `primo_ordine/flussi_parziali.py` *(`cs`)* e `primo_ordine/tick.py` *(`cs_al_centro`)*;
  - **le prove,** `csv/solitone/carta_punto_fisso.py`, `carta_punto_fisso_r.py`, `s2_spettro.py`.
- **Le prove:**
  - **D0-D4 `8/8`** *(sez. `10`, a `3faa4858`)*: **a `Lambda_c = 34` nessun metodo trova il punto fisso;**
  - **(r-D5) `7/7`** *(sez. `14`, a `1fcc9e9b`)*: **(d3), la legge interna e il dominio `s > 0` cedono prima del punto fisso;**
  - **S2 `20/20`** *(sez. `28.5`, a `015f5ee2`)*: **(w1) e (w4), il vuoto con la legge di `cs` e' INSTABILE PER COSTRUZIONE in tutta la mappa;**
  - **V-R `34/34`** *(sez. `31.11`, a `e6798e4a`)*: **con la reazione il vuoto resta instabile in tutta la mappa.**
- **Lo stato: SCARTATA** *(confermata da Luca, `2026-11-12` `01:40`)*:
  - **il vuoto da solo fa da orologio, ed e' instabile** *(S2, V-R)*;
  - **Luca alle `18:17` ha scelto `N(rho)`** *(la scelta 5, sez. `31.19`)*.

## 2. F1, LA MEMORIA *(`A15`)*

- **La forma:** **`cs_nuovo = cs_vecchio + (cs_legge(Lambda) - cs_vecchio) r`, `r` in `(0, 1]`** *(sez. `16.2`, `18`)*.
- **Il codice:** `csv/solitone/carta_f1.py`, `carta_f1_lunga.py`, `h4_vuoto.py`.
- **Le prove:**
  - **F1 `2/3`** *(sez. `20`, a `f5f0c47c`)*: **F1-V FALLISCE;**
  - **F1 col rilassamento esatto `2/3`** *(sez. `22`, a `d2689b81`)*: **la perturbazione cresce;**
  - **T2** *(sez. `25.4`, a `2d996ae0`)*;
  - **B1 (iv)** *(sez. `27.6`, a `e340476c`)*;
  - **H4** *(sez. `27.11`, a `a54a3ee4`)*: **il DEVE di (v0) FALLISCE, il vuoto uniforme con F1 e' instabile da solo;**
  - **S1 `5/5`** *(sez. `28.3`, a `00dedc5b`)*: **il falso-uno di F1-V confermato;**
  - **S2** *(sez. `28.5`)*: **«la colpa e' della LEGGE, non della memoria».**
- **Lo stato: SCARTATA come cura** *(confermata da Luca, `2026-11-12` `01:40`)*: **non cura l'instabilita', che sta nella legge del §1** *(S2)*.

## 3. M-rho ISTANTANEA

- **La forma:** **`cs = s / (1 + rho / rho_c)`**, **`rho` di inizio tick** *(sez. `29.2`, `30`)*.
- **Il codice:** `csv/solitone/s4_materia_mrho.py` *(`cs_di`)*; **in T-L2** `csv/solitone/s5_prove.py`.
- **Le prove:**
  - **S4 `102/116`** *(sez. `30.5`, a `e51dd24c`)*: **un difetto dello strumento;**
  - **S4.7 `101/101`** *(sez. `30.8`, a `59c562f0`)*: **lo strumento curato; «M-rho meno congelato» NEGATIVA in `14` punti su `15` a `rho_0 = 1`; a `rho_0` `1e-4`, `1e-2` l'instabilita' (I-cs) e' l'unica;**
  - **T-L2, accanto** *(sez. `31.20`, a `a82ca3d0`)*: **l'escursione dell'energia `1.00e+04`, `26` volte il lapse.**
- **Lo stato: SCARTATA come forma istantanea** *(confermata da Luca, `2026-11-12` `01:40`)*: **non conserva l'energia** *(T-L2)*; **la sua forma conservativa e' il lapse del §4.**

## 4. IL LAPSE `N(rho)` DI OGGI *(il banco, fuori dal nucleo)*

- **La forma:**
  - **`E_N = somma_k s N_k H_k + somma_a w_a H_a`**, **`N = 1/(1 + rho/rho_c)`, `w_a` la media armonica;**
  - **la reazione `Omega^psi_k = s N'(rho_k) [H_k + somma dw/dcs H_a]`** *(mezzo passo prima e dopo, punto medio implicito)*;
  - **`cs` al centro del palindromo a punto fisso** *(sez. `31.2`-`31.4`, `31.13`)*.
- **Il codice:** `csv/solitone/tick_lapse.py`; **le prove** `s5_banco.py`, `s5_prove.py`, `s4_materia_mrho.py --lapse/--lapse2/--lapse3`, `s5_caduta.py`.
- **Le prove:**

| la prova | l'esito | il codice |
|---|---|---|
| **S5.1** | **`2/2`:** **a `N = 1` il tick di oggi AL BIT** | `9344cc65` |
| **T-L1** | **`2/2`:** **sul vuoto al bit; calmo** | `a82ca3d0` |
| **T-L2** | **`6/8`:** **nessuna deriva;** **FALLISCE `dtau^2`** *(il rapporto `1.82`)*; **FALLISCE il DEVE FALLIRE senza reazione** *(l'escursione `27` volte piu' grande, ma la pendenza non la vede)* | `a82ca3d0` |
| **T-L3** | **interrotta** *(il punto fisso di `cs` nelle basi)* | `a82ca3d0` |
| **T-L3 rifatta** | **`2/3`:** **`5` punti su `45` senza punto fisso, tutti a `rho_0/rho_c >= 1`; il residuo di una base `2.492e-10` sopra `1e-12`** | `a2c0a50f` |
| **T-L4** | **`2/6`:** **il verso si rovescia col gradiente;** ### **il pacchetto va verso `N` piu' ALTO** *(l'opposto della gravita')*; **l'ampiezza `0.874` della prevista** | `a82ca3d0` |
| **A** *(S5.3, la soglia `1e-9`)* | **in corsa** | `a5f9a514` |

- **Lo stato: CANDIDATA** *(proposto)*: **conserva meglio di M-rho istantanea, ma col segno di oggi la materia della banda CADE verso il tempo piu' veloce** *(T-L4)*.

## 5. LA FORMA (a): L'ENERGIA DELLA MATERIA CONTATA DALLA CIMA DELLA BANDA

- **La forma:** **`E_N - eps_top somma_k (N_k - 1) rho_k`.**
  - **Con `N` esterno** *(T-L4b)*: **una fase per nodo `e^{+i eps_top (N_k - 1)/2}` su `psi` prima e dopo il tick.**
  - **Col lapse** *(S5.3 A)*: **`e^{+i eps_a [(N_k - 1) + N'_k rho_k]/2}`** *(la derivata della stessa energia)*.
  - **`eps_top` la cima della coppia piu' alta a `Gamma` del tick di oggi:** **`0.4767266` per tick a `s 0.15`.**
  - **A `N = 1` e' il tick di oggi.**
- **Il codice:** `csv/solitone/s5_caduta_segno.py` *(`N` esterno)*; `csv/solitone/tick_lapse.py` *(`fase_a`, col lapse)*; `csv/solitone/s5_caduta_solitone.py` *(G1)*.
- **Le prove:**

| la prova | l'esito | il codice |
|---|---|---|
| **T-L4b** | **`7/7`:** ### **il verso GIUSTO** *(verso `N` piu' basso, si rovescia col gradiente)*; **l'ampiezza `~670` volte piu' piccola della forma di oggi, `0.68` della previsione all'ordine zero** *(non (f1))*; **il principio di equivalenza fra tre pacchetti entro il `3.4%`** | `127d5018` *(il referto a `f16cadf8`)* |
| **A, forma (a)** | **interrotta:** **la base a `(1e-4, 0.1, 0.15)` senza punto fisso con la forma (a)** *(converge in `1` giro senza)*; ### **e un mio errore di progetto: la fase su `psi` non e' globale, `psi` e' accoppiato a `phi`** | `a5f9a514` *(registrata a `1000a48f`)* |
| **G1** | **`6/8`:** ### **(e3) il solitone vero (TBS a `10000`) va verso `N` piu' ALTO** *(`+5.14e-06` a `gamma 0.01`, al netto di `N = 1`; il pacchetto di T-L4b andava al contrario)*; **FALLISCONO il controllo di scala di `E_g`** *(la mia `h_k` contiene il vuoto)* **e la caduta nulla a `N = 1`** *(`-1.36e-08`, `137` errori)*; **il cuore `0.1493` SOPRA la cima della banda** | `0c7abd11` *(corsa a `e31bdef4`)* |

- **Lo stato: CANDIDATA** *(proposto)*.
  - **La lettura di Luca:** **la forza minuscola non e' un difetto; conta che si sommi e che arrivi lontano** *(la portata con M-Phi, passo `5`)*.
  - **La condizione per «PRONTA PER IL NUCLEO»** *(il mandato, punto N)*: **A da' (l1) per la forma (a) E G1 da' (e1).**

## 6. IL NUCLEO UNIFICATO E LE ENERGIE DEI REFERTI VECCHI *(Luca `2026-11-12` `14:55`, `15:08`)*

- ### **Le energie per regione e per settore dipendono dalla scelta dello zero;** **fra referti del nucleo vecchio e del nucleo unificato si confrontano solo il TOTALE** *(convertito: `+ pi (M + V)`, entro `1e-14 max(|tot|, pi (M + V))`)*, **`M` e `V`.**
- **Il perche':** **lo zero di v2** *(`energia_pesata.termini_di_h`)* **sposta energia fra archi e nodi; sul toro intero si compensa, al confine di una regione no** *(R-1 di C35-pi, `doc/TASK_HISTORY/2026-11-12_unificazione.md`, sez. `6`)*.

## 7. I COEFFICIENTI DEL MEZZO SPOSTAMENTO *(U6 dell'unificazione; Luca `2026-11-12` `18:28`)*

- **La forma:** **`hop = alpha I + beta S`, `alpha = (1 + z)/2`, `beta = (1 - z)/2` calcolati a parte** *(`primo_ordine/flussi_parziali._alfa_beta`)*.
- **Il codice delle prove:** `csv/solitone/u6_coefficienti.py` *(le forme avvolte in memoria, fuori dal nucleo)*; **il referto** `doc/referti_l2/u6_coefficienti.txt` *(`cd89b710`; le uscite grezze `925e1f70`)*.

| la forma | la deriva di `Lambda` per tick | il rapporto con oggi | la rms di `rho` dopo `1000` tick | la cassetta | lo stato |
|---|---|---|---|---|---|
| **oggi** | `+3.7e-16` | `1` | `0` | `107/108` *(D6)* | ### **IN USO** *(Luca: la continuita' al bit coi riferimenti)* |
| **k1** `|z| = 1` | `-2.3e-15` | `-6.18` | `9.9e-13` | `99/108` | **SCARTATA** *(peggio)* |
| **k2** `alpha + beta = 1` | `+3.7e-16` | `+1.0000` | `0` *(al bit)* | `107/108` | **SCARTATA** *(identica a oggi)* |
| **k3** `I - beta (I - S)` | `-2.1e-17` | `-0.056` | `4.4e-13` | `99/108` *(8 confronti al bit coi riferimenti registrati)* | ### **CURA PRONTA** *(quando la deriva pesa, o si rifa' la base; con la ri-registrazione dichiarata dei riferimenti)* |
