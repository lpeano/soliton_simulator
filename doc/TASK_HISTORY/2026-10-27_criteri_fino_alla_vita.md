# I CRITERI `2` E `3` DEL CONTO DELL'ENERGIA DEL LEGAME, FINO ALLA VITA; LA DIFFERENZA FRA I DUE ZERI NEL TEMPO; LA LUCE *(la parte 1 del mandato dopo `15df5c63`)*

> **Il mandato:** ### **la parte 1 del mandato dopo `15df5c63`** *(la risposta di Luca delle `12:37` alla domanda 1 di `15df5c63`; [[ENERGIA-DEL-LEGAME]], [[PROGETTO-MASSA-COLLETTIVA]])*: ### **i criteri `2` (le taglie) e `3` (i due zeri) valgono FINO ALLA VITA del solitone** *(`320` tick a `N 1e6`, `140` a `N 1e5`)*: ### **riscritti cosi', come CORREZIONE DICHIARATA DOPO I NUMERI** *(la lezione di `0fb93b8c`)*, ### **e rivalutati sul jsonl.** ### **Il controllo in piu': la differenza fra i due zeri nel tempo** *(tick intero, `N 1e5` `L 48`)* ### **dalla vita a `T_MAX`: cresce in modo regolare dall'arrotondamento?** ### **E la luce in queste unita'.**
> ### **Nessuna corsa nuova:** ### **lo script legge `doc/referti_l2/energia_del_legame.jsonl`** *(`csv/_energia_del_legame.py` `0197ecc0`; la serie ogni `10` tick)*.

**LIVELLO:** una rivalutazione su dati gia' committati.

## 0. LA STELLA POLARE

1. **`A14`:** ### **l'energia contata nei due zeri.** 2. **Il gradino:** ### **dove finisce il confronto fra le taglie e fra gli zeri.** 3. **Aggiunge un numero o una legge?** ### **No.** 4. **Tocca `rho`, `c_s` o il segno?** ### **No.** 5. **Emergente o imposto?** ### **Nessuna fisica nuova.**

## 1. CHE COSA CREDO PRIMA DI GUARDARE, E CHE COSA NON SO

- ### **Gia' visto** *(`energia_del_legame_dove.txt`, `f266d9bb`)*: ### **ALLA VITA il criterio `2` e' `7.53e-6` e `1.20e-6`, il `3` e' `8.9e-14` e `3.9e-14`;** ### **a `T_MAX` `1.98e-3` e `1.63e-4`.** ### **Quindi credo `5/5` coi criteri corretti** *(lo dichiaro: la correzione e' DOPO i numeri, su decisione di Luca)*.
- ### ⚠ **NON HO VISTO** ### **i punti INTERMEDI della serie** *(ogni `10` tick)*: ### **la diagnosi guardava solo la vita e `T_MAX`.** ### **Il criterio «fino alla vita» lo leggo come il MASSIMO su `t <= vita`, non solo a `t = vita`** *(piu' severo)*.
- ### ⚠ **NON SO** ### **come cresce la differenza fra gli zeri dopo la vita:** ### **un esponenziale da `1e-14` a `1.6e-4` in `1860` tick darebbe un tasso intorno a `0.01` per tick** *(una stima a occhio, NON un numero del referto)*; ### **ma puo' anche saltare alla rottura e poi saturare.**

## 2. LA PROGETTAZIONE *(le letture fissate qui, prima di vedere la serie)*

1. ### **IL CRITERIO `2` CORRETTO:** ### **`max_{t <= vita} max_pezzo |Delta E_pezzo(L1, t) - Delta E_pezzo(L2, t)| / (N |e_K(0)|) <= 1e-3`** *(il totale di ogni pezzo, per ogni `N`, zero e modo)*. **DEVE.**
2. ### **IL CRITERIO `3` CORRETTO:** ### **`max_{t <= vita} max_{regione, pezzo} |Delta E(simm) - Delta E(oggi) - 2 pi (1/2) Delta norma| / (N |e_K(0)|) <= 1e-6`** *(come in `_energia_del_legame_dove.py`)*. **DEVE.**
3. ### **LA DIFFERENZA FRA I DUE ZERI NEL TEMPO** *(`g(t)`, il peggiore su regioni e pezzi, `N 1e5` `L 48` tick intero; e, come confronto, le altre tre corse col tick intero)*: ### **il fit ai minimi quadrati di `ln g` contro `t` su `[vita, T_MAX]`: il tasso `r` per tick e `R^2`.** ### **LA LETTURA «REGOLARE»: `R^2 >= 0.9` E nessun salto** *(nessun passo di `10` tick in cui `log10 g` cresce di piu' di `1`)*. ### **Altrimenti si descrive l'andamento** *(i salti, dove; il tasso nella prima e nella seconda meta')*. ### **E' una LETTURA, non un criterio.**
4. ### **I CONTROLLI DELLO STRUMENTO DEL FIT** *(la regola del controllo di scala)*: ### **`(p1)` un esponenziale sintetico `1e-14 e^{0.01 t}` col rumore relativo del `10%`: ridà `r` entro il `5%` e `R^2 >= 0.9`** *(DEVE)*; ### **`(p2)` un gradino** *(`1e-14` fino a `t 500`, poi `1e-5`)*: ### **la lettura dice «NON regolare»** *(DEVE)*.
5. ### **LA LUCE:** ### **`c = s = 0.30` archi per tick a `s 0.3`** *(`0764d566`: `c = r s`, `r = 1` sul piatto)*; ### **il fronte di ogni corsa** *(`velocita_fronte` del jsonl)* ### **e `v_max` della coppia** *(`0.183601`)* ### **divisi per `c`, stampati dallo script.**

### **Mi FERMO** ### **se `(p1)` o `(p2)` fallisce** *(lo strumento del fit non legge)*, ### **o se un criterio corretto fallisce** *(allora il «fino alla vita» non basta, e lo dico a Luca)*.

## 2-bis. ANNOTAZIONE, PRIMA DELLA CORSA *(un controllo della pairing sul jsonl, NON una misura)*

- ### **LA VITA DI `N 1e5` COL TICK INTERO:** ### **il campo `vita` del jsonl** *(la risoluzione `10` tick)* ### **e' `130`; `vita20`** *(la risoluzione `20` tick di `74f99039`)* ### **e' `140`, il numero del mandato.** ### **Uso `140`** *(il mandato, e il massimo su piu' punti: il piu' severo)*; ### **lo script lo controlla contro `vita20`.**

## 3. TODO

1. questo task history, da solo; 2. lo script `csv/_criteri_fino_alla_vita.py`, committato prima della corsa; 3. la corsa; 4. il referto, la relazione, l'indice (`ENERGIA-DEL-LEGAME`).
