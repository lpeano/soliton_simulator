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
voci nell'indice      851
in LISTA              391   (stato aperto o da-decidere, e un tipo che puo' essere un fronte)
FUORI LISTA           460   col motivo, dai campi dell'indice
```

---

## LE SETTE FAMIGLIE

| | famiglia | cosa raccoglie | voci in lista |
|---|---|---|--:|
| **A** | **INERZIA E AVVIO** | l'inerzia spinoriale, il contrasto, `rho_s`, la rampa, cio' che decide come nasce un nodo | 66 |
| **B** | **TEMPO UNICO** | un solo orologio: `dt_n`/`dt_e` contro `DT` nudo, `r`, `tau_pp`, le medie d'arco | 10 |
| **C** | **DOPPIA COPERTURA E CREAZIONE** | la fase su `2pi`/`4pi`, la torsione `tw`, la mitosi, Schwinger, cio' che si eredita | 16 |
| **D** | **SOGLIE TARATE E SOTTO PLANCK** | `A11`: ogni clip, pavimento o tetto che non esprima un vincolo dichiarato | 7 |
| **E** | **DISEGNO E STATISTICHE GLOBALI** | `A2`/`A5`: mediane e medie globali dentro una legge locale, e il disegno nella fisica | 9 |
| **F** | **FRENO E CONTRAZIONE** | `SCALA_MIN`, il freno a senso unico, la coesione, la repulsione, `d0`, `LAM` | 41 |
| **G** | **ARRETRATO DEGLI STRUMENTI** | presidi, ancore, reperti, ripresa, il passo incompleto: **non e' fisica** | 7 |
| **?** | **SENZA FAMIGLIA** | nessuna regola dell'indice ha deciso: **le elenco invece di metterle in una famiglia a caso** | 235 |

---

## FAMIGLIA **A** — INERZIA E AVVIO   *(66 voci)*

| blocca? | id | alias | che cos'e' | stato | tipo | fonte |
|:--:|---|---|---|:--:|:--:|---|
| `DA-DECIDERE` | **CONFIG-1** | — | APERTA il 2026-09-25 / LE SEI MISURE DI OGGI GIRAVANO CON 28 LEGGI SU 31 SPENTE, misurato… | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **I1** | — | IDEA DI LUCA, per dopo: costruire UNA massa, farla maturare, leggerne la struttura sul grafo e... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **INERZIA-1** | — | LA LEGGE DELL'INERZIA CEDE A k = 2, ED È UN DIFETTO DIMOSTRATO (misura 3, f8b27d9): coppia... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **M2** | — | LA MITOSI — DUE DIFETTI DA ACCLARARE. ① il figlio nasce nel PUNTO MEDIO: posfiglio = 0.5... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S08** | — | Se φ non e' l'azimut del Bloch, CHE COS'E'? / Z121 ha refutato la frase del docstring (R ≤ 0.18... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S12** | — | S12 APPROVATO DA LUCA il 2026-09-24 / IL RILASSAMENTO DI rep DENTRO mitosi() (:5280) E' UN... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **U2** | — | M2 DIVENTA URGENTE — la mitosi mette figli SOTTO la scala di Planck. Con la semina nuova gli... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `NO` | **C1-PEQ-ESATTO** | C1 | PEQESATTO — rilassamento in forma esatta / GLOBALE §2① / 7/7 (Z95) | `da-decidere` | `cura` | `STATO_RUN.md` |
| `NO` | **C2-PEQ-NASCITA** | C2 | PEQNASCITALOCALE — nascita locale di peq / GLOBALE §2② / 6/6 (Z96) | `da-decidere` | `cura` | `STATO_RUN.md` |
| `SI` | **CLI-1** | — | I SIGILLI DI CURA 4 E CURA 5 NON HANNO MAI PROVATO IL PERCORSO CLI: impostavano S.SEMINAMATURA =... | `da-decidere` | `cura` | `STATO_RUN.md` |
| `NO` | **PAT-1** | — | dovespingelagravita.py non rispetta il pattern 5 (nessun CONTROLLO DELL'INVOLUCRO) / PATTERN §4... | `da-decidere` | `cura` | `STATO_RUN.md` |
| `NO` | **D20** | — | La correzione (1) su inerzia NON e' stata cablata, e il gate che la autorizzava aveva misurato... | `aperto` | `difetto` | `STATO_RUN.md` |
| `NO` | **D26** | — | Le coorti non sopravvivevano allo SNAPSHOT: dopo un salva/ricarica il lignaggio ripartiva VUOTO... | `da-decidere` | `difetto` | `STATO_RUN.md` |
| `NO` | **D30** | — | massa chiama semina SENZA massid (:6209), quindi masseinfo non viene MAI popolato e... | `aperto` | `difetto` | `STATO_RUN.md` |
| `NO` | **D38** | — | nasce (:3850) e' gated su SCALAMIN or SCALAMINPASSO: la legge «nessun arco sotto LAM» e'... | `aperto` | `difetto` | `STATO_RUN.md` |
| `NO` | **RAMPA-2** | — | APERTA il 2026-09-25 (richiesta di Luca) / AL PASSO 0 TUTTI LEGGONO cs = CSM. La cache... | `aperto` | `difetto` | `STATO_RUN.md` |
| `NO` | **REG-B** | — | FASE B: le SCHEDE, a lotti, un commit per lotto / MANDATO-REGISTRO §2 / LE QUATTRO DELL'ORDINE... | `da-decidere` | `difetto` | `STATO_RUN.md` |
| `SI` | **U1** | — | URGENTE, PRIMA DI QUALUNQUE GIRO LUNGO — massacriticacollasso: 21 usi DENTRO LEGGI FISICHE... | `da-decidere` | `difetto` | `STATO_RUN.md` |
| `NO` | **R2** | — | R2 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / NUOVO: il residuo della catena theta = sigma +... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **S2** | — | S2 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / NON SI RIPRODUCE sul sistema corretto, E CAMBIA... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Y1** | — | Y1 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / Il settore U(1) non ha un'osservabile dell'OROLOGIO /... | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z1** | — | Z1 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / inerzia: la correzione (1) NON e' stata cablata... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z101** | — | Z101 APERTA ⏳[EPOCA 3 · MISURA] / VALIDAZIONE A 600 PASSI: 6 criteri su 8 REGGONO. L'ESPLOSIONE... | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z12** | — | Z12 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / pesi() gira SEDICI volte per passo, a cavallo... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z125** | — | Z125 DIFETTO DI METODO, MIO ⏳[archivi delle cure · LETTURA] / IL §E NON ESISTE NEL REPO OLTRE E1... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z127** | — | Z127 LA LETTURA CADE ⏳[archivi delle cure · PROVA] / E1 NON PASSA: CON FASE2PI LA GENERAZIONE DI... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z13** | — | Z13 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / calcolapsi() ricalcola i pesi in TUTTE le chiamate... | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z17** | — | Z17 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / A6 nell'inerzia e' garantito dall'ORDINE, non... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z18** | — | Z18 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / LO SFASAMENTO eta: per mesi il nodo appena nato ha... | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z21** | — | Z21 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / SPINFEEDBACK con TAUA = 2.0: ESITO MISTO, e non... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z23** | — | Z23 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / SPINFEEDBACK NON E' ANTISIMMETRICO: sum(out) !=... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z24** | — | Z24 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL DENOMINATORE PER GRADO: la misura NON... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z26** | — | Z26 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / A QUATTRO SEMI SPINFEEDBACK NON PRODUCE EFFETTO... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z27** | — | Z27 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / Z24 MISURATA: i tre punti NON sono lo stesso schema.... | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z29** | — | Z29 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / Z24 CHIUSA — dei tre punti UNO era un cricchetto e ora... | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z3** | — | Z3 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / peq DEGENERE: un fallback a DUE REGIMI, scoperto... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z30** | — | Z30 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / CHIUSA il 2026-09-18 — INDIFFERENTE, quindi nudo per... | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z32** | — | Z32 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / Z9 RIMISURATA SUL BLOB ATTUALE: INTATTA (+2.8... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z33** | — | Z33 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA MEDIANA IN ritmo() E' ENTRAMBE: normalizzazione… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z34** | — | Z34 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / Z33 MISURATA: NON e' un difetto del GAUGE, e'... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z35** | — | Z35 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / NESSUNA delle due vie cura Z33: la (1) E' IL... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z37** | — | Z37 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA CUCITURA DELLO SNAPSHOT FALLISCE SU ENTRAMBI... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z38** | — | Z38 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL §1 DEL MANDATO GAUGE E' CHIUSO: il gauge... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z41** | — | Z41 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / median(/f/) FA TRE MESTIERI, NON DUE: E' ANCHE IL… | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z42** | — | Z42 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / CURATO E SIGILLATO 10/10 — L'ANELLO ISTANTANEO... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z44** | — | Z44 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / CHIUSA — f = 0 NON E' FISICA: E' IL TRANSITORIO... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z45** | — | Z45 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / CHIUSA — L'IPOTESI MATERIA/ANTIMATERIA CADE.... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z46** | — | Z46 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL 93 % DEI NODI NON INVECCHIA, SONO SEMPRE GLI... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z48** | — | Z48 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / QUALIFICATA il 2026-09-18: VALE PER IL BATCH.... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z49** | — | Z49 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL CICLO C'E', MA NON E' NEL CORPO: E' NELLA... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z50** | — | Z50 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / QUALIFICATA il 2026-09-18: VALE PER LA REGIONE... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z52** | — | Z52 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA PREDIZIONE DI LUCA E' SBAGLIATA NELLA SUA... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z53** | — | Z53 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / LE COORTI SOPRAVVIVEVANO GIA' ALLA MITOSI. NON... | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z57** | — | Z57 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / omegas NON E' UN CRICCHETTO PURO: cresce la... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z60** | — | Z60 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA CRONOLOGIA DELLA DEGENERAZIONE: r NON... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z66** | — | Z66 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / median(lambdanodi()) SI CONGELA: 0.6092... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z69** | — | Z69 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / SEI GUARDIE PROTEGGONO DA UN DIFETTO GIA'... | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z87** | — | Z87 DA RIVERIFICARE ⏳[EPOCA 2 · MISURA] / d SCENDE A DIECI VOLTE SOTTO LAM MENTRE SCALAMIN E'... | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z88** | — | Z88 DA RIVERIFICARE ⏳[EPOCA 1 · CODICE] / AVVERTENZA SULL'EPOCA 1: OTTO grandezze che la SEMINA... | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z9** | — | Z9 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / RISCRITTA IL 2026-09-18 — NON «CHIUSA»: RISCRITTA IN... | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z90** | — | Z90 DA RIVERIFICARE ⏳[EPOCA 2 · MISURA] / IL RAMO D DIVERGE: nsub = 22591, E IL VINCOLO VINCENTE... | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **C20** | — | C20 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / PRIMA MISURA DELLA CONSERVAZIONE DI Ltot =… | `da-decidere` | `misura` | `RAMIFICAZIONI.md` |
| `NO` | **C22** | — | C22 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA CRESCITA DI Ltot E' L'INERZIA CHE SI... | `da-decidere` | `misura` | `RAMIFICAZIONI.md` |
| `NO` | **C24** | — | C24 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA CRESCITA DI Ltot STA NELLA CODA, NON NEL... | `da-decidere` | `misura` | `RAMIFICAZIONI.md` |
| `NO` | **OMEGA-ETA** | — | APERTA il 2026-09-26 (Luca: da seguire nel run base, NON una cura) / IL RAPPORTO /omega/... | `aperto` | `misura` | `STATO_RUN.md` |
| `DA-DECIDERE` | **Q6** | — | Q6 (1a) / confrontava i valori dopo il passo, quando il rilassamento li ha gia' mossi in... | `da-decidere` | `presidio` | `CLAUDE.md` |

---

## FAMIGLIA **B** — TEMPO UNICO   *(10 voci)*

| blocca? | id | alias | che cos'e' | stato | tipo | fonte |
|:--:|---|---|---|:--:|:--:|---|
| `NO` | **C4-COES-CAUSALE** | C4 | COESCAUSALE — istante unico e cono locale / GLOBALE §2④ / 5/5 (Z98) | `da-decidere` | `cura` | `STATO_RUN.md` |
| `NO` | **CHK3-D** | — | Nel referto del CHK3, la sezione «I DIFETTI NUOVI CONTRO LE MISURE GIA' FATTE» — D27 (quattro... | `da-decidere` | `cura` | `STATO_RUN.md` |
| `NO` | **FASCE-TAU** | — | LA CRESCITA E' COORDINATA COL TEMPO PROPRIO? — l'espansione non dev'essere omogenea in senso... | `da-decidere` | `cura` | `STATO_RUN.md` |
| `NO` | **G1** | — | §1 QUANTO CONTA IL DISEGNO — Ldisegno/d per arco, per regione, nel tempo, e la correlazione col... | `da-decidere` | `cura` | `STATO_RUN.md` |
| `NO` | **Z43** | — | Z43 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / APERTA — ED E' UNA DECISIONE SULLA DEFINIZIONE... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z5** | — | Z5 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / A3 NON E' UN CASO PARTICOLARE DI A2 — risolta... | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z51** | — | Z51 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA Y NON C'E': NE' NEL DENSO, NE' NEL VUOTO... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **C12** | — | C12 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / SECONDO CASO DEL PUNTO FISSO... | `da-decidere` | `misura` | `RAMIFICAZIONI.md` |
| `NO` | **C13** | — | C13 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL TEMPO-LUCE NON E' TESTABILE A QUESTA... | `da-decidere` | `misura` | `RAMIFICAZIONI.md` |
| `NO` | **C5** | — | C5 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / tauluce = d/cs e' PIATTO ⇒ la sostituzione rompe la… | `da-decidere` | `misura` | `RAMIFICAZIONI.md` |

---

## FAMIGLIA **C** — DOPPIA COPERTURA E CREAZIONE   *(16 voci)*

| blocca? | id | alias | che cos'e' | stato | tipo | fonte |
|:--:|---|---|---|:--:|:--:|---|
| `DA-DECIDERE` | **FRAG1** | — | mitosi() SU UNA RETE SENZA CAMPO VA IN IndexError INVECE DI DICHIARARLO. I = self.rhosorgente()... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **PASSO-2** | — | UN AVANZAMENTO INCOMPLETO NEL SIMULATORE STESSO, :8404: for in range(300): net.step() nel... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S06** | — | Il «muro dell'1 %» dell'antifase e' causato da D35: l'antifase «non annichila» perche' +2π letto... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S07** | — | dphiarc = angle(exp(1j·Δφ)) (:5894) COLLASSA a 2π una differenza che vive su 4π — e' B3 del... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S13** | — | IL TEMPO D'ARCO DOVREBBE ESSERE min(ri, rj) INVECE DELLA MEDIA ARITMETICA? — proposta per TUTTO... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `NO` | **CURA-3** | — | - phi su 2pi con le soglie che la seguono / nella forma decisa: frazioni che sul dominio 4pi danno… | `da-decidere` | `cura` | `STATO_RUN.md` |
| `NO` | **PAT-2** | — | spegnigravbifase.py:184 non rispetta il pattern 2 (usa max\/Δ\/ invece delle FIRME) / PATTERN §4... | `da-decidere` | `cura` | `STATO_RUN.md` |
| `NO` | **D35** | — | L'antiparticella di Schwinger nasce con +2π (:5443) e nel campo F = Σ exp(iφ) E' IDENTICA alla... | `aperto` | `difetto` | `STATO_RUN.md` |
| `NO` | **REG-A** | — | FASE A del registro della fisica: l'INVENTARIO degli scrittori di stato / MANDATO-REGISTRO §2 /... | `da-decidere` | `difetto` | `STATO_RUN.md` |
| `NO` | **REG-C** | — | FASE C: LA STORIA di ogni legge, e le schede delle leggi TOLTE / MANDATO-REGISTRO §2 / cio' che... | `da-decidere` | `difetto` | `STATO_RUN.md` |
| `NO` | **REG-R** | — | LA REGOLA MANTENUTA del registro della fisica — la riga in CLAUDE.md («nessuna legge fisica... | `da-decidere` | `difetto` | `STATO_RUN.md` |
| `NO` | **Z25** | — | Z25 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / CHIUSA — IL DENOMINATORE PER GRADO ERA UN... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z36** | — | Z36 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / APERTA, MA RI-LETTA il 2026-09-18 (Z37): il... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z56** | — | Z56 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / chibasc: NON E' UNA MONOCOLTURA CHE SI RIBALTA... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **C17** | — | C17 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LA DISPERSIONE DI r E' RUMORE: la FASE 5 non... | `da-decidere` | `misura` | `RAMIFICAZIONI.md` |
| `NO` | **MITOSI-TASSO** | — | APERTA il 2026-09-26 (era una voce PERSA: viveva senza ID) / CHE IL TASSO DI MITOSI RESTI DELLO... | `aperto` | `misura` | `STATO_RUN.md` |

---

## FAMIGLIA **D** — SOGLIE TARATE E SOTTO PLANCK   *(7 voci)*

| blocca? | id | alias | che cos'e' | stato | tipo | fonte |
|:--:|---|---|---|:--:|:--:|---|
| `DA-DECIDERE` | **A1-COSTANTI** | A1 | AUDIT DELLE COSTANTI TARATE — 90 commenti «misurato/tarato» nel sorgente. Si separano le... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **RIPRESA-ARGV** | — | APERTA il 2026-09-26 (limite di un meccanismo che ho costruito io) / LA RIPRESA SI FIDA DEL... | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S11** | — | r E' SATURO AL SUO TETTO PER UN TERZO DEI NODI, e la quota CRESCE: 0.76 % - 29.57 % in 600 passi... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `NO` | **C1BIS-ANOM-SIMM** | C1-bis | ANOMSIMM — il pavimento 1e-9 tolto / 21/9 §② / 6/6 (Z99) | `da-decidere` | `cura` | `STATO_RUN.md` |
| `NO` | **Z28** | — | Z28 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / CHIUSA PRIMA DI NASCERE — il limite «serve una... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z64** | — | Z64 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / L'ALGEBRA SU x E' FALSIFICATA (fattore 44 000)... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **C21** | — | C21 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / TRE CRITERI DI SIGILLO SBAGLIATI IN UN GIORNO, tutti... | `aperto` | `misura` | `RAMIFICAZIONI.md` |

---

## FAMIGLIA **E** — DISEGNO E STATISTICHE GLOBALI   *(9 voci)*

| blocca? | id | alias | che cos'e' | stato | tipo | fonte |
|:--:|---|---|---|:--:|:--:|---|
| `DA-DECIDERE` | **M1** | — | LA MATERIA È UNO STATO, NON UNA SOSTANZA — e non c'è SCARICO. Nel codice la materia è la... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `NO` | **CHK2** | — | CHECKPOINT 2 / GLOBALE §3 / raggiunto e riferito a Luca. IL RUN LUNGO NON SI LANCIA | `da-decidere` | `cura` | `STATO_RUN.md` |
| `NO` | **CHK3** | — | CHECKPOINT: referto dei quattro esiti, ciascuno contro le sue letture fissate PRIMA /... | `da-decidere` | `cura` | `STATO_RUN.md` |
| `NO` | **E3** | — | EPOCA 3 + RUN LUNGO — tag epoca-3, 3000 passi, M1/M4 leggere durante il run / GLOBALE §4 / 🔒... | `da-decidere` | `cura` | `STATO_RUN.md` |
| `NO` | **G4-MEMARCO** | — | MEMARCO — LA MEMORIA DEL MOTO TRADOTTA IN FORMA RELAZIONALE (aggiunta di Luca al §4, 2026-09-22) /… | `da-decidere` | `cura` | `STATO_RUN.md` |
| `NO` | **D14** | — | median(\/f\/) fa TRE mestieri, non due: e' anche il rompi-anello / Z41 / — / APERTO | `aperto` | `difetto` | `STATO_RUN.md` |
| `NO` | **Z82** | — | Z82 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / SOSPETTO NON VERIFICATO: n3 normalizza su... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **C23** | — | C23 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL FATTORE (CSM/cs)^2 NON E' 1 SULLA CODA a 500... | `da-decidere` | `misura` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **P3** | — | NESSUNA STATISTICA SENZA BARRA D'ERRORE, e per confronti fra bracci si usa la | `da-decidere` | `presidio` | `CLAUDE.md` |

---

## FAMIGLIA **F** — FRENO E CONTRAZIONE   *(41 voci)*

| blocca? | id | alias | che cos'e' | stato | tipo | fonte |
|:--:|---|---|---|:--:|:--:|---|
| `DA-DECIDERE` | **A2-DXD** | A2 | RIMISURARE NEL REGIME NUOVO: \/dx\//d del freno-legge (criterio di riapertura: quota 0.5 non... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **A3-DISEGNO** | A3 | IL DISEGNO ESCE DALLA DINAMICA — cura a sé, prima delle tre prove. pos entra nella fisica in… | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **E4-LAM** | — | LAM FATTO il 2026-09-24 / LA LEGGE «NESSUNA LUNGHEZZA SOTTO LAM» DEVE DIVENTARE STRUTTURALE —... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **PASSO-1** | — | IL PASSO NON È step(): SONO CINQUE CHIAMATE, e 24 script sotto csv/ avanzano in modo INCOMPLETO... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **REPERTI-IMMUTABILI** | — | APERTA il 2026-09-26 (proposta di Luca), famiglia G / UN COMMIT PUO' TOCCARE UN REPERTO GIA'... | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S01** | — | Chi fa crescere d0: in G3 gli scrittori sommano -1.6e+03 e med d0 RADDOPPIA lo stesso / il... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S02** | — | Il freno di SCALAMIN e' il motore di d0 / DECISO da Z108: bilancio che CHIUDE a 1.138e-13 su 600... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S03** | — | La memoria del moto fa scappare d0 / DECISO da Z109: spegnendola d0 cresce ancora (1.1607)... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S05** | — | La compressione d/d0 < 1 e' un difetto e non una fase / G3 dice che peggiora senza gravita'... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S09** | — | IL TETTO DI r E' RAGGIUNTO PER UNA VIA CHE NON CONOSCIAMO — lettura di Luca, 2026-09-22: la... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `NO` | **C3-SCALA-MIN-PASSO** | C3 | SCALAMINPASSO — il freno una volta per passo / GLOBALE §2③ / 6/6 (Z97) | `da-decidere` | `cura` | `STATO_RUN.md` |
| `NO` | **C5RES-INVARIANTI** | C5-res | I RESIDUI DI C5 — I4 la scatola nera (rigiocare da solo il passo in cui scatta un invariante)... | `da-decidere` | `cura` | `STATO_RUN.md` |
| `NO` | **D0** | — | CHI FA SCAPPARE d0 / 21/9 / MISURATO: e' IL FRENO. Gli scrittori spingono giu' -1.543e+05, il... | `da-decidere` | `cura` | `STATO_RUN.md` |
| `NO` | **G2** | — | §2 DOVE SPINGE LA GRAVITA' / GLOBALE-DISEGNO §2 / FATTO. Il saldo vive sul CONFINE vuoto-massa... | `da-decidere` | `cura` | `STATO_RUN.md` |
| `NO` | **G3** | — | §3 PROVA DI SPEGNIMENTO: la GRAVITA' BIFASE / GLOBALE-DISEGNO §3 / FATTA. sigillo 7/7 ·... | `da-decidere` | `cura` | `STATO_RUN.md` |
| `NO` | **G4** | — | §4 PROVA DI SPEGNIMENTO: la MEMORIA DEL MOTO — flag MEMMOTO / GLOBALE-DISEGNO §4 / FATTO (finito... | `da-decidere` | `cura` | `STATO_RUN.md` |
| `NO` | **PROBLEMI-CHK3** | — | IL PIANO DEI PROBLEMI APERTI — per ciascuno: la domanda da chiudere · la misura o derivazione... | `da-decidere` | `cura` | `STATO_RUN.md` |
| `NO` | **PROVA-COMB** | — | LA PROVA COMBINATA: TUTTE LE CURE APPROVATE ACCESE INSIEME — 600 passi, stesso seme e scena... | `da-decidere` | `cura` | `STATO_RUN.md` |
| `SI` | **SCALE-TW** | — | LE SCALE DELLA TORSIONE: un'analisi completa, DA CAPO / mandato di Luca ricevuto alle 17:44 del... | `da-decidere` | `cura` | `STATO_RUN.md` |
| `NO` | **D01** | — | S09 clippa al passo causale — quindi e' gia' una LUNGHEZZA — e poi moltiplica per median(d0)... | `aperto` | `difetto` | `STATO_RUN.md` |
| `SI` | **D03** | — | La memoria del moto prende le direzioni da pos, normalizza su Imed GLOBALE, e ha un tetto... | `da-decidere` | `difetto` | `STATO_RUN.md` |
| `NO` | **D04** | — | smpchiudi() RISCRIVE tutto d0 a fine passo e NON ha nessun tracciad0 attorno: e' una scrittura... | `aperto` | `difetto` | `STATO_RUN.md` |
| `NO` | **D24** | — | A2 e' VIOLATO da Lam = mean(I) -- una media GLOBALE dentro una legge locale -- e la violazione... | `aperto` | `difetto` | `STATO_RUN.md` |
| `NO` | **D25** | — | Il gauge del tempo e' la costante 1e-9, e il 93 % dei nodi non invecchia / Z46 — MISURATO IN... | `da-decidere` | `difetto` | `STATO_RUN.md` |
| `NO` | **D28** | — | nsub esplode e lo tira max(/vd/) su POCHISSIMI archi: il costo dell'intero sistema e' governato... | `aperto` | `difetto` | `STATO_RUN.md` |
| `SI` | **D31** | — | Il freno di SCALAMIN (smpchiudi) E' IL MOTORE della crescita di d0: vale il 117.41 % del Δ... | `da-decidere` | `difetto` | `STATO_RUN.md` |
| `NO` | **D33** | — | La repulsione alla massima compressione e' AZZERATA proprio dove serve: dal 75 % al 96 % degli... | `aperto` | `difetto` | `STATO_RUN.md` |
| `NO` | **D36** | — | LA SOGLIA DELLA MITOSI E' IN UNITA' ASSOLUTE DI tw, MENTRE LA SCALA DI tw DIPENDE DAL DOMINIO DI... | `da-decidere` | `difetto` | `STATO_RUN.md` |
| `NO` | **REG-V** | — | verificaregistro.py: completezza, esistenza, coerenza con la traccia di d0 e col registro dei... | `da-decidere` | `difetto` | `STATO_RUN.md` |
| `NO` | **X2** | — | X2 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / ZETALOC: «smorzamento locale» che dipende da una... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z104** | — | Z104 APERTA ⏳[EPOCA 3 · DERIVAZIONE] / MEMARCO: LA MEMORIA DEL MOTO TRADOTTA IN FORMA... | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z142** | — | Z142 REPERTO, DIFETTI MIEI ⏳[archivi delle cure · SIGILLO FALLITO] / IL SIGILLO DI E4-LAM... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z148** | — | LA LEGGE d = LAM REGGE PERCHE' UNA CURA E' ACCESA (2026-09-24) | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z39** | — | Z39 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / UN FATTO STABILE DI CLAUDE.md E' CADUTO: cs E' VIVO.... | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z4** | — | Z4 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / floord0: SOSPESA, e i due rami violano assiomi... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z74** | — | Z74 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / il ramo B rallenta x11: nsub esplode, e lo tira... | `da-decidere` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z89** | — | Z89 DA RIVERIFICARE ⏳[EPOCA 1 · CODICE] / 1755 MB DI .pkl NON HANNO IL COMANDO CHE LI RIGENERA... | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z91** | — | Z91 APERTA ⏳[EPOCA 2 · LETTURA DEL CODICE] / SCALAMIN FRENA OGNI SCRITTURA SEPARATAMENTE, QUINDI... | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **Z92** | — | Z92 🟨LIMITE DICHIARATO ⏳[EPOCA 2 · LETTURA DEL CODICE] / COESADIM legge ISTANTI MISTI, e il suo... | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `NO` | **C18** | — | C18 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / IL FDT RIFATTO SUL SISTEMA NON CASTRATO (FASE 5... | `da-decidere` | `misura` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **R5** | — | contava 25 aperture su 24 passi: l'iniezione del test apriva il freno lei stessa | `da-decidere` | `presidio` | `CLAUDE.md` |

---

## FAMIGLIA **G** — ARRETRATO DEGLI STRUMENTI   *(7 voci)*

| blocca? | id | alias | che cos'e' | stato | tipo | fonte |
|:--:|---|---|---|:--:|:--:|---|
| `DA-DECIDERE` | **A4-METRICHE** | A4 | le METRICHE DEL SETTORE CHIRALE / doc/TASKHISTORY/2026-09-20metriche-settore-chirale.md ( il... | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **ANCORE-1** | — | APERTA il 2026-09-25 / 25 SIGILLI PRENDONO «IL CODICE DI PRIMA» DA HEAD (43 occorrenze su 310... | `aperto` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **B6** | — | le due cure OFF: COPPIARECIPROCA e GRAVAMPIEZZA / :739 e :732 (entrambe = False)... | `aperto` | `altro` | `STATO_RUN.md` |
| `NO` | **D13** | — | I sigilli storici non sono stati rigirati sul blob corrente / Z11 / — / APERTO | `aperto` | `difetto` | `STATO_RUN.md` |
| `NO` | **Z15** | — | Z15 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / 14 .pkl su 36 non portano il BLOB del codice che li ha... | `aperto` | `fronte` | `RAMIFICAZIONI.md` |
| `DA-DECIDERE` | **P5** | — | OGNI RAMO else / FALLBACK / getattr(..., default) SU UN PERCORSO FISICO VA CONTATO. | `da-decidere` | `presidio` | `CLAUDE.md` |
| `DA-DECIDERE` | **P6** | — | OGNI CSV DI MISURA PORTA BLOB, SEME E TUTTI I FLAG che distinguono quel run dagli altri | `da-decidere` | `presidio` | `CLAUDE.md` |

---

## FAMIGLIA **?** — SENZA FAMIGLIA — da assegnare a mano   *(235 voci)*

| blocca? | id | alias | che cos'e' | stato | tipo | fonte |
|:--:|---|---|---|:--:|:--:|---|
| `DA-DECIDERE` | **A3b** | — | (CITATO 15 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **AAAA-MM-GG** | — | (CITATO 3 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `NO` | **AB-CONTROLLI** | — | l'A/B di W5 non ha salvato i punti di CONTROLLO nel vuoto, e senza quelli la densificazione non... | `da-decidere` | `altro` | `csv/_test_fork/_ab_pozzo_d.py` |
| `DA-DECIDERE` | **ARCHI-PASSO** | — | (CITATO 2 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **AUTO-ATTENUA** | — | (CITATO 2 volte, MAI definito in un registro) [AUTO-ATTENUA] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **AUTO-MANUTENZIONE** | — | (CITATO 2 volte, MAI definito in un registro) [AUTO-MANUTENZIONE] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **AUTO-NORMALIZZANTE** | — | (CITATO 4 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **B7** | — | i reperti DA RIMISURARE sulla scena nuova / Z43, Z46, Z48-Z52, coerg / misurati su sep = 8 /... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **B9** | — | Z63 / Z64 — i 1455 nodi a 10⁻¹³; la catena f → x → r che non riproduce r / registro, ex-LISTA 2... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **BACKGROUND-INDEPENDENT** | — | (CITATO 2 volte, MAI definito in un registro) [BACKGROUND-INDEPENDENT] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **BIS-ANOM-SIMM** | — | (CITATO 6 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **BIS-DELTA** | — | (CITATO 3 volte, MAI definito in un registro) [BIS-DELTA] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `NO` | **CLIP-INVENTARIO** | — | INVENTARIO dei clip, tetti e pavimenti del passo pieno: 27 TETTI FISICI su 117 guardie | `aperto` | `altro` | `TASK_HISTORY/2026-09-27_etc-p…` |
| `DA-DECIDERE` | **COES-CAUSALE** | — | (CITATO 6 volte, MAI definito in un registro) [COES-CAUSALE] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `NO` | **COLLAUDO-NON-ESEGUITO** | — | un collaudo che si RIFIUTA di girare esce con 2, e il controllo C4 lo conta come PASS | `da-decidere` | `altro` | `csv/_controlli_riordino.py` |
| `DA-DECIDERE` | **CONFIG-1/** | — | (CITATO 4 volte, MAI definito in un registro) [CONFIG-1/] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **COSA-RICONTROLLARE** | — | (CITATO 3 volte, MAI definito in un registro) [COSA-RICONTROLLARE] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **CROSS-PASSO** | — | (CITATO 3 volte, MAI definito in un registro) [CROSS-PASSO] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **CURA1-CORTO** | — | (CITATO 2 volte, MAI definito in un registro) [CURA1-CORTO] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **CURA2-CORTO** | — | (CITATO 2 volte, MAI definito in un registro) [CURA2-CORTO] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **CURE-FINE** | — | (CITATO 2 volte, MAI definito in un registro) [CURE-FINE] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **CURE-INIZIO** | — | (CITATO 2 volte, MAI definito in un registro) [CURE-INIZIO] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **D3** | — | (CITATO 5 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `NO` | **D32-CONTATORE** | — | i contatori `_rep_taupp_*` contano un clamp che NON ESISTE PIU' | `da-decidere` | `altro` | `soliton_simulator.py` |
| `DA-DECIDERE` | **DIFETTI-NUOVI-FINE** | — | (CITATO 2 volte, MAI definito in un registro) [DIFETTI-NUOVI-FINE] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **DIFETTI-NUOVI-INIZIO** | — | (CITATO 2 volte, MAI definito in un registro) [DIFETTI-NUOVI-INIZIO] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **E1** | — | (CITATO 56 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **E4b** | — | (CITATO 5 volte, MAI definito in un registro) [E4b] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **F1** | — | (CITATO 19 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **F2** | — | (CITATO 17 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **F3** | — | (CITATO 14 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **F4** | — | (CITATO 4 volte, MAI definito in un registro) [F4] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **F5** | — | (CITATO 3 volte, MAI definito in un registro) [F5] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **FASE-5** | — | (CITATO 2 volte, MAI definito in un registro) [FASE-5] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **FASE1** | — | (CITATO 3 volte, MAI definito in un registro) [FASE1] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `NO` | **FILI-CORTI** | — | i fili si accorciano SOLO FRA LE MASSE o OVUNQUE? Il calo della distanza viene dai `d`, non... | `da-decidere` | `altro` | `csv/_test_fork/_ab_pozzo_d/RE…` |
| `DA-DECIDERE` | **FRENO-LEGGE** | — | (CITATO 5 volte, MAI definito in un registro) [FRENO-LEGGE] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `NO` | **FUGA-MULTIRIGA** | — | la via d'uscita di H-REG-R e H-P1-bis e' una regex SENZA re.S: una dichiarazione su PIU' RIGHE... | `da-decidere` | `altro` | `csv/_hook_fisica.py` |
| `DA-DECIDERE` | **G5** | — | (CITATO 4 volte, MAI definito in un registro) [G5] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **G6** | — | (CITATO 16 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **G7** | — | (CITATO 3 volte, MAI definito in un registro) [G7] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **G8** | — | (CITATO 3 volte, MAI definito in un registro) [G8] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **G9** | — | (CITATO 6 volte, MAI definito in un registro) [G9] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **GLOBALE-DISEGNO** | — | (CITATO 19 volte, MAI definito in un registro) [GLOBALE-DISEGNO] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `NO` | **H-REGR-LARGA** | — | H-REG-R associa una scheda per NOME DI FUNZIONE: scatta su qualunque modifica a `_applica_flag`... | `da-decidere` | `altro` | `csv/_hook_fisica.py` |
| `DA-DECIDERE` | **H1** | — | (CITATO 7 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **H2** | — | (CITATO 4 volte, MAI definito in un registro) [H2] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **H3** | — | (CITATO 3 volte, MAI definito in un registro) [H3] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **H3b** | — | (CITATO 3 volte, MAI definito in un registro) [H3b] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **H4** | — | (CITATO 4 volte, MAI definito in un registro) [H4] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **H5** | — | (CITATO 4 volte, MAI definito in un registro) [H5] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **H6** | — | (CITATO 3 volte, MAI definito in un registro) [H6] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **HDF5** | — | (CITATO 8 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **I2** | — | (CITATO 28 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **I3** | — | (CITATO 8 volte, MAI definito in un registro) [I3] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **I4** | — | (CITATO 14 volte, MAI definito in un registro) [I4] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **I5** | — | (CITATO 14 volte, MAI definito in un registro) [I5] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **IC95** | — | (CITATO 80 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **INTERO-BLOCCO** | — | (CITATO 7 volte, MAI definito in un registro) [INTERO-BLOCCO] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **K1** | — | (CITATO 26 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **K2** | — | (CITATO 19 volte, MAI definito in un registro) [K2] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **K3** | — | (CITATO 17 volte, MAI definito in un registro) [K3] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **K4** | — | (CITATO 12 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **K5** | — | (CITATO 12 volte, MAI definito in un registro) [K5] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **K7** | — | (CITATO 28 volte, MAI definito in un registro) [K7] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **K8** | — | (CITATO 10 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **L1** | — | (CITATO 9 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **M1b** | — | (CITATO 23 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **M2b** | — | (CITATO 7 volte, MAI definito in un registro) [M2b] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **M3** | — | (CITATO 27 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **M3c** | — | (CITATO 20 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **M4** | — | (CITATO 18 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **MANDATO-PATTERN** | — | (CITATO 2 volte, MAI definito in un registro) [MANDATO-PATTERN] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **MANDATO-REGISTRO** | — | (CITATO 12 volte, MAI definito in un registro) [MANDATO-REGISTRO] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `NO` | **MASSA-ID** | — | le masse si identificano con l'ID di massa (conc_nodi), non coi nodi del passo 0 ne' con la fase | `aperto` | `altro` | `TASK_HISTORY/2026-09-27_massa…` |
| `NO` | **MASSA-MIGRA** | — | la massa segue i NODI o la COERENZA? E come cambia la sua FORMA? | `da-decidere` | `altro` | `TASK_HISTORY/2026-09-27_pilot…` |
| `DA-DECIDERE` | **MASSE-COERENTI** | — | (CITATO 6 volte, MAI definito in un registro) [MASSE-COERENTI] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **MIT1** | — | (CITATO 7 volte, MAI definito in un registro) [MIT1] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **MIT2** | — | (CITATO 7 volte, MAI definito in un registro) [MIT2] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **MODEL-FREE** | — | (CITATO 4 volte, MAI definito in un registro) [MODEL-FREE] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **N1** | — | (CITATO 15 volte, MAI definito in un registro) [N1] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **N1b** | — | (CITATO 8 volte, MAI definito in un registro) [N1b] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **N2** | — | (CITATO 17 volte, MAI definito in un registro) [N2] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **N3** | — | (CITATO 6 volte, MAI definito in un registro) [N3] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **N3b** | — | (CITATO 22 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **N6** | — | (CITATO 12 volte, MAI definito in un registro) [N6] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **N7** | — | (CITATO 13 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **O2** | — | (CITATO 9 volte, MAI definito in un registro) [O2] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **P1b** | — | (CITATO 7 volte, MAI definito in un registro) [P1b] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **P2b** | — | (CITATO 3 volte, MAI definito in un registro) [P2b] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **P5a** | — | (CITATO 5 volte, MAI definito in un registro) [P5a] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **P5b** | — | (CITATO 6 volte, MAI definito in un registro) [P5b] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **P7** | — | (CITATO 18 volte, MAI definito in un registro) [P7] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **P8** | — | (CITATO 20 volte, MAI definito in un registro) [P8] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **P9** | — | (CITATO 12 volte, MAI definito in un registro) [P9] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `NO` | **PASSO-PIENO** | — | un hook che rifiuta uno script che avanza con net.step() invece di csv/_passo.py passo_pieno | `da-decidere` | `altro` | `csv/_passo.py` |
| `DA-DECIDERE` | **PEQ-ESATTO** | — | (CITATO 6 volte, MAI definito in un registro) [PEQ-ESATTO] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **PEQ-NASCITA** | — | (CITATO 6 volte, MAI definito in un registro) [PEQ-NASCITA] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **PER-ARCO** | — | (CITATO 2 volte, MAI definito in un registro) [PER-ARCO] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **POST-HOC** | — | (CITATO 5 volte, MAI definito in un registro) [POST-HOC] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **PUNTO-DI-RIPRESA** | — | (CITATO 3 volte, MAI definito in un registro) [PUNTO-DI-RIPRESA] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Q0** | — | (CITATO 3 volte, MAI definito in un registro) [Q0] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Q1** | — | (CITATO 13 volte, MAI definito in un registro) [Q1] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Q1a** | — | (CITATO 5 volte, MAI definito in un registro) [Q1a] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Q1b** | — | (CITATO 6 volte, MAI definito in un registro) [Q1b] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Q2** | — | (CITATO 9 volte, MAI definito in un registro) [Q2] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Q3** | — | (CITATO 9 volte, MAI definito in un registro) [Q3] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Q4** | — | (CITATO 23 volte, MAI definito in un registro) [Q4] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Q5** | — | (CITATO 7 volte, MAI definito in un registro) [Q5] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Q8** | — | (CITATO 13 volte, MAI definito in un registro) [Q8] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **QUADRO-FINE** | — | (CITATO 2 volte, MAI definito in un registro) [QUADRO-FINE] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **QUADRO-INIZIO** | — | (CITATO 2 volte, MAI definito in un registro) [QUADRO-INIZIO] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **QUASI-CANCELLAZIONE** | — | (CITATO 2 volte, MAI definito in un registro) [QUASI-CANCELLAZIONE] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **R1** | — | (CITATO 30 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **R3b** | — | (CITATO 12 volte, MAI definito in un registro) [R3b] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **R4** | — | (CITATO 13 volte, MAI definito in un registro) [R4] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **R6** | — | (CITATO 27 volte, MAI definito in un registro) [R6] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `NO` | **RAMI-OFF-CURA2** | — | i rami a flag spento di TEMPO_UNICO_MITOSI, archiviati COPIATI dal sorgente | `da-decidere` | `altro` | `csv/_archivio/rami_off_cura2.…` |
| `DA-DECIDERE` | **RAMPA-2/** | — | (CITATO 2 volte, MAI definito in un registro) [RAMPA-2/] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **RAMPA2** | — | (CITATO 3 volte, MAI definito in un registro) [RAMPA2] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **RES-INVARIANTI** | — | (CITATO 6 volte, MAI definito in un registro) [RES-INVARIANTI] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **RI-GIRABILE** | — | (CITATO 4 volte, MAI definito in un registro) [RI-GIRABILE] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **RI-GIRABILI** | — | (CITATO 3 volte, MAI definito in un registro) [RI-GIRABILI] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **RI-INTERROGA** | — | (CITATO 2 volte, MAI definito in un registro) [RI-INTERROGA] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **RI-LETTA** | — | (CITATO 4 volte, MAI definito in un registro) [RI-LETTA] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `NO` | **RISCRITTURA-GO** | — | riscrivere il simulatore in Go: valutato, NON deciso | `da-decidere` | `altro` | `VALUTAZIONE_go.md` |
| `NO` | **RITMO-PAVIMENTO** | — | IL PAVIMENTO DEL RITMO MORDE: min(r) = 1.414212e-06 e' ESATTAMENTE il pavimento, non un valore... | `da-decidere` | `altro` | `REGISTRO_FISICA.md` |
| `DA-DECIDERE` | **ROMPI-ANELLO** | — | (CITATO 8 volte, MAI definito in un registro) [ROMPI-ANELLO] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **S04** | — | La crescita e' NUCLEAZIONE, non stiramento / CADE con Z108: nascite meno morti valgono lo 0.01 %... | `da-decidere` | `altro` | `STATO_RUN.md` |
| `DA-DECIDERE` | **S1** | — | (CITATO 51 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **S1a** | — | (CITATO 15 volte, MAI definito in un registro) [S1a] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **S1b** | — | (CITATO 19 volte, MAI definito in un registro) [S1b] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **S3** | — | (CITATO 43 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **S3a** | — | (CITATO 5 volte, MAI definito in un registro) [S3a] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **S4a** | — | (CITATO 4 volte, MAI definito in un registro) [S4a] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **S8** | — | (CITATO 20 volte, MAI definito in un registro) [S8] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **S8b** | — | (CITATO 6 volte, MAI definito in un registro) [S8b] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **S8c** | — | (CITATO 3 volte, MAI definito in un registro) [S8c] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **S8d** | — | (CITATO 4 volte, MAI definito in un registro) [S8d] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **SCALA-MIN-PASSO** | — | (CITATO 6 volte, MAI definito in un registro) [SCALA-MIN-PASSO] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **SIGILLO-CURA2** | — | (CITATO 2 volte, MAI definito in un registro) [SIGILLO-CURA2] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **SIGILLO-CURA2-RIPARATO** | — | (CITATO 2 volte, MAI definito in un registro) [SIGILLO-CURA2-RIPARATO] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **SOTTO-PASSO** | — | (CITATO 4 volte, MAI definito in un registro) [SOTTO-PASSO] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **STANDARD 1** | — | (CITATO 10 volte, MAI definito in un registro) [STANDARD 1] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **STANDARD 2** | — | (CITATO 5 volte, MAI definito in un registro) [STANDARD 2] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **STANDARD 5** | — | (CITATO 3 volte, MAI definito in un registro) [STANDARD 5] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **STANDARD 7** | — | (CITATO 2 volte, MAI definito in un registro) [STANDARD 7] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **STANDARD 9** | — | (CITATO 13 volte, MAI definito in un registro) [STANDARD 9] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **STANDARD ⑤** | — | (CITATO 3 volte, MAI definito in un registro) [STANDARD ⑤] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **STEP2** | — | (CITATO 66 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **SU2** | — | (CITATO 67 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **T0** | — | (CITATO 32 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **T1** | — | (CITATO 112 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **T1a** | — | (CITATO 19 volte, MAI definito in un registro) [T1a] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **T1b** | — | (CITATO 23 volte, MAI definito in un registro) [T1b] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **T6** | — | (CITATO 32 volte, MAI definito in un registro) [T6] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **T7** | — | (CITATO 9 volte, MAI definito in un registro) [T7] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **T9** | — | (CITATO 7 volte, MAI definito in un registro) [T9] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **TEMPO-LUCE** | — | (CITATO 10 volte, MAI definito in un registro) [TEMPO-LUCE] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **TERRA-BUCONERO** | — | (CITATO 3 volte, MAI definito in un registro) [TERRA-BUCONERO] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **TRIAGE-FINE** | — | (CITATO 2 volte, MAI definito in un registro) [TRIAGE-FINE] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **TRIAGE-INIZIO** | — | (CITATO 2 volte, MAI definito in un registro) [TRIAGE-INIZIO] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **U4** | — | (CITATO 5 volte, MAI definito in un registro) [U4] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **U5** | — | (CITATO 6 volte, MAI definito in un registro) [U5] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **U6** | — | (CITATO 5 volte, MAI definito in un registro) [U6] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **U7b** | — | (CITATO 12 volte, MAI definito in un registro) [U7b] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **V10** | — | (CITATO 5 volte, MAI definito in un registro) [V10] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **V5b** | — | (CITATO 3 volte, MAI definito in un registro) [V5b] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **V6b** | — | (CITATO 6 volte, MAI definito in un registro) [V6b] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `NO` | **VIDEO-SCENA** | — | il video della scena del pilota: diagnostico, mostra `pos` che NON e' la distanza fisica | `aperto` | `altro` | `TASK_HISTORY/2026-09-27_video…` |
| `DA-DECIDERE` | **VUOTO-MASSA** | — | (CITATO 2 volte, MAI definito in un registro) [VUOTO-MASSA] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **W2** | — | (CITATO 4 volte, MAI definito in un registro) [W2] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **W4** | — | (CITATO 7 volte, MAI definito in un registro) [W4] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `NO` | **W5** | — | CRITERIO di POZZO-D: A/B nel driver, scena (ii)(a), 4 semi, 120 passi, con la barra fra semi | `da-decidere` | `altro` | `TASK_HISTORY/2026-09-27_d02-p…` |
| `DA-DECIDERE` | **Y0** | — | (CITATO 4 volte, MAI definito in un registro) [Y0] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Y10** | — | (CITATO 4 volte, MAI definito in un registro) [Y10] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Y3** | — | (CITATO 9 volte, MAI definito in un registro) [Y3] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Y4** | — | (CITATO 5 volte, MAI definito in un registro) [Y4] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Y5** | — | (CITATO 65 volte, MAI definito in un registro) | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Y6** | — | (CITATO 9 volte, MAI definito in un registro) [Y6] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Y7** | — | (CITATO 5 volte, MAI definito in un registro) [Y7] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Y8** | — | (CITATO 4 volte, MAI definito in un registro) [Y8] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Z128** | — | (CITATO 2 volte, MAI definito in un registro) [Z128] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Z147** | — | (CITATO 3 volte, MAI definito in un registro) [Z147] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Z1b** | — | (CITATO 12 volte, MAI definito in un registro) [Z1b] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Z1c** | — | (CITATO 30 volte, MAI definito in un registro) [Z1c] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Z4a** | — | (CITATO 16 volte, MAI definito in un registro) [Z4a] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **Z4b** | — | (CITATO 10 volte, MAI definito in un registro) [Z4b] | `da-decidere` | `altro` | `(nessuna definizione trovata)` |
| `DA-DECIDERE` | **DOPPIA-COP** | — | LA CURA (b): la doppia copertura 4 pi e' un ASSIOMA e va resa STRUTTURALE, non misurata | `aperto` | `cura` | `CURE_fisica_ordine.md` |
| `DA-DECIDERE` | **RIPIEGHI-ZERO** | — | ZERO ripieghi che cambiano la fisica in silenzio: tutti e 100 i confronti `len(x) < n` | `aperto` | `cura` | `TASK_HISTORY/2026-09-28_mitos…` |
| `SI` | **SCHED-PASSO** | — | il passo pieno diventa uno SCHEDULATORE: le regole del passo sono architettura, non intenzioni | `aperto` | `cura` | `PIANO_schedulatore_passo.md` |
| `NO` | **ALLUNG-RELATIVO** | — | il criterio V6 dell'allungamento sottrae variazioni relative con DENOMINATORI DIVERSI | `aperto` | `difetto` | `csv/_test_fork/_pilota_prova1…` |
| `NO` | **ARCHI-PRIMI** | — | la vista disegna i PRIMI 24000 archi per indice: il 100 % finisce in un quadrante, misurato | `aperto` | `difetto` | `soliton_simulator.py` |
| `SI` | **CENS-A1** | CENSIMENTO:A1 | [A] la RIDUZIONE AL LIMITE dello spinore: lo stato che la garantisce non e' raggiungibile | `aperto` | `difetto` | `CENSIMENTO_intenzioni.md` |
| `SI` | **CENS-A2** | CENSIMENTO:A2 | [A] `TORS_4PI`: *"Prova sperimentale, default off"*, e il default e' `True` | `aperto` | `difetto` | `CENSIMENTO_intenzioni.md` |
| `NO` | **CENS-A3** | CENSIMENTO:A3 | [A] `COPPIA_MIT`: *"(opzione, spenta di default)"*, e il default e' `1.0` | `aperto` | `difetto` | `CENSIMENTO_intenzioni.md` |
| `NO` | **CENS-A4** | CENSIMENTO:A4 | [A] `MITOSI_DIR`: *"MITOSI DIREZIONALE ATTIVA"*, e il valore e' `0.0` | `aperto` | `difetto` | `CENSIMENTO_intenzioni.md` |
| `NO` | **CENS-A5** | CENSIMENTO:A5 | [A] `_passo_spinoriale` *"ORFANO"*: smentito da un altro commento dello stesso file | `aperto` | `difetto` | `CENSIMENTO_intenzioni.md` |
| `SI` | **CENS-A6** | CENSIMENTO:A6 | [A] `README.md`: *"Tutti gli script di lancio includono esplicitamente `--sync`"* | `aperto` | `difetto` | `CENSIMENTO_intenzioni.md` |
| `SI` | **CENS-A7** | CENSIMENTO:A7 | [A] il commento di `calcola_psi`: *"~19 chiamanti"*, misurato **2** | `aperto` | `difetto` | `CENSIMENTO_intenzioni.md` |
| `NO` | **D05** | — | I residui di C5: I4 scatola nera, I5 underflow per riga, modalita' fine / il mandato C5 e la... | `aperto` | `difetto` | `STATO_RUN.md` |
| `NO` | **D06** | — | fattcsultimo e' SCRITTO e MAI LETTO (quarto caso della stessa famiglia) / Z7, letto dal codice /... | `aperto` | `difetto` | `STATO_RUN.md` |
| `NO` | **D07** | — | TAUA e' UN SOLO numero per DUE leggi fisiche distinte / Z10, Z9-bis / — / APERTO | `aperto` | `difetto` | `STATO_RUN.md` |
| `NO` | **D08** | — | Il terzo ramo di calcolapsi (elif sotto REPULSLEGGE) e' DICHIARATO, non corretto / Z14, letto... | `aperto` | `difetto` | `STATO_RUN.md` |
| `NO` | **D10** | — | nsub governa il costo dell'intero sistema ed e' INVISIBILE: nessun contatore, nessuna colonna /... | `aperto` | `difetto` | `STATO_RUN.md` |
| `NO` | **D12** | — | 1755 MB di .pkl non hanno il comando che li rigenera (par.5-quinquies: «un dato che nessuno... | `aperto` | `difetto` | `STATO_RUN.md` |
| `NO` | **D15** | — | A7: la carica chirale NON si conserva / Z71, letto dal codice / — / APERTO | `aperto` | `difetto` | `STATO_RUN.md` |
| `NO` | **D21** | — | floord0 e' SOSPESA, e i due rami violano assiomi DIVERSI: la scelta non e' stata fatta / Z4 / —... | `aperto` | `difetto` | `STATO_RUN.md` |
| `NO` | **D23** | — | La cucitura dello snapshot FALLISCE su entrambi i fronti, e si DIMOSTRA perche'. NON CABLATA /... | `aperto` | `difetto` | `STATO_RUN.md` |
| `NO` | **D29** | — | CINQUE NODI DI VUOTO sono i piu' connessi dell'intero sistema: il vuoto ha degli HUB, e non... | `aperto` | `difetto` | `STATO_RUN.md` |
| `NO` | **FOGLIO-NULLO** | — | il diagnostico dei fogli vale il suo NULLO sulla scena (ii): la fase sta sul confine | `aperto` | `difetto` | `csv/_test_fork/_pilota_prova1…` |
| `NO` | **FORMA-N-VUOTO** | — | `n` in forma_passo0 non puo' cambiare: e' l'insieme congelato del passo 0 (P4) | `aperto` | `difetto` | `csv/_test_fork/_pilota_prova1…` |
| `DA-DECIDERE` | **MCRIT-RICALCOLO** | — | massa_critica_adattiva si ricalcola 7 volte per passo su stati diversi: e' una lettura mista | `aperto` | `difetto` | `REGISTRO_FISICA.md` |
| `DA-DECIDERE` | **MITOSI-SOGLIA-GRAD** | — | la soglia di mitosi si abbassa col gradiente di tempo proprio: ampiezza 0.3 e tanh a mano | `aperto` | `difetto` | `REGOLE_composizione_T3.md` |
| `DA-DECIDERE` | **RINCULO-RIPETUTI** | — | il rinculo dei genitori applica UNA spinta sola a un nodo genitore due volte nello stesso passo | `aperto` | `difetto` | `TASK_HISTORY/2026-09-28_mitos…` |
| `DA-DECIDERE` | **S09-MEDIANA** | — | la spinta S09 scala con `median(d0)` GLOBALE: lo stesso A2 gia' curato in S05 il 2026-09-17 | `aperto` | `difetto` | `soliton_simulator.py` |
| `NO` | **SYNCDB-HEADLESS** | — | `--sync-db` in headless CARICA ma non SALVA: lo dice il docstring del driver | `aperto` | `difetto` | `csv/_test_fork/_scena_video.py` |
| `DA-DECIDERE` | **TORS-SPINTA** | — | la spinta repulsiva di torsione: legge DINAMICA dentro mitosi(), con tre numeri non derivati | `aperto` | `difetto` | `REGOLE_composizione_T3.md` |
| `NO` | **V5-SOGLIA** | — | il criterio V5 confonde SCIOGLIERSI con MIGRARE, e misura lo spostamento con LAM | `aperto` | `difetto` | `TASK_HISTORY/2026-09-27_pilot…` |
| `NO` | **FATTI-AVVIO** | — | la catena di AVVIO non ha un solo fatto in FATTI_dal_codice.md: _applica_flag, avvia_test... | `da-decidere` | `fronte` | `FATTI_dal_codice.md` |
| `NO` | **IMPL-2** | — | una SECONDA implementazione indipendente, scritta dalle LEGGI e non dal codice | `da-decidere` | `fronte` | `VALUTAZIONE_go.md` |
| `NO` | **INDICE-LEGGERO** | — | l'indice pesa 169 KB e leggerlo intero non fa risparmiare contesto: serve un comando di... | `da-decidere` | `fronte` | `csv/_indice_id.py` |
| `NO` | **B7-SHAKE** | B7 | SHAKE 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / shake-then-freeze — la precessione mutua non... | `da-decidere` | `misura` | `RAMIFICAZIONI.md` |
| `NO` | **PROVA1-40-80** | — | i NODI delle masse del passo 0 si avvicinano piu' dei controlli a 40-80 passi; il calo sta negli INT | `aperto` | `misura` | `csv/_test_fork/_pilota_prova1…` |
| `NO` | **SCHED-T3-REGOLE** | — | le regole di composizione: 94 scritture, 80 nelle cinque forme, 6 eccezioni in tre famiglie | `aperto` | `misura` | `REGOLE_composizione_T3.md` |
| `NO` | **SCHW-CORTI** | — | il 39 % delle coppie Schwinger ACCORCIA il grafo: 2*dd < d, misurato | `aperto` | `misura` | `csv/_test_fork/_pilota_prova1…` |
| `NO` | **TRATTI-INTERNI** | — | a 80 passi il calo di A(t) sta negli INTERNI, non nel varco: le regioni si contraggono | `aperto` | `misura` | `csv/_test_fork/_pilota_prova1…` |
| `NO` | **H-ETC-1** | — | PRESIDIO PROPOSTO E NON CABLATO: zero calcola_psi senza w dentro passo_pieno | `aperto` | `presidio` | `TASK_HISTORY/2026-09-27_etc-p…` |
| `NO` | **H-ETC-2** | — | PRESIDIO PROPOSTO E NON CABLATO: permutare le cinque leggi deve dare lo STESSO stato (Jacobi) | `aperto` | `presidio` | `TASK_HISTORY/2026-09-27_etc-p…` |
| `DA-DECIDERE` | **P1** | — | NON USARE L'ASSOCIAZIONE SENZA VERIFICARE LO STORICO. | `da-decidere` | `presidio` | `CLAUDE.md` |
| `DA-DECIDERE` | **P2** | — | PRIMA DI ESCLUDERE UN FLAG DA UNA MISURA: FORZA IL SISTEMA O LO CORREGGE? | `da-decidere` | `presidio` | `CLAUDE.md` |
| `DA-DECIDERE` | **P4** | — | PRIMA DI MISURARE SE UNA GRANDEZZA CAMBIA, VERIFICARE CHE SIA LIBERA DI CAMBIARE. | `da-decidere` | `presidio` | `CLAUDE.md` |
| `DA-DECIDERE` | **R3** | — | pretendeva bias == 0.0 esatto e falliva su due ulp di arrotondamento | `da-decidere` | `presidio` | `CLAUDE.md` |
| `NO` | **STATI-LOCALI** | — | gli stati .npz del grafo restano LOCALI: in git vanno solo sha1, percorso e comando | `aperto` | `presidio` | `TASK_HISTORY/2026-09-27_tratt…` |
| `DA-DECIDERE` | **U3** | — | confrontava con il mio sviluppo e/2 invece del valore esatto e/(2+e); il numero stampato... | `da-decidere` | `presidio` | `CLAUDE.md` |

---

## 📤 **FUORI LISTA — 460 voci, ciascuna col MOTIVO** *(dai campi dell'indice)*

### motivo: **etichetta LOCALE a una scheda o a un sigillo: il nome pieno include il sigillo, e non e' un fronte del programma**   *(245 voci)*

| id | che cos'e' | tipo |
|---|---|:--:|
| A2b | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| ACCOPPIAMENTO2 | (CITATO 2 volte, MAI definito in un registro; citato solo in... [ACCOPPIAMENTO2] | `criterio-locale` |
| ALLA-NASCITA | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task...… | `criterio-locale` |
| ANTI-ALLINEAMENTO | (CITATO 2 volte, MAI definito in un registro; citato solo in... [ANTI-ALLINEAMENTO] | `criterio-locale` |
| AUTO-REFERENZIALE | (CITATO 2 volte, MAI definito in un registro; citato solo in... [AUTO-REFERENZIALE] | `criterio-locale` |
| COER-4PI | la coerenza della massa e' `/<e^{i phi}>/`: il campo NON distingue `phi` da `phi+2pi`… | `criterio-locale` |
| COME-MISURARE | (CITATO 2 volte, MAI definito in un registro; citato solo in... [COME-MISURARE] | `criterio-locale` |
| COMPONENTI:A1 | A1. STEP2OROLOGIO — aggancio OROLOGIO ↔ METRICA · omegaclk = (cs/CSM)² | `criterio-locale` |
| COMPONENTI:A2 | peq è lo sfondo diffuso locale (Legge I, :265): nessuna statistica globale | `criterio-locale` |
| COMPONENTI:A3 | dopo la proiezione arco→nodo, numeratore e denominatore vivono entrambi sui nodi | `criterio-locale` |
| COMPONENTI:A5 | d/cs è il tempo causale | `criterio-locale` |
| COMPONENTI:A6 | A6 (ragione primaria) / l'inerzia si valuta sullo stato precedente. Una funzione istantanea… | `criterio-locale` |
| COMPONENTI:A8 | il fallback dello sfondo è contato — e non basta quante volte scatta: si registra quando (Y5) | `criterio-locale` |
| COMPONENTI:B1 | --deparam-orologio / SÌ — «zero parametri» nel suo commento / byte-identità a OFF dichiarata... | `criterio-locale` |
| COMPONENTI:B10 | --tau-luce / SÌ — d/cs, lo stesso tau già cablato nello Strato 1, coefficiente 1 / NO —… | `criterio-locale` |
| COMPONENTI:B11 | --cs-dinamico / sì (cs = CSM/(1+GAMMA√I), stesso GAMMA di G(rho)) / A/B storico; nessun... | `criterio-locale` |
| COMPONENTI:B2 | --spinore-corretto / sì per costruzione (evaluate-then-commit, \/psi\/=1) / «Default off =... | `criterio-locale` |
| COMPONENTI:B3 | --verlet / è una scelta di integratore, non una legge / «attivare per il confronto A/B» /... | `criterio-locale` |
| COMPONENTI:B4 | --spinore-vivo / sì (reinnesto nell'ordine ETC, zero parametri) / «Reversibile, per A/B... | `criterio-locale` |
| COMPONENTI:B5 | --chi-core / «nessun segno selezionato a priori» / «default off per A/B» / NON STABILITO. Il… | `criterio-locale` |
| COMPONENTI:B6 | --campo-spinoriale / sì (FASE 1, riduzione al limite esatta) / «Default off = byte-identico»;… | `criterio-locale` |
| COMPONENTI:B7 | --fork-su2 / sì (Berry non normalizzato, il peso cos(chi/2) è ciò che resta non normalizzando)… | `criterio-locale` |
| COMPONENTI:B8 | --fork-su2-mem / sì — tau = d/cs, «nessun numero nuovo, d e cs esistono già» / 23/23 PASS, S7... | `criterio-locale` |
| COMPONENTI:B9 | --step2-orologio / SÌ — orologio di Compton omega ∝ cs²; «fisica NECESSARIA e derivata: zero... | `criterio-locale` |
| COMPONENTI:C1 | --gamma-turbo / dichiarato dal codice stesso: «[DIAGNOSTICO, NON PERCORSO CERTIFICATO]... | `criterio-locale` |
| COMPONENTI:C2 | --kuramoto-su2 / meccanismo di allineamento aggiunto a mano, non derivato. E refutato per... | `criterio-locale` |
| COMPONENTI:C3 | --regime (deterministico, ecc.) / cambia quattro interruttori insieme (TAUA, GPH, CALOREINIT... | `criterio-locale` |
| COMPONENTI:D1 | csnodoprev esteso alla mitosi — il figlio eredita cs dal padre, come le altre sei cache /... | `criterio-locale` |
| COMPONENTI:D2 | psispinprec esteso alla mitosi — settima voce della stessa convenzione / guardia 4π fallita… | `criterio-locale` |
| COMPONENTI:S1 | FAIL ATTESO — vs blob 2277e9a0, di quattro cambiamenti fa / nodi 3164 contro 2924, 32 shape | `criterio-locale` |
| COMPONENTI:S2 | riduzione al limite sul blob ATTUALE: ON (cs=CSM) vs OFF byte-identico / 0.000e+00 con nodi… | `criterio-locale` |
| COMPONENTI:S3 | S3.0 / IL CONTROLLO POSITIVO: il test VEDE l'effetto / 39/40 nodi con \/f(1)−f(0)\/ 1e-13 | `criterio-locale` |
| COMPONENTI:S3b | l'orologio rallenta dove cs è basso / 0.0100 volte a cs = 0.1·CSM | `criterio-locale` |
| COMPONENTI:S3c | a cs = CSM il fattore è 1 esatto / 1.000000000000000 | `criterio-locale` |
| COMPONENTI:Y0-Y10 | Y10, 11/11 PASS. | `criterio-locale` |
| COMPONENTI:Z30 | Z30: la forma del denominatore — nudo (attuale, zero scelte) contro linea (la meno | `criterio-locale` |
| D4 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| D5 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [D5] | `criterio-locale` |
| D6 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [D6] | `criterio-locale` |
| D97 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [D97] | `criterio-locale` |
| DA-DECIDERE | (CITATO 222 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| DE-ACCOPPIABILITA | (CITATO 2 volte, MAI definito in un registro; citato solo in... [DE-ACCOPPIABILITA] | `criterio-locale` |
| DOMANDE-BUSSOLA | (CITATO 2 volte, MAI definito in un registro; citato solo in... [DOMANDE-BUSSOLA] | `criterio-locale` |
| DOVE-VA | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| E4a | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [E4a] | `criterio-locale` |
| END-TO-END | (CITATO 4 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| ESENTE-P3 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task... [ESENTE-P3] | `criterio-locale` |
| EVALUATE-THEN-COMMIT | (CITATO 2 volte, MAI definito in un registro; citato solo in... [EVALUATE-THEN-COMMIT] | `criterio-locale` |
| F7 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [F7] | `criterio-locale` |
| FASE2 | (CITATO 6 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| FORK-FIRST | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task...… | `criterio-locale` |
| G0 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [G0] | `criterio-locale` |
| G5b | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [G5b] | `criterio-locale` |
| GLOBALE-DIS | (CITATO 4 volte, MAI definito in un registro; citato solo in referti/sigilli/task...… | `criterio-locale` |
| H6b | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [H6b] | `criterio-locale` |
| IN-CHE-ORDINE | (CITATO 2 volte, MAI definito in un registro; citato solo in... [IN-CHE-ORDINE] | `criterio-locale` |
| IN-RUN | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| INERZIA-1( | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task...… | `criterio-locale` |
| INERZIA-INERZIA | (CITATO 3 volte, MAI definito in un registro; citato solo in... [INERZIA-INERZIA] | `criterio-locale` |
| J2 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [J2] | `criterio-locale` |
| JHEP04 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| K0 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [K0] | `criterio-locale` |
| K10 | (CITATO 4 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [K10] | `criterio-locale` |
| K11 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [K11] | `criterio-locale` |
| K12 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [K12] | `criterio-locale` |
| K2a | SIGILLO osservabile-P1: si cambia SOLO `d` (un arco del cammino minimo x10) e la distanza… | `criterio-locale` |
| K2b | SIGILLO osservabile-P1: si cambia SOLO `pos` (un nodo di 10 LAM) e la distanza NON deve... | `criterio-locale` |
| K300 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| K6 | (CITATO 9 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| K9 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [K9] | `criterio-locale` |
| L0 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [L0] | `criterio-locale` |
| L10 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [L10] | `criterio-locale` |
| L113 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| L117 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| L184 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| L189 | (CITATO 4 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| L191 | (CITATO 4 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| L203 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| L206 | (CITATO 5 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| L208 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| L212 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| L257 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| L309 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| L311 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| L312 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| L317 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| L323 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| L324 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| L949 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| L982 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| M0 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [M0] | `criterio-locale` |
| M0a | MISURA 0 di DRIVER-SCENA-II: `--nodi 0` NON e' rispettato -- net.n = 455 dopo `_applica_flag`... | `criterio-locale` |
| M0b | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [M0b] | `criterio-locale` |
| M0c | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [M0c] | `criterio-locale` |
| M1c | (CITATO 5 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [M1c] | `criterio-locale` |
| M3b | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [M3b] | `criterio-locale` |
| M5a | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [M5a] | `criterio-locale` |
| M5b | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [M5b] | `criterio-locale` |
| M5c | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [M5c] | `criterio-locale` |
| M8 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [M8] | `criterio-locale` |
| MASSA-VUOTO | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task...… | `criterio-locale` |
| N4 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [N4] | `criterio-locale` |
| N5 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [N5] | `criterio-locale` |
| N7b | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [N7b] | `criterio-locale` |
| N7c | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [N7c] | `criterio-locale` |
| N8 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [N8] | `criterio-locale` |
| O1 | (CITATO 12 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| O3 | (CITATO 8 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| O3a | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [O3a] | `criterio-locale` |
| O3c | (CITATO 4 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [O3c] | `criterio-locale` |
| O4 | (CITATO 7 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| P0 | (CITATO 12 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [P0] | `criterio-locale` |
| P10 | (CITATO 9 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [P10] | `criterio-locale` |
| P11 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [P11] | `criterio-locale` |
| PADRE-FIGLIO | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task...… | `criterio-locale` |
| PAT-1/PAT-2 | (CITATO 1 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| PCG64 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| PESO-MAX | partecipazioni multiple: l'opacita' di un nodo e' il MAX su tutte le masse, non la media… | `criterio-locale` |
| Q7 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [Q7] | `criterio-locale` |
| QQ777 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| R0 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [R0] | `criterio-locale` |
| R11 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [R11] | `criterio-locale` |
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
| REGISTRO_FISICA:C3 | frazione di impacchettamento 0.384 NELLA SFERA INTERNA — i nodi a distanza = RCONN dal bordo... | `criterio-locale` |
| REGISTRO_FISICA:C4 | nessun rifiuto falso: con n sotto la capienza misurata la semina riesce sempre, su quattro… | `criterio-locale` |
| REGISTRO_FISICA:D33 | la repulsione si spegne dove servirebbe. Il segno si inverte oltre 3.5π, ma | `criterio-locale` |
| REGISTRO_FISICA:D35 | l'antifase non è un'antifase. Il campo è F = Σ K·exp(iφ), e | `criterio-locale` |
| REGISTRO_FISICA:D37 | UNA CHIAVE DUPLICATA NEI DOMINI, ed è mia | `criterio-locale` |
| REGISTRO_FISICA:E1a | E1a la mitosi non muore / Luca / gnatimitosi 0 e n cresce / il nullo: se la cura rompesse fm,… | `criterio-locale` |
| REGISTRO_FISICA:E1b | E1b la mitosi non esplode / Luca / n finale < 10× il riferimento, e il run arriva a 600 passi… | `criterio-locale` |
| REGISTRO_FISICA:E1c | E1c il fattore / mio / le nascite salgono di un fattore fra 5× e 100× / DERIVATA dagli archi… | `criterio-locale` |
| REGISTRO_FISICA:E2 | E2 le coppie annichilano / Luca / NON MISURABILE, e si dichiara / vedi il blocco qui sotto | `criterio-locale` |
| REGISTRO_FISICA:E3 | E3 la finestra di D33 / mio / si riporta la popolazione delle due finestre nei due bracci /… | `criterio-locale` |
| REGISTRO_FISICA:E4 | E4 i diagnostici di fase / mio / max(φ) < 2π nel braccio della cura / la riserva ② di Z120.… | `criterio-locale` |
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
| REGISTRO_FISICA:S2 | passo ZERO: min distanza fra POSIZIONI = LAM (cKDTree, k=2) / è A13 misurato direttamente, e… | `criterio-locale` |
| REGISTRO_FISICA:S3 | passo ZERO: sum(d < LAM) == 0 E sum(d == LAM) == 0 / i due INSIEME: il primo da solo lo… | `criterio-locale` |
| REGISTRO_FISICA:S4 | gsmnascite == 0 al passo zero / il presidio non deve scattare. Rileva solo il passo zero, non… | `criterio-locale` |
| REGISTRO_FISICA:S5 | nodi isolati == 0 / un nodo isolato non è un nodo più semplice: è un nodo che esce dalla fisica | `criterio-locale` |
| REGISTRO_FISICA:S6 | d == /posi − posj/ per OGNI arco al passo zero / dice se la cura ha curato D02 a questo sito... | `criterio-locale` |
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
| REGISTRO_FISICA:V1 | quanto vale a, il passo tipico di rumore, misurato / è il numero che decide la condizione a <... | `criterio-locale` |
| REGISTRO_FISICA:V2 | la deriva di oggi sotto rumore simmetrico / deve riprodurre Z113: ≈ +1.582e-03 con i suoi… | `criterio-locale` |
| REGISTRO_FISICA:V3 | la deriva della proposta, stessa a, stessi d / deve essere del secondo ordine: raddoppiando a… | `criterio-locale` |
| REGISTRO_FISICA:V4 | la deriva della proposta al confine (d → LAM) / → 0, mentre quella di oggi → a/2 | `criterio-locale` |
| REGISTRO_FISICA:V5 | la deriva della proposta lontano / decade come 1/d in assoluto, 1/d² in relativo | `criterio-locale` |
| REGISTRO_FISICA:V6 | il caso che DEVE fallire: la forma exp(dx/u) / deve esplodere vicino al confine, e il test lo... | `criterio-locale` |
| REGISTRO_FISICA:V7 | mai sotto LAM: una discesa enorme, dx = −100·d / oggi attraversa; la proposta no, per… | `criterio-locale` |
| REGISTRO_FISICA:V8 | la DISTRIBUZIONE di \/dx\//d, non solo il suo tipico / è il numero che decide fra piana e Itô... | `criterio-locale` |
| REGISTRO_FISICA:V9 | quante scritture hanno \/dx\//d 1, e quante 2 / 1: Itô comprime; 2: Itô inverte il verso. Se... | `criterio-locale` |
| RI-ANCORATA | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task...… | `criterio-locale` |
| RI-ETICHETTATO | (CITATO 2 volte, MAI definito in un registro; citato solo in... [RI-ETICHETTATO] | `criterio-locale` |
| RI-GIRABILIT | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task...… | `criterio-locale` |
| RI-GIRABILITA | (CITATO 2 volte, MAI definito in un registro; citato solo in... [RI-GIRABILITA] | `criterio-locale` |
| RI-LETTO | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task... [RI-LETTO] | `criterio-locale` |
| RI-MISURA | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task... [RI-MISURA] | `criterio-locale` |
| RI-SCRIVA | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task... [RI-SCRIVA] | `criterio-locale` |
| RI-VERIFICARE | (CITATO 2 volte, MAI definito in un registro; citato solo in... [RI-VERIFICARE] | `criterio-locale` |
| RI-VERIFICATI | (CITATO 2 volte, MAI definito in un registro; citato solo in... [RI-VERIFICATI] | `criterio-locale` |
| RIDUZIONE-AL-LIMITE | (CITATO 2 volte, MAI definito in un registro; citato solo in... [RIDUZIONE-AL-LIMITE] | `criterio-locale` |
| RITMOWRAP2 | (CITATO 4 volte, MAI definito in un registro; citato solo in referti/sigilli/task...… | `criterio-locale` |
| S0 | (CITATO 6 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [S0] | `criterio-locale` |
| S1c | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [S1c] | `criterio-locale` |
| S1d | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [S1d] | `criterio-locale` |
| S1e | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [S1e] | `criterio-locale` |
| S2b | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [S2b] | `criterio-locale` |
| S6b | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [S6b] | `criterio-locale` |
| S6c | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [S6c] | `criterio-locale` |
| S7b | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [S7b] | `criterio-locale` |
| S7c | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [S7c] | `criterio-locale` |
| S7d | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [S7d] | `criterio-locale` |
| SCALE-FREE | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task...… | `criterio-locale` |
| SHAKE-THEN-FREEZE | (CITATO 2 volte, MAI definito in un registro; citato solo in... [SHAKE-THEN-FREEZE] | `criterio-locale` |
| SOVRA-CORREGGE | (CITATO 2 volte, MAI definito in un registro; citato solo in... [SOVRA-CORREGGE] | `criterio-locale` |
| STANDARD 3 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task... [STANDARD… | `criterio-locale` |
| T3a | SIGILLO scena (ii): lo STESSO seme due volte da' byte IDENTICI -- 219 firme sha1 su 219 | `criterio-locale` |
| T3b | SIGILLO scena (ii): semi DIVERSI danno reti diverse -- 99 firme su 219 cambiano | `criterio-locale` |
| T8 | (CITATO 4 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [T8] | `criterio-locale` |
| TS-1 | (CITATO 5 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| TS-2 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| TS-3 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| TS-4 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| TS-5 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| TS-6 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| TW-1 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| TW-2 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| TW-3 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| TW-4 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| TW-5 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| TW-6 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| U7 | (CITATO 10 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) | `criterio-locale` |
| U7a | (CITATO 8 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [U7a] | `criterio-locale` |
| V0 | (CITATO 7 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [V0] | `criterio-locale` |
| V1b | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [V1b] | `criterio-locale` |
| VALORE-NULL | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task...… | `criterio-locale` |
| VERIFICATA-SP | (CITATO 1 volte, MAI definito in un registro; citato solo in... [VERIFICATA-SP] | `criterio-locale` |
| W1 | (CITATO 8 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [W1] | `criterio-locale` |
| W3 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [W3] | `criterio-locale` |
| X0 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [X0] | `criterio-locale` |
| X4 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [X4] | `criterio-locale` |
| X5 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [X5] | `criterio-locale` |
| X6 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [X6] | `criterio-locale` |
| X7 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [X7] | `criterio-locale` |
| Y5a | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [Y5a] | `criterio-locale` |
| Y5b | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [Y5b] | `criterio-locale` |
| Y5c | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [Y5c] | `criterio-locale` |
| Z0 | (CITATO 10 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [Z0] | `criterio-locale` |
| Z146 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| Z2b | (CITATO 5 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [Z2b] | `criterio-locale` |
| Z4c | (CITATO 4 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [Z4c] | `criterio-locale` |
| Z4d | (CITATO 4 volte, MAI definito in un registro; citato solo in referti/sigilli/task history) [Z4d] | `criterio-locale` |
| Z888 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| ZZ888 | (CITATO 2 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |
| ZZ999 | (CITATO 3 volte, MAI definito in un registro; citato solo in referti/sigilli/task history)… | `criterio-locale` |

### motivo: **gia' curata o chiusa**   *(151 voci)*

| id | che cos'e' | tipo |
|---|---|:--:|
| A1-INERZIA | INERZIA VALE SEMPRE ⏳[EPOCA 1 · CODICE] / Teorema di inerzia — lo Strato 0 e' inerte: la... | `misura` |
| A1-TREVIE | la catena a TRE VIE di step — if CHICORE… / elif VERSOCHI… / elif not(…) / :3623 · :3626 ·… | `altro` |
| A2-ANELLO | l'anello A6 di Z70 — periodo 2, via chiralitacorelocale/CHICORE / doc/RAMIFICAZIONI.md Z70 /... | `altro` |
| A2-BLOCH | BLOCH VALE SEMPRE ⏳[EPOCA 1 · CODICE] / Invarianza del Bloch sotto Step 2 — phc e' una fase... | `misura` |
| A3-CHIRALE | Z71 — la carica chirale non si conserva / doc/RAMIFICAZIONI.md Z71 / APERTA. I due punti di... | `altro` |
| A3-FDT | FDT VALE SEMPRE ⏳[EPOCA 1 · CODICE] / FDT del solo scuotimento — il drift di n →... | `misura` |
| A5-PANNELLO | il PANNELLO FEDELE (interpolazione di psi accanto a campospaziale) / la ex-LISTA 3 di questo... | `altro` |
| A6-PERCCHI | percchi FA DUE LAVORI CON REGOLE OPPOSTE: chibasc lo tratta da CHIRALITA', TEMPOSEGNO da… | `altro` |
| ARCH-LCONSERVA | _togli_rotazione_rigida esce dal simulatore; L_CONSERVA diventa un no-op accettato | `cura` |
| ARCH-PAVIMENTI | i pavimenti morti (_floor_d0, _pav_d0, i due 0.05 su d) escono dal simulatore | `cura` |
| ARCH-SYNC | SYNC_UPDATE e i suoi rami escono dal simulatore; --sync diventa un no-op accettato | `cura` |
| B1 | Z47 — pos nella fisica: l'ultimo SFONDO / doc/RAMIFICAZIONI.md Z47, doc/ASSIOMI.md / NON... | `altro` |
| B10 | --override-blob e la COPIA del driver / csv/testfork/scenavideoripresa.py (e68bb8c5, 17466… | `altro` |
| B2 | Z31 — i sigilli non ri-girabili / Z31, citata in 17 file / rifatta TRE volte, l'ultima ieri /… | `altro` |
| B3 | i rami di memoriahebbianamoto / solitonsimulator.py:4616-4918 / mai guardati / sono 25, non… | `altro` |
| B4 | i np.zeros / tutto il simulatore / mai guardati / sono 116, non 10. Il numero utile non è... | `altro` |
| B4-FROZEN | FROZEN VALE SEMPRE ⏳[EPOCA 1 · CODICE] / Bloch frozen-o-noise / senza scuotimento \/<n\/ =... | `misura` |
| B5 | theta / l'aliasing del settore di spin / CLAUDE.md §9, registro C14, fronte A / aperto e noto... | `altro` |
| B5-KURAMOTO | KURAMOTO VALE SEMPRE ⏳[EPOCA 1 · CODICE] / Kuramoto refutato / K-frozen byte-identico a OFF... | `misura` |
| B6-TURBO | TURBO VALE SEMPRE ⏳[EPOCA 1 · MISURA] / Esito B del turbo — con cs al 5 % di CSM lo Step 2… | `misura` |
| B8 | IL BLOCCO DEL RUN A 6000 AL PASSO 2700 / doc/REFERTObloccorun6000.md (131 righe)... | `altro` |
| C1 | C1 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / ESITO (I): nessun bug. omega = coppia/inerzia porta... | `misura` |
| C10 | C10 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / LA BARRA D'ERRORE USATA FINORA E' TRE VOLTE TROPPO... | `misura` |
| C11 | C11 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / psispinprec non era esteso alla mitosi ⇒ la guardia… | `misura` |
| C14 | C14 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / ESITO (A) sui QUATTRO BRACCI — nessuna firma emerge… | `misura` |
| C15 | C15 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / La firma di /<n/ che «pendeva» È CHIUSA come rumore.... | `misura` |
| C16 | C16 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / ESITO (I) CONFERMATO QUATTRO VOLTE, con la barra… | `misura` |
| C19 | C19 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / CHIUSO il 2026-09-16: le due convenzioni di theta ora... | `misura` |
| C2 | C2 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / Il −1 e' cancellato da √tau, con tau ∝ rho^1.81 / +1.176… | `misura` |
| C25 | C25 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / UN FILE NON SI PUO' COMMITTARE PER IL SUO ESSERE CRLF:… | `misura` |
| C26 | C26 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / VERSOCHI E' UN NO-OP SILENZIOSO SOTTO CHICORE, che e'... | `misura` |
| C27 | C27 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / TRE FLAG VIVONO DENTRO if VIRIALE: E NON LO DICHIARANO.... | `misura` |
| C28 | C28 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / 14 FLAG SU 16 NON HANNO ALCUN SIGILLO. Tier 2 (metrica)… | `misura` |
| C3 | C3 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / Il residuo di 0.34 e' TRANSITORIO, non un termine… | `misura` |
| C4 | C4 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / inerzia = T² — chiude il buco dimensionale; esponente… | `misura` |
| C5-INVARIANTI | INVARIANTI — 42 domini, due livelli / mandato C5 / 3/3 (Z100); accesi di default | `cura` |
| C6 | C6 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / Il rumore non guida omega / Rstoc = 0.041, sotto… | `misura` |
| C7 | C7 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / La cache csnodoprev veniva scartata a ogni mitosi ⇒ nel… | `misura` |
| C8 | C8 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / LA FASE 2 NON SI CHIUDE. Col tempo-luce cablato la… | `misura` |
| C9 | C9 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / --tau-luce ha un effetto GRANDE sulla pendenza (che… | `misura` |
| CTRL-RISCELTA | i punti di controllo si RISCEGLIEVANO a ogni checkpoint: l'osservabile della PROVA 1 andava a… | `difetto` |
| CURA2-STRUTTURALE | la CURA 2 diventa STRUTTURALE: i rami `else` di TEMPO_UNICO_MITOSI escono dal simulatore… | `altro` |
| D02 | pozzografo calcola L da self.pos — IL DISEGNO — mentre il suo docstring dichiara «la distanza... | `difetto` |
| D11 | d scende DIECI VOLTE sotto LAM mentre SCALAMIN e' acceso, e la causa NON e' trovata / Z87 /… | `difetto` |
| D16 | SCALAMIN frenava OGNI scrittura separatamente: il risultato dipendeva dall'ORDINE delle leggi… | `difetto` |
| D17 | peq diventava NEGATIVO e il pavimento max(peq, 1e-9) NE RIBALTAVA IL SEGNO (da -3.72 a… | `difetto` |
| D18 | COESADIM leggeva ISTANTI MISTI e il suo tetto era GLOBALE / Z92 · A5 / COESCAUSALE (C4) / CURATO | `difetto` |
| D19 | OTTO grandezze che la semina legge erano INERTI SUL VUOTO in ogni run di epoca 1 / Z88 / la… | `difetto` |
| D22 | Il DENOMINATORE PER GRADO: la misura non distingue (A) da (B), ma (B) cade per DIMOSTRAZIONE,… | `difetto` |
| D32 | I TEMPI PROPRI DICHIARATI SONO TRE, E SONO TRE GRANDEZZE DIVERSE: r, taupp e d/cs. corr(r... | `difetto` |
| D34 | D34 CURATO IN CODICE il 2026-09-24 / Il wrap «a 4π» di ritmo() (:2584-2585) NON AVVOLGE: su... | `difetto` |
| D37 | D37 CURATO il 2026-09-24 / CHIAVE DUPLICATA NEI DOMINI: 'csnodoprev' compare DUE VOLTE (:226… | `difetto` |
| DRIVER-SCENA-II | APERTA il 2026-09-26 (rilievo di Luca) / IL DRIVER NON SA FARE LA SCENA (ii), e sono QUATTRO... | `difetto` |
| ETC-C1-CONFINE | cura (c) pezzo 1: la fotografia si apre a inizio PASSO PIENO, non di step, e idempotente | `cura` |
| ETC-PASSO | LA CURA (a): il passo diventa SINCRONO -- fotografia a inizio passo, commit a fine passo | `cura` |
| ETICHETTA-A13 | l'etichetta sbagliata `A13` dove la regola e' `A3-DISEGNO`: corretta nei documenti, non… | `altro` |
| INERZIA-1(C) | 1(C) — CURATA e SIGILLATA 3/6 il 2026-09-25: GIUSTA e INSUFFICIENTE / LA CURA TOGLIE… | `altro` |
| LETTORI-INDICE | CHIUSA il 2026-09-26 (decisioni di Luca) / ESITO: 1 RITIRATO, 1 CONVERTITO, 4 FUORI PERIMETRO… | `altro` |
| MASSA-ID-FISSO | MASSA-ID a LIGNAGGIO FISSO: non applicabile, la precondizione V-PRE non regge (i nati toccano… | `misura` |
| MAX-NODI-FERMA | MAX_NODI e' una guardia di MEMORIA che oggi cambia la FISICA in silenzio: deve FERMARE il run | `cura` |
| MITOSI-NON-DIVISA | la mitosi NON si spezza per TIPO restando byte-identica: struttura e stato si alternano 26 volte | `misura` |
| OKN-ASSERT | CHIUSA il 2026-09-26, a run finito (residuo rilevato da Luca) / UN getattr(..., default) CHE... | `altro` |
| OSSERVABILE-P1 | APERTA il 2026-09-26 (rilievo di Luca) / NON ESISTE UNO STRUMENTO UFFICIALE PER LA DISTANZA… | `difetto` |
| P1BIS-DELTA | in coda per la LISTA CHIUSA, famiglia G (ordine di Luca, 2026-09-25) / P1-bis VERIFICA LA... | `altro` |
| POTENZE-1 | CHIUSA il 2026-09-26 con la CURA A (rhos/W^2), sigillo 6/6: F2 da x47 000 a x1.4, F1 2.427... | `altro` |
| POZZO-D | la cura di D02 (flag `POZZO_D` nel codice): nel pozzo del grafo `L` viene da `self.d` e non da… | `altro` |
| RAMPA-1 | CHIUSA il 2026-09-25, strada (3) (decisione di Luca): sigillo 9/9 dal CLI, ramp =... | `altro` |
| RIORDINO-NOMI-H | il prefisso `H-` e' sui NOMI VECCHI (H-P3) e non sui nomi semantici (H-CLI) che la proposta... | `altro` |
| RIORDINO-POSTO2 | IL POSTO 2 HA 11 REGOLE E IL TETTO E' 10: quale si fonde | `fronte` |
| RIPIEGO-1 | APERTA E CHIUSA il 2026-09-25 (difetto mio, rilevato da LUCA) / UN RIPIEGO GLOBALE SU UNA... | `altro` |
| SCENA-1 | CHIUSA il 2026-09-25, strada (1) (decisione di Luca) / SEMINALAM era approvata ma… | `altro` |
| SCHED-T1 | T1 dello schedulatore: la composizione e' una LISTA e c'e' UN SOLO esecutore, esegui_passo | `cura` |
| SCHED-T2-TIPI | T2 (i tipi): gli 8 tipi del registro del passo, e dopo L_CONSERVA sono coerenti 8 su 8 | `cura` |
| SCHED-T2-VALIDA | T2: esegui_passo VALIDA la composizione -- apri primo, coda fissa, registro, nessun doppio | `cura` |
| T4-TAUTOLOGICO | il collaudo T4 della scomposizione non puo' fallire: D_interni e' zero per identita' algebrica | `difetto` |
| X1 | X1 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / TEMPOPROPRIOORIENTATO: il principio e' giusto, ma dtn <… | `fronte` |
| X3 | X3 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / AUDIT DI LETTURA DELLE LEGGI — registrato (2026-09-16) /... | `fronte` |
| Y2 | Y2 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / Due osservabili U(1) hanno il nullo SBAGLIATO o NON... | `fronte` |
| Z10 | Z10 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / TAUA E' UN SOLO NUMERO PER DUE LEGGI FISICHE DISTINTE —... | `fronte` |
| Z100 | Z100 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / INVARIANTI (C5): il programma si ferma quando una... | `fronte` |
| Z102 | Z102 CHIUSA PER MISURA ⏳[EPOCA 3 · MISURA] / CHI FA SCAPPARE d0: E' IL FRENO DELLA SCALA… | `fronte` |
| Z103 | Z103 CHIUSA PER MISURA ⏳[EPOCA 3 · MISURA] / IL POZZO GRAVITAZIONALE USA IL DISEGNO, E IL SUO... | `fronte` |
| Z105 | Z105 CHIUSA PER MISURA ⏳[EPOCA 3 · MISURA] / DOVE SPINGE LA GRAVITA': TUTTO IL SALDO NETTO DI... | `fronte` |
| Z106 | Z106 CHIUSA PER MISURA ⏳[EPOCA 3 · MISURA] / GLI ARCHI PIU' SPINTI DA S09 NON SONO UNA CODA... | `fronte` |
| Z107 | Z107 CHIUSA PER MISURA ⏳[EPOCA 3 · MISURA] / LA GRAVITA' NON E' IL MOTORE DELLA FUGA DI d0... | `fronte` |
| Z108 | Z108 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / IL BILANCIO DI d0 CHIUDE, E IL MOTORE… | `fronte` |
| Z109 | Z109 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / LA MEMORIA DEL MOTO NON E' IL MOTORE… | `fronte` |
| Z11 | Z11 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / RIGIRO DEI SIGILLI STORICI — lavoro PREVISTO, non… | `fronte` |
| Z110 | Z110 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / r E taupp SONO DUE GRANDEZZE DIVERSE… | `fronte` |
| Z111 | Z111 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / LA REPULSIONE ALLA MASSIMA… | `fronte` |
| Z112 | Z112 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / L'IPOTESI DELLA COMPRESSIONE REGGE… | `fronte` |
| Z113 | Z113 CHIUSA PER DIMOSTRAZIONE + MISURA / IL CRICCHETTO DEL FRENO E' CONFERMATO SU RUMORE... | `fronte` |
| Z114 | Z114 CHIUSA PER DIMOSTRAZIONE / GLI SCRITTORI DI d0 NON TRACCIATI SONO DUE, NON TRE: init… | `fronte` |
| Z115 | Z115 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / G4-bis: SPEGNERE L'INTERO BLOCCO FA... | `fronte` |
| Z116 | Z116 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / I TRE BRACCI: 6/8 · 7/8 · 6/8. E... | `fronte` |
| Z117 | Z117 CHIUSA PER DIMOSTRAZIONE + MISURA / IL WRAP «A 4π» DI ritmo() NON AVVOLGE NIENTE: su… | `fronte` |
| Z118 | Z118 CHIUSA PER DIMOSTRAZIONE / IL CENSIMENTO DELLE FASI: 52 punti, 38 gravi. E IL NUMERO CHE... | `fronte` |
| Z119 | Z119 CHIUSA PER DIMOSTRAZIONE + MISURA / L'ANTIPARTICELLA DI SCHWINGER NASCE CON +2π, E NEL... | `fronte` |
| Z120 | Z120 CHIUSA PER DIMOSTRAZIONE / LA VERIFICA DI B1: NESSUNA RIGA DELLA FISICA DISTINGUE φ DA φ… | `fronte` |
| Z121 | Z121 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / φ NON E' L'AZIMUT DEL VETTORE DI… | `fronte` |
| Z122 | Z122 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / I TEMPI PROPRI DICHIARATI NON SONO… | `fronte` |
| Z123 | Z123 CHIUSA PER MISURA ⏳[archivi delle cure · MISURA] / LA PROVA DI RITMOWRAP2PI: 6/8 COME... | `fronte` |
| Z124 | Z124 CHIUSA PER MISURA ⏳[archivi delle cure · SIGILLO] / IL SIGILLO DI FASE2PI: 6/6 PASS, e… | `fronte` |
| Z134 | Z134 CURA IN CODICE ⏳[archivi delle cure · CURA] / CURA 1 — L'OROLOGIO: RITMOWRAP2PI APPROVATA… | `fronte` |
| Z135 | Z135 CHIUSA PER MISURA ⏳[archivi delle cure · PROVA] / LA PROVA DI CURA 1: la mitosi NON… | `fronte` |
| Z136 | Z136 CHIUSA PER DIMOSTRAZIONE ⏳[archivi delle cure · CONTROLLO DI LUCA] / LE DUE STRADE DELLA... | `fronte` |
| Z14 | Z14 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / IL TERZO RAMO DI calcolapsi (elif sotto REPULSLEGGE)... | `fronte` |
| Z144 | Z144 CURA IN CODICE ⏳[archivi delle cure · CURA] / E4-LAM PASSA 6/6: la legge d = LAM si... | `fronte` |
| Z145 | CHIUSO — T5 del sigillo di CURA 2 era invalido: dv 0 letto come effetto (2026-09-24) | `fronte` |
| Z16 | Z16 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / Y5 ROSSO: la causa e' rhosorgente <= 0, NON peq. E… | `fronte` |
| Z19 | Z19 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / QUARTA VOLTA: una grandezza letta in un momento del… | `fronte` |
| Z2 | Z2 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / spinta: A2 e A3 sono stati tolti, A1 NO (2026-09-17) /… | `fronte` |
| Z20 | Z20 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / UN DRIVER CHE FORZA UN FLAG IN TUTTI I BRACCI RENDE… | `fronte` |
| Z22 | Z22 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / REGOLA 9 — par.5-quinquies ESISTEVA, ed e' stato… | `fronte` |
| Z31 | Z31 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / QUATTRO SIGILLI NON SONO PIU' RI-GIRABILI: il loro… | `fronte` |
| Z40 | Z40 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / A2 E' VIOLATO DA Lam = mean(I), E LA VIOLAZIONE E' LA... | `fronte` |
| Z47 | Z47 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / PROGETTO DI LUNGO PERIODO — NON INIZIATO. GEOMETRIA... | `fronte` |
| Z54 | Z54 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / CHIUSA — L'ARCHIVIO A SERIE: --db-serie +... | `fronte` |
| Z55 | Z55 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / APERTA — PERCHE' NELLA RIGIOCATA LA STRINGA "schwinger"... | `fronte` |
| Z58 | Z58 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / L'IPOTESI DELLA PORTATA CADE — lambdanodi… | `fronte` |
| Z59 | Z59 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / L'INERZIA AL PAVIMENTO CRESCE, e il CUMULATO SOTTOSTIMA… | `fronte` |
| Z6 | Z6 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / IL TRANSITORIO DI ACCENSIONE E' UN BLOCCO STRUTTURALE —… | `fronte` |
| Z61 | Z61 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / LE DUE FINESTRE A 6 PASSI: ritmo() NON NASCE... | `fronte` |
| Z62 | Z62 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / L'EVENTO DEL PASSO 198 NON E' UN ARTEFATTO... | `fronte` |
| Z63 | Z63 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / NE' REDISTRIBUZIONE NE' RIDUZIONE: IL FONDO… | `fronte` |
| Z65 | Z65 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / NESSUNA DELLE QUATTRO LETTURE: IL GRAFO E'… | `fronte` |
| Z67 | Z67 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / scalap CURATA: il punto fisso e' SCIOLTO, e... | `fronte` |
| Z68 | Z68 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / PASSO 2: la diagnosi era SBAGLIATA -- non e' la... | `fronte` |
| Z7 | Z7 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / fattcsultimo e' SCRITTO e MAI LETTO — quarto caso della... | `fronte` |
| Z70 | Z70 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / L'ANELLO A6 FRA CHIRALITA' E TORSIONE: C'E', MA NON E'... | `fronte` |
| Z71 | Z71 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / A7 -- LA CARICA CHIRALE NON SI CONSERVA, E IL PUNTO E'… | `fronte` |
| Z72 | Z72 🟨VALE PER QUELLA SCENA ⏳[EPOCA 1 · MISURA] / PHICRIT = 2pi REGGE, e la ragione e'... | `fronte` |
| Z75 | Z75 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / nsub GOVERNA IL COSTO DELL'INTERO SISTEMA ED E'... | `fronte` |
| Z76 | Z76 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / I NATI HANNO GRADO 2 E SONO LA MAGGIORANZA DEL SISTEMA:… | `fronte` |
| Z77 | Z77 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / LA TENSIONE NASCE DAL DENOMINATORE: d0 CROLLA A SCATTI... | `fronte` |
| Z78 | Z78 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / d0 HA DIECI SCRITTORI E NESSUNO E' CONTATO — e i due... | `fronte` |
| Z79 | Z79 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / d0 NON E' MOSSO DALLA COESIONE: E' MOSSO DAL SUO CLIP —… | `fronte` |
| Z8 | Z8 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / Lo 0.3457 % di nodi ancora al pavimento 1e-6 NON e'... | `fronte` |
| Z80 | Z80 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / IL CLIP DI d0 PROTEGGE, NON PRODUCE:… | `fronte` |
| Z81 | Z81 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / IL FRATELLO S09 NON E' DEL TUTTO CAUSALE: clippa a ±c·DT… | `fronte` |
| Z83 | Z83 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / DOMANDA APERTA: d0 DEVE STARE SOPRA LAM? Il sistema… | `fronte` |
| Z84 | Z84 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / E' cs^2lap CHE ALLUNGA L'ARCO — la TENSIONE DEI VICINI... | `fronte` |
| Z85 | Z85 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / I LETTORI DI percchi, CENSITI DAL DISCO: la catena… | `fronte` |
| Z86 | Z86 VALE SEMPRE ⏳[EPOCA 2 · CODICE] / IL CRITERIO Z4a DEL SIGILLO DEL RAMO D ERA SBAGLIATO, E... | `fronte` |
| Z93 | Z93 CHIUSA PER MISURA ⏳[EPOCA 2 · MISURA] / L'ARCO DELL'INNESCO E' 2773-4158, NATO-NATO -- ED… | `fronte` |
| Z94 | Z94 CHIUSA PER MISURA ⏳[EPOCA 2 · MISURA] / peq DIVENTA NEGATIVO, E IL PAVIMENTO max(peq,… | `fronte` |
| Z95 | Z95 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / PEQESATTO (C1): il rilassamento di peq in forma... | `fronte` |
| Z96 | Z96 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / PEQNASCITALOCALE (C2): UNA SOLA legge di nascita… | `fronte` |
| Z97 | Z97 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / SCALAMINPASSO (C3): il freno UNA VOLTA PER PASSO.… | `fronte` |
| Z98 | Z98 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / COESCAUSALE (C4): un solo ISTANTE e il CONO DEL... | `fronte` |
| Z99 | Z99 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / ANOMSIMM (C1-bis): il pavimento max(peq, 1e-9) E'… | `fronte` |

### motivo: **sospetto, NON acclarato: si promuove con la prova**   *(18 voci)*

| id | che cos'e' | tipo |
|---|---|:--:|
| CENS-B1 | [B] *"`SPINORE_VIVO = True` **NON E' MAI STATO VALIDATO COME DEFAULT** ... | `sospetto` |
| CENS-B10 | [B] *"**ESPLORATIVO**: lega la creazione di coppia anche all'anomalia di d | `sospetto` |
| CENS-B11 | [B] tre osservabili di controllo nominate una per una -- *"esponente di sc | `sospetto` |
| CENS-B12 | [B] *"KERNEL BILANCIATO DAL TEMPO PROPRIO (tau^alpha) **SEMPRE ATTIVO** .. | `sospetto` |
| CENS-B13 | [B] *"`inerzia = np.maximum(_contrasto * _T2, 1e-6)` -- **il pavimento RES | `sospetto` |
| CENS-B14 | [B] l'osservabile e' calcolata (`m0_spin_core`, `m0_spin_core_disp`); `Che | `sospetto` |
| CENS-B15 | [B] il **condizionale** scritto nel commento: *"Un esito positivo va letto | `sospetto` |
| CENS-B16 | [B] (1) INVENTARIO e (2) README sono prescritti *"nello stesso commit del | `sospetto` |
| CENS-B2 | [B] ON di default *"PER DECISIONE DI LUCA E SU BASI DI FORMA, **NON** perc | `sospetto` |
| CENS-B3 | [B] *"IN VERIFICA"*, e nel corpo: *"stabile, ma **il guadagno sul decadime | `sospetto` |
| CENS-B4 | [B] *"costanti temporali TAU_P/TAU_BG/TAU_TW come RAPPORTI adimensionali . | `sospetto` |
| CENS-B5 | [B] *"**Da validare su TEMPI LUNGHI** (hardware di Luca): taglia stabile e | `sospetto` |
| CENS-B6 | [B] *"**DA RIPRENDERE**: seme iniziale di asimmetria strutturale (fase/tor | `sospetto` |
| CENS-B7 | [B] *"Default ancora off; **convergenza e superiorita' rispetto al percors | `sospetto` |
| CENS-B8 | [B] *"INTEGRATORE METRICO **SPERIMENTALE** ... Default off per mantenere i | `sospetto` |
| CENS-B9 | [B] *"LEGGE DI STABILITA' (**esplorativa**): i nuovi nodi in regione sovra | `sospetto` |
| PSI-FLASH | /psi/ SALTA di 1.6x nei passi con nascite: due siti ricalcolano psi dopo la mitosi, nello… | `sospetto` |
| SCIOGLIMENTO-FASE | perche' coer_campo va da 0.999 a 0.20 in 120 passi: la scena non tocca phivel e la coppia non… | `sospetto` |

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
| A3c | un RAPPORTO confrontato con un MASSIMO / (115, accanto a due massimi di passi diversi) /... | `assioma` |
| A4 | STRATIFICAZIONE CAUSALE | `assioma` |
| A5 | CAUSALITA' DELLA MEDIAZIONE | `assioma` |
| A6 | INERZIA (TEOREMA, non assioma) | `assioma` |
| A7 | CONSERVAZIONE E STATO | `assioma` |
| A7b | COROLLARIO: uno stato non nasce indefinito (aggiunto 2026-09-17) | `assioma` |
| A8 | UN RAMO SILENZIOSO NON E' UN RAMO | `assioma` |
| A8b | COROLLARIO: le cache CROSS-PASSO | `assioma` |
| A9 | UN PRESIDIO CHE NON IMPEDISCE NON E' UN PRESIDIO | `assioma` |

### motivo: **teoria: assioma, standard o corollario**   *(16 voci)*

| id | che cos'e' | tipo |
|---|---|:--:|
| H-INDICE | PRESIDIO DEL HOOK: un ID citato in un documento vivo o nel messaggio che non e' nell'indice | `presidio` |
| H-P1-bis | PRESIDIO DEL HOOK: un referto committato senza toccare la relazione | `presidio` |
| H-P3 | PRESIDIO DEL HOOK: un sigillo che configura il modulo A MANO invece di passare dal CLI | `presidio` |
| H-P5 | PRESIDIO DEL HOOK: un referto che non dichiara la configurazione INTERA | `presidio` |
| H-P7 | PRESIDIO DEL HOOK: un flag il cui commento cambia senza nominare quel flag | `presidio` |
| H-P8 | PRESIDIO DEL HOOK: un confronto che prende il codice di prima da HEAD invece che dal PADRE | `presidio` |
| H-P9 | PRESIDIO DEL HOOK: uno strumento che fa avanzare una rete con net.step() invece di passo_pieno | `presidio` |
| H-REG-R | PRESIDIO DEL HOOK: una legge che cambia senza la sua scheda in REGISTRO_FISICA | `presidio` |
| H-RIGHE | PRESIDIO DEL HOOK: CLAUDE.md oltre le 400 righe | `presidio` |
| H-VALIDATORE | PRESIDIO DEL HOOK: un indice mal formato o con una voce persa rispetto al tag | `presidio` |
| L-DOPO-STOP | DOPO UNO STOP, se Luca non risponde si lavora SOLO la coda: nessuna cura fisica, nessun run... | `presidio` |
| L-NUMERI | OGNI NUMERO SCRITTO IN UN COMMIT O IN UN REFERTO ESCE DA UNO SCRIPT | `presidio` |
| L-PATCH | LE PATCH SI LANCIANO IN PRIMO PIANO; niente git stash con una patch in corso; nei patch… | `presidio` |
| L-UN-PROMPT | UN PROMPT ALLA VOLTA: i rilievi che arrivano durante un lavoro vanno in CODA | `presidio` |
| P1-bis | LA RELAZIONE SI SCRIVE NELLO STESSO COMMIT DEL RISCONTRO | `presidio` |
| P1-quater | OGNI SOSTITUZIONE DI TESTO SI ASSERISCE PER SE', MAI IN BLOCCO | `presidio` |

### motivo: **non e' un difetto**   *(8 voci)*

| id | che cos'e' | tipo |
|---|---|:--:|
| COPPIA-RAMP | APERTA il 2026-09-26 / PERCHE' LA COPPIA NON PORTA ramp? Misurato sui figli (2 semi, media... | `misura` |
| D09 | chibasc BLOCCA la mitosi e DIMEZZA l'olonomia netta: fa l'OPPOSTO del suo scopo dichiarato /... | `difetto` |
| D27 | Il grafo e' in QUATTRO COMPONENTI che non si toccano mai / Z65, misurato in ORIGINE su un… | `difetto` |
| HASHSEED-RIPROD | FALSO ALLARME: PYTHONHASHSEED non cambia lo stato del simulatore (23/23 identiche) | `difetto` |
| NODI-1 | RITIRATA (Luca, 2026-09-25). NON cancellata: resta come storia, col motivo. PERCHE' È CADUTA,… | `altro` |
| S10 | S10 RITIRATA il 2026-09-24 / Il tetto 1.414213 di r viene da un ramo di ritmo() che NON GIRA /… | `altro` |
| Z130 | Z130 SOSPETTO RITIRATO, MIO ⏳[archivi delle cure · LETTURA] / S10 E' RITIRATA: la premessa… | `fronte` |
| Z73 | Z73 RITIRATA ⏳[EPOCA 1 · MISURA] / RITIRATA UNA SECONDA VOLTA il 2026-09-20, e la smentita… | `fronte` |

### motivo: **standard di prova: un criterio di metodo, non un fronte**   *(6 voci)*

| id | che cos'e' | tipo |
|---|---|:--:|
| L-SOGLIA | UNA SOGLIA NON SI CALCOLA DAI DATI CHE GIUDICA, e si collauda sul caso nullo | `standard` |
| P1-sexies | UN CRITERIO SI COLLAUDA SU UN CASO A RISPOSTA NOTA, e il caso che DEVE fallire e' il piu'… | `standard` |
| STANDARD 10 | STANDARD 10 — UNA CURA NON AUMENTA IL NUMERO DELLE LEGGI (criterio di Luca, 2026-09-25) | `standard` |
| STANDARD 4 | SNAPSHOT CONTRO SNAPSHOT, ALLO STESSO ISTANTE | `standard` |
| STANDARD 6 | OGNI DIFETTO ACCLARATO SI REGISTRA SUBITO NELLA CODA UNICA | `standard` |
| STANDARD 8 | UN DIFETTO DIMOSTRATO SI CURA: MISURARE NON E' CURARE | `standard` |

---

## ⚠ **VOCI SENZA ID: LA PERDITA DICHIARATA DI QUESTA VISTA**

**Nell'indice entrano solo le voci CON UN ID.** Queste **non ne hanno**, quindi **non possono
comparire qui** — e lo scrivo **prima** dei numeri, invece di lasciarle sparire:

**✅ NESSUNA: dal 2026-09-26 l'elenco e' VUOTO.** `MITOSI-TASSO` e `CURA-3` — le due voci
che vivevano senza etichetta — **hanno un ID**, e compaiono. **Il controllo resta: se
l'elenco CRESCE, il generatore si ferma.**

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
| DRIVER-SCENA-II | ✅ |
| OSSERVABILE-P1 | ✅ |
| MITOSI-TASSO (era una voce PERSA) | ✅ |
| CURA-3 (era `CURA 3`, con lo spazio) | ✅ |
| D02 | ✅ |
| D03 | ✅ |
| D09 — la voce che NON torna | ✅ |
| D31 | ✅ |
| chi comprime d0 | ✅ |
| **voci PERSE dichiarate** | 0 |

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
