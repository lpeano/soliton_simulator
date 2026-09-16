# PIANO per il MERGE di `fork-su2` in `main` — **PROPOSTA, non eseguita**

> **2026-09-16.** Mandato: §6.3 del TODO — *«Luca ha deciso che `fork-su2` diventa la linea di
> lavoro unica, per non avere due verita'. Non e' stato fatto. Proponi il piano, non eseguire:
> e' una decisione di Luca, e un merge e' difficile da disfare.»*
>
> **Nulla e' stato eseguito.** Tutti i numeri qui sotto vengono da comandi di sola lettura
> (`git merge-base`, `git rev-parse`, `git merge-tree --write-tree`, che **non** scrive nulla nel
> working tree). **Il merge non e' stato fatto e non va fatto senza il tuo via.**

---

## 0. IL FATTO CHE CAMBIA TUTTO IL PIANO

> ### **`main` NON HA MAI TOCCATO `soliton_simulator.py`.**
>
> ```
> blob soliton_simulator.py    merge-base 194a9456    main 194a9456    fork-su2 08784685
> ```
> Il blob di `main` e' **identico a quello della merge-base**. I 20 commit che `main` ha in piu'
> sono **tutti documentazione**: `CLAUDECONNECT.md` (+479 righe), `Checkpoint.md` (+212),
> `CLAUDE.md` (+26), `.github/copilot-instructions.md` (+15), e la cancellazione di **quattro file
> spazzatura** (`3`, `il`, `nel`, `riprende` — frammenti di commenti `.bat` finiti come file).

**Quindi questo non e' un merge di codice: e' un merge di RACCONTO.** Il codice che atterrerebbe
in `main` e' **esattamente `08784685`**, byte per byte, senza nessuna fusione. **Il rischio
tecnico e' molto piu' basso di come e' stato descritto** — ma il rischio **editoriale** e' reale,
ed e' tutto nei due file che confliggono.

---

## 1. LO STATO, misurato

| | |
|---|---|
| merge-base | `1583c7d4` |
| `main` avanti di | **20 commit** (solo documentazione) |
| `fork-su2` avanti di | **191 commit** |
| `dev-spinoriale` | **0 commit avanti, 120 indietro** -> **gia' interamente contenuto in `fork-su2`** |
| worktree | `main` e' **estratto in un worktree separato**: `C:/Users/lpeano/st_main` |

**Conflitti reali, da `git merge-tree` (prova a secco, niente scritto):**

