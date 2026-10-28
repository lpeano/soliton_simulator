# L'IPOTESI DI LUCA SULLO ZERO DEL VUOTO *(01:26 del `2026-10-27`; il testo nella relazione e in `doc/PROGETTO_MITOSI.md` 3(c))*

> **Il mandato:** ### **«l'energia liberata dalla nascita di un nodo sposta lo zero del vuoto uniforme»** *(un'IPOTESI da provare)*. ### **`(0)` IL CONTROLLO: uno spostamento UNIFORME dello zero e' una fase globale: le densita' al bit con e senza, `200` tick;** ### **`(1)` QUANTO SERVE: il `delta` locale che assorbirebbe `Delta E` della nascita** *(`v1`, `v3`)*, ### **`delta = Delta E / (la norma locale)`, `(i)` lo zero del solo vuoto, `(ii)` di tutti i pezzi; in unita' di `lambda* = 1/2`;** ### **`(2)` L'UNIVERSALITA': un profilo locale di `delta`, i pacchetti delle due bande a `eps 0` e `0.5`** *(come `7daa8840`)*, ### **l'accelerazione nei casi `(i)` e `(ii)`, contro la caduta da un gradiente di `s`;** ### **`(3)` la variante PROPORZIONALE all'energia locale.** ### **DEVE: `(0)` al bit. PUO' FALLIRE: `(2)` universale entro il `2%`** *(il guardiano si aspetta NO per l'additivo)*; ### **PUO' FALLIRE: `(3)` universale entro il `2%`.** *([[PROGETTO-MITOSI]], [[D-BILANCIO-NASCITA]], [[VUOTO-SUL-FONDO]])*

**LIVELLO:** una misura in memoria; nessun file del nucleo.

## 0. LA STELLA POLARE

1. **`A14`:** ### **dove va l'energia della nascita.** 2. **Il gradino:** ### **un canale nuovo, e se e' universale** *(il principio di equivalenza)*. 3. **Aggiunge un numero o una legge?** ### **Una legge di PROVA, in memoria** *(lo spostamento locale)*, ### **non nel nucleo.** 4. **Tocca `rho`, `c_s` o il segno?** ### **No.** 5. **Emergente o imposto?** ### **Il profilo e' imposto: si misura come risponde la materia.**

## 1. CHE COSA CREDO, E CHE COSA NON SO

- ### **LO ZERO E' UNA FASE PER UNITA' DI NORMA:** ### **lo zero `lambda` sposta l'energia di `2 pi lambda` per unita' di norma e ruota la fase di `-2 pi lambda s` per tick** *(`0fb93b8c`; e lo zero simmetrico misurato sul vuoto: `-0.9425` per tick a `s 0.3`, `3ceea6a3`)*. ### **UNO SPOSTAMENTO LOCALE `delta_k` e' quindi un POTENZIALE `V_k = 2 pi delta_k` per unita' di norma.**
- ### **`(ii)` su materia e vuoto:** ### **un potenziale uguale per tutti agisce sull'IMPULSO** *(`dk/dt = -dV/dx`)*, ### **e l'accelerazione e' `omega'' dk/dt`: va come la CURVATURA della banda** *(l'inverso della massa efficace)*: ### **NON universale** *(le due bande hanno curvature diverse, anche di segno)*: ### **la previsione del guardiano.**
- ### **`(i)` sul solo vuoto:** ### **una fase sul vuoto non cambia `Lambda` al primo ordine, e la materia sente il vuoto solo attraverso `rho/Lambda`:** ### **credo l'accelerazione NULLA** *(o del secondo ordine)*.
- ### **`(3)` PROPORZIONALE all'energia:** ### **la fase `-s g_k e_k` per tick, con `e_k` l'energia locale per unita' di norma:** ### **`H` diventa `(1 + g) H` localmente, cioe' un tempo locale diverso:** ### **credo che cada come nel gradiente di `cs`** *(Hamilton)*, ### **universale quanto quello.**
- ### ⚠ **NON SO:** ### **se `(0)` passa AL BIT** *(una fase globale moltiplicata e poi la dinamica: l'arrotondamento puo' cambiare l'ultimo bit dei moduli; in `7daa8840` le due convenzioni «uguali» entro `1e-10`, non al bit)*: ### **la soglia «al bit» e' del mandato, e la tengo.**

