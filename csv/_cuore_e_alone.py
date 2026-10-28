# -*- coding: utf-8 -*-
r"""**IL CUORE E L'ALONE DEL CONGELATO LUNGO** *(la risposta di Luca delle `18:12` del `2026-10-28` a `40061005`; [[VUOTO-SUL-FONDO]], [[PROGETTO-MASSA-COLLETTIVA]];
il task history `doc/TASK_HISTORY/2026-10-28_cuore_e_alone.md`)*: ### **nessuna corsa: i punti di `doc/referti_l2/congelato_lungo/` e gli stati finali di `db/congelato_lungo/`.**
### **(a)** il cuore *(`f_win M`)* e l'alone *(`(1 - f_3w0) M`)* nel tempo; ### **(b)** la FWHM; ### **(c)** il profilo radiale medio, all'inizio e alla fine;
### **(d)** il cuore finale contro il solitone del risolutore alla norma del cuore *(stessa `s`, stessa `c`)*, proiettato sullo stesso toro.

> ### **Gli stati finali** *(tick `10000`)* **vengono da `python csv/_congelato_lungo.py --pezzo <L> <scena>`, ripetuto** *(il dato e' il comando)*;
> ### **lo stato iniziale si ricostruisce con `_congelato_lungo.iniziale`.**

    python csv/_cuore_e_alone.py --referto > doc/referti_l2/cuore_e_alone.txt
"""
import hashlib
import io
import json
import math
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

SCENA = "uniforme"             # ### gli .npz di 'uniforme' e 'fondo' sono identici al byte: si controlla, e si analizza uno
ANELLO = 1.0                   # ### la larghezza degli anelli del profilo radiale
R_PROFILO = 30                 # ### i raggi stampati del profilo
FINESTRA = 500.0
TOLL_SCALA = 0.02              # ### il controllo di scala: lo stato iniziale contro il risolutore a N = M (la tolleranza di un controllo)
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


def baricentro(z, rho):
    M = float(rho.sum())
    c = (rho @ z["pos"]) / M
    d = np.hypot(z["pos"][:, 0] - c[0], z["pos"][:, 1] - c[1])
    return M, c, d


def anelli(rho, d):
    """### **Il profilo radiale medio:** ### **la media di `rho` per nodo negli anelli `[k, k+1)`.**"""
    k = np.floor(d / ANELLO).astype(int)
    somma = np.bincount(k, weights=rho)
    quanti = np.bincount(k)
    prof = np.full(len(somma), np.nan)
    v = quanti > 0
    prof[v] = somma[v] / quanti[v]
    return prof


def fwhm(prof):
    """### **`2 r_1/2`:** ### **`r_1/2` dove il profilo per anelli scende a meta' del primo anello, per interpolazione lineare fra i centri degli anelli.**"""
    meta = 0.5 * prof[0]
    for k in range(1, len(prof)):
        if prof[k] <= meta:
            r0, r1 = (k - 0.5) * ANELLO, (k + 0.5) * ANELLO
            return 2.0 * (r0 + (prof[k - 1] - meta) / (prof[k - 1] - prof[k]) * (r1 - r0))
    return float("nan")


def risolutore(rec, Nn):
    """### **Il risolutore a `N` con la `s` e la `c` di `rec`** *(le righe di `_deriva_congelato.prepara`)* ### **e il suo profilo sul toro** *(le righe di `_energia_del_legame.stato`)*."""
    import _modi_pi_e_solitoni as MPS
    import _solitoni_triangoli as STR
    import _solitone_vuoto_congelato as VC
    vero = MPS.LAM0
    MPS.LAM0 = STR.LAM0_TRI
    try:
        ls = MPS.largo(VC.FORMA, rec["c"], VC.S, Nn)
    finally:
        MPS.LAM0 = vero
    q, r, u = STR.profilo_u(VC.FORMA, rec["c"], VC.S, Nn, STR.LAM0_TRI, ls["larghezza"])
    return ls, q, r, u


