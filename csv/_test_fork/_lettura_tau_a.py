# -*- coding: utf-8 -*-
"""`1` -- **L'ACCENSIONE DEL CAMPO: chi usa `TAU_A`, e quanto varrebbero i candidati.**

> **Mandato di Luca, 2026-09-25. SOLA LETTURA, nessuna riga del simulatore.**

**(a)** la tabella dei lettori di `TAU_A`, **dall'AST** e non da un `grep`: si vuole **in quale
FUNZIONE** cade ogni lettura, perche' *«un numero con PIU' ruoli va detto»*.
**(b)** per ogni candidato al tempo di rampa *(`d/cs` d'arco, periodo dello spinore)*: **esiste?
che FORMA ha (per nodo o per arco)? quanto vale nella scena `(ii)`?**
**(c)** la conseguenza: **quanti passi servirebbero** con ciascun candidato, contro i `5000` di oggi.

**Tutto pure-read.** ASCII puro nel sorgente.
"""
import ast
import io
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SIM = os.path.join(RADICE, "soliton_simulator.py")
DEST = os.path.join(_QUI, "_lettura_tau_a", "LETTURA_tau_a.txt")
os.makedirs(os.path.dirname(DEST), exist_ok=True)

P_ = []


def P(s=""):
    P_.append(s)
    print(s)


# =========================================================== (a) la tabella dall'AST
src = io.open(SIM, encoding="utf-8").read()
arb = ast.parse(src)
righe = src.split(chr(10))

# mappa riga -> (classe, funzione), costruita scendendo l'albero
dove = {}


def visita(n, cls=None, fn=None):
    if isinstance(n, ast.ClassDef):
        cls = n.name
    elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
        fn = n.name
        for k in range(n.lineno, getattr(n, "end_lineno", n.lineno) + 1):
            dove[k] = (cls, fn)
    for c in ast.iter_child_nodes(n):
        visita(c, cls, fn)


visita(arb)

NOMI = ("TAU_A", "_TAU_A_REGIME", "TAU_A_LOCALE")
letture = []
for n in ast.walk(arb):
    if isinstance(n, ast.Name) and n.id in NOMI:
        c, f = dove.get(n.lineno, (None, None))
        scrittura = isinstance(n.ctx, (ast.Store,))
        letture.append((n.lineno, n.id, "SCRIVE" if scrittura else "legge",
                        c or "-", f or "<modulo>", righe[n.lineno - 1].strip()[:88]))
letture.sort()

P("=" * 110)
P("(a) CHI USA `TAU_A` -- dall'AST, con la FUNZIONE in cui cade ogni occorrenza")
P("=" * 110)
P()
P("%-6s %-14s %-7s %-8s %-26s %s" % ("riga", "nome", "cosa", "classe", "funzione", "riga di codice"))
for r in letture:
    P("%-6d %-14s %-7s %-8s %-26s %s" % r)
P()

# =========================================================== i valori dei due regimi
import importlib.util as iu

_sp = iu.spec_from_file_location("sim_ta", SIM)
S = iu.module_from_spec(_sp)
_sp.loader.exec_module(S)

P("I DUE VALORI, e quale e' il DEFAULT:")
P("  REGIME = %r  (default del sorgente)  ->  TAU_A = %.4f" % (S.REGIME, S.TAU_A))
P("  ramo `deterministico`: TAU_A = 50.0   commento: \"alta persistenza memoria spinoriale\"")
P("  ramo `stocastico`:     TAU_A =  2.0   commento: \"canonico\"")
P("  TAU_A_LOCALE = %s   (commento nel sorgente: \"IN VERIFICA\")" % S.TAU_A_LOCALE)
P("  DT = %.4f   ->   TAU_A/DT = %.0f passi a r = 1" % (S.DT, S.TAU_A / S.DT))
P()
P("DOVE NASCE `eta`, cioe' CHI PARTE DA ZERO (dall'AST, scritture di `self.eta`):")
for n in ast.walk(arb):
    if isinstance(n, ast.Attribute) and n.attr == "eta" and isinstance(n.ctx, ast.Store):
        c, f = dove.get(n.lineno, (None, None))
        P("  riga %-6d in %-26s  %s" % (n.lineno, (f or "<modulo>"), righe[n.lineno - 1].strip()[:80]))
P()

# =========================================================== (b) i candidati
P("=" * 110)
P("(b) I CANDIDATI AL TEMPO DI RAMPA -- esistono? che forma hanno? quanto valgono?")
P("=" * 110)
P()
cand = []
for nome, attesa in (("_tempo_luce_nodo", "per NODO"), ("ritmo", "per NODO"),
                     ("_tau_arco_causale", "per ARCO"), ("_cs_arco_da_nodo", "per ARCO"),
                     ("_r_nodo_mitosi", "per NODO"), ("_fattore_tempo_arco", "per ARCO")):
    esiste = hasattr(S.Rete, nome)
    cand.append((nome, attesa, esiste))
    P("  %-22s %-10s  %s" % (nome, attesa, "ESISTE" if esiste else "NON esiste"))
P()

# la scena (ii) (b): la piu' economica
S.SEMINA_LAM = True
S.net = S.Rete(11)
S.test["dati"] = {}
S._NMASSE_VIDEO["sep"] = 4.0
S._MC_VIDEO["nodi"] = 0
S._MC_VIDEO["fasi_casuali"] = False
S._semina_masse_coerenti()
net = S.net
P("SCENA (ii) (b): n = %d, archi = %d" % (net.n, len(net.d)))
P()