| file | esito |
|---|---|
| `soliton_simulator.py` | **nessun conflitto** — `main` non l'ha toccato |
| `CLAUDE.md` | **CONFLITTO** (entrambi modificati) |
| `CLAUDECONNECT.md` | **CONFLITTO** (entrambi modificati) |
| `.github/copilot-instructions.md` | auto-merge riuscito |
| `Checkpoint.md` | nessun conflitto (`fork-su2` non l'ha toccato: vince la versione di `main`) |
| tutto il resto | nessun conflitto |

---

## 2. I TRE PRESIDI DEL REGISTRO, RI-VERIFICATI DAL DISCO

| presidio (voce **K** di `doc/RAMIFICAZIONI.md`) | stato reale, oggi |
|---|---|
| **rename del file di STATO** — *«un merge cieco cancellerebbe quello di dev-spinoriale»* | **GIA' RISOLTO, e il rischio non era dove si credeva.** `fork-su2` ha `STATO_CLAUDE_fork-su2.md`; **`main` non ha NESSUN file di STATO** (il suo albero ha solo `CLAUDE.md` e `CLAUDECONNECT.md` fra i file di governo). Il file che sparirebbe e' quello di **`dev-spinoriale`**, e sparirebbe **solo se si cancella quel branch** — non per il merge |
| **ri-timbro del gate** | **NON RISOLVIBILE OGGI, ed e' il vero blocco.** `CLAUDE.md` §0 (2026-09-16) spiega perche': in `08784685` c'e' il cablaggio di `--tau-luce` col **sigillo FALLITO**. Portarlo in `main` significa **rendere `main` un branch il cui blob non e' certificato** |
| **l'AVVISO** | **CHIUSO** oggi: `AVVISO_LAVORO_IN_CORSO.md` e' stato svuotato e marcato, con la tabella di dove sta ora ciascuna cosa |

---

## 3. LA RACCOMANDAZIONE — **non adesso, e per una ragione precisa**

> **Il merge e' tecnicamente facile e concettualmente prematuro.**
> `main` e' oggi l'unico branch il cui `soliton_simulator.py` **coincide con un blob certificato**.
> Portarci sopra `08784685` significa **perdere l'ultimo punto fermo** mentre la voce **A** del
> registro — il collo di bottiglia, il sigillo `--tau-luce` che non passa — e' ancora aperta.
> **Finche' A non chiude, «una sola verita'» significherebbe «nessun riferimento certificato».**

**Cosa fare invece, subito e a costo quasi zero:** `main` oggi non e' una *verita' concorrente*,
e' una **cronaca ferma al 2026-09-10**. Il pericolo reale non e' il merge mancante: e' che
**qualcuno legga `main` e creda che sia lo stato del progetto.** Una riga in testa a `CLAUDE.md`
**di `main`** — *«questo branch e' FERMO al 2026-09-10; il lavoro vivo e' su `fork-su2`»* — rimuove
il 90 % del danno con lo 0 % del rischio, e non impegna nessuna decisione.

---

## 4. SE INVECE SI FA — la procedura, nell'ordine

**Precondizione dichiarata:** *«accetto che `main` contenga un blob con un sigillo aperto»*,
oppure **prima si chiude A**. E' la sola decisione che conta; il resto e' meccanica.

1. **Backup nominativo, non il reflog.** `git branch main-pre-merge-2026-09-16 main` **e push del
   tag/branch**. Il reflog e' locale e scade: un branch spinto no.
2. **Attenzione al worktree.** `main` e' estratto in `C:/Users/lpeano/st_main`: il merge va fatto
   **li'**, o quel worktree va rimosso prima. Un `git checkout main` dalla cartella principale
   **fallisce** finche' quel worktree esiste. *(E' l'unica trappola operativa vera di tutto il
   piano.)*
3. **Direzione:** `git checkout main && git merge fork-su2 --no-ff` (mai squash: si perderebbe la
   tracciabilita' «quale pezzo ha fatto cosa», che e' il §5 del progetto).
4. **I due conflitti, risolti a mano e in modo diverso l'uno dall'altro:**
   - **`CLAUDECONNECT.md`** e' una **cronaca**: si **CONCATENANO** i due rami in ordine
     cronologico. Nessuna delle due versioni va scartata — sono due pezzi di storia diversi, non
     due versioni della stessa. *(I §47-55 di `main` e i §44-58 di `fork-su2` vanno controllati
     per **numerazione duplicata**: e' l'unico punto in cui una fusione meccanica farebbe danno.)*
   - **`CLAUDE.md`** sono **regole**: vince **`fork-su2`** come base, e dai 26 righe di `main` si
     riportano **solo** le regole che non esistono gia' — una per una, dichiarando quali.
     **Non si concatena un file di regole.**
5. **Verifica post-merge, prima di spingere:**
   `git hash-object soliton_simulator.py` deve dare **`08784685`**. Se da' altro, la fusione ha
   toccato il codice, e **si annulla**: `main` non aveva nulla da fondere li' dentro.
6. **`dev-spinoriale`:** e' contenuto al 100 % in `fork-su2`. **Non va cancellato**, va marcato
   **ARCHIVIATO** nella sua ultima riga di STATO. Cancellarlo farebbe sparire
   `STATO_CLAUDE_dev-spinoriale.md`, che e' l'unico posto dove vive il racconto di quel branch.
7. **Dopo il merge, `fork-su2` resta il branch di lavoro** (e `main` torna a essere il punto di
   pubblicazione), oppure si lavora su `main`: **va deciso, non lasciato implicito.** Due branch
   vivi senza una regola su chi comanda sono **di nuovo due verita'**, che e' il problema da cui
   si partiva.

---

## 5. COSA NON HO FATTO, esplicitamente

Nessun `merge`, nessun `checkout`, nessun `branch`, nessun `push`, nessuna cancellazione.
`git merge-tree --write-tree` scrive **solo oggetti nel database git**, non tocca il working tree
ne' sposta alcun riferimento: e' il modo di **vedere i conflitti senza produrli**.
