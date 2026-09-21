# CLAUDE.md — soliton_simulator (branch dev-spinoriale)

Istruzioni autorevoli per Claude Code su questo repo. Valgono per ogni sessione.
Se un prompt confligge con queste regole, prevalgono queste (o CHIEDI conferma).

---

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
**senza toccare anche `RELAZIONE_PER_CLAUDE.md`**. Si installa con
`python csv/_hook_relazione.py --installa`.
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
  **DA DECIDERE (Luca):** un `.gitattributes` con `soliton_simulator.py text eol=lf` toglierebbe
  la trappola alla radice. **Non l'ho aggiunto: cambia il comportamento di git su tutto il repo.**
- **Corollario, e va rispettato anche quando e' scomodo:** se un run e' partito col codice non
  committato, **la copia `._sim.py` va committata insieme ai dati**, non cancellata «tanto poi lo
  committo». Il file committato **dopo** ha lo stesso contenuto ma **non lo dimostra**.

### ⚠ DUE CONVENZIONI DI HASH, E NON SONO LO STESSO NUMERO (2026-09-20)

**`csv/_presidio.py` stampa `hashlib.sha1(byte_grezzi)` — SENZA l'intestazione git.**
**`git hash-object` calcola `sha1("blob <len> " + contenuto)`.**
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

## 9. FATTI VERIFICATI DAL CODICE (per non rifare errori gia' fatti)
- **LE RIGHE CITATE QUI SOTTO SONO SHIFTATE: il blob e' cambiato** (2026-09-15). Il cablaggio di
  `TAU_LUCE` e il fix della cache hanno spostato tutto cio' che sta dopo la riga ~810. Vale il par.0
  (*cerca per NOME di funzione/flag, non per riga*), ma poiche' le righe **sono** citate ovunque,
  ecco la conversione, **generata confrontando i TRE blob riga per riga** (`git cat-file`), non per aritmetica: un `-` significa che la stringa non esiste in quel blob. **RIGENERATA il 2026-09-15 dopo che tre righe, calcolate a mano per differenza, erano sbagliate.** I numeri storici **non sono stati
  riscritti** nelle voci: li' dicono a quale blob si riferivano, ed e' un'informazione, non un errore.

  | punto | `f5887254` | `b298677a` | **ORA (`08784685`)** |
  |---|---|---|---|
  | commento stale "si conserva, non rilassa" | 868 | 901 | **901** |
  | commento stale "omega si CONSERVA" | 1803 | 1852 | **1864** |
  | rumore sul Bloch (`amp[:, None]`) | 1847 | 1896 | **1908** |
  | `nb_vic = self._nb_prec` | 1856 | 1905 | **1917** |
  | `inerzia = np.maximum(_rho_sorgente(), 1e-6)` | 1891 | 1940 | **1952** |
  | `correzione = np.cross(B, nb)` | 1895 | 1944 | **1956** |
  | `correzione += cross(_nb_grav(), nb)` | 1901 | 1950 | **1962** |
  | `_tau = TAU_A * max(_dens/_dens_rif, 0.05)` | 1913 | 1967 | **1979** |
  | **il rilassamento** `- omega_src/_tau` | 1918 | 1972 | **1984** |
  | `calcio_omega` dentro `semina()` | 1593 | 1642 | **1654** |
  | **la guardia 4pi** `len(_ps) == self.n` | 1780 | 1829 | **1841** |
  | scrittura di `_psi_spin_prec` | 2555 | 2647 | **2659** |
  | guardia `len(csp) >= n` in `_tempo_luce_nodo` | 2435 | 2565 | **2577** |
  | scrittura della cache `_cs_nodo_prev` | 2826 | 2918 | **2930** |
  | trasporto SCALARE `mat(A)@_a` | 2531 | 2623 | **2635** |
  | `cs_floor` | 2382 | 2436 | **2448** |
  | `def _eredita_spinore_figli` | 1133 | 1170 | **1170** |
  | mitosi -> `_eredita_spinore_figli(a)` | 3125 | 3217 | **3229** |
  | Schwinger -> `_eredita_spinore_figli(aa, -1)` | 3242 | 3334 | **3346** |
- Trasporto forza = SCALARE: `_coppia_interferenza`, **righe 2207-2208**
  (`np.conj(_a)*(mat(A)@_a) + np.conj(_b)*(mat(A)@_b)`, stessa A su a e b) -> abeliano per
  struttura. VERIFICATO dal sorgente
  sul blob 4fc7a794 il 2026-09-13. **La riga 2196 citata in passato era il DOCSTRING, non il codice**
  (la funzione inizia a 2192, il docstring occupa 2193-2200): errore da par.0, corretto.
- cs = CS_M/(1+GAMMA*sqrt(I)) (riga 2187, `cs_floor`): vive SOLO nel settore metrica/gravita', MAI
  nell'orologio/EM. VERIFICATO dal sorgente il 2026-09-13.
- Orologio/EM (`_phc`, `omega_clk`, `ritmo()`, `dt_n=DT*r`): NON usa cs. Due tempi propri scollegati
  (metrico tau_p=d/cs vs orologio dt_n=DT*r). L'accoppiamento cs<->orologio e' lo Step 2 (non fatto).
- `_passo_spinoriale`: NON orfano (docstring stale), cablato dietro `SPINORE_VIVO` (OFF). E' ON-SITE
  (precessione dello spinore del nodo con memoria hebbiana + inerzia |Psi|^2), NON arc-connection.
- `PLAST_MIT=0` in TUTTI i test committati: la "compressione" osservata e' il regime di default
  (dimezzamento d0=d/2, "compressione degenere"), NON la generazione di spazio (mai girata).
- **`FORK_SU2_MEM` / `--fork-su2-mem` (STRATO 1, 2026-09-14):** la connessione `N_ij` si costruisce
  dai Bloch RITARDATI `self._nb_ret` invece che da quelli correnti. Metodo `_bloch_ritardato()`;
  stato per-nodo `_nb_ret` (ereditato dalla mitosi in `_eredita_spinore_figli`), cache
  `_cs_nodo_prev` e `_r_corrente` **scritte solo col flag ON** (da cui dipende la byte-identita'
  di S1: se un giorno servissero a ramo spento, il sigillo S1 va rifatto). Richiede `--fork-su2`;
  da solo viene IGNORATO con avviso. VERIFICATO dal sorgente sul blob 2277e9a0.
  **✅ MARCHIO TOLTO IL 2026-09-16 — `tau` SEGUE `cs`, MISURATO. Il sigillo e' ora 25/27 PASS + 2
  FAIL ATTESI** (`csv/_seal_fork/_sigillo_strato1_risigillo_2026-09-16.txt`, blob `08784685`,
  **con `--cs-dinamico`**). Il marchio qui sotto e' **storico**: si legge per sapere **com'era** e
  **cosa lo ha tolto**, non come stato attuale.
  **COSA LO HA TOLTO: il SIGILLO 8, scritto apposta perche' rilanciare il sigillo com'era NON
  SAREBBE BASTATO.** Nei test in-process `_cs_nodo_prev` era `None` o `np.full(nodi, cs)`, cioe'
  **COSTANTE**: un `cs` costante non esercita `tau = d/cs`, lo rende indistinguibile da `tau ∝ d`.
  S8 da' a quattro nodi **`cs = 1, 2, 4, 8`** con **tutto il resto identico** (stessa `d`, `r = 1`
  su tutti — l'**opposto esatto** di S7, che varia `r` e tiene `cs` fisso):
  * **S8** `alpha = 1-exp(-dt_n*cs/d)` per nodo -> `max|alpha_mis - alpha_atteso| = 2.550e-15`;
  * **S8b** rapporto `cs=8 / cs=1` = **7.660686976** misurato = atteso — **se `cs` fosse ignorato
    varrebbe ESATTAMENTE 1.000000000**, come il `r=2/r=1` col bug del `DT` nudo;
  * **S8c** `|rapporto - 1| = 6.661`; **S8d** controprova con `cs` COSTANTE -> `alpha` uguale per
    tutti (`3.816e-16`), cosi' S8 non puo' passare per un artefatto dello slerp.
  **I DUE FAIL SONO S1a/S1b, PREVISTI E COMMITTATI PRIMA** (`doc/PREDIZIONE_risigillo_strato1.md`,
  commit `2853b36`): fra il blob di riferimento `968fba34` e `08784685` c'e' **C11**, che **non e'
  gated su `FORK_SU2_MEM`** — nel codice nuovo l'orologio a 4pi e' attivo, nel vecchio era inerte
  al 95.33 %. Due orologi -> due `r` -> due `dt_n` -> traiettorie diverse -> `N` diverso (**3096
  contro 3020, 32 array su 32 con shape diversa**). **Il `max|A-B| = 0.000e+00` stampato accanto a
  quei FAIL e' MANCANZA DI CONFRONTO, non identita'.** **NON e' una regressione: e' una cura che ha
  fatto il suo mestiere.** **E il sigillo si cita cosi': «25/27 PASS + 2 FAIL ATTESI», MAI «23/23».**
  **⚠ E COSA S8 *NON* DICE:** che `tau = d/cs` sia **fisicamente** distinguibile da `tau ∝ d` nei
  run veri. **Non lo e'** (C13: `cs_std/cs` fra **0.0086 %** e **0.24 %**, sempre sotto l'1 %).
  **S8 prova che la LEGGE e' cablata e viva; C13 dice che alle densita' simulabili quella legge ha
  poco da dire.** Due affermazioni diverse, nessuna sostituisce l'altra.
  **Sullo stesso ri-sigillo e' emerso un difetto grosso: vedi la voce «IL SIGILLO SI SCHIANTAVA».**

  **⚠ MARCHIO STORICO (2026-09-15, rilievo di Luca, verificato dal disco) — TOLTO il 2026-09-16,
  vedi sopra: il sigillo 23/23 dello STRATO 1 NON AVEVA MAI ESERCITATO LA DIPENDENZA DA `cs`.** L'argv di `_sigillo_strato1.py` (righe 380-386)
  **non contiene `--cs-dinamico`**, quindi `cs = CS_M` costante e `_cs_nodo_prev` non veniva scritta:
  il ritardo girava su **`tau = d/CS_M`**. E vale **due volte**: quel sigillo e' del blob `2277e9a0`,
  **precedente alla cura della cache**, quindi anche col flag acceso la cache sarebbe stata
  **scartata a ogni mitosi**.
  **COSA RESTA VALIDO:** il **meccanismo** del ritardo (slerp geodetico, `alpha = 1-exp(-dt_n/tau)`)
  e **S7**, che misura il rapporto `r=2 / r=1 = 1.9753` — quel rapporto dipende da **`r`**, non da
  `cs`, quindi il presidio sul tempo proprio **tiene**.
  **COSA NON E' MAI STATO TESTATO:** che `tau` **segua `cs`**. Ed e' proprio la ragione per cui
  `tau = d/cs` sarebbe piu' principiato di `tau ∝ rho`. **Finora nessuno l'ha vista funzionare.**
