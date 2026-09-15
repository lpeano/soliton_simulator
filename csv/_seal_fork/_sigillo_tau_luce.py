# -*- coding: utf-8 -*-
"""SIGILLO di `--tau-luce` (FASE 2) — T1..T5.

T1  flag OFF byte-identico al file PRIMA della modifica (copre ANCHE l'estrazione di
    `_tempo_luce_nodo` da `_bloch_ritardato`: se il refactor avesse cambiato una virgola, T1 cade).
T2  riduzione al limite: `tau` forzato al valore vecchio -> torna ESATTAMENTE al ramo OFF.
T3  la PENDENZA di theta contro l'inerzia con ON, con SE, r^2 e IC95.
T4  SIGILLO DI COVARIANZA: e' una LEGGE o un numero? Si cambia una grandezza a monte e si verifica
    che `tau` la segua DA SOLO. Se resta fermo, e' un numero con una formula intorno.
T5  ampiezza e stabilita': |omega| e theta ON vs OFF, niente NaN, |nb| = 1.
"""
import contextlib, importlib.util, io, os, sys
import numpy as np

RAD = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(RAD); sys.path.insert(0, RAD)
ARGS = ["--batch", "--nmasse", "3", "--sep", "8", "--passi", "1", "--ogni", "100000",
        "--db-ogni", "100000", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
        "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--cs-dinamico",
        "--fork-su2", "--fork-su2-mem", "--csv", os.path.join(os.environ.get("TMP", "."), "_sig.csv")]
CAMPI = ("pos", "phi", "phi0", "phivel", "eta", "d", "d0", "vd", "peq", "tw", "twp", "i", "j",
         "perc_chi", "perc_tw", "_nb", "_nb_prec", "_nb_ret", "_psi_spinor", "omega_s", "psi")


def carica(percorso, nome, extra=()):
    spec = importlib.util.spec_from_file_location(nome, percorso)
    M = importlib.util.module_from_spec(spec); sys.modules[nome] = M
    sys.argv = ["soliton_simulator.py"] + ARGS + list(extra)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(M)
        a = M._cli(); M._applica_regime(a); M._applica_flag(a)
    return M


def scena(M, seed):
    net = M.Rete(seed); net.semina(80)
    for _ in range(6):
        passo(M, net)
    Nc = M.massa_critica_collasso()
    for k in range(3):
        ang = 2 * np.pi * k / 3
        net.nuova_massa(int(Nc * 0.6), raggio=0.8,
                        centro=(8.0 * np.cos(ang), 8.0 * np.sin(ang), 0.0), fase=0.0)
    return net


def passo(M, net):
    M.scuoti_vuoto(net); net.step(); net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()


def evolvi(M, seed, n):
    net = scena(M, seed)
    for _ in range(n):
        passo(M, net)
    return net


def confronta(a, b, eti):
    print("  PRESIDIO: uno zero con N DIVERSO e' MANCANZA DI CONFRONTO, non identita'.")
    print("    n_A = %d   n_B = %d   ->  %s" % (a.n, b.n, "CONFRONTABILI" if a.n == b.n else "NON CONFRONTABILI"))
    if a.n != b.n:
        return False
    ok = True; peggio = 0.0
    for c in CAMPI:
        va, vb = getattr(a, c, None), getattr(b, c, None)
        if va is None or vb is None:
            continue
        va, vb = np.asarray(va), np.asarray(vb)
        if va.shape != vb.shape:
            print("    %-14s SHAPE diversa -> FAIL" % c); ok = False; continue
        d = float(np.max(np.abs(va.astype(complex) - vb.astype(complex)))) if va.size else 0.0
        peggio = max(peggio, d)
        if d != 0.0:
            ok = False; print("    %-14s max|A-B| = %.3e  FAIL" % (c, d))
    rng = (a.rng.bit_generator.state == b.rng.bit_generator.state)
    print("    %d campi confrontati, PEGGIOR max|A-B| = %.3e   stato RNG %s"
          % (len(CAMPI), peggio, "identico" if rng else "DIVERSO"))
    ok = ok and rng
    print("  %s: %s" % (eti, "PASS" if ok else "FAIL"))
    return ok


