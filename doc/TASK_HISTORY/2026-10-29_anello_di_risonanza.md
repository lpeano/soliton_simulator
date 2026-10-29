# 2026-10-29 — L'ANELLO DI RISONANZA E IL TERZO PASSO *([[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il mandato di Luca delle `12:11`, dopo `dfb5ab7e` e `6d941a4d`)*

> **LIVELLO:** un conto sugli stati fermi salvati *(nessuna corsa)*; una corsa di `180` unita' di tempo a `s 0.075`; nessun file del nucleo.

## 1. LE PREMESSE DAL CODICE

### Il punto `1`: come il legame agisce sulle piatte

| che cosa | dove | il fatto |
|---|---|---|
| la fase del legame | `primo_ordine/materia_vuoto.applica` | `psi_h *= exp(-i alpha(rho/Lambda) dtau f)`, **la stessa fase per tutte le `12` componenti del nodo** *(`np.take(al * dtau * f, nodo)`, poi `psi_h * esp.reshape(-1, 1)`)*; `rho` = `sum |psi|^2` del nodo, `Lambda` = `sum |phi|^2` del nodo |
| quante volte | `composizione.ORDINE` | `CAMM-MATERIA-VUOTO` due volte, `f = 0.5` *(il primo e l'ultimo pezzo)*: **in tutto `exp(-i alpha dtau)` per tick** |
| `dtau` | `flussi_parziali.dtau_nodo` sulla scena | `= s` in ogni nodo *(`0.3`, `0.15`, `0.075`: letto)* |

**Il fatto:** il legame e' **uno scalare per nodo**, uguale su ogni banda. In un mezzo uniforme di densita' `rho` sposta **tutte** le bande *(piatte comprese)* della stessa fase: `ph_banda(rho) = ph_banda(0) + alpha(rho/Lambda) s`, con `ph = -arg(lambda)` per tick.

### Le convenzioni

- `ph = -arg(lambda)` per tick, come in `_dove_va_la_materia.autovettori`: `P0` a `0`, `Ppi` a `-pi s`.
- Lo stato fermo: `T psi0 = e^{-i mu s} psi0`, quindi `ph_sol = mu s` per tick, `mu` per unita' di tempo. **Il «`-mu`» del mandato e' questa frequenza** *(il segno e' quello della convenzione)*.

### Il terzo passo

- Lo stato di `S1` `s 0.075` *(`dfb5ab7e`)*: il residuo `9.696e-06`, lo sha1 `9744446c`; **non e' fermo secondo il criterio.**

## 2. I CRITERI

- **Il conto, per anello `r = 0..24`** dello stato fermo *(il baricentro, anelli larghi `1`)*: `alpha` medio sui nodi dell'anello *(`alpha(rho_nodo/Lambda_nodo)`)*; `ph_P0(r) = alpha s`, `ph_Ppi(r) = -pi s + alpha s`.
  **Le condizioni** *(avvolte in `(-pi, pi]`)*: `(c1)` `ph_p(r) - ph_sol` per `p` = `P0`, `Ppi`; `(c2)` `ph_p(r) + ph_p'(r) - 2 ph_sol` per le tre coppie `P0+P0`, `P0+Ppi`, `Ppi+Ppi`. **Un incrocio:** un cambio di segno fra due anelli vicini.
  Per unita' di tempo: diviso per `s`.
- **In piu'** *(dichiarato qui)*: la frequenza del modo nel sistema che ruota, `2 pi / periodo` *(`11.45`)*, contro `ph_p(r) - ph_sol`: i raggi dove `|ph_p(r) - ph_sol| = 2 pi s / 11.45`.
- **A `s 0.3` e `s 0.15`**, gli stati fermi di `26300537` e `dfb5ab7e`.
- **Il terzo passo:** `S1` `s 0.075`, `L 81`, dallo stato di `dfb5ab7e`; `2400` tick; l'esame di `dfb5ab7e`; **la finestra fra `10` volte il residuo e `1e-2`**, non `1e3` volte: **una deroga**, motivata dal residuo `9.7e-6` *(con `1e3` volte il bordo basso sarebbe `9.7e-3`, quasi la saturazione)*.
- **DEVE:** lo sha1 degli stati; `dtau = s` su ogni nodo; `M` conservata nella corsa entro `1e-10`.

## 3. LE LETTURE *(di Luca, scritte prima, senza soglie)*

- `(r1)` una condizione si incrocia negli anelli `12`-`13` a tutte e due le `s`: l'anello di risonanza spiega dove nasce il modo *(quale)*;
- `(r2)` si incrocia altrove; `(r3)` nessun incrocio; `(r4)` altro, descritto.
- Il terzo passo: il terzo punto della serie `0.139`, `0.151`.

## 4. LE MOTIVAZIONI

- Il modo vive dove la densita' cade *(gli anelli `12`-`13`)*: li' `alpha` passa da `~1` a `~0`, e la frequenza locale delle piatte attraversa un intervallo largo `s`.

## 5. TODO

1. questo file, DA SOLO, e aspettare il push;
2. `csv/_anello_di_risonanza.py`, commit; `--referto`; RELAZIONE; MAPPA *(la riga `d`; le due voci della lista d'attesa)*; commit.

## 6. ANNOTAZIONE DOPO IL REFERTO *(`doc/referti_l2/anello_di_risonanza.txt`; lo script `sha1-BYTE fd579c2c`, `c0db073f`; `6/6`)*

| per tick, avvolte | `s 0.3`: anello `12` / `13` / `14` / `15` | `s 0.15`: anello `12` / `13` / `14` / `15` |
|---|---|---|
| `alpha` medio | `0.992` / `0.753` / `0.055` / `0.0003` | `0.992` / `0.771` / `0.061` / `0.0004` |
| `(c1)` `P0` | `+0.457` / `+0.386` / `+0.176` / `+0.160` | `+0.234` / `+0.201` / `+0.094` / `+0.085` |
| `(c2)` `P0+Ppi` | `-0.028` / `-0.171` / `-0.590` / `-0.623` | `-0.004` / `-0.070` / `-0.283` / `-0.301` |
| `|c1 P0|` meno la frequenza del modo | `+0.293` / `+0.221` / `+0.012` / `-0.005` | `+0.151` / `+0.118` / `+0.012` / `+0.003` |

| la condizione | gli incroci a `s 0.3` | a `s 0.15` |
|---|---|---|
| `(c1)` `P0`, `Ppi`; `(c2)` `P0+P0`, `P0+Ppi`, `Ppi+Ppi` | nessuno | nessuno |
| `|c1 P0|` = la frequenza del modo *(aggiunta)* | fra gli anelli `14` e `15` | nessuno |
| `(c2)` `P0+Ppi` nel cuore *(anelli `0`-`11`)* | `-0.023` | `-0.0016` |

| lettura *(di Luca, scritta prima)* | esito |
|---|---|
| (r1) un incrocio negli anelli `12`-`13` a tutte e due le `s` | **no** |
| (r2) un incrocio altrove | solo la condizione aggiunta, fra `14` e `15`, e solo a `s 0.3` |
| (r3) nessun incrocio | **si', per le condizioni `c1` e `c2`** |
| (r4) altro | **la coppia `P0+Ppi` e' quasi risonante nel cuore saturo** *(`c2` `-0.023` a `s 0.3`, `-0.0016` a `s 0.15`: si avvicina a zero al calare di `s`)*, non sul bordo |
| il terzo passo *(`s 0.075`)* | **il tasso non si misura:** lo stato di partenza non e' fermo *(`9.7e-6` per tick)*; `|D|/|psi0|` e' gia' `1.9e-2` al tempo `60` e cresce senza un tratto esponenziale; la finestra, anche in deroga, e' vuota |
