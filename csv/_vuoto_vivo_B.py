# -*- coding: utf-8 -*-
r"""**IL SOLITONE SU `B` A `Gamma` COL TICK INTERO (IL VUOTO VIVO)** *(UNA PROVA, NESSUNA MODIFICA AL NUCLEO; il mandato di Luca delle `22:35` del `2026-10-31`;
[[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]], [[LIBRO-DEI-CONTI]], [[VUOTO-SUL-FONDO]]; il task history `doc/TASK_HISTORY/2026-11-01_vuoto_vivo_B.md`)*:
### **due solitoni dall'inviluppo** *(`BG`: `B` a `Gamma`, la scelta migliore a eps `0.5`; `AK`: `A` a `K`)*, ### **due vuoti** *(`U` uniforme, `F` il fondo `F0`)*, ### **il tick
INTERO** *(i `14` pezzi, `phi` non rimesso; `cs` spento)*: il cuore liscio e netto, la larghezza, l'alone, il baricentro, `Lambda`, le bande di `D`, il libro dei conti.

    python csv/_vuoto_vivo_B.py --controllo > doc/referti_l2/vuoto_vivo_B_controllo.txt
    python csv/_vuoto_vivo_B.py --corsa NOME          # un pezzo; si ripete finche' dice "finita"
    python csv/_vuoto_vivo_B.py --referto > doc/referti_l2/vuoto_vivo_B.txt
"""
import contextlib
import math
import os
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

import _consolida_B as CO                                      # noqa: E402

CB = CO.CB
MB = CB.MB
LP = CB.LP
N = CB.N                       # ### 1e6
L = CB.L                       # ### 81
EPS = CB.EPS_LUNGA             # ### 0.5
TAU_FINE = 3000.0              # ### il mandato: 3000 unita' di tempo
PEZZO = 10000                  # ### tick per pezzo (un processo)
OGNI = 10                      # ### il cuore, la larghezza, l'alone, il baricentro, Lambda, i conti per regione
OGNI_D = 20                    # ### le bande di D
META = 0.5                     # ### la dissoluzione: f_liscia sotto META del valore iniziale (il mandato)
R_VICINO = 2.0                 # ### il disco 2 w_in (_solitone_dal_fondo.R_VICINO)
LAM_ZERO = 0.5                 # ### lo zero dei conti (_solitone_dal_fondo.LAM_ZERO)
RAPPORTO = (3.0, 5.0)          # ### H_tot a O(s^2): il RAPPORTO dichiarato in _regime_del_passo.py (99eb7a42)
TOLL_NORMA = 1e-10             # ### M e V (_solitone_dal_fondo.TOLL_NORMA)
# ### il controllo positivo: lo stato di 15df5c63 (eps 0, vuoto uniforme, s 0.3), la vita ogni 20 tick = 320
S_RIF = 0.3
VITA_RIF = 320
OGNI_VITA_TAU = 6.0            # ### 20 tick a s 0.3 (_solitone_dal_fondo.OGNI_VITA_TAU)
CORSE = {                      # ### nome: (solitone, vuoto, s), nell'ordine di esecuzione
    "BG-U-0.15": ("BG", "uniforme", 0.15),
    "BG-F-0.15": ("BG", "fondo", 0.15),
    "AK-U-0.15": ("AK", "uniforme", 0.15),
    "AK-F-0.15": ("AK", "fondo", 0.15),
    "BG-U-0.075": ("BG", "uniforme", 0.075),
    "BG-F-0.075": ("BG", "fondo", 0.075),
}
DIR_JSON = os.path.join(RADICE, "doc", "referti_l2", "vuoto_vivo_B")
DIR_NPZ = os.path.join(RADICE, "db", "vuoto_vivo_B")
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


@contextlib.contextmanager
def scena(s, vuoto, eps):
    """### **Le righe di `_diagnosi_s4.iniziale` a questo `s`, col vuoto `vuoto`** *(`_deriva_congelato.nuovo`)* **e `eps` in memoria** *(come `_massimo_di_B.scena`)*."""
    import _deriva_congelato as DC
    import _diagnosi_s4 as D
    with D.configura(LP.FORMA, s, N):
        rec = DC.prepara(s)
        rec["fattore"] = (L - 0.1) / rec["larghezza"]
        z = DC.nuovo(rec, vuoto)
        assert z["L"] == L, (z["L"], L)
        z["par"]["eps"] = eps
        yield rec, z, z["st"]["phi_h"].copy(), z["st"]["psi_h"].copy()


