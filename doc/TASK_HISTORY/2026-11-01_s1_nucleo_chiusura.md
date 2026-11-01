# 2026-11-01 — `S1` NEL NUCLEO, LA CHIUSURA *(il mandato di Luca dopo `3fe2f12d`; [[STRUMENTO-LEGGE-DALLA-TABELLA]], [[SUITE-NEL-COMMIT]], [[PIANO-2D-3D]])*

> **La decisione di Luca:**
> - `energia_pesata.py` prende `N` da `materia_vuoto` *(la forma della tabella)*, come la legge;
> - `_collauda_materia_vuoto` e `_collauda_deriva` si legano a `S3` esplicita, piu' i collaudi equivalenti per `S1`;
> - `M-B1` ha un riferimento al bit per `S1`, e quello di `S3` resta;
> - il cono di `L2` e gli altri numeri che cambiano: i valori con `S1` diventano il riferimento di `S1`, quelli di `S3` restano;
> - gli storici di `csv/` si rigirano al loro commit.

## 1. LE PREMESSE DAL CODICE

> **Dichiaro l'ordine:** prima di scrivere questo file ho fatto una **ricognizione con `grep`** *(per formule, sugli stessi pattern del passo `2`)*, per sapere che cosa scrivere qui. **La ricerca che fa da criterio e' lo script del passo `2`, dopo questo commit.**

### Dove la formula di `S3` e' scritta a mano *(blob sha1-BYTE di oggi)*
- **`primo_ordine/energia_pesata.py`** *(`7889c512`)*, `termini_di_h`: `N[vivi] = rho*log(rho/(rho+lam))`. **E' la `N` di `Omega`** *(la fase `CAMM-FASE-VUOTO`, che il motore applica con `cs` acceso)* e di `g_dello_stato` *(l'osservabile del modo DINAMICO di `H_w`)*.
- ### ⚠ **`primo_ordine/_misura_mb2.py`** *(`5e749d40`)*, **due volte:** `h_tot` *(riga `136`)* e `pezzi_di_h` *(riga `194`)*. **E' questa che fa fallire i bracci `(a)` e `(b)` di `H_w`:** `_misura_hw.h_w` legge `MB2.pezzi_di_h`, **non** `energia_pesata`. `energia_pesata` entra in `H_w` solo nel modo dinamico.
  - Il commento di `_misura_mb2.h_tot` dice che e' **una seconda fonte voluta**: «non si importa da `materia_vuoto.py`: se le due divergessero, il confronto lo direbbe». **Con due forme la seconda fonte scritta a mano non puo' seguire la tabella.** Il confronto infatti l'ha detto: `H_w` piatto.
- **Quindi la premessa del mandato** *(«`energia_pesata.py` riga `190`»)* **e' vera ma non basta:** se correggo solo `energia_pesata`, i bracci `(a)` e `(b)` restano piatti. **Correggo tutti e due**, come chiede il passo `3` *(«e ogni altro punto trovato al passo `2` che serve la legge del predefinito»)*.

### Gli altri tre collaudi rossi
- **`M-B1`** *(`_collauda_mb1.py`, `b74c228e`)*: il controllo positivo confronta i byte del pezzo `CAMM-MATERIA-VUOTO` di oggi con l'albero di **`8c7b9288`**, che gira `S3`. Con `S1` i byte sono diversi, per costruzione.
- **La misura completa di `L2`** *(`_misura_completa_l2.py`, `134fd231`)*: il rosso **non e' il cono** *(`A1` passa: `0.6532 <= 1`)*. E' **`A2`**, «il rumore fra i due protocolli statici», e il suo criterio e' `<= 1e-10`.
  - Il protocollo `"S3"` *(la forma sostituita da `statica_protocollo`, scritta in `_misura_forme_l2._alpha_beta`)* si confronta col protocollo `"MOTORE"` *(il pezzo del nucleo)*.
  - **Il nome `"S3"` e' scritto a mano in `braccio_rumore`.** Con `S1` predefinita i due protocolli girano **due leggi diverse**: lo scarto `1.09` non e' piu' rumore.
- **`_collauda_materia_vuoto`** *(`711259d7`)* e **`_collauda_deriva`** *(`aacacb75`)*: i bracci scritti per `S3` chiamano `MV.pezzi`, `MV.N`, `MV.beta`, cioe' il predefinito.

### Che cosa ne segue, PRIMA del codice
- **Con `S3` esplicita la correzione e' al bit:** `MV.N_s3` fa **le stesse operazioni** di quelle due righe *(`r*np.log(r/s)`, `s = r + lam`, sui nodi con `rho > 0`, zero altrove)*.
- **`csv/solitone/` non dovrebbe cambiare:** le sue corse tengono `mot.cs` spento *(`mot.lambda_c = None`)*, e a forma spenta `energia_pesata.applica` non fa niente. **Lo dice il collaudo dei `38`, non io.**
- **La seconda fonte di `_misura_mb2` perde l'indipendenza sulla sola `N`:** gli altri termini *(Grover, moneta, archi)* restano scritti li', e il braccio `(0)` di `H_w` li confronta ancora. **L'indipendenza su `N` sta in `_collauda_forme`:** `S1` uguale al bit alle espressioni di `csv/`, e la coerenza `alpha = dN/drho`, `beta = dN/dLambda` a differenze finite.

