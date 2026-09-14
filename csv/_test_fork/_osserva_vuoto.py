# -*- coding: utf-8 -*-
"""OSSERVATORE DEL VUOTO — misura PURE-READ di chi (angoli fra Bloch vicini) e <n> (isotropia).

PERCHE' ESISTE
--------------
Due cose erano date per scontate e mai misurate:
  1. lo scuotimento del vuoto e' MEDIATO (colpisce self._nb a :1803, che a :2034 viene sovrascritto
     dalla proiezione del primario; raggiunge _psi_spinor solo via il torque cross(B,nb), quindi
     O(amp*|B|*dt) e non O(amp)). SCUOTE ABBASTANZA da rompere la degenerazione dei Bloch?
  2. l'ISOTROPIA e' ASSERITA, non dimostrata (doc/ROADMAP_fork_SU2.md:46 cita una riga marcata
     "# APERTO:" che e' un condizionale). <n> resta ~0, o la dinamica rettifica il rumore isotropo?

COME NON CONTAMINA LA FISICA (par.2.3)
--------------------------------------
Non e' una modifica a soliton_simulator.py: e' un OSSERVATORE ESTERNO che avvolge `Rete.step` e,
DOPO che il passo e' finito, LEGGE gli array committati. Non scrive nulla, non chiama nulla che
muti stato (in particolare MAI `calcola_psi()`, che riscriverebbe `self.psi`), non consuma `net.rng`.
La purezza non e' affermata: e' sigillata da `_sigillo_osservatore.py` (run con/senza -> stato
byte-identico), che va girato PRIMA dei run lunghi.

SEPARAZIONE MATERIA / VUOTO — zero parametri nuovi (par.3)
----------------------------------------------------------
La soglia e' `Lam = <|Psi|^2>` = `lambda_vuoto(net)`, cioe' la scala di energia del vuoto CHE IL
SISTEMA USA GIA' per modulare l'ampiezza dello scuotimento (`amp = sqrt(Lam)/(1+I2/Lam)`). Non e'
un numero scelto: e' una grandezza di stato. Per robustezza si riportano ANCHE i percentili p10/p90,
cosi' la lettura non dipende dalla soglia.
NB: `Lam` e' una media globale, ma qui e' una CLASSIFICAZIONE DIAGNOSTICA, non una correzione
applicata allo stato: il divieto del par.4 ("niente sottrazione della media globale") riguarda la
DINAMICA, e nulla di quanto segue rientra nella dinamica.

USO
---
python csv/_test_fork/_osserva_vuoto.py --seed 1 --passi 2000 --ogni 100 \\
       --tag on   [--regime-det]  [--no-osserva]
"""
import argparse
import csv as _csv
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--passi", type=int, default=2000)
    ap.add_argument("--ogni", type=int, default=100)
    ap.add_argument("--tag", default="on")
    ap.add_argument("--regime-det", action="store_true", dest="regime_det",
                    help="braccio OFF: --regime deterministico, che cambia SOLO SCUOTIMENTO "
                         "(True->False). Verificato confrontando TUTTI i globali del modulo.")
    ap.add_argument("--no-osserva", action="store_true", dest="no_osserva",
                    help="gira senza osservatore: serve al sigillo di byte-identita'.")
    ap.add_argument("--outdir", default=HERE)
    a = ap.parse_args()

    base = os.path.join(a.outdir, "_vuoto_%s_s%d" % (a.tag, a.seed))
    argv = ["soliton_simulator.py",
            "--batch", "--nmasse", "3", "--sep", "8",
            "--seed", str(a.seed), "--passi", str(a.passi),
            "--ogni", str(a.ogni), "--db-ogni", str(a.passi),
            "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto", "--chi-core",
            "--calore-scal", "--deparam-orologio", "--verlet",
            "--fork-su2", "--fork-su2-mem",
            "--csv", base + ".cond.csv", "--sync-db", base + ".pkl", "--db-cleanup"]
    if a.regime_det:
        argv += ["--regime", "deterministico"]

    os.chdir(ROOT)
    sys.path.insert(0, ROOT)
    sys.argv = argv
    import soliton_simulator as S

    arg = S._cli()
    S._applica_regime(arg)
    print("[osserva] tag=%s seed=%d passi=%d  SCUOTIMENTO=%s  FORK_SU2=%s FORK_SU2_MEM=%s"
          % (a.tag, a.seed, a.passi, S.SCUOTIMENTO, S.FORK_SU2, S.FORK_SU2_MEM), flush=True)

    righe = []
    stato = {"k": 0}
    orig_step = S.Rete.step

    def in_applica_flag():
        """_applica_flag gira 300 step di riscaldamento su un'ALTRA rete (quella interattiva
        globale): vanno ESCLUSI, altrimenti le misure mescolano due sistemi."""
        f = sys._getframe(2)
        for _ in range(7):
            if f is None:
                return False
            if f.f_code.co_name == "_applica_flag":
                return True
            f = f.f_back
        return False

    def misura(net, passo):
        """SOLO LETTURA degli array gia' committati. Nessuna scrittura, nessun rng, nessuna
        chiamata che ricalcoli campi (mai calcola_psi())."""
        n = int(net.n)
        nb = getattr(net, "_nb", None)
        psi = getattr(net, "psi", None)
        if nb is None or psi is None or len(nb) < n or len(psi) < n or n < 2 or not len(net.i):
            return
        nb = np.asarray(nb, float)[:n]
        I2 = np.abs(np.asarray(psi)[:n]) ** 2
        Lam = float(np.mean(I2))                      # = lambda_vuoto(net), scala di stato

        # ---- MISURA A: chi_ij = angolo fra i Bloch dei due estremi di ogni arco --------------
        ii, jj = net.i, net.j
        m = (ii < n) & (jj < n)
        ii, jj = ii[m], jj[m]
        cos_chi = np.clip(np.sum(nb[ii] * nb[jj], axis=1), -1.0, 1.0)
        chi = np.arccos(cos_chi)
        I2a = 0.5 * (I2[ii] + I2[jj])                 # densita' dell'ARCO (media dei due nodi)

        # ---- MISURA B: <n> = media vettoriale dei Bloch --------------------------------------
        r = {"passo": passo, "n": n, "n_archi": int(len(chi)), "Lam": Lam}
        p10, p90 = float(np.percentile(I2, 10)), float(np.percentile(I2, 90))

        regioni = (("tot", np.ones(n, bool), np.ones(len(chi), bool)),
                   ("mat", I2 > Lam, I2a > Lam),      # soglia = scala del vuoto (zero parametri)
                   ("vuo", I2 <= Lam, I2a <= Lam),
                   ("p90", I2 >= p90, I2a >= p90),    # robustezza: la lettura non deve dipendere
                   ("p10", I2 <= p10, I2a <= p10))    # dalla soglia scelta
        for nome, sel_n, sel_a in regioni:
            c = chi[sel_a]
            r["chi_%s_n" % nome] = int(c.size)
            if c.size:
                r["chi_%s_media" % nome] = float(np.mean(c))
                r["chi_%s_std" % nome] = float(np.std(c))
                r["chi_%s_mediana" % nome] = float(np.median(c))
                # frazioni vicino ai due poli degeneri (0 = allineati, pi = antipodali)
                r["chi_%s_fr_lt10g" % nome] = float(np.mean(c < np.radians(10.0)))
                r["chi_%s_fr_gt170g" % nome] = float(np.mean(c > np.radians(170.0)))
            else:
                for k in ("media", "std", "mediana", "fr_lt10g", "fr_gt170g"):
                    r["chi_%s_%s" % (nome, k)] = float("nan")
            v = nb[sel_n]
            r["nmed_%s_N" % nome] = int(v.shape[0])
            if v.shape[0]:
                mv = v.mean(axis=0)
                r["nmed_%s_x" % nome] = float(mv[0])
                r["nmed_%s_y" % nome] = float(mv[1])
                r["nmed_%s_z" % nome] = float(mv[2])
                r["nmed_%s_mod" % nome] = float(np.linalg.norm(mv))
                # riferimento statistico: per direzioni casuali |<n>| ~ 1/sqrt(N)
                r["nmed_%s_atteso" % nome] = float(1.0 / np.sqrt(max(v.shape[0], 1)))
                r["nmed_%s_sigma" % nome] = (float(np.linalg.norm(mv) * np.sqrt(v.shape[0])))
            else:
                for k in ("x", "y", "z", "mod", "atteso", "sigma"):
                    r["nmed_%s_%s" % (nome, k)] = float("nan")

        # ---- STABILITA' (gratis) -------------------------------------------------------------
        psp = getattr(net, "_psi_spinor", None)
        nbr = getattr(net, "_nb_ret", None)
        r["norma_psi_err"] = (float(np.max(np.abs(np.linalg.norm(np.asarray(psp)[:n], axis=1) - 1.0)))
                              if psp is not None and len(psp) >= n else float("nan"))
        r["norma_nret_err"] = (float(np.max(np.abs(np.linalg.norm(np.asarray(nbr)[:n], axis=1) - 1.0)))
                               if nbr is not None and len(nbr) >= n else float("nan"))
        r["nan_psi"] = int(not np.all(np.isfinite(np.asarray(psi)[:n])))
        r["max_pos"] = (float(np.max(np.abs(np.asarray(net.pos)[:n])))
                        if getattr(net, "pos", None) is not None and len(net.pos) >= n else float("nan"))
        righe.append(r)

    def spia(self):
        mio = not in_applica_flag()
        orig_step(self)
        if mio:
            stato["k"] += 1
            if stato["k"] == 1 or stato["k"] % a.ogni == 0:
                misura(self, stato["k"])

    if not a.no_osserva:
        S.Rete.step = spia
    S.batch_condensazione(arg)

    if not a.no_osserva and righe:
        cols = list(righe[0].keys())
        out = base + ".vuoto.csv"
        with open(out, "w", newline="") as f:
            wcsv = _csv.DictWriter(f, fieldnames=cols)
            wcsv.writeheader()
            for r in righe:
                wcsv.writerow(r)
        print("[osserva] %d campioni -> %s" % (len(righe), out), flush=True)


if __name__ == "__main__":
    main()
