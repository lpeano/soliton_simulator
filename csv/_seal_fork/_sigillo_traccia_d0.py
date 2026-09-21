# -*- coding: utf-8 -*-
"""SIGILLO DI `TRACCIA_D0` -- la strumentazione dei DICIANNOVE punti che toccano `d0`.

Criteri fissati PRIMA in `doc/TASK_HISTORY/2026-09-20_strumentare-d0.md` (`1e6448a`).

  Z0  i due blob, in BYTE GREZZI (`sha1`), **mai** `git hash-object` (C18: sono due numeri diversi).
  Z1  [BLOCCANTE] `TRACCIA_D0 = False` -> stato BYTE-IDENTICO al simulatore PRIMA della patch.
      **Una sola divergenza = STOP.** La strumentazione non deve cambiare un bit.
  Z2  CONTROLLO POSITIVO: a `True` la traccia PRODUCE numeri, e non banali (non tutti zero, e
      almeno due siti distinti devono aver toccato `d0`). **Un sigillo di sola byte-identita'
      passerebbe anche su codice morto** (par.10.2).
  Z2b ⚠ E LA TRACCIA NON DEVE FINIRE NELLO SNAPSHOT: `_traccia_d0_log` e' una `list` e
      `_g_traccia_d0` un `dict`, e il filtro di `salva_stato` accetta solo ndarray/scalari/str.
      Si VERIFICA invece di dedurlo dal tipo.
  Z3  [BLOCCANTE] la RIGIOCATA resta fedele -> e' il sigillo interno di `_rigiocata_0_120.py`
      (che passo' `138/138`), e si gira A PARTE col flag ACCESO: se la strumentazione avesse
      toccato il percorso, li' si vedrebbe.

⚠ IL SIMULATORE PRIMA si estrae con `git cat-file -p` IN BINARIO, mai con `git checkout`
  (par.5-quinquies, la trappola CRLF).
ASCII PURO.
"""
import hashlib
import os
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SIM_ORA = os.path.join(RADICE, "soliton_simulator.py")
COMMIT_PRIMA = "77ed65c"        # l ultimo commit PRIMA della strumentazione TRACCIA_VD
PASSI = 30
CAMPI = ("d0", "d", "vd", "psi", "phi", "eta", "perc_chi", "tw", "omega_s", "pos")

esiti = []


def segna(nome, ok, det):
    esiti.append((nome, ok))
    print("%-5s %-6s %s" % (nome, "PASS" if ok else "FAIL", det))


