# REFERTO -- `Z43` CURA (2): **il tempo proprio viene da `cs`**

*(Decisione di Luca del 2026-10-05: `r = cs_nodo / CS_M`, esponente `p = 1`, <<orologio a luce>>. I **sette criteri** sono fissati in `doc/TASK_HISTORY/2026-10-05_z43-cura2-r-da-cs.md`, committato **prima** del codice in `012f419`.)*

| | |
|---|---|
| **simulatore** | `f7237563`, da `ca3cdd8a` *(che e' la `PARTE A` `062172d3` **piu' un solo commento**)* |
| **patch** | `b343e354` | 
| **strumento** | `5461b850` |
| **piattaforma** | Windows 11, python `3.13.2`, numpy `2.3.0`, `AMD64` |
| **passi** | `150` |
| **configurazione del driver dichiarata INTERA** | `True` *(sul braccio `B`, il CURATO: il braccio `A` e' il vecchio e sarebbe fuori configurazione **per costruzione**)* |

## IL VERDETTO

| criterio | che cosa pretendeva | esito |
|---|---|---|
| **`0`** | il *prima* + la patch = il blob di oggi, al byte | **PASSA** |
| **`1`** | `r == _cs_nodo_prev / CS_M` **AL BIT** | **PASSA** |
| **`2`** | niente altalena, **`<= 1.2` su OGNI coppia dal passo `3`** | **PASSA** |
| **`3`** | autocorrelazione a ritardo `1` **`>= -0.50`** | **PASSA** |
| **`4`** | `r` materia `<` `r` vuoto -- ### **FEDELTA', non fisica** | si riporta |
| **`5`** | localita', **misurata** | si riporta |
| **`6`** | lo stato **DEVE** divergere dalla `PARTE A` | **PASSA (lo STATO dal passo 2)** |
| **`7`** | `150` passi senza `FERMO` | **PASSA** |

> ### **ESITO COMPLESSIVO: `TUTTI I CRITERI CHE FERMANO PASSANO`**

## CRITERIO `1` -- **FEDELTA' AL BIT**

| | |
|---|---|
| chiamate col ramo di legge | `149` |
| nodi confrontati | `1907888` |
| nodi **diversi** | `0` |
| max scarto | `0.000000e+00` |

**La legge e' quella dichiarata**, su `1907888` nodi e `149` chiamate, **senza un ulp di scarto**. E non e' una verifica a vuoto: il confronto gira sul valore **restituito da `ritmo()`** e sul `_csp` che ha **davvero** letto -- dopo il passo `_cs_nodo_prev` e' **gia' stato riscritto nello stesso passo**, quindi da fuori quella verifica **non si puo' fare**.

## CRITERIO `2` -- **NIENTE ALTALENA, PER COPPIA DI PASSI**

*(La correzione del guardiano, `b337ec1`: l'aggregato su `150` passi **nasconde l'inizio**.)*

| coppia | `r` dispari | `r` pari | rapporto | a DUE lati |
|--:|--:|--:|--:|--:|
| `4` | `8.355026e-01` | `8.290727e-01` | **`1.007756`** | `1.007756` |
| `10` | `8.224743e-01` | `8.207982e-01` | **`1.002042`** | `1.002042` |
| `20` | `8.124330e-01` | `8.112945e-01` | **`1.001403`** | `1.001403` |
| `30` | `8.039747e-01` | `8.031230e-01` | **`1.001061`** | `1.001061` |
| `40` | `7.985503e-01` | `7.985382e-01` | **`1.000015`** | `1.000015` |
| `60` | `7.976762e-01` | `7.978742e-01` | **`0.999752`** | `1.000248` |
| `100` | `8.099757e-01` | `8.103005e-01` | **`0.999599`** | `1.000401` |
| `140` | `8.145234e-01` | `8.144660e-01` | **`1.000070`** | `1.000070` |

| | |
|---|---|
| coppie totali | `75` |
| coppie **ESCLUSE** *(cache di `cs` non allineata)* | `1` |
| coppie valutate dal passo `3` | `74` |
| coppie **sopra `1.2`** | **`0`** |
| primo passo da cui resta `<= 1.2` | **`4`** |
| rapporto **massimo** fra le valutate | `1.007756` *(coppia `4`)* |
| a **DUE lati**, `max(r, 1/r)` massimo | `1.007756` *(coppia `4`)* |
| sopra `1.2` **a due lati** | `0` coppie |

* **ESCLUSA la coppia `2`:** la cache di cs NON e' allineata: r = 1 per SICUREZZA

> ### E LE ESCLUSIONI SONO **CONTATE E DICHIARATE**, non nascoste: sono le coppie in cui `r = 1` **per SICUREZZA e non per legge** *(la cache di `cs` non c'e' o non e' allineata)*, e **un rapporto fra due `1` non dice niente sull'altalena.** Il loro **numero** si', e per questo e' qui.

> ### E UNA COSA CHE IL CRITERIO, COME E' SCRITTO, NON VEDE -- e la riporto **accanto** invece di sostituirla: `<= 1.2` e' **a UN LATO SOLO**. Un'alternanza in cui il passo **dispari** e' piu' BASSO del pari da' un rapporto `< 1` e **passerebbe**, pur essendo un'altalena. ### **Il criterio e' di Luca e non lo reinterpreto:** applico quello, e la colonna <<a due lati>> e' la lettura completa.

> ### E UNA COSA CHE QUESTO CRITERIO HA IN MENO DELLA `PARTE A`, e la dico invece di lasciarla credere: ### **PER LA `PARTE B` C'E' UN SOLO STRUMENTO.** Nella `PARTE A` il rapporto per coppia era misurato **da due strumenti su due piattaforme** -- il mio e quello del guardiano su Linux -- e **coincidevano fino alla terza cifra**. Qui no, e il perche' e' nel codice: `csv/_test_fork/_z43_tempo_proprio.py` esce dal suo `_ritmo_in` appena `_med_f_prec is None` *(<<il ramo di sicurezza>>)*, e da questa cura ### **`_med_f_prec` e' None SEMPRE.** ### **Quello strumento misura la legge VECCHIA, e sul blob nuovo non vedrebbe niente** -- rigirarlo darebbe `150` record vuoti, non una seconda misura. ### **Non l'ho rigirato, e non spaccio il criterio per confermato due volte.**

## CRITERIO `3` -- **AUTOCORRELAZIONE A RITARDO `1`**, e l'anello ha **DUE** cammini

*(Annotazione del guardiano, 2026-10-05.)* L'anello non e' uno:

1. `cs -> r -> dt_e -> cs`;
2. `r -> _dts dell'orologio -> fase di _psi_spinor -> interferenza in psi -> abs(psi)^2 -> cs -> r`.

### E L'AUTOCORRELAZIONE **LI VEDE SOMMATI, non li distingue:** se oscillasse, il passo dopo sarebbe **capire quale dei due**.

| | |
|---|---|
| serie usata | dal passo `2`, `149` punti *(esclusa la coda iniziale con la cache non allineata)* |
| **autocorrelazione a ritardo `1`** | **`0.891635`** |
| soglia *(**la scelgo io**)* | `-0.50` |

**La soglia `>= -0.50` l'ho scelta io**, e lo dichiaro: il mandato diceva <<non fortemente negativa>> **senza un numero**. L'ho fissata **prima di vedere i dati** -- un'alternanza perfetta a periodo `2` da' `-1`, e `-0.5` e' il punto di mezzo. ### **Il numero si riporta comunque, qualunque sia il verdetto.**

## LA DISTRIBUZIONE DI `r` -- e la **SEPARAZIONE** fra la parte UNIFORME e quella che VARIA

> ### UNA RIGA DEL MIO TASK HISTORY ERA **FALSA**, e il guardiano l'ha corretta: *<<`cs = CS_M` -> `r = 1`, il tempo proprio coincide con quello coordinato **dove la metrica non e' deformata**>>*. ### **E' FALSO.** Da `_cs_nodo`, `cs = CS_M` **SOLO se `I = 0`**; per ogni `I > 0` si ha `cs_floor < CS_M`, e la transizione `0.5*(1 + tanh(1 - u))` vale **`<= 0.880797`** a `u = 0` e **`0.5`** a `u = 1` *(vuoto uniforme)*. ### **Quindi NESSUN nodo con campo ha `r = 1`: il limite `r = 1` e' L'ASSENZA DI CAMPO, non <<la metrica non deformata>>.**
>
> **E la convergenza va detta intera:** la parte aritmetica l'avevo trovata anche io scrivendo il codice -- la docstring del simulatore dice gia' `0.880797` e <<SOLO dove `I = 0`>> -- ### **ma non ero tornato a correggere il task history, e il guardiano e' arrivato prima di me.** La riga resta dov'e' *(par.8: **si ANNOTA, non si riscrive**)*.

| passo | `r` q01 | `r` q25 | **`r` MEDIANO** | `r` q75 | `r` q99 | `r` max | `r > 1` |
|--:|--:|--:|--:|--:|--:|--:|--:|
| `2` | `0.497257` | `0.705016` | **`0.853423`** | `0.938849` | `0.992533` | `0.998982` | `0` |
| `3` | `0.457769` | `0.679477` | **`0.835503`** | `0.931092` | `0.991036` | `0.999720` | `0` |
| `4` | `0.444945` | `0.662943` | **`0.829073`** | `0.926087` | `0.990115` | `0.998981` | `0` |
| `5` | `0.445182` | `0.663725` | **`0.828354`** | `0.925817` | `0.990336` | `0.999418` | `0` |
| `10` | `0.445523` | `0.662342` | **`0.820798`** | `0.922285` | `0.990010` | `0.999645` | `0` |
| `20` | `0.447493` | `0.660504` | **`0.811295`** | `0.915230` | `0.989201` | `0.999051` | `0` |
| `50` | `0.464845` | `0.664610` | **`0.797504`** | `0.902039` | `0.987052` | `0.999025` | `0` |
| `100` | `0.458328` | `0.673703` | **`0.810300`** | `0.909104` | `0.987571` | `0.999411` | `0` |
| `150` | `0.433408` | `0.676198` | **`0.815126`** | `0.912862` | `0.988441` | `1.000000` | `0` |

| passo | **UNIFORME** *(`r` mediano)* | **VARIA**: `CV` | `q95/q05` | `max/min` |
|--:|--:|--:|--:|--:|
| `2` | `0.853422599` | `0.176883` | `1.809270` | `2.417668` |
| `3` | `0.835502596` | `0.188237` | `1.855332` | `3.208931` |
| `4` | `0.829072668` | `0.195317` | `1.880329` | `3.281319` |
| `5` | `0.828353877` | `0.194750` | `1.873493` | `3.270809` |
| `10` | `0.820798176` | `0.193392` | `1.865670` | `3.211570` |
| `20` | `0.811294520` | `0.190007` | `1.843831` | `3.088452` |
| `50` | `0.797504429` | `0.179946` | `1.801668` | `2.792407` |
| `100` | `0.810300492` | `0.178567` | `1.792621` | `2.879259` |
| `150` | `0.815126366` | `0.186746` | `1.875136` | `3.176363` |

> ### LA SEPARAZIONE, al passo `150`:
> * **la parte UNIFORME** e' `r` mediano `= 0.815126`, cioe' ### **IL PASSO MEDIO RALLENTA DI UN FATTORE 0.815126.** ### **NON E' FISICA: e' un CAMBIO DI UNITA' DI TEMPO**, e si potrebbe riassorbire ridefinendo `DT`;
> * **la parte che VARIA fra nodi** e' l'unica **FISICA**: `CV = 0.186746`, `q95/q05 = 1.875136`, `max/min = 3.176363`.
>
> ### **E `r > 1` su `0` nodi in tutta la corsa**: se non fosse ZERO, la forma sarebbe violata.

**L'ATTESO ERA SCRITTO PRIMA DELLA CORSA**, e viene da una **misura**: `C5` di `66a798d` dava `(cs/CS_M)^2` mediano `0.6457`, quindi `cs/CS_M` mediano `~0.8036`. ### **MISURATO: `0.815126`** *(al passo `150`)*, scarto relativo `1.440 %`.

## CRITERIO `5` -- **LOCALITA', MISURATA e non presunta**

*(Il primo criterio di sigillo di questo repo che misura la **localita'** di una legge. Chiama **`_cs_nodo` -- la legge stessa, non una copia** -- due volte.)*

| | |
|---|---|
| `stato` | `fatto` |
| `passo_di_I` | `10` |
| `n` | `12802` |
| `uno_su_n` | `7.811279487580065e-05` |
| `mean_I` | `2.688007332224694` |
| `nodo_perturbato` | `11316` |
| `I_del_nodo` | `20.131765297140973` |
| `perturbazione` | `I del nodo piu' denso RADDOPPIATO (x2: un fattore, non un numero)` |
| `contatore_prima` | `None` |
| `contatore_dopo` | `None` |
| `contatore_mosso` | `False` |
| `contatore_ripristinato` | `None` |

| distanza sul grafo | nodi | mediana `\|dcs\|/cs` | max | **mediana / (1/n)** |
|--:|--:|--:|--:|--:|
| `0` | `1` | `5.526207e-01` | `5.526207e-01` | **`7074.6498`** |
| `1` | `87` | `7.778896e-03` | `4.645756e-02` | **`99.5854`** |
| `2` | `448` | `5.392324e-05` | `1.770860e-04` | **`0.6903`** |
| `3` | `1178` | `3.120080e-05` | `1.685825e-04` | **`0.3994`** |
| `4` | `1799` | `3.476554e-05` | `1.827623e-04` | **`0.4451`** |
| `5` | `2168` | `3.871237e-05` | `1.796703e-04` | **`0.4956`** |
| `6` | `2375` | `3.959716e-05` | `1.805882e-04` | **`0.5069`** |
| **`oltre 6_salti`** | `4746` | `3.295734e-05` | `1.793079e-04` | **`0.4219`** |

> ### E SI RIPORTA **IN FUNZIONE DELLA DISTANZA, non come un numero solo:** ### **un numero solo non distingue <<locale piu' una coda globale>> da <<globale>>.** La **forma della curva** lo fa, e l'ultima colonna e' il confronto col `1/n` atteso da `CS-LAMBDA-GLOBALE`.

> ### E LA MISURA **NON HA MOSSO CIO' CHE MISURA:** `mean(I) > 1e-30` verificato **PRIMA** di chiamare, e `_cs_lam_degenere` **salvato e ripristinato** *(`contatore_mosso = False`, `contatore_ripristinato = None`)*.

## CRITERIO `4` -- `r` materia `<` `r` vuoto: ### **E' FEDELTA', NON FISICA**

> *(Annotazione del guardiano, 2026-10-05, e la applico alla lettera.)* `r` materia `<` `r` vuoto ### **SEGUE DALLA FORMULA di `_cs_nodo`**: `cs_floor = CS_M/(1 + sqrt(I)*sqrt(1/scala))` **decresce in `I`**, e la transizione `0.5*(1 + tanh(1 - u))` pure. ### **Quindi puo' fallire SOLO se il codice e' sbagliato:** e' un `FALSO-UNO` in attesa, **non una predizione messa alla prova**. ### **NON si rivendica come conferma della fisica.**

| passo di `r` | nodi materia | `r` mediano **MATERIA** | `r` mediano **VUOTO** | rapporto | materia `<` vuoto |
|--:|--:|--:|--:|--:|:--|
| `3` | `641` | `0.559663297` | `0.962150262` | `0.581680` | **SI** |
| `4` | `641` | `0.565691842` | `0.959483385` | `0.589580` | **SI** |
| `5` | `641` | `0.566790000` | `0.959141828` | `0.590935` | **SI** |
| `10` | `641` | `0.572574991` | `0.957296075` | `0.598117` | **SI** |
| `20` | `641` | `0.582729846` | `0.952603066` | `0.611724` | **SI** |
| `50` | `641` | `0.604579324` | `0.944501842` | `0.640104` | **SI** |
| `150` | `642` | `0.587524306` | `0.951865208` | `0.617235` | **SI** |

**Passi in cui `r` materia `<` `r` vuoto: `137` su `137`** *(`100.00 %`)*.

**L'ACCOPPIAMENTO E' SFASATO DI UNO, E DEVE ESSERLO:** `r_t = cs_(t-1)/CS_M`, e `cs_(t-1)` viene da `I_(t-1)`. Le **maschere** materia *(top `5 %` di `abs(psi)^2`)* e vuoto *(bottom `25 %`)* vengono da `I` del passo `t`, e il `r` dal passo `t+1`. Su 150 passi. ### **Le maschere si CONSERVANO** *(due bool per nodo, 3.8 MB su %d passi)*, cosi' **non c'e' nessun limite da dichiarare** -- e la prima versione dello strumento uno ce l'aveva, evitabile con 4 MB.

## CRITERIO `6` -- **IL CASO CHE DEVE FALLIRE**

| | |
|---|---|
| primo passo con una differenza **qualsiasi** | `1` |
| primo passo in cui diverge lo **STATO** | **`2`** |

> ### AL PASSO `1` LE DIFFERENZE SONO `4`, E **NESSUNA E' STATO**: sono i **contatori** che la cura rinomina -- `_ritmo_cs_assente`, `_ritmo_cs_forma`, `_ritmo_sicurezza`, `_ritmo_sicurezza_shape`. ### **Lo stato e' IDENTICO, e DEVE esserlo: al passo `1` `r = 1` in ENTRAMBE le leggi** *(la vecchia perche' `_psi_prec` non esiste, la nuova perche' la cache di `cs` non esiste)*. ### **E' il criterio `1` della `PARTE A` che si ripresenta da solo: dove le due leggi coincidono, coincide tutto.**

> ### E DUE DI QUELLE DIFFERENZE, DAL PASSO `2`, SONO `_med_f_prec` e `_med_f_ultimo`, classificate **STATO**: differiscono **per costruzione**, perche' la legge **vecchia** li scrive e la **nuova** no. ### **Sono i due registri morti della cura, e vederli qui e' la conferma che la promozione del gauge e' uscita** *(`RITMO-FLAG-SENZA-OGGETTO`)*.

| passo | differenze | di cui **STATO** | `cs_assente` *(cumulato)* | forma | `r` mediano | `r == 1` su |
|--:|--:|--:|--:|:--|--:|--:|
| `1` | `4` | `0` | `1` | `[-1, 12802]` | `1.000000` | `12802` |
| `2` | `43` | `28` | `1` | `[-1, 12802]` | `0.853423` | `0` |
| `3` | `59` | `41` | `1` | `[-1, 12802]` | `0.835503` | `0` |
| `4` | `61` | `42` | `1` | `[-1, 12802]` | `0.829073` | `0` |
| `5` | `61` | `42` | `1` | `[-1, 12802]` | `0.828354` | `0` |
| `10` | `61` | `42` | `1` | `[-1, 12802]` | `0.820798` | `0` |
| `20` | `62` | `42` | `1` | `[-1, 12802]` | `0.811295` | `0` |
| `50` | `140` | `81` | `1` | `[-1, 12802]` | `0.797504` | `0` |
| `100` | `160` | `89` | `1` | `[-1, 12802]` | `0.810300` | `0` |
| `150` | `163` | `91` | `1` | `[-1, 12802]` | `0.815126` | `2` |

## CRITERIO `7` -- **150 PASSI**, e che cosa cambia **A VALLE**

| | `A` *(la `PARTE A`)* | `B` *(il curato)* | scarto |
|---|--:|--:|--:|
| `n` | `14328` | `12827` | `-1501` |
| archi | `473397` | `471596` | `-1801` |

## L'ASPETTATIVA CHE AVEVO SCRITTO **PRIMA** DELLA CORSA

Nel task history, committato **prima del codice** *(`012f419`)*, avevo scritto:

> *<<Mi aspetto che l'altalena SPARISCA (rapporto per coppia `<= 1.2` da subito, cioe' dal passo `3`), e NON mi aspetto che l'anello `cs <-> r` oscilli.>>*

### **CONFERMATA, su entrambi i punti:** il rapporto per coppia resta `<= 1.2` **dalla PRIMA coppia valutabile** *(la `4`, cioe' i passi `3`-`4`: la coppia `2` e' esclusa perche' li' `r = 1` per sicurezza)*, col massimo a **`1.007756`**; e l'autocorrelazione e' **`0.891635`**, cioe' ### **fortemente POSITIVA** -- una serie che scende e risale **liscia**, non un'alternanza.

> ### ⚠ **E LO SCRIVO CON LA RISERVA CHE MERITA: nella `PARTE A` LA STESSA ### PREVISIONE ERA SBAGLIATA.** Avevo scritto che il rapporto <<sarebbe calato ma non crollato>> e invece **crollo'** *(`BRACCIO A`, `66a798d`)*. ### **Una previsione indovinata non rende affidabile chi la fa: rende verificata QUESTA.** Il motivo che avevo dato -- *<<l'anello vecchio passava per una DIVISIONE PER UNA MEDIANA, che AMPLIFICA; il nuovo per una `tanh` SATURA e per `dt_e`, che e' una catena CONTRATTIVA>>* -- e' **coerente** col numero misurato, ### **ma il numero non dimostra il meccanismo: dimostra solo che non oscilla.**

## LA DOMANDA APERTA PER LUCA -- e **non la risolvo io**

> ### IL MANDATO HA **DUE LETTURE** su un punto, e la differenza e' il ramo **`TEMPO_SEGNO`** *(`:5303`-`:5312`)*:
> * **(A)** *<<con `TAU_LOC > 0` restituisce `cs_nodo_prev / CS_M` per nodo>>* -- e allora quel ramo diventa **IRRAGGIUNGIBILE per costruzione**;
> * **(B)** *<<il ramo che leggeva la FASE esce dalla fisica>>* -- e allora esce **solo** quello.
>
> ### **HO SCELTO LA LETTURA `B`, LA MINIMA**, e il perche' e' una regola: il par.2 dice di **non estendere una cura da soli**, e `TEMPO_SEGNO` **non e' nominato** fra i rami che escono. ### **E OGGI LE DUE LETTURE SONO INDISTINGUIBILI** *(`TEMPO_SEGNO = False`, quindi la scelta e' **byte-inerte**)*. ### **Ma se un giorno venisse acceso darebbero `r` DIVERSI, e quella e' una decisione di Luca.**

## CHE COSA RESTA APERTO

1. **`RITMO-FLAG-SENZA-OGGETTO`** *(aperta da questa cura)*: `RITMO_WRAP_2PI` e `TEMPO_PROPRIO_ORIENTATO` **perdono il loro unico consumatore fisico** e **non sono stati tolti**; `_sigillo_ritmo_wrap.py` e `_sigillo_anello.py` **perdono il loro oggetto** e ### **nessuno dei due e' sbagliato** -- si rigirano **al loro commit**.
2. **`CS-LAMBDA-GLOBALE`**: da questa cura **il tempo di ogni legge locale legge una media globale**, e il criterio `5` dice **di quanto**.
3. **LA MISURA CON `DT` DIMEZZATO**, decisa da Luca per **dopo** questo sigillo, col criterio fissato in `a0641f` -- un transitorio **fisico** dura lo stesso **TEMPO**, un **artefatto** resta a periodo `2` **PASSI**, e un **raccordo** si accorcia nel tempo e non nei passi.
4. **i due registri morti** `_med_f_prec`/`_med_f_ultimo` e **`_psi_prec` promosso e non piu' letto dalla fisica**: una voce da aprire, **non in questo commit**.

---

*Referto **generato** da `csv/_seal_fork/_referto_z43_cura2.py` dal `sigillo.json` della corsa: ### **nessun numero e' ricopiato a mano** (`L-NUMERI`).*
