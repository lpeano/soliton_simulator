# -*- coding: utf-8 -*-
r"""**LE PROVE DELLA TOLLERANZA DI `Omega` SULLA SCALA DEI DATI** — *`P1`-`P4` e `P6`.*

> ### ⛔ **Il task history e' `2026-10-19_tolleranza_omega.md`** *(`1c6f4167`)*, che fissa
> la scala, le prove e cosa ferma ciascuna; il codice e' `7395cd9a`.

- `P1` ### **il fatto del guardiano, riprodotto:** rapporto `1`, `dtau 0.5`, `x 0.01`, la
  prima applicazione dove ### **il criterio di prima** non si sarebbe fermato.
- `P2` ### **il controllo positivo, che puo' fallire:** `6` bracci di `D4` *(`x 0.01` e `x 1`,
  ai tre rapporti, `dtau 0.5`, i primi `20` tick)*; per ogni applicazione il punto fisso si
  itera ### **fino a `GIRI_MAX_OMEGA`** *(una copia DICHIARATA del corpo del ciclo di
  `applica`, che non si ferma)*, e la STAGNAZIONE e' ### **la mediana degli ultimi `10`
  scarti.** ### **Passa se `stagnazione / (eps * scala) <= 8` in tutte.**
- `P3` ### **i due casi sintetici:** uno scarto che si ferma al rumore ### **converge**; un
  ciclo di periodo `2` di ampiezza `1e-6` ### **ALZA**.
- `P4` ### **il braccio reale che deve ALZARE:** `applica` a frazione `16` *(`tau = 8`)* sul
  grumo a `x = 1`.
- `P6` ### **il braccio `0` con `cs` ACCESO:** la scena di `C1`, `dtau 0.25`, `32` tick; a
  ogni tick ### **un tick dal MEDESIMO stato** col codice di PRIMA *(`energia_pesata` al blob
  di `1c6f4167`)* e con quello di adesso: `max|delta phi| <= n_app * tau * max|phi| *
  EPS_OMEGA * scala`.

Gira con:  python csv/_tolleranza_omega.py
"""
import hashlib
import importlib.util
import io
import os
import subprocess
import sys
import tempfile

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

PRIMA = "1c6f4167"            # il commit PRIMA del codice (il task history)
TICK_P2 = 20
FRAZIONE_P4 = 16.0
TICK_P6 = 32
EPS = float(np.finfo(float).eps)
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-64s %s   %s" % (che[:64], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def _copia(st):
    return {k: (v.copy() if hasattr(v, "copy") else v) for k, v in st.items()}


# =====================================================================================
#   LA DIAGNOSI DI UNA APPLICAZIONE: la copia DICHIARATA del corpo del ciclo
# =====================================================================================
def diagnosi(mot, st, par, frazione):
    """### Lo scarto a ogni giro, ### **fino a `GIRI_MAX_OMEGA`, senza fermarsi.**"""
    import energia_pesata as EP
    s = _copia(st)
    tau = float(mot.dtau[0]) * float(frazione)
    phi = s["phi_h"]
    salvo = phi.copy()
    prec = EP.omega(mot, s, par).copy()
    seq = []
    for _g in range(EP.GIRI_MAX_OMEGA):
        np.multiply(salvo, np.exp(-1j * (prec * (tau * 0.5))[mot.inc.nodo]), out=phi)
        nuovo = EP.omega(mot, s, par)
        seq.append(float(np.max(np.abs(nuovo - prec))))
        prec = nuovo.copy()
    pn, pa = EP.termini_di_h(mot, s, par)
    lam = mot.densita_vuoto(s)
    csp = EP.cs_primo(lam, mot.lambda_c, np.empty(mot.inc.n))
    dw = EP.d_peso_arco(mot)
    arco = EP._per_nodo(mot, dw * np.repeat(pa, 2), np.empty(mot.inc.n))
    return {"seq": seq, "stagnazione": float(np.median(seq[-10:])),
            "max_omega": float(np.max(np.abs(prec))),
            "nodo": float(np.max(np.abs(csp * pn))), "arco": float(np.max(np.abs(csp * arco))),
            "scala": EP.scala_omega(mot, st)}


