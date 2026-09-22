# `S05` e I DUE TEMPI PROPRI — **misurati sugli snapshot gia' scritti**

> Generato da `csv/_test_fork/_repulsione_e_due_tempi.py`. **Nessun run.** Legge gli
> archivi delle cure e il sorgente come testo.
>
> **Le costanti sono LETTE DAL SORGENTE, non ricordate:** `GAMMA = 0.05` · `TORS_4PI = True` · `TEMPO_SEGNO = False` · `TAU_LOC = 1.0` · `TEMPO_PROPRIO_ORIENTATO = False`.

## CANDIDATO 1 — **la repulsione alla massima compressione (`S05`)**

**IL PUNTO DI INVERSIONE, ricavato dal codice e non supposto:** con `soglia0 = 9.4248` *(= `3.00 pi`)* il `centro` vale **`2.7500`**, cioe' l'inversione di segno avviene a
**`|tw| = 10.9956` = `3.500 pi`**. *(La soglia LOCALE e' modulata di al piu' `-30 %`, quindi il punto di inversione vero varia per arco: si riporta quello misurato.)*

### La torsione contro il tetto `4pi`

| archivio | passo | archi | `max\|tw\|/pi` | `p50/pi` | `p99/pi` | `p99.99/pi` | `\|tw\| >= 2.5pi` | `\|tw\| >= 3.5pi` | `\|tw\| >= 4pi` |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| G4 riferimento (tutto acceso) | 120 | 526282 | **10.9325** | 0.5681 | 2.0344 | 8.8153 | 0.001997 | **0.001739** | 0.001668 |
| G4 riferimento (tutto acceso) | 240 | 526336 | **10.0055** | 0.5194 | 1.9884 | 8.6996 | 0.002058 | **0.001623** | 0.001539 |
| G4 riferimento (tutto acceso) | 360 | 526418 | **10.5001** | 0.4646 | 2.1644 | 8.1610 | 0.003148 | **0.001484** | 0.001362 |
| G4 riferimento (tutto acceso) | 480 | 526512 | **9.6588** | 0.4852 | 2.3493 | 7.2865 | 0.004955 | **0.001271** | 0.00105 |
| G4 riferimento (tutto acceso) | 600 | 526672 | **12.9967** | 0.5836 | 2.3836 | 6.4362 | 0.006594 | **0.0008221** | 0.000638 |
| G4 senza memoria del moto | 120 | 526318 | **12.1769** | 0.6720 | 2.0323 | 9.0919 | 0.002101 | **0.001794** | 0.001729 |
| G4 senza memoria del moto | 240 | 526357 | **10.4144** | 0.8328 | 2.1962 | 8.5622 | 0.002487 | **0.001662** | 0.001569 |
| G4 senza memoria del moto | 360 | 526398 | **11.9900** | 0.8127 | 2.2050 | 8.0540 | 0.003235 | **0.001474** | 0.001358 |
| G4 senza memoria del moto | 480 | 526476 | **11.2796** | 0.7422 | 2.2933 | 7.3104 | 0.00453 | **0.001313** | 0.001162 |
| G4 senza memoria del moto | 600 | 526619 | **10.7853** | 0.7094 | 2.4520 | 7.0126 | 0.008566 | **0.001058** | 0.0008621 |
| G3 senza gravita' bifase | 120 | 526246 | **9.8366** | 0.6849 | 2.1046 | 8.8870 | 0.002094 | **0.001667** | 0.001615 |
| G3 senza gravita' bifase | 240 | 526300 | **11.6216** | 0.5800 | 2.0952 | 8.7433 | 0.002512 | **0.001604** | 0.001526 |
| G3 senza gravita' bifase | 360 | 526376 | **10.0125** | 0.5617 | 2.1383 | 7.9868 | 0.002605 | **0.001398** | 0.001294 |
| G3 senza gravita' bifase | 480 | 526491 | **9.4783** | 0.6006 | 2.2876 | 7.2559 | 0.005398 | **0.001193** | 0.001045 |
| G3 senza gravita' bifase | 600 | 526784 | **12.2552** | 0.6054 | 2.3300 | 6.7085 | 0.005334 | **0.0008049** | 0.0006454 |
| validazione 600 (`_val600`) | 120 | 526282 | **10.9325** | 0.5681 | 2.0344 | 8.8153 | 0.001997 | **0.001739** | 0.001668 |
| validazione 600 (`_val600`) | 240 | 526336 | **10.0055** | 0.5194 | 1.9884 | 8.6996 | 0.002058 | **0.001623** | 0.001539 |
| validazione 600 (`_val600`) | 360 | 526418 | **10.5001** | 0.4646 | 2.1644 | 8.1610 | 0.003148 | **0.001484** | 0.001362 |
| validazione 600 (`_val600`) | 480 | 526512 | **9.6588** | 0.4852 | 2.3493 | 7.2865 | 0.004955 | **0.001271** | 0.00105 |
| validazione 600 (`_val600`) | 600 | 526672 | **12.9967** | 0.5836 | 2.3836 | 6.4362 | 0.006594 | **0.0008221** | 0.000638 |

