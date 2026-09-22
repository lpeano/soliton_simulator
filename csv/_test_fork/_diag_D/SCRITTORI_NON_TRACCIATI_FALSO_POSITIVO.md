# GLI SCRITTORI DI `d0` **NON TRACCIATI**

> Punto 4 del mandato dei sospesi. Generato da `csv/_test_fork/_scrittori_non_tracciati.py`.
> **Blob simulatore ORA: `21e3a3dc`.** ⚠ Le `22` dell'inventario della `FASE A` vengono da
> `ab685eac`: **le righe sono SPOSTATE**, il flag di `G4-bis` ha aggiunto testo a `:906`
> *(par.0: si cerca per NOME, non per riga)*.

COLLAUDO DEL CRITERIO su sorgenti SINTETICI a risposta nota (`P1-sexies`)
------------------------------------------------------------------------------------------------
K1 scrittura SEGUITA da `_traccia_d0` nella stessa funzione -> TRACCIATA -> OK
K2 IL CASO CHE DEVE FALLIRE: una scrittura in un'ALTRA funzione, con un `_traccia_d0`
     piu' avanti nel file -> deve risultare NON TRACCIATA -> OK: la funzione discrimina
K3 SECONDO CASO CHE DEVE FALLIRE: DUE scritture e UN solo `_traccia_d0` -> la PRIMA
     non e' coperta -> OK: una traccia copre UNA scrittura
------------------------------------------------------------------------------------------------
  -> i criteri PASSANO

**SCRITTURE SU `self.d0`: 22** · **SITI DI TRACCIA: 19**

| riga | funzione | tipo | sito di traccia | codice |
|--:|---|---|---|---|
| `1514` | `__init__` | diretto | **— NESSUNO** | `self.d = np.zeros(0); self.d0 = np.zeros(0); self.vd = np.zeros(0)` |
| `2495` | `_allaccia` | CONCATENA | `S01_archi_nuovi` | `self.d = np.concatenate([self.d, dd]); self.d0 = np.concatenate([self.d0, dd])` |
| `3719` | `_smp_chiudi` | diretto | **— NESSUNO** | `self.d0 = v + self._smorza(v, dx, 'd0_passo')` |
| `5040` | `step` | aumentato | `S02_rilass_visco` | `self.d0 += self._sd0(dt_e * (self.d - self.d0) / tau_p_loc)` |
| `5051` | `step` | aumentato | `S03_diff_guscio` | `self.d0 += self._sd0(np.clip(dt_e * cs_taup * d_arco * _lap_d0, -_cfl, _cfl))` |
| `5055` | `step` | aumentato | `S04_rilass_TAU_P` | `self.d0 += self._sd0(dt_e * (self.d - self.d0) / TAU_P)` |
| `5059` | `step` | diretto | `P1_dopo_rilass` | `self.d0 = self._pav_d0(self.d0)` |
| `5235` | `mitosi` | diretto | `S05_spinta_locale` | `self.d0 = self.d0 + self._sd0(spinta)          # Locale pura` |
| `5238` | `mitosi` | diretto | `P2_dopo_spinta` | `self.d0 = self._pav_d0(self.d0)       # PAVIMENTO: la spinta non deve` |
| `5370` | `mitosi` | CONCATENA | `S06_mitosi` | `self.d0 = np.concatenate([self.d0[keep], d0new])` |
| `5473` | `mitosi` | CONCATENA | `S07_schwinger` | `self.d0 = np.concatenate([self.d0, dd, dd])` |
| `5703` | `memoria_hebbiana_moto` | aumentato per indice | `S08_proj` | `self.d0[mask] += self._sd0(proj, mask)` |
| `5706` | `memoria_hebbiana_moto` | diretto | `P3_dopo_proj` | `self.d0 = self._pav_d0(self.d0)          # PAVIMENTO` |
| `5850` | `memoria_hebbiana_moto` | aumentato per indice | `S09_spinta_med` | `self.d0[mask] += self._sd0(spinta * float(np.median(self.d0[mask])), mask)` |
| `5856` | `memoria_hebbiana_moto` | aumentato per indice | `S10_grav_med` | `self.d0[mask] += self._sd0(grav * float(np.median(self.d0[mask])), mask)` |
| `5859` | `memoria_hebbiana_moto` | diretto | `P4_dopo_grav` | `self.d0 = self._pav_d0(self.d0)` |
| `5879` | `memoria_hebbiana_moto` | aumentato per indice | `S11_flusso` | `self.d0[mask] += self._sd0(flusso, mask)` |
| `5882` | `memoria_hebbiana_moto` | diretto | `P5_dopo_flusso` | `self.d0 = self._pav_d0(self.d0)` |
| `6030` | `memoria_hebbiana_moto` | aumentato per indice | **— NESSUNO** | `self.d0[mask] += self._sd0(_delta_coes, mask)` |
| `6032` | `memoria_hebbiana_moto` | aumentato per indice | `S12_coesione` | `self.d0[mask] += self._sd0(` |
| `6036` | `memoria_hebbiana_moto` | diretto | `P6_dopo_coesione` | `self.d0 = self._pav_d0(self.d0)` |
| `6084` | `memoria_hebbiana_moto` | diretto | `P7_dopo_4917` | `self.d0 = self._pav_d0(self.d0)` |

## ⚠ LE NON TRACCIATE: **3 su 22**

| riga | funzione | tipo | termine del bilancio di `G4` | come ci arriva |
|--:|---|---|---|---|
| `1514` | `__init__` | diretto | — | **NON e' una scrittura di PASSO:** e' l'inizializzazione. Il bilancio misura `Δ` **fra inizio e fine di un passo**, e qui non c'e' nessun passo. **Fuori perimetro, non scoperta.** |
| `3719` | `_smp_chiudi` | diretto | **FRENO** | **`D04`.** L'involucro di `_g4_prova.py` avvolge **`_smorza`** e somma **solo** le chiamate con `quale == 'd0_passo'`. **E' il termine che in `Z107` mancava** e che vale il `117 %`–`218 %` della crescita. |
| `6030` | `memoria_hebbiana_moto` | aumentato per indice | **❓ NON SO** | **Nessuna lettura scritta per questo sito: va guardato.** |

## L'ESITO

**⚠ 1 scritture NON tracciate e SENZA una lettura che dica dove il bilancio le prende:** [(6030, 'memoria_hebbiana_moto', 'aumentato per indice')]

**⚠ MA «IL BILANCIO LE COPRE» NON SIGNIFICA «IL SIMULATORE LE TRACCIA».** Il bilancio e' **uno strumento esterno** che avvolge `_smorza` e i siti che concatenano. **Nel simulatore i siti mancano ancora**, ed e' il difetto `D04`: chiunque rifaccia la traccia senza quell'involucro **ritrova il buco di `Z107`**.
