# 2026-11-02 — IL SOLITONE CHE SI VESTE DA SOLO: L'ACCENSIONE LENTA DEL VUOTO *(il mandato di Luca delle `01:13`; [[PIANO-2D-3D]], [[VUOTO-SUL-FONDO]], [[LIBRO-DEI-CONTI]], [[PRECEDENZA-IN-CODA]])*

> **L'idea di Luca:**
> - si parte a vuoto congelato e si accende la dinamica del vuoto poco a poco, con un fattore `lam(t)` da `0` a `1` su TUTTO l'aggiornamento del vuoto;
> - il solitone si veste del suo vuoto da solo, senza Newton;
> - il tempo di vita si misura dopo, sul solitone vestito, **separando la rampa dalla perdita lenta**.
>
> **Sostituisce il Newton congiunto** del mandato delle `01:04`, dopo la carta *(`4d1c2b65`)*.

## 1. LE PREMESSE DAL CODICE *(a `4d1c2b65`)*

### Il tick, i pezzi del vuoto, `dtau`

- **Il tick:** `tick.percorri_tick` percorre i `14` pezzi di `composizione.ORDINE` e chiama `mot.operatori[nome](st, par, frazione)`, con `nome` da `tick.OPERATORE`.
- **I pezzi del vuoto** *(`_solitone_vuoto_congelato.VUOTO`)*: `CAMM-GROVER-VUOTO`, `CAMM-SPOSTAMENTO-VUOTO`, `CAMM-FASE-VUOTO`.
  - Grover e spostamento sono **flussi parziali**: `G(theta) = P_u + e^{i theta}(I - P_u)` e `alpha I + beta S`, con `theta` da `z_nodo(mot, frazione)` e `z_arco(mot, frazione)`.
  - **Scalare `dtau` di un pezzo e' passargli `frazione * lam`.** A `lam = 1` e' la stessa frazione al bit *(`x * 1.0 = x`)*.
  - `CAMM-FASE-VUOTO` ha generatore nullo con `cs` spento: scalato o no, non fa niente.
- **La rotazione gemella `beta`:** `materia_vuoto.applica` ruota `psi` di `alpha * dtau * f` e `phi` di `be * dtau * f`, con `(al, be) = pezzi(rho, lam)`.
  - ⚠ **Sotto `_screening_forme_s3.forma` *(come girano le corse di `csv/`)* `MV.pezzi` e' SOSTITUITO** dalle espressioni di `csv/`. Quindi **la `beta` si scala sostituendo `MV.pezzi` con una funzione che restituisce `(al, lam * be)`** di quello attivo, non `MV.beta`.
  - La diagnostica qui sotto l'ha mostrato: **sostituendo `MV.beta` la scala non arrivava.**
- ⛔ **Il nucleo rifiuta la frazione `0`** *(`flussi_parziali._frazione_valida`: «una frazione di passo sta in `(0, 1]`»)*. **Con `lam = 0` i pezzi del vuoto non si applicano**: un pezzo di `dtau` nullo e' un pezzo che non gira, come nel tick congelato.
  - Nella rampa `lam > 0` sempre *(sotto)*: **`lam = 0` serve solo al controllo.**
- **Il tick congelato** *(`_congelato_lungo.avanza` = `_deriva_congelato.tick_congelato` con `salta = VC.VUOTO`)*: salta i tre pezzi del vuoto; **`CAMM-MATERIA-VUOTO` gira intero** *(ruota anche `phi` di `beta`)*; **`phi` si rimette a `phi0` a fine tick.**

### ⛔ UN DEVE DEL MANDATO CHE NON PASSA, MISURATO PRIMA DEL CODICE

**DICHIARO L'ORDINE:** ho fatto una diagnostica **prima** di questo task history, per sapere se lo schema si poteva scrivere *(nello scratchpad; copiata in `doc/referti_l2/accensione_lenta/diag_lam01.py.txt`, l'uscita in `diag_lam01.txt`)*. Sulla scena di BG-F-0.15, dalla sua partenza, `20` tick, il tick dell'accensione contro il riferimento:

