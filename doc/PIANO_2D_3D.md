# IL PIANO: 2D PER LE PROPRIETA' LOCALI DEL PASSO, 3D PER LE LEGGI GLOBALI

> ### ⭐ **DECISIONE DI LUCA, `2026-10-23`, `18:34`** *([[PIANO-2D-3D]])*: ### **il piano discusso col guardiano dalle `18:00` alle `18:34`, approvato.** Le sue parole: ### «dovremmo
> formalizzare tutte queste considerazioni e il nuovo piano sul repository». ### **E' il PIANO CORRENTE.** ### **Collegato a [[DECISIONE-SOLO-TRIANGOLI]] e a
> [[DECISIONE-L1-NATURA-A-SIMULATORE-B]].**
>
> ### ⛔ **LE DECISIONI DI FISICA APERTE RESTANO APERTE:** ### **questo documento non ne prende nessuna** *(sezione `F`)*. ### **Non tocca** `doc/ASSIOMI.md`, `doc/STELLA_POLARE.md`, `leggi.yaml`,
> l'albero delle decisioni, il nucleo.
>
> ### 📏 **I NUMERI:** ### **ognuno verificato contro il referto del suo commit prima di scriverlo.** ### **Dove il testo del mandato e il referto non coincidono, qui c'e' il numero del
> REFERTO, e la differenza e' segnalata con ⚠.**

## A. IL PRINCIPIO

- ### **In 2D** *(i triangoli)* ### **si provano le PROPRIETA' LOCALI del passo:** ### **come scala con `s`; lo zero dell'energia; la risposta di una particella di prova a un gradiente di `cs`**
  *(l'universalita' e il verso)*.
- ### **Le LEGGI GLOBALI si decidono in 3D:**
  - ### **la forma del campo prodotto dalla materia** *(in 3D `1/r^2`; in 2D `1/r`, col potenziale logaritmico; in relativita' generale a `2+1` dimensioni nessuna forza locale, solo difetti
    conici, e nessuna onda gravitazionale)*;
  - ### **l'esistenza e la stabilita' dei solitoni** *(in 2D il legame cubico e' il caso critico)*;
  - ### **lo spin:** ### **le rotazioni dello SPAZIO in 2D sono solo `U(1)`; lo spin INTERNO del modello resta `SU(2)` anche sui triangoli** *(il trasporto `U` in `SU(2)`, la simmetria
    della griglia sollevata al dicicloico `Dic6` dentro `SU(2)`, `doc/PROGETTO_TRIANGOLI.md`)*: ### **cio' che in 2D manca e' la piena `SU(2)` delle rotazioni dello spazio, non quella dello
    spinore** *(la correzione di Luca, errore del guardiano `n.55`, `2026-10-23`)*;
  - ### **la propagazione senza coda** *(solo nelle dimensioni dispari)*.
- ### **LE IDEE SULLO SPAZIO-TEMPO `3+1`** *(la discussione del `2026-10-23`, `18:37`-`19:39`: le idee di Luca, i fatti, le prove da fare, la verifica del `3.08` dell'era `1`; NESSUNA decisione)*: ### **`doc/SPAZIOTEMPO_3PIU1.md`** *([[SPAZIOTEMPO-3PIU1]])*.
- ### **Il 2D e' un GRADINO.** ### **L'obiettivo tecnico e' la FCC** *(non bipartita, `12` vicini)*; ### **l'obiettivo di fisica e' lo spazio che emerge** *(`D9`: `DEC-D9-GEOMETRIA` in
  `doc/ALBERO_era2.yaml`, «come nasce la geometria: la topologia e la metrica», `presa: false`)*.

> 📝 **LA NOTA SULLO SPIN DELLA PRIMA VERSIONE** *(`7e794402`)* ### **segnalava il contrasto con `doc/PROGETTO_TRIANGOLI.md`; Luca l'ha risolto con la frase sopra** *(errore del guardiano `n.55`)*.

## B. CHE COSA SI TRASFERISCE AL 3D, E CHE COSA NO

### **SI TRASFERISCE** *(proprieta' della FORMA del passo: da RIVERIFICARE in 3D)*:

