# -*- coding: utf-8 -*-
"""FASE C — QUALE CANALE E' LA PORTA D'INGRESSO DEL DISORDINE PER LO SPIN?

L'IPOTESI DA TESTARE (non da assumere)
--------------------------------------
"dare memoria a tutte le dinamiche che dovrebbero averla combatte il disordine".

LA PRECISAZIONE CHE GOVERNA LA LETTURA
--------------------------------------
La memoria NON ORDINA. Un rilassamento dx/dt = (x_eq - x)/tau RALLENTA i cambiamenti, non li
ORIENTA: la prova e' nel repo, lo Strato 1 e' memoria pura ed e' passato 23/23 SENZA ordinare i
Bloch. La memoria agisce sui TASSI (filtro passa-basso sul rumore veloce, vita piu' lunga della
correlazione ereditata). Quindi la domanda per ogni canale e' un CONFRONTO DI TEMPI, non
"aiuta o no".

COSA MISURA (tutto PURE-READ, su uno stato gia' evoluto)
--------------------------------------------------------
Ricostruisce, SENZA mutare nulla, gli ingredienti del passo spinoriale al punto in cui il
disordine entra (`_passo_spinoriale`, righe ~1855-1890 e ~2030-2046):

    B        = media pesata dei Bloch dei VICINI (con il segno chirale)
    inerzia  = max(rho_sorgente, 1e-6)                <- il DENOMINATORE
    omega   ~ cross(B, nb) / inerzia                   <- la coppia, amplificata da 1/inerzia
    theta    = |omega| * dt_n                          <- RADIANTI DI ROTAZIONE PER PASSO

`theta` e' il numero che decide tutto: se e' dell'ordine del radiante, il Bloch fa mezzo giro per
tick e nessuna memoria sulla VELOCITA' puo' trattenerlo, perche' la memoria su omega conserva la
ROTAZIONE, non la DIREZIONE.

PUREZZA
-------
Ricalcola gli ingredienti in locale da array di stato. Non chiama `_passo_spinoriale`, non
committa nulla, non consuma `net.rng`. Le uniche funzioni del simulatore usate sono quelle che
servono a ricostruire i pesi, e vengono chiamate su una COPIA profonda della rete, cosi' anche
le loro mutazioni di cache non toccano lo stato vero.
"""
import argparse
import contextlib
import copy
import io
import os
import sys

import numpy as np

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _prepara():
    os.chdir(RADICE); sys.path.insert(0, RADICE)
    sys.argv = ["soliton_simulator.py", "--batch", "--nmasse", "3", "--sep", "8",
                "--passi", "1", "--ogni", "100000", "--db-ogni", "100000",
                "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto", "--chi-core",
                "--calore-scal", "--deparam-orologio", "--verlet", "--cs-dinamico",
                "--csv", os.path.join(os.environ.get("TMP", "."), "_canali.csv")]
    import soliton_simulator as S
    a = S._cli(); S._applica_regime(a)
    with contextlib.redirect_stdout(io.StringIO()):
        S._applica_flag(a)
    return S


def _scena(S, seed, passi):
    net = S.Rete(seed); net.semina(80)
    for _ in range(6):
        S.scuoti_vuoto(net); net.step(); net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()
    Nc = S.massa_critica_collasso()
    for k in range(3):
        ang = 2 * np.pi * k / 3
        net.nuova_massa(int(Nc * 0.6), raggio=0.8,
                        centro=(8.0 * np.cos(ang), 8.0 * np.sin(ang), 0.0), fase=0.0)
    for _ in range(passi):
        S.scuoti_vuoto(net); net.step(); net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()
    return net


