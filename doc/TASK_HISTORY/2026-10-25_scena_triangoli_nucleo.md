# COLMARE LE MANCANZE DEL CENSIMENTO, PARTE A: LA SCENA A TRIANGOLI NEL NUCLEO

> **Il mandato:** di Luca, `2026-10-25`, «colmare le mancanze del censimento», parte `A` *([[DECISIONE-SOLO-TRIANGOLI]], [[N-DIREZIONI-DI-MOTO]], [[CENSIMENTO-DECISIONI]])*.
> ### ⚠ **L'ORDINE, registrato** *([[PRECEDENZA-IN-CODA]])*: ### **questo mandato era in coda dopo il prototipo della curvatura;** ### **ho eseguito PRIMA la parte 0-bis della curvatura** *(arrivata dopo, ma completamento della parte `0`; `0764d566`, `afba052b`)*, ### **poi questo; il mandato «la parte 2 della curvatura sulla carta» viene dopo.**

**LIVELLO:** un cambiamento di una scena *(non di una legge)*; **una parte su tre.**

## 0. LA STELLA POLARE

1. **`A14`:** ### **non si applica** *(la scena non e' una legge: `leggi.yaml` e l'impronta `2e7f795d2a52fbe7` NON cambiano, e si verifica)*.
2. **Il gradino:** ### **`(a)` l'identita' al bit** *(la scena del nucleo contro quella dello strumento, e il quadrato di oggi)*.
3. **Aggiunge un numero o una legge?** ### **No: porta nel nucleo una costruzione gia' usata da tutte le misure dei triangoli.**
4. **Tocca `rho`, `c_s` o il segno?** ### **No.**
5. **Emergente o imposto?** ### **Il reticolo e' imposto** *(come oggi)*: ### **si sposta solo il POSTO dove si costruisce.**

## 1. IL RAGIONAMENTO PRELIMINARE, DAL CODICE

- ### **OGGI NEL NUCLEO:** ### **`primo_ordine/corrente.py`, `toro`** *(il quadrato, «grado `2 d`»)*; ### **`primo_ordine/scena_l2.py`, `scena`** *(il toro quadrato col grumo, `versori_geometrici` sugli assi)*; ### **`primo_ordine/driver.py`, `grafo`** *(la `catena` e l'`anello` della pipeline delle leggi di PROVA)*. ### **Nessuno dei due file e' nella chiusura del nucleo di `P-R1`** *(`csv/_rami_era2.py`: `12` file dalle radici `tick passo motore materia_vuoto saturazione`)*.
- ### **NEGLI STRUMENTI:** ### **`csv/_triangoli.py`: `toro_spostamenti`, `versori`, `scena_toro`, `TRIANGOLI`, `QUADRATO`** *(la trappola dello `zip` che tronca in silenzio)*.
- ### **IL MODULO DEL NUCLEO, e perche':** ### **`toro_spostamenti` in `corrente.py`** *(accanto a `toro`: e' la stessa costruzione del grafo, generale negli spostamenti)*; ### **`GRIGLIE`, `GRIGLIA_DEL_MODELLO = "triangoli"`, `versori` e `scena_toro` in `scena_l2.py`** *(il modulo delle scene)*. ### **Nessun file nuovo** *(la LISTA di `csv/_file_fisica.py` non cambia)*.
- ### ⚠ **I DUE CONTRASTI, riportati e NON risolti da me:**
  1. ### **IL DRIVER:** ### **`driver.py` e' la pipeline delle leggi di PROVA** *(`prova: true`, gli integratori `locale`/`globale`)*, ### **e i suoi collaudi** *(`_collauda_passo`, `_collauda_grafo`, `_collauda_simmetrie`, `_collauda_cs`, `_collauda_determinismo`)* ### **sono costruiti sulla catena di `9` nodi di `config/prova.yaml`** *(i raggi del cono di `_collauda_passo` sono quelli della catena)*: ### **far diventare la sua scena di default i triangoli vuol dire RIDEFINIRE quei collaudi, non portare una scena.** ### **NON lo faccio: e' una domanda per Luca.**
  2. ### **IL NOME DEL QUADRATO:** ### **`scena_l2.scena` costruisce il quadrato e il nome non lo dice;** ### **ma la usano `12` strumenti di `csv/`, che questa parte NON deve cambiare:** ### **la rinomina va insieme al passaggio degli strumenti alla funzione del nucleo** *(un lavoro a se', dopo)*. ### **Qui: la scena nuova `scena_toro(griglia, ...)` vuole il NOME della griglia esplicito, e il quadrato e' solo `"quadrato_di_servizio"`.**

## 2. IL SIGILLO *(`csv/_sigillo_scena_triangoli.py`; i criteri fissati QUI)*