def sul_toro(z, r, u, Nn):
    """### **Il profilo `u(r)` sul toro, centrato nell'origine e rinormalizzato a `Nn`** *(come `_energia_del_legame.stato`)*: ### **`rho` per nodo.**"""
    import _solitoni_triangoli as STR
    g = np.interp(z["rr"], r, u, right=0.0) * math.sqrt(STR.AREA_NODO)
    rho = g * g
    return rho * (Nn / float(rho.sum()))


def finale(L, scena):
    import _congelato_lungo as CL
    rec, z = CL.iniziale(L, scena)
    rho0 = __import__("_energia_del_legame").densita(z["inc"], z["st"])[0].copy()
    dati = np.load(os.path.join(CL.STATI, CL.nome(L, scena) + ".npz"))
    z["st"]["psi_h"][...] = dati["psi_h"]
    return rec, z, rho0, int(dati["t"])


def serie_a(L):
    import _congelato_lungo as CL
    righe, pts = CL.serie(L, SCENA)
    w_in = righe[0]["w_in"]
    print("### (a) L %d: il cuore = f_win M (entro w_in %.4f), l'alone = (1 - f_3w0) M (oltre 3 w0 = %.4f), in frazione di M; %d punti" % (L, w_in, 3.0 * righe[0]["w0"], len(pts)))
    tau = np.array([p["tau"] for p in pts])
    cu = np.array([p["f_win"] for p in pts])
    al = np.array([1.0 - p["f_3w0"] for p in pts])
    a = 0.0
    while a < tau[-1] - 1e-9:
        m = (tau >= a - 1e-9) & (tau <= a + FINESTRA + 1e-9)
        pc = np.polyfit(tau[m], cu[m], 1)[0]
        pa = np.polyfit(tau[m], al[m], 1)[0]
        print("  tau [%6.0f, %6.0f]: cuore medio %.5f (da %.5f a %.5f), pendenza %+.3e; alone medio %.5f (da %.5f a %.5f), pendenza %+.3e; fra w_in e 3 w0 medio %.5f"
              % (a, a + FINESTRA, cu[m].mean(), cu[m][0], cu[m][-1], pc, al[m].mean(), al[m][0], al[m][-1], pa, (1.0 - cu[m] - al[m]).mean()))
        a += FINESTRA
    return righe, pts


