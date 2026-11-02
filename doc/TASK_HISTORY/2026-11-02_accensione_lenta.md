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
