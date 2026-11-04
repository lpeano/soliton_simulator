# -*- coding: utf-8 -*-
r"""**IL TEST DEL BORDO: LA RIFLESSIONE DI UN PACCHETTO IN BANDA `B`** *(Luca `2026-11-03` `21:52`; il task history `doc/TASK_HISTORY/2026-11-03_TB3_bordo_assorbente.md`, sez. 1 e 5.9)*
    python csv/solitone/carta_bordo.py > doc/referti_l2/bordo_riflessione.txt
### **Il protocollo** *(dichiarato nel task history PRIMA dei numeri)*: la scena di `TB3` *(`V.scena`, il vuoto `F3`)*, **senza solitone**; il vuoto gira come il tick lo fa girare *(`phi0(n) = e^{i omega n} F3`,
`omega` dalla tabella di `carta_fase`)*; il tick INTERO *(`AC.tick` dopo la rampa)*; **il pacchetto:** l'autovettore di banda `B` di `A(k)` *(`DV.matrice` sul vuoto `F3`)* al `k` della griglia con la velocita' di
gruppo piu' grande *(su entrambe le bande del gruppo)*, per un inviluppo gaussiano largo `W` centrato a `R0 = R_A - 3 W` dal centro del bordo lungo la velocita' di gruppo; `|psi|^2 = N_PAC`.
### **La misura:** `M_in(t)` la materia a `r < R_A - W`; `t_min` il tempo del minimo di `M_in` nella corsa senza bordo *(`g_max = 0`)* entro `L / v_g`; **la riflessione** `R(g) = max M_in(t) / M0` per `t` in
`[t_min, T]`, `T = 2 L / v_g` *(conservativa: la coda dispersiva conta come riflessione)*. ### **I DEVE:** `R0-F` *(deve fallire)* senza bordo `R < SOGLIA` *(il pacchetto rientra dal toro)*; `RB` il piu' piccolo
`g_max` della griglia con `R < SOGLIA` esiste *(se no: FERMO)*; `RB-M` il bilancio `M` dentro + assorbita = `M0` entro `1e-10` per ogni `g_max`.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

GRIGLIA = (0.0, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1)   # ### il task history sez. 1 (lo 0 e' il controllo)
SOGLIA = 1e-2                  # ### Luca 21:52: la riflessione sotto 1e-2
W = 4.0                        # ### protocollo (sez. 5.9): la larghezza dell'inviluppo, nodi
N_PAC = 1.0                    # ### protocollo: |psi|^2 del pacchetto (il solitone ha 1e6: il regime lineare)
TOLL_M = 1e-10                 # ### Luca 21:52: il bilancio

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-120s %s   %s" % (che[:120], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def velocita(ph, s, L):
    """### **La velocita' di gruppo** `grad_k omega`, `omega = fase per tick / s`, per banda e per `k` della griglia *(differenze centrali, la fase avvolta)*: `(L, L, 12, 2)` in nodi per unita' di tempo."""
    import _solitoni_triangoli as STR
    A = np.array([STR.A1, STR.A2])
    B = 2.0 * np.pi * np.linalg.inv(A).T
    d1 = np.angle(np.exp(1j * (np.roll(ph, -1, axis=0) - np.roll(ph, 1, axis=0)))) / (2.0 * s)
    d2 = np.angle(np.exp(1j * (np.roll(ph, -1, axis=1) - np.roll(ph, 1, axis=1)))) / (2.0 * s)
    M = np.linalg.inv(B / L)
    return np.einsum("ij,...j->...i", M, np.stack([d1, d2], axis=-1))


