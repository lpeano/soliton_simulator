# -*- coding: utf-8 -*-
r"""**S4: LA LEGGE M-rho HA UN'INSTABILITA' NELLA MATERIA?** *(sul ramo laterale; Luca `2026-11-11` `09:17`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `30`)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/s4_materia_mrho.py > doc/referti_l2/s4_spettro_materia_mrho.txt
    python csv/solitone/s4_materia_mrho.py --v2 > doc/referti_l2/s4_spettro_materia_mrho_v2.txt
    python csv/solitone/s4_materia_mrho.py --lapse > doc/referti_l2/s5_lapse_spettro.txt
    python csv/solitone/s4_materia_mrho.py --lapse2 > doc/referti_l2/s5_lapse_spettro_v2.txt

**`--lapse2`** *(S5.2-bis punto 3, sez. `31.23`)*: **come `--lapse`, col punto fisso di `cs` del banco SMORZATO** *(`omega 0.5`, fino a `1000` giri: lo strumento, non la legge)*; **per ogni punto la storia degli scarti della base;**
**DEVE: dove il metodo di prima convergeva, lo stesso `cs` entro `1e-14`; un punto che non converge nemmeno cosi' si riporta e si toglie dalla mappa** *(dichiarato)*.

**`--lapse`** *(T-L3 di S5.2, sez. `31.15`)*: **la mappa e' il BANCO DEL LAPSE** *(`tick_lapse.tick`, la colonna «M-rho» e' il lapse)* **contro il `cs` congelato** *(il fondo passato identico, come `--v2`)*; **niente `A = F + P Q`** *(la reazione non e' un solo numero per nodo)*; **DEVE FALLIRE: il banco senza la reazione a `rho_0 1e-2`; le letture (l1)-(l3).**

**`--v2`** *(S4.7, sez. `30.7`)*: **il fondo `psi_0` calcolato UNA volta sulla mappa M-rho e passato IDENTICO al `cs` congelato; niente legge spenta** *(non e' il riferimento: l'errore n.135)*; **il DEVE contro la tabella del referto di 30.5.**

**Il fondo uniforme** `psi_0 = sqrt(rho_0) q` *(`q` la combinazione del solitone BG della coppia piu' alta a `Gamma`, ricalcolata in ogni punto)*, `phi_0 = c F3`; **due fasi** `u_psi`, `u_phi`.
**M-rho istantanea:** `cs = s / (1 + rho / rho_c)` col `rho` di inizio tick, `mot.lambda_c = None`. **La legge spenta:** `cs = s`. **Il `cs` congelato:** `cs = cs(rho_0)` costante.
**Lo spettro** come S2 *(`36` reali per cella, Richardson, `fft2`)*; **il meccanismo** `A = F + P Q`; **i DEVE** *(il vuoto con M-rho, la legge spenta, l'onda piana, il fattore `1.001`)*; **le letture (m1)-(m4).**
"""
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)
from solitone import carta_f1_lunga as F1L  # noqa: E402
from solitone import carta_punto_fisso as CPF  # noqa: E402

A_REL = 1e-4                   # ### come S2 (sez. 28.4): l'impulso relativo, Richardson
TOLL_LIN = 1e-6                # ### Luca (S2): |R(2a) - R(a)| / max|R|
TOLL_TRASL = 1e-9              # ### come S2
TOLL_PF = 1e-9 if "--lapse3" in sys.argv else 1e-12   # ### Luca (S4.0 a): il residuo della base; con --lapse3 1e-9 (Luca 2026-11-11 23:42, S5.3 A, scritta prima)
TOLL_UNIT = 1e-10              # ### sez. 30.4: la precisione di S2 (2.9e-11)
STABILE = 1e-9                 # ### Luca: stabile se |lambda|_max - 1 sotto 1e-9
TOLL_APQ = 1e-6                # ### mio (sez. 30.4): |A - F - P Q| / |A|
ONDA_AMP, ONDA_N, ONDA_DA, TOLL_ONDA = 1e-11, 100, 20, 0.05   # ### Luca: 100 tick, 5%; come S2: 1e-11 relativo, dal tick 20
ONDA_SAT = 1e-4                # ### mio: la pendenza solo finche' la differenza resta sotto 1e-4 relativo (oltre non e' lineare)
FATT_F = 1e-3                  # ### Luca
RAPPORTI = (1e-3, 1e-2, 1e-1, 1.0, 10.0)   # ### Luca: rho_0 / rho_c
RHO0 = (1e-4, 1e-2, 1.0)                   # ### Luca: rho_0, in unita' della norma per nodo
S_SCAN = (0.05, 0.15, 0.3)                 # ### Luca
MEZZO = (1e-2, 1e-1, 0.15)                 # ### mio: il punto della traslazione (rho_0, rapporto, s)
LAPSE3 = "--lapse3" in sys.argv             # ### S5.3 A (sez. 32.1): come --lapse2, con la soglia delle basi 1e-9
LAPSE2 = "--lapse2" in sys.argv or LAPSE3   # ### S5.2-bis punto 3 (sez. 31.23)
FORMA_A = "--forma-a" in sys.argv           # ### S5.3 A (sez. 32.1): il banco del lapse con la forma (a) (tick_lapse.fase_a); eps_a = la cima della coppia a Gamma del tick di oggi a cs = s
A_EPS = 1e-6                               # ### l'ampiezza delle colonne per eps_a (come A_IMP di T-L4b)
LAPSE = "--lapse" in sys.argv or LAPSE2     # ### T-L3 (sez. 31.15)
OMEGA_L, GIRI_L = (0.5, 1000) if LAPSE2 else (1.0, None)   # ### Luca (punto 3): omega 0.5, fino a 1000 giri
TOLL_CS_NUOVO = 1e-14                      # ### Luca (punto 3)
V2 = "--v2" in sys.argv or LAPSE            # ### S4.7 (sez. 30.7); --lapse usa il fondo unico
SENZA_RHO0 = 1e-2                          # ### sez. 31.15: il DEVE FALLIRE a rho_0 1e-2
JEANS_K, RETICOLO_K = 1.0, 2.0             # ### sez. 31.15 (miei): |k| < 1 la firma di Jeans, |k| > 2 la scala del reticolo


