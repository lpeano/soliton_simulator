# IL PUNTO DELLA SITUAZIONE — **generato dall'INDICE**

> **SOLA LETTURA.** Generato da `csv/_punto_della_situazione.py` leggendo **soltanto**
> `doc/INDICE_ID.tsv`. **Non e' scritto a memoria e non fa piu' parsing di Markdown**:
> se un task manca qui, **manca dall'indice** — e quello e' il difetto da correggere.
> **⚠ Una voce senza ID non compare**: e' il prezzo dichiarato della fonte unica, e il
> collaudo lo verifica *(il caso `CONTAGIO`)*.

```
voci nell'indice    850
elencate qui        583   (tolte le etichette locali, gli assiomi e gli standard)
  di cui task       147
  di cui difetti     86   (tipo `difetto` o `sospetto`)
  senza marcatore   350   NON elencate: non sono lavoro in corso
```

> ## ⚠ **DUE LIMITI DICHIARATI, e vengono dalla FONTE UNICA**
> ① **le voci senza marcatore non si elencano** *(350)*: nell'indice ci sono **tutti** gli
> ID, anche quelli che non sono lavoro. **Il punto della situazione e' il LAVORO.**
> ② **alcune voci della coda NON HANNO UN ID che l'indice riconosca**, e quindi non possono
> comparire: **`S-MIT1`/`S-MIT2`** *(stem di UNA lettera prima del trattino)*, **`FAMIGLIE`**,
> **`PROVE`**, **`PATTERN`** *(una parola sola)*, **`4-bis`**, **`8-bis`**, **`G4-bis`**
> *(suffisso minuscolo)*, **`V`** *(una lettera)*. **Sono `8` righe della coda unica: se
> devono comparire, gli serve un ID** — e non e' una regex piu' larga, e' una rinomina.

## IN CORSO — 2

| id | cosa | tipo | ultimo commit che lo nomina |
|---|---|:--:|---|
| **`SCHED-PASSO`** | il passo pieno diventa uno SCHEDULATORE: le regole del passo sono architettura, non intenzioni | `cura` | `1f8ceac 09:52` |
| **`SCHED-T3-REGOLE`** | le regole di composizione: 94 scritture, 80 nelle cinque forme, 6 eccezioni in tre famiglie | `misura` | `792b925 15:02` |

## CON RISERVA — 43

