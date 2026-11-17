# IL NUCLEO DEL PRINCIPALE E' CONGELATO

stato: CONGELATO

> **Ricongelato il 2026-11-16 dopo la riunione di numba** *(sbloccato SOLO per il merge `ca55169e`, con la riga di Luca delle `16:10`; le tre suite `67/67` dopo il merge)*.

> **La decisione di Luca** *(2026-11-08, `21:47`-`21:49`, dopo il revert `de46816d`)*: **sul ramo `primo-ordine` NESSUN commit
> modifica file in `primo_ordine/`** *(il nucleo, le leggi, i collaudi del nucleo, `collauda.py` compreso)* **finche'
> `zero-nel-nucleo` non e' riunito al principale per decisione di Luca.** [[H-NUCLEO-CONGELATO]]

## LA RIUNIONE *(Luca `2026-11-12` `10:39`: il passo `3` della ROTTA; U0 confermato da Luca; `doc/TASK_HISTORY/2026-11-12_unificazione.md`)*

- ### **Il nucleo del principale DIVENTA quello del laterale** *(con v2, lo zero simmetrico)*: **la fusione di `zero-nel-nucleo` a `986440d6` sul ramo `unificazione`** *(i tag `pre-unificazione-principale` `fca1dd26`, `pre-unificazione-laterale` `986440d6`)*.
- ### **Lo stato resta `CONGELATO`**, e **alla fine di U5 si RICONGELA sul nucleo UNIFICATO** *(la decisione di Luca)*.
  - **Il presidio non ha sha da aggiornare:** **blocca OGNI file sotto `primo_ordine/` sul ramo `primo-ordine`, qualunque contenuto.**
  - **Sul ramo `unificazione` non agisce** *(guarda il nome del ramo)*: **cosi' la fusione porta il nucleo.**
- **Il nucleo unificato, i file che cambiano rispetto al principale** *(`sha1-BYTE`, i byte grezzi)*:

| il file | prima *(`fca1dd26`)* | il nucleo unificato |
|---|---|---|
| `primo_ordine/_collauda_motore.py` | `e4526319` | `4d60d2f2` |
| `primo_ordine/_collauda_r60.py` | `2c972bfe` | `1ee3f0eb` |
| `primo_ordine/_mappa.yaml` | `1eb339be` | `f3bb3fdc` |
| `primo_ordine/_misura_hw.py` | `a28e1413` | `98c1d34b` |
| `primo_ordine/_misura_mb2.py` | `266b5600` | `48269077` |
| `primo_ordine/energia_pesata.py` | `cfaff204` | `43bce8ad` |
| `primo_ordine/flussi_parziali.py` | `1461182f` | `d43b1cf8` |
| `primo_ordine/leggi/leggi.yaml` | `809d7fdb` | `1c0eac29` |
| `primo_ordine/termini/camm_grover.py` | `925a9103` | `10b70489` |
| `primo_ordine/termini/camm_grover_vuoto.py` | `60ef8476` | `8f88bc20` |
| `primo_ordine/termini/camm_spostamento.py` | `4123e139` | `d58a753f` |
| `primo_ordine/termini/camm_spostamento_vuoto.py` | `a98c4267` | `a58a55ea` |

- ### **U5, FATTO** *(`2026-11-12`)*: **`primo-ordine` avanzato al ramo `unificazione`** *(U4 verde)*; **P3-D sul `primo-ordine` locale, prima del push: `4/4`** *(`doc/referti_l2/unificazione_p3_U5.txt`)*. ### **IL NUCLEO E' RICONGELATO SUL NUCLEO UNIFICATO** *(lo stato `CONGELATO`, il presidio attivo sul ramo `primo-ordine`)*.
- **La tabella dei due rami qui sotto e le regole 1-7 sono la STORIA fino alla riunione;** **dopo U5 c'e' un ramo solo.**

## Che cosa lo impone

**Il presidio `H-NUCLEO-CONGELATO`** *(`csv/_nucleo_congelato.py`, chiamato dal `pre-commit` in testa)*: sul ramo
`primo-ordine`, finche' questo file dice `stato: CONGELATO`, **ogni commit che tocca un file sotto `primo_ordine/` e'
RIFIUTATO.** **Se questo file manca, il nucleo e' CONGELATO lo stesso** *(chiuso per difetto)*.

## I due rami

| ramo | il nucleo | che cosa ci si fa |
|---|---|---|
| **`primo-ordine`** *(il principale)* | **SENZA v2, congelato** | gli allungamenti *(`C35-pi`, poi `S162`, poi `C50-0`)*; il referto di `C35-0`; il periodo di `TB3`; la stazionarieta'; T3 e la `U(1)` *(nella libreria)*; **la relazione, la MAPPA, gli indici** |
| **`zero-nel-nucleo`** *(il laterale, `C:\Users\lpeano\wt_zero`)* | **CON v2** | **(m-b)**; poi D0-D4 *(il punto fisso di `cs` col solitone)* e la sua cura; poi `cs` acceso col solitone e il peso del vuoto *(M1-M4 del progetto delle `16:44`)*; **ogni modifica del nucleo** |

