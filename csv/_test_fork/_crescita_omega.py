# -*- coding: utf-8 -*-
"""FASE 1 (Gilbert/FDT) — COME CRESCE `omega_s`? Diffusivo o balistico? E qual e' la sorgente?

PERCHE' QUESTA SONDA
--------------------
La derivazione analitica di `doc/ANALISI_gilbert_fdt.md` distingue due regimi, che danno tempi di
crescita diversi di DUE ORDINI:
  DIFFUSIVO (direzione della coppia scorrelata a ogni passo):  |omega|(n) = |F| * dt * sqrt(n)
  BALISTICO (direzione coerente):                              |omega|(n) = |F| * dt * n
Con un solo campione di `|omega_s|` non si distinguono. Serve la TRAIETTORIA.
Misura anche `Lam` (energia del vuoto) e `amp` (ampiezza del rumore sul Bloch), che servono al
coefficiente di fluttuazione-dissipazione e che nessun calcolo puo' inventare.

PUREZZA
-------
Legge SOLO array di stato (`psi`, `omega_s`, `_nb`, `i`, `j`, `d`). `Lam` e' ricalcolata in locale
come `mean(|psi|^2)` — la stessa formula di `lambda_vuoto` — invece di chiamare quella funzione,
che invocherebbe `calcola_psi()` e muterebbe la cache. Non consuma `net.rng`.
"""
import argparse
import contextlib
import io
import os
import sys

import numpy as np

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--passi", type=int, default=150)
    ap.add_argument("--ogni", type=int, default=10)
    ap.add_argument("--seed", type=int, default=1)
    o = ap.parse_args()

    os.chdir(RADICE); sys.path.insert(0, RADICE)
    sys.argv = ["soliton_simulator.py", "--batch", "--nmasse", "3", "--sep", "8",
                "--passi", "1", "--ogni", "100000", "--db-ogni", "100000",
                "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto", "--chi-core",
                "--calore-scal", "--deparam-orologio", "--verlet", "--cs-dinamico",
                "--csv", os.path.join(os.environ.get("TMP", "."), "_crescita.csv")]
    import soliton_simulator as S
    a = S._cli(); S._applica_regime(a)
    with contextlib.redirect_stdout(io.StringIO()):
        S._applica_flag(a)

    net = S.Rete(o.seed); net.semina(80)
    def passo(r):
        S.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
    for _ in range(6):
        passo(net)
    Nc = S.massa_critica_collasso()
    for k in range(3):
        ang = 2 * np.pi * k / 3
        net.nuova_massa(int(Nc * 0.6), raggio=0.8,
                        centro=(8.0 * np.cos(ang), 8.0 * np.sin(ang), 0.0), fase=0.0)

    print("CALORE_VETTORIALE=%s  _CALORE_INIT=%.3g  TAU_A=%.3g  TAU_A_LOCALE=%s  DT=%.3g"
          % (S.CALORE_VETTORIALE, S._CALORE_INIT, S.TAU_A, S.TAU_A_LOCALE, S.DT))
    print("SCUOTIMENTO=%s  SYNC_UPDATE=%s  (il rumore sul Bloch vive a :1847 solo se SCUOTIMENTO e non SYNC)"
          % (S.SCUOTIMENTO, S.SYNC_UPDATE))
    print()
    print(" passo      n   |omega_s| med   theta med      Lam        amp med    inerzia med  tau/DT med")
    print(" " + "-" * 104)
    for t in range(1, o.passi + 1):
        passo(net)
        if t % o.ogni and t != 1:
            continue
        n = net.n
        om = np.linalg.norm(np.asarray(net.omega_s[:n], float), axis=1)
        psi = np.asarray(net.psi[:n])
        I2 = np.abs(psi) ** 2
        Lam = float(np.mean(I2))                      # = lambda_vuoto, ricalcolata in locale
        amp = np.sqrt(Lam) / (1.0 + I2 / max(Lam, 1e-300))
        rif = max(float(np.median(I2[I2 > 1e-6])), 1e-6) if np.any(I2 > 1e-6) else 1.0
        tau = S.TAU_A * np.maximum(I2 / rif, 0.05) if S.TAU_A_LOCALE else np.full(n, S.TAU_A)
        # |F| = |coppia|/inerzia, ricostruito dai soli array di stato
        rs = getattr(net, "rho_spin", None)
        rho = np.asarray(rs)[:n] if (rs is not None and len(rs) >= n) else I2
        inerzia = np.maximum(rho, 1e-6)
        # dt_n: il ritmo muterebbe _psi_prec, quindi si usa il tic nominale DT come riferimento
        theta = om * S.DT
        print(" %5d  %6d   %12.4g  %10.4g deg  %10.3g  %10.3g  %10.4g  %10.4g"
              % (t, n, float(np.median(om)), float(np.degrees(np.median(theta))),
                 Lam, float(np.median(amp)), float(np.median(inerzia)), float(np.median(tau) / S.DT)))
    print()
    print("LETTURA: |omega|(n) ~ n  -> BALISTICO (coppia coerente, cresce verso il punto fisso tau*F)")
    print("         |omega|(n) ~ sqrt(n) -> DIFFUSIVO (coppia scorrelata: e' un random walk smorzato)")
    print("         plateau            -> gia' all'equilibrio: la dissipazione esistente BASTA")


if __name__ == "__main__":
    main()
