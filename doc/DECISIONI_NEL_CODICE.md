# LE DECISIONI DI LUCA NEL CODICE *(il mandato delle `01:28` del `2026-11-01`, punto `5`: PRIMA la lettura, nessuna modifica; il task history `doc/TASK_HISTORY/2026-11-01_decisioni_nel_codice.md`)*

> **Le decisioni** *(Luca `01:27`; la MAPPA, sez. `5`)*: **(7)** la moneta accesa, eps `0.5` come nella tabella; **(1)** `S1`; **le piatte**, la strada (A), il solitone sul massimo di `B` a `Gamma`.
> **I numeri di riga sono quelli dei blob di oggi** *(sha1-BYTE accanto a ogni file)*: si cercano per nome di funzione, perche' le righe si spostano.

## 1. (7) eps

| dove | il blob | la riga | che cosa fa |
|---|---|---|---|
| `primo_ordine/leggi/leggi.yaml`, `CAMM-MONETA-SPIN`, `parametri.eps.valore` | `2593860b` | `342` | **`0.5`: la tabella = il deciso** |
| `primo_ordine/scena_l2.py`, `EPS_MONETA` *(restituito da `scena_toro`)* | `a581e3cd` | `81`, `115` | **`0.5` scritto a mano nel nucleo**, non letto dalla tabella; e un secondo `{"eps": 0.5}` alla riga `283`. **Il valore e' quello deciso**, ma e' **una seconda fonte** *(la regola `STRUMENTO-LEGGE-DALLA-TABELLA`)*. **E' nel nucleo: non toccato, segnalato.** |
| `csv/_energia_del_legame.py`, `stato` | `0d9ed2c0` | `77` | **scrive `par["eps"] = 0.0`** sulla scena di `scena_toro`; **e' la scena di tutto il filone** *(`_deriva_congelato.nuovo`, riga `68`; `_diagnosi_s4.iniziale`; `_livelli_piatti.scena`; `_massimo_di_B.scena`; `_vuoto_vivo_B.scena`)* |
| `csv/_energia_del_legame.py`, `PAR` *(il libro dei conti, `per_nodo`)* | `0d9ed2c0` | `39` | `{"eps": 0.0}`: il default del libro dei conti; chi gira a eps acceso passa `par` *(`029cac81`)* |
| `csv/_solitone_vuoto_congelato.py`, `controllo_zero` e `corsa` | `81db8c0a` | `80`, `108` | scrivono `par["eps"] = 0.0` |
| `csv/_scomposizione_solitone.py`, `scena` | `17dde60a` | `65` | scrive `0.0` |
| `csv/_solitoni_triangoli.py`, `dinamica` | `ec6fb68a` | `135` | scrive `0.0` |
| `csv/_solitoni_in_gradiente.py`, `scena` | `f3c68bd2` | `77` | scrive `0.0` |
| `csv/_vuoto_da_solo.py`, `corsa`; `csv/_vuoto_disturbato.py`, `corsa` | `e9c2f408`, `c4f03848` | `64`; `78` | scrivono `0.0` |
| `csv/_massimo_di_B.py`, `scena`; `csv/_vuoto_vivo_B.py`, `scena` | `b75de4f9`, `25170803` | `71`; `81` | **rimettono eps a mano** *(`z["par"]["eps"] = eps`, l'argomento)*: il filone del solitone protetto gira a `0.5` cosi' |
| `csv/solitone/protetto.py`, `scena_riferimento`, `scena_vuoto` | `47605b08` | -- | eps **argomento, senza default** |

**La lettura:** la tabella e il nucleo dicono `0.5`, **le scene condivise di `csv/` scrivono `0`**, e il filone del solitone protetto lo rimette a `0.5` a mano. **Gli script del filone `S1` a eps `0`** *(`_livelli_piatti`, `_modo_lento`, `_strada_b_*`, `_dove_va_la_materia`, ...)* **ottengono `0` dalla scena condivisa**: se `_energia_del_legame.stato` leggesse la tabella, cambierebbero risultato.

## 2. (1) la forma del legame

| dove | il blob | la riga | che cosa fa |
|---|---|---|---|
| `primo_ordine/materia_vuoto.py`, `alpha`, `beta`, `pezzi` | `68ff3ffd` | `80`, `94`, `111` | **`S3`:** `alpha = ln(rho/(rho+Lambda)) + Lambda/(rho+Lambda)`, `beta = -rho/(rho+Lambda)`. **Il predefinito del nucleo NON e' il deciso.** |
| `csv/_screening_forme_s3.py`, `forma(nome)`, `pezzi_di(nome)` | `80ffe96c` | `90`, `69` | **mette `S1` in memoria**, sostituendo `MV.pezzi` dentro un contesto, e lo rimette all'uscita |
| `csv/_solitone_vuoto_congelato.py`, `FORMA` | `81db8c0a` | `27` | **`"S1"`**: il predefinito degli strumenti condivisi di `csv/` |
| `csv/_livelli_piatti.py`, `FORMA` | `8ff427e5` | `36` | `"S1"` |

**La lettura:** in `csv/` `S1` e' gia' il predefinito, ma **il nucleo usa `S3`**. **E' il caso del punto `7` del mandato:** la modifica che servirebbe e' nel nucleo *(sotto)*.

## 3. Le piatte, la strada (A): il costruttore del solitone

| dove | il blob | la riga | che cosa fa |
|---|---|---|---|
| `csv/_energia_del_legame.py`, `stato` | `0d9ed2c0` | `85`-`86` | **`A` a `K`:** l'inviluppo `g` per `Q_K` di `_triangoli_forza.coppia_K` e la fase di `K`: **lo stato iniziale di ogni scena del filone** |
| `csv/_consolida_B.py`, `q_migliore`, `inviluppo` | `22086409` | `127`, `136` | **`B` a `Gamma`:** la scelta migliore da `griglia.json`, l'inviluppo di `pK` per lo spinore |
| `csv/solitone/protetto.py`, `coppia`, `griglia`, `scelta`, `inviluppo`, `stato_AK` | `47605b08` | -- | gli stessi costruttori, con `N`, `eps`, `s`, `L` come argomenti *(collaudati al bit in `55962e54`)* |

## 4. CHE COSA SERVIREBBE NEL NUCLEO *(punto `7`: NON fatto, decide Luca)*

- **(1) la forma:** in `primo_ordine/materia_vuoto.py` `alpha` e `beta` *(e `pezzi`, che le chiama)* dovrebbero dare quelle di `S1` *(le espressioni di `_screening_forme_s3.pezzi_di("S1")`)*. **Ma in `primo_ordine/` le leggi non si scrivono a mano:** la via e' la tabella `primo_ordine/leggi/leggi.yaml` e il generatore *(`doc/COME_SI_AGGIUNGE_UNA_LEGGE.md`)*, poi la suite.- **(7) eps:** il nucleo e' gia' a `0.5`. **La seconda fonte** in `primo_ordine/scena_l2.py` *(`EPS_MONETA = 0.5` e il `{"eps": 0.5}` della riga `283`)* dovrebbe leggere la tabella. Il valore non cambia: **e' pulizia, non fisica.**

## 5. DOPO LA DECISIONE DI LUCA DELLE `16:52` *(`c7ad2238`; il referto `doc/referti_l2/s1_e_moneta_nel_nucleo.txt`)*

- **(1) la forma:** `primo_ordine/leggi/leggi.yaml`, `CAMM-MATERIA-VUOTO`, `parametri.forma` *(`S1` predefinita, `S3` ammessa)*; `primo_ordine/materia_vuoto.py` legge `FORMA` dal modulo generato `termini/camm_materia_vuoto.py`; `N_s1`, `alpha_s1`, `beta_s1` *(le espressioni di `csv/`)* e `N_s3`, `alpha_s3`, `beta_s3` *(i corpi di prima)*; `scegli` e `forma_esplicita` per `S3`. **Le sezioni `2` e `4` qui sopra descrivono il nucleo di PRIMA.**
- **(7) eps:** solo dalla tabella *(`dict(termini.camm_moneta_spin.PARAMETRI)`)*: tolti `scena_l2.EPS_MONETA` e i `20` `{"eps": 0.5}` del nucleo e dei suoi collaudi. **La seconda fonte della sezione `1` non c'e' piu'.**
- **le scene di `csv/`** *(`_energia_del_legame.stato` e le altre della sezione `1`)* **restano a eps `0`: STORICHE** *(Luca `16:52`)*; `csv/solitone/protetto.forma_predefinita` legge la forma dalla tabella.

## 6. LA CHIUSURA *(`00821633`; il referto `doc/referti_l2/s1_nucleo_chiusura.txt`)*

- **La `N` dell'energia** viene da `materia_vuoto` *(per nome di modulo)* in `energia_pesata.termini_di_h`, `_misura_mb2.h_tot` e `_misura_mb2.pezzi_di_h`: **fuori da `materia_vuoto.py` nessuna formula della legge scritta a mano** *(`csv/_cerca_formule_legge.py`)*.
- **I collaudi legati a `S3` esplicita**, coi loro equivalenti `S1`: `_collauda_materia_vuoto` `(0)` e `(4)`, `_collauda_deriva` `(1-bis)`. **`M-B1`:** riferimento `8c7b9288` per `S3`, `c7ad2238` per `S1`. **`A2` di `L2`:** la forma del protocollo statico da `MV.ATTIVA` *(la mia lettura)*.
- ### ⚠ **APERTO:** `e_K` della libreria *(lo storico `_vuoto_vivo_B.e_K_di`)* cambia di `1.0` con `S1`. Decide Luca.