## Le regole *(Luca)*

1. **Il nucleo del principale e' congelato** *(sopra)*. **Una modifica URGENTE del nucleo sul principale: FERMO e chiedere a Luca.** **Le modifiche della LIBRERIA (`csv/`) restano permesse sul principale, con la suite.**
2. **La relazione, la MAPPA e gli indici si aggiornano SOLO sul principale.** Il laterale scrive i suoi esiti in un task history e in referti SUOI; sul principale si aggiunge una riga che rimanda al commit del laterale.
3. **Il principale si fonde NEL laterale a intervalli** *(per esempio a ogni cura della libreria)*, **MAI il contrario fino alla riunione.**
4. **I processi: una corsa lunga e una prova corta alla volta, sommando i due rami.**
5. **La suite gira su ciascun ramo quando cambia un file che sorveglia, su quel ramo.**
6. **La riunione: v2 torna sul principale DOPO gli allungamenti, per decisione di Luca.** ### ⚠ **`16d2ebdb` e' stato annullato con un revert (`de46816d`): un nuovo merge di `zero-nel-nucleo` NON riporterebbe le modifiche.** **Servira' il revert del revert, o ricreare il ramo dai commit di v2** *(il task history di v2)*.
7. **Il braccio 0, per il futuro: ogni cambio del nucleo controlla anche le COSTANTI dei referti** *(`e_K`, le unita' dell'energia, l'intestazione della scena della corsa)*, **non solo le chiavi della dinamica.** **Dopo la riunione, lo spostamento di `pi` per norma dell'energia si DICHIARA nei referti per il confronto con le corse vecchie.**

## Come si sblocca

**Solo con una decisione SCRITTA di Luca:** questo file passa a `stato: SBLOCCATO` **con** una riga
`decisione_di_luca: <data, ora, il testo o il riferimento>`. **Senza quella riga, uno stato diverso da `CONGELATO`
RIFIUTA ogni commit sul principale.** ### ⚠ **Il limite** *(`A9`)*: **il presidio impedisce di DIMENTICARE, non di
scrivere la riga senza la decisione: quella resta una regola.** **E una testa staccata non ha ramo: il presidio non la vede.**

## LA RIUNIONE DI NUMBA SUL PRINCIPALE *(decisione di Luca 2026-11-16 15:50 (15/11), 18:08, 19:12, 19:57, 13:58 e il via delle 16:10)*

- **Il merge di `motore-numba` nel principale porta nel nucleo UN file nuovo** *(`primo_ordine/motore_numba.py`, lo switch SPENTO per difetto)* **e UNA voce nella mappa** *(`primo_ordine/_mappa.yaml`)*; **nessun file di fisica del nucleo cambia.** **Lo stato e' stato SBLOCCATO SOLO per il commit del merge** *(`ca55169e`, la riga `decisione_di_luca` delle `16:10`)* **ed e' RICONGELATO nel commit dopo le tre suite** *(`67/67` su E: spento, su C: spento, su E: acceso)*.

| il file | il nucleo del principale, prima | il nucleo del principale, dopo la riunione di numba |
|---|---|---|
| `primo_ordine/_collauda_motore.py` | `4d60d2f2` | `4d60d2f2` |
| `primo_ordine/_collauda_r60.py` | `1ee3f0eb` | `1ee3f0eb` |
| `primo_ordine/_mappa.yaml` | `f3bb3fdc` | `26f2abaf` **(CAMBIA: la voce `motore_numba.py`)** |
| `primo_ordine/_misura_hw.py` | `98c1d34b` | `98c1d34b` |
| `primo_ordine/_misura_mb2.py` | `48269077` | `48269077` |
| `primo_ordine/energia_pesata.py` | `43bce8ad` | `43bce8ad` |
| `primo_ordine/flussi_parziali.py` | `d43b1cf8` | `d43b1cf8` |
| `primo_ordine/leggi/leggi.yaml` | `1c0eac29` | `1c0eac29` |
| `primo_ordine/termini/camm_grover.py` | `10b70489` | `10b70489` |
| `primo_ordine/termini/camm_grover_vuoto.py` | `8f88bc20` | `8f88bc20` |
| `primo_ordine/termini/camm_spostamento.py` | `d58a753f` | `d58a753f` |
| `primo_ordine/termini/camm_spostamento_vuoto.py` | `a58a55ea` | `a58a55ea` |
| `primo_ordine/motore_numba.py` | *(non c'e')* | `61a3e756` **(NUOVO)** |

- **Gli altri `11`: IDENTICI** *(`sha1-BYTE` misurati dal disco del merge, `2026-11-16`)*.

## IL RAMO `motore-numba` *(decisione di Luca 2026-11-15 15:50, 18:08, 19:12, 19:57; la carta `doc/TASK_HISTORY/2026-11-15_motore_numba.md`)*

- **Sul ramo `motore-numba` il nucleo cambia per decisione di Luca: UN file nuovo** *(`primo_ordine/motore_numba.py`)* **e UNA voce nella mappa** *(`primo_ordine/_mappa.yaml`, la strada (a) delle `19:57`: P-MOD vuole ogni modulo in mappa)*; **nessun file di fisica del nucleo cambia.** *(`H-NUCLEO-CONGELATO` blocca solo il ramo `primo-ordine`.)*

| il file | il nucleo di oggi | il ramo `motore-numba` |
|---|---|---|
| `primo_ordine/_collauda_motore.py` | `4d60d2f2` | `4d60d2f2` |
| `primo_ordine/_collauda_r60.py` | `1ee3f0eb` | `1ee3f0eb` |
| `primo_ordine/_mappa.yaml` | `f3bb3fdc` | `26f2abaf` **(CAMBIA; `3dbf10ef` a `e1df85c3`, poi la dipendenza `flussi_parziali` del secondo passo)** |
| `primo_ordine/_misura_hw.py` | `98c1d34b` | `98c1d34b` |
| `primo_ordine/_misura_mb2.py` | `48269077` | `48269077` |
| `primo_ordine/energia_pesata.py` | `43bce8ad` | `43bce8ad` |
| `primo_ordine/flussi_parziali.py` | `d43b1cf8` | `d43b1cf8` |
| `primo_ordine/leggi/leggi.yaml` | `1c0eac29` | `1c0eac29` |
| `primo_ordine/termini/camm_grover.py` | `10b70489` | `10b70489` |
| `primo_ordine/termini/camm_grover_vuoto.py` | `8f88bc20` | `8f88bc20` |
| `primo_ordine/termini/camm_spostamento.py` | `d58a753f` | `d58a753f` |
| `primo_ordine/termini/camm_spostamento_vuoto.py` | `a58a55ea` | `a58a55ea` |
| `primo_ordine/motore_numba.py` | *(non c'e')* | `61a3e756` **(NUOVO; `40d05c43` a `e1df85c3`, `8c7bc873` a `330d3718`, `eea1d3b0` a `5b33b7f5` il secondo passo W3, `92113af2` a `c87fad26` l'argomento `fma` di H1, `a43a3a3c` a `0d7cfa0f` il modo `esplicita`: la FMA vera, Luca 2026-11-16 08:57, poi la firma dell'intrinseco)** |

- **Gli altri `11` file della tabella: IDENTICI** *(`sha1-BYTE` misurati nel clone).* **Il guardiano verifica questo ramo contro questa tabella.**

## IL RAMO `mitosi` *(decisioni di Luca 2026-11-17 11:33 e 16:38: D-M1, D-R5; la carta `doc/TASK_HISTORY/2026-11-17_mitosi_verso_il_test.md`)*

- **Sul ramo `mitosi` il presidio NON agisce** *(guarda il nome del ramo)*: **il nucleo cambia SOLO per l'INFRASTRUTTURA che non dipende dalla regola di `phi_h`** *(D-R5)*; **la regola della nascita resta FERMA fino a D-M3.** **Nulla torna al principale senza un mandato di Luca** *(R-NAVI)*.
- **B2, `Motore.cresci` completo** *(dalla base `37e43b3d`)*: **la geometria** *(`n` per estremita', `U` per arco)*, **`dtau`, `cs` e le chiavi PER NODO dello stato** *(`psi`, `Lambda`, `rho`, `h_int`)* **seguono la crescita**, **i valori nuovi SOLO da `iniziali`** *(nessun default di fisica)*, **tutti controllati PRIMA di toccare qualunque cosa**; **la cache di numba si svuota.** **Il corpo sta nel modulo NUOVO `primo_ordine/crescita_dati.py`**: **`motore.py` col corpo dentro arrivava a `760` righe, oltre il tetto di `700`** *(ora `697`)*.

| il file *(`sha1-BYTE`, i byte grezzi)* | prima *(`37e43b3d`)* | B2 |
|---|---|---|
| `csv/_file_fisica.py` | `c63f4908` | `793f38b4` |
| `csv/_rami_era2.py` | `38c0d4ef` | `74b16007` |
| `primo_ordine/_collauda_motore.py` | `4d60d2f2` | `f0a8f90a` |
| `primo_ordine/_mappa.yaml` | `26f2abaf` | `376b4d37` |
| `primo_ordine/crescita_dati.py` | *(nuovo)* | `3be38e61` |
| `primo_ordine/flussi_parziali.py` | `d43b1cf8` | `1a7e973e` *(solo il commento e il messaggio di `dtau_nodo`)* |
| `primo_ordine/motore.py` | `0e07bbfd` | `5582c4af` |
