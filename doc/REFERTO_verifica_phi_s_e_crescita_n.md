# REFERTO — **`n` cresce in DUE punti soli, e `phi_s` a `:2719` non rompe niente. Le `(c)` reggono**

**Blob `f81c4fe1`** *(sha1 byte grezzi; git `af8a96f1`)* · **verificato dal codice, non dai
commenti** · **NESSUN CODICE TOCCATO.**

---

## 1. ⚠ LA DOMANDA GENERALE: **`n` non è un attributo, è `len(self.phi)`**

```python
:1141   def n(self): return len(self.phi)
```

**Quindi «dove cresce `n`» significa «dove cresce `self.phi`». Tutte le assegnazioni, dal disco:**

```
:1061  __init__   self.phi = np.zeros(0)                                  n = 0
:1880  semina     self.phi = concatenate([self.phi, ph % 4pi])            CRESCE
:4175  mitosi     self.phi = concatenate([self.phi, fm])                  CRESCE
:4295  mitosi     self.phi = concatenate([self.phi, anti])   (Schwinger)  CRESCE
:3629  step       self.phi = (_phi_t + dt_n_s*self.phivel + delta_sync_phi) % 4pi
```

**`:3629` è il quinto punto, ed è una RIASSEGNAZIONE — la stessa forma che il mandato teme per
`phi_s`.** **Ma preserva la lunghezza, e per costruzione:**

```
_phi_t          = self.phi.copy()        (:3341)              lunghezza n
self.phivel     = _phivel_t + delta_phivel (:3628)            lunghezza n
delta_sync_phi  = np.zeros(self.n)       (:3578)   oppure  dt_n_s * forza * sin(media - _phi_t)
```

**È una somma PUNTUALE di array di lunghezza `n`, e fra `:3341` e `:3629` non c'è nessuna chiamata
a `semina` o `mitosi`:** dentro `step` `n` non può cambiare.

> **CONCLUSIONE: `n` cresce SOLO da `semina` e `mitosi` (due rami: figli e antinodi Schwinger).**
> **Non esiste una quarta via.** **La classificazione `(c)` NON si rovescia.**

## 2. ⚠ `phi_s` A `:2719`: **la riassegnazione dà lunghezza `n` ESATTA, e lo impone il codice cinque righe sopra**

```python
:2719   self.phi_s = np.arccos(np.clip(nb_new[:, 2], -1, 1))
```

**La lunghezza di `phi_s` diventa quella di `nb_new`. E `nb_new` deriva da `nb`, che deriva da
`self._nb` — che poche righe prima, nella STESSA funzione, è NORMALIZZATO A `n`
INCONDIZIONATAMENTE:**

```python
:2201   if not hasattr(self, "_nb") or self._nb is None:
:2202       b0 = self.phi_s if len(self.phi_s) == n else np.zeros(n)
:2203       self._nb = np.stack([np.sin(b0), np.zeros(n), np.cos(b0)], axis=1)   -> n
:2204   elif len(self._nb) < n:
:2206       nuovi = np.tile([0.0, 0.0, 1.0], (k, 1))
:2207       self._nb = np.vstack([self._nb, nuovi])                              -> n
:2208   elif len(self._nb) > n:
:2209       self._nb = self._nb[:n]                                              -> n
```

**Tutti e tre i rami finiscono con `len(self._nb) == n`.** E c'è una **seconda conferma
indipendente**: a `:2707` il rumore si somma come `rng.normal(0, 1.0, (n, 3))` — **se `nb_new` non
fosse lungo `n`, numpy fallirebbe il broadcast.**

> **`:2719` NON è un percorso scoperto: assegna a `phi_s` lunghezza `n` esatta.**
> **La `(c)` su `phi_s` REGGE, e si cura come le altre quattro.**

**⚠ E c'è un dettaglio che vale la pena notare:** la guardia che il mandato chiede di salvare —
`:2202`, `b0 = self.phi_s if len(self.phi_s) == n else np.zeros(n)` — **sta dentro il ramo
`_nb is None`, cioè la PRIMISSIMA chiamata.** A quel punto `phi_s` viene da `semina`, quindi è già
lungo `n`. **È ridondante anche lei**, ma è un **TERNARIO** *(classe già registrata: il default è
inline e visibile)*, **non una delle 18.** **Non la tocco, e la registro.**

