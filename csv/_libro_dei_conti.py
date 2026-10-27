# -*- coding: utf-8 -*-
r"""**IL LIBRO DEI CONTI DELL'ENERGIA** *([[LIBRO-DEI-CONTI]]; `doc/LIBRO_DEI_CONTI.md`; il task history `doc/TASK_HISTORY/2026-10-27_libro_dei_conti_strumento.md`)*:
### **i conti per nodo** *(i costituenti, la cinetica, il legame `S1`, il vuoto, `H_tot`, `M`, `V`)* ### **sommati per regione con `math.fsum`;** ### **la strada `A`**
*(il guadagno netto di dischi annidati, tick per tick: entrate e uscite separate)* ### **come strumento; la strada `B`** *(il conto dopo ogni pezzo del tick, da una copia:
`tick.percorri_tick(..., quanti = k)`)* ### **come diagnosi del va-e-vieni del passo.** ### **Il `main` gira i sigilli `(i)`-`(iv)` e `(B)`.**

> ### **Si usa come libreria:** `conti_per_nodo`, `per_regione`, `dischi`, `guadagni_A`, `pezzi_B`. ### **Il legame e' quello ATTIVO** *(`S1` dentro `_screening_forme_s3.forma("S1")`)*: ### **chi chiama lo dichiara.**
> ### **In memoria; nessun file del nucleo.** ### **Importati, non copiati:** `_energia_del_legame` *(`stato`, `per_nodo`, `densita`)*, `_scomposizione_solitone` *(`F1`, `stato_uniforme`, `parti`)*,
> `_solitone_vuoto_congelato` *(`S`, `FORMA`)*, `_solitoni_triangoli`, `_modi_pi_e_solitoni.largo`, `_screening_forme_s3.forma`, `_triangoli_bassa_energia.conv`, `tick.percorri_tick`.

Gira con:  python csv/_libro_dei_conti.py > doc/referti_l2/libro_dei_conti.txt
"""
import io
import json
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

CONTI = ("cost", "cin", "leg", "vuo", "tot", "M", "V")
RIF = os.path.join(RADICE, "doc", "referti_l2", "energia_del_legame.jsonl")
JSONL = os.path.join(RADICE, "doc", "referti_l2", "libro_dei_conti.jsonl")
N_RIF = 1e5
FATTORE = 12.0
ZERO = "simm"
LAM_ZERO = 0.5
R_VICINO = 2.0                 # ### VICINO di `15df5c63`
RAGGI = (1.0, 2.0, 3.0, 4.0)   # ### i dischi annidati, in unita' di `w_in`
T_MAX = 2000
OGNI = 10                      # ### il campionamento di `energia_del_legame.jsonl`
VITA = 140                     # ### la vita di `N 1e5` (`vita20`, il mandato)
T_VUOTO = 200
T_B = 200
OGNI_B = 10
S_PASSI = (0.3, 0.15)
TOLL_I = 1e-12
TOLL_II = 1e-6
TOLL_III = 1e-12
RAPPORTO_ATTESO = 4.0
TOLL_IV = 0.2
OK = [0, 0]
FALLITE = []


# ---------------------------------------------------------------------------------------------------------------- la libreria
def conti_per_nodo(inc, mot, st, e_K, lam_z):
    """### **I conti per nodo** *(gli array prima della somma)*: ### **come `_energia_del_legame.energie`, nodo per nodo** *(il legame `S1`; `+ 2 pi lambda` per unita' di norma)*."""
    import _energia_del_legame as EL
    import _scomposizione_solitone as SC
    rho, lam = EL.densita(inc, st)
    assert np.all(lam > 0.0), "Lambda nullo in un nodo: il legame S1 non e' definito"
    em = EL.per_nodo(inc, mot, st, "phi_h") + 2 * math.pi * lam_z * rho
    ev = EL.per_nodo(inc, mot, st, "psi_h") + 2 * math.pi * lam_z * lam
    el = lam * SC.F1(rho / lam)
    ec = rho * (e_K + 2 * math.pi * lam_z)
    return {"cost": ec, "cin": em - ec, "leg": el, "vuo": ev, "tot": em + ev + el, "M": rho, "V": lam}


