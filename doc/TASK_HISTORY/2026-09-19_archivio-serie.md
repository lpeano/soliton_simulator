# TASK HISTORY — **l'archivio: serie numerata, gzip, RIGIOCA. E il generatore È uno solo**

**Data:** 2026-09-19 · **Branch** `fork-su2` · **HEAD alla scrittura** `24add7d`
**Blob:** `b9e07c73` *(git blob)* · **byte grezzi:** `2a7207a4` · **albero PULITO**
**HDF5 SCARTATO per decisione di Luca. `gzip` sullo stesso `pickle`.**
**Tutto dev'essere BYTE-INERTE sulla fisica: è salvataggio, non dinamica.**

---

## 1. RAGIONAMENTO PRELIMINARE

### 1.1 ✅ **§1 — IL GENERATORE È UNO SOLO.** Verificato dal disco, in modo esaustivo

```
np.random / numpy.random        -> UNA sola occorrenza:  :1010  self.rng = np.random.default_rng(seed)
import random / from random     -> NESSUNA
random.random|randint|choice|shuffle|uniform|gauss|seed  -> NESSUNA
RandomState / Generator(        -> NESSUNA
self.rng                        -> 20 usi, tutti sullo stesso oggetto
net.rng                         -> :537, :4705 (alias locale), :4714, :4715, :5490 -- LO STESSO oggetto
```

> **Non esiste una seconda sorgente di casualità.** **`rng_state` è salvato (`:2860`) e ripristinato
> (`self.rng.bit_generator.state = stato['rng_state']`), quindi la riproduzione da snapshot ha tutto
> ciò che le serve.** **SI PROCEDE.**

**⚠ E una riserva che dichiaro adesso, perché la verifica di §1 non la copre:** *«un solo generatore»*
garantisce che **la casualità** sia riproducibile, **non** che lo sia **ogni** sorgente di
non-determinismo *(ordine di iterazione di un `set`, hash randomization, BLAS multi-thread)*.
**Quella garanzia la dà `V6`, non `§1`:** la rigiocata byte-identica è **il test empirico**, e se
fallisse senza un `np.random` globale, la causa sarebbe lì. **Lo scrivo prima per non poterlo
presentare come sorpresa dopo.**

### 1.2 Il difetto è UNO, ed è al punto di chiamata

```python
:7185   net.salva_stato(_db)      # _db e' un PATH FISSO -> SOVRASCRIVE
```

**`salva_stato` salva il giusto** *(32 ndarray + scalari + le tre strutture di `Z53` + `rng_state` +
il blob verificato al ricarico + `tmp`/`os.replace` atomico)*. **Il problema è il PATH.**

### 1.3 ⚠ Un difetto REALE che la compressione porta a galla

```python
:2869 (attuale)   pickle.dump(stato, open(tmp, 'wb'), protocol=...)
:2899 (attuale)   stato = pickle.load(open(path, 'rb'))
```

**Il file non viene MAI chiuso esplicitamente: si affida al refcount di CPython.** Con un file
normale funziona *(il buffer viene scaricato alla distruzione)*. **Con `gzip` NO: un `GzipFile` non
chiuso può lasciare il trailer incompleto e il file ILLEGGIBILE.**

> **Quindi la compressione non è «un `open` diverso»: impone il `with`.** **È una correzione
> necessaria, non un abbellimento** — e va detta, perché tocca `salva_stato`, che il §2 dice di non
> toccare *(il §2 parla del CONTENUTO: quello non cambia di un byte)*.

### 1.4 ⚠ Come si riconosce «una serie di un altro run» — **la regola va SCELTA e DICHIARATA (A8)**

Il §2 chiede di rifiutare, ma **«di un altro run» non è una proprietà leggibile di un file.**
**Quello che È leggibile:**

| segnale | cosa cattura | già coperto? |
|---|---|---|
| `blob` diverso | **codice diverso** | **sì**, `carica_stato` RIFIUTA già |
| `_db_step` non multiplo di `--db-ogni` | **cadenza diversa** → altra configurazione | **no** |
| seme/parametri diversi a parità di blob | **run diverso, stesso codice** | **NO, e non è nel `.pkl`** |

