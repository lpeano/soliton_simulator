# -*- coding: utf-8 -*-
r"""**IL VUOTO VIVO: PERCHE' `H_tot` NON SCALA COME `s^2`** *(il mandato di Luca delle `11:22` del `2026-11-01`, sull'esito di `326747d0`; NESSUNA MODIFICA AL NUCLEO;
[[LIBRO-DEI-CONTI]], [[VUOTO-SUL-FONDO]]; il task history `doc/TASK_HISTORY/2026-11-01_energia_e_respiro.md`)*:
### **(E0)** la correzione del libro dei conti *(il `par` del tick)*: il caso nullo e il termine della moneta; ### **(E1)** il vuoto a due `s`, al bit;
### **(E2)** le corse brevi sono quelle committate, al bit; ### **(E3)** il rapporto di `max abs(H - H(0))` fra `s 0.15` e `0.075` col termine della moneta;
### **(E4)** quando cade il massimo.

    python csv/_energia_vuoto_vivo.py > doc/referti_l2/energia_vuoto_vivo.txt
"""
import math
import os
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

import _vuoto_vivo_B as V                                      # noqa: E402

PASSI = (0.15, 0.075)
TAU_BREVE = 150.0              # ### prima della dissoluzione di BG-U (tempo 160.5, 326747d0)
TAU_PRIMI = 10.0               # ### (E4): il massimo nei primi 10 unita' di tempo e dopo
CORSE_BREVI = ("BG-U", "BG-F")
TOLL_MONETA = 1e-12            # ### relativo: tot(eps) - tot(0) contro eps * sum(elicita)
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if deve and not passa:
        FALLITE.append(che)
    print("  %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def preparata(z, phi0, pK, sol, s):
    """### **La partenza come in `_vuoto_vivo_B.corsa`:** l'inviluppo *(o `pK`)*, `e_K`, ### **lo stato della scena rimesso**, poi `psi_h = p0`."""
    salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
    p0, info = V.partenza(sol, z, phi0, pK, s)
    e_K = V.e_K_di(z)
    for k, v in salvato.items():
        z["st"][k][...] = v
    z["st"]["psi_h"][...] = p0
    return p0, info, e_K


def e0():
    import _deriva_congelato as DC
    import _energia_del_legame as EL
    import _libro_dei_conti as LC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    print("### (E0) LA CORREZIONE: il par del tick nel libro dei conti (la scena U, s %g, eps %g, lo stato BG)" % (PASSI[0], V.EPS))
    with V.scena(PASSI[0], "uniforme", V.EPS) as (_rec, z, phi0, pK):
        _p0, _info, e_K = preparata(z, phi0, pK, "BG", PASSI[0])
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            a = LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO)
            b = LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO, EL.PAR)
            c = LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO, {"eps": 0.0})
            d = LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO, z["par"])
            h = z["mot"].elicita(z["st"])
        eps = float(z["par"]["eps"])
    nullo = all(a[k].tobytes() == b[k].tobytes() == c[k].tobytes() for k in a)
    esito("DEVE PASSARE: senza par = col PAR del modulo = col par a eps 0, AL BIT, ogni conto", nullo, " ".join(sorted(a)) + "; PAR %s" % EL.PAR)
    dt = math.fsum(d["tot"].tolist()) - math.fsum(a["tot"].tolist())
    atteso = eps * math.fsum(h.tolist())
    rel = abs(dt - atteso) / abs(atteso) if atteso else float("inf")
    uguali = all(d[k].tobytes() == a[k].tobytes() for k in ("leg", "vuo", "M", "V", "cost"))
    esito("DEVE PASSARE: col par della corsa (eps %g) tot cambia di eps * sum(elicita) (entro %g relativo), e solo cin e tot cambiano" % (eps, TOLL_MONETA), rel <= TOLL_MONETA and uguali,
          "tot(eps) - tot(0) %+.6e, eps * sum(h) %+.6e, relativo %.1e; leg vuo M V cost al bit: %s; in N |e_K| %+.4e" % (dt, atteso, rel, uguali, dt / (V.N * abs(e_K))))


def e1():
    print("### (E1) IL VUOTO A DUE s: phi_h della scena a s %g = a s %g, AL BIT" % PASSI)
    for v in ("uniforme", "fondo"):
        ph = []
        for s in PASSI:
            with V.scena(s, v, V.EPS) as (_rec, z, _phi0, _pK):
                ph.append(z["st"]["phi_h"].tobytes())
        esito("FATTO (non un sigillo): il vuoto %s a s %g = a s %g, al bit" % ((v,) + PASSI), ph[0] == ph[1], "", deve=False)