| | la prova | il criterio |
|---|---|---|
| `(a)` | `scena_l2.scena_toro("triangoli", lati, 1.0, 0.1)` contro `csv/_triangoli.scena_toro(TRIANGOLI, lati, 1.0, 0.1)` ai lati `(6,6)`, `(12,12)`, `(48,48)`, `(96,6)` | ### **DEVE: ogni attributo di `Incidenza`, `Motore` e dello stato AL BIT** *(`_triangoli_forza.byte_attr`)*, ### **e il passo di un tick al bit** |
| `(b)` | la matrice del tick: `_triangoli.matrice_tick` con la scena del nucleo *(in memoria)* contro quella dello strumento, lato `48`, `dtau 0.05`; i livelli a `K` contro `8781162c` | ### **DEVE: al bit; i livelli entro `1e-12`** |
| `(c)` | `scena_toro("quadrato_di_servizio", ...)` contro `csv/_triangoli.scena_toro(QUADRATO, ...)`; `corrente.toro(lati)` contro `toro_spostamenti(lati, assi)`; `scena_l2.scena` invariata *(il blob della funzione)* | ### **DEVE: al bit** |
| `(d)` | «la griglia del modello e' ancora il quadrato» | ### **DEVE FALLIRE, PER LA CHIAVE GIUSTA: `GRIGLIA_DEL_MODELLO == "triangoli"` e la scena di quella griglia ha grado `6` a ogni nodo** |
| `(e)` | la trappola dello `zip` | ### **DEVE FALLIRE: `toro_spostamenti((6,6), ((1,0,0),))` ALZA** |
| `(f)` | `leggi.yaml` e l'impronta | ### **DEVE: il blob di `leggi.yaml` e `composizione.IMPRONTA` invariati** |

### **LA SUITE:** `python primo_ordine/collauda.py`, ### **intera, nel commit del cambiamento** *([[SUITE-NEL-COMMIT]])*. ### **Mi FERMO se** ### **il sigillo o la suite falliscono.**

## 3. TODO

1. questo task history, da solo; 2. il cambiamento in `corrente.py` e `scena_l2.py`, il sigillo, la suite, il referto `doc/referti_l2/sigillo_scena_triangoli.txt`, l'indice, il censimento, la relazione — un commit; poi le parti `B` e `C`.

## 4. IL RISULTATO *(dopo `36040a07`)*

### **LA SCENA A TRIANGOLI NEL NUCLEO, FATTA** *(`36040a07`; il sigillo `doc/referti_l2/sigillo_scena_triangoli.{txt,jsonl}`, `csv/_sigillo_scena_triangoli.py` `sha1-BYTE dcea2ea2`)*: ### **`13/13`; la suite `64` su `64`.**
- ### **`primo_ordine/corrente.py`, `toro_spostamenti(lati, spostamenti)`** *(la trappola dello `zip` chiusa: uno spostamento con un numero di componenti diverso ALZA)*; ### **`primo_ordine/scena_l2.py`, `GRIGLIE`, `GRIGLIA_DEL_MODELLO = "triangoli"`, `versori`, `scena_toro(griglia, lati, dtau, x)`** *(il quadrato solo come `"quadrato_di_servizio"`)*.
- ### **IL SIGILLO:** ### **i triangoli del nucleo = `csv/_triangoli.scena_toro` AL BIT a `(6,6)`, `(12,12)`, `(48,48)`, `(96,6)`** *(`11` attributi d'incidenza, `33` di motore, lo stato, un tick)*; ### **la matrice del tick al bit** *(lato `48`, `s 0.05`)*; ### **i livelli a `K` contro `8781162c`: `0.0`;** ### **il quadrato di servizio al bit; `corrente.toro` = `toro_spostamenti` sugli assi al bit; `scena_l2.scena` al bit col padre `6ea2ba20`;** ### **la griglia del modello e' `triangoli`, grado `6` a ogni nodo** *(la DEVE FALLIRE per la chiave)*; ### **la trappola dello `zip` alza; `leggi.yaml` e l'impronta `2e7f795d2a52fbe7` intatti.**
- ### ⚠ **UNA PRECISAZIONE DEL SIGILLO:** ### **gli strumenti di `csv/` cambiano la moneta con la globale `_triangoli.EPS_MONETA`, il nucleo la prende dalla tabella** *(`0.5`)*: ### **nel confronto `(b)` la scena del nucleo riceve la moneta dello strumento.**
- ### **I DUE PUNTI APERTI** *(domande per Luca)*: ### **`(1)` il driver resta sulla catena:** ### **e' la pipeline delle leggi di PROVA, e i suoi collaudi sono costruiti sulla catena di `9` nodi** *(farla diventare a triangoli vuol dire ridefinire quei collaudi)*; ### **`(2)` `scena_l2.scena` resta il quadrato e il nome non lo dice:** ### **la usano `12` strumenti di `csv/`; la rinomina e il loro passaggio alla funzione del nucleo sono un lavoro a se', dopo.**
- ### **LA PARTE C NON SI ESEGUE in questo giro** *(la precisazione di Luca delle `17:38`)*: ### **la decisione provvisoria di Luca delle `16:38`** *(`S1` al posto di `S3`, rivedibile in 3D)* ### **resta APERTA, legata a [[DECISIONE-LINEARE]].**
