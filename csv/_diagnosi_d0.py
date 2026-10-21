# -*- coding: utf-8 -*-
r"""**LA DIAGNOSI DELLA REGRESSIONE DI `D0`: il punto fisso di `Omega`, giro per giro.**

> ### ⛔ **Il task history e' `2026-10-21_regressione_d0.md`** *(`db3ee090`)*. ### **Una diagnosi:
> nessun file del nucleo si tocca.** Si ripete il braccio `braccio_accesa` di
> `primo_ordine/_collauda_cs.py` *(`corri(nn, seme, LC_DI_PROVA)`)* e, ### **SOLO IN MEMORIA**,
> `energia_pesata.applica` si avvolge con ### **una COPIA del suo ciclo che registra**, a ogni giro:
> `max|cs'|`, `max tetto_k`, `max|Omega|`, la scala del criterio, lo scarto.

## ⛔ IL CONTROLLO CHE RIPETE LA COSA GIUSTA

### **La copia deve ALZARE la stessa eccezione dell'originale, con lo stesso scarto finale**
*(`1.252e-12`, `3008bd13`)*: ### **se no, la diagnosi misura un'altra cosa.**

Gira con:  python csv/_diagnosi_d0.py
"""
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

EPS = float(np.finfo(float).eps)
JSONL = os.path.join(RADICE, "doc", "referti_l2", "diagnosi_d0.jsonl")


class Registra(Exception):
    pass


