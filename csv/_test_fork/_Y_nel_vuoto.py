# -*- coding: utf-8 -*-
"""LA Y NEL VUOTO, E NELLA VARIAZIONE -- il complemento di `Z50`. **NESSUN RUN NUOVO.**

Letture fissate PRIMA: doc/TASK_HISTORY/2026-09-18_Y-nel-vuoto.md (0f7cea6)

⚠ IN TESTA: `--tau-luce` HA IL SIGILLO FALLITO (par.0). `--chi-basc` attivo. **UN SEME.**
**NESSUN VERDETTO DI FISICA, NESSUNA IDENTIFICAZIONE.**
⚠ E l'ispezione dei fotogrammi e' **VISIVA**: «ciano» e' un colore della colormap e **il giallo e'
SATURAZIONE, non un valore**. **Qui si FALSIFICA, non si conferma.**

`Z50` ha misurato `A_m` sul DENSO. Se i bracci sono CIANO -- interferenza DISTRUTTIVA, `|psi|` basso
-- stavano nel COMPLEMENTO. Qui si misura:
  ① IL VUOTO      `rho_spin < k * mediana`, regione interna, **NON pesato** (nullo `1/sqrt(N)`),
                  piu' un CONTROLLO pesato sul DEFICIT `(mediana - rho_spin)`.
                  ⚠ Sul vuoto pesare per `rho_spin` significa pesare per una quantita' UNIFORMEMENTE
                  MINUSCOLA: i pesi non porterebbero informazione. Per questo NON pesato.
  ② LA VARIAZIONE `Delta = rho_spin(t2) - rho_spin(t1)` sui nodi COMUNI (i primi `min(n1,n2)`: i
                  nuovi si appendono in coda), `A_m` pesato sui `Delta > 0`, regione interna.
                  **E' la misura che risponde: un canale di condensazione e' una cosa che ACCADE.**
  ③ IL TEMPO      `A_1` e `A_3` ai sei istanti, DENSO e VUOTO, col NULLO a ciascuno.
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

print("=" * 118)
print("LA Y NEL VUOTO E NELLA VARIAZIONE   [%s, %d masse]   -- NESSUN RUN NUOVO" % (D, NM))
print("=" * 118)
print("""  ⚠ `--tau-luce` HA IL SIGILLO FALLITO (par.0). UN SEME. NESSUN VERDETTO DI FISICA.
  ⚠ L'ispezione dei fotogrammi e' VISIVA: qui si FALSIFICA, non si conferma.""")

S = {}
for p in sorted(glob.glob(os.path.join(D, "frame_*.pkl"))):
    a = pickle.load(open(p, "rb"))["attrs"]
    S[int(a.get("_db_step", -1))] = a
F = sorted(S)
N0 = len(S[F[0]]["pos"])
print("\n  istanti: %s   n0 = %d   (angoli delle masse: %s)"
      % (F, N0, ", ".join("%.0f" % np.degrees(2 * np.pi * k / NM) for k in range(NM))))


def geo(f):
    a = S[f]; n = len(a["pos"])
    P = np.asarray(a["pos"])[:n]
    R = np.linalg.norm(P[:, :2], axis=1)
    th = np.arctan2(P[:, 1], P[:, 0])
    rs = np.asarray(a.get("rho_spin", np.zeros(n)), float)[:n]
    RA = float(np.median(R[:N0]))
    return n, R, th, rs, RA


def Am(th, w, m):
    W = float(np.sum(w))
    return float(np.abs(np.sum(w * np.exp(1j * m * th))) / W) if W > 0 else float("nan")


def neff(w):
    s1 = float(np.sum(w)); s2 = float(np.sum(w * w))
    return (s1 * s1 / s2) if s2 > 0 else 0.0


def riga(eti, th, w, extra=""):
    ne = neff(w); nullo = 1.0 / np.sqrt(max(ne, 1.0))
    a1, a2, a3, a6 = (Am(th, w, m) for m in (1, 2, 3, 6))
    print("  %-26s %-8d %-9.1f | %-8.4f %-8.4f %-8.4f %-8.4f | %-8.4f  %s"
          % (eti, len(th), ne, a1, a2, a3, a6, nullo,
             ("A_3/nullo %.2f  A_1/nullo %.2f" % (a3 / nullo, a1 / nullo)) + extra))


# ------------------------------------------------------------------ ①
print("\n--- ① IL VUOTO: `A_m` sui nodi RAREFATTI della regione interna ---")
print("  %-26s %-8s %-9s | %-8s %-8s %-8s %-8s | %-8s  %s"
      % ("caso", "nodi", "N_eff", "A_1", "A_2", "A_3", "A_6", "NULLO", "rapporti"))
for f in F:
    n, R, th, rs, RA = geo(f)
    med = float(np.median(rs))
    interna = R < RA / 2.0
    for k in (1.0, 0.1):
        sel = interna & (rs < k * med)
        if sel.sum() < 30:
            print("  %-26s %-8d  (meno di 30: NON SI LEGGE)" % ("f%d vuoto<%.1gx med" % (f, k), int(sel.sum())))
            continue
        riga("f%d vuoto<%.1gx med NONpes" % (f, k), th[sel], np.ones(int(sel.sum())))
        defi = np.maximum(med - rs[sel], 0.0)
        if defi.sum() > 0:
            riga("f%d   (controllo DEFICIT)" % f, th[sel], defi)

# ------------------------------------------------------------------ ②
print("\n--- ② LA VARIAZIONE: `A_m` pesato su `Delta rho_spin > 0`, regione interna ---")
print("  %-26s %-8s %-9s | %-8s %-8s %-8s %-8s | %-8s  %s"
      % ("intervallo", "nodi", "N_eff", "A_1", "A_2", "A_3", "A_6", "NULLO", "rapporti"))
for a_, b_ in zip(F[:-1], F[1:]):
    n1, R1, t1, r1, RA1 = geo(a_)
    n2, R2, t2, r2, RA2 = geo(b_)
    m = min(n1, n2)
    d = r2[:m] - r1[:m]
    interna = R2[:m] < RA2 / 2.0
    sel = interna & (d > 0)
    if sel.sum() < 30:
        print("  %-26s %-8d  (meno di 30: NON SI LEGGE)" % ("f%d->%d" % (a_, b_), int(sel.sum())))
        continue
    riga("f%d->%d  D>0  (comuni %d)" % (a_, b_, m), t2[:m][sel], d[sel])

# ------------------------------------------------------------------ ③
print("\n--- ③ L'ANDAMENTO NEL TEMPO: `A_1` e `A_3`, DENSO contro VUOTO, col nullo ---")
print("  %-8s | %-9s %-9s %-9s %-9s | %-9s %-9s %-9s %-9s"
      % ("frame", "DEN A_1", "DEN A_3", "DEN null", "DEN N_ef", "VUO A_1", "VUO A_3", "VUO null", "VUO N_ef"))
for f in F:
    n, R, th, rs, RA = geo(f)
    med = float(np.median(rs))
    interna = R < RA / 2.0
    d_sel = interna & (rs > 10.0 * med)
    v_sel = interna & (rs < med)
    out = ["%-8d |" % f]
    for sel, w in ((d_sel, rs), (v_sel, None)):
        if sel.sum() < 30:
            out.append(" %-9s %-9s %-9s %-9d" % ("-", "-", "-", int(sel.sum())))
            continue
        ww = w[sel] if w is not None else np.ones(int(sel.sum()))
        ne = neff(ww); nu = 1.0 / np.sqrt(max(ne, 1.0))
        out.append(" %-9.4f %-9.4f %-9.4f %-9.1f" % (Am(th[sel], ww, 1), Am(th[sel], ww, 3), nu, ne))
    print("".join(out))

# ------------------------------------------------------------------ istogramma del vuoto
print("\n--- L'ISTOGRAMMA ANGOLARE DEL VUOTO INTERNO (rho_spin < mediana), al frame %d ---" % F[1])
f = F[1]
n, R, th, rs, RA = geo(f)
sel = (R < RA / 2.0) & (rs < np.median(rs))
if sel.sum() >= 30:
    h, b = np.histogram(th[sel], bins=24, range=(-np.pi, np.pi))
    hm = h / max(h.mean(), 1e-30)
    print("  %d nodi. Angoli delle masse: %s"
          % (int(sel.sum()), ", ".join("%.0f" % np.degrees(2 * np.pi * k / NM) for k in range(NM))))
    for k in range(24):
        c = np.degrees(0.5 * (b[k] + b[k + 1]))
        print("    %+7.1f deg  %-7.3f %s" % (c, hm[k], "#" * int(min(hm[k] * 22, 72))))
else:
    print("  troppi pochi: %d" % int(sel.sum()))

print("""
  COME SI LEGGE -- le quattro letture erano fissate PRIMA (task history 0f7cea6):
    A_3 alto sul VUOTO ai frame precoci E sulla VARIAZIONE -> la Y esiste come struttura del campo
        rarefatto e come canale di accensione. E' UN RISULTATO.
    A_3 al NULLO in tutte e tre le varianti -> ARTEFATTO DELLA COLORMAP: l'osservazione visiva era
        sbagliata, e Z50 resta la conclusione.
    A_1 domina anche sul vuoto e sulla variazione -> IL DIPOLO E' LA STRUTTURA VERA, e la domanda
        cambia: da dove viene un dipolo in una configurazione a TRE?
    N_eff troppo basso -> NON SI LEGGE, e si dichiara.""")
print("=" * 118)
