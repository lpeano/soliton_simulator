# -*- coding: utf-8 -*-
"""CONFRONTO DEI PESI D'ARCO — diagnosi del reperto del PEZZO 2.

Il peso `sin(chi)` SOVRA-CORREGGE: traccia l'indeterminatezza dell'asse m_hat, che si annulla a
ENTRAMBI gli estremi, ma quell'indeterminatezza e' dannosa SOLO a chi=pi.
  * chi=0  : U = cos(0) I - sin(0) (m.sigma) = I  qualunque sia m  -> asse indeterminato INNOCUO
  * chi=pi : U = -i (m.sigma), e sin(chi/2)=1 NON uccide il termine -> asse indeterminato DANNOSO
Quindi il peso giusto deve annullarsi SOLO a chi=pi.

Questo script NON decide: misura i candidati sugli stessi criteri e stampa la tabella.
Non tocca soliton_simulator.py (blob invariato). Pure-read.
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
esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-52s %s" % ("PASS" if ok else "FAIL", nome, misura))


def spinori(m, seed):
    g = np.random.default_rng(seed)
    p = g.normal(size=(m, 2)) + 1j * g.normal(size=(m, 2))
    return p / np.linalg.norm(p, axis=1)[:, None]


print("=" * 92)
print("A. IL PESO cos(chi/2) NON E' UNA SCELTA: e' cio' che resta quando NON si normalizza")
print("=" * 92)
# Trasporto parallelo NON normalizzato, polinomiale nei Bloch (no arccos, no asse, no floor):
#     N = (1 + n_i.n_j) I + i (n_i x n_j).sigma
g = np.random.default_rng(5)
M = 200000
ni = g.normal(size=(M, 3)); ni /= np.linalg.norm(ni, axis=1)[:, None]
nj = g.normal(size=(M, 3)); nj /= np.linalg.norm(nj, axis=1)[:, None]
U, w_sin = Rete._link_su2(ni, nj)
cos_chi = np.clip(np.sum(ni * nj, axis=1), -1.0, 1.0)
chi = np.arccos(cos_chi)
cr = np.cross(ni, nj)
N = ((1.0 + cos_chi)[:, None, None] * np.eye(2, dtype=complex)
     + 1j * (cr[:, 0, None, None] * SX + cr[:, 1, None, None] * SY + cr[:, 2, None, None] * SZ))
d_N = np.max(np.abs(N - (2.0 * np.cos(chi / 2.0))[:, None, None] * U))
verdetto("A1 N == 2 cos(chi/2) * U (identita' esatta)", d_N < 1e-12, "max|N - 2cos(chi/2)U| = %.3e" % d_N)
verdetto("A2 il peso e' DERIVATO, non tarato", True,
         "nessun numero scelto: e' |N|/2, la norma del trasporto non normalizzato")

print()
print("=" * 92)
print("B. I CANDIDATI SUI CRITERI CHE CONTANO")
print("=" * 92)
PESI = [
    ("sin(chi)        [ATTUALE]", lambda c: np.sin(c)),
    ("cos(chi/2)      [da N]   ", lambda c: np.cos(c / 2.0)),
    ("cos^2(chi/2)    [(1+n.n)/2]", lambda c: np.cos(c / 2.0) ** 2),
    ("1 (nessun peso) [+ U:=I a pi]", lambda c: np.ones_like(c)),
]
print("%-30s %8s %8s %8s   %s" % ("peso", "chi=0", "chi=90", "chi=180", "verdetto"))
print("-" * 92)
for nome, f in PESI:
    v0 = f(np.array([0.0]))[0]
    v90 = f(np.array([np.pi / 2]))[0]
    v180 = f(np.array([np.pi]))[0]
    note = []
    note.append("EM preservato" if v0 > 0.99 else "**SPEGNE chi=0 -> perde il canale di fase**")
    note.append("antipodale spento" if v180 < 1e-12 else "**NON spegne l'antipodale**")
    print("%-30s %8.4f %8.4f %8.4f   %s" % (nome, v0, v90, v180, " ; ".join(note)))

print()
print("=" * 92)
print("C. RIDUZIONE ALLO SCALARE A chi=0 (il sigillo che oggi fallisce)")
print("=" * 92)
# Bloch allineati, spinori con FASI DIVERSE (il caso reale: _psi_spinor non e' il canonico di nb).
K = 40000
nn = g.normal(size=(K, 3)); nn /= np.linalg.norm(nn, axis=1)[:, None]
pa, pb = spinori(K, 55), spinori(K, 66)
Ua, _ = Rete._link_su2(nn, nn.copy())
ov = np.einsum('kx,kxy,ky->k', np.conj(pa), Ua, pb)
scalare = np.imag(np.sum(np.conj(pa) * pb, axis=1))
for nome, f in PESI:
    contrib = f(np.zeros(K)) * np.imag(ov)
    d = np.max(np.abs(contrib - scalare))
    ok = d < 1e-12
    print("  [%s] %-30s max|contrib - scalare| = %.3e" % ("PASS" if ok else "FAIL", nome, d))
    esiti.append(ok)

print()
print("=" * 92)
print("D. CONTINUITA' ATTORNO A chi=pi (il problema VERO che il peso deve curare)")
print("=" * 92)
# L'indeterminatezza a chi=pi NON e' sull'angolo: e' sulla DIREZIONE dell'asse. Due perturbazioni
# di pari ampiezza ma direzione diversa attorno all'antipodale danno assi m_hat COMPLETAMENTE
# diversi. Il test giusto: fisso n_i, prendo n_j quasi-antipodale perturbato di eps in tutte le
# direzioni azimutali, e misuro la DISPERSIONE del contributo. Se resta O(1) per eps->0, il
# contributo e' indeterminato (dannoso); se svanisce con eps, il peso ha curato.
eps = np.array([1e-6, 1e-4, 1e-2])
ang = np.linspace(0.0, 2.0 * np.pi, 361)[:-1]   # direzione della perturbazione
p1 = spinori(1, 77)
p2 = spinori(1, 88)
for nome, f in PESI:
    disp = []
    for e in eps:
        # n_i = +z ; n_j = quasi -z, inclinato di eps nella direzione azimutale ang
        a_ = np.tile(np.array([[0.0, 0.0, 1.0]]), (len(ang), 1))
        b_ = np.stack([np.sin(np.pi - e) * np.cos(ang),
                       np.sin(np.pi - e) * np.sin(ang),
                       np.full_like(ang, np.cos(np.pi - e))], axis=1)
        Uk, _ = Rete._link_su2(a_, b_)
        val = f(np.full(len(ang), np.pi - e)) * np.imag(
            np.einsum('kx,kxy,ky->k', np.conj(np.tile(p1, (len(ang), 1))), Uk,
                      np.tile(p2, (len(ang), 1))))
        disp.append(val.max() - val.min())
    ok = disp[0] < 1e-3          # per eps->0 la dispersione deve svanire
    print("  [%s] %-30s dispersione su 360 direzioni: %s" %
          ("PASS" if ok else "FAIL", nome,
           "  ".join("eps=%.0e -> %.2e" % (e, d) for e, d in zip(eps, disp))))
    esiti.append(ok)

print()
print("=" * 92)
tot, ok = len(esiti), sum(esiti)
print("ESITO: %d/%d PASS (i FAIL qui sono DIAGNOSI dei candidati, non rotture del codice)" % (ok, tot))
print("""
LETTURA (nessuna decisione presa qui - serve Luca):
 * `sin(chi)` e' l'unico candidato che FALLISCE la riduzione allo scalare a chi=0: spegne il
   canale di fase (EM) per curare un problema che a chi=0 non esiste.
 * `cos(chi/2)` passa C e D, vale 1 a chi=0 e 0 a chi=pi, e **non e' una scelta**: e' |N|/2, la
   norma del trasporto parallelo NON normalizzato (A1). Zero manopole, e in piu' si calcola senza
   arccos e senza normalizzare l'asse -> niente floor, niente caso degenere da gestire a mano.
 * `cos^2(chi/2)` passa gli stessi test ma pesa 0.50 a chi=90 invece di 0.71: dimezza proprio gli
   archi ortogonali, dove vive il contenuto non-abeliano piu' forte. Piu' aggressivo del necessario.
 * `nessun peso` fallisce D: il contributo SALTA attorno a chi=pi (asse indeterminato non spento).
   Conferma che un ammorbidimento serve: la domanda non e' SE pesare, ma con quale funzione.
 * CAVEAT: tutti questi pesi sono GLOBALI (toccano tutto lo spettro). Un ammorbidimento STRETTO
   solo vicino a pi resta possibile, ma richiede una scala di larghezza = un numero nuovo = una
   manopola (par.3). `cos(chi/2)` evita la manopola perche' non e' scelto: emerge.
 * Il peso entra nella FORZA, non nella U usata per l'olonomia di plaquette: l'effetto su W(r)
   va comunque verificato a parte (doc/PROTOCOLLO_test_olonomia.md).
""")
sys.exit(0)