| id | cosa | tipo | ultimo commit che lo nomina |
|---|---|:--:|---|
| **`CLI-1`** | I SIGILLI DI CURA 4 E CURA 5 NON HANNO MAI PROVATO IL PERCORSO CLI: impostavano S.SEMINAMATURA =... | `cura` | `a92f599 13:21` |
| **`FRAG1`** | mitosi() SU UNA RETE SENZA CAMPO VA IN IndexError INVECE DI DICHIARARLO. I = self.rhosorgente()... | `altro` | `4a76517 15:00` |
| **`INERZIA-1(C)`** | 1(C) — CURATA e SIGILLATA 3/6 il 2026-09-25: GIUSTA e INSUFFICIENTE / LA CURA TOGLIE ESATTAMENTE... | `altro` | `4a76517 15:00` |
| **`RIPRESA-ARGV`** | APERTA il 2026-09-26 (limite di un meccanismo che ho costruito io) / LA RIPRESA SI FIDA DEL... | `altro` | `4a76517 15:00` |
| **`S09`** | IL TETTO DI r E' RAGGIUNTO PER UNA VIA CHE NON CONOSCIAMO — lettura di Luca, 2026-09-22: la... | `altro` | `a92f599 13:21` |
| **`U2`** | M2 DIVENTA URGENTE — la mitosi mette figli SOTTO la scala di Planck. Con la semina nuova gli... | `altro` | `a461b65 15:15` |
| **`Z100`** | Z100 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / INVARIANTI (C5): il programma si ferma quando una... | `fronte` | `bc940ff 22:30` |
| **`Z101`** | Z101 APERTA ⏳[EPOCA 3 · MISURA] / VALIDAZIONE A 600 PASSI: 6 criteri su 8 REGGONO. L'ESPLOSIONE... | `fronte` | `bc940ff 22:30` |
| **`Z102`** | Z102 CHIUSA PER MISURA ⏳[EPOCA 3 · MISURA] / CHI FA SCAPPARE d0: E' IL FRENO DELLA SCALA MINIMA.... | `fronte` | `7263b19 16:38` |
| **`Z103`** | Z103 CHIUSA PER MISURA ⏳[EPOCA 3 · MISURA] / IL POZZO GRAVITAZIONALE USA IL DISEGNO, E IL SUO... | `fronte` | `52563ed 02:42` |
| **`Z107`** | Z107 CHIUSA PER MISURA ⏳[EPOCA 3 · MISURA] / LA GRAVITA' NON E' IL MOTORE DELLA FUGA DI d0... | `fronte` | `94be0a5 16:41` |
| **`Z116`** | Z116 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / I TRE BRACCI: 6/8 · 7/8 · 6/8. E... | `fronte` | `ce7939b 20:06` |
| **`Z12`** | Z12 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / pesi() gira SEDICI volte per passo, a cavallo... | `fronte` | `4a7597e 09:06` |
| **`Z121`** | Z121 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / φ NON E' L'AZIMUT DEL VETTORE DI BLOCH.... | `fronte` | `df1f42e 20:45` |
| **`Z124`** | Z124 CHIUSA PER MISURA ⏳[archivi delle cure · SIGILLO] / IL SIGILLO DI FASE2PI: 6/6 PASS, e il... | `fronte` | `01cf2c6 11:43` |
| **`Z13`** | Z13 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / calcolapsi() ricalcola i pesi in TUTTE le chiamate... | `fronte` | `c04d2b0 18:40` |
| **`Z134`** | Z134 CURA IN CODICE ⏳[archivi delle cure · CURA] / CURA 1 — L'OROLOGIO: RITMOWRAP2PI APPROVATA e... | `fronte` | `287e27d 14:40` |
| **`Z135`** | Z135 CHIUSA PER MISURA ⏳[archivi delle cure · PROVA] / LA PROVA DI CURA 1: la mitosi NON muore... | `fronte` | `c04d2b0 18:40` |
| **`Z136`** | Z136 CHIUSA PER DIMOSTRAZIONE ⏳[archivi delle cure · CONTROLLO DI LUCA] / LE DUE STRADE DELLA... | `fronte` | `29c7c0b 15:05` |
| **`Z144`** | Z144 CURA IN CODICE ⏳[archivi delle cure · CURA] / E4-LAM PASSA 6/6: la legge d = LAM si... | `fronte` | `3e5b7b3 17:45` |
| **`Z17`** | Z17 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / A6 nell'inerzia e' garantito dall'ORDINE, non... | `fronte` | `82aa2d1 19:03` |
| **`Z24`** | Z24 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL DENOMINATORE PER GRADO: la misura NON... | `fronte` | `bc30e62 12:48` |
| **`Z29`** | Z29 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / Z24 CHIUSA — dei tre punti UNO era un cricchetto e ora... | `fronte` | `7935806 17:03` |
| **`Z41`** | Z41 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / median(/f/) FA TRE MESTIERI, NON DUE: E' ANCHE IL… | `fronte` | `5422126 13:41` |
| **`Z47`** | Z47 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / PROGETTO DI LUNGO PERIODO — NON INIZIATO. GEOMETRIA... | `fronte` | `ae29dc4 08:46` |
| **`Z48`** | Z48 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / QUALIFICATA il 2026-09-18: VALE PER IL BATCH.... | `fronte` | `c90a02d 13:59` |
| **`Z52`** | Z52 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA PREDIZIONE DI LUCA E' SBAGLIATA NELLA SUA... | `fronte` | `092babb 14:09` |
| **`Z53`** | Z53 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / LE COORTI SOPRAVVIVEVANO GIA' ALLA MITOSI. NON... | `fronte` | `56b348b 13:12` |
| **`Z71`** | Z71 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / A7 -- LA CARICA CHIRALE NON SI CONSERVA, E IL PUNTO E' UNO... | `fronte` | `c48ff7f 23:09` |
| **`Z75`** | Z75 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / nsub GOVERNA IL COSTO DELL'INTERO SISTEMA ED E'... | `fronte` | `1d511be 20:23` |
| **`Z76`** | Z76 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / I NATI HANNO GRADO 2 E SONO LA MAGGIORANZA DEL SISTEMA: la… | `fronte` | `a69d328 19:16` |
| **`Z77`** | Z77 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / LA TENSIONE NASCE DAL DENOMINATORE: d0 CROLLA A SCATTI... | `fronte` | `bc30e62 12:48` |
| **`Z78`** | Z78 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / d0 HA DIECI SCRITTORI E NESSUNO E' CONTATO — e i due... | `fronte` | `6f9d714 09:31` |
| **`Z79`** | Z79 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / d0 NON E' MOSSO DALLA COESIONE: E' MOSSO DAL SUO CLIP — e... | `fronte` | `bc30e62 12:48` |
| **`Z84`** | Z84 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / E' cs^2lap CHE ALLUNGA L'ARCO — la TENSIONE DEI VICINI... | `fronte` | `bc30e62 12:48` |
| **`Z9`** | Z9 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / RISCRITTA IL 2026-09-18 — NON «CHIUSA»: RISCRITTA IN... | `fronte` | `294e3f8 13:15` |
| **`Z90`** | Z90 DA RIVERIFICARE ⏳[EPOCA 2 · MISURA] / IL RAMO D DIVERGE: nsub = 22591, E IL VINCOLO VINCENTE... | `fronte` | `e435734 17:06` |
| **`Z94`** | Z94 CHIUSA PER MISURA ⏳[EPOCA 2 · MISURA] / peq DIVENTA NEGATIVO, E IL PAVIMENTO max(peq, 1e-9)... | `fronte` | `92fe29e 21:10` |
| **`Z95`** | Z95 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / PEQESATTO (C1): il rilassamento di peq in forma... | `fronte` | `b5d526f 19:43` |
| **`Z96`** | Z96 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / PEQNASCITALOCALE (C2): UNA SOLA legge di nascita per... | `fronte` | `43863af 19:42` |
| **`Z97`** | Z97 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / SCALAMINPASSO (C3): il freno UNA VOLTA PER PASSO. IL... | `fronte` | `4f39828 20:10` |
| **`Z98`** | Z98 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / COESCAUSALE (C4): un solo ISTANTE e il CONO DEL... | `fronte` | `eeb31ec 20:20` |
| **`Z99`** | Z99 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / ANOMSIMM (C1-bis): il pavimento max(peq, 1e-9) E' TOLTO.… | `fronte` | `294e3f8 13:15` |