## 2. LA PROGETTAZIONE *(fissata qui, prima dei numeri; lo script `csv/_zero_del_vuoto.py`)*

1. ### **`(0)`:** ### **il toro a triangoli `L 24`** *(la scena di `C3`, il vuoto uniforme e la coppia a `K`)* ### **col tick intero, `S1`, lo zero simmetrico, `cs` spento, `s 0.3`, `200` tick:** ### **con e senza `delta = 0.1` UNIFORME** *(in unita' di `lambda`, su materia e vuoto)*: ### **`M`, `V`, `rho_k`, `|phi_h|` AL BIT.**
2. ### **`(1)`:** ### **`Delta E` di `v1` e `v3` a `L 24` dal referto di `f7ee87a9`** *(`divisione_vuoto.jsonl`)*; ### **LA NORMA LOCALE = la somma di `Lambda`** *(caso `(i)`)* ### **o di `Lambda + rho`** *(caso `(ii)`)* ### **sui CINQUE NODI della mossa** *(`n`, `i`, `j`, `k`, `l`, dopo la nascita, con il `phi` della regola)*; ### **`delta = |Delta E| / (2 pi norma)`, e `delta/(1/2)`.**
3. ### **`(2)` e `(3)`, LA SCENA:** ### **il toro a striscia `96 x 6`** *(il toro `A` di `7daa8840`: `scena_l2.scena_toro("triangoli", (96, 6), ...)`)*, ### **il vuoto uniforme, il tick intero, `S1`, lo zero simmetrico, `s0 = 0.3`;** ### **i pacchetti di `7daa8840`** *(`_forza_da_cs.pacchetto`, `x0 = Lx/4`, `W = Lx/16`, la banda `Q[:, 0]` di `_triangoli_forza.coppia_K(eps, s0)`, la fase di `K`)*; ### **le due bande, `eps 0` e `0.5`: QUATTRO pacchetti.** ### **IL PROFILO, dichiarato:** ### **`cos(2 pi m1/Lx)` con l'ampiezza `eta = +-1e-2`** *(quello di `7daa8840`: liscio e largo, cosi' il confronto col gradiente di `s` e' alla pari)*.
4. ### **I QUATTRO MECCANISMI:** ### **`(ii)` la fase `e^{-i 2 pi s delta_k}` per tick su `psi` E `phi`, `delta_k = eta cos(...)`;** ### **`(i)` la stessa sul solo `phi`;** ### **`(3)` la fase `e^{-i s g_k e_k}` su `psi` e `phi`, `g_k = eta cos(...)`, `e_k` l'energia per unita' di norma DEL CAMPO al nodo** *(`per_nodo` col campo, diviso la sua densita')*; ### **`(H)` il gradiente di `cs`: `cs = s0 (1 + eta cos(...))`, nessuna fase.** ### **LA FASE SI APPLICA A META' PRIMA E A META' DOPO il tick** *(il palindromo)*.
5. ### **L'ACCELERAZIONE: il differenziale** *(`doc/PATTERN_DI_PROVA.md`, le corse della forza)*: ### **`a = (a(+eta) - a(-eta))/2`, con `a(+-eta)` dal fit di `x(+-eta) - x(0)`** *(`_forza_da_cs.fit_moto`)*; ### **il tempo `T = max(Lx/4, ceil(10 x 2 pi/delta_min))`, la finestra `|dx| < Lx/32`** *(come `7daa8840`)*.
6. ### **L'UNIVERSALITA' di un meccanismo:** ### **le quattro accelerazioni entro il `2%` dalla loro media** *(segno compreso)*.

| | il criterio | il tipo |
|---|---|---|
| `0` | ### **`delta` uniforme: `M`, `V`, `rho_k`, `|phi_h|` AL BIT, `200` tick** | DEVE |
| `2` | ### **l'additivo `(ii)` universale entro il `2%`** | PUO' FALLIRE |
| `3` | ### **il proporzionale universale entro il `2%`** | PUO' FALLIRE |

- ### **LE LETTURE:** ### **`(1)` `delta` contro `1/2`;** ### **`(i)`;** ### **`(H)` la caduta di riferimento** *(e se e' universale lei)*; ### **i rapporti fra i meccanismi.** ### **Se lo zero si muove, l'universalita' che fisso' `lambda* = 1/2` va ricontrollata: si dice nel referto.**

