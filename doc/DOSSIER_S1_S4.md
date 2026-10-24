# IL DOSSIER S1 CONTRO S4 *(gli argomenti per [[DEC-FC-COESIONE]]: tutti quelli gia' MISURATI, e nessuna decisione)*

> ### ⛔ **NESSUNA SCELTA E' FATTA QUI.** ### **La scelta fra `S1` e `S4` e' di Luca** *(`DEC-FC-COESIONE`, `presa: false`; con lei `DEC-D7-DIVISIONE`)*. ### **La nota del nodo nell'albero NON si tocca:
> questo documento raccoglie gli argomenti.** ### **Le forme:** ### **`S1` = `x - arctan x`, accoppiamento `2 x^2/(1 + x^2)^2`; `S4` = la forma chiusa di `primo_ordine/_deriva_forme_l2.py`, `alpha_4 = pi (x^p -
> 1)/(x^p + 1)`, `p = 2/pi`, accoppiamento `4 x^p/(1 + x^p)^2`** *(`_screening_forme_s3._ab`, `acc_mano`)*. ### **NESSUNA delle due e' DERIVATA** *(`doc/TASK_HISTORY/2026-10-22_lineare_s1_s4.md`)*.
>
> ### ⚠ **L'avvertenza:** ### **tutto sotto e' MISURATO salvo dove e' scritto «previsione»;** ### **i risultati sul QUADRATO sono marcati da rifare sui triangoli** *([[DECISIONE-SOLO-TRIANGOLI]])*.

## 1. IL CRITERIO DI LUCA E CHE COSA LASCIA *(DECISIONE-LINEARE)*

- ### **«con poca materia, l'accoppiamento efficace fra materia e vuoto deve andare a zero»: ESCLUDE `S2` e `S3`, lascia `S1` e `S4`** *(`8917b0a2`, la voce `DECISIONE-LINEARE`)*.
- ### **I controlli `13/13`** *(`e345cd8f`)*: ### **l'accoppiamento del codice = la formula a mano entro `5.7e-10`; a `x 0.01`: `S1 1.9996e-4`, `S4 1.9218e-1`** *(`~1000` volte)*; ### **a `x 1` `S1 0.5`, `S4 1.0`.**
- ### **La scala `12/12`** *(`cb846b2a`)*: ### **per tutte e due l'instabilita' che resta e' FISSA IN ARCHI** *(un artefatto del reticolo)*; ### **`gamma` `S1 0.0057`, `S4 0.297`.**
- ### **La materia `15/16`** *(`b16e58ba`; quadrato, R2)*: ### **`gamma` a `x 0.01, 0.1, 0.3, 1, 3`: `S1 0.000, 0.0057, 0.105, 0.653, 0.569`; `S4 0.079, 0.297, 0.580, 1.229, 2.696`.**
- ### **Con `cs`** *(`974d411a`)*: ### **R1 `S1 0.402`, `S4 0.443`: l'instabilita' del sistema completo viene da `cs` e dalla fase del vuoto, non dal legame** *(la voce `CANALE-CS-SECONDA-SORGENTE`)*.

## 2. LA STABILITA'

| dove | `S1` | `S4` | fonte |
|---|---|---|---|
| lo screening, R2, `x 1e-4` *(quadrato / triangoli)* | `0.0000` / `0.0000` | `0.0014` / `0.0010` | `389093bc` |
| lo screening, `x 0.1` | `0.0048` / `0.0037` | `0.2971` / `0.2831` | `389093bc` |
| lo stato uniforme, quadrato | l'UNICO stabile *(`x 0.01`, `40` stati su `360`)* | instabile gia' a `x 0.01` | `c4efc937` |
| i triangoli, il vuoto accoppiato a `Gamma` | stabile *(`<= 3.3e-6`)* | `0.011`-`0.19`, crescente con `x` | `77f9f850` |
| i triangoli, la particella vestita a `K` | stabile fino a `x 1e-2`, instabile a `x 0.1` | instabile quasi ovunque *(stabile solo banda alta, `eps 0.5`, `x 1e-4`)* | `92c63912` |

## 3. IL LEGAME E I SOLITONI *(quadrato)*

- ### **Il legame collettivo** *(`c4efc937`)*: ### **`S1` lega solo a `N 100`** *(`7` su `60`)*, ### **`S4` da `N 10`** *(`17` su `60`)*; ### **nessuna delle due ha `D = 0`.** ### **La teoria scritta la':
  `S4` va come `x^{2/pi}`, sotto-critica in 2D, legata; `S1` come `x^2`, sopra-critica in 2D** *(il caso critico del 2D: i solitoni si giudicano in 3D, `doc/PIANO_2D_3D.md`)*.
- ### **I solitoni larghi** *(`9a6955f3`; almeno `4` archi)*: ### **`S1` gia' a `s 0.3`** *(`N 1e5`-`1e7`: larghezze `4.24`, `7.46`, `13.20`; `mu +0.2955`..`+0.2995`)*; ### **`S4` solo da `s 0.7`** *(`N 1e7`: `4.03`, `mu +2.17`)*; ### **`S3` solo a `s 0.99`.**
- ### **La risposta statica** *(`ebf5317a`)*: ### **`beta ~ x^3` per `S1`, `~ x^1.64` per `S4`**: ### **«una forma che a `x` piccolo si allontana dal lineare E' IN TENSIONE CON LE OSSERVAZIONI, ma il `x` della materia reale non e' noto».**

## 4. IL SEGNO DEL LEGAME RISPETTO ALLA CURVATURA *(e il verso della caduta del solitone)*

- ### ⚠ **NESSUNA MISURA DINAMICA:** ### **la parte D di «il segno della gravita'» si e' FERMATA** *(nessun solitone largo `>= 4` archi a quelle `s`: `e31366ec`)*, ### **e la C.3 di `9a6955f3` NON e' stata eseguita**
  *(`f79d2cd4`, la griglia quadrata dopo [[DECISIONE-SOLO-TRIANGOLI]])*.
- ### **LA PREVISIONE DI HAMILTON** *(`doc/TASK_HISTORY/2026-10-23_segno_gravita.md`)*: ### **con lo zero di oggi `a/a_RG = -mu/Dt`: `S1` (`mu > 0`) verso `cs` ALTO; con lo zero simmetrico `a/a_RG = -(s/Dt)(pi + mu/s)`.**
  ### **I segni misurati di `mu`: `S1` sempre `> 0`; `S4` `< 0` a `N` piccolo, `> 0` a `N` grande.** ### **«Il verso sbagliato» per `S1` e' dunque una PREVISIONE, non un'osservazione.**

## 5. LA PROPRIETA' DI `S4` A DENSITA' NULLA *(`92c63912`; registrata il `2026-10-24`)*

- ### **IL FATTO, dalla formula:** ### **`alpha_4(x) = pi (x^p - 1)/(x^p + 1)`, `p = 2/pi > 0`: a `x -> 0` `x^p -> 0`, quindi `alpha_4 -> -pi`** *(`-3.14154` a `x 1e-8`)*; ### **`beta_4 -> 0`** *(come `x^{1 + 2/pi}`)*; ### **l'accoppiamento
  `x alpha_4' -> 0`** *(il criterio di Luca e' rispettato: e' la FASE a non spegnersi, non l'accoppiamento)*. ### **`S1`: `alpha_1 = x^2/(1 + x^2) -> 0`.**
