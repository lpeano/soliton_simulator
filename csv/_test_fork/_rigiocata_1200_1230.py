# -*- coding: utf-8 -*-
"""LA RIGIOCATA DEL RAMO D DA UNO SNAPSHOT -- il nodo che si accende, se c'e'.

⚠⚠ IL NOME DEL FILE DICE `1200_1230` ED E' STORICO: LA PREMESSA DI ALLORA ERA SBAGLIATA.
  **L'esplosione NON e' dopo il passo 1200.** Cronologia dal registro dei run e dal disco:
  ```
  12:40   ultimo frame pulito, il 185                       passo 1110
  12:58   `nsub = 22591` catturato                          ultimo snapshot su disco: 1080
  13:02-13:14  compare lo snapshot 1200                     -> il run HA SUPERATO il 1200
  13:14   fermato al frame 205 (passo 1230)                 stack in `rilassa_disegno`,
                                                            cioe' FUORI dal ciclo dei sotto-passi
  ```
  **E' un PICCO TRANSITORIO fra il 1110 e il 1200, e il run si e' ripreso DA SOLO.**
  **La conferma indipendente sta nei TIMESTAMP degli snapshot:** ogni intervallo di 120 passi costa
  **7 minuti**; il `1080 -> 1200` ne e' costato **34** -- cinque volte tanto -- **e lo snapshot
  1200 e' arrivato lo stesso**.

⚠ PERCHE' ESISTE: il sistema e' deterministico e lo snapshot porta anche lo stato dell'RNG,
  quindi ripartire dal 1080 ricostruisce **esattamente** la finestra in cui l'esplosione vive --
  che **nessuno snapshot copre**, perche' fra 1080 e 1200 non ce n'e' nessuno.
  Il punto di partenza e' l'opzione **`--da=<passo>`** (default **1080**).

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
import io
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, RADICE)   # il simulatore vive nella RADICE, non qui
# ⚠ IL PUNTO DI PARTENZA E' PARAMETRICO, E IL 1200 ERA SBAGLIATO -- rilievo di Luca.
#   L'esplosione NON e' dopo il 1200: e' un PICCO TRANSITORIO fra il 1110 e il 1200, e **il
#   run si e' ripreso da solo**. LA PROVA C'ERA IN DUE POSTI, E NON E' STATA LETTA:
#     (a) `stack_STOP_finale.txt` mostra il processo in `rilassa_disegno`, cioe' FUORI dal
#         ciclo dei sotto-passi. Era stato fatto un `grep` di `nsub`, non trovato nulla, e
#         tirato dritto: **l'ASSENZA di quelle variabili diceva che era in un'altra funzione**;
#     (b) i TIMESTAMP degli snapshot: `0960 -> 1080` in SETTE minuti, come ogni altro
#         intervallo, e **`1080 -> 1200` in TRENTAQUATTRO** -- cinque volte tanto -- **e lo
#         snapshot 1200 arriva lo stesso**. Il run ha ATTRAVERSATO l'esplosione.
DA = 1080
for _a in sys.argv[1:]:
    if _a.startswith("--da="):
        DA = int(_a.split("=", 1)[1])
SNAP = os.path.join(RADICE, "csv", "_test_fork", "_ab_D", "scena_%06d.pkl.gz" % DA)
OUT = os.path.join(RADICE, "csv", "_test_fork", "_diag_D",
                   "RIGIOCATA_%06d_avanti.txt" % DA)
SOGLIA_N1 = 100      # ⚠ SOGLIA DICHIARATA, e RESTA: il mandato chiede *la stessa* soglia.
#   Non si integra l'esplosione: si vuole il PASSO in cui scatta e l'ARCO su cui vive, non la
#   sua evoluzione. Se scatta, ci si ferma li'.
MAX_PASSI = 125      # dal 1080 si arriva al 1200 e oltre: la finestra dev'essere COPERTA
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
    W("# RIGIOCATA `%d -> %d` DEL RAMO D -- il picco TRANSITORIO che il run ha attraversato\n"
      % (DA, DA + MAX_PASSI))
    W("# soglia DICHIARATA: ci si ferma quando n1 > %d. Max %d passi.\n" % (SOGLIA_N1, MAX_PASSI))
    W("# ramp = min(1, eta/TAU_A), letto dal codice a :2958. TAU_A = %s\n" % S.TAU_A)
    W("# origine: vuoto < %d, massa < %d, nato >= %d\n" % (N_VUOTO, N0_SEMINA, N0_SEMINA))
    W("# stato di partenza: n = %d, archi = %d\n\n" % (net.n, len(net.d)))

    def orig(x):
        return "V" if x < N_VUOTO else ("M" if x < N0_SEMINA else "N")

    W("%5s | %11s %5s %6s %11s | %7s | %-40s | %-30s | %s\n"
      % ("passo", "n1", "n2", "n3", "nsub", "secondi", "ARCO con |anom| MASSIMO",
         "arco candidato 2773-4158", "nati piu' giovani (eta | I | ramp)"))
    W("-" * 215 + "\n")

    # ⚠ IL CICLO DEV'ESSERE QUELLO DEL DRIVER, E LA PRIMA VERSIONE NON LO ERA.
    #   Il driver (`:35-37`) e la rigiocata gia' sigillata (`_rigiocata_0_120.py:188-192`) chiamano
    #   `passo_test()` UNA VOLTA OGNI `PASSI_PER_FRAME` passi -- *«una volta per frame: fa avanzare
    #   le fasi»*. **Io non lo chiamavo**, quindi la rigiocata NON ERA FEDELE e i suoi numeri non
    #   erano confrontabili col run vero. Trovato leggendo la rigiocata sigillata, non dai numeri:
    #   quelli sembravano ragionevoli.
    PPF = int(S.PASSI_PER_FRAME)
    fermato = None
    for k in range(1, MAX_PASSI + 1):
        passo = DA + k
        _t0 = time.time()
        if (k - 1) % PPF == 0:
            S.passo_test()
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

        # ⚠ QUESTA RIGA E' FINITA DENTRO L'`else:` QUI SOPRA, E PER 45 PASSI NON HA SCRITTO NULLA.
        #   L'ancora della sostituzione era `    W("%5d | ...` -- **una SOTTOSTRINGA** della riga
        #   vera, indentata a OTTO spazi. `t.count(v) == 1` era soddisfatto, ma il match cadeva a
        #   offset 4, e il risultato aveva DODICI spazi: sintatticamente valido, semanticamente nel
        #   ramo sbagliato. `py_compile` passava.
        #   **P1-quater, QUARTA OCCORRENZA, e in una forma NUOVA:** asserire che l'ancora sia UNICA
        #   non basta se l'ancora e' un FRAMMENTO di riga. **L'ancora dev'essere una RIGA INTERA,
        #   col suo `\n` iniziale**, altrimenti l'unicita' non dice dove cade il match.
        W("%5d | %11.0f %5d %6.0f %11d | %7.1f | %-40s | %-30s | %s\n"
          % (passo, n1, 1, n3, nsub, time.time() - _t0, smax, scan, sgio))
        o.flush()
        if n1 > SOGLIA_N1:
            fermato = passo
            W("\n*** n1 = %.0f SUPERA LA SOGLIA %d AL PASSO %d: MI FERMO QUI, come dichiarato.\n"
              % (n1, SOGLIA_N1, passo))
            break
        net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()

    if fermato is None:
        W("\n*** In %d passi (da %d a %d) `n1` NON ha superato %d.\n"
          % (MAX_PASSI, DA + 1, DA + MAX_PASSI, SOGLIA_N1))
        W("    La finestra 1110-1200 E' COPERTA: se il picco non compare, allora la FEDELTA'\n"
          "    della rigiocata va SIGILLATA, e va detto. Non si raffina la soglia.\n")
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
