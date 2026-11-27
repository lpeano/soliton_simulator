# 2026-11-27 -- [M2245] (del 27/11, DECISIONE DI LUCA 22:45 e 22:47): LE CINQUE LETTURE, IL MERGE lapse-u -> mitosi, IL CORPO FUSO CON LE NASCITE, IL «VIA» A [M-GM], LA NASCITA NEL VUOTO CON IL LAPSE [[PROGETTO-MITOSI]]

**La lettera:** `origin/guardiano:guardiano/posta/2026-11-27_2245_M2245.md`, letta alle `22:47` su comando di Luca («Leggi la posta.»), insieme a `ATTESA_M-GM_esperimento_gravitomagnetico.md` (la versione corretta delle 22:20) e a `guardiano/CODA.md`.

**L'etichetta e' gia' usata.** Esisteva gia' un [M2245] del 24/11 (il vento del vuoto, i commit `91de626d`..`8e90c3d5`), e `git log --all --grep "[M2245"` trova quelli.
- **Del mandato del 27/11 non e' fatto niente.**
- Nei commit lo scrivo **`[M2245] (27/11)`** e i pezzi **`[M2245-A1]`..`[M2245-F]`**, con la data nel titolo.

## 1. LE PREMESSE DAL CODICE *(prima di guardare; cosa NON so)*

- **Il nucleo:** `git diff --name-only 42638304` da' 5 file su `origin/lapse-u` e 9 su `origin/mitosi`.
  - Da `d27805ac`, la base del merge [M1330-A2], **lapse-u non ha toccato `primo_ordine/`**: 0 file.
  - **Quindi il merge dovrebbe lasciare il nucleo a 9 file senza conflitti nel nucleo.** I conflitti attesi sono nella documentazione: la relazione, il registro, l'inventario, la coda.
- **Le distanze:** mitosi e' 168 commit dietro `origin/lapse-u` e 99 avanti. Il worktree `E:/soliton_lavoro/wt_mitosi` e' pulito, a `82739c06`.
- **La fiammata:** e' `MITOSI_V2`, con `538` nascite fra `k 35976` e `45949`.
  - Tutti i `DH` sono negativi, `-somma DH = E_persa` al bit (`mitosi_energia_fiammata.txt`, [M0237-2]).
  - **Dove stanno i registri delle nascite e la serie `n(k)` non lo so ancora:** lo leggo dal ramo mitosi (`mitosi_dati.py`, `doc/referti_l2/nascite/`).
