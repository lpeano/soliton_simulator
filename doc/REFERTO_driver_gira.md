# REFERTO — UN DRIVER CHE FORZA UN FLAG IN TUTTI I BRACCI RENDE L'A/B NON ATTRIBUIBILE

**Data:** 2026-09-17 · **Branch:** `fork-su2` · **Sollevato da:** Luca, come reperto a sé.

---

## 1. IL DIFETTO

`csv/_test_fork/_esperimento_spin_feedback.py`, funzione `gira()`, versione che ho scritto per prima:

```python
def gira(tag, extra, passi=120, seme=5):
    cmd = [... , "--cs-dinamico", "--tau-a", "2.0"] + list(extra) + [...]
```

`--tau-a 2.0` stava nella **lista comune**, cioè nel pezzo di comando che **ogni** braccio riceve.
Il terzo braccio — quello che doveva essere il **riferimento a `TAU_A = 50`** — lo riceveva anche lui.

**Conseguenza:** il "riferimento" non era un riferimento. Confrontare `TAU_A = 2.0` con
`TAU_A = 2.0` e chiamarlo A/B su `TAU_A` è **misurare la differenza fra un run e se stesso**, cioè
il rumore del caos, con l'etichetta di un effetto.

**La forma generale, ed è questa che va ricordata:**

> **Un driver che costruisce i bracci come `comune + variabile` sposta il confine fra i due a ogni
> riga che si aggiunge alla lista comune. Un flag messo lì non è più una variabile: è una
> costante — e se è proprio quello che si voleva variare, l'esperimento non ha un braccio di
> controllo, e NESSUN messaggio lo dice.**

È della stessa famiglia già catalogata in CLAUDE.md par.9 sotto *«quando si ribalta un default, si
cercano TUTTI i punti che ottenevano il vecchio comportamento per OMISSIONE»*: lì un default
ribaltato **converte i rami di controllo in duplicati del ramo di prova**; qui lo fa una riga del
driver. **In entrambi i casi il sigillo/esperimento continua a PASSARE**, perché confronta due cose
identiche e le trova identiche.

---

## 2. HA CONTAMINATO L'ESPERIMENTO `TAU_A = 2.0` DI IERI? — **NO.** Verificato **dai dati**.

La domanda non si risponde dal comando (che si può ricordare male) ma dal **blocco di
certificazione scritto nel CSV** — è esattamente l'uso per cui P6 esiste.

