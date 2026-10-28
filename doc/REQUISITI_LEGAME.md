# I REQUISITI DEL LEGAME MATERIA-VUOTO E LA STABILITA' DEI SOLITONI SULLA CARTA *([[DECISIONE-LINEARE]], [[PIANO-2D-3D]]; il mandato di Luca del `2026-10-28`, `19:18`)*

> **Nessuna scelta fra `S1` e `S4`: resta di Luca.** I referti: `doc/referti_l2/requisiti_legame.txt` *(lo script `sha1-BYTE e62182ea`, `2b3f1421`; `17/17`)*;
> la parte `2`: `doc/referti_l2/diagnosi_s4.txt` *(lo script `9e8805ba`)*. Il task history: `doc/TASK_HISTORY/2026-10-28_requisiti_legame.md`.

## 1. LE PREMESSE DAL CODICE

| | `S1` | `S4` |
|---|---|---|
| `alpha(x)` *(`_screening_forme_s3._ab`)* | `x^2/(1+x^2)` | `pi (x^p - 1)/(x^p + 1)`, `p = 2/pi` |
| `alpha(0)` | `0` | `-pi` |
| il tetto di `alpha - alpha(0)` | `1` | `2 pi` |
| `sigma_eff = d ln(alpha - alpha(0))/d ln x` | `2/(1+x^2)` | `p/(1+x^p)` |

- **L'equazione dell'inviluppo** *(`_gravita_collettiva.profilo`)*, adimensionale: `lap v + (alpha(v^2) - alpha(0)) v = nu v`, `xi = r/l`, `l = sqrt(|c|/s)`, `x = v^2`,
  `nu = mu/s - alpha(0)`, `n = N/(Lambda0 l^d)`. **`c` e `s` fissano solo la scala:** il segno di `dn/dnu` dipende dalla forma e da `d`.
- **La convenzione di VK, dal risolutore:** `mu` riportato `= -<H>` per `c < 0`, cioe' la frequenza `omega`; **stabile se `dN/dmu > 0`**.
- **La curvatura in 3D:** non misurata *(`doc/PROGETTO_FCC.md`)*; entra solo nella colonna `N` del 3D, con la `c` dei triangoli a `s 0.3` come parametro.

## 2. I CRITERI E I CONTROLLI *(`17/17`)*