- ### **IL FATTO, misurato:** ### **a `x 1e-8` la particella vestita con `S1` = la nuda entro `2e-13`; con `S4` NO** *(`0.73`-`0.75` sulla banda bassa, `v_b` non definita sulla alta)*: ### **il DEVE della parte `C` di
  `92c63912` RESTA FALLITO** *(il criterio non cambia)*, ### **ed e' una PROPRIETA' FISICA della forma `S4`, non un difetto della misura.**
- ### ⚠ **UNA DISCONTINUITA' DEL CODICE** *(dal sorgente: `_screening_forme_s3.pezzi_di`, `vivi = rho > 0.0`)*: ### **a `rho = 0` ESATTO la fase e' `0`; a `rho` piccolissimo ma positivo e' `~ -pi`.** ### **Con `S1` il limite e' continuo.**

## 6. LA VERIFICA DEL SEGNO *(l'osservazione del guardiano: «se ha anche il segno che lo annulla, `S4` riporta la materia allo zero NON universale»)*

### **SULLA CARTA, dalle due definizioni:**
1. ### **Il legame mette su `psi` la fase `exp(-i alpha dtau)` per tick** *(`primo_ordine/materia_vuoto.applica`: `exp(-i al dtau f)` due volte, `f = 0.5`)*: ### **con `alpha_4(0) = -pi` e `dtau = s`, `psi -> e^{+i pi s} psi`.**
2. ### **Lo zero simmetrico e' `A_simm = e^{-i pi s} A_oggi`** *(`6e022419`)*, ### **quindi `A_oggi = e^{+i pi s} A_simm`.**
3. ### **Un tick col simmetrico e `S4` a densita' nulla:** ### **`e^{+i pi s} A_simm psi = A_oggi psi`.**

### **L'ESITO: IL SEGNO E' QUELLO CHE ANNULLA LO ZERO SIMMETRICO.** ### **Con lo zero simmetrico, `S4` riporta la MATERIA allo zero di oggi, quello NON universale;** ### **il VUOTO no** *(`beta_4(0) = 0`)*. ### **Con
lo zero di oggi** *(la convenzione del repo)* ### **`S4` aggiunge un altro `e^{+i pi s}`.** ### **Il numero lo conferma:** ### **in `92c63912` a `x 1e-8` `omega(0)` con `S4` e' `-0.48448` e `-1.40045`** *(le due bande,
`eps 0`, `s 0.3`)* ### **contro i valori di OGGI della stessa coppia `-0.48450` e `-1.40046`.**

## 7. IN SINTESI *(argomenti, non una scelta)*

| | `S1` | `S4` |
|---|---|---|
| il criterio di Luca *(accoppiamento -> 0)* | si' | si' |
| torna alla particella nuda a densita' nulla | si' *(`2e-13`)* | NO *(`alpha_4(0) = -pi`: riporta allo zero di oggi)* |
| stabile a poca materia | si' *(quadrato e triangoli)* | quasi stabile a `x 1e-4`, instabile sopra |
| lega a `N` piccolo *(quadrato)* | no *(da `N 100`)* | si' *(da `N 10`)* |
| solitoni larghi | da `s 0.3` | da `s 0.7` |
| il verso della caduta del solitone | NON misurato *(previsione: verso `cs` alto con lo zero di oggi)* | NON misurato |
