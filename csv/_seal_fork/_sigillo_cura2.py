# -*- coding: utf-8 -*-
"""SIGILLO DI `CURA 2` -- IL TEMPO UNICO NELLA MITOSI (`TEMPO_UNICO_MITOSI`).

Il principio di Luca: *si applicano le cose corrette e coerenti; dove intenzione e
implementazione divergono si realizza l'INTENZIONE; ogni grandezza con le sue unita' giuste.*

⚠ IL TEST CHE CONTA E' `T3`, ed e' quello che CODIFICA LA REGOLA: **i quattro usi in cui
  intenzione e implementazione COINCIDONO devono restare INTOCCATI.** `tau_soglia`,
  `tau_tetto`, `centro`, `segno` sono posizioni sull'asse della TORSIONE, e li' la legge e'
  giusta. Se la cura li toccasse, avrebbe curato cio' che non era rotto -- e `T3` lo prende
  **dall'AST**, non dalla mia parola.

ASCII PURO.
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
sys.path.insert(0, RADICE)
SORGENTE = os.path.join(RADICE, "soliton_simulator.py")
DRIVER = os.path.join(RADICE, "csv", "_test_fork", "_scena_video.py")
RIF120 = os.path.join(RADICE, "csv", "_test_fork", "_cura1_corto", "scena_000120.pkl.gz")
DEST = os.path.join(_QUI, "_sig_cura2")
INERTE = os.path.join(DEST, "inerte")
COMUNE = ["--sep=4.0", "--serie=20", "--chi-basc=on", "--chi-coop=on", "--scala-min=off",
          "--coes-adim=on", "--peq-esatto=on", "--peq-nascita-locale=on",
          "--scala-min-passo=on", "--coes-causale=on", "--anom-simm=on", "--invarianti=on"]

# i quattro usi COERENTI: intenzione e implementazione dicono la stessa cosa -> NON si toccano
TORSIONE = ("tau_soglia", "tau_tetto", "centro", "segno")
# i nomi che la CURA introduce: se comparissero in un uso TORSIONE, la cura avrebbe
# curato cio' che non era rotto
NUOVI = ("_ft", "ampiezza_int", "resp_int", "_rn", "_tau_a", "_rap", "_resp_rep")


def confronta_snap(p_a, p_b, W):
    import gzip
    import pickle

    def leggi(p):
        return pickle.load(gzip.open(p, "rb"))["attrs"]
    A, B = leggi(p_a), leggi(p_b)
    ug = dv = nc = 0
    diversi = []
    for k in sorted(set(A) | set(B)):
        if k not in A or k not in B:
            nc += 1
            continue
        a, b = A[k], B[k]
        try:
            if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
                a, b = np.asarray(a), np.asarray(b)
                if a.shape != b.shape:
                    dv += 1
                    diversi.append("%s(shape %s!=%s)" % (k, a.shape, b.shape))
                    continue
                if a.size == 0 or np.array_equal(a, b):
                    ug += 1
                else:
                    dv += 1
                    try:
                        diversi.append("%s(max|d|=%.3e)" % (k, float(np.max(np.abs(a - b)))))
                    except Exception:
                        diversi.append(k)
            elif a == b:
                ug += 1
            else:
                dv += 1
                diversi.append("%s(%r != %r)" % (k, a, b))
        except Exception:
            nc += 1
    W("  campi UGUALI %d   DIVERSI %d   non confrontati %d\n" % (ug, dv, nc))
    if diversi:
        W("  i diversi: %s\n" % ", ".join(diversi[:8]))
    return ug, dv, nc


def _nomi(nodo):
    out = set()
    for n in ast.walk(nodo):
        if isinstance(n, ast.Name):
            out.add(n.id)
        elif isinstance(n, ast.Attribute):
            out.add(n.attr)
    return out


def assegnamenti(src, bersagli):
    """{nome: nomi letti nel VALORE}, per gli assegnamenti a quei bersagli. Dall'AST."""
    fuori = {}
    for n in ast.walk(ast.parse(src)):
        if not isinstance(n, ast.Assign) or n.value is None:
            continue
        for b in n.targets:
            if isinstance(b, ast.Name) and b.id in bersagli:
                fuori.setdefault(b.id, set()).update(_nomi(n.value))
    return fuori


def rami_del_flag(src, flag):
    """{funzione: [righe]} dei test su quel flag. Dall'AST, non dal testo (`STANDARD 9`)."""
    alb = ast.parse(src)
    fn = {}
    for n in ast.walk(alb):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for r in range(n.lineno, (getattr(n, "end_lineno", None) or n.lineno) + 1):
                fn.setdefault(r, n.name)
    fuori = {}
    for n in ast.walk(alb):
        if isinstance(n, ast.If) and flag in {x.id for x in ast.walk(n.test)
                                              if isinstance(x, ast.Name)}:
            fuori.setdefault(fn.get(n.lineno, "(modulo)"), []).append(n.lineno)
    return fuori


