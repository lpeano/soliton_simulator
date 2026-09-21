# -*- coding: utf-8 -*-
"""L'ARCO DELL'INNESCO -- misurato all'ISTANTE GIUSTO, che la rigiocata non guarda.

⚠ PERCHE' ESISTE, ed e' un LIMITE DELLO STRUMENTO PRECEDENTE, non un raffinamento.
  `_rigiocata_1200_1230.py` misura `n1` e l'arco di `|anom|` massimo **subito dopo `net.step()`**.
  Ma `nsub` lo calcola il codice **all'INGRESSO di `step()`**, cioe' **dopo** `mitosi()`,
  `rilassa_disegno()`, `memoria_hebbiana_moto()` e `scuoti_vuoto()`. **I due istanti NON
  coincidono, ed e' misurato quanto:**
      riga 1125 della rigiocata, DOPO step():          n1 = 1,     nsub = 4
      py-spy DENTRO step() del 1126, all'INGRESSO:     n1 = 22591, nsub = 22591
  **Lo stesso passo, due numeri che differiscono di quattro ordini.** L'arco colpevole vive
  nell'istante che la rigiocata **non guarda**.

COSA FA: ricostruisce lo stato **all'ingresso di ogni `step()`** -- cioe' esattamente dove il
  codice calcola `nsub` -- e registra l'arco di `|anom|` MASSIMO in QUEL punto. Nient'altro.

⚠ NON INTEGRA IL PASSO ESPLOSIVO, e non per prudenza: **non gli serve.** La misura avviene PRIMA
  di chiamare `step()`, quindi quando `n1` supera la soglia lo strumento **ha gia' la risposta** e
  si ferma **senza pagare i 22591 sotto-passi**. E' la differenza fra questo strumento e l'altro.

⚠ E' PURE-READ SUL SIMULATORE: non tocca il codice, non cambia flag, non scrive stato.
  L'unica cosa che fa e' leggere `net.psi`, `net.peq`, `net.i`, `net.j` fra una chiamata e l'altra.
ASCII PURO.
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
sys.path.insert(0, RADICE)

DA = 1080
FINO = None      # ⚠ `--fino=N`: si misura l'ingresso del passo N e SI ESCE SENZA INTEGRARLO.
for _a in sys.argv[1:]:
    if _a.startswith("--da="):
        DA = int(_a.split("=", 1)[1])
    if _a.startswith("--fino="):
        FINO = int(_a.split("=", 1)[1])
SNAP = os.path.join(RADICE, "csv", "_test_fork", "_ab_D", "scena_%06d.pkl.gz" % DA)
OUT = os.path.join(RADICE, "csv", "_test_fork", "_diag_D", "ARCO_INNESCO_%06d.txt" % DA)
SOGLIA_N1 = 100      # la STESSA soglia della rigiocata, e qui si applica PRIMA di integrare
MAX_PASSI = 125
N_TOP = 8            # quanti archi di `|anom|` piu' grande si stampano al momento dell'innesco
N_VUOTO, N0_SEMINA = 900, 2391


def main():
    os.chdir(RADICE)
    sys.argv = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
                "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
                "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
                "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
                "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--chi-coop",
                "--scala-min", "--coes-adim", "--plast-din", "--viriale", "--olon-part"]
    import soliton_simulator as S
    a = S._cli(); S._applica_regime(a); S._applica_flag(a)
    for f in ("CHI_COOP", "SCALA_MIN", "COES_ADIM"):
        if not getattr(S, f):
            raise SystemExit("[innesco] %s e' SPENTO: non e' la configurazione del ramo D" % f)
    net = S.net
    if not net.carica_stato(SNAP):
        raise SystemExit("[innesco] `carica_stato` ha RIFIUTATO %s" % SNAP)

    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    W = o.write
    W("# L'ARCO DELL'INNESCO -- misura ALL'INGRESSO di `step()`, dove il codice calcola `nsub`\n")
    W("# partenza: snapshot %d, n = %d, archi = %d\n" % (DA, net.n, len(net.d)))
    W("# soglia: ci si ferma quando n1 > %d, e ci si ferma PRIMA di integrare quel passo.\n"
      % SOGLIA_N1)
    W("# origine: vuoto < %d, massa < %d, nato >= %d\n\n" % (N_VUOTO, N0_SEMINA, N0_SEMINA))
    W("%5s | %11s | %-46s | %12s %12s\n"
      % ("passo", "n1", "ARCO con |anom| MASSIMO all'INGRESSO", "min(peq)", "median(peq)"))
    W("-" * 108 + "\n")

    def orig(x):
        return "V" if x < N_VUOTO else ("M" if x < N0_SEMINA else "N")

    def misura():
        """ESATTAMENTE la catena del codice: :4167 -> :4215 -> :4218 -> :4264 (ramo VERLET)."""
        n = net.n
        I = np.abs(net.psi[:n]) ** 2
        i, j = np.asarray(net.i), np.asarray(net.j)
        m = (i < n) & (j < n)
        rho = 0.5 * (I[i[m]] + I[j[m]])
        peq = np.asarray(net.peq)[m]
        anom = (rho - peq) / np.maximum(peq, 1e-9)
        src = S.ALPHA_M * anom
        n1 = float(np.ceil(np.abs(src).max() * S.DT / (0.02 * S.CS_M)))
        return n1, i[m], j[m], rho, peq, anom

    PPF = int(S.PASSI_PER_FRAME)
    innesco = None
    for k in range(1, MAX_PASSI + 1):
        passo = DA + k
        if (k - 1) % PPF == 0:
            S.passo_test()
        S.scuoti_vuoto(net)
        # ⚠ LA MISURA STA QUI: dopo `scuoti_vuoto` e PRIMA di `step()`, cioe' nello stesso punto
        #   in cui `step()` calcolera' `nsub`. E' l'istante che la rigiocata non guarda.
        n1, ii, jj, rho, peq, anom = misura()
        km = int(np.argmax(np.abs(anom)))
        W("%5d | %11.0f | %-46s | %12.4e %12.4e\n"
          % (passo, n1,
             "%d-%d(%s%s) rho=%.2e peq=%.2e anom=%.3e"
             % (int(ii[km]), int(jj[km]), orig(int(ii[km])), orig(int(jj[km])),
                rho[km], peq[km], anom[km]),
             float(np.min(peq)), float(np.median(peq))))
        o.flush()
        if n1 > SOGLIA_N1 or passo == FINO:
            innesco = passo
            if n1 > SOGLIA_N1:
                W("\n*** INNESCO AL PASSO %d: n1 = %.0f SUPERA LA SOGLIA %d.\n"
                  % (passo, n1, SOGLIA_N1))
            else:
                W("\n*** PASSO %d RAGGIUNTO (`--fino`): si misura l'INGRESSO e NON si integra.\n"
                  % passo)
            W("*** MI FERMO QUI SENZA INTEGRARE IL PASSO: la misura e' gia' fatta.\n\n")

            # ⚠ L'ARCO COL `peq` PIU' BASSO -- e' LUI il candidato, non quello di `|anom|` massimo.
            #   `min(peq)` decade GEOMETRICAMENTE mentre `median(peq)` SALE: un arco esce dalla
            #   popolazione. Il suo `anom` non e' ancora grande PERCHE' anche il suo `rho` e'
            #   piccolo -- esplode quando `rho` risale con `peq` rimasto indietro.
            kp = int(np.argmin(peq))
            W("L'ARCO COL `peq` PIU' BASSO -- il candidato:\n")
            W("  arco %d-%d (%s%s)   peq=%.6e   rho=%.6e   anom=%.6e\n"
              % (int(ii[kp]), int(jj[kp]), orig(int(ii[kp])), orig(int(jj[kp])),
                 peq[kp], rho[kp], anom[kp]))
            _n = net.n
            _I = np.abs(net.psi[:_n]) ** 2
            W("  I dei due nodi: I[%d]=%.6e  I[%d]=%.6e\n"
              % (int(ii[kp]), _I[int(ii[kp])], int(jj[kp]), _I[int(jj[kp])]))
            W("  eta dei due nodi: %.3f  %.3f   (TAU_A = %s)\n\n"
              % (float(np.asarray(net.eta)[int(ii[kp])]),
                 float(np.asarray(net.eta)[int(jj[kp])]), S.TAU_A))

            W("I %d ARCHI COL `peq` PIU' BASSO:\n" % N_TOP)
            W("%4s | %14s | %12s %12s %14s | %8s\n"
              % ("#", "arco", "peq", "rho", "anom", "origine"))
            W("-" * 78 + "\n")
            for r, c in enumerate(np.argsort(peq)[:N_TOP]):
                c = int(c)
                W("%4d | %6d-%-7d | %12.4e %12.4e %14.4e | %8s\n"
                  % (r + 1, int(ii[c]), int(jj[c]), peq[c], rho[c], anom[c],
                     orig(int(ii[c])) + orig(int(jj[c]))))
            W("\n")
            ordine = np.argsort(-np.abs(anom))[:N_TOP]
            W("I %d ARCHI CON |anom| PIU' GRANDE, in quell'istante:\n" % N_TOP)
            W("%4s | %14s | %12s %12s %14s | %10s\n"
              % ("#", "arco", "rho", "peq", "anom", "origine"))
            W("-" * 82 + "\n")
            for r, c in enumerate(ordine):
                c = int(c)
                W("%4d | %6d-%-7d | %12.4e %12.4e %14.4e | %10s\n"
                  % (r + 1, int(ii[c]), int(jj[c]), rho[c], peq[c], anom[c],
                     orig(int(ii[c])) + orig(int(jj[c]))))
            W("\nQUANTI ARCHI HANNO `peq` AL PAVIMENTO O SOTTO (<= 1e-9): %d su %d\n"
              % (int(np.sum(peq <= 1e-9)), len(peq)))
            break
        net.step()
        net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()

    if innesco is None:
        W("\n*** In %d passi (da %d a %d) `n1` NON ha superato %d ALL'INGRESSO di `step()`.\n"
          % (MAX_PASSI, DA + 1, DA + MAX_PASSI, SOGLIA_N1))
        W("    Va detto: o l'innesco e' altrove, o la ricostruzione dell'istante non e' fedele.\n")
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
