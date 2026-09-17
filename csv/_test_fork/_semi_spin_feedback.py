# -*- coding: utf-8 -*-
"""A/B di `SPIN_FEEDBACK` A QUATTRO SEMI, con la cura del denominatore dentro. (mandato par.3)

IL CRITERIO E' SCRITTO QUI, PRIMA DI GIRARE, e non si proroga.

LA DOMANDA: il `-32 %` di nodi a `TAU_A = 2.0` si riduce accendendo `SPIN_FEEDBACK`?
Su UN seme dava `-31.9 % -> -28.9 %`, cioe' **+3.0 punti**. **Un seme non e' un dato** (P3).

IL DISEGNO, appaiato per seme:
  per ogni seme s in {5, 11, 17, 23}:  un braccio OFF e un braccio ON, TUTTO il resto identico,
  `TAU_A = 2.0` in ENTRAMBI. La differenza si calcola DENTRO il seme (appaiata), e la barra e' la
  dispersione FRA SEMI di quelle differenze -- MAI la SE interna a un run (P3, C10).

IL CRITERIO, fissato ADESSO:
  con 4 semi appaiati, `t(0.025, 3) = 3.182`. L'effetto e' DICHIARATO se
      |media delle differenze|  >  3.182 * SD(differenze) / sqrt(4)   =   1.591 * SD
  cioe' se l'IC95 della media appaiata NON contiene lo zero.
  **Se lo contiene, l'effetto NON C'E', e si scrive come LIMITE SUPERIORE** -- *«il feedback non
  sposta il conteggio nodi di piu' di X punti»* -- **non come «nessun effetto»** (presidio sui
  risultati nulli: un nullo si legge solo insieme alla RISOLUZIONE che lo ha prodotto).

SI RIPORTANO ENTRAMBI I LATI DEL BILANCIO:
  - il GUADAGNO preteso: conteggio nodi;
  - il COSTO gia' visto: `max|d0|` (era `x17.5 -> x27`, +21 punti) e `max|psi|` (era `x91 -> x112`).
  **Un bilancio che pesa solo il lato favorevole non e' un bilancio.**

P6: `TAU_A` e `SPIN_FEEDBACK` sono letti DAI DATI (il blocco `# RUN_PARAMS` del CSV), non dal
comando. Un run che non lo conferma NON SI CONTA.
ASCII PURO.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import _presidio
_presidio.avvia(__file__)

import json
import pickle
import subprocess

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SC = os.environ.get("SCRATCH", HERE)
SEMI = [5, 11, 17, 23]
PASSI = 120
REG = {"deterministico": 50.0, "canonico": 2.0}


def gira(tag, seme, feedback):
    db = os.path.join(SC, "_sem_%s.pkl" % tag)
    csv = os.path.join(SC, "_sem_%s.csv" % tag)
    cmd = [sys.executable, os.path.join(ROOT, "soliton_simulator.py"),
           "--batch", "--nmasse", "3", "--sep", "8", "--seed", str(seme),
           "--passi", str(PASSI), "--ogni", str(PASSI), "--db-ogni", str(PASSI),
           "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto", "--chi-core",
           "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2", "--fork-su2-mem",
           "--cs-dinamico", "--tau-a", "2.0"]
    if feedback:
        cmd.append("--spin-feedback")
    cmd += ["--csv", csv, "--sync-db", db, "--db-cleanup"]
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    attrs = pickle.load(open(db, "rb"))["attrs"] if (p.returncode == 0 and os.path.exists(db)) else None
    # P6: le condizioni si leggono DAI DATI
    cond = None
    if os.path.exists(csv):
        with open(csv, encoding="utf-8", errors="replace") as fh:
            prima = fh.readline()
        if prima.startswith("# RUN_PARAMS "):
            P = json.loads(prima[len("# RUN_PARAMS "):])
            la = P.get("leggi_attive", {})
            ov = P.get("tau_a_over")
            cond = dict(tau_a=(float(ov) if ov is not None else REG.get(la.get("REGIME"), float("nan"))),
                        feedback=bool(la.get("SPIN_FEEDBACK")), seme=P.get("seed"))
    return p, attrs, cond


print("=" * 118)
print("A/B `SPIN_FEEDBACK` a %d SEMI, con la cura del denominatore. TAU_A = 2.0 in entrambi i bracci."
      % len(SEMI))
print("=" * 118)

D = {}
for s in SEMI:
    for fb in (False, True):
        tag = "%s_%s" % (s, "on" if fb else "off")
        D[(s, fb)] = gira(tag, s, fb)

# ---------------------------------------------------------------- P6 PRIMA di tutto
print("\n--- P6: le condizioni LETTE DAI DATI (# RUN_PARAMS), non dal comando ---")
print("  %-8s %-8s %-10s %-14s %-8s %-6s" % ("seme", "braccio", "TAU_A", "SPIN_FEEDBACK", "seed", "rc"))
valide = []
for s in SEMI:
    for fb in (False, True):
        p, attrs, cond = D[(s, fb)]
        if cond is None:
            print("  %-8d %-8s NESSUN blocco RUN_PARAMS -> IL RUN NON SI CONTA" % (s, "ON" if fb else "OFF"))
            continue
        ok = (abs(cond["tau_a"] - 2.0) < 1e-9) and (cond["feedback"] == fb) and (cond["seme"] == s)
        print("  %-8d %-8s %-10s %-14s %-8s %-6s %s"
              % (s, "ON" if fb else "OFF", cond["tau_a"], cond["feedback"], cond["seme"],
                 p.returncode, "" if ok else "  <-- NON CONFORME, NON SI CONTA"))
        if ok and attrs is not None:
            valide.append((s, fb))
coppie = [s for s in SEMI if (s, False) in valide and (s, True) in valide]
print("\n  semi con ENTRAMBI i bracci validi: %s  (%d)" % (coppie, len(coppie)))
if len(coppie) < 4:
    print("  ⚠ MENO DI 4 SEMI APPAIATI: con 3 gradi di liberta' o meno la barra FRA SEMI non e'")
    print("     utilizzabile (t(0.025,1) = 12.706). Si riporta, ma NON si conclude.")


def leggi(attrs):
    n = len(np.asarray(attrs["psi"]))
    d0 = np.asarray(attrs["d0"], float); psi = np.abs(np.asarray(attrs["psi"]))
    return dict(n=n, d0=float(np.max(d0)), psi=float(np.max(psi)))


# ---------------------------------------------------------------- i numeri, per seme
print("\n--- I NUMERI, per seme (appaiati) ---")
print("  %-6s %-10s %-10s %-10s %-12s %-12s %-12s %-12s" %
      ("seme", "n OFF", "n ON", "delta n", "d0 OFF", "d0 ON", "psi OFF", "psi ON"))
dn, dd0, dpsi = [], [], []
for s in coppie:
    a = leggi(D[(s, False)][1]); b = leggi(D[(s, True)][1])
    dn.append(b["n"] - a["n"]); dd0.append(b["d0"] - a["d0"]); dpsi.append(b["psi"] - a["psi"])
    print("  %-6d %-10d %-10d %-10d %-12.5g %-12.5g %-12.5g %-12.5g"
          % (s, a["n"], b["n"], b["n"] - a["n"], a["d0"], b["d0"], a["psi"], b["psi"]))

if len(coppie) >= 2:
    T = {2: 12.706, 3: 4.303, 4: 3.182, 5: 2.776, 6: 2.571}

    def barra(v, nome, unita=""):
        v = np.asarray(v, float)
        k = len(v)
        m = float(np.mean(v)); sd = float(np.std(v, ddof=1)) if k > 1 else float("nan")
        se = sd / np.sqrt(k) if k > 1 else float("nan")
        t = T.get(k, 2.0)
        ic = t * se
        dichiarato = abs(m) > ic
        print("  %-22s media %+10.4g   SD FRA SEMI %10.4g   IC95 +-%9.4g   -> %s"
              % (nome, m, sd, ic, "EFFETTO DICHIARATO" if dichiarato else "IC95 CONTIENE LO ZERO"))
        if not dichiarato:
            print("  %-22s   -> si scrive come LIMITE SUPERIORE: non si sposta di piu' di %.4g %s"
                  % ("", abs(m) + ic, unita))
        return dichiarato

    print("\n--- IL CRITERIO, fissato PRIMA: IC95 appaiato, t(0.025, %d) = %s ---"
          % (len(coppie) - 1, T.get(len(coppie), "?")))
    print("  (la barra e' la dispersione FRA SEMI delle differenze appaiate, MAI la SE interna)")
    barra(dn, "delta CONTEGGIO NODI", "nodi")
    print("\n--- E L'ALTRO LATO DEL BILANCIO (il COSTO), con la stessa cura ---")
    barra(dd0, "delta max|d0|")
    barra(dpsi, "delta max|psi|")
    # il contesto: il -32 % contro cui si misura
    print("\n  PER CONTESTO, e va ricordato: il `-32 %%` e' il divario TAU_A=50 -> TAU_A=2.0.")
    print("  Qui entrambi i bracci sono a TAU_A = 2.0: si misura SOLO quanto il feedback recupera.")
    if len(coppie) >= 2:
        med_off = float(np.mean([leggi(D[(s, False)][1])["n"] for s in coppie]))
        print("  media n OFF = %.1f ; il recupero medio vale %+.2f %% del braccio OFF"
              % (med_off, 100.0 * float(np.mean(dn)) / max(med_off, 1)))

print("\n" + "=" * 118)
print("""COME SI LEGGE -- il criterio era scritto PRIMA e non si proroga
  IC95 NON contiene lo zero -> l'effetto e' DICHIARATO, con la sua ampiezza.
  IC95 CONTIENE lo zero     -> l'effetto NON C'E' come misurato, e si scrive come LIMITE SUPERIORE.
                               «non si sposta di piu' di X» -- NON «nessun effetto».
  E il bilancio si legge sui DUE lati: se il conteggio nodi migliora ma `d0` peggiora oltre la sua
  barra, l'ipotesi non ha retto: ha spostato il problema.""")
