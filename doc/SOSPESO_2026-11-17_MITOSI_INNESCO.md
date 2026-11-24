# SOSPESO IL `2026-11-17` *(Luca `23:07`)*: LA MITOSI E IL SUO INNESCO -- **IL DOCUMENTO DA CUI SI RIPRENDE**

> **Decisione di Luca (`23:07`): si SOSPENDE tutto.** Nessuna corsa nuova, nessun codice nuovo *(nemmeno B4 sul ramo `mitosi`)*. **La ripresa parte da QUESTO documento.** [[MITOSI-QUANTO-OLONOMIA]]
> **Ogni numero qui e' RICOPIATO dal repo, col riferimento; niente e' calcolato di nuovo** *(Q-A1)*. **La carta:** `doc/MITOSI_era2_carta.md`, sez. `13`-`15`.

## 0. LO STATO DEL DISCO AL MOMENTO DELLA SOSPENSIONE

- **Il registro** *(`doc/REGISTRO_CORSE.md`)*: **NESSUNA corsa aperta** -- ogni voce `APERTO` ha la sua chiusura *(controllato voce per voce alle `23:07`; C1, C2 e i `12` segmenti della torsione chiusi `FINITO`)*; **nessun processo python in esecuzione.** **Niente da fermare, niente da riprendere a meta'.**
- **Il ramo `primo-ordine`:** l'ultimo lavoro e' `52caa06a` *(la sez. 15 e la stima della corsa gemella)*, piu' il commit di questa sospensione.
- **Il ramo `mitosi`** *(worktree `C:/Users/lpeano/wt_mitosi`)*: **resta com'e'**, ultimo commit `42717d33` *(il referto di B3, `doc/referti_l2/mitosi_B3_u1.txt`, `14/14`)*; prima `c2cb792b` *(B3, la U(1) sul grafo generico)* e `f7f3e43d` *(B2, `Motore.cresci`)*. **Nulla si riunisce a `primo-ordine`** *(R-NAVI)*.
- **I dati di C2** *(il braccio senza mitosi)*: gli stati salvati in `E:/soliton_simulator/controllo/C2/` *(fino a `stato_03000.npz`)*; la serie di Theta tick per tick in `E:/soliton_simulator/controllo/torsione/` *(`C2_<k0>.npz`, `candidati.npz`)*. **La ripresa dagli stati e' AL BIT** *(K3, `doc/referti_l2/torsione_tempo_proprio_K3.txt`; i `12` segmenti, `doc/referti_l2/torsione_segmenti.txt`)*.

## a) DOVE SIAMO

- **L'innesco e' (a), IL CONTATORE DEL LAPSE** *(decisione di Luca, `21:00`; carta sez. `15.1`)*: `Theta_a = pi * somma sui tick (dtau_nodo_i - dtau_nodo_j)`, una memoria per arco; l'arco si divide a `|Theta_a| >= 2 pi`. **Dichiarato come contatore della deriva fra orologi vicini, NON come olonomia** *(14.6-bis: su un ciclo la somma e' zero, e' un gradiente)*.
- **LA DERIVA NETTA C'E'** *(sez. `15.2`, `doc/referti_l2/torsione_segmenti.txt`)*: il criterio di Luca passa -- sull'arco del massimo *(r `18.12`)* la deriva netta in `3000` tick e' `0.675` rad contro un'oscillazione massima di `0.0082`; **`20` archi su `20`**. Il ritmo netto massimo `2.256e-04` rad per tick a r `18.08`; **il primo `2 pi` al tick `2.79e+04`**.
- **MA SCATTA SOLO NEL GUSCIO DELLA MATERIA:** entro `1e5` tick `2929` archi, **tutti fra `10.0` e `22.3` nodi**; entro `1e6` tick `5346`, fra `2.3` e `23.45` -- **tutti dentro il confine `23.81`** *(15.2)*.
- **E S1 LI VIETA TUTTI: `0` su `2929`** *(sez. `15.3`, `doc/referti_l2/innesco_S1.txt`)*: nel guscio il termine della materia della nascita FA e' praticamente tutto `|DH|` *(materia/`|DH|` fra `0.93` e `1.37`, mediana `1.003`)*, e **`DH` e' fortemente NEGATIVO** *(la mediana da `-1.2e+03` a `10`-`12` nodi a `-26` a `22`-`24`)*. *(Lo stato di C2 a `k 3000`, non quello allo scatto: dichiarato.)*
- **FUORI DAL CONFINE E' IMPRATICABILE** *(sez. `15.4`, `doc/referti_l2/innesco_stima.txt`)*: `10` nascite oltre `23.81` al tick `7.47e+06` = `7652` ore al tick misurato di C2 *(`3.690` s)*, **`0.9` anni** -- e li' con FA la materia e' ancora il `6%`; oltre `29.81` *(dove S1 passa)* al tick `6.2e+08`, **`73` anni**.

