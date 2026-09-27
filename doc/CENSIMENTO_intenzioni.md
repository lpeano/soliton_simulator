# CENSIMENTO delle INTENZIONI DICHIARATE E MAI FATTE RISPETTARE


> ## ⚠ **VERIFICA DI CONTROLLO, fatta dopo la consegna e PRIMA del commit**
> Il censimento e' stato prodotto da un **sotto-agente**. **Non l'ho relazionato sulla fiducia:**
> ho riverificato un campione delle affermazioni che portano piu' peso, e **una era sbagliata**.
>
> | affermazione | esito della verifica |
> |---|---|
> | `A2` `TORS_4PI = True`, commento *"prova sperimentale"*, **nessun `--tors-4pi`** | ✅ confermata *(0 occorrenze del flag)* |
> | `A3` `COPPIA_MIT` si contraddice *("ATTIVA" e "spenta di default")* | ✅ confermata, e le due frasi stanno **sulla stessa riga** |
> | `A6` il `README` dice *"tutti gli script includono `--sync`"* | ✅ confermata: **`SYNC_UPDATE = False` a runtime** nell'argv del driver |
> | `B12` *"nemmeno una traccia: 0 file in `doc/`"* | ### ❌ **SBAGLIATA: i file sono 2.** Corretta in loco |
> | il riscontro trasversale *(0 voci d'indice)* | ✅ confermato su **tutti e quattro** i flag provati |
>
> **La correzione di `B12` NON annulla la voce: la indebolisce.** `KERNEL_ALPHA` **e' censito**
> come *guardia silenziosa* il 2026-09-20, ma **mai misurato come legge** — resta in **(B)**.
>
> **E il riscontro trasversale regge, ed e' la cosa piu' importante del file:** delle sette voci
> di **(A)**, **nessuna ha un ID nell'indice**.

> Sola lettura, **2026-09-27**. Branch `fork-su2`, `HEAD` = `5979372`.
> **Questo documento NON corregge niente e NON propone nessuna cura.** Elenca e classifica.
> Nessun file esistente e' stato toccato; nessun run del simulatore e' stato lanciato.
> *(Prosecuzione di metodo di `doc/AUDIT_misurato_vs_asserito.md` (2026-09-14), che classificava
> MISURATO / ASSERITO / SMENTITO sulle AFFERMAZIONI. Qui l'oggetto e' diverso: le PROMESSE.)*

---

## QUANTE VOCI, PER CLASSE

| classe | che cos'e' | voci |
|---|---|---|
| **(A)** | **dichiarata e FALSA nel codice** -- il codice fa il contrario di cio' che il commento dice | **7** |
| **(B)** | **costruita e mai misurata** -- esiste, gira o puo' girare, nessuna prova | **16** |
| **(C)** | **misurata** -- con la citazione del referto / sigillo / commit | **12** |
| **(D)** | **obsoleta o superata** -- la premessa e' caduta o il codice e' cambiato | **6** |
| | **totale** | **41** |

**Le voci ambigue sono in (B) con l'ambiguita' dichiarata nella riga stessa** (`B2`, `B4`, `B13`,
`B15`), come prescritto dal mandato: meglio una voce da declassare che una persa.

---

## IL METODO

**LE CHIAVI CERCATE** (case-insensitive dove serve): `SPERIMENTALE` * `da misurare` *
`da validare` * `da verificare` * `riduzione al limite` * `ESPLORATIVO` * `TODO` *
`DA RIPRENDERE` * `APERTO` * `non ancora` * `orfano` / `ORFANO` * `default off` / `OFF di default` *
`IN VERIFICA` * `da decidere` * `provvisorio` * `placeholder` * `per ora` * e, in un secondo giro,
`MAI VALIDATO` * `mai misurato` * `mai sigillato` * `MAI CHIAMATA` * `MUTO` * `inerte`.

**I FILE COPERTI:**

- `soliton_simulator.py` (10 638 righe) -- **per grep, mai letto interamente**; letti i blocchi di
  contesto attorno a ogni riscontro;
- `csv/_passo.py`, `csv/_cli_flag.py`, `csv/_presidio.py` -- **zero riscontri di sostanza** (i soli
  hit sono la parola *metodo* e una frase sul lavoro esplorativo in `_presidio.py:32`, che e' una
  motivazione di progetto, non una promessa);
- `README.md`, `FISICA.md`, `Checkpoint.md`, `CLAUDE.md`;
- `doc/COMPONENTI_PROMOSSE.md` (**la fonte piu' densa**: e' il registro che governa che cosa e'
  fisica di default, candidata, esperimento o esclusa), `doc/AUDIT_misurato_vs_asserito.md`,
  `doc/REFERTO_calcpsi_tempo1.md`, `doc/REFERTO_calcpsi_tempo2.md`, `doc/STATO_RUN.md`,
  `doc/REGISTRO_FISICA.md` (per grep);
- `csv/_seal_fork/` e `csv/_seal_fase1/` -- **elenco completo dei file**, per cercare la prova;
- `doc/INDICE_ID.tsv` -- **NON letto** (170+ KB, vietato dal mandato): interrogato con
  `python csv/_indice_id.py --testo <PAROLA>` su sette chiavi.

**COME HO DATATO.** Per ogni riscontro, la **prima apparizione della stringa** nella storia:

```
git log --all -S"<stringa>" --format="%h %ad" --date=short -- <file> | tail -1
```

(!) **Il limite di questa datazione, e va detto:** `670310f` **(2026-08-28)** e' il commit che importa
`soliton_simulator.py` per la prima volta (*"Implement code changes to enhance functionality and
improve performance"*, verificato con `git log -1 670310f`). **Ogni voce datata 2026-08-28 significa
quindi "c'era dal primo blob di questo repo", non "e' nata quel giorno":** la sua eta' reale e'
ignota e potrebbe essere maggiore.

**COME HO VERIFICATO SE UNA COSA E' ATTIVA NEL DRIVER.** Il driver e' `csv/_test_fork/_scena_video.py`.
Una volta sola, l'introspezione dei booleani di modulo nella configurazione del driver:

```
python -c "import sys;sys.path.insert(0,'csv');import _cli_flag;_S,a=_cli_flag.argv_del_driver(dest='csv/_test_fork/_scarto_cli');S,_=_cli_flag.carica_dal_cli(list(a),nome='chk');[print(k,'=',v) for k,v in sorted(vars(S).items()) if isinstance(v,bool)]"
```

e, nello stesso giro, l'argv verbatim del driver (`_cli_flag.argv_del_driver`):

```
soliton_simulator.py --test MASSE-COERENTI --nmasse 3 --sep 6.1158 --giri 0 --campo-spinoriale
--spinore-vivo --spinore-corretto --chi-core --calore-scal --deparam-orologio --verlet --fork-su2
--fork-su2-mem --cs-dinamico --tau-luce --rumore-colorato --pav-com --guscio-morbido --zeta-vir
--ritmo-wrap-2pi --tempo-unico-mitosi --semina-lam --semina-matura --mitosi-2lam --pozzo-d
--contrasto-intensivo --nodi 0 --chi-basc --chi-coop --coes-adim --peq-esatto --peq-nascita-locale
--scala-min-passo --coes-causale --anom-simm --invarianti=on --plast-din --viriale --olon-part
```

**Per i parametri NON booleani** (`COPPIA_MIT`, `PLAST_MIT`, `MITOSI_DIR`, `KERNEL_ALPHA`,
`GAMMA_TURBO`) la tabella dei booleani non dice nulla: ho verificato **dall'argv** che il driver non
passa il loro flag, quindi resta il default di modulo letto dal sorgente.

**COSA SIGNIFICA "nessuna prova trovata".** Ho cercato, per la componente, un referto in `doc/`, un
sigillo in `csv/_seal_fork/` (elenco completo dei ~250 file), una voce nell'indice
(`--testo`), un commit. **Se scrivo "nessuna prova trovata" significa che NON L'HO TROVATA, non che
non esista.** Non ho mai dedotto l'assenza di una misura dal silenzio del codice.

---

## (!) UN RISCONTRO CHE VALE PER TUTTO IL CENSIMENTO: **le intenzioni non sono nell'indice**

`python csv/_indice_id.py --testo <chiave>` su 805 voci:

| chiave | voci nell'indice |
|---|---|
| `sperimentale` | **0** |
| `in verifica` | **0** |
| `esplorativo` | **0** |
| `orfano` | **0** |
| `mai validato` | **0** |
| `TORS_4PI` | **0** |
| `COPPIA_MIT` | **0** |
| `MITOSI_DIR` | **0** |
| `KERNEL_ALPHA` | **0** *(nell'INDICE. In `doc/` sono 2 file: vedi la correzione in `B12`)* |
| `da misurare` | 2 (`MITOSI-TASSO`, `PSI-FLASH`) |
| `riduzione al limite` | 4 (`COMPONENTI:B6`, `COMPONENTI:S2`, `SCIOGLIMENTO-FASE`, `PESO-MAX`) |

> **La famiglia "dichiarato e mai fatto rispettare" non ha una casa nell'indice.** L'unica voce che
> intercetta una di queste componenti e' `COMPONENTI:B6` (`--campo-spinoriale`, stato
> `da-decidere`), e ci arriva **per riflesso** da `doc/COMPONENTI_PROMOSSE.md`, non perche' qualcuno
> abbia aperto la voce. Delle sette voci di (A), **nessuna** ha un ID.

---

# (A) DICHIARATA E FALSA NEL CODICE -- 7 voci

## `A1` -- la RIDUZIONE AL LIMITE dello spinore: lo stato che la garantisce non e' raggiungibile

| | |
|---|---|
| **dove** | `soliton_simulator.py:1427-1430` (blocco di `CAMPO_SPINORIALE`), `:4006-4016` (dentro `calcola_psi`), `_estendi_psi_spinor` **`:1952-1962`**, `_bloch_a_spinore` **`:1868-1873`** |
| **data di nascita** | **2026-09-09** (`954549f`, prima apparizione di *"non ancora agganciato a"*, nello stesso blocco) |
| **cosa promette** | *"Riduzione-al-limite: con `_psi_spinor=(e^{i phi},0)` la componente 0 == campo scalare"* -- cioe' che il campo spinoriale si riduca **esattamente** al campo scalare |
| **prova** | `csv/_seal_fase1/_sigillo_fase1.py` **esiste e testa S3** -- ma **INIETTA a mano** lo stato (`psp[:,0] = np.exp(1j*net.phi)`) e commuta `sm.CAMPO_SPINORIALE` **sul modulo**. Nessun file di referto committato accanto (`csv/_seal_fase1/` contiene **solo** il `.py`). La dichiarazione e' inoltre ricopiata in `doc/REVISIONE_avvio_e_memoria.md:66` e `doc/REFACTORING_SPINORIALE.md:228` |
| **attiva nel driver** | **SI** (`--campo-spinoriale` nell'argv) |

**PERCHE' E' FALSA, dal codice.** `_estendi_psi_spinor` inizializza **sempre** da
`_bloch_a_spinore(nb_rif)`, e quel metodo restituisce

```
np.stack([np.cos(th/2.0), np.sin(th/2.0)*np.exp(1j*ph)], axis=1)
```

cioe' **la componente 0 e' REALE** (`cos(th/2)`) e **`phi` -- la fase U(1) -- non vi entra affatto**:
`th` e `ph` vengono dai soli `nb[:,2]` e `arctan2(nb[:,1], nb[:,0])`. Lo stato `(e^{i phi}, 0)` non
e' un caso limite del percorso vivo: e' uno stato **che il percorso vivo non produce mai**. L'unico
punto del file che lo produce e' il **fallback** di `calcola_psi` (`:4014-4015`), che scatta solo se
`_psi_spinor` e' assente o piu' corto di `n`.

> **La forma dell'errore:** il sigillo verifica una **proprieta' algebrica di `calcola_psi`** (vera),
> e la dichiarazione la presenta come una **riduzione al limite del sistema** (non verificata,
> perche' il limite e' fuori dall'orbita del sistema).

---

## `A2` -- `TORS_4PI`: *"Prova sperimentale, default off"*, e il default e' `True`

| | |
|---|---|
| **dove** | `soliton_simulator.py:894-897` |
| **data di nascita** | **2026-08-28** (`670310f`, primo blob: **il valore `True` e il commento *"default off"* nascono insieme**) |
| **cosa promette** | che sia un ramo **sperimentale**, **spento per default**, quindi con un braccio OFF disponibile |
| **prova** | `doc/COMPONENTI_PROMOSSE.md:27` lo elenca fra i **dieci flag gia' a `True`** che *"non sono mai passati per i tre criteri"*. **Nessun sigillo dedicato trovato.** Nessuna voce nell'indice |
| **attiva nel driver** | **SI** (`TORS_4PI = True`) |

**E NON E' SOLO IL COMMENTO.** `TORS_4PI` **non ha flag da riga di comando** (nessun `--tors-4pi` in
`soliton_simulator.py` ne' in `csv/_cli_flag.py`): non e' spegnibile, quindi **il braccio OFF che il
commento promette non esiste**. I suoi lettori sono nel percorso vivo: `:596` (`DENS_CRIT_C`),
`:5446`, `:5922`, `:5951-5955`, e la soglia di mitosi stampata a `:7762`/`:8050` (`3*np.pi if
TORS_4PI else PHI_CRIT`).

---

## `A3` -- `COPPIA_MIT`: *"(opzione, spenta di default)"*, e il default e' `1.0`

| | |
|---|---|
| **dove** | `soliton_simulator.py:856-865` |
| **data di nascita** | **2026-08-28** (`670310f`) |
| **cosa promette** | due cose: che sia **spenta di default**, e che olonomia / **separazione della coppia** / **effetto sulla densita'** siano *"Da MISURARE"* |
| **prova** | **nessuna prova trovata** per le tre osservabili: `grep -rl "separazione della coppia" doc/` = **0 file**; nessun `_sigillo_coppia*` in `csv/_seal_fork/`; nessuna voce nell'indice |
| **attiva nel driver** | **SI** -- `COPPIA_MIT = 1.0` e l'argv del driver non passa `--coppia`, quindi il ramo `if COPPIA_MIT > 0.0` (`:6327`) gira |

**IL BLOCCO SI CONTRADDICE DA SOLO, A UNA RIGA DI DISTANZA.** `:856` apre con *"CREAZIONE DI COPPIA
alla Schwinger **ATTIVA** (default B)"* e `:857` continua, sulla stessa riga fisica, con
*"EMISSIONE DI COPPIA alla mitosi (opzione, **spenta di default**)"*. Sono due strati di commento
sovrapposti: quello vecchio non e' stato rimosso quando il default e' stato ribaltato -- **ed e'
esattamente il caso che `CLAUDE.md` par.6 (2) descrive**: *"quando un default si ribalta, "l'assenza del
flag" smette di significare OFF"*.

---

## `A4` -- `MITOSI_DIR`: *"MITOSI DIREZIONALE ATTIVA"*, e il valore e' `0.0`

| | |
|---|---|
| **dove** | `soliton_simulator.py:899-902`, ramo a `:6192` |
| **data di nascita** | **2026-09-02** (`21563d7`) |
| **cosa promette** | il commento **apre** dichiarandola **ATTIVA** e **chiude** con *"Sperimentale."* |
| **prova** | menzionata in `doc/REGISTRO_FISICA.md`; **nessuna misura trovata**; nessuna voce nell'indice |
| **attiva nel driver** | **NO** -- `MITOSI_DIR = 0.0`, e `if MITOSI_DIR != 0.0` (`:6192`) **non gira mai**. Nessun flag CLI |

**E' l'errore SPECULARE ad `A2`/`A3`:** li' il commento dichiara spento cio' che e' acceso, qui
dichiara **attivo cio' che e' spento**. Chi legge il commento crede che la replicazione sia
polarizzata e che il baricentro trasli lungo la geodetica; il codice non calcola nemmeno il `bias`.

---

## `A5` -- `_passo_spinoriale` *"ORFANO"*: smentito da un altro commento dello stesso file

| | |
|---|---|
| **dove** | dichiarazione `soliton_simulator.py:1037-1044`; **smentita** `:3823-3824` |
| **data di nascita** | **2026-09-03** (`2a97cad`, prima apparizione di *"e' ORFANO"*) |
| **cosa promette / afferma** | *"l'EVOLUZIONE SU(2) E' CONGELATA. Il metodo `_passo_spinoriale` (Passo 2+3) e' ORFANO: la sua chiamata e' stata rimossa ... e non e' mai stata reinnestata nel percorso vivo"*, con la conseguenza dichiarata che *"la fase di Berry / curvatura non-abeliana misurata dal 2026-09-02 e' ~0 per SPINORE CONGELATO"* |
| **prova della smentita** | il file lo dice **di se stesso** a `:3823-3824`: *"TERZO CASO DELLA STESSA FAMIGLIA: `_passo_spinoriale` con docstring "ORFANO" ma **VIVO**; `VERSO_CHI` cablato ma MUTO; `spin_locale` definita e MAI CHIAMATA. **Lo stato di vita del codice non e' leggibile dal codice.**"* Il reinnesto e' `SPINORE_VIVO` (`:1048-1051`), **`True` nel driver** |
| **attiva nel driver** | **SI** (il metodo gira) |

Il blocco `:1030-1044` **non e' stato aggiornato** quando il reinnesto e' avvenuto. *(La storia di
questa voce e' in `D4`.)*

---

## `A6` -- `README.md`: *"Tutti gli script di lancio includono esplicitamente `--sync`"*

| | |
|---|---|
| **dove** | `README.md:175` (e le righe collegate `:155`, `:181`, `:295`, `:325`, `:337`) |
| **data di nascita** | **2026-09-03** (`fea9900`) |
| **cosa promette** | che `--sync` sia nella configurazione di **ogni** lancio, *"sia nel ramo [...]"* |
| **prova** | **smentita per misura, in questo giro**: l'argv del driver `csv/_test_fork/_scena_video.py`, letto con `_cli_flag.argv_del_driver`, **non contiene `--sync`**, e `SYNC_UPDATE = False` nella tabella dei booleani |
| **attiva nel driver** | **NO** |

La frase descrive i `.bat` storici alla radice del repo (`RunTutti.bat`, `run_*.bat`), che **non sono
il percorso vivo**. Un lettore che prende il README per la configurazione corrente conclude
l'opposto del vero. *(Vedi anche `B7` per la promessa di misura su `--sync`, e `D5` per la sua
riclassificazione.)*

---

## `A7` -- il commento di `calcola_psi`: *"~19 chiamanti"*, misurato **2**

| | |
|---|---|
| **dove** | `soliton_simulator.py:3978-3986` |
| **data di nascita** | **2026-09-17** (`203136f`) |
| **cosa afferma** | *"L'architettura giusta c'e' gia' (il parametro `w` esiste), ma **~19 chiamanti** non lo passano"* |
| **prova che lo smentisce** | `doc/REFERTO_calcpsi_tempo1.md`: *"**NON LO SONO.** Le chiamate a `calcola_psi` dentro il passo sono **DUE**, non sedici"*, con la tabella per sito (`step:3006` 20 volte, `step:3118` 20 volte, `_registra_concorrenza:1768` 3 volte al setup). Sigillo `csv/_seal_fork/_sigillo_calcpsi_T1.py` / `.txt` |
| **attiva nel driver** | **SI** (i contatori `_calcpsi_chiamate` / `_calcpsi_w_none` / `_calcpsi_origini` girano) |

**Il commento non e' stato corretto dopo la misura.** *(La misura e la cura parziale sono in `C2`.)*

---

# (B) COSTRUITA E MAI MISURATA -- 16 voci

| # | dove | data di nascita | cosa promette | prova | attiva nel driver |
|---|---|---|---|---|---|
| **`B1`** | `soliton_simulator.py:1060-1065` (`SPINORE_VIVO`) | **2026-09-18** (`2bf446f`) | *"`SPINORE_VIVO = True` **NON E' MAI STATO VALIDATO COME DEFAULT** ... NESSUN SIGILLO e' mai stato girato con questo valore come DEFAULT DI MODULO. E' un cambio **NON CERTIFICATO** finche' il rigiro completo non e' chiuso"* + *"Richiede **rimisura di Berry**"* | **nessuna prova trovata** del rigiro completo ne' della rimisura di Berry. `doc/COMPONENTI_PROMOSSE.md` **B4** lo tiene *"NON STABILITO"* | **SI** (`--spinore-vivo`) |
| **`B2`** | `:1621-1650` (`SPIN_FEEDBACK`) | **2026-09-18** (`6b045c0`) | ON di default *"PER DECISIONE DI LUCA E SU BASI DI FORMA, **NON** perche' una misura lo abbia mostrato migliore"* | **PARZIALE, e la parte mancante e' dichiarata**: la FORMA e' misurata (antisimmetria da `1.112` a `6.5e-16`, sigillo **12/12** `csv/_seal_fork/_sigillo_denominatore.txt`), l'**EFFETTO no**: A/B a **quattro semi** senza effetto, segno non concorde (`doc/REFERTO_semi_spin_feedback.md`), e `doc/COMPONENTI_PROMOSSE.md` par.H ammette *"ne soddisfa due su tre"*. (!) **AMBIGUA**: (C) sulla forma, (B) sull'effetto -- messa in (B) | **SI** |
| **`B3`** | `:508` + corpo `:3617-3622` (`TAU_A_LOCALE`) | **2026-08-28** (`670310f`) | *"IN VERIFICA"*, e nel corpo: *"stabile, ma **il guadagno sul decadimento lungo non e' ancora confermato** (manca il confronto lungo TAU_A-fisso vs locale)"* | **nessuna prova trovata** del confronto lungo. `doc/COMPONENTI_PROMOSSE.md:33-53` gli dedica una sezione: *"non e' spegnibile per un A/B -> il criterio (2) non e' nemmeno **verificabile**: non esiste il ramo OFF su cui fare la byte-identita'"*. `doc/REFERTO_tau_a_due_leggi.md` tratta la **separazione dei due ruoli** di `TAU_A`, non il confronto promesso | **SI** (e **senza flag CLI**) |
| **`B4`** | `:411` (`TAU_LOCALI`), commento a `:415-416` | **2026-08-28** (`670310f`) | *"costanti temporali TAU_P/TAU_BG/TAU_TW come RAPPORTI adimensionali ... rispetto a frequenze locali (invarianza per riparametrizzazione). **IN VERIFICA**"* | **nessuna prova trovata**. `doc/COMPONENTI_PROMOSSE.md:23` fra i dieci non certificati. (!) **AMBIGUA per una ragione di forma**: le righe `:415-416` che portano *"IN VERIFICA"* e *"False = costanti fisse"* stanno **dopo** `CALORE_VETTORIALE` (`:413-414`), quindi **il commento e' orfano del suo flag** e a colpo d'occhio sembra riferirsi al flag sbagliato | **SI** (e **senza flag CLI**) |
| **`B5`** | `:95` (`SCHERMATURA`) | **2026-09-03** (`5198938`) | *"**Da validare su TEMPI LUNGHI** (hardware di Luca): taglia stabile e coerente?"* | **nessuna prova trovata**. `Checkpoint.md` porta la voce gemella *"[DA VERIFICARE] Stabilita' della taglia, contrasto nucleo/guscio e indipendenza da seed su tempi lunghi (almeno ~2000 passi, preferibilmente 20000 e 2-3 semi)"*, anch'essa del 2026-09-03. `doc/COMPONENTI_PROMOSSE.md:22` fra i dieci non certificati | **SI** |
| **`B6`** | `:112` (`REGIME = "deterministico"`) | **2026-08-28** (`670310f`) | *"**DA RIPRENDERE**: seme iniziale di asimmetria strutturale (fase/torsione)"*, perche' *"manca l'innesco della prima asimmetria (tau omogeneo all'inizio)"* | **nessuna prova trovata** di un seme di asimmetria strutturale cablato. (!) Nota: `doc/COMPONENTI_PROMOSSE.md` **C3** classifica `--regime` come esperimento *OFF per sempre* perche' *"cambia **quattro interruttori insieme**"* -- mentre il **modulo** e' su `"deterministico"` | **SI** |
| **`B7`** | `Checkpoint.md:399-402` e `:410-415`; flag a `soliton_simulator.py:936` (`SYNC_UPDATE`) | **2026-09-03** (`11f3f87` / `0f6e94c`) | *"Default ancora off; **convergenza e superiorita' rispetto al percorso storico sono da misurare**"* | **PARZIALE e negativa, dallo stesso giorno**: il test di convergenza preliminare non mostra vantaggio (*"errore `phi` `1.36e-2` senza sync contro `2.37e-2` con sync"*) e `Checkpoint.md` conclude *"Non promuovere quindi a default: servono ..."*. **Nessuna misura successiva trovata in 24 giorni.** Riclassificato in `doc/COMPONENTI_PROMOSSE.md` E.bis.1 (vedi `D5`) | **NO** |
| **`B8`** | `:950-952` e `:8313` (`VERLET`) | **2026-09-03** (`7946c46`) | *"INTEGRATORE METRICO **SPERIMENTALE** ... Default off per mantenere invariato il comportamento canonico; attivare con `--verlet` per il **confronto A/B**"* | **`doc/COMPONENTI_PROMOSSE.md` B3 la dichiara esplicitamente non misurata**: *"**nessuno ha mai misurato la deriva di energia** del ramo Eulero: senza quel numero, (3) e' un'opinione"*, e registra la **tensione**: *"Il suo commento dice "INTEGRATORE METRICO SPERIMENTALE"; `CLAUDE.md` par.4 **prescrive** Verlet per il second'ordine ... **Le due frasi non possono essere entrambe vere**"*. Nessun `_sigillo_verlet*` in `csv/_seal_fork/` | **SI** (`--verlet` nell'argv) -- cioe' **il ramo "sperimentale" e' il percorso vivo** |
| **`B9`** | `:851-853` (`ANTIFASE_ADD`) | **2026-08-28** (`670310f`) | *"LEGGE DI STABILITA' (**esplorativa**): i nuovi nodi in regione sovra-densa nascono in ANTIFASE ... il grumo si stabilizza"* | **nessuna misura trovata.** `doc/COMPONENTI_PROMOSSE.md` par.E la **esclude** -- ma **sulla base del commento stesso**: *"Finche' il commento dice "esplorativa", l'autore stesso non le classifica come fisica"*. **E' esclusa senza essere stata misurata**, ed e' per questo che sta in (B) e non in (C) | **NO** (e senza flag CLI) |
| **`B10`** | `:854-855` (`COPPIA_DENSITA`) | **2026-08-28** (`670310f`) | *"**ESPLORATIVO**: lega la creazione di coppia anche all'anomalia di densita' ... per il feedback anti-accrescimento. **Da validare**"* | come `B9`: **nessuna misura trovata**, esclusa in par.E sulla base del proprio commento | **NO** (e senza flag CLI) |
| **`B11`** | `:866-874` (`PLAST_MIT`) | **2026-08-28** (`670310f`) | tre osservabili di controllo nominate una per una -- *"esponente di scala R(M), conservazione olonomia, sopravvivenza del collasso oltre la massa critica"* -- e la clausola *"**Da MISURARE, non imporre**"* | **nessuna prova trovata** delle tre osservabili. (!) E la promessa e' rimasta **senza esecutore**: `PLAST_DIN` (**ON nel driver**, `--plast-din`) e' dichiarato il suo sostituto (*"Se True **sostituisce** PLAST_MIT statico"*), quindi la misura promessa su `PLAST_MIT` non verra' mai fatta da nessuno | **NO** (`0.0`, senza flag CLI) |
| **`B12`** | `:884-889` (`KERNEL_ALPHA`) | **2026-08-28** (`670310f`) | *"KERNEL BILANCIATO DAL TEMPO PROPRIO (tau^alpha) **SEMPRE ATTIVO** ... **meccanismo con cui la materia pesa i legami secondo il tempo proprio (principio di equivalenza)**. alpha=0 lo spegne"* | **nessuna prova trovata**: `--testo KERNEL_ALPHA` sull'indice = **0 voci**. **[CORREZIONE, verifica di controllo: <<nemmeno una traccia, 0 file in doc/>> era SBAGLIATO. I file sono DUE: `doc/TASK_HISTORY/2026-09-18_Z9-per-coorte.md` e `doc/TASK_HISTORY/2026-09-20_tre-guardie-silenziose.md`, e il secondo lo censisce come GUARDIA SILENZIOSA (`:2704  _pesi  if KERNEL_ALPHA != 0.0 ...`). Quindi NON e' <<mai censito>>: e' censito come guardia e mai MISURATO come legge. La voce resta in (B), indebolita.]** **E' il solo meccanismo sempre-attivo che non compare nemmeno nella lista dei dieci non certificati** di `COMPONENTI_PROMOSSE.md`. Rivendica il **principio di equivalenza**, che e' la prova (3) del bersaglio di progetto (`CLAUDE.md` par.1) | **SI** (`1.0`, senza flag CLI: *"alpha=0 lo spegne"* non e' raggiungibile da riga di comando) |
| **`B13`** | `:3556` (il pavimento dell'inerzia) | **2026-09-17** (`6a4980a`) | *"`inerzia = np.maximum(_contrasto * _T2, 1e-6)` -- **il pavimento RESTA: deve diventare inerte**"*, e i contatori `_inerzia_al_pavimento` / `_inerzia_tot` sono cablati a `:3557-3558` per dimostrarlo | **nessuna prova trovata** di un referto che legga quei due contatori (`grep -rl _inerzia_al_pavimento doc/` = 0 file). (!) **AMBIGUA**: i contatori potrebbero essere letti da uno script di `csv/` che non ho ispezionato uno per uno (vedi *"COSA NON HO COPERTO"*) | **SI** |
| **`B14`** | `:9787` (`SPIN DEL NUCLEO (TODO Checkpoint)`) | **2026-09-05** (`48310e0`) | l'osservabile e' calcolata (`m0_spin_core`, `m0_spin_core_disp`); `Checkpoint.md:279` la tiene fra i *"[TODO PRIORITARIO 1] Aggiungere **e misurare** `spin_core` e `spin_core_disp`"* | **PARZIALE e dichiaratamente insufficiente**: `Checkpoint.md:214` porta *"**[IN VERIFICA -- 1 solo seme]** Run `test_spincore.bat` seed 1 (2000 passi)"*. **Nessuna campagna a piu' semi trovata** | **SI** (l'osservabile e' calcolata dal driver) |
| **`B15`** | `:1598-1620` (`GAMMA_TURBO`) | **2026-09-16 circa** (dai documenti `doc/PREDIZIONE_turbo_cs2.md`, `doc/ESITO_scan_turbo_K300.md`) | il **condizionale** scritto nel commento: *"Un esito positivo va letto come "il gradiente di cs, **IN ISOLAMENTO**, retroagisce sullo spin": un CONDIZIONALE, non un'affermazione sul regime reale"* -- perche' il turbo **rompe di proposito** la condivisione di `GAMMA` | il **turbo isolato** e' misurato (`csv/_seal_fork/_sigillo_turbo.py`, `_sigillo_turbo_OUT.txt`, `doc/ESITO_scan_turbo_K300.md`). **Il condizionale no**: il regime reale con `GAMMA` **condiviso** non e' mai stato misurato (`doc/REPERTO_gamma_condiviso.md`). (!) **AMBIGUA**: (C) per il turbo, (B) per il condizionale, che e' la parte che deciderebbe. E il commento avverte di suo: *"`:5318` (diaglog) **RE-IMPLEMENTA cs inline** e NON chiama `_cs_nodo`: sotto turbo quella colonna riporta il cs NON turboato. **Non usarla.**"* | **NO** (`1.0`) |
| **`B16`** | `CLAUDE.md` par.6 + `doc/PROPOSTA_presidi_inventario.md` | **2026-09-20** (`c3837af`, creazione del documento) | (1) INVENTARIO e (2) README sono prescritti *"nello stesso commit del cambiamento, mai "poi""*, **e il file stesso ammette che non sono presidi**: *"(!) (1) e (2) **SONO REGOLE SCRITTE, NON PRESIDI: oggi non impediscono nulla** (`A9`). Il meccanismo che le renderebbe presidi e' **proposto e NON cablato**"* | **nessun hook corrispondente**: i nove `.githooks/` elencati in `CLAUDE.md` par.12 non ne contengono uno di inventario. **La prova qui e' l'autodenuncia**, che e' il caso piu' onesto del censimento: e' l'unica voce che dichiara da se' di non essere fatta rispettare | **non applicabile** |

---

# (C) MISURATA -- 12 voci, con la citazione

| # | l'intenzione | **dove sta la prova** | attiva nel driver |
|---|---|---|---|
| **`C1`** | `:113-114` *"**# APERTO**: la PRECESSIONE fra due masse persiste in regime deterministico? Se si', il momento angolare netto NON dipende dal vuoto stocastico"* (2026-08-28) | **`doc/AUDIT_misurato_vs_asserito.md`** par.1.1-1.2 e par.3.2 (2026-09-14): *"-> **Oggi e' [MISURATO], per la prima volta**: vedi par.3.2"*. (!) E l'audit registra **il difetto collaterale**: `doc/ROADMAP_fork_SU2.md:46` e `doc/BUSSOLA_TECNICA_dev-spinoriale.md:142` avevano citato **l'apodosi di un periodo ipotetico** come risultato acquisito | **SI** |
| **`C2`** | l'`A8` di `calcola_psi` (`:3978-3986`): *"prima di correggere, **SI CONTA -- e si conta CHI**"* | **`doc/REFERTO_calcpsi_tempo1.md`** (Q1/Q2 PASS, `_calcpsi_w_none = 134/134`, la tabella per sito) e **`doc/REFERTO_calcpsi_tempo2.md`** (cablaggio; Q4: *"i due **DIFFERISCONO**: nodi 1669 vs 1850 -> IL DIFETTO NON ERA TEORICO"*; **Q8 FALLISCE, `Y5` si rompe**). Sigilli: `csv/_seal_fork/_sigillo_calcpsi_T1.py`/`.txt`, `_sigillo_calcpsi_T2.py`/`.txt`. **La cura e' parziale e cablata**: `:5220` e `:5382` passano `w`, `:5261` no | **SI** |
| **`C3`** | `TAU_LUCE` (`:1525-1560`): *"Default False = byte-identico"*, con tre piani di motivazione e i numeri | **sigillato e FALLITO, e il fallimento e' committato**: `csv/_seal_fork/_sigillo_tau_luce.py`, **`doc/SIGILLO_tau_luce_FALLITO.md`**, poi `_sigillo_tau_luce_RIPARATO_2026-09-19.txt` e `doc/REFERTO_sigillo_tau_luce_riparato.md`. `doc/COMPONENTI_PROMOSSE.md` **B10**: *"criterio (2) **NON SODDISFATTO**"* | **SI** (`--tau-luce`) -- (!) **gira una componente il cui sigillo non passa**, e il registro lo dice |
| **`C4`** | `TW_SPINORE` (`:1070-1074`): *"pilota il Bloch di **tw/2** (spin-1/2, **geometrico**) ... Zero parametri"* | **smentito per misura**: `doc/REFERTO_tw_spinore.md` e `doc/COMPONENTI_PROMOSSE.md` B-bis/par.E -- *"Commento `tw/2` (un **ANGOLO**), codice `tw/(4pi)` sommato a una **VELOCITA'**: **628.3 = 2pi/DT** volte piu' debole"*. (!) Il **commento del flag** resta quello smentito: vale anche come (A), ma la smentita e' registrata altrove | **NO** |
| **`C5`** | `SPIN_LARMOR` (`:1066-1069`): *"termine non-abeliano perpendicolare a n che **sostiene la precessione di Larmor senza auto-spegnersi** quando gli spin si ordinano"* | **dimostrato falso**: `doc/COMPONENTI_PROMOSSE.md` par.E -- *"**Si autoannulla dove servirebbe** ... `np.cross(nb_vic[ii], nb_vic[jj])` **si annulla esattamente all'allineamento** ... **nullo per costruzione** proprio nel regime che dovrebbe sostenere"*. Vedi anche `doc/MAPPA_accoppiamenti_spin.md`, `doc/REFERTO_faseA_sigilli.md` | **NO** |
| **`C6`** | `L_CONSERVA` (`:846-850`): *"ERRATA, NON usare"* | **misurato, e il numero e' nel commento**: *"AZZERA tutta la rotazione rigida ad ogni passo -> distrugge la PRECESSIONE FISICA REALE (`L_z ~ -0.9`, verso coerente all'**84 %**)"*. `doc/COMPONENTI_PROMOSSE.md` par.E | **NO** |
| **`C7`** | `_feedback_spinoriale_archi` (`:2050-2065`): il docstring **precedente** diceva due cose | **il modello di come si chiude una dichiarazione falsa**: la smentita e' scritta **nel codice**, coi numeri (*"`\|sum(out)\|/max\|out\|` valeva **mediana 1.112, MAX 8.441**, quando l'errore macchina e' ~1e-16"*), e i reperti sono `doc/REFERTO_denominatore.md`, `csv/_test_fork/_scelta_denominatore.txt`, sigillo `csv/_seal_fork/_sigillo_denominatore.txt` **12/12** | **SI** |
| **`C8`** | `SCALA_P_MEDIANA` (`:510-514`): *"DIAGNOSTICO, NON FISICA ALTERNATIVA ... per la **RIDUZIONE AL LIMITE** del sigillo `Y1`. **NON ha un flag da riga di comando, di proposito**"* | `csv/_seal_fork/_sigillo_scala_p.py` / `.txt`. **L'assenza di flag e' qui una scelta dichiarata e coerente** (il sigillo lo accende in processo e lo rispegne), non l'omissione di `B3`/`B4`/`B12` | **NO** |
| **`C9`** | `STEP2_OROLOGIO` (`:1500-1524`): *"la riduzione al limite e' esatta **per COSTRUZIONE** e non per taratura"* | **promosso con sigillo 10/10 e controllo positivo**: `csv/_seal_fork/_sigillo_step2.py`, `_sigillo_step2_2026-09-16.txt`, `doc/REFERTO_faseA_sigilli.md`, `doc/REFERTO_step2_U1.md`, e `doc/COMPONENTI_PROMOSSE.md` A1 (*"`S3.0` -- **IL CONTROLLO POSITIVO**: il test VEDE l'effetto, 39/40 nodi"*). (!) Il criterio (3) resta **bloccato** e la ragione e' scritta (B9: *"a densita' reali `cs` e' MORTO"*) | **SI** |
| **`C10`** | `RUMORE_COLORATO` (`:1561-1597`): *"Aspettarsi che NON cambi i numeri e' **parte della predizione, non una scusa dopo**"* | `csv/_seal_fork/_sigillo_rumore_colorato.py` / `.txt`, `doc/PREDIZIONE_taglio_spettrale.md`. **La predizione e' stata scritta prima** | **SI** (`--rumore-colorato`) |
| **`C11`** | `spin_locale` *"definita e MAI CHIAMATA"* (`:3820-3832`) | **rimossa con sigillo di byte-identita' assoluta**: `csv/_seal_fork/_sigillo_rimozione5.py` / `.txt`, e la **dottrina** trascritta in `doc/COMPONENTI_PROMOSSE.md` par.F.4 perche' non si perdesse. Il blob di recupero e' nominato nel commento (`87450f7`) | **non applicabile** (rimossa) |
| **`C12`** | `VERSO_CHI` *"cablato ma MUTO"* | **dimostrato irraggiungibile**: `doc/COMPONENTI_PROMOSSE.md` par.E -- *"`if CHI_CORE ...` arriva **prima** di `elif VERSO_CHI ...`, e `--chi-core` e' nella config di **ogni** run: il ramo **non e' mai raggiunto**"*. Intercettato da `csv/_test_fork/_audit_default.py` | **NO** |

---

# (D) OBSOLETA O SUPERATA -- 6 voci

| # | dove | data di nascita | cosa diceva | che cosa l'ha superata | attiva nel driver |
|---|---|---|---|---|---|
| **`D1`** | `:954-960` (`ELAST_C`) | **2026-08-28** (`670310f`) il valore, **2026-09-17** la dichiarazione di morte | *"COEFFICIENTE DEL NUCLEO ELASTICO: **default storico**, esposto solo per esperimenti di ridondanza/sensibilita'"* | **la bonifica della plasticita' del 2026-09-17, e la dichiarazione e' nel file**: *">>> **INUTILIZZATO dal 2026-09-17** ... NON E' STATO CANCELLATO DI PROPOSITO: **e' EVIDENZA** ... con ELAST_C = 100 il fattore aveva mediana ~8.8e5, cioe' la plasticita' era **CONGELATA**"*. (!) **Questa e' una dichiarazione ONORATA**: si e' misurato, si e' scritto il numero, e si e' scritto **perche' il codice morto resta** | **NO** (il flag `--elast-c` esiste ancora) |
| **`D2`** | `:6230-6231` | **2026-08-28** (`670310f`) | *"profilo di percorrenza del figlio: eredita la chiralita' del genitore a (**dormiente, non ancora accoppiato**). Salto a 0."* | **la premessa e' caduta**: `perc_chi` e `perc_geom` sono letti dal percorso vivo -- `CHI_BASC`, `CHI_COOP`, `TORS_4PI` (`:5446-5447`), `FRAME_DRAG`, e la catena descritta a `:1294` e `:9109`. Reperto: `doc/REFERTO_lettori_perc_chi.md`. **Il commento e' scaduto** | **SI** (il codice gira; il commento mente) |
| **`D3`** | `:1427-1430` e `:4009` (`CAMPO_SPINORIALE`) | **2026-09-09** (`954549f`) | *"calcolato **IN PARALLELO** ... **non ancora agganciato** a gravita'/forze/mitosi (fasi 2-4)"*, ripreso in `doc/COMPONENTI_PROMOSSE.md` B6 per classificarlo *"ALTERNATIVA, non difetto"* | **la premessa sta cadendo sotto i piedi al registro**: il commit di `HEAD`, **`5979372` (2026-09-27)**, si intitola *"PSI-FLASH non e' un difetto del fotogramma: **la psi ricalcolata ENTRA nel pozzo di gravita'**"*. (!) **AMBIGUITA' DICHIARATA**: non ho verificato quale delle due frasi valga oggi nel codice, e non l'ho dedotta. *(La parte FALSA di questo blocco e' `A1`.)* | **SI** |
| **`D4`** | `:1037-1044` | **2026-09-03** (`2a97cad`) | *"l'EVOLUZIONE SU(2) **E' CONGELATA** ... e non e' mai stata reinnestata nel percorso vivo"* | **vero il 2026-09-03, superato da `SPINORE_VIVO`** (2026-09-18). Il blocco non e' stato aggiornato. *(E' la faccia storica di `A5`.)* (!) E la conseguenza dichiarata -- *"la fase di Berry ... e' ~0 per SPINORE CONGELATO"* -- **cambia di significato** ora che lo spinore e' vivo: la rimisura di Berry e' la promessa aperta di `B1` | **SI** |
| **`D5`** | `:936` (`SYNC_UPDATE`) e le sue motivazioni sparse nei documenti | **2026-08-28** il flag, **2026-09-03** le promesse | era descritto come cio' che *"accende lo scuotimento"* e come una **legge** con una convergenza da dimostrare | **riclassificato per lettura del codice**: `doc/COMPONENTI_PROMOSSE.md` **E.bis.1** -- *"**`SYNC_UPDATE`: la motivazione e' FALSA. Non accende lo scuotimento** ... **SPOSTA il punto di iniezione del rumore**"*, e *"**RICLASSIFICATA: NON e' una legge, e' uno SCHEMA DI INTEGRAZIONE** -- stessa categoria di `VERLET`"*. *(Vedi anche `A6` e `B7`.)* | **NO** |
| **`D6`** | `Checkpoint.md` nel suo insieme (~640 righe) | file **2026-09-05 / 2026-09-07** | contiene ~40 voci `[TODO]`, `[IN VERIFICA]`, `[DA VERIFICARE]`, `[IMPLEMENTATO, SPERIMENTALE]` | **almeno due sono state fatte e la voce non e' stata chiusa**: *"il TODO che chiede di **reimplementare SU(2)** e la struttura spinoriale"* (`:434`) e *"il TODO che chiede di **ancorare la schermatura a `N_c`**"* (`:437`) -- e `soliton_simulator.py:97` dichiara *"la schermatura e' **ora sempre ancorata a N_c**"*. (!) **NON COPERTO**: non ho verificato voce per voce quali dei ~40 TODO siano oggi chiusi. **Il file e' un serbatoio di intenzioni non riconciliate, e va trattato come tale** | **non applicabile** |

---

# COSA NON HO COPERTO -- dichiarato, perche' una copertura parziale dichiarata vale piu' di una totale asserita

1. **`doc/INDICE_ID.tsv` non e' stato letto** (vietato dal mandato: 170+ KB). L'ho **interrogato** con
   `csv/_indice_id.py --testo` su **sette** chiavi. Le altre chiavi del mandato non sono state
   passate all'indice: **una voce d'indice che copra una di queste intenzioni con parole diverse
   potrebbe esistere e io non l'avrei vista.**
2. **I ~250 file di `csv/_seal_fork/` e le altre cartelle `csv/_seal_*` non sono stati letti uno per
   uno**: ho letto l'**elenco dei nomi** e aperto i file rilevanti. Una prova che sta **dentro** uno
   script dal nome non parlante **non l'ho trovata**. Questo tocca in particolare `B13` (i contatori
   del pavimento dell'inerzia).
3. **`csv/_test_fork/` non e' stato censito.** Ho usato il suo driver e citato due suoi file
   (`_audit_default.py`, `_scelta_denominatore.txt`) perche' altri documenti li nominano, ma **non ho
   cercato chiavi al suo interno**. E' plausibile che contenga sonde che leggono contatori `A8` di
   cui io ho scritto *"nessuna prova trovata"*.
4. **`doc/relazioni/` (i giorni chiusi) non e' stato censito**, ne' `RELAZIONE_PER_CLAUDE.md` oltre un
   grep di superficie. Una misura fatta e relazionata **solo** in un giorno chiuso, senza referto e
   senza sigillo, **mi sfugge**.
5. **Il confronto sistematico README-contro-default non e' stato fatto.** Ho verificato **un** caso
   (`A6`, `--sync`). `CLAUDE.md` par.6 (2) prescrive che il README dichiari *"il DEFAULT"* di ogni flag:
   **un censimento completo di quella tabella contro i valori reali di modulo e' un lavoro a se',
   e non l'ho fatto.**
6. **I file storici alla radice non sono stati censiti**: i nove
   `soliton_simulator.backup_*.py`, `soliton_simulator.regressione_*.py.bak`, i ~40 `.bat`,
   `RELAZIONE_CLAUDE_2026-09-08.md`, `RELAZIONE_CLAUDE_2026-09-09.md`,
   `RELAZIONE_CLAUDE_dev-spinoriale.md`, `STATO_CLAUDE_fork-su2.md`, `ROADMAP_dev-spinoriale.md`,
   `REPORT_LIMITE_CONTINUO.md`, `REPORT_SESSIONE_2026-09-04.md`,
   `INTERPRETAZIONE_campagna_spinore_vivo*.md`, `AVVISO_LAVORO_IN_CORSO.md`,
   `GEOMETRIA_CONTATTO.md`. **Sono per definizione pieni di intenzioni scadute**, e censirli
   richiederebbe prima decidere quali siano ancora vivi.
7. **`doc/` conta 200+ file.** Ho letto integralmente o in parte **otto** documenti e ho grep-ato
   l'intera cartella per nome di flag. **Le `PREDIZIONE_*.md` (18 file) non sono state confrontate
   una per una col loro esito**: una predizione scritta e mai verificata e' esattamente l'oggetto di
   questo censimento, e **quel filone e' scoperto**.
8. **Non ho lanciato nessun run**, quindi **nessuna** delle voci (B) e' stata risolta in questo giro:
   il censimento dice *"non trovo la prova"*, non *"la misura dara' questo"*.
9. **Le date sono date di PRIMA APPARIZIONE DELLA STRINGA, non dell'intenzione.** Vedi l'avvertenza
   su `670310f` nel paragrafo del metodo: undici delle voci sono datate 2026-08-28 solo perche' quel
   commit importa il file intero.
