# -*- coding: utf-8 -*-
"""SIGILLO PEZZO 1 — connessione di Berry U_ij in SU(2) (fork non-abeliano).

Verifica la funzione ISOLATA `Rete._link_su2`, senza farla girare dentro la dinamica
(il cablaggio nella forza e' il PEZZO 3). Pure-read: non istanzia la rete, non tocca RNG.

Verdetto secco: stampa PASS/FAIL per ogni sigillo ed esce 0 (tutti PASS) o 1 (almeno un FAIL).
Riferimento: doc/ROADMAP_fork_SU2.md (PEZZO 1 e PEZZO 2) + CLAUDE.md par.2 (sigilli).
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from soliton_simulator import Rete  # noqa: E402

I2 = np.eye(2, dtype=complex)
esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-46s %s" % ("PASS" if ok else "FAIL", nome, misura))


def versori(m, seed):
    """Versori isotropi (gaussiana normalizzata: nessun verso preferito)."""
    g = np.random.default_rng(seed).normal(size=(m, 3))
    return g / np.linalg.norm(g, axis=1)[:, None]


def bloch_di(psi):
    """Bloch di uno spinore (mappa di Pauli), stessa forma di _nb_grav."""
    a = psi[:, 0]
    b = psi[:, 1]
    n = np.stack([2.0 * np.real(np.conj(a) * b), 2.0 * np.imag(np.conj(a) * b),
                  np.abs(a) ** 2 - np.abs(b) ** 2], axis=1)
    return n / np.maximum(np.linalg.norm(n, axis=1), 1e-30)[:, None]


M = 20000
ni = versori(M, 20260913)
nj = versori(M, 13092026)
U, w = Rete._link_su2(ni, nj)

# --- S1. RIDUZIONE AL LIMITE: allineati -> U = I esattamente, w = 0 ---------------------------
Ua, wa = Rete._link_su2(ni, ni.copy())
d_id = np.max(np.abs(Ua - I2))
verdetto("S1 allineati -> U = I (riduzione al limite)", d_id == 0.0, "max|U-I| = %.3e" % d_id)
# [SPECIFICA CAMBIATA PER DELIBERA il 2026-09-13 - non e' il test aggiustato per farlo passare]
# PRIMA: w = sin(chi) -> ad allineati w = 0 e questo test pretendeva max|w| == 0.0 (e passava).
# ORA:   w = cos(chi/2) = |<n_i|n_j>| (overlap di spin) -> ad allineati w = 1, overlap MASSIMO.
# MOTIVO: sin(chi) spegneva gli archi a Bloch allineati, cioe' il canale di fase (EM). Misure e
# delibera in _sigillo_pezzo2.py (P5), _sigillo_pesi.py, _sigillo_N.py. La pretesa VECCHIA era
# sbagliata: se questo test tornasse a chiedere w=0 ad allineati, starebbe ri-chiedendo il bug.
verdetto("S1b allineati -> w = 1 (overlap massimo, EM preservato)",
         np.max(np.abs(wa - 1.0)) < 1e-15, "max|w - 1| = %.3e" % np.max(np.abs(wa - 1.0)))

# --- S2. UNITARIETA': U U^dag = I (conserva |psi| = 1) ----------------------------------------
UU = U @ np.conj(np.transpose(U, (0, 2, 1)))
d_un = np.max(np.abs(UU - I2))
verdetto("S2 unitarieta' U U^dag = I", d_un < 1e-12, "max|UU^dag - I| = %.3e" % d_un)

# --- S3. det U = 1 -> e' SU(2), non solo U(2) (det=1 lascia la fase U(1)/EM separata) ---------
det = U[:, 0, 0] * U[:, 1, 1] - U[:, 0, 1] * U[:, 1, 0]
d_det = np.max(np.abs(det - 1.0))
verdetto("S3 det U = 1 (SU(2), non U(2))", d_det < 1e-12, "max|det U - 1| = %.3e" % d_det)

# --- S4. ORIENTAMENTO DELL'ARCO: U_ji = U_ij^dag ----------------------------------------------
Uji, wji = Rete._link_su2(nj, ni)
d_or = np.max(np.abs(Uji - np.conj(np.transpose(U, (0, 2, 1)))))
verdetto("S4 U_ji = U_ij^dag (orientamento arco)", d_or < 1e-12, "max|U_ji - U_ij^dag| = %.3e" % d_or)
verdetto("S4b w simmetrico (w_ij = w_ji)", np.max(np.abs(w - wji)) < 1e-15,
         "max|w_ij - w_ji| = %.3e" % np.max(np.abs(w - wji)))

# --- S5. CORRETTEZZA GEOMETRICA: U_ij trasporta davvero psi_j sul sito i -----------------------
# Non basta che U sia unitaria: deve essere LA rotazione giusta. U_ij psi_j deve dare psi_i a meno
# di fase globale -> |<psi_i|U_ij|psi_j>| = 1. (Esclusi i quasi-antipodali: li' il trasporto non e'
# definito e il PESO lo spegne.)
psi_i = Rete._bloch_a_spinore(ni)
psi_j = Rete._bloch_a_spinore(nj)
trasp = np.einsum('kxy,ky->kx', U, psi_j)
ovl = np.abs(np.sum(np.conj(psi_i) * trasp, axis=1))
buoni = w > 1e-6
d_tr = np.max(np.abs(ovl[buoni] - 1.0))
verdetto("S5 trasporto: |<psi_i|U_ij|psi_j>| = 1", d_tr < 1e-9,
         "max| |ovl| - 1 | = %.3e  (su %d archi non degeneri)" % (d_tr, int(buoni.sum())))
# controprova: il Bloch trasportato COINCIDE con n_i (non con n_j, non con altro)
d_bl = np.max(np.linalg.norm(bloch_di(trasp)[buoni] - ni[buoni], axis=1))
verdetto("S5b Bloch trasportato = n_i", d_bl < 1e-9, "max|R n_j - n_i| = %.3e" % d_bl)

# --- S6. ANTIPODALITA': il PESO la gestisce, nessun asse inventato -----------------------------
nap = versori(4000, 7)
Uap, wap = Rete._link_su2(nap, -nap)
fin = np.all(np.isfinite(Uap)) and np.all(np.isfinite(wap))
verdetto("S6 antipodali: nessun NaN/inf", fin, "finiti = %s" % fin)
verdetto("S6b antipodali: w = 0 (arco spento)", np.max(wap) < 1e-15, "max w = %.3e" % np.max(wap))
UUap = Uap @ np.conj(np.transpose(Uap, (0, 2, 1)))
d_unap = np.max(np.abs(UUap - I2))
verdetto("S6c antipodali: U resta unitaria", d_unap < 1e-12, "max|UU^dag - I| = %.3e" % d_unap)
# il contributo pesato all'arco e' nullo: nessuna direzione spuria entra nella forza
contrib = wap * np.abs(np.einsum('kx,kxy,ky->k', np.conj(Rete._bloch_a_spinore(nap)), Uap,
                                 Rete._bloch_a_spinore(-nap)))
verdetto("S6d antipodali: contributo pesato = 0", np.max(np.abs(contrib)) < 1e-15,
         "max|w*ovl| = %.3e" % np.max(np.abs(contrib)))

# --- S7. CONTINUITA' DEL PESO: w = sin(chi), niente soglie nette -------------------------------
# w deve svanire LISCIO ai due estremi. Confronto con sin(chi) analitico su tutto l'intervallo.
th = np.linspace(0.0, np.pi, 200001)
a_ = np.stack([np.zeros_like(th), np.zeros_like(th), np.ones_like(th)], axis=1)
b_ = np.stack([np.sin(th), np.zeros_like(th), np.cos(th)], axis=1)
_, wsc = Rete._link_su2(a_, b_)
# [SPECIFICA CAMBIATA PER DELIBERA - vedi S1b] PRIMA: w = sin(chi). ORA: w = cos(chi/2).
d_w = np.max(np.abs(wsc - np.cos(th / 2.0)))
verdetto("S7 w = cos(chi/2) esatto (nessuna soglia)", d_w < 1e-12,
         "max|w - cos(chi/2)| = %.3e" % d_w)
salto = np.max(np.abs(np.diff(wsc)))
verdetto("S7b w continuo (nessun salto)", salto < 1e-4, "max salto = %.3e" % salto)

# --- S8. PUREZZA: la funzione non consuma RNG e non muta gli input -----------------------------
rng = np.random.default_rng(12345)
st0 = rng.bit_generator.state
ni_c = ni.copy()
nj_c = nj.copy()
Rete._link_su2(ni, nj)
st1 = rng.bit_generator.state
verdetto("S8 pure-read: RNG non consumato", str(st0) == str(st1), "stato RNG invariato")
verdetto("S8b pure-read: input non mutati",
         np.array_equal(ni, ni_c) and np.array_equal(nj, nj_c), "n_i, n_j invariati")

# --- S9. NON-ABELIANITA': due link con assi diversi NON commutano ------------------------------
# E' il punto del fork: con lo scalare A_ij il commutatore sarebbe identicamente nullo.
U1, _ = Rete._link_su2(np.array([[0.0, 0.0, 1.0]]), np.array([[1.0, 0.0, 0.0]]))
U2, _ = Rete._link_su2(np.array([[0.0, 0.0, 1.0]]), np.array([[0.0, 1.0, 0.0]]))
comm = np.max(np.abs(U1[0] @ U2[0] - U2[0] @ U1[0]))
verdetto("S9 non commutativita' [U1,U2] != 0", comm > 1e-3, "max|[U1,U2]| = %.3e" % comm)

print("-" * 78)
tot = len(esiti)
ok = sum(esiti)
print("SIGILLO PEZZO 1: %d/%d PASS -> %s" % (ok, tot, "PASS" if ok == tot else "FAIL"))
sys.exit(0 if ok == tot else 1)
