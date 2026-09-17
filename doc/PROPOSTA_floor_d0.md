# PROPOSTA TECNICA — ⑥ `_floor_d0`. **NON CABLATA.**

Il mandato (§3) dice: *«⑥ `_floor_d0` — **SOSPESA**: `cs`/`dt_e` non raggiungibili, ritorno scalare,
sette chiamanti, e sostituire entrambi i rami renderebbe `PAV_COM` inerte. **Riporta la proposta,
non cablare.**»* Questo documento è quella proposta.

---

## 1. COS'È OGGI, dal codice

```python
def _floor_d0(self):          # nessun argomento, ritorna uno SCALARE
    if PAV_COM:  ...          # f * median(d0)      -> pavimento "comovente"
    else:        return 0.05  # il muro assoluto
```

**Sette punti di chiamata**, tutti nella forma `self.d0 = np.maximum(self.d0, self._floor_d0())`.

**I due rami violano assiomi diversi, e questo è il punto:**

| ramo | forma | assioma violato |
|---|---|---|
| `PAV_COM = False` (**default**) | `0.05` | **A1** — numero scelto; e **A3b**: è una scala assoluta in un modello che non ne ha |
| `PAV_COM = True` | `f · median(d0)` | **A2** (statistica globale) + **A3** (normalizzato sul proprio insieme) |

**Nessuno dei due è salvabile aggiustando l'altro.** È la ragione per cui «sostituire entrambi i
rami» renderebbe `PAV_COM` inerte: i due rami diventerebbero **la stessa cosa**, e un flag che non
distingue più nulla non è un flag — è codice morto con un interruttore davanti.

---

## 2. LA FORMA CHE SODDISFAREBBE GLI ASSIOMI

Un pavimento su `d0` esiste per una ragione dichiarata nel codice stesso (`:3421`): *«la spinta non
deve portare `d0` sotto la scala minima, o lo stress `|d-d0|/d0` diverge»*. È un **vincolo di
buona definizione**, non una scelta di scenario — quindi, per A1, è **lecito purché il valore sia
l'unico possibile**, non uno fra molti.

**La scala minima di un arco è la scala dell'arco, non una costante:**

```python
def _floor_d0(self):
    # per ARCO, non scalare: ogni arco ha la propria scala minima
    return self.d * (1.0 / (1.0 + ...))   # <- IL PUNTO APERTO, vedi §3
```

**Il candidato naturale, e perché non lo cablo senza decisione:** il pavimento causale
`d0 >= dt_e * cs_arco` — *«in un passo la forma di riposo non può scendere sotto il cammino che
un'onda percorre in quel passo»*. Ha la stessa struttura del `max(t_luce, t_visco)` già cablato
nella plasticità (commit `f405327`): **un limite al confine fisico, non un numero scelto.**

---

## 3. I TRE OSTACOLI, e sono tecnici, non di principio

**① Il ritorno è SCALARE, i chiamanti si aspettano uno scalare.**
`np.maximum(self.d0, scalare)` e `np.maximum(self.d0, array_per_arco)` funzionano **entrambi** in
numpy — ma **solo se l'array è lungo quanto `d0`**. Dei sette chiamanti, alcuni girano **dopo**
operazioni che cambiano il numero di archi (mitosi, Schwinger). **Un ritorno per-arco va verificato
chiamante per chiamante**, e due di essi (`:3378`, `:3776`) stanno dentro `mitosi()` e nel blocco
Schwinger, cioè **esattamente dove gli array si stanno ricostruendo.**

**② `cs_arco` e `dt_e` non sono raggiungibili da `_floor_d0`.**
`cs_arco` è **locale a `step`** (`:3129`). `dt_e` ora **è** raggiungibile — l'ho portato su `self`
come `_dt_e_ultimo` per la correzione ③ (commit `3ca7731`) — ma `cs_arco` no.
**Si risolverebbe con lo stesso pattern**, uno snapshot `self._cs_arco_ultimo`. **Non l'ho fatto:**
aggiungere stato al simulatore per una correzione che non è stata autorizzata sarebbe cablarla a
metà, e lo stato aggiunto sopravvivrebbe alla decisione di non farla.

**③ `PAV_COM` diventerebbe inerte, e non è una conseguenza accettabile in silenzio.**
`--pav-com` è nella configurazione della campagna `cs_floor`. Un flag che smette di distinguere
**senza dirlo** è la classe di difetto già catalogata (`VERSO_CHI` cablato ma muto). Se la forma
nuova sostituisce entrambi i rami, allora `PAV_COM` va **dichiarato NO-OP e stampare un avviso**,
come è stato fatto per `--elast-c` e `--step2-orologio`.

---

## 4. COSA DECIDERE, e non lo decido io

1. **Il pavimento su `d0` è un vincolo di buona definizione o una legge di scenario?** Se è il
   primo, la forma causale `dt_e · cs_arco` è la candidata e A1 la assolve. Se è il secondo,
   `PAV_COM` ha ragione di esistere come alternativa e i due rami vanno **tenuti**.
2. **Si accetta di rendere `PAV_COM` un NO-OP dichiarato?**
3. **Si accetta un secondo snapshot di stato (`_cs_arco_ultimo`) sul simulatore?**

**Finché queste tre non hanno risposta, ⑥ resta SOSPESA** — ed è la stessa ragione per cui è
arrivata sospesa dal mandato: *«il mandato NON dice quale ramo di `PAV_COM` sostituire»*.

---

## 5. UNA COSA CHE SI PUÒ DIRE SUBITO, e vale indipendentemente dalla decisione

Il pavimento **è attivo**: nel run di sigillo a 60 passi `min(d0) = 0.05` **esatto**, cioè il muro
assoluto sta toccando gli archi più corti. **Non è una protezione dormiente.** Quantificare *quanti*
archi tocca richiede una misura che questo giro non prevede, ma **il fatto che il minimo di `d0`
coincida esattamente col valore del muro è già una risposta**: se il pavimento non mordesse mai,
`min(d0)` sarebbe un numero qualunque sopra `0.05`.