| la proprieta' | dove e' misurata | il numero del referto |
|---|---|---|
| ### il legame obbedisce alla relativita' generale al bit | `c4efc937` *(`gravita_collettiva`)* | ### **`D_tot = D_ramo` entro `1.3e-11`, lo stesso per forme, densita' e taglie entro `2.4e-11`; `D = 0` entro `9.87e-12` sul ramo basso di `eps 0`** ⚠ *(«`D = 0`» vale per il ramo basso di `eps 0`: sul ramo alto `D = -2 pi/s^2`, e la parte del LEGAME e' quella esatta)* |
| ### il principio di equivalenza tiene dove il passo vale `exp(-i s H)`: il solitone con `c = c0 s` obbedisce | `05055fc6` *(`scala_e_zero`)* | ### **`|D| <= 2.05e-8` su `30` punti** *(la soglia era `1e-6`)* ⚠ *(il mandato dice «al bit»: `2e-8` non e' la precisione di macchina)* |
| ### la violazione va come `s^2` grazie al palindromo | `05055fc6` sul quadrato; `8781162c` sui triangoli | ### **contro `s`: `2.140`, `2.127`, `2.123`, `2.124`** *(quadrato)*; ### **`2.140`, `2.127`, `2.123`, `2.122`** *(triangoli)* ⚠ *(contro `s - 0.02`: `1.70`-`1.72`, e su quella scala il PUO'-FALLIRE di `05055fc6` era FALLITO)* |
| ### lo zero simmetrico e' l'unico universale fra i rami a `eps 0` | `e31366ec` sul quadrato; `8781162c` e `cbcb99c7` sui triangoli | ### **`lambda* = 0.500000026`, `0.500000006`, `0.500000000`** *(quadrato, `s0 0.3, 0.5, 0.9`)*; ### **`0.50000000` a `eps 0`, `s 0.05`-`0.5`** *(triangoli, otto decimali)* |

### **NON SI TRASFERISCE** *(dipende dal reticolo)*: ### **dove stanno i modi leggeri, e il segno della gravita'.**

- ### **Sul QUADRATO** *(bipartito)* ### **la gravita' dei rami e' REPULSIVA:** ### **`a_H/a_RG` a `s` piccolo `-1.8433` a `s 0.05`, il limite di grado `2` `-1.8671`** *(`e31366ec`, `eps 0`)*.
- ### **Sui TRIANGOLI** *(non bipartiti)* ### **la coppia a `K` e `K'` e' massiva, isotropa, con `salto/s` che tende a `pi`** *(`3.1392`, `3.1319`, `3.0532`, `2.8909` a `s 0.05`-`0.5`)*, ### **e con
  lo zero simmetrico cade verso `cs` BASSO, uguale sulle due bande:** ### **`a_H/a_RG = +2.2616` a `s 0.05`, `+1.6310` a `s 0.5`** *(`8781162c`)*. ### **La dinamica lo conferma:** ### **`a_mis/a_H`
  fra `0.92` e `0.98` in ogni caso, `a_1/a_0 = 1.007` col simmetrico** *(`cbcb99c7`)*.
- ### **INDIZIO, da UN SOLO confronto, NON una regola:** ### **la non bipartizione va col segno giusto.** ### **E' un argomento per la FCC contro la cubica e la BCC** *(la BCC e' bipartita:
  `doc/PROGETTO_TRIANGOLI.md`)*.

## C. PROSEGUIRE

