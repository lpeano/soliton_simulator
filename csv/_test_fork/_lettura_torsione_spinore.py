# -*- coding: utf-8 -*-
"""`2` -- **LA TORSIONE LETTA DALLO SPINORE: che cosa esiste gia', e quanto vale.**

> **Mandato di Luca, 2026-09-25. SOLA LETTURA, nessuna riga del simulatore.**
> *«Si puo' leggere per ogni arco la ROTAZIONE dello spinore trasportato da i a j, e il suo
> avvolgimento su 4pi, con cio' che il codice calcola gia'?»*

**COSA SI LEGGE, e tutto e' `PURE-READ` per dichiarazione del codice:**

```
_link_su2_N(nb_i, nb_j) = (1 + n_i.n_j) I + i (n_i x n_j).sigma        `staticmethod`, PURE-READ
IDENTITA' SIGILLATA (`csv/_seal_fork/_sigillo_N.py`):  N_ij = 2 cos(chi/2) U_ij
   dove U_ij = exp(-i (chi/2) m_hat.sigma) e' la CONNESSIONE DI BERRY unitaria,
   e `chi = arccos(n_i . n_j)` e' **L'ANGOLO DI ROTAZIONE DEL TRASPORTO**.
circolazione_topologica() -> `berry_spin`: **la fase di Berry spinoriale sui CICLI**,
   dichiarata nel docstring **«curvatura non-abeliana SU(2), gauge-invariante»**.
```

**LA DOMANDA CHE DECIDE IL COSTO, e si risponde con un conto:** `chi = arccos(n_i.n_j)` sta in
`[0, pi]`, quindi **un SOLO arco non puo' superare `pi`** — **un quarto** del ricoprimento `4pi`.
**Se il quanto deve essere `4pi`, non puo' vivere su un arco: deve vivere su un CICLO.**
E il ciclo **c'e' gia'**, con la sua curvatura gia' calcolata.

**Si misura:** la distribuzione di `chi` per arco, l'angolo `SU(2)` del trasporto, il numero di
cicli, `berry_spin` e l'olonomia di fase — nella scena `(ii)`, **su 4 semi**.
"""
import io
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
DEST = os.path.join(_QUI, "_lettura_torsione", "LETTURA_torsione_spinore.txt")
os.makedirs(os.path.dirname(DEST), exist_ok=True)

import importlib.util as iu

_sp = iu.spec_from_file_location("sim_ts", os.path.join(RADICE, "soliton_simulator.py"))
S = iu.module_from_spec(_sp)
_sp.loader.exec_module(S)

P_ = []


def P(s=""):
    P_.append(s)
    print(s)


P("=" * 108)
P("(2a) LA TORSIONE LETTA DALLO SPINORE -- cosa esiste gia', e quanto vale")
P("=" * 108)
P()
P("I FLAG, dai default del sorgente -- e decidono COSA e' leggibile:")
for nome in ("SPINORE_VIVO", "SPINORE_CORRETTO", "CAMPO_SPINORIALE", "CHI_DA_SPINORE",
             "CHI_CORE", "CHI_BASC", "FORK_SU2", "FORK_SU2_MEM", "TORS_4PI", "OLON_PART"):
    P("  %-18s = %s" % (nome, getattr(S, nome, "ASSENTE")))
P()
P("CHE COSA IL CODICE CALCOLA GIA' (pure-read per dichiarazione):")
P("  `_link_su2_N`             %s   staticmethod: N_ij = (1+n_i.n_j) I + i (n_i x n_j).sigma"
  % ("ESISTE" if hasattr(S.Rete, "_link_su2_N") else "NON esiste"))
P("  `_bloch_ritardato`        %s   i Bloch a t-tau (STRATO 1)"
  % ("ESISTE" if hasattr(S.Rete, "_bloch_ritardato") else "NON esiste"))
P("  `circolazione_topologica` %s   restituisce `berry_spin` = curvatura non-abeliana SU(2) sui CICLI"
  % ("ESISTE" if hasattr(S.Rete, "circolazione_topologica") else "NON esiste"))
P("  `chiralita_core_locale`   %s   l'identita' materia/vuoto"
  % ("ESISTE" if hasattr(S.Rete, "chiralita_core_locale") else "NON esiste"))
P()