def per_regione(conti, maschere):
    """### **Le somme per regione con `math.fsum`** *(la somma esatta, arrotondata una volta)*: `{regione: {conto: valore}}`."""
    return {nome: {c: math.fsum(conti[c][m].tolist()) for c in CONTI} for nome, m in maschere.items()}


def dischi(rr, w, raggi):
    """### **I dischi annidati** `r <= k w` ### **e il toro intero.**"""
    out = {"disco_%g" % k: rr <= k * w for k in raggi}
    out["toro"] = np.ones(len(rr), dtype=bool)
    return out


def guadagni_A(serie, nomi):
    """### **La strada `A`:** ### **per ogni disco il guadagno netto di `H_tot` fra due tick consecutivi della serie;** ### **le entrate e le uscite separate** *(i tick positivi e negativi)*."""
    out = {}
    for d in nomi:
        g = [b[1][d]["tot"] - a[1][d]["tot"] for a, b in zip(serie[:-1], serie[1:])]
        t = [b[0] for b in serie[1:]]
        out[d] = (t, g)
    return out


def pezzi_B(inc, mot, st, par, maschere, e_K, lam_z, quanti_tot):
    """### **La strada `B`:** ### **da una COPIA dello stato, il conto per regione dopo `k` pezzi, `k = 0 .. quanti_tot`** *(`tick.percorri_tick(copia, ..., quanti = k)`)*; ### **lo stato vero non si muove.**"""
    import tick as TK
    out, fine = [], None
    for k in range(quanti_tot + 1):
        copia = {kk: (v.copy() if hasattr(v, "copy") else v) for kk, v in st.items()}
        if k:
            TK.percorri_tick(copia, mot, par, (), None, k)
        out.append(per_regione(conti_per_nodo(inc, mot, copia, e_K, lam_z), maschere))
        fine = copia
    return out, fine


