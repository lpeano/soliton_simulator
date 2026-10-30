# -*- coding: utf-8 -*-
r"""**IL MODO DI (R) E LA VITA DEL SOLITONE** *(UNA DIAGNOSI, NON UNA CURA; il mandato di Luca delle `20:46` del `2026-10-30`; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il task history `doc/TASK_HISTORY/2026-10-30_modo_di_R.md`)*:
### **(2) la corsa lunga di `R_1e6` riletta dai `.jsonl` committati; (5) la vita `ln(soglia/seme)/gamma` contro l'osservato, per `r 1`, `r 1.5247`, `R_1e6`;**
### **(3) `R_1e6` rifatta dallo stato fermo fino al tick `14000`, AL BIT coi pezzi committati, con `D` in memoria SOLO agli istanti dell'esame: le rotazioni per banda, la frequenza di `A` contro lo spettro libero, gli anelli, le armoniche.**
### **Niente su disco** *(solo `stdout`)*.

    python csv/_modo_di_R.py > doc/referti_l2/modo_di_R.txt
"""
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

import _livelli_piatti as LP                                   # noqa: E402

NOME = "R_1e6"
T_FINE = 14000
ISTANTI = tuple(range(10400, T_FINE + 1, 400))      # ### i 10 istanti (Luca: ~10 fra 10000 e 14000), ciascuno col D del tick dopo
OGNI_TICK = tuple(range(12000, 12041))              # ### D consecutivi ogni tick: la rotazione senza alias (dtau 0.15)
OGNI_5 = tuple(range(12000, 12201, 5))              # ### D ogni 5 tick (dtau 0.75): il controllo dell'alias
ARMONICHE_A = (ISTANTI[0], 12000, ISTANTI[-1])
SIGMA = 3.0                                         # ### il 3 sigma di doc/PATTERN_DI_PROVA.md
FINESTRA_LUCA = (1500.0, 2200.0)                    # ### la finestra del guardiano (Luca 20:46), stampata accanto a quella del criterio
SEME_LUCA = 1e-9
SOGLIA = 1e-2                                       # ### la soglia della vita (Luca 20:46) = la saturazione di SL
DIR_ML = os.path.join(RADICE, "doc", "referti_l2", "modo_lento")


def pezzi():
    D = LP.DIR_JSON
    righe = sorted([LP.leggi(os.path.join(D, n)) for n in os.listdir(D) if n.startswith("lunga_%s_" % NOME) and n.endswith(".jsonl")], key=lambda x: x["t0"])
    for x, y in zip(righe, righe[1:]):
        assert x["t1"] == y["t0"], ("un buco fra i pezzi", x["t1"], y["t0"])
    return righe


def finestra(tau, nD, attesa):
    """### **Il criterio di `5f06dbfb`:** da `FATTORE_DEROGA` volte la deriva attesa a `SOGLIA`; il fit `ln|D| = a + gamma tau`."""
    basso = LP.FATTORE_DEROGA * attesa * np.maximum(tau, LP.S)
    fin = [i for i in range(len(tau)) if basso[i] < nD[i] < SOGLIA]
    if len(fin) < 3:
        return None
    i0, i1 = fin[0], fin[-1]
    x, y = tau[i0:i1 + 1], np.log(nD[i0:i1 + 1])
    g, a = np.polyfit(x, y, 1)
    return {"tau": (float(x[0]), float(x[-1])), "campioni": i1 - i0 + 1, "gamma": float(g), "a": float(a), "scarto_max": float(np.abs(y - (a + g * x)).max())}


def fit_fra(tau, nD, lo, hi):
    m = (tau >= lo) & (tau <= hi)
    g, a = np.polyfit(tau[m], np.log(nD[m]), 1)
    return {"gamma": float(g), "a": float(a), "campioni": int(m.sum())}


