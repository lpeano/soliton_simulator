# -*- coding: utf-8 -*-
r"""**L'IPOTESI DI LUCA SULLO ZERO DEL VUOTO** *([[ZERO-DEL-VUOTO]], [[PROGETTO-MITOSI]]; il task history `doc/TASK_HISTORY/2026-10-27_zero_del_vuoto.md`)*:
### **`(0)` uno spostamento UNIFORME dello zero e' una fase globale; `(1)` il `delta` che assorbirebbe l'energia della nascita; `(2)` l'universalita' di uno
spostamento LOCALE** *(`(ii)` su materia e vuoto, `(i)` sul solo vuoto)* ### **contro la caduta da un gradiente di `cs`; `(3)` la variante proporzionale all'energia.**

> ### **In memoria; nessun file del nucleo: lo spostamento e' una legge di PROVA** *(una fase per nodo intorno al tick)*.
> ### **Importati, non copiati:** `_forza_da_cs` *(`pacchetto`, `fit_moto`, `MIN_PUNTI`)*, `_triangoli_forza` *(`coppia_K`, `tori`)*, `_energia_del_legame.per_nodo`, `_scomposizione_solitone` *(`scena`,
> `stato_uniforme`)*, `_conto_del_vuoto` *(`stato_K`, `nascita`)*, `_divisione_vuoto.phi_regola`, `scena_l2.scena_toro`, `tick.percorri_tick`.

Gira con:  python csv/_zero_del_vuoto.py > doc/referti_l2/zero_del_vuoto.txt
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

JSONL = os.path.join(RADICE, "doc", "referti_l2", "zero_del_vuoto.jsonl")
RIF_NASCITA = os.path.join(RADICE, "doc", "referti_l2", "divisione_vuoto.jsonl")
S0 = 0.3
ZERO = "simm"
LAM_ZERO = 0.5
FORMA = "S1"
L0 = 24                        # ### (0): il toro della scena di C3
T0 = 200
DELTA_UNIFORME = 0.1           # ### (0): in unita' di lambda
L_NASCITA = 24
REGOLE = ("v1", "v3")
LX, LY = 96, 6                 # ### (2), (3): il toro a striscia A di 7daa8840
NB = 12
ETA = 1e-2
EPS = (0.0, 0.5)
PERIODI = 10
TOLL_UNIV = 0.02
MECCANISMI = ("ii", "i", "prop", "H")
OK = [0, 0]
FALLITE = []


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


def fase_nodo(inc, st, campo, angolo):
    """### `campo <- e^{-i angolo_k} campo` sulle estremita' del nodo `k`."""
    a = np.take(angolo, inc.nodo)
    if st[campo].ndim == 2:
        st[campo] *= np.exp(-1j * a)[:, None]
    else:
        st[campo] *= np.exp(-1j * a)


def energia_per_norma(inc, mot, st, campo):
    """### **L'energia per unita' di norma del campo al nodo, allo zero simmetrico** *(`per_nodo` col campo / la sua densita' + `2 pi lambda`)*."""
    import _energia_del_legame as EL
    altro = "phi_h" if campo == "psi_h" else "psi_h"
    e = EL.per_nodo(inc, mot, st, altro)
    d = np.zeros(inc.n)
    x = st[campo]
    np.add.at(d, inc.nodo, np.sum(np.abs(x) ** 2, axis=1) if x.ndim == 2 else np.abs(x) ** 2)
    out = np.zeros(inc.n)
    vivi = d > 1e-300
    out[vivi] = e[vivi] / d[vivi]
    return out + 2 * math.pi * LAM_ZERO