def referto():
    import _congelato_lungo as CL
    import _energia_del_legame as EL
    import _solitoni_triangoli as STR
    print("=" * 130)
    print("IL CUORE E L'ALONE DEL CONGELATO LUNGO (Luca 18:12, a 40061005): N 1e6, s %g, zero simmetrico, S1, cs spento, il congelato vero; nessuna corsa nuova" % CL.S)
    print("=" * 130)
    print("  la configurazione: SCENA %s ANELLO %g R_PROFILO %d FINESTRA %g TOLL_SCALA %g; TAGLIE %s, T_MAX %d" % (SCENA, ANELLO, R_PROFILO, FINESTRA, TOLL_SCALA, CL.TAGLIE, CL.T_MAX))
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: cuore fermo + alone che cresce + FWHM che resta o cala = STABILE e irradia; cuore che cala senza fermarsi = si svuota; (d): il cuore e' gia' l'oggetto stazionario?")
    for L in CL.TAGLIE:
        print("-" * 130)
        f_u = os.path.join(CL.STATI, CL.nome(L, "uniforme") + ".npz")
        f_f = os.path.join(CL.STATI, CL.nome(L, "fondo") + ".npz")
        esito("DEVE PASSARE: L %d, gli stati finali 'uniforme' e 'fondo' identici al byte" % L, io.open(f_u, "rb").read() == io.open(f_f, "rb").read(), "")
        righe, pts = serie_a(L)
        rec, z, rho0, t = finale(L, SCENA)
        esito("DEVE PASSARE: L %d, lo stato finale e' quello del tick %d (sha1 = sha_fine del pezzo %05d)" % (L, CL.T_MAX, righe[-1]["t0"]),
              t == CL.T_MAX and CL.sha(z["st"]["psi_h"]) == righe[-1]["sha_fine"], "t %d" % t)
        w_in, w0 = righe[0]["w_in"], righe[0]["w0"]
        p = CL.punto(z, t, w_in, w0)
        esito("DEVE PASSARE: L %d, il punto ricalcolato dallo stato finale = l'ultimo punto del jsonl, AL BIT" % L,
              all(p[k] == pts[-1][k] for k in ("w", "f_win", "f_3w0", "picco", "M")), "")
        rho1 = EL.densita(z["inc"], z["st"])[0]
        M0, c0, d0 = baricentro(z, rho0)
        M1, c1, d1 = baricentro(z, rho1)
        pr0, pr1 = anelli(rho0, d0), anelli(rho1, d1)
        # ### (d) e il controllo di scala: il risolutore a N = M e a N = il cuore finale, proiettato sullo stesso toro
        _ls, _q, r_M, u_M = risolutore(rec, M0)
        rs_M = sul_toro(z, r_M, u_M, M0)
        _Ms, _cs, ds_M = baricentro(z, rs_M)
        prs_M = anelli(rs_M, ds_M)
        N_c = pts[-1]["f_win"] * M1
        ls, q, r_c, u_c = risolutore(rec, N_c)
        rs_c = sul_toro(z, r_c, u_c, N_c)
        _Mc, _cc, ds_c = baricentro(z, rs_c)
        prs_c = anelli(rs_c, ds_c)
        f0, fM = fwhm(pr0), fwhm(prs_M)
        esito("DEVE PASSARE (scala): L %d, lo stato iniziale contro il risolutore a N = M: FWHM e picco entro %g" % (L, TOLL_SCALA),
              abs(f0 / fM - 1.0) <= TOLL_SCALA and abs(rho0.max() / rs_M.max() - 1.0) <= TOLL_SCALA,
              "FWHM %.4f contro %.4f; picco %.2f contro %.2f" % (f0, fM, rho0.max(), rs_M.max()))
        print("### (b) L %d: la FWHM all'inizio %.4f, alla fine %.4f (rapporto %.4f); il picco per nodo %.2f e %.2f (rapporto %.4f); il baricentro finale (%+.2e, %+.2e)"
              % (L, f0, fwhm(pr1), fwhm(pr1) / f0, rho0.max(), rho1.max(), rho1.max() / rho0.max(), c1[0], c1[1]))
        print("### (d) L %d: il cuore finale N_c = %.1f (%.5f M); il risolutore a N_c: %s, larghezza %.4f (a N = M: %.4f), mu %+.6f; la sua frazione entro w_in sul toro %.5f"
              % (L, N_c, N_c / M1, ls["verdetto"], ls["larghezza"], rec["larghezza"], ls["mu"], float(rs_c[ds_c <= w_in].sum()) / N_c))
        print("  FWHM: il cuore finale %.4f, il risolutore a N_c %.4f (rapporto %.4f); il picco per nodo: %.2f contro %.2f (rapporto %.4f); rho_centro AREA_NODO del risolutore %.2f"
              % (fwhm(pr1), fwhm(prs_c), fwhm(pr1) / fwhm(prs_c), rho1.max(), rs_c.max(), rho1.max() / rs_c.max(), q["rho_centro"] * STR.AREA_NODO))
        print("### (c) L %d: il profilo radiale medio per anelli [r, r+%g): l'inizio, la fine, il risolutore a N = M e a N_c (rho per nodo)" % (L, ANELLO))
        for k in range(min(R_PROFILO + 1, len(pr1))):
            print("  r %3d: inizio %12.5e   fine %12.5e   ris(M) %12.5e   ris(N_c) %12.5e   fine/inizio %10.3e   fine/ris(N_c) %10.3e"
                  % (k, pr0[k], pr1[k], prs_M[k], prs_c[k], pr1[k] / pr0[k] if pr0[k] > 0 else float("nan"), pr1[k] / prs_c[k] if prs_c[k] > 0 else float("nan")))
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import _solitone_vuoto_congelato as VC
    s_vero = VC.S
    try:
        if argv[:1] == ["--referto"]:
            referto()
        else:
            raise SystemExit(__doc__)
    finally:
        VC.S = s_vero
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