1. ### **LA FORZA SUI TRIANGOLI** *(il mandato «i triangoli, secondo gradino»)*: ### **FATTO in `cbcb99c7`** *(lo specchio: i `4` casi su `128` restano FALLITI, la causa misurata e' un'accelerazione propria del pacchetto, [[PACCHETTO-K-NON-FERMO]];
   da ora lo specchio si fissa sul differenziale, `doc/PATTERN_DI_PROVA.md`)*:
   - ### **Hamilton confermato dalla dinamica** *(`a_mis/a_H` `0.920`-`0.976` a `eta 1e-2`; `0.882`-`0.988` con `eta 1e-3`; il differenziale `0.921`-`0.977`)*;
   - ### **il fattore NON viene dalla velocita'** *(con `v_max = 0.60 s` `a/a_RG` e' `1.63`-`1.68`: da spiegare)*;
   - ### **le due bande uguali col SOLO zero simmetrico** *(`a_1/a_0 = 1.007` a `eps 0`)*;
   - ### **la violazione da moneta va come `s^2 eps^2`:** ### **`lambda* - 1/2 ~ s^2.030 eps^1.873`; la differenza fra le bande `~ s^2.177 eps^1.714`**;
   - ### **il limite a `s` piccolo piatto** *(`0.969`, `0.977`)*.
   - ### **IL BILANCIO DEI TRIANGOLI** *(`77f9f850`, `92c63912`)*: ### **l'UNICO modo senza massa e' a `s = 1` ESATTO, a `Gamma` attraverso la fase `pi`, a `1/sqrt2 = v_max`; per `s < 1` quei rami hanno salto `2 pi (1 - s)`
     -- la massa da ritardo;** ### **la moneta non apre modi senza massa fino a `pi/2`; la vestizione dal vuoto non cambia `omega''`;** ### **`v_b/v_max` della coppia a `K` da `1.310` (`s 0.05`) a `0.778` (`s 1`), con
     l'incrocio `v_b = v_max` fra `s 0.7` e `0.9`** *(la stima del guardiano per interpolazione: `s ~ 0.73`, DA MISURARE)*; ### **la `c` del modello NON c'e' sui triangoli: va cercata nel campo `U(1)` o nelle onde di
     `cs`, in 3D.** ### **`S1` contro `S4`: il dossier `doc/DOSSIER_S1_S4.md`.**
2. ### **POI LA FCC:** ### **la stessa catena** *(gli spettri, i modi leggeri, Hamilton, la forza)*. ### **Gli strumenti si progettano in un mandato a se':** ### **la scena FCC** *(`12`
   estremita' per nodo)*, ### **la zona di Brillouin** *(l'ottaedro troncato; i punti `Gamma`, `X`, `L`, `W`, `K`)*, ### **la prova di non bipartizione, la simmetria del reticolo, il toro a lati
   diversi.**

## D. FERMARE IN 2D, PER RIPRENDERE IN 3D

3. ### **I SOLITONI** *(l'esistenza, le larghezze, la stabilita', la dinamica nel gradiente)*.
4. ### **IL CANALE DI `cs`** *(come la materia produce `cs`; `doc/RACCOLTA_CS.md`, e `R1` `0.402` per `S1`, `0.443` per `S4`: `974d411a`)*.
5. ### **LA SCELTA FRA `S1` E `S4`** *(`DEC-FC-COESIONE`)*: ### **resta APERTA, e con lei `DEC-D7-DIVISIONE`** *(`presa: false`)*.

## E. IN PAUSA

6. ### **LA MONETA NEL TICK** *(`682e15ef`: `C1` il bilancio alternato sul nodo, `C2` la rotazione unica sul nodo, `C3` la rotazione unica sull'arco; `C4` globale, scartata)*: ### **sui triangoli
   la coppia a `K` e' gia' massiva a `eps 0` e cade nel verso giusto; la moneta sposta poco lo zero universale** *(`lambda*` da `0.50003066` a `0.50162143` a `eps > 0`, `8781162c`; `lambda* - 1/2 ~
   s^2.03 eps^1.87`, `cbcb99c7`)*. ### **La forma della moneta si decide sulla FCC, dove lo spin e' pieno.**

## F. LE DECISIONI DI LUCA CHE STANNO MATURANDO *(APERTE: nessuna e' presa)*

7. ### **LO ZERO DELL'ENERGIA** *(la convenzione dei pezzi parziali: oggi `exp(i theta (I - P))`; simmetrica `exp(i theta (I - 2P)/2)`, come gia' la moneta)*. ### **Informazione:** ### **e' fisica, non
   convenzione** *(la dinamica nel gradiente cambia: `6e022419`, lo scarto `9.88e-2` a `eta 1e-2`, uguale entro `2.3e-14` a `eta 0`; sui triangoli i versi opposti delle bande con lo zero di oggi,
   `cbcb99c7`)*; ### **lo zero simmetrico e' l'unico universale.** ### **Da decidere DOPO la conferma dinamica sui triangoli** *(arrivata in `cbcb99c7`, con lo stop sullo specchio)*.
