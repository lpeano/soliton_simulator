# 📒 **IL REGISTRO DELLE GRANDEZZE: per nodo, per arco, e la regola di nascita**

> ### **Generato da** `csv/_test_fork/_registro_grandezze.py`. **Non si modifica a mano:**
> si rigira lo strumento. *(`L-NUMERI`.)* ### **Le regole di nascita qui sono PROPOSTE dal
> codice, non decise:** l'espressione e' sempre riportata, e cio' che non e' evidente resta
> **DA DECIDERE**.

| | |
|---|---|
| scena | `nmasse 3`, `sep 6.1158` → **`n = 12802`**, **archi `m = 471564`**, dopo **30** passi |
| riferimento di `n` | ``phi`` — ### **`n` E' `len(phi)`** *(property `:2063`)*: non e' un membro del registro, e' il **metro** |
| riferimento di `m` | `i`, `j` — `len(i) = 471564`, `len(j) = 471564`, ### **e coincidono** |
| ### **per NODO** | ### **32** |
| ### **per ARCO** | ### **11** |
| ambigue *(`n == m`, indistinguibili)* | ### **NESSUNA** — `n = 12802` e `m = 471564` |

## Le grandezze **PER NODO** (`len == n`)

| grandezza | forma | tipo | scr. | ### **SEMINA** | ### **MITOSI** *(+Schwinger)* | ### **`_allaccia`** | senza regola di nascita |
|---|---|---|---|---|---|---|---|
| `_chi_core_nodi` | `12802` | `float64` | 1 | — | — | — | ### ⚠ **NESSUNA REGOLA DI NASCITA**: o e' **DERIVATA** *(ricalcolata a piena lunghezza ogni passo)*, o e' un **BUCO**. ### **DA DECIDERE, e si legge A MANO** *(scritture: `:2558` `chiralita_core_locale`)* |
| `_chi_core_raggio` | `12802` | `float64` | 1 | — | — | — | ### ⚠ **NESSUNA REGOLA DI NASCITA**: o e' **DERIVATA** *(ricalcolata a piena lunghezza ogni passo)*, o e' un **BUCO**. ### **DA DECIDERE, e si legge A MANO** *(scritture: `:2561` `chiralita_core_locale`)* |
| `_chi_core_rho0` | `12802` | `float64` | 1 | — | — | — | ### ⚠ **NESSUNA REGOLA DI NASCITA**: o e' **DERIVATA** *(ricalcolata a piena lunghezza ogni passo)*, o e' un **BUCO**. ### **DA DECIDERE, e si legge A MANO** *(scritture: `:2559` `chiralita_core_locale`)* |
| `_chi_geom_nodi` | `12802` | `float64` | 1 | — | — | — | ### ⚠ **NESSUNA REGOLA DI NASCITA**: o e' **DERIVATA** *(ricalcolata a piena lunghezza ogni passo)*, o e' un **BUCO**. ### **DA DECIDERE, e si legge A MANO** *(scritture: `:2556` `chiralita_core_locale`)* |
| `_cs_nodo_prev` | `12802` | `float64` | 3 | — | eredita <br> *`:2349`* | — |  |
| `_deg` | `12802` | `int64` | 2 | — | — | — | ### ⚠ **NESSUNA REGOLA DI NASCITA**: o e' **DERIVATA** *(ricalcolata a piena lunghezza ogni passo)*, o e' un **BUCO**. ### **DA DECIDERE, e si legge A MANO** *(scritture: `:2046` `__init__`, `:2066` `_grado`)* |
| `_fatt_cs_ultimo` | `12802` | `float64` | 1 | — | — | — | ### ⚠ **NESSUNA REGOLA DI NASCITA**: o e' **DERIVATA** *(ricalcolata a piena lunghezza ogni passo)*, o e' un **BUCO**. ### **DA DECIDERE, e si legge A MANO** *(scritture: `:3757` `_passo_spinoriale`)* |
| `_g_rampa_prec` | `12802` | `float64` | 1 | — | — | — | ### ⚠ **NESSUNA REGOLA DI NASCITA**: o e' **DERIVATA** *(ricalcolata a piena lunghezza ogni passo)*, o e' un **BUCO**. ### **DA DECIDERE, e si legge A MANO** *(scritture: `:4308` `_pesi`)* |
| `_nb` | `12802×3` | `float64` | 9 | — | eredita <br> *`:2353`* | — |  |
| `_nb_prec` | `12802×3` | `float64` | 2 | — | eredita <br> *`:2355`* | — |  |
| `_nb_ret` | `12802×3` | `float64` | 4 | — | eredita <br> *`:2361`* | — |  |
| `_psi_prec` | `12802` | `complex128` | 4 | — | eredita <br> *`:2375`* | — |  |
| `_psi_spin_prec` | `12802×2` | `complex128` | 2 | — | eredita <br> *`:2387`* | — |  |
| `_psi_spinor` | `12802×2` | `complex128` | 6 | — | ### **DA DECIDERE** <br> *`:2368`* | — |  |
| `_r_corrente` | `12802` | `float64` | 2 | — | — | — | ### ⚠ **NESSUNA REGOLA DI NASCITA**: o e' **DERIVATA** *(ricalcolata a piena lunghezza ogni passo)*, o e' un **BUCO**. ### **DA DECIDERE, e si legge A MANO** *(scritture: `:2010` `__init__`, `:5577` `step`)* |
| `_spinor_lift` | `12802×2` | `complex128` | 4 | — | ### **DA DECIDERE** <br> *`:2373`* | — |  |
| `_xi_rumore` | `12802×3` | `float64` | 1 | — | — | — | ### ⚠ **NESSUNA REGOLA DI NASCITA**: o e' **DERIVATA** *(ricalcolata a piena lunghezza ogni passo)*, o e' un **BUCO**. ### **DA DECIDERE, e si legge A MANO** *(scritture: `:3642` `_passo_spinoriale`)* |
| `conc_nodi` | `12802×0` | `float64` | 1 | — | — | — | ### ⚠ **NESSUNA REGOLA DI NASCITA**: o e' **DERIVATA** *(ricalcolata a piena lunghezza ogni passo)*, o e' un **BUCO**. ### **DA DECIDERE, e si legge A MANO** *(scritture: `:2058` `__init__`)* |
| `eta` | `12802` | `float64` | 6 | zero / costante <br> *`:3177`, `:3180`* | zero / costante <br> *`:6644`, `:6807`* | — |  |
| `mem_mot` | `12802×3` | `float64` | 5 | zero / costante <br> *`:3187`* | zero / costante <br> *`:6659`, `:6821`* | — |  |
| `omega_s` | `12802×3` | `float64` | 6 | ### **DA DECIDERE** <br> *`:3192`* | eredita <br> *`:2363`* | — |  |
| `perc_chi` | `12802` | `int64` | 4 | ### **DA DECIDERE** <br> *`:3182`* | eredita <br> *`:6647`, `:6810`* | — |  |
| `perc_geom` | `12802` | `int64` | 4 | ### **DA DECIDERE** <br> *`:3185`* | eredita <br> *`:6650`, `:6814`* | — |  |
| `perc_tw` | `12802` | `float64` | 4 | zero / costante <br> *`:3186`* | zero / costante <br> *`:6658`, `:6820`* | — |  |
| `phi` | `12802` | `float64` | 5 | ### **DA DECIDERE** <br> *`:3139`* | ### **DA DECIDERE** <br> *`:6641`, `:6803`* | — |  |
| `phi0` | `12802` | `float64` | 4 | ### **DA DECIDERE** <br> *`:3140`* | ### **DA DECIDERE** <br> *`:6641`, `:6804`* | — |  |
| `phi_s` | `12802` | `float64` | 5 | zero / costante <br> *`:3141`* | ### ⚠ **INCOERENTE NELLO STESSO EVENTO: eredita / zero / costante** <br> *`:6642`, `:6805`* | — |  |
| `phivel` | `12802` | `float64` | 6 | ### ⚠ **INCOERENTE NELLO STESSO EVENTO: ### **DA DECIDERE** / zero / costante** <br> *`:3155`, `:3157`* | media <br> *`:6643`, `:6806`* | — |  |
| `pos` | `12802×3` | `float64` | 7 | ### **DA DECIDERE** <br> *`:3138`* | ### ⚠ **INCOERENTE NELLO STESSO EVENTO: ### **DA DECIDERE** / media** <br> *`:6640`, `:6802`* | — |  |
| `psi` | `12802` | `complex128` | 5 | — | media <br> *`:2306`* | — |  |
| `psi_spin` | `12802×2` | `complex128` | 2 | — | eredita <br> *`:2312`* | — |  |
| `rho_spin` | `12802` | `float64` | 2 | — | eredita <br> *`:2322`* | — |  |