# ====================================================================== (2) LA CORSA LUNGA RILETTA
def rileggi():
    print("### (2) LA CORSA LUNGA DI R_1e6 RILETTA DAI .jsonl COMMITTATI")
    righe = pezzi()
    cj = LP.leggi(os.path.join(LP.DIR_JSON, "cerca_%s.json" % NOME))
    dd = [d for x in righe for d in x["D"]]
    pts = [p for x in righe for p in x["punti"]]
    s = righe[0]["s"]
    tau = np.array([d["t"] for d in dd], dtype=float) * s
    nD = np.array([d["nD"] for d in dd])
    att = cj["residuo_finale"] / s
    fw = finestra(tau, nD, att)
    print("  %d pezzi, tick %d -> %d; la deriva attesa residuo/s %.3e per unita' di tempo" % (len(righe), righe[0]["t0"], righe[-1]["t1"], att))
    if fw is None:
        print("  la finestra del criterio: meno di 3 campioni")
    else:
        print("  LA FINESTRA del criterio (da %g volte la deriva attesa a %g): tau %.0f .. %.0f, %d campioni: gamma %.5f, a %.3f (il seme efficace e^a %.3e), scarto max di ln %.3f"
              % (LP.FATTORE_DEROGA, SOGLIA, fw["tau"][0], fw["tau"][1], fw["campioni"], fw["gamma"], fw["a"], math.exp(fw["a"]), fw["scarto_max"]))
    fl = fit_fra(tau, nD, *FINESTRA_LUCA)
    print("  la finestra del guardiano tau %.0f .. %.0f: %d campioni, gamma %.5f, a %.3f" % (FINESTRA_LUCA[0], FINESTRA_LUCA[1], fl["campioni"], fl["gamma"], fl["a"]))
    t0 = fw["tau"][0] if fw else FINESTRA_LUCA[0]
    prima = [d for d, x in zip(dd, tau) if x < t0]
    dentro = [d for d, x in zip(dd, tau) if fw and fw["tau"][0] <= x <= fw["tau"][1]]
    for chi, gr in (("PRIMA della finestra", prima), ("DENTRO la finestra", dentro)):
        if gr:
            print("  le bande di D %s (%d campioni, media): %s" % (chi, len(gr), "  ".join("%s %.4f" % (b, float(np.mean([d["bande"][b] for d in gr]))) for b in ("A", "P0", "Ppi", "B"))))
    fn = LP.forma_pendenze(tau[tau < t0], nD[tau < t0])
    if fn["forma"] is not None:
        print("  la forma PRIMA della finestra, col criterio aggiunto: %s (b %.4f +- %.4f, gamma %.2e +- %.1e, %d campioni)" % (fn["forma"].upper(), fn["b"], fn["sigma_b"], fn["gamma"], fn["sigma_gamma"], fn["campioni"]))
    print("  v / attesa prima della finestra (|D| / (residuo/s tau), mediana): %.3f" % float(np.median(nD[tau < t0] / (att * tau[tau < t0]))))
    cu = [(p["tau"], p["f_win"]) for p in pts]
    print("  il cuore: %.5f a tau 0, %.5f a %.0f, %.5f a %.0f" % (cu[0][1], [c for t, c in cu if t <= t0][-1], t0, cu[-1][1], cu[-1][0]))
    return {"tau": tau, "nD": nD, "fw": fw}


# ====================================================================== (5) LA VITA
def vita(lunga):
    print("### (5) LA VITA: t_vita = ln(%g/seme)/gamma, contro l'osservato (il primo tau con |D|/|psi0| >= %g)" % (SOGLIA, SOGLIA))
    casi = []
    for nome, f in (("r 1 (s 0.3; 03142636)", "modo_r1_s0.3.json"), ("r 1.5247 (s 0.15; 03142636)", "modo_r1.52.json")):
        m = LP.leggi(os.path.join(DIR_ML, f))
        tau = np.array(m["t"], dtype=float) * m["s"]
        nD = np.array(m["nD"])
        w = m["analisi"]["finestra"]
        fw = fit_fra(tau, nD, w["tau"][0], w["tau"][1])
        casi.append((nome, tau, nD, fw["gamma"], fw["a"]))
    if lunga["fw"] is not None:
        casi.append(("R_1e6 (s 0.15; la corsa lunga)", lunga["tau"], lunga["nD"], lunga["fw"]["gamma"], lunga["fw"]["a"]))
    for nome, tau, nD, g, a in casi:
        sopra = np.nonzero(nD >= SOGLIA)[0]
        oss = float(tau[sopra[0]]) if len(sopra) else None
        semi = (("1e-9 (Luca)", SEME_LUCA), ("il primo campione %.2e" % nD[0], float(nD[0])), ("il seme efficace e^a %.2e" % math.exp(a), math.exp(a)))
        prev = "; ".join("%s: %.0f" % (k, math.log(SOGLIA / v) / g) for k, v in semi)
        print("  %-32s gamma %.5f | previsto, seme %s | OSSERVATO %s" % (nome, g, prev, ("%.1f" % oss) if oss is not None else "mai sopra %g" % SOGLIA))
    print("  (il tasso di Luca per r 1, 0.151 di dfb5ab7e a s 0.15: col seme 1e-9 %.0f)" % (math.log(SOGLIA / SEME_LUCA) / 0.151))