def L0(s):
    """### la legge del vuoto (`rho_0 = 0`): il lapse con `--lapse`, M-rho senza."""
    return ("lapse", s, 1.0, False) if LAPSE else ("mrho", s, 1.0)
TOLL_BASI = 1e-14                          # ### Luca (S4.7): lo scarto fra le basi
TOLL_30_5 = 1e-3                           # ### mio (sez. 30.7): «alla terza cifra»
REF_30_5 = os.path.join(os.path.dirname(os.path.dirname(_QUI)), "doc", "referti_l2", "s4_spettro_materia_mrho.txt")
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-104s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:104], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return buono


def main():
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    import composizione as CM
    import tick as TK
    from solitone import bordo as BO
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    from solitone import tick_lapse as TL
    for m in ("__init__", "corsa_accensione", "toro", "bordo", "carta_punto_fisso", "carta_f1_lunga", "tick_lapse"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("tick", "flussi_parziali", "energia_pesata"):
        _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s_scena = V.CORSE[CA.NOME]
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab, omega, K = d["c"].copy(), float(d["omega"]), int(d["K"])
    c = BO.c_di(CPF.TICK_D4, tab, K, omega)
    gr = V.LP.leggi(os.path.join(V.CB.DIR_JSON, "griglia.json"))[V.CO.NOME_EPS]
    th, fi = float(gr["minimo"]["theta"]), float(gr["minimo"]["phi"])
    t00 = time.time()
    print("=" * 130)
    print("S4 (sez. 30): M-rho nella materia; il fondo sqrt(rho_0) q, q = cos(%.6f) q1 + e^{i %.6f} sin(%.6f) q2 (griglia.json, %s); a %g; stabile se |lambda|_max - 1 < %g" % (th, fi, th, V.CO.NOME_EPS, A_REL, STABILE))
    print("=" * 130)
    with CA.con_L(CA.LCORSA.get(CPF.CORSA)), V.scena(s_scena, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s_scena)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        phi_v = CA.vuoto_della_corsa(z, CPF.CORSA)
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, mot, par, inc = z["st"], z["mot"], z["par"], z["inc"]
        n, Lt = inc.n, z["L"]
        assert inc.nodo.size == 6 * n and np.array_equal(inc.nodo[0::2], np.repeat(np.arange(n), 3)), "la cella NON e' di 3 archi per nodo"
        assert st["phi_h"].size == 6 * n and st["psi_h"].size == 12 * n, "psi o phi NON hanno 12 e 6 componenti per cella"
        forma_psi = st["psi_h"].shape
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        phi_b = c * phi_v
        st["psi_h"][...] = 0.0
        st["phi_h"][...] = phi_b
        lam0 = mot.densita_vuoto(st).copy()
        print("### la scena: s %g (la scena), la forma materia-vuoto %s, eps %g; psi %s %s; Lambda del vuoto per nodo da %.15f a %.15f" % (
            s_scena, VC.FORMA, z["par"]["eps"], forma_psi, st["psi_h"].dtype, float(lam0.min()), float(lam0.max())))
        A1, A2 = TO.vettori()
        B = 2.0 * np.pi * np.linalg.inv(np.array([A1, A2])).T
        m = np.fft.fftfreq(Lt) * Lt
        M1, M2 = np.meshgrid(m, m, indexing="ij")
        KK = np.full((Lt, Lt), np.inf)
        KX = np.zeros((Lt, Lt, 2))
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                kv = ((M1 + a * Lt)[..., None] * B[0] + (M2 + b * Lt)[..., None] * B[1]) / Lt
                q = np.hypot(kv[..., 0], kv[..., 1])
                meglio = q < KK
                KK = np.where(meglio, q, KK)
                KX = np.where(meglio[..., None], kv, KX)
        i1, i2 = np.arange(n) // Lt, np.arange(n) % Lt

        def rho_di(psi):
            r = np.zeros(n)
            np.add.at(r, inc.nodo, np.sum(np.abs(psi.reshape(inc.nodo.size, -1)) ** 2, axis=1))
            return r

        def cs_di(psi, legge):
            """### `legge`: `("mrho", s, rho_c)` o `("cost", valore)`."""
            if legge[0] in ("mrho", "lapse"):
                return legge[1] / (1.0 + rho_di(psi) / legge[2])
            return np.full(n, float(legge[1]))

        EPS_A = {}                     # ### S5.3 A: eps_a per s (si riempie prima delle basi, con --forma-a)

        def mappa(psi, phi, legge, u_psi, u_phi, dcs=None, fattore=1.0):
            """### UN tick: `(u_psi^* psi', u_phi^* phi')`; il `cs` dallo stato di INIZIO tick, `mot.lambda_c = None`."""
            for k in chiavi:
                st[k][...] = salvato[k]
            st["psi_h"][...] = psi.reshape(forma_psi)
            st["phi_h"][...] = phi
            if legge[0] == "lapse":
                assert dcs is None, "il lapse non ha un impulso di cs"
                TL.tick(mot, st, par, legge[1], ("rho_c", legge[2]), senza_reazione=legge[3], omega=OMEGA_L, giri_max=GIRI_L, eps_a=(EPS_A[legge[1]] if FORMA_A else None))
                return st["psi_h"].reshape(n, 12) * np.conj(u_psi) * fattore, st["phi_h"] * np.conj(u_phi) * fattore
            fa = None
            if legge[0] == "cost_a":       # ### S5.3 A (sez. 32.1, la cura): il congelato della forma (a), la fase STATICA e^{+i eps_a (N_0 - 1)} per tick, a meta' prima e dopo
                fa = np.exp(0.5j * EPS_A[legge[2]] * (legge[1] / legge[2] - 1.0))
                st["psi_h"][...] = st["psi_h"] * fa
            cs = cs_di(psi, legge)
            if dcs is not None:
                cs = cs + dcs
            mot.cs = cs
            mot.lambda_c = None
            TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
            if fa is not None:
                st["psi_h"][...] = st["psi_h"] * fa
            return st["psi_h"].reshape(n, 12) * np.conj(u_psi) * fattore, st["phi_h"] * np.conj(u_phi) * fattore

        def cong(cs0, s):
            """### la legge del `cs` congelato: `("cost", cs0)`; con `--forma-a` `("cost_a", cs0, s)` *(la fase statica della forma (a))*."""
            return ("cost_a", cs0, s) if FORMA_A else ("cost", cs0)

        def cella(psi, phi):
            p = psi.reshape(n, 12)
            f = phi.reshape(n, 6)
            return np.concatenate([p.real, p.imag, f.real, f.imag], axis=1)

        def base(rho0, legge, psi_dato=None):
            """### il fondo, le due fasi, i residui; `q` dalla coppia piu' alta a `Gamma` del blocco di `psi` in QUESTO punto; `psi_dato` (S4.7): il fondo passato com'e'."""
            out = {"rho0": rho0, "legge": legge}
            if psi_dato is not None:
                psi = psi_dato.copy()
            elif rho0 > 0.0:
                Mg = np.zeros((12, 12), dtype=complex)
                rr = []
                for cc in range(12):
                    p = np.zeros((n, 12), dtype=complex)
                    p[:, cc] = math.sqrt(rho0)
                    rr.append(float(np.max(np.abs(rho_di(p) - rho0))))
                    p1, _ = mappa(p, phi_b, legge, 1.0, 1.0)
                    Mg[:, cc] = p1[0] / math.sqrt(rho0)
                lam, Vv = np.linalg.eig(Mg)
                E = -np.angle(lam)
                o = np.argsort(E)
                top = [int(o[-2]), int(o[-1])]
                Qm = np.linalg.qr(Vv[:, top])[0]
                q = math.cos(th) * Qm[:, 0] + np.exp(1j * fi) * math.sin(th) * Qm[:, 1]
                q /= np.linalg.norm(q)
                psi = np.tile(math.sqrt(rho0) * q, (n, 1))
                out.update({"E_top": (float(E[top[0]]), float(E[top[1]])), "rho_e": max(rr), "q": q})
            else:
                psi = np.zeros((n, 12), dtype=complex)
            r0 = rho_di(psi)
            p1, f1 = mappa(psi, phi_b, legge, 1.0, 1.0)
            if rho0 > 0.0:
                zz = complex(np.vdot(psi, p1))
                up = zz / abs(zz)
            else:
                up = 1.0 + 0.0j
            zz = complex(np.vdot(phi_b, f1))
            uf = zz / abs(zz)
            res_p = float(np.max(np.abs(p1 * np.conj(up) - psi))) / float(np.max(np.abs(psi))) if rho0 > 0.0 else float(np.max(np.abs(p1)))
            res_f = float(np.max(np.abs(f1 * np.conj(uf) - phi_b))) / float(np.max(np.abs(phi_b)))
            out.update({"psi": psi, "phi": phi_b.copy(), "u_psi": up, "u_phi": uf, "res_p": res_p, "res_f": res_f, "rho_min": float(r0.min()), "rho_max": float(r0.max()),
                        "cs0": float(np.mean(cs_di(psi, legge))), "om_psi": -math.atan2(up.imag, up.real), "om_phi": -math.atan2(uf.imag, uf.real)})
            return out

        def stampa_base(nome, b):
            print("    %s: rho da %.6e a %.6e; cs del fondo %.10f; omega_psi %+.10f, omega_phi %+.10f; i residui psi %.3e, phi %.3e%s" % (
                nome, b["rho_min"], b["rho_max"], b["cs0"], b["om_psi"], b["om_phi"], b["res_p"], b["res_f"],
                ("; E delle due bande alte %.12f, %.12f (la differenza %.2e); rho dei vettori della base: lo scarto %.2e" % (b["E_top"][0], b["E_top"][1], b["E_top"][1] - b["E_top"][0], b["rho_e"])) if "q" in b else ""))

        def scale(b):
            ap = A_REL * (math.sqrt(b["rho0"] / 12.0) if b["rho0"] > 0.0 else 1.0)
            af = A_REL * float(np.sqrt(np.mean(np.abs(b["phi"]) ** 2)))
            return np.array([ap] * 24 + [af] * 12)

        def spinta(b, j, f, x0):
            ps = b["psi"].copy()
            ph = b["phi"].copy()
            a = scale(b)[j] * f
            if j < 12:
                ps[x0, j] += a
            elif j < 24:
                ps[x0, j - 12] += 1j * a
            elif j < 30:
                ph[6 * x0 + j - 24] += a
            else:
                ph[6 * x0 + j - 30] += 1j * a
            return ps, ph

        def risposta(b, legge, x0=0, colonne=None, fattore=1.0):
            sc = scale(b)
            R = np.zeros((n, 36, 36))
            dev = 0.0
            for j in (range(36) if colonne is None else colonne):
                us = {}
                for f in (1, -1, 2, -2):
                    ps, ph = spinta(b, j, f, x0)
                    us[f] = cella(*mappa(ps, ph, legge, b["u_psi"], b["u_phi"], fattore=fattore))
                r1 = (us[1] - us[-1]) / (2 * sc[j])
                r2 = (us[2] - us[-2]) / (4 * sc[j])
                dev = max(dev, float(np.max(np.abs(r2 - r1))) / max(float(np.max(np.abs(r1))), 1e-300))
                R[:, :, j] = (4.0 * r1 - r2) / 3.0
            return R, dev

        def risposta_cs(b, legge):
            """### `P`: la risposta della cella a un impulso di `cs` nel nodo `0` *(Richardson)*; `Q`: la risposta del `cs` dei nodi a un impulso dello stato della cella `0` *(dalla legge)*."""
            a = A_REL * b["cs0"]
            us = {}
            for f in (1, -1, 2, -2):
                d = np.zeros(n)
                d[0] = f * a
                us[f] = cella(*mappa(b["psi"], b["phi"], legge, b["u_psi"], b["u_phi"], dcs=d))
            P = (4.0 * (us[1] - us[-1]) / (2 * a) - (us[2] - us[-2]) / (4 * a)) / 3.0
            sc = scale(b)
            Qx = np.zeros((n, 36))
            for j in range(36):
                cc = {}
                for f in (1, -1, 2, -2):
                    ps, _ph = spinta(b, j, f, 0)
                    cc[f] = cs_di(ps, legge)
                Qx[:, j] = (4.0 * (cc[1] - cc[-1]) / (2 * sc[j]) - (cc[2] - cc[-2]) / (4 * sc[j])) / 3.0
            return np.fft.fft2(P.reshape(Lt, Lt, 36), axes=(0, 1)), np.fft.fft2(Qx.reshape(Lt, Lt, 36), axes=(0, 1))

        def spettro(R):
            nd = R.shape[1]
            Ak = np.fft.fft2(R.reshape(Lt, Lt, nd, nd), axes=(0, 1))
            mod = np.abs(np.linalg.eigvals(Ak.reshape(-1, nd, nd)))
            mk = mod.max(axis=1)
            im = int(np.argmax(mk))
            return {"Ak": Ak, "max": float(mk[im]), "min": float(mod.min()), "dev_unit": float(np.max(np.abs(mod - 1.0))), "ik": im, "neq": int(np.sum(mk >= mk[im] - 1e-9)), "k0": float(mk[0])}

        def descrivi(sp, nome):
            a1, a2 = divmod(sp["ik"], Lt)
            w, vr = np.linalg.eig(sp["Ak"][a1, a2])
            bb = int(np.argmax(np.abs(w)))
            kx = KX[a1, a2]
            d = {"m": (a1, a2), "k": float(KK[a1, a2]), "dir": float(np.degrees(np.arctan2(kx[1], kx[0]))) % 360.0, "lam": complex(w[bb]), "v": vr[:, bb], "neq": sp["neq"],
                 "fpsi": float(np.sum(np.abs(vr[:24, bb]) ** 2) / np.sum(np.abs(vr[:, bb]) ** 2))}
            print("      %s: |lambda|_max %.12f (ln %.3e per tick), lambda %+.8f %+.8fi; al k (%d, %d), |k| %.5f, la direzione %.2f gradi; %d k equivalenti; |lambda| a k = 0 %.12f; la frazione in psi %.4f"
                  % (nome, abs(w[bb]), math.log(abs(w[bb])), w[bb].real, w[bb].imag, a1, a2, d["k"], d["dir"], sp["neq"], sp["k0"], d["fpsi"]))
            sys.stdout.flush()
            return d

        tab_ = []
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            # ============================================================== le basi: (m4) prima di tutto
            if FORMA_A:                # ### S5.3 A: eps_a(s) = la cima della coppia piu' alta a Gamma del tick di oggi (cs = s), dalle 12 colonne uniformi (come T-L4b)
                for s_ in S_SCAN:
                    Mg = np.zeros((12, 12), dtype=complex)
                    for cc in range(12):
                        u = []
                        for f_ in (1.0, -1.0):
                            p = np.zeros((n, 12), dtype=complex)
                            p[:, cc] = f_ * A_EPS
                            u.append(mappa(p, phi_b, ("cost", s_), 1.0, 1.0)[0][0])
                        Mg[:, cc] = (u[0] - u[1]) / (2 * A_EPS)
                    E_ = np.sort(-np.angle(np.linalg.eigvals(Mg)))
                    EPS_A[s_] = 0.5 * float(E_[-1] + E_[-2])
                    print("### LA FORMA (a), s %g: eps_a = %.12f per tick (la coppia piu' alta a Gamma del tick di oggi: %.12f, %.12f)" % (s_, EPS_A[s_], E_[-2], E_[-1]))
            print("### LE BASI (S4.0 a): il residuo sotto %g" % TOLL_PF)
            basi = {}
            tolti = set()

            def diagnosi_cs(rho0, ra, s):
                """### **Il punto fisso di `cs` della base** *(il fondo uniforme)* **col metodo di prima e col nuovo; la storia degli scarti.** `None` se il nuovo non converge."""
                rc = rho0 / ra
                Mg = np.zeros((12, 12), dtype=complex)
                for cc in range(12):
                    pp = np.zeros((n, 12), dtype=complex)
                    pp[:, cc] = math.sqrt(rho0)
                    p1, _ = mappa(pp, phi_b, ("cost", s / (1.0 + rho0 / rc)), 1.0, 1.0)
                    Mg[:, cc] = p1[0] / math.sqrt(rho0)
                lam, Vv = np.linalg.eig(Mg)
                E = -np.angle(lam)
                o = np.argsort(E)
                Qm = np.linalg.qr(Vv[:, [int(o[-2]), int(o[-1])]])[0]
                qq = math.cos(th) * Qm[:, 0] + np.exp(1j * fi) * math.sin(th) * Qm[:, 1]
                psi = np.tile(math.sqrt(rho0) * qq / np.linalg.norm(qq), (n, 1))
                ris = {}
                for nome, om, gm in (("prima", 1.0, None), ("nuovo", OMEGA_L, GIRI_L)):
                    for k in chiavi:
                        st[k][...] = salvato[k]
                    st["psi_h"][...] = psi.reshape(forma_psi)
                    st["phi_h"][...] = phi_b
                    stor = []
                    try:
                        cs_, g_ = TL.cs_al_centro(mot, st, par, s, ("rho_c", rc), False, omega=om, giri_max=gm, storia=stor)
                        ris[nome] = (cs_.copy(), g_, stor)
                    except AssertionError:
                        ris[nome] = (None, len(stor), stor)
                    sc = ris[nome][2]
                    print("    il punto fisso di cs, rho_0 %g, rapporto %g, s %g, %s (omega %g): %s in %d giri; gli scarti %s ... %s" % (
                        rho0, ra, s, nome, om, "converge" if ris[nome][0] is not None else "### NON converge", len(sc),
                        " ".join("%.2e" % x for x in sc[:3]), " ".join("%.2e" % x for x in sc[-3:])))
                if ris["nuovo"][0] is None:
                    print("    ### il punto (rho_0 %g, rapporto %g, s %g) NON converge nemmeno col metodo nuovo (lo scarto finale %.3e): si TOGLIE dalla mappa (dichiarato)" % (rho0, ra, s, ris["nuovo"][2][-1]))
                    return None
                if ris["prima"][0] is not None:
                    d = float(np.max(np.abs(ris["prima"][0] - ris["nuovo"][0])))
                    confronti.append(d)
                return ris
            confronti = []
            for s in S_SCAN:
                basi[(0.0, None, s)] = base(0.0, L0(s))
                stampa_base("rho_0 0, M-rho, s %g" % s, basi[(0.0, None, s)])
                for rho0 in RHO0:
                    if not V2:
                        basi[(rho0, "spenta", s)] = base(rho0, ("cost", s))
                        stampa_base("rho_0 %g, la legge spenta, s %g" % (rho0, s), basi[(rho0, "spenta", s)])
                    for ra in RAPPORTI:
                        legge = ("lapse", s, rho0 / ra, False) if LAPSE else ("mrho", s, rho0 / ra)
                        if LAPSE2:
                            dia = diagnosi_cs(rho0, ra, s)
                            if dia is None:
                                tolti.add((rho0, ra, s))
                                continue
                        try:
                            basi[(rho0, ra, s)] = base(rho0, legge)
                        except AssertionError as ex:
                            if not LAPSE2:
                                raise
                            print("    ### il punto (rho_0 %g, rapporto %g, s %g): la BASE non si costruisce (il punto fisso di cs del tick non converge): si TOGLIE dalla mappa (dichiarato): %s" % (rho0, ra, s, str(ex)[:150]))
                            tolti.add((rho0, ra, s))
                            continue
                        stampa_base("rho_0 %g, rho_0/rho_c %g, s %g, M-rho" % (rho0, ra, s), basi[(rho0, ra, s)])
                        basi[(rho0, ("cong", ra), s)] = base(rho0, cong(basi[(rho0, ra, s)]["cs0"], s), psi_dato=basi[(rho0, ra, s)]["psi"] if V2 else None)
                        if V2:
                            stampa_base("rho_0 %g, rho_0/rho_c %g, s %g, il cs congelato (il fondo di M-rho)" % (rho0, ra, s), basi[(rho0, ("cong", ra), s)])
            if V2:
                sb = max(float(np.max(np.abs(basi[k]["psi"] - basi[(k[0], k[1][1], k[2])]["psi"]))) for k in basi if isinstance(k[1], tuple))
                esito("(S4.7) lo scarto fra il fondo di M-rho e quello del cs congelato < %g, in tutti i punti" % TOLL_BASI, sb < TOLL_BASI, "%.3e" % sb)
            if LAPSE2:
                print("    i punti tolti: %d %s" % (len(tolti), sorted(tolti)))
                esito("(punto 3) dove il metodo di prima converge, lo stesso cs col nuovo entro %g (%d punti)" % (TOLL_CS_NUOVO, len(confronti)), bool(confronti) and max(confronti) <= TOLL_CS_NUOVO, "%.3e" % (max(confronti) if confronti else float("nan")))
            peggio = max(max(b["res_p"], b["res_f"]) for b in basi.values())
            print("    il residuo piu' grande fra le %d basi: %.3e" % (len(basi), peggio))
            if not esito("(S4.0 a) ogni base e' un punto fisso nel riferimento che gira (il residuo < %g)" % TOLL_PF, peggio < TOLL_PF, "%.3e" % peggio):
                print("  LA LETTURA: (m4) il fondo uniforme non e' un punto fisso: FERMO prima dello spettro")
                print("=" * 130)
                print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
                return 1
            # ============================================================== i DEVE del vuoto con M-rho, e il fattore
            print("### rho_0 = 0 CON M-rho (il vuoto stabile per costruzione)")
            for s in S_SCAN:
                b = basi[(0.0, None, s)]
                R, dev = risposta(b, L0(s))
                sp = spettro(R)
                print("    s %g: la linearita' %.2e; max ||lambda| - 1| %.3e" % (s, dev, sp["dev_unit"]))
                esito("rho_0 0, M-rho, s %g: lo spettro e' unitario (< %g)" % (s, TOLL_UNIT), sp["dev_unit"] < TOLL_UNIT, "%.3e" % sp["dev_unit"])
            b = basi[(0.0, None, 0.15)]
            print("### IL DEVE FALLIRE: rho_0 0, M-rho, s 0.15, psi e phi per (1 + %g) dopo il tick" % FATT_F)
            R, _ = risposta(b, L0(0.15), fattore=1.0 + FATT_F)
            sp = spettro(R)
            esito("il fattore: |lambda| = %.3f entro 1e-9 su ogni k" % (1 + FATT_F), abs(sp["max"] - 1 - FATT_F) < 1e-9 and abs(sp["min"] - 1 - FATT_F) < 1e-9, "%.3e, %.3e" % (sp["max"] - 1 - FATT_F, sp["min"] - 1 - FATT_F))
            esito("il fattore: lo spettro e' unitario (< %g)" % TOLL_UNIT, sp["dev_unit"] < TOLL_UNIT, "%.3e" % sp["dev_unit"], deve=False)
            del R
            # ============================================================== la legge spenta
            if not V2:
                print("### LA LEGGE SPENTA (cs = s), rho_0 > 0: la materia senza orologio")
            spenta = {}
            for s in (S_SCAN if not V2 else ()):
                for rho0 in RHO0:
                    b = basi[(rho0, "spenta", s)]
                    R, dev = risposta(b, ("cost", s))
                    sp = spettro(R)
                    print("    rho_0 %g, s %g: la linearita' %.2e; max ||lambda| - 1| %.3e" % (rho0, s, dev, sp["dev_unit"]))
                    d_ = descrivi(sp, "la legge spenta")
                    spenta[(rho0, s)] = (sp["max"], d_, sp["dev_unit"])
                    esito("la legge spenta, rho_0 %g, s %g: lo spettro e' unitario (< %g)" % (rho0, s, TOLL_UNIT), sp["dev_unit"] < TOLL_UNIT, "%.3e" % sp["dev_unit"])
                    esito("la legge spenta, rho_0 %g, s %g: la linearita' < %g" % (rho0, s, TOLL_LIN), dev < TOLL_LIN, "%.2e" % dev)
            spenta_ok = all(v[2] < TOLL_UNIT for v in spenta.values())
            # ============================================================== la mappa: M-rho e il cs congelato
            print("### LA MAPPA: %d punti, M-rho e il cs congelato" % (len(RHO0) * len(RAPPORTI) * len(S_SCAN)))
            migliore = None
            for s in S_SCAN:
                for rho0 in RHO0:
                    for ra in RAPPORTI:
                        legge = ("lapse", s, rho0 / ra, False) if LAPSE else ("mrho", s, rho0 / ra)
                        if (rho0, ra, s) in tolti:
                            print("  IL PUNTO rho_0 %g, rho_0/rho_c %g, s %g: TOLTO (il punto fisso di cs non converge)" % (rho0, ra, s))
                            continue
                        b = basi[(rho0, ra, s)]
                        bc = basi[(rho0, ("cong", ra), s)]
                        print("  IL PUNTO rho_0 %g, rho_0/rho_c %g (rho_c %.4e), s %g: cs del fondo %.10f" % (rho0, ra, rho0 / ra, s, b["cs0"]))
                        try:
                            R, dev = risposta(b, legge)
                        except AssertionError as ex:
                            if not LAPSE2:
                                raise
                            print("    ### il punto (rho_0 %g, rapporto %g, s %g) NON converge su una perturbazione: TOLTO (dichiarato): %s" % (rho0, ra, s, str(ex)[:150]))
                            tolti.add((rho0, ra, s))
                            continue
                        sp = spettro(R)
                        esito("rho_0 %g, rapporto %g, s %g: la linearita' < %g" % (rho0, ra, s, TOLL_LIN), dev < TOLL_LIN, "%.2e" % dev)
                        d_ = descrivi(sp, "M-rho")
                        if (rho0, ra, s) == MEZZO:
                            Rx, _ = risposta(b, legge, x0=(Lt // 2) * Lt + 7, colonne=(0, 24))
                            x0 = (Lt // 2) * Lt + 7
                            dtr = 0.0
                            for j in (0, 24):
                                sh = np.roll(R[:, :, j].reshape(Lt, Lt, -1), (x0 // Lt, x0 % Lt), axis=(0, 1)).reshape(n, -1)
                                dtr = max(dtr, float(np.max(np.abs(Rx[:, :, j] - sh))) / float(np.max(np.abs(sh))))
                            esito("l'invarianza per traslazione al punto %s (le direzioni 0 e 24) < %g" % (MEZZO, TOLL_TRASL), dtr < TOLL_TRASL, "%.3e" % dtr)
                            del Rx
                        del R
                        Rc, devc = risposta(bc, cong(b["cs0"], s))
                        spc = spettro(Rc)
                        del Rc
                        dc = descrivi(spc, "il cs congelato")
                        if not LAPSE:
                            a1, a2 = d_["m"]
                            Pk, Qk = risposta_cs(b, legge)
                            A = sp["Ak"][a1, a2]
                            Fk = spc["Ak"][a1, a2]
                            PQ = np.outer(Pk[a1, a2], Qk[a1, a2])
                            apq = float(np.linalg.norm(A - Fk - PQ) / np.linalg.norm(A))
                            wb, eb = np.linalg.eig(Fk)
                            inv = np.linalg.inv(eb)
                            lam_ = d_["lam"]
                            contr = np.array([(Qk[a1, a2] @ eb[:, q_]) * (inv[q_, :] @ Pk[a1, a2]) / (lam_ - wb[q_]) for q_ in range(36)])
                            g = complex(np.sum(contr))
                            coef = inv @ d_["v"]
                            pes = np.abs(coef) ** 2 / np.sum(np.abs(coef) ** 2)
                            oc = np.argsort(-np.abs(contr))
                            op = np.argsort(-pes)
                            print("      il meccanismo al k di M-rho: |A - F - P Q| / |A| %.2e; g(lambda) = %+.6e %+.6ei (deve essere 1: lambda non e' un autovalore di F); |P| %.3e, |Q| %.3e; il cs congelato a quel k: max|lambda_b| %.12f"
                                  % (apq, g.real, g.imag, float(np.linalg.norm(Pk[a1, a2])), float(np.linalg.norm(Qk[a1, a2])), float(np.max(np.abs(wb)))))
                            print("      le bande del cs congelato: i pesi piu' grandi %s; i contributi a g piu' grandi %s" % (
                                "; ".join("%.4f (omega_b %+.6f, |lambda_b| %.9f)" % (pes[q_], -np.angle(wb[q_]), abs(wb[q_])) for q_ in op[:3]),
                                "; ".join("%+.4e %+.4ei (omega_b %+.6f)" % (contr[q_].real, contr[q_].imag, -np.angle(wb[q_])) for q_ in oc[:3])))
                            esito("rho_0 %g, rapporto %g, s %g: A = F + P Q al k piu' instabile (< %g)" % (rho0, ra, s, TOLL_APQ), apq < TOLL_APQ, "%.2e" % apq)
                        tab_.append({"rho0": rho0, "ra": ra, "s": s, "cs0": b["cs0"], "max": sp["max"], "cong": spc["max"], "spenta": spenta[(rho0, s)][0] if not V2 else float("nan"), "d": d_, "dc": dc})
                        if migliore is None or sp["max"] > migliore[0]:
                            migliore = (sp["max"], rho0, ra, s, d_, b, legge)
                        del sp, spc
            senza = []
            if LAPSE:
                print("### T-L3, DEVE FALLIRE: il banco SENZA la reazione a rho_0 %g, contro il cs congelato" % SENZA_RHO0)
                for s in S_SCAN:
                    for ra in RAPPORTI:
                        if (SENZA_RHO0, ra, s) in tolti:
                            continue
                        b = basi[(SENZA_RHO0, ra, s)]
                        ls = ("lapse", s, SENZA_RHO0 / ra, True)
                        try:
                            bs = base(SENZA_RHO0, ls, psi_dato=b["psi"])
                            R, dev = risposta(bs, ls)
                        except AssertionError as ex:
                            if not LAPSE2:
                                raise
                            print("    ### senza reazione, rapporto %g, s %g: il punto fisso di cs NON converge: saltato (dichiarato): %s" % (ra, s, str(ex)[:150]))
                            continue
                        sp = spettro(R)
                        del R
                        d_ = descrivi(sp, "senza reazione")
                        cg = [r_ for r_ in tab_ if (r_["rho0"], r_["ra"], r_["s"]) == (SENZA_RHO0, ra, s)][0]["cong"]
                        senza.append((s, ra, math.log(sp["max"]) - math.log(cg), d_))
                        print("    rapporto %g, s %g: il residuo della base %.3e; la linearita' %.2e; ln |lambda|_max senza reazione meno il congelato %+.4e" % (ra, s, max(bs["res_p"], bs["res_f"]), dev, senza[-1][2]))
                        del sp
            # ============================================================== l'onda piana al punto piu' instabile
            if migliore[0] - 1.0 > STABILE:
                mx, rho0, ra, s, d_, b, legge = migliore
                a1, a2 = d_["m"]
                fase = np.exp(2j * np.pi * (a1 * i1 + a2 * i2) / Lt)
                dl = np.real(d_["v"][None, :] * fase[:, None])
                dl *= ONDA_AMP / float(np.max(np.abs(dl)))
                sc_rel = max(math.sqrt(rho0 / 12.0), 1.0)
                print("### L'ONDA PIANA: al punto rho_0 %g, rapporto %g, s %g, al k (%d, %d), l'ampiezza massima %g; M-rho vera, %d tick, contro un gemello" % (rho0, ra, s, a1, a2, ONDA_AMP, ONDA_N))
                pb, fb = b["psi"].copy(), b["phi"].copy()
                po, fo = b["psi"] + dl[:, :12] + 1j * dl[:, 12:24], b["phi"] + (dl[:, 24:30] + 1j * dl[:, 30:36]).reshape(-1)
                D = []
                for k in range(ONDA_N):
                    pb, fb = mappa(pb, fb, legge, 1.0, 1.0)
                    po, fo = mappa(po, fo, legge, 1.0, 1.0)
                    D.append(math.sqrt(float(np.sum(np.abs(po - pb) ** 2) + np.sum(np.abs(fo - fb) ** 2))))
                D = np.array(D)
                tt = np.arange(1, ONDA_N + 1)
                sel = (tt >= ONDA_DA) & (D < ONDA_SAT * sc_rel * math.sqrt(n))
                t_onda = F1L.pendenza(tt[sel], np.log(D[sel])) if np.sum(sel) >= 3 else float("nan")
                t_sp = math.log(mx)
                print("    la differenza ai tick 1, 10, 20, 50, 100: %s; la pendenza su %d tick (dal %d, sotto %g relativo): %.6e per tick; lo spettro %.6e" % (
                    " ".join("%.3e" % D[t - 1] for t in (1, 10, 20, 50, 100)), int(np.sum(sel)), ONDA_DA, ONDA_SAT, t_onda, t_sp))
                esito("l'onda piana cresce col tasso dello spettro entro il %g%%" % (100 * TOLL_ONDA), t_onda == t_onda and abs(t_onda / t_sp - 1.0) <= TOLL_ONDA, "il rapporto %.4f" % (t_onda / t_sp))
            else:
                print("### L'ONDA PIANA: nessun punto instabile (il massimo %.12f): non si semina" % migliore[0])
    # ================================================================== la tabella e le letture
    print("-" * 130)
    print("  LA MAPPA (ln |lambda|_max per tick; 0 = unitario entro %g):" % STABILE)
    print("  %8s %8s %6s %12s %13s %13s %13s %13s %9s %8s %8s" % ("rho_0", "rho0/rhoc", "s", "cs fondo", "M-rho", "cs congelato", "legge spenta", "M-rho - cong", "|k|", "dir", "f psi"))
    for r_ in tab_:
        print("  %8g %8g %6g %12.8f %13.5e %13.5e %13.5e %13.5e %9.5f %8.2f %8.4f" % (r_["rho0"], r_["ra"], r_["s"], r_["cs0"], math.log(r_["max"]), math.log(r_["cong"]), (math.log(r_["spenta"]) if r_["spenta"] == r_["spenta"] else float("nan")),
              math.log(r_["max"]) - math.log(r_["cong"]), r_["d"]["k"], r_["d"]["dir"], r_["d"]["fpsi"]))
    inst = {(r_["rho0"], r_["ra"], r_["s"]): r_["max"] - 1.0 > STABILE for r_ in tab_}
    print("  M-rho instabili: %d su %d" % (sum(inst.values()), len(inst)))
    if LAPSE:
        dif = [math.log(r_["max"]) - math.log(r_["cong"]) for r_ in tab_]
        sopra = [(r_, d) for r_, d in zip(tab_, dif) if d > STABILE]
        print("  T-L3: il lapse sopra il congelato oltre %g in %d punti su %d; la differenza piu' grande %+.4e" % (STABILE, len(sopra), len(tab_), max(dif)))
        ssopra = [x for x in senza if x[2] > STABILE]
        print("  T-L3-F, senza la reazione (rho_0 %g): sopra il congelato in %d punti su %d; il massimo %+.4e" % (SENZA_RHO0, len(ssopra), len(senza), max(x[2] for x in senza) if senza else float("nan")))
        esito("T-L3-F: senza la reazione il banco NON supera il congelato oltre %g in nessun punto" % STABILE, len(ssopra) == 0, "%d punti sopra" % len(ssopra), deve=False)
        if not sopra:
            print("  LA LETTURA: (l1) (I-cs) SPARISCE: il lapse non supera il congelato oltre %g in tutta la mappa" % STABILE)
        else:
            ret = [r_ for r_, d in sopra if r_["d"]["k"] > RETICOLO_K]
            jea = [r_ for r_, d in sopra if r_["d"]["k"] < JEANS_K and r_["d"]["fpsi"] > 0.5]
            for r_, d in sopra:
                print("    sopra: rho_0 %g, rapporto %g, s %g: %+.4e, |k| %.5f, la frazione in psi %.4f" % (r_["rho0"], r_["ra"], r_["s"], d, r_["d"]["k"], r_["d"]["fpsi"]))
            if ret:
                print("  LA LETTURA: (l3) un'instabilita' alla scala del reticolo (|k| > %g) in %d punti: FERMO" % (RETICOLO_K, len(ret)))
            elif len(jea) == len(sopra):
                print("  LA LETTURA: (l2) la firma di Jeans (|k| < %g, l'autovettore nella materia) in tutti i %d punti sopra il congelato: CANDIDATA GRAVITA' (il tasso per rho_0 e k qui sopra)" % (JEANS_K, len(sopra)))
            else:
                print("  LA LETTURA: caso intermedio (sopra il congelato %d punti: %d con la firma di Jeans, %d alla scala del reticolo)" % (len(sopra), len(jea), len(ret)))
    if V2 and not LAPSE:
        vecchi = {}
        with open(REF_30_5, encoding="utf-8") as f:
            dentro = False
            for riga in f:
                if "LA MAPPA (ln |lambda|_max" in riga:
                    dentro = True
                    continue
                if dentro:
                    p_ = riga.split()
                    if len(p_) == 11:
                        try:
                            vecchi[(float(p_[0]), float(p_[1]), float(p_[2]))] = float(p_[4])
                        except ValueError:
                            pass
        peggio_v = 0.0
        for r_ in tab_:
            if r_["rho0"] < 1.0:
                vv = vecchi[(r_["rho0"], r_["ra"], r_["s"])]
                peggio_v = max(peggio_v, abs(math.log(r_["max"]) / vv - 1.0))
        print("  (S4.7) i punti a rho_0 1e-4 e 1e-2 contro la tabella di 30.5 (%d righe lette): lo scarto relativo piu' grande di ln |lambda|_max %.3e" % (len(vecchi), peggio_v))
        esito("(S4.7) i punti a rho_0 1e-4 e 1e-2 ridanno 30.5 entro %g relativo" % TOLL_30_5, peggio_v < TOLL_30_5, "%.3e" % peggio_v)
        r0_ = [r_ for r_ in tab_ if (r_["rho0"], r_["ra"], r_["s"]) == (1e-4, 1e-3, 0.05)][0]
        sf = abs(math.log(r0_["max"]) / vecchi[(1e-4, 1e-2, 0.05)] - 1.0)
        esito("(S4.7) il controllo sa dire di no: il punto (1e-4, 1e-3, 0.05) contro la riga (1e-4, 1e-2, 0.05) di 30.5 entro %g" % TOLL_30_5, sf < TOLL_30_5, "%.3e" % sf, deve=False)
        print("  (S4.7) nessuna lettura nuova (sez. 30.7): la colonna M-rho - cong dice quanto (I-cs) aggiunge sopra (I-mod)")
    elif LAPSE:
        pass
    elif not spenta_ok:
        print("  ### LA LEGGE SPENTA NON E' UNITARIA (sopra): la materia e' instabile anche senza orologio; le letture (m1)-(m3) presuppongono un riferimento stabile e NON si leggono (sez. 30.4). FERMO")
    else:
        soglie = {}
        for s in S_SCAN:
            for rho0 in RHO0:
                fila = [inst[(rho0, ra, s)] for ra in RAPPORTI]
                soglia = next((RAPPORTI[i] for i in range(len(fila)) if all(fila[i:])), None) if any(fila) else None
                monot = (not any(fila)) or (soglia is not None and not any(fila[:RAPPORTI.index(soglia)]))
                soglie[(rho0, s)] = (soglia, monot)
                print("  rho_0 %g, s %g: instabile a %s; la soglia %s" % (rho0, s, [ra for ra in RAPPORTI if inst[(rho0, ra, s)]], soglia))
        if not any(inst.values()):
            print("  LA LETTURA: (m1) stabile in tutta la mappa: M-rho passa la prova lineare nella materia")
        elif all(inst.values()):
            print("  LA LETTURA: (m3) instabile in tutta la mappa: anche l'anello nella materia si chiude in fase. FERMO: la decisione e' di Luca")
        elif all(v[1] for v in soglie.values()):
            print("  LA LETTURA: (m2) instabile solo oltre una soglia di rho_0 / rho_c (sopra, per rho_0 e s)")
        else:
            print("  LA LETTURA: caso intermedio (nessuna di m1, m2, m3)")
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
