# `RAMPA-2` — CHI USA IL TEMPO-LUCE O `cs` QUANDO LA CACHE NON C'E' ANCORA

*(`csv/_chi_usa_il_tempo_luce.py`, per **AST**. Mandato di Luca, 2026-09-25. Sola lettura.)*

> ### IL FATTO, misurato su `RAMPA-1`
> Al **passo 0** `_cs_nodo_prev` **non esiste**: il tempo-luce si calcola con **`cs = CS_M`**
> ovunque. Al passo 1 il `cs` vero e' **`p50 1.672`** contro **`CS_M = 2`**
> (`cs_std/cs = 19.07 %`): **il tempo-luce del passo 0 e' sbagliato del ~20 %, in modo
> SISTEMATICO e nella STESSA DIREZIONE per tutti.** Non e' rumore: e' un **bias**.
>
> **`RAMPA-1` ha curato UNA delle leggi che leggono lì** (la maturita' della cura 4, che ora
> non legge piu' niente: `eta = +inf`). **Le altre sono qui sotto.**

## L'ELENCO — 40 occorrenze nel simulatore

| dove (funzione) | riga | cosa | codice |
|---|---|---|---|
| `_passo_spinoriale` | `:3121` | legge CS_M | `_tauc = LAM / max(CS_M, 1e-12)` |
| `_passo_spinoriale` | `:3265` | legge CS_M | `_cs_in = np.full(n, CS_M)` |
| `_passo_spinoriale` | `:3270` | legge CS_M | `_fatt_cs = (CS_M / _cs_in) ** 2                    # adimensionale, == 1 dove cs == CS_M` |
| `_passo_spinoriale` | `:3300` | chiamata a _tempo_luce_nodo | `_T = self._tempo_luce_nodo(i, j)                   # d_nodo/cs_nodo, UNICO punto della l` |
| `_passo_spinoriale` | `:3435` | chiamata a _tempo_rampa | `_trq = self._tempo_rampa()` |
| `_passo_spinoriale` | `:3451` | chiamata a _tempo_luce_nodo | `_tau = self._tempo_luce_nodo(i, j)[:, None]` |
| `_passo_spinoriale` | `:3555` | legge CS_M | `_csn2 = np.full(n, CS_M)` |
| `_passo_spinoriale` | `:3556` | legge CS_M | `omega_clk = omega_clk * (_csn2 / CS_M) ** 2` |
| `_tempo_rampa` | `:3689` | chiamata a _tempo_luce_nodo | `tl = np.asarray(self._tempo_luce_nodo(self.i, self.j), float)` |
| `_pesi` | `:3701` | chiamata a _tempo_rampa | `_tr = self._tempo_rampa()` |
| `_cs_nodo` | `:4623` | legge CS_M | `cs_floor = CS_M / (1.0 + np.sqrt(_I) * np.sqrt(1.0 / _scala))` |
| `_cs_nodo` | `:4624` | legge CS_M | `cs_floor = np.minimum(cs_floor, CS_M)` |
| `_cs_nodo` | `:4626` | legge CS_M | `return cs_floor + (CS_M - cs_floor) * transizione` |
| `_bloch_ritardato` | `:4665` | chiamata a _tempo_luce_nodo | `tau = self._tempo_luce_nodo(ii, jj)` |
| `_tau_arco_causale` | `:4781` | legge CS_M | `cs_arco = np.full(n_archi, CS_M, dtype=float)   # la convenzione di `:4795`` |
| `_tau_arco_causale` | `:4783` | chiamata a _cs_arco_da_nodo | `cs_arco = self._cs_arco_da_nodo(np.asarray(csn, dtype=float), self.i, self.j)` |
| `_tempo_luce_nodo` | `:4855` | legge CS_M | `cs_nodo = np.full(n, CS_M)` |
| `step` | `:5158` | legge CS_M | `if _psi_ct is not None else CS_M)` |
| `step` | `:5160` | legge CS_M | `cs_rappr = CS_M` |
| `step` | `:5353` | chiamata a _cs_arco_da_nodo | `cs_arco = self._cs_arco_da_nodo(cs_nodo, i, j)` |
| `step` | `:5354` | legge CS_M | `cs_max_corrente = float(np.max(cs_arco)) if len(cs_arco) else CS_M` |
| `step` | `:5356` | legge CS_M | `cs_arco = np.full(len(i), CS_M, dtype=float)` |
| `step` | `:5357` | legge CS_M | `cs_max_corrente = CS_M` |
| `step` | `:5452` | legge CS_M | `cs2_src = (cs_arco ** 2 if CS_DINAMICO else CS_M ** 2)` |
| `step` | `:5464` | legge CS_M | `beta = 2.0 * zeta_loc * (cs_arco if CS_DINAMICO else CS_M) / np.maximum(self.d, 1e-6)` |
| `step` | `:5466` | legge CS_M | `beta = 2.0 * ZETA_M * (cs_arco if CS_DINAMICO else CS_M) / np.maximum(self.d, 1e-6)` |
| `step` | `:5501` | legge CS_M | `n3 = np.ceil(np.abs(self.vd).max() * DT / (0.05 * max(np.median(self.d), 0.1) * cs_max_c` |
| `step` | `:5511` | legge CS_M | `n3 = np.ceil(np.abs(self.vd).max() * DT / (0.1 * max(np.median(self.d), 0.1) * cs_max_co` |
| `step` | `:5554` | legge CS_M | `beta_new = 2.0 * zeta_loc * (cs_arco if CS_DINAMICO else CS_M) / np.maximum(d_new, 1e-6)` |
| `step` | `:5556` | legge CS_M | `beta_new = 2.0 * ZETA_M * (cs_arco if CS_DINAMICO else CS_M) / np.maximum(d_new, 1e-6)` |
| `step` | `:5651` | legge CS_M | `cs_taup = (cs_arco if CS_DINAMICO else CS_M)` |
| `mitosi` | `:5841` | chiamata a _fattore_tempo_arco | `_ft = self._fattore_tempo_arco(len(avv))       # dt_e/DT: il tempo d'arco, LETTO` |
| `mitosi` | `:5928` | chiamata a _tau_arco_causale | `_tau_a = self._tau_arco_causale(len(rep))` |
| `memoria_hebbiana_moto` | `:6680` | legge CS_M | `scala_statale = (CS_M ** 2) / I_med` |
| `memoria_hebbiana_moto` | `:6742` | legge CS_M | `_csa = np.full(int(np.sum(mask)), float(CS_M))` |
| `_applica_flag` | `:8370` | legge CS_M | `% (LAM / max(CS_M, 1e-12), (LAM / max(CS_M, 1e-12)) / max(DT, 1e-12)))` |
| `_applica_flag` | `:8370` | legge CS_M | `% (LAM / max(CS_M, 1e-12), (LAM / max(CS_M, 1e-12)) / max(DT, 1e-12)))` |
| `batch_condensazione` | `:9241` | legge CS_M | `"CS_M": CS_M, "K_C": K_C, "PHI_CRIT": PHI_CRIT,` |
| `_diag_completa` | `:9308` | legge CS_M | `floor_diag = CS_M / (1.0 + GAMMA * np.sqrt(np.maximum(I2[:n], 0.0)))` |
| `_diag_completa` | `:9310` | legge CS_M | `cs_nodo_diag = floor_diag + (CS_M - floor_diag) * trans_diag` |

## RAGGRUPPATO PER FUNZIONE — **13 funzioni toccano il tempo-luce o `cs`**

```
step                               14
_passo_spinoriale                  8
_cs_nodo                           3
_tau_arco_causale                  2
mitosi                             2
memoria_hebbiana_moto              2
_applica_flag                      2
_diag_completa                     2
_tempo_rampa                       1
_pesi                              1
_bloch_ritardato                   1
_tempo_luce_nodo                   1
batch_condensazione                1
```

## L'ORDINE DEL PASSO, letto da `csv/_passo.py` (non da un elenco a mano)

```
[('modulo', 'scuoti_vuoto'), ('metodo', 'step'), ('metodo', 'mitosi'), ('metodo', 'rilassa_disegno'), ('metodo', 'memoria_hebbiana_moto')]
```

## COSA QUESTO ELENCO **NON** DICE, e sono tre cose

1. **non dice che ognuna di queste sia un difetto.** Una legge che legge `cs` al passo 1 e'
   sbagliata **solo se il valore che riceve non e' quello del luogo** — e al passo 0 non lo
   e' per nessuno, perche' la cache non c'e'. **Quante di esse ne dipendano DAVVERO va
   misurato**, una per una, e questo strumento **non lo misura**: le trova.
2. **non dice se il fallback sia CONTATO.** E' la domanda di `P5`, ed e' quella che pesa:
   un ramo che cade su `CS_M` senza dirlo e' un **comportamento sconosciuto**. In questo
   repo uno di quei rami scattava nel **71.88 %** delle chiamate **senza che nessun sigillo
   se ne accorgesse**.
3. **la cura non e' «usare `CS_M` meglio»:** e' la stessa famiglia di `B1` (*il passo 1 senza
   tempo proprio*) e di `C7` (*la cache scartata a ogni mitosi*). **La forma di cura che ha
   funzionato in `C7` era EREDITARE**, non ricalcolare: il figlio prende `cs` dal padre.
   **Al passo 0 non c'e' un padre da cui ereditare**, e questa e' la differenza vera.