# ---------------------------------------------------------------------------------------------------------------- i sigilli
def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if deve and not passa:
        FALLITE.append(che)
    print("  %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scrivi(r):
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def scena(rec, senza_materia):
    import _energia_del_legame as EL
    L, inc, mot, st, par, pos, rr, Q, m1, m2, r_mat = EL.stato(N_RIF, FATTORE, rec)
    if senza_materia:   # ### la scena di `N 1e5`, la materia a zero (il profilo non si risolve a norma zero)
        st["psi_h"][...] = 0.0
    rho, _l = EL.densita(inc, st)
    M = float(rho.sum())
    w = None
    if M > 0:   # ### la larghezza come `_energia_del_legame.corsa.forma_m`
        cm = (rho @ pos) / M
        w = math.sqrt(float(rho @ np.sum((pos - cm) ** 2, axis=1)) / M)
    return L, inc, mot, st, par, rr, w


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import _modi_pi_e_solitoni as MPS
    import _scomposizione_solitone as SC
    import _screening_forme_s3 as SF
    import _solitoni_triangoli as STR
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import composizione as CM
    import tick as TK
    _presidio.avvia(__file__)
    print("=" * 130)
    print("IL LIBRO DEI CONTI DELL'ENERGIA: i conti per nodo sommati per regione (fsum); la strada A (dischi annidati, entrate e uscite nel tempo) e la B (pezzo per pezzo, diagnosi); i sigilli")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_libro_dei_conti.py", "csv/_energia_del_legame.py", "csv/_scomposizione_solitone.py", "csv/_solitone_vuoto_congelato.py",
                                     "primo_ordine/energia_pesata.py", "primo_ordine/tick.py", "doc/referti_l2/energia_del_legame.jsonl")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: N_RIF %g FATTORE %g ZERO %s LAM_ZERO %g R_VICINO %g RAGGI %s T_MAX %d OGNI %d VITA %d T_VUOTO %d T_B %d OGNI_B %d S_PASSI %s TOLL_I %g TOLL_II %g TOLL_III %g RAPPORTO_ATTESO %g TOLL_IV %g"
          % (N_RIF, FATTORE, ZERO, LAM_ZERO, R_VICINO, RAGGI, T_MAX, OGNI, VITA, T_VUOTO, T_B, OGNI_B, S_PASSI, TOLL_I, TOLL_II, TOLL_III, RAPPORTO_ATTESO, TOLL_IV))
    print("  il legame S1 (in memoria, _screening_forme_s3.forma); cs SPENTO; lo zero simmetrico (BE.conv('simm')); le energie a zero lambda: + 2 pi lambda per unita' di norma, materia e vuoto")
    print("-" * 130)
    if os.path.exists(JSONL):
        os.remove(JSONL)
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    vero = MPS.LAM0
    MPS.LAM0 = STR.LAM0_TRI
    try:
        cc, _cy, _w0 = STR.c_triangoli(VC.S)
        rec = {"larghezza": MPS.largo(VC.FORMA, cc, VC.S, N_RIF)["larghezza"], "c": cc}
    finally:
        MPS.LAM0 = vero
    L, inc, mot, st, par, rr, w = scena(rec, False)
    _L, _i, _m, _s, _p, _pos, _rr, Q, m1, m2, _r = __import__("_energia_del_legame").stato(N_RIF, FATTORE, rec)
    incu, motu, stu = SC.stato_uniforme(L, Q, m1, m2)
    Eu, _a, _b, Mu, _c = SC.parti(incu, motu, stu)
    e_K = Eu / Mu
    sc = N_RIF * abs(e_K)
    print("  N %g L %d: w_in %.4f; e_K(0) %+.6f; l'unita' N |e_K(0)| = %.6e" % (N_RIF, L, w, e_K, sc))
    print("-" * 130)

    # ------------------------------------------------------------------------------------------------ (i)
    print("### (i) IL VUOTO UNIFORME SENZA MATERIA: il guadagno netto di ogni disco per %d tick (i dischi del solitone, w_in %.4f)" % (T_VUOTO, w))
    _L0, inc0, mot0, st0, par0, rr0, _w0 = scena(rec, True)
    mas0 = dischi(rr0, w, RAGGI)
    serie0 = []
    peg0, scala0 = 0.0, 0.0
    with SF.forma(VC.FORMA), BE.conv(ZERO):
        for t in range(T_VUOTO + 1):
            c0 = conti_per_nodo(inc0, mot0, st0, e_K, LAM_ZERO)
            scala0 = max(scala0, math.fsum(np.abs(c0["tot"]).tolist()))
            serie0.append((t, per_regione(c0, mas0)))
            if t < T_VUOTO:
                TK.percorri_tick(st0, mot0, par0, (), None, len(CM.ORDINE))
    for d, (_t, g) in guadagni_A(serie0, list(mas0)).items():
        peg0 = max(peg0, max(abs(x) for x in g))
    print("  il guadagno netto massimo %.3e; sum_k |e_tot,k| %.6e" % (peg0, scala0))
    esito("DEVE PASSARE (i): sul vuoto uniforme il guadagno netto di ogni disco a ogni tick entro %g di sum_k |e_tot,k|" % TOLL_I, peg0 <= TOLL_I * scala0, "%.3e (soglia %.3e)" % (peg0, TOLL_I * scala0))
    scrivi({"tipo": "vuoto", "guadagno_max": peg0, "scala": scala0})
    print("-" * 130)

    # ------------------------------------------------------------------------------------------------ (ii), (iii), A
    rif = None
    for l in io.open(RIF, encoding="utf-8"):
        d = json.loads(l)
        if d.get("tipo") == "corsa" and d["N"] == N_RIF and d["L"] == L and d["zero"] == ZERO and d["modo"] == "intero":
            rif = d
    assert rif is not None, "la corsa di riferimento manca in %s" % RIF
    mas = {"vicino": rr <= R_VICINO * w, "lontano": rr > R_VICINO * w}
    mas_t = dict(mas, totale=np.ones(inc.n, dtype=bool))
    dsc = dischi(rr, w, RAGGI)
    print("### (ii) I CONTI PER REGIONE CONTRO energia_del_legame.jsonl (N %g L %d simm intero), ogni %d tick fino a %d" % (N_RIF, L, OGNI, T_MAX))
    rif_t = {x["t"]: x["E"] for x in rif["serie"]}
    peg2, dove2 = 0.0, ""
    peg3a, peg3b = 0.0, 0.0
    serieA = []
    h0 = None
    t0 = time.time()
    with SF.forma(VC.FORMA), BE.conv(ZERO):
        for t in range(T_MAX + 1):
            c = conti_per_nodo(inc, mot, st, e_K, LAM_ZERO)
            rd = per_regione(c, dsc)
            serieA.append((t, rd))
            if h0 is None:
                h0 = rd["toro"]["tot"]
            if t % OGNI == 0:
                rg = per_regione(c, mas_t)
                for reg in ("vicino", "lontano", "totale"):
                    for k in CONTI:
                        x = abs(rg[reg][k] - rif_t[t][reg][k]) / sc
                        if x > peg2:
                            peg2, dove2 = x, "t %d %s %s" % (t, reg, k)
                for k in CONTI:
                    peg3a = max(peg3a, abs(rg["vicino"][k] + rg["lontano"][k] - rg["totale"][k]) / sc)
                if t:
                    anelli = 0.0
                    prec = serieA[-1 - OGNI][1] if len(serieA) > OGNI else serieA[0][1]
                    nomi = list(dsc)
                    for i, dn in enumerate(nomi):
                        a_ora = rd[dn]["tot"] - (rd[nomi[i - 1]]["tot"] if i else 0.0)
                        a_prima = prec[dn]["tot"] - (prec[nomi[i - 1]]["tot"] if i else 0.0)
                        anelli += a_ora - a_prima
                    peg3b = max(peg3b, abs(anelli - (rd["toro"]["tot"] - prec["toro"]["tot"])) / sc)
            if t < T_MAX:
                TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
    print("  il peggiore %.3e (%s) (%.0f s)" % (peg2, dove2, time.time() - t0))
    esito("DEVE PASSARE (ii): i conti per regione = energia_del_legame.jsonl entro %g di N |e_K(0)|" % TOLL_II, peg2 <= TOLL_II, "%.3e (%s)" % (peg2, dove2))
    scrivi({"tipo": "riferimento", "peggiore": peg2, "dove": dove2})
    dev_vita = max(abs(x[1]["toro"]["tot"] - h0) for x in serieA if x[0] <= VITA)
    print("-" * 130)

    # ------------------------------------------------------------------------------------------------ (iv)
    print("### (iv) L'ERRORE DEL PASSO: max |H_tot(t) - H_tot(0)| per s t <= %g, a s %s (lo stesso stato iniziale, mot.cs = s)" % (S_PASSI[0] * VITA, S_PASSI))
    dev = {}
    for s in S_PASSI:
        _L1, inc1, mot1, st1, par1, rr1, _w1 = scena(rec, False)
        mot1.cs = np.full(inc1.n, s)
        n_t = int(round(S_PASSI[0] * VITA / s))
        tutto = np.ones(inc1.n, dtype=bool)
        with SF.forma(VC.FORMA), BE.conv(ZERO):
            hh = []
            for t in range(n_t + 1):
                hh.append(math.fsum(conti_per_nodo(inc1, mot1, st1, e_K, LAM_ZERO)["tot"][tutto].tolist()))
                if t < n_t:
                    TK.percorri_tick(st1, mot1, par1, (), None, len(CM.ORDINE))
        dev[s] = max(abs(x - hh[0]) for x in hh)
        print("  s %g: %d tick; max |H_tot(t) - H_tot(0)| %.6e = %.3e N |e_K(0)|" % (s, n_t, dev[s], dev[s] / sc))
    rap = dev[S_PASSI[0]] / dev[S_PASSI[1]] if dev[S_PASSI[1]] > 0 else math.inf
    esito("DEVE PASSARE (iv): l'errore del passo va come s^2: il rapporto s %g / s %g entro %g +- %g%%" % (S_PASSI[0], S_PASSI[1], RAPPORTO_ATTESO, 100 * TOLL_IV),
          abs(rap / RAPPORTO_ATTESO - 1.0) <= TOLL_IV, "%.4f" % rap)
    scrivi({"tipo": "passo", "dev": {str(k): v for k, v in dev.items()}, "rapporto": rap})
    print("-" * 130)
    print("### (iii) LA QUADRATURA CON A (identita' dichiarate nel task history)")
    esito("DEVE PASSARE (iii-a): vicino + lontano = totale, ogni conto, entro %g di N |e_K(0)|" % TOLL_III, peg3a <= TOLL_III, "%.3e" % peg3a)
    esito("DEVE PASSARE (iii-b): gli anelli sommati = Delta H_tot del toro, entro %g di N |e_K(0)|" % TOLL_III, peg3b <= TOLL_III, "%.3e" % peg3b)
    esito("DEVE PASSARE (iii-c): max_{t <= vita} |Delta H_tot| del toro = l'errore del passo a s %g (lo stesso numero, un'identita')" % S_PASSI[0],
          abs(dev_vita - dev[S_PASSI[0]]) <= TOLL_III * sc, "%.6e contro %.6e" % (dev_vita, dev[S_PASSI[0]]))
    print("-" * 130)

    # ------------------------------------------------------------------------------------------------ la lettura A
    print("### LA STRADA A, LA LETTURA: per ogni disco, le somme dei guadagni positivi (ENTRATE) e negativi (USCITE) di H_tot per tick, in unita' di N |e_K(0)|; fino alla vita (%d) e dopo" % VITA)
    gA = guadagni_A(serieA, list(dsc))
    letturaA = {}
    for dn, (tt, g) in gA.items():
        g = np.array(g)
        tt = np.array(tt)
        pr, do = tt <= VITA, tt > VITA
        ent_p, usc_p = float(g[pr & (g > 0)].sum()) / sc, float(g[pr & (g < 0)].sum()) / sc
        ent_d, usc_d = float(g[do & (g > 0)].sum()) / sc, float(g[do & (g < 0)].sum()) / sc
        n_ent_d = int(np.sum(do & (g > 0)))
        letturaA[dn] = {"entrate_vita": ent_p, "uscite_vita": usc_p, "entrate_dopo": ent_d, "uscite_dopo": usc_d, "tick_entrata_dopo": n_ent_d, "tick_dopo": int(do.sum())}
        print("  %-9s: fino alla vita entrate %+.4e uscite %+.4e (saldo %+.4e); dopo entrate %+.4e uscite %+.4e (saldo %+.4e; %d tick in entrata su %d)"
              % (dn, ent_p, usc_p, ent_p + usc_p, ent_d, usc_d, ent_d + usc_d, n_ent_d, int(do.sum())))
    scrivi({"tipo": "strada_A", "dischi": letturaA})
    print("-" * 130)

    # ------------------------------------------------------------------------------------------------ B
    print("### LA STRADA B, LA DIAGNOSI: da una copia, il conto dopo ogni pezzo; il va-e-vieni sum_k |Delta_k E| contro |Delta_tick E|, i primi %d tick ogni %d (N |e_K(0)|)" % (T_B, OGNI_B))
    _L2, inc2, mot2, st2, par2, rr2, _w2 = scena(rec, False)
    mas2 = {"vicino": rr2 <= R_VICINO * w, "lontano": rr2 > R_VICINO * w}
    nq = len(CM.ORDINE)
    okB = True
    vv = {(reg, k): [0.0, 0.0] for reg in mas2 for k in ("cost", "cin", "leg", "vuo", "tot")}
    with SF.forma(VC.FORMA), BE.conv(ZERO):
        for t in range(T_B):
            if t % OGNI_B == 0:
                pz, fine = pezzi_B(inc2, mot2, st2, par2, mas2, e_K, LAM_ZERO, nq)
                vero_st = {kk: (v.copy() if hasattr(v, "copy") else v) for kk, v in st2.items()}
                TK.percorri_tick(vero_st, mot2, par2, (), None, nq)
                okB &= all(np.array_equal(fine[kk], vero_st[kk]) for kk in ("psi_h", "phi_h"))
                for (reg, k), acc in vv.items():
                    acc[0] += sum(abs(pz[i + 1][reg][k] - pz[i][reg][k]) for i in range(nq)) / sc
                    acc[1] += abs(pz[nq][reg][k] - pz[0][reg][k]) / sc
            TK.percorri_tick(st2, mot2, par2, (), None, nq)
    esito("DEVE PASSARE (B): dopo %d pezzi la copia = il tick intero al bit (psi e phi)" % nq, okB, "")
    for (reg, k), (vai, saldo) in sorted(vv.items()):
        print("  %-8s %-4s: il va-e-vieni %.4e, il saldo dei tick %.4e, il rapporto %s" % (reg, k, vai, saldo, "%.1f" % (vai / saldo) if saldo > 0 else "-"))
    scrivi({"tipo": "strada_B", "va_e_vieni": {"%s %s" % rk: v for rk, v in vv.items()}})
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
