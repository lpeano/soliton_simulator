# 2026-11-01 — LA CASSETTA DEGLI ATTREZZI DEL SOLITONE *(il mandato di Luca delle `01:22` del `2026-11-01`, ⑦ in coda; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; NESSUNA MODIFICA AL NUCLEO, NESSUNA CORSA LUNGA)*

> **La coda:** il controllo a vuoto congelato e' chiuso *(`da88f475`)*. Ora ⑦, poi ⑧ *(`01:27` + `01:28`)*.

## 1. LE PREMESSE DAL CODICE

**Dove stanno oggi gli strumenti** *(letti dal sorgente, cercati per nome di funzione)*:

| il tema | la funzione | il file |
|---|---|---|
| le uscite | `distanza`, `gruppi_di`, `uscite`, `margine`, `giudizio`; `Libero` *(il tick libero ricomposto dai mezzi pezzi di `_bande_piatte`)* | `csv/_chiudere_le_uscite.py` |
| le uscite | `altre` *(`(n3)`, le coppie dispersive `(c0)`-`(c2)`)*, `per_costruzione` | `csv/_massimo_di_B.py` |
| lo spettro dalla scena | `spettro(z, phi0)` *(`DV.matrice` a `AMP`, poi `DV.autovettori`)*, `residuo`, `famiglia` | `csv/_scatola.py` |
| il solitone protetto | `bloch_B`, `coppia` *(le due colonne QR del livello piu' alto di `A(Gamma)`)*, `q_migliore` *(theta, phi di `griglia.json`)*, `inviluppo` | `csv/_massimo_di_B.py`, `csv/_coppia_di_B.py`, `csv/_consolida_B.py` |
| la scena | `MB.scena(N, L, eps)` *(da `LP.scena`, `s` fissato dal modulo)*; `_vuoto_vivo_B.scena(s, vuoto, eps)` *(`s` e il vuoto come argomenti)* | `csv/_massimo_di_B.py`, `csv/_vuoto_vivo_B.py` |
| le misure | `CL.punto` *(`w`, il cuore netto `f_win`, `f_3w0`, il picco, `M`)*; `SN.campione` *(piu' la finestra liscia `f_liscia` e il baricentro)*; l'alone `1 - f_3w0` *(`_vuoto_vivo_B.misura`)* | `csv/_congelato_lungo.py`, `csv/_salti_nel_cuore.py`, `csv/_vuoto_vivo_B.py` |
| le bande di `D`, le rotazioni | `ML.Bande` *(`coeff`, `parte`, `misura`, `rotazione`)*; il periodo dai cambi di segno in `ML.analizza` | `csv/_modo_lento.py` |
| la forma della crescita | `LP.forma_pendenze` *(il criterio aggiunto, collaudato in `collaudo_forma`)* | `csv/_livelli_piatti.py` |
| la vita, il tasso | il primo `tau` con `|D|/|psi0| >= SOGLIA` *(`_modo_di_R.vita`, `SOGLIA = 1e-2`)*; `CO.limite` *(il limite superiore del tasso sull'ampiezza)* | `csv/_modo_di_R.py`, `csv/_consolida_B.py` |

**I due errori nati da qui, e dove la libreria li impedisce:**
- **la famiglia di pesi sbagliata** *(`c6ad04ac`, corretta in `d2b7a89b`)*: lo spettro di `r 1.5247` era calcolato coi pesi `a_n = pi, b_a = r pi` della famiglia `lp`, mentre lo stato era della famiglia `sb`. **Nella libreria lo spettro ha UNA sola firma: dalla scena `(z, phi0)`** *(`DV.matrice`)*, **mai da pesi passati a mano**; e quando si legge uno stato, **DEVE** tornare il suo residuo registrato *(entro `1e-6` relativo, la tolleranza di `_scatola.TOLL_RES_REL`)*;
- **il periodo campionato raro** *(gli alias, `03142636`)*: `ML.analizza` ricava il periodo dai cambi di segno senza guardare il passo. **Nella libreria la funzione vuole il passo come argomento** *(nessun default)*, **e accanto al periodo letto restituisce gli ALIAS compatibili coi campioni** *(le frequenze `|1/T +- k/passo|`)*: **un alias non si riconosce dai campioni da soli**, quindi la funzione non sceglie, **dichiara l'ambiguita'**, e chi la usa la scioglie con un'altra misura *(le rotazioni per banda, come in `03142636`)*. **Nessun numero scelto:** il limite di Nyquist `2` passi e' matematica.

**Le dipendenze nascoste che la libreria NON cambia:** `CB.coppia` e `MB.bloch_B` dividono la fase per il `S` del modulo *(`0.15`)*; `_vuoto_vivo_B.partenza` lo corregge con `E0 * CB.S / s`. **Nella libreria `s` e' un argomento**, e la conversione si fa una volta. **`DV.matrice` scrive `z["st"]` e lo rimette** *(la guardia di `6c5da5e8`)*: le misure si fanno comunque PRIMA della coppia, come in `CO.partenza_robusta`.

**Il metodo per il «al bit»:** le funzioni della libreria sono **le stesse espressioni** degli strumenti di oggi *(copiate, non richiamate: gli script vecchi restano come sono, punto `5`)*. I test confrontano coi numeri **gia' committati**: i `float` dei `.json`/`.jsonl` **con `==`**, e le righe dei referti di testo **rigenerate con lo stesso formato e cercate tali e quali** nel referto.

### Cosa NON so
- se `previsioni.json` di `_massimo_di_B` e la riga `(n2) P0 + Ppi 0.0096` bastino come riferimento delle uscite, o se qualche riga dei referti sia stata stampata da un codice diverso da quello di oggi *(lo dira' il test: (t2))*;
- quanto costa ogni test: lo misuro *(nessuna corsa lunga: al piu' un tick o una `DV.matrice` per test)*.

## 2. I CRITERI *(scritti prima)*

| il test | che cosa ridà AL BIT | il caso che DEVE fallire |
|---|---|---|
| `U1` | `uscite` + `altre` sullo spettro libero di `_massimo_di_B.previsioni`: **ogni valore di `previsioni.json`** *(eps `0.5` e `0`)* | lo stesso con `g` spostato di `1e-3`: non coincide |
| `U2` | `_chiudere_le_uscite`, eps `0`: `(n2) P0 + Ppi` a `mu -0.56602` = la riga del referto *(`%.5f`)* | -- |
| `U3` | lo spettro **dalla scena** di `r 1.5247` *(famiglia `sb`)*: il residuo dello stato = il registrato entro `1e-6` | **coi pesi della famiglia `lp`: DEVE fallire** *(l'errore di `c6ad04ac`)* |
| `P1` | `A` a `K`: lo stato della scena `N 1e6`, `L 81`, eps `0.5` -> `sha_partenza` e `mu` di `lunga_AK_00000.jsonl` *(`a8e0e43b`)* | -- |
| `P2` | `B` a `Gamma` dall'inviluppo: `robusta_N3e5_000000.jsonl` -> `sha_partenza`, `E0`, `bloch`, `mu`, `residuo` | con `q2` al posto della scelta migliore: lo `sha` non coincide |
| `P3` | `B` a `Gamma` con `s` come argomento: la partenza di BG-F-0.15 *(`_vuoto_vivo_B`)* -> `mu`, `w_in`, `e_K` del primo pezzo | -- |
| `M1` | `campione` sullo stato finale di `rig.npz` *(controllato con lo `sha_fine`)* = l'ultimo campione di `salti_nel_cuore` | la finestra netta al posto della liscia: diverso |
| `M2` | `punto` e l'alone sullo stato finale di `db/consolida_B/lunga_B.npz` = l'ultimo punto di `consolida_B`; **e le bande di `D`** = l'ultima riga `D` | -- |
| `M3` | `limite` sui pezzi di `a8e0e43b` = `limite_3000.json` | -- |
| `M4` | `forma_pendenze` sulla serie vera di `breve_R_1e6` e sui casi del collaudo = le righe di `livelli_piatti.txt` | i casi stessi sono i controlli: lineare, esponenziale, nullo |
| `M5` | la vita *(il primo `tau` sopra `1e-2`)* = gli `OSSERVATO` di `modo_di_R.txt` per `r 1` e `r 1.5247` | -- |
| `M6` | il periodo dai cambi di segno, su una serie sintetica, **col passo**: un periodo vero di `33` passi letto giusto; **un periodo vero di `1.1` passi** *(l'alias di `03142636`)* **NON letto giusto, ma il vero nella lista degli alias** | **senza il passo: DEVE rifiutare** *(la firma)* |

## 3. LE LETTURE *(di Luca, scritte prima)*

- **(t1)** ogni modulo ridà al bit i numeri committati;
- **(t2)** un modulo non li ridà: quale, e perche' *(un errore vecchio o nuovo)*.

## 4. LE MOTIVAZIONI

Gli strumenti di questo filone si importano a catena *(`_vuoto_vivo_B` -> `_consolida_B` -> `_coppia_di_B` -> `_massimo_di_B` -> `_livelli_piatti` -> `_modo_lento`, `_strada_b_*`)*, con copie e varianti, e due errori sono nati da qui. **Una libreria con un modulo per tema e i suoi test** fa si' che uno script nuovo non debba sapere quale script vecchio contiene la versione giusta. **I test al bit dicono che la libreria e' quella che ha prodotto i referti.**

## 5. TODO

1. Questo file, committato **DA SOLO**.
2. `csv/solitone/` *(`__init__.py`, `uscite.py`, `protetto.py`, `misure.py`)* e i test *(`test_uscite.py`, `test_protetto.py`, `test_misure.py`, e `collauda.py` che li gira)*, piu' le righe dell'inventario: committati **prima** di girarli.
3. `python csv/solitone/collauda.py > doc/referti_l2/cassetta_solitone.txt`: il referto, committato.
4. `RELAZIONE`, la MAPPA, la sezione `6` qui. **Se un test non passa: committare lo stato e FERMO.**
5. Le decisioni da chiudere *(la moneta (7), `S1` (1), le piatte (17, 19, 25), la regola dei livelli piatti)* **NON in questo mandato**: sono di Luca.

## 6. L'ESITO


**Il referto** *(`doc/referti_l2/cassetta_solitone.txt`, da `python csv/solitone/collauda.py`, girato a `37e56400`; i blob sha1-BYTE nel referto e nell'inventario)*. **La libreria `csv/solitone/`** ha tre moduli. Le funzioni sono **le stesse espressioni** degli strumenti che hanno prodotto i referti: sono copie, non richiami, e gli script vecchi non sono stati toccati.
- **`uscite`**: le uscite (n0)-(n3) e le coppie dispersive coi margini, con `Omega` come argomento. **Lo spettro ha una sola firma, dalla scena** *(`spettro_scena(z, phi0, s)`)*. Quando si legge uno stato, `stato_nella_scena` **rifiuta** *(con un `AssertionError`)* se il residuo registrato non torna entro `1e-6`;
- **`protetto`**: le due scene *(quella di riferimento e quella col vuoto scelto)*, la coppia di `B` a `Gamma` con `E0 = fase/s`, la scelta dentro la coppia, l'inviluppo, `A` a `K`, `mu` di Rayleigh. `N`, `eps`, `s`, `L` e la forma sono argomenti;
- **`misure`**: il cuore netto e quello liscio, `w`, l'alone, il baricentro, le bande di `D`, le rotazioni, la forma della crescita, la vita *(`1e-2`)*, il limite del tasso. **Il periodo dai cambi di segno vuole il passo** *(non ha un default)*, **e restituisce gli alias.**

**I test** *(tempi: `20`, `12` e `6` s)*:
- **le uscite:**
  - `U1`: le `24` uscite, `E0` e le bande di `previsioni.json`, a eps `0.5` e a eps `0`, AL BIT; con `g + 1e-3` non coincidono;
  - `U2`: la riga `(n2) P0 + Ppi` di `chiudere_le_uscite.txt`;
  - `U3`: `r 1.5247` dalla scena della sua famiglia: il residuo `1.685968e-10` e le bande libere sono le righe di `scatola/uscite.txt`. **Nella scena della famiglia sbagliata `stato_nella_scena` rifiuta** *(residuo `7.9e-2`: l'errore di `c6ad04ac`)*;
- **il solitone protetto:**
  - `P1`: `A` a `K` della corsa di `a8e0e43b`, lo `sha` e `mu`;
  - `P2`: `B` a `Gamma` dall'inviluppo a `N 3e5`: lo `sha`, `E0`, `bloch`, `mu` e il residuo di `robusta_N3e5`. Col partner della scelta lo `sha` non coincide;
  - `P3`: la partenza di BG-F-0.15 sulla scena del fondo: `mu`, il residuo, `w_in`, `h`, `e_K`. **`E0` coincide anche con la conversione fatta una volta sola** *(differenza `0`)*;
- **le misure:**
  - `M1`: il campione a `t 0` di `salti_nel_cuore` e il punto di `a8e0e43b`. La finestra netta e quella liscia sono diverse *(`0.620386` contro `0.618068`)*;
  - `M2`: lo stato di BG-F-0.15 al tick `20000`: il campione, l'alone e la riga `D` coincidono con l'ultimo pezzo;
  - `M3`: `limite_3000.json`;
  - `M4`: i `5` casi del collaudo della forma *(la serie vera di `breve_R_1e6` compresa)*, riga per riga;
  - `M5`: gli `OSSERVATO 142.2` e `621.8` di `modo_di_R.txt`;
  - `M6`: un periodo vero di `33` passi letto giusto. Un periodo vero di `1.1` passi viene letto `33.0`, cioè **l'alias**, e **il vero `3.3` compare fra gli alias**. Senza il passo, la funzione rifiuta.

**La lettura e' (t1).** Una nota onesta: i test confrontano con i numeri committati, quindi **dicono che la libreria e' il codice che ha prodotto quei referti, non che quei referti siano giusti**. Il `RuntimeWarning` *(una divisione per zero)* in `_scomposizione_solitone.parti`, chiamata da `e_K_di`, ricompare anche qui: `e_K` coincide al bit, ma il warning resta **in lista, non spiegato**.

**Per gli script nuovi:** `import solitone.uscite`, `solitone.protetto` e `solitone.misure`, con `csv/` nel `sys.path`.

**Il mandato delle `01:22` e' chiuso. Le decisioni che il mandato elenca** *(la moneta (7), `S1` (1), le piatte (17, 19, 25), la regola dei livelli piatti)* **restano di Luca.** **Il successivo in coda e' ⑧** *(`01:27` + `01:28`)*.
