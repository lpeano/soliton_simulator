# -*- coding: utf-8 -*-
"""Prova di fumo della scena (ii): geometria, saturazione, coerenza, distanza minima."""
import importlib.util as iu
import sys
import time

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

sp = iu.spec_from_file_location("s", "soliton_simulator.py")
S = iu.module_from_spec(sp)
sp.loader.exec_module(S)
S.SEMINA_LAM = True


def prova(sep, casuali, seme=11):
    S.net = S.Rete(seme)
    S.test["dati"] = {}
    S._NMASSE_VIDEO["sep"] = sep
    S._MC_VIDEO["nodi"] = 0
    S._MC_VIDEO["fasi_casuali"] = casuali
    t0 = time.time()
    S._semina_masse_coerenti()
    dt = time.time() - t0
    co = S.test["dati"]["coorti"]
    D = S._dphi = S.net._dphi()
    print("  tempo %.1f s" % dt)
    for k in range(3):
        ph = S.net.phi[co["massa_%d" % k]]
        z = abs(np.mean(np.exp(1j * ph * 2 * np.pi / D)))
        print("    massa_%d  n=%-5d std(phi) %8.4f   COERENZA CIRCOLARE |<e^iphi>| = %.6f"
              % (k, len(ph), ph.std(), z))
    ph = S.net.phi[co["vuoto"]]
    z = abs(np.mean(np.exp(1j * ph * 2 * np.pi / D)))
    print("    vuoto    n=%-5d std(phi) %8.4f   COERENZA CIRCOLARE           = %.6f"
          "   nullo ~ 1/sqrt(n) = %.4f" % (len(ph), ph.std(), z, 1.0 / np.sqrt(len(ph))))
    # ------------------------------------------------------------------------------------
    # LA COERENZA **FRA** LE REGIONI, e questa misura MANCAVA: era il difetto stesso.
    # ⚠ Rilievo di Luca, 2026-09-25: la prima stesura dava alle tre masse fasi SFASATE DI
    #   120 GRADI (`_dphi()*(k+0.5)/3`), e la prova di fumo **non se ne accorgeva**, perche'
    #   misurava solo la coerenza DENTRO ciascuna regione -- che era perfetta in entrambi i casi.
    #   **Un criterio che non guarda la grandezza di cui si discute non e' un criterio.**
    # IL NULLO SI SA IN ANTICIPO: tre gruppi uguali a 120 gradi si CANCELLANO, quindi la
    #   versione sfasata darebbe **~0**; la versione a fase unica da' **quanto ciascuna regione**.
    un = np.concatenate([co["massa_%d" % k] for k in range(3)])
    zu = abs(np.mean(np.exp(1j * S.net.phi[un] * 2 * np.pi / D)))
    # e le tre fasi MEDIE, in gradi sul campo (che vede `phi` su 2 pi)
    med = [np.angle(np.mean(np.exp(1j * S.net.phi[co["massa_%d" % k]] * 2 * np.pi / D)),
                    deg=True) % 360.0 for k in range(3)]
    # ATTENZIONE ALLA CONVENZIONE, senno' il numero si legge male: queste fasi sono
    #   NORMALIZZATE AL PERIODO DI `phi` (4 pi), perche' e' cosi' che si misura la coerenza
    #   di una variabile a 4 pi. **IL CAMPO USA `exp(1j*phi)` DIRETTAMENTE** (`:3635`), quindi
    #   `phi = _dphi()/2 = 2 pi` da' `exp(i 2 pi) = 1`, cioe' **FASE ZERO ESATTA NEL CAMPO**.
    #   I `180` gradi qui sotto sono la coordinata su 4 pi, NON la fase del campo.
    campo = [np.angle(np.mean(np.exp(1j * S.net.phi[co["massa_%d" % k]])), deg=True) % 360.0
             for k in range(3)]
    print("    FRA LE REGIONI (unione)  |<e^iphi>| = %.6f    fasi medie normalizzate a 4pi = "
          "%.2f / %.2f / %.2f gradi" % (zu, med[0], med[1], med[2]))
    # l'etichetta NON si scrive fissa: nel braccio a fasi casuali "fase ZERO" sarebbe FALSO,
    # e un'etichetta sbagliata su un numero giusto e' peggio di nessuna etichetta.
    _et = ("-> FASE ZERO, e la STESSA per tutte e tre"
           if max(min(abs(c), abs(360.0 - c)) for c in campo) < 1.0
           else "-> NON e' fase zero (atteso: braccio a fasi casuali)")
    print("       NEL CAMPO (exp(1j*phi), :3635): %.3f / %.3f / %.3f gradi  %s"
          % (campo[0], campo[1], campo[2], _et))
    print("       sfasamenti: %.2f e %.2f gradi   -> ATTESO 0 e 0 (stessa fase per tutte);"
          " la versione SFASATA dava 120 e 240, e |<e^iphi>| ~ 0"
          % ((med[1] - med[0]) % 360.0, (med[2] - med[0]) % 360.0))
    if not casuali and zu < 0.9:
        print("       !! LE TRE MASSE NON HANNO LA STESSA FASE: interferenza messa dalla"
              " CONDIZIONE INIZIALE, non dalla dinamica.")
    from scipy.spatial import cKDTree
    dd = cKDTree(S.net.pos).query(S.net.pos, k=2)[0][:, 1]
    print("    min distanza fra nodi = %.9f   LAM = %.9f   archi = %d"
          % (dd.min(), S.LAM, len(S.net.d)))
    return S.test["dati"]["scena_ii"]


print("=" * 96)
print("SCENA (b)  --sep 4.0   fasi COERENTI")
d = prova(4.0, False)
print("   ", {k: (round(v, 6) if isinstance(v, float) else v) for k, v in sorted(d.items())})
print()
print("SCENA (b)  --sep 4.0   fasi CASUALI  (braccio di controllo di S10)")
prova(4.0, True)
print()
print("SCENA (a)  --sep 6.1158   fasi COERENTI")
d = prova(6.1158, False)
print("   ", {k: (round(v, 6) if isinstance(v, float) else v) for k, v in sorted(d.items())})