## Le grandezze **PER ARCO** (`len == m`)

| grandezza | forma | tipo | scr. | ### **SEMINA** | ### **MITOSI** *(+Schwinger)* | ### **`_allaccia`** | senza regola di nascita |
|---|---|---|---|---|---|---|---|
| `_dt_e_ultimo` | `471564` | `float64` | 1 | — | — | — | ### ⚠ **NESSUNA REGOLA DI NASCITA**: o e' **DERIVATA** *(ricalcolata a piena lunghezza ogni passo)*, o e' un **BUCO**. ### **DA DECIDERE, e si legge A MANO** *(scritture: `:5570` `step`)* |
| `_rep` | `471564` | `float64` | 6 | — | ### ⚠ **INCOERENTE NELLO STESSO EVENTO: eredita / zero / costante** <br> *`:6733`, `:6854`* | zero / costante <br> *`:3365`* |  |
| `_sin2_vir` | `471564` | `float64` | 2 | — | — | — | ### ⚠ **NESSUNA REGOLA DI NASCITA**: o e' **DERIVATA** *(ricalcolata a piena lunghezza ogni passo)*, o e' un **BUCO**. ### **DA DECIDERE, e si legge A MANO** *(scritture: `:2035` `__init__`, `:7176` `memoria_hebbiana_moto`)* |
| `d` | `471564` | `float64` | 8 | — | ### **DA DECIDERE** <br> *`:6723`, `:6842`* | ### **DA DECIDERE** <br> *`:3361`* |  |
| `d0` | `471564` | `float64` | 9 | — | ### **DA DECIDERE** <br> *`:6726`, `:6845`* | ### **DA DECIDERE** <br> *`:3361`* |  |
| `i` | `471564` | `int64` | 4 | — | ### **DA DECIDERE** <br> *`:6710`, `:6840`* | ### **DA DECIDERE** <br> *`:3356`* |  |
| `j` | `471564` | `int64` | 4 | — | ### **DA DECIDERE** <br> *`:6711`, `:6841`* | ### **DA DECIDERE** <br> *`:3356`* |  |
| `peq` | `471564` | `float64` | 8 | — | ### ⚠ **INCOERENTE NELLO STESSO EVENTO: eredita / zero / costante** <br> *`:6729`, `:6848`* | zero / costante <br> *`:3364`* |  |
| `tw` | `471564` | `float64` | 6 | — | ### **DA DECIDERE** <br> *`:6735`, `:6856`* | zero / costante <br> *`:3366`* |  |
| `twp` | `471564` | `float64` | 6 | — | eredita <br> *`:6736`, `:6857`* | zero / costante <br> *`:3367`* |  |
| `vd` | `471564` | `float64` | 6 | — | ### ⚠ **INCOERENTE NELLO STESSO EVENTO: eredita / zero / costante** <br> *`:6728`, `:6847`* | zero / costante <br> *`:3363`* |  |