### Il SEGNO: quanti archi sono davvero in repulsione

| archivio | passo | archi | `tau_pp > centro` | **`resp < 0`** | `min(resp)` | `_rep > 0` | `max(_rep)` | somma della spinta `0.02*d0*_rep` |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| G4 riferimento (tutto acceso) | 120 | 526282 | 928 | **50** | -1.671e-02 | 1873 | 1.585e-03 | 2.888e-03 |
| G4 riferimento (tutto acceso) | 240 | 526336 | 861 | **51** | -1.492e-02 | 2187 | 3.000e-03 | 3.972e-03 |
| G4 riferimento (tutto acceso) | 360 | 526418 | 802 | **85** | -1.351e-02 | 2518 | 3.229e-03 | 6.322e-03 |
| G4 riferimento (tutto acceso) | 480 | 526512 | 682 | **129** | -1.239e-02 | 2839 | 1.796e-03 | 9.560e-03 |
| G4 riferimento (tutto acceso) | 600 | 526672 | 446 | **110** | -1.581e-02 | 3073 | 2.153e-03 | 1.271e-02 |
| G4 senza memoria del moto | 120 | 526318 | 953 | **43** | -1.689e-02 | 1938 | 1.834e-03 | 2.888e-03 |
| G4 senza memoria del moto | 240 | 526357 | 885 | **59** | -1.445e-02 | 2167 | 1.907e-03 | 2.850e-03 |
| G4 senza memoria del moto | 360 | 526398 | 791 | **76** | -1.578e-02 | 2448 | 1.590e-03 | 3.688e-03 |
| G4 senza memoria del moto | 480 | 526476 | 700 | **88** | -1.632e-02 | 2754 | 1.574e-03 | 5.375e-03 |
| G4 senza memoria del moto | 600 | 526619 | 571 | **117** | -1.637e-02 | 3015 | 1.576e-03 | 7.441e-03 |
| G3 senza gravita' bifase | 120 | 526246 | 887 | **37** | -1.472e-02 | 1538 | 8.622e-04 | 2.589e-03 |
| G3 senza gravita' bifase | 240 | 526300 | 853 | **50** | -1.468e-02 | 1768 | 1.752e-03 | 3.618e-03 |
| G3 senza gravita' bifase | 360 | 526376 | 752 | **71** | -8.346e-03 | 2099 | 2.124e-03 | 5.353e-03 |
| G3 senza gravita' bifase | 480 | 526491 | 642 | **92** | -1.469e-02 | 2415 | 1.903e-03 | 6.975e-03 |
| G3 senza gravita' bifase | 600 | 526784 | 446 | **106** | -1.698e-02 | 2782 | 2.253e-03 | 8.398e-03 |
| validazione 600 (`_val600`) | 120 | 526282 | 928 | **50** | -1.671e-02 | 1873 | 1.585e-03 | 2.888e-03 |
| validazione 600 (`_val600`) | 240 | 526336 | 861 | **51** | -1.492e-02 | 2187 | 3.000e-03 | 3.972e-03 |
| validazione 600 (`_val600`) | 360 | 526418 | 802 | **85** | -1.351e-02 | 2518 | 3.229e-03 | 6.322e-03 |
| validazione 600 (`_val600`) | 480 | 526512 | 682 | **129** | -1.239e-02 | 2839 | 1.796e-03 | 9.560e-03 |
| validazione 600 (`_val600`) | 600 | 526672 | 446 | **110** | -1.581e-02 | 3073 | 2.153e-03 | 1.271e-02 |

