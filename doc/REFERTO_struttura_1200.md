# REFERTO — **La struttura a 1200 passi: il guscio esiste, ma è fatto dei nodi che non maturano. E il gauge è sul pavimento nel 99.76 % delle chiamate**

**Data:** 2026-09-18 · **Blob `a1ae5090` INVARIATO** — nessuna cura, nessun run nuovo
**Dati:** il run **continuo** a 1200 passi (`seed 900`, 1 invocazione, 0 resume) · **un seme**
**Previsioni scritte PRIMA del run:** `fb87640` · **Sonda:** `_struttura_1200.py` (`e1751a7e`)

> **⚠ IN TESTA, NON IN FONDO:**
> **`--tau-luce` HA IL SIGILLO FALLITO** (`doc/SIGILLO_tau_luce_FALLITO.md`, CLAUDE.md par.0):
> **la scena include una legge NON CERTIFICATA, e OGNI numero di questo referto lo eredita.**
> **`--chi-basc` è attivo:** `perc_chi` non è un'etichetta di lignaggio.
> **`Z9` è aperta:** tutto è su un kernel che non ha finito di accendersi. **Un seme.**
> **NESSUN VERDETTO DI FISICA, nessuna identificazione.**

---

## 0. IL NUMERO CHE VIENE PRIMA DI TUTTI — **i contatori A8**

```
_ritmo_chiamate           2886
_ritmo_med_sul_pavimento  2879      <-  il 99.76 %
_ritmo_med_non_promosso   1202
_ritmo_f_tutto_nullo         5
_ritmo_med_assente           3      _ritmo_sicurezza 4      _ritmo_guard4pi_ko 3
```

> **`median(|f|)` cade sulla costante di regolarizzazione `1e-9` in `2879` chiamate su `2886`.**
> **Non è un caso degli istanti campionati: è il 99.76 % del run.**
> **Il gauge del tempo proprio, in questa scena, NON È una statistica del sistema: è un numero.**

**E la cura di `Z42` ha lavorato 1202 volte:** `_ritmo_med_non_promosso = 1202` — **milleduecento
volte il pavimento NON è stato promosso a gauge del passo dopo.** *(Senza quel ramo, cablato in
`c6630fc`, la degenerazione si sarebbe rovesciata in saturazione altrettante volte.)*

---

## 1. ① LA MATURAZIONE — la mediana è piantata, il `p95` corre

```
passo   n      eta med      ramp p05     RAMP MED     ramp p95    frac ramp=0   Lam
120     1199   0.0100017    0.000200034  0.000200034  0.017716    0.000000      3.36941e-09
800     1203   0.0100113    0.000200226  0.000200226  0.166599    0.000000      9.26511e-07
1200    1204   0.0100170    0.000200339  0.000200339  0.260698    0.000000      4.40759e-06
```

**`p05 = ramp MEDIANO = 0.0002`, identici e fermi;** **il `p95` cresce di 15 volte** (`0.018 → 0.26`).
**È `Z46` vista da un'altra grandezza: la maggioranza non matura, una minoranza corre.**
**`Lam` (energia del vuoto) cresce invece di `1300` volte.**

**Nessun nodo con `|psi| = 0`** ai tre istanti — **la previsione era «quasi nulla», ed è ZERO**:
*(`Z44` contava i neonati, e qui la mitosi è ferma: 8 nodi in 1200 passi.)*

**⚠ NON confronto con `0.0002 / 0.0102 / 0.0212`:** quelli sono di **un'altra scena** con `n ~ 450`
(A3c). **Si guarda la FORMA, non il numero.**

## 2. ② IL GUSCIO — **esiste, si stabilizza, e si approfondisce**

```
passo   minimo di |psi| a r     |psi| al minimo   nodi nel bin   bin oltre il minimo
120     8.55                    1.2091e-06        179 (15.1 %)   0     <- AL BORDO
800     7.21                    1.1770e-06         31 ( 2.6 %)   4
1200    7.21                    1.2002e-06         36 ( 3.0 %)   4
```

**Il minimo si sposta da `8.55` a `7.21` e poi RESTA FERMO.**
**E il contrasto CRESCE:**

```
passo   |psi| DENTRO   |psi| FUORI    rapporto        |<n>| dentro / fuori
800     0.0028458      1.2912e-06     ~2200           0.99991 / 1
1200    0.0056714      1.3050e-06     ~4300           0.99982 / 1
```

**Il rapporto dentro/fuori RADDOPPIA fra 800 e 1200: il guscio si approfondisce.**
**Ma la coerenza `|<n>|` NON distingue: vale `~1` dentro e fuori.** *(Era una delle quattro
grandezze del profilo: non contribuisce.)*

### ⚠ E I TRE FALSIFICATORI, applicati PRIMA di descrivere

| | passo 120 | passo 800 | passo 1200 |
|---|---|---|---|
| **(a)** `eta` del bin minimo / `eta` INTERNA | `0.0100 / 1.057` = **0.0095** | `0.0100 / 8.503` = **0.0012** | `0.0100 / 13.73` = **0.00073** |
| **(b)** nodi nel bin / mediana per bin | 179 / 10 | 31 / 11 | 36 / 9 |
| **(c)** bin oltre il minimo | **0 → AL BORDO** | 4 | 4 |

