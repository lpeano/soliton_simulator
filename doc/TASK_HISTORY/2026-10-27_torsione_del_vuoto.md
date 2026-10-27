# LA TORSIONE DEL VUOTO SUGLI ARCHI, ATTORNO AL SOLITONE `S1` *(l'aggiunta al libro dei conti, `13:06`-`13:09`; la risposta di Luca delle `13:46`: subito, prima dello strumento)*

> **Il mandato:** ### **la misura scritta nell'aggiunta al libro dei conti** *(`doc/PROGETTO_MITOSI.md` 3(a), l'ipotesi di Luca e del guardiano; [[PROGETTO-MITOSI]], [[LIBRO-DEI-CONTI]], [[ENERGIA-DEL-LEGAME]])*: ### **sulla corsa del solitone `S1` col tick intero** *(`N 1e5` `L 48`, `N 1e6` `L 81`, lo zero simmetrico, `2000` tick, `cs` spento e acceso a `lambda_c = Lambda`)*: ### **per ogni arco la torsione `(a3)` srotolata nel tempo; il ritmo contro la distanza dal solitone e contro la differenza di `cs` ai capi; il primo arco e il primo tick a `2 pi`, quanti archi ci arrivano; il ritmo contro la differenza di energia del vuoto ai capi; il freno: il ritmo costante o calante nel tempo.** ### **Nessuna nascita, solo la misura; nessun freno inventato.**
> ### **In memoria; nessun file del nucleo; B-4, B-5 e l'impronta `2e7f795d2a52fbe7` intatte.**

**LIVELLO:** una misura.

## 0. LA STELLA POLARE

1. **`A14`:** ### **la torsione e' una fase; il confronto con l'energia del vuoto ai capi e' un conto.** 2. **Il gradino:** ### **dove la mitosi scatterebbe, prima di accenderla.** 3. **Aggiunge un numero o una legge?** ### **No: la soglia `2 pi` e' quella dell'era `1`, qui solo LETTA.** 4. **Tocca `rho`, `c_s` o il segno?** ### **No: `cs` acceso col tick del nucleo** *(`tick.tick_con_cs`)*, ### **come in `_vuoto_disturbato`.** 5. **Emergente o imposto?** ### **Si misura se la torsione cresce dove `cs` cambia.**

## 1. CHE COSA CREDO PRIMA DI GUARDARE, E CHE COSA NON SO

- ### **LA DEFINIZIONE** *(`(a3)` di `PROGETTO_MITOSI`)*: ### **il vuoto vive sulle estremita': `phi_h` ha due slot per arco** *(`flussi_parziali.hop_phi`: `phi.reshape(m, 2)`, il lato `0` al nodo `inc.nodo[2a]`, il lato `1` a `inc.nodo[2a+1]`)*; ### **la torsione dell'arco `a` e' `theta_a = arg(conj(phi_h[2a+1]) phi_h[2a])`,** ### **srotolata nel tempo tick per tick** *(il contatore dei giri)*. ### **Il vuoto e' neutro** *(nessuna `U`)*, ### **quindi `theta_a` e' invariante per una fase globale, e per lo zero `lambda`** *(lo spostamento `2 pi lambda` e' lo stesso ai due capi)*.
- ### **Credo:** ### **senza materia, col vuoto uniforme, `theta_a = 0` al bit per sempre** *(ogni estremita' fa le stesse operazioni)*; ### **col solitone, l'accoppiamento materia-vuoto** *(`materia_vuoto.applica`: `beta` su `phi`, che dipende da `rho`)* ### **sfasa le estremita' dove `rho` cambia da un capo all'altro: la torsione cresce sul BORDO del solitone, anche con `cs` spento.**
- ### ⚠ **NON SO:** ### **se con `cs` acceso la torsione segue `Delta cs`** *(l'ipotesi)* ### **o segue `rho`** *(l'accoppiamento)*: ### **i due sono correlati fra loro** *(`cs` segue `Lambda`, e `Lambda` cambia dove la materia c'e')*, ### **quindi una correlazione con `Delta cs` NON separa le due cause da sola:** ### **il confronto con `cs` spento e' quello che separa.**
- ### ⚠ **NON SO** ### **se il punto fisso di `cs` converge col solitone** *(in `_vuoto_disturbato` girava sul vuoto da solo)*: ### **se `tick_con_cs` ALZA, lo riporto e mi fermo su quella corsa.**
- ### ⚠ **NON SO** ### **se il ritmo per tick sta sotto `pi`** *(lo srotolamento lo vuole)*: ### **lo controllo a ogni tick.**

