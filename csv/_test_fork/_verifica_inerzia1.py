# -*- coding: utf-8 -*-
"""VERIFICA PRELIMINARE DELLA CORREZIONE (1) -- `inerzia`. **NON e' un cablaggio, e' un gate.**

Il mandato propone:   inerzia = (rho_sorgente / peq_nodo) * (d_nodo / cs_nodo)**2
oggi il codice fa:    inerzia = max(rho_sorgente * (CS_M/cs)**2, 1e-6)

GATE A (commit 31922ff) ha autorizzato (1) misurando `I/peq_nodo`, con `I = |psi|^2`.
MA `_rho_sorgente()` NON RESTITUISCE `|psi|^2` quando CAMPO_SPINORIALE e' ON -- e lo e' in TUTTI i
run del fork: restituisce `rho_spin`, la norma del campo EMESSO dallo spinore.
Quindi il gate ha misurato una grandezza DIVERSA da quella che (1) userebbe.

Questo file misura la differenza, invece di assumerla in un verso o nell'altro.
Dati: i .pkl gia' committati. ASCII PURO. Nessun run.
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

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FILES = sorted(glob.glob(os.path.join(HERE, "_vuoto_s2ON_s?.pkl")))
CS_M = 2.0
LAM = None  # letto sotto se serve

print("=" * 118)
print("VERIFICA (1) -- il NUMERATORE di `inerzia` e il DENOMINATORE `peq_nodo` sono la stessa cosa?")
print("=" * 118)

tutti_r, tutti_I, tutti_rs = [], [], []
for f in FILES:
    A = pickle.load(open(f, "rb"))["attrs"]
    I = np.abs(np.asarray(A["psi"])) ** 2
    n = len(I)
    rs = A.get("rho_spin")
    if rs is None:
        continue
    rs = np.asarray(rs, float)[:n]
    ok = np.isfinite(rs) & np.isfinite(I) & (I > 0)
    tutti_I.append(I[ok]); tutti_rs.append(rs[ok])
    tutti_r.append(rs[ok] / I[ok])

I = np.concatenate(tutti_I); RS = np.concatenate(tutti_rs); R = np.concatenate(tutti_r)
print("\n--- (a) `rho_spin` contro `|psi|^2`: il docstring dice che coincidono NEL LIMITE ---")
print("  |psi|^2  : mediana %.4g   p05 %.4g   p95 %.4g" % (np.median(I), *np.percentile(I, [5, 95])))
print("  rho_spin : mediana %.4g   p05 %.4g   p95 %.4g" % (np.median(RS), *np.percentile(RS, [5, 95])))
print("  rapporto rho_spin/|psi|^2 : mediana %.4g   p05 %.4g   p95 %.4g   MAX %.4g"
      % (np.median(R), *np.percentile(R, [5, 95]), R.max()))
print("  correlazione: %.4f   |   se coincidessero, il rapporto sarebbe 1.0000 e la corr. 1.0000"
      % np.corrcoef(RS, I)[0, 1])
print("""
  LETTURA: NON coincidono. Il rapporto copre quattro ordini fra p05 e p95, e il MASSIMO e'
  astronomico (un nodo dove |psi|^2 e' ~0 mentre il campo emesso non lo e'). Il limite citato dal
  docstring -- "spinori in fase" -- NON e' il regime in cui gira il fork.""")

# ---------------------------------------------------------------- (b) peq proiettato sui nodi
print("\n--- (b) `peq_nodo`: la proiezione arco->nodo, con la forma di `den_w` (GATE B) ---")
rap_giusto, rap_misto, inerzia_oggi, inerzia_nuova = [], [], [], []
for f in FILES:
    A = pickle.load(open(f, "rb"))["attrs"]
    I = np.abs(np.asarray(A["psi"])) ** 2
    n = len(I)
    i = np.asarray(A["i"], int); j = np.asarray(A["j"], int)
    peq = np.asarray(A["peq"], float)
    rs = np.asarray(A.get("rho_spin"), float)[:n] if A.get("rho_spin") is not None else I
    deg = np.maximum(np.bincount(i, minlength=n) + np.bincount(j, minlength=n), 1)
    pn = (np.bincount(i, peq, minlength=n) + np.bincount(j, peq, minlength=n)) / deg
    ok = np.isfinite(pn) & (pn > 0) & np.isfinite(rs)
    rap_giusto.append(I[ok] / pn[ok])        # quello che GATE A ha misurato
    rap_misto.append(rs[ok] / pn[ok])        # quello che (1) userebbe davvero

    csn = A.get("_cs_nodo_prev")
    cs = np.asarray(csn, float)[:n] if (csn is not None and len(np.asarray(csn)) >= n) else np.full(n, CS_M)
    inerzia_oggi.append(np.maximum(rs[ok] * (CS_M / np.maximum(cs[ok], 1e-12)) ** 2, 1e-6))
    dd = (np.bincount(i, np.asarray(A["d"], float), minlength=n) +
          np.bincount(j, np.asarray(A["d"], float), minlength=n)) / deg
    inerzia_nuova.append((rs[ok] / pn[ok]) * (dd[ok] / np.maximum(cs[ok], 1e-12)) ** 2)

