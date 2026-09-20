# -*- coding: utf-8 -*-
"""M1-M4 -- le misure che vengono PRIMA della cura di `scala_p`.

Letture FISSATE PRIMA: doc/TASK_HISTORY/2026-09-20_scala-p-punto-fisso.md (f90fc1b).
NESSUN RUN: `dpozzo` e `phi_g` si ricalcolano da `pozzo_grafo`, che e' una lettura pura, e `tw` e'
negli snapshot.

  M1  |dpozzo| percentili e TRAIETTORIA          -> l'ordine di grandezza di cio' che si normalizza
  M2  phi_g percentili e QUANTO E' VICINO A ZERO -> e' il candidato DENOMINATORE. Se si annulla,
      servirebbe un pavimento, cioe' un NUMERO, e A1 lo vieta: QUESTA MISURA PUO' FAR CADERE LA CURA
  M3  median(ampiezza) vale davvero tanh(1) = 0.761594?  -> si VERIFICA il punto fisso, non si deduce
  M4  sin2 percentili: e' incollato? -> e' la firma che il punto fisso MORDE

M3 E' UN CONTROLLO SU ME STESSO: ho dedotto il punto fisso dall'ALGEBRA, e l'algebra letta e non
misurata mi ha gia' ingannato oggi (l'anomalia (1) del mandato precedente diceva che `ampiezza` non
fosse limitata, ed era falso dal codice). Se M3 non da' 0.761594 mi fermo e riporto.

COSA E' CHIAMATO E COSA E' REPLICATO, dichiarato:
  - `pozzo_grafo` e' CHIAMATO (e' un metodo, e va usato quello vero);
  - il blocco di `sin2` e' REPLICATO, perche' e' INLINE dentro `memoria_hebbiana_moto` e non esiste
    una funzione da chiamare. La replica segue riga per riga :4418-4432 e legge i flag dal MODULO.

IL BLOB: gli snapshot sono di `7c4dec1d`, il codice e' un altro -> override DICHIARATO, la logica di
`carica_stato` meno la verifica del blob, cache derivate invalidate.
ASCII PURO.
"""
import glob
import gzip
import os
import pickle
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
ARCHIVIO = os.path.join(RADICE, "csv", "_test_fork", "_g6000")
PILOTA = os.path.join(RADICE, "csv", "_test_fork", "_pilota_sep_4p0")

sys.argv = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "8",
            "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
            "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
            "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
            "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--plast-din",
            "--viriale", "--olon-part"]
sys.path.insert(0, RADICE)
os.chdir(RADICE)
import soliton_simulator as S

_a = S._cli()
S._applica_regime(_a)
S._applica_flag(_a)

TANH1 = float(np.tanh(1.0))


def carica(path):
    ap = gzip.open if str(path).endswith(".gz") else open
    with ap(path, "rb") as f:
        st = pickle.load(f)
    for k, v in st["attrs"].items():
        setattr(S.net, k, v)
    S.net.rng.bit_generator.state = st["rng_state"]
    S.net._S = None
    if hasattr(S.net, "_perm"):
        S.net._perm = None
    if hasattr(S.net, "_ker_cache"):
        S.net._ker_cache = {}


def q(a, p):
    a = np.asarray(a)
    a = a[np.isfinite(a)]
    return float(np.percentile(a, p)) if a.size else float("nan")


def misura():
    """Riproduce il calcolo di `memoria_hebbiana_moto` fino a `sin2`, e basta."""
    n = int(S.net.n)
    if not hasattr(S.net, "psi") or len(S.net.psi) < n:
        S.net.calcola_psi()
    I = np.abs(S.net.psi[:n]) ** 2
    mask = (S.net.i < n) & (S.net.j < n)
    ii, jj = S.net.i[mask], S.net.j[mask]
    phi_g, _m, dpozzo = S.net.pozzo_grafo(I)          # IL metodo, non una replica

    ad = np.abs(dpozzo)
    scala_p = max(float(np.median(ad)), 1e-9) if len(dpozzo) else 1e-9
    ampiezza = np.tanh(ad / scala_p)

    # --- REPLICA di :4418-4432 (il blocco e' INLINE: non c'e' una funzione da chiamare)
    twn_a = S.net.tw[mask] / S.PHI_CRIT
    circ_nodo = np.zeros(n)
    grado_c = np.zeros(n)
    np.add.at(circ_nodo, ii, twn_a)
    np.add.at(circ_nodo, jj, -twn_a)
    np.add.at(grado_c, ii, 1.0)
    np.add.at(grado_c, jj, 1.0)
    circ_nodo = circ_nodo / np.maximum(grado_c, 1.0)
    circ_arc = 0.5 * (circ_nodo[ii] + circ_nodo[jj])
    r_rad = ampiezza
    if S.OLON_PART:
        t_tan = np.tanh(np.hypot(np.abs(circ_arc), np.abs(twn_a)))
    else:
        t_tan = np.tanh(np.abs(circ_arc))
    H = np.maximum(np.hypot(r_rad, t_tan), 1e-9)
    cos2 = (r_rad / H) ** 2
    sin2 = (t_tan / H) ** 2

    # --- il candidato DENOMINATORE della cura: il pozzo medio d'ARCO
    phi_arc = 0.5 * (phi_g[ii] + phi_g[jj])
    return dict(n=n, narchi=int(mask.sum()), phi_g=phi_g[:n], phi_arc=phi_arc,
                ad=ad, scala_p=scala_p, ampiezza=ampiezza, sin2=sin2, cos2=cos2,
                t_tan=t_tan)