def applica_registrata(EP, registro):
    """### La COPIA del ciclo di `EP.applica`, che registra: stessi conti, stesso ordine."""
    def applica(mot, st, par, frazione):
        if mot.cs is None or mot.lambda_c is None:
            return st
        tau = float(mot.dtau[0]) * float(frazione)
        phi = st["phi_h"]
        salvo = mot._b("ep_phi_salvo", phi.shape, phi.dtype)
        salvo[...] = phi
        prec = EP.omega(mot, st, par).copy()
        tetto = EP.tetto_omega(mot, st, par)
        EP.controlla_tetto(prec, tetto, "Omega di partenza")
        scala = float(np.max(tetto))
        lam = mot.densita_vuoto(st)
        csp = float(np.max(np.abs(EP.cs_primo(lam, mot.lambda_c, np.empty(mot.inc.n)))))
        giri_reg = []
        giri = 0
        for giri in range(1, EP.GIRI_MAX_OMEGA + 1):
            np.multiply(salvo, np.exp(-1j * (prec * (tau * 0.5))[mot.inc.nodo]), out=phi)
            nuovo = EP.omega(mot, st, par)
            scarto = float(np.max(np.abs(nuovo - prec)))
            giri_reg.append((scarto, float(np.max(np.abs(nuovo)))))
            if EP.entro_tolleranza(scarto, scala):
                prec = nuovo.copy()
                EP.controlla_tetto(prec, EP.tetto_omega(mot, st, par), "Omega finale")
                break
            prec = nuovo.copy()
        else:
            phi[...] = salvo
            registro.append({"csp": csp, "tetto": scala, "criterio": EP.EPS_OMEGA * scala,
                             "giri": giri_reg})
            raise Registra("il punto medio NON CONVERGE: ultimo scarto %.3e" % scarto)
        np.multiply(salvo, np.exp(-1j * (prec * tau)[mot.inc.nodo]), out=phi)
        mot.giri_omega = giri
        registro.append({"csp": csp, "tetto": scala, "criterio": EP.EPS_OMEGA * scala,
                         "giri": giri_reg, "convergenza": giri})
        return st
    return applica


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import _collauda_cs as CC
    import energia_pesata as EP
    import flussi_parziali as FP
    import tick as TK
    print("=" * 100)
    print("LA DIAGNOSI DELLA REGRESSIONE DI D0: il punto fisso di Omega, giro per giro")
    print("=" * 100)
    print("  il braccio: braccio_accesa di _collauda_cs.py: corri(nn, seme, %g), DTAU %g, TICK %d,"
          " VUOTO_MODULO %g; EPS_OMEGA %.3e, GIRI_MAX_OMEGA %d"
          % (CC.LC_DI_PROVA, CC.DTAU, CC.TICK, CC.VUOTO_MODULO, EP.EPS_OMEGA, EP.GIRI_MAX_OMEGA))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    vero = EP.applica
    for nn, seme in CC.SCENE:
        # ### l'ORIGINALE, per lo scarto finale
        orig = None
        _i, mot, st, par = CC.scena(nn, seme)
        tick_orig = None
        try:
            for t in range(CC.TICK):
                FP.accendi_cs(mot, CC.LC_DI_PROVA, st)
                TK.tick(st, mot, par)
        except AssertionError as e:
            orig = str(e)
            tick_orig = t
        # ### la COPIA che registra
        registro = []
        EP.applica = applica_registrata(EP, registro)
        copia, tick_copia = None, None
        try:
            _i, mot, st, par = CC.scena(nn, seme)
            for t in range(CC.TICK):
                FP.accendi_cs(mot, CC.LC_DI_PROVA, st)
                TK.tick(st, mot, par)
        except Registra as e:
            copia = str(e)
            tick_copia = t
        finally:
            EP.applica = vero
        print("### scena nn=%d seme=%d" % (nn, seme))
        print("  l'originale: %s" % ("ALZA al tick %d: %s" % (tick_orig, orig[:110]) if orig
                                      else "passa tutti i %d tick" % CC.TICK))
        print("  la copia:    %s" % ("ALZA al tick %d: %s" % (tick_copia, copia) if copia
                                      else "passa tutti i %d tick" % CC.TICK))
        uguale = (orig is None) == (copia is None) and tick_orig == tick_copia
        if orig and copia:
            so = orig.split("ultimo scarto ")[1].split(")")[0]
            sc = copia.split("ultimo scarto ")[1]
            uguale &= so == sc
        print("  ### LA COPIA RIPETE L'ORIGINALE: %s" % ("SI'" if uguale else "### NO -- STOP"))
        if not uguale:
            return 1
        if registro:
            conv = [r.get("convergenza") for r in registro if "convergenza" in r]
            print("  le chiamate di applica: %d; giri alla convergenza: min %s, max %s"
                  % (len(registro), min(conv) if conv else "-", max(conv) if conv else "-"))
            ult = registro[-1]
            print("  L'ULTIMA CHIAMATA%s: max|cs'| %.6e, max tetto %.6e, il criterio (8 ulp del tetto)"
                  " %.3e" % (" (QUELLA CHE ALZA)" if "convergenza" not in ult else "",
                             ult["csp"], ult["tetto"], ult["criterio"]))
            g = ult["giri"]
            for k in list(range(0, min(len(g), 12))) + list(range(max(12, len(g) - 6), len(g))):
                print("     giro %3d  scarto %.6e  max|Omega| %.6e  scarto/criterio %.3e"
                      "  scarto/(8 ulp max|Omega|) %.3e"
                      % (k + 1, g[k][0], g[k][1], g[k][0] / ult["criterio"],
                         g[k][0] / (EP.EPS_OMEGA * g[k][1]) if g[k][1] else float("inf")))
            sc = np.array([x[0] for x in g])
            w = min(60, len(sc))
            rap = sc[-1] / sc[-2] if len(sc) > 1 else float("nan")
            print("  lo scarto negli ultimi %d giri: min %.3e, max %.3e (cala? %s); il rapporto"
                  " dell'ultimo giro %.4f" % (w, sc[-w:].min(), sc[-w:].max(),
                                             "si'" if sc[-1] < 0.5 * sc[-w] else
                                             "NO, si ferma o oscilla", rap))
            if "convergenza" not in ult and 0 < rap < 1:
                manca = np.log(sc[-1] / ult["criterio"]) / -np.log(rap)
                print("  ### a quel ritmo, i giri che mancano al criterio: %.1f (in tutto %.0f)"
                      % (manca, len(sc) + manca))
            with io.open(JSONL, "a", encoding="utf-8") as f:
                f.write(json.dumps({"nn": nn, "seme": seme, "tick": tick_copia,
                                    "ultima": ult, "chiamate": len(registro)}) + "\n")
        print("-" * 100)
        sys.stdout.flush()
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
