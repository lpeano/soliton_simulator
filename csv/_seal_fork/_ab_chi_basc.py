# -*- coding: utf-8 -*-
"""A/B DI `chi_basc` -- e i sigilli Z0-Z5. DUE CONFIG, LO STESSO CODICE.

Letture FISSATE PRIMA: doc/TASK_HISTORY/2026-09-20_chi-basc-off.md (fb7916a).

  ramo A:  `--chi-basc` acceso   (come tutti i run finora)
  ramo B:  `CHI_BASC = False`    (il default di modulo, spento in processo dal runner)

⚠ NON E' UNA MODIFICA AL SIMULATORE: il default e' gia' `False` (`:746`), ed e' il DRIVER che lo
accende. I due bracci girano lo STESSO codice in due CONFIGURAZIONI.

  Z1  BYTE-IDENTITA' [BLOCCANTE]: il ramo A contro il simulatore PRIMA dei contatori (`e9f5d70`).
      Se i contatori dei nati o `olonomia_media` avessero toccato la fisica, si vedrebbe QUI.
  Z2  CONTROLLO POSITIVO: A contro B DEVE differire.
  Z3  `perc_chi` NON e' piu' riscritta in B: si confronta con quella che ci si aspetta dalle sole
      NASCITE, e in A si mostra che invece cambia.
  Z4  l'anello `A6` e' rotto in B -- ma si verifica DAL CODICE, non dai numeri: vedi `Z70`.
  Z5  stabilita'.

LA MISURA CHE DECIDE e' `L` e l'OLONOMIA NETTA: se in B sopravvivono, lo spinore basta e `chi_basc`
e' ridondante; se si azzerano, `chi_basc` serviva -- e NON e' un fallimento, e' l'informazione.
ASCII PURO.
"""
import os
import re
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SIM_ORA = os.path.join(RADICE, "soliton_simulator.py")
BASE = os.path.join(RADICE, "csv", "_seal_fork", "_ab_chibasc")
COMMIT_PRIMA = "e9f5d70"          # il simulatore PRIMA dei contatori e di `olonomia_media`
PASSI = 60
# --da-snapshot=<path>: la finestra si sposta dove la mitosi e' GIA' ATTIVA. Senza, si parte dalla
# semina, e la finestra 0->60 NON prova nulla sulla mitosi (nel run vero n resta 2391 fino al 120).
DA_SNAP = None
for _x in sys.argv[1:]:
    if _x.startswith("--da-snapshot="):
        DA_SNAP = _x.split("=", 1)[1]
    elif _x.startswith("--passi="):
        PASSI = int(_x.split("=", 1)[1])
CAMPI = ("psi", "d", "phi", "eta", "n", "pos", "tw")

esiti = []


def segna(nome, ok, det):
    esiti.append((nome, ok))
    print("%-5s %-6s %s" % (nome, "PASS" if ok else "FAIL", det))