### Cosa NON so
- **se `H_w` torna a pendenza `~2` con `S1`** *(la domanda del mandato; le letture `h1`/`h2`)*;
- se `A2` di `L2`, con il protocollo statico in `S1`, resta sotto `1e-10` *(con `S3` il rumore restava piccolo; con `S1` non l'ho mai misurato)*;
- se l'albero di `c7ad2238` si materializza in `M-B1` come quello di `8c7b9288`;
- quanti punti trova la ricerca per formule, oltre a quelli della ricognizione.

## 2. LA PROGETTAZIONE

1. **La ricerca per formule** *(passo `2`)*: lo script `csv/_cerca_formule_legge.py`.
   - **Cerca** in `primo_ordine/` e `csv/solitone/` *(esclusi `materia_vuoto.py` e i moduli generati `termini/`)*: `log(rho`, `log(r/`, `atan`, `arctan`, `x^2/(1+x^2)` *(anche come `1 + x*x`)*, piu' `rho + lam` *(per le copie di `beta` di `S3`)*.
   - Separa le occorrenze nel **testo** *(commenti e stringhe, col modulo `tokenize`)* da quelle nel **codice**.
   - **Ogni occorrenza nel codice ha un giudizio scritto nello script**, per file e testo della riga, con una categoria: `legge a mano`, `screening dichiarato`, `oracolo di collaudo`, `modulo di un'altra legge`, `non e' la legge`.
   - Un'occorrenza **senza giudizio fa fallire**. Il criterio: **zero `legge a mano`** dopo la correzione.
   - **Il caso che deve fallire:** sul blob di `energia_pesata.py` a `HEAD` *(prima della correzione)* lo script **deve** trovare la riga `legge a mano`.
2. **La correzione:**
   - `energia_pesata.termini_di_h` e `_misura_mb2.h_tot`/`pezzi_di_h` chiamano `MV.N(rho, lam)`, **per nome di modulo** *(cosi' `scegli` e `forma_esplicita` la cambiano)*;
   - i commenti che dicono «seconda fonte, non si importa» si riscrivono **col perche'**.
3. **I collaudi** *(la decisione)*:
   - **`_collauda_materia_vuoto`:**
     - i bracci di `S3` *(il braccio `(0)` intero, e in `(4)` la chiamata «`alpha` non e' tagliata»)* girano dentro `MV.forma_esplicita("S3")`;
     - **nuovi bracci `S1`**, dentro `forma_esplicita("S1")`: `alpha -> 1` per `x` grande *(`|1 - alpha| <= 1/x^2 + 8 eps`, perche' `1 - alpha = 1/(1+x^2)`)*; `alpha ~ x^2` per `x` piccolo *(`|alpha/x^2 - 1| <= x^2 + 8 eps`, perche' `alpha/x^2 = 1/(1+x^2)`)*; il limite a `Lambda = 0` *(`1`, `-pi/2`, `rho`, esatti)*; `0` dove `rho = 0`; le due derivate a differenze finite *(come per `S3`)*; in `(4)`, `alpha` finita e in `(0, 1]` sui nodi pieni;
     - **i bracci comuni** *(il flusso, le norme, due mezzi, i bordi)* **girano col predefinito:** sono proprieta' di un flusso di fase, non di una forma. **Le righe che esistono restano col loro testo:** con `S3` esplicita devono uscire identiche.
   - **`_collauda_deriva`:**
     - `(1-bis)` dentro `forma_esplicita("S3")`;
     - **il braccio `S1` equivalente:** con `S1`, `beta = x/(1+x^2) - arctan x` **e' la `b` della saturazione** *(stessa funzione)*. Il braccio dice che nel regime `globale` **il termine torna cubico come la saturazione**: `|beta_S1 - b_sat| <= 8 eps x` *(l'errore di arrotondamento della differenza fra termini di ordine `x`)*.
   - **`M-B1`:** il riferimento del controllo positivo si sceglie dalla forma attiva: **`S3` -> `8c7b9288`** *(come oggi)*, **`S1` -> `c7ad2238`** *(il commit in cui `S1` e' entrata nel nucleo)*. Gli altri bracci *(le perturbazioni)* restano su `8c7b9288`: provano il meccanismo, non la forma.
   - ### ⚠ **`A2` di `L2`: LA MIA LETTURA, da confermare.** Il protocollo statico prende la forma da `MV.ATTIVA` invece che dalla stringa `"S3"`. Con `S3` esplicita e' **la corsa di prima, al bit**; col predefinito confronta `S1` sostituita con `S1` del motore, cioe' **il rumore fra due protocolli della STESSA legge**, che e' la domanda del braccio. **Leggerla come «i valori con `S1` diventano il riferimento»** non darebbe niente: con due leggi diverse lo scarto non e' rumore. **Se Luca la legge diversamente, si lega `A2` a `S3` esplicita.**
   - **Il cono e gli altri numeri che cambiano:** nessun codice. **Il riferimento di `S1` e' la corsa `chiusura_S1`** *(il json e le uscite)*, quello di `S3` resta `prima`.
4. **`D6` della cassetta, riscritto:**
   - nessun `.py` di `csv/solitone/` cambiato da **`3fe2f12d`**, l'ultimo commit in cui i `32` test e `D5` hanno dato i numeri al bit col predefinito `S1`; e niente di non committato;
   - **`collauda.py` si esclude, dichiarato:** e' il collaudo, non la libreria, e questo mandato lo cambia;
   - il secondo braccio *(nessuno script fuori importa la libreria)* resta.
5. **Le due corse della suite**, una alla volta: `python csv/_suite_al_bit.py --gira chiusura_S3 --forma S3`, poi `--gira chiusura_S1`. Si confrontano con `prima` e con `dopo_S3`/`dopo_S1`. Poi `python csv/solitone/collauda.py`.

## 3. I CRITERI *(del mandato, scritti prima)*

| | il criterio |
|---|---|
| `C1` | **DEVE:** col predefinito `S1`, `H_w` con pendenza `>= 1.9` in `(a)` e in `(b)`, come con `S3`. **Se non torna: FERMO.** |
| `C2` | **DEVE:** con `S3` esplicita, nessuna riga di fisica diversa da `prima.json`. **Le righe nuove dei bracci `S1` aggiunti non sono righe diverse:** si elencano a parte, come i metadati *(impronte, conteggi, righe di codice)*. |
| `C3` | **DEVE:** col predefinito `S1`, la suite intera con codice d'uscita `0`. |
| `C4` | **DEVE:** i `38` di `csv/solitone/` al bit, col `D6` riscritto. |
| `C5` | **DEVE:** la ricerca per formule dice **zero `legge a mano`** fuori da `materia_vuoto.py`, salvo gli strumenti di screening dichiarati. **E il caso che deve fallire fallisce.** |
| `C6` | Un solo processo di calcolo alla volta. Nessun parametro nuovo. Le tolleranze dei bracci nuovi vengono dalla forma *(scritte sopra)*, non da una scelta. |

## 4. LE LETTURE *(di Luca, scritte prima)*

- **(h1)** corretta `energia_pesata`, `H_w` torna a pendenza `~2`: era solo la formula vecchia;
- **(h2)** non torna: c'e' un'altra incoerenza fra la legge e l'energia;
- **(h3)** altro.
- ### ⚠ **La mia attesa, scritta prima:** `(h1)`, ma con **due** righe vecchie, non una *(`energia_pesata` e `_misura_mb2`)*. **Se torna correggendo solo `_misura_mb2` lo scrivo:** e' `(h1)` per la strada che la premessa non nominava.

## 5. LA STELLA POLARE

1. **`A14`:** l'energia del nucleo diventa **quella della legge che gira**. Con `cs` acceso la fase `CAMM-FASE-VUOTO` usa `Omega` da `H_k`, e `H_k` ora contiene la `N` di `S1`. **Questo e' il senso del mandato:** conservare l'energia della legge vera.
2. **Il gradino:** `(a)` per `S3` *(identita' al bit)*; per `S1`, la convergenza col passo *(pendenza `~2`)* e' una prova di coerenza, **non** un risultato fisico.
3. **Numeri e leggi:** nessun numero, nessuna legge nuova. **Si tolgono tre copie a mano di una legge.**
4. **Il verso:** non cambia. `N` entra in `H_k` col segno di prima; con `S1`, `N >= 0` invece di `<= 0`, e la fase `Omega` cambia di conseguenza.
5. **Emergente o imposto:** non si applica. E' coerenza fra la legge e la sua energia.

## 6. TODO

1. Questo file, committato **DA SOLO**.
2. `csv/_cerca_formule_legge.py` e la riga d'inventario, committati; girato **su `HEAD` prima della correzione** *(il caso che deve fallire)*.
3. La correzione *(`energia_pesata`, `_misura_mb2`)*, i collaudi *(`_collauda_materia_vuoto`, `_collauda_deriva`, `_collauda_mb1`, `_misura_completa_l2`)*, `D6`, i presidi *(`_rami_era2` se servono rami nuovi)*, l'inventario. `collauda.py --solo-veloci` nel messaggio. **Un commit.**
4. La ricerca per formule dopo la correzione *(`C5`)*; la suite `chiusura_S3`, poi `chiusura_S1`; la cassetta. **Uno alla volta.**
5. Il referto `doc/referti_l2/s1_nucleo_chiusura.txt`, la relazione, la MAPPA, `DECISIONI_NEL_CODICE` *(sez. `6`)*, l'esito qui.

## 7. L'ESITO