## 2. LA PROGETTAZIONE *(le letture fissate qui, prima dei numeri)*

1. ### **LE SCENE:** ### **le righe di `_energia_del_legame.stato`** *(importate, non copiate)*, ### **`fattore 12`** *(`N 1e5` -> `L 48`, `N 1e6` -> `L 81`)*, ### **la forma `S1`, lo zero simmetrico** *(`BE.conv(0.5)`)*, ### **`T_MAX 2000`.** ### **`cs` SPENTO: `tick.percorri_tick`** *(come `_energia_del_legame.corsa`, modo intero)*; ### **`cs` ACCESO: `tick.tick_con_cs(st, mot, par, lc, ())` con `lc` = la media di `Lambda` per nodo a `t 0`** *(`RAPPORTO 1`, come `_vuoto_disturbato`)*.
2. ### **LA TORSIONE:** ### **a ogni tick `z_a = conj(phi[2a+1]) phi[2a]`, l'incremento `d_a = arg(z_a(t) conj(z_a(t-1)))`, `theta_a += d_a`.** ### **IL RITMO dell'arco: `omega_a = theta_a(T_MAX)/T_MAX`** *(radianti per tick)*; ### **e per finestre di `250` tick** *(il freno)*.
3. ### **LA DISTANZA:** ### **`r_a` = la media delle distanze dal centro dei due nodi** *(`rr` di `stato`)*; ### **le classi di larghezza `1`.** ### **`VICINO` = `r_a <= 2 w_in`** *(come in `15df5c63`)*.
4. ### **`Delta cs_a = |cs(nodo 2a) - cs(nodo 2a+1)|`, mediato su tutti i tick** *(con `cs` spento e' zero)*; ### **`Delta e_vuoto_a` = la stessa cosa per l'energia del vuoto per nodo** *(`_energia_del_legame.per_nodo(..., "psi_h")`)*, ### **mediata ogni `10` tick** *(costa)*.
5. ### **`2 pi`:** ### **il primo tick in cui un arco ha `|theta_a| >= 2 pi`, quell'arco** *(la sua `r_a`)*, ### **e quanti archi ci sono arrivati a `T_MAX`.**

| | il criterio | il tipo |
|---|---|---|
| `s1` | ### **lo srotolamento, su fasi SINTETICHE: un ritmo di `0.7` rad per tick ridà `0.7` entro `1e-12`** | DEVE |
| `s2` | ### **un ritmo di `3.5` rad per tick** *(oltre `pi`)* ### **lo fa scattare la guardia** *(`max |d| > pi/2`)* | DEVE |
| `0` | ### **il vuoto UNIFORME senza materia** *(`N 0`, `L 48`, `2000` tick, `cs` spento e acceso)*: ### **`max |theta_a| = 0` al bit** *(la previsione del guardiano)* | DEVE |
| `g` | ### **in ogni corsa col solitone: `max |d_a| < pi/2` su tutti gli archi e tutti i tick** *(lo srotolamento e' valido)* | DEVE |
| `1` | ### **con `cs` acceso, il ritmo e' MASSIMO vicino al solitone:** ### **la classe di distanza con la media di `|omega_a|` piu' alta sta in `VICINO`** *(a ogni `N`)* | PUO' FALLIRE |
| `2` | ### **con `cs` acceso, il ritmo e' proporzionale a `Delta cs`:** ### **la correlazione di Pearson fra `|omega_a|` e `Delta cs_a` sopra `0.9`** *(a ogni `N`)* | PUO' FALLIRE |

