# -*- coding: utf-8 -*-
r"""**T6a: IL VALORE DI `e`, PERTURBATIVO** *(Luca `2026-11-07` `13:26`: l'energia elettrostatica del solitone maturo `~1%` della sua energia; il task history
`doc/TASK_HISTORY/2026-11-07_u1_prototipo_verificato.md` sez. `6`)*

    python csv/solitone/_u1_carica_e.py > doc/referti_l2/u1_carica_e.txt

### *(dal `2026-11-08` in `csv/solitone/`: la cassetta, `D6`, vuole che nessuno script FUORI importi la libreria; fino a `9e7cb734` era `csv/_u1_carica_e.py`)*

### **Lo stato maturo:** `db/accensione_lenta/TB3.npz` *(la fine di `TB3`, tick `200000`)*, **gli `sha` contro `sha_fine` dell'ultima riga** *(`R0`)*.
### **`E_sol = E[TB3] - E[0]`** *(il libro dei conti della corsa, `tot`, meno il vuoto `c(t) F3` allo stesso `t`)*; **`Q = somma rho`** *(la norma)*.
### **L'elettrostatica: Poisson sul toro con la trasformata** *(`PS`: a `L 12` = `lstsq` denso di `Campo.matrice_div` entro `1e-12`; `PS-F`: senza l'arco `a1 + a2`)*,
**`E = D^T lambda`, lo sfondo uniforme che neutralizza** *(sul toro una carica netta non ha campo: `somma div E = 0`)*.
### **`e = e_1 sqrt(0.01 / r_1)`** *(`e_1 = 1`, `r = K / E_sol`)*; **la formula di controllo `e^2 Q^2 ln(R/w) / 2 pi`.**
### **La verifica DINAMICA** *(le due statiche sono vere per costruzione: `K ~ e^2`, `B = 0` per un gradiente)*: **`N_DIN` tick dopo la rampa, il campo elettrostatico iniziale,
la sorgente, SENZA bordo**: `(K + V) / E_sol` *(`RD`: entro il `10%` di `0.01`, Luca)*, `max|e B_p|` *(`EB`: `<= 1` rad, Luca; se no FERMO)*,
Gauss *(`G5`: `div E - e (rho - mean)` costante entro `N 6 eps max|E| / (e max rho)`, la forma della stima della decisione `(1)` di Luca, per `E`)*, **`G5-F`** *(la sorgente spenta: deve fallire)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)   # ### dal 2026-11-08 in csv/solitone/ (D6); _u1_prototipo e gli strumenti in csv/
for _p in (_QUI, _CSV, os.path.join(os.path.dirname(_CSV), "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

RAPPORTO = 0.01        # ### Luca 13:26: l'energia elettrostatica ~1% di quella del solitone
TOLL_RD = 0.10         # ### Luca 13:26: entro il 10%
EB_MAX = 1.0           # ### Luca 13:26: max |e B_p| oltre 1 rad: FERMO
E_1 = 1.0              # ### il calcolo a e_1 (l'energia va come e^2)
N_DIN = 200            # ### i tick della verifica dinamica (mio, dichiarato: ~200 x 0.15 = 30 unita' di tempo)
L_PS = 12              # ### il toro piccolo del controllo PS
TOLL_PS = 1e-12
FORMA = "compatto"     # ### Luca 13:26
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-118s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))


def archi(L):
    """### Gli archi `3 v + a` del toro `L x L` come `Campo` li vuole: `a1`, `a2`, `a1 + a2`."""
    v = np.arange(L * L)
    m1, m2 = v // L, v % L

    def nb(d1, d2):
        return ((m1 + d1) % L) * L + (m2 + d2) % L
    jj = np.stack([nb(1, 0), nb(0, 1), nb(1, 1)], axis=1).reshape(-1)
    return np.repeat(v, 3), jj


def poisson(b, ii, jj, L, con_diag=True):
    """### `E = D^T lambda` con `D D^T lambda = b` *(il laplaciano del grafo sul toro, per trasformata)*; `b` a media nulla."""
    k = 2.0 * math.pi * np.fft.fftfreq(L)
    k1, k2 = k[:, None], k[None, :]
    autov = 6.0 - 2.0 * np.cos(k1) - 2.0 * np.cos(k2) - (2.0 * np.cos(k1 + k2) if con_diag else 0.0)
    if not con_diag:
        autov = autov - 2.0          # ### PS-F: il grado resta 6, ma senza l'arco a1 + a2 nei vicini (sbagliato apposta)
    B = np.fft.fft2(b.reshape(L, L))
    autov[0, 0] = 1.0
    lam = B / autov
    lam[0, 0] = 0.0
    lam = np.fft.ifft2(lam).real.reshape(-1)
    return lam[jj] - lam[ii]