def un_passo(inc, mot, st, par, meccanismo, profilo):
    """### **Un tick con lo spostamento a meta' prima e a meta' dopo** *(il palindromo)*."""
    import composizione as CM
    import tick as TK

    def meta():
        if meccanismo in ("ii", "i"):
            ang = 0.5 * 2 * math.pi * S0 * profilo
            if meccanismo == "ii":
                fase_nodo(inc, st, "psi_h", ang)
            fase_nodo(inc, st, "phi_h", ang)
        elif meccanismo == "prop":
            ap = 0.5 * S0 * profilo * energia_per_norma(inc, mot, st, "psi_h")
            av = 0.5 * S0 * profilo * energia_per_norma(inc, mot, st, "phi_h")
            fase_nodo(inc, st, "psi_h", ap)
            fase_nodo(inc, st, "phi_h", av)
    meta()
    TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
    meta()


def corsa(eps, banda, meccanismo, eta, T):
    import _forza_da_cs as FC
    import _screening_forme_s3 as SF
    import _triangoli_bassa_energia as BE
    import _triangoli_forza as TF
    import scena_l2 as SL
    inc, mot, st, par = SL.scena_toro("triangoli", (LX, LY), 1.0, 0.1)
    n = inc.n
    m1 = (np.arange(n) // LY).astype(float)
    m2 = (np.arange(n) % LY).astype(float)
    profilo = eta * np.cos(2.0 * np.pi * m1 / LX)
    mot.cs = S0 * (1.0 + profilo) if meccanismo == "H" else np.full(n, S0)
    mot.lambda_c = None
    par = dict(par)
    par["eps"] = eps
    Q = TF.coppia_K(eps, S0)[banda]["Q"]
    x0, W = LX / 4.0, LX / 16.0
    st["psi_h"][...] = FC.pacchetto(m1, x0, W, Q[:, 0], TF.tori()["A"]["fase_K"](m1, m2)).reshape(st["psi_h"].shape)
    st["phi_h"][...] = SL.VUOTO_PER_ESTREMITA
    fase = np.exp(2j * np.pi * m1 / LX)
    xx = []
    with SF.forma(FORMA), BE.conv(ZERO):
        for t in range(T + 1):
            if t:
                un_passo(inc, mot, st, par, meccanismo, profilo if meccanismo != "H" else None)
            w = np.sum(np.abs(st["psi_h"].reshape(n, NB)) ** 2, axis=1)
            dx = ((LX / (2.0 * np.pi) * np.angle(np.sum(w * fase))) - x0 + LX / 2.0) % LX - LX / 2.0
            if abs(dx) >= LX / 32.0:
                break
            xx.append(float(dx))
    return np.array(xx)


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import _conto_del_vuoto as C3
    import _divisione_vuoto as DV
    import _forza_da_cs as FC
    import _scomposizione_solitone as SC
    import _screening_forme_s3 as SF
    import _triangoli_bassa_energia as BE
    import _triangoli_forza as TF
    import composizione as CM
    import scena_l2 as SL
    _presidio.avvia(__file__)
    print("=" * 130)
    print("L'IPOTESI DI LUCA SULLO ZERO DEL VUOTO (01:26): (0) lo spostamento uniforme; (1) quanto serve alla nascita; (2) l'universalita' dello spostamento locale; (3) la variante proporzionale")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_zero_del_vuoto.py", "csv/_forza_da_cs.py", "csv/_triangoli_forza.py", "csv/_conto_del_vuoto.py", "csv/_divisione_vuoto.py",
                                     "doc/referti_l2/divisione_vuoto.jsonl")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: S0 %g ZERO %s LAM_ZERO %g FORMA %s L0 %d T0 %d DELTA_UNIFORME %g L_NASCITA %d REGOLE %s LX %d LY %d ETA %g EPS %s PERIODI %d TOLL_UNIV %g MECCANISMI %s; cs spento (salvo H)"
          % (S0, ZERO, LAM_ZERO, FORMA, L0, T0, DELTA_UNIFORME, L_NASCITA, REGOLE, LX, LY, ETA, EPS, PERIODI, TOLL_UNIV, MECCANISMI))
    print("  lo spostamento dello zero: la fase e^{-i 2 pi s delta_k} per tick, a meta' prima e a meta' dopo il tick; (ii) su psi e phi, (i) sul solo phi; (prop) e^{-i s g_k e_k}, e_k l'energia per unita' di norma allo zero simmetrico; (H) cs = s0 (1 + eta cos)")
    print("-" * 130)
    if os.path.exists(JSONL):
        os.remove(JSONL)
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    # ------------------------------------------------------------------ (0)
    print("### (0) LO SPOSTAMENTO UNIFORME (delta %g su materia e vuoto, L %d, %d tick)" % (DELTA_UNIFORME, L0, T0))
    Q0 = TF.coppia_K(0.0, S0)[0]["Q"][:, 0]
    fin = {}
    for con in (False, True):
        inc, mot, st = SC.stato_uniforme(L0, Q0, np.arange(L0 * L0) // L0, np.arange(L0 * L0) % L0)
        st["phi_h"][...] = SL.VUOTO_PER_ESTREMITA
        par = {"eps": 0.0}
        prof = np.full(inc.n, DELTA_UNIFORME)
        with SF.forma(FORMA), BE.conv(ZERO):
            for t in range(T0):
                if con:
                    un_passo(inc, mot, st, par, "ii", prof)
                else:
                    un_passo(inc, mot, st, par, "nessuno", prof)
        rho = np.zeros(inc.n)
        np.add.at(rho, inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
        fin[con] = (rho, np.abs(st["phi_h"]))
    uguale = fin[False][0].tobytes() == fin[True][0].tobytes() and fin[False][1].tobytes() == fin[True][1].tobytes()
    d_rho = float(np.max(np.abs(fin[False][0] - fin[True][0])))
    d_phi = float(np.max(np.abs(fin[False][1] - fin[True][1])))
    esito("DEVE PASSARE (0): delta uniforme: rho_k e |phi_h| AL BIT con e senza, %d tick" % T0, uguale, "max|d rho| %.1e max|d |phi|| %.1e" % (d_rho, d_phi))
    scrivi({"tipo": "uniforme", "al_bit": uguale, "d_rho": d_rho, "d_phi": d_phi})
    print("-" * 130)
    # ------------------------------------------------------------------ (1)
    print("### (1) QUANTO SERVE: delta = |Delta E| / (2 pi norma locale), la norma sui cinque nodi della mossa dopo la nascita (L %d)" % L_NASCITA)
    rif = {}
    for l in io.open(RIF_NASCITA, encoding="utf-8"):
        d = json.loads(l)
        if d.get("tipo") == "regola" and d.get("mossa") == "nascita" and d.get("L") == L_NASCITA:
            rif[d["regola"]] = d
    sc = C3.stato_K(L_NASCITA)
    dopo = C3.nascita(L_NASCITA, *sc)
    ii2, jj2, nn2, _d2, psi2 = dopo[:5]
    nodi = dopo[6]
    cinque = [nodi[x] for x in ("n", "i", "j", "k", "l") if x in nodi]
    nh = DV.nodo_h(ii2, jj2)
    rho = np.zeros(nn2)
    np.add.at(rho, nh, np.sum(np.abs(psi2) ** 2, axis=1))
    for nome in REGOLE:
        ph = DV.phi_regola(nome, "nascita", sc, dopo)
        lam = np.zeros(nn2)
        np.add.at(lam, nh, np.abs(ph) ** 2)
        dE = rif[nome]["dH"]
        NV = float(lam[cinque].sum())
        NT = NV + float(rho[cinque].sum())
        di, dii = abs(dE) / (2 * math.pi * NV), abs(dE) / (2 * math.pi * NT)
        print("  %s: Delta E %+.6e; i nodi %s; Lambda %.4f, rho %.4f; (i) delta %.4e = %.4e lambda*; (ii) delta %.4e = %.4e lambda*" % (nome, dE, cinque, NV, NT - NV, di, di / 0.5, dii, dii / 0.5))
        scrivi({"tipo": "quanto", "regola": nome, "dE": dE, "nodi": cinque, "Lambda": NV, "rho": NT - NV, "delta_i": di, "delta_ii": dii})
    print("-" * 130)
    # ------------------------------------------------------------------ (2), (3)
    print("### (2), (3): L'ACCELERAZIONE DIFFERENZIALE a = (a(+eta) - a(-eta))/2 (dal fit di x(+-eta) - x(0)); il toro a striscia %d x %d, eta %g" % (LX, LY, ETA))
    acc = {m: {} for m in MECCANISMI}
    for eps in EPS:
        bande = TF.coppia_K(eps, S0)
        for b in range(2):
            T = max(LX // 4, int(math.ceil(PERIODI * 2.0 * np.pi / bande[b]["delta_min"])))
            for mec in MECCANISMI:
                t0 = time.time()
                x0 = corsa(eps, b, mec, 0.0, T)
                xp = corsa(eps, b, mec, ETA, T)
                xm = corsa(eps, b, mec, -ETA, T)
                k = min(len(x0), len(xp), len(xm))
                if k < FC.MIN_PUNTI:
                    acc[mec][(eps, b)] = None
                    print("  eps %g banda %d %-4s: meno di %d punti" % (eps, b, mec, FC.MIN_PUNTI))
                    continue
                tt = np.arange(k, dtype=float)
                ap = FC.fit_moto(tt, xp[:k] - x0[:k])
                am = FC.fit_moto(tt, xm[:k] - x0[:k])
                a = 0.5 * (ap["a"] - am["a"])
                acc[mec][(eps, b)] = a
                print("  eps %g banda %d (w %+.4f) %-4s: T %d, punti %d; a(+) %+.4e a(-) %+.4e -> a %+.4e (%.0f s)" % (eps, b, bande[b]["w"], mec, T, k, ap["a"], am["a"], a, time.time() - t0))
                sys.stdout.flush()
                scrivi({"tipo": "caduta", "eps": eps, "banda": b, "w": bande[b]["w"], "meccanismo": mec, "T": T, "punti": k, "a_piu": ap["a"], "a_meno": am["a"], "a": a})
    print("-" * 130)
    print("### L'UNIVERSALITA' PER MECCANISMO: le quattro accelerazioni contro la loro media; e contro la caduta da cs (H)")
    univ = {}
    for mec in MECCANISMI:
        v = [acc[mec][k] for k in sorted(acc[mec])]
        if any(x is None for x in v):
            univ[mec] = None
            print("  %-4s: NON MISURATO (corse senza punti)" % mec)
            continue
        mu = float(np.mean(v))
        sc_ = max(abs(x / mu - 1.0) for x in v) if mu != 0 else math.inf
        univ[mec] = sc_
        print("  %-4s: a %s; la media %+.4e; lo scarto massimo %.4f; contro H %s"
              % (mec, " ".join("%+.4e" % x for x in v), mu, sc_, " ".join("%.4f" % (x / acc["H"][k]) if acc["H"][k] else "-" for x, k in zip(v, sorted(acc[mec])))))
        scrivi({"tipo": "universalita", "meccanismo": mec, "a": v, "media": mu, "scarto": sc_})
    print("-" * 130)
    print("### I CRITERI")
    esito("PUO' FALLIRE (2): l'additivo (ii) universale entro il %g%%" % (100 * TOLL_UNIV), univ["ii"] is not None and univ["ii"] <= TOLL_UNIV, "%s" % univ["ii"], deve=False)
    esito("PUO' FALLIRE (3): il proporzionale universale entro il %g%%" % (100 * TOLL_UNIV), univ["prop"] is not None and univ["prop"] <= TOLL_UNIV, "%s" % univ["prop"], deve=False)
    print("  ### SE LO ZERO SI MUOVE: l'universalita' che fisso' lambda* = 1/2 va ricontrollata (il mandato)")
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
