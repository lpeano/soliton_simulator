# -*- coding: utf-8 -*-
"""RUNNER A SIMULATORE ESPLICITO -- importa UNA copia data del simulatore e ne dumpa lo stato.

Serve al sigillo `V1`: per confrontare DUE versioni del simulatore bisogna poterle caricare
entrambe, e `import soliton_simulator` ne carica una sola, quella della radice. Qui il file si
sceglie con `--sim=<path>` e si carica con `importlib`, cosi' il vecchio si estrae da git in un
percorso qualunque e NON si tocca mai il file della radice.

Uso:  python _runner_sim.py --sim=<path> --out=<npz> [--passi=12]
ASCII PURO.
"""
import importlib.util
import os
import sys

import numpy as np

PASSI = 12
MEDIANA = False
SENZA_CHI_BASC = False
SIM = None
OUT = None
for _x in sys.argv[1:]:
    if _x.startswith("--sim="):
        SIM = os.path.abspath(_x.split("=", 1)[1])
    elif _x.startswith("--out="):
        OUT = os.path.abspath(_x.split("=", 1)[1])
    elif _x.startswith("--passi="):
        PASSI = int(_x.split("=", 1)[1])
    elif _x == "--scala-p-mediana":
        MEDIANA = True
    elif _x == "--senza-chi-basc":
        SENZA_CHI_BASC = True
if not SIM or not OUT:
    raise SystemExit("uso: --sim=<path> --out=<npz> [--passi=N]")

# gli STESSI flag del driver, percorso UFFICIALE
sys.argv = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "8",
            "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
            "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
            "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
            "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--plast-din",
            "--viriale", "--olon-part"]

_spec = importlib.util.spec_from_file_location("sim_sotto_esame", SIM)
S = importlib.util.module_from_spec(_spec)
sys.modules["sim_sotto_esame"] = S
_spec.loader.exec_module(S)

a = S._cli()
S._applica_regime(a)
S._applica_flag(a)
if SENZA_CHI_BASC:
    # IL RAMO B DELL'A/B: si spegne `CHI_BASC` DOPO `_applica_flag`, in processo. Non e' una
    # modifica al simulatore: e' una CONFIGURAZIONE diversa dello stesso codice -- il default di
    # modulo e' gia' `False`, ed e' il DRIVER che lo accende con `--chi-basc`.
    S.CHI_BASC = False
if MEDIANA:
    # DIAGNOSTICO: la scala VECCHIA, per la riduzione al limite `Y1`. Non c'e' un flag da riga di
    # comando nel simulatore, di proposito: si accende QUI, in processo, e solo il sigillo lo fa.
    if not hasattr(S, "SCALA_P_MEDIANA"):
        raise SystemExit("questo simulatore non ha SCALA_P_MEDIANA: e' la versione PRIMA della cura")
    S.SCALA_P_MEDIANA = True
S._NMASSE_VIDEO["n"] = 3
S._NMASSE_VIDEO["sep"] = 8.0
S._NMASSE_VIDEO["size"] = None
S.avvia_test("N-MASSE")()

for _ in range(PASSI):
    S.scuoti_vuoto(S.net)
    S.net.step()
    S.net.mitosi()
    S.net.rilassa_disegno()
    S.net.memoria_hebbiana_moto()

np.savez(OUT,
         psi=np.asarray(S.net.psi), d=np.asarray(S.net.d), phi=np.asarray(S.net.phi),
         eta=np.asarray(S.net.eta), n=np.asarray([S.net.n]),
         pos=np.asarray(S.net.pos), tw=np.asarray(S.net.tw),
         omega_s=np.asarray(getattr(S.net, "omega_s", np.zeros((1, 3)))),
         mem_mot=np.asarray(getattr(S.net, "mem_mot", np.zeros((1, 3)))))
# i contatori, se il simulatore li ha (V2): si stampano, cosi' il sigillo li legge dallo stdout
if hasattr(S, "rapporto_guardie"):
    r = S.rapporto_guardie(S.net)
    for k in sorted(r):
        v = r[k]
        print("GUARDIA %-14s tot=%-8d salti=%-8d frazione=%-10.6f shape=%-14s quando=%s"
              % (k, v["tot"], v["salti"], v["frazione"], v["shape"], v["quando"]))
else:
    print("GUARDIE: il simulatore %s NON ha rapporto_guardie (e' la versione PRIMA)" % SIM)
