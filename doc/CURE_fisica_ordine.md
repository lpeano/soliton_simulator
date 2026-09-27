# L'ELENCO DELLE CURE DI FISICA — **proposta d'ordine, da approvare**

> ## 🛑 **QUESTO DOCUMENTO NON DECIDE NIENTE.** È l'elenco che Luca ha chiesto per approvare
> ## l'ordine. **Nessuna cura è iniziata**, nessun codice è cambiato.
>
> **Decisioni di Luca del 2026-09-27 che governano tutto l'elenco:**
> **(1) PRIORITÀ ASSOLUTA ALLE CURE DELLA FISICA** — nessuna misura né test esplorativo finché la
> fisica non è curata. **L'aggiornamento sincrono È fisica ed è la cura prioritaria.**
> **(2) LA DOPPIA COPERTURA (`4 pi`) È UN ASSIOMA**, di default e strutturale: **non si misura se
> sia migliore — si VERIFICA che sia dove si dichiara.**
> **(3) TUTTO SI MANTIENE:** ciò che è attivo **resta attivo** *(le cure lo dichiarano e lo rendono
> strutturale, non lo spengono)*; ciò che esce si **ARCHIVIA** *(tag + `csv/_archivio/`)*, **mai
> cancellato**; gli stati `.npz` del pilota **si conservano**.
>
> **ECCEZIONE non negoziabile:** **ogni cura ha il suo SIGILLO prima/dopo, col caso che DEVE
> fallire.** Non è un test esplorativo: **è la prova della cura.**

---

## 0. LO STATO DELLO STOP

