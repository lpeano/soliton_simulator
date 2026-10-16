# -*- coding: utf-8 -*-
r"""**LE QUATTRO FORME, MISURATE** — *con `rho` come sorgente. Il motore NON si tocca.*

> **Punto 2 del mandato di Luca del 2026-10-15** *(terzo pezzo di `L2`)*. La derivazione
> simbolica sta in `_deriva_forme_l2.py` *(`20`/`20`)*.

## ⛔ COME SI CAMBIA IL TERMINE SENZA TOCCARE IL MOTORE

### **Si sostituisce `mot.operatori["CAMM-SATURAZIONE"]` a runtime**, dentro questo script —
una funzione che: ### ① prende `rho_k = somma_h |psi_h|^2` *(la DENSITA', non l'elicita')*;
### ② mette su `psi` ### **una FASE `exp(-i alpha dtau)`** *(e non una rotazione attorno a
`n`: con `rho` come sorgente `dN/dpsi^* = alpha psi`)*; ### ③ mette su `phi` la fase
`exp(-i beta dtau)`, come il motore fa oggi.
### ✅ **E si rimette a posto in un `finally`:** l'oggetto e' condiviso, e lasciarlo
sostituito **falserebbe ogni misura successiva nella stessa corsa.**

## ⚠ LA SINGOLARITA' DI `alpha` DOVE `psi = 0`, e perche' NON e' un pavimento

### `S2`, `S3` e `S4` hanno `alpha` **divergente** per `rho -> 0`. ### ⛔ **Ma dove
`rho = 0` si ha `psi = 0`**, e ### **la fase di un vettore nullo non vuol dire niente:**
`exp(-i alpha dtau) · 0 = 0` per **qualunque** `alpha`.
### ✅ **Quindi li' si pone `alpha = 0`, e NON e' una cura dove non c'e' un errore**
*(`A11`)*: e' ### **il valore che l'espressione prende dove e' definita** — una
singolarita' **eliminabile**, non tagliata.
### 📌 **E dove `rho` e' PICCOLO ma non nullo `alpha` resta GRANDE e si usa com'e':** e'
esattamente il caso che il punto `(d)` va a misurare.

## 📌 LE CORSE SONO LUNGHE E STANNO FUORI DAL `pre-commit`

### **Misure DICHIARATE**, non collaudi. ### **E la corsa senza materia e' in cache per
`(dtau, tick)`**, perche' con `psi = 0` il termine non fa niente, qualunque forma sia.

Gira con:  python primo_ordine/_misura_forme_l2.py
"""
import os
import sys
import time

import numpy as np
import tick as TK

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

OK = [0, 0]
# ### ⛔ **LA CONFIGURAZIONE INTERA, DICHIARATA E STAMPATA**
TICK = 2000
FINESTRE = 10
TICK_SCAN = 1000
FINESTRE_SCAN = 10
DTAU = (0.5, 0.25)
DTAU_SPIN = (0.5,)
X_SCAN = (0.01, 0.03, 0.1, 0.2, 0.5, 1.0, 2.0)
VUOTO = 1.0
RAGGIO = 1
SEME = 7
FORME = ("S1", "S2", "S3", "S4")
# ### ⭐ **L-ESTENSIONE DICHIARATA: dove il verdetto resta INDECISO si ALLUNGA la corsa.**
# ### ⚠ **E non si abbassa la soglia:** le `3` barre sono di Luca, e ### **la barra scende
# ### come `1/sqrt(N)`** -- allungare e- l-unica cosa onesta da fare.
TICK_LUNGO = 10000
FINESTRE_LUNGO = 20
_SENZA = {}
P4 = 2.0 / np.pi


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-56s %s   %s" % (che[:56], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


# ====================================================================== le quattro forme
def _alpha_beta(nome, x):
    """### `(alpha, beta)` della forma `nome`, ### **dalle formule DERIVATE in `sympy`.**"""
    x = np.asarray(x, dtype=float)
    if nome == "S1":
        return x ** 2 / (1.0 + x ** 2), x / (1.0 + x ** 2) - np.arctan(x)
    if nome == "S2":
        with np.errstate(divide="ignore", invalid="ignore"):
            al = 1.0 + np.log(x)
        return al, -x
    if nome == "S3":
        with np.errstate(divide="ignore", invalid="ignore"):
            al = np.log(x / (1.0 + x)) + 1.0 / (1.0 + x)
        return al, -x / (1.0 + x)
    if nome == "S4":
        from scipy.special import hyp2f1
        xp = x ** P4
        al = np.pi * (xp - 1.0) / (xp + 1.0)
        F = np.pi * x - 2.0 * np.pi * x * hyp2f1(1.0, 1.0 / P4, 1.0 + 1.0 / P4, -xp)
        return al, F - x * al
    raise AssertionError("forma %r sconosciuta" % (nome,))


