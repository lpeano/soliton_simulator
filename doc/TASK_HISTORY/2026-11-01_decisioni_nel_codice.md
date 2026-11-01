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