def nuovo_med(m):
    """median(tanh(|dpozzo| / phi_arc)) -- quello che la CURA produrrebbe.
    Se anche questo fosse costante nel tempo, avrei solo SPOSTATO il punto fisso, non sciolto."""
    r = m["ad"] / np.maximum(m["phi_arc"], 1e-300)
    return float(np.median(np.tanh(r))), float(np.min(m["phi_arc"]))


def riga(et, m):
    nm, pmin = nuovo_med(m)
    print("%-10s | %-10.4g %-10.4g %-10.4g | %-11.6g %-9.6f | %-9.4g %-9.4g | %-9.6f %-10.4g"
          % (et, q(m["ad"], 5), q(m["ad"], 50), q(m["ad"], 95),
             m["scala_p"], float(np.median(m["ampiezza"])),
             q(m["sin2"], 50), q(m["sin2"], 95), nm, pmin))


def main():
    fs = sorted(glob.glob(os.path.join(ARCHIVIO, "scena_??????.pkl*")))
    pil = sorted(glob.glob(os.path.join(PILOTA, "pilota_??????.pkl*")))
    if not fs:
        print("nessuno snapshot in %s" % ARCHIVIO)
        return 1
    print("OLON_PART = %s   PHI_CRIT = %.6f   tanh(1) = %.6f" % (S.OLON_PART, S.PHI_CRIT, TANH1))
    print("")
    print("=" * 126)
    print("M1 / M3 / M4 -- |dpozzo|, il PUNTO FISSO di median(ampiezza), e sin2")
    print("=" * 126)
    print("%-10s | %-10s %-10s %-10s | %-11s %-9s | %-9s %-9s | %-9s %-10s"
          % ("passo", "|dp| p05", "|dp| p50", "|dp| p95", "scala_p", "med(amp)",
             "sin2 p50", "sin2 p95", "NUOVO med", "min phi_arc"))
    nuovi = []
    scarti = []
    ultimo = None
    for p in fs[::4] + [fs[-1]]:
        passo = int(re.search(r"_(\d{6})\.", p).group(1))
        carica(p)
        m = misura()
        riga("passo %d" % passo, m)
        nuovi.append(nuovo_med(m)[0])
        scarti.append(abs(float(np.median(m["ampiezza"])) - TANH1))
        ultimo = m
    for p in pil:
        passo = int(re.search(r"_(\d{6})\.", p).group(1))
        carica(p)
        m = misura()
        riga("PIL %d" % passo, m)
        nuovi.append(nuovo_med(m)[0])
        scarti.append(abs(float(np.median(m["ampiezza"])) - TANH1))
        ultimo = m
    print("")
    print("  M3 -- scarto |median(ampiezza) - tanh(1)|:  max %.3e   su %d istanti"
          % (max(scarti), len(scarti)))
    if max(scarti) < 1e-9:
        print("     -> IL PUNTO FISSO C'E', ESATTO. median(ampiezza) = tanh(1) a ogni istante.")
    elif max(scarti) < 1e-3:
        print("     -> il punto fisso c'e' ma NON e' esatto (mediana su campione pari: media dei due")
        print("        centrali). Resta un ancoraggio, e va detto cosi'.")
    else:
        print("     *** IL PUNTO FISSO NON C'E': la mia algebra e' SBAGLIATA. Mi fermo e riporto. ***")

    print("")
    print("  Y3 IN ANTICIPO -- il NUOVO median(tanh(|dp|/phi_arc)) SI MUOVE nel tempo?")
    print("     valori: %s" % "  ".join("%.4f" % x for x in nuovi))
    print("     min %.6f   max %.6f   escursione %.4f   (il VECCHIO e' 0.761594 FISSO)"
          % (min(nuovi), max(nuovi), max(nuovi) - min(nuovi)))
    if max(nuovi) - min(nuovi) < 1e-6:
        print("     *** E' ANCORA UN PUNTO FISSO, solo a un altro valore: la cura NON scioglie. ***")
    else:
        print("     -> SI MUOVE: non e' un punto fisso. La cura fa quello che deve.")

    # ---------------------------------------------------------------- M2, la misura che decide
    print("")
    print("=" * 126)
    print("M2 -- phi_g: IL CANDIDATO DENOMINATORE. Si annulla?")
    print("=" * 126)
    for et, arr in (("phi_g  per NODO", ultimo["phi_g"]),
                    ("phi_arc per ARCO", ultimo["phi_arc"])):
        a = np.asarray(arr, float)
        print("  %-18s n=%-8d  min %.6g   p01 %.6g   p05 %.6g   p50 %.6g   max %.6g"
              % (et, a.size, float(a.min()), q(a, 1), q(a, 5), q(a, 50), float(a.max())))
        for s in (0.0, 1e-12, 1e-9, 1e-6):
            k = int(np.sum(a <= s))
            print("       <= %-8.0e : %-8d (%.4f %%)" % (s, k, 100.0 * k / max(a.size, 1)))
        # e il rapporto che la cura userebbe
    print("")
    rap = ultimo["ad"] / np.maximum(ultimo["phi_arc"], 1e-300)
    print("  IL RAPPORTO DELLA CURA  |dpozzo| / phi_arc:")
    print("     p01 %.4g   p05 %.4g   p50 %.4g   p95 %.4g   p99 %.4g   max %.4g   non-finiti %d"
          % (q(rap, 1), q(rap, 5), q(rap, 50), q(rap, 95), q(rap, 99),
             float(np.nanmax(rap)), int(np.sum(~np.isfinite(rap)))))
    nuovo = np.tanh(rap)
    print("     -> median(tanh(rapporto)) = %.6f    (il vecchio e' %.6f, e NON si muove mai)"
          % (float(np.median(nuovo)), TANH1))
    print("")
    print("UN SEME, UNA SCENA. Il pilota e' a sep=4.0, l'archivio a sep=8.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
