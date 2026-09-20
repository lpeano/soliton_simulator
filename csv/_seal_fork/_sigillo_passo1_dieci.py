# -*- coding: utf-8 -*-
"""SIGILLO DEL PASSO 1, SECONDO GIRO -- i dieci contatori sono BYTE-INERTI e si leggono.

Mandato: doc/REFERTO_classifica_18_guardie.md + doc/REFERTO_verifica_phi_s_e_crescita_n.md.

  W1  BYTE-IDENTITA' [BLOCCANTE]: la sola contabilita' non deve cambiare un bit di psi, d, phi,
      eta, n, pos, tw. Confronto col simulatore PRIMA (`a6cd7d6`), estratto da git IN BINARIO.
  W2  I CONTATORI SI LEGGONO: tutti e dieci presenti in `rapporto_guardie`.
  W3  E POSSONO SCATTARE -- ma qui il criterio e' DIVERSO PER CLASSE, ed e' fissato PRIMA:
        * le tre (a) DEVONO poter scattare. Se una non scatta, e' codice morto e va detto;
        * le cinque (c) sono state classificate come "non possono fallire": se NON si riesce a
          farle scattare nemmeno CORROMPENDO lo stato, quella e' la prova PIU' FORTE della (c),
          non un fallimento. Se invece scattano corrompendo `perc_chi`/`phi_s`, vuol dire che la
          guardia E' raggiungibile da uno stato malformato, e il contatore serve.
      ⚠ La distinzione e' scritta QUI, PRIMA di girare: un criterio che si decide dopo aver visto
      l'esito e' la classe di difetto che questo repo ha gia' preso cinque volte.
  W4  le due (b) hanno `_spento`, non `_salti`: si verifica che il contatore SPENTO sia al 100 %.

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
BASE = os.path.join(RADICE, "csv", "_seal_fork", "_sig_dieci")
COMMIT_PRIMA = "a6cd7d6"
PASSI = 12
CAMPI = ("psi", "d", "phi", "eta", "n", "pos", "tw")
CLASSE_A = ("nb_prec", "snap_psispin", "nb_grav_proiez")
CLASSE_C = ("calore_chi", "chicore_passo", "temposegno", "spinore_vivo", "chi_da_spinore")
CLASSE_B = ("compat_chi", "k_frange")

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
        print(pr.stdout[-1200:])
        print(pr.stderr[-1800:])
        raise SystemExit("runner uscito con %d" % pr.returncode)
    return pr.stdout


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
    print("simulatore PRIMA (%s): sha1 grezzo %s" % (COMMIT_PRIMA, hashlib.sha1(q.stdout).hexdigest()[:8]))
    print("simulatore ORA            : sha1 grezzo %s" % hashlib.sha1(dn).hexdigest()[:8])
    print("")

    oA, oB = os.path.join(BASE, "prima.npz"), os.path.join(BASE, "ora.npz")
    print("braccio A: simulatore PRIMA")
    gira(vecchio, oA)
    print("braccio B: simulatore ORA")
    outB = gira(SIM_ORA, oB)
    A, B = np.load(oA), np.load(oB)
    fuori = []
    for k in CAMPI:
        x, y = A[k], B[k]
        if x.shape != y.shape:
            fuori.append("%s(shape)" % k)
        elif not np.array_equal(x, y):
            fuori.append("%s(max|A-B|=%.3e)" % (k, float(np.nanmax(np.abs(x - y)))))
    segna("W1", not fuori, "%d campi: %s" % (len(CAMPI), "TUTTI IDENTICI" if not fuori else fuori))
    if fuori:
        print("  *** W1 e' BLOCCANTE. FERMO. ***")
        return 1

    righe = [r for r in outB.split("\n") if r.startswith("GUARDIA")]
    visti = set(r.split()[1] for r in righe if len(r.split()) > 1)
    attesi = set(CLASSE_A + CLASSE_C) | set(k + "_SPENTO" for k in CLASSE_B)
    manc = sorted(attesi - visti)
    segna("W2", not manc, "i dieci si leggono: %d attesi presenti%s"
          % (len(attesi), "" if not manc else "   MANCANO: %s" % manc))
    for r in righe:
        print("      " + r)

    # ------------------------------------------------------------------ W4, le due (b)
    ok_b = True
    for k in CLASSE_B:
        m = [r for r in righe if r.split()[1] == k + "_SPENTO"]
        if not m:
            ok_b = False
            continue
        fr = float(re.search(r"frazione=(\S+)", m[0]).group(1))
        if abs(fr - 1.0) > 1e-9:
            ok_b = False
    segna("W4", ok_b, "le due (b): il ramo e' SPENTO al 100 % (flag/costante off), come atteso")

    # ------------------------------------------------------------------ W3
    print("")
    print("W3 -- si prova a far SCATTARE ciascun contatore, corrompendo lo stato")
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

    def prova(k, prep):
        p0 = salti(k)
        pc, ps, nb, nbp, psp = (net.perc_chi.copy(), net.phi_s.copy(),
                                getattr(net, "_nb", None), getattr(net, "_nb_prec", None),
                                getattr(net, "psi_spin", None))
        try:
            prep()
        except Exception:
            pass
        net.perc_chi, net.phi_s = pc, ps
        net._nb, net._nb_prec = nb, nbp
        if psp is not None:
            net.psi_spin = psp
        return salti(k) - p0

    def corrompi_perc_chi():
        net.perc_chi = np.zeros(3, int)

    prove = {}
    # (c) calore_chi  -- funzione di modulo, flag forzato in processo
    _cv = S.CALORE_VETTORIALE
    S.CALORE_VETTORIALE = True
    prove["calore_chi"] = prova("calore_chi", lambda: (corrompi_perc_chi(), S.scuoti_vuoto(net)))
    S.CALORE_VETTORIALE = _cv
    # (c) chicore_passo / temposegno / chi_da_spinore  -- `perc_chi` corto, poi uno step
    _td, _cds = S.TEMPO_SEGNO, S.CHI_DA_SPINORE
    S.TEMPO_SEGNO = True
    S.CHI_DA_SPINORE = True
    for k in ("chicore_passo", "temposegno", "chi_da_spinore"):
        prove[k] = prova(k, lambda: (corrompi_perc_chi(), net.step()))
    S.TEMPO_SEGNO, S.CHI_DA_SPINORE = _td, _cds
    # (c) spinore_vivo -- `phi_s` di lunghezza sbagliata
    prove["spinore_vivo"] = prova(
        "spinore_vivo", lambda: (setattr(net, "phi_s", np.zeros(3)), net.step()))
    # (a) nb_prec -- `_nb_prec` di lunghezza sbagliata
    prove["nb_prec"] = prova(
        "nb_prec", lambda: (setattr(net, "_nb_prec", np.zeros((3, 3))), net.step()))
    # (a) snap_psispin -- `psi_spin` di lunghezza sbagliata
    prove["snap_psispin"] = prova(
        "snap_psispin", lambda: (setattr(net, "psi_spin", np.zeros((3, 2), complex)), net.step()))
    # (a) nb_grav_proiez -- `_nb` corto
    prove["nb_grav_proiez"] = prova(
        "nb_grav_proiez", lambda: (setattr(net, "_nb", np.zeros((3, 3))),
                                   net.memoria_hebbiana_moto()))

    print("      classe  sito                incremento")
    ok_a = True
    non_forzabili = []
    for k in CLASSE_A + CLASSE_C:
        cl = "(a)" if k in CLASSE_A else "(c)"
        inc = prove.get(k, 0)
        print("      %-7s %-20s %d%s" % (cl, k, inc,
              "   <- SCATTA" if inc > 0 else "   <- NON forzabile"))
        if inc <= 0:
            non_forzabili.append((cl, k))
            if cl == "(a)":
                ok_a = False
    print("")
    for cl, k in non_forzabili:
        if cl == "(c)":
            print("      (c) %-18s non si fa scattare NEMMENO corrompendo lo stato:" % k)
            print("          e' la prova PIU' FORTE della (c), non un fallimento. Criterio fissato PRIMA.")
        else:
            print("      *** (a) %-14s NON scatta: sarebbe CODICE MORTO, e va detto. ***" % k)
    segna("W3", ok_a, "le tre (a) scattano tutte" if ok_a
          else "almeno una (a) NON scatta: vedi sopra")

    print("")
    n_pass = sum(1 for _, o in esiti if o)
    print("ESITO: %d/%d" % (n_pass, len(esiti)))
    print("")
    print("NB: UNA scena, UN seme, %d passi." % PASSI)
    return 0 if n_pass == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
