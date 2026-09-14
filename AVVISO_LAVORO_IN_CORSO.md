# ⚠ AVVISO — LAVORO IN CORSO (2026-09-14, fine giornata)

> **Leggi questo PRIMA di trarre conclusioni dal repo.** Branch `fork-su2`.
> Scritto per chi legge il repo da fuori (Claude web / chiunque riprenda) e potrebbe avere uno
> snapshot vecchio o trovare il codice in uno stato intermedio.
> **Aggiornato al commit `3d2c9e5`.**

---

## 1. DUE COSE CHE SEMBRANO ERRORI E NON LO SONO

### 1.1 — Il blob sul DISCO non coincide con quello CERTIFICATO. È VOLUTO.

| | |
|---|---|
| blob di `soliton_simulator.py` **sul disco** | **`c0803713`** |
| blob **certificato** in `CLAUDE.md` §0 | **`2277e9a0`** |

Il `.py` sul disco è **avanti** di un cablaggio (**STEP 2**, `--step2-orologio`) **il cui sigillo è
FALLITO**. Il gate **non** è stato ri-timbrato, di proposito: ri-timbrare su un cablaggio non
sigillato sarebbe un timbro falso.

**Non "correggere" il disallineamento aggiornando CLAUDE.md.** Va risolto in un senso o nell'altro
(sigillo corretto → ri-timbro, oppure rollback del cablaggio), ed è una decisione di Luca.

**La baseline NON è contaminata:** S1 e S2 del sigillo Step 2 **passano** (`0.000e+00`, nodi
3164 vs 3164, 0 shape divergenti). A flag spento il codice è **byte-identico** a `2277e9a0`.

### 1.2 — Il sigillo dello STEP 2 fallisce, ma NON sappiamo se il cablaggio sia sbagliato

`S3` misurava `1.000000000000` per ogni `cs`. **Diagnosi provata:** nel setup del test
`omega_clk` vale **esattamente 0** (dopo `semina()`, `eta = 0` → `ramp = 0` → pesi nulli → `den = 0`).
Moltiplicare zero per `(cs/CS_M)^2` dà zero, e la fase misurata veniva **tutta dalla precessione**.

- **PROVATO:** il sigillo è **cieco**.
- **NON PROVATO:** che il cablaggio sia corretto. **Un test cieco non assolve.**
- Il prossimo passo è correggere lo **STRUMENTO**, non il cablaggio — sapendo che oggi **non
  sappiamo** se il cablaggio sia giusto.

---

## 2. C'È UN ESPERIMENTO IN VOLO IN QUESTO MOMENTO

**SHAKE-THEN-FREEZE.** Predizione scritta e committata **prima** dei run:
`doc/PREDIZIONE_shake_then_freeze.md` (commit `d0f3de6`).

