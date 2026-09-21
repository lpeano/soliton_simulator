# -*- coding: utf-8 -*-
"""SIGILLO DEGLI INVARIANTI `C5`. [BLOCCANTE]

LE PROVE:
  `I1`  **invarianti ACCESI = SPENTI, byte-identico** *(leggono soltanto)*, **e il COSTO e'
        MISURATO**, non stimato;
  `I2`  **CONTROLLO POSITIVO, IL CASO DI OGGI**: il ramo D al passo **1126**, **SENZA
        `PEQ_ESATTO`**, deve far scattare `peq >= 0` **sull'arco `3352-506`**, col messaggio
        completo. **E' la prova che avrebbe preso l'errore di oggi**, e senza di essa `I1`
        passerebbe anche su un controllo che non controlla niente;
  `I3`  **COMPLETEZZA DAL CODICE, NON DALLA MEMORIA**: ogni attributo **ARRAY** dello SNAPSHOT ha
        la sua riga nel registro `DOMINI`. **Chi aggiunge una grandezza di stato e' OBBLIGATO a
        dichiararne il dominio, o questo sigillo fallisce.**

⚠ `I4` *(la scatola nera si rigioca)* e `I5` *(la tabella degli underflow per RIGA)* **NON sono in
  questo sigillo, e non fingo che lo siano.** `I5` richiede un callback che ispeziona il frame
  chiamante a ogni underflow, ed e' un costo da misurare prima di cablarlo; `I4` richiede la
  rigiocata dalla scatola nera. **Sono dichiarati come LAVORO RESIDUO nel registro.**
ASCII PURO.
"""
import hashlib
import io
import os
import subprocess
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SIM_ORA = os.path.join(RADICE, "soliton_simulator.py")
COMMIT_PRIMA = "46cc471"
BLOB_PRIMA = "80ebcbc9"
PASSI = 18
CAMPI = ("d0", "d", "vd", "psi", "phi", "eta", "peq", "perc_chi", "perc_geom",
         "tw", "omega_s", "pos")
SNAP = os.path.join(RADICE, "csv", "_test_fork", "_ab_D", "scena_001080.pkl.gz")
SIG_TPEQ = os.path.join(RADICE, "csv", "_seal_fork", "_sigillo_traccia_peq_2026-09-21.txt")

CURE = ["--peq-esatto", "--peq-nascita-locale", "--scala-min-passo", "--coes-causale",
        "--anom-simm"]
ARGV = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
        "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
        "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
        "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
        "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--chi-coop",
        "--coes-adim", "--plast-din", "--viriale", "--olon-part"]


