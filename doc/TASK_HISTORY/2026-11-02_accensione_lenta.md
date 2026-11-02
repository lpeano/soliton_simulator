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

## 6-bis. LE DECISIONI DI LUCA *(`2026-11-02`, dopo `25614c34` e `4d1c2b65`)* E IL COMPLETAMENTO DELLA CARTA

> **Le premesse della sez. `1` restano come sono:** questa sezione le ANNOTA con le decisioni.

### Le decisioni

1. **`A2`: la (i).**
   - Con `lam = 0`, `phi` resta `phi0` **AL BIT** a ogni tick.
   - `psi` coincide con `_congelato_lungo.avanza` **entro l'arrotondamento**, con la causa dichiarata: la rotazione di `beta` e il ritorno danno un ulp sul modulo, `1.3e-14` su `20` tick.
   - Lo schema resta quello del mandato.
   - **La tolleranza che scrivo in `test_accensione`, dichiarata qui prima:** `|psi - psi_avanza| / |psi| <= 1e-12` su `20` tick. E' cento volte la differenza misurata, e dieci volte sotto la tolleranza di linearita' della carta.
2. **La vita** *(precisazione della decisione `9`)*.
   - **Per i solitoni che respirano, la vita principale** e' il tempo a cui il cuore liscio scende a **META'** del suo valore a `T_acc` *(misurato, o estrapolato e dichiarato come tale)*.
   - Accanto, la pendenza dell'alone e del cuore.
   - **La soglia `|D|/|psi0| >= 1e-2`** resta per il regime per cui e' nata *(un seme esponenziale su uno stato fermo)*. Qui e' una misura **accessoria**, con le bande di `D`: rispetto alla partenza sulla rampa, rispetto allo stato a `T_acc` dopo.
   - Una riga nella MAPPA accanto alla decisione `9`.
3. **La carta, il completamento** *(prima delle corse; l'errore del guardiano `n.90`: la carta chiedeva solo `n mu`)*. **I passi sono sotto.**
4. **Il libro dei conti di riferimento di BG-F a eps `0`, blocco per blocco:** si dichiara. Inizio e fine col `par`, come gia' fatto.

### Le premesse dal codice per il completamento *(cosa credo prima di guardare, e cosa NON so)*

- **I campioni committati del cuore di BG-F-0.15 vivo** *(`_vuoto_vivo_B`)* sono ogni `OGNI = 10` tick, cioe' ogni `1.5` unita' di tempo. Il limite di Nyquist e' un periodo di `3.0`.
  - Un periodo vero di `~4.07` starebbe sopra Nyquist. Ma dai soli campioni non si distingue dai suoi alias `1/|1/T +- k/1.5|` *(per `4.07`, con `k = 1, 2`: `2.375`, `1.096`, `0.919`, `0.633`)*.
  - ⚠ **Ho guardato i campioni committati prima di scrivere questo file** *(dichiarato: uno spettro nello scratchpad, non committato)*. Nei primi campioni il cuore **alterna a ogni campione**, cioe' alla frequenza di Nyquist. Poi domina una variazione lenta *(centinaia di unita' di tempo)*.
  - **Quindi `Omega` non si legge dai campioni committati:** serve una serie **densa**.
- **La serie densa:** il tick intero del nucleo da BG-F-0.15 *(la scena e la partenza di `_vuoto_vivo_B`, come la corsa)*, il cuore liscio **a ogni tick** *(passo `0.15`, Nyquist `0.3`)*. Due finestre:
  - **(W1)** dalla partenza, `0 .. 600` unita' di tempo *(`4000` tick)*. **Il controllo:** i campioni a `t % 10 == 0` coincidono **al bit** con il cuore committato di `_vuoto_vivo_B`.
  - **(W2)** dallo stato finale della corsa viva a `10000` *(`db/respiro_sul_fondo/BG-F-0.15.npz`)*, `300` unita' di tempo *(`2000` tick)*. **Il controllo:** gli `sha` dello stato = `sha_fine` dell'ultimo pezzo committato di `_respiro_sul_fondo`.
- **`Omega`:** il picco dello spettro del cuore liscio *(tolta la tendenza quadratica, finestra di Hann, il picco interpolato con la parabola sui tre punti)*, piu' il periodo dai cambi di segno *(`misure.periodo_dai_cambi`, col passo di `1` tick)*.
  - **Si riportano i primi picchi, non solo il massimo.** Il periodo dai cambi deve stare entro il `5%` del picco: e' un controllo, e se fallisce lo dico.
  - **`Omega` della carta** e' il picco di (W1). Quello di (W2) dice se il respiro cambia nel tempo.