SEMI = [11, 12, 13, 14]
ris = []
for seme in SEMI:
    S.SEMINA_LAM = True
    S.net = S.Rete(seme)
    S.test["dati"] = {}
    S._NMASSE_VIDEO["sep"] = 4.0
    S._MC_VIDEO["nodi"] = 0
    S._MC_VIDEO["fasi_casuali"] = False
    S._semina_masse_coerenti()
    net = S.net
    net.step()                     # UN passo: senza, il campo non esiste (vedi il passo zero)
    o = dict(seme=seme, n=int(net.n), archi=int(len(net.d)))
    nb = getattr(net, "_nb", None)
    o["nb_presente"] = bool(nb is not None and np.size(nb) and len(nb) >= net.n)
    if o["nb_presente"]:
        nb = np.asarray(nb, float)[:net.n]
        nb = nb / np.maximum(np.linalg.norm(nb, axis=1), 1e-30)[:, None]
        ii, jj = net.i, net.j
        cosk = np.clip(np.sum(nb[ii] * nb[jj], axis=1), -1.0, 1.0)
        chi = np.arccos(cosk)
        o["chi_p05"] = float(np.percentile(chi, 5)); o["chi_p50"] = float(np.median(chi))
        o["chi_p95"] = float(np.percentile(chi, 95)); o["chi_max"] = float(chi.max())
        # l'ANGOLO SU(2) del trasporto: U = exp(-i (chi/2) m.sigma) -> angolo SU(2) = chi
        # e il PESO |N|/2 = cos(chi/2) = overlap di spin (identita' sigillata)
        o["overlap_p50"] = float(np.median(np.cos(chi / 2.0)))
        # quanti archi hanno chi oltre le frazioni del ricoprimento
        for q, et in ((np.pi / 2, "pi/2"), (np.pi * 0.9, "0.9 pi")):
            o["chi_oltre_%s" % et] = float(np.mean(chi > q))
    # i CICLI e la curvatura non-abeliana
    try:
        c = net.circolazione_topologica()
        o["n_cicli"] = int(c.get("n_cicli", 0))
        for k in ("olonomia_max", "olonomia_media_assoluta"):
            o[k] = float(c.get(k, float("nan")))
        bs = np.asarray(c.get("berry_spin", np.zeros(0)), float)
        o["berry_n"] = int(bs.size)
        if bs.size:
            o["berry_p50"] = float(np.median(np.abs(bs))); o["berry_max"] = float(np.max(np.abs(bs)))
    except Exception as e:
        o["cicli_errore"] = str(e)[:110]
    ris.append(o)

P("-" * 108)
P("LA MISURA, scena (ii) (b), DOPO UN PASSO, su %d semi" % len(SEMI))
P("-" * 108)


def st(campo):
    v = [r[campo] for r in ris if campo in r]
    if not v:
        return None
    a = np.asarray(v, float)
    return a, float(a.mean()), (float(a.std(ddof=1) / np.sqrt(len(a))) if len(a) > 1 else float("nan"))


P()
if all(r.get("nb_presente") for r in ris):
    P("  `_nb` (Bloch per nodo) E' PRESENTE coi default: la rotazione del trasporto E' LEGGIBILE.")
    P()
    P("  chi = arccos(n_i . n_j), L'ANGOLO DI ROTAZIONE DEL TRASPORTO SU(2), per ARCO:")
    for c, et in (("chi_p05", "p05"), ("chi_p50", "p50"), ("chi_p95", "p95"), ("chi_max", "max")):
        a, m, s = st(c)
        P("     %-4s  %.6f rad = %.6f pi     (media su %d semi, SE %.2e)"
          % (et, m, m / np.pi, len(SEMI), s))
    a, m, s = st("overlap_p50")
    P("     overlap di spin |N|/2 = cos(chi/2), mediano: %.6f  (1 = allineati, 0 = antipodali)" % m)
    for et in ("pi/2", "0.9 pi"):
        a, m, s = st("chi_oltre_%s" % et)
        P("     frazione di archi con chi > %-7s : %.6f +- %.6f" % (et, m, s))
    P()
    P("  IL LIMITE STRUTTURALE, e non e' una misura ma un CONTO: `arccos` sta in [0, pi],")
    P("  quindi UN ARCO NON PUO' SUPERARE `pi` = UN QUARTO del ricoprimento `4pi`.")
    P("  -> se il quanto deve essere `4pi`, NON PUO' VIVERE SU UN ARCO: serve un CICLO.")
else:
    P("  `_nb` NON e' presente coi default: la rotazione NON e' leggibile senza accendere un flag.")
    for r in ris:
        P("     seme %d: nb_presente = %s" % (r["seme"], r.get("nb_presente")))
P()
P("  I CICLI, e la curvatura non-abeliana che il codice CALCOLA GIA':")
a = st("n_cicli")
if a:
    P("     n_cicli = %.1f +- %.1f" % (a[1], a[2]))
for c, et in (("berry_n", "campioni di `berry_spin`"), ("berry_p50", "|berry_spin| mediano"),
              ("berry_max", "|berry_spin| max"), ("olonomia_max", "olonomia di fase max"),
              ("olonomia_media_assoluta", "olonomia di fase media |.|")):
    a = st(c)
    if a:
        P("     %-30s = %.6g +- %.2g" % (et, a[1], a[2]))
for r in ris:
    if "cicli_errore" in r:
        P("     seme %d: ERRORE nei cicli -> %s" % (r["seme"], r["cicli_errore"]))

io.open(DEST, "w", encoding="utf-8", newline="\n").write(chr(10).join(P_) + chr(10))
