# -*- coding: utf-8 -*-
"""FASE A — la PARENTELA e' ricostruibile, e quanto vale chi padre-figlio alla nascita?

DOMANDA
-------
Alla mitosi il figlio eredita il Bloch del padre per COPIA ESATTA (`_eredita_spinore_figli`,
righe ~1133-1170). Quindi ogni nascita crea una coppia perfettamente correlata. Ma la misura dice
chi = 90 gradi ovunque. Il problema non e' "manca un meccanismo ordinante": e' un BILANCIO fra un
tasso di CREAZIONE (la mitosi) e un tasso di DISTRUZIONE (rumore + precessione mutua).

Questo script chiude la FASE A: verifica il fatto e stabilisce se l'albero genealogico si puo'
ricostruire, perche' senza parentela il tasso di distruzione si potrebbe misurare solo per proxy.

COSA MISURA
-----------
1. per ogni nodo NUOVO, quanti genitori ha e se il padre `a` (quello da cui eredita) e'
   identificabile: nell'arco (a, m) il padre sta nel lato `i`, il figlio nel lato `j`
   (costruzione in `mitosi`, righe ~3172-3173);
2. `chi` padre-figlio SUBITO dopo la nascita -> deve essere 0 se l'eredita' e' una copia esatta;
3. di quanto si e' spostato il PADRE nello stesso passo -> e' il riferimento che dice se la
   correlazione appena creata ha una speranza di vita.

PUREZZA
-------
Legge SOLO array di stato (`net.i`, `net.j`, `net._nb`). NON chiama `calcola_psi()` ne' `ritmo()`,
che mutano cache di continuita' lette dalla dinamica (`psi`, `_psi_prec`). Non consuma `net.rng`.
Il ciclo di evoluzione e' quello canonico del batch, nello stesso ordine.

VALORE-NULL (par.9 di CLAUDE.md, sempre accanto alla misura)
------------------------------------------------------------
direzioni di Bloch CASUALI -> chi = 90.000 +- 39.171 gradi. Un `chi` vicino a quello NON e' un
risultato: e' l'assenza di risultato.

USO
---
python csv/_test_fork/_parentela_bloch.py [--passi N] [--seed S]
"""
import argparse
import contextlib
import io
import os
import sys

import numpy as np

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CHI_NULL_MEDIA = 90.000      # direzioni casuali: <chi> = 90 gradi esatti
CHI_NULL_STD = 39.171        # e la loro dispersione


def _angolo(u, v):
    """Angolo fra due direzioni, in gradi. Nessuna normalizzazione assunta."""
    c = float(np.dot(u, v) / max(np.linalg.norm(u) * np.linalg.norm(v), 1e-30))
    return float(np.degrees(np.arccos(np.clip(c, -1.0, 1.0))))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--passi", type=int, default=40)
    ap.add_argument("--seed", type=int, default=1)
    opz = ap.parse_args()

    os.chdir(RADICE)
    sys.path.insert(0, RADICE)
    sys.argv = ["soliton_simulator.py", "--batch", "--nmasse", "3", "--sep", "8",
                "--seed", str(opz.seed), "--passi", "1", "--ogni", "1000",
                "--db-ogni", "100000",
                "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto", "--chi-core",
                "--calore-scal", "--deparam-orologio", "--verlet", "--cs-dinamico",
                "--csv", os.path.join(os.environ.get("TMP", "."), "_parentela.csv")]
    import soliton_simulator as S

    a = S._cli()
    S._applica_regime(a)
    with contextlib.redirect_stdout(io.StringIO()):
        S._applica_flag(a)        # costruisce la rete e la riscalda (300 passi)
    net = S.net

    print("flag: SCUOTIMENTO=%s SYNC_UPDATE=%s SPINORE_CORRETTO=%s CAMPO_SPINORIALE=%s"
          % (S.SCUOTIMENTO, S.SYNC_UPDATE, S.SPINORE_CORRETTO, S.CAMPO_SPINORIALE))
    print("stato dopo riscaldamento: n=%d archi=%d   (seme %d)" % (net.n, len(net.i), opz.seed))

    def passo(rete):
        S.scuoti_vuoto(rete); rete.step(); rete.mitosi()
        rete.rilassa_disegno(); rete.memoria_hebbiana_moto()

    nuovi = due_genitori = padre_identificato = 0
    chi_nascita = []
    moto_padre = []
    for _ in range(opz.passi):
        n_prima = net.n
        nb_prima = np.array(net._nb[:n_prima], float)     # copia di sola lettura
        passo(net)
        if net.n == n_prima:
            continue
        ii, jj = net.i, net.j
        for m in range(n_prima, net.n):
            gen_i = [int(x) for x in ii[jj == m] if x < n_prima]   # archi (x, m) -> x e' il padre `a`
            gen_j = [int(x) for x in jj[ii == m] if x < n_prima]   # archi (m, x) -> x e' `b`
            nuovi += 1
            if len(gen_i) + len(gen_j) == 2:
                due_genitori += 1
            if len(gen_i) == 1:
                padre_identificato += 1
                padre = gen_i[0]
                chi_nascita.append(_angolo(net._nb[padre], net._nb[m]))
                moto_padre.append(_angolo(nb_prima[padre], net._nb[padre]))

    print()
    print("nuovi nodi osservati             : %d" % nuovi)
    print("  con ESATTAMENTE 2 genitori     : %d  (%.1f%%)"
          % (due_genitori, 100.0 * due_genitori / max(nuovi, 1)))
    print("  con il padre `a` identificabile: %d  (%.1f%%)"
          % (padre_identificato, 100.0 * padre_identificato / max(nuovi, 1)))

    if chi_nascita:
        ch = np.array(chi_nascita)
        mp = np.array(moto_padre)
        print()
        print("chi PADRE-FIGLIO alla nascita (gradi), n=%d:" % len(ch))
        print("   media %.4f  mediana %.4f  min %.4f  max %.4f"
              % (ch.mean(), np.median(ch), ch.min(), ch.max()))
        print("   VALORE-NULL (direzioni casuali): %.3f +- %.3f" % (CHI_NULL_MEDIA, CHI_NULL_STD))
        print()
        print("spostamento del PADRE nel passo della nascita (gradi), n=%d:" % len(mp))
        print("   media %.4f  mediana %.4f  min %.4f  max %.4f"
              % (mp.mean(), np.median(mp), mp.min(), mp.max()))
        print("   confronta col VALORE-NULL: uno spostamento ~90 gradi in UN passo significa")
        print("   che il Bloch decorrela DA SE' STESSO in un tick.")
    else:
        print("\nnessuna nascita nei passi osservati: aumenta --passi.")

    print()
    print("n finale=%d  nati=%d  coppie Schwinger=%d" % (net.n, net.nati, net.coppie_nate))


if __name__ == "__main__":
    main()