- ### **LE LETTURE** *(nessuna soglia)*: ### **il ritmo contro la distanza** *(`cs` spento e acceso)*; ### **la correlazione con `Delta e_vuoto`** *(spento e acceso)*; ### **il primo arco e tick a `2 pi`, il conto;** ### **il freno: la media di `|omega|` per finestra di `250` tick, in `VICINO` e in tutto il toro: costante, calante o crescente;** ### **il confronto spento/acceso** *(se con `cs` spento la torsione e' la stessa, la causa non e' `cs`)*.

### **Mi FERMO** ### **se `s1`, `s2`, `0` o `g` fallisce** *(lo strumento non misura la torsione)*, ### **o se il punto fisso di `cs` ALZA** *(lo riporto, e la corsa con `cs` spento resta)*.

## 2-bis. ANNOTAZIONE, PRIMA DELLA CORSA *(la prova di costruzione a `60` tick, `N 1e5` soltanto: NON il referto)*

- ### **IL CONTROLLO `0` SENZA MATERIA:** ### **il profilo del solitone non si risolve a norma zero** *(`_gravita_collettiva.profilo`: `NaN`)*: ### **il controllo usa la scena di `N 1e5` con la materia messa a zero** *(lo stesso toro `L 48`)*. ### **A `60` tick: `max |theta| = 0` al bit, `cs` spento e acceso.**
- ### ⚠ **I NUMERI GIA' VISTI, DICHIARATI:** ### **`(i)` con `cs` SPENTO la guardia SCATTA: l'incremento massimo per tick `3.13`** *(quasi `pi`)*; ### **`390` archi su `6912` oltre `pi/2`, a `r` da `5.8` a `10.8`** *(il bordo del solitone, `w_in 3.81`)*, ### **col loro `|z|` minimo da `1.2e-3` a `0.20`:** ### **non solo fasi vicino a uno zero del modulo: la fase relativa GIRA piu' in fretta di quanto un tick risolva.** ### **`(ii)` con `cs` ACCESO il punto fisso di `cs` NON CONVERGE GIA' AL TICK `0`** *(`120` giri, l'ultimo scarto `0.217`)*: ### **`tick.tick_con_cs` ALZA.**
- ### **LE SOGLIE NON CAMBIANO.** ### **Lo script ha in piu' la diagnosi della guardia** *(gli archi oltre `pi/2`: quanti, a che `r`, col loro `|z|` minimo)* ### **e il tick a cui il punto fisso alza.** ### **La corsa si fa intera per documentare le due fermate a piena taglia** *(`N 1e6` `L 81` compreso)*; ### **le fermate del §2 restano:** ### **se `g` fallisce o il punto fisso alza, il referto lo dice e mi FERMO.**

## 3. TODO

1. questo task history, da solo; 2. lo script `csv/_torsione_del_vuoto.py`, committato prima della corsa; 3. la corsa; 4. il referto, la relazione, l'indice (una voce `TORSIONE-DEL-VUOTO`).

## 4. IL RISULTATO

