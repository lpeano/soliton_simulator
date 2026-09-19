# -*- coding: utf-8 -*-
"""LE SOMME -- le cure REDISTRIBUISCONO o RIDUCONO?

Letture e soglia FISSATE PRIMA: doc/TASK_HISTORY/2026-09-20_la-somma.md (abc67a8).
NESSUN RUN qui: si leggono gli snapshot dei due A/B, RICOSTRUITI e verificati (ramo A contro
archivio: 113 campi, 0 diversi, in ENTRAMBI gli esperimenti).

IL FATTO CHE MOTIVA LA MISURA: due cure in punti DIVERSI della stessa catena danno lo STESSO
profilo -- massimo giu' di circa un terzo, nodi eccitati raddoppiati, nodo target triplicato.
L'IPOTESI: le cure non RIDUCONO omega, la REDISTRIBUISCONO.

LE QUATTRO LETTURE (soglia: coincidono entro il 5 %, E deve valere su ENTRAMBE le cure)
  A  le somme COINCIDONO          -> REDISTRIBUZIONE: si riporta QUALE grandezza si conserva
  B  le somme SCENDONO in B       -> le cure riducono davvero
  C  le somme SALGONO in B        -> le cure IMMETTONO: il caso peggiore
  D  coincidono per UNA sola      -> QUELLA e' la conservata, ed e' il reperto

I PRESIDI
- le somme sono ESTENSIVE: si VERIFICA che `n` sia identico nei tre rami, e se non lo e' si
  normalizza DICHIARANDOLO (A3c);
- `inerzia` al pavimento: si riporta QUANTI nodi per ramo. Una somma pesata su un pavimento e'
  pesata su UN NUMERO SCELTO, non su uno stato;
- code pesanti: mai la media senza la mediana accanto;
- NESSUNA IDENTIFICAZIONE ("si conserva il momento angolare"): si riporta SE una somma coincide,
  E QUALE.
ASCII PURO.
"""
import gzip
import os
import pickle
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
PASSO = 240
SOGLIA = 0.05          # "coincidono entro il 5 %", fissata PRIMA
RAMI = [("A (nessuna cura)", "csv/_seal_fork/_ab_coppia_reciproca/A"),
        ("B  coppia-recipr", "csv/_seal_fork/_ab_coppia_reciproca/B"),
        ("B' grav-ampiezza", "csv/_seal_fork/_ab_grav_ampiezza/B")]


def carica(d):
    p = os.path.join(RADICE, d, "scena_%06d.pkl.gz" % PASSO)
    with gzip.open(p, "rb") as f:
        return pickle.load(f)["attrs"]


def grandezze(at):
    n = len(at["eta"])
    om = np.asarray(at["omega_s"], float)[:n]
    mod = np.linalg.norm(om, axis=1)
    # l'INERZIA si RICOSTRUISCE come il codice la calcola (:2417): max(_contrasto*_T2, 1e-6).
    # _T2 non e' negli snapshot: si usa il PAVIMENTO come limite inferiore noto, e si DICHIARA
    # che l'energia pesata e' calcolata con l'inerzia RICOSTRUITA SOLO dove e' ricostruibile.
    rho = np.asarray(at["rho_spin"], float)[:n]
    return dict(n=n, mod=mod, om=om, rho=rho,
                s_abs=float(mod.sum()),
                s_vec=om.sum(axis=0),
                s_quad=float((mod ** 2).sum()),
                med=float(np.median(mod)), mx=float(mod.max()),
                sopra=set(np.flatnonzero(mod > 1e2).tolist()),
                pav=int(np.sum(rho <= 1e-6)))


def rel(x, y):
    return abs(y - x) / abs(x) if x else float("inf")


