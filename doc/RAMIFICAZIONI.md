# REGISTRO DELLE RAMIFICAZIONI — lo **stato** dei fronti, non la cronaca

> Branch `fork-su2`. Creato 2026-09-15. Blob al momento della creazione: **`7d484580`**.
> **Questo e' uno STATO, non un diario.** La cronaca sta nei documenti di `doc/` e in
> `CLAUDECONNECT.md`. Qui c'e' solo: dove siamo, su cosa, e cosa lo chiuderebbe.
>
> **Si aggiorna nello STESSO commit del riscontro che lo cambia** (§5-bis). Un registro aggiornato
> «dopo» e' un registro falso.
>
> **Registro GEMELLO:** questo file tiene i **fronti aperti**. Lo stato **promosso / candidato /
> esperimento / correzione** delle **componenti** (cioe' dei flag) sta in
> **`doc/COMPONENTI_PROMOSSE.md`**, e la regola che lo governa e' **`CLAUDE.md` §10**.
> Non si mescolano: qui c'e' *cosa non sappiamo ancora*, li' c'e' *cosa e' fisica e cosa e' opzione*.

---

## ⚠ LA COSA DA LEGGERE PER PRIMA

> **⚠ QUARTO MARCHIO, il piu' esteso — 2026-09-16, DUE CORREZIONI DI DIFETTO SENZA FLAG.**
> **Ogni misura di questo repo prodotta PRIMA del blob `c57800c1` e' «prodotta con `_xi_rumore`
> EREDITATO alla mitosi e SENZA il fattore `cs^-2` nell'inerzia: misura di un sistema DIVERSO da
> quello corrente».** Vale per gli **8 CSV della campagna a quattro bracci**, per **tutti i sigilli
> del 2026-09-16** e per ogni voce di questo registro che li cita.
> **① `_xi_rumore` non si eredita** (blob `57681b9e`): `xi` e' un campione dell'**AMBIENTE**, non
> una proprieta' del nodo. Prima, padre e figlio avevano rumore **correlato: misurato `+1.0000`**;
> dopo, **`+0.0065` su 258 coppie**.
> **SIGILLO DELLE DUE CORREZIONI: 16/16 PASS** (`csv/_seal_fork/_sigillo_correzioni.txt`).
> **② `inerzia = max(rho*(CS_M/cs)^2, 1e-6)`** (blob `c57800c1`): il fattore che la derivazione
> `inerzia = (d/cs)^2` impone e che **mancava**. Sigillo **M2 PASS**, `max|A-B| = 0.000e+00` con
> nodi **3070 = 3070** dove `cs = CS_M`; **M2b PASS** (col `cs` vivo il fattore morde).
> **⚠ MA L'EFFETTO OGGI E' MINUSCOLO, ed era scritto PRIMA:** il fattore vale **1.0000048** sul
> nodo mediano (`cs_std/cs = 0.0333 %` a 150 passi). **Si e' fatta perche' senza la legge e'
> sbagliata**, non per un effetto misurabile a questa densita'.
> **Le voci di §B e §C NON sono state ri-misurate**: portano questo marchio in aggiunta ai tre
> precedenti.

> **⚠ SECONDO MARCHIO, aggiunto il 2026-09-15 sera — L'OROLOGIO.** Tutte le misure di questo repo
> fino al blob `08784685` sono state prese con il **ritmo SCALARE a 2π**: la doppia copertura
> (**FASE 5, 4π**) **non era attiva** (95.33 % di scarto della guardia, **C11**).
> **Non erano «integrate male»** — `r` era ricalcolato a ogni passo e valido; erano misure di un
> **modello diverso da quello che il flag dichiarava**.
> **Condizione da riverificare col settore 4π in funzione**, e vale **anche per T3 e i suoi quattro
> bracci**, cioè per il divario stesso che stiamo inseguendo.
>
> **✅ TERZO MARCHIO — TOLTO IL 2026-09-16. `tau` SEGUE `cs`, MISURATO.**
> Il ri-sigillo dello STRATO 1 con **`--cs-dinamico`** e il nuovo **SIGILLO 8** da'
> **25/27 PASS + 2 FAIL ATTESI** (S1a/S1b, previsti e committati **prima** in
> `doc/PREDIZIONE_risigillo_strato1.md`). **S8b: rapporto `cs=8 / cs=1` = 7.660686976**
> misurato = atteso — **se `cs` fosse ignorato varrebbe ESATTAMENTE 1.000000000**.
> **Rilanciare il sigillo com'era NON sarebbe bastato:** nei test in-process
> `_cs_nodo_prev` era `None` o **costante**, e un `cs` costante non esercita `tau = d/cs`.
> **⚠ E NON SIGNIFICA che `tau = d/cs` sia distinguibile da `tau ∝ d` nei run veri:** C13
> dice di no. **S8 prova che la LEGGE e' viva; C13 che a queste densita' ha poco da dire.**
> **E sullo stesso ri-sigillo e' uscito un difetto grosso: il sigillo SI SCHIANTAVA da un
> giorno** (`AttributeError` a S2, `_tempo_luce_nodo` mancante in `FintaRete`): **S2..S8 e
> S3b non giravano affatto**, e dal blob `f7051c3` il «23/23» non era **riproducibile**.
>
> **⚠ TERZO MARCHIO, testo STORICO — `cs` COSTANTE (2026-09-15, rilievo di Luca).**
> Il **sigillo 23/23 dello STRATO 1** e le due misure del braccio OFF sono girati **senza
> `--cs-dinamico`**: `cs = CS_M` costante, `_cs_nodo_prev` mai scritta, quindi `tau = d/CS_M`.
> **Il meccanismo del ritardo regge** (S7 misura `r=2/r=1 = 1.9753`, che dipende da `r` non da `cs`);
> **la dipendenza di `tau` da `cs` NON e' mai stata esercitata** — ed e' *proprio* la ragione per cui
> `tau = d/cs` sarebbe piu' principiato di `tau ∝ rho`.
> Vale **doppio** per lo Strato 1: quel sigillo e' del blob `2277e9a0`, **precedente alla cura della
> cache**, quindi anche col flag acceso la cache sarebbe stata scartata a ogni mitosi.
> **I quattro run in partenza sono la PRIMA VOLTA che quella dipendenza gira davvero: non e'
> «rifare la misura meglio», e' MISURARE PER LA PRIMA VOLTA.**
>
> **Quattro chiusure (§B) sono MISURE fatte su un settore ALIASATO** — lo spin gira a ~112
> giri/passo, quindi ogni misura su di esso e' presa su uno sfarfallio.
> **Vanno rifatte quando `omega` rientra nel tetto.** Se questo non resta scritto, fra un mese
> verranno lette come definitive: e' **esattamente** il difetto che `doc/AUDIT_misurato_vs_asserito.md`
> ha gia' trovato nei documenti di questo progetto.

---

# A. CHIUSE PER DIMOSTRAZIONE — algebriche, **non si riaprono**

| # | fronte | riscontro | sostegno |
|---|---|---|---|
| **A1** | **Teorema di inerzia** — lo Strato 0 e' inerte: la connessione costruita dagli stessi stati che trasporta e' uno **specchio**, `<psi_i\|N\|psi_j> = 2<psi_i\|psi_j>` esatto | **1.57e-15** su 200 000 coppie | `csv/_seal_fork/_reperto_inerzia.py`, `CLAUDE.md` §6 |
| **A2** | **Invarianza del Bloch sotto Step 2** — `_phc` e' una **fase globale**, e `nb = psi†σpsi` non la vede | **3.3e-16** | `csv/_seal_fork/_sigillo_step2.py`, `CLAUDECONNECT.md` §926 |
| **A3** | **FDT del solo scuotimento** — il drift di `n → (n+a·g)/\|n+a·g\|` e' `−a²n`, funzione del **solo `n`**, senza i vicini: **un rumore locale non puo' allineare ai vicini** | verificato a **1.28e-07** | `doc/PREDIZIONE_fdt_scuotimento.md` |

> **Sono dimostrazioni**, non misure: valgono a qualunque risoluzione, **anche con lo spin aliasato**.

**Nota su A2, dichiarata perche' il registro non deve contenere numeri senza fonte:** il mandato che
ha generato questo file cita `2.78e-17` e `1.11e-16`. **Non compaiono da nessuna parte nel repo**
(cercati: zero occorrenze), mentre `3.3e-16` compare in 10 punti. Ho scritto **quello documentato**.
Se i due numeri vengono da run di Luca fuori dal repo, vanno committati per entrare qui.

---

# B. CHIUSE PER MISURA — **su un settore ALIASATO ⇒ DA RIFARE**

> **MARCHIO COMUNE, che non si toglie:** *misurate con il settore di spin a **~112 giri/passo**
> (aliasato). **Da rifare se e quando `omega` rientra nel tetto** `2π·cs/λ`.*

| # | fronte | riscontro | cosa lo chiuderebbe **davvero** |
|---|---|---|---|
| **B4** | **Bloch frozen-o-noise** | senza scuotimento `\|<n>\| = 1.000000`; con, `chi = 90.0 ± 39.2` contro il nullo **90.000 ± 39.171** | la stessa misura con `theta < ~1 giro/passo` |
| **B5** | **Kuramoto refutato** | K-frozen **byte-identico** a OFF; K-noise = NO-rumore | idem |
| **B6** | **Esito B del turbo** — con `cs` al **5 %** di `CS_M` lo Step 2 non muove lo spin | `chi` ON 89.9865 / OFF 89.9941 contro 90.000; autocorrelazione piatta su 14 bin | idem, **+ un secondo seme** (§2.7) |
| **B7** | **shake-then-freeze** — la precessione mutua non organizza | `chi` deriva di **−0.33°** in 600 passi da stato casuale | idem |

---

# C. DIAGNOSI CHIUSE (2026-09-15)

| # | cosa e' stato stabilito | numero | sostegno |
|---|---|---|---|
| **C1** | **ESITO (I): nessun bug.** `omega = coppia/inerzia` porta **esattamente** il −1 richiesto | pendenza **−1.056**, `r = −0.981`, n=2781 | `doc/TRACING_omega.md` |
| **C2** | Il −1 e' **cancellato da `√tau`**, con `tau ∝ rho^1.81` | `+1.176 ± 0.019` (n=2195) | `doc/TAU_tempo_luce.md` |
| **C3** | Il residuo di 0.34 e' **TRANSITORIO**, non un termine mancante | `0.979 → 0.010` fra i passi 50 e 400 | `doc/BARRE_ERRORE_pendenze.md` |
| **C4** | **`inerzia = T²`** — chiude il buco dimensionale; esponente `cs^−2` **derivato**, verso confermato | stesso esponente dello Step 2, derivato **prima e indipendentemente** | `doc/INERZIA_tempo_quadro.md` |
| **C5** | **`tau_luce = d/cs` e' PIATTO** ⇒ la sostituzione **rompe** la cancellazione | **+0.097 ± 0.0055**, IC95 [+0.086, +0.108] | `doc/TAU_tempo_luce.md` §7 |
| **C6** | Il rumore **non** guida `omega` | `R_stoc = 0.041`, **sotto** l'errore atteso 0.097 | `doc/TRACING_omega.md` §6.1 |
| **C7** | **La cache `_cs_nodo_prev` veniva scartata a ogni mitosi** ⇒ nel 72 % delle chiamate `tau = d/cs` calcolava `tau = d/CS_M`. **Curata** (il figlio eredita da `src`, sesta voce della stessa convenzione). **NB: e' chiuso il DIFETTO, non un effetto fisico** — vedi D.2/**P** | fallback **71.88 % → 0.00 %**; cache inusabile **24/30 → 0/30**; sigillo **P1-P4 + P1b: 5/5 PASS** | `doc/FIX_cache_cs.md`, `csv/_seal_fork/_sigillo_fix_cache.txt` |
| **C8** | **LA FASE 2 NON SI CHIUDE.** Col tempo-luce cablato la pendenza resta **lontanissima** dall'attesa `-0.69`, e `theta` resta **aliasato** su tutti e sei i run misurati | ON post media **-0.4745**, divario **-0.2155**, SE della media **0.0165** ⇒ **z = 13.1**; `theta` **30.7-44.9 giri/passo** | `doc/FIX_cache_cs.md` §7, `csv/_test_fork/_controllo_semi.txt` |
| **C9** | **`--tau-luce` ha un effetto GRANDE sulla pendenza** (che pero' non basta): il contrasto ON-OFF e' **11 volte** la dispersione fra semi | ON-OFF **-0.3219** contro dispersione fra semi **0.030** | `csv/_test_fork/_rimisura_t3.txt` |
| **C11** | **`_psi_spin_prec` non era esteso alla mitosi ⇒ la guardia ESATTA di `ritmo()` scartava il ramo a **4π**: la **FASE 5 (orologio di doppia copertura) era INERTE in ogni run `--campo-spinoriale` mai girato**. `r` veniva dal ritmo **SCALARE a 2π**, quello storico — **non stale: diverso**. **CURATO**, settima voce della stessa convenzione | guardia 4π fallita nel **95.33 %** (143/150), condizione `len(_psi_spin_prec) != n` in **143/143**; dopo la cura **0.00 %** (0/60) e `len == n` **60/60**; sigillo **S1-S5 + S1b: 6/6 PASS**, `S1` `max\|A-B\| = 0.000e+00` con `n_A = n_B = 2501` | `doc/REPERTO_psi_spin_prec.md`, `csv/_seal_fork/_sigillo_psi_spin_prec.txt` |
| **C12** | **⚠ SECONDO CASO DEL PUNTO FISSO AUTO-NORMALIZZANTE.** `r` è normalizzato sulla **propria mediana** (`x = f/median(f)`, monotona) ⇒ **`median(r) = 1.0` identicamente, con qualunque orologio.** Quindi `S4` — che confrontava le due mediane — **non poteva misurare nulla**, e il suo `z = 0.00` non significa «nessun effetto» | `median(r)` **1.000000** contro **0.999999**, `z = 0.00`, per costruzione. L'unico numero informativo è la **dispersione**: **0.4421 → 0.4257** (−3.7 %), **un seme, nullo non misurato → C10** | `doc/REPERTO_psi_spin_prec.md` §8; il primo caso e' `_tau`/`_dens_rif` in `CLAUDE.md` §9 |
| **C13** | **⚠⚠ IL TEMPO-LUCE NON E' TESTABILE A QUESTA DENSITA'.** `cs` non e' «quasi-costante per caso»: e' **morto per densita'** (`I ~ 0.05` contro soglia `~400`, §6). Quindi **`tau = d/cs` E' `tau ∝ d`**, e tutto il ramo di lavoro su di esso è, in questo regime, **un ramo su `tau ∝ d`**. **Chi legge «tau = d/cs cablato e misurato» NON deve credere che il canale sia stato provato: non lo è.** | **AGGIORNATO a fine run (500 passi, 4 run): `cs_std/cs_medio` = **0.193 / 0.213 / 0.198 / 0.244 %** — **~4-5 volte** sotto la soglia dell'1 %, non 116. **Il rapporto CRESCE COL SISTEMA:** `0.0086 %` al passo 50 (n~80) → `0.096 %` al passo 300 → `~0.21 %` al passo 500, cioè **venti volte in 450 passi**. **La voce regge** (sotto l'1 %: `tau = d/cs` è `tau ∝ d`) **ma il margine è un quarantesimo di come l'avevo scritto**, e la traiettoria è monotona: **il tempo-luce non è «non testabile mai», è «non testabile a 500 passi»** | serve **`cs` VIVO**: alta densita', oppure il **turbo su GAMMA** — che pero' e' un **esperimento**, non fisica (`doc/COMPONENTI_PROMOSSE.md` C1) |
| **C14** | **ESITO (A) sui QUATTRO BRACCI — nessuna firma emerge nemmeno a risoluzione 6.4x migliore.** E **(A) NON è conclusivo**: `theta` resta oltre il giro per passo | `chi` mat **89.778 / 89.876** (OFF) e **90.048 / 90.084** (ON) contro il null 90.000; autocorrelazione max-z **1.81-2.36** su **40 bin** (il null ne dà 2.2-2.5); frazioni ai poli coincidenti entro il terzo decimale in tutti e quattro; **gradiente `theta` 96.37 → 15.08 = 6.39x** | `theta` sotto il tetto `2π·cs/λ`. Solo allora la frase «lo spin non si organizza» diventa dicibile |
| **C15** | **La firma di |<n>| che «pendeva» È CHIUSA come rumore.** Stamattina 1.741 / 1.374 (`z +2.11`, `+1.16`), *sempre dallo stesso lato* | su 4 run: **1.237 / 0.760 / 0.147 / 0.813**, `z` da `+0.81` a `-1.99` — **due sotto e due sopra** il null empirico `0.9213 ± 0.3888`. **Non si riproduce** | — chiusa, e per la ragione giusta: **piu' dati, non una rilettura** |
| **C16** | **`ESITO (I)` CONFERMATO QUATTRO VOLTE, con la barra giusta.** L'esponente di `omega = coppia/inerzia` non si muove fra semi, bracci e **due leggi di `tau` diverse** | `sigma` = **-1.0498 / -1.0592 / -1.0562 / -1.0554** (`r^2` 0.968-0.973, `n` 2458-3019) contro il **-1.056** del tracing | `doc/REFERTO_S_R_FDT.md` §2-bis |
| **C17** | **LA DISPERSIONE DI `r` E' RUMORE: la FASE 5 non ha, a oggi, NESSUN effetto misurabile.** Ne' sulla mediana (non poteva, C12) ne' sulla dispersione (poteva, e non ne ha). La cura C11 resta giusta — un flag inerte al 95.33 % e' un difetto — ma **il suo effetto fisico resta non dimostrato**, come per C7 (voce **P**) | `ON - OFF = +0.0130 +- 0.0274`, **IC95 [-0.074, +0.100]**, **+3.4 %** in relativo (su 2 semi sembrava ~10 %). Controllo C12: `r_mediana` = **1.000000** su 7 run su 8 | `doc/REFERTO_S_R_FDT.md` §3 |
| **C18** | **IL FDT RIFATTO SUL SISTEMA NON CASTRATO (FASE 5 attiva, `--cs-dinamico` acceso): MIGLIORA DI DUE ORDINI E RESTA INSUFFICIENTE DI TRE. NON SI CABLA** | `lambda` **3.47 -> ~26** (x7.5); `tau_smorz` **28.8 -> 3.7-3.8 passi**; `kT/Lam` **~2e7 -> 1.1e6** (OFF) / **1.5e5** (ON); ma `tau_smorz/tau_disordine` resta **3081** (OFF) / **726** (ON). Il migliore e' **1500 volte** sopra la banda in cui il FDT si applica | `doc/REFERTO_S_R_FDT.md` §4 |
| **C19** | **CHIUSO il 2026-09-16: le due convenzioni di `theta` ora girano INSIEME.** `theta_coord = \|omega\|*DT` (coordinata, la convenzione di C8 e dell'attesa `-0.69`) e `theta_prop = \|omega\|*dt_n` (proprio, quella giusta per §9) sono **entrambe** colonne del CSV, col loro rapporto `r_ratio` (che **e' `r`**). **Controllo di identita' cablato e verificato: `pend(prop) - pend(coord) - pend(r) = 4.6e-16`.** **E ne e' uscita una correzione alla CATENA:** da `\|omega\|_eq = \|F\|*sqrt(dt_n*tau/2)` con `dt_n = DT*r` segue `pend(theta_coord) = sigma + tau/2 + r/2` e `pend(theta_prop) = sigma + tau/2 + 3r/2`. **La formula usata finora, `sigma + tau/2`, ASSUMEVA `pend(r) = 0` in entrambe le convenzioni, e non era mai stato verificato.** Ora `t3_b_r` lo misura | **NB: il DIVARIO e' indipendente dalla convenzione** (`divario_prop - divario_coord = 0`, verificato). Gli 8 CSV gia' committati **non hanno** le colonne nuove: `_verdetto_S_R.py` lo dichiara con «(nessun dato)» invece di inventare | `doc/INVENTARIO_strumenti.md` §3-ter |
| **C20** | **PRIMA MISURA DELLA CONSERVAZIONE DI `L_tot = somma(inerzia*\|omega\|)`, mai fatta prima.** **Cresce del ~3.4 % a ogni passo con crescita**, sia PRIMA sia DOPO la correzione `cs^-2`. **La violazione e' MISURATA, non piu' argomentata** — e la correzione **non la chiude a questa densita'**, com'era scritto PRIMA (fattore `1.0000048` sul nodo mediano) | PRE mediana **+0.0340** (media +0.0413, 517 nodi nati); POST mediana **+0.0355** (media +0.0397, 479 nati). **Il confronto fra i due NON e' significativo** (traiettorie caotiche diverse): conta che **entrambi** stiano a ~3.4 % | `csv/_seal_fork/_sigillo_correzioni.txt`, sigillo **M4** |
| **C21** | **TRE CRITERI DI SIGILLO SBAGLIATI IN UN GIORNO, tutti scritti dal MODELLO MENTALE del codice invece che da una MISURA.** `N3b` (soglia assoluta su un comportamento legittimo), `M1b`/`M3` (misurati nel momento sbagliato), `M3c` (confrontati con la coppia sbagliata). **Un criterio scaduto che produce un FAIL FALSO costa PIU' di un sigillo mancante: si porta dietro una DIAGNOSI** | `M3c` stampava **«nodi nati 0»** — un numero **impossibile**, ed e' il modo in cui un criterio sbagliato si denuncia da solo. Misurato: nati **211**, freschi **194**, differenza **17** = esattamente l'ultima nidiata (`freschi[k] == nati[k-1]`) | presidio in `CLAUDE.md` §9 |
| **C22** | **⚠ LA CRESCITA DI `L_tot` NON E' GUIDATA DALLA MITOSI — il meccanismo del mandato e' SMENTITO dai dati.** Il mandato motivava il fattore `cs^-2` con *«alla mitosi il figlio riceve un'inerzia nuova e il padre non ne perde»*. Misurato: `L_tot` cresce **DI PIU' nei passi SENZA nascite** | su **tutti e quattro** i run: `dL/L` **con** mitosi **+0.0273 / +0.0229 / +0.0176 / +0.0189**; **senza** mitosi **+0.0792 / +0.1591 / +0.1372 / +0.0668** — da **3 a 7 volte** tanto. Conteggi solidi: 347-412 passi con contro 87-152 senza | `doc/REFERTO_baseline_corretta.md` §1. **Il meccanismo esiste (M1 lo ha visto) ma NON e' il termine dominante.** Direzione nuova: guardare i passi SENZA nascite |
| **C23** | **IL FATTORE `(CS_M/cs)^2` NON E' ~1 SULLA CODA a 500 passi.** La mediana resta `1.000020` — il nodo tipico non lo sente — ma il **massimo** arriva a **1.019** e il **6-16 % dei nodi** supera l'1 % | `frac>1%`: **0.000 al passo 50**, **0.057-0.161 al passo 500**; `cs_std/cs` da `6-9e-5` a `1.9-2.4e-3` (= 0.19-0.24 %, **coincide con C13**) | `doc/REFERTO_baseline_corretta.md` §2. **NB: avevo scritto «0.000» nella predizione del turbo citando uno smoke a 60 PASSI** — e' il presidio §9 sulle soglie prese dall'istante sbagliato, violato da me che l'ho scritto |
| **C10** | **⚠⚠ LA BARRA D'ERRORE USATA FINORA E' TRE VOLTE TROPPO PICCOLA.** Su questo sistema **caotico** la pendenza trasversale cambia da run a run di **0.03 a codice INVARIATO**; la `SE` interna a un singolo run vale **~0.010**. **Il valore sotto ipotesi nulla di un confronto fra due run non e' zero** | dispersione fra semi **0.0302** (ramo pre) / **0.0286** (post) contro `SE` interna **~0.010** | `csv/_test_fork/_controllo_semi.txt` |

---

# D. APERTE — la struttura conta piu' dell'elenco

## D.1 — LA CATENA COLLO-DI-BOTTIGLIA (**un** fronte, non tre)

```
 A. cablare tau = d/cs      ->   B. la FORMA del dissipativo   ->   E. sotto-passi per lo spin
    SIGILLO FALLITO oggi          -omega/tau  (FRENA)                SOLO se dopo A e B resta
    (T2/T3/T4): flag OFF,         -lambda n x (n x B)  (ORIENTA)     un residuo modesto
    gate non ri-timbrato          ^ il "tira verso" mancante, ma
    misurato 129.5 -> 43.6          il coefficiente tornerebbe una
    giri/passo (atteso ~9)          SCELTA => manopola. Nodo aperto.
```

> **Questa catena BLOCCA tutto il resto.** Finche' lo spin e' aliasato **ogni misura su di esso e'
> nulla**, e le quattro voci di §B restano da rifare. **A e' il collo di bottiglia dell'intero
> programma.**

| # | stato | criterio di chiusura |
|---|---|---|
| **A** | `--tau-luce` cablato, **SIGILLO ANCORA FALLITO**. T2 resta da riscrivere (il monkeypatch colpiva il metodo **condiviso**). T3 **rifatto oggi** dopo la cura della cache (C7), e poi **su 3 semi**: ON post medio **-0.4745** contro l'attesa **-0.69**, divario **-0.2155** a **z = 13.1**, e `theta` resta a **30.7-44.9 giri/passo**. *(La lettura intermedia «un sesto recuperato» e' stata **RITIRATA**: era dispersione di run — C10.)* `doc/SIGILLO_tau_luce_FALLITO.md`, `doc/FIX_cache_cs.md` §6 | T1-T5 tutti PASS, **e** `theta` sotto il tetto `2π·cs/λ` |
| **B** | **CHIUSA COME NON DERIVABILE** (2026-09-16). Il coefficiente di `−λ n×(n×B)` sarebbe una **scelta** (§3), e ora ci sono **TRE ragioni indipendenti** per cui non si deriva: ① il **FDT** licenzia un `λ` ~10⁴ volte troppo lento (`doc/ANALISI_gilbert_fdt.md`); ② la **FASE 1 LLG** ha mostrato che il punto di cablaggio proposto non produce allineamento e che la dinamica esistente orienta verso `−B` (`doc/FASE1_gilbert_llg.md`, commit `8fa052c`); ③ **NON ESISTE UN BILANCIO da cui farlo uscire** — lo spin e' **accoppiato ma senza grandezza conservata**: il torque `cross(B_i, nb_i)` **non e' azione-reazione** (normalizzazione per `deg_i` diversa fra i due estremi, e la riflessione `z→−z` sui legami omochirali rompe l'antisimmetria **nella struttura**), e nel file **non esiste nessuna funzione di energia totale** (`doc/MAPPA_accoppiamenti_spin.md`). **NB: il terzo argomento e' DIMOSTRATO dalla formula, l'AMPIEZZA della violazione non e' misurata** | riaprirebbe **solo** una derivazione del coefficiente da un principio, cioe' la voce **L**. **Misura che manca e costa poco:** `|Σᵢ cross(Bᵢ,nbᵢ)| / Σᵢ |cross(Bᵢ,nbᵢ)|` — `~1/√n` = rumore di somma, `O(1)` = violazione grande |
| **E** | **non aperto**, e **non va aperto ora**: risolverebbe i giri **senza abbassare `omega`**, cioe' integrerebbe bene una rotazione che **viola il tetto di causalita' del modello**. Il fine non e' risolvere `omega`: e' **farlo rientrare nel tetto** | solo dopo A e B, e solo per un residuo modesto |

## D.2 — CANALI MAI TESTATI (**nessuna misura li esclude**)

| # | fronte | perche' e' aperto | criterio di chiusura |
|---|---|---|---|
| **C** | il fattore **`cs^−2` mancante nell'inerzia** ⇒ `cs` entrerebbe nello spin **via la MASSA**, non via l'orologio | esito **(b)** di `doc/INERZIA_tempo_quadro.md`: il fattore **manca nel codice** (zero occorrenze di `cs` in tutto il percorso che costruisce `Psi`). Le sei misure riguardano **solo** lo Step 2, che e' fase globale | cablarlo con flag+sigilli **e** misurare a densita' dove `cs ≠ CS_M` |
| **I** | **correlazione genealogica** (parentela → spin) | l'albero e' **ricostruibile** (FASE A del bilancio, 100% su 7/7 e poi 4163 coppie). **Misura mai fatta:** `<n_i·n_j>` per **grado di parentela**, non per distanza spaziale | l'osservabile esiste gia' (osservatore sigillato): serve solo farla |
| **R** | **REFUTATA (2026-09-16).** L'anello avrebbe dovuto far cambiare `sigma` al cambiare di `tau`. **Cambiando `tau` di DUE ORDINI DI GRANDEZZA** (pendenza **+1.708** OFF -> **+0.020** ON) **`sigma` NON SI MUOVE: -1.0545 contro -1.0558, differenza 0.0013 — VENTITRE VOLTE sotto la barra di sistema (0.030, C10).** E l'attesa ricalcolata **peggiora** il divario invece di chiuderlo (ON **+0.386**, IC95 [+0.054, +0.718], **esclude lo zero**). **Non cerco un colpevole nuovo (P1)** | chiusa come meccanismo. **Resta NON SPIEGATO il residuo positivo** in entrambi i bracci (**+0.126** OFF, **+0.386** ON) -> voce **R2** |
| **R2** | **NUOVO: il residuo della catena `theta = sigma + tau/2` non e' spiegato, E TENSIONE CON C3.** C3 lo dava **transitorio** (`0.979 -> 0.010` fra i passi 50 e 400); a **500 passi** vale **+0.126** (OFF) e **+0.386** (ON). **⚠ PRIMA DI TOCCARLO va sciolto il §0 del referto: `theta` e' misurato in DUE CONVENZIONI DIVERSE** (`\|omega\|*DT` in `_rimisura_t3.py`, `\|omega\|*dt_n` in MISURA F). Puo' essere tutta li' | rimisurare **entrambe** le convenzioni nello stesso run: costa **una riga** (`g` contiene gia' `om_src` e `dtn`), **zero run nuovi** |
| **S** | **CHIUSA COME RUMORE (2026-09-16), per il criterio scritto prima.** 4 semi per braccio: OFF media **89.872** sd 0.094 **IC95 [89.722, 90.022]**; ON media **90.049** sd 0.034 **IC95 [89.995, 90.103]**. **Entrambi CONTENGONO 90** -> l'ipotesi si RITIRA, non si raffina. E il segno concorde non regge nemmeno come indizio: `OFF s3` vale **89.9999**, il null esatto | chiusa. `doc/REFERTO_S_R_FDT.md` §1 |
| **S2** | **NON SI RIPRODUCE sul sistema corretto, E CAMBIA SEGNO** (2026-09-16, baseline `c57800c1`). Il contrasto `chi` ON-OFF era **+0.1769** e ora vale **-0.146**: il braccio **OFF** si e' spostato da **89.872** (4 semi, sd 0.094) a **90.130** (2 semi), cioe' **+0.26 gradi = 2.7 volte** la sua dispersione fra semi. **E' il cambiamento piu' grande prodotto dalle tre correzioni.** **⚠ E NON si dichiara una firma nell'altro verso:** l'IC95 di OFF esclude 90 ma i due semi concordano a **0.004 gradi**, e con **1 grado di liberta'** una coincidenza fra due punti da' un intervallo **spuriamente stretto** | **>= 4 semi per braccio.** Cio' che e' stabilito e' solo che il `+0.177` **non si riproduce** |
| **P** | **la cura della cache ha un effetto fisico?** — **INDECIDIBILE con 3 semi** | `Delta` per seme: **-0.0445 / +0.0367 / -0.0635** → **segno NON concorde**. `media -0.0238`, `SE 0.0307`, `t = -0.77`. **`IC95 = [-0.156, +0.108]` contiene lo ZERO *e* contiene il `-0.120` dell'ipotesi «~meta'» del mandato.** Nessuna delle due e' esclusa: l'esperimento **non ha potenza** | piu' semi (~12 per una `SE` di 0.015), **oppure** una misura che non passi da un confronto fra traiettorie caotiche |
| **J** | **quantizzazione delle masse**: esistono taglie preferite? | `massa_critica_collasso()` e' una **soglia**, e le soglie **selezionano** | istogramma delle masse, coi **picchi verificati al cambio di binning** (un picco che sparisce non e' un picco) |

## D.3 — SETTORI INTERI MAI INTERROGATI

| # | fronte | nota |
|---|---|---|
| **G** | **metrica / densita'** col rigore dato allo spin | pista indicata da Luca: e' li' che sarebbe avvenuto il **salto del raggio 0.8 → 13.2** mentre le firme di spin restavano piatte. **NON verificato in questo giro**: i due numeri non sono stati ricontrollati dai dati, e vanno confermati prima di usarli |
| **F** | il canale del **SEGNO** (doppia copertura) | **ATTENZIONE, e' un limite strutturale:** e' **`Z2`, abeliano**. Riguarda materia/antimateria e la carica, **NON puo' produrre la struttura non-abeliana del fork.** Aprirlo sperando che dia il non-abeliano sarebbe un errore di categoria |

## D.4 — IGIENE / INFRASTRUTTURA

| # | fronte | stato **verificato oggi** | criterio |
|---|---|---|---|
| **H** | **purezza dei diagnostici**: `calcola_psi()` **scrive** `self.psi` ed e' chiamata da `circolazione_topologica` (~1467), `diagnostica` (~5448), `_picchi_nuovi` (~6184) | **⚠ PIU' STRETTO DI COME E' STATO POSTO.** Il **percorso batch e' GIA' PROTETTO**: snapshot/restore espliciti di `psi`, `_psi_prec`, `_psi_spinor`, `_nb`, `psi_spin`… **e dello stato RNG**, alle righe **6300-6319** (diaglog) e **6357-6419** (condensazione) — verificato dal sorgente. **Tutte le misure di questo programma vengono da li'.** Il rischio resta sul percorso **GUI/video** (`update()`), non protetto. **AGGIUNTO 2026-09-15:** sullo stesso percorso GUI c'e' la **terza via di crescita dei nodi**, `semina()` (`:1600`), che **non** passa da `_eredita_spinore_figli` e quindi **lascia la cache `_cs_nodo_prev` corta** anche dopo la cura (C7). In batch e' inerte: `semina_cont=False` di default, si accende **solo** dalla GUI (`:4610`, `:4753`) | test binario **sul percorso GUI**: run con/senza diagnostiche → byte-identico? **e** contatore `_cs_fallback` a zero con `semina_cont` acceso |
| **K** | **merge in `main`** (fork-su2 come linea unica) | **PIANO SCRITTO, NON ESEGUITO** (2026-09-16, `doc/PIANO_merge_main.md`). **Il fatto che cambia il quadro: `main` NON HA MAI TOCCATO `soliton_simulator.py`** — il suo blob e' quello della merge-base (`194a9456`), i suoi 20 commit sono **tutta documentazione**. Non e' un merge di codice, e' un merge di **racconto**: conflitti **solo** su `CLAUDE.md` e `CLAUDECONNECT.md` (prova a secco con `git merge-tree`). Dei tre presidi: il **rename dello STATO** e' **gia' risolto** (`main` non ha NESSUN file di STATO; quello a rischio e' di `dev-spinoriale`, e solo se si cancella quel branch); l'**AVVISO** e' **chiuso** oggi; il **ri-timbro del gate NON e' risolvibile** finche' A e' aperta. **Trappola operativa vera:** `main` e' estratto in un **worktree separato** (`C:/Users/lpeano/st_main`). **RACCOMANDAZIONE: non adesso** — `main` e' oggi l'unico branch il cui codice coincide con un blob certificato, e portarci `08784685` significherebbe perdere l'ultimo punto fermo mentre A e' aperta | **decisione di Luca.** Il costo-zero che toglie il 90 % del danno: una riga in testa a `CLAUDE.md` **di `main`** che dica «branch FERMO al 2026-09-10, il lavoro vivo e' su `fork-su2`» |
| **M** | **ottimizzazione** | **due cose da NON fare, gia' accertate:** il loop CFL **non e' il collo** (`doc/PROFILAZIONE_costo_run.md`); `_pesi` e' una **ricorsione**, non 16 ricalcoli (`doc/REPERTO_pesi_ricorsione.md`). **Resta il costo, non la cura** | una misura che mostri un collo **diverso** da quelli gia' esclusi |
| **D** | rumore **bianco senza taglio spettrale** (catastrofe UV discreta) | **CABLATO il 2026-09-16 dietro `--rumore-colorato`, FLAG OFF** (blob `08784685` -> `c5e5088c` -> `a467fd9a`), dopo il via libera di Luca sulla predizione CORRETTA. OU con `tau_c = LAM/CS_M` = 0.400 = **40 passi**, `dt_n = DT*r` (non `DT`), **`amp` INVARIATA**, zero coefficienti. **SIGILLO A META': N1.0, N1.0b, N1 (`max\|A-B\| = 0.000e+00`, nodi 3020 = 3020) e N1b PASS; poi SI E' SCHIANTATO** a N7 (`AttributeError: Generator.normal is read-only`): **N2, N3, N6 e N7 NON sono girati**. Corretta la spia (proxy sull'OGGETTO `rng`), da rigirare. **Difetto trovato leggendo il chiamante:** `_passo_spinoriale` riceve `dt_n_s`, che sotto `--tempo-segno` e' **NEGATIVO** per l'antimateria -> `a > 1` -> la ricorsione **sarebbe divergita in silenzio**; da qui la guardia `\|dt_n\|`. **E il criterio di N3b era MIO ed era sbagliato:** «fallback <= 1» in assoluto avrebbe fatto fallire il sigillo per una ragione **legittima** (l'estensione scatta su `semina`/`nuova_massa`, la voce **H**, dove e' CORRETTA: i nodi esistenti conservano `xi`, solo i nuovi ricevono un'estrazione stazionaria). Corretto in **DELTA** sui passi di sola mitosi | **N7 e' quello che decide** (la ricorsione usa `dt_n` per nodo? col `DT` nudo N1..N6 passerebbero IDENTICI — e' il bug dello Strato 1 che solo S7 stano'), poi la campagna `{OFF, ON} x >= 2 semi`. **PREDIZIONE INVARIATA:** `theta` non scende, e se si muove SALE (<= 5 %). Un calo significativo sarebbe un reperto **a mio carico** | `doc/PREDIZIONE_taglio_spettrale.md`, `csv/_seal_fork/_sigillo_rumore_colorato.txt` |
| **N** | `python soliton_simulator.py --help` e' **rotto** (`%` non escapato in una help string) | **preesistente**, verificato sulla copia pre-modifica: non introdotto da noi | l'help si stampa |