### **Mi FERMO** ### **se `(0)` fallisce** *(lo strumento)*.

## 2-bis. ANNOTAZIONE, PRIMA DELLA CORSA *(la prova di costruzione: `(0)` a `10` tick, `PERIODI 1`: NON il referto)*

- ### **`(0)` USA LA SCENA DEL NUCLEO `L 24`** *(`_scomposizione_solitone.stato_uniforme`, la coppia a `K` uniforme, il vuoto uniforme)*, ### **non il grafo di `C3`** *(`C3` serve solo a `(1)`)*.
- ### **`(3)`: `e_k` = l'energia per unita' di norma allo ZERO SIMMETRICO** *(`per_nodo` / la densita' `+ pi`, la stessa dei conti)*.
- ### ⚠ **I NUMERI GIA' VISTI:** ### **`(0)` FALLISCE AL BIT: `max |d rho| 2.2e-15`, `max |d |phi|| 1.8e-15`** *(l'arrotondamento: lo avevo scritto nel §1 come cio' che NON so)*; ### **la soglia «al bit» e' del mandato e NON la cambio: la corsa vera la misura, e se fallisce mi fermo e lo chiedo.** ### **`(1)` a `L 24`: `v1` `delta 0.057` = `0.11 lambda*`; `v3` `2.4e-4` = `4.8e-4 lambda*`.** ### **Su `24` tick: l'additivo `(ii)` manda le due bande in versi OPPOSTI** *(`+-1.8e-4`)*; ### **il solo vuoto `(i)` `~1e-11`;** ### **il proporzionale entro il `4.9%`, la caduta da `cs` entro il `4.75%`.**

## 3. TODO

1. questo task history, da solo; 2. lo script, committato prima; 3. la corsa e il referto; 4. la relazione, l'indice *(una voce `ZERO-DEL-VUOTO`)*, la mappa.

## 4. IL RISULTATO

- ### **IL REFERTO:** `doc/referti_l2/zero_del_vuoto.{txt,jsonl}` *(`csv/_zero_del_vuoto.py` `sha1-BYTE eaa6a2b1`, committato e pulito; [[ZERO-DEL-VUOTO]])*. ### ⛔ **`0/3`, LA DEVE `(0)` FALLISCE: FERMO.**
- ### ⛔ **`(0)` LO SPOSTAMENTO UNIFORME** *(`delta 0.1` su materia e vuoto, `L 24`, `200` tick)*: ### **`max |d rho| 3.2e-14`, `max |d |phi|| 1.6e-14`: NON al bit** *(l'arrotondamento di una fase globale moltiplicata e poi la dinamica: l'avevo scritto come cio' che non so, e la prova a `10` tick lo aveva gia' mostrato a `2e-15`)*. ### **La soglia «al bit» e' del mandato: non la cambio.** ### **La domanda per Luca:** ### **la `(0)` si riscrive «entro `1e-12` relativo»** *(come per la torsione in fase alle `17:51`)*, ### **o resta fallita?**
- ### **`(1)` QUANTO SERVE** *(`L 24`, la norma sui cinque nodi della mossa)*: ### **`v1`** *(`Delta E -8.548`)*: ### **`delta 0.057` = `0.113 lambda*`** *(il solo vuoto)*, ### **`0.056` = `0.112 lambda*`** *(materia e vuoto)*; ### **`v3`** *(`-0.0453`)*: ### **`2.4e-4` = `4.8e-4 lambda*`.** ### **LA LETTURA: piccolo per `v3`, un decimo dello zero simmetrico per `v1`.**
- ### ⛔ **`(2)` L'ADDITIVO NON E' UNIVERSALE** *(la previsione del guardiano: giusta)*: ### **`(ii)` su materia e vuoto: le due bande cadono in VERSI OPPOSTI** *(`-1.80e-4`, `+1.79e-4`, `-1.70e-4`, `+1.70e-4`: circa `4` volte la caduta da `cs`, col segno della curvatura della banda)*; ### **`(i)` il solo vuoto: `~2.5e-10`** *(`1e-5` della caduta da `cs`: al primo ordine il vuoto non spinge la materia)*.
- ### **`(3)` IL PROPORZIONALE all'energia: entro il `6.1%`** *(`4.46e-5`, `4.35e-5`, `4.01e-5`, `3.98e-5`)*, ### **contro la caduta da `cs` `0.95`-`1.07`:** ### **la PUO' FALLIRE `(3)`** *(entro il `2%`)* ### **FALLISCE;** ### **dalle quattro accelerazioni del referto lo scarto e' soprattutto fra i due `eps`** *(le due coppie `4.46e-5`/`4.35e-5` e `4.01e-5`/`3.98e-5`)*.
- ### **`(H)` LA CADUTA DA UN GRADIENTE DI `cs`, il riferimento: universale entro l'`1.1%`** *(`4.15e-5`, `4.17e-5`, `4.20e-5`, `4.11e-5`)*.
- ### **CHE COSA VUOL DIRE** *(una lettura)*: ### **uno spostamento dello zero ADDITIVO e' un potenziale uguale per tutti: accelera secondo la massa efficace della banda, e le due bande in versi opposti;** ### **non puo' essere il canale della gravita' universale.** ### **Lo spostamento PROPORZIONALE all'energia e' un tempo locale: si avvicina alla caduta da `cs`, ma non la eguaglia** *(il `6%` contro l'`1%`)*. ### **L'universalita' che fisso' `lambda* = 1/2`:** ### **non e' toccata da questa misura** *(lo zero qui e' imposto, non mosso dalla nascita)*.
- ### **LA MAPPA** *(nello stesso commit)*: ### **la coda: lo zero FATTO col FERMO; poi il solitone con la sua buca.**

