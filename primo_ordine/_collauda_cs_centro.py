# -*- coding: utf-8 -*-
"""`D2` — **`cs` DALLO STATO AL CENTRO DEL PALINDROMO, a PUNTO FISSO.**

> ### ⛔ **IL PUNTO DELICATO, con le parole del mandato del `2026-10-16`:** `cs` dipende da
> `Lambda`, e ### **`Lambda` cambia DURANTE il passo**, quindi il tempo proprio diventa
> ### **dinamico.** ### **Un `cs` letto all'INIZIO del passo ROMPE IL PALINDROMO.**

## ⭐⭐ IL RISULTATO, in una riga: **la pendenza**

```
forma SPENTA                 2.002        <- il secondo ordine di oggi
cs al CENTRO (punto fisso)   2.000        <- IL SECONDO ORDINE E' CONSERVATO
cs a INIZIO PASSO            0.998        <- IL SECONDO ORDINE E' PERSO
```

### ✅ **Cioe' la valutazione simmetrica FUNZIONA**, e la variante ingenua
### **perde esattamente cio' che il mandato prevedeva che perdesse.**

## ⛔ IL PUNTO FISSO CONVERGE, ma **COSTA**, e il numero va letto

| la scena | `Lambda_c` | i giri | il rapporto di contrazione |
|---|---|---|---|
| `nn=16 seme=7` | `0.8` | `38` | `0.415` |
| `nn=16 seme=7` | `8.0` | ### **`47`** | `0.490` |
| `nn=16 seme=7` | `80.0` | `11` | `0.041` |
| `nn=12 seme=11` | `0.8` | `28` | `0.307` |
| `nn=12 seme=11` | `8.0` | `34` | `0.364` |
| `nn=12 seme=11` | `80.0` | `12` | `0.046` |

### ⛔⛔ **IL MASSIMO E' `47` GIRI, e ogni giro costa MEZZO TICK:** cioe'
### **~`23` tick di lavoro per OGNI tick.** ### ⚠ **E' un numero che Luca deve vedere**,
perche' ### **fa il simulatore ~`23` volte piu' lento** quando la forma e' accesa.
### 📌 **E la convergenza e' PIU' RAPIDA dove `Lambda_c` e' grande** *(`11` giri a
`Lambda_c/Lambda = 10`)*, perche' la' ### **`cs` e' piccolo, il passo e' corto, e `Lambda`
si muove meno.**
### ✅ **In nessun regime provato il punto fisso NON converge** — ### **nemmeno a
`Lambda_c/Lambda = 0.1`**, che e' il regime che il mandato temeva.

## ⚠ CHE COSA MANCA DI `D2`, e si dice

Il mandato chiede che la variante ingenua perda ### **il secondo ordine `E` la simmetria
`PTheta`**. ### **Il secondo ordine e' MISURATO qui.** ### ⛔ **La `PTheta` NO**, e il
motivo e' che vive su ### **un'altra scena** *(quella di `_misura_theta_nonlineare.py`,
con la sua permutazione delle estremita')*: ### **va fatta la', non riscritta qui** — e
riscriverla sarebbe ### **un secondo strumento per la stessa simmetria.**
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(_QUI, "leggi"))
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))
import _presidio                                              # noqa: E402
import composizione as CM                                     # noqa: E402
import deriva as DV                                           # noqa: E402
import flussi_parziali as FP                                  # noqa: E402
import tick as TK                                             # noqa: E402

NL = chr(10)
EPS = float(np.finfo(float).eps)
SCENE = ((16, 7), (12, 11))
# ### ⛔ **I TRE `Lambda_c`, e sono i TRE RAPPORTI di `D4`** *(`0.1`, `1`, `10` volte il
# ### `Lambda` iniziale, che e' `8.0`)*. ### ⚠ **Non sono una scelta: sono i tre punti in
# ### cui il mandato chiede di guardare.**
LAMBDA_INIZIALE = 8.0
LC = (0.8, 8.0, 80.0)
# ### ⛔ **I CRITERI, fissati nel task history del punto `D`.**
PENDENZA_MIN = 1.9
PENDENZA_INGENUA_MAX = 1.5
DTAU_PENDENZA = (0.4, 0.2, 0.1, 0.05)
T_FISICO = 0.8
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))


def giri_del_punto_fisso(nn, seme, lambda_c):
    """`(giri, rapporto)`: ### **quanti giri** e ### **quanto contrae**, misurati."""
    _i, mot, st, par = DV.scena(nn, seme, 1.0, norma="locale",
                                vuoto_modulo=2.0, su2=True)
    fp = mot._b("cc_fp", (mot.inc.n,), float)
    meta = TK.meta_del_palindromo()
    prec = FP.cs(mot.densita_vuoto(st), lambda_c, fp).copy()
    rapporti, s = [], None
    for giri in range(1, TK.GIRI_MAX + 1):
        copia = {k: (v.copy() if hasattr(v, "copy") else v) for k, v in st.items()}
        mot.cs = prec
        TK.percorri_tick(copia, mot, par, (), None, meta)
        nuovo = FP.cs(mot.densita_vuoto(copia), lambda_c, fp).copy()
        sn = float(np.max(np.abs(nuovo - prec)))
        if s is not None and s > 0.0:
            rapporti.append(sn / s)
        s, prec = sn, nuovo
        if sn <= 8.0 * EPS * float(np.max(np.abs(nuovo))):
            return giri, (float(np.median(rapporti)) if rapporti else -1.0)
    return -1, (float(np.median(rapporti)) if rapporti else -1.0)