def pend_se(x, y):
    ok = np.isfinite(x) & np.isfinite(y) & (x > 0) & (y > 0)
    lx, ly = np.log(x[ok]), np.log(y[ok])
    b = float(np.polyfit(lx, ly, 1)[0]); r = float(np.corrcoef(lx, ly)[0, 1]); n = int(ok.sum())
    se = abs(b / r) * np.sqrt((1 - r * r) / (n - 2))
    return b, se, r * r, n


def main():
    SEED, PASSI = 1, 25
    esiti = {}
    print("=" * 104)
    print("T1 - flag OFF byte-identico al file PRIMA della modifica (copre anche l'ESTRAZIONE)")
    print("=" * 104)
    vecchio = carica(os.path.join("csv", "_seal_fork", "_old_sim_pre_tauluce.py"), "sim_vecchio")
    nuovo_off = carica("soliton_simulator.py", "sim_off")
    print("  TAU_LUCE nel modulo nuovo (deve essere False): %s" % nuovo_off.TAU_LUCE)
    esiti["T1"] = confronta(evolvi(vecchio, SEED, PASSI), evolvi(nuovo_off, SEED, PASSI), "T1")

    print()
    print("=" * 104)
    print("T2 - riduzione al limite: tau forzato al valore VECCHIO -> deve tornare al ramo OFF")
    print("=" * 104)
    M = carica("soliton_simulator.py", "sim_lim", ["--tau-luce"])
    print("  TAU_LUCE (deve essere True): %s" % M.TAU_LUCE)

    def tau_vecchio(self, ii, jj):
        n = self.n
        dens = np.abs(self.psi[:n]) ** 2
        rif = max(float(np.median(dens[dens > 1e-6])), 1e-6) if np.any(dens > 1e-6) else 1.0
        return M.TAU_A * np.maximum(dens / rif, 0.05)
    M.Rete._tempo_luce_nodo = tau_vecchio          # forza la legge al valore vecchio
    print("  `_tempo_luce_nodo` forzato a restituire TAU_A*max(dens/dens_rif, 0.05)")
    esiti["T2"] = confronta(evolvi(nuovo_off, SEED, PASSI), evolvi(M, SEED, PASSI), "T2")

    print()
    print("=" * 104)
    print("T3 - LA PENDENZA di theta contro l'inerzia, con SE / r^2 / IC95 (mai una pendenza nuda)")
    print("=" * 104)
    M_on = carica("soliton_simulator.py", "sim_on", ["--tau-luce"])
    ris = {}
    for eti, Mx in (("OFF", nuovo_off), ("ON ", M_on)):
        net = evolvi(Mx, SEED, 300)
        n = net.n
        rs = getattr(net, "rho_spin", None)
        rho = np.asarray(rs)[:n] if (rs is not None and len(rs) >= n) else np.abs(np.asarray(net.psi[:n])) ** 2
        inz = np.maximum(rho, 1e-6)
        om = np.linalg.norm(np.asarray(net.omega_s[:n], float), axis=1)
        th = np.degrees(om * Mx.DT)
        v = rho > 1.0000001e-6
        b, se, r2, nn = pend_se(inz[v], th[v])
        ris[eti.strip()] = (b, se, r2, nn, float(np.median(om)), float(np.median(th)), n)
        print("  %s  pendenza %+.4f +- %.4f   r^2 %.3f   n %d   IC95 [%+.4f, %+.4f]"
              % (eti, b, se, r2, nn, b - 1.96 * se, b + 1.96 * se))
    attesa = -1.078 + 0.097 / 2
    bo, seo = ris["ON"][0], ris["ON"][1]
    print("  attesa dalla FASE 1: %+.3f    misurata ON: %+.4f +- %.4f   z dalla attesa: %.2f"
          % (attesa, bo, seo, abs(bo - attesa) / seo))
    bf = ris["OFF"][0]
    esiti["T3"] = bool(bo < bf - 0.3)
    print("  T3 (la pendenza si ALLONTANA da zero rispetto a OFF, di almeno 0.3): %s"
          % ("PASS" if esiti["T3"] else "FAIL"))

    print()
    print("=" * 104)
    print("T4 - SIGILLO DI COVARIANZA: e' una LEGGE o un numero travestito?")
    print("=" * 104)
    net = evolvi(M_on, SEED, 60)
    ii, jj = net.i, net.j
    t0 = M_on.Rete._tempo_luce_nodo(net, ii, jj).copy()
    d0 = net.d.copy()
    net.d = d0 * 2.0
    t_d = M_on.Rete._tempo_luce_nodo(net, ii, jj).copy()
    net.d = d0
    csp = getattr(net, "_cs_nodo_prev", None)
    if csp is not None:
        c0 = np.asarray(csp, float).copy(); net._cs_nodo_prev = c0 * 2.0
        t_c = M_on.Rete._tempo_luce_nodo(net, ii, jj).copy(); net._cs_nodo_prev = c0
    else:
        t_c = None
    r_d = float(np.median(t_d / np.maximum(t0, 1e-300)))
    print("  d -> 2d   : tau_nuovo/tau_vecchio = %.6f   (atteso 2.000000)" % r_d)
    ok4 = abs(r_d - 2.0) < 1e-6
    if t_c is not None:
        r_c = float(np.median(t_c / np.maximum(t0, 1e-300)))
        print("  cs -> 2cs : tau_nuovo/tau_vecchio = %.6f   (atteso 0.500000)" % r_c)
        ok4 = ok4 and abs(r_c - 0.5) < 1e-6
    # il CONTRASTO: la legge VECCHIA non segue la geometria, perche' non e' una legge sulla geometria
    dens = np.abs(net.psi[:net.n]) ** 2
    rif = max(float(np.median(dens[dens > 1e-6])), 1e-6) if np.any(dens > 1e-6) else 1.0
    tv0 = M_on.TAU_A * np.maximum(dens / rif, 0.05)
    net.d = d0 * 2.0
    dens2 = np.abs(net.psi[:net.n]) ** 2
    rif2 = max(float(np.median(dens2[dens2 > 1e-6])), 1e-6) if np.any(dens2 > 1e-6) else 1.0
    tv1 = M_on.TAU_A * np.maximum(dens2 / rif2, 0.05)
    net.d = d0
    print("  CONTRASTO - la legge VECCHIA con d -> 2d: rapporto = %.6f  (resta FERMA: non e' una"
          % float(np.median(tv1 / np.maximum(tv0, 1e-300))))
    print("              legge sulla geometria, e questo e' esattamente il punto)")
    esiti["T4"] = ok4
    print("  T4: %s" % ("PASS - tau SEGUE lo stato da solo: e' una LEGGE" if ok4 else "FAIL - tau non segue: e' un NUMERO"))

    print()
    print("=" * 104)
    print("T5 - ampiezza e stabilita'")
    print("=" * 104)
    for eti in ("OFF", "ON"):
        b, se, r2, nn, omm, thm, n = ris[eti]
        print("  %-3s  |omega| mediana %10.4g   theta %10.4g gradi/passo = %7.2f giri   n=%d"
              % (eti, omm, thm, thm / 360.0, n))
    fatt = ris["ON"][5] / max(ris["OFF"][5], 1e-300)
    print("  fattore su theta: %.4f   (atteso ~1/13 = 0.077 dal rapporto sqrt(tau))" % fatt)
    net_on = evolvi(M_on, SEED, 60)
    nb = np.asarray(net_on._nb[:net_on.n], float)
    nrm = np.linalg.norm(nb, axis=1)
    nan = int(np.sum(~np.isfinite(nb))) + int(np.sum(~np.isfinite(net_on.psi[:net_on.n])))
    print("  |nb| max scostamento da 1: %.3e    NaN/inf: %d" % (float(np.max(np.abs(nrm - 1.0))), nan))
    esiti["T5"] = (nan == 0) and float(np.max(np.abs(nrm - 1.0))) < 1e-9
    print("  T5: %s" % ("PASS" if esiti["T5"] else "FAIL"))

    print()
    print("=" * 104)
    print("ESITO: " + "   ".join("%s=%s" % (k, "PASS" if v else "FAIL") for k, v in esiti.items()))
    print("SIGILLO COMPLESSIVO: %s" % ("PASS" if all(esiti.values()) else "FAIL"))
    print("=" * 104)
    return 0 if all(esiti.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
