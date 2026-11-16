# IL PIANO DI VERIFICA NELLA SCATOLA GIUSTA *(Luca `2026-11-16` `17:47`; R-SCATOLA al `5%` con le TRE clausole)*

> **La domanda di Luca** *(`17:43`)*: **la fisica vista finora** *(le coppie B2 e B2-pi, il triangolo a `120`, le forze a `35`, `51`, `66`)* **viene da `L 162`, dove R-SCATOLA non e' rispettata: e' quella che vedremo nella scatola giusta?**
> **Le previsioni sono committate PRIMA dei risultati; le soglie non si rivedono** *(se si rivedono: post-hoc, dichiarato)*.
> **Le fasi `0`-`2` si fanno; la fase `3` SOLO dopo «VIA ALLA FASE 3».**

## Le scelte comuni *(del guardiano, su delega di Luca)*

- **Gli stessi mattoni** *(`L162_MGU_03000`, il francobollo)* **e le stesse condizioni iniziali delle corse di `L 162`** *(la stessa `d`, le stesse fasi)*: **cambia SOLO la scatola.**
- **L'interprete di E:; codice NUOVO; il motore di oggi** *(numba spento, la ROTTA)*; **un filo per processo; al massimo `5` processi.**
- **I tori:** **`doc/referti_l2/piano_scatola_tori.txt`** *(`6f9280a8`)*: **`R_ogg = r_scena + 25`, la distanza al lato del rombo `L sqrt(3)/4 >= max(3 R_ogg, 2 R_ogg + 30)`, il primo multiplo di `3`.**

## FASE 0 -- IL CANCELLO

- **La prova del mattone da solo su `L 186`** *(il mandato delle `16:17` con la correzione delle `16:58`; la carta `doc/TASK_HISTORY/2026-11-16_scatola5.md`; la corsa `prova-scatola5-L186`, aperta alle `17:47`)*. **Se non passa: FERMO, il piano si ferma.**

## FASE 1 -- LE FORZE *(corse brevi)*

| corsa | la fase | `d` | il toro | il riferimento su `L 162` / `L 243` |
|---|---|---|---|---|
| F-35 | in fase | `35` | `L 297` | `-1.010266e-06` *(`coppia_GU_L162.txt`)* |
| F-51 | in fase | `51` | `L 351` | `-2.615720e-08` *(`coppia_GUd50_L162.txt`)* |
| F-66 | in fase | `66` | `L 402` | `-1.337978e-08` *(`coppia_GUd65_L243.txt`, su `L 243`)* |
| A-35 | antifase | `35` | `L 297` | `+3.605169e-07` *(`coppia_GUpi_L162.txt`)* |
| A-45 | antifase | `45` | `L 330` | *(nessuno: nuova)* |
| A-51 | antifase | `51` | `L 351` | *(nessuno: nuova)* |
| A-66 | antifase | `66` | `L 402` | *(nessuno: nuova)* |

- **Il metodo: quello dei referti di `L 162`** *(lo strumento `csv/solitone/mattone_coppia_L162.py`: `2000` tick; `d''` sui tick `250`-`2000` con la sua barra; lo stesso codice di misura, la scena col toro e il bordo della regola)*.
- ### **LE PREVISIONI** *(del guardiano)*:
  - **P-F1:** **a `35` la forza in fase entro il `5%` di `-1.010e-6` e in antifase entro il `5%` di `+3.605e-7`** *(la parte corta non sente la scatola)*.
  - **P-F2:** **a `51` entro il `10%`** *(in fase, contro `-2.616e-8`)*.
  - **P-F3:** **a `66` DIVERSA di piu' del `10%`** *(su `L 243` c'e' la forza delle copie; il verso non lo prevedo)*.

## FASE 2 -- IL CONFRONTO CON CIO' CHE C'E' GIA'

- **La tabella «`L 162` contro la scatola giusta»** *(la prova del mattone della fase `0`; le forze della fase `1`)*; **i COSTI della fase `3` coi tempi veri** *(sotto)*; **commit; FERMO per Luca.**

