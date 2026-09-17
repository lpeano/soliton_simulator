# -*- coding: utf-8 -*-
"""SCOMPOSIZIONE della crescita di `L_tot` — SUI DATI COMMITTATI, nessun run nuovo.

VINCOLO DICHIARATO (doc/PREDIZIONE_scomposizione_L.md par.0): la scomposizione sui soli intervalli
SENZA nascite NON e' calcolabile dai CSV, perche' il campionamento e' ogni 50 passi e in 50 passi
nascono sempre nodi (0 intervalli birth-free su 10, in tutti e quattro i run). Qui si scompone la
crescita dell'INTENSITA' PER NODO, che risponde alla stessa domanda a risoluzione di campione:

    L_tot ~ n * <I*|omega|>   =>   d log(L/n) = d log(I) + d log(|omega|)  (+ misto)
                                                 \_ A _/     \_ B _/

E il controllo par.3.2 — `L_tot/n` e la mediana di `I*|omega|` — e' ESATTO: separa AGGREGAZIONE
(cresce n) da INTENSIFICAZIONE (cresce l'intensita' per nodo), che il totale non distingue.
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
import csv
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = [("OFF", 1), ("OFF", 2), ("ON", 1), ("ON", 2)]
T95 = {1: 12.706, 2: 4.303, 3: 3.182}


def leggi(br, s):
    with open(os.path.join(HERE, "_vuoto_base_%s_s%d.vuoto.csv" % (br, s))) as f:
        return list(csv.DictReader(f))


def col(rows, k):
    return np.array([float(r[k]) if r[k] not in ("", "nan") else np.nan for r in rows])


print("=" * 112)
print("SCOMPOSIZIONE DELLA CRESCITA DI L_tot — dati committati, blob c57800c1, nessun run nuovo")
print("=" * 112)
print()
print("3.2 — AGGREGAZIONE contro INTENSIFICAZIONE (controllo ESATTO, non serve birth-free)")
print("-" * 112)
print("  %-9s %8s %12s %12s %12s %12s" % ("run", "n", "L_tot", "L_tot/n", "I mediana", "|omega| med"))
tabella = {}
for br, s in RUN:
    r = leggi(br, s)
    n = col(r, "n"); L = col(r, "L_tot")
    I = col(r, "fdt_inerzia_mediana"); om = col(r, "fdt_om_mediana")
    pa = col(r, "passo")
    ok = np.isfinite(L) & np.isfinite(I) & np.isfinite(om) & (n > 100)
    tabella[(br, s)] = (pa[ok], n[ok], L[ok], I[ok], om[ok])
    print("  %-9s %8d %12.4g %12.4g %12.4g %12.4g"
          % ("%s_s%d" % (br, s), int(n[-1]), L[-1], L[-1] / n[-1], I[-1], om[-1]))
print()
print("  crescita dal PRIMO campione utile all'ULTIMO (fattore moltiplicativo):")
print("  %-9s %10s %10s %10s %10s %10s" % ("run", "n", "L_tot", "L_tot/n", "I med", "|om| med"))
for br, s in RUN:
    pa, n, L, I, om = tabella[(br, s)]
    print("  %-9s %10.3f %10.3f %10.3f %10.3f %10.3f"
          % ("%s_s%d" % (br, s), n[-1] / n[0], L[-1] / L[0], (L[-1] / n[-1]) / (L[0] / n[0]),
             I[-1] / I[0], om[-1] / om[0]))

print()
print("=" * 112)
print("1 — LA SCOMPOSIZIONE:  d log(L/n) = d log(I) + d log(|omega|)  (+ misto)")
print("=" * 112)
print("  Per ogni coppia di campioni consecutivi. A = contributo dell'INERZIA, B = di OMEGA.")
print("-" * 112)
ris = {}
for br, s in RUN:
    pa, n, L, I, om = tabella[(br, s)]
    ln = L / n
    dA = np.diff(np.log(I))
    dB = np.diff(np.log(om))
    dT = np.diff(np.log(ln))
    misto = dT - dA - dB            # scarto fra la somma dei due e il totale osservato
    print("  %s_s%d" % (br, s))
    print("     %6s %10s %10s %10s %10s %8s" % ("passo", "d log(L/n)", "A=dlog I", "B=dlog om", "misto", "A/(A+|B|)"))
    for k in range(len(dT)):
        den = abs(dA[k]) + abs(dB[k])
        print("     %6d %10.4f %10.4f %10.4f %10.4f %8.3f"
              % (int(pa[k + 1]), dT[k], dA[k], dB[k], misto[k], abs(dA[k]) / den if den else np.nan))
    sA, sB = float(np.sum(dA)), float(np.sum(dB))
    ris[(br, s)] = (sA, sB, float(np.sum(dT)), float(np.sum(misto)))
    print("     TOTALE   d log(L/n) = %+.4f   A = %+.4f   B = %+.4f   misto = %+.4f"
          % (np.sum(dT), sA, sB, np.sum(misto)))
    print("     -> A vale il %.1f %% di |A|+|B|;  A/B = %s"
          % (100 * abs(sA) / (abs(sA) + abs(sB)), "%.2f" % (sA / sB) if sB else "inf"))
    print()

print("=" * 112)
print("ATTENZIONE: LA SCOMPOSIZIONE QUI SOPRA NON CHIUDE, ED E' UN DIFETTO DEL METODO, NON DEI DATI")
print("=" * 112)
print("  `L_tot/n` e' una MEDIA di `I*|omega|`; `I` e `omega` qui sopra sono MEDIANE.")
print("  LE MEDIANE NON SI MOLTIPLICANO PER DARE LA MEDIA: il termine misto assorbe tutto lo")
print("  scarto, ed e' infatti dell'ordine del totale. La scomposizione mediana NON e' leggibile,")
print("  e si conserva solo come tentativo dichiarato.")
print("  SERVONO STATISTICHE COMMENSURABILI, cioe' MEDIE. Nei CSV ce ne sono due:")
print("     Lam           = media di |psi|^2  -> proxy di media(inerzia), il fattore cs^2 e' ~1")
print("     fdt_om2_media = media di omega^2  -> RMS(omega) = sqrt(...)")
print()
print("=" * 112)
print("1-bis — LA SCOMPOSIZIONE VERA, con statistiche MEDIE")
print("=" * 112)
ris2 = {}
for br, s in RUN:
    r = leggi(br, s)
    r = [x for x in r if float(x["n"]) > 100 and x["L_tot"] not in ("", "nan")]
    pa = np.array([float(x["passo"]) for x in r]); n = np.array([float(x["n"]) for x in r])
    L = np.array([float(x["L_tot"]) for x in r]); lam = np.array([float(x["Lam"]) for x in r])
    rms = np.sqrt(np.array([float(x["fdt_om2_media"]) for x in r]))
    Imed = np.array([float(x["fdt_inerzia_mediana"]) for x in r])
    ln = L / n
    print("  === %s_s%d ===" % (br, s))
    print("  %6s %11s %11s %11s %13s" % ("passo", "L/n", "Lam ~ <I>", "RMS(omega)", "I MEDIANA"))
    for k in range(len(pa)):
        marca = "  <- al FLOOR" if Imed[k] <= 1.0000001e-6 else ""
        print("  %6d %11.4g %11.4g %11.4g %13.4g%s" % (pa[k], ln[k], lam[k], rms[k], Imed[k], marca))
    A = float(np.log(lam[-1] / lam[0])); B = float(np.log(rms[-1] / rms[0]))
    T = float(np.log(ln[-1] / ln[0]))
    ris2[(br, s)] = (A, B, T)
    print("  d log(L/n) = %+.4f   A = d log(Lam) = %+.4f   B = d log(RMS om) = %+.4f   misto = %+.4f"
          % (T, A, B, T - A - B))
    print("  -> PESO DI A: %.1f %% di |A|+|B|   |   Lam x%.0f, RMS(omega) x%.2f"
          % (100 * abs(A) / (abs(A) + abs(B)), np.exp(A), np.exp(B)))
    print()
print("  IL MISTO E' GRANDE E NEGATIVO, e ha DUE cause note, entrambe nello stesso verso:")
print("   (1) `Lam` e' media di rho, ma l'inerzia ha un FLOOR 1e-6: finche' molti nodi sono al")
print("       floor, media(inerzia) > Lam, e converge verso Lam DALL'ALTO -> `Lam` SOVRASTIMA la")
print("       crescita di media(inerzia);")
print("   (2) `I` e `omega` sono ANTICORRELATI (pendenza -1.056, C1), quindi media(I*omega)")
print("       cresce MENO di media(I)*RMS(omega).")
print("  ATTENZIONE: QUINDI `A` E' SE MAI SOVRASTIMATO. MA `B` E' MISURATO DIRETTAMENTE ED E' ~0: la")
print("  conclusione «non e' omega che cresce» NON dipende dalla sovrastima di A.")
print()
print("=" * 112)
print("IL NUMERO CHE DECIDE — dispersione FRA SEMI (P3), mai la SE interna")
print("=" * 112)
for br in ("OFF", "ON"):
    fa = [100 * abs(ris2[(br, s)][0]) / (abs(ris2[(br, s)][0]) + abs(ris2[(br, s)][1])) for s in (1, 2)]
    a = [ris2[(br, s)][0] for s in (1, 2)]
    b = [ris2[(br, s)][1] for s in (1, 2)]
    m, sd = float(np.mean(fa)), float(np.std(fa, ddof=1))
    print("  %-4s  A = %+.4f / %+.4f   B = %+.4f / %+.4f" % (br, a[0], a[1], b[0], b[1]))
    print("  %-4s  peso di A: %.1f %% / %.1f %%   media %.1f %%  sd %.1f %%  IC95 [%.1f, %.1f] (t(1)=12.706)"
          % (br, fa[0], fa[1], m, sd, m - 12.706 * sd / math.sqrt(2), m + 12.706 * sd / math.sqrt(2)))
print()
print("=" * 112)
print("CONTROLLO 3.1 — il confronto e' fra gli STESSI nodi? `n` CRESCE in ogni intervallo")
print("=" * 112)
for br, s in RUN:
    pa, n, L, I, om = tabella[(br, s)]
    cal = int(np.sum(np.diff(n) < 0))
    print("  %-9s n da %d a %d;  intervalli con n in CALO (rimozioni/fusioni): %d"
          % ("%s_s%d" % (br, s), int(n[0]), int(n[-1]), cal))
print("  -> se e' 0, la popolazione non perde nodi: `Delta L` mescola crescita e AGGIUNTA, mai")
print("     crescita e RIMOZIONE. E' il caso piu' semplice da leggere, ma NON isola i birth-free.")
print("=" * 112)