def breve(nome, s):
    """### **La corsa breve:** fino a `TAU_BREVE`, `H_tot` del libro *(eps `0`)* e col `par` della corsa, a ogni tick."""
    import _deriva_congelato as DC
    import _libro_dei_conti as LC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import composizione as CM
    import tick as TK
    sol, vuoto = nome.split("-")
    n_t = int(round(TAU_BREVE / s))
    h0, h5 = [], []
    s0 = time.time()
    with V.scena(s, "uniforme" if vuoto == "U" else "fondo", V.EPS) as (_rec, z, phi0, pK):
        _p0, _info, e_K = preparata(z, phi0, pK, sol, s)
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            for t in range(n_t + 1):
                if t:
                    TK.percorri_tick(z["st"], z["mot"], z["par"], (), None, len(CM.ORDINE))
                h0.append(math.fsum(LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO)["tot"].tolist()))
                h5.append(math.fsum(LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO, z["par"])["tot"].tolist()))
    return {"h0": np.array(h0), "h5": np.array(h5), "e_K": e_K, "secondi": time.time() - s0}


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("IL VUOTO VIVO: PERCHE' H_tot NON SCALA COME s^2 (Luca 11:22) -- la scena di _vuoto_vivo_B (N %.0e, L %d, eps %g, il tick intero, cs spento, lo zero %s)" % (V.N, V.L, V.EPS, "conv('simm')"))
    print("  la configurazione: PASSI %s TAU_BREVE %g TAU_PRIMI %g CORSE_BREVI %s TOLL_MONETA %g; RAPPORTO %s LAM_ZERO %g OGNI %d (di _vuoto_vivo_B); l'unita' N |e_K|" % (PASSI, TAU_BREVE, TAU_PRIMI, CORSE_BREVI, TOLL_MONETA, V.RAPPORTO, V.LAM_ZERO, V.OGNI))
    print("=" * 130)
    e0()
    e1()
    print("### (E2, E3) LE CORSE BREVI, fino a tempo %g (dichiarate): H del libro a eps 0 e col par della corsa" % TAU_BREVE)
    R = {}
    for nome in CORSE_BREVI:
        for s in PASSI:
            r = breve(nome, s)
            R[(nome, s)] = r
            _t, camp, _dd, _rr = V.serie("%s-%g" % (nome, s))
            com = {c["t"]: c["E"]["totale"]["tot"] for c in camp if c["t"] <= len(r["h0"]) - 1}
            ug = all(r["h0"][t] == v for t, v in com.items())
            esito("DEVE PASSARE: %s a s %g = la corsa committata, H del libro (eps 0) AL BIT su %d campioni" % (nome, s, len(com)), ug and len(com) > 0, "%.0f s" % r["secondi"])
    print("-" * 130)
    for nome in CORSE_BREVI:
        for chiave, che in (("h0", "il libro a eps 0 (la definizione di 326747d0)"), ("h5", "col termine della moneta (il par della corsa)")):
            dd = []
            for s in PASSI:
                r = R[(nome, s)]
                dd.append(float(np.max(np.abs(r[chiave] - r[chiave][0]))))
                print("  %s s %-6g %-48s max|H - H(0)| %.4e (in N |e_K| %.4e)" % (nome, s, che, dd[-1], dd[-1] / (V.N * abs(r["e_K"]))))
            rap = dd[0] / dd[1] if dd[1] > 0 else float("inf")
            ok = V.RAPPORTO[0] <= rap <= V.RAPPORTO[1]
            if chiave == "h5":
                esito("DEVE PASSARE (Luca): %s, col termine della moneta, il rapporto fra s %g e %g sul tempo %g fra %g e %g" % ((nome,) + PASSI + (TAU_BREVE,) + V.RAPPORTO), ok, "%.4f" % rap)
            else:
                esito("DEVE FALLIRE (il caso di 326747d0): %s, il libro a eps 0, lo stesso rapporto FUORI da %g-%g" % ((nome,) + V.RAPPORTO), not ok, "%.4f" % rap)
    print("-" * 130)
    print("### (E4) QUANDO CADE IL MASSIMO")
    for nome in CORSE_BREVI:
        for s in PASSI:
            _t, camp, _dd, _rr = V.serie("%s-%g" % (nome, s))
            H = np.array([c["E"]["totale"]["tot"] for c in camp])
            tt = np.array([c["t"] for c in camp]) * s
            i = int(np.argmax(np.abs(H - H[0])))
            r = R[(nome, s)]
            tb = np.arange(len(r["h0"])) * s
            pr = tb <= TAU_PRIMI
            sc = V.N * abs(r["e_K"])
            print("  %s s %-6g: la corsa committata (eps 0): il massimo a tempo %.1f (di %.1f); la breve: eps 0 nei primi %g %.3e, dopo %.3e; con la moneta nei primi %g %.3e, dopo %.3e (in N |e_K|)"
                  % (nome, s, tt[i], tt[-1], TAU_PRIMI, np.max(np.abs(r["h0"][pr] - r["h0"][0])) / sc, np.max(np.abs(r["h0"][~pr] - r["h0"][0])) / sc,
                     TAU_PRIMI, np.max(np.abs(r["h5"][pr] - r["h5"][0])) / sc, np.max(np.abs(r["h5"][~pr] - r["h5"][0])) / sc))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


if __name__ == "__main__":
    main(sys.argv[1:])