def collaudo(W):
    W("COLLAUDO DEI CRITERI su casi a RISPOSTA NOTA (`P1-sexies`), PRIMA di misurare\n")
    W("-" * 100 + "\n")
    e = []

    # K1/K2 -- la forma di Poisson contro il clip
    for lam, atteso in ((0.01, "coincidono"), (2.0, "differiscono")):
        pois = 1.0 - np.exp(-lam)
        clip = min(lam, 1.0)
        vicino = abs(pois - clip) < 0.01 * max(lam, 1e-9)
        ok = vicino if atteso == "coincidono" else (not vicino)
        W("K%d lambda = %-5s : Poisson %.6f, clip %.6f -> %s -> %s\n"
          % (len(e) + 1, lam, pois, clip, atteso, "OK" if ok else "*** NO ***"))
        e.append(ok)
    W("   -> a lambda piccolo l'errore relativo e' lambda/2; a lambda = 2 il clip da' 1.0\n")
    W("      esatto mentre Poisson da' 0.864665: **e' li' che le due forme differiscono**.\n")

    # K3 -- la forma ESATTA e' una COMBINAZIONE CONVESSA per QUALUNQUE passo
    peggio = 0.0
    for rap in (0.1, 1.0, 5.0, 50.0):
        v0, bers = 0.3, 0.9
        esatto = bers + (v0 - bers) * np.exp(-rap)
        peggio = max(peggio, 0.0 if min(v0, bers) <= esatto <= max(v0, bers) else 1.0)
    ok = (peggio == 0.0)
    W("K3 la forma ESATTA resta fra i due valori per dt/tau in {0.1, 1, 5, 50} -> %s\n"
      % ("OK: combinazione convessa" if ok else "*** scavalca ***"))
    e.append(ok)

    # K4 -- IL CASO CHE DEVE FALLIRE: l'EULERO scavalca
    v0, bers, rap = 0.3, 0.9, 2.5
    eul = v0 + rap * (bers - v0)
    ok = not (min(v0, bers) <= eul <= max(v0, bers))
    W("K4 IL CASO CHE DEVE FALLIRE: l'EULERO con dt/tau = 2.5 da' %.4f, FUORI da [%.1f, %.1f]"
      " -> %s\n" % (eul, v0, bers, "OK: il difetto di `S12` e' riprodotto" if ok else "*** NO ***"))
    e.append(ok)

    # K5 -- IL CASO CHE DEVE FALLIRE: un `segno` che USA un nome della cura
    finto = "segno = -np.tanh(3.0 * (tau_pp - centro)) * _ft\n"
    letti = assegnamenti(finto, ("segno",)).get("segno", set())
    ok = bool(letti & set(NUOVI))
    W("K5 SECONDO CASO CHE DEVE FALLIRE: un `segno` che usa `_ft` -> intercettato %s -> %s\n"
      % (sorted(letti & set(NUOVI)), "OK" if ok else "*** il criterio non lo vede ***"))
    e.append(ok)

    # K6 -- e il `segno` VERO non deve essere segnalato
    vero = "segno = -np.tanh(3.0 * (tau_pp - centro))\n"
    letti = assegnamenti(vero, ("segno",)).get("segno", set())
    ok = not (letti & set(NUOVI))
    W("K6 e il `segno` VERO non si segnala: legge %s -> %s\n"
      % (sorted(letti), "OK" if ok else "*** falso allarme ***"))
    e.append(ok)

    ok = all(e)
    W("-" * 100 + "\n  -> %s\n\n" % ("i criteri PASSANO" if ok else "*** NON PASSANO ***"))
    return ok


