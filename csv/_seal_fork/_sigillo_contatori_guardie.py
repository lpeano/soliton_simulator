# -*- coding: utf-8 -*-
"""SIGILLO DEL PASSO 1 -- i contatori delle guardie silenziose sono BYTE-INERTI e POSSONO SCATTARE.

Mandato: doc/TASK_HISTORY/2026-09-20_tre-guardie-silenziose.md (93e1628).

  V1  BYTE-IDENTITA' [BLOCCANTE]: la sola contabilita' non deve cambiare un bit di `psi`, `d`,
      `phi`, `eta`, `n` (e qui anche `pos` e `tw`). Si confronta il simulatore PRIMA -- estratto da
      git IN BINARIO, mai con `git checkout` (C18) -- contro quello di ADESSO, a parita' di tutto.
  V2  I CONTATORI SI LEGGONO: per sito, col nome, la frazione, la FORMA e QUANDO.
  V3  E POSSONO SCATTARE, su CIASCUNO: si forza una lunghezza sbagliata e si verifica che il
      contatore salga. SENZA QUESTA PROVA sarebbe codice morto -- par.10 punto 2: un sigillo di
      sola byte-identita' passa anche su codice che non fa niente.

I due bracci di V1 girano in PROCESSI SEPARATI (`_runner_sim.py`), perche' `import` carica un solo
simulatore per processo e il file della radice NON si tocca mai.
ASCII PURO.
"""
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
BASE = os.path.join(RADICE, "csv", "_seal_fork", "_sig_contatori")
# Il commit di RIFERIMENTO si passa da riga di comando: lo stesso sigillo serve per PIU' cure
# byte-inerti (i contatori, poi i tre gruppi del PASSO 2), e ognuna va confrontata col commit che
# la PRECEDE. Cablarlo qui avrebbe costretto a modificare il sigillo a ogni cura -- e un sigillo
# che cambia a ogni giro non certifica piu' la stessa cosa.
COMMIT_PRIMA = "93e1628"
for _x in sys.argv[1:]:
    if _x.startswith("--commit-prima="):
        COMMIT_PRIMA = _x.split("=", 1)[1]
PASSI = 12
CAMPI = ("psi", "d", "phi", "eta", "n", "pos", "tw")
SITI = ("kernel_alpha", "tempo_luce", "zeta_vir_a", "zeta_vir_b", "tors4pi")

esiti = []


def segna(nome, ok, det):
    esiti.append((nome, ok))
    print("%-5s %-6s %s" % (nome, "PASS" if ok else "FAIL", det))


