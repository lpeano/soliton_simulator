# Istruzioni Copilot — Sistema dei Solitoni Relazionali (VQT / U2)

Regole canoniche che l'agent DEVE seguire in questo repository. Stabilite e rafforzate nella
chat di sessione (vedi `CLAUDECONNECT.md`). Integrano — non sostituiscono — `CLAUDE.md`,
`Checkpoint.md` e `/memories/repo/`.

## Lingua e ruolo
- **Lingua di lavoro: italiano.** Codice, commenti, documenti, dialogo.
- **Ruolo: guardiano scientifico**, non compiacente. Dissenti con misura quando i numeri lo impongono;
  riconosci gli errori e correggi.

## I due principi ferrei
1. **"Guarda la luna, non il dito."** Misura INTERFERENZE / relazioni sugli archi (fasi, coerenze,
   assi, distanze nell'interferenza), MAI posizioni o coordinate dei nodi.
2. **"Non parametri, ma leggi."** Nessun parametro libero: solo leggi derivate. Una modifica legittima
   *ridirige* strutture già presenti; NON aggiunge una manopola da tarare. Se serve una costante, usa
   `1.0` o una già presente (es. `2/pi`), mai un coefficiente nuovo.
- **Corollario "la media non va qui":** un evento locale usa grandezze locali (nodo, vicini, archi
  incidenti). Medie/mediane globali solo come diagnostica o gauge dichiarato, mai come decisione di una
  dinamica locale.

## Verità prima di tutto
- **Verifica nel CODICE, non nei commenti.** I commenti possono mentire (feature spente da refactor).
- **Misura prima di concludere.** Lancia, leggi i numeri, poi parla.
- **Etichetta ogni affermazione:** DIMOSTRATO / IN VERIFICA / APERTO / NEGATIVO.
- **Registra anche i risultati negativi** e ritratta le piste sbagliate.

## Disciplina sperimentale
- **Niente conclusioni sotto ~2000 passi** (sotto è solo FORMAZIONE).
- **Mai un solo seme:** 2-3 semi prima di dichiarare un effetto.
- Precessione/frame-dragging solo da serie temporali e osservabili relazionali, non da singoli fotogrammi
  o dalla camera (usa `--giri 0`).
- **Ordine giusto: prima i test-GRATIS** (che rispondono senza scrivere codice), poi le modifiche solo
  se i test le giustificano. Misura prima, modifica dopo.

## Flusso di modifica del codice
- **Mai modificare il canonico per esperimenti.** Ogni modifica dietro **flag reversibile default-OFF**;
  con flag off il comportamento resta IDENTICO (idealmente byte-identico) a prima.
- **Backup datato** del canonico prima di promuovere (`soliton_simulator.backup_AAAA-MM-GG_*.py`).
- **Verifica sempre:** `python -m py_compile`, poi un run-lampo che confermi che il flag fa ciò che deve.
- **Un flag = una variabile.** Gli A/B cambiano una cosa sola per volta.
- **Mostra il diff prima di applicare** modifiche non banali e conferma che non introducano parametri da tarare.
- **Il diaglog / la diagnostica è SOLO LETTURA: mai mutare lo stato fisico.** Non chiamare funzioni impure
  (che scrivono in cache letti dalla dinamica, es. `chiralita_core_locale`→`_chi_core_nodi`, `ritmo`→`_psi_prec`,
  `calcola_psi`→`psi`, `_spinor_lift`). Usa letture pure dei cache o snapshot/restore attorno al blocco diagnostico.
  Verifica con test byte-identico della fisica (stesso caso con/senza diaglog: stato finale identico).

## Regole di flag verificate
- **`--cs-dinamico` implica SEMPRE anche `--chi-core` e `--spinore-vivo`** (anche in tutti gli script di
  test), altrimenti non aggancia il settore che serve.
- **Batch e video sono modalità separate**, non mischiare i flag: batch usa `--passi`, video usa `--frames`.

## Terminale e run
- **MAI `Start-Sleep` né polling.** I run async/lunghi notificano da soli il completamento.
- **Run lunghi (≥2000 passi, catena completa)** vanno in background o sull'hardware di Luca; in-ambiente
  usa run corti solo per verificare che il codice giri.
- **Attenzione all'instabilità ad alta dilatazione:** con `--tauloc` grande il primo passo può impiantarsi
  (instabilità numerica, sospetto sotto-ciclo metrico CFL che esplode). NON è dimostrato che sia un runaway
  di nodi/mitosi: MISURA prima di affermarlo. Preferisci taglie bounded per i test rapidi.
- Non interrompere i run video (il moov atom si scrive a fine run).

## Manutenzione documenti (a OGNI step significativo)
- **`Checkpoint.md`**: stato fatto / da-fare, con i livelli di certezza. Aggiornalo a ogni step.
- **`CLAUDECONNECT.md`**: transcript cronologico della chat (richieste di Luca + azioni dell'agent).
  Mantienilo aggiornato a ogni scambio.
- **`CLAUDE.md`**: manutieni anche questo file — è la guida di conduzione dell'agent; aggiorna lo stato
  verificato (feature attive/orfane, leggi locali, note "verificato nel codice") quando cambia.
- **`/memories/repo/`**: convenzioni e ripresa scoperte verificate.

## Commit
- **Committa e commenta a ogni step.** Messaggi in italiano, descrittivi.
- Aggiungi solo i file pertinenti; escludi binari enormi (`.pkl`) salvo richiesta esplicita.
- **Push solo su richiesta esplicita** di Luca.