- **Le bande della materia:** `uscite.spettro_scena` *(i gruppi `A`, `B`, `P0`, `Ppi`, dalla scena)*. **Le bande del vuoto:** `test_vuoto` *(come la carta di `4d1c2b65`)*.
- ### ⚠ **UNA COSA CHE IL MANDATO NON DICE E IL CODICE SI'** *(una lettura, non un criterio; decide Luca)*:
  - nel tick la materia entra nel vuoto **solo attraverso `rho = |psi|^2`** *(la rotazione gemella `beta(rho, Lambda)` ruota `phi`)*, e il vuoto entra nella materia solo attraverso `Lambda = |phi|^2`;
  - un'onda del vuoto `delta phi` accanto al condensato `F0` cambia `Lambda` con la frequenza **`nu_v - nu_F0`**, non `nu_v`;
  - **quindi un'uscita che conserva `V` sposta un quanto dal condensato** *(`nu_F0 = -pi`, nelle unita' di `4d1c2b65`)* **all'onda**.

  **Scrivo le due forme, e le riporto tutte e due:**
  - **(L) la lettera del mandato:** `nu_v + E_m` contro `n mu + k Omega` *(mod `2 pi/s`)*;
  - **(C) col condensato:** `E_m +- (nu_v - nu_F0)` contro `n mu + k Omega`. Per le bande laterali sul vuoto da solo: `nu_F0 + k Omega` *(cio' che `rho` porta nel vuoto)* contro le bande del vuoto.
  - ⚠ **Prevedo, prima del conto:** `nu_F0` sta **sul bordo** della banda dispersiva `[-pi, -pi + 1.58]`. Quindi in (C) **`nu_F0 + k Omega` cade dentro quella banda se `0 < k Omega < 1.58`**, cioe' per `Omega` vicino a `2 pi/4.07 = 1.54`. **Un'uscita aperta, se `Omega` e' quello.** Non lo so finche' non misuro.
- **Che cosa NON so:**
  - se il cuore ha un respiro netto o uno spettro largo;
  - se `Omega` dipende dalla finestra;
  - come stimare la **quota** di un'uscita aperta senza l'elemento di matrice dell'accoppiamento.

### La progettazione del completamento

1. **Questo file, da solo.**
2. **`csv/solitone/respiro.py`** *(nuovo)*:
   - `serie_densa`: il tick intero, il cuore liscio a ogni tick, la ripresa da uno stato;
   - `omega`: i picchi e i cambi, col passo;
   - `circolare` *(un intervallo ridotto mod `2 pi/s`)* e `margine_mod`: la distanza di una frequenza da un intervallo sul cerchio, negativa se dentro;
   - `somma`: gli intervalli di Minkowski di due bande.
3. **`csv/solitone/test_respiro.py`** *(nella cassetta)*:
   - (R1) `omega` ritrova un seno noto a ogni tick, entro `1e-6` sulla frequenza;
   - (R1-F) lo stesso seno campionato ogni `10` tick NON ridà la frequenza vera: deve fallire, per l'alias;
   - (R2) `margine_mod`: un punto dentro un intervallo che passa per lo zero del cerchio e' dentro, uno fuori e' fuori, col segno;
   - (R3) `somma` contro il conto a mano su due intervalli.
4. **`D6`** in un commit a se'.
5. **`csv/solitone/carta_respiro.py`** *(il runner)*: (W1), (W2), `Omega`, le bande laterali `mu + k Omega` *(`k = -3 .. 3`)* e le loro armoniche `n (mu + k Omega)` *(`n = 1, 2`)* contro le bande del vuoto; le uscite miste (L) e (C) per `A`, `B`, `P0`, `Ppi`, contro `n mu + k Omega` *(`n = 1, 2`, `k = -3 .. 3`)*; il margine di ognuna; **quale uscita e' aperta**.
6. **La quota, se un'uscita e' aperta** *(dichiarato qui: un ordine di grandezza, non una derivazione)*:
   - dalle righe `D` committate della corsa viva, la parte di `|D|^2/|psi0|^2` nel gruppo di materia dell'uscita;
   - la sua pendenza per `1000` unita' di tempo sul tratto `5000 .. 10000`, contro la pendenza dell'alone *(`~2.5e-3` per `1000`)*;
   - **compatibile** se la pendenza del gruppo e' almeno quella dell'alone *(il gruppo puo' alimentare l'alone)*; **incompatibile** se e' sotto di un ordine di grandezza.
   - Se nessuna uscita e' aperta: **la quota non si confronta**, e lo dico.
7. **Il referto** `doc/referti_l2/solitone_vestito_carta_respiro.txt`, la relazione, la MAPPA *(la riga accanto alla decisione `9`; l'errore `n.90`)*.
8. **Poi l'accensione**, i passi `2`-`5` della sez. `2`, con `A2` secondo la (i) e la vita secondo la decisione `2`.

### Due annotazioni col codice *(scritte quando ho scritto `respiro.py`, prima di ogni numero della scena)*

- **`PERIODI_MIN = 10`:** un picco conta solo se nella finestra ci stanno almeno `10` suoi periodi. Sotto, e' la deriva lenta, che nei campioni committati domina lo spettro *(centinaia di unita' di tempo)*. **E' un limite della finestra, non un parametro del modello.**
- **`R1-F` corretto prima della prova a secco:** il seno di prova di periodo `4.07` campionato ogni `1.5` sta **sopra** Nyquist e si legge giusto, quindi il test non distingueva. **Il seno del test e' quello sotto Nyquist che da' gli stessi campioni radi** *(periodo `2.3755`)*: campionato ogni `10` tick si legge `4.07`.
- **DICHIARO una prova a secco** del runner con `400` tick per finestra, nello scratchpad, prima del commit del codice, per vedere che girasse; le uscite non entrano nel repo.

### Che cosa mi farebbe FERMARE

- **il controllo di (W1) o di (W2) fallisce:** la serie densa non e' la corsa;
- **R1-F passa:** il test dell'alias non distingue;
- **nessun picco netto nel cuore** *(il primo picco non supera di `3` volte il secondo, fuori dalle sue armoniche)*: `Omega` non e' definito. FERMO, e decide Luca come proseguire.

### Le letture *(fissate qui, prima dei numeri)*

- **(r1)** nessuna uscita aperta, ne' (L) ne' (C): l'alone non viene da un'uscita lineare; si passa all'accensione.
- **(r2)** un'uscita (C) aperta col respiro *(`nu_F0 + k Omega` nel vuoto, o una mista)* e quota compatibile: il respiro irraggia, e l'alone potrebbe venire da li'.
- **(r3)** un'uscita aperta ma con quota incompatibile: e' aperta ma non spiega l'alone.
- **(r4)** solo (L) aperta: decide Luca quale forma vale.
- **(r5)** altro.

## 7. L'ESITO

### La carta completata col respiro *(il referto `doc/referti_l2/solitone_vestito_carta_respiro.txt`; il codice `2f3e93f8`, `D6` `49a116d5`)*

- **I controlli passano:** `R1`, `R1-F`, `R2`, `R3`, `V0`-`V4`; (W1) al bit coi `400` campioni committati; (W2) gli `sha` della fine della corsa viva.
- ### ⛔ **FERMO, sul criterio scritto prima:** il primo picco del cuore in (W1) supera il primo non armonico di **`1.58`** volte, non di `3`. **`Omega` non e' definito.**
  - I picchi di (W1): `57.44`, `42.41`, `36.50`, `0.9909`, `0.9829`.
  - I picchi di (W2): `19.54`, `26.18`, `11.70`, `13.29`, `2.029`.
  - **Nessun picco a `~4.07`.**
- **Le bande laterali, le uscite miste e la quota non sono state calcolate.** **L'accensione non e' partita:** decide Luca fra (a), (b), (c) della relazione.
- **La riga finale del referto conta anche il `PUO' FALLIRE`** *(«DEVE fallite: `2`»)*: la DEVE fallita e' una sola. Un difetto del runner, dichiarato.
- **Le letture (r1)-(r5) non si applicano:** la carta si e' fermata prima delle uscite.

## 8. LA DECISIONE DI LUCA DOPO `04b02794` *(2026-11-02)*: la (a), le tabelle per OGNI picco

### Le decisioni *(di Luca, verbatim nella sostanza)*

1. **La (a): niente `Omega` unico.** Le tabelle per **ogni** picco, in tutte e due le finestre (W1) e (W2): i `5` picchi gia' trovati di ciascuna, **piu' quelli fino a `1/10` dell'ampiezza del primo**.
   - per ogni picco `Omega_j`: `n (mu + k Omega_j)` *(`k = -3 .. 3`, `n = 1, 2`)* contro le bande del vuoto attorno a `F0`, col margine *(`respiro.margine_mod`)*;
   - le uscite miste *(un'onda del vuoto piu' un'onda di materia `A`, `B`, `P0`, `Ppi`)* **a `k = 0` SEMPRE** *(non dipendono da `Omega`)*, e con le bande laterali di ogni picco;
   - per ogni uscita aperta: **l'ampiezza del picco che la apre e la quota**, contro l'alone che cresce di `~2.5e-3` ogni `1000`.
2. **La lettura del guardiano, da verificare e non da presumere:** il picco veloce di (W1) *(`Omega 6.341`, `6.392`)* da' `mu - Omega = 39.709`, `39.658` *(mod `41.887902`)*, dentro la banda del vuoto `[38.746309, 40.328044]`: un'uscita verso il vuoto aperta dal respiro veloce. In (W2) i picchi lenti *(`Omega` fino a `0.537`)* con `k = 3` spostano `mu` di `~1.6`, oltre il margine `+1.02`: da controllare.
3. **Il DEVE fallito resta scritto com'e'** *(era un FERMO giusto)*; il conto finale «DEVE fallite: `2`» si corregge in `1` DEVE e `1` PUO' FALLIRE.
4. **Il modulo, il test e il runner dell'accensione lenta nel repo** prima di girare le corse.
5. **Poi le corse dell'accensione lenta** come da mandato *(sez. `2` e `6-bis`)*.

### Le premesse dal codice *(cosa credo prima di guardare, e cosa NON so)*

- **`respiro.omega(y, passo, quanti)`** ordina i massimi locali dello spettro di Hann per altezza e ne rifinisce i primi `quanti`. **Con `quanti = None` li rifinisce tutti** *(`loc[:None]`)*, nello stesso ordine: **i primi `5` sono quelli di `04b02794`, per costruzione** *(la stessa serie, lo stesso codice)*. Lo controllo con il diff delle righe dei picchi fra il referto vecchio e il nuovo.
- **«Fino a `1/10` dell'ampiezza del primo»:** l'ampiezza e' quella **rifinita** *(`a cos + b sin`)*, il primo e' il primo per altezza dello spettro *(`57.44` in (W1), `19.54` in (W2))*. Il numero `1/10` e' di Luca.
- ⚠ **Un massimo locale accanto a un picco forte** *(un lobo della finestra)* si rifinisce entro `+- 1` canale, quindi puo' tornare **sulla stessa frequenza** del picco forte: un doppione. **Due picchi rifiniti entro `1` canale sono lo stesso picco:** si tiene il piu' ampio. **E' una regola sul canale, non un numero nuovo** *(il canale e' `1/finestra`)*.
- **Le bande:** la materia da `uscite.spettro_scena`, il vuoto da `test_vuoto` *(come nella carta di `04b02794`)*. Il margine con `respiro.margine_mod`, il minimo sulle `6` bande del vuoto.
- **Le uscite miste a `k = 0`** non dipendono da `Omega`: si stampano **una volta**. **(L), (C+), (C-)** come scritto nella sez. `6-bis`; `n = 1`, `k = 0`, il gruppo del solitone in (C) e' **per costruzione** *(`E_m = mu`, `nu_v = nu_F0` sul bordo)* e non conta.
- **La quota:**
  - un'uscita con un'onda di **materia** *(le miste)*: la pendenza del suo gruppo in `|D|^2` contro quella dell'alone, come scritto nella sez. `6-bis` *(passo `6`)*;
  - un'uscita del **vuoto da solo** *((L) `n (mu + k Omega)` e (C) `nu_F0 + k Omega`)*: **l'alone e' materia** *(`1 - f_3w0`, `misure.alone`)* e `D` e' materia. ### **La quota di un'uscita del vuoto da solo non si misura dalle serie che ho.** Lo scrivo accanto all'ampiezza del picco, **senza un numero inventato** *(`A1`)*.
- **Che cosa NON so:** quanti picchi ci sono fino a `1/10`; se la lettura del guardiano regge *(lo dice il conto)*; quale sia il margine `+1.02` del punto `2` *(credo sia il margine di `mu` stesso, a `k = 0`, dalla banda del vuoto piu' vicina: lo stampo e lo confronto)*.

### La progettazione

1. **Questo file, da solo.**
2. **`csv/solitone/respiro.py`:** `elenco(r, frazione, primi)` — i primi `primi` picchi, piu' quelli con ampiezza `>= frazione` volte il primo, senza doppioni entro `1` canale. **`test_respiro.py`, (R4):** tre seni di ampiezza `1`, `0.15`, `0.05` *(con la tendenza)*: l'elenco a `1/10` con `primi = 1` ritrova i primi due e non il terzo, entro `1e-6` sulla frequenza, senza doppioni. **(R4-F, DEVE FALLIRE):** lo stesso elenco a `1/30` NON contiene il terzo.
3. **`carta_respiro.py`:**
   - il conto finale separa DEVE e PUO' FALLIRE;
   - il DEVE del picco netto resta, scritto com'e', e fallisce; ### **dopo il FERMO, la decisione di Luca (a):** le tabelle per ogni picco delle due finestre *(`quanti = None`, `elenco` a `1/10` coi primi `5`)*;
   - per ogni picco: (L) `n (mu + k Omega_j)`, (C) `nu_F0 + k Omega_j`, le miste coi `k != 0`; una volta le miste a `k = 0`;
   - **la lettura del guardiano**, in righe a parte: `mu - Omega_j` mod `P` per i picchi veloci di (W1), la banda e il margine; per (W2), il margine di `mu` a `k = 0` e lo spostamento `3 Omega_j` di ogni picco;
   - **l'elenco delle uscite aperte**, con la finestra, il periodo e l'ampiezza del picco che la apre, il margine, e la quota.
   - Lo stesso referto `doc/referti_l2/solitone_vestito_carta_respiro.txt` *(il vecchio resta nella storia, a `04b02794`)*.
4. **Il cassetto:** `D6` in un commit a se'.
5. **Il referto, la relazione, l'esito qui.**
6. **L'accensione nel repo:** `csv/solitone/accensione.py`, `test_accensione.py` *(A1, A2 secondo la (i), A0 che DEVE FALLIRE; nella cassetta)*, `corsa_accensione.py` *(il runner delle corse, TA1000 e TA2000)*; `D6` a se'; poi le corse, **un processo alla volta**, a pezzi; il referto `doc/referti_l2/accensione_lenta.txt`.

### Che cosa mi farebbe FERMARE

- (W1) o (W2) non coincidono coi controlli di prima *(al bit, gli `sha`)*;
- **i primi `5` picchi di una finestra NON sono quelli di `04b02794`** *(il diff delle righe)*;
- (R4) fallisce o (R4-F) passa;
- per l'accensione: A1 o A2 falliscono, o A0 passa *(come gia' scritto nella sez. `6-bis`)*.

### Le letture *(fissate qui, prima dei numeri)*

- **(p1)** la lettura del guardiano regge: `mu - Omega_j` dentro la banda del vuoto per i picchi veloci di (W1). **Un'uscita del vuoto da solo, aperta dal respiro veloce;** la sua quota non e' misurabile da `D`, e lo dico.
- **(p2)** la lettura non regge *(fuori banda, o dentro per meno del canale in `Omega`)*: lo dico, coi numeri.
- **(p3)** un'uscita mista aperta **a `k = 0`**: indipendente dal respiro, un'uscita lineare dello stato stesso, che la carta di `4d1c2b65` non guardava.
- **(p4)** in (W2) un `k = +-3` dentro una banda: il respiro lento sposta `mu` oltre il margine. Se non succede: lo dico.
- **la quota**, per ogni uscita mista aperta: compatibile / fra le due / incompatibile, come nella sez. `6-bis`.

### 8-bis. L'AGGIUNTA DI LUCA *(09:20)*: DI CHE MODO E' OGNI PICCO

**L'aggiunta** *(arrivata mentre scrivevo la sez. `8`, prima del codice: entra in questa carta perche' usa le stesse finestre)*:
- con le stesse finestre (W1) e (W2), **lo spettro separato** del cuore liscio, di `w`, del baricentro *(`x` e `y`)*, della **deformazione** *(l'anisotropia del secondo momento: ovale e triangolare, le armoniche `2` e `3` dell'angolo)* e di **`Lambda` medio sotto il solitone**;
- **per ogni picco della tabella:** in quale osservabile e' piu' forte *(il respiro, la deformazione, lo spostamento, lo scambio col vuoto, o nessuna: un battimento interno)*.