def main():
    W = sys.stdout.write
    try:
        os.makedirs(DEST)
    except OSError:
        pass
    ref = io.open(os.path.join(DEST, "REFERTO.txt"), "w", encoding="utf-8", newline="\n")

    def P(s):
        W(s)
        ref.write(s)

    P("# SIGILLO -- `CURA 2`: il tempo unico nella mitosi\n#\n")
    if not collaudo(P):
        ref.close()
        return 1

    import hashlib
    sorg = io.open(SORGENTE, encoding="utf-8").read()
    P("blob simulatore ORA (sha1 byte grezzi) %s\n"
      % hashlib.sha1(io.open(SORGENTE, "rb").read()).hexdigest()[:8])
    P("riferimento `_cura1_corto/scena_000120.pkl.gz` -- STESSA configurazione, flag SPENTO\n\n")
    esiti = []

    # T1 -- default spento
    import re
    m = re.search(r"^TEMPO_UNICO_MITOSI\s*=\s*(True|False)\b", sorg, re.M)
    ok = (m is not None and m.group(1) == "False")
    P("T1    %s IL DEFAULT E' SPENTO: `TEMPO_UNICO_MITOSI = %s`\n"
      % ("PASS" if ok else "FAIL", m.group(1) if m else "ASSENTE"))
    esiti.append(ok)

    # T2 -- il GATE, dall'AST
    rami = rami_del_flag(sorg, "TEMPO_UNICO_MITOSI")
    attese = {"mitosi", "_applica_flag"}
    ok = bool(rami) and set(rami) <= attese
    P("T2    %s GATE (AST): i rami stanno SOLO in %s -> %s\n"
      % ("PASS" if ok else "FAIL", sorted(attese),
         {k: v for k, v in sorted(rami.items())}))
    esiti.append(ok)

    # T3 -- I QUATTRO USI COERENTI SONO INTOCCATI
    ass = assegnamenti(sorg, TORSIONE)
    sporchi = {k: sorted(v & set(NUOVI)) for k, v in ass.items() if v & set(NUOVI)}
    ok = (set(TORSIONE) <= set(ass)) and not sporchi
    P("T3    %s I QUATTRO USI `TORSIONE` SONO INTOCCATI: %s\n"
      % ("PASS" if ok else "FAIL",
         "nessuno legge un nome della cura" if not sporchi else sporchi))
    P("      trovati: %s\n" % sorted(ass))
    P("      -> e' il test che CODIFICA la regola di Luca: dove intenzione e implementazione\n")
    P("         COINCIDONO non si tocca. Se la cura li toccasse, avrebbe curato cio' che non\n")
    P("         era rotto -- e questo lo prende DALL'AST, non dalla mia parola.\n")
    esiti.append(ok)

    # T4/T5 -- byte-inerzia a flag SPENTO, e controllo positivo ACCESO
    import runpy
    import time
    os.chdir(RADICE)
    import soliton_simulator as S
    for nome, acceso in (("SPENTO", False), ("ACCESO", True)):
        d = os.path.join(INERTE, nome)
        try:
            os.makedirs(d)
        except OSError:
            pass
        for f in os.listdir(d):
            if f.endswith(".pkl.gz"):
                os.remove(os.path.join(d, f))
        orig = S._applica_flag

        def _w(a, _v=acceso):
            r = orig(a)
            S.TEMPO_UNICO_MITOSI = _v
            return r
        S._applica_flag = _w
        vecchio = list(sys.argv)
        sys.argv = ["_scena_video.py", "20", d] + COMUNE
        t0 = time.time()
        try:
            runpy.run_path(DRIVER, run_name="__main__")
        finally:
            S._applica_flag = orig
            sys.argv = vecchio
        P("\n  [%s] %.1f s   TEMPO_UNICO_MITOSI = %s\n"
          % (nome, time.time() - t0, S.TEMPO_UNICO_MITOSI))
        p = os.path.join(d, "scena_000120.pkl.gz")
        if not os.path.exists(p):
            P("*** snapshot mancante ***\n")
            esiti.append(False)
            continue
        ug, dv, nc = confronta_snap(RIF120, p, P)
        if not acceso:
            ok = (dv == 0 and ug > 100)
            P("T4    %s BYTE-INERTE spento: %d identici, %d diversi, %d non confrontati\n"
              % ("PASS" if ok else "FAIL", ug, dv, nc))
            P("      -> i `non confrontati` sono i CONTATORI nuovi, che girano anche a flag\n")
            P("         spento di proposito: cosi' il \"prima\" del criterio `K` arriva da qui,\n")
            P("         senza un run in piu'.\n")
        else:
            ok = (dv > 0)
            P("T5    %s CONTROLLO POSITIVO acceso: %d campi diversi\n"
              % ("PASS" if ok else "FAIL", dv))
        esiti.append(ok)

    n = sum(1 for x in esiti if x)
    P("\n" + "=" * 100 + "\nESITO: %d/%d\n" % (n, len(esiti)) + "=" * 100 + "\n")
    P("*** %s ***\n" % ("SIGILLO PASSATO. Il giro corto puo' partire."
                        if n == len(esiti) else
                        "SIGILLO FALLITO: reperto, commit, STOP (par.5)."))
    P("\n!! E IL SIGILLO NON DICE CHE LA CURA SIA GIUSTA: dice che tocca SOLO cio' che era\n")
    P("   incoerente, che a flag spento non cambia un bit, e che acceso fa qualcosa.\n")
    P("   Se la mitosi viva o muoia lo dice il GIRO CORTO, non questo.\n")
    ref.close()
    return 0 if n == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
