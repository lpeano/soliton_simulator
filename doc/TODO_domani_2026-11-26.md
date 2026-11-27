# IL TODO PER DOMANI, 2026-11-26 *([M0925], DECISIONE DI LUCA `09:25` del 2026-11-25, arrivata dalla posta, `25b17e3f`)*

> **Oggi si sospende.** Niente corse e niente codice nuovo. **Le corse di domani partono solo su «leggi la posta».** [[PROGETTO-MITOSI]]

## Lo stato alla sospensione *(2026-11-25, `09:28`)*

- **La coda:** il lanciatore `coda_m1446.py` e' uscito dopo il giro 3 di [M0414] *(chiuso alle `07:18:33`, uscita `0`)*, senza altro da lanciare. **Nessun processo python degli script di `doc/referti_l2/` e' aperto** *(verificato alle `09:28`)*. Il worktree di `lapse-u` e' pulito.
- **[M0414], il punto fisso accoppiato** *(`doc/referti_l2/fondo_puntofisso_chi_v2.txt`)*: tre giri; C non passa *(i respiri `0.572`, `0.695`, `0.412`)*; **D: il respiro e' un modo normale.** Al giro 3: `w` medio circa `4.5`, `omega` medio `0.0833`, la profondita' del pozzo `-102.3`, **`Omega_b = 2 pi/2500 = 2.513e-03` per tick**, `max|chi|` `114.0` *(`-3.80%` dal giro 2)*.
- **[M0137], la coppia dal giro 3:** i casi noti passano *(`due_corpi_fondo_v4_noto.txt`)*, **ma il vuoto non si compone**: il fit del fondo su `phi_v` da' `a = -0.0065+0.0182i`, residuo `52.17`; `c0` `-1.5627`. **Le corse d1', d2', d3' non sono partite.**
- **[M0237], la mitosi** *(ramo `mitosi`, worktree `C:\Users\lpeano\wt_mitosi`)*: pezzi 0-2 fatti *(H cala, `|dH|/|H| 1.397e-03`, e va nelle nascite)*; **pezzi 3 e 4 fermi:** K3 fallito *(MITOSI non viene da `mitosi_lunga.corsa`)*, K4 fallito *(la divisione per `max(rho) = 0` nel residuo di Gauss)*.

## Gli stati di partenza *(lo sha1 dei byte, i primi 12 caratteri, dai file `.sha1`)*

| pezzo | lo stato | sha1 |
|---|---|---|
| A, B *(psi e chi)* | `E:/soliton_simulator/controllo/M0414/puntofisso_accoppiato/giro_3/partenza_giro_4.npz` | `bee0464d6d2e` |
| A, B *(il giro 3)* | `E:/soliton_simulator/controllo/M0414/puntofisso_accoppiato/giro_3/giro.json` | `a14be2e5b46b` |
| B *(`phi_v` fresco)* | il vuoto della scena *(`Z["phi_v"]` di `triangolo_chi_v4.scena`)* | -- |
| D2 *(il vuoto puro)* | `E:/soliton_simulator/controllo/M0237/vuoto/vuoto_35976.npz` | `1b265f08` |
| D1, D2 *(la sorgente)* | `E:/soliton_simulator/controllo/mitosi_rami/TRONCO/prima_nascita_35976.npz` | `abbdcaca` |

## Il piano *(la via: DECISIONE DI LUCA `09:25`)*

### A. La diagnosi del vuoto del giro 3 *(a costo zero, letture su `partenza_giro_4.npz`)*
- `rho_phi` lontano *(`d > 45`)* contro il vuoto fresco a `phi_v`: il rapporto per anello `[45, 60)`, `[60, 75)`, `[75, 90)`;
- il gradiente di fase di `phi` lontano: `J_phi` radiale e tangenziale per anello *(i nodi giusti: `(m1 +- 1, m2)` lungo `x`, `(m1 +- 1, m2 +- 2)` lungo `y`)*;
- `chi(d)` per anello: dove torna a zero, se torna *(`chi_fondo` `-23.95` a `d > 45`)*;
- **prima dei numeri, il caso noto (V1):** sul vuoto fresco a `phi_v` il rapporto e' `1` e la corrente `0` entro `1e-9`;
- il referto `doc/referti_l2/vuoto_giro3.txt`.

