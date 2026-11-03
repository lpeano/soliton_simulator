# -*- coding: utf-8 -*-
r"""**I TEST DELLA PARTENZA SIMMETRICA** *(`protetto.q_simmetrica`, `partenza_simmetrica`; Luca dopo `aad1435a` e `21:14`; il task history `2026-11-03_D0_ruotata_e_TS`, sez. 8-9)*.
### `S0` il vuoto ruotato: `R F3 = c_v F3` con `c_v = +-1` *(e `F0` registrato)*; `S1` `|S psi - c psi| / |psi|` sotto `TOLL` e `c = 1`; `S1-F` *(deve fallire)* la partenza di oggi;
`S2` la norma `N`; `S3` `q+` nella coppia *(Bloch)* e `P q+ = q+`; `S4` il tick VIVO commuta con `phi -> -phi` *(10 tick nella rampa dalla partenza `TS` su `F3`, 10 dopo dallo stato di
`TM1000` a `13333`)*; `S4-F` *(deve fallire)* con `phi -> 1.1 phi`.
"""
import os

import numpy as np

from . import protetto as P

TOLL = 1e-12                   # ### come carta_impulso.TOLL_UGUALE e carta_d0
N_TICK = 10                    # ### come carta_d0
T_STATO = 13333                # ### come carta_d0: il primo stato completo di TM1000 oltre K


def _corri(z, x, t0, K):
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    from . import accensione as AC
    for k, v in x.items():
        z["st"][k][...] = v
    with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
        for t in range(t0 + 1, t0 + N_TICK + 1):
            AC.tick(z, t, K)
    return {k: z["st"][k].copy() for k in x}


def _scarto(a, b):
    return max((float(np.linalg.norm(a[k] - b[k]) / np.linalg.norm(b[k])) if np.linalg.norm(b[k]) > 0 else float(np.linalg.norm(a[k] - b[k]))) for k in b)


