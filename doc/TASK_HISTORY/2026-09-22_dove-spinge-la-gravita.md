# G2 — DOVE SPINGE LA GRAVITA' (§2 del mandato del 2026-09-22)

> **Committato PRIMA del lavoro** (par.5-septies). Se le sezioni ① e ② si rivelano sbagliate
> **non si riscrivono: si ANNOTANO** con cio' che le ha smentite.

**Precede:** `G1` (commit `3c03223`, `Z103`) — misurato che **il pozzo gravitazionale usa il
disegno**, e che la differenza **cresce** e **dipende dal centro**.
**Segue:** `G3` (spegnimento di `GRAV_BIFASE`), `G4` (`MEM_MOTO`), `CHK3`.

---

## ① RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare*

**Cosa so gia', misurato e committato:**
- `S09_spinta_med` ha saldo **verso il basso**: `-1.268e+05` su 120 passi (`Z102`);
- `S10_grav_med` **non ha mai girato**: e' il ramo `else`, inerte in questa configurazione;
- il **freno** `_smorza` aggiunge `+3.205e+05` e **ribalta il segno** del saldo complessivo;
- il **pozzo** da cui nasce `grav` e' calcolato sul **DISEGNO** (`G1`), e il disegno **impone un
  centro** (`r` da `-0.088` a `+0.181` su 5 snapshot su 5).

**Cosa mi aspetto, e puo' benissimo essere smentito:**
- poiche' il pozzo dipende dal centro del disegno, **mi aspetto che la spinta NON sia uniforme fra
  regioni**, e che sia piu' forte dove il disegno e' piu' denso — cioe' **nelle masse**;
- mi aspetto che le **salite e le discese siano entrambe grandi** e quasi si cancellino, perche' il
  saldo di `S09` (`-1.27e+05`) e' piccolo davanti a cio' che il freno ci mette (`+3.20e+05`);
- **non so** se i 20 archi piu' spinti siano pochi archi patologici o la coda di una distribuzione
  liscia. **E' la differenza fra un difetto locale e una legge sbagliata ovunque**, e non la deduco.

**Cosa NON so, ed e' il punto della misura:** `Z102` ha dato **un solo numero** per `S09`, il saldo
globale. **Un saldo globale non dice DOVE.** Due sistemi con lo stesso saldo — uno che spinge in
modo uniforme, uno che spinge tutto su mille archi — sono **due fisiche diverse**.

> **⚠ ANNOTAZIONE DEL 2026-09-22, A MISURA FATTA. `par.5-septies`: il ragionamento
> preliminare NON si riscrive quando si rivela sbagliato, SI ANNOTA.**
> **① «mi aspetto che sia piu' forte nelle masse» — SBAGLIATO.** Il saldo vive
> sul **CONFINE vuoto-massa** *(`-1.4150` per arco contro `+0.0304` di `massa-massa`)*, `Z105`.
> **② «salite e discese entrambe grandi che quasi si cancellano» — GIUSTO, ma
> SOLO FUORI DAL CONFINE:** si elidono al **98 %** nel vuoto e nelle masse, e **NON si elidono sul
> confine** *(`|saldo|/tot = 0.885`)*.
> **③ «non so se i 20 archi piu' spinti siano pochi archi patologici o la coda di una
> distribuzione liscia» — LA RISPOSTA E' NESSUNA DELLE DUE: sono un PLATEAU DI
> SATURAZIONE.** Quaranta archi con **un solo numero**, `±1.663184`, e concentrazione
> `0.01925` contro un nullo di `0.01`. **E i 20 col `|saldo|` maggiore sono `20 su 20` NEL VUOTO,
> non sul confine: anche questa aspettativa e' caduta.**
> **④ L'ASSUNZIONE CHE NON AVEVO NEMMENO SCRITTO COME TALE** — che la mitosi APPENDESSE
> archi senza riordinare — **era falsa in 61 passi su 120**, e l'ha presa la guardia.

---

## ② PROGETTAZIONE DEL RAGIONAMENTO — *come intendo arrivarci*

