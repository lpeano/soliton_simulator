# 🧮 **SMISTAMENTO PER IL RUN BASE — la lista su cui decide Luca** *(2026-09-26)*

*(**Generata** da `csv/_vista_smistamento.py` **dai DATI**: `doc/INDICE_ID.tsv` +
`doc/ORDINE_SI.tsv`. **Nessuna decisione sta nel codice**, e questa vista **non si modifica a
mano**: si rigenera.)*

> ## ⚠ **`blocca_run_base` NON E' RIEMPITO A INTUITO.**
> Qui stanno **solo** le voci che potrebbero bloccare: tipo `difetto`, `fronte`, `misura` o
> `cura`, **e** stato `aperto` o `da-decidere`. Tutto il resto — `chiuso`, `non-difetto`,
> `teoria`, `criterio-locale`, `assioma`, `standard` — **non blocca MAI**, ed e' `NO`
> **per regola, non per giudizio**.

```
voci nell'indice          777
in questo smistamento     137   (tipo difetto/fronte/misura/cura E stato aperto/da-decidere)
di cui blocca SI          6
```

## 🎯 **L'ORDINE DI LAVORO DEI `SI`** — 6 voci, e l'ordine E' PER DIPENDENZA

> **Il lavoro sui `SI` comincia SOLO col via di Luca.** L'ordine e i motivi vengono da
> **`doc/ORDINE_SI.tsv`**, che e' un DATO: si cambia la' dentro, non qui.

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

