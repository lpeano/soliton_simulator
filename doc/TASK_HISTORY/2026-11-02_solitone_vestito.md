# 2026-11-02 — IL SOLITONE VESTITO DEL SUO VUOTO *(il mandato di Luca delle `01:04`, con la CORREZIONE delle `01:06`; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]], [[LIBRO-DEI-CONTI]], [[VUOTO-SUL-FONDO]])*

> **La domanda di Luca:** esiste uno stato fermo di materia **e** vuoto insieme, cioe' uno stato che il tick rida' a meno di due fasi *(`e^{-i mu s}` sulla materia, `e^{-i nu s}` sul vuoto)*? Se esiste, regge col vuoto vivo meglio di BG-F-0.15?
>
> **La correzione delle `01:06`** *(vale questa versione, [[PRECEDENZA-IN-CODA]])*: **lo scopo e' il TEMPO DI VITA**, non un solitone perenne *(la materia e' metastabile, Luca `2026-10-30` `20:41`)*.
> - In ogni lettura il referto da' **il tempo di vita** con la soglia della decisione `9`, per lo stato vestito e per BG-F-0.15. **Il riassestamento iniziale va separato dalla perdita lenta.**
> - **`(v2)` non e' un fallimento:** e' il tempo di vita pulito, il numero per la voce `27`.
> - Se il passo `2` trova un'uscita verso il vuoto, il referto dice **da quali parametri dipende il suo margine** *(`s`, `N`, `g`)*.

## 1. LE PREMESSE DAL CODICE *(a `52f216ff`)*

### Tre premesse del mandato che il codice e i dati committati NON confermano

- **(P-a) La partenza di BG-F-0.15 NON e' uno stato fermo, nemmeno a vuoto congelato.** `_vuoto_vivo_B.partenza` la costruisce come **l'inviluppo** di `pK` per la scelta migliore della coppia *(`CO.inviluppo`)*, **senza Newton**. Il suo residuo per tick, nel primo pezzo committato *(`doc/referti_l2/vuoto_vivo_B/BG-F-0.15_000000.jsonl`, `info.residuo`)*, e' **`3.29e-2`**; `mu = 4.161868161822483`.
  - **E a vuoto congelato BG-F-0.15 respira:** in `respiro_congelato.txt` `|D|/|psi0|` vale `1.0e-1` a tempo `3`, e fra `1.25` e `1.92` dopo. Regge *(cuore e `w` fermi)*, ma **non e' fermo**: e' lo «stato che respira» della strada (A).
- **(P-b) Il Newton su `B` a `Gamma` a vuoto congelato non e' mai arrivato a convergenza.** In `doc/referti_l2/consolida_B/vincolo_e05.json` *(eps `0.5`, vuoto uniforme, la scelta migliore col vincolo sul partner)* il residuo si ferma a **`1.16e-5`** dopo `30` passi, contro la soglia **`LP.SB.TOLL_RES = 1e-9`** *(`_strada_b_r`)*. A eps `0` *(`vincolo_e0.json`)* si ferma a `1.12e-4`.
  - Fra gli stati fermi committati, quello convergente e' **(R)** di `_livelli_piatti` *(`N 1e6`, residuo `4.7e-10`; `doc/BANDE_PIATTE.md`)*, **non** `B` a `Gamma`.
- **(P-c) La soglia della decisione `9` su BG-F-0.15 non misura una vita.** `t_vita` e' il primo `tau` con `|D|/|psi0| >= 1e-2`, con `D = e^{i mu s t} psi(t) - psi0`. Su uno stato non fermo **`D` cresce dal primo tick**: col residuo `3.3e-2` per tick, il primo campione *(tempo `3.0`)* ha gia' `|D|/|psi0| = 1.0e-1`, a vuoto vivo **e** congelato.
  - `doc/BANDE_PIATTE.md` *(la riga della sez. `6` su `1.13e-4`)* lo aveva gia' scritto: **«la soglia su `|D|` totale non distingue i due casi»** *(la deriva in `B` di uno stato non fermo, contro un'uscita)*.

### Che cosa ne segue, PRIMA del codice