- **IL TIC DEI PROCESSI LOCALI E' `dt_n = DT*r`, NON `DT`** (fatto generale, non solo del fork).
  `DT` nudo e' il tempo di COORDINATA: usarlo dentro un rilassamento locale cancella la dipendenza
  dall'orologio del luogo, cioe' impone la foliazione sincrona globale = **un frame preferito, un
  "etere"**. Tutta la fisica del file integra gia' in `dt_n`/`dt_e` (phivel, tw); `DT` nudo vive
  solo nel conteggio dei sottopassi CFL. Preso una volta nello Strato 1 (bug dell'istruzione, non
  dell'esecuzione) e corretto. **Presidio permanente: il sigillo S7** (`_sigillo_strato1.py`), che
  misura `alpha` su nodi con ritmi diversi: con `dt_n` il rapporto r=2/r=1 vale 1.9753, col `DT`
  varrebbe esattamente 1.000. S1..S6 passavano IDENTICI col bug: senza S7 era invisibile.
- **PRESIDIO PERMANENTE — PRIMA DI LEGGERE UNA STATISTICA RIASSUNTIVA, CHIEDITI CHE VALORE
  AVREBBE SE NON CI FOSSE NIENTE** (il valore sotto ipotesi nulla). Costa due righe e ferma gli
  autoinganni piu' comuni. Casi reali gia' presi su questo repo:
  * `N = 3164 -> 3209` a 150 passi sembrava un effetto del fork: era rumore a 1e-16 amplificato dal
    caos (2026-09-13). Sotto ipotesi nulla, due run che divergono a 1e-16 danno ESATTAMENTE quello.
  * `max|A-B| = 0.000e+00` sembrava identita': era mancanza di confronto, 3209 nodi contro 3073
    (2026-09-14). Sotto ipotesi nulla di "nessun array confrontabile", il massimo di un insieme
    vuoto e' 0.
  * `spin_overlap = 0.5000` e `chi ~ 90 +- 39 gradi` NON sono numeri qualunque: sono **esattamente**
    i valori di direzioni di Bloch CASUALI (`<|<psi_i|psi_j>|^2> = (1+<cos chi>)/2 = 0.5`;
    `sin(chi)/2` ha media 90.000 e std 39.171 gradi). Chi li vede deve riconoscerli.
- **PRESIDIO — QUANDO SI APRE UNA DOMANDA NUOVA, RI-INTERROGA LE MISURE VECCHIE.** Una misura letta
  correttamente per la domanda di allora puo' essere DECISIVA per una domanda posta mesi dopo, e
  nessuno torna a chiedergliela. Caso reale: `spin_ovl = 0.5 (direzione random)` fu misurato e letto
  BENE a 800 passi (verdetto (B) abeliano = disordinato, `STATO:513`); ma diceva gia' che il fork
  SU(2) avrebbe cercato struttura su un substrato senza struttura, e quella conseguenza e' stata
  tratta solo il 2026-09-14. Non tutte le risposte arrivano da run nuovi.
- **PRESIDIO — UN PATTERN CHE SPIEGA TUTTO VA VERIFICATO CONTRO LA FONTE PRIMA DI SCRIVERLO.**
  Nel primo audit (2026-09-14) l'esecutore ha costruito un reperto inesistente ("il segnale era nei
  dati e nessuno l'ha visto") cercando un terzo episodio che completasse uno schema: bastava leggere
  `STATO:513` per intero per vedere che il segnale era stato visto e annotato. **L'entusiasmo per uno
  schema elegante e' una fonte di errore quanto la disattenzione.**
- **TRAPPOLA DI LETTURA (2026-09-14): `max|A-B| = 0.000e+00` puo' significare "nessun confronto".**
  Se due run divergono al punto di cambiare il NUMERO DI NODI, nessun array ha piu' la stessa
  shape, il confronto non ha nulla da confrontare e lo zero e' MANCANZA DI CONFRONTO, non
  identita'. (Misurato: Strato 0 = 3209 nodi, Strato 1 = 3073, 32 shape su 32 divergenti.)
  E' il gemello speculare del falso positivo del 2026-09-13. **Guardare SEMPRE prima la riga delle
  shape / del conteggio nodi.**
- **EREDITA' ALLA MITOSI = COPIA ESATTA (verificato dal codice, 2026-09-15, blob f5887254).**
  `_eredita_spinore_figli` (righe ~1133-1170) copia dal padre `src` SENZA perturbazione: `_nb`,
  `_nb_prec`, `_nb_ret`, `omega_s`, `_psi_spinor`, `_spinor_lift`, `_psi_prec`. Il figlio nasce al
  PUNTO MEDIO dell'arco (riga ~3094) con ESATTAMENTE due archi, verso entrambi i genitori (righe
  ~3172-3173). **Conseguenza: ogni nascita crea una coppia con chi = 0** (misurato 0.0000 esatto).
  **La parentela NON e' registrata** (gli unici `parent` del file, righe ~949-982, sono lo
  spanning-tree dei cicli, non genealogia) **ma e' RICOSTRUIBILE in volo**: il padre `a` sta nel
  lato `i` dell'arco `(a, m)`. Misurato 100% su 7/7 e poi su 4163 coppie.
  NB: l'antinodo Schwinger (riga ~3242) eredita `-psi`, ma `nb = psi^dag sigma psi` e' INVARIANTE
  per fase globale: **anche l'antinodo nasce con chi = 0 in Bloch**. "Antichirale" riguarda il segno
  di doppia copertura, NON la direzione.
- **SOTTO `--spinore-corretto` IL RUMORE NON TOCCA IL BLOCH DIRETTAMENTE** (verificato dal codice,
  2026-09-15). Il ramo additivo sul Bloch/spinore (righe ~2060, ~2085) e' gated su `SYNC_UPDATE`,
  che e' SPENTO in tutti i run del fork; il `_nb` committato e' DERIVATO da `_psi_spinor` (righe
  ~2066-2069, ~2088). Il rumore entra SOLO via `correzione = cross(B, nb)` -> `omega_new`: e'
  **rumore di COPPIA, non di posizione sulla sfera**.
- **IL SETTORE DI SPIN NON E' RISOLTO NEL TEMPO DAL PASSO DT** (misurato 2026-09-15,
  `doc/BILANCIO_ordine_spin.md`; UN seme, UNA scena, passo 60: da riconfermare). `omega_s` letto
  direttamente dal simulatore da `theta = |omega_s|*dt_n` mediana **2.4e4 GRADI per passo = ~67 giri
  interi**, 99.3% dei nodi oltre il giro. Non c'e' clamp su `theta` (righe ~2033-2037).
  CAUSA: `inerzia = np.maximum(_rho_sorgente(), 1e-6)` (riga 1891) con densita' mediana **1.21e-07**
  -> il pavimento e' attivo sul **99.7%** dei nodi, e `omega = coppia/inerzia` ~ 6e4 mentre la coppia
  e' ORDINARIA (0.06). **Il pavimento 1e-6 NON e' la causa: la MITIGA** (senza, omega sarebbe otto
  volte maggiore). **E' LA STESSA RADICE di "a densita' reali cs e' MORTO" (par.6), con segno
  opposto:** la densita' minuscola CONGELA la metrica e FA ESPLODERE lo spin.
  CONSEGUENZA DI LETTURA: le misure negative sul settore di spin restano valide, ma NON dicono "non
  esiste una fisica ordinante": dicono "in questo regime numerico nessun ordine sopravvive a un tick".