**ARCHI IN REPULSIONE, sommati su tutti gli snapshot: 1589.**


### ⚠ **LA FINESTRA DELLA REPULSIONE: fra l'inversione del SEGNO e lo zero dell'AMPIEZZA**

> **`resp = salita * discesa * (1/tau_pp) * segno`.** Il `segno` si inverte a `tau_pp > centro`, cioe' **oltre `~3.5pi`**.
> **Ma `discesa = clip(1 - |tw|/4pi, 0, 1)` vale ESATTAMENTE ZERO per `|tw| >= 4pi`.**
> **Quindi la repulsione puo' esistere SOLO nella finestra `[~3.5pi, 4pi)`, larga mezzo `pi`** — e **oltre il tetto e' zero per costruzione**, cioe' **proprio dove la materia e' piu' compressa**, che e' il caso per cui la legge dichiara di esistere.

| archivio | passo | oltre l'inversione | **nella finestra `[3.5pi, 4pi)`** | **oltre `4pi`: repulsione ZERO** | quota azzerata |
|---|--:|--:|--:|--:|--:|
| G4 riferimento (tutto acceso) | 120 | 928 | **37** | **878** | **94.6 %** |
| G4 riferimento (tutto acceso) | 240 | 861 | **44** | **810** | **94.1 %** |
| G4 riferimento (tutto acceso) | 360 | 802 | **64** | **717** | **89.4 %** |
| G4 riferimento (tutto acceso) | 480 | 682 | **116** | **553** | **81.1 %** |
| G4 riferimento (tutto acceso) | 600 | 446 | **97** | **336** | **75.3 %** |
| G4 senza memoria del moto | 120 | 953 | **34** | **910** | **95.5 %** |
| G4 senza memoria del moto | 240 | 885 | **49** | **826** | **93.3 %** |
| G4 senza memoria del moto | 360 | 791 | **61** | **715** | **90.4 %** |
| G4 senza memoria del moto | 480 | 700 | **79** | **612** | **87.4 %** |
| G4 senza memoria del moto | 600 | 571 | **103** | **454** | **79.5 %** |
| G3 senza gravita' bifase | 120 | 887 | **27** | **850** | **95.8 %** |
| G3 senza gravita' bifase | 240 | 853 | **41** | **803** | **94.1 %** |
| G3 senza gravita' bifase | 360 | 752 | **55** | **681** | **90.6 %** |
| G3 senza gravita' bifase | 480 | 642 | **78** | **550** | **85.7 %** |
| G3 senza gravita' bifase | 600 | 446 | **84** | **340** | **76.2 %** |
| validazione 600 (`_val600`) | 120 | 928 | **37** | **878** | **94.6 %** |
| validazione 600 (`_val600`) | 240 | 861 | **44** | **810** | **94.1 %** |
| validazione 600 (`_val600`) | 360 | 802 | **64** | **717** | **89.4 %** |
| validazione 600 (`_val600`) | 480 | 682 | **116** | **553** | **81.1 %** |
| validazione 600 (`_val600`) | 600 | 446 | **97** | **336** | **75.3 %** |

**⚠ E LA VERIFICA CHE LA FINESTRA E' DAVVERO IL VINCOLO:** `min(resp)` vale `~-1.5e-02` su tutti gli snapshot — **non cresce mai**, perche' gli archi che potrebbero dare una repulsione grande sono **esattamente quelli che `discesa` azzera**.