def densita_materia(mot, st):
    """### `rho_k = somma_h |psi_h|^2` — ### **la sorgente, per nodo.**"""
    rho = np.zeros(mot.inc.n, dtype=float)
    np.add.at(rho, mot.inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
    return rho


def _termine(nome):
    """### Il termine sostituito: ### **`rho` come sorgente, e una FASE su `psi`.**"""
    import flussi_parziali as FP

    def agisci(st, parametri, frazione):
        mot = agisci.mot
        rho = densita_materia(mot, st)
        lam = mot.densita_vuoto(st)
        with np.errstate(divide="ignore", invalid="ignore"):
            x = np.where(lam > 0, rho / np.where(lam > 0, lam, 1.0), 0.0)
        al, be = _alpha_beta(nome, x)
        # ### ⚠ **dove `rho = 0` la fase di `psi` NON VUOL DIRE NIENTE** *(`psi = 0`)*:
        # ### si pone `alpha = 0`. ### **Singolarita- ELIMINABILE, non tagliata.**
        al = np.where(rho > 0, al, 0.0)
        al = np.where(np.isfinite(al), al, 0.0)
        be = np.where(np.isfinite(be), be, 0.0)
        dtau = FP.dtau_nodo(mot)
        f = float(frazione)
        nodo = mot.inc.nodo
        fp = np.take(al * dtau * f, nodo)
        st["psi_h"] *= np.exp(-1j * fp).reshape(-1, 1)
        ff = np.take(be * dtau * f, nodo)
        st["phi_h"] *= np.exp(-1j * ff)
        mot.applicazioni["CAMM-SATURAZIONE"] += 1
        return st

    return agisci


def _corri(dtau, ampiezza, materia, elicita, forma, rovescia, tick, spento=False):
    """### `(Lambda(t), rho(t), per)` con la forma `forma` **sostituita a runtime.**"""
    import deriva as DV
    import scena_l2 as SC
    inc, mot, st, par, _c, per = SC.scena(dtau, VUOTO, ampiezza, RAGGIO, materia,
                                          True, False, SEME, elicita)
    vero = mot.operatori["CAMM-SATURAZIONE"]
    if spento:
        def nulla(st_, parametri, frazione):
            return st_
        mot.operatori["CAMM-SATURAZIONE"] = nulla
    else:
        ag = _termine(forma)
        ag.mot = mot
        if rovescia:
            base = ag

            def rov(st_, parametri, frazione):
                # ### il segno di `beta` rovesciato: si rifa- il conto con `-beta`
                m = base.mot
                rho = densita_materia(m, st_)
                lam = m.densita_vuoto(st_)
                with np.errstate(divide="ignore", invalid="ignore"):
                    x = np.where(lam > 0, rho / np.where(lam > 0, lam, 1.0), 0.0)
                al, be = _alpha_beta(forma, x)
                al = np.where(rho > 0, al, 0.0)
                al = np.where(np.isfinite(al), al, 0.0)
                be = np.where(np.isfinite(be), be, 0.0)
                import flussi_parziali as FP2
                dt = FP2.dtau_nodo(m)
                f = float(frazione)
                nodo = m.inc.nodo
                st_["psi_h"] *= np.exp(-1j * np.take(al * dt * f, nodo)).reshape(-1, 1)
                st_["phi_h"] *= np.exp(+1j * np.take(be * dt * f, nodo))
                m.applicazioni["CAMM-SATURAZIONE"] += 1
                return st_
            mot.operatori["CAMM-SATURAZIONE"] = rov
        else:
            mot.operatori["CAMM-SATURAZIONE"] = ag
    try:
        lam = [mot.densita_vuoto(st).copy()]
        rho = [densita_materia(mot, st)]
        for _t in range(tick):
            TK.tick(st, mot, par)
            lam.append(mot.densita_vuoto(st).copy())
            rho.append(densita_materia(mot, st))
    finally:
        mot.operatori["CAMM-SATURAZIONE"] = vero
    return np.array(lam), np.array(rho), per


def senza_materia(dtau, tick):
    ch = (dtau, tick)
    if ch not in _SENZA:
        _SENZA[ch] = _corri(dtau, 0.0, False, 1, "S1", False, tick)
    return _SENZA[ch]


def pari(dtau, x, elicita, forma, tick):
    """### `(E, O, per, dentro, rho)`."""
    amp = float(np.sqrt(x)) * VUOTO
    b, _rb, per = senza_materia(dtau, tick)
    a1, r1, _p = _corri(dtau, amp, True, elicita, forma, False, tick)
    a2, _r2, _p = _corri(dtau, amp, True, elicita, forma, True, tick)
    dentro = [v for d, nodi in per.items() if d <= RAGGIO for v in nodi]
    return 0.5 * ((a1 - b) + (a2 - b)), 0.5 * ((a1 - b) - (a2 - b)), per, dentro, r1


def media_barra(campo, nodi, finestre):
    t = campo.shape[0]
    b = [int(round(t * i / float(finestre))) for i in range(finestre + 1)]
    med = [float(np.mean(campo[b[i]:b[i + 1]][:, nodi])) for i in range(finestre)]
    return (float(np.mean(med)),
            float(np.std(med, ddof=1)) / np.sqrt(finestre) if finestre > 1 else
            float("nan"))


# ====================================================================== i bracci
def braccio_nullo():
    print("-" * 96)
    print("### (A) IL CONTROLLO NULLO: termine SPENTO -> dLambda = 0 esatto")
    for dtau in DTAU:
        b, _r, _p = senza_materia(dtau, 200)
        a, _r2, _p2 = _corri(dtau, 1.0, True, 1, "S1", False, 200, spento=True)
        m = float(np.max(np.abs(a - b)))
        esito("(A) termine spento, dtau = %.2f" % dtau, m <= 1e-12,
              "max |dLambda| = %.3e su 200 tick" % m)


def braccio_verso():
    print("-" * 96)
    print("### (B) IL VERSO, per forma: media di E sul grumo su %d tick, %d finestre"
          % (TICK, FINESTRE))
    fuori = {}
    for forma in FORME:
        for dtau in DTAU:
            t0 = time.time()
            E, O, per, dentro, rho = pari(dtau, 1.0, 1, forma, TICK)
            mE, sE = media_barra(E, dentro, FINESTRE)
            mO, sO = media_barra(O, dentro, FINESTRE)
            tutti = list(range(E.shape[1]))
            mT, sT = media_barra(E, tutti, FINESTRE)
            fuori[(forma, dtau)] = (mE, sE, mO, sO, mT)
            print("  %s dtau=%.2f   E = %+.6e +- %.3e (%.1f barre)   O = %+.6e +- %.3e"
                  "   somma-nodi %+.2e   [%.1f s]"
                  % (forma, dtau, mE, sE, abs(mE) / sE if sE > 0 else float("nan"),
                     mO, sO, mT, time.time() - t0))
            sys.stdout.flush()
    return fuori


def braccio_spin():
    print("-" * 96)
    print("### (C) L'INDIPENDENZA DALLO SPIN: +1, -1 e isotropo alla STESSA densita'")
    fuori = {}
    for forma in FORME:
        for dtau in DTAU_SPIN:
            riga = {}
            for el in (1, -1, 0):
                E, O, per, dentro, rho = pari(dtau, 1.0, el, forma, TICK)
                riga[el] = media_barra(E, dentro, FINESTRE) + (E[1][dentro].mean(),)
            a, b, c = riga[1], riga[-1], riga[0]
            d1 = abs(a[0] - b[0]) / np.sqrt(a[1] ** 2 + b[1] ** 2)
            d2 = abs(a[0] - c[0]) / np.sqrt(a[1] ** 2 + c[1] ** 2)
            fuori[(forma, dtau)] = (a, b, c, d1, d2)
            print("  %s dtau=%.2f   E(+1) = %+.4e   E(-1) = %+.4e   E(iso) = %+.4e"
                  % (forma, dtau, a[0], b[0], c[0]))
            print("        differenze: +1 contro -1 = %.1f barre, +1 contro iso = %.1f"
                  " barre" % (d1, d2))
            # ### ⭐ **E AL PRIMO TICK DEVONO ESSERE IDENTICI**, perche- `rho` e- LO
            # ### STESSO: e- il controllo che la sorgente e- davvero `rho`.
            m = max(abs(a[2] - b[2]), abs(a[2] - c[2]))
            esito("(C) %s: al PRIMO tick le tre elicita' danno lo STESSO dLambda" % forma,
                  m <= 1e-12,
                  "max differenza al tick 1 = %.3e: ### la sorgente E' rho" % m)
            sys.stdout.flush()
    return fuori


def braccio_esponente():
    print("-" * 96)
    print("### (D) L'ESPONENTE in x, per forma (%d tick)" % TICK_SCAN)
    fuori = {}
    for forma in FORME:
        for dtau in DTAU:
            punti = []
            for x in X_SCAN:
                E, O, per, dentro, rho = pari(dtau, x, 1, forma, TICK_SCAN)
                mE, sE = media_barra(E, dentro, FINESTRE_SCAN)
                punti.append((x, mE, sE))
            loc = []
            for i in range(1, len(punti)):
                x0, e0, _ = punti[i - 1]
                x1, e1, _ = punti[i]
                if e0 * e1 > 0:
                    loc.append((x0, x1, np.log(abs(e1 / e0)) / np.log(x1 / x0)))
            fuori[(forma, dtau)] = (punti, loc)
            print("  %s dtau=%.2f   E: %s" % (forma, dtau,
                  "  ".join("%.3g:%+.2e" % (x, e) for x, e, _s in punti)))
            print("        pendenze LOCALI: %s"
                  % "  ".join("[%.3g->%.3g] %.3f" % t for t in loc))
            sys.stdout.flush()
    return fuori


def braccio_lungo(verso):
    """### ⭐ **L-ESTENSIONE: le forme il cui verdetto non arriva a `3` barre, allungate.**"""
    print("-" * 96)
    print("### (B-bis) ESTENSIONE DICHIARATA: %d tick e %d finestre, per le forme indecise"
          % (TICK_LUNGO, FINESTRE_LUNGO))
    fuori = {}
    for forma in FORME:
        for dtau in DTAU:
            mE, sE = verso[(forma, dtau)][0], verso[(forma, dtau)][1]
            if sE > 0 and abs(mE) / sE >= 3.0:
                continue
            t0 = time.time()
            E, O, per, dentro, rho = pari(dtau, 1.0, 1, forma, TICK_LUNGO)
            m2, s2 = media_barra(E, dentro, FINESTRE_LUNGO)
            mo2, so2 = media_barra(O, dentro, FINESTRE_LUNGO)
            fuori[(forma, dtau)] = (m2, s2, mo2, so2)
            print("  %s dtau=%.2f   E = %+.6e +- %.3e (%.1f barre)   O = %+.6e +- %.3e"
                  " (%.1f barre)   [%.1f s]"
                  % (forma, dtau, m2, s2, abs(m2) / s2 if s2 > 0 else float("nan"),
                     mo2, so2, abs(mo2) / so2 if so2 > 0 else float("nan"),
                     time.time() - t0))
            sys.stdout.flush()
    return fuori


def braccio_cono():
    print("-" * 96)
    print("### (E) IL CONO, nei DUE modi: |alpha| dtau contro pi, e il cambiamento dello"
          " STATO")
    fuori = {}
    for forma in FORME:
        dtau = 0.5
        # ### la fase per tick al variare di `rho`, a `Lambda = 1`
        dove = None
        for rho in (1e-12, 1e-9, 1e-6, 1e-3, 1e-2, 1e-1, 1.0):
            al, _be = _alpha_beta(forma, np.array([rho]))
            fase = abs(float(al[0])) * dtau
            if dove is None and fase > np.pi:
                dove = (rho, fase)
        # ### e il cambiamento dello STATO per tick, con e senza il termine
        E, O, per, dentro, rho_t = pari(dtau, 1.0, 1, forma, 60)
        a1, r1, _p = _corri(dtau, 1.0, True, 1, forma, False, 60)
        a0, r0, _p = _corri(dtau, 1.0, True, 1, forma, False, 60, spento=True)
        # ### il cambiamento dello stato si legge su `rho` per nodo, tick per tick
        dr1 = float(np.max(np.abs(np.diff(r1, axis=0))))
        dr0 = float(np.max(np.abs(np.diff(r0, axis=0))))
        fuori[forma] = (dove, dr1, dr0)
        print("  %s   |alpha| dtau > pi per la PRIMA volta a rho = %s   (la' la fase vale"
              " %s)" % (forma,
                        "%.0e" % dove[0] if dove else "MAI (su rho da 1e-12 a 1)",
                        "%.3f" % dove[1] if dove else "-"))
        print("        e il CAMBIAMENTO DI STATO per tick, max |d rho_k|: col termine"
              " %.6e, senza %.6e  -> rapporto %.3f"
              % (dr1, dr0, dr1 / dr0 if dr0 > 0 else float("nan")))
        sys.stdout.flush()
    return fuori


def braccio_larghezza():
    print("-" * 96)
    print("### (F) LA LARGHEZZA DEL GRUMO nel tempo (raggio quadratico medio di rho)")
    import scena_l2 as SC
    _i, _m, _s, _p, centro, per = SC.scena(0.5, VUOTO, 1.0, RAGGIO, True, True, False,
                                           SEME, 1)
    dist = np.zeros(sum(len(v) for v in per.values()))
    for d, nodi in per.items():
        for v in nodi:
            dist[v] = d
    fuori = {}
    for forma in list(FORME) + ["ATTUALE (h, rotazione)"]:
        if forma.startswith("ATTUALE"):
            a, r, _p = _corri(0.5, 1.0, True, 1, "S1", False, TICK, spento=False)
            # ### ⚠ **l-ATTUALE e- il termine DEL MOTORE**, non una sostituzione: si gira
            # ### ### **senza sostituire niente.**
            import deriva as DV
            inc, mot, st, par, _c, per2 = SC.scena(0.5, VUOTO, 1.0, RAGGIO, True, True,
                                                   False, SEME, 1)
            r = [densita_materia(mot, st)]
            for _t in range(TICK):
                TK.tick(st, mot, par)
                r.append(densita_materia(mot, st))
            r = np.array(r)
        else:
            _a, r, _p = _corri(0.5, 1.0, True, 1, forma, False, TICK)
        tot = np.sum(r, axis=1)
        w = np.sqrt(np.sum(r * (dist ** 2).reshape(1, -1), axis=1) / tot)
        fuori[forma] = (float(w[0]), float(w[len(w) // 2]), float(w[-1]),
                        float(np.max(w)))
        print("  %-22s larghezza: t=0 %.4f   meta' %.4f   fine %.4f   max %.4f"
              % (forma, w[0], w[len(w) // 2], w[-1], np.max(w)))
        sys.stdout.flush()
    return fuori


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import scena_l2 as SC
    t0 = time.time()
    print("=" * 96)
    print("LE QUATTRO FORME, MISURATE -- con rho come sorgente. IL MOTORE NON SI TOCCA.")
    print("=" * 96)
    print("  LA CONFIGURAZIONE: toro %s   TICK = %d (%d nella scansione)   FINESTRE = %d"
          "   raggio = %d   seme = %d   vuoto = %.1f"
          % (SC.LATI, TICK, TICK_SCAN, FINESTRE, RAGGIO, SEME, VUOTO))
    print("  dtau = %s (lo spin a %s)   x = %s   forme = %s"
          % (DTAU, DTAU_SPIN, X_SCAN, FORME))
    print("  ### CORSE LUNGHE: stanno FUORI dal pre-commit, come misure DICHIARATE.")
    sys.stdout.flush()
    braccio_nullo()
    verso = braccio_verso()
    braccio_spin()
    esp = braccio_esponente()
    lungo = braccio_lungo(verso)
    braccio_cono()
    braccio_larghezza()
    print("=" * 96)
    print("### IL VERDETTO, forma per forma")
    for forma in FORME:
        for dtau in DTAU:
            if (forma, dtau) in lungo:
                mE, sE = lungo[(forma, dtau)][0], lungo[(forma, dtau)][1]
                quanti = TICK_LUNGO
            else:
                mE, sE = verso[(forma, dtau)][0], verso[(forma, dtau)][1]
                quanti = TICK
            barre = abs(mE) / sE if sE > 0 else float("nan")
            esito("(B) %s a dtau=%.2f: E fuori da 3 barre" % (forma, dtau),
                  barre >= 3.0,
                  "E = %+.4e +- %.3e (%.1f barre, %d tick) -> %s"
                  % (mE, sE, barre, quanti,
                     ("il vuoto si ACCUMULA" if mE > 0 else "la materia CONSUMA")
                     if barre >= 3 else "indeciso"))
    print("=" * 96)
    print("  %d su %d   [corsa intera: %.1f s]" % (OK[0], OK[1], time.time() - t0))
    print("### ⛔ E LA FORMA NON SI DECIDE QUI: la tabella delle leggi NON e' toccata,")
    print("###   e la scelta fra S1-S4 (o altro) e' di Luca.")
    print("=" * 96)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
