# 2026-10-29 — IL MODO INSTABILE DELLO STATO FERMO DI `S1` *([[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il mandato di Luca delle `08:24`, dopo `26300537`)*

> **LIVELLO:** lo spettro della mappa linearizzata sullo stato fermo salvato *(`L 81`)*, la forma del modo, un controllo di `450` tick; nessuna corsa lunga; nessun file del nucleo.

## 1. LE PREMESSE DAL CODICE

| che cosa | dove | il fatto |
|---|---|---|
| lo stato fermo | `db/stato_fermo/fermo_L81.npz`; lo sha1 in `doc/referti_l2/stato_fermo/cerca_L81.json` | `S1`, `s 0.3`, `N 1e6`, `mu -0.532745112`, residuo `9.808e-10` |
| il tick | `csv/_stato_fermo.py` `tick` | il congelato vero *(`VC.VUOTO` saltati, `phi` rimesso)* |
| il tick libero e le bande | `csv/_dove_va_la_materia.py` `matrice`, `autovettori` | `A`, `B`, `P0`, `Ppi` per indice di fase |
| la corsa dello stato fermo | `doc/referti_l2/stato_fermo/corsa_L81_00000.jsonl` | un punto ogni `10` tick |

## 2. I CRITERI

- **L'operatore:** `G(psi) = e^{i mu s} T(psi)` *(il sistema che ruota)*; `J v = (G^P(psi0 + h v) - G^P(psi0 - h v)) / (2 h)` sul vettore reale *(parte reale e immaginaria)*, `h = 1e-5 |psi0| / |v|`.
  **`P = 10` tick per prodotto**: lo stesso autovettore, `lambda_tick = lambda^{1/P}` *(il modulo e' univoco)*; separa i moduli `> 1` dal cerchio `|lambda| = 1` dei modi lineari.
- **Arnoldi** *(`scipy.sparse.linalg.eigs`, `which="LM"`)*: `k = 6` autovalori, `ncv = 40`, `tol = 1e-8`, al piu' `30` riavvii.
- **Il tasso:** `ln|lambda_tick| / s` per unita' di tempo; il confronto col `~0.2` della corsa.
- **Gli autovalori `= 1` attesi** *(la fase, le due traslazioni)*: col cerchio dei modi lineari a `|lambda| = 1`, Arnoldi a modulo massimo non li separa; **il controllo si fa diretto:** `|J (i psi0) - i psi0| / |psi0|` *(la fase, esatto)*, e `J d_x psi0` contro `d_x psi0` per la traslazione *(la derivata per differenze sul reticolo: approssimata)*.
- **La forma del modo** *(i due vettori reali `a`, `b` dell'autovettore complesso)*:
  - le armoniche angolari `m = 0 .. 12` attorno al baricentro della perturbazione della densita' `drho = 2 Re(sum conj(psi0) dpsi)` e della fase `2 Im(...)`, per anelli larghi `1`; la frazione di ciascuna `m`;
  - il profilo radiale di `|dpsi|^2`;
  - il peso per banda *(`A`, `B`, `P0`, `Ppi`)* come in `9aa268c8`.
- **Il controllo indipendente:** `450` tick dallo stato fermo; il punto del tick `450` = quello di `corsa_L81_00000.jsonl` al bit; lo scostamento `D = e^{i mu s t} psi(t) - psi0`, normalizzato; la sua sovrapposizione col sottospazio reale dei modi con `|lambda| > 1`.
- **Il punto `4`** *(la curva `N(mu)` sul reticolo)*: solo se il modo e' `m = 0`; uno script a parte.
- **DEVE:** il residuo dello stato fermo ricalcolato `< 1e-9`; lo sha1; `J` lineare *(`h` e `2 h` entro `1e-4` su un vettore a caso)*; il tick `450` al bit.

## 3. LE LETTURE *(di Luca, scritte prima, senza soglie)*

- `(a)` il modo e' radiale *(`m = 0`)*, nella banda `A`: VK applicato male *(dove: la curva `N(mu)`)*;
- `(b)` il modo rompe la simmetria rotonda *(`m >= 1`, quale)*, nella banda `A`: un'instabilita' che il criterio radiale non vede;
- `(c)` il modo ha peso in `B` o nelle piatte: la struttura a due componenti;
- `(d)` altro, descritto.

## 4. LE MOTIVAZIONI

- I dati della corsa: `|w - w(0)|` `3.1e-6` al tick `400`, `2.6e-3` al `500`: una crescita esponenziale da un residuo di `1e-9`.

## 5. TODO

1. questo file, da solo;
2. `csv/_modo_instabile.py`, commit; il referto; RELAZIONE; MAPPA *(la riga `d` della sezione `3` e le due righe della lista d'attesa)*; commit.

## 6. ANNOTAZIONE DOPO IL REFERTO *(`doc/referti_l2/modo_instabile.txt`; lo script `sha1-BYTE 9e6afa60`, `b02f6ce8`; `5/6`)*

| controllo | esito |
|---|---|
| lo stato fermo = la ricerca *(sha1)*; il residuo | passa; `9.808e-10` |
| `J` lineare *(`h`, `2 h`)* | passa; `1.4e-09` |
| la fase: `J (i psi0) = i psi0` | passa; `9.85e-09` |
| la traslazione lungo `A1` *(approssimata, senza DEVE)* | `|J d - d| / |d| = 2.297e-02` dopo `10` tick |
| **Arnoldi converge** *(`k 6`, `ncv 40`, `tol 1e-8`, `30` riavvii)* | **FALLISCE:** `0` autovalori convergiti; `21220` tick, `1050` s |
| il tick `450` dallo stato fermo = la corsa di `26300537` | passa, al bit; `|D| / |psi0| = 5.886e-03` |

- **Il sigillo e' FALLITO** *(Arnoldi)*: lo stato e il fallimento committati; **FERMO** *(par. `5`)*. Le parti `2` e `3` *(la forma e la sovrapposizione)* non hanno un modo su cui leggersi.
- **La causa non e' misurata.**
