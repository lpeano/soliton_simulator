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

## Misure covarianti (IL SISTEMA SI ESTENDE)
Il sistema si estende sempre: N cresce (da ~400 a ~20000 nodi) e le `d0` si stirano. Ogni misura metrica va
gestita **in modo covariante**, altrimenti misuri l'espansione, non la fisica (il dito, non la luna).
- **MAI confrontare a passo-coordinata fisso.** Confronta a **N appaiato** e/o **tempo proprio cumulativo
  appaiato** (`tau_cum = Σ tau_mean·DT`), non allo stesso `step`.
- **MAI usare medie globali che diluiscono con N** (es. `spin_cluster_modulo = |media Bloch|/N` cala come
  ~1/√N per pura aggiunta di nodi): usa osservabili **intensivi/adimensionali**, **per-dominio** (nucleo/guscio
  separati), o **normalizzati per la scala comovente** (`d_mean`, mediana `d0`).
- **I trend nel tempo** (1ª vs 2ª metà) vanno letti a **scala/popolazione appaiata**, non a passo fisso.
- Osservabili già covarianti da preferire: rapporti relazionali (coer, cosphi, correlazioni istantanee),
  invarianti topologici (`guscio_circ`, carica), quantità per-arco.
- Regola pratica: prima di dichiarare un effetto, **rifai la misura a N appaiato**; se sparisce, era espansione.


## Flusso di modifica del codice
- **Mai modificare il canonico per esperimenti.** Ogni modifica dietro **flag reversibile default-OFF**;
  con flag off il comportamento resta IDENTICO (idealmente byte-identico) a prima.
- **Backup datato** del canonico prima di promuovere (`soliton_simulator.backup_AAAA-MM-GG_*.py`).
- **Verifica sempre:** `python -m py_compile`, poi un run-lampo che confermi che il flag fa ciò che deve.
- **Un flag = una variabile.** Gli A/B cambiano una cosa sola per volta.
- **Mostra il diff prima di applicare** modifiche non banali e conferma che non introducano parametri da tarare.
- **ATTENZIONE MANIACALE — il diaglog, il trace e la condensazione sono SOLO-LETTURA: mai mutare la fisica,
  mai consumare `net.rng`.** Ogni funzione diagnostica impura (scrive cache letti dalla dinamica, es.
  `chiralita_core_locale`→`_chi_core_nodi`, `ritmo`→`_psi_prec`, `calcola_psi`→`psi`/`psi_spin`/`rho_spin`/
  `_psi_spin_prec`, `_spinor_lift`) va neutralizzata con snapshot/restore. Il SET COMPLETO da ripristinare
  attorno a diaglog E condensazione: `psi,_psi_prec,_spinor_lift,_psi_spinor,_nb,_nb_prec,omega_s,phi_s`
  + cache campo-spinoriale `psi_spin,rho_spin,_psi_spin_prec` + **stato RNG** (`net.rng.bit_generator.state`).
  BUG storico (2026-09-11): sotto `--campo-spinoriale` mancavano le 3 cache spinoriali + l'RNG → il diaglog
  contaminava (N 3228 vs 3299). **VERIFICA OBBLIGATORIA dopo OGNI modifica a diaglog/trace/misure:** run CON vs
  SENZA `--diaglog`, **BYTE-IDENTICO** (`max|A-B|=0` su TUTTI gli array, non solo N). Script `csv/_seal_53c/_check_presidio.py`.
  Futuro concordato (non ora): refactor diaglog→messaging (produttore emette snapshot immutabile; consumer
  applica REGOLE PURE disaccoppiate da `net`) → purezza per costruzione.

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
- **OGNI COMMIT COINCIDE CON UNA PUSH** (regola Luca 2026-09-11): dopo ogni `git commit` fai subito `git push`.
  (Sostituisce la vecchia regola "push solo su richiesta".)
- **Messaggi di commit MOLTO APPROFONDITI:** cosa/perche'/come, file toccati, esito sigilli/verifiche, numeri
  chiave, cosa deve ri-controllare il prossimo agente. Un commit deve bastare a capire lo step senza il codice.
- **PRIMA DI OGNI RUN: commit + push.** Nessun run (test, campagna, check) parte con working tree sporco non
  committato: prima si committa e pusha lo stato, poi si lancia. Cosi' ogni run e' riproducibile da un commit noto.

## Allineamento e riproducibilità (SEMPRE, per il doppio-check indipendente)
- **Committa TUTTI i dati del test, non solo il verdetto.** Le evidenze grezze (CSV diaglog/condensazione) E
  gli script di analisi (`_verifica.py`, `_valuta*.py`, `_confronta.py`) vanno versionati, così il prossimo
  agente (Claude) può rifare il doppio-check SENZA rilanciare. Non lasciare untracked le evidenze su cui poggia
  un verdetto etichettandole "rigenerabili".
- **Nel messaggio di commit di' ESPLICITAMENTE a Claude cosa sono i file e cosa verificare:** quale run è quale
  (es. OLD=pre-flag, OFF=flag off, ON=flag on), su quali dati gira lo script di analisi, e i punti sospetti della
  logica da ricontrollare. Un sigillo vale quanto il codice che lo verifica → serve revisione indipendente.
- **Escludi solo il davvero-rigenerabile, e indica SEMPRE nel commit COME rigenerarlo** (es. `_old_sim.py` =
  `git show <commit>:soliton_simulator.py`; `.pkl` = DB deterministici da seed). Mai escludere le evidenze di un verdetto.
- **Allinea la doc canonica su `main` a valle di OGNI step/verdetto** (worktree `../st_main`): il tracing
  (`CLAUDECONNECT.md`, `Checkpoint.md`, `CLAUDE.md`) deve riflettere l'esito PRIMA di chiudere il task.
- **Verifica che il push sia andato davvero:** `git status -sb` deve mostrare il branch allineato con `origin`
  (e `git ls-files`/`git status --short` sulle cartelle dei dati). Non fermarti al commit locale.
