# RELAZIONE — per Claude web · **aggiornata 2026-09-20 (sera)**

> **Scritta per Claude web**, che legge il repo e non ha la conversazione.
> Branch `fork-su2`. **Simulatore sul disco: `dbadb71f`** *(sha1 dei BYTE GREZZI, convenzione
> `csv/_presidio.py`; il blob **git** dello stesso file e' `5fc5bfdf` — **sono due numeri diversi
> per lo stesso file**, vedi `CLAUDE.md` §5-quinquies)*. Gate in `CLAUDE.md` §0 a `c0803713`,
> **non ri-timbrato di proposito**.
> Il documento e' **cumulativo e append-only**: i fatti stanno nell'ordine in cui sono nati, e
> l'ultimo lavoro e' **in fondo**.
> **⚠ SE LEGGI UNA COSA SOLA, LEGGI IL §0-OGGI QUI SOTTO.** Sotto di esso restano il §0-ante del
> **16 settembre** e il §0 del **15**, tenuti perche' la sequenza conti — **ma NON sono lo stato
> attuale.**

---

## 0-OGGI. **DOVE SIAMO IL 2026-09-20 (sera)** — il dettaglio e' nelle nove sezioni del 20/9, in fondo

> **NESSUN RUN E' IN ESECUZIONE. Nessun dato nuovo di fisica e' stato prodotto oggi.**
> **La giornata e' stata di MISURA e di CURA, e il simulatore e' cambiato quattro volte, tutte
> sigillate.**

**① IL FATTO PIU' GRANDE: il run a `sep = 8` girava su QUATTRO SISTEMI SEPARATI.** Il grafo era in
**quattro componenti connesse con ZERO archi fra loro**, dal passo 6 al 2700, e i due picchi del
grado erano **la semina**, non una forma emersa *(`Z65`)*. **Tutto cio' che e' stato osservato
finora e' avvenuto in quattro sistemi che giravano nello stesso programma.**
**E il pannello del campo mostrava interferenza FRA le masse** — `campo_spaziale` somma su **tutti
i nodi**, non sugli archi. **Il pannello non mentiva: la lettura si'.**

**② QUATTRO CURE, tutte sigillate, nessuna con numeri scelti:**

| cosa | sigillo | esito |
|---|---|---|
| **`scala_p`** *(`Z67`)* | **`5/5`** | il punto fisso **`median(ampiezza) = tanh(1)` e' SCIOLTO** (`0.7616 -> 0.1423`); `sin2` non e' piu' **saturo a 1**; **`ZETA_VIR` adesso frena del `19 %`**, prima non frenava quasi nulla |
| **`PASSO 2`, tre gruppi** *(`Z68`)* | **`3/3`** | la diagnosi del mandato era **sbagliata**: non la lunghezza, **l'ORDINE** |
| **`PASSO 1` sui dieci** *(`Z69`)* | **`3/4 + 1 FAIL ATTESO`** | **sei guardie proteggono da un difetto GIA' CURATO.** Il `FAIL` e' la riclassificazione di `nb_grav_proiez` da `(a)` a `(c)`, **predetta prima del sigillo e APPROVATA da Luca** |
| **driver: `--sep` + ripresa** | **`4/4`** e **`5/5`** | pronti per il run, non usati |

**③ IL REPERTO DI METODO, ed e' il piu' trasportabile:** **cinque volte in due giorni un criterio e'
sopravvissuto alla ragione che l'aveva generato.** Quattro erano criteri di **sigillo**
*(`N3b`, `M1b`, `M3c`, e il mio `V2` che ha bocciato un comportamento corretto)*; **la quinta e' una
famiglia di sei guardie NEL CODICE**, che proteggono da difetti curati mesi fa. **La forma e' la
stessa, e non si riconosce dal contenuto: si riconosce dalla forma.**

**④ E COSA NON E' STATO FATTO, per essere espliciti:** il **`PASSO 2`** del secondo giro *(gli
`else` dichiarativi sui dieci siti)*; il **PANNELLO FEDELE** *(un pannello che interpola `psi`
invece di ricostruirlo con la FFT)*; e **IL RUN a `sep = 4.0`**, che e' **l'ultimo dei tre** per
decisione di Luca. **L'ordine e' `① guardie -> ② pannello -> ③ run`, ed e' scritto in
`doc/STATO_RUN.md`.**

**⑤ DUE DECISIONI FERME, che aspettano Luca:** la forma del contatore sulla catena
`:3517`-`:3526` *(tre contatori di «salti» o uno con tre conteggi etichettato «quale ramo»)*, e il
via libera al `PASSO 2`.

**⑥ E TRE DIFETTI MIEI, dichiarati perche' si ripetono:** il cast a `float` che **scartava la parte
immaginaria di `psi`** *(lo stesso errore di `_mod()`, due volte in un giorno)*; un mio criterio di
sigillo **scaduto** che ha prodotto un FAIL falso; e **tre messaggi di commit bucati dai backtick**
in `git commit -m` — da cui la regola, ora permanente: **sempre `-F`.**

---

## 0-ante. **L'ULTIMO GIRO (2026-09-16) — in quindici righe.** Il dettaglio e' il §9

> **Blob: `08784685` -> ... -> `c57800c1`.** `soliton_simulator.py` e' stato toccato **tre volte**
> oggi, tutte e tre committate **prima** di qualunque run.
>
> 1. **`S` e' CHIUSA: rumore.** 4 semi per braccio, IC95 con `t(3)`: OFF `[89.722, 90.022]`,
>    ON `[89.995, 90.103]` — **entrambi contengono 90**. E `OFF s3` vale **89.9999**, il null esatto.
>    *(Resta aperta una domanda DIVERSA: il contrasto ON-OFF `+0.177` esclude lo zero, ma i due
>    bracci differiscono anche di ~7x in RISOLUZIONE -> voce `S2`.)*
> 2. **`R` e' REFUTATA**, dal dato piu' pulito del lotto: `tau` cambia di **due ordini** (+1.708 ->
>    +0.020) e **`sigma` si muove di 0.0013**, contro una barra di sistema di 0.030.
> 3. **`ESITO (I)` confermato QUATTRO volte**: `-1.0498 / -1.0592 / -1.0562 / -1.0554` contro il
>    `-1.056` del tracing. Due bracci, due leggi di `tau`, l'esponente non si muove di 0.01.
> 4. **Il FDT rifatto sul sistema pulito: CENTO volte meglio, MILLECINQUECENTO volte insufficiente.**
>    `kT/Lam` da ~2e7 a **1.2e5**, ma il disordine resta **726-3081 volte** piu' veloce dello
>    smorzamento. **NON SI CABLA.**
> 5. **Lo spin e' ACCOPPIATO MA SENZA BILANCIO** (terzo esito, non previsto dal mandato): decide
>    dove la materia si divide e con che verso la gravita' tira, ma **nessun canale trasferisce una
>    grandezza conservata**. Il torque **non e' azione-reazione** (dimostrato dalla formula) e nel
>    file **non esiste un'energia totale**. **Quindi `lambda` NON SI DERIVA**: manca la grammatica.
> 6. **Il marchio dello STRATO 1 e' TOLTO: `tau` SEGUE `cs`, misurato per la prima volta.**
>    Sigillo **25/27 + 2 FAIL ATTESI** (previsti e committati prima). **`S8b`: rapporto `cs=8/cs=1`
>    = 7.660686976 = atteso** — se `cs` fosse ignorato varrebbe esattamente 1.000000000.
> 7. **I DUE `theta` sono chiusi** (`C19`): `theta_coord = |omega|*DT` e `theta_prop = |omega|*dt_n`
>    girano ora **insieme**, col controllo d'identita' a `4.6e-16`. **Differivano del 26 % sulla
>    mediana.** E ne e' uscita una correzione: la catena `sigma + tau/2` **assumeva `pend(r) = 0`**,
>    mai verificato.
> 8. **Taglio spettrale CABLATO** (`--rumore-colorato`, flag OFF). **`N7` VINTO**: la ricorsione usa
>    `dt_n = DT*r` **per nodo**, errore `0.000e+00`, contro `6.142e-01` col `DT` nudo. `N2` aperto.
> 9. **DUE CORREZIONI DI DIFETTO, SENZA FLAG** (decisione di Luca, §9.12):
>    **①** `_xi_rumore` **non si eredita** — `xi` e' l'AMBIENTE, non una proprieta' del nodo.
>    Correlazione padre-figlio **da `+1.0000` a `+0.0065`** su 258 coppie.
>    **②** `inerzia = max(rho*(CS_M/cs)^2, 1e-6)` — il fattore `cs^-2` che la derivazione impone e
>    che **mancava**. **`M2` (il decisivo) PASS: `max|A-B| = 0.000e+00`, nodi 3070 = 3070.**
>    **⚠ Ma l'effetto OGGI e' minuscolo — fattore mediano `1.0000048` — ed era scritto PRIMA.**
> 10. **La trappola CRLF e' chiusa alla radice** (`.gitattributes`, `eol=lf`). Aveva morso **due
>    volte**: la prima per un mio `git checkout`, la seconda **da sola**, fra due commit.
> 11. **⚠ QUATTRO SIGILLI SI SONO ROTTI OGGI, E NESSUNO LO HA DETTO**: `AttributeError` a S2
>    (metodo estratto assente dal guscio), `AttributeError` a N7 (`Generator.normal` read-only),
>    **loop infinito** a N2 (46 minuti al 68 % di CPU), e **due criteri SCADUTI** che hanno prodotto
>    FAIL falsi. **Una sola forma: un diagnostico che tocca i globali del simulatore, o ne elenca i
>    metodi a mano, si rompe appena il simulatore cambia forma — in SILENZIO.**
> 12. **⚠ E TUTTI I DATI DI OGGI PORTANO IL MARCHIO**: prodotti **prima** delle due correzioni,
>    cioe' su un **sistema diverso** da quello corrente. **La campagna va RIFATTA.**
> 13. **E LA CONSERVAZIONE E' STATA MISURATA PER LA PRIMA VOLTA:** **`L_tot = somma(I*omega)` cresce del ~3.4 % a ogni passo con crescita**, sia prima sia dopo
>    la correzione ②. **La violazione non e' piu' argomentata: ha un numero.** E la correzione
>    **non la chiude a questa densita'**, com'era scritto prima (fattore 1.0000048).
> 14. **⚠ E TRE CRITERI DI SIGILLO SBAGLIATI, TUTTI MIEI, TUTTI LO STESSO GIORNO** (`N3b`, `M1b`/`M3`, `M3c`): scritti dal **modello mentale** del codice invece che da una
>    **misura**. Presidio nuovo in §9. **Un FAIL falso costa piu' di un sigillo mancante.**
>
> 13. **LA PRIMA PROMOZIONE MAI FATTA: `STEP2_OROLOGIO` E' FISICA DI DEFAULT** (§9.15). La sezione
>     A del registro delle componenti era **vuota**; ora ha la sua prima voce, coi tre criteri §10 e
>     **il criterio di retrocessione scritto AL MOMENTO**, non dopo. Risigillo col braccio OFF vero:
>     **9/10 PASS + 1 FAIL ATTESO**, `S2` = `0.000e+00` con **nodi 2924 = 2924, shape divergenti 0**.
>     *(L'argomento non e' «funziona meglio»: e' «la sua assenza e' un DIFETTO» — un sistema in cui
>     l'EM non risponde alla metrica e' sbagliato, non diverso. E lo stesso esponente `cs^2` era gia'
>     stato derivato, per una strada indipendente, nell'inerzia: **consistenza trovata, non costruita**.)*
>
> 14. **⚠ E UN FALSO PASS INTERCETTATO PRIMA CHE ACCADESSE — vale piu' della promozione.**
>     **Ribaltare un default converte ogni braccio di controllo ottenuto per OMISSIONE del flag in un
>     duplicato del braccio di prova.** `_sigillo_step2.py` prendeva il braccio OFF cosi': senza
>     l'adeguamento, **`S2` avrebbe confrontato ON contro ON e sarebbe PASSATO SEMPRE**, con le
>     **shape UGUALI** — quindi invisibile **anche alla guardia delle shape**, che e' il presidio
>     scritto apposta per quella classe di falso PASS. **Regola nuova in §9.**
>
> 15. **`TW_SPINORE` NON e' stato acceso: la legge CODIFICATA non e' quella DICHIARATA** (§9.16).
>     Il commento dice «pilota il Bloch di `tw/2`» (un **ANGOLO**); il codice somma `tw/(4π)` a una
>     **VELOCITA'** angolare, e l'angolo che ne esce e' **628.3 volte piu' piccolo** (`= 2π/DT`).
>     Il termine finisce nella **memoria** `omega_s`, dove lo stesso file dichiara che darebbe
>     «accumulo/divergenza», e **non e' diviso per l'inerzia** — unico del blocco.
>     **Il mandato diceva «sigillato e poi acceso»: ho SEGNALATO invece di eseguire (P1).**
>     **Non dico che sia trascurabile**: lo 0.054 % e' un'**ampiezza**, la domanda e' **direzionale**.
>     **DECISO da Luca: RESTA SPENTO.** Il fronte **non si chiude** — resta aperto come **difetto di
>     cablaggio**, e a chiuderlo sara' **una decisione di fisica**, non una misura in piu'. Il
>     commento nel codice **resta falso**, quindi il presidio e' in **`CLAUDE.md` §9**: il rischio
>     non e' dimenticarla, e' **riaccenderla credendo di aggiungere `tw/2`**.
>
> 16. **AUDIT DI LETTURA DELLE LEGGI, e una regola nuova: SI MISURA PER PROMUOVERE, SI DIMOSTRA PER
>     ESCLUDERE** (§9.17). Una misura dice *«questa legge produce un effetto»*, **non dice se ha
>     senso**: `SPIN_LARMOR` produceva un effetto ed era **sbagliata**, `cs^-2` non ne produce quasi
>     ed e' **necessario**. **Nove leggi escluse per DIMOSTRAZIONE**, ognuna con **quale proprieta'
>     rompe** e la riga che lo prova; **otto confermate sane**; e **DUE motivazioni della tabella
>     proposta CORRETTE dal codice** — `SYNC_UPDATE` **non** accende lo scuotimento (lo **sposta**),
>     e `LS_AZIM` non pecca di «asse di laboratorio» ma di **baricentro GLOBALE** (§4) e **indice
>     cablato** (§3). **Il codice delle escluse NON si cancella:** e' l'evidenza che spiega perche'
>     esistono i loro sostituti.
>
> 17. **VERDETTO SULLO STEP 2: la RETROCESSIONE NON SCATTA** (§9.18). Campagna a variabile singola,
>     **8/8 run**, 4 semi **appaiati**, criterio committato prima: **0 firme di SPIN su 11** e
>     **0 osservabili U(1) su 5** escludono lo zero. La promozione **regge**, e per la ragione su cui
>     poggiava: `_phc` e' una **fase globale**.
>     **⚠ MA il punto vero e' un altro: meta' di quei nulli NON HA POTENZA.** La risoluzione varia di
>     **tre ordini** — **0.213 %** su `chi`, **129 %** su `|<n>|`, **603 %** sulla coerenza di segno.
>     **Ventidue righe tutte «contiene lo zero», e non significano la stessa cosa.** Il risultato si
>     scrive come **limite superiore**, e dove la barra e' piu' larga del valore si scrive
>     **«non misurato»**. Nuovo presidio in §9.
>     **E una lacuna strutturale:** fra **256** colonne **nessuna** misura l'orologio direttamente.

---

## 0. L'ULTIMO GIRO (2026-09-15, sera) — in dodici righe

> 1. **Trovato e curato un difetto silenzioso:** la cache `_cs_nodo_prev` veniva **scartata a ogni
>    mitosi**, quindi nel **71.88 %** delle chiamate `tau = d/cs` calcolava `tau = d/CS_M`.
>    Colpiva anche **lo STRATO 1, gia' sigillato 23/23**. Sigillo della patch: **5/5 PASS**.
> 2. **La cura NON chiude la FASE 2.** La pendenza T3 va da **-0.4265** a **-0.4710** contro
>    l'attesa **-0.69**: **16.9 % del divario**, non la meta'. `theta` resta a **42.8 giri/passo**.
>    **⚠ IL "16.9 %" E' STATO RITIRATO — vedi il punto 4. Lo lascio scritto perche' la sequenza
>    conti: e' cosi' che un numero sopravvive mezza giornata prima di cadere.**
> 3. **Due predizioni opposte, entrambe sbagliate:** il mandato diceva ~50 %, **io dicevo zero**.
>    L'errore mio e' spiegato al §6-duodecies ed e' di tipo generale.
> 4. **Il controllo sui semi ha SMENTITO il punto 2** (§6-terdecies): su 3 semi il segno di `Delta`
>    **non è nemmeno concorde** (-0.0445 / **+0.0367** / -0.0635), `t = -0.77`. **Il "16.9 %" è
>    ritirato.** E la scoperta collaterale vale più della vicenda: **la barra d'errore usata in tutto
>    il programma è 3 volte troppo piccola** (dispersione fra semi **0.030** contro `SE` interna
>    **0.010**).
> 5. **SETTIMO difetto silenzioso, il più grosso** (§6-quaterdecies): `_psi_spin_prec` non era esteso
>    alla mitosi → la guardia **esatta** di `ritmo()` scartava il ramo a **4π** nel **95.33 %** dei
>    casi → **la FASE 5 (doppia copertura) non è MAI entrata in funzione.** Curato, **6/6 PASS**.
>    **Non** è "tempo proprio stale": è **l'orologio scalare storico invece di quello dichiarato.**
> 6. **`S4` di quella cura ha misurato la cosa sbagliata:** `median(r) = 1.0` **per costruzione**,
>    con qualunque orologio. Secondo caso del **punto fisso auto-normalizzante**.
> 7. **ESITO (A) sul braccio OFF della prima misura vera** (par.6-sexdecies): nessuna firma si
>    stacca dal casuale, su 2 semi. **Ma theta e' a 92.8-98.7 giri/passo, il DOPPIO di quanto avevo
>    scritto**: (A) e' l'esito che l'aliasing produrrebbe da solo.
> 8. **--cs-dinamico era SPENTO** (par.6-septdecies), dimostrato da TRE vie. Decisione di Luca:
>    **ci va SEMPRE**. E il sigillo 23/23 dello STRATO 1 **non ha mai esercitato la dipendenza da
>    cs** (par.6-octodecies): i quattro run in partenza sono **la prima volta che gira davvero**.
> 9. **Due REGOLE nuove** (par.6-vicies): la **promozione delle componenti** (par.10) e **un dato
>    deve portarsi dietro le proprie condizioni** (par.9). Dal primo e' uscito il reperto dei
>    **10 flag gia' accesi** che non sono mai passati per nessun criterio.
> 11. **I QUATTRO BRACCI, esito finale** (par.6-unvicies): **(A) NON conclusivo**. Nessuna firma
>    emerge **nemmeno a risoluzione 6.4x migliore** (theta 96.4 -> 15.1 giri/passo). Le obiezioni
>    "la FASE 5 non era attiva" e "cs era spento" sono **entrambe chiuse**: e' il negativo piu'
>    pulito della sessione. Ma theta resta **oltre il giro per passo**, quindi la frase "lo spin non
>    si organizza" resta **INDICIBILE**.
> 12. **Due presidi di metodo, entrambi correzioni a me** (par.6-duovicies): **due semi non bastano
>    per una barra fra semi** (t con 1 gdl = 12.7), e **una soglia su un sistema che cresce va
>    dichiarata con l'istante** (cs_std/cs: venti volte in 450 passi).
> 10. **E la domanda aperta più utile non cerca un bug** (§6-quindecies): l'attesa `-0.69` assume che
>    `sigma` sia indipendente da `tau`, ma c'è un **anello** che lo mette a valle. **Forse è il
>    BERSAGLIO a essere mal calcolato.** Da provare **per prima**; **non lanciata**, e il numero
>    **non è nei dati** come si credeva.

---

## 0-ter. **I SEI PATTERN COMPORTAMENTALI** (regole di Luca, 2026-09-16) — leggi questi prima di proporre qualsiasi cosa

> **Sono REGOLE, non suggerimenti**, e stanno anche in `CLAUDE.md` §0-ter. Sono qui perche' un
> Claude web nuovo le deve ricevere **leggendo questa relazione**, senza doverle far dare di nuovo.
> Nascono tutte da errori realmente commessi su questo repo, quasi tutti **nello stesso giorno**.

**P1 — NON USARE L'ASSOCIAZIONE SENZA VERIFICARE LO STORICO.**
Prima di proporre una diagnosi, una cura o un mandato, **rileggere dal DISCO** cio' che e' gia'
stabilito su quel punto (`doc/RAMIFICAZIONI.md`, questa relazione, i documenti di reperto) e
verificare di **non contraddire un fatto gia' misurato**. Se si contraddice: **o c'e' un dato nuovo
che lo supera — e lo si dichiara — o la proposta cade.**
L'associazione genera **candidati**, non conclusioni. Le frasi *«manca X»*, *«il problema e' Y»*,
*«basta fare Z»* sono il **segnale d'allarme**: li', prima di scrivere, si controlla.
Se rileggendo **non si trova nulla**, **dirlo**: *«non ho un fatto stabilito su questo, sto
proponendo per analogia»*.
*(Quattro precedenti, tutti del 2026-09-15: `--tau-luce` messo nella casella del turbo; `theta ~43`
trasportato fra due configurazioni; `--step2-orologio` fra gli esperimenti benche' derivato e
sigillato 10/10; **«universo in accelerazione senza freni» quando il freno `−omega/tau` era gia'
misurato** e anche il ginocchio — previsto `7.059e4`, misurato `7.271e4`, scarto x1.03.)*

**P2 — PRIMA DI ESCLUDERE UN FLAG: forza il sistema o lo CORREGGE?**
Escludere una **correzione** significa misurare un sistema che si sa difettoso.

**P3 — NESSUNA STATISTICA SENZA BARRA D'ERRORE**, e per confronti **fra bracci** si usa la
**dispersione FRA SEMI**, mai la `SE` interna a un singolo run (**C10**: la pendenza cambia di
**0.03 a codice invariato**, contro `SE` interna ~**0.010**). **Per una barra fra semi servono
>= 4 semi**: con 2, `t(0.025,1) = 12.706`.

**P4 — PRIMA DI MISURARE SE UNA GRANDEZZA CAMBIA, VERIFICARE CHE SIA LIBERA DI CAMBIARE.**
Una quantita' normalizzata sulla propria mediana non puo' muoversi: misurarla e' un test vuoto
(**C12**).

**P5 — OGNI RAMO `else` / fallback / `getattr(..., default)` su un percorso fisico VA CONTATO.**
Un fallback mai misurato e' un comportamento sconosciuto; uno che scatta l'80 % delle volte **non
e' un fallback: e' il comportamento principale** (**C7** 71.88 %, **C11** 95.33 %).

**P6 — OGNI CSV DI MISURA porta BLOB, SEME e TUTTI i flag** che distinguono quel run dagli altri
bracci. Un file che si distingue dagli altri **solo per il nome** non e' un dato: e' un ricordo.

> **Uso:** P1 e' un prerequisito di **scrittura**; P2 e P6 sono check di **preparazione** di un run;
> P3, P4, P5 sono check di **lettura** di un risultato. Un run che non soddisfa P6 in **ogni** campo
> **non si conta**.

---

## 1. IN UNA RIGA (2026-09-14 — storico, resta valido)

> **Lo scan del turbo è chiuso: ESITO B.** Con `cs` forzato fino al **5 % di `CS_M`**, lo Step 2
> **non muove lo spin**: i due bracci sono indistinguibili su tutte e tre le firme.
> È il **sesto lato** dello stesso fatto. **Lo scan ai K minori si ferma qui**, risparmiando
> ~40 ore di macchina.

Documento del verdetto: **`doc/ESITO_scan_turbo_K300.md`** — con i dati committati accanto.

---

## 2. IL VERDETTO — i numeri, contro la predizione scritta PRIMA

Due bracci, seme 1, 2000 passi, `exit = 0`, **un solo interruttore di differenza**
(`--step2-orologio`). Tutto il resto identico, verificato dal blocco `# RUN_PARAMS` dei CSV — non
dalla memoria.

**Il forcing ha morso, molto oltre il bersaglio:**

| | `cs_min / CS_M` finale |
|---|---|
| Step2 ON | **0.047** |
| Step2 OFF | **0.032** |

Il bersaglio era «almeno il dimezzamento». Siamo a **un ventesimo**. Traiettoria: 2.000 → 0.610
(passo 400) → 0.204 (1000) → 0.095 (2000).

**E le firme non si muovono lo stesso** (medie su 20 campioni, gradi):

| firma | ON | OFF | nullo casuale |
|---|---|---|---|
| `chi` materia | **89.9865** | **89.9941** | **90.000** |
| dispersione | 39.199 | 39.196 | **39.171** |
| `chi` **p90** (archi più densi) | **90.0309** | **89.9609** | 90.000 |
| \|⟨n⟩\| in unità di 1/√N | 0.83 | 1.00 | ~1 |

La differenza fra i bracci sulla firma principale è **0.008°** contro una dispersione di **39.2°**.

**Terza firma, quella che discrimina** — autocorrelazione spaziale su 14 bin
(`csv/_test_fork/_autocorr_k300.txt`):

| | vicino | lontano |
|---|---|---|
| ON | −0.0200 | 0.0032 |
| OFF | 0.0148 | 0.0014 |

**Piatta a zero ovunque, in entrambi.** Il segno del "calo" è addirittura **opposto** fra i due:
è rumore di campionamento, non struttura. **Nessuna scala di dominio.**

| esito predetto | misurato |
|---|---|
| **A** struttura (`chi` intermedio, autocorrelazione che decade) | no |
| **B** il chiuso regge | **SI** |
| **C** artefatto solo a K estremo | no — non c'è **nessun** effetto da estrapolare |

---

## 3. PERCHÉ LO SCAN SI CHIUDE (la logica dichiarata prima, non dopo)

> Se al forcing **massimo** le firme sono piatte, l'esito B è indicato e i K minori sono superflui:
> nessun effetto a K=300 implica nessuno a K minori.

Questa asimmetria era **scritta e approvata prima di partire**, ed è la ragione per cui ho iniziato
da K=300 invece che dal basso. Ha fatto il suo lavoro: **un quarto del costo**, stessa conclusione.

---

## 4. IL SESTO LATO

| # | misura | esito |
|---|---|---|
| 1 | teorema di inerzia (Strato 0) | la connessione è uno **specchio** della materia — 1.57e-15 |
| 2 | frozen-o-noise | ciò che rispecchia è **rumore** |
| 3 | Kuramoto | refutato — K-frozen **byte-identico** a OFF; K-noise = NO-rumore |
| 4 | FDT | `E[n'] - n = -a^2 n`, **dimostrato**, verificato a 1.28e-07 |
| 5 | shake-then-freeze | `chi` deriva di **−0.33°** in 600 passi da stato casuale |
| 6 | **Step 2 con `cs` vivo** | **nessuna differenza ON/OFF a `cs/CS_M = 0.047`** |

Sei misure indipendenti, **un solo fatto**: il settore di spin non ha una forza organizzante
emergente, e **non ne acquisisce una** agganciando l'orologio alla metrica.

---

## 5. I DUE CAVEAT, INTERI — quello che il verdetto **non** dice

**1. Un solo seme.** `CLAUDE.md` §2.7: nessuna conclusione su un solo seme. Questo è **screening**,
legittimo come tale, **non** un fatto pubblicabile. Un secondo seme costa ~1.7 h per braccio.

**2. Il turbo ristretto è un ISOLAMENTO DIAGNOSTICO, non il regime reale.** `GAMMA` è **condiviso**
fra `cs`, `satura()` e la saturazione del campo spinoriale. Restringerlo a `_cs_nodo` **rompe di
proposito** quella condivisione; nel regime reale ad alta densità cambierebbero **entrambi**.

> La formula onesta: **«il gradiente di cs, IN ISOLAMENTO e fino al 5 % di CS_M, non retroagisce
> sullo spin»** — un **condizionale**.

E vale in entrambe le direzioni: **un negativo in isolamento è più debole, non più forte**, di un
negativo nel regime vero. Non prova che nel regime reale non succeda nulla; prova che **questo
canale, da solo, non basta**.

**3. Una correzione a me stesso.** Nella versione precedente di questa relazione avevo scritto che
nel braccio OFF le colonne `cs_*` sarebbero state `NaN`. **Falso:** entrambi i bracci hanno
`--fork-su2-mem`, che scrive `_cs_nodo_prev`, quindi `cs_*` è popolato in tutti e due — ed è
proprio da lì che vengono i numeri del §2.

---

## 6. DUE COSE CHE ASPETTANO UNA TUA DECISIONE

### 6.1 `_pesi()` — la premessa del mandato di ottimizzazione è falsa

FASE A fatta, **FASE B non eseguita**, come prescrive il mandato (se la premessa non regge,
fermati). Documento: **`doc/REPERTO_pesi_ricorsione.md`**.

Le 16 chiamate per passo **non** sono ricalcoli ridondanti di `calcola_psi()` (quello è il
**12.8 %**). L'**80.9 %** passa da `stato_crossover()` via `massa_critica_adattiva()`, e il
**43.6 %** è **`_pesi()` che chiama se stessa** un livello più sotto:

```
_pesi -> _lam_archi -> lambda_nodi -> massa_critica_adattiva -> stato_crossover -> _pesi
```

Il ciclo non è infinito perché `lambda_nodi` ha già la guardia `_calcolo_schermatura`, che nel ramo
rientrante restituisce **LAM costante** invece della schermatura vera. **Quindi le due `_pesi()`
calcolano cose diverse**, e cachearne una per l'altra non romperebbe l'ultimo bit: **cambierebbe la
schermatura**. Tre strade nel documento, §5. **Non ho scelto e non ho toccato niente.**

### 6.2 `:5318` — un diagnostico che non segue la fisica

Il diaglog **re-implementa `cs` inline** e non chiama `_cs_nodo`: **sotto turbo quella colonna
mente**. Dichiarato e non risolto (la tua indicazione era «applicazione UNICA»). I numeri di questa
relazione **non** vengono da lì: vengono dall'osservatore, che legge `_cs_nodo_prev`, il `cs` vero.

---

## 6-bis. IL BILANCIO DEI TASSI (2026-09-15) — **FASI A, B, C CHIUSE**, e un REPERTO

Documento: **`doc/BILANCIO_ordine_spin.md`**. Nessuna modifica al simulatore (blob `f5887254`).

**La riformulazione.** Alla mitosi il figlio eredita il padre per **copia esatta** e nasce
**adiacente**: ogni nascita crea una coppia con `chi = 0` (misurato, `0.0000` esatto). Ma `chi = 90`
ovunque. Quindi **l'ordine non manca: nasce di continuo e viene distrutto.** Non serve un meccanismo
ordinante — serve misurare il **bilancio**.

**FASE B — i due tassi** (osservatore **sigillato PASS**: 19 campi + stato RNG a `0.000e+00`, con N
confrontabile). Scena reale, 250 passi, **due semi**, 4163 coppie padre-figlio:

| | seme 1 | seme 2 |
|---|---|---|
| `tau_dec` (decorrelazione della coppia) | **0.63 passi** | **0.63 passi** |
| `tau_mit` locale (una mitosi nel vicinato) | 187 passi | 210 passi |
| rapporto | **295** | **335** |

> **`tau_dec` << `tau_mit` di quasi TRE ORDINI. Dominio della distruzione.**

**E il confondente e' ESCLUSO, non stimato.** All'eta' 1, quando `chi` e' gia' 89.7 (nullo:
90.000 +- 39.171), la **distanza e' invariata** (0.540 contro 0.539) e l'**arco diretto e' vivo al
100%**. Decorrelano **da adiacenti e connessi**: e' disordine, non disaccoppiamento geometrico.

**FASE C — l'ipotesi «dare memoria combatte il disordine» e' REFUTATA, e c'e' un reperto.**
Leggendo `omega_s` **direttamente dal simulatore**:

> **il Bloch fa ~67 GIRI COMPLETI per passo** (2.4e4 gradi/passo; 99.3% dei nodi oltre il giro
> intero). **Il settore di spin NON e' risolto nel tempo dal passo DT.**

Perche': `omega = coppia/inerzia`, la coppia e' **ordinaria** (0.06) ma l'inerzia e' la **densita'**,
che vale **1.2e-7** — sette ordini sotto l'unita'. Il pavimento `1e-6` **non e' la causa: la
mitiga** (senza, `omega` sarebbe otto volte piu' grande).

**E' la stessa radice del problema noto su `cs`**, con segno opposto: la densita' e' minuscola alle
scale simulabili, quindi **congela la metrica** (`cs` fermo a `CS_M`) **e fa esplodere lo spin**
(`omega` divisa per quella densita').

**Perche' piu' memoria peggiorerebbe:** il punto fisso del rilassamento e' `omega_eq = tau · F`,
cioe' **omega e' proporzionale alla memoria**. Il canale ha gia' la memoria piu' lunga del sistema
(2470 passi) e ruota di 67 giri per tick. La memoria vive sulla **velocita' angolare**: conserva la
rotazione, non la direzione. **Nessun canale merita piu' memoria**, e ognuno e' escluso col suo
numero (la densita': il 99.7% dei nodi e' sotto il pavimento; `cs`: fase globale, `nb` invariante a
3.3e-16, piu' l'esito B; i pesi: il campo e' al valore casuale entro il 7%).

**Cosa cambia per i sei lati.** Restano **validi** — nessuno e' invalidato. Cambia
l'**interpretazione**: non dicono «non esiste una fisica ordinante», dicono «**in questo regime
numerico nessun ordine puo' sopravvivere a un tick**». Due strade aperte, entrambe decisione di
Luca: un **sotto-passo per lo spin** (lo stesso principio di `nsub` per la metrica), oppure
**rileggere tutto dove la densita' e' O(1)**.

**Caveat:** i 67 giri/passo sono misurati a **passo 60, un seme, una scena** — vanno rifatti prima
di trattarli come stabili. `tau_dec` invece e' su due semi e 4163 coppie.

---

## 6-ter. GILBERT / FDT (2026-09-15) — **ipotesi NON confermata, nessun cablaggio**

Documento: **`doc/ANALISI_gilbert_fdt.md`**. Mandato: *il termine mancante e' lo smorzamento di
Gilbert, e il FDT ne fissa il coefficiente?* **Testato. Cade — e cade prima della derivazione.**

**Due premesse del mandato sono COMMENTI STALE.** E' il caso d'uso di §0:
- *"`omega_s` e' conservativo: si conserva, non rilassa"* (righe **868** e **1803**) -> **FALSO**.
  L'unico aggiornamento per passo e' la riga **1918**, che contiene `- omega_src/_tau`:
  **la dissipazione c'e' gia'.**
- *"il calcio termico alimenta `omega_s`"* (riga ~1590) -> **FALSO**: e' dentro `semina()`, quindi e'
  il punto zero **alla nascita del nodo**, non una sorgente per passo.

Quindi lo schema *"accumulatore conservativo + rumore che lo alimenta = crescita illimitata"*
**non descrive questo codice**: mancano entrambi i pezzi.

**E la crescita non e' quella che avevo dedotto nemmeno io.** Da un solo campione avevo inferito
crescita *balistica*; ho misurato la traiettoria **prima** di scrivere il verdetto (150 passi, 15
punti) ed e' **DIFFUSIVA**: `omega/sqrt(n)` costante entro il **4.6%**, `omega/n` varia di 3.5x.

**E c'e' un PLATEAU.** Random walk smorzato, `omega_eq = sigma*sqrt(tau/(2 dt))`:

| | |
|---|---|
| previsto | **7.06e4** |
| misurato al passo 150 | **7.27e4** (scarto x1.03) |
| theta al plateau | **112 giri per passo** |

> **La dissipazione non manca: c'e', funziona, e un equilibrio finito lo produce gia'.**
> Il problema e' *dove* sta quel plateau — e dipende dall'**ingresso** (coppia/inerzia), non
> dall'uscita. **La diagnosi corretta resta l'inerzia a 1e-7.**

**Il coefficiente si deriva davvero, e a zero parametri.** Dal rumore sul Bloch: `D = 2 amp^2/dt`;
imponendo che l'equilibrio di Langevin coincida con quello di Boltzmann,
`lambda = amp^2 |B| / (2 dt kT)`. Con l'unica temperatura parameter-free (`kT = Lam`, l'energia del
vuoto da cui il rumore stesso e' costruito) **`Lam` si cancella**: `lambda = |B|/(2 dt)`.

| tempo | valore |
|---|---|
| `tau_smorzamento` (allineamento FDT **derivato**) | **28.8 passi** |
| `tau_disordine` (rimescolamento **misurato**) | **0.0030 passi** |

> **Terzo ramo della regola scritta prima: lo smorzamento FDT e' ~10^4 volte troppo lento.
> REPERTO, non fallimento.** La FASE 2 **non e' partita**.

**Controllo di consistenza:** l'equipartizione darebbe `kT = 800` contro `Lam = 4.4e-5` — rapporto
~2e7. **Non e' equilibrio termico ma dinamico pilotato**, ed e' la ragione strutturale: il FDT
accoppia una dissipazione a una **fluttuazione**, e qui il termine dominante non lo e'.

**Non e' un fallimento dell'idea di Gilbert:** il termine LLG resta l'**unico** che allinea. Cade il
fatto che il suo coefficiente FDT basti *a questa scala*. Metterne uno piu' grande sarebbe
**sceglierlo** (§3) e mettere dissipazione senza fluttuazione: lo stesso errore, ribaltato.

**Una correzione a un fatto MIO.** `CLAUDE.md` §9 diceva (scritto da me ieri)
`omega_eq = tau * coppia/inerzia`, proporzionale a `tau`: e' il punto fisso **deterministico**, e
sovrastima di ~20x. **Corretto in §9**: `omega_eq ~ sqrt(tau)`. La conclusione operativa resta
(piu' memoria = piu' rotazione), ma l'esponente era sbagliato e la diagnosi *"manca la
dissipazione"* era **falsa**.

---

## 6-quater. `inerzia`: MASSA o FRAZIONE? (2026-09-15) — **FASE A chiusa: nessuna delle due**

Documento: **`doc/INERZIA_massa_o_frazione.md`**. Prima relazione scritta sotto la regola nuova
**§5-ter** (a ogni riscontro, una relazione, subito).

Il mandato chiedeva di scegliere fra due ipotesi su `inerzia = |Psi|^2`: **frazione normalizzata**
(scala come 1/N) o **massa vera**. **Dal codice non e' ne' l'una ne' l'altra.**

- **Non e' normalizzata.** `F = mat(w) @ (1.0 * e^{i phi})` e' una **somma pesata sui vicini**: non
  c'e' divisione per `N`, non esiste alcun vincolo `sum|psi|^2 = cost` in tutto il file, e `satura`
  e' un **tetto morbido** (asintoto `1/GAMMA = 20`), non una normalizzazione. Il codice prevede il
  **contrario** della firma (1): `|psi|` dovrebbe **crescere** col numero di vicini.
- **Non e' una massa.** `inerzia = max(_rho_sorgente(), 1e-6)` (riga **1891**) e' **letteralmente**
  il modulo quadro del campo: nessuna massa, nessun volume, nessun fattore. Solo il floor.

**E allora perche' vale 1e-7? L'ETA', non la normalizzazione.** In `_pesi()`:
`ramp = min(1, eta/TAU_A)`, con `eta += dt_n` (~0.01) per passo e **`TAU_A = 50`** nel regime
deterministico, quindi un nodo raggiunge **peso pieno solo dopo ~5000 passi**. Al passo 150
`ramp ~ 0.03`, e `w` va come `ramp_i*ramp_j ~ 9e-4`. **E i figli della mitosi nascono con `eta = 0`**,
quindi una frazione stabile della popolazione resta **permanentemente immatura**. Coerente con la
crescita gia' misurata di `Lam`: **7.45e-14 al passo 1 -> 1.32e-4 al passo 150**, nove ordini in 150
passi. Il campo **si sta accendendo**, non e' a regime.

**IL REPERTO — l'analisi dimensionale.** `w`, `F`, `psi`, `|psi|^2`, `B`, `nb`, `cross(B,nb)` sono
**tutti adimensionali**, quindi **`correzione/inerzia` e' adimensionale**. Ma la riga **1918** e'
`omega += dt_n*(correzione/inerzia - omega/tau)` e `theta = |omega|*dt_n` deve essere un **angolo**:
servirebbe **`[correzione/inerzia] = 1/T^2`**. In un corpo rigido `dw/dt = tau/I` lo da' **da se'**,
perche' coppia e momento d'inerzia portano entrambi `M L^2`. Qui il numeratore e' un puro prodotto
vettoriale geometrico e il denominatore una pura intensita' di campo.

> **Onestamente:** `CLAUDE.md` dice che `DT` e' un **contatore di tick**, quindi il modello potrebbe
> lavorare di proposito in unita' adimensionali, e allora non c'e' un "errore" da dichiarare. Ma
> resta la conseguenza: **non c'e' protezione dimensionale, e il valore di `omega` e' libero.**
> Nulla lo lega a una frequenza propria del modello (`cs/LAM`). Il "4000x il tetto di Planck" non e'
> un'affermazione fisica: **nel rapporto non c'e' alcuna scala di frequenza.** Ed e' anche il motivo
> per cui **riparametrizzare non puo' aiutare**: non ci sono unita' da riscalare.

**Per la FASE B cambia la variabile.** Il mandato chiede l'istogramma contro `N`; la lettura dice che
la variabile giusta e' **`|Psi|^2` contro `eta`** (l'eta' del nodo). Se i piccoli sono i **giovani**,
il `1e-7` e' **maturazione**, non normalizzazione — transitoria, se non fosse che la mitosi la
rigenera. Faro' entrambe, dichiarando la stratificazione per `eta` come **quarta firma**, aggiunta.

**FASE B e C non fatte.** Nessun run lanciato per la FASE A: e' sola lettura del sorgente.

---

## 6-quinquies. `inerzia` e' un **TEMPO^2** (2026-09-15) — la lettura di Luca chiude il buco

Documento: **`doc/INERZIA_tempo_quadro.md`**. Relazione dovuta per **§5-ter**.

Avevo riportato un buco dimensionale: `correzione/inerzia` e' adimensionale, ma la riga 1918
richiede `1/T^2`. **La lettura di Luca lo chiude esattamente**, e discende dal principio fondativo
(§8: *"lo spinore E' il tempo proprio della massa"*): se `Psi` porta **tempo**, allora
`[inerzia] = [|Psi|^2] = T^2` e `[correzione/inerzia] = 1/T^2`. **La massa e' il modulo quadro di un
tempo proprio.** Non e' una toppa: chiude al primo colpo, senza coefficienti.

**QUALE tempo — e il codice lo decide.** NON l'orologio `dt_n = DT*r`, perche' `r` e' **derivato da
`Psi`** (`ritmo()`: `a = angle(psi) - angle(psi_prec)`): sarebbe **circolare**. Resta il tempo
**metrico**, l'unico definito indipendentemente da `Psi`.

**DA DOVE entrerebbe — un solo slot.** In `F = mat(w) @ (amp * e^{i phi})`: `w = exp(-d/lam)*ramp*ramp`
e' l'esponenziale di **rapporti**, `e^{i phi}` e' una fase. **L'unico slot e' `amp`** (riga 2176),
oggi la costante `1.0`.

**L'ESPONENTE, derivato.** Il solitone ha lunghezza d'onda ~`LAM` e le onde viaggiano a `cs`, quindi
il suo periodo proprio e' `T_j = LAM/cs_j` — grandezze **gia' nel sistema**. Se l'ampiezza di
emissione e' il tempo proprio dell'emettitore:

> **inerzia ∝ cs^(-2)   <=>   omega = coppia/inerzia ∝ cs^2**

**IL TEST DEL VERSO PASSA, e non per costruzione.** Nei pozzi `cs` e' piccolo -> inerzia grande ->
omega piccola -> **la materia densa ruota piu' lentamente**. E' il verso del redshift
gravitazionale, ed e' **lo STESSO esponente dello Step 2** gia' cablato e **sigillato 10/10**
(`omega_clk *= (cs/CS_M)^2`), che fu derivato **prima** e **indipendentemente** dall'orologio di
Compton. Due canali indipendenti — la **massa** e l'**orologio** — danno lo stesso `omega ∝ cs^2`.
**Non e' una coincidenza costruita: e' una consistenza trovata.**

**ESITO (b): IL FATTORE MANCA.** Ricerca esaustiva: **zero** occorrenze di `cs` in `calcola_psi`,
`_pesi`, `_lam_archi`, `lambda_nodi`, `_rho_sorgente`, `satura`. La dipendenza **implicita** via `d`
esiste (l'onda metrica muove `d`) ma **non puo' essere quella derivata, per costruzione**:
`exp(-d/lam)` e' adimensionale **qualunque cosa faccia `d`**. **Esito (c) escluso rigorosamente.**
**Non l'ho cablato:** sarebbe un pezzo, con flag e sigilli, e la decisione e' di Luca.

**DA SAPERE PRIMA DI DECIDERE:** a densita' attuali `cs ~ CS_M`, quindi il fattore varrebbe una
**costante** (`LAM/CS_M = 0.4`, inerzia x0.16). **NON risolverebbe il `1e-7`**, che resta **ETA'**.
Due cose separate, tenute separate.

**IL COSTO DELLA LETTURA, dichiarato.** Chiude il buco a 1918 ma **ne apre due** altrove: riga
**1847** somma `amp ~ T` a un **versore adimensionale**; `scuoti_vuoto` (riga **534**) somma `T` a
`phivel ~ 1/T`. E una che c'era gia' sotto **entrambe** le letture: `lambda_nodi` confronta `|psi|^2`
con un **conteggio per volume**. **Il modello non e' dimensionalmente chiuso in nessuna delle due
letture.** La lettura di Luca chiude quello che conta di piu' — il buco che produce i 112 giri — ma
non e' globalmente consistente com'e' il codice oggi.
**A favore**, pero': sotto la lettura `GAMMA ~ 1/T` **coerentemente in tutti e tre** i suoi usi
(`satura`, `cs`, `psi_spin`), coerente col fatto gia' registrato che sia **condiviso**.

**PISTA REGISTRATA, NON APERTA:** se il fattore c'e', **`cs` entra nello spin ATTRAVERSO LA MASSA**,
non attraverso l'orologio — e **nessuna delle sei misure lo esclude**, perche' tutte riguardavano lo
Step 2 (fase globale, Bloch invariante a 3.3e-16). Mai testato.

---

## 6-sexies. MATURAZIONE (2026-09-15) — **CONCLUSO: ESITO (C)**

Documento: **`doc/MATURAZIONE_aliasing.md`**. Predizione scritta **prima** e committata prima
(`doc/PREDIZIONE_maturazione.md`, commit `a8a0360`). **Run CONCLUSO, 2000 passi.**
Relazione dovuta per §5-ter.

> ### VERDETTO: **ESITO (C).** L'aliasing e' **STRUTTURALE, non transitorio.**
> La maturazione **funziona** (`ramp` lineare, `rho` da 1.76e-11 a 5.5e-4, pavimento rilasciato dal
> 100% al 7%) **ma non toglie l'aliasing: la frazione aliasata e' 100% a OGNI campione, l'ultimo
> compreso.**

**La domanda:** il `1e-7` dell'inerzia e' ETA'. Se lo e', l'aliasing (112 giri/passo) potrebbe
sparire **da solo** per maturazione, e non ci sarebbe niente da riparare. Va accertato **prima** di
cablare qualunque cura, perche' cablare su un sistema aliasato darebbe un risultato inattribuibile.

**Sigillo PASS** (20 campi + RNG, `0.000e+00`, N confrontabile) e **flag confermati IN-RUN**:
`GAMMA_TURBO = 1`, `STEP2_OROLOGIO = False`, fork+MEM attivi. Comportamento **naturale**, non forzato.

**PRIMA META' DELLA PREDIZIONE: CONFERMATA.** La predizione diceva che `theta` non sarebbe sceso
subito, perche' l'inerzia e' bloccata sul **pavimento `1e-6`**, e che la densita' mediana lo avrebbe
attraversato **"poco dopo il passo 150-300"**. Misurato: attraversamento al passo **~245-250**,
`rho` mediana da **1.5e-8** (passo 25) a **5.07e-6** (passo 425), e il pavimento passa dal vincolare
il **100%** dei nodi al **14.7%**.

**SECONDA META': NON CONFERMATA (ancora), ed e' il riscontro che conta.** `rho` e' cresciuta **4.5x
oltre il pavimento** e **`theta` NON e' sceso**: piatto a **~4.6e4** gradi/passo, con la frazione
aliasata ancora al **100%**. Se `theta` seguisse `1/inerzia`, sarebbe gia' a ~1.0e4.

**COSA HO SBAGLIATO NELLA PREDIZIONE, dichiarato.** La catena `omega ∝ ramp^-4` tratta `omega` come
se fosse **istantaneamente** uguale a `coppia/inerzia`. **Non lo e':** `omega_s` e' una **memoria**
con rilassamento (riga 1918) e tempo caratteristico **gia' misurato**, `tau/DT ≈ 250 passi`. Dal
ginocchio (250) a ora (425) e' passato **meno di un tempo di rilassamento**: siamo **dentro** il
transitorio. **Il dato non falsifica ancora la predizione, ma non la conferma, e la predizione era
incompleta.**

**LA PREVISIONE CORRETTA, scritta ORA prima di vederla:** se `theta` insegue `1/rho` con ritardo
`tau ≈ 250`, la discesa deve diventare visibile **dal passo ~500-600**. **Se al passo 800 `theta` e'
ancora a 4.6e4, la lettura `omega ∝ 1/inerzia` e' sbagliata, non solo ritardata** — esito **(C)**.

**UNA PROIEZIONE SCOMODA, detta ora e non fra due ore:** con `theta ∝ n^-4`, la soglia di 30
gradi/passo sarebbe attraversata a **~2660 passi**, **oltre i 2000 del run**. E al passo 2000 `ramp`
mediano sara' **~0.31**: **nessuna popolazione matura (`ramp > 0.9`)**, quindi la **seconda misura**
prevista dal mandato (`chi` nella zona matura) **non sara' eseguibile su questo run**.
Due strade, **decisione di Luca**: prolungare a ~3000 passi (altre ~2-3 h), oppure fermarsi a 2000 e
riportare la **pendenza** di `theta(n)`, dichiarando l'attraversamento come **estrapolazione**.

**AGGIORNAMENTO AL PASSO 1200 — IL CRITERIO E' SCATTATO.** Avevo scritto prima di vederlo: *"se al
passo 800 theta e' ancora a 4.6e4, la lettura omega ∝ 1/inerzia e' SBAGLIATA, non solo ritardata"*.
**E' cosi'.** Regressione su 14 campioni, solo dopo il rilascio del pavimento (passi 425-1200):

```
d(log theta)/d(log n)    = -0.020      attesa dalla lettura: -4
d(log theta)/d(log rho)  = -0.006      attesa dalla lettura: -1
leva:  n x2.82   rho x16.9   theta x0.977
```

> **Con `rho` cresciuta quasi 17 volte, `theta` e' variato del -2%. Non e' un ritardo: e' ASSENZA DI
> DIPENDENZA. VERDETTO INDICATO: ESITO (C), l'aliasing e' STRUTTURALE, non transitorio.**
> E lo si sa **al passo 1200, non a 20.000** — che era lo scopo di misurare la pendenza.

**Meccanismo candidato (IPOTESI, non ancora misurata):** riga 1913,
`_tau = TAU_A * max(dens/dens_rif, 0.05)`. Prima della maturazione quasi tutti i nodi sono sotto
`1e-6`, scatta il **pavimento 0.05** e `tau/DT = 250`. Dopo, per il nodo mediano `dens/dens_rif ≈ 1`
e `tau = TAU_A`, cioe' **`tau/DT = 5000`**. **La memoria si e' allungata di ~20x esattamente mentre
il sistema maturava.** Con `omega_eq = |F|·sqrt(dt·tau/2)`, se `|F| ∝ 1/rho` **e** `tau ∝ rho`,
allora `omega_eq ∝ rho^(-1/2)` e anche quella discesa arriverebbe su 5000 passi. Da verificare
aggiungendo la colonna `tau` alla sonda, senza toccare la fisica.

**I NUMERI FINALI.** `theta` **non e' piatto** — ha un picco a 4.978e4 (passo 600) e cala a
**3.243e4** (passo 2000), **-35%**. Ma la domanda era *"cala COME PREVISTO?"*, e la risposta e' no,
di due ordini:

| finestra | leva su `rho` | `d(log theta)/d(log rho)` | atteso |
|---|---|---|---|
| tutto post-pavimento (22 campioni) | **x309** | **-0.061** | -1 (o -0.5 raffinata) |
| ultima parte (1300-2000) | x8.7 | -0.131 | idem |

Dal picco di `theta` alla fine, con `rho` cresciuta **x43.3**: se seguisse `1/rho` sarebbe **1149**;
se `rho^(-1/2)` sarebbe **7564**; **misurato 3.243e4** — **28x e 4.3x sopra**. La pendenza `-0.061`
con leva `x309` cade nella banda `-0.2..+0.2`: **il criterio temporale posto da Luca e' soddisfatto,
la lettura e' SBAGLIATA, non ritardata.**

**Il limite dichiarato in anticipo si e' avverato:** `ramp` mediano finale **0.2585** (proiezione
fatta al passo 425: ~0.31). **Nessuna popolazione matura**, quindi la seconda misura (`chi` nella
zona matura) **non era eseguibile** — come avevo detto prima, non dopo.

**E UN INDIZIO TRASVERSALE CHE PUNTA DALLA PARTE SBAGLIATA.** Alla stessa istantanea, negli ultimi
campioni: nodi **giovani** (`ramp<0.1`) `theta = 3.485e4`; nodi **maturi** (`ramp>0.5`)
`theta = 4.088e4`. **I maturi ruotano PIU' VELOCEMENTE.** Se `omega = coppia/inerzia` e l'inerzia
cresce con la maturita', dovrebbe essere il contrario. **E' a un solo istante, quindi il ritardo non
puo' spiegarlo** — ma e' grezzo (due classi, campione piccolo sui maturi): lo riporto come
**indizio**, non come misura. Il test vero e' la regressione trasversale del
`doc/CRITERIO_omega_rho.md` §4.1, **in corso**.

**Costo misurato:** 425 passi in 9.0 min (~1.3 s/passo a N≈4100); stima **2-3 h** per i 2000.

---

## 6-septies. IL TEST TRASVERSALE (2026-09-15) — **la lettura `omega = coppia/inerzia` e' FALSIFICATA**

Documenti: **`doc/CRITERIO_omega_rho.md`** (criterio scritto PRIMA + esito) e
`doc/MATURAZIONE_aliasing.md`. Sonda **ri-sigillata PASS** prima dell'uso. **Nessun run in volo.**

**Perche' serviva un test senza tempo.** Luca ha rilevato che la mia ipotesi **rigenerava la propria
scusa**: ogni volta che l'effetto non si vedeva, il ritardo era cresciuto (pavimento -> `tau=250` ->
`tau=5000`). Con `tau` proporzionale a `rho` e `rho` crescente, **aspettare non converge mai**.
Il presidio, ora in `CLAUDE.md` §9: **quando la spiegazione e' temporale, il test che la decide non
deve contenere il tempo.**

**RISULTATO 1 — il meccanismo `tau` e' CONFERMATO PER MISURA**, non piu' ipotesi:

| passo | `tau/DT` | % col pavimento 0.05 attivo |
|---|---|---|
| 1-200 | **250** | 100% -> 69% |
| 400 | 2884 | 10.7% |
| **700** | **4425** | **8.9%** |

`tau/DT` da **250 a 4425** (**x17.7**), e tende a `TAU_A/DT = 5000` — l'ancoraggio del nodo mediano
che Luca aveva dedotto dalla riga 1913. **La memoria si allunga di quasi 18x mentre il sistema
matura.** Ma non salva la lettura, perche' il test qui sotto non contiene il tempo.

**RISULTATO 2 — il test trasversale: la lettura CADE.** 4374 nodi, **leva sull'inerzia x10 080**
(quattro decadi), a **un solo istante**:

```
correlazione r = -0.395
theta per decile di inerzia:  basso 6.663e4 -> medio 5.073e4 -> ALTO 3.464e4
PENDENZA  d(log theta)/d(log inerzia) = -0.106
```

| esponente | `theta` cadrebbe di |
|---|---|
| -1.000 (lettura originale) | **x10 080** |
| -0.500 (lettura raffinata) | **x100.4** |
| **-0.106 (misurato)** | x2.66 — osservato per decili **x1.92** |

> **VERDETTO: `omega = coppia/inerzia` come LEGGE DI SCALA e' FALSIFICATA.** L'esponente misurato e'
> **-0.106**, non -1 ne' -0.5, su quattro decadi e **senza scappatoia temporale**.

**CORREZIONE AL MIO STESSO CRITERIO, dichiarata.** La banda che avevo scritto (-0.2..+0.2) diceva
*"omega NON dipende da inerzia PER NESSUNA VIA"*. **Quella formulazione e' troppo forte e i dati la
smentiscono:** `r = -0.395` e l'andamento per decili e' **monotono**, `theta` cala di **x1.92**. Una
dipendenza **c'e'**. La formulazione corretta: **`omega` dipende da `inerzia` con esponente -0.106,
circa UN DECIMO di quello richiesto.** La conclusione non cambia, la motivazione si': non e'
"nessuna dipendenza", e' **una dipendenza dieci volte troppo debole** — e nessun ritardo, per quanto
lungo (ora sappiamo: 4425 passi), spiega un **esponente** sbagliato di un fattore 10.
Sto correggendo un mio criterio **dopo** aver visto i dati, ed e' la mossa che il presidio §9 vieta:
lo dichiaro. La differenza e' che **non sto salvando l'ipotesi, la seppellisco lo stesso** — la
correzione rende il verdetto **piu' preciso, non piu' clemente**.

**E RITIRO UN INDIZIO PRECEDENTE.** Avevo riportato che i nodi "maturi" ruotavano **piu'
velocemente** (segno opposto all'atteso). Il test per **decili di inerzia** lo **smentisce**:
l'andamento e' monotono **nel verso giusto**. "Maturo" e "inerzia alta" non sono la stessa
popolazione, e vale il test per decili, non il confronto a due classi. **Indizio ritirato.**

---

## 6-octies. TRACING di `omega` (2026-09-15) — **il controllo ha stanato un termine mancante, ed era MIO**

Documenti: `doc/PREDIZIONE_tracing_omega.md` (criterio, committato **prima**: `075a09f` + esito (IV)
in `457abe4`) e **`doc/TRACING_omega.md`**. **CONCLUSO: ESITO (I)**, col meccanismo identificato.

**Il riscontro.** `correzione` ha **DUE** termini (righe 1895-1901) e io ne avevo ricostruito **uno**:
```
correzione = cross(B, nb)
if CAMPO_SPINORIALE:  correzione += cross(_nb_grav(), nb)      <- ATTIVO nei run del fork
```
Il secondo e' il torque verso il Bloch del **campo emesso spinoriale**. La mia catena lo ignorava.

**Come e' stato stanato: dal controllo, non dall'occhio.** Nel criterio (§IV.4, scritto **prima**)
avevo messo un controllo sulla **direzione** del residuo, perche' un `R_stoc` alto ha due cause:
rumore genuino **oppure un mio errore**. Regola: `cos(stoc, det)` ~ 0 = rumore isotropo; ~ ±1 =
**errore sistematico mio**, e allora **(IV) non si dichiara**.
**Misurato `cos = +0.643`**, oltre la soglia 0.5, e **stabile su tutti e otto i campioni**
(+0.348 … +0.643). Un residuo **allineato e persistente non e' rumore: e' formula che manca.**
E l'ampiezza torna: con `R_stoc ~ 2.8` e `cos ~ 0.64`, il deterministico vero e' ~`1+R·cos` = **2.8x**
quello ricostruito — **mancava un termine dello stesso ordine del primo**.

> **Senza quel controllo avrei dichiarato l'ESITO (IV)** — *"e' il rumore che guida omega"* — con
> `R_stoc` fra 13 e 2.8 a sostenerlo. **Sarebbe stato un falso positivo:** avrei attribuito al
> rumore un effetto che e' **una riga di codice**.

**Tre esiti che il termine mancante NON cambia** (perche' non dipendono da esso):
1. **Il dissipativo NON domina:** rapporto coppia/dissipazione = **73.88**. L'ipotesi *"omega e'
   governato dal rilassamento"* e' **esclusa**, non rinviata.
2. **L'angolo (B,nb) e' PIATTO:** pendenza **-0.006** (`r = -0.025`), mediana **59.4 gradi**.
   Nessun allineamento crescente con la densita' -> **(II-b) escluso**, e in modo robusto, perche'
   `B` e' ricostruito **esatto** (il codice lo costruisce da `_nb_prec`, non dal `nb` rumoroso).
3. **`|B|` DECRESCE** con l'inerzia (**-0.534**), non cresce -> **(II-a) escluso**.

E una conferma incrociata: il `theta` misurato qui, **-0.113**, coincide col **-0.106** del test
trasversale di ieri, misurato in modo indipendente. **Le due misure si confermano a vicenda.**

**Cosa NON dichiaro.** Il run incompleto stampava **(I)**, colpevole a valle. **Non lo dichiaro:**
era calcolato con `coppia/inerzia` dimezzata. Il run corretto e' in volo, tracer **ri-sigillato PASS**
dopo la modifica e **prima** dell'uso. Il run incompleto e' conservato come evidenza in
`csv/_test_fork/_tracing_omega_INCOMPLETO.txt`.

**IL RUN CORRETTO — ESITO (I), E IL COLPEVOLE HA UN NOME.**

Con il secondo termine al suo posto, la ricostruzione spiega il **96%** dell'incremento:
`R_stoc = 0.041`, **sotto** l'errore che la mia stessa approssimazione prevedeva (**0.097**).
**(IV) ESCLUSO** — e questo **valida a posteriori** la diagnosi: l'`R_stoc ~ 2.8` di prima **era** il
termine mancante, non il rumore.

| pendenza su `log inerzia` (passo 400, 2781 nodi) | valore | r |
|---|---|---|
| `coppia` (completa) | **-0.056** | -0.260 |
| **`coppia/inerzia`** | **-1.056** | **-0.981** |
| **`theta`** | **-0.113** | -0.353 |

La coppia e' **piatta**: tutto il `-1` viene dalla divisione per l'inerzia, ed esce **-1.056 con
r = -0.981**, praticamente esatto. **La formula d'ingresso e' giusta; l'esponente si perde DOPO.**

**DOVE si perde: nel rilassamento, attraverso `sqrt(tau)`.** `omega` e' un random walk smorzato, il
cui equilibrio e' `|omega|_eq = sigma * sqrt(tau/(2 dt))`. Le due pendenze, **misurate**:

```
sigma = |coppia|/inerzia   pendenza  -1.056     (2781 nodi, r = -0.981)
tau                        pendenza  +1.812     (20 nodi; via indiretta: +1.867)
attesa per |omega|:  -1.056 + 1.812/2 = -0.150
theta MISURATO                        = -0.113        scarto 0.037
```

> **Il `-1` della coppia e' cancellato dal `+0.91` di `sqrt(tau)`.** `tau = TAU_A*max(dens/dens_rif,
> 0.05)` cresce con la densita', e il suo peso entra nel plateau come **radice**. Coppia e memoria si
> annullano a vicenda e resta `-0.11`.
> **NON C'E' NESSUN BUG:** non c'e' una riga che fa qualcosa di diverso da quel che si crede. C'e' un
> **rilassamento la cui costante di tempo dipende dalla stessa grandezza** che sta al denominatore
> della coppia. **E' il sistema che si cancella da se'.**

**UNA COLONNA DA BUTTARE, dichiarata.** Nel run corretto la colonna `angolo` e' **invalida**: la
calcolo come `arcsin(|correzione|/|B|)`, che e' un seno **solo** se `correzione = cross(B,nb)`; col
secondo termine satura e stampa 90.00 per tutti. **Va ignorata.** L'esclusione di **(II-b) regge
lo stesso** e viene dal run *incompleto*, dove l'angolo era esattamente quello fra `B` e `nb`:
**-0.006, r = -0.025, mediana 59.4 gradi**. I dati "difettosi" misuravano bene proprio cio' che al
run corretto sfugge.

**Verdetto contro il criterio scritto prima:** **(I) confermato**; (II-a) escluso (`|B|` **decresce**,
-0.534); (II-b) escluso (angolo piatto); (III) non si applica; (IV) escluso (`R_stoc` 0.041).

**L'errore era nella MIA ricostruzione, non nel simulatore:** `soliton_simulator.py` non e' stato
toccato, blob `f5887254`.

---

## 6-novies. `tau` deve essere il TEMPO-LUCE `d/cs`? (2026-09-15) — **criterio scritto, misura IN VOLO**

Documento: **`doc/TAU_tempo_luce.md`**. Contiene **solo il criterio e il setup**, committati
**prima** dei dati. **I numeri non ci sono ancora.**

**La domanda nasce dal verdetto del tracing:** il `-1` della coppia e' cancellato dal `+0.91` di
`sqrt(tau)`. L'aliasing viene dall'**interazione di DUE leggi**: `omega = coppia/inerzia`
(riga 1918) e `tau = TAU_A*max(dens/dens_rif, 0.05)` (riga 1913).

**Le due righe non sono pari, e la seconda ha gia' due fatti MISURATI contro:**
1. **non fa quello che dichiara**: e' scritta come `tau ∝ dens` ma misurata da' **`rho^1.81`**
   (via indiretta `+1.867`: due strade indipendenti, stesso scarto dall'unita');
2. **il perche' e' strutturale**: `dens_rif` e' la **MEDIANA**, quindi per il nodo mediano
   `dens/dens_rif ~ 1` **sempre** — `tau` del nodo tipico e' **ancorato a `TAU_A` per costruzione**
   (rilievo di Luca, gia' in `CLAUDE.md` §9). **Punto fisso auto-normalizzante, non transitorio.**
Una riga che non fa quello che dichiara e' la categoria che questo repo ha gia' pagato **tre volte**.

**L'incoerenza da sanare:** se `inerzia = T² = (d/cs)²`, allora **il tempo che COSTRUISCE l'inerzia
e quello che la RILASSA devono essere lo stesso**. Oggi sono **due diversi nella stessa equazione**.
Il candidato `tau = d/cs` e' **imposto** (causalita': non si puo' ricordare piu' a lungo di quanto si
impieghi a sapere di se'), **gia' cablato** (e' il `tau` dello Strato 1, messo li' per la stessa
ragione) e a **zero manopole**.

**Nota di metodo:** il tracer misura `tau_luce` con la **STESSA formula gia' nel file**
(`_bloch_ritardato`: `d_nodo` = media degli archi incidenti con fallback `LAM`, `cs_nodo` dalla cache
`_cs_nodo_prev`), non con una nuova. Misurare la proposta con una formula diversa da quella cablata
sarebbe stato incoerente col suo stesso argomento.

**IL CRITERIO, fissato prima:** `pendenza(theta) = -1.056 + pendenza(d/cs)/2`.
`|pendenza(d/cs)| <= 0.3` -> `theta` torna a **~ -1.0**, la cancellazione si rompe;
`pendenza(d/cs) ~ +1.8` -> **non cambia nulla**, la sostituzione resta piu' coerente ma **non
risolve**, e va detto cosi'.

**IL CAVEAT DI AMPIEZZA, da dire comunque:** `tau` passa da ~44 unita' di tempo a ~0.25, e poiche'
`|omega|_eq ∝ sqrt(tau)` il fattore e' **~1/13**: da **112 giri/passo a ~9**.
**Un ordine di grandezza nella direzione giusta, NON la soluzione dell'aliasing.**

**ESITO DELLA FASE 1 — e prima una CORREZIONE A ME STESSO.**

La formula del criterio (`pendenza(theta) = sigma + tau/2`) **va verificata sul caso attuale prima di
usarla per estrapolare**, e **non regge**:

| | `sigma` | `tau` | attesa | misurata | scarto |
|---|---|---|---|---|---|
| run 400 passi, `tau` su **20 nodi** | -1.056 | **+1.812** | -0.150 | -0.113 | **0.037** |
| run 300 passi, `tau` su **2195 nodi** | -1.078 | **+1.176** | -0.490 | -0.152 | **0.338** |

> **Correzione a `doc/TRACING_omega.md` §6.3 e al commit `9713ddb`:** lì avevo scritto che la catena
> «si chiude» con scarto **0.037**. Quel numero usava `pendenza(tau)` su **20 nodi**. Su **2195**
> (`r = +0.796`) lo scarto è **0.338**: **la catena NON si chiude.** Il meccanismo qualitativo regge
> (√`tau` cancella **parte** del −1) ma il conto quantitativo no, e **resta un residuo di ~0.34
> nell'esponente che non so spiegare.**

**LA MISURA CHE IL CRITERIO CHIEDEVA:**
```
pendenza tau_ATTUALE  = +1.176   (r = +0.796, 2195 nodi)
pendenza tau_LUCE     = +0.097   (r = +0.351, 2195 nodi)     <- PIATTO
sigma = coppia/inerzia = -1.078
```
**`d/cs` è piatto (+0.097)**: prima banda del criterio, fissata prima di misurare. Un `tau` piatto
**non può cancellare niente**.

| stima per `theta` con `tau_luce` | |
|---|---|
| naive (solo formula) | **-1.030** |
| **corretta, se il residuo 0.338 resta** | **-0.692** |
| oggi, misurato | **-0.152** |

> **La stima onesta è −0.69, non −1.03.** Ma in entrambe: **la cancellazione SI ROMPE**, un fattore
> **4.5-7** sull'esponente.

**L'AMPIEZZA, coi numeri misurati:** `tau/DT` da **6500** a **66.5** passi (rapporto 0.0102);
`|omega|_eq ∝ √tau` → fattore **0.101** → `theta` da **126.7 a 12.8 GIRI per passo**.
**Un ordine di grandezza nella direzione giusta, e il settore resta ALIASATO. Non è una cura.**

**Restano aperti:** il **residuo di 0.338** (da stanare prima di fidarsi di qualunque predizione
quantitativa su questa catena) e l'**aliasing** (13 giri/passo).

**Cosa NON tocca:** la riga 1918, `inerzia`, e la **forma** del termine dissipativo — in particolare
**non** apre la questione se `-omega/tau` debba essere un allineamento LLG `-lambda n x (n x B)`:
e' **separata e aperta**, e mescolarla renderebbe inattribuibile qualunque risultato.

---

## 6-decies. BARRE D'ERRORE (2026-09-15) — **il residuo e' REALE ma TRANSITORIO. E ho corretto due volte, sbagliando la prima correzione.**

Documento: **`doc/BARRE_ERRORE_pendenze.md`**. **Nessun run**, solo statistica sui CSV su disco.

**1. La premessa da verificare non reggeva, ma la verifica era giusta da chiedere.**
L'ipotesi era: *"`r = 0.35` -> pendenza fragile, `SE ~ 0.3`"*. **`SE` non dipende quasi da `r`:
dipende da `sqrt(n)`.** Stessa pendenza, stesso `r`: `SE` = **0.108** con 20 punti, **0.0097** con
2195. `r^2` basso dice che la relazione **spiega poca varianza**, non che la pendenza sia incerta.

| grandezza | pendenza | SE | r^2 | IC 95% |
|---|---|---|---|---|
| `sigma` | -1.0780 | 0.0073 | 0.908 | [-1.0923, -1.0637] |
| `tau` attuale | +1.1760 | 0.0191 | 0.634 | [+1.1386, +1.2134] |
| `tau` luce (`d/cs`) | +0.0970 | 0.0055 | 0.123 | [+0.0862, +0.1078] |
| `theta` | -0.1520 | 0.0097 | 0.100 | [-0.1711, -0.1329] |

**2. Propagazione: `z = 21.8`.** Lo scarto al passo 300 **non e' rumore**. Si passa al secondo check.

**3. Il secondo check: e' TRANSITORIO, e si chiude.** Lo scarto cala di **due ordini**:

```
passo   50  100  150  200  250  300  350  400
scarto 0.979 0.660 0.448 0.427 0.194 0.337 0.230 0.010
pendenza su log(passo): -0.412
```

> **Al passo 400 la catena CHIUDE (scarto 0.010).** `tau ~ 4425-6500 passi` contro un run di 400: il
> sistema ha vissuto **meno di un decimo** di un rilassamento, e la formula vale **all'equilibrio**.
> **VERDETTO: TRANSITORIO, NON UN TERMINE MANCANTE. La ricerca non e' giustificata.**

**4. E la mia correzione di stamattina aveva la CAUSA SBAGLIATA.** Avevo attribuito la differenza
`0.037` vs `0.338` al campione (20 contro 2195 nodi), e l'avevo messo in `CLAUDE.md` §9 come fatto.
**A parita' di passo le due strade CONCORDANO:** passo 300 -> +1.176 contro +1.178 (scarto **0.002**);
passo 400 -> +1.812 contro +1.867 (scarto **0.055**). **La differenza e' il PASSO, non il campione.**

> **Quindi il numero ORIGINALE — "la catena si chiude, scarto 0.037" — era GIUSTO**, e col conto
> rifatto lo e' ancora di piu' (0.010). **Ho corretto una cosa giusta con una spiegazione sbagliata,
> e me ne sono accorto solo facendo il check che Luca ha chiesto.**

**Cosa resta e cosa no:** resta il presidio *"una pendenza si riporta col suo `SE`"* — ed e' proprio
applicandolo che si e' visto che `SE = 0.0097`. **Non resta** *"una pendenza su 20 nodi non e' una
pendenza"* **come spiegazione di questo caso**: qui i 20 nodi davano il numero giusto. Corretto in
`CLAUDE.md` §9, in `doc/TRACING_omega.md` e in `doc/TAU_tempo_luce.md`, **in loco**, lasciando le
righe originali visibili.

---

## 6-undecies. FASE 2 `--tau-luce` (2026-09-15) — **SIGILLO FALLITO. Ci si ferma.**

Documento: **`doc/SIGILLO_tau_luce_FALLITO.md`**. Blob `f5887254` -> **`7d484580`**.
**Gate NON ri-timbrato.** Flag **OFF di default**, e **T1 dimostra la byte-identita'**: il
comportamento di default del repo e' **invariato**.

```
T1=PASS   T2=FAIL   T3=FAIL   T4=FAIL   T5=PASS      ->   SIGILLO COMPLESSIVO: FAIL
```

**T1 PASS**, ed e' quello che copre di piu': confronto contro il file **prima** della modifica, 21
campi + RNG a `0.000e+00` con N confrontabile. Certifica insieme il flag OFF **e** che l'estrazione
di `_tempo_luce_nodo` da `_bloch_ritardato` non ha cambiato una virgola.

**T2 FAIL — ma e' un difetto del TEST.** Il monkeypatch agisce sul metodo **condiviso**, quindi
cambia **anche la ritardazione dello Strato 1** (`--fork-su2-mem` e' attivo): due meccanismi insieme,
traiettoria diversa, `N` 1718 contro 1647. E' il rovescio della scelta - giusta - di avere **una
sola** formula: un test naive che la sostituisce colpisce entrambi gli utilizzatori. Il presidio ha
funzionato: la riga dei conteggi per prima ha impedito di leggere uno zero come identita'.

**T3 FAIL — l'effetto e' REALE ma la META' di quello predetto.**

| | pendenza | SE | r^2 | n |
|---|---|---|---|---|
| OFF | -0.1685 | 0.0090 | 0.126 | 2417 |
| **ON** | **-0.4265** | **0.0091** | 0.464 | 2534 |

Spostamento **0.258**, cioe' **~28 sigma**: indiscutibile. **Ma l'attesa era -1.03** (naive) **o
-0.69** (stima onesta): misurata **-0.43**. Il criterio chiedeva almeno 0.3: **non ci arriva**.
**Non ho una spiegazione della meta' mancante e non ne invento una.**

**T4 FAIL a meta', ED E' UN REPERTO CHE TOCCA ANCHE LO STRATO 1.**
`d -> 2d` da' **2.000000 esatto**: sulla geometria e' una legge. `cs -> 2cs` da' **1.000000**: non
segue. La causa **non e' il cablaggio nuovo**: `_cs_nodo_prev` e' scritta in `step()` con l'`n` di
quel momento, poi `mitosi()` fa crescere `n`, e al passo dopo `len(csp) >= n` e' **falso** -> la
guardia ricade su `cs_nodo = CS_M`. **Misurato: cache usabile in 6 passi su 30 = 20%.**

> **Nell'80% dei passi il `cs` locale non viene usato affatto** — e vale **anche per lo STRATO 1**,
> sigillato 23/23, che usa la stessa funzione: il suo `tau = d/cs` e' in realta' **`d/CS_M`** quasi
> sempre. Il ritardo esiste, ma **la parte che porta la curvatura e' inerte.**
> **Ereditato, non introdotto oggi, e non era stato notato.**

**T5 PASS** sulla stabilita' (`|nb|-1 = 2.2e-16`, zero NaN) ma con un numero da leggere: `theta` da
**129.5 a 43.6 GIRI per passo**, fattore **0.336** contro lo 0.077 atteso. **L'ampiezza cala di 3x,
non di 13x, e 43.6 giri/passo restano un settore massicciamente aliasato. Non e' una cura, e ora
c'e' il numero misurato a dirlo.**

**Tre cose da fare, NESSUNA "al volo" in questo commit** (§2): riscrivere T2; decidere sul reperto
`_cs_nodo_prev` (**questione a se'**, tocca un meccanismo gia' sigillato); capire la meta' mancante
di T3 **con un criterio scritto prima**.

---

## 6-duodecies. LA CACHE `_cs_nodo_prev` (2026-09-15) — **difetto REALE, curato, sigillo 5/5. Ma NON spiega la meta' mancante di T3, e lo dico PRIMA di ri-misurare**

**IL DIFETTO.** `_cs_nodo_prev` e' scritta a **fine passo** con l'`n` di quel passo (riga ~2918). La
**mitosi aggiunge nodi**, quindi al passo dopo la guardia `len(csp) >= n` di `_tempo_luce_nodo`
fallisce e si cade nel ramo `else` -> **`cs_nodo = CS_M` costante**.

**Misurato sul file PRIMA della patch** (seme 1, scena 3 masse, 30 passi):

| | |
|---|---|
| passi con cache **inusabile** | **24 su 30** |
| chiamate finite nel **fallback** | **23 su 32 = 71.88 %** |

**Ne risentivano DUE chiamanti**, non uno: `_bloch_ritardato` (riga 2462, **lo STRATO 1, gia'
sigillato 23/23**) e il rilassamento sotto `--tau-luce` (riga 1947).

**PERCHE' NESSUN SIGILLO L'AVEVA VISTO.** Il ramo `else` **non e' un errore**: e' il fallback
legittimo per `--cs-dinamico` OFF e per il primo passo. Il codice fa quello che dice. E' la
**condizione** a essere sbagliata in presenza di mitosi. Niente NaN, niente runaway, nessuna
byte-identita' violata. **Un difetto silenzioso non si trova guardando se il codice sbaglia: si
trova contando quale strada prende.** Da qui il presidio nuovo in `CLAUDE.md` par.9:

> **Ogni ramo `else` / fallback / `getattr(..., default)` su un percorso FISICO va strumentato con un
> contatore.** Un fallback che scatta il 72 % delle volte **non e' un fallback: e' il comportamento
> principale.** E' il gemello del presidio del *valore sotto ipotesi nulla*.

**LA CURA.** Il figlio **eredita `cs` dal padre** in `_eredita_spinore_figli`: **sesta voce della
stessa convenzione** gia' usata per `_nb`, `_nb_prec`, `_nb_ret`, `omega_s`, `_psi_spinor`,
`_psi_prec`. Zero parametri, zero floor, zero valori nuovi. **Non toccati** la guardia, il ramo
`else`, la scrittura a fine passo.

**SIGILLO `csv/_seal_fork/_sigillo_fix_cache.py` — 5/5 PASS**

| | esito | numeri |
|---|---|---|
| **P1** flag OFF byte-identico | PASS | `n_A = n_B = 1692` (**confrontabili**), 21 campi, `max\|A-B\| = 0.000e+00`, RNG identico |
| **P1b** col flag ON devono DIFFERIRE | PASS | `n` 1821 contro 1771 |
| **P2** il contatore | PASS | **71.88 % -> 0.00 %** |
| **P3** `len(cache) == n` a ogni passo | PASS | **24/30 -> 0/30** |
| **P4** stabilita' | PASS | `\|nb\|-1 = 2.2e-16`, NaN/inf **0** |

**P1b non era nel mandato: l'ho aggiunto.** Senza, una patch che non fa **nulla** passerebbe P1, P3 e
P4. Il controllo necessario e' che il risultato **fisico** cambi.

### E QUI LA COSA CHE CONTA PER TE — **una premessa del mandato non regge**

P4 misura anche la dispersione di `cs` **riparato**:

```
cs cache: min 1.99954   max 2.0   (CS_M = 2)      max/min = 1.000230
```

> **`cs` varia dello 0.023 %.**

Il mandato argomentava: *«l'effetto di `tau = d/cs` puo' esistere solo quando `cs` varia, cioe' in un
quinto dei passi; con la cache attiva 1/5 del tempo, un effetto dimezzato e' quello che deve
succedere»* — e ne concludeva che la meta' mancante di T3 (misurato **-0.43** contro **-0.69**
onesto / **-1.03** naive) era **questo bug**.

**Non segue.** Il fallback **non disattivava** `tau = d/cs`: lo calcolava come **`tau = d/CS_M`**, e
**il fattore `d` era vivo nel 100 % dei passi.** Cio' che la FASE 2 sostituisce e'
`TAU_A*max(dens/dens_rif, 0.05)` con `d/cs`, e **quasi tutto quel cambiamento sta in `d`**, non in
`cs`. Il difetto congelava **solo** il fattore `cs` — che ha **2.3e-4** di escursione totale.
Attribuirgli uno spostamento di pendenza di ordine **0.3** significa chiedere a una grandezza che
varia di 2e-4 di produrre un effetto tre ordini di grandezza piu' grande.

**PREDIZIONE, scritta e committata PRIMA della ri-misura** (`doc/FIX_cache_cs.md` par.5, commit
`43e9a47`): la pendenza T3 col flag ON **non si muovera' in modo misurabile**, `|Delta|` sotto il
proprio `SE` (~0.01). Se e' cosi', vale la lettura gia' fissata dal mandato stesso: **«il bug non era
la causa: resta un residuo vero da capire. Non inventare una spiegazione: riporta e fermati.»**

**LA CURA RESTA GIUSTA COMUNQUE**, per una ragione indipendente dal residuo: `cs` e' quasi-costante
**oggi**, alle densita' attuali (`CLAUDE.md` par.6, *«a densita' reali cs e' MORTO»*). Il giorno in cui
`cs` sara' vivo, una cache scartata a ogni mitosi sarebbe un difetto **grande** — e lo sarebbe **in
silenzio**. Si ripara adesso, mentre e' innocuo e dimostrabile.

**COSA RESTA SCOPERTO.** Le vie di crescita dei nodi sono **tre**: mitosi (`:3192`), Schwinger
(`:3309`) e **`semina()` (`:1600`)**. La terza **non** passa da `_eredita_spinore_figli`. In batch e'
inerte (`semina_cont=False` di default, si accende **solo** dalla GUI), quindi **non tocca nessuna
misura committata** — ma e' sul percorso GUI, lo stesso della voce **H** di `doc/RAMIFICAZIONI.md`,
e li' e' registrata.

### ESITO DELLA RI-MISURA — **la mia predizione e' SMENTITA, e la scrivo per prima**

Quattro bracci, 300 passi, seme 1 (`csv/_test_fork/_rimisura_t3.txt`; codice committato **prima** del
run, `22a7c41`).

| braccio | pendenza | SE | r^2 | n | theta mediana |
|---|---|---|---|---|---|
| PRE  OFF | -0.1685 | 0.0090 | 0.126 | 2417 | 129.51 giri/passo |
| **PRE  ON** | **-0.4265** | 0.0091 | 0.464 | 2534 | 43.55 giri/passo |
| POST OFF | -0.1491 | 0.0085 | 0.109 | 2517 | 131.27 giri/passo |
| **POST ON** | **-0.4710** | 0.0107 | 0.417 | 2690 | 42.81 giri/passo |

> **`Delta` = -0.0445 +- 0.0141, `z` = 3.16.** Avevo predetto `|Delta|` **sotto il proprio SE**.
> **Ho predetto zero e ho misurato 3 sigma.**

**Le DUE previsioni opposte erano entrambe sbagliate.** Il mandato diceva **~50 %** (*«un effetto
dimezzato e' quello che deve succedere»*); io dicevo **zero**. **Misurato: 16.9 %** del divario verso
l'attesa onesta `-0.69`. **Restano aperti `-0.219`, e `theta` resta a 42.8 giri/passo: la FASE 2 non
si chiude.** E' il caso *«valori intermedi»* previsto dal mandato: si riporta il numero e la
frazione, **senza forzare**.

*(Controllo di validita' superato: `PRE ON = -0.4265` riproduce il `-0.43` gia' in
`doc/SIGILLO_tau_luce_FALLITO.md`. Stessa scena, confronto col numero storico valido.)*

**IL MIO ERRORE, perche' e' il tipo che si ripete.** Avevo argomentato: *«`cs` varia dello 0.023 %,
quindi non puo' spostare la pendenza»*. **Ho confrontato l'AMPIEZZA di una variazione con l'ampiezza
di una pendenza.** Una pendenza trasversale non misura **quanto** una grandezza varia, misura
**quanto la sua variazione e' CORRELATA con l'ascissa**: un fattore che cambia dello 0.02 % ma
**sistematicamente nella stessa direzione** lungo l'asse dell'inerzia **sposta la pendenza**; uno che
cambia del 50 % a caso non la sposta. **Argomento di ampiezza su una domanda di correlazione.**
Resta vero il resto — `d` era vivo nel 100 % dei passi, e i **6/7** di divario ancora aperto lo
confermano — ma *«non puo' muoverla affatto»* era falso.

### ⚠ E UN DUBBIO SUL METRO, che ti segnalo perche' vale CONTRO di me

`z = 3.16` usa le `SE` **interne a un singolo run**. Ma i due bracci ON sono **due traiettorie di un
sistema caotico** (`N` 3999 contro 4100): **il valore sotto ipotesi nulla non e' zero**, e' la
dispersione della pendenza fra run che differiscono per una perturbazione irrilevante — **mai
misurata su questa osservabile**. Per `CLAUDE.md` par.2.7 (*mai su un solo seme*) va **misurata**:
**controllo in volo**, tre semi x due bracci, `csv/_test_fork/_controllo_semi.py`, con la lettura
scritta **dentro lo script prima dei dati**. Se il segno non e' concorde sui tre semi, **il
`16.9 %` non e' un numero riportabile** e vanno corretti tutti i documenti che l'hanno gia' scritto,
questo compreso.

---

## 6-terdecies. IL CONTROLLO SUI SEMI (2026-09-15) — **ritiro il "16.9 %". Era dispersione di run.**

`csv/_test_fork/_controllo_semi.py`, 3 semi x 2 bracci, 300 passi.

| seme | ON **pre** | ON **post** | `Delta` |
|---|---|---|---|
| 1 | -0.4265 ± 0.0091 | -0.4710 ± 0.0107 | **-0.0445** |
| 2 | -0.4846 ± 0.0099 | -0.4479 ± 0.0082 | **+0.0367** ← **segno opposto** |
| 3 | -0.4412 ± 0.0080 | -0.5047 ± 0.0116 | **-0.0635** |

> `media = -0.0238`, `SE della media = 0.0307`, **`t = -0.77`**.
> **`IC95 = [-0.156, +0.108]`**: contiene lo **zero** *e* il **-0.120** dell'ipotesi «~metà».
> **Tre semi non decidono. Nessuna delle due ipotesi è esclusa.**

**IL NULLO CHE NESSUNO AVEVA MISURATO**, ed è la parte che vale per tutto il programma:

| | |
|---|---|
| `SE` **interna** a un singolo run | **~0.010** |
| dispersione **FRA SEMI, a codice INVARIATO** | **0.0302** / **0.0286** |

> **La barra giusta è TRE VOLTE quella usata.** Su questo sistema caotico la pendenza trasversale
> cambia da run a run di **0.03 senza che il codice cambi**. **Tutte** le pendenze committate in
> questo programma portano la barra piccola: le conclusioni sembrano reggere perché gli effetti sono
> grandi (il **-1.056** del tracing, il **+0.097** di `d/cs` contro `-1`, il contrasto ON-OFF
> **-0.32** = 11 volte la dispersione) **ma vanno ricontrollate una per una contro 0.03.**

**REGGE:** la **FASE 2 non si chiude** — ON post medio **-0.4745** contro l'attesa `-0.69`, divario
**-0.2155**, `SE` della media **0.0165** → **`z = 13.1`**; `theta` **30.7-44.9 giri/passo** su sei run.

---

## 6-quaterdecies. **`_psi_spin_prec`: la FASE 5 non è MAI entrata in funzione** — e questo tocca tutto ciò che è stato misurato

Cercando altri casi del pattern *«snapshot cross-passo non esteso alla mitosi»* ne è emerso un
**settimo**, e in un punto che non è diagnostico.

**FASE A** (`doc/REPERTO_psi_spin_prec.md`, 150 passi): la guardia di `ritmo()` è un'uguaglianza
**ESATTA**, quindi **un solo nodo di mitosi** la fa scartare.

| esito di `ritmo()` | | |
|---|---|---|
| guardia 4π **FALLISCE** → ricade sul **ritmo scalare a 2π** | **143/150** | **95.33 %** |
| guardia 4π passa | 6/150 | 4.00 % |
| `return` anticipato su `_psi_prec` (`r = 1`) | 1/150 | 0.67 % |

**La condizione che fallisce è una sola, in 143 casi su 143: `len(_psi_spin_prec) != n`.**
`psi_spin`, che `calcola_psi` ricostruisce **dentro** il passo, era sempre lungo `n`. Il 4π girava
**solo ai passi 2 e 3**, prima della prima mitosi.

### ⚠ LA FORMULAZIONE CONTA, e quella corrente è sbagliata

Circola già la frase *«la fisica ha integrato con un tempo proprio stale»*. **Non è vero, e l'ho
verificato.** `signed` era **già calcolato** nella versione **scalare a 2π** poche righe sopra; la
guardia decide solo se **sovrascriverlo**. `r` era **ricalcolato a ogni passo ed era valido** — il
contatore registra `len(_psi_prec) == n` in **149 chiamate su 150**.

> **La frase vera:** la fisica ha integrato con **l'orologio SCALARE STORICO**, e la doppia copertura
> **non è mai entrata in funzione.** *"Integrate male"* implicherebbe **errore numerico**;
> *"orologio diverso da quello dichiarato"* implica **modello diverso** — **e solo la seconda è vera.**
> Le misure sono **valide per il sistema che è girato davvero**, e **non valide** come misure del
> sistema col settore 4π attivo.

**Marchio registrato** in `doc/RAMIFICAZIONI.md` (secondo marchio, in testa): *«misurate col ritmo
scalare a 2π; la doppia copertura non era attiva. Da riverificare col settore 4π in funzione»* —
**T3 e i suoi quattro bracci inclusi**, cioè il divario stesso che stiamo inseguendo.

### FASE B — curato, **sigillo 6/6 PASS**

Settima voce della stessa convenzione (`vstack`, perché `psi_spin` è `n × 2` **complesso**).
Blob **`b298677a` → `08784685`**.

| | | |
|---|---|---|
| **S1** OFF byte-identico | **PASS** | `n_A = n_B = 2501`, `max\|A-B\| = 0.000e+00`, RNG identico |
| **S1b** con ON devono differire | **PASS** | `n` 2392 contro 2200 |
| **S2** contatore | **PASS** | **88.33 % → 0.00 %** |
| **S3** `len == n` | **PASS** | **54/60 → 0/60** |
| **S5** stabilità | **PASS** | `\|nb\|-1 = 2.2e-16`, NaN/inf 0 |

### ⚠⚠ E S4 HA MISURATO LA COSA SBAGLIATA — lo dice il codice, non il numero

```
PRIMA   r: mediana 1.000000    DOPO   r: mediana 0.999999    z = 0.00
```

**Quel `z = 0.00` non significa «la cura non cambia `r`»: significa che la mediana di `r` NON PUÒ
cambiare.** In coda a `ritmo()`, `x = f / median(|f|)` e `r_normalized = r / r_unit` con `r_unit` il
valore a `x = 1`: il nodo mediano ha `x = 1` **per definizione**, la mappa è **monotona**, quindi
**`median(r) = 1.0` ESATTAMENTE, con qualunque orologio.**

> **È il SECONDO caso dello stesso trabocchetto strutturale.** Il primo è `_tau = TAU_A *
> max(_dens/_dens_rif, 0.05)` con `_dens_rif = median(_dens)`. **Una grandezza normalizzata sulla
> propria mediana ha un punto fisso, e su quel punto non si misura nulla.** Presidio in `CLAUDE.md` §9.

L'unico numero informativo è la **dispersione**: `0.4421 → 0.4257` (**−3.7 %**) — **un seme, nullo
non misurato**. Per il presidio del paragrafo precedente, **non basta**.

**Quindi l'attesa «`r` cambierà in modo significativo» non è confermata, e non è nemmeno smentita:
`S4`, com'è costruito, NON PUÒ rispondere.** E **non dico che questo chiuda T3**: non è stato
misurato, e un difetto grande non implica un effetto grande — la cache `cs` lo ha appena dimostrato.

---

## 6-quindecies. **L'ANELLO DI RETROAZIONE: e se il BERSAGLIO fosse mal calcolato?** (rilievo di Luca, 2026-09-15)

È l'osservazione più utile della giornata, e **non propone un colpevole nuovo.**

### Il rilievo

L'attesa contro cui misuriamo da due giorni nasce da:

```
pendenza(theta) = pendenza(sigma) + pendenza(tau)/2
                = -1.078          + 0.097/2          ~ -1.03   (naive)
                -> -0.69 con la correzione del transitorio
```

**e assume che `sigma = coppia/inerzia` resti `-1.078` anche col nuovo `tau`.** Ma c'è un **anello**:

```
  tau  ->  omega  ->  fasi (phi)  ->  psi  ->  inerzia = |psi|^2  ->  sigma = coppia/inerzia
   ^________________________________________________________________________|
```

Cambiando `tau` cambia `omega`; `omega` fa evolvere le fasi; le fasi costruiscono `psi`; **`psi` E'
l'inerzia**. Quindi **`sigma` non è una costante indipendente: è A VALLE di `tau`.** Usare il `sigma`
misurato nel braccio **vecchio** per predire il braccio **nuovo** presuppone che l'anello non ci sia.

| | |
|---|---|
| se `sigma` nel braccio ON **non è più** `-1.078` | l'attesa **non era** `-0.69` → il "divario" è in parte **un artefatto della predizione**, non un bug da cercare |
| se `sigma` è ancora `≈ -1.078` | l'anello è debole, **l'attesa regge e il divario è reale** |

**Ciò che la rende seria:** non dice *«c'è un altro bug»*, dice *«il bersaglio contro cui misuriamo
potrebbe essere mal calcolato»*. **È l'unica ipotesi sul tavolo che non richiede di trovare qualcosa
di rotto**, e per questo va provata **per prima** fra le spiegazioni del residuo.

### La mia correzione: **il numero NON è nei dati, e non costa zero**

Il rilievo dice *«è un numero solo, già nei dati dei quattro bracci: costa zero»*. **Verificato, ed è
falso.** `csv/_test_fork/_rimisura_t3.py` calcola **solo** la pendenza di `theta` contro l'inerzia:
**zero occorrenze** di `coppia` o `sigma` in tutto lo script, e le reti non sono persistite.
**`sigma` non è mai stato calcolato né salvato. Serve un run.**

*(Lo scrivo perché è la stessa regola del registro: **un numero entra solo se è già nel repo.**
Qui non c'è.)*

### E un secondo motivo per non rifarlo com'era

Quel `sigma` andrebbe misurato su un sistema che **è appena cambiato due volte** — e la seconda ha
**acceso la FASE 5**, che sta **a monte di tutto l'anello**: `dt_n = DT*r` è il tic con cui `omega`
si rilassa (§6-quaterdecies). Misurarlo sul sistema a 2π risponderebbe alla domanda di **ieri**.

### La proposta, con il presidio di Luca incorporato **per costruzione**

Un solo script, **3 semi × 2 bracci** (~50 min), che **nello stesso run** misura `sigma`, `tau`,
`theta`, e **ricalcola l'attesa `sigma + tau/2` col `sigma` misurato IN QUEL BRACCIO**.

Così il presidio — *«se `sigma` risultasse cambiato non basta dire «ecco perché»: va RICALCOLATA
l'attesa e verificato che il divario si chiuda QUANTITATIVAMENTE, con le barre d'errore»* — **è
soddisfatto per costruzione**, non a posteriori: l'attesa ricalcolata si confronta col misurato
**contro la barra giusta (0.03, non 0.01 — §6-terdecies)**. Se non si avvicina, **l'anello non era
la causa**, e lo dirà il numero.

**Criterio scritto prima, come sempre. Registrato come fronte R** in `doc/RAMIFICAZIONI.md`.
**Non lanciato**: aspetta il via libera.

---

## 6-sexdecies. **PRIMA MISURA DEL SETTORE SPINORIALE, braccio OFF: ESITO (A)** — e l'aliasing è il doppio di quanto avevo scritto

Predizione committata **prima** del run (`c547294`), soglie in **codice** committate prima di girare
(`c8cd9d1`). 2 semi, 500 passi, blob `08784685`, osservatore **sigillato 6/6 PASS**.

| | seme 1 | seme 2 |
|---|---|---|
| `chi` **materia** | 89.9682° · `SE 0.0854` → **`z = −0.37`** | 90.0639° · `SE 0.0857` → **`z = +0.75`** |
| `chi` **p90** | 90.0210° → `z = +0.14` | 90.1174° → `z = +0.70` |
| autocorrelazione, **10 bin** (0.57–15.0) | `max\|z\| = 1.80` | `max\|z\| = 1.09` |
| frazioni `<10°` / `>170°` | 0.00745 / 0.00744 | 0.00763 / 0.00773 |

Le frazioni ai poli **coincidono entro il terzo decimale** su entrambi i semi: distribuzione
**simmetrica attorno a 90°**. Un ordinamento darebbe eccesso sotto i 10°, un'antiallineazione sopra
i 170°. **Nessuno dei due.**

**Una cosa pende e non la annuncio:** `|<n>|` è sopra il casuale su **entrambi** i semi (1.741 e
1.374). **Ma il nullo che l'osservatore stampa (`1/√N`) è la SCALA, non l'ATTESA.** Misurato con
4000 estrazioni di `N` versori casuali: **`|<n>|·√N = 0.915 ± 0.383`**, `p95 ≈ 1.59`. Contro quello:
`z = +2.11` (seme 1, **sopra** il p95) e `z = +1.16`. **Media 1.64. Va riguardata, non annunciata.**

**⚠ CORREZIONE A UN MIO NUMERO:** la predizione diceva *«`theta` resta a ~43 giri/passo»*.
**Misurato 98.65 e 92.81.** Il `43` è il valore del braccio **ON**, con `--tau-luce`; questi run
sono il sistema naturale. **Il 98–99 % dei nodi compie più di un giro intero per passo.**

**Ciò che (A) toglie di mezzo** è l'obiezione *«ma la FASE 5 non era attiva»*, che rendeva i sei lati
precedenti **non conclusivi**. **Ciò che non toglie:** (A) è l'esito che l'aliasing produrrebbe **da
solo**. Il negativo è **più pulito**, non **conclusivo**.

---

## 6-septdecies. **`--cs-dinamico` era SPENTO** — e la decisione di Luca: **ci va SEMPRE**

Rilievo di Luca, e la verifica ha dato **tre vie indipendenti concordi**.

**1) Dai dati, e non è `0` ma `nan`:** `cs_std = cs_min = cs_max = **nan**` su tutti gli 11 campioni
di entrambi i semi. **`nan` è una prova di ASSENZA, non di costanza**: uno `0` direbbe *«cs c'era e
non variava»*, il `nan` dice che **la cache `_cs_nodo_prev` non esiste.**
**2) Dal codice:** la cache è scritta **solo** dentro `if CS_DINAMICO:` — e `FORK_SU2_MEM` valeva
**1**, letto dal CSV. **Resta solo `CS_DINAMICO`.**
**3) Dal log in-run:** `CS_DIN=False` su entrambi i semi, letto dai **globali vivi** durante il ciclo.

### La decisione, e la ragione è più forte di quella numerica che avevo misurato io

Avevo argomentato sull'**ampiezza**: dove `cs` era acceso, `cs ∈ [1.99954, 2.0]` (**0.023 %**) contro
`tau = d/cs ∈ [0.0271, 1.0509]` (**×38.74**) → **`cs` pesa `0.00629 %` della dispersione di `tau`,
una parte su 15 898**. Il numero resta vero, **ma non è quello che decide**, e il mio «propongo di
lanciare com'è» era sbagliato.

> **Senza `--cs-dinamico` la cache non viene MAI scritta, quindi cade anche il `tau = d/cs` dello
> STRATO 1** (`_bloch_ritardato`), non solo quello di `--tau-luce`: **tutta la memoria del fork
> girava su una legge amputata.**
> **Un `cs` costante non è un `cs` piccolo: è un `cs` ASSENTE**, e rende `tau = d/cs` un
> `tau ∝ d` travestito. **Il punto non è l'ampiezza: è che la legge dev'essere CABLATA.**

**Correzione al rilievo:** diceva che ciò *«spiegherebbe il 16.9 % di T3»*. **No:**
`_rimisura_t3.py` riga 24 **contiene `--cs-dinamico`** — T3 girava col `cs` dinamico. E il **16.9 %
era già stato ritirato** (segno non concorde su 3 semi, `t = −0.77`). **Non c'è un 16.9 % da
spiegare.**

---

## 6-octodecies. ⚠ **IL SIGILLO 23/23 DELLO STRATO 1 NON HA MAI ESERCITATO LA DIPENDENZA DA `cs`**

Rilievo di Luca, **verificato dal disco** — e vale **due volte**, non una.

L'argv di `csv/_seal_fork/_sigillo_strato1.py` (righe **380-386**) **non contiene `--cs-dinamico`**.
E quel sigillo è del blob **`2277e9a0`**, **precedente alla cura della cache**: anche col flag
acceso, la cache sarebbe stata **scartata a ogni mitosi**.

| | |
|---|---|
| **resta valido** | il **meccanismo** del ritardo (slerp geodetico, `alpha = 1−exp(−dt_n/tau)`) e **S7**, che misura `r=2 / r=1 = **1.9753**` — dipende da **`r`**, non da `cs`: il presidio sul tempo proprio **tiene** |
| **mai testato** | che **`tau` SEGUA `cs`** — ed è *proprio* la ragione per cui `tau = d/cs` sarebbe più principiato di `tau ∝ rho` |

> **I quattro run in partenza sono la PRIMA VOLTA che quella dipendenza gira davvero.**
> **Non è «rifare la misura meglio»: è misurare per la prima volta.** *(Scritto prima che partano.)*

---

## 6-novodecies. **T3 sul sistema pulito** — il numero, e perché **non** riporto l'«11 %»

4 bracci, 300 passi, seme **1**, **con `--cs-dinamico`**, blob `08784685`.

| braccio | pendenza | SE | r² | n | `theta` | fallback |
|---|---|---|---|---|---|---|
| PRE OFF | −0.1685 | 0.0090 | 0.126 | 2417 | 129.51 giri/passo | n/d |
| PRE ON | −0.4265 | 0.0091 | 0.464 | 2534 | 43.55 | n/d |
| **POST OFF** | **−0.1024** | 0.0071 | 0.088 | 2146 | 128.88 | **0/302** |
| **POST ON** | **−0.4555** | 0.0082 | 0.567 | 2364 | **38.99** | **2/608** |

Lo script stampa `Delta = −0.0290 ± 0.0122`, `z = 2.37`, «11.0 % recuperato».
**Non lo riporto.** Quella `SE` è **interna a un singolo run**; la dispersione **fra semi** vale
**~0.030** (**C10**). Con `Delta = 0.029` e barra `0.030`, **non c'è un effetto: c'è un seme.**
**È il 16.9 % di stamattina con un'altra cifra**, e quello fu ritirato quando tre semi diedero segno
**non concorde**.

**Regge invece, contro la barra giusta:** **la FASE 2 non si chiude** (divario **−0.2345** verso
`−0.69`, `z ≈ 7.8`) · `--tau-luce` ha un effetto **grande** (ON−OFF **−0.3531**, ~12× la
dispersione) · **`theta` resta ALIASATO a 38.99 giri/passo** nel braccio migliore.

---

## 6-vicies. DUE REGOLE NUOVE, e un reperto che ne è uscito

**§10 — PROMOZIONE DELLE COMPONENTI.** Una componente sotto flag diventa fisica di default **solo**
se: ① **derivata** non tarata · ② **sigillata con CONTROLLO POSITIVO** («con ON DEVONO differire»:
un sigillo che verifica solo la byte-identità a OFF passerebbe anche su **codice morto**) ·
③ **la sua assenza è un DIFETTO, non un'alternativa**. Si promuove il **default**, non si cancella
il ramo. Registro: `doc/COMPONENTI_PROMOSSE.md`, **sezione A VUOTA**.

> **IL REPERTO:** il file ha **51 flag booleani, 10 già a `True`**. Nessuno è passato per quei
> criteri, **perché non esistevano**. Il peggiore: **`TAU_A_LOCALE`** — acceso di default, marcato
> **«IN VERIFICA» dal suo stesso commento**, e **senza flag da riga di comando**, quindi **non
> spegnibile per un A/B**: il criterio ② non è nemmeno *verificabile*. Ed è la branca che produce
> il **punto fisso auto-normalizzante** (`tau_mediano ≈ TAU_A` sempre), cioè **esattamente ciò che
> `--tau-luce` sostituirebbe**. *Una legge «in verifica» è la fisica di default da mesi, mentre la
> sua alternativa è dietro un flag i cui sigilli non passano.*

**§9 — UN DATO DEVE PORTARSI DIETRO LE PROPRIE CONDIZIONI.** Ogni CSV deve portare **blob, seme e
tutti i flag che distinguono quel run dagli altri bracci**. *Un file che si distingue dagli altri
solo per il NOME non è un dato: è un ricordo.* Caso reale: il braccio OFF aveva **136 colonne e
sette flag corretti**, ma **non `TAU_LUCE`** — l'unica variabile che distingue i due bracci — né
`CS_DINAMICO`, né blob, né seme. **Il run non era sbagliato: era non certificabile dai dati.**
Diagnosi **dal disco**: i CSV scritti alle `19:18:46`, la colonna aggiunta alle `19:23:32`,
**cinque minuti dopo**. Sanato: ora il CSV porta `TAU_LUCE`, `CS_DINAMICO`, **blob** (calcolato come
lo calcola git, senza subprocess) e **seme**.

---

## 6-unvicies. **I QUATTRO BRACCI — ESITO (A), non conclusivo. Gradiente di risoluzione 6.4×.**

4 run · 2 bracci × 2 semi · 500 passi · blob `08784685` **scritto dentro ogni CSV**.
Predizione e soglie committate **prima** (`c547294`, `b934445`). Referto: `doc/REFERTO_4bracci_4pi.md`.

**Conformità: PASS su tutti e quattro, ogni campo, letto dal CSV** — `CS_DINAMICO = 1` ovunque,
`TAU_LUCE = 0/0/1/1`, `seed = 1/2/1/2`, tutto il resto identico. **Un solo interruttore di
differenza, e stavolta è nei dati e non nel nome del file.**

### Il gradiente — il valore vero di questi run

| braccio | `theta` s1 | s2 | media |
|---|---|---|---|
| **OFF** | 101.22 | 91.53 | **96.37 giri/passo** |
| **ON** | 16.46 | 13.71 | **15.08 giri/passo** |

> **Fattore 6.39.** Atteso dal T3 (`129 → 39`): **3.3**. Al passo 300: **4.3**. **Finale: 6.39.**
> Il gradiente **cresce col tempo**, ed è il **doppio** di quanto la lettura T3 suggerisse.

### Le firme, tutte al casuale

| | `OFF_s1` | `OFF_s2` | `ON_s1` | `ON_s2` |
|---|---|---|---|---|
| `chi` **materia** | 89.7779 (`z −2.12`) | 89.8756 (`z −1.45`) | 90.0481 (`z +0.56`) | 90.0845 (`z +0.99`) |
| `\|<n>\|·√N` | 1.2373 | 0.7596 | 0.1467 | 0.8130 |
| autocorr. `max\|z\|` | 1.81 | 2.04 | 2.36 | 2.20 |

**Autocorrelazione: `max|z|` fra 1.81 e 2.36 su QUARANTA bin.** Sotto ipotesi nulla il massimo di 40
gaussiane vale ~2.2–2.5. **È esattamente il rumore.** E le **frazioni ai poli** (`<10°` e `>170°`)
coincidono **entro il terzo decimale** in tutti e quattro: distribuzione simmetrica attorno a 90°,
ed è il controllo che **non dipende dalle barre d'errore**.

### ⚠ L'unico `z` grande NON si riproduce

`OFF_s2` dà `chi_p90` con `z = −4.17` → lo script lo marca **INDETERMINATO**. Ma sull'**altro seme
dello stesso braccio** vale **−0.07**: i due differiscono di **0.63°, quattro volte la `SE` interna**.
**È dispersione di run** — la **terza volta oggi** che la `SE` interna produce un falso segnale, dopo
il `16.9 %` e l'`11.0 %`.

### Una domanda aperta si CHIUDE

`|<n>|` **non pende più**. Stamattina 1.741 e 1.374 (`z +2.11`, `+1.16`), *sempre dallo stesso lato*,
lasciata dichiaratamente aperta. Ora su quattro run: **1.237 / 0.760 / 0.147 / 0.813** — **due sotto
e due sopra** il null empirico. **Non si riproduce: era rumore.** Chiusa **con più dati, non con una
rilettura.**

---

## 6-duovicies. DUE PRESIDI DI METODO che questo run ha prodotto — e sono entrambi correzioni a me

**① DUE SEMI NON BASTANO PER UNA BARRA FRA SEMI.** Con 2 semi la deviazione standard ha **un grado di
libertà**, e `t(0.025, 1) = 12.706`: l'IC95 è **12.7 volte** la `SE` della media.

E c'è un caso reale che **sembra un segnale**: `chi` materia è **sotto 90 su entrambi i semi OFF**
(89.778, 89.876) e **sopra 90 su entrambi gli ON** (90.048, 90.084) — **segno concorde**, `z ≈ 3.5`
preso ingenuamente. **Ma l'IC95 con 1 gdl è largo 1.2° e contiene lo zero.**

> **Il segno concorde su due semi non è una prova: è un'ipotesi da rifare con quattro.**
> Registrato come **fronte S**, non come risultato, con la sua soglia: **≥ 4 semi** (`t(3) = 3.18`).
> Se reggesse, sarebbe **la prima firma non nulla del settore**.

**② UNA SOGLIA SU UN SISTEMA CHE CRESCE VA DICHIARATA CON L'ISTANTE IN CUI SI MISURA.**

```
passo  50  (n ~ 80)     cs_std/cs = 0.0086 %     margine sotto l'1 % :  116x
passo 300  (n ~ 3000)   cs_std/cs = 0.096  %                         :   10x
passo 500  (n ~ 3200)   cs_std/cs = 0.19-0.24 %                      :  ~4x
```

**Venti volte in 450 passi.** Avevo registrato il primo valore in **C13** come se fosse una proprietà
del sistema: era **un'istantanea su 80 nodi appena seminati**. **C13 regge** (siamo sotto l'1 %:
`tau = d/cs` è `tau ∝ d`) **ma la sua forza è un quarantesimo di come l'avevo scritta** — e la
traiettoria è **monotòna crescente**.

> **Conseguenza nuova:** il tempo-luce non è *«non testabile mai»*, è **«non testabile a 500 passi»**.
> A maturazione sufficiente `cs` potrebbe uscire dal regime degenere **senza turbo**.

---

## 6-tervicies. IL VERDETTO, e cosa rende dicibile

> *«Con la doppia copertura a 4π attiva, `cs` dinamico cablato per la prima volta, e il settore
> campionato a 13.7–16.5 giri per passo — **6.4 volte** meglio del braccio di riferimento — nessuna
> delle firme misurabili si stacca dal valore casuale: `chi` in materia e nel p90, le frazioni ai
> poli, `|<n>|` contro il null empirico, l'autocorrelazione su 40 bin. **Resta indeciso** se ciò
> dipenda dall'assenza di ordine o dall'impossibilità di vederlo a questa risoluzione.»*

**Ciò che (A) TOGLIE di mezzo:** le obiezioni *«ma la FASE 5 non era attiva»* e *«ma `cs` era
spento»*. **Entrambe chiuse.** È **il negativo più pulito della sessione** — non perché le barre
siano grandi, ma **perché sono piccole** (`SE ≈ 0.09°` su ~210 000 archi): un segnale **sarebbe
visibile**.

**Ciò che NON toglie:** `theta` è ancora **oltre il giro per passo**, col **96–98 %** dei nodi sopra
i 30°/passo *(prima: 99.9 %)*. **La frase «lo spin non si organizza» resta INDICIBILE** finché
`theta` non scende sotto il tetto `2π·cs/λ`.

**E il braccio ON non ha testato il tempo-luce**: con `cs_std/cs = 0.19–0.24 %` ha confrontato
**distanza contro densità** (C13), non tempo-luce contro densità.

---

## 7. IL LAVORO DI CONTORNO, in breve

- **Profilazione** (`doc/PROFILAZIONE_costo_run.md`): il collo **non** è il loop CFL. I due hoist
  autorizzati non valgono la pena, e **non sono stati applicati**. La leva vera è `nsub`, cioè la
  **scala**, non il codice. Corollario da tenere: **il costo È il segnale** — forzare `cs` basso è
  caro *perché* è lontano dal regime naturale.
- **Fix critico** (`cda0931`): il guard di `--gamma-turbo` leggeva `CS_DINAMICO` **prima** che
  fosse assegnato, quindi **turbo sempre spento**, con un avviso che **diceva il falso**. Bug mio,
  e il **terzo** della stessa famiglia (leggere un flag prima dell'assegnazione, come il falso O3c).
  **L'ha visto Luca, non io.** Il primo run K=300 girava a K=1: **buttato**, non riciclato. Il
  presidio non è «ricordarsi l'ordine» ma **non dipendere dall'ordine**: leggere dagli argomenti.
- **Osservatore incrementale** (`ee21618` + `646116f`): senza scrittura incrementale un run lungo
  non è troncabile sull'evidenza. Il primo tentativo scriveva **prima** che la riga fosse completa:
  CSV troncato. Bug mio, corretto.

---

## 8. DOVE SIAMO

**Il quadro e' cambiato di natura, non di segno — e ora sappiamo anche cosa NON e'.**

L'ordine di spin **non manca**: nasce a ogni mitosi (chi = 0 esatto) e viene distrutto ~300 volte
piu' in fretta di quanto nasca. Il meccanismo e' che il Bloch fa **~67-112 giri per tick**, perche'
la coppia e' ordinaria ma l'inerzia e' una densita' di **1.2e-7**.

E oggi si e' chiusa anche la prima ipotesi di cura: **non e' dissipazione mancante.** La
dissipazione c'e' (riga 1918), e' efficace, produce gia' un plateau — e il plateau e' comunque
aliasato. Il coefficiente di Gilbert derivato dal FDT e' **10^4 volte troppo lento**.

> **I sei lati restano validi. Cambia cio' che si puo' concludere da essi:** non *"non esiste una
> fisica ordinante"*, ma *"in questo regime numerico nessun ordine sopravvive a un tick"*.
> E ora sappiamo che **non si aggiusta aggiungendo attrito**: si aggiusta sulla **scala**.

E' la **stessa radice** del fatto gia' noto in `CLAUDE.md` §6 (*a densita' reali cs e' MORTO*): la
densita' minuscola alle scale simulabili **congela** un settore e **fa esplodere** l'altro. Un solo
problema di scala, due sintomi opposti — e ora anche una cura esclusa.

### ⚠ AGGIORNAMENTO 2026-09-15 sera — **tre affermazioni di questo paragrafo erano diventate FALSE**

Le lascio visibili invece di cancellarle, perche' e' utile sapere **come** invecchia un documento:

| diceva | oggi |
|---|---|
| *"Nessun run in volo"* | **falso:** `csv/_test_fork/_controllo_semi.py` sta girando |
| *"il blob sul disco e' `f5887254`"* | **falso:** e' **`b298677a`** — era stale di **tre** blob |
| *"`soliton_simulator.py` **non e' stato toccato**"* | **falso:** e' stato toccato due volte, `TAU_LUCE` e il fix della cache |

**E TUTTI I NUMERI DI RIGA di questo repo sono shiftati.** La tabella di conversione verificata dal
disco e' in `CLAUDE.md` §9, in testa (il rilassamento di `omega_s` **1918 -> 1972**, i due commenti
stale **868 -> 901** e **1803 -> 1852**, e altri 14).

**IL CONTROLLO IN VOLO, e perche' e' contro di me.** La ri-misura T3 dice `Delta = -0.0445 +- 0.0141`,
`z = 3.16`. Quelle `SE` sono l'errore della retta **DENTRO un singolo run**, ma i due bracci sono
**due traiettorie di un sistema caotico** (`N` 3999 contro 4100): **il valore sotto ipotesi nulla non
e' zero**, ed e' la dispersione fra run — **mai misurata su questa osservabile**.
`_controllo_semi.py` la misura su **3 semi x 2 bracci**, con la lettura scritta **dentro lo script
prima dei dati**:

- segno concorde **e** `|media| > 2*SE(media)` -> **sistematico**, il 16.9 % resta;
- segno concorde ma non separato dal rumore -> **plausibile, NON dimostrato**, e il `z = 3.16` cade;
- **segno non concorde** -> era **dispersione di run**, e **"16.9 %" non e' un numero riportabile**:
  vanno corretti `doc/FIX_cache_cs.md` §6, `doc/RAMIFICAZIONI.md` C8/C8-bis, `CLAUDE.md` §9 e
  **questa relazione**.

**Cinque cose aspettano te** *(stato aggiornato al 2026-09-15 sera)*:
1. **alzare l'inerzia**, cioe' rileggere tutto dove la densita' e' O(1): toglie la causa, non il
   sintomo. E' la leva che il lavoro di oggi indica come la sola non-cosmetica;
2. **sotto-passo per lo spin** (lo stesso principio di `nsub`): presidio numerico onesto, non una
   cura. NB: con la crescita **diffusiva con plateau** misurata oggi il numero di sotto-passi
   **non diverge** — ne servirebbero ~112, non "sempre di piu'";
3. **correggere i due commenti stale**, oggi alle righe **901** e **1852** (un commit suo):
   **ANCORA NON FATTO**, e sono loro ad aver fatto partire un mandato da una diagnosi sbagliata;
4. **`_pesi()`**: FASE B non eseguita, la premessa del mandato e' falsa (`doc/REPERTO_pesi_ricorsione.md`);
5. **`:5318`**: il diaglog re-implementa `cs` inline — sotto turbo quella colonna mente.

Il **gate** e' a `c0803713` in `CLAUDE.md` §0, il blob sul disco e' **`b298677a`**. **Non
ri-timbrato di proposito**, e oggi a maggior ragione: i sigilli della FASE 2 **non passano**.
*(La frase precedente diceva `f5887254` e «il `.py` non e' stato toccato»: vera il 15 mattina,
falsa dal cablaggio di `TAU_LUCE` in poi. Storia dei blob: `f5887254` -> `968c903` (estrazione di
`_tempo_luce_nodo`) -> `7d484580` (`TAU_LUCE`) -> **`b298677a`** (fix cache + contatore).)*

Dettagli: `doc/ESITO_scan_turbo_K300.md`, `doc/REPERTO_pesi_ricorsione.md`,
`doc/PROFILAZIONE_costo_run.md`, `doc/REPERTO_gamma_condiviso.md`, `doc/PREDIZIONE_*.md`,
`doc/AUDIT_misurato_vs_asserito.md`, `STATO_CLAUDE_fork-su2.md`, `CLAUDECONNECT.md`.

---

# 9. IL GIRO DEL **2026-09-16** — blob `08784685`, invariato

> **Nessuna riga di `soliton_simulator.py` e' stata toccata oggi.** Tutto quello che segue e'
> lettura di codice, documentazione, strumenti diagnostici e sigilli. I quattro run della voce **S**
> sono **in volo** mentre questo paragrafo viene scritto (passo ~100/500): **i loro numeri NON sono
> qui**, e chi legge non deve aspettarseli.

## 9.1 — I SEI PATTERN COMPORTAMENTALI sono ora nel repo (§0-ter)

`P1..P6` stanno in **`CLAUDE.md` §0-ter** e, identici, in **§0-ter di questa relazione**.
Prima vivevano solo nella conversazione: un Claude web nuovo doveva **farseli dare di nuovo** ogni
volta. **Vanno letti prima di proporre qualsiasi cosa**, e in particolare **P1**: *l'associazione
genera candidati, non conclusioni; prima di scrivere «manca X» si rilegge dal disco.*
*(Precedenti che l'hanno generata: quattro errori dello stesso tipo in un solo giorno, elencati li'.)*

## 9.2 — **A COSA SI ACCOPPIA LO SPIN: e' uscito un TERZO esito, che il mandato non prevedeva**

`doc/MAPPA_accoppiamenti_spin.md`. Il mandato prevedeva due uscite — *«c'e' un accoppiamento,
quindi `lambda` si deriva da li'»* oppure *«non c'e', lo spin e' isolato»*. **Nessuna delle due.**

> ### **ACCOPPIATO MA SENZA BILANCIO. Lo spin parla con tutti e non deve niente a nessuno.**

**Non e' isolato — e' uno dei settori piu' connessi del file.** Decide **dove la materia si divide**
(`rho_spin` -> soglia di mitosi, `:3173`, e coppie di Schwinger, `:3316`), **quanto pesa**
(sorgente di gravita', `:1787`), **quanta inerzia ha lui stesso** (`:1952`), e — l'accoppiamento
piu' forte e il meno citato — **con che verso la gravita' tira**: in `memoria_hebbiana_moto`, che
gira a **ogni passo**, la spinta di ogni arco e' **moltiplicata per `<nb_i . nb_j>`** (`:3583-3586`),
dietro il solo `SPINORE`, che vale `True`. *Due nodi con spin antipodali si respingono invece di
attrarsi; due ortogonali non si vedono.*

**Ma nessuno di questi canali TRASFERISCE una grandezza conservata: sono MODULAZIONI.** E il punto
che decide **si dimostra dalla formula, non si misura**:

> **il torque `cross(B_i, nb_i)` NON e' azione-reazione.** Il contributo della coppia `(i,j)` vale
> `(w_ij/deg_i)*cross(nb_j,nb_i)` su `i` e `(w_ij/deg_j)*cross(nb_i,nb_j)` su `j`: **opposti solo
> se `deg_i == deg_j`** — e questo grafo non e' regolare. In piu', sui legami fra chiralita'
> **uguali** il vicino entra **RIFLESSO** (`z -> -z`), e li' l'antisimmetria non e' rotta da una
> normalizzazione: e' **rotta nella struttura**.

E **nel file non esiste nessuna funzione di energia totale**: `grep -i energ` da' solo commenti,
`lambda_vuoto` (una densita' locale) e il termostato Nose-Hoover (`:2767-2806`) — che e' gated su
`REGIME == "deterministico"`, quindi **spento in tutti i run di questo programma**, e che comunque
agirebbe su `phivel`, **non** su `omega_s`. Lo spinore poi e' normalizzato **`|psi| = 1` in modo
atomico a ogni passo** (`:2128-2129`): **non ha ampiezza, quindi non ha energia** da scambiare.

**Conseguenza diretta, ed e' la terza ragione indipendente dopo il FDT e la FASE 1:**
**`lambda` NON SI DERIVA.** Non perche' manchi un canale: perche' **manca la grammatica**. Cablare
Gilbert resterebbe una **manopola** (§3). La voce **B** del registro passa da *«non aperto»* a
**CHIUSA COME NON DERIVABILE**.

**`TW_SPINORE` non e' «un canale aperto in un verso solo»: e' CHIUSO IN ENTRAMBI.** `tw -> nb`
esiste (`:1990-1996`) ma e' gated su `TW_SPINORE = False`, come `SPIN_LARMOR`; e **`nb -> tw` non
esiste**: la dinamica di `tw` (`:2878-2883`) e' guidata da **`dph`**, la differenza di fase, e non
contiene ne' `nb` ne' `omega_s`.
**⚠ DA NON CONFONDERE CON C11:** li' era la **FASE 5**, l'**orologio** a 4pi in `ritmo()`, cablato e
curato; qui e' `TW_SPINORE`, il **torque** a 4pi, **spento di proposito**. Due cose diverse con lo
stesso «4pi» nel nome.

**COSA QUESTO NON DICE (dichiarato):** che il torque non conservi si **dimostra**; **quanto** non
conservi **non e' misurato**. La misura che lo chiuderebbe costa dieci righe e **zero run nuovi**:
`|SOMMA_i cross(B_i,nb_i)| / SOMMA_i |cross(B_i,nb_i)|` — `~1/sqrt(n)` sarebbe rumore di somma,
`O(1)` violazione grande. **Non fatta oggi.**

## 9.3 — MISURA F e G nell'osservatore, e il **SIGILLO 6/6 PASS**

Per rispondere alla voce **R** servivano `sigma`, `tau` e `theta` **nello stesso run**: sono state
aggiunte all'osservatore come **MISURA F** (le tre pendenze trasversali, con `SE`, `r^2`, `n`, piu'
`t3_attesa = b_sigma + b_tau/2` e `t3_divario`) e **MISURA G** (gli ingredienti del conto FDT).

**La scelta di metodo che conta:** MISURA F **non ricostruisce** la catena di `omega`, **riusa**
`_tracing_omega.ingredienti`. Riscriverla avrebbe riesposto all'errore del 15 — il termine
`cross(_nb_grav(), nb)` omesso, che valeva **~2.8 volte** il deterministico. E poiche' quella
ricostruzione **non contiene** `Bg` ne' `_otw`, e' valida **solo con `SPIN_LARMOR` e `TW_SPINORE`
spenti**: per questo sono **colonne del CSV** (P6) e la conformita' li controlla.

**Sigillo dell'osservatore rigirato, ora con `--cs-dinamico` anche nei suoi run: 6/6 PASS.**
`O1.0` nodi **3020 = 3020** (il confronto **esiste**, prima di leggere lo zero) e `O1`
**`max|A-B| = 0.000e+00`**. Contava davvero: MISURA F chiama `ritmo()`, `_pesi()`, `calcola_psi()` e
`_nb_grav()` — **tutte funzioni che MUTANO cache lette dalla dinamica** — su una copia profonda.

## 9.4 — IL GATE: **resta indietro, e ora c'e' scritto perche'**

Blob sul disco **`08784685`**, gate **`c0803713`**. Fra i due ci sono **tre** cambiamenti e **non
hanno lo stesso stato**: il cablaggio di **`--tau-luce`** ha il **sigillo FALLITO**, mentre le cure
**C7** (5/5) e **C11** (6/6) sono sigillate. **Basta il primo a bloccare il timbro**: il gate
certifica **un blob**, non un sottoinsieme dei suoi cambiamenti.
**Lettura operativa, perche' «gate indietro» non vuol dire «codice non fidato»:** un run **senza**
`--tau-luce` gira su un file il cui unico delta non sigillato e' **inerte**; un run **con**
`--tau-luce` gira su un ramo **esplicitamente non certificato**, e va detto nel documento che lo usa.

## 9.5 — DUE CORREZIONI AL MANDATO, ENTRAMBE SCRITTE **PRIMA** DI ESEGUIRE

`doc/PREDIZIONE_risigillo_strato1.md`. Il §6.2 chiedeva di rilanciare il sigillo dello Strato 1
*«con `--cs-dinamico`, resto identico»*.

1. **«Resto identico» non e' possibile, e S1a/S1b FALLIRANNO — legittimamente.** Fra il blob di
   riferimento (`968fba34`, pre-Strato 1) e `08784685` c'e' **C11**, che **non e' gated su
   `FORK_SU2_MEM`**: gira in ogni run `--campo-spinoriale`. Nel codice nuovo la guardia esatta di
   `ritmo()` passa, nel vecchio falliva nel **95.33 %** delle chiamate. Due orologi diversi -> due
   `r` -> due `dt_n` -> **traiettorie diverse**. **Byte-identita' con un blob che ha un orologio
   diverso sarebbe una CONTRADDIZIONE, non un successo.** *(C7 invece e' un no-op esatto con MEM
   OFF: la cache non esiste.)* Va detto prima, o domani si legge «da 23/23 a N/23» e si conclude una
   **regressione** dove c'e' una **cura che ha fatto il suo mestiere**.
2. **Aggiungere `--cs-dinamico` all'argv NON BASTA a esercitare la dipendenza da `cs`.** Verificato
   dal disco: nei sigilli **in-process** `_cs_nodo_prev` e' `None` (`:330`) oppure
   `np.full(nodi, cs)` (`:224`) — **COSTANTE**. Un `cs` costante non esercita `tau = d/cs`: lo rende
   indistinguibile da `tau ∝ d`. `--cs-dinamico` cambia solo i **tre run veri**; **S7**, il presidio
   piu' fine del lotto, misura la dipendenza da **`r`**, non da **`cs`**.
   **Rilanciare il sigillo com'era avrebbe lasciato il marchio esattamente dov'era.**

**Percio' e' stato scritto il SIGILLO 8**, l'unico del lotto che fallirebbe se `cs` fosse ignorato:
quattro nodi con **`cs = 1, 2, 4, 8`**, stessa `d`, **`r = 1` su tutti** — l'opposto esatto di S7,
che varia `r` e tiene `cs` fisso — e si verifica `alpha = 1 - exp(-dt_n*cs/d)` **nodo per nodo**.
Con `S8b` (il rapporto `cs=8 / cs=1`: se `cs` fosse ignorato varrebbe **esattamente 1.000000000**)
e `S8d`, la controprova con `cs` costante, perche' S8 non possa passare per un artefatto dello slerp.
**In volo mentre scrivo: l'esito non e' qui.**

## 9.6 — IL MERGE IN `main`: piano scritto, **niente eseguito**

`doc/PIANO_merge_main.md`. **Il fatto che cambia il quadro:**

> ### **`main` NON HA MAI TOCCATO `soliton_simulator.py`.**
> `blob: merge-base 194a9456 | main 194a9456 | fork-su2 08784685`

I 20 commit che `main` ha in piu' sono **tutta documentazione** (`CLAUDECONNECT.md` +479 righe,
`Checkpoint.md` +212, `CLAUDE.md` +26, e la cancellazione di 4 file spazzatura).
**Non e' un merge di codice, e' un merge di RACCONTO**, e i conflitti reali — da prova a secco con
`git merge-tree`, che non tocca il working tree — sono **due soli file**: `CLAUDE.md` e
`CLAUDECONNECT.md`.

**Due dei tre presidi del registro non erano dove si credeva:** il **rename dello STATO** e' **gia'
risolto** (`main` non ha **nessun** file di STATO; quello a rischio e' di `dev-spinoriale`, e solo
se si cancella quel branch), l'**AVVISO** e' **chiuso** oggi, e il **ri-timbro del gate** e' il vero
blocco. **E c'e' una trappola operativa che nel registro non c'era:** `main` e' estratto in un
**worktree separato** (`C:/Users/lpeano/st_main`), quindi un `git checkout main` dalla cartella
principale **fallisce** finche' quel worktree esiste.

**RACCOMANDAZIONE: non adesso.** `main` e' oggi **l'unico branch il cui codice coincide con un blob
certificato**; portarci `08784685` significherebbe **perdere l'ultimo punto fermo** mentre la voce
**A** e' aperta. Il pericolo vero non e' il merge mancante: e' che qualcuno **legga `main` e creda
che sia lo stato del progetto**. Una riga in testa a `CLAUDE.md` **di `main`** — *«branch FERMO al
2026-09-10, il lavoro vivo e' su `fork-su2`»* — toglie il 90 % del danno con lo 0 % del rischio.

## 9.7 — UNA DISCREPANZA FRA IL MANDATO E IL DISCO

Il TODO di oggi dice che `AVVISO_LAVORO_IN_CORSO.md` *«NON esiste piu': e' stato chiuso. Non
cercarlo»*. **Esiste**: 8042 byte, ultimo commit `8447f47`, e il contenuto era **stale** (blob
`f5887254`, gate `c0803713`, «nessun run in volo» al 15 a mezzogiorno).
**L'ho SVUOTATO e marcato CHIUSO, non cancellato**, con la tabella di dove sta ora ciascuna cosa che
conteneva: il contenuto era gia' tutto altrove, e cancellarlo avrebbe lasciato la **discrepanza**
senza traccia. **Se Luca lo vuole rimosso e' una sua decisione, non mia.**
*(L'unica cosa non replicata altrove e' stata conservata: le fonti auditate — `ROADMAP:46`/`:42`,
`PROTOCOLLO:41-44`, `STATO:112`/`:433` — **non sono state corrette**, ed e' una decisione di Luca.)*

## 9.8 — COSA E' ANCORA IN VOLO (e quindi cosa NON e' in questa relazione)

| | stato |
|---|---|
| **voce S** — `chi` materia, 4 semi per braccio | **4 run in volo**, 500 passi, passo ~100 al momento della scrittura |
| **voce R** — attesa `sigma + tau/2` ricalcolata | **negli stessi run** (MISURA F). Nessun numero ancora |
| **dispersione di `r`** | idem. Su 2 semi era ~10 % piu' alta nell'ON; **serve la barra fra semi** |
| **conto FDT rifatto** | idem (MISURA G). I tre numeri — `lambda`, `tau_smorz` vs `tau_disordine`, `kT/Lam` — **non ci sono ancora** |
| **ri-sigillo Strato 1 + S8** | **in volo** |

> **Quindi: oggi nessun numero fisico nuovo.** Quello che c'e' e' **una diagnosi strutturale
> (`lambda` non si deriva)**, **due correzioni a un mandato fatte prima di eseguirlo**, **un sigillo
> di purezza 6/6**, e **tre decisioni di igiene scritte invece che rimandate**.

## 9.9 — **I DUE `theta` SONO CHIUSI** (C19): ora girano insieme, e ne e' uscita una correzione alla catena

`theta` non era un'osservabile sola. `_rimisura_t3.py` `:73` usa `theta = |omega|*DT` (tempo di
**COORDINATA** — la convenzione di **C8** e dell'attesa **`-0.69`**); MISURA F usa
`theta = |omega|*dt_n` (tempo **PROPRIO**, quello giusto per §9). **Finche' ne girava una sola, un
numero che si muoveva poteva essere fisica oppure l'unita' di misura che cambia** — ed era gia'
successo.

**Ora l'osservatore scrive ENTRAMBE, fianco a fianco, nello stesso campione:** `theta_coord_*`,
`theta_prop_*` e **`r_ratio_*`**, il loro rapporto, che **e' `r`** (la FASE 5 agisce proprio li').
In MISURA F: `t3_b_theta_coord`, `t3_b_theta_prop`, **`t3_b_r`**.
**Nessuna delle due e' stata dismessa** — la giusta e' `prop`, ma tutto lo storico e' in `coord` e
serve per rileggerlo. **`theta_*` senza suffisso resta come LEGACY ed E' `theta_prop`**: gli 8 CSV
gia' committati e i due script di verdetto la leggono con quel nome, e rinominarla li avrebbe resi
illeggibili. *(Deviazione dichiarata rispetto al mandato, che chiedeva «mai `theta` nudo».)*

**E quanto conta? Al primo campione di prova, 120 passi: `theta_coord = 107.7` contro
`theta_prop = 85.3` giri/passo — il 26 % di differenza sulla mediana.** Non e' un dettaglio.

**Controllo di identita' cablato:** poiche' `theta_prop = theta_coord * r` sullo stesso campione,
deve valere `pend(prop) - pend(coord) - pend(r) = 0` **esattamente**. La colonna `t3_identita`
misura **`4.6e-16`**. Se un giorno non fosse ~`1e-12`, l'errore e' **nel codice, non nella fisica**.

> ### E LA CORREZIONE CHE NE E' USCITA, che non era nel mandato
> Da `|omega|_eq = |F|*sqrt(dt_n*tau/2)` con `dt_n = DT*r`:
> ```
> pend(theta_coord) = sigma + tau/2 +   r/2
> pend(theta_prop)  = sigma + tau/2 + 3*r/2
> ```
> **La formula usata finora, `sigma + tau/2`, ASSUMEVA `pend(r) = 0` — in ENTRAMBE le convenzioni,
> e non era mai stato verificato.** Ora `t3_b_r` lo misura.
> *(Il **divario** resta pero' **indipendente dalla convenzione**: `divario_prop − divario_coord =
> pend(r) − pend(r) = 0`, verificato nei dati. Quindi il residuo non spiegato della voce **R2**
> non era un artefatto di convenzione.)*

---

## 9.10 — **TAGLIO SPETTRALE: predizione scritta, cablaggio NON fatto.** Tre premesse del mandato non reggono

`doc/PREDIZIONE_taglio_spettrale.md`. Il mandato metteva **P1 in vigore** e chiedeva di segnalare,
non eseguire, ogni affermazione in contrasto con un fatto misurato. **Ce ne sono tre.**

**① LA RICORSIONE DATA NON RIDUCE L'AMPIEZZA: PRESERVA LA VARIANZA, esattamente.**
Per `x' = a x + b g` la varianza stazionaria e' `b^2/(1-a^2)`; con `b^2 = 1-a^2` vale **1**, cioe'
quella del rumore bianco. Verificato: **analitico `1.000000`, simulato `0.997330`** su 400 000
passi, `tau_c = 0.400` = 40 passi. **Cambia solo la STRUTTURA TEMPORALE, non l'ampiezza.**
La stima «varianza /20 -> ampiezza /4.47» descrive un oggetto **diverso** (banda limitata a densita'
spettrale costante) e per ottenerlo servirebbe **moltiplicare per `sqrt(2 dt/tau_c)`**, cioe'
**toccare `amp`** — che il mandato vieta e che sarebbe **un coefficiente scelto** (§3).
**Le due prescrizioni del mandato sono incompatibili fra loro.**

**② IL RUMORE NON MUOVE IL BLOCH. Lo muove `omega`, di tre ordini di grandezza.**
Misurato sui quattro run di oggi:

| run | calcio del rumore | moto del Bloch | rapporto |
|---|---|---|---|
| OFF s3 / s4 | **7.68 / 8.44** gradi/passo | 37 874 / 37 866 | **0.020 % / 0.022 %** |
| ON s3 / s4 | **7.23 / 9.42** | 5 705 / 4 274 | **0.127 % / 0.220 %** |

Il «kick da ~90 gradi» **non esiste**: vale **7-9 gradi**. Il `85.6` citato e' reale ma e' lo
spostamento del **padre nel passo della nascita su n = 7** (`doc/BILANCIO_ordine_spin.md:97`, che
scrive esso stesso *«se regge sulla statistica»*) — **non una misura del rumore**.
E dal codice: sotto `--spinore-corretto` il `_nb` committato e' **derivato da `_psi_spinor`**, quindi
il calcio del rumore viene **sovrascritto**: il rumore entra **solo nella COPPIA**, via
`cross(B, nb)`.

**③ E QUELLA COPPIA E' GIA' MISURATA MARGINALE: `R_stoc = 0.041` contro l'errore atteso `0.097`
(C6).** Il taglio agisce su un canale che vale il **4 %** dell'ingresso di `omega`, **senza
cambiarne l'ampiezza**. Non c'e' via per cui `theta` scenda di 4.5x.

> **PREDIZIONE CORRETTA: `theta` NON SCENDE. Se si muove, SALE** (≲ 5 %). Una forzante **correlata**
> su 40 passi fa crescere `omega` stocastico come **`n`** invece che `sqrt(n)` — fino a `sqrt(40)
> ~ 6.3` **sulla sola componente stocastica**, che pero' vale il 4 %.
> **E l'ipotesi qualitativa del mandato non puo' verificarsi:** richiede che il rumore domini la
> decorrelazione del Bloch, e la domina allo **0.02-0.22 %**. `B` e' costruito da `_nb_prec`, il
> Bloch committato, il cui moto e' `omega`. **Colorare il rumore non puo' stabilizzare `B`.**

**COSA RESTA IN PIEDI, ed e' la parte che conta:** *«si fa perche' il rumore bianco e' fisicamente
SBAGLIATO»*. **Questa giustificazione regge intatta** e non dipende da nessuna delle tre
correzioni: `tau_c = LAM/CS_M` e' **derivato**, la ricorsione **non introduce coefficienti**.
**Il cablaggio ha senso — ma per correggere una legge sbagliata, aspettandosi che NON cambi i
numeri.**

**E una correzione da fare comunque, se si cabla:** **il `dt` della ricorsione dev'essere
`dt_n = DT*r`, non `DT`**. Il mandato non lo dice; §9 e' esplicito che `DT` nudo dentro un processo
locale impone **un frame preferito**. **E' l'errore gia' preso nello Strato 1**, che S1..S6
passavano identici e solo **S7** ha stanato: **serve un sigillo tipo S7 fra N1 e N6**, o passerebbe
invisibile come allora.

**Serve il via di Luca su una cosa sola: quale delle due prescrizioni incompatibili vale.**

---

## 9.11 — **IL TAGLIO SPETTRALE E' CABLATO** (flag OFF), e il sigillo e' a meta': N1/N1b PASS, poi SI E' SCHIANTATO

> **Via libera di Luca, 2026-09-16**, dopo aver letto e accettato le tre correzioni del §9.10:
> *«il cablaggio resta legittimo, ma per la sola ragione onesta — e senza aspettarsi niente su
> `theta`»*. **Risolve l'incompatibilita' del mandato in favore di `amp` INTOCCATA: rumore
> DIVERSO, non rumore MINORE.**
>
> **Blob: `08784685` -> `c5e5088c` -> `a467fd9a`.** Due commit di codice, entrambi **prima** di
> qualsiasi run (§5). **Il flag nasce OFF.**

### 9.11.1 — Come e' cablato

```
tau_c = LAM / CS_M = 0.400  = 40 passi        # tempo-luce del solitone: DERIVATO
a = exp(-|dt_n| / tau_c)      b = sqrt(1 - a^2)
xi = xi*a + b*g                               # g = la STESSA rng.normal(0,1,(n,3)) del ramo bianco
_nb += xi * amp                               # amp INVARIATA
```

Il ramo OFF e' **letteralmente invariato** (`_calcio = _g`), e **`g` e' estratto PRIMA del ramo**,
nella stessa posizione di prima: cosi' il braccio spento consuma l'RNG **esattamente** come faceva.
E' la condizione che rende possibile N1.

**Tre scelte di costruzione, dichiarate:**
1. **`dt_n = DT*r`, non `DT`** — il rumore e' un processo **locale** del nodo; `DT` nudo
   imporrebbe la foliazione sincrona globale, cioe' **un frame preferito** (§9).
2. **`xi` inizializzato da `N(0,1)`, cioe' dalla distribuzione STAZIONARIA.** Partire da zero
   darebbe un primo calcio attenuato di `b = 0.22` per ~40 passi: **un artefatto all'accensione**.
   Costo dichiarato: **un'estrazione RNG in piu'**, che rende impossibile una byte-identita' di
   run intero per N2 — per questo N2 e' scritto come **controllo mirato**.
3. **Eredita' di `_xi_rumore` alla mitosi**, stessa convenzione di `_nb`/`_nb_prec`/`_nb_ret`/
   `omega_s`/`_psi_spinor`/`_psi_prec`/`_cs_nodo_prev`/`_psi_spin_prec`. **E' la terza volta**
   (C7, C11): **stavolta scritta PRIMA di misurarla, non dopo.**

### 9.11.2 — ⚠ UN DIFETTO TROVATO LEGGENDO IL CHIAMANTE, non aspettando che esplodesse

> **`_passo_spinoriale` NON riceve `dt_n`: riceve `dt_n_s`** (`:2931`).

E `dt_n_s` (`:2747-2751`), sotto **`--tempo-segno`** (MOD 5.3a, Feynman-Stuckelberg), vale
`(1 + (perc_chi-1)*m_coer) * dt_n`, che per l'**antimateria coerente e' NEGATIVO**.
Con `dt_n < 0` verrebbe `a = exp(+|dt|/tau_c) > 1` e la ricorsione **sarebbe divergita IN
SILENZIO**: nessun NaN subito, solo `xi` che cresce di passo in passo finche' il Bloch smette di
avere senso. Da qui **`|dt_n|`**: il tempo di correlazione e' una **durata**, dipende dal modulo
del tic, non dal verso. **Nessun numero nuovo** — e' la stessa classe di guardia dei
`np.maximum(..., 1e-9)` gia' nel file.

**Oggi `TEMPO_SEGNO = False` e non cambia un bit.** Lo scrivo lo stesso perche' **un difetto che
esiste solo in una combinazione di flag e' esattamente quello che salta fuori fra sei mesi**,
quando nessuno ricorda che le due cose interagiscono.

### 9.11.3 — ⚠⚠ LA TRAPPOLA CRLF HA MORSO **DA SOLA**

Fra il commit `7f2af6c` e il cablaggio, `soliton_simulator.py` era tornato **CRLF** (442240 byte,
6510 CRLF, sha1 grezzo `37c31630`) **senza che io avessi lanciato nessun `git checkout`**.
L'ha fermata l'`assert '\r\n' not in s` che avevo messo in testa allo script di patch: **senza,
avrei scritto un file misto.**

> **E' la seconda volta in una giornata.** La prima l'avevo causata io con `git checkout`; questa
> e' arrivata da sola. **Il `.gitattributes` con `soliton_simulator.py text eol=lf` non e'
> cosmesi: e' l'unica cosa che toglie la trappola alla radice.** Resta una decisione di Luca.

### 9.11.4 — IL SIGILLO: due PASS, poi uno SCHIANTO

```
[PASS] N1.0   il riferimento e' il blob PRE-cablaggio      blob = 08784685 (atteso 08784685)
[PASS] N1.0b  stesso numero di nodi (il confronto ESISTE)  PRE = 3020, POST(OFF) = 3020
[PASS] N1     flag OFF vs codice pre-cablaggio             max|A-B| = 0.000e+00
[PASS] N1b    ON != OFF (il flag FA qualcosa)              35 array divergenti
```

**Il ramo OFF e' intatto e il flag non e' codice morto. Questo e' stabilito.**

> **⚠ E N1b NON VA LETTO COME MISURA DI UN EFFETTO.** I nodi finali sono **3020 (OFF) contro 2449
> (ON)**, ma il ramo ON consuma **un'estrazione RNG in piu'** all'inizializzazione, quindi le due
> traiettorie divergono **completamente dal primo passo**: e' **caos con semi diversi**, non
> l'ampiezza di un effetto fisico. N1b prova **solo** che il flag fa qualcosa.

**POI LO SCHIANTO:**
```
AttributeError: 'numpy.random._generator.Generator' object attribute 'normal' is read-only
```
La spia di N7 monkeypatchava `net.rng.normal`, che in numpy e' **read-only**. **N2, N3, N6 e N7
non sono girati.**

> **E' lo stesso modo di fallire del sigillo dello STRATO 1 di stamattina: NON FALLISCE, SI
> SCHIANTA** — la modalita' piu' facile da non notare. Due volte in un giorno, su due sigilli
> diversi, per la stessa ragione strutturale: **un guscio in-process che tocca il simulatore
> pezzo per pezzo si rompe appena il simulatore cambia forma.**
> **Corretto:** la spia ora avvolge l'**oggetto** `rng` con un proxy che inoltra tutto e registra
> solo `normal` (`net.rng` e' un attributo normale, quindi sostituibile). Resta pure-read: non
> cambia ne' l'ordine ne' il numero delle estrazioni.

### 9.11.5 — E IL CRITERIO SBAGLIATO ERA MIO — il contatore lo ha detto prima di schiantarsi

`_xi_fallback = 2` su 36 chiamate nella costruzione della scena. **Non e' un difetto**, e il
perche' conta: il ramo di estensione scatta quando i nodi crescono **senza passare da
`_eredita_spinore_figli`**, cioe' su **`semina()` e `nuova_massa()` — LA TERZA VIA DI CRESCITA,
la voce H del registro**. Li' l'estensione e' **corretta**: i nodi esistenti **conservano** il
loro `xi` (vstack sulla testa) e **solo i nuovi** ricevono un'estrazione stazionaria, perche' un
nodo appena nato non ha passato.

> **Quindi il criterio di N3b che avevo scritto era SBAGLIATO:** *«fallback <= 1»* **in assoluto**
> avrebbe fatto **fallire il sigillo per una ragione legittima**.
> **Corretto in DELTA:** sui 25 passi di sola mitosi l'estensione **non deve scattare affatto**,
> perche' li' l'eredita' deve bastare. **E' il criterio che misura la cosa giusta**, e la
> differenza fra i due non e' stilistica: uno avrebbe prodotto un FAIL falso, e un FAIL falso
> costa piu' di un sigillo mancante, perche' si porta dietro una diagnosi.

### 9.11.6 — COSA E' ANCORA IGNOTO

| | stato |
|---|---|
| **N2** — `tau_c -> 0` collassa sul rumore bianco | **non girato** |
| **N3 / N3b** — `_xi_rumore` esteso alla mitosi | **non girato** |
| **N6** — stabilita', `\|nb\| = 1`, no NaN/runaway | **non girato** |
| **N7 / N7b / N7c** — **la ricorsione usa `dt_n = DT*r` per nodo, e col `DT` nudo NON tornerebbe** | **non girato — ED E' QUELLO CHE DECIDE** |
| campagna `{OFF, ON} x >= 2 semi` | **non lanciata** |

> **N7 e' il sigillo che conta, e la ragione non e' ovvia:** N1..N6 provano la **struttura** — ramo
> OFF intatto, il flag fa qualcosa, lo stato si eredita, nulla esplode — e **passerebbero IDENTICI
> anche se la ricorsione usasse `DT` nudo**, cioe' col tic di **coordinata** al posto del tempo
> proprio del nodo. **E' esattamente il bug gia' preso nello Strato 1, dove S1..S6 passavano
> identici e solo S7 lo ha stanato.**

**E la predizione resta quella del §9.10, invariata:** `theta` **non scende**, e se si muove
**sale** (<= 5 %). **Si e' cablato perche' il rumore bianco e' fisicamente sbagliato, non perche'
risolva l'aliasing.** Se il verdetto dovesse mostrare un calo significativo, **il reperto sarebbe
a mio carico**: vorrebbe dire che uno fra C6, il rapporto 0.02-0.22 % e la conservazione della
varianza non regge.

---

## 9.12 — **STOP AI TEST. DUE CORREZIONI DI DIFETTO, SENZA FLAG.** E `M2`, il sigillo decisivo, **PASSA**

> **Decisione di Luca, 2026-09-16:** i test in corso si interrompono, e due difetti entrano nel
> codice **senza flag**, come **correzioni di difetto** (categoria **D** del registro: *un bug
> curato non ha un interruttore*).
> **Blob: `a467fd9a` -> `57681b9e` -> `c57800c1`.** Due commit di codice, uno per correzione,
> **entrambi prima di qualunque run** (§5).
>
> ### ⚠ MARCHIO SU TUTTI I DATI PRECEDENTI
> **Ogni misura di questo repo prodotta prima del blob `c57800c1` e' «prodotta con `_xi_rumore`
> EREDITATO alla mitosi e SENZA il fattore `cs^-2` nell'inerzia: misura di un sistema DIVERSO da
> quello corrente».** Vale per gli 8 CSV della campagna, per i sigilli di oggi, e per tutto cio'
> che sta in §9.1-9.11.

### 9.12.1 — La trappola CRLF e' chiusa alla radice

`.gitattributes` con `*.py|*.md|*.csv|*.txt|*.json text eol=lf` e i binari marcati `binary`.
**Provato con lo stesso comando che aveva causato il danno stamattina:**
```
git checkout -- soliton_simulator.py  ->  444654 byte, 0 CRLF, sha1 a467fd9a   INVARIATO
```
*(La regola non riscrive nulla: fissa cio' che gia' c'e'. Verificato prima e dopo
`git add --renormalize .`: byte identici.)*

### 9.12.2 — CORREZIONE ① : `_xi_rumore` NON si eredita — **e l'analogia sbagliata era MIA**

Stamattina avevo aggiunto l'eredita' di `_xi_rumore` alla mitosi, scrivendo che era *«la stessa
convenzione di `_nb`/`_nb_prec`/`_nb_ret`/`omega_s`/`_psi_spinor`/`_psi_prec`/`_cs_nodo_prev`/
`_psi_spin_prec`»* e **vantandomi di averla scritta PRIMA di misurarla** invece che dopo (C7, C11).

> **L'analogia era FALSA, e averla applicata in anticipo non la rende giusta.**
> Quegli otto sono **proprieta' del NODO**: e' corretto che il figlio le erediti.
> **`xi` no: e' un campione dell'AMBIENTE che spintona il nodo, un processo ESTERNO.**
> **Due nodi distinti non ricevono lo stesso identico spintone.**

**Cosa produceva:** padre e figlio con rumore **correlato al 100 %** per ~40 passi
(`tau_c = LAM/CS_M`) — una correlazione **spuria** fra oggetti che devono essere indipendenti, e
**proprio nella grandezza che serve a decorrelare**.

**La correzione e' una CANCELLAZIONE**: si toglie il blocco, e il figlio riceve un `xi` **fresco**
dal ramo di estensione gia' presente, che estrae dalla **stazionaria** (`N(0,1)`, coerente con
`b = sqrt(1-a^2)`) — non da zero, che sarebbe un transitorio artificiale. **Nessun feedback sul
padre:** il rumore non e' una quantita' che si ripartisce.

**E i contatori cambiano nome, perche' cambia il loro significato:** `_xi_fallback` ->
`_xi_esteso` + `_xi_nuovi`. **L'estensione non e' piu' un fallback: e' IL PERCORSO NORMALE della
mitosi.** Chiamarla «fallback» avrebbe fatto leggere come difetto il comportamento **corretto** —
ed e' esattamente l'errore che avevo gia' fatto scrivendo il criterio di N3b, che avrebbe prodotto
un **FAIL falso**.

### 9.12.3 — CORREZIONE ② : il fattore `cs^-2` nell'inerzia

`inerzia = max(rho, 1e-6)` **non aveva alcuna dipendenza da `cs`**. La derivazione la impone
(`doc/INERZIA_tempo_quadro.md`, esito **(b)**): `correzione` e' adimensionale e `omega` e' `1/T`,
quindi `correzione/inerzia` deve dare `1/T^2` -> **`inerzia` e' un TEMPO AL QUADRATO**, e il tempo
proprio del nodo e' `d/cs` -> **`inerzia ∝ (d/cs)^2 ∝ cs^-2`**.
**Esponente DERIVATO, verso CONFERMATO** (Compton con `c -> cs`), e **lo stesso esponente dello
Step 2** (`omega_clk *= (cs/CS_M)^2`), derivato **prima e indipendentemente**: consistenza
**trovata**, non costruita.

**Forma:** `inerzia = max(rho * (CS_M/cs_nodo)^2, 1e-6)`. Adimensionale, **esattamente 1** dove
`cs = CS_M`. Nessun coefficiente nuovo, nessun floor nuovo; `cs_nodo` dalla cache
`_cs_nodo_prev` col fallback **contato** (P5).

**Perche' e' una correzione di CONSERVAZIONE:** alla mitosi il figlio riceve un'inerzia nuova e il
padre non ne perde, quindi **`L_tot = somma(I*omega)` cresce a ogni divisione**. `omega` e'
intensiva — un corpo rigido che si spezza mantiene `omega` in ogni frammento — quindi **e'
l'inerzia che deve ripartirsi, e non lo fa**. Con `inerzia ∝ cs^-2` la nascita di un figlio alza
la densita' locale, abbassa `cs` locale, e **l'inerzia di padre e figlio aumenta insieme**: un
feedback **mediato dal campo**, che non richiede di sottrarre nulla al padre — cosa peraltro
impossibile, perche' `|psi|^2` e' **ricalcolata dalle fasi**, non e' una variabile di stato.

**Una scelta di struttura, dichiarata:** la lettura di `_cs_nodo_prev` e' scritta **inline** e non
estratta in un metodo, benche' gemella di quella in `_tempo_luce_nodo`. **Duplicazione
consapevole:** oggi **tre sigilli si sono rotti** perche' un metodo estratto non era nei gusci
in-process. Il commento marca i due punti come da tenere allineati.

### 9.12.4 — ✅ `M2`, IL SIGILLO DECISIVO: **PASS**

> `(CS_M/cs_nodo)^2` vale **esattamente 1** dove `cs = CS_M`, e **`rho * 1.0 == rho` bit per bit**
> in IEEE. Quindi **senza `--cs-dinamico`** (cache mai scritta -> fallback a `CS_M`) il codice
> NUOVO **deve** essere byte-identico al riferimento. Se non lo fosse, **la FORMA del fattore
> sarebbe sbagliata**, e ci si ferma li'.

```
M2   nodi PRE = 3070, POST = 3070      <- il confronto ESISTE (le shape PRIMA dello zero)
     34 array numerici confrontati
     max|A-B| = 0.000e+00              array divergenti: 0          PASS
M2b  con --cs-dinamico: 3020 contro 3101 nodi, 35 array divergenti  PASS (il fattore MORDE)
```

**`M2b` e' il controllo opposto e serve tanto quanto `M2`:** senza, `M2` passerebbe anche su un
fattore **inerte**, cioe' su codice morto.

### 9.12.5 — E IL NUMERO CHE IL MANDATO CHIEDEVA DI DICHIARARE PRIMA

| | |
|---|---|
| `cs` | `[1.994899, 2.000000]` |
| `cs_std / cs` | **0.0333 %** |
| fattore `(CS_M/cs)^2`, **mediana** | **1.000004812** |
| scarto **massimo** da 1 | **5.1e-03** |

> **L'attesa scritta prima e' confermata:** il fattore vale **1.0000048** sul nodo mediano.
> **L'effetto quantitativo OGGI e' minuscolo**, esattamente come dichiarato nel commit **prima** di
> guardare i dati. **La correzione si e' fatta perche' senza la legge e' SBAGLIATA**, non per un
> effetto misurabile a questa densita'.

**E una precisazione che va fatta, perche' il numero non e' nessuno dei due gia' citati:** il
`cs_std/cs` misurato qui e' **0.033 %**, mentre C13 riporta **0.0086 %** al passo 50 e **0.24 %**
al passo 500. Questi run sono a **150 passi**, e la traiettoria di quel rapporto e' **monotona
crescente**: il valore sta **dentro** la forbice, ma **non e' nessuno dei due estremi**, e citarlo
come se lo fosse sarebbe stato sbagliato.

### 9.12.6 — IL SIGILLO E' ATTERRATO: **11/13 PASS, due FAIL — ed entrambi sono CRITERI MIEI SCADUTI**

```
[PASS] M0   riferimento = blob a467fd9a         444654 byte, 0 CRLF (sha1 dei BYTE GREZZI)
[PASS] M0b  il codice corrente e' DIVERSO       c57800c1, 448943 byte, 0 CRLF
[PASS] M0c  nessuno dei due ha CRLF             .gitattributes in vigore
[PASS] M2.0 il confronto ESISTE                 nodi PRE 3070 = POST 3070
[PASS] M2   cs = CS_M -> BYTE-IDENTICO          max|A-B| = 0.000e+00        <- IL DECISIVO
[PASS] M2b  con cs VIVO il fattore MORDE        3020 contro 3101, 35 array divergenti
[PASS] M1   PRIMA il rumore era CORRELATO       corr = +1.0000
[FAIL] M1b  DOPO dev'essere INDIPENDENTE        corr = nan su 0 coppie
[FAIL] M3   len(_xi_rumore) == n a ogni passo   estensioni 24, nodi con xi fresco 1734
[PASS] M4   la conservazione e' calcolabile     (misura, non timbro)
[PASS] M5a  |nb| = 1                            max||nb|-1| = 2.220e-16 su 3101 nodi
[PASS] M5b  nessun NaN/inf                      tutti finiti
[PASS] M5c  nessun runaway                      max|x| = 9.355
                                                SIGILLO CORREZIONI: 11/13 -> FAIL
```

**`M1` da' `corr = +1.0000`, non il `+0.951` che avevo previsto**, e il motivo e' che misuro al
**momento dell'eredita'**, prima che il passo successivo li faccia divergere: il difetto era
**massimo**, non attenuato. **Meglio cosi' per il sigillo:** un controllo positivo piu' netto.

**I DUE FAIL: VERIFICATI, non spiegati via.** Ho misurato invece di argomentare:

| | |
|---|---|
| `len(xi)` **dopo `step()`** | **allineato**: 1608=1608, 1652=1652, 1703=1703, 1750=1750 |
| `len(xi)` **dopo `mitosi()`** | **corto**: 1608 contro 1652, 1652 contro 1703, 1703 contro 1750 |

**`M3` controllava a FINE passo, cioe' DOPO `mitosi()`** — dove l'array e' legittimamente corto,
**perche' con la correzione ① l'estensione avviene dentro `_passo_spinoriale`**, che e' la **prima**
cosa del passo dopo. **L'array non e' mai stale quando viene USATO**: chi lo usa lo estende prima.
**Il criterio giusto e' «allineato dopo `step()`», e il mio era scritto per la versione EREDITATA.**

**`M1b` dava `0 coppie` per la stessa ragione**: subito dopo la mitosi i figli **non hanno ancora**
un `xi`, quindi non c'era niente da correlare. Misurato **uno step dopo**, su una scena vera:

> ### **corr(xi_padre, xi_figlio) = +0.0065 su 258 coppie** — contro **+1.0000** prima della correzione.
> **La correzione ① funziona.** Il rumore di padre e figlio e' indipendente.

**Ma il sigillo resta FAIL finche' non lo rigiro con i criteri giusti**, e il fallimento e'
committato com'e' (§5). **Un criterio scaduto che produce un FAIL falso costa piu' di un sigillo
mancante**, perche' si porta dietro una diagnosi — ed e' la **seconda volta oggi** che scrivo un
criterio per una versione del codice che nel frattempo e' cambiata (la prima fu `N3b`,
«fallback <= 1»).

### 9.12.7 — Dove eravamo rimasti coi test, e cosa resta

**Il sigillo del rumore colorato era a 12/13 prima dello STOP:**
> **`N7` E' VINTO** — `max|xi_mis - xi_atteso(dt_n)| = **0.000e+00**` nodo per nodo, contro
> **`6.142e-01`** col `DT` nudo, `std(a)` fra i nodi `1.133e-02`. **Il tic della ricorsione E' il
> tempo proprio del nodo.**

L'unico FAIL era **`N2`**, e la causa era **mia, tre volte diverse**: alzare `CS_M` piantava il
**CFL** (46 minuti al 68 % di CPU: *non falliva, si piantava*); abbassare `LAM` **spegneva il
campo** (`Lam = 0` -> la guardia saltava l'intero blocco del rumore -> `n/d`); la via giusta —
alzare `CS_M` **solo dentro `_passo_spinoriale`** — e' scritta ma non ancora eseguita.

| | stato |
|---|---|
| `M1b` e `M3` coi criteri corretti | **da rigirare** (il difetto e' nel criterio, ed e' misurato) |
| metriche §3 nell'osservatore (`L_tot`, `r` per eta', corr `xi`, fattore `cs`) | **da fare** |
| campagna `{OFF, ON} x >= 2 semi` sul sistema corretto | **da rifare** |
| `N2` del rumore colorato | **da rigirare** sul nuovo riferimento |

---

## 9.13 — I CRITERI RISCRITTI: **15/16 PASS**, `M1c` (che mancava) passa, e **la prima misura della conservazione mai fatta**

> Il sigillo delle due correzioni era uscito **11/13** con due FAIL, **entrambi criteri miei
> scaduti**. Riscritti e rigirati: **15/16**. Il sedicesimo era **ancora un criterio mio**.

### 9.13.1 — I criteri giusti, e cosa c'era di sbagliato in ognuno

| | avevo scritto | giusto | esito |
|---|---|---|---|
| **M1** | `\|corr\| > 0.5` | **`max\|xi_figlio - xi_padre\| == 0` esatto** — il vecchio codice **copiava**: non e' «correlazione alta», e' **identita' byte a byte** | **PASS** `0.000e+00` su 84 coppie |
| **M1b** | misurare **subito dopo `mitosi()`**, soglia `0.15` | misurare **dopo lo `step()` successivo**, soglia **`3/sqrt(3N)`** | **PASS** `corr = -0.0605`, `3 sigma = 0.1651` -> **1.10 sigma** |
| **M1c** | **non esisteva** | `var(xi_neonati) ~ 1`, nullo `sqrt(2/k)` | **PASS** `0.9756` su 330, `1 +- 0.0778` -> **0.31 sigma** |
| **M3** | `len(xi) == n` a **fine passo** | `len(xi) == n` **dopo `step()`**, cioe' **quando viene usato** | **PASS** |
| **M3b** | **non esisteva** | l'estensione **non tocca la testa**: i nodi esistenti conservano `xi` | **PASS** |
| **M3c** | `_xi_nuovi == nodi nati` | `_xi_nuovi == nati - ultima nidiata` (**sfasamento di un giro**) | **FAIL**, poi corretto |

> ### `M1c` e' quello che mancava, ed e' quello che rende `M1b` non vuoto.
> **`M1b` da solo non prova che la correzione sia giusta: prova solo che i figli sono
> INDIPENDENTI dai padri. Un figlio con `xi = 0` passerebbe `M1b` a pieni voti** — e sarebbe
> sbagliato, perche' darebbe esattamente il transitorio (`b = 0.22` per ~40 passi) che
> l'estrazione stazionaria esiste per evitare. **Passa: `var = 0.9756`, a 0.31 sigma da 1.**

**E le soglie non sono piu' scelte.** `|corr| < 0.15` me l'ero **inventato**. Il valore sotto
ipotesi nulla della correlazione campionaria di variabili indipendenti e' `sigma ~ 1/sqrt(3N)`;
su 110 coppie da' `3 sigma = 0.165`. **E' lo stesso presidio del «valore sotto ipotesi nulla»
gia' scritto in `CLAUDE.md` §9 — che avevo applicato agli altri e non a me.**

### 9.13.2 — `M3c`: **«nodi nati 0»**, un numero IMPOSSIBILE

E' quello il segnale che l'errore fosse mio. Misurato iterazione per iterazione:

```
nati DURANTE step()  :   0     <- quello che M3c contava
nati DURANTE mitosi(): 211     <- dove nascono DAVVERO
xi freschi assegnati : 194

nati    per iterazione: 0, 0, 24, 42, 50, 41, 37, 17
freschi per iterazione: 0, 0,  0, 24, 42, 50, 41, 37
```

> **`freschi[k] == nati[k-1]` per OGNI k**, e la differenza `211 - 194 = 17` e' **esattamente**
> l'ultima nidiata, che ricevera' il suo `xi` al giro dopo. **Il contatore e' corretto**; il mio
> criterio confrontava la crescita attraverso `step()`, che e' **zero per costruzione**.

**Corretto:** ora il criterio chiede `_xi_nuovi == nati - ultima_nidiata`, e **lo sfasamento e'
parte del criterio, non una tolleranza**: se non tornasse **esattamente**, il contatore mentirebbe.

### 9.13.3 — ⚠ **TRE CRITERI SBAGLIATI IN UN GIORNO, E LA FORMA E' SEMPRE LA STESSA** (nuovo presidio in §9)

| | l'errore |
|---|---|
| **`N3b`** | *«fallback <= 1»* **in assoluto**, mentre l'estensione su `semina()`/`nuova_massa()` e' **legittima** (voce **H**) |
| **`M1b`/`M3`** | misurati nel **momento sbagliato**: subito dopo `mitosi()`, dove i figli **non hanno ancora** `xi` e l'array e' **legittimamente corto** |
| **`M3c`** | confrontato con la **coppia sbagliata**: crescita di `step()`, **zero per costruzione** |

> **La radice e' una sola: ho scritto il criterio dal MIO MODELLO MENTALE del codice invece che da
> una MISURA di cosa il codice fa nel punto in cui il criterio guarda.** Tutte e tre le volte la
> misura ha impiegato **meno tempo della spiegazione** che avrei dato senza farla.
>
> **E un criterio scaduto che produce un FAIL falso costa PIU' di un sigillo mancante, perche' si
> porta dietro UNA DIAGNOSI:** chi legge il FAIL cerca il difetto nel codice, e il difetto non c'e'.
>
> **Corollario utile:** `«nodi nati 0»` era un numero **impossibile**, ed e' il modo in cui un
> criterio sbagliato **si denuncia da solo**. Vale la pena cercarli.

### 9.13.4 — `M4`: **LA PRIMA MISURA DELLA CONSERVAZIONE MAI FATTA** — e non e' un timbro, e' un risultato

```
PRE   20 eventi di crescita   Delta L / L per passo: mediana +0.0340   media +0.0413   517 nodi nati
POST  20 eventi di crescita   Delta L / L per passo: mediana +0.0355   media +0.0397   479 nodi nati
```

> ### **`L_tot = somma(inerzia * |omega|)` CRESCE del ~3.4 % A OGNI PASSO con crescita.**
> ### **In ENTRAMBI. La violazione e' MISURATA, non piu' argomentata.**

**E la correzione ② NON la chiude a questa densita'** — esattamente come scritto **prima** di
guardare i dati: il fattore `(CS_M/cs)^2` vale **1.0000048** sul nodo mediano, e **non puo'
spostare un bilancio che sbaglia del 3.4 % per passo**.

**⚠ E il confronto `0.0340` contro `0.0355` NON e' significativo:** `PRE` e `POST` sono
**traiettorie caotiche diverse** (517 contro 479 nodi nati). **Cio' che conta e' che ENTRAMBI
stiano a ~3.4 %**, non quale dei due sia piu' alto. *(E' lo stesso errore di lettura di `N1b`,
dove `3020 contro 2449` nodi non era l'ampiezza di un effetto ma caos con semi diversi.)*

**Cosa questo apre, e va detto senza gonfiarlo:** il mandato diceva che la correzione ② e' «di
conservazione». **Lo e' in linea di principio — il meccanismo del feedback mediato dal campo c'e'
— ma a questa densita' il canale e' chiuso**, perche' `cs` e' quasi-costante (`cs_std/cs = 0.033 %`).
**La violazione del 3.4 % per passo resta un fronte aperto, e ora ha un numero.**

### 9.13.5 — Stato

| | |
|---|---|
| `M0`, `M2` (**il decisivo**), `M2b`, `M5a/b/c` | **PASS**, invariati |
| `M1`, `M1b`, `M1c`, `M3`, `M3b` | **PASS** coi criteri corretti |
| `M3c` | **PASS**: `xi freschi 538`, `nati 552`, ultima nidiata `14` non ancora servita -> **`552 - 14 = 538`, COINCIDONO ESATTAMENTE**. Lo sfasamento di un giro e' **parte del criterio**, non una tolleranza |
| **SIGILLO CORREZIONI** | **16/16 PASS** |
| metriche §3 nell'osservatore (`L_tot`, `r` per eta', corr `xi`, fattore `cs`) | **da fare** |
| campagna `{OFF, ON} x >= 2 semi` sul sistema corretto | **da rifare** |
| `N2` del taglio spettrale | **da rigirare** sul nuovo riferimento |


---

## 9.14 — LA BASELINE CORRETTA, LA SCOMPOSIZIONE DI `L_tot`, E L'INVENTARIO DEI SIGILLI

*(Tre riscontri che erano rimasti fuori da questa relazione. Li scrivo qui perche' chi legge solo
questa dev'essere allineato — §5-ter — e perche' il terzo cambia il piano di lavoro.)*

### 9.14.1 — `L_tot` cresce: **e' l'INERZIA, non `omega`**

Predizione scritta e committata **prima** del calcolo (`doc/PREDIZIONE_scomposizione_L.md`, `5fe79cd`),
**confermata**. Scomposizione `d log(L/n) = d log(I) + d log(|omega|) + misto` sui 4 run di baseline,
dal passo 50 al 500:

| run | `d log(L/n)` | **A = `d log(Lam)`** | **B = `d log RMS(omega)`** | **peso di A** |
|---|---|---|---|---|
| OFF s1 | +4.703 | **+6.032** | +0.702 | **89.6 %** |
| OFF s2 | +4.833 | **+7.253** | +0.549 | **93.0 %** |
| ON s1 | +1.859 | **+5.931** | +0.142 | **97.7 %** |
| ON s2 | +2.308 | **+7.301** | **-0.019** | **99.7 %** |

In fattori su 450 passi: `Lam` **x376-1481**, `RMS(omega)` **x0.98-2.02**. **Nel braccio ON `omega`
e' piatto o in leggero CALO mentre l'inerzia cresce di tre ordini.**

> **`L_tot` non e' una violazione di conservazione: e' un campo che si sta accendendo.** La domanda
> *«si conserva?»* **e' mal posta prima del regime** — a 500 passi il sistema ha vissuto **un decimo**
> della propria maturazione (`ramp = min(1, eta/TAU_A)`, pieno a ~5000 passi).

**Prova indipendente:** l'inerzia **mediana** lascia il pavimento `1e-6` solo al passo **250-350**.
Per meta' run il nodo **tipico** ha avuto un'inerzia che **non e' una massa, e' una regolarizzazione**.

**E un fatto NON previsto:** `L_tot/n` cresce **x6.4-126** mentre il prodotto delle **mediane** non
si avvicina -> **la crescita sta nella CODA, non nel nodo tipico**. Non e' spiegato.
*(Due errori miei, dichiarati nel referto: la prima scomposizione usava le **mediane** contro una
**media** e non chiudeva; e un `glob` di pulizia ha toccato i file-riferimento dei sigilli, ripristinati
e verificati blob per blob.)*

### 9.14.2 — FASE A: **14 flag su 16 non hanno NESSUN sigillo**

Inventario per lettura del codice (`doc/REFERTO_faseA_sigilli.md`). **Tutti e 28 i nomi di flag
esistono** nell'argv. Ma: **Tier 2 e Tier 3 sono a zero su dieci**; `RUMORE_COLORATO` ha `N2` FAIL;
`TAU_LUCE` ha il sigillo **fallito**. **Passa solo `STEP2_OROLOGIO`.**

**E due flag che sarebbero stati MUTI, e nessuno dei due lo dichiara:**
- **`VERSO_CHI` e' MORTO sotto `CHI_CORE`** (`:2881` arriva prima di `:2884`, e `--chi-core` e' in
  **ogni** run): accenderlo sarebbe stato un **no-op silenzioso**. **Esce dalla lista.**
- **`LS_AZIM`, `OLON_PART` e `ZETA_VIR` vivono dentro `if VIRIALE:`** e non lo dicono. `ZETA_VIR` ha
  un **secondo** punto d'uso dentro `if VERLET:`, quindi e' **parzialmente** condizionato — peggio che
  esserlo del tutto, perche' **meta' dell'effetto sparirebbe in silenzio**.

> **L'assenza di sigilli sta FORZANDO la metodologia migliore**, non impedendo il lavoro: con ~15
> leggi accese insieme, nessun cambiamento sarebbe attribuibile a una sola.

---

## 9.15 — LA PRIMA PROMOZIONE (`STEP2_OROLOGIO`), E UN FALSO PASS INTERCETTATO PRIMA CHE ACCADESSE

### 9.15.1 — Lo Step 2 e' **fisica di default** dal 2026-09-16

E' la **prima** voce mai scritta nella sezione A di `doc/COMPONENTI_PROMOSSE.md`. I tre criteri §10,
col riscontro di ciascuno:

1. **DERIVATA:** orologio di Compton `omega = m c^2/hbar` con `c -> cs`, quindi `omega` va come
   `cs^2` ed e' **l'unica forma possibile**. Zero parametri. **E lo stesso esponente `cs^2` e'
   derivato per una strada INDIPENDENTE** nell'inerzia (`inerzia` come `cs^-2`):
   **consistenza trovata, non costruita.**
2. **SIGILLATA con controllo positivo:** `S3.0` dimostra che il test **VEDE** (39/40 nodi,
   `|f(1)-f(0)|` mediana **1.279e-03**), senza il quale un sigillo passerebbe **anche su codice morto**.
3. **ASSENZA = DIFETTO** (Luca): *«un sistema in cui l'EM non risponde alla metrica e' un sistema
   SBAGLIATO, non diverso»*. La fase U(1) **evolveva gia'**; mancava che **rispondesse alla curvatura**.
   **E non e' promossa per inerzia:** fino a ieri era OFF e **non e' mai stata accesa in una misura
   committata**.

**Criterio di RETROCESSIONE, scritto al momento della promozione:** torna a flag se un riscontro
committato mostra che `_phc` **non e' una fase globale** — cioe' se una firma di **SPIN** si muovesse
per lo Step 2 **oltre la dispersione fra semi** (0.03, mai la `SE` interna). Oggi `_phc` moltiplica
`a1` e `b1` per lo **stesso** fattore (`:2212-2213`, uniche occorrenze) e il Bloch e' invariante a **3.3e-16**.

### 9.15.2 — IL PEZZO CHE CONTA PIU' DELLA PROMOZIONE

**Ribaltare un default converte ogni braccio di controllo ottenuto per OMISSIONE del flag in un
duplicato del braccio di prova.** `_sigillo_step2.py` prendeva il suo braccio OFF **cosi'**:

> senza l'adeguamento, **`S2` avrebbe confrontato ON contro ON e sarebbe PASSATO SEMPRE** — un falso
> PASS della classe gia' catalogata (*«`0.000e+00` puo' significare "nessun confronto"»*), **ma con le
> shape UGUALI**, quindi **invisibile anche alla guardia delle shape**.

Adeguati nello stesso commit il sigillo (`--senza-step2-orologio`) e l'osservatore (`--senza-step2`).
**Regola nuova in §9: quando si ribalta un default, si cercano NELLO STESSO COMMIT tutti i punti che
ottenevano il vecchio comportamento per omissione.**

**Risigillo eseguito dopo la promozione, col braccio OFF vero: 9/10 PASS + 1 FAIL ATTESO.**
`S2` da' `0.000e+00` con **nodi 2924 = 2924, shape divergenti 0** — cioe' **il confronto esiste**, ed
e' identico a prima: senza `--cs-dinamico` il fattore e' **1 esatto**, quindi **la riduzione al limite
regge anche col braccio OFF vero**. *(`S1` fallisce contro un blob di quattro cambiamenti fa: 3164
contro 2924 nodi = mancanza di confronto. Si cita «9/10 + 1 FAIL ATTESO», MAI «10/10».)*

---

## 9.16 — `TW_SPINORE`: **la legge CODIFICATA non e' quella DICHIARATA** — segnalo, non eseguo

Il mandato diceva *«`TW_SPINORE` sigillato e poi acceso»*. **Non l'ho acceso e non ho scritto il
sigillo** (P1). Misura trasversale, 209 852 archi, run ON, 150 passi, seme 1, `--cs-dinamico` acceso:

| | grandezza | valore |
|---|---|---|
| **(a)** | **DICHIARATO** dal commento: angolo/passo `= tw/2` | **9.827e-01 rad** |
| **(b)** | **CODIFICATO** (`:2149`): `tw/(4pi)` sommato a `omega_new` | **1.564e-01** |
| **(c)** | l'angolo che (b) produce davvero `= (b)*dt_n` | **1.564e-03 rad** |
| | **(a)/(c) `= 2pi/DT`** | **628.3** |

`omega` **e' una velocita' angolare** (`theta = |omega|*dt`, `:2210` e `:2296`): il commento descrive
un **angolo**. **Sono due leggi diverse, e quella che gira e' (c).**

**E finisce nella MEMORIA** (`self.omega_s`, `:2313`), dove all'equilibrio vale `tw/(4pi)*tau/dt_n`
= **3.910e+01** (a `tau/dt_n = 250`) contro una mediana di `|omega_s|` di **7.239e+04**.
**Il commento di `SYNC_SPINORE` (`:724`) dice, dello stesso blocco, che un torque messo in `omega_s`
«darebbe accumulo/divergenza».** E, **unico del blocco**, `_otw` **non e' diviso per l'inerzia**.

> **QUELLO CHE NON DICO:** che sia **trascurabile**. Lo **0.054 %** e' un'**AMPIEZZA**, e la domanda
> e' **DIREZIONALE** — l'asse TW e' **fisso e persistente**, `omega` e' un **random walk**. E' lo stesso
> errore ampiezza-contro-correlazione che ho gia' fatto sul `cs` allo 0.023 %: **non lo rifaccio al
> contrario.** *(Ed e' proprio la ragione per cui Luca lo aveva scelto per primo.)*

**Controllo positivo, ed e' DEBOLE:** ON/OFF divergono (**2849 -> 3047** nodi, +6.9 %) **ma con shape
diverse** -> dice *«che cambia»*, non *«di quanto»*.

**Perche' non ho scritto il sigillo:** il suo criterio naturale (*«ruota il Bloch di `tw/2`»*)
fallirebbe di **628** — non per un difetto del codice, ma perche' **verrebbe dalla DESCRIZIONE
invece che dal codice**. Sarebbe il **quarto** criterio stale in due giorni. **Un sigillo scritto
sulla descrizione di una legge che il codice non implementa e' un modo elaborato di certificare un
malinteso.**

### ✅ DECISIONE DI LUCA (2026-09-16): **resta spento** — strada 3 di tre

Le altre due erano **correggere il cablaggio** (che per il §10 ne farebbe una **correzione di
difetto**, quindi **senza flag**) e **sigillare cio' che fa davvero**, riscrivendo il commento.

**Il fronte `W` NON si chiude:** resta aperto come **difetto di cablaggio**, e il suo criterio di
chiusura e' **una decisione di fisica** su quale delle due leggi sia quella voluta — **non una misura
in piu'**. **Il commento nel codice resta falso**, e il rischio vero non e' dimenticare la componente:
e' **riaccenderla credendo di aggiungere `tw/2`**. Per questo il fatto sta in **`CLAUDE.md` §9**, che
si legge a ogni sessione, e non solo nel referto.

**E `soliton_simulator.py` non e' stato toccato nemmeno per annotarlo:** due run video stavano girando
su quel blob, e cambiarlo avrebbe rotto la corrispondenza fra il file sul disco e quello che ha
prodotto gli output (§5-quinquies). -> `doc/REFERTO_tw_spinore.md`, voce **W** del registro.


---

## 9.17 — AUDIT DI LETTURA DELLE LEGGI: **si misura per PROMUOVERE, si dimostra per ESCLUDERE**

> **2026-09-16, blob `a44adc31`. Nessun run, nessuna modifica alla fisica, nessuna accensione.**
> Mandato di Luca: *«quali leggi hanno senso fisico, quali no, quali vanno integrate meglio»*.
> Registrato in `doc/COMPONENTI_PROMOSSE.md` **sezione E** (nuova), `doc/RAMIFICAZIONI.md` (**X1**,
> **X2**, **X3**) e `CLAUDE.md` §9.

### 9.17.1 — La regola, che e' il vero risultato

> **Una MISURA dice *«questa legge produce un effetto»*. NON dice se ha senso.**
> `SPIN_LARMOR` **produceva** un effetto ed era **sbagliata**. Il fattore `cs^-2` non ne produce
> quasi, ed e' **necessario**. **Le due cose non coincidono.**

**Conseguenza operativa, ed e' vincolante:** escludere una legge perche' *«non produce effetto»*
**non e' un argomento**. Si deve dire **QUALE PROPRIETA' ROMPE** — antisimmetria su arco orientato,
localita' (§4), zero-manopole (§3), un'identita' misurata — **citandone il punto nel codice**.
**E per questo un'esclusione per dimostrazione NON si riapre con una misura:** torna in gioco solo
se cade la dimostrazione.

### 9.17.2 — Le nove escluse, con la proprieta' che rompono

| flag | proprieta' rotta | riga |
|---|---|---|
| `SPIN_LARMOR` | l'asse `cross(nb_i, nb_j)` **si annulla all'allineamento**: nullo per costruzione **proprio dove servirebbe** | `:2065` |
| `TW_SPINORE` | implementazione != legge dichiarata (**628.3 = 2π/DT**), e finisce nella **memoria** contro un divieto scritto nello stesso blocco | `:2149-2154`, `:2313` |
| `POLO_MATURO` | `np.where(_twn[i] >= _twn[j], chi[i], chi[j])` e' **SIMMETRICO** dove serve **ANTIsimmetrico** (`tw` vive su arco **orientato**, e `dph` e' antisimmetrico). Il commento ammette: *«rompe il bilanciamento»* | `:3032` contro `:3034` |
| `VERSO_CHI` | **no-op silenzioso** sotto `--chi-core`, che c'e' sempre | `:2881`/`:2884` |
| `L_CONSERVA` | **azzera tutta** la rotazione rigida: distrugge la precessione **misurata** (`L_z ~ -0.9`, 84 % coerente) | `:549-553` |
| `SYNC_SPINORE` | allineamento **imposto** (Kuramoto), non derivato — e su una **media di vicinato** | `:2161-2163` |
| `ANTIFASE_ADD`, `COPPIA_DENSITA` | **il codice stesso** le marca *«esplorativa»* / *«ESPLORATIVO»* | `:554`, `:557` |
| `TEMPO_SEGNO` | **NO-GO gia' registrato** | `:2829-2833` |
| `GAMMA_TURBO` | non e' una legge: **amplificatore diagnostico** (§10-C) | — |

### 9.17.3 — ⚠ DUE VOCI DELLA TABELLA PROPOSTA NON REGGEVANO

**(a) `SYNC_UPDATE` — la motivazione era FALSA.** Si diceva *«accende lo scuotimento»*. Il codice
dice il contrario: `:1980 if SCUOTIMENTO and not SYNC_UPDATE` lo **disattiva**, e `:2279`/`:2302`
`if SYNC_UPDATE and SCUOTIMENTO` lo **riapplicano altrove**. **Non accende: SPOSTA.** E non sono
«due variabili in un flag»: tutti i suoi effetti sono **una sola scelta coerente** — *ogni legge
legge lo stato a `t-1`* — cioe' **Gauss-Seidel -> Jacobi**.
> **RICLASSIFICATO: non e' una legge, e' uno SCHEMA DI INTEGRAZIONE**, stessa categoria di `VERLET`.
> Non rompe una proprieta' fisica, e **non appartiene alle escluse**.

**(b) `LS_AZIM` — l'obiezione era imprecisa, ma la voce resta esclusa per una ragione piu' forte.**
Verificato: i centri delle masse stanno su un **cerchio nel piano `z = 0`** (`:5666-5668`), quindi
`z` **e'** la normale geometrica della configurazione iniziale — **non** un asse arbitrario.
**Ma:**
1. **usa il BARICENTRO GLOBALE**, `_cen = self.pos[:self.n].mean(0)` (`:3773`) — precisamente cio'
   che §4 vieta. **E nello stesso metodo ci sono QUATTRO annotazioni** *«LOCALE PURA: rimossa la
   sottrazione di …»* (`:3721`, `:3747`, `:3783`, `:3799`): **quattro medie globali sono gia' state
   tolte da li' per questa ragione**, e `LS_AZIM` ne reintroduce una quinta per un'altra via;
2. **l'asse e' CABLATO, non DERIVATO**: `np.cross(_rhat, _spin)[:, 2]` (`:3777`) prende l'indice
   **2** e basta — anche dove `z` e' giusto, **il codice non lo calcola: lo assume**. §3 vale anche
   per un **indice** scelto.

### 9.17.4 — I due fronti aperti che ne escono (non escluse, a rischio preciso)

**`TEMPO_PROPRIO_ORIENTATO` (X1).** Il principio e' **giusto**. Ma con `r < 0` -> `dt_n < 0`, e
**tre consumatori si rompono**: `:2143` il termine dissipativo **amplifica** invece di smorzare;
`:2661` `alpha = 1 - exp(-dt_n/tau)` diventa **negativo** e lo slerp **estrapola via**; `:2834`
`self.eta += dt_n` fa **diminuire l'ETA'**, che pilota `ramp`. **Protetto** solo il rumore OU
(`:1993`, usa `np.abs`); **benigna** l'inversione della rotazione.
> **IL FATTO NUOVO:** `--tempo-segno` mette il segno in **`dt_n_s`**, una variabile **separata**
> (`:2829-2833`), cosi' `eta` resta sul `dt_n` non firmato; `--tempo-proprio-orientato` lo mette
> **dentro `r`**, quindi dentro `dt_n` stesso, e **dilaga**. **Due meccanismi per la stessa idea,
> con architetture opposte.**

**`ZETA_LOC` (X2).** `med_rho = np.median(rho)` (`:3136`) e' **globale** -> lo smorzamento «locale»
dipende da tutto il sistema. E c'e' il difetto piu' insidioso: per il nodo **mediano**
`eccesso = 0` **sempre** -> `zeta_loc = ZETA_M` **per costruzione**. E' **lo stesso punto fisso
auto-normalizzante** gia' registrato per `_tau`/`_dens_rif` (**C12**): **sulla mediana non si
misura nulla.**

### 9.17.5 — Otto confermate sane, e una cosa che vale la pena notare

`PAV_COM` (la legge al posto del numero) · `GUSCIO_MORBIDO` (forma standard + clamp CFL) ·
`ZETA_VIR` (`cos2 + sin2 = 1` **esatto**, e' una decomposizione ortogonale) · `CHI_BASC` (soglia =
`PHI_CRIT`, **non** una mediana) · `PLAST_DIN` (stress saturato) · `VIRIALE` · `OLON_PART` ·
`STEP2_OROLOGIO` (gia' promosso).

> **`VIRIALE` costruisce `circ_nodo` ANTISIMMETRICAMENTE** — `np.add.at(circ_nodo, ii, twn_a)` e
> `np.add.at(circ_nodo, jj, -twn_a)` (`:3755`): **l'opposto esatto del difetto di `POLO_MATURO`**,
> nello stesso blocco. Il codice **sa** fare la cosa giusta: `POLO_MATURO` la disfa apposta.

**Sane come COSTRUZIONE, non sigillate:** nessuna di esse ha un sigillo, restano spente, e la
**FASE A resta valida**.

### 9.17.6 — E il codice delle escluse NON si cancella

Resta spento, ed e' **l'evidenza che spiega perche' esistono i loro sostituti**: `TW_SPINORE` esiste
**perche'** `SPIN_LARMOR` fallisce. **Cancellare il secondo farebbe perdere il perche' del primo.**


---

## 9.18 — VERDETTO SULLO STEP 2: la retrocessione **non scatta**, e meta' dei nulli **non ha potenza**

> **2026-09-16, blob `a44adc31`.** 8 run, 500 passi, **4 semi appaiati** per braccio,
> `--cs-dinamico` acceso, `--tau-luce` e `--tw-spinore` esclusi. **8/8 `rc=0` in 53.8 minuti.**
> Predizione e soglia **committate prima** (`doc/PREDIZIONE_step2_U1.md`, `b7cb537`).
> -> `doc/REFERTO_step2_U1.md`.

### 9.18.1 — Il criterio di retrocessione **non scatta**

| | |
|---|---|
| firme di **SPIN** che escludono lo zero | **0 su 11** |
| osservabili **U(1)** che escludono lo zero | **0 su 5** |

`chi` medio `Delta = -0.035 +- 0.192` gradi · `chi` std `-0.021 +- 0.100` · spin overlap
`+2.5e-04 +- 1.6e-03` · `|omega_s|` `-1730 +- 5218` · coerenza di segno `+1.6e-03 +- 5.9e-03`.

> **La promozione REGGE, e per la ragione su cui poggiava:** `_phc` moltiplica `a1` e `b1` per lo
> **stesso** fattore (`:2212-2213`, uniche occorrenze), quindi il Bloch e' invariante per fase
> globale. **Non e' fortuna: e' la proprieta' che il criterio sorvegliava, ed e' stata messa alla
> prova.** Il debito contratto con la promozione (*«le conseguenze su U(1) sono da misurare»*) e'
> **saldato, con esito negativo**.

### 9.18.2 — ⚠ E QUI LA COSA CHE CONTA DAVVERO

**«Contiene lo zero» non vale uguale per tutte le righe.** La risoluzione varia di **tre ordini**:

| | risoluzione | il nullo dice… |
|---|---|---|
| `chi` medio / std, spin overlap | **0.21 – 0.32 %** | **molto** |
| `|omega_s|` | 6.7 % | qualcosa |
| `n`, `Lam` | 11 – 35 % | poco |
| **`|<n>|`** | **129 %** | **NIENTE** |
| **coerenza di segno** | **603 %** | **NIENTE** |

> **Ventidue righe tutte «contiene lo zero», e non significano la stessa cosa.** E' la versione
> **statistica** del `max|A-B| = 0.000e+00` per **mancanza di confronto**: uno zero letto come
> informazione mentre e' **assenza** di informazione.
>
> **Forma onesta, cioe' LIMITI SUPERIORI:** lo Step 2 **non sposta `chi` di piu' di 0.19 gradi**, ne'
> lo spin overlap di piu' di **0.0016**, ne' `|omega_s|` di piu' del **6.7 %**. **Su `|<n>|` e sulla
> coerenza di segno non si sa nulla.**
>
> **E la cura non e' piu' passi:** dove la grandezza **vale gia' il suo nullo**, la barra percentuale
> **non puo'** essere piccola. Li' servono **piu' SEMI**. -> presidio nuovo in `CLAUDE.md` §9.

### 9.18.3 — Un controllo che vale, e una lacuna strutturale

**Il controllo:** `fatt_cs`, `cs_std` e la frazione oltre l'1 % **non** differiscono fra i bracci —
ed e' **giusto**, perche' `fatt_cs` e' il fattore dell'**inerzia**, una **correzione di difetto**,
**non** gated su `STEP2`. **I due bracci sono identici in tutto tranne l'orologio.**

> **LA LACUNA (voce `Y1`):** fra le **256** colonne dell'osservatore **nessuna** misura l'orologio —
> niente `clk`, `orolog`, `fase`, `phc`. Si misurano le **conseguenze** di `omega_clk`, **mai
> `omega_clk`**. Quindi il nullo su U(1) **non dice** *«l'orologio non e' cambiato»*: dice *«cio' che
> sappiamo misurare non se ne accorge»*. **Ed e' cambiato:** il **10.8 %** dei nodi ha
> `|fatt_cs - 1| > 1 %`.

### 9.18.4 — E due nulli da correggere (voce `Y2`)

`u1_segno_ov_nullo` scrive **`2/pi`** nei CSV ed e' **sbagliato** — `canon` viene da `_nb_grav()`,
una direzione diversa, quindi il nullo e' **`(2/3)*(2/pi) = 0.42441`**. Col nullo giusto il misurato
**0.4254 ± 0.0105** e' **il caso**. **Il valore sbagliato e' nei dati gia' scritti** e non lo
acquisiranno: va **annotato**. E `u1_verso_arco_coer` **resta muta** finche' il suo nullo non e'
misurato contro **coppie casuali** (`nb_grav` e' una media di vicinato: i nodi adiacenti sono
correlati **per costruzione**).

---

## 9.19 — LA BONIFICA: **sei correzioni, quattro cablate, `U7b` risolto** — e **quattro numeri corretti, tre dei quali miei**

**Che cos'era.** Un mandato di **bonifica, non di ricerca**: sei correzioni strutturali, **nessun
run di misura**, **nessuna predizione numerica**. Il giro precedente si era **fermato** perché il
sigillo bloccante `U7b` falliva (`dt_e/tau_p` massimo **34629** → divergenza su ~0.11 % degli
archi). Questo giro lo risolve.

**Il termine di paragone è ora sul disco.** `doc/ASSIOMI.md` **non esisteva**, e il mandato ordinava
che ogni correzione dichiarasse quale assioma soddisfa. Ora esiste (commit `804522b`), e **si
dichiara BOZZA**: non generativo, non indipendente, con una **violazione ammessa** (`Lam = mean(I)`
è globale e A2 lo vieta, ma è una correzione che ha funzionato). Le sue citazioni di codice sono
state **verificate dal disco**, non accettate: `Legge I` è davvero a `:265`.

### Cosa è stato cablato, e con quale sigillo

| correzione | assiomi | sigillo |
|---|---|---|
| **`d_arco = self.d`** — era un array **per-arco indicizzato con indici di nodo** | A3 (popolazione) | **V1 8/8** |
| **`tau_p = max(t_luce, t_visco)`** — plasticità viscoelastica causale | A1, A2, A3, A4, A5 | **V2-V5 8/8** |
| **`spinta = 0.02·d0·_rep`** — era `0.02·median(d0)·rep` | A2, A3 *(non A1)* | **V6 2/2** |
| **`_rep` con memoria** su `tau_pp` — era istantaneo | A5 liv.1, A7 | **V7-V8 6/6** |
| **`spin_locale()` rimossa** — codice morto | — | **V9 4/4**, byte-identico |

**Il numero che conta: `dt_e/tau_p` da 34629 a 0.456** (**0.400** sul codice vivo). **`U7b` è
risolto** — e non con un clamp. `tau_p >= d/cs` **non è un numero scelto**: sotto quel valore la
forma di riposo si adatterebbe **più in fretta di quanto un segnale attraversi l'arco**. È l'unico
valore possibile, perché oltre c'è una violazione di A5. **È la distinzione che A1 impone: «questo
valore si può spostare?»** Il pavimento `1e-6` sull'inerzia sì (perché `1e-6` e non `1e-7`? nessuna
ragione). Questo no.

**E la plasticità era CONGELATA, non «spenta a metà»:** `tau_p` mediano passa da **6.85e+05** a
**2.376**, cioè **288 000 volte** più corto. Il difetto era triplo in una riga sola: `ELAST_C = 100`
è un numero scelto (A1), `median(I_nodi)` è globale (A2), e — il peggiore — `rho_arco` vive sugli
**archi** mentre `median(I_nodi)` vive sui **nodi** (A3): su coda pesante l'arco tipico sta **8830
volte sopra** la mediana nodale.

### QUATTRO NUMERI CORRETTI DOPO L'ESECUZIONE, e **tre erano miei**

Questo è il contenuto che vale di più, e va letto per primo.

1. **Il `−0.349` di `d_arco` era MIO ed era UN SEME.** L'avevo scritto in `doc/REFERTO_U7_fallito.md`
   come *«ANTICORRELATA»*, cioè come **il** fatto. Su quattro semi: **−0.3488 / +0.1444 / +0.0319 /
   +0.3760**. **Il segno non è concorde.** Il vecchio `d_arco` non era anticorrelato: era
   **scorrelato**. *(La diagnosi ne esce **più forte** — un'anticorrelazione stabile sarebbe comunque
   informazione col segno sbagliato, questo è **rumore** — ma il numero non reggeva, ed è **P3**.)*
2. **Il `+1.000 esatto` del criterio non regge attraverso `np.corrcoef`:** su un seme dà
   `0.99999999999999978`. Non è un difetto della cura: è arrotondamento di un **calcolo**, e sotto
   c'è un'**identità** (`d_arco` *è* `self.d`), esatta su 4/4 con `np.array_equal`. **Si testa
   l'identità, non la sua immagine numerica.**
3. **Il `19x` di V5b era un mio errore di AGGREGAZIONE:** facevo la media delle **mediane per seme**
   invece della mediana della popolazione unita. Sulla popolazione unita: **4089x**, il referto
   reggeva. **Ma aggregando si sarebbe perso un fatto:** il rapporto vale **8161 / 3 / 9384 /
   23754**. **Su un seme su quattro gli archi sotto 1 non sono affatto il vuoto profondo.**
   «Il vincolo scatta nel vuoto» è vero su **3 semi su 4**, non è una proprietà della forma.
4. **E uno che corregge CLAUDE.md §9: `_tau` NON ha il punto fisso che quella voce gli attribuiva.**
   La voce diceva *«per il nodo mediano `dens/dens_rif ~ 1` **sempre** … punto fisso
   auto-normalizzante»*. **Misurato: 0.3698 / 0.0629 / 0.8024 / 0.7475** — fattore **13** fra semi.
   **Perché:** `_dens_rif = median(_dens[_dens > 1e-6])` è la mediana di un **sottoinsieme** (il
   78-88 %), quindi numeratore e denominatore vivono su popolazioni **diverse** — la condizione che
   C12 richiede e che qui **manca**. **Controprova:** togliendo il filtro il rapporto vale
   **`1.000000` esatto su 4 semi su 4**. **Il filtro è l'unica cosa che separa i due casi.**
   *(Lezione: la voce **citava** il filtro e **concludeva comunque** per il punto fisso. L'argomento
   era stato scritto guardando la **forma ricordata** `x/median(x)`, non l'espressione che gira.)*

### Un contatore cablato apposta, e cosa ha trovato

`peq` può essere degenere (`<= 1e-30`), e P5 impone di **contare** ogni protezione. Cablato anche il
contatore dell'**intersezione** — *quanti scatti del vincolo causale cadono proprio lì* — invece di
inferirla. Risultato: **0.0000 %** di `peq` degenere nei dati **maturi** (300 passi), **2.50 %** nel
run **giovane** (40 passi), e **il 99.91 %** degli scatti causali del sistema giovane sta **proprio
su quegli archi** (207563 su 207753). **Quindi il `max` ha due regimi:** nel maturo descrive il vuoto
profondo, nel giovane descrive **il punto in cui `peq` non è definito**. Due cose diverse, e si
distinguono **solo contandole**.

### Due correzioni NON cablate, e perché

- **① `inerzia` — il gate che la autorizzava aveva misurato un'altra grandezza.** `_rho_sorgente()`
  **non** restituisce `|psi|²` con `CAMPO_SPINORIALE` ON (e lo è in **tutti** i run del fork):
  restituisce `rho_spin`, il campo **emesso**. Ma `peq` insegue `|psi|²`. **Correlazione 0.80**,
  rapporto da **0.005** a **8.8** fra p05 e p95, **massimo 7684**. GATE A aveva misurato
  `|psi|²/peq_nodo`. **E togliendo il pavimento senza metterne uno derivato l'inerzia non "può"
  annullarsi: si annulla** — `min = 0` esatto su 6 nodi. Le due strade (allineare le popolazioni, o
  costruire un `peq_spin` che non esiste) sono **un cambio di modello** e **una legge nuova**:
  entrambe eccedono una bonifica.
- **⑥ `_floor_d0`** — i due rami violano assiomi **diversi** (`0.05` viola A1; `f·median(d0)` viola
  A2 e A3), quindi **nessuno si salva aggiustando l'altro**, e sostituirli entrambi renderebbe
  `PAV_COM` **inerte**. Tre decisioni aperte in `doc/PROPOSTA_floor_d0.md`.

### Una domanda aperta degli assiomi, **risolta**

`doc/ASSIOMI.md` chiedeva se **A3 sia un caso particolare di A2**. Il codice ha un controesempio:
**`u_nodo = I / media_dei_vicini`** (`:2607`) **soddisfa A2** (nessuna scorciatoia globale: la media
è sui vicini topologici) e **viola A3** (che nomina esplicitamente «media dei primi vicini»).
**Quindi A3 è indipendente.** Ma `u_nodo` **non va corretto**: sta dentro `_cs_nodo`, cioè dentro
ciò che **definisce** la causalità, e A4 giudica quel livello a parte.

### Il debito che questa bonifica contrae

**Non è stato misurato quale fisica esca da una plasticità 288 000 volte più veloce.** Serve una
campagna, e questo giro non la prevedeva. È registrato in `doc/COMPONENTI_PROMOSSE.md` §F.5 perché
non si perda — come quello dello Step 2, che è poi stato saldato (§9.18).

**E `--elast-c` è ora un NO-OP dichiarato che stampa un avviso.** `ELAST_C` **non è stato
cancellato**: resta marcato come inutilizzato, perché è l'evidenza che spiega perché esiste il suo
sostituto (§9). Stessa cosa per la dottrina di `spin_locale`, trascritta in §F.4 prima di rimuovere
il metodo.

---

## 9.20 — `peq` ALLA NASCITA: **la verifica preliminare ferma il cablaggio**, e il reperto si rilegge al contrario

**Che cos'era.** Un mandato di bonifica su `peq`: il contatore cablato in `f405327` diceva che il
vincolo causale scatta **99.91 %** delle volte su archi dove `peq` è degenere, e quindi — questa la
lettura proposta — **non sta proteggendo il vuoto profondo, sta mascherando un `peq` non definito**.
La cura proposta: inizializzare `peq` dai due nodi dell'arco invece che a `NaN`.

Il mandato imponeva una **verifica preliminare prima del cablaggio**. **L'ha fermato.**

### 1. `psi` è raggiungibile, ma è **identicamente zero**

```
DOPO la costruzione della scena:  len(psi) = 120 = n
  psi tutti zero?  True       max|psi| = 0

IL VALORE CHE LA CURA SCRIVEREBBE  ->  0.5*(I[a]+I[b]) :
  min 0    mediana 0    max 0
  degeneri lo stesso:  4555 su 4555   (100.00 %)
```

`psi` nasce `np.zeros(0, complex)` ed è popolato **solo dentro `step()`**. Quando gli archi nascono,
**la densità non esiste come grandezza fisica**. La cura scriverebbe **`0` al posto di `NaN`**, e
`0 <= 1e-30`: **il contatore resterebbe identico e il sigillo decisivo fallirebbe per costruzione.**
Non è un dettaglio implementativo — **la cura sarebbe inerte rispetto al problema che dichiara di
risolvere.** E uno snapshot non aiuta: non esiste un istante precedente da fotografare.

### 2. Il reperto va riletto: **non è una finestra permanente, sono DUE PASSI**

Ho cablato un secondo contatore per **deciderlo invece di argomentarlo** — quanti **passi distinti**
hanno almeno un `peq` degenere:

```
RUN REALE, 60 passi:
  _taup_peq_degenere  (archi-passo cumulativi) :  207520
  _taup_peq_deg_passi (PASSI DISTINTI)         :       2
```

**Due passi su sessanta.** I 207520 archi-passo sono **~103 760 archi × 2 passi**: il **transitorio
di accensione** moltiplicato per il numero di archi. **Un contatore cumulativo, da solo, non
distingue «difetto sempre presente» da «transitorio moltiplicato»** — e senza il secondo si sceglie
la diagnosi che si ha già in mente. *(È lo stesso presidio del valore sotto ipotesi nulla, applicato
a un conteggio: «quanto varrebbe questo numero se il fenomeno fosse innocuo?».)*

La sequenza misurata: costruzione → `NaN` al **100 %**; passo 1 → `psi` **ancora zero**, quindi
`peq = rho = 0` **esatto**; passo 2 → **zero degeneri**; poi sempre zero. Coerente col già misurato:
**0 %** nei dati maturi, **2.49 %** nel run giovane — che erano **2/60 passi** diluiti nel cumulativo.

### 3. Il ribaltamento: **il `NaN` non è il difetto, è l'unica cosa onesta**

Il mandato lo marca come *«IL PROBLEMA»*: *«`NaN` dice "non lo so" — ma si sa»*. **Alla costruzione
della scena non si sa**: i nodi esistono come **posizioni**, ma la loro densità è **zero per
costruzione**. Il `NaN` non nasconde un valore noto: dice, correttamente, che la grandezza **non è
ancora definita**, e la delega alla calibrazione è il meccanismo che la definisce appena esiste.

**Il difetto, se c'è, è a valle e di altra natura:** al passo 1 **l'intero campo** è zero, non solo
`peq`. Il vincolo causale che scatta lì **non maschera un difetto numerico: attraversa un sistema
che non è ancora partito.**

**Questo non assolve tutto.** `pmed = median(self.peq)` nello Schwinger **viola A2** ed è un difetto
vero, **indipendente dal transitorio**: lì il sistema è avviato e i due nodi dell'arco hanno una
densità vera. **È cablabile** — ma il mandato la lega al sigillo che non può passare, e cablarla da
sola significherebbe presentare quel fallimento come se fosse il suo verdetto.

### 4. Cosa ne è degli assiomi

Il corollario **A7b** — *«uno stato non nasce indefinito»* — è stato aggiunto, **col suo limite
misurato accanto**: si applica **dopo** aver verificato che nel punto di nascita esista qualcosa da
cui costruire. **Sostituire un indefinito con uno zero non è inizializzare: è nascondere.**

E la domanda aperta **#2** degli assiomi è **risolta**: `u_nodo` soddisfa A2 e viola A3, quindi
**A3 è indipendente da A2**.

### 5. La speculazione registrata

`doc/SPECULAZIONI_cs_acromatico.md` — linea di Luca, **commit dedicato, nessun codice**, e in
`RAMIFICAZIONI.md` sta in **D.5**, la sezione delle voci **senza criterio di chiusura**, non fra i
fronti. Ne ho verificate le affermazioni controllabili: *«il modello non ha espansione metrica»* è
**vero** (`:3242`, nessun termine `∝ d`); *`cs_std/cs = 11 %`* è **committato** (`ef44b03`,
`11.123 %`). **Il rinvio al «conto sul punto fisso dello scuotimento» (`I/Lam ~ 1/3`) NON l'ho
trovato nel repo**: `doc/INDAGINE_scuotimento.md` esiste ma non contiene quel calcolo. Testo lasciato
verbatim come ordinato, **con il rinvio mancante dichiarato**.

---

## 9.21 — ①: **la diagnosi dimensionale è confermata e vale 10⁶**, ma il transitorio blocca il cablaggio — e **due mie obiezioni si correggono**

**Che cos'era.** Il mandato attacca l'unica correzione che tocca `sigma`, cioè la **sorgente** di
`omega`: `inerzia = (rho_sorgente / peq_nodo) · (d/cs)²`. Tesi: `|psi|²` grezzo **non è un `T²`**, è
una densità non normalizzata usata al posto di un tempo al quadrato, e il fattore `cs⁻²` già cablato
**non arriva a destinazione** perché il pavimento `1e-6` lo mangia.

### 1. La tesi è misurata, ed è **più severa** di come è scritta

| passo | mediana `_fatt_cs` | max `_fatt_cs` | **al pavimento** | mediana `inerzia` | mediana `T²` |
|---|---|---|---|---|---|
| 2 | 1.126 | 1.168 | **100.00 %** | **1e-06** | 0.75 |
| 12 | 1.535 | **6.430** | **100.00 %** | **1e-06** | 1.03 |
| 24 | 1.588 | 5.585 | **100.00 %** | **1e-06** | 1.08 |

**Il mandato dice 99.7 %. La misura dice 100.00 %, a ogni passo.** `inerzia` non è «quasi sempre al
pavimento»: **è il pavimento** — la costante `1e-6`. `_fatt_cs` sale fino a **6.43** e **non serve a
nulla**. E `T²/inerzia = 1.03e+06`: **un fattore un milione** fra ciò che l'inerzia è e ciò che, per
dimensione, dovrebbe essere. **Questo risultato non dipende dal cablaggio, ed è il valore del giro.**

### 2. Ma la verifica preliminare ② — che il mandato marca come bloccante — **fallisce**

`_passo_spinoriale` (`:3062`) gira **prima** della calibrazione di `peq` (`:3147`):

```
passo   peq NaN        peq <= 0        peq_nodo <= 0
  0     14134 (100%)        0            360 / 360     <- TUTTI
  1          0        14134 (100%)       360 / 360     <- TUTTI
  2+         0             0                  0        <- pulito
```

**Non sono «i nuovi archi»: sono tutti, per due passi.** `rho/peq_nodo` sarebbe `0/0` = **NaN**, e
`inerzia` entra in **`omega_s`, la memoria persistente**: un NaN lì non è un valore sbagliato per due
passi, **contamina il run per sempre**. **E il pavimento non protegge:** `np.maximum(NaN, 1e-6)` è
**NaN**. Oggi il transitorio è salvato solo perché `rho·_fatt_cs` vale `0` e `max(0, 1e-6) = 1e-6`.

### 3. **Due mie obiezioni del giro precedente vanno corrette**

Nel referto di Z1 avevo dato due ragioni per non cablare ①. **Contro questo mandato, una cade e
l'altra va rinominata:**

1. **CADE.** Avevo scritto che togliendo il pavimento l'inerzia **si annulla** (`min = 0` su 6 nodi).
   **Questo mandato non toglie il pavimento** — lo dichiara e ne dà la ragione giusta (`omega =
   coppia/inerzia`: inerzia minore = omega **maggiore**; il pavimento è **il tappo, non il
   colpevole**). L'obiezione era valida contro un'altra proposta, **non contro questa**.
2. **VA RINOMINATA.** Avevo chiamato «errore di **popolazione** (A3)» il fatto che `rho_sorgente` sia
   `rho_spin` mentre `peq` insegue `|psi|²`. **Non è A3:** dopo la proiezione arco→nodo le due
   grandezze vivono **entrambe sui nodi**, e su questo **il mandato ha ragione**. È una questione di
   **coerenza di grandezza**, **più debole** di come l'avevo scritta. *(Correlazione misurata per
   passo: `1.000 / 1.000 / 0.992 / 0.487 / 0.612 / 0.683` — coincidono all'inizio, poi divergono.)*

**Il blocco vero è un terzo, che non avevo visto:** l'ordine di chiamata `:3062` prima di `:3147`.

### 4. Il transitorio è un **blocco strutturale**, non una curiosità

| correzione | fermata da |
|---|---|
| `peq` alla nascita | `psi` è **zero** quando gli archi nascono |
| **① `inerzia`** | `peq_nodo` è **zero su tutti i nodi** ai passi 0-1 |

**Stessa radice:** `psi` non è calcolato prima del primo `step`, quindi nel transitorio **ogni
grandezza derivata è zero**, e ogni correzione che costruisca un **rapporto fra grandezze di stato**
ci inciampa. **Due correzioni ferme dallo stesso muro.** La via che le sblocca entrambe — calcolare
`psi` una volta alla costruzione della scena — **è un cambio del percorso di inizializzazione, non
una bonifica**, e cambia il seme di ogni run esistente.

### 5. Un fatto nuovo: **`_fatt_cs_ultimo` è scritto e mai letto**

Una sola occorrenza nel codice, ed è la scrittura. Il commento dice *«per la metrica (solo lettura a
valle)»*: **a valle non c'è nessuno.** **Quarto caso della stessa famiglia** — `_passo_spinoriale`
(docstring «ORFANO» ma vivo), `VERSO_CHI` (cablato ma muto), `spin_locale` (mai chiamata).
**Lo stato di vita del codice non è leggibile dal codice.** Conseguenza utile: togliere `_fatt_cs`
dall'inerzia — necessario in ①, o si avrebbe `cs⁻⁴` — **non rompe nessun consumatore**.

### 6. Cosa non è stato guardato

`chi`, `|<n>|`, autocorrelazione, **`theta`**, `omega/sqrt(n)`, `L_tot`, MISURA U, `cs_std/cs`:
**non calcolati, non riportati**, come il mandato §5 impone. In particolare `theta` è il numero che
① punta a muovere, e si guarderà **a bonifica finita, contro una predizione scritta prima** — che è
già committata (`doc/PREVISIONI_qualitative.md`, commit `9c9cc43`, **scritta prima di un cablaggio
che poi non è avvenuto**).

---

## 9.22 — A8, l'audit retroattivo, e **① cablata**: il pavimento passa dal 100 % allo 0.35 %

**Tre fasi.** A8 negli assiomi → audit retroattivo delle correzioni già cablate → cablaggio di ①.

### 1. A8: «un ramo silenzioso non è un ramo»

**Ogni fallback su un percorso fisico deve essere contato.** Un ramo che scatta senza segnalarlo
**non produce un errore: produce una fisica diversa, silenziosa, che sembra funzionare** — è così
che `_psi_spin_prec` ha tenuto la FASE 5 inerte nel **95.33 %** delle chiamate senza che un solo
sigillo se ne accorgesse. **A8 si dichiara più debole degli altri**: A1-A5 dicono cosa una legge
*può essere*, A8 dice come va *strumentata*. È metodologico — e **APERTO** ora registra che **due
voci su otto** non sono assiomi nel senso delle altre sei (A6 è un teorema, A8 è metodo).

### 2. L'audit retroattivo: **quattro rami non contati, tutti a zero**

`d_arco` e la plasticità causale erano state cablate **prima** che A8 esistesse. Riesaminate:

| ramo | contatore | scatta |
|---|---|---|
| **`I_nodi → np.ones(n)`** | **aggiunto** | **0.0000 %** |
| `np.maximum(cs_taup, 1e-9)` | **aggiunto** | 0.0000 % |
| `np.maximum(tau_pp, 1e-12)` | **aggiunto** | 0.0000 % |
| `getattr(_dt_e_ultimo, DT)` | **aggiunto** | 0.0000 % |

**Il più pericoloso leggeva zero:** il fallback di `I_nodi` è **densità 1** contro `|psi|² ~ 1e-6` —
**sei ordini di grandezza**, in silenzio. Non scatta mai. **Ma A8 vuole il contatore anche quando
legge zero:** prima di oggi non si sapeva che leggesse zero, si sapeva solo che **non era esploso**.

**E A8b ha trovato il reperto vero:** la **stessa** cache `_cs_nodo_prev`, letta in **due** punti,
cade nel fallback **0 volte su 62** da `_tempo_luce_nodo` e **2 su 66** da `_passo_spinoriale`
(**3.03 %**). È preesistente alla bonifica, ma diventa rilevante proprio ora, perché ① legge `cs`
da lì.

*(I due rami che superano l'1 % — `peq` degenere e il vincolo causale — sono il transitorio già
registrato come Z3/Z6, non difetti nuovi: marcarli sarebbe contarli due volte.)*

### 3. ① cablata — e il blocco si scioglie con **A6**, non con una rete

```
era:  inerzia = max(rho_sorgente * (CS_M/cs)^2, 1e-6)
ora:  inerzia = max((rho_sorgente / peq_nodo) * (d_nodo/cs_nodo)^2, 1e-6)
```

**Il fatto che ha sbloccato tutto è di ordine di esecuzione, e si legge dal disco:** l'inerzia si
calcola a `:3137`, mentre `cs` è scritto a `:3213`, `peq` a `:3222`, `d` a `:3318`. **Tutte le
grandezze lette lì sono già quelle del passo precedente: A6 è soddisfatto per costruzione**, senza
aggiungere nessuno snapshot. Il mandato temeva di doverne aggiungere; l'ordine li forniva già.

**Il numero che conta — Y4, bloccante:**

> **Il pavimento `1e-6` passa dal 100.00 % allo 0.3457 %.**

**Non è stato toccato: è diventato inerte da solo**, ed è esattamente la **firma** che la previsione
scritta prima chiedeva. Prima, `inerzia` **era** la costante `1e-6`, mentre `_fatt_cs` saliva fino a
**6.43** senza servire a nulla (`T²/inerzia = 1.03e+06`).

**Y1 (bloccante): zero NaN in `omega_s`.** E non perché filtrato — **filtrare sarebbe stata la
quarta rete** sopra lo stesso buco, e **diluire non funzionerebbe affatto** perché `NaN` è
**assorbente** (`0.9·x + 0.1·NaN = NaN`): diluire cura un valore *cattivo*, non un valore *assente*.

**Il fallback del primo passo non è una convenzione nuova**, e questo era il punto delicato: il
codice **sostituisce già `peq` con `rho` quando è NaN, in due punti** (`:3544`, `:3657`), e
`rho/rho = 1`. Il neutro **è** il limite di una sostituzione già presente, non un numero scelto.

### 4. Il settimo criterio corretto dopo l'esecuzione — **e stavolta di forma**

Y5 chiedeva *«passi distinti ≤ 3»* e dava FAIL con 4. Il difetto era mio: la previsione scritta
prima dice *«scatta solo nel transitorio e poi mai»*, che è un'affermazione sulla **posizione**, non
sul **conteggio**. **Un fallback che scatta 4 volte all'inizio e uno che scatta 4 volte sparse danno
lo stesso numero e sono diagnosi opposte.** E la soglia `3` l'avevo scelta guardando una **scena
ridotta** invece del run reale.

**Ho misurato la posizione invece di spostare la soglia:** ultima invocazione col fallback = **8 su
66**, poi **58 consecutive pulite**. Il criterio è ora quello che la previsione già conteneva: **il
fallback cessa e non torna.**

### 5. Cosa resta aperto

- **La coerenza di grandezza** (`rho_spin` contro `|psi|²`) **non è risolta**: ① è stata cablata
  **con quella riserva scritta**, non perché sia caduta. Si chiuderebbe con un `peq_spin` che **non
  esiste** — una legge nuova, non una bonifica.
- **Lo 0.3457 % di nodi ancora al pavimento non è caratterizzato** (voce **Z8**).
- **`theta` non è stato guardato**, come il mandato impone. Si guarderà a bonifica finita, contro
  previsioni già committate **prima** del cablaggio.

---

## 9.23 — **`psi = 0` non era mancata inizializzazione: era il RAMP sull'età.** Tre argomenti, due caduti, e un cablaggio autorizzato che sarebbe stato inerte

**Come si è arrivati qui.** Avevo raccomandato di rimandare a dopo la campagna il calcolo di `psi`
alla costruzione della scena. **Il guardiano ha demolito quella raccomandazione, e aveva ragione:**
*«la comparabilità è già rotta»* — quattro blob in un giro, tre correzioni di legge (`d_arco`,
`tau_p` da `6.85e+05` a `2.376`, il pavimento dell'inerzia da 100 % a 0.35 %). **Non esisteva un
regime da preservare.** Ho ritirato la raccomandazione, dato il via libera alla modifica — e poi
**la verifica preliminare l'ha fermata.**

### 1. `psi` era già calcolato

```
nuova_massa()  ->  semina(..., mass_id)  ->  _registra_concorrenza()  ->  calcola_psi()
```

**Misurato:** subito dopo `nuova_massa`, `len(psi) == n` (**è stato calcolato**) ma `max|psi| = 0`.
**Aggiungere una chiamata lì sarebbe stato inerte** — e sarebbe stata la **quinta rete** sopra lo
stesso buco.

### 2. La causa è `ramp`, e lo zero è il valore GIUSTO

```
eta: min 0, max 0        ramp = min(1, eta/TAU_A) = 0        pesi: max 0   ->   psi = 0
CONTROPROVA, forzando eta = TAU_A:                           max|psi| = 8.02
```

`_pesi()` fa `base = exp(-d/lam) · ramp[i] · ramp[j]`. Con `eta = 0` **tutti i pesi sono zero**,
qualunque cosa faccia `calcola_psi`. **Il campo c'è: è il kernel che lo azzera.**

> **Quindi `psi = 0` non è «l'assenza dell'inizializzazione»: è il valore corretto di una legge che
> dice "un nodo appena nato non pesa ancora".** Nascere con `eta = 0` **è giusto**.

### 3. Il fatto nuovo, ed è più grande della domanda che l'ha prodotto

| passo | `ramp` mediano |
|---|---|
| 1 | **0.0002** |
| 60 | **0.0106** |
| 120 | **0.0217** |

`eta` cresce di **~0.009 per passo** (è `eta += dt_n`, il **tempo proprio**) e `TAU_A = 50`:

> **Per `ramp = 1` servono ~5526 passi. I run di questo programma sono 300-500.**
> A 500 passi `ramp` mediano vale **~0.09**, e poiché `base ∝ ramp[i]·ramp[j]`, **il peso d'arco
> tipico è ~1 % di quello maturo.**

**Non è un difetto, ed è importante non chiamarlo così:** `ramp` è una **legge**. **Ma è una
condizione di regime mai dichiarata** — tutte le misure di questo programma sono state prese su un
sistema in cui **il kernel non ha mai finito di accendersi**. **E le conseguenze non sono state
misurate:** dire *«quindi le misure sono sbagliate»* sarebbe l'errore ampiezza-contro-correlazione
già catalogato in §9. **È stabilito il regime, non il suo effetto.** (Voce **Z9**.)

### 4. I tre argomenti che avevano prodotto il via libera

| | esito |
|---|---|
| **① la comparabilità è già rotta** | **REGGE** — ed è quello che ha demolito la mia raccomandazione |
| **② `omega_s` è memoria persistente** | **CADUTO, misurato:** al passo 0 `omega_s` **non cambia di un bit** (campo zero → coppia zero → l'inerzia non conta); al passo 1 la variazione `0.0059` è **dentro l'intervallo di regime** (0.0060-0.0064) |
| **③ `psi = 0` è un'incoerenza (A7b)** | **CADUTO:** è il valore corretto di `ramp = 0` |

**Restava ① a sostenere «prima, non dopo». Ma «prima» era prima di una modifica che non avrebbe
cambiato niente.**

### 5. Cosa ne consegue per gli assiomi

**A7b ha ora il suo caso speculare**, scritto accanto all'enunciato: **uno zero può essere il valore
corretto di una legge, e allora A7b non si applica.** La domanda che distingue i due casi:
***«esiste una legge per cui questo valore è quello giusto?»*** Se sì, non è un indefinito
travestito: è uno stato. **Se no, è un buco.**

### 6. E una nota sul metodo, perché è il punto

Il guardiano ha corretto un mio argomento sbagliato; io ne ho verificati tre suoi e **due sono
caduti**, incluso quello che aveva usato per spingere la decisione. **Nessuno dei due aveva ragione
per intero, e la misura ha deciso entrambe le volte.** La misura su `omega_s` è stata committata
**anche se indebolisce l'argomento di chi l'aveva chiesta** — e sono quelle che servono di più:
impediscono a qualcuno, fra sei mesi, di rifare lo stesso ragionamento.

---

## 9.24 — **`TAU_A` governa DUE leggi**, e la cura proposta ne faceva una terza già bocciata da un sigillo

**Il mandato voleva sostituire `TAU_A = 50` con `LAM/cs`**, il tempo-luce del solitone, per curare
**Z9** (il kernel matura in ~5526 passi, i run sono 300-500). **La verifica preliminare l'ha
fermato — la quarta volta su quattro.**

### 1. La mappa: due tempi, un numero

| riga | uso |
|---|---|
| `:2429` | `ramp = min(1, eta/TAU_A)` — **maturazione del kernel** (il difetto Z9) |
| `:2226`/`:2229` | `_tau = TAU_A · max(dens/dens_rif, 0.05)` — **vita media della memoria spinoriale** |

**Due tempi che non hanno nulla in comune se non il nome:** uno dice *quando un insieme di punti
diventa un oggetto*, l'altro *quanto a lungo un nodo ricorda la propria rotazione*. **Condividono un
numero per accidente storico.** Cambiarlo li tocca entrambi, e il secondo regge `omega_eq ∝
sqrt(tau)`, il random walk smorzato, il plateau di `|omega_s|`.

### 2. Il fatto che decide: **quella sostituzione esiste già, e il suo sigillo è FALLITO**

```
:2218   if TAU_LUCE:
:2222       _tau = self._tempo_luce_nodo(i, j)      # d_nodo / cs_nodo
```

**`--tau-luce` fa esattamente questo.** È la **FASE 2**, il suo sigillo **non è passato**
(`doc/SIGILLO_tau_luce_FALLITO.md`), è la voce **A** del registro e in CLAUDE.md §0 è dichiarata
**«il collo di bottiglia del programma»** — la ragione per cui **il gate resta indietro rispetto al
disco**.

> **Cablare `TAU_A = LAM/cs` avrebbe applicato a `_tau` una sostituzione equivalente, ma senza
> flag, senza sigillo, e dichiarata «correzione di difetto» — mentre la stessa cosa, fatta
> esplicitamente, è un ramo non certificato.** È il presidio di §2.6: *un timbro si mette DOPO il
> sigillo, mai prima.*

### 3. Due premesse minori, corrette

- **`LAM` non è «di stato»:** è `0.8` a `:146`, spostabile con `--lam`. `TAU_A = LAM/cs` **non
  elimina il numero scelto: lo sposta.** Resta legittimo — CLAUDE.md §3 elenca `LAM` fra le scale
  **già esistenti**, e A1 vieta le costanti **nuove** — **ma la formula corretta è «nessun parametro
  NUOVO», non «zero parametri».**
- **Il `git blame` non conferma la «compensazione scaduta»:** `TAU_A = 50` e la riga del `ramp`
  vengono **dallo stesso commit** `670310fc`, messaggio generico. **Non c'è evidenza** che `TAU_A`
  sia stato alzato per stabilizzare `omega`, quindi la modifica **non si può descrivere come
  rimozione di una compensazione scaduta.**

### 4. Cosa resta intatto

**Z9 non è toccata da nulla di tutto questo.** Il `ramp` matura in ~5526 passi, i run sono 300-500,
il peso d'arco tipico è ~1 % di quello maturo. **La diagnosi del mandato è giusta: è il VEICOLO
della cura che non regge.**

**Tre vie, tutte decisioni di regime** (`doc/REFERTO_tau_a_due_leggi.md` §6). La più pulita:
**separare le due leggi**, con una scala distinta per la maturazione e `TAU_A` dov'è. **Ma separare
significa stabilire che oggi due leggi condividono un numero per accidente — ed è una decisione.**

---

## 9.25 — **Rigirato il sigillo di `--tau-luce`: T4 si ribalta, T1 è scaduto, e T3 ha CAMBIATO SEGNO**

**La tesi era:** un sigillo preso su un sistema poi cambiato **quattordici volte** non è un ostacolo,
è una voce da rigirare. **Verificata: è vera su un punto su tre, e il rigiro ne ha aperto uno nuovo.**

### I due verdetti affiancati

| | **allora** (`7d484580`, 15 set) | **oggi** (`69ee5403`) | |
|---|---|---|---|
| **T1** byte-identità a flag OFF | PASS | **FAIL** | **criterio SCADUTO** |
| **T2** riduzione al limite | FAIL (`n` 1718 vs 1647) | FAIL (`n` 1682 vs 1680) | **stessa ragione** |
| **T3** pendenza | FAIL (OFF −0.1685 → ON −0.4265) | FAIL (OFF **−1.7311** → ON **−1.2749**) | **RAGIONE DIVERSA** |
| **T4** covarianza | FAIL (`cs→2cs` = `1.000000`) | **PASS** (`cs→2cs` = **`0.500000`**) | **ribaltato** |

### ✅ T4 — il FAIL era l'artefatto di un difetto poi curato

```
allora :  cs -> 2cs : 1.000000   (atteso 0.500000)   <- NON SEGUE
oggi   :  cs -> 2cs : 0.500000   (atteso 0.500000)   <- ESATTO
```

`_cs_nodo_prev` veniva scartata a ogni mitosi (**80 % dei passi con `cs = CS_M`**); la cura **C7**
(`43e9a47`) ha portato il fallback da **71.88 %** a **0.00 %**. **`tau = d/cs` segue ora lo stato da
solo su entrambe le grandezze, in modo esatto: è una LEGGE, non un numero travestito.** Il sigillo
di allora **non poteva dirlo**.

### T1 — scaduto, **e non è una regressione**

T1 confronta il codice attuale, a flag OFF, con `_old_sim_pre_tauluce.py` — verificato dal disco:
blob **`f5887254`**, cioè **`f7051c3~1`**, **quindici commit fa**. **Le differenze che rileva sono
le sette correzioni di legge sigillate: T1 sta misurando che la bonifica è avvenuta.** Non ho
riscritto il criterio: **lo dichiaro scaduto**, come il mandato ordina.

### T2 — stessa ragione, **ed era previsto prima di girarlo**

Il monkeypatch colpisce il metodo **condiviso** `_tempo_luce_nodo`, quindi cambia anche lo Strato 1.
**È un difetto del test, non del codice, e il rigiro non poteva cambiarlo** — scritto nella
marcatura (`b6c83c3`) **prima** dell'esecuzione. **Conseguenza che resta:** finché T2 non è
riscritto, `--tau-luce` **non ha una riduzione al limite** — manca cioè il sigillo che dimostra che
il flag *sostituisce* una legge invece di *aggiungerne* una.

### ⚠ T3 — il reperto nuovo: **l'effetto ha cambiato verso**

| | pendenza OFF | pendenza ON | effetto |
|---|---|---|---|
| allora | −0.1685 | −0.4265 | ON si **allontana** da zero di 0.258 |
| oggi | **−1.7311 ± 0.0197** | **−1.2749 ± 0.0155** | ON si **avvicina** di 0.456 |

**`IC95` disgiunti**, quindi non è il caso. **E anche il braccio OFF si è spostato di dieci volte**
(−0.1685 → −1.7311): non per `--tau-luce`, ma per la **bonifica** — l'inerzia dimensionale entra
proprio nella grandezza contro cui la pendenza è misurata. **I due esperimenti non misurano la
stessa cosa**, e trattare i quattro numeri come commensurabili sarebbe un errore.

**Non invento una spiegazione** — è il punto in cui, in una notte, ne sono state generate tre
sbagliate. Il mandato fissa la lettura **prima**: *«fallisce per una ragione diversa → reperto nuovo,
riporta e fermati.»*

### Cosa ne è dell'ostacolo a `TAU_A`

**Non cade, ma non regge più per le ragioni di allora.** E resta fermo il punto che il blocco aveva
sollevato per primo, **che nessun rigiro tocca**: `TAU_A = LAM/cs` **non elimina il numero scelto —
lo sposta su `LAM`** (`0.8` a `:146`, spostabile con `--lam`). Su quello il mandato stesso ha
accolto il blocco.

### Due voci nuove nel registro

- **Z10** — **`TAU_A` è un solo numero per DUE leggi fisiche distinte**, e la loro coincidenza è
  **accidentale, non derivata**: il `git blame` la conferma (stesso commit `670310fc`, messaggio
  generico). **È un difetto di suo**, indipendente da Z9 e da `--tau-luce`.
- **Z11** — **rigiro dei sigilli storici**, registrato come **lavoro previsto**: il caso
  `--tau-luce` mostra che un sigillo può dire il falso **in entrambi i versi** — T4 da FAIL a PASS,
  **T1 da PASS a FAIL**. Vale per Strato 1 (25/27), Step 2 (9/10), rumore colorato, e per i sigilli
  di questa bonifica quando il blob cambierà ancora.

---

## 9.26 — **Z9: la legge è giusta, il PUNTO in cui valutarla no.** `_pesi()` gira sedici volte per passo

**La correzione proposta** — `ramp = min(1, eta / (d_nodo/cs_nodo))` al posto di `eta/TAU_A` —
**separa le due leggi che `TAU_A` governava** e **fa sparire il numero** invece di spostarlo su
`LAM`, che era l'errore bocciato. **Quattro verifiche preliminari su cinque passano. La quinta
blocca.**

### Il reperto

```
passo    _pesi() PRIMA della scrittura di _cs_nodo_prev    DOPO
  1              9                                          7
  2              9                                          7
  5              9                                          7
```

**A ogni passo `_pesi()` è chiamata 16 volte, 9 prima che la cache sia aggiornata (`:3213`) e 7
dopo.** Se il `ramp` leggesse `_tempo_luce_nodo`, **9 chiamate userebbero il `cs` precedente (A6 ✓)
e 7 quello corrente (A6 ✗)**: **il 44 %, a ogni passo, in modo permanente** — non nel transitorio.
E **il valore della maturazione dipenderebbe da quale delle sedici chiamate la calcola**: un
dettaglio di implementazione, non la fisica.

### Il terzo lettore, e perché A8b esiste

```
_cs_nodo_prev  letta da _tempo_luce_nodo   :  0.0000 %
_cs_nodo_prev  letta da _passo_spinoriale  :  3.0303 %
_cs_nodo_prev  letta da _pesi()            :  7.8189 %
```

I 19 fallback di `_pesi()` sono **tutti al passo 0**: la frazione alta viene dal **numero di
chiamate**, non da un comportamento peggiore. **Ed è esattamente il punto di A8b: la frazione di un
fallback non è una proprietà della cache, è una proprietà del CONSUMATORE** — finché ogni
consumatore non è contato separatamente, quel numero non dice nulla.

### Le altre quattro verifiche passano, **e la diagnosi di Z9 regge**

- **`_tempo_luce_nodo`** è chiamabile, restituisce **per nodo**, **non chiama `_pesi()`** (nessuna
  ricorsione), nessun ricalcolo.
- **Nodi isolati: ZERO** su 87120 nodi-chiamata → **`LAM` non entrerebbe mai** nella maturazione. Il
  divieto del mandato è rispettato **di fatto**, non solo di forma.
- **L'ordine di grandezza conferma Z9:** `d_nodo ~ 1.63`, `cs ~ 2.0` → tempo-luce **~0.82** contro
  `TAU_A = 50`; con `eta` a ~0.009/passo, `ramp = 1` arriverebbe **entro un centinaio di passi** —
  **dentro la durata dei run**.
- **`TAU_A` non compare altrove:** rienumerato sul blob attuale, nessun punto nuovo.

### Cosa lo sbloccherebbe

**Uno snapshot per-passo del tempo-luce nodale**, calcolato una volta all'inizio di `step()` e letto
da tutte e sedici le chiamate: risolve **A6**, l'**ordine**, e il **costo** (16 valutazioni → 1).
**Ma è stato nuovo, e A8b impone di estenderlo ai cinque punti di crescita e di contarlo** — il
prezzo che questo repo ha già pagato **due volte** (`_cs_nodo_prev` 71.88 %, `_psi_spin_prec`
95.33 %). **Aggiungere stato per una correzione non autorizzata sarebbe cablarla a metà**, e lo
stato sopravviverebbe alla decisione di non farla.

> **Il blocco non è sulla LEGGE — è sul PUNTO in cui verrebbe valutata.** La legge è quella giusta:
> fa sparire il numero, separa le due scale, e non usa `LAM`.

---

## 9.27 — `calcola_psi(w=None)`: **il 100 % delle chiamate ricalcola i pesi. Ma «sedici violazioni» sono DUE**, e il resto era già misurato

**TEMPO 1 — solo strumentazione, e i due sigilli passano:**
```
Q1b BYTE-IDENTICO: max|A-B| = 0.000e+00   (38 array, nodi 1669 = 1669)
Q2  _calcpsi_w_none = 134 su 134  ->  il 100 % delle chiamate ricalcola i pesi
```
**Nessuno dei ~19 chiamanti passa `w`, benché il parametro esista.** Su questo la diagnosi è giusta.

### La tabella ridimensiona la premessa

```
step:3006      1.00 per passo    DENTRO il passo
step:3118      1.00 per passo    DENTRO il passo
-------------------------------------------------
DENTRO il passo (violano :2959):  2.00 per passo
```

**Il mandato dice *«le sedici volte sono sedici violazioni»*. Non lo sono: sono DUE.** Le sedici
chiamate a `_pesi()` vengono per l'**80.5 %** da `stato_crossover`, raggiunto attraverso
`massa_critica_adattiva` — **`_pesi()` chiama indirettamente sé stesso**, profondità **2**.

### ⚠ E questo era già committato il 14 settembre

`doc/REPERTO_pesi_ricorsione.md`, voce **M**. I numeri coincidono: allora `calcola_psi` **12.8 %** e
`stato_crossover` **80.9 %**, oggi **13.3 %** e **80.5 %**. **E quel referto fermò un mandato per la
stessa ragione**, con le stesse parole: *«il mandato assume che le 16 chiamate siano ricalcoli
ridondanti da parte di `calcola_psi()`… la misura dice che la premessa è falsa.»*

**La premessa di oggi è la stessa, e la misura la smentisce di nuovo.** *(È P1, e stavolta l'ho
mancato io: il fatto era sul disco e non l'ho riletto prima di misurare. La misura ha confermato,
non scoperto.)*

### Ma il difetto esiste, ed è flagrante — **su due punti**

```python
:3006   psi_forces = psi_t if SYNC_UPDATE else self.calcola_psi()
:3007   MtPsi = self._mat(w) @ psi_forces
```

**Nella stessa espressione:** `psi_forces` viene da `calcola_psi()`, che **ricalcola i pesi al suo
interno**; `self._mat(w)` usa il **`w` di `step`**. **Due insiemi di pesi diversi, moltiplicati
insieme** — esattamente la «lettura mista t/t+1» che il commento a `:2960` vieta, **una riga sotto**.
Stessa struttura a `:3118`. **Entrambi i rami sono presi perché `SYNC_UPDATE` è FALSE** in tutti i
run del fork: **con `SYNC_UPDATE` ON il difetto non esiste.**

*(La domanda del 14 settembre era l'**ottimizzazione**; questa è la **correttezza**. Sono diverse, e
la seconda è legittima anche se la prima era stata chiusa.)*

### Il TEMPO 2 è realizzabile, e la sua portata è chiara

**Due righe**: passare `w`, che a `:3007` **è già presente e già usato** — quindi valido, e la
topologia non cambia fra `:2979` e i due punti. **Elimina 2 ricalcoli su 16 (13 %), non sedici.**
**E sull'effetto non ho una previsione:** se i pesi coincidono, il difetto è **teorico**. È **Q4** a
deciderlo, non un'attesa.

### 9.27-bis — la discrepanza «due o tre punti», sciolta

**Rilievo del guardiano:** lui contava **tre** punti dentro `step`, il contatore ne registrava
**due**. **Non era un disaccordo: unità diverse.** Dal codice:

```python
:3005   if REPULS_LEGGE:          # True di default  ->  :3006 GIRA
:3036   elif MU_PSI != 0.0:       # elif ESCLUSO     ->  :3037 NON gira
:3118   ...                                             GIRA (se K_SYNC != 0)
```

**`:3006` e `:3037` sono i due rami di un `if`/`elif` mutuamente esclusivi**, e il commento a
`:3039` chiama il secondo *«vecchia repulsione a parametro, fallback»*. **Il contatore misura ciò
che gira, il grep ciò che è scritto: entrambe le misure sono giuste e servono a cose diverse.**

**Conseguenza per il TEMPO 2: i punti da toccare sono TRE, non due** — ma `:3037` è **su un ramo
spento**, quindi **nessun sigillo può esercitarlo**, e il referto dovrà dirlo invece di contarlo fra
i successi. *(È la classe di `VERSO_CHI`: cablato ma muto.)*

---

## 9.28 — **`Y5` rosso: la causa è `rho_sorgente ≤ 0`**, e non è nessuna delle due porte ipotizzate

**Strumentazione byte-inerte** (`max|A-B| = 0.000e+00`, nodi 2025 = 2025) che separa le porte del
fallback dello sfondo dell'inerzia. **Nessuna riparazione: il mandato chiedeva di misurare.**

```
PORTA A  (len(peq) != len(i))   :  0        MAI
PORTA B  (peq NaN o <= 0)       :  4 / 66   ultima invocazione 8
   -> _peq_nodo NON valido      :  2392     ultima 8
   -> rho_sorgente NON valido   :  2019     ultima 66     <---
fallback totale                 :  3215     ultima 66   (3215 CON archi, 0 senza)
```

**Nessuna delle tre letture fissate prima. È una quarta:**

- **PORTA A non scatta mai** → nessun difetto di lunghezza, A8b in quella forma non si applica;
- **PORTA B solo fino all'invocazione 8**, e il suo conteggio **2392** è **esattamente il fallback
  totale del blob PRE-TEMPO 2** → **la componente `peq` è INVARIATA**;
- **la causa permanente è `rho_sorgente ≤ 0`** — cioè **`rho_spin`, il campo EMESSO**. Il TEMPO 2 ha
  cambiato `psi` (Q4: 1669 nodi contro 1850) e **ha prodotto nodi in cui il campo emesso si
  annulla**, dove prima non accadeva.

### I due rilievi del guardiano, verificati dal codice

**① *«l'inerzia legge `peq` DOPO la diffusione di questo passo: è A5»* → FALSO.** L'ordine lo decide:
`_peq_t` a `:2986`, l'inerzia legge a `:3217`, la **calibrazione** è a `:3302` e la **diffusione** a
`:3320` — **cento righe dopo**. L'informazione dei vicini di questo passo **non è ancora entrata**.

**② *«`_peq_t` esiste e l'inerzia non lo usa»* → VERO nella forma, senza conseguenza oggi**: fra
`:2986` e `:3217` nulla modifica `self.peq`, quindi **lo stato vivo È la fotografia** e la
sostituzione sarebbe **byte-identica**.
**Ma il rilievo coglie una cosa vera:** la garanzia viene **dall'ORDINE, non dalla struttura**. Se
`_passo_spinoriale` venisse spostato dopo `:3320`, **A6 si romperebbe in silenzio**. *(Ed è il limite
di come l'avevo scritto io nel commento dell'inerzia: «A6 soddisfatto per costruzione» — è
soddisfatto **dall'ordine**, che è più fragile.)*

**③ Il parallelo con `_psi_spin_prec` e `_cs_nodo_prev` NON regge:** quelle erano **cache inerti**
(**95.33 %** e **71.88 %** di fallback, la legge dichiarata non girava). **Qui lo snapshot è
EQUIVALENTE, non mancante.** Chiamarla «la terza volta nello stesso settore» sovrappone **un
meccanismo morto** e **una garanzia che dipende dall'ordine**: la seconda va irrobustita, la prima
era un difetto.

### Cosa resta aperto

Quattro vie, tutte decisioni: **rimisurare `Y5`** (se i nodi a campo emesso nullo sono legittimi);
**trattare `rho_sorgente ≤ 0` come caso a sé**; **revertire il TEMPO 2** (ma Q4 ha dimostrato che
quel difetto era **reale**); oppure — indipendente da `Y5` — **far leggere `_peq_t`**, che oggi
sarebbe byte-identico: **irrobustimento, non correzione**.

---

## 9.29 — **I nodi senza campo non c'erano prima: il TEMPO 2 li ha creati.** E `Z9` non c'entra

**La domanda era una sola:** i nodi con `rho_sorgente ≤ 0` c'erano già prima del TEMPO 2?
**Sonda ESTERNA, identica sui due blob** — il vecchio non ha i contatori cablati, e strumentare solo
uno dei due non sarebbe un confronto. Copia estratta con `git cat-file -p`, **mai `git checkout`**;
`hash-object` verificato = `9dfd91c4`.

| | **VECCHIO `9dfd91c4`** | **ATTUALE `a8f1b2f4`** |
|---|---|---|
| invocazioni con `rho ≤ 0` | **0** | **26** su 66 |
| nodi-invocazione | **0** | **488** |
| di cui **zero esatto** | 0 | **488** |
| di cui denormali | 0 | **0** |

> **Prima non ce n'era nessuno. È la seconda lettura: il TEMPO 2 li ha creati.**

### Il sospetto `Z9` è smentito — da tre misure indipendenti

1. **Sono ZERO ESATTO, non denormali** (488/488, zero sotto `1e-300`). **La maturazione lenta del
   kernel lascerebbe valori piccolissimi ma non nulli.**
2. **Il `ramp` dei loro vicini (0.0039742) è quello di tutti (0.0038639)**: non hanno vicini più
   immaturi della media.
3. **`ramp` è identico nei due blob** — il TEMPO 2 non lo tocca. **Se la causa fosse `Z9`, ci
   sarebbero stati anche prima.**

### Chi sono: **i figli della mitosi**

```
GRADO  senza campo :  2.00     con campo : 119.00
ETA    senza campo : 0.0136    con campo : 0.1936
```

**Grado esattamente 2** — la firma della mitosi (§9: *«il figlio nasce con esattamente due archi»*)
— **ed età 14 volte minore**. E la distribuzione lo conferma: dopo il setup, **un rivolo di 1-5 nodi
per invocazione**, con `n` che cresce da 443 a 488.

### ⚠ Cosa non dico: il meccanismo

**So chi sono, quando, e che prima non c'erano. Non so PERCHÉ il TEMPO 2 li produca, e non lo
invento.** L'ipotesi ovvia — *«`calcola_psi()` ricalcolava i pesi e popolava `psi_spin` per i nodi
nuovi»* — **non è verificata**, e **confligge** con la verifica preliminare del TEMPO 2, che aveva
misurato la topologia **invariata al 100 %** dentro `step` (la mitosi avviene **fuori**). **Le due
cose non tornano da sole.**

### E una correzione alla sonda, prima dei numeri

La prima versione usava una **scena mia** e dava **60** invocazioni contro le **66** del batch: la
differenza erano i **sei passi di riscaldamento** dopo `semina(80)`. **Una sonda che non riproduce
la scena misura un altro sistema**, e il primo risultato era di quel sistema. Scena ora riprodotta
**dal sorgente**, conteggi allineati.

> **`Q8` non ha reso visibile un difetto preesistente: ha intercettato una REGRESSIONE**, e prima
> che entrasse in una campagna. **È esattamente ciò per cui il rigiro dei sigilli esiste.**

---

## 9.30 — **Il TEMPO 2 non ha creato un difetto: ha tolto uno SFASAMENTO.** Per mesi il neonato ha pesato `2e-4` invece di zero

**L'ipotesi era precisa e nasceva da una riga:**

```python
:3018   w = self._pesi(); self.eta += dt_n
        ^^^^^^^^^^^^^^^   ^^^^^^^^^^^^^^^
        usa eta VECCHIA   POI la incrementa
```

**Confermata su tutti e tre i punti.**

### ① Il test diretto — 100 %

```
su 31 nodi-passo appena nati (grado 2, eta = 0):
  ramp PRIMA dell'incremento ESATTAMENTE 0 :  31 / 31   (100.00 %)
  ramp DOPO  l'incremento    ESATTAMENTE 0 :   0 / 31
  ramp DOPO, minimo osservato              :  0.0002
```

### ③ Il conto dei pesi — 100 %

```
archi incidenti ai neonati       : 62
di cui con peso ESATTAMENTE ZERO : 62   (100.00 %)
```

Entrambi gli archi del figlio hanno peso zero, perché **`ramp[figlio]` è un FATTORE di ogni suo
arco** (`base ∝ ramp[i]·ramp[j]`). Quindi `psi = 0`, e `rho_sorgente = 0`.

### ② La controprova — risolta leggendo il codice

```
VECCHIO :2979  w = self._pesi(); self.eta += dt_n
        :3006  ... self.calcola_psi()     <- RICALCOLA _pesi(), DOPO l'incremento
ATTUALE :3018  w = self._pesi(); self.eta += dt_n
        :3052  ... self.calcola_psi(w)    <- usa `w`, eta VECCHIA
```

**Nel blob vecchio il ricalcolo avveniva dopo l'incremento**, e il neonato riceveva un peso
**minuscolo ma non nullo** — confermato dalla misura indipendente di §9.29: sul blob vecchio i nodi
con `rho ≤ 0` erano **zero**.

### Il verdetto

> **Il TEMPO 2 non ha introdotto un difetto: ha TOLTO uno sfasamento.**
> **E il peso zero per un neonato è l'INTENTO DICHIARATO** — CLAUDE.md §9 e A7b dicono la stessa
> cosa: *«un nodo appena nato non pesa ancora»*, e zero è il valore corretto di `ramp` con `eta = 0`.
> **Il `2e-4` di prima era una PERDITA DI SINCRONIA, non una scelta di legge.**

**`Y5` era scritto su quel comportamento sfasato: è l'ottavo criterio scaduto di questo giro.**
**Non l'ho riscritto** — serve un mandato proprio, perché riscrivere un criterio è la cosa su cui
questo repo ha già sbagliato otto volte.

### Il fatto che va registrato, e non è piccolo

> **Per tutto il tempo in cui quel codice è girato, il nodo appena nato ha pesato `~2e-4` invece di
> `0`, e nessuno lo sapeva.**

**È la QUARTA volta** che uno sfasamento temporale silenzioso viene alla luce: `_cs_nodo_prev`
(**71.88 %**), `_psi_spin_prec` (**95.33 %**, FASE 5 inerte per mesi), **i due `theta`** (C19), e
questo. **La famiglia è sempre la stessa: una grandezza letta in un momento del passo diverso da
quello che il codice dichiara** — ed è ciò che A6 chiede di escludere, **col segno opposto**: non uno
stato troppo nuovo, ma **due letture della stessa grandezza a istanti diversi**.

**E le quattro sono emerse TUTTE per caso, indagando altro.** La scansione sistematica — *quali
altre grandezze sono lette in più punti del passo?* — **non è mai stata fatta** (voce **Z19**).

---

## 9.31 — **`Y5` riscritto, `Q8` sbloccato.** E la quarta volta dello stesso difetto ha una voce propria

**Il codice non è stato toccato.** Si è riscritto un **criterio** e registrato un **fatto**.

### Perché il vecchio `Y5` era scaduto — l'ottavo di questo giro

Diceva *«il fallback dello sfondo cessa entro poche invocazioni e non torna»*, **ed era vero solo
perché il neonato riceveva un peso spurio `~2e-4`** — lo sfasamento `eta` misurato in §9.30. Tolto
quello, i figli hanno `rho_sorgente = 0` al primo passo **sempre, per costruzione**, ed è **ciò che
l'intento dichiara** (§9: *«un nodo appena nato non pesa ancora»*).

> **Il criterio vecchio leggeva quella CORREZIONE come un danno.**
> **`Q8` non ha intercettato un guasto: ha intercettato una correzione che il criterio non sapeva
> riconoscere. Il presidio ha funzionato — anche nel dirci che il problema era lui.**

### Il criterio nuovo, e **come può fallire**

| | cosa misura | esito |
|---|---|---|
| **Y5.0** | gli indici dei nodi sono stabili (`n` monotono) | **PASS** — da 80 a 488, mai decrescente |
| **Y5a** | il fallback scatta **solo** su nodi di grado 2 (firma mitosi) | **PASS** — grado min 2, mediana 2, **max 2** |
| **Y5b** | **nessun nodo maturo** cade nel fallback | **PASS** — 0 nodi con `eta` sopra metà della mediana |
| **Y5c** | ogni nodo resta in fallback **una sola invocazione** | **PASS** — «1 inv → 48 nodi», peggiore **1** |

```
ETA dei caduti : min 0.0022  mediana 0.0138  max 0.0141     (mediana di TUTTI: 0.2332)
```

**Diciassette volte più giovani, grado esattamente 2, e ciascuno per un solo passo.**

**E il criterio PUÒ fallire**, che è la ragione per cui sostituisce il vecchio: basta **un** nodo
maturo in fallback (`Y5b`) — nulla nella forma del codice lo impedisce — o **un** figlio che ci
resti due invocazioni (`Y5c`), che significherebbe `eta` non cresciuta o campo non acceso al passo
dopo. **Sarebbe un difetto nuovo.** Il vecchio `Y5` misurava invece *«quando cessa»*, che dipendeva
**dallo sfasamento**: era un criterio scritto sul difetto, non sulla legge.

### La voce nuova: **il tempo di valutazione è esso stesso una grandezza fisica**

| caso | cosa era sfasato | quanto scattava | conseguenza |
|---|---|---|---|
| `_cs_nodo_prev` | cache scartata a ogni mitosi | **71.88 %** | `cs = CS_M` costante |
| `_psi_spin_prec` | cache non estesa alla mitosi | **95.33 %** | FASE 5 / 4π inerte per mesi |
| i due `theta` (C19) | tempo di coordinata vs proprio | — | un numero che si muove per la convenzione |
| lo sfasamento `eta` | pesi valutati a un `eta` diverso | **sempre, sui neonati** | il neonato pesava `2e-4` invece di 0 |

**Nessuno di questi produceva un errore.** Il sistema girava, i sigilli passavano, i numeri
sembravano ragionevoli. **E ogni volta si stava misurando un'altra fisica.**

**E il collegamento ad A6, che mancava:** **A6 si viola anche senza toccare la formula.** La
violazione può stare nell'**ordine delle chiamate** invece che nella forma della legge — **e allora
non si vede leggendo la formula**. Chi applica A6 non deve guardare solo *quali* grandezze entrano
in una legge, ma **a quale tempo ciascuna è valutata, e se quel tempo è garantito dalla STRUTTURA o
solo dall'ORDINE**. *(Caso reale: l'inerzia legge `peq`, `cs` e `d` prima che vengano aggiornati —
corretto **oggi**, ma si romperebbe **in silenzio** se il blocco venisse spostato. Voce **Z17**.)*

**Tutte e quattro sono emerse per caso, indagando altro. La scansione sistematica non è mai stata
fatta** (**Z19**).

### Cosa chiude questo giro

**Un difetto che il codice si portava da mesi, chiuso senza toccare una riga di fisica** — perché la
correzione era già stata fatta dal TEMPO 2, e mancava solo un criterio che sapesse riconoscerla.

### ⚠ E il rigiro ha trovato la seconda cosa: **`Q1` è il NONO criterio scaduto**

```
V1 8/8 PASS · V2-V5 8/8 PASS · V6-V10 12/12 PASS · Y 10/10 PASS
Q0,Q3-Q8 7/7 PASS · Y5 riscritto 4/4 PASS
Q1-Q2  2/3  ->  FAIL
```

```
[FAIL] Q1a c'e' CONFRONTO (stesso N)   0 array confrontati, 38 con shape diverse, nodi 1669 vs 1850
[PASS] Q1b BYTE-IDENTICO: 0.000e+00    su 0 array     <- MANCANZA DI CONFRONTO
```

**Il presidio ha funzionato in modo esemplare:** `Q1b` avrebbe dato un **falso PASS** — uno zero su
**zero array confrontati** — e **`Q1a` l'ha intercettato**, perché guarda le shape **prima** di
leggere lo zero. *(È il caso catalogato in §9: «`max|A-B| = 0.000e+00` può significare "nessun
confronto"».)*

**Il riferimento di `Q1` è il blob `69ee5403`, cioè PRIMA del TEMPO 2**, e il TEMPO 2 **cambia le
traiettorie per costruzione** (`Q4`: 1669 nodi contro 1850). **La domanda di `Q1` — "i contatori
sono inerti?" — ha già avuto risposta allora**, e oggi la stessa misura risponde a un'altra domanda.
**Identico a `T1` del sigillo `--tau-luce`.**

**Non l'ho riscritto:** riscrivere un criterio va fatto **con un mandato proprio**, ed è la regola
che questo stesso giro ha appena applicato a `Y5`.

---

## 9.32 — **`Z9` è ancora quella, e `R6` regge.** Il TEMPO 2 agiva sul 2.4 % delle chiamate

**Due verdetti presi contro numeri di otto commit fa**, con la stessa disciplina che aveva rimesso in
discussione il sigillo di `--tau-luce`: *un verdetto preso su un sistema cambiato non è un verdetto,
è una voce da rigirare*.

### `Z9` — sostanzialmente intatta

**Due scene, e la distinzione è metodologica:** la misura originale usava una scena a **3 masse da
120**; quella è **l'unica confrontabile coi suoi numeri**. La scena del **batch** è il sistema reale.
**Riporto entrambe.**

| passo | `ramp` mediano **oggi** (scena orig.) | **`cdc0e41`** |
|---|---|---|
| 1 | 0.0002 | 0.0002 |
| 60 | **0.010179** | 0.0106 |
| 120 | **0.020414** | 0.0217 |

```
eta/passo : 0.00849  (era ~0.009)      ramp = 1 a 5887  (era ~5526)
scena del batch                        ramp = 1 a 5960
```

**I numeri vanno nella direzione che il mandato indicava come possibile — maturazione un po' più
lenta — e la catena causale è plausibile:** i neonati ora pesano **zero** invece di `2e-4`,
contribuiscono meno a `psi`, quindi `r` è più basso e `eta` cresce più piano.

> **Ma è UN SOLO SEME, e P3 vieta di chiamarlo un effetto.** La dispersione di `ramp` fra semi **non
> è mai stata misurata**, e uno scarto del **6-8 %** su un seme **non è distinguibile da essa**.
> **La lettura onesta è la prima delle tre: `Z9` è intatta.**

**E il fatto non cambia di una virgola:** il kernel matura in **~5900 passi**, i run sono **300-500**,
a 500 passi `ramp` sta **sotto il 10 %**.

### `R6` — **regge**, e il perché è istruttivo

```
                        OGGI        riferimento (8bfcf46)
_pesi() per passo        12                 16
   PRIMA della cache      7                  9
   DOPO                   5                  7
```

**Il TEMPO 2 ha ridotto le chiamate da 16 a 12, ma `_pesi()` gira ANCORA a cavallo.** La lettura era
fissata prima: **gira a cavallo → `R6` regge**. Valutare lì il `ramp` violerebbe **A6 sul 42 %** delle
chiamate, a ogni passo.

**E il quadro per chiamante spiega perché il TEMPO 2 non poteva bastare:**

```
stato_crossover = 1354      step = 123      calcola_psi = 37
```

**Il TEMPO 2 agiva su `calcola_psi`, che è il 2.4 % delle chiamate. L'89 % viene da
`stato_crossover`**, attraverso `massa_critica_adattiva` — **la ricorsione indiretta già registrata
il 14 settembre** (voce **M**). **Correggere `calcola_psi` non poteva sbloccare `R6`, e infatti non
l'ha sbloccato.** *(Questo dà anche la misura giusta del TEMPO 2: era corretto e necessario, ma la
sua portata era il 2.4 % — ed è coerente con ciò che il referto del TEMPO 1 aveva già scritto:
«elimina 2 ricalcoli su 16».)*

### Cosa resta

**`Z9` va curata, e le due cure provate sono bocciate a ragione**: `TAU_A = LAM/cs` **sposta** il
numero su `LAM`; `ramp = eta/(d/cs)` **viola A6** dove verrebbe valutato. **La via che `R6` indica**
— valutare il `ramp` **una volta per passo** da uno snapshot — **resta la voce Z12, con il prezzo
A8b**. **Oppure affrontare la ricorsione `stato_crossover → _pesi()`, l'89 %** — ma è la voce **M**,
un fronte diverso.

---

## 9.33 — **`TAU_A = 2.0` non diverge. Ma «non esplode» non è «sta bene»**

**La domanda:** la testimonianza di Luca dice che `TAU_A = 50` fu scelto *«prima di creare il
repository, per non far esplodere tutto»*. **Da git non è verificabile** — il valore c'è dal primo
commit che aggiunge il file (**`670310f`**, 28 agosto; *non* `ca02af0`, che è del 13 settembre), e
**`git log -S` trova un solo commit: nessuno lo ha mai cambiato**. È **assenza di prova**, non prova
di assenza. **L'esperimento la mette alla prova.**

### S1 — non diverge: 5/5 PASS

```
nessun NaN/inf · |nb|-1 = 2.2e-16 · d0>0 · _taup_cfl_max 0.5627 (vs 0.5644) · omega x2.69
```

### ⚠ Ma i segni di stress sono grossi

| max | `TAU_A=50` | `TAU_A=2.0` | |
|---|---|---|---|
| `psi` | 0.064 | **5.834** | **× 91** |
| `d0` | 2.878 | **50.22** | **× 17.4** |
| `phivel` | 2.787 | **63.35** | **× 22.7** |
| **nodi finali** | **2577** | **1754** | **−32 %** |

> **Il sistema non diverge, ma non è lo stesso sistema.** «Regge» qui significa soltanto
> **«l'aritmetica non produce NaN»**.

### S2 — `Z9` sarebbe risolta, e non di poco

```
TAU_A=50   ramp med 0.0148   ramp=1 al passo ~8133
TAU_A=2.0  ramp med 0.4704   ramp=1 al passo ~255
```

**Il kernel arriverebbe a maturità DENTRO la durata dei run.** *(Il `~8133` usa un metodo diverso
dal `~5960` della rimisura — `eta/120` contro `(eta₁₂₀−eta₁)/119` — e va confrontato solo col `~255`
della stessa tabella.)*

### Il verdetto: la **terza** lettura

**Due conseguenze opposte, da tenere insieme:** la compensazione **sembra scaduta** nel senso stretto
(non diverge più — *plausibilmente per le correzioni di questo giro, ma non l'ho misurato*); **ma il
prezzo non è un dettaglio**, e adottare `TAU_A = 2.0` **non sarebbe togliere una compensazione:
sarebbe cambiare sistema.**

**Non promosso, default invariato, flag OFF, `S3` byte-identico verificato prima del run.**

### E un punto che vale per la prossima mossa

**L'esperimento ha mosso ENTRAMBE le leggi che `TAU_A` governa** (**Z10**): la maturazione del
kernel **e** la vita media della memoria spinoriale. **Parte dello stress osservato può venire dalla
seconda, non dalla prima** — e **distinguerle richiede esattamente la separazione che `Z10`
chiede.** *(Il che rende `Z10` non più un fronte collaterale, ma il prerequisito per interpretare
questo risultato.)*

### Cosa non ho guardato

`chi`, `|<n>|`, `theta`, `L_tot`, MISURA U: **non misurati e non riportati**, come ordinato. **Senza
quelli non si può dire se la terza combinazione sia fisicamente sensata** — si sa solo che non
produce NaN. **Ed è un solo seme:** i rapporti (× 91, −32 %) **non hanno barra**, e su questo sistema
la dispersione fra semi è grande. **Sono ordini di grandezza, non misure.**

---

## 9.34 — **Il riferimento del mio A/B non era un riferimento.** Verificato dai dati: il `−32 %` di §9.33 **regge**

**Data:** 2026-09-17 · **Sollevato da Luca**, non trovato da me mentre lo usavo.

### Il difetto, nella sua forma generale

Il driver `csv/_test_fork/_esperimento_spin_feedback.py` costruisce i bracci come
`lista_comune + variabile`. Io avevo scritto `--tau-a 2.0` **nella lista comune**. Quindi il terzo
braccio — quello che doveva essere il **riferimento a `TAU_A = 50`** — lo riceveva anche lui.

> **Un driver che forza un flag in tutti i bracci rende ogni A/B che lo usa non attribuibile, e
> nessun messaggio lo dice.** Il test continua a **PASSARE**, perché confronta due cose identiche e
> le trova identiche.

È la stessa famiglia già catalogata in CLAUDE.md par.9 sotto *«quando si ribalta un default si
cercano TUTTI i punti che ottenevano il vecchio comportamento per OMISSIONE»*: lì un default
ribaltato **converte i rami di controllo in duplicati del ramo di prova**; qui lo fa una riga del
driver.

### La domanda che Luca ha posto, e che io non avevo posto

**Il `−32 %` di §9.33 era misurato contro `TAU_A = 50`, o contro un altro run a `TAU_A = 2.0`?**

E il modo in cui va risposta è il punto: **dai dati, non dal comando e non dalla memoria** (P6).
Il simulatore scrive in testa a ogni CSV una riga `# RUN_PARAMS {...}` con `tau_a_over` e
`leggi_attive.REGIME`.

| file | REGIME | `tau_a_over` | **`TAU_A` effettivo** | seed |
|---|---|---|---|---|
| `_exp_tau50.csv` | deterministico | `null` | **50.0** | 5 |
| `_exp_tau02.csv` | deterministico | `2.0` | **2.0** | 5 |

**Il riferimento era `TAU_A = 50`. §9.33 REGGE, i suoi numeri valgono, la terza lettura resta.**

E la controprova non era scontata: il `−32 %` ricalcolato dalla colonna `n_tot` dei CSV di ieri dà
**2577 → 1754 = −31.9 %**, e il braccio `rif` **rigirato oggi da un processo diverso** dà **2577
nodi esatti**. **Due riferimenti indipendenti, stesso numero.**

### Gli altri esperimenti, e il limite della mia verifica

Scansionati tutti i 34 driver che lanciano il simulatore in sottoprocesso. **Otto hanno più di un
braccio; nessun altro porta il difetto.**

**Ma il limite va dichiarato, perché altrimenti quella frase vale meno di quanto sembra.** La
scansione guarda **il disco di oggi**, e il file difettoso **era già stato corretto**. Il mio primo
rilevatore automatico — quello che cercava un flag presente sia nella lista comune sia fra le
varianti — ha restituito **zero collisioni, compreso il file che aveva il bug**.
**Un rilevatore che non trova il caso che lo ha generato non è un presidio.** La tabella è stata
rifatta a mano sul criterio *«quanti bracci, e quale flag è la variabile»*.

### Due lacune trovate strada facendo

1. **P6: `# RUN_PARAMS` non contiene né `TAU_A` né `G_PH` né il `blob`.** `TAU_A` è solo
   **deducibile** (`REGIME` + `tau_a_over`); il `blob` **nemmeno quello**, mentre CLAUDE.md par.9
   lo chiede esplicitamente. Qui la verifica si è salvata perché `tau_a_over` c'era: se avessi
   dovuto dedurre `TAU_A` dal solo `REGIME`, l'override sarebbe stato **invisibile nei dati** e
   questa risposta **non sarebbe stata possibile.**
2. **Par.5: il driver non era committato.** `_esperimento_spin_feedback.py` risulta `??` in
   `git status`, benché il commit `d3874fd` si intitoli *«Committato PRIMA del run»* — quel commit
   conteneva **il simulatore e le previsioni**, non il driver.

→ `doc/REFERTO_driver_gira.md`, registro `Z20`.

---

## 9.35 — **`SPIN_FEEDBACK` con `TAU_A = 2.0`: esito MISTO**, e non ne scelgo una delle quattro letture

**Un seme (5), 120 passi. `SPIN_FEEDBACK` NON HA UN SIGILLO: componente non certificato.
Nessuna promozione, nessun cablaggio, il default non cambia.**

### `E4` — il GATE: il feedback è applicato? **Sì**, e il numero dice più di quanto il gate chiedesse

`_sfb_applicato` **124 su 126** chiamate (98.4 %); `_sfb_lift_corto` 2 (il transitorio iniziale);
`_sfb_mask_vuota` **0**. **Nessuna traccia della famiglia `_psi_spin_prec`**, che fu inerte nel
95.33 % delle chiamate per mesi — ed era la ragione per cui i contatori erano stati cablati prima
del run.

Ampiezza in forma confrontabile (**A3c**, mediane dello **stesso passo**):
**rapporto |feedback|/|coppia| MEDIO su 126 passi = `2.706`.** *(Il massimo, 115, è un passo solo e
non è il tipico; e i due max separati — coppia `0.2602`, feedback `0.04145` — **sono presi in passi
diversi e non hanno quoziente**.)*

**Il gate passa: l'esperimento non è nullo. Ma `2.706` non significa «il feedback contribuisce»:
significa che il termine di feedback vale quasi TRE VOLTE la coppia su cui retroagisce. Un termine
chiamato *feedback* che domina il termine primario non è una correzione: è il motore.** Questo non
invalida l'esperimento, lo **qualifica**, e va davanti a qualunque lettura di `E2` ed `E3`.

### `E1` — stabilità **[BLOCCANTE]: 4/4 PASS**

0 NaN/inf · `max||nb|−1| = 2.220e-16` · `min d0 = 0.05 > 0` · `_taup_cfl_max` **0.5532** ON contro
0.5627 OFF, entrambi **< 1**. **Non diverge, e il vincolo causale su `tau_p` regge da entrambi i lati.**

### `E2` — il conteggio dei nodi, contro il `−32 %`

```
TAU_A = 50  (riferimento)   : 2577 nodi
TAU_A = 2.0, feedback OFF   : 1754 nodi   −31.9 %
TAU_A = 2.0, feedback ON    : 1833 nodi   −28.9 %
```

**La perdita si riduce di 3.0 punti** (+79 nodi, **+4.5 %**). **Direzione attesa. Ampiezza NON
stabilita, e lo dico prima che qualcuno la citi:**

- **un solo seme.** P3 chiede ≥ 4 semi per una barra fra semi;
- **il nullo di questa differenza non è misurato.** Il nullo caotico noto sul conteggio nodi vale
  ~1.4 % (`3164 → 3209`), ma è di **un'altra configurazione**, e `SPIN_FEEDBACK` **non è una
  perturbazione a 1e-16**: vale 2.7 volte la coppia, quindi quel nullo **non è nemmeno quello
  giusto da citare**.

Si scrive così: **«la perdita di nodi si riduce di 3.0 punti su un seme; il nullo di questa
differenza non è misurato»** — non «il feedback recupera il 4.5 % dei nodi».

### `E3` — e questa è la parte che non va minimizzata

| | `TAU_A=50` | OFF | ON |
|---|---|---|---|
| `psi` max | 0.0641 | 5.834 (×91) | **7.206 (×112)** |
| `d0` max | 2.878 | 50.22 (×17.5) | **77.83 (×27)** |
| `omega_s` max | — | 4.664e+04 | 3.441e+04 |
| `phivel` max | — | 63.35 | 50.66 |
| `ramp` mediana | — | 0.4704 | 0.4661 |

**Gli indicatori di stress PEGGIORANO col feedback acceso**: sono le stesse due grandezze che in
§9.33 avevano fatto scrivere *«non diverge non è sta bene»*, e con `SPIN_FEEDBACK` acceso **stanno
peggio**. `omega_s` e `phivel` invece **calano**: **il quadro non è monotono** — il feedback sposta
lo stress da un canale all'altro, non lo riduce. `ramp` è **indistinguibile** fra i due bracci, come
deve essere (`TAU_A` è identico): **è il controllo negativo interno dell'A/B, ed è utile che sia
piatto.**

### Il verdetto contro le quattro letture fissate prima

`(d)` contributo trascurabile → **escluso** da `E4`. `(c)` peggiora/diverge → **escluso** da `E1`.
**Fra `(a)` «si riduce IN MODO NETTO → l'ipotesi regge» e `(b)` «resta uguale → l'ipotesi cade» NON
scelgo**, e la ragione è la parola **«netto»**: sul conteggio nodi la direzione è quella di `(a)` ma
su **un seme e senza nullo**; sulle grandezze di stress il risultato è **contrario** ad `(a)`.

> **Un'ipotesi che guadagna 3 punti sul conteggio nodi mentre peggiora di 21 punti percentuali il
> picco di `d0` non ha «retto»: ha spostato il problema.**

**Per decidere servono, in quest'ordine: (1) un SIGILLO per `SPIN_FEEDBACK`; (2) ≥ 4 semi su `E2`;
(3) `Z10` — separare le due leggi che `TAU_A` governa**, perché finché `TAU_A` è insieme la scala
del `ramp` e la vita media della memoria spinoriale, *«cosa ha fatto `TAU_A = 2.0`»* non ha una
risposta unica, e questo A/B ci poggia sopra.

→ `doc/REFERTO_esperimento_spin_feedback.md`, registro `Z21`.

---

## 9.36 — **`E4a` è il DECIMO criterio scaduto**, e stavolta l'ho corretto *prima* che producesse il FAIL falso

I nove precedenti sono in §9.31 (l'ottavo, `Y5`) e nel suo seguito (il nono, `Q1`).

**Com'era scritto:** *«il feedback è applicato in **tutte** le chiamate»*, cioè
`_sfb_applicato == _sfb_chiamate`.
**Cosa fa davvero il codice:** `_spinor_lift` è più corto di `n` nei **primi due passi**, quindi la
guardia `:1344` scatta **2 volte su 126** — **legittimamente**, ed è un **transitorio di
inizializzazione**, non un fallback strutturale.

**Il criterio avrebbe dato FAIL su un comportamento corretto**, e si sarebbe portato dietro **una
diagnosi**: chi legge il FAIL cerca il difetto, e il difetto non c'è. È **esattamente** la forma di
`N3b`, `M1b`/`M3` e `M3c` già catalogata in CLAUDE.md par.9.

**Come è riscritto, e perché può ancora fallire:**

```
E4a:  _sfb_applicato >= 0.95 * _sfb_chiamate       (misurato: 124/126 = 98.4 %)
```

**Non è un criterio che passa sempre.** Fallirebbe esattamente nel caso che i contatori esistono per
intercettare: se una delle due guardie diventasse il **comportamento principale** invece del
transitorio. `_psi_spin_prec` scattava nel **95.33 %** delle chiamate — con questa soglia
**avrebbe dato FAIL al primo giro**, invece di restare inerte per mesi.

**La regola che ne esce, ed è la stessa di CLAUDE.md par.9 vista da un altro lato:** un criterio si
scrive **da una misura**, e la soglia si **deriva dal comportamento reale del codice nel punto in
cui il criterio guarda** — non dal proprio modello mentale di come «dovrebbe» andare. *«Tutte le
chiamate»* era il modello mentale; *«2 su 126 sono il transitorio»* è la misura.

---

## 9.37 — **Il `2.706` non è un fatto sul feedback. E `F3` fallisce prima ancora di essere scritto**

**Data:** 2026-09-17 · sonda `csv/_test_fork/_sonda_2706.py`, 64 invocazioni, `TAU_A = 2.0`,
scena del batch **in-process**. **Nessun run di misura, nessun sigillo, nessuna promozione.**

### Perché questa misura viene prima del sigillo

Il mandato di Luca la mette davanti a tutto con una frase che è il criterio stesso:
**«non si certifica un componente di cui non si sa cosa sia».** Avevo scritto, nel referto
precedente, che *«un termine chiamato feedback che vale quasi tre volte la coppia su cui
retroagisce non è una correzione, è il motore»*. **Quella frase non regge**, e il modo in cui non
regge è istruttivo.

### (1.1) Il confronto è pulito su tre assi, sporco su un quarto — **che è quello temporale**

Puliti e **verificati, non assunti**: stessa popolazione (`len = n = 484` entrambe, per-nodo),
stesso statistico (`median(abs(·))` contro `median(abs(·))`), stesso istante, **zero** nodi con
feedback esattamente nullo. E la premessa che il mandato *assumeva* — che `_spinor_lift` sia
normalizzato, così che `imag(ov) ∈ [−1,1]` — **regge: norma ∈ [1.000000, 1.000000] su 64
invocazioni.**

Sporco il quarto:

```
|feedback| / |coppia|, 64 invocazioni
   MEDIA        2086.2      <- dominata dai primi passi
   MEDIANA         1.834
   p25 / p75       1.113 / 9.507
   min / max       0.698 / 54844     ->  4.9 ORDINI di escursione
   ultimi 10 passi (il regime)        mediana  0.748
   passi col rapporto < 1                      14 / 64  (21.9 %)
```

**Il rapporto scende SOTTO 1 a maturazione.** Il `2.706` era una media su una popolazione **non
stazionaria**: descrive i primi campioni e **nessun passo reale**.

**È l'undicesimo caso di A3c, e cade sul mio stesso rimedio.** Due giorni fa avevo sostituito
*«due massimi presi in passi diversi»* con *«media dei rapporti per-passo»*, convinto di aver
sistemato popolazione, istante e unità. **A3c dice «stessa POPOLAZIONE», e una popolazione che si
muove di cinque ordini non è una popolazione.** La forma dell'errore è identica, spostata di un
asse: dallo **spazio** al **tempo**.

### (1.2) L'ampiezza viene dalla COPPIA, non dal feedback

Da 0 a 63 passi: **`|coppia|` cresce di un fattore ~2.9 milioni** (`2.1e-8 → 6.0e-2`),
**`|feedback|` di ~37** (`0.0011 → 0.042`).

E le sotto-grandezze dicono che il feedback è **ordinario**: `|imag(ov)|` mediana **0.035**
(max 0.852 — ben dentro `[0,1]`, e molto sotto lo 0.5 di spinori scorrelati: gli adiacenti sono
quasi in fase, come deve essere dopo una mitosi che copia esattamente); `w/grado` mediana
**0.0073**; `|feedback|` mediana **0.0228**, cioè **sotto il valore sotto ipotesi nulla che avevo
stimato prima della misura** (~0.5/grado ≈ 0.1).

**Terza lettura, con una precisazione che cambia la frase:** non *«la coppia è piccola»* — a regime
i due termini sono dello **stesso ordine** (0.060 contro 0.042). **La coppia parte sei ordini sotto
il suo valore di regime**, e il rapporto eredita quel transitorio.

### (1.3) Una premessa del mandato va corretta

Il feedback entra nella **stessa somma** della coppia (`coppia += _fb`, `:3129`) e attraversa la
**stessa divisione** — che è per **`M_PH = 1.0`, una COSTANTE**, non per l'inerzia. Questa è la
catena della **FASE** (`phivel`); la correzione dell'inerzia di sei ordini vive in
`_passo_spinoriale`, nel settore dello **SPIN** (`omega_s`). **Due catene separate: quella
correzione non tocca questo rapporto.**

*(E una fragilità annotata: `_cm` misura la coppia **accumulata fin lì**; il twist di `:3154` viene
dopo. Con `TW_SPINORE` spento non manca nulla, ma accendendolo `_cm` misurerebbe una coppia
**parziale** senza che nulla lo segnali.)*

### ⚠ (2) La cosa che non era fra le domande: **`F3` fallisce già adesso**

Ho anticipato nella sonda il criterio `F3` del mandato (`sum(out) == 0`, l'antisimmetria), per
sapere se valesse la pena scriverlo.

```
|sum(out)| / max|out| :   mediana 1.112     MAX 8.441     (errore macchina: ~1e-14)
```

**Non è rumore: è ordine unità.** E la causa è **algebrica, sulla riga**:

```python
np.add.at(out, ii, -flusso / np.maximum(grado[ii], 1e-9))
np.add.at(out, jj,  flusso / np.maximum(grado[jj], 1e-9))
```

Per ogni arco `(a,b)`: `out[a] −= f/g_a`, `out[b] += f/g_b`. Somma = **`f·(1/g_b − 1/g_a)`**,
**zero solo se `g_a == g_b`**. Verifica su un caso minimo (stella, gradi `[3,1,1,1]`, `f = 1`):
previsto `3·(1−1/3) = 2.000000`, **misurato 2.000000**. Controprova con denominatore **simmetrico**
sull'arco: somma **−2.2e-16**, antisimmetria recuperata. *(Il caso «grafo regolare» che avevo messo
come controllo è **degenere** — `sum = 0` ma anche `max|out| = 0` — e non prova nulla: lo dico
perché l'avevo scritto io.)*

**Il docstring dice due cose:** *«coppia **antisimmetrica** ai nodi»* e *«la divisione per il grado
pesato resta locale e **non introduce una manopola**»*.
**La seconda è vera, ed è esattamente la ragione per cui la prima è falsa.** La normalizzazione
messa per **non** introdurre un parametro **distrugge la proprietà che dà senso al termine**.

Con `sum(out) ≠ 0` il termine **inietta coppia netta**, e il segno dell'iniezione dipende dalla
**disomogeneità dei gradi** — una proprietà della **topologia**, non della fisica dello spin.
**È il cricchetto che A7 esclude.**

**Quinto membro della famiglia «un flag che non fa ciò che dichiara»**, dopo `_passo_spinoriale`,
`VERSO_CHI`, `spin_locale`, `TW_SPINORE`. **E qui non è il commento a essere stale: è la PROPRIETÀ
DICHIARATA a non esserci.**

### Il limite di questa misura, dichiarato

**La sonda non riproduce il `2.706`**: gira in-process, 60 passi, senza `--verlet`,
`--calore-scal`, `--deparam-orologio`, e l'esperimento ne faceva 126. Dà media 2086, mediana 1.83.
**Non so attribuire per intero la differenza fra 2086 e 2.706, e non la spiego con un'ipotesi.**

Ma i tre fatti che questa misura stabilisce **non dipendono dalla configurazione**: la popolazione
**non è stazionaria** (quindi la media è comunque lo statistico sbagliato); il rapporto **scende
sotto 1** a maturazione; e **`sum(out) ≠ 0` si dimostra sulla riga**, quindi vale in ogni
configurazione con gradi disomogenei.

### Cosa resta a Luca

1. **`E4b` va riscritto** su una statistica che rispetti la non-stazionarietà.
2. **`F3` ha risposto prima di essere scritto, e ha risposto NO.** Il mandato diceva *«se non è
   zero, la premessa cade»*: **non è zero.** Gli altri criteri misurerebbero un termine di cui già
   sappiamo che non è quello che dichiara.
3. **La domanda vera è cambiata:** se il termine **deve** essere antisimmetrico, il divisore per
   grado va ripensato — e quella è una **legge nuova** (par.10), non una riparazione. Se **non**
   deve esserlo, va corretto **il docstring**, e il termine va descritto per quello che è: una
   **sorgente netta di coppia pilotata dalla disomogeneità dei gradi**.

**`SPIN_FEEDBACK` resta OFF. Mi fermo qui, come ordinato.**

---

## 9.38 — **(A) o (B)? La misura non distingue. Ma (B) cade per dimostrazione, e l'«alternativa» è il codice attuale**

**Data:** 2026-09-17 · `csv/_test_fork/_misura_denominatore.py`, tre varianti, `TAU_A = 2.0`,
60 passi, **un seme**. **Nessuna cura cablata, nessun sigillo, nessun test a semi.**

### La premessa di (B) non regge — dal sorgente, non dalla misura

Il mandato fonda la lettura (B) su *«c'è già una divisione per l'inerzia a valle»*. **Dal disco:** il
feedback ha **una sola** chiamata (`:3113`), finisce in `coppia`, e `coppia` va a `:3197` →
`delta_phivel = … / **M_PH**`, con **`M_PH = 1.0`, una costante globale** (`:206`). L'**unica**
`/inerzia` del file (`:2283`) divide **`correzione`**, un 3-vettore dentro `_passo_spinoriale`,
**non `coppia`**.

**Il feedback vive nel settore della FASE; `omega_s` e `inerzia` vivono in quello dello SPIN e non
lo vedono mai.** Non c'è nessuna doppia divisione da togliere — e togliere `/grado` non toglierebbe
una normalizzazione di due: toglierebbe **l'unica**.

**(B) è esclusa per DIMOSTRAZIONE, non per misura**, che è la distinzione imposta da CLAUDE.md.

### E il criterio cambia: qui `sum(out) = 0` **è** la conservazione

L'avvertenza del mandato — *«`sum(coppia)` non è fisica, ciò che si conserva è `sum(I·ω)` e `I`
varia per nodo»* — **vale per il settore dello spin**. In un settore a **massa uniforme**:

```
d/dt sum(phivel) = sum(coppia) / M_PH    =>    sum(out) = 0  <=>  sum(phivel) si conserva
```

Quindi `G1` non è un criterio di forma: **è la legge di conservazione stessa**. E `L_tot` non è lo
strumento giusto, perché misura un settore in cui il termine non entra.

*(Non l'ho calcolato: il simulatore **non espone l'array dell'inerzia** — è una locale di
`_passo_spinoriale`. Metterci `I = 1` avrebbe dato un `sum(|ω|)` **travestito da `L_tot`**: il
fallback silenzioso che P5 vieta. Riporto `sum(|omega_s|)` col suo nome.)*

### La misura

| | `G1` mediana | `sum\|d_step\|` | `\|deriva\|/scala` | n finale |
|---|---|---|---|---|
| **attuale** | **1.112e+00** | 298.14 | 1.0658 | **548** |
| **senza** | **6.475e-16** | 293.51 | 1.0382 | **564** |
| **simm** | **8.540e-16** | **243.16** | **0.92442** | **554** |

**`G1`: quindici ordini di grandezza.** Il difetto è confermato **ed è il denominatore** — entrambe
le cure lo tolgono esattamente. **Ma proprio per questo `G1` non discrimina.**

`simm` è il migliore su tutte le colonne della conservazione. **E non lo uso per decidere:** guarda
`n finale` — **548 / 564 / 554**. Le tre traiettorie **divergono**, quindi sto confrontando **tre
sistemi diversi**, su **un seme**, senza nullo misurato; e il nullo caotico noto sul conteggio nodi
vale già ~1.4 % mentre qui `n` differisce del **2.9 %**.

> **La misura non distingue (A) da (B), e lo dico invece di sceglierne una.**

### ⚠ L'«alternativa» del mandato è il codice attuale

Il mandato propone *«accumulare `±flusso` senza denominatore, e dividere per il grado DOPO, sul
totale del nodo»*. **È algebricamente identica**, perché `grado[k]` è lo stesso per tutti gli archi
di `k` e **si raccoglie**:

```
out[k] = Σ (±f / g_k)  =  (Σ ±f) / g_k
```

Verificato: **`max|attuale − alternativa| = 5.551e-17`**, e `|sum|/max` vale **7.119e-01 in
entrambe**, contro **2.365e-16** della forma simmetrica. **Lo scambio *sembra* esatto se si guarda
la fase di accumulo, ma la normalizzazione successiva lo rompe di nuovo.**
**L'unico modo di avere `sum(out) = 0` è un denominatore simmetrico sull'ARCO — o nessuno.**

### ⚠⚠ E il difetto era **già dimostrato nel repo**, su un termine gemello

`doc/MAPPA_accoppiamenti_spin.md` (88-96), già committato, dice di `B` (`:2080-2082`):

> *«Il contributo della coppia `(i,j)` al torque su `i` è `(w_ij/deg_i)·cross(…)`; quello su `j` è
> `(w_ij/deg_j)·cross(…)`. Sono opposti **solo se `deg_i == deg_j`**. […] **Quindi `Σ_i L_i` non è
> conservata, per costruzione.** **NB ONESTO:** che non sia conservata si **dimostra**; **quanto**
> non lo sia [non è misurato].»*

**Stesso difetto, stessa causa, altro termine.** La mia `1.112` è la **prima misura di ampiezza** di
qualcosa che nel repo era **già dimostrato in forma**.

**È P1, e l'ho mancato io:** dovevo rileggere quel documento **prima** di trattare il difetto come
nuovo. Il presidio *«quando si apre una domanda nuova, ri-interroga le misure vecchie»* esiste
esattamente per questo caso.

**E la conseguenza supera il termine in esame:** lo schema «dividi per il grado del nodo» compare in
**almeno quattro punti** — `:1367-1368` (il feedback), `:2082` (`B`), `:2294` (`_otw`), `:3154` (il
twist) — **e per il punto precedente «dentro» e «dopo» sono la stessa cosa**. **Non l'ho misurato
sugli altri tre: è un fronte nuovo, e non lo apro dentro questo mandato.**

### Il pregio smentito, e dove sta

Cercato in tutto il repo: l'affermazione sta in **un solo posto**, il **docstring** (`:1336-1341`) —
*«coppia **antisimmetrica** ai nodi»* e *«la divisione per il grado **non introduce una manopola**»*.
**La seconda è vera ed è la ragione per cui la prima è falsa.** Riscriverlo è `G9`, cioè **parte
della cura**: non l'ho toccato.

### Cosa resta a Luca

1. La misura è **indifferente**; ma §1 del mandato **pre-registra** che nel caso indifferente si
   sceglie **(A)**, e (B) è **separatamente esclusa** per dimostrazione. **Se accetti entrambe, (A)
   è quello che resta** — serve il via libera, perché §5.2 dice STOP.
2. **Il denominatore simmetrico non ha oggi una derivazione.** Il candidato indicato, `w`, **non
   funziona**: `flusso = w·imag(ov)`, quindi dividere per `w` lo **cancella** e il peso dell'arco
   sparisce dalla legge. `(g_i+g_j)/2`, `min`, `max`, `sqrt(g_i·g_j)` sono **quattro scelte
   arbitrarie (A1)**.
3. **Il fronte nuovo** dei tre punti gemelli.

**`SPIN_FEEDBACK` resta OFF.**

---

## 9.39 — **Il denominatore era un ERRORE. Tolto, sigillo 12/12. E `G6` dice che la fase è CUCITA**

**Data:** 2026-09-17 · cura in `c4eaded`, sigillo in `d2deb8f`, blob **`11cf103f`** (byte grezzi).
**`SPIN_FEEDBACK` resta OFF di default:** è una **correzione di difetto** (categoria D, par.10),
**non una promozione**.

### Il difetto, e va letto come errore — non come scelta

```python
out[i] -= flusso / grado[i]
out[j] += flusso / grado[j]     # DUE denominatori DIVERSI
```

La somma vale `f·(1/g_j − 1/g_i)`: **zero solo se i gradi coincidono**, e su un grafo disomogeneo
non coincidono mai. Misurato **`|sum(out)|/max|out|` mediana 1.112, MAX 8.441** contro un errore
macchina di `1e-16`. Il termine **iniettava coppia netta**, col verso pilotato dalla
**disomogeneità dei gradi** — una proprietà della **topologia**, non della fisica dello spin.

**`imag(<ψ_i|ψ_j>)` è antisimmetrico per costruzione: la legge era giusta, era la divisione ad
averla rotta.**

### Perché **nessun** denominatore, e non uno simmetrico

Quattro varianti misurate (`eaa402b`). `nudo`, `(g_i+g_j)/2` e `g_i+g_j−2w` portano `G1`
**tutte e tre** all'epsilon (`6.5e-16 / 1.1e-15 / 7.9e-16`): **la correttezza non discrimina.**

E la domanda che giustificherebbe un denominatore d'arco — *«|out| cresce col grado?»* — **non ha
risoluzione su questo grafo**:

```
numerosità per grado (2..9):   1018 | 20 | 10 | 20 | 50 | 30 | 80 | 90
```

**Il ~77 % dei nodi ha grado esattamente 2** — sono i figli della mitosi, che nascono con due archi

> **⚠ RITIRATO il 2026-09-18 — vedi §9.41.** Il «~77 %» e' un **errore di POPOLAZIONE** mio: il `1018` era su **5410** nodi-istanza e l'avevo diviso per **1318**, la somma delle sole colonne stampate. Il valore vero e' **19.85 %**, la distribuzione e' **BIMODALE** (mediana **119**, il **65.57 %** dei nodi ha grado >= 100), e **la misura aveva risoluzione**. Rifatta sul range giusto: il vecchio `/grado` era **INTENSIVO** (pendenza −0.003), `nudo` e' **ESTENSIVO** (+0.878). → `doc/REFERTO_Z24.md`

(fatto già in CLAUDE.md par.9) — e le mediane di `|out|` per grado sono **non monotone** su tutte e
quattro le varianti.

**E la pendenza del fit era un artefatto:** dava `+0.03` per la forma attuale **mentre le mediane
calavano**, perché dominata da una coda di poche decine di nodi. Ho corretto lo strumento perché
riportasse **entrambi**: *una pendenza che contraddice le mediane binnate non si cita come titolo.*

Restano **A1 e par.3**: **nessun denominatore ha zero scelte**; `(g_i+g_j)/2` è una fra quattro
combinazioni, `g_i+g_j−2w` è un oggetto definito ma resta la scelta di quale oggetto usare.

**E l'ampiezza non esplode — è il contrario dell'intuizione:** `|out|` mediano **0.0400 → 0.0223**,
`max|out|` **0.816 → 0.590**. **È più piccolo di prima.** *(Spiegazione plausibile e **non
verificata**: `grado` è il grado **pesato**, non il conteggio, e dividere per un numero minore di
uno **amplifica**. Se fosse giusta, il vecchio `/grado` non normalizzava: amplificava.)*

### Il sigillo — **12/12 PASS**

| | esito |
|---|---|
| **`G1` [BLOCCANTE]** | mediana **6.475e-16**, MAX **2.752e-15** su 64 invocazioni — **era 1.112 / 8.441**: quindici ordini |
| `G2` | al limite **grado pesato = 1**: `max\|A−B\| = 0.000e+00`, **shape uguali** |
| `G3` | coi gradi veri differisce: `0.40874` |
| `G5` / `G5b` | `0.000e+00` / `2.220e-16` |
| `G7` | lift corto **2 su 66** (invocazioni 0 e 6): il transitorio |
| `G8` | 0 NaN, `\|nb\|−1 = 2.2e-16`, CFL **0.400** |
| `G9` | docstring riscritto **con i numeri che lo hanno smentito** |

**`G2` non è scritto come nel mandato, ed era dichiarato prima** (`doc/PREVISIONI_qualitative.md`,
`f3f1ab0`): con `grado[i] = grado[j] = g` la vecchia forma dà `±f/g` e la nuova `±f`, quindi la
byte-identità vale **solo per `g = 1`**. **Col criterio del mandato avrebbe dato un FAIL falso** —
l'undicesimo criterio scritto dal modello mentale invece che dalla misura, e stavolta intercettato
**prima** di girarlo.

### ⭐ `G6` — la cucitura di fase, **che non aveva mai fatto nessuno**

```
|Δ imag(ov)| mediano   : 0.0011042
|imag(ov)| mediano     : 0.034603
RAPPORTO |Δ| / |ov|    : 0.031911      -> la fase si muove del 3 % per passo
CAMBI DI SEGNO         : 0.0035        -> lo 0.35 %, contro un NULLO di 0.50
```

**La fase è cucita.** `imag(ov)` è **continuo** fra passi consecutivi: il termine è una **corrente
orientata vera**, non rumore di gauge travestito. **È la proprietà che rende significativo tutto il
resto**, ed è la prima volta che qualcuno la verifica.

**E il nullo non è zero, è 0.5**: se `imag(ov)` fosse rumore a media zero, **metà** degli archi
sopravvissuti cambierebbe segno a ogni passo. Senza quel nullo, `0.0035` non direbbe niente.

*(Vale la pena metterlo accanto al marchio della BUSSOLA sulle `berry_*`, che sono **morte perché
telescopano**. Qui **non telescopa**: la grandezza sopravvive da un passo al successivo.)*

### `G4` — riportato, **non giudicato**

Deriva di `sum(phivel)` **−118.14** contro **−70.41** pre-cura. **Non è pass/fail:** le due
traiettorie **divergono** (n finale diverso), quindi è un confronto **fra sistemi diversi**, su un
seme, senza nullo misurato. Lo riporto e **non lo interpreto**.

### Cosa la cura **non** fa

- **Non restituisce la proprietà del vecchio docstring:** `out[k]` resta una **somma** su termini
  che crescono col grado. **~~Se sia un difetto non è stato misurabile~~ — RITIRATO il 2026-09-18: era un errore di popolazione mio. È misurabile ed è misurato (§9.41): il vecchio `/grado` era INTENSIVO, `nudo` è ESTENSIVO, e conservazione e intensività sono in conflitto algebrico.**
- **Non tocca gli altri tre punti con lo stesso schema** — `:2082` (`B`), `:2294` (`_otw`), `:3154`
  (twist) — **già dimostrati in forma** in `doc/MAPPA_accoppiamenti_spin.md` e **mai misurati**:
  è `Z24`.
- **Non promuove nulla.** `SPIN_FEEDBACK` resta **OFF di default**.

---

## 9.40 — **A quattro semi `SPIN_FEEDBACK` non produce effetto misurabile. E cadono ENTRAMBI i numeri che avevo citato**

**Data:** 2026-09-18 · 8 run (4 semi × OFF/ON), `TAU_A = 2.0` in entrambi i bracci, 120 passi, con
la cura del denominatore dentro (blob `11cf103f`). **Criterio scritto e committato PRIMA**
(`4d4db99`), non prorogato.

### P6 prima di guardare i numeri

Otto run su otto conformi, `TAU_A` e `SPIN_FEEDBACK` letti **dal blocco `# RUN_PARAMS` di ciascun
CSV**, non dal comando. Quattro semi con **entrambi** i bracci validi: il disegno appaiato ha i tre
gradi di libertà che servono.

### Il risultato: **il segno non è nemmeno concorde**

| seme | n OFF | n ON | **δn** |
|---|---|---|---|
| 5 | 1754 | 1785 | **+31** |
| 11 | 1947 | 1947 | **0** |
| 17 | 1810 | 1813 | **+3** |
| 23 | 1949 | 1890 | **−59** |

```
δ CONTEGGIO NODI :  media  −6.25    SD FRA SEMI  37.84    IC95 ±60.2    -> CONTIENE LO ZERO
δ max|d0|        :  media +14.55    SD FRA SEMI 102.3     IC95 ±162.7   -> CONTIENE LO ZERO
δ max|psi|       :  media +0.887    SD FRA SEMI  2.188    IC95 ±3.482   -> CONTIENE LO ZERO
```

**Recupero medio: `−0.34 %` del braccio OFF.** La media è **negativa**.

È la firma di **C10**, nella sua forma più netta: su un seme un effetto apparente, su quattro il
segno **cambia**.

### I tre nulli **non si scrivono allo stesso modo**

| | IC95 | risoluzione | come si scrive |
|---|---|---|---|
| **δ nodi** | ±60.2 su 1865 | **3.2 %** | **«non sposta il conteggio di più di ~66 nodi»** — il nullo **dice qualcosa** |
| **δ `max\|d0\|`** | ±162.7 su 14.55 | barra **11×** il valore | **«NON MISURATO»** |
| **δ `max\|psi\|`** | ±3.482 su 0.887 | barra **3.9×** il valore | **«NON MISURATO»** |

**Tre righe che dicono «contiene lo zero» e significano due cose diverse.**

### Cadono **entrambi** i numeri che avevo citato — anche quello che usavo *contro* l'ipotesi

Il **`+3.0 punti`** era `1754 → 1833` su un seme, cioè **+79 nodi**: **sta fuori dall'IC95** della
misura a quattro.

E cade anche il **«costo» di +21 punti su `d0`**, anch'esso un seme. Qui `d0` fa
`−7.5 / +160.2 / −79.2 / −15.3`: due semi migliorano, uno peggiora di 4.9 volte. La dispersione è
tale che non si può dire niente — **il che toglie anche l'argomento contrario**: non ho una prova
che il feedback peggiori `d0`.

> **Il mio verdetto precedente — *«ha spostato il problema»* — era costruito su due numeri di un
> seme solo, e nessuno dei due sopravvive.** La formulazione giusta è più povera e più onesta:
> **a quattro semi, `SPIN_FEEDBACK` non produce un effetto misurabile su nessuna delle tre
> grandezze.**

### La lettura pre-registrata che si applica

È la **seconda** delle quattro fissate il 2026-09-17: *«la perdita resta uguale → l'ipotesi cade.
Candidato successivo: `TAU_A` è anche la vita media (`:2265`)»*.

**L'ipotesi «il `−32 %` dipendeva dalla trasmissione staccata» CADE:** riattaccare il feedback — e
riattaccarlo **riparato** — non lo recupera. **Il fronte si sposta su `Z10`**, che era già aperto.

### ⭐ Un controllo gratis che non avevo programmato

**Il braccio OFF del seme 5 dà `1754` nodi, esattamente come nell'esperimento PRE-CURA**
(commit `1347246`). **La cura è inerte a flag spento su un run batch vero di 120 passi**, non solo
nello stub del sigillo: il rito §2.1 confermato sul campo.

*Onestà su cosa prova:* un conteggio identico dopo 120 passi su un sistema caotico è una condizione
**necessaria e molto stringente** — basta `1e-16` per farlo divergere — **ma non è una
dimostrazione di byte-identità**.

### Cosa resta vero di questo giro

**Il valore non è nel risultato dell'A/B: è nella bonifica.**

1. **Il cricchetto è tolto**: `|sum(out)|/max|out|` da **1.112** a **6.5e-16**. Vale a prescindere
   dall'A/B — **un cricchetto è un difetto anche se il termine non produce effetti misurabili**.
2. **`G6`: la fase è cucita** (cambi di segno 0.35 % contro un nullo di 50 %).
3. **`SPIN_FEEDBACK` ora ha un sigillo** (12/12) che prima non aveva.

**Resta OFF di default.** L'A/B non dà nessuna ragione per cambiarlo.

### I limiti, dichiarati

Quattro semi sono il **minimo**: con 8 la risoluzione su δn passerebbe da 3.2 % a ~2 %, quindi **un
effetto vero ma ≤ 1 % resterebbe invisibile a questo disegno**. 120 passi sono ~1/50 della
maturazione di `ramp`. Una sola scena.

---

## 9.41 — **`Z24` misurata: uno dei tre è un cricchetto ATTIVO. E ritiro una mia conclusione: il «77 %» era un errore di POPOLAZIONE**

**Data:** 2026-09-18 · `csv/_test_fork/_misura_Z24.py` · **Nessuna cura eseguita**: il mandato dice
STOP dopo la misura.

### I tre punti **non sono lo stesso schema** — verificato dal sorgente prima di misurare

| punto | accumulo | è uno scambio? | gate | residuo | esito |
|---|---|---|---|---|---|
| **1 — `B`** | `+` su entrambi | **no**, è un **campo medio** | — | `correzione` **2.266** | cricchetto, **ma non per il denominatore** |
| **2 — `_otw`** | `+` su entrambi | **no**, è un Δω | **`TW_SPINORE=False`** | — | **LATENTE** |
| **3 — `twist_nodo`** | **`+twn` / `−twn`** | **sì** | **`FRAME_DRAG=True`** | **6.756** | **⚠ CRICCHETTO ATTIVO = `Z25`** |
| 3-controllo, **nudo** | | | | **0.000e+00 esatto** | **la divisione è l'intera causa** |

**Il ritrovamento è il punto 3:** `FRAME_DRAG = True` **di default**, quindi quel termine **gira in
ogni run mai fatto**, e finisce in `coppia → delta_phivel / M_PH` con `M_PH` **uniforme** — dove
`sum = 0` **è** la conservazione.

**E il punto 1 non si cura col denominatore, misurato:** divisione senza `refl` **2.622**, `refl`
senza divisione **6.507**, denominatore d'arco **3.060**, e **solo togliendo entrambe** si arriva a
**1.379e-15**. **Togliere solo il denominatore peggiora.** La seconda rottura è `refl`, e toglierla
**è una legge nuova**, non una bonifica. *(MAPPA le dichiarava entrambe **in forma**, col suo NB
onesto «quanto non lo sia non è misurato»: ora è misurato.)*

### ⚠ E ritiro una mia conclusione, propagata in cinque posti

Avevo scritto — in `Z25`, nel docstring del simulatore, nelle previsioni, in §9.39 e nel referto dei
semi — che *«il ~77 % dei nodi ha grado esattamente 2, quindi la domanda «|out| cresce col grado?»
non ha risoluzione»*.

**È un errore di POPOLAZIONE — quello che A3 chiama per nome — fatto sul mio stesso conteggio:** il
`1018` era su **5410** nodi-istanza, e l'ho diviso per **1318**, cioè per la somma delle **sole
colonne che avevo stampato** (gradi 2..9).

```
distribuzione VERA (passo 60, seme 5): 549 nodi, 22044 archi
   grado  MEDIA 80.3   MEDIANA 119   MAX 122
   grado == 2    : 19.85 %     grado >= 100 : 65.57 %      -> BIMODALE
```

**I bin che avevo guardato coprivano il 21 % dei nodi. La misura aveva risoluzione — un fattore
60 — e io ho guardato dove non ce n'era.**

### Rifatta sul range giusto, la domanda **ha** una risposta

| variante | `\|out\|` a `g=2` | a `g≥100` | rapporto | pendenza |
|---|---|---|---|---|
| **attuale (pre-cura)** | 0.04885 | 0.04829 | **0.989** | **−0.003 → INTENSIVA** |
| **nudo (cablata)** | 0.001694 | 0.06127 | **36.2** | **+0.878 → ESTENSIVA** |
| media | 0.002333 | 0.04406 | 18.9 | +0.719 |
| linea | 0.001372 | 0.02313 | 16.9 | +0.691 |

**Il vecchio `/grado` rendeva `out` intensiva davvero — ciò che il docstring dichiarava — e nessuna
delle tre cure lo fa.**

### Il compromesso, che è **algebrico** e non negoziabile

- `sum(out) = 0` richiede un denominatore **simmetrico sull'arco**;
- l'indipendenza dal grado richiede il denominatore **del nodo che riceve**.

**Non possono valere insieme.** Il vecchio codice sceglieva la seconda **rompendo** la prima, e non
lo diceva.

**La cura resta giusta su ciò che ripara** — un cricchetto è una violazione di A7, non una scelta di
modello — **ma il suo costo non era «non misurabile»: è misurato ed è grande.** Ai neonati `|out|`
scende di un **fattore 29**; al bulk sale del 27 %.

### Due decisioni a Luca

1. **Curare il punto 3** sapendo del compromesso — non come l'ho fatto io, credendo che la domanda
   non avesse risposta.
2. **Se riconsiderare `nudo`** per `SPIN_FEEDBACK`: coi dati veri `linea` è la **meno estensiva**
   (16.9 contro 36.2). **Lo riporto, non lo propongo:** la cura è committata e sigillata 12/12, e
   cambiarla è una decisione.

### E il limite di §3 del mandato è **chiuso, non aperto**

Il mandato lo registrava come *«serve una topologia a grado basso o variabile»*. **C'è già:**
bimodale, `2` contro `119`. La domanda **era** misurabile ed **è** misurata.

---

## 9.42 — **`Z24` chiusa: uno dei tre era un cricchetto ed è curato, due non lo erano.** E il §3 del mandato era un errore

**Data:** 2026-09-18 · cura in `b376471`, sigillo **8/8** in `1d41a6c`→`_sigillo_twist_nodo.txt`
· blob byte `da216e56`.

### Il §3 del mandato si chiude, non si apre

Il mandato chiedeva di registrare come **aperto** un fronte — *«serve una topologia a grado basso o
variabile»* — **costruito sulla mia conclusione sbagliata del «77 %»**. Quel fronte **non esiste**:
la topologia a grado variabile **c'è già** (bimodale, `2` contro `119`, escursione un fattore 60), e
la domanda **era** misurabile ed **è** misurata. Registrato come **errore del mandato** (`Z28`).

**Una precisazione che serve fra sei mesi.** Luca scrive che *«il ~77 % di grado 2 e il grado medio
~121 non sono in contraddizione»*: **vero in generale, ma non salva il mio numero.** Il `77 %` era
**aritmeticamente sbagliato** — `1018/1318` invece di `1018/5410` — e lo sarebbe stato anche su una
distribuzione uniforme. Il valore vero è **19.85 %**.

**È il quarto errore di popolazione in due giorni**, e il più istruttivo: **il denominatore
sbagliato era visibile nella mia stessa tabella** (le colonne erano `g=2..9` e le ho sommate come se
fossero il totale). **Presidio: il denominatore di una frazione si prende dalla POPOLAZIONE, mai
dalla somma di ciò che si è scelto di stampare.**

### I tre punti — **due non erano cricchetti, ed è un risultato**

| punto | esito | ragione |
|---|---|---|
| **3 — `twist_nodo`** | **CURATO** | scambio `+twn`/`−twn` rotto dalla divisione; **attivo** (`FRAME_DRAG=True`) |
| **1 — `B`/`correzione`** | **non curato** | **due rotture**: togliere il denominatore **peggiora** (2.266→2.622); la seconda è `refl`, **legge nuova** |
| **2 — `_otw`** | **non curato** | **latente** (`TW_SPINORE=False`), e non è nemmeno uno scambio |

### Il sigillo — **8/8**

**`H1` [BLOCCANTE]: `|sum|/max|·|` mediana e MAX = `0.000e+00` su 66/66**, era **6.756 / 8.483**.
**Zero esatto**, non «all'epsilon»: `twn` è sommato e sottratto senza passare per una divisione.
`H2` al limite **grado topologico = 1** (non «gradi uguali»: dichiarato prima). `H3b`:
`sum(nuova) = 2.2e-16` contro `sum(vecchia) = 2.2218`. `H5`: 0 NaN, **CFL 0.400**.

### ⚠ `H4` — il rischio era scritto prima, e la previsione era giusta

Qui `grado` è il **conteggio** (media ~80, mediana 119), **non** il grado pesato di `Z25`: la cura
**moltiplica** il termine invece di dividerlo.

```
|twist_nodo| mediano :  0.231 -> 27.5    fattore 119
max|twist_nodo|      :  0.5   -> 34      fattore 68
previsione ex ante (52823d4): "~10^2 volte più grande"
```

**E il sistema regge comunque** (`max|phivel|` 14.065 contro 14.345 pre-cura): si applica la
**prima** delle tre letture fissate prima. *(`n` finale 548 → 461 e `max|omega_s|` 34778 → 12124:
**riportati, non attribuiti** — traiettorie divergenti, un seme, nessuna barra.)*

**E il vecchio commento diceva che il termine *«emerge nella scala giusta (~0.2 della coppia
principale) senza aggiustamenti»*: quella scala veniva PROPRIO dalla divisione. Era un
aggiustamento, solo non dichiarato.**

### ⚠ `H6` ha prodotto un **FAIL FALSO** — dodicesimo criterio scaduto

Cercava le frasi smentite nel sorgente e falliva trovandole — **ma le trovava perché il commento
nuovo LE CITA come ritirate**, che è esattamente la cosa giusta da fare. **Il criterio non
distingueva «asserito» da «citato come ritirato».** *(E `H6b` cercava una sottostringa spezzata da
un backtick: sbagliato due volte.)*

**Committato col fallimento prima di toccarlo** (par.5), poi riscritto sul **marcatore di ritiro** —
e **può ancora fallire**, se l'affermazione ricomparisse **fuori** dal ritiro.

**Un FAIL falso costa più di un sigillo mancante**: chi legge cerca il difetto nel codice, e il
difetto non c'è.

### La decisione rinviata di proposito — `Z30`

Coi valori veri, `linea` è la **meno estensiva** delle tre forme esatte (**16.9** contro **36.2** di
`nudo`). **Non tocco `Z25`**: è sigillata 12/12, e cambiarla ora significherebbe rifare il sigillo
**su un criterio diverso da quello con cui la scelta era stata fatta**. Si decide **insieme ai due
punti, con lo stesso criterio** — *la coerenza fra i punti vale più che ottimizzarne uno solo*.
**Ora che `Z24` è chiusa, la decisione è sbloccata.**

---

## 9.43 — **I default cambiati erano DUE righe, non una. E il rigiro ha trovato quattro sigilli non ri-girabili**

**Data:** 2026-09-18 · blob `aa84755b` · **Ripresa dopo un riavvio del PC.**

### Lo stato dal disco — due premesse del mandato erano sbagliate

| atteso | **misurato dal disco** |
|---|---|
| HEAD `38975bd` | **`6b045c0`** — la promozione di `SPIN_FEEDBACK` **era già committata** |
| blob `bcb9db5f` | **`cce15c46`** — è il blob **post-promozione** |
| «il cambio dei default non era stato committato» | **lo era**, e il disco era **identico a HEAD** |

**Nessuna modifica a metà sopravvissuta.** I non tracciati erano **solo output** di sigilli, più
`_sigillo_rimozione5_rigiro….txt` a **zero byte** — residuo del job ucciso dal riavvio. Rimossi
perché rigenerabili, **non committati come risultati**.

### I due default — e il secondo è il reperto

```
SPIN_FEEDBACK = False -> True    (già fatto, 6b045c0)
SPINORE_VIVO  = False -> True    (mancava)
```

**L'audit sul codice già committato lo diceva:**

```
:3189   if SPINORE_VIVO and SPINORE and SPIN_FEEDBACK:
        SPINORE_VIVO = False   SPINORE = True   SPIN_FEEDBACK = True
   -> il feedback GIRA nel default?  NO      manca: ['SPINORE_VIVO']
```

**Accendere solo `SPIN_FEEDBACK` lo lasciava ACCESO MA INERTE — e inerte in silenzio:** il metodo non
veniva nemmeno chiamato, quindi **nemmeno i contatori A8 sarebbero scattati**, perché stanno **dentro**
quel blocco. È la famiglia «cablato ma muto» (`VERSO_CHI`, `_passo_spinoriale` «ORFANO»,
`spin_locale`, `TW_SPINORE`, la FASE 5 inerte al 95.33 % **per mesi**) — **stavolta intercettata
prima che accadesse**, e da uno strumento scritto apposta.

**I quattro rami dell'avviso sono stati esercitati**, non dedotti: default nudo → *gira*;
`--senza-spinore-vivo` → *non gira*; `--senza-spin-feedback` → *diagnostico*; `--spinore-vivo` →
*no-op dichiarato che non rompe i comandi già scritti*.

**E ho corretto un difetto nel mio stesso avviso:** stampava *«manca `--spinore-vivo`»*, ma quel flag
è ora un **no-op** e a spegnere è `--senza-spinore-vivo`. **Un avviso che indica il flag sbagliato
manda chi legge a cercare la causa dove non è.**

> ⚠ **E va detto chiaro: `SPINORE_VIVO = True` non è mai stato validato COME DEFAULT.** Le campagne
> lo passavano **da fuori**, quindi la *configurazione* era la stessa, **ma nessun sigillo è mai stato
> girato con questo valore come default di modulo.** È scritto nel commento del flag.

### Il rigiro — **52 PASS, 0 FAIL nei sei gruppi sani**

| gruppo | esito |
|---|---|
| `V1` `_sigillo_d_arco` | **8/8** |
| `V2-V5` `_sigillo_taup_causale` | **8/8** |
| `V6-V10` `_sigillo_rep_spinta` | **12/12** |
| `Y5` `_sigillo_Y5_riscritto` | **4/4** |
| `F/G` `_sigillo_denominatore` | **12/12** |
| `H` `_sigillo_twist_nodo` | **8/8** |

### ⚠ E quattro sigilli non sono più ri-girabili — **una sola causa**

`_sigillo_inerzia`, `_sigillo_calcpsi_T1`, `_sigillo_calcpsi_T2`, `_sigillo_rimozione5` caricano una
copia **PRE** del simulatore da `SC = os.environ.get("SCRATCH", HERE)` — **lo scratchpad di sessione,
che non è nel repo.** Il riavvio l'ha cancellato.

- **`_sigillo_inerzia`: `Y6` FAIL FALSO** — legge un PRE vuoto, conta `0` usi, **fallisce su codice
  corretto**;
- **`_sigillo_calcpsi_T1`: `[run pre FALLITO rc=2]` → 0/1 FAIL**;
- **`_sigillo_calcpsi_T2`: modalità ridotta** — un solo verdetto, `Q3` e `Q6` dipendono dal PRE;
- **`_sigillo_rimozione5`: SI SCHIANTA** (`FileNotFoundError`) — **la modalità peggiore**, già
  catalogata col caso dello Strato 1: *«NON FALLIVA: SI SCHIANTAVA»*.

> **È `par.5-quinquies` applicato ai riferimenti dei sigilli stessi, e il riavvio l'ha DIMOSTRATO
> invece che argomentato.** Un sigillo che non si può rigirare non protegge nulla.

**E il difetto non è solo il file mancante: tre di essi DEGRADANO IN SILENZIO** —
`pre_src = "" if not exists` trasforma un riferimento assente in **un confronto contro il vuoto**,
che poi produce un FAIL su codice sano. **Un riferimento mancante deve RIFIUTARE, non degradare.**

**Meccanismo proposto** (`Z31`) — e **dichiaro che finché non è cablato resta una proposta, non un
presidio**: il PRE **non si conserva, si DERIVA** con `git cat-file -p <commit>:soliton_simulator.py`
in **binario**, tramite un helper in `csv/_presidio.py` che **esce con errore** se quel commit non è
nel repo. Il riferimento resta pinnato da **un hash — l'unica identità che non mente** — e non costa
500 KB per sigillo. *(La convenzione esiste già: `_old_sim_pre_*.py` sono committate. Questi quattro
non l'hanno seguita.)*

**Non riparati in questo giro, per ordine del mandato. Nessuno dei quattro è una regressione fisica.**

### Aperto per Luca — `Z30`

`nudo` (**36.2**) contro `linea` (**16.9**) per il denominatore di `SPIN_FEEDBACK`. **Ora che `Z24` è
chiusa è decidibile. Riportata, non decisa.**

---

# 9.44 — **RELAZIONE COMPLETA A CLAUDE WEB: dal giro di `Z24` al riavvio, e la DOMANDA aperta**

**Data:** 2026-09-18 · **Branch** `fork-su2` · **HEAD** `a2a0445` · **blob byte** `aa84755b`
**Scritto perché una domanda senza il suo ragionamento, per chi legge solo il repo, non è mai stata
posta** (nuova regola `par.5-sexies` in `CLAUDE.md`).

> **Claude web non ha la conversazione: ha i file.** Questo paragrafo esiste per dargli l'arco
> intero senza doverlo ricostruire dai commit.

---

## 1. L'ARCO, in ordine

### 1.1 — `Z24`: i tre punti «collo stesso schema» — **due non lo erano**

Il giro precedente aveva curato `SPIN_FEEDBACK` (`Z25`: tolto un denominatore che rompeva
l'antisimmetria). `Z24` chiedeva se lo stesso difetto fosse in altri tre punti. **Misurato, non
assunto:**

| punto | accumulo | esito |
|---|---|---|
| **1 — `B`/`correzione`** | `+` su entrambi → **non è uno scambio** | cricchetto (**2.266**) **ma non per il denominatore** |
| **2 — `_otw`** | `+` su entrambi, ed è un Δω | **LATENTE** (`TW_SPINORE=False`) |
| **3 — `twist_nodo`** | **`+twn`/`−twn`** | **CRICCHETTO ATTIVO** (`FRAME_DRAG=True`) |

**Il punto 1 ha DUE rotture indipendenti**, e la misura lo dimostra: togliere solo il denominatore
**peggiora** (2.266 → 2.622); un denominatore d'arco **peggiora** (3.060); solo togliendo **anche**
la riflessione `refl` si arriva a **1.379e-15**. **Toglierla è una legge nuova, non una bonifica.**

**Il punto 3 è stato curato** (`nudo`), **sigillo 8/8**, con `H1 = 0.000e+00` esatto su 66/66.

### 1.2 — **Un mio errore, ritirato: il «77 %»**

Avevo scritto, in cinque posti, che *«il ~77 % dei nodi ha grado 2, quindi la domanda «|out| cresce
col grado?» non ha risoluzione»*. **Errore di POPOLAZIONE:** `1018/1318` invece di `1018/5410` — il
denominatore era **la somma delle sole colonne che avevo stampato**.

**Distribuzione vera: 19.85 % a grado 2, 65.57 % a grado ≥ 100, mediana 119. È BIMODALE.**
**La misura aveva risoluzione — un fattore 60 — e io avevo guardato dove non ce n'era.**

**Quarto errore di popolazione in due giorni.** Presidio che ne discende: *il denominatore di una
frazione si prende dalla POPOLAZIONE, mai dalla somma di ciò che si è scelto di stampare.*

### 1.3 — **Il compromesso che ne è emerso, ed è algebrico**

Rifatta sul range giusto, la domanda ha una risposta netta:

| variante | `\|out\|` a `g=2` | a `g≥100` | rapporto | lettura |
|---|---|---|---|---|
| **pre-cura** (`/grado`) | 0.04885 | 0.04829 | **0.989** | **INTENSIVA** |
| **`nudo`** (cablata) | 0.001694 | 0.06127 | **36.2** | ESTENSIVA |
| `media` | 0.002333 | 0.04406 | 18.9 | ESTENSIVA |
| **`linea`** (`g_i+g_j−2w`) | 0.001372 | 0.02313 | **16.9** | ESTENSIVA |

> **`sum(out) = 0` richiede un denominatore SIMMETRICO SULL'ARCO; l'indipendenza dal grado richiede
> quello DEL NODO CHE RICEVE. Non possono valere insieme.**
> Il vecchio codice sceglieva la seconda **rompendo** la prima, **e non lo diceva**.

### 1.4 — I default: **erano DUE righe, non una**

`SPIN_FEEDBACK = True` **da solo non basta**. Il ramo è
`if SPINORE_VIVO and SPINORE and SPIN_FEEDBACK`, e `SPINORE_VIVO` era `False`: il feedback sarebbe
stato **acceso e inerte, in silenzio** — nemmeno i contatori A8 sarebbero scattati, perché stanno
**dentro** quel blocco. **Famiglia «cablato ma muto», intercettata prima che accadesse** da uno
strumento scritto apposta (`csv/_test_fork/_audit_default.py`).

**Promosso in `COMPONENTI_PROMOSSE.md` sezione H — NON in A** — con la dicitura:
**«attivo per DECISIONE, su basi di FORMA — l'A/B a quattro semi NON ha mostrato un effetto»**, e
con l'ammissione che **dei tre criteri di §10 ne soddisfa due**: il ③ («la sua assenza è un
difetto») è **argomentato, non misurato**.

### 1.5 — Il riavvio, e cosa ha dimostrato

**Niente di committato è andato perso.** Ma ha cancellato lo **scratchpad di sessione**, e con esso
il termine di paragone di **quattro sigilli**:

- **`_sigillo_inerzia`: `Y6` FAIL FALSO** (legge un PRE vuoto, fallisce su codice corretto);
- **`_sigillo_calcpsi_T1`: `[run pre FALLITO rc=2]`**;
- **`_sigillo_calcpsi_T2`: modalità ridotta**;
- **`_sigillo_rimozione5`: SI SCHIANTA.**

> **Il riavvio ha DIMOSTRATO `par.5-quinquies` sui riferimenti dei sigilli invece di argomentarlo:
> un sigillo il cui termine di paragone sta in una cartella temporanea non è ri-girabile, e un
> sigillo che non si può rigirare non protegge nulla.**

**E tre di essi degradano in silenzio** (`pre_src = ""`): un riferimento assente diventa **un
confronto contro il vuoto**. **Deve rifiutare, non degradare.**

**Il rigiro dei sei gruppi sani: 52 PASS, 0 FAIL, 0 crash.** Ma **la copertura è PARZIALE**, e non
dico «sigilli passati».

---

## 2. ⚠ LA DOMANDA APERTA — **`Z30`, e adesso è decidibile**

**Domanda, in una riga:**

> **Il denominatore dei termini d'arco dev'essere `nudo` (zero scelte, ma ESTENSIVO 36.2×) oppure
> `linea` = `g_i+g_j−2w` (una scelta, ma il MENO estensivo: 16.9×)?**

### Perché non l'ho decisa io

Perché **le due scelte vanno fatte insieme, con lo stesso criterio** — `SPIN_FEEDBACK` (`Z25`) e
`twist_nodo` (`Z27`) — e perché la cura di `Z25` è **committata e sigillata 12/12**: cambiarla ora
significherebbe **rifare il sigillo su un criterio diverso da quello con cui la scelta era stata
fatta**. *La coerenza fra i punti vale più che ottimizzarne uno solo.*

### Cosa pesa da una parte e dall'altra — **tutto già misurato**

| | **`nudo`** (attuale) | **`linea`** = `g_i+g_j−2w` |
|---|---|---|
| antisimmetria (`G1`/`H1`) | **esatta** | **esatta** — non discrimina |
| scelte arbitrarie (A1, §3) | **ZERO** | **una**: quale oggetto d'arco usare |
| estensività (`g=2` → `g≥100`) | **36.2×** | **16.9×** ← il meno peggio |
| ampiezza `max\|out\|` | 0.590 | **0.169** |
| derivazione | «nessun denominatore» non richiede derivazione | **è il grado dell'arco nel grafo linea**: un oggetto definito, non una combinazione scelta fra media/min/max |

**Nessuna delle due recupera l'intensività** che il pre-cura aveva (0.989): quella richiede un
denominatore **nodale**, che **rompe la conservazione**. Il compromesso non si aggira.

### Il criterio di chiusura, scritto adesso

> **Una decisione esplicita fra *«esattezza senza scelte»* e *«esattezza + minima estensività»*,
> presa con un criterio dichiarato PRIMA, e applicata a ENTRAMBI i punti (`Z25` e `Z27`) nello
> stesso giro** — con il rigiro dei due sigilli, `F/G` e `H`.

### ⚠ E una cosa che NON so, e che potrebbe cambiare la risposta

**Non è stato misurato se l'estensività sia un difetto.** Sappiamo *quanto* i termini crescono col
grado; **non sappiamo se crescere col grado sia sbagliato.** In un modello relazionale un nodo più
connesso partecipa a più relazioni: **potrebbe essere la fisica.**

**Se qualcuno sa rispondere a questo, la scelta fra `nudo` e `linea` diventa una conseguenza invece
che una preferenza.** È la domanda che mi interessa di più, ed è aperta a Claude web quanto a Luca.

---

## 3. GLI ALTRI FRONTI CHE RESTANO APERTI, con la loro condizione

- **`Z31`** — i quattro sigilli non ri-girabili. **Meccanismo proposto** (derivare il PRE da
  `git cat-file` in binario, con rifiuto esplicito se il commit manca) **ma NON cablato: finché non
  lo è, resta una proposta, non un presidio.**
- **`Z9`** — `ramp` arriva al pieno a **~5000 passi**, i run ne fanno 120-500: **ogni misura di
  questo tipo vive nel transitorio.** Non toccata per ordine.
- **`SPINORE_VIVO = True` non è mai stato validato COME DEFAULT** — le campagne lo passavano da
  fuori. I sei gruppi sani lo coprono, i quattro rotti **no**.
- **Il punto 1 di `Z24`** (`refl`): **legge nuova**, non bonifica.
- **4 semi sono il minimo**: un effetto vero ≤ 1 % è **invisibile** a questo disegno.

---

## 9.45 — **La premessa di Luca è vera e la compensazione esiste. Ma la scelta del denominatore NON si vede a valle**

**Data:** 2026-09-18 · un seme (5), 60 passi, una scena · `csv/_test_fork/_estensivita_grado.py`
**Task history scritto e pushato PRIMA della misura:** `75a15bc`.

### La speculazione, e cosa ne è rimasto

Luca: *«il grado è un proxy della densità; un nodo denso ha inerzia alta, quindi ruota di meno a
parità di coppia; l'estensività è già compensata dall'inerzia, e normalizzare anche il feedback la
compenserebbe due volte. Quindi `nudo` — ma va misurato.»*

**Tre risultati, e il terzo cambia la domanda.**

### ① «grado alto = regione densa» — **confermato, e non era un fatto stabilito**

`corr(grado, rho_sorgente) = +0.79`; fra le due mode il rapporto è **637×** (`0.00228` a `g=2`
contro `1.453` a `g≥100`). **Era una premessa. Adesso è misurata.**

### ② La compensazione **esiste ed è grande — nel settore dello SPIN**

Contrasto `rho/peq`: **×295** verso il bulk. E `omega_s` **decresce col grado di un fattore ~130**
(`56.2` a `g=2` contro `0.428` a `g≥100`). **È esattamente il segno che l'argomento prevede: più
denso → più inerzia → ruota meno.**

*(Nota di metodo: su `rho/peq` la correlazione di Pearson dà `+0.20`, che sembra debole, **ma è la
statistica sbagliata** — su una distribuzione bimodale con code pesanti è dominata dalla varianza
dentro il bulk. **Il rapporto fra le mode, `295×`, è quella giusta.** È la lezione già pagata in
`Z27`.)*

### ③ ⚠ **Ma la scelta del denominatore non arriva all'osservabile**

| `phivel` *(la catena dove il feedback ENTRA)* | `g=2` | `g≥100` | rapporto |
|---|---|---|---|
| **PRE** (`/grado`, termine **intensivo** 0.989) | 1.938 | 9.478 | **4.891** |
| **POST** (`nudo`, termine **estensivo ×36.2**) | 1.893 | 9.186 | **4.853** |

**0.8 % di differenza** — e il confronto è fra i **due estremi disponibili**: un fattore **37** sul
termine produce **0.8 %** sull'osservabile.

> **Il bias di grado di `phivel` precede la cura, sopravvive alla cura, e non è il denominatore a
> produrlo.** La spiegazione più semplice, e la do come tale: `coppia` contiene altri termini —
> `_coppia_interferenza`, la repulsione, `twist_nodo` — **e sono quelli a dominarne la struttura in
> grado**. Coerente con l'A/B a quattro semi, che non mostrava effetto.

### Cosa ne segue per `Z30` — **e correggo come l'avevo posta**

**Avevo portato a Luca `36.2` contro `16.9` come la posta in gioco. Quei numeri sono sul TERMINE; a
valle valgono `0.8 %`.** La scelta andava presentata dicendo **su cosa** si misurano.

- **il criterio «quale forma è meno estensiva» NON discrimina**: l'osservabile non lo vede;
- **restano `A1` e §3 — `nudo` non richiede nessuna scelta** — ma ora non è solo un principio:
  **è una misura che dice che l'alternativa non compra niente**;
- **`linea` non è «più sicuro»: è una scelta in più senza un guadagno misurabile.**

**La speculazione regge, con una precisazione:** la compensazione è **reale e misurata**, ma agisce
sul settore dello **spin**, non su quello in cui il feedback entra. **Il feedback non ha bisogno di
essere normalizzato — non perché l'inerzia lo compensi, ma perché la sua forma non arriva
all'osservabile.**

### La domanda nuova che ne nasce, **non misurata**

**Il bias di grado di `phivel` (`×4.9`) è esso stesso un difetto? Da dove viene?** Candidati:
`_coppia_interferenza`, la repulsione, `twist_nodo`. **Aperta.**

### I limiti

Un seme, 60 passi, una scena. **PRE e POST divergono**: i valori assoluti non si confrontano fra i
due giri — **ciò che si confronta è il rapporto fra le mode DENTRO ciascun giro**, ed è per questo
che la misura è disegnata così. E `omega_s` a `g=2` vale 42-56 contro 0.43 nel bulk: i neonati
ruotano in un regime completamente diverso, **non interpretato** — è il settore aliasato, `Z9`.

---

## 9.46 — **`Z9` rimisurata sul blob attuale: INTATTA (+2.8 %). E il meccanismo che poteva cambiarla è bloccato da una normalizzazione**

**Data:** 2026-09-18 · blob `72acd6aa` · un seme (5), 120 passi, **due scene** ·
**task history scritto e pushato PRIMA:** `93308af` · strumento `csv/_test_fork/_rimisura_Z9.py`,
**lo stesso usato le due volte precedenti**.

### Il rilievo di Luca era corretto

Il numero di `Z9` era del blob `a8f1b2f4` — **prima** di `Z25`, `Z24/Z27` e dei due default. **E il
meccanismo che descriveva esiste tutto:** `eta += dt_n`, `dt_n = DT·r`, `r = ritmo()` dipende da
`psi`, e il feedback ora gira e cambia `psi`.

### Il numero — **`Z9` regge**

| | `ramp` a 1 / 60 / 120 | `ramp = 1` al passo |
|---|---|---|
| **storico** | 0.0002 / 0.0106 / 0.0217 | **~5526** |
| **(A) scena originale** *(l'unico confronto lecito)* | **0.0002 / 0.010232 / 0.021151** | **5680** → **+2.8 %** |
| **(B) scena del batch** *(il sistema che gira davvero)* | 0.0002 / 0.0099 / 0.0199 | **6049** |

**La previsione ex ante era «invariato entro un fattore ~2»: è entro il 3 %.**
**E il numero da citare d'ora in poi è quello della scena (B).**

### ⭐ Il perché non si è mosso — **P4, verificato non dedotto**

`ritmo()` (`:2043-2049`) normalizza su `median(|f|)`, e con `TEMPO_PROPRIO_ORIENTATO = False`
(default) `f = |signed| ≥ 0`, quindi `median(x) = 1` esatto e la mappa `x → r` è monotona.

**Misurato: `median(r) = 1.0` a meno di `~1.4e-4` in 245 chiamate su 246.** *(L'unica eccezione è il
primo passo, `f` identicamente nullo, dove `med` cade sul pavimento `1e-9`.)*

> **`median(dt_n) = DT` esattamente ⟹ l'incremento MEDIANO di `eta` è PINNATO PER COSTRUZIONE, e il
> meccanismo è bloccato al PRIMO ORDINE.**

È **C12 — ma la condizione andava verificata, non citata**: con `--tempo-proprio-orientato`
l'ancoraggio **cadrebbe**, perché `f` sarebbe firmato mentre `med` resta `median(|f|)`.
**Ciò che resta libero è la forma della distribuzione di `r` e la popolazione: insieme valgono
`+2.8 %`.**

### ⚠ E due correzioni ai miei stessi criteri, **in due giri consecutivi**

1. Avevo scritto il criterio P4 col **MASSIMO**: dava `scarto MAX da 1.0 = 1.000e+00`, che letto da
   solo direbbe *«l'ancoraggio non c'è»* mentre i numeri accanto lo smentivano. **Il massimo
   descriveva la coda, non la popolazione** — stessa forma di `A3c` e della pendenza di `Z27`.
2. Corretto in **frazione**, ho messo la soglia a `1e-6` e ho etichettato **116 chiamate su 246**
   come *«transitorio degenere»*. **Sono `0.999857 … 0.999919`: `1.0` a quattro cifre.** La soglia
   era troppo stretta e l'etichetta sbagliata.

**In un giro dedicato a verificare un ancoraggio, ho sbagliato due volte lo statistico con cui lo
verificavo.** È la famiglia che continuo a catalogare, e stavolta è mia due volte di fila.

### `R6` regge, e un numero annotato

`_pesi()` **12 per passo** (rif. 16), **861 PRIMA / 624 DOPO** la scrittura della cache → **gira
ancora a cavallo: `R6` regge.** Per chiamante: `stato_crossover` 1354, `step` 123, `calcola_psi` 8.

**Fallback su `_cs_nodo_prev`: 1.2121 %** — **piccolo ma non nullo, e non l'ho interpretato**: manca
il confronto col valore della rimisura precedente. **Annotato come da verificare.**

### Cosa ne segue

- **`Z9` non cambia nessuna conclusione**: resta che i run da 120-500 passi vivono nel transitorio —
  a 120 passi il sistema ha vissuto **~1/50** della maturazione;
- **`Z9` non precludeva `Z30`**, e ora si può dirlo con un numero misurato sul blob attuale invece
  che su uno di due generazioni fa.

### I limiti

Un seme, 120 passi. **Le due scene non si mescolano** e danno `5680` contro `6049` (**+6.5 %**):
è la differenza di metodo già registrata.

---

## 9.47 — **La mediana in `ritmo()` è ENTRAMBE: normalizzazione *e* gauge. `Z9` non si cura da lì (A4). E il gauge è DEGENERE un passo su 31**

**Data:** 2026-09-18 · blob `72acd6aa` · un seme (5), 120 passi · **nessun cablaggio**
**Task history scritto e pushato PRIMA:** `bb058c0` · `csv/_test_fork/_mediana_ritmo.py`

### La domanda era: normalizzazione o gauge? — **tre prove, due risposte**

| prova | esito |
|---|---|
| **(a) dimensionale** | `f = |Δangolo/DT|` ha dimensione **`1/T`** → la divisione **serve** all'adimensionalità, **non è eliminabile** → **normalizzazione** |
| **(b) strutturale** | il ritorno è `1 + TAU_LOC·(r/r_unit − 1)`, **una deviazione da un riferimento**; e il docstring dice testualmente *«ancorata alla mediana globale come **gauge**»* → **gauge** |
| **(c) di consumo** | `r` **non è mai** usato come rapporto fra nodi: `dt_n = DT·r`, `eta += dt_n`, `alpha = 1−exp(−dt_n/tau)`, `delta_phivel` — **tutti usi in valore assoluto**, e **nessuna soglia** usa `r` direttamente → **il gauge conta** |

> **È ENTRAMBE.** La quarta lettura, quella che avevo aggiunto al mandato **prima** di misurare:
> *«una normalizzazione che si è portata dietro un gauge»*. **La domanda come alternativa secca era
> mal posta.**

### Conseguenza — **`Z9` non si cura da `ritmo()`**

`dt_n`/`dt_e` alimentano `eta` (cioè `Z9` stessa), `alpha` dello Strato 1, `delta_phivel`, `_rep`,
il termostato. **Cambiare `r_unit` riscala TUTTI i tempi propri locali.** Toglierla rompe
l'adimensionalità; sostituirla **cambia l'unità di misura del tempo**. **È A4, e va deciso come
tale — non come una bonifica.**

*(Se si volesse farlo: serve una scala **locale, derivata, di dimensione `1/T`**. Candidato `cs/d`,
l'inverso del tempo-luce del nodo. **Riportato, non proposto:** sceglierlo **è** scegliere un gauge.
E l'architettura lo ammette già — il ramo `TEMPO_SEGNO` a `:2027` ritorna `1 + (twn/deg)/PHI_CRIT`,
locale e normalizzato da una costante derivata: **è il pattern di `cs_floor`/`Lam`**, anche se è una
legge diversa.)*

### `2.4` — **la terza lettura non si applica al ramo vero**

`median(|f|)` per quarti, **ramo 4π (quello delle campagne)**: **0.0254 → 0.0201 → 0.0228 → 0.0358**
— **×1.4 in 120 passi, quasi piatta.** È il caso che avevo scritto come **peggiore**: *«una costante
mascherata da statistica»*. *(Sul ramo scalare 2π variava ×8.4 — ma quel ramo nessuno lo gira.)*

### ⚠ Il reperto che non cercavo — **il gauge è degenere 1 passo su 31**

```
median(|f|) ESATTAMENTE ZERO : 4 invocazioni su 126  (3.2 %)   [ramo 4π]
```

**Accade anche a `n = 451`**: più della metà dei nodi ha variazione di fase **esattamente nulla** in
quel passo. Allora `med` cade sul **pavimento `1e-9`**, `x` esplode, e **`r` diventa BINARIO** — `√2`
per i non nulli, `1.414e-06` per gli altri.

> **Il pavimento, messo come protezione, diventa il parametro fisico.** Stessa famiglia del `1e-6`
> sull'inerzia e del `0.05` su `_tau`. **Difetto indipendente dall'ancoraggio, mai registrato.**

### E ciò che resta libero — **lo spread è grande, ma piatto**

`median(r) = 1.000000000` per identità. Ma la **dispersione `p95−p05` vale `1.267`** su una mediana
di `1.0`: **`r` spazia su un intervallo largo quanto il suo stesso valore centrale** — e **non
cresce** (per quarti `1.216 → 1.302`).

> **È il CENTRO a essere fisso, non la fisica.** L'ancoraggio toglie che il *nodo tipico* acceleri
> **rispetto a sé stesso**, non la differenza **fra** nodi.

### ⚠ E un errore mio, il secondo di questa classe in due giri

**La sonda ha misurato il ramo sbagliato:** `CAMPO_SPINORIALE = False`, **126/126 invocazioni sul
ramo scalare 2π** — una configurazione che **le campagne non usano**. Stessa classe di
`--cs-dinamico` spento (`doc/REPERTO_cs_dinamico_spento.md`).

**E cambiava i numeri:** gli zeri da `11.1 %` a `3.2 %`, la scala di `f` da `3.04` a `0.0280` — **un
fattore 100**. Rifatta sul ramo vero; il ramo 2π resta in
`csv/_test_fork/_mediana_ritmo_ramo2pi.txt` perché **il confronto fra i due è informativo**.

**Nel task history avevo elencato cosa non sapevo, ma non avevo messo «con quale configurazione
misuro»** — ed è la domanda che viene prima di tutte. **`_rimisura_Z9.py` lo stampa dal passo 0:
andrebbe fatto ovunque.**

---

## 9.48 — **`Z33` non è un difetto del GAUGE: è un difetto di ORDINE/SNAPSHOT. E il mandato aveva il segno sbagliato**

**Data:** 2026-09-18 · blob `72acd6aa` · un seme (5), 126 passi, **nessuna cura**
**Task history scritto e pushato PRIMA:** `aff0df6` · `csv/_test_fork/_gauge_degenere.py`

### (A) Sono nel percorso fisico — **la lettura «artefatto» è esclusa**

`126/126` invocazioni vengono da **`step()`**, nessun diagnostico; le 4 degeneri **alimentano `dt_n`
e quindi `eta`**.

### (B) Ma `f` non ha mediana piccola: **è IDENTICAMENTE NULLO**

| passo | n | ramo | frazione `f=0` | `max\|f\|` | `snap ==` | `len ps/psp` |
|---|---|---|---|---|---|---|
| 0 | 80 | 2π | **1.0000** | 0 | **True** | 80 / −1 |
| 1 | 80 | 4π | **1.0000** | 0 | **True** | 80 / 80 |
| 6 | 440 | 2π | **1.0000** | 0 | **True** | **440 / 80** |
| 7 | 440 | 4π | 0.9818 | 3.55e-13 | False | 440 / 440 |

**Non c'è una statistica che collassa: non c'è variazione da misurare. Il pavimento `1e-9` non
c'entra.**

**Due cause, entrambe confermate, entrambe trovate leggendo `step()` prima di misurare:**

1. **snapshot confrontato con sé stesso (3/4)** — `_psi_spin_prec` si aggiorna a `:3099-3101`, cioè
   **dopo** `ritmo()`;
2. **lunghezze disallineate (passo 6)** — `440/80` dopo l'iniezione delle masse: il guard di `:2038`
   fallisce, si cade sul 2π, e lì anche `_psi_prec` è corto → scatta il **ramo di sicurezza `:2028`**
   (`np.ones(n)`). **Terzo membro della famiglia `C11`/`C7`.**

### (C) Transitorio, senza ambiguità

Passi **0, 1, 6, 7**. **Zero dopo il passo 20.** **Non coincidono con le mitosi** (nati = 0):
coincidono con le **due discontinuità della popolazione** — l'avvio e l'iniezione delle tre masse.

### (D) La dilatazione sparisce — **ma verso il BASSO**

| gruppo | `std(r)` | `fraz r>1.4` | `fraz r<1e-5` |
|---|---|---|---|
| **DEGENERI** | **0 ESATTO** | **0.0000** | **0.4909** |
| SANI | 0.4146 | 0.0926 | 0.0000 |

**`std(r) = 0` esatto: tutti i nodi allo stesso ritmo.** Ma **il mandato prevedeva `r → ±1`
(`x → ∞`)**: misurato il contrario. Se `f` è **identicamente nullo**, `x = 0`, quindi
`r ≈ 1.414e-06`.

I quattro si dividono in **due regimi opposti**: passi 0 e 6 → `r = 1.0` (ramo di sicurezza);
**passi 1 e 7 → `dt_n = DT × 1.4e-06`, cioè il tempo proprio si ferma per tutti.**

**Lo avevo previsto nel task history, prima di misurare.** Averlo scritto prima è ciò che rende la
correzione al mandato credibile invece che comoda.

### Verdetto — **la seconda lettura, e la seconda metà della quinta**

`Z33` è **transitorio, confinato, con cura opzionale**. E la quinta lettura che avevo aggiunto
diceva: *«se `f` è identicamente nullo e la causa è lo snapshot → è un difetto di ORDINE, non di
gauge, e cambierebbe tutto il quadro»*. **È esattamente così.**

> **`Z33` va spostata fuori dalla famiglia `A3` in cui l'avevo messa io.**

### Il §4 del mandato cade, **e con un numero**

`eta` non cresce in **2 passi su 126 = 1.6 %**, tutti nel transitorio iniziale. **Impatto su `Z9`
≤ ~2 %** — dentro il `+2.8 %` già misurato e dentro il `+6.5 %` fra le due scene.
**Rimisurare `Z9` non cambierebbe nulla di leggibile.**

### Se si curasse — **e non è il gauge**

1. una guardia che **rilevi e DICHIARI** `psi_spin == _psi_spin_prec` (A8);
2. **estendere lo snapshot con la popolazione** — **la stessa cura di `C7`/`C11`**.

**Nessuna delle due è una decisione di gauge**, quindi non ricade nel §3 del mandato. **Riportate,
non proposte**, e la cura resta **opzionale**: 4 passi su 126, tutti nel transitorio.

### Il limite

I quattro eventi sono legati a **due discontinuità specifiche di questa scena**. **Il `3.2 %` è
della scena, non del sistema.**

---

## 9.49 — **Nessuna delle due vie cura `Z33`. La cura è il contatore. E `K7` apre un difetto più grande del primo**

**Data:** 2026-09-18 · blob byte `94b6cc29` · un seme (5), 126 passi · **nessuna cura cablata**
**Task history scritto e pushato PRIMA** · `csv/_test_fork/_Z33_due_vie.py`

### La via (1) è il difetto, non la cura — **verificato dal sorgente**

`psi_spin` è assegnato in **un solo punto** (`:2693`, dentro `calcola_psi()`); `ritmo()` consuma a
`:3124`, **all'inizio di `step()`**, e lo snapshot si aggiorna a `:3132`, **dopo**.

> **Il consumo legge già uno stato `t−1`: l'ordine attuale rispetta A6.** Spostare l'aggiornamento
> confronterebbe `psi_spin` **con sé stesso** → `f = 0` per costruzione, sempre.
> **Se avessi eseguito il mandato alla lettera avrei *introdotto* il difetto che dovevo curare.**

### La via (2) non cura, **e il conto lo dice**

`semina()` non estende `_psi_spin_prec` (voce **H**); `_eredita_spinore_figli` lo estende **solo per
la mitosi**, ed è giustificato — il figlio nasce dal padre. **Ma `nuova_massa` crea nodi senza
genitore.**

```
all'iniezione:  n 80 -> 440    NODI NUOVI 360 = 81.8 % della popolazione
```

Estenderli col **valore corrente** (l'unica scelta che non inventa un moto) darebbe loro `f = 0`
esatto: essendo l'**81.8 %**, **la mediana resterebbe zero**. Estenderli con altro **inventa una
fase precedente** — **A1** + **A7b**.

> **Non è una scelta fra «inventare» e «funzionare»: non funziona comunque.**

### La cura è il CONTATORE, ed è già dentro

`800fb24`, **byte-inerte verificata** contro `aa84755b` estratto in binario:
`max|A−B| = 0.000e+00` su `psi`/`phivel`/`eta`/`d`/`d0`/`omega_s`/`_nb`, **shape identiche**.

```
_ritmo_chiamate 126   _ritmo_sicurezza 2 (shape 80/440)   _ritmo_guard4pi_ko 0
_ritmo_snap_identico 1   _ritmo_f_tutto_nullo 1   _ritmo_f_mediana_nulla 1
-> passi con tempo proprio DEGENERE: 4 su 126 = 3.17 %
```

**E i quattro casi sono legittimi, uno per uno:** al passo 0 **non esiste un prima**; all'iniezione i
360 nodi nuovi **non hanno un passato**; negli altri due **il campo davvero non si è mosso**.
**Il codice fa la cosa giusta: mancava solo che lo dicesse.**

### ⚠ E i contatori hanno corretto me

Avevo scritto che all'iniezione *«il guard 4π fallisce, si cade sul 2π»*. **`_ritmo_guard4pi_ko = 0`:
non fallisce mai** — il ramo di sicurezza `:2028` viene **prima**. **La mia sonda ricostruiva i rami
nell'ordine sbagliato; il contatore, che sta nel codice vero, è autoritativo.**

E il quarto caso **non era «escluso»**: `_ritmo_f_mediana_nulla = 1` esiste davvero (valori a
`3.5e-13`, rumore numerico) — **ma il contatore li distingue, ed è il suo mestiere.**

### ⚠⚠ `K7` — **il tempo proprio non è cucito**, ed è più grande di `Z33`

| | `\|Δ\|/\|·\|` | cambi di segno |
|---|---|---|
| **`f = \|signed\|`** *(quella che il codice usa)* | **0.647** | — |
| `signed` | 0.933 | **0.342** *(nullo 0.50)* |
| **`imag(ov)` del feedback (`G6`)** | **0.032** | **0.0035** |

**`f` salta del `64.7 %` del proprio valore fra passi consecutivi. Venti volte peggio del feedback.**

> **Il tempo proprio è costruito su una grandezza che non è cucita**, e `Z33` — 4 passi su 126 con
> `f` nullo — **è un caso particolare di un problema che c'è in TUTTI i passi.**

**Due precisazioni contro l'overclaim:** il codice prende `|signed|`, quindi **i cambi di segno sono
già scartati** (il `0.933` è gonfiato da quelli, il numero che conta è `0.647`); **ma proprio per
questo `--tempo-proprio-orientato` alimenterebbe una grandezza NON cucita — è un avviso per quel
flag.**

### Cosa resta a Luca

1. **`Z33` è dichiarata** (contatore dentro): chiudere?
2. **`Z36` è il fronte nuovo, e più grande.** **Criterio di chiusura scritto: distinguere «il campo
   oscilla davvero così» da «la fase non è confrontabile fra passi».** Non ho una misura che le
   separi.
3. **`Z9` non va rimisurata**: `eta` non cresce in **2 passi su 126 = 1.6 %**, impatto ≤ ~2 %.

---

## 9.50 — **`Z36`: la cucitura fallisce su ENTRAMBI i fronti, e si DIMOSTRA perché. NON cablata. E `Z36` stesso va ri-letto**

**Data:** 2026-09-18 · blob `f8f46683` (git) / `94b6cc29` (byte) · un seme (5), 120 passi
**Strumento:** `csv/_test_fork/_Z36_cucitura.py` (committato **prima** di girarlo, `5b6d140`)
**Task history con l'obiezione, scritto e pushato PRIMA della misura:** `02ac909`
**Referto:** `doc/REFERTO_Z36_cucitura.md` · **NESSUNA CURA CABLATA**

### Il mandato, e l'obiezione scritta prima

Il mandato diceva: *«la forma è identica a quella che `_spinor_lift` usa già, misurata a `0.35 %`.
Non stai inventando una cura: stai applicando una che funziona, allo stesso tipo di oggetto.»*

**Ho scritto nel task history, prima di misurare, che i due oggetti NON sono lo stesso tipo:** il
lift è una **parametrizzazione** del Bloch, definita a meno di una fase globale — quella fase è
**gauge**; `psi_spin` è un **campo calcolato** la cui fase **è l'orologio**. E il conto:
`a_curato = a_originale − angle(overlap)`, quindi per rotazione rigida di `φ` verrebbe `φ − φ = 0`:
**l'orologio si fermerebbe esattamente nel caso che deve misurare.**

### (A) Il candidato del mandato è ESCLUSO

```
|psi_spin[:,0]| / |psi_spin|   (13320 nodi-istanza, ultimi 30 passi)
   mediana 0.999881   p05 0.990825   p01 0.976511   MIN 0.899377
   frazione sotto 1e-1 / 1e-2 / 1e-3 / 1e-6 / 1e-9 :  0.000000  su TUTTE
```

**La prima componente non passa MAI vicino a zero: è sempre almeno il 90 % del modulo.**
`angle(psi_spin[:,0])` **non è mal definito.** Lo spinore **non ruota** fra le componenti.

### (C) Gli stati consecutivi sono QUASI IDENTICI

```
|<psi_prec|psi>| normalizzato :  mediana 1   p05 0.999957   frazione > 0.99 = 1.0000
```

**Il 100 % delle coppie consecutive ha overlap > 0.99.**

### (B) Nessuna correlazione

```
corr( log(comp0/|psi|), log(salto relativo) ) = -0.0017     su 52149 nodi-coppia
tutti i 52145 stanno nella fascia comp0 > 1e-1
```

**Il candidato cade due volte: per assenza della causa e per assenza di correlazione.**

### (D) ⚠ LA CURA FALLISCE SU ENTRAMBI GLI ASSI

| | `a` ORIGINALE | `a` CURATO |
|---|---|---|
| **LIVELLO** `median\|a\|` | **3.94e-04** | **7.03e-06** |
| **SALTO** `\|Δa\|/\|a\|` | **0.712** | **0.786** |
| rapporto livello curato/originale | | **0.0179** |

**Il livello crolla di 56 volte — la cura toglie il 98 % del segnale** (era la lettura prevista).
**E il salto NON scende, PEGGIORA.** **Non è un compromesso «meno segnale ma più stabile»: è peggio
su entrambi gli assi.**

### ⚠ E si dimostra perché — dalla STRUTTURA dell'oggetto, non da un seme

Poiché la componente 0 è il **99.99 %** dello spinore:

```
overlap ~ conj(psp[:,0])*ps[:,0]   =>   angle(overlap) ~ a_originale
=>  a_curato = a_or - angle(overlap) ~ 0  +  CANCELLAZIONE CATASTROFICA
```

**La cura sottrae `a` a sé stessa**, ed è per questo che il salto **relativo aumenta**.
**Il conto nel task history era giusto nella conclusione e INCOMPLETO nella ragione:** avevo detto
*«per rotazione rigida»*; la misura dice che **basta che una componente domini**.

**E perché nel lift funziona e qui no:** là le due componenti sono **entrambe vive** e la fase globale
è **gauge**; qui **una ne porta il 99.99 %** e la sua fase **è il segnale**. **Lo stesso codice, su
oggetti diversi, fa cose opposte.**

### ⚠ E `L1` da solo sarebbe stato un FALSO PASS

Il sigillo del mandato guardava **un numero solo** (il salto). **Se il salto fosse sceso, avrei
cablato una cura che toglie il 98 % dell'orologio.** **La coppia salto+livello era necessaria**, ed
era nel task history perché ce l'ho messa io — **il mandato non la chiedeva.**

### ⚠ E `Z36` STESSO VA RI-LETTO — il `64.7 %` è un rapporto su una grandezza minuscola

Gli stati consecutivi hanno overlap **> 0.99 nel 100 % dei casi**, e il livello di `a` è
**3.94e-04 rad/passo**. Quindi *«il tempo proprio salta del 65 %»* significa: una fase che avanza di
`4e-04` per passo **varia di ~2.8e-04** — **in valore assoluto MENO del salto del feedback
(`1.1e-03`)**.

> **È la stessa forma dell'errore del `2.706`: un rapporto grande perché il denominatore è piccolo.**
> **L'ho trovata addosso a me per la seconda volta.**

La mia frase *«il tempo proprio non è cucito, venti volte peggio del feedback»* (§9.49) **resta vera
SUL RAPPORTO, ma va qualificata: NON è «il tempo proprio è rumore».** *(E non è rumore numerico:
`4e-04` è dodici ordini sopra la precisione di `angle`.)*

### Cosa resta a Luca

1. **La cucitura è esclusa PER DIMOSTRAZIONE**, non per misura su un seme: torna in gioco **solo** se
   cade la dimostrazione, cioè se lo spinore smettesse di stare al 99.99 % su una componente.
2. **`Z36` resta aperta con la domanda AFFINATA:** non *«la fase è confrontabile?»* — **lo è** — ma
   ***«un avanzamento di fase di `4e-04` per passo, che fluttua del 65 %, è l'orologio che
   vogliamo?»*** E si ricollega a `Z9`: con un avanzamento così piccolo **la maturazione è lenta per
   costruzione**.
3. **Niente cablato:** `psi_spin` non toccato, `f` non ridefinito, gauge non toccato.
   **`Z9` non rimisurata**: il §5 del mandato la prevede **dopo** la cura, e la cura non c'è.
4. **LIMITE dichiarato:** un seme, 120 passi, una scena. La dominanza al 99.99 % **potrebbe essere di
   questa configurazione** (`_psi_spinor` nasce da `exp(i·φ)` sull'asse 0, `:2657`).

---

## 9.51 — **Il §1 del mandato «gauge del vuoto»: il gauge è nella materia, la MIA obiezione è REFUTATA, e `cs` è VIVO**

**Data:** 2026-09-18 · blob `f8f46683` · 1 seme (5), 120 passi, ramo **4pi** su 124/126 invocazioni
**Strumento:** `csv/_test_fork/_gauge_vuoto.py` (`dd48ec0`, committato **prima** di girarlo)
**Task history con l'obiezione, pushato PRIMA:** `0e571b4` · **Referto:** `doc/REFERTO_gauge_vuoto.md`
**NESSUNA CURA CABLATA.**

### Il reperto del mandato, verificato dal sorgente

`r` (in `ritmo()`, `:2076`) è ancorato a **`median(|f|)`** — la materia, e `median(x) = 1` per
identità. `omega_clk` (in `STEP2_OROLOGIO`, `:2502`) è ancorato a **`CS_M`** — il vuoto. **E a
`:2458` si moltiplicano.** Il reperto **è reale**.

### (B) Il gauge attuale sta NELLA MATERIA — ma non «più degli altri»

```
cs/CS_M dei nodi x~1   : p05 0.5267  MEDIANA 0.8012  p95 0.9768   (n = 866)
cs/CS_M di TUTTI       : p05 0.5283  MEDIANA 0.8265  p95 0.9922   (n = 13320)
rho/peq  x~1 / TUTTI   : MEDIANA 1.272 / 1.354
```

Il nodo mediano di `f` ha **`cs/CS_M = 0.80`**, cioè **`(cs/CS_M)² = 0.64`** nel fattore di `STEP2`:
**i due riferimenti non coincidono, la lettura «cura cosmetica» non scatta.** **Ma i nodi a `x ~ 1`
non si distinguono dalla popolazione:** il nodo mediano di `f` è **un nodo tipico**. Non è che il
gauge sia finito in un posto strano — **è che tutta la popolazione sta nella materia.**

### (C) ⚠ LA MIA OBIEZIONE È REFUTATA DALLA MISURA

Avevo scritto **prima di guardare** che `cs/CS_M` non è ancorato al vuoto ma a **`mean(I)`**
(`_Lam = np.mean(_I)`, `:2914`), e che avrebbe avuto **un punto fisso della famiglia C12**.

```
median(I)/mean(I) :  0.145 (1/4)   0.653 (metà)   0.462 (ultimo)      -> FATTORE 4.5
cs/CS_M mediano   :  1 -> 0.871 -> 0.823 -> 0.841
```

**Il nodo tipico NON è inchiodato.** **Dove avevo ragione:** la scala **è** `mean(I)`, ed è nel
codice. **Dove avevo torto, ed è tutta la differenza:** `median(|f|)` inchioda **la mediana**, che
**è** il nodo tipico, **per identità, sempre**; `mean(I)` inchioda **la media**, che su una
distribuzione asimmetrica **non è il nodo tipico**.

> **È P1 applicato a un'identità algebrica: avevo trasportato la FORMA di C12 senza guardare QUALE
> statistica. È lo stesso errore della voce su `_tau`, che ho corretto io due giorni fa.**
> **E l'esito è un argomento A FAVORE del mandato, che avevo scritto per metterlo in dubbio:** il
> gauge proposto è **genuinamente meno auto-referenziale** di quello attuale.

### (D) ⚠ Il punto che NON decido da solo

```
                          MEDIANA     x<1e-3    x>1e3    in [0.1,10]
f*d/CS_M  (candidato)      0.0188     0.0394    0.0000     0.1510
f*d/cs    (tempo-luce)     0.0244     0.0286    0.0000     0.1786
f/median|f| (ATTUALE)      1.0000     0.0005    0.0000     0.8712
```

**Il criterio che avevo FISSATO non scatta:** avevo scritto *«fuori da O(1) di più di 3 ordini»*, e
**sono 1.7**. **Non lo sposto a posteriori.** **Ma la frazione nella banda utile passa da `87.1 %` a
`15.1 %`**, e poiché nessun nodo supera `x = 10`, **l'`84.9 %` finirebbe sotto `r_norm = 0.141`,
cioè nel decimo inferiore della dilatazione** (oggi ≤ `12.9 %`). **Il tetto NON si apre** (`1.358`
contro `√2 = 1.414`): **è la popolazione che scivola in fondo.** *(Aritmetica sulla distribuzione
misurata, non una predizione di run.)*

**DUE LETTURE LEGITTIME, e la misura NON le separa:** *(1)* **difetto** — col tipico a `0.019` il
bottleneck lavora nel tratto **lineare** e la saturazione **non morde per nessuno**; *(2)* **fisica**
— *«il nodo tipico ha un orologio 53 volte più lento del vuoto»* è **ciò che una dilatazione
gravitazionale deve dire**, e con `median(|f|)` era **invisibile per costruzione**.

> **Non è un «allineamento di gauge»: è un CAMBIO DI SIGNIFICATO di `r`**, da *«ritmo relativo al
> nodo tipico»* a *«ritmo relativo al vuoto»*. **Non ho un criterio, scritto prima, che separi le
> due letture, e non me lo invento adesso. DECIDE LUCA.**

### ⚠ E UNA COSA CHE NON CERCAVO: **un fatto stabile di CLAUDE.md è caduto**

```
cs/CS_M            : min 0.2834   p05 0.5283   MEDIANA 0.8265   max 0.9998
cs_std/cs per passo: MEDIANA 17.6 %   (min 16.6 %, max 19.4 %)
frazione cs/CS_M > 0.99 : 6.3 %
```

CLAUDE.md par.9 dice, come **fatto stabile**: *«`cs_std/cs` fra 0.0086 % e 0.24 %, sempre sotto
l'1 % … `tau = d/cs` **E'** `tau ∝ d` … il braccio ON non testa il tempo-luce»*.
**È superato di ~2000 volte rispetto allo 0.0086 %, e sta SOPRA la soglia dell'1 % di 17 volte.**

**E si sa perché, dal codice:** la cura di `cs_floor` del 2026-09-16 (**categoria D, nessun flag**)
ha sostituito la scala **assoluta** `1/GAMMA² = 400` con la scala **relazionale** `mean(I)`. Con
`400` e `I ~ 1e-7`, `sqrt(I/400) ~ 1e-5` — **`cs` era inchiodato**. Con `mean(I)`, `I/mean(I)` è
**O(1) per costruzione, a qualunque densità**.

> **`cs` non è vivo perché il sistema è maturato: è vivo perché la SCALA è diventata relazionale.**
> **Una correzione di difetto senza flag ha riaperto un fronte che il registro dava per chiuso.**

**Cosa NON dice:** non dice che `tau = d/cs` sia **fisicamente distinguibile** da `tau ∝ d` — quello
richiede il **confronto**, non la dispersione. Dice che **la premessa che lo escludeva è caduta**.
**Il giudizio «il braccio ON non testa il tempo-luce» va rifatto**, e con esso la parte del fronte
**A** che vi si appoggiava. → **`Z39`**.

### Cosa resta a Luca

1. **Le due letture del (D)** — degenerazione o fisica. **Serve una regola, scritta prima.**
2. **Se via libera: `CS_M/d_nodo`** — l'unico dei due candidati **senza statistica di popolazione al
   suo interno**, e la stessa ancora già certificata in sezione A. **Ma prima va CONTATO il ramo
   `d_nodo → LAM`** (`:3041`, `:3043`): il mandato vieta `LAM`, e per quella via rientrerebbe. **P5.**
3. **`Z39` è un fronte suo:** rifare `tau = d/cs` contro `tau ∝ d` su ≥ 4 semi.
4. **Limiti:** un seme, 120 passi, una scena; `cs_std/cs` **cresce col tempo**, quindi va citato con
   il passo. Fallback `cs = CS_M` scattato **2 volte su 248** (`0.8 %`).

---

## 9.52 — **`doc/ASSIOMI.md` è completo: A9 e A10 sono dentro. E la tensione più scomoda ora ha un numero**

**Data:** 2026-09-18 · **SOLA DOCUMENTAZIONE — nessun codice toccato**, blob `f8f46683` invariato
**Task history, pushato PRIMA:** `6ea24af` · Decisione di Luca: **sono assiomi, vanno tutti.**

### Lo stato verificato dal disco, prima di accettare il mandato (P1)

`doc/ASSIOMI.md` conteneva già **A1–A8** con i corollari **A3b, A3c, A7b, A8b**, e **APERTO #2 era
già barrato** col controesempio `u_nodo`. **A9 e A10: zero occorrenze.** **Non era una riscrittura
da fare: era un completamento** — e il mandato lo dice per primo, registrando che il mandato
*precedente* chiedeva una riscrittura in buona parte già fatta. **Da 15.003 a 23.850 byte.**

### A9 — *un presidio che non impedisce non è un presidio*

Soglia operativa: **alla TERZA occorrenza si smette di scrivere e si cerca il meccanismo.**
I tre casi (encoding cp1252 **sei volte**; par.5-quinquies violato e dimostrato dal riavvio;
`:2959` con **~20 chiamanti**) la superano tutti.

> **A9 è l'unico assioma che ha già FALSIFICATO SE STESSO:** la **settima** occorrenza
> dell'encoding colpì **lo script che stava CONTANDO le sei precedenti.**

**E si applica a se stesso:** finché resta una riga in un documento, **A9 è una violazione di A9**.
Per il suo caso capofila il meccanismo **esiste**: `csv/_presidio.py`.
**Dichiarato nel testo:** la soglia «alla terza» è **SCELTA, non derivata** — altrimenti A9
diventerebbe esso stesso un numero scelto, cioè **una violazione di A1**.

### A10 — *una sola grandezza può legare due domini*

Il caso, **misurato oggi** (`Z38`): `r` ancorato a `median(|f|)` → **la materia**; `omega_clk`
ancorato a `CS_M` → **il vuoto**; **e a `:2458` si moltiplicano.** Il nodo a cui `r` è ancorato ha
**`cs/CS_M = 0.801`**, cioè **`(cs/CS_M)² = 0.64`** nel fattore di `STEP2`: **lo scarto fra i due
ponti ha un numero, non è solo un argomento.**

**⚠ E un limite che la misura ha aggiunto, e che ho messo dentro l'assioma:** A10 dice **CHE** uno
dei due ponti è sbagliato; **non dice QUALE**, e sceglierlo **non è una sua conseguenza**. Spostando
`r` sul ponte del vuoto la banda utile del bottleneck passa da `87.1 %` a `15.1 %` e **`r` cambia
significato**. Le due letture — degenerazione o dilatazione gravitazionale reale — **la misura non
le separa.**

> **A10 è una DIAGNOSI, non una prescrizione. Un assioma che dicesse anche quale ponte tenere
> starebbe scegliendo la fisica, e non è il suo mestiere.**

### La tabella dei casi di A3 — cinque, ognuno col suo numero

`rho_arco/median(I_nodi)` = **8830** · media-di-mediane **19** contro **4089** · **A3c** (un rapporto
accanto a due massimi di passi diversi) · estensività confusa con l'età · **la mediana in `ritmo()`,
`median(x) = 1` per identità.**

> **L'ultimo è il più grave, perché non produce un numero sbagliato: produce un numero GIUSTO che
> non significa niente.**

### APERTO — due precisazioni, e una tensione che si è INASPRITA

**La categoria è dichiarata:** **A1–A5, A7, A10 dicono come un sistema dev'essere FATTO; A8, A9 e
A3c dicono come dev'essere OSSERVABILE, come le regole vanno rese EFFICACI, e come i numeri vanno
CONFRONTATI.** Il conteggio è aggiornato: **tre voci su dieci** (prima «due su otto»), più **A6 che
è un teorema**. E il perché la distinzione conta: **il giorno in cui esistesse l'azione unica `S`,
A1–A5/A7/A10 diventerebbero vincoli su `S`; A8/A9/A3c no — resterebbero vincoli su CHI LA MISURA.**

**E la tensione non è stata cancellata, è stata resa più forte** → **`Z40`**: `_cs_nodo` costruisce
la scala di `cs` come **`mean(I)`, una media sulla propria popolazione** — **esattamente la
scorciatoia globale che A2 vieta** — **e funziona**: `cs_std/cs` da **0.0086 %** a **17.6 %**,
fattore **~2050** *(il mandato citava `1300`, da una misura precedente: stesso fatto, due misure;
qui si riporta quella del blob `f8f46683`)*. **Le due vie sono incompatibili e nessuna è gratis:**
o **A2 ammette le medie globali DERIVATE** — ma deve dichiarare cosa distingue `mean(I)` da una
scorciatoia, e **quella distinzione oggi non esiste scritta** — **oppure `cs_floor` si rifà con
`peq`**, che però **nasce `NaN`** e il cui fallback ricade su `rho`, **una grandezza diversa**.

> **Non si chiude «tanto funziona»: è precisamente l'argomento che A2 esiste per rifiutare.**

### Due riferimenti incrociati corretti nello stesso commit

- **`Z5` portava una nota STALE:** *«va riportata in `doc/ASSIOMI.md` alla prossima revisione»* —
  **lo era già** (APERTO #2 barrato). Corretta.
- **`doc/ASSIOMI.md` NON era nella lista dei documenti di riferimento di `CLAUDE.md` par.7**, pur
  essendo citato nel §0-bis di ogni mandato. **Un documento che si deve leggere e che non compare
  fra i riferimenti è esattamente il difetto che A9 descrive.** Aggiunto.

---

## 9.53 — **La frequenza di riferimento: il numero c'è, e la legge NON si può cablare. `median(|f|)` fa TRE mestieri**

**Data:** 2026-09-18 · blob `f8f46683` · 1 seme (5), 120 passi, ramo **4pi** su 124/126
**Task history pushato PRIMA:** `b6308d1` · **Sonde:** `8088ce4` + `_retroazione_r`, committate
prima di girarle · **Referto:** `doc/REFERTO_frequenza_riferimento.md`
**NESSUNA CURA CABLATA, NESSUN NUMERO NEL SIMULATORE.**

### Il numero chiesto

| riferimento `[1/tempo]` | mediana | **std/med nel TEMPO** | `median(x)` = pinnato? |
|---|---|---|---|
| `median(\|f\|)` **ATTUALE** | 0.0394 | **0.6234** | **SÌ, `1` a dieci cifre** (identità) |
| `cs_nodo/d_nodo` | 1.776 | **0.0974** | no (`0.017 / 0.011 / 0.032`) |
| `CS_M/d_nodo` | 2.271 | **0.0986** | no |
| `CS_M/LAM` | 2.5 | **0 esatto** | — |

**Passando a `cs_nodo/d_nodo`, `x` si moltiplica per `0.01503`.** Poiché **`TAU_LOC = 1.0`**
(`:251`, nessuno smorzamento) **`r` andrebbe da `1.000` a `≈ 0.021`: `dt_n = DT·r` scenderebbe di
~47 volte**, e non uniformemente (il fattore varia di 4 fra passi).

**`CS_M/LAM` è squalificato senza girare niente:** `LAM` è **fisso** (`:146`, riassegnato solo da
CLI) → **`CS_M/LAM = 2.5` è un numero**, varianza nel tempo **0**.
*(Da non confondere con `lambda_vuoto(net) = mean(|psi|²)`, `:486`, che è **dinamica**: due nomi
quasi uguali, due nature opposte.)*

> **⚠ E il dato più informativo non è quello cercato: il riferimento ATTUALE è SEI VOLTE più
> volatile dei candidati** (`0.62` contro `0.097`). **Oggi `r` è misurato contro un metro che oscilla
> del 62 % da un passo all'altro, e quell'oscillazione è divisa via per costruzione.**

**E la riserva del giro scorso è chiusa:** nodi isolati (`d_nodo → LAM`, il ramo vietato) = **0 su
124 invocazioni**. *(P5: contato, non assunto.)*

### ⚠ La strada si chiude, e non per una scelta fra candidati: per una RETROAZIONE

**Verificato dal sorgente**, non dedotto:

```
:3389   self.phi = (_phi_t + (dt_n_s * self.phivel) + delta_sync_phi) % (4*np.pi)
:2972   dt_n = DT * r
        f = Δangle(psi_spin) / DT        <- diviso per il tempo di COORDINATA
```

**`Δphi ∝ dt_n = DT·r` ⟹ al prim'ordine `f ∝ r`.** L'anello: `r ↓ → dt_n ↓ → la fase avanza meno →
f ↓ → x ↓ → r ↓`.

| | guadagno dell'anello |
|---|---|
| **oggi** `x = f/median(\|f\|)` | riscalando tutti gli `f` di λ, **`x` non cambia** → **guadagno 1, PER COSTRUZIONE** |
| riferimento **assoluto** `R` | `r ≈ √2·x` nel tratto lineare → **guadagno `√2·x_misurato ≈ 0.021–0.035`** |

> **Guadagno ≪ 1 ⟹ `x → 0` di ~50 volte per passo: l'orologio si fermerebbe.** E un `R` scelto
> perché il guadagno valga 1 sarebbe **un filo di rasoio e un numero tarato** (A1).

**Ecco il terzo mestiere:** `median(|f|)` è normalizzazione (adimensionalità), **gauge** (il punto di
riferimento) **e ROMPI-ANELLO** (rende `r` indipendente dalla deriva comune di `f`).
*(Nel verdetto su `e342ae8` avevo scritto «la mediana è ENTRAMBE». **Sono TRE.**)*

### ⚠ E su A10 il vincolo 5 del mandato va ROVESCIATO

`omega_clk = coerenza * r` (`:2458`), **poi** `* (cs/CS_M)²` (`:2502`).

- con **`r = f·d/cs`**: *(coerenza) × (ritmo **proprio** del nodo, nessun riferimento esterno) ×
  (dilatazione vs vuoto)* → **UN SOLO ponte verso il vuoto** ✓
- con `r = f·d/CS_M`: **DUE confronti col vuoto moltiplicati** → **il doppio conteggio che A10
  vieta** ✗

> **È un riscontro su A10 stesso, aggiunto ieri: l'assioma non dice se il «ponte» sia l'ANCORA o la
> GRANDEZZA che attraversa, e le due letture danno candidati OPPOSTI. Va disambiguato.**

**Il riferimento derivabile quindi ESISTE — `cs_nodo/d_nodo`:** passa **A1** (nessuna costante:
tutto stato), **A3**, **A6** (`_tempo_luce_nodo` legge già `_cs_nodo_prev`), **A10**; unica tensione
**A2** (`cs` importa `mean(I)`), **già registrata in `Z40`**. È **già calcolato** (`1/tempo_luce`) e
**già sigillato** (`S8`, `max|err| = 2.55e-15`). **Ma non è sostituibile finché `f` è misurato in
tempo di coordinata.**

### ⚠ Una misura l'ho sbagliata, e la ritiro prima di usarla

```
        E1  f(t+1) vs r(t)     E2  NULLO: vs f(t)     E3  PARZIALE
MEDIANA   +0.4755  sd 0.174      +0.4727  sd 0.129      -0.9193  sd 0.409
```

**E1 ed E2 coincidono: la correlazione grezza con `r` è spiegata interamente
dall'autocorrelazione di `f`** — il controllo nullo ha fatto il suo mestiere.
**`E3` invece non si può leggere:** dentro un passo **`r` è una funzione deterministica di `f`**,
quindi a `f` fissato **non ha varianza residua**: la regressione a due regressori è **degenere per
costruzione**, e il `−0.92` con `sd 0.41` è **collinearità, non fisica**. **La ritiro come prova.**
**La domanda non è decidibile trasversalmente — la decide il codice (`:3389`).**

*(E una seconda svista mia, dichiarata: la colonna riassuntiva `max|median(x)−1|` vale `1` per tutte
e quattro le righe perché **dominata dai passi degeneri di `Z33`**. Non separa niente: separano le
cifre per passo.)*

### Cosa resta a Luca — **due strade, ed è una decisione di fisica**

1. **Si taglia l'anello alla radice:** `f = Δangle/dt_n` (tempo **proprio**). Rende A1 realizzabile
   ed è **la regola permanente di CLAUDE.md par.9** sul tic locale. **Ma cambia la definizione di
   `f`, che era stata esclusa in `Z36`.**
2. **Si tiene `median(|f|)`**, e si dichiara che **il difetto A10 resta aperto per una ragione ORA
   NOTA**, non per distrazione.

**Non ho un criterio, scritto prima, che scelga fra le due.** → **`Z41`.**

---

## 9.54 — **L'anello istantaneo di `ritmo()` è rotto: `10/10`. E il metro resta ballerino**

**Data:** 2026-09-18 · blob **`f8f46683` → `a1ae5090`** *(sha1 dei BYTE GREZZI, non `git hash-object`)*
**Task history pushato PRIMA:** `fd198ba` · **Previsioni pushate PRIMA della cura:** `631ff15`
**Cura:** `c6630fc` · **FAIL del sigillo committato:** `c818208` · **`10/10`:** `b98c5d1`
**Referto:** `doc/REFERTO_anello_istantaneo.md` · **Categoria D: nessun flag.**

### Il difetto era ESATTO, non approssimato

```python
med = max(float(np.median(np.abs(f))), 1e-9)     # calcolato DA f
x   = f / med                                     # e usato SU f
```

**A6** (`f` e `r` si determinavano a vicenda dentro il passo) e **A3** (`median(x) = 1` per identità)
**nella stessa riga**.

```
PRIMA  max|median(x) - 1| = 0.000e+00   su 122 passi
DOPO   p05 0.3260   mediana 0.9759   p95 2.9968   max|med-1| = 12.493
```

> **Non era «quasi» un punto fisso: lo era A MACCHINA.**

### La cura non cambia il gauge — cambia QUANDO lo si legge

**⚠ E il presidio che regge tutto nessuno l'aveva nominato: `ritmo()` ha TRE call-site, e DUE sono
DIAGNOSTICI** (`:3124` la fisica, `:6263` `_diag_completa`, `:6921`). **Se lo snapshot avanzasse
dentro `ritmo()`, ogni chiamata diagnostica farebbe avanzare lo stato fisico** — par.2.3 violato, e
**sarebbe il QUINTO difetto di questa famiglia**.

| chi | cosa fa |
|---|---|
| `ritmo()` | **LEGGE** `_med_f_prec` *(mai lo scrive)* e **REGISTRA** `_med_f_ultimo` |
| `step()` `:3129-3131` | **PROMUOVE**, accanto a `_psi_prec` e `_psi_spin_prec` |

**La contaminazione è chiusa PER COSTRUZIONE:** `step()` chiama `ritmo()` **prima** di promuovere,
quindi il valore promosso è **sempre** quello della chiamata fisica.

**⚠ E il mandato citava `Z33` col segno rovesciato:** diceva *«`Z33` è nata dall'aggiornamento DOPO
il consumo»*; **`680d069` ha misurato il contrario** — promuovere **dopo** è ciò che **fa valere
A6**. **Il pattern di `:3129-3131` è quello da SEGUIRE.**

**Uno SCALARE, non l'array: A8b chiusa per costruzione** — `med` non ha lunghezza, quindi
l'estensione a mitosi/`semina`/`nuova_massa` **non serve**. È esattamente ciò che mancò a
`_cs_nodo_prev` (**71.88 %**) e `_psi_spin_prec` (**95.33 %**).

**⚠ E un presidio che la MISURA ha imposto:** `1e-9` **non è una misura, è la protezione da
divisione per zero**, e promuoverlo renderebbe **la regolarizzazione il gauge del passo dopo**.
Misurato **prima**: `med_t/med_{t-1}` ha `max = 4.81e+07`, **esattamente il passo che segue un gauge
degenere**. **Senza quel ramo `Z33` non sarebbe sparita: si sarebbe ROVESCIATA**, da «tutti sul
pavimento» a «tutti in saturazione». **Misurato dopo: sul pavimento 2, non promosso 2 — 2 su 2.**

### Il sigillo — `10/10`, e `P1` è una byte-identità VERA

`P1`: **`n: 444 CONTRO 444`**, 7 array su 7 con **shape uguali**, `max|A-B| = 0.000e+00`.
**Non è «nessun confronto»: la riga delle shape lo dimostra** — **e valida anche il wrapper del
sigillo: se avessi ricostruito `f` male, `P1` sarebbe fallito.**
`P7`: **il tetto non si è spostato** (`1.4142130` contro `1.41419`).

### ⚠ Il sigillo è FALLITO al primo giro, per un difetto MIO — committato prima di aggiustare

`c818208`: **P0, P1, P2 FAIL.** Estraevo il blob di riferimento con
`git cat-file -p HEAD:soliton_simulator.py`, **ma `HEAD` era già il commit della cura**: **ho
confrontato il codice curato con sé stesso**, e `P2` dava **`max|A-B| = 0.000e+00` con SHAPE
UGUALI** — **la trappola già catalogata, col segno ROVESCIATO** *(là lo zero era mancanza di
confronto, qui identità perfetta per la ragione sbagliata)*.
**La riga delle shape, stampata per prima, l'ha reso leggibile subito: `n: 459 contro 459`.**
**È un difetto di STRUTTURA:** un riferimento ancorato a `HEAD` **si sposta col lavoro** — la stessa
ragione per cui il gate è ancorato al **BLOB** (par.2.6).

### ⚠ IL FRONTE NUOVO — `Z43`: il metro resta ballerino

Previsto **prima di misurare** (`fd198ba` §1.6) e **prima di cablare** (previsione 5, `631ff15`), e
**confermato più forte della stima**: avevo previsto `p05 ≈ 0.53 / p95 ≈ 2.10`; misurato sul codice
curato **`0.326 / 2.997`** — **un fattore ~9.**

> **L'anello è rotto, ma la dispersione del gauge (`62 %` fra passi) NON viene più divisa via: passa
> dentro `r`.** E si vede nel codominio: **il pavimento `1.414e-06` ORA SI TOCCA** (prima
> `min 1.293e-04`), mentre **il tetto resta fermo**.

**Non è un'obiezione alla cura** — A6 non è negoziabile, e **un punto fisso esatto è peggio di un
metro mobile** — **ma è la stessa domanda di `Z36`, spostata di un livello:** *un gauge che oscilla
del 62 % fra passi è il metro che vogliamo?*
**E le strade note sono già chiuse:** un riferimento assoluto non è cablabile (`Z41`) e la cucitura
toglie il 98 % del segnale (`Z37`). **Resta la via che `Z41` ha nominato e che Luca non ha deciso:
`f = Δangle/dt_n`.**

### I limiti

Un seme, 120 passi, una scena. **`P8` non dimostra nulla su `Z9`**: `ramp` **0.0002 / 0.00981 /
0.01962** con `TAU_A = 50`, **riportato e NON confrontato** con `0.0002/0.0102/0.0212`, che sono di
un'altra scena (A3c); e la previsione 6 diceva di aspettarsi uno scarto **dentro la dispersione fra
semi (~3 %)**, quindi **non interpretabile su un seme**.

---

## 9.55 — **Chi non ruota: non è «metà», non è la chiralità. È il transitorio di NASCITA — e `Z43` non ne è un sintomo**

**Data:** 2026-09-18 · **blob `a1ae5090` INVARIATO** *(nessuna cura, strumentazione inerte)*
1 seme (5), 120 passi · Task history pushato PRIMA: `0d9abac` · Sonda committata prima di girarla
**Referto:** `doc/REFERTO_chi_non_ruota.md` · → **`Z44`**, **`Z45`**, e **`Z43` qualificata**

### ⚠ Due premesse del mandato cadono prima ancora delle letture

**1) «Metà dei nodi ha `f = 0`» NON esiste.** Misurato:

```
passi con almeno un nodo a f = 0 : 13 su 124
frazione MEDIANA sui passi degeneri : 0.004357   <- UNO o DUE nodi su ~450
passo 0  : 80/80   = 100 %    <- non esiste un prima
passo 5  : 414/440 = 94.09 %  <- dopo l'iniezione di 360 nodi SENZA GENITORE
altri 11 : 1 o 2 nodi
```

**Ci sono due passi di NASCITA e undici passi con 1-2 nodi. Nessun regime «a metà».**
*(«Metà» era **aritmetica della mediana**, non una misura.)*

**2) Il bilanciamento di `perc_chi` non viene dalla mitosi antichirale.** I tre rami, **contati**:

```
semina/nuova_massa (:1850, rng.choice([-1,1]))   4 chiamate   440 nodi   <- il 94.6 %
mitosi UGUALE      (:3945)                     126 chiamate    19 nodi
Schwinger OPPOSTO  (:4066)                       5 chiamate     6 nodi   <- l'1.3 %
frazione +1 : 0.4375 (n=80) -> 0.5066 -> 0.5054 (n=459)
```

**L'universo è bilanciato entro lo 0.8 %, e il ramo Schwinger gira davvero** — ma è **l'1.3 %**.

### ⑤b — l'ipotesi materia/antimateria CADE, e cade dove c'è potenza

```
passo  n fermi  frazione +1   NULLO (popolazione)   scarto
0      80       0.437500      0.437500              +0.000000   <- TAUTOLOGIA intercettata dal nullo
5      414      0.519324      0.506818              +0.012505
16     1        0.000000      0.505643              -0.505643   <- ARITMETICA, non segnale
```

**I due soli passi con potenza dicono NO.** Al passo 0 lo scarto è **esattamente zero** — e non
poteva essere altro: **tutti** i nodi sono fermi, quindi la popolazione dei fermi **è** la
popolazione. **Il valore sotto ipotesi nulla ha intercettato una tautologia.**
Gli altri undici passi hanno **1-2 nodi**: con `n = 1` la frazione **deve** valere 0 o 1, e i sei
passi a `n = 1` danno **tre `+1` e tre `−1`**. **Bilanciati.**

**⚠ E il canale esiste davvero — l'avevo mancato nel task history e l'ho dichiarato prima di
misurare:** `CALORE_VETTORIALE = True` (`:270`), e `scuoti_vuoto` (`:538-540`) fa
`phivel[:n] += rng.normal(0,1)*ampiezza * perc_chi` **a ogni passo**. **Ma è un SEGNO su un rumore
SIMMETRICO:** la marginale di un `+1` e di un `−1` è **identica**; può agire **solo** per
correlazione. **La misura conferma che sul singolo nodo non agisce.**

### La catena si chiude, e ③ e ④ reggono INSIEME

```
nodo APPENA NATO -> eta ~ 0 -> ramp ~ 0 -> pesi ~ 0 -> psi_spin = 0 ESATTO
                 -> angle(0) = 0 (CONVENZIONE numpy) -> f = 0 -> gauge degenere
```

**③, nella forma più forte:** `|psi_spin|` dei nodi fermi è **`0.0000e+00` anche nel MASSIMO**, in
**12 passi su 13** *(eccezione il passo 32: `1.1e-06`, **600 volte** sotto la mediana)*.

> **`f = 0` non dice «il tempo è fermo»: dice «la fase non è definita». Non è una misura, è un
> valore di ritorno.**

**④:** `ramp` dei fermi fino a **66 volte** sotto la popolazione (`eta` `0.0141` contro `0.9317` al
passo 117), **e lo scarto CRESCE col tempo** (11 → 66): la popolazione matura, loro sono appena nati.

**① NON regge, e il suo NO è informativo:** Jaccard ≈ **0** fra passi degeneri consecutivi — **non
sono gli stessi nodi: non è congelamento, è un transitorio di nascita.**
**② NON regge** (`|Δψ| = 0.0000e+00`) **ma non è un'ipotesi concorrente: è la CONSEGUENZA di ③.**
**Era previsto nel task history: sono lo stesso fatto a due livelli.**

### ⚠ Ma `Z43` NON è un sintomo di `Z9`

La lettura ④ del mandato diceva *«`Z33`/`Z43` sono sintomi di `Z9`»*. **Per `Z33` è vero. Per `Z43`
no:** i passi degeneri sono **13 su 124** e solo **2** hanno `median(|f|) = 0`, mentre il rapporto
`med_t/med_{t-1}` ha **`p05 0.482` / `p95 2.097`** — percentili su 123 passi, che due estremi non
possono spostare — e **l'11.4 % dei passi sta fuori da `[0.5, 2]`**.

> **Curare `Z9` toglierebbe i 13 passi degeneri, NON l'oscillazione del gauge negli altri 111.**

*(Limite dichiarato: non ho ricalcolato quei percentili escludendo esplicitamente i passi degeneri —
l'argomento è di robustezza, non una misura dedicata.)*

### Cosa resta a Luca

1. **`Z33` risale a `Z9`**: è il transitorio di maturazione del kernel sui nodi nuovi, **non un
   difetto del tempo**. La cura, se si vuole, è **a monte**.
2. **`Z43` resta, ed è qualificata come chiesto: una DECISIONE SULLA DEFINIZIONE DEL TEMPO**, non una
   questione tecnica.
3. **Nessuna cura, nessun cablaggio, nessuna promozione, nessun cambio di default.** Blob invariato.

---

## 9.56 — **La campagna a 1200 passi: la domanda sui segmenti, e cosa ho dovuto rispondere «non verificato»**

**Data:** 2026-09-18 · blob **`a1ae5090` invariato** · **run IN CORSO al momento della scrittura**
**Task history e previsioni pushati PRIMA del run:** `fb87640` · **Sonda + inventario:** `35a5786`

### La domanda di Luca, e la risposta onesta

Luca ha chiesto, prima di lasciarmi analizzare: **«i quattro segmenti CONTINUANO lo stesso stato, o
sono quattro run separati che ripartono dalla semina?»**

> **Risposta: NON VERIFICATO — e non lo asserisco.**

Li **avevo progettati** per riprendere (`--sync-db` carica lo stato se il blob combacia, `:7111`,
e il `.pkl` contiene `rng_state`). **Ma la prova diretta me la sono buttata via io:** nel mio script
il comando python era piped a **`| tail -3`**, che ha scartato proprio la riga
`[db] stato CARICATO … riprendo da step interno N`. **L'unica evidenza dell'avvenuto resume era
quella, e non l'ho conservata.**

**Non ho difeso il disegno: ho fermato il run segmentato e ne ho lanciato UNO CONTINUO**, con la riga
di comando del mandato e **`--passi 1200` in una sola invocazione**. Verificato **dal log**, non
dedotto:

```
run.log:  "[batch] condensazione: seed=900 passi=1200 ogni=10 sep=8.0 nmasse=3"
invocazioni di python nel log      : 1      <- UNA SOLA
righe "[db] stato CARICATO"        : 0      <- nessun resume: parte dalla semina
```

**E il `.pkl` vecchio è stato cancellato + `--db-cleanup`:** senza, il run nuovo **avrebbe ripreso da
quello stale**, cioè esattamente il difetto da togliere.

*(I quattro istanti `120/400/800/1200` sono ora **punti di campionamento dentro quel run**: un
watcher copia il `.pkl` quando `_db_step` li tocca.)*

### ✅ `n` piatto NON è un artefatto del tetto — verificato

```
MAX_NODI = 4000000      (:1000, "GUARDIA DI MEMORIA, non di fisica")
n misurato ~ 1199
```

**Il tetto è 3300 volte lontano.** In questa configurazione **la mitosi è davvero quasi ferma**
(3 nodi in 100 passi, contro 19 in 126 delle scene-sonda).

### ⚠ Il controllo su `eta`, e il riferimento giusto

Dallo snapshot a 120 passi *(del run poi interrotto)*: **`eta` mediana = `0.0100`**, `_db_step = 120`,
blob salvato `a1ae5090`, `dirty = False`.

> **⚠ È CENTO VOLTE più piccola dell'`eta` che le scene-sonda avevano a 120 passi (`~0.98`).**
> **Non è una contraddizione: è una scena diversa** — qui si parte da `n ≈ 1196` già seminati, là da
> 80 che crescevano a 459. **Ma significa che in questa configurazione il kernel matura molto più
> lentamente**, e il controllo *«`eta(1200) ≈ 10 × eta(120)`»* **va fatto DENTRO questa scena**:
> confrontarlo coi numeri delle sonde sarebbe un errore di popolazione (**A3c**).

### Tre limiti trovati dal disco, e uno è diventato irrilevante

1. **`--db` NON ESISTE:** argparse lo rifiuta come ambiguo con `--db-cleanup`/`--db-ogni`.
   **Il flag è `--sync-db`.** Il primo lancio è fallito così; la correzione è in
   `doc/INVENTARIO_strumenti.md` perché il prossimo non ci ricada.
2. **Il `.pkl` non contiene il tracking delle masse:** `salva_stato` (`:2862-2866`) salva solo
   `ndarray/int/float/bool/str`, e `conc_nodi`/`masse_info` sono **liste e dizionari**.
3. **⚠ Ma il punto 2 è diventato IRRILEVANTE, e in meglio:** il `--diaglog` ha **231 colonne, una
   riga per passo su tutti i 1200**, e contiene già — **calcolate dal batch col tracking VERO** —
   **`coer_01`, `coer_02`, `coer_12`** (coerenza FRA le masse), **`m0_coer`/`m1_coer`/`m2_coer`**
   (interna), e **`centro_coer` / `guscio_coer`** (il contrasto centro/guscio), più
   `eta_min/mean/max`, `cs_eff_*`, `rho0_core_max`, `n_naninf`, `d_min/max/mean`.
   **Il blocco ③ non ha più bisogno della mia ricostruzione per posizione.**

### ⚠ Due cose che dichiaro invece di scoprirle dopo

**Il watcher è partito quando il run era già al passo 290: il `.pkl` a 120 NON c'è.** Prenderà
**400, 800, 1200**. **Non rilancio nulla per recuperarlo** — sarebbe un run separato, cioè ciò che
Luca ha appena escluso — e la traiettoria continua di `centro_coer`/`guscio_coer` **copre tutti i
1200 passi, incluso il 120**. Solo il *profilo radiale* a 120 manca, e tre istanti bastano per dire
se il minimo si sposta e si approfondisce.

**E un errore di processo, la TERZA volta: due heredoc nella stessa chiamata di shell non
funzionano** in questo ambiente, e la seconda volta ha ucciso il watcher senza che il run se ne
accorgesse. **È un caso di `A9`: la nota non ha impedito il ripetersi.** **Il meccanismo è: un file
per chiamata, scritto con lo strumento di scrittura, mai due heredoc insieme.**

### Cosa NON è ancora committato, e perché

**I dati di `csv/_test_fork/_g1200/` sono ESCLUSI da questo commit: il run è ATTIVO e sta scrivendo
`diag.csv`, `cond.csv`, `run.log` e `stato.pkl`.** CLAUDE.md vieta `git add -A` con un run attivo, e
i `.pkl` **non si committano mai** (binari, 22 MB: il loro comando è in `INVENTARIO_strumenti.md`).
**Si committano a run finito, con il referto.**

### 9.56-bis — ⚠ **LA PROVA DELLA CONTINUITÀ C'È, ed è migliore della riga di log che avevo perso. E una mia falsa allarme, corretta**

**Il `diaglog` ha 726 righe, una per passo**, e `eta_mean` è **monotona crescente senza un solo
reset**:

```
step      eta_mean     eta_max     n_tot   n_naninf
0         0.003748     0.06744     1196    0
102       0.073014     1.30415     1199    0
307       0.231682     3.88778     1200    0
518       0.394475     6.42988     1203    0
722       0.567138     9.19917     1203    0
```

> **Se il run fosse ripartito dalla semina, `eta_mean` sarebbe ricaduta a `~0.0037`. Non lo fa mai.**
> **Questa è la prova diretta della continuità, ed è più forte della riga `[db]` che avevo buttato
> via col `tail -3`.** Combacia con l'altra evidenza: **1 sola invocazione nel log, 0 righe di
> resume.**

**E la crescita è quasi ESATTAMENTE lineare:** da `0.0730` (step 102) a `0.5671` (step 722) è
**×7.8 su ×7.1 di passi**. **Il controllo di Luca — *«`eta` a 1200 deve essere ~10 volte quella a
120»* — REGGE.**

### ⚠ MA SOLO SULLA MEDIA: sulla MEDIANA avrei dato un falso allarme, e l'avevo dato

**Dagli snapshot per-nodo, `eta` MEDIANA:**

```
step 120 : 0.0100017      step 130 : 0.0100018
step 470 : 0.0100066      step 680 : 0.0100096
```

**La mediana è PIANTATA sul valore di semina (`0.0100`) mentre media e massimo crescono di due
ordini.** Avevo letto la mediana e stavo per concludere *«`eta` non si accumula»*: **era sbagliato, e
lo correggo prima di usarlo.**

> **IL FATTO VERO, ed è un dato su `Z9`: la maturazione è confinata a una MINORANZA di nodi.**
> **Più della metà della popolazione resta al valore di nascita per 700 passi**, mentre una coda
> matura e trascina la media. **`eta_max` arriva a `9.2` mentre la mediana non si muove dalla terza
> cifra.**

**E questo dice anche perché il criterio di Luca poteva ingannare:** *«se `eta` non cresce, il run
non è continuo»* — **qui il run È continuo (provato) e la mediana NON cresce lo stesso.**
**L'inferenza «mediana ferma ⟹ run non continuo» non vale**, e questo è il caso che lo mostra.

### ⚠ E un difetto MIO nel watcher, trovato e corretto

Il primo watcher faceva `shutil.copyfile` del `.pkl` mentre il run lo sostituiva con `os.replace`:
**due file su tre portavano un `_db_step` DIVERSO dal loro nome** (`stato_400.pkl` conteneva il passo
**130**, `stato_800.pkl` il passo **470**).
**Li ho RINOMINATI col loro `_db_step` vero** — restano stati legittimi di un run continuo, solo a
istanti diversi — **e ho riscritto il watcher perché RI-SCRIVA l'oggetto che ha letto invece di
copiare il file, con verifica del `_db_step` dopo la scrittura.**
> **Il nome di un file non è un dato: il `_db_step` dentro lo è.** *(Stessa famiglia di P6: «un file
> che si distingue dagli altri solo per il nome non è un dato».)*

**Stabilità a 722 passi: `n_naninf = 0` su tutte le righe, `n` da 1196 a 1203.**

---

## 9.57 — **Non è metà: è il 93 %, sono SEMPRE GLI STESSI, e sono LE TRE MASSE. E il gauge del tempo è la costante `1e-9`**

**Data:** 2026-09-18 · **blob `a1ae5090` INVARIATO** — nessuna cura, nessun run nuovo
**Dati:** i `.pkl` del run **continuo** a 1200 passi (seed 900, 1 invocazione, 0 resume)
**Task history col conto fatto PRIMA:** `49c0c28` · **Referto:** `doc/REFERTO_chi_non_invecchia.md`
**⚠ In testa:** `--tau-luce` **ha il sigillo FALLITO**, `--chi-basc` attivo, **un seme**, `Z9` aperta.

### Il conto scritto PRIMA di aprire i `.pkl`: previsto `1.0025`, misurato `1.0000`

Da `eta += DT·r` si ricava `r` dalla sola crescita di `eta`. Il pavimento di `ritmo()` vale
`1e-6/(1/√2+1e-6) = 1.414212e-06`, che in 560 passi accumula `7.92e-06` — **contro `7.90e-06`
misurati.** Misurato poi dai `.pkl`, su **quattro intervalli su quattro**:

```
r FERMI mediana 1.414213e-06     r FERMI p95 1.414222e-06     r/r_floor = 1.0000
```

> **Non sono «lenti»: sono al PAVIMENTO ASSOLUTO, e lo è anche il loro 95° percentile.**

### ① Non è metà — è il 93 %, e non cala

```
step    n      p05/p25/MEDIANA/p75 (IDENTICI)   p95        max       | FERMI  FRAZ.
120     1199   0.010001683                      0.885813   1.54005   | 1116   0.9308
800     1203   0.0100113                        8.329932  10.28641   | 1116   0.9277
1200    1204   0.010016956                     13.034878  15.91664   | 1116   0.9269
```

**`p05 = p25 = mediana = p75`, identici.** **Tre quarti della popolazione allo stesso valore**, e si
muove **solo il `p95`**. **Non è «mediana bassa»: è un blocco.**

### ② Sempre gli stessi — `Jaccard = 1.0000` ovunque

`120→130→470→800→840`: **1.0000 a ogni transizione**, primo contro ultimo **1.0000**, `|B\A| = 0`.
**Gli stessi identici 1116 nodi per 720 passi. Nessuno entra, nessuno esce.**

### ③ Il falsificatore della mitosi: **escluso in modo totale**

**4 nodi nuovi in 1200 passi, e ZERO di loro è fermo.** *(Età anagrafica esatta: i nodi si appendono
in coda, quindi l'indice è l'ordine di nascita.)* **Non è il transitorio di nascita.**

### ⚠ CHI SONO — e qui la voce cambia natura

```
           n      grado p25/med/p75     raggio p25/med/p75
FERMI     1116    371 / 371 / 371       7.732 / 8.004 / 8.281
mobili      87      7 /   9 /  12       1.739 / 2.504 / 3.518
```

> **Raggio mediano `8.004` = `sep`: i «fermi» SONO le tre masse seminate. I «mobili» sono il
> centro.** **Grado `371` contro `9`: un fattore 41.** *(Conferma indipendente dal tracking del
> batch: `TRACK accr=1116`, lo stesso numero.)*

### ⚠ IL ROVESCIAMENTO — il gauge del tempo non è più una mediana

```
median(|f|) = 1.000000e-09  a TUTTI gli istanti   <- il PAVIMENTO max(median, 1e-9) E' ATTIVO

           f mediana        frazione f == 0 ESATTO    x = f/med mediana     |psi_spin|
FERMI      0.0000e+00       0.4928 -> 0.6102          0.0000e+00            6.03e-06 PIATTO
mobili     0.0583 -> 0.175  0.0000                    5.8e+07 -> 1.7e+08    9.8e-03  (x27)
```

**Il 49-61 % dei nodi ha `f` esattamente zero ⟹ `median(|f|) = 0` ⟹ `med` cade sulla costante.**

> **Il gauge del tempo proprio non è una statistica del sistema: è il numero `1e-9`.**
> È alla lettera l'avvertimento di CLAUDE.md par.9: *«alle scale simulabili la regolarizzazione
> diventa il parametro fisico»*.

**E il sistema si separa in due popolazioni che non si parlano: il 93 % a `x = 0` e il 7 % a
`x ≈ 10⁸`. Non c'è più nessuno in mezzo.**

### Cosa questo NON dice

- **`Z44` non è smentita: NON SI TRASPORTA.** Là i `f = 0` erano **1-2 su 450** ed erano **neonati**;
  qui sono **il 53-61 %** e sono **le masse**. **Due popolazioni diverse, entrambe da citare con la
  loro scena** (A3c).
- **NON so perché** i nodi a grado **371** abbiano `|psi_spin|` **mille volte più debole** di quelli
  a grado **9**. **È il fatto più strano della misura e non ho una spiegazione misurata. Non la
  invento** — era la quinta lettura, *«nessuna regge → si dice»*.
- **Non dico che sia un difetto del codice o della fisica.**

### Cosa resta a Luca

1. **`Z9` va riscritta**, e **il testo proposto è nel referto §8 — NON cablato.** Il punto chiave:
   **il criterio di chiusura non può essere «`ramp` mediano cresce», perché il `ramp` mediano è
   quello di un nodo che non si muove.**
2. **`Z43` va rovesciata:** non è che il metro oscilla del 62 % — **in questa configurazione il metro
   è `1e-9`.**
3. **Il mandato sull'embedding**: la NOTA diceva *«se metà dei nodi non invecchia, l'oscillazione del
   62 % potrebbe venire da lì»*. **Misurato: il nodo mediano è un nodo mai maturato, ed è una delle
   masse.** **La precedenza va decisa da te.**

---

## 9.58 — **La scena del VIDEO: `--sync-db` non salva, un frame è sei passi, e `CALORE_VETTORIALE` è spento**

**Data:** 2026-09-18 · blob **`a1ae5090` invariato** · **run IN CORSO** alla scrittura
**Task history e previsioni pushati PRIMA del run:** `904e823` · **Driver:** `56d1b4e`

> **⚠ QUESTO PARAGRAFO ARRIVA IN RITARDO, e lo dico.** I fatti qui sotto erano nel task history da un
> commit, **ma non in questa relazione** — e il par.5-ter chiede **entrambi**, *«così chi legge solo
> questa è comunque allineato»*. **Me l'ha dovuto chiedere Luca, ed è la seconda volta.**
> **Il meccanismo, non la nota (A9): da qui in avanti il paragrafo di relazione va NELLO STESSO
> COMMIT del task history, non in uno successivo.**

### ① `--sync-db` nel ramo VIDEO **carica e basta: non salva mai**

```python
:5836   _db_v = getattr(a, "sync_db", None)
:5837   if _db_v and os.path.exists(_db_v):
:5839       net.carica_stato(_db_v)      # <- SOLO LETTURA
```

**In tutto `esegui_headless` non c'è nessuna chiamata a `salva_stato`**, e il commento lo dice da sé:
*«se `--sync-db` e il file esiste, **CARICA** lo stato … renderizzo **IN AVANTI** da lì»*.

> **Il comando previsto per questa scena NON avrebbe prodotto nessun `.pkl`, e le misure non si
> sarebbero potute fare.**
> **La via, senza forzare:** un driver che riproduce la scena **col percorso ufficiale del
> programma** — `_cli()` → `_applica_regime` → `_applica_flag` → `avvia_test("N-MASSE")` — e **il
> ciclo per frame COPIATO da `update()` (`:5091-5100`), senza il rendering.** *(Il rendering non è
> fisica, ed è anche la ragione per cui costa meno.)*

### ② `PASSI_PER_FRAME = 6`: la scena è **2400 passi**, non 400

`:686`, e `update()` fa **sei** `step()` per frame. `N-MASSE` dura `dur=120 + dur=280` = **400
frame = 2400 passi di motore.** **Il conto della durata va fatto su questo, non sui frame.**

### ③ La durata, **misurata** su un pilota di 15 frame

```
scena avviata: n = 2391   (N_c*0.8 per massa, N_c = 621, tre masse)
frame  1  n=2391  archi=429498  coer_l=0.639  dil= +7.88%   [16.97 s/frame]
frame 15  n=2391  archi=429498  coer_l=0.515  dil=+20.40%   [16.57 s/frame medio]
```

**`n = 2391` alla semina coincide ESATTAMENTE col frame 10 della tabella di riferimento**, e
`coer_l`/`dil` sono nello stesso intorno: **è la scena giusta, verificata e non assunta.**
**Stima dichiarata prima del lancio: 3-4 ore**, con l'avvertenza che **il costo cresce coi nodi e
una estrapolazione lineare sottostima.**

### ④ ⚠ Una differenza di configurazione che nessuno aveva nominato

Letto dal modulo **dopo** `_applica_flag` (P6: dai dati, non dal comando):

```
CALORE_VETTORIALE = False      <- perche' il comando ha `--calore-scal`
CHI_BASC          = True
```

**Nel giro di `Z45` `CALORE_VETTORIALE` era l'UNICO canale vivo fra `perc_chi` e la dinamica**
(`scuoti_vuoto` firma il calcio termico con `perc_chi`). **Qui è SPENTO.** **E `--chi-basc` è
ACCESO**, quindi **`perc_chi` non è un'etichetta di lignaggio ma una variabile della torsione.**

> **Due differenze OPPOSTE rispetto a `Z45`: il canale è spento e l'etichetta è dinamica.**
> **`Z45` non si trasporta a questa scena** — e nemmeno `Z46`, che è del batch: **le due scene
> differiscono in TRE cose** (masse a `N_c·0.8` invece di `N_c·0.6`, **mitosi attiva**, canale
> spento). **`Z46` andrà QUALIFICATA «vale per il batch», non corretta.**

### Le previsioni, committate prima del run

La più importante è **scomoda di proposito**: *se il guscio ha `eta` più bassa dell'interno, **è il
fronte di nascita, non una parete**, e la lettura del video va corretta*. Più tre falsificatori,
incluso il discriminante che ha funzionato su `Z46`: **se `eta` dei fermi cresce di `DT·r_floor`, è
di nuovo il pavimento di `ritmo()` e la scena non c'entra.**

### Stato del run

**In corso.** Al frame 50: `n` da `2391` a `2576` *(la mitosi si è accesa: nel batch erano 4 nodi in
1200 passi)*, `archi` `429 724`, `coer_l` `0.286`, `dil` `+25.1 %`, **`14.1 s/frame`** — leggermente
**meno** della stima, perché il pilota includeva l'avvio. **Nessun verdetto: i numeri arrivano col
referto.**

---

## 9.59 — **Tre verifiche prima del run: il rendering NON tocca la fisica (verificato), e `--chi-basc` cambia una misura**

**Data:** 2026-09-18 · blob **`a1ae5090` invariato** · **run a 400 frame FERMATO e RIFATTO**
**Sigillo:** `csv/_seal_fork/_sigillo_driver_video.py` · **PASS**

### ① ⚠ «Il rendering non è fisica» era una DEDUZIONE — ora è una misura

Avevo concluso che *«l'unica cosa che manca è il rendering, che non è fisica»*. **Era un argomento,
non una verifica** — e il precedente di `lambda_vuoto` *(che sembrava di sola lettura e chiamava
`calcola_psi()`, che SCRIVE `self.psi`)* dice che non basta.

**Enumerato dal sorgente:** `update()` chiama, oltre al ciclo fisico, **`net.diagnostica()`
(`:5104`, OGNI frame — il driver la chiamava solo ogni 5)**, **`net.campo_spaziale()` (`:5136`)**,
**`net.pozzo_grafo()` (`:5218`)**, **`net.intensita()` (`:5267`)** — **tutte assenti dal driver.**

**⚠ E una distinzione che mi ero perso:** il commento a `:7168` — *«le funzioni diagnostiche
aggiornano cache che la DINAMICA legge»* — riguarda **`_diag_completa`** (`:6255`, che chiama
`net.calcola_psi()` e `net.ritmo()`), **NON `net.diagnostica()`. Sono due funzioni diverse, e il
batch protegge la PRIMA** con snapshot+restore. **E `update()` non avvolge `diagnostica` in
nessuna protezione.**

**LA PROVA, non la lettura:** due run identici di 12 frame, uno **solo-fisica** e uno che chiama
**anche** le quattro funzioni di disegno a ogni frame, **nello stesso ordine di `update()`**:

```
n: 2391 contro 2391
psi / phi / phivel / eta / d / d0 / tw / omega_s / _nb / psi_spin / _psi_spinor / _psi_prec /
perc_chi / pos        ->  TUTTI  max|A-B| = 0.000e+00   con SHAPE UGUALI
[PASS] shape divergenti 0, array confrontati 14, max|A-B| = 0.000e+00
```

> **Il driver È equivalente — e lo dichiaro con la verifica accanto, non con l'argomento.**
> *(La riga delle shape è stampata per prima: `max|A-B| = 0` può significare «nessun confronto».)*

**Il run a 400 frame era arrivato al frame ~50: l'ho FERMATO e i dati CANCELLATI**, perché giravano
su una traiettoria la cui equivalenza non era ancora provata. **Rifatto dopo il PASS.**

### ② ⚠ `--chi-basc` riscrive `perc_chi`: **la misura ④ va riformulata**

**Se `chi_basc` riscrive `perc_chi` a ogni passo, contare «quale ramo di mitosi gira» NON BASTA:
qualunque cosa la mitosi assegni, il basculamento può sovrascriverla al passo dopo.**

**La misura diventa TRE numeri per passo, non uno:**
1. **quanti `perc_chi` assegnati dalla MITOSI**, e **da quale ramo** (`:3945` eredita UGUALE,
   `:4066` eredita OPPOSTO) — **contati** (A8);
2. **quanti RISCRITTI da `chi_basc`**, e **con quale segno**;
3. **il BILANCIO NETTO**: la frazione `+1` nel tempo.

> **Senza questa separazione non si sa se l'antimateria emerga dalla MITOSI o dal BASCULAMENTO.**
> **Sono due meccanismi diversi, e la domanda riguarda il primo.**

### ③ ⚠ `--tau-luce` ha il sigillo FALLITO — **e va nel REFERTO, non solo in testa all'output**

**La scena del video include una legge NON CERTIFICATA** (`doc/SIGILLO_tau_luce_FALLITO.md`,
CLAUDE.md par.0), **ed ogni numero che ne esce lo eredita.** *(E vale anche per il video già girato:
la tabella dei fotogrammi porta la stessa qualifica.)*

### ④ E una correzione a un numero MIO: `PASSI_PER_FRAME = 6`

**La scena è `400 frame = 2400 PASSI DI MOTORE`**, e la tabella letta dai fotogrammi **va
RIMAPPATA**: **frame 375 = passo `2250`**, non 375.
**Senza questa conversione i confronti con `Z46` (che è a `1200 passi`) sbagliano di un fattore 2**,
e va scritto nel referto.

---

## 9.60 — **`Z47` registrata: `pos` è l'unico SFONDO rimasto, e nessuno lo aveva scritto**

**Data:** 2026-09-18 · **SOLA DOCUMENTAZIONE** — nessun codice toccato, blob **`a1ae5090`** invariato
**→ `doc/RAMIFICAZIONI.md` voce `Z47`** *(progetto di lungo periodo, NON iniziato)* **e la
DICHIARAZIONE in `doc/ASSIOMI.md`.**

### La dichiarazione, che oggi il repo non faceva da nessuna parte

> **Il modello è relazionale nella DINAMICA. La nascita della TOPOLOGIA e le DIREZIONI usano un
> embedding euclideo in 3D (`self.pos`) come ausilio computazionale. In quel punto NON è
> background-independent. L'errore dell'embedding NON è misurato.**

**Non è un difetto nascosto: è una scelta di implementazione che nessuno aveva reso esplicita**, ed è
emersa da una domanda di Luca — *«ma io posso evitare questa retroazione?»*.

**E cosa È relazionale non è poco:** `psi`, `cs`, `d`, `phi`, le forze, il tempo proprio, la mitosi e
il settore spinoriale **non leggono MAI `pos`**.

### ⚠ Verificato riga per riga: i punti VIVI sono QUATTRO, non tre

| punto | cosa fa |
|---|---|
| `:1958` `_allaccia` | `cKDTree(self.pos)` → **decide LA TOPOLOGIA** |
| `:4230`/`:4267` `memoria_hebbiana_moto` | `v = pos[j]−pos[i]` → `dirarc`, `grad_tw` → **scrive `mem_mot` e `_nb`** |
| `:4425` | `v_rel` → `dir_radiale`, `dir_laterale` (gravità, frame-drag) |
| `:1498-1499` `chiralita_core_locale` | **sfera EUCLIDEA** di raggio `r` |
| **`:3409-3410` Kuramoto** | `cmv`, `r_cm` dal centro di massa |

> **⚠ Il quinto rigo è la correzione:** il mandato lo dava come condizionale — *«`:3409` solo se
> `K_SYNC != 0`»* — **ma `K_SYNC = 1.0` di DEFAULT (`:199`): è VIVO.**
> *(Davvero inerti solo `:4338` sotto `LS_AZIM = False` e `:4199` sotto `L_CONSERVA = False`,
> quest'ultimo marcato **«ERRATA, NON usare»**.)*

**E `pos` INSEGUE `d`** (`rilassa_disegno`, `EMB_IT = 3`): **c'è un anello**
`d → pos (approssimato, 3D) → topologia + direzioni → d`.

### Le tre conseguenze, e la prima sorprende

1. **La DIMENSIONE 3 è fisicamente rilevante:** `_allaccia` cerca per **RAGGIO**, non per `k` vicini,
   e `N_vicini ~ densità·rc^D`. **In 6D il grado esploderebbe.** *(Con un `k`-NN la dimensione
   sarebbe stata indifferente: non lo è.)*
2. **Viola `A5`:** due nodi si allacciano perché **vicini NEL DISEGNO**. **Un legame può nascere fra
   punti che non si sono MAI parlati.**
3. **Un grafo arbitrario non si rappresenta esattamente in 3D** *(già a cinque nodi le distanze sono
   sovradeterminate)*: **l'errore dell'embedding rientra nella fisica.**

### Il progetto, e il suo costo — registrato, **non iniziato**

**La geometria ricostruita dalle sole `d`:** tre distanze fissano un triangolo, quindi **gli angoli
fra gli archi di un nodo si ricostruiscono senza coordinate**; un **riferimento locale** per nodo;
una **connessione** per confrontare riferimenti vicini — **e il precedente esiste già nel codice:
`_spinor_lift` fa la cucitura di fase per lo spinore, misurata a `0.35 %`: è trasporto parallelo.**
**Servirebbe l'analogo per la GEOMETRIA.**

**Il costo, scritto perché è ciò che decide:** **quattro settori** da riscrivere *(`_allaccia`,
`memoria_hebbiana_moto`, `chiralita_core_locale`, e il `cmv` del Kuramoto)*; **la connessione non
esiste e ogni scelta lì dentro è una LEGGE da derivare (A1)**; **due riferimenti vicini possono
essere incompatibili — quella È la curvatura**, e **non si ottiene uno spazio globale ma una
connessione locale**; **e sarebbe un SISTEMA NUOVO: tutto ciò che è stato misurato NON si
trasporta.** **Settimane, non ore.**

### Il criterio di avvio — **una misura, non un'opinione**

**«Quanto mente l'embedding?»** → `|pos_i − pos_j| / d_ij` per arco **e la stabilità
dell'ORIENTAMENTO** fra passi.
> **⚠ La seconda conta più della prima: le direzioni sono NORMALIZZATE (`v/L`), quindi l'errore
> sulla LUNGHEZZA si cancella e resta quello sull'ORIENTAMENTO — ed è quello che entra in `grad_tw`
> e in `_nb`.**

**Errore piccolo e orientamento stabile → il guadagno è TEORICO: si dichiara il limite e non si
riscrive niente. Errore grande o orientamento che sobbalza → la motivazione è MISURATA**, e
spiegherebbe anche **`Z43`** *(il metro che oscilla del 62 %)*. **La misura non è stata fatta qui.**

---

## 9.61 — **Il referto mancante del batch a 1200: il guscio esiste, ma è fatto dei nodi che non maturano. E il gauge è sul pavimento nel 99.76 % delle chiamate**

**Data:** 2026-09-18 · blob **`a1ae5090` invariato** · run **finito** (passo 1200, 21662 righe)
**Previsioni scritte PRIMA del run:** `fb87640` · **Referto:** `doc/REFERTO_struttura_1200.md` → **`Z48`**

> **⚠ `--tau-luce` HA IL SIGILLO FALLITO: la scena include una legge NON CERTIFICATA, e ogni numero
> qui sotto lo eredita.** `--chi-basc` attivo, `Z9` aperta, **un seme**, **nessun verdetto di
> fisica**.

### ⚠ Il numero che viene prima di tutti — i contatori A8

```
_ritmo_chiamate 2886   _ritmo_med_sul_pavimento 2879   ->   il 99.76 %
_ritmo_med_non_promosso 1202     _ritmo_f_tutto_nullo 5
```

> **`median(|f|)` cade sulla costante `1e-9` in `2879` chiamate su `2886`. Non è un caso degli
> istanti campionati: è tutto il run.** **Il gauge del tempo proprio, in questa scena, non è una
> statistica del sistema: è un numero.**

**E la cura di `Z42` ha lavorato 1202 volte:** milleduecento volte il pavimento **non** è stato
promosso a gauge del passo dopo.

### ① Maturazione — `Z46` vista da un'altra grandezza

`p05 = ramp MEDIANO = 0.000200`, **identici e fermi** ai passi 120/800/1200, mentre il **`p95` cresce
di 15 volte** (`0.0177 → 0.2607`) e `Lam` di **1300**. **Nessun nodo con `|psi| = 0`** — la
previsione diceva «quasi nulla», ed è **zero**.

### ② Il guscio — esiste, si stabilizza, si approfondisce

```
passo 120 : minimo di |psi| a r = 8.55   (179 nodi)   bin oltre: 0   <- AL BORDO
passo 800 : r = 7.21  (31 nodi)   bin oltre: 4   |psi| dentro/fuori ~2200
passo 1200: r = 7.21  (36 nodi)   bin oltre: 4   |psi| dentro/fuori ~4300
```

**I tre falsificatori, applicati PRIMA di descrivere:** **(b)** non è un minimo di *statistica* (il
bin ha **più** nodi della mediana per bin); **(c)** al passo 120 era **al bordo**, a 800 e 1200 c'è
popolazione oltre; **⚠ (a) SCATTA e peggiora:** `eta` del bin minimo / `eta` interna =
**`0.0095 → 0.0012 → 0.00073`**.

> **La previsione diceva: *«se il guscio ha `eta` più bassa, è il FRONTE DI NASCITA, non una
> parete»*. La prima metà è vera, la seconda NO — e la ragione è misurata: la mitosi qui è FERMA
> (8 nodi in 1200 passi).**
> **Quei nodi non sono nati da poco: sono i nodi che NON HANNO MAI MATURATO — gli stessi `1116` di
> `Z46`, a raggio mediano `8.004`.**
> **Il «guscio» coincide con l'anello delle masse seminate ferme al pavimento di `ritmo()`.**

### ③ ⚠ Le fasi — **la mia previsione era rovesciata**

Gli sfasamenti **non convergono a `2π/3`** *(previsto, regge)* ma **si stabilizzano**.
**Ma avevo previsto coerenza INTERNA > coerenza FRA masse, e il misurato è l'opposto:**

```
coer FRA masse : 0.235 -> 0.779 -> 0.807
coer INTERNA   : 0.204 -> 0.223 -> 0.204
```

> **Quattro volte più alta FRA le masse che DENTRO ciascuna. Le tre masse si allineano fra loro più
> di quanto ciascuna sia coerente al proprio interno. Non so spiegarlo, e non lo spiego.**

### ④ Il contrasto

`rho` al centro **×3400**; `rho` al guscio **piatta**; **rapporto centro/guscio da `3.3e+03` a
`1.36e+07`** — quattro ordini in 1080 passi. Stress `max|d−d0|/d0` da `18.9` a `50.2`. **Nessun NaN.**

### Un limite della sonda, dichiarato

**Cerca i `.pkl` per NOME**, e il `400` non esiste *(il primo watcher li mislabellò: gli istanti veri
sono `120/130/470/800/840/1200`)*. **`130`, `470` e `840` non sono stati letti.** Tre istanti bastano
per dire «si sposta e si approfondisce», **ma la risoluzione è minore di quella disponibile.**

---

## 9.62 — **`Z48` qualificata, e il run della scena giusta è GIÀ in corso: l'inversione si vede già**

**Data:** 2026-09-18 · blob **`a1ae5090` invariato** · **run IN CORSO** (frame 275/400)
**Task history e previsioni:** questo stesso commit *(meccanismo par.5-octies + A9)*

### ✅ `Z48` QUALIFICATA — e la prova era già nel mio referto

Il mio referto concludeva *«il guscio coincide con l'anello delle masse seminate»*. **Vero PER IL
BATCH.** **Ma non è la struttura osservata nel video**, e **la ragione per cui il batch non poteva
contenerla è misurata nel referto stesso:**

```
batch 1200 :  8 nodi e 10 archi in 1200 passi   ->  LA MITOSI E' FERMA
video      :  5112 mitosi,  n da 2391 a 7503
```

> **La struttura osservata è fatta di MATERIA NUOVA, e nel batch quella materia non nasce.**
> **Nessuna misura sul batch poteva trovarla.** **`Z48` è QUALIFICATA, non corretta.**

### ✅ Il run che il mandato chiede è già in corso — verificato, non assunto

Il driver sigillato sta girando la config esatta **da `94e2ec0`**, e **traccia la tabella dei
fotogrammi**: al frame 270 **`n = 5443`** contro `5465`, **`dil = +10.75 %`** contro `+10.3 %`.
**È la stessa scena.** **Frame 275/400, `15.6 s/frame`, ~33 min alla fine.**
**Non lo rilancio:** rilanciarlo costerebbe **1 h 45** per riavere gli stessi numeri.

**⚠ E L'INVERSIONE È GIÀ VISIBILE, prima di qualunque analisi:**

```
frame 265 : dil = +10.967 %
frame 275 : dil =  +8.593 %
```

### ⚠ La mia riserva sul §3: i raggi `4 / 8 / 12` sono ASSOLUTI su un sistema che DILATA

Il sistema si dilata del `+19.6 %` e poi si ricomprime, e `d medio` va da `0.934` a `1.753` a
`1.483` — **quasi un fattore 2.**

> **CLAUDE.md par.4 lo vieta esplicitamente:** *«Mai confronti a PASSO FISSO su un sistema che si
> espande/dilata: genera ALIASING… normalizza sulla scala (COMOVENTE), non su intervalli
> assoluti.»*
> **`r < 4` al frame 10 e `r < 4` al frame 375 non sono la stessa regione fisica.**

**Riporterò ENTRAMBE le letture** — assoluta *(come chiesto)* **e comovente** *(normalizzata al
raggio dell'anello misurato a ogni istante, non al `sep = 8` di semina)*. **Se concordano, la riserva
cade e lo dico. Se divergono, la lettura assoluta è aliasata e si scarta, non si media.**

### Le previsioni, e una è deliberatamente scomoda

**Mi aspetto l'OPPOSTO di `Z48` sul punto ③**: lì i nodi della struttura erano **vecchi e fermi**;
qui la mitosi è viva e mi aspetto **nodi NATI DOPO**. **Ma il discriminante è quello che ha
funzionato due volte: se il loro `r` valesse `1.414212e-06`, sarebbero fermi come quelli di `Z46`, e
«materia nuova» sarebbe sbagliato.**
**E il quarto falsificatore è l'esito scomodo: se la struttura coincidesse con l'anello `r ≈ 8`,
sarebbe la stessa cosa di `Z48` e la distinzione del mandato cadrebbe.**

### Limiti dichiarati prima

**Un seme. `--tau-luce` ha il SIGILLO FALLITO: ramo non certificato, ogni numero lo eredita.**
**5 snapshot invece dei 20 chiesti**, e `d medio` ricostruito da quelli: **per l'istante
dell'inversione la risoluzione è 5 frame, per il profilo radiale sono 5 punti.** **Lo dico prima
invece di presentarlo come sufficiente.**

---

## 9.63 — **Il ciclo c'è, ma non è nel corpo: è nella CODA. E l'anello si sfalda mentre il centro si accende**

**Data:** 2026-09-18 · blob **`a1ae5090` invariato** · scena VIDEO, **400 frame = 2400 passi**, 1h49
**Previsioni scritte PRIMA:** `515ed53` · **Referto:** `doc/REFERTO_struttura_video.md` → **`Z49`**

> **⚠ `--tau-luce` HA IL SIGILLO FALLITO: la scena include una legge NON CERTIFICATA e ogni numero
> qui sotto lo eredita.** `--chi-basc` attivo. **Un seme. Nessun verdetto di fisica.**

### La scena è la stessa — confermato a quattro cifre

`d MEDIA` misurata `0.9275 / 1.4502 / 1.6739 / 1.7537 / 1.4871` contro `0.934 / 1.454 / 1.676 /
1.753 / 1.483` della tabella dei fotogrammi.

### ⚠ Il ciclo non è dove sembrava

```
frame      10       115      190      270      375      400
d MEDIA    0.9275   1.4502   1.6739   1.7537   1.4871   1.4004    <- sale poi SCENDE
d MEDIANA  0.8626   0.9636   1.0126   1.1191   1.3191   1.3514    <- SALE SEMPRE
d p95      1.9709   4.6983   6.1655   6.3985   3.6234   2.9533    <- sale poi CROLLA
```

> **La distanza TIPICA non si ricomprime mai. È il `p95` a dimezzarsi, e con lui la media.**
> **La «ricompressione» è il RIASSORBIMENTO DELLA CODA LUNGA, non una contrazione del corpo.**

**È la trappola del §4 del mandato** *(«se bimodale, non riportare mediane»)*: **media e mediana
dicono cose opposte, e solo la coppia descrive il fenomeno.** **Non l'avevo previsto: l'ho trovato
solo perché il presidio imponeva di non fidarsi delle mediane.**

**E la dilatazione RIMBALZA:** `−7.44 %` (370) → `−2.70 %` (375) → `−4.21 %` (380) → **`+2.80 %`**
(385) → `−1.13 %` (400). **La tabella si fermava al 375.**

### ⚠ La regione interna si svuota, si riempie, e si accende di cinque ordini

```
nodi(r<4):  900 -> 291 -> 224 -> 221 -> 559 -> 907
rho_spin :  3.7e-07 ....................-> 5.6e-02     (CINQUE ORDINI)
|psi|    :  1.0e-04 ....................-> 0.666
```

**Il minimo di popolazione (frame 270) coincide col massimo di `d MEDIA`: riempimento e
ricompressione sono lo stesso intervallo.**

### ⚠ E l'anello si sfalda — grado da `496` a `2`

```
grado ANELLO   496 -> 160 -> 87 -> 2 -> 2 -> 2
grado INTERNA  127 -> 157 -> 143 -> 121 -> 127 -> 109
```

> **Non è che la struttura «ingloba» le masse: le masse si DISGREGANO e la materia si concentra al
> centro.** *(Descrizione dei numeri, non un meccanismo: il meccanismo non è misurato.)*

### ⚠ Di cosa è fatta — **l'OPPOSTO di `Z48`**, e il discriminante lo conferma

`eta` interna **`28.60`** contro anello **`9.81`** *(tre volte più matura)*, e **i nodi NUOVI stanno
più nell'ANELLO (`76 %`) che al centro (`38 %`)**.

```
r ricavato da eta += DT*r :  INTERNA 1.08 -> 1.41      ANELLO 0.71 -> 0.37
r/r_floor (interna)       :  ~1e+06
```

> **La previsione diceva: *«se il loro `r` valesse `1.414212e-06`, "materia nuova" sarebbe
> sbagliato»*. NON lo vale — è `10⁶` volte il pavimento. È l'opposto di `Z46`/`Z48`.**
> **E l'anello RALLENTA (`0.71 → 0.37`) mentre il centro accelera.**

### ⚠ `perc_chi`: la separazione si ottiene **senza contatori**

```
frac +1 :  0.000 (frame 10) -> 0.0292 -> 0.0369 -> 0.0834 -> 0.1468 -> 0.1645
```

**Alla semina `rng.choice([-1,1])` darebbe `~0.50`. Al frame 10 vale `0.000`.**

> **⟹ `chi_basc` ha già riscritto TUTTI i 2391 nodi entro il frame 10.** **L'antimateria di questa
> scena viene dal BASCULAMENTO, non dalla generazione** — e la separazione che avevo chiesto **si
> ottiene per deduzione, non serve strumentare.**
> **⚠ Ma è una deduzione da due numeri, non un conteggio: un conteggio diretto richiederebbe
> contatori durante il run, e non è stato fatto.**

### ✅ E la mia riserva sui raggi assoluti **CADE, e lo dico**

`R_anello` **misurato** varia solo dell'**8 %** (`7.67 → 8.04 → 7.37`): **assoluto e comovente danno
gli stessi numeri.** **La riserva era legittima — par.4 vieta gli intervalli fissi su un sistema che
dilata — ma qui non morde.** **⚠ Vale solo perché l'anello non si è spostato abbastanza: non è una
licenza generale.**
**E `R_anello` fa il ciclo da solo:** `7.56 → 8.04 → 7.37`.

### La coerenza globale crolla mentre quella locale sale

`|<nb>|` globale `0.995 → 0.190`; `coer_l` locale `→ 0.669`. **Due grandezze diverse: si citano
separate, non si mediano.**

### Cosa resta a Luca

1. **Nessuna identificazione**, come chiesto: i numeri e la forma.
2. **Il MECCANISMO non è misurato** — perché l'anello perda i legami e il centro si accenda.
3. **Limiti:** un seme, `--tau-luce` non certificato, **5 punti** per il profilo e **5 frame** di
   risoluzione per il ciclo.

---

## 9.64 — **Non è una Y: nella regione interna il modo dominante è il DIPOLO, e l'`A_3 = 0.97` sono le tre masse**

**Data:** 2026-09-18 · blob **`a1ae5090` invariato** · **nessun run nuovo** *(i sei `.pkl` esistevano)*
**Letture fissate PRIMA:** `4cf1817` · **Referto:** `doc/REFERTO_forma_Y.md` → **`Z50`**

> **⚠ `--tau-luce` HA IL SIGILLO FALLITO: ramo non certificato, ogni numero lo eredita.** Un seme.
> **L'osservazione «forma una Y» è VISIVA: qui è stata messa alla prova, non confermata.**

### ⚠ Prima del risultato, un difetto MIO — trovato perché il suo esito era assurdo

Avevo derivato la soglia di «regione densa» **per analogia** con `lambda_vuoto = mean(|psi|²)`,
applicandola a `rho_spin`. **L'analogia non regge:**

```
rho_spin al frame 400:   MEDIA 1.4432e+01   MEDIANA 6.4175e-03   ->  RAPPORTO 2249
```

**La media di `rho_spin` non è il livello di vuoto: è una statistica della CODA.** Selezionava
**1479 nodi tutti a `r ≈ 7.7`** — **l'anello** — e dava *«nodi interni densi = 0»* a ogni istante.
**Non era un fatto sul sistema: era la soglia.**
**Controprova:** con la **mediana**, i nodi interni selezionati sono **623 su 811**, con `rho_spin`
mediana **8.7 volte** quella globale. **La regione interna densa esiste: era la soglia a non
vederla.**

> **È P1 applicato a una soglia: un'analogia va verificata sulla DISTRIBUZIONE che seleziona, non
> sulla forma della formula.** *(La media resta nell'output come **controesempio dichiarato**.)*

### Il risultato — col NULLO accanto, senza cui l'istogramma è un disegno

```
soglia 10x la mediana       A_1      A_2      A_3      A_6    | NULLO
frame 400  CON L'ANELLO    0.0756   0.2169   0.9652   0.8744  | 0.0292
frame 400  SOLO INTERNI    0.4001   0.3242   0.2310   0.1358  | 0.1198
```

- **Con l'anello `A_3 = 0.965` contro un nullo di `0.029` — 33 volte. Ma sono le tre masse seminate,
  che stanno a `0°/120°/240°` PER COSTRUZIONE.**
- **Dentro: `A_3 = 0.231` contro nullo `0.120` — meno di due volte — mentre `A_1 = 0.400` è 3.3
  volte il nullo.**

> **Il modo dominante nella regione interna è il DIPOLO, non il tre.**
> **Scatta la terza lettura: «`A_3` grande solo includendo l'anello → artefatto delle tre masse».**

### L'istogramma lo mostra direttamente: **un picco, non tre**

```
 +52.5°  3.254  #################################################################
 +67.5°  3.998  ######################################################################
(il resto fra 0.23 e 0.86; un rialzo secondario a +172.5° = 1.35)
```

**Un lobo dominante, e il picco NON è su una massa: è FRA due masse (`0°` e `120°`).**
**Tre bracci a `0/120/240` non ci sono.**

### Robustezza e limiti

Fra soglia `10×` e `100×` la mediana i valori cambiano (`A_1` `0.400 → 0.611`, `A_3` `0.231 →
0.437`) **ma l'ORDINE no: `A_1 > A_3` in entrambe.**
**⚠ La statistica interna è DEBOLE:** `N_eff` scende a **21** (nullo `0.22`), e al frame 375 vale
**10.9** (nullo `0.30`): **lì non si misura nulla, e non lo leggo.**
**E la regione interna densa compare TARDI:** `0/0/0/0/18/370` nodi ai sei istanti — **coerente con
`Z49`**, e tutto ciò che si dice sulla forma riguarda **gli ultimi 150 frame**.

### Cosa questo NON dice

- **NON dice che il video sia sbagliato.** Dice che **la firma a tre bracci non è misurabile nella
  regione interna con questa definizione di «densa»**, e che `A_3 = 0.97` **è spiegato dalle tre
  masse**. **E il modo trovato — il dipolo — è comunque una struttura ANISOTROPA, non un disco.**
- **NON è un verdetto sulla predizione di Luca**, che riguarda il **CICLO** e si decide col run a due
  masse — **in corso, frame 30/400**. **Questa misura toglie UN meccanismo candidato (la Y
  topologica), non la predizione.**
- **Nessuna identificazione.** *(La Y a 120° è Fermat-Steiner e compare ovunque: era scritto nel task
  history PRIMA, proprio perché se fosse uscita non sarebbe stata una spiegazione.)*

---

## 9.65 — **La Y non c'è: né nel denso, né nel vuoto, né nella variazione. Il dipolo sì**

**Data:** 2026-09-18 · blob **`a1ae5090` invariato** · **nessun run nuovo**
**Letture fissate PRIMA:** `0f7cea6` · **Referto:** `doc/REFERTO_Y_nel_vuoto.md` → **`Z51`**
**`Z50` QUALIFICATA:** vale **per la regione densa**.

> **⚠ `--tau-luce` HA IL SIGILLO FALLITO: ramo non certificato, ogni numero lo eredita.** Un seme.

### Il rilievo era giusto — ma nel posto giusto la Y non c'è lo stesso

`Z50` aveva misurato `A_m` **sul denso**; se i bracci sono **ciano** — interferenza distruttiva,
`|psi|` basso — **stavano nel complemento.** **Misurato il complemento:**

**① IL VUOTO INTERNO È ISOTROPO**

```
A_3/nullo ai sei istanti:  1.14 · 0.68 · 0.36 · 0.70 · 1.31 · 1.71     -> MAI due volte il nullo
frame 10 (883 nodi, la statistica migliore):  A_3/nullo = 1.14
istogramma del vuoto (f115, 268 nodi): tutti e 24 i bin fra 0.448 e 1.343, media 1
                                        (nel DENSO il picco arrivava a 3.998)
```

**Il controllo pesato sul DEFICIT concorda ovunque** *(terza cifra)*: **il risultato non dipende
dalla scelta del peso** — era la riserva che avevo scritto prima.

**② LA VARIAZIONE — la misura che doveva rispondere, e risponde NO**

```
intervallo     nodi  N_eff | A_3/nullo   A_1/nullo
f10 -> 115      215  187.9 |   1.66        0.69
f190 -> 270     157   14.9 |   0.99        1.34    <- N_eff 15: NON SI LEGGE
f270 -> 375     413   43.4 |   1.57        0.66
f375 -> 400     733   76.3 |   1.92        3.37
```

> **`A_3` non supera `1.92` in nessun intervallo. Il campo NON si accende lungo tre bracci.**
> **⚠ Ma nell'ultimo `A_1/nullo = 3.37`: si accende lungo UNA direzione.**

**③ IL TEMPO:** il vuoto **resta al nullo per tutti e sei gli istanti**. **Non c'è nessun «alto
presto e poi cala»: non c'è mai stato niente da calare.**

### Verdetto contro le quattro letture

**Scatta la SECONDA** — *«`A_3` al nullo in tutte e tre le varianti → artefatto della colormap»* —
**e la TERZA a metà**: `A_1` domina nella **variazione** (`3.37×`) e nel **denso** (`3.3×`), **ma non
nel vuoto**, dove è al nullo.

> **Con TRE definizioni diverse di «dove cercare» e col nullo accanto a ogni numero, `A_3` non
> supera MAI due volte il nullo.** **`A_1` sì, in due varianti su tre.**
> **Il sistema si accende lungo UNA direzione, non tre.**

### ⚠ E un limite VERO della misura, non una scusa

**`A_m` sui NODI pesa i PUNTATORI; il fotogramma mostra IL CAMPO INTERPOLATO fra di essi**
(`campo_spaziale`, kernel FFT). **Sono due oggetti diversi, e questa misura ha guardato il secondo.**
**Per chiudere davvero servirebbe `A_m` sulla GRIGLIA, e NON è stato fatto.**

### Cosa non dice

**Non dice che nel video non si veda niente**: dice che **ciò che si vede non ha una firma a tre
bracci nella distribuzione angolare dei nodi in `rho_spin`.**
**Non è un verdetto sulla predizione di Luca**, che riguarda il **CICLO** e si decide col run a due
masse — **in corso, frame 80/400.**

---

## 9.66 — **La predizione di Luca è sbagliata nella forma forte. Ma il ciclo si spezza in due fenomeni, e uno dei due dipende davvero dal numero di masse**

**2026-09-18** · blob `a1ae5090` **invariato** · **A/B a variabile singola su `--nmasse` (3 → 2)**
**Predizione committata PRIMA del run:** `a4fbe42` · **Sonda committata prima di girarla:** `7f81634`
**Referto:** `doc/REFERTO_due_masse.md` · **Output:** `csv/_test_fork/_ab_due_tre.txt`

> **⚠ IN TESTA:** **`--tau-luce` HA IL SIGILLO FALLITO** (par.0): **entrambi** i bracci girano su un
> ramo **NON CERTIFICATO**, e ogni numero lo eredita. **`--chi-basc` attivo in entrambi.**
> **UN SEME PER BRACCIO. NESSUNA IDENTIFICAZIONE DI FISICA.**

### La predizione, e cosa è successo

> **«Con DUE masse questa dinamica NON ci sarà più. Sarà completamente differente.
> Ed è dovuto all'INTERAZIONE FRA TRE MASSE, contro l'interazione fra due.»**

**Non è così, e lo scrivo perché era scritto nel mandato che si dovesse scrivere.**
**La curva che decideva era nominata prima — `nodi(regione interna)`, con la regione definita
`r < R_anello(t)/2` e `R_anello(t)` MISURATO:**

```
COMOVENTE (r < R_anello(t)/2)   f10    f115   f190   f270   f375   f400  | min/f10  f400/min
TRE  (Z49)                      883    268    222    222    497    811   | 0.2514   3.6532
DUE  (ctrl)                     867    242    191    216    274    332   | 0.2203   1.7382
```

**La U c'è in entrambi. Il minimo cade allo STESSO istante (`f190`). E la DISCESA è la stessa:
`min/f10` vale `0.246` e `0.269` in assoluta, `0.251` e `0.220` in comovente — quattro numeri, due
bracci, stesso valore entro il 20 %.**

### ⚠ Ma non scatta nemmeno la lettura ② secca: scatta **la terza**, quella tenuta aperta

**Il RECUPERO è tutt'altro.** Fra il minimo e la fine `n` **quasi raddoppia in entrambi**
(`4307 → 8018` e `3350 → 5878`), quindi un conteggio che cresce può voler dire *«la regione si
riempie»* **oppure** *«il sistema cresce e la regione lo segue»*. **Il rapporto fra i due tassi
separa i due casi:**

```
braccio      f_min   int_min  int_f400  n_min   n_f400  | recupero / crescita
TRE  (Z49)    190      222      811     4307     8018   |      1.9624
DUE  (ctrl)   190      191      332     3350     5878   |      0.9906
```

> **A TRE masse la regione interna si riempie DUE VOLTE più in fretta del sistema.**
> **A DUE cresce ESATTAMENTE come il sistema: `0.9906`. In senso relativo NON si riempie affatto, e
> la «risalita» del conteggio nudo È la crescita della popolazione.**

**⚠ E questa normalizzazione è POST-HOC, e lo dichiaro:** la lettura fissata prima è il **conteggio
nudo**, e quella **dà una U in entrambi.** **Riporto entrambe perché chi legge possa pesarle
diversamente** — non per scegliere quella che mi conviene.

### L'accensione — il falsificatore 3, e **non scatta alla lettera**

```
rho_spin med (interna COMOVENTE)
             f10         f115        f190        f270        f375        f400       | escursione
TRE  (Z49)   3.7728e-07  6.5691e-06  3.4709e-07  5.0703e-07  4.0612e-03  5.5564e-02 | x1.601e+05
DUE  (ctrl)  4.4894e-07  3.3742e-04  7.5504e-05  1.0729e-06  2.6102e-04  2.4743e-03 | x5512
                                                 -> RAPPORTO TRE/DUE all'ultimo istante: x22.46
                                                 -> lo stesso su |psi|:                 x14.5
```

**`rho_spin` SI accende anche a due masse (`×5512`): *«ciclo sì, accensione no»* è FALSO, e il
falsificatore come era scritto NON scatta.** **Ma l'accensione finale è `22.46` volte più debole.**

**E la forma è diversa, ed è la cosa che il rapporto finale nasconde:**
- **a TRE masse** `rho_spin` resta **piatta e bassa** per quattro istanti su sei e poi **esplode** fra
  `f270` e `f400`: **un evento TARDIVO e BRUSCO**;
- **a DUE masse** si accende **PRESTO** — `3.37e-04` al `f115`, cioè **51 volte** il valore a tre masse
  **nello stesso istante** — poi **SI SPEGNE** (`1.07e-06` al `f270`, un fattore `315` in giù), e poi
  risale più debole.

> **La separabilità che il falsificatore 3 anticipava c'è, ma lungo una cucitura diversa da quella
> prevista: non «ciclo sì, accensione no», ma LO SVUOTAMENTO È DEL SISTEMA e IL RIEMPIMENTO CON
> L'ACCENSIONE DIPENDONO DAL NUMERO DI MASSE.**

### ⚠ E una conclusione di `Z49` **non si trasporta**

```
r ANELLO   TRE   0.7090  0.7831  0.7219  0.5233  0.3877   <- SCENDE
           DUE   0.8196  0.9823  0.8928  0.6206  1.0035   <- finisce SOPRA il valore iniziale
```

**`Z49` aveva scritto *«il centro accelera mentre l'anello rallenta»*. Il centro accelera in entrambi.
L'ANELLO RALLENTA SOLO A TRE MASSE.**

**Dove invece i due bracci sono indistinguibili, e conta quanto il resto:** `d` mediano cresce
**monotono** in entrambi (`×1.57` e `×1.41`, **nessuna ricompressione nella mediana** — coerente con
`Z49`, dove il ciclo era **nella coda**); la decoerenza del Bloch è la **stessa curva**
(`0.9953 → 0.1900` contro `0.9935 → 0.1754`); `perc_chi` è **persino leggermente più alto** a due
masse; e **il discriminante di `Z46` non scatta in nessuno dei due** (`r/r_floor ~ 10⁶`, non `1.0000`).
**La nube gonfia e si ricomprime in ENTRAMBI**, a due masse più grande e col picco più tardi.

### I due falsificatori del confronto, e come sono stati trattati

- **FALSIFICATORE 2 — SCATTA.** `R_anello` varia il **`20.1 %`** a due masse contro il **`9.1 %`** a
  tre: **più del doppio della soglia dell'8 % fissata prima.** **Quindi la lettura assoluta è
  ALIASATA e vale la COMOVENTE** — che è **la meno generosa** (`1.74` invece di `2.31`).
  **Non ho scelto la più comoda.**
- **FALSIFICATORE 1 — era già scattato nel pilota, e resta.** `n0 = 1895` contro `2391`: il
  **`79.3 %`**, non il `66.7 %` proporzionale.

### ⚠ Cosa questo **non** dice

- **Non dice che sia l'interazione a TRE CORPI.** **`--nmasse` cambia TRE cose insieme** — numero di
  masse, **popolazione**, geometria della semina — **e le cause non sono separate.** Servirebbe un
  braccio a **due masse con la popolazione di tre**, e **non è stato fatto.** È un **limite di
  progetto**, dichiarato prima del run e non scoperto dopo.
- **Non dice che il meccanismo nominato nella lettura ② sia quello.** `lambda_nodi` che accorcia la
  portata dove la densità cresce è **un candidato NOMINATO, non MISURATO**: questo A/B **non lo tocca.**
- **Non dice niente sulla barra d'errore. UN SEME PER BRACCIO.** `×22.46` e `1.96 contro 0.99` sono
  rapporti grandi, **ma non hanno una barra e con un seme non possono averla.** **Per farne un fatto
  servono ≥ 4 semi per braccio** (par.9, `P3`).

### Un errore mio, corretto prima di usarlo

**La prima versione della sonda aveva `DT = 0.02`; il simulatore ha `DT = 0.01` (`:189`).**
I miei `r` uscivano **esattamente la metà** di quelli già committati in `Z49`, e **è stato quel
disaccordo con un numero già nel repo a farmelo vedere.** Corretto e rigirato: `r` interna a tre
masse vale ora `1.409586` contro il `1.4096` di `Z49`. **Il numero committato ha fatto da presidio.**

---

## 9.67 — **Le coorti sopravvivevano già alla mitosi. Non sopravvivevano allo snapshot** *(sigillo 9/9)*

**2026-09-18** · blob **`a1ae5090` → `b9e07c73`** · **CATEGORIA D del par.10: correzione di difetto,
NESSUN FLAG** · **il gate NON si sposta, resta `c0803713`**
**Verifica scritta PRIMA del codice:** `695ced0` · **FAIL intermedio committato:** `a872383`
**Referto:** `doc/REFERTO_coorti_snapshot.md` · **Sigillo:** `csv/_seal_fork/_sigillo_coorti.py`

### Il mandato chiedeva due cose, e **la prima era già fatta**

Il mandato diceva *«alla mitosi il figlio nasce SENZA appartenenza»*. **Dal disco, `:3951-3954`, i
figli ereditano una COPIA PROFONDA delle voci del genitore `a`, con la scelta di `a` già motivata nel
commento**; il ramo Schwinger fa lo stesso (`:4076-4082`) e `conc_archi` è riallineato
(`:3997-4001`). **`:1858` — l'`extend` con liste vuote che il mandato citava — è in `semina()`, non in
`mitosi()`, ed è corretto lì.**

> **E `S2` lo MISURA sui due bracci invece di asserirlo:** frazione di nodi con coorte non vuota
> **`0.8238` nel vecchio contro `0.8238` nel nuovo — identica**, `374` su `454`.
> **⚠ È l'`82.4 %`, non il «~100 %» della lettura fissata prima**, e il numero si riporta com'è: il
> complemento sono **i nodi seminati**, che per costruzione non hanno lignaggio.

### Il difetto vero — **una riga, e uno scarto silenzioso**

```python
:2865   if isinstance(v, (np.ndarray, int, float, bool, np.integer, np.floating, str)):
:2866       stato['attrs'][k] = v
```

**`conc_nodi` e `conc_archi` sono `list`, `masse_info` è un `dict`: non matchano, e spariscono.**
**E la docstring della funzione dichiara *«salva TUTTE le grandezze di stato … così non ne dimentica
nessuna»*: per queste tre non è vero.** **Dopo un salva/ricarica il lignaggio riparte VUOTO**, e ogni
misura di appartenenza su uno snapshot ricaricato **guarda un sistema senza storia.**

**`S3a` lo DIMOSTRA:** nel `.pkl` vecchio le tre chiavi sono `[]`, nel nuovo ci sono tutte e tre.

**La cura** aggiunge le tre chiavi **esplicitamente**, e **il filtro NON si allarga**: allargarlo
farebbe entrare anche le cache derivate (`_S`, `_perm`, `_ker_cache`) **che `carica_stato` invalida
apposta** — **e quello che entra va SAPUTO.**

### Il sigillo — **9/9**, e `S1` è il decisivo

```
    vec/nuo      n: 454 contro 454   UGUALE
      psi  phi  phivel  eta  d  d0  omega_s  _nb  pos   -> max|A-B| = 0.000e+00 su TUTTI
  [PASS] S1     shape diverse = 0, campi confrontati = 9/9, max|A-B| = 0.000e+00
```

**Lo zero non è mancanza di confronto:** la riga delle shape è stampata **prima**, e *«9/9, shape
diverse = 0»* **è parte del criterio** *(la trappola `C18`, chiusa per costruzione)*.
**⚠ E `salva_stato` è stato CHIAMATO ai passi 20 e 45 in entrambi i bracci: senza, la funzione
modificata non sarebbe stata esercitata e il PASS sarebbe stato vuoto.**
**`S4`: `_ripara_tracking` scatta `0` volte in entrambi.** **`S6`: `_sigillo_anello.py` dà `10/10` sul
blob nuovo — `Z42` regge.**

### ⚠ Il FAIL intermedio era **il mio criterio**, ed è committato

Il primo giro ha dato **`8/9`**. `S6` cercava la stringa `"FAIL"` nello stdout del sigillo figlio e
**la trovava dentro il testo esplicativo di una riga che PASSA**:

```
[PASS] P2  shape divergenti 7, max|A-B| = 0.000e+00 (0 con shape uguali = FAIL)
```

**Il sigillo figlio riportava `10/10 PASS` e `returncode 0`. Era un FAIL FALSO.**
**È par.9 alla lettera, ed è il quarto caso della stessa famiglia in questo repo** (`N3b`, `M1b`/`M3`,
`M3c`): **il criterio guarda nel posto giusto con la chiave sbagliata.** **E il costo non è
simmetrico: un FAIL falso costa più di un sigillo mancante, perché si porta dietro una diagnosi.**

Il criterio nuovo **parsa la riga `ESITO: n/m PASS`** e richiede `passati == totali` **con
`totali > 0`** *(riga mancante → `totali = -1` → **fallisce** invece di passare per assenza di prova)*,
**più** `"[FAIL]"` **con le parentesi**. **`S1`-`S5` sono identici fra i due giri.**

### Cosa resta aperto, e non è poco

- **il costo a `n = 8000` NON è misurato:** `S5` dà **`+25.6 %`** sul `.pkl` a `n = 454` *(dove gli
  archi sono già `21930`)*, **e non lo estrapolo**;
- **il TEMPO non si legge affatto:** due esecuzioni dello stesso sigillo danno **`×1.0051`** e
  **`×0.9245`** — *il nuovo più veloce del vecchio*, **che è impossibile.** **È rumore di sistema su
  60 passi**, e serve a dire **una cosa sola**: il costo **non esplode**;
- **nessuno snapshot esistente acquisisce le coorti retroattivamente:** i sei `.pkl` di `_gvideo` e i
  sei di `_g2m` vengono dal blob `a1ae5090`. **Per averle servirebbe rigirare le scene.**
- **la separazione «coorte assegnata dalla MITOSI» contro «riscritta da `chi_basc`» resta da fare:**
  **non è ricavabile dai `.pkl` neanche adesso** — servirebbero **contatori DURANTE il run**.

---

## 9.68 — **`Z9` riscritta: il kernel gira al `7.5 %` del maturo, e `Z9` aveva scambiato un valore di `r` per una costante**

**2026-09-18** · blob **`b9e07c73` INVARIATO** · **nessun run nuovo**, i dodici `.pkl` esistevano
**Task history con la derivazione, committato PRIMA:** `efd7a34` · **Previsioni:** `f3895aa`
**Referto:** `doc/REFERTO_Z9_coorti.md` · **Output:** `csv/_test_fork/_z9_coorti.txt`

> **⚠ IN TESTA:** **`--tau-luce` HA IL SIGILLO FALLITO** (par.0): ramo **NON CERTIFICATO**, ogni numero
> lo eredita. **`--chi-basc` attivo. UN SEME per scena. COORTE ANAGRAFICA, NON PER MASSA.**
> **Si è MISURATO, non curato: `TAU_A`, `ramp` e `_pesi()` non sono stati toccati.**

### Il difetto di `Z9` ha un nome, e si legge dal codice

```
:3236  self.eta += dt_n      :3038  dt_n = DT * r      :2649  ramp = min(1, eta/TAU_A)
```

> **`d(eta)/d(passo) = DT · r` ESATTAMENTE, per nodo → `passi(ramp = 1) = TAU_A/(DT·r) = 5000/r`.**
> **Il `~0.009/passo` di `Z9` è il tasso di un nodo con `r ≈ 0.9`, scambiato per una costante.**
> **Non esiste UN tempo di maturazione: ce n'è uno PER NODO.**

**Il falsificatore fissato prima non scatta:** `d(eta)/d(passo)` misurato contro `DT·r` letto dà
**`0.9977` e `0.9966`** negli ultimi due intervalli — **confermata entro lo `0.3 %`**. Nel primo dà
`0.625`, **e la ragione è misurata:** al frame 10 `r` mediano vale **`1.414119 = √2`, il TETTO di
`ritmo()`**, e scende a `~1.0`; `r` campionato ai due estremi non cattura un `r` che si muove.

**E il fatto più pulito del giro:** al frame 10 tutti i `2391` nodi hanno la **stessa età anagrafica**
(60 passi) ma `eta` va da **`0.2722` a `0.5049`** — **un fattore `1.85`**. **Stessa età, tempi propri
diversi dell'85 %.**

### Il rilievo di Luca, confermato con un numero

```
frame 400            ramp MED   fr(ramp>0.5)   fr(ramp>0.9)
coorte ORIGINALE      0.3212      0.3768         0.0000        (TRE)
TUTTA LA POPOLAZIONE  0.2171      0.1409         0.0000
coorte ORIGINALE      0.3264      0.3821         0.0000        (DUE)
TUTTA LA POPOLAZIONE  0.2207      0.1538         0.0000
```

> **La statistica di popolazione sottostima di `2.67` e `2.48` volte la maturità della coorte che
> porta la struttura.** **`ramp > 0.9`: ZERO ovunque.**
> **⚠ E la mia previsione 1 cade a metà: avevo scritto «credo nemmeno a `ramp > 0.5`». Falso —
> oltre un terzo della coorte originale ci arriva. I NODI ORIGINALI MATURANO, quando il tempo c'è.**

### Il `93 %` di `Z46` non si ripresenta — **ed è una proprietà della SCENA**

```
FERMI (r/r_floor < 2):  TRE  0 / 8 / 0 / 0 / 0 / 0     DUE  0 / 3 / 0 / 0 / 46 / 3
```

**Contro il `92.7 %` del batch di `Z46`.** **⚠ Sono SCENE DIVERSE e non si trasporta (A3c): quello che
si può dire è che la frazione al pavimento non è una proprietà del SISTEMA, ma della SCENA — e questo
QUALIFICA `Z46`, non lo smentisce.** *(Confermato indipendentemente dai contatori A8:
`_ritmo_med_sul_pavimento = 2` su 2400 passi qui, contro `1202` su 1200 passi nel batch.)*

**Estrapolazione:** `4667` passi (TRE) e `5345` (DUE) contro i `2400` fatti — **il `51.4 %` e il
`44.9 %` del cammino.**

### Il kernel — e **non è un'ampiezza pura**

**`base/base_maturo = ramp[i]·ramp[j]` ESATTO** *(gli altri due fattori sono identici nel kernel
acerbo e in quello maturo e si cancellano; l'assoluto NON è stato ricostruito, perché
`_lam_archi → lambda_nodi → massa_critica_adattiva → i pesi` è una catena RICORSIVA e ricostruirla
fuori è l'errore già fatto su `correzione`)*.

```
frame 400   p05        MEDIANA    p95        fr>0.01   fr>0.5   fr>0.9
TRE         4.122e-02  7.454e-02  3.527e-01   0.9951   0.0000   0.0000
DUE         3.367e-02  5.527e-02  2.893e-01   0.9943   0.0000   0.0000
```

**⚠ Previsione 7 SBAGLIATA:** avevo previsto `< 0.01` per la stragrande maggioranza; **il `99.51 %`
è SOPRA `0.01`.**
**⚠ Previsione 6 SBAGLIATA NEL SEGNO:** il prodotto mediano è `1.58×` e `1.13×` **il quadrato** del
`ramp` mediano, non più piccolo. **Mi era venuta subito una spiegazione — *gli archi connettono
coetanei* — e l'ho MISURATA invece di scriverla:**

```
corr(ramp[i], ramp[j]) = +0.8015 (TRE)  +0.8569 (DUE)
NULLO (estremo j rimescolato, 5 volte)  = +0.0027 +0.0012 -0.0014 +0.0009 +0.0002
```

**Duecento volte il nullo: gli archi sono ASSORTATIVI PER ETÀ.** La spiegazione regge — **ma adesso
è un numero.**

**«Diverso o solo più forte»: risposta PARZIALE.** Se `ramp[i]·ramp[j]` fosse **costante** sarebbe
un'ampiezza pura. **Non lo è: `p95/p05` passa da `2.31` (frame 10) a `8.56`/`8.59` (frame 400), e la
variazione è correlata con l'età.** **Il kernel acerbo non riscala i pesi: li RIPESA, a favore dei
legami vecchio-vecchio.** **⚠ Ma se la FENOMENOLOGIA sia diversa resta NON RISPOSTO: deciderlo
richiederebbe `≥ 4667` passi o forzare `ramp = 1`, che è CABLARE.** *(Era la previsione 8, e si è
avverata a metà.)*

### Il criterio nuovo — **due pezzi, nessuna soglia scelta**

**`Z9-a`, la condizione di regime da DICHIARARE in ogni referto che usi una scena:**
`passi_mancanti = TAU_A/(DT · r̃_MOBILI) − passi_fatti`, con **`r` LETTO** da `_r_corrente` *(mai
stimato da `eta`: sarebbe circolare)* e la mediana **sui soli MOBILI** (A3c).
**Oggi `2267` (TRE) e `2945` (DUE).**

**`Z9-b`, il criterio di chiusura:** **`Z9` si chiude quando `median(ramp[i]·ramp[j])` sugli archi
INTERNI alla coorte originale vale `1`.** **Nessuna soglia scelta: `ramp` satura in un punto ESATTO,
`eta = TAU_A`.** **Oggi `0.074950` e `0.055417` → NON SODDISFATTO di un fattore `13` e `18`**, e la
frazione di archi maturi è **`0.000000` esatto**. **E può fallire davvero:** se `r` scendesse al
pavimento il numero smetterebbe di crescere e il criterio resterebbe aperto per sempre — **ed è
esattamente ciò che è successo nel batch di `Z46`.**

### ⚠ E la parte del mio criterio che **oggi non fa lavoro** — A9

**La restrizione «archi interni alla coorte originale» serviva a togliere la diluizione dei neonati.
Misurata, non toglie niente:** `0.074950` contro `0.074540` su tutti gli archi — **quarta cifra.**

```
             nodi           grado MEDIANO   estremi d'arco
ORIGINALI    2391 (29.8 %)      496.0          861330
NATI DOPO    5627 (70.2 %)        2.0           11942     <- l'1.37 % degli estremi
```

**E il `2.0` è esattamente ciò che il codice prescrive** *(il figlio nasce con due archi verso i due
genitori, par.9)*, **verificato dai dati.**

> **A9: «un presidio che non impedisce non è un presidio».** **Quella restrizione oggi è INERTE, e lo
> dichiaro invece di venderla come protezione.** **Quello che fa funzionare il criterio è che la
> mediana è sugli ARCHI e non sui NODI** — ed è **quella** la differenza col criterio scaduto.

### Il difetto **P6** registrato

**`RUN_PARAMS` (`:6274-6296`) scrive `REGIME` e le costanti `LAM/GAMMA/SCALA_B/CS_M/K_C/PHI_CRIT` —
ma NON `TAU_A`, NON `G_PH`, NON `CALORE_INIT`: i tre numeri che DEFINISCONO il regime sono gli unici
che mancano.** Deducibili, non scritti — **e la deduzione è stata fatta con la catena più corta
disponibile, non a memoria: il `.pkl` registra il BLOB, `git cat-file -p` lo apre, e da lì si leggono
`REGIME = "deterministico"` e `_TAU_A_REGIME = 50.0`.**

### Cosa resta senza risposta

**«I nodi di QUESTA MASSA maturano?»** — `conc_nodi` non è nei `.pkl` (`Z53`), e **il presidio del
blob è stato PROVATO, non asserito** (`carica_stato` → `RuntimeError: DB RIFIUTATO`).
**Ho risposto all'altra delle due definizioni che il mandato nomina, e non la spaccio per la stessa
domanda. Per la prima servirebbe RIGIRARE UNA SCENA col blob nuovo.**

---

## 9.69 — **Il sigillo di `--tau-luce` è riparato: `6/7 PASS`. Resta `T3`, e quel `FAIL` è un RISULTATO**

**2026-09-19** · blob **`b9e07c73` INVARIATO — e il sigillo stesso lo DIMOSTRA (`T0`)**
**Fallimento committato PRIMA:** `38bd0a7` · **Riparazione committata PRIMA della corsa:** `54c9730`
**Referto:** `doc/REFERTO_sigillo_tau_luce_riparato.md` · **Task history:** `47b7804`

```
ESITO: T0=PASS  T1a=PASS  T1b=PASS  T2=PASS  T3=FAIL  T4=PASS  T5=PASS
TEMPI: T1a=93s  T1b=35s  T2=68s  T3=2975s  T4=66s  T5=66s     TOTALE 3305 s
```

> **Si è riparato il SIGILLO. La LEGGE non è stata toccata, e non lo asserisco io: `T0` misura il
> blob della fisica PRIMA e DOPO la corsa, e sono identici.**

### La diagnosi: **due criteri scaduti e un difetto del test.** La terza lettura non scatta

**`T1` asseriva «il flag OFF è byte-identico al comportamento PRIMA della modifica» ed ESEGUIVA «il
disco di oggi è uguale al codice di tre giorni fa»** — con **sette correzioni di legge sigillate** in
mezzo. **Falso per costruzione.** Riparato ancorando il confronto alla **coppia di blob che racchiude
il cambiamento** (`f5887254` → `7d484580`), entrambi pinnati, estratti in **binario**, col blob
**ricalcolato e verificato**, e con **rifiuto** se non estraibili — mai il `pre_src = ""` che degrada.

> **`T1a`: `n_A = n_B = 1718`, 21 campi, `max|A-B| = 0.000e+00`, RNG identico.**
> **IL CABLAGGIO NON CAMBIÒ IL RAMO OFF.** Era la condizione bloccante, e regge.

**E la terza lettura — «la legge è sbagliata» — NON scatta, per `T4`:** `d→2d` dà `2.000000`,
`cs→2cs` dà `0.500000`, la legge vecchia resta a `1.000000`. **`tau` è una LEGGE.**

### ⚠ `T2` — riparato, e **la diagnosi esistente era incompleta**

Il documento del fallimento dice che `_tempo_luce_nodo` è chiamato *«anche da `_bloch_ritardato`»*.
**Verificato dal disco: i chiamanti sono TRE.**

```
:2337  _passo_spinoriale   L'INERZIA (_T2 = T^2)   -- NON gated su TAU_LUCE
:2442  _passo_spinoriale   il rilassamento tau-luce, dentro `if TAU_LUCE:`
:3027  _bloch_ritardato    lo STRATO 1
```

**I primi due stanno nella STESSA funzione, quindi `co_name` non basta: il monkeypatch vecchio
cambiava TRE meccanismi, e uno dei tre è l'INERZIA, che è legge promossa e non c'entra col flag.**
Il wrapper nuovo discrimina per riga del chiamante, **ma la riga non è pinnata**: si trova a runtime
**cercando il flag** (par.0), e **se i siti non sono esattamente uno il sigillo rifiuta di girare**.

> **Risultato: `0.000e+00` ESATTO**, dove prima c'erano residui fino a `6.063e-07` **sui soli campi
> dello Strato 1** — che erano **la firma del difetto**.

### ⚠ `T3` — il criterio è rifatto, e **fallisce su dati veri**

Il criterio vecchio prendeva soglia **e direzione** da un'attesa (`-1.03`) calcolata quando `cs` era
**morto**. Il nuovo non prescrive direzione e non sceglie soglia: **l'effetto deve superare il nullo
MISURATO fra semi, su 4 semi appaiati** (`P3`).

```
DIFF ON-OFF per seme:  +0.1849   -0.0535   +1.0288   +0.8919
media +0.5130   std 0.5286   SE 0.2643   IC95 = [-0.3280, +1.3540]   t(3) = 3.182
NULLO MISURATO: std(OFF fra semi) = 0.6936      SE INTERNA tipica = 0.1129
```

**L'IC95 contiene lo zero.** **Si scrive come LIMITE (par.9): *l'effetto non è distinguibile da zero,
risoluzione `±0.84`* — e la stima puntuale `+0.51` è SOTTO la risoluzione: è NON MISURATO, non
«nessun effetto».**

> **⚠ E `C10` è confermata con un numero PEGGIORE di quello che dice: il rapporto fra dispersione
> FRA SEMI e `SE` INTERNA vale `6.1`, non `~3`.** **Il vecchio `T3` usava la `SE` interna e
> dichiarava effetti a `28 sigma`.**

**`T3-bis` riporta il rovesciamento del segno sui tre blob senza spiegarlo e senza incorporarlo** —
riscrivere il criterio finché `T3` passa sarebbe aggiustarlo, non ripararlo. **E i quattro semi
mostrano che parte di quella storia può essere dispersione fra semi, non evoluzione del codice: a
codice invariato le pendenze `OFF` valgono `+0.337 / -0.950 / +0.005 / -1.059`. I tre numeri storici
sono tutti su UN seme.**

### Cosa resta, e cosa non cambia

**Il SIGILLO COMPLESSIVO resta `FAIL`, e il gate resta a `c0803713`.** **`--tau-luce` è ancora un ramo
NON CERTIFICATO**, e ogni referto che usa quelle scene continua a ereditare il limite.
**Ma ciò che lo blocca è ora UNO SOLO (`T3`) invece di tre, e i due che sono caduti erano difetti del
SIGILLO, non della legge.**

**Il costo, misurato e NON pulito:** `3305 s`, di cui `T3` da solo `2975 s` — **e i primi ~22 minuti
hanno condiviso la CPU con un rendering video**, proprio nel tratto di `T3`. **È un limite superiore.**
Il costo sta quasi tutto nei semi: **otto** corse da 300 passi dove prima ne bastavano due. **È il
prezzo di `P3`.**

**I sigilli del giro rigirano identici:** `_sigillo_coorti` **9/9**, `_sigillo_anello` **10/10**
annidato, `62 s`.

---

## `D2` — **il criterio di rifiuto della serie era un criterio AGGIUNTO, e rifiutava il caso d'uso** (2026-09-19)

**Riscontro: `7/7`, `csv/_seal_fork/_prova_D2_rigiocata_2026-09-19.txt`, blob del simulatore
`1d42c733`, script `a3fad1a4` committato e pulito.**

Il mandato dell'archivio chiedeva di rifiutare *«una serie di un ALTRO RUN»*, e **«un altro run»
significa un'altra FISICA: il discriminante è il BLOB.** L'implementazione ha invece introdotto un
criterio di **CONTIGUITÀ** dei passi alla cadenza `--db-ogni` corrente — **mai chiesto** — e la
conseguenza è che **`--db-rigioca` non può fare la cosa per cui esiste**: infittire un archivio
significa rigirare con `--db-ogni` più piccolo, e una serie `250/500/750` **non è contigua** a
cadenza `50`.

```
P2   cadenza 50 -> 'serie NON CONTIGUA: mancano [300, 350, 400, 450, 550] (attesi 11, trovati 3)'
P3   END-TO-END: returncode=1 in 19.2 s -- il programma RIFIUTA di infittire
P3b  nessuno snapshot creato ne' toccato
```

> **⚠ E IL PUNTO CHE RENDE LA PROVA CONCLUSIVA È `P2b`, non `P2`.** Con `db_ogni = 50` i passi
> `250/500/750` **sono tutti multipli di 50**, quindi il criterio **(b)** che il commit `2c92b9d`
> dichiarava **non può scattare**. Il rifiuto viene **esclusivamente** dalla contiguità: non c'è una
> seconda spiegazione possibile, ed è **verificato**, non assunto.

**`P4` è il rovesciamento esatto del mandato, e vale più di `P2`:** gli snapshot della prova sono
**file VUOTI, 0 byte** — non sono pickle, **non hanno un blob** — e la verifica alla cadenza
legittima **li accetta**. **Il criterio implementato RIFIUTA una cadenza legittima e ACCETTA
l'ignoto**, mentre doveva fare l'opposto.

**Questo difetto non nasce da una svista di programmazione: nasce da un criterio AGGIUNTO rispetto
al mandato.** È la stessa famiglia dei criteri scaduti già catalogati in `CLAUDE.md` par.9
(*«un test può fallire perché il codice è sbagliato, o perché il criterio chiede la cosa
sbagliata»*) — **qui era il criterio**, e **il rilievo è di Luca**: io l'avevo visto come sospetto
dalla lettura, **senza vedere che la causa fosse la divergenza dal mandato**.

**Due osservazioni incidentali, dichiarate perché viste:**
- **il rifiuto costa `19.2 s`**: arriva **dopo** la semina della rete, non prima. Nessun passo è
  girato (`P3b`), ma la verifica potrebbe stare prima di costruire la scena;
- **`--nmasse 1` diventa `2` in silenzio** (`max(2, ...)` a `:6345` e `:6385`). **Non è un difetto
  nascosto**: il valore effettivo è scritto nei dati come `nmasse_effettive` (`:6352`) e stampato.
  Lo annoto perché **chi legge il comando della prova vede `1` e i dati dicono `2`**.

**Cosa NON prova questa prova:** la serie è fatta di **nomi**, non di snapshot veri, quindi **il
caricamento non è esercitato**. La rigiocata che *funziona* — dopo la correzione — va provata su
**snapshot VERI**, e quella prova non è ancora stata fatta.

## Il COSTO dell'archivio, misurato su uno snapshot vero (2026-09-19)

**`csv/_seal_fork/_costo_archivio_2026-09-19.txt`**, script `4efcc767` committato e pulito,
snapshot `csv/_test_fork/_pilota6000/pilota.pkl` — **27.73 MB** *(il task history diceva 26.45: è
lo stesso file, `MB` contro `MiB`)*.

**① La scansione del blob NON è cara, quindi il controllo si fa COMPLETO.** È la domanda che il
mandato poneva prima della correzione di `D2`:

```
pickle.load di uno snapshot: 0.156 s
  24 snapshot (6000 passi @ 250) ->  3.8 s di solo controllo all'avvio
 120 snapshot (6000 passi @  50) -> 18.8 s
 240 snapshot (2400 passi @  10) -> 37.5 s
```

> Su un run che dura **ore**, `3.8 s` all'avvio non sono un costo. **Quindi NON serve l'header né
> alcuna lettura parziale: si carica ogni snapshot e si confronta il blob**, che è ciò che il
> mandato chiedeva. *(Per curiosità: `blob` è la **terza** chiave del dizionario, quindi un header
> sarebbe stato tecnicamente possibile — ma una soluzione non necessaria è solo un modo in più di
> sbagliare.)*

**② `gzip` comprime POCO e, al livello che ho committato, costa MOLTO.**

| livello | scrittura | dimensione | rapporto | lettura |
|---|---|---|---|---|
| — (nessuno) | **0.129 s** | 27.73 MB | 1.000x | 0.156 s |
| 1 | 0.82 s | 16.08 MB | 1.725x | 0.32 s |
| 6 | 1.27 s | 15.81 MB | 1.755x | 0.31 s |
| **9 (il default, ed è quello che ho committato)** | **4.42 s** | 15.77 MB | 1.759x | 0.32 s |

> **⚠ Il livello 9 è irrazionale su questi dati, e non l'ha scelto nessuno: è il default di
> `gzip.open`.** Costa **5.4 volte** il livello 1 per guadagnare il **2 %** di spazio
> *(15.77 contro 16.08 MB)*, ed è **34 volte** più lento dello scrivere non compresso.
> **Su float64 densi `gzip` dà `1.76x` e basta** — era l'incognita dichiarata nel task history
> (*«potrebbe comprimere poco»*): **comprime poco.**

**Cosa significa su una campagna vera**, ed è il numero che serve per decidere: `2400` passi con
`--db-ogni 10` = **240 snapshot** → **17.7 minuti** di sola compressione al livello 9 contro
**31 s** senza, per passare da `6.65 GB` a `3.78 GB`.

> **NON HO SCELTO IL LIVELLO, e non lo scelgo: un livello è UN NUMERO SCELTO (par.3).** Il default
> resta `9` finché Luca non decide. **Lo riporto con i numeri, che è ciò che il mandato chiede al
> punto 5.**

**⚠ E questo NON è `V8`, è `V8` PARZIALE, dichiarato tale nello script stesso:** qui c'è **una**
scrittura e **una** lettura su **un** file. **`V8` vero deve misurare l'overhead PER PASSO dentro
un run**, cioè quanto rallenta la simulazione. Questi numeri sono un **limite inferiore onesto**,
non il costo di campagna.

## `D2` e `D1` — **curati, e la cura è provata END-TO-END** (2026-09-19)

**`8/8`, `csv/_seal_fork/_prova_D2_rigiocata_DOPO_2026-09-19.txt`**, script `b6297465`, simulatore
`d62801ab`. **Lo stesso script del «prima»**, che rileva la firma e **rovescia le proprie attese**.

```
R1  run 100 passi @25            -> snapshot [25, 50, 75, 100]            61 s
R2  la stessa serie a cadenza 10 -> guaio=None        (PRIMA: 'serie NON CONTIGUA')
R3  --db-rigioca 50 100 @10      -> NUOVI [60, 70, 80, 90]   rc=0         44 s
R4  gli snapshot preesistenti INTATTI (mtime+dimensione): 4 su 4
R5  [db] ARCHIVIO: 4 snapshot scritti, 1 saltati (gia' presenti), 0 FALLITI.
```

**Il discriminante ora è IL BLOB**, e si verifica su **tutti** gli snapshot: `0.4 s` per quattro,
e la funzione **stampa quanto è costata** *(un controllo che costa e non lo dice è un controllo che
qualcuno un giorno toglie senza sapere cosa gli costava)*.

**`P1` si è rovesciato ed è il rovesciamento che conta di più:** i file da **0 byte** che la
versione vecchia **accettava** ora sono `ILLEGGIBILE (EOFError)` → **RIFIUTATI**. Prima il criterio
rifiutava il legittimo e accettava l'ignoto; ora fa l'opposto.

> **⚠ Ho tolto ANCHE il criterio dei MULTIPLI della cadenza, che il mandato non nominava.** La
> ragione è una frase del mandato stesso — *«cadenze diverse nella stessa serie sono legittime»* —
> e il criterio dei multipli **è** un criterio di cadenza: infittire a `30` una serie scritta a
> `250` sarebbe stato rifiutato allo stesso modo, per la stessa ragione sbagliata. **Toglierne uno
> e lasciare l'altro avrebbe curato il caso provato e lasciato il difetto.** **È una decisione mia
> oltre la lettera del mandato, ed è dichiarata perché possa essere ribaltata: è una riga.**

**Due cose che ho considerato e NON ho fatto, perché sarebbero CRITERI AGGIUNTI** — cioè l'errore
appena corretto: il controllo *«passo nel nome == passo nei dati»* dentro la verifica *(è `V4`, un
**sigillo**, non un presidio d'avvio)*, e l'anticipo del rifiuto **prima** della semina *(la prova
ha misurato che il rifiuto costa `19.2 s` perché arriva dopo la costruzione della scena: è un
fastidio, non un difetto)*.

**⚠ Cosa questa prova NON è: non è `V6`.** Qui si prova che la rigiocata **gira e non distrugge**,
**non** che riproduca la stessa traiettoria. **Una scena, un seme, 150 passi.**

**Un difetto residuo, piccolo e dichiarato:** con `--db-rigioca 50 80` il messaggio di resume dice
*«ne mancano … per arrivare a `--passi`»*, cioè il totale del run, **non** il `80` della rigiocata.
Il conteggio è giusto, **la frase no**.

## ⚠ `V6` FALLISCE — **la rigiocata riproduce la FISICA byte per byte, ma non `conc_nodi`** (2026-09-19)

**`10/11`, `csv/_seal_fork/_sigillo_archivio_2026-09-19.txt`**, sigillo `dece5b2d`, simulatore
`d62801ab` *(byte grezzi `a937a098`)*. **I due BLOCCANTI PASSANO. Il DECISIVO no.**

```
V1  PRE-ARCHIVIO (b9e07c73) vs flag OFF : 97 campi confrontati, IDENTICI     PASS
V1b i due DB vengono da codici DIVERSI (7 metadati differiscono)             PASS
V2  flag OFF vs flag ON                 : 97 campi confrontati, IDENTICI     PASS
V6  rigiocata da 50 -> passi [75, 100]  : 194 campi confrontati, 2 guai      FAIL
      [V6@75]  97 campi, 1 guaio -> conc_nodi
      [V6@100] 97 campi, 1 guaio -> conc_nodi
```

**Quello che i dati dicono, e mi fermo qui perché il mandato dice di fermarsi:**

- **la FISICA è riprodotta byte per byte.** Su `97` campi, `96` combaciano esattamente a **entrambi**
  i passi rigenerati — tutti gli `ndarray`, e `rng_state`. **L'unico campo che differisce è
  `conc_nodi`**, e differisce a tutti e due i passi;
- **`conc_archi` e `masse_info` NON sono fra i guai**: delle tre strutture di `Z53` ne diverge
  **una sola**;
- **`V5` PASSA**: salva → ricarica restituisce tutte e tre le strutture identiche, **compressa**.
  Quindi **non è la persistenza**;
- `conc_nodi` è una **struttura di MISURA** (il lignaggio delle coorti), **non di fisica**: nessuno
  dei suoi lettori è chiamato da `step()`/`mitosi()`/`scuoti_vuoto()` — è scritto nel commento della
  cura del 2026-09-18.

> **NON HO UNA SPIEGAZIONE, e non la invento.** Il task history aveva dichiarato in anticipo che
> `V6` è *il test empirico* della riserva su §1 (*«un solo generatore garantisce che la CASUALITÀ
> sia riproducibile, non che lo sia ogni sorgente di non-determinismo»*). **Ma quella riserva
> riguardava la traiettoria, e la traiettoria è IDENTICA.** Il fallimento è in un posto diverso da
> quello che la riserva prevedeva.

**Cosa NON so, e serve per decidere:** il diff è **troncato a 60 caratteri** nel referto
(`conc_nodi: [[], [], [], ... != [[], [], [], ...`), quindi **non so in che cosa differiscano** —
lunghezza, contenuto, o ordine. **Il sigillo ha detto CHE differiscono, non COME.**

**Le altre voci, per completezza:**

```
V3 4 file ai passi [25,50,75,100]                                            PASS
V4 passo nel NOME == _db_step nei DATI, 4 file su 4                          PASS
V5 round-trip GZIP delle 3 strutture di Z53: 3 su 3                          PASS
V7 .pkl (1504 B) e .pkl.gz (712 B): stesso contenuto, entrambi ricaricabili  PASS
V8 100 passi @25: 66.2 s senza gzip, 76.9 s con -> +2.66 s/snapshot, +16.1%  PASS
V9 _sigillo_coorti.py rigira: 9/9 PASS in 62 s                               PASS
```

**⚠ `V8` è su una scena BREVE e NON si estrapola:** `+2.66 s` per snapshot qui contro i `4.42 s`
misurati su uno snapshot del pilota, **perché la rete a 100 passi è piccola**. Il `+16.1 %` sul run
è il numero di *questa* scena, non di una campagna.

## `V6` — **lo strumento ha parlato: la differenza è la stringa `"schwinger"`, e non è una differenza di CONTENUTO** (2026-09-19)

**`csv/_seal_fork/_sigillo_archivio_V6_dettaglio_2026-09-19.txt`**, sigillo `c56ab4df` →
terza iterazione, simulatore **invariato** `d62801ab`. **Tre giri dello strumento, e i primi due
hanno detto cose sbagliate — le riporto entrambe perché erano mie.**

**① Il dettaglio si contraddiceva:** `len A = len B = 876`, **`DIVERSI 0`**, accanto a un `FAIL`.
**② «primo byte diverso all'offset 3» era un artefatto mio:** l'offset 3 cade dentro il **campo
lunghezza del FRAME** del protocollo 5 (`\x80\x05\x95` + 8 byte). Due pickle di lunghezza diversa
differiscono **sempre** lì, e quel byte non dice **niente** su dove sia la differenza vera.

**③ Saltato l'header, la differenza è a `offset 21642` — identica ai due passi:**

```
A: ... \xf0  j=\x06\x00\x00       e a ]     <- LONG_BINGET: riferimento al MEMO
B: ... \xf0  \x8c\tschwinger\x94  e a ]     <- SHORT_BINUNICODE "schwinger" + MEMOIZE
```

> **È la stessa stringa `"schwinger"`.** In `A` era già nel memo *(stesso oggetto, riusato)*; in `B`
> è un **oggetto distinto con lo stesso valore**, quindi pickle la riscrive per esteso. **I 7 byte
> di differenza sono esattamente questo.**

**Quello che è MISURATO, non dedotto:**

| | |
|---|---|
| `repr(A) == repr(B)` | **True**, a entrambi i passi |
| oggetti distinti per identità, 1º livello | `A = 876`, `B = 876` — **uguali** |
| `pickle` p5 | `21710` contro `21717` |
| `pickle` p0 (ASCII, **senza framing**) | `39152` contro `39163` → **non è il framing** |

**La differenza è ALIASING, ma al SECONDO livello** — dentro le sotto-liste, non fra di esse. **Il
mio contatore guardava solo il primo livello e per questo diceva `876 = 876`: era una misura giusta
della cosa sbagliata.**

> **CONSEGUENZA: `conc_nodi` ha lo STESSO CONTENUTO nei due rami.** Ciò che differisce è **l'identità
> degli oggetti stringa Python**, non lo stato. **E il criterio di `V6` — confronto dei byte della
> serializzazione — è sensibile a quella identità.** Per gli `ndarray` il confronto sui byte è
> giusto; **per le strutture Python cattura anche l'aliasing, che non è stato.**

**NON cambio il criterio da solo.** Lo avevo scritto prima di vedere il numero, ed è la ragione per
cui lo scrivo anche adesso: **riscriverlo ora lo riscriverei per far passare la mia stessa
modifica**, e sarebbe il **quattordicesimo** criterio riscritto. **La decisione è di Luca.**

**⚠ E resta una domanda che i dati NON chiudono, quindi la lascio aperta invece di risolverla:**
*perché* nella rigiocata quella stringa sia un oggetto diverso è una spiegazione che **non ho
misurato**. Il fatto misurato è che **il contenuto coincide**; il meccanismo no.

## ✅ L'ARCHIVIO È SIGILLATO — `12/12` sul blob `7c4dec1d` (2026-09-19)

**`csv/_seal_fork/_sigillo_archivio_2026-09-19.txt`**, sigillo `6c039a43`, byte grezzi del
simulatore `5216c891`. **I quattro decisivi passano.**

```
V1  PRE-ARCHIVIO (b9e07c73) vs flag OFF : 97 campi, IDENTICI     PASS  [bloccante]
V2  flag ON vs flag OFF                 : 97 campi, IDENTICI     PASS  [bloccante]
V6  rigiocata da 50 -> [75, 100]        : 194 campi, IDENTICI    PASS  [decisivo]
V6b il criterio PRENDE ancora le differenze vere: 4 casi su 4    PASS  [decisivo]
V0 V1b V3 V4 V5 V7 V8 V9                                         PASS
```

### `V6` passa, e **non perché ho allentato il criterio**

**È l'unica cosa che conta di questo giro**, e la dimostra `V6b`, non `V6`:

```
aliasing rotto (deepcopy), valori intatti  -> uguale=True    atteso=True
un valore cambiato ([80][0][0]: 0 -> 1)    -> uguale=False   atteso=False
una voce aggiunta (len 879 -> 880)         -> uguale=False   atteso=False
un ndarray float64 con UN elemento cambiato-> uguale=False   atteso=False
```

**Senza `V6b`, un `PASS` dopo la riscrittura di un criterio non è distinguibile da un criterio
disattivato.** *(Quattordicesimo criterio riscritto del programma — registrato come tale in
`Z55`, e la ragione è **misurata**: l'aliasing di `pickle` non è stato del sistema.)*

**E la fisica resta il vincolo duro:** gli `ndarray` si confrontano ancora sui **byte**; i `float`
con `struct.pack` e non con `==`, così `NaN` combacia con sé stesso e **`-0.0` non passa per
`0.0`**; il **tipo** deve coincidere.

### La compressione, e la proposta HDF5 che si chiude

**`V8` misura la decisione di Luca:** `+5.7 %` sul run al **livello 1**, contro `+16.1 %` al
livello 9 — stessi 100 passi @25. **`1.76x` su float64 densi è il limite del DATO, non del
formato**, e per questo **l'ibrido `pickle`+HDF5 è chiuso**: comprimerebbe gli stessi byte con gli
stessi algoritmi.

### Il buco dei blob, **misurato invece che stimato**

```
doc/RAMIFICAZIONI.md         119 voci,  36 col blob  (30 %)
doc/COMPONENTI_PROMOSSE.md    23 voci,   0 col blob  ( 0 %)
doc/INVENTARIO_strumenti.md    9 voci,   2 col blob  (22 %)
TOTALE 151 voci, 38 col blob (25 %), e 69 CITANO NUMERI DI MISURA SENZA BLOB
```

**L'impressione era *«alcune ce l'hanno, la maggioranza no»*. Il numero è `25 %`, e
`COMPONENTI_PROMOSSE` è a ZERO su 23** — cioè proprio il registro dove si decide cosa è fisica.

> **⚠ E IL PRESIDIO ATTIVO NON L'HO TROVATO, quindi lo dico invece di scrivere l'ennesima nota.**
> Un controllo che **rifiuti** una voce nuova senza blob è possibile solo sulle **tabelle**, dove
> c'è una struttura. Su prosa libera ogni riga contiene numeri — date, percentuali, numeri di riga
> — e **un controllo che segnala tutto non lo legge nessuno.** Quello che ho scritto è una
> **misura**: non fallisce, non blocca, e **non verifica che il blob citato sia quello GIUSTO**.

### Cosa NON è stato dimostrato, e va riletto così fra sei mesi

- **il sigillo dice che la fisica NON È CAMBIATA, non che sia GIUSTA.** `V1`/`V2` confrontano il
  codice con sé stesso prima e dopo;
- **`V6` gira su UNA scena e UN seme:** dimostra che il meccanismo non perde stato, **non** che la
  rigiocata combaci su tutti i semi;
- **`V8` è su una scena BREVE:** su una campagna il costo per snapshot **cresce col numero di nodi**;
- **`Z55` resta APERTA:** *perché* nella rigiocata `"schwinger"` sia un oggetto diverso **non è
  misurato**. Il contenuto coincide; il meccanismo no.

**Il gate del programma resta `c0803713`:** questo `12/12` certifica **l'archivio** sul blob
`7c4dec1d`, **non il fork**.

## Il run a 6000 passi, letto a METÀ — `doc/REFERTO_run6000_parziale.md` (2026-09-19)

**Frame 450 su 1000**, blob `7c4dec1d`, seme **42**, dal solo CSV di progresso *(nessuno snapshot
aperto: il run sta ancora girando)*.

**Il fatto strutturale:** il sistema **aggiunge nodi e quasi non aggiunge archi**.

```
n           x3.98    (2391 -> 9511)
archi       x1.021   (429498 -> 438532)
grado medio x0.26    (359.3 -> 92.2)
```

**È l'estensione nel tempo di ciò che `Z9` aveva misurato a un istante** *(«i nati dopo sono il
70.2 % dei nodi ma portano l'1.37 % degli estremi d'arco»)*. E spiega perché il costo per frame sia
cresciuto solo del **10 %** mentre `n` quadruplicava: **il costo è sugli archi, non sui nodi.**

**Il fatto nuovo, ed è oltre dove `Z49` si fermava:** la dilatazione **non rimbalza più**.
`−1.13 %` (frame 400) → `−4.89` (425) → **`−13.25`** (450). `Z49` aveva visto un rimbalzo
(`−7.44 → −2.70 → −4.21 → +2.80 → −1.13`) e si fermava lì. **Da 2400 passi in poi accelera verso il
basso**, mentre la coerenza locale **sale** al massimo del run (`0.6867`, e ancora in salita).

> **⚠ E una coincidenza che vale la pena guardare:** al frame 400 questo run dà `n = 8018`,
> `coer_l = 0.6691`, `dil = −1.132 %` — **identici a `Z49`**, che girava sul blob `a1ae5090`.
> **Le cure entrate fra i due blob non hanno spostato questa scena di una cifra.** Osservazione,
> non misura controllata: sono blob diversi, ed è la situazione in cui `A3c` vieta di trasportare.

**Cosa NON dice:** `Z9-b`, `ramp`, `p95/p05` e il ciclo dei nodi interni **stanno negli snapshot**,
e non li ho aperti per non rubare CPU al run. L'analizzatore è pronto e committato.
**E `P10` non è decidibile da `dil`:** parla di **nodi interni in unità comoventi**, e usare la
dilatazione al suo posto sarebbe cambiare la grandezza dopo aver visto i dati.

**Un mio errore già visibile:** l'estrapolazione dal pilota dava `n ≈ 8400` a 1000 frame; al **450**
siamo già a **9511**. Sbagliata di un fattore 3-5, per la ragione che avevo dichiarato — il pilota
misurava i primi 60 frame, dove `n` **non cresceva affatto**. Le stime nuove (`24 000` / `48 000`)
vengono dallo stesso tipo di estrapolazione e **meritano la stessa diffidenza**.

## ⚠ IL RUN A 6000 SI È FERMATO AL PASSO 2700, E IL PROCESSO È VIVO (2026-09-19)

**Referto: `doc/REFERTO_blocco_run6000.md` · dati grezzi: `csv/_test_fork/_dump_2700.txt`**
*(238 righe, tutte le 113 chiavi dello snapshot; script `043922cc`)*.

```
ultimo progresso : frame 450, passo 2700, ore 16:35:05     -> FERMO DA 2h08
processo         : VIVO, 12015 s di CPU su 12060 di orologio = 99.6 %, SU UN SOLO CORE
ritmo precedente : 15.6 s/frame, stabile per 450 frame
```

**Escluso misurando:** memoria *(287 MB usati, 11.5 GB liberi)*, disco *(17 GB)*, CFL
*(`_taup_cfl_max` fermo a `0.5657`, zero clamp)*, `MAX_NODI` *(9511 su 4 000 000 = **0.24 %**)*,
`NaN`/`inf` *(**zero** su tutti gli array)*. **Lo stato al passo 2700 non è rotto.**

**Cosa stava degenerando**, negli ultimi 420 passi: `d0` massimo da **43 a 395**, `d` massimo
raddoppiato, `phivel` massimo quasi triplicato. E `d0` **non è un outlier isolato**: `p50 = 1.305`,
**1227 archi sopra 10×p50**, e l'arco peggiore ha `d0 = 394.65` contro `d = 0.0899` →
**`d/d0 = 2.3e-04`**.

> **Un dato che riguarda `Z9`, non il blocco:** `_r_corrente` ha `p90 = p99 = MAX = 1.414213`,
> cioè **oltre il 10 % dei nodi è ESATTAMENTE al tetto √2 di `ritmo()`**. E `eta` massimo vale
> `36.37` su `TAU_A = 50`: **il nodo più vecchio è al 73 % della maturazione, a metà run.**
> **Nessuno è ancora maturo**, quindi `fr(ramp > 0.9)` è ancora zero.
> **E il rischio di `P3` si sta manifestando:** i nodi con `r < 1e-4` sono passati da `0.0004` a
> `0.0026`, **sei volte in 420 passi** — è il meccanismo che farebbe **smettere di crescere `Z9-b`**.

**NON HO UNA SPIEGAZIONE DEL BLOCCO, e la dico così.** Il consumo single-core con memoria stabile
indica **un loop Python**, non numpy; ma il candidato ovvio — il CFL — **è fermo**, quindi o il
meccanismo è un altro o esiste un ciclo che il CFL non conta. `py-spy` direbbe su quale riga è
fermo, **dall'esterno e senza toccarlo**, e non è installato.

**Cosa resta salvabile: tutto.** 45 snapshot, 1.3 GB, cadenza 60, **nessun buco**, blob `7c4dec1d`
ovunque. **Le misure del §3 si possono fare su metà run senza rigirare niente** — ed è esattamente
il motivo per cui l'archivio è stato costruito. La ripresa è sigillata `5/5`.

## I TRE CRICCHETTI — **una premessa cade, un'ipotesi cade, e l'errore della premessa è MIO** (2026-09-19)

**`doc/REFERTO_tre_cricchetti.md`** · 45 snapshot del run fermato al 2700 · blob `7c4dec1d` ·
seme **42** · **un seme, una scena**, `--tau-luce` **6/7**. **Nessun run, nessuna cura.**

**① `chi_basc` — NON è una monocoltura che si ribalta.**

```
fr(perc_chi == +1):  0.0000 -> 0.1705     l'83 % e' ancora -1 al passo 2700
transizione GRADUALE: 25 snapshot su 45 fra 0.05 e 0.95, passi 1260-2700, NON finita
```

> **La premessa opposta veniva da un difetto del MIO dump:** applicava il **modulo a tutto**, e su
> `±1` il modulo dà `1` ovunque — `min = max = 1` significava *«tutti ±1»*, non *«tutti +1»*.
> **Corretto alla fonte (`c56d992`) e rigenerato**, perché il file era già uscito dal repo.
> **Seconda volta nella stessa giornata** che quella funzione mi si ritorce contro.

**E la spiegazione non vale:** il controllo di consistenza fissato *prima* — `twn` ricostruito deve
riprodurre `perc_chi` — **dà `0.972` contro la soglia `0.999`**. Quindi *«si ribalta perché `twn`
supera `PHI_CRIT`»* **non lo scrivo**. Il fatto vale; la spiegazione no.

**② `omega_s` — non è un cricchetto puro.** Mediana `0 → 51.22`, **ma 13 intervalli su 44
scendono**: la lettura *«monotono ⇒ cricchetto (A7)»* **non scatta**. Cresce la **coda**: `p90` da
`0.52` a **`1.5 × 10⁴`**.
**E il `_tau` del mandato non è quello che gira:** con `--tau-luce` ON il ramo è
`_tempo_luce_nodo`, non `TAU_A·max(dens/dens_rif, 0.05)`. Misurato **`tau/TAU_A ≈ 0.0138`**:
settanta volte più piccolo. **Il punto fisso di `A3` qui non è in gioco.**

**③ LA PORTATA — l'ipotesi CADE.** Misurato chiamando `lambda_nodi()` **dal codice vero**:

```
med(lambda) = 0.60917 COSTANTE su tutti i 2700 passi   (il pavimento sarebbe 0.12)
rc = 1.8275 IMMOBILE        rc/d da 2.119 a 1.379  ->  MAI sotto 1
ma il GRADO si separa: p50 496 -> 2,  p75 496 -> 68
```

> **La condizione che avrebbe dovuto reggerla non si verifica mai.** La separazione del grado c'è,
> **per un'altra ragione**: non è la portata che si accorcia, **sono le distanze che crescono**
> (`d` mediano `0.86 → 1.33`). **Il raggio di connessione resta fermo mentre il sistema si dilata.**

**④ L'inerzia al pavimento cresce, e il cumulato sottostima**: per **intervallo** va a `0.1152`
(30 intervalli su 43 in crescita), contro il `6.2 %` **cumulato**.

**`Z9` è RIQUALIFICATA, non chiusa** (`Z9-ter`): `eta` max `36.37` su `TAU_A = 50` → **`ramp =
0.73`**. **Il kernel stava maturando, e il sistema si è fermato mentre maturava.** La domanda non è
più *«come lo faccio maturare»* ma *«cosa succede quando matura»*.

**E le cure di ieri tengono**, in un sistema che degenera: `_ritmo_chiamate 2700` con
`f_tutto_nullo 1`, `med_sul_pavimento 2`, `snap_identico 1` — **uno o due casi su 2700**.
**`Z33`, `Z42`, `Z43` reggono.**

## LA CRONOLOGIA — **`r` non cresce: parte saturo e oscilla. E `omega_s` salta di 5 ordini in 60 passi** (2026-09-19)

**`doc/REFERTO_cronologia.md`** · 45 snapshot, passi 60-2700 · blob `7c4dec1d` · seme 42 ·
strumento `csv/_test_fork/_cronologia.py`, letture fissate **prima** in `8def0af`.

**Il fatto più netto dell'intera cronologia:**

```
passo 180:  omega_s max = 0.35        nati = 2
passo 240:  omega_s max = 7.58e+04    nati = 26
```

**Cinque ordini di grandezza in 60 passi, al 9 % del run** — e **nello stesso intervallo `r` p25
crolla** da `1.2094` a `0.2991`.

**E `r` non degenera affatto: parte già saturo.** Al primo snapshot (passo 60) `r` p25/p50/p75 vale
`1.4126 / 1.4141 / 1.4142`: **tutta la distribuzione è al tetto `√2`**. Poi crolla, e **oscilla
violentemente** — `p25` salta fra `0.05` e `1.24` fra snapshot consecutivi.

> **⚠ Il verdetto automatico dice «lettura B, candidata `r p75`», ed è FRAGILE per un difetto del
> mio criterio.** `t50` presuppone una crescita **monotona**: su una grandezza che **parte al
> massimo**, `t50 = 60` significa *«era già sopra soglia quando abbiamo iniziato a guardare»*, non
> *«si muove per prima»*. E il ritardo che fa scattare `B` è **esattamente il minimo** richiesto.
> **Non ho cambiato il criterio a posteriori**: riporto ciò che produce e perché non basta.

**Osservazione, non causa:** nello stesso intervallo la **mitosi comincia a correre** (`nati` 0 / 2
/ 26 / 185 ai passi 120 / 180 / 240 / 300). **Che coincidano è un fatto; che una causi l'altra non
l'ho misurato.**

**La bimodalità non compare di colpo:** `_deg` p25 tocca il grado di nascita al passo **540**, p50
al **1500** — si apre in **mille passi**.

**Cosa non ho fatto:** la rigiocata `--db-rigioca 180 240 --db-ogni 5`, che darebbe **dodici
istanti invece di due** dentro la finestra dell'evento. **Le quattro letture fissate prima non la
indicano — è la lettura dei dati a indicarla — e la differenza conta.**

## LE DUE FINESTRE A 6 PASSI — **due letture precedenti cadono, e il run è riproducibile da capo** (2026-09-19)

**`doc/REFERTO_finestre_fini.md`** · rigiocata **sigillata 3/3** · blob `7c4dec1d` · seme 42 ·
risoluzione **6 passi** *(il driver campiona in frame: `--db-ogni 5` non è rappresentabile, e l'ho
dichiarato prima di misurare)*.

**① `ritmo()` NON nasce saturo.**

```
passo  6: r p50 = 0.8569      passo 18: 1.3783
passo 12: r p50 = 1.2004      passo 24: 1.4141   <- AL TETTO, e non lo lascia piu'
```

> **`r` satura in 24 passi.** La lettura *«nasce fuori scala, difetto di forma»* **non è
> sostenuta**: c'è una **transizione vera e datata**. In quella finestra `omega_s` max
> **decresce** (`1.61 → 1.12`), con **zero mitosi**.

**② L'evento è al passo 198, e la mitosi NON c'entra.**

```
passo 192:  om max = 0.31   nati = 3
passo 198:  om max = 401    nati = 3      <- x1300 in SEI passi, NESSUN nodo nuovo
```

> **A 60 passi mitosi ed evento coincidevano (`Z60`). A 6 passi si separano**, e l'osservazione
> precedente **cade: era un artefatto della risoluzione.** Dopo il 198 i picchi non tornano più
> indietro — **×190 in 42 passi**.

**③ Uno schema che avevo visto, misurato e scartato.** L'apparente **antifase** fra `r` e
`omega_s`: `corr = −0.58` sulle variazioni, nullo `σ ≈ 0.316` su 10 intervalli → **1.8 σ**, e
**5 segni opposti su 10, esattamente il caso**. **Non è sostenuta e non la scrivo.**

**④ Un limite dichiarato:** `r` cambia **fra campioni adiacenti** (6 passi), quindi il periodo è
**≤ 12 passi e non risolto** — **Nyquist**. Non dichiaro un periodo, e non chiamo *oscillazione*
ciò che potrebbe essere **aliasing** (§4).

> **E il sigillo ha dato una cosa non richiesta:** `SA` mostra che **ripartendo da zero si
> riottiene byte-identico lo snapshot 60**. **Il run è riproducibile da capo** — finora era solo
> argomentato.

## IL PASSO 198 — **non è un artefatto numerico: è UN NODO NEONATO sotto il pavimento dell'inerzia** (2026-09-19)

**`doc/REFERTO_passo198.md`** · 11 snapshot a **6 passi**, rigiocata sigillata 3/3 · blob
`7c4dec1d` · seme 42 · **un seme, una scena**.

**① Non è la popolazione.** Mentre `omega_s` max fa **`×1295`**, i percentili **CALANO**:

```
        p75        p95      p99      max     | n>1e2
192   0.08953    0.1744   0.2266   0.3097   |   0
198   0.08438    0.1646   0.2144   401      |   1      <- UNO su 2394
```

**② I tre candidati numerici cadono tutti, e sono DATATI:** `_cs_lam_degenere` **`+0` in tutti e
dieci gli intervalli** *(le due occorrenze sono prima del passo 180)*; `_fatt_cs_ultimo` **fermo**
a `p50 = 1.48`; **`NaN`/`inf` ZERO** su 8 campi × 11 istanti, e zero valori oltre `1e10`/`1e15`.

**③ Chi è:** **indice 2393 su n = 2394 — l'ultimo.**

```
                questo nodo    mediana pop.
eta             0.0607         1.4968      <- NEONATO, ~8 passi
_deg            2              496         <- IL GRADO DI NASCITA
rho_spin        5.70e-10       0.0123      <- venti MILIONI di volte sotto
```

**E il pavimento dell'inerzia è `1e-6`: questo nodo sta MILLE VOLTE SOTTO.** Sei passi prima il
massimo era un altro nodo: **non era anomalo.**

**④ Vale per tutti, a ogni istante:** i nodi con `omega > 1e2` hanno **sempre** `eta` `0.04-0.16`,
**`_deg` mediano `2`**, `rho ~10⁻⁹`. E **`_sfondo_ko_rho` scatta per la prima volta esattamente al
passo 198** — è il contatore dei nodi che cadono nel fallback dello sfondo **per `rho`**.

**⑤ È un contagio:** Jaccard `1.0000` per 12 passi *(resta solo lui)*, poi `1 → 4 → 5 → 8 → 10 →
12` con Jaccard `0.62-0.83`: **nessuno guarisce.**

> **⚠ NON è un candidato nuovo: è il meccanismo che `CLAUDE.md` §9 descrive già** *(`inerzia =
> max(rho_sorgente, 1e-6)`, `omega = coppia/inerzia`)* — **ma con la natura cambiata.** Là il
> pavimento era attivo sul **99.7 %** dei nodi; **qui la densità mediana è `~10⁻²` e il pavimento è
> attivo SOLO SUI NEONATI.** **Non è più una proprietà del regime: è un difetto dei nodi appena
> nati.**

**⚠ E un difetto del mio criterio, dichiarato:** la lettura `B` non è scattata per un **rapporto
fra due mediane che valgono `~10⁻¹⁵`, cioè zero macchina**. Avevo scritto un criterio su un
rapporto **senza chiedermi se il denominatore fosse un numero**. Non l'ho cambiato a posteriori.

**Cosa NON ho misurato:** **la coppia** su quei nodi — l'ultimo anello della catena. È coerente con
tutto il resto, ma non è misurato, e non lo scrivo come se lo fosse.

## LE SOMME — **il fondo si solleva di otto ordini, e il momento netto converge** (2026-09-20)

**`doc/REFERTO_somme.md`** · blob `775ceab7` · passo 240 · tre rami · snapshot **ricostruiti e
verificati** *(ramo A: `113 campi, 0 diversi` contro l'archivio, in entrambi gli esperimenti)*.

**Nessuna delle quattro letture scatta**, e `sum|omega|/n` va in **direzioni opposte**:
**`+23.6 %`** con `COPPIA_RECIPROCA`, **`−13.8 %`** con `GRAV_AMPIEZZA`. **Le due cure non
concordano nemmeno nel segno.**

**Il reperto è un altro, e le somme non lo catturavano** — l'istogramma sì:

```
log10|omega|   -14    -12    -10     -8     -6     -4     -2
A              619    836     24      9      3     10    904
B                0      0      0      0      0   1477    900
B'               0      0      0      0      0   1472    900
```

> **Nel ramo A ci sono 1455 nodi fra `10⁻¹⁴` e `10⁻¹²`. Nei curati NON CE N'È NEMMENO UNO: sono
> tutti risaliti a `~10⁻⁴`.** Mediana `4.93e-11 → 1.88e-03` (**otto ordini**), `p25` **nove ordini**.
> **E i due rami curati sono quasi indistinguibili fra loro** (Jaccard `B` vs `B'` = `0.8333`,
> contro `0.40`/`0.48` verso A).

**E il momento netto converge:** `|sum(omega)|/n` da **`75.286`** a **`20.401`** e **`20.098`** —
**−72.9 % e −73.3 %, con i due valori a `1.73 %` l'uno dall'altro**. **Non è conservazione** *(scende
del 73 %)*: **è convergenza a un valore comune, da due punti diversi della catena.**

**Tre cose dichiarate:** `n` **non** è identico (2417/2426/2420) e le somme sono estensive, quindi
tutto è **normalizzato per `n`** · `sum(inerzia·|omega|²)` — l'energia vera — **non l'ho calcolata**,
richiede `_T2` che non è negli snapshot · e **`rel()` usava `abs()`: ha perso il SEGNO**, ed è quel
segno a contenere il reperto.

**Cosa resta aperto:** perché `1455` nodi stiano a `10⁻¹³` nel ramo A, e perché **qualunque**
perturbazione del termine di coppia li accenda.

## `f` E `median(|f|)` — **l'algebra è falsificata, `f` CROLLA, e la catena non riproduce `r`** (2026-09-20)

**`doc/REFERTO_f_e_median.md`** · blob `775ceab7` · le due finestre a 6 passi · **nessun run: i dati
bastavano** *(`psi_spin`, `_psi_spin_prec` e `_med_f_prec` sono tutti negli snapshot)*.

**① L'algebra è falsificata, con un margine enorme:**

```
passo     x DEDOTTO     x RICALCOLATO     rapporto
12          1.6            0.72065         0.45
18          4.35           0.0807754       0.019
24        224              0.0051151       2.3e-05     <- fattore 44 000
```

**② E `f` non cresce: CROLLA.** `|f|` mediana da `0.1794` a `0.00304` nella finestra `0→60`
(**−98 %**), mentre il `med` usato **sale** del `12 %`. **Nessuna delle quattro letture scatta come
scritta** — e il pavimento **non scatta mai** (`+0` in tutte e venti le transizioni, coerente col
`2 su 2700`: il contatore non conta un'altra cosa).

**③ ⚠ Il reperto nuovo:** ricalcolando `r` dalla formula di `ritmo()` nodo per nodo, **la
ricostruzione riproduce `r` al passo 6** (scarto `0.032`) **e non lo riproduce più dal 24**
(`0.0072` contro `1.4141`, scarto `1.406`).

> Due spiegazioni possibili, **nessuna misurata**: il `med` salvato non è quello usato in quel passo,
> **oppure `_r_corrente` è scritto in un momento del passo diverso** da quello in cui `psi_spin` e
> `_psi_spin_prec` hanno i valori salvati — **famiglia `Z19`, quarta occorrenza**.
> **Conseguenza: non posso concludere se sia `f` a muoversi o il metro ad accorciarsi.** Quello che
> misuro è vero di `f` **come lo ricostruisco io**.

**④ Un fatto che NON dipende dalla ricostruzione:** `_med_f_prec`, letto **direttamente** dagli
snapshot, **oscilla dell'`802 %`** fra passi consecutivi nella finestra dell'evento, contro il
**`19.1 %`** della finestra iniziale. **`Z43` dava il `62 %`: qui è tredici volte tanto, e solo
durante l'evento.**

---

## 2026-09-20 — **LA TOPOLOGIA: nessuna delle quattro letture. Il grafo è in QUATTRO PEZZI che non si toccano mai** (`Z65`)

**Blob `775ceab7`, seme 42, i 45 snapshot di `_g6000` più i 10 di `_fin_A`. Nessun run, nessuna
cura, il simulatore non è stato toccato.** Clustering **esatto, non campionato** (costo misurato:
`0.75 s` per 9511 nodi e 438 532 archi). Letture fissate prima in
`doc/TASK_HISTORY/2026-09-20_topologia.md`. → `doc/REFERTO_topologia.md`

**⚠ E il nome non si usa: si riporta la forma, coi numeri.**

**① I due presidi, e uno non era mai stato misurato.** Il grado ricalcolato da `i`/`j` coincide con
`_deg` su **45 snapshot su 45**, con zero auto-anelli e zero archi duplicati. E **`eta[k]` non
diminuisce mai**, in nessuna delle 44 transizioni: **la stabilità degli indici era un'assunzione di
`CLAUDE.md` §9** (*«i nodi si appendono in coda»*) e adesso è una misura. Tutto il seguire-le-coorti
poggiava su quella.

**② La quarta lettura — quella data per più probabile — è falsificata.** Seguendo per **2100 passi**
i 1025 nodi di grado 2 del passo 600: l'**84.0 %** è ancora di grado 2, la **mediana non si muove di
un'unità**, il massimo passa da 2 a **6**. E il test **trasversale** (che non contiene il tempo) dice
che il **36.5 %** dei nodi con `eta ≥ 16` è ancora di grado 2. **Non è un transitorio demografico: il
grado 2 è permanente.**

**③ Il fatto centrale, che nessuna delle quattro letture prevedeva.** Il grafo **intero** ha
**quattro componenti connesse, dal passo 6 al passo 2700**: `900 + 497×3 = 2391` alla semina,
`2899/2815/2119/1678` al 2700. **Non si fondono, non si spezzano.**

```
archi DIRETTI fra componenti diverse:            0
catene che uniscono due componenti diverse:      0 su 5167
```

**Zero, a tutte e tre le soglie di grado provate (`≥11`, `≥41`, `≥101`) e a entrambi i passi.**

**④ E non è una forma emersa: è la semina.** `_semina_n_masse` costruisce
`int(massa_critica_collasso()*0.8) = 497` nodi per massa, e **al passo 6 la densità interna dei tre
pezzi da 497 è `1.0000` esatta — nascono grafi COMPLETI**. In 2700 passi si diluiscono dello `0.8 %`.
Il quarto pezzo è `SEME_INIZIALE = 900` a `0.1476`, e resta a `0.1472`.

**⑤ L'istogramma è bimodale con una valle VUOTA:** su 9511 nodi **nessuno** ha grado fra `226` e
`495` (**270 valori consecutivi**), e nessuno fra `11` e `40`. **Il clustering è una dicotomia, non
un gradiente:** `C = 0` **esatto sul 100 %** dei 7120 nodi di grado ≤ 10, e **mai zero** sui 2391 di
grado ≥ 11. **Le catene sono corte e tutte interne:** l'**85 %** è lunga 1, il massimo è 11, e non
c'è nessuna scala caratteristica (decadimento monotono, nessun picco).

**⑥ Le due popolazioni non si mescolano mai.** Tutti e **2126** i nodi di grado > 100 erano presenti
al passo 60 (`1.0000`); dei **7120** nati dopo, **nessuno** supera mai grado 100 (`0.0000`); dei 2391
iniziali, **nessuno** scende mai a grado 2. Gli archi crescono del **2.1 %** mentre i nodi crescono
del **298 %**.

> **Nessuna delle quattro letture scatta:** `A` cade sulle catene fra pezzi diversi (`0.0000`), `B`
> sulla valle vuota, `C` perché il clustering dei grado-2 è **esattamente** zero, `D` perché il grado
> 2 è permanente. **Non ne invento una quinta.**
> **Quello che si vede non è una struttura che si è formata: è la condizione iniziale, più una regola
> di nascita che aggiunge nodi senza mai collegarli fra loro.**

**⑦ ⚠ Una correzione a una misura mia, dichiarata.** Il primo strumento aveva misurato che **il
100 % delle catene ha due punti d'appoggio DISTINTI** — il numero è giusto, ma **la domanda era
un'altra**: il mandato chiedeva se i due capi stessero in **pezzi** diversi, e **due nodi distinti
possono benissimo stare nello stesso pezzo**. Ho scritto un secondo strumento per prendere la
distinzione al livello del blocco, ed è lì che esce lo `0.0000`. **La misura al livello del nodo
rispondeva a una domanda che non era stata fatta.**

**Cosa questo NON dice:** non dice che la fisica non produca struttura — dice che **in questa scena,
con questa semina, la connettività non si muove**. Una scena con una semina diversa è **una misura
diversa, e non è stata fatta**. **Un seme, una scena, nessuna barra d'errore fra semi.**

---

## 2026-09-20 — **il video rigenerato dagli snapshot: le quattro componenti, guardate**

**Blob `775ceab7`, seme 42, i 45 snapshot di `_g6000` (passi 60→2700). NESSUNA FISICA ESEGUITA.**
Strumento `csv/_test_fork/_video_da_snapshot.py`, uscita `csv/_test_fork/_video_g6000/`.
Scelte fissate prima in `doc/TASK_HISTORY/2026-09-20_video-da-snapshot.md` (`d20a3ea`).

> **⚠ È UN'ISPEZIONE, NON UNA MISURA.** Nessun numero di questo paragrafo entra in un referto come
> risultato: ciò che è misurato sta in `Z65`. **E il rischio era scritto prima: il rischio è di
> LEGGERE il video.**

**① Il blob, risolto senza toccare il simulatore.** Gli stati sono del blob `7c4dec1d`, il codice è
`775ceab7`, e `carica_stato` li rifiuta. Si è usata la strada già provata: nello **script** la
logica di `carica_stato` **meno** la verifica del blob, **compresa l'invalidazione delle cache
derivate** (`_S`, `_perm`, `_ker_cache`). **Nessun flag nuovo nel simulatore, nessuna riscrittura
degli snapshot**, e il blob di ogni snapshot è stampato accanto al suo frame.

**② E le funzioni di disegno non sono cambiate fra i due blob — verificato, non assunto.** Estratte
una per una da `git cat-file -p 7c4dec1d`: `campo_spaziale`, `pozzo_grafo`, `diagnostica`,
`rilassa_disegno`, `carica_stato`, `salva_stato`, `lambda_nodi`, `_allaccia`, `intensita` sono
**tutte identiche**. L'intero delta fra i due blob è **70 righe in 5 punti** (i due flag
sperimentali, il sito della coppia, il cablaggio CLI): **nessuno tocca il rendering.** È scritto
anche in testa a ogni frame.

**③ Il presidio sui flag ha girato e passa.** I 20 flag del modulo, applicati col percorso ufficiale
(`_cli` + `_applica_regime` + `_applica_flag`), sono stati **confrontati uno per uno** con quelli
che il run stesso ha scritto nell'intestazione di `prog.csv`: **tutti uguali**. *(Se uno solo
avesse differito lo script si sarebbe fermato senza disegnare: il rendering dipende da
`SCHERMATURA`, `CAMPO_SPINORIALE`, `GAMMA`, `LAM`.)*

**④ La verifica visiva del reperto è passata su tutti e 45 i frame:**

```
componenti: 4 su 45 frame su 45
ARCHI FRA COMPONENTI DIVERSE: 0 su 45 frame su 45
P0 (grado dalla matrice contro `_deg`): 0 nodi discordanti, su tutti i frame
indici-ancora delle quattro componenti: [0, 900, 1397, 1894] — MAI cambiati
```

**Le taglie, dal primo all'ultimo frame:**

```
passo 60     900 / 497 / 497 / 497
passo 2700  1678 / 2119 / 2899 / 2815
```

**⑤ Cosa si vede — e lo scrivo come descrizione, non come conclusione.** Il pezzo che nasce da
`SEME_INIZIALE` *(il primo, indice-àncora `0`)* **si espande fino a occupare lo stesso spazio delle
tre masse e a circondarle**, mentre i tre pezzi da 497 restano **compatti e densi**. **Nel campo, a
sinistra, questo appare come materia che si addensa fra le masse.** **Nella topologia, a destra,
quei nodi sono di un altro colore e non condividono nemmeno un arco.**

> **Quindi: ciò che era stato descritto come «condensazione fra le masse» è spazialmente reale e
> topologicamente disgiunto.** **Sovrapposizione nello spazio non è connessione**, ed è la cosa che
> il video permette di distinguere e che il campo da solo non permetteva.
> **Non dico che sia «il vuoto che si struttura»: dico che sono nodi della PRIMA componente, e che
> non toccano le altre tre.** Il perché non è misurato qui.

**⑥ Un numero che lo strumento ha fatto emergere e che NON è una misura: `max|pos|` non è
monotono.** Cresce da `8.75` (passo 60) a **`16.40` al passo 1500**, poi **ritorna a `11.32`** al
2640 e risale a `12.77` al 2700. **Lo stampo perché l'ho usato per fissare l'inquadratura**, e
perché una non-monotonia dell'estensione spaziale **non era stata notata prima** — ma viene da una
pre-passata di rendering, **su un seme e una scena, e andrebbe misurata a parte prima di
significare qualcosa.**

**⑦ I limiti, dichiarati anche in testa a ogni frame:** cadenza **60 passi/frame** contro i **6**
dell'originale — **dieci volte più a scatti**, 2.2 s a 20 fps; **vista fissa** e **inquadratura
fissa** *(una camera rotante confonderebbe la lettura della separazione; un'inquadratura
ri-normalizzata a ogni frame nasconderebbe l'espansione)*; **costo misurato 1.12 s/frame**, 50 s in
tutto. **Un seme, una scena.**

---

## 2026-09-20 — **il pilota di `sep`: la soglia è misurata, e le due finestre NON si sovrappongono**

**Blob `775ceab7`, seme 42, scena N-MASSE a 3 masse. Solo SEMINA** *(la domanda si decide lì: è
`_allaccia` a collegare)*. Strumento `csv/_test_fork/_pilota_sep.py`, esito
`csv/_test_fork/_pilota_scan_sep.txt`. Letture fissate prima in
`doc/TASK_HISTORY/2026-09-20_run-masse-interagenti.md` (`eb94a48`).

**⚠ PRIMA: una premessa del mandato non reggeva, e l'ho misurata.** `sep` è il **raggio del
cerchio**, non la distanza fra le masse: con `nm = 3` la distanza a coppie è `sep·√3`. Col vecchio
`sep = 8` i bordi massa-massa stavano a **12.46**, non a `8 − 1.4 = 6.6`. **Non erano tre volte
troppo lontane: erano cinque volte troppo lontane.**

### La scansione, alla semina

```
sep    bordi mm   archi mm   bordi mv   archi mv   componenti   archi totali
1.0      0.332     668921     -3.635     303774        1          1402193
1.4      1.025     308591     -3.235     297715        1          1035804
1.8      1.718      31850     -2.835     285446        1           746794
2.0      2.064       2345     -2.635     274541        1           706384
2.19     2.393          0     -2.445     261454        1           690952
2.4      2.757          0     -2.235     244239        1           673737
4.0      5.528          0     -0.635      97590        1           527088
4.7      6.741          0     +0.065      48286        1           477784
5.5      8.126          0     +0.865      13013        1           442511
8.0     12.456          0     +3.365          0        4           429498
```

**① La soglia del contatto massa-massa è misurata e coincide col conto:** gli archi massa-massa
esistono per `sep ≤ 2.0` e sono **zero da `sep = 2.19`**. Il conto diceva
`sep < (rc + 1.4)/√3 = 2.194`, con `rc = 3·median(lambda_nodi()) = 2.400`. **Coincide.**

**② ⚠ E IL FATTO CHE DECIDE IL MANDATO: le due finestre non si sovrappongono.**

```
perche' le masse si tocchino fra loro      ->  sep <= 2.19
perche' le masse stiano FUORI dal vuoto    ->  sep >= 5.6 circa
```

> **Non esiste un `sep` in cui le tre masse si parlano DIRETTAMENTE e restano fuori dal vuoto.**
> Il vuoto è una sfera di raggio `3.94` (p95) con code fino oltre `5`: **finché le masse sono
> abbastanza vicine da toccarsi, sono anche dentro il vuoto** — e il grafo è **una sola
> componente**, non quattro.

**③ La lettura `C` è scattata sulla LETTERA, non nella sostanza.** A `sep = 1.8` c'è **una sola
componente alla semina**, che è la condizione di `C` — ma `C` diagnosticava *«le masse si sono
compenetrate»*, e **la misura dice il contrario**: i bordi massa-massa stanno a **`+1.72`**, i
centri a `3.13`, e le tre masse restano **tre addensamenti distinti** che si collegano con
**31 850 archi diretti**. **La componente unica viene dal VUOTO**, che a `sep = 1.8` le contiene
tutte e tre (bordi a `−2.84`).
> **Il criterio era scritto sull'osservabile sbagliato: il conteggio delle componenti non separa
> «masse compenetrate» da «masse dentro il vuoto».** L'osservabile giusto è il **segno del bordo
> massa-massa**, ed è positivo. **Non ho cambiato il criterio dopo aver visto i dati: lo riporto
> com'è e dico perché non regge.**

**④ Il costo, che va nella decisione:** gli archi alla semina passano da **429 498** (`sep = 8`) a
**746 794** (`sep = 1.8`): **×1.74**. A `sep = 1.0` sono **×3.26**. **Il run precedente faceva
`16.34 s/frame` e si è fermato a 2700 passi:** partire con il 74 % di archi in più **peggiora quel
punto di partenza**, e la durata a `sep = 1.8` **non è ancora misurata** — il mio stesso presidio
della lettura `C` ha fermato il pilota prima dei 300 passi, **come doveva**.

> **Mi fermo qui, come ordina il §1 del mandato, perché la scelta non è più mia:** il mandato
> descrive una scena con **masse separate che si toccano**, e **quella scena non esiste in questa
> geometria**. Le opzioni misurate sono tre, e sono nel paragrafo del referto.

---

## 2026-09-20 — **il pilota a `sep = 4.0`: la scena è quella (lettura `A`). Il vincolo è il DISCO**

**Blob `775ceab7`**, seme 42, scena N-MASSE 3 masse, **300 passi**. Strumento
`csv/_test_fork/_pilota_sep.py`, esito `csv/_test_fork/_pilota_sep4.txt`. Letture fissate prima in
`doc/TASK_HISTORY/2026-09-20_run-sep4-mediato.md` (`01946c6`).
**Il pilota non è il run: questi numeri decidono se lanciare, non entrano in un referto.**

### La scena regge — lettura `A`

```
             archi m-m   archi m-vuoto   componenti   nodi MISTI   n      rc
semina           0           97590            1            0       2391   2.400
passo 30         0           97504            1          119       2556   1.828
passo 150        0           97459            1          180       2647   1.828
passo 300        0           97447            1          196       2687   1.828
```

- **archi massa-massa: ZERO a ogni istante** — le masse non si toccano mai, **come la scena vuole**;
- **archi massa-vuoto: `97590 → 97447`, cioè `−0.15 %` in 300 passi.** **Non crollano: il contatto
  col vuoto REGGE** *(lettura `B` esclusa)*;
- **una sola componente, sempre** *(lettura `D` esclusa)*;
- **e una popolazione nuova: 196 nodi `MISTO`**, nati da archi fra gruppi diversi. **Nel run vecchio
  non potevano esistere: i gruppi non si toccavano.**

### ⚠ Il verdetto STAMPATO dal pilota è del mandato VECCHIO, e va detto

Lo script ha stampato *«QUINTA CASELLA: le masse non si parlano fra loro... è una scena diversa da
quella descritta»*. **Quella casella l'avevo scritta quando l'obiettivo era il contatto DIRETTO.**
Col mandato nuovo **l'interazione mediata dal vuoto è l'obiettivo**, quindi `mm = 0` è **la lettura
`A`, non una casella di allarme**.
> **È la terza volta in due giorni che un criterio sopravvive al mandato che lo ha generato.** Lo
> dichiaro invece di reinterpretare il numero in silenzio: **i numeri sono giusti, l'etichetta che
> lo script ci ha messo sopra no.**

### ⚠ Un'osservazione che non ho misurato, e che segnalo perché è strana

**`median(lambda_nodi())` vale `0.6092` — identico a quattro decimali — dal passo 30 al 300**,
mentre `n` cresce da 2556 a 2687. Cala una volta sola (`0.8 → 0.6092`) e **poi non si muove più**.
**Non è il pavimento** (`0.15·LAM = 0.12`). **Non so perché, e non lo invento:** è la famiglia di
`P4` — *prima di misurare se una grandezza cambia, verificare che sia libera di cambiare*.

### Il costo — **e qui il mandato va rivisto**

```
DURATA misurata:  876.6 s per 300 passi  =  2.922 s/passo  =  17.5 s/frame
                  (misurata a 100 passi: 3.03 s/passo, quindi NON sta accelerando molto)
10.000 passi a ritmo costante:  29 220 s  =  8.1 ORE    <- LIMITE INFERIORE
SNAPSHOT:  36.40 MB compresso a n = 2687  (il vecchio ne faceva ~29 a n piu' grande:
           qui pesano di piu' perche' gli archi sono 527 mila contro 430 mila)
```

**⚠ IL DISCO: `15 GB` liberi su `476`, cioè il `97 %` occupato.** È il vincolo che decide, non il
tempo.

```
--db-ogni 60   ->  166 snapshot   6.0 - 9.1 GB     lascerebbe 6-9 GB su un disco al 97 %
--db-ogni 120  ->   83 snapshot   3.0 - 4.5 GB     <- proposto
--db-ogni 200  ->   50 snapshot   1.8 - 2.7 GB
```

**Propongo `--db-ogni 120`** *(uno snapshot ogni 20 frame)*: **83 snapshot contro i 45 del run
vecchio, su 3.7 volte più passi**, e `3-4.5 GB` invece di `6-9`. **Non si tagliano i passi: si dirada
la cadenza**, come ordina il mandato.

### E un rischio che va detto prima, non dopo

**Il run vecchio si è bloccato al passo 2700 dopo 3h30, e la causa non è mai stata trovata**
*(`doc/REFERTO_blocco_run6000.md`: memoria, disco, CFL, `MAX_NODI`, `NaN` tutti esclusi)*. **Questo
run ne chiede almeno 8.** **`--db-serie` e la ripresa sigillata `5/5` sono ciò che rende il blocco
recuperabile invece che fatale** — ma la patch della ripresa **non è ancora stata riapplicata al
driver** *(`doc/STATO_RUN.md`)*. **Va fatta prima, insieme al commit di `--sep`.**

---

## 2026-09-20 — **la scansione dei quattro schemi, e ⚠ l'anomalia ① NON è quella descritta**

**Blob `775ceab7`** (sha1 dei byte grezzi) · strumento `csv/_test_fork/_scansione_schemi.py`,
esito `csv/_test_fork/_scansione_schemi.txt` · mandato in
`doc/TASK_HISTORY/2026-09-20_anomalie-viriale-zetavir.md` (`7398f94`).
**Run e test fermi. Nessuna cura applicata. Il simulatore non è stato toccato.**

### L'elenco completo, con la triage per ruolo

```
SCHEMA                                            totale   di cui FISICA
A  guardie `len(X) == len(Y)` in un `if`             91          64
B  default da `np.zeros`/`np.full` su maschera        9           7
C  saturazioni VERE (`tanh`, `clip`, `x/sqrt`)       59          35
   + clip al DOMINIO di arccos/arcsin                 8           -      (esatti, NON scale)
D  memorie `self._*` fra funzioni diverse            10           -
```

**La triage è nel codice e il criterio è dichiarato**, non lasciato all'impressione: `P5` parla di
**percorso fisico**, e una guardia dentro `_diag_completa` non sta sullo stesso piano di una dentro
`step`. **Nessuna riga sparisce dall'elenco: ogni riga porta il suo ruolo.**

**E una separazione dentro `C`:** `np.clip(x, -1, 1)` **prima di `arccos`** non è una scala — il
coseno fra due versori vive in `[-1,1]` per costruzione e il clip toglie solo l'arrotondamento.
Sono **8**, e contarli con le saturazioni vere le avrebbe sepolte.

**Delle 10 memorie di `D`, quattro sono CACHE** esplicitamente invalidate da `carica_stato`
(`_S`, `_perm`, `_ker_cache`, `_r3`); **sei portano stato fisico**: `_chi_core_nodi`, `_deg`,
`_nb`, `_psi_spinor`, `_sin2_vir`, `_spinor_lift`.

### ⚠ IL REPERTO: l'anomalia ① non è «una scala nascosta». È **un'autonormalizzazione**

**Il mandato dice: `r_rad = ampiezza` NON limitata, quindi `tanh` la confronta contro `1`.**
**Dal codice, `ampiezza` È LIMITATA — ed è essa stessa l'uscita di un `tanh`:**

```python
:4399   scala_p  = max(float(np.median(np.abs(dpozzo))), 1e-9)
:4401   ampiezza = np.tanh(np.abs(dpozzo) / scala_p)      # in [0,1)
...
:4425   r_rad = ampiezza                                   # NON riassegnata fra 4401 e 4425
:4427   t_tan = np.tanh(...)                               # in [0,1)
```

> **Quindi `r_rad` e `t_tan` sono ENTRAMBI in `[0,1)`: il confronto «ampiezza contro uno» non
> avviene, e la premessa dell'anomalia ① come scritta NON REGGE.**

**Ma al suo posto ce n'è una diversa, e appartiene a una famiglia che questo repo conosce:**

```
scala_p = median(|dpozzo|)        ->   ampiezza = tanh(|dpozzo| / median(|dpozzo|))
```

**È una normalizzazione sul PROPRIO insieme — `A3`.** E ha la conseguenza esatta del presidio
`P4`/`C12`: **`median(ampiezza) = tanh(1) = 0.76159` PER COSTRUZIONE**, sempre, qualunque cosa
faccia il pozzo. *(Stessa forma di `median(r) = 1` in `ritmo()` e di `_tau`/`_dens_rif`: due
precedenti già misurati.)*

**E l'asimmetria è il punto:**

```
r_rad  normalizzato sulla PROPRIA MEDIANA        (A3, si muove col sistema)
t_tan  normalizzato su PHI_CRIT                  (una costante del modello, dichiarata)
```

> **`cos2` e `sin2` ripartiscono confrontando una grandezza AUTONORMALIZZATA con una
> ASSOLUTA.** **La ripartizione virale è ancorata a `tanh(1)` sul lato radiale.**
> **Non l'ho misurato sui dati e non lo invento:** è un'algebra letta dal codice, e va **verificata
> sui percentili di `ampiezza` e `sin2`** prima di curare — è il PASSO 3 del mandato, e ora si sa
> **cosa** misurare.

### Perché mi fermo qui, come ordina il §5.2

**`A` ha 64 occorrenze su percorso fisico e `C` ne ha 35.** Curarle in un commit violerebbe il
par.1 *(un interruttore alla volta)*, e la mia stessa task history dice di riportare e aspettare
quando una famiglia è numerosa. **Servono due decisioni prima di procedere:**

1. **l'ordine di attacco delle famiglie** — la mia proposta: **`D` (dichiarazione, zero
   comportamento) → contatori su `②③` → `①` alla luce del reperto qui sopra → poi `A` e `C` a
   blocchi**, perché le prime tre sono chiuse e le ultime due sono programmi;
2. **se `①` vada curata come «autonormalizzazione da sostituire»** *(e allora la scala va
   **derivata**, e `median(|dpozzo|)` **non** è derivazione ma `A3`)* **oppure dichiarata e
   lasciata**, come è stato fatto per altri punti fissi già trovati.

---

## 2026-09-20 — **`scala_p`: il punto fisso è MISURATO ed è ESATTO. E la via della cura REGGE**

**Blob `0a488348`** (sha1 dei byte grezzi; git `775ceab7`) · seme 42 · **13 istanti** dei 45
snapshot di `_g6000` (`sep = 8`) **più** lo snapshot del pilota a `sep = 4.0` · strumento
`csv/_test_fork/_misure_scala_p.py`, esito `_misure_scala_p.txt` · letture fissate **prima** in
`doc/TASK_HISTORY/2026-09-20_scala-p-punto-fisso.md` (`f90fc1b`).
**NESSUN RUN. Nessuna cura applicata. Il simulatore non è stato toccato.**

### M3 — **il punto fisso c'è, ed è ESATTO**

```
median(ampiezza) = 0.761594 = tanh(1)   su 14 istanti su 14
scarto massimo |median(ampiezza) - tanh(1)| = 2.343e-11
```

> **Non era una deduzione: adesso è una misura.** *(E `M3` esisteva proprio come controllo su me
> stesso, dopo che stamattina un'algebra letta e non misurata mi aveva ingannato.)*

### M1 — **perché il punto fisso è così saldo: la scala insegue la grandezza**

```
passo      |dpozzo| p50        scala_p
60           0.01095           0.0109542
540          0.8732            0.873171
1500       198.4             198.366
2700      1499              1498.84
```

**`|dpozzo|` mediano cresce di un fattore `137 000` in 2700 passi, e `scala_p` lo segue cifra per
cifra** — perché **è** quella mediana. **Il metro si dilata esattamente quanto la cosa misurata:
per questo il nodo mediano resta inchiodato a `tanh(1)`, sempre.**

### M4 — **la firma che il punto fisso morde**

```
sin2 p50   0.0266 -> 0.255 -> 0.223        sin2 p95 = 1 (SATURO) per quasi tutto l'archivio
```

### M2 — **la misura che poteva far cadere la cura: `phi_g` NON si annulla**

```
phi_arc (per ARCO), snapshot del pilota:   min 5.004e-05
   <= 0 : 0      <= 1e-12 : 0      <= 1e-9 : 0      <= 1e-6 : 0   (0.0000 %)
phi_g  (per NODO):                          min 1.275e-07
   <= 0 : 0      <= 1e-12 : 0      <= 1e-9 : 0      <= 1e-6 : 1   (0.0372 %)
```

**⚠ E UNA CORREZIONE ALLA MIA PRIMA LETTURA, perché il blocco `M2` guarda un solo istante:** sugli
altri istanti dell'archivio **`min(phi_arc)` scende fino a `1.5e-11`** (passo 1500) e `2.4e-11`
(passo 1260). **Non è zero, ma è undici ordini sotto la mediana.**

**Eppure la divisione è SICURA, e non per un pavimento: per costruzione.**

```
phi_g >= 0 per definizione (somma di I[k]/L con I = |psi|^2 >= 0)
=>  |dpozzo| = |phi_g[j] - phi_g[i]|  <=  phi_g[i] + phi_g[j]  =  2 * phi_arc
=>  |dpozzo| / phi_arc  <=  2   SEMPRE
```

**Misurato: `max = 2` esatto, `p99 = 1.898`, zero valori non finiti su 527 452 archi.**
> **Il numeratore si annulla almeno tanto in fretta quanto il denominatore.** **Non serve un
> pavimento, quindi `A1` non viene violato, e la via REGGE.**
> **Resta un solo caso da definire, ed è una DEFINIZIONE e non una scala:** `phi_arc = 0` esatto
> implica `dpozzo = 0` esatto, cioè `0/0`. **Va scritto `0` e dichiarato**, non lasciato a un
> `np.maximum` di comodo.

### ⚠ `Y3` in anticipo — **il nuovo rapporto SI MUOVE**

```
median(tanh(|dpozzo| / phi_arc)) ai 14 istanti:
0.1353  0.1013  0.0916  0.0736  0.0947  0.1533  0.2166  0.2940  0.3336  0.3917  0.4329  0.4398  0.4398  0.1231
min 0.0736   max 0.4398   escursione 0.3662        (il VECCHIO e' 0.761594, FISSO)
```

> **Non è un punto fisso spostato: è un punto fisso SCIOLTO.** **E la traiettoria è monotona
> crescente sull'archivio** *(0.09 → 0.44 fra il passo 780 e il 2700)*, **cioè la grandezza che
> oggi non può muoversi, con la cura, si muoverebbe — e nella direzione del maturare del sistema.**
> **È il sigillo `Y3` misurato PRIMA di scrivere la cura**, e non sostituisce `Y3`: lo rende
> prevedibile.

### Cosa NON è misurato

`L` *(il momento angolare netto)* e l'effetto su `beta` di `ZETA_VIR`: **sono `Y5` e `Y6`, e
richiedono la cura applicata.** **E un seme, una scena.**

---

## 2026-09-20 — **PASSO 1 chiuso, sigillo 3/3: e il difetto NON è la lunghezza, è l'ORDINE**

**Simulatore `7aa72c4a`** (sha1 dei byte grezzi; git `2a369526`) — **il blob È cambiato**: i
contatori sono committati in `4edfab2`. Sigillo `csv/_seal_fork/_sigillo_contatori_guardie.py`,
esito `_sigillo_contatori_guardie.txt`. Mandato in
`doc/TASK_HISTORY/2026-09-20_tre-guardie-silenziose.md` (`93e1628`).

```
V1  PASS   7 campi (psi, d, phi, eta, n, pos, tw): TUTTI IDENTICI   -> la contabilita' e' INERTE
V2  PASS   i contatori si leggono a fine run: 5 siti su 5
V3  PASS   tutti e 5 scattano quando devono (forzando una lunghezza sbagliata)
```

### I numeri, e il quarto è quello che decide

```
sito            invocazioni   salti   frazione   shape al fallimento   QUANDO (ultimo salto)
kernel_alpha         145        0      0.0 %          -                    -
tempo_luce            34        0      0.0 %          -                    -
tors4pi               12        0      0.0 %          -                    -
zeta_vir_a            12        1      8.3 %     (-1, 429498)              1  di 12
zeta_vir_b            55       11     20.0 %     (-1, 429498)             11  di 55
```

**① Tre guardie su cinque non saltano MAI** *(su 145, 34 e 12 invocazioni)*. **Restano difetti di
FORMA** — un ramo silenzioso non è un ramo — **ma non sono difetti ATTIVI.**

**② Le due `ZETA_VIR` saltano, e `shape[0] = -1` dice PERCHÉ: `_sin2_vir` è `None`, non di
lunghezza sbagliata.** **Non è un problema di lunghezza: è l'ORDINE.** `_sin2_vir` lo scrive
`memoria_hebbiana_moto`, che nel ciclo gira **dopo** `step`: alle prime invocazioni la memoria
**non esiste ancora**. **È l'anomalia ④ del mandato precedente, misurata invece che congetturata.**

**③ ⚠ E IL «QUANDO» CAMBIA LA DIAGNOSI, che è la ragione per cui l'ho aggiunto.** `zeta_vir_b`
salta il **20 %** delle invocazioni — un numero che da solo suona come difetto sistemico. **Ma
l'ultimo salto è all'invocazione `11` di `55`:** i salti sono **confinati all'inizio**, e dopo
**non accade mai più**.
> **Transitorio, non comportamento principale.** **`A8` chiede esattamente questo, e i due casi
> danno lo STESSO conteggio:** senza il `quando`, avrei riportato un `20 %` che significa un'altra
> cosa.

*(`zeta_vir_b` ha 55 invocazioni contro 12 passi perché il ramo Verlet gira a sottopassi CFL.)*

### Lo stato, e cosa resta

**Il `PASSO 2` è ACCODATO per decisione di Luca:** si torna a `scala_p`, che è più avanti.
**Nulla si perde:** i contatori sono **byte-inerti e sigillati**, e restano come **presidio
permanente**. **Ma il riferimento dei sigilli successivi non è più `775ceab7`: è `7aa72c4a`.**

**E il mandato delle guardie va corretto dove sbagliava:** `ca02af0` non è il primo commit
*(è `0ebaa4a`, 28 agosto)* e **nessuno dei siti viene da lì**. **Il criterio che regge è
*«nessuna ragione dichiarata nella storia»***, confermato dai messaggi d'origine
*(«Implement code changes…», «TestAperti»)*.

---

## 2026-09-20 — **`scala_p` curata (5/5) e `PASSO 2` chiuso (3/3). E il freno anisotropo adesso frena**

**Simulatore `f81c4fe1`** (sha1 dei byte grezzi; git `af8a96f1`) · **nessun run lanciato** ·
`Z67` e `Z68` nel registro.

### `scala_p` — il punto fisso è sciolto

```
Y1  PASS   riduzione al limite A==B: 7 campi BYTE-IDENTICI
Y2  PASS   controllo positivo: 6 campi su 7 differiscono
Y3  PASS   median(ampiezza)  0.761594156 (= tanh(1))  ->  0.142251920
Y4  PASS   sin2  mediana 0.007224 -> 0.197120     p95 1.000000 (SATURO) -> 0.980561
Y6         moltiplicatore di beta (1-sin2)  0.992776 -> 0.802880   (-19.13 %)
Y5         |L|  157.81 -> 154.80   (rapporto 0.9809)
Y7  PASS   zero NaN,  max||nb|-1| = 1.11e-16
Y8         rigirati: _sigillo_sep_driver 4/4,  _sigillo_ripresa_scena 5/5 -> nessuno si muove
```

**`Y1` è la prova che la forma algebrica è esatta:** `np.divide(ad, den, where=den>0)` con
denominatore positivo riduce **bit per bit** alla vecchia espressione. **`Y3` è il sigillo della
cura:** `tanh(1)` a nove cifre con la scala vecchia, `0.1423` con quella nuova.

**E `Y6` è la conseguenza che conta:** il moltiplicatore di `beta` passa da `0.993` a `0.803`.
**Prima `ZETA_VIR` era acceso e non frenava quasi nulla** — perché `sin2` era schiacciato dal punto
fisso. **Adesso frena del 19 %.**

### `PASSO 2` — la diagnosi era sbagliata, e il `PASSO 1` è servito a questo

**Il mandato diceva «guardie che saltano per lunghezza sbagliata».** La misura dice **`-1`**, cioè
**`_sin2_vir is None`**: **è l'ORDINE, non la lunghezza.** **Estendere un array non avrebbe
risolto niente, e avrebbe aggiunto codice che sembra una cura.**

**E i salti sono i primi, consecutivi — dimostrato, non assunto:** `quando` è l'indice dell'ultima
invocazione saltata, gli indici sono distinti e `>= 1`, quindi **11 indici distinti col massimo
`11` sono esattamente `{1..11}`**. Transitorio di avvio.

**Le tre cure sono tutte byte-inerti** (`V1`: 7 campi identici), e nessuna introduce un numero:
- **A** — `else` che **dichiara** che al primo giro non c'è freno anisotropo. **Non si inizializza
  `_sin2_vir`**: `0` è freno pieno, `1` è freno nullo, **qualunque valore è `A1`**, e non c'è
  niente da cui derivarlo. **La frazione di salti resta quella, ed è dichiarata invece che
  azzerata;**
- **B** — le tre inerti dichiarano il ramo alternativo. **Si curano benché non scattino:** difetti
  di **forma**, non di frequenza;
- **C** — il default `np.zeros` è dichiarato **e contato**: **`0` archi fuori dal `mask` su 12
  invocazioni**.

### ⚠ Tre difetti miei, in un giro

1. **il cast a `float`** per riportare lo scarto massimo **scartava la parte immaginaria di `psi`**
   — **lo stesso errore di `_mod()` di stamattina, la seconda volta in un giorno**. Non ha falsato
   verdetti *(il confronto è `np.array_equal`)*, ma su una differenza immaginaria avrebbe stampato
   `0` su un campo diverso;
2. **`V2` era un criterio scaduto** e ha prodotto un **FAIL falso** quando `C` ha aggiunto
   legittimamente un sesto contatore. **La domanda giusta è «ci sono tutti quelli attesi», non
   «quanti sono»;**
3. **tre messaggi di commit bucati dai backtick** in `git commit -m`. **Salvato come regola: sempre
   `-F`.**

### Cosa resta aperto, col conto

`A` **91** guardie *(64 su percorso fisico)* · `B` **9** default su maschera *(7)* · `C` **59**
saturazioni vere *(35)* · `D` **10** memorie fra funzioni *(6 con stato fisico)*.
**In questo giro ne sono state curate 7.**

---

## 2026-09-20 — **PASSO 1 sui dieci: `3/4 PASS + 1 FAIL ATTESO`. E il FAIL è il reperto**

**Simulatore `f81c4fe1 → dbadb71f`** *(byte grezzi; git `af8a96f1 → 5fc5bfdf`)*, commit `93421eb` ·
sigillo `csv/_seal_fork/_sigillo_passo1_dieci.py` (`849dd25`), esito `_sigillo_passo1_dieci.txt` ·
**nessun run.**

```
W1  PASS         7 campi (psi, d, phi, eta, n, pos, tw): TUTTI IDENTICI -> contabilità INERTE
W2  PASS         i dieci contatori si leggono: 10 su 10
W4  PASS         le due (b) sono SPENTE al 100 % (flag/costante off), come atteso
W3  FAIL ATTESO  una (a) non scatta -> ed è la riclassificazione, non un difetto
```

### La misura, su 12 passi

```
nb_prec           1 salto su 12    shape (-1, 2391)    quando = 1
tutti gli altri   0 salti
```

**`shape[0] = -1` significa `_nb_prec is None`**, e `quando = 1` dice che è **solo la prima
invocazione**. **È lo stesso transitorio d'avvio di `zeta_vir` (`Z68`), e la stessa causa:
l'ORDINE** — `_nb_prec` è scritto **dentro** `_passo_spinoriale`, quindi alla prima chiamata non
esiste. **La diagnosi che avevo dato è confermata da un numero.**

### ⚠ `W3` — e il criterio era diverso per classe, scritto PRIMA

```
(a) nb_prec           SCATTA
(a) snap_psispin      SCATTA
(a) nb_grav_proiez    NON forzabile   <- il FAIL
(c) chicore_passo     SCATTA corrompendo perc_chi
(c) temposegno        SCATTA corrompendo perc_chi
(c) spinore_vivo      SCATTA corrompendo phi_s
(c) calore_chi        NON forzabile
(c) chi_da_spinore    NON forzabile
```

**`:4586` va RICLASSIFICATA da `(a)` a `(c)`, ed è la più forte delle sei:** quattro righe sopra la
guardia c'è una **riparazione di `_nb`** che gira sotto **lo stesso flag `SPINORE`**. Non è che sia
difficile farla fallire: **non è raggiungibile.**

> **⚠ E la predizione è in `849dd25`, il commit che introduce il sigillo — ANTENATO del run.**
> *«nb_grav_proiez potrebbe NON scattare, perché quattro righe sopra la guardia c'è una riparazione
> di `_nb` che gira sotto lo stesso flag SPINORE. Se così fosse, quella (a) andrebbe
> RICLASSIFICATA (c) — e sarebbe un reperto, non un errore.»*
> **Il `FAIL` si cita così: `3/4 PASS + 1 FAIL ATTESO`, mai `4/4`.** *(Stessa convenzione di
> `S1a`/`S1b` nel ri-sigillo dello Strato 1.)*

### E le `(c)` si spaccano in due, il che non era previsto

- **`(c)` FORTI — non forzabili nemmeno corrompendo lo stato:** `calore_chi`, `chi_da_spinore`,
  **e ora `nb_grav_proiez`**. **La guardia non è raggiungibile: il contatore vale solo come
  sentinella di regressione;**
- **`(c)` DEBOLI — scattano se si corrompe `perc_chi`/`phi_s`:** `chicore_passo`, `temposegno`,
  `spinore_vivo`. **La guardia È raggiungibile da uno stato malformato**, anche se nessun percorso
  del codice lo produce oggi. **Lì il contatore serve davvero.**

> **La distinzione non esisteva prima di questa misura, ed è più utile della classificazione
> originale:** *«ridondante»* non è una proprietà unica. **`calore_chi` è protetta dalla forma del
> codice; `spinore_vivo` è protetta solo da un'INVARIANTE che tre funzioni mantengono.**

**Bilancio: `(a)` 2 · `(c)` 6 · `(b)` 2.**

---

## 2026-09-20 — **il pannello fedele: e il nucleo NON è il colpevole. La sovrapposizione è VERA**

**Simulatore `27f1ab03` INVARIATO** *(è rendering)* · strumento `csv/_test_fork/_video_da_snapshot.py`
(`3a7df5a`), 45 frame dai soliti snapshot · **costo del pannello nuovo: `0.01 s/frame`**, contro
`1.14 s` del frame intero. **Nessun run.**

### Cosa fa, e perché è la stessa legge

`campo_spaziale` calcola `|conv(S, K)|² − conv(n, K²)`: **il nucleo `K` sparge ogni nodo su una
portata `λ`, ed è quello che RICOSTRUISCE il campo fra i nodi.** Il pannello nuovo prende
**`K = δ`** — nessuna spargitura — e la stessa formula diventa, cella per cella,
`|Σz|² − Σ|z|²`: **l'interferenza fra i nodi che stanno davvero lì.**
**Non è un'approssimazione diversa: è la stessa legge a risoluzione piena.**
**E i buchi sono TRASPARENTI, non neri:** *«campo nullo»* e *«nessun dato»* sono due cose diverse.

### ⚠ IL REPERTO, ed è l'opposto di quello che mi aspettavo

**Al passo 60** il pannello col nucleo mostra una nuvola diffusa **fra** le masse; il fedele mostra
il vuoto come **un blocco compatto al centro**. **Lì il nucleo spargeva davvero.**

**Al passo 2700 no:** il fedele mostra le quattro popolazioni **sovrapposte nello spazio**,
esattamente come il pannello col nucleo. **La sovrapposizione è VERA, non un artefatto del
rendering.**

> **Quindi l'errore di lettura non era «il pannello inventa struttura».** **Era: il pannello non
> può distinguere SOVRAPPOSIZIONE da CONNESSIONE — e nessun pannello di campo può.**
> **Quella distinzione la fa solo la topologia, ed è per questo che i tre pannelli stanno insieme:**
> **continuità · fedeltà · topologia.** Al passo 2700 i primi due dicono *«un'unica struttura»* e il
> terzo dice **`4` componenti, `0` archi fra loro.**

### I numeri, dichiarati su ogni frame

```
passo    n      celle 3D vuote   colonne vuote   celle con >= 2 nodi   (% delle OCCUPATE)
60      2391      99.77 %          95.58 %            228                  26.9 %
600     3433      99.71 %          88.31 %            120                  11.0 %
1800    5938      99.51 %          82.25 %            495                  27.0 %
2700    9511      99.31 %          86.77 %           1200                  46.6 %
```

**`celle con >= 2 nodi` è il numero che decide:** l'interferenza richiede **due** contributi, quindi
**è DEFINITA solo lì**. **Al passo 600 lo è nell'`11 %` delle celle occupate; al 2700 nel `47 %`.**
**Tutto il resto, nel pannello di sinistra, è il nucleo.**

**E il sistema occupa meno dell'`1 %` del volume inquadrato** *(celle 3D vuote fra `99.3` e
`99.8 %`)*: **l'inquadratura fissa, scelta per non nascondere l'espansione, mostra soprattutto
vuoto** — ed è corretto che lo faccia.

---

## 2026-09-20 — **`chi_basc` fa l'OPPOSTO del suo scopo: blocca la mitosi e dimezza l'olonomia netta**

**A/B `csv/_seal_fork/_ab_chi_basc.py`, sigillo `4/4`** · simulatore `edb8f844` *(byte grezzi)* ·
**60 passi per braccio, un seme, una scena** · **due CONFIG, lo stesso codice** *(il default di
modulo è già `CHI_BASC = False`: è il driver che lo accende)*.
**`Z1` byte-identico** contro il simulatore pre-contatori → **la strumentazione non tocca la fisica.**

### ① Con `chi_basc` acceso, in 60 passi **non nasce niente**

```
                      A (chi_basc ON)     B (OFF)
n                          2391            2494
N(+1)                         0            1267
N(-1)                      2391            1227
differenza                -2391              40
nati da mitosi                0              70   (27 eventi)
nati da Schwinger             0              33   (17 eventi)
```

### ② E il meccanismo si legge

`chi_basc` rende `perc_chi` **uniforme** — in A **tutti e 2391 a `−1`** — quindi **le differenze
chirali si annullano**, quindi `twist_dip = π/2·(chi[i] − chi[j]) = 0`, quindi **`tw` non cresce**:

```
tw  mediana    0.648  ->  2.288          twn mediana   0.748  ->  2.783
```

**Senza torsione la soglia di mitosi non si abbassa.** **`chi_basc` non «rompe la simmetria»:
la IMPONE.**

### ③ L'olonomia netta va nella direzione **opposta** a quella dichiarata

```
olonomia_media (FIRMATA)   -0.158  ->  -1.366        x8.7 PIU' GRANDE senza chi_basc
olonomia_media_assoluta     7.168  ->   7.217        (le assolute non vedono niente)
```

Lo scopo dichiarato era *«senza, le chiralità 50/50 si bilanciano e azzerano l'olonomia netta»*.
**Misurato: accade il contrario.** *(E le medie assolute non lo avrebbero mai mostrato — è
esattamente il motivo per cui la media firmata andava aggiunta.)*

### ④ ⚠ Ma `L` va nell'altro verso, e le due grandezze **divergono**

```
|L|      993.4  ->  65.8      rapporto 0.066
per nodo 0.415  ->  0.0264    quindi NON e' un effetto di taglia
```

> **Olonomia netta `×8.7` SU, `|L|` `×15` GIÙ.** **Non le concilio: è il reperto.**
> **E le due letture fissate prima NON coprono questo caso:** `α` *(l'olonomia sopravvive →
> ridondante)* e `β` *(si azzera → serviva)* **presupponevano che olonomia e `L` andassero
> insieme.** **Non ci vanno.**

### ⚠ E un difetto della mia misura, dichiarato

`coer_l`, `coer_g` e `dil` tornano **`nan` in entrambi i bracci**, mentre **nel CSV del run vero
valgono `0.64`-`0.69`**. È un **artefatto del mio ordine di chiamata** *(`diagnostica()` dopo
`circolazione_topologica()`)*, **non del codice**: quei tre numeri sono **non misurati** qui.

---

## 2026-09-20 — **⚠ RITRATTAZIONE: l'A/B di `chi_basc` era la FINESTRA. Rifatto, si ribalta**

**La verifica chiesta da Luca ha morso, e il mio esito precedente era un artefatto.**

### La causa: **l'A/B partiva dal passo ZERO**

Il runner fa `avvia_test("N-MASSE")()` e poi i passi: **semina e va**. E nel run vero, **con
`chi_basc` ACCESO**, `n` resta **`2391` fino al passo `120`** — le prime nascite sono fra `120` e
`180`. **La finestra `0→60` è l'assestamento di semina, non il regime.**

### Rifatto dal passo `192`, `120` passi: **tutte e tre le conclusioni forti cadono**

```
                        finestra 0->60          finestra 192->312
                        A (ON)    B (OFF)       A (ON)    B (OFF)
nati totali                0        103           215       260      (+21 %, non 0 contro 103)
  di cui mitosi            0         70           168       193
  di cui Schwinger         0         33            47        67      (-30 % con chi_basc)
tw mediana             0.648      2.288         1.367     1.361      IDENTICI (0.4 %)
olonomia netta         -0.158    -1.366         1.810     1.270      SEGNO OPPOSTO fra finestre
|L|                     993.4      65.8         89.05    336.80      x0.066  ->  x3.78
```

**① La mitosi NON è bloccata:** `+21 %` di nascite senza `chi_basc`, non `0` contro `103`.
**② `tw` è IDENTICO** *(`1.367` contro `1.361`)*: **il fattore `3.5` della prima misura era
l'assestamento di semina**, non la legge.
**③ ⚠ L'olonomia netta e `|L|` si INVERTONO cambiando finestra.** Erano `×8.7` su e `×15` giù;
adesso sono `−30 %` e `×3.78` su. **Due grandezze che si invertono cambiando finestra non sono
misurate: sono rumore di transitorio.**

> **Quindi la «divergenza fra olonomia e `L`» che avevo registrato come REPERTO non è un reperto:
> è la stessa instabilità, vista due volte.** **La ritiro.**

### Cosa resta, e non è poco

**A regime, `chi_basc` acceso dà meno nascite: `−17 %` in totale e `−30 %` sulle sole coppie di
Schwinger** *(`47` contro `67`)*. **È l'unico effetto stabile fra le due finestre**, e tocca
proprio il ramo che **conserva** la carica *(`Z71`)*.

### ⚠ E un limite della finestra rifatta, che va dichiarato

**Lo snapshot di partenza è stato prodotto CON `chi_basc` acceso**, che aveva già omogeneizzato
`perc_chi` a `−1`. Quindi **anche il ramo B parte da `Nm1 ≈ 2580`**, e la `differenza` è dominata
dalla **condizione iniziale ereditata**, non dalla legge.
> **L'A/B rifatto misura la DINAMICA successiva, non la CARICA.** Per misurare la carica servirebbe
> una rigiocata **da zero** in entrambi i rami, lunga abbastanza da superare l'assestamento — che è
> un run, non una finestra.
