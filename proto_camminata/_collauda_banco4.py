r"""IL BANCO DEL `v4` — **la famiglia frazionaria, e i bracci che DEVONO scattare.**

> ## ⛔ **QUESTO BANCO PROVA UNA COSA SOLA, per ora: la FRAZIONE DI UN'INVOLUZIONE.**
> ## ### **Un interruttore alla volta** *(par. `3`)*: `vuoto4`, `cslocale` e `camminata4`
> ## arrivano dopo, ognuno col suo commit.

| | il braccio | che cosa prova |
|---|---|---|
| `W1` | a `cs = 1` la frazione e' il pezzo del `v3` | ### **AL BIT**, e non a `1e-16` |
| `W1-bis` | a `cs = 0` la frazione e' l'identita' | ### **AL BIT** |
| `W4` | l'inversa e' `cs -> -cs` | `<= n_est * eps` |
| `W9` | la norma si conserva a ogni `cs` | `<= n_est * eps` |
| — | la forma e' **unitaria** a `cs` qualunque | sulla matrice, nei due versi |
| ### ⛔ **DEVE** | la `C` **si rompe** alle frazioni | ### **se NON si rompesse, la derivazione del `2.3` sarebbe sbagliata** |
| ### ⛔ **DEVE** | il **tick intero** NON e' un'involuzione | ### **quindi <<la frazione del tick>> non esiste** *(`A4`)* |
| ### ⛔ **DEVE** | un `cs` che varia **dentro** un blocco rompe l'unitarieta' | ### **percio' l'assunzione di `frazione()` conta** |
| `A1` | le due candidate, a `forza = 0`, sono il `v3` | ### **AL BIT** |
| ### ⛔ **DEVE** | accese, **cambiano `Lambda`** | ### **una legge che non cambia niente non e' una legge** |
| — | il **TEOREMA**: `scatter` da solo non muove `Lambda` | ### **a blocchi per nodo**, quindi il meccanismo e' in **DUE tempi** |
| `A2` | `dispersione` da' `cs = 1.0` **AL BIT** sul fondo del `v3` | e ### ⛔ **`contrasto` NO**, e si dichiara |
| ### ⛔ **DEVE** | `densita` **NON** e' invariante di scala | ### **e' il braccio che separa il RELAZIONALE dallo SCALATO** |
| ### ⛔ **DEVE** | `contrasto` correla col **grado** piu' di `dispersione` | ### **l'artefatto degli estremi e' REALE** |
| `W5` `W6` | `cs` e la quota sono **pari sotto `C`** e **gauge-invarianti** | ### **AL BIT** |
| `W2` | nessun `clip`, nessuna costante tarata | sul **sorgente** |
| — | la lettura non importa il simulatore | sul **sorgente** |
| — | determinismo fra **DUE processi** | uscita identica |

Gira con:  python proto_camminata/_collauda_banco4.py
"""
import math
import os
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio                                              # noqa: E402

_presidio.avvia(__file__)

import camminata as CM                                         # noqa: E402
import camminata2 as C2                                        # noqa: E402
import camminata3 as C3                                        # noqa: E402
import camminata4 as C4                                        # noqa: E402
import cslocale4 as CS4                                       # noqa: E402
import frazione4 as F4                                         # noqa: E402
import geometria as GE                                         # noqa: E402
import scena as SC                                             # noqa: E402
import vuoto3 as V3                                            # noqa: E402
import vuoto4 as V4                                            # noqa: E402

EPS = float(np.finfo(float).eps)
NL = chr(10)
SEME = 11
CLIP = ("np.clip", ".clip(", "np.maximum", "np.minimum", "np.fmax", "np.fmin")
# ### ⚠ **`np.minimum` STA in `frazione4.py`, ed e- DICHIARATO:** e- la forma `min` del
# ### `cs` dell-arco, cioe- ### **una SCELTA DI LEGGE dichiarata e accendibile**, non un
# ### clip su un valore fuori intervallo. ### **Il braccio cerca gli ALTRI.**
# ### ⚠ **`np.minimum.at` e `np.maximum.at` STANNO in `cslocale4.py`, e sono
# ### DICHIARATI:** sono il `min` e il `max` della forma `contrasto`, cioe-
# ### ### **la grandezza stessa di una candidata** -- e la candidata esiste
# ### ### **per mostrare che e- un artefatto degli estremi.** ### **Non sono clip.**
CLIP_AMMESSI = {"frazione4.py": ("np.minimum",),
                "cslocale4.py": ("np.minimum", "np.maximum"),
                "vuoto4.py": (),
                "camminata4.py": ()}


