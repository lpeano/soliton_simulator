# LE CORSE SOSPESE *(la decisione di Luca del `2026-11-22` `14:01`, e [M1417] S4)* [[PROGETTO-MITOSI]]

> **Perche' questo file:** il registro delle corse (`doc/REGISTRO_CORSE.md`) non ha l'esito SOSPESO *(gli esiti sono FINITO, FERMATO, FALLITO: `csv/solitone/_registro_corse.py`, che e' in uso da MITOSI_v2 e non si tocca)*. **Le tre voci qui sotto risultano FALLITO nel registro** perche' i loro lanciatori *(`doc/referti_l2/triangolo_lancia_v3.sh`, `_v4.sh`)* chiudono da soli la voce con FALLITO quando il processo esce con un codice diverso da `0`: **la fermata delle `14:10-14:11` (uscita `127`) non e' un fallimento della corsa.** **Le voci FALLITO restano** *(Luca, S4)*; **alla ripresa, una voce APERTA nuova.**

## Il perche' *(di Luca, `14:01`)*

> «collegamento di χ alla materia di oggi (V1); in attesa della forma solo orologio [M1310]; la decisione se riprenderle o rifarle è di Luca.»

**Annotazione** *(`14:27`, `1a63daf6`)*: **il bivio di [M1310] non e' passato** *(l'orologio della variante V3 va piu' veloce dove `N` e' piu' basso)*: **la forma «solo orologio» non si costruisce.** La decisione su queste tre corse resta di Luca.

## Le corse

| la voce del registro | il comando | fermata | l'ultimo stato integro | lo sha1 *(dei byte, coincide col `.sha1`)* | max \|Theta\| all'ultima tappa |
|---|---|---|---|---|---|
| `chi-tronco-t120` | `doc/referti_l2/triangolo_chi_v3.py tronco --quale t120 --fino 200000` | `14:10` *(pid 22400)* | `E:\soliton_simulator\controllo\CHI\triangolo\t120\stato_035000.npz`, **k 35000** | `cf61f98d...` | `3.1099` *(13:12, k 32370)* |
| `chi-tronco-t120r28` | `doc/referti_l2/triangolo_chi_v3.py tronco --quale t120r28 --fino 200000` | `14:11` *(pid 9092)* | `...\t120r28\stato_035000.npz`, **k 35000** | `544c4dbe...` | `2.9296` *(13:12, k 32368)* |
| `chi-tronco-t000` | `doc/referti_l2/triangolo_chi_v4.py tronco --quale t000 --fino 200000` | `14:11` *(pid 7584)* | `...\t000\stato_029250.npz`, **k 29250** | `c389d7c7...` | `3.0169` *(13:41, k 28289)* |

- **Come si riprende:** lo stesso comando *(il tronco cerca l'ultimo stato salvato della sua cartella e riparte da li': la ripresa P8 dei tronchi)*, **con una voce APERTA nuova** nel registro.
- **Nessun file a meta':** in ognuna delle tre cartelle l'ultimo `.npz` e' quello col `.sha1`, e lo sha1 dei byte coincide *(controllato alle `14:13`)*.

## Non sospese

- **`chi-mattone-v2`** *(`doc/referti_l2/chi_mattone_v3.py corsa --fino 20000`, `CHI/mattone_v2`)*: gira fino a `k 20000` *(la fine della corsa)*; **non e' la corsa del referto `doc/referti_l2/chi_mattone_v2.txt` delle `01:11`**, che e' la parte C allungata della corsa vecchia *(`CHI/mattone`)*.
- **`mitosi-ramo-MITOSI-v2`** *(Luca: non si sospende)*; **`mitosi-ramo-C2EXT`** e' finita da sola alle `12:41` *(FINITO, uscita `0`, `k 45976`; la chiusura committata nel ramo mitosi, `d0ca7274`)*.
