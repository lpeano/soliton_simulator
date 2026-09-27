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