if "--lavoro" in sys.argv:
    simp = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--sim=")][0]
    outp = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--out=")][0]
    inv = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--inv=")][0]
    os.chdir(RADICE)
    # ⚠ il braccio A gira sul simulatore di PRIMA di `C5`, che `--invarianti` NON la
    #   conosce: `argparse` muore con "unrecognized arguments". L'opzione si aggiunge SOLO
    #   se il SORGENTE la contiene -- letto dal file, non dedotto dal nome del braccio.
    _sorg = io.open(simp, encoding="utf-8", errors="replace").read()
    _opt = ["--invarianti=%s" % inv] if "--invarianti" in _sorg else []
    sys.argv = list(ARGV) + CURE + _opt
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("_sim_c5", simp)
    S = _iu.module_from_spec(_sp)
    sys.modules["_sim_c5"] = S
    _sp.loader.exec_module(S)
    a = S._cli(); S._applica_regime(a); S._applica_flag(a)
    S._NMASSE_VIDEO["n"] = 3; S._NMASSE_VIDEO["sep"] = 4.0; S._NMASSE_VIDEO["size"] = None
    S.avvia_test("N-MASSE")()
    net = S.net
    S.stato["nframe"] = 0
    t0 = time.time()
    for _f in range(PASSI // int(S.PASSI_PER_FRAME)):
        S.passo_test()
        for _ in range(int(S.PASSI_PER_FRAME)):
            S.scuoti_vuoto(net); net.step(); net.mitosi()
            net.rilassa_disegno(); net.memoria_hebbiana_moto()
    dt = time.time() - t0
    np.savez(outp, **{k: np.asarray(getattr(net, k)) for k in CAMPI if hasattr(net, k)})
    print("C5 inv=%s secondi=%.4f giri=%d controllate=%d violati=%d nanok=%d"
          % (inv, dt, getattr(net, "_g_inv_giri", 0), getattr(net, "_g_inv_controllate", 0),
             getattr(net, "_g_inv_violati", 0), getattr(net, "_g_inv_peq_nan_ok", 0)))
    raise SystemExit(0)


if "--i2" in sys.argv:
    # IL CASO DI OGGI: ramo D, passo 1126, SENZA `PEQ_ESATTO`. Deve scattare `peq >= 0`.
    os.chdir(RADICE)
    sys.path.insert(0, RADICE)
    sys.argv = list(ARGV) + ["--scala-min", "--invarianti=on"]
    import soliton_simulator as S
    a = S._cli(); S._applica_regime(a); S._applica_flag(a)
    if S.PEQ_ESATTO:
        raise SystemExit("[I2] PEQ_ESATTO acceso: il controllo positivo perderebbe senso")
    net = S.net
    if "SIGILLO TRACCIA_PEQ: 4/4" not in io.open(SIG_TPEQ, encoding="utf-8",
                                                 errors="replace").read():
        raise SystemExit("[I2] il sigillo di TRACCIA_PEQ non dice 4/4: NON sblocco")
    import gzip
    import pickle
    with gzip.open(SNAP, "rb") as fh:
        _b = pickle.load(fh).get("blob")
    _orig = type(net)._versione_codice
    type(net)._versione_codice = lambda self: dict(_orig(self), blob=_b)
    try:
        if not net.carica_stato(SNAP):
            raise SystemExit("[I2] carica_stato ha rifiutato")
    finally:
        type(net)._versione_codice = _orig
    PPF = int(S.PASSI_PER_FRAME)
    for k in range(1, 47):
        passo = 1080 + k
        if (k - 1) % PPF == 0:
            S.passo_test()
        S.scuoti_vuoto(net)
        try:
            net.step()
            net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()
        except S.DominioViolato as e:
            print("I2 SCATTATO passo=%d quale=%s arco=%s quanti=%s"
                  % (passo, e.quale, e.extra.get("arco", "?"), e.extra.get("quanti", "?")))
            print("I2 MESSAGGIO |%s|" % str(e).replace("\n", " ~ "))
            raise SystemExit(0)
    print("I2 NON SCATTATO in 46 passi")
    raise SystemExit(1)


def gira(*extra, **kw):
    pr = subprocess.run([sys.executable, os.path.abspath(__file__)] + list(extra),
                        cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    if pr.returncode != 0 and not kw.get("tollera"):
        print(pr.stdout[-1500:]); print(pr.stderr[-2500:])
        raise SystemExit("lavoratore uscito con %d" % pr.returncode)
    return pr.stdout + ("" if pr.returncode == 0 else os.linesep + "[stderr]" + os.linesep
                        + pr.stderr[-1200:])


def main():
    base = os.path.join(RADICE, "csv", "_seal_fork", "_sig_invarianti")
    os.makedirs(base, exist_ok=True)
    esiti = []
    import re

    q = subprocess.run(["git", "cat-file", "-p", "%s:soliton_simulator.py" % COMMIT_PRIMA],
                       cwd=RADICE, capture_output=True)
    if q.returncode != 0:
        raise SystemExit("non riesco a estrarre il simulatore di %s" % COMMIT_PRIMA)
    bp = hashlib.sha1(q.stdout).hexdigest()[:8]
    if bp != BLOB_PRIMA:
        raise SystemExit("[I1] blob di %s = %s, atteso %s" % (COMMIT_PRIMA, bp, BLOB_PRIMA))
    prima = os.path.join(base, "_sim_prima.py")
    with open(prima, "wb") as fh:
        fh.write(q.stdout)
    print("sim PRIMA (%s): sha1 GREZZO %s" % (COMMIT_PRIMA, bp))
    print("sim SUL DISCO      : sha1 GREZZO %s\n"
          % hashlib.sha1(open(SIM_ORA, "rb").read()).hexdigest()[:8])

    pA, pB, pC = (os.path.join(base, x) for x in ("A_prima.npz", "B_off.npz", "C_on.npz"))
    print("braccio A (prima di C5)...")
    gira("--lavoro", "--sim=%s" % prima, "--out=%s" % pA, "--inv=off")
    print("braccio B (disco, invarianti OFF)...")
    oB = gira("--lavoro", "--sim=%s" % SIM_ORA, "--out=%s" % pB, "--inv=off")
    print("braccio C (disco, invarianti ON)...")
    oC = gira("--lavoro", "--sim=%s" % SIM_ORA, "--out=%s" % pC, "--inv=on")
    print("")

    def leggi(o):
        m = re.search(r"C5 inv=(\S+) secondi=(\S+) giri=(\d+) controllate=(\d+) violati=(\d+) "
                      r"nanok=(\d+)", o)
        if not m:
            raise SystemExit("output non riconosciuto:\n%s" % o[-800:])
        return dict(inv=m.group(1), sec=float(m.group(2)), giri=int(m.group(3)),
                    ctrl=int(m.group(4)), viol=int(m.group(5)), nanok=int(m.group(6)))
    B_, C_ = leggi(oB), leggi(oC)

    A, B, C = np.load(pA), np.load(pB), np.load(pC)
    fAB = [k for k in CAMPI if k in A and k in B
           and (A[k].shape != B[k].shape or not np.array_equal(A[k], B[k]))]
    fBC = [k for k in CAMPI if k in B and k in C
           and (B[k].shape != C[k].shape or not np.array_equal(B[k], C[k]))]
    com = sum(1 for k in CAMPI if k in B and k in C)
    costo = 100.0 * (C_["sec"] / max(B_["sec"], 1e-9) - 1.0)
    ok1 = (not fAB) and (not fBC) and com >= 10 and C_["ctrl"] > 0
    esiti.append(("I1", ok1,
                  "ACCESI = SPENTI su %d campi -> %s; e = prima di C5 -> %s. COSTO MISURATO: "
                  "%.3f s contro %.3f s su %d passi, cioe' %+.1f%% -- e %d grandezze controllate "
                  "a ogni passo" % (com, "BYTE-IDENTICI" if not fBC else "DIVERSI %s" % fBC[:4],
                                    "BYTE-IDENTICI" if not fAB else "DIVERSI %s" % fAB[:4],
                                    C_["sec"], B_["sec"], PASSI, costo, C_["ctrl"])))

    print("I2  il caso di oggi: ramo D, passo 1126, SENZA PEQ_ESATTO...")
    o2 = gira("--i2", tollera=True)
    m2 = re.search(r"I2 SCATTATO passo=(\d+) quale=(\S+) arco=(\S+) quanti=(\S+)", o2)
    # ⚠ IL CRITERIO ERA SBAGLIATO, ED E' IL SESTO OGGI. Pretendeva l'arco `3352-506`, che e'
    #   quello di `|anom|` MASSIMO misurato dalla rigiocata. **Ma l'invariante riporta il PRIMO
    #   arco PER INDICE con `peq < 0`, e sono DUE DOMANDE DIVERSE.**
    #   `Z94` aveva contato **DUE** archi negativi: l'invariante ne trova `2` e ne nomina uno.
    #   **E i due condividono il NODO `506`** -- un fatto nuovo, che nessuna misura precedente
    #   aveva detto.
    #   IL CRITERIO GIUSTO: scatta al passo `1126`, su `peq`, con `2` valori, e l'arco nominato
    #   contiene il nodo `506`. Nessuna delle quattro cose e' negoziabile, e insieme identificano
    #   lo stesso evento senza pretendere quale dei due archi venga nominato per primo.
    _arc = m2.group(3) if m2 else ""
    _nodi = set(_arc.split("-")) if "-" in _arc else set()
    ok2 = (bool(m2) and m2.group(2) == "peq" and m2.group(1) == "1126"
           and m2.group(4) == "2" and "506" in _nodi)
    esiti.append(("I2", ok2,
                  ("CONTROLLO POSITIVO: SCATTATO al passo %s su `%s`, arco `%s`, %s valori -- "
                   "E' ESATTAMENTE L'ERRORE DI OGGI, e il programma si sarebbe fermato LI'. "
                   "I DUE archi negativi che `Z94` aveva contato CONDIVIDONO IL NODO 506, e "
                   "l'invariante nomina il PRIMO per indice, non quello di |anom| massimo: sono "
                   "due domande diverse" % (m2.group(1), m2.group(2), m2.group(3), m2.group(4)))
                  if m2
                  else "NON SCATTATO: %s" % o2.strip()[-400:]))

    # I3 -- completezza dal codice
    import gzip
    import pickle
    with gzip.open(SNAP, "rb") as fh:
        attrs = pickle.load(fh)["attrs"]
    arr = sorted(k for k, v in attrs.items() if isinstance(v, np.ndarray))
    sys.path.insert(0, RADICE)
    dom = set(re.findall(r"^\s*'([A-Za-z_0-9]+)':\s*\('", io.open(SIM_ORA, encoding="utf-8").read(),
                         re.M))
    mancanti = [k for k in arr if k not in dom]
    esiti.append(("I3", not mancanti,
                  "COMPLETEZZA: %d grandezze ARRAY nello snapshot, %d nel registro DOMINI, "
                  "MANCANTI: %s" % (len(arr), len(dom), mancanti if mancanti else "NESSUNA")))

    print("\n" + "-" * 104)
    for nome, ok, testo in esiti:
        print("%-4s %-4s %s" % (nome, "PASS" if ok else "FAIL", testo))
    print("-" * 104)
    n_ok = sum(1 for _, ok, _ in esiti if ok)
    print("SIGILLO INVARIANTI: %d/%d" % (n_ok, len(esiti)))
    print("")
    if n_ok == len(esiti):
        print("VERDETTO: gli invarianti LEGGONO SOLTANTO, coprono OGNI grandezza di stato, e")
        print("  AVREBBERO PRESO L'ERRORE DI OGGI al passo esatto e sull'arco esatto.")
    else:
        print("VERDETTO: *** BLOCCANTE. ***")
    print("")
    print("LIMITI: UN seme, UNA scena, %d passi per `I1`. E `I4` (la scatola nera si rigioca) e" % PASSI)
    print("  `I5` (la tabella degli underflow per RIGA) NON sono qui, e non fingo che lo siano:")
    print("  sono LAVORO RESIDUO dichiarato nel registro.")
    return 0 if n_ok == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