### ⭐ **L'IPOTESI DI LUCA, scritta prima dei numeri**

> **Ogni frequenza e' un modo diverso in cui il solitone tiene la sua energia.** Dichiarato: **l'energia totale e' una sola** *(`H` si conserva)*.

**Che cosa questa carta puo' dire dell'ipotesi, e che cosa no:** dice **in quale osservabile** sta ogni frequenza. Non misura l'energia di ciascun modo, e non misura `H` *(non lo calcolo qui: lo dichiaro)*.

### Le premesse dal codice

- **`misure.campione`** da' gia' il baricentro `(x, y)`, `w`, il cuore liscio. **`_energia_del_legame.densita(inc, st)`** da' `rho` e **`lam = |phi|^2` per nodo**: e' lo stesso `Lambda` che entra nella materia.
- **Le definizioni** *(le scrivo qui; sono scelte di misura, non leggi)*:
  - **`Lambda` medio sotto il solitone:** `sum(rho lam)/sum(rho)` *(pesato con la materia)*;
  - **la deformazione:** con `dx + i dy` dal baricentro e il peso `rho g` *(`g` la rampa del cuore liscio, la stessa di `f_liscia`: il cuore, non l'alone)*, `Q2 = sum(rho g (dx + i dy)^2)/sum(rho g r^2)` *(l'ovale)* e `Q3 = sum(rho g (dx + i dy)^3)/sum(rho g r^3)` *(il triangolo)*. **Lo spettro si fa sulla parte reale e sull'immaginaria**: un ovale che RUOTA ha `|Q2|` costante, ma `Re` e `Im` oscillano.
  - ⚠ **Il peso `g` invece di `rho` intero:** l'alone a `r` grande dominerebbe `r^3`. **Una scelta, dichiarata.**
- **«Piu' forte» fra osservabili con unita' diverse** non si confronta con le ampiezze. **Si confronta la SIGNIFICATIVITA'**: l'ampiezza rifinita alla frequenza del picco *(minimi quadrati, `a cos + b sin` piu' la tendenza)* divisa per la **mediana** dello spettro d'ampiezza di quell'osservabile *(Hann, i canali con almeno `PERIODI_MIN` periodi)*. E' adimensionale.
  - **La classe del picco** e' quella dell'osservabile con la significativita' piu' alta: **respiro** *(`f_liscia`, `w`)*, **spostamento** *(`x`, `y`)*, **deformazione** *(`Re/Im Q2`, `Re/Im Q3`)*, **scambio col vuoto** *(`Lambda` medio)*;
  - **«nessuna (un battimento interno)»** se in nessun osservabile la significativita' arriva a **`3`** *(il `3` di `doc/PATTERN_DI_PROVA.md`, `P1-sexies`; ⚠ qui la mediana non e' una sigma: **lo dichiaro come criterio di lettura, non come test statistico**)*.
  - Accanto, **l'ampiezza relativa** di ogni osservabile *(divisa per la sua media; per `x`, `y` divisa per `w` medio; `Q2`, `Q3` gia' adimensionali)*, per chi la vuole leggere.