> **DECISIONE, e la dichiaro invece di lasciarla implicita:** con `--db-serie` si **scansionano TUTTI**
> gli snapshot della serie e si **RIFIUTA** se **(a)** un `blob` qualsiasi differisce da quello
> corrente, oppure **(b)** un `_db_step` non è multiplo di `--db-ogni`.
> **⚠ E DICHIARO ANCHE IL BUCO: due run con lo STESSO blob e la STESSA cadenza ma SEME DIVERSO non
> sono distinguibili dai `.pkl`**, perché **il seme non è fra gli `attrs`**. *(Verificato: `attrs`
> contiene `rng_state`, che è lo stato DOPO N passi, non il seme.)* **Questo è un presidio PARZIALE,
> e chiamarlo totale sarebbe il difetto che A9 descrive.**

### 1.5 Cosa NON so

- **quanto comprime `gzip` su questi dati** *(molti `float64` densi: potrebbe comprimere poco)* —
  **si MISURA, non si stima**: il §3 lo impone e il pilota ha già mostrato `26.45 MB` non compressi;
- **quanto costa in tempo** per snapshot;
- **se la rigiocata combaci davvero** — è `V6`, ed è il punto in cui la riproducibilità o regge o no.

---

## 2. PROGETTAZIONE

### 2.1 Dove si tocca, e perché è byte-inerte
- **`salva_stato`**: `with` + `gzip` **per estensione** (`.gz`). **Il contenuto non cambia.**
- **`carica_stato`**: accetta **entrambi** i formati *(retrocompatibilità, `V7`)*.
- **CLI**: `--db-serie` (booleano, OFF) · `--db-rigioca <da> <a>` (due interi).
- **`batch_condensazione`**: il blocco di caricamento (`:7127-7133`) e il punto di salvataggio
  (`:7182-7185`).

> **⚠ NESSUN GLOBALE DI MODULO NUOVO.** Le opzioni si leggono da `a` **nel punto di chiamata**:
> così **la fisica non può vederle nemmeno in linea di principio**, e `V1`/`V2` diventano vere per
> costruzione invece che per misura. *(La misura si fa lo stesso.)*

### 2.2 La serie
`<stem>_%06d<ext>`, padding a 6 cifre → ordine alfabetico = ordine temporale.
**Ripresa:** con `--db-serie` si carica **il più alto** della serie, non `_db`.
**Contatore**: snapshot scritti, saltati, **e FALLITI** — *«un salvataggio che fallisce in silenzio è
il difetto peggiore qui»*, quindi **si conta e si dichiara a fine run** (A8).

### 2.3 La rigiocata
`--db-rigioca da a`: carica `<stem>_{da:06d}`, gira fino ad `a`, salva ogni `--db-ogni`.
**NON sovrascrive:** se il path esiste, **salta e conta**. **L'archivio originale non è
distruggibile da una rigiocata sbagliata.**

### 2.4 I sigilli, e i tre decisivi
`V0` blob byte grezzi · **`V1` byte-identità a flag OFF [BLOCCANTE]** · **`V2` byte-identità anche a
flag ON** *(il salvataggio non deve perturbare — precedente `lambda_vuoto`)* · `V3` `k*N` passi → `k`
file · `V4` passo nel NOME == passo nei DATI · `V5` round-trip con coorti · **`V6` LA RIGIOCATA
COMBACIA** · `V7` retrocompatibilità · `V8` costo MISURATO · `V9` rigiro dei sigilli del giro.

### 2.5 COSA MI FA FERMARE
- **`V1` o `V2` che cadono** → ho toccato la fisica: **STOP**;
- **`V6` che non combacia** → la riproduzione non funziona, e **§1 ha escluso la causa più ovvia**:
  **STOP e riporta**, senza inventare la spiegazione;
- **`gzip` che costa troppo per passo** → **lo dico** e si lascia non compresso.

---

## 3. TODO DEL NEXT STEP