## b) LA SCELTA APERTA PER LUCA *(sez. `15.6`)*

- **(i)** togliere S1 o cambiarne la natura: **le nascite nel guscio, dentro la materia**;
- **(ii)** tenere S1 e accettare che la mitosi non scatti sul mattone di `L 186`: **nessun test sul mattone**;
- **(iii)** **un altro innesco** per il vuoto fuori dal confine.

### **NESSUNA DI QUESTE E' SCELTA.**

## c) LA PROPOSTA DEL GUARDIANO *(`23:00`)* -- ### **SUA, NON DECISA**

- **La strada (i), CON UNA CONDIZIONE.** La nascita nel guscio con D7 su `psi` rilascia fino a circa `-1.2e3` *(15.3)*, e **la compensazione locale di A3 non puo' assorbirlo**: il vuoto di `S` vale decine -- ### **una STIMA del guardiano, NON misurata.**
- **Quindi:** si sceglie **la regola della MATERIA sulle estremita' nuove** perche' la nascita sia **A ENERGIA NULLA**: **una famiglia a un parametro fra «`psi` non toccata» e D7, la radice di `DH = 0`**; **locale, norma conservata, deterministica.** **Da MISURARE prima sugli archi del guscio, col suo caso noto.**
- **Gli effetti da attendere** *(del guardiano)*: **il mattone si diluisce** *(piu' nodi sotto la stessa materia: il lapse cambia)*; **il primo quanto a circa `2.8e4` tick** *(15.2: `2.79e+04`)*, **circa `29` ore su `L 186`** *(la stima del guardiano, col tick misurato di C2 `3.690` s di `innesco_stima.txt`)*; **due corse di circa `3.5e4` tick** *(con la mitosi, e C2 estesa)* **in parallelo, circa `36` ore**, con la ripresa al bit sui riavvii; ### **FERMO prima di lanciarle.**
- ### ⚠ **Il guardiano nota** *(Claude Code, accanto)*: **«a energia nulla» e' un vincolo che SCEGLIE il parametro** *(la radice), **non una manopola** -- ma va verificato che la radice **esista e sia UNICA** su ogni arco del guscio *(la famiglia va da `DH` negativo con D7 a «`psi` non toccata», il cui `DH` non e' misurato nel guscio)*: **se non esiste, FERMO.**

## d) LE DECISIONI IN VIGORE

| | che cosa | dove |
|---|---|---|
| **D-M1** | il ramo `mitosi`, lo scongelamento del nucleo SOLO li'; la riunione solo con un mandato di Luca | carta sez. `9` |
| **D-M2** | la divisione d'arco piu' il flip *(la dislocazione)*, con la scelta del flip SIMMETRICA ALLO SPECCHIO | carta sez. `9`, `10.3` |
| **D-M3** | **FA con la compensazione locale di A3** *(H totale conservata alla nascita)* | carta sez. `15.1` |
| **D-M4** | UNA nascita per tick, per cominciare | carta sez. `9` |
| **D-R4** | **la crescita IRREVERSIBILE** *(nessuna fusione)*: **la freccia del tempo DICHIARATA**, accanto a CPT | carta sez. `13` *(intestazione)*, `13.5` |
| **D-R5** | il nucleo sul ramo `mitosi` si allenta SOLO per l'infrastruttura che non dipende dalla regola di `phi_h` | carta sez. `13` *(intestazione)* |
| **D-R1, D-R2, D-R3** | ### **SOSPESE** *(Luca `18:04`)* | carta sez. `13.7` |
| il bordo | **tolto** | carta sez. `15.1` |
| C2 | **il braccio SENZA mitosi** della prova | carta sez. `15.1` |
| il mattone | **su `L 186`** | carta sez. `15.1` |
| **S1** | la materia della nascita FA sotto l'`1%` del modulo di `DH` -- **l'`1%` E' UN NUMERO** *(`A1`)*: scelta del guardiano | carta sez. `15.1` |
| **S2** | gli archi nuovi da `Theta = 0`, l'arco diviso consumato | carta sez. `15.1` |
| **S3** | la compensazione deterministica e simmetrica *(o una regola sulla fase, o FERMO)* | carta sez. `15.1` |
| **S4** | P7 riscritta: la FORMA del profilo della curvatura di Regge contro `N(rho)` | carta sez. `15.1` |

## e) LE COSE APERTE

- **B4 e la memoria per arco sul ramo `mitosi`:** **non partiti**; **possono partire PER PRIMI alla ripresa**: non dipendono dalla scelta (b) *(carta sez. `15.6`)*.
- **P-L5** *(la compensazione deterministica e simmetrica)*: **non misurata** *(carta sez. `15.5`)*.
- **Il cancello P6 da riscrivere a parita' di `E` e di `cs`:** una nascita cambia `E` e `cs` ovunque *(carta sez. `13.1`, P-M2)*.
- **`A` cresce come GRADIENTE** *(`max |A| = 33.0` in `3000` tick contro una circolazione `6.5e-05`: carta sez. `14.7`)*: **sulle corse lunghe servira' una ritaratura di gauge periodica** *(la circolazione non cambia)*.
- **Il campo NON compatto:** il quanto `2 pi` della placchetta non ha senso pieno; **(d) esclusa nel campo di oggi** *(carta sez. `14.7`-`14.8`)*.
- **L'entropia: da definire** *(carta sez. `13.5`)*.
- **I triangoli** *(in fase, e tre sfasate sul vuoto)* **dopo il mattone, col confine locale** *(il mandato di Luca `23:07`)*.
- *(Accodati dal `16:38`: i passi B dopo B4 sul ramo, e la domanda sull'area e `l/l*` dei triangoli nuovi, la stella di Hodge: carta sez. `14.6`.)*

## f) GLI ERRORI DEL GUARDIANO DI OGGI POMERIGGIO *(elencati nel mandato di Luca `23:07`)*

- **n.186:** i post Itaca dati per non pubblicati.
- **n.187:** il danno del rientro detto non misurato *(TB3, TBS)*.
- **n.188:** la decisione dell'`11/10` sul quanto non richiamata *(carta sez. `14.1`)*.
- **n.189:** la stazionarieta' del lapse data per buona: il trapezio *(carta sez. `14.3`; `doc/TASK_HISTORY/2026-11-17_torsione_tempo_proprio.md`)*.
- **n.190:** K2 mal posta *(carta sez. `14.6-bis`)*.

## g) LA RIPRESA

1. **IL PRIMO PASSO: la risposta di Luca su (b).**
2. **Poi** *(se la scelta e' (i))*: **il mandato della regola della materia a energia nulla** *(la proposta c)*, misurata prima sugli archi del guscio col suo caso noto.
3. **Indipendenti dalla scelta, se Luca li vuole:** B4 e la memoria per arco sul ramo `mitosi`.
4. **Prima di toccare qualunque cosa:** `python csv/indice.py valida` e il registro *(le corse aperte)*, come da `CLAUDE.md` sez. `13`.
