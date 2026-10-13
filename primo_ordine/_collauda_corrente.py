# -*- coding: utf-8 -*-
"""IL COLLAUDO DELLA CORRENTE LOCALE — **esiste, chiude, e la PORTATA e' misurata.**

### ⛔ **QUESTO COLLAUDO CORREGGE UNA MIA CONCLUSIONE, e lo dice.** Il collaudo di
`primo_ordine/_collauda_energia.py` afferma — **e resta vero** — che la mia candidata *(«cio'
che lo spostamento porta»)* **non chiude il bilancio**. ### **Da quel fatto avevo inferito
che una corrente locale NON ESISTESSE: il salto non si fa.** ### ✅ **Esiste**, e qui si
**costruisce.**

### ⭐ **L'ORDINE DEI BRACCI E' QUELLO CHE SERVE A CREDERCI:**

| | il braccio | che cosa **esclude** |
|---|---|---|
| `1` | c'e' **MATERIA**: `Delta e` non e' zero, e il supporto di una coppia e' **piu' di un nodo** | ### **il FALSO-ZERO**: un bilancio che chiude perche' **non c'e' niente da bilanciare** |
| `2` | l'**identita'** `somma_k Q_k = 0` | ### che la chiusura venga **da altro** |
| `3` | la **forma** vale `Delta e` su un `x` **che non e' nella base** | ### di **verificare la forma con cio' con cui e' costruita** |
| `4` | la **continuita'** chiude **entro ulp** | — |
| `5` | ### ⛔ **DEVE FALLIRE:** un arco col **verso invertito** | ### che il bilancio **sia cieco al verso** |
| `6` | ### ⛔ **DEVE FALLIRE:** una carica **non instradata** | ### che chiuda **per caso** e non **per costruzione** |
| `7` | ### ⛔ **DEVE FALLIRE:** `Q` **perturbato** cosi' che la somma **non sia zero** | ### che la chiusura **non dipenda dall'identita'** -- ### **che e' tutto l'argomento** |
| `8` | la **portata** non cresce col grafo: **due taglie** della stessa famiglia | ### **<<portata = diametro>>**, che su UNA taglia da' lo stesso numero |

Gira con:  python primo_ordine/_collauda_corrente.py
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import _presidio                                              # noqa: E402
import corrente as CO                                         # noqa: E402

OK = [0, 0]
EPS = float(np.finfo(float).eps)
# ### ⚠ **LE SOGLIE, FISSATE QUI E NON NEL CORPO:** una soglia scritta dentro un braccio
# ### e- ### **una soglia che si puo- aggiustare dopo aver visto il numero.**
ULP_MAX = 1000.0
ROTTO_MIN = 1e-3
# ### ⭐ **LA PORTATA ATTESA, `3` ARCHI, E' UN NUMERO MISURATO E NON SCELTO:** viene
# ### dalla scala di `python primo_ordine/corrente.py` -- grado `4`, diametro `4`, `5` e
# ### `6` ### **danno tutti `3`.** ### ⚠ **E qui serve come SOGLIA DEL CONFRONTO**, cioe'
# ### per dire ### **quali taglie sono sopra la saturazione**: senza, il braccio
# ### confronterebbe un grafo tagliato con uno no.
PORTATA_ATTESA = 3


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))


def _banco(ii, jj, nn, seme=4):
    inc, mot, st, par = CO._scena(ii, jj, nn, seme)
    Q = CO.forma_quadratica(st, mot, par)
    x = CO.x_da_psi(st["psi_h"])
    de = CO._delta_e(st, mot, par, st["psi_h"], np.zeros(nn, dtype=float)).copy()
    return inc, mot, st, par, Q, x, de


def main(argv):
    _presidio.avvia(__file__)
    print("=" * 96)
    print("IL COLLAUDO DELLA CORRENTE LOCALE: LA COSTRUZIONE, E I TRE CASI CHE DEVONO FALLIRE")
    print("=" * 96)
    # ### (0) IL TERMINE DI BORDO: ### **l-argomento, prima della costruzione.**
    # ### ⛔ **Se questo cadesse, la costruzione non avrebbe su che cosa poggiare** -- e
    # ### allora il difetto starebbe ### **nel mio `e_h`**, non nell-argomento.
    iia, jja, nna = CO.anello(40)
    dentro = np.zeros(nna, dtype=bool)
    dentro[:20] = True
    dint, dbor, cambio, _s = CO.termine_di_bordo(iia, jja, nna, dentro)
    esito("### (0) perturbando DENTRO `R`, `somma_R Delta e` non cambia",
          dint < 1e-12 and cambio > 1.0,
          "|cambio| = %.3e, ma per nodo fino a %.3f" % (dint, cambio))
    esito("### (0-bis) DEVE CAMBIARE: perturbando AL BORDO di `R`",
          dbor > ROTTO_MIN, "|cambio| = %.3e" % dbor)

    ii, jj, nn = CO.toro((3, 3))
    inc, mot, st, par, Q, x, de = _banco(ii, jj, nn)
    J, portata, dia = CO.instrada(Q, inc, x)
    sc = float(np.max(np.abs(de)))

    # ### (1) LA MATERIA
    esito("### (1) c-e- MATERIA: `Delta e` non e- zero", sc > 1e-3,
          "max |Delta e| = %.3f" % sc)
    esito("### (1-bis) il SUPPORTO di una coppia e- piu- di un nodo",
          dia["supporto"] > 1, "supporto max %d nodi" % dia["supporto"])

    # ### (2) L-IDENTITA-
    ident = float(np.max(np.abs(np.sum(Q, axis=0))))
    esito("### (2) l-identita- `somma_k Q_k = 0`", ident < 1e-12,
          "%.3e" % ident)

    # ### (3) LA FORMA, su un `x` FUORI dalla base
    forma = float(np.max(np.abs(np.einsum("i,kij,j->k", x, Q, x) - de)))
    esito("### (3) la forma vale `Delta e` su un `x` fuori dalla base",
          forma < 1e-12, "%.3e" % forma)

    # ### (4) LA CONTINUITA-
    res = float(np.max(np.abs(CO.divergenza(J, inc) - de)))
    ulp = res / (EPS * max(sc, 1e-30))
    esito("### (4) la continuita- CHIUDE nodo per nodo", ulp < ULP_MAX,
          "residuo %.3e = %.1f ulp" % (res, ulp))

    # ### (5) DEVE FALLIRE: IL VERSO INVERTITO
    Jm = J.copy()
    a = int(np.argmax(np.abs(J)))
    Jm[a] = -Jm[a]
    rotto = float(np.max(np.abs(CO.divergenza(Jm, inc) - de)))
    esito("### (5) DEVE FALLIRE: un arco col verso INVERTITO rompe",
          rotto > ROTTO_MIN, "residuo %.3e (era %.3e)" % (rotto, res))

    # ### (6) DEVE FALLIRE: UNA CARICA NON INSTRADATA
    # ### ⛔ **Si toglie l-ULTIMO nodo vivo di UNA coppia**, cioe- ### **una carica che
    # ### non viene mandata da nessuna parte** -- e allora ### **la somma zero non si
    # ### usa piu-, e la continuita- DEVE rompersi.**
    Jp = np.zeros(inc.m, dtype=float)
    dist, prev, arco = CO._cammini(inc)
    saltata = 0
    D = Q.shape[1]
    for i in range(D):
        for j in range(D):
            peso = float(x[i]) * float(x[j])
            c = Q[:, i, j]
            vivi = np.flatnonzero(np.abs(c) > 1e-14)
            if vivi.size <= 1 or peso == 0.0:
                continue
            rif = int(vivi[0])
            # ### ⚠ **`[1:-1]` invece di `[1:]`: l-ultimo NON si instrada**
            for k in vivi[1:-1]:
                k = int(k)
                quanto = float(c[k]) * peso
                v = k
                while v != rif:
                    aa = int(arco[rif, v])
                    u = int(prev[rif, v])
                    Jp[aa] += quanto if int(inc.ii[aa]) == u else -quanto
                    v = u
            saltata += 1
    buco = float(np.max(np.abs(CO.divergenza(Jp, inc) - de)))
    esito("### (6) DEVE FALLIRE: una carica NON instradata rompe",
          buco > ROTTO_MIN and saltata > 0,
          "residuo %.3e su %d coppie" % (buco, saltata))

    # ### (7) DEVE FALLIRE: `Q` CHE NON SOMMA A ZERO
    # ### ⭐ **E QUESTO E- IL BRACCIO CHE PROVA L-ARGOMENTO:** se la chiusura non
    # ### dipendesse dall-identita-, ### **questo passerebbe comunque.**
    Qg = Q.copy()
    Qg[0, 0, 0] += 1.0
    Jg, _p, _d = CO.instrada(Qg, inc, x)
    deg = de.copy()
    deg += np.einsum("i,kij,j->k", x, Qg - Q, x)
    guasto = float(np.max(np.abs(CO.divergenza(Jg, inc) - deg)))
    esito("### (7) DEVE FALLIRE: `Q` che non somma a zero non chiude",
          guasto > ROTTO_MIN, "residuo %.3e" % guasto)

    # ### (8) LA PORTATA NON CRESCE COL GRAFO
    # ### ⛔ **E IL CONFRONTO NON PUO- PARTIRE DAL `3x3`:** il `3x3` ha diametro `2`, e
    # ### la- la portata vale `2` ### **perche- IL GRAFO LA TAGLIA.** Confrontarlo col
    # ### `4x4` darebbe ### **<<2 contro 3>>, cioe- <<cresce>>** -- e sarebbe
    # ### ### **una conclusione sbagliata presa da un taglio.**
    # ### ⭐ **Quindi le due taglie sono entrambe SOPRA la saturazione** *(diametro
    # ### `>= PORTATA_ATTESA`)*, e il braccio ### **lo pretende invece di sperarlo.**
    coppie = []
    for lati in ((4, 4), (4, 6)):
        ii2, jj2, nn2 = CO.toro(lati)
        inc2, mot2, st2, par2, Q2, x2, de2 = _banco(ii2, jj2, nn2)
        J2, portata2, dia2 = CO.instrada(Q2, inc2, x2)
        res2 = float(np.max(np.abs(CO.divergenza(J2, inc2) - de2)))
        coppie.append((lati, portata2, dia2["diametro"],
                       res2 / (EPS * max(float(np.max(np.abs(de2))), 1e-30))))
    sopra = all(d >= PORTATA_ATTESA for _l, _p, d, _u in coppie)
    diversi = coppie[0][2] != coppie[1][2]
    uguale = coppie[0][1] == coppie[1][1] == PORTATA_ATTESA
    esito("### (8) la PORTATA non cresce col grafo (due taglie SOPRA la saturazione)",
          sopra and diversi and uguale,
          "  ".join("%s: portata %d, diametro %d" % (l, p, d)
                    for l, p, d, _u in coppie))
    esito("### (8-bis) e il `3x3` mostra il TAGLIO, non una crescita",
          portata < PORTATA_ATTESA and dia["diametro"] < PORTATA_ATTESA,
          "portata %d su diametro %d" % (portata, dia["diametro"]))
    esito("### (8-ter) e la continuita- chiude su tutte e due le taglie",
          all(u < ULP_MAX for _l, _p, _d, u in coppie),
          "  ".join("%.1f ulp" % u for _l, _p, _d, u in coppie))

    print("=" * 96)
    print("  %d su %d" % (OK[0], OK[1]))
    print("=" * 96)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