def main():
    import _presidio
    _presidio.avvia(__file__)
    import _deriva_congelato as DC
    import _libro_dei_conti as LCO
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    import _u1_oggi as UO
    import _u1_prototipo as U1
    from solitone import bordo as BO
    from solitone import corsa_accensione as CA
    for m in ("_u1_oggi.py", "_u1_prototipo.py"):
        _presidio.avvia(os.path.join(_QUI if m == "_u1_oggi.py" else _CSV, m))
    print("=" * 130)
    print("T6a: IL VALORE DI e PERTURBATIVO (Luca 13:26): l'energia elettrostatica del solitone maturo di TB3 = %g della sua energia; forma %s; e_1 %g; N_DIN %d (mio)" % (RAPPORTO, FORMA, E_1, N_DIN))
    print("=" * 130)
    # ------------------------------------------------------------------ PS, PS-F
    ii, jj = archi(L_PS)
    c12 = U1.Campo(ii, jj, (L_PS, L_PS), 1.0, FORMA, np.ones(3 * L_PS * L_PS))
    rng = np.random.default_rng(1)
    b = rng.standard_normal(L_PS * L_PS)
    b -= b.mean()
    Ed = np.linalg.lstsq(c12.matrice_div(), b, rcond=None)[0]
    Ef = poisson(b, ii, jj, L_PS)
    Ef_f = poisson(b, ii, jj, L_PS, con_diag=False)
    ePS = float(np.max(np.abs(Ef - Ed)) / np.max(np.abs(Ed)))
    ePSF = float(np.max(np.abs(Ef_f - Ed)) / np.max(np.abs(Ed)))
    esito("DEVE PASSARE: PS a L %d Poisson per trasformata = lstsq denso di Campo.matrice_div entro %g relativo" % (L_PS, TOLL_PS), ePS <= TOLL_PS, "%.3e" % ePS)
    esito("DEVE FALLIRE: PS-F gli autovalori senza l'arco a1 + a2: entro %g" % TOLL_PS, not (ePSF <= TOLL_PS), "%.3e" % ePSF)
    # ------------------------------------------------------------------ lo stato maturo
    rr = CA.serie("TB3")[0]
    ult = rr[-1]
    e_K = rr[0]["e_K"]
    camp = ult["campioni"][-1]
    with np.load(os.path.join(CA.DIR_NPZ, "TB3.npz")) as d:
        t_st = int(d["t"])
        stT = {k: d[k].copy() for k in d.files if k != "t"}
    esito("DEVE PASSARE: R0 lo stato di TB3.npz (t %d) ha gli sha di ogni chiave = sha_fine dell'ultima riga" % t_st,
          t_st == ult["t1"] and all(SFM.sha(stT[k]) == v for k, v in ult["sha_fine"].items()), "chiavi %d" % len(ult["sha_fine"]))
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab_c, omega = d["c"].copy(), float(d["omega"])
    with UO.scena(E_1, FORMA) as (z, campo, K, s):
        st, mot, inc, L = z["st"], z["mot"], z["inc"], int(z["L"])
        assert set(stT) == {k for k, v in st.items() if isinstance(v, np.ndarray)}, "le chiavi dello stato NON sono quelle della scena"
        assert float(np.max(mot.cs) - np.min(mot.cs)) == 0.0, "cs NON e' uniforme: lstsq e il peso w di K non coincidono"
        phi_v = CA.vuoto_della_corsa(z, "TB3")
        assert np.array_equal(campo.ii, inc.nodo[0::2]) and np.array_equal(campo.jj, inc.nodo[1::2])
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            for k, v in stT.items():
                st[k][...] = v
            co = LCO.conti_per_nodo(inc, mot, st, e_K, V.LAM_ZERO, z["par"])
            E_T = {k: math.fsum(co[k].tolist()) for k in ("cin", "vuo", "leg", "cost", "tot")}
            st["psi_h"][...] = 0.0
            st["phi_h"][...] = BO.c_di(t_st, tab_c, K, omega) * phi_v
            E_0 = math.fsum(LCO.conti_per_nodo(inc, mot, st, e_K, V.LAM_ZERO, z["par"])["tot"].tolist())
            for k, v in stT.items():
                st[k][...] = v
        E_sol = E_T["tot"] - E_0
        rho = U1.rho_nodi(st, mot)
        Q = float(rho.sum())
        print("  l'energia (il libro della corsa, t %d): E[TB3] tot %.10e (cin %.6e vuo %.6e leg %.6e cost %.6e); il campione %.10e (relativa %.3e); E[0] il vuoto c(t) F3 %.10e"
              % (t_st, E_T["tot"], E_T["cin"], E_T["vuo"], E_T["leg"], E_T["cost"], camp["E"]["totale"]["tot"], E_T["tot"] / camp["E"]["totale"]["tot"] - 1.0, E_0))
        print("  E_sol = E[TB3] - E[0] = %.10e (l'energia che il solitone aggiunge al vuoto, dichiarata); Q = somma rho = %.10e (il campione M %.10e)" % (E_sol, Q, camp["E"]["totale"]["M"]))
        # -------------------------------------------------------------- l'elettrostatica a e_1, e
        b1 = E_1 * (rho - rho.mean())
        E1 = poisson(b1, campo.ii, campo.jj, L)
        res1 = float(np.max(np.abs(campo.div(E1) - b1)) / np.max(np.abs(b1)))
        campo.E[...] = E1
        K1 = campo.K()
        r1 = K1 / E_sol
        e = E_1 * math.sqrt(RAPPORTO / r1)
        print("  a e_1 %g: K %.6e, r_1 = K / E_sol %.6e; il residuo di Gauss |div E - e (rho - mean)| / max %.3e" % (E_1, K1, r1, res1))
        print("### e = e_1 sqrt(%g / r_1) = %.10e" % (RAPPORTO, e))
        campo.e = e
        campo.E[...] = poisson(e * (rho - rho.mean()), campo.ii, campo.jj, L)
        rs = campo.K() / E_sol
        print("  il rapporto statico a e: %.6e (= %g PER COSTRUZIONE: K ~ e^2, un falso-uno dichiarato); max|e B| statico %.3e (= 0 PER COSTRUZIONE: E e' un gradiente, A = 0)" % (rs, RAPPORTO, float(np.max(np.abs(e * campo.B())))))
        R, w = 0.5 * L, float(camp["w"])
        print("  la formula di controllo e^2 Q^2 ln(R/w) / 2 pi (R = L/2 = %g, w %.4f): %.6e, contro K %.6e (rapporto %.3f: solo l'ordine di grandezza)"
              % (R, w, e * e * Q * Q * math.log(R / w) / (2.0 * math.pi), campo.K(), (e * e * Q * Q * math.log(R / w) / (2.0 * math.pi)) / campo.K()))
        # -------------------------------------------------------------- la verifica dinamica
        E_init = campo.E.copy()
        risultati = {}
        for sorg in (True, False):
            for k, v in stT.items():
                st[k][...] = v
            campo.A[...] = 0.0
            campo.E[...] = E_init
            UO.scrivi_U(mot, campo)
            G0 = campo.div() - e * (rho - rho.mean())
            scala = e * float(np.max(rho))
            peg_G, peg_eB, rap, maxE = 0.0, 0.0, [], float(np.max(np.abs(campo.E)))
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                for j in range(N_DIN):
                    UO.tick(z, t_st + 1 + j, K, campo, sorg)
                    r_ = U1.rho_nodi(st, mot)
                    G = campo.div() - e * (r_ - r_.mean())
                    peg_G = max(peg_G, float(np.max(np.abs(G - G0))) / scala)
                    peg_eB = max(peg_eB, float(np.max(np.abs(e * campo.B()))))
                    rap.append((campo.K() + campo.V()) / E_sol)
                    maxE = max(maxE, float(np.max(np.abs(campo.E))))
            risultati[sorg] = (peg_G, peg_eB, np.array(rap), maxE / scala)
        peg_G, peg_eB, rap, maxE_rel = risultati[True]
        stima = N_DIN * 6.0 * np.finfo(float).eps * maxE_rel   # ### N tick x 6 archi per nodo x eps x max|E|, relativo a e max rho (la forma della stima di Luca, per E: mia, dichiarata)
        print("### la verifica dinamica (%d tick dopo la rampa da TB3 a t %d, il campo elettrostatico iniziale, la sorgente, SENZA bordo):" % (N_DIN, t_st))
        for j in (0, 9, 49, 99, N_DIN - 1):
            print("  il tick %4d: (K + V) / E_sol %.6e" % (j + 1, rap[j]))
        esito("DEVE PASSARE: RD (K + V) / E_sol all'ultimo tick entro il %g%% di %g (Luca)" % (100 * TOLL_RD, RAPPORTO), abs(rap[-1] / RAPPORTO - 1.0) <= TOLL_RD, "%.6e" % rap[-1])
        esito("DEVE PASSARE: EB max |e B_p| su tutti i tick <= %g rad (Luca: oltre, FERMO)" % EB_MAX, peg_eB <= EB_MAX, "%.3e" % peg_eB)
        esito("DEVE PASSARE: G5 Gauss div E - e (rho - mean) costante entro N 6 eps max|E| / (e max rho) = %.3e (la forma della stima di Luca, per E)" % stima, peg_G <= stima, "%.3e" % peg_G)
        esito("DEVE FALLIRE: G5-F la sorgente spenta: Gauss costante entro la stessa stima", not (risultati[False][0] <= stima), "%.3e" % risultati[False][0])
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
