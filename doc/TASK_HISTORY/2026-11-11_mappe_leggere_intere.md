# 2026-11-11 -- LE MAPPE LEGGERE DELLE CORSE INTERE *(Luca `23:31`; per i video del guardiano)* [[PIANO-2D-3D]] [[VUOTO-SUL-FONDO]]

## 1. LE PREMESSE DAL CODICE *(cosa credo prima di guardare, e cosa NON so)*

- **Le mappe complete stanno su `E:\soliton_simulator\mappe\<corsa>\`** *(`corsa_accensione.RADICE_E`)*: **`rho` e `Lambda` in `float32`, una istantanea ogni `100` tick, `d1`, `d2`, `L`, `centro`** *(letto con `np.load`: `C35-0`, `C35-pi`, `S162` `21` file fino a `200000`; `C50-0` `20` file fino a `200000`)*.
- **Gli indici** *(`doc/referti_l2/mappe_indice_<corsa>.txt`)* **danno di ogni file la dimensione e lo `sha1` dei byte.**
- **`mappe_leggere.npz` di oggi lo scrive `csv/solitone/carta_campo.py`** *(fino a `66000` per le tre corse di `L 162`)*:
  - **`rho` della mappa in `float16`;**
  - **`dLambda = Lambda - Lambda(t 0)`, calcolato in `float64` e poi portato in `float16`;**
  - **`centro = (c1, c2)` da `toro.centro` sulla `rho` in `float64`;**
  - **`d1`, `d2` = `m - L//2`; `tempo = t s`** *(`s 0.15`)*;
  - **e per `L 162` `centro_bordo`, `R_A`, `g_max` dal `bordo` del jsonl.**
- **Cosa NON so:**
  - **la dimensione compressa di `101` fotogrammi** *(non compressi `101 x 26244 x 2 x 2` byte = `10.6 MB`)*;
  - **se il `bordo` di `C50-0` si legga con `CA.serie` come per le altre** *(provato: si', `c0`, `R_A 55`, `g_max 0.03`)*.

## 2. PROGETTAZIONE DEL RAGIONAMENTO

- **Uno script nuovo, `csv/solitone/mappe_leggere_intere.py --corsa <nome>`:**
  - **solo lettura su `E:`;**
  - **scrive `doc/referti_l2/campo_<corsa>/mappe_leggere_intere.npz`** *(per `C50-0` la cartella nuova)*;
  - **nessuna corsa, nessun cambio al nucleo.**
- **Lo STESSO calcolo di `carta_campo.py` per ogni fotogramma** *(le stesse operazioni nello stesso ordine)*, **un fotogramma ogni `2000` tick** *(`t % 2000 == 0`: `101` fotogrammi)*, **`np.savez_compressed`**, **`ogni = 20`** *(istantanee)*.
- **I DEVE:**
  - **F0:** **lo `sha1` di ogni file su `E:` = l'indice;**
  - **il numero dei fotogrammi = `101`**, **da `0` a `200000`;**
  - ### **IL DEVE DI LUCA:** **ai tick comuni** *(`0`-`66000`, ogni `2000`)* **`rho`, `dLambda` e `centro` coincidono con `mappe_leggere.npz` entro la precisione di `float16`** *(`|nuovo - vecchio| <= 2^-10 |vecchio|`, piu' il passo minimo del `float16`)*;
  - **DEVE FALLIRE:** **lo stesso confronto col fotogramma vecchio spostato di uno** *(`t` contro `t + 2000`)*;
  - **la dimensione di ogni file stampata, e DEVE stare sotto i `15 MB`.**
- **Cosa mi farebbe FERMARE:**
  - **un `sha1` diverso dall'indice;**
  - **un fotogramma comune che non coincide** *(vorrebbe dire che il calcolo NON e' quello di `carta_campo`)*.
- **I referti:** **`doc/referti_l2/mappe_leggere_intere_<corsa>.txt`.**

## 3. TODO DEL NEXT STEP

1. **lo script; la voce in `doc/INVENTARIO_strumenti.md`;**
2. **la suite, poi il commit del codice;**
3. **le quattro estrazioni; il commit dei `npz` e dei referti, con le dimensioni;**
4. **la riga nella relazione.**
