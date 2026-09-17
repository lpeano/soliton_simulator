# -*- coding: utf-8 -*-
"""SIGILLO — TRASPORTO PARALLELO NON NORMALIZZATO  N  (candidato per la forza del PEZZO 3).

    N_ij = (1 + n_i.n_j) I + i (n_i x n_j).sigma          [polinomiale nei Bloch]

Identita' chiave:  N_ij = 2 cos(chi/2) U_ij  ->  il PESO cos(chi/2) non e' scelto, e' cio' che
resta quando NON si normalizza. Zero manopole (CLAUDE.md par.3).

TRE PRESIDI DI LUCA, sigillati qui:
 (1) FATTORE 2 — nella forza si usa N/2, che a chi=0 vale I: riduzione allo scalare ESATTA.
 (2) DUE OGGETTI, DUE USI — N nella forza (polinomiale, floor-free); U = N/sqrt(det N)
     nell'olonomia (pure-read). La radice vive SOLO nel diagnostico, mai nella forza.
 (3) LIMITE DI CIO' CHE L'ALGEBRA PUO' DIRE — vedi la nota finale: qui si chiude il problema
     numerico/EM/antipodale, NON la correttezza DINAMICA del peso. Quella la dice un run.

Pure-read: non tocca soliton_simulator.py (blob invariato), non consuma RNG.
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
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from soliton_simulator import Rete  # noqa: E402

SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.array([[1, 0], [0, -1]], complex)
I2 = np.eye(2, dtype=complex)
esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-50s %s" % ("PASS" if ok else "FAIL", nome, misura))


def enne(ni, nj):
    """N_ij = (1 + n_i.n_j) I + i (n_i x n_j).sigma — nessuna divisione, nessun arccos, nessun floor."""
    ni = np.asarray(ni, float).reshape(-1, 3)
    nj = np.asarray(nj, float).reshape(-1, 3)
    d = np.sum(ni * nj, axis=1)
    c = np.cross(ni, nj)
    return ((1.0 + d)[:, None, None] * I2
            + 1j * (c[:, 0, None, None] * SX + c[:, 1, None, None] * SY + c[:, 2, None, None] * SZ))


def spinori(m, seed):
    g = np.random.default_rng(seed)
    p = g.normal(size=(m, 2)) + 1j * g.normal(size=(m, 2))
    return p / np.linalg.norm(p, axis=1)[:, None]


def versori(m, seed):
    g = np.random.default_rng(seed).normal(size=(m, 3))
    return g / np.linalg.norm(g, axis=1)[:, None]


M = 200000
ni, nj = versori(M, 101), versori(M, 202)
N = enne(ni, nj)
U, _ = Rete._link_su2(ni, nj)
chi = np.arccos(np.clip(np.sum(ni * nj, axis=1), -1.0, 1.0))

print("=" * 94)
print("BASE — il ponte con il PEZZO 1 gia' sigillato")
print("=" * 94)
d = np.max(np.abs(N - (2.0 * np.cos(chi / 2.0))[:, None, None] * U))
verdetto("B1 N = 2 cos(chi/2) U (ponte col PEZZO 1)", d < 1e-12, "max|N - 2cos(chi/2)U| = %.3e" % d)
detN = N[:, 0, 0] * N[:, 1, 1] - N[:, 0, 1] * N[:, 1, 0]
d = np.max(np.abs(detN - 4.0 * np.cos(chi / 2.0) ** 2))
verdetto("B2 det N = 4 cos^2(chi/2) (reale, >= 0)", d < 1e-12 and np.min(detN.real) >= -1e-12,
         "max|det N - 4cos^2| = %.3e ; max|Im| = %.1e" % (d, np.max(np.abs(detN.imag))))

print()
print("=" * 94)
print("PRESIDIO 1 — il fattore 2: nella forza si usa N/2, e a chi=0 riduce ESATTAMENTE allo scalare")
print("=" * 94)
K = 40000
nn = versori(K, 303)
Nal = enne(nn, nn.copy())
d = np.max(np.abs(Nal / 2.0 - I2))
# NB: con versori normalizzati NUMERICAMENTE il prodotto scalare vale 1 +- 1e-16, quindi "esatto"
# si verifica su Bloch ESATTI (assi cartesiani); sui numerici si pretende precisione macchina.
esatti = np.array([[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
d_ex = np.max(np.abs(enne(esatti, esatti.copy()) / 2.0 - I2))
verdetto("P1a allineati ESATTI: N/2 = I, zero esatto", d_ex == 0.0, "max|N/2 - I| = %.3e" % d_ex)
verdetto("P1a-num allineati numerici: N/2 = I", d < 1e-15, "max|N/2 - I| = %.3e" % d)
pa, pb = spinori(K, 55), spinori(K, 66)
contrib = np.imag(np.einsum('kx,kxy,ky->k', np.conj(pa), Nal / 2.0, pb))
scalare = np.imag(np.sum(np.conj(pa) * pb, axis=1))
d = np.max(np.abs(contrib - scalare))
verdetto("P1b allineati: Im<psi_i|N/2|psi_j> = scalare", d < 1e-15,
         "max|contrib - scalare| = %.3e  <-- con sin(chi) dava 9.99e-01" % d)

print()
print("=" * 94)
print("PRESIDIO 2 — due oggetti, due usi: N nella forza, U = N/sqrt(det N) nell'olonomia")
print("=" * 94)
buoni = chi < np.pi - 1e-6
Urec = N[buoni] / np.sqrt(detN[buoni].real)[:, None, None]
d = np.max(np.abs(Urec - U[buoni]))
verdetto("P2a U recuperabile da N: U = N/sqrt(det N)", d < 1e-12, "max|U_rec - U| = %.3e" % d)
d = np.max(np.abs(Urec @ np.conj(np.transpose(Urec, (0, 2, 1))) - I2))
verdetto("P2b U cosi' ricostruita e' unitaria", d < 1e-12, "max|UU^dag - I| = %.3e" % d)
T = 20000
na, nb, nc = versori(T, 1), versori(T, 2), versori(T, 3)
Wn = np.trace(enne(na, nb) @ enne(nb, nc) @ enne(nc, na), axis1=1, axis2=2)
Ua, _ = Rete._link_su2(na, nb)
Ub, _ = Rete._link_su2(nb, nc)
Uc, _ = Rete._link_su2(nc, na)
Wu = np.trace(Ua @ Ub @ Uc, axis1=1, axis2=2)
ok = np.abs(Wu) > 1e-6
d = np.max(np.abs(np.angle(Wn[ok] / Wu[ok])))
verdetto("P2c fase dell olonomia IDENTICA con N o con U", d < 1e-9,
         "max|arg(W_N/W_U)| = %.3e  (il peso e' scalare positivo: fattorizza)" % d)

print()
print("=" * 94)
print("ANTIPODALE — gestito da N stesso, senza floor e senza caso speciale")
print("=" * 94)
nap = versori(4000, 7)
Nap = enne(nap, -nap)
d_ex = np.max(np.abs(enne(esatti, -esatti)))
verdetto("A1 antipodali ESATTI: N = 0, zero esatto", d_ex == 0.0, "max|N| = %.3e" % d_ex)
verdetto("A1-num antipodali numerici: N = 0", np.max(np.abs(Nap)) < 1e-15,
         "max|N| = %.3e  (dot=-1 e cross=0: niente da normalizzare)" % np.max(np.abs(Nap)))
ang = np.linspace(0, 2 * np.pi, 361)[:-1]
p1, p2 = spinori(1, 77), spinori(1, 88)
eps_l = [1e-6, 1e-4, 1e-2]
disp = []
for e in eps_l:
    a_ = np.tile(np.array([[0.0, 0.0, 1.0]]), (len(ang), 1))
    b_ = np.stack([np.sin(np.pi - e) * np.cos(ang), np.sin(np.pi - e) * np.sin(ang),
                   np.full_like(ang, np.cos(np.pi - e))], axis=1)
    v = np.imag(np.einsum('kx,kxy,ky->k', np.conj(np.tile(p1, (len(ang), 1))),
                          enne(a_, b_) / 2.0, np.tile(p2, (len(ang), 1))))
    disp.append(v.max() - v.min())
verdetto("A2 indeterminatezza antipodale svanisce", disp[0] < 1e-6,
         "dispersione: " + "  ".join("eps=%.0e -> %.2e" % (e, dd) for e, dd in zip(eps_l, disp)))

print()
print("=" * 94)
print("FISICA DEL PESO — perche' cos(chi/2) e non un altro (argomenti di Luca, qui MISURATI)")
print("=" * 94)
# F1. cos(chi/2) E' l'OVERLAP QUANTISTICO dei due spin: |<n_i|n_j>| con |n> = spinore di Bloch.
# Non e' un artefatto del non-normalizzare: e' quanto i due spin si sovrappongono.
ov_spin = np.abs(np.sum(np.conj(Rete._bloch_a_spinore(ni)) * Rete._bloch_a_spinore(nj), axis=1))
d = np.max(np.abs(ov_spin - np.cos(chi / 2.0)))
verdetto("F1 cos(chi/2) = |<n_i|n_j>| (overlap di spin)", d < 1e-12,
         "max| |<n_i|n_j>| - cos(chi/2) | = %.3e" % d)
# F2. CONSISTENZA AMPIEZZA/PROBABILITA'. La forza e' Im<psi_i|N|psi_j>: una AMPIEZZA. Va pesata
# con l'overlap-AMPIEZZA cos(chi/2), non con l'overlap-PROBABILITA' cos^2(chi/2) (regola di Born),
# che conterebbe due volte. Qui si verifica che cos^2 E' davvero la probabilita' di Born.
born = np.abs(np.sum(np.conj(Rete._bloch_a_spinore(ni)) * Rete._bloch_a_spinore(nj), axis=1)) ** 2
d = np.max(np.abs(born - np.cos(chi / 2.0) ** 2))
verdetto("F2 cos^2(chi/2) = |<n_i|n_j>|^2 = Born (probabilita')", d < 1e-12,
         "max|Born - cos^2(chi/2)| = %.3e -> cos^2 pesa una AMPIEZZA con una PROBABILITA'" % d)
d = np.max(np.abs((1.0 + np.sum(ni * nj, axis=1)) / 2.0 - born))
verdetto("F2b (1+n_i.n_j)/2 = Born (la forma polinomiale)", d < 1e-12,
         "max|(1+n.n)/2 - Born| = %.3e" % d)

print()
print("=" * 94)
print("ROBUSTEZZA — N e' polinomiale: nessuna divisione, nessun floor, nessun caso speciale")
print("=" * 94)
verdetto("R1 nessun NaN/inf su 200000 archi casuali", np.all(np.isfinite(N)), "tutti finiti")
est = np.tile(np.array([0.0, 0.0, 1.0]), (3, 1))
est2 = np.array([[0.0, 0.0, 1.0], [0.0, 0.0, -1.0], [1.0, 0.0, 0.0]])
verdetto("R2 nessun NaN/inf sui casi limite (0, pi, pi/2)", np.all(np.isfinite(enne(est, est2))),
         "tutti finiti")
Nji = enne(nj, ni)
d = np.max(np.abs(Nji - np.conj(np.transpose(N, (0, 2, 1)))))
verdetto("R3 N_ji = N_ij^dag ESATTO (azione-reazione)", d == 0.0,
         "max|N_ji - N_ij^dag| = %.3e  (esatto perche' polinomiale)" % d)
c_ij = np.imag(np.einsum('kx,kxy,ky->k', np.conj(spinori(M, 1)), N / 2.0, spinori(M, 2)))
verdetto("R4 |contributo| <= 1 (nessuna amplificazione)", np.max(np.abs(c_ij)) <= 1.0,
         "max|Im<psi_i|N/2|psi_j>| = %.6f" % np.max(np.abs(c_ij)))
med, err = np.mean(c_ij), np.std(c_ij) / np.sqrt(M)
verdetto("R5 nessun verso preferito", abs(med) < 5 * err,
         "media = %+.3e (3 sigma = %.3e)" % (med, 3 * err))

print("=" * 94)
tot, ok_ = len(esiti), sum(esiti)
print("SIGILLO N: %d/%d PASS -> %s" % (ok_, tot, "PASS" if ok_ == tot else "FAIL"))
print("""
DELIBERA (Claude Code, su raccomandazione motivata di Luca): il peso e' cos(chi/2).
 * NON e' un compromesso ne' un regolarizzatore: e' l'OVERLAP DI SPIN |<n_i|n_j>| (F1), cioe'
   l'accoppiamento fisico tra i due solitoni. Un accoppiamento e' GLOBALE per natura: l'interferenza
   dipende dall'overlap a OGNI angolo, non solo vicino a pi. Quindi "globale ma non scelto" non e'
   un compromesso, e' corretto. La singolarita' antipodale si cura come CONSEGUENZA (overlap -> 0),
   non come scopo — ed e' il motivo per cui l'ammorbidimento "stretto" era la domanda sbagliata.
 * Contro cos^2(chi/2): quella e' la PROBABILITA' di Born (F2). La forza e' Im<psi_i|N|psi_j>, una
   AMPIEZZA: si pesa con un'ampiezza, non con una probabilita'. cos^2 conterebbe due volte.
 * Contro sin(chi): spegne chi=0 e perde il canale di fase (EM).
 * Contro l'ammorbidimento stretto: richiede una larghezza = un numero nuovo = manopola (par.3).
