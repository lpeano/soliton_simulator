# IL VUOTO DA SOLO CON UN DISTURBO: STABILE, O SOLO STAZIONARIO? *(il mandato breve del 2026-10-27, 08:59, parte 2)*

> **Il mandato:** di Luca, `2026-10-27`, `08:59` *([[VUOTO-DA-SOLO]], [[CANALE-CS-SECONDA-SORGENTE]], [[SOLITONE-VUOTO-CONGELATO]])*: ### **errore del guardiano `n.72`: un vuoto uniforme al bit su un reticolo regolare e' STAZIONARIO PER SIMMETRIA;** ### **`e9e42332` non distingue <<stabile>> da <<stazionario>>.** ### **Le stesse scene con un disturbo casuale del vuoto, ampiezza relativa `1e-6`,** ### **`cs` spento e `cs` acceso.**
> ### **In memoria; nessun file del nucleo.** ### **Lo script `csv/_vuoto_disturbato.py`, il referto `doc/referti_l2/vuoto_disturbato.{txt,jsonl}`.**
> ### ⚠ **IL PROCESSORE E' CONDIVISO** ### **con la corsa della materia di `C2`, che non si ferma:** ### **i tempi di tutte e due ne risentono.**

**LIVELLO:** una misura dinamica col controllo nullo.

## 0. LA STELLA POLARE

1. **`A14`:** ### **`V` si conserva** *(si controlla)*. 2. **Il gradino:** ### **il vuoto uniforme e' STABILE** *(un disturbo piccolo resta piccolo)* ### **o solo stazionario?** 3. **Aggiunge un numero o una legge?** ### **Un seme e un'ampiezza, dichiarati dal mandato:** ### **sono la misura, non la fisica.** 4. **Tocca `rho`, `c_s` o il segno?** ### **`cs` e' una delle due serie.** 5. **Emergente o imposto?** ### **La crescita del disturbo e' cio' che si misura.**

## 1. CHE COSA CI SI ASPETTA DALLA FORMA *(prima dei numeri)*

- ### **Con la materia a zero e `cs` SPENTO** *(serie `(i)`)*: ### **il vuoto e' un cammino quantistico LINEARE** *(il Grover e lo spostamento; il legame vuole `rho > 0`)*: ### **unitario, quindi il disturbo NON CRESCE in norma;** ### **lo scarto di `Lambda` per estremita' puo' oscillare** *(il disturbo si sparge in onde)* ### **ma resta dell'ordine del disturbo iniziale.** ### **Previsione: (i) stabile, lo scarto `~1e-6`.**
- ### **Con `cs` ACCESO** *(serie `(ii)`)*: ### **il tempo proprio dipende da `Lambda`** *(`cs = Lambda/(Lambda + Lambda_c)`)*, ### **e `CAMM-FASE-VUOTO` porta `cs'(Lambda)`:** ### **il vuoto diventa NON LINEARE, e una crescita e' possibile.** ### ⚠ **COSA NON SO:** ### **se cresce, e quanto.** ### **Il riferimento** *(`974d411a`, `R1` con `cs`, `S1`: `0.402`)* ### **era sul QUADRATO, CON la materia** *(`x 0.1`)*, ### **in unita' di `N dtau`:** ### **e' un confronto di ordine di grandezza, non una previsione.**

## 2. LA MISURA *(fissata qui)*

- ### **Le scene di `e9e42332`:** ### **i triangoli, `s 0.3`, `L 48, 69, 81, 120`, lo zero di oggi, il tick intero, la forma `S1` in memoria, la materia a zero, `T_MAX 2000`, `dtau 1`.**
- ### **IL DISTURBO:** ### **`phi_e <- phi_e (1 + 1e-6 xi_e)` per estremita', `xi_e` normale standard reale,** ### **il seme `20261027`** *(`numpy.random.default_rng`)*. ### **`V0` si legge DOPO il disturbo.**
- ### **(i) `cs` SPENTO:** ### **`mot.cs = s`, `lambda_c None`, `tick.percorri_tick`** *(come nelle corse del solitone)*.
- ### **(ii) `cs` ACCESO:** ### **`tick.tick_con_cs`** *(il `cs` simmetrico al centro del palindromo, `D2`)* ### **con `Lambda_c` = la media di `Lambda` per nodo a `t 0`** *(il rapporto `1`, come `lambda_c_di` di `_collauda_cs_l1` con `RAPPORTO 1`)*. ### ⚠ **Quindi il tempo proprio uniforme passa da `0.3` a `cs = 1/2`:** ### **e' la forma, non una scelta; lo si dichiara.**
- ### **Le misure ogni `20` tick:** ### **lo scarto quadratico medio di `Lambda` per estremita'** *(`Lambda_k / d_k`)*, ### **`V`, il primo tick oltre `0.1` e oltre `1`;** ### **il tasso: la pendenza di `log(scarto)` contro `t`** *(minimi quadrati, su tutta la serie e sulla seconda meta')*.
- ### **IL CONTROLLO NULLO** *(il caso che deve dare zero)*: ### **la serie `(ii)` SENZA disturbo a `L 48`:** ### **lo scarto resta `0` AL BIT** *(se cresce, la crescita non viene dal disturbo)*.
- ### **LA CONVERSIONE per `974d411a`:** ### **`dtau = 1`, quindi il tasso per tick e' il tasso per unita' di `N dtau`.**

| | il criterio | il tipo |
|---|---|---|
| `1` | ### **`V` conservato entro `1e-10` relativo** *(ogni corsa)* | DEVE |
| `2` | ### **il controllo nullo:** ### **`cs` acceso senza disturbo, `L 48`, lo scarto `0` al bit per `T_MAX`** | DEVE |
| `3` | ### **`(i)` `cs` spento: lo scarto non supera `1e-5` fino a `T_MAX`, a ogni `L`** *(il vuoto stabile)* | PUO' FALLIRE |

### **LA LETTURA:** ### **con `cs` acceso, il tasso contro `0.402`;** ### **se `(i)` o `(ii)` crescono, il tempo all'ordine `1` contro la vita del solitone** *(`320` e `140` tick)*. ### **Mi FERMO** ### **se `1` o `2` fallisce.**

## 3. TODO

1. questo task history, da solo; 2. lo script, committato prima della corsa *(scritto in binario, senza `CRLF`)*; 3. la corsa, in parallelo a `C2`; 4. il referto, la relazione, l'indice.
