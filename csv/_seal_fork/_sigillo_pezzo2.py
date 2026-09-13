# -*- coding: utf-8 -*-
"""SIGILLO PEZZO 2 — il PESO sin(chi) sul CONTRIBUTO D'ARCO (fork non-abeliano).

Il PEZZO 1 ha sigillato i FATTORI (U unitaria, w=sin(chi) continuo). Qui si sigilla la GRANDEZZA
che finira' davvero nella forza al PEZZO 3:

    contrib_ij = w_ij * Im<psi_i| U_ij |psi_j>        (oggi:  Im<psi_i|psi_j>, scalare)

Non tocca soliton_simulator.py: usa `Rete._link_su2` cosi' com'e' (blob invariato).
Verdetto secco: PASS/FAIL per sigillo, exit 0 (tutti PASS) / 1 (almeno un FAIL).
Riferimento: doc/ROADMAP_fork_SU2.md PEZZO 2 + doc/BUSSOLA_TECNICA par.4.1.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from soliton_simulator import Rete  # noqa: E402

esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-48s %s" % ("PASS" if ok else "FAIL", nome, misura))


def spinori(m, seed):
    """Spinori generici normalizzati: fase propria ARBITRARIA, non i rappresentanti canonici.
    E' il caso reale: nel codice `_psi_spinor` non e' il canonico del Bloch di `_nb_grav`."""
    g = np.random.default_rng(seed)
    p = g.normal(size=(m, 2)) + 1j * g.normal(size=(m, 2))
    return p / np.linalg.norm(p, axis=1)[:, None]


def versori(m, seed):
    g = np.random.default_rng(seed).normal(size=(m, 3))
    return g / np.linalg.norm(g, axis=1)[:, None]


def contributo(ni, nj, pi_, pj):
    """w_ij * Im<psi_i| U_ij |psi_j> — il termine d'arco del PEZZO 3."""
    U, w = Rete._link_su2(ni, nj)
    return w * np.imag(np.einsum('kx,kxy,ky->k', np.conj(pi_), U, pj)), w


M = 20000
ni = versori(M, 11)
nj = versori(M, 22)
pi_ = spinori(M, 33)
pj = spinori(M, 44)
c_ij, w_ij = contributo(ni, nj, pi_, pj)

# --- P1. AZIONE-REAZIONE: il contributo e' ANTISIMMETRICO nello scambio i<->j -----------------
# Sigillo FISICO: U_ji = U_ij^dag => <psi_j|U_ji|psi_i> = conj(<psi_i|U_ij|psi_j>) => Im cambia
# segno, e w e' simmetrico. Se fallisse, la coppia i-j creerebbe momento dal nulla.
c_ji, _ = contributo(nj, ni, pj, pi_)
d_as = np.max(np.abs(c_ij + c_ji))
verdetto("P1 antisimmetria i<->j (azione-reazione)", d_as < 1e-12,
         "max|c_ij + c_ji| = %.3e" % d_as)

# --- P2. LIMITE ALLINEATO: il contributo svanisce, e ci va LISCIO -----------------------------
th = np.linspace(0.0, np.pi, 200001)
a_ = np.tile(np.array([0.0, 0.0, 1.0]), (len(th), 1))
b_ = np.stack([np.sin(th), np.zeros_like(th), np.cos(th)], axis=1)
pa = np.tile(spinori(1, 101), (len(th), 1))
pb = np.tile(spinori(1, 202), (len(th), 1))
c_sc, w_sc = contributo(a_, b_, pa, pb)
verdetto("P2 allineati (chi=0): contributo = 0", abs(c_sc[0]) < 1e-15, "c(chi=0) = %.3e" % c_sc[0])
verdetto("P2b antipodali (chi=pi): contributo = 0", abs(c_sc[-1]) < 1e-15,
         "c(chi=pi) = %.3e" % c_sc[-1])

# --- P3. CONTINUITA' E LISCEZZA: nessun salto, nessuna soglia --------------------------------
salto = np.max(np.abs(np.diff(c_sc)))
verdetto("P3 continuita' (nessun salto in chi)", salto < 1e-4, "max salto = %.3e" % salto)
# liscio = la derivata numerica resta limitata anche AI BORDI (una soglia netta darebbe un picco)
der = np.abs(np.diff(c_sc) / np.diff(th))
verdetto("P3b liscio ai bordi (derivata limitata)", np.max(der) < 10.0,
         "max|dc/dchi| = %.3f  (bordi: %.3f / %.3f)" % (np.max(der), der[0], der[-1]))

# --- P4. NESSUNA DIREZIONE SPURIA dal caso degenere -------------------------------------------
nap = versori(4000, 7)
c_ap, w_ap = contributo(nap, -nap, spinori(4000, 55), spinori(4000, 66))
verdetto("P4 antipodali: contributo identicamente 0", np.max(np.abs(c_ap)) == 0.0,
         "max|c| = %.3e" % np.max(np.abs(c_ap)))