**📖 LA REVISIONE STORICA DI OGNI VOCE** *(che cosa e' VERIFICATO sul codice e che cosa e'
INFERENZA)*: [CLI-1](REVISIONE_SI_2026-09-26.md#cli-1) · [D02](REVISIONE_SI_2026-09-26.md#d02) · [D03](REVISIONE_SI_2026-09-26.md#d03) · [D31](REVISIONE_SI_2026-09-26.md#d31) · [SCALE-TW](REVISIONE_SI_2026-09-26.md#scale-tw) · [U1](REVISIONE_SI_2026-09-26.md#u1)

**Le voci che NON bloccano hanno la loro sezione qui:** [NON BLOCCANO](REVISIONE_SI_2026-09-26.md#non-bloccano).

## FAMIGLIA **A** — INERZIA E AVVIO   *(58 voci)*

| blocca? | id | che cos'e' | **il motivo, in una frase** | fonte |
|:--:|---|---|---|---|
| `NO` | **C1-PEQ-ESATTO** | PEQESATTO — rilassamento in forma esatta / GLOBALE §2① / 7/7 (Z95) | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **C2-PEQ-NASCITA** | PEQNASCITALOCALE — nascita locale di peq / GLOBALE §2② / 6/6 (Z96) | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `SI` | **CLI-1** | I SIGILLI DI CURA 4 E CURA 5 NON HANNO MAI PROVATO IL PERCORSO CLI: impostavano S.SEMINAMATURA =... | il sigillo delle cure 4 e 5 gira in configurazione DI MODULO, non dal CLI: certifica un percorso che nessun run usa | `STATO_RUN.md` |
| `NO` | **PAT-1** | dovespingelagravita.py non rispetta il pattern 5 (nessun CONTROLLO DELL'INVOLUCRO) / PATTERN §4... | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **D20** | La correzione (1) su inerzia NON e' stata cablata, e il gate che la autorizzava aveva misurato... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D26** | Le coorti non sopravvivevano allo SNAPSHOT: dopo un salva/ricarica il lignaggio ripartiva VUOTO... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D30** | massa chiama semina SENZA massid (:6209), quindi masseinfo non viene MAI popolato e... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D38** | nasce (:3850) e' gated su SCALAMIN or SCALAMINPASSO: la legge «nessun arco sotto LAM» e'... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **RAMPA-2** | APERTA il 2026-09-25 (richiesta di Luca) / AL PASSO 0 TUTTI LEGGONO cs = CSM. La cache... | e' il transitorio di UN passo: al passo 0 tutti leggono `cs = CS_M`. **Si cura comunque**, ma non blocca il run base | `STATO_RUN.md` |
| `NO` | **REG-B** | FASE B: le SCHEDE, a lotti, un commit per lotto / MANDATO-REGISTRO §2 / LE QUATTRO DELL'ORDINE... | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `SI` | **U1** | URGENTE, PRIMA DI QUALUNQUE GIRO LUNGO — massacriticacollasso: 21 usi DENTRO LEGGI FISICHE... | la repulsione di coerenza e' attiva e `massa_critica_collasso` e' usata in `21` punti dentro leggi fisiche: **si misura prima** | `STATO_RUN.md` |
| `NO` | **R2** | R2 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / NUOVO: il residuo della catena theta = sigma +... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **S2** | S2 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / NON SI RIPRODUCE sul sistema corretto, E CAMBIA... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Y1** | Y1 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / Il settore U(1) non ha un'osservabile dell'OROLOGIO /... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z1** | Z1 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / inerzia: la correzione (1) NON e' stata cablata... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z101** | Z101 APERTA ⏳[EPOCA 3 · MISURA] / VALIDAZIONE A 600 PASSI: 6 criteri su 8 REGGONO. L'ESPLOSIONE... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `RAMIFICAZIONI.md` |
| `NO` | **Z12** | Z12 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / pesi() gira SEDICI volte per passo, a cavallo... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z125** | Z125 DIFETTO DI METODO, MIO ⏳[archivi delle cure · LETTURA] / IL §E NON ESISTE NEL REPO OLTRE E1... | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `RAMIFICAZIONI.md` |
| `NO` | **Z127** | Z127 LA LETTURA CADE ⏳[archivi delle cure · PROVA] / E1 NON PASSA: CON FASE2PI LA GENERAZIONE DI... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `RAMIFICAZIONI.md` |
| `NO` | **Z13** | Z13 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / calcolapsi() ricalcola i pesi in TUTTE le chiamate... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z17** | Z17 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / A6 nell'inerzia e' garantito dall'ORDINE, non... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z18** | Z18 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / LO SFASAMENTO eta: per mesi il nodo appena nato ha... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z21** | Z21 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / SPINFEEDBACK con TAUA = 2.0: ESITO MISTO, e non... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z23** | Z23 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / SPINFEEDBACK NON E' ANTISIMMETRICO: sum(out) !=... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z24** | Z24 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL DENOMINATORE PER GRADO: la misura NON... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z26** | Z26 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / A QUATTRO SEMI SPINFEEDBACK NON PRODUCE EFFETTO... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z27** | Z27 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / Z24 MISURATA: i tre punti NON sono lo stesso schema.... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z29** | Z29 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / Z24 CHIUSA — dei tre punti UNO era un cricchetto e ora... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z3** | Z3 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / peq DEGENERE: un fallback a DUE REGIMI, scoperto... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z30** | Z30 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / CHIUSA il 2026-09-18 — INDIFFERENTE, quindi nudo per... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z32** | Z32 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / Z9 RIMISURATA SUL BLOB ATTUALE: INTATTA (+2.8... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z33** | Z33 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA MEDIANA IN ritmo() E' ENTRAMBE: normalizzazione… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z34** | Z34 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / Z33 MISURATA: NON e' un difetto del GAUGE, e'... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z35** | Z35 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / NESSUNA delle due vie cura Z33: la (1) E' IL... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z37** | Z37 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA CUCITURA DELLO SNAPSHOT FALLISCE SU ENTRAMBI... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z38** | Z38 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL §1 DEL MANDATO GAUGE E' CHIUSO: il gauge... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z41** | Z41 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / median(/f/) FA TRE MESTIERI, NON DUE: E' ANCHE IL… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z42** | Z42 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / CURATO E SIGILLATO 10/10 — L'ANELLO ISTANTANEO... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z44** | Z44 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / CHIUSA — f = 0 NON E' FISICA: E' IL TRANSITORIO... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z45** | Z45 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / CHIUSA — L'IPOTESI MATERIA/ANTIMATERIA CADE.... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z46** | Z46 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL 93 % DEI NODI NON INVECCHIA, SONO SEMPRE GLI... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z48** | Z48 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / QUALIFICATA il 2026-09-18: VALE PER IL BATCH.... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z49** | Z49 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL CICLO C'E', MA NON E' NEL CORPO: E' NELLA... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z50** | Z50 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / QUALIFICATA il 2026-09-18: VALE PER LA REGIONE... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z52** | Z52 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA PREDIZIONE DI LUCA E' SBAGLIATA NELLA SUA... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z53** | Z53 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / LE COORTI SOPRAVVIVEVANO GIA' ALLA MITOSI. NON... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z57** | Z57 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / omegas NON E' UN CRICCHETTO PURO: cresce la... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z60** | Z60 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA CRONOLOGIA DELLA DEGENERAZIONE: r NON... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z66** | Z66 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / median(lambdanodi()) SI CONGELA: 0.6092... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z69** | Z69 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / SEI GUARDIE PROTEGGONO DA UN DIFETTO GIA'... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z87** | Z87 DA RIVERIFICARE ⏳[EPOCA 2 · MISURA] / d SCENDE A DIECI VOLTE SOTTO LAM MENTRE SCALAMIN E'... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z88** | Z88 DA RIVERIFICARE ⏳[EPOCA 1 · CODICE] / AVVERTENZA SULL'EPOCA 1: OTTO grandezze che la SEMINA... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z9** | Z9 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / RISCRITTA IL 2026-09-18 — NON «CHIUSA»: RISCRITTA IN... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z90** | Z90 DA RIVERIFICARE ⏳[EPOCA 2 · MISURA] / IL RAMO D DIVERGE: nsub = 22591, E IL VINCOLO VINCENTE... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **C20** | C20 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / PRIMA MISURA DELLA CONSERVAZIONE DI Ltot =… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **C22** | C22 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA CRESCITA DI Ltot E' L'INERZIA CHE SI... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **C24** | C24 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA CRESCITA DI Ltot STA NELLA CODA, NON NEL... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **OMEGA-ETA** | APERTA il 2026-09-26 (Luca: da seguire nel run base, NON una cura) / IL RAPPORTO /omega/... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |

## FAMIGLIA **B** — TEMPO UNICO   *(10 voci)*

| blocca? | id | che cos'e' | **il motivo, in una frase** | fonte |
|:--:|---|---|---|---|
| `NO` | **C4-COES-CAUSALE** | COESCAUSALE — istante unico e cono locale / GLOBALE §2④ / 5/5 (Z98) | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **CHK3-D** | Nel referto del CHK3, la sezione «I DIFETTI NUOVI CONTRO LE MISURE GIA' FATTE» — D27 (quattro... | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **FASCE-TAU** | LA CRESCITA E' COORDINATA COL TEMPO PROPRIO? — l'espansione non dev'essere omogenea in senso... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **G1** | §1 QUANTO CONTA IL DISEGNO — Ldisegno/d per arco, per regione, nel tempo, e la correlazione col... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **Z43** | Z43 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / APERTA — ED E' UNA DECISIONE SULLA DEFINIZIONE... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z5** | Z5 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / A3 NON E' UN CASO PARTICOLARE DI A2 — risolta... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z51** | Z51 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA Y NON C'E': NE' NEL DENSO, NE' NEL VUOTO... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **C12** | C12 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / SECONDO CASO DEL PUNTO FISSO... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **C13** | C13 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL TEMPO-LUCE NON E' TESTABILE A QUESTA... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **C5** | C5 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / tauluce = d/cs e' PIATTO ⇒ la sostituzione rompe la… | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |

## FAMIGLIA **C** — DOPPIA COPERTURA E CREAZIONE   *(11 voci)*

| blocca? | id | che cos'e' | **il motivo, in una frase** | fonte |
|:--:|---|---|---|---|
| `NO` | **CURA-3** | - phi su 2pi con le soglie che la seguono / nella forma decisa: frazioni che sul dominio 4pi danno… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **PAT-2** | spegnigravbifase.py:184 non rispetta il pattern 2 (usa max\/Δ\/ invece delle FIRME) / PATTERN §4... | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **D35** | L'antiparticella di Schwinger nasce con +2π (:5443) e nel campo F = Σ exp(iφ) E' IDENTICA alla... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **REG-A** | FASE A del registro della fisica: l'INVENTARIO degli scrittori di stato / MANDATO-REGISTRO §2 /... | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **REG-C** | FASE C: LA STORIA di ogni legge, e le schede delle leggi TOLTE / MANDATO-REGISTRO §2 / cio' che... | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **REG-R** | LA REGOLA MANTENUTA del registro della fisica — la riga in CLAUDE.md («nessuna legge fisica... | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **Z25** | Z25 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / CHIUSA — IL DENOMINATORE PER GRADO ERA UN... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z36** | Z36 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / APERTA, MA RI-LETTA il 2026-09-18 (Z37): il... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z56** | Z56 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / chibasc: NON E' UNA MONOCOLTURA CHE SI RIBALTA... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **C17** | C17 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA DISPERSIONE DI r E' RUMORE: la FASE 5 non... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **MITOSI-TASSO** | APERTA il 2026-09-26 (era una voce PERSA: viveva senza ID) / CHE IL TASSO DI MITOSI RESTI DELLO... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |

## FAMIGLIA **D** — SOGLIE TARATE E SOTTO PLANCK   *(4 voci)*

| blocca? | id | che cos'e' | **il motivo, in una frase** | fonte |
|:--:|---|---|---|---|
| `NO` | **C1BIS-ANOM-SIMM** | ANOMSIMM — il pavimento 1e-9 tolto / 21/9 §② / 6/6 (Z99) | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **Z28** | Z28 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / CHIUSA PRIMA DI NASCERE — il limite «serve una... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z64** | Z64 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / L'ALGEBRA SU x E' FALSIFICATA (fattore 44 000)... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **C21** | C21 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / TRE CRITERI DI SIGILLO SBAGLIATI IN UN GIORNO, tutti... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |

## FAMIGLIA **E** — DISEGNO E STATISTICHE GLOBALI   *(7 voci)*

| blocca? | id | che cos'e' | **il motivo, in una frase** | fonte |
|:--:|---|---|---|---|
| `NO` | **CHK2** | CHECKPOINT 2 / GLOBALE §3 / raggiunto e riferito a Luca. IL RUN LUNGO NON SI LANCIA | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **CHK3** | CHECKPOINT: referto dei quattro esiti, ciascuno contro le sue letture fissate PRIMA /... | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **E3** | EPOCA 3 + RUN LUNGO — tag epoca-3, 3000 passi, M1/M4 leggere durante il run / GLOBALE §4 / 🔒... | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **G4-MEMARCO** | MEMARCO — LA MEMORIA DEL MOTO TRADOTTA IN FORMA RELAZIONALE (aggiunta di Luca al §4, 2026-09-22) /… | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D14** | median(\/f\/) fa TRE mestieri, non due: e' anche il rompi-anello / Z41 / — / APERTO | la scala globale e' **uguale ovunque**: non introduce una differenza fra nodi | `STATO_RUN.md` |
| `NO` | **Z82** | Z82 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / SOSPETTO NON VERIFICATO: n3 normalizza su... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **C23** | C23 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL FATTORE (CSM/cs)^2 NON E' 1 SULLA CODA a 500... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |

## FAMIGLIA **F** — FRENO E CONTRAZIONE   *(31 voci)*

| blocca? | id | che cos'e' | **il motivo, in una frase** | fonte |
|:--:|---|---|---|---|
| `NO` | **C3-SCALA-MIN-PASSO** | SCALAMINPASSO — il freno una volta per passo / GLOBALE §2③ / 6/6 (Z97) | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **C5RES-INVARIANTI** | I RESIDUI DI C5 — I4 la scatola nera (rigiocare da solo il passo in cui scatta un invariante)... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D0** | CHI FA SCAPPARE d0 / 21/9 / MISURATO: e' IL FRENO. Gli scrittori spingono giu' -1.543e+05, il... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **G2** | §2 DOVE SPINGE LA GRAVITA' / GLOBALE-DISEGNO §2 / FATTO. Il saldo vive sul CONFINE vuoto-massa... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **G3** | §3 PROVA DI SPEGNIMENTO: la GRAVITA' BIFASE / GLOBALE-DISEGNO §3 / FATTA. sigillo 7/7 ·... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **G4** | §4 PROVA DI SPEGNIMENTO: la MEMORIA DEL MOTO — flag MEMMOTO / GLOBALE-DISEGNO §4 / FATTO (finito... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **PROBLEMI-CHK3** | IL PIANO DEI PROBLEMI APERTI — per ciascuno: la domanda da chiudere · la misura o derivazione... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **PROVA-COMB** | LA PROVA COMBINATA: TUTTE LE CURE APPROVATE ACCESE INSIEME — 600 passi, stesso seme e scena... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `SI` | **SCALE-TW** | LE SCALE DELLA TORSIONE: un'analisi completa, DA CAPO / mandato di Luca ricevuto alle 17:44 del... | prima la misura `M1`: **quanta mitosi e DOVE** -- senza quella, le scale della torsione si leggerebbero su un sistema che non si sa dove crea | `STATO_RUN.md` |
| `NO` | **D01** | S09 clippa al passo causale — quindi e' gia' una LUNGHEZZA — e poi moltiplica per median(d0)... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `SI` | **D02** | pozzografo calcola L da self.pos — IL DISEGNO — mentre il suo docstring dichiara «la distanza... | `pozzo_grafo` usa `self.pos` a `:6541` -- **verificato** -- ed entra nella spinta `S09`: il disegno entra nella gravita' | `STATO_RUN.md` |
| `SI` | **D03** | La memoria del moto prende le direzioni da pos, normalizza su Imed GLOBALE, e ha un tetto... | decisione di Luca: **o si spegne in modo dichiarato, o `MEM_ARCO`** -- la memoria del moto prende le direzioni da `pos` e normalizza su una mediana GLOBALE | `STATO_RUN.md` |
| `NO` | **D04** | smpchiudi() RISCRIVE tutto d0 a fine passo e NON ha nessun tracciad0 attorno: e' una scrittura... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D24** | A2 e' VIOLATO da Lam = mean(I) -- una media GLOBALE dentro una legge locale -- e la violazione... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D25** | Il gauge del tempo e' la costante 1e-9, e il 93 % dei nodi non invecchia / Z46 — MISURATO IN... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `STATO_RUN.md` |
| `NO` | **D28** | nsub esplode e lo tira max(/vd/) su POCHISSIMI archi: il costo dell'intero sistema e' governato... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `SI` | **D31** | Il freno di SCALAMIN (smpchiudi) E' IL MOTORE della crescita di d0: vale il 117.41 % del Δ... | il freno di `_smorza` e' ancora a SENSO UNICO -- **verificato**: il docstring dice «smorzando solo la DISCESA» e `eff = where(scende, dx*fatt, dx)`; `Z91` e' curato e acceso | `STATO_RUN.md` |
| `NO` | **D33** | La repulsione alla massima compressione e' AZZERATA proprio dove serve: dal 75 % al 96 % degli... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D36** | LA SOGLIA DELLA MITOSI E' IN UNITA' ASSOLUTE DI tw, MENTRE LA SCALA DI tw DIPENDE DAL DOMINIO DI... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **REG-V** | verificaregistro.py: completezza, esistenza, coerenza con la traccia di d0 e col registro dei... | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **X2** | X2 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / ZETALOC: «smorzamento locale» che dipende da una... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z104** | Z104 APERTA ⏳[EPOCA 3 · DERIVAZIONE] / MEMARCO: LA MEMORIA DEL MOTO TRADOTTA IN FORMA... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `RAMIFICAZIONI.md` |
| `NO` | **Z142** | Z142 REPERTO, DIFETTI MIEI ⏳[archivi delle cure · SIGILLO FALLITO] / IL SIGILLO DI E4-LAM... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `RAMIFICAZIONI.md` |
| `NO` | **Z148** | LA LEGGE d = LAM REGGE PERCHE' UNA CURA E' ACCESA (2026-09-24) | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `RAMIFICAZIONI.md` |
| `NO` | **Z39** | Z39 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / UN FATTO STABILE DI CLAUDE.md E' CADUTO: cs E' VIVO.... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z4** | Z4 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / floord0: SOSPESA, e i due rami violano assiomi... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z74** | Z74 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / il ramo B rallenta x11: nsub esplode, e lo tira... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z89** | Z89 DA RIVERIFICARE ⏳[EPOCA 1 · CODICE] / 1755 MB DI .pkl NON HANNO IL COMANDO CHE LI RIGENERA... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z91** | Z91 APERTA ⏳[EPOCA 2 · LETTURA DEL CODICE] / SCALAMIN FRENA OGNI SCRITTURA SEPARATAMENTE, QUINDI... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **Z92** | Z92 🟨LIMITE DICHIARATO ⏳[EPOCA 2 · LETTURA DEL CODICE] / COESADIM legge ISTANTI MISTI, e il suo... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |
| `NO` | **C18** | C18 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL FDT RIFATTO SUL SISTEMA NON CASTRATO (FASE 5... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |

## FAMIGLIA **G** — ARRETRATO DEGLI STRUMENTI   *(2 voci)*

| blocca? | id | che cos'e' | **il motivo, in una frase** | fonte |
|:--:|---|---|---|---|
| `NO` | **D13** | I sigilli storici non sono stati rigirati sul blob corrente / Z11 / — / APERTO | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **Z15** | Z15 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / 14 .pkl su 36 non portano il BLOB del codice che li ha... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |

## FAMIGLIA **?** — SENZA FAMIGLIA — nessuna regola ha deciso   *(14 voci)*

| blocca? | id | che cos'e' | **il motivo, in una frase** | fonte |
|:--:|---|---|---|---|
| `NO` | **D05** | I residui di C5: I4 scatola nera, I5 underflow per riga, modalita' fine / il mandato C5 e la... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D06** | fattcsultimo e' SCRITTO e MAI LETTO (quarto caso della stessa famiglia) / Z7, letto dal codice /... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D07** | TAUA e' UN SOLO numero per DUE leggi fisiche distinte / Z10, Z9-bis / — / APERTO | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D08** | Il terzo ramo di calcolapsi (elif sotto REPULSLEGGE) e' DICHIARATO, non corretto / Z14, letto... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D10** | nsub governa il costo dell'intero sistema ed e' INVISIBILE: nessun contatore, nessuna colonna /... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D12** | 1755 MB di .pkl non hanno il comando che li rigenera (par.5-quinquies: «un dato che nessuno... | voce di PROCESSO o di STRUMENTO: non e' una legge del sistema | `STATO_RUN.md` |
| `NO` | **D15** | A7: la carica chirale NON si conserva / Z71, letto dal codice / — / APERTO | la premessa e' superata da `CHI_COOP` *(decisione di Luca)* | `STATO_RUN.md` |
| `NO` | **D21** | floord0 e' SOSPESA, e i due rami violano assiomi DIVERSI: la scelta non e' stata fatta / Z4 / —... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D23** | La cucitura dello snapshot FALLISCE su entrambi i fronti, e si DIMOSTRA perche'. NON CABLATA /... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **D29** | CINQUE NODI DI VUOTO sono i piu' connessi dell'intero sistema: il vuoto ha degli HUB, e non... | nessuna prova la lega al run base: **non blocca fino a prova contraria**, ed e' la regola, non un giudizio | `STATO_RUN.md` |
| `NO` | **FATTI-AVVIO** | la catena di AVVIO non ha un solo fatto in FATTI_dal_codice.md: _applica_flag, avvia_test... |  | `FATTI_dal_codice.md` |
| `NO` | **IMPL-2** | una SECONDA implementazione indipendente, scritta dalle LEGGI e non dal codice |  | `VALUTAZIONE_go.md` |
| `NO` | **INDICE-LEGGERO** | l'indice pesa 169 KB e leggerlo intero non fa risparmiare contesto: serve un comando di... |  | `csv/_indice_id.py` |
| `NO` | **B7-SHAKE** | SHAKE 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / shake-then-freeze — la precessione mutua non... | fronte di epoca 1-2 o «vale per quella scena»: e' una MISURA DA RIFARE, non un ostacolo | `RAMIFICAZIONI.md` |

---

**COSA QUESTA LISTA NON DICE:**
- **non dice che le altre 640 voci siano irrilevanti**: dice che **non possono bloccare un run
  base** perche' sono chiuse, sono teoria, o sono etichette locali di un sigillo.
- **il titolo e' UNA riga**: la spiegazione sta nella fonte, e la fonte e' in colonna.
- **`motivo` viene dalla COLONNA dell'indice**, non da una regola di questo script: se una riga
  non ha motivo, **manca il DATO**, e lo dice.