## CANDIDATO 2 — **due definizioni di tempo proprio**

### I punti del codice, letti dal sorgente

**`r` / `dt_n` — il ritmo dei NODI: 57 righe** *(di cui 26 in commento)*.

| riga | | codice |
|--:|---|---|
| `249` | cod | `'_r_corrente':   ('pos', 'ritmo dell orologio locale: un RITMO e positivo'),` |
| `1193` | cod | `TEMPO_PROPRIO_ORIENTATO = False # FLAG 4 (separato, profondo): toglie \|.\| da f in ritmo() -> r con SEGNO` |
| `1496` | cod | `self._r_corrente = None` |
| `1758` | cod | `_psi_prec (evita il reset spurio globale in ritmo() su len!=n). No-op se --spinore-corretto off.` |
| `2647` | cod | `def _passo_spinoriale(self, i, j, w, dt_n, psi_snapshot=None,` |
| `2707` | cod | `_dtl = dt_n if np.isscalar(dt_n) else np.asarray(dt_n, float)[:n]` |
| `2968` | cod | `dtn = dt_n if np.isscalar(dt_n) else np.asarray(dt_n)[:n]` |
| `4067` | cod | `alpha = 1 - exp(-dt_n/tau)                 dt_n = DT*r = TEMPO PROPRIO del nodo` |
| `4103` | cod | `r_loc = getattr(self, "_r_corrente", None)` |
| `4104` | cod | `if r_loc is None or len(r_loc) < n:` |
| `4105` | cod | `dt_n = np.full(n, DT)           # orologio globale (TAU_LOC = 0): r == 1 -> dt_n = DT` |
| `4107` | cod | `dt_n = DT * np.asarray(r_loc, float)[:n]` |
| `4108` | cod | `alpha = 1.0 - np.exp(-dt_n / tau)   # rilassamento ESATTO, non un eulero esplicito` |
| `4277` | cod | `r = self.ritmo()                       # None se l'orologio e' globale` |
| `4279` | cod | `dt_n = DT; dt_e = DT` |
| `4281` | cod | `dt_n = DT * r                      # per nodo` |
| `4327` | cod | `self._r_corrente = r` |
| `4331` | cod | `dt_n_s = dt_n` |
| `4337` | cod | `if TEMPO_SEGNO and not (not np.isscalar(dt_n) and len(self.perc_chi) >= self.n` |
| `4342` | cod | `if TEMPO_SEGNO and not np.isscalar(dt_n) and len(self.perc_chi) >= self.n and len(self.psi) >= self.n:` |
| `4345` | cod | `dt_n_s = (1.0 + (_pc - 1.0) * _mcoer) * dt_n` |
| `4346` | cod | `w = self._pesi(); self.eta += dt_n` |
| `4526` | cod | `dt_scal = float(np.median(dt_n)) if np.ndim(dt_n) else float(dt_n)` |
| `7341` | cod | `print("[tempo-proprio-orientato] ritmo() con segno: r orientato (toglie \|.\| da f)")` |
| `7409` | cod | `"Ornstein-Uhlenbeck sul rumore stesso e `dt_n = DT*r` (non DT: e' un processo "` |
| `7874` | cod | `help="FLAG 4 (separato, profondo): toglie \|.\| da f in ritmo() -> r con SEGNO (tempo proprio "` |
| `7917` | cod | `"nuovi, `amp` INVARIATA, `dt` = dt_n = DT*r (processo locale). "` |
| `7988` | cod | `"va avanti); omega/fase interne usano s_k*dt_n, eta/geometria usano \|dt_n\|. La MAGNITUDINE del "` |
| `7989` | cod | `"ritmo() diventa la torsione esplicita 1+\|tw\|/PHI_CRIT (il de Broglie del campo emesso, bocciato "` |
| `8269` | cod | `tau = net.ritmo()` |
| `8927` | cod | `tau = net.ritmo()` |

