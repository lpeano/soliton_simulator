# -*- coding: utf-8 -*-
"""ESPERIMENTO: `TAU_A = 2.0` con `SPIN_FEEDBACK` ATTACCATO. A/B A VARIABILE SINGOLA.

  run A:  TAU_A = 2.0,  SPIN_FEEDBACK = OFF    (gia' fatto: psi x91, d0 x17, NODI -32 %)
  run B:  TAU_A = 2.0,  SPIN_FEEDBACK = ON     <- l'unica differenza

L'IPOTESI: il -32 % di nodi dipende dal fatto che lo spinore matura in fretta ma NON RETROAGISCE
sulla geometria -- un motore acceso con la trasmissione staccata.

!! `SPIN_FEEDBACK` NON HA UN SIGILLO: nessuna riduzione al limite, nessun controllo positivo.
Questo e' un esperimento su un COMPONENTE NON CERTIFICATO. NON promuove nulla.

E1 [BLOCCANTE] stabilita'   E2 il conteggio dei nodi (il numero che decide)
E3 psi / d0 / ramp          E4 [A8] il feedback e' davvero applicato, e quanto pesa?
ASCII PURO.
"""
import sys as _sys_enc  # PRESIDIO ENCODING (CLAUDE.md): lo stdout di Windows e' cp1252 e
# uccide qualunque print con un carattere non-ASCII. E' successo SETTE volte, l'ultima allo
# script che stava CONTANDO le occorrenze. Il `# -*- coding: utf-8 -*-` NON basta: riguarda il
# SORGENTE, non lo STDOUT. Questa riga lo risolve alla radice.
try:
    _sys_enc.stdout.reconfigure(encoding="utf-8")
    _sys_enc.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import os
import pickle
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SC = os.environ.get("SCRATCH", HERE)
esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-46s %s" % ("PASS" if ok else "FAIL", nome, misura))


def gira(tag, extra, passi=120, seme=5, tau_a="2.0"):
    db = os.path.join(SC, "_sfb_%s.pkl" % tag)
    cmd = [sys.executable, os.path.join(ROOT, "soliton_simulator.py"),
           "--batch", "--nmasse", "3", "--sep", "8", "--seed", str(seme),
           "--passi", str(passi), "--ogni", str(passi), "--db-ogni", str(passi),
           "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto", "--chi-core",
           "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2", "--fork-su2-mem",
           "--cs-dinamico"] + (["--tau-a", tau_a] if tau_a else []) + list(extra) + [
           "--csv", os.path.join(SC, "_sfb_%s.csv" % tag), "--sync-db", db, "--db-cleanup"]
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return p, (pickle.load(open(db, "rb"))["attrs"] if (p.returncode == 0 and os.path.exists(db)) else None)


print("=" * 118)
print("ESPERIMENTO SPIN_FEEDBACK con TAU_A = 2.0.  A/B A VARIABILE SINGOLA.")
print("=" * 118)
print("!! SPIN_FEEDBACK NON HA UN SIGILLO. Esperimento su componente NON CERTIFICATO.")
print("  NON promuove nulla, il default NON cambia.")

pA, A = gira("off", [])
pB, B = gira("on", ["--spin-feedback"])

# il RIFERIMENTO: TAU_A = 50, cioe' SENZA --tau-a. (Nella prima versione di questo script la
# funzione `gira` aggiungeva SEMPRE `--tau-a 2.0`, quindi il "riferimento" non era tale e il
# conteggio dei nodi restava `None`: bug mio, corretto passando `tau_a=None`.)
pR, R = gira("rif", [], tau_a=None)

print("\n--- E4 [A8]: il feedback e' DAVVERO applicato?  (la domanda che decide se l'esperimento vale) ---")
if B is None:
    print("  run B fallito: vedi E1")
else:
    for k in ("_sfb_chiamate", "_sfb_applicato", "_sfb_off", "_sfb_lift_corto", "_sfb_mask_vuota"):
        print("     %-22s OFF: %-8s   ON: %-8s" % (k, A.get(k) if A else "-", B.get(k)))
    ch, ap = B.get("_sfb_chiamate") or 0, B.get("_sfb_applicato") or 0
    # il criterio NON e' "100 %": la guardia `len(_spinor_lift) < n` scatta nel TRANSITORIO,
    # quando i nodi nuovi non hanno ancora il lift. Cio' che conta e' che il feedback sia
    # applicato nella STRAGRANDE maggioranza, non che non manchi mai.
    verdetto("E4a il feedback e' applicato (guardie solo nel transitorio)",
             ch > 0 and ap >= 0.95 * ch,
             "applicato %s su %s chiamate (%.1f %%); lift_corto %s, mask_vuota %s"
             % (ap, ch, 100.0 * ap / max(ch, 1), B.get("_sfb_lift_corto") or 0,
                B.get("_sfb_mask_vuota") or 0))
    cm, fm, rp = B.get("_sfb_amp_coppia"), B.get("_sfb_amp_fb"), B.get("_sfb_rapporto_max")
    som, nn_ = B.get("_sfb_rapporto_som") or 0.0, B.get("_sfb_rapporto_n") or 0
    rmed = som / nn_ if nn_ else float("nan")
    print("     rapporto |feedback|/|coppia| (mediane dello STESSO passo):")
    print("        MEDIO su %d passi : %.6g       <- e' questo il numero da leggere" % (nn_, rmed))
    print("        MASSIMO           : %.6g       (un solo passo, non il tipico)" % (rp or 0))
    print("     [A3c] i due MAX separati (coppia %.4g, feedback %.4g) sono presi in passi DIVERSI:"
          % (cm or 0, fm or 0))
    print("           NON hanno quoziente, e non vanno divisi fra loro.")
    verdetto("E4b il contributo NON e' trascurabile (rapporto MEDIO)",
             rmed > 1e-3, "feedback/coppia medio = %.6g" % rmed)


