# -*- coding: utf-8 -*-
"""CHI FA SCAPPARE `d0`: LA SOMMA PER SCRITTORE, separata in SALITE e DISCESE. [SOLA MISURA]

⚠ NESSUNA CURA. Si misura e basta.

COSA MISURA, e perche' cosi':
  Ogni scrittore di `d0` ha un punto di traccia gia' nel simulatore (`_traccia_d0(sito, prima)`).
  **Non si tocca il simulatore:** si SOSTITUISCE quel metodo con uno che, allo stesso punto,
  calcola cio' che serve -- **la somma ALGEBRICA dei `delta` positivi e di quelli negativi,
  separate** -- e poi non fa altro. E' PURE-READ: legge `prima` e `self.d0`, non scrive stato.

⚠ PERCHE' SEPARARE SALITE E DISCESE, e non guardare il saldo: **un saldo piccolo puo' nascere da
  due termini enormi che quasi si cancellano**, e quello e' un sistema fragile; oppure da due
  termini piccoli, e quello e' un sistema quieto. **Il saldo da solo non distingue i due casi.**

⚠ I SITI CHE CONCATENANO (`S01`, `S06` mitosi, `S07` Schwinger) cambiano la LUNGHEZZA di `d0`:
  li' il `delta` elemento-per-elemento NON ESISTE, e si registra soltanto il cambio di lunghezza.
  **Dichiarato, non nascosto:** quei siti compaiono nella tabella con `n/d`.

LA PREVISIONE DA VERIFICARE, scritta PRIMA (mandato di Luca, 2026-09-21 22:38):
  **`S09` + `S10` hanno saldo netto VERSO L'ALTO e CRESCONO con `median(d0)`.**
  Se il saldo e' verso il basso, o se il rapporto `saldo / median(d0)` NON cresce, **la previsione
  CADE e va detto.**
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
sys.path.insert(0, RADICE)

PASSI = 120
LIMITE_S = 2100          # ⚠ se sfora, si ferma PULITA e scrive cio' che ha
for _a in sys.argv[1:]:
    if _a.startswith("--passi="):
        PASSI = int(_a.split("=", 1)[1])
    if _a.startswith("--limite="):
        LIMITE_S = int(_a.split("=", 1)[1])
OUT = os.path.join(RADICE, "csv", "_test_fork", "_diag_D", "SOMMA_PER_SCRITTORE_d0.txt")

# LA CONFIGURAZIONE DELLA VALIDAZIONE, identica
ARGV = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
        "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
        "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
        "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
        "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--chi-coop",
        "--coes-adim", "--plast-din", "--viriale", "--olon-part",
        "--peq-esatto", "--peq-nascita-locale", "--scala-min-passo", "--coes-causale",
        "--anom-simm", "--invarianti=on"]

CONTI = {}          # sito -> dict(su, giu, n_su, n_giu, giri, salta)
PER_PASSO = []      # (passo, median_d0, {sito: saldo})


def main():
    os.chdir(RADICE)
    sys.argv = list(ARGV)
    import soliton_simulator as S
    S.TRACCIA_D0 = True
    a = S._cli(); S._applica_regime(a); S._applica_flag(a)
    for f in ("PEQ_ESATTO", "PEQ_NASCITA_LOCALE", "SCALA_MIN_PASSO", "COES_CAUSALE",
              "ANOM_SIMM", "INVARIANTI"):
        if not getattr(S, f):
            raise SystemExit("[d0] %s e' SPENTO: non e' la configurazione della validazione" % f)

    corrente = {}

    def traccia(self, sito, prima, pavimento=None):
        """SOSTITUISCE `_traccia_d0`. PURE-READ: legge e somma, non scrive stato."""
        c = CONTI.setdefault(sito, dict(su=0.0, giu=0.0, n_su=0, n_giu=0, giri=0, salta=0))
        c["giri"] += 1
        dopo = np.asarray(self.d0, dtype=float)
        pri = np.asarray(prima, dtype=float)
        if len(pri) != len(dopo):
            c["salta"] += 1          # sito che CONCATENA: il delta non esiste
            return
        dx = dopo - pri
        su = float(np.sum(dx[dx > 0.0]))
        giu = float(np.sum(dx[dx < 0.0]))
        c["su"] += su; c["giu"] += giu
        c["n_su"] += int(np.sum(dx > 0.0)); c["n_giu"] += int(np.sum(dx < 0.0))
        corrente[sito] = corrente.get(sito, 0.0) + su + giu

    S.Rete._traccia_d0 = traccia

    S._NMASSE_VIDEO["n"] = 3; S._NMASSE_VIDEO["sep"] = 4.0; S._NMASSE_VIDEO["size"] = None
    S.avvia_test("N-MASSE")()
    net = S.net
    S.stato["nframe"] = 0
    PPF = int(S.PASSI_PER_FRAME)
    t0 = time.time()
    fatti = 0
    fermato = None
    for k in range(1, PASSI + 1):
        if (k - 1) % PPF == 0:
            S.passo_test()
        corrente.clear()
        S.scuoti_vuoto(net); net.step(); net.mitosi()
        net.rilassa_disegno(); net.memoria_hebbiana_moto()
        fatti = k
        PER_PASSO.append((k, float(np.median(net.d0)), dict(corrente)))
        if time.time() - t0 > LIMITE_S:
            fermato = "LIMITE DI TEMPO (%d s): fermata PULITA al passo %d" % (LIMITE_S, k)
            break

    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    W = o.write
    W("# CHI FA SCAPPARE `d0` -- LA SOMMA PER SCRITTORE, SALITE e DISCESE separate\n")
    W("# configurazione: quella della VALIDAZIONE (sei cure accese). Passi fatti: %d su %d.\n"
      % (fatti, PASSI))
    W("# tempo: %.1f s%s\n" % (time.time() - t0, "" if fermato is None else "   *** %s" % fermato))
    W("# SOLA MISURA: nessuna cura, nessuna modifica al simulatore.\n")
    W("#\n# ⚠ I siti che CONCATENANO cambiano la lunghezza di `d0`: li' il delta\n")
    W("#   elemento-per-elemento NON ESISTE, e la riga porta `n/d`. Dichiarato.\n\n")

    W("%-20s %14s %14s %14s | %10s %10s | %6s %6s\n"
      % ("scrittore", "SALITE", "DISCESE", "SALDO", "|saldo|/tot", "saldo/giro",
         "giri", "salta"))
    W("-" * 112 + "\n")
    tot_saldo = 0.0
    for sito in sorted(CONTI):
        c = CONTI[sito]
        saldo = c["su"] + c["giu"]
        tot = c["su"] - c["giu"]
        if c["giri"] == c["salta"]:
            W("%-20s %14s %14s %14s | %10s %10s | %6d %6d\n"
              % (sito, "n/d", "n/d", "n/d", "n/d", "n/d", c["giri"], c["salta"]))
            continue
        tot_saldo += saldo
        W("%-20s %14.6e %14.6e %14.6e | %10.4f %10.3e | %6d %6d\n"
          % (sito, c["su"], c["giu"], saldo, abs(saldo) / max(tot, 1e-300),
             saldo / max(c["giri"] - c["salta"], 1), c["giri"], c["salta"]))
    W("-" * 112 + "\n")
    W("%-20s %14s %14s %14.6e\n" % ("SALDO TOTALE", "", "", tot_saldo))
    W("\n")

    # ---------------------------------------------------------------- S09 e S10
    W("=" * 112 + "\n")
    W("LA PREVISIONE DI LUCA, scritta PRIMA: `S09` + `S10` hanno saldo netto VERSO L'ALTO\n")
    W("e CRESCONO con `median(d0)`.\n")
    W("=" * 112 + "\n")
    due = [s for s in CONTI if s.startswith("S09") or s.startswith("S10")]
    if not due:
        W("*** `S09` e `S10` NON HANNO MAI GIRATO in questa configurazione: la previsione non e'\n")
        W("    verificabile qui, e va detto invece di dedurre. ***\n")
    else:
        W("\n%6s %12s | %14s %14s %14s | %12s\n"
          % ("passo", "median(d0)", "S09 saldo", "S10 saldo", "S09+S10", "(S09+S10)/med"))
        W("-" * 92 + "\n")
        righe = []
        for k, med, cor in PER_PASSO:
            s9 = sum(v for s, v in cor.items() if s.startswith("S09"))
            s10 = sum(v for s, v in cor.items() if s.startswith("S10"))
            righe.append((k, med, s9, s10, s9 + s10))
            if k % max(1, len(PER_PASSO) // 12) == 0 or k == 1:
                W("%6d %12.6f | %14.6e %14.6e %14.6e | %12.6e\n"
                  % (k, med, s9, s10, s9 + s10, (s9 + s10) / max(med, 1e-300)))
        W("\n")
        tot9 = sum(r[2] for r in righe); tot10 = sum(r[3] for r in righe)
        tot = tot9 + tot10
        W("SALDO CUMULATO su %d passi:  S09 = %.6e   S10 = %.6e   S09+S10 = %.6e\n"
          % (len(righe), tot9, tot10, tot))
        W("VERSO: %s\n" % ("VERSO L'ALTO" if tot > 0 else
                           ("VERSO IL BASSO" if tot < 0 else "NULLO")))
        # cresce con median(d0)? Si guarda la PENDENZA di (S09+S10) contro median(d0).
        med = np.array([r[1] for r in righe]); val = np.array([r[4] for r in righe])
        ok = np.isfinite(med) & np.isfinite(val) & (med > 0)
        W("\nCRESCE CON `median(d0)`? Si misura la PENDENZA di `S09+S10` contro `median(d0)`,\n")
        W("e il RAPPORTO `(S09+S10)/median(d0)`: se il rapporto e' COSTANTE, la crescita e'\n")
        W("PROPORZIONALE a `median(d0)` -- che e' l'auto-amplificazione dell'ipotesi.\n")
        if int(np.sum(ok)) >= 3:
            p = np.polyfit(med[ok], val[ok], 1)
            r = np.corrcoef(med[ok], val[ok])[0, 1]
            rap = val[ok] / med[ok]
            W("  pendenza = %.6e   r = %.4f   su %d punti\n" % (p[0], r, int(np.sum(ok))))
            W("  rapporto `(S09+S10)/median(d0)`: primo %.6e, ultimo %.6e, mediano %.6e,\n"
              % (rap[0], rap[-1], float(np.median(rap))))
            W("    dispersione relativa = %.4f  (piccola = rapporto COSTANTE = proporzionale)\n"
              % (float(np.std(rap)) / max(abs(float(np.mean(rap))), 1e-300)))
            W("\nESITO DELLA PREVISIONE: saldo %s, pendenza contro `median(d0)` %s (r = %.4f).\n"
              % ("VERSO L'ALTO" if tot > 0 else "VERSO IL BASSO",
                 "POSITIVA" if p[0] > 0 else "NEGATIVA", r))
        else:
            W("  *** meno di 3 punti utili: la pendenza NON si misura, e non la invento. ***\n")
    W("\n")
    W("LIMITI: UN seme, UNA scena, %d passi. Questa e' la somma di cio' che ogni scrittore\n" % fatti)
    W("  SPINGE, NON di cio' che sopravvive: con `SCALA_MIN_PASSO` il freno agisce UNA VOLTA a\n")
    W("  fine passo, quindi la somma qui e' quella GREZZA, prima del freno. E' cio' che serve per\n")
    W("  sapere CHI spinge -- ma non dice quanto ne resta.\n")
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
