# 🧮 **SMISTAMENTO PER IL RUN BASE — la lista su cui decide Luca** *(2026-09-26)*

*(**Generata** da `csv/_indice_id.py` dall'indice: nessuna riga e' ricopiata a mano.)*

> ## ⚠ **`blocca_run_base` NON E' RIEMPITO A INTUITO.**
> Qui stanno **solo** le voci che potrebbero bloccare: tipo `difetto`, `fronte`, `misura`
> o `cura`, **e** stato `aperto` o `da-decidere`. **Le decide Luca**, riga per riga.
> Tutto il resto — `chiuso`, `non-difetto`, `teoria`, `criterio-locale`, `assioma`,
> `standard` — **non blocca MAI**, ed e' gia' `NO` nell'indice **per regola, non per
> giudizio**.

```
voci nell'indice          740
in questo smistamento     137   (tipo difetto/fronte/misura/cura E stato aperto/da-decidere)
```

## 🎯 **L'ORDINE DI LAVORO DEI `SI`** — 8 voci, e l'ordine E' PER DIPENDENZA

> **Il lavoro sui `SI` comincia SOLO col via di Luca.** Qui c'e' l'ordine e il perche'.

| # | voce | perche' viene qui | stima |
|--:|---|---|--:|
| 1 | **DRIVER-SCENA-II** | **senza un driver che faccia la scena `(ii)`(a) non si puo' girare NIENTE**: viene prima di ogni misura, perche' ogni misura va fatta su quella scena | 1-2 h |
| 2 | **OSSERVABILE-P1** | **e' la grandezza che la `PROVA 1` misura**: viene subito dopo il driver perche' il suo collaudo ha bisogno di una scena vera | 1-1,5 h |
| 3 | **D02** | **il disegno entra nella gravita'** *(`pozzo_grafo` usa `pos` a `:6541`)*: va curato PRIMA delle misure, altrimenti si misura un sistema che si sa difettoso *(`P2`)* | 1,5-2,5 h |
| 4 | **U1** | **misura prima**: quanto pesa `massa_critica_collasso` nei `21` punti | 1 h |
| 5 | **SCALE-TW** | **la misura `M1`**: quanta mitosi e DOVE. Va dopo `D02` perche' la spinta cambia dove i nodi nascono | 1,5-2 h |
| 6 | **D31** | **misura del freno**, e poi la forma decisa `1+tanh`: la deriva si misura sulla scena del driver | 1-1,5 h |
| 7 | **CLI-1** | **i sigilli delle cure 4 e 5 dal CLI**: indipendente dagli altri, si puo' fare in qualunque momento, e sta qui perche' e' il piu' breve | 40-60 min |
| 8 | **D03 · D31 · SCALE-TW** | **LE DECISIONI DI LUCA**: spegnere in modo dichiarato o `MEM_ARCO`; la forma del freno; che fare delle scale della torsione. **Vengono DOPO le misure**, perche' una decisione senza numeri e' una decisione al buio | — (decide Luca) |
| 9 | **RAMPA-2** | **si cura comunque**, e sta per ultima perche' e' il transitorio di un passo | 30-45 min |
| 10 | **RUN BASE** | scena `(ii)`(a), 4 semi, 600 passi, tutte le cure, `P5` attivo, tag `base-epoca-4`; poi la `PROVA 1` | il run: ore-macchina |