print("\n--- E1: STABILITA'  [BLOCCANTE] ---")
print("  rc: OFF=%s  ON=%s" % (pA.returncode, pB.returncode))
if pB.returncode != 0 or B is None:
    print((pB.stderr or "")[-1500:])
    verdetto("E1 il run con SPIN_FEEDBACK completa", False, "rc=%s" % pB.returncode)
else:
    print("  %-10s %-26s %-26s" % ("campo", "OFF (NaN, max|.|)", "ON (NaN, max|.|)"))
    for k in ("psi", "omega_s", "d", "d0", "phivel"):
        def f(X):
            a = np.asarray(X.get(k))
            nn = int(np.sum(~np.isfinite(a)))
            mx = float(np.max(np.abs(a[np.isfinite(a)]))) if np.any(np.isfinite(a)) else float("nan")
            return "%d, %.4g" % (nn, mx)
        print("  %-10s %-26s %-26s" % (k, f(A), f(B)))
    nan_tot = sum(int(np.sum(~np.isfinite(np.asarray(B[k])))) for k in ("psi", "omega_s", "d", "d0", "phivel"))
    verdetto("E1a nessun NaN/inf con feedback ON  [BLOCCANTE]", nan_tot == 0, "NaN/inf: %d" % nan_tot)
    nb = np.asarray(B.get("_nb"), float)
    nn = np.linalg.norm(nb, axis=1) if nb.ndim == 2 else np.array([1.0])
    verdetto("E1b |nb| = 1", float(np.max(np.abs(nn - 1.0))) < 1e-9,
             "max| |nb|-1 | = %.3e" % np.max(np.abs(nn - 1.0)))
    d0 = np.asarray(B["d0"], float)
    verdetto("E1c d0 > 0", bool(np.all(d0 > 0)), "min d0 %.6g" % d0.min())
    verdetto("E1d tau_p stabile", (B.get("_taup_cfl_max") or 9) < 1.0,
             "_taup_cfl_max ON=%s  OFF=%s" % (B.get("_taup_cfl_max"), A.get("_taup_cfl_max")))

    print("\n--- E2: IL CONTEGGIO DEI NODI  [il numero che decide] ---")
    nA = len(np.asarray(A["psi"])); nB = len(np.asarray(B["psi"]))
    nR = len(np.asarray(R["psi"])) if R is not None else None
    print("  TAU_A=50 (riferimento)     : %s nodi" % nR)
    print("  TAU_A=2.0, feedback OFF    : %d nodi   (%.1f %% del riferimento)"
          % (nA, 100.0 * nA / nR if nR else float("nan")))
    print("  TAU_A=2.0, feedback ON     : %d nodi   (%.1f %% del riferimento)"
          % (nB, 100.0 * nB / nR if nR else float("nan")))
    if nR:
        pA_ = 100.0 * (nA - nR) / nR
        pB_ = 100.0 * (nB - nR) / nR
        print("  variazione contro il riferimento:  OFF %+.1f %%    ON %+.1f %%" % (pA_, pB_))
        print("  -> la perdita si RIDUCE? %s" % ("SI', da %+.1f a %+.1f" % (pA_, pB_) if pB_ > pA_
                                                 else "NO, da %+.1f a %+.1f" % (pA_, pB_)))

    print("\n--- E3: le stesse grandezze del run A ---")
    for k in ("psi", "d0"):
        a = float(np.max(np.abs(np.asarray(A[k])))); b = float(np.max(np.abs(np.asarray(B[k]))))
        r = float(np.max(np.abs(np.asarray(R[k])))) if R is not None else float("nan")
        print("  %-5s max: TAU_A=50 %.5g   OFF %.5g (x%.3g)   ON %.5g (x%.3g)"
              % (k, r, a, a / r if r else float("nan"), b, b / r if r else float("nan")))
    for eti, X, ta in (("OFF", A, 2.0), ("ON ", B, 2.0)):
        eta = np.asarray(X.get("eta"), float)[:len(np.asarray(X["psi"]))]
        ramp = np.minimum(1.0, eta / ta)
        print("  ramp %s: mediana %.5g   p05 %.5g   p95 %.5g" % (eti, np.median(ramp),
                                                                 np.percentile(ramp, 5),
                                                                 np.percentile(ramp, 95)))

print("\n" + "=" * 118)
ok = sum(esiti)
print("ESPERIMENTO: %d/%d PASS" % (ok, len(esiti)))
print("""
LE QUATTRO LETTURE, FISSATE PRIMA
  la perdita di nodi si RIDUCE in modo netto  -> l'ipotesi REGGE. Ma NON promuovere: SPIN_FEEDBACK
                                                va SIGILLATO prima.
  la perdita resta UGUALE                     -> l'ipotesi CADE, e il candidato e' Z10: TAU_A e'
                                                ANCHE la vita media della memoria spinoriale.
  peggiora o diverge                          -> la trasmissione e' staccata per una ragione che
                                                nessuno aveva scritto. REPERTO.
  il contributo e' TRASCURABILE (E4)          -> ESPERIMENTO NULLO. Si dice, e non si interpretano
                                                le altre differenze.""")