- **ATTENZIONE, DUE COMMENTI STALE SU `omega_s`** (verificato 2026-09-15): le righe **868**
  (*"motore conservativo: si conserva, non rilassa"*) e **1803** (*"omega si CONSERVA, non insegue
  lo zero"*) dicono il FALSO. L'UNICO aggiornamento per passo e' la riga **1918**, che contiene
  **`- omega_src/_tau`**: e' un rilassamento del primo ordine, con
  `tau = TAU_A * max(rho/rho_rif, 0.05)`. **La dissipazione su `omega_s` ESISTE.** Chi legge solo i
  commenti costruisce una diagnosi sbagliata (e' successo: vedi `doc/ANALISI_gilbert_fdt.md` par.1).
  NB anche: il calcio termico `calcio_omega` (righe 1592-1594) e' DENTRO `semina()`, quindi e' il
  punto zero ALLA NASCITA del nodo, **non** una sorgente di rumore per passo.
- **PIU' MEMORIA SU `omega_s` = PIU' ROTAZIONE, non piu' ordine** (riga 1918; misurato 2026-09-15).
  **CORRETTO il 2026-09-15** — la versione precedente di questo punto diceva
  `omega_eq = tau * coppia/inerzia` (proporzionale a `tau`): e' il punto fisso DETERMINISTICO, che
  varrebbe se la direzione della coppia fosse coerente. **Non lo e'.** La traiettoria misurata
  (`csv/_test_fork/_crescita_omega.py`, 150 passi, 15 punti) dice che `|omega_s|` cresce come
  **`sqrt(n)`** (`omega/sqrt(n)` costante entro il **4.6%**, mentre `omega/n` varia di 3.5x): e' un
  **RANDOM WALK SMORZATO**, e il suo equilibrio e'
  **`omega_eq = |F| * sqrt(dt_n * tau / 2)`, cioe' proporzionale a `sqrt(tau)`, non a `tau`**.
  Misurato: previsto 7.06e4, osservato 7.27e4 al passo 150 (scarto x1.03), con la decelerazione
  visibile (x1.138 da n=100 a n=150 contro x1.225 del puro sqrt(n)).
  **LA CONCLUSIONE RESTA:** omega cresce con la memoria (come `sqrt(tau)`), la memoria vive sulla
  VELOCITA' ANGOLARE e conserva la ROTAZIONE, non la DIREZIONE, e il plateau vale comunque
  **112 giri per passo**. **L'ipotesi "dare memoria combatte il disordine" e' REFUTATA.**
  **E LA DISSIPAZIONE NON MANCA: c'e', e' efficace, e un plateau finito lo produce gia'.** Il
  problema e' DOVE sta quel plateau, e dipende dall'INGRESSO (coppia/inerzia), non dall'uscita.
  **L'ipotesi "dare memoria combatte il disordine" e' REFUTATA su questo canale.**
  NB: `--regime` NON serve a testare TAU_A: cambia TAU_A INSIEME a G_PH, _CALORE_INIT e SCUOTIMENTO
  (quattro interruttori insieme, contro par.1).
- **BILANCIO DEI TASSI (misurato, 2 semi, 4163 coppie, 2026-09-15):** `tau_dec` (decorrelazione di
  una coppia padre-figlio) = **0.63 passi** su ENTRAMBI i semi; `tau_mit` locale = 187 / 210 passi
  -> rapporto **295 / 335**. **Dominio della distruzione.** Il confondente geometrico e' ESCLUSO,
  non stimato: all'eta' 1, con chi gia' a 89.7, la distanza e' INVARIATA (0.540 contro 0.539) e
  l'arco diretto e' vivo al **100%**. Decorrelano da ADIACENTI e CONNESSI.
- **IL COEFFICIENTE DI GILBERT DAL FDT SI DERIVA (zero parametri) ED E' ~1e4 VOLTE TROPPO LENTO**
  (`doc/ANALISI_gilbert_fdt.md`, 2026-09-15). Dal rumore sul Bloch (riga 1847, `amp`):
  `D = 2*amp^2/dt`; imponendo che l'equilibrio di Langevin `<th^2> = D/(2 lambda)` coincida con
  quello di Boltzmann `<th^2> = 2kT/|B|` si ottiene `lambda = amp^2*|B|/(2*dt*kT)`. Con l'unica
  temperatura parameter-free del sistema (`kT = Lam`, l'energia del vuoto, da cui il rumore stesso
  e' costruito) **`Lam` SI CANCELLA**: `lambda = |B|/(2*dt)` = 3.47/tempo, cioe' un tempo di
  allineamento di **28.8 passi** — contro un rimescolamento misurato di **0.0030 passi**.
  **Il FDT non licenzia uno smorzamento sufficiente**, e metterne uno piu' grande significherebbe
  SCEGLIERLO (contro par.3) e mettere dissipazione senza fluttuazione: lo stesso errore, ribaltato.
  Controllo: l'equipartizione con `I=1e-6` darebbe `kT = 800` contro `Lam = 4.4e-5` (rapporto ~2e7)
  -> **non e' equilibrio termico ma equilibrio DINAMICO pilotato**, ed e' la ragione strutturale per
  cui il FDT non puo' fissare il coefficiente: accoppia una dissipazione a una FLUTTUAZIONE, e qui
  il termine dominante non e' una fluttuazione.
- **IL TEMPO DI DISSIPAZIONE E' FISSATO DA UN PAVIMENTO, non dalla densita'** (misurato 2026-09-15).
  Nella seconda meta' di un run `tau/DT` vale esattamente **250** = `TAU_A*0.05/DT`, cioe' il
  pavimento di `max(rho/rho_rif, 0.05)` (riga 1913). Stessa famiglia del pavimento `1e-6`
  sull'inerzia: alle scale simulabili **la regolarizzazione diventa il parametro fisico**.
- **PRESIDIO — UN'IPOTESI CHE RIGENERA LA PROPRIA SCUSA NON E' UN'IPOTESI** (rilievo di Luca,
  2026-09-15, `doc/CRITERIO_omega_rho.md`). Se ogni volta che l'effetto atteso non si vede la
  spiegazione diventa "il ritardo e' piu' lungo di quanto credessi", e la grandezza che fissa quel
  ritardo **cresce insieme** a quella che si sta misurando, allora **aspettare non chiudera' MAI la
  questione**: il bersaglio si sposta a ogni misura. E' la forma classica della congettura
  **non falsificabile**, e si riconosce dalla FORMA dell'argomento, non dal suo contenuto.
  CASO REALE, preso su questo repo: "theta non scende perche' l'inerzia e' al pavimento" -> il
  pavimento si rilascia e theta non scende -> "perche' insegue con tau=250" -> passano 775 passi e
  theta non scende -> "perche' ora tau e' 5000". Tre scuse, ognuna generata dal fallimento della
  precedente, e `tau ∝ rho` con `rho` crescente: l'attesa **non converge per costruzione**.
  **PRESIDIO OPERATIVO:** quando una spiegazione e' temporale (un ritardo), il test che la decide
  **non deve contenere il tempo**. Si misura la relazione **TRASVERSALE**, a un solo istante, fra
  individui che in quel momento hanno valori diversi della variabile: se la relazione non c'e'
  **allo stesso istante**, nessun ritardo puo' spiegarla. E il criterio si scrive **prima**, con una
  soglia numerica, e **non si proroga**: se scatta, l'ipotesi si **RITIRA**, non si raffina.
- **⚠ CORRETTA il 2026-09-17 — `_tau` NON HA IL PUNTO FISSO CHE QUESTA VOCE GLI ATTRIBUIVA.**
  **La versione precedente diceva:** *«poiche' il riferimento e' la MEDIANA, per il nodo mediano
  `_dens/_dens_rif ~ 1` sempre... e' un punto fisso auto-normalizzante... far maturare il sistema
  non puo', PER COSTRUZIONE, accorciare la memoria del nodo tipico»*.
  **MISURATO** (`csv/_test_fork/_analisi7_assiomi.txt`, 4 semi, 300 passi, blob `a44adc31`):
  `tau_mediano/TAU_A` vale **0.3698 / 0.0629 / 0.8024 / 0.7475** — un **fattore 13 fra semi**,
  non 1.
  **PERCHE', ed e' scritto nella voce stessa che lo negava:** `_dens_rif = median(_dens[_dens >
  1e-6])` e' la mediana di un **SOTTOINSIEME** (il **78-88 %** dei nodi), non dell'insieme.
  Numeratore e denominatore vivono su **popolazioni diverse**, ed e' esattamente la condizione che
  il punto fisso di **C12** richiede e che qui **manca**. *(La stessa distinzione che
  `doc/ASSIOMI.md` A3 chiama «errore di popolazione» — qui col segno opposto: **salva** la legge
  invece di romperla, e la salva **per caso**.)*
  **CONTROPROVA, che e' cio' che rende la correzione conclusiva:** ricalcolando con la mediana su
  **tutti** i nodi, il rapporto vale **`1.000000` ESATTO su 4 semi su 4**. Il filtro e' l'**unica**
  cosa che separa i due casi.
  **COSA RESTA VERO:** il punto fisso **esatto** non c'e', ma il rapporto resta confinato entro un
  fattore ~16: l'ancoraggio e' **attenuato, non abolito**.
  **COSA NON E' PIU' SOSTENUTO:** la conseguenza operativa *«far maturare il sistema non puo', PER
  COSTRUZIONE, accorciare la memoria del nodo tipico»*. **Non e' dimostrato il contrario** — non e'
  stato misurato a tempi diversi — ma **la DIMOSTRAZIONE su cui poggiava non regge.**
  **E IL PAVIMENTO `0.05` NON E' «QUASI TUTTI I NODI»:** misurato **19.58 %** in media (8.8-45.3 %)
  a 300 passi. Il **250 = TAU_A*0.05/DT** citato altrove in questo paragrafo riguarda la **seconda
  meta'** di un run: e' un'altra misura, e **non si trasporta a questa senza dirlo.**
  **LEZIONE DI METODO, ed e' la ragione per cui la voce sbagliata e' sopravvissuta due giorni:**
  la voce **citava il filtro** `[_dens > 1e-6]` e **concludeva comunque** per il punto fisso.
  L'argomento algebrico era stato scritto **guardando la forma** `x/median(x)` e **non l'espressione
  effettiva**. E' P1 applicato al proprio testo: **un'identita' algebrica va verificata sul codice
  che gira, non sulla sua forma ricordata.**
- **`correzione` HA DUE TERMINI, NON UNO** (righe **1895-1901**, verificato 2026-09-15):
  `correzione = cross(B, nb)`, e **se `CAMPO_SPINORIALE`** (ATTIVO in tutti i run del fork)
  `correzione += cross(_nb_grav(), nb)` — il torque verso il Bloch del **campo emesso spinoriale**.
  **Chi ricostruisce la catena di `omega` fuori dal simulatore e ne dimentica uno calcola meta'
  coppia** (successo il 2026-09-15: il residuo non spiegato valeva ~2.8 volte il deterministico).
  NB per la ricostruzione: `B` e' costruito da `nb_vic = self._nb_prec` (riga 1854), cioe' il Bloch
  **committato**, mentre il `nb` del prodotto vettore e' quello **DOPO** il rumore di riga 1847.
- **VERDETTO DEL TRACING DI `omega` (2026-09-15, `doc/TRACING_omega.md`): ESITO (I), NESSUN BUG.**
  La formula d'ingresso e' **giusta**: `coppia/inerzia` ha pendenza trasversale **-1.056** con
  `r = -0.981` su 2781 nodi — esattamente il `-1` che la legge richiede, e viene **tutto** dalla
  divisione per l'inerzia (la coppia da sola e' **piatta**, -0.056). Ma `theta` ha **-0.113**:
  **l'esponente si perde A VALLE**, nel rilassamento, attraverso `sqrt(tau)`.
  Esclusi per misura: (II-a) `|B|` **decresce** (-0.534), non cresce; (II-b) l'angolo `(B,nb)` e'
  **piatto** (-0.006, `r = -0.025`, mediana 59.4 gradi); (IV) `R_stoc = 0.041`, **sotto** l'errore
  atteso della ricostruzione (0.097) -> il rumore e' **marginale**, non guida `omega`.
  E il termine dissipativo **non domina**: rapporto coppia/dissipativo **= 188.9**.
- **LA CATENA `pendenza(theta) = pendenza(sigma) + pendenza(tau)/2` CHIUDE, ma solo A TEMPI LUNGHI**
  (2026-09-15, `doc/BARRE_ERRORE_pendenze.md`). Lo scarto fra attesa e misurata **CALA di due ordini
  col tempo**: **0.979** al passo 50 -> **0.010** al passo 400 (pendenza su `log(passo)`: **-0.412**).
  **E' un TRANSITORIO, non un termine mancante:** `tau ~ 4425-6500 passi` mentre i run ne hanno
  300-400, quindi il sistema ha vissuto **meno di un decimo** di un tempo di rilassamento, e la
  formula vale **all'EQUILIBRIO**.
  **DOPPIA CORREZIONE, entrambe mie, entrambe dello stesso giorno:** prima avevo scritto che la
  catena chiudeva (scarto 0.037); poi che NON chiudeva (0.338) **attribuendolo ai 20 nodi**; en-
  trambe le letture erano parziali. **A parita' di passo le due strade di misura di `tau` CONCORDANO**
  (passo 300: diretta +1.176 su 2195 contro indiretta +1.178, scarto **0.002**; passo 400: +1.812 su
  20 contro +1.867 su 2781, scarto **0.055**). **La differenza e' il PASSO, non il campione.**
- **PRESIDIO — `r^2` BASSO NON SIGNIFICA PENDENZA INCERTA** (2026-09-15). `SE_b = |b/r|*sqrt((1-r^2)/(n-2))`:
  il fattore dominante e' **`sqrt(n)`**, non `r`. Stessa pendenza e stesso `r = 0.32`: `SE` vale
  **0.108** con 20 punti, **0.0097** con 2195. Quindi una pendenza con `r^2 = 0.10` su 2195 nodi e'
  determinata a **+-0.01**. `r^2` basso dice che la relazione **spiega poca varianza**, non che la
  pendenza sia fragile. **Serve sempre `SE`, non `r`, per decidere se uno scarto e' significativo.**
- **`d/cs` E' PIATTO CONTRO L'INERZIA: pendenza +0.097** (`r = +0.351`, 2195 nodi; 2026-09-15,
  `doc/TAU_tempo_luce.md`). Quindi sostituire `tau = TAU_A*max(dens/dens_rif, 0.05)` (riga 1913) con
  il **tempo-luce `d/cs`** (lo stesso `tau` gia' cablato nello Strato 1) **romperebbe la
  cancellazione**: `theta` passerebbe da **-0.152** a fra **-0.69** (stima onesta, col residuo) e
  **-1.03** (stima naive). **MA L'AMPIEZZA NON RISOLVE:** `tau/DT` da **6500** a **66.5** passi, e
  poiche' `|omega|_eq ∝ sqrt(tau)` il fattore e' **0.101**: da **126.7 a 12.8 GIRI per passo**.
  **Un ordine di grandezza nella direzione giusta, e il settore resta ALIASATO. Non e' una cura.**
- **PRESIDIO — UNA FORMULA PREDITTIVA SI VALIDA SUL CASO NOTO *PRIMA* DI USARLA PER ESTRAPOLARE**
  (2026-09-15). La relazione `theta = sigma + tau/2` sembrava confermata (scarto 0.037) finche' non
  si e' rifatta la misura di `tau` su un campione serio: **scarto 0.338**. Se avessi estrapolato
  senza ri-verificare, avrei predetto `-1.03` invece di `-0.69`.
  **NB (corretto il 2026-09-15 stesso):** avevo aggiunto qui il corollario *"una pendenza su 20
  nodi non e' una pendenza"*, citando `+1.812` contro `+1.176` come prova. **Quella prova NON era
  valida:** i due numeri sono a **passi diversi** (400 e 300), e a parita' di passo le due strade
  concordano entro 0.055. Il corollario resta una **buona prudenza** (un campione ridotto ha `SE`
  piu' grande, e infatti 20 nodi danno `SE = 0.108` contro 0.0097), ma **non era la causa di quel
  caso**, e citarlo come tale era un errore.
- **PRESIDIO — UN CRITERIO DI SIGILLO SI SCRIVE DA UNA MISURA, NON DAL PROPRIO MODELLO MENTALE
  DEL CODICE** (2026-09-16, dopo **tre** casi nello stesso giorno). Prima di fissare la soglia o
  la coppia di grandezze che un sigillo confronta, **si misura cosa fa davvero il codice** nel
  punto in cui il criterio guarda. Costa meno della spiegazione che si darebbe senza.
  **I TRE CASI, e la forma e' sempre la stessa:**
  * **`N3b`** — *«il ramo di fallback scatta <= 1 volta»* **in assoluto**: ma l'estensione su
    `semina()`/`nuova_massa()` e' **legittima** (voce **H**), quindi il criterio avrebbe prodotto
    un **FAIL su un comportamento corretto**;
  * **`M1b`/`M3`** — misurati **nel momento sbagliato**: subito dopo `mitosi()`, dove i figli
    **non hanno ancora** un `xi` e l'array e' **legittimamente corto**, perche' l'estensione
    avviene dentro `_passo_spinoriale`, cioe' all'inizio del passo **dopo**;
  * **`M3c`** — confrontato con la **coppia sbagliata**: la crescita attraverso `step()`, che e'
    **zero per costruzione** (i nodi nascono in `mitosi()`), contro i nodi nati. Stampava
    **«nodi nati 0»**, e un numero **impossibile** e' il modo in cui un criterio sbagliato si
    denuncia da solo.
  **UN CRITERIO SCADUTO CHE PRODUCE UN FAIL FALSO COSTA PIU' DI UN SIGILLO MANCANTE**, perche' si
  porta dietro **una diagnosi**: chi legge il FAIL cerca il difetto nel codice, e il difetto non
  c'e'. **E la soglia si deriva dal VALORE SOTTO IPOTESI NULLA, non si sceglie:** `|corr| < 0.15`
  era inventato; il nullo della correlazione campionaria di variabili indipendenti e'
  `sigma ~ 1/sqrt(3N)`, che su 110 coppie da' `3 sigma = 0.165`.
- **PRESIDIO — OGNI RAMO `else` / FALLBACK / `getattr(..., default)` SU UN PERCORSO FISICO VA
  STRUMENTATO CON UN CONTATORE: quante volte e' scattato?** Un fallback mai misurato e' un
  comportamento **sconosciuto**, e uno che scatta il 72% delle volte **non e' un fallback, e' il
  comportamento principale.** E' il gemello del presidio del "valore sotto ipotesi nulla": li'
  *"quanto varrebbe se non ci fosse niente?"*, qui *"quante volte questo ramo e' davvero quello che
  gira?"*. CASO REALE che ha generato la regola (2026-09-15): il ramo `else` di `_tempo_luce_nodo`
  scattava nel **71.88%** delle chiamate (23 su 32, cache inusabile in **24 passi su 30**) senza che
  nessun sigillo se ne accorgesse — perche' il ramo **non e' un errore**: e' il fallback legittimo
  per `--cs-dinamico` OFF e per il primo passo. Niente NaN, niente runaway, nessuna byte-identita'
  violata. **Un difetto silenzioso non si trova guardando se il codice sbaglia: si trova contando
  quale strada prende.**
- **PRESIDIO — SU QUESTO SISTEMA CAOTICO LA BARRA D'ERRORE DI UNA PENDENZA E' ~3 VOLTE LA `SE`
  INTERNA AL RUN** (misurato 2026-09-15, `csv/_test_fork/_controllo_semi.txt`). La stessa pendenza
  trasversale, **a codice INVARIATO**, cambia da seme a seme di **0.0302** (e 0.0286 sull'altro
  ramo), mentre la `SE` di campionamento **dentro** un singolo run vale **~0.010**. Quindi:
  **la `SE` interna e' la barra giusta per parlare di QUEL run, non del SISTEMA.** Per confrontare
  due run (due flag, due versioni del codice) il **valore sotto ipotesi nulla NON e' zero**: e' 0.03,
  e va misurato con piu' semi, non dedotto.
  CASO REALE che ha generato la regola: `Delta = -0.0445 +- 0.0141`, `z = 3.16` su **un** seme
  sembrava un effetto a 3 sigma. Su tre semi il **segno non e' nemmeno concorde**
  (-0.0445 / **+0.0367** / -0.0635), `t = -0.77`. **Un'ora di lavoro e tre documenti da correggere.**
  **CONSEGUENZA DA VERIFICARE, non ancora fatta:** tutte le pendenze committate in questo programma
  portano una `SE` interna, cioe' **una barra ~3 volte troppo piccola**. Le conclusioni gia' tratte
  sembrano reggere perche' gli effetti sono grandi (il **-1.056** del tracing, il **+0.097** di `d/cs`
  contro `-1`, il contrasto ON-OFF **-0.32** = 11 volte la dispersione), ma **vanno ricontrollate una
  per una contro 0.03, non contro 0.01.**
- **LA CACHE `_cs_nodo_prev` VENIVA SCARTATA A OGNI MITOSI — CURATO il 2026-09-15** (commit
  `43e9a47`, `doc/FIX_cache_cs.md`, sigillo `csv/_seal_fork/_sigillo_fix_cache.py` **5/5 PASS**).
  La cache e' scritta a fine passo con l'`n` di quel passo (riga ~2918); la **mitosi aggiunge nodi**,
  quindi al passo dopo la guardia `len(csp) >= n` falliva e `_tempo_luce_nodo` cadeva su
  `cs_nodo = CS_M`. Ne risentivano **due** chiamanti: `_bloch_ritardato` (**lo STRATO 1**, gia'
  sigillato 23/23) e il rilassamento sotto `--tau-luce`. Cura: il figlio **eredita `cs` dal padre**
  in `_eredita_spinore_figli`, **sesta voce della stessa convenzione** di `_nb`/`_nb_prec`/`_nb_ret`/
  `omega_s`/`_psi_spinor`/`_psi_prec` — zero parametri. Misurato: fallback **71.88% -> 0.00%**,
  passi con cache inusabile **24/30 -> 0/30**.
  **MA ATTENZIONE A COSA QUESTO NON DICE.** L'effetto FISICO della cura **non e' dimostrato**:
  su **3 semi** (`doc/FIX_cache_cs.md` par.7) `Delta` vale **-0.0445 / +0.0367 / -0.0635** — **segno
  NON concorde** — con `media -0.0238`, `SE 0.0307`, `t = -0.77`, e **`IC95 = [-0.156, +0.108]` che
  contiene lo ZERO *e* il `-0.120` dell'ipotesi "~meta'"**. **Tre semi non decidono: l'esperimento
  non ha potenza.** E' il fronte **P** di `doc/RAMIFICAZIONI.md`.
  **CORREZIONE DI UNA VOCE CHE AVEVO SCRITTO IO STESSO OGGI:** qui c'era scritto *"il difetto
  contribuiva il 16.9% del divario, `z = 3.16`"*, misurato su **UN** seme. **RITIRATO:** quel `z` usava
  la `SE` **interna a un singolo run** (~0.010) mentre la dispersione **fra semi, a codice invariato**,
  vale **0.030**. Era dispersione di run.
  **IL MIO ERRORE, da non rifare:** avevo argomentato che `cs` riparato varia solo dello **0.023%**
  (`min 1.99954`, `max 2.0`, `CS_M = 2`) e che quindi **non poteva** spostare la pendenza. **Avevo
  confrontato l'AMPIEZZA di una variazione con l'ampiezza di una pendenza.** Una pendenza trasversale
  non misura **quanto** una grandezza varia, misura **quanto la sua variazione e' CORRELATA** con
  l'ascissa: un fattore che cambia dello 0.02% ma **sistematicamente nella stessa direzione** lungo
  l'asse dell'inerzia **sposta la pendenza**; uno che cambia del 50% a caso non la sposta.
  **Argomento di AMPIEZZA su una domanda di CORRELAZIONE: e' l'errore, e si ripete facile.**
  Resta vero che `d` era vivo nel **100%** dei passi e che quasi tutto l'effetto della FASE 2 sta in
  `d` — i **6/7** di divario ancora aperto lo confermano — ma *"non puo' muoverla affatto"* era falso.
  **La cura resta giusta anche per una ragione indipendente:** `cs` e' quasi-costante **oggi**
  (par.6); il giorno in cui sara' vivo, una cache scartata a ogni mitosi sarebbe un difetto
  **grande**, e lo sarebbe **in silenzio**.
  NB — **la terza via di crescita dei nodi resta scoperta:** `semina()` (riga ~1600) **non** passa da
  `_eredita_spinore_figli`. In batch e' inerte (`semina_cont=False` di default, si accende **solo**
  dalla GUI, righe ~4610 e ~4753), quindi non tocca nessuna misura committata; registrata in
  `doc/RAMIFICAZIONI.md` sotto la voce **H** (percorso GUI).
- **`_psi_spin_prec` NON ERA ESTESO ALLA MITOSI → LA FASE 5 (OROLOGIO A 4pi) E' STATA INERTE IN OGNI
  RUN MAI GIRATO — CURATO il 2026-09-15** (commit `cc98ac0`, `doc/REPERTO_psi_spin_prec.md`, sigillo
  `csv/_seal_fork/_sigillo_psi_spin_prec.py` **6/6 PASS**). La guardia di `ritmo()` e' un'uguaglianza
  **ESATTA** (`len(_ps) == n and len(_psp) == n`), quindi bastava **un** nodo di mitosi per farla
  scartare. **MISURATO: 95.33%** delle chiamate (143/150), e la condizione che falliva era
  `len(_psi_spin_prec) != n` in **143 casi su 143** — `psi_spin`, ricostruito da `calcola_psi`
  **dentro** il passo, era sempre lungo `n`. Il 4pi girava **solo ai passi 2 e 3**, prima della prima
  mitosi. Dopo la cura: **0.00%**.
  **ATTENZIONE ALLA FORMULAZIONE, perche' quella sbagliata circola gia':** **NON** e' vero che *"la
  fisica ha integrato con un tempo proprio stale"*. `signed` era **gia' calcolato** nella versione
  **SCALARE a 2pi** poche righe sopra; la guardia decide solo se **sovrascriverlo** col 4pi. `r` era
  **ricalcolato a ogni passo ed era valido** (`len(_psi_prec) == n` in 149 chiamate su 150). La
  frase vera e': **la fisica ha integrato con l'orologio SCALARE STORICO, e la doppia copertura non
  e' mai entrata in funzione.** Le misure **non sono corrotte**: sono misure di un **modello diverso
  da quello che il flag dichiarava**. *"Integrate male"* implicherebbe errore numerico; *"orologio
  diverso da quello dichiarato"* implica modello diverso, **e solo la seconda e' vera.**
  **Conseguenza:** tutte le misure fino al blob `08784685` portano il marchio *"prese col ritmo
  scalare a 2pi; da riverificare col settore 4pi in funzione"* — **T3 e i suoi quattro bracci
  inclusi** (`doc/RAMIFICAZIONI.md`, secondo marchio in testa).
- **PRESIDIO — UNA GRANDEZZA NORMALIZZATA SULLA PROPRIA MEDIANA HA UN PUNTO FISSO: SU QUELLO NON SI
  MISURA NULLA.** Se `x = f / median(f)` e la mappa `x -> y` e' **monotona**, allora `median(y)` vale
  **una costante ESATTA**, sempre, qualunque cosa faccia `f`. Confrontare due configurazioni su
  quella mediana e' **come confrontare due termometri dopo averli azzerati ciascuno sulla propria
  lettura mediana**: si ottiene zero per costruzione, e lo zero non dice niente.
  **DUE CASI REALI, entrambi su questo repo:**
  * `_tau = TAU_A * max(_dens/_dens_rif, 0.05)` con `_dens_rif = median(_dens)` → `tau_mediano ~
    TAU_A` **sempre**, a qualunque maturazione (voce sotto);
  * `ritmo()`: `x = f/median(|f|)`, `r_normalized = r/r_unit` con `r_unit` = il valore a `x = 1`
    → **`median(r) = 1.0 ESATTAMENTE`**, con qualunque orologio. Il sigillo `S4` della cura di
    `_psi_spin_prec` confrontava proprio le due mediane e ha dato `z = 0.00`: **non "nessun
    effetto", ma "nessuna misura"**. L'unico numero informativo era la **dispersione**
    (`0.4421 -> 0.4257`, -3.7%, **un seme**, nullo non misurato → vedi il presidio su C10).
  **REGOLA: prima di confrontare una statistica riassuntiva fra due rami, controlla se il codice la
  ancora a se stessa.** E' il gemello del presidio del valore sotto ipotesi nulla: li' *"quanto
  varrebbe se non ci fosse niente?"*, qui *"questa grandezza puo' anche solo in linea di principio
  cambiare?"*.
- **PRESIDIO — UN DATO DEVE PORTARSI DIETRO LE PROPRIE CONDIZIONI. UN FILE CHE SI DISTINGUE DAGLI
  ALTRI SOLO PER IL NOME NON E' UN DATO: E' UN RICORDO.** Ogni CSV di misura deve portare, in ogni
  riga o in un blocco di testa: **il BLOB**, **il SEME**, e **TUTTI i flag che distinguono quel run
  dagli altri bracci dello stesso esperimento** — non solo quelli che si pensava contassero.
  **Non basta scriverli nel log:** il log si perde, il CSV resta.
  CASO REALE (2026-09-15, rilievo di Luca): il braccio OFF della prima misura del settore spinoriale
  ha 136 colonne e **sette** colonne di flag corrette (`FORK_SU2=1`, `FORK_SU2_MEM=1`,
  `KURAMOTO_SU2=0`, `STEP2=0`, `GAMMA_TURBO=1.0`, `SCUOTIMENTO=1`, `SYNC_UPDATE=0`) — **ma NON ha
  `TAU_LUCE`**, che e' l'**unica** variabile che distingue i due bracci di quell'esperimento, **ne'
  `CS_DINAMICO`**, ne' il blob, ne' il seme. I due bracci erano distinguibili **solo dal nome del
  file**. Il run **non era sbagliato** (il flag era davvero OFF, come doveva); era **non
  certificabile dai dati**.
  **E la diagnosi è stata fatta dal DISCO, non dalla memoria:** i CSV sono stati scritti alle
  `19:18:46`, la colonna e' stata aggiunta al codice alle `19:23:32` — **cinque minuti dopo**.
  *(Chi avesse "ricordato" che la colonna c'era avrebbe certificato un file che non la contiene.)*
  **COROLLARIO OPERATIVO:** quando si aggiunge una colonna di certificazione, **i dati gia' scritti
  non la acquisiscono**. O si rilancia, o si annota **esplicitamente nel documento** che la colonna
  manca e **da dove si deduce lo stato** — e un'annotazione dichiarata vale, una ricostruzione a
  memoria no. *(Nel caso reale: `CS_DINAMICO` off e' deducibile da `cs_std = nan` su tutti gli 11
  campioni, perche' la cache `_cs_nodo_prev` non viene scritta a flag spento. Deducibile, non
  scritto.)*
- **IL SIGILLO DELLO STRATO 1 SI SCHIANTAVA DA UN GIORNO, E NESSUNO SE N'ERA ACCORTO PERCHE'
  NESSUNO LO AVEVA RIGIRATO** (2026-09-16, `csv/_seal_fork/_sigillo_strato1_CRASH_2026-09-16.txt`).
  `_bloch_ritardato` calcolava `tau = d/cs` **inline**; dal commit `f7051c3` (cablaggio di
  `--tau-luce`) la legge e' stata **estratta** nel metodo condiviso `_tempo_luce_nodo`, che
  `_bloch_ritardato` ora **chiama**. `FintaRete` — il guscio in-process del sigillo — espone i
  metodi del simulatore **UNO PER UNO**, quindi da quel momento gli mancava il metodo:
  `AttributeError` a S2, e **S2, S3, S5, S6, S7, S8 e S3b non giravano affatto**.
  **NON FALLIVA: SI SCHIANTAVA** — la modalita' piu' facile da non notare.
  **CONSEGUENZA PIU' FORTE DEL MARCHIO:** dal blob `f7051c3` in poi il «23/23» non era nemmeno
  **RIPRODUCIBILE**. **Un sigillo che non viene rigirato non protegge nulla.**
  **FRAGILITA' DI STRUTTURA, non caso singolo:** poiche' `FintaRete` elenca i metodi a mano,
  **qualunque estrazione futura** di un metodo dentro `_bloch_ritardato` o `_coppia_interferenza`
  rompera' il sigillo **allo stesso modo e in silenzio**. **Gli altri sigilli in-process non sono
  stati controllati per lo stesso difetto** (2026-09-16).
- **⚠ SUPERATA il 2026-09-18 — `cs` E' VIVO: `cs_std/cs = 17.6 %`, non `0.0086-0.24 %`.**
  **MISURATO** (`doc/REFERTO_gauge_vuoto.md` par.1, `csv/_test_fork/_gauge_vuoto.py`, blob
  `f8f46683`, 1 seme, 120 passi, ramo 4pi): `cs/CS_M` ha **mediana 0.8265**, `p05` **0.528**, **min
  0.283**; **`cs_std/cs` per passo vale 17.6 %** (min 16.6 %, max 19.4 %), e la frazione con
  `cs/CS_M > 0.99` e' solo il **6.3 %**.
  **La voce qui sotto dice, come fatto stabile, «sempre sotto l'1 %»: e' superata di un fattore
  ~2000 rispetto allo 0.0086 % e ~73 rispetto allo 0.24 %, ed e' SOPRA la soglia dell'1 % di
  DICIASSETTE volte.** La voce resta scritta perche' dice **com'era** e **a quale blob**: e' un'
  informazione, non un errore (stessa convenzione dei marchi storici dello Strato 1).
  **PERCHE', dal codice e non da una congettura:** la cura di `cs_floor` del 2026-09-16 (categoria D,
  nessun flag) ha sostituito la scala **ASSOLUTA** `1/GAMMA^2 = 400` con la scala **RELAZIONALE**
  `_Lam = mean(I)` (`:2914`, `:2921`). Con `400`, `I ~ 1e-7` dava `sqrt(I/400) ~ 1e-5` e **`cs` era
  inchiodato a `CS_M`**; con `mean(I)` il rapporto `I/mean(I)` e' **O(1) per costruzione, a
  QUALUNQUE densita'**.
  > **`cs` non e' vivo perche' il sistema e' maturato: e' vivo perche' la SCALA e' diventata
  > relazionale.** **Una correzione di difetto senza flag ha riaperto un fronte che il registro dava
  > per chiuso «alle densita' simulabili».**
  **⚠ E COSA QUESTO NON DICE:** **non** dice che `tau = d/cs` sia **fisicamente distinguibile** da
  `tau ∝ d` nei run veri — quello richiede il **confronto**, non la dispersione. Dice che **la
  premessa che lo escludeva e' caduta**. **Il giudizio «il braccio ON non testa il tempo-luce» VA
  RIFATTO**, e con esso la parte del fronte **A** che vi si appoggiava. **-> `Z39` del registro.**
  **LIMITE: un seme, 120 passi, una scena** — e il presidio sull'istante (poco sotto) vale anche qui:
  quel rapporto **cresce col tempo**, quindi va citato **con il passo a cui e' misurato.**
- **IL TEMPO-LUCE `tau = d/cs` NON E' TESTABILE ALLE DENSITA' SIMULABILI — MISURATO, non dedotto**
  (2026-09-15, rilievo di Luca). Con `--cs-dinamico` **acceso** e la cache **riparata**:
  `cs ∈ [1.99893, 2.0]`, `cs_std = 1.72e-4`, cioe' **`cs_std/cs = 0.0086 %`** — **116 volte sotto**
  la soglia dell'1% sotto la quale `d/cs` e' indistinguibile da `d`. E dentro `tau`, `cs` pesa
  **0.00629 %** della dispersione (**1 parte su 15 898**).
  **CONSEGUENZA, e va detta cosi':** `cs` non e' quasi-costante *per caso*, e' **MORTO PER DENSITA'**
  (par.6, `I ~ 0.05` contro soglia `~400`). Quindi **`tau = d/cs` E' `tau ∝ d`**, e tutto il ramo di
  lavoro su `--tau-luce` e' — **in questo regime** — un ramo su **`tau ∝ d`**:
  **distanza contro densita'**, non tempo-luce contro densita'.
  **E' un confronto sensato e informativo, ma NON e' quello che il nome del flag dice.**
  **TRE COSE CHE NE DISCENDONO, da non rileggere male fra un mese:**
  * il braccio ON **non testa il tempo-luce**;
  * la giustificazione principale della sostituzione (`inerzia = T^2 = (d/cs)^2`, la causalita') vive
    sul **`cs` locale**: resta vera **in linea di principio**, **non e' esercitata** in questo regime;
  * il fix della cache `_cs_nodo_prev` era **giusto** (un bug e' un bug) ma **in questo regime muove
    lo 0.009%**: **non poteva spiegare nulla** — ed e' il motivo strutturale per cui il «16.9%» e
    l'«11.0%» sono caduti, al di la' della barra d'errore sbagliata.
  **QUANDO SARA' TESTABILE:** solo con **`cs` VIVO** — alta densita', oppure il **turbo su GAMMA**,
  che pero' e' un **esperimento** (`doc/COMPONENTI_PROMOSSE.md` C1), non fisica.
  **Cio' che NON dipende da `cs` e resta il valore vero dei quattro bracci: il GRADIENTE DI
  RISOLUZIONE**, `theta` da **~129** a **~39** giri/passo.
- **PRESIDIO — DUE SEMI SODDISFANO IL MINIMO DEL par.2.7 MA NON PERMETTONO DI STIMARE UNA BARRA
  FRA SEMI.** Con 2 semi la deviazione standard ha **UN grado di liberta'**, e `t(0.025, 1) = 12.706`:
  l'IC95 diventa ~**12.7 volte** la `SE` della media, cioe' praticamente inutilizzabile.
  CASO REALE (2026-09-15, `doc/REFERTO_4bracci_4pi.md`): `chi` materia e' **sotto 90 su entrambi i
  semi OFF** (89.778, 89.876) e **sopra 90 su entrambi i semi ON** (90.048, 90.084) — segno concorde,
  `z ~ 3.5` se preso ingenuamente. **Ma l'IC95 con 1 gdl e' largo 1.2 gradi e contiene lo zero.**
  **Il segno concorde su 2 semi non e' una prova: e' un'ipotesi da rifare con 4.** Con 4 semi
  `t(3) = 3.18`, quattro volte piu' stretto. **Per una barra FRA SEMI servono >= 4 semi.**
- **PRESIDIO — UNA SOGLIA SU UNA GRANDEZZA DI UN SISTEMA CHE CRESCE VA DICHIARATA CON L'ISTANTE IN
  CUI SI MISURA**, altrimenti si finisce per citare la piu' comoda. CASO REALE (2026-09-15):
  `cs_std/cs` — il rapporto che decide se `tau = d/cs` e' distinguibile da `tau ∝ d` — vale
  **0.0086%** al passo 50 (n~80), **0.096%** al passo 300, **0.19-0.24%** al passo 500:
  **venti volte in 450 passi.** Avevo registrato il primo valore come se fosse una proprieta' del
  sistema; era un'istantanea su 80 nodi appena seminati. Il margine sotto la soglia dell'1% e'
  passato da **116x** a **~4x**. La conclusione regge, **la sua forza no** — e poiche' la traiettoria
  e' **monotona crescente**, il regime **cambia con la maturazione**: il tempo-luce non e' «non
  testabile mai», e' «non testabile a 500 passi».
- **`conc_nodi`/`conc_archi`/`masse_info` NON FINIVANO NELLO SNAPSHOT — CURATO il 2026-09-18**
  (blob `a1ae5090` -> **`b9e07c73`**, `doc/REFERTO_coorti_snapshot.md`, sigillo
  `csv/_seal_fork/_sigillo_coorti.py` **9/9 PASS**). Il filtro di `salva_stato` (`:2865-2866`) accetta
  `ndarray`/scalari/`str`; **`conc_nodi` e `conc_archi` sono `list` e `masse_info` e' un `dict`: non
  matchavano, e venivano SCARTATI IN SILENZIO** — mentre la docstring della funzione dichiara
  *«salva TUTTE le grandezze di stato ... cosi' non ne dimentica nessuna»*. **Dopo un salva/ricarica
  il lignaggio delle coorti ripartiva VUOTO.** **Cura: si aggiungono ESPLICITAMENTE dopo il ciclo su
  `__dict__`; IL FILTRO NON SI ALLARGA** (allargarlo farebbe entrare le cache derivate `_S`, `_perm`,
  `_ker_cache`, **che `carica_stato` INVALIDA apposta**). **CATEGORIA D del par.10: nessun flag.**
  **⚠ E LA META' DEL MANDATO CHE NON SERVIVA:** l'**eredita' alla mitosi c'era GIA'** (`:3951-3954`,
  copia profonda dal genitore `a`; ramo Schwinger `:4076-4082`; `conc_archi` riallineato
  `:3997-4001`). **`:1858` — l'`extend` con liste vuote — e' in `semina()`, NON in `mitosi()`, ed e'
  CORRETTO li'.** **Misurato sui DUE bracci: frazione di nodi con coorte non vuota `0.8238` contro
  `0.8238`, identica** *(e' l'`82.4 %`, **non** il «~100 %» atteso: il complemento sono i nodi
  **seminati**, che per costruzione non hanno lignaggio)*.
  **⚠ COSA QUESTO NON DA': gli snapshot GIA' SCRITTI non acquisiscono le coorti retroattivamente.**
  I sei `.pkl` di `_gvideo` e i sei di `_g2m` vengono dal blob `a1ae5090`: **per averle servirebbe
  rigirare le scene.** **E il costo a `n = 8000` NON E' MISURATO:** `S5` da' **`+25.6 %`** sul `.pkl`
  a `n = 454`, e **il tempo non si legge** (due esecuzioni: `x1.0051` e **`x0.9245`**, cioe' il nuovo
  *piu' veloce* del vecchio — **rumore di sistema su 60 passi**).
- **`scala_p` E' CURATA (2026-09-20, `Z67`, sigillo 5/5, categoria D: nessun flag).** La scala di
  `ampiezza` in `memoria_hebbiana_moto` **non e' piu' `median(|dpozzo|)`** — che era **`A3`** e
  inchiodava **`median(ampiezza) = tanh(1) = 0.761594` PER COSTRUZIONE** *(misurato su 14 istanti
  su 14, scarto `2.3e-11`)*. **Ora e' il POZZO LOCALE `0.5*(phi_g[ii]+phi_g[jj])`**: un gradiente
  relativo, adimensionale e locale. **NESSUN PAVIMENTO, e non per fiducia: il rapporto e' `<= 2`
  PER COSTRUZIONE** *(`phi_g >= 0` -> `|phi_g[j]-phi_g[i]| <= 2*phi_arc`; max misurato `2` esatto)*.
  **`0/0` e' definito ZERO, dichiarato.** **CONSEGUENZA MISURATA: `sin2` non e' piu' saturo
  (`p95` da `1.000000` a `0.980561`) e il moltiplicatore di `beta` passa da `0.9928` a `0.8029`:
  `ZETA_VIR` era acceso e NON FRENAVA QUASI NULLA.**
  **⚠ `SCALA_P_MEDIANA` e' una costante DIAGNOSTICA senza flag da riga di comando**, di proposito:
  serve solo alla riduzione al limite del sigillo, e non deve poter essere accesa da un comando.
- **ESISTONO I CONTATORI DELLE GUARDIE, e si leggono con `rapporto_guardie(net)`** (2026-09-20,
  `Z68`/`Z69`). **Sono BYTE-INERTI** *(verificato: 7 campi identici contro il blob precedente)* e
  coprono **quindici siti**. **Ogni sito ha QUATTRO numeri, non uno:** invocazioni, salti, **la
  FORMA al fallimento** *(le due lunghezze; `-1` significa memoria ASSENTE, non lunghezza 0)* e
  **QUANDO** — l'indice dell'ULTIMA invocazione saltata. **Il `quando` non e' un lusso:** `20 %` di
  salti **confinati alle prime 11 invocazioni su 55** e `20 %` **sparsi su tutto il run** danno lo
  **stesso conteggio** e sono due diagnosi opposte (`A8`).
  **⚠ E I CONTATORI DELLE `(b)` SI CHIAMANO `_spento`, NON `_salti`:** misurano un ramo che non gira
  **per scelta** (flag o costante a zero), non una legge saltata. Mescolarli produrrebbe una
  «frazione di fallimento» che e' una **frequenza di selezione**.
- Ancora elastica verso LAM (riga ~3234): e' a CORTO raggio (filtro_portata=1-tanh(d/LAM)), fissa la
  scala LOCALE (materia legata), NON blocca l'espansione a grande scala.

- **⚠ `STEP2_OROLOGIO` E' ON DI DEFAULT dal 2026-09-16 (prima promozione eseguita, par.10).**
  **CONSEGUENZA OPERATIVA CHE VALE PER OGNI SCRIPT: l'ASSENZA di `--step2-orologio` NON significa
  piu' OFF, significa ON.** Il braccio OFF si ottiene **solo** con **`--senza-step2-orologio`**
  (nell'osservatore: **`--senza-step2`**), ed e' un **DIAGNOSTICO, non fisica alternativa**.
  `--step2-orologio` resta accettato come **NO-OP dichiarato** (stampa un avviso), per non rompere
  comandi e script gia' scritti.
  **PERCHE' E' UN PRESIDIO E NON UNA NOTA:** il sigillo `_sigillo_step2.py` prendeva il braccio OFF
  **per omissione del flag**. Se non fosse stato adeguato nello stesso commit, **`S2` avrebbe
  confrontato ON contro ON** e sarebbe **PASSATO SEMPRE** — un falso PASS esattamente della classe
  gia' catalogata qui (*«`max|A-B| = 0.000e+00` puo' significare "nessun confronto"»*), **e stavolta
  con le shape UGUALI**, quindi invisibile anche alla guardia delle shape. Adeguati nello stesso
  commit: `csv/_seal_fork/_sigillo_step2.py` e `csv/_test_fork/_osserva_vuoto.py`.
  **REGOLA GENERALE CHE NE DISCENDE: quando si ribalta un default, si cercano nello stesso commit
  TUTTI i punti che ottenevano il vecchio comportamento per OMISSIONE.** Un default ribaltato non
  rompe niente rumorosamente: **converte i rami di controllo in duplicati del ramo di prova.**

- **`TW_SPINORE` RESTA SPENTO PER DECISIONE DI LUCA (2026-09-16), E IL SUO COMMENTO E' FALSO.**
  Il commento (`:705-709`, `:2146-2148`) dice che la torsione *«pilota il Bloch di `tw/2`»*, cioe' un
  **ANGOLO**. **Il codice (`:2149-2154`) somma `tw/(4 pi)` a `omega_new`, che e' una VELOCITA'
  ANGOLARE** (`theta = |omega|*dt`, `:2210` e `:2296`): l'angolo effettivo e' **1.564e-03 rad/passo**
  contro i **9.827e-01** dichiarati, **fattore 628.3 = 2 pi / DT** — *un'unita' di misura mancante,
  non un'approssimazione*. E il termine finisce in **`self.omega_s`** (`:2313`), la **memoria
  persistente**, mentre il commento di `SYNC_SPINORE` (`:724`, `:2157-2160`) dice, **dello stesso
  blocco**, che metterci un torque *«darebbe accumulo/divergenza»*. **Unico fra i termini del blocco,
  `_otw` NON e' diviso per l'inerzia.**
  **CHI VOLESSE RIACCENDERLO LEGGA PRIMA `doc/REFERTO_tw_spinore.md`**: accenderlo **non** aggiunge
  la legge che il commento descrive. *(Stessa classe di `VERSO_CHI`, muto sotto `CHI_CORE`: un flag
  che non fa cio' che dichiara e' peggio di un flag assente.)*
  **E NON E' ARCHIVIATO COME «TRASCURABILE»:** il peso in **ampiezza** e' **0.054 %**, ma la domanda
  e' **DIREZIONALE** — l'asse TW e' **fisso e persistente**, `omega` e' un **random walk**. L'argomento
  di ampiezza su una domanda di correlazione **e' l'errore gia' fatto su `cs` allo 0.023 %**, e vale
  **anche al contrario**. **Resta il fronte `W` del registro.**
  **NESSUN SIGILLO E' STATO SCRITTO, di proposito:** il suo criterio naturale verrebbe **dalla
  descrizione invece che dal codice**, e sarebbe il **quarto** criterio stale in due giorni.

- **PRESIDIO — SI MISURA PER PROMUOVERE, SI DIMOSTRA PER ESCLUDERE** (audit di lettura chiesto da
  Luca, 2026-09-16, `doc/COMPONENTI_PROMOSSE.md` sezione **E**). Una misura dice *«questa legge
  produce un effetto»*; **non dice se ha senso.** `SPIN_LARMOR` produceva un effetto ed era
  **sbagliata**; il fattore `cs^-2` non ne produce quasi ed e' **necessario**.
  **CONSEGUENZA OPERATIVA: escludere una legge perche' «non produce effetto» NON E' UN ARGOMENTO.**
  Si deve dire **QUALE PROPRIETA' ROMPE** — antisimmetria su arco orientato, localita' (§4),
  zero-manopole (§3), un'identita' misurata — **e citarne il punto nel codice.**
  **E per questo le esclusioni per DIMOSTRAZIONE non si riaprono con una misura:** tornano in gioco
  solo se cade la dimostrazione, cioe' se quella proprieta' non e' piu' richiesta o se il codice
  cambia. E' la stessa distinzione che §5-quater impone gia' al registro dei fronti.
  **IL CODICE DI UNA LEGGE ESCLUSA NON SI CANCELLA MAI:** resta spento, ed e' **l'evidenza che
  spiega perche' esiste il suo sostituto** (`TW_SPINORE` esiste **perche'** `SPIN_LARMOR` fallisce:
  cancellare il secondo farebbe perdere il **perche'** del primo).

- **PRESIDIO — UN RISULTATO NULLO SI LEGGE SOLO INSIEME ALLA RISOLUZIONE CHE LO HA PRODOTTO**
  (2026-09-16, `doc/REFERTO_step2_U1.md`). *«L'IC95 contiene lo zero»* **non e' un risultato**
  finche' non si dice **quale effetto quel test AVREBBE potuto vedere**. E' la versione statistica
  del `max|A-B| = 0.000e+00` per **mancanza di confronto**: in entrambi i casi uno zero viene letto
  come informazione mentre e' **assenza di informazione**.
  **CASO REALE, nella STESSA tabella:** contrasto Step 2 ON/OFF, 4 semi appaiati — su `chi` la
  risoluzione e' lo **0.213 %** (il nullo dice **molto**: `chi` non si sposta di piu' di 0.19 gradi),
  su **`|<n>|` e' il 129 %** e sulla **coerenza di segno il 603 %** (il nullo dice **NIENTE**: la
  barra e' **piu' larga del valore**). **Ventidue righe tutte «contiene lo zero», e non significano
  la stessa cosa.**
  **REGOLA OPERATIVA: un risultato negativo si scrive come LIMITE SUPERIORE** — *«X non si sposta di
  piu' di Y»* — **non come «X non cambia».** E se il limite superiore e' piu' grande della grandezza
  stessa, si scrive **«non misurato»**, non «nessun effetto».
  **E la cura non e' sempre piu' passi:** dove la grandezza **vale gia' il suo nullo** (un Bloch
  medio di versori casuali, una coerenza che vale 0) la barra percentuale **non puo'** essere
  piccola. Li' servono **piu' SEMI**.