| | `psi_h` | `phi_h` | `Lambda` |
|---|---|---|---|
| `lam = 1` contro `tick.percorri_tick` | **al bit** | **al bit** | **al bit** |
| `lam = 0` contro `_congelato_lungo.avanza` | **diverso, `1.28e-14`** | **al bit** | diverso, `1.78e-15` |

- **Il perche', dal codice:**
  - il congelato fa girare `CAMM-MATERIA-VUOTO` intero, quindi a meta' tick `phi` e' ruotato di `e^{-i beta dtau/2}`, e rimesso a `phi0` solo alla fine;
  - il secondo `CAMM-MATERIA-VUOTO` legge `Lambda = |e^{i theta} phi0|^2`, che **in aritmetica esatta e' `|phi0|^2`**, ma differisce di un ulp;
  - a `lam = 0` *(`beta` scalata a zero)* `phi` non ruota mai, quindi `Lambda` e' `|phi0|^2` esatto.
  
  **La differenza e' di arrotondamento, non di fisica.**
- **Quindi il DEVE «con `lam = 0` e' `_congelato_lungo.avanza` AL BIT» NON PASSA** con lo schema del mandato *(«`lam` scala anche la rotazione gemella `beta`»)*. **FERMO: decide Luca.**
- **Le possibilita', con la mia raccomandazione** *(non scelgo)*:
  - **(i)** *(la raccomando)* il criterio diventa: con `lam = 0`, `phi` resta `phi0` **al bit** a ogni tick *(passa)*, e `psi` coincide con `avanza` **entro l'arrotondamento**, con la causa dichiarata *(`1.3e-14` su `20` tick)*. Lo schema resta quello del mandato.
  - **(ii)** con `lam = 0` il tick dell'accensione **e'** `avanza` *(un ramo a parte)*. Il DEVE passa **per costruzione**, cioe' e' un **FALSO-UNO**: non verifica il codice che gira nella rampa.
  - **(iii)** la `beta` non si scala; `phi` si rimette a `phi0` a fine tick con un peso `1 - lam`. Ma questo e' **un'altra legge del vuoto**, e il mandato non la chiede.

### La seconda decisione aperta: la vita con la soglia `9`, «rampa» contro «perdita lenta»

- La soglia della decisione `9`: il primo `tau` con `|D|/|psi0| >= 1e-2`, con `D = e^{i mu s t} psi(t) - psi0`. **Su BG-F-0.15 da' `3.0`, il primo campione** *(la carta, `4d1c2b65`)*: misura la deriva di una partenza non ferma.
- **La mia proposta per separare le due parti** *(da confermare)*:
  - **la rampa:** `D` rispetto alla partenza *(`psi0` = BG-F-0.15, `mu` = il suo)*, su `0 .. T_acc`;
  - **la perdita lenta:** `D` rispetto al **solitone vestito**, cioe' allo stato a `T_acc`, con `mu` di Rayleigh del tick intero su quello stato, da `T_acc` in poi.
  - **Il limite, gia' scritto** *(`doc/BANDE_PIATTE.md`, sez. `6`)*: anche lo stato vestito respira, e la soglia su `|D|` totale non distingue il respiro da un'uscita. **Le bande di `D` lo dicono.**
  - **Accanto, in ogni caso:** la pendenza dell'alone e del cuore, e l'estrapolazione del cuore a meta' *(come `respiro_congelato`)*.

### Altri fatti

- **La corsa viva di riferimento** *(BG-F-0.15)*: `_respiro_congelato.serie_viva`, cioe' `_vuoto_vivo_B` *(`0 .. 3000`)* piu' `_respiro_sul_fondo` *(`3000 .. 10000`)*.
  - ⚠ **Il suo libro dei conti e' a eps `0`** *(`_vuoto_vivo_B.corsa` non passa il `par`)*. Col `par` ci sono **solo l'inizio e la fine** *(`_respiro_congelato --ripartizione`)*. **Il confronto del libro blocco per blocco sara' fra conti diversi:** si dichiara.
- **`e_K`** con la libreria: `protetto.e_K` *(il legame spento)*, `-4.7122750003546425`.