def braccio_p2(rapporto, x):
    """### Le diagnosi di tutte le applicazioni nei primi `TICK_P2` tick di un braccio."""
    import _misura_d4 as D4
    import energia_pesata as EP
    import statica_protocollo as PR
    PR.SOSTITUISCI = False
    lc = rapporto * D4.lambda_medio(PR.DTAU[0])
    vero = EP.applica
    diag = []

    def applica(mot, st, par, frazione):
        if mot.cs is not None and mot.lambda_c is not None:
            diag.append(diagnosi(mot, st, par, frazione))
        return vero(mot, st, par, frazione)
    EP.applica = applica
    try:
        PR.corri(PR.DTAU[0], x, "S3", TICK_P2, PR.T_ACCENSIONE[1], (0,), congela="pezzo",
                 lambda_c=lc)
    finally:
        EP.applica = vero
    return diag


def p1_p2():
    import energia_pesata as EP
    print("### P1 + P2: la stagnazione dello scarto, contro la scala VECCHIA e la NUOVA")
    print("  (le prime %d tick di 6 bracci di D4, dtau 0.5; scala vecchia = max|Omega|)"
          % TICK_P2)
    peggio_nuova, quanti, falsi_vecchi = 0.0, 0, 0
    p1 = None
    print("  %-8s %-6s %-6s %-14s %-14s %-12s %s"
          % ("rapporto", "x", "app.", "stagn. max", "ulp NUOVA max", "ulp VECCHIA", "alzava?"))
    for r in (0.1, 1.0, 10.0):
        for x in (0.01, 1.0):
            dd = braccio_p2(r, x)
            un = [d["stagnazione"] / (EPS * d["scala"]) for d in dd]
            uv = [d["stagnazione"] / (EPS * d["max_omega"]) if d["max_omega"] > 0
                  else float("inf") for d in dd]
            falsi = sum(1 for d in dd
                        if not any(q <= EP.EPS_OMEGA * d["max_omega"] for q in d["seq"]))
            falsi_vecchi += falsi
            quanti += len(dd)
            peggio_nuova = max([peggio_nuova] + un)
            print("  %-8g %-6g %-6d %-14.3e %-14.2f %-12.2f %d applicazioni su %d"
                  % (r, x, len(dd), max(d["stagnazione"] for d in dd), max(un), max(uv),
                     falsi, len(dd)))
            sys.stdout.flush()
            if p1 is None and r == 1.0 and x == 0.01:
                for d in dd:
                    if not any(q <= EP.EPS_OMEGA * d["max_omega"] for q in d["seq"]):
                        p1 = d
                        break
    print("-" * 100)
    if p1 is not None:
        print("### P1: il punto del guardiano (rapporto 1, dtau 0.5, x 0.01), la prima")
        print("  applicazione in cui il criterio di PRIMA non si sarebbe fermato:")
        print("     gli ultimi 10 scarti: %s" % "  ".join("%.2e" % q for q in p1["seq"][-10:]))
        print("     stagnazione (mediana degli ultimi 10) %.3e" % p1["stagnazione"])
        print("     max|Omega| = %.3e  -> soglia VECCHIA 8 eps max|Omega| = %.3e"
              % (p1["max_omega"], EP.EPS_OMEGA * p1["max_omega"]))
        print("     i termini: max|cs' x nodo| = %.3e   max|cs' x arco| = %.3e"
              % (p1["nodo"], p1["arco"]))
        print("     la scala NUOVA max|cs'| pi (Lambda + rho) = %.3e -> soglia %.3e"
              % (p1["scala"], EP.EPS_OMEGA * p1["scala"]))
    else:
        print("### P1: ### nessuna applicazione del braccio (1, 0.01) era un falso non-converge")
    esito("P2 la stagnazione sta entro 8 ulp della scala NUOVA, in tutte le "
          "applicazioni", peggio_nuova <= 8.0,
          "%d applicazioni, il peggio %.2f ulp; con la scala VECCHIA alzavano %d"
          % (quanti, peggio_nuova, falsi_vecchi))


def p3():
    import energia_pesata as EP
    print("-" * 100)
    print("### P3: il criterio sui due casi SINTETICI (scala 1)")

    def converge(seq):
        for q in seq[:EP.GIRI_MAX_OMEGA]:
            if EP.entro_tolleranza(q, 1.0):
                return True
        return False
    rumore = [max(1e-2 * 0.1 ** k, 1.5 * EPS) for k in range(EP.GIRI_MAX_OMEGA)]
    ciclo = [2e-6] * EP.GIRI_MAX_OMEGA
    esito("P3 (i) uno scarto che si ferma al rumore (1.5 ulp) CONVERGE", converge(rumore), "")
    esito("P3 (ii) un ciclo di periodo 2 di ampiezza 1e-6 ALZA", not converge(ciclo),
          "lo scarto resta 2e-6 a ogni giro")