**La domanda** (di Luca): *"serve un periodo di scuotimento caotico prima del test?"*
- Nella lettura **ricottura**: **no, dimostrato** (l'accoppiamento ordinante è **zero**, e la
  diffusione sulla sfera ha una sola distribuzione stazionaria, l'uniforme).
- **Ma apre un esperimento mai fatto:** il braccio OFF si congelava al polo **solo perché partiva
  dal polo** — lo stato più degenere possibile, punto fisso esatto per simmetria. Scuotere **e poi
  smettere** congela una configurazione **casuale**, che nel punto fisso **non è**.
- **La domanda vera: qual è l'attrattore della SOLA precessione, da uno stato casuale?**

**Protocollo:** fase 1 scuotimento ON (300 passi) → `--sync-db` salva; fase 2 **resume dallo stesso
DB** con `--regime deterministico` (spegne **solo** `SCUOTIMENTO`, sigillato O2), 600 passi.
Zero modifiche al simulatore.

**⚠ Se trovi i file `csv/_test_fork/_vuoto_stf_*` senza un commit di ESITO, il run non è finito o
non è stato letto. NON leggerli come risultato.** L'esito, quando c'è, sta in un commit dedicato e
in coda a `doc/PREDIZIONE_shake_then_freeze.md`.

---

## 3. QUELLO CHE È CHIUSO, E COME VA DETTO

**Quattro misure indipendenti sono UN fatto da quattro lati: il settore di spin non ha una forza
organizzante emergente.**

1. **Teorema di inerzia** — la connessione è uno **specchio** della materia (1.57e-15).
2. **Frozen-o-noise** — ciò che specchia è **rumore**. Senza scuotimento i Bloch **non si muovono**
   (`|⟨n⟩| = 1.000000` sul polo per 300 passi); con scuotimento sono rumore bianco **ovunque**,
   materia compresa (χ = 90.0 ± 39.2 contro l'atteso casuale 90.000 ± 39.171).
3. **Kuramoto REFUTATO** — allineamento locale aggiunto **non basta** a vincere il rumore.
4. **FDT** — nel rumore **non c'è dissipazione compagna**: `E[n'] − n = −a²·n`, senza `{n_k}`.
   **Dimostrato**, non solo misurato. È l'unico dei quattro che **spiega** gli altri tre.

**Formula onesta:** le tre porte ovvie (precessione / rumore / Kuramoto) sono **chiuse**. Se si
vuole struttura di spin, va **imposta e dichiarata**, o trovata in una fisica **non ancora
identificata**. Non è un fallimento: è **conoscenza convergente**, e chiude vie invece di lasciarci
cercare dietro porte chiuse.

**Cosa NON dire:** che il fork "funziona" o "riproduce la gravità". Lo Strato 1 è sigillato 23/23 e
la formula corretta è **«il fork non è più inerte»**. Olonomia `W(r)`, stabilità lunga e verso della
gravità **non sono stati misurati**, e sotto ~2000 passi / un solo seme non si conclude (§2.7).

---

## 4. TRE ERRORI DI LETTURA GIÀ PAGATI — non ripeterli

1. **`N = 3164 → 3209`** a 150 passi sembrava un effetto del fork: era **rumore a 1e-16 amplificato
   dal caos**.
2. **`max|A−B| = 0.000e+00`** sembrava identità: era **mancanza di confronto** (3209 nodi contro
   3073, 32 shape su 32 divergenti). **Guardare sempre prima il conteggio nodi.**
3. **`spin_ovl = 0.5` e `χ ≈ 90° ± 39°` non sono numeri qualunque:** sono **esattamente** i valori
   di direzioni di Bloch **casuali**. Chi li vede deve riconoscerli.

**La regola che li copre** (ora in `CLAUDE.md` §9): *prima di leggere una statistica riassuntiva,
chiediti che valore avrebbe **se non ci fosse niente**.*

*(Aggiunta di oggi: attenzione anche a **media contro mediana**. Il grado dei nodi ha media 119 e
**mediana 2** — usare la media come "tipico" inganna.)*

---

## 5. DOVE LEGGERE I DETTAGLI

| documento | cosa contiene |
|---|---|
| `STATO_CLAUDE_fork-su2.md` | **parti da qui**: sezione `>>> PER CHI RIPRENDE` in testa |
| `CLAUDECONNECT.md` §44–58 | il racconto cronologico, **con gli errori e come sono stati trovati** |
| `doc/AUDIT_misurato_vs_asserito.md` | cosa nel corpus è **misurato**, cosa solo **asserito**, cosa **smentito** |
| `doc/INDAGINE_scuotimento.md` | cos'è lo scuotimento, le ampiezze misurate, la trappola `--regime` |
| `doc/PREDIZIONE_*.md` | le predizioni scritte **prima** dei run, con gli esiti in coda |

**⚠ Le fonti auditate NON sono state corrette** (`ROADMAP:46` e `:42`, `PROTOCOLLO:41-44`,
`STATO:112` e `:433`): chi le legge **senza** l'audit prende ancora un'asserzione per una misura.
È una decisione di Luca, non una svista.