def main():
    D = {}
    for nome, d in RAMI:
        D[nome] = grandezze(carica(d))
    A = D["A (nessuna cura)"]

    print("passo %d   soglia 'coincidono' = %.0f %%   (fissata PRIMA)" % (PASSO, 100 * SOGLIA))
    print("")
    print("=== PRESIDIO: n IDENTICO? (le somme sono ESTENSIVE) ===")
    for nome in D:
        print("   %-18s n = %d" % (nome, D[nome]["n"]))
    tutti_uguali = len(set(D[k]["n"] for k in D)) == 1
    print("   -> %s" % ("SI: le somme sono confrontabili direttamente"
                        if tutti_uguali else
                        "*** NO: le somme NON sono confrontabili senza normalizzare ***"))

    print("")
    print("=== PRESIDIO: quanti nodi hanno rho <= 1e-6 (il PAVIMENTO dell'inerzia) ===")
    for nome in D:
        print("   %-18s %d nodi su %d  (%.3f %%)"
              % (nome, D[nome]["pav"], D[nome]["n"], 100.0 * D[nome]["pav"] / D[nome]["n"]))
    print("   una somma pesata sull'inerzia e' pesata su 1e-6 per QUESTI nodi: un numero SCELTO")

    print("")
    print("=" * 112)
    print("LE SOMME")
    print("=" * 112)
    print("%-18s | %-14s %-14s | %-13s %-13s" %
          ("ramo", "sum|omega|", "sum|omega|^2", "mediana", "max"))
    for nome in D:
        d = D[nome]
        print("%-18s | %-14.6g %-14.6g | %-13.6g %-13.6g"
              % (nome, d["s_abs"], d["s_quad"], d["med"], d["mx"]))
    print("")
    print("%-18s | %s" % ("ramo", "sum(omega_s) VETTORIALE  -- il momento NETTO, altra grandezza"))
    for nome in D:
        v = D[nome]["s_vec"]
        print("%-18s | [%12.6g %12.6g %12.6g]   |v| = %.6g"
              % (nome, v[0], v[1], v[2], float(np.linalg.norm(v))))

    print("")
    print("=== GLI SCARTI RELATIVI CONTRO IL RAMO A ===")
    print("%-18s | %-14s %-14s %-14s" % ("ramo", "sum|omega|", "sum|omega|^2", "|sum(omega)|"))
    conserva = {}
    for nome in D:
        if nome.startswith("A "):
            continue
        d = D[nome]
        r1 = rel(A["s_abs"], d["s_abs"])
        r2 = rel(A["s_quad"], d["s_quad"])
        r3 = rel(float(np.linalg.norm(A["s_vec"])), float(np.linalg.norm(d["s_vec"])))
        conserva[nome] = dict(s_abs=r1, s_quad=r2, s_vec=r3)
        print("%-18s | %-14s %-14s %-14s"
              % (nome, "%+.2f %%" % (100 * r1), "%+.2f %%" % (100 * r2), "%+.2f %%" % (100 * r3)))

    print("")
    print("=== LA CONCENTRAZIONE: frazione di sum|omega| detenuta dai primi k nodi ===")
    print("%-18s | %-10s %-10s %-10s %-10s" % ("ramo", "top 10", "top 100", "top 1000", "tutti"))
    for nome in D:
        m = np.sort(D[nome]["mod"])[::-1]
        tot = m.sum()
        print("%-18s | %-10.4f %-10.4f %-10.4f %-10d"
              % (nome, m[:10].sum() / tot, m[:100].sum() / tot, m[:1000].sum() / tot, len(m)))

    print("")
    print("=== L'ISTOGRAMMA di log10(|omega_s|), STESSI BIN ===")
    bins = np.arange(-20, 7, 2.0)
    print("%-18s | %s" % ("ramo", " ".join("%6.0f" % b for b in bins[:-1])))
    for nome in D:
        m = D[nome]["mod"]
        lg = np.log10(np.maximum(m, 1e-300))
        h, _ = np.histogram(lg, bins=bins)
        print("%-18s | %s" % (nome, " ".join("%6d" % x for x in h)))

    print("")
    print("=== I NODI SOPRA 1e2: sono gli STESSI fra i rami? (Jaccard) ===")
    nomi = list(D)
    for a in range(len(nomi)):
        for b in range(a + 1, len(nomi)):
            X, Y = D[nomi[a]]["sopra"], D[nomi[b]]["sopra"]
            u = len(X | Y)
            print("   %-18s vs %-18s |X|=%-4d |Y|=%-4d  J = %s"
                  % (nomi[a], nomi[b], len(X), len(Y), "%.4f" % (len(X & Y) / u) if u else "-"))

    print("")
    print("=" * 112)
    print("IL VERDETTO, secondo le quattro letture fissate PRIMA")
    print("=" * 112)
    for g, et in (("s_abs", "sum|omega|"), ("s_quad", "sum|omega|^2"), ("s_vec", "|sum(omega)|")):
        v = [conserva[k][g] for k in conserva]
        ok = all(x <= SOGLIA for x in v)
        print("   %-14s scarti: %s   -> %s"
              % (et, "  ".join("%+.2f %%" % (100 * x) for x in v),
                 "COINCIDE su ENTRAMBE" if ok else "non coincide"))
    coincidenti = [et for g, et in (("s_abs", "sum|omega|"), ("s_quad", "sum|omega|^2"),
                                    ("s_vec", "|sum(omega)|"))
                   if all(conserva[k][g] <= SOGLIA for k in conserva)]
    print("")
    if len(coincidenti) == 3:
        print("-> LETTURA A: TUTTE le somme coincidono entro il %.0f %%. E' REDISTRIBUZIONE." % (100 * SOGLIA))
    elif len(coincidenti) >= 1:
        print("-> LETTURA D: coincide SOLO %s." % ", ".join(coincidenti))
        print("   QUELLA e' la quantita' che non cambia, ed e' il reperto.")
    else:
        scesi = all(D[k]["s_abs"] < A["s_abs"] for k in conserva)
        saliti = all(D[k]["s_abs"] > A["s_abs"] for k in conserva)
        if scesi:
            print("-> LETTURA B: le somme SCENDONO in entrambe le cure. Riducono davvero.")
        elif saliti:
            print("-> LETTURA C: le somme SALGONO in entrambe le cure. LE CURE IMMETTONO.")
        else:
            print("-> NESSUNA DELLE QUATTRO: le due cure non concordano nemmeno fra loro.")
            print("   Si riporta COSI', senza inventarne una quinta.")
    print("")
    print("NESSUNA IDENTIFICAZIONE: si riporta SE una somma coincide e QUALE, non cosa significhi.")
    print("UN SEME, UNA SCENA, mezzo run, override del blob. --tau-luce sigillo 6/7.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