**📖 LA REVISIONE STORICA DI OGNI VOCE** *(che cosa e' VERIFICATO sul codice e che cosa e' INFERENZA)*: [CLI-1](REVISIONE_SI_2026-09-26.md#cli-1) · [D02](REVISIONE_SI_2026-09-26.md#d02) · [D03](REVISIONE_SI_2026-09-26.md#d03) · [D31](REVISIONE_SI_2026-09-26.md#d31) · [DRIVER-SCENA-II](REVISIONE_SI_2026-09-26.md#driver-scena-ii) · [OSSERVABILE-P1](REVISIONE_SI_2026-09-26.md#osservabile-p1) · [SCALE-TW](REVISIONE_SI_2026-09-26.md#scale-tw) · [U1](REVISIONE_SI_2026-09-26.md#u1)

**Le voci che NON bloccano hanno la loro sezione qui:** [NON BLOCCANO](REVISIONE_SI_2026-09-26.md#non-bloccano).


**Somma delle stime, senza il run e senza le decisioni: `8,5-12,5 h`.** *(Stime, non misure: la piu' incerta e' `D02`, che tocca una legge.)*

## FAMIGLIA **A** — INERZIA E AVVIO   *(59 voci)*

| blocca? | id | che cos'e' | **il motivo, in una frase** | fonte |
|:--:|---|---|---|---|
| `NO` | **C1-PEQ-ESATTO** | PEQESATTO — rilassamento in forma esatta / GLOBALE §2① / 7/7 (Z95) | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **C2-PEQ-NASCITA** | PEQNASCITALOCALE — nascita locale di peq / GLOBALE §2② / 6/6 (Z96) | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `SI` | **CLI-1** | I SIGILLI DI CURA 4 E CURA 5 NON HANNO MAI PROVATO IL PERCORSO CLI: impostavano S.SEMINAMATURA = True e… | il sigillo delle cure 4 e 5 gira in configurazione DI MODULO, non dal CLI: certifica un percorso che nessun run usa | `STATO_RUN.md` |
| `NO` | **PAT-1** | dovespingelagravita.py non rispetta il pattern 5 (nessun CONTROLLO DELL'INVOLUCRO) / PATTERN §4 / PRIMA del… | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **D20** | La correzione (1) su inerzia NON e' stata cablata, e il gate che la autorizzava aveva misurato UN'ALTRA… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D26** | Le coorti non sopravvivevano allo SNAPSHOT: dopo un salva/ricarica il lignaggio ripartiva VUOTO / Z53,… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D30** | massa chiama semina SENZA massid (:6209), quindi masseinfo non viene MAI popolato e registraconcorrenza non… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D38** | nasce (:3850) e' gated su SCALAMIN or SCALAMINPASSO: la legge «nessun arco sotto LAM» e' VERIFICATA sempre… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `SI` | **DRIVER-SCENA-II** | il 2026-09-26 (rilievo di Luca) / IL DRIVER NON SA FARE LA SCENA (ii), e sono QUATTRO cose insieme… | senza un driver che faccia la scena `(ii)`(a) non esiste il RUN BASE, e le quattro cose sono verificate alle righe citate (`:223`, `:328`, `:7187`, `:8681`) | `STATO_RUN.md` |
| `NO` | **RAMPA-2** | il 2026-09-25 (richiesta di Luca) / AL PASSO 0 TUTTI LEGGONO cs = CSM. La cache csnodoprev non esiste… | e' il transitorio di UN passo: al passo 0 tutti leggono `cs = CS_M`. **Si cura comunque**, ma non blocca il run base | `STATO_RUN.md` |
| `NO` | **REG-B** | FASE B: le SCHEDE, a lotti, un commit per lotto / MANDATO-REGISTRO §2 / LE QUATTRO DELL'ORDINE DI LUCA SONO… | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `SI` | **U1** | URGENTE, PRIMA DI QUALUNQUE GIRO LUNGO — massacriticacollasso: 21 usi DENTRO LEGGI FISICHE (mitosi, step,… | la repulsione di coerenza e' attiva e `massa_critica_collasso` e' usata in `21` punti dentro leggi fisiche: **si misura prima** | `STATO_RUN.md` |
| `NO` | **R2** | 🟨VALE PER QUELLA SCENA ⏳/ NUOVO: il residuo della catena theta = sigma + tau/2 non e'… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **S2** | 🟨VALE PER QUELLA SCENA ⏳/ NON SI RIPRODUCE sul sistema corretto, E CAMBIA SEGNO… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Y1** | ⏳/ Il settore U(1) non ha un'osservabile dell'OROLOGIO / Fra le 256… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z1** | 🟨VALE PER QUELLA SCENA ⏳/ inerzia: la correzione (1) NON e' stata cablata — il gate che… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z101** | ⏳/ VALIDAZIONE A 600 PASSI: 6 criteri su 8 REGGONO. L'ESPLOSIONE E' SPARITA,… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `RAMIFICAZIONI.md` |
| `NO` | **Z12** | 🟨VALE PER QUELLA SCENA ⏳/ pesi() gira SEDICI volte per passo, a cavallo della… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z125** | DIFETTO DI METODO, MIO ⏳[archivi delle cure · LETTURA] / IL §E NON ESISTE NEL REPO OLTRE E1 ED E2: ho… | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `RAMIFICAZIONI.md` |
| `NO` | **Z127** | ⏳[archivi delle cure · PROVA] / E1 NON PASSA: CON FASE2PI LA GENERAZIONE DI MATERIA SI… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `RAMIFICAZIONI.md` |
| `NO` | **Z13** | ⏳/ calcolapsi() ricalcola i pesi in TUTTE le chiamate (100 %), e in… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z17** | 🟨VALE PER QUELLA SCENA ⏳/ A6 nell'inerzia e' garantito dall'ORDINE, non dalla… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z18** | ⏳/ LO SFASAMENTO eta: per mesi il nodo appena nato ha pesato 2e-4… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z21** | 🟨VALE PER QUELLA SCENA ⏳/ SPINFEEDBACK con TAUA = 2.0: ESITO MISTO, e non si sceglie… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z23** | 🟨VALE PER QUELLA SCENA ⏳/ SPINFEEDBACK NON E' ANTISIMMETRICO: sum(out) != 0, e la… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z24** | 🟨VALE PER QUELLA SCENA ⏳/ IL DENOMINATORE PER GRADO: la misura NON distingue (A) da… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z26** | 🟨VALE PER QUELLA SCENA ⏳/ A QUATTRO SEMI SPINFEEDBACK NON PRODUCE EFFETTO MISURABILE.… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z27** | ⏳/ Z24 MISURATA: i tre punti NON sono lo stesso schema. UNO e' un… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z29** | ⏳/ Z24 CHIUSA — dei tre punti UNO era un cricchetto e ora e' CURATO,… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z3** | 🟨VALE PER QUELLA SCENA ⏳/ peq DEGENERE: un fallback a DUE REGIMI, scoperto da un… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z30** | ⏳/ CHIUSA il 2026-09-18 — INDIFFERENTE, quindi nudo per A1 (decisione… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z32** | 🟨VALE PER QUELLA SCENA ⏳/ Z9 RIMISURATA SUL BLOB ATTUALE: INTATTA (+2.8 %). E il… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z33** | 🟨VALE PER QUELLA SCENA ⏳/ LA MEDIANA IN ritmo() E' ENTRAMBE: normalizzazione… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z34** | 🟨VALE PER QUELLA SCENA ⏳/ Z33 MISURATA: NON e' un difetto del GAUGE, e' un difetto di… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z35** | 🟨VALE PER QUELLA SCENA ⏳/ NESSUNA delle due vie cura Z33: la (1) E' IL DIFETTO, la (2)… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z37** | 🟨VALE PER QUELLA SCENA ⏳/ LA CUCITURA DELLO SNAPSHOT FALLISCE SU ENTRAMBI I FRONTI, e… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z38** | 🟨VALE PER QUELLA SCENA ⏳/ IL §1 DEL MANDATO GAUGE E' CHIUSO: il gauge attuale sta… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z41** | 🟨VALE PER QUELLA SCENA ⏳/ median(/f/) FA TRE MESTIERI, NON DUE: E' ANCHE IL… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z42** | 🟨VALE PER QUELLA SCENA ⏳/ CURATO E SIGILLATO 10/10 — L'ANELLO ISTANTANEO DI ritmo() E'… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z44** | 🟨VALE PER QUELLA SCENA ⏳/ CHIUSA — f = 0 NON E' FISICA: E' IL TRANSITORIO DI NASCITA.… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z45** | 🟨VALE PER QUELLA SCENA ⏳/ CHIUSA — L'IPOTESI MATERIA/ANTIMATERIA CADE. L'universo e'… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z46** | 🟨VALE PER QUELLA SCENA ⏳/ IL 93 % DEI NODI NON INVECCHIA, SONO SEMPRE GLI STESSI, E… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z48** | 🟨VALE PER QUELLA SCENA ⏳/ QUALIFICATA il 2026-09-18: VALE PER IL BATCH. Il «guscio»… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z49** | 🟨VALE PER QUELLA SCENA ⏳/ IL CICLO C'E', MA NON E' NEL CORPO: E' NELLA CODA. E… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z50** | 🟨VALE PER QUELLA SCENA ⏳/ QUALIFICATA il 2026-09-18: VALE PER LA REGIONE DENSA. Il… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z52** | 🟨VALE PER QUELLA SCENA ⏳/ LA PREDIZIONE DI LUCA E' SBAGLIATA NELLA SUA FORMA FORTE —… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z53** | ⏳/ LE COORTI SOPRAVVIVEVANO GIA' ALLA MITOSI. NON SOPRAVVIVEVANO ALLO… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z57** | 🟨VALE PER QUELLA SCENA ⏳/ omegas NON E' UN CRICCHETTO PURO: cresce la CODA, non il… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z60** | 🟨VALE PER QUELLA SCENA ⏳/ LA CRONOLOGIA DELLA DEGENERAZIONE: r NON CRESCE, PARTE… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z66** | 🟨VALE PER QUELLA SCENA ⏳/ median(lambdanodi()) SI CONGELA: 0.6092 IDENTICO A QUATTRO… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z69** | 🟨VALE PER QUELLA SCENA ⏳/ SEI GUARDIE PROTEGGONO DA UN DIFETTO GIA' CURATO, e le (c)… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z87** | ⏳/ d SCENDE A DIECI VOLTE SOTTO LAM MENTRE SCALAMIN E' ACCESO, E LA… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z88** | ⏳/ AVVERTENZA SULL'EPOCA 1: OTTO grandezze che la SEMINA legge sono… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z9** | ⏳/ RISCRITTA IL 2026-09-18 — NON «CHIUSA»: RISCRITTA IN MODO CHE SI… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z90** | ⏳/ IL RAMO D DIVERGE: nsub = 22591, E IL VINCOLO VINCENTE E' n1 — LA… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **C20** | 🟨VALE PER QUELLA SCENA ⏳/ PRIMA MISURA DELLA CONSERVAZIONE DI Ltot =… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **C22** | 🟨VALE PER QUELLA SCENA ⏳/ LA CRESCITA DI Ltot E' L'INERZIA CHE SI ACCENDE, NON UNA… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **C24** | 🟨VALE PER QUELLA SCENA ⏳/ LA CRESCITA DI Ltot STA NELLA CODA, NON NEL NODO TIPICO —… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **OMEGA-ETA** | il 2026-09-26 (Luca: da seguire nel run base, NON una cura) / IL RAPPORTO /omega/ FIGLIO/MATURO SALE… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |

## FAMIGLIA **B** — TEMPO UNICO   *(10 voci)*

| blocca? | id | che cos'e' | **il motivo, in una frase** | fonte |
|:--:|---|---|---|---|
| `NO` | **C4-COES-CAUSALE** | COESCAUSALE — istante unico e cono locale / GLOBALE §2④ / 5/5 (Z98) | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **CHK3-D** | Nel referto del CHK3, la sezione «I DIFETTI NUOVI CONTRO LE MISURE GIA' FATTE» — D27 (quattro componenti) e… | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **FASCE-TAU** | LA CRESCITA E' COORDINATA COL TEMPO PROPRIO? — l'espansione non dev'essere omogenea in senso assoluto, ma… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **G1** | §1 QUANTO CONTA IL DISEGNO — Ldisegno/d per arco, per regione, nel tempo, e la correlazione col CENTRO del… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **Z43** | 🟨VALE PER QUELLA SCENA ⏳/ APERTA — ED E' UNA DECISIONE SULLA DEFINIZIONE DEL TEMPO,… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z5** | 🟨VALE PER QUELLA SCENA ⏳/ A3 NON E' UN CASO PARTICOLARE DI A2 — risolta una delle… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z51** | 🟨VALE PER QUELLA SCENA ⏳/ LA Y NON C'E': NE' NEL DENSO, NE' NEL VUOTO, NE' NELLA… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **C12** | 🟨VALE PER QUELLA SCENA ⏳/ SECONDO CASO DEL PUNTO FISSO AUTO-NORMALIZZANTE. r è… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **C13** | 🟨VALE PER QUELLA SCENA ⏳/ IL TEMPO-LUCE NON E' TESTABILE A QUESTA DENSITA'. cs non e'… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **C5** | 🟨VALE PER QUELLA SCENA ⏳/ tauluce = d/cs e' PIATTO ⇒ la sostituzione rompe la… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |

## FAMIGLIA **C** — DOPPIA COPERTURA E CREAZIONE   *(11 voci)*

| blocca? | id | che cos'e' | **il motivo, in una frase** | fonte |
|:--:|---|---|---|---|
| `NO` | **CURA-3** | phi su 2pi con le soglie che la seguono / nella forma decisa: frazioni che sul dominio 4pi danno… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **PAT-2** | spegnigravbifase.py:184 non rispetta il pattern 2 (usa max\/Δ\/ invece delle FIRME) / PATTERN §4 / PRIMA del… | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **D35** | L'antiparticella di Schwinger nasce con +2π (:5443) e nel campo F = Σ exp(iφ) E' IDENTICA alla particella,… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **REG-A** | FASE A del registro della fisica: l'INVENTARIO degli scrittori di stato / MANDATO-REGISTRO §2 / FATTA… | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **REG-C** | FASE C: LA STORIA di ogni legge, e le schede delle leggi TOLTE / MANDATO-REGISTRO §2 / cio' che non si… | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **REG-R** | LA REGOLA MANTENUTA del registro della fisica — la riga in CLAUDE.md («nessuna legge fisica entra, cambia o… | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **Z25** | 🟨VALE PER QUELLA SCENA ⏳/ CHIUSA — IL DENOMINATORE PER GRADO ERA UN ERRORE, ed e'… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z36** | 🟨VALE PER QUELLA SCENA ⏳/ APERTA, MA RI-LETTA il 2026-09-18 (Z37): il 64.7 % e' UN… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z56** | 🟨VALE PER QUELLA SCENA ⏳/ chibasc: NON E' UNA MONOCOLTURA CHE SI RIBALTA — e la… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **C17** | 🟨VALE PER QUELLA SCENA ⏳/ LA DISPERSIONE DI r E' RUMORE: la FASE 5 non ha, a oggi,… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **MITOSI-TASSO** | il 2026-09-26 (era una voce PERSA: viveva senza ID) / CHE IL TASSO DI MITOSI RESTI DELLO STESSO ORDINE… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |

## FAMIGLIA **D** — SOGLIE TARATE E SOTTO PLANCK   *(4 voci)*

| blocca? | id | che cos'e' | **il motivo, in una frase** | fonte |
|:--:|---|---|---|---|
| `NO` | **C1BIS-ANOM-SIMM** | ANOMSIMM — il pavimento 1e-9 tolto / 21/9 §② / 6/6 (Z99) | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **Z28** | 🟨VALE PER QUELLA SCENA ⏳/ CHIUSA PRIMA DI NASCERE — il limite «serve una topologia a… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z64** | 🟨VALE PER QUELLA SCENA ⏳/ L'ALGEBRA SU x E' FALSIFICATA (fattore 44 000), f CROLLA… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **C21** | ⏳/ TRE CRITERI DI SIGILLO SBAGLIATI IN UN GIORNO, tutti scritti dal… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |

## FAMIGLIA **E** — DISEGNO E STATISTICHE GLOBALI   *(7 voci)*

| blocca? | id | che cos'e' | **il motivo, in una frase** | fonte |
|:--:|---|---|---|---|
| `NO` | **CHK2** | CHECKPOINT 2 / GLOBALE §3 / raggiunto e riferito a Luca. IL RUN LUNGO NON SI LANCIA | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **CHK3** | CHECKPOINT: referto dei quattro esiti, ciascuno contro le sue letture fissate PRIMA / GLOBALE-DISEGNO §5 /… | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **E3** | EPOCA 3 + RUN LUNGO — tag epoca-3, 3000 passi, M1/M4 leggere durante il run / GLOBALE §4 / 🔒 solo dopo che i… | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **G4-MEMARCO** | MEMARCO — LA MEMORIA DEL MOTO TRADOTTA IN FORMA RELAZIONALE (aggiunta di Luca al §4, 2026-09-22) /… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D14** | median(\/f\/) fa TRE mestieri, non due: e' anche il rompi-anello / Z41 / — / APERTO | la scala globale e' **uguale ovunque**: non introduce una differenza fra nodi | `STATO_RUN.md` |
| `NO` | **Z82** | 🟨VALE PER QUELLA SCENA ⏳/ SOSPETTO NON VERIFICATO: n3 normalizza su median(d), e nel… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **C23** | 🟨VALE PER QUELLA SCENA ⏳/ IL FATTORE (CSM/cs)^2 NON E' 1 SULLA CODA a 500 passi. La… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |

## FAMIGLIA **F** — FRENO E CONTRAZIONE   *(33 voci)*

| blocca? | id | che cos'e' | **il motivo, in una frase** | fonte |
|:--:|---|---|---|---|
| `NO` | **C3-SCALA-MIN-PASSO** | SCALAMINPASSO — il freno una volta per passo / GLOBALE §2③ / 6/6 (Z97) | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **C5RES-INVARIANTI** | I RESIDUI DI C5 — I4 la scatola nera (rigiocare da solo il passo in cui scatta un invariante), I5 la tabella… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D0** | CHI FA SCAPPARE d0 / 21/9 / MISURATO: e' IL FRENO. Gli scrittori spingono giu' -1.543e+05, il vincolo… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **G2** | §2 DOVE SPINGE LA GRAVITA' / GLOBALE-DISEGNO §2 / FATTO. Il saldo vive sul CONFINE vuoto-massa (-1.4150/arco,… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **G3** | §3 PROVA DI SPEGNIMENTO: la GRAVITA' BIFASE / GLOBALE-DISEGNO §3 / FATTA. sigillo 7/7 · controllo involucro… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **G4** | §4 PROVA DI SPEGNIMENTO: la MEMORIA DEL MOTO — flag MEMMOTO / GLOBALE-DISEGNO §4 / FATTO (finito 14:39:27).… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **PROBLEMI-CHK3** | IL PIANO DEI PROBLEMI APERTI — per ciascuno: la domanda da chiudere · la misura o derivazione che la chiude ·… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **PROVA-COMB** | LA PROVA COMBINATA: TUTTE LE CURE APPROVATE ACCESE INSIEME — 600 passi, stesso seme e scena, letture della… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `SI` | **SCALE-TW** | LE SCALE DELLA TORSIONE: un'analisi completa, DA CAPO / mandato di Luca ricevuto alle 17:44 del 2026-09-22 /… | prima la misura `M1`: **quanta mitosi e DOVE** -- senza quella, le scale della torsione si leggerebbero su un sistema che non si sa dove crea | `STATO_RUN.md` |
| `NO` | **D01** | S09 clippa al passo causale — quindi e' gia' una LUNGHEZZA — e poi moltiplica per median(d0): statistica… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `SI` | **D02** | pozzografo calcola L da self.pos — IL DISEGNO — mentre il suo docstring dichiara «la distanza REALE» / G1… | `pozzo_grafo` usa `self.pos` a `:6541` -- **verificato** -- ed entra nella spinta `S09`: il disegno entra nella gravita' | `STATO_RUN.md` |
| `SI` | **D03** | La memoria del moto prende le direzioni da pos, normalizza su Imed GLOBALE, e ha un tetto 0.01median(d0) /… | decisione di Luca: **o si spegne in modo dichiarato, o `MEM_ARCO`** -- la memoria del moto prende le direzioni da `pos` e normalizza su una mediana GLOBALE | `STATO_RUN.md` |
| `NO` | **D04** | smpchiudi() RISCRIVE tutto d0 a fine passo e NON ha nessun tracciad0 attorno: e' una scrittura invisibile… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D24** | A2 e' VIOLATO da Lam = mean(I) -- una media GLOBALE dentro una legge locale -- e la violazione e' la ragione… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D25** | Il gauge del tempo e' la costante 1e-9, e il 93 % dei nodi non invecchia / Z46 — MISURATO IN EPOCA 1, blob… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `STATO_RUN.md` |
| `NO` | **D28** | nsub esplode e lo tira max(/vd/) su POCHISSIMI archi: il costo dell'intero sistema e' governato da una… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `SI` | **D31** | Il freno di SCALAMIN (smpchiudi) E' IL MOTORE della crescita di d0: vale il 117.41 % del Δ, mentre gli… | il freno di `_smorza` e' ancora a SENSO UNICO -- **verificato**: il docstring dice «smorzando solo la DISCESA» e `eff = where(scende, dx*fatt, dx)`; `Z91` e' curato e acceso | `STATO_RUN.md` |
| `NO` | **D32** | I TEMPI PROPRI DICHIARATI SONO TRE, E SONO TRE GRANDEZZE DIVERSE: r, taupp e d/cs. corr(r, taupp) fra -0.25 e… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D33** | La repulsione alla massima compressione e' AZZERATA proprio dove serve: dal 75 % al 96 % degli archi oltre… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D36** | LA SOGLIA DELLA MITOSI E' IN UNITA' ASSOLUTE DI tw, MENTRE LA SCALA DI tw DIPENDE DAL DOMINIO DI phi: le due… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `SI` | **OSSERVABILE-P1** | il 2026-09-26 (rilievo di Luca) / NON ESISTE UNO STRUMENTO UFFICIALE PER LA DISTANZA FRA LE MASSE. La… | e' la grandezza che la `PROVA 1` misura: senza, la prova non ha numero | `STATO_RUN.md` |
| `NO` | **REG-V** | verificaregistro.py: completezza, esistenza, coerenza con la traccia di d0 e col registro dei domini di C5 /… | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **X2** | 🟨VALE PER QUELLA SCENA ⏳/ ZETALOC: «smorzamento locale» che dipende da una statistica… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z104** | ⏳/ MEMARCO: LA MEMORIA DEL MOTO TRADOTTA IN FORMA RELAZIONALE — la legge… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `RAMIFICAZIONI.md` |
| `NO` | **Z142** | REPERTO, DIFETTI MIEI ⏳[archivi delle cure · SIGILLO FALLITO] / IL SIGILLO DI E4-LAM FALLISCE 4/5, E I… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `RAMIFICAZIONI.md` |
| `NO` | **Z148** | LA LEGGE d = LAM REGGE PERCHE' UNA CURA E' ACCESA (2026-09-24) | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `RAMIFICAZIONI.md` |
| `NO` | **Z39** | ⏳/ UN FATTO STABILE DI CLAUDE.md E' CADUTO: cs E' VIVO. csstd/cs =… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z4** | 🟨VALE PER QUELLA SCENA ⏳/ floord0: SOSPESA, e i due rami violano assiomi DIVERSI… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z74** | 🟨VALE PER QUELLA SCENA ⏳/ il ramo B rallenta x11: nsub esplode, e lo tira \/vd\/.max()… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z89** | ⏳/ 1755 MB DI .pkl NON HANNO IL COMANDO CHE LI RIGENERA, e il… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z91** | ⏳/ SCALAMIN FRENA OGNI SCRITTURA SEPARATAMENTE, QUINDI IL RISULTATO… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z92** | 🟨LIMITE DICHIARATO ⏳/ COESADIM legge ISTANTI MISTI, e il suo tetto e'… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **C18** | 🟨VALE PER QUELLA SCENA ⏳/ IL FDT RIFATTO SUL SISTEMA NON CASTRATO (FASE 5 attiva,… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |

## FAMIGLIA **G** — ARRETRATO DEGLI STRUMENTI   *(2 voci)*

| blocca? | id | che cos'e' | **il motivo, in una frase** | fonte |
|:--:|---|---|---|---|
| `NO` | **D13** | I sigilli storici non sono stati rigirati sul blob corrente / Z11 / — / APERTO | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **Z15** | ⏳/ 14 .pkl su 36 non portano il BLOB del codice che li ha prodotti, e… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |

## FAMIGLIA **?** — SENZA FAMIGLIA — nessuna regola ha deciso   *(11 voci)*

| blocca? | id | che cos'e' | **il motivo, in una frase** | fonte |
|:--:|---|---|---|---|
| `NO` | **D05** | I residui di C5: I4 scatola nera, I5 underflow per riga, modalita' fine / il mandato C5 e la coda / — / APERTO | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D06** | fattcsultimo e' SCRITTO e MAI LETTO (quarto caso della stessa famiglia) / Z7, letto dal codice / — / APERTO | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D07** | TAUA e' UN SOLO numero per DUE leggi fisiche distinte / Z10, Z9-bis / — / APERTO | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D08** | Il terzo ramo di calcolapsi (elif sotto REPULSLEGGE) e' DICHIARATO, non corretto / Z14, letto dal codice / —… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D10** | nsub governa il costo dell'intero sistema ed e' INVISIBILE: nessun contatore, nessuna colonna / Z75 / — /… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D12** | 1755 MB di .pkl non hanno il comando che li rigenera (par.5-quinquies: «un dato che nessuno potra' rifare») /… | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **D15** | A7: la carica chirale NON si conserva / Z71, letto dal codice / — / APERTO | la premessa e' superata da `CHI_COOP` *(decisione di Luca)* | `STATO_RUN.md` |
| `NO` | **D21** | floord0 e' SOSPESA, e i due rami violano assiomi DIVERSI: la scelta non e' stata fatta / Z4 / — / APERTO | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D23** | La cucitura dello snapshot FALLISCE su entrambi i fronti, e si DIMOSTRA perche'. NON CABLATA / Z37 / — / APERTO | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D29** | CINQUE NODI DI VUOTO sono i piu' connessi dell'intero sistema: il vuoto ha degli HUB, e non dovrebbe averne /… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **B7-SHAKE** | SHAKE 🟨VALE PER QUELLA SCENA ⏳/ shake-then-freeze — la precessione mutua non organizza /… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |

---

**COSA QUESTA LISTA NON DICE:**
- **non dice che le altre 603 voci siano irrilevanti**: dice che **non possono bloccare un
  run base** perche' sono chiuse, sono teoria, o sono etichette locali di un sigillo.
- **il titolo e' UNA riga**: la spiegazione sta nella fonte, e la fonte e' nella colonna.
- **`DA-DECIDERE` e' la risposta onesta**, non una casella vuota: nessun documento dichiara
  che quella voce blocchi o non blocchi il run base.
