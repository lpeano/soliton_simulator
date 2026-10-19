# LA RIMOZIONE DEL RAMO DEL PUNTO MEDIO PER PEZZO

> **Il mandato:** decisione di Luca del `2026-10-18` alle `21:48`, registrata in
> `doc/CODA_2026-10-16.md` *(la sezione della rimozione, col perimetro del guardiano e la
> riga sulla RIPRESA)*. Viene **dopo** il censimento dei punti fissi e la matrice *(passi
> `A`-`E` della memoria, chiusi in `94aeda64`)* e **prima** di `D4`.
> **Il motivo, con le parole del mandato:** col `G` letto sullo stato il passo di default da'
> `C1 = 2.091` e il ramo acceso `2.019`, quindi ### **il ramo non serve**; acceso, il punto
> fisso di `cs` non converge in `4` casi su `8`; ### **un ramo spento e' una trappola per chi
> verra' dopo.** Codice e numeri restano nella storia *(`2c95af13`)* e nel referto
> `doc/referti_l2/punto_medio_per_pezzo.txt`.

**LIVELLO CORRENTE:** `L2`/`L3`, la coda dopo la memoria. ### **E' la rimozione di uno
schema SPENTO: il passo di default non deve cambiare, e l'impronta resta
`2e7f795d2a52fbe7`** *(la tabella delle leggi non si tocca)*.

## 0. LA STELLA POLARE — *le cinque risposte, PRIMA del codice*

1. **`A14`, conserva energia e carica localmente?** ### **Non cambia niente:** il ramo e'
   spento, e il passo che gira e' quello di prima **al bit** *(e' cio' che il braccio `0`
   misura)*. La rimozione non tocca nessuna legge.
2. **A quale gradino arriva?** `(a)`: `M-B1` al bit su due scene, `C1` rifatto, un caso che
   deve fallire. `(b)` e `(c)`: ### **non si applicano, perche' non si afferma nessun
   fenomeno** -- si toglie del codice che non gira.
3. **Aggiunge un numero o una legge?** ### **Ne TOGLIE:** `EPS_PUNTO_FISSO` *(un doppione
   di `tick.EPS_CS`)*, `GIRI_MAX_PESO` *(un tetto di giri)*, un punto fisso, un ramo nel
   motore, e l'`assert` che sorvegliava il doppione. Nessuna toppa, nessun clip.
4. **Tocca `rho`, `c_s` o il segno?** ### **Tocca solo il ramo spento**, che usava `cs`
   per il peso d'arco al punto medio. Col ramo spento ### **nessun verso dell'accoppiamento
   cambia.**
5. **Emergente o imposto?** ### **Non si applica**: nessun fenomeno viene affermato; e
   `C1` deve ridare **lo stesso numero** di prima, non uno migliore.

## 1. RAGIONAMENTO PRELIMINARE — *che cosa credo PRIMA di guardare*

- **Il censimento:** il guardiano conta i nomi del ramo *(`regola_punto_medio`,
  `hop_phi_punto_medio`, `s_arco_da_lambda`, `z_arco_da_s`, `hop_phi_con_s`, `giri_peso`,
  `EPS_PUNTO_FISSO`, `_misura_punto_medio`)* in ### **`8` file e `37` righe** fuori da
  `doc/` e dalla relazione. ### **Il mio numero lo da' uno script**, e ### **credo che sia
  diverso:** il mio passo `C` *(`csv/_matrice_dipendenze.py`)* e il passo `B` non nominano
  quelle funzioni, ma `csv/_censimento_punti_fissi.py` nomina `hop_phi_punto_medio` fra i
  previsti -- quindi ### **credo almeno `1` file in piu'.** Se e' diverso, ### **spiego la
  differenza file per file.**
- **Che cosa ho letto nel codice:** dopo `2c95af13^` i tre file del nucleo
  *(`flussi_parziali.py`, `motore.py`, `tick.py`)* li ha toccati ### **SOLO `2c95af13`**, e
  il suo diff su quei tre e' ### **tutto ramo** *(le due funzioni ritagliate, le due costanti,
  `s_arco_da_lambda`, `hop_phi_punto_medio`, i due attributi e il ramo nel motore, il
  doppione con l'`assert`)*. ### **Quindi la rimozione e' TORNARE AI BYTE DEL PADRE
  `2c95af13^`** per quei tre file *(con `git cat-file`, in binario: par.`7`)*.
