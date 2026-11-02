# -*- coding: utf-8 -*-
r"""**I TEST DELLE MAPPE** *(il task history `2026-11-02_accensione_lenta`, sez. `12`)*: ### **il disco, un'istantanea della scena scritta e riletta, l'indice.**
### ⚠ **Scrivono su `E:`** *(`mappe.RADICE`, la cartella `_prova`)*: ### **la cassetta dipende dal disco esterno** *(dichiarato)*."""
import hashlib
import os

import numpy as np

from . import mappe as MP

TOLL = 1e-6                    # ### Luca 15:49: sum rho = M e sum Lambda = V entro 1e-6 relativo (float32)
QUANTE = 1067                  # ### la stima del task history: le istantanee fino a 16000, ogni 100 tick


def gira(esito):
    import _energia_del_legame as EL
    import _vuoto_vivo_B as V
    print("### LE MAPPE (csv/solitone/mappe.py): RADICE %s OGNI %d VOLTE_SPAZIO %d; TOLL %g QUANTE %d" % (MP.RADICE, MP.OGNI, MP.VOLTE_SPAZIO, TOLL, QUANTE))
    sol, vuoto, s = V.CORSE["BG-F-0.15"]
    with V.scena(s, vuoto, V.EPS) as (_rec, z, phi0, pK):
        p0, _info = V.partenza(sol, z, phi0, pK, s)
        z["st"]["psi_h"][...] = p0
        n = z["inc"].n
        st = MP.stima(n, QUANTE)
        ok, libero, nota = MP.controlla_disco(MP.RADICE, st)
        esito("DEVE PASSARE: K1 il disco %s esiste, e' scrivibile, e ha almeno %d volte la stima (%d istantanee, %d byte)" % (MP.RADICE, MP.VOLTE_SPAZIO, QUANTE, st), ok, nota)
        ok_f, _l, nota_f = MP.controlla_disco(MP.RADICE, libero // MP.VOLTE_SPAZIO + 1)
        esito("DEVE FALLIRE: K1-F il disco basta per una stima di %d volte meno lo spazio libero piu' 1 byte" % MP.VOLTE_SPAZIO, not ok_f, nota_f)
        prima = V.shas(z)
        ist = MP.istantanea(z, 0, 0.0, (0.0, 0.0))
        dopo = V.shas(z)
        rho, la = EL.densita(z["inc"], z["st"])
        M, Vv = float(rho.sum()), float(la.sum())
        f = os.path.join(MP.RADICE, "_prova", "_prova_000000.npz")
        dim, sha = MP.scrivi(f, [ist, ist], np.asarray(z["m1"]), np.asarray(z["m2"]), z["L"])
        d = MP.leggi(f)
    esito("DEVE PASSARE: K0 l'istantanea non tocca lo stato (gli sha di ogni chiave prima e dopo)", prima == dopo, "")
    eM = abs(float(d["rho"][1].astype(np.float64).sum()) / M - 1.0)
    eV = abs(float(d["Lambda"][1].astype(np.float64).sum()) / Vv - 1.0)
    esito("DEVE PASSARE: K2 riletta, sum rho = M e sum Lambda = V entro %g relativo (float32)" % TOLL, eM <= TOLL and eV <= TOLL,
          "M %.6f errore %.2e; V %.6f errore %.2e; il file %d byte" % (M, eM, Vv, eV, dim))
    r2 = d["rho"][1].astype(np.float64)
    r2[int(np.argmax(r2))] *= 2.0
    eF = abs(float(r2.sum()) / M - 1.0)
    esito("DEVE FALLIRE: K2-F con il nodo piu' denso raddoppiato, sum rho = M entro %g" % TOLL, not eF <= TOLL, "errore %.2e" % eF)
    with open(f, "rb") as fh:
        b = fh.read()
    riga = MP.riga_indice(f, s)
    esito("DEVE PASSARE: K3 la riga dell'indice ha la dimensione e lo sha1 del file (hashlib sui byte letti a parte)",
          ("%d byte" % len(b)) in riga and hashlib.sha1(b).hexdigest() in riga and sha == hashlib.sha1(b).hexdigest(), riga)
    os.remove(f)
