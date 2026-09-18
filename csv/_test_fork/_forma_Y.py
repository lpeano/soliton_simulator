# -*- coding: utf-8 -*-
"""Y O DISCO? -- l'anisotropia angolare della regione densa. **NESSUN RUN NUOVO, SOLA LETTURA.**

Progettazione e QUATTRO LETTURE fissate PRIMA: doc/TASK_HISTORY/2026-09-18_forma-Y-o-disco.md (4cf1817)

⚠ IN TESTA: `--tau-luce` HA IL SIGILLO FALLITO (par.0), `--chi-basc` attivo, **UN SEME**,
**NESSUN VERDETTO DI FISICA, NESSUNA IDENTIFICAZIONE.**
⚠ E l'osservazione «in mezzo forma una Y» e' **VISIVA**: questa misura serve a METTERLA ALLA PROVA,
non a confermarla.

LA SOGLIA E' DERIVATA, NON SCELTA (A1): `rho_spin > k * mean(rho_spin)` -- **sopra il livello di
vuoto della STESSA grandezza**, l'analogo di `lambda_vuoto = mean(|psi|^2)` (`:486-494`) applicato a
`rho_spin` invece che a `I`. **NON uso `lambda_vuoto` stesso: sono due campi diversi, e confrontarli
sarebbe un errore di popolazione (A3c).** Si riporta a **k = 1 E k = 10**: se la forma cambia con la
soglia, **la forma non e' un fatto**.

IL VALORE SOTTO IPOTESI NULLA, senza cui l'istogramma e' un disegno:
  `A_m = |Sum_k rho_k e^{i m theta_k}| / Sum_k rho_k`  vale **~1/sqrt(N_eff)** per punti CASUALI,
  con `N_eff = (Sum rho)^2 / Sum rho^2`. **Si riporta SEMPRE accanto ad A_m.**

LA TRAPPOLA: `A_3` grande puo' venire DALLE TRE MASSE. Si riportano SEMPRE due valori -- **TUTTI** i
nodi densi e **SOLO LA REGIONE INTERNA** (`r < R_anello(t)/2`, `R_anello` MISURATO).
ASCII PURO.
"""
import glob
import os
import pickle
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import _presidio
_presidio.avvia(__file__)

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
os.chdir(ROOT)
D = sys.argv[1] if len(sys.argv) > 1 else os.path.join("csv", "_test_fork", "_gvideo")
NM = int(sys.argv[2]) if len(sys.argv) > 2 else 3
NBIN = 24

print("=" * 116)
print("Y O DISCO? -- anisotropia angolare della regione densa   [%s, %d masse]" % (D, NM))
print("=" * 116)
print("""  ⚠ `--tau-luce` HA IL SIGILLO FALLITO (par.0): ramo NON CERTIFICATO. `--chi-basc` attivo.
  ⚠ UN SEME. NESSUN VERDETTO DI FISICA, NESSUNA IDENTIFICAZIONE.
  ⚠ L'osservazione «forma una Y» e' VISIVA: qui si MISURA, non si conferma.""")

S = {}
for p in sorted(glob.glob(os.path.join(D, "frame_*.pkl"))):
    a = pickle.load(open(p, "rb"))["attrs"]
    S[int(a.get("_db_step", -1))] = a
F = sorted(S)
if not F:
    print("  NESSUNO snapshot in %s" % D); sys.exit(1)
N0 = len(S[F[0]]["pos"])
print("\n  istanti (FRAME): %s   n0 = %d" % (F, N0))


def Am(th, w, m):
    W = float(np.sum(w))
    if W <= 0:
        return float("nan")
    return float(np.abs(np.sum(w * np.exp(1j * m * th))) / W)


def neff(w):
    s1 = float(np.sum(w)); s2 = float(np.sum(w * w))
    return (s1 * s1 / s2) if s2 > 0 else 0.0


# ------------------------------------------------------------------ passo 0: planarita'
print("\n--- PASSO 0: LA SCENA E' PLANARE? (se no, proiettare e' gia' un'assunzione) ---")
print("  %-8s %-14s %-14s %-14s" % ("frame", "|z| mediano", "r mediano", "|z|/r"))
for f in F:
    P = np.asarray(S[f]["pos"])[:len(S[f]["pos"])]
    z = np.abs(P[:, 2]); r = np.linalg.norm(P[:, :2], axis=1)
    print("  %-8d %-14.5g %-14.5g %-14.5g" % (f, np.median(z), np.median(r),
                                              np.median(z) / max(np.median(r), 1e-12)))