## 3. `:2279` E `:4586` — **perché NON si curano come le altre**

**`_nb` e `_nb_prec` sono estesi da `_eredita_spinore_figli`** *(mitosi e Schwinger)*, **ma
`semina()` NON passa da lì** — è la **voce `H`** di `RAMIFICAZIONI.md`, già registrata.

**E la verifica del §2 mostra cosa succede davvero:** `_nb` **non resta corto**, perché
`_passo_spinoriale` lo **rinormalizza a `n` a ogni chiamata** (`:2204-:2209`). **Quindi:**

- **`:4586`** *(`memoria_hebbiana_moto`, `len(self._nb) >= self.n`)*: gira **dopo** `_passo_spinoriale`
  nel ciclo del driver, quindi `_nb` è già stato rinormalizzato. **Può fallire solo se
  `_passo_spinoriale` non ha girato** — cioè se `SPINORE_VIVO` è spento o se la sua guardia `:3623`
  è scattata. **Non è indipendente: dipende da `:3623`, che è una `(c)`;**
- **`:2279`** *(`_nb_prec`)*: `_nb_prec` è scritto a `:2712` **dentro** `_passo_spinoriale`, quindi
  alla **prima** chiamata non esiste ancora. **È lo STESSO transitorio di avvio di `zeta_vir`
  (`Z68`), e la stessa causa: l'ORDINE.**

> **Quindi le tre `(a)` non sono tre difetti indipendenti: due sono CONSEGUENZE dell'ordine di
> chiamata, e la terza (`:3353`) è la causa di un sintomo già contato.**
> **Il contatore serve a tutte e tre — ma la diagnosi è una sola, ed è la stessa di `Z68`.**

## 4. LA MIA OBIEZIONE SULLE `(b)`, PER INTERO — **e la decisione è di Luca**

**Il mandato chiede il contatore anche sulle `(b)`.** **Su due sono d'accordo, su tre no, e la
ragione non è di principio ma di COSA misurerebbe il numero.**

**D'ACCORDO su `:2021` (`COMPAT_CHI = False`) e `:4661` (`K_FRANGE = 0.0`):** lì il contatore
misurerebbe *«quante volte il ramo non è girato perché il flag/la costante è spento»* — **un valore
noto in anticipo (il 100 %) che però cambierebbe il giorno in cui qualcuno accende il flag.**
**È un presidio vero contro un'accensione silenziosa.**

**NON D'ACCORDO sulla catena `:3517` / `:3520` / `:3526`**, e il motivo è preciso:

```python
if   CHI_CORE and len(perc_chi) >= n:      twn = da chiralita_core_locale()
elif VERSO_CHI and len(perc_chi) >= n:     twn = da perc_chi
elif not (CHI_CORE and len(perc_chi) >= n): twn = _tw_t / PHI_CRIT       <- l'ELSE esplicito
```

**Qui NON c'è nessun ramo silenzioso: `:3526` È l'`else` dichiarato, e copre il caso.** Un
contatore di «salti» su ciascuno dei tre **non conterebbe una legge saltata: conterebbe QUALE RAMO
È STATO SCELTO.** **E quel numero, messo accanto agli altri contatori sotto il nome `salti`,
inviterebbe la lettura sbagliata** — una «frazione di fallimento» che è in realtà una frequenza di
selezione. **È la stessa famiglia del criterio scaduto: un numero che si porta dietro una diagnosi
falsa.**

**LA MIA PROPOSTA, se vuoi comunque il presidio:** **UN contatore solo sulla catena, con TRE
conteggi e il nome `_ramo_framedrag_*`**, etichettato **«quale ramo»** e non «quante volte è
saltata». **Soddisfa `A8`** *(la catena non è più muta: si sa quale via prende)* **senza produrre
una frazione che mente.**

**Decidi tu: la applico come chiedi, o come propongo.**

---

## 5. RIEPILOGO — cosa è pronto a partire

```
(c) CONFERMATE, si curano:   :574  :2285  :3390  :3623  :3669
(a) si curano:               :2279  :3353  :4586
(b) contatore SI:            :2021  :4661
(b) contatore, DA DECIDERE:  :3517  :3520  :3526     (la catena: vedi §4)
```

**Otto siti nel PASSO 1, più due, più la catena se decidi così.** **Nessun codice toccato finora.**