# ----------------------------------------------------------------- il lavoratore
if "--lavoro" in sys.argv:
    simp = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--sim=")][0]
    outp = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--out=")][0]
    trac = "--traccia" in sys.argv
    os.chdir(RADICE)
    sys.argv = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
                "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
                "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
                "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
                "--pav-com", "--guscio-morbido", "--zeta-vir", "--plast-din",
                "--viriale", "--olon-part"]
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("_sim_x", simp)
    S = _iu.module_from_spec(_sp)
    sys.modules["_sim_x"] = S
    _sp.loader.exec_module(S)
    if trac:
        if not hasattr(S, "TRACCIA_D0"):
            raise SystemExit("questo simulatore non ha TRACCIA_D0")
        S.TRACCIA_D0 = True
    a = S._cli(); S._applica_regime(a); S._applica_flag(a)
    S._NMASSE_VIDEO["n"] = 3; S._NMASSE_VIDEO["sep"] = 4.0; S._NMASSE_VIDEO["size"] = None
    S.avvia_test("N-MASSE")()
    net = S.net
    S.stato["nframe"] = 0
    for _f in range(PASSI // int(S.PASSI_PER_FRAME)):
        S.passo_test()
        for _ in range(int(S.PASSI_PER_FRAME)):
            S.scuoti_vuoto(net); net.step(); net.mitosi()
            net.rilassa_disegno(); net.memoria_hebbiana_moto()
    d = {k: np.asarray(getattr(net, k)) for k in CAMPI if hasattr(net, k)}
    np.savez(outp, **d)
    log = getattr(net, "_traccia_d0_log", [])
    glob = getattr(net, "_g_traccia_d0", {})
    print("TRACCIA voci=%d siti=%d" % (len(log), len(glob)))
    for k in sorted(glob):
        print("SITO %-20s %d" % (k, glob[k]))
    somme = {}
    for v in log:
        somme[v["sito"]] = somme.get(v["sito"], 0.0) + (v.get("somma", 0.0) or 0.0)
    for k in sorted(somme):
        print("SOMMA %-20s %.6e" % (k, somme[k]))
    # Z2b: cio' che `salva_stato` salverebbe davvero
    import numpy as _np
    salvati = [k for k, v in net.__dict__.items()
               if isinstance(v, (_np.ndarray, int, float, bool, _np.integer, _np.floating, str))]
    print("SNAPSHOT traccia_nel_filtro=%d"
          % sum(1 for k in salvati if "traccia" in k.lower()))
    raise SystemExit(0)


def gira(sim, out, traccia=False):
    cmd = [sys.executable, os.path.abspath(__file__), "--lavoro", "--sim=%s" % sim, "--out=%s" % out]
    if traccia:
        cmd.append("--traccia")
    pr = subprocess.run(cmd, cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    if pr.returncode != 0:
        print(pr.stdout[-1500:]); print(pr.stderr[-2000:])
        raise SystemExit("lavoratore uscito con %d" % pr.returncode)
    return pr.stdout


def main():
    base = os.path.join(RADICE, "csv", "_seal_fork", "_sig_traccia_d0")
    os.makedirs(base, exist_ok=True)
    vecchio = os.path.join(base, "_sim_prima.py")
    q = subprocess.run(["git", "cat-file", "-p", "%s:soliton_simulator.py" % COMMIT_PRIMA],
                       cwd=RADICE, capture_output=True)
    if q.returncode != 0:
        raise SystemExit("non riesco a estrarre il simulatore di %s" % COMMIT_PRIMA)
    with open(vecchio, "wb") as f:      # BINARIO: niente riscrittura delle newline
        f.write(q.stdout)
    with open(SIM_ORA, "rb") as f:
        dn = f.read()
    print("Z0  simulatore PRIMA (%s): sha1 GREZZO %s"
          % (COMMIT_PRIMA, hashlib.sha1(q.stdout).hexdigest()[:8]))
    print("Z0  simulatore ORA            : sha1 GREZZO %s" % hashlib.sha1(dn).hexdigest()[:8])
    print("Z0  (NB: NON e' `git hash-object`. Sono due numeri diversi per lo stesso file, C18.)")
    print("")

    oA = os.path.join(base, "A_prima.npz")
    oB = os.path.join(base, "B_ora_off.npz")
    oC = os.path.join(base, "C_ora_on.npz")
    print("braccio A: simulatore PRIMA della patch")
    gira(vecchio, oA)
    print("braccio B: simulatore ORA, TRACCIA_D0 = False")
    gira(SIM_ORA, oB)
    print("braccio C: simulatore ORA, TRACCIA_D0 = True")
    outC = gira(SIM_ORA, oC, traccia=True)
    print("")

    A, B = np.load(oA), np.load(oB)
    def diff(x, y):
        f = []
        for k in CAMPI:
            if k not in x or k not in y:
                f.append("%s(assente)" % k); continue
            a, b = x[k], y[k]
            if a.shape != b.shape:
                f.append("%s(shape %s vs %s)" % (k, a.shape, b.shape))
            elif not np.array_equal(a, b):
                f.append("%s(max|d|=%.3e)" % (k, float(np.nanmax(np.abs(a - b)))))
        return f
    f1 = diff(A, B)
    segna("Z1", not f1, "a flag SPENTO: %d campi su %d -> %s"
          % (len(CAMPI), len(CAMPI), "BYTE-IDENTICI" if not f1 else "DIVERSI: %s" % f1[:6]))
    if f1:
        print("  *** Z1 e' BLOCCANTE: la strumentazione TOCCA la fisica. FERMO. ***")
        return 1

    C = np.load(oC)
    f2 = diff(A, C)
    segna("Z1b", not f2, "a flag ACCESO la FISICA non cambia: %s"
          % ("identica" if not f2 else "DIVERSA: %s" % f2[:6]))

    import re
    voci = re.search(r"TRACCIA voci=(\d+) siti=(\d+)", outC)
    siti = dict(re.findall(r"^SITO (\S+)\s+(\d+)$", outC, re.M))
    somme = dict(re.findall(r"^SOMMA (\S+)\s+(\S+)$", outC, re.M))
    nz = [k for k, v in somme.items() if abs(float(v)) > 0.0]
    segna("Z2", bool(voci) and int(voci.group(2)) >= 2 and len(nz) >= 2,
          "traccia: %s voci su %s siti distinti; siti con somma NON nulla: %d -> %s"
          % (voci.group(1) if voci else "0", voci.group(2) if voci else "0", len(nz),
             sorted(nz)[:6]))

    m = re.search(r"SNAPSHOT traccia_nel_filtro=(\d+)", outC)
    segna("Z2b", bool(m) and int(m.group(1)) == 0,
          "la traccia NON entra nello snapshot: %s campi 'traccia' passano il filtro di salva_stato"
          % (m.group(1) if m else "?"))

    print("")
    print("  i DICIANNOVE siti, quante volte hanno girato in %d passi:" % PASSI)
    for k in sorted(siti):
        print("    %-22s %6s   somma algebrica %s" % (k, siti[k], somme.get(k, "n/d")))

    print("")
    n_pass = sum(1 for _, o in esiti if o)
    print("ESITO: %d/%d" % (n_pass, len(esiti)))
    print("")
    print("⚠ Z3 NON E' QUI: e' il sigillo interno di `_rigiocata_0_120.py` (che passo' 138/138),")
    print("  e si gira col flag ACCESO. Se la strumentazione avesse toccato il PERCORSO, li' si")
    print("  vedrebbe -- e questo sigillo, che confronta solo lo stato finale, no.")
    print("UN SEME, UNA SCENA, %d passi." % PASSI)
    return 0 if n_pass == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
