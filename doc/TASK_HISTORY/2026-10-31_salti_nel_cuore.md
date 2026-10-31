# 2026-10-31 — I SALTI NEL CUORE: UN CONTROLLO DELLA MISURA SULLA CORSA LUNGA DI `B` A `Gamma` *(UNA PROVA IN `csv/`, NESSUNA MODIFICA AL NUCLEO; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il mandato di Luca delle `19:08`, dopo `751bca7f`)*

> **Lo script:** `csv/_salti_nel_cuore.py` *(importa `_consolida_B`, `_coppia_di_B`, `_massimo_di_B`)*. **I dati:** `doc/referti_l2/salti_nel_cuore/`; gli stati in `db/salti_nel_cuore/` *(ignorato)*. **Il referto:** `doc/referti_l2/salti_nel_cuore.txt`.

## 1. LE PREMESSE DAL CODICE

- **Il fatto** *(il guardiano)*: il cuore `f_win` fra campioni consecutivi *(`10` tick)* varia di solito di `~1e-4`, ma salta spesso di `~0.0028`, in su o in giu', sempre della stessa ampiezza, con un salto di `w` di `~0.001`.
- **Il cuore, dal codice** *(`_congelato_lungo.punto`)*: `rho` per nodo *(`_energia_del_legame.densita`)*, **il baricentro `c = rho . pos / M` sulle posizioni NON periodiche**, `d` la distanza dei nodi da `c`, ### **`f_win = sum(rho[d <= w_in])/M`: una finestra NETTA.** `w_in` e' fisso per la corsa *(`_deriva_congelato.forma`, `6.6437`)*.
- **I jsonl NON hanno il baricentro** *(i campioni: `M`, `f_3w0`, `f_win`, `picco`, `t`, `tau`, `w`)*, **e degli stati resta solo quello di ripresa.** ### **Quindi gli stati si RIGENERANO:** dalla partenza *(`_coppia_di_B.partenza_corsa("B")`, lo sha1 `d22b7cc2`)*, **pezzo per pezzo con gli STESSI confini e la STESSA sequenza degli originali**: una scena nuova, `DC.forma`, **`_dove_va_la_materia.matrice`** *(che scrive lo stato della scena e cambia `Lambda` di `1.8e-15`: `baf1e5b3`; la si chiama per avere la stessa scena al bit)*, lo stato caricato, i tick.
- ### **Il controllo che gli stati sono al bit:** a fine di ogni pezzo **lo sha1 DEVE essere `sha_fine` dell'originale**, e **`f_win` di ogni campione DEVE essere quello del jsonl, al bit.** **Se no, mi fermo e lo dichiaro.**

### Cosa NON so

- **Se la rigenerazione e' al bit** *(stessa macchina, stesso numpy: lo credo, non l'ho provato)*.
- **Lo spessore di un arco:** lo prendo come **la lunghezza di un arco** *(la distanza fra i due nodi di un arco, da `pos`)*, e lo misuro.

## 2. I CRITERI

| il punto | il criterio, scritto prima |
|---|---|
| `0` | **La rigenerazione:** `17` pezzi *(`5` di `4000` tick di `a8e0e43b`, `12` di `10000` di `consolida_B`, fino a `133334`)*, uno per processo, ogni pezzo committato. **DEVE:** lo sha1 della fine = `sha_fine`; `f_win` di ogni campione = l'originale al bit; la partenza = `sha_partenza`. |
| `(a)` | **Il baricentro `(x, y)` ogni `10` tick**, con `f_win`, `w`. |
| `(b)` | **La scomposizione esatta di ogni passo:** `Delta f_win = (dentro a tutti e due) + (entrati) - (usciti)`; **il termine della FINESTRA** = `sum(rho2[entrati])/M - sum(rho1[usciti])/M`, **i nodi che hanno attraversato il bordo** *(quanti, e le loro `d - w_in` prima e dopo)*. **Un SALTO** e' un passo con `abs(Delta f_win) > 10 x` la mediana di `abs(Delta f_win)` *(`FATTORE_DEROGA`; il criterio di riconoscimento, non una lettura)*. Per ogni salto: `Delta f`, il termine della finestra, il resto, i nodi, lo spostamento del baricentro. |
| `(c)` | **Il cuore con la finestra LISCIA:** il peso `1` per `d <= w_in - h/2`, `0` per `d >= w_in + h/2`, **LINEARE in mezzo**, `h` la lunghezza di un arco *(dichiarata: la piu' semplice; un'altra forma darebbe un altro numero)*. **I salti della liscia, con lo stesso criterio** *(10 volte la SUA mediana)* **e contati agli stessi istanti dei salti della netta.** |
| `(d)` | **L'oscillazione lenta:** su `f_liscia` *(e `f_win`)* lo spettro *(la FFT della serie meno la media)*: **il periodo del picco, l'ampiezza** *(`(max - min)/2` e la deviazione standard)*; **il legame col baricentro:** la correlazione a ritardo zero fra `f_liscia` e la distanza del baricentro dalla sua media, e fra `f_liscia` e `w`. |

## 3. LE LETTURE *(di Luca, scritte prima, senza soglie)*

- **(j1)** i salti sono della finestra *(spariscono con quella liscia)*;
- **(j2)** restano anche con la finestra liscia: un fatto fisico *(descriverlo)*;
- **(j3)** altro.

## 4. LE MOTIVAZIONI

**Una misura che salta per la geometria del reticolo non e' fisica, e un'oscillazione «lenta» letta su una misura a gradini puo' essere in parte il baricentro che passa sopra i nodi.** Prima di leggere il cuore come fisica, **si separa la misura dall'oggetto.**

## 5. TODO

1. Questo file, committato **DA SOLO**.
2. `csv/_salti_nel_cuore.py` e la riga nell'inventario, committati prima di girare.
3. `--rigenera` a pezzi *(`17`)*, ogni pezzo committato; **se un DEVE del bit fallisce: FERMO.**
4. `--referto`; `RELAZIONE`; `MAPPA` *(la riga `d`)*; `doc/FATTI_dal_codice.md` *(se la finestra netta salta: un fatto su `_congelato_lungo.punto`)*; la sezione `6` qui.
