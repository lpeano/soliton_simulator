# OGNI LETTURA DI `rho_s` / `_rho_sorgente` — la verifica che precede `INERZIA-1(C)`

*(`csv/_letture_rho_s.py`, per **AST**, **stringhe incluse**. Decisione di Luca, 2026-09-25:
cura **(C) LOCALE** — `rho_s` si normalizza per vicino **dentro `_contrasto` e solo lì**.
Sola lettura.)*

> ### LA DOMANDA: **la normalizzazione esce da `_contrasto`?**
> Se una lettura di `rho_s` **fuori** da `_passo_spinoriale` vedesse il valore normalizzato,
> la cura non sarebbe locale e toccherebbe **il campo** invece dell'**inerzia**.

```
occorrenze totali                      16
  letture                              14
  scritture                            2
  di cui trovate come STRINGA          4   <- la famiglia che l'audit di `eta` mancava
letture DENTRO `_passo_spinoriale`     7
letture FUORI                          7
```

## LETTURE **DENTRO** `_passo_spinoriale` — dove vive `_contrasto` — 7

| funzione | riga | come | nome | codice |
|---|---|---|---|---|
| `_passo_spinoriale` | `:3351` | attributo | `_rho_sorgente` | `_rho_s = self._rho_sorgente()` |
| `_passo_spinoriale` | `:3353` | nome | `_rho_s` | `np.isfinite(_rho_s) & (_rho_s > 0))` |
| `_passo_spinoriale` | `:3353` | nome | `_rho_s` | `np.isfinite(_rho_s) & (_rho_s > 0))` |
| `_passo_spinoriale` | `:3362` | nome | `_rho_s` | `_ko_rho = int(np.sum(~(np.isfinite(_rho_s) & (_rho_s > 0))))` |
| `_passo_spinoriale` | `:3362` | nome | `_rho_s` | `_ko_rho = int(np.sum(~(np.isfinite(_rho_s) & (_rho_s > 0))))` |
| `_passo_spinoriale` | `:3381` | nome | `_rho_s` | `_contrasto = np.where(_ok_n, _rho_s / np.where(_ok_n, _peq_nodo, 1.0), 1.0)` |
| `_passo_spinoriale` | `:3429` | attributo | `_rho_sorgente` | `_tq = _tq * self._rho_sorgente()[:, None]` |

## LETTURE **FUORI** — **queste NON devono vedere la normalizzazione** — 7

| funzione | riga | come | nome | codice |
|---|---|---|---|---|
| `<modulo>` | `:246` | STRINGA | `rho_spin` | `'rho_spin': ('nonneg', 'densita spinoriale: una DENSITA non e negativa'),` |
| `lambda_nodi` | `:2921` | attributo | `_rho_sorgente` | `rho = self._rho_sorgente()   # [FASE 2] \|psi\|^2 (off) o rho_spin = norma d` |
| `_rho_sorgente` | `:3859` | STRINGA | `rho_spin` | `_rs = getattr(self, "rho_spin", None)` |
| `mitosi` | `:5992` | attributo | `_rho_sorgente` | `I = self._rho_sorgente()   # [FASE 5] soglia mitosi su densita' SPINORIALE (` |
| `mitosi` | `:6173` | attributo | `_rho_sorgente` | `I = self._rho_sorgente()   # [FASE 5] densita' coppia su campo SPINORIALE (r` |
| `batch_condensazione` | `:10223` | STRINGA | `rho_spin` | `_snap_fisica = {k: getattr(net, k) for k in ('psi', '_psi_prec', '_spinor_li` |
| `batch_condensazione` | `:10281` | STRINGA | `rho_spin` | `_snap_cond = {k: getattr(net, k) for k in ('psi', '_psi_prec', '_spinor_lift` |

## SCRITTURE — 2

| funzione | riga | come | nome | codice |
|---|---|---|---|---|
| `_passo_spinoriale` | `:3351` | nome | `_rho_s` | `_rho_s = self._rho_sorgente()` |
| `calcola_psi` | `:3848` | attributo | `rho_spin` | `self.rho_spin = np.real(np.sum(np.conj(self.psi_spin) * self.psi_spin, axis=` |

## RAGGRUPPATO PER FUNZIONE

```
_passo_spinoriale                8
mitosi                           2
batch_condensazione              2
<modulo>                         1
lambda_nodi                      1
calcola_psi                      1
_rho_sorgente                    1
```

## IL VERDETTO SULLA LOCALITA' DELLA CURA

La cura e' LOCALE **se e solo se** la normalizzazione si applica a una variabile che vive
**dentro** `_passo_spinoriale` e **non** al valore restituito da `_rho_sorgente()`.
**Il punto della cura e' `_contrasto`**: `_rho_s / max(_cn, 1)` invece di `_rho_s`, con
**lo STESSO `_cn`** che `_peq_nodo` usa gia' come denominatore. **Nessuna grandezza nuova**
(`STANDARD 10`), e `_rho_s` **resta quello che era** per ogni altra riga del file.

**COSA GUARDARE NELLA TABELLA «FUORI»:** ogni riga li' e' una legge che legge il campo del
nodo e **che la cura NON deve toccare**. Se dopo la cura una di quelle cambia, la cura non
e' locale — e il sigillo lo misura con la byte-identita' a flag spento.

## COSA QUESTO ELENCO **NON** DICE

- **non dice che le letture FUORI siano equivalenti fra loro:** alcune usano `rho_spin`
  direttamente, altre passano da `_rho_sorgente()`. La tabella distingue **come**, non
  **quanto pesa** ciascuna.
- **la riduzione non si cerca qui:** questo audit risponde a *«chi legge»*, non a *«chi
  riduce»*. Per `eta` la domanda era l'altra, e le due non si sostituiscono.