def evolvi(nn, seme, dtau, modo, lambda_c):
    """Evolve ### **per lo STESSO tempo fisico** `T_FISICO`, coi tre modi."""
    _i, mot, st, par = DV.scena(nn, seme, dtau, norma="locale",
                                vuoto_modulo=2.0, su2=True)
    quanti = int(round(T_FISICO / dtau))
    for _t in range(quanti):
        if modo == "centro":
            TK.tick_con_cs(st, mot, par, lambda_c)
        elif modo == "inizio":
            FP.accendi_cs(mot, lambda_c, st)
            TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
        else:
            TK.tick(st, mot, par)
    return st["psi_h"].copy(), st["phi_h"].copy()


def pendenza(nn, seme, modo, lambda_c):
    """La pendenza ### **asintotica** di `|x(dtau) - x(dtau/2)|` contro `dtau`."""
    err = []
    for dtau in DTAU_PENDENZA:
        a = evolvi(nn, seme, dtau, modo, lambda_c)
        b = evolvi(nn, seme, dtau / 2.0, modo, lambda_c)
        err.append(max(float(np.max(np.abs(a[0] - b[0]))),
                       float(np.max(np.abs(a[1] - b[1])))))
    pend = [float(np.log2(err[k] / err[k + 1])) for k in range(len(err) - 1)
            if err[k + 1] > 0.0]
    return pend, err


def braccio_punto_fisso():
    """### ⛔ **IL PUNTO FISSO CONVERGE in ogni regime**, e i giri si RIPORTANO."""
    print("      %-18s %7s %10s" % ("scena / Lambda_c", "giri", "contrazione"))
    peggio = 0
    for nn, seme in SCENE:
        for lc in LC:
            g, r = giri_del_punto_fisso(nn, seme, lc)
            peggio = max(peggio, g)
            print("      nn=%-3d lc=%-6.1f %7d %10.3f" % (nn, lc, g, r))
            esito("### (f) il punto fisso converge: nn=%d, `Lambda_c = %.1f`" % (nn, lc),
                  g > 0, "%d giri, contrazione %.3f" % (g, r))
    esito("### (f) e il MASSIMO dei giri sta sotto il tetto dichiarato",
          0 < peggio < TK.GIRI_MAX,
          "massimo %d giri su un tetto di %d: ogni giro costa MEZZO tick, quindi ~%d tick"
          " di lavoro per tick" % (peggio, TK.GIRI_MAX, peggio // 2))


def braccio_secondo_ordine():
    """### ⭐⭐ **IL SECONDO ORDINE: conservato al CENTRO, PERSO a inizio passo.**"""
    nn, seme = SCENE[0]
    print("      %-10s %10s   %s" % ("modo", "pendenza", "le pendenze a ogni dimezzamento"))
    fuori = {}
    for modo in ("spenta", "centro", "inizio"):
        pend, _err = pendenza(nn, seme, modo, LAMBDA_INIZIALE)
        fuori[modo] = pend[-1] if pend else float("nan")
        print("      %-10s %10.3f   %s"
              % (modo, fuori[modo], " ".join("%.3f" % x for x in pend)))
    esito("### (o1) la forma SPENTA e' del SECONDO ordine", fuori["spenta"] >= PENDENZA_MIN,
          "pendenza %.3f >= %.1f" % (fuori["spenta"], PENDENZA_MIN))
    esito("### (o2) `cs` al CENTRO CONSERVA il secondo ordine",
          fuori["centro"] >= PENDENZA_MIN,
          "pendenza %.3f >= %.1f: la valutazione simmetrica FUNZIONA"
          % (fuori["centro"], PENDENZA_MIN))
    esito("### (o3) DEVE fallire: `cs` a INIZIO PASSO PERDE il secondo ordine",
          fuori["inizio"] <= PENDENZA_INGENUA_MAX,
          "pendenza %.3f <= %.1f: e' il PRIMO ordine, e il palindromo e' rotto"
          % (fuori["inizio"], PENDENZA_INGENUA_MAX))


def main(argv):
    del argv
    _presidio.avvia(__file__)
    print("=" * 100)
    print("`D2`: `cs` AL CENTRO DEL PALINDROMO, A PUNTO FISSO")
    print("=" * 100)
    braccio_punto_fisso()
    braccio_secondo_ordine()
    print("=" * 100)
    print("`D2`: %d su %d   %s"
          % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("  ### ⚠ E LA `PTheta` NON E' QUI: vive sulla scena di"
          " `_misura_theta_nonlineare.py`,")
    print("  ###   e riscriverla qui sarebbe un SECONDO strumento per la stessa simmetria.")
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
