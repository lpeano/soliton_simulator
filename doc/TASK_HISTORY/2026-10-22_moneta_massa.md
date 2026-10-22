# LA MONETA E' LA MASSA? LA CURVATURA `c` DELLA CAMMINATA A ONDE LUNGHE IN FUNZIONE DI `eps`

> **Il mandato:** decisione di Luca del `2026-10-22` alle `19:43`, dopo `82b40ca1` *(`doc/ORIGINE_32_ARCHI.md`)*. ### **MISURE: `leggi.yaml` e
> l'impronta INTATTI; `eps` SOLO come parametro della scena** *(come `f9c5521e`)*. ### **Nessuna cura, nessuna regola di scala cambiata.**

**LIVELLO:** `L2`, misure.

## 0. LA STELLA POLARE

1. **`A14`:** ### **non si applica** *(nessuna legge cambia)*.
2. **Il gradino:** `(a)` ### **a `eps` di oggi lo strumento ridà `c` di `82b40ca1`** *(il controllo che ripete la cosa giusta)*; `(b)` ### **`eps =
   0` toglie la moneta** *(il caso «senza massa»)*; `(c)` ### **gli automi di Dirac** *(sez. `4`)*.
3. **Aggiunge un numero o una legge?** ### **No: `eps` varia SOLO nella scena**, ### **come informazione.**
4. **Tocca `rho`, `c_s` o il segno?** ### **No:** tocca la camminata *(la moneta di spin)*; `cs` spento.
5. **Emergente o imposto?** ### **E' la domanda:** ### **la curvatura `c` e' la massa che la moneta impone, o altro.**

## 1. LA LETTURA DA METTERE ALLA PROVA *(dal mandato, alla lettera)*

> «la moneta di spin `eps` fa da MASSA della materia: a onde lunghe la camminata ha dispersione `omega^2 ~ Delta^2 + v^2 k^2`, con `Delta` (il
> salto a `k = 0`) proporzionale a `eps`, quindi `c = v^2 / Delta` proporzionale a `1/eps`; e senza moneta (`eps = 0`) la camminata e' SENZA
> MASSA (dispersione lineare a `k` piccolo).»

## 2. RAGIONAMENTO PRELIMINARE E PREVISIONI *(scritte prima)*

- ### **LA PROCEDURA DI `82b40ca1`, letta dal codice** *(`_stabilita_lineare.camminata_complessa`, `fasi`, e `np.gradient`)*: ### **`omega =
  -angle(lambda) / dtau`** dei `12` rami *(materia `8` + vuoto `4`)* ordinati a ogni `k`, ### **lungo `(m, 0)`**; ### **`c` = la mediana su
  rami `3, 4, 5, 9, 10, 11` di `|v_g(1)| / k(1)`** *(`v_g` = `np.gradient`)*. ### **Il controllo che ripete la cosa giusta usa ESATTAMENTE questa
  procedura.**
- ### ⚠ **IL LATO `64` E LA REGOLA DI OGGI:** ### **oggi `eps = 0.5` a tutte e due le taglie**, quindi ### **a lato `64` `eps dtau = 0.03125`**, non
  `0.0625`: ### **la `c = 0.3882` di `82b40ca1` e' a `eps = 0.5`.** ### **La scansione: gli STESSI `eps`** *(`0`, `0.125`, `0.25`, `0.5`, `1`, `2`,
  cioe' `eps dtau` `0`-`0.25` a lato `32`)* ### **a tutte e due le taglie** *(«`eps` variato a `dtau` fisso», e la regola di oggi)*; ### **il controllo
  `c` a `eps = 0.5` a tutte e due.**
- ### **LA MISURA DELLA MASSA, nel SETTORE DELLA MATERIA** *(`A(k)[:8, :8]`: la moneta agisce sulla materia)*: ### **i rami dispersivi** *(`|v_g|`
  massimo `> 0.1` lungo `(m, 0)`)*; per ognuno ### **il fit `omega_b(k) - omega_b(0) = sqrt(Delta^2 + v^2 k^2) - Delta`** *(minimi quadrati, `k` fino a
  `0.25 pi`)*, ### **`c = v^2/Delta`**, e ### **il controllo del fit entro `5%`**; ### **e il salto a `k = 0`** *(la distanza dal ramo piu' vicino del
  settore)*, come informazione.
- ### ⭐ **LE PREVISIONI:** ### **credo PARZIALE.** La moneta e' ### **`exp(-i eps dtau sigma.n)`** *(una fase sullo spin: si', una massa)*, ### **ma
  la camminata ha anche il Grover** *(il flusso `pi s` sulle direzioni)*, ### **che mescola le estremita' e puo' aprire un salto suo**: ### **credo che
  a `eps = 0` la camminata NON sia del tutto senza massa** *(`v_g(2)/v_g(1)` lontano da `1`)*, ### **e che `Delta` cresca con `eps` meno che
  linearmente** *(`Delta^2 ~ Delta_G^2 + (k eps)^2`)*. ### **`c * Delta` costante: credo di si', entro il `5%`** *(se la parabola e' quella di un
  Dirac)*. ### **La lunghezza segue `c`:** credo di si' *(`82b40ca1`: `12` su `18`)*.

## 3. LE MISURE, I CONTROLLI E LE LETTURE *(copiati dal mandato)*

- ### **MISURA `1`** *(la camminata sola, esatta; veloce)*: lato `32` e `64`, gli `eps` della sez. `2`. ### **DEVE RIUSCIRE:** ### **a `eps = 0.5` la
  procedura di `82b40ca1` ridà `c = 0.3894` (lato `32`) e `0.3882` (lato `64`) entro `1e-4`.** ### **Committata DA SOLA.**
- ### **MISURA `2`:** `S1`, `R2`, `x 0.1`, lato `32`, base proiettata, `N dtau 400`, la norma, ### **a `eps dtau` `0.03125`, `0.0625`, `0.125`**: il
  `k` del massimo e `gamma`, ### **contro `sqrt(2 gamma / c)`** con la `c` della misura `1`. ### **`eps dtau 0.0625` e' `cb846b2a`: deve ridarlo AL
  BIT.**
- ### **LE LETTURE:**
  - ### **EPS E' LA MASSA** se ### **`c * Delta` costante entro `5%`** su tutti gli `eps > 0`, ### **`Delta` proporzionale a `eps` entro `5%`**, e ###
    **a `eps = 0` la dispersione a `k` piccolo LINEARE** *(`v_g(2)/v_g(1)` entro `5%` di `1`)*; ### **altrimenti NON E' LA MASSA, o PARZIALE coi
    numeri.**
  - ### **LA LUNGHEZZA SEGUE `c`** se il `k` misurato sta ### **entro `1` passo dal previsto per tutti e tre gli `eps`.**
  - ### **`c * Delta` *(o `v`)* la stessa a lato `32` e `64` entro `1%`.**
- ### **LA CONSEGUENZA, scritta e NON adottata** *(sez. `4` del mandato)*: ### **la regola di scala per `eps` che terrebbe fissa la dispersione
  fisica**, il confronto con ### **gli automi di Dirac** *(D'Ariano-Perinotti: la massa nella moneta, `m a -> 0` nel limite continuo)*, ### **e che
  cosa cambierebbe nei referti di `L2`.** ### **Una domanda per Luca.**

## 4. TODO

1. Questo task history, ### **committato DA SOLO.**
2. `csv/_moneta_massa.py --misura 1`: commit, corsa, ### **referto, commit.**
3. `--misura 2`: corsa, referto *(`doc/referti_l2/moneta_massa.txt` e `.jsonl` le due misure)*, la relazione con ### **la conseguenza e UNA
   domanda.**