c_al, _ = contributo(nap, nap.copy(), spinori(4000, 55), spinori(4000, 66))
verdetto("P4b allineati: contributo identicamente 0", np.max(np.abs(c_al)) == 0.0,
         "max|c| = %.3e" % np.max(np.abs(c_al)))

# --- P5. CONFRONTO COL RAMO SCALARE ATTUALE — il punto delicato --------------------------------
# Lo scalare di oggi e' Im<psi_i|psi_j> (senza U, senza w). Domanda del sigillo del PEZZO 3:
# "allineati -> byte-identico allo scalare". Lo verifico QUI, prima di cablare.
sc_al = np.imag(np.sum(np.conj(spinori(4000, 55)) * spinori(4000, 66), axis=1))
verdetto("P5 allineati: scalare Im<psi_i|psi_j> e' NON nullo",
         np.max(np.abs(sc_al)) > 1e-3,
         "max|Im<psi_i|psi_j>| = %.3e  (media |.| = %.3e)" % (np.max(np.abs(sc_al)),
                                                              np.mean(np.abs(sc_al))))
print("     ^-- NON e' un FAIL del peso: e' il REPERTO da portare al PEZZO 3 (vedi in fondo).")
# controprova nel caso in cui gli spinori SONO i canonici dei Bloch (fasi legate):
pc = Rete._bloch_a_spinore(nap)
sc_can = np.imag(np.sum(np.conj(pc) * pc, axis=1))
verdetto("P5b allineati + spinori canonici: scalare = 0",
         np.max(np.abs(sc_can)) < 1e-15, "max|Im<psi_i|psi_j>| = %.3e" % np.max(np.abs(sc_can)))

# --- P6. IL PESO NON INTRODUCE VERSI: isotropia del contributo ---------------------------------
# Se il peso o l'asse introducessero una direzione preferita, la media del contributo su archi
# isotropi sarebbe != 0 in modo sistematico. Deve essere ~0 entro l'errore statistico (1/sqrt(M)).
med = np.mean(c_ij)
err = np.std(c_ij) / np.sqrt(M)
verdetto("P6 nessun verso preferito (media ~ 0)", abs(med) < 5.0 * err,
         "media = %+.3e  (3 sigma = %.3e)" % (med, 3.0 * err))

# --- P7. SCALA: il peso non amplifica (|contrib| <= 1, nessun guadagno spurio) -----------------
verdetto("P7 |contributo| <= 1 (nessuna amplificazione)", np.max(np.abs(c_ij)) <= 1.0,
         "max|c| = %.6f" % np.max(np.abs(c_ij)))

print("-" * 86)
tot = len(esiti)
ok = sum(esiti)
print("SIGILLO PEZZO 2: %d/%d PASS -> %s" % (ok, tot, "PASS" if ok == tot else "FAIL"))
print("""
REPERTO PER IL PEZZO 3 (da leggere PRIMA di cablare, non dopo)
--------------------------------------------------------------
P5 misura una cosa che la ROADMAP da' per scontata e che NON lo e'. Il sigillo previsto per il
PEZZO 3 dice: "flag OFF / tutti allineati -> BYTE-IDENTICO al ramo scalare". Le due meta' non
sono equivalenti:
  * flag OFF -> byte-identico: VERO per costruzione (non si esegue il ramo nuovo).
  * tutti allineati -> byte-identico: **FALSO in generale.** Con chi=0 il peso vale w=0, quindi il
    contributo nuovo e' ZERO; ma lo scalare di oggi, Im<psi_i|psi_j>, NON e' zero se i due spinori
    hanno FASI diverse (P5: |Im| fino a ~1). Coincidono solo se gli spinori sono i rappresentanti
    canonici dei rispettivi Bloch (P5b), che nel codice NON e' il caso: `_nb_grav` costruisce i
    Bloch dal campo EMESSO `psi_spin`, mentre a essere trasportato e' `_psi_spinor`. Sono due
    oggetti distinti: i Bloch possono essere allineati mentre le fasi no.
  * CONSEGUENZA FISICA: il peso sin(chi) SPEGNE gli archi a Bloch allineati — cioe' proprio quelli
    che oggi portano il contributo di FASE (settore U(1)/orologio, il canale EM). Non e' un bug del
    peso: e' quello che il peso fa per costruzione. Ma va DECISO consapevolmente, non scoperto dopo.
  * NON e' un problema di antipodalita': li' anche lo scalare tende a spegnersi da solo.
Da portare a Luca prima del PEZZO 3. Nessuna scelta presa qui: questo script MISURA, non decide.
""")
sys.exit(0 if ok == tot else 1)
