# IL PUNTO DELLA SITUAZIONE — **generato dalla CODA UNICA**

> **SOLA LETTURA.** Generato da `csv/_punto_della_situazione.py` leggendo
> `doc/STATO_RUN.md`. **Non e' scritto a memoria**, ed e' il punto: **se un task manca
> qui, manca dalla coda** — e quello e' il difetto da correggere.

## IN CORSO — 1

| id | cosa | ultimo commit che lo nomina |
|---|---|---|
| **`G4`** | **§4 PROVA DI SPEGNIMENTO: la MEMORIA DEL MOTO** — flag `MEM_MOTO` | `49a4cb2 13:58` |

## CON RISERVA — 3

| id | cosa | ultimo commit che lo nomina |
|---|---|---|
| **`V`** | **VALIDAZIONE a 600 passi** | `49a4cb2 13:58` |
| **`B8`** | **⚠ IL BLOCCO DEL RUN A 6000 AL PASSO 2700** | `166958d 11:44` |
| **`B10`** | **⚠ `--override-blob` e la COPIA del driver** | `e2a15dd 19:33` |

## IN CODA — 11

| id | cosa | ultimo commit che lo nomina |
|---|---|---|
| **`G4-bis`** | **IL SECONDO BRACCIO: spegnere l'INTERO blocco di `mem_mot`**, spostamento di fase compreso | `010809a 13:57` |
| **`G4-MEMARCO`** | **`MEM_ARCO` — LA MEMORIA DEL MOTO TRADOTTA IN FORMA RELAZIONALE** *(aggiunta di Luca al §4, 2026-09-22)* | `010809a 13:57` |
| **`CHK3`** | **CHECKPOINT: referto dei quattro esiti, ciascuno contro le sue letture fissate PRIMA** | `944064a 13:06` |
| **`CHK3-D`** | **Nel referto del `CHK3`, la sezione «I DIFETTI NUOVI CONTRO LE MISURE GIA' FATTE»** — `D27` *(quattro componenti)* e `D25` *(il tempo che non scorre) | `944064a 13:06` |
| **`PAT-1`** | **`_dove_spinge_la_gravita.py` non rispetta il pattern `5`** *(nessun CONTROLLO DELL'INVOLUCRO)* | `cefcf58 12:01` |
| **`PROVE`** | **LE TRE PROVE DELL'IPOTESI DELLA GRAVITA' A SPINTA** — ① due masse si avvicinano? ② con che legge? ③ tutti i corpi cadono uguale? | `56b348b 13:12` |
| **`C5-res`** | **I RESIDUI DI `C5`** — **`I4`** la scatola nera *(rigiocare da solo il passo in cui scatta un invariante)*, **`I5`** la tabella degli underflow **per | `1b40fdb 22:37` |
| **`REG-B`** | **FASE B: le SCHEDE, a lotti** — prima le componenti dentro le misure in corso | `5756198 12:56` |
| **`REG-C`** | **FASE C: LA STORIA** di ogni legge, e le schede delle leggi TOLTE | `—` |
| **`REG-R`** | **LA REGOLA MANTENUTA del registro della fisica** — la riga in `CLAUDE.md` *(«nessuna legge fisica entra, cambia o esce dal simulatore senza passare d | `010809a 13:57` |
| **`REG-V`** | **`_verifica_registro.py`**: completezza, esistenza, coerenza con la traccia di `d0` e col registro dei domini di `C5` | `—` |

## (senza marcatore) — 17

| id | cosa | ultimo commit che lo nomina |
|---|---|---|
| **`PAT-2`** | **`_spegni_grav_bifase.py:184` non rispetta il pattern `2`** *(usa `max\ | `cefcf58 12:01` |
| **`8-bis`** | **ARCHIVIO A ROTAZIONE** — si scrive su `C:`, ogni snapshot completo va su `E:` con `sha1` dei byte compressi, sigilli `R1`-`R5` | `1b40fdb 22:37` |
| **`E3`** | **EPOCA 3 + RUN LUNGO** — tag `epoca-3`, 3000 passi, `M1`/`M4` leggere durante il run | `56b348b 13:12` |
| **`A1`** | **la catena a TRE VIE di `step`** — `if CHI_CORE… / elif VERSO_CHI… / elif not(…)` | `692b3dc 13:09` |
| **`A2`** | **l'anello `A6` di `Z70`** — periodo 2, via `chiralita_core_locale`/`CHI_CORE` | `bc30e62 12:48` |
| **`A3`** | **`Z71` — la carica chirale non si conserva** | `aef6854 12:37` |
| **`A4`** | **le METRICHE DEL SETTORE CHIRALE** | `30250d7 10:58` |
| **`A5`** | **il PANNELLO FEDELE** *(interpolazione di `psi` accanto a `campo_spaziale`)* | `692b3dc 13:09` |
| **`A6`** | **`perc_chi` FA DUE LAVORI CON REGOLE OPPOSTE: `chi_basc` lo tratta da CHIRALITA', `TEMPO_SEGNO` da CARICA** — e finche' condividono un array **nessun | `79be011 07:55` |
| **`B1`** | **`Z47` — `pos` nella fisica: l'ultimo SFONDO** | `abc5b49 11:28` |
| **`B2`** | **`Z31` — i sigilli non ri-girabili** | `96c7f22 11:08` |
| **`B3`** | **i rami di `memoria_hebbiana_moto`** | `874c879 01:04` |
| **`B4`** | **i `np.zeros`** | `cefcf58 12:01` |
| **`B5`** | **`theta` / l'aliasing del settore di spin** | `53e08f3 12:30` |
| **`B6`** | **le due cure OFF: `COPPIA_RECIPROCA` e `GRAV_AMPIEZZA`** | `56b348b 13:12` |
| **`B7`** | **i reperti DA RIMISURARE sulla scena nuova** | `56b348b 13:12` |
| **`B9`** | **`Z63` / `Z64`** — i 1455 nodi a `10⁻¹³`; la catena `f → x → r` che non riproduce `r` | `0732e85 12:49` |

## FATTO — 14

| id | cosa | ultimo commit che lo nomina |
|---|---|---|
| **`4-bis`** | **DIAGNOSI DEI PICCHI DI `n1`** | `010809a 13:57` |
| **`C1`** | `PEQ_ESATTO` — rilassamento in forma esatta | `944064a 13:06` |
| **`C2`** | `PEQ_NASCITA_LOCALE` — nascita locale di `peq` | `5942f16 09:05` |
| **`C3`** | `SCALA_MIN_PASSO` — il freno una volta per passo | `ee46840 11:13` |
| **`C4`** | `COES_CAUSALE` — istante unico e cono locale | `1b40fdb 22:37` |
| **`C1-bis`** | `ANOM_SIMM` — il pavimento `1e-9` tolto | `1b40fdb 22:37` |
| **`C5`** | `INVARIANTI` — 42 domini, due livelli | `ccf1f73 12:37` |
| **`CHK2`** | **CHECKPOINT 2** | `1b40fdb 22:37` |
| **`D0`** | **CHI FA SCAPPARE `d0`** | `49a4cb2 13:58` |
| **`G1`** | **§1 QUANTO CONTA IL DISEGNO** — `L_disegno/d` per arco, per regione, nel tempo, e la correlazione col CENTRO del disegno | `010809a 13:57` |
| **`G2`** | **§2 DOVE SPINGE LA GRAVITA'** | `5756198 12:56` |
| **`G3`** | **§3 PROVA DI SPEGNIMENTO: la GRAVITA' BIFASE** | `56b348b 13:12` |
| **`PATTERN`** | **`doc/PATTERN_DI_PROVA.md`** — la lista di controllo di ogni prova | `5756198 12:56` |
| **`REG-A`** | **FASE A del registro della fisica: l'INVENTARIO degli scrittori di stato** | `9a82bfb 12:53` |

## DIFETTI E SOSPETTI — 36 righe

| stato | quanti | quali |
|---|--:|---|
| (stato non riconosciuto) | 2 | `S02` `S04` |
| APERTO / in attesa | 25 | `D01` `D02` `D04` `D05` `D06` `D07` `D08` `D09` `D10` `D11` `D12` `D13` `D14` `D15` `D20` `D21` `D23` `D24` `D28` `D29` `D30` `D31` `S01` `S03` `S05` |
| CURA DERIVATA | 1 | `D03` |
| CURA INEFFICACE | 1 | `D26` |
| CURATO | 5 | `D16` `D17` `D18` `D19` `D22` |
| DA RIMISURARE | 1 | `D25` |
| NON E' UN DIFETTO | 1 | `D27` |

**ID massimo usato:** difetti `D31` · sospetti `S05`. **Gli ID non si riusano.**
