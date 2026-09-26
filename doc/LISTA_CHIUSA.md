# 📋 **LA LISTA CHIUSA — BOZZA PER L'APPROVAZIONE DI LUCA**

*(**Generata** da `csv/_lista_chiusa.py` da **UNA fonte**: `doc/INDICE_ID.tsv`. `P1-ter`.)*

> ## ⚠ **NON E' ANCORA UNA LISTA CHIUSA: E' UNA PROPOSTA.** La approva Luca.
> **Nessuna voce e' esclusa in silenzio:** `FUORI LISTA` porta ogni voce **col motivo**, e i
> motivi vengono dai **campi dichiarati** dell'indice (`stato`, `tipo`), non da una regex sulla
> prosa.

## 🔄 **QUESTA VISTA NON FA PIU' PARSING DI MARKDOWN** *(`PASSO 3` ridotto)*

| | prima (fino al 2026-09-26) | ora |
|---|---|---|
| fonti | **cinque** documenti in Markdown | **una**: `doc/INDICE_ID.tsv` |
| che cos'e' una voce | **inferito** dalla contiguita' delle righe | un `id`, **dichiarato** |
| lo stato | **inferito** dalle parole della riga | la colonna `stato` |
| la famiglia | **inferita** da parole chiave, `111` senza famiglia | la colonna `famiglia` |
| il testo | `420` caratteri della riga | `117` del `titolo_breve` **+ la fonte in colonna** |

```
voci nell'indice      738
in LISTA              333   (stato aperto o da-decidere, e un tipo che puo' essere un fronte)
FUORI LISTA           405   col motivo, dai campi dell'indice
```

---

## LE SETTE FAMIGLIE

| | famiglia | cosa raccoglie | voci in lista |
|---|---|---|--:|
| **A** | **INERZIA E AVVIO** | l'inerzia spinoriale, il contrasto, `rho_s`, la rampa, cio' che decide come nasce un nodo | 54 |
| **B** | **TEMPO UNICO** | un solo orologio: `dt_n`/`dt_e` contro `DT` nudo, `r`, `tau_pp`, le medie d'arco | 9 |
| **C** | **DOPPIA COPERTURA E CREAZIONE** | la fase su `2pi`/`4pi`, la torsione `tw`, la mitosi, Schwinger, cio' che si eredita | 14 |
| **D** | **SOGLIE TARATE E SOTTO PLANCK** | `A11`: ogni clip, pavimento o tetto che non esprima un vincolo dichiarato | 5 |
| **E** | **DISEGNO E STATISTICHE GLOBALI** | `A2`/`A5`: mediane e medie globali dentro una legge locale, e il disegno nella fisica | 9 |
| **F** | **FRENO E CONTRAZIONE** | `SCALA_MIN`, il freno a senso unico, la coesione, la repulsione, `d0`, `LAM` | 44 |
| **G** | **ARRETRATO DEGLI STRUMENTI** | presidi, ancore, reperti, ripresa, il passo incompleto: **non e' fisica** | 8 |
| **?** | **SENZA FAMIGLIA** | nessuna regola dell'indice ha deciso: **le elenco invece di metterle in una famiglia a caso** | 190 |

---

## FAMIGLIA **A** — INERZIA E AVVIO   *(54 voci)*

