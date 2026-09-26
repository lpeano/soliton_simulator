# IL PUNTO DELLA SITUAZIONE — **generato dalla CODA UNICA**

> **SOLA LETTURA.** Generato da `csv/_punto_della_situazione.py` leggendo
> `doc/STATO_RUN.md`. **Non e' scritto a memoria**, ed e' il punto: **se un task manca
> qui, manca dalla coda** — e quello e' il difetto da correggere.

## CON RISERVA — 3

| id | cosa | ultimo commit che lo nomina |
|---|---|---|
| **`V`** | **VALIDAZIONE a 600 passi** | `69a78f7 17:09` |
| **`B8`** | **⚠ IL BLOCCO DEL RUN A 6000 AL PASSO 2700** | `4a5d085 20:33` |
| **`B10`** | **⚠ `--override-blob` e la COPIA del driver** | `f6d432c 12:45` |

## IN CODA — 13

| id | cosa | ultimo commit che lo nomina |
|---|---|---|
| **`G4-MEMARCO`** | **`MEM_ARCO` — LA MEMORIA DEL MOTO TRADOTTA IN FORMA RELAZIONALE** *(aggiunta di Luca al §4, 2026-09-22)* | `010809a 13:57` |
| **`SCALE-TW`** | **LE SCALE DELLA TORSIONE: un'analisi completa, DA CAPO** | `7935806 17:03` |
| **`PROBLEMI-CHK3`** | **IL PIANO DEI PROBLEMI APERTI** — per ciascuno: **la domanda da chiudere · la misura o derivazione che la chiude · da che scheda dipende · cosa blocc | `1fce1b5 13:20` |
| **`FAMIGLIE`** | **IL CERCATORE DI FAMIGLIE DI DIFETTI** — uno strumento che legge il sorgente *(AST)* e segnala i punti che ricadono nelle famiglie **gia' note**, cia | `0f4383b 11:34` |
| **`FASCE-TAU`** | **LA CRESCITA E' COORDINATA COL TEMPO PROPRIO?** — l'espansione non dev'essere omogenea in senso **assoluto**, ma omogenea **DENTRO UNA FASCIA DI TEMP | `1fce1b5 13:20` |
| **`CHK3`** | **CHECKPOINT: referto dei quattro esiti, ciascuno contro le sue letture fissate PRIMA** | `1fce1b5 13:20` |
| **`CHK3-D`** | **Nel referto del `CHK3`, la sezione «I DIFETTI NUOVI CONTRO LE MISURE GIA' FATTE»** — `D27` *(quattro componenti)* e `D25` *(il tempo che non scorre) | `944064a 13:06` |
| **`PAT-1`** | **`_dove_spinge_la_gravita.py` non rispetta il pattern `5`** *(nessun CONTROLLO DELL'INVOLUCRO)* | `bf8aaad 17:45` |
| **`PROVE`** | **LE TRE PROVE DELL'IPOTESI DELLA GRAVITA' A SPINTA** — ① due masse si avvicinano? ② con che legge? ③ tutti i corpi cadono uguale? | `7935806 17:03` |
| **`C5RES-INVARIANTI`** | **I RESIDUI DI `C5`** — **`I4`** la scatola nera *(rigiocare da solo il passo in cui scatta un invariante)*, **`I5`** la tabella degli underflow **per | `f6d432c 12:45` |
| **`REG-C`** | **FASE C: LA STORIA** di ogni legge, e le schede delle leggi TOLTE | `—` |
| **`REG-R`** | **LA REGOLA MANTENUTA del registro della fisica** — la riga in `CLAUDE.md` *(«nessuna legge fisica entra, cambia o esce dal simulatore senza passare d | `a2a6053 19:20` |
| **`REG-V`** | **`_verifica_registro.py`**: completezza, esistenza, coerenza con la traccia di `d0` e col registro dei domini di `C5` | `—` |

## (senza marcatore) — 23

| id | cosa | ultimo commit che lo nomina |
|---|---|---|
| **`S-MIT2`** | **LA FINESTRA DI CREAZIONE DELLA MITOSI, MISURATA DAL CODICE:** `avv ∈ (1.500, 1.750) · PHI_CRIT`, cioè una **banda larga `1/6` della soglia**. **Sopr | `1d618da 08:40` |
| **`FRAG1`** | **`mitosi()` SU UNA RETE SENZA CAMPO VA IN `IndexError` INVECE DI DICHIARARLO.** `I = self._rho_sorgente()` è **vuoto** finché non è girato un `step() | `4a76517 15:00` |
| **`A1-COSTANTI`** | **AUDIT DELLE COSTANTI TARATE** — **`~90` commenti «misurato/tarato»** nel sorgente. Si separano le **COSTANTI TARATE** *(es. `389/484` della massa cr | `f6d432c 12:45` |
| **`A2-DXD`** | **RIMISURARE NEL REGIME NUOVO:** `\ | `f6d432c 12:45` |
| **`I1`** | **IDEA DI LUCA, per dopo:** costruire **UNA** massa, **farla maturare**, leggerne la struttura **sul grafo** e **REPLICARLA come modello** per le tre  | `c5e1788 08:12` |
| **`PAT-2`** | **`_spegni_grav_bifase.py:184` non rispetta il pattern `2`** *(usa `max\ | `bf8aaad 17:45` |
| **`8-bis`** | **ARCHIVIO A ROTAZIONE** — si scrive su `C:`, ogni snapshot completo va su `E:` con `sha1` dei byte compressi, sigilli `R1`-`R5` | `1b40fdb 22:37` |
| **`PROVA-COMB`** | **LA PROVA COMBINATA: TUTTE LE CURE APPROVATE ACCESE INSIEME** — 600 passi, stesso seme e scena, **letture della validazione** *(8 criteri)* **e BILAN | `a44e863 19:18` |
| **`E3`** | **EPOCA 3 + RUN LUNGO** — tag `epoca-3`, 3000 passi, `M1`/`M4` leggere durante il run | `165b0a3 01:44` |
| **`A1-TREVIE`** | **la catena a TRE VIE di `step`** — `if CHI_CORE… / elif VERSO_CHI… / elif not(…)` | `f6d432c 12:45` |
| **`A2-ANELLO`** | **l'anello `A6` di `Z70`** — periodo 2, via `chiralita_core_locale`/`CHI_CORE` | `f6d432c 12:45` |
| **`A3-CHIRALE`** | **`Z71` — la carica chirale non si conserva** | `f6d432c 12:45` |
| **`A4-METRICHE`** | **le METRICHE DEL SETTORE CHIRALE** | `f6d432c 12:45` |
| **`A5-PANNELLO`** | **il PANNELLO FEDELE** *(interpolazione di `psi` accanto a `campo_spaziale`)* | `f6d432c 12:45` |
| **`A6-PERCCHI`** | **`perc_chi` FA DUE LAVORI CON REGOLE OPPOSTE: `chi_basc` lo tratta da CHIRALITA', `TEMPO_SEGNO` da CARICA** — e finche' condividono un array **nessun | `f6d432c 12:45` |
| **`B1`** | **`Z47` — `pos` nella fisica: l'ultimo SFONDO** | `f6d432c 12:45` |
| **`B2`** | **`Z31` — i sigilli non ri-girabili** | `8724ef3 21:07` |
| **`B3`** | **i rami di `memoria_hebbiana_moto`** | `109fb34 21:11` |
| **`B4`** | **i `np.zeros`** | `f6d432c 12:45` |
| **`B5`** | **`theta` / l'aliasing del settore di spin** | `f6d432c 12:45` |
| **`B6`** | **le due cure OFF: `COPPIA_RECIPROCA` e `GRAV_AMPIEZZA`** | `f6d432c 12:45` |
| **`B7`** | **i reperti DA RIMISURARE sulla scena nuova** | `f6d432c 12:45` |
| **`B9`** | **`Z63` / `Z64`** — i 1455 nodi a `10⁻¹³`; la catena `f → x → r` che non riproduce `r` | `9ab7eab 10:52` |

## FATTO — 17

| id | cosa | ultimo commit che lo nomina |
|---|---|---|
| **`4-bis`** | **DIAGNOSI DEI PICCHI DI `n1`** | `f74c2cc 18:20` |
| **`C1-PEQ-ESATTO`** | `PEQ_ESATTO` — rilassamento in forma esatta | `f6d432c 12:45` |
| **`C2-PEQ-NASCITA`** | `PEQ_NASCITA_LOCALE` — nascita locale di `peq` | `f6d432c 12:45` |
| **`C3-SCALA-MIN-PASSO`** | `SCALA_MIN_PASSO` — il freno una volta per passo | `f6d432c 12:45` |
| **`C4-COES-CAUSALE`** | `COES_CAUSALE` — istante unico e cono locale | `f6d432c 12:45` |
| **`C1BIS-ANOM-SIMM`** | `ANOM_SIMM` — il pavimento `1e-9` tolto | `f6d432c 12:45` |
| **`C5-INVARIANTI`** | `INVARIANTI` — 42 domini, due livelli | `f6d432c 12:45` |
| **`CHK2`** | **CHECKPOINT 2** | `1b40fdb 22:37` |
| **`D0`** | **CHI FA SCAPPARE `d0`** | `7935806 17:03` |
| **`G1`** | **§1 QUANTO CONTA IL DISEGNO** — `L_disegno/d` per arco, per regione, nel tempo, e la correlazione col CENTRO del disegno | `4a76517 15:00` |
| **`G2`** | **§2 DOVE SPINGE LA GRAVITA'** | `0be343a 09:21` |
| **`G3`** | **§3 PROVA DI SPEGNIMENTO: la GRAVITA' BIFASE** | `0be343a 09:21` |
| **`G4`** | **§4 PROVA DI SPEGNIMENTO: la MEMORIA DEL MOTO** — flag `MEM_MOTO` | `3eb6b7a 13:01` |
| **`G4-bis`** | **IL SECONDO BRACCIO: spegnere l'INTERO blocco di `mem_mot`** | `da9a014 13:42` |
| **`PATTERN`** | **`doc/PATTERN_DI_PROVA.md`** — la lista di controllo di ogni prova | `5708a3e 13:12` |
| **`REG-A`** | **FASE A del registro della fisica: l'INVENTARIO degli scrittori di stato** | `9a82bfb 12:53` |
| **`REG-B`** | **FASE B: le SCHEDE**, a lotti, **un commit per lotto** | `26c4165 16:17` |

## DIFETTI E SOSPETTI — 47 righe

| stato | quanti | quali |
|---|--:|---|
| (stato non riconosciuto) | 7 | `D25` `D31` `D36` `S02` `S03` `S04` `S11` |
| APERTO / in attesa | 29 | `D38` `D01` `D02` `D04` `D05` `D06` `D07` `D08` `D10` `D12` `D13` `D14` `D15` `D20` `D21` `D23` `D24` `D28` `D29` `D30` `D32` `D33` `D35` `S01` `S05` `S06` `S07` `S08` `S09` |
| CURA DERIVATA | 2 | `D03` `S13` |
| CURA INEFFICACE | 1 | `D26` |
| CURATO | 6 | `D11` `D16` `D17` `D18` `D19` `D22` |
| NON E' UN DIFETTO | 2 | `D09` `D27` |

**ID massimo usato:** difetti `D38` · sospetti `S13`. **Gli ID non si riusano.**
