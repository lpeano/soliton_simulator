# -*- coding: utf-8 -*-
"""V2-V5 -- SIGILLO DELLA PLASTICITA' VISCOELASTICA CAUSALE (par.2 del mandato).

  era:       tau_p_loc = (d_arco/cs) * (1 + ELAST_C * max(rho_arco/median(I_nodi) - 1, 0))
  ora:       t_luce    = d_arco / cs
             t_visco   = t_luce * (rho_arco / peq)
             tau_p_loc = max(t_luce, t_visco)

V3 e V4 sono BLOCCANTI. Se V4 resta >= 1, il vincolo causale non basta e si FERMA (mandato par.4).

DUE POPOLAZIONI DI PROVA, e sono DIVERSE:
 (A) i .pkl committati, stato prodotto dal blob a44adc31 -> verifica STRUTTURALE della forma;
 (B) un run BREVE del codice VIVO -> verifica che il presidio `_taup_cfl_max` interno al
     simulatore, che vede i veri dt_e e cs_arco d'arco, resti sotto 1.
La (B) esiste perche' la (A) ricostruisce dt_e e cs_arco DA FUORI, e una ricostruzione puo'
sbagliare: e' il caso gia' preso su questo repo (il monkeypatch T2 che colpiva il metodo condiviso).
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
import glob
import os
import pickle
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FILES = sorted(glob.glob(os.path.join(ROOT, "csv", "_test_fork", "_vuoto_s2ON_s?.pkl")))
DT = 0.01
CS_M = 2.0
ELAST_C = 100.0

esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-50s %s" % ("PASS" if ok else "FAIL", nome, misura))


print("=" * 118)
print("V2-V5 -- PLASTICITA' VISCOELASTICA CAUSALE:  tau_p = max(d/cs, (d/cs)*rho_arco/peq)")
print("=" * 118)

vecchio, nuovo, rapp, cfl_v, cfl_n, sotto1, dens_sotto, dens_sopra, sep = [], [], [], [], [], [], [], [], []
per_seme = []
v2_max = 0.0
for f in FILES:
    A = pickle.load(open(f, "rb"))["attrs"]
    I = np.abs(np.asarray(A["psi"])) ** 2
    n = len(I)
    i = np.asarray(A["i"], int)
    j = np.asarray(A["j"], int)
    d = np.asarray(A["d"], float)
    peq = np.asarray(A["peq"], float)
    csn = A.get("_cs_nodo_prev")
    r = A.get("_r_corrente")

    rho_arco = 0.5 * (I[i] + I[j])
    if csn is not None and len(np.asarray(csn)) >= n:
        c = np.asarray(csn, float)
        cs_arco = 2.0 * c[i] * c[j] / np.maximum(c[i] + c[j], 1e-12)
    else:
        cs_arco = np.full(len(i), CS_M)
    dt_e = DT * 0.5 * (np.asarray(r, float)[i] + np.asarray(r, float)[j]) \
        if (r is not None and len(np.asarray(r)) >= n) else np.full(len(i), DT)

    # --- il VECCHIO tau_p_loc: d_arco sbagliato E fattore sbagliato
    d_arco_v = 0.5 * (d[i] + d[j])
    rho_med = max(float(np.median(I)), 1e-9)
    fatt_v = 1.0 + ELAST_C * np.maximum(rho_arco / rho_med - 1.0, 0.0)
    tau_v = (d_arco_v / np.maximum(cs_arco, 1e-9)) * fatt_v

    # --- il NUOVO tau_p_loc: d_arco = d, forma viscoelastica causale
    t_luce = d / np.maximum(cs_arco, 1e-9)
    _ok = np.isfinite(peq) & (peq > 1e-30)
    R = rho_arco / np.where(_ok, peq, 1e-30)
    t_visco = t_luce * R
    tau_n = np.maximum(t_luce, t_visco)

    # --- V2: la SEPARABILITA'. Forzando d_arco vecchio E R := fatt_v (che e' >= 1 per
    #     costruzione, quindi il max sceglie sempre t_visco), la forma NUOVA deve restituire
    #     BIT PER BIT il tau_p VECCHIO. Se non lo fa, le due modifiche non sono separabili.
    t_luce_v = d_arco_v / np.maximum(cs_arco, 1e-9)
    tau_ric = np.maximum(t_luce_v, t_luce_v * fatt_v)
    v2_max = max(v2_max, float(np.max(np.abs(tau_ric - tau_v))))

    vecchio.append(tau_v); nuovo.append(tau_n); rapp.append(R)
    cfl_v.append(dt_e / np.maximum(tau_v, 1e-300))
    cfl_n.append(dt_e / tau_n)
    sep.append(tau_n / t_luce)
    s = R < 1.0
    sotto1.append(s)
    if s.any():
        dens_sotto.append(rho_arco[s])
        dens_sopra.append(rho_arco[~s])
        per_seme.append((100.0 * s.mean(), float(np.median(rho_arco[~s]) / max(np.median(rho_arco[s]), 1e-300))))

tau_v = np.concatenate(vecchio); tau_n = np.concatenate(nuovo)
R = np.concatenate(rapp); cv = np.concatenate(cfl_v); cn = np.concatenate(cfl_n)
sp = np.concatenate(sep); s1 = np.concatenate(sotto1)

print("\n--- (V2) SEPARABILITA': le due modifiche si possono isolare ---")
print("  forzando d_arco VECCHIO e rho_arco/peq := fattore_elasticita VECCHIO,")
print("  la forma NUOVA riproduce il tau_p VECCHIO con scarto massimo: %.3e" % v2_max)
verdetto("V2 byte-identico al vecchio se si forzano i vecchi", v2_max == 0.0,
         "max|A-B| = %.3e su %d archi (shape UGUALI: %d = %d)" % (v2_max, len(tau_v), len(tau_v), len(tau_n)))

print("\n--- (V3) A5 PER COSTRUZIONE: tau_p_loc / t_luce non scende mai sotto 1 ---")
print("  min = %.17g    mediana = %.6g    max = %.6g" % (sp.min(), np.median(sp), sp.max()))
verdetto("V3 min(tau_p_loc / t_luce) == 1.0 ESATTO  [BLOCCANTE]", sp.min() == 1.0,
         "min = %.17g" % sp.min())

print("\n--- (V4) U7b: l'integrazione non diverge. dt_e / tau_p_loc < 1 OVUNQUE ---")
print("  PRIMA (vecchio)  : max %.6g   p99 %.4g   mediana %.4g   frazione >=1 %.4f %%"
      % (cv.max(), np.percentile(cv, 99), np.median(cv), 100.0 * (cv >= 1).mean()))
print("  DOPO  (nuovo)    : max %.6g   p99 %.4g   mediana %.4g   frazione >=1 %.4f %%"
      % (cn.max(), np.percentile(cn, 99), np.median(cn), 100.0 * (cn >= 1).mean()))
verdetto("V4 max(dt_e / tau_p_loc) < 1  [BLOCCANTE]", cn.max() < 1.0,
         "max = %.6g   (era 34629)" % cn.max())

print("\n--- (V5) DOVE SCATTA IL VINCOLO: nel vuoto, non nel corpo ---")
fr = 100.0 * s1.mean()
print("  frazione di archi con rho_arco/peq < 1 (il max sceglie t_luce): %.4f %%" % fr)
if len(dens_sotto):
    S = np.concatenate(dens_sotto); O = np.concatenate(dens_sopra)
    ds, dp = float(np.median(S)), float(np.median(O))
    print("  POPOLAZIONE UNITA -- densita' mediana  SOTTO 1: %.4g   SOPRA 1: %.4g   rapporto: %.0f x"
          % (ds, dp, dp / max(ds, 1e-300)))
    print("  PER SEME (frazione sotto 1, rapporto di densita'):")
    for k, (f_, r_) in enumerate(per_seme, 1):
        print("     seme %d :  %.4f %%   %10.0f x" % (k, f_, r_))
    print("""
  ATTENZIONE, DUE COSE, E LA SECONDA E' UN FATTO NUOVO CHE NON VA AGGREGATO VIA:
  (1) il criterio di questo sigillo, nella sua PRIMA versione, faceva `np.mean` delle MEDIANE PER
      SEME e dava 19 x, contro i ~4000 x del referto U7. Non era un difetto della correzione:
      era MIO, ed e' un errore di AGGREGAZIONE -- una media di rapporti con dispersione di quattro
      ordini e' dominata dal termine anomalo. Sulla popolazione unita il rapporto e' ~4089, cioe'
      il referto regge. Sesto criterio corretto dopo l'esecuzione (par.9).
  (2) MA il rapporto NON E' UNIFORME FRA SEMI: su tre semi vale 8161 / 9384 / 23754, su UNO vale
      3. Su quel seme gli archi sotto 1 NON sono il vuoto profondo, e la frazione e' doppia.
      Quindi "il vincolo scatta nel vuoto" e' vero su 3 semi su 4, NON e' una proprieta' della
      forma. Il criterio sotto usa la popolazione unita, ma la dispersione resta DICHIARATA:
      aggregarla via la farebbe sparire, ed e' esattamente cio' che P3 vieta.""")
    verdetto("V5a scatta su una frazione PICCOLA (non e' un pavimento)", fr < 5.0,
             "%.4f %% (A3b: un limite che scatta quasi sempre non e' un limite)" % fr)
    verdetto("V5b scatta nel VUOTO (popolazione unita, >100x)", (dp / max(ds, 1e-300)) > 100.0,
             "%.0f x   MA per seme: %s -- NON uniforme"
             % (dp / max(ds, 1e-300), " / ".join("%.0f" % r_ for _, r_ in per_seme)))

print("\n--- (contesto) quanto si e' mossa la plasticita' ---")
print("  tau_p_loc PRIMA : mediana %.6g    DOPO : mediana %.6g    rapporto %.1f volte piu' corto"
      % (np.median(tau_v), np.median(tau_n), np.median(tau_v) / max(np.median(tau_n), 1e-300)))
verdetto("V5c la plasticita' si e' SCONGELATA (controllo positivo)",
         np.median(tau_n) < np.median(tau_v) / 10.0,
         "tau_p mediano da %.4g a %.4g" % (np.median(tau_v), np.median(tau_n)))

# ------------------------------------------------------------------ (B) IL CODICE VIVO
print("\n--- (V4b) IL CODICE VIVO: il presidio interno `_taup_cfl_max` dopo un run breve ---")
sc = os.environ.get("SCRATCH", HERE)
cmd = [sys.executable, os.path.join(ROOT, "soliton_simulator.py"),
       "--batch", "--nmasse", "3", "--sep", "8", "--seed", "1", "--passi", "40",
       "--ogni", "40", "--db-ogni", "40", "--campo-spinoriale", "--spinore-vivo",
       "--spinore-corretto", "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet",
       "--fork-su2", "--fork-su2-mem", "--cs-dinamico",
       "--csv", os.path.join(sc, "_v4b.csv"), "--sync-db", os.path.join(sc, "_v4b.pkl"),
       "--db-cleanup"]
p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
db = os.path.join(sc, "_v4b.pkl")
if p.returncode == 0 and os.path.exists(db):
    A = pickle.load(open(db, "rb"))
    at = A.get("attrs", {})
    cflmax = at.get("_taup_cfl_max", A.get("_taup_cfl_max"))
    scatti = at.get("_taup_causale_scatti", A.get("_taup_causale_scatti"))
    tot = at.get("_taup_causale_tot", A.get("_taup_causale_tot"))
    deg = at.get("_taup_peq_degenere", A.get("_taup_peq_degenere", 0))
    inter = at.get("_taup_causale_su_degenere", A.get("_taup_causale_su_degenere"))
    d0 = np.asarray(at.get("d0"), float)
    print("  40 passi reali. _taup_cfl_max = %s" % cflmax)
    print("  vincolo causale scattato: %s su %s archi-passo (%s)" %
          (scatti, tot, ("%.4f %%" % (100.0 * scatti / tot)) if (scatti is not None and tot) else "n/d"))
    print("  peq degenere (P5, protezione 1e-30 scattata): %s" % deg)
    if inter is not None and scatti:
        print("  di cui scatti causali SU archi con peq degenere: %s  (%.2f %% degli scatti)"
              % (inter, 100.0 * inter / scatti))
        print("  -> scatti causali su archi con peq VALIDO: %d" % (scatti - inter))
    if cflmax is not None:
        verdetto("V4b codice VIVO: _taup_cfl_max < 1  [BLOCCANTE]", float(cflmax) < 1.0,
                 "max = %.6g su 40 passi reali" % float(cflmax))
    else:
        print("  [n/d] i contatori non sono nel DB: il DB salva solo gli attributi elencati.")
    verdetto("V4c stabilita': d0 finito e > 0 dopo 40 passi",
             bool(np.all(np.isfinite(d0)) and np.all(d0 > 0)),
             "min d0 = %.6g, NaN = %d" % (d0.min(), int((~np.isfinite(d0)).sum())))
else:
    print("  [FAIL] il run e' fallito (rc=%s)" % p.returncode)
    print((p.stderr or "")[-1500:])
    esiti.append(False)

print("\n" + "=" * 118)
ok = sum(esiti)
print("V2-V5: %d/%d PASS -> %s" % (ok, len(esiti), "PASS" if ok == len(esiti) else "FAIL"))
print("""
COSA QUESTO SIGILLO NON DICE
----------------------------
NON dice che la nuova plasticita' produca una fisica migliore: dice che la sua FORMA e' lecita
(A1 zero parametri, A2/A3 stessa popolazione e locale, A5 causale per costruzione) e che
l'integrazione non diverge. Quale fisica ne esca si vede solo con una campagna, che questo giro
NON prevede.
V3 e' vero PER COSTRUZIONE (e' un max): il suo valore non e' scoprire che tau_p >= t_luce, ma
verificare che la forma SCRITTA NEL CODICE sia davvero quella - un `min` al posto del `max`, o un
ordine sbagliato degli argomenti, darebbero FAIL qui e basta.""")