- **ARCHIVIO A SERIE — `--db-serie` e `--db-rigioca` (2026-09-19, sigillo 12/12 sul blob `7c4dec1d`).**
  `--db-serie` NUMERA gli snapshot (`<stem>_000250.pkl`) invece di sovrascriverli; `--db-rigioca DA A`
  ricarica lo snapshot `DA` e rigioca fino ad `A` **INFITTENDO** l'archivio, **senza sovrascrivere**
  cio' che esiste (salta e conta). Con path `.gz` lo snapshot e' compresso a **livello 1**.
  **Entrambi OFF di default. NON sono fisica** (`doc/COMPONENTI_PROMOSSE.md` **G**): sono
  **infrastruttura di persistenza**, e il par.10 non si applica perche' il par.10 governa **leggi**.
  **`V1`/`V2`: 97 campi byte-identici** contro il codice pre-archivio e fra ON e OFF.
  **⚠ IL DISCRIMINANTE PER RIFIUTARE UNA SERIE E' IL BLOB, NON LA CADENZA**, e il perche' e' un
  errore gia' fatto: il primo criterio pretendeva la **contiguita'** dei passi e **rifiutava proprio
  il caso d'uso di `--db-rigioca`** (infittire = cadenza piu' piccola = serie non contigua).
  **Cadenze diverse nella stessa serie sono LEGITTIME: e' il senso dell'archivio.**
