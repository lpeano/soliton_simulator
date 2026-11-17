# IL FILO DELLA RICERCA, IN SALVO E IN SOSPESO *(Luca `2026-11-17` `09:19`-`09:20`)*

> ### **LA VERIFICA NELLA SCATOLA GIUSTA** *(`doc/PIANO_VERIFICA_SCATOLA.md`)* **E' SOSPESA e si rifara'** *(decisione di Luca, `09:19`)*. **Nessuna corsa si riprende stasera.**
> **Questo documento salva TUTTO il filo di questi giorni** *(decisione di Luca, `09:20`)*: cosa e' stato trovato, cosa e' stato corretto, le domande aperte, i test da fare *(con le previsioni gia' scritte)*, lo stato delle corse e come riprenderle, e il resto del repo in sospeso *(parte `7`)*.
> **Il testo delle parti `1`-`6` e' del guardiano.** Claude Code lo ha portato qui **controllando ogni numero contro il referto citato**: **un numero che non torna NON e' stato cambiato** -- accanto c'e' *«il referto dice ...»*; **uno senza fonte** ha accanto *«la fonte: non trovata»*. La carta: `doc/TASK_HISTORY/2026-11-17_sospeso_filo.md` *(`74579055`)*.

> **Il MANDATO UNICO di Luca delle `09:49`** *(che sostituisce quello delle `09:20`)* **riprende queste parti come A** *(A1-A5 = parti `1`-`3`, `5`, `6`)* **e B** *(B1-B6 = parte `7`)*; **B4, le considerazioni delle `11:47`, resta SENZA TESTO** *(Q-A1 della ROTTA, R-QUALITA')*. La carta: `doc/TASK_HISTORY/2026-11-17_mitosi_primo_passo.md`.

## LE SEGNALAZIONI DEL CONTROLLO *(i numeri e le frasi che non tornano o non hanno fonte; NESSUNA cambia una previsione da confermata a fallita)*

1. **A, B2-pi:** la partenza «`35`» e' la `d` nominale; **la misurata e' `37.048`**; la fascia `39.89`-`42.42` vale **da `k 8000`**; «i minimi e i massimi salgono» e' detto **da due cicli**.
2. **B:** la forza a `d 66` *(`L 243`)*: **finestra `250`-`1814`** *(la corsa al tetto)*, **e la soglia di Gauss rivista DOPO il risultato** *(dichiarato)*; «la coda lunga attrattiva (probabilmente U)»: **la fonte non trovata come frase**.
3. **C e Q7:** **`1.52` e' il rapporto MISURATO / PREVISTO** della pattinatrice, **non l'accelerazione che la pattinatrice prevede**; il «`1.5`x contro `4`-`5`x» e' la stima del guardiano scritta prima.
4. **C, i DUE STRATI** *(`27`-`32` avanti, `17`-`27` fino a `-23` gradi a `k 5000`)* **e «quasi un anello, a tratti sei gobbe»: la fonte non trovata.**
5. **D, le culle che SEGUONO la materia** *(`0.1`-`2` nodi, `+-5` gradi)* **e il guscio `0.44` -> `0.21`: la fonte non trovata**; **la correzione «le culle ferme -> era il guscio» (parte `2`, riga `3`) non e' scritta da nessuna parte**, e `doc/CONSIDERAZIONI/2026-11-15_triangoli.md` dice ancora «le culle nel vuoto restano».
6. **Q11:** **il mandato delle `13:04` sui vortici `+1`/`-1` non e' nel repo ne' nelle mie trascrizioni** *(coerente con «non mandato»)*.
7. **Q17:** «il motore fuso circa `10`x»: **la fonte non trovata** *(c'e' «`4`-`12`x» per le tre funzioni del secondo passo)*.
8. **7.1:** la voce `7` della ROTTA ha **`0.0128`**, non `0.0178`; la voce `8` *(il video triplo)* e' **CHIUSA** *(`102814bd`)*, non «mai girato»; la voce `20` scrive ancora «IN CORSO sul ramo» su un ramo chiuso.
9. ### **7.4: le considerazioni delle `11:47` del `2026-11-16` NON sono scritte: il testo di quel mandato non lo trovo** *(serve che venga incollato)*.

## PARTE 1 -- COSA ABBIAMO TROVATO

> ### ⚠ **LE PARTI A-E SONO SU `L 162`, DOVE R-SCATOLA NON E' RISPETTATA** *(la domanda Q1)*.
> **Come leggere le note in corsivo:** *«il referto dice ...»* = il numero del guardiano NON torna col referto, e resta com'e' con accanto quello del referto; *«la fonte: non trovata»* = non l'ho trovato in nessun referto, task history, relazione o messaggio di commit *(nemmeno nel worktree del mattone)*: **non e' smentito, e' senza provenienza** (`L-NUMERI`). Le fonti: `M/` = `doc/referti_l2/mattone/`; `TH-M` = `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`.

### A. Gli oggetti legati *(su `L 162`, mondo G+U, i mattoni `L162_MGU_03000`)*

- **il triangolo a `120` gradi:** il lato `39.26` *(k 0)* -> massimo `39.94` *(k 2100)* -> minimo `32.67` *(k 8600)* -> `38.79` *(k 12000)*; **il giro `+1` in tutte le `12` in `61` controlli su `61`; P4 confermata.**
  *Fonte: `M/legati_lettura_t120_3.txt` («da 39.2573 (k 0) a 38.7910 (k 12000); max 39.9362 a k 2100; min 32.6670 a k 8600»); `TH-M` («61 controlli su 61», «P4 PASSA»). Tutto torna. (La serie non lisciata di `M/triangolo_t120_rotazione_B.txt` ha il minimo `32.661` a `k 8650`.)*
- **la coppia in fase (B2):** minimo `28.72` *(circa k 5100)*, massimo `33.77` *(k 9950)*, minimo `29.40` *(k 14750)*; il periodo circa `9700` tick; **P1 e P1-bis confermate.**
  *Fonte: `TH-M` («dal minimo 28.72 (k 5100)», «al MASSIMO 33.77 a k 9950», «P1-bis PASSA»); `M/legati_lettura_GU2.txt` («min 29.3990 a k 14750», «9700 tick», P1 «CONFERMATA»). Tutto torna (la serie lisciata: `28.7277` a `k 5050`, `33.7514`).*
- **la coppia in antifase (B2-pi):** `35` -> `39.46` *(k 2000)* -> massimo `41.21` *(k 4350)* -> fra `39.89` e `42.42` fino a `k 18000`; il periodo circa `7700`; **i minimi e i massimi SALGONO a ogni giro; P2' FALLITA, P2'' confermata.**
  *«il referto dice»: la partenza MISURATA e' `37.048` (`d0` vera, `M/coppia_GUpi_L162.txt`; `M/legati_lettura_GUpi2.txt` «da 37.0483 (k 0)»): `35` e' la `d` NOMINALE della scena. La fascia `39.89`-`42.42` vale da `k 8000` (`TH-M`: «39.8906-42.4156 in 8000-17042»). Il periodo: `7667` tick. «Salgono»: `TH-M` lo dice da DUE cicli («min 39.87 -> 41.16, max 41.20 -> 42.41»), e aggiunge «da due cicli non si dice se e' una deriva». Il resto torna.*

### B. Le forze

- **a `d 35` in fase `-1.010266e-6`, in antifase `+3.605169e-7`** *(L 162)*; **a `d 51` in fase `-2.615720e-8`** *(L 162)*; **a `d 66` in fase `-1.337978e-8`** *(L 243)*. **La regola di fase: in fase attraggono, in antifase respingono; una coda lunga attrattiva** *(probabilmente U)*.
  *Fonte: `M/coppia_GU_L162.txt` (`-1.010266e-06 +- 5.2e-09`), `M/coppia_GUpi_L162.txt` (`+3.605169e-07 +- 6.8e-09`), `M/coppia_GUd50_L162.txt`, `M/coppia_GUd65_L243.txt`: i quattro numeri tornano. Accanto: le `d0` VERE sono `35.057`, `37.048` (l'antifase NON parte da `35`), `51.006`; **`d 66` su `L 243`: la corsa e' finita a `k 1814` (la finestra `250`-`1814`), e il DEVE di Gauss era CADUTO (`2.284e-10` contro `1e-10`), la soglia poi portata a `1e-9` DOPO il risultato, dichiarato** (`M/coppia_GUd65_L243.txt`). La regola di fase: `RELAZIONE_PER_CLAUDE.md` («IN FASE ATTRAE, IN OPPOSIZIONE RESPINGE»). «La coda lunga attrattiva (probabilmente U)»: la fonte come frase non trovata; il piu' vicino e' il confronto con `U_2000` in `M/coppia_GUd50_L162.txt`, e `doc/referti_l2/scatola5_u.txt` dice che i tre punti «NON stanno su una sola potenza».*

### C. Il triangolo a `120`: la forma e la rotazione *(`c211cf19` e le mappe)*

- **la forma a tre punte** *(m=3 della densita' nell'anello `12`-`32`)* **gira in verso antiorario: `+98` gradi in `12000` tick, piu' in fretta al minimo del lato; la pattinatrice da' `1.52`x contro i circa `4`-`5`x misurati (NON spiega).**
  *Fonte: `M/triangolo_t120_rotazione_B.txt` (`+98.49` a `12000`; omega massimo `+48.6` gradi per `1000` tick a `k 8500`, il lato minimo a `k 8650`). «il referto dice»: `1.52` NON e' cio' che la pattinatrice prevede: e' il rapporto MISURATO / PREVISTO al minimo del lato (`k 9000`: «misurato / previsto 1.52 -> la pattinatrice NON spiega»). Il «circa `1.5`x previsto contro `4`-`5`x» e' la stima del guardiano scritta PRIMA (`TH-M`); con L costante la previsione sarebbe `1.25`x (`TH-M`). E `TH-M` avverte: il picco di omega cade dove l'ampiezza a tre punte e' minima (`0.024`), dove l'angolo e' fragile («scritto, non provato»).*
- **DUE STRATI:** i lobi esterni *(`27`-`32`)* sempre avanti; l'interno *(`17`-`27`)* indietro fino a `-23` gradi a `k 5000` mentre perde la tre punte.
  *La fonte: non trovata (`M/girandola.txt` ha gli angoli per anello solo fino a `k 2000`, e su anelli diversi: `8`-`14`, `14`-`20`, `20`-`26`, `26`-`32`).*
- **la pulsazione delle forme** *(un ciclo visto)*: tre punte `0.37` *(largo)* -> `0.02`-`0.05` *(stretto, quasi un anello, a tratti sei gobbe)* -> `0.16`.
  *Fonte: `M/triangolo_t120_rotazione_B.txt` (`0.3669` a `k 0`; `0.0496`, `0.0239`, `0.0452` a `k 8000`, `8500`, `9000`; `0.1624` a `k 12000`): torna. «quasi un anello, a tratti sei gobbe»: la fonte non trovata (dalle mappe?).*
- **il campo B al centro NEGATIVO su tutta la corsa e CRESCENTE** *(`1.2`-`1.8` volte quello di `k 2000`)*, **non segue la velocita' della forma; L negativo.**
  *Fonte: `M/triangolo_t120_rotazione_B.txt` (B da `-6.0e-4` a `k 500`, tutti negativi; i rapporti `1.23`-`1.84`; il segno di L «-»); `TH-M` («B NON segue omega»). Torna.*
- **i segni (`eebb2f39`): coerenti; un vortice `+1` costruito a mano ha L e B negativi: e' la firma del `+1`.** **IPOTESI:** l'energia circola contro il verso della fase *(«onda all'indietro», o le onde di Kelvin su un vortice)*.
  *Fonte: `M/segni_vortice.txt` (L dell'energia `-9.413002e+04`; B dopo `3` tick `-1.9084e-07`; S1 coerente, `8`/`8`). Torna.*

### D. Il vuoto attorno al triangolo

- **le culle SEGUONO la materia** *(`0.1`-`2` nodi dal loro centro, `+-5` gradi senza accumularsi)*; **il GUSCIO grande** *(`30`-`45` nodi)* **NON gira e si spegne** *(tre punte `0.44` -> `0.21`)*. **L'ipotesi di Luca: la scatola piccola trattiene il guscio.**
  *La fonte dei numeri (`0.1`-`2` nodi, `+-5` gradi, `0.44` -> `0.21`): non trovata. I testi piu' vecchi dicono il contrario sulle culle («le culle restano ferme», `TH-M`; e la previsione P4 di `TH-M` le voleva «FERME»): la parte `2` lo elenca fra le cose corrette («le culle ferme: era il guscio»). Il «`1`-`2` gradi contro `+98`» del guscio sta in `doc/PIANO_VERIFICA_SCATOLA.md` (P-V6), senza un referto citato. Il guscio `30`-`45`: la definizione di P-V6.*

### E. Lo specchio *(`6faa1a3d`)*

- **F3 riflesso = -F3 al bit; il tick commuta con lo specchio con `T = sigma.l`, A col segno del verso, `phi -> -phi`** *(`3.5e-14` dopo `10` tick entro `40` nodi)*: **il modello e' simmetrico; il verso del vortice e' la condizione iniziale. Il vuoto F3 e' un FLUSSO uniforme con una fase per direzione** *(non un motivo ogni `3` nodi)*.
  *Fonte: `6faa1a3d` («F3 RIFLESSO = -F3 AL BIT ... T = sigma.l (UNITARIA), A COL SOLO SEGNO DEL VERSO, phi -> -phi: 3.5e-14 DOPO 10 TICK ENTRO 40 NODI»; accanto: la sola rottura e' il bordo, e un errore dichiarato dello script sulla soglia su tutto il toro). «Il verso e' la condizione iniziale»: `5f4fa81c` (la decisione di Luca delle `12:57`: lo specchio chiuso senza corsa). «F3 e' un flusso»: `13466107`. Torna.*

### F. L'alone del vuoto del mattone *(`ee7b8215`)*

- **i raggi al `10%` e al `5%` fermi a `24`-`25` nodi su `L 162`, `L 243`, `L 324`; dietro una coda all'`1`-`1.5%` con un fronte che avanza; l'energia del vuoto per nodo massima su un guscio fra gli anelli `13` e `14`** *(il primo indizio per la mitosi)*.
  *Fonte: `ee7b8215` e `M/porto_alone_vuoto.txt` (`24`/`25` su `L 162` e `L 324`; su `L 243` `25`/`26`); `TH-M` (la coda, il fronte, il massimo all'anello `13`-`14`). Torna (su `L 243` un anello in piu').*

### G. R-SCATOLA

- **al `2%` insegue la coda** *(R_ogg `44` -> `61` su `L 324`)*; **al `5%` la fase `0` sul mattone singolo su `L 186`** *(`abd5b9c3`)*: **raggio della materia `0.005%`, picco `0.13%` / `0.05%`, `5%` del vuoto `25`/`25`/`26`, massa e Gauss a posto; il periodo del respiro mal misurato** *(la finestra lunga quanto il respiro, lo spettro senza riga dominante)*; **ADOTTATA per il mattone singolo con la correzione post-hoc dichiarata** *(`069f5c1b`)*.
  *Fonte: `ee7b8215` («il 2%: 44, 45, 45, 61.0 (k 0, 950, 1000, 1755)»); `doc/referti_l2/prova_scatola5.txt` (la materia `0.005%`; il picco `0.132%` contro `L 243`, `0.049%` contro `L 324`; il `5%` del vuoto `25`/`25`, `25`/`25`, `26`/`26`; la massa `1.802e-14`; Gauss massimo `3.339e-11` sotto `3.150e-10`; il periodo `125.08` contro `187.62`, «7/8 ... NON ADOTTATA»); `scatola5_periodo_diagnosi.txt`; `069f5c1b` e `doc/ROTTA.md` (l'adozione). Torna.*

### H. Gli strumenti

- **Numba nel nucleo, i due passi AL BIT con la FMA esplicita** *(D1-D4)*, **ma `1.07`x a `2` fili e `0.99`-`1.04`x a `6`: spento per difetto** *(`b4b7f11f`)*. **I hook del commit tre volte piu' veloci** *(`06e5f3e8`)*. **La ripresa delle corse provata al bit** *(`notte.py`, R2 `8`/`8` su `L 297` e `L 339`)*.
  *Fonte: `b4b7f11f` («AL BIT, SPENTO PER DIFETTO»); `0a60d844` (D1 `20`/`20`, D3, D4 al bit); `011377eb` (D2b `14`/`14` con la FMA esplicita); `abf59c6f` (`1.07`x a `2` fili, `0.99`-`1.04`x a `6`); `ae93f7d9` (i hook: `326.4`, `338.6`, `318.7` s prima, `114` s dopo: circa `3`x); `doc/referti_l2/prova_ripresa.txt`, `61e8ca37` (`L 297` `8`/`8`), `704c5baf` (`L 339` `8`/`8`). Torna.*

## PARTE 2 -- COSA E' STATO CORRETTO *(l'elenco, con il commit)*

| | la cosa corretta | il commit | la nota |
|---|---|---|---|
| `1` | il ritorno apparente dei «centri» del triangolo *(difetto della misura)* | `b20633d1` | `TH-M`: «NON i tre "centri" della serie, che saltano vicino all'esagono: il difetto scritto dal guardiano». *La parola «ritorno» non c'e'; il piu' vicino e' «la forma torna indietro fra 3500 e 5000» (`c211cf19`).* |
| `2` | il verso degli angoli delle girandole | `259ae269` | «i numeri del guardiano specchiati ... uno specchio di convenzione»; accanto `eebb2f39` *(i segni coerenti)* |
| `3` | «le culle ferme» *(era il guscio)* | ### **la fonte: non trovata come correzione** | *Il piu' vicino: `ee7b8215` / `TH-M` («il vuoto e' teso su un GUSCIO ... (la "culla"?)»). E `doc/CONSIDERAZIONI/2026-11-15_triangoli.md` dice ANCORA «le culle nel vuoto restano»: **la correzione non e' scritta da nessuna parte.*** |
| `4` | il reticolo come causa *(caduto)* | `aedf6e51` | «il reticolo non tira il vuoto»; la previsione in `7f01286a` |
| `5` | F3 come motivo ogni `3` nodi *(e' un flusso)* | `13466107` | il controllo di prima dichiarato sbagliato in `6b07fca5` |
| `6` | il raggio inscritto `L/2` contro `0.433 L` | `8debe00f` | l'errore del guardiano n.`179`; i tori ricontati in `413480a0` |
| `7` | la clausola della fascia dimenticata | `a157210b` *(segnalata)*, `8debe00f` *(«le clausole sono tre»)*, `9aa7e7f9` *(nel codice)* | |
| `8` | il periodo del respiro come soglia | `abd5b9c3` *(la diagnosi, errore mio)*, `069f5c1b` *(la decisione, n.`182`)* | lo script `c0a14ed7` |
| `9` | l'`1.33`x di Numba *(era il carico)* | `abf59c6f`, `b311cbaf` | «il 1.33x della notte era a macchina carica» |
| `10` | le stime dei tempi delle corse | `61e8ca37` | «`13`-`16` s per tick (non `7.5`)» |

## PARTE 3 -- LE DOMANDE APERTE *(ognuna con: perche' conta, il test, la previsione se c'e', il costo stimato)*

- **Q1. La fisica di `L 162` regge nella scatola giusta?** Test: la verifica sospesa *(le corse da riprendere, parte `5`)*. **Previsioni gia' committate: P-F1..P-F3, P-V3..P-V6** *(`106158f8`: il commit tocca `doc/PIANO_VERIFICA_SCATOLA.md` con le sette previsioni; controllato)*.
- **Q2. Gli oggetti composti: R_ogg al `5%` CRESCE** *(F-66 `57` -> `86`, A-66 `57` -> `77`, F-51 `50` -> `68`, V-B2pi `42` -> `59`, V-T120 `47` -> `59`; il mattone singolo fermo a `25`)*. **Ipotesi del guardiano:** la somma delle code deboli dei mattoni. **Test** *(sola lettura)*: il profilo dell'alone delle coppie contro due volte quello del mattone singolo. **Da decidere da Luca:** R_ogg dei composti = l'estensione della materia + `25`.
  *Fonte: `doc/referti_l2/notte_tabella.txt`; `prova_scatola5.txt` (`25.0` all'inizio e alla fine). Torna. Accanto: per V-B2pi il `59` e' da `k 1750` (prima `42`-`43`); V-B2, non nella lista, va da `42` a un massimo di `59` (`k 1750`) e finisce a `43`.*
- **Q3. R_ogg a gradini; V-B2 e V-B2pi con la STESSA serie di R_ogg** *(vero o un difetto della misura)*: test sulle mappe dei pezzi.
- **Q4. Il DEVE della massa delle corse della notte, sui conti uniti:** non calcolato.
- **Q5. La coppia in antifase:** i minimi e i massimi che salgono; l'equilibrio intorno a `40` e' della scatola? *(P-V4.)* *(Accanto, da `TH-M`: «da due cicli non si dice se e' una deriva».)*
- **Q6. Il triangolo: la pulsazione delle forme si ripete o si smorza?** Il jitterbug di Fuller *(l'angolo oscilla)* o la trottola che respira *(l'angolo cresce sempre)*? Test: un secondo ciclo, fino a circa `k 25000`.
- **Q7. L'accelerazione della rotazione al minimo** *(`4`-`5`x contro `1.52`x della pattinatrice)*: da dove viene? Test: L e I della materia nel tempo, `omega = L / I`.
  *«il referto dice»: `1.52` e' il rapporto MISURATO / PREVISTO dalla pattinatrice al minimo del lato, non l'accelerazione prevista (vedi la parte `1C`); il «`1.5`x contro `4`-`5`x» e' la stima del guardiano scritta prima (`TH-M`).*
- **Q8. L'«onda all'indietro»:** in quale ramo della dispersione stanno i mattoni *(la velocita' di gruppo e di fase)*.
- **Q9. Il guscio del vuoto ruota in una scatola grande?** *(P-V6, l'ipotesi di Luca.)*
- **Q10. La quantizzazione del flusso:** il flusso di B di un vortice `+2` e' il doppio del `+1`?
- **Q11. Vortice `+1` e `-1` vicini: si attraggono, si legano, si annichilano?** *(«Il mandato della carta, Luca 13:04 del 2026-11-16, non mandato».)*
  *La fonte: non trovata: nessun testo delle `13:04` del `2026-11-16` sui vortici `+1`/`-1` nel repo (commit di tutti i rami, relazione, ROTTA, task history, considerazioni) ne' nelle trascrizioni delle mie sessioni. Coerente con «non mandato»: il testo lo ha il guardiano.*
- **Q12. Il mattone singolo in moto:** con una spinta *(un gradiente di fase)* va dritto a velocita' costante? la massa inerziale? la stessa in tutte le direzioni del reticolo?
- **Q13. La mappa della forza `V(d, la differenza di fase)`:** le fasi intermedie *(`60`, `90`, `120` gradi)* e piu' distanze.
- **Q14. Le fasi dei mattoni nel tempo:** derivano o si agganciano?
- **Q15. Il terzo corpo:** il triangolo e' la somma di tre coppie?
- **Q16. I puntini:** la tabella delle leggi dei mattoni, poi la prova del «clic» *(il modello a puntini contro la coppia vera)*.
- **Q17. La velocita':** Numba anche su `termini_di_h` ed `elicita` *(circa il `40%` del tick)*; il motore fuso *(circa `10`x, non al bit)*; i `3` giri del punto fisso *(non al bit)*.
  *Fonte: il `40%`: `doc/ROTTA.md`, `doc/TASK_HISTORY/2026-11-15_motore_numba.md`; i `3` giri: `1d913fd1`. «il motore fuso circa `10`x»: la fonte non trovata; il piu' vicino: «le tre funzioni del secondo passo `4`-`12`x piu' veloci ciascuna» (`2026-11-15_motore_numba.md`).*
- **Q18. Parcheggiate:** il bordo come orizzonte *(`cs -> 0`, idea di Luca)*; le strade S3-S5 dei hook; il trasloco del repo su E:.

*(Il costo stimato di ogni test: il testo del guardiano non lo dà; non lo invento. I costi misurati per tick sono nella parte `5`.)*

## PARTE 4 -- LA MITOSI DELLO SPAZIOTEMPO *(il contesto per il prossimo lavoro)*

- **Il piano:** **D9** *(lo spazio emerge dalla mitosi)*, **D7** *(la nascita: padre e figlio `psi/sqrt(2)`, la stessa fase)*, **la decisione `10`** *(il calore paga la nascita, la soglia e' il bilancio)*; **`crescita.py` e' solo l'intestazione; D7 e' bloccata da `DEC-FC-COESIONE`** *(non presa)*.
  *Fonte: `doc/ALBERO_era2.yaml`: `DEC-D9-GEOMETRIA` (`presa: false`; e `doc/PIANO_era2.md`); `DEC-D7-DIVISIONE` («psi -> psi/sqrt(2) per il padre E per il figlio, CON LA STESSA FASE»; `dipende_da` `DEC-D6F-FORME-VUOTO`, `DEC-FC-COESIONE`; `presa: false`); la decisione `10` «PRESA in 3e8375b (il calore paga la nascita, e LA SOGLIA E' IL BILANCIO)»; `DEC-FC-COESIONE` `presa: false` (`dipende_da` `DEC-QC-CONSERVATA`), e `P-ALB` rifiuta D7 come presa; `primo_ordine/crescita.py`: `11` righe, «TAPPA 1: SOLO L-INTESTAZIONE». Torna.*
- **Cosa gli strumenti presuppongono e andra' ripensato con un grafo che cresce:** il vuoto F3 sul reticolo, Gauss sulla griglia fissa, il bordo a cerchio, R-SCATOLA, le mappe, numba.
- **Gli indizi gia' raccolti:** l'alone del mattone *(F)*, il guscio dell'energia del vuoto agli anelli `13`-`14`; le forze e gli oggetti legati *(A, B)* come dati per la coesione.

## PARTE 5 -- LE CORSE SOSPESE E COME RIPRENDERLE

*(La fonte: `doc/referti_l2/notte_tabella.txt`, lo script `notte_tabella.py` a `9650ea2c`; gli sha1 ricalcolati dal disco e concordi col `.sha1` accanto. Controllato: ogni numero torna.)*

| corsa | toro, R_A | l'ultimo `k` | di | l'ultimo stato | sha1 | s per tick | lo stato |
|---|---|---|---|---|---|---|---|
| V-B2 | `L 297`, `85.06` | `2223` | `12000` | `stato_02223.npz` | `af975abf` | `16.717` | SOSPESA |
| V-B2pi | `L 321`, `92.42` | `1870` | `10000` | `stato_01870.npz` | `14950bf6` | `19.854` | SOSPESA |
| V-T120 | `L 339`, `97.16` | `332` | `12000` | `stato_00332.npz` | `65415993` | `23.849` | FERMATA *(Luca `00:20`, R-SCATOLA)* |
| F-66 | `L 402`, `116` | `1019` | `2000` | `stato_01019.npz` | `6ca3d8e2` | `34.593` | SOSPESA |
| A-66 | `L 402`, `116` | `835` | `2000` | `stato_00835.npz` | `d7830888` | `34.398` | SOSPESA |
| F-51 | `L 351`, `101` | `1076` | `2000` | `stato_01076.npz` | `f4caab19` | `24.942` | SOSPESA |
| A-51, A-45, F-35, A-35 | | -- | `2000` | -- | -- | -- | NON PARTITE |

- **Gli stati stanno in `E:\soliton_simulator\notte\<nome>\`** *(`stato_<k>.npz` col `.sha1` accanto; i pezzi `pezzo_<da>_<a>.npz` con le serie, le mappe e i conti; `scena.json`)*. ### **NON SI CANCELLANO.**
- **Il DEVE della massa** *(la massa persa = la massa uscita dal bordo entro `1e-6`, sui conti uniti)* **NON e' ancora calcolato** per nessuna *(Q4)*.
- ### **LA CONDIZIONE PER RIPRENDERLE: il nucleo IDENTICO a quello di oggi.**
  - **`doc/NUCLEO_CONGELATO.md` di oggi:** sha1 dei byte grezzi **`a83b9e64a157ecc5832b6a02a34d5dbc985abcc9`** *(l'ultimo commit che lo tocca: `b4b7f11f`, `2026-11-16` `16:50`; lo stato: `CONGELATO`)*.
  - **Accanto** *(perche' quel file dice lo STATO del congelamento, non i byte del nucleo)*: **gli sha1 dei byte dei `12` file del nucleo che le voci della notte hanno timbrato** *(il registro, `notte-F-51`, il campo `nucleo.sha1_byte`)*: `primo_ordine/_collauda_motore.py` `4d60d2f2` · `_collauda_r60.py` `1ee3f0eb` · `_mappa.yaml` `26f2abaf` · `_misura_hw.py` `98c1d34b` · `_misura_mb2.py` `48269077` · `energia_pesata.py` `43bce8ad` · `flussi_parziali.py` `d43b1cf8` · `leggi/leggi.yaml` `1c0eac29` · `termini/camm_grover.py` `10b70489` · `termini/camm_grover_vuoto.py` `8f88bc20` · `termini/camm_spostamento.py` `d58a753f` · `termini/camm_spostamento_vuoto.py` `a58a55ea`. *(La stessa voce dice `diversi: [primo_ordine/_mappa.yaml]`, `uguali_alla_tabella: false`: era cosi' a ogni lancio della notte, e cosi' resta la condizione: **gli stessi byte**.)*
  - **E lo strumento:** `csv/solitone/notte.py` *(`ff846b8c`, sha1-byte `7cfa457f`)*, provato al bit *(`doc/referti_l2/prova_ripresa.txt`)*.
  - ### **Se il nucleo cambia** *(per esempio la mitosi)*: **le corse si RIFANNO da capo, e gli stati restano come archivio.**
- **IL COMANDO DI RIPRESA** *(con l'interprete di E:, `1` filo, numba spento)*:
  `E:/python/py3132/python.exe csv/solitone/notte.py corsa --nome <nome> --da ultimo --fino <fino> --registro <voce nuova> [--ferma-alle <ISO>]`
  **`--da ultimo`** prende l'ultimo stato, **ricalcola lo sha1 e lo confronta col `.sha1`**; se non coincide lo scrive e prende lo stato prima. **Prima: una voce NUOVA nel registro** *(la vecchia e' chiusa SOSPESA, col comando scritto dentro)*.

## PARTE 6 -- L'ORDINE PROPOSTO PER LA RIPRESA *(del guardiano; LO DECIDE LUCA)*

1. **Le letture senza corse:** Q2, Q3, Q4.
2. **La decisione su R_ogg dei composti;** poi la verifica *(Q1, Q5, Q9)*.
3. **La tabella delle leggi dei mattoni;** poi Q12-Q15; poi i puntini *(Q16)*.
4. **La mitosi:** prima la carta *(la coesione, D7, la decisione 10, dove nascono i nodi, cosa si rompe)*; **il codice solo dopo la verifica.**

## PARTE 7 -- IL RESTO DEL REPO IN SOSPESO *(il censimento, dal repo, non a memoria)*

*(I conti di 7.3, 7.5 e 7.6 escono da `doc/referti_l2/sospeso_censimento.txt`: lo script `sospeso_censimento.py` a `52d1ea9e`, in sola lettura, dopo un `git fetch`. La 7.1 e la 7.2 sono lette da `doc/ROTTA.md` e da `doc/CENSIMENTO_DECISIONI.md` come stanno OGGI.)*

### 7.1 LA ROTTA: le voci della coda *(`doc/ROTTA.md`, «La coda»; le voci `1`-`6` sono i passi della rotta del tempo locale, sopra la coda)*

| voce | il titolo | lo stato **(come lo scrive la ROTTA)** | cosa manca | la carta *(come la cita la ROTTA)* |
|---|---|---|---|---|
| `7` | I BRACCI DI P6 | **CHIUSA** *(`8ca61a34`, `15`/`15`)* | la DOMANDA APERTA sul rapporto misurato / atteso di U. *«il referto dice»: la ROTTA ha sostituito `0.0178` con **`0.0128`** («col numero nuovo al posto di 0.0178»)* | `doc/referti_l2/p6_bracci.txt` |
| `7-bis` | IL LAPSE MENO COSTOSO, LA PARTENZA A CALDO DEL PUNTO FISSO | «DOPO il referto dei bracci di P6; poi FERMO per Luca» | **aspetta un mandato** *(i bracci sono chiusi)* | non citata |
| `8` | IL VIDEO TRIPLO | *«il referto dice»: **CHIUSA**, non «mai girato»* *(`102814bd`, `8`/`8`: la cresta e' l'equilibrio)* | -- | il codice `bea419ba`; `doc/referti_l2/campo_g1_tre/referto.txt` |
| `9` | LA PROVA DELLE BANDE PIATTE SUL BUCO DEL VUOTO | **PRONTA, aspetta un mandato** | il mandato; la proposta delle bande del VUOTO *(`6` componenti)* aspetta Luca | il mandato delle `17:00` del `2026-11-12` |
| `10` | P1 | **FERMO prima del codice: aspetta la decisione di Luca** | la decisione sulle correzioni del guardiano | `3de28902` |
| `11` | P9, il solitone in fondo a una banda | **solo SU CARTA, poi FERMO** | la carta | non citata |
| `12` | LA U(1) TOPOLOGICA | **PRONTA, solo SU CARTA, aspetta un mandato** | il mandato | le quattro domande della sezione delle tre forze |
| `13` | IL RIMANDO *(P10; i resti di S5; la rotazione di `360` gradi; il lapse esplicito)* | «GIA' REGISTRATI: NON si avviano senza un mandato» | un mandato per ognuno | non citata |
| `14` | LA PERDITA DI MASSA DEL SOLITONE E LA SUA DIMENSIONE *(e la taglia doppia)* | «IN CODA, dopo la voce `7-bis`; solo registrata, nessuna corsa» | la `7-bis` prima; un mandato | non citata |
| `15` | IL BILANCIO DELLE ENERGIE, LA PRIMA APPLICAZIONE A `Grampa` | **CHIUSA** *(`003dd8de`; la chiusura `doc/referti_l2/bilancio_chiusura.txt`)* | -- *(la domanda forza/colpetto passata alla coppia G+U)* | `doc/TASK_HISTORY/2026-11-14_bilancio_energie.md` |
| `16` | I DATI NEL REPO: GLI STATI DI PARTENZA E I MATTONI | «e' la PROSSIMA, e aspetta il mandato di Luca» | il mandato *(non eseguita con la riunione delle navi)* | non citata |
| `17` | LE CONSIDERAZIONI DELLA NOTTE *(e la girandola)* | «SOLO SU CARTA»; parte quando la voce `16` e' fatta *(NON ancora)* e B2 ha detto forza o colpetto *(la lettura non e' scritta)* | la voce `16`; la lettura forza/colpetto | `doc/CONSIDERAZIONI/2026-11-15_triangoli.md`; `259ae269` |
| `18` | LE COPIE DEL PUNTO FISSO: QUALE CAMPO VEDONO | **solo SU CARTA, decide Luca** | la decisione | il ramo mattone, sez. `16`; il peso `703b1e63` |
| `19` | IL DOCUMENTO DI STATO | «DOPO la riunione delle due navi; il mandato lo da' Luca» | il mandato *(la riunione e' fatta, `1fcd8682`)* | non citata |
| `20` | LA CONVERGENZA (LA SCATOLA) | *«il referto dice»: la ROTTA scrive ancora «IN CORSO sul ramo»*, **ma il ramo e' chiuso** *(`nave-mattone-chiusa-2026-11-16`)*: **la riga e' SCADUTA** | **cosa ne resta dopo R-SCATOLA al `5%`:** il nucleo fermo a `24`-`25` nodi su tre tori *(F)* risponde per il mattone singolo; **per i composti la domanda e' Q2** | il ramo mattone, sez. `19` |
| `21` | IL PENDOLO PULITO | **NON ora: il mandato lo da' Luca** | il mandato | `22317f86` *(il dato su `L 81`)* |

### 7.2 LE DECISIONI DI LUCA NON NEL CODICE *(`doc/CENSIMENTO_DECISIONI.md`, `95d39bf0`, del `2026-10-25`: NON riverificato oggi)*

- **`48` decisioni contate; `25` nel nucleo, `15` giustamente fuori, `8` MANCANZE: `2` LIBERE, `6` BLOCCATE da una decisione aperta.**
- **Le `2` libere** *(l'«ordine proposto» del censimento)*: **[[DECISIONE-SOLO-TRIANGOLI]]** *(la scena a triangoli nel nucleo)*; **il criterio di [[DECISIONE-L1-NATURA-A-SIMULATORE-B]]** *(«e' fisico solo cio' che CONVERGE raffinando», in `doc/PATTERN_DI_PROVA.md`)*.
- **Le `6` bloccate, con cosa le sblocca:**

| la decisione | che cosa manca | la sblocca |
|---|---|---|
| [[DECISIONE-LINEARE]] | il nucleo ha la forma che la decisione esclude *(`CAMM-MATERIA-VUOTO` e' `S3`)* | `S1` contro `S4` *(`doc/DOSSIER_S1_S4.md`)* |
| [[DOMANDA-VIA-DEL-CAMPO]] | la `U` d'arco dinamica *(solo negli strumenti, `csv/_u1_prototipo.py`)* | `DOMANDA-U-DINAMICA-LE-FORME`; le scelte di [[PROGETTO-U1]] |
| [[DECISIONE-DIREZIONE-STRADA-3]] | la `C` misurata ma non dichiarata in tabella; nessun termine d'ordinamento | `DOMANDA-L-ORDINAMENTO-IN-H-O-NON-H`, `DOMANDA-DOVE-STA-LA-C-IN-TABELLA` |
| [[DOMANDA-BANDE-O-SEGNO-LOCALE]] | il segno locale `q_h`, da nessuna parte | il termine d'ordinamento |
| il freno della coesione e' la `(c)` *(`2026-10-08`)* | da nessuna parte | ### **`DEC-FC-COESIONE`** *(`presa: false`)* |
| [[D-BILANCIO-NASCITA]] | chi paga la nascita: `crescita.py` e' l'intestazione, `motore.cresci` permuta lo stato | `DEC-NASCITA-PSI`, `DOMANDA-MITOSI-LE-FORME`, il nodo `D7` |

- ### **IN EVIDENZA: `DEC-FC-COESIONE`** *(`doc/ALBERO_era2.yaml`, `presa: false`, `dipende_da` `DEC-QC-CONSERVATA`)*: **blocca il freno della coesione E il nodo D7** *(la divisione; `P-ALB` rifiuta D7 come presa)*, **quindi la mitosi** *(parte `4`)*. *(Il censimento: «Luca CONFERMA la regola di D7, ma il campo resta false perche' D7 dipende da DEC-FC-COESIONE, non presa».)*

### 7.3 L'INDICE *(`doc/indice/voci.jsonl`; NESSUNA VOCE CAMBIATA)*

| classe | AGENDA | APERTA | CHIUSA | DA_CLASSIFICARE | SOSPESA | SUPERATA | in tutto |
|---|---|---|---|---|---|---|---|
| CRITERIO | `4` | `3` | `17` | `0` | `78` | `0` | `102` |
| CURA | `5` | `0` | `45` | `0` | `3` | `7` | `60` |
| **DECISIONE** | **`71`** | **`4`** | `18` | `0` | `0` | `6` | `99` |
| **DIFETTO** | **`11`** | **`20`** | `51` | `0` | `132` | `2` | `216` |
| **FRONTE** | **`35`** | **`11`** | `5` | `0` | `77` | `3` | `131` |
| **MISURA** | **`27`** | **`2`** | `125` | `0` | `24` | `1` | `179` |
| NON_DEFINITA | `0` | `0` | `0` | `187` | `0` | `0` | `187` |
| PRESIDIO | `26` | `39` | `1` | `0` | `7` | `0` | `73` |
| STANDARD | `12` | `42` | `3` | `0` | `0` | `3` | `60` |
| TEORIA | `14` | `0` | `0` | `0` | `0` | `0` | `14` |
| **in tutto** | `205` | `121` | `265` | `187` | `321` | `22` | **`1121`** |

- **L'elenco delle `APERTA` e `AGENDA` di DECISIONE, FRONTE, MISURA, DIFETTO** *(`181` voci, l'id e il titolo)*: **l'APPENDICE A** in fondo, copiata dal referto.
- **I `187` `DA_CLASSIFICARE` sono tutti `NON_DEFINITA`** *(gli ID citati e non definiti, `indice.py citazioni`)*.

### 7.4 I LAVORI DELLE ULTIME SESSIONI FUORI DALLA VERIFICA

- ### ⚠ **LE CONSIDERAZIONI DEL MATTINO DEL `2026-11-16`** *(il mandato di Luca delle `11:47`, MAI scritte)*: **NON LE HO SCRITTE: IL TESTO DI QUEL MANDATO NON LO TROVO.** **Cercato:** nel repo *(commit, relazione, task history, `doc/CONSIDERAZIONI/`: nessun «11:47» del `2026-11-16`)* e **nelle trascrizioni di tutte le mie sessioni** *(i messaggi di Luca del `2026-11-16` cominciano alle `12:57`, la decisione dello specchio)*. **Scriverle «col testo di quel mandato» senza il testo vorrebbe dire inventarlo.** ### **Serve che Luca o il guardiano incollino il testo delle `11:47`:** allora `doc/CONSIDERAZIONI/2026-11-16_triangolo_forme.md` si scrive in un commit a se'.
- **La cottura del mattone su `L 324`** *(porto-cottura)*: **al tetto a `k 1755`** *(`3f6b1cc2` sul ramo mattone; `16.4` s per tick; Gauss `1.855e-10`)*; **R_ogg al `2%` da `44` a `61`, R-SCATOLA NON rispettata**; **gli stati salvati sono `k 950` e `1000`, `k 1755` NON e' salvato** *(la relazione)*. **Le cinque corse dei porti grandi: MAI partite** *(Luca `2026-11-15` `18:08`: «NON partono prima di D5»; poi la notte le ha sostituite col piano di verifica)*.
- **La carta vortice `+1` / `-1`** *(Q11)*: **non scritta** *(il mandato non mandato: parte `3`)*.
- **La quantizzazione del flusso** *(Q10)*, **il secondo ciclo del triangolo** *(Q6)*: **nessuna carta.**
- **Numba su `termini_di_h` ed `elicita` e il motore fuso** *(Q17)*: le strade di `doc/TASK_HISTORY/2026-11-15_motore_numba.md` *(«nessuna presa»)*; numba spento per difetto *(`b4b7f11f`)*.
- **I hook S3-S5; il peso di `doc/indice/storico.jsonl`; il trasloco su E:; il bordo come orizzonte** *(Q18)*: parcheggiati, nessuna carta.

### 7.5 I RAMI SU ORIGIN *(nessun ramo cancellato)*

| il ramo | l'ultimo commit | la data | dentro `primo-ordine` | il tag sull'ultimo commit | lo stato |
|---|---|---|---|---|---|
| `main` | `252630fe` | `2026-09-10` | **NO** | -- | **fermo, da decidere** *(il worktree `C:/Users/lpeano/st_main` e' su di lui)* |
| `dati-grezzi` | `c7a90cd7` | `2026-09-21` | **NO** | -- | **fermo, da decidere** |
| `dev-dof` | `125666a2` | `2026-09-09` | **NO** | -- | **fermo, da decidere** |
| `dev-infra` | `36a310c9` | `2026-09-07` | SI' | -- | riunito *(contenuto)* |
| `dev-spinoriale` | `c9fcc1e8` | `2026-09-13` | SI' | -- | riunito *(contenuto)* |
| `fork-su2` | `803bfed7` | `2026-10-08` | SI' | `era-1-secondo-ordine` | **chiuso** *(l'era `1`)* |
| `last` | `2235a3cf` | `2026-09-02` | **NO** | -- | **fermo, da decidere** |
| `media` | `182e30f1` | `2026-09-27` | **NO** | -- | **fermo, da decidere** |
| `unificazione` | `0fa7792d` | `2026-11-12` | SI' | -- | riunito *(il passo `3` della ROTTA)* |
| `zero-nel-nucleo` | `986440d6` | `2026-11-12` | SI' | `laterale-archiviato`, `pre-unificazione-laterale` | **chiuso** *(archiviato)* |
| `strumento-mattone` | `5f4fa81c` | `2026-11-16` | SI' | `nave-mattone-chiusa-2026-11-16` | **chiuso** *(riunito, `1fcd8682`)* |
| `motore-numba` | `abf59c6f` | `2026-11-16` | SI' | `motore-numba-riunito-2026-11-16` | **chiuso** *(riunito)* |

*(«Lo stato» e' la MIA lettura dai tre dati -- antenato, tag, data --: i cinque rami NON contenuti sono di settembre, e se chiuderli e' una decisione di Luca. Il numero dei loro commit fuori da `primo-ordine` e l'ultimo messaggio sono nel referto.)*

### 7.6 LE CORSE E I LUCCHETTI

- **Nessuna corsa aperta nel registro di `primo-ordine`** *(`0` voci APERTE)*; **nessun file di tappe aperto** su `E:\soliton_simulator\registro_tappe`.
- **Il registro del worktree del mattone** *(`C:/Users/lpeano/soliton_simulator_mattone`, fermo a `5f4fa81c`)* **ha `1` voce che risulta APERTA: `p6-0_2000`** *(dal `2026-11-13` `19:18`)*. ### **E' una copia vecchia:** **nel registro di `primo-ordine` la stessa voce e' `CHIUSO` `FINITO`** *(`2026-11-13` `19:46`, «2000 tick (62000) in 938 s»)*. Nessuna corsa gira.
- **I lucchetti: nessuno** *(`index.lock` in nessuno dei cinque worktree; `commit.lock` di `committa2` assente)*.

## APPENDICE A -- LE VOCI `APERTA` E `AGENDA` DI DECISIONE, FRONTE, MISURA, DIFETTO *(copiate da `doc/referti_l2/sospeso_censimento.txt`)*

```
### DECISIONE, APERTA: 4
    BUDGET-COLLAUDI-500                              il budget dei collaudi e- 500 s, soglia di LAVORO decisa da Luca, e niente parallelismo
    D-BILANCIO-NASCITA                               la nascita si paga: i genitori con la tensione, il vuoto col suo termine
    DOMANDA-BASE-DI-CICLI                            la base di cicli non e unica, e lo stesso difetto compare in tre pezzi diversi
    DOMANDA-LA-CARTA-NON-ESISTE                      la carta della fisica non ha un documento, e le sue etichette collidono con ID veri
### DECISIONE, AGENDA: 71
    BASTA-PROTOTIPI                                  basta prototipi: il simulatore riusa l-architettura provata dell-era 1, adattata
    COESIONE-TERMINE-O-CAMPO                         la coesione simmetrica viene da un termine LOCALE o da un CAMPO?
    CS-LOCALE-DAL-VUOTO                              il tempo proprio e la velocita- locale della luce vengono dal VUOTO, non dalla materia del nodo
    DEC-ALBERO-CINQUE-SENZA-ARGOMENTO                di CINQUE nodi dell-albero il repo non dice l-argomento, e delle decisioni 1, 3, 10 nemmeno
    DEC-NASCITA-PSI                                  con che stato nasce un nodo? il punto 3 chiede UNA REGOLA DICHIARATA per ogni grandezza
    DEC-REGOLA-FORMA                                 che CODICE genera una `regola`? il punto 11(a) chiede che crescita e vuoto si generino
    DECISIONE-DIREZIONE-STRADA-3                     strada (3): C esatta nelle leggi e ROTTA SPONTANEAMENTE nello stato, con pareti
    DECISIONE-L1-NATURA-A-SIMULATORE-B               LA NATURA E- (A), IL SIMULATORE E- (B): fisso in archi = artefatto; serve un dizionario
    DECISIONE-LA-C-VUOLE-IL-TEMPO-ROVESCIATO         La C del cammino era una conseguenza delle involuzioni: coi flussi parziali serve una CT
    DECISIONE-LINEARE                                LINEARE, il regime di poca materia di S3: l-accoppiamento rho dalpha/drho deve andare a zero
    DECISIONE-SOLO-TRIANGOLI                         SOLO TRIANGOLI: la fisica si misura sui triangoli; il quadrato solo come controllo di servizio
    DECISIONE-TICK-OROLOGIO-MASSIMO                  il tick e l orologio piu veloce possibile: theta <= pi e cs ha un massimo
    DERIVA-DELLA-FORMA-D                             la forma (D) non conserva la sua conservazione modificata: perche-?
    DOMANDA-A-NON-E-MECCANICA                        (A) non e meccanica: dE/d theta_k = 0, quindi Hamilton da d pi_k / dt = 0
    DOMANDA-A3B-CLASSE                               A3b: con che classe entra nell-indice?
    DOMANDA-BANDA-ANTIMATERIA                        la banda di sotto come antimateria: un vuoto con la banda negativa occupata, la norma come N+ - N-?
    DOMANDA-C2-O-C4                                  due componenti o quattro: il gap c-e- solo con C4?
    DOMANDA-CHI-CAUSA-L-ANISOTROPIA                  sul cubico i versori del v3 RIDUCONO l-anisotropia direzionale: e- una leva o si lascia?
    DOMANDA-CHIRALITA                                la chiralita: quale grandezza del modello e? la moneta di spin, le due componenti a K, le valli
    DOMANDA-CONDIZIONI-INIZIALI-IN-TABELLA           la tabella non ha un posto dove dichiarare le condizioni iniziali
    DOMANDA-CONO-EMERGENTE                           il cono di luce unico puo' emergere dalla dinamica della materia vestita dal vuoto?
    DOMANDA-D13-CONIUGATI                            D13: i coniugati delle memorie -- tw come fase U(1) sull-arco?
    DOMANDA-D9-GEOMETRIA                             D9: la geometria viene da d e p_d dentro H, o dalle relazioni fra gli psi?
    DOMANDA-DOVE-STA-LA-C-IN-TABELLA                 la C e decisa al punto F3 e nessuna legge della tabella la dichiara
    DOMANDA-DOVE-VIVE-LAMBDA-C-SENZA-UN-VALORE       la scheda di Lambda_c non si genera dalla tabella: lo schema pretende valore E origine
    DOMANDA-ESTREMITA-NUOVE-INIZIALI                 con che psi e che phi nascono le estremita di un arco nuovo
    DOMANDA-FLUSSO-SENZA-AZIONE                      un flusso non dichiara dove agisce: lo schema non ha il campo azione per lui
    DOMANDA-FORME-VUOTO                              le TRE forme del vuoto locale: che cos-e- un grado, quanti per nodo, l-accoppiamento
    DOMANDA-FUSIONE                                  la FUSIONE di due nodi: si vieta, e con che cosa?
    DOMANDA-GOBBA-SEGNO-GRAVITA                      la gobba del vuoto e il segno della gravita: la massa sul fondo fa un pozzo o una collina di cs?
    DOMANDA-GRAFO-INIZIALE                           il grafo iniziale SENZA pos: reticolo, k-regolare, espansore?
    DOMANDA-GRANDEZZA-LOCALE-TEMPO                   da dove viene la grandezza locale da cui escono r_k e cs_k?
    DOMANDA-GUSCIO-E-INTERFERENZA                    il guscio e- interferenza e non materia: che cosa resta dell-ipotesi del guscio?
    DOMANDA-IL-PI-DEL-NODO-CHE-NASCE                 il pi di un nodo nuovo: la decisione 10 (il calore paga la nascita) riscritta su pi
    DOMANDA-IL-V4-ENTRA-NELL-ERA-2                   cinque gruppi di operatori del v4 sono nel banco e non in tabella
    DOMANDA-IL-VALORE-DI-LAMBDA-C                    il valore di Lambda_c: parametro dichiarato, memoria di nascita, o altro
    DOMANDA-L-ORDINAMENTO-IN-H-O-NON-H               il termine di ordinamento entra in H (e nel flusso) o come legge NON-H?
    DOMANDA-LA-FORMA-DI-CS-CHE-SATURA                la forma di cs dal vuoto che satura: la scala Lambda_0 non esiste in tabella
    DOMANDA-LA-FORMA-DI-F-NELL-ORDINAMENTO           quale F in Lambda F(q q / Lambda^2): esiste, NON e unica, ed e la stessa classe di G
    DOMANDA-LA-GERARCHIA-GRAVITA-EM                  la gerarchia gravita/elettromagnetismo deve EMERGERE dal modello, o si accetta come parametro
    DOMANDA-LA-MITOSI-CREA-VUOTO                     la mitosi CREA vuoto? a densita costante V cresce, e oggi V si conserva esattamente
    DOMANDA-LAMBDA-GRANDEZZA                         lambda: su quale grandezza si misura, e da dove viene il suo valore?
    DOMANDA-LO-STATO-CONTIENE-IL-PASSATO             lo stato contiene il passato? una memoria al posto dei punti fissi di cs, scelta per il modello
    DOMANDA-MASSA-E-FORME-MANCANTI                   il termine di massa e due forme del flusso sono nel banco e non in tabella
    DOMANDA-MITOSI-LE-FORME                          le quattro forme della mitosi: lo spareggio, phi, il ramo della radice, la connessione
    DOMANDA-PASSO-FRAZIONARIO-O-ASINCRONO            pezzi frazionari o tick asincroni, e l-invarianza locale dei secondi NON e- dimostrata dove cs varia
    DOMANDA-PESO-ARCO-COME-MEMORIA                   il peso d-arco come memoria dinamica: la geometria nasce dalla dinamica?
    DOMANDA-PORTATA-DEL-VUOTO-MEDIATORE              quale instradamento, cioe quale cono: la liberta di ricircolo adesso sceglie la portata
    DOMANDA-PRIMA-LEGARE-POI-MISURARE                senza stato legato tre letture non sono decidibili: si cerca prima un legame?
    DOMANDA-Q-DEL-NODO-SOMMA-O-MEDIA                 q_k e la SOMMA o la MEDIA dei q_h sulle estremita del nodo?
    DOMANDA-QUALE-FORMA-FISSA-CS                     quale forma del vuoto fissa cs: nessuna delle tre e- libera da tutti i difetti
    DOMANDA-QUALE-INVARIANTE-CON-CS                  con cs non uniforme H_tot non e conservato: quale quantita deve conservare il passo?
    DOMANDA-QUALE-LAMBDA-SULL-ARCO                   quale Lambda usa l arco nel termine di ordinamento: del nodo, la media, o dell arco?
    DOMANDA-QUALE-SCENA-3D-PRINCIPALE                quale scena 3D fa da principale, se nessuna delle due provate e- isotropa?
    DOMANDA-QUALE-SEGNO                              quale segno della non linearita-, se quello che lega lega solo in 1D?
    DOMANDA-QUANDO-LA-CAMMINATA-IN-TABELLA           quando si porta la camminata nella tabella? il porting aspetta TRE decisioni aperte
    DOMANDA-QUANTITA-CONSERVATA                      esiste una moneta isotropa, causale e simmetrica fra le bande con una quantita- conservata?
    DOMANDA-REGOLE-FUORI-CLAUDE                      le regole di gestione fuori da CLAUDE.md, e quelle dentro senza presidio: vanno bene?
    DOMANDA-U-DINAMICA-LE-FORME                      le quattro forme della U d arco dinamica: la scala, il caso senza vuoto, le olonomie, l esponente
    DOMANDA-UNITA-DI-STATO                           l-unita- di stato: qual e- la capacita- di un nodo?
    DOMANDA-VALLE-CARICA                             la valle come carica: K - K' si conserva con la moneta accesa? e il momento angolare modulo 6?
    DOMANDA-VIA-DEL-CAMPO                            si passa alla via del campo, dato che nessuna non linearita- locale lega in 3D?
    INDIRIZZO-MASSA-COLLETTIVA                       l indirizzo di Luca: una massa e una velocita di gruppo collettive, non una massa per nodo
    N-DIREZIONI-DI-MOTO                              le direzioni n della moneta sono DIREZIONI DI MOTO, non un campo fisso
    PIANO-2D-3D                                      IL PIANO: 2D per le proprieta' locali del passo, 3D per le leggi globali (la FCC)
    PROPOSTA-FASE-DISPARI-COESIONE                   la fase DISPARI sotto coniugazione di carica come forma della coesione
    PROPOSTA-LOG1P-IN-N                              log1p nella formula di N: la proposta resta APERTA, e NON si fa ora
    PROPOSTA-SCANSIONE-FORZA-NONLINEARE              la coerenza del cluster migliora con la forza: si estende la scansione?
    PROVV-U-FISSE-TRE-SCENE                          le matrici d-arco sono FISSE, in tre scene dichiarate: provvisorio
    PROVV-VERSORI-NON-RELAZIONALI                    i versori del riferimento locale sono DATI e non relazionali: provvisorio
    SPIN-LEGATO-AL-MOTO                              lo spin si lega al moto: una moneta exp(-i eps dtau sigma.n) e il trasporto U(2)
### FRONTE, APERTA: 11
    AUDIT-CURE                                       per ogni legge aggiunta: compensava un difetto che ORA e' curato? Non il numero: la LEGGE
    CONTA-RIGHE                                      DUE CONVENZIONI PER CONTARE LE RIGHE: i miei strumenti contavano uno in piu' di H-RIGHE
    FINESTRA-PRE-NASCITA                             una finestra PRIMA della prima nascita (216) non dice niente sulle nascite: e' costata TRE volte
    IMPL-2                                           una SECONDA implementazione indipendente, scritta dalle LEGGI e non dal codice
    LINGUAGGIO-REGOLE                                un linguaggio dichiarativo delle leggi, da cui GENERARE il codice e il documento: proposta di Luca
    LOSCHMIDT-ECO                                    l'eco di Loschmidt PER VOCE: un errore subito grande e' irreversibilita' del CODICE
    NON-TRACCIATI                                    484 file non tracciati: 98 CITATI e non tracciati sono riferimenti al vuoto, e il .gitignore blocca
    PIATTAFORMA-NON-TIMBRATA                         I REFERTI NON TIMBRANO LA PIATTAFORMA, e i conteggi assoluti ne dipendono
    PRESTAZIONI-CORSE                                le corse costano: sei strade per il tempo di calcolo, da affrontare a modello STABILE
    REG-V                                            verificaregistro.py: completezza, esistenza, coerenza con la traccia di d0 e col registro dei...
    RISCRITTURA-GO                                   riscrivere il simulatore in Go: valutato, NON deciso
### FRONTE, AGENDA: 35
    CAMMINATA-NELLA-TABELLA                          la camminata entra nella tabella -- ASSORBITA da SIMULATORE-ERA-2, e i quattro punti restano
    CANALE-CS-SECONDA-SORGENTE                       IL CANALE DI cs: LA SECONDA SORGENTE DELL-INSTABILITA- DELLA MATERIA UNIFORME
    CONSERVAZIONE-LOCALE                             A14: ogni legge si giudica su tre domande -- energia locale, carica locale, totali solo per nascita
    CORRENTE-DERIVATA-H-TOT                          la strada D del libro dei conti: una corrente d energia per H_tot derivata dai commutatori
    DIVISIONE-AUTOCONSISTENTE                        la divisione dell arco come UNA legge: dove si rompe, cosa ereditano i figli, il calcio
    EM-CURVATURA-BIDIREZIONALE                       l accoppiamento EM-curvatura e' bidirezionale in natura: il verso EM->curvatura c'e' o manca?
    GEOMETRIA-DELLA-CRESCITA                         SPECULATIVA: lo spazio delle fasi CRESCE, e una forza nuova come OSTRUZIONE fra le nascite
    GRAVITA-POTENZIALE                               due potenziali nel codice e nessun Poisson risolto: Poisson e un VINCOLO DI SCALA
    GRIGLIA-A-TRIANGOLI                              GRIGLIA A TRIANGOLI: GEOMETRIA DALLE SOLE CONNESSIONI
    I1                                               IDEA DI LUCA, per dopo: costruire UNA massa, farla maturare, leggerne la struttura sul grafo e...
    INVARIANZA-LOCALE-CS                             ogni legge che usa una grandezza GLOBALE da all osservatore locale un riferimento esterno
    ISOTROPIA-LOCALE                                 l-irregolarita- locale si attenua con la distanza? e si riduce costruendo meglio la scena?
    LEGAME-SCENE-GRANDI                              il completamento del legame: scene 3D grandi, misura in archi assoluti, e M2
    LIBRO-DEI-CONTI                                  il libro dei conti: conta giusto; H_tot col legame S1 DERIVA senza scalare con s (iv' 0.72): FERMO
    LORENTZ-MATERIA-INTERFERENZA                     la materia per interferenza aggira la violazione di Lorentz che si propaga alle basse energie?
    LUCE-VINCOLO-LAMPI-GAMMA                         LA LUCE DEL MODELLO RISPETTA IL VINCOLO DEI LAMPI GAMMA?
    M-SPINORE                                        trasporto SU(2) per arco con memoria: il candidato campo di gauge della carica
    M1                                               LA MATERIA È UNO STATO, NON UNA SOSTANZA — e non c'è SCARICO. Nel codice la materia è la...
    MAPPA-DEL-LAVORO                                 la mappa del lavoro (doc/MAPPA.md): lo stato in un posto solo, aggiornata a ogni referto e decisione
    MASSE-PESI-SOVRAPPOSTE                           un nodo appartiene a PIU masse con peso diverso: una massa e una configurazione del campo, non nodi
    MATERIA-LEGGERA                                  la materia leggera: v_max/c dipende dalla massa della coppia rispetto alla larghezza della banda?
    MODELLO-MINIMO                                   un modello semplice (spinore, grafo, LAM) da costruire DOPO il simulatore completo
    O4                                               CONSERVAZIONE DELL'ENERGIA. L'energia assorbita non si riesce a bilanciare
    PROGETTO-CURVATURA                               IL PROGETTO DELLA CURVATURA DELLO SPAZIO: cs nelle lunghezze, gamma = 1, sulla carta
    PROGETTO-DRIVER-CAMMINATA                        il progetto del driver della camminata: tre opzioni, lo schema, il timbro, il sigillo, sette domande
    PROGETTO-MASSA-COLLETTIVA                        il progetto della massa collettiva: inventario, ipotesi di Luca, costituenti senza massa, tre misure
    PROGETTO-MITOSI                                  IL PROGETTO DELLA MITOSI NELL ERA 2, sulla carta: olonomia, forma sui triangoli, bilancio col vuoto
    PROGETTO-U1                                      IL PROGETTO DEL CAMPO U(1) SUGLI ARCHI: la luce del modello, sulla carta
    REVERSIBILITA-LOCALE                             reversibilita' LOCALE, irreversibilita' GLOBALE: la sola freccia e' la crescita dello spazio
    RINOMINA-SCENA-QUADRATO                          scena_l2.scena costruisce il quadrato e il nome non lo dice: la rinomina, con i 12 strumenti
    SIMULATORE-ERA-2                                 basta prototipi: la camminata entra in primo_ordine e DIVENTA il simulatore
    SPAZIO-CHE-NASCE                                 lo spazio nasce dalla dinamica: U d-arco dinamica, mitosi al quanto di olonomia
    SPAZIO-TRIANGOLAZIONE-SENZA-POSIZIONI            SPECULATIVA: lo spazio come triangolazione senza posizioni, curvatura nei vertici
    SPAZIOTEMPO-3PIU1                                LE IDEE SULLO SPAZIO-TEMPO 3+1: il tempo dei tick, la FCC a quattro direzioni, torsione e Minkowski
    VUOTO-LOCALE-DETERMINISTICO                      termostato locale + scuotimento DETERMINISTICO: UNA legge per nodo, fase <-> vuoto
### MISURA, APERTA: 2
    DOMANDA-CORRENTE-LOCALE-NON-ESISTE               la corrente locale di E ESISTE per la parte lineare, portata misurata 3 archi
    SCHED-T3-REGOLE                                  le regole di composizione: 94 scritture, 80 nelle cinque forme, 6 eccezioni in tre famiglie
### MISURA, AGENDA: 27
    CARICA-A14-3                                     la carica di A14.3: la rotazione interna sigma_z ha due segni e si conserva a eps 0 e U = I
    CENSIMENTO-DECISIONI                             IL CENSIMENTO DELLE DECISIONI DI LUCA: 48, di cui 25 nel nucleo, 15 giustamente fuori, 8 mancanze
    CONTO-DEL-VUOTO                                  conto del vuoto: nascita con D7 e flip liberano energia; il vuoto uniforme, al massimo, non assorbe
    DIMENSIONE-E-ISOTROPIA-DELLE-SCENE               le scene del banco non hanno dimensione 3, e la mia misura dell-isotropia era confusa
    DIVISIONE-DEL-VUOTO                              la divisione del vuoto: nessuna regola di phi con V conservata chiude il conto della nascita
    ENERGIA-DEL-LEGAME                               il conto dell energia del legame: il vuoto cede energia alla materia; 5/5 coi criteri fino alla vita
    ENERGIA-NON-CONSERVATA-S1                        H_tot col legame S1 e' conservata a O(s^2): la "non conservazione" era lo stato di partenza
    MASSA-NEI-DIFETTI                                la massa nei difetti: nessuno stato legato; il bordo locale non converge; Lambda per nodo cambia cs
    MISURA-ANTIMATERIA-PIEGA-DIVERSO                 i pezzi frazionari fanno piegare il tempo in modo diverso a materia e antimateria
    MISURA-ARCO-E-COINCIDENZA                        nei tick asincroni la frequenza dell-arco e- una COINCIDENZA, non il minimo dei cs
    MISURA-BUCO-SPETTRO-PER-FAMIGLIA                 il buco nello spettro c-e- sull-anello e sul geometrico 3D, non sul cubico
    MISURA-C-ESATTA-OPPURE-LOCALITA                  C esatta oppure localita-, non entrambe: il conto e- il determinante del blocco
    MISURA-CS-NESSUN-EFFETTO-SULLA-MATERIA           a queste taglie il cs locale non produce nessun effetto misurabile sulla materia
    MISURA-DUE-GRUMI-NESSUNA-INTERAZIONE             due grumi non interagiscono, e il 20 per cento di G2(b) sta dentro la barra d-errore
    MISURA-GUSCIO-ANTIFASE                           il guscio in antifase c-e-, ma e- interferenza di Grover e la saturazione lo distrugge
    MISURA-INVARIANZA-LOCALE-V4                      l-invarianza locale della luce: misurata SOLO a cs UNIFORME, e la- i tick asincroni la rispettano
    MISURA-NORMA-ERA2                                la norma totale sum_nodi psi^dag psi: l-invariante QUADRATICO su cui si misura l-integratore
    MISURA-SEGNO-LEGA-IN-1D                          la forma (D) col segno diretto LEGA IN 1D, e in 3D l-effetto cala con la taglia
    SCOMPOSIZIONE-SOLITONE                           l energia a riposo del solitone: i costituenti 127%, il legame -27%, la cinetica ~0
    SCOMPOSIZIONE-ZERO-LAMBDA                        la scomposizione con lo zero simmetrico: il legame 63% dei costituenti, il solitone 37% (5/5)
    SOLITONE-VUOTO-CONGELATO                         il solitone col vuoto congelato: stabile a N 1e6; col tick intero vive 320: lo disfa il vuoto
    SOLITONI-TRIANGOLI                               i solitoni sui triangoli: S1 esiste nel risolutore ma nella dinamica si disfa; S3 e S4 solo stretti
    TORSIONE-DEL-VUOTO                               la torsione del vuoto: in energia massima sul bordo della buca, senza freno; in fase illeggibile
    U1-PROTOTIPO-TRIANGOLI                           IL PROTOTIPO U(1) SUI TRIANGOLI: c = 1 per tempo proprio, Courant 0.408, la DEVE di gauge fallita
    VUOTO-DA-SOLO                                    il vuoto da solo e stabile al bit: il vuoto risponde alla materia, non si disfa per conto suo
    VUOTO-DISTURBATO                                 il vuoto da solo e stabile, non solo stazionario: un disturbo 1e-6 non cresce, cs spento o acceso
    VUOTO-SUL-FONDO                                  il vuoto uniforme e' il MASSIMO; dal fondo il vuoto PRENDE energia, il solitone vive 1.6-1.9 volte
### DIFETTO, APERTA: 20
    BLOB-DAL-DISCO-NON-DAL-REPO                      il blob dichiarato di un reperto era quello del DISCO con le CRLF, non dei committati
    CENS-B16                                         [B] (1) INVENTARIO e (2) README sono prescritti *"nello stesso commit del 
    COLLAUDO-NON-ESEGUITO                            un collaudo che si RIFIUTA di girare esce con 2, e il controllo C4 lo conta come PASS
    D-AGGIORNA-COMMIT-FALSO                          il flag --commit di aggiorna era falso per costruzione: la riga finisce in un commit futuro
    DUE-STRUMENTI-ARCHIVIO-E                         due strumenti per lo stesso mestiere: spostare gli output su E-
    ESENTE-P3                                        (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task... [ESENTE-P3]
    FALSO-UNO                                        un verdetto NEGATIVO prodotto da una voce che non parla del merito: il gemello di FALSO-ZERO
    FALSO-ZERO                                       uno ZERO prodotto da un insieme o un campione che ho scelto io: cinque volte in una sessione
    FUGA-MULTIRIGA                                   la via d'uscita di H-REG-R e H-P1-bis e' una regex SENZA re.S: una dichiarazione su PIU' RIGHE...
    H-REGR-LARGA                                     H-REG-R associa una scheda per NOME DI FUNZIONE: scatta su qualunque modifica a `_applica_flag`...
    INDICE-COLLAUDO-SCRITTURA                        `crea-lotto` e `storico-commit` NON hanno un caso nel collaudo di `indice.py`
    METADATI-REPERTO-PER-NECESSITA                   metadati.jsonl ha una via di scrittura e ZERO storico: e- un REPERTO per necessita-
    PASSO-PIENO                                      un hook che rifiuta uno script che avanza con net.step() invece di csv/_passo.py passo_pieno
    PRESIDIO-RIFIUTO-SOLO-SIGILLI                    _presidio.avvia rifiuta di girare SOLO se il nome comincia con _sigillo_: A9 lo dice senza
    REFERTO-VERDE-SU-FALLIMENTO                      un referto scriveva il segno VERDE su un collaudo FALLITO: 20 su 22 con la spunta
    RELAZIONE-BINARIA                                un NUL letterale rende RELAZIONE_PER_CLAUDE.md binaria per git, e i suoi diff illeggibili
    REPERTI-IMMUTABILI                               APERTA il 2026-09-26 (proposta di Luca), famiglia G | UN COMMIT PUO' TOCCARE UN REPERTO GIA'...
    REPLAY-CIECO-ALLE-CANCELLAZIONI                  il REPLAY di P-T2 non vedeva una cancellazione: 13 su 13 con 4 record tolti
    RIPRESA-ARGV                                     APERTA il 2026-09-26 (limite di un meccanismo che ho costruito io) | LA RIPRESA SI FIDA DEL...
    Z125                                             Z125 DIFETTO DI METODO, MIO ⏳[archivi delle cure · LETTURA] | IL §E NON ESISTE NEL REPO OLTRE E1...
### DIFETTO, AGENDA: 11
    COSTO-MEMORIA-DEI-FLUSSI-PARZIALI                I flussi parziali costano 1.17x dello stato in buffer, e la scena passa la soglia
    DIFETTO-LAMBDA-NON-PIU-INVARIANTE-SOTTO-IL-VUOTO Con i flussi parziali Lambda_k non e piu invariante sotto la camminata del vuoto
    DIFETTO-TERNARIO-CHE-NON-SCEGLIE                 un ternario che non scegliE: per il braccio lineare misuravo la Q di N
    DIFETTO-TRE-MISURE-FUORI-DALLA-SUITE             tre misure della simmetria rotte dal divieto del vuoto nullo, e la suite non le girava
    DOMANDA-DUE-SOGLIE-SENZA-ERRORE                  due soglie senza l-errore da cui proteggono: tol in corrente.instrada e il limite a Lambda zero
    FRECCE-IMPOSTE                                   il censimento delle leggi che impongono una direzione nel tempo: NOVE, e DUE curabili prima
    L-NUMERI-DERIVA-ORFANA                           il rapporto 4.20 della deriva di E non esce da nessuno script: numero orfano
    MEMORIE-MANCANTI                                 il rapporto sulle memorie: il censimento dello stato, il bilancio, e le memorie candidate
    PUNTO-FISSO-CS-SOLITONE                          il punto fisso di cs (tick.tick_con_cs) non converge col solitone S1, gia al tick 0
    STRUMENTI-SULLA-LEGGE-VECCHIA                    20 coppie file/simbolo misurano, saltano o sostituiscono la legge che NON gira
    V-MAX-DIREZIONI                                  _triangoli_forza.v_max sottostima la velocita massima sui gruppi degeneri (61 direzioni)
```