def shas(z):
    import _stato_fermo as SFM
    return {k: SFM.sha(v) for k, v in sorted(z["st"].items()) if isinstance(v, np.ndarray)}


def e_K_di(z):
    """### **`e_K`: l'energia per norma dello stato uniforme di `A` a `K`** *(le righe di `_solitone_dal_fondo.prepara`)*."""
    import _scomposizione_solitone as SC
    incu, motu, stu = SC.stato_uniforme(z["L"], z["Q"], z["m1"], z["m2"])
    Eu, _a, _b, Mu, _c = SC.parti(incu, motu, stu)
    return Eu / Mu


def partenza(sol, z, phi0, pK, s):
    """### **(BG)** l'inviluppo per la scelta migliore a eps 0.5 *(theta, phi di `griglia.json`; la coppia ricalcolata su QUESTA scena)*; ### **(AK)** `pK`. ### `mu` di Rayleigh del tick congelato."""
    import _modo_al_variare_di_s as MS
    info = {}
    if sol == "BG":
        gr = LP.leggi(os.path.join(CB.DIR_JSON, "griglia.json"))[CO.NOME_EPS]
        th, fi = gr["minimo"]["theta"], gr["minimo"]["phi"]
        q1, q2, E0, G = CB.coppia(z, phi0)
        lam = np.linalg.eigvals(G)
        E = np.sort(-np.angle(lam) / s)
        q = math.cos(th) * q1 + np.exp(1j * fi) * math.sin(th) * q2
        p = CO.inviluppo(z, pK, q, N)
        info.update({"theta": th, "phi": fi, "E0": float(E0 * CB.S / s), "separazione": float(E[-2] - E[-3]), "degenere": float(E[-1] - E[-2]),
                     "bloch": float(np.linalg.norm(G @ q - np.exp(-1j * E0 * CB.S) * q))})
    else:
        p = pK.copy()
    T = MS.tick(z, phi0, p, LP.FORMA)
    lr = complex(np.vdot(p, T) / np.vdot(p, p))
    info["mu"] = -math.atan2(lr.imag, lr.real) / s
    info["residuo"] = float(np.linalg.norm(T - lr * p) / np.linalg.norm(p))
    return p, info


def misura(z, t, w_in, w0, h, LC, conti, mas):
    """### **Un campione:** il cuore liscio e netto, la larghezza, il baricentro *(`_salti_nel_cuore.campione`)*, l'alone `1 - f_3w0`, `Lambda` medio per regione, i conti per regione."""
    import _congelato_lungo as CL
    import _salti_nel_cuore as SN
    c, _rho, _d, _M = SN.campione(z, t, w_in, h)
    pt = CL.punto(z, t, w_in, w0)
    c["alone"] = 1.0 - pt["f_3w0"]
    E = LC.per_regione(conti, mas)
    c["lam_vicino"] = E["vicino"]["V"] / float(mas["vicino"].sum())
    c["lam_lontano"] = E["lontano"]["V"] / float(mas["lontano"].sum())
    c["E"] = E
    return c


def nomi(nome):
    pre = "%s_" % nome
    return sorted(n for n in os.listdir(DIR_JSON) if n.startswith(pre) and n.endswith(".jsonl")) if os.path.isdir(DIR_JSON) else []


