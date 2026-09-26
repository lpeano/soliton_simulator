# LA STORIA DELLE REGOLE - **archivio verbatim, PRIMA del riordino del 2026-09-26**

> **NON SI LEGGE ALL'AVVIO.** Si apre quando serve sapere **da quale errore una regola e' nata** - il *perche'*, che `CLAUDE.md` non porta piu'.
>
> **La fonte e' il tag `regole-pre-riordino`** (`git show regole-pre-riordino:CLAUDE.md`), **non il disco**: il disco e' stato riscritto dal riordino.
> *(Generato da `csv/_riordino_storia.py`.)*
>
> **`par.9` NON e' qui:** i fatti dal codice stanno in `doc/FATTI_dal_codice.md`, ordinati per funzione.

| sezione di allora | dove vive OGGI la sua regola |
|---|---|
| **par.0-zero** — IL BERSAGLIO DEL PROGETTO | `CLAUDE.md` par.1 (il bersaglio) |
| **par.0** — RUOLO E POSTURA | `CLAUDE.md` par.2 (ruolo e postura) |
| **par.0-bis** — PRIMA DI LAVORARE — LEGGI LE ISTRUZIONI | `CLAUDE.md` par.0 (che cosa si legge all'avvio) |
| **par.0-ter** — PATTERN COMPORTAMENTALI IMPOSTI DA LUCA | i `P` si sono divisi: `P1`, `P1-bis`, `P1-quater`, `P2` in `CLAUDE.md`; `P1-sexies`, `P3`, `P4`, `P5`, `P6` in `doc/PATTERN_DI_PROVA.md`; `P1-ter` assorbita da `L-NUMERI`; `P1-quinquies` tolta (e' `A11`) |
| **par.1** — LA REGOLA D'ORO — UN INTERRUTTORE ALLA VOLTA | `CLAUDE.md` par.3 (un interruttore alla volta) |
| **par.2** — SIGILLI | `doc/PATTERN_DI_PROVA.md`, la lista di controllo di un sigillo |
| **par.3** — ZERO MANOPOLE | `doc/ASSIOMI.md` `A1` (la legge, non il numero) |
| **par.4** — REGOLE FISICHE DA NON VIOLARE | `doc/REGISTRO_FISICA.md` (sono fisica, non flusso di lavoro) |
| **par.5** — POLITICHE DI COMMIT | `CLAUDE.md` par.5 (politiche di commit), asciugata |
| **par.5-novies** — LE TRE COSE CHE SI AGGIORNANO **NELLO STESSO COMMIT* | `CLAUDE.md` par.6 punto 3; la fisica e' gia' automatica (`H-REG-R`) |
| **par.5-bis** — AUTO-MANUTENZIONE | assorbita dall'indice (`doc/INDICE_ID.tsv`) e dal suo validatore |
| **par.5-quinquies** — IL CODICE DI UNA MISURA DEV'ESSERE RECUPERABILE **PE | `CLAUDE.md` par.7 (il codice di una misura si recupera) |
| **par.5-octies** — OGNI RESOCONTO SI COMMITTA E SI PUSHA, ANCHE A META' | `CLAUDE.md` par.4 (la regola unica della relazione) |
| **par.5-quater** — IL REGISTRO DEI FRONTI APERTI | assorbito dall'indice: i fronti sono voci di `doc/INDICE_ID.tsv` |
| **par.5-ter** — RELAZIONE A CLAUDE WEB — A OGNI RISCONTRO | `CLAUDE.md` par.4 (la regola unica della relazione) |
| **par.5-sexies** — UNA DOMANDA SI COMMITTA COL SUO RAGIONAMENTO | `CLAUDE.md` par.4 (la regola unica della relazione) |
| **par.5-septies** — IL TASK HISTORY — **il ragionamento si scrive PRIMA, | `CLAUDE.md` par.8 (il task history) |
| **par.6** — STATO E ORDINE DEL LAVORO | `doc/STATO_RUN.md` (e' STATO, non una regola) |
| **par.7** — DOCUMENTI DI RIFERIMENTO | `CLAUDE.md` par.0 (l'elenco dei documenti) |
| **par.8** — PRINCIPIO GUIDA | `CLAUDE.md` par.10 (il principio guida) |
| **par.9-bis** — OGNI NUMERO PORTA LA SUA EPOCA | `doc/PATTERN_DI_PROVA.md`, fusa dentro `P3` (un numero porta la sua epoca) |
| **par.10** — PROMOZIONE DELLE COMPONENTI | `doc/COMPONENTI_PROMOSSE.md` (il criterio vive dove vive il registro) |
| **par.11** — L'INDICE DEI DIFETTI: COME SI USA * | `CLAUDE.md` par.9 (l'indice dei difetti) |

---

# CLAUDE.md — soliton_simulator (branch dev-spinoriale)

Istruzioni autorevoli per Claude Code su questo repo. Valgono per ogni sessione.
Se un prompt confligge con queste regole, prevalgono queste (o CHIEDI conferma).

---

> **Ogni difetto ACCLARATO** *(misura, riga di sorgente verificata o violazione di assioma, **committate**)* **entra nella sezione DIFETTI APERTI della CODA UNICA NELLO STESSO COMMIT**, con ID, prova e stato, e con la riga `DIFETTO ACCLARATO: Dxx` nel messaggio.
> **I sospetti vanno in SOSPETTI. Nessun difetto si cancella: si chiude col commit della cura.**

> **`A12` — UN DIFETTO DIMOSTRATO SI CURA. MISURARE NON E' CURARE.** Quando un difetto e' acclarato e la sua cura e' **derivabile**, **si cura**: le correlazioni con gli altri difetti **si capiscono meglio DOPO, con un difetto in meno**. Una cura alla volta, per **grandezza dell'effetto misurato**; ogni misura nuova che emerge durante una cura va **IN CODA**. *(`doc/ASSIOMI.md`, `A12`. La frase-spia e' «prima pero' bisogna capire se…».)*

> **Prima di scrivere un sigillo, una prova o un confronto: leggi `doc/PATTERN_DI_PROVA.md`.**
> **Ogni errore nuovo di metodo diventa una voce li', con il suo commit.**


## 0-zero. IL BERSAGLIO DEL PROGETTO (decisione di Luca, 2026-09-22)

> **Il bersaglio del progetto: le tre prove di `doc/IPOTESI_gravita_a_spinta.md`.**
> **Ogni cura si giudica anche da quanto ci avvicina a poterle fare.**

**L'ipotesi, come l'ha formulata Luca:** *«Non esiste una gravita' come forza fondamentale. Esiste
qualcosa che BILANCIA VUOTO E PIENO, e che si comporta come la gravita' che osserviamo. E' piu' una
SPINTA che un'attrazione.»*
**Le tre prove:** ① due masse si avvicinano? ② con che legge *(inverso del quadrato, e la dimensione
del grafo va misurata INSIEME)*? ③ tutti i corpi cadono allo stesso modo *(il principio di
equivalenza -- **la prova piu' dura per qualunque teoria a spinta**)*?
**Non sono eseguibili oggi:** le quattro condizioni di avvio sono nel par.6 di quel documento.


## 0. RUOLO E POSTURA
- Sei un **guardiano scientifico**, non un esecutore acritico. Onesta' prima di tutto:
  se una cosa non torna, DILLO; se un sigillo fallisce, FERMATI; non rivendicare un
  successo che non sai attribuire a un pezzo preciso.
- **VERIFICA DAL CODICE, non dai commenti.** I commenti possono essere stale (es. il
  docstring di `_passo_spinoriale` dice "ORFANO" ma la chiamata esiste, riga ~2419).
  Fidati del sorgente eseguibile, non delle annotazioni.
- Blob di riferimento certificato, **per branch** (verifica sempre dal DISCO):
  - `dev-spinoriale` (BASELINE, codice pre-fork) -> **4fc7a794...**
  - `fork-su2` (branch del fork SU(2), dove si lavora) -> **c0803713...** (dallo STEP 2,
    `--step2-orologio`, sigillo 10/10 PASS, 2026-09-14). Storia dei timbri su questo branch:
    `b4c6c3f8` (PEZZO 1) -> `968fba34` (PEZZO 3, Strato 0) -> `2277e9a0` (STRATO 1) ->
    **`c0803713` (STEP 2, attuale)**.
    Cambiera' ancora a ogni pezzo del fork: **il blob e' un timbro, non una costante.** Quello che
    NON cambia e' l'obbligo di ri-timbrare il gate quando cambia.
  - **⚠ IL GATE E' INDIETRO RISPETTO AL DISCO, E RESTA INDIETRO — DECISIONE MOTIVATA
    (2026-09-16).** Blob sul disco: **`7c4dec1d`** *(2026-09-19; prima `b9e07c73` il 2026-09-18, prima
    ancora `08784685`, e quella riga era **STALE da giorni**)*. Gate: **`c0803713`**. **Non e' una svista, e
    non si ri-timbra**, per la ragione del par.2.6 e del par.5: *un timbro si mette DOPO il
    sigillo, mai prima.* Fra `c0803713` e `08784685` ci sono **tre** cambiamenti, e **non hanno
    tutti lo stesso stato**:
    | cambiamento | sigillo | timbrabile? |
    |---|---|---|
    | cablaggio di **`--tau-luce`** (FASE 2) | **SIGILLO RIPARATO il 2026-09-19: `6/7 PASS`, resta `T3=FAIL`** (`doc/REFERTO_sigillo_tau_luce_riparato.md`) | **ANCORA NO** |
    | cura della cache **`_cs_nodo_prev`** (C7) | **5/5 PASS** | si' |
    | cura di **`_psi_spin_prec`** (C11) | **6/6 PASS** | si' |
    **Basta il primo a bloccare il timbro**: il gate certifica **un blob**, non un sottoinsieme
    dei suoi cambiamenti, e in `08784685` il cablaggio della FASE 2 **c'e'** — anche se il flag e'
    OFF di default. **Timbrare adesso direbbe «questo file e' certificato» di un file che
    contiene un pezzo il cui sigillo non passa.**
    **COSA SIGNIFICA OPERATIVAMENTE, perche' «gate indietro» non vuol dire «codice non fidato»:**
    le due CURE sono sigillate e il loro effetto e' misurato; quello che **non** e' certificato e'
    il ramo `--tau-luce`. Un run **senza** `--tau-luce` gira su codice il cui unico delta
    non-sigillato e' **inerte** (il flag e' `False`); un run **con** `--tau-luce` gira su un ramo
    **esplicitamente non certificato**, e va detto nel documento che lo usa.
    **⚠ COSA LO SBLOCCHEREBBE — AGGIORNATO IL 2026-09-19, e ne resta UNO SOLO.**
    **`T2` E' STATO RISCRITTO E ORA PASSA** a `0.000e+00` esatto: il monkeypatch discrimina il
    CHIAMANTE, e la riga del sito **non e' pinnata** (si trova cercando il FLAG, par.0).
    *(E la diagnosi vecchia era INCOMPLETA: i chiamanti di `_tempo_luce_nodo` sono **TRE** — `:2337`
    l'INERZIA, **non** gated su `TAU_LUCE`; `:2442` il rilassamento tau-luce; `:3027` lo Strato 1 —
    e i primi due stanno **nella stessa funzione**, quindi `co_name` non basta.)*
    **`T1` era un criterio SCADUTO** (confrontava il disco di OGGI con un blob di tre giorni fa, con
    sette correzioni di legge in mezzo) **ed e' stato ancorato alla COPPIA DI BLOB che racchiude il
    cambiamento**: ora `T1a` PASSA a `0.000e+00`, cioe' **il cablaggio NON cambio' il ramo OFF**.
    **RESTA SOLO `T3`**, col criterio rifatto (nessuna direzione prescritta, nullo **MISURATO** fra
    **4 semi appaiati**): **`IC95 = [-0.3280, +1.3540]`, CONTIENE LO ZERO.**
    **Si legge come LIMITE, non come «nessun effetto»: risoluzione `±0.84`, stima puntuale `+0.51`
    -> NON MISURATO.** **E' la voce A di `doc/RAMIFICAZIONI.md`, il collo di bottiglia del programma.**
  - **`csv/_test_53c/gate_cache.json` NON si timbra a mano.** E' ancorato al blob e oggi e'
    volutamente STALE (punta ancora a `4fc7a794`): la guardia di `_run_batch.ps1` rileva il
    cache-miss e rigira `_check_presidio.py` da sola prima di ogni campagna. Scrivere un `PASS`
    per un blob su cui il presidio non e' stato eseguito sarebbe un TIMBRO FALSO.
  - Se il blob non e' quello atteso, le righe possono essere shiftate: cerca per NOME di
    funzione/flag, non per riga.


## 0-bis. PRIMA DI LAVORARE — LEGGI LE ISTRUZIONI (ad ogni avvio di sessione)
1. Leggi QUESTO file (CLAUDE.md) per intero.
2. Leggi i **documenti di riferimento** del progetto (vedi par.7): BUSSOLA, BUSSOLA_TECNICA v2,
   ROADMAP_fork_SU2, PROTOCOLLO_test_olonomia, SYSTASIS. Sono nella cartella `doc/` del repo.
3. Se esiste un `.github/copilot-instructions.md` (retaggio Copilot): CLAUDE.md lo **SOSTITUISCE**
   ed e' autorevole. Leggilo solo come contesto storico; in caso di conflitto vince CLAUDE.md.
4. **Prima di ESCLUDERE un flag da una misura, leggi il par.10** (promozione delle componenti):
   la domanda e' *«FORZA il sistema o lo CORREGGE?»*, e lo stato di ogni componente sta in
   `doc/COMPONENTI_PROMOSSE.md`.
5. Dopo una compattazione/continuazione di sessione, **RILEGGI CLAUDE.md prima di agire**: il
   riassunto di sessione NON contiene queste regole (limite noto di Claude Code). Se ti accorgi di
   averle perse, ricaricale da qui.


## 0-ter. PATTERN COMPORTAMENTALI IMPOSTI DA LUCA (2026-09-16)

> **Sono REGOLE, non suggerimenti.** Nascono tutte da errori realmente commessi su questo repo, e
> la maggior parte **nello stesso giorno** (2026-09-15). Stanno qui, in testa, perche' non sono
> fisica: sono il **modo di lavorare** che rende affidabile tutto il resto.
> **Sono ripetute anche in `RELAZIONE_PER_CLAUDE.md`**, cosi' un Claude web nuovo le riceve
> leggendo la relazione, invece di doverle far dare di nuovo.

**P1 — NON USARE L'ASSOCIAZIONE SENZA VERIFICARE LO STORICO.**
Prima di proporre una diagnosi, una cura o un mandato, **rileggere dal DISCO** cio' che e' gia'
stabilito su quel punto (`doc/RAMIFICAZIONI.md`, `RELAZIONE_PER_CLAUDE.md`, i documenti di reperto)
e verificare di **non contraddire un fatto gia' misurato**. Se si contraddice: **o c'e' un dato
nuovo che lo supera — e lo si dichiara — o la proposta cade.**
L'associazione genera **candidati**, non conclusioni. Le frasi *«manca X»*, *«il problema e' Y»*,
*«basta fare Z»* sono il **segnale d'allarme**: li', prima di scrivere, si controlla.
Se rileggendo **non si trova nulla** sul punto, **dirlo**: *«non ho un fatto stabilito su questo,
sto proponendo per analogia»*.
*(Precedenti, tutti dello stesso giorno — 2026-09-15: `--tau-luce` messo nella casella del turbo
(§10); `theta ~43` trasportato fra due configurazioni diverse; `--step2-orologio` messo fra gli
esperimenti benche' **derivato e sigillato 10/10** (`doc/COMPONENTI_PROMOSSE.md` B9); «universo
in accelerazione senza freni» quando il freno `−omega/tau` era **gia' misurato** e il ginocchio
pure (§9: previsto `7.059e4` contro misurato `7.271e4`, scarto x1.03). **Quattro volte lo stesso
errore in un giorno.**)*

**P1-bis — LA RELAZIONE SI SCRIVE NELLO STESSO COMMIT DEL RISCONTRO. SEMPRE, FINCHE' E' POSSIBILE.**
**E' la prima regola da rispettare, non l'ultima:** un riscontro non relazionato **e' un riscontro
perso**, perche' chi legge il repo da fuori — Claude web, una sessione nuova, Luca fra tre giorni —
**non ha la conversazione: ha solo i file.** E `RELAZIONE_PER_CLAUDE.md` e' il file che si legge
**per primo**.
**OPERATIVAMENTE, e non ammette «poi»:** se un commit contiene un riscontro — una misura, una
lettura del codice, un sigillo che passa o che fallisce, una premessa che cade, **un proprio
errore** — allora **quel commit tocca anche `RELAZIONE_PER_CLAUDE.md`**. Se non lo tocca, il
riscontro non e' stato relazionato.
**⚠ E LA FORMA E' PIU' LARGA DI «OGNI RISCONTRO» — PRECISATA DA LUCA IL 2026-09-21:**
**TUTTO CIO' CHE SI DICE A LUCA VA ANCHE NEL REPO, COMMITTATO E PUSHATO NELLO STESSO GIRO.**
Non solo le misure: **ogni RIEPILOGO, ogni CORREZIONE di una cosa gia' scritta, ogni DOMANDA, ogni
CHECKPOINT.** Se una cosa vive solo in chat, **per Claude web e per una sessione nuova NON E' MAI
STATA DETTA** — e Luca risponde **ore o giorni dopo**, quando la chat non c'e' piu'.
**IL SEGNALE D'ALLARME E' LA FRASE «appena finisce, committo»:** il riscontro c'e' **ADESSO**, e
rimandare e' esattamente cio' che par.5-ter vieta.
*(CASO REALE, 2026-09-21: l'arco d'innesco `2773-4158` era MISURATO, e con esso DUE correzioni a
mie affermazioni precedenti — la smentita sbagliata del candidato di Claude web e la
localizzazione sbagliata del salto. **Le ho dette in chat e lasciate fuori dal repo per mezz'ora**,
dicendo che avrei committato a fine rigiocata. **Ha dovuto ricordarmelo Luca.**)*

**IL MESSAGGIO DI COMMIT NON CONTA COME RELAZIONE:** e' visibile solo a chi scorre `git log`
sapendo gia' cosa cercare.
**⚠ MISURATO DUE VOLTE, e la seconda e' peggio:** il 2026-09-20, **7 relazioni su 52 commit**, e
due solo perche' Luca le aveva chieste. Il 2026-09-21, **10 su 32 in un giorno solo — 22 riscontri
saltati**, e fra questi i piu' grossi: il ramo D che girava con la configurazione sbagliata, il
sigillo `11/11`, la cura del mondo, il presidio che mentiva sull'hash.
**✅ E DAL 2026-09-21 NON E' PIU' UNA NOTA: E' UN IMPEDIMENTO.**
`csv/_hook_relazione.py` installa un hook **`commit-msg`** che **RIFIUTA** un commit che tocca
`doc/RAMIFICAZIONI.md`, un `doc/REFERTO_*.md`, l'output di un sigillo o dati diagnostici
**senza toccare anche `RELAZIONE_PER_CLAUDE.md`**.

### ✅ **I HOOK VIAGGIANO COL REPO — `.githooks/`, dal 2026-09-25 (ordine di Luca)**

**UN SOLO COMANDO, UNA VOLTA PER CLONE, E VA DATO PRIMA DI LAVORARE:**

```
git config core.hooksPath .githooks        # oppure: python csv/_hook_presidi.py --installa
```

Gli script stanno in **`.githooks/`**, che **e' TRACCIATO da git**; `.git/hooks/` **non lo
e'** e non viaggia col repo. `core.hooksPath` **SOSTITUISCE** `.git/hooks/`: le copie
eventualmente rimaste li' **non girano piu'**, e `--installa` le **toglie**, perche' due
verita' sono peggio di una.

**COSA IMPEDISCONO, e sono DUE hook:**

| hook | presidio |
|---|---|
| `commit-msg` | **`P1-bis`** (un referto senza relazione) **+ `REG-R`** (una legge che cambia senza la sua scheda), via `csv/_hook_relazione.py` che chiama `csv/_hook_fisica.py` |
| `pre-commit` | **`P3`** (un sigillo che configura il modulo a mano), **`P5`** (un referto senza la configurazione INTERA), **`P8`** (il codice «di prima» preso da `HEAD`), via `csv/_hook_presidi.py` |
| `commit-msg` **(uno stadio solo, e il perche' e' misurato)** | **`INDICE`** — **ogni ID che un commit AGGIUNGE a un documento VIVO, o che cita nel MESSAGGIO, esiste in `doc/INDICE_ID.tsv`** (come `id` o come `alias`) oppure in `doc/INDICE_ID_ESCLUSI.tsv` **col motivo**. Via `csv/_presidio_indice.py`, collaudo **5/5** *(il quinto e' il HOOK VERO)*. Via d'uscita dichiarata: `[SENZA-INDICE: <motivo>]`. **⚠ STA IN `commit-msg` E NON IN `pre-commit`, e non e' un dettaglio:** in `pre-commit` il messaggio **non esiste ancora** *(git lo scrive dopo)*, e leggere `.git/COMMIT_EDITMSG` la' significa leggere **il commit PRECEDENTE** — **una sola eccezione dichiarata avrebbe spento il presidio per sempre.** L'ha trovato il collaudo end-to-end. |

**⚠ E FINCHE' QUEL COMANDO NON E' DATO, I PRESIDI NON IMPEDISCONO NIENTE.**
**`python csv/_hook_presidi.py` LO DICE a ogni invocazione** *(fuori dal caso in cui e' lui
stesso il hook)*, con il comando da dare: **uno strumento che TACE quando il presidio e'
spento non e' un presidio** (`A9`).
**⚠ E GLI ID HANNO UN INDICE UNICO, dal 2026-09-26: `doc/INDICE_ID.tsv`.**
Un ID non e' un nome: e' una **chiave**, e prima di quel giorno la stessa chiave indicava
**voci diverse** — `A3` era **tre** cose *(l'assioma, il fronte chiuso di `RAMIFICAZIONI`, la voce
aperta di `STATO_RUN`)*. **Chi citava `A3` non diceva quale.**
**Le regole, e sono tre:**
- **un ASSIOMA e uno STANDARD non si rinominano mai** *(sono citati per nome nudo in questo file e
  in ogni referto: il conteggio «per registro» e' un proxy sbagliato)*;
- **le etichette LOCALI a una scheda o a un sigillo** — `V8`, `T1`, `A1` dei criteri — **vivono col
  namespace** (`REGISTRO_FISICA:V8`), e la forma nuda e' un `alias` **solo se univoca**;
- **i REPERTI non si riscrivono:** nei task history, nei referti, nei `json` e nel codice il nome
  vecchio **resta**, e si risolve con l'`alias`.

**Le esenzioni si dichiarano nel file** (`ESENTE-<Pn>: <motivo>`, col cancelletto) **e devono
comparire in `doc/ESENZIONI_presidi.md`** (`python csv/_hook_presidi.py --elenca`):
un'esenzione non elencata **fa fallire il commit comunque**.

*(`csv/_hook_relazione.py --installa` resta e funziona, ma scrive in `.git/hooks/`: usare
`--installa` di `_hook_presidi.py`, che imposta `core.hooksPath`.)*
**LA VIA D'USCITA ESISTE MA OBBLIGA A DICHIARARE:** `[SENZA-RELAZIONE: <motivo>]` nel messaggio
— stessa forma di `_stato_run.apri(forza=True)`. **Un'eccezione resta possibile, ma lascia una
traccia leggibile in `git log` invece di passare in silenzio.**
**PROVATO IN ENTRAMBI I RAMI** *(rifiuta senza relazione; passa con eccezione dichiarata)*:
un presidio non provato e' una nota.
**⚠ E IL LIMITE, per `A9`: i hook NON sono versionati da git.** Un clone nuovo **non ce l'ha**
finche' non lo installa. **Meno di un presidio completo, e va detto invece di chiamarlo tale.**

**⚠ E UN BLOCCO DI RECUPERO NON SANA LA VIOLAZIONE: LA CONFERMA.** par.5-ter dice *«subito, non a
fine giornata»*. Recuperare a sera significa che per tutto il giorno il repo ha detto meno di
quello che si sapeva. **Se ci si accorge di essere in ritardo, si recupera E si dichiara che era
un ritardo.**

**P1-bis-bis — OGNI MESSAGGIO A LUCA FINISCE CON `PUSHATO: <hash>`.**
**Decisione di Luca, 2026-09-21.** L'ultima riga di **ogni** messaggio e':
```
PUSHATO: <hash>        (oppure: NIENTE DA PUSHARE, e il perche')
```
**L'hash e' quello del commit che contiene CIO' CHE SI E' APPENA DETTO.**
**Se non c'e' un hash, quello che si e' detto per Claude web NON ESISTE.**
**Nessun «appena finisce, committo».**
**PERCHE' E' UNA RIGA E NON UNA NOTA:** il hook `commit-msg` di `P1-bis` guarda **i file toccati**,
non la chat — **sulla forma allargata non puo' impedire nulla** (`A9`). **Questa riga e' il presidio
che Luca vede a colpo d'occhio**, e un messaggio che ne e' privo si riconosce senza leggere il resto.
**NON e' un automatismo e va detto cosi':** e' un obbligo di forma, verificabile dal destinatario,
non dal sistema.


**P1-ter — UNA TABELLA DI NUMERI SI GENERA DA CODICE, MAI SI RICOPIA A MANO.**
Ogni tabella in un commit, in un referto o nel registro **si produce con uno script che legge il
file di dati, e se ne incolla l'output**. **Ricopiare a mano e' un'operazione senza presidio.**
**CASO REALE, 2026-09-21:** ricopiando a mano dal MIO STESSO file grezzo ho fatto **slittare due
righe** — al passo 600 i valori del 360, al 1080 quelli del 600 — **e su quella tabella ho scritto
una conclusione ROVESCIATA su `peq`** *(«cresce, non e' degenere» mentre CROLLA di 14 ordini)*.
**Se ne e' accorto chi ha letto il FILE invece del commit.** **Un numero ricopiato non ha
provenienza: uno generato ce l'ha.**

**P1-quater — OGNI SOSTITUZIONE DI TESTO SI ASSERISCE PER SE', MAI IN BLOCCO.**
Gli script che modificano file usano un helper che **conta l'ancora e fallisce se non e' unica**,
**una sostituzione alla volta**. **Un `assert` globale del tipo `t != originale` e' soddisfatto
dalle ALTRE sostituzioni e lascia passare in silenzio quella che non ha attaccato.**
**TRE VOLTE IN UN GIORNO, 2026-09-21:** ① **il driver** — `--scala-min` e `--coes-adim` parsati e
**mai inoltrati**, e il ramo D e' girato **1230 passi** con la configurazione sbagliata;
② **il sigillo dei flag**, nato con un euristico su finestra fissa; ③ **il hook di `P1-bis`**,
la cui correzione non ha attaccato mentre l'`assert` passava. **Riconoscerlo non e' bastato le
prime due volte: serve l'helper, non l'attenzione.**

**P1-quinquies — PRIMA DI SCRIVERE UN CLIP, UN PAVIMENTO O UN TETTO: `A11`.**
**Se protegge da un ERRORE, cerca l'errore.** Un limite e' ammesso solo se esprime un
**vincolo fisico dichiarato**; se sta li' per non dividere per zero, per non andare
negativo o per non esplodere, **il difetto e' altrove e il limite lo nasconde**.
**I sette corollari stanno in `doc/ASSIOMI.md`, `A11`**, ciascuno col difetto reale da cui
nasce. **Il piu' caro, misurato:** `max(peq, 1e-9)` ha trasformato un'anomalia di
**`-3.72`** in una di **`+1.805e+06`** *(`Z94`)* — **ribaltando il segno** — e ci sono
volute ore per trovarlo.

**P1-sexies — UN CRITERIO DI SIGILLO SI COLLAUDA SU UN CASO SINTETICO A RISPOSTA NOTA, PRIMA DI
APPLICARLO AL CODICE VERO.**
**Decisione di Luca, 2026-09-21.** Si costruiscono **due** casi con l'esito gia' noto — **uno che
DEVE passare e uno che DEVE fallire** — si verifica che il criterio dia quelle due risposte, e
**solo allora** lo si punta sul codice.
**PERCHE' E' UNA REGOLA E NON UNA RACCOMANDAZIONE: CINQUE CRITERI SBAGLIATI IN UN GIORNO**, e
**ogni volta il FAIL era del criterio, non della cura**:
| criterio | cosa sbagliava |
|---|---|
| **`Q6` (1a)** | confrontava i valori **dopo** il passo, quando il rilassamento li ha gia' mossi in **entrambi** i rami: `1.0000` contro `1.0000`, **assenza di CONTRASTO letta come assenza di effetto** |
| **`Q6` (2a)** | *«>= 100 volte»* una dispersione che a flag spento e' **ZERO ESATTO**: `100*0 = 0`, **passava con qualunque valore** |
| **`R3`** | pretendeva `bias == 0.0` **esatto** e falliva su **due ulp** di arrotondamento |
| **`R5`** | contava **25 aperture su 24 passi**: **l'iniezione del test apriva il freno lei stessa** |
| **`U3`** | confrontava con il mio **sviluppo** `e/2` invece del valore **esatto** `e/(2+e)`; il numero stampato, `0.952380952`, **era gia' `2/2.1`, cioe' la prova che il codice era giusto** |
**Il par.9 diceva gia' *«un criterio si scrive DA UNA MISURA, non dal proprio modello mentale»*.
Non e' bastato: `A9` dice che un presidio che non impedisce non e' un presidio.** Il collaudo su un
caso a risposta nota **impedisce**, perche' un criterio vuoto o troppo stretto **si denuncia sul
caso sintetico**, dove la risposta e' nota in anticipo.
**⚠ E IL CASO CHE DEVE FALLIRE E' IL PIU' IMPORTANTE:** quattro dei cinque errori qui sopra
sarebbero stati presi da un controllo *«questo criterio, su un caso che DEVE fallire, fallisce
davvero?»*.


**P2 — PRIMA DI ESCLUDERE UN FLAG DA UNA MISURA: FORZA IL SISTEMA O LO CORREGGE?**
Escludere un **forzante** (turbo) protegge la misura; escludere una **correzione** significa
**misurare un sistema che si sa difettoso**. (E' il presidio gia' scritto in §10, promosso qui
perche' e' comportamentale, non di componente.)

**P3 — NESSUNA STATISTICA SENZA BARRA D'ERRORE**, e per confronti **fra bracci** si usa la
**dispersione FRA SEMI**, mai la `SE` interna a un singolo run. Su questo sistema caotico la
pendenza trasversale cambia di **0.03 a codice INVARIATO**, contro una `SE` interna di **~0.010**
(§9, `doc/RAMIFICAZIONI.md` C10). **E per una barra fra semi servono >= 4 semi**: con 2,
`t(0.025,1) = 12.706` e l'IC95 e' inutilizzabile.

**P4 — PRIMA DI MISURARE SE UNA GRANDEZZA CAMBIA, VERIFICARE CHE SIA LIBERA DI CAMBIARE.**
Una quantita' normalizzata sulla propria mediana **non puo' muoversi**: misurarla e' un test vuoto
(§9, `doc/RAMIFICAZIONI.md` C12). Due casi reali: `_tau`/`_dens_rif` e `median(r)` in `ritmo()`.

**P5 — OGNI RAMO `else` / FALLBACK / `getattr(..., default)` SU UN PERCORSO FISICO VA CONTATO.**
Un fallback mai misurato e' un comportamento **sconosciuto**; uno che scatta l'80 % delle volte
**non e' un fallback: e' il comportamento principale** (C7: 71.88 %; C11: 95.33 %).

**P6 — OGNI CSV DI MISURA PORTA BLOB, SEME E TUTTI I FLAG** che distinguono quel run dagli altri
bracci dello stesso esperimento — non solo quelli che si pensava contassero. **Un file che si
distingue dagli altri solo per il NOME non e' un dato: e' un ricordo.** Non basta il log: il log si
perde, il CSV resta.

> **Come si usano.** P1 e' un **prerequisito di scrittura** (si applica prima di proporre); P2 e P6
> sono **check di preparazione** di un run; P3, P4, P5 sono **check di lettura** di un risultato.
> Se un run non soddisfa P6 in **ogni** campo, **non si conta**.

---


## 1. LA REGOLA D'ORO — UN INTERRUTTORE ALLA VOLTA
- **Tutto nel fork, tutti i flag nuovi OFF di default.** Un file, un branch. Completezza SENZA cecita'.
- Si accende **UN SOLO meccanismo per volta**, si sigilla, poi il successivo. MAI tutto insieme:
  con tutto acceso, ogni risultato (bello o brutto) e' ININTERPRETABILE.
- "Il core e' nuovo" NON e' una scusa per accendere tutto insieme. Un-pezzo-alla-volta non e'
  fedelta' al vecchio sistema: e' **diagnosticabilita'**. Vale anche in un universo nuovo.
- Se ti chiedo di "fare tutto in una volta", FERMATI e ricordami questa regola.


## 2. SIGILLI (rito obbligatorio, in ordine)
1. **Flag OFF = byte-identico** al comportamento precedente: `max|A-B| = 0.000e+00`. Se fallisce -> STOP.
2. **Riduzione al limite:** ogni strato torna a quello sotto nel limite (allineato / tau->0 / Hebb-off).
   NB: ridurre al VECCHIO scalare e' opzionale (compat all'indietro); ridurre allo strato SOTTO no.
3. **Purezza pure-read:** i diagnostici non mutano stato ne' RNG. Snapshot/restore COMPLETO
   (incluso lo stato dell'RNG) prima e dopo ogni misura: un run con/senza diagnostici byte-identico.
4. **Norma |psi|=1**, no NaN/inf. **Stabilita':** no runaway; per Hebb, `g <= G(rho)` sempre.
5. **Unitarieta' SU(2):** `U_ij^dag U_ij = I` preservata anche DURANTE l'evoluzione, non solo all'init.
6. **Gate ancorato al git-BLOB** (un commit puo' "mentire", un blob no). Verifica dal DISCO.
7. **Statistica:** nessuna conclusione sotto ~2000 passi, MAI su un solo seme. Un risultato su
   un seme e' baseline interna, non un fatto pubblicabile: serve robustezza su piu' semi.


## 3. ZERO MANOPOLE
- Nessun parametro nuovo tarato a mano. Le scale esistono gia': `tau = d/cs`, `G(rho)` con lo
  STESSO `GAMMA` di cs, `LAM`, `K_C`.
- Se ti accorgi di dover scegliere un numero nuovo per far funzionare qualcosa, **FERMATI e chiedi**:
  quasi sempre significa che ti sei fermato sul dito, o che il meccanismo va derivato, non tarato.


## 4. REGOLE FISICHE DA NON VIOLARE
- **U_ij resta in SU(2):** costruiscilo/evolvilo NELL'ALGEBRA di Lie (exp, slerp/geodetica), MAI
  come blend lineare di matrici (uscirebbe da SU(2)). Questo protegge unitarieta' **E**
  elettromagnetismo (la fase globale U(1)/segno vive separata: SU(2) ha det=1, non la tocca).
- **Freccia causale spinore -> link:** i nodi guidano, gli archi ricordano. Se in un test gli
  spinori diventano passivi (il link li comanda) -> BUG, da rilevare, non l'obiettivo.
- **Integratore:** VERLET (leapfrog) solo per il SECOND'ordine con inerzia (xddot: fasi, spinori,
  metrica). Per il RILASSAMENTO di primo ordine (xdot: memoria del gauge Strato 1/2) usa il passo
  ESATTO `U(t+dt) = U_target + (U-U_target) e^{-dt/tau}`, NON Verlet. Se ti chiedo Verlet su un
  rilassamento, segnalalo invece di eseguire.
- **`--cs-dinamico` CI VA SEMPRE (decisione di Luca, 2026-09-15).** Non e' un'opzione di scenario:
  **senza, `cs = CS_M` costante e `_cs_nodo_prev` non viene MAI scritta**, quindi cade anche il
  `tau = d/cs` dello **STRATO 1** (`_bloch_ritardato`), non solo quello di `--tau-luce`: **tutta la
  memoria del fork gira su una legge amputata.** Una misura senza `--cs-dinamico` **non misura il
  sistema che si crede di misurare**, ed e' successo (`doc/REPERTO_cs_dinamico_spento.md`).
  **NB, e non cambia la regola:** alle densita' simulabili `cs` varia pochissimo — misurato
  `cs \in [1.99954, 2.0]`, cioe' **0.023%**, che pesa **0.00629%** della dispersione di `tau = d/cs`
  (una parte su **15 898**). **Il punto non e' l'ampiezza: e' che la legge dev'essere CABLATA.**
  Un `cs` costante non e' un `cs` piccolo: e' un `cs` **assente**, e rende `tau = d/cs` un
  `tau ∝ d` travestito.
- **Dipendenza di flag:** `--cs-dinamico` implica `--chi-core` e `--spinore-vivo` (senza, e' inerte/incoerente).
- **Mai confronti a PASSO FISSO su un sistema che si espande/dilata:** genera ALIASING (una struttura
  che trasla o si dilata, campionata a intervalli costanti, sembra ferma o va a velocita' falsa).
  Campiona in modo adattivo o normalizza sulla scala (comovente), non su intervalli assoluti.
- **LOCALE PURA — niente sottrazione della media:** mai togliere la media globale (spinta.mean(),
  flusso.mean(), ...). La media globale introduce NON-LOCALITA' (una scorciatoia che il sistema
  relazionale non deve avere). Tutto agisce per arco/vicinato. La media NON va qui.


## 5. POLITICHE DI COMMIT
- **Commit PRIMA di ogni run** (riproducibilita'): il codice che genera un output dev'essere gia'
  committato quando l'output nasce.
- **Un commit = un cambiamento logico** (un flag nuovo, un pezzo, un fix). NON impacchettare piu'
  meccanismi in un solo commit: rompe la tracciabilita' del "quale pezzo ha fatto cosa".
- **Messaggio approfondito**, sempre, in questa forma: COSA e' cambiato / PERCHE' / COME /
  NUMERI (i risultati chiave del run) / COSA-RICONTROLLARE (i dubbi aperti).
- **Committa gli output col verdetto** (dati + eventuale grafico + esito del sigillo), anche senza
  averli guardati in dettaglio: servono a chi verifica.
- **Ogni commit = push.** Niente lavoro non spinto.
- **Niente `Start-Sleep` ne' polling** in run/script: le attese attive sprecano tempo e crediti.
- **Commit del sigillo:** quando accendi un flag, il commit deve riportare l'esito del sigillo
  (byte-identico OFF? riduzione al limite? stabilita'?). Se il sigillo FALLISCE, committa comunque
  lo stato + il fallimento e FERMATI: non "aggiustare al volo" dentro lo stesso commit.


## 5-novies. LE TRE COSE CHE SI AGGIORNANO **NELLO STESSO COMMIT** (regola di Luca, 2026-09-20)

> **① INVENTARIO · ② README · ③ FISICA.** **Nello stesso commit del cambiamento, mai «poi».**

**LA MISURA CHE LE MOTIVA, rifatta dal disco il 2026-09-20** *(e i numeri sono PEGGIORI di quelli
da cui il mandato partiva — `81/34/47` — perche' quel conto non includeva i sigilli)*:

```
strumenti  csv/_test_fork/*.py      79      in INVENTARIO   19   (24 %)   ->  60 MANCANTI
sigilli    csv/_seal_fork/*.py      45      in INVENTARIO    8   (18 %)   ->  37 MANCANTI
                                                                     TOTALE  97 MANCANTI
flag CLI   add_argument()           93      nel README      38   (41 %)   ->  55 MANCANTI
```
*(dai 79 strumenti sono escluse 5 COPIE del simulatore/driver — `*._sim.py`, `_driver_prima_*` —
che non sono strumenti e non vanno inventariate.)*

**L'inventario NON e' abbandonato: e' VIVO, aggiornato stamattina.** **Il difetto non e'
l'incuria, e' che l'aggiornamento dipende dal RICORDARSENE** — e `A9` dice che un presidio che
dipende dal ricordarsene non e' un presidio. **`Z31` e' gia' successo TRE volte, l'ultima dopo
essere stato citato due volte nella stessa sessione.**

### ① INVENTARIO — ogni strumento creato o modificato, nello stesso commit
Ogni file in **`csv/_test_fork/`** e **`csv/_seal_fork/`** che nasce o cambia aggiorna la sua voce
in **`doc/INVENTARIO_strumenti.md`**, con **quattro** cose:
- **il file**; - **il COMANDO che lo rigira, verbatim**; - **cosa misura**;
- **il BLOB su cui e' stato girato l'ultima volta** *(sha1 dei byte grezzi — **non**
  `git hash-object`: sono due numeri diversi per lo stesso file, par.5-quinquies)*.

**⚠ E IL TRIAGE NON E' BUROCRAZIA — inventariare una sonda come un sigillo GONFIA IL CONTO E
NASCONDE I SIGILLI VERI:**
```
SIGILLO                  -> voce COMPLETA: comando + blob + se e' ancora RI-GIRABILE
SONDA usa-e-getta        -> UNA riga che dice DOVE sta il referto
SONDA SENZA referto      -> ⚠ e' un REPERTO: una misura fatta e mai scritta
SIGILLO NON ri-girabile  -> ⚠ e' un `Z31` NUOVO, non un'omissione di inventario
```

### ② README — ogni flag o switch nuovo o modificato, nello stesso commit
Va nel **`README`** con: **cosa fa**, **il DEFAULT**, e **se e' byte-inerte a default spento**.
**Il default conta piu' della descrizione:** quando `STEP2_OROLOGIO` e' passato a ON di default,
*«l'assenza del flag»* ha smesso di significare OFF — e un `README` che non lo dice **converte i
rami di controllo in duplicati del ramo di prova**.

### ③ FISICA — ogni legge nuova, curata o riqualificata, nello stesso commit
Va riflessa nella **documentazione di fisica/matematica**: **la forma, la derivazione, il perche'**
— **non solo il registro dei difetti.** Il registro dice *«questo era rotto»*; la documentazione
di fisica dice *«questa e' la legge»*, e le due cose non si sostituiscono.
**Il rischio e' gia' occorso:** `62a03c7` — *«la relazione aveva la testa ferma al 16 SETTEMBRE»*,
**quattro giorni**, sul file che una sessione nuova rilegge **per primo**.

> **⚠ STATO DI QUESTE TRE REGOLE, e va detto qui perche' `A9` lo impone:**
> **oggi sono REGOLE SCRITTE, non presidi.** Nessuna di esse impedisce nulla.
> Il meccanismo che le renderebbe presidi e' **proposto e NON cablato**, in attesa di decisione:
> vedi **`doc/PROPOSTA_presidi_inventario.md`**.

---


## 5-bis. AUTO-MANUTENZIONE (tieni aggiornati i documenti vivi)
- **Aggiorna CLAUDE.md** quando cambia un FATTO stabile: un nuovo flag, un blob nuovo certificato,
  un fatto verificato dal codice, una regola nuova. CLAUDE.md deve restare vero. NON aggiornarlo per
  cose effimere (lo stato del task del giorno va nel file di STATO, non qui).
- **Aggiorna il file di STATO** (`STATO_CLAUDE_dev-spinoriale.md` o equivalente) a OGNI commit:
  dove siamo, quale strato, cosa manca, quale sigillo e' passato.
- Quando aggiorni CLAUDE.md o lo STATO, e' un commit dedicato con messaggio che dice cosa e' cambiato
  nelle regole/stato e perche'. Le regole si versionano come il codice.
- Se un fatto in par.9 si rivela superato dal codice, CORREGGILO qui (non lasciare un fatto stale:
  e' esattamente l'errore del docstring "ORFANO").


## 5-quinquies. IL CODICE DI UNA MISURA DEV'ESSERE RECUPERABILE **PER COSTRUZIONE** (regola di Luca, 2026-09-16)

- **`soliton_simulator.py` deve SEMPRE stare in uno di questi due stati, mai fuori:**
  1. **il blob sul disco coincide con quello COMMITTATO nel branch su cui si lavora** — cioe' il
     branch *e'* il codice che gira (**il caso normale, e quello da preferire**); **oppure**
  2. **accanto ai dati resta una COPIA ESATTA del file che ha girato**, committata **insieme** a
     quei dati.
- **Non e' una raccomandazione: e' CABLATA**, perche' una regola che dipende dal ricordarsene non
  e' un presidio. `csv/_test_fork/_osserva_vuoto.py` confronta il proprio blob con
  **`git rev-parse HEAD:soliton_simulator.py`** e, se differiscono, **scrive da solo**
  `<base>._sim.py` accanto all'output e lo dichiara nel log.
  **Le due strade della guardia sono state PROVATE ENTRAMBE** (2026-09-16): il ramo «committato»
  passa, e il ramo «non committato» scrive una copia il cui blob e' **identico** a quello del file
  che ha girato (`a435ebb8` = `a435ebb8`). *(Un fallback mai visto scattare e' un comportamento
  sconosciuto: par.9, presidio dei rami `else`.)*
- **Si confronta col BLOB A HEAD, mai con `git status`.** Un file puo' risultare «modificato» per
  sole newline e avere lo **stesso** blob; e puo' essere identico a un commit **vecchio** senza
  esserlo a HEAD. **Il blob e' l'unica identita' che non mente** (par.2.6), e vale per i
  **diagnostici** quanto per il simulatore -> `doc/INVENTARIO_strumenti.md`.
- **Perche' la regola esiste, e il caso reale che l'ha generata (2026-09-16):** MISURA G e' rimasta
  **non committata** mentre **quattro run la stavano gia' usando**. La riproducibilita' si e'
  salvata **solo** perche' nessuno ha toccato il file nel frattempo — **un fatto che dovevo
  ASSERIRE io**, mentre il par.5 esiste apposta perche' non debba asserirlo nessuno.
  **La copia automatica toglie l'asserzione di mezzo.**
- **⚠ LA TRAPPOLA CRLF, trovata dalla guardia stessa il 2026-09-16 — TRE stati, non due.**
  `core.autocrlf = true` e **nessun `.gitattributes`**: `git checkout` riscrive le newline
  **LF -> CRLF** sul disco, e `git hash-object` **non lo mostra**, perche' applica proprio il
  filtro `clean` che annulla la differenza. Quindi esiste un terzo stato:
  **stesso CONTENUTO, byte DIVERSI.**
  **Misurato:** un `git checkout -- soliton_simulator.py` ha portato il file da **435730 byte (LF)**
  a **442240 (CRLF)**, cambiando lo **sha1 dei byte grezzi** da **`08784685`** a **`37c31630`** —
  mentre `git hash-object`, `git rev-parse HEAD:` e persino `git diff` continuavano a dire
  **`08784685` / nessuna differenza**. *(E `git status` diceva `M` con `git diff` VUOTO: la conferma
  che `git status` non e' lo strumento giusto, come gia' scritto sopra.)*
  **La fisica e' la stessa — Python ignora le newline — ma il file NON e' piu' byte-identico a
  quello che i CSV citano col loro `blob`**, che e' calcolato sui **byte grezzi**.
  **PER RIPRISTINARE I BYTE ESATTI non si usa `git checkout`:** si usa
  `git cat-file -p HEAD:soliton_simulator.py`, scritto in **binario**. *(E' la stessa ragione per
  cui le copie storiche `_old_sim_pre_*.py` si estraggono in binario — par.9.)*
  **La guardia ora distingue i tre casi** e scrive il motivo in `<base>._sim.motivo.txt`, **su
  file e non solo a stdout**: dentro un sigillo lo stdout e' **catturato**, ed e' cosi' che un
  allarme vero diventa indistinguibile da uno spurio.
  **✅ RISOLTO, E QUESTA RIGA ERA STALE DA NOVE GIORNI — corretta il 2026-09-25.**
  La versione precedente diceva *«DA DECIDERE (Luca): un `.gitattributes`… **non l'ho
  aggiunto**»*. **E' STATO AGGIUNTO IL 2026-09-16, per decisione di Luca**, e copre `*.py`,
  `*.md`, `*.csv`, `*.txt`, `*.json` con **`text eol=lf`**, i binari come `binary`, e **se
  stesso**. Dal 2026-09-25 c'e' in piu' **`.githooks/* text eol=lf`**, perche' quei file
  **non hanno estensione** e sono script `#!/bin/sh`: su Linux un hook coi `^M` muore con
  `/bin/sh^M: bad interpreter`, e **un presidio che non parte e' peggio di uno assente**.
  **⚠ COME SE N'E' ACCORTO, e vale come lezione piu' della correzione:** il 2026-09-25 ho
  **SOVRASCRITTO** `.gitattributes` con un `cat >` **dandolo per inesistente**, e nel
  messaggio di commit ho citato **questa riga** come stato attuale. Il file c'era, con
  trentasette righe deliberate. Ripristinato da git (`2d98cd6`).
  **UN FATTO STALE QUI NON E' UN'IMPRECISIONE: E' UNA PREMESSA CHE QUALCUNO USERA' PER AGIRE**
  — e l'ho usata io, per cancellare un file. E' l'errore del docstring «ORFANO» (par.0),
  fatto **sul file che vieta di farlo** (par.5-bis).
- **Corollario, e va rispettato anche quando e' scomodo:** se un run e' partito col codice non
  committato, **la copia `._sim.py` va committata insieme ai dati**, non cancellata «tanto poi lo
  committo». Il file committato **dopo** ha lo stesso contenuto ma **non lo dimostra**.

### ⚠ DUE CONVENZIONI DI HASH, E NON SONO LO STESSO NUMERO (2026-09-20)

**`csv/_presidio.py` stampa `hashlib.sha1(byte_grezzi)` — SENZA l'intestazione git.**
**`git hash-object` calcola `sha1("blob <len>\0" + contenuto)`.**
**Sono DUE NUMERI DIVERSI PER LO STESSO FILE**, ed entrambi compaiono nei documenti di questo repo.

| file | sha1 GREZZO (timbro del presidio) | blob GIT |
|---|---|---|
| `_scena_video.py` prima della ripresa | **`f14ea4bd`** | `14d6f2c7` |
| `_scena_video.py` con la ripresa | **`7a02c5c3`** | `6d290089` |

**COME SI RICONOSCE L'ERRORE:** `git cat-file -t 7a02c5c3` risponde **`Not a valid object name`** —
non perche' il file non esista, ma perche' **quel numero non e' un oggetto git.**
**Per recuperare un file da un timbro del presidio si passa dal COMMIT, non dal numero:**
`git cat-file -p <commit>:<path>`.

**NON e' un difetto del presidio: e' la convenzione che il par.5-quinquies IMPONE**, perche'
`git hash-object` applica il filtro `clean` e puo' dire «nessuna differenza» su due file con byte
diversi (la trappola CRLF misurata il 2026-09-16). **Il presidio guarda i byte veri.**
**Quando si cita un blob, si dice QUALE DELLE DUE.**

### UN `.pkl` SENZA IL SUO COMANDO NON E' UN DATO

I `.pkl` NON si committano (binari, ~18 MB l'uno: git non li dimenticherebbe piu').
**Ma il sistema e' deterministico: il dato E' il comando che lo produce.**

**REGOLA, senza eccezioni:** ogni volta che un run produce un `.pkl`, **nello STESSO commit** va
scritto in `doc/INVENTARIO_strumenti.md`:
- **il nome del `.pkl`**;
- **la RIGA DI COMANDO COMPLETA** che lo rigenera, **verbatim**, tutti i flag inclusi;
- **il BLOB** del simulatore (`sha1` dei byte grezzi, **non** `git hash-object`: trappola CRLF, C18);
- **il BLOB dello script** che l'ha lanciato, se ce n'e' uno;
- **il SEME**, il numero di passi, e la data.

**Un `.pkl` prodotto e non documentato cosi' e' un dato che nessuno potra' rifare.**
E' la stessa famiglia di P6 (*«un file che si distingue dagli altri solo per il nome non e' un dato:
e' un ricordo»*), applicata a cio' che il repo non puo' contenere.

### PRESIDIO ENCODING — **lo stdout di Windows e' cp1252, e uccide gli script**

**Ogni script di sigillo o di misura DEVE cominciare con:**
```python
import sys as _sys_enc
try:
    _sys_enc.stdout.reconfigure(encoding="utf-8")
    _sys_enc.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
```
**`# -*- coding: utf-8 -*-` NON BASTA:** riguarda il **SORGENTE**, non lo **STDOUT**. Un singolo
`⚠`, `→` o `Δ` in un `print` fa morire lo script con `UnicodeEncodeError` — **dopo aver girato**,
buttando via il run.

**Perche' e' una REGOLA e non una raccomandazione: e' successo SETTE volte**, e la settima **allo
script che stava CONTANDO le occorrenze precedenti**. **Una nota che non impedisce il ripetersi non
e' un presidio.**

**COPERTURA REALE, e il numero va detto giusto perche' «74 su 74» suonava come «tutti»:** applicato
il 2026-09-17 a **63 script su 95** tracciati sotto `csv/` (escluse le **copie del simulatore**
`_old_sim_pre_*.py` e `*._sim.py`, che **non sono script** e non vanno toccate). I **74** erano le
famiglie `_seal_fork/` e `_test_fork/`, cioe' **gli strumenti in uso**; i **32 mancanti** sono di
campagne piu' vecchie (`_seal_53*`, `_seal_fase*`, `deparam_*`, `fase3_cov`). **Non e' copertura
totale, e chiamarla tale era un errore mio.**

> **⚠ QUESTO BLOCCO E' GIA' SUPERATO:** `csv/_presidio.py` (2026-09-17) fa la stessa cosa **piu'**
> il **timbro git** dello script, in **una riga**: `_presidio.avvia(__file__)`. Nei nuovi script si
> usa quello. La sostituzione nei 63 esistenti e' un **commit dedicato ancora da fare** (`Z22`).

---


## 5-octies. OGNI RESOCONTO SI COMMITTA E SI PUSHA, ANCHE A META' RUN (regola di Luca, 2026-09-18)

> **Un run che gira senza un resoconto pushato e' un run che, se la macchina si riavvia, NESSUNO SA
> CHE ESISTEVA.** **Non si aspetta la fine: se un run e' a meta', si committa quello che si sa a
> meta'** — cosa gira, da quando, cosa ha gia' prodotto, cosa manca.

**IL PRECEDENTE, ed e' di oggi:** il PC si e' riavviato durante il lavoro e **si e' perso SOLO il non
committato**. **E il commit `b84702b` dice «RUN FERMATO» senza dire A CHE PASSO era, ne' se i dati
parziali servissero** — ed e' esattamente il caso che questa prassi deve coprire.
**Vale anche, e soprattutto, per i run FERMATI e FALLITI.**

### IL MECCANISMO — `csv/_stato_run.py`, e cosa e' automatico e cosa NO

**Il registro e' `doc/STATO_RUN.md`, append-only, scritto AUTOMATICAMENTE:**
```python
import _stato_run as R
R.apri(nome, comando, note)     # ora + BLOB (sha1 byte grezzi, C18) + HEAD + COMANDO VERBATIM
R.tappa(nome, "frame 170/400, n 2391 -> 4120")        # avanzamento
R.chiudi(nome, "FINITO"|"FERMATO"|"FALLITO", "a che punto era, e se i dati parziali servono")
```

**⚠ DICHIARAZIONE ONESTA, e va letta PRIMA di chiamarlo presidio completo (Regola 9):**
- **AUTOMATICA e' la SCRITTURA.** Il file esiste **sempre**, quindi **dopo un riavvio lo stato si
  legge DAL DISCO invece che dalla memoria** — ed e' il 90 % del problema.
- **IL COMMIT NON E' AUTOMATICO, E NON PUO' ESSERLO IN MODO SICURO:** committare da dentro un run
  significherebbe fare operazioni git **mentre il run scrive**, e questo stesso file vieta
  `git add -A` con un run attivo, per una ragione che resta valida.
- **MA UN IMPEDIMENTO C'E', ed e' quello che rende la regola piu' di una nota:**
  **`apri()` RIFIUTA di partire se l'ultima voce e' ancora APERTA** *(salvo `forza=True`,
  che obbliga a dichiarare perche')*. **Non si puo' aprire un run nuovo lasciando il precedente
  senza esito.**

> **E' meno di un automatismo e piu' di un promemoria, e va detto cosi'** — la stessa onesta' che
> par.5-septies applica all'ordine del task history.

**REGOLA OPERATIVA:** `R.apri()` **prima** del lancio, `R.tappa()` a ogni snapshot/tappa,
`R.chiudi()` **sempre** — e **`git add doc/STATO_RUN.md && git commit && git push`** al primo
momento utile, **senza aspettare la fine del run**.

---


## 5-quater. IL REGISTRO DEI FRONTI APERTI (regola di Luca, 2026-09-15)
- **Lo stato dei fronti aperti sta in `doc/RAMIFICAZIONI.md`**, ed e' uno **STATO, non una cronaca**
  (la cronaca vive nei documenti di `doc/` e in `CLAUDECONNECT.md`).
- **Si aggiorna nello STESSO commit del riscontro che lo cambia** (par.5-bis): un registro aggiornato
  "dopo" e' un registro falso.
- **Le chiuse per DIMOSTRAZIONE e le chiuse per MISURA non si mescolano mai.** Le prime sono
  definitive; le seconde portano **sempre** la condizione che le renderebbe da rifare — e oggi
  quattro di esse sono misurate su un **settore ALIASATO** (~112 giri/passo), quindi **da rifare**.
- **Ogni voce ha un criterio di chiusura.** Una voce senza criterio non e' un fronte, e' un
  desiderio: va in una sezione a parte.
- **Un numero entra nel registro solo se e' gia' nel repo.** Il registro non e' il posto dove i
  numeri nascono.


## 5-ter. RELAZIONE A CLAUDE WEB — A OGNI RISCONTRO (regola di Luca, 2026-09-15)
- **A ogni riscontro di QUALSIASI tipo** — una misura, un'analisi, una simulazione, una lettura del
  codice, un sigillo che passa o che fallisce, una premessa che cade, un errore mio — **scrivi una
  RELAZIONE per Claude web con quello che hai VISTO, e committala e pushala.**
- **Subito, non a fine giornata.** Il riscontro si relaziona **nel momento in cui c'e'**, prima di
  passare al pezzo successivo. **Un riscontro non relazionato e' un riscontro perso:** chi legge il
  repo da fuori non ha la conversazione, ha solo i file.
- **Si scrive QUELLO CHE SI E' VISTO**, non quello che si spera: i NUMERI, con accanto il
  **valore-null / il riferimento** (par.9), e la provenienza (quanti semi, quanti passi, quale scena).
- **Valgono come riscontro anche, e soprattutto:** i risultati **negativi**, le ipotesi **refutate**,
  le premesse di un mandato che **non reggono al codice**, i **propri errori** e le **correzioni a
  fatti gia' scritti**. Non si relaziona solo quando funziona.
- **Dove:** un documento dedicato in `doc/` quando il riscontro e' un pezzo di lavoro, **PIU'** un
  paragrafo in `RELAZIONE_PER_CLAUDE.md`, cosi' chi legge solo quella e' comunque allineato.
- Vale **in aggiunta** a par.5 (politiche di commit) e par.5-bis (documenti vivi), non al loro posto:
  un riscontro che cambia un FATTO STABILE va **anche** in par.9, e lo stato **anche** nel file di STATO.


## 5-sexies. UNA DOMANDA SI COMMITTA COL SUO RAGIONAMENTO (regola di Luca, 2026-09-18)

> **Ogni volta che si pone una domanda a Luca — o si lascia una decisione aperta — TUTTO IL
> RAGIONAMENTO che ci porta va COMMITTATO E PUSHATO, nello stesso giro in cui la domanda viene
> posta.**

**Non e' un'estensione di par.5-ter, e' il suo caso piu' stretto.** par.5-ter dice di relazionare
ogni **riscontro**; questa dice che anche una **domanda** e' un atto da relazionare, perche':

- **la domanda arriva a Luca IN CHAT, ma la risposta si dara' fra ore o giorni, e in chat non c'e'
  piu' il ragionamento.** Chi risponde deve poter leggere **dal repo** perche' la domanda esiste,
  quali alternative sono state misurate, e con che numeri;
- **le domande sono ANCHE per Claude web**, che **non ha la conversazione: ha solo i file.** Una
  domanda che vive solo in chat, per lui, **non e' mai stata posta**;
- **e una decisione presa senza il ragionamento sotto e' una decisione presa al buio**, anche
  quando chi decide e' Luca.

**OPERATIVAMENTE, per ogni domanda o decisione lasciata aperta:**
1. **una voce nel registro** (`doc/RAMIFICAZIONI.md`) con **il criterio di chiusura** — cosa
   esattamente la deciderebbe (par.5-quater: una voce senza criterio non e' un fronte, e' un
   desiderio);
2. **un paragrafo in `RELAZIONE_PER_CLAUDE.md`** con **i numeri e le alternative gia' misurate**,
   non solo la domanda;
3. **commit + push nello stesso giro.** **Una domanda posta in chat e non pushata e' un riscontro
   perso**, esattamente come un risultato non relazionato.

**E vale anche per le domande che si RISPONDONO da soli:** se durante il lavoro nasce una domanda e
poi si trova la risposta, **va committato anche il percorso**, non solo l'esito. *(E' successo piu'
volte in questo repo che la strada scartata fosse piu' informativa della strada presa: le quattro
varianti del denominatore, le due rotture del punto 1, i tre nulli letti con risoluzioni diverse.)*

---


## 5-septies. IL TASK HISTORY — **il ragionamento si scrive PRIMA, e si committa PRIMA** (regola di Luca, 2026-09-18)

> **Quando si lavora a un task si seguono TRE passi, in quest'ordine:**
> **① RAGIONAMENTO PRELIMINARE · ② PROGETTAZIONE DEL RAGIONAMENTO · ③ entrambi scritti in un
> TASK HISTORY, col TODO del next step, COMMITTATO E PUSHATO.**

**Dove:** `doc/TASK_HISTORY/<AAAA-MM-GG>_<slug>.md`. La convenzione completa, col template e con
cio' che la regola NON e', sta in **`doc/TASK_HISTORY/README.md`**.

**Le tre sezioni, e cosa ciascuna deve contenere:**
1. **RAGIONAMENTO PRELIMINARE** — *cosa credo prima di guardare*: le premesse, cosa mi aspetto, e
   **cosa NON so**. **Non si riscrive quando si rivela sbagliato: si ANNOTA** con cio' che l'ha
   smentito. *(Un ragionamento riscritto a posteriori e' una ricostruzione, non un impegno.)*
2. **PROGETTAZIONE DEL RAGIONAMENTO** — *come intendo arrivarci*: i passi, **cosa decide ciascuno**,
   e **cosa mi farebbe FERMARE**. Le letture si fissano **qui**, prima di vedere i numeri.
3. **TODO DEL NEXT STEP** — la lista **operativa** del passo successivo, non un riassunto. **Si
   aggiorna nello stesso commit del riscontro che la cambia** (par.5-bis).

**IL RITO, ed e' il punto della regola: il task history si committa e si pusha PRIMA del lavoro**,
non insieme e non dopo. **Cosi' l'ordine e' VERIFICABILE DA GIT** — il commit del task history
dev'essere **antenato** dei commit del lavoro che descrive — **invece che asserito da me.**
E' **par.5 applicato al PENSIERO invece che al codice**: *«il codice che genera un output dev'essere
gia' committato quando l'output nasce»*.

**PERCHE' ESISTE, e sono casi di questo repo, non principi generali:**
- **la strada SCARTATA e' risultata piu' informativa di quella presa** — le quattro varianti del
  denominatore, le **due** rotture del punto 1 di `Z24`, i tre nulli letti con risoluzioni diverse;
- **un riavvio del PC** ha cancellato lo scratchpad e con esso il termine di paragone di **quattro
  sigilli** (`Z31`);
- **quattro errori di POPOLAZIONE in due giorni** sono stati trovati **rileggendo il proprio
  ragionamento**, non i risultati.

**NON duplica `doc/PREVISIONI_qualitative.md`:** le previsioni riguardano **l'esito di una misura**,
il task history riguarda **il PERCORSO** — e copre anche i task che **non hanno una misura**.

**⚠ DICHIARAZIONE ONESTA, per Regola 9:** la verifica da git e' un **CONTROLLO, non un
IMPEDIMENTO**. Non impedisce di scrivere il task history dopo e antidatarlo nel testo: impedisce di
farlo **senza che git lo mostri**. **E' meno di un meccanismo e piu' di una nota, e va detto cosi'**
invece di chiamarlo presidio.

**⚠ E UN LIMITE DA RIVERIFICARE:** non e' noto se la regola regga ai **task corti**. Un task da due
comandi potrebbe non meritare tre sezioni, e allora verrebbe **aggirata** — che e' il modo in cui le
regole muoiono. **CRITERIO: se in tre giri consecutivi un task salta il task history, la regola va
RIVISTA, non ignorata.**

---


## 6. STATO E ORDINE DEL LAVORO
Ordine: **prima il FORK (non-abeliano), poi il resto.** GAMMA / Step 2 (cs<->orologio) / verifica
EM<->curvatura sono A VALLE: non toccarli finche' il fork non gira (a densita' reali cs e' MORTO,
I~0.05 vs soglia ~400 -> tutti i test cs-dipendenti oggi sono NULLI).

Il fork si costruisce a strati (ognuno un flag OFF, ognuno si riduce a quello sotto):
- **STRATO 0 — connessione Berry statica (arc-connection): IL PRIMO MATTONE.**
  `U_ij = exp(-i (chi/2) m_hat . sigma)`, `chi=arccos(n_i.n_j)`, `m_hat=(n_j x n_i)/|n_j x n_i|`.
  Peso antipodalita': `w_ij = |n_j x n_i| = sin(chi)` (NIENTE soglia netta, NIENTE coeff. tarato).
  Sostituzione nella forza (`_coppia_interferenza`, righe 2207-2208): `Im<psi_i|psi_j> -> w_ij * Im<psi_i| U_ij |psi_j>`.
  Flag OFF (es. `FORK_SU2=False`). Sigillo: OFF -> byte-identico scalare; ON+allineati -> scalare.
- **STRATO 1 — connessione con MEMORIA (ritardazione): FATTO** (2026-09-14, flag `FORK_SU2_MEM`
  / `--fork-su2-mem`, OFF di default; sigillo `csv/_seal_fork/_sigillo_strato1.py`, **23/23 PASS**).
  Realizzato come **ritardazione dei BLOCH**, non come memoria della matrice: `_bloch_ritardato()`
  rilassa il versore `n_ret` verso quello corrente con **slerp geodetico** e
  `alpha = 1 - exp(-dt_n/tau)`, `tau = d_nodo/cs_nodo`. Si rilassa il Bloch e NON U/N perche' un
  blend lineare di matrici uscirebbe da SU(2) (par.4). Il trasporto resta sugli spinori CORRENTI.
  **E' il pezzo che ACCENDE il fork:** rompe il teorema di inerzia dello Strato 0 (vedi par.9).
  Riduce a Strato 0 per tau->0 (esatto, 0.000e+00) e a riposo (5.3e-15).
- **STRATO 2 — memoria hebbiana saturata (relazionale):** `dg/dt=c_ij*g*(1-g/G(rho))/tau`, tetto
  `G(rho)` legato alla DENSITA' col GAMMA di cs ("sorelle non catena": G da rho, NON da cs diretto).
  Riduce a Strato 1 per g=cost.

**FATTO STABILITO (non ri-derivare male):** il trasporto attuale e' SCALARE (righe 2207-2208, stessa A
applicata ad a e b) -> il sistema e' abeliano per STRUTTURA -> l'olonomia e' banale (W=2) qualunque
cosa facciano gli spinori on-site. **La dinamica sugli ARCHI (arc-connection) e' il pezzo mancante:
senza, non c'e' olonomia.** L'evoluzione on-site esistente (`SPINORE_VIVO`, `KURAMOTO_SU2`) e'
COMPLEMENTARE (fornisce stati di nodo variati da trasportare), non sostitutiva.


## 7. DOCUMENTI DI RIFERIMENTO (cartella `doc/` del repo)
`doc/BUSSOLA_dev-spinoriale.md` (perche'/dove-va) · `doc/BUSSOLA_TECNICA_dev-spinoriale.md` v2
(dove/come, formule, flag, sigilli) · `doc/ROADMAP_fork_SU2.md` (in-che-ordine) ·
`doc/PROTOCOLLO_test_olonomia.md` (come misurare W(r)) · `doc/SYSTASIS_nota_concettuale.md`
(il concetto). Leggili PRIMA di lavorare sul fork (vedi par.0-bis).
**E IL TERMINE DI PARAGONE: `doc/ASSIOMI.md`** — **DIECI voci** (A1-A10, piu' i corollari
A3b/A3c/A7b/A8b), aggiornato il 2026-09-18 con **A9** (*un presidio che non impedisce non e' un
presidio*) e **A10** (*una sola grandezza puo' legare due domini*). **Era gia' citato nel par.0-bis
di ogni mandato e NON era in questa lista: un documento che si deve leggere e che non compare fra i
riferimenti e' esattamente il difetto che A9 descrive.** **Tre voci su dieci sono METODOLOGICHE**
(A8, A9, e il corollario A3c) **e una e' un TEOREMA** (A6): la distinzione e' dichiarata nella
sezione `APERTO` del documento, e **va tenuta**.
**E i TRE REGISTRI, che sono STATO e non cronaca:** `doc/RAMIFICAZIONI.md` (i fronti aperti, par.5-quater) ·
`doc/COMPONENTI_PROMOSSE.md` (cosa e' fisica e cosa e' opzione, par.10) ·
**`doc/INVENTARIO_strumenti.md`** (QUALE script produce QUALE numero, **col blob di ogni script**:
un commit puo' mentire, un blob no — e vale per i diagnostici quanto per il simulatore).
NB: `ROADMAP_dev-spinoriale.md` (radice) e' la roadmap GAMMA/Step 2, A VALLE del fork (par.6).


## 8. PRINCIPIO GUIDA (per capire il "perche'")
"Lo spinore E' il tempo proprio della massa; da esso discendono l'interazione con la luce, con la
metrica, e l'aggregazione di spazio-tempo-materia." Ogni "-> nasce" e' un'IPOTESI da dimostrare
(derivazione, non innesto), non una rivendicazione. Verbo onesto: "dovrebbe emergere", non "genera".


## 9-bis. OGNI NUMERO PORTA LA SUA EPOCA (regola di Luca, 2026-09-21)

> **Ogni numero citato — in un referto, in un mandato, nel registro — porta la sua EPOCA.**
> **Un numero dell'epoca 1 non si usa come premessa per l'epoca 2.**
> **E' la stessa regola dei commenti scaduti, applicata ai DATI.**

**`EPOCA 2` = il blob del tag `epoca-2` (`4954fe5b`, byte grezzi) PIU' la configurazione con
`CHI_COOP`, `SCALA_MIN`, `COES_ADIM` ACCESI.** Sono **due** cose insieme: **un run a flag spenti
su quel blob e' ancora EPOCA 1**, e lo provano `Z1` e `Z1c` (byte-identici al simulatore di prima).

### ⚠ CORREZIONE DEL 2026-09-21 — **la frase qui sopra e' IMPRECISA, e la lascio leggibile**
**Cio' che avevo scritto:** *«un run a flag spenti su quel blob e' ancora EPOCA 1, lo provano `Z1`
e `Z1c`».* **VALE SOLO CON L'ARGV NUDO.**
**Perche' e' sbagliata:** `Z1c` confronta contro **«PRIMA + la cura del mondo»**, non contro
**«PRIMA»** — la cura e' innestata su ENTRAMBI i bracci di proposito, senno' il sigillo misurerebbe
LEI invece dei tre flag. **Quindi `Z1c` NON dice nulla sull'equivalenza con l'epoca 1.** A dirlo e'
`Z1b`, che misura la differenza: **`n` 2569 -> 2580, archi 527 308 -> 526 202.** La cura e'
**categoria D** e fa finalmente agire gli **otto** flag sul vuoto.

**LA CLASSIFICAZIONE CORRETTA, in quattro righe:**
```
EPOCA 1       blob PRECEDENTE al tag, qualunque configurazione

EPOCA 1       blob del tag, argv NUDO, tre flag spenti
              -> byte-identico, lo prova Z1

EPOCA 1-bis   blob del tag, argv del FORK, tre flag spenti
              -> NON e' epoca 1: e' epoca 1 CON LA CURA DEL MONDO.
                 Il vuoto nasce coi flag del run invece che coi default. Lo misura Z1b.

EPOCA 2       blob del tag + CHI_COOP, SCALA_MIN, COES_ADIM ACCESI
```

**⚠ LA CONSEGUENZA PRATICA, ed e' operativa:** **i run del FORK di epoca 1 NON si riproducono sul
blob nuovo, nemmeno a flag spenti** — **e NON E' UN DIFETTO.** Chi vuole rigirarli deve usare il
**blob PRECEDENTE** (`git cat-file -p <commit>:soliton_simulator.py`, scritto in BINARIO).

**Il tag NON si sposta e NON si riscrive:** un tag pubblicato che cambia sotto i piedi e' peggio
dell'imprecisione. La correzione vive qui e in una `git notes` sul commit del tag.


**DUE COROLLARI, entrambi nati da difetti misurati oggi:**
- **un'espansione che si vede come TENSIONE locale (`d/d0` che cresce) non e' espansione: e' un
  difetto.** **Un'espansione che dipende dal punto di riferimento ha un CENTRO: e' un difetto.**
- **l'epoca ritira le MISURE, non i DIFETTI.** Un difetto trovato leggendo il codice resta un
  difetto in epoca 2 **finche' il percorso che lo contiene gira ancora**. Nessuno si archivia
  perche' *«era del sistema vecchio»*.

**⚠ E IL CASO CHE HA GENERATO LA REGOLA, perche' non e' un principio astratto:** fino al
2026-09-21 il **vuoto** nasceva all'`import`, **prima** che i flag fossero applicati, e la
ricostruzione della rete era **condizionata** a `--seed`/`--nodi` — quindi non scattava mai nel
caso normale. **OTTO grandezze che la semina legge** *(`CALORE_VETTORIALE`, `CAMPO_SPINORIALE`,
`GAMMA`, `LAM`, `MAX_NODI`, `SCALA_AMP`, `SCALA_MIN`, `TAU_A`)* **sono state INERTI SUL VUOTO in
OGNI run di epoca 1, in silenzio.** Fra queste **`LAM` fissa `R_CONN = 3*LAM`, il raggio con cui
il vuoto si allaccia**, e **`CALORE_VETTORIALE` decide il calcio termico alla nascita** — e
`--calore-scal` e' in **ogni** comando del fork. **-> `Z88` del registro.**

---


## 10. PROMOZIONE DELLE COMPONENTI (regola di Luca, 2026-09-15)

**Perche' esiste.** Finche' una legge validata resta un flag opzionale, puo' essere **dimenticata**,
**esclusa per errore**, o **disattivata in silenzio**. Due casi reali, entrambi del 2026-09-15:
`--tau-luce` stava per essere escluso dalla prima misura vera del settore spinoriale perche' messo
nella stessa casella del turbo (**errore di categoria**: il turbo AMPLIFICA un parametro, `--tau-luce`
CORREGGE una legge) - intercettato **per fortuna, non per struttura**; e la **FASE 5 / doppia
copertura a 4pi** era cablata, sigillata e documentata, ed **inerte nel 95.33% delle chiamate**.

**Una componente sotto flag PUO' diventare fisica di default solo se soddisfa TUTTI E TRE:**
1. **DERIVATA, non tarata** - discende da un principio (causalita', coerenza dimensionale,
   conservazione) **senza coefficienti scelti**. Se serve un `K != 1`, **non e' promuovibile**.
2. **SIGILLATA** - byte-identita' a flag OFF, riduzione al limite, **e un sigillo che dimostri che FA
   QUALCOSA** (controllo positivo: *«con ON DEVONO differire»*). Un sigillo che verifica solo la
   byte-identita' a OFF **non prova che il flag serva**: passerebbe anche su codice morto.
3. **LA SUA ASSENZA E' UN DIFETTO, NON UN'ALTERNATIVA.** E' il criterio che separa davvero:
   *«il sistema senza X e' SBAGLIATO»* -> promuovibile;
   *«il sistema senza X e' DIVERSO»* -> **resta flag, per sempre.**
   **Non si riempie per inerzia:** *«e' sempre stato acceso»* **non e'** *«senza e' sbagliato»*.

**COME si promuove - si cambia il DEFAULT, non si cancella il ramo:**
- il flag diventa **ON di default**;
- resta un `--senza-<nome>` marcato **«DIAGNOSTICO, non fisica alternativa»**, per gli A/B;
- **il gate certifica il comportamento ON.**
Cancellare il ramo vecchio farebbe perdere la capacita' di **misurare cosa fa quella legge**, che e'
servita piu' volte (ogni sigillo di byte-identita' vive di quel ramo). Promuovere il default la
conserva.

**RETROCESSIONE:** una componente promossa torna a flag **solo** con un riscontro **committato** che
ne mostri un difetto - **mai per ripensamento**. La voce nel registro porta il criterio che la
farebbe retrocedere, scritto **al momento della promozione**, non dopo.

**TRE CATEGORIE, e non si mescolano:**
- **FISICA CERTIFICATA** - ON di default, spegnibile **solo** come diagnostico;
- **ESPERIMENTI** - OFF di default **sempre**: turbo, Kuramoto, e ogni meccanismo **aggiunto a mano**
  invece che derivato;
- **CORREZIONI DI DIFETTO** - **nessun flag**, gia' nel codice. **Un bug curato non ha un
  interruttore** (la cache `_cs_nodo_prev`, `_psi_spin_prec`). Metterle fra le candidate sarebbe un
  errore di categoria: non sono leggi, sono riparazioni.

- **PRESIDIO - PRIMA DI ESCLUDERE UN FLAG DA UNA MISURA, CHIEDITI: FORZA IL SISTEMA O LO CORREGGE?**
  Escludere un **forzante** (turbo) protegge la misura; escludere una **correzione** significa
  **misurare un sistema che si sa difettoso**. *(Precedente: `--tau-luce` escluso come se fosse il
  turbo, 2026-09-15. La prima misura vera del settore spinoriale stava per essere fatta alla
  risoluzione peggiore disponibile: `theta ~ 96` giri/passo invece di ~43.)*

**LO STATO DI OGNI COMPONENTE STA IN `doc/COMPONENTI_PROMOSSE.md`**, e si aggiorna **nello stesso
commit** del riscontro che lo cambia (par.5-bis).
**NB verificato dal disco il 2026-09-15 (blob `08784685`): il file ha 51 flag booleani di modulo, di
cui 10 gia' a `True`** - fra questi `TAU_A_LOCALE`, marcato **«IN VERIFICA»** nel suo stesso
commento e **senza flag da riga di comando**. Cioe': **esiste gia' uno strato di componenti accese di
default che non e' mai passato per questi tre criteri, perche' i tre criteri non esistevano.**
Il registro serve prima di tutto a **rendere visibile quello strato**, non solo a governare le
promozioni future.

---


## 11. L'INDICE DEI DIFETTI: COME SI USA *(dal 2026-09-26)*

- **LA FONTE E' `doc/INDICE_ID.tsv`** — un TSV di **13 colonne**, e **non ce n'e' un'altra**.
- **colonne:** `id` · `alias` · `titolo_breve` · `fonte_principale` · `stato` · `blocca_run_base` · `tipo` · `famiglia` · `stato_da` · `avanzamento` · `revisione` · `motivo` · `nota`
- **`stato`:** `aperto` | `chiuso` | `non-difetto` | `teoria` | `da-decidere`
- **`blocca_run_base`:** `SI` | `NO` | `DA-DECIDERE` | `DA VERIFICARE`
- **`tipo`:** `difetto` | `sospetto` | `fronte` | `misura` | `cura` | `presidio` | `assioma` | `standard` | `criterio-locale` | `altro` · **`famiglia`:** `A`-`G` oppure `?` · **`avanzamento`:** `FATTO` | `IN CORSO` | `IN CODA` | `BLOCCATO` | `CON RISERVA` | `(senza marcatore)`
- **UN DIFETTO NUOVO = UNA RIGA NELL'INDICE**, piu' la spiegazione lunga in `doc/STATO_RUN.md` **con lo STESSO ID**. **MAI IL CONTRARIO:** un ID nuovo in un documento vivo **senza la sua riga** viene **RIFIUTATO dal hook**.
- **`blocca_run_base = SI` RICHIEDE `motivo`** *(la prova in una frase)*: **una decisione senza prova non passa il validatore.**
- **LE VISTE SI GENERANO, NON SI MODIFICANO A MANO:**
  `python csv/_lista_chiusa.py` · `python csv/_vista_smistamento.py` · `python csv/_punto_della_situazione.py`
- **IL VALIDATORE:** `python csv/_indice_id.py` *(e `python csv/_indice_id.py --collaudo`)*. **Gira da solo nel `pre-commit`**: schema, vocabolari, ID unici, coerenza `stato`/`blocca`, `motivo` dove serve, **e nessuna voce persa rispetto al tag**.
- **COSA BLOCCA IL RUN BASE** si legge in **`doc/SMISTAMENTO_run_base.md`** *(gli `SI`, in ordine di lavoro)*; **il PERCHE' di ogni `SI`** sta in **`doc/REVISIONE_SI_2026-09-26.md`**, che separa ✅ *verificato sul codice* da 🟨 *misura di Luca* da 🧠 *inferenza*.
- **LA LISTA E' CONGELATA al tag `lista-chiusa-v1`: SI SPUNTA, NON SI RIGENERA.** L'importatore che la costruiva dal Markdown e' in **`csv/_archivio/_indice_id_importatore.py`** e **NON si rilancia** *(rilanciarlo sovrascriverebbe la fonte con una ricostruzione, buttando via le decisioni scritte nelle colonne)*.