def _perc(v, etichetta, unita=""):
    v = np.asarray(v, float)
    q = np.percentile(v, [5, 25, 50, 75, 95])
    print("  %-26s mediana %10.3g   [5%%..95%%] %10.3g .. %-10.3g  max %10.3g %s"
          % (etichetta, q[2], q[0], q[4], v.max(), unita))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--passi", type=int, default=60)
    ap.add_argument("--seed", type=int, default=1)
    o = ap.parse_args()
    S = _prepara()
    net = _scena(S, o.seed, o.passi)
    lav = copy.deepcopy(net)              # tutte le mutazioni di cache restano QUI
    n = lav.n
    print("stato: n=%d archi=%d  dopo %d passi (seme %d)" % (n, len(lav.i), o.passi, o.seed))
    print("costanti: TAU_A=%.3g  TAU_A_LOCALE=%s  DT=%.3g  LAM=%.3g  GAMMA=%.3g  CS_M=%.3g"
          % (S.TAU_A, S.TAU_A_LOCALE, S.DT, S.LAM, S.GAMMA, S.CS_M))

    w = lav._pesi()
    lav.calcola_psi(w)
    i, j = lav.i, lav.j
    nb = np.asarray(lav._nb[:n], float)
    rho = lav._rho_sorgente()
    inerzia = np.maximum(rho, 1e-6)

    chi_nodi = lav.perc_chi[:n].astype(float)
    chi = (chi_nodi[i] * chi_nodi[j]).astype(float)
    mask = (i < n) & (j < n)
    ii, jj, wl, cl = i[mask], j[mask], w[mask], chi[mask]
    B = np.zeros((n, 3)); deg = np.zeros(n)
    refl = np.where(cl[:, None] > 0, np.array([1.0, 1.0, -1.0]), np.array([1.0, 1.0, 1.0]))
    np.add.at(B, ii, nb[jj] * wl[:, None] * refl); np.add.at(deg, ii, wl)
    np.add.at(B, jj, nb[ii] * wl[:, None] * refl); np.add.at(deg, jj, wl)
    B = B / np.maximum(deg[:, None], 1e-9)

    r = lav.ritmo()
    r = np.ones(n) if r is None else np.asarray(r)[:n]
    dt_n = S.DT * r

    coppia = np.cross(B, nb)
    omega_istante = coppia / inerzia[:, None]
    theta = np.linalg.norm(omega_istante, axis=1) * dt_n

    print()
    print("=" * 96)
    print("GLI INGREDIENTI, al punto in cui il disordine entra")
    print("=" * 96)
    _perc(np.linalg.norm(B, axis=1), "|B| (media dei vicini)")
    _perc(rho, "rho sorgente")
    _perc(inerzia, "inerzia = max(rho,1e-6)")
    print("  frazione di nodi col PAVIMENTO 1e-6 attivo (rho < 1e-6): %.1f%%"
          % (100.0 * np.mean(rho < 1e-6)))
    _perc(np.linalg.norm(coppia, axis=1), "|cross(B,nb)| (coppia nuda)")
    _perc(np.linalg.norm(omega_istante, axis=1), "|omega| = coppia/inerzia", "rad/tempo")
    _perc(dt_n, "dt_n = DT*r")
    print()
    _perc(np.degrees(theta), "theta = |omega|*dt_n", "GRADI PER PASSO")
    print("  frazione di nodi con theta > 90 gradi in UN passo : %.1f%%" % (100.0 * np.mean(theta > np.pi / 2)))
    print("  frazione con theta > 360 gradi (giro intero)      : %.1f%%" % (100.0 * np.mean(theta > 2 * np.pi)))

    # VALORE-NULL per |B|: gli STESSI pesi, ma con i Bloch dei vicini PERMUTATI. Se |B| misurato
    # coincide col null, i pesi non portano coerenza: il disordine e' nei VICINI, non in `w`.
    rng_null = np.random.default_rng(20260915)
    perm = rng_null.permutation(n)
    nb_perm = nb[perm]
    B0 = np.zeros((n, 3)); deg0 = np.zeros(n)
    np.add.at(B0, ii, nb_perm[jj] * wl[:, None] * refl); np.add.at(deg0, ii, wl)
    np.add.at(B0, jj, nb_perm[ii] * wl[:, None] * refl); np.add.at(deg0, jj, wl)
    B0 = B0 / np.maximum(deg0[:, None], 1e-9)
    k_eff = (deg ** 2) / np.maximum(
        np.bincount(ii, wl ** 2, minlength=n) + np.bincount(jj, wl ** 2, minlength=n), 1e-30)
    print()
    print("=" * 96)
    print("IL CANALE `w` — i pesi portano coerenza, o il disordine e' tutto nei VICINI?")
    print("=" * 96)
    _perc(np.linalg.norm(B, axis=1), "|B| MISURATO")
    _perc(np.linalg.norm(B0, axis=1), "|B| NULL (vicini permutati)")
    _perc(k_eff, "k_eff = (sum w)^2/sum w^2", "vicini efficaci")
    _perc(1.0 / np.sqrt(np.maximum(k_eff, 1e-30)), "1/sqrt(k_eff) atteso casuale")
    rap = float(np.median(np.linalg.norm(B, axis=1))) / max(float(np.median(np.linalg.norm(B0, axis=1))), 1e-30)
    print("  rapporto mediano |B|_misurato / |B|_null : %.3f   (1.000 = nessuna coerenza dai pesi)" % rap)

    om_vero = np.linalg.norm(np.asarray(lav.omega_s[:n], float), axis=1)
    theta_vero = om_vero * dt_n
    print()
    print("=" * 96)
    print("LO STATO VERO — `omega_s` LETTO DAL SIMULATORE (non ricostruito)")
    print("=" * 96)
    _perc(om_vero, "|omega_s| (memoria hebbiana)", "rad/tempo")
    _perc(np.degrees(theta_vero), "theta_vero = |omega_s|*dt_n", "GRADI PER PASSO")
    print("  giri interi per passo (mediana)                  : %.1f" % (float(np.median(theta_vero)) / (2 * np.pi)))
    print("  frazione di nodi con theta_vero > 360 gradi      : %.1f%%" % (100.0 * np.mean(theta_vero > 2 * np.pi)))
    print("  PUNTO FISSO della memoria: omega_eq = tau * coppia/inerzia -> PIU' memoria = PIU' rotazione.")

    print()
    print("=" * 96)
    print("I TEMPI A CONFRONTO (FASE C.2)")
    print("=" * 96)
    med_theta = float(np.median(theta))
    tau_dis = 1.0 / max(med_theta / (np.pi / 2), 1e-30)
    print("  tau_disordine (passi per ruotare di 90 gradi, mediana) : %.4f passi" % tau_dis)
    print("  tau_memoria GIA' PRESENTE su omega_s (TAU_A)           : %.1f  [tempo proprio] = %.0f passi"
          % (S.TAU_A, S.TAU_A / S.DT))
    if S.TAU_A_LOCALE:
        dens = np.abs(lav.psi[:n]) ** 2
        rif = max(float(np.median(dens[dens > 1e-6])), 1e-6) if np.any(dens > 1e-6) else 1.0
        tau_loc = S.TAU_A * np.maximum(dens / rif, 0.05)
        _perc(tau_loc / S.DT, "  TAU_A locale / DT", "PASSI")
    print()
    print("  Se theta e' dell'ordine di 90 gradi per passo, la memoria su omega NON trattiene il")
    print("  Bloch: conserva la ROTAZIONE, non la DIREZIONE. E' il punto della FASE C.")


if __name__ == "__main__":
    main()
