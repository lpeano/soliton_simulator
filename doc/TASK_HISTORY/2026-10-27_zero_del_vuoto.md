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
