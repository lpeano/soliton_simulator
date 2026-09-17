# -*- coding: utf-8 -*-
"""ESPERIMENTO: `TAU_A = 2.0` nel ramo DETERMINISTICO. Era una cura, o no?

LA DOMANDA: la testimonianza di Luca dice che `TAU_A = 50` fu scelto *«in sessioni precedenti,
prima di creare il repository, per non far esplodere tutto»*. Da git NON e' verificabile (il valore
c'e' dal primo commit che aggiunge il file, `670310f`, e nessun commit lo ha mai cambiato).
QUESTO ESPERIMENTO LA METTE ALLA PROVA.

⚠ COSA SI STA CREANDO: `TAU_A = 2.0` CON `G_PH = 3e-3` non e' ne' il canonico (che vuole
`G_PH = 0.15`) ne' il deterministico originale. E' UNA TERZA COMBINAZIONE, MAI VALIDATA.

S1 [BLOCCANTE] stabilita': no NaN/inf/runaway, |nb| = 1, inerzia > 0, tau_p_loc > 0, e i sotto-passi
               CFL (se esplodono, il sistema sta compensando per non divergere).
S2             la firma di Z9: `ramp` mediano ai passi 1/60/120 e il passo per ramp = 1.

LE TRE LETTURE, FISSATE PRIMA:
  DIVERGE                     -> la testimonianza e' CONFERMATA. E' un RISULTATO, non un fallimento.
  REGGE e ramp matura nei run -> la compensazione e' SCADUTA. Si discute, NON si promuove.
  REGGE con segni di STRESS   -> si riportano senza minimizzarli. "Non esplode" non e' "sta bene".
ASCII PURO.
"""
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
    print("[%s] %-48s %s" % ("PASS" if ok else "FAIL", nome, misura))


def gira(tag, extra, passi=120, seme=5):
    db = os.path.join(SC, "_exp_%s.pkl" % tag)
    cmd = [sys.executable, os.path.join(ROOT, "soliton_simulator.py"),
           "--batch", "--nmasse", "3", "--sep", "8", "--seed", str(seme),
           "--passi", str(passi), "--ogni", str(passi), "--db-ogni", str(passi),
           "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto", "--chi-core",
           "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2", "--fork-su2-mem",
           "--cs-dinamico"] + list(extra) + [
           "--csv", os.path.join(SC, "_exp_%s.csv" % tag), "--sync-db", db, "--db-cleanup"]
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return p, (pickle.load(open(db, "rb"))["attrs"] if (p.returncode == 0 and os.path.exists(db)) else None)


print("=" * 118)
print("ESPERIMENTO --tau-a 2.0 nel DETERMINISTICO.  G_PH e CALORE_INIT NON toccati.")
print("=" * 118)

p50, A = gira("tau50", [])                      # il default: TAU_A = 50
p02, B = gira("tau02", ["--tau-a", "2.0"])      # l'esperimento

print("\n--- il flag e' arrivato? ---")
for l in (p02.stdout or "").splitlines():
    if "tau-a" in l:
        print("   " + l.strip()[:150])
if "[tau-a]" not in (p02.stdout or ""):
    print("   !! l'avviso del flag NON compare: l'override potrebbe essere INERTE. Verificare.")

print("\n--- S1: STABILITA'  [BLOCCANTE] ---")
print("  run TAU_A=50 : rc=%s      run TAU_A=2.0 : rc=%s" % (p50.returncode, p02.returncode))
if p02.returncode != 0:
    print("  IL RUN CON TAU_A=2.0 E' FALLITO. Coda dell'errore:")
    print((p02.stderr or "")[-2000:])
    verdetto("S1 il run con TAU_A=2.0 completa", False, "rc=%s" % p02.returncode)
elif B is None:
    verdetto("S1 il run con TAU_A=2.0 completa", False, "nessun DB prodotto")
