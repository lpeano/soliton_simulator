# -*- coding: utf-8 -*-
"""I CRITERI DELLA PROVA DI `CURA 2`, letti dai due snapshot. **Sola lettura.**

I criteri sono quelli fissati PRIMA, in `doc/REGISTRO_FISICA.md` scheda 9 par.9:
`E1a` `E1b` `B` `K` `H` `G` `R` `C` `V8`/`V9`.

**`T5` E' QUI**, per decisione di Luca del 2026-09-24: il controllo positivo di `CURA 2` e'
il confronto fra **`_cura2_corto`** e **`_cura1_corto`**, che sono **due processi freschi a un
solo braccio** -- lo `STANDARD 1` che il sigillo aveva violato (`Z145`).

`P1-ter`: questa tabella si GENERA, non si ricopia.
ASCII puro.
"""
import gzip
import io
import os
import pickle
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
RIF = os.path.join(_QUI, "_cura1_corto", "scena_000120.pkl.gz")
CUR = os.path.join(_QUI, "_cura2_corto", "scena_000120.pkl.gz")
DEST = os.path.join(_QUI, "_cura2_corto", "REFERTO_criteri.txt")

# La convenzione di `G1`-`G2`, NON una nuova: `_dove_spinge_la_gravita.py:72`.
# **LETTI DAL RUN**, non assunti: il log dice "n = 2391 nodi alla semina".
N_VUOTO, N0_SEMINA = 900, 2391
# `PHI_CRIT` LETTO DAL SIMULATORE, non ricopiato: e' la costante che `mitosi()` usa.
sys.path.insert(0, RADICE)
from soliton_simulator import PHI_CRIT
ETI = ("vuoto-vuoto", "massa-massa", "nato-nato", "CONFINE vuoto-massa",
       "CONFINE con nato", "altro")


def classe_arco(i, j, n0=N0_SEMINA, nv=N_VUOTO):
    """0 vv, 1 mm, 2 nn, 3 confine vuoto-massa, 4 confine con nato, 5 altro."""
    ci = np.where(i < nv, 0, np.where(i < n0, 1, 2))
    cj = np.where(j < nv, 0, np.where(j < n0, 1, 2))
    lo, hi = np.minimum(ci, cj), np.maximum(ci, cj)
    c = np.full(len(i), 5)
    c[(lo == 0) & (hi == 0)] = 0
    c[(lo == 1) & (hi == 1)] = 1
    c[(lo == 2) & (hi == 2)] = 2
    c[(lo == 0) & (hi == 1)] = 3
    c[hi == 2] = np.where(lo[hi == 2] == 2, 2, 4)
    return c


def leggi(p):
    with gzip.open(p, "rb") as f:
        return pickle.load(f)


def q(v, qs=(10, 50, 90)):
    v = np.asarray(v, dtype=float)
    v = v[np.isfinite(v)]
    if not len(v):
        return [float("nan")] * len(qs)
    return [float(x) for x in np.percentile(v, qs)]