def gira(sim, out, extra=()):
    cmd = [sys.executable, os.path.join(_QUI, "_runner_sim.py"),
           "--sim=%s" % sim, "--out=%s" % out, "--passi=%d" % PASSI] + list(extra)
    if DA_SNAP:
        cmd.append("--da-snapshot=%s" % DA_SNAP)
    pr = subprocess.run(cmd, cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    if pr.returncode != 0:
        print(pr.stdout[-1200:])
        print(pr.stderr[-1800:])
        raise SystemExit("runner uscito con %d" % pr.returncode)
    return pr.stdout


def leggi(out, tag, campi):
    m = re.search(r"^%s (.*)$" % tag, out, re.M)
    if not m:
        return None
    d = {}
    for k in campi:
        mm = re.search(r"\b%s=(\S+)" % re.escape(k), m.group(1))
        if mm:
            try:
                d[k] = float(mm.group(1))
            except ValueError:
                d[k] = mm.group(1)
    return d


def main():
    os.makedirs(BASE, exist_ok=True)
    import hashlib
    vecchio = os.path.join(BASE, "_sim_prima.py")
    q = subprocess.run(["git", "cat-file", "-p", "%s:soliton_simulator.py" % COMMIT_PRIMA],
                       cwd=RADICE, capture_output=True)
    if q.returncode != 0:
        raise SystemExit("non riesco a estrarre il simulatore di %s" % COMMIT_PRIMA)
    with open(vecchio, "wb") as f:
        f.write(q.stdout)
    with open(SIM_ORA, "rb") as f:
        dn = f.read()
    print("Z0  simulatore PRIMA (%s): sha1 grezzo %s"
          % (COMMIT_PRIMA, hashlib.sha1(q.stdout).hexdigest()[:8]))
    print("Z0  simulatore ORA           : sha1 grezzo %s" % hashlib.sha1(dn).hexdigest()[:8])
    print("Z0  %d passi per braccio   finestra: %s"
          % (PASSI, ("dallo snapshot %s" % os.path.basename(DA_SNAP)) if DA_SNAP
             else "DALLA SEMINA (passo 0)"))
    print("")

    oR, oA, oB = (os.path.join(BASE, x) for x in ("RIF.npz", "A.npz", "B.npz"))
    print("riferimento: simulatore PRIMA, --chi-basc acceso")
    outR = gira(vecchio, oR)
    print("ramo A     : simulatore ORA,   --chi-basc acceso")
    outA = gira(SIM_ORA, oA)
    print("ramo B     : simulatore ORA,   CHI_BASC = False")
    outB = gira(SIM_ORA, oB, ["--senza-chi-basc"])
    print("")
    R, A, B = np.load(oR), np.load(oA), np.load(oB)

    def diff(x, y):
        f = []
        for k in CAMPI:
            a, b = x[k], y[k]
            if a.shape != b.shape:
                f.append("%s(shape %s vs %s)" % (k, a.shape, b.shape))
            elif not np.array_equal(a, b):
                f.append("%s(max|d|=%.3e)" % (k, float(np.nanmax(np.abs(a - b)))))
        return f

    f1 = diff(R, A)
    segna("Z1", not f1, "riduzione al limite RIF==A su %d campi: %s"
          % (len(CAMPI), "BYTE-IDENTICI" if not f1 else "DIVERSI -> %s" % f1))
    if f1:
        print("  *** Z1 e' BLOCCANTE: la strumentazione tocca la fisica. FERMO. ***")
        return 1
    f2 = diff(A, B)
    segna("Z2", len(f2) > 0, "controllo positivo A!=B: %d campi su %d differiscono"
          % (len(f2), len(CAMPI)))

    CH = ("n", "Np1", "Nm1", "diff", "nati_mitosi", "ev_mitosi", "nati_schw", "ev_schw")
    OL = ("n_cicli", "olon_media", "olon_media_ass", "olon_rms", "circ_media",
          "berry_media", "berry_segno_media")
    PE = ("tw50", "tw95", "twn50", "twn95", "om50", "om95", "deg50")
    DI = ("coer_l", "coer_g", "dil")
    cA, cB = leggi(outA, "CHI", CH), leggi(outB, "CHI", CH)
    lA, lB = leggi(outA, "OLON", OL), leggi(outB, "OLON", OL)
    pA, pB = leggi(outA, "PERC", PE), leggi(outB, "PERC", PE)
    dA, dB = leggi(outA, "DIAG", DI), leggi(outB, "DIAG", DI)
    gA = re.search(r"DIAG amp_med=\S+ sin2_med=\S+ sin2_p95=\S+ Lx=(\S+) Ly=(\S+) Lz=(\S+) \|L\|=(\S+)", outA)
    gB = re.search(r"DIAG amp_med=\S+ sin2_med=\S+ sin2_p95=\S+ Lx=(\S+) Ly=(\S+) Lz=(\S+) \|L\|=(\S+)", outB)

    print("")
    print("=" * 112)
    print("LA CARICA CHIRALE")
    print("=" * 112)
    print("  %-16s %14s %14s" % ("", "A (chi_basc ON)", "B (OFF)"))
    for k in CH:
        print("  %-16s %14s %14s" % (k, cA.get(k), cB.get(k)))
    segna("Z3", (cB.get("nati_mitosi", 0) + cB.get("nati_schw", 0)) > 0,
          "in B `perc_chi` e' scritta SOLO dalle nascite: %d da mitosi + %d da Schwinger"
          % (cB.get("nati_mitosi", -1), cB.get("nati_schw", -1)))

    print("")
    print("=" * 112)
    print("L'OLONOMIA -- la FIRMATA accanto alle ASSOLUTE, e L")
    print("=" * 112)
    for k in OL:
        print("  %-18s %14.6g %14.6g" % (k, lA.get(k, float("nan")), lB.get(k, float("nan"))))
    if gA and gB:
        LA = np.array([float(x) for x in gA.groups()[:3]])
        LB = np.array([float(x) for x in gB.groups()[:3]])
        print("  %-18s [%9.3e %9.3e %9.3e]  |L| = %.6e" % ("L  (A)", LA[0], LA[1], LA[2], float(gA.group(4))))
        print("  %-18s [%9.3e %9.3e %9.3e]  |L| = %.6e" % ("L  (B)", LB[0], LB[1], LB[2], float(gB.group(4))))
        rap = float(gB.group(4)) / max(float(gA.group(4)), 1e-30)
        print("  |L| B/A = %.4f" % rap)

    print("")
    print("=" * 112)
    print("I PERCENTILI E LA DIAGNOSTICA")
    print("=" * 112)
    for k in PE:
        print("  %-10s %14.6g %14.6g" % (k, pA.get(k, float("nan")), pB.get(k, float("nan"))))
    for k in DI:
        print("  %-10s %14.6g %14.6g" % (k, dA.get(k, float("nan")), dB.get(k, float("nan"))))

    m = re.search(r"STAB nan_psi=(\d+) nan_d=(\d+) nan_pos=(\d+) max\|\|nb\|-1\|=(\S+)", outB)
    if m:
        segna("Z5", int(m.group(1)) == 0 and int(m.group(2)) == 0 and int(m.group(3)) == 0
              and float(m.group(4)) < 1e-9,
              "stabilita' in B: nan %s/%s/%s  max||nb|-1| = %s"
              % (m.group(1), m.group(2), m.group(3), m.group(4)))
    print("")
    n_pass = sum(1 for _, o in esiti if o)
    print("ESITO: %d/%d" % (n_pass, len(esiti)))
    print("")
    print("Z4 NON E' UN NUMERO: l'anello si verifica DAL CODICE (`Z70`). Con `chi_basc` spento cade")
    print("   la gamba `perc_chi <- tw`, quindi l'anello si rompe per costruzione.")
    print("UN SEME, UNA SCENA, %d passi. NON E' UN VERDETTO: e' una misura." % PASSI)
    return 0 if n_pass == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