## 5. LA CHIUSURA (Luca, 2026-10-28 08:31)

- ### **LA DEVE `(0)` CORRETTA DOPO I NUMERI** *(Luca, `2026-10-28` `08:31`; come per la torsione in fase, `11410186`)*: ### **«al bit» diventa «entro `1e-12` relativo».** ### **Rivalutata sul jsonl** *(`doc/referti_l2/zero_del_vuoto_c0.txt`, `csv/_zero_del_vuoto_c0.py` `sha1-BYTE 80bbb052`; le scale dichiarate: il massimo di `rho_k` e di `|phi_h|` dello stato iniziale, entrambi `1`)*: ### **`3.186e-14` e `1.643e-14` relativo: PASSA.** ### **L'esito dopo la correzione: `1/3`, nessuna DEVE fallita** *(le due PUO' FALLIRE `(2)` e `(3)` restano fallite)*.
- ### ⛔ **LA CHIUSURA DELL'IPOTESI** *(Luca, `08:31`)*: ### **lo spostamento dello zero del vuoto come «canale di gravita'» SI CHIUDE.**
  - ### **`(a)` lo spostamento ADDITIVO** *(tutti i pezzi)* ### **NON e' gravita':** ### **le due bande accelerano in versi opposti** *(`-1.80e-4` / `+1.79e-4`)*, ### **come una particella e un'antiparticella in un potenziale elettrico.** ### **Annotato in [[DOMANDA-BANDA-ANTIMATERIA]]:** ### **per un potenziale additivo le due bande si comportano gia' come cariche opposte** *(una lettura, NON una misura della carica)*.
  - ### **`(b)` lo spostamento del SOLO vuoto non spinge la materia** *(`~2.5e-10`)*.
  - ### **`(c)` lo spostamento PROPORZIONALE all'energia e' quasi universale** *(`6.1%`, la differenza dipende da `eps`)* ### **ma meno della caduta da `cs`** *(`1.1%`)*: ### **equivale a un ritmo del tempo locale, cioe' a un altro modo di scrivere `cs`, meno pulito.** ### **Il canale della gravita' resta `cs`.**
  - ### **`(d)` il `delta` che servirebbe:** ### **`0.113 lambda*` per la nascita `v1`, `4.8e-4 lambda*` per `v3`.**
- ### ❓ **RESTA APERTA** *(in `doc/PROGETTO_MITOSI.md` 3(c))*: ### **«dove va l'energia della nascita»,** ### **con la nota che il vuoto del FONDO prende energia dalla materia** *(`76eecbf5`)* ### **e che li' va riprovata.**
- ### **La voce [[ZERO-DEL-VUOTO]] e' CHIUSA** *(il criterio: la decisione di Luca delle `08:31` su `43c3a298`)*; ### **la mappa aggiornata nello stesso commit;** ### **il prossimo in coda: il solitone con la sua buca** *(`22:59`)*.