# [CORREZIONE 2026-09-18, dopo il primo giro] LA SOGLIA SULLA MEDIA E' INUTILIZZABILE PER
# `rho_spin`: MISURATO al frame 400, `media = 1.44e+01` contro `mediana = 6.42e-03`, cioe' un
# RAPPORTO 2249. La media NON e' il livello di vuoto di questo campo: E' UNA STATISTICA DELLA CODA,
# e selezionava SOLO i 1479 nodi estremi -- tutti a `r ~ 7.7`, cioe' L'ANELLO. Ecco perche' i nodi
# "interni densi" risultavano ZERO: non e' un fatto sul sistema, era la soglia.
# LA SOGLIA GIUSTA E' SULLA MEDIANA, che per questo campo E' il valore tipico. Si riportano TRE
# decadi (1x, 10x, 100x la mediana) PIU' la media come CONTROESEMPIO dichiarato.
for K, BASE in ((1.0, "med"), (10.0, "med"), (100.0, "med"), (1.0, "media")):
    print("\n" + "=" * 116)
    print("SOGLIA  rho_spin > %.0f x %s(rho_spin)%s" % (
        K, "median" if BASE == "med" else "mean",
        "" if BASE == "med" else "   <- ⚠ CONTROESEMPIO: la media e' dominata dalla CODA (media/mediana ~ 2249)"))
    print("=" * 116)
    print("  %-7s %-7s %-8s %-8s %-9s | %-9s %-9s %-9s %-9s | %-9s %-10s"
          % ("frame", "densi", "interni", "R_anel", "N_eff", "A_1", "A_2", "A_3", "A_6", "NULLO", "contrasto"))
    for f in F:
        a = S[f]; n = len(a["pos"])
        P = np.asarray(a["pos"])[:n]
        R = np.linalg.norm(P[:, :2], axis=1)
        th = np.arctan2(P[:, 1], P[:, 0])
        rs = np.asarray(a.get("rho_spin", np.zeros(n)), float)[:n]
        mrs = float(np.median(rs)) if BASE == "med" else float(np.mean(rs))
        dens = rs > K * mrs
        RA = float(np.median(R[:N0]))
        interni = dens & (R < RA / 2.0)
        for eti, sel in (("TUTTI", dens), ("INTERNI", interni)):
            if sel.sum() < 10:
                print("  %-7d %-7s (troppo pochi: %d)" % (f, eti, int(sel.sum()))); continue
            w = rs[sel]; t = th[sel]
            ne = neff(w); nullo = 1.0 / np.sqrt(max(ne, 1.0))
            h, _ = np.histogram(t, bins=NBIN, range=(-np.pi, np.pi), weights=w)
            contr = (h.max() - h.min()) / max(h.mean(), 1e-30)
            print("  %-7s %-7d %-8d %-8.3f %-9.1f | %-9.4f %-9.4f %-9.4f %-9.4f | %-9.4f %-10.3f"
                  % ((str(f) + " " + eti)[:7], int(dens.sum()), int(interni.sum()), RA, ne,
                     Am(t, w, 1), Am(t, w, 2), Am(t, w, 3), Am(t, w, 6), nullo, contr))

# ------------------------------------------------------------------ istogramma esplicito
print("\n--- L'ISTOGRAMMA ANGOLARE della REGIONE INTERNA (soglia 1x), ultimo istante ---")
f = F[-1]; a = S[f]; n = len(a["pos"])
P = np.asarray(a["pos"])[:n]; R = np.linalg.norm(P[:, :2], axis=1)
th = np.arctan2(P[:, 1], P[:, 0]); rs = np.asarray(a["rho_spin"], float)[:n]
RA = float(np.median(R[:N0]))
sel = (rs > 10.0 * np.median(rs)) & (R < RA / 2.0)   # 10x la MEDIANA, non la media
if sel.sum() >= 10:
    h, b = np.histogram(th[sel], bins=NBIN, range=(-np.pi, np.pi), weights=rs[sel])
    hm = h / max(h.mean(), 1e-30)
    att = [np.degrees(2 * np.pi * k / NM) for k in range(NM)]
    print("  frame %d, %d nodi. Angoli delle masse: %s" % (f, int(sel.sum()),
                                                           ", ".join("%.0f" % x for x in att)))
    for k in range(NBIN):
        c = np.degrees(0.5 * (b[k] + b[k + 1]))
        print("    %+7.1f deg  %-8.3f %s" % (c, hm[k], "#" * int(min(hm[k] * 20, 70))))
else:
    print("  troppi pochi nodi interni: %d" % int(sel.sum()))

# ------------------------------------------------------------------ controllo geometrico
print("\n--- CONTROLLO GEOMETRICO (⚠ NON discrimina da solo: un disco E una Y simmetrica danno lambda1~lambda2) ---")
print("  %-8s %-12s %-12s %-12s" % ("frame", "R_gir", "R_disco_eq", "lambda1/lambda2"))
for f in F:
    a = S[f]; n = len(a["pos"])
    P = np.asarray(a["pos"])[:n, :2]; R = np.linalg.norm(P, axis=1)
    rs = np.asarray(a.get("rho_spin", np.zeros(n)), float)[:n]
    RA = float(np.median(R[:N0]))
    sel = (rs > 10.0 * np.median(rs)) & (R < RA / 2.0)
    if sel.sum() < 10:
        continue
    Q = P[sel]; w = rs[sel]
    c = np.average(Q, axis=0, weights=w); Qc = Q - c
    rg = float(np.sqrt(np.average(np.sum(Qc ** 2, axis=1), weights=w)))
    M = (Qc * w[:, None]).T @ Qc / max(float(np.sum(w)), 1e-30)
    ev = np.sort(np.linalg.eigvalsh(M))[::-1]
    print("  %-8d %-12.5g %-12.5g %-12.5g" % (f, rg, np.sqrt(2.0) * rg, ev[0] / max(ev[1], 1e-30)))

print("""
  COME SI LEGGE -- le letture erano fissate PRIMA (task history 4cf1817):
    TRE picchi, A_3 BEN SOPRA IL NULLO, e la Y NELLA REGIONE INTERNA -> struttura TOPOLOGICA:
        a due masse non puo' esistere, e la predizione di Luca ha un MECCANISMO.
    istogramma PIATTO, A_3 al livello del NULLO -> e' un DISCO: l'osservazione visiva NON REGGE,
        e si scrive che l'impressione era sbagliata.
    A_3 grande SOLO con l'anello -> e' l'ARTEFATTO delle tre masse seminate.
    tre picchi che si formano e POI si dissolvono -> e' un TRANSITORIO, e va detto QUANDO.
    ⚠ E se la forma CAMBIA fra soglia 1x e 10x -> LA FORMA NON E' UN FATTO.""")
print("=" * 116)