# --- candidato 1: il tempo-luce PER NODO, `_tempo_luce_nodo` (gia' cablato, Strato 1) ---
try:
    # firma vera: `_tempo_luce_nodo(self, ii, jj)` -- vuole gli indici degli archi.
    tl = np.asarray(net._tempo_luce_nodo(net.i, net.j), float)
    P("  CANDIDATO 1 -- `d_nodo/cs_nodo` (`_tempo_luce_nodo`, GIA' CABLATO nello Strato 1).")
    # ! CORREZIONE DI UNA MIA CAUTELA SBAGLIATA: avevo scritto che il valore fosse PER ARCO
    #   perche' la firma prende `(ii, jj)`. E' FALSO: la shape misurata e' `n` (i NODI).
    #   Gli indici servono a COSTRUIRE `d_nodo` (la lunghezza tipica degli archi del nodo);
    #   il ritorno e' PER NODO, cioe' ESATTAMENTE la forma che serve a `ramp`.
    #   Lo dico invece di cancellarlo: era una cautela sbagliata, e la shape l'ha smentita.
    P("     FORMA: la firma e' `(self, ii, jj)` ma il RITORNO e' PER NODO -- misurato:")
    P("     shape restituita = %d,  nodi = %d,  archi = %d   -> shape == nodi: %s"
      % (tl.size, net.n, len(net.d), tl.size == net.n))
    P("     E' ESATTAMENTE la forma che serve a `ramp`: nessuna riduzione arco->nodo da inventare.")
    P("  valori:")
    P("     p05 %.6g   p50 %.6g   p95 %.6g   (in unita' di tempo)" %
      (np.percentile(tl, 5), np.median(tl), np.percentile(tl, 95)))
    P("     PASSI per ramp = 1 (tempo/DT):  p05 %.1f   p50 %.1f   p95 %.1f"
      % (np.percentile(tl, 5) / S.DT, np.median(tl) / S.DT, np.percentile(tl, 95) / S.DT))
    P("     contro i %.0f passi di TAU_A: piu' rapido di un fattore %.1f (mediana)"
      % (S.TAU_A / S.DT, S.TAU_A / max(np.median(tl), 1e-30)))
except Exception as e:
    P("  CANDIDATO 1 -- `_tempo_luce_nodo`: NON LEGGIBILE cosi': %s" % e)
P()

# --- candidato 2: il periodo dell'orologio, da `ritmo()` ---
try:
    r_ = np.asarray(net.ritmo(), float)
    P("  CANDIDATO 2 -- il PERIODO DELLO SPINORE. Ingredienti disponibili:")
    P("     `ritmo()` (il fattore di tempo proprio `r`): p05 %.6g  p50 %.6g  p95 %.6g"
      % (np.percentile(r_, 5), np.median(r_), np.percentile(r_, 95)))
    P("     `dt_n = DT*r`: p50 %.6g" % (S.DT * np.median(r_)))
    ock = getattr(net, "omega_clk", None)
    if ock is not None and np.size(ock):
        o_ = np.abs(np.asarray(ock, float))
        per = 2.0 * np.pi / np.maximum(o_, 1e-300)
        P("     `omega_clk`: p50 |omega| %.6g  ->  periodo 2pi/|omega|: p05 %.6g p50 %.6g p95 %.6g"
          % (np.median(o_), np.percentile(per, 5), np.median(per), np.percentile(per, 95)))
        P("     PASSI per ramp = 1: p50 %.1f" % (np.median(per) / S.DT))
    else:
        P("     `omega_clk` NON ESISTE come attributo al passo zero: il periodo dello spinore")
        P("     NON e' leggibile PRIMA del primo passo. E' un fatto, non un dettaglio: il")
        P("     candidato 2 richiede che l'orologio esista GIA', e al passo zero non esiste.")
except Exception as e:
    P("  CANDIDATO 2: NON LEGGIBILE: %s" % e)
P()

# =========================================================== (c) la conseguenza
P("=" * 110)
P("(c) LA CONSEGUENZA: `ramp` nei giri corti da 120 passi")
P("=" * 110)
P()
P("  `ramp = min(1, eta/TAU_A)` ed `eta` cresce di `dt_n = DT*r` per passo.")
P("  Con `r ~ 1`, al passo `k`:  ramp(k) = k*DT/TAU_A = k/%.0f" % (S.TAU_A / S.DT))
for k in (1, 8, 30, 60, 120, 1230, 5000):
    P("     passo %-6d ramp = %.6f   (il campo e' al %.4f %% del suo valore)"
      % (k, min(1.0, k * S.DT / S.TAU_A), 100.0 * min(1.0, k * S.DT / S.TAU_A)))
P()
P("  E `ramp` entra nei pesi COME PRODOTTO DI DUE NODI (`ramp[i]*ramp[j]`, `:3537`),")
P("  quindi il peso dell'arco va come `ramp^2`: al passo 120, %.3e del valore maturo."
  % (min(1.0, 120 * S.DT / S.TAU_A) ** 2))

io.open(DEST, "w", encoding="utf-8", newline="\n").write(chr(10).join(P_) + chr(10))