## 2. LA PROGETTAZIONE *(dopo la decisione di Luca)*

1. **Questo file, da solo**, con la diagnostica.
2. **`csv/solitone/accensione.py`** *(nuovo)*:
   - `tick_acceso(z, lam)`: il ciclo di `percorri_tick` *(`mot.apri_tick`, `CM.ORDINE`, `TK.OPERATORE`, `mot.chiudi_tick`)*. I pezzi di `VC.VUOTO` con `frazione * lam`, saltati a `lam = 0`; `MV.pezzi` con `(al, lam * be)`. **Il palindromo resta palindromo:** ogni pezzo del vuoto ha la stessa scala nelle due meta'.
   - **La rampa** *(scelta e dichiarata qui, prima)*: `lam_k = sin^2(pi k / (2 K))`, `K = T_acc/s` tick, `k = 1 .. K`. `lam_K = 1` esatto. Dopo, `tick.percorri_tick` *(il tick intero del nucleo)*.
   - le corse a pezzi *(come `_vuoto_vivo_B.corsa`, la ripresa al bit)*; le misure di `V.misura`, il libro col `par`, `D` e le bande.
3. **`csv/solitone/test_accensione.py`:** `lam = 1` al bit su qualche tick; `lam = 0` secondo la decisione; nella cassetta. `D6` al commit.
4. **Le corse, una alla volta:** `T_acc 1000` fino a `6000`; `T_acc 2000` fino a `7000`.
5. **Il referto** `doc/referti_l2/accensione_lenta.txt`, la MAPPA *(voci `1` e `27`)*, la relazione.

## 3. I CRITERI *(del mandato)*

| | criterio | |
|---|---|---|
| `A1` | con `lam = 1` il tick dell'accensione e' il tick intero AL BIT *(su alcuni tick)* | DEVE: **passa nella diagnostica** |
| `A2` | con `lam = 0` e' `_congelato_lungo.avanza` AL BIT | DEVE: ### **NON PASSA** *(sopra)*: decide Luca |
| `A3` | `M` e `V` entro `1e-10` in tutte le corse | DEVE |
| `A4` | il libro dei conti col `par` della corsa *(eps `0.5`)* | DEVE |
| `A5` | nessuna modifica al nucleo, nessuna legge nuova, nessun peso tarato, un processo alla volta | |
| `A6` | se il solitone si scioglie durante la rampa: FERMO | |

## 4. LE LETTURE *(di Luca, scritte prima)*

- **(a1)** dopo la rampa il solitone si assesta e perde piu' lentamente di BG-F: il numero pulito e' quello dopo la rampa.
- **(a2)** dopo la rampa perde come BG-F: la perdita e' del vuoto vivo; il tempo di vita e' quello *(voce `27`)*.
- **(a3)** `T_acc 1000` e `2000` danno risultati diversi: l'accensione non e' ancora lenta.
- **(a4)** altro.

## 5. LA STELLA POLARE

1. **`A14`:** non si tocca. Nessuna legge cambia: si scala il `dtau` dei pezzi del vuoto *(che e' gia' un argomento dei pezzi)*.
2. **Il gradino:** una corsa con un protocollo di partenza; il risultato fisico e' **il tasso dopo la rampa**.
3. **Numeri e leggi:** due numeri di protocollo, `T_acc` *(`1000`, `2000`, del mandato)* e la forma della rampa *(`sin^2`, dichiarata)*. **Non sono parametri del modello:** il criterio `(a3)` controlla che il risultato non ne dipenda.
4. **Il verso:** non si applica.
5. **Emergente o imposto:** il vestito del solitone **dovrebbe emergere** dalla dinamica, non da un Newton.

## 6. TODO

1. Questo file, con la diagnostica, committato **DA SOLO**.
2. *(In coda, solo scrittura:)* la MAPPA, voce `33` *(Luca `01:17`-`01:19`)* e la sua aggiunta *(Luca `01:23`-`01:28`)*; la voce `32`.
3. **FERMO:** la decisione su `A2` e la definizione della vita dopo la rampa.
4. *(Dopo Luca)* i passi `2`-`5` della progettazione.

## 7. L'ESITO