""")
print("""
PRESIDIO 3 — QUELLO CHE QUESTO SIGILLO **NON** DIMOSTRA (onesta' permanente)
---------------------------------------------------------------------------
Tutto qui sopra e' ALGEBRA. Chiude tre cose e solo quelle:
  * il problema NUMERICO   (niente arccos, niente asse normalizzato, niente floor, niente caso
    speciale: N non divide mai per nulla, e a chi=pi vale 0 da solo);
  * il problema EM         (a chi=0, N/2 = I -> riduzione allo scalare ESATTA: 0.000e+00);
  * il problema ANTIPODALE (l'indeterminatezza dell'asse svanisce senza inventare direzioni).
NON dimostra che il peso cos(chi/2) sia DINAMICAMENTE corretto. Il peso sotto-pesa gli archi a chi
grande (0.707 a 90 gradi, 0.500 a 120). C'e' un argomento buono che sia giusto - N|psi_j> e' la
proiezione naturale del trasportato, e solitoni con Bloch disallineati interferiscono davvero meno -
ma e' un ARGOMENTO, non una MISURA. Che questo peso produca la fisica giusta (olonomia W(r)
sensata, stabilita', comportamento dell EM) lo dice un RUN, non l algebra.
ELEGANTE non significa DINAMICAMENTE CORRETTO. Non far contrabbandare all eleganza la conclusione.
""")
sys.exit(0 if ok_ == tot else 1)
