# -*- coding: utf-8 -*-
r"""**I TEST DELLE USCITE** *(il task history `2026-11-01_cassetta_solitone`, `U1`-`U3`)*: ### **i numeri gia' committati, AL BIT.**"""
import json
import math
import os

from . import RADICE
from . import uscite as U


def _riga_con(percorso, *pezzi):
    with open(percorso, encoding="utf-8") as f:
        return [r for r in f.read().splitlines() if all(p in r for p in pezzi)]


def gira(esito):
    import _bande_piatte as BP
    import _chiudere_le_uscite as CU
    import _dove_va_la_materia as DV
    import _livelli_piatti as LP
    import _massimo_di_B as MB
    import _scatola as SC
    print("### LE USCITE (csv/solitone/uscite.py)")
    esito("DEVE PASSARE: le costanti = quelle degli strumenti (GRUPPI, W, TOLL_RES_REL, Omega a s %g)" % LP.S,
          U.GRUPPI == DV.GRUPPI and U.W == CU.W and U.TOLL_RES_REL == SC.TOLL_RES_REL and U.omega(LP.S) == CU.OMEGA and BP.S_MENU == LP.S, "")
    # ### U1: previsioni.json di _massimo_di_B, ogni valore
    with open(os.path.join(MB.DIR_JSON, "previsioni.json"), encoding="utf-8") as f:
        prev = json.loads(f.read())
    om = U.omega(LP.S)
    for nome, eps in MB.CASI.items():
        lib = CU.Libero(eps)
        E = BP.fasi(lib.tick(math.pi, math.pi), LP.S)
        sp = U.gruppi_di(E)
        E0 = float(E[0, 0, BP.B_[-1]])
        u = U.tutte(E0, MB.G_, sp, om)
        ref = prev[nome]
        diversi = [k for k in ref["uscite"] if u.get(k) != ref["uscite"][k]]
        esito("DEVE PASSARE: U1 %s (eps %g), E0, le bande e le %d uscite = previsioni.json AL BIT" % (nome, eps, len(ref["uscite"])),
              E0 == ref["E0"] and {k: list(v) for k, v in sp.items()} == ref["bande"] and not diversi and set(u) == set(ref["uscite"]),
              "E0 %+.6f; diverse %s" % (E0, diversi))
        mm = U.margine(u, "B")
        esito("DEVE PASSARE: U1 %s, le aperte e il margine = previsioni.json" % nome, U.aperte(u, "B") == ref["aperte"] and [mm[1], mm[0]] == ref["margine"], "%s %.4f" % (mm[1], mm[0]))
        u2 = U.tutte(E0, MB.G_ + 1e-3, sp, om)
        esito("DEVE FALLIRE: U1 %s con g spostato di 1e-3, le uscite = previsioni.json" % nome, not all(u2[k] == ref["uscite"][k] for k in ref["uscite"]), "")
    # ### U2: _chiudere_le_uscite, eps 0, (n2) P0 + Ppi a mu -0.56602
    lib = CU.Libero(0.0)
    sp = U.gruppi_di(lib.E(math.pi, math.pi))
    u = U.uscite(None, 1.0, sp, om, mu=-0.56602)
    v = "%.5f" % u["(n2) P0 + Ppi"]
    rr = _riga_con(os.path.join(RADICE, "doc", "referti_l2", "chiudere_le_uscite.txt"), "(n2) P0 + Ppi a 0.0096 fuori")
    esito("DEVE PASSARE: U2 eps 0, mu -0.56602: (n2) P0 + Ppi = la riga di chiudere_le_uscite.txt", len(rr) == 1 and rr[0].rstrip().endswith(v), v)
    # ### U3: lo spettro DALLA SCENA di r 1.5247 (famiglia sb); il residuo registrato DEVE tornare
    nome, fam, r, g, _da, _t, _tipo = [c for c in SC.CASI if c[0] == "r 1.5247"][0]
    psi, mu, res_reg = SC.stato_di(nome)
    with SC.famiglia(fam, r, g) as (z, phi0):
        sp, res = U.stato_nella_scena(z, phi0, psi, mu, LP.S, LP.FORMA, res_reg)
    f_us = os.path.join(RADICE, "doc", "referti_l2", "scatola", "uscite.txt")
    riga_b = "le bande libere: %s" % "  ".join("%s [%+.5f, %+.5f]" % (k, v_[0], v_[1]) for k, v_ in sp.items())
    riga_r = "%.6e contro %.6e" % (res, res_reg)
    esito("DEVE PASSARE: U3 r 1.5247 dalla scena (famiglia sb): il residuo e le bande libere = le righe di scatola/uscite.txt",
          len(_riga_con(f_us, riga_b)) == 1 and len(_riga_con(f_us, "r 1.5247", riga_r)) == 1, riga_r)
    try:
        with SC.famiglia("lp", r, g) as (z, phi0):
            U.stato_nella_scena(z, phi0, psi, mu, LP.S, LP.FORMA, res_reg)
        rifiutato, nota = False, ""
    except AssertionError as e:
        rifiutato, nota = True, str(e)[:90]
    esito("DEVE FALLIRE: U3 r 1.5247 nella scena della famiglia SBAGLIATA (lp), l'errore di c6ad04ac: stato_nella_scena lo accetta", rifiutato, nota)
