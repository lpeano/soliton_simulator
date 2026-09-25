# OGNI LETTURA DI `eta`, **PER AST** — la verifica che precede `RAMPA-1`

*(`csv/_letture_eta.py`. Decisione di Luca, 2026-09-25: `RAMPA-1` strada (3), il vuoto dato
ha **eta infinita**. Sola lettura: nessuna riga del simulatore cambia qui.)*

> **`+inf` non e' un numero grande, e' un VALORE SPECIALE.** `inf/inf = nan`,
> `inf - inf = nan`, una **media** che lo contiene vale `inf`, un `sum` diventa `inf`.
> **Quindi la domanda non e' «dove sta scritto `eta`»: e' «chi lo RIDUCE».**

## ① IL SIMULATORE — `soliton_simulator.py`

| riga | cosa | codice | **riduzione?** |
|---|---|---|---|
| `:1605` | scrittura | `self.phivel = np.zeros(0); self.eta = np.zeros(0)` | — |
| `:2720` | scrittura | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `:2720` | lettura | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `:2723` | scrittura | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `:2723` | lettura | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `:2747` | lettura | `self.eta[_a:_b] = np.asarray(_tr, float)[_a:_b]` | — |
| `:2752` | lettura | `self.eta[_a:_b] = float(_tr)` | — |
| `:3419` | lettura | `_tq = _tq * np.minimum(1.0, self.eta[:n] / _trq)[:, None]` | — |
| `:3684` | lettura | `ramp = np.minimum(1.0, self.eta / _tr)` | — |
| `:4976` | scrittura | `w = self._pesi(); self.eta += dt_n` | — |
| `:6022` | scrittura | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `:6022` | lettura | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `:6178` | scrittura | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `:6178` | lettura | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `:9332` | lettura | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len(net.eta) >= n e` | — |
| `:9332` | lettura | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len(net.eta) >= n e` | — |
| `:9332` | lettura | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len(net.eta) >= n e` | — |

```
occorrenze di `eta` nel simulatore   17
letture                              11
scritture                            6
CON UNA RIDUZIONE sulla stessa riga  0
```

### IL GUARDIANO DICEVA `:3419`, `:3684` e l'incremento a `:4976`

```
righe attese dal guardiano   [3419, 3684, 4976]
righe TROVATE per AST        [1605, 2720, 2723, 2747, 2752, 3419, 3684, 4976, 6022, 6178, 9332]
attese e NON trovate         nessuna
trovate e NON attese         [1605, 2720, 2723, 2747, 2752, 6022, 6178, 9332]
```

## ② GLI STRUMENTI DI `csv/`

| file | riga | codice | **riduzione?** |
|---|---|---|---|
| `csv/_seal_53a/_sigillo_53a.py` | `:51` | `eta_min = min(eta_min, float(np.min(net.eta[:net.n])) if net.n else 0.0)` | ⚠ **min** |
| `csv/_seal_53c/_old_sim.py` | `:786` | `self.phivel = np.zeros(0); self.eta = np.zeros(0)` | — |
| `csv/_seal_53c/_old_sim.py` | `:1388` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_53c/_old_sim.py` | `:1388` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_53c/_old_sim.py` | `:1909` | `ramp = np.minimum(1.0, self.eta / TAU_A)` | — |
| `csv/_seal_53c/_old_sim.py` | `:2201` | `w = self._pesi(); self.eta += dt_n` | — |
| `csv/_seal_53c/_old_sim.py` | `:2744` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_53c/_old_sim.py` | `:2744` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_53c/_old_sim.py` | `:2861` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_53c/_old_sim.py` | `:2861` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_53c/_old_sim.py` | `:4939` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_53c/_old_sim.py` | `:4939` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_53c/_old_sim.py` | `:4939` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_ab_reciprocita.py` | `:199` | `eta = np.asarray(at["eta"], float)` | — |
| `csv/_seal_fork/_ab_reciprocita.py` | `:203` | `% (nome, om[k], min(1.0, eta[k] / float(_S.TAU_A)),` | ⚠ **min** |
| `csv/_seal_fork/_runner_sim.py` | `:106` | `eta=np.asarray(S.net.eta), n=np.asarray([S.net.n]),` | — |
| `csv/_seal_fork/_sigillo_anello.py` | `:108` | `snap[k + 1] = float(np.median(np.asarray(r.eta[:r.n], float))) if len(getattr(r,` | ⚠ **median** |
| `csv/_seal_fork/_sigillo_step2.py` | `:157` | `net.eta = np.full(n, S.TAU_A)          # <-- ramp = 1: i pesi esistono, omega_cl` | — |
| `csv/_seal_fork/_sigillo_turbo.py` | `:60` | `net.eta = np.full(n, S.TAU_A)             # ramp = 1: i pesi esistono (lezione d` | — |
| `csv/_seal_fork/_sigillo_Y5_riscritto.py` | `:72` | `eta = np.asarray(getattr(self, "eta", np.zeros(n)), float)[:n]` | — |
| `csv/_seal_fork/_sigillo_Y5_riscritto.py` | `:75` | `"grado": grado[idx].copy(), "eta": eta[idx].copy(),` | — |
| `csv/_seal_fork/_sigillo_Y5_riscritto.py` | `:76` | `"eta_med_tutti": float(np.median(eta))})` | ⚠ **median** |
| `csv/_seal_fork/_ab_chibasc/_sim_prima.py` | `:1089` | `self.phivel = np.zeros(0); self.eta = np.zeros(0)` | — |
| `csv/_seal_fork/_ab_chibasc/_sim_prima.py` | `:1926` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_ab_chibasc/_sim_prima.py` | `:1926` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_ab_chibasc/_sim_prima.py` | `:2583` | `_tq = _tq * np.minimum(1.0, self.eta[:n] / TAU_A)[:, None]` | — |
| `csv/_seal_fork/_ab_chibasc/_sim_prima.py` | `:2804` | `ramp = np.minimum(1.0, self.eta / TAU_A)` | — |
| `csv/_seal_fork/_ab_chibasc/_sim_prima.py` | `:3481` | `w = self._pesi(); self.eta += dt_n` | — |
| `csv/_seal_fork/_ab_chibasc/_sim_prima.py` | `:4291` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_ab_chibasc/_sim_prima.py` | `:4291` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_ab_chibasc/_sim_prima.py` | `:4412` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_ab_chibasc/_sim_prima.py` | `:4412` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_ab_chibasc/_sim_prima.py` | `:6944` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_ab_chibasc/_sim_prima.py` | `:6944` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_ab_chibasc/_sim_prima.py` | `:6944` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_anom_simm/_sim_prima.py` | `:1304` | `self.phivel = np.zeros(0); self.eta = np.zeros(0)` | — |
| `csv/_seal_fork/_sig_anom_simm/_sim_prima.py` | `:2191` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_anom_simm/_sim_prima.py` | `:2191` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_anom_simm/_sim_prima.py` | `:2855` | `_tq = _tq * np.minimum(1.0, self.eta[:n] / TAU_A)[:, None]` | — |
| `csv/_seal_fork/_sig_anom_simm/_sim_prima.py` | `:3076` | `ramp = np.minimum(1.0, self.eta / TAU_A)` | — |
| `csv/_seal_fork/_sig_anom_simm/_sim_prima.py` | `:4093` | `w = self._pesi(); self.eta += dt_n` | — |
| `csv/_seal_fork/_sig_anom_simm/_sim_prima.py` | `:5018` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_anom_simm/_sim_prima.py` | `:5018` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_anom_simm/_sim_prima.py` | `:5163` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_anom_simm/_sim_prima.py` | `:5163` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_anom_simm/_sim_prima.py` | `:7972` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_anom_simm/_sim_prima.py` | `:7972` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_anom_simm/_sim_prima.py` | `:7972` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_chicoop/_sim_prima.py` | `:1109` | `self.phivel = np.zeros(0); self.eta = np.zeros(0)` | — |
| `csv/_seal_fork/_sig_chicoop/_sim_prima.py` | `:1965` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_chicoop/_sim_prima.py` | `:1965` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_chicoop/_sim_prima.py` | `:2624` | `_tq = _tq * np.minimum(1.0, self.eta[:n] / TAU_A)[:, None]` | — |
| `csv/_seal_fork/_sig_chicoop/_sim_prima.py` | `:2845` | `ramp = np.minimum(1.0, self.eta / TAU_A)` | — |
| `csv/_seal_fork/_sig_chicoop/_sim_prima.py` | `:3640` | `w = self._pesi(); self.eta += dt_n` | — |
| `csv/_seal_fork/_sig_chicoop/_sim_prima.py` | `:4464` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_chicoop/_sim_prima.py` | `:4464` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_chicoop/_sim_prima.py` | `:4594` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_chicoop/_sim_prima.py` | `:4594` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_chicoop/_sim_prima.py` | `:7159` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_chicoop/_sim_prima.py` | `:7159` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_chicoop/_sim_prima.py` | `:7159` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_coes_causale/_sim_prima.py` | `:1276` | `self.phivel = np.zeros(0); self.eta = np.zeros(0)` | — |
| `csv/_seal_fork/_sig_coes_causale/_sim_prima.py` | `:2163` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_coes_causale/_sim_prima.py` | `:2163` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_coes_causale/_sim_prima.py` | `:2827` | `_tq = _tq * np.minimum(1.0, self.eta[:n] / TAU_A)[:, None]` | — |
| `csv/_seal_fork/_sig_coes_causale/_sim_prima.py` | `:3048` | `ramp = np.minimum(1.0, self.eta / TAU_A)` | — |
| `csv/_seal_fork/_sig_coes_causale/_sim_prima.py` | `:4054` | `w = self._pesi(); self.eta += dt_n` | — |
| `csv/_seal_fork/_sig_coes_causale/_sim_prima.py` | `:4979` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_coes_causale/_sim_prima.py` | `:4979` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_coes_causale/_sim_prima.py` | `:5124` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_coes_causale/_sim_prima.py` | `:5124` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_coes_causale/_sim_prima.py` | `:7854` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_coes_causale/_sim_prima.py` | `:7854` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_coes_causale/_sim_prima.py` | `:7854` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_contatori/_sim_prima.py` | `:1053` | `self.phivel = np.zeros(0); self.eta = np.zeros(0)` | — |
| `csv/_seal_fork/_sig_contatori/_sim_prima.py` | `:1890` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_contatori/_sim_prima.py` | `:1890` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_contatori/_sim_prima.py` | `:2508` | `_tq = _tq * np.minimum(1.0, self.eta[:n] / TAU_A)[:, None]` | — |
| `csv/_seal_fork/_sig_contatori/_sim_prima.py` | `:2729` | `ramp = np.minimum(1.0, self.eta / TAU_A)` | — |
| `csv/_seal_fork/_sig_contatori/_sim_prima.py` | `:3373` | `w = self._pesi(); self.eta += dt_n` | — |
| `csv/_seal_fork/_sig_contatori/_sim_prima.py` | `:4136` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_contatori/_sim_prima.py` | `:4136` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_contatori/_sim_prima.py` | `:4257` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_contatori/_sim_prima.py` | `:4257` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_contatori/_sim_prima.py` | `:6748` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_contatori/_sim_prima.py` | `:6748` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_contatori/_sim_prima.py` | `:6748` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_dieci/_sim_prima.py` | `:1062` | `self.phivel = np.zeros(0); self.eta = np.zeros(0)` | — |
| `csv/_seal_fork/_sig_dieci/_sim_prima.py` | `:1899` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_dieci/_sim_prima.py` | `:1899` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_dieci/_sim_prima.py` | `:2517` | `_tq = _tq * np.minimum(1.0, self.eta[:n] / TAU_A)[:, None]` | — |
| `csv/_seal_fork/_sig_dieci/_sim_prima.py` | `:2738` | `ramp = np.minimum(1.0, self.eta / TAU_A)` | — |
| `csv/_seal_fork/_sig_dieci/_sim_prima.py` | `:3394` | `w = self._pesi(); self.eta += dt_n` | — |
| `csv/_seal_fork/_sig_dieci/_sim_prima.py` | `:4178` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_dieci/_sim_prima.py` | `:4178` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_dieci/_sim_prima.py` | `:4299` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_dieci/_sim_prima.py` | `:4299` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_dieci/_sim_prima.py` | `:6809` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_dieci/_sim_prima.py` | `:6809` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_dieci/_sim_prima.py` | `:6809` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_invarianti/_sim_prima.py` | `:1328` | `self.phivel = np.zeros(0); self.eta = np.zeros(0)` | — |
| `csv/_seal_fork/_sig_invarianti/_sim_prima.py` | `:2215` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_invarianti/_sim_prima.py` | `:2215` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_invarianti/_sim_prima.py` | `:2879` | `_tq = _tq * np.minimum(1.0, self.eta[:n] / TAU_A)[:, None]` | — |
| `csv/_seal_fork/_sig_invarianti/_sim_prima.py` | `:3100` | `ramp = np.minimum(1.0, self.eta / TAU_A)` | — |
| `csv/_seal_fork/_sig_invarianti/_sim_prima.py` | `:4117` | `w = self._pesi(); self.eta += dt_n` | — |
| `csv/_seal_fork/_sig_invarianti/_sim_prima.py` | `:5065` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_invarianti/_sim_prima.py` | `:5065` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_invarianti/_sim_prima.py` | `:5210` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_invarianti/_sim_prima.py` | `:5210` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_invarianti/_sim_prima.py` | `:8042` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_invarianti/_sim_prima.py` | `:8042` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_invarianti/_sim_prima.py` | `:8042` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_peq_esatto/_sim_prima.py` | `:1203` | `self.phivel = np.zeros(0); self.eta = np.zeros(0)` | — |
| `csv/_seal_fork/_sig_peq_esatto/_sim_prima.py` | `:2090` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_peq_esatto/_sim_prima.py` | `:2090` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_peq_esatto/_sim_prima.py` | `:2753` | `_tq = _tq * np.minimum(1.0, self.eta[:n] / TAU_A)[:, None]` | — |
| `csv/_seal_fork/_sig_peq_esatto/_sim_prima.py` | `:2974` | `ramp = np.minimum(1.0, self.eta / TAU_A)` | — |
| `csv/_seal_fork/_sig_peq_esatto/_sim_prima.py` | `:3884` | `w = self._pesi(); self.eta += dt_n` | — |
| `csv/_seal_fork/_sig_peq_esatto/_sim_prima.py` | `:4747` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_peq_esatto/_sim_prima.py` | `:4747` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_peq_esatto/_sim_prima.py` | `:4883` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_peq_esatto/_sim_prima.py` | `:4883` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_peq_esatto/_sim_prima.py` | `:7546` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_peq_esatto/_sim_prima.py` | `:7546` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_peq_esatto/_sim_prima.py` | `:7546` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_peq_nascita/_sim_prima.py` | `:1235` | `self.phivel = np.zeros(0); self.eta = np.zeros(0)` | — |
| `csv/_seal_fork/_sig_peq_nascita/_sim_prima.py` | `:2122` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_peq_nascita/_sim_prima.py` | `:2122` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_peq_nascita/_sim_prima.py` | `:2785` | `_tq = _tq * np.minimum(1.0, self.eta[:n] / TAU_A)[:, None]` | — |
| `csv/_seal_fork/_sig_peq_nascita/_sim_prima.py` | `:3006` | `ramp = np.minimum(1.0, self.eta / TAU_A)` | — |
| `csv/_seal_fork/_sig_peq_nascita/_sim_prima.py` | `:3952` | `w = self._pesi(); self.eta += dt_n` | — |
| `csv/_seal_fork/_sig_peq_nascita/_sim_prima.py` | `:4821` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_peq_nascita/_sim_prima.py` | `:4821` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_peq_nascita/_sim_prima.py` | `:4957` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_peq_nascita/_sim_prima.py` | `:4957` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_peq_nascita/_sim_prima.py` | `:7639` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_peq_nascita/_sim_prima.py` | `:7639` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_peq_nascita/_sim_prima.py` | `:7639` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_scala_min_passo/_sim_prima.py` | `:1255` | `self.phivel = np.zeros(0); self.eta = np.zeros(0)` | — |
| `csv/_seal_fork/_sig_scala_min_passo/_sim_prima.py` | `:2142` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_scala_min_passo/_sim_prima.py` | `:2142` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_scala_min_passo/_sim_prima.py` | `:2805` | `_tq = _tq * np.minimum(1.0, self.eta[:n] / TAU_A)[:, None]` | — |
| `csv/_seal_fork/_sig_scala_min_passo/_sim_prima.py` | `:3026` | `ramp = np.minimum(1.0, self.eta / TAU_A)` | — |
| `csv/_seal_fork/_sig_scala_min_passo/_sim_prima.py` | `:3972` | `w = self._pesi(); self.eta += dt_n` | — |
| `csv/_seal_fork/_sig_scala_min_passo/_sim_prima.py` | `:4874` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_scala_min_passo/_sim_prima.py` | `:4874` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_scala_min_passo/_sim_prima.py` | `:5018` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_scala_min_passo/_sim_prima.py` | `:5018` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_scala_min_passo/_sim_prima.py` | `:7721` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_scala_min_passo/_sim_prima.py` | `:7721` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_scala_min_passo/_sim_prima.py` | `:7721` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_scala_p/_sim_prima.py` | `:1048` | `self.phivel = np.zeros(0); self.eta = np.zeros(0)` | — |
| `csv/_seal_fork/_sig_scala_p/_sim_prima.py` | `:1885` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_scala_p/_sim_prima.py` | `:1885` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_scala_p/_sim_prima.py` | `:2503` | `_tq = _tq * np.minimum(1.0, self.eta[:n] / TAU_A)[:, None]` | — |
| `csv/_seal_fork/_sig_scala_p/_sim_prima.py` | `:2724` | `ramp = np.minimum(1.0, self.eta / TAU_A)` | — |
| `csv/_seal_fork/_sig_scala_p/_sim_prima.py` | `:3368` | `w = self._pesi(); self.eta += dt_n` | — |
| `csv/_seal_fork/_sig_scala_p/_sim_prima.py` | `:4131` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_scala_p/_sim_prima.py` | `:4131` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_scala_p/_sim_prima.py` | `:4252` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_scala_p/_sim_prima.py` | `:4252` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_scala_p/_sim_prima.py` | `:6696` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_scala_p/_sim_prima.py` | `:6696` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_scala_p/_sim_prima.py` | `:6696` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_traccia_d0/_sim_prima.py` | `:1102` | `self.phivel = np.zeros(0); self.eta = np.zeros(0)` | — |
| `csv/_seal_fork/_sig_traccia_d0/_sim_prima.py` | `:1958` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_traccia_d0/_sim_prima.py` | `:1958` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_traccia_d0/_sim_prima.py` | `:2617` | `_tq = _tq * np.minimum(1.0, self.eta[:n] / TAU_A)[:, None]` | — |
| `csv/_seal_fork/_sig_traccia_d0/_sim_prima.py` | `:2838` | `ramp = np.minimum(1.0, self.eta / TAU_A)` | — |
| `csv/_seal_fork/_sig_traccia_d0/_sim_prima.py` | `:3593` | `w = self._pesi(); self.eta += dt_n` | — |
| `csv/_seal_fork/_sig_traccia_d0/_sim_prima.py` | `:4415` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_traccia_d0/_sim_prima.py` | `:4415` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_traccia_d0/_sim_prima.py` | `:4545` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_traccia_d0/_sim_prima.py` | `:4545` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_traccia_d0/_sim_prima.py` | `:7110` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_traccia_d0/_sim_prima.py` | `:7110` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_traccia_d0/_sim_prima.py` | `:7110` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_traccia_peq/_sim_committato.py` | `:1187` | `self.phivel = np.zeros(0); self.eta = np.zeros(0)` | — |
| `csv/_seal_fork/_sig_traccia_peq/_sim_committato.py` | `:2074` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_traccia_peq/_sim_committato.py` | `:2074` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_fork/_sig_traccia_peq/_sim_committato.py` | `:2737` | `_tq = _tq * np.minimum(1.0, self.eta[:n] / TAU_A)[:, None]` | — |
| `csv/_seal_fork/_sig_traccia_peq/_sim_committato.py` | `:2958` | `ramp = np.minimum(1.0, self.eta / TAU_A)` | — |
| `csv/_seal_fork/_sig_traccia_peq/_sim_committato.py` | `:3823` | `w = self._pesi(); self.eta += dt_n` | — |
| `csv/_seal_fork/_sig_traccia_peq/_sim_committato.py` | `:4674` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_traccia_peq/_sim_committato.py` | `:4674` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_fork/_sig_traccia_peq/_sim_committato.py` | `:4810` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_traccia_peq/_sim_committato.py` | `:4810` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_fork/_sig_traccia_peq/_sim_committato.py` | `:7473` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_traccia_peq/_sim_committato.py` | `:7473` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_fork/_sig_traccia_peq/_sim_committato.py` | `:7473` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_k2/_old_sim.py` | `:769` | `self.phivel = np.zeros(0); self.eta = np.zeros(0)` | — |
| `csv/_seal_k2/_old_sim.py` | `:1371` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_k2/_old_sim.py` | `:1371` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_seal_k2/_old_sim.py` | `:1845` | `ramp = np.minimum(1.0, self.eta / TAU_A)` | — |
| `csv/_seal_k2/_old_sim.py` | `:2060` | `w = self._pesi(); self.eta += dt_n` | — |
| `csv/_seal_k2/_old_sim.py` | `:2603` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_k2/_old_sim.py` | `:2603` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_seal_k2/_old_sim.py` | `:2720` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_k2/_old_sim.py` | `:2720` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_seal_k2/_old_sim.py` | `:4758` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_k2/_old_sim.py` | `:4758` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_seal_k2/_old_sim.py` | `:4758` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_test_fork/_arco_innesco.py` | `:141` | `% (float(np.asarray(net.eta)[int(ii[kp])]),` | — |
| `csv/_test_fork/_arco_innesco.py` | `:142` | `float(np.asarray(net.eta)[int(jj[kp])]), S.TAU_A))` | — |
| `csv/_test_fork/_chi_non_invecchia.py` | `:74` | `e, n = eta(s)` | — |
| `csv/_test_fork/_chi_non_ruota.py` | `:102` | `eta=np.asarray(self.eta[:n], float).copy(),` | — |
| `csv/_test_fork/_esperimento_spin_feedback.py` | `:146` | `eta = np.asarray(X.get("eta"), float)[:len(np.asarray(X["psi"]))]` | — |
| `csv/_test_fork/_esperimento_spin_feedback.py` | `:147` | `ramp = np.minimum(1.0, eta / ta)` | — |
| `csv/_test_fork/_esperimento_tau_a.py` | `:129` | `eta = np.asarray(X.get("eta"), float)` | — |
| `csv/_test_fork/_esperimento_tau_a.py` | `:131` | `eta = eta[:n]` | — |
| `csv/_test_fork/_esperimento_tau_a.py` | `:131` | `eta = eta[:n]` | — |
| `csv/_test_fork/_esperimento_tau_a.py` | `:132` | `ramp = np.minimum(1.0, eta / ta)` | — |
| `csv/_test_fork/_esperimento_tau_a.py` | `:133` | `cres = float(np.median(eta)) / 120.0` | ⚠ **median** |
| `csv/_test_fork/_esperimento_tau_a.py` | `:136` | `% (eti, np.median(eta), np.median(ramp), np.percentile(ramp, 5),` | ⚠ **median, percentile** |
| `csv/_test_fork/_maturazione.py` | `:105` | `eta = np.asarray(net.eta[:n], float)` | — |
| `csv/_test_fork/_maturazione.py` | `:105` | `eta = np.asarray(net.eta[:n], float)` | — |
| `csv/_test_fork/_maturazione.py` | `:106` | `ramp = np.minimum(1.0, eta / S.TAU_A)` | — |
| `csv/_test_fork/_perche_ramp_cala.py` | `:68` | `eta = np.asarray(net.eta, float)` | — |
| `csv/_test_fork/_perche_ramp_cala.py` | `:68` | `eta = np.asarray(net.eta, float)` | — |
| `csv/_test_fork/_perche_ramp_cala.py` | `:69` | `return eta.copy(), tr.copy(), np.minimum(1.0, eta / tr)` | — |
| `csv/_test_fork/_perche_ramp_cala.py` | `:69` | `return eta.copy(), tr.copy(), np.minimum(1.0, eta / tr)` | — |
| `csv/_test_fork/_pilota_eta.py` | `:47` | `eta = np.asarray(a["eta"], float)[:n]` | — |
| `csv/_test_fork/_pilota_eta.py` | `:84` | `e = eta[:m][sel]` | — |
| `csv/_test_fork/_pilota_eta.py` | `:96` | `ramp = np.minimum(1.0, eta[:m] / TAU_A)` | — |
| `csv/_test_fork/_pilota_eta.py` | `:104` | `e = eta[:m][sel]` | — |
| `csv/_test_fork/_pilota_eta.py` | `:132` | `% float(np.mean((eta[I2] >= TAU_A) & (eta[J2] >= TAU_A))))` | ⚠ **mean** |
| `csv/_test_fork/_pilota_eta.py` | `:132` | `% float(np.mean((eta[I2] >= TAU_A) & (eta[J2] >= TAU_A))))` | ⚠ **mean** |
| `csv/_test_fork/_pilota_scena6000.py` | `:138` | `eta = np.asarray(ultimo["at"].get("eta"), float)` | — |
| `csv/_test_fork/_pilota_scena6000.py` | `:173` | `m = min(e0.size, eta.size)` | ⚠ **min** |
| `csv/_test_fork/_pilota_scena6000.py` | `:174` | `d_eta = (eta[:m] - e0[:m]) / dpasso` | — |
| `csv/_test_fork/_rigiocata_1200_1230.py` | `:163` | `eta = np.asarray(net.eta)[:n]` | — |
| `csv/_test_fork/_rigiocata_1200_1230.py` | `:163` | `eta = np.asarray(net.eta)[:n]` | — |
| `csv/_test_fork/_rigiocata_1200_1230.py` | `:167` | `gio = idx[np.argsort(eta[idx])[:N_GIOVANI]]` | ⚠ **sort** |
| `csv/_test_fork/_rigiocata_1200_1230.py` | `:168` | `ramp = np.minimum(1.0, eta / S.TAU_A)` | — |
| `csv/_test_fork/_rigiocata_1200_1230.py` | `:169` | `sgio = " ".join("%d:%.3f\|%.1e\|%.3f" % (g, eta[g], I[g], ramp[g]) for g in gio)` | — |
| `csv/_test_fork/_rimisura_Z9.py` | `:130` | `eta = np.asarray(r.eta, float)[:n]` | — |
| `csv/_test_fork/_rimisura_Z9.py` | `:130` | `eta = np.asarray(r.eta, float)[:n]` | — |
| `csv/_test_fork/_rimisura_Z9.py` | `:131` | `ramp = np.minimum(1.0, eta / TA)` | — |
| `csv/_test_fork/_rimisura_Z9.py` | `:132` | `traj.append((k, n, float(np.median(eta)), float(np.median(ramp)),` | ⚠ **median** |
| `csv/_test_fork/_sonda_eta_ramp.py` | `:55` | `eta = np.asarray(self.eta, float)[:n]` | — |
| `csv/_test_fork/_sonda_eta_ramp.py` | `:55` | `eta = np.asarray(self.eta, float)[:n]` | — |
| `csv/_test_fork/_sonda_eta_ramp.py` | `:58` | `neo = (grado == 2) & (eta <= 0.0)          # figli della mitosi, eta ancora a ze` | — |
| `csv/_test_fork/_sonda_eta_ramp.py` | `:60` | `ramp_pre = np.minimum(1.0, eta / TA)` | — |
| `csv/_test_fork/_sonda_eta_ramp.py` | `:64` | `eta_post = eta + DT` | — |
| `csv/_test_fork/_sonda_eta_ramp.py` | `:72` | `eta_pre=float(np.max(eta[neo])),` | ⚠ **max** |
| `csv/_test_fork/_sonda_rho_zero.py` | `:61` | `eta = np.asarray(getattr(self, "eta", np.zeros(n)), float)[:n]` | — |
| `csv/_test_fork/_sonda_rho_zero.py` | `:63` | `ramp = np.minimum(1.0, eta / TA)` | — |
| `csv/_test_fork/_sonda_rho_zero.py` | `:75` | `"eta_ko_med": float(np.median(eta[ko])) if ko.any() else -1.0,` | ⚠ **median, any** |
| `csv/_test_fork/_sonda_rho_zero.py` | `:76` | `"eta_ok_med": float(np.median(eta[~ko])) if (~ko).any() else -1.0,` | ⚠ **median, any** |
| `csv/_test_fork/_tassi_coppie.py` | `:151` | `eta = passo - nb` | — |
| `csv/_test_fork/_tassi_coppie.py` | `:152` | `vivi = (eta >= 0) & (eta <= ETA_MAX)` | — |
| `csv/_test_fork/_tassi_coppie.py` | `:152` | `vivi = (eta >= 0) & (eta <= ETA_MAX)` | — |
| `csv/_test_fork/_tassi_coppie.py` | `:155` | `f = f[vivi]; p = p[vivi]; eta = eta[vivi]` | — |
| `csv/_test_fork/_tassi_coppie.py` | `:155` | `f = f[vivi]; p = p[vivi]; eta = eta[vivi]` | — |
| `csv/_test_fork/_tassi_coppie.py` | `:162` | `np.add.at(self.chi_somma, eta, chi)` | — |
| `csv/_test_fork/_tassi_coppie.py` | `:163` | `np.add.at(self.chi_n, eta, 1.0)` | — |
| `csv/_test_fork/_tassi_coppie.py` | `:164` | `np.add.at(self.dist_somma, eta, dist)` | — |
| `csv/_test_fork/_tassi_coppie.py` | `:165` | `np.add.at(self.arco_vivo, eta, vivo)` | — |
| `csv/_test_fork/_topologia.py` | `:64` | `eta = np.asarray(at["eta"], float)[:n].copy()` | — |
| `csv/_test_fork/_topologia.py` | `:66` | `return n, i, j, deg_sal, eta` | — |
| `csv/_test_fork/_topologia.py` | `:209` | `n, i, j, deg_sal, eta = carica(passo)` | — |
| `csv/_test_fork/_topologia.py` | `:257` | `del A, tri, C, cat, deg, eta, i, j` | — |
| `csv/_test_fork/_topologia_neonati.py` | `:69` | `eta = np.asarray(at["eta"], float)[:n].copy()` | — |
| `csv/_test_fork/_topologia_neonati.py` | `:71` | `return dict(n=n, deg=deg_ric, deg_sal=deg_sal, eta=eta, loop=loop, dup=dup,` | — |
| `csv/_test_fork/_topologia_neonati.py` | `:159` | `eta = dati[passo]["eta"]` | — |
| `csv/_test_fork/_topologia_neonati.py` | `:165` | `m = (eta >= ETA_BIN[k]) & (eta < ETA_BIN[k + 1])` | — |
| `csv/_test_fork/_topologia_neonati.py` | `:165` | `m = (eta >= ETA_BIN[k]) & (eta < ETA_BIN[k + 1])` | — |
| `csv/_test_fork/_tracing_omega.py` | `:212` | `amp=amp, eta=np.asarray(lav.eta[:n], float), fatt_cs=fatt_cs,` | — |
| `csv/_test_fork/_verifica_flag_accesi.py` | `:232` | `_r = _np.minimum(1.0, _np.asarray(_net.eta, float)` | — |
| `csv/_test_fork/_limite_accoppiamento/_sim_diag.py` | `:1575` | `self.phivel = np.zeros(0); self.eta = np.zeros(0)` | — |
| `csv/_test_fork/_limite_accoppiamento/_sim_diag.py` | `:2690` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_test_fork/_limite_accoppiamento/_sim_diag.py` | `:2690` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_test_fork/_limite_accoppiamento/_sim_diag.py` | `:2693` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_test_fork/_limite_accoppiamento/_sim_diag.py` | `:2693` | `self.eta = np.concatenate([self.eta, np.zeros(n)])` | — |
| `csv/_test_fork/_limite_accoppiamento/_sim_diag.py` | `:2717` | `self.eta[_a:_b] = np.asarray(_tr, float)[_a:_b]` | — |
| `csv/_test_fork/_limite_accoppiamento/_sim_diag.py` | `:2722` | `self.eta[_a:_b] = float(_tr)` | — |
| `csv/_test_fork/_limite_accoppiamento/_sim_diag.py` | `:3393` | `_tq = _tq * np.minimum(1.0, self.eta[:n] / _trq)[:, None]` | — |
| `csv/_test_fork/_limite_accoppiamento/_sim_diag.py` | `:3659` | `ramp = np.minimum(1.0, self.eta / _tr)` | — |
| `csv/_test_fork/_limite_accoppiamento/_sim_diag.py` | `:4951` | `w = self._pesi(); self.eta += dt_n` | — |
| `csv/_test_fork/_limite_accoppiamento/_sim_diag.py` | `:5983` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_test_fork/_limite_accoppiamento/_sim_diag.py` | `:5983` | `self.eta = np.concatenate([self.eta, np.zeros(len(sel))])` | — |
| `csv/_test_fork/_limite_accoppiamento/_sim_diag.py` | `:6139` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_test_fork/_limite_accoppiamento/_sim_diag.py` | `:6139` | `self.eta = np.concatenate([self.eta, np.zeros(nc)])` | — |
| `csv/_test_fork/_limite_accoppiamento/_sim_diag.py` | `:9230` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_test_fork/_limite_accoppiamento/_sim_diag.py` | `:9230` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |
| `csv/_test_fork/_limite_accoppiamento/_sim_diag.py` | `:9230` | `cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len` | — |

```
occorrenze negli strumenti           287
CON UNA RIDUZIONE sulla stessa riga  14
```

## ③ IL VERDETTO

**NEL SIMULATORE NESSUNA LETTURA DI `eta` FINISCE IN UNA RIDUZIONE**: `+inf` non ha
niente da rompere nella FISICA.

**NEGLI STRUMENTI le riduzioni sono %d**: non rompono la fisica, **rompono i REFERTI** --
una `median(eta)` che diventa `inf` stampa `inf` invece di un numero, e un referto che
stampa `inf` va **dichiarato**, non lasciato passare. *(E la stessa famiglia del `PASS`
su `inf` gia' catalogata: un verdetto vacuo.)*

## COSA QUESTO ELENCO **NON** DICE

- **la riduzione si cerca SULLA STESSA RIGA.** Un `eta` messo in una variabile e ridotto
  **tre righe dopo** NON viene visto. **E' il limite vero di questo strumento**, e si
  dichiara invece di far sembrare l'elenco completo.
- **non e' un presidio:** non impedisce a nessuno di scrivere domani una `mean(eta)`.
