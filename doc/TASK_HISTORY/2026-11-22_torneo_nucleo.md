# IL TORNEO DELLE FORME, IL PASSO 3: LE FORME NEL NUCLEO DI `lapse-u` *(il mandato [M1631]; la decisione di Luca delle `19:20` circa sulle sez. 5 e 9 della carta)* [[PROGETTO-MITOSI]]

> **Scritto e committato PRIMA di toccare il nucleo.** La carta: `doc/CARTA_torneo_nonlinearita.md`.

## 1. LE PREMESSE DAL CODICE *(cosa credo prima di guardare, e cosa NON so)*

- **La forma si sceglie dalla tabella:** `primo_ordine/leggi/leggi.yaml`, voce `CAMM-MATERIA-VUOTO`, `parametri.forma` *(`valore: S1`, `ammessi: {S1, S3}`)*; il modulo generato `primo_ordine/termini/camm_materia_vuoto.py` porta `PARAMETRI = {'forma': 'S1'}`; `primo_ordine/materia_vuoto.py` ha `FORME = {"S1": ..., "S3": ...}` e `FORMA = _TMV.PARAMETRI["forma"]`, con l'assert `FORMA in FORME`.
- **Il collaudo delle forme** *(`primo_ordine/_collauda_forme.py`)* pretende `sorted(MV.FORME) == sorted(ammessi)` e il generatore della tabella uguale all'espressione della forma predefinita, e fa le differenze finite di `alpha = dN/drho` e `beta = dN/dLambda` **per OGNI forma di `MV.FORME`**: **le forme nuove sono provate da quel collaudo senza toccarlo** *(e non lo posso toccare: il diff del nucleo contro `42638304` SOLO nei cinque file del mandato)*.
- **Gli `ammessi` sono testo:** credo che nessuno li derivi simbolicamente *(lo cerco nel generatore prima di scriverli)*. **Non so** se il generatore rifiuta un nome con `+` o `.` come chiave YAML *(`L+0.5`)*: lo vedo rigenerando.
- **Il diff del nucleo contro `42638304` oggi:** `_mappa.yaml` *(+4)* e `motore_numba.py` *(+325)*, gia' dentro i cinque file ammessi. **Dopo il passo 3 deve contenere SOLO quei cinque file.**
- **F0 al bit:** `S1` non cambia una riga, quindi il tick a F0 deve restare identico al bit; **la prova la da' la ripresa di uno stato di oggi** *(sotto)* e `collauda.py`.

## 2. PROGETTAZIONE DEL RAGIONAMENTO

- **(R0) Il braccio 0, PRIMA di toccare il nucleo:** il file nuovo `doc/referti_l2/ripresa_F0.py`: lo stato `CHI/caduta/V1/stato_001750.npz` *(la caduta libera di oggi, V1: `cs = s N` e la fase (a))*, il campo `A` ed `E` rimessi dal file, `250` tick di `caduta_segno_v2.tick_var` col `residuo` di Gauss allo stesso `k` assoluto della corsa; **lo stato a `k 2000` contro `stato_002000.npz` del disco, ARRAY PER ARRAY, al bit.** **Se il braccio 0 NON coincide** *(la ripresa non e' esatta: uno stato interno che il file non porta)*, **la prova di dopo non vale:** lo dico, e la ripresa si fa come confronto prima/dopo dello stesso script *(lo sha1 dopo `250` tick col nucleo di prima, contro quello col nucleo di dopo)*.
- **(R1) Lo sblocco:** `doc/NUCLEO_CONGELATO.md` di `lapse-u` a `stato: SBLOCCATO` con la riga di Luca, **nello stesso commit del nucleo** *(il presidio non agisce su `lapse-u`; la procedura alla lettera)*.
- **(R2) Il nucleo, UN commit:** `leggi.yaml` *(gli `ammessi` nuovi: `L+0.5`, `L+0.25`, `L0`, `L-0.25`, `L-0.5`, `L-1`, `FH`, `FT`, con le espressioni di `N` della carta sez. 1; `valore: S1` NON cambia; l'`origine` dice la decisione e il mandato)*; `python primo_ordine/_genera.py` *(il modulo generato)*; `materia_vuoto.py` *(le funzioni `N`, `alpha`, `beta` delle forme nuove e `FORME` esteso)*.
  - **Flambda:** `lambda * N_s1`, `lambda * alpha_s1`, `lambda * beta_s1` *(una fabbrica; i limiti sono quelli di S1 per `lambda`)*.
  - **FH:** `N = Lambda (x - 2 arctan x)`, `alpha = (x^2 - 1)/(x^2 + 1)`, `beta = x - 2 arctan x - x (x^2 - 1)/(x^2 + 1)`; a `Lambda = 0` il limite `1`, `-pi`, `rho`.
  - **FT:** `N = Lambda (ln cosh(x - 1) - ln cosh 1)`, `alpha = tanh(x - 1)`, `beta = N/Lambda - x tanh(x - 1)`; a `Lambda = 0` il limite `1`, `-1 - ln 2 - ln cosh 1`, `rho`. ### ⚠ **`ln cosh y` si calcola come `|y| + log1p(e^{-2|y|}) - ln 2`** *(`cosh` trabocca oltre `y ~ 710`; e' la stessa funzione, una forma float diversa: FT non ha un riferimento al bit, quindi non rompe niente, dichiarato)*.
  - **A `rho = 0`:** `alpha` vale cio' che l'espressione prende a `x = 0` *(come S1: `0` per Flambda, `-1` per FH, `tanh(-1)` per FT; `psi = 0` la', quindi la fase non conta)*, `beta = 0` e `N = 0` per tutte. **A `rho = 0` e `Lambda = 0`:** `0` *(come S1)*.
- **(R3) Le suite:** `python primo_ordine/collauda.py` *(a F0)*; `_collauda_forme.py` deve passare con le forme nuove dentro *(le differenze finite per ognuna)*; la ripresa di R0 al bit; il diff del nucleo contro `42638304` coi soli cinque file.
- **(R4) Il ricongelamento:** `stato: CONGELATO` nel commit dopo le suite, con gli esiti.
- **COSA MI FA FERMARE:** il braccio 0 o la ripresa dopo NON al bit; `collauda.py` non verde; un file del nucleo fuori dai cinque; il generatore che rifiuta i nomi o le espressioni *(la cura sarebbe cambiare i nomi nella tabella: se cambia una scelta della carta, lo dico)*; le differenze finite di una forma nuova fuori da `1e-7` *(un errore mio nelle derivate: lo cerco, non allargo la soglia)*.

## 3. TODO DEL NEXT STEP

1. commit di questo file, della sez. 9 della carta *(la decisione di Luca su 1d)* e della relazione;
2. `doc/referti_l2/ripresa_F0.py`: commit, poi il braccio 0 *(R0)*, il referto committato;
3. R1 + R2 in un commit *(il nucleo)*, con `collauda.py` nel messaggio;
4. R3: i referti committati; R4: RICONGELATO;
5. poi il passo 4 *(i lanciatori, la semina al fondo, le voci della coda a priorita' `0`)* e le tenute *(5a)*; **[M1446-F2]** *(tre corse corte a `d 39`, in fase e in antifase: U spento, phi congelato, tutti e due)* **a priorita' `1` dopo le tenute**.