- **Il DEVE «il controllo positivo: lo stesso Newton col vuoto CONGELATO ritrova lo stato di BG-F-0.15 entro la soglia» non puo' passare cosi' come e' scritto.** BG-F-0.15 non e' un punto fisso, e su `B` a `Gamma` a vuoto congelato non e' noto nessun punto fisso a `1e-9`.
- **Il tempo di vita di BG-F-0.15 con la soglia `9`** esce `<= 3.0` *(il primo campione)*: misura la non-stazionarieta' della partenza, **non** la perdita lenta. **Separare il riassestamento dalla perdita lenta** vuole una definizione che oggi non c'e'.
- **Sono due decisioni di Luca, non mie:**
  - che cosa fa da controllo positivo del Newton;
  - come si separa il riassestamento dalla perdita lenta.

  **Quindi: il passo `2` si fa** *(e' indipendente da queste premesse, e Luca lo vuole prima di ogni corsa)*; **poi FERMO, prima di scrivere il Newton.**

### Il vuoto nel tick, dal codice

- **L'ordine** *(`composizione.ORDINE`, `14` pezzi)*: `MATERIA-VUOTO`, `FASE-VUOTO`, `MONETA-SPIN`, `GROVER`, `SPOSTAMENTO`, `GROVER-VUOTO`, `SPOSTAMENTO-VUOTO` **x2**, poi lo specchio.
- **`CAMM-FASE-VUOTO`** ha generatore `cs_primo(Lambda) * (...)`, **nullo con `cs` spento** *(la scena di BG-F-0.15)*.
- **`CAMM-MATERIA-VUOTO`** con `S1` ha `alpha = beta = 0` **dove `rho = 0`**.
- **Quindi, con `psi = 0`, il tick sul vuoto e' LINEARE:** `GROVER-VUOTO` e `SPOSTAMENTO-VUOTO`. **Linearizzare attorno a `F0` e' prendere questo operatore.** Lo verifico numericamente, non lo suppongo.
- **`F0`** *(`_vuoto_sul_fondo.fondo_uniforme`)*: `+valore` alla coda di ogni arco, `-valore` alla testa, **costante per direzione**. Ogni nodo ha **una coda e una testa per ognuna delle `3` direzioni**: `6` estremita' per cella, quindi **`6` bande del vuoto**.
- **`phi_h` e' ordinato per ARCO** *(`2a`, `2a+1`)*, non per nodo: **la struttura a celle si ricostruisce** da `inc.nodo` e dalla direzione di ogni arco *(come in `fondo_uniforme`)*, **e si verifica** *(`V2`)*.

### Cosa NON so

- Se `F0` sia un autostato esatto del tick del vuoto *(`nu` e il suo residuo li misura `V3`)*.
- **Una mia lettura fisica, dichiarata e da non usare come criterio:**
  - in uno stato fermo congiunto la materia entra nel vuoto **solo attraverso `rho = |psi|^2`** *(`alpha`, `beta` dipendono da `rho` e `Lambda`)*;
  - `rho` in uno stato fermo **non dipende dal tempo** e non porta `mu`, quindi il vuoto e' forzato alla **sua** frequenza `nu`;
  - `mu` arriva nel vuoto solo se `rho` oscilla, cioe' attraverso i **battimenti** della materia *(per esempio il respiro)*.

  **Il confronto di Luca** *(`n mu` contro le bande del vuoto)* **lo faccio alla lettera.** Accanto riporto **dove cade `nu`**, perche' e' l'altra frequenza in gioco.

## 2. LA PROGETTAZIONE

1. **Questo file, da solo.**
2. **La carta** *(uno script nuovo, `csv/_solitone_vestito.py --carta`; niente Newton)*, sulla scena di BG-F-0.15 *(`csv/solitone/protetto.scena_vuoto`, `s 0.15`, `L 81`, il fondo, la forma della tabella)*, col tick intero *(`tick.percorri_tick`, sotto `SF.forma(VC.FORMA)` e `BE.conv(DC.ZERO)`, come `_vuoto_vivo_B.corsa`)*, `psi = 0`:
   - la mappa estremita' -> `(cella, tipo)`; la matrice di Bloch `A_v(k)` `6 x 6` dalle risposte a un impulso, una per tipo, piu' `fft2`;
   - le frequenze `-arg(autovalori)/s` su tutta la griglia `81 x 81`, le `6` bande come intervalli circolari mod `2 pi/s`;
   - `nu` di `F0`; `mu`, `2 mu`, `3 mu` di BG-F-0.15 *(dal jsonl)*; per ciascuno: **dentro o fuori, e il margine** *(la distanza dal bordo di banda piu' vicino; negativo se dentro)*;
   - **la vita di BG-F-0.15 con la soglia `9`**, dai campioni `D` committati di `_vuoto_vivo_B` *(il primo `tau` con `|D|/|psi0| >= 1e-2`)*.
3. **Il referto della carta**, la relazione, l'esito. **FERMO**, con le domande.

**Cosa mi farebbe FERMARE prima:** `V1`-`V4` non passano *(la carta non e' affidabile)*.

## 3. I CRITERI

**Del mandato** *(sul Newton e sulla corsa: per il passo `4`, non per questo giro)*:
- `M` e `V` entro `1e-10`;
- lo stato vestito rida' se stesso entro la soglia;
- il controllo positivo;
- il libro dei conti col `par`;
- nessuna modifica al nucleo, nessun peso tarato, un processo alla volta;
- se il Newton non converge: FERMO.

**Della carta** *(miei, scritti prima)*:

| | criterio | |
|---|---|---|
| `V1` | con `psi = 0` il tick sul vuoto e' lineare: `|T(F0 + a e) - T(F0) - T(a e)| / |T(a e)| <= 1e-10`, `e` un vettore casuale | DEVE |
| `V2` | `A_v` ricostruisce il tick: `T(phi)` per un `phi` casuale contro `ifft(A_v fft(phi))`, scarto relativo `<= 1e-12` | DEVE |
| `V3` | `A_v(k)` unitaria a ogni `k` entro `1e-12`; `F0` autostato del tick, residuo `<= 1e-12` | DEVE |
| `V4` | il rivelatore «dentro una banda» trova `nu` **dentro o sul bordo** *(margine `<= 1e-9`)*; `V4-F`: una frequenza nel mezzo del gap piu' largo e' **fuori** | DEVE / DEVE FALLIRE |

## 4. LE LETTURE *(di Luca, scritte prima)*

- **(v1)** lo stato vestito esiste e col vuoto vivo `w` resta limitato.
- **(v2)** esiste, ma col vuoto vivo si allarga come BG-F: il tempo di vita va misurato *(voce `27`)*. **Non e' un fallimento.**
- **(v3)** il passo `2` trova `mu` o `n mu` dentro una banda del vuoto: e' un'uscita verso il vuoto.
- **(v4)** il Newton non converge.
- **(v5)** altro.

## 5. LA STELLA POLARE

1. **`A14`:** non si tocca. Nessuna legge cambia: e' una misura.
2. **Il gradino:** una lettura sulla carta *(lo spettro lineare del vuoto)*.
3. **Numeri e leggi:** nessuno nuovo. Le soglie `V1`-`V4` sono di arrotondamento.
4. **Il verso:** non si applica.
5. **Emergente o imposto:** se c'e' un'uscita verso il vuoto, emerge dallo spettro del tick, non e' imposta.

## 6. TODO

1. Questo file, committato **DA SOLO**.
2. `csv/_solitone_vestito.py` *(`--carta`)* e la riga d'inventario, committati prima della corsa.
3. La carta, una corsa: `python csv/_solitone_vestito.py --carta > doc/referti_l2/solitone_vestito_carta.txt`.
4. La relazione, l'esito qui, la MAPPA *(voce `27`)*. **FERMO** con due domande:
   - il controllo positivo del Newton;
   - la separazione riassestamento / perdita lenta.
5. *(Dopo Luca)* il modulo del Newton congiunto in `csv/solitone/`, i suoi test, `D6`, la corsa del passo `4`, il referto `doc/referti_l2/solitone_vestito.txt`, `CHIUDERE_LE_USCITE`.

## 7. L'ESITO

*(scritto dopo la corsa della carta, a `922279a5`; il referto `doc/referti_l2/solitone_vestito_carta.txt`)*

- **La progettazione e' cambiata prima del codice:** la carta sta nella libreria *(`csv/solitone/vuoto.py`, `test_vuoto.py`, `carta_vuoto.py`)*, non in `csv/_solitone_vestito.py`. **Il motivo:** il lavoro nuovo passa solo da `csv/solitone/` *(Luca `2026-11-01` `16:52`)*.
- **`V0`-`V4` passano:** la linearita' `4.3e-16`, la ricostruzione `7.7e-16`, l'unitarieta' `4.4e-16`, il residuo di `F0` `7.6e-15`.
- **Le bande del vuoto:**
  - quattro piatte *(due a `0`, due a `-pi`)* e due dispersive larghe `1.5817` *(`[pi - 1.58, pi]` e `[-pi, -pi + 1.58]`)*; coprono il `7.55%` del cerchio mod `2 pi/s`;
  - `nu` di `F0` e' `-pi`, sul bordo.
- **`mu`, `2 mu`, `3 mu` cadono fuori** *(margini `+1.0203`, `+5.1821`, `+9.3440`)*: **non e' `(v3)`.**
- **La vita di BG-F-0.15 con la soglia `9` e' `3.0`**: il primo campione, come previsto in `(P-c)`.
- **Il passo `3` (il Newton congiunto) NON si fa** *(Luca `01:13`)*: lo sostituisce l'accensione lenta, il mandato successivo in coda. **La domanda sul controllo positivo cade con lui.** La domanda sulla separazione riassestamento / perdita lenta passa al mandato dell'accensione.