| | |
|---|---|
| **run in corso** | ### **NESSUNO.** Verificato: **zero processi Python**. |
| **l'A/B di `--sync`** | ### **NON È MAI PARTITO.** Non l'ho lanciato; nulla da fermare, nulla da registrare come `INTERROTTO`. **Lo dico perché il mandato lo dava per avviato.** |
| **voci SOSPESE** *(non cancellate, restano aperte)* | `SCIOGLIMENTO-FASE` · `PSI-FLASH` · `TRATTI-INTERNI` · `MASSA-ID` · `MASSA-ID-FISSO` · `VIDEO-SCENA` · `ARCHI-PRIMI` · `V5-SOGLIA` · `FOGLIO-NULLO` · `FORMA-N-VUOTO` · `SCHW-CORTI` · `PROVA1-40-80` · `ALLUNG-RELATIVO` · `STATI-LOCALI` — **14 voci**, `avanzamento = BLOCCATO`, con la ragione nella nota |
| **gli stati del pilota** | **conservati** *(81 `.npz` locali, `.gitignore`, `sha1` e comando nell'inventario)* |

---

# (a) 🥇 **ETC SU TUTTO IL PASSO PIENO** — *prima, e da sola*

| | |
|---|---|
| **ID proposto** | **`ETC-PASSO`** *(nuovo)* |
| **dove** | `soliton_simulator.py`: le cinque leggi del passo *(`scuoti_vuoto`, `step`, `mitosi`, `rilassa_disegno`, `memoria_hebbiana_moto`)*, `calcola_psi` **`:3998-4030`**, i ~19 chiamanti con `w=None` |
| **cosa si cura** | una **fotografia di inizio passo** letta da tutte le leggi; le scritture si accumulano e si applicano **insieme** a fine passo; **`calcola_psi` riceve SEMPRE `w`** *(`w=None` fuori dall'inizializzazione = errore)*; i nati ricevono `psi` **solo per sé**, **senza ricalcolare gli altri** |
| **cosa si archivia prima** | **tag `pre-etc-passo`** + `csv/_archivio/rami_pre_etc.py` coi rami rimossi **copiati com'erano**, con funzione, riga, cosa facevano e il tag da cui si rilanciano |
| **il sigillo** | **prima/dopo**, con: ① **cosa DEVE cambiare** — i flash spariscono, `mean(phi_g)` **continuo** nei passi con nascite *(oggi `138.7 → 366.2 → 139.7`)*; ② **cosa NON deve cambiare** — firme campo per campo sui passi **senza** nascite; ③ **il caso che DEVE fallire** — **riattivare il ricalcolo in `memoria_hebbiana_moto` deve far scattare `H-ETC-1`** |
| **i presidi** | **`H-ETC-1`**: dentro `passo_pieno`, `calcola_psi` **senza `w`** è chiamata **0 volte**. **`H-ETC-2`**: **permutare l'ordine delle leggi dà lo stesso stato** *(tolleranza dichiarata)* — **è la proprietà di Jacobi** |
| **chiude** | **`PSI-FLASH`** · **`CENS-A7`** *(«~19 chiamanti», misurati 2)* · **`CENS-B7`** *(`--sync` mai misurato)* · **`CENS-A6`** *(`README:175` falso)* |

> **⚠ E `PSI-FLASH` NON è un difetto del diagnostico: è nella FISICA.** La `psi` ricalcolata in
> `memoria_hebbiana_moto` entra in `I` → `pozzo_grafo(I)` → **la spinta `S09`** dello **stesso**
> passo. **È la ragione per cui questa cura è la prima.**

---

# (b) 🥈 **DOPPIA COPERTURA STRUTTURALE** — *dopo il sigillo di (a)*

| | |
|---|---|
| **ID proposto** | **`DOPPIA-COP`** *(nuovo)* |
| **dove** | `_dphi` / `FASE_2PI` **`:1300`, `:4072-4078`** · **`TORS_4PI` `:894`** *(«prova sperimentale», **nessun flag per spegnerlo**)* · **`RITMO_WRAP_2PI`** *(**il driver lo passa**: il ritmo avvolge su `2 pi`)* · il wrapping di `dph` e della torsione · lo spinore *(`_psi_spinor`, segno di doppia copertura)* · **la soglia `3 pi` di `SCALE-TW`** |
| **cosa si cura** | **`4 pi` di default e STRUTTURALE**: i rami a `2 pi` **escono** dal codice; i flag `2 pi` diventano **no-op accettati** *(la forma di `--tempo-unico-mitosi`)*; il commento **«prova sperimentale» di `TORS_4PI` si riscrive come ASSIOMA** |
| **cosa si archivia prima** | **tag `pre-doppia-copertura`** + `csv/_archivio/rami_2pi.py` |
| **il sigillo** | ### **VERIFICA che l'assioma sia implementato** — ogni punto dell'inventario **a `4 pi` a runtime** — **NON una misura se sia migliore** *(decisione (2))* |
| **il presidio** | un hook che **fallisce se nel percorso vivo ricompare un avvolgimento a `2 pi` non dichiarato come lettura del campo scalare**, col suo caso che deve fallire |
| **chiude** | **`CENS-A2`** *(`TORS_4PI` dichiarata sperimentale e attiva)* |

> ### ⚠ **DOVE LA DOPPIA COPERTURA NON PUÒ VIVERE, e va detto invece di forzarlo:**
> **il campo scalare legge `e^{i phi}`, periodo `2 pi`** — **31 righe su 31**, `Z118`/`Z120`.
> **Lì la doppia copertura vive NELLO SPINORE** *(segno, mezzi angoli)*, non in `phi`.
>
> ### ⚠ **E UN'ATTESA DA RIPORTARE, NON DA DECIDERE:** con `FASE_2PI` le mitosi passavano da **62
> ### a 1** *(soglia `3 pi`, `D36`)*. **Rendere tutto `4 pi` può spostare quell'equilibrio.**
> **Me l'aspetto nella direzione opposta** *(soglia più alta in un dominio doppio → **meno**
> mitosi, non di più)*, **ma non lo misuro ora** e **non so di quanto**.

---

# (c) 🥉 **I RESIDUI `A3`/`A2` CON CURA CHIARA**

| ID | dove | cosa si cura | il sigillo |
|---|---|---|---|
| **`D03`** *(blocca `SI`)* | memoria del moto | le direzioni vengono da **`pos`** e la normalizzazione è su **`Imed` GLOBALE** | byte-identico a flag spento; **caso che deve fallire:** con `pos` alterato a `d` costante, a flag acceso **non cambia** |
| **`KURA-POS`** *(nuovo)* | `:5385-5386` | `r_cm = norm(pos - cmv)` con **`cmv` = centro di massa GLOBALE**, e `pozzo = I2.sum()/r_cm` | ⚠ **`I2.sum()` SI CANCELLA in `prof_rel`: quel residuo è INERTE.** La cura riguarda **solo `pos` e `cmv`** — e dirlo è ciò che evita di curare un non-difetto |
| **`S09-MEDIANA`** | `:6808` | la spinta scala con **`median(d0)` GLOBALE**: stesso `A2` già curato nel sito **fratello** `S05` il 2026-09-17, mai portato qui | byte-identico a flag spento; A/B con la barra fra semi. **Se l'effetto fosse sotto la barra la cura resta giusta per DIMOSTRAZIONE, non per misura** |
| **`RITMO-MEDIANA`** *(nuovo)* | `ritmo()` | `r_k` normalizzato sulla **mediana GLOBALE** di `\|f\|`. **`A3` è già curato** *(mediana del passo PRECEDENTE)*; **resta `A2`: la globalità** | riduzione al limite: a mediana locale == globale, byte-identico |
| **`SCHW-CORTI`** | `:6368-6369` | `dd` nasce da **`pos`**: residuo `A3-DISEGNO`. **Misurato: il `39 %` delle coppie accorcia il grafo** | il gemello di `POZZO_D`: con `pos` alterato, a flag acceso `dd` **non cambia** |

---

# (d) **GLI ALTRI `SI`, E LE VOCI DI FISICA DEL CENSIMENTO**

**Per la decisione (3) queste RESTANO ATTIVE: la cura è DICHIARARLE e renderle strutturali
— commento vero, flag coerente, voce d'indice — NON spegnerle.**

| ID | che cos'è | la cura |
|---|---|---|
| **`U1`** *(blocca `SI`)* | `massa_critica_collasso`: **21 usi DENTRO le leggi** | da leggere e decidere |
| **`CLI-1`** *(blocca `SI`)* | i sigilli di `cura 4`/`cura 5` **non hanno mai provato il percorso CLI** | rifarli via CLI |
| **`SCALE-TW`** *(blocca `SI`)* | le scale della torsione, **da capo**. **`M1` è misurata** *(`0` nascite nelle masse e nel varco)* | l'analisi, **dopo (b)**: la soglia `3 pi` è parte dell'assioma |
| **`D31`** *(blocca `SI`)* | il freno di `SCALA_MIN` **è il motore** della crescita di `d0` *(il `117 %`)* | da leggere e decidere |
| **`CENS-A3`** | `COPPIA_MIT`: *«ATTIVA»* e *«spenta di default»* **sulla stessa riga** | **il commento si riscrive**; le tre misure promesse restano aperte |
| **`CENS-B1`** | `SPINORE_VIVO` **si autodenuncia**: *«mai validato come default»* | dichiarare lo stato; il rigiro è una **misura**, quindi **sospesa** |
| **`CENS-B12`** | `KERNEL_ALPHA` *«SEMPRE ATTIVO»*, **rivendica il principio di equivalenza** — la prova ③ del bersaglio | voce d'indice *(fatta)*, commento vero, e **un flag** perché *«alpha=0 lo spegne»* sia raggiungibile |
| **`CENS-B8`** | `VERLET`: il ramo detto *«SPERIMENTALE»* **è il percorso vivo** | riscrivere il commento; `COMPONENTI_PROMOSSE` già registra la contraddizione |
| **le altre 4 (A) e 13 (B)** | nell'indice come `CENS-A*` / `CENS-B*` | stessa forma: **dichiarare, non spegnere** |

---

# (e) **SCELTE DI MODELLO — SOLO IL DOCUMENTO DELLE OPZIONI, NIENTE CODICE**

**ID proposto: `MODELLO-FASE`.** **Non si implementa niente**: si scrivono le opzioni con ciò che
ciascuna comporta, e **decide Luca**.

1. **come `phi` entra nello spinore dentro l'assioma della doppia copertura** — `e^{i phi/2}`?
   *(Oggi `_psi_spinor` **non contiene `phi` affatto**: nasce dall'azimut del Bloch. È `CENS-A1`.)*
2. **le masse dipinte anche nello spinore** — oggi la scena scrive `phi` e `phi0` **e basta**.
3. **le velocità di fase iniziali** — *la fase come orologio?* `dphi/dt = omega0·r_k + delta_k`,
   con `delta_k` *(l'attuale `phivel`)* come **eccitazione**, nulla o quasi per una massa a riposo.
   *(Oggi la scena **non tocca `phivel`**: è `H1`, confermata dal sorgente.)*
   **Alternativa aperta:** `phi` come **onda con inerzia** *(sine-Gordon)* — e allora basterebbe una
   **condizione iniziale coerente**.

---

## 📌 CHE COSA SERVE DA LUCA, PRIMA DI PROSEGUIRE

1. **l'ordine è approvato così?** *(in particolare: **(a) da sola** prima di tutto)*;
2. **`blocca_run_base` delle 23 voci `CENS-*` è `DA-DECIDERE`**: quali diventano `SI`?
   *(Non l'ho deciso io: una decisione senza prova non passa il validatore.)*
3. **(e) è un documento o si ferma qui?**

**Fino alla risposta: nessuna cura inizia.**



---

# 6. **LA REGOLA DI LUCA APPLICATA ALLE 23 `CENS-*`** *(2026-09-27)*

> **La regola, verbatim:** `SI` = **la falsita' cambia i NUMERI della fisica del run**;
> `NO` = **si risolve riscrivendo un commento o un documento**.
> **Applicata a TUTTE e 23, non solo alle cinque nominate.** L'ho applicata io alla
> classe (A) e alle (B) non attive; **le dieci che la regola NON decideva le ha decise
> Luca** *(risposte a `bf15c0c`)*. Esito: **5 `SI` · 18 `NO` · 0 ancora aperte**.

*(La colonna **chi** dice se la riga porta una decisione esplicita di Luca — oppure
l'applicazione della regola da parte mia.)*

## ✅ `SI` — 5 voci

| ID | che cos'e' | chi | motivo |
|---|---|---|---|
| `CENS-A1` | la RIDUZIONE AL LIMITE dello spinore: lo stato che la gara | **LUCA** | SI. Si chiude con la decisione (e) sul legame phi-spinore. |
| `CENS-A2` | `TORS_4PI`: *"Prova sperimentale, default off"*, e il defa | regola | chiusa da (b): rendere `4 pi` strutturale puo' spostare la soglia di mitosi |
| `CENS-A6` | `README.md`: *"Tutti gli script di lancio includono esplic | regola | chiusa da (a): la cura rende l'aggiornamento SINCRONO, e cio' cambia i numeri |
| `CENS-A7` | il commento di `calcola_psi`: *"~19 chiamanti"*, misurato  | regola | chiusa da (a): imporre `w` a ogni `calcola_psi` cambia quale `psi` legge la fisica |
| `CENS-B7` | *"Default ancora off; **convergenza e superiorita' rispett | regola | chiusa da (a): `--sync` e' la cura (a) stessa, e cambia i numeri | CORREZIONE DEL 2026-09-27, da ETC-PASSO FASE 0 (ae8d056): il motivo precedente era mio ed era sbagliato. --sync rende Jacobi l'INTERNO di step, non il passo: 0 usi in scuoti_vuoto, mitosi, rilassa_disegno, memoria_hebbiana_moto. blocca_run_base = SI resta corretto. |

## `NO` — 18 voci

| ID | che cos'e' | chi | motivo |
|---|---|---|---|
| `CENS-A3` | `COPPIA_MIT`: *"(opzione, spenta di default)"*, e il defau | regola | il ramo gira UGUALE prima e dopo: la falsita' e' nel commento, e si riscrive |
| `CENS-A4` | `MITOSI_DIR`: *"MITOSI DIREZIONALE ATTIVA"*, e il valore e | regola | il ramo e' MORTO (`MITOSI_DIR = 0.0`): un commento falso su codice che non gira |
| `CENS-A5` | `_passo_spinoriale` *"ORFANO"*: smentito da un altro comme | regola | due commenti che si contraddicono: nessuno dei due esegue niente |
| `CENS-B1` | *"`SPINORE_VIVO = True` **NON E' MAI STATO VALIDATO COME D | **LUCA** | legge ATTIVA, resta attiva (decisione 3). da misurare dopo il run base. |
| `CENS-B2` | ON di default *"PER DECISIONE DI LUCA E SU BASI DI FORMA,  | **LUCA** | legge ATTIVA, resta attiva (decisione 3). da misurare dopo il run base. |
| `CENS-B3` | *"IN VERIFICA"*, e nel corpo: *"stabile, ma **il guadagno  | **LUCA** | LA CURA E' DICHIARARE CHE IL RAMO OFF NON ESISTE (nessun flag CLI): non si misura un ramo che non c'e', si scrive che non c'e'. |
| `CENS-B4` | *"costanti temporali TAU_P/TAU_BG/TAU_TW come RAPPORTI adi | **LUCA** | LA CURA E' DICHIARARE CHE IL RAMO OFF NON ESISTE (nessun flag CLI): non si misura un ramo che non c'e', si scrive che non c'e'. |
| `CENS-B5` | *"**Da validare su TEMPI LUNGHI** (hardware di Luca): tagl | **LUCA** | legge ATTIVA, resta attiva (decisione 3). da misurare dopo il run base. |
| `CENS-B6` | *"**DA RIPRENDERE**: seme iniziale di asimmetria struttura | **LUCA** | NO: e' PROGETTO (chiede un meccanismo nuovo), non una lacuna di misura. |
| `CENS-B8` | *"INTEGRATORE METRICO **SPERIMENTALE** ... Default off per | **LUCA** | legge ATTIVA, resta attiva (decisione 3). da misurare dopo il run base. |
| `CENS-B9` | *"LEGGE DI STABILITA' (**esplorativa**): i nuovi nodi in r | regola | NON attiva nel driver: non puo' cambiare i numeri di questo run |
| `CENS-B10` | *"**ESPLORATIVO**: lega la creazione di coppia anche all'a | regola | NON attiva nel driver: non puo' cambiare i numeri di questo run |
| `CENS-B11` | tre osservabili di controllo nominate una per una -- *"esp | regola | NON attiva (`PLAST_DIN` e' il sostituto): la promessa e' rimasta senza esecutore |
| `CENS-B12` | *"KERNEL BILANCIATO DAL TEMPO PROPRIO (tau^alpha) **SEMPRE | **LUCA** | NON blocca il run base, BLOCCA LA PROVA 3 (universalita'): la misura del principio di equivalenza va fatta prima della PROVA 3. Correzione del guardiano al mio SI: un SI avrebbe bloccato il run base con una misura SOSPESA dalla decisione (1). |
| `CENS-B13` | *"`inerzia = np.maximum(_contrasto * _T2, 1e-6)` -- **il p | **LUCA** | legge ATTIVA, resta attiva (decisione 3). da misurare dopo il run base. |
| `CENS-B14` | l'osservabile e' calcolata (`m0_spin_core`, `m0_spin_core_ | **LUCA** | legge ATTIVA, resta attiva (decisione 3). da misurare dopo il run base. |
| `CENS-B15` | il **condizionale** scritto nel commento: *"Un esito posit | regola | e' un CONDIZIONALE scritto in un commento: si risolve riscrivendolo |
| `CENS-B16` | (1) INVENTARIO e (2) README sono prescritti *"nello stesso | regola | e' di PROCESSO (inventario e README), non di fisica: nessun numero lo tocca |

## ✅ **LE DIECI CHE ERANO AMBIGUE SONO DECISE**

> **La regola non le decideva, e invece di forzarla l'ho detto.** Le ha decise Luca:
> `CENS-A1` **`SI`** *(si chiude con la decisione **(e)** sul legame `phi`-spinore)*;
> `CENS-B1 B2 B5 B8 B13 B14` **`NO`** *(leggi **attive**, restano attive —
> decisione (3) — e **da misurare dopo il run base**)*;
> `CENS-B3 B4` **`NO`**, e la cura e' **dichiarare che il ramo OFF non esiste**;
> `CENS-B6` **`NO`** *(progetto)*.
>
> ### ⚠ **E UNA CORREZIONE DEL GUARDIANO SU UN MIO `SI`: `CENS-B12`
> ### (`KERNEL_ALPHA`) E' `NO`.**
> Non blocca il **run base**: **blocca la PROVA 3** *(universalita')*, e la misura
> del principio di equivalenza va fatta **prima della PROVA 3**.
> **Il mio `SI` avrebbe bloccato il run base con una misura SOSPESA** dalla
> decisione (1) — cioe' esattamente la conseguenza che avevo segnalato come aperta,
> **applicata alla voce sbagliata**.