- **`z_arco_da_s` e `hop_phi_con_s`:** stanno nel percorso di default *(le chiamano `z_arco`
  e `hop_phi`)*. ### **Tornando al padre, `z_arco` e `hop_phi` riprendono la forma che
  avevano**, con ### **le stesse operazioni nello stesso ordine** *(il docstring di
  `z_arco_da_s` lo diceva gia')*. ### **Credo che il passo resti identico al bit.** Se `M-B1`
  dice di no, ### **le due funzioni tornano**, e la rimozione si limita al resto.
- **Che cosa NON so:** se qualche strumento fuori dal nucleo *(collaudi, misure)* chiama
  ancora uno di quei nomi, e si romperebbe. ### **Lo dice il censimento**, prima del codice.

## 2. PROGETTAZIONE — *i passi, e cosa FERMA ciascuno*

| | il passo | che cosa DECIDE | che cosa mi FERMA |
|---|---|---|---|
| `1` | `csv/_censimento_ramo_punto_medio.py`: i nomi del ramo in ogni file tracciato, ### **codice e documentazione separati** | il perimetro | -- |
| `2` | i tre file del nucleo **ai byte di `2c95af13^`**; `_misura_punto_medio.py` senza i bracci che accendono il ramo *(il censimento dei `14` pezzi resta, con una nota che rimanda a `2c95af13` e al referto)*; `csv/_rami_era2.py` senza i due rami dichiarati; gli altri file del censimento | il codice | un file che **chiama** un nome tolto, e non e' nel censimento |
| `3` | ### **il braccio `0`:** `python primo_ordine/_misura_mb1.py --contro <HEAD prima della rimozione>` | ### **`M-B1` al bit, distanza del passo intero `0` esatto, su ENTRAMBE le scene** | ### **un solo bit diverso: STOP**, e `z_arco_da_s`/`hop_phi_con_s` tornano |
| `4` | ### **il caso che DEVE fallire:** `python primo_ordine/_misura_mb1.py --collaudo` *(un operatore e l'ordine alterati apposta)* | che il braccio `0` **puo' dire NO** | ### **se l'alterato passa: STOP** |
| `5` | ### **il controllo che deve riuscire:** `C1` rifatto sul blob nuovo | ### **`2.091`**, coi casi che devono fallire *(`0.044` e `0.012`)* | un numero diverso: STOP |
| `6` | il censimento rifatto **dopo** | ### **`0` occorrenze dei nomi tolti nel codice**, salvo `_misura_punto_medio` *(il file resta)* | un nome rimasto nel codice |
| `7` | inventario, mappa, coda, RIPRESA *(la sezione che manca, col rimando a `g_dello_stato` e all'errore `n.12`)*, la voce della memoria *(il conto DOPO)* | -- | -- |

### ⛔ **E IL CASO CHE DEVE FALLIRE E' QUELLO DEL GUARDIANO** *(la versione piu' recente del
mandato, in coda: «un `M-B1` contro un passo alterato apposta, che deve dare distanza
`> 0`»)* -- ### **e c'e' gia':** e' il `--collaudo` di `_misura_mb1.py`. ### **Lo dichiaro
qui, prima.**
### 📌 **E `_misura_punto_medio.py` resta RIGIRABILE AL SUO COMMIT** *(`880955bb`, il
referto `punto_medio_per_pezzo.txt`)*: ### **l'inventario lo dice.**

## 3. TODO DEL NEXT STEP

1. lo script del censimento, committato; la corsa **prima** della rimozione, col referto.
2. la rimozione *(un commit)*, coi file del censimento.
3. `M-B1 --contro` sulle due scene, e `--collaudo`.
4. `C1` rifatto *(`primo_ordine/_misura_strada_d.py`)*.
5. il censimento **dopo**, col referto.
6. inventario, mappa, coda, RIPRESA, la voce della memoria; la relazione.
