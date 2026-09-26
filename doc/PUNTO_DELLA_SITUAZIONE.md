# IL PUNTO DELLA SITUAZIONE — **generato dall'INDICE**

> **SOLA LETTURA.** Generato da `csv/_punto_della_situazione.py` leggendo **soltanto**
> `doc/INDICE_ID.tsv`. **Non e' scritto a memoria e non fa piu' parsing di Markdown**:
> se un task manca qui, **manca dall'indice** — e quello e' il difetto da correggere.
> **⚠ Una voce senza ID non compare**: e' il prezzo dichiarato della fonte unica, e il
> collaudo lo verifica *(il caso `CONTAGIO`)*.

```
voci nell'indice    740
elencate qui        485   (tolte le etichette locali, gli assiomi e gli standard)
  di cui task        88
  di cui difetti     47   (tipo `difetto` o `sospetto`)
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

## CON RISERVA — 43

| id | cosa | tipo | ultimo commit che lo nomina |
|---|---|:--:|---|
| **`CLI-1`** | I SIGILLI DI CURA 4 E CURA 5 NON HANNO MAI PROVATO IL PERCORSO CLI: impostavano S.SEMINAMATURA = True e… | `cura` | `7935806 17:03` |
| **`FRAG1`** | mitosi() SU UNA RETE SENZA CAMPO VA IN IndexError INVECE DI DICHIARARLO. I = self.rhosorgente() è vuoto… | `altro` | `4a76517 15:00` |
| **`INERZIA-1(C)`** | 1(C) — CURATA e SIGILLATA 3/6 il 2026-09-25: GIUSTA e INSUFFICIENTE / LA CURA TOGLIE ESATTAMENTE -1.0000 DI… | `altro` | `4a76517 15:00` |
| **`RIPRESA-ARGV`** | APERTA il 2026-09-26 (limite di un meccanismo che ho costruito io) / LA RIPRESA SI FIDA DEL BLOB, E IL BLOB… | `altro` | `4a76517 15:00` |
| **`S09`** | IL TETTO DI r E' RAGGIUNTO PER UNA VIA CHE NON CONOSCIAMO — lettura di Luca, 2026-09-22: la quota di nodi al… | `altro` | `29c7c0b 15:05` |
| **`U2`** | M2 DIVENTA URGENTE — la mitosi mette figli SOTTO la scala di Planck. Con la semina nuova gli archi stanno fra… | `altro` | `f4bc082 11:25` |
| **`Z100`** | Z100 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / INVARIANTI (C5): il programma si ferma quando una grandezza esce… | `fronte` | `bc940ff 22:30` |
| **`Z101`** | Z101 APERTA ⏳[EPOCA 3 · MISURA] / VALIDAZIONE A 600 PASSI: 6 criteri su 8 REGGONO. L'ESPLOSIONE E' SPARITA,… | `fronte` | `bc940ff 22:30` |
| **`Z102`** | Z102 CHIUSA PER MISURA ⏳[EPOCA 3 · MISURA] / CHI FA SCAPPARE d0: E' IL FRENO DELLA SCALA MINIMA. Gli… | `fronte` | `7263b19 16:38` |
| **`Z103`** | Z103 CHIUSA PER MISURA ⏳[EPOCA 3 · MISURA] / IL POZZO GRAVITAZIONALE USA IL DISEGNO, E IL SUO DOCSTRING DICE… | `fronte` | `945f1d7 20:08` |
| **`Z107`** | Z107 CHIUSA PER MISURA ⏳[EPOCA 3 · MISURA] / LA GRAVITA' NON E' IL MOTORE DELLA FUGA DI d0: SPENTA, d0 SCAPPA… | `fronte` | `94be0a5 16:41` |
| **`Z116`** | Z116 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / I TRE BRACCI: 6/8 · 7/8 · 6/8. E SPEGNENDO TUTTO IL… | `fronte` | `ce7939b 20:06` |
| **`Z12`** | Z12 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / pesi() gira SEDICI volte per passo, a cavallo della… | `fronte` | `16e9953 14:48` |
| **`Z121`** | Z121 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / φ NON E' L'AZIMUT DEL VETTORE DI BLOCH. Il docstring… | `fronte` | `df1f42e 20:45` |
| **`Z124`** | Z124 CHIUSA PER MISURA ⏳[archivi delle cure · SIGILLO] / IL SIGILLO DI FASE2PI: 6/6 PASS, e il criterio che… | `fronte` | `01cf2c6 11:43` |
| **`Z13`** | Z13 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / calcolapsi() ricalcola i pesi in TUTTE le chiamate (100 %), e in… | `fronte` | `c04d2b0 18:40` |
| **`Z134`** | Z134 CURA IN CODICE ⏳[archivi delle cure · CURA] / CURA 1 — L'OROLOGIO: RITMOWRAP2PI APPROVATA e accesa dal… | `fronte` | `287e27d 14:40` |
| **`Z135`** | Z135 CHIUSA PER MISURA ⏳[archivi delle cure · PROVA] / LA PROVA DI CURA 1: la mitosi NON muore, il bilancio… | `fronte` | `c04d2b0 18:40` |
| **`Z136`** | Z136 CHIUSA PER DIMOSTRAZIONE ⏳[archivi delle cure · CONTROLLO DI LUCA] / LE DUE STRADE DELLA CURA 1 DANNO LO… | `fronte` | `29c7c0b 15:05` |
| **`Z144`** | Z144 CURA IN CODICE ⏳[archivi delle cure · CURA] / E4-LAM PASSA 6/6: la legge d = LAM si verifica SEMPRE, e… | `fronte` | `3e5b7b3 17:45` |
| **`Z17`** | Z17 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / A6 nell'inerzia e' garantito dall'ORDINE, non dalla… | `fronte` | `82aa2d1 19:03` |
| **`Z24`** | Z24 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL DENOMINATORE PER GRADO: la misura NON distingue (A) da… | `fronte` | `bc30e62 12:48` |
| **`Z29`** | Z29 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / Z24 CHIUSA — dei tre punti UNO era un cricchetto e ora e' CURATO,… | `fronte` | `7935806 17:03` |
| **`Z41`** | Z41 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / median(/f/) FA TRE MESTIERI, NON DUE: E' ANCHE IL… | `fronte` | `5422126 13:41` |
| **`Z47`** | Z47 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / PROGETTO DI LUNGO PERIODO — NON INIZIATO. GEOMETRIA RELAZIONALE SENZA… | `fronte` | `ae29dc4 08:46` |
| **`Z48`** | Z48 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / QUALIFICATA il 2026-09-18: VALE PER IL BATCH. Il «guscio»… | `fronte` | `c90a02d 13:59` |
| **`Z52`** | Z52 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA PREDIZIONE DI LUCA E' SBAGLIATA NELLA SUA FORMA FORTE —… | `fronte` | `092babb 14:09` |
| **`Z53`** | Z53 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / LE COORTI SOPRAVVIVEVANO GIA' ALLA MITOSI. NON SOPRAVVIVEVANO ALLO… | `fronte` | `56b348b 13:12` |
| **`Z71`** | Z71 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / A7 -- LA CARICA CHIRALE NON SI CONSERVA, E IL PUNTO E' UNO SOLO… | `fronte` | `c48ff7f 23:09` |
| **`Z75`** | Z75 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / nsub GOVERNA IL COSTO DELL'INTERO SISTEMA ED E' INVISIBILE: nessun… | `fronte` | `1d511be 20:23` |
| **`Z76`** | Z76 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / I NATI HANNO GRADO 2 E SONO LA MAGGIORANZA DEL SISTEMA: la… | `fronte` | `a69d328 19:16` |
| **`Z77`** | Z77 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / LA TENSIONE NASCE DAL DENOMINATORE: d0 CROLLA A SCATTI mentre d quasi… | `fronte` | `bc30e62 12:48` |
| **`Z78`** | Z78 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / d0 HA DIECI SCRITTORI E NESSUNO E' CONTATO — e i due candidati del… | `fronte` | `6f9d714 09:31` |
| **`Z79`** | Z79 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / d0 NON E' MOSSO DALLA COESIONE: E' MOSSO DAL SUO CLIP — e il clip SCALA… | `fronte` | `bc30e62 12:48` |
| **`Z84`** | Z84 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / E' cs^2lap CHE ALLUNGA L'ARCO — la TENSIONE DEI VICINI, DIFFUSA — e il… | `fronte` | `bc30e62 12:48` |
| **`Z9`** | Z9 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / RISCRITTA IL 2026-09-18 — NON «CHIUSA»: RISCRITTA IN MODO CHE SI… | `fronte` | `294e3f8 13:15` |
| **`Z90`** | Z90 DA RIVERIFICARE ⏳[EPOCA 2 · MISURA] / IL RAMO D DIVERGE: nsub = 22591, E IL VINCOLO VINCENTE E' n1 — LA… | `fronte` | `e435734 17:06` |
| **`Z94`** | Z94 CHIUSA PER MISURA ⏳[EPOCA 2 · MISURA] / peq DIVENTA NEGATIVO, E IL PAVIMENTO max(peq, 1e-9) NON LO… | `fronte` | `92fe29e 21:10` |
| **`Z95`** | Z95 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / PEQESATTO (C1): il rilassamento di peq in forma ESATTA. peq NON… | `fronte` | `b5d526f 19:43` |
| **`Z96`** | Z96 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / PEQNASCITALOCALE (C2): UNA SOLA legge di nascita per peq, e… | `fronte` | `43863af 19:42` |
| **`Z97`** | Z97 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / SCALAMINPASSO (C3): il freno UNA VOLTA PER PASSO. IL CRICCHETTO E'… | `fronte` | `4f39828 20:10` |
| **`Z98`** | Z98 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / COESCAUSALE (C4): un solo ISTANTE e il CONO DEL LUOGO. E col tetto… | `fronte` | `eeb31ec 20:20` |
| **`Z99`** | Z99 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / ANOMSIMM (C1-bis): il pavimento max(peq, 1e-9) E' TOLTO.… | `fronte` | `294e3f8 13:15` |

## IN CODA — 9

| id | cosa | tipo | ultimo commit che lo nomina |
|---|---|:--:|---|
| **`C5RES-INVARIANTI`** | I RESIDUI DI C5 — I4 la scatola nera (rigiocare da solo il passo in cui scatta un invariante), I5 la tabella… | `cura` | `f6d432c 12:45` |
| **`CHK3`** | CHECKPOINT: referto dei quattro esiti, ciascuno contro le sue letture fissate PRIMA / GLOBALE-DISEGNO §5 /… | `cura` | `1fce1b5 13:20` |
| **`CHK3-D`** | Nel referto del CHK3, la sezione «I DIFETTI NUOVI CONTRO LE MISURE GIA' FATTE» — D27 (quattro componenti) e… | `cura` | `944064a 13:06` |
| **`FASCE-TAU`** | LA CRESCITA E' COORDINATA COL TEMPO PROPRIO? — l'espansione non dev'essere omogenea in senso assoluto, ma… | `cura` | `1fce1b5 13:20` |
| **`G4-MEMARCO`** | MEMARCO — LA MEMORIA DEL MOTO TRADOTTA IN FORMA RELAZIONALE (aggiunta di Luca al §4, 2026-09-22) /… | `cura` | `010809a 13:57` |
| **`PAT-1`** | dovespingelagravita.py non rispetta il pattern 5 (nessun CONTROLLO DELL'INVOLUCRO) / PATTERN §4 / PRIMA del… | `cura` | `bf8aaad 17:45` |
| **`PAT-2`** | spegnigravbifase.py:184 non rispetta il pattern 2 (usa max\/Δ\/ invece delle FIRME) / PATTERN §4 / PRIMA del… | `cura` | `bf8aaad 17:45` |
| **`PROBLEMI-CHK3`** | IL PIANO DEI PROBLEMI APERTI — per ciascuno: la domanda da chiudere · la misura o derivazione che la chiude ·… | `cura` | `1fce1b5 13:20` |
| **`SCALE-TW`** | LE SCALE DELLA TORSIONE: un'analisi completa, DA CAPO / mandato di Luca ricevuto alle 17:44 del 2026-09-22 /… | `cura` | `7935806 17:03` |

## BLOCCATO — 5

| id | cosa | tipo | ultimo commit che lo nomina |
|---|---|:--:|---|
| **`NODI-1`** | RITIRATA (Luca, 2026-09-25). NON cancellata: resta come storia, col motivo. PERCHE' È CADUTA, ed è una… | `altro` | `5708a3e 13:12` |
| **`S10`** | S10 RITIRATA il 2026-09-24 / Il tetto 1.414213 di r viene da un ramo di ritmo() che NON GIRA / — / RITIRATA,… | `altro` | `3eb6b7a 13:01` |
| **`Z114`** | Z114 CHIUSA PER DIMOSTRAZIONE / GLI SCRITTORI DI d0 NON TRACCIATI SONO DUE, NON TRE: init (fuori perimetro) e… | `fronte` | `bf8aaad 17:45` |
| **`Z117`** | Z117 CHIUSA PER DIMOSTRAZIONE + MISURA / IL WRAP «A 4π» DI ritmo() NON AVVOLGE NIENTE: su (-2π, 2π) E'… | `fronte` | `29b7846 13:43` |
| **`Z73`** | Z73 RITIRATA ⏳[EPOCA 1 · MISURA] / RITIRATA UNA SECONDA VOLTA il 2026-09-24, e la smentita sta nel MESSAGGIO… | `fronte` | `7935806 17:03` |

## FATTO — 31

| id | cosa | tipo | ultimo commit che lo nomina |
|---|---|:--:|---|
| **`C1-PEQ-ESATTO`** | PEQESATTO — rilassamento in forma esatta / GLOBALE §2① / 7/7 (Z95) | `cura` | `f6d432c 12:45` |
| **`C1BIS-ANOM-SIMM`** | ANOMSIMM — il pavimento 1e-9 tolto / 21/9 §② / 6/6 (Z99) | `cura` | `f6d432c 12:45` |
| **`C2-PEQ-NASCITA`** | PEQNASCITALOCALE — nascita locale di peq / GLOBALE §2② / 6/6 (Z96) | `cura` | `f6d432c 12:45` |
| **`C3-SCALA-MIN-PASSO`** | SCALAMINPASSO — il freno una volta per passo / GLOBALE §2③ / 6/6 (Z97) | `cura` | `f6d432c 12:45` |
| **`C4-COES-CAUSALE`** | COESCAUSALE — istante unico e cono locale / GLOBALE §2④ / 5/5 (Z98) | `cura` | `f6d432c 12:45` |
| **`C5-INVARIANTI`** | INVARIANTI — 42 domini, due livelli / mandato C5 / 3/3 (Z100); accesi di default | `cura` | `f6d432c 12:45` |
| **`CHK2`** | CHECKPOINT 2 / GLOBALE §3 / raggiunto e riferito a Luca. IL RUN LUNGO NON SI LANCIA | `cura` | `1b40fdb 22:37` |
| **`E4-LAM`** | LAM FATTO il 2026-09-24 / LA LEGGE «NESSUNA LUNGHEZZA SOTTO LAM» DEVE DIVENTARE STRUTTURALE — sempre accesa,… | `altro` | `612e7fa 23:14` |
| **`G1`** | §1 QUANTO CONTA IL DISEGNO — Ldisegno/d per arco, per regione, nel tempo, e la correlazione col CENTRO del… | `cura` | `4a76517 15:00` |
| **`G3`** | §3 PROVA DI SPEGNIMENTO: la GRAVITA' BIFASE / GLOBALE-DISEGNO §3 / FATTA. sigillo 7/7 · controllo involucro… | `cura` | `0be343a 09:21` |
| **`G4`** | §4 PROVA DI SPEGNIMENTO: la MEMORIA DEL MOTO — flag MEMMOTO / GLOBALE-DISEGNO §4 / FATTO (finito 14:39:27).… | `cura` | `3eb6b7a 13:01` |
| **`LETTORI-INDICE`** | CHIUSA il 2026-09-26 (decisioni di Luca) / ESITO: 1 RITIRATO, 1 CONVERTITO, 4 FUORI PERIMETRO — e i quattro… | `altro` | `24499f1 17:08` |
| **`OKN-ASSERT`** | CHIUSA il 2026-09-26, a run finito (residuo rilevato da Luca) / UN getattr(..., default) CHE DECIDE AL POSTO… | `altro` | `e216730 01:33` |
| **`POTENZE-1`** | CHIUSA il 2026-09-26 con la CURA A (rhos/W^2), sigillo 6/6: F2 da x47 000 a x1.4, F1 2.427 contro 2.4567… | `altro` | `4a76517 15:00` |
| **`RAMPA-1`** | CHIUSA il 2026-09-25, strada (3) (decisione di Luca): sigillo 9/9 dal CLI, ramp = 1.000000000000000 per 120… | `altro` | `4a5d085 20:33` |
| **`REPERTI-IMMUTABILI`** | APERTA il 2026-09-26 (proposta di Luca), famiglia G / UN COMMIT PUO' TOCCARE UN REPERTO GIA' CITATO DA UN… | `altro` | `4a76517 15:00` |
| **`RIPIEGO-1`** | APERTA E CHIUSA il 2026-09-25 (difetto mio, rilevato da LUCA) / UN RIPIEGO GLOBALE SU UNA CONDIZIONE LOCALE… | `altro` | `da1c65b 01:26` |
| **`S12`** | S12 APPROVATO DA LUCA il 2026-09-24 / IL RILASSAMENTO DI rep DENTRO mitosi() (:5280) E' UN EULERO ESPLICITO,… | `altro` | `e216730 01:33` |
| **`SCENA-1`** | CHIUSA il 2026-09-25, strada (1) (decisione di Luca) / SEMINALAM era approvata ma INCOMPATIBILE con la scena… | `altro` | `f96b4bc 15:07` |
| **`Z106`** | Z106 CHIUSA PER MISURA ⏳[EPOCA 3 · MISURA] / GLI ARCHI PIU' SPINTI DA S09 NON SONO UNA CODA: SONO UN PLATEAU… | `fronte` | `e0dd5a4 16:43` |
| **`Z110`** | Z110 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / r E taupp SONO DUE GRANDEZZE DIVERSE CON LO STESSO… | `fronte` | `cfa33e7 18:55` |
| **`Z111`** | Z111 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / LA REPULSIONE ALLA MASSIMA COMPRESSIONE E' AZZERATA… | `fronte` | `be28256 16:24` |
| **`Z113`** | Z113 CHIUSA PER DIMOSTRAZIONE + MISURA / IL CRICCHETTO DEL FRENO E' CONFERMATO SU RUMORE SIMMETRICO, E… | `fronte` | `6e56ec3 17:58` |
| **`Z118`** | Z118 CHIUSA PER DIMOSTRAZIONE / IL CENSIMENTO DELLE FASI: 52 punti, 38 gravi. E IL NUMERO CHE DECIDE B1 E'… | `fronte` | `4d0fabc 13:57` |
| **`Z119`** | Z119 CHIUSA PER DIMOSTRAZIONE + MISURA / L'ANTIPARTICELLA DI SCHWINGER NASCE CON +2π, E NEL CAMPO E' IDENTICA… | `fronte` | `945f1d7 20:08` |
| **`Z120`** | Z120 CHIUSA PER DIMOSTRAZIONE / LA VERIFICA DI B1: NESSUNA RIGA DELLA FISICA DISTINGUE φ DA φ + 2π, fuori… | `fronte` | `df1f42e 20:45` |
| **`Z122`** | Z122 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / I TEMPI PROPRI DICHIARATI NON SONO DUE, SONO TRE — e… | `fronte` | `d7b2456 20:38` |
| **`Z127`** | Z127 LA LETTURA CADE ⏳[archivi delle cure · PROVA] / E1 NON PASSA: CON FASE2PI LA GENERAZIONE DI MATERIA SI… | `fronte` | `16e9953 14:48` |
| **`Z145`** | CHIUSO — T5 del sigillo di CURA 2 era invalido: dv 0 letto come effetto (2026-09-24) | `fronte` | `a4065e6 00:02` |
| **`Z16`** | Z16 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / Y5 ROSSO: la causa e' rhosorgente <= 0, NON peq. E nessuna delle due… | `fronte` | `45a77d0 18:31` |
| **`Z5`** | Z5 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / A3 NON E' UN CASO PARTICOLARE DI A2 — risolta una delle… | `fronte` | `56b348b 13:12` |

## DIFETTI E SOSPETTI — 47 righe

> **Il raggruppamento e' per il campo `stato` dell'indice**, non per le parole della prosa:
> piu' grossolano di prima *(non distingue `CURA INEFFICACE` da `DA RIMISURARE`)*, ma
> **dichiarato**. Il dettaglio sta nella fonte.

| stato | quanti | quali |
|---|--:|---|
| `aperto` | 26 | `D01` `D02` `D04` `D05` `D06` `D07` `D08` `D10` `D12` `D13` `D14` `D15` `D20` `D21` `D23` `D24` `D28` `D29` `D30` `D32` `D33` `D35` `D38` `DRIVER-SCENA-II` `OSSERVABILE-P1` `RAMPA-2` |
| `chiuso` | 8 | `D11` `D16` `D17` `D18` `D19` `D22` `D34` `D37` |
| `da-decidere` | 11 | `D03` `D25` `D26` `D31` `D36` `REG-A` `REG-B` `REG-C` `REG-R` `REG-V` `U1` |
| `non-difetto` | 2 | `D09` `D27` |

**ID massimo usato:** difetti `D38` · sospetti `—`. **Gli ID non si riusano.**
