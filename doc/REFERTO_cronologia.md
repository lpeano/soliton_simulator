# REFERTO — **la cronologia della degenerazione: chi si muove per primo**

**Blob `7c4dec1d`** · seme **42** · **45 snapshot**, passi 60-2700, cadenza 60 · strumento
`csv/_test_fork/_cronologia.py`, esito `csv/_test_fork/_cronologia.txt` · letture e soglie fissate
**PRIMA** in `doc/TASK_HISTORY/2026-09-19_cronologia-degenerazione.md` (`8def0af`).

> **`--tau-luce` sigillo `6/7`** *(`T3` dichiarato)*: ogni numero lo eredita. **UN SEME, UNA
> SCENA.** **Nessun run, nessuna cura.** Nessuna identificazione, nessun verdetto di fisica.

---

## 1. IL VERDETTO AUTOMATICO — e **perché non basta**

Le quattro letture, applicate meccanicamente, danno:

```
ordine dei t50:  r p75 (60) -> omega_s max (240) -> peq p50 (420) -> tw max (480)
                 -> inerzia pav (780) -> fatt_cs max (1260) -> omega_s p50 (1680)
                 -> d0 p50 (1740) -> d0 max (2040)
span 33 snapshot        ritardo primo-secondo 3 snapshot   ->   LETTURA B, candidata `r p75`
```

### ⚠ Ma `t50` presuppone una crescita MONOTONA, e `r p75` non cresce

**Al primo snapshot disponibile (passo 60):**

```
r  p25 = 1.4126     p50 = 1.4141     p75 = 1.4142        TETTO = sqrt(2) = 1.41421356
```

**Tutta la distribuzione è già al tetto.** Quindi `t50(r p75) = 60` **non significa «si muove per
prima»: significa «era già sopra la soglia quando abbiamo iniziato a guardare».**

**E poi `r` non degenera: CROLLA e OSCILLA.**

```
passo  180: p25 = 1.2094      240: p25 = 0.2991
passo 1020: p25 = 1.0999     1080: p25 = 0.0569     1140: p25 = 0.5856     1200: p25 = 0.0532
```

**Salta fra `0.05` e `1.24` da uno snapshot all'altro.** Su una grandezza così, il `t50` **non
misura niente**.

> **È un limite del mio strumento, non un risultato.** E il ritardo che fa scattare `B` è
> **esattamente il minimo** richiesto (3 snapshot): anche senza il problema della monotonia, la
> lettura sarebbe marginale.
> **NON ho cambiato il criterio a posteriori** — è fissato in `8def0af` e resta. **Riporto ciò che
> produce, e perché non basta.**

## 2. IL FATTO CHE I DATI MOSTRANO, e che le quattro letture NON catturano

```
passo 180:  omega_s max = 0.35          nati = 2
passo 240:  omega_s max = 7.58e+04      nati = 26
```

**CINQUE ORDINI DI GRANDEZZA IN 60 PASSI.** È il salto più violento dell'intera cronologia, e
avviene al **9 % del run**.

**E nello stesso intervallo `r` p25 crolla** da `1.2094` a `0.2991`.

### L'osservazione che ci sta accanto, e che NON è una causa

```
nati:   0 (passo 120)    2 (180)    26 (240)    185 (300)
```

**La mitosi comincia a correre nello stesso intervallo.** **Che le due cose coincidano è un fatto
misurato; che una causi l'altra NON l'ho misurato, e non lo scrivo.**

## 3. GLI ALTRI EVENTI, in ordine

| passo | cosa |
|---|---|
| **180-240** | `omega_s` max **+5 ordini**; `r` p25 crolla; la mitosi parte |
| **540** | `_deg` **p25** scende al grado di nascita (`2`) |
| **780** | l'inerzia al pavimento attraversa metà escursione |
| **1260** | `fatt_cs` max attraversa (arriva a `142.8`; **atteso ~1**) |
| **1500** | `_deg` **p50** scende al grado di nascita |
| **1680-2040** | `omega_s` **p50** e `d0` attraversano — **gli ultimi** |

> **La bimodalità di `_deg` non compare di colpo: si apre in MILLE passi**, dal 540 (p25) al 1500
> (p50). **Non è un evento: è un processo.**

**E `d0`, che al 2700 arriva a `394.7`, è l'ULTIMA grandezza a muoversi** (`t50 = 2040`). **La
degenerazione degli archi è una CONSEGUENZA tardiva, non l'innesco.**

## 4. UN MIO CRITERIO TROPPO STRETTO, dichiarato

`_r_corrente p75` **non raggiunge mai `√2` entro `1e-9`** — arriva a `1.4142`. La soglia che avevo
scritto (`TETTO - 1e-9`) era **troppo stretta**, e l'evento «p75 al tetto» risulta `None` pur
essendo di fatto raggiunto. **Lo dichiaro invece di allentarla a posteriori.**

## 5. COSA NON HO FATTO, E PERCHÉ

**La rigiocata `--db-rigioca 180 240 --db-ogni 5`** darebbe **dodici istanti invece di due** dentro
la finestra dell'evento — ed è esattamente ciò per cui la rigiocata è stata costruita oggi.

> **Non l'ho lanciata.** Il mandato dice di rigiocare **solo se il §2 indica un intervallo**, e le
> **quattro letture fissate prima NON lo indicano**: è la **lettura dei dati** a indicarlo.
> **La differenza conta**, e la decisione è di Luca.

**Se si rigioca, due cose vanno con essa:** il sigillo *(lo stato finale deve essere byte-identico
allo snapshot 240 che già esiste — se non lo è, si ferma)*, e la dichiarazione che userebbe
`_scena_video_ripresa.py`, perché il driver del run è stato ripristinato a `f14ea4bd` e **non ha
`--riprendi`**.

## 6. COSA RESTA APERTO

- **cosa accade fra il passo 180 e il 240**: 60 passi di risoluzione non bastano;
- **perché `r` parte già saturo al tetto**: l'archivio comincia al passo 60, e **la transizione, se
  c'è stata, è avvenuta prima**;
- **perché il run si è fermato**: nulla qui lo spiega.