# ====================================================================== (3) LA CORSA NUOVA
def corsa():
    import _congelato_lungo as CL
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _modo_al_variare_di_s as MS
    import _modo_instabile as MI
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    print("### (3) R_1e6 RIFATTA DALLO STATO FERMO FINO AL TICK %d, AL BIT COI PEZZI; D SOLO AGLI ISTANTI DELL'ESAME" % T_FINE)
    r, g, N = LP.CONFIG[NOME]
    psi0, mu, _cj = LP.stato(NOME)
    fine = {x["t1"]: x["sha_fine"] for x in pezzi()}
    tieni = set(ISTANTI) | {t + 1 for t in ISTANTI} | set(OGNI_TICK) | set(OGNI_5)
    Ds = {}
    with LP.scena(N) as (_rec, z, phi0, _p), LP.configurazione(r, g):
        ph, Z = DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        bande = LP.ML.Bande(Z, z["L"])
        vista = MS.Vista(z, psi0)
        _w, kk = MI.armoniche(vista, np.ones(vista.n))
        z["st"]["psi_h"][...] = psi0
        s0 = time.time()
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            for t in range(1, max(tieni) + 1):          # ### fino a 14001: l'ultimo istante vuole il D del tick dopo (il primo giro morto per KeyError 14001)
                CL.avanza(z, phi0, 1)
                if t in fine:
                    LP.esito("DEVE PASSARE: lo stato al tick %d = sha_fine del pezzo committato (AL BIT)" % t, SFM.sha(z["st"]["psi_h"]) == fine[t], fine[t][:8])
                if t in tieni:
                    Ds[t] = np.exp(1j * mu * LP.S * t) * z["st"]["psi_h"] - psi0
        print("  %d tick in %.0f s; %d D in memoria" % (T_FINE, time.time() - s0, len(Ds)))
    n0 = float(np.linalg.norm(psi0))
    S = LP.S
    # ### lo spettro libero nella convenzione di Newton: E = fase/s + ALPHA0, riportato in (-pi/s, pi/s]
    E = ph / S + MS.ALPHA0[LP.FORMA]
    E = (E + math.pi / S) % (2.0 * math.pi / S) - math.pi / S

    def avvolgi(x):
        return (x + math.pi / S) % (2.0 * math.pi / S) - math.pi / S

    def reale(d, nomi):
        return np.fft.ifft2(bande.parte(bande.coeff(d), nomi), axes=(0, 1)).reshape(-1, 12)

    def anelli(x):
        p = np.bincount(kk, weights=np.sum(np.abs(x.reshape(-1, 12)) ** 2, axis=1))
        return p / p.sum()

    print("-- i controlli dello strumento")
    d = Ds[12000]
    som = sum(reale(d, (gr,)) for gr in ("Ppi", "A", "P0", "B"))
    LP.esito("DEVE PASSARE: le quattro parti nello spazio reale ricompongono D", float(np.linalg.norm(som.reshape(-1) - d.reshape(-1))) / float(np.linalg.norm(d)) < 1e-10,
             "%.1e" % (float(np.linalg.norm(som.reshape(-1) - d.reshape(-1))) / float(np.linalg.norm(d))))
    for om, dt, deve in ((1.234, 0.15, True), (1.234, 0.75, True), (5.0, 0.15, True), (5.0, 0.75, False)):
        v = bande.rotazione(d, d * np.exp(-1j * om * dt), ("A",), dt)
        LP.esito("DEVE %s: la rotazione di una parte sintetica e^{-i %.3f dtau}, dtau %.2f, ridà %.3f%s" % ("PASSARE" if deve else "FALLIRE (l'alias)", om, dt, om, "" if deve else " (oltre pi/dtau)"),
                 (abs(v - om) < 1e-9) == deve, "%.6f" % v)

    print("-- (a) le rotazioni per banda (l'energia della parte RISPETTO A mu = %.9f)" % mu)
    gruppi = ("P0", "A", "Ppi", "B")
    rot_i = {gr: [bande.rotazione(Ds[t], Ds[t + 1], (gr,), S) for t in ISTANTI] for gr in gruppi}
    for gr in gruppi:
        print("  %-3s ai 10 istanti (dtau %.2f): media %+.5f dev %.5f; %s" % (gr, S, float(np.mean(rot_i[gr])), float(np.std(rot_i[gr])), " ".join("%+.4f" % x for x in rot_i[gr])))
    for nomi, k1 in ((("P0", "A"), "P0 + A"), (("P0", "Ppi"), "P0 + Ppi")):
        v = np.array(rot_i[nomi[0]]) + np.array(rot_i[nomi[1]])
        print("  la somma %-8s: media %+.5f dev %.5f -> %s" % (k1, float(v.mean()), float(v.std()), "ZERO entro %g sigma" % SIGMA if abs(v.mean()) <= SIGMA * v.std() else "NON zero (|media| > %g sigma)" % SIGMA))
    blocchi = {}
    for nome_b, ts in (("ogni tick", OGNI_TICK), ("ogni 5 tick", OGNI_5)):
        dt = (ts[1] - ts[0]) * S
        blocchi[nome_b] = {gr: [bande.rotazione(Ds[a], Ds[b], (gr,), dt) for a, b in zip(ts, ts[1:])] for gr in gruppi}
        print("  il blocco %s da %d (dtau %.2f, %d coppie): %s" % (nome_b, ts[0], dt, len(ts) - 1, "  ".join("%s %+.5f (dev %.5f)" % (gr, float(np.mean(blocchi[nome_b][gr])), float(np.std(blocchi[nome_b][gr]))) for gr in gruppi)))
    for gr in gruppi:
        a, b = float(np.mean(blocchi["ogni tick"][gr])), float(np.mean(blocchi["ogni 5 tick"][gr]))
        print("  l'alias, %-3s: ogni tick %+.5f, ogni 5 %+.5f, differenza %+.5f (2 pi/0.75 = %.4f)" % (gr, a, b, b - a, 2.0 * math.pi / (5 * S)))

    print("-- (b) la frequenza delle parti contro lo spettro libero (E = rotazione + mu; lo spettro E(k) = fase/s + ALPHA0, la convenzione di Newton)")
    intervalli = {gr: (float(E[..., list(idx)].min()), float(E[..., list(idx)].max())) for gr, idx in bande.gruppi.items()}
    for gr, (lo, hi) in intervalli.items():
        print("  la banda %-3s libera: E fra %+.5f e %+.5f" % (gr, lo, hi))
    print("  mu %+.5f" % mu)
    dentro_A = None
    for gr in ("A", "P0", "Ppi"):
        Em = avvolgi(float(np.mean(blocchi["ogni tick"][gr])) + mu)
        dentro = [b for b, (lo, hi) in intervalli.items() if lo <= Em <= hi]
        lo, hi = intervalli[gr]
        dist = 0.0 if lo <= Em <= hi else min(abs(Em - lo), abs(Em - hi))
        print("  la parte %-3s: E %+.5f; dentro le bande libere %s; dalla SUA banda %s (distanza dal bordo %.5f)" % (gr, Em, dentro or "NESSUNA (nel gap)", "DENTRO" if lo <= Em <= hi else "FUORI", dist))
        if gr == "A":
            dentro_A = lo <= Em <= hi

    print("-- (b), (c) dove stanno: i profili per anelli (r 0 .. %d) e i raggi medi" % LP.ML.R_PROFILO)
    p0 = anelli(psi0)
    unif = np.bincount(kk).astype(float)
    unif = unif / unif.sum()
    r_ = np.arange(len(p0))
    rm = {"psi0": float((r_ * p0).sum()), "uniforme": float((r_ * unif).sum())}
    print("  |psi0|^2: raggio medio %.3f; %s" % (rm["psi0"], " ".join("%.4f" % x for x in p0[:LP.ML.R_PROFILO + 1])))
    print("  la densita' UNIFORME sul toro (il caso nullo): raggio medio %.3f" % rm["uniforme"])
    loc = {}
    for gr in ("A", "P0"):
        rr = []
        for t in ISTANTI:
            pa = anelli(reale(Ds[t], (gr,)))
            rr.append(float((r_ * pa).sum()))
            if t in ARMONICHE_A:
                print("  |D_%s|^2 a tick %d (tau %.1f): raggio medio %.3f; %s" % (gr, t, t * S, rr[-1], " ".join("%.4f" % x for x in pa[:LP.ML.R_PROFILO + 1])))
        m = float(np.mean(rr))
        loc[gr] = abs(m - rm["psi0"]) < abs(m - rm["uniforme"])
        print("  %-3s: il raggio medio ai 10 istanti %.3f (dev %.3f) contro psi0 %.3f e uniforme %.3f -> %s" % (gr, m, float(np.std(rr)), rm["psi0"], rm["uniforme"], "LOCALIZZATA (piu' vicina a psi0)" if loc[gr] else "DIFFUSA (piu' vicina all'uniforme)"))

    print("-- le bande e |D| ai 10 istanti")
    nn = []
    for t in ISTANTI:
        c = bande.coeff(Ds[t])
        pk = np.abs(c) ** 2
        tot = float(pk.sum())
        nn.append(float(np.linalg.norm(Ds[t])) / n0)
        print("  tick %5d tau %6.1f |D|/|psi0| %.3e  %s" % (t, t * S, nn[-1], "  ".join("%s %.4f" % (gr, float(pk[..., list(idx)].sum()) / tot) for gr, idx in bande.gruppi.items())))
    gg, aa = np.polyfit(np.array(ISTANTI) * S, np.log(nn), 1)
    print("  il tasso ai 10 istanti: %.5f (seme efficace e^a %.3e)" % (gg, math.exp(aa)))

    print("-- (d) le armoniche (m = 0 .. 12) di drho e della fase")
    for t in ARMONICHE_A:
        for chi, x in (("D", Ds[t]), ("D_A", reale(Ds[t], ("A",))), ("D_P0", reale(Ds[t], ("P0",)))):
            dr, df = MI.per_nodo(vista, x / float(np.linalg.norm(x)))
            wd, _k = MI.armoniche(vista, dr)
            wf, _k = MI.armoniche(vista, df)
            print("  tick %5d %-5s drho: %s | fase: %s" % (t, chi, " ".join("%.3f" % v for v in wd), " ".join("%.3f" % v for v in wf)))

    print("-- LE LETTURE, COI CRITERI SCRITTI PRIMA")
    v = np.array(rot_i["P0"]) + np.array(rot_i["A"])
    zero = abs(v.mean()) <= SIGMA * v.std()
    print("  la somma P0 + A zero: %s; la parte A localizzata: %s; la frequenza di A fuori dalla banda A libera: %s" % (zero, loc["A"], not dentro_A))
    if zero and loc["A"] and not dentro_A:
        print("  LA LETTURA: (i1) una coppia P0 + modo interno di A")
    elif not loc["A"]:
        print("  LA LETTURA: (i2) la parte A e' diffusa: radiazione; la crescita viene da altro (vedi le bande e le rotazioni qui sopra)")
    else:
        print("  LA LETTURA: (i3) altro")


def main():
    import _presidio
    _presidio.avvia(__file__)
    import _deriva_congelato as DC
    import _solitone_vuoto_congelato as VC
    vero = (VC.FORMA, VC.S, DC.N)
    try:
        lunga = rileggi()
        print("-" * 130)
        vita(lunga)
        print("-" * 130)
        corsa()
    finally:
        VC.FORMA, VC.S, DC.N = vero
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; fallite: %s" % (LP.OK[0], LP.OK[1], LP.FALLITE))
    return 0 if LP.OK[0] == LP.OK[1] else 1


if __name__ == "__main__":
    sys.exit(main())
