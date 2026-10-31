# -*- coding: utf-8 -*-
r"""**I SALTI NEL CUORE: UN CONTROLLO DELLA MISURA SULLA CORSA LUNGA DI `B` A `Gamma`** *(UNA PROVA, NESSUNA MODIFICA AL NUCLEO; il mandato di Luca delle `19:08` del `2026-10-31`;
[[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il task history `doc/TASK_HISTORY/2026-10-31_salti_nel_cuore.md`)*:
### **la corsa RIGENERATA pezzo per pezzo, coi confini e la sequenza degli originali** *(lo sha1 della fine e `f_win` di ogni campione al bit: DEVE)*; ### **il baricentro, la scomposizione esatta del passo del cuore, il cuore con la finestra LISCIA, l'oscillazione lenta.**

    python csv/_salti_nel_cuore.py --rigenera            # un pezzo; si ripete finche' dice "finita"
    python csv/_salti_nel_cuore.py --referto > doc/referti_l2/salti_nel_cuore.txt
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

import _consolida_B as CO                                      # noqa: E402

CB = CO.CB
MB = CB.MB
LP = CB.LP
S = CB.S
N = CB.N
L = CB.L
EPS = CB.EPS_LUNGA
OGNI = CB.OGNI
FATTORE = LP.FATTORE_DEROGA     # ### un SALTO: abs(Delta f) > 10 volte la mediana (il riconoscimento, non una lettura)
ISTANTI = (21230, 31400, 59400, 60130, 76580, 96260)    # ### gli istanti del guardiano (Luca 19:08)
MAX_ATTR = 24                   # ### quanti nodi che attraversano il bordo si scrivono per passo
DIR_JSON = os.path.join(RADICE, "doc", "referti_l2", "salti_nel_cuore")
DIR_NPZ = os.path.join(RADICE, "db", "salti_nel_cuore")
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


def lunghezza_arco(z):
    """### **La lunghezza di un arco:** le estremita' `2a`, `2a + 1` di `inc.nodo` sono i due nodi dell'arco `a`; ### **la MEDIANA** *(gli archi che chiudono il toro hanno la distanza non periodica)*."""
    nd = np.asarray(z["inc"].nodo)
    p = z["pos"]
    ll = np.hypot(p[nd[0::2], 0] - p[nd[1::2], 0], p[nd[0::2], 1] - p[nd[1::2], 1])
    return float(np.median(ll))


def campione(z, t, w_in, h):
    """### **Le righe di `_congelato_lungo.punto`, la stessa espressione** *(il confronto al bit)*, **piu' il baricentro e la finestra liscia.**"""
    import _energia_del_legame as EL
    rho, _l = EL.densita(z["inc"], z["st"])
    M = float(rho.sum())
    c = (rho @ z["pos"]) / M
    d = np.hypot(z["pos"][:, 0] - c[0], z["pos"][:, 1] - c[1])
    w = math.sqrt(float(rho @ np.sum((z["pos"] - c) ** 2, axis=1)) / M)
    g = np.clip((w_in + 0.5 * h - d) / h, 0.0, 1.0)
    return {"t": t, "x": float(c[0]), "y": float(c[1]), "w": w, "f_win": float(rho[d <= w_in].sum()) / M, "f_liscia": float(rho @ g) / M}, rho, d, M


def nomi_rig():
    return sorted(n for n in os.listdir(DIR_JSON) if n.startswith("rig_") and n.endswith(".jsonl")) if os.path.isdir(DIR_JSON) else []