def corsa(nome):
    """### **Un pezzo di `PEZZO` tick della corsa `nome`;** ### **la ripresa DEVE essere al bit** *(ogni chiave di `z["st"]`)*."""
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _libro_dei_conti as LC
    import _salti_nel_cuore as SN
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import composizione as CM
    import tick as TK
    sol, vuoto, s = CORSE[nome]
    t_fine = int(round(TAU_FINE / s))
    fatti = nomi(nome)
    testa = LP.leggi(os.path.join(DIR_JSON, fatti[0])) if fatti else None
    prec = LP.leggi(os.path.join(DIR_JSON, fatti[-1])) if fatti else None
    if prec is not None and (prec["t1"] >= t_fine or prec["t_dis"] is not None):
        print("  la corsa %s: finita (%d pezzi)" % (nome, len(fatti)))
        return 0
    os.makedirs(DIR_JSON, exist_ok=True)
    os.makedirs(DIR_NPZ, exist_ok=True)
    f_rip = os.path.join(DIR_NPZ, nome + ".npz")
    s0 = time.time()
    with scena(s, vuoto, EPS) as (rec, z, phi0, pK):
        w0 = rec["larghezza"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            w_in = DC.forma(z, w0)[0]
        h = SN.lunghezza_arco(z)
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        p0, info = partenza(sol, z, phi0, pK, s)
        e_K = e_K_di(z)
        ph, Z = DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        bande = LP.ML.Bande(Z, z["L"])
        for k, v in salvato.items():      # ### la partenza (il tick congelato di Rayleigh) non lascia niente nella scena
            z["st"][k][...] = v
        mu = info["mu"]
        if prec is None:
            t0 = 0
            z["st"]["psi_h"][...] = p0
        else:
            t0 = prec["t1"]
            with np.load(f_rip) as dati:
                assert int(dati["t"]) == t0
                for k in z["st"]:
                    if isinstance(z["st"][k], np.ndarray):
                        z["st"][k][...] = dati[k]
            assert shas(z) == prec["sha_fine"], "lo stato di ripresa NON e' la fine del pezzo prima (al bit, ogni chiave)"
            assert testa["info"]["mu"] == mu and testa["w_in"] == w_in, "la scena NON e' quella del primo pezzo"
        vic = z["rr"] <= R_VICINO * w_in
        mas = {"vicino": vic, "lontano": ~vic, "totale": np.ones(z["inc"].n, dtype=bool)}
        t1 = min(t0 + PEZZO, t_fine)
        camp, dd = [], []
        gpos, gneg = 0.0, 0.0
        t_dis = None
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            conti = LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, LAM_ZERO)
            prec_d2 = math.fsum(conti["tot"][vic].tolist())
            if t0 == 0:
                c = misura(z, 0, w_in, w0, h, LC, conti, mas)
                c["gA_pos"], c["gA_neg"] = 0.0, 0.0
                camp.append(c)
            f_lis0 = camp[0]["f_liscia"] if t0 == 0 else testa["campioni"][0]["f_liscia"]
            for t in range(t0 + 1, t1 + 1):
                TK.percorri_tick(z["st"], z["mot"], z["par"], (), None, len(CM.ORDINE))
                conti = LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, LAM_ZERO)
                d2 = math.fsum(conti["tot"][vic].tolist())
                g = d2 - prec_d2
                prec_d2 = d2
                if g > 0:
                    gpos += g
                else:
                    gneg += g
                if t % OGNI == 0:
                    c = misura(z, t, w_in, w0, h, LC, conti, mas)
                    c["gA_pos"], c["gA_neg"] = gpos, gneg
                    gpos, gneg = 0.0, 0.0
                    camp.append(c)
                    if c["f_liscia"] < META * f_lis0:
                        t_dis = t
                if t % OGNI_D == 0:
                    D = np.exp(1j * mu * s * t) * z["st"]["psi_h"] - p0
                    cf = bande.coeff(D)
                    pk = np.abs(cf) ** 2
                    tot = float(pk.sum())
                    dd.append({"t": t, "nD": float(np.linalg.norm(D)) / float(np.linalg.norm(p0)), "bande": {gn: float(pk[..., list(idx)].sum()) / tot for gn, idx in bande.gruppi.items()}})
                if t_dis is not None:
                    t1 = t
                    break
        sha_fine = shas(z)
        tmp = f_rip.replace(".npz", "_tmp.npz")
        np.savez(tmp, t=t1, **{k: v for k, v in z["st"].items() if isinstance(v, np.ndarray)})
    os.replace(tmp, f_rip)
    riga = {"nome": nome, "sol": sol, "vuoto": vuoto, "s": s, "eps": EPS, "N": N, "L": L, "t0": t0, "t1": t1, "t_fine": t_fine, "t_dis": t_dis,
            "w_in": w_in, "h": h, "e_K": e_K, "info": info, "campioni": camp, "D": dd, "sha_fine": sha_fine, "secondi": time.time() - s0}
    LP.scrivi_nuovo(os.path.join(DIR_JSON, "%s_%06d.jsonl" % (nome, t0)), riga)
    fl = camp[-1]["f_liscia"]
    print("  la corsa %s: il pezzo %d -> %d%s; f_liscia %.5f (all'inizio %.5f), w %.4f, alone %.5f; mu %+.6f; %.0f s"
          % (nome, t0, t1, ", SCIOLTO (f_liscia sotto meta')" if t_dis is not None else "", fl, f_lis0, camp[-1]["w"], camp[-1]["alone"], mu, time.time() - s0))
    return 0