### B. La coppia: `psi` e chi dal giro 3, `phi` FRESCO
- **la semina:** `psi_A + psi_B` *(la copia traslata di `(+24, +48)`)*; `chi_A + chi_B - chi_fondo` *(`chi_fondo` = la media di chi a `d > 45` dello stato del giro 3)*; **`pi = 0`**; **`phi = a phi_v` FRESCO, con `a = 1` e la fase dichiarata** *(il fit non si fa piu')*; i campi `A`, `E` da Gauss sullo stato composto;
- **lo script nuovo** `doc/referti_l2/due_corpi_fondo_v6.py` *(v4 e v5 non si toccano)*;
- **i casi noti:** (G) la geometria al bit; (T) le masse entro `1e-9`; (K2) d2' = d1' a `k 0` al bit con `kappa 0`; **(V2) il vuoto composto a `k 0` e' `phi_v` al bit lontano da entrambi** *(`d > 45`)*;
- **le corse:** d1' *(due, chi on)*, d2' *(due, chi off, lo stesso `c0`)*, d3' *(uno, chi on)*; `6000` tick, stati ogni `250`, tre processi in coda;
- **le letture** *(`due_corpi_lettura_v2`, i nodi giusti)*: (i) `d(k)` e `a` per finestra di `500`; (ii) `J` radiale `[16, 32)`; (iii) `rho_phi` vicino alla massa; (iv) `chi(k)`; (v) `w`, `omega`, il respiro. Per tutte e tre.

### C. Il criterio di lettura *(DECISIONE DI LUCA `09:25`)*
- **d3' e' il controllo:** d1' si legge **solo sulle finestre** in cui d3' ha `w` e `omega` **entro il `5%`** del giro 3 *(`w 4.5`, `omega 0.0833`)* **e il pozzo entro il `10%`** *(`-102`)*. **Se nessuna finestra passa, il verdetto su d1' non si da', e si dichiara;**
- **d2'** *(chi off)* deve dare `d(k)` fermo entro `0.5` nodi, **altrimenti nessun verdetto**;
- nessuna soglia diversa senza DECISIONE DI LUCA *(hh:mm)*.

### D. La mitosi [M0237] *(ATTESA DI LUCA: si fanno solo su una decisione di domani)*
- **D1** *(a costo zero)*: da quale script e quale commit viene la corsa MITOSI *(git log sui file, i meta degli `npz`, i TIMBRO del log)*. Si dichiara nella carta *(`doc/CARTA_mitosi.md`)*. Se non e' `mitosi_lunga.corsa`, K3 si riscrive contro la via vera. **Gia' visto:** il log `mitosi_rami/log_MITOSI.txt` ha «lo scatto del tronco», `gauss_acc` e `|Ec|`, che `mitosi_lunga.corsa` non stampa;
- **D2** *(una scelta da dichiarare)*: per il vuoto puro *(`psi = 0`)*, il residuo di Gauss senza la normalizzazione a `rho`, dichiarato nella carta PRIMA, e K4 rifatto.

## Le decisioni

- **PRESE** *(DECISIONE DI LUCA `09:25`)*: la via A, B, C; `phi` fresco con `a = 1`; d3' come controllo e le sue soglie *(`5%`, `10%`)*; d2' fermo entro `0.5` nodi; la sospensione di oggi.
- **APERTE** *(ATTESA DI LUCA)*:
  - D1 e D2 della mitosi;
  - **la fase dichiarata di `phi` fresco**: `phi_v` cosi' com'e' *(fase `0`)*, oppure `c(t) phi_v` al tick della scena;
  - le domande ancora sul tavolo: [M0105-02] *(il controllo di struttura: il riferimento `da79cc1` o l'equivalenza dei nomi)*; [M2330] *(la geometria di d1 e d2, chi fuori equilibrio)*; [M2210-r4] *(il bordo e il suo vuoto di riferimento)*; E(p) *(il segno di `E_w`)*; C1, D, [M0140].

## Le previsioni del guardiano *(dalla posta, prima)*

- P1 *(`65%`)*: `rho_phi` lontano dal giro 3 sotto l'`80%` del vuoto fresco;
- P2 *(`60%`)*: `J_phi` lontano radiale verso l'oggetto, non tangenziale;
- P3 *(`55%`)*: in d3' `w` e `omega` entro il `5%` del giro 3 su almeno `6` finestre su `12`;
- P4 *(`70%`)*: d1' si avvicina, d2' fermo;
- P5 *(`50%`)*: sulle finestre valide, K fra `0.8` e `1.2`;
- P6 *(`60%`)*: D1 trova che MITOSI viene da un'altra via.