def gira(sim, out):
    cmd = [sys.executable, os.path.join(_QUI, "_runner_sim.py"),
           "--sim=%s" % sim, "--out=%s" % out, "--passi=%d" % PASSI]
    pr = subprocess.run(cmd, cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    if pr.returncode != 0:
        print(pr.stdout[-1500:])
        print(pr.stderr[-2000:])
        raise SystemExit("runner uscito con %d" % pr.returncode)
    return pr.stdout


def main():
    os.makedirs(BASE, exist_ok=True)
    import hashlib
    # --- il simulatore PRIMA, estratto IN BINARIO
    vecchio = os.path.join(BASE, "_sim_prima.py")
    q = subprocess.run(["git", "cat-file", "-p", "%s:soliton_simulator.py" % COMMIT_PRIMA],
                       cwd=RADICE, capture_output=True)
    if q.returncode != 0:
        raise SystemExit("non riesco a estrarre il simulatore di %s" % COMMIT_PRIMA)
    with open(vecchio, "wb") as f:
        f.write(q.stdout)
    with open(SIM_ORA, "rb") as f:
        dn = f.read()
    print("simulatore PRIMA (%s): sha1 grezzo %s" % (COMMIT_PRIMA, hashlib.sha1(q.stdout).hexdigest()[:8]))
    print("simulatore ORA           : sha1 grezzo %s" % hashlib.sha1(dn).hexdigest()[:8])
    print("")

    # ---------------------------------------------------------------- V1
    oA = os.path.join(BASE, "prima.npz")
    oB = os.path.join(BASE, "ora.npz")
    print("braccio A: simulatore PRIMA (%d passi)" % PASSI)
    gira(vecchio, oA)
    print("braccio B: simulatore ORA   (%d passi)" % PASSI)
    outB = gira(SIM_ORA, oB)
    A, B = np.load(oA), np.load(oB)
    diversi = []
    for k in CAMPI:
        a, b = A[k], B[k]
        if a.shape != b.shape:
            diversi.append("%s(shape %s vs %s)" % (k, a.shape, b.shape))
        elif not np.array_equal(a, b):
            # ⚠ NON si casta a `float`: `psi` e' COMPLESSO e il cast scarta la parte
            # immaginaria. `np.abs` della differenza complessa E' il modulo.
            diversi.append("%s(max|A-B|=%.3e)" % (k, float(np.nanmax(np.abs(a - b)))))
    segna("V1", not diversi,
          "%d campi confrontati (%s): %s"
          % (len(CAMPI), ", ".join(CAMPI),
             "TUTTI IDENTICI" if not diversi else "DIVERSI -> %s" % diversi))
    if diversi:
        print("  *** V1 e' BLOCCANTE: la contabilita' sta toccando la fisica. FERMO. ***")
        return 1

    # ---------------------------------------------------------------- V2
    righe = [r for r in outB.split("\n") if r.startswith("GUARDIA")]
    segna("V2", len(righe) == len(SITI),
          "i contatori si leggono a fine run: %d siti su %d" % (len(righe), len(SITI)))
    for r in righe:
        print("      " + r)

    # ---------------------------------------------------------------- V3
    print("")
    print("V3 -- ogni contatore PUO' scattare? (si forza una lunghezza sbagliata, uno per uno)")
    sys.argv = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "8",
                "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
                "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
                "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
                "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--plast-din",
                "--viriale", "--olon-part"]
    sys.path.insert(0, RADICE)
    import soliton_simulator as S
    a = S._cli()
    S._applica_regime(a)
    S._applica_flag(a)
    S._NMASSE_VIDEO["n"] = 3
    S._NMASSE_VIDEO["sep"] = 8.0
    S._NMASSE_VIDEO["size"] = None
    S.avvia_test("N-MASSE")()
    net = S.net

    def salti(k):
        return int(getattr(net, "_g_%s_salti" % k, 0))

    prove = {}

    # kernel_alpha: `len(self.tw) != len(self.d)` dentro `_pesi`
    tw0 = net.tw.copy()
    p0 = salti("kernel_alpha")
    net.tw = np.zeros(len(net.d) + 1)
    try:
        net._pesi()
    except Exception:
        pass
    prove["kernel_alpha"] = salti("kernel_alpha") - p0
    net.tw = tw0

    # tempo_luce: `len(dd) != len(ii)` -- si chiama con `ii` piu' corto
    p0 = salti("tempo_luce")
    try:
        net._tempo_luce_nodo(net.i[:3], net.j[:3])
    except Exception:
        pass
    prove["tempo_luce"] = salti("tempo_luce") - p0

    # zeta_vir_a e _b: `_sin2_vir` di lunghezza sbagliata, col flag ACCESO
    p0a, p0b = salti("zeta_vir_a"), salti("zeta_vir_b")
    net._sin2_vir = np.zeros(3)
    try:
        net.step()
    except Exception:
        pass
    prove["zeta_vir_a"] = salti("zeta_vir_a") - p0a
    prove["zeta_vir_b"] = salti("zeta_vir_b") - p0b

    # tors4pi: `avv = np.abs(self.tw)`, quindi basta `tw` di lunghezza diversa da `i`
    p0 = salti("tors4pi")
    tw1 = net.tw.copy()
    net.tw = np.zeros(len(net.i) + 1)
    try:
        net.mitosi()
    except Exception:
        pass
    prove["tors4pi"] = salti("tors4pi") - p0
    net.tw = tw1

    tutti = True
    for k in SITI:
        ok = prove.get(k, 0) > 0
        tutti = tutti and ok
        print("      %-14s incremento %d  -> %s" % (k, prove.get(k, 0),
              "SCATTA" if ok else "*** NON SCATTA: codice morto ***"))
    segna("V3", tutti, "tutti e %d i contatori scattano quando devono" % len(SITI)
          if tutti else "almeno un contatore NON scatta")

    print("")
    n_pass = sum(1 for _, o in esiti if o)
    print("ESITO: %d/%d" % (n_pass, len(esiti)))
    print("")
    if n_pass == len(esiti):
        print("VERDETTO: i contatori sono BYTE-INERTI, si LEGGONO, e SCATTANO quando devono.")
        print("  Il PASSO 1 e' chiuso: adesso si puo' MISURARE quanto mordono le guardie.")
    else:
        print("VERDETTO: IL SIGILLO NON PASSA. I contatori NON si usano per decidere niente.")
    print("NB: UNA scena, UN seme, %d passi. V1 prova che la contabilita' non tocca la fisica" % PASSI)
    print("  IN QUESTO REGIME, non che non la tocchi mai.")
    return 0 if n_pass == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
