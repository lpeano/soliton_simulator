"""Test del lift spinoriale e del feedback locale sugli archi."""
import numpy as np
import soliton_simulator as sim


def test_lift_due_pi(npassi=360):
    """Un giro del Bloch deve chiudere il lift con segno meno."""
    net = sim.Rete(0)
    net.phi = np.zeros(1)
    riferimento = None
    for t in np.linspace(0.0, 2.0 * np.pi, npassi + 1):
        net._nb = np.array([[np.cos(t), np.sin(t), 0.0]], float)
        net._aggiorna_lift_spinoriale()
        if riferimento is None:
            riferimento = net._spinor_lift[0].copy()
    residuo = np.vdot(riferimento, net._spinor_lift[0])
    print(f"test_lift_2pi_overlap={residuo.real:.6g}{residuo.imag:+.6g}j "
          f"atteso=-1 segno={'OK' if residuo.real < -0.9 else 'FALLITO'}")


def olonomia_endpoint(net, ciclo):
    chi = net.perc_chi
    prodotto = 1
    for e, _verso in ciclo:
        i, j = int(net.i[e]), int(net.j[e])
        prodotto *= int(chi[i]) * int(chi[j])
    return int(prodotto)


def olonomia_da_perc_tw(net, ciclo):
    tw = np.rint(net.perc_tw / np.pi).astype(int) & 1
    hol = 1
    attraversamenti = 0
    for e, _verso in ciclo:
        i, j = int(net.i[e]), int(net.j[e])
        if (tw[i] ^ tw[j]) != 0:
            hol *= -1
            attraversamenti += 1
    return hol, attraversamenti


def olonomia_mobius_candidato(ciclo):
    """Controtest: applicare -sigma_x a ogni arco misura solo la parita'."""
    transizione = np.array([[0, -1], [-1, 0]], dtype=int)
    hol = np.eye(2, dtype=int)
    for _e, _verso in ciclo:
        hol = hol @ transizione
    return hol


def esegui(seed=1, passi=400, feedback=False):
    sim.SPINORE_VIVO = True
    sim.SPIN_FEEDBACK = feedback
    net = sim.Rete(seed)
    net.semina(sim.SEME_INIZIALE)
    for _ in range(passi):
        sim.scuoti_vuoto(net)
        net.step()
        net.mitosi()
        net.rilassa_disegno()
        net.memoria_hebbiana_moto()

    cicli = net._base_cicli_topologici()
    valori = np.array([olonomia_endpoint(net, c) for c in cicli], dtype=int)
    matrici = [olonomia_mobius_candidato(c) for c in cicli]
    tw_olonomie = [olonomia_da_perc_tw(net, c) for c in cicli]
    lift = np.array([net.olonomia_lift_ciclo(c) for c in cicli], dtype=complex)
    n_pari = sum(len(c) % 2 == 0 for c in cicli)
    n_dispari = len(cicli) - n_pari
    n_meno_identita = sum(np.array_equal(m, -np.eye(2, dtype=int)) for m in matrici)
    n_cuciture = sum(a > 0 for _h, a in tw_olonomie)
    n_hol_meno = sum(h == -1 for h, _a in tw_olonomie)
    n_attraversamenti = sum(a for _h, a in tw_olonomie)
    chi = net.perc_chi[:net.n]
    validi = (net.i < net.n) & (net.j < net.n)
    prodotti = chi[net.i[validi]] * chi[net.j[validi]]

    print(f"seed={seed} passi={passi} feedback={feedback} nodi={net.n} "
          f"archi={int(validi.sum())} cicli={len(cicli)}")
    print(f"chi_media={float(np.mean(chi)):.6g} chi_frazione_positiva={float(np.mean(chi > 0)):.6g}")
    print(f"archi_chi_prod_mean={float(np.mean(prodotti)):.6g}")
    print(f"olonomia_endpoint_unici={sorted(set(valori.tolist())) if len(valori) else []}")
    print(f"cicli_pari={n_pari} cicli_dispari={n_dispari} "
          f"candidato_Tm_hol=-I={n_meno_identita}/{len(cicli)}")
    print(f"perc_tw_nonzero={int(np.count_nonzero(np.rint(net.perc_tw / np.pi)))} "
          f"cicli_con_cucitura={n_cuciture}/{len(cicli)} "
          f"attraversamenti={n_attraversamenti} hol_Z2=-1={n_hol_meno}/{len(cicli)}")
    print(f"lift_cicli_validi={int(np.count_nonzero(np.abs(lift) > 1e-12))} "
          f"lift_fase_media={float(np.mean(np.angle(lift))) if len(lift) else 0.0:.6g} "
          f"lift_fase_abs_media={float(np.mean(np.abs(np.angle(lift)))) if len(lift) else 0.0:.6g}")
    print(f"feedback_arco_ampiezza_ultima={getattr(net, '_spin_feedback_last', 0.0):.6g}")


if __name__ == "__main__":
    test_lift_due_pi()
    for feedback in (False, True):
        for seme in (1, 2):
            esegui(seme, feedback=feedback)
