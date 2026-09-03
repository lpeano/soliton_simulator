# Come interpretare i dati — Campagna `spinore-vivo + plast-din`

Guida di lettura per la campagna prodotta da `test_spinore_vivo_plastdin.bat`.
È la **copia** della campagna `spinore-vivo` con **in più** la legge di
**plasticità metrica dinamica** (`--plast-din`). Leggere prima
[INTERPRETAZIONE_campagna_spinore_vivo.md](INTERPRETAZIONE_campagna_spinore_vivo.md):
qui si documentano **solo le differenze** e il confronto.

> **Disciplina.** Non concludere sotto ~2000 passi né da un solo seme. Etichettare
> ogni conclusione: **dimostrato / in verifica / aperto**.

---

## 1. Cosa cambia rispetto alla base

- **Entrambe** le campagne hanno `--spinore-vivo`. Differiscono **solo** per
  `--plast-din` → un flag, una variabile.
- Confronto diretto: `out_spinore_plastdin/` (questa) vs `out_spinore/` (base),
  stessi nomi file, stessi semi, stessa config.

### La legge `--plast-din` (dove genera volume)
Alla **mitosi** (suddivisione di un arco), il `d0` di riposo dei due archi figli:

$$d0_h = \frac{d}{2}\left(1 + \tanh\!\big(\max(\,\underbrace{(|tw|/\Phi_{crit}-1)}_{\text{eccesso torsione}}\cdot\underbrace{|d-d0|/d0}_{\text{stress metrico}}\,,\ 0)\big)\right)$$

- Volume extra **solo** dove l'arco ha **torsione oltre il critico** E **stress
  metrico** alto. Altrove il fattore è 0 → dimezzamento canonico ($d0_h=d/2$).
- Locale (solo `tw`, `d`, `d0` dell'arco), nessuna coordinata, zero parametri.
- Effetto atteso: alza la **coda** di `d0` (`d0_max`) senza gonfiare `d0_mean`,
  e riduce lo `stress` metrico dove agisce.

---

## 2. Le domande di questa campagna

**D1 — La plasticità cambia l'ordine di spin?**
Confronta `spin_cluster_modulo` ($S_M$) e `spin_cluster_omega` ($\omega_S$) tra
questa campagna e la base. Se lo spazio si rilassa dove è teso, gli spin potrebbero
ordinarsi diversamente (più o meno, o precessione più/meno persistente).

- $S_M$ **uguale** alla base → l'ordine di spin **non dipende** dalla plasticità
  (settori disaccoppiati: buona robustezza).
- $S_M$ o $\omega_S$ **diversi** → la geometria che si rilassa **influenza** lo
  spinore: accoppiamento metrica↔spin da caratterizzare.
- In particolare: la base mostra $\omega_S$ **in declino** (precessione che
  rallenta). Domanda chiave: con `--plast-din`, $\omega_S$ **decade più lento,
  uguale, o più veloce**? Se la plasticità rilassa la tensione che frena la
  rotazione, $\omega_S$ potrebbe **persistere** più a lungo.

**D2 — La plasticità genera volume dove c'è tensione?**
Colonne metriche: `d0_mean`, `d0_max`, `stress`, `dil`, `m0_raggio`, `scala_com`.

- Atteso: `d0_max` **più alto** che nella base (coda gonfiata nei punti tesi),
  `d0_mean` **simile** (non gonfia ovunque), `stress` metrico **più basso** dove
  la plasticità ha sciolto la tensione.
- Se `d0_mean` sale molto → la plasticità agisce ovunque (non adattiva): sospetto.
- Se `stress` non cala → la plasticità non sta effettivamente rilassando: aperto.

---

## 3. Tabella di confronto (base vs plast-din, ultimo terzo, 2 semi)

| Grandezza | Base | Plast-din | Lettura |
|---|---|---|---|
| $S_M$ | ~0.60 | ? | uguale = disaccoppiato; diverso = metrica↔spin |
| $\omega_S$ | declina → ~0.17 | ? | più persistente = la plasticità sostiene la precessione |
| berry firm/abs | ~0 (incoerente) | ? | atteso ancora incoerente |
| `d0_max` | riferimento | atteso ↑ | volume nei punti tesi |
| `d0_mean` | riferimento | atteso ≈ | non gonfia ovunque |
| `stress` | riferimento | atteso ↓ | tensione sciolta dalla plasticità |

---

## 4. I run della campagna

| File diaglog (`out_spinore_plastdin/`) | Config | Spinore | plast-din | Seme |
|---|---|---|---|---|
| `m2_on_s1/2.csv` | binario base | vivo | **sì** | 1, 2 |
| `prec_on_s1/2.csv` | binario precessione piena | vivo | **sì** | 1, 2 |
| `m2_off_s1.csv` | binario base | congelato | **sì** | 1 |
| `prec_off_s1.csv` | binario precessione piena | congelato | **sì** | 1 |

Le baseline OFF qui hanno lo spinore congelato **ma plast-din attivo**: isolano
l'effetto della sola plasticità sulla metrica, senza il contributo dello spinore.

---

## 5. Riassunto operativo

1. Aspetta i 4 run ON completi (2000 passi, 2 semi).
2. Confronta $S_M$, $\omega_S$ con la base (`out_spinore/`) sull'ultimo terzo.
3. Confronta `d0_max`/`d0_mean`/`stress` base vs plast-din → dove/quanto genera volume.
4. Verifica se $\omega_S$ persiste di più con la plasticità (declino più lento).
5. Etichetta: dimostrato / in verifica / aperto.