def controllo():
    """### **(0)** la scena `(U, s 0.15)` = `_massimo_di_B.scena` al bit; `F0` = `fondo_uniforme` al bit; ### **la vita `320` dello stato di `15df5c63` col MIO tick intero.**"""
    import _controllo_matrice as CM_
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _solitoni_triangoli as STR
    import _triangoli_bassa_energia as BE
    import _vuoto_sul_fondo as VSF
    import composizione as CM
    import scena_l2 as SL
    import tick as TK
    print("=" * 130)
    print("IL VUOTO VIVO SU B A Gamma (Luca 22:35): IL CONTROLLO -- le scene al bit, il vuoto F0, la vita di 15df5c63 col tick intero di questo script")
    print("  la configurazione: N %.0e L %d EPS %g TAU_FINE %g PEZZO %d OGNI %d OGNI_D %d META %g R_VICINO %g LAM_ZERO %g RAPPORTO %s TOLL_NORMA %g S_RIF %g VITA_RIF %d OGNI_VITA_TAU %g; CORSE %s; FORMA %s; cs spento (EL.stato: mot.cs costante = s, lambda_c None; tick.percorri_tick)"
          % (N, L, EPS, TAU_FINE, PEZZO, OGNI, OGNI_D, META, R_VICINO, LAM_ZERO, RAPPORTO, TOLL_NORMA, S_RIF, VITA_RIF, OGNI_VITA_TAU, CORSE, LP.FORMA))
    print("=" * 130)
    with MB.scena(N, L, EPS) as (_r, z, _ph, _p):
        a = CM_.istantanea(z)
        ea = z["par"]["eps"]
    with scena(CB.S, "uniforme", EPS) as (_r, z, _ph, _p):
        b = CM_.istantanea(z)
        eb = z["par"]["eps"]
        assert z["mot"].lambda_c is None and np.all(z["mot"].cs == CB.S)
    c = CM_.confronta(a, b)
    esito("DEVE PASSARE: la scena (U, s %g, eps %g) di questo script = _massimo_di_B.scena, AL BIT, ogni chiave" % (CB.S, EPS), all(v[0] for v in c.values()) and ea == eb, " ".join(sorted(c)))
    with scena(CB.S, "fondo", EPS) as (_r, z, _ph, _p):
        f0 = VSF.fondo_uniforme(z["inc"], L, SL.VUOTO_PER_ESTREMITA)[0]
        esito("DEVE PASSARE: il vuoto (F) della scena = _vuoto_sul_fondo.fondo_uniforme (F0), AL BIT", z["st"]["phi_h"].tobytes() == f0.tobytes(), "")
    print("### IL CONTROLLO POSITIVO DEL TICK INTERO: lo stato di 15df5c63 (eps 0, il vuoto uniforme, s %g); la vita col criterio di _solitoni_triangoli, ogni %d tick" % (S_RIF, int(round(OGNI_VITA_TAU / S_RIF))))
    ogni_vita = int(round(OGNI_VITA_TAU / S_RIF))
    vita = None
    s0 = time.time()
    with scena(S_RIF, "uniforme", 0.0) as (rec, z, _ph, _p):
        w0 = rec["larghezza"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            w_in = DC.forma(z, w0)[0]
            for t in range(1, int(round(600.0 / S_RIF)) + 1):
                TK.percorri_tick(z["st"], z["mot"], z["par"], (), None, len(CM.ORDINE))
                if t % ogni_vita == 0:
                    w, fr = DC.forma(z, w0)[:2]
                    if abs(w / w_in - 1.0) > STR.TOLL_LARGH or fr < STR.FRAZ_MIN:
                        vita = t
                        break
    esito("DEVE PASSARE: la vita (ogni %d tick) = %d di 15df5c63" % (ogni_vita, VITA_RIF), vita == VITA_RIF, "vita %s (%.0f s)" % (vita, time.time() - s0))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--controllo" in argv:
        controllo()
    elif "--corsa" in argv:
        sys.exit(corsa(argv[argv.index("--corsa") + 1]))
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
