# `CLI-1` — I SIGILLI DI `CURA 4` E `CURA 5` PASSANO DAL CLI

*(mandato di Luca, 2026-09-25: «rifai i sigilli di cura 4 e cura 5 PASSANDO DAL CLI (argv del
driver), non impostando il modulo». Task history scritto e committato **PRIMA** del lavoro,
par.5-septies.)*

## ① RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare*

**IL DIFETTO, ed è già misurato:** i due sigilli impostano `S.SEMINA_MATURA = bool(FLAG)` e
`S.MITOSI_2LAM = bool(FLAG)` **direttamente sul modulo importato**. Ed è per questo che
**passavano `7/7` e `8/8` mentre i due flag erano MORTI da riga di comando** — assegnazione in
`esegui_headless`, `global` dichiarato in `_applica_flag`, quindi una **locale silenziosamente
inerte**. Il difetto l'ha trovato **il sigillo del driver**, non i due sigilli della legge.

> ### **UN SIGILLO CHE IMPOSTA IL MODULO A MANO PROVA LA LEGGE, NON IL FLAG.**
> `7/7` e `8/8` **restano validi per la LEGGE**: la fisica misurata è quella. Non dicevano
> **niente** sul percorso che la campagna usa davvero.

**COSA MI ASPETTO:** che i verdetti **non cambino** — la legge è la stessa, l'unica differenza è
**chi accende il flag**. Se un verdetto cambia, **il flag non fa dal CLI ciò che fa dal modulo**, e
quello sarebbe un difetto **più grosso** di quello che sto curando.

**COSA NON SO, e lo dichiaro invece di assumerlo:**
1. se `_applica_flag(a)` sia eseguibile **da solo** nel processo figlio di un sigillo: dal
   2026-09-25 **semina anche il vuoto** (`semina(-1 if SEMINA_LAM else a.nodi)`, `SCENA-1`), quindi
   non è più una funzione di soli flag;
2. **se il DRIVER possa dare il braccio OFF.**

## ⚠ UN RISCONTRO CHE CAMBIA IL MANDATO, trovato PRIMA di scrivere codice

**IL DRIVER NON PUÒ PRODURRE IL BRACCIO OFF DI QUESTE TRE CURE.** `--semina-lam`,
`--semina-matura` e `--mitosi-2lam` sono **cablati incondizionatamente** nella lista delle opzioni
del driver (`csv/_test_fork/_scena_video.py`, il blocco delle obbligatorie), **senza `if`** — a
differenza di `--chi-coop`, `--scala-min` e compagnia, che passano solo `if VAR == "on"`.
**È DI PROPOSITO: è `NUDA = CAMPAGNA`**, cioè esattamente la proprietà che il sigillo del driver
certifica (`15/15`). Una cura obbligatoria **non deve** avere un modo di essere dimenticata.

**CONSEGUENZA OPERATIVA, e non è un aggiramento del mandato:** *«argv del driver»* si realizza
così, e la lettera del mandato resta soddisfatta perché **il percorso attraversato è quello vero**:

```
braccio ON    l'argv che IL DRIVER COSTRUISCE DAVVERO, catturata dal driver stesso
braccio OFF   la STESSA argv, MENO il flag in prova    <- "un comando che dimentica il flag"
                                                          e' l'unico OFF che il CLI ammette,
                                                          perche' i flag sono `store_true`:
                                                          non esiste `--semina-matura=off`
```

**E l'argv NON SI RICOSTRUISCE A MANO:** si **cattura dal driver**, con la stessa tecnica che il
sigillo del driver già usa (esecuzione del testo del driver fino all'ancora `S._applica_flag(a)`).
**Ricostruirla sarebbe UNA SECONDA FORMULA per la stessa cosa**, ed è l'errore che questo repo
inseglie da giorni.

## ② PROGETTAZIONE DEL RAGIONAMENTO — *come intendo arrivarci*

| passo | cosa fa | **cosa DECIDE** |
|---|---|---|
| **1** | un modulo condiviso `csv/_cli_flag.py`: `argv_del_driver(modo)` e `carica_dal_cli(argv)` | che esista **UNA sola** implementazione della cattura dell'argv |
| **2** | il sigillo del driver **usa** quel modulo al posto del proprio codice inline, e si rigira | che la fattorizzazione **non abbia cambiato niente**: deve restare `15/15` |
| **3** | i due sigilli configurano i bracci **con `carica_dal_cli`**, e **non assegnano più il flag** | se il flag, **dal CLI**, produce la stessa fisica |
| **4** | un criterio nuovo in ciascuno: **`CLI`** — «il flag è arrivato al modulo **e nessuno lo ha assegnato a mano**» | che il sigillo non possa più passare su un flag morto |

**IL PRESIDIO CONTRO ME STESSO (`P1-quater`):** ogni sostituzione con la sua asserzione di unicità,
**una alla volta**. E la prova che l'assegnazione a mano **è sparita** si fa **per AST sul file del
sigillo** (`STANDARD 9`), non con un `in` sul testo.

**COSA MI FAREBBE FERMARE, e si scrive ORA, prima dei numeri:**
- se un verdetto di `CURA 4` o `CURA 5` **cambia** passando dal CLI → **STOP**: non è un sigillo da
  aggiustare, è un difetto del percorso, e si committa il `FAIL` così com'è (par.5);
- se il sigillo del driver **non torna `15/15`** dopo la fattorizzazione → **STOP**, si ripristina:
  una fattorizzazione che cambia un esito non è una fattorizzazione;
- se `_applica_flag` **non è eseguibile** nel figlio → **non si forza**: si dichiara il limite e si
  passa dal `_cli()` del simulatore con l'argv catturata, che è comunque il percorso vero del parse.

## ③ TODO DEL NEXT STEP

- [ ] `csv/_cli_flag.py` + fattorizzazione del sigillo del driver, rigirato (`15/15` atteso)
- [ ] `CURA 4` dal CLI, criterio `CLI` incluso, un processo per braccio (`STANDARD 1`)
- [ ] `CURA 5` dal CLI, idem
- [ ] referto + relazione + chiusura di `CLI-1` nella coda, **nello stesso commit** del riscontro
- [ ] **poi** `INERZIA-1` direzione (C), sola lettura: `I3` col taglio OPPOSTO, `coppia`/`inerzia`
      in `k` separatamente, e di quanto si sposta la scala dell'inerzia