**`tau_pp` — il surrogato per ARCO: 16 righe** *(di cui 4 in commento)*.

| riga | | codice |
|--:|---|---|
| `2553` | cod | `return 1.0 + (twn / np.maximum(deg, 1.0)) / max(PHI_CRIT, 1e-9)` |
| `5120` | cod | `tau_nodo = 1.0 + tau_nodo / np.maximum(self._deg, 1) / PHI_CRIT` |
| `5160` | cod | `tau_pp = 1.0 + avv / PHI_CRIT                     # tempo proprio locale (>=1)` |
| `5161` | cod | `tau_soglia = 1.0 + soglia / PHI_CRIT              # tempo proprio ALLA soglia (locale)` |
| `5162` | cod | `tau_tetto = 1.0 + TW_TETTO / PHI_CRIT             # tempo proprio al tetto 4pi (=3)` |
| `5166` | cod | `segno = -np.tanh(3.0 * (tau_pp - centro))` |
| `5167` | cod | `tau_locale = 1.0 / tau_pp                          # ritmo (sempre positivo)` |
| `5205` | cod | `self._rep_taupp_clamp = getattr(self, "_rep_taupp_clamp", 0) + int(np.sum(np.asarray(tau_pp) < 1e-12))` |
| `5206` | cod | `self._rep_taupp_tot = getattr(self, "_rep_taupp_tot", 0) + int(np.size(tau_pp))` |
| `5207` | cod | `self._rep = self._rep + _dte * (rep - self._rep) / np.maximum(tau_pp, 1e-12)` |
| `5324` | cod | `tau_a = 1.0 + np.abs(self.tw[sel]) / PHI_CRIT` |
| `5353` | cod | `d0h = dh * (1.0 + PLAST_MIT * sciolta)   # sciolta = \|tw\|/PHI_CRIT >= 1` |

### Quanto differiscono, sugli STESSI nodi

> `tau_nodo = 1 + mean(|tw| sugli archi incidenti)/PHI_CRIT` e' **la forma esatta** che
> `ritmo()` userebbe nel ramo `TEMPO_SEGNO` *(`:2553`)* e che `mitosi()` usa per il
> gradiente *(`:5120`)*. **Si confronta con `r` = `_r_corrente`, quello che il sistema
> usa davvero in `dt_n = DT*r`.**

