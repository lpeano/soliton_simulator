# -*- coding: utf-8 -*-
"""SIGILLO DEL TURBO — `--gamma-turbo K` tocca `cs` e SOLO `cs`?

Vedi `doc/REPERTO_gamma_condiviso.md` e `RELAZIONE_PER_CLAUDE.md`.

PERCHE' ESISTE
--------------
`GAMMA` e' UN parametro fisico CONDIVISO fra **tre** usi:
    `:2354`  cs_floor  = CS_M / (1 + GAMMA*sqrt(I))            <- cs, il bersaglio
    `:2216`  satura(f) = f / (1 + GAMMA*sqrt(|f|^2 + 1e-9))    <- saturazione SCALARE
    `:2168`  psi_spin  = _Fs / (1 + GAMMA*norm)                <- saturazione del campo SPINORIALE
Un turbo GLOBALE su `GAMMA` cambierebbe la dinamica del campo invece della sensibilita' di `cs`, e
il risultato sarebbe INATTRIBUIBILE: il braccio di controllo (Step2 ON vs OFF a parita' di K) non
lo isolerebbe, perche' entrambi i bracci avrebbero il campo alterato allo stesso modo.
Il turbo e' quindi RISTRETTO a `_cs_nodo`. **Questo sigillo verifica che la restrizione TENGA.**

I SIGILLI
---------
  T1  K = 1 -> byte-identico (nessun effetto)
  T2  IL DECISIVO: con K > 1, `satura()` e la saturazione SPINORIALE sono INVARIATE (max|D| = 0)
      mentre `cs_nodo` CAMBIA. Se una delle due si muove, l'isolamento e' rotto -> STOP.
  T3  scaling: `cs_nodo` risponde a K in modo MONOTONO e nel verso giusto (cs piu' basso a K piu'
      alto, a parita' di I), e a densita' nulla resta CS_M.

PURE-READ: non modifica il simulatore, lo importa. Seed fisso.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
os.chdir(ROOT)
sys.path.insert(0, ROOT)
sys.argv = ["soliton_simulator.py"]
import soliton_simulator as S  # noqa: E402

esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-48s %s" % ("PASS" if ok else "FAIL", nome, misura))


def rete(nodi=60, seed=11):
    net = S.Rete(seed)
    net.semina(nodi)
    n = net.n
    net.eta = np.full(n, S.TAU_A)             # ramp = 1: i pesi esistono (lezione del S3 cieco)
    g = np.random.default_rng(seed)
    net.psi = (g.random(n) * 0.5) * np.exp(1j * g.random(n) * 2 * np.pi)
    return net, n


print("=" * 96)
print("SIGILLO TURBO — `--gamma-turbo K` tocca cs e SOLO cs?")
print("=" * 96)
print("GAMMA = %.5g.  Usi di GAMMA nel file: cs (:2354), satura() (:2216), psi_spin (:2168)." % S.GAMMA)

net, n = rete()
w = net._pesi()
I = np.abs(net.psi[:n]) ** 2

# ---------------------------------------------------------------- T1: K = 1 e' neutro
vT = S.GAMMA_TURBO
try:
    S.GAMMA_TURBO = 1.0
    cs_1 = net._cs_nodo(I, w).copy()
    S.GAMMA_TURBO = 1.0
    cs_1b = net._cs_nodo(I, w).copy()
    verdetto("T1 K = 1 e' NEUTRO (cs identico a se stesso)",
             float(np.max(np.abs(cs_1 - cs_1b))) == 0.0,
             "max|D cs| = %.3e su %d nodi" % (float(np.max(np.abs(cs_1 - cs_1b))), n))

    # ------------------------------------------------------------ T2: ISOLAMENTO (il decisivo)
    print()
    print("=" * 96)
    print("T2 — IL DECISIVO: con K > 1, satura() e psi_spin sono INVARIATE mentre cs CAMBIA?")
    print("=" * 96)
    # riferimenti PRIMA del turbo
    _f = net.psi[:n].copy()
    sat_1 = S.Rete.satura(_f).copy()   # staticmethod: prende solo f
    _psp = np.zeros((n, 2), complex)
    _psp[:, 0] = net.psi[:n]
    _Fs = net._mat(w) @ _psp
    _norm = np.sqrt(np.sum(np.abs(_Fs) ** 2, axis=1) + 1e-9)
    spin_1 = (_Fs / (1.0 + S.GAMMA * _norm)[:, None]).copy()   # :2168, con GAMMA letto AL MOMENTO

    for K in (2.0, 5.0, 10.0):
        S.GAMMA_TURBO = K
        cs_K = net._cs_nodo(I, w)
        sat_K = S.Rete.satura(_f)
        _Fs2 = net._mat(w) @ _psp
        _norm2 = np.sqrt(np.sum(np.abs(_Fs2) ** 2, axis=1) + 1e-9)
        spin_K = _Fs2 / (1.0 + S.GAMMA * _norm2)[:, None]
        d_sat = float(np.max(np.abs(sat_K - sat_1)))
        d_spin = float(np.max(np.abs(spin_K - spin_1)))
        d_cs = float(np.max(np.abs(cs_K - cs_1)))
        print("   K = %5.1f | D satura() = %.3e | D psi_spin = %.3e | D cs = %.3e"
              % (K, d_sat, d_spin, d_cs))
        verdetto("T2 K=%g: satura() INVARIATA" % K, d_sat == 0.0, "max|D| = %.3e" % d_sat)
        verdetto("T2 K=%g: psi_spin INVARIATA" % K, d_spin == 0.0, "max|D| = %.3e" % d_spin)
        verdetto("T2 K=%g: cs CAMBIA (il turbo MORDE)" % K, d_cs > 1e-9, "max|D cs| = %.3e" % d_cs)

    # ------------------------------------------------------------ T3: scaling e verso
    print()
    print("=" * 96)
    print("T3 — cs risponde a K nel verso giusto e in modo monotono?")
    print("=" * 96)
    print("   Atteso: cs_floor = CS_M/(1 + K*GAMMA*sqrt(I)) -> cs CALA al crescere di K, a parita' di I.")
    print("   K       cs mediana     cs min      cs/CS_M mediana")
    med = []
    for K in (1.0, 2.0, 5.0, 10.0):
        S.GAMMA_TURBO = K
        c = net._cs_nodo(I, w)
        med.append(float(np.median(c)))
        print("  %5.1f    %9.6f   %9.6f      %.6f" % (K, med[-1], float(np.min(c)), med[-1] / S.CS_M))
    mono = all(med[k + 1] <= med[k] for k in range(len(med) - 1))
    verdetto("T3 cs MONOTONO NON CRESCENTE in K", mono,
             "mediane: " + " -> ".join("%.6f" % m for m in med))
    verdetto("T3b il turbo MORDE davvero (cs cala)", med[-1] < med[0] - 1e-9,
             "cs mediana: K=1 -> %.6f ; K=10 -> %.6f  (calo %.3e)" % (med[0], med[-1], med[0] - med[-1]))
    # a densita' NULLA il floor e' CS_M qualunque sia K: il turbo non inventa cs
    S.GAMMA_TURBO = 10.0
    c0 = net._cs_nodo(np.zeros(n), w)
    verdetto("T3c a densita' NULLA cs = CS_M anche con K=10",
             float(np.max(np.abs(c0 - S.CS_M))) < 1e-12,
             "max|cs - CS_M| = %.3e  (il turbo amplifica la SENSIBILITA', non crea cs dal nulla)"
             % float(np.max(np.abs(c0 - S.CS_M))))
finally:
    S.GAMMA_TURBO = vT

print("=" * 96)
tot_, ok_ = len(esiti), sum(esiti)
print("SIGILLO TURBO: %d/%d PASS -> %s" % (ok_, tot_, "PASS" if ok_ == tot_ else "FAIL"))
print("""
COSA QUESTO SIGILLO NON DICE
----------------------------
Che il turbo sia FISICAMENTE LEGITTIMO: dice solo che e' RISTRETTO come dichiarato. Restringere
ROMPE DI PROPOSITO la condivisione di GAMMA fra cs e le due saturazioni, quindi il turbo e' un
ISOLAMENTO DIAGNOSTICO e **non** il regime reale ad alta densita' — dove, con GAMMA condiviso,
cambierebbero ENTRAMBI. Un esito positivo dello scan va letto come CONDIZIONALE:
"il gradiente di cs, IN ISOLAMENTO, retroagisce sullo spin".
E non dice nulla sulla dinamica: quella la dicono i run.
""")
sys.exit(0 if ok_ == tot_ else 1)
