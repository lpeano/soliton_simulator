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

> **⚠ SECONDO MARCHIO, aggiunto il 2026-09-15 sera — L'OROLOGIO.** Tutte le misure di questo repo
> fino al blob `08784685` sono state prese con il **ritmo SCALARE a 2π**: la doppia copertura
> (**FASE 5, 4π**) **non era attiva** (95.33 % di scarto della guardia, **C11**).
> **Non erano «integrate male»** — `r` era ricalcolato a ogni passo e valido; erano misure di un
> **modello diverso da quello che il flag dichiarava**.
> **Condizione da riverificare col settore 4π in funzione**, e vale **anche per T3 e i suoi quattro
> bracci**, cioè per il divario stesso che stiamo inseguendo.
>
> **⚠ TERZO MARCHIO — `cs` COSTANTE (2026-09-15, rilievo di Luca, verificato dal disco).**
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
| **B** | **non aperto.** Il nodo e' che il coefficiente di `−λ n×(n×B)` sarebbe una **scelta** (§3), a meno di derivarlo — e il FDT **non basta** (`doc/ANALISI_gilbert_fdt.md`: ~10⁴ volte troppo lento) | una derivazione del coefficiente **senza** taratura |
| **E** | **non aperto**, e **non va aperto ora**: risolverebbe i giri **senza abbassare `omega`**, cioe' integrerebbe bene una rotazione che **viola il tetto di causalita' del modello**. Il fine non e' risolvere `omega`: e' **farlo rientrare nel tetto** | solo dopo A e B, e solo per un residuo modesto |

## D.2 — CANALI MAI TESTATI (**nessuna misura li esclude**)

| # | fronte | perche' e' aperto | criterio di chiusura |
|---|---|---|---|
| **C** | il fattore **`cs^−2` mancante nell'inerzia** ⇒ `cs` entrerebbe nello spin **via la MASSA**, non via l'orologio | esito **(b)** di `doc/INERZIA_tempo_quadro.md`: il fattore **manca nel codice** (zero occorrenze di `cs` in tutto il percorso che costruisce `Psi`). Le sei misure riguardano **solo** lo Step 2, che e' fase globale | cablarlo con flag+sigilli **e** misurare a densita' dove `cs ≠ CS_M` |
| **I** | **correlazione genealogica** (parentela → spin) | l'albero e' **ricostruibile** (FASE A del bilancio, 100% su 7/7 e poi 4163 coppie). **Misura mai fatta:** `<n_i·n_j>` per **grado di parentela**, non per distanza spaziale | l'osservabile esiste gia' (osservatore sigillato): serve solo farla |
| **R** | **L'ATTESA `-0.69` E' CALCOLATA BENE?** — l'anello `tau → omega → phi → psi → inerzia → sigma` rende `sigma` **a valle** di `tau`, ma la predizione usa il `sigma` del braccio **vecchio** (`-1.078`). **Non propone un colpevole nuovo: mette in dubbio il BERSAGLIO.** Unica ipotesi sul tavolo che **non** richiede di trovare qualcosa di rotto ⇒ **va provata per prima** | **nessuno ancora.** ⚠ il rilievo lo dava per «già nei dati dei quattro bracci»: **verificato falso** — `_rimisura_t3.py` ha **zero occorrenze** di `coppia`/`sigma` e le reti non sono persistite. **Serve un run** | misurare `sigma`, `tau`, `theta` **nello stesso run** (3 semi × 2 bracci) e **ricalcolare** l'attesa `sigma + tau/2` col `sigma` **di quel braccio**: se l'attesa ricalcolata si avvicina al misurato **entro la barra giusta (0.03)**, il divario era un artefatto della predizione; se no, **l'anello non era la causa** |
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
| **K** | **merge in `main`** (fork-su2 come linea unica) | tre presidi noti: rename del file di STATO, **ri-timbro del gate**, AVVISO da aggiornare o cancellare | merge fatto coi tre presidi eseguiti |
| **M** | **ottimizzazione** | **due cose da NON fare, gia' accertate:** il loop CFL **non e' il collo** (`doc/PROFILAZIONE_costo_run.md`); `_pesi` e' una **ricorsione**, non 16 ricalcoli (`doc/REPERTO_pesi_ricorsione.md`). **Resta il costo, non la cura** | una misura che mostri un collo **diverso** da quelli gia' esclusi |
| **D** | rumore **bianco senza taglio spettrale** (catastrofe UV discreta) | **oggi ESCLUSO:** `R_stoc = 0.041` — il rumore non guida `omega` | si riaprirebbe solo se `R_stoc` risultasse ≫ 1 in un altro regime |
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
