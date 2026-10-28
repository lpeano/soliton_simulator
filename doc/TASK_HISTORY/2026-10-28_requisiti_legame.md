# 2026-10-28 — I REQUISITI DEL LEGAME, LA STABILITA' SULLA CARTA (2D E 3D), LA DIAGNOSI DI S4 *([[DECISIONE-LINEARE]], [[DECISIONE-L1-NATURA-A-SIMULATORE-B]], [[PIANO-2D-3D]]; il mandato di Luca delle `19:18`)*

> **LIVELLO:** un documento (`doc/REQUISITI_LEGAME.md`), conti sulla carta, una corsa di diagnosi in memoria. Nessun file del nucleo. Nessuna scelta fra `S1` e `S4`.

## 1. LE PREMESSE DAL CODICE

| che cosa | dove | il fatto |
|---|---|---|
| le forme | `_screening_forme_s3._ab` | `S1`: `alpha = x^2/(1+x^2)`; `S4`: `alpha = pi (x^p - 1)/(x^p + 1)`, `p = 2/pi`; `beta` accanto |
| il risolutore 2D | `_gravita_collettiva.profilo` | `H = |c| (-lap) + sg s alpha(u^2/Lambda0)`, `sg = segno di c`; il tempo immaginario a `N` fisso; `mu` riportato `= sg <H>`; pesi `2 pi r dr` |
| i dati 2D | `doc/referti_l2/solitoni_triangoli.jsonl` (`bcbd1f40`) | `tipo esistenza`, `griglia triangoli`, `lam0 6`: `N`, `mu`, `larghezza`, `x_centro` per forma, `s`, `N` |
| il cuore di `S1` in dinamica | `doc/referti_l2/congelato_lungo/` (`40061005`) | il picco per nodo; `rho_nodo = u^2 AREA_NODO` (`_energia_del_legame.stato`) |
| la curvatura in 3D | `doc/PROGETTO_FCC.md` | NON misurata: un parametro |
| `S4` piu' larga sui triangoli | `solitoni_triangoli.txt` | `3.106` archi a `s 0.3`, `N 1e7`; `2.840` a `s 0.99`, `N 1e7` |
| la dinamica | `_congelato_lungo.py` | il congelato vero; `VC.FORMA`, `VC.S`, `DC.N` sono globali dei moduli |

## 2. I CRITERI

- **(b)** `sigma_eff(x) = d ln(alpha(x) - alpha(0)) / d ln x` *(per `S4` `alpha(0) = -pi`; per `S1` `0`)*: la formula chiusa e le differenze finite sul codice.
- **(c), (d)** l'equazione adimensionale, dal risolutore: `lap v + (alpha(v^2) - alpha(0)) v = nu v`, `xi = r / l`, `l = sqrt(|c|/s)`, `v^2 = x`;
  `nu = mu/s - alpha(0)`, `n = N / (Lambda0 l^d)`. **`c` e `s` cambiano solo la scala:** il segno di `dn/dnu` dipende dalla forma e da `d`.
  `n(nu)` col tiro *(shooting)* in `d = 2, 3`, anche sul ramo che il tempo immaginario non trova.
- **la convenzione di VK, dal risolutore:** per `c < 0` lo stato legato e' il fondamentale di `H`; `omega = mu` riportato; **stabile se `dN/dmu > 0`**.
- **i controlli** *(DEVE)*: la gaussiana del logaritmo esatta in `d = 2, 3` *(`n = pi^{d/2} e^{nu - 1 + d}`)*, entro `1e-6`; Townes in 2D *(cubica, `n = 11.7009`)*;
  la potenza `x^sigma` con l'esponente `1/sigma - d/2` *(3D cubica: `-1/2`, DEVE risultare instabile; 3D `sigma 1/2`: `+1/2`, stabile)*;
  il tiro in 2D contro i punti del risolutore di `bcbd1f40` entro `1e-3` in `n`. **R6:** `dbeta/dx + x dalpha/dx = 0` per `S1` e `S4`.
- **parte 2:** `S4`, `N 1e7`; `s 0.3` a `L 81` e `L 120`, `3000` di tempo fisico; `s 0.99` a `L 81`, `3000` di tempo fisico. **DEVE:** lo script con `S1`, `s 0.3`, `N 1e6`, `L 81` ridà i punti di `40061005` al bit sui primi `200` tick; i pezzi al bit; `M`.

## 3. LE LETTURE *(senza soglie)*

- (b): il cuore misurato vive dove `sigma_eff` e' sotto o sopra `2/d`.
- (c), (d): `dn/dnu > 0` stabile, `< 0` instabile, ramo per ramo; esiste o no un `n` minimo.
- parte 2: il cuore di `S4` si stabilizza o si svuota; la larghezza in archi cambia o no fra `s 0.3` e `s 0.99`. `S4` resta con R2 e R3 contrari.

## 4. LE MOTIVAZIONI

- La riduzione adimensionale rende il risultato indipendente dalla curvatura 3D non misurata.

## 5. TODO

1. questo file, da solo;
2. `csv/_requisiti_legame.py`, commit; referto; `doc/REQUISITI_LEGAME.md`; RELAZIONE; MAPPA; commit;
3. `csv/_diagnosi_s4.py`, commit; le corse a pezzi; referto; il documento; RELAZIONE; MAPPA; commit.