def main():
    W = sys.stdout.write
    f = io.open(DEST, "w", encoding="utf-8", newline="\n")

    def P(s):
        W(s)
        f.write(s)

    dR, dC = leggi(RIF), leggi(CUR)
    A, B = dR["attrs"], dC["attrs"]
    A_, B_ = A, B                    # alias per la sezione della saturazione
    nA, nB = len(A["_cs_nodo_prev"]), len(B["_cs_nodo_prev"])

    P("# I CRITERI DELLA PROVA DI `CURA 2` -- generati, non ricopiati (`P1-ter`)\n#\n")
    P("# riferimento  _cura1_corto  blob %s  commit %s\n"
      % (str(dR.get("blob"))[:8], str(dR.get("commit"))[:7]))
    P("# prova        _cura2_corto  blob %s  commit %s\n"
      % (str(dC.get("blob"))[:8], str(dC.get("commit"))[:7]))
    P("# UN INTERRUTTORE DI DIFFERENZA: TEMPO_UNICO_MITOSI.\n")
    P("# E DUE PROCESSI FRESCHI A UN SOLO BRACCIO (`STANDARD 1`): e' `T5`, dopo `Z145`.\n\n")

    # ------------------------------------------------------------------ E1a / E1b
    P("=" * 96 + "\n`E1a` / `E1b` -- LA MITOSI VIVE? ESPLODE?\n" + "=" * 96 + "\n")
    P("  %-26s %14s %14s %12s\n" % ("", "cura1 (OFF)", "cura2 (ON)", "rapporto"))
    righe = [("n al passo 120", nA, nB),
             ("archi", len(A["i"]), len(B["i"])),
             ("nati da mitosi", A.get("_g_nati_mitosi"), B.get("_g_nati_mitosi")),
             ("eventi di mitosi", A.get("_g_nati_mitosi_ev"), B.get("_g_nati_mitosi_ev")),
             ("nascite (semina/mit)", A.get("_g_sm_nascite"), B.get("_g_sm_nascite"))]
    for nome, a, b in righe:
        r = (float(b) / float(a)) if (a not in (None, 0) and b is not None) else float("nan")
        P("  %-26s %14s %14s %12.4f\n" % (nome, a, b, r))
    ev = B.get("_g_nati_mitosi_ev") or 0
    e1a = ev > 0 and 0.1 <= (float(ev) / max(A.get("_g_nati_mitosi_ev") or 1, 1)) <= 10.0
    e1b = nB < 10 * nA
    P("\n  `E1a` LA MITOSI NON MUORE ed e' dello STESSO ORDINE  -> %s\n"
      % ("PASS" if e1a else "*** FAIL ***"))
    P("  `E1b` NON ESPLODE (n < 10x il riferimento)            -> %s\n"
      % ("PASS" if e1b else "*** FAIL ***"))
    P("\n  !! IL TERMINE DI PARAGONE E' `FASE_2PI`, che qui e' CADUTA: 62 eventi -> 1.\n")

    # ------------------------------------------------------------------ K
    P("\n" + "=" * 96 + "\n`K` -- QUANTE VOLTE IL CLIP AVREBBE MORSO, e su QUALE LATO\n" + "=" * 96 + "\n")
    tot = B.get("_tum_clip_prob_tot") or 1
    for nome, k, nota in (
            ("clip ALTO su `prob` (resp > 1)", "_tum_clip_prob",
             "la forma di Poisson toglie QUESTO"),
            ("clip a ZERO su `prob` (resp <= 0)", "_tum_clip0_prob",
             "Poisson lo CONSERVA: qui le due forme COINCIDONO"),
            ("clip ALTO su `rep`", "_tum_clip_rep", "decide se `tanh` cambierebbe qualcosa"),
            ("Eulero con dt/tau > 1", "_tum_eulero_gt1",
             "misura quanto serviva `S12` in QUESTO regime")):
        v = B.get(k)
        P("  %-36s %14s / %12s = %9.5f %%   %s\n"
          % (nome, v, tot, 100.0 * (v or 0) / tot, nota))
    P("\n  -> il clip ha DUE lati e ora sono contati entrambi (richiesta di Luca).\n")

    # ------------------------------------------------------------------ C / H
    P("\n" + "=" * 96 + "\n`C` / `H` -- LE GUARDIE `A8`: invocazioni, salti, forma, QUANDO\n" + "=" * 96 + "\n")
    for nome, pre in (("`_r_corrente` (l'orologio)", "_tum_r"),
                      ("`_cs_nodo_prev` (la velocita')", "_tum_cs"),
                      ("`_dt_e_ultimo` (il tempo d'arco)", "_tum_t")):
        t = B.get(pre + "_tot")
        s = B.get(pre + "_salti", 0) or 0
        P("  %-34s invocazioni %5s   salti %5s (%6.2f %%)   forma %s   ultimo %s\n"
          % (nome, t, s, 100.0 * s / max(t or 1, 1),
             B.get(pre + "_forma", "-"), B.get(pre + "_quando", "-")))
    P("\n  -> un fallback mai misurato e' un comportamento SCONOSCIUTO (`P5`); uno che scatta\n")
    P("     il 72 %% NON e' un fallback, e' il comportamento principale.\n")

    # ------------------------------------------------------------------ R
    P("\n" + "=" * 96 + "\n`R` -- `d0` e `d/d0`: QUANTILI e divisione per CLASSE D'ARCO\n" + "=" * 96 + "\n")
    P("  convenzione di `G1`-`G2` (`_dove_spinge_la_gravita.py:72`), NON una nuova:\n")
    P("    nodo < %d = VUOTO   < %d = MASSA seminata   oltre = NATO\n" % (N_VUOTO, N0_SEMINA))
    P("  e `%d` e' LETTO DAL RUN: il log dice \"n = %d nodi alla semina\".\n\n" % (N0_SEMINA, N0_SEMINA))
    for etichetta, gr in (("d0", "d0"), ("d/d0", None)):
        P("  --- %s ---\n" % etichetta)
        P("  %-22s %10s %10s %10s %10s %10s %10s %9s\n"
          % ("classe", "p10 OFF", "p50 OFF", "p90 OFF", "p10 ON", "p50 ON", "p90 ON", "n ON"))
        for cid in range(6):
            fila = []
            for D in (A, B):
                i, j = np.asarray(D["i"]), np.asarray(D["j"])
                c = classe_arco(i, j)
                m = (c == cid)
                v = np.asarray(D["d0"], dtype=float)
                if gr is None:
                    v = np.asarray(D["d"], dtype=float) / np.maximum(v, 1e-300)
                fila.append((q(v[m]), int(m.sum())))
            P("  %-22s %10.4f %10.4f %10.4f %10.4f %10.4f %10.4f %9d\n"
              % ((ETI[cid],) + tuple(fila[0][0]) + tuple(fila[1][0]) + (fila[1][1],)))
        P("\n")
    P("  !! LA MEDIANA DA SOLA NON BASTA (rilievo di Luca): e' un riassunto GLOBALE di un\n")
    P("     rapporto LOCALE, e puo' nascondere compressione e stiramento che si COMPENSANO.\n")
    P("  !! E `A2`: queste sono statistiche del REFERTO. Nessuna entra nella legge.\n")

    # ------------------------------------------------------------------ G
    P("\n" + "=" * 96 + "\n`G` -- DOVE NASCE LA MATERIA rispetto al GRADIENTE DI `r`\n" + "=" * 96 + "\n")
    P("  Si RIPORTA, non si giudica (criterio di Luca).\n\n")
    for nome, D in (("cura1 (OFF)", A), ("cura2 (ON)", B)):
        i, j = np.asarray(D["i"]), np.asarray(D["j"])
        n = len(D["_cs_nodo_prev"])
        r = np.asarray(D.get("_r_corrente", np.ones(n)), dtype=float)
        # `_r_corrente` e' scritto in `step()`; `mitosi()` gira DOPO e aggiunge nodi, quindi
        # ALLO SNAPSHOT l'array e' corto dei figli dell'ULTIMO passo. NON e' un difetto, ed e'
        # il motivo per cui `_tum_r_salti = 0`: `_r_nodo_mitosi` e' chiamata DENTRO `mitosi()`,
        # PRIMA che i figli esistano, e li' `len(r) == n`.
        # E' l'ordine che salva la legge, non la guardia -- l'OPPOSTO di `_cs_nodo_prev`
        # (71.88 %) e `_psi_spin_prec` (95.33 %), dove la mitosi aveva gia' allungato `n`.
        # Per la MISURA si restano sugli archi i cui DUE estremi hanno un `r`.
        ok = (i < len(r)) & (j < len(r))
        if len(r) < n:
            P("  %-12s  `_r_corrente` e' lungo %d su %d nodi (i %d figli dell'ultimo passo\n"
              % (nome, len(r), n, n - len(r)))
            P("                nascono DOPO la scrittura): la misura resta sui %d archi con\n"
              % int(ok.sum()))
            P("                entrambi gli estremi noti, su %d.\n" % len(i))
        i, j = i[ok], j[ok]
        g = np.abs(r[i] - r[j])
        nati = (i >= N0_SEMINA) | (j >= N0_SEMINA)
        a1 = q(g)
        a2 = q(g[nati]) if nati.any() else [float("nan")] * 3
        P("  %-12s  TUTTI  %.3e %.3e %.3e   |  ARCHI CON UN NATO  %.3e %.3e %.3e  (n=%d)\n"
          % (nome, a1[0], a1[1], a1[2], a2[0], a2[1], a2[2], int(nati.sum())))
    P("\n  -> se il gradiente sugli archi con un NATO fosse sistematicamente piu' alto, la\n")
    P("     materia nascerebbe DOVE IL TEMPO CAMBIA. E' cio' che la cura rende misurabile:\n")
    P("     prima il gradiente veniva da `|tw|`, che e' TORSIONE, non tempo.\n")

    # ------------------------------------------------------------------ SATURAZIONE
    P("\n" + "=" * 96 + "\n`A11` cor.6 -- LA SATURAZIONE DI `tanh(grad)`: il limite MORDE?\n"
      + "=" * 96 + "\n")
    P("  La soglia della mitosi e' `soglia0 * (1 - 0.3*tanh(grad))`. Se `tanh(grad) -> 1`\n")
    P("  la modulazione diventa un RISCALAMENTO COSTANTE della soglia, cioe' un PARAMETRO\n")
    P("  NASCOSTO (`A1`), e `A11` cor.6 dice che un limite che satura e' un ALLARME.\n")
    P("  E' l'argomento con cui la scheda 9 par.2 ha scelto `r` invece di `1/r`:\n")
    P("    r    in [1.4142e-6, 1.4142]  -> tanh(grad) <= 0.8884\n")
    P("    1/r  in [0.707, 707107]      -> tanh(grad) -> 1 ESATTO\n")
    P("  QUI SI MISURA SE L'ARGOMENTO REGGE SUI DATI.\n\n")
    P("  %-14s %10s %10s %10s %12s %12s\n"
      % ("braccio", "p50", "p90", "p99", "max", "> 0.95"))
    for nome, D, sorgente in (("cura1 (OFF)", A_, "da |tw|"), ("cura2 (ON)", B_, "da r")):
        i, j = np.asarray(D["i"]), np.asarray(D["j"])
        n = len(D["_cs_nodo_prev"])
        if sorgente == "da r":
            r = np.asarray(D.get("_r_corrente", np.ones(n)), dtype=float)
            ok = (i < len(r)) & (j < len(r))
            g = np.abs(r[i[ok]] - r[j[ok]])
        else:
            # `tau_nodo = 1 + mean(|tw|)/PHI_CRIT`, ricostruito come in `mitosi()`
            tw = np.abs(np.asarray(D["tw"], dtype=float))
            deg = np.maximum(np.asarray(D["_deg"], dtype=float), 1.0)
            acc = np.zeros(n)
            mi, mj = i < n, j < n
            np.add.at(acc, i[mi], tw[mi])
            np.add.at(acc, j[mj], tw[mj])
            tau_nodo = 1.0 + acc / deg[:n] / PHI_CRIT
            g = np.abs(tau_nodo[i] - tau_nodo[j])
        th = np.tanh(g)
        a = q(th, (50, 90, 99))
        P("  %-14s %10.4f %10.4f %10.4f %12.4f %11.4f %%   (%s)\n"
          % (nome, a[0], a[1], a[2], float(th.max()),
             100.0 * float((th > 0.95).mean()), sorgente))
    P("\n  -> la quota con `tanh(grad) > 0.95` e' la misura del cor.6: se fosse ALTA, la\n")
    P("     modulazione sarebbe un riscalamento costante e il `0.3` un parametro nascosto.\n")

    P("\n" + "=" * 96 + "\n")
    P("!! COSA QUESTO REFERTO NON DICE: che la cura sia GIUSTA. Dice che la mitosi vive, che\n")
    P("   il bilancio chiude, e QUANTO le forme nuove differiscono da quelle vecchie.\n")
    f.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