G = np.concatenate(rap_giusto); M = np.concatenate(rap_misto)
print("  |psi|^2 / peq_nodo   (cio' che GATE A ha misurato): mediana %.4g  p05 %.4g  p95 %.4g  max %.4g"
      % (np.median(G), *np.percentile(G, [5, 95]), G.max()))
print("  rho_spin / peq_nodo  (cio' che (1) userebbe)      : mediana %.4g  p05 %.4g  p95 %.4g  max %.4g"
      % (np.median(M), *np.percentile(M, [5, 95]), M.max()))

O = np.concatenate(inerzia_oggi); N = np.concatenate(inerzia_nuova)
print("\n--- (c) l'INERZIA che ne risulta ---")
print("  OGGI  : mediana %.4g   min %.4g   max %.4g   (col pavimento 1e-6)" % (np.median(O), O.min(), O.max()))
print("  NUOVA : mediana %.4g   min %.4g   max %.4g   (senza pavimento)" % (np.median(N), N.min(), N.max()))
print("  dinamica (max/min): OGGI %.4g    NUOVA %.4g" % (O.max() / max(O.min(), 1e-300),
                                                         N.max() / max(N.min(), 1e-300)))
print("  nodi con inerzia NUOVA sotto 1e-12 (omega = coppia/inerzia esploderebbe): %d  (%.4f %%)"
      % (int((N < 1e-12).sum()), 100.0 * (N < 1e-12).mean()))
print("""
  LETTURA, e va detta senza addolcirla: la forma proposta toglie il pavimento `1e-6` -- che e'
  giusto, perche' e' una manopola attiva sul 99.7 % dei nodi (A1, A3b) -- ma NON mette al suo posto
  un limite DERIVATO. Dove il campo emesso si annulla, `rho_spin/peq_nodo` va a zero e l'inerzia
  con lui: `omega = coppia/inerzia` diverge. Il difetto non e' l'assenza di protezione: e' che la
  forma non dichiara il proprio dominio, che e' cio' che A1 chiede a un limite lecito (e che il
  `max(t_luce, t_visco)` della plasticita' invece fa).""")

print("\n" + "=" * 118)
print("""CONCLUSIONE -- (1) NON E' STATA CABLATA, e la ragione e' di FORMA, non di effetto:

 1. ERRORE DI POPOLAZIONE (A3), nella forma che gli ASSIOMI chiamano proprio cosi': il numeratore
    `rho_sorgente` e' il campo EMESSO dallo spinore, il denominatore `peq` insegue `|psi|^2`
    (:3115, `rho = 0.5*(I[i]+I[j])` con `I = |psi|^2`). Due campi diversi: correlazione 0.80 sui
    quattro semi, rapporto da 0.005 a 8.8 fra p05 e p95 e massimo 7684.
    "Un rapporto ha senso solo se numeratore e denominatore vivono sulla STESSA popolazione."
 2. IL GATE CHE LO AUTORIZZAVA HA MISURATO UN'ALTRA GRANDEZZA: GATE A ha misurato `I/peq_nodo`.
 3. E TOGLIENDO IL PAVIMENTO SENZA METTERE UN LIMITE DERIVATO, l'inerzia NON "puo'" annullarsi:
    SI ANNULLA. Misurato `min = 0` ESATTO su 6 nodi (0.045 %), contro il minimo 1e-6 di oggi, e una
    dinamica max/min che passa da 5957 a 1.4e+301. Li' `omega = coppia/inerzia` e' una divisione
    per zero. La frazione e' piccola, ma per una DIVERGENZA la frazione non e' l'argomento giusto:
    U7b e' stato bloccante allo 0.11 %.

DUE STRADE, ed e' una DECISIONE, non una deduzione:
 (A) allineare le popolazioni: `inerzia = (|psi|^2 / peq_nodo) * (d/cs)^2`. Il rapporto torna
     coerente e GATE A torna pertinente -- MA l'inerzia smette di usare `rho_sorgente`, cioe'
     ESCE dalla FASE 2 (il campo emesso), e questo e' un cambio di modello, non una bonifica.
 (B) costruire uno sfondo del CAMPO EMESSO (un `peq_spin`, che oggi NON ESISTE) e usare
     `rho_spin/peq_spin`. Coerente per popolazione -- ma e' una LEGGE NUOVA, e questo giro e' una
     bonifica, non una ricerca.

NON SCELGO IO. La (A) e' un cambio di modello; la (B) e' un meccanismo nuovo. Entrambe eccedono il
mandato, che per (1) diceva "GATE A e B superati" -- e superati lo erano, su un'altra grandezza.""")
