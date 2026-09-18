# REFERTO — **Le coorti sopravvivono già alla mitosi. NON sopravvivevano allo snapshot**

**Data:** 2026-09-18 · **Blob:** `a1ae5090` → **`b9e07c73`** · **Sigillo `_sigillo_coorti.py`: 9/9 PASS**
**Verifica scritta PRIMA del codice:** `695ced0` · **Letture fissate PRIMA:** stesso commit, §2
**Il FAIL intermedio è committato:** `a872383` *(era il criterio, non il codice)*
**La catena dei commit:** `7d75432` la cura · `a872383` il FAIL com'era · **`600fe6c`** il
criterio riscritto · `928cb62` l'esito `9/9`

> **⚠ CORREZIONE A UN COMMIT GIÀ PUSHATO:** il messaggio di `928cb62` cita **`6b5cd0f`** per il
> commit del criterio. **È un hash SBAGLIATO: quello giusto è `600fe6c`.** Il messaggio non si
> riscrive *(sarebbe una riscrittura di storia già pushata)*, quindi la correzione vive **qui**.
> **In un repo che ancora tutto agli hash, un hash inventato è un difetto, non un refuso.**

> **CATEGORIA D del par.10 — correzione di difetto, NESSUN FLAG.** *Un bug curato non ha un
> interruttore.* **Il gate NON si sposta: resta a `c0803713`** per la ragione del par.0
> (`--tau-luce` ha il sigillo FALLITO ed è cablato nel file).

---

## 1. IL MANDATO CHIEDEVA DUE COSE. **LA PRIMA ERA GIÀ FATTA**

**Il mandato diceva:** *«alla mitosi il figlio nasce SENZA appartenenza: `:1858` estende con liste
VUOTE»*. **Dal disco, `:3951-3954`:**

```python
# TRACKING: i figli della mitosi ereditano la concorrenza del genitore a (nascono dalla sua
# divisione, concorrono alle stesse masse). conc_archi viene riallineato sotto (keep+nuovi).
if self.conc_nodi:
    for kk in a:
        eredita = [v[:] for v in self.conc_nodi[kk]] if kk < len(self.conc_nodi) else []
        self.conc_nodi.append(eredita)
```

**Il figlio eredita una COPIA PROFONDA dal genitore `a`, e la scelta di `a` è già motivata nel
commento.** **Il ramo Schwinger fa lo stesso (`:4076-4082`)** e **`conc_archi` è riallineato
(`:3997-4001`)**. **`:1858` — l'`extend` con liste vuote che il mandato citava — è in `semina()`, non
in `mitosi()`, ed è CORRETTO lì:** un nodo appena seminato non ha lignaggio finché
`_registra_concorrenza` non glielo assegna.

> **⚠ E `S2` lo MISURA invece di asserirlo, sui DUE bracci:**
> **frazione di nodi con coorte non vuota = `0.8238` nel VECCHIO, `0.8238` nel NUOVO — identica.**
> **`374` su `454`.** **La lettura era fissata prima: *«`S2` già ~100 % PRIMA della modifica →
> conferma che l'ereditarietà c'era già, e lo si scrive»*.**
> **È `82.4 %`, non `~100 %`, e il numero si riporta com'è:** il complemento sono **i nodi SEMINATI**,
> che per costruzione non hanno lignaggio. **Non arrotondo verso la mia ipotesi.**

## 2. IL DIFETTO VERO — **una riga, e uno scarto SILENZIOSO**

```python
:2865   if isinstance(v, (np.ndarray, int, float, bool, np.integer, np.floating, str)):
:2866       stato['attrs'][k] = v
```

**`conc_nodi` e `conc_archi` sono `list`, `masse_info` è un `dict`: non matchano nessuno di quei tipi
e vengono SCARTATI IN SILENZIO.** **E la docstring della funzione dichiara *«salva TUTTE le grandezze
di stato … così non ne dimentica nessuna»*: per queste tre NON è vero.**

**CONSEGUENZA:** dopo un salva/ricarica **il lignaggio riparte VUOTO**, e **ogni misura di
appartenenza fatta su uno snapshot ricaricato guarda un sistema SENZA STORIA.**

**`S3a` lo DIMOSTRA invece di dedurlo:**

```
VECCHIO  chiavi presenti in attrs: []
NUOVO    chiavi presenti in attrs: ['conc_nodi', 'conc_archi', 'masse_info']
```

## 3. LA CURA — **esplicita, e il filtro NON si tocca**

**Si aggiungono le tre chiavi dopo il ciclo su `__dict__`, con `getattr` guardato.**
**Il filtro NON si allarga**, e la ragione è scritta nel codice: **allargarlo farebbe entrare anche le
cache derivate** (`_S`, `_perm`, `_ker_cache`) **che `carica_stato` INVALIDA apposta** — e **quello
che entra va SAPUTO.**

**Perché non tocca la fisica** *(enumerato dal disco nel giro precedente, `695ced0`)*: i lettori di
`conc_nodi` sono `indici_massa_vivi`, `aggiorna_pesi_concorrenza`, `tracking_masse`,
`_registra_concorrenza`, `_ripara_tracking` — **e nessuno dei loro chiamanti è `step()`, `mitosi()` o
`scuoti_vuoto()`.** **È una struttura di MISURA PURA.**

---

## 4. IL SIGILLO — **9/9 PASS**, e `S1` è il decisivo