## D.5 — IL PROGRAMMA LUNGO

| # | | |
|---|---|---|
| **L** | **l'azione unica / la lagrangiana** da cui derivare tutto, memorie incluse (Mori-Zwanzig) | E' cio' che renderebbe il modello **falsificabile** invece che soltanto coerente. **Non e' un task: e' la direzione.** Per la regola 3 non e' un fronte — non ha un osservabile che lo chiuda — ed e' qui per questo, in una sezione a parte |

---

# REGOLE DI MANUTENZIONE — **la parte che conta**

1. **Una voce si sposta di sezione solo con un RISCONTRO committato** (numero + file), **mai per
   impressione**.
2. **Chiuse per DIMOSTRAZIONE e chiuse per MISURA non si mescolano MAI.** Le prime sono definitive;
   le seconde portano **sempre** la condizione che le renderebbe da rifare.
3. **Ogni voce ha: stato, il documento/commit che la sostiene, e il criterio che la chiuderebbe.**
   Una voce **senza criterio di chiusura non e' un fronte: e' un desiderio** → sezione a parte
   (oggi: **L**).
4. **Si apre un fronte nuovo solo dichiarando quale osservabile lo chiuderebbe.**
5. **Il registro si aggiorna nello STESSO commit del riscontro** che lo cambia (§5-bis).
6. **ORDINE DI LAVORO:** la catena **D.1 ha precedenza assoluta**; **H in parallelo**, perche' e'
   piccolo e mette in dubbio ogni misura; **tutto il resto non si apre finche' A non e' chiuso.**
7. **Un fronte fermo per piu' di 3 sessioni va o chiuso o dichiarato DORMIENTE**, con la ragione.
   Un fronte aperto e mai toccato e' **rumore nel registro**.

> **E una regola che viene dall'esperienza di oggi:** un numero entra qui **solo se e' nel repo**.
> Due numeri del mandato che ha creato questo file non ci sono (vedi nota su **A2**): non li ho
> scritti. **Il registro non e' il posto dove i numeri nascono.**