## IN CODA — 27

| id | cosa | tipo | ultimo commit che lo nomina |
|---|---|:--:|---|
| **`AB-CONTROLLI`** | l'A/B di W5 non ha salvato i punti di CONTROLLO nel vuoto, e senza quelli la densificazione non... | `altro` | `d21af90 08:13` |
| **`C5RES-INVARIANTI`** | I RESIDUI DI C5 — I4 la scatola nera (rigiocare da solo il passo in cui scatta un invariante)... | `cura` | `f6d432c 12:45` |
| **`CHK3`** | CHECKPOINT: referto dei quattro esiti, ciascuno contro le sue letture fissate PRIMA /... | `cura` | `1fce1b5 13:20` |
| **`CHK3-D`** | Nel referto del CHK3, la sezione «I DIFETTI NUOVI CONTRO LE MISURE GIA' FATTE» — D27 (quattro... | `cura` | `944064a 13:06` |
| **`CLIP-INVENTARIO`** | INVENTARIO dei clip, tetti e pavimenti del passo pieno: 27 TETTI FISICI su 117 guardie | `altro` | `1f8ceac 09:52` |
| **`COLLAUDO-NON-ESEGUITO`** | un collaudo che si RIFIUTA di girare esce con 2, e il controllo C4 lo conta come PASS | `altro` | `8ed23cd 01:31` |
| **`D32-CONTATORE`** | i contatori `_rep_taupp_*` contano un clamp che NON ESISTE PIU' | `altro` | `768653c 01:26` |
| **`DOPPIA-COP`** | LA CURA (b): la doppia copertura 4 pi e' un ASSIOMA e va resa STRUTTURALE, non misurata | `cura` | `eefefb9 11:23` |
| **`FASCE-TAU`** | LA CRESCITA E' COORDINATA COL TEMPO PROPRIO? — l'espansione non dev'essere omogenea in senso... | `cura` | `1fce1b5 13:20` |
| **`FATTI-AVVIO`** | la catena di AVVIO non ha un solo fatto in FATTI_dal_codice.md: _applica_flag, avvia_test... | `fronte` | `982258e 02:01` |
| **`FILI-CORTI`** | i fili si accorciano SOLO FRA LE MASSE o OVUNQUE? Il calo della distanza viene dai `d`, non... | `altro` | `8c2997c 10:00` |
| **`FUGA-MULTIRIGA`** | la via d'uscita di H-REG-R e H-P1-bis e' una regex SENZA re.S: una dichiarazione su PIU' RIGHE... | `altro` | `ee5ecd3 22:52` |
| **`G4-MEMARCO`** | MEMARCO — LA MEMORIA DEL MOTO TRADOTTA IN FORMA RELAZIONALE (aggiunta di Luca al §4, 2026-09-22) /… | `cura` | `010809a 13:57` |
| **`H-ETC-2`** | PRESIDIO PROPOSTO E NON CABLATO: permutare le cinque leggi deve dare lo STESSO stato (Jacobi) | `presidio` | `4b80887 10:49` |
| **`H-REGR-LARGA`** | H-REG-R associa una scheda per NOME DI FUNZIONE: scatta su qualunque modifica a `_applica_flag`... | `altro` | `ee5ecd3 22:52` |
| **`IMPL-2`** | una SECONDA implementazione indipendente, scritta dalle LEGGI e non dal codice | `fronte` | `8f71b29 01:54` |
| **`INDICE-LEGGERO`** | l'indice pesa 169 KB e leggerlo intero non fa risparmiare contesto: serve un comando di... | `fronte` | `18db738 00:54` |
| **`MASSA-MIGRA`** | la massa segue i NODI o la COERENZA? E come cambia la sua FORMA? | `altro` | `6e3d520 08:02` |
| **`PASSO-PIENO`** | un hook che rifiuta uno script che avanza con net.step() invece di csv/_passo.py passo_pieno | `altro` | `fdd9889 01:50` |
| **`PAT-1`** | dovespingelagravita.py non rispetta il pattern 5 (nessun CONTROLLO DELL'INVOLUCRO) / PATTERN §4... | `cura` | `bf8aaad 17:45` |
| **`PAT-2`** | spegnigravbifase.py:184 non rispetta il pattern 2 (usa max\/Δ\/ invece delle FIRME) / PATTERN §4... | `cura` | `bf8aaad 17:45` |
| **`PROBLEMI-CHK3`** | IL PIANO DEI PROBLEMI APERTI — per ciascuno: la domanda da chiudere · la misura o derivazione... | `cura` | `1fce1b5 13:20` |
| **`RAMI-OFF-CURA2`** | i rami a flag spento di TEMPO_UNICO_MITOSI, archiviati COPIATI dal sorgente | `altro` | `6b73f40 01:02` |
| **`RISCRITTURA-GO`** | riscrivere il simulatore in Go: valutato, NON deciso | `altro` | `8e3cf9c 00:58` |
| **`RITMO-PAVIMENTO`** | IL PAVIMENTO DEL RITMO MORDE: min(r) = 1.414212e-06 e' ESATTAMENTE il pavimento, non un valore... | `altro` | `982258e 02:01` |
| **`SCALE-TW`** | LE SCALE DELLA TORSIONE: un'analisi completa, DA CAPO / mandato di Luca ricevuto alle 17:44 del... | `cura` | `a92f599 13:21` |
| **`W5`** | CRITERIO di POZZO-D: A/B nel driver, scena (ii)(a), 4 semi, 120 passi, con la barra fra semi | `altro` | `6e3d520 08:02` |

## BLOCCATO — 12

| id | cosa | tipo | ultimo commit che lo nomina |
|---|---|:--:|---|
| **`MASSA-ID`** | le masse si identificano con l'ID di massa (conc_nodi), non coi nodi del passo 0 ne' con la fase | `altro` | `4f2b224 11:37` |
| **`MASSA-ID-FISSO`** | MASSA-ID a LIGNAGGIO FISSO: non applicabile, la precondizione V-PRE non regge (i nati toccano le mas | `misura` | `4f2b224 11:37` |
| **`NODI-1`** | RITIRATA (Luca, 2026-09-25). NON cancellata: resta come storia, col motivo. PERCHE' È CADUTA, ed... | `altro` | `5708a3e 13:12` |
| **`PROVA1-40-80`** | i NODI delle masse del passo 0 si avvicinano piu' dei controlli a 40-80 passi; il calo sta negli INT | `misura` | `57236bf 10:17` |
| **`S10`** | S10 RITIRATA il 2026-09-24 / Il tetto 1.414213 di r viene da un ramo di ritmo() che NON GIRA / —... | `altro` | `3eb6b7a 13:01` |
| **`SCHW-CORTI`** | il 39 % delle coppie Schwinger ACCORCIA il grafo: 2*dd < d, misurato | `misura` | `a92f599 13:21` |
| **`STATI-LOCALI`** | gli stati .npz del grafo restano LOCALI: in git vanno solo sha1, percorso e comando | `presidio` | `efc7a95 11:55` |
| **`TRATTI-INTERNI`** | a 80 passi il calo di A(t) sta negli INTERNI, non nel varco: le regioni si contraggono | `misura` | `4c4b4bf 11:12` |
| **`VIDEO-SCENA`** | il video della scena del pilota: diagnostico, mostra `pos` che NON e' la distanza fisica | `altro` | `5836e4c 12:07` |
| **`Z114`** | Z114 CHIUSA PER DIMOSTRAZIONE / GLI SCRITTORI DI d0 NON TRACCIATI SONO DUE, NON TRE: init (fuori... | `fronte` | `bf8aaad 17:45` |
| **`Z117`** | Z117 CHIUSA PER DIMOSTRAZIONE + MISURA / IL WRAP «A 4π» DI ritmo() NON AVVOLGE NIENTE: su (-2π... | `fronte` | `18db738 00:54` |
| **`Z73`** | Z73 RITIRATA ⏳[EPOCA 1 · MISURA] / RITIRATA UNA SECONDA VOLTA il 2026-09-20, e la smentita sta... | `fronte` | `2cca038 17:52` |

## FATTO — 63

| id | cosa | tipo | ultimo commit che lo nomina |
|---|---|:--:|---|
| **`ARCH-LCONSERVA`** | _togli_rotazione_rigida esce dal simulatore; L_CONSERVA diventa un no-op accettato | `cura` | `56552f0 08:19` |
| **`ARCH-PAVIMENTI`** | i pavimenti morti (_floor_d0, _pav_d0, i due 0.05 su d) escono dal simulatore | `cura` | `04077b3 17:58` |
| **`ARCH-SYNC`** | SYNC_UPDATE e i suoi rami escono dal simulatore; --sync diventa un no-op accettato | `cura` | `23f81cf 20:10` |
| **`C1-PEQ-ESATTO`** | PEQESATTO — rilassamento in forma esatta / GLOBALE §2① / 7/7 (Z95) | `cura` | `f6d432c 12:45` |
| **`C1BIS-ANOM-SIMM`** | ANOMSIMM — il pavimento 1e-9 tolto / 21/9 §② / 6/6 (Z99) | `cura` | `f6d432c 12:45` |
| **`C2-PEQ-NASCITA`** | PEQNASCITALOCALE — nascita locale di peq / GLOBALE §2② / 6/6 (Z96) | `cura` | `f6d432c 12:45` |
| **`C3-SCALA-MIN-PASSO`** | SCALAMINPASSO — il freno una volta per passo / GLOBALE §2③ / 6/6 (Z97) | `cura` | `f6d432c 12:45` |
| **`C4-COES-CAUSALE`** | COESCAUSALE — istante unico e cono locale / GLOBALE §2④ / 5/5 (Z98) | `cura` | `f6d432c 12:45` |
| **`C5-INVARIANTI`** | INVARIANTI — 42 domini, due livelli / mandato C5 / 3/3 (Z100); accesi di default | `cura` | `f6d432c 12:45` |
| **`CHK2`** | CHECKPOINT 2 / GLOBALE §3 / raggiunto e riferito a Luca. IL RUN LUNGO NON SI LANCIA | `cura` | `1b40fdb 22:37` |
| **`CURA2-STRUTTURALE`** | la CURA 2 diventa STRUTTURALE: i rami `else` di TEMPO_UNICO_MITOSI escono dal simulatore senza... | `altro` | `982258e 02:01` |
| **`E4-LAM`** | LAM FATTO il 2026-09-24 / LA LEGGE «NESSUNA LUNGHEZZA SOTTO LAM» DEVE DIVENTARE STRUTTURALE —... | `altro` | `612e7fa 23:14` |
| **`ETC-C1-CONFINE`** | cura (c) pezzo 1: la fotografia si apre a inizio PASSO PIENO, non di step, e idempotente | `cura` | `6ac0008 22:24` |
| **`ETC-PASSO`** | LA CURA (a): il passo diventa SINCRONO -- fotografia a inizio passo, commit a fine passo | `cura` | `1f8ceac 09:52` |
| **`ETICHETTA-A13`** | l'etichetta sbagliata `A13` dove la regola e' `A3-DISEGNO`: corretta nei documenti, non ancora... | `altro` | `e519408 03:52` |
| **`G1`** | §1 QUANTO CONTA IL DISEGNO — Ldisegno/d per arco, per regione, nel tempo, e la correlazione col... | `cura` | `4a76517 15:00` |
| **`G3`** | §3 PROVA DI SPEGNIMENTO: la GRAVITA' BIFASE / GLOBALE-DISEGNO §3 / FATTA. sigillo 7/7 ·... | `cura` | `0be343a 09:21` |
| **`G4`** | §4 PROVA DI SPEGNIMENTO: la MEMORIA DEL MOTO — flag MEMMOTO / GLOBALE-DISEGNO §4 / FATTO (finito... | `cura` | `8ee4377 17:24` |
| **`H-ETC-1`** | PRESIDIO PROPOSTO E NON CABLATO: zero calcola_psi senza w dentro passo_pieno | `presidio` | `1f8ceac 09:52` |
| **`H-INDICE`** | PRESIDIO DEL HOOK: un ID citato in un documento vivo o nel messaggio che non e' nell'indice | `presidio` | `2b273da 22:34` |
| **`H-P1-bis`** | PRESIDIO DEL HOOK: un referto committato senza toccare la relazione | `presidio` | `ee5ecd3 22:52` |
| **`H-P3`** | PRESIDIO DEL HOOK: un sigillo che configura il modulo A MANO invece di passare dal CLI | `presidio` | `9176216 12:38` |
| **`H-P5`** | PRESIDIO DEL HOOK: un referto che non dichiara la configurazione INTERA | `presidio` | `1b5f7ab 09:07` |
| **`H-P7`** | PRESIDIO DEL HOOK: un flag il cui commento cambia senza nominare quel flag | `presidio` | `69624a8 20:27` |
| **`H-P8`** | PRESIDIO DEL HOOK: un confronto che prende il codice di prima da HEAD invece che dal PADRE | `presidio` | `7b8a396 13:03` |
| **`H-P9`** | PRESIDIO DEL HOOK: uno strumento che fa avanzare una rete con net.step() invece di passo_pieno | `presidio` | `7b8a396 13:03` |
| **`H-REG-R`** | PRESIDIO DEL HOOK: una legge che cambia senza la sua scheda in REGISTRO_FISICA | `presidio` | `8455a16 23:44` |
| **`H-RIGHE`** | PRESIDIO DEL HOOK: CLAUDE.md oltre le 400 righe | `presidio` | `2b273da 22:34` |
| **`H-VALIDATORE`** | PRESIDIO DEL HOOK: un indice mal formato o con una voce persa rispetto al tag | `presidio` | `69624a8 20:27` |
| **`L-DOPO-STOP`** | DOPO UNO STOP, se Luca non risponde si lavora SOLO la coda: nessuna cura fisica, nessun run... | `presidio` | `69624a8 20:27` |
| **`L-NUMERI`** | OGNI NUMERO SCRITTO IN UN COMMIT O IN UN REFERTO ESCE DA UNO SCRIPT | `presidio` | `8455a16 23:44` |
| **`L-PATCH`** | LE PATCH SI LANCIANO IN PRIMO PIANO; niente git stash con una patch in corso; nei patch script... | `presidio` | `2b273da 22:34` |
| **`L-UN-PROMPT`** | UN PROMPT ALLA VOLTA: i rilievi che arrivano durante un lavoro vanno in CODA | `presidio` | `72b27d0 22:41` |
| **`LETTORI-INDICE`** | CHIUSA il 2026-09-26 (decisioni di Luca) / ESITO: 1 RITIRATO, 1 CONVERTITO, 4 FUORI PERIMETRO —... | `altro` | `4f15f7a 18:58` |
| **`MAX-NODI-FERMA`** | MAX_NODI e' una guardia di MEMORIA che oggi cambia la FISICA in silenzio: deve FERMARE il run | `cura` | `a461b65 15:15` |
| **`MITOSI-NON-DIVISA`** | la mitosi NON si spezza per TIPO restando byte-identica: struttura e stato si alternano 26 volte | `misura` | `1003be6 15:13` |
| **`OKN-ASSERT`** | CHIUSA il 2026-09-26, a run finito (residuo rilevato da Luca) / UN getattr(..., default) CHE... | `altro` | `e216730 01:33` |
| **`P1-bis`** | LA RELAZIONE SI SCRIVE NELLO STESSO COMMIT DEL RISCONTRO | `presidio` | `2ebbd25 09:22` |
| **`P1-quater`** | OGNI SOSTITUZIONE DI TESTO SI ASSERISCE PER SE', MAI IN BLOCCO | `presidio` | `1f8ceac 09:52` |
| **`POTENZE-1`** | CHIUSA il 2026-09-26 con la CURA A (rhos/W^2), sigillo 6/6: F2 da x47 000 a x1.4, F1 2.427... | `altro` | `4a76517 15:00` |
| **`POZZO-D`** | la cura di D02 (flag `POZZO_D` nel codice): nel pozzo del grafo `L` viene da `self.d` e non da `pos` | `altro` | `89b8ec9 07:57` |
| **`RAMPA-1`** | CHIUSA il 2026-09-25, strada (3) (decisione di Luca): sigillo 9/9 dal CLI, ramp =... | `altro` | `4a5d085 20:33` |
| **`REPERTI-IMMUTABILI`** | APERTA il 2026-09-26 (proposta di Luca), famiglia G / UN COMMIT PUO' TOCCARE UN REPERTO GIA'... | `altro` | `4a76517 15:00` |
| **`RIORDINO-NOMI-H`** | il prefisso `H-` e' sui NOMI VECCHI (H-P3) e non sui nomi semantici (H-CLI) che la proposta... | `altro` | `13031da 22:08` |
| **`RIORDINO-POSTO2`** | IL POSTO 2 HA 11 REGOLE E IL TETTO E' 10: quale si fonde | `fronte` | `13031da 22:08` |
| **`RIPIEGO-1`** | APERTA E CHIUSA il 2026-09-25 (difetto mio, rilevato da LUCA) / UN RIPIEGO GLOBALE SU UNA... | `altro` | `da1c65b 01:26` |
| **`S12`** | S12 APPROVATO DA LUCA il 2026-09-24 / IL RILASSAMENTO DI rep DENTRO mitosi() (:5280) E' UN... | `altro` | `1486cac 09:27` |
| **`SCENA-1`** | CHIUSA il 2026-09-25, strada (1) (decisione di Luca) / SEMINALAM era approvata ma INCOMPATIBILE... | `altro` | `f96b4bc 15:07` |
| **`SCHED-T1`** | T1 dello schedulatore: la composizione e' una LISTA e c'e' UN SOLO esecutore, esegui_passo | `cura` | `7b8a396 13:03` |
| **`SCHED-T2-TIPI`** | T2 (i tipi): gli 8 tipi del registro del passo, e dopo L_CONSERVA sono coerenti 8 su 8 | `cura` | `1f8ceac 09:52` |
| **`SCHED-T2-VALIDA`** | T2: esegui_passo VALIDA la composizione -- apri primo, coda fissa, registro, nessun doppio | `cura` | `5ac5150 08:56` |
| **`Z106`** | Z106 CHIUSA PER MISURA ⏳[EPOCA 3 · MISURA] / GLI ARCHI PIU' SPINTI DA S09 NON SONO UNA CODA... | `fronte` | `e0dd5a4 16:43` |
| **`Z110`** | Z110 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / r E taupp SONO DUE GRANDEZZE DIVERSE CON... | `fronte` | `cfa33e7 18:55` |
| **`Z111`** | Z111 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / LA REPULSIONE ALLA MASSIMA COMPRESSIONE... | `fronte` | `be28256 16:24` |
| **`Z113`** | Z113 CHIUSA PER DIMOSTRAZIONE + MISURA / IL CRICCHETTO DEL FRENO E' CONFERMATO SU RUMORE... | `fronte` | `6e56ec3 17:58` |
| **`Z118`** | Z118 CHIUSA PER DIMOSTRAZIONE / IL CENSIMENTO DELLE FASI: 52 punti, 38 gravi. E IL NUMERO CHE... | `fronte` | `4a7597e 09:06` |
| **`Z119`** | Z119 CHIUSA PER DIMOSTRAZIONE + MISURA / L'ANTIPARTICELLA DI SCHWINGER NASCE CON +2π, E NEL... | `fronte` | `945f1d7 20:08` |
| **`Z120`** | Z120 CHIUSA PER DIMOSTRAZIONE / LA VERIFICA DI B1: NESSUNA RIGA DELLA FISICA DISTINGUE φ DA φ +... | `fronte` | `4a7597e 09:06` |
| **`Z122`** | Z122 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / I TEMPI PROPRI DICHIARATI NON SONO DUE... | `fronte` | `d7b2456 20:38` |
| **`Z127`** | Z127 LA LETTURA CADE ⏳[archivi delle cure · PROVA] / E1 NON PASSA: CON FASE2PI LA GENERAZIONE DI... | `fronte` | `16e9953 14:48` |
| **`Z145`** | CHIUSO — T5 del sigillo di CURA 2 era invalido: dv 0 letto come effetto (2026-09-24) | `fronte` | `a4065e6 00:02` |
| **`Z16`** | Z16 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / Y5 ROSSO: la causa e' rhosorgente <= 0, NON peq. E nessuna... | `fronte` | `45a77d0 18:31` |
| **`Z5`** | Z5 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / A3 NON E' UN CASO PARTICOLARE DI A2 — risolta... | `fronte` | `56b348b 13:12` |

## DIFETTI E SOSPETTI — 86 righe

> **Il raggruppamento e' per il campo `stato` dell'indice**, non per le parole della prosa:
> piu' grossolano di prima *(non distingue `CURA INEFFICACE` da `DA RIMISURARE`)*, ma
> **dichiarato**. Il dettaglio sta nella fonte.

| stato | quanti | quali |
|---|--:|---|
| `aperto` | 58 | `ALLUNG-RELATIVO` `ARCHI-PRIMI` `CENS-A1` `CENS-A2` `CENS-A3` `CENS-A4` `CENS-A5` `CENS-A6` `CENS-A7` `CENS-B1` `CENS-B10` `CENS-B11` `CENS-B12` `CENS-B13` `CENS-B14` `CENS-B15` `CENS-B16` `CENS-B2` `CENS-B3` `CENS-B4` `CENS-B5` `CENS-B6` `CENS-B7` `CENS-B8` `CENS-B9` `D01` `D04` `D05` `D06` `D07` `D08` `D10` `D12` `D13` `D14` `D15` `D20` `D21` `D23` `D24` `D28` `D29` `D30` `D33` `D35` `D38` `FOGLIO-NULLO` `FORMA-N-VUOTO` `MCRIT-RICALCOLO` `MITOSI-SOGLIA-GRAD` `PSI-FLASH` `RAMPA-2` `RINCULO-RIPETUTI` `S09-MEDIANA` `SCIOGLIMENTO-FASE` `SYNCDB-HEADLESS` `TORS-SPINTA` `V5-SOGLIA` |
| `chiuso` | 14 | `CTRL-RISCELTA` `D02` `D11` `D16` `D17` `D18` `D19` `D22` `D32` `D34` `D37` `DRIVER-SCENA-II` `OSSERVABILE-P1` `T4-TAUTOLOGICO` |
| `da-decidere` | 11 | `D03` `D25` `D26` `D31` `D36` `REG-A` `REG-B` `REG-C` `REG-R` `REG-V` `U1` |
| `non-difetto` | 3 | `D09` `D27` `HASHSEED-RIPROD` |

**ID massimo usato:** difetti `D38` · sospetti `—`. **Gli ID non si riusano.**