else:
    def san(X, eti):
        out = {}
        for k in ("psi", "omega_s", "d", "d0", "phivel"):
            v = X.get(k)
            if v is None:
                out[k] = "assente"; continue
            a = np.asarray(v)
            nn = int(np.sum(~np.isfinite(a)))
            out[k] = (nn, float(np.max(np.abs(a[np.isfinite(a)]))) if np.any(np.isfinite(a)) else float("nan"))
        return out

    s50, s02 = san(A, "50"), san(B, "2.0")
    print("  %-12s %-28s %-28s" % ("campo", "TAU_A=50 (NaN, max|.|)", "TAU_A=2.0 (NaN, max|.|)"))
    for k in ("psi", "omega_s", "d", "d0", "phivel"):
        f = lambda t: ("%d, %.4g" % t) if isinstance(t, tuple) else t
        print("  %-12s %-28s %-28s" % (k, f(s50[k]), f(s02[k])))
    nan_tot = sum(t[0] for t in s02.values() if isinstance(t, tuple))
    verdetto("S1a nessun NaN/inf con TAU_A=2.0  [BLOCCANTE]", nan_tot == 0,
             "NaN/inf totali: %d" % nan_tot)
    nb = np.asarray(B.get("_nb"), float)
    nn = np.linalg.norm(nb, axis=1) if nb.ndim == 2 else np.array([1.0])
    verdetto("S1b |nb| = 1", float(np.max(np.abs(nn - 1.0))) < 1e-9,
             "max| |nb|-1 | = %.3e" % np.max(np.abs(nn - 1.0)))
    d0 = np.asarray(B["d0"], float); d = np.asarray(B["d"], float)
    verdetto("S1c d0 > 0 e d > 0", bool(np.all(d0 > 0) and np.all(d > 0)),
             "min d0 %.6g, min d %.6g" % (d0.min(), d.min()))
    cfl = B.get("_taup_cfl_max")
    verdetto("S1d tau_p stabile (dt_e/tau_p < 1)", cfl is not None and float(cfl) < 1.0,
             "_taup_cfl_max = %s   (con TAU_A=50: %s)" % (cfl, A.get("_taup_cfl_max")))
    # RUNAWAY: confronto delle ampiezze fra i due bracci
    om50 = np.asarray(A.get("omega_s"), float); om02 = np.asarray(B.get("omega_s"), float)
    m50 = float(np.median(np.abs(om50))) if om50.size else float("nan")
    m02 = float(np.median(np.abs(om02))) if om02.size else float("nan")
    print("  |omega_s| mediana : TAU_A=50 -> %.6g     TAU_A=2.0 -> %.6g   (rapporto %.3g)"
          % (m50, m02, m02 / m50 if m50 else float("nan")))
    print("  nodi finali       : TAU_A=50 -> %d           TAU_A=2.0 -> %d"
          % (len(np.asarray(A["psi"])), len(np.asarray(B["psi"]))))
    verdetto("S1e nessun RUNAWAY di omega_s (entro 100x)",
             np.isfinite(m02) and (m02 < 100 * m50 if m50 else False),
             "rapporto %.4g" % (m02 / m50 if m50 else float("nan")))

    print("\n--- S2: LA FIRMA DI Z9 ---")
    print("  (calcolata da eta finale: ramp = min(1, eta/TAU_A))")
    for eti, X, ta in (("TAU_A=50 ", A, 50.0), ("TAU_A=2.0", B, 2.0)):
        eta = np.asarray(X.get("eta"), float)
        n = len(np.asarray(X["psi"]))
        eta = eta[:n]
        ramp = np.minimum(1.0, eta / ta)
        cres = float(np.median(eta)) / 120.0
        p1 = (ta / cres) if cres > 0 else float("inf")
        print("     %s  eta med %.5g   ramp med %.5g   p05 %.5g   p95 %.5g   ramp=1 al passo ~%.0f"
              % (eti, np.median(eta), np.median(ramp), np.percentile(ramp, 5),
                 np.percentile(ramp, 95), p1))
    print("     riferimento Z9 (blob a8f1b2f4, TAU_A=50): ramp med 0.0202 al passo 120, ramp=1 a ~5960")

print("\n" + "=" * 118)
ok = sum(esiti)
print("ESPERIMENTO: %d/%d PASS -> %s" % (ok, len(esiti), "REGGE" if ok == len(esiti) else "NON REGGE"))
print("""
COME SI LEGGE -- le tre letture erano fissate PRIMA
  DIVERGE                      -> la testimonianza di Luca e' CONFERMATA: TAU_A = 50 era una CURA,
                                  e il difetto che curava ESISTE ANCORA. E' il risultato piu'
                                  informativo dei tre, e NON e' un fallimento.
  REGGE e ramp matura nei run  -> la compensazione e' SCADUTA. Si discute, NON si promuove.
  REGGE con segni di STRESS    -> si riportano senza minimizzarli: "non esplode" non e' "sta bene".
E in ogni caso questo NON e' categoria D, NON e' una correzione, e il DEFAULT NON CAMBIA.""")