- **`gzip` SU QUESTI DATI COMPRIME `1.76x` E BASTA, ed e' IL LIMITE DEL DATO** (float64 densi;
  misurato su uno snapshot vero da 27.73 MB, `csv/_seal_fork/_costo_archivio_2026-09-19.txt`).
  Il livello **9** — che e' il **default di `gzip.open`**, mai scelto da nessuno — costa **4.42 s**
  per snapshot contro **0.82 s** del livello 1, per il **2 %** di spazio in piu'. **Cablato il
  livello 1** (decisione di Luca). **E questo numero CHIUDE la proposta ibrida `pickle`+HDF5:**
  HDF5 comprimerebbe gli stessi byte con gli stessi algoritmi.
- **IL 75 % DELLE VOCI DEI REGISTRI NON PORTA IL BLOB DEL CODICE CHE LE HA PRODOTTE — MISURATO**
  (2026-09-19, `csv/_blob_nelle_voci.py`, output `csv/_blob_nelle_voci_2026-09-19.txt`):
  **151 voci, 38 col blob (25 %), e 69 citano NUMERI DI MISURA senza blob.**
  `RAMIFICAZIONI` 36/119, `COMPONENTI_PROMOSSE` **0/23**, `INVENTARIO` 2/9.
  **Non e' un presidio: e' una MISURA** — non impedisce niente e **non verifica che il blob citato
  sia quello GIUSTO**, solo che ce ne sia uno. **Un presidio ATTIVO su prosa libera NON e' stato
  trovato**, e va detto invece di scrivere l'ennesima nota: ogni riga di prosa contiene numeri
  (date, percentuali, numeri di riga), e un controllo che segnala tutto non lo legge nessuno.

