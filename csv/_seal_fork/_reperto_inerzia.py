# -*- coding: utf-8 -*-
"""REPERTO — il PEZZO 3 cablato sui Bloch degli spinori trasportati e' IDENTICAMENTE INERTE.

Non e' un bug del cablaggio: e' un TEOREMA. Se i Bloch da cui si costruisce la connessione sono
i Bloch DEGLI STESSI spinori che vengono trasportati, allora

        <psi_i| N_ij |psi_j>  ==  2 <psi_i|psi_j>          esattamente

quindi N/2 agisce come l'IDENTITA' sull'overlap e la forza non cambia di un bit.

DIMOSTRAZIONE (due righe):
    (n_i.sigma)(n_j.sigma) = (n_i.n_j) I + i (n_i x n_j).sigma
    =>  N_ij = (1 + n_i.n_j) I + i (n_i x n_j).sigma = I + (n_i.sigma)(n_j.sigma)
    Ma n_i e' il Bloch di psi_i, quindi |psi_i> e' autovettore di (n_i.sigma) con autovalore +1:
        (n_i.sigma)|psi_i> = |psi_i>   ->   <psi_i|(n_i.sigma) = <psi_i|
    e analogamente (n_j.sigma)|psi_j> = |psi_j>. Quindi
        <psi_i|N|psi_j> = <psi_i|psi_j> + <psi_i|(n_i.sigma)(n_j.sigma)|psi_j> = 2<psi_i|psi_j>.

SIGNIFICATO: la connessione di Berry costruita dagli stessi stati che trasporta e' BANALE SULLA
FORZA. Trasporta psi_j esattamente su psi_i, quindi l'overlap non puo' cambiare. E' la forma forte
del caveat gia' scritto in doc/ROADMAP_fork_SU2.md ("i link derivati dai soli Bloch sono schiavi
della materia, no gradi di liberta' propri"): non sono solo schiavi, sono INERTI.

NB: questo riguarda la FORZA. L'OLONOMIA di plaquette resta non banale (due U con assi diversi non
commutano, sigillo PEZZO 1 S9), quindi il fork puo' ancora produrre un DIAGNOSTICO non abeliano.
Ma un diagnostico non e' dinamica: se la forza non cambia, il fork non fa nulla al sistema.

Pure-read. Non tocca soliton_simulator.py.
"""
import numpy as np

SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.array([[1, 0], [0, -1]], complex)
I2 = np.eye(2, dtype=complex)


def bloch(p):
    a, b = p[:, 0], p[:, 1]
    return np.stack([2 * np.real(np.conj(a) * b), 2 * np.imag(np.conj(a) * b),
                     np.abs(a) ** 2 - np.abs(b) ** 2], axis=1)


def enne(ni, nj):
    d = np.sum(ni * nj, axis=1)
    c = np.cross(ni, nj)
    return ((1.0 + d)[:, None, None] * I2
            + 1j * (c[:, 0, None, None] * SX + c[:, 1, None, None] * SY + c[:, 2, None, None] * SZ))


def spinori(m, g):
    p = g.normal(size=(m, 2)) + 1j * g.normal(size=(m, 2))
    return p / np.linalg.norm(p, axis=1)[:, None]


g = np.random.default_rng(7)
M = 200000
ps, qs = spinori(M, g), spinori(M, g)

# --- CASO A: Bloch DEGLI STESSI spinori trasportati (= come il PEZZO 3 e' stato cablato) --------
N = enne(bloch(ps), bloch(qs))
lhs = np.einsum('kx,kxy,ky->k', np.conj(ps), N, qs)
rhs = 2.0 * np.sum(np.conj(ps) * qs, axis=1)
dA = float(np.max(np.abs(lhs - rhs)))
print("[CASO A] Bloch presi dagli STESSI spinori trasportati (cablaggio attuale)")
print("         max| <psi_i|N|psi_j> - 2<psi_i|psi_j> | = %.3e  su %d coppie" % (dA, M))
print("         -> N/2 == identita' sull'overlap: LA FORZA NON CAMBIA. Fork INERTE.")

# --- CASO B: Bloch da un campo DIVERSO (es. psi_spin, il campo emesso) --------------------------
rs, ss = spinori(M, g), spinori(M, g)
N2 = enne(bloch(rs), bloch(ss))
lhs2 = np.einsum('kx,kxy,ky->k', np.conj(ps), N2, qs)
scal = np.sum(np.conj(ps) * qs, axis=1)
dB = float(np.max(np.abs(np.imag(lhs2 / 2.0) - np.imag(scal))))
print()
print("[CASO B] Bloch presi da un campo DIVERSO dagli spinori trasportati")
print("         max| Im<psi_i|N/2|psi_j> - Im<psi_i|psi_j> | = %.3e" % dB)
print("         -> QUI il trasporto agisce davvero.")

print("""
LA DOMANDA CHE QUESTO APRE (decisione di Luca, non mia)
-------------------------------------------------------
Il fork e' inerte perche' la connessione e' costruita dagli stessi stati che trasporta. Per farlo
agire servirebbe che i Bloch della connessione e gli spinori trasportati siano oggetti DIVERSI.
Nel codice quei due oggetti esistono gia': `_nb_grav` costruisce i Bloch dal campo EMESSO
`psi_spin`, mentre cio' che viene trasportato in `_coppia_interferenza` e' `_psi_spinor`.
Ma attenzione: sceglierlo PERCHE' fa muovere il risultato sarebbe tarare un meccanismo per
ottenere un effetto - l'opposto del par.3. La domanda giusta e' FISICA: la connessione di gauge
su un arco, in questo sistema, da CHE COSA deve essere costruita? Finche' non c'e' una risposta
derivata, il cablaggio resta inerte e il flag resta OFF.
""")