| controllo | esito |
|---|---|
| `sigma_eff` dal codice = la formula chiusa | `3.4e-10` |
| R6 per `S1` e `S4` *(con l'arrotondamento stimato)*; una `beta` rotta | passano; la rotta risulta rotta |
| il logaritmo esatto, `d 2` e `3`, `nu -1, 0, 1` | entro `1e-6` |
| Townes, `d 2` | `n 11.700897` |
| le potenze `x^1` (3D), `x^0.5` (3D), `x^2` (2D): l'esponente `1/sigma - d/2` | `-0.50000`, `+0.50000`, `-0.50000`; le due negative risultano instabili |
| il tiro in 2D contro i punti del risolutore di `bcbd1f40` *(`S1`, `S4`; `s 0.3`, `0.99`; `lam0 6`, `4`)* | `n` entro `8.4e-07` |

## 3. (a) I REQUISITI

| | il requisito | `S1` | `S4` | fonte |
|---|---|---|---|---|
| R1 | `rho dalpha/drho -> 0` a poca materia | si' | si' | `8917b0a2`, `e345cd8f` |
| R2 | `alpha(0) = 0`: la particella nuda, lo zero simmetrico | si' *(entro `2e-13`)* | **NO** *(`alpha(0) = -pi`: riporta allo zero di oggi)* | `92c63912`; `DOSSIER_S1_S4.md` 5, 6 |
| R3 | la materia diluita stabile | si' *(stato uniforme; vuoto a `Gamma`; vestita a `K` fino a `x 1e-2`, instabile a `x 0.1`)* | **NO** | `c4efc937`, `77f9f850`, `92c63912` |
| R4 | un solitone largo e stabile in 2D | **sulla carta si'** *(ramo `dn/dnu > 0` sopra `n 22.9`; i misurati tutti sopra)*; **in dinamica:** col tick intero si disfa *(`320` tick)*; col congelato vero non scappa, il cuore si svuota frenando | **sulla carta si'** *(`dn/dnu > 0` su tutta la griglia)*; solo stretti *(`<= 3.1` archi)*; la dinamica: la parte `2` | `bcbd1f40`, `40061005`, `9a1695b5`; qui |
| R5 | un solitone stabile in 3D | **sulla carta si'** sopra `n 169` *(`N ~ 87` col parametro)*, sotto instabile | **sulla carta si'** su tutta la griglia | qui; nessuna misura 3D |
| R6 | la coerenza con l'energia | si': `alpha`, `beta` da una primitiva *(qui)*; la rotazione gemella *(`acbdfb88`)* | `alpha`, `beta` da una primitiva *(qui)*; la rotazione gemella NON misurata | `acbdfb88`; qui |

## 4. (b) L'ESPONENTE EFFICACE E IL CUORE

| `x` | `1e-6` | `1e-2` | `1` | `1e2` | `1e3` | `1e4` |
|---|---|---|---|---|---|---|
| `sigma_eff` `S1` | `2.000` | `2.000` | `1.000` | `2.0e-4` | `2.0e-6` | `2.0e-8` |
| `sigma_eff` `S4` | `0.637` | `0.604` | `0.318` | `0.032` | `7.7e-3` | `1.8e-3` |

Il critico: `1` in 2D, `2/3` in 3D. `S4` a `x -> 0`: `0.6366 < 2/3`.

| il solitone | `x` al centro | `sigma_eff` li' |
|---|---|---|
| `S1`, `s 0.3`, `N 1e2` .. `1e7` *(`bcbd1f40`, `lam0 6`)* | `6.7` .. `3153` | `4.4e-2` .. `2.0e-7` |
| `S4`, `s 0.3`, `N 1e1` .. `1e7` | `2.3` .. `4.7e4` | `0.23` .. `6.7e-4` |
| `S1` congelato lungo `L 81`, tick `0` e `10000` *(`40061005`)* | `979` e `703` | `2.1e-6` e `4.1e-6` |

**Il cuore di tutti i solitoni misurati vive dove `sigma_eff` e' molto sotto `2/d`:** il regime saturato.

## 5. (c) VK IN 2D E (d) IL 3D, SULLA CARTA

| | `n` minimo sulla griglia | dove *(`nu`/tetto)* | `dn/dnu` |
|---|---|---|---|
| `S1`, `d 2` | `22.87` | `0.1` | `< 0` sotto, `> 0` sopra |
| `S4`, `d 2` | `0.0185` | `1e-4` *(il bordo della griglia)* | `> 0` ovunque |
| `S1`, `d 3` | `169.0` *(`N 86.8` col parametro)* | `0.1` | `< 0` sotto, `> 0` sopra |
| `S4`, `d 3` | `2.384` | `1e-4` *(il bordo)* | `> 0` ovunque |

- I solitoni `S1` misurati *(`N >= 100`, `nu/tetto >= 0.54`)* stanno sul ramo `dn/dnu > 0`.
- **La corsa lunga di `S1`** *(`40061005`, `9a1695b5`)*: non scappa, il cuore si svuota frenando. **VK sull'inviluppo dice "stabile" per quello stato:** lo svuotamento non e' l'instabilita' di VK dell'inviluppo.

## 6. (e) LA LETTURA FINALE *(informazione per Luca, nessuna proposta)*

- `S1` soddisfa R1, R2, R3, R6; R4 e R5 **sulla carta** *(sopra `n` minimo)*; R4 in dinamica no ancora.
- `S4` soddisfa R1, R6 *(la primitiva)*; R4, R5 sulla carta; **R2 e R3 no.**
- **La forma "`x^2` a poca materia, saturazione nel cuore" e' gia' `S1`:** `sigma_eff = 2` sotto `x 1e-2`, `2/(1+x^2)` sopra; il tetto `1`.
- Per `S1` l'ostacolo che resta per R4 non e' la stabilita' dell'inviluppo: e' fuori dall'equazione dell'inviluppo *(la dinamica del passo sul reticolo)*.

## 7. LA DIAGNOSI DI `S4` *(parte `2`)*

In corsa *(`9e8805ba`)*: si scrive col referto.

## 8. LE DOMANDE PER LUCA

Si scrivono col referto della parte `2`.