**Lo strumento: `csv/_test_fork/_dove_spinge_la_gravita.py`.**
**SOLA LETTURA sulla fisica:** si **sostituisce** `_traccia_d0` con una funzione pure-read allo
stesso punto di chiamata, esattamente come `_somma_per_scrittore_d0.py`. **Il simulatore non si
tocca**, e nemmeno il driver.

**I tre numeri che produce:**
1. **per REGIONE** — `vuoto-vuoto`, `massa-massa`, `nato-nato`, `CONFINE vuoto-massa`,
   `CONFINE con nato` — **salite e discese separate**, il saldo, e **il saldo PER ARCO** (senza il
   quale una regione con piu' archi sembra sempre la piu' spinta: e' un errore di popolazione,
   `A3`);
2. **i 20 archi piu' spinti**, con i **nodi** `i`/`j`, la loro regione, `d`, `d0` e `L/d`;
3. **la concentrazione**: che frazione del totale positivo sta nell'`1 %` di archi piu' spinti.
   **Il valore sotto ipotesi nulla e' `0.01`** (spinta uniforme), quindi il confronto e' con `0.01`,
   **non con una soglia scelta**.

**COSA DECIDE CIASCUN PASSO, e le letture si fissano QUI, prima dei numeri:**

| se si misura | si legge |
|---|---|
| saldo **per arco** simile in tutte le regioni | la spinta e' **globale**: non segue la massa, e **non si comporta come gravita'** |
| saldo per arco **maggiore in `massa-massa`/`CONFINE`** | la spinta **segue la massa**: il pozzo fa il suo mestiere, il difetto di `G1` e' di ampiezza, non di direzione |
| saldo per arco **maggiore in `vuoto-vuoto`** | **la spinta e' piu' forte dove non c'e' niente**: e' un difetto, e va a `CHK3` |
| frazione nell'`1 %` piu' spinto **vicino a `0.01`** | distribuzione **liscia**: nessun arco patologico |
| frazione nell'`1 %` **molto sopra `0.01`** | **pochi archi portano quasi tutto**: difetto locale, e i 20 archi dicono quali |

**COSA MI FAREBBE FERMARE:**
- **se la prefissazione degli archi non regge.** Il conteggio **per arco cumulato** assume che la
  mitosi **APPENDA** archi senza riordinare i precedenti. **Non lo suppongo: lo VERIFICO a ogni
  passo** confrontando il prefisso di `(i, j)` con quello del passo prima. **Se anche una sola
  volta non regge, la tabella dei 20 archi NON si stampa** e lo strumento lo dichiara: un
  cumulato su indici riordinati sarebbe **numeri veri sommati sull'arco sbagliato**;
- se `S09` non gira (come `S10` in `Z102`): allora **la misura non e' verificabile qui**, e si dice.

**⚠ `P1-sexies` — IL CRITERIO SI COLLAUDA PRIMA, SU CASI A RISPOSTA NOTA.** Tre casi, e **il piu'
importante e' quello che DEVE fallire**:
- **A** — aggregazione per regione su `dx` costruito a mano, con somme per regione **note**: deve
  ritrovarle esatte;
- **B** — concentrazione su una distribuzione **uniforme**: deve dare `~0.01`, cioe' il nullo;
- **C** — **il caso che DEVE fallire**: una permutazione degli archi. **La guardia del prefisso
  DEVE accorgersene.** Se non se ne accorge, lo strumento **si ferma e non misura**.

---

## ③ TODO DEL NEXT STEP

- [x] task history committato **prima** del lavoro
- [x] `csv/_test_fork/_dove_spinge_la_gravita.py` + voce di inventario, **committato prima di
      girarlo** (par.5)
- [x] rigiocata 120 passi, `TRACCIA_D0`, configurazione della validazione *(tre giri: `Z105` per regione, poi l'accumulatore per chiave, poi le colonne complete)*
- [x] esito -> **`Z105`** *(per regione)* e **`Z106`** *(il plateau)*, `RELAZIONE_PER_CLAUDE.md`, commit e push
- [ ] **poi `G3`**: `GRAV_BIFASE = False` impostato **dalla rigiocata sul modulo**, 600 passi,
      invarianti accesi, **stessi criteri assoluti** della validazione