Il simulatore scrive in testa a ogni CSV una riga `# RUN_PARAMS {...}` con, fra gli altri,
`tau_a_over` (l'override da riga di comando) e `leggi_attive.REGIME`.
**`TAU_A` in sé NON è scritto: si DEDUCE** da `REGIME` + `tau_a_over`
(`deterministico` → 50.0, `canonico` → 2.0).

| file | REGIME | `tau_a_over` | **`TAU_A` effettivo** | SPIN_FEEDBACK | seed |
|---|---|---|---|---|---|
| `_exp_tau50.csv` | deterministico | `null` | **50.0** | False | 5 |
| `_exp_tau02.csv` | deterministico | `2.0` | **2.0** | False | 5 |
| `_e5_pre.csv` | deterministico | `2.0` | 2.0 | False | 5 |
| `_e5_post.csv` | deterministico | `2.0` | 2.0 | False | 5 |

**Il riferimento di ieri era `TAU_A = 50`.** Il driver `_esperimento_tau_a.py` chiama
`gira("tau50", [])` con `extra` **vuoto** e non ha mai avuto `--tau-a` nella lista comune
(verificato dal blob committato a `f0bf4db`, righe 40-58).

**Quindi: l'esperimento di ieri REGGE, i suoi numeri valgono, e la "terza lettura"
(*regge con segni di stress*) resta.**

### 2-bis. CONTROPROVA INDIPENDENTE, e non era scontata

Il `−32 %` ricalcolato **dalla colonna `n_tot` dei CSV di ieri**:

```
tau50  n_tot al passo 120 = 2577      tau02  n_tot al passo 120 = 1754     ->  -31.9 %
```

E il braccio `rif` del run di **oggi** — un processo diverso, lanciato dal driver **corretto** —
dà **2577 nodi esatti**. **Due riferimenti indipendenti, stesso numero.**
*(Su un sistema caotico questo non è banale: dice che a seme e flag identici il run è deterministico
e riproducibile, cioè che la divergenza fra i bracci viene dai flag e non dal rumore di esecuzione.)*

---

## 3. ALTRI ESPERIMENTI SONO PASSATI DI LÌ? — verificato, **no**, con un limite dichiarato

Scansione di tutti i `.py` sotto `csv/` che lanciano il simulatore in sottoprocesso con `--batch`
(34 file; escluse le copie storiche `_old_sim_pre_*.py` e i `._sim.py`, che sono **copie del
simulatore**, non driver).

**Solo 8 hanno più di un braccio**, e in nessuno la lista comune contiene un flag che quel
particolare esperimento stia variando:

| driver | bracci | esito |
|---|---|---|
| `_sigillo_pezzo3.py` | 2 | pulito |
| `_sigillo_rumore_colorato.py` | 3 | pulito |
| `_sigillo_step2.py` | 3 | pulito |
| `_sigillo_strato1.py` | 3 | pulito |
| `_misura_tw.py` | 3 | pulito |
| `_sigillo_osservatore.py` | 4 | pulito |
| `_esperimento_tau_a.py` | 2 | `--fork-su2-mem` comune — **voluto**: è la configurazione fissa |
| `_esperimento_spin_feedback.py` | 3 | `--fork-su2-mem` comune — idem; il difetto era `--tau-a`, **ora corretto** |

**IL LIMITE, e va detto perché altrimenti questa tabella vale meno di quanto sembra:** la scansione
guarda il **disco di oggi**, e il driver difettoso **è già stato corretto**. Il mio primo
rilevatore automatico — quello che cercava un flag presente sia nella lista comune sia fra le
varianti — ha restituito **zero collisioni, compreso il file che aveva il bug**.
**Un rilevatore che non trova il caso che lo ha generato non è un presidio**, ed è la ragione per
cui la tabella sopra è stata rifatta a mano sul criterio *«quanti bracci, e quale flag è la
variabile»*. La conclusione «nessun altro contaminato» vale per lo **stato attuale del disco**;
per i run **già girati** vale il metodo del par.2: **si legge `# RUN_PARAMS` dal CSV**, non il
driver.

---

## 4. IL PRESIDIO CHE NE DISCENDE

**Un A/B si certifica dai DATI dei suoi bracci, non dal codice del driver.** Il driver dice cosa
*si intendeva* lanciare; il blocco `# RUN_PARAMS` dice cosa *è stato* lanciato. Quando divergono,
ha ragione il CSV.

**E una lacuna P6 trovata strada facendo, da sanare:** nel blocco `# RUN_PARAMS` **non compaiono
né `TAU_A` né `G_PH` né il `blob`**. `TAU_A` è oggi *deducibile* (da `REGIME` + `tau_a_over`), e
`blob` **non lo è affatto** — mentre CLAUDE.md par.9 chiede esplicitamente **blob, seme e tutti i
flag** in ogni CSV di misura. È lo stesso caso del braccio OFF a cui mancava `TAU_LUCE`:
**il run non è sbagliato, è non-certificabile dai suoi dati.**
Qui si è salvato perché `tau_a_over` c'era; se avessi dovuto dedurre `TAU_A` dal solo `REGIME`,
l'override sarebbe stato **invisibile nei dati** e questa verifica **non sarebbe stata possibile**.

---

## 5. COSA NON DICE QUESTO REFERTO

- **Non dice che il driver fosse committato.** `_esperimento_spin_feedback.py` risulta `??`
  (non tracciato) in `git status`: il commit `d3874fd`, che si intitola *«Committato PRIMA del
  run»*, conteneva **il simulatore e le previsioni**, non il driver. Par.5 chiede che il codice che
  genera un output sia già committato quando l'output nasce: **per il driver non è stato fatto.**
  Va committato **ora, insieme ai dati**, con questa nota accanto — non «tanto poi lo committo».
- **Non dice che l'esperimento `SPIN_FEEDBACK` sia valido**: dice solo che la sua **base**
  (il `−32 %`) regge. La lettura dell'esperimento è in `doc/REFERTO_esperimento_spin_feedback.md`.