# i DIAGNOSTICI della cura di `scala_p` (Y3, Y4) e il momento angolare netto (Y5).
# L e' definito QUI e la definizione si dichiara: L = somma di (pos - baricentro) x mem_mot,
# cioe' il momento angolare della MEMORIA DEL MOTO -- la grandezza su cui agisce L_CONSERVA.
_P = np.asarray(S.net.pos)[:S.net.n]
_M = np.asarray(getattr(S.net, "mem_mot", np.zeros_like(_P)))[:S.net.n]
_L = np.cross(_P - _P.mean(axis=0), _M).sum(axis=0) if len(_P) == len(_M) else np.zeros(3)
print("DIAG amp_med=%.9f sin2_med=%.9f sin2_p95=%.9f Lx=%.6e Ly=%.6e Lz=%.6e |L|=%.6e"
      % (float(getattr(S.net, "_diag_amp_med", float("nan"))),
         float(getattr(S.net, "_diag_sin2_med", float("nan"))),
         float(getattr(S.net, "_diag_sin2_p95", float("nan"))),
         _L[0], _L[1], _L[2], float(np.linalg.norm(_L))))
_nb = getattr(S.net, "_nb", None)
_nbn = (float(np.abs(np.linalg.norm(np.asarray(_nb)[:S.net.n], axis=1) - 1.0).max())
        if _nb is not None and len(_nb) >= S.net.n else float("nan"))
print("STAB nan_psi=%d nan_d=%d nan_pos=%d max||nb|-1|=%.3e"
      % (int(np.sum(~np.isfinite(S.net.psi))), int(np.sum(~np.isfinite(S.net.d))),
         int(np.sum(~np.isfinite(S.net.pos))), _nbn))
# ---- A/B del SETTORE CHIRALE. Tutte LETTURE, piu' `circolazione_topologica`, che e' dichiarata
# passiva -- ⚠ e la dichiarazione NON e' esatta: scrive `_shat_prec` e `_nhat_prec`. Sono cache
# DIAGNOSTICHE (nessuna legge le rilegge: verificato), ma sono scritture, e il docstring dice
# "non modifica alcuno stato dinamico". Si chiama UNA volta sola, a fine run, in ENTRAMBI i rami.
_pc = np.asarray(S.net.perc_chi)[:S.net.n]
_np1 = int(np.sum(_pc > 0)); _nm1 = int(np.sum(_pc < 0))
print("CHI n=%d Np1=%d Nm1=%d diff=%d nati_mitosi=%d ev_mitosi=%d nati_schw=%d ev_schw=%d"
      % (S.net.n, _np1, _nm1, _np1 - _nm1,
         int(getattr(S.net, "_g_nati_mitosi", 0)), int(getattr(S.net, "_g_nati_mitosi_ev", 0)),
         int(getattr(S.net, "_g_nati_schwinger", 0)), int(getattr(S.net, "_g_nati_schwinger_ev", 0))))
try:
    _c = S.net.circolazione_topologica()
    print("OLON n_cicli=%d olon_media=%.6e olon_media_ass=%.6e olon_rms=%.6e "
          "circ_media=%.6e berry_media=%.6e berry_segno_media=%.6e"
          % (_c["n_cicli"], _c["olonomia_media"], _c["olonomia_media_assoluta"],
             _c["olonomia_rms"], _c["circolazione_media"], _c["berry_spin_media"],
             _c["berry_segno_media"]))
except Exception as _e:
    print("OLON ERRORE: %s" % _e)
_tw = np.abs(np.asarray(S.net.tw))
_twn = np.zeros(S.net.n)
np.add.at(_twn, S.net.i, _tw); np.add.at(_twn, S.net.j, _tw)
_twn = _twn / np.maximum(np.asarray(S.net._deg)[:S.net.n], 1)
_om = np.linalg.norm(np.asarray(S.net.omega_s)[:S.net.n], axis=1)
def _p(a, q):
    return float(np.percentile(a, q)) if len(a) else float("nan")
print("PERC tw50=%.6g tw95=%.6g twn50=%.6g twn95=%.6g om50=%.6g om95=%.6g deg50=%.6g"
      % (_p(_tw, 50), _p(_tw, 95), _p(_twn, 50), _p(_twn, 95), _p(_om, 50), _p(_om, 95),
         _p(np.asarray(S.net._deg)[:S.net.n], 50)))
_dg = S.net.diagnostica()
print("DIAG coer_l=%.6g coer_g=%.6g dil=%.6g" % (_dg["coer_l"], _dg["coer_g"], _dg["dil"]))
print("OK n=%d archi=%d passi=%d" % (S.net.n, len(S.net.i), PASSI))