- [x] blob/branch · **§1 il generatore È uno solo** (e la riserva su `V6` dichiarata)
- [x] §2 serie + §3 gzip → **COSTO MISURATO** *(`eed2ce5`)* → **riportato a Luca: manca la sua
      decisione sul livello di compressione**
- [x] §4 rigiocata — **implementata, e il suo primo criterio era SBAGLIATO: vedi §4-bis**
- [ ] sigilli **V0-V9** *(nessuno scritto; la prova di `D2` ne anticipa un pezzo, non li sostituisce)*
- [ ] registro + `INVENTARIO_strumenti.md` + relazione + **CHECKPOINT**
- [ ] **⚠ NON toccare:** la fisica, `os.replace`, la verifica del blob, il filtro di `salva_stato`,
      i default di `--sync-db`/`--db-ogni`

---

## 4-bis. ⚠ CORREZIONE — **la §1.4 di questo documento era SBAGLIATA, e il commit `2c92b9d` con essa**

**Scritto il 2026-09-19 dopo la prova, e messo QUI perché un documento di progettazione che resta
sbagliato è peggio di un documento assente: qualcuno lo rileggerà per capire perché il codice è
così.** *(`par.5-bis`: un fatto che si rivela superato si CORREGGE, non si lascia stale.)*

### Cosa diceva la §1.4, e cosa è successo

La §1.4 decideva di rifiutare una serie se **(a)** un blob differisce oppure **(b)** un `_db_step`
non è multiplo di `--db-ogni`. **L'implementazione ha fatto una terza cosa, mai decisa da nessuno:
ha preteso che i passi fossero CONTIGUI**, e ha **delegato (a)** a `carica_stato` sul solo snapshot
caricato.

> **La contiguità rifiutava proprio il caso d'uso di `--db-rigioca`:** infittire significa rigirare
> con `--db-ogni` più piccolo, e una serie `250/500/750` **non è contigua** a cadenza `50`.
> **Dimostrato, non dedotto:** `csv/_seal_fork/_prova_D2_rigiocata_2026-09-19.txt`, `7/7`,
> commit `edab9d4`.

### E il criterio **(b)** era sbagliato per la STESSA ragione

**Il rilievo di Luca:** *«cadenze diverse nella stessa serie sono legittime: è il senso
dell'archivio. Il rischio vero è mescolare due FISICHE, non due cadenze.»* **Il criterio (b) è un
criterio di cadenza**: infittire a `30` una serie scritta a `250` sarebbe stato rifiutato allo
stesso modo. **Quindi è caduto anche lui**, e questa è una decisione **oltre la lettera del
mandato**, dichiarata in `ba759c6` perché possa essere ribaltata.

### Cosa vale ADESSO — e questa riga è quella da credere

> **Il discriminante è IL BLOB, e si verifica su TUTTI gli snapshot della serie.** Un file che non
> si apre, o che non è un dizionario, è **rifiutato**: non è uno snapshot. **Nessun vincolo di
> cadenza, di contiguità o di allineamento.**

**Il costo è misurato** *(`eed2ce5`)*: `0.156 s` per snapshot non compresso, `0.32 s` compresso —
**`3.8 s` per una serie da 24**, su un run che dura ore. **Per questo NON serve l'header** che la
§1.4 ipotizzava come ripiego: *(per curiosità, `blob` è la **terza** chiave del dizionario, quindi
sarebbe stato possibile — ma una soluzione non necessaria è solo un modo in più di sbagliare)*.

### Il buco del presidio resta quello dichiarato, e resta aperto

**Due run con lo stesso blob ma SEME DIVERSO non sono distinguibili dai `.pkl`**, perché il seme
non è fra gli `attrs`. **La §1.4 lo dichiarava e aveva ragione: quella parte non è cambiata.**

### La lezione, che è la stessa di ieri

**Un test può fallire perché il codice è sbagliato, o perché il criterio chiede la cosa sbagliata.**
Qui era **il criterio** — ed era un criterio **aggiunto** rispetto a un mandato che invece era
chiaro. **È il tredicesimo criterio scaduto in tre giorni**, e il primo che non veniva da una
descrizione stale ma da un'**aggiunta silenziosa**.