def main():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL BANCO DEL v4 -- la frazione di un-involuzione, e i bracci che DEVONO scattare")
    print("=" * 100)
    SC._niente_simulatore()

    sc = SC.irregolare()
    geo = GE.scena_curva(sc, SEME)
    n_est = 2 * sc["m"]
    tol = n_est * EPS
    rng = np.random.default_rng(SEME)
    psi = CM.stato_casuale(sc, SEME)
    phi = rng.normal(size=n_est) + 1j * rng.normal(size=n_est)
    nodo = sc["nodo"]
    arco = np.arange(n_est) // 2
    PEZZI = (("Grover dello spinore", lambda v: CM.moneta_grover(v, sc), psi, nodo),
             ("spostamento con trasporto", lambda v: C2.spostamento_trasporto(v, geo, sc),
              psi, arco),
             ("Grover del vuoto", lambda v: V3.grover_scalare(v, sc), phi, nodo),
             ("spostamento del vuoto", lambda v: V3.spostamento_scalare(v), phi, arco))
    uno = np.ones(n_est)

    # ================================================================ la MATERIA
    # ### ⛔ **PRIMA DI TUTTO: i quattro pezzi SONO involuzioni ermitiane?** Se non lo
    # ### fossero, ### **tutto il resto di questo banco non proverebbe niente** -- e- la
    # ### materia del braccio, non un preambolo.
    inv = []
    her = []
    for _nome, X, v, _bl in PEZZI:
        inv.append(float(np.max(np.abs(X(X(v)) - v))))
        # ### l-ermitianita- si prova sul prodotto scalare: `<a, X b> = <X a, b>`
        a = v
        b = np.roll(v, 7, axis=0)
        her.append(abs(complex(np.vdot(a, X(b))) - complex(np.vdot(X(a), b))))
    esito("### MATERIA: i quattro pezzi sono INVOLUZIONI ERMITIANE",
          max(inv) <= tol and max(her) <= tol,
          "### max|X(X(v)) - v| = %.3g, max|<a,Xb> - <Xa,b>| = %.3g, soglia %.3g"
          % (max(inv), max(her), tol))

    # ================================================================ W1
    a1 = []
    a0 = []
    for _nome, X, v, _bl in PEZZI:
        for fa in F4.FAMIGLIE:
            a1.append(float(np.max(np.abs(F4.frazione(X, v, uno, fa) - X(v)))))
            a0.append(float(np.max(np.abs(F4.frazione(X, v, 0.0 * uno, fa) - v))))
    esito("### (W1) a `cs = 1` la frazione e- il pezzo del `v3`, AL BIT",
          max(a1) == 0.0,
          "### %d casi (4 pezzi x 2 famiglie), max scarto = %.3g" % (len(a1), max(a1)))
    esito("### (W1-bis) a `cs = 0` la frazione e- l-IDENTITA-, AL BIT",
          max(a0) == 0.0, "### %d casi, max scarto = %.3g" % (len(a0), max(a0)))

    # ================================================================ W4 e W9
    # ### ⛔ **E LE DUE SOGLIE SCALANO CON LA TAGLIA DEL VETTORE, perche- l-errore
    # ### di macchina e- RELATIVO:** `phi` qui ha norma `~832` *(NON normalizzato, e lo
    # ### e- di proposito: un vettore di norma `1` non eserciterebbe la scala)*, e
    # ### pretendere `n_est * eps` su una grandezza di taglia `832` vorrebbe dire
    # ### ### **pretendere `7` cifre in piu' di quante il `float64` ne abbia.**
    # ### ⚠ **E questa NON e- una soglia allargata per far passare un braccio:** e-
    # ### la soglia ### **dimensionalmente giusta** -- `n_est * eps * taglia` -- e al
    # ### primo giro l-avevo scritta ### **senza la taglia**, e il braccio e- diventato
    # ### rosso a `1.14e-13` contro `9.24e-14`. ### **Il rosso era mio, non del codice.**
    peggio_inv = (0.0, "", "", 0.0)
    peggio_nor = (0.0, "", "", 0.0)
    for nome, X, v, _bl in PEZZI:
        n0 = float(np.sum(np.abs(v) ** 2))
        amp = math.sqrt(n0)
        for fa in F4.FAMIGLIE:
            for c in (0.13, 0.37, 0.5, 0.86):
                cc = c * uno
                w = F4.frazione(X, v, cc, fa)
                dn = abs(float(np.sum(np.abs(w) ** 2)) - n0) / max(n0, 1.0)
                di = float(np.max(np.abs(F4.frazione_inversa(X, w, cc, fa) - v)))                     / max(amp, 1.0)
                if dn > peggio_nor[0]:
                    peggio_nor = (dn, nome, fa, c)
                if di > peggio_inv[0]:
                    peggio_inv = (di, nome, fa, c)
    esito("### (W4) l-inversa e- `cs -> -cs`, ed e- ESATTA",
          peggio_inv[0] <= tol,
          "### max scarto RELATIVO = %.3g su 32 casi (peggiore: %s, fam %s, cs %.2f), "
          "soglia %.3g" % (peggio_inv[0], peggio_inv[1], peggio_inv[2], peggio_inv[3],
                           tol))
    esito("### (W9) la norma si conserva a ogni `cs`",
          peggio_nor[0] <= tol,
          "### max|dnorma|/norma = %.3g (peggiore: %s, fam %s, cs %.2f), soglia %.3g"
          % (peggio_nor[0], peggio_nor[1], peggio_nor[2], peggio_nor[3], tol))

    # ================================================================ l-unitarieta-
    # ### ⭐ **SULLA MATRICE, e non sul prodotto scalare:** la norma conservata su UN
    # ### vettore ### **non basta** -- una matrice non unitaria puo' conservare la norma
    # ### di un vettore particolare. ### **Qui si costruisce `M^dag M`.**
    def matrice(X, cs, fa, dim, forma):
        M = np.zeros((dim, dim), dtype=complex)
        for j in range(dim):
            b = np.zeros(dim, dtype=complex)
            b[j] = 1.0
            M[:, j] = np.asarray(F4.frazione(X, b.reshape(forma), cs, fa)).reshape(-1)
        return M

    Xg = lambda v: V3.grover_scalare(v, sc)                   # noqa: E731
    peggio_u = 0.0
    for fa in F4.FAMIGLIE:
        for c in (0.21, 0.5, 0.79):
            M = matrice(Xg, c * uno, fa, n_est, (-1,))
            peggio_u = max(peggio_u,
                           float(np.max(np.abs(M.conj().T @ M - np.eye(n_est)))),
                           float(np.max(np.abs(M @ M.conj().T - np.eye(n_est)))))
    esito("### la forma e- UNITARIA, provata su `M^dag M` e `M M^dag`",
          peggio_u <= tol,
          "### max scarto = %.3g su 6 casi, soglia %.3g" % (peggio_u, tol))

    # ================================================================ DEVE: la C si rompe
    # ### ⛔ **SE LA `C` *NON* SI ROMPESSE, LA DERIVAZIONE DEL `2.3` SAREBBE SBAGLIATA.**
    # ### `C` e- ### **antiunitaria**, quindi `C e^{i t} = e^{-i t} C`: una fase scalare
    # ### commuta con `C` ### **solo se `t` e- dispari sotto `C`**, e qui `t = pi cs` con
    # ### `cs` ### **pari sotto `C`**, perche- `W5` lo pretende.
    def scarto_C_spin(cs, fa):
        Xs = lambda v: CM.moneta_grover(v, sc)                # noqa: E731
        a = C2.coniuga2(F4.frazione(Xs, psi, cs, fa))
        b = F4.frazione(Xs, C2.coniuga2(psi), cs, fa)
        return float(np.max(np.abs(a - b)))

    r_uno = scarto_C_spin(uno, "B")
    r_fra = {fa: [scarto_C_spin(c * uno, fa) for c in (0.25, 0.5, 0.75)]
             for fa in F4.FAMIGLIE}
    esito("### a `cs = 1` la `C` COMMUTA col Grover dello spinore, al bit",
          r_uno == 0.0, "### |C X - X C| = %.3g (e- il `v3`)" % r_uno)
    esito("### DEVE SCATTARE: alle frazioni la `C` NON commuta",
          min(min(v) for v in r_fra.values()) > 1e-3,
          "### (A) %.3f / %.3f / %.3f   (B) %.3f / %.3f / %.3f  a `cs = 0.25/0.5/0.75`"
          % tuple(r_fra["A"] + r_fra["B"]))
    esito("### e `(B)` rompe MENO di `(A)`, e in modo SIMMETRICO in `cs`",
          r_fra["B"][0] < r_fra["A"][0] and r_fra["B"][2] < r_fra["A"][2]
          and abs(r_fra["B"][0] - r_fra["B"][2]) <= 1e-12,
          "### `(B)` a `0.25` e `0.75`: %.6f e %.6f (differenza %.3g)"
          % (r_fra["B"][0], r_fra["B"][2], abs(r_fra["B"][0] - r_fra["B"][2])))

    # ================================================================ DEVE: A4
    # ### ⛔ **IL TICK INTERO NON E- UN-INVOLUZIONE**, quindi ### **<<la frazione del tick
    # ### intero>> NON ESISTE** in questa famiglia: e- `A4`, e il mandato chiede di non
    # ### nasconderlo.
    def tick(v):
        return C2.spostamento_trasporto(CM.moneta_grover(v, sc), geo, sc)

    d_tick = float(np.max(np.abs(tick(tick(psi)) - psi)))
    esito("### DEVE SCATTARE: il TICK INTERO non e- un-involuzione",
          d_tick > 1e-3,
          "### max|T(T(psi)) - psi| = %.3g: ### **la frazione del tick NON ESISTE** (A4)"
          % d_tick)

    # ================================================================ DEVE: il blocco
    # ### ⛔ **`frazione()` ASSUME che `cs` sia costante dentro il blocco di `X`.**
    # ### Se l-assunzione non contasse, l-assunzione sarebbe ### **decorazione.**
    cs_storto = uno.copy()
    cs_storto[0] = 0.3                     # ### una sola estremita- di un nodo
    esito("### `blocco_costante` vede il `cs` storto dentro il nodo",
          F4.blocco_costante(cs_storto, nodo) > 0.0
          and F4.blocco_costante(0.4 * uno, nodo) == 0.0,
          "### variazione dentro il blocco: %.3f (storto) contro %.3g (uniforme)"
          % (F4.blocco_costante(cs_storto, nodo),
             F4.blocco_costante(0.4 * uno, nodo)))
    M = matrice(Xg, cs_storto, "B", n_est, (-1,))
    rotta = float(np.max(np.abs(M.conj().T @ M - np.eye(n_est))))
    esito("### DEVE SCATTARE: un `cs` storto dentro il blocco ROMPE l-unitarieta-",
          rotta > 1e-3,
          "### max|M^dag M - I| = %.3g: ### **percio- l-assunzione di `frazione()` conta**"
          % rotta)

    # ================================================================ il cs dell-arco
    csn = rng.random(sc["n"])
    fuori = []
    dentro = []
    for forma in ("min", "armonica", "media"):
        ca = F4.cs_da_arco(csn, sc, forma)
        dentro.append(F4.blocco_costante(ca, arco))
        fuori.append((float(ca.min()) < 0.0) or (float(ca.max()) > 1.0))
    esito("### il `cs` dell-ARCO e- costante dentro l-arco, e sta in `[0, 1]`",
          max(dentro) == 0.0 and not any(fuori),
          "### tre forme (`min`, `armonica`, `media`), variazione dentro l-arco %.3g"
          % max(dentro))
    # ### ⭐ **E LE TRE FORME DEVONO DARE NUMERI DIVERSI**, altrimenti la scelta che
    # ### lascio a Luca ### **non sarebbe una scelta.**
    tre = [F4.cs_da_arco(csn, sc, f) for f in ("min", "armonica", "media")]
    sep = min(float(np.max(np.abs(tre[i] - tre[j])))
              for i, j in ((0, 1), (0, 2), (1, 2)))
    esito("### e le TRE forme dell-arco danno numeri DIVERSI: la scelta e- una scelta",
          sep > 1e-3,
          "### la coppia piu- vicina differisce di %.3f: ### **e- una DECISIONE DI LUCA**"
          % sep)

    # ================================================================ `A1`: il vuoto
    import _letture3 as L3
    st, _z, _d = L3.grumo(sc, GE.scena_identita(sc), 0, 1, 8.0, seme=SEME)
    psiG = st["psi"]
    phiF = V3.vuoto_fondo(sc, V3.LAMBDA0, SEME)
    rif = V4.passo_vuoto(phiF, psiG, sc, None)
    l_rif = V3.lambda_nodo(rif, sc)
    n_phi = V3.norma_vuoto(phiF)
    spenti, accesi, norme = [], [], []
    for cand in V4.CANDIDATE:
        spenti.append(float(np.max(np.abs(
            V4.passo_vuoto(phiF, psiG, sc, cand, forza=0.0) - rif))))
        f1 = V4.passo_vuoto(phiF, psiG, sc, cand, forza=1.0)
        accesi.append(float(np.max(np.abs(V3.lambda_nodo(f1, sc) - l_rif))))
        norme.append(abs(V3.norma_vuoto(f1) - n_phi) / n_phi)
    esito("### (W1) le due candidate di `A1`, a `forza = 0`, sono il `v3` AL BIT",
          max(spenti) == 0.0,
          "### `scatter` %.3g, `trasmissione` %.3g" % tuple(spenti))
    # ### \u26d4 **E QUESTO BRACCIO DEVE SCATTARE: una legge che non cambia NIENTE non e-
    # ### una legge.** ### **Se `max|Lambda - Lambda_v3|` fosse `~0`, la materia NON
    # ### starebbe scrivendo sul vuoto**, e il punto `A1` sarebbe fallito.
    esito("### DEVE SCATTARE: accese, le candidate CAMBIANO `Lambda` rispetto al `v3`",
          min(accesi) > 1e-3,
          "### max|Lambda - Lambda_v3|: `scatter` **%.3f**, `trasmissione` **%.3f**"
          % tuple(accesi))
    esito("### (W9) la norma del vuoto si conserva con le candidate accese",
          max(norme) <= tol,
          "### max|dnorma|/norma = %.3g, soglia %.3g" % (max(norme), tol))
    # ### \u2b50 **IL TEOREMA, MISURATO:** `scatter` da solo NON puo- muovere `Lambda`,
    # ### perche- Grover e l-identita- sono ### **entrambe a blocchi per nodo** -- quindi
    # ### ogni loro interpolazione conserva `Lambda_k`. ### **Il meccanismo e- in DUE
    # ### tempi**, e per questo `scatter` si misura SUL TICK.
    solo = V4.scatter(phiF, psiG, sc)
    d_solo = float(np.max(np.abs(V3.lambda_nodo(solo, sc)
                                 - V3.lambda_nodo(phiF, sc))))
    esito("### IL TEOREMA: `scatter` DA SOLO non muove `Lambda` (a blocchi per nodo)",
          d_solo <= tol * max(float(np.max(V3.lambda_nodo(phiF, sc))), 1.0),
          "### max|dLambda| = %.3g: ### **il meccanismo e- in DUE tempi, e lo spostamento "
          "e- il secondo**" % d_solo)
    # ### \u26d4 **E LA QUOTA DEL VUOTO E- `1` DOVE NON C-E- MATERIA**, cioe- il `v3`:
    # ### se non lo fosse, la legge agirebbe ### **anche nel vuoto puro.**
    q = V4.quota_vuoto(psiG, phiF, sc)
    senza = CM.rho_nodo(psiG, sc) == 0.0
    esito("### la QUOTA del vuoto e- `1` ESATTO dove non c-e- materia",
          bool(np.any(senza)) and float(np.max(np.abs(q[senza] - 1.0))) == 0.0
          and float(np.min(q)) < 1.0,
          "### %d nodi senza materia, scarto da `1`: %.3g; e il minimo e- %.6f"
          % (int(np.sum(senza)), float(np.max(np.abs(q[senza] - 1.0))),
             float(np.min(q))))

    # ================================================================ `A2`: il `cs`
    # ### \u2b50 **LA RIDUZIONE A `cs = 1` SUL FONDO DEL `v3`, forma per forma** -- e solo
    # ### una delle tre ci arriva ### **AL BIT.**
    al_bit = {f: bool(np.all(CS4.cs_nodo(phiF, sc, f) == 1.0)) for f in CS4.FORME}
    esito("### (W1) la forma `dispersione` da- `cs = 1.0` AL BIT sul fondo del `v3`",
          al_bit["dispersione"],
          "### dispersione %s, contrasto %s, densita %s -- ### **e la differenza e- "
          "DICHIARATA, non taciuta**"
          % tuple("AL BIT" if al_bit[f] else "NO" for f in CS4.FORME))
    esito("### DEVE SCATTARE: `contrasto` NON ci arriva al bit",
          not al_bit["contrasto"],
          "### `cs` minimo = %.17g: ### **`7e-16` sotto `1`, e si propagherebbe nella "
          "frazione**" % float(np.min(CS4.cs_nodo(phiF, sc, "contrasto"))))

    # ### \u26d4 **IL BRACCIO CHE SEPARA IL RELAZIONALE DALLO SCALATO, e vale piu- di
    # ### tutti gli altri di `A2`:** si moltiplica `phi` per una costante. ### **Una
    # ### grandezza relazionale NON cambia; una che ha una SCALA cambia.**
    rngc = np.random.default_rng(SEME + 1)
    pnu = rngc.normal(size=n_est) + 1j * rngc.normal(size=n_est)
    scala = {}
    for f in CS4.FORME:
        a = CS4.cs_nodo(pnu, sc, f)
        b = CS4.cs_nodo(7.0 * pnu, sc, f)
        scala[f] = float(np.max(np.abs(a - b)))
    esito("### `dispersione` e `contrasto` sono INVARIANTI DI SCALA, `densita` NO",
          scala["dispersione"] <= tol and scala["contrasto"] <= tol
          and scala["densita"] > 1e-3,
          "### moltiplicando `phi` per `7`: dispersione %.3g, contrasto %.3g, "
          "### **densita %.3f** -- ### **la terza ha una SCALA, ed e- il suo difetto "
          "dichiarato**" % (scala["dispersione"], scala["contrasto"], scala["densita"]))

    # ### \u26a0 **E LA CORRELAZIONE COL GRADO SI MISURA, perche- e- il costo di ognuna.**
    gr = sc["grado"].astype(float)
    corr = {}
    for f in CS4.FORME:
        v = []
        for seme in (3, 17, 101):
            rr = np.random.default_rng(seme)
            pp = rr.normal(size=n_est) + 1j * rr.normal(size=n_est)
            v.append(float(np.corrcoef(CS4.cs_nodo(pp, sc, f), gr)[0, 1]))
        corr[f] = float(np.mean(v))
    esito("### DEVE: `contrasto` correla col GRADO piu- di `dispersione` (artefatto estremi)",
          abs(corr["contrasto"]) > abs(corr["dispersione"]) + 0.1,
          "### correlazione media su tre semi: dispersione **%+.3f**, contrasto "
          "**%+.3f**, densita **%+.3f**"
          % (corr["dispersione"], corr["contrasto"], corr["densita"]))

    # ### \u2705 **`W5` e `W6` SU `cs`: PARI sotto `C`, e invariante di GAUGE** -- e- cio-
    # ### che fa piegare il tempo allo stesso modo a materia e antimateria.
    gauge = GE.scena_gauge_puro(sc, SEME)
    psi_g = np.empty_like(psiG)
    for e in range(n_est):
        kk = int(sc["nodo"][e])
        psi_g[e] = np.exp(1j * gauge["fi"][kk]) * (gauge["g"][kk] @ psiG[e])
    cC, cG = [], []
    for f in CS4.FORME:
        cC.append(float(np.max(np.abs(CS4.cs_nodo(np.conj(pnu), sc, f)
                                      - CS4.cs_nodo(pnu, sc, f)))))
        qa = V4.quota_vuoto(psiG, phiF, sc)
        qb = V4.quota_vuoto(C2.coniuga2(psiG), np.conj(phiF), sc)
        qc = V4.quota_vuoto(psi_g, phiF, sc)
        cG.append(max(float(np.max(np.abs(qa - qb))), float(np.max(np.abs(qa - qc)))))
    # ### ⛔ **E I DUE CASI SI SEPARANO, perche- NON hanno la stessa soglia:**
    # ### `cs` legge `|phi|^2` ### **elemento per elemento**, e la coniugazione non lo
    # ### tocca ⟹ ### **`0` AL BIT.** ### ⚠ **La QUOTA legge anche `rho`**, che e-
    # ### una ### **SOMMA sulle estremita-**, e `C` ne cambia ### **l-ORDINE** ⟹ lo
    # ### scarto e- l-errore di somma, ### **`0.19 eps` misurato.**
    # ### ⭐ **Al primo giro pretendevo `0` anche la-, e il braccio era rosso per una
    # ### soglia MIA**: con tre addendi l-ordine conta, e questo e- un fatto del
    # ### `float64`, non una rottura di `C`.
    esito("### (W5) `cs` e- PARI sotto `C`, AL BIT",
          max(cC) == 0.0,
          "### max scarto sulle tre forme = %.3g: `|phi|^2` non cambia sotto "
          "coniugazione" % max(cC))
    esito("### (W5, W6) la QUOTA e- pari sotto `C` e invariante di GAUGE",
          max(cG) <= tol,
          "### max scarto = %.3g (= %.2f eps), soglia %.3g: ### **lo scarto e- l-ORDINE "
          "DELLA SOMMA di `rho`, non una rottura**" % (max(cG), max(cG) / EPS, tol))

    # ================================================================ il PASSO del v4
    import saturazione3 as S3
    K = 12
    st3 = C3.stato3(sc, SEME)
    uno_n = np.ones(sc["n"], dtype=float)
    reg = []
    for fl in (None, S3.flusso):
        a, b = dict(st3), dict(st3)
        for _ in range(K):
            a = C3.passo3(a, sc, geo, uno_n, 1.0, 0.5, fl)
            b = C4.passo4_F(b, sc, geo, 1.0, 0.5, None, fl)
        reg.append(max(float(np.max(np.abs(b["psi"] - a["psi"]))),
                       float(np.max(np.abs(b["phi"] - a["phi"])))))
    esito("### (W1) `(F)` con `cs = 1` imposto e tutto spento E- IL `v3`, AL BIT",
          max(reg) == 0.0,
          "### senza `N` %.3g, con `N` %.3g, su %d tick: ### **e- la REGRESSIONE, il primo "
          "braccio del mandato**" % (reg[0], reg[1], K))
    # ### \u2b50 **E `(S)` CON `cs = 1` SCATTA OVUNQUE A OGNI TICK, quindi DEVE essere il
    # ### `v3` AL BIT TOO:** `tau += 1` supera `1`, ### **tutti i nodi scattano e tutti
    # ### gli archi scattano** -- cioe- il tick intero del `v3`. ### **Se non lo fosse,
    # ### la regola degli archi sarebbe sbagliata.**
    a, s = dict(st3), C4.stato_S(st3, sc)
    for _ in range(K):
        a = C3.passo3(a, sc, geo, uno_n, 1.0, 0.5, None)
        s = C4.passo4_S(s, sc, geo, 1.0, 0.5, None)
    d_S = max(float(np.max(np.abs(s["psi"] - a["psi"]))),
              float(np.max(np.abs(s["phi"] - a["phi"]))))
    esito("### (W1) `(S)` con `cs = 1` e- il `v3` AL BIT: scattano TUTTI, e tutti gli archi",
          d_S == 0.0,
          "### max scarto = %.3g, nodi scattati nell-ultimo tick %d su %d"
          % (d_S, int(np.sum(s["scattato"])), sc["n"]))

    # ### un `cs` imposto NON uniforme: e- il controllo di `L0`
    cs_nu = 0.3 + 0.7 * np.random.default_rng(5).random(sc["n"])
    nF, nS, iF, iS = [], [], 0.0, 0.0
    cF = dict(st3)
    for _ in range(K):
        cF = C4.passo4_F(cF, sc, geo, 1.0, 0.5, cs_nu)
    nF = [abs(CM.norma(cF["psi"]) - CM.norma(st3["psi"])) / CM.norma(st3["psi"]),
          abs(V3.norma_vuoto(cF["phi"]) - V3.norma_vuoto(st3["phi"]))
          / V3.norma_vuoto(st3["phi"])]
    dF = dict(cF)
    for _ in range(K):
        dF = C4.passo4_F(dF, sc, geo, 1.0, 0.5, cs_nu, inverso=True)
    iF = max(float(np.max(np.abs(dF["psi"] - st3["psi"]))),
             float(np.max(np.abs(dF["phi"] - st3["phi"])))) \
        / max(math.sqrt(V3.norma_vuoto(st3["phi"])), 1.0)
    sS = C4.stato_S(st3, sc)
    storia = []
    for _ in range(K):
        sS = C4.passo4_S(sS, sc, geo, 1.0, 0.5, cs_nu)
        storia.append(sS["scattato"].copy())
    nS = [abs(CM.norma(sS["psi"]) - CM.norma(st3["psi"])) / CM.norma(st3["psi"]),
          abs(V3.norma_vuoto(sS["phi"]) - V3.norma_vuoto(st3["phi"]))
          / V3.norma_vuoto(st3["phi"])]
    # ### \u26d4 **L-INVERSO DI `(S)` LEGGE IL BIT, e per questo il bit sta nello STATO.**
    dS = dict(sS)
    for t in range(K - 1, -1, -1):
        dS["scattato"] = storia[t]
        dS = C4.passo4_S(dS, sc, geo, 1.0, 0.5, cs_nu, inverso=True)
    iS = max(float(np.max(np.abs(dS["psi"] - st3["psi"]))),
             float(np.max(np.abs(dS["phi"] - st3["phi"])))) \
        / max(math.sqrt(V3.norma_vuoto(st3["phi"])), 1.0)
    esito("### (W9) le norme di `psi` e di `phi` si conservano, separatamente, in `(F)` e `(S)`",
          max(nF + nS) <= tol,
          "### `(F)` %.3g e %.3g, `(S)` %.3g e %.3g (relative), soglia %.3g"
          % (nF[0], nF[1], nS[0], nS[1], tol))
    esito("### (W4) l-INVERSO e- esatto, per `(F)` e per `(S)`",
          max(iF, iS) <= tol,
          "### `(F)` %.3g, `(S)` %.3g su %d+%d tick (relativi), soglia %.3g"
          % (iF, iS, K, K, tol))

    # ### \u26d4 **`W7`: IL CONO.** Si parte da UNA estremita- e si guarda ### **il raggio
    # ### del supporto**: dopo `t` tick non deve superare `t` archi. ### **E in `(S)` puo-
    # ### essere MINORE**, che e- il <<moto a scatti>>.
    d0 = SC.distanze(sc, 0)
    raggi = {}
    for et in ("F", "S"):
        p0 = np.zeros((n_est, 2), dtype=complex)
        p0[int(np.argmax(sc["nodo"] == 0)), 0] = 1.0
        z = {"psi": p0, "phi": np.zeros(n_est, dtype=complex)}
        if et == "S":
            z = C4.stato_S(z, sc)
        peggio = []
        for t in range(1, 7):
            z = (C4.passo4_F(z, sc, geo, 1.0, 0.5, cs_nu) if et == "F"
                 else C4.passo4_S(z, sc, geo, 1.0, 0.5, cs_nu))
            vivi = np.abs(z["psi"]).sum(axis=1) > 1e-14
            peggio.append(int(np.max(d0[sc["nodo"][vivi]])) if np.any(vivi) else 0)
        raggi[et] = peggio
    esito("### (W7) IL CONO: dopo `t` tick il supporto sta entro `t` archi, in `(F)` e `(S)`",
          all(r <= t + 1 for et in raggi for t, r in enumerate(raggi[et])),
          "### `(F)` raggi %s, `(S)` raggi %s, su `t = 1..6`"
          % (raggi["F"], raggi["S"]))

    # ### \u2b50 **`W5` SUL PASSO: ed e- QUI che `(F)` e `(S)` si separano.**
    def C_passo(et, cs):
        z = {"psi": psiG, "phi": phiF}
        if et == "S":
            z = C4.stato_S(z, sc)
            a1 = C3.coniuga3(C4.passo4_S(z, sc, geo, 1.0, 0.5, cs))
            z2 = C4.stato_S(C3.coniuga3(z), sc)
            a2 = C4.passo4_S(z2, sc, geo, 1.0, 0.5, cs)
        else:
            a1 = C3.coniuga3(C4.passo4_F(z, sc, geo, 1.0, 0.5, cs))
            a2 = C4.passo4_F(C3.coniuga3(z), sc, geo, 1.0, 0.5, cs)
        return max(float(np.max(np.abs(a1["psi"] - a2["psi"]))),
                   float(np.max(np.abs(a1["phi"] - a2["phi"]))))

    geo_i = GE.scena_identita(sc)
    geo_sal = geo
    geo = geo_i
    cF1, cS1 = C_passo("F", None), C_passo("S", None)
    cFn, cSn = C_passo("F", cs_nu), C_passo("S", cs_nu)
    geo = geo_sal
    esito("### (W5) a `cs = 1` la `C` tiene su ENTRAMBE le candidate",
          max(cF1, cS1) <= tol,
          "### `(F)` %.3g, `(S)` %.3g: ### **e- il `v3`**" % (cF1, cS1))
    esito("### DEVE SCATTARE: con `cs` non uniforme `(F)` ROMPE la `C` e `(S)` NO",
          cFn > 1e-3 and cSn <= tol,
          "### `(F)` **%.4f** contro `(S)` **%.3g**: ### **e- il PREZZO di `(F)`, e il "
          "GUADAGNO di `(S)`**" % (cFn, cSn))

    # ### \u26d4 **`W8` SUL SORGENTE, PEZZO PER PEZZO** -- il mandato lo chiede alla
    # ### lettera: *<<un collaudo lo verifica sul sorgente, pezzo per pezzo>>*.
    src = open(os.path.join(_QUI, "camminata4.py"), encoding="utf-8").read()
    corpo = src.split("def _lineare4(")[1].split("def _lineare4_inverso(")[0]
    pezzi_w8 = (("moneta_spin", "cs_k * dt"), ("moneta_grover", "cs_e"),
                ("spostamento_trasporto", "cs_a"), ("grover_scalare", "cs_e"),
                ("spostamento_scalare", "cs_a"))
    mancanti = []
    for nome, atteso in pezzi_w8:
        righe = [r for r in corpo.split(NL) if nome in r]
        if not righe or not all(atteso in r for r in righe):
            mancanti.append("%s (atteso `%s`)" % (nome, atteso))
    # ### \u26a0 **E NESSUN PEZZO PRENDE UN TICK FISSO:** si cerca `dt` NUDO e `1.0`.
    nudo = [r.strip() for r in corpo.split(NL)
            if ("moneta_grover" in r or "spostamento_trasporto" in r
                or "grover_scalare" in r or "spostamento_scalare" in r)
            and ("cs_e" not in r and "cs_a" not in r)]
    esito("### (W8) UNA SOLA grandezza, verificata SUL SORGENTE pezzo per pezzo",
          not mancanti and not nudo,
          "### %d pezzi guardati, %d senza la loro frazione, %d con un tick FISSO"
          % (len(pezzi_w8), len(mancanti), len(nudo)))

    # ### ⛔ **E SENZA UN GEMELLO CHE FALLISCE, IL BRACCIO DI SOPRA SAREBBE UN
    # ### FALSO-UNO:** si rifa' lo STESSO controllo su un sorgente FINTO in cui un pezzo
    # ### prende ### **un tick fisso** -- e ### **deve trovarlo.**
    def guarda(testo):
        man, nud = [], []
        for nome, atteso in pezzi_w8:
            rr = [r for r in testo.split(NL) if nome in r]
            if not rr or not all(atteso in r for r in rr):
                man.append(nome)
        nud = [r for r in testo.split(NL)
               if ("moneta_grover" in r or "spostamento_trasporto" in r
                   or "grover_scalare" in r or "spostamento_scalare" in r)
               and ("cs_e" not in r and "cs_a" not in r)]
        return man, nud

    finto = corpo.replace("x, cs_e, famiglia", "x, 1.0, famiglia")
    f_man, f_nud = guarda(finto)
    esito("### DEVE SCATTARE: lo stesso controllo su un sorgente FINTO col tick fisso",
          bool(f_man) or bool(f_nud),
          "### sul finto: %d pezzi senza la frazione, %d con un tick fisso "
          "(%s): ### **il controllo VEDE**"
          % (len(f_man), len(f_nud), ", ".join(f_man) or "nessuno"))

    # ================================================================ il sorgente
    for f in ("frazione4.py", "cslocale4.py", "vuoto4.py", "camminata4.py"):
        testo = open(os.path.join(_QUI, f), encoding="utf-8").read()
        trovati = [c for c in CLIP if c in testo and c not in CLIP_AMMESSI.get(f, ())]
        esito("### (W2) nessun `clip` non dichiarato in `%s`" % f,
              not trovati,
              "### %d forme cercate, %d ammesse e DICHIARATE (`%s`)"
              % (len(CLIP), len(CLIP_AMMESSI.get(f, ())),
                 ", ".join(CLIP_AMMESSI.get(f, ())) or "nessuna"))
        esito("### `%s` non IMPORTA il simulatore" % f,
              "import soliton_simulator" not in testo
              and "from soliton_simulator" not in testo, "### cercate le due forme")

    # ================================================================ il determinismo
    for f in ("frazione4.py", "cslocale4.py", "vuoto4.py", "camminata4.py"):
        imp = []
        for _ in range(2):
            pr = subprocess.run([sys.executable, os.path.join(_QUI, f)],
                                cwd=RADICE, capture_output=True, text=True,
                                encoding="utf-8", errors="replace")
            imp.append((pr.stdout or "").strip())
        esito("### il DETERMINISMO di `%s` fra DUE PROCESSI" % f,
              len(imp) == 2 and imp[0] == imp[1] and bool(imp[0]),
              "### %d caratteri confrontati" % len(imp[0] if imp else ""))

    print("=" * 100)
    print("IL BANCO DEL v4: %d su %d   ### %s"
          % (ok[0], ok[1], "TUTTI PASSATI" if ok[0] == ok[1] else "CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(main())