8. ### **LA REGOLA DI SCALA** *(`s -> 0`, `s` fisso, `s -> 1`)*. ### **Informazione:** ### **la violazione del principio di equivalenza va come `s^2` a `s` piccolo ed e' d'ordine `1` vicino al cono**
   *(`05055fc6`: `delta` continuo `0.554`-`0.663` a `s 0.99`; la misura di violazione `Vi` fino a `1.29e+02` a `s 0.99`)* ⚠ *(il mandato dice «rapporti fra specie fino a `~129`»: nel
   referto `129` e' `Vi`, la misura di violazione della coppia, non un rapporto grezzo)*: ### **e' la ragione piu' forte contro `s -> 1` nella forma di oggi.** ### **Da decidere PRIMA di costruire gli
   strumenti della FCC, perche' fissa il regime di lavoro.** ⚠ *(una regola di scala IN VIGORE c'e' gia': `7fc47558`, «la regola di scala di oggi dimezza la velocita' fisica»; aperta e' la
   SCELTA fra i tre limiti)*.
9. ### **LE DOMANDE APERTE:** ### **il fattore `2.26`** *(non `1`; `cbcb99c7`: non viene dalla velocita', viene dalla forma della banda)*; ### **lo spostamento di `lambda*` con la moneta**; ### **perche' la
   bipartizione inverte il segno.**

## G. IL BILANCIO DEL `2026-10-22`/`23`

> ### **La tabella e' GENERATA da `git log`:** ### **il risultato in una riga e' l'oggetto del commit del referto** *(troncato)*. ### **La griglia:** ### **«quadrato, marcato»** *(i `25` file
> di `406b32f0`, dal `44d4963d` al `9a6955f3`)*, ### **«triangoli»**, ### **«--»** dove il lavoro non e' una misura su griglia o la marcatura non lo copre.