- ### **IL REFERTO:** `doc/referti_l2/torsione_del_vuoto.{txt,jsonl}` *(`csv/_torsione_del_vuoto.py` `sha1-BYTE e4a4291a`, committato e pulito; l'impronta `2e7f795d2a52fbe7` intatta)*. ### ⛔ **`3/6`, LA DEVE `g` FALLISCE: FERMO.**
- ### **I CONTROLLI PASSANO:** ### **`(s1)` il ritmo sintetico `0.7` rad per tick si srotola esatto;** ### **`(s2)` a `3.5` la guardia scatta;** ### **`(0)` il vuoto uniforme senza materia: la torsione `0` al bit per `2000` tick, `cs` spento e acceso.**
- ### ⛔ **LA DEVE `g` FALLISCE: LO SROTOLAMENTO TICK PER TICK NON E' VALIDO.** ### **Con `cs` spento l'incremento massimo per tick e' `pi`** *(`3.1416`)* ### **a tutte e due le taglie;** ### **oltre `pi/2`: `5794` archi su `6912`** *(`N 1e5` `L 48`, `r` da `0.5` a `40.3`)* ### **e `15535` su `19683`** *(`N 1e6` `L 81`)*; ### **il loro `|z|` minimo va da `1.5e-5` a `0.14`:** ### **non solo fasi vicino a uno zero del modulo; la fase relativa delle estremita' gira piu' in fretta di quanto un tick risolva** *(nella prova a `60` tick erano `390` archi, sul bordo del solitone a `r` `5.8`-`10.8`: col tempo il gas porta il fenomeno su tutto il toro)*. ### **QUINDI I RITMI, IL PRIMO ARCO A `2 pi`, IL FRENO E LE CORRELAZIONI DEL REFERTO NON SI LEGGONO** *(sono scritti, ma uno srotolamento con incrementi a `pi` e' ambiguo di un giro per tick)*.
- ### ⛔ **CON `cs` ACCESO IL PUNTO FISSO NON CONVERGE GIA' AL TICK `0`** *(`120` giri; l'ultimo scarto `0.217` a `N 1e5`, `0.265` a `N 1e6`; [[PUNTO-FISSO-CS-SOLITONE]])*: ### **le corse con `cs` acceso non esistono, e le due PUO' FALLIRE del guardiano** *(il ritmo massimo vicino al solitone; la proporzionalita' a `Delta cs`)* ### **sono scritte «FALLISCE» dallo script ma sono NON MISURATE.** ### **Sul vuoto da solo il punto fisso converge** *(il controllo `0`; `_vuoto_disturbato`)*: ### **e' la materia che lo rompe.**
- ### **LE DOMANDE PER LUCA** *(nessuna scelta presa)*: ### **`1` LA TORSIONE:** ### **lo srotolamento vuole un campionamento piu' fine del tick** *(per esempio dopo ogni pezzo del palindromo, come la strada `B`)*, ### **o una finestra limitata alla vita del solitone** *(dove il fenomeno era sul bordo)*, ### **o un'altra grandezza** *(`(a1)`-`(a5)` di `PROGETTO_MITOSI`)*? ### **`2` IL PUNTO FISSO DI `cs` COL SOLITONE:** ### **come si procede** *(lo schema del punto fisso e' una scelta tua; il nucleo dice di relazionare)*? ### **Il criterio di chiusura: le due risposte.**
- ### **LA CODA, DOPO LE RISPOSTE:** ### **`(c)` lo strumento del libro dei conti** *(`A` + `B`)* ### **non dipende dalla torsione:** ### **posso cominciarlo mentre aspetto?** ### **Per la regola** *(un sigillo fallito: commit e FERMO)* ### **non lo comincio senza un tuo si'.**

## 5. CORREZIONE *(dopo il referto; trovata dalla torsione in forma d'energia)*

- ### ⛔ **UN MIO ERRORE:** ### **`BE.conv(LAM_ZERO)` con `LAM_ZERO = 0.5` da' la convenzione di OGGI** *(`_triangoli_bassa_energia.conv` prende il nome, `"simm"`)*: ### **i referti `76e85c0a` e `9a8f9afa` dicono «lo zero simmetrico» e sono allo zero di OGGI.** ### **La torsione e' una fase RELATIVA, e la convenzione cambia la dinamica per una fase globale** *(`762cb0e8`: `2 pi lambda` entro `8.9e-15`)*: ### **mi aspetto gli stessi numeri a meno dell'arrotondamento** *(ma con incrementi a `pi` l'arrotondamento puo' cambiare lo srotolamento)*. ### **Corretto lo script** *(`ZERO = "simm"`)*; ### **la corsa si rifa, e il referto lo dice.**
