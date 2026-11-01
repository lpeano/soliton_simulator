# 2026-11-01 — LE DECISIONI CHIUSE, LE VOCI SUPERATE, LE DECISIONI NEL CODICE *(i mandati di Luca delle `01:27` e `01:28` del `2026-11-01`, ⑧ in coda; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; NESSUNA CORSA, NESSUNA MODIFICA AL NUCLEO)*

> **La coda:** ⑦ chiuso *(`55962e54`)*. ⑧ e' l'ultimo mandato in coda.

## 1. LE PREMESSE DAL CODICE

**Le tre decisioni di Luca** *(`01:27`, punto `1`)*: **(7)** la moneta accesa, eps `0.5` come nella tabella; **(1)** `S1`; **le piatte, la strada (A)**, il solitone sul massimo di `B` a `Gamma`, nessuna cura.

**Dove vivono oggi** *(lette dal sorgente, cercate per nome)*:
- **(7) eps.** La tabella: `primo_ordine/leggi/leggi.yaml`, `CAMM-MONETA-SPIN`, `parametri.eps.valore: 0.5` **= il deciso.** Ma **gli strumenti di scena di `csv/` scrivono `0`** *(non per omissione: lo SCRIVONO)*: `_energia_del_legame.stato` *(`par["eps"] = 0.0`, e `PAR = {"eps": 0.0}` del libro dei conti)*, `_solitone_vuoto_congelato` *(due punti)*, `_scomposizione_solitone`, `_solitoni_triangoli`, `_solitoni_in_gradiente`, `_vuoto_da_solo`, `_vuoto_disturbato`. **Le scene del filone del solitone protetto lo rimettono a mano:** `_massimo_di_B.scena` e `_vuoto_vivo_B.scena` *(`z["par"]["eps"] = eps`)*. La libreria `csv/solitone/` lo vuole come argomento, senza default.
- **(1) la forma.** **Il nucleo usa `S3`:** `primo_ordine/materia_vuoto.py`, `alpha = ln(rho/(rho+Lambda)) + Lambda/(rho+Lambda)`, `beta = -rho/(rho+Lambda)`. **`S1` entra SOLO in memoria**, da `csv/`: `_screening_forme_s3.forma(nome)` sostituisce `MV.pezzi` dentro un contesto, e `_solitone_vuoto_congelato.FORMA = "S1"`, `_livelli_piatti.FORMA = "S1"`.
- **le piatte, (A).** Lo stato di `A` a `K` si costruisce in `_energia_del_legame.stato` *(l'inviluppo per `Q_K` e la fase di `K`)*; quello su `B` a `Gamma` in `_consolida_B.inviluppo` + `q_migliore`, e oggi in `csv/solitone/protetto.py` *(`inviluppo`, `scelta`, `griglia`)*.

**Che cosa ne segue, PRIMA di toccare niente:**
- **(1) richiede il nucleo:** il valore predefinito della forma vive in un file del nucleo con un valore diverso da quello deciso. **E' il caso del punto `7`: FERMO su questo punto**, scritto a Luca con il file, le righe e la modifica che servirebbe. In `csv/` `S1` e' gia' il predefinito degli strumenti condivisi.
- **(7) negli strumenti condivisi c'e' un CONFLITTO fra due richieste dello stesso mandato:** «il valore predefinito di ogni scena e' quello della TABELLA» e «gli script vecchi non si cambiano e ridanno al bit i loro referti». Gli script del filone `S1` a eps `0` *(`_livelli_piatti`, `_modo_lento`, `_strada_b_*`, `_dove_va_la_materia`, ...)* **ottengono eps `0` dalle scene condivise** *(`_energia_del_legame.stato`)*: se la scena condivisa passa a `0.5`, quegli script **cambiano risultato** se non vengono modificati per chiedere il caso ridotto. **Non si possono avere tutte e due.** **Non scelgo io:** lo scrivo a Luca *(sez. `5`, la raccomandazione)*.
- **Quello che si puo' fare senza conflitto: l'allineamento nella libreria NUOVA** *(`csv/solitone/`, che nessuno script vecchio importa)*: eps letto dalla tabella, `ridotto=True` per eps `0` col «caso ridotto» stampato; il costruttore predefinito su `B` a `Gamma`, `A` a `K` con un argomento esplicito; la forma `S1` letta da dove vive in `csv/` *(`_solitone_vuoto_congelato.FORMA`)*.
- **Il DEVE dei tre referti vecchi:** se nessun modulo che gli script vecchi importano cambia, **il blob di ognuno resta quello di prima**, e lo dimostro cosi' *(la catena degli import di ciascuno, blob per blob, prima e dopo)*. **Rigirarli non aggiungerebbe niente:** un referto rifatto da byte identici e' un FALSO-UNO. Lo dichiaro.

### Cosa NON so
- se Luca intendeva «gli strumenti condivisi» come le scene di `csv/` *(allora il conflitto e' suo da sciogliere)* o come la libreria *(allora l'allineamento qui basta)*.

## 2. I CRITERI *(scritti prima)*

| il punto | il criterio |
|---|---|
| `D1` | **la MAPPA, sez. `5`:** (7), (1), le piatte segnate PRESE con data, ora e i commit che le motivano; accanto a ognuna «nel codice: ...». |
| `D2` | **la MAPPA, sez. `4`:** le voci `13`, `15`, `16`, `17`, `19`, `20`, `22`, `25`, `26`, `29` chiuse, ciascuna con una riga di motivo e il commit; le aperte del punto `3` annotate, non toccate. |
| `D3` | `doc/BANDE_PIATTE.md` e `doc/CHIUDERE_LE_USCITE.md`: una riga in cima; `RELAZIONE`: un paragrafo. |
| `D4` | **la lettura** *(punto `5`)*: `doc/DECISIONI_NEL_CODICE.md`, ogni punto col file e la funzione *(i numeri di riga al blob di oggi, dichiarati)*. |
| `D5` | **l'allineamento nella libreria:** **DEVE** il collaudo `csv/solitone/collauda.py` passare ancora tutto *(i test usano argomenti espliciti)*, piu' i test nuovi: eps letto **=** `0.5` della tabella; `ridotto=True` **=** `0` e dichiarato; il costruttore predefinito **=** l'inviluppo su `B` a `Gamma` *(lo `sha` di `P3`)*; **DEVE FALLIRE:** il costruttore predefinito confrontato con `A` a `K`. |
| `D6` | **i tre referti vecchi** *(dichiarati: eps `0` `doc/referti_l2/livelli_piatti.txt`; eps `0.5` `doc/referti_l2/massimo_di_B.txt`; `A` a `K` `doc/referti_l2/coppia_di_B.txt`)*: **DEVE** il blob di ogni modulo della catena degli import dello script = quello di prima dell'allineamento. |
| `D7` | **FERMO** su (1) nel nucleo e sul conflitto di (7) nelle scene condivise: scritti a Luca, col file, la funzione e la modifica che servirebbe. |

## 3. LE LETTURE

Nessuna lettura fisica: e' scrittura e allineamento. **Il criterio di chiusura delle due domande a Luca:** una sua decisione registrata nella MAPPA.

## 4. LE MOTIVAZIONI

Le decisioni prese da Luca vanno dove le legge chi lavora *(la MAPPA, i documenti, il codice)*; una decisione scritta in un posto e contraddetta dal codice **non e' presa**. E un allineamento che cambia in silenzio i referti vecchi **distrugge la loro riproducibilita'**: per questo il conflitto va a Luca.

## 5. TODO

1. Questo file, committato **DA SOLO**.
2. `D1`-`D3`: la MAPPA, i due documenti, la relazione. Commit.
3. `D4`: `doc/DECISIONI_NEL_CODICE.md`. Commit.
4. `D5`: la libreria e i test nuovi, committati **prima** di girarli; il collaudo; il referto. `D6` nello stesso referto.
5. `D7`: la MAPPA «nel codice: ...», la relazione, **FERMO** coi due punti per Luca.

**La raccomandazione per il conflitto di (7)** *(di Luca)*: **lasciare le scene condivise come sono** *(scrivono `0` in modo esplicito, ed e' il comportamento con cui i referti vecchi sono nati)* **e fare della libreria l'unico strumento per le prove nuove**, con eps dalla tabella. L'alternativa: le scene condivise leggono la tabella **e** ogni script vecchio a eps `0` dichiara `ridotto=True`. Questo **modifica gli script vecchi** *(contro il punto `6`)*, e ognuno andrebbe ricontrollato al bit.

## 6. L'ESITO


**La lettura** *(`doc/DECISIONI_NEL_CODICE.md`, `9180fd38`; file, funzione e riga al blob di oggi)*:
- **(7) eps.** La tabella dice `0.5`, come il deciso. Il nucleo dice `0.5`, ma scritto a mano in `primo_ordine/scena_l2.py` *(`EPS_MONETA`, piu' un secondo `{"eps": 0.5}`)*: **e' una seconda fonte, non letta dalla tabella.** **Le scene condivise di `csv/` scrivono `0`** in `9` punti; quello che conta e' `_energia_del_legame.stato`, che e' la scena di tutto il filone. Il filone del solitone protetto rimette `0.5` a mano;
- **(1) la forma.** **Il nucleo usa `S3`** *(`materia_vuoto.alpha`, `beta`)*. `S1` entra solo in memoria, da `_screening_forme_s3.forma`, ed e' il predefinito di `csv/`;
- **le piatte.** `A` a `K` si costruisce in `_energia_del_legame.stato`, `B` a `Gamma` in `_consolida_B.inviluppo` + `q_migliore` e in `csv/solitone/protetto.py`.

**L'allineamento, fatto dove non c'e' conflitto: nella libreria nuova** *(`92069d24`; il referto `doc/referti_l2/cassetta_solitone_decisioni.txt`, `38/38`)*:
- eps si legge dalla tabella *(`_genera.carica`)*;
- `ridotto=True` da' `0`, con la dichiarazione «CASO RIDOTTO» da stampare nel referto;
- la forma `S1` si legge da `_solitone_vuoto_congelato.FORMA`;
- il costruttore predefinito e' su `B` a `Gamma` e coincide al bit con la partenza di BG-F-0.15; `A` a `K` si ottiene con `quale="AK"` *(DEVE FALLIRE: i due sono diversi)*;
- i `32` test di `55962e54` passano ancora;
- **D6, i tre referti vecchi** *(eps `0`: `livelli_piatti.txt`; eps `0.5`: `massimo_di_B.txt`; `A` a `K`: `coppia_di_B.txt`)*. Nessun `.py` fuori da `csv/solitone/` e' cambiato dopo `9180fd38`, e nessuno script vecchio importa la libreria: **i loro blob sono quelli di prima, quindi ridanno i loro referti.** **Rigirarli da byte identici sarebbe un FALSO-UNO**, e non l'ho fatto.

### ⛔ **FERMO, due punti per Luca** *(il punto `7` del mandato)*:
1. **(1) la forma nel nucleo.**
   - Il problema: `primo_ordine/materia_vuoto.py` *(`alpha` riga `80`, `beta` riga `94`, `pezzi` riga `111`, blob `68ff3ffd`)* da' `S3`, mentre il deciso e' `S1`.
   - La modifica che servirebbe: `S1` come forma del nucleo, **attraverso la tabella `primo_ordine/leggi/leggi.yaml` e il generatore**, non a mano *(`doc/COME_SI_AGGIUNGE_UNA_LEGGE.md`)*, poi la suite.
   - **Non fatto.**
2. **(7) eps nelle scene condivise di `csv/`.** Il mandato chiede due cose che non stanno insieme: «il valore predefinito di ogni scena e' quello della tabella» e «gli script vecchi non si cambiano e ridanno i loro referti». Gli script a eps `0` *(`_livelli_piatti`, `_modo_lento`, `_strada_b_*`, `_dove_va_la_materia`, ...)* prendono `0` da `_energia_del_legame.stato` *(riga `77`)*.
   - **La raccomandazione:** lasciare quelle scene come sono, e usare la libreria come strumento delle prove nuove *(e' gia' fatto)*.
   - **L'alternativa:** le scene leggono la tabella, e ogni script vecchio a eps `0` chiede `ridotto=True`. Questo modifica gli script vecchi, e ognuno andrebbe ricontrollato al bit.

**E una cosa vista e non toccata** *(e' nel nucleo)*: la seconda fonte di eps in `scena_l2.py` dovrebbe leggere la tabella. **Il valore e' giusto: e' pulizia.**

**La MAPPA:** accanto a (7), (1) e alla riga `11` *(le piatte)*, «nel codice: ...», col commit dell'allineamento.

**I mandati in coda sono finiti.** **Il criterio di chiusura dei due punti:** una decisione di Luca registrata nella MAPPA.