- **PRESIDIO — DURANTE UN RUN, NESSUN FILE DEL PERCORSO IN USO SI MODIFICA: non solo il simulatore,
  ma anche il DRIVER e ogni script che il processo ha importato** (regola di Luca, 2026-09-19).
  **Il mandato del 19/9 diceva «NON toccare il simulatore finche' il run non e' finito»: il DRIVER
  era in uso e NON era coperto**, e la patch della ripresa gli e' stata applicata **mentre il run a
  6000 passi girava** (poi ripristinata, `228eb07`). **E' rispettare la LETTERA superando
  l'INTENZIONE**, ed e' il modo in cui un vincolo scritto bene viene aggirato in buona fede.
  **LA PROVA DICE CHE STAVOLTA NON C'E' STATO DANNO, NON CHE FOSSE SICURO** (`23f783e`, **3/3**:
  ripartendo dal passo 1800 si riottiene **identico** lo snapshot 1860, scritto durante la finestra
  della patch; 113 campi confrontati, 0 diversi, e il controllo positivo ne trova 84 diversi contro
  un altro istante, quindi lo zero significa *identico* e non *criterio cieco*).
  **PERCHE' E' ANDATA BENE, e perche' non basta:** Python compila il sorgente **una sola volta**,
  all'avvio, e non lo rilegge; il `.pyc` del driver era del giorno prima e **nessuno lo importa**
  (viene solo eseguito come `__main__`); gli snapshot sono scritti **dall'immagine in memoria**.
  **MA SE QUEL DRIVER LEGGESSE UNA CONFIGURAZIONE A RUNTIME, O FACESSE UN RELOAD, LA STESSA MOSSA
  AVREBBE ROTTO UN RUN DA SETTE ORE E MEZZA** — e non ci sarebbe stato modo di accorgersene se non
  dai numeri, alla fine.
  **REGOLA OPERATIVA: finche' un run e' in corso, il file sul disco deve restare quello che lo ha
  lanciato.** Il punto **non** e' se il processo se ne accorge: e' che per tutta la durata del run
  il repo direbbe una cosa diversa da quella che sta girando. Se serve modificare uno strumento in
  uso, si lavora su una **COPIA** e si porta la modifica sul file vero **a run chiuso**.

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
