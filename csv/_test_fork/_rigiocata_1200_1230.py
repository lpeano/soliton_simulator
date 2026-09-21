# -*- coding: utf-8 -*-
"""LA RIGIOCATA `1200 -> 1230` DEL RAMO D -- il nodo che si accende, se c'e'.

⚠ PERCHE' ESISTE: il ramo D e' stato fermato al passo ~1230 con `nsub = 22591`, ma **l'ultimo
  snapshot e' il 1200 e li' `n1` vale 1**. **L'innesco vive nei ~30 passi in mezzo, e NESSUNO
  SNAPSHOT LO COPRE.** Il sistema e' deterministico e lo snapshot porta anche lo stato dell'RNG:
  ripartire dal 1200 ricostruisce esattamente cio' che ha preceduto l'esplosione.

⚠ CI SI FERMA ALL'INNESCO, NON SI INTEGRA L'ESPLOSIONE: quando `n1` supera `SOGLIA_N1` si
  registra lo stato di quel passo e si esce. **Senza, questa rigiocata si pianterebbe come il ramo
  D**, e per la stessa ragione.

COSA REGISTRA, a OGNI passo:
  * `n1`, `n2`, `n3`, `nsub`, calcolati **come il codice** *(`:4264`, ramo VERLET)*;
  * ⚠ **l'arco dove `|anom|` e' MASSIMO** -- indice, i due nodi, `rho`, `peq`, `anom`, e l'ORIGINE
    dei due nodi. **E' il punto chiave: se il candidato e' sbagliato, il colpevole vero compare
    qui da solo.** Si registra SEMPRE, non solo quando conferma;
  * l'arco **`2773-4158`**, il candidato di Claude web *(cercato per COPPIA DI NODI, mai per indice:
    gli archi si riordinano)*;
  * i **NATI PIU' GIOVANI** *(i `N_GIOVANI` con `eta` minima)*: `I`, `eta`, e il peso di
    maturazione **`ramp = min(1, eta/TAU_A)`** -- **letto dal codice a `:2958`, non dedotto**.

⚠ LA RICOSTRUZIONE E' FEDELE PER COSTRUZIONE, e va detto come: dentro `step()` il codice calcola
  `psi` -> `rho`, POI aggiorna `peq`, POI usa il `peq` aggiornato per `anom`. Quindi leggere
  `net.psi` e `net.peq` SUBITO DOPO `step()` (e prima di `mitosi()`) da' **esattamente** le
  quantita' che quel passo ha usato.
ASCII PURO.
"""
import glob
import io
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, RADICE)   # il simulatore vive nella RADICE, non qui
SNAP = os.path.join(RADICE, "csv", "_test_fork", "_ab_D", "scena_001200.pkl.gz")
OUT = os.path.join(RADICE, "csv", "_test_fork", "_diag_D", "RIGIOCATA_1200_1230.txt")
SOGLIA_N1 = 100      # ⚠ SOGLIA DICHIARATA: sopra questa ci si ferma. Non si integra l'esplosione.
MAX_PASSI = 60       # oltre il 1260 non si va: l'innesco misurato e' prima del 1230
N_GIOVANI = 5
CAND = (2773, 4158)
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
            raise SystemExit("[rigiocata] %s e' SPENTO: non e' la configurazione del ramo D" % f)
    net = S.net
    if not net.carica_stato(SNAP):
        raise SystemExit("[rigiocata] `carica_stato` ha RIFIUTATO %s -- blob diverso?" % SNAP)

    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    W = o.write
    W("# RIGIOCATA `1200 -> 1230` DEL RAMO D -- l'innesco che nessuno snapshot copre\n")
    W("# soglia DICHIARATA: ci si ferma quando n1 > %d. Max %d passi.\n" % (SOGLIA_N1, MAX_PASSI))
    W("# ramp = min(1, eta/TAU_A), letto dal codice a :2958. TAU_A = %s\n" % S.TAU_A)
    W("# origine: vuoto < %d, massa < %d, nato >= %d\n" % (N_VUOTO, N0_SEMINA, N0_SEMINA))
    W("# stato di partenza: n = %d, archi = %d\n\n" % (net.n, len(net.d)))

    def orig(x):
        return "V" if x < N_VUOTO else ("M" if x < N0_SEMINA else "N")

    W("%5s | %8s %5s %5s %8s | %-34s | %-30s | %s\n"
      % ("passo", "n1", "n2", "n3", "nsub", "ARCO con |anom| MASSIMO",
         "arco candidato 2773-4158", "nati piu' giovani (eta | I | ramp)"))
    W("-" * 190 + "\n")

    fermato = None
    for k in range(1, MAX_PASSI + 1):
        passo = 1200 + k
        S.scuoti_vuoto(net)
        net.step()
        n = net.n
        I = np.abs(net.psi[:n]) ** 2
        i, j = np.asarray(net.i), np.asarray(net.j)
        m = (i < n) & (j < n)
        rho = 0.5 * (I[i[m]] + I[j[m]])
        peq = np.asarray(net.peq)[m]
        anom = (rho - peq) / np.maximum(peq, 1e-9)
        src = S.ALPHA_M * anom
        cs_max = S.CS_M
        n1 = float(np.ceil(np.abs(src).max() * S.DT / (0.02 * cs_max)))
        beta_max = float(np.max(np.abs(net.vd))) if len(net.vd) else 0.0
        n3 = float(np.ceil(np.abs(net.vd).max() * S.DT
                           / (0.05 * max(float(np.median(net.d)), 0.1) * cs_max / S.CS_M)))
        nsub = int(max(4, n1, 1, n3))

        # ⚠ l'arco di |anom| MASSIMO, registrato SEMPRE
        km = int(np.argmax(np.abs(anom)))
        ii, jj = int(i[m][km]), int(j[m][km])
        smax = ("%d-%d(%s%s) rho=%.2e peq=%.2e anom=%.3e"
                % (ii, jj, orig(ii), orig(jj), rho[km], peq[km], anom[km]))

        # l'arco candidato, cercato per COPPIA DI NODI
        sel = np.where(((i[m] == CAND[0]) & (j[m] == CAND[1]))
                       | ((i[m] == CAND[1]) & (j[m] == CAND[0])))[0]
        if len(sel):
            c = int(sel[0])
            scan = "rho=%.2e peq=%.2e anom=%.3e" % (rho[c], peq[c], anom[c])
        else:
            scan = "(arco ASSENTE)"

        # i nati piu' giovani
        eta = np.asarray(net.eta)[:n]
        nati = np.arange(n) >= N0_SEMINA
        if nati.any():
            idx = np.where(nati)[0]
            gio = idx[np.argsort(eta[idx])[:N_GIOVANI]]
            ramp = np.minimum(1.0, eta / S.TAU_A)
            sgio = " ".join("%d:%.3f|%.1e|%.3f" % (g, eta[g], I[g], ramp[g]) for g in gio)
        else:
            sgio = "(nessun nato)"

        W("%5d | %8.0f %5d %5.0f %8d | %-34s | %-30s | %s\n"
          % (passo, n1, 1, n3, nsub, smax, scan, sgio))
        o.flush()
        if n1 > SOGLIA_N1:
            fermato = passo
            W("\n*** n1 = %.0f SUPERA LA SOGLIA %d AL PASSO %d: MI FERMO QUI, come dichiarato.\n"
              % (n1, SOGLIA_N1, passo))
            break
        net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()

    if fermato is None:
        W("\n*** In %d passi `n1` NON ha superato %d. O la rigiocata non e' fedele, o l'innesco\n"
          "    e' piu' avanti. Va detto, non raffinato.\n" % (MAX_PASSI, SOGLIA_N1))
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