def rigenera():
    """### **Un pezzo:** la scena nuova, `DC.forma`, `matrice` e `autovettori` *(la sequenza degli originali: `matrice` scrive lo stato della scena)*, lo stato, i tick nei contesti degli originali."""
    import _congelato_lungo as CL
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    orig = CO.serie_B()
    fatti = nomi_rig()
    k = len(fatti)
    if k >= len(orig):
        print("  la rigenerazione: finita (%d pezzi)" % k)
        return 0
    o = orig[k]
    psi0, _mu, _da = CB.partenza_corsa("B")
    assert SFM.sha(psi0) == o["sha_partenza"], "psi0 NON e' la partenza degli originali"
    f_rip = os.path.join(DIR_NPZ, "rig.npz")
    if k == 0:
        assert o["t0"] == 0
        st = psi0
    else:
        prec = LP.leggi(os.path.join(DIR_JSON, fatti[-1]))
        assert prec["t1"] == o["t0"], "un buco fra i pezzi rigenerati"
        with np.load(f_rip) as dati:
            assert int(dati["t"]) == o["t0"]
            st = dati["psi_h"].copy()
        assert SFM.sha(st) == orig[k - 1]["sha_fine"], "lo stato di ripresa NON e' la fine dell'originale del pezzo prima"
    ref = {p["t"]: p for p in o["punti"]}
    t0, t1 = o["t0"], o["t1"]
    os.makedirs(DIR_JSON, exist_ok=True)
    os.makedirs(DIR_NPZ, exist_ok=True)
    s0 = time.time()
    with MB.scena(N, L, EPS) as (rec, z, phi0, _p):
        w0 = rec["larghezza"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            w_in = DC.forma(z, w0)[0]
        assert w_in == o["w_in"], "w_in NON e' quello dell'originale"
        _ph, Z = DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        LP.ML.Bande(Z, z["L"])
        h = lunghezza_arco(z)
        z["st"]["psi_h"][...] = st
        out, diversi = [], 0
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            prev, rho1, d1, M1 = campione(z, t0, w_in, h)
            if k == 0:
                out.append(prev)
            for t in range(t0 + 1, t1 + 1):
                CL.avanza(z, phi0, 1)
                if t % OGNI == 0:
                    p, rho2, d2, M2 = campione(z, t, w_in, h)
                    in1, in2 = d1 <= w_in, d2 <= w_in
                    en, us = in2 & ~in1, in1 & ~in2
                    p["fin"] = float(rho2[en].sum()) / M2 - float(rho1[us].sum()) / M1
                    p["n_e"], p["n_u"] = int(en.sum()), int(us.sum())
                    if en.any() or us.any():
                        ii = np.nonzero(en | us)[0][:MAX_ATTR]
                        p["attr"] = [[int(i), float(d1[i] - w_in), float(d2[i] - w_in), float(rho2[i] / M2)] for i in ii]
                    out.append(p)
                    rho1, d1, M1 = rho2, d2, M2
        for p in out:
            r = ref.get(p["t"])
            if r is None or r["f_win"] != p["f_win"] or r["w"] != p["w"]:
                diversi += 1
        sha_fine = SFM.sha(z["st"]["psi_h"])
        tmp = f_rip.replace(".npz", "_tmp.npz")
        np.savez(tmp, psi_h=z["st"]["psi_h"], t=t1)
    bit = sha_fine == o["sha_fine"]
    riga = {"t0": t0, "t1": t1, "w_in": w_in, "h": h, "sha_fine": sha_fine, "sha_fine_originale": o["sha_fine"], "bit": bit, "f_win_diversi": diversi,
            "campioni_originali": len(o["punti"]), "campioni": out, "secondi": time.time() - s0}
    LP.scrivi_nuovo(os.path.join(DIR_JSON, "rig_%06d.jsonl" % t0), riga)
    os.replace(tmp, f_rip)
    print("  la rigenerazione: il pezzo %d, tick %d -> %d: %s; f_win diversi dall'originale %d su %d; h %.6f (%.0f s)"
          % (k, t0, t1, "AL BIT (sha1 %s)" % sha_fine[:8] if bit else "### NON AL BIT (%s contro %s)" % (sha_fine[:8], o["sha_fine"][:8]), diversi, len(out), h, riga["secondi"]))
    return 0 if (bit and diversi == 0) else 3


# ====================================================================== IL REFERTO
def picco_spettro(tt, y):
    yy = np.asarray(y) - float(np.mean(y))
    dt = float(tt[1] - tt[0])
    F = np.abs(np.fft.rfft(yy))
    fr = np.fft.rfftfreq(len(yy), dt)
    i = int(np.argmax(F[1:])) + 1
    return 1.0 / fr[i], float(F[i] * 2.0 / len(yy)), fr, F


def referto():
    orig = CO.serie_B()
    rr = [LP.leggi(os.path.join(DIR_JSON, n)) for n in nomi_rig()]
    print("=" * 130)
    print("I SALTI NEL CUORE (Luca 19:08): la corsa lunga di B a Gamma (eps %g, N %.0e, L %d, s %g), RIGENERATA; FATTORE %g ISTANTI %s MAX_ATTR %d OGNI %d" % (EPS, N, L, S, FATTORE, ISTANTI, MAX_ATTR, OGNI))
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: (j1) i salti sono della finestra (spariscono con la liscia); (j2) restano: un fatto fisico; (j3) altro")
    print("=" * 130)
    print("### (0) LA RIGENERAZIONE")
    esito("DEVE PASSARE: tutti i pezzi rigenerati", len(rr) == len(orig), "%d su %d" % (len(rr), len(orig)))
    esito("DEVE PASSARE: ogni pezzo AL BIT (lo sha1 della fine = l'originale)", all(r["bit"] for r in rr), " ".join(r["sha_fine"][:8] for r in rr[-3:]))
    esito("DEVE PASSARE: f_win e w di ogni campione = l'originale, al bit", all(r["f_win_diversi"] == 0 for r in rr), "%d diversi" % sum(r["f_win_diversi"] for r in rr))
    if not rr:
        return
    h, w_in = rr[0]["h"], rr[0]["w_in"]
    cc = [p for r in rr for p in r["campioni"]]
    t = np.array([p["t"] for p in cc])
    tau = t * S
    f = np.array([p["f_win"] for p in cc])
    fl = np.array([p["f_liscia"] for p in cc])
    w = np.array([p["w"] for p in cc])
    x = np.array([p["x"] for p in cc])
    y = np.array([p["y"] for p in cc])
    print("  %d campioni, tick %d .. %d; w_in %.6f; h (la lunghezza di un arco, la mediana) %.6f; la finestra liscia: 1 fino a w_in - h/2, 0 da w_in + h/2, lineare in mezzo" % (len(cc), t[0], t[-1], w_in, h))
    print("-" * 130)
    print("### (a) IL BARICENTRO")
    print("  x %.5f .. %.5f (la media %.5f), y %.5f .. %.5f (la media %.5f); la distanza dalla media: la mediana %.5f, il massimo %.5f; la distanza fra campioni: la mediana %.2e, il massimo %.2e"
          % (x.min(), x.max(), x.mean(), y.min(), y.max(), y.mean(), float(np.median(np.hypot(x - x.mean(), y - y.mean()))), float(np.hypot(x - x.mean(), y - y.mean()).max()),
             float(np.median(np.hypot(np.diff(x), np.diff(y)))), float(np.hypot(np.diff(x), np.diff(y)).max())))
    print("-" * 130)
    print("### (b) I SALTI DELLA FINESTRA NETTA E LA SCOMPOSIZIONE ESATTA DEL PASSO")
    df, dfl, dw = np.diff(f), np.diff(fl), np.diff(w)
    fin = np.array([p["fin"] for p in cc[1:]])
    ne = np.array([p["n_e"] for p in cc[1:]])
    nu = np.array([p["n_u"] for p in cc[1:]])
    med = float(np.median(np.abs(df)))
    sal = np.abs(df) > FATTORE * med
    print("  la mediana di |Delta f_win| %.3e; un salto oltre %g volte: %d salti su %d passi" % (med, FATTORE, int(sal.sum()), len(df)))
    if sal.any():
        a = np.abs(df[sal])
        print("  l'ampiezza dei salti: %.5f .. %.5f (la mediana %.5f); in su %d, in giu' %d; |Delta w| ai salti: la mediana %.2e (fuori dai salti %.2e)"
              % (a.min(), a.max(), float(np.median(a)), int((df[sal] > 0).sum()), int((df[sal] < 0).sum()), float(np.median(np.abs(dw[sal]))), float(np.median(np.abs(dw[~sal])))))
        print("  ai salti: con nodi che attraversano il bordo %d su %d; quanti nodi: %s; il termine della finestra / Delta f: la mediana %.4f; |Delta f - il termine| la mediana %.2e (contro %.2e di |Delta f| fuori dai salti)"
              % (int(((ne + nu)[sal] > 0).sum()), int(sal.sum()), dict(zip(*np.unique((ne + nu)[sal], return_counts=True))), float(np.median(fin[sal] / df[sal])),
                 float(np.median(np.abs(df[sal] - fin[sal]))), med))
        print("  fuori dai salti: con nodi che attraversano %d su %d" % (int(((ne + nu)[~sal] > 0).sum()), int((~sal).sum())))
    # ### il guardiano etichetta un passo col campione d'INIZIO: a ogni istante si stampano TUTTI E DUE i passi (96ddfa9c: prima solo quello che finisce a t)
    print("  gli istanti del guardiano: il passo che FINISCE a t (fine) e quello che COMINCIA a t (inizio):")
    idx = {int(tt): i for i, tt in enumerate(t[1:])}
    for ti, i, qu in [(ti, idx.get(ti + k), qu) for ti in ISTANTI for k, qu in ((0, "fine  "), (OGNI, "inizio"))]:
        if i is None:
            print("    t %d %s: nessun campione" % (ti, qu))
            continue
        p = cc[i + 1]
        print("    t %6d %s: Delta f_win %+.5f (salto: %s), il termine della finestra %+.5f, il resto %+.2e; entrati %d usciti %d %s; Delta w %+.2e; Delta f_liscia %+.2e; il baricentro si sposta di %.2e"
              % (ti, qu, df[i], "si" if sal[i] else "no", fin[i], df[i] - fin[i], ne[i], nu[i],
                 ("(d - w_in prima/dopo: %s)" % " ".join("%+.4f/%+.4f" % (q[1], q[2]) for q in p.get("attr", [])[:8])) if p.get("attr") else "", dw[i], dfl[i],
                 math.hypot(x[i + 1] - x[i], y[i + 1] - y[i])))
    print("-" * 130)
    print("### (c) LA FINESTRA LISCIA")
    medl = float(np.median(np.abs(dfl)))
    sall = np.abs(dfl) > FATTORE * medl
    print("  la mediana di |Delta f_liscia| %.3e; i salti della liscia (oltre %g volte la SUA mediana): %d su %d passi; il massimo |Delta f_liscia| %.3e (contro il massimo |Delta f_win| %.3e)"
          % (medl, FATTORE, int(sall.sum()), len(dfl), float(np.abs(dfl).max()), float(np.abs(df).max())))
    if sal.any():
        print("  agli istanti dei salti della netta: |Delta f_liscia| la mediana %.3e, il massimo %.3e; salti della liscia fra questi %d"
              % (float(np.median(np.abs(dfl[sal]))), float(np.abs(dfl[sal]).max()), int((sal & sall).sum())))
    print("  la netta meno la liscia: %.5f .. %.5f (la media %.5f)" % (float((f - fl).min()), float((f - fl).max()), float((f - fl).mean())))
    print("-" * 130)
    print("### (d) L'OSCILLAZIONE LENTA")
    rc = np.hypot(x - x.mean(), y - y.mean())
    for nome, s in (("f_liscia", fl), ("f_win", f), ("w", w), ("la distanza del baricentro", rc)):
        P, A, _fr, _F = picco_spettro(tau, s)
        print("  %-28s la media %.5f, (max - min)/2 %.5f, la deviazione standard %.5f; lo spettro: il picco al periodo %.1f unita' di tempo (l'ampiezza %.5f)"
              % (nome, float(s.mean()), float((s.max() - s.min()) / 2.0), float(s.std()), P, A))
    print("  le correlazioni a ritardo zero: f_liscia con la distanza del baricentro %+.3f; f_liscia con w %+.3f; f_win con f_liscia %+.3f"
          % (float(np.corrcoef(fl, rc)[0, 1]), float(np.corrcoef(fl, w)[0, 1]), float(np.corrcoef(f, fl)[0, 1])))
    print("-" * 130)
    print("### LE LETTURE: i numeri sono quelli sopra; la parola (j1)/(j2)/(j3) nella relazione")
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--rigenera" in argv:
        sys.exit(rigenera())
    elif "--referto" in argv:
        referto()
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