## ⚖ Il riepilogo, CONTATO dallo strumento

| | con una REGOLA DI NASCITA | ### **senza** | di cui **DA DECIDERE** | di cui ### **INCOERENTI** |
|---|---|---|---|---|
| **PER NODO** | **22** | ### **10** | **9** | ### **3** |
| **PER ARCO** | **9** | ### **2** | **5** | ### **3** |

**PER NODO — senza regola di nascita (10):** `_chi_core_nodi`, `_chi_core_raggio`, `_chi_core_rho0`, `_chi_geom_nodi`, `_deg`, `_fatt_cs_ultimo`, `_g_rampa_prec`, `_r_corrente`, `_xi_rumore`, `conc_nodi`

**PER NODO — DA DECIDERE (9):** `_psi_spinor`, `_spinor_lift`, `omega_s`, `perc_chi`, `perc_geom`, `phi`, `phi0`, `phivel`, `pos`

**PER NODO — INCOERENTI nello stesso evento (3):** `phi_s`, `phivel`, `pos`

**PER ARCO — senza regola di nascita (2):** `_dt_e_ultimo`, `_sin2_vir`

**PER ARCO — DA DECIDERE (5):** `d`, `d0`, `i`, `j`, `tw`

**PER ARCO — INCOERENTI nello stesso evento (3):** `_rep`, `peq`, `vd`

