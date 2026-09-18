# REFERTO — **Non è metà: è il 93 %, sono SEMPRE GLI STESSI, e sono LE TRE MASSE**

**Data:** 2026-09-18 · **Blob `a1ae5090` INVARIATO** — nessuna cura, nessun run nuovo
**Dati:** i `.pkl` del run **continuo** a 1200 passi (`seed 900`, 1 sola invocazione, 0 resume)
**Task history col conto fatto PRIMA:** `49c0c28` · **Sonda:** `_chi_non_invecchia.py` (`44611f63`)

> **⚠ IN TESTA, NON IN FONDO:** questa configurazione usa **`--tau-luce`, il cui SIGILLO È FALLITO**
> (CLAUDE.md par.0) e **`--chi-basc`**, che riscrive `perc_chi` a ogni passo. **Un seme.**
> **`Z9` è aperta.** **Nessun verdetto di fisica.**

---

## 0. IL VERDETTO CONTRO LE CINQUE LETTURE FISSATE PRIMA

| lettura | esito |
|---|---|
| frazione ~50 %, sempre gli stessi, `n` costante → **sistema congelato, `Z9` va riscritta** | **✓ REGGE — ma il numero è `93 %`, non 50 %** |
| flusso che riparte (transitorio di nascita) | **NO — `Jaccard = 1.0000` su tutte le transizioni** |
| mediana bassa ma frazione piccola → coda | **NO — `p05 = p25 = mediana = p75`, identici** |
| nessuna regge | non è il caso |
| **⚠ LA MIA: `r` dei fermi = PAVIMENTO → la causa è il BOTTLENECK, non `eta`/`ramp`** | **✓ REGGE, e in forma esatta: `r/r_floor = 1.0000`** |

---

## 1. ⚠ IL CONTO FATTO PRIMA DI APRIRE I `.pkl` — previsto `1.0025`, misurato `1.0000`

Nel task history (`49c0c28`), **prima di guardare**, avevo ricavato `r` dalla sola crescita di `eta`:

```
r al PAVIMENTO di ritmo()   : 1.414212e-06
eta dal pavimento, 560 passi: 7.919585e-06        eta MISURATA (120->680): 7.900000e-06
rapporto PREVISTO           : 1.0025
```

**Misurato dai `.pkl`, su quattro intervalli su quattro:**

```
intervallo    r FERMI mediana   r FERMI p95      r/r_floor
120 -> 130    1.414213e-06      1.414222e-06     1.0000
130 -> 470    1.414214e-06      1.414224e-06     1.0000
470 -> 800    1.414213e-06      1.414224e-06     1.0000
800 -> 840    1.414213e-06      1.414225e-06     1.0000
```

> **Non sono «lenti»: sono al PAVIMENTO ASSOLUTO di `ritmo()`, e lo è anche il loro 95° percentile.**

## 2. ① Non è metà — **è il 93 %, e non cala**

```
step    n      p05          p25          MEDIANA      p75          p95        max      | FERMI  FRAZ.
120     1199   0.010001683  0.010001683  0.010001683  0.010001683  0.885813   1.54005  | 1116   0.9308
470     1203   0.010006633  0.010006633  0.010006633  0.010006633  4.779141   5.81670  | 1116   0.9277
800     1203   0.0100113    0.0100113    0.0100113    0.0100113    8.329932  10.28641  | 1116   0.9277
1200    1204   0.010016956  0.010016956  0.010016956  0.010016957  13.03488  15.91664  | 1116   0.9269
```

**`p05 = p25 = MEDIANA = p75`, tutti identici, a ogni istante.** **Solo il `p95` si muove** — e
arriva a `13.03` mentre i tre quarti inferiori non si spostano dalla quinta cifra.
**Non è «mediana bassa»: sono TRE QUARTI della popolazione allo stesso identico valore.**

## 3. ② Sono SEMPRE GLI STESSI — `Jaccard = 1.0000`

```
120 -> 130 : 1.0000     130 -> 470 : 1.0000     470 -> 800 : 1.0000     800 -> 840 : 1.0000
PRIMO (120) contro ULTIMO (840): intersezione 1116 su 1116 = 1.0000     |B\A| = 0 ovunque
```

**Gli stessi identici 1116 nodi, per 720 passi. Nessuno entra, nessuno esce.**
**Congelamento permanente, non flusso.**

## 4. ③ Il falsificatore della mitosi è **escluso in modo totale**

```
step 1200 : n 1204   nati dopo t0: 4   fermi NATI dopo: 0   fermi PRESENTI a t0: 1116
```

**Quattro nodi nuovi in 1200 passi, e NESSUNO di loro è fermo.** *(L'età anagrafica è esatta, non
stimata: i nodi si appendono in coda, quindi l'indice è l'ordine di nascita.)*
**Non è il transitorio di nascita di `Z44`.**

## 5. ⚠ CHI SONO — **e qui il quadro cambia di natura**

```
                n      grado p25/med/p75        raggio p25/med/p75
FERMI          1116    371 / 371 / 371          7.732 / 8.004 / 8.281
mobili           87      7 /   9 /  12          1.739 / 2.504 / 3.518
```