- **I triangoli «tre sfasate» (A4):** **non so** se ci sono stati con `chi` acceso, ne' dove. Lo cerco, e se non ci sono uso quelli che ci sono, dichiarandolo (lo permette la lettera).
- **Il vento a due corpi (A5):** `M2034/coppia/d1`, da `0` a `6000`, c'e'. La lettura di `J_phi` per anello esiste gia' in forma vicina (`vento_vuoto_v3.py` e il vuoto del giro 3 di [M2034-A]).
- **Un conflitto fra la lettera e CLAUDE.md par. 2:** B2 dice «i due collaudi con repository temporaneo su C: come gia' dichiarato». La DECISIONE DI LUCA delle 18:59, che e' successiva, dice **«C: MAI (ne' temp)»**.
  - **Prevale CLAUDE.md:** `TMP`/`TEMP` su `E:\soliton_lavoro\tmp`. Lo dichiaro.
  - **Non so** se i due collaudi creano il repository temporaneo con `tempfile`: in quel caso basta `TMP`. Se il percorso e' cablato su C:, FERMO su B2 e lo dico.
- **[M-GM] (D):** richiede un ramo nuovo, `u-dinamica`, e un worktree `E:/soliton_lavoro/wt_u_dinamica`.
  - CLAUDE.md par. 2 elenca solo `wt_lapse_u` e `wt_mitosi`: **la riga va aggiornata** nello stesso commit della creazione (gestione autorizzata dalla decisione delle 22:45, D3).
  - **Il pezzo 0 di [M-GM] e' A4.**
- **Il tempo:** ogni corsa di C e F e' di 12000 e 6000 tick. Con le nascite accese MITOSI_V2 faceva circa 7.5 s per tick: **C e F sono ore o una notte.**

## 2. PROGETTAZIONE DEL RAGIONAMENTO

**L'ORDINE, e una scelta mia dichiarata qui:** la lettera elenca A prima di B, ma **faccio B prima di A**.
- **Il perche':**
  - A1-A3 leggono i dati e gli strumenti della mitosi, che stanno sul ramo `mitosi`;
  - A4-A5 leggono gli strumenti di lapse-u (chi v2, la coppia, `coppia_a0`);
  - «una sezione di carta per tutte e cinque» sta in **un** file, `doc/CARTA_mitosi.md` sul ramo mitosi, e solo dopo il merge i due insiemi di strumenti sono sullo stesso albero.
- **Se B fallisce** (il nucleo oltre 9 file, la suite sotto 67, il caso noto delle nascite non al bit): FERMO su C, D ed F. Faccio A con A1-A3 su mitosi e A4-A5 su lapse-u, e lo dichiaro.

**I passi, che cosa decide ciascuno e cosa mi fa fermare:**

1. **E-0, la ricevuta «letta»** (questo file e la relazione, su lapse-u). Commit e push.
2. **B1, il merge:** `git merge origin/lapse-u` in `wt_mitosi`, senza squash e senza rebase.
   - Nei conflitti di documentazione si tengono tutte e due le parti, come in [M1330-A2].
   - **DEVE:** `git diff --name-only 42638304 HEAD -- primo_ordine/` = esattamente i 9 file del criterio. **Altrimenti FERMO, senza committare.**
3. **B2:** `python primo_ordine/collauda.py` nel worktree mitosi deve dare **67 su 67**, poi il caso noto delle nascite dal tronco (`k 35976 -> 36000` al bit), con lo script che lo provo' allora (lo cerco per nome). **FERMO** se uno dei due fallisce.
4. **B3:** il commit del merge e il push su `mitosi`. **Da qui C, D ed F girano su mitosi**, e D su `u-dinamica`.
5. **A, la carta:** una sezione in `doc/CARTA_mitosi.md` con le cinque letture.
   - **Per ciascuna:** il fit o il test dichiarato **prima** e i casi noti.
   - **Le soglie che fisso io (criteri dentro il mandato):**
     - A1: «costante» se la pendenza di `DH` contro `n` e contro la densita' e' compatibile con zero a 2 sigma, «lineare» se il fit lineare ha residui senza struttura;
     - A3: «a gradini» con il rapporto varianza/media sopra 2 in oltre meta' delle finestre. E' la soglia del guardiano, e la adotto dichiarandola.
   - Poi gli script, uno per lettura, e i referti. **Commit e push dopo ogni lettura.**
6. **A4 decide D:** se nessun triangolo ha un giro di fase intero, [M-GM] si ferma li' (D4).
7. **C:** la carta (C1), poi `corpo_fuso_mitosi.py` con K0, K1 e K2 (C2), poi la corsa in coda, un processo (C3).
   - **Prima di ogni lancio:** l'impegnabile libero sopra 8 GB, letto e scritto nella riga del registro.
8. **D:** il ramo `u-dinamica` con il suo worktree e la sua `safe.directory`, e CLAUDE.md par. 2 aggiornato. Poi la carta di [M-GM] con S1-S4 confermate e `e_A` scritta, il codice, K1-K4, P1, P2, P3: **una corsa alla volta**.
   - **Se A serve nel nucleo:** la carta dichiara PRIMA quali file cambiano.
9. **F:** la carta, `vuoto_lapse_mitosi.py`, il controllo con il lapse piatto (= [M0106] al bit sui primi 250 tick), poi la corsa in coda dopo C.
   - **Al massimo tre processi:** C, F e una corsa di [M-GM].
10. **E:** `doc/TODO_prossima_sessione_2026-11-27.md` allineato a `guardiano/CODA.md`, con le voci chiuse marcate e il perche'; la ricevuta [M2245] e le previsioni confrontate.

**I limiti di processo:** il tetto e' 10, il freno a 4 GB, e prima di ogni lancio l'impegnabile libero deve stare sopra 8 GB. **Il lanciatore e la coda sono quelli della cartella del ramo che lancia**, cioe' `coda_m1446.py` dal worktree.

## 3. TODO DEL NEXT STEP

- [ ] E-0: questo file e la ricevuta «letta» nella relazione; commit e push su lapse-u
- [ ] B1: il merge in `wt_mitosi`; DEVE il nucleo a 9 file
- [ ] B2: `collauda.py` 67/67 (TMP su E:); il caso noto delle nascite al bit
- [ ] B3: commit e push su mitosi
- [ ] A: la carta delle cinque letture (CARTA_mitosi.md); commit e push
- [ ] A1 `mitosi_costo_nodo.txt` · A2 `mitosi_a_di_k.txt` · A3 `mitosi_ritmo.txt` · A4 `triangoli_vortice.txt` · A5 `vento_due_corpi.txt`; commit e push dopo ognuno
- [ ] C1-C2: la carta, `corpo_fuso_mitosi.py`, K0-K2; C3 la corsa in coda
- [ ] D: `u-dinamica` con il worktree e CLAUDE.md par. 2; la carta di [M-GM]; il codice; K1-K4; P1 -> P2 -> P3
- [ ] F: la carta, `vuoto_lapse_mitosi.py`, il controllo con il lapse piatto, la corsa in coda dopo C
- [ ] C4 e F3: i verdetti a corse chiuse
- [ ] E: il TODO allineato a CODA; la ricevuta [M2245] con le previsioni confrontate; poi FERMO
