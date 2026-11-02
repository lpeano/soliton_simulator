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