- **Che cosa NON so:** se il baricentro si muove davvero *(un solitone fermo darebbe rumore)*; se `Q2`, `Q3` sono sopra il rumore della griglia a triangoli *(la griglia stessa ha una simmetria `6`: un `Q3` statico non e' una deformazione)*. **Per questo si fa lo spettro tolta la tendenza, non il valore.**

### La progettazione *(si aggiunge ai passi della sez. `8`)*

- **`respiro.py`:** `serie_modi(z, t0, t1, w_in, h)` *(il tick intero; a ogni tick `misure.campione` piu' `Lambda` medio, `Q2`, `Q3`)*; `presenza(y, passo, f)` *(la significativita' a `f`)*. ### **`f_liscia` resta quella di `misure.campione`: il controllo al bit di (W1) resta.**
- **`test_respiro.py`, (R5):** un seno noto con rumore gaussiano *(seme fisso)*: la significativita' alla sua frequenza supera `3`; **(R5-F, DEVE FALLIRE):** sul solo rumore la significativita' alla stessa frequenza supera `3`.
- **`carta_respiro.py`:** (W1) e (W2) con `serie_modi`; i primi `5` picchi di ogni osservabile; **per ogni picco della tabella**, la significativita' e l'ampiezza relativa in ogni osservabile, e la classe.

### Che cosa mi farebbe FERMARE *(in piu')*

- (R5) fallisce, o (R5-F) passa.

### Le letture *(in piu', prima dei numeri)*

- **(m1)** i picchi lenti di (W1) e (W2) stanno nel **respiro** e la coppia veloce in un **altro** osservabile: le frequenze sono modi diversi, come dice l'ipotesi.
- **(m2)** tutti i picchi stanno nello **stesso** osservabile: per questa carta, un modo solo con piu' frequenze.
- **(m3)** la coppia veloce `~0.99` sta nello **scambio col vuoto** *(`Lambda`)*: coerente con la lettura del guardiano *(`mu - Omega` nella banda del vuoto)*.
- **(m4)** un picco **«nessuna»**: un battimento interno, che nessuno di questi osservabili vede.

### 8-ter. Le annotazioni col codice *(scritte col commit del codice, prima della corsa vera)*

- ### ⚠ **LA PREMESSA SULLA SIGNIFICATIVITA' ERA SBAGLIATA** *(la sez. `8-bis` non si riscrive: si annota)*. **La prova a secco** *(finestre di `400` e `300` tick, nello scratchpad, dichiarata)* **da' significativita' fra `~10` e `~3e5`.** Su una serie liscia e deterministica la mediana dello spettro e' il fondo delle code della finestra di Hann, non un rumore: la significativita' dice **quanto e' pulito l'osservabile**, non quanto e' forte il picco.
  - **Quindi la classe si legge dalla QUOTA:** `a^2/2` sulla varianza dell'osservabile tolta la tendenza, cioe' **la parte della fluttuazione di quell'osservabile che sta a quella frequenza**. E' adimensionale e si confronta fra osservabili.
  - **La significativita' resta, con la soglia `3`, solo per dire SE il picco c'e'** in quell'osservabile. La classe e' la quota piu' alta fra gli osservabili dove c'e'; **«nessuna»** se non c'e' in nessuno.
  - **Il test:** `R5-Q` *(un seno puro ha quota `1` entro `1e-2`; un seno nel rumore ha la quota attesa `a^2/2/(sigma^2 + a^2/2)` entro un fattore `2`)*.
- **`R4` con la tolleranza di `1` canale, non `1e-6`:** con tre seni insieme la rifinitura di uno alla volta sente gli altri *(il terzo letto a `19.5032` per `19.5`)*. **Il canale e' lo stesso criterio di identita' che usa `elenco`.**
- **Le uscite del vuoto da solo `n mu` a `k = 0`** si stampano una volta, nella sezione delle miste a `k = 0`, e non si ripetono per ogni picco.

### 8-quater. L'ESITO *(il referto `doc/referti_l2/solitone_vestito_carta_respiro.txt`, a `e8ccbac1`; la relazione per i numeri)*

- **I controlli passano** *(W1 al bit, W2 gli `sha`, `R1`-`R5-Q`, `V0`-`V4`)*; **i primi `5` picchi identici a `04b02794`**; il DEVE del picco netto fallisce come scritto; il conto finale corretto *(`1` DEVE, `1` PUO' FALLIRE)*.
- **(p1) REGGE:** `mu - Omega` della coppia veloce dentro la banda del vuoto *(margini `-0.62`, `-0.67`)*.
- **(p3) SI':** tre miste aperte a `k = 0` *(`(L) B n 1`, `(C+) A n 1`, `(C+) B n 2`)*.
- **(p4) SI', dal lato `-`:** `mu - 3 Omega` dentro per `7` picchi su `14` di (W2).
- **La quota:** nessuna uscita COMPATIBILE da sola; `P0`, `Ppi`, `A` «fra le due»; la loro somma `~0.96` volte l'alone *(una lettura)*.
- **I modi:** (m1) in parte; (m3) no; (m4) no. **La coppia veloce e' uno spostamento** *(e `w`)*, **i lenti sono confusi dalla deriva** *(i periodi tondi, `50.0000`)*.
- **Poi:** la voce `33` (d) della MAPPA *(in coda)*, e l'accensione lenta nel repo e le corse.

## 9. L'ESITO DELL'ACCENSIONE LENTA *(il referto `doc/referti_l2/accensione_lenta.txt`, a `5c13ac57`; la relazione per i numeri)*

- **I criteri `A3`, `A4`, `A6`** e la fine della corsa: **passano** per `TA1000` e `TA2000` *(ESITO `8/8`)*. `A1`, `A2` *(la (i))*, `A0` nella cassetta: `56/56`.
- **(a2) per l'alone** *(cresce come nel vivo dopo la rampa, `+2.54e-3` e `+2.52e-3` per `1000`)*; **(a1) no.**
- **(a3) solo in apparenza, per la vita a meta' del cuore** *(`~29371` contro `~14972`)*.
  - ### **Annoto una premessa sbagliata della sez. `1` e della progettazione** *(non riscrivo)*: la vita «a meta' del valore a `T_acc`» prende **un valore istantaneo** di un cuore che **oscilla lento**. `TA1000` arriva a `T_acc` in un minimo *(`0.39`)*, `TA2000` in un massimo *(`0.53`)*.
  - **La differenza viene dalla fase, non dalla rampa.**
- **Aperta, a Luca:** la vita dalla media del cuore a blocchi, o dall'alone? Criterio di chiusura: la sua scelta, e la misura dai `jsonl` gia' committati.
- **La MAPPA:** voci `1` e `27`, una riga ciascuna.

## 10. LA DECISIONE DI LUCA SULLA VITA *(2026-11-02, dopo `bfee5330`)*

### Le decisioni *(di Luca, nella sostanza)*

1. **La vita dal cuore a blocchi:** il cuore liscio mediato su blocchi di `1000`; la meta' rispetto alla media del **primo blocco dopo `T_acc`** *(per il vivo, il primo blocco dopo `0`)*. Misurata se la si raggiunge, altrimenti estrapolata dalla pendenza delle medie a blocchi, dichiarata. Una riga nella MAPPA accanto alla decisione `9`.
2. **La corsa lunga:** `TA1000` continuata dal suo ultimo pezzo fino a `16000`, stesse misure, un solo processo. Se la meta' a blocchi arriva prima, si scrive il tempo e si prosegue fino a `16000`.
3. **L'alone accanto:** il tempo a cui l'alone arriverebbe al `10%` della materia con la pendenza misurata *(estrapolato, dichiarato)*, per `TA1000`, `TA2000` e il vivo. Il referto dice che sono **due processi** *(l'allargamento dentro `B` e l'emissione fuori)* e da' i due tempi.
4. **La barra d'errore:** la dispersione delle pendenze dell'alone fra `TA1000`, `TA2000` e il vivo **sulla stessa finestra**, dichiarata come stima.
5. **(a2) nella MAPPA**, voci `1` e `27`.

### Le premesse dal codice *(cosa credo prima di guardare, e cosa NON so)*

- **L'alone** e' `1 - f_3w0` *(`_vuoto_vivo_B.misura`)*: **e' gia' una frazione della materia.** Il `10%` e' `alone = 0.1`.
- ### ⚠ **La corsa si FERMA da sola** *(`corsa_accensione.corsa`)*: al primo campione col cuore istantaneo sotto `META` del cuore **alla partenza** *(`0.59164`, quindi `0.296`)*, scrive `t_dis` e interrompe; e `--corsa` dice «finita» quando un pezzo ha `t_dis`. **Con la corsa lunga questo criterio puo' scattare prima di `16000`** *(il cuore istantaneo e' sceso a `0.39` a `T_acc`)*, **contro il punto `2`.** Era nato per `A6` *(«non si scioglie durante la rampa»)*. **La modifica, che dichiaro:** la corsa si interrompe **solo nella rampa**; dopo, registra il PRIMO tempo sotto la soglia e prosegue. **Sui pezzi gia' fatti non cambia niente** *(`t_dis` e' `None` in tutti e `9`)*.
- **`_respiro_congelato.blocchi`** stampa i blocchi fino al suo `TAU_FINE`, e l'ultimo blocco prende **tutto il resto**: per `TA1000` a `16000` la tabella sarebbe sbagliata. **Scrivo una tabella a blocchi nella corsa**, con lo stesso formato e la fine come argomento.
- **I blocchi completi:** un blocco `[a, a + 1000)` conta se c'e' un campione entro un passo di campionamento dalla sua fine *(il passo misurato dai campioni, `1.5`)*. **Non e' un numero scelto:** e' il passo. Cosi' l'ultimo blocco di `TA1000` a `6000` *(un campione, le pendenze `nan`)* non entra nella vita.
- **Il tempo «misurato» della meta' a blocchi:** **il centro del primo blocco** con la media sotto meta'. **E' una scelta di lettura, la dichiaro:** la risoluzione e' il blocco *(`1000`)*.
- **L'estrapolazione:** la retta delle medie a blocchi contro i centri, **su tutti i blocchi completi dopo `T_acc`**, e il tempo a cui la retta arriva a meta'. Solo se la pendenza e' negativa, e con almeno `3` blocchi.
- **La pendenza dell'alone per il punto `3`:** la retta su **tutto il tratto dopo `T_acc`** di ciascuna corsa *(il vivo: da `0` alla fine, `9999`)*; il tempo e' quello a cui **la retta** arriva a `0.1`.
- **La finestra comune del punto `4`:** **`2000 .. 7000`**, l'unica che sta **dopo le due rampe** e dentro tutte e tre le corse. **Il limite, dichiarato:** la barra e' la dispersione delle tre pendenze stesse, quindi **dire che le tre stanno nella barra e' quasi vero per costruzione**; dice quanto e' larga la dispersione, non e' un errore indipendente. **Tre numeri danno una stima grezza** *(la deviazione standard con `n - 1`)*.
- **Il confronto di prima** *(`TA1000` `1000 .. 6000`, `TA2000` `2000 .. 7000`)* resta nel referto **sulle stesse finestre di `bfee5330`**, cosi' i numeri gia' committati si rifanno.
- **Cosa NON so:** se il cuore a blocchi scende sotto meta' prima di `16000` *(a `6000` la media a blocchi e' `~0.50` contro `0.44` del primo blocco dopo `T_acc`: **sale, non scende**)*; se la corsa lunga regge.

### La progettazione

1. Questo paragrafo, **da solo**.
2. **`accensione.py`:** `medie_a_blocchi`, `vita_a_blocchi`, `tempo_alone`. **`test_accensione.py`:**
   - `A7` *(un cuore lineare: la vita estrapolata esatta)*;
   - `A7-M` *(un cuore che scende sotto meta' in un blocco: misurata al suo centro)*;
   - `A7-F` *(DEVE FALLIRE: un cuore che sale da' una vita)*;
   - `A8` *(un alone lineare: il tempo al `10%` esatto)*;
   - `A8-F` *(DEVE FALLIRE: un alone che cala da' un tempo)*.

   **`corsa_accensione.py`:**
   - `TA1000` fino a `16000`;
   - l'arresto solo nella rampa;
   - la tabella a blocchi;
   - nel referto: la vita a blocchi per le tre corse, l'alone al `10%`, la barra sulla finestra comune, i due processi.

   L'inventario. **Commit.** Poi `D6`, commit a se'.
3. **Le corse:** la cassetta, poi `--corsa TA1000` un pezzo alla volta fino a «finita» *(`~7` pezzi, `~70` minuti)*.
4. **Il referto, la relazione, la MAPPA** *(voci `1`, `27`, la riga accanto alla decisione `9`)*, **l'esito qui.**

### Che cosa mi farebbe FERMARE

- un test nuovo che non passa, o un `DEVE FALLIRE` che passa;
- la ripresa di `TA1000` non al bit *(l'assert della corsa)*;
- `A3` o `A4` che falliscono sulla corsa lunga;
- i numeri del confronto di `bfee5330` non rifatti.

### Le letture *(fissate qui, prima dei numeri)*

- **(v1)** il cuore a blocchi non scende sotto meta' prima di `16000`, e la pendenza delle medie e' **piccola o positiva**: **la vita del cuore e' molto piu' lunga della corsa**, o non c'e'.
- **(v2)** scende sotto meta' prima di `16000`: si scrive il tempo.
- **(v3)** l'alone al `10%` arriva in un tempo dell'ordine di `~4 x 10^4` *(la pendenza `~2.5e-3` per `1000`)*: **l'emissione e' il processo piu' rapido**.
- **(v4)** le tre pendenze dell'alone sulla finestra comune stanno entro `~10%` l'una dall'altra: **(a2) regge con la barra**.

### 10-bis. L'ESITO *(il referto a `00822ce0`; la relazione per i numeri)*

- **I DEVE della corsa lunga passano;** la cassetta `62/62`.
- ### ⛔ **UNA PREMESSA CHE MANCAVA** *(annoto, non riscrivo)*: non avevo scritto che **le misure centrano sul baricentro EUCLIDEO e il dominio e' un toro** *(`x` `±60`, `y` `±34.64`)*. Il solitone **deriva lungo `-x` e accelera dopo `~9000`**, e fra `~13000` e `~14000` **attraversa il bordo**: la «vita misurata a `13500`» e l'«alone misurato a `13005`» del referto **sono il bordo, non uno scioglimento** *(dopo, il cuore torna a `0.30`-`0.34`)*. La diagnostica: `doc/referti_l2/accensione_lenta/diag_toro.txt`.
- **(v1)/(v2) per `TA1000`: NON DECIDIBILE.** Fino a `12000` le medie non arrivano a meta' *(minimo `0.38425` contro `0.22120`)*; oltre, le misure non valgono.
- **(v3) regge** per il vivo e `TA2000` *(`~42416`, `~39829`)*. **(v4) regge** *(la dispersione `2.4%` sulla finestra comune)*. **(a2) nella MAPPA.**
- **FERMO:** le domande a Luca nella relazione *(il baricentro periodico e la corsa da rifare, o un criterio di validita'; il moto del solitone)*.

## 11. LA DERIVA DEL SOLITONE E LE MISURE SUL TORO *(Luca, 2026-11-02, dopo `455b9a95`)*

### Le decisioni *(di Luca, nella sostanza)*

1. **Il centro periodico:** la media circolare *(l'argomento di `sum rho e^{i 2 pi x / Lx}`, e cosi' per `y`, sui vettori del reticolo)*, e tutte le misure centrate li' *(cuore liscio, `w`, alone, i blocchi)*.
2. **Il criterio di validita'** *(dalla geometria, non tarato)*: una misura vale finche' `3 w <` meta' del lato corto del toro. Il primo blocco che non lo rispetta e' marcato, e la vita si dice solo sui blocchi validi.
3. **La ripresa:** `TA1000` dall'ultimo stato salvato prima della deriva *(il tick piu' vicino a `9000`)* fino a `16000`. I blocchi fino a `9000` si ricalcolano se gli stati ci sono, altrimenti si dichiara.
4. **La deriva, da descrivere e non da interpretare:**
   - la traiettoria e la velocita' per blocco;
   - la direzione, rispetto agli assi del reticolo e al lato corto;
   - la velocita' contro `w`;
   - l'alone e il libro dei conti avanti e dietro rispetto al moto.
5. **La MAPPA, voci `1` e `27`:** l'emissione `2.51e-3` con la barra `2.4%`, la deriva, il criterio.

**I criteri:**
- **DEVE:** `M` e `V` entro `1e-10`; il libro col `par`.
- **DEVE:** su un solitone traslato di mezzo lato, il centro periodico da' i numeri del solitone al centro, entro l'arrotondamento.
- **DEVE:** prima di `9000` il centro periodico e quello euclideo coincidono entro `0.1`.

**Le letture:** (t1)-(t4), nel mandato.

### Le premesse dal codice *(cosa credo prima di guardare, e cosa NON so)*

- ### ⛔ **UNA PREMESSA DEL MANDATO CHE CADE: in `db/` NON c'e' uno stato a `9000`.** `corsa_accensione.corsa` salva **solo l'ultimo stato**: `db/accensione_lenta/TA1000.npz` *(sovrascritto a ogni pezzo)*, oggi a `16000`, e `TA1000_acc.npz`, **solo `psi`** a `T_acc`. **Nessuno stato prima della deriva.**
  - **Cio' che faccio, e lo dichiaro:** rigiro la corsa **da `0`**, sotto il nome nuovo **`TP1000`** *(stesso `T_acc`, stessa rampa, stesso tick)*, con le misure nuove accanto alle vecchie.
  - **Il controllo:** **ogni pezzo di `TP1000` deve dare lo stesso `sha_fine` del pezzo di `TA1000` con lo stesso `t0`, AL BIT** *(un DEVE in piu')*. Cosi' **lo stato a `9000` e' quello della corsa committata**, e i blocchi prima di `9000` **si ricalcolano davvero**.
  - **Il costo:** `~1 h 45'` *(`6213 s` per gli `11` pezzi)*. Prima dicevo `~3 ore`: era una stima a occhio, sbagliata.
  - **Perche' non chiedo prima:** il risultato e' **lo stesso** che darebbe la ripresa a `9000` se lo stato ci fosse, e il controllo al bit lo verifica. Se Luca preferisce un'altra strada, la corsa si ferma col semaforo.
- ### ⛔ **UN MIO ERRORE IN `455b9a95`, ENTRATO NEL MANDATO: il toro NON ha un «lato corto».** Dal codice *(`_energia_del_legame.stato`)*:
  - `pos = d1 A1 + d2 A2`, con `A1 = (1, 0)` e `A2 = (-1/2, sqrt3/2)`, e `d1, d2` interi in `[-40, 40]` *(`L 81`)*;
  - **il toro e' un ROMBO a `60` gradi**, coi periodi `L A1`, `L A2`, `L (A1 + A2)`, **tutti lunghi `81`**;
  - **`34.64` e' solo l'estensione in `y` della rappresentazione dei nodi** *(`40 sqrt3/2`)*, e io l'ho chiamata «il mezzo lato corto». **Era sbagliato.**
  - **La distanza dalla propria immagine e' `81` in ogni direzione del reticolo:** la meta' e' **`40.5`**, ed e' il raggio del cerchio inscritto nella cella di Wigner-Seitz *(un esagono)*.
  - **Cio' che faccio:** il criterio usa **la meta' del periodo piu' corto**, `40.5`, **calcolata dai vettori del toro** *(non scritta a mano)*: e' cio' che dicono le parole di Luca *(«meta' del lato»: i lati sono `81`)*. **Il referto marca anche il primo blocco con `3 w >= 34.64`**, cosi' Luca sceglie **senza una corsa nuova**. **Decide Luca.**
- **La media circolare sui vettori del reticolo:** per ogni nodo gli indici `m1, m2` *(periodo `L`)*:
  - `c1 = L/(2 pi) arg sum rho e^{i 2 pi m1/L}`, e cosi' `c2`;
  - il centro e' `c1 A1 + c2 A2`.
- **Le distanze dal centro, con l'immagine piu' vicina:**
  - lo scarto per indice si riporta in `[-L/2, L/2)`;
  - **poi, fra le `9` immagini `(k1, k2)` in `{-1, 0, 1}^2`, si prende la piu' corta**: col rombo a `60` gradi, riportare ogni indice da solo **non basta**.
- **Le misure periodiche: le stesse espressioni** di `_salti_nel_cuore.campione` e `_congelato_lungo.punto`:
  - il cuore liscio *(la rampa `g` con `w_in`, `h`)*;
  - `f_win`;
  - `w`;
  - l'alone `1 - f_3w0`.

  Cambia **solo la distanza**.
- ### **Il test del mezzo lato:** una `rho` gaussiana *(la larghezza della partenza)* su un fondo uniforme, sul reticolo vero, spostata di **`40` indici** *(`L` e' dispari: «mezzo lato» e' `40`)*: **lungo `A1`, lungo `A2`, e lungo entrambi**.
  - E' una **permutazione esatta** dei nodi, quindi i numeri devono coincidere **entro l'arrotondamento delle somme**.
  - **Il caso che DEVE FALLIRE:** le misure euclidee sullo stesso solitone spostato.
- **Avanti e dietro rispetto al moto:** la direzione del moto si conosce **solo dopo**. Per ogni campione:
  - registro l'alone in **`8` settori angolari** di `45` gradi attorno al centro periodico;
  - registro il libro dei conti **per settore** *(tutto il settore, il solitone compreso)*.

  **Nel referto:**
  - per ogni blocco, la direzione della velocita' del blocco;
  - «avanti» sono **i `4` settori a meno di `90` gradi da quella direzione**, «dietro» gli altri `4`;
  - la risoluzione e' di `45` gradi, dichiarata.
- ### ⚠ **UN NUMERO DI PROTOCOLLO, DICHIARATO:** il libro per settore **ogni `5 OGNI_D` = `100` tick**.
  - Il libro per settore aggiunge `56` numeri a campione. A ogni campione i `jsonl` passerebbero da `~9` a `~30` MB per la corsa.
  - **Non e' un parametro del modello:** e' la cadenza di una misura.
  - L'alone per settore resta **a ogni campione**.
- **La velocita':** la traiettoria del centro periodico **srotolata** *(la somma dei passi con l'immagine piu' vicina fra campioni consecutivi)*. Per blocco: la retta di `x` e di `y` contro il tempo, `v = (vx, vy)`, il modulo.
  - **L'angolo rispetto agli assi del reticolo** *(`A1`, `A2`, `A1 + A2` sono a `0`, `120`, `60` gradi)*: si riporta l'angolo fra `-30` e `30` gradi rispetto alla direzione del reticolo piu' vicina.
  - **La velocita' contro `w`:** la tabella per blocco.
- **Cosa NON so:**
  - se la corsa da `0` ridara' gli `sha_fine` al bit *(il tick e' deterministico, ma non l'ho mai verificato su `11` pezzi)*;
  - se il centro euclideo e quello periodico coincidono entro `0.1` prima di `9000`. **Una stima:** l'alone uniforme, il `2%`, tira il baricentro euclideo verso l'origine di `~2% x 3 = 0.06`.

### La progettazione

1. Questo paragrafo, **da solo**.
2. **`csv/solitone/toro.py`** *(nuovo)*: `centro(rho, m1, m2, L)`, `scarti(m1, m2, c1, c2, L)` *(l'immagine piu' vicina)*, `misure(rho, m1, m2, L, w_in, w0, h)`, `settori(...)`, `meta_periodo(L)`.
   - **`csv/solitone/test_toro.py`:**
     - `T1` *(il mezzo lato lungo `A1`, `A2`, entrambi)*;
     - `T1-F` *(DEVE FALLIRE: l'euclideo sullo spostato)*;
     - `T2` *(al centro il periodico e l'euclideo coincidono; `T2` e' un controllo, non al bit: le distanze lontane cambiano)*;
     - `T3` *(`meta_periodo(81) = 40.5`)*.
   - **`corsa_accensione.py`:**
     - la corsa `TP1000`;
     - le misure periodiche in ogni campione;
     - il libro per settore ogni `100` tick;
     - nel referto la sezione `TP1000`, coi DEVE:
       - `A3` e `A4`;
       - **gli `sha_fine` di `TA1000` al bit**;
       - **i due centri entro `0.1` prima di `9000`**;
     - la tabella a blocchi periodica col blocco non valido marcato, la vita sui blocchi validi, la deriva.
   - **La cassetta:** `test_toro`. **Commit.** Poi `D6`.
3. **La corsa:** la cassetta, poi `TP1000` da `0` a `16000`, un pezzo alla volta.
4. **Il referto, la relazione, la MAPPA, l'esito.**

### Che cosa mi farebbe FERMARE

- `T1` che non passa, o `T1-F` che passa;
- un `sha_fine` di `TP1000` diverso da `TA1000` *(il tick non e' deterministico: tutto cambia)*;
- `A3` o `A4`;
- i due centri non entro `0.1` prima di `9000` *(DEVE)*.

### Le letture *(quelle di Luca, (t1)-(t4); in piu', le mie, prima dei numeri)*

- **(p1)** col centro periodico il blocco `13000 .. 14000` non crolla *(il cuore resta `~0.3`-`0.4`)*.
- **(p2)** `3 w` arriva a `40.5` solo se `w > 13.5`. Nella corsa euclidea `w` era `~10.5`-`11` a `10000`-`12000`, e quella misura e' gia' gonfiata dall'alone lontano: **potrebbe non arrivarci mai prima di `16000`.**

### TODO

- *(In attesa della decisione di Luca)* la stessa prova su un toro piu' grande *(`L 120`)*: separa la deriva e la vita dal limite del toro.

### 11-bis. LA CONFERMA DI LUCA *(dopo `8e425771`, arrivata mentre scrivevo il codice; prima della corsa)*

1. **Il criterio e' `40.5`**, la meta' del periodo *(decisione di Luca)*. Il `34.64` era **l'errore di lettura `n.92`** *(il mio)*: nel referto **solo come confronto**.
2. **La corsa da `0` come `TP1000`**, col controllo al bit su `TA1000`: **va bene.**
3. **Le parole:** il toro **non ha un bordo**. Cio' che rompeva le misure e' **il TAGLIO DELLE COORDINATE** *(gli indici da `-40` a `+40`)*; il crollo a `13500` e' **l'effetto della misura euclidea sul taglio**. Nel referto e nella MAPPA si scrive cosi'. ### **Correggo le mie parole in `455b9a95` e nella sez. `11`** *(«il bordo del toro»)*: **le annoto qui, non le riscrivo.**
4. **Il rombo e' uguale nelle tre direzioni:** nessuna direzione del moto viene dalla forma del toro. **Il referto confronta la direzione con gli assi del reticolo e con la partenza.**
   - **Come leggo «la partenza», e lo dichiaro:** la direzione del centro periodico al primo campione rispetto al nodo d'origine *(la partenza non e' centrata su un nodo: `x ~ 0.19`)*.
   - **Il confronto:** con la direzione dello spostamento totale srotolato.

**Nel codice** *(un commit a se', prima di `D6` e della corsa)*: le righe del referto di `sul_toro`. **Le misure non cambiano.**

## 12. LE MAPPE PER L'ANIMAZIONE *(Luca, 2026-11-02 15:49; un'aggiunta, non cambia la coda)*

### La decisione *(di Luca, nella sostanza)*

- **Ogni `100` tick** *(`15` unita' di tempo)*: `rho` *(`sum_h |psi_h|^2`)* e `Lambda` per nodo in `float32`, piu' `t`, il centro periodico e `lam` *(la rampa)*.
- **Un `.npz` compresso per pezzo** in `E:\soliton_simulator\mappe\<corsa>\<corsa>_<t0>.npz`, con le coordinate dei nodi *(`d1`, `d2`)* e i vettori del toro, una volta per file. **Nel repo solo l'indice:** `doc/referti_l2/mappe_indice.txt`.
- **Se `TP1000` e' gia' partita, NON si interrompe:** le mappe si fanno dopo, con una ripetizione di `TP1000` identica *(controllo al bit sugli `sha_fine`)*, o nella prossima corsa in coda; **si dichiara quale.**
- **I DEVE:**
  - col salvataggio acceso gli `sha_fine` sono identici;
  - `E:` esiste, e' scrivibile, con lo spazio libero almeno `10` volte la stima, altrimenti FERMO;
  - rileggendo un'istantanea, `sum rho = M` e `sum Lambda = V` entro `1e-6` relativo.
- **TODO dopo:** `csv/solitone/anima.py`, i fotogrammi del toro.

### Le premesse dal codice *(cosa credo prima di guardare, e cosa NON so)*

- ### **`TP1000` E' GIA' PARTITA** *(il driver dopo `18c91ad8`)*: **non la interrompo.**
- ### **LA MIA SCELTA, DICHIARATA: la ripetizione.** Le mappe vengono da **`TM1000`**, una ripetizione di `TP1000`, **dopo** che `TP1000` si chiude col suo referto.
  - **Il perche':** la prossima corsa in coda *(il toro `L 120`)* aspetta una decisione di Luca, e non so quando partira'.
  - **Il controllo:** ogni pezzo di `TM1000` deve dare lo `sha_fine` del pezzo di `TP1000` con lo stesso `t0`, **al bit**. **E' esattamente il DEVE del salvataggio:** gli stessi pezzi, con le mappe e senza.
- ### ⚠ **«Lo stesso codice» non puo' essere letterale:** per salvare le mappe, `corsa_accensione.py` deve cambiare. **Cambia a corsa chiusa** *(`CLAUDE.md`, par. `5`: durante un run nessun file del percorso in uso si modifica)*. **Il tick no:** il controllo al bit lo verifica.
- **I campioni di `TM1000` sarebbero identici a quelli di `TP1000`** *(stesse misure, stati al bit)*.
  - **La mia scelta, dichiarata:** i `jsonl` di `TM1000` vanno su `E:`, accanto alle mappe, e non nel repo *(sono `~20` MB di doppioni)*.
  - **Nel repo** restano il confronto degli `sha_fine` e l'indice.
- **`rho` e `Lambda`:** sono `_energia_del_legame.densita` *(`rho = sum_h |psi_h|^2`, `lam = |phi_h|^2`, per nodo)*. Nel libro, `M` e `V` del totale sono `sum rho` e `sum lam` *(`_libro_dei_conti.conti_per_nodo`: `"M": rho`, `"V": lam`)*. **Il confronto del DEVE e' quindi diretto**, e `float32` lo rispetta *(`~6e-8` relativo per valore; la somma in `float64` alla rilettura)*.
- **La stima:** `6561` nodi `x 2 x 4` byte `= 52 KB` a istantanea. Da `0` a `16000` sono `1067` istantanee *(ogni `100` tick)*, cioe' `~56` MB prima della compressione. **Il DEVE del disco: libero `>= 10 x 56 MB`.** Oggi `E:` ha `214` GB liberi *(`df`)*.
- **Il test della cassetta scrive su `E:`** *(una cartella `_prova`)*: **la cassetta dipende dal disco esterno.** Lo dichiaro: e' cio' che chiede il DEVE del disco.
- **Cosa NON so:** quanto comprime `savez_compressed` su `rho` e `Lambda` in `float32`.

### La progettazione

1. Questo paragrafo, **da solo** *(mentre `TP1000` gira: i suoi `jsonl` nuovi sono non tracciati, e lo dichiaro nel messaggio)*.
2. **Subito** *(non toccano il percorso della corsa)*:
   - **`csv/solitone/mappe.py`:** `controlla_disco`, `istantanea`, `scrivi`, `leggi`, `indice`.
   - **`csv/solitone/test_mappe.py`:**
     - `K1` *(il disco)*;
     - `K1-F` *(DEVE FALLIRE: lo spazio con una stima piu' grande del disco)*;
     - `K2` *(un'istantanea della scena scritta e riletta: `sum rho = M`, `sum Lambda = V` entro `1e-6`)*;
     - `K2-F` *(DEVE FALLIRE: con un nodo alterato)*;
     - `K3` *(lo `sha1` e la dimensione dell'indice sono quelli del file)*.
   - L'inventario. **Commit.**
3. **Dopo il referto di `TP1000`:**
   - in `corsa_accensione.py`, la corsa `TM1000` *(gemella `TP1000`, le mappe ogni `100` tick, i `jsonl` su `E:`)*;
   - la cassetta col `test_mappe`;
   - `D6`;
   - la corsa;
   - l'indice;
   - il referto *(gli `sha_fine` al bit, le riletture)*.

### Che cosa mi farebbe FERMARE

- `E:` assente, non scrivibile, o senza spazio;
- un `sha_fine` di `TM1000` diverso da `TP1000`;
- una rilettura fuori da `1e-6`.

### 11-ter. L'AGGIUNTA DI LUCA *(15:54)*: NEL REFERTO DELLA DERIVA, IL LOGARITMO DELLO SPOSTAMENTO, LA VELOCITA' CONTRO `w`, L'AMPIEZZA DEL CUORE

**La richiesta** *(nella sostanza)*:
- **(i)** il logaritmo dello spostamento del centro periodico contro il tempo, dalla fine della rampa, con **la pendenza a tratti**. Se e' una retta gia' prima di `9000`, e' **un'instabilita' presente fin dall'inizio, nascosta dal tremolio del respiro**.
- **(ii)** la velocita' contro `w` per `TP1000` e, dove i dati bastano, per **il vivo** *(senza rampa)* e **`TA2000`**. Se il moto parte allo stesso `w`, e' **una soglia di larghezza**.
- **(iii)** l'ampiezza dell'oscillazione del cuore **a finestre di `500`**, accanto alla velocita'.

**L'ordine** *(`[[PRECEDENZA-IN-CODA]]`, registrato)*: e' arrivata dopo l'aggiunta delle mappe *(15:49)*, ma **riguarda il referto della deriva, che viene prima nella coda**. La si fa **col referto di `TP1000`**; le mappe vengono dopo, come scritto nella sez. `12`.

### Le premesse dal codice

- ### ⚠ **`corsa_accensione.py` E' NEL PERCORSO DELLA CORSA IN USO** *(`TP1000` gira)*: **non si modifica** *(par. `5`)*. Quindi **uno script a parte**, `csv/solitone/carta_deriva.py`, che legge i pezzi, col suo referto **`doc/referti_l2/deriva_solitone.txt`**. Non tocca la corsa.
- **I dati:**
  - `TP1000`: il centro periodico *(`c1`, `c2`)* in ogni campione, la traiettoria srotolata come in `sul_toro`;
  - **il vivo** *(`_respiro_congelato.serie_viva`, fino a `9999`)* e **`TA2000`** *(fino a `7000`)*: **solo il centro EUCLIDEO**.
  - Il baricentro di queste due resta entro `~3.5` dalla partenza, e su `TP1000` **il DEVE `TP2`** misura la differenza fra i due centri prima di `9000`. **Lo dichiaro:** per queste due corse il centro e' l'euclideo, **valido finche' `TP2` dice che i due coincidono.**
- **Le definizioni** *(le mie, dichiarate prima dei numeri)*:
  - **(i) lo spostamento:** `s(t) = |X(t) - X_rif|`, con `X_rif` **la media di `X` sul primo blocco dopo `T_acc`** *(lo stesso riferimento della vita, la decisione di Luca dopo `bfee5330`)*.
    - **La pendenza a tratti:** per ogni blocco di `BLOCCO` `= 1000`, la retta di `ln s` contro `t` sui campioni del blocco, per `1000`.
    - **E due rette lunghe:** su `T_acc + 1000 .. 9000` e da `9000` al primo blocco non valido.
    - **Un esponenziale da' pendenze uguali a ogni tratto;** un moto uniforme da' pendenze che calano come `1/t`.
    - ⚠ **Nel primo blocco `s` e' piccolo e dominato dal tremolio:** `ln s` e' rumore, e lo stampo comunque.
  - **(ii) la velocita':** per ogni blocco di `1000`, la retta di `x` e di `y` contro `t` *(per `1000`)*, e `w` medio del blocco. **Senza una soglia mia:** la tabella, e la lettura e' di Luca.
  - **(iii) l'ampiezza del cuore** in finestre di `500`:
    - `sqrt(2)` volte la deviazione standard del cuore liscio meno la sua retta nella finestra, cioe' **l'ampiezza di un seno con quella varianza**. E' una scelta, dichiarata;
    - accanto, la velocita' della stessa finestra.
- **Il periodo del tremolio:** la coppia veloce `~0.99` *(la carta del respiro)*. I campioni ogni `1.5` lo **aliasano**: `ln s` campione per campione e' rumoroso. **Le rette per blocco lo mediano.**

### La progettazione *(si aggiunge ai passi della sez. `11`)*

1. **`csv/solitone/carta_deriva.py`** *(nuovo, mentre `TP1000` gira; non nel percorso della corsa)*: le tre tabelle, per `TP1000`, il vivo, `TA2000`. Una prova sui pezzi gia' committati di `TA1000` *(il centro euclideo, fino a `9000`)*.
2. **Dopo `TP1000`:** il referto `deriva_solitone.txt`, insieme a quello della corsa.

### 12-bis. LA DECISIONE DI LUCA SULLA PROPOSTA DI `3e3277a2`: `TM1000` SALVA ANCHE GLI STATI

- **`TM1000` salva lo stato COMPLETO** *(ogni chiave di `z["st"]`: cio' che serve a ripartire al bit, come la ripresa dei pezzi)* **a `t` `2000`, `6000`, `10000`**, in `E:\soliton_simulator\stati\TM1000\`, con la riga nell'indice del repo *(il percorso, la dimensione, lo `sha1`)*.
- **Il controllo** *(un DEVE)*: ripartendo da ciascuno stato per `100` tick si ritrova **al bit** lo stato della corsa.
- **Come, dal codice** *(dichiarato prima)*:
  - durante `TM1000` registro gli `sha` di ogni chiave *(`_vuoto_vivo_B.shas`)* anche al tick `t + 100`;
  - il controllo carica lo stato salvato in una scena nuova, fa `100` tick col tick della corsa *(`accensione.tick`, dopo la rampa e' il tick intero)* e confronta gli `sha`.
  - **I tempi sono in unita' di tempo:** il tick e' `round(t / s)`, con `s = 0.15`. `2000 / 0.15 = 13333.3`: il tick `13333`. **Lo dichiaro: il tick piu' vicino.**
- **La stima:** lo stato intero e' `~2.3` MB *(come `db/accensione_lenta/TA1000.npz`)*, quindi tre stati sono `~7` MB.

### 11-quater. LA CURVATURA NEL REFERTO DELLA DERIVA *(per il mandato «due giri», Luca `17:30`-`17:33`, che vi e' condizionato)*

- **«Due giri» si fa SOLO se il referto di `TP1000` conferma che la traiettoria curva**, con la curvatura blocco per blocco, il raggio e il verso. **Il codice del referto della deriva non la calcola:** la aggiungo a `carta_deriva.py` *(non nel percorso della corsa in uso)*, come **(iv)**.
- **La definizione** *(dichiarata prima dei numeri)*. Per due finestre consecutive *(di `1000` e di `500`)*:
  - `d theta` e' la differenza degli angoli della velocita', riportata in `(-180, 180]`;
  - `ds` e' la distanza fra le posizioni medie;
  - la curvatura e' `kappa = d theta [rad] / ds`, per nodo *(il passo del reticolo e' `1`)*;
  - il raggio e' `1/|kappa|`;
  - il verso e' antiorario se `d theta > 0`.
  
  Accanto: l'angolo girato in tutto, e il raggio contro `|v|`.
- ### **IL CRITERIO DELLA CONDIZIONE** *(fissato QUI, prima dei numeri; i due numeri vengono dalle premesse di Luca)*: **la traiettoria «curva» se, nelle finestre di `500` da `11000`** *(Luca: il tratto dritto comincia a `11250`)* **fino alla fine dei dati validi di `TP1000`**:
  - `d theta` ha **lo stesso segno in ogni coppia consecutiva**;
  - **e l'angolo girato in tutto supera `10` gradi** *(Luca osserva `+10` fra `11250` e `12600`)*.
  
  **Altrimenti si scrive, e «due giri» non si fa.** Se Luca vuole un altro criterio, lo cambia prima del referto.
- **L'ordine nella coda** *(`[[PRECEDENZA-IN-CODA]]`, la decisione di Luca nel mandato)*: `(1)` la deriva; **`(1-bis)` due giri, condizionato**; `(2)` le mappe `TM1000`; `(3)` la direzione; `(4)` `cs` col solitone.
