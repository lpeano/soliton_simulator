# LA VERIFICA DI `B1` — **esiste una riga che distingue `φ` da `φ + 2π`?**

> Generato da `csv/_test_fork/_phi_distingue.py`. **Blob `3d91338e`.** Sola lettura.
> **Lo strumento RESTRINGE, non decide:** riporta ogni uso che **non** passa da una funzione a periodo `2π` e **non** sta dentro un avvolgimento. **La lettura e' una per una.**
>
> **⚠ Il criterio e' ASIMMETRICO di proposito:** in caso di dubbio un uso finisce fra i **candidati**. **Un falso allarme costa una lettura; un falso silenzio costa la decisione.**

**CANDIDATI: 31** — di cui **MEZZI ANGOLI: 3** e **USI GREZZI: 28**.

## MEZZI ANGOLI — **questi DISTINGUEREBBERO `φ` da `φ+2π`**

| riga | funzione | quale | perché | codice |
|--:|---|:--:|---|---|
| `5894` | `memoria_hebbiana_moto` | `phi` | MEZZO ANGOLO o coefficiente NON INTERO dentro `angle` (coeff=None) | `dphi_arc = np.angle(np.exp(1j * (self.phi[jj] - self.phi[ii])))` |
| `8587` | `_diag_completa` | `phi` | MEZZO ANGOLO o coefficiente NON INTERO dentro `angle` (coeff=None) | `fase_m = float(np.angle(np.sum(I2[idx_m] * np.exp(1j*net.phi[idx_m]))))` |
| `8868` | `_diag_completa` | `phi` | MEZZO ANGOLO o coefficiente NON INTERO dentro `angle` (coeff=None) | `fasi_nuc = [np.angle(np.mean(np.exp(1j*net.phi[info[m]['idx']]))) for m in mm]` |

## USI GREZZI — **da leggere uno per uno**

| riga | funzione | quale | perché | codice |
|--:|---|:--:|---|---|
| `1480` | `__init__` | `phi` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `self.pos = np.zeros((0, 3)); self.phi = np.zeros(0); self.phi0 = np.zeros(0)` |
| `1566` | `n` | `phi` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `def n(self): return len(self.phi)` |
| `2218` | `circolazione_topologica` | `phi` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `dph = self._w4(self.phi[self.i] - self.phi[self.j])   # 1-forma di fase, orientata i->j` |
| `2349` | `semina` | `phi` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `self.phi = np.concatenate([self.phi, ph % (4 * np.pi)])` |
| `2350` | `semina` | `phi0` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `self.phi0 = np.concatenate([self.phi0, ph % (4 * np.pi)])` |
| `4295` | `step` | `_phi_t` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `_phi_t = self.phi.copy()` |
| `4625` | `step` | `phi` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `self.phi = (_phi_t + (dt_n_s * self.phivel) + delta_sync_phi) % (4 * np.pi)  # dt_n_s = verso f` |
| `4628` | `step` | `_phi_t` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `dph = self._w4(_phi_t[i] - _phi_t[j])` |
| `5273` | `mitosi` | `phi` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `D = self._w4(self.phi[a] - self.phi[b])` |
| `5289` | `mitosi` | `fm` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `fm = (self.phi[a] - (0.5 + bias) * D) % (4 * np.pi)` |
| `5291` | `mitosi` | `fm` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `fm = (self.phi[a] - 0.5 * D) % (4 * np.pi)` |
| `5311` | `mitosi` | `fm` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `fm = np.where(flip, (fm + 2 * np.pi) % (4 * np.pi), fm)  # +2pi in copertura 4pi = antifase` |
| `5314` | `mitosi` | `phi` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `self.phi = np.concatenate([self.phi, fm]); self.phi0 = np.concatenate([self.phi0, fm])` |
| `5353` | `mitosi` | `phi` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `self.phi[a] = (self.phi[a] + calcio_a) % (4 * np.pi)` |
| `5354` | `mitosi` | `phi` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `self.phi[b] = (self.phi[b] + calcio_b) % (4 * np.pi)` |
| `5357` | `mitosi` | `phi` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `self.phi[g] = (self.phi[g] + self.rng.normal(0, 1, len(g)) *` |
| `5403` | `mitosi` | `fm` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `self.twp = np.concatenate([self.twp[keep], self._w4(self.phi[a] - fm),` |
| `5404` | `mitosi` | `fm` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `self._w4(fm - self.phi[b])])` |
| `5443` | `mitosi` | `anti` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `anti = (fm[pick] + 2 * np.pi) % (4 * np.pi)` |
| `5458` | `mitosi` | `phi` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `self.phi = np.concatenate([self.phi, anti])` |
| `5459` | `mitosi` | `phi0` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `self.phi0 = np.concatenate([self.phi0, anti])` |
| `5508` | `mitosi` | `anti` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `self.twp = np.concatenate([self.twp, self._w4(self.phi[aa] - anti),` |
| `5509` | `mitosi` | `anti` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `self._w4(anti - self.phi[bb])])` |
| `6105` | `memoria_hebbiana_moto` | `phi` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `self.phi[ii] = (self.phi[ii] + shift_fase_dinamico) % (4 * np.pi)` |
| `8345` | `_diag_completa` | `phi` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `cols['phi_min'], cols['phi_max'], cols['phi_mean'], _ = _stat(net.phi[:n])` |
| `8890` | `_diag_completa` | `phi` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `phg = net.phi[:net.n][anello]` |
| `8928` | `_ordine` | `phi` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `n = net.n; P = net.pos[:n]; phi = net.phi[:n]` |
| `8953` | `_gusci_esterni` | `phi` | USO GREZZO: non passa da nessuna funzione a periodo `2pi` e non e' dentro un avvolgimento | `tree = cKDTree(P); phi = net.phi[:n]` |