> **Raggio mediano `8.004` = `sep`. I «fermi» SONO le tre masse seminate. I «mobili» sono la
> regione centrale.** **E il grado differisce di un fattore 41.**

*(Conferma indipendente, dal tracking del batch stesso: `TRACK accr=1116` — lo stesso numero.)*

## 6. ⚠ IL DATO CHE ROVESCIA IL QUADRO — **il gauge non è più una mediana**

```
median(|f|) = 1.000000e-09  a TUTTI gli istanti   <- il PAVIMENTO `max(median, 1e-9)` E' ATTIVO

           f mediana      f p95        frazione f == 0 ESATTO     x = f/med mediana
FERMI      0.0000e+00     2.66e-13     0.4928 -> 0.6102           0.0000e+00
mobili     0.0583 -> 0.175  1.38       0.0000                     5.8e+07 -> 1.7e+08

|psi_spin| mediana : FERMI 6.06e-06 -> 6.03e-06 (PIATTO)   mobili 3.6e-04 -> 9.8e-03 (x27)
```

**Più della metà dei nodi ha `f` ESATTAMENTE zero** *(49 % → 61 %)*, quindi `median(|f|) = 0`,
quindi **`med` cade sulla costante di regolarizzazione `1e-9`.**

> **Il gauge del tempo proprio non è più una statistica del sistema: è il numero `1e-9`.**
> È alla lettera ciò che CLAUDE.md par.9 avverte — *«alle scale simulabili la regolarizzazione
> diventa il parametro fisico»*.

**E da lì il sistema si separa in due popolazioni che non si parlano più:**

| | `x = f/med` | `r` | `eta` | `psi_spin` |
|---|---|---|---|---|
| **93 %** (le masse) | **0** | **pavimento `1.414e-06`** | **congelata** | `6e-06`, **piatto** |
| **7 %** (il centro) | **`10⁷ – 10⁸`** | **saturazione, `≈ √2`** | cresce a `15.9` | cresce ×27 |

**Non c'è più nessuno in mezzo.** `x` salta da `0` a `10⁸` senza valori intermedi.

## 7. COSA QUESTO **NON** DICE

- **⚠ `Z44` NON è smentita: non si trasporta.** Là i nodi con `f = 0` erano **1-2 su 450** ed erano
  **neonati**; qui sono **il 53-61 %** e sono **le masse**. **Scena diversa, regime diverso (A3c).**
  **Sono due misure di popolazioni diverse, e vanno citate entrambe con la loro scena.**
- **NON so perché** i nodi a grado **371** abbiano `|psi_spin|` **mille volte più debole** di quelli
  a grado **9**. **È il fatto più strano della misura, e non ho una spiegazione misurata.**
  **Non la invento** *(era la quinta lettura: «nessuna regge → si dice»)*.
- **NON dico che sia un difetto del codice o della fisica.** Dico che **il 93 % del sistema ha il
  tempo proprio fermo al pavimento, che sono sempre gli stessi, e che il gauge è una costante.**

---

## 8. `Z9` VA RISCRITTA — **il testo proposto, NON cablato**

> **`Z9` — non «il kernel matura lentamente», ma «la maggioranza non matura affatto».**
> Misurato sul run continuo a 1200 passi (`a1ae5090`, seed 900, **`--tau-luce` non certificato**):
> **`1116` nodi su `1204` (`92.7 %`) hanno `eta` ferma al valore di semina per l'intero run**, con
> **`p05 = p25 = mediana = p75` identici** e **`Jaccard = 1.0000`** fra tutti gli istanti: **sono
> sempre gli stessi.** **Non è il transitorio di nascita** (4 nodi nuovi in 1200 passi, **zero**
> fermi fra loro). **Sono le tre masse seminate** (grado `371`, raggio `8.00 = sep`), mentre i `87`
> mobili sono la regione centrale (grado `9`, raggio `2.5`).
> **La causa NON è `eta` né `ramp`: è a monte.** Il loro `r` vale **`1.414213e-06`**, cioè
> **`r/r_floor = 1.0000`** — **il pavimento assoluto di `ritmo()`** — perché **`f = 0` esatto** per
> il 49-61 % e quindi **`median(|f|)` cade sulla costante `1e-9`**.
> **CRITERIO DI CHIUSURA:** `Z9` si chiude quando **la frazione di nodi con `eta` al valore di
> semina cala sotto il 10 % su ≥ 4 semi** — **non** quando `ramp` mediano cresce, perché il `ramp`
> mediano **è quello di un nodo che non si muove.**
> **LIMITE:** un seme, una scena, `--tau-luce` non certificato, `--chi-basc` attivo.

## 9. COSA NON HO FATTO

**Nessuna cura, nessun cablaggio, nessuna promozione, nessun run nuovo.** Non toccati `EMB_IT`,
`TAU_A`, `ramp`, il gauge, il `+1e-6`, il `max(...,1e-9)`. **Il testo di `Z9` è una PROPOSTA.**
**Gli istanti sono citati col loro `_db_step`, mai col nome del file** *(il primo watcher li aveva
mislabellati: uno conteneva `840`)*.
