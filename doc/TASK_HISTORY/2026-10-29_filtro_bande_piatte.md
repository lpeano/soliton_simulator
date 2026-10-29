# 2026-10-29 — LA DIAGNOSI COL FILTRO SULLE BANDE PIATTE *(NON una cura; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il mandato di Luca delle `10:22`, in coda dopo quello delle `10:00`)*

> **LIVELLO:** uno strumento di diagnosi in `csv/`, mai nel nucleo; corse brevi in memoria dagli stati fermi salvati.

## 1. LE PREMESSE DAL CODICE

| che cosa | dove | il fatto |
|---|---|---|
| l'esito delle `10:00` | `dfb5ab7e` | il tasso `0.139` a `s 0.3`, `0.151` a `s 0.15`; il periodo `11.45` a tutte e due; il modo sul bordo e nelle piatte; lo stato fermo a `s 0.075` e di `S4` non trovato |
| gli stati fermi | `csv/_modo_al_variare_di_s.py` `carica` | `S1_s0.300` *(`26300537`)*, `S1_s0.150` *(`dfb5ab7e`)* |
| il tick, la scena | `csv/_modo_al_variare_di_s.py` `scena`, `tick` | il congelato vero |
| gli autovettori del tick libero | `csv/_dove_va_la_materia.py` `matrice`, `autovettori`, `GRUPPI` | ordinati per fase: `Ppi` = indici `0-3`, `A` = `4-5`, `P0` = `6-9`, `B` = `10-11` |
| **il punto `5` del mandato** | `dfb5ab7e` | il passo dove il modo e' piu' forte: **`s 0.15`** *(`0.151` contro `0.139`)* |

## 2. I CRITERI

- **Il filtro**, a ogni tick dopo il tick: `fft2` di `psi`; i coefficienti sugli autovettori `Z(k)`; a zero quelli di `P0` e `Ppi`; indietro; la norma tolta *(prima della rinormalizzazione)*; la rinormalizzazione a `N`.
- **Le corse:** `S1` `s 0.3` `L 81` per `600` tick; `S1` `s 0.15` `L 81` per `1200` tick *(lo stesso tempo fisico, `180`)*.
- **L'esame**, come `5f06dbfb` e `dfb5ab7e`: `D(t) = e^{i mu s t} psi(t) - psi0` ogni `round(3/s)` tick dal tempo `60`; il tasso nella finestra fra `1e3` volte il residuo e `1e-2`; il periodo; anelli e bande ai tre istanti dichiarati dai dati *(il primo `|D|/|psi0| >= 1e-4`, il primo `>= 1e-3`, l'ultimo della finestra)*.
  **E lo stesso esame rispetto allo stato fermo filtrato una volta e rinormalizzato** *(`psi0f`)*: se il filtro sposta lo stato fermo, `D` rispetto a `psi0` parte gia' grande.
- **La norma tolta:** a ogni tick *(stampata ogni `round(3/s)` tick)* e il totale.
- **Il controllo** *(punto `4`)*: la frazione di `|psi0|^2` nelle piatte; e la distanza `|psi0f - psi0| / |psi0|`.
- **DEVE:** lo sha1 degli stati fermi; la somma dei pesi per banda = `|psi|^2` *(Parseval)* entro `1e-12`.

## 3. LE LETTURE *(di Luca, scritte prima, senza soglie)*

- `(a)` col filtro il modo sparisce, o il tasso cala molto: le piatte sono il canale;
- `(b)` il modo resta con lo stesso tasso: il canale e' un altro *(dove va `D`)*;
- `(c)` il filtro cambia troppo lo stato fermo per leggere: si scrive;
- `(d)` altro, descritto.

## 4. LE MOTIVAZIONI

- Il filtro non e' locale *(la trasformata sul toro)* e rompe le conservazioni: una prova del canale, non una modifica del modello.
- Se il canale sono le piatte, la cura si cerca nel modello *(la moneta o la composizione che allontanano le piatte dalla frequenza del solitone)*: una voce della lista d'attesa della MAPPA, da NON eseguire.

## 5. TODO

1. questo file, DA SOLO, e aspettare il push;
2. `csv/_filtro_bande_piatte.py`, commit; `--referto`; RELAZIONE; MAPPA *(la riga `d`; la voce della lista d'attesa; la riga `5` della coda)*; commit.

## 6. ANNOTAZIONE DOPO IL REFERTO *(`doc/referti_l2/filtro_bande_piatte.txt`; lo script `sha1-BYTE 093675f7`, `8068d88e`; `4/4`)*

| | `S1` `s 0.3` | `S1` `s 0.15` |
|---|---|---|
| il tasso SENZA filtro *(`dfb5ab7e`)* | `0.13870` | `0.15108` |
| il tasso COL filtro, rispetto allo stato fermo filtrato *(`psi0f`)* | `0.00067` | `0.00047` |
| il tasso COL filtro, rispetto allo stato fermo *(`psi0`)* | `0.00018` | `0.00008` |
| `|D|/|psi0|` rispetto a `psi0f`, tempo `60` -> `180` | `3.5e-03` -> `4.0e-03` | `2.7e-03` -> `3.0e-03` |
| le bande di `D` rispetto a `psi0f` *(`A` / `B`)* | `0.986` / `0.014` -> `0.990` / `0.010` | `0.980` / `0.020` -> `0.984` / `0.016` |
| il controllo: le piatte nello stato fermo; `|psi0f - psi0| / |psi0|` | `3.8959e-05`; `6.2417e-03` | `3.9004e-05`; `6.2454e-03` |
| la norma tolta: il primo tick; la media degli ultimi `100` *(`200`)* tick; il totale | `3.896e-05`; `7.328e-06`; `4.4200e-03` | `3.900e-05`; `1.925e-06`; `2.3449e-03` |

| lettura *(di Luca, scritta prima)* | esito |
|---|---|
| (a) col filtro il modo sparisce o il tasso cala molto: le piatte sono il canale | **SI':** il tasso cala da `0.139` a `0.0007` *(`s 0.3`)* e da `0.151` a `0.0005` *(`s 0.15`)*; in `180` unita' di tempo `D` non cresce |
| (b) resta con lo stesso tasso | no |
| (c) il filtro cambia troppo lo stato fermo | **una cautela, non un impedimento:** lo sposta di `6.2e-3` *(le piatte sono `3.9e-5` della norma)*; e toglie norma a ogni tick, costante *(`7.3e-6` per tick a `s 0.3`)*: il bordo continua a riempire le piatte |
| (d) altro | -- |