| archivio | passo | nodi | `med r` | `med tau_nodo` | correlazione | `med(r/tau_nodo)` | `p01` | `p99` | `max/min` di `r` |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| G4 riferimento (tutto acceso) | 120 | 2647 | 1.018363 | 1.435352 | **+0.1058** | 6.6729e-01 | 4.9318e-03 | 1.1657e+00 | 1.301e+04 |
| G4 riferimento (tutto acceso) | 240 | 2694 | 0.593971 | 1.407897 | **-0.0600** | 4.0748e-01 | 5.0042e-03 | 1.1122e+00 | 2.014e+04 |
| G4 riferimento (tutto acceso) | 360 | 2760 ⚠ | 0.763052 | 1.428474 | **-0.1299** | 5.2129e-01 | 4.6729e-03 | 1.2308e+00 | 1.000e+06 |
| G4 riferimento (tutto acceso) | 480 | 2836 | 0.344277 | 1.434849 | **+0.2875** | 2.4626e-01 | 7.1849e-03 | 1.0268e+00 | 2.971e+04 |
| G4 riferimento (tutto acceso) | 600 | 2952 ⚠ | 1.408827 | 1.416630 | **+0.0147** | 9.7420e-01 | 2.4639e-01 | 1.2307e+00 | 1.376e+02 |
| G4 senza memoria del moto | 120 | 2668 ⚠ | 1.148017 | 1.453643 | **-0.0450** | 7.9070e-01 | 1.8363e-02 | 1.0774e+00 | 3.720e+03 |
| G4 senza memoria del moto | 240 | 2703 | 1.013702 | 1.456750 | **+0.1553** | 6.3758e-01 | 8.8260e-03 | 1.0404e+00 | 2.304e+04 |
| G4 senza memoria del moto | 360 | 2736 ⚠ | 1.176403 | 1.444988 | **+0.1410** | 7.3635e-01 | 5.9707e-03 | 1.0736e+00 | 4.349e+03 |
| G4 senza memoria del moto | 480 | 2798 ⚠ | 1.111639 | 1.437518 | **+0.0761** | 7.0458e-01 | 1.0666e-02 | 1.1206e+00 | 1.498e+03 |
| G4 senza memoria del moto | 600 | 2913 ⚠ | 1.109436 | 1.438291 | **+0.0872** | 6.9708e-01 | 1.7252e-02 | 1.1048e+00 | 7.057e+02 |
| G3 senza gravita' bifase | 120 | 2617 | 0.926422 | 1.464281 | **-0.1241** | 5.9455e-01 | 1.0104e-02 | 1.1770e+00 | 1.678e+04 |
| G3 senza gravita' bifase | 240 | 2658 ⚠ | 1.382121 | 1.449706 | **-0.0406** | 9.2570e-01 | 4.9437e-02 | 1.2129e+00 | 3.764e+02 |
| G3 senza gravita' bifase | 360 | 2723 | 0.664293 | 1.445179 | **-0.0963** | 4.5104e-01 | 2.1045e-03 | 1.1906e+00 | 1.000e+06 |
| G3 senza gravita' bifase | 480 | 2814 ⚠ | 1.346234 | 1.469827 | **-0.1316** | 8.9567e-01 | 3.5006e-03 | 1.2107e+00 | 1.000e+06 |
| G3 senza gravita' bifase | 600 | 3055 ⚠ | 0.370034 | 1.431236 | **+0.3039** | 2.6481e-01 | 3.8319e-03 | 1.1508e+00 | 1.238e+03 |
| validazione 600 (`_val600`) | 120 | 2647 | 1.018363 | 1.435352 | **+0.1058** | 6.6729e-01 | 4.9318e-03 | 1.1657e+00 | 1.301e+04 |
| validazione 600 (`_val600`) | 240 | 2694 | 0.593971 | 1.407897 | **-0.0600** | 4.0748e-01 | 5.0042e-03 | 1.1122e+00 | 2.014e+04 |
| validazione 600 (`_val600`) | 360 | 2760 ⚠ | 0.763052 | 1.428474 | **-0.1299** | 5.2129e-01 | 4.6729e-03 | 1.2308e+00 | 1.000e+06 |
| validazione 600 (`_val600`) | 480 | 2836 | 0.344277 | 1.434849 | **+0.2875** | 2.4626e-01 | 7.1849e-03 | 1.0268e+00 | 2.971e+04 |
| validazione 600 (`_val600`) | 600 | 2952 ⚠ | 1.408827 | 1.416630 | **+0.0147** | 9.7420e-01 | 2.4639e-01 | 1.2307e+00 | 1.376e+02 |

⚠ `⚠` accanto al numero di nodi = **`_r_corrente` era PIU' CORTO di `_deg`** e si e' tagliato al minimo. E' la stessa famiglia di `A8b` *(cache cross-passo da estendere a ogni punto di crescita)*, e si dichiara invece di nasconderla.

## LE LETTURE, fissate PRIMA

1. **`S05` e' INERTE se `resp < 0` non capita MAI.** Se capita ma poco, **non si dice «inerte»**: si dice **quanto**, e si confronta col saldo degli altri scrittori *(par.9: un negativo si scrive come LIMITE)*.
2. **I due tempi sono la STESSA grandezza** se correlazione `~1` e rapporto con dispersione trascurabile; **DIVERSI** se la correlazione e' bassa o il rapporto varia di ordini di grandezza.

**LIMITI:** UN seme, UNA scena, gli archivi delle cure. **Il `2.5pi` del commento `:64-66` e' PRE-FORK** *(par.9-bis)*: qui non si sta verificando quel numero, si sta misurando **quello di oggi**.
