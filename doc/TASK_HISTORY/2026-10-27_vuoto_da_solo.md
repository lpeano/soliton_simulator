# IL VUOTO DA SOLO: E' INSTABILE PER CONTO SUO? *(il mandato breve del 2026-10-27, 02:43)*

> **Il mandato:** di Luca, `2026-10-27`, `02:43` *([[SOLITONE-VUOTO-CONGELATO]], [[CANALE-CS-SECONDA-SORGENTE]], [[PROGETTO-MASSA-COLLETTIVA]])*: ### **nel tick intero `Lambda` per estremita' sotto il solitone scende a `0.08`-`0.22`, LONTANO sale a `2.9`** *(`L 81`)* ### **e `5.1`** *(`L 120`)* ### **a `N 1e6`:** ### **`(1)` il vuoto RISPONDE alla materia, o `(2)` e' INSTABILE da solo?**
> ### **In memoria; nessun file del nucleo.** ### **Lo script `csv/_vuoto_da_solo.py`, il referto `doc/referti_l2/vuoto_da_solo.{txt,jsonl}`.** ### **PRIMA della corsa lunga di `C2`** *(fermata per questo)*.

**LIVELLO:** una misura dinamica col controllo.

## 0. LA STELLA POLARE

1. **`A14`:** ### **`V` si conserva** *(si controlla)*. 2. **Il gradino:** ### **il vuoto senza materia e' stazionario?** 3. **Aggiunge un numero o una legge?** ### **No.** 4. **Tocca `rho`, `c_s` o il segno?** ### **`cs` e' spento** *(`lambda_c None`, come nelle corse di allora)*. 5. **Emergente o imposto?** ### **La stabilita' del vuoto e' cio' che si misura.**

## 1. CHE COSA CI SI ASPETTA DALLA FORMA *(prima dei numeri)*

- ### **Con la materia a ZERO il legame non agisce** *(`rho = 0` da' fase nulla: `materia_vuoto`, `vivi = rho > 0`)*; ### **il vuoto uniforme per estremita' e' INVARIANTE sotto il Grover** *(il vettore uniforme ne e' autovettore)* ### **e sotto lo spostamento** *(i due capi uguali)*: ### **in aritmetica esatta resta uniforme; nei bit, salvo l'arrotondamento.** ### **`cs` e' spento: il canale di `cs` non agisce** *(la seconda sorgente di `CANALE-CS-SECONDA-SORGENTE` non c'e')*. ### **Quindi la previsione dalla forma e' la lettura `(1)`.**

## 2. LA MISURA *(fissata qui)*

- ### **Le scene di `74f99039`:** ### **i triangoli, `s 0.3`, `L 48, 69, 81, 120`, lo zero di oggi, il tick intero** *(`tick.percorri_tick`, `salta` vuoto, la forma `S1` in memoria come allora)*, ### **`T_MAX 2000`; la MATERIA A ZERO** *(`psi = 0`: lo strumento lo accetta)*; ### **il vuoto iniziale uniforme `VUOTO_PER_ESTREMITA`.**
- ### **Le misure ogni `20` tick:** ### **`Lambda` per estremita'** *(`Lambda_k/d_k`)*: ### **il minimo, il massimo, lo scarto quadratico medio sul toro; `V`;** ### **il primo tick in cui lo scarto supera `0.1` e `1`.**
- ### **IL CONTROLLO: lo stesso col vuoto CONGELATO** *(i pezzi del vuoto saltati e `phi` rimesso)*: ### **uniforme AL BIT.**
- ### **ACCANTO: i valori del tick intero col solitone di `74f99039`** *(`Lambda` lontano a `320` tick, dal suo jsonl)*.

| | il criterio | il tipo |
|---|---|---|
| `1` | ### **`V` conservato entro `1e-10` relativo** | DEVE |
| `2` | ### **il controllo: col vuoto congelato `Lambda` per estremita' uniforme AL BIT** | DEVE |
| `3` | ### **il vuoto da solo resta uniforme entro `1e-6` fino a `T_MAX`** *(lo scarto quadratico medio di `Lambda` per estremita'; allora la lettura e' la `(1)`)* | PUO' FALLIRE |

### **LA LETTURA:** ### **se lo scarto cresce, il tempo in cui arriva all'ordine `1` contro la vita del solitone** *(`320`, `140` tick)*. ### **Mi FERMO** ### **se `1` o `2` fallisce.**

## 3. TODO

1. questo task history, da solo; 2. lo script, committato prima della corsa *(i byte committati: scritto senza `CRLF`)*; 3. la corsa; 4. il referto, la relazione, l'indice.

## 4. IL RISULTATO *(dopo `58bc40c4`)*

### **IL REFERTO DEL VUOTO DA SOLO:** `doc/referti_l2/vuoto_da_solo.{txt,jsonl}` *(`csv/_vuoto_da_solo.py` al commit `58bc40c4`; il task history `7a115c93`)*. ### **`3/3`.**

- ### ⭐ **IL VUOTO DA SOLO E' STABILE, AL BIT:** ### **con la materia a zero e il tick intero, a `L 48, 69, 81, 120`, `Lambda` per estremita' resta `1.000000000` a ogni nodo per `2000` tick** *(lo scarto quadratico medio `0.0`; `V` esatto)*; ### **lo stesso col vuoto congelato** *(il controllo)*.
- ### **QUINDI LA LETTURA E' LA `(1)`: IL VUOTO RISPONDE ALLA MATERIA, non e' instabile per conto suo** *(e `cs` era spento: il canale di [[CANALE-CS-SECONDA-SORGENTE]] non c'entra qui)*. ### **Le salite di `Lambda` lontano nelle corse col solitone** *(`2.34` / `0.80` a `320` tick, `2.91` / `5.14` alla fine, `N 1e6`)* ### **sono ONDE DEL VUOTO partite dalla buca sotto la materia** *(il centro `2.12` a `320` tick, `0.08` / `0.22` alla fine)*, ### **non il vuoto che si disfa da solo.**
- ### **LA STRADA CHE NE VIENE** *(la lettura del guardiano, non una scelta)*: ### **l'oggetto giusto e' il solitone CON la sua buca: lo stato stazionario dei due insieme** *(materia e vuoto),* ### **non il solitone del risolutore col vuoto fisso.**