| il mandato | la griglia | i commit | il risultato in una riga *(l'oggetto del commit)* |
|---|---|---|---|
| i triangoli, R1 | triangoli | `56608e8a` *(10-22 00:29)* | TRIANGOLI, R1: 10 SU 10 -- R1 NON STABILE, MASSIMO 0.3897 ALL INTERNO (0.720 DEL QUADRATO) -- I TRIANGOLI TOLGONO IL 28 PER CENTO IN R1 E IL 6 IN R2 -... |
| S3 ripensata | -- | `3d009495` *(10-22 00:40)* | S3 RIPENSATA: IL DOCUMENTO -- LA BANDA NON E DELLA GEOMETRIA, NE DELLA SCALA, NE DI nu_S3 (nu /4, GUADAGNO -15 PER CENTO): E DELLA CAMMINATA -- LA LET... |
| due misure su S3: S-E e la materia diluita | -- | `642dee6f` *(10-22 02:27)*, `07083f09` *(10-22 02:40)* | LA MATERIA DILUITA: INSTABILE -- LA BANDA 0.3933 A x 1e-4, IL 97.9 PER CENTO DI x 0.1 -- nu_S3 = rho dalpha/drho DAL CODICE ENTRO 1.3e-10 -- E A x PIC... |
| lo stato finale | -- | `07ca006e` *(10-22 02:53)*, `3c540740` *(10-22 07:48)*, `6b2f332b` *(10-22 07:53)*, `6f297d71` *(10-22 16:35)* | STATO FINALE, R1T E LA SINTESI: NESSUN BRACCIO DEGENERA, MA IN TUTTI E QUATTRO I GRUMI SONO FISSI IN ARCHI (0.998-1.003) -- LA MATERIA SI RAGGRUPPA AL... |
| la prova di Grover | -- | `52e31a41` *(10-22 09:47)* | LA PROVA DI GROVER: GROVER INNOCENTE -- CON FOURIER LE BANDE PIATTE SPARISCONO, LA BANDA DI S3 NO (0.87-0.92 DI GROVER, QUADRATO E TRIANGOLI) -- LA MA... |
| lo screening delle forme di S3 (l'errore n.33) | -- | `389093bc` *(10-22 12:06)* | LO SCREENING DELLE FORME DI S3: IL LEGAME TIENE -- S1 E S4 (ACCOPPIAMENTO -> 0) STABILI A POCA MATERIA, S2 E S3 NO -- NESSUNA STABILE A x 0.1, S1 ALL ... |
| DECISIONE-LINEARE (S1 / S4) | -- | `e345cd8f` *(10-22 13:07)*, `cb846b2a` *(10-22 16:41)*, `b16e58ba` *(10-22 18:00)*, `974d411a` *(10-22 19:12)* | DECISIONE-LINEARE, PARTE CS E SINTESI: CON cs R1 E INSTABILE PER S1 (0.402) E S4 (0.443) -- CON S1 L INSTABILITA DI R1 VIENE DA cs, NON DA S3 (R2 0.00... |
| l'origine dei 32 archi | -- | `82b40ca1` *(10-22 19:30)* | L ORIGINE DEI 32 ARCHI: IL DOCUMENTO -- E LA LUNGHEZZA DELL INSTABILITA MODULAZIONALE 2 pi sqrt(c/(2 gamma)) CON LA CAMMINATA NEL CONTINUO -- FISSA IN... |
| la moneta e la massa? | -- | `e133316a` *(10-22 19:54)*, `238b3599` *(10-22 20:22)* | LA MONETA E LA MASSA? MISURA 2: LA LUNGHEZZA SEGUE c (ENTRO UN PASSO A TRE eps) -- MA LA PROVA DISTINGUE POCO -- LA CONSEGUENZA SCRITTA: eps NON E LA ... |
| le voci del registro e la decisione su L1 | -- | `d06e402c` *(10-22 20:29)*, `80d89521` *(10-22 20:33)*, `28b4c92d` *(10-22 20:39)*, `82dc6310` *(10-22 20:47)*, `63e6499f` *(10-22 20:53)* | REGISTRO: LA VOCE LUCE-VINCOLO-LAMPI-GAMMA -- LA LUCE DEL MODELLO RISPETTA IL VINCOLO DEI LAMPI GAMMA? (FRONTE, FISICA, ERA 2, AGENDA) |
| da dove viene la massa della camminata? | -- | `7fc47558` *(10-22 21:04)* | DA DOVE VIENE LA MASSA DELLA CAMMINATA? DAL GENERATORE CONTINUO: Delta E c COSTANTI A s PICCOLO, LINEARE A s = 1 -- LA REGOLA DI SCALA DI OGGI DIMEZZA... |
| la raccolta su cs e Lambda_c | -- | `4106d391` *(10-22 21:16)* | LA RACCOLTA SU cs E Lambda_c: IL DOCUMENTO -- 39 VOCI (19 ERA 2), 1 NODO, 24 SEZIONI DELLA MAPPA, 54 TASK HISTORY, 7 REFERTI -- LA LETTURA DI OGGI E S... |
| la massa vicino al cono (l'errore n.36) | -- | `51f45268` *(10-22 21:39)* | LA MASSA VICINO AL CONO: SI SPEGNE COME (1 - s)^1 (p 1.05, LA PREVISIONE) -- CONTA SOLO s, QUINDI cs -- LA MASSA INVARIANTE LOCALMENTE -- E UN DIFETTO... |
| la prova del principio di equivalenza | quadrato, marcato | `44d4963d` *(10-22 22:30)* | LA PROVA DEL PRINCIPIO DI EQUIVALENZA: LE MASSE DELLE SPECIE NON SCALANO INSIEME CON s (124 V SU 125 SOPRA 1e-3) -- LE TAGLIE FALLISCONO SULLE CATENE ... |
| il verso e l'intensita' della forza da cs | quadrato, marcato | `f6f7b108` *(10-23 09:34)*, `557d94d6` *(10-23 09:39)* | LA FORZA DA cs, LA CORSA: IL VERSO DIPENDE DALLA SPECIE (eps 0 ALTO VERSO cs ALTO, eps 0.5 VERSO cs BASSO) -- TIENE HAMILTON CON omega(0), CADE omega(... |
| la moneta dentro il tick (sulla carta) | quadrato, marcato | `682e15ef` *(10-23 09:47)* | LA MONETA DENTRO IL TICK, IL PROGETTO SULLA CARTA: QUATTRO COSTRUZIONI (C2 ROTAZIONE UNICA SUL NODO RACCOMANDATA, C1 COME CONTROLLO) -- LA SPECIE eps ... |
| la gravita' collettiva (n.45) | quadrato, marcato | `d6c03598` *(10-23 10:54)*, `c4efc937` *(10-23 11:13)* | LA GRAVITA COLLETTIVA, LA CORSA COL CRITERIO D (n.45): IL LEGAME E LA RELATIVITA GENERALE AL BIT, IL SOLITONE NO (D DIPENDE DA NORMA E FORMA) -- 8 CON... |
| la scala e lo zero (n.46) | quadrato, marcato | `05055fc6` *(10-23 11:39)* | LA SCALA E LO ZERO: A eps 0 I RAMI OBBEDISCONO CON LA FASE CONTINUA (/D/ <= 4.2e-10) -- LA VIOLAZIONE VA COME s^2 (IL PALINDROMO) -- IL SOLITONE CON c... |
| lo zero simmetrico (n.47) | quadrato, marcato | `6e022419` *(10-23 12:33)* | LO ZERO SIMMETRICO IN MEMORIA: TUTTE LE SPECIE CADONO NELLO STESSO VERSO, VERSO cs ALTO (UNA SPINTA, /a/a_RG/ ~ 2 A s0 PICCOLO) -- LO ZERO A META NON ... |
| il segno della gravita' (n.48, n.49; la parte D) | quadrato, marcato | `e31366ec` *(10-23 13:57)*, `6caeff02` *(10-23 15:00)*, `6c36b19a` *(10-23 15:10)* | IL SEGNO DELLA GRAVITA, LA PROVA DELLA CORREZIONE DEL RAMO: A eps 0.5 s0 0.1 ORA curv - Dt 0.1650, eta 0 SOTTO IL RUMORE (2 SU 2) |
| i modi a k = pi e i solitoni larghi (n.51, n.52) | quadrato, marcato | `9a6955f3` *(10-23 15:35)* | I MODI A k = pi E I SOLITONI LARGHI: A eps 0 LA BANDA PIU BASSA SENZA MASSA A (pi, pi), I MODI MASSIVI A (pi, 0) SELLE -- SIMMETRICA: (pi, 0) VERSO cs... |
| la C.3 non eseguita; il blocco P-ALB | -- | `f79d2cd4` *(10-23 16:23)* | LA C.3 SUL QUADRATO COMMITTATA NON ESEGUITA (GRIGLIA QUADRATA, DECISIONE DI LUCA SOLO TRIANGOLI) -- E IL BLOCCO P-ALB SCIOLTO: DEC-D7-DIVISIONE RESTA ... |
| solo triangoli, parte 0 (n.53) | -- | `406b32f0` *(10-23 16:36)* | LA DECISIONE DI LUCA: SOLO TRIANGOLI (REGISTRATA NELL INDICE, NEL REGISTRO DELLA FISICA E IN CLAUDE.md) -- 25 FILE DEL QUADRATO MARCATI -- CHE COSA SA... |
| i triangoli, primo gradino | triangoli | `8781162c` *(10-23 17:02)* | I TRIANGOLI, PRIMO GRADINO, IL REFERTO: LA COPPIA PIU STRETTA A K E K', MASSIVA (salto/s 3.14-2.89), ISOTROPA; lambda* = 1/2 SOLO A eps 0 (IL PUO-FALL... |
| i triangoli, secondo gradino | triangoli | `cbcb99c7` *(10-23 19:08)* | I TRIANGOLI, SECONDO GRADINO, IL REFERTO: HAMILTON CONFERMATO DALLA DINAMICA (a/a_H 0.92-0.98) -- UN DEVE-PASSARE FALLISCE (LO SPECCHIO A eta 1e-3, 4 ... |

### **GLI ERRORI DEL GUARDIANO DAL n.38 AL n.53** *(la formulazione del mandato; accanto, quella del repo dove c'e')*

| n. | la formulazione del mandato | la formulazione del repo |
|---|---|---|
| `n.38` | V era il criterio sbagliato | ### **non trovata nel repo** *(ne' col numero ne' senza)* |
| `n.39` | la separazione moneta/ritardo | ### **non trovata nel repo** *(ne' col numero ne' senza)* |
| `n.40` | «tutte negative» | senza numero: «Il «tutte negative» delle pendenze NON dice il verso della forza» (`RELAZIONE_PER_CLAUDE.md`); ««TUTTE NEGATIVE» vale per le catene principali, non per tutte le specie» (`doc/TASK_HISTORY/2026-10-23_forza_da_cs.md`) |
| `n.41` | le taglie a pari eta | ### **non trovata nel repo** *(ne' col numero ne' senza)* |
| `n.42` | le pendenze del fit invece di omega(0) | senza numero: «`a_prev[Dt]`, cioe' la previsione fatta con le pendenze del `Dt` del fit (quelle del guardiano)» (`2026-10-23_forza_da_cs.md`); `557d94d6` |
| `n.43` | la tolleranza dello specchio | ### **non trovata nel repo** *(ne' col numero ne' senza)* |
| `n.44` | SATURAZIONE creduta attiva | senza numero: «`CAMM-SATURAZIONE` NON E' NELL'ORDINE ... Il guardiano la conta fra i pezzi: nel passo di oggi non c'e'» (`2026-10-23_gravita_collettiva.md`) |
| `n.45` | la pendenza logaritmica | «la pendenza logaritmica `d ln omega/d ln s` NON e' ben posta dove `omega` passa per lo zero» (`2026-10-23_gravita_collettiva.md`; `f3180571`, `c4efc937`) |
| `n.46` | il controllo a c costante | «il controllo a `c` costante di `c4efc937` era mal posto -- il termine di moto non scalava con `s`; il controllo giusto e' `c` proporzionale a `s`» (`2026-10-23_scala_e_zero.md`) |
| `n.47` | l'esponente 1 invece di 2 | «aveva previsto la violazione del moto come `s`; `05055fc6` ha misurato `s^2` (il palindromo)» (`2026-10-23_zero_simmetrico.md`) |
| `n.48` | zero a meta' preso per zero simmetrico | «lo zero a meta' non e' il simmetrico» (`2026-10-23_segno_gravita.md`) |
| `n.49` | Einstein con omega assoluto | «`Q` con `omega(0)` assoluto non e' dinamico» (`2026-10-23_segno_gravita.md`) |
| `n.50` | il vuoto non fissato nella parte D | senza numero: `6caeff02`, «LA PRECISAZIONE DI LUCA SULLA PARTE D REGISTRATA (IL VUOTO Lambda0 = 4 ...)» |
| `n.51` | il salto vicino a pi | «Gli errori del guardiano n.51 e n.52 sono nel mandato» (`2026-10-23_modi_pi_e_solitoni.md`): ### **il contenuto NON e' scritto nel repo** |
| `n.52` | solitoni larghi non verificati | come n.51: il contenuto NON e' scritto nel repo |
| `n.53` | il quadrato usato dopo la decisione di Luca | ⚠ **diversa:** «i mandati del 2026-10-22/23 dicevano «stessa griglia di 51f45268», cioe' il quadrato, e la frase di cbc1114f «_triangoli.scena fa solo il toro quadrato» era stata accettata senza verificarla» (la voce `DECISIONE-SOLO-TRIANGOLI`; `doc/REGOLE/par13.md`): ### **il quadrato usato PRIMA della decisione, perche' una frase non verificata diceva che i triangoli non c'erano** |
| `n.55` | la frase sullo spin in 2D del mandato del piano («le rotazioni sono solo `U(1)`») | ### **corretta da Luca** *(`2026-10-23`)*: le rotazioni dello SPAZIO in 2D sono solo `U(1)`, lo spin INTERNO resta `SU(2)` *(sezione `A`)* |
| `n.56` | le tre imprecisioni del mandato del piano | ### **restano come segnalate col ⚠** *(sezione `B`)*: `|D| <= 2.05e-8`, non al bit; `129` e' `Vi`; `D_tot = D_ramo` |
