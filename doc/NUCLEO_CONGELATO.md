# IL NUCLEO DEL PRINCIPALE E' CONGELATO

stato: CONGELATO

> **La decisione di Luca** *(2026-11-08, `21:47`-`21:49`, dopo il revert `de46816d`)*: **sul ramo `primo-ordine` NESSUN commit
> modifica file in `primo_ordine/`** *(il nucleo, le leggi, i collaudi del nucleo, `collauda.py` compreso)* **finche'
> `zero-nel-nucleo` non e' riunito al principale per decisione di Luca.** [[H-NUCLEO-CONGELATO]]

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