## Le espressioni, per chi verifica

**Ogni scrittura in un sito di nascita, con l'espressione INTERA.**
### **Senza questa tabella la colonna «regola PROPOSTA» sarebbe una cosa da CREDERE.**

| grandezza | riga | funzione | catena dalla nascita | allunga? | espressione |
|---|---|---|---|---|---|
| `_cs_nodo_prev` | `:2349` | `_eredita_spinore_figli` | mitosi -> _eredita_spinore_figli | ### **SI** | `np.concatenate([_csp_er, np.asarray(_csp_er, float)[src]])` |
| `_deg` | `:2066` | `_grado` | mitosi -> _grado | no | `np.maximum(np.bincount(self.i, minlength=self.n) + np.bincount(self.j, minlength=self.n), 1)` |
| `_g_rampa_prec` | `:4308` | `_pesi` | semina -> _registra_concorrenza -> calcola_psi -> _pesi | no | `np.array(ramp, dtype=float, copy=True)` |
| `_nb` | `:2353` | `_eredita_spinore_figli` | mitosi -> _eredita_spinore_figli | ### **SI** | `np.vstack([self._nb, self._nb[src]])` |
| `_nb_prec` | `:2355` | `_eredita_spinore_figli` | mitosi -> _eredita_spinore_figli | ### **SI** | `np.vstack([self._nb_prec, self._nb_prec[src]])` |
| `_nb_ret` | `:2361` | `_eredita_spinore_figli` | mitosi -> _eredita_spinore_figli | ### **SI** | `np.vstack([_nbr_er, _nbr_er[src]])` |
| `_psi_prec` | `:2375` | `_eredita_spinore_figli` | mitosi -> _eredita_spinore_figli | ### **SI** | `np.concatenate([self._psi_prec, self._psi_prec[src]])` |
| `_psi_spin_prec` | `:2387` | `_eredita_spinore_figli` | mitosi -> _eredita_spinore_figli | ### **SI** | `np.vstack([_pspr, np.asarray(_pspr)[src]])` |
| `_psi_spinor` | `:2368` | `_eredita_spinore_figli` | mitosi -> _eredita_spinore_figli | ### **SI** | `np.vstack([self._psi_spinor, er])` |
| `_spinor_lift` | `:2373` | `_eredita_spinore_figli` | mitosi -> _eredita_spinore_figli | ### **SI** | `np.vstack([self._spinor_lift, el])` |
| `eta` | `:3177` | `semina` | *(radice)* | ### **SI** | `np.concatenate([self.eta, np.zeros(n)])` |
| `eta` | `:3180` | `semina` | *(radice)* | ### **SI** | `np.concatenate([self.eta, np.zeros(n)])` |
| `eta` | `:6644` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.eta, np.zeros(len(sel))])` |
| `eta` | `:6807` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.eta, np.zeros(nc)])` |
| `mem_mot` | `:3187` | `semina` | *(radice)* | ### **SI** | `np.vstack([self.mem_mot, np.zeros((n, 3))]) if len(self.mem_mot) else np.zeros((n, 3))` |
| `mem_mot` | `:6659` | `mitosi` | *(radice)* | ### **SI** | `np.vstack([self.mem_mot, self.mem_mot[a]]) if len(self.mem_mot) else np.zeros((len(sel), 3))` |
| `mem_mot` | `:6821` | `mitosi` | *(radice)* | ### **SI** | `np.vstack([self.mem_mot, np.zeros((nc, 3))]) if len(self.mem_mot) else np.zeros((nc, 3))` |
| `omega_s` | `:2363` | `_eredita_spinore_figli` | mitosi -> _eredita_spinore_figli | ### **SI** | `np.vstack([self.omega_s, self.omega_s[src]])` |
| `omega_s` | `:3192` | `semina` | *(radice)* | ### **SI** | `np.vstack([self.omega_s, calcio_omega]) if len(self.omega_s) else calcio_omega` |
| `perc_chi` | `:3182` | `semina` | *(radice)* | ### **SI** | `np.concatenate([self.perc_chi, chi_nuovi])` |
| `perc_chi` | `:6647` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.perc_chi, self.perc_chi[a]])` |
| `perc_chi` | `:6810` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.perc_chi, -self.perc_chi[aa]])` |
| `perc_geom` | `:3185` | `semina` | *(radice)* | ### **SI** | `np.concatenate([self.perc_geom, chi_nuovi])` |
| `perc_geom` | `:6650` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.perc_geom, self.perc_geom[a]])` |
| `perc_geom` | `:6814` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.perc_geom, self.perc_geom[aa]])` |
| `perc_tw` | `:3186` | `semina` | *(radice)* | ### **SI** | `np.concatenate([self.perc_tw, np.zeros(n)])` |
| `perc_tw` | `:6658` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.perc_tw, np.zeros(len(sel))])` |
| `perc_tw` | `:6820` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.perc_tw, np.zeros(nc)])` |
| `phi` | `:3139` | `semina` | *(radice)* | ### **SI** | `np.concatenate([self.phi, ph % self._dphi()])` |
| `phi` | `:6641` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.phi, fm])` |
| `phi` | `:6803` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.phi, anti])` |
| `phi0` | `:3140` | `semina` | *(radice)* | ### **SI** | `np.concatenate([self.phi0, ph % self._dphi()])` |
| `phi0` | `:6641` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.phi0, fm])` |
| `phi0` | `:6804` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.phi0, anti])` |
| `phi_s` | `:3141` | `semina` | *(radice)* | ### **SI** | `np.concatenate([self.phi_s, np.zeros(n)])` |
| `phi_s` | `:6642` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.phi_s, self.phi_s[a]])` |
| `phi_s` | `:6805` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.phi_s, np.zeros(nc)])` |
| `phivel` | `:3155` | `semina` | *(radice)* | ### **SI** | `np.concatenate([self.phivel, calcio_phi])` |
| `phivel` | `:3157` | `semina` | *(radice)* | ### **SI** | `np.concatenate([self.phivel, np.zeros(n)])` |
| `phivel` | `:6643` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.phivel, 0.5 * (self.phivel[a] + self.phivel[b])])` |
| `phivel` | `:6806` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.phivel, 0.5 * (self.phivel[aa] + self.phivel[bb])])` |
| `pos` | `:3138` | `semina` | *(radice)* | ### **SI** | `np.vstack([self.pos, p])` |
| `pos` | `:6640` | `mitosi` | *(radice)* | ### **SI** | `np.vstack([self.pos, pos_figlio])` |
| `pos` | `:6802` | `mitosi` | *(radice)* | ### **SI** | `np.vstack([self.pos, 0.5 * (self.pos[aa] + self.pos[bb])])` |
| `psi` | `:2306` | `_eredita_psi_figli` | mitosi -> _eredita_psi_figli | ### **SI** | `np.concatenate([cur[:n0], 0.5 * (cur[a] + cur[b])])` |
| `psi` | `:4400` | `calcola_psi` | semina -> _registra_concorrenza -> calcola_psi | no | `np.zeros(self.n, complex)` |
| `psi` | `:4407` | `calcola_psi` | semina -> _registra_concorrenza -> calcola_psi | no | `self.satura(F)` |
| `psi_spin` | `:2312` | `_eredita_psi_figli` | mitosi -> _eredita_psi_figli | ### **SI** | `np.concatenate([cs[:n0], cs[a]])` |
| `psi_spin` | `:4421` | `calcola_psi` | semina -> _registra_concorrenza -> calcola_psi | no | `_Fs / (1.0 + GAMMA * _norm)[:, None]` |
| `rho_spin` | `:2322` | `_eredita_psi_figli` | mitosi -> _eredita_psi_figli | ### **SI** | `np.concatenate([np.asarray(rs)[:n0], np.asarray(rs)[a]])` |
| `rho_spin` | `:4422` | `calcola_psi` | semina -> _registra_concorrenza -> calcola_psi | no | `np.real(np.sum(np.conj(self.psi_spin) * self.psi_spin, axis=1))` |
| `_rep` | `:3365` | `_allaccia` | *(radice)* | ### **SI** | `np.concatenate([self._rep, np.zeros(len(dd))])` |
| `_rep` | `:6516` | `mitosi` | *(radice)* | no | `np.zeros(len(rep))` |
| `_rep` | `:6542` | `mitosi` | *(radice)* | no | `rep + (self._rep - rep) * np.exp(-_rap)` |
| `_rep` | `:6733` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self._rep[keep], self._rep[sel], self._rep[sel]])` |
| `_rep` | `:6854` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self._rep, np.zeros(2 * nc)])` |
| `d` | `:3361` | `_allaccia` | *(radice)* | ### **SI** | `np.concatenate([self.d, dd])` |
| `d` | `:6723` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.d[keep], dh, dh])` |
| `d` | `:6842` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.d, dd, dd])` |
| `d0` | `:3361` | `_allaccia` | *(radice)* | ### **SI** | `np.concatenate([self.d0, dd])` |
| `d0` | `:6570` | `mitosi` | *(radice)* | no | `self.d0 + self._sd0(spinta)` |
| `d0` | `:6726` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.d0[keep], d0new])` |
| `d0` | `:6845` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.d0, dd, dd])` |
| `i` | `:3356` | `_allaccia` | *(radice)* | ### **SI** | `np.concatenate([self.i, a])` |
| `i` | `:6710` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.i[keep], a, m])` |
| `i` | `:6840` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.i, aa, k])` |
| `j` | `:3356` | `_allaccia` | *(radice)* | ### **SI** | `np.concatenate([self.j, b])` |
| `j` | `:6711` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.j[keep], m, b])` |
| `j` | `:6841` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.j, k, bb])` |
| `peq` | `:3364` | `_allaccia` | *(radice)* | ### **SI** | `np.concatenate([self.peq, np.full(len(dd), np.nan)])` |
| `peq` | `:6729` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.peq[keep], self.peq[sel], self.peq[sel]])` |
| `peq` | `:6848` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.peq, np.full(2 * nc, pmed)])` |
| `tw` | `:3366` | `_allaccia` | *(radice)* | ### **SI** | `np.concatenate([self.tw, np.zeros(len(dd))])` |
| `tw` | `:6735` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.tw[keep], zz, zz])` |
| `tw` | `:6856` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.tw, zz2, zz2])` |
| `twp` | `:3367` | `_allaccia` | *(radice)* | ### **SI** | `np.concatenate([self.twp, np.zeros(len(dd))])` |
| `twp` | `:6736` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.twp[keep], self._wphi(self.phi[a] - fm), self._wphi(fm - self.phi[b])])` |
| `twp` | `:6857` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.twp, self._wphi(self.phi[aa] - anti), self._wphi(anti - self.phi[bb])])` |
| `vd` | `:3363` | `_allaccia` | *(radice)* | ### **SI** | `np.concatenate([self.vd, np.zeros(len(dd))])` |
| `vd` | `:6728` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.vd[keep], self.vd[sel], self.vd[sel]])` |
| `vd` | `:6847` | `mitosi` | *(radice)* | ### **SI** | `np.concatenate([self.vd, np.zeros(2 * nc)])` |

## ⚠ Che cosa questo registro NON dice

| | |
|---|---|
| **la proposta non e' la regola** | ### **dove c'e' «DA DECIDERE» decide Luca**, e dove
  c'e' «INCOERENTE» ce ne sono **due** per la stessa grandezza: per `9-ter` **una delle due
  e' un difetto, non una seconda legge** |
| **le scritture FUORI dai siti di nascita** non sono guardate qui | una grandezza puo'
  essere allungata da una funzione **di servizio** *(e' il caso di `_estendi_psi_spinor`)*:
  ### **quello e' proprio l'estensore che DISARMA le guardie a valle**, misurato in
  `f173050` |
| **il secondo asse** | il controllo `len == n` guarda **il primo asse**. Le forme a due
  assi sono in tabella, ### **e un presidio su un solo asse va dichiarato** |