- **(b) NON è un minimo di statistica:** il bin del minimo ha **più** nodi della mediana per bin.
- **(c)** al passo **120** il minimo era **all'estremo del raggio popolato** — **lì non era una
  parete**; a **800** e **1200** ci sono **4 bin oltre**: **è dentro la nube.**
- **⚠ (a) SCATTA, ed è netto: i nodi del guscio hanno `eta` MILLE VOLTE più bassa dell'interno, e il
  rapporto PEGGIORA col tempo** (`0.0095 → 0.00073`).

> **La previsione scritta prima diceva: *«se il guscio ha `eta` più bassa dell'interno, è il FRONTE
> DI NASCITA, non una parete»*. Qui la prima metà è vera e la seconda NO — e la ragione è
> misurata:**
> **la mitosi in questa scena è FERMA (8 nodi in 1200 passi). Quei nodi non sono NATI da poco:
> sono i nodi che NON HANNO MAI MATURATO — gli stessi `1116` di `Z46`, che stanno a raggio mediano
> `8.004`.**
> **Il «guscio» coincide con l'anello delle masse seminate che restano al pavimento di `ritmo()`.**
> **Non è un fronte di nascita e non è una parete: è la regione dei nodi congelati.**

## 3. ③ LE FASI — **e qui la mia previsione era ROVESCIATA**

```
passo   n1    n2    n3   |  d(1-2)     d(2-3)     d(3-1)   |  coer INTERNA   coer FRA MASSE
120     400   399   400  |  -1.50672   -1.94096   -2.83551 |  0.2043         0.23511
800     404   397   402  |  +0.92176   -1.67322   +0.75145 |  0.22317        0.77930
1200    403   399   402  |  +0.81827   -1.56090   +0.74264 |  0.20351        0.80692
```

**Gli sfasamenti NON convergono a `2π/3 = 2.094`** — la previsione era questa, e regge.
**Ma si STABILIZZANO:** fra 800 e 1200 cambiano di `0.10 / 0.11 / 0.01`.

> **⚠ E LA PREVISIONE SULLA COERENZA ERA ESATTAMENTE AL CONTRARIO.** Avevo scritto: *«mi aspetto
> coerenza INTERNA a ciascuna massa PIÙ ALTA di quella FRA masse»*.
> **Misurato: la coerenza FRA le masse passa da `0.235` a `0.807`, mentre quella INTERNA resta a
> `~0.20`.** **È QUATTRO VOLTE più alta fra le masse che dentro ciascuna.**
> **Le tre masse si allineano fra loro più di quanto ciascuna sia coerente al proprio interno.**
> **Non so spiegarlo, e non lo spiego.**

*(Coorti assegnate **per posizione** al centro di semina più vicino: il tracking non è nel `.pkl`.
Approssimazione **dichiarata**. I tre conteggi restano `~400` ciascuno a tutti gli istanti.)*

## 4. ④ IL CONTRASTO E LA SANITÀ

```
passo   n      rho centro   rho guscio   centro/guscio   max|d-d0|/d0   NaN/inf
120     1199   1.1075e-07   3.3198e-11   3.34e+03        18.9           no
800     1203   6.9598e-05   2.7990e-11   2.49e+06        49.8           no
1200    1204   3.7947e-04   2.7921e-11   1.36e+07        50.2           no
```

**`rho` al centro cresce di `3400` volte; `rho` al guscio è PIATTA** (`3.3e-11 → 2.8e-11`).
**Il contrasto centro/guscio va da `3.3e+03` a `1.36e+07`: quattro ordini in 1080 passi.**
**Lo stress `max|d−d0|/d0` passa da `18.9` a `50.2` e si stabilizza.** **Nessun NaN, nessun runaway.**

---

## 5. COSA QUESTO **NON** DICE, e un limite della sonda

- **NESSUNA IDENTIFICAZIONE DI FISICA.** Non dico cosa sia la struttura. Riporto **i numeri e la
  forma**.
- **Non so spiegare** perché la coerenza **fra** masse superi di quattro volte quella **interna**.
  **È il fatto più strano del referto, e non invento una spiegazione.**
- **⚠ LIMITE DELLA SONDA, dichiarato:** cerca i file `stato_{120,400,800,1200}.pkl` per **nome**, e
  **il `400` non esiste** *(il primo watcher mislabellò gli snapshot; gli istanti veri sono
  `120/130/470/800/840/1200`)*. **Quindi `130`, `470` e `840` NON sono stati letti.**
  **Tre istanti bastano per dire «si sposta e si approfondisce», ma la risoluzione temporale è
  minore di quella disponibile.** *(Il `_db_step` dentro il file è autoritativo; il nome no.)*
- **Un seme, una scena, e `--tau-luce` non certificato.**

## 6. COSA NON HO FATTO

**Nessuna cura, nessun cablaggio, nessuna promozione, nessun run nuovo.** Blob invariato.
**`Z46` non è stata toccata:** resta valida **per il batch**, ed è **confermata** da questo referto
per un'altra via *(il `ramp` mediano piantato e il `p95` che corre)*.