def p4():
    import energia_pesata as EP
    import flussi_parziali as FP
    import scena_l2 as SC
    import statica_protocollo as PR
    print("-" * 100)
    print("### P4: il braccio REALE che deve ALZARE: applica a frazione %g (tau = %g)"
          % (FRAZIONE_P4, PR.DTAU[0] * FRAZIONE_P4))
    inc, mot, st, par, _c, _per = SC.scena(PR.DTAU[0], PR.VUOTO, 0.0, PR.RAGGIO, False, True,
                                           False, PR.SEME, 1, lati=PR.LATI)
    PR.metti_grumi(st, inc, PR.LATI, (0,), PR.RAGGIO, PR.VUOTO)
    FP.accendi_cs(mot, float(np.mean(mot.densita_vuoto(st))), st)
    try:
        EP.applica(mot, st, par, FRAZIONE_P4)
        alza, nota = False, "### ha CONVERGIUTO in %d giri" % mot.giri_omega
    except AssertionError as e:
        alza, nota = True, str(e)[:90]
    esito("P4 una NON convergenza vera continua ad ALZARE", alza, nota)


def _vecchio():
    """### `energia_pesata` al blob di `PRIMA`, ### **come modulo a parte.**"""
    src = subprocess.check_output(["git", "show", PRIMA + ":primo_ordine/energia_pesata.py"],
                                  cwd=RADICE)
    d = tempfile.mkdtemp()
    p = os.path.join(d, "energia_pesata_prima.py")
    io.open(p, "wb").write(src)
    spec = importlib.util.spec_from_file_location("energia_pesata_prima", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m, hashlib.sha1(src).hexdigest()[:8]


def p6():
    import _misura_hw as HW
    import _misura_mb2 as MB2
    import deriva as DV
    import energia_pesata as EP
    import flussi_parziali as FP
    import tick as TK
    print("-" * 100)
    vecchio, blob = _vecchio()
    print("### P6: il braccio 0 con cs ACCESO -- la scena di C1, dtau 0.25, %d tick; a ogni"
          " tick UN tick dal medesimo stato col codice di PRIMA (energia_pesata a %s, sha1"
          " %s) e con quello di adesso" % (TICK_P6, PRIMA, blob))
    dtau = 0.25
    inc, mot, st, par = DV.scena(MB2.NN, MB2.SEME, dtau, norma=MB2.NORMA,
                                 vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
    st["psi_h"][...], st["phi_h"][...] = HW.stato_non_uniforme()
    lc = float(np.mean(mot.densita_vuoto(st)))
    FP.accendi_cs(mot, lc, st)
    vero = EP.applica
    conto = {"n": 0, "scala": 0.0}

    def nuovo(m, s, p, f):
        conto["n"] += 1
        conto["scala"] = max(conto["scala"], EP.scala_omega(m, s))
        return vero(m, s, p, f)
    peggio = 0.0
    try:
        for _t in range(TICK_P6):
            pre = _copia(st)
            EP.applica = vecchio.applica
            TK.tick_con_cs(pre, mot, par, lc, ())
            EP.applica = nuovo
            conto["n"], conto["scala"] = 0, 0.0
            TK.tick_con_cs(st, mot, par, lc, ())
            d = float(np.max(np.abs(st["phi_h"] - pre["phi_h"])))
            d = max(d, float(np.max(np.abs(st["psi_h"] - pre["psi_h"]))))
            limite = (conto["n"] * dtau * 0.5 * float(np.max(np.abs(st["phi_h"])))
                      * EP.EPS_OMEGA * conto["scala"])
            peggio = max(peggio, d / limite if limite > 0 else (0.0 if d == 0 else 1e300))
    finally:
        EP.applica = vero
    esito("P6 con cs acceso il passo resta entro la tolleranza nuova, a ogni tick",
          peggio <= 1.0, "il peggio: %.3f volte il limite" % peggio)


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import energia_pesata as EP
    print("=" * 100)
    print("LE PROVE DELLA TOLLERANZA DI `Omega` SULLA SCALA DEI DATI -- P1-P4 e P6")
    print("=" * 100)
    print("  EPS_OMEGA = 8 eps = %.3e   GIRI_MAX_OMEGA = %d   la scala: max|cs'| pi"
          " (Lambda + rho)" % (EP.EPS_OMEGA, EP.GIRI_MAX_OMEGA))
    print("-" * 100)
    p1_p2()
    p3()
    p4()
    p6()
    print("=" * 100)
    print("LE PROVE: %d su %d" % (OK[0], OK[1]))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