def main(argv):
    del argv
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_dal_fondo as SD
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import bordo as BO
    from solitone import campo as CP
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    for m in ("__init__", "accensione", "bordo", "campo", "corsa_accensione", "toro"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    _sol, vuoto, s = V.CORSE[CA.NOME]
    K = int(round(CA.CORSE["TF3"][0] / s))
    with np.load(os.path.join(CA.DIR_NPZ, "fase_F3.npz")) as d:
        omega = float(d["omega"])
    print("=" * 130)
    print("IL TEST DEL BORDO (Luca 21:52): la riflessione di un pacchetto in banda B sul vuoto F3; %s (s %g, eps %g); R_A %g W %g N_PAC %g SOGLIA %g GRIGLIA %s; omega %.17e (fase_F3.npz)"
          % (CA.NOME, s, V.EPS, BO.R_A, W, N_PAC, SOGLIA, GRIGLIA, omega))
    print("=" * 130)
    with V.scena(s, vuoto, V.EPS) as (_rec, z, _phi0, _pK):
        inc, L = z["inc"], z["L"]
        m1, m2 = np.asarray(z["m1"]), np.asarray(z["m2"])
        F3 = SD.fondo_con_fasi(inc, L, tuple(dict(SD.FASI)["F3"]))
        chiavi = [k for k, v in z["st"].items() if isinstance(v, np.ndarray)]
        salvato = {k: z["st"][k].copy() for k in chiavi}
        ph, Z = DV.autovettori(DV.matrice(z, F3, DV.AMP))
        for k in chiavi:
            z["st"][k][...] = salvato[k]
        vg = velocita(ph, s, L)
        idx = list(dict(DV.GRUPPI)["B"])
        mod = np.hypot(vg[..., idx, 0], vg[..., idx, 1])
        i1, i2, ib = np.unravel_index(int(np.argmax(mod)), mod.shape)
        b = idx[ib]
        v = vg[i1, i2, b]
        u = v / np.hypot(*v)
        vmod = float(np.hypot(*v))
        print("### IL PACCHETTO: k della griglia (%d, %d), la banda %d del gruppo B; la velocita' di gruppo (%+.5f, %+.5f), |v_g| %.5f nodi per unita' di tempo" % (i1, i2, b, v[0], v[1], vmod))
        c1 = c2 = L // 2
        R0 = BO.R_A - 3.0 * W
        A1, A2 = TO.vettori()
        Ai = np.linalg.inv(np.array([A1, A2]).T)
        e = Ai @ (R0 * u)
        p1, p2 = int(round(c1 + e[0])), int(round(c2 + e[1]))
        _kk, rp = CP.anelli(m1, m2, p1, p2, L, float("inf"))
        _kk, rc = CP.anelli(m1, m2, c1, c2, L, float("inf"))
        R0v = float(rc[p1 * L + p2])
        fase = np.exp(2j * np.pi * (i1 * m1 + i2 * m2) / L)
        cel = np.exp(-0.5 * (rp / W) ** 2)[:, None] * fase[:, None] * Z[i1, i2, :, b][None, :]
        cel *= math.sqrt(N_PAC / float(np.sum(np.abs(cel) ** 2)))
        psi0 = cel.reshape(z["st"]["psi_h"].shape)
        dentro = rc < BO.R_A - W
        print("  il centro del bordo (%d, %d); il centro del pacchetto (%d, %d) a R0 %.3f (atteso R_A - 3 W = %g); M_in a t 0: %.6f" % (c1, c2, p1, p2, R0v, R0, float(np.sum(np.abs(cel[dentro]) ** 2)) / N_PAC))
        T = int(math.ceil(2.0 * L / vmod / s))
        t_cerca = int(math.ceil(L / vmod / s))
        print("  T %d tick (2 L / v_g); il minimo di M_in senza bordo cercato entro %d tick (L / v_g)" % (T, t_cerca))
        R, t_min, mins = {}, None, None
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            for g_max in GRIGLIA:
                for k in chiavi:
                    z["st"][k][...] = salvato[k]
                z["st"]["psi_h"][...] = psi0
                z["st"]["phi_h"][...] = F3
                g_e, _gn, _r = BO.g_estremita(z, c1, c2, BO.R_A, g_max)
                M0 = float(np.sum(np.abs(z["st"]["psi_h"]) ** 2))
                Mass, serie, cen = 0.0, [], []
                for n in range(1, T + 1):
                    AC.tick(z, K + n, K)
                    if g_max > 0.0:
                        dM, _dV = BO.assorbi(z["st"], g_e, np.exp(1j * omega * n) * F3)
                        Mass += dM
                    rho = np.zeros(inc.n)
                    np.add.at(rho, inc.nodo, np.sum(np.abs(z["st"]["psi_h"]) ** 2, axis=1))
                    serie.append(float(rho[dentro].sum()) / M0)
                    if g_max == 0.0 and n * s <= R0 / vmod:
                        cen.append((n * s, float(np.sum(rho * rc)) / float(rho.sum())))
                serie = np.array(serie)
                M1 = float(np.sum(np.abs(z["st"]["psi_h"]) ** 2))
                if g_max == 0.0:
                    print("  ### senza bordo, a T: |phi - e^{i omega T} F3| / |F3| %.3e (il vuoto di riferimento del test: il tick intero da F3, senza rampa)"
                          % (float(np.linalg.norm(z["st"]["phi_h"] - np.exp(1j * omega * T) * F3)) / float(np.linalg.norm(F3))))
                    t_min = int(np.argmin(serie[:t_cerca])) + 1
                    mins = float(serie[t_min - 1])
                    if len(cen) > 2:
                        pv = np.polyfit([c[0] for c in cen], [c[1] for c in cen], 1)[0]
                        print("  ### senza bordo: la distanza media della materia dal centro cresce di %.5f nodi per unita' di tempo nel primo tratto (|v_g| atteso %.5f)" % (pv, vmod))
                    print("  ### senza bordo: il minimo di M_in a t %d tick (%.1f), M_in %.3e" % (t_min, t_min * s, mins))
                R[g_max] = float(serie[t_min - 1:].max())
                bil = abs((M1 + Mass) / M0 - 1.0)
                print("    g_max %-7g: R %.3e (il massimo di M_in dopo t_min); M finale %.3e; assorbita %.6f; il bilancio %.2e" % (g_max, R[g_max], M1 / M0, Mass / M0, bil))
                if g_max > 0.0:
                    esito("DEVE PASSARE: RB-M g_max %g il bilancio M + assorbita = M0 entro %g" % (g_max, TOLL_M), bil <= TOLL_M, "%.2e" % bil)
        for k in chiavi:
            z["st"][k][...] = salvato[k]
    esito("DEVE FALLIRE: R0-F senza bordo R < %g (il pacchetto rientra dal toro)" % SOGLIA, not R[0.0] < SOGLIA, "R %.3e" % R[0.0])
    sotto = [g for g in GRIGLIA if g > 0.0 and R[g] < SOGLIA]
    esito("DEVE PASSARE: RB un g_max della griglia con R < %g (il piu' piccolo e' quello della corsa)" % SOGLIA, bool(sotto), "il piu' piccolo: %s" % (sotto[0] if sotto else "nessuno: FERMO"))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s; G_MAX %s" % (OK[0], OK[1], len(FALLITE), FALLITE, sotto[0] if sotto else None))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