```
--- S1 [DECISIVO] -- BYTE-INERZIA DELLA FISICA, con salva_stato CHIAMATO ai passi (20, 45) ---
    vec/nuo      n: 454 contro 454   UGUALE
      psi       shape (454,)         max|A-B| = 0.000e+00
      phi       shape (454,)         max|A-B| = 0.000e+00
      phivel    shape (454,)         max|A-B| = 0.000e+00
      eta       shape (454,)         max|A-B| = 0.000e+00
      d         shape (21930,)       max|A-B| = 0.000e+00
      d0        shape (21930,)       max|A-B| = 0.000e+00
      omega_s   shape (454, 3)       max|A-B| = 0.000e+00
      _nb       shape (454, 3)       max|A-B| = 0.000e+00
      pos       shape (454, 3)       max|A-B| = 0.000e+00
  [PASS] S1     shape diverse = 0, campi confrontati = 9/9, max|A-B| = 0.000e+00
```

> **E lo zero NON è mancanza di confronto:** la riga delle shape è stampata **PRIMA**, e
> *«campi confrontati = 9/9, shape diverse = 0»* **è parte del criterio, non un commento**
> *(è la trappola `C18` di par.9, e stavolta è chiusa per costruzione).*
> **⚠ E `salva_stato` È STATO CHIAMATO ai passi 20 e 45 in ENTRAMBI i bracci:** senza, la funzione
> modificata **non sarebbe stata esercitata** e il PASS sarebbe stato **vuoto**.

**Gli altri:**

| punto | esito | il numero |
|---|---|---|
| `S0` i due blob devono DIFFERIRE | **PASS** | `a1ae5090` contro `b9e07c73` |
| `S2` le coorti alla mitosi, sui DUE bracci | **PASS** | `0.8238` contro `0.8238` |
| `S3a` le chiavi ASSENTI nel vecchio | **PASS** | `[]` |
| `S3b` presenti nel nuovo | **PASS** | tutte e tre |
| `S3c` round-trip | **PASS** | `len(conc_nodi) = 454 = n`, `conc_archi = 21930`, `masse_info = 3`, contenuto **identico al disco** |
| `S4` `_ripara_tracking` (P5) | **PASS** | **0 chiamate in entrambi** su 60 passi |
| `S5` il costo | **PASS** | `.pkl` **`+25.6 %`** a `n = 454` |
| `S6` `Z42` regge sul blob nuovo | **PASS** | `_sigillo_anello.py` **10/10** |

### 4.1 ⚠ `S5` — **quello che il numero NON dice**

**`+25.636 %` sul `.pkl`, a `n = 454`.** **Non è il numero delle scene vere**, dove `n` vale
`5878-8018`: **`conc_nodi` cresce col numero di NODI e `conc_archi` col numero di ARCHI**, e a `n = 454`
gli archi sono già `21930`. **Il costo a `n = 8000` NON è misurato, e non lo estrapolo.**

**E il TEMPO non si legge affatto:** due esecuzioni dello stesso sigillo hanno dato **`×1.0051`** e
**`×0.9245`** — **il secondo dice che il codice NUOVO è più veloce del VECCHIO**, che è impossibile.
**È rumore di sistema su 60 passi**, e serve a dire **una cosa sola**: *il costo non ESPLODE*, che era
la soglia dichiarata prima. **Per una misura di tempo servirebbero più ripetizioni e una barra.**

### 4.2 ⚠ IL FAIL INTERMEDIO — **il criterio, non il codice**, ed è committato

**Il primo giro ha dato `8/9`.** **`S6` cercava la stringa `"FAIL"` nello stdout del sigillo figlio,
e la trovava — DENTRO IL TESTO ESPLICATIVO DI UNA RIGA CHE PASSA:**

```
[PASS] P2  shape divergenti 7, max|A-B| = 0.000e+00 (0 con shape uguali = FAIL)
```

**Il sigillo figlio riportava `10/10 PASS` e `returncode 0`.** **Era un FAIL FALSO.**

> **È par.9 alla lettera: *«un criterio di sigillo si scrive DA UNA MISURA, non dal proprio modello
> mentale del codice»*.** **Quarto caso della stessa famiglia in questo repo** *(`N3b`, `M1b`/`M3`,
> `M3c`)*, **e la forma è sempre la stessa: il criterio guarda nel posto giusto con la chiave
> sbagliata.**
> **E il costo non è simmetrico: un FAIL falso costa PIÙ di un sigillo mancante**, perché si porta
> dietro **una diagnosi** — chi lo legge va a cercare un difetto che non c'è.

**Il criterio nuovo è LETTO dall'output:** si parsa la riga `ESITO: 10/10 PASS` e si richiede
`passati == totali` **con `totali > 0`** *(se la riga manca, `totali` resta `-1` e `S6` **FALLISCE**
invece di passare per assenza di prova — stessa famiglia del `max|A-B| = 0` per mancanza di confronto)*,
**più** la ricerca di **`"[FAIL]"` con le parentesi**, che è il marcatore di riga e non può comparire
in un testo esplicativo. **Due condizioni indipendenti.**

**`S1`-`S5` sono identici fra i due giri**, byte per byte nell'output: **la correzione ha toccato solo
`S6`**, ed è verificabile confrontando `a872383` con questo commit.

---

## 5. COSA RESTA APERTO

- **il costo a `n = 8000` NON è misurato**, e il `.pkl` delle scene vere pesa già ~18-48 MB;
- **la separazione «coorte assegnata dalla MITOSI» contro «riscritta da `chi_basc`» resta da fare**:
  **non è ricavabile dai `.pkl`** neanche adesso — **servirebbero contatori DURANTE il run**, ed è il
  limite già dichiarato in `Z49`;
- **nessuno snapshot esistente acquisisce le coorti retroattivamente.** I sei `.pkl` di `_gvideo` e i
  sei di `_g2m` sono stati scritti dal blob `a1ae5090`: **per averle servirebbe rigirare le scene**,
  e **non è stato fatto.**
