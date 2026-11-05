# 2026-11-05 — `TBG`: IL BORDO PARZIALE *(Luca `2026-11-04` `20:18`-`22:26`; la voce `4` della coda, dopo `TL120`)* -- **LA PROPOSTA DEI VALORI DI `g`, FERMO: DECIDE LUCA**

> **La domanda di Luca:** esiste un `g` per cui il solitone diventa **rotondo e isotropo ma resta legato**, senza partire? `g_max` e' la manopola fra il toro aperto *(`TB3`, `0.03`)* e il toro chiuso *(`0`)*: col bordo parziale **il mare arriva a un equilibrio**, emissione contro assorbimento, a una densita' fissata da `g`. ### **`g` e' un parametro dell'AMBIENTE** *(quanto l'universo diluisce la radiazione, la voce `35`)*, **non una legge del modello: va dichiarato cosi'** *(e per `A1` non e' una manopola del modello: non entra nelle leggi, sceglie la scena)*.
> **Il disegno di Luca:** il bordo di `TB3` tranne `g_max`, `F3`, la partenza di `TF3`, fino a `30000`, **CON LE MAPPE** *(come `TB3`)*; l'arresto (i) resta, cosi' la corsa si ferma se il solitone parte.

## 1. LE PREMESSE *(dal repo)*
- **La riflessione misurata** *(`doc/referti_l2/bordo_riflessione.txt`, il pacchetto in banda `B`: `R` = la materia che torna dentro dopo un passaggio)*:

| `g_max` | `0` | `1e-4` | `3e-4` | `1e-3` | `3e-3` | `1e-2` | `3e-2` |
|---|---|---|---|---|---|---|---|
| `R` | `0.999` | `0.970` | `0.915` | `0.746` | `0.417` | `0.060` | `0.0096` *(la coda dispersiva)* |

- **Il costo:** come `TB3` *(il bordo, due libri per tick, le mappe)*: **`991` s per pezzo, `5.51` ore per corsa** *(`diag_tl120_costo.txt`)*. **Lo spazio su `E:`:** le mappe di `TB3` sono **`90751753` byte** per corsa *(`diag_e_tb3.txt`)*; **nel repo** `~43` MB di jsonl per corsa.
- **Le soglie della carta della forma:** sul toro chiuso *(`TM1000`)* **`rho 1` sta sotto il mare in tutte le mappe** e `rho 10` vicino *(`|c1| / c0` fino a `13%`)*; su `TB3` tutte sopra. **Col bordo parziale il mare sta fra i due:** ### **le soglie che contano sono `100` e `300`** *(sopra il mare in tutte e due le corse estreme)*; `1` e `10` si stampano con la marca «sotto il mare» mappa per mappa, come oggi.
- **Che cosa NON so:** la densita' del mare all'equilibrio per un `g` dato *(e' cio' che la corsa misura)*; se l'equilibrio arriva entro `30000` *(il mare di `TM1000` cresceva ancora a `16000`)*.

## 2. LA PROPOSTA *(il punto di partenza del guardiano, motivato con `R`)*
- ### **`g_max = 0.003`, `0.001`, `0.0003`:** la materia che torna a ogni passaggio **`42%`, `75%`, `92%`** -- **tre punti fra il toro aperto** *(`1%`)* **e quello chiuso** *(`100%`)*, **circa uniformi in `log(1 - R)`** *(la frazione assorbita `0.58`, `0.25`, `0.085`)*: il mare all'equilibrio dovrebbe salire di un fattore `~2`-`3` da un punto all'altro *(una stima: la densita' all'equilibrio va come l'emissione divisa per l'assorbimento)*.
- **Tre corse: `~16.5` ore** *(`3 x 5.51`)*, `~272` MB su `E:` *(`3 x 90.75`)*, `~130` MB nel repo.
- **Per ogni `g`, il referto** *(il mandato)*: la densita' del mare all'equilibrio *(oltre `25` nodi e nella fascia)*, lo spostamento, la velocita' e la persistenza come `tb3_corsa.txt`, l'esagonalita', l'ovalita', lo spessore del bordo, la corona nel tempo *(la carta della forma)*, il bilancio del bordo.
- **Gli stati completi?** `TBS` li salva *(Luca `13:16`)*; ### **per `TBG` il mandato non li nomina: la scelta e' di Luca** *(proposta: come `TBS`, ogni `1500` piu' `t 0`, `~2.3` MB l'uno: la corrente nella corona al variare di `g`)*.

### LE LETTURE DI LUCA *(scritte prima di girare; registrate)*
- **(g1)** c'e' un intervallo di `g` in cui l'esagonalita' scende di almeno due deviazioni standard sotto quella di `TB3` e il solitone non parte: **la finestra esiste**; conta quanto e' larga.
- **(g2)** il solitone si arrotonda solo dove e' gia' partito: **niente finestra**.
- **(g3)** l'esagonalita' non dipende da `g` entro il rumore: **il bagno non arrotonda**.
- **(g4)** altro, da descrivere.
- **Un run per `g` e' indicativo** *(le partenze sparse)*: **se (g1), va ripetuta con altri semi prima di dirlo.**
- ### ⚠ **Una nota per (g1):** a `TB3` l'esagonalita' e' `0.46%`-`1.33%` secondo la soglia, con una deviazione standard di mappa in mappa `0.19`-`0.24%`, e **il confronto con `TM1000` (il toro chiuso, `F0`) non si leggeva a nessuna soglia** *(`forma_solitone.txt`)*: **«due deviazioni standard sotto `TB3`» vuol dire sotto `~0.2`-`0.9%`**, e sul toro chiuso a `100` e `300` gia' stava a `0.43`-`0.46%`. **Il criterio e' di Luca; lo segnalo perche' la differenza da risolvere e' piccola.**

## 3. LE DOMANDE A LUCA *(il criterio di chiusura: le sue risposte, scritte qui)*
1. **I valori di `g`** *(`0.003`, `0.001`, `0.0003`, o altri)*.
2. **Le soglie della forma** *(`100` e `300` le principali)*.
3. **Gli stati completi** *(si' o no, a quali tempi)*.
4. **Il costo** *(`~16.5` ore, `~272` MB su `E:`)*.