| blocca? | id | alias | che cos'e' | stato | tipo | fonte |
|:--:|---|---|---|:--:|:--:|---|
| `DA-DECIDERE` | **CLI-1** | — | I SIGILLI DI CURA 4 E CURA 5 NON HANNO MAI PROVATO IL PERCORSO CLI: impostavano S.SEMINAMATURA = True e… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **CONFIG-1** | — | APERTA il 2026-09-25 / LE SEI MISURE DI OGGI GIRAVANO CON 28 LEGGI SU 31 SPENTE, misurato… | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D20** | — | La correzione (1) su inerzia NON e' stata cablata, e il gate che la autorizzava aveva misurato UN'ALTRA… | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D26** | — | Le coorti non sopravvivevano allo SNAPSHOT: dopo un salva/ricarica il lignaggio ripartiva VUOTO / Z53,… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D30** | — | massa chiama semina SENZA massid (:6209), quindi masseinfo non viene MAI popolato e registraconcorrenza non… | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **I1** | — | IDEA DI LUCA, per dopo: costruire UNA massa, farla maturare, leggerne la struttura sul grafo e REPLICARLA… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **INERZIA-1** | — | LA LEGGE DELL'INERZIA CEDE A k = 2, ED È UN DIFETTO DIMOSTRATO (misura 3, f8b27d9): coppia ×2.39, inerzia… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **M2** | — | LA MITOSI — DUE DIFETTI DA ACCLARARE. ① il figlio nasce nel PUNTO MEDIO: posfiglio = 0.5 (self.pos[a] +… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **OMEGA-ETA** | — | APERTA il 2026-09-26 (Luca: da seguire nel run base, NON una cura) / IL RAPPORTO /omega/ FIGLIO/MATURO SALE… | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **RAMPA-2** | — | APERTA il 2026-09-25 (richiesta di Luca) / AL PASSO 0 TUTTI LEGGONO cs = CSM. La cache csnodoprev non esiste… | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S08** | — | Se φ non e' l'azimut del Bloch, CHE COS'E'? / Z121 ha refutato la frase del docstring (R ≤ 0.18 contro un… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S12** | — | S12 APPROVATO DA LUCA il 2026-09-24 / IL RILASSAMENTO DI rep DENTRO mitosi() (:5280) E' UN EULERO ESPLICITO,… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `SI` | **U1** | — | URGENTE, PRIMA DI QUALUNQUE GIRO LUNGO — massacriticacollasso: 21 usi DENTRO LEGGI FISICHE (mitosi, step,… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **U2** | — | M2 DIVENTA URGENTE — la mitosi mette figli SOTTO la scala di Planck. Con la semina nuova gli archi stanno fra… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **C1-PEQ-ESATTO** | C1 | PEQESATTO — rilassamento in forma esatta / GLOBALE §2① / 7/7 (Z95) | `da-decidere` | `cura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **C2-PEQ-NASCITA** | C2 | PEQNASCITALOCALE — nascita locale di peq / GLOBALE §2② / 6/6 (Z96) | `da-decidere` | `cura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **PAT-1** | — | dovespingelagravita.py non rispetta il pattern 5 (nessun CONTROLLO DELL'INVOLUCRO) / PATTERN §4 / PRIMA del… | `da-decidere` | `cura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D38** | — | nasce (:3850) e' gated su SCALAMIN or SCALAMINPASSO: la legge «nessun arco sotto LAM» e' VERIFICATA sempre… | `aperto` | `difetto` | `STATO_RUN.md` |
| `DA-DECIDERE` | **REG-B** | — | FASE B: le SCHEDE, a lotti, un commit per lotto / MANDATO-REGISTRO §2 / LE QUATTRO DELL'ORDINE DI LUCA SONO… | `da-decidere` | `difetto` | `STATO_RUN.md` |
| `DA-DECIDERE` | **R2** | — | R2 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / NUOVO: il residuo della catena theta = sigma + tau/2 non e'… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **S2** | — | S2 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / NON SI RIPRODUCE sul sistema corretto, E CAMBIA SEGNO… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Y1** | — | Y1 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / Il settore U(1) non ha un'osservabile dell'OROLOGIO / Fra le 256… | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z1** | — | Z1 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / inerzia: la correzione (1) NON e' stata cablata — il gate che… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z12** | — | Z12 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / pesi() gira SEDICI volte per passo, a cavallo della… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z125** | — | Z125 DIFETTO DI METODO, MIO ⏳[archivi delle cure · LETTURA] / IL §E NON ESISTE NEL REPO OLTRE E1 ED E2: ho… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z127** | — | Z127 LA LETTURA CADE ⏳[archivi delle cure · PROVA] / E1 NON PASSA: CON FASE2PI LA GENERAZIONE DI MATERIA SI… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z134** | — | Z134 CURA IN CODICE ⏳[archivi delle cure · CURA] / CURA 1 — L'OROLOGIO: RITMOWRAP2PI APPROVATA e accesa dal… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z17** | — | Z17 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / A6 nell'inerzia e' garantito dall'ORDINE, non dalla… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z18** | — | Z18 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / LO SFASAMENTO eta: per mesi il nodo appena nato ha pesato 2e-4… | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `SI` | **Z21** | — | Z21 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / SPINFEEDBACK con TAUA = 2.0: ESITO MISTO, e non si sceglie… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z23** | — | Z23 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / SPINFEEDBACK NON E' ANTISIMMETRICO: sum(out) != 0, e la… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z24** | — | Z24 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL DENOMINATORE PER GRADO: la misura NON distingue (A) da… | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z26** | — | Z26 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / A QUATTRO SEMI SPINFEEDBACK NON PRODUCE EFFETTO MISURABILE.… | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z3** | — | Z3 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / peq DEGENERE: un fallback a DUE REGIMI, scoperto da un… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z32** | — | Z32 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / Z9 RIMISURATA SUL BLOB ATTUALE: INTATTA (+2.8 %). E il… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z33** | — | Z33 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA MEDIANA IN ritmo() E' ENTRAMBE: normalizzazione… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z34** | — | Z34 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / Z33 MISURATA: NON e' un difetto del GAUGE, e' un difetto di… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z35** | — | Z35 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / NESSUNA delle due vie cura Z33: la (1) E' IL DIFETTO, la (2)… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z37** | — | Z37 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA CUCITURA DELLO SNAPSHOT FALLISCE SU ENTRAMBI I FRONTI, e… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z46** | — | Z46 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL 93 % DEI NODI NON INVECCHIA, SONO SEMPRE GLI STESSI, E… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z48** | — | Z48 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / QUALIFICATA il 2026-09-18: VALE PER IL BATCH. Il «guscio»… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z49** | — | Z49 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL CICLO C'E', MA NON E' NEL CORPO: E' NELLA CODA. E… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z50** | — | Z50 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / QUALIFICATA il 2026-09-18: VALE PER LA REGIONE DENSA. Il… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z52** | — | Z52 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA PREDIZIONE DI LUCA E' SBAGLIATA NELLA SUA FORMA FORTE —… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z57** | — | Z57 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / omegas NON E' UN CRICCHETTO PURO: cresce la CODA, non il… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z60** | — | Z60 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA CRONOLOGIA DELLA DEGENERAZIONE: r NON CRESCE, PARTE… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z66** | — | Z66 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / median(lambdanodi()) SI CONGELA: 0.6092 IDENTICO A QUATTRO… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z87** | — | Z87 DA RIVERIFICARE ⏳[EPOCA 2 · MISURA] / d SCENDE A DIECI VOLTE SOTTO LAM MENTRE SCALAMIN E' ACCESO, E LA… | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z88** | — | Z88 DA RIVERIFICARE ⏳[EPOCA 1 · CODICE] / AVVERTENZA SULL'EPOCA 1: OTTO grandezze che la SEMINA legge sono… | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z90** | — | Z90 DA RIVERIFICARE ⏳[EPOCA 2 · MISURA] / IL RAMO D DIVERGE: nsub = 22591, E IL VINCOLO VINCENTE E' n1 — LA… | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **C20** | — | C20 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / PRIMA MISURA DELLA CONSERVAZIONE DI Ltot =… | `da-decidere` | `misura` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **C22** | — | C22 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA CRESCITA DI Ltot E' L'INERZIA CHE SI ACCENDE, NON UNA… | `da-decidere` | `misura` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **C24** | — | C24 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA CRESCITA DI Ltot STA NELLA CODA, NON NEL NODO TIPICO —… | `da-decidere` | `misura` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Q6** | — | Q6 (1a) / confrontava i valori dopo il passo, quando il rilassamento li ha gia' mossi in entrambi i rami:… | `da-decidere` | `presidio` | `CLAUDE.md` |

---

## FAMIGLIA **B** — TEMPO UNICO   *(9 voci)*

| blocca? | id | alias | che cos'e' | stato | tipo | fonte |
|:--:|---|---|---|:--:|:--:|---|
| `DA-DECIDERE` | **C4-COES-CAUSALE** | C4 | COESCAUSALE — istante unico e cono locale / GLOBALE §2④ / 5/5 (Z98) | `da-decidere` | `cura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **FASCE-TAU** | — | LA CRESCITA E' COORDINATA COL TEMPO PROPRIO? — l'espansione non dev'essere omogenea in senso assoluto, ma… | `da-decidere` | `cura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **G1** | — | §1 QUANTO CONTA IL DISEGNO — Ldisegno/d per arco, per regione, nel tempo, e la correlazione col CENTRO del… | `da-decidere` | `cura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **Z43** | — | Z43 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / APERTA — ED E' UNA DECISIONE SULLA DEFINIZIONE DEL TEMPO,… | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z5** | — | Z5 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / A3 NON E' UN CASO PARTICOLARE DI A2 — risolta una delle… | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z51** | — | Z51 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA Y NON C'E': NE' NEL DENSO, NE' NEL VUOTO, NE' NELLA… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **C12** | — | C12 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / SECONDO CASO DEL PUNTO FISSO AUTO-NORMALIZZANTE. r è… | `da-decidere` | `misura` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **C13** | — | C13 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL TEMPO-LUCE NON E' TESTABILE A QUESTA DENSITA'. cs non e'… | `da-decidere` | `misura` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **C5** | — | C5 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / tauluce = d/cs e' PIATTO ⇒ la sostituzione rompe la… | `da-decidere` | `misura` | `RAMIFICAZIONI.md` |

---

## FAMIGLIA **C** — DOPPIA COPERTURA E CREAZIONE   *(14 voci)*

| blocca? | id | alias | che cos'e' | stato | tipo | fonte |
|:--:|---|---|---|:--:|:--:|---|
| `DA-DECIDERE` | **D35** | — | L'antiparticella di Schwinger nasce con +2π (:5443) e nel campo F = Σ exp(iφ) E' IDENTICA alla particella,… | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **FRAG1** | — | mitosi() SU UNA RETE SENZA CAMPO VA IN IndexError INVECE DI DICHIARARLO. I = self.rhosorgente() è vuoto… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **PASSO-2** | — | UN AVANZAMENTO INCOMPLETO NEL SIMULATORE STESSO, :8404: for in range(300): net.step() nel percorso di… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S06** | — | Il «muro dell'1 %» dell'antifase e' causato da D35: l'antifase «non annichila» perche' +2π letto da exp(iφ)… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S07** | — | dphiarc = angle(exp(1j·Δφ)) (:5894) COLLASSA a 2π una differenza che vive su 4π — e' B3 del mandato /… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S13** | — | IL TEMPO D'ARCO DOVREBBE ESSERE min(ri, rj) INVECE DELLA MEDIA ARITMETICA? — proposta per TUTTO il sistema,… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **PAT-2** | — | spegnigravbifase.py:184 non rispetta il pattern 2 (usa max\/Δ\/ invece delle FIRME) / PATTERN §4 / PRIMA del… | `da-decidere` | `cura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D09** | — | chibasc BLOCCA la mitosi e DIMEZZA l'olonomia netta: fa l'OPPOSTO del suo scopo dichiarato / Z73 / — / APERTO | `aperto` | `difetto` | `STATO_RUN.md` |
| `DA-DECIDERE` | **REG-A** | — | FASE A del registro della fisica: l'INVENTARIO degli scrittori di stato / MANDATO-REGISTRO §2 / FATTA… | `da-decidere` | `difetto` | `STATO_RUN.md` |
| `DA-DECIDERE` | **REG-C** | — | FASE C: LA STORIA di ogni legge, e le schede delle leggi TOLTE / MANDATO-REGISTRO §2 / cio' che non si… | `da-decidere` | `difetto` | `STATO_RUN.md` |
| `DA-DECIDERE` | **REG-R** | — | LA REGOLA MANTENUTA del registro della fisica — la riga in CLAUDE.md («nessuna legge fisica entra, cambia o… | `da-decidere` | `difetto` | `STATO_RUN.md` |
| `DA-DECIDERE` | **Z36** | — | Z36 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / APERTA, MA RI-LETTA il 2026-09-18 (Z37): il 64.7 % e' UN… | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z56** | — | Z56 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / chibasc: NON E' UNA MONOCOLTURA CHE SI RIBALTA — e la… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **C17** | — | C17 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA DISPERSIONE DI r E' RUMORE: la FASE 5 non ha, a oggi,… | `da-decidere` | `misura` | `RAMIFICAZIONI.md` |

---

## FAMIGLIA **D** — SOGLIE TARATE E SOTTO PLANCK   *(5 voci)*

| blocca? | id | alias | che cos'e' | stato | tipo | fonte |
|:--:|---|---|---|:--:|:--:|---|
| `DA-DECIDERE` | **A1-COSTANTI** | A1 | AUDIT DELLE COSTANTI TARATE — 90 commenti «misurato/tarato» nel sorgente. Si separano le COSTANTI TARATE (es.… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **RIPRESA-ARGV** | — | APERTA il 2026-09-26 (limite di un meccanismo che ho costruito io) / LA RIPRESA SI FIDA DEL BLOB, E IL BLOB… | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **C1BIS-ANOM-SIMM** | C1-bis | ANOMSIMM — il pavimento 1e-9 tolto / 21/9 §② / 6/6 (Z99) | `da-decidere` | `cura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **Z64** | — | Z64 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / L'ALGEBRA SU x E' FALSIFICATA (fattore 44 000), f CROLLA… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **C21** | — | C21 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / TRE CRITERI DI SIGILLO SBAGLIATI IN UN GIORNO, tutti scritti dal… | `aperto` | `misura` | `RAMIFICAZIONI.md` |

---

## FAMIGLIA **E** — DISEGNO E STATISTICHE GLOBALI   *(9 voci)*

| blocca? | id | alias | che cos'e' | stato | tipo | fonte |
|:--:|---|---|---|:--:|:--:|---|
| `DA-DECIDERE` | **M1** | — | LA MATERIA È UNO STATO, NON UNA SOSTANZA — e non c'è SCARICO. Nel codice la materia è la condizione I Λ… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **CHK2** | — | CHECKPOINT 2 / GLOBALE §3 / raggiunto e riferito a Luca. IL RUN LUNGO NON SI LANCIA | `da-decidere` | `cura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **CHK3** | — | CHECKPOINT: referto dei quattro esiti, ciascuno contro le sue letture fissate PRIMA / GLOBALE-DISEGNO §5 /… | `da-decidere` | `cura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **E3** | — | EPOCA 3 + RUN LUNGO — tag epoca-3, 3000 passi, M1/M4 leggere durante il run / GLOBALE §4 / 🔒 solo dopo che i… | `da-decidere` | `cura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **G4-MEMARCO** | — | MEMARCO — LA MEMORIA DEL MOTO TRADOTTA IN FORMA RELAZIONALE (aggiunta di Luca al §4, 2026-09-22) /… | `da-decidere` | `cura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D14** | — | median(\/f\/) fa TRE mestieri, non due: e' anche il rompi-anello / Z41 / — / APERTO | `aperto` | `difetto` | `STATO_RUN.md` |
| `DA-DECIDERE` | **Z82** | — | Z82 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / SOSPETTO NON VERIFICATO: n3 normalizza su median(d), e nel… | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **C23** | — | C23 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL FATTORE (CSM/cs)^2 NON E' 1 SULLA CODA a 500 passi. La… | `da-decidere` | `misura` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **P3** | — | NESSUNA STATISTICA SENZA BARRA D'ERRORE, e per confronti fra bracci si usa la | `da-decidere` | `presidio` | `CLAUDE.md` |

---

## FAMIGLIA **F** — FRENO E CONTRAZIONE   *(44 voci)*

| blocca? | id | alias | che cos'e' | stato | tipo | fonte |
|:--:|---|---|---|:--:|:--:|---|
| `DA-DECIDERE` | **A2-DXD** | A2 | RIMISURARE NEL REGIME NUOVO: \/dx\//d del freno-legge (criterio di riapertura: quota 0.5 non nulla) e gli… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **A3-DISEGNO** | A3 | IL DISEGNO ESCE DALLA DINAMICA — cura a sé, prima delle tre prove. pos entra nella fisica in… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D24** | — | A2 e' VIOLATO da Lam = mean(I) -- una media GLOBALE dentro una legge locale -- e la violazione e' la ragione… | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D25** | — | Il gauge del tempo e' la costante 1e-9, e il 93 % dei nodi non invecchia / Z46 — MISURATO IN EPOCA 1, blob… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D28** | — | nsub esplode e lo tira max(/vd/) su POCHISSIMI archi: il costo dell'intero sistema e' governato da una… | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D31** | — | Il freno di SCALAMIN (smpchiudi) E' IL MOTORE della crescita di d0: vale il 117.41 % del Δ, mentre gli… | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D32** | — | I TEMPI PROPRI DICHIARATI SONO TRE, E SONO TRE GRANDEZZE DIVERSE: r, taupp e d/cs. corr(r, taupp) fra -0.25 e… | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D33** | — | La repulsione alla massima compressione e' AZZERATA proprio dove serve: dal 75 % al 96 % degli archi oltre… | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D36** | — | LA SOGLIA DELLA MITOSI E' IN UNITA' ASSOLUTE DI tw, MENTRE LA SCALA DI tw DIPENDE DAL DOMINIO DI phi: le due… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **E4-LAM** | — | LAM FATTO il 2026-09-24 / LA LEGGE «NESSUNA LUNGHEZZA SOTTO LAM» DEVE DIVENTARE STRUTTURALE — sempre accesa,… | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **PASSO-1** | — | IL PASSO NON È step(): SONO CINQUE CHIAMATE, e 24 script sotto csv/ avanzano in modo INCOMPLETO (inventario… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **REPERTI-IMMUTABILI** | — | APERTA il 2026-09-26 (proposta di Luca), famiglia G / UN COMMIT PUO' TOCCARE UN REPERTO GIA' CITATO DA UN… | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S01** | — | Chi fa crescere d0: in G3 gli scrittori sommano -1.6e+03 e med d0 RADDOPPIA lo stesso / il BILANCIO COMPLETO… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S02** | — | Il freno di SCALAMIN e' il motore di d0 / DECISO da Z108: bilancio che CHIUDE a 1.138e-13 su 600 passi, il… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S03** | — | La memoria del moto fa scappare d0 / DECISO da Z109: spegnendola d0 cresce ancora (1.1607), quindi NON e' il… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S05** | — | La compressione d/d0 < 1 e' un difetto e non una fase / G3 dice che peggiora senza gravita' (0.7489→0.6258):… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S09** | — | IL TETTO DI r E' RAGGIUNTO PER UNA VIA CHE NON CONOSCIAMO — lettura di Luca, 2026-09-22: la quota di nodi al… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **C3-SCALA-MIN-PASSO** | C3 | SCALAMINPASSO — il freno una volta per passo / GLOBALE §2③ / 6/6 (Z97) | `da-decidere` | `cura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **C5RES-INVARIANTI** | C5-res | I RESIDUI DI C5 — I4 la scatola nera (rigiocare da solo il passo in cui scatta un invariante), I5 la tabella… | `da-decidere` | `cura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D0** | — | CHI FA SCAPPARE d0 / 21/9 / MISURATO: e' IL FRENO. Gli scrittori spingono giu' -1.543e+05, il vincolo… | `da-decidere` | `cura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **G2** | — | §2 DOVE SPINGE LA GRAVITA' / GLOBALE-DISEGNO §2 / FATTO. Il saldo vive sul CONFINE vuoto-massa (-1.4150/arco,… | `da-decidere` | `cura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **G3** | — | §3 PROVA DI SPEGNIMENTO: la GRAVITA' BIFASE / GLOBALE-DISEGNO §3 / FATTA. sigillo 7/7 · controllo involucro… | `da-decidere` | `cura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **G4** | — | §4 PROVA DI SPEGNIMENTO: la MEMORIA DEL MOTO — flag MEMMOTO / GLOBALE-DISEGNO §4 / FATTO (finito 14:39:27).… | `da-decidere` | `cura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **PROBLEMI-CHK3** | — | IL PIANO DEI PROBLEMI APERTI — per ciascuno: la domanda da chiudere · la misura o derivazione che la chiude ·… | `da-decidere` | `cura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **PROVA-COMB** | — | LA PROVA COMBINATA: TUTTE LE CURE APPROVATE ACCESE INSIEME — 600 passi, stesso seme e scena, letture della… | `da-decidere` | `cura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **SCALE-TW** | — | LE SCALE DELLA TORSIONE: un'analisi completa, DA CAPO / mandato di Luca ricevuto alle 17:44 del 2026-09-22 /… | `da-decidere` | `cura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D01** | — | S09 clippa al passo causale — quindi e' gia' una LUNGHEZZA — e poi moltiplica per median(d0): statistica… | `aperto` | `difetto` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D02** | — | pozzografo calcola L da self.pos — IL DISEGNO — mentre il suo docstring dichiara «la distanza REALE» / G1… | `aperto` | `difetto` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D03** | — | La memoria del moto prende le direzioni da pos, normalizza su Imed GLOBALE, e ha un tetto 0.01median(d0) /… | `da-decidere` | `difetto` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D04** | — | smpchiudi() RISCRIVE tutto d0 a fine passo e NON ha nessun tracciad0 attorno: e' una scrittura invisibile… | `aperto` | `difetto` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D11** | — | d scende DIECI VOLTE sotto LAM mentre SCALAMIN e' acceso, e la causa NON e' trovata / Z87 / — / APERTO | `aperto` | `difetto` | `STATO_RUN.md` |
| `DA-DECIDERE` | **REG-V** | — | verificaregistro.py: completezza, esistenza, coerenza con la traccia di d0 e col registro dei domini di C5 /… | `da-decidere` | `difetto` | `STATO_RUN.md` |
| `DA-DECIDERE` | **X2** | — | X2 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / ZETALOC: «smorzamento locale» che dipende da una statistica… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z104** | — | Z104 APERTA ⏳[EPOCA 3 · DERIVAZIONE] / MEMARCO: LA MEMORIA DEL MOTO TRADOTTA IN FORMA RELAZIONALE — la legge… | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z142** | — | Z142 REPERTO, DIFETTI MIEI ⏳[archivi delle cure · SIGILLO FALLITO] / IL SIGILLO DI E4-LAM FALLISCE 4/5, E I… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z144** | — | Z144 CURA IN CODICE ⏳[archivi delle cure · CURA] / E4-LAM PASSA 6/6: la legge d = LAM si verifica SEMPRE, e… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z148** | — | LA LEGGE d = LAM REGGE PERCHE' UNA CURA E' ACCESA (2026-09-24) | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z39** | — | Z39 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / UN FATTO STABILE DI CLAUDE.md E' CADUTO: cs E' VIVO. csstd/cs =… | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z4** | — | Z4 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / floord0: SOSPESA, e i due rami violano assiomi DIVERSI… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z74** | — | Z74 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / il ramo B rallenta x11: nsub esplode, e lo tira \/vd\/.max()… | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z89** | — | Z89 DA RIVERIFICARE ⏳[EPOCA 1 · CODICE] / 1755 MB DI .pkl NON HANNO IL COMANDO CHE LI RIGENERA, e il… | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **Z92** | — | Z92 🟨LIMITE DICHIARATO ⏳[EPOCA 2 · LETTURA DEL CODICE] / COESADIM legge ISTANTI MISTI, e il suo tetto e'… | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **C18** | — | C18 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL FDT RIFATTO SUL SISTEMA NON CASTRATO (FASE 5 attiva,… | `da-decidere` | `misura` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **R5** | — | contava 25 aperture su 24 passi: l'iniezione del test apriva il freno lei stessa | `da-decidere` | `presidio` | `CLAUDE.md` |

---

## FAMIGLIA **G** — ARRETRATO DEGLI STRUMENTI   *(8 voci)*

| blocca? | id | alias | che cos'e' | stato | tipo | fonte |
|:--:|---|---|---|:--:|:--:|---|
| `DA-DECIDERE` | **A4-METRICHE** | A4 | le METRICHE DEL SETTORE CHIRALE / doc/TASKHISTORY/2026-09-20metriche-settore-chirale.md ( il documento… | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **ANCORE-1** | — | APERTA il 2026-09-25 / 25 SIGILLI PRENDONO «IL CODICE DI PRIMA» DA HEAD (43 occorrenze su 310 file di csv/ —… | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **B6** | — | le due cure OFF: COPPIARECIPROCA e GRAVAMPIEZZA / :739 e :732 (entrambe = False), doc/REFERTOsomme.md, due… | `aperto` | `altro` | `STATO_RUN.md` |
| `NO` | **LETTORI-INDICE** | — | APERTA il 2026-09-26 (PASSO 3 ridotto, decisione di Luca) / SEI LETTORI LEGGONO ANCORA I REGISTRI IN MARKDOWN… | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D13** | — | I sigilli storici non sono stati rigirati sul blob corrente / Z11 / — / APERTO | `aperto` | `difetto` | `STATO_RUN.md` |
| `DA-DECIDERE` | **Z15** | — | Z15 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / 14 .pkl su 36 non portano il BLOB del codice che li ha prodotti, e… | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **P5** | — | OGNI RAMO else / FALLBACK / getattr(..., default) SU UN PERCORSO FISICO VA CONTATO. | `da-decidere` | `presidio` | `CLAUDE.md` |
| `DA-DECIDERE` | **P6** | — | OGNI CSV DI MISURA PORTA BLOB, SEME E TUTTI I FLAG che distinguono quel run dagli altri | `da-decidere` | `presidio` | `CLAUDE.md` |

---

## FAMIGLIA **?** — SENZA FAMIGLIA — da assegnare a mano   *(190 voci)*

| blocca? | id | alias | che cos'e' | stato | tipo | fonte |
|:--:|---|---|---|:--:|:--:|---|
| `DA-DECIDERE` | **A3b** | — | (CITATO 15 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **AAAA-MM-GG** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **ARCHI-PASSO** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **AUTO-ATTENUA** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **AUTO-MANUTENZIONE** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **AUTO-NORMALIZZANTE** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **B7** | — | i reperti DA RIMISURARE sulla scena nuova / Z43, Z46, Z48-Z52, coerg / misurati su sep = 8 / rimisura sulla… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **B9** | — | Z63 / Z64 — i 1455 nodi a 10⁻¹³; la catena f → x → r che non riproduce r / registro, ex-LISTA 2 punto 3 /… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **BACKGROUND-INDEPENDENT** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **BIS-ANOM-SIMM** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **BIS-DELTA** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **COES-CAUSALE** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **CONFIG-1/** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **COSA-RICONTROLLARE** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **CROSS-PASSO** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **CURA1-CORTO** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **CURA2-CORTO** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **CURE-FINE** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **CURE-INIZIO** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **D21** | — | floord0 e' SOSPESA, e i due rami violano assiomi DIVERSI: la scelta non e' stata fatta / Z4 / — / APERTO | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D23** | — | La cucitura dello snapshot FALLISCE su entrambi i fronti, e si DIMOSTRA perche'. NON CABLATA / Z37 / — / APERTO | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D29** | — | CINQUE NODI DI VUOTO sono i piu' connessi dell'intero sistema: il vuoto ha degli HUB, e non dovrebbe averne /… | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D3** | — | (CITATO 7 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **DIFETTI-NUOVI-FINE** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **DIFETTI-NUOVI-INIZIO** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **E1** | — | (CITATO 55 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **E4b** | — | (CITATO 5 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **F1** | — | (CITATO 18 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **F2** | — | (CITATO 16 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **F3** | — | (CITATO 14 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **F4** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **F5** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **FASE-5** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **FASE1** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **FRENO-LEGGE** | — | (CITATO 5 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **G5** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **G6** | — | (CITATO 16 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **G7** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **G8** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **G9** | — | (CITATO 6 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **GLOBALE-DISEGNO** | — | (CITATO 15 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **H1** | — | (CITATO 7 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **H2** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **H3** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **H3b** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **H4** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **H5** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **H6** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **HDF5** | — | (CITATO 8 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **I2** | — | (CITATO 28 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **I3** | — | (CITATO 8 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **I4** | — | (CITATO 12 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **I5** | — | (CITATO 12 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **IC95** | — | (CITATO 80 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **INTERO-BLOCCO** | — | (CITATO 7 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **K1** | — | (CITATO 26 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **K2** | — | (CITATO 19 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **K3** | — | (CITATO 17 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **K4** | — | (CITATO 12 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **K5** | — | (CITATO 12 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **K7** | — | (CITATO 28 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **K8** | — | (CITATO 10 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **L1** | — | (CITATO 9 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **M1b** | — | (CITATO 23 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **M2b** | — | (CITATO 7 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **M3** | — | (CITATO 27 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **M3c** | — | (CITATO 20 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **M4** | — | (CITATO 18 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **MANDATO-PATTERN** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **MANDATO-REGISTRO** | — | (CITATO 12 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **MASSE-COERENTI** | — | (CITATO 6 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **MIT1** | — | (CITATO 6 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **MIT2** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **MODEL-FREE** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **N1** | — | (CITATO 15 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **N1b** | — | (CITATO 8 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **N2** | — | (CITATO 17 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **N3** | — | (CITATO 6 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **N3b** | — | (CITATO 22 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **N6** | — | (CITATO 12 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **N7** | — | (CITATO 13 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **O2** | — | (CITATO 9 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **P1b** | — | (CITATO 7 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **P2b** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **P5a** | — | (CITATO 5 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **P5b** | — | (CITATO 6 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **P7** | — | (CITATO 18 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **P8** | — | (CITATO 20 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **P9** | — | (CITATO 12 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **PEQ-ESATTO** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **PEQ-NASCITA** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **PER-ARCO** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **POST-HOC** | — | (CITATO 5 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **PUNTO-DI-RIPRESA** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Q0** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Q1** | — | (CITATO 13 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Q1a** | — | (CITATO 5 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Q1b** | — | (CITATO 6 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Q2** | — | (CITATO 9 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Q3** | — | (CITATO 9 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Q4** | — | (CITATO 23 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Q5** | — | (CITATO 7 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Q8** | — | (CITATO 13 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **QUADRO-FINE** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **QUADRO-INIZIO** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **QUASI-CANCELLAZIONE** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **R1** | — | (CITATO 30 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **R3b** | — | (CITATO 12 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **R4** | — | (CITATO 13 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **R6** | — | (CITATO 27 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **RAMPA-2/** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **RAMPA2** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **RES-INVARIANTI** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **RI-GIRABILE** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **RI-GIRABILI** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **RI-INTERROGA** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **RI-LETTA** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **ROMPI-ANELLO** | — | (CITATO 8 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **S04** | — | La crescita e' NUCLEAZIONE, non stiramento / CADE con Z108: nascite meno morti valgono lo 0.01 % del Δ… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S1** | — | (CITATO 51 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **S1a** | — | (CITATO 15 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **S1b** | — | (CITATO 19 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **S3** | — | (CITATO 43 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **S3a** | — | (CITATO 5 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **S4a** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **S8** | — | (CITATO 20 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **S8b** | — | (CITATO 6 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **S8c** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **S8d** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **SCALA-MIN-PASSO** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **SIGILLO-CURA2** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **SIGILLO-CURA2-RIPARATO** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **SOTTO-PASSO** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **STANDARD 1** | — | (CITATO 10 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **STANDARD 2** | — | (CITATO 5 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **STANDARD 5** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **STANDARD 7** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **STANDARD 9** | — | (CITATO 10 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **STANDARD ⑤** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **STEP2** | — | (CITATO 66 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **SU2** | — | (CITATO 67 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **T0** | — | (CITATO 32 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **T1** | — | (CITATO 112 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **T1a** | — | (CITATO 19 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **T1b** | — | (CITATO 23 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **T6** | — | (CITATO 32 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **T7** | — | (CITATO 9 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **T9** | — | (CITATO 7 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **TEMPO-LUCE** | — | (CITATO 10 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **TERRA-BUCONERO** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **TRIAGE-FINE** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **TRIAGE-INIZIO** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **U4** | — | (CITATO 5 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **U5** | — | (CITATO 6 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **U6** | — | (CITATO 5 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **U7b** | — | (CITATO 12 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **V10** | — | (CITATO 5 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **V5b** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **V6b** | — | (CITATO 6 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **VUOTO-MASSA** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **W2** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **W4** | — | (CITATO 7 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Y0** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Y10** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Y3** | — | (CITATO 9 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Y4** | — | (CITATO 5 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Y5** | — | (CITATO 64 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Y6** | — | (CITATO 9 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Y7** | — | (CITATO 5 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Y8** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Z128** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Z147** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Z1b** | — | (CITATO 12 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Z1c** | — | (CITATO 30 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Z4a** | — | (CITATO 16 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Z4b** | — | (CITATO 10 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **C5-INVARIANTI** | C5 | INVARIANTI — 42 domini, due livelli / mandato C5 / 3/3 (Z100); accesi di default | `da-decidere` | `cura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D05** | — | I residui di C5: I4 scatola nera, I5 underflow per riga, modalita' fine / il mandato C5 e la coda / — / APERTO | `aperto` | `difetto` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D06** | — | fattcsultimo e' SCRITTO e MAI LETTO (quarto caso della stessa famiglia) / Z7, letto dal codice / — / APERTO | `aperto` | `difetto` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D07** | — | TAUA e' UN SOLO numero per DUE leggi fisiche distinte / Z10, Z9-bis / — / APERTO | `aperto` | `difetto` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D08** | — | Il terzo ramo di calcolapsi (elif sotto REPULSLEGGE) e' DICHIARATO, non corretto / Z14, letto dal codice / —… | `aperto` | `difetto` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D10** | — | nsub governa il costo dell'intero sistema ed e' INVISIBILE: nessun contatore, nessuna colonna / Z75 / — /… | `aperto` | `difetto` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D12** | — | 1755 MB di .pkl non hanno il comando che li rigenera (par.5-quinquies: «un dato che nessuno potra' rifare») /… | `aperto` | `difetto` | `STATO_RUN.md` |
| `DA-DECIDERE` | **D15** | — | A7: la carica chirale NON si conserva / Z71, letto dal codice / — / APERTO | `aperto` | `difetto` | `STATO_RUN.md` |
| `DA-DECIDERE` | **B7-SHAKE** | B7 | SHAKE 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / shake-then-freeze — la precessione mutua non organizza /… | `da-decidere` | `misura` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **P1** | — | NON USARE L'ASSOCIAZIONE SENZA VERIFICARE LO STORICO. | `da-decidere` | `presidio` | `CLAUDE.md` |
| `DA-DECIDERE` | **P2** | — | PRIMA DI ESCLUDERE UN FLAG DA UNA MISURA: FORZA IL SISTEMA O LO CORREGGE? | `da-decidere` | `presidio` | `CLAUDE.md` |
| `DA-DECIDERE` | **P4** | — | PRIMA DI MISURARE SE UNA GRANDEZZA CAMBIA, VERIFICARE CHE SIA LIBERA DI CAMBIARE. | `da-decidere` | `presidio` | `CLAUDE.md` |
| `DA-DECIDERE` | **R3** | — | pretendeva bias == 0.0 esatto e falliva su due ulp di arrotondamento | `da-decidere` | `presidio` | `CLAUDE.md` |
| `DA-DECIDERE` | **U3** | — | confrontava con il mio sviluppo e/2 invece del valore esatto e/(2+e); il numero stampato, 0.952380952, era… | `da-decidere` | `presidio` | `CLAUDE.md` |

---

## 📤 **FUORI LISTA — 405 voci, ciascuna col MOTIVO** *(dai campi dell'indice)*

### motivo: **etichetta LOCALE a una scheda o a un sigillo: il nome pieno include il sigillo, e non e' un fronte del programma**   *(240 voci)*

| id | che cos'e' | tipo |
|---|---|:--:|
| A2b | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| ACCOPPIAMENTO2 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| ALLA-NASCITA | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| ANTI-ALLINEAMENTO | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| AUTO-REFERENZIALE | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| CLI-1) | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| COME-MISURARE | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| COMPONENTI:A1 | A1. STEP2OROLOGIO — aggancio OROLOGIO ↔ METRICA · omegaclk = (cs/CSM)² | `criterio-locale` |
| COMPONENTI:A2 | peq è lo sfondo diffuso locale (Legge I, :265): nessuna statistica globale | `criterio-locale` |
| COMPONENTI:A3 | dopo la proiezione arco→nodo, numeratore e denominatore vivono entrambi sui nodi | `criterio-locale` |
| COMPONENTI:A5 | d/cs è il tempo causale | `criterio-locale` |
| COMPONENTI:A6 | A6 (ragione primaria) / l'inerzia si valuta sullo stato precedente. Una funzione istantanea di… | `criterio-locale` |
| COMPONENTI:A8 | il fallback dello sfondo è contato — e non basta quante volte scatta: si registra quando (Y5) | `criterio-locale` |
| COMPONENTI:B1 | --deparam-orologio / SÌ — «zero parametri» nel suo commento / byte-identità a OFF dichiarata;… | `criterio-locale` |
| COMPONENTI:B10 | --tau-luce / SÌ — d/cs, lo stesso tau già cablato nello Strato 1, coefficiente 1 / NO —… | `criterio-locale` |
| COMPONENTI:B11 | --cs-dinamico / sì (cs = CSM/(1+GAMMA√I), stesso GAMMA di G(rho)) / A/B storico; nessun… | `criterio-locale` |
| COMPONENTI:B2 | --spinore-corretto / sì per costruzione (evaluate-then-commit, \/psi\/=1) / «Default off =… | `criterio-locale` |
| COMPONENTI:B3 | --verlet / è una scelta di integratore, non una legge / «attivare per il confronto A/B» /… | `criterio-locale` |
| COMPONENTI:B4 | --spinore-vivo / sì (reinnesto nell'ordine ETC, zero parametri) / «Reversibile, per A/B;… | `criterio-locale` |
| COMPONENTI:B5 | --chi-core / «nessun segno selezionato a priori» / «default off per A/B» / NON STABILITO. Il… | `criterio-locale` |
| COMPONENTI:B6 | --campo-spinoriale / sì (FASE 1, riduzione al limite esatta) / «Default off = byte-identico»;… | `criterio-locale` |
| COMPONENTI:B7 | --fork-su2 / sì (Berry non normalizzato, il peso cos(chi/2) è ciò che resta non normalizzando)… | `criterio-locale` |
| COMPONENTI:B8 | --fork-su2-mem / sì — tau = d/cs, «nessun numero nuovo, d e cs esistono già» / 23/23 PASS, S7… | `criterio-locale` |
| COMPONENTI:B9 | --step2-orologio / SÌ — orologio di Compton omega ∝ cs²; «fisica NECESSARIA e derivata: zero… | `criterio-locale` |
| COMPONENTI:C1 | --gamma-turbo / dichiarato dal codice stesso: «[DIAGNOSTICO, NON PERCORSO CERTIFICATO]… | `criterio-locale` |
| COMPONENTI:C2 | --kuramoto-su2 / meccanismo di allineamento aggiunto a mano, non derivato. E refutato per… | `criterio-locale` |
| COMPONENTI:C3 | --regime (deterministico, ecc.) / cambia quattro interruttori insieme (TAUA, GPH, CALOREINIT,… | `criterio-locale` |
| COMPONENTI:D1 | csnodoprev esteso alla mitosi — il figlio eredita cs dal padre, come le altre sei cache /… | `criterio-locale` |
| COMPONENTI:D2 | psispinprec esteso alla mitosi — settima voce della stessa convenzione / guardia 4π fallita… | `criterio-locale` |
| COMPONENTI:S1 | FAIL ATTESO — vs blob 2277e9a0, di quattro cambiamenti fa / nodi 3164 contro 2924, 32 shape | `criterio-locale` |
| COMPONENTI:S2 | riduzione al limite sul blob ATTUALE: ON (cs=CSM) vs OFF byte-identico / 0.000e+00 con nodi… | `criterio-locale` |
| COMPONENTI:S3 | S3.0 / IL CONTROLLO POSITIVO: il test VEDE l'effetto / 39/40 nodi con \/f(1)−f(0)\/ 1e-13 | `criterio-locale` |
| COMPONENTI:S3b | l'orologio rallenta dove cs è basso / 0.0100 volte a cs = 0.1·CSM | `criterio-locale` |
| COMPONENTI:S3c | a cs = CSM il fattore è 1 esatto / 1.000000000000000 | `criterio-locale` |
| COMPONENTI:Y0-Y10 | Y10, 11/11 PASS. | `criterio-locale` |
| COMPONENTI:Z30 | Z30: la forma del denominatore — nudo (attuale, zero scelte) contro linea (la meno | `criterio-locale` |
| CURA-3 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| D4 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| D5 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| D6 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| D97 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| DA-DECIDERE | (CITATO 438 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| DE-ACCOPPIABILITA | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| DOMANDE-BUSSOLA | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| DOVE-VA | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| E4a | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| END-TO-END | (CITATO 4 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| ESENTE-P3 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| EVALUATE-THEN-COMMIT | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| F7 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| FASE2 | (CITATO 4 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| FORK-FIRST | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| G0 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| G5b | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| GLOBALE-DIS | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| H6b | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| IN-CHE-ORDINE | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| IN-RUN | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| INERZIA-1( | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| INERZIA-INERZIA | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| J2 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| JHEP04 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| K0 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| K10 | (CITATO 4 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| K11 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| K12 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| K300 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| K6 | (CITATO 9 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| K9 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| L0 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| L10 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| L113 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| L117 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| L184 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| L189 | (CITATO 4 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| L191 | (CITATO 4 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| L203 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| L206 | (CITATO 5 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| L208 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| L212 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| L257 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| L309 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| L311 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| L312 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| L317 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| L323 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| L324 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| L949 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| L982 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| M0 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| M0b | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| M0c | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| M1c | (CITATO 5 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| M3b | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| M5a | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| M5b | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| M5c | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| M8 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| MASSA-VUOTO | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| N4 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| N5 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| N7b | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| N7c | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| N8 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| O1 | (CITATO 12 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| O3 | (CITATO 8 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| O3a | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| O3c | (CITATO 4 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| O4 | (CITATO 7 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| P0 | (CITATO 12 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| P10 | (CITATO 9 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| P11 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| PADRE-FIGLIO | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| PAT-1/PAT-2 | (CITATO 1 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| PCG64 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| Q7 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| QQ777 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| R0 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| R11 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| REGISTRO_FISICA:A1 | flag SPENTO = BYTE-IDENTICO al codice precedente, firma dei byte, un processo per braccio | `criterio-locale` |
| REGISTRO_FISICA:A11 | IL PAVIMENTO 1e-6 | `criterio-locale` |
| REGISTRO_FISICA:A13 | A13 dice che sotto LAM non esiste niente, nemmeno una distanza fra nodi. Quindi la cura | `criterio-locale` |
| REGISTRO_FISICA:A2 | al passo 1, ramp == 1 su TUTTI i nodi della semina iniziale, ESATTO | `criterio-locale` |
| REGISTRO_FISICA:A3 | un nodo nato da MITOSI parte da ramp = 0 e arriva a 1 nel suo tempo-luce | `criterio-locale` |
| REGISTRO_FISICA:A4 | contrasto massa/vuoto e Lam al passo 1, contro P2 = 27 e P3 = 5 | `criterio-locale` |
| REGISTRO_FISICA:A5 | CONTROLLO POSITIVO: ON e OFF DEVONO differire | `criterio-locale` |
| REGISTRO_FISICA:A6 | CASO CHE DEVE FALLIRE: con maturi=False forzato, A2 deve dare FAIL | `criterio-locale` |
| REGISTRO_FISICA:A7 | TAUA non è più letto da pesi — dall'AST, non da un grep | `criterio-locale` |
| REGISTRO_FISICA:C1 | flag spento: byte-identico / par.2.1. L'arresto vive dentro SEMINALAM: a flag spento non esiste | `criterio-locale` |
| REGISTRO_FISICA:C2 | la capienza è INDIPENDENTE da n chiesto (prova del raddoppio) / È IL CRITERIO CHE OGGI… | `criterio-locale` |
| REGISTRO_FISICA:C3 | frazione di impacchettamento 0.384 NELLA SFERA INTERNA — i nodi a distanza = RCONN dal bordo,… | `criterio-locale` |
| REGISTRO_FISICA:C4 | nessun rifiuto falso: con n sotto la capienza misurata la semina riesce sempre, su quattro… | `criterio-locale` |
| REGISTRO_FISICA:D33 | la repulsione si spegne dove servirebbe. Il segno si inverte oltre 3.5π, ma | `criterio-locale` |
| REGISTRO_FISICA:D35 | l'antifase non è un'antifase. Il campo è F = Σ K·exp(iφ), e | `criterio-locale` |
| REGISTRO_FISICA:D37 | UNA CHIAVE DUPLICATA NEI DOMINI, ed è mia | `criterio-locale` |
| REGISTRO_FISICA:E1a | E1a la mitosi non muore / Luca / gnatimitosi 0 e n cresce / il nullo: se la cura rompesse fm,… | `criterio-locale` |
| REGISTRO_FISICA:E1b | E1b la mitosi non esplode / Luca / n finale < 10× il riferimento, e il run arriva a 600 passi… | `criterio-locale` |
| REGISTRO_FISICA:E1c | E1c il fattore / mio / le nascite salgono di un fattore fra 5× e 100× / DERIVATA dagli archi… | `criterio-locale` |
| REGISTRO_FISICA:E2 | E2 le coppie annichilano / Luca / NON MISURABILE, e si dichiara / vedi il blocco qui sotto | `criterio-locale` |
| REGISTRO_FISICA:E3 | E3 la finestra di D33 / mio / si riporta la popolazione delle due finestre nei due bracci / il… | `criterio-locale` |
| REGISTRO_FISICA:E4 | E4 i diagnostici di fase / mio / max(φ) < 2π nel braccio della cura / la riserva ② di Z120. Il… | `criterio-locale` |
| REGISTRO_FISICA:E4-LAM | LA LEGGE d = LAM SI VERIFICA SEMPRE (decisione di Luca, 2026-09-24) | `criterio-locale` |
| REGISTRO_FISICA:P1 | somma dei pesi per nodo / 50 / 9 / 0.18 | `criterio-locale` |
| REGISTRO_FISICA:P2 | contrasto Imassa / Ivuoto / 13 / 27 / 2.1 | `criterio-locale` |
| REGISTRO_FISICA:P3 | Λ / 140 / 5 / 0.036 | `criterio-locale` |
| REGISTRO_FISICA:P3b | ampiezza dello scuotimento / — / 5× più bassa / 0.2 | `criterio-locale` |
| REGISTRO_FISICA:P4 | csfloor dentro le masse / 0.9 / 0.55 / 0.61 | `criterio-locale` |
| REGISTRO_FISICA:P5 | lambdanodi / — / quasi COSTANTE, 0.74-0.76 LAM ovunque / — | `criterio-locale` |
| REGISTRO_FISICA:REG-R | R, la regola mantenuta (da cablare quando le schede coprono le leggi attive): nessuna | `criterio-locale` |
| REGISTRO_FISICA:S1 | flag SPENTO = byte-identico: firma dei byte su tutti i campi, un processo per braccio /… | `criterio-locale` |
| REGISTRO_FISICA:S10 | le regioni restano coerenti: frazione di nodi della coorte con I Λ, ai passi 0, 30, 60, 120 /… | `criterio-locale` |
| REGISTRO_FISICA:S2 | passo ZERO: min distanza fra POSIZIONI = LAM (cKDTree, k=2) / è A13 misurato direttamente, e è… | `criterio-locale` |
| REGISTRO_FISICA:S3 | passo ZERO: sum(d < LAM) == 0 E sum(d == LAM) == 0 / i due INSIEME: il primo da solo lo… | `criterio-locale` |
| REGISTRO_FISICA:S4 | gsmnascite == 0 al passo zero / il presidio non deve scattare. Rileva solo il passo zero, non… | `criterio-locale` |
| REGISTRO_FISICA:S5 | nodi isolati == 0 / un nodo isolato non è un nodo più semplice: è un nodo che esce dalla fisica | `criterio-locale` |
| REGISTRO_FISICA:S6 | d == /posi − posj/ per OGNI arco al passo zero / dice se la cura ha curato D02 a questo sito:… | `criterio-locale` |
| REGISTRO_FISICA:S7 | giro corto di 120 passi: la mitosi viva, il bilancio di d0 CHIUDE / E1a e B, gli stessi di… | `criterio-locale` |
| REGISTRO_FISICA:S9 | al passo ZERO: intensità media DENTRO le regioni / quella del vuoto, 1 — e si riporta il… | `criterio-locale` |
| REGISTRO_FISICA:SCENA-1 | 1, STRADA (1): IL VUOTO DI DEFAULT E' LA SATURAZIONE, E SEMINALAM E' OBBLIGATORIA (Luca,… | `criterio-locale` |
| REGISTRO_FISICA:T2 | -0.15 … +0.44 / fa cio' che la geometria impone | `criterio-locale` |
| REGISTRO_FISICA:T3 | un arco sotto LAM a flag SPENTI FERMA il run / quello che prima non faceva | `criterio-locale` |
| REGISTRO_FISICA:T4 | e con d = LAM non si ferma / il controllo che rende T3 leggibile: senza, T3 passerebbe anche… | `criterio-locale` |
| REGISTRO_FISICA:T5 | byte-inerte: 206 campi identici, 0 diversi contro cura1corto / l'invariante legge soltanto | `criterio-locale` |
| REGISTRO_FISICA:U2 | U2 È ATTIVA IN ENTRAMBI I BRACCI DI P-GONFIA E FABBRICA LUNGHEZZA (Luca, 2026-09-25) | `criterio-locale` |
| REGISTRO_FISICA:U2-5 | 5 è MODEL-FREE: non confronta col mio conto, legge d e d0 e conta gli archi che | `criterio-locale` |
| REGISTRO_FISICA:U2-6 | 6 È IL CASO CHE DEVE FALLIRE (P1-sexies, ed è il criterio più importante): la | `criterio-locale` |
| REGISTRO_FISICA:U2a | la LUNGHEZZA FABBRICATA da nasce, sum(LAM - v) sugli archi troncati, SEPARATA per grandezza… | `criterio-locale` |
| REGISTRO_FISICA:U2b | quanti archi sono stati troncati, e su quanti visti — stessa separazione / idem | `criterio-locale` |
| REGISTRO_FISICA:U2c | frazione di archi sotto 2 LAM / ai passi 0 e 120 | `criterio-locale` |
| REGISTRO_FISICA:V1 | quanto vale a, il passo tipico di rumore, misurato / è il numero che decide la condizione a <… | `criterio-locale` |
| REGISTRO_FISICA:V2 | la deriva di oggi sotto rumore simmetrico / deve riprodurre Z113: ≈ +1.582e-03 con i suoi… | `criterio-locale` |
| REGISTRO_FISICA:V3 | la deriva della proposta, stessa a, stessi d / deve essere del secondo ordine: raddoppiando a… | `criterio-locale` |
| REGISTRO_FISICA:V4 | la deriva della proposta al confine (d → LAM) / → 0, mentre quella di oggi → a/2 | `criterio-locale` |
| REGISTRO_FISICA:V5 | la deriva della proposta lontano / decade come 1/d in assoluto, 1/d² in relativo | `criterio-locale` |
| REGISTRO_FISICA:V6 | il caso che DEVE fallire: la forma exp(dx/u) / deve esplodere vicino al confine, e il test lo… | `criterio-locale` |
| REGISTRO_FISICA:V7 | mai sotto LAM: una discesa enorme, dx = −100·d / oggi attraversa; la proposta no, per… | `criterio-locale` |
| REGISTRO_FISICA:V8 | la DISTRIBUZIONE di \/dx\//d, non solo il suo tipico / è il numero che decide fra piana e Itô:… | `criterio-locale` |
| REGISTRO_FISICA:V9 | quante scritture hanno \/dx\//d 1, e quante 2 / 1: Itô comprime; 2: Itô inverte il verso. Se… | `criterio-locale` |
| RI-ANCORATA | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| RI-ETICHETTATO | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| RI-GIRABILIT | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| RI-GIRABILITA | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| RI-LETTO | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| RI-MISURA | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| RI-SCRIVA | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| RI-VERIFICARE | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| RI-VERIFICATI | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| RIDUZIONE-AL-LIMITE | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| RITMOWRAP2 | (CITATO 4 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| S0 | (CITATO 6 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| S1c | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| S1d | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| S1e | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| S2b | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| S6b | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| S6c | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| S7b | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| S7c | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| S7d | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| SCALE-FREE | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| SHAKE-THEN-FREEZE | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| SOVRA-CORREGGE | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| STANDARD 3 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| T8 | (CITATO 4 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| TS-1 | (CITATO 5 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| TS-2 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| TS-3 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| TS-4 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| TS-5 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| TS-6 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| TW-1 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| TW-2 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| TW-3 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| TW-4 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| TW-5 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| TW-6 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| U7 | (CITATO 10 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| U7a | (CITATO 8 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| V0 | (CITATO 7 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| V1b | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| VALORE-NULL | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| VERIFICATA-SP | (CITATO 1 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| W1 | (CITATO 8 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| W3 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| X0 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| X4 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| X5 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| X6 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| X7 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| Y5a | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| Y5b | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| Y5c | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| Z0 | (CITATO 10 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| Z146 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| Z2b | (CITATO 5 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| Z4c | (CITATO 4 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| Z4d | (CITATO 4 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| Z888 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| ZZ888 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| ZZ999 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |

### motivo: **gia' curata o chiusa**   *(135 voci)*

| id | che cos'e' | tipo |
|---|---|:--:|
| A1-INERZIA | INERZIA VALE SEMPRE ⏳[EPOCA 1 · CODICE] / Teorema di inerzia — lo Strato 0 e' inerte: la… | `misura` |
| A1-TREVIE | la catena a TRE VIE di step — if CHICORE… / elif VERSOCHI… / elif not(…) / :3623 · :3626 ·… | `altro` |
| A2-ANELLO | l'anello A6 di Z70 — periodo 2, via chiralitacorelocale/CHICORE / doc/RAMIFICAZIONI.md Z70 /… | `altro` |
| A2-BLOCH | BLOCH VALE SEMPRE ⏳[EPOCA 1 · CODICE] / Invarianza del Bloch sotto Step 2 — phc e' una fase… | `misura` |
| A3-CHIRALE | Z71 — la carica chirale non si conserva / doc/RAMIFICAZIONI.md Z71 / APERTA. I due punti di… | `altro` |
| A3-FDT | FDT VALE SEMPRE ⏳[EPOCA 1 · CODICE] / FDT del solo scuotimento — il drift di n →… | `misura` |
| A5-PANNELLO | il PANNELLO FEDELE (interpolazione di psi accanto a campospaziale) / la ex-LISTA 3 di questo… | `altro` |
| A6-PERCCHI | percchi FA DUE LAVORI CON REGOLE OPPOSTE: chibasc lo tratta da CHIRALITA', TEMPOSEGNO da… | `altro` |
| B1 | Z47 — pos nella fisica: l'ultimo SFONDO / doc/RAMIFICAZIONI.md Z47, doc/ASSIOMI.md / NON… | `altro` |
| B10 | --override-blob e la COPIA del driver / csv/testfork/scenavideoripresa.py (e68bb8c5, 17466… | `altro` |
| B2 | Z31 — i sigilli non ri-girabili / Z31, citata in 17 file / rifatta TRE volte, l'ultima ieri /… | `altro` |
| B3 | i rami di memoriahebbianamoto / solitonsimulator.py:4616-4918 / mai guardati / sono 25, non 23… | `altro` |
| B4 | i np.zeros / tutto il simulatore / mai guardati / sono 116, non 10. Il numero utile non è… | `altro` |
| B4-FROZEN | FROZEN VALE SEMPRE ⏳[EPOCA 1 · CODICE] / Bloch frozen-o-noise / senza scuotimento \/<n\/ =… | `misura` |
| B5 | theta / l'aliasing del settore di spin / CLAUDE.md §9, registro C14, fronte A / aperto e noto:… | `altro` |
| B5-KURAMOTO | KURAMOTO VALE SEMPRE ⏳[EPOCA 1 · CODICE] / Kuramoto refutato / K-frozen byte-identico a OFF;… | `misura` |
| B6-TURBO | TURBO VALE SEMPRE ⏳[EPOCA 1 · MISURA] / Esito B del turbo — con cs al 5 % di CSM lo Step 2 non… | `misura` |
| B8 | IL BLOCCO DEL RUN A 6000 AL PASSO 2700 / doc/REFERTObloccorun6000.md (131 righe),… | `altro` |
| C1 | C1 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / ESITO (I): nessun bug. omega = coppia/inerzia porta… | `misura` |
| C10 | C10 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / LA BARRA D'ERRORE USATA FINORA E' TRE VOLTE TROPPO… | `misura` |
| C11 | C11 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / psispinprec non era esteso alla mitosi ⇒ la guardia… | `misura` |
| C14 | C14 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / ESITO (A) sui QUATTRO BRACCI — nessuna firma emerge… | `misura` |
| C15 | C15 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / La firma di /<n/ che «pendeva» È CHIUSA come rumore.… | `misura` |
| C16 | C16 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / ESITO (I) CONFERMATO QUATTRO VOLTE, con la barra giusta.… | `misura` |
| C19 | C19 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / CHIUSO il 2026-09-16: le due convenzioni di theta ora… | `misura` |
| C2 | C2 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / Il −1 e' cancellato da √tau, con tau ∝ rho^1.81 / +1.176… | `misura` |
| C25 | C25 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / UN FILE NON SI PUO' COMMITTARE PER IL SUO ESSERE CRLF:… | `misura` |
| C26 | C26 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / VERSOCHI E' UN NO-OP SILENZIOSO SOTTO CHICORE, che e'… | `misura` |
| C27 | C27 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / TRE FLAG VIVONO DENTRO if VIRIALE: E NON LO DICHIARANO.… | `misura` |
| C28 | C28 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / 14 FLAG SU 16 NON HANNO ALCUN SIGILLO. Tier 2 (metrica)… | `misura` |
| C3 | C3 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / Il residuo di 0.34 e' TRANSITORIO, non un termine… | `misura` |
| C4 | C4 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / inerzia = T² — chiude il buco dimensionale; esponente… | `misura` |
| C6 | C6 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / Il rumore non guida omega / Rstoc = 0.041, sotto l'errore… | `misura` |
| C7 | C7 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / La cache csnodoprev veniva scartata a ogni mitosi ⇒ nel… | `misura` |
| C8 | C8 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / LA FASE 2 NON SI CHIUDE. Col tempo-luce cablato la… | `misura` |
| C9 | C9 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / --tau-luce ha un effetto GRANDE sulla pendenza (che pero'… | `misura` |
| CHK3-D | Nel referto del CHK3, la sezione «I DIFETTI NUOVI CONTRO LE MISURE GIA' FATTE» — D27 (quattro… | `cura` |
| D16 | SCALAMIN frenava OGNI scrittura separatamente: il risultato dipendeva dall'ORDINE delle leggi… | `difetto` |
| D17 | peq diventava NEGATIVO e il pavimento max(peq, 1e-9) NE RIBALTAVA IL SEGNO (da -3.72 a… | `difetto` |
| D18 | COESADIM leggeva ISTANTI MISTI e il suo tetto era GLOBALE / Z92 · A5 / COESCAUSALE (C4) / CURATO | `difetto` |
| D19 | OTTO grandezze che la semina legge erano INERTI SUL VUOTO in ogni run di epoca 1 / Z88 / la… | `difetto` |
| D22 | Il DENOMINATORE PER GRADO: la misura non distingue (A) da (B), ma (B) cade per DIMOSTRAZIONE,… | `altro` |
| D34 | D34 CURATO IN CODICE il 2026-09-24 / Il wrap «a 4π» di ritmo() (:2584-2585) NON AVVOLGE: su… | `altro` |
| D37 | D37 CURATO il 2026-09-24 / CHIAVE DUPLICATA NEI DOMINI: 'csnodoprev' compare DUE VOLTE (:226 e… | `altro` |
| INERZIA-1(C) | 1(C) — CURATA e SIGILLATA 3/6 il 2026-09-25: GIUSTA e INSUFFICIENTE / LA CURA TOGLIE… | `altro` |
| OKN-ASSERT | CHIUSA il 2026-09-26, a run finito (residuo rilevato da Luca) / UN getattr(..., default) CHE… | `altro` |
| P1BIS-DELTA | in coda per la LISTA CHIUSA, famiglia G (ordine di Luca, 2026-09-25) / P1-bis VERIFICA LA… | `altro` |
| RAMPA-1 | CHIUSA il 2026-09-25, strada (3) (decisione di Luca): sigillo 9/9 dal CLI, ramp =… | `altro` |
| RIPIEGO-1 | APERTA E CHIUSA il 2026-09-25 (difetto mio, rilevato da LUCA) / UN RIPIEGO GLOBALE SU UNA… | `altro` |
| SCENA-1 | CHIUSA il 2026-09-25, strada (1) (decisione di Luca) / SEMINALAM era approvata ma… | `altro` |
| X1 | X1 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / TEMPOPROPRIOORIENTATO: il principio e' giusto, ma dtn < 0… | `fronte` |
| X3 | X3 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / AUDIT DI LETTURA DELLE LEGGI — registrato (2026-09-16) /… | `fronte` |
| Y2 | Y2 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / Due osservabili U(1) hanno il nullo SBAGLIATO o NON… | `fronte` |
| Z10 | Z10 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / TAUA E' UN SOLO NUMERO PER DUE LEGGI FISICHE DISTINTE —… | `fronte` |
| Z100 | Z100 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / INVARIANTI (C5): il programma si ferma quando una… | `fronte` |
| Z101 | Z101 APERTA ⏳[EPOCA 3 · MISURA] / VALIDAZIONE A 600 PASSI: 6 criteri su 8 REGGONO.… | `fronte` |
| Z102 | Z102 CHIUSA PER MISURA ⏳[EPOCA 3 · MISURA] / CHI FA SCAPPARE d0: E' IL FRENO DELLA SCALA… | `fronte` |
| Z103 | Z103 CHIUSA PER MISURA ⏳[EPOCA 3 · MISURA] / IL POZZO GRAVITAZIONALE USA IL DISEGNO, E IL SUO… | `fronte` |
| Z105 | Z105 CHIUSA PER MISURA ⏳[EPOCA 3 · MISURA] / DOVE SPINGE LA GRAVITA': TUTTO IL SALDO NETTO DI… | `fronte` |
| Z106 | Z106 CHIUSA PER MISURA ⏳[EPOCA 3 · MISURA] / GLI ARCHI PIU' SPINTI DA S09 NON SONO UNA CODA:… | `fronte` |
| Z107 | Z107 CHIUSA PER MISURA ⏳[EPOCA 3 · MISURA] / LA GRAVITA' NON E' IL MOTORE DELLA FUGA DI d0:… | `fronte` |
| Z108 | Z108 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / IL BILANCIO DI d0 CHIUDE, E IL MOTORE… | `fronte` |
| Z109 | Z109 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / LA MEMORIA DEL MOTO NON E' IL MOTORE… | `fronte` |
| Z11 | Z11 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / RIGIRO DEI SIGILLI STORICI — lavoro PREVISTO, non ancora… | `fronte` |
| Z110 | Z110 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / r E taupp SONO DUE GRANDEZZE DIVERSE… | `fronte` |
| Z111 | Z111 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / LA REPULSIONE ALLA MASSIMA… | `fronte` |
| Z112 | Z112 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / L'IPOTESI DELLA COMPRESSIONE REGGE… | `fronte` |
| Z113 | Z113 CHIUSA PER DIMOSTRAZIONE + MISURA / IL CRICCHETTO DEL FRENO E' CONFERMATO SU RUMORE… | `fronte` |
| Z114 | Z114 CHIUSA PER DIMOSTRAZIONE / GLI SCRITTORI DI d0 NON TRACCIATI SONO DUE, NON TRE: init… | `fronte` |
| Z115 | Z115 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / G4-bis: SPEGNERE L'INTERO BLOCCO FA… | `fronte` |
| Z116 | Z116 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / I TRE BRACCI: 6/8 · 7/8 · 6/8. E… | `fronte` |
| Z117 | Z117 CHIUSA PER DIMOSTRAZIONE + MISURA / IL WRAP «A 4π» DI ritmo() NON AVVOLGE NIENTE: su… | `fronte` |
| Z118 | Z118 CHIUSA PER DIMOSTRAZIONE / IL CENSIMENTO DELLE FASI: 52 punti, 38 gravi. E IL NUMERO CHE… | `fronte` |
| Z119 | Z119 CHIUSA PER DIMOSTRAZIONE + MISURA / L'ANTIPARTICELLA DI SCHWINGER NASCE CON +2π, E NEL… | `fronte` |
| Z120 | Z120 CHIUSA PER DIMOSTRAZIONE / LA VERIFICA DI B1: NESSUNA RIGA DELLA FISICA DISTINGUE φ DA φ… | `fronte` |
| Z121 | Z121 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / φ NON E' L'AZIMUT DEL VETTORE DI… | `fronte` |
| Z122 | Z122 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / I TEMPI PROPRI DICHIARATI NON SONO… | `fronte` |
| Z123 | Z123 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / LA PROVA DI RITMOWRAP2PI: 6/8 COME… | `fronte` |
| Z124 | Z124 CHIUSA PER MISURA ⏳[archivi delle cure · SIGILLO] / IL SIGILLO DI FASE2PI: 6/6 PASS, e il… | `fronte` |
| Z13 | Z13 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / calcolapsi() ricalcola i pesi in TUTTE le chiamate… | `fronte` |
| Z135 | Z135 CHIUSA PER MISURA ⏳[archivi delle cure · PROVA] / LA PROVA DI CURA 1: la mitosi NON… | `fronte` |
| Z136 | Z136 CHIUSA PER DIMOSTRAZIONE ⏳[archivi delle cure · CONTROLLO DI LUCA] / LE DUE STRADE DELLA… | `fronte` |
| Z14 | Z14 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / IL TERZO RAMO DI calcolapsi (elif sotto REPULSLEGGE):… | `fronte` |
| Z145 | CHIUSO — T5 del sigillo di CURA 2 era invalido: dv 0 letto come effetto (2026-09-24) | `fronte` |
| Z16 | Z16 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / Y5 ROSSO: la causa e' rhosorgente <= 0, NON peq. E… | `fronte` |
| Z19 | Z19 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / QUARTA VOLTA: una grandezza letta in un momento del… | `fronte` |
| Z2 | Z2 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / spinta: A2 e A3 sono stati tolti, A1 NO (2026-09-17) / La… | `fronte` |
| Z20 | Z20 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / UN DRIVER CHE FORZA UN FLAG IN TUTTI I BRACCI RENDE… | `fronte` |
| Z22 | Z22 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / REGOLA 9 — par.5-quinquies ESISTEVA, ed e' stato violato… | `fronte` |
| Z28 | Z28 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / CHIUSA PRIMA DI NASCERE — il limite «serve… | `fronte` |
| Z30 | Z30 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / CHIUSA il 2026-09-18 — INDIFFERENTE, quindi nudo per… | `fronte` |
| Z31 | Z31 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / QUATTRO SIGILLI NON SONO PIU' RI-GIRABILI: il loro… | `fronte` |
| Z38 | Z38 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL §1 DEL MANDATO GAUGE E' CHIUSO: il gauge… | `fronte` |
| Z40 | Z40 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / A2 E' VIOLATO DA Lam = mean(I), E LA VIOLAZIONE E' LA… | `fronte` |
| Z41 | Z41 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / median(/f/) FA TRE MESTIERI, NON DUE: E'… | `fronte` |
| Z42 | Z42 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / CURATO E SIGILLATO 10/10 — L'ANELLO… | `fronte` |
| Z44 | Z44 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / CHIUSA — f = 0 NON E' FISICA: E' IL… | `fronte` |
| Z45 | Z45 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / CHIUSA — L'IPOTESI MATERIA/ANTIMATERIA CADE.… | `fronte` |
| Z47 | Z47 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / PROGETTO DI LUNGO PERIODO — NON INIZIATO. GEOMETRIA… | `fronte` |
| Z53 | Z53 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / LE COORTI SOPRAVVIVEVANO GIA' ALLA MITOSI. NON… | `fronte` |
| Z54 | Z54 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / CHIUSA — L'ARCHIVIO A SERIE: --db-serie +… | `fronte` |
| Z55 | Z55 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / APERTA — PERCHE' NELLA RIGIOCATA LA STRINGA "schwinger"… | `fronte` |
| Z58 | Z58 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / L'IPOTESI DELLA PORTATA CADE — lambdanodi NON… | `fronte` |
| Z59 | Z59 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / L'INERZIA AL PAVIMENTO CRESCE, e il CUMULATO SOTTOSTIMA… | `fronte` |
| Z6 | Z6 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / IL TRANSITORIO DI ACCENSIONE E' UN BLOCCO STRUTTURALE —… | `fronte` |
| Z61 | Z61 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LE DUE FINESTRE A 6 PASSI: ritmo() NON NASCE… | `fronte` |
| Z62 | Z62 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / L'EVENTO DEL PASSO 198 NON E' UN ARTEFATTO… | `fronte` |
| Z63 | Z63 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / NE' REDISTRIBUZIONE NE' RIDUZIONE: IL FONDO… | `fronte` |
| Z65 | Z65 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / NESSUNA DELLE QUATTRO LETTURE: IL GRAFO E' IN… | `fronte` |
| Z67 | Z67 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / scalap CURATA: il punto fisso e' SCIOLTO, e… | `fronte` |
| Z68 | Z68 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / PASSO 2: la diagnosi era SBAGLIATA -- non e' la… | `fronte` |
| Z69 | Z69 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / SEI GUARDIE PROTEGGONO DA UN DIFETTO GIA'… | `fronte` |
| Z7 | Z7 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / fattcsultimo e' SCRITTO e MAI LETTO — quarto caso della… | `fronte` |
| Z70 | Z70 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / L'ANELLO A6 FRA CHIRALITA' E TORSIONE: C'E', MA NON E'… | `fronte` |
| Z71 | Z71 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / A7 -- LA CARICA CHIRALE NON SI CONSERVA, E IL PUNTO E'… | `fronte` |
| Z72 | Z72 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / PHICRIT = 2pi REGGE, e la ragione e'… | `fronte` |
| Z75 | Z75 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / nsub GOVERNA IL COSTO DELL'INTERO SISTEMA ED E'… | `fronte` |
| Z76 | Z76 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / I NATI HANNO GRADO 2 E SONO LA MAGGIORANZA DEL SISTEMA:… | `fronte` |
| Z78 | Z78 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / d0 HA DIECI SCRITTORI E NESSUNO E' CONTATO — e i due… | `fronte` |
| Z79 | Z79 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / d0 NON E' MOSSO DALLA COESIONE: E' MOSSO DAL SUO CLIP —… | `fronte` |
| Z8 | Z8 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / Lo 0.3457 % di nodi ancora al pavimento 1e-6 NON e'… | `fronte` |
| Z80 | Z80 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / IL CLIP DI d0 PROTEGGE, NON PRODUCE: coesionerelazionale… | `fronte` |
| Z81 | Z81 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / IL FRATELLO S09 NON E' DEL TUTTO CAUSALE: clippa a ±c·DT… | `fronte` |
| Z83 | Z83 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / DOMANDA APERTA: d0 DEVE STARE SOPRA LAM? Il sistema… | `fronte` |
| Z84 | Z84 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / E' cs^2lap CHE ALLUNGA L'ARCO — la TENSIONE DEI VICINI,… | `fronte` |
| Z85 | Z85 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / I LETTORI DI percchi, CENSITI DAL DISCO: la catena della… | `fronte` |
| Z86 | Z86 VALE SEMPRE ⏳[EPOCA 2 · CODICE] / IL CRITERIO Z4a DEL SIGILLO DEL RAMO D ERA SBAGLIATO, E… | `fronte` |
| Z9 | Z9 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / RISCRITTA IL 2026-09-18 — NON «CHIUSA»: RISCRITTA IN… | `fronte` |
| Z93 | Z93 CHIUSA PER MISURA ⏳[EPOCA 2 · MISURA] / L'ARCO DELL'INNESCO E' 2773-4158, NATO-NATO -- ED… | `fronte` |
| Z94 | Z94 CHIUSA PER MISURA ⏳[EPOCA 2 · MISURA] / peq DIVENTA NEGATIVO, E IL PAVIMENTO max(peq,… | `fronte` |
| Z95 | Z95 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / PEQESATTO (C1): il rilassamento di peq in forma… | `fronte` |
| Z96 | Z96 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / PEQNASCITALOCALE (C2): UNA SOLA legge di nascita… | `fronte` |
| Z97 | Z97 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / SCALAMINPASSO (C3): il freno UNA VOLTA PER PASSO.… | `fronte` |
| Z98 | Z98 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / COESCAUSALE (C4): un solo ISTANTE e il CONO DEL… | `fronte` |
| Z99 | Z99 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / ANOMSIMM (C1-bis): il pavimento max(peq, 1e-9) E'… | `fronte` |

### motivo: **assioma: un vincolo sulla forma delle leggi, non una voce da curare**   *(16 voci)*

| id | che cos'e' | tipo |
|---|---|:--:|
| A1 | LA LEGGE, NON IL NUMERO | `assioma` |
| A10 | UNA SOLA GRANDEZZA PUO' LEGARE DUE DOMINI | `assioma` |
| A11 | UN LIMITE E' UNA LEGGE, NON UNA TOPPA | `assioma` |
| A12 | UN DIFETTO DIMOSTRATO SI CURA. MISURARE NON È CURARE. | `assioma` |
| A13 | LAM È LA SCALA DI PLANCK DEL SISTEMA (decisione di Luca, 2026-09-24) | `assioma` |
| A2 | NESSUNA SCORCIATOIA GLOBALE | `assioma` |
| A3 | NIENTE SI NORMALIZZA SUL PROPRIO INSIEME | `assioma` |
| A3c | un RAPPORTO confrontato con un MASSIMO / (115, accanto a due massimi di passi diversi) /… | `assioma` |
| A4 | STRATIFICAZIONE CAUSALE | `assioma` |
| A5 | CAUSALITA' DELLA MEDIAZIONE | `assioma` |
| A6 | INERZIA (TEOREMA, non assioma) | `assioma` |
| A7 | CONSERVAZIONE E STATO | `assioma` |
| A7b | COROLLARIO: uno stato non nasce indefinito (aggiunto 2026-09-17) | `assioma` |
| A8 | UN RAMO SILENZIOSO NON E' UN RAMO | `assioma` |
| A8b | COROLLARIO: le cache CROSS-PASSO | `assioma` |
| A9 | UN PRESIDIO CHE NON IMPEDISCE NON E' UN PRESIDIO | `assioma` |

### motivo: **non e' un difetto**   *(13 voci)*

| id | che cos'e' | tipo |
|---|---|:--:|
| COPPIA-RAMP | APERTA il 2026-09-26 / PERCHE' LA COPPIA NON PORTA ramp? Misurato sui figli (2 semi, media… | `altro` |
| D27 | Il grafo e' in QUATTRO COMPONENTI che non si toccano mai / Z65, misurato in ORIGINE su un… | `altro` |
| NODI-1 | RITIRATA (Luca, 2026-09-25). NON cancellata: resta come storia, col motivo. PERCHE' È CADUTA,… | `altro` |
| POTENZE-1 | CHIUSA il 2026-09-26 con la CURA A (rhos/W^2), sigillo 6/6: F2 da x47 000 a x1.4, F1 2.427… | `altro` |
| S10 | S10 RITIRATA il 2026-09-24 / Il tetto 1.414213 di r viene da un ramo di ritmo() che NON GIRA /… | `altro` |
| S11 | r E' SATURO AL SUO TETTO PER UN TERZO DEI NODI, e la quota CRESCE: 0.76 % - 29.57 % in 600… | `altro` |
| Z130 | Z130 SOSPETTO RITIRATO, MIO ⏳[archivi delle cure · LETTURA] / S10 E' RITIRATA: la premessa era… | `fronte` |
| Z25 | Z25 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / CHIUSA — IL DENOMINATORE PER GRADO ERA UN… | `fronte` |
| Z27 | Z27 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / Z24 MISURATA: i tre punti NON sono lo stesso schema.… | `fronte` |
| Z29 | Z29 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / Z24 CHIUSA — dei tre punti UNO era un cricchetto e… | `fronte` |
| Z73 | Z73 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / chibasc BLOCCA LA MITOSI e DIMEZZA L'OLONOMIA NETTA:… | `fronte` |
| Z77 | Z77 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / LA TENSIONE NASCE DAL DENOMINATORE: d0 CROLLA A SCATTI… | `fronte` |
| Z91 | Z91 APERTA ⏳[EPOCA 2 · LETTURA DEL CODICE] / SCALAMIN FRENA OGNI SCRITTURA SEPARATAMENTE,… | `fronte` |

### motivo: **standard di prova: un criterio di metodo, non un fronte**   *(1 voci)*

| id | che cos'e' | tipo |
|---|---|:--:|
| STANDARD 10 | STANDARD 10 — UNA CURA NON AUMENTA IL NUMERO DELLE LEGGI (criterio di Luca, 2026-09-25) | `standard` |

---

## ⚠ **VOCI SENZA ID: LA PERDITA DICHIARATA DI QUESTA VISTA**

**Nell'indice entrano solo le voci CON UN ID.** Queste **non ne hanno**, quindi **non possono
comparire qui** — e lo scrivo **prima** dei numeri, invece di lasciarle sparire:

- **il `tasso di mitosi`** — e' un punto di `COSA NON SO DERIVARE` della scheda ⑨, **una voce di elenco in prosa senza etichetta**. Per comparire le serve un ID in un registro.
- **`CURA 3`** — l'etichetta e' **`CURA 3` con lo SPAZIO**, e uno spazio non fa un identificatore. Basterebbe `CURA-3`: **e' una rinomina, e la decide Luca.**

**E TRE compaiono solo attraverso l'ID che le CONTIENE**, dichiarato nel codice:

- **i 24 script che avanzano con step() da solo** — la tabella dei 24 script **non ha un ID**: la copre `PASSO-1`, il cui titolo li conta
- **la soglia di torsione 3pi** — la riga `soglia0 = 3π` fra i limiti `A11` **non ha un ID**: la copre `D36`, che e' la soglia della mitosi in unita' assolute di `tw` — **copertura per contenuto, non identita'**
- **chi comprime d0** — le sei misure da rifare in configurazione del driver **non hanno un ID ciascuna**: le copre `CONFIG-1`, la voce che le raccoglie

---

## ✅ IL CONTROLLO *(`P1-sexies`)*

Le voci che Luca aveva elencato come mancanti restano il criterio. **Se una non compare, il
generatore NON SCRIVE IL FILE.** E **se l'elenco delle voci PERSE cresce oltre le due
dichiarate, si ferma anche allora**: una perdita nuova non deve passare come le altre.

| deve comparire | trovata? |
|---|:--:|
| SCALE-TW | ✅ |
| B5 — theta / l'aliasing del settore di spin | ✅ |
| cura 5 via CLI (CLI-1) | ✅ |
| D33 | ✅ |
| A3 — il disegno esce dalla dinamica | ✅ |
| PASSO-2 | ✅ |
| FRAG1 | ✅ |
| M1 | ✅ |
| M2 | ✅ |
| i 24 script che avanzano con step() da solo | ✅ |
| \|dx\|/d = V8/V9, che decide il freno | ✅ |
| la soglia di torsione 3pi | ✅ |
| chi comprime d0 | ✅ |
| **voci PERSE dichiarate** | 2 |

## COSA QUESTA BOZZA *NON* DICE

- **`stato` e `famiglia` vengono dall'indice**, e l'indice li ricava dalla fonte con **regole
  dichiarate**: dove la fonte non porta un marcatore, lo stato e' `da-decidere`. **Non e'
  un'incertezza di questa vista: e' un'incertezza dei REGISTRI, resa visibile.**
- **`blocca?` non e' un giudizio mio:** `NO` viene da una **regola** *(un chiuso, un
  non-difetto, una teoria o un criterio-locale non bloccano mai)*, `SI` **solo** dove la fonte
  lo dichiara, e `DA-DECIDERE` e' la **risposta onesta**. La lista su cui decidere e'
  `doc/SMISTAMENTO_run_base.md`.
- **non contiene la DIMENSIONE** ne' l'**ordine per DIPENDENZE**: nessun campo dell'indice li
  porta, e ricavarli sarebbe giudizio mio riga per riga. **Il mandato li chiede: mancano.**
- **una voce che nessun registro DEFINISCE non c'e'**: questa vista non guarda i registri, e
  **non puo' vedere cio' che l'indice non ha**. E' il prezzo di una fonte sola, ed e' il
  rovescio del guadagno.
