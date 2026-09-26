# 🔎 **I SEI LETTORI E L'INDICE — che cosa aprono, e QUALE CAMPO MANCA**

*(**Generata** da `csv/_analisi_lettori_indice.py`. Punto 5 del mandato del 2026-09-26.)*

> ## ⛔ **NESSUNO DEI SEI SI CONVERTE COM'E', e i motivi sono di TRE tipi**
> **due CONSUMATORI** hanno bisogno di **un campo che l'indice non ha**; **due GENERATORI**
> leggono **il CODICE** e aprono il registro **per SCRIVERCI**; **uno misura la PROSA** dei
> registri *(convertirlo distruggerebbe cio' che misura)* e **uno non tocca i tre registri**.

**Perche' lo dico invece di convertire:** Luca ha scritto *«se uno ha bisogno di un campo che
l'indice non ha, **dimmelo** invece di rileggere il Markdown»*. **Vale per tutti e sei.**

## LA MISURA — dal sorgente, non a memoria

| strumento | righe | registri che NOMINA | legge il CODICE? | scrive? | classe |
|---|--:|---|:--:|:--:|---|
| `_punto_della_situazione.py` | 162 | STATO_RUN | — | — | **CONSUMATORE** |
| `_seal_fork/_triage_difetti.py` | 302 | PATTERN_DI_PROVA, RAMIFICAZIONI, STATO_RUN | — | SI | **CONSUMATORE** |
| `_cure_verificate.py` | 352 | STATO_RUN | SI | SI | **GENERATORE** |
| `_quadro_unico.py` | 313 | STATO_RUN | SI | SI | **GENERATORE** |
| `_blob_nelle_voci.py` | 87 | COMPONENTI_PROMOSSE, RAMIFICAZIONI | — | — | **MISURA DELLA PROSA** |
| `_inventario_passo.py` | 269 | INVENTARIO_passo_incompleto | — | SI | **FUORI PERIMETRO** |

## VOCE PER VOCE — che cosa estrae, e che campo servirebbe

### `csv/_punto_della_situazione.py` — **CONSUMATORE**

- **che cosa estrae oggi:** estrae da ogni riga della coda `id`, `cosa` e **il MARCATORE DI AVANZAMENTO** *(`▶` IN CORSO, `⏸` IN CODA, `✅` FATTO, `❌` BLOCCATO, `⚠` CON RISERVA)*, e raggruppa per marcatore
- **campo che manca all'indice:** **`avanzamento`** — l'indice ha `stato` *(aperto/chiuso/…)*, che **non distingue IN CORSO da IN CODA**: e' proprio la distinzione che questo documento serve a mostrare

### `csv/_seal_fork/_triage_difetti.py` — **CONSUMATORE**

- **che cosa estrae oggi:** prende **le voci `CODICE`** di `RAMIFICAZIONI` e per ciascuna un **ESITO**, e asserisce che nessuna resti senza esito
- **campo che manca all'indice:** **`classe`** *(`CODICE`/`MISURA`/`PROVA`)* **e `esito`** — l'indice non ha ne' l'una ne' l'altro: sono la CHIAVE del triage

### `csv/_cure_verificate.py` — **GENERATORE**

- **che cosa estrae oggi:** legge **`soliton_simulator.py`** *(i flag)* e **SCRIVE** la sezione `CURE VERIFICATE` dentro `STATO_RUN`: apre il registro **per scriverci**, non per trovare difetti
- **campo che manca all'indice:** **`flag`, `default`, `sigillo`, `prova`, `esito`** — cinque campi che l'indice non ha; e comunque la sua FONTE e' il codice, non il registro

### `csv/_quadro_unico.py` — **GENERATORE**

- **che cosa estrae oggi:** legge **`soliton_simulator.py`** e il **driver**, e **SCRIVE** i tre elenchi nel `PUNTO DI RIPRESA` di `STATO_RUN`
- **campo che manca all'indice:** **`in_codice`, `acceso_nei_run`, `default`** — e come sopra: la fonte e' il codice

### `csv/_blob_nelle_voci.py` — **MISURA DELLA PROSA**

- **che cosa estrae oggi:** conta **quante voci dei registri portano il BLOB** del codice che le ha prodotte: il suo oggetto **E' la prosa dei registri**
- **campo che manca all'indice:** **nessuno**: convertirlo all'indice **distruggerebbe cio' che misura**. Se leggesse l'indice misurerebbe l'indice, non i registri

### `csv/_inventario_passo.py` — **FUORI PERIMETRO**

- **che cosa estrae oggi:** legge **gli script di `csv/`** e scrive `doc/INVENTARIO_passo_incompleto.md`: **non apre nessuno dei tre registri per trovare difetti**
- **campo che manca all'indice:** **nessuno**: non e' un consumatore dei registri

---

## 📌 **LA PROPOSTA MINIMA: TRE CAMPI, e due strumenti si convertono**

| campo | a chi serve | da dove si ricava |
|---|---|---|
| **`avanzamento`** *(`IN CORSO`/`IN CODA`/`FATTO`/`BLOCCATO`/`CON RISERVA`)* | `_punto_della_situazione` | dal **primo marcatore della cella**, che e' esattamente cio' che quello strumento fa oggi — e porta con se' il suo difetto gia' curato: *conta il primo nel TESTO, non il primo di una lista* |
| **`classe`** *(`CODICE`/`MISURA`/`PROVA`)* | `_triage_difetti` | dal tag `[EPOCA n · CLASSE]` delle righe di `RAMIFICAZIONI`, che l'indice oggi **butta via** *(lo togliamo dal titolo per renderlo leggibile)* |
| **`esito`** | `_triage_difetti` | **NON si ricava**: e' il triage stesso a produrlo. Servirebbe che il triage **scrivesse** nell'indice, non che lo leggesse — **e questo cambia il verso del flusso**, quindi lo decide Luca |

**Con `avanzamento` e `classe`, DUE strumenti su sei si convertono** *(`_punto_della_situazione`
e la META' in lettura di `_triage_difetti`)*. **Gli altri quattro NON sono consumatori di
difetti**, e la condizione di fine del mandato — *«nessun consumatore apre piu' i registri per
TROVARE DIFETTI»* — **per loro e' gia' vera oggi**, ma per una ragione diversa da quella
attesa: **non li aprono per quello.**

## ⚠ COSA QUESTA ANALISI *NON* DICE

- **non dice che i quattro fuori perimetro siano a posto**: dice che **non cercano difetti**.
  `_cure_verificate` e `_quadro_unico` **scrivono** dentro `STATO_RUN`, e questo resta un
  accoppiamento: se un giorno l'indice diventasse la fonte anche delle CURE, andrebbero rifatti.
- **la colonna «scrive?» e' un'euristica sul sorgente** *(cerca una `open(..., "w")` vicino a un
  nome di registro)*: dice che lo strumento scrive **qualcosa**, non necessariamente nel registro.
- **non ho convertito niente**: `LETTORI-INDICE` resta **APERTA**. Chiuderla adesso vorrebbe dire
  dichiarare finito un lavoro che dipende da una decisione di Luca sui tre campi.