## FASE 3 -- GLI OGGETTI LEGATI *(corse lunghe; SOLO dopo «VIA ALLA FASE 3»; le tre in parallelo)*

| corsa | che cosa | il toro del mandato | il toro della regola *(la `d` piu' grande della corsa su `L 162`)* | i tick |
|---|---|---|---|---|
| V-B2 | la coppia in fase da `d 35` | `L 278` | **`L 297`** | `12000` |
| V-B2pi | la coppia in antifase da `d 35` | `L 312` | **`L 321`** *(su `L 162` fino a `42.42`)* | `10000` |
| V-T120 | il triangolo a `120` | `L 334` | **`L 339`** *(il lato fino a `40.84`)* | `12000` |

- ### **UN PUNTO PER LUCA:** **i tori del mandato vengono dalle scene TIPO del conto di R-SCATOLA-U** *(la coppia a `30` e a `40`, il triangolo di lato `40`)*; **con la `d` piu' grande che ogni corsa tocca, la regola vuole `L 297`, `321`, `339`.** **Si decide al via della fase `3`.**
- ### **LE PREVISIONI** *(del guardiano; P-V6 l'ipotesi di Luca)*:
  - **P-V3** *(V-B2)*: **resta legata; il primo minimo fra `27` e `31`; il periodo entro il `15%` di `9700` tick.**
  - **P-V4** *(V-B2pi, la piu' a rischio)*: **la distanza ESCE dalla fascia `38.5`-`42.5` in cui stava su `L 162`** *(l'equilibrio intorno a `40` era in parte della scatola)*. **Cade se resta nella fascia fino a `10000`.**
  - **P-V5** *(V-T120)*: **resta legato** *(il lato con un minimo fra `30` e `35`)*; **il giro `+1` in tutte le `12` a ogni controllo; la forma gira in verso antiorario; B al centro negativo.**
  - **P-V6** *(l'IPOTESI DI LUCA sulla scatola, `2026-11-15` `18:43`)*: **il GUSCIO del vuoto** *(la m=3 di `|phi - phi0|` fra `30` e `45` nodi)* **NON resta fermo: a `k 12000` ha girato almeno un TERZO della rotazione dei lobi** *(su `L 162`: `1`-`2` gradi contro `+98`)*. **Cade se gira meno di un terzo.**
- ### **V-T120 FERMATA** *(Luca `2026-11-17` `00:20`)*: **R-SCATOLA al `5%` non rispettata da `k 250`** *(R_ogg al `5%` da `47` a `59`: la distanza al lato `2.49` R_ogg, R_A `1.65` R_ogg)*; **gli stati restano su E:** *(`E:/soliton_simulator/notte/V-T120`)*; **il posto va a F-51.** **Il triangolo si RILANCIA piu' avanti, con un mandato di Luca, su un toro scelto DOPO aver misurato quanto cresce R_ogg al `5%` del triangolo** *(dalle serie della corsa fermata e da quelle di `L 162`)*.
- **Le letture alla fine di ognuna: le stesse dei referti di `L 162`** *(la serie, le mappe, la girandola, B, gli anelli)*, **con lo stesso codice.**

## I COSTI *(la stima del mandato; i numeri veri dalla fase `0` nella fase `2`)*

- **I nodi crescono come `L^2`.** **La stima del mandato** *(a macchina libera circa `2.2 s` per tick su `L 150`)*: **circa `7 s` per tick su `L 278`, `9` su `312`, `11` su `334`: V-B2 circa `24` ore, V-B2pi circa `25`, V-T120 circa `37`; in parallelo circa un giorno e mezzo.** **Con i tori della regola** *(`297`, `321`, `339`)* **un po' di piu': si riscrive col tempo per tick misurato su `L 186`.**
- **La fase `1`:** **`7` corse da `2000` tick su `L 297`-`402`.**