def gira(esito):
    import _solitone_dal_fondo as SD
    import _vuoto_vivo_B as V
    from . import carta_impulso as CI
    from . import corsa_accensione as CA
    print("### LA PARTENZA SIMMETRICA (protetto.q_simmetrica, partenza_simmetrica): TOLL %g N_TICK %d T_STATO %d" % (TOLL, N_TICK, T_STATO))
    sol, vuoto, s = V.CORSE[CA.NOME]
    K = int(round(CA.CORSE["TP1000"][0] / s))
    with V.scena(s, vuoto, V.EPS) as (_rec, z, phi0, pK):
        inc, L = z["inc"], z["L"]
        chiavi = [k for k, v in z["st"].items() if isinstance(v, np.ndarray)]
        salvato = {k: z["st"][k].copy() for k in chiavi}
        q, ev, G = P.q_simmetrica(z, phi0, s, +1)
        m2 = P.centro_inversione(z, pK)
        p = P.partenza_simmetrica(z, pK, q, V.N, m2)
        p_oggi, _info = V.partenza(sol, z, phi0, pK, s)
        for k in chiavi:
            z["st"][k][...] = salvato[k]
        _ok, dd = CI.assi(inc, L)
        dove = CI.rotazione(inc, L, dd, m2)
        F3 = SD.fondo_con_fasi(inc, L, tuple(dict(SD.FASI)["F3"]))
        righe, ok0 = [], True
        for nv, ph in (("F0", phi0), ("F3", F3)):
            r = CI.applica(ph, dove)
            cv = complex(np.vdot(ph, r) / np.vdot(ph, ph))
            sc = float(np.linalg.norm(r - cv * ph) / np.linalg.norm(ph))
            righe.append("%s: c_v %+.12f %+.1ei, |R phi - c_v phi| / |phi| %.2e" % (nv, cv.real, cv.imag, sc))
            if nv == "F3":
                ok0 = sc <= TOLL and min(abs(cv - 1), abs(cv + 1)) <= TOLL
                cv3 = cv
        esito("DEVE PASSARE: S0 il vuoto F3 ruotato (attorno a %s / 2) e' +-F3 entro %g" % (m2, TOLL), ok0, "; ".join(righe))
        rp = CI.applica(p, dove, P.SIGMA_Z)
        c = complex(np.vdot(p, rp) / np.vdot(p, p))
        a1 = float(np.linalg.norm(rp - c * p) / np.linalg.norm(p))
        esito("DEVE PASSARE: S1 la partenza simmetrica: |R psi - c psi| / |psi| entro %g e c = 1 entro %g" % (TOLL, TOLL), a1 <= TOLL and abs(c - 1) <= TOLL,
              "%.3e, c %+.15f %+.1ei; m2 %s" % (a1, c.real, c.imag, m2))
        ro = CI.applica(p_oggi, dove, P.SIGMA_Z)
        co = complex(np.vdot(p_oggi, ro) / np.vdot(p_oggi, p_oggi))
        ao = float(np.linalg.norm(ro - co * p_oggi) / np.linalg.norm(p_oggi))
        esito("DEVE FALLIRE: S1-F la partenza DI OGGI (V.partenza) e' simmetrica entro %g" % TOLL, not ao <= TOLL, "%.3e" % ao)
        nn = float(np.sum(np.abs(p) ** 2))
        esito("DEVE PASSARE: S2 la norma della partenza simmetrica e' N = %g entro %g relativo" % (V.N, TOLL), abs(nn / V.N - 1.0) <= TOLL, "%.3e" % abs(nn / V.N - 1.0))
        lam = complex(np.vdot(q, G @ q))
        bl = float(np.linalg.norm(G @ q - lam * q))
        pq = float(np.linalg.norm(P.matrice_P(P.SIGMA_Z) @ q - q))
        esito("DEVE PASSARE: S3 q+ e' nella coppia (|G q - <G> q| entro %g) e P q+ = q+ (entro %g)" % (TOLL, TOLL), bl <= TOLL and pq <= TOLL and abs(ev - 1) <= TOLL,
              "Bloch %.2e, |P q - q| %.2e, l'autovalore %+.15f" % (bl, pq, ev))
        x0 = dict(salvato)
        x0["psi_h"] = p.copy()
        x0["phi_h"] = F3.copy()
        with np.load(os.path.join(CA.base_e("TM1000"), "stati", "TM1000", "TM1000_stato_%06d.npz" % T_STATO)) as d:
            x1 = {k: d[k].copy() for k in chiavi}
        peggio, peggio_f = 0.0, 0.0
        for x, t0 in ((x0, 0), (x1, T_STATO)):
            a = _corri(z, x, t0, K)
            xm = dict(x)
            xm["phi_h"] = -x["phi_h"]
            b = _corri(z, xm, t0, K)
            am = dict(a)
            am["phi_h"] = -a["phi_h"]
            peggio = max(peggio, _scarto(b, am))
            xf = dict(x)
            xf["phi_h"] = 1.1 * x["phi_h"]
            bf = _corri(z, xf, t0, K)
            af = dict(a)
            af["phi_h"] = 1.1 * a["phi_h"]
            peggio_f = max(peggio_f, _scarto(bf, af))
        for k in chiavi:
            z["st"][k][...] = salvato[k]
    esito("DEVE PASSARE: S4 il tick VIVO commuta con phi -> -phi (%d tick nella rampa da TS su F3 e %d dopo da TM1000 a %d), ogni chiave entro %g" % (N_TICK, N_TICK, T_STATO, TOLL),
          peggio <= TOLL, "il peggiore %.3e (c_v di F3 %+.3f: %s)" % (peggio, cv3.real, "S4 necessario" if cv3.real < 0 else "S4 un controllo in piu'"))
    esito("DEVE FALLIRE: S4-F lo stesso con phi -> 1.1 phi", not peggio_f <= TOLL, "il peggiore %.3e" % peggio_f)
