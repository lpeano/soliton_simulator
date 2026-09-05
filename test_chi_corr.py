"""PRIMO TEST (chiralita' di gruppo / lignaggio) — vedi memoria repo ripresa_chiralita_gruppo.md.

Decide se la chiralita' EREDITATA (perc_chi: casuale alla nascita, ereditata alla mitosi)
forma DOMINI COERENTI sulla topologia. Misura <chi_i*chi_j> sugli archi validi.

METRICHE DI DECISIONE:
  - cc_mean   = <chi_i*chi_j> sugli archi (>0 = domini coerenti di lignaggio)
  - sigma     = cc_mean*sqrt(n_archi)  (significativita' NAIVE: assume archi indipendenti,
                falsata su topologia condivisa -> tenuta solo come riferimento)
  - frac_pos  = frazione archi con cc>0 (0.5 = casuale)
  - z_perm    = z-score ROBUSTO da permutazione delle etichette chi a TOPOLOGIA FISSA:
                risponde a "la correlazione osservata supera quella attesa se chi fosse
                assegnata a caso ai nodi?". E' la metrica che DECIDE.

VERDETTO: z_perm >~ 2-3 coerente su tutti i semi -> chiralita' di gruppo REALE (lignaggi).
          z_perm ~ 0 -> pista morta.
NB: 400 passi = solo FORMAZIONE. Risultato PRELIMINARE (vedi CLAUDE.md, no conclusioni <2000).
"""
import numpy as np
import soliton_simulator as ss

SEME_INIZIALE = 80
PASSI = 400
SEMI = [1, 2, 3]
N_PERM = 500

ss.SPINORE_VIVO = True
ss.SPIN_LARMOR = False


def evolvi_e_misura(seed):
    net = ss.Rete(seed)
    net.semina(SEME_INIZIALE)
    for _ in range(PASSI):
        net.step()
        net.mitosi()
        net.rilassa_disegno()
        net.memoria_hebbiana_moto()
    n = net.n
    i = np.asarray(net.i); j = np.asarray(net.j)
    m = (i < n) & (j < n)
    ii, jj = i[m], j[m]
    chi = np.asarray(net.perc_chi[:n], dtype=float)
    cc = chi[ii] * chi[jj]
    n_arcs = len(cc)
    cc_mean = float(cc.mean()) if n_arcs else 0.0
    sigma_naive = cc_mean * np.sqrt(n_arcs) if n_arcs else 0.0
    frac_pos = float((cc > 0).mean()) if n_arcs else 0.0
    # Controllo permutazione: rimescolo chi sui nodi tenendo FISSA la topologia.
    rng = np.random.default_rng(1234 + seed)
    perm = np.empty(N_PERM)
    for k in range(N_PERM):
        chp = rng.permutation(chi)
        perm[k] = (chp[ii] * chp[jj]).mean() if n_arcs else 0.0
    pm, ps = float(perm.mean()), float(perm.std())
    z = (cc_mean - pm) / ps if ps > 1e-12 else 0.0
    return dict(seed=seed, n=n, n_arcs=n_arcs, cc_mean=cc_mean, sigma=sigma_naive,
                frac_pos=frac_pos, perm_mean=pm, perm_std=ps, z=z)


if __name__ == "__main__":
    print(f"# PRIMO TEST — chiralita' di gruppo <chi_i*chi_j> | passi={PASSI} "
          f"semi={SEMI} n_perm={N_PERM} spinore_vivo={ss.SPINORE_VIVO}")
    print(f"# {'seed':>4} {'n':>5} {'archi':>7} {'cc_mean':>9} {'sigma':>8} "
          f"{'frac>0':>7} {'perm_mu':>9} {'perm_sd':>8} {'z_perm':>7}")
    zs = []
    for s in SEMI:
        r = evolvi_e_misura(s)
        zs.append(r['z'])
        print(f"  {r['seed']:>4d} {r['n']:>5d} {r['n_arcs']:>7d} {r['cc_mean']:>9.4f} "
              f"{r['sigma']:>8.2f} {r['frac_pos']:>7.3f} {r['perm_mean']:>9.4f} "
              f"{r['perm_std']:>8.4f} {r['z']:>7.2f}")
    zs = np.array(zs)
    verdetto = ("chiralita' di GRUPPO reale" if np.all(zs > 2.0)
                else "PISTA MORTA (nessuna struttura)" if np.all(np.abs(zs) < 2.0)
                else "AMBIGUO (semi discordi)")
    print(f"# VERDETTO [PRELIMINARE, 400 passi]: z_perm medio = {zs.mean():.2f} -> {verdetto}")
