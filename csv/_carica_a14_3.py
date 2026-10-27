# -*- coding: utf-8 -*-
r"""**LA CARICA DI `A14.3`: QUATTRO CANDIDATE NEL TICK** *([[PROGETTO-U1]]; la parte 3 del mandato dopo `15df5c63`; il task history `doc/TASK_HISTORY/2026-10-27_carica_a14_3.md`)*:
### **`Q_N` la norma, `Q_S = sum psi^+ sigma_z psi` la rotazione interna, `Q_B = N+ - N-` il segno della banda di `W0`, `Q_F` il segno della frequenza locale;**
### **la loro deriva in tre dinamiche:** ### **`W0`** *(senza i pezzi che dipendono dallo stato)*, ### **il tick intero a `eps 0` e a `eps 0.5`.** ### **Una misura breve, dichiarata; nessuna scelta.**

> ### **In memoria; nessun file del nucleo.** ### **Importati, non copiati:** `_scomposizione_solitone.scena`, `_screening_forme_s3.forma`, `_triangoli_bassa_energia.conv`, `tick.percorri_tick`.

Gira con:  python csv/_carica_a14_3.py > doc/referti_l2/carica_a14_3.txt
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

JSONL = os.path.join(RADICE, "doc", "referti_l2", "carica_a14_3.jsonl")
L = 12
T = 200
SEME = 20261027
ZERO = "simm"                  # ### le bande si leggono allo zero simmetrico: lo spettro della materia e' simmetrico (787296da)
FORMA = "S1"
SALTA_W0 = ("CAMM-MATERIA-VUOTO", "CAMM-FASE-VUOTO")   # ### i pezzi che dipendono dallo stato
EPS = (0.0, 0.5)
TOLL_0 = 1e-12
TOLL_1 = 1e-10
TOLL_2 = 1e-12
TOLL_MODI = 1e-9
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


def un_tick(st, mot, par, salta):
    import composizione as CM
    import tick as TK
    TK.percorri_tick(st, mot, par, salta, None, len(CM.ORDINE))


def cariche(inc, psi, psi_dopo, Pp, Pm):
    """### `(Q_N, Q_S, Q_B, Q_F)` dello stato `psi`; `Q_F` vuole anche lo stato al tick dopo."""
    x = psi.reshape(-1)
    qn = float(np.sum(np.abs(psi) ** 2))
    qs = float(np.sum(np.abs(psi[:, 0]) ** 2) - np.sum(np.abs(psi[:, 1]) ** 2))
    qb = float(np.real(np.vdot(x, Pp @ x)) - np.real(np.vdot(x, Pm @ x)))
    sov = np.zeros(inc.n, dtype=complex)
    np.add.at(sov, inc.nodo, np.sum(np.conj(psi) * psi_dopo, axis=1))
    rho = np.zeros(inc.n)
    np.add.at(rho, inc.nodo, np.sum(np.abs(psi) ** 2, axis=1))
    om = -np.angle(sov)
    qf = float(np.sum(np.sign(om) * rho))
    return qn, qs, qb, qf


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import _scomposizione_solitone as SC
    import _screening_forme_s3 as SF
    import _triangoli_bassa_energia as BE
    import composizione as CM
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA CARICA DI A14.3: QUATTRO CANDIDATE (la norma, la rotazione interna sigma_z, N+ - N- della banda di W0, il segno della frequenza locale) IN TRE DINAMICHE")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_carica_a14_3.py", "primo_ordine/tick.py", "primo_ordine/flussi_parziali.py", "primo_ordine/materia_vuoto.py", "primo_ordine/motore.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: L %d T %d SEME %d ZERO %s FORMA %s SALTA_W0 %s EPS %s TOLL_0 %g TOLL_1 %g TOLL_2 %g TOLL_MODI %g; il vuoto uniforme; cs spento; U = I"
          % (L, T, SEME, ZERO, FORMA, SALTA_W0, EPS, TOLL_0, TOLL_1, TOLL_2, TOLL_MODI))
    print("-" * 130)
    if os.path.exists(JSONL):
        os.remove(JSONL)
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    inc, mot, st, par = SC.scena(L)
    rng = np.random.default_rng(SEME)
    psi0 = rng.standard_normal(st["psi_h"].shape) + 1j * rng.standard_normal(st["psi_h"].shape)
    psi0 *= math.sqrt(6.0 * inc.n / float(np.sum(np.abs(psi0) ** 2)))   # ### la norma per nodo ~ Lambda = 6: x ~ 1
    phi0 = st["phi_h"].copy()
    D = psi0.size
    # ------------------------------------------------------------------ W0 e le sue bande
    t0 = time.time()
    W = np.zeros((D, D), dtype=complex)
    with SF.forma(FORMA), BE.conv(ZERO):
        for j in range(D):
            s = {k: (x.copy() if hasattr(x, "copy") else x) for k, x in st.items()}
            e = np.zeros(D, dtype=complex)
            e[j] = 1.0
            s["psi_h"][...] = e.reshape(st["psi_h"].shape)
            s["phi_h"][...] = phi0
            un_tick(s, mot, dict(par), SALTA_W0)
            W[:, j] = s["psi_h"].reshape(-1)
    unit = float(np.max(np.abs(W.conj().T @ W - np.eye(D))))
    lam, V = np.linalg.eig(W)
    om = -np.angle(lam)                       # ### W = e^{-i omega}
    piu = om > TOLL_MODI
    meno = om < -TOLL_MODI
    zero = ~(piu | meno)
    pi_ = np.abs(np.abs(om) - math.pi) <= TOLL_MODI
    Qp, _r = np.linalg.qr(V[:, piu])
    Qm, _r = np.linalg.qr(V[:, meno])
    Pp, Pm = Qp @ Qp.conj().T, Qm @ Qm.conj().T
    comm = max(float(np.max(np.abs(W @ Pp - Pp @ W))), float(np.max(np.abs(W @ Pm - Pm @ W))))
    orto = float(np.max(np.abs(Pp @ Pm)))
    print("### W0 (il tick senza %s), %d componenti (%.0f s): l'unitarieta' %.1e; omega da %+.6f a %+.6f; %d positive, %d negative, %d a zero, %d a pi; [W, P+-] %.1e; P+ P- %.1e"
          % (SALTA_W0, D, time.time() - t0, unit, om.min(), om.max(), int(piu.sum()), int(meno.sum()), int(zero.sum()), int(pi_.sum()), comm, orto))
    scrivi({"tipo": "W0", "D": D, "unitarieta": unit, "positive": int(piu.sum()), "negative": int(meno.sum()), "zero": int(zero.sum()), "pi": int(pi_.sum()), "commutatore": comm})
    print("-" * 130)
    # ------------------------------------------------------------------ le tre dinamiche
    dinamiche = (("W0", SALTA_W0, 0.0), ("intero eps 0", (), 0.0), ("intero eps 0.5", (), 0.5))
    ris = {}
    for nome, salta, eps in dinamiche:
        s = {k: (x.copy() if hasattr(x, "copy") else x) for k, x in st.items()}
        s["psi_h"][...] = psi0
        s["phi_h"][...] = phi0
        p = dict(par)
        p["eps"] = eps
        serie = []
        t0 = time.time()
        with SF.forma(FORMA), BE.conv(ZERO):
            prima = s["psi_h"].copy()
            un_tick(s, mot, p, salta)
            for t in range(T + 1):
                dopo = s["psi_h"].copy()
                serie.append(cariche(inc, prima, dopo, Pp, Pm))
                if t < T:
                    prima = dopo
                    un_tick(s, mot, p, salta)
        a = np.array(serie)
        q0 = a[0, 0]
        der = [float(np.max(np.abs(a[:, k] - a[0, k]))) / q0 for k in range(4)]
        ris[nome] = der
        print("  %-15s: la deriva massima relativa a Q_N(0) = %.1f: Q_N %.2e; Q_S %.2e (Q_S(0) %+.4f); Q_B %.2e (Q_B(0) %+.4f); Q_F %.2e (Q_F(0) %+.4f) (%.0f s)"
              % (nome, q0, der[0], der[1], a[0, 1], der[2], a[0, 2], der[3], a[0, 3], time.time() - t0))
        scrivi({"tipo": "dinamica", "nome": nome, "eps": eps, "salta": list(salta), "derive": der, "iniziali": [float(x) for x in a[0]], "finali": [float(x) for x in a[-1]]})
    print("-" * 130)
    print("### I CRITERI")
    esito("DEVE PASSARE (0): Q_N conservata entro %g relativo nelle tre dinamiche" % TOLL_0, all(ris[n][0] <= TOLL_0 for n in ris), " ".join("%s %.1e" % (n, ris[n][0]) for n in ris))
    esito("DEVE PASSARE (1): Q_B = N+ - N- conservata entro %g relativo sotto W0 (il controllo dei proiettori)" % TOLL_1, ris["W0"][2] <= TOLL_1, "%.1e" % ris["W0"][2])
    esito("PUO' FALLIRE (2): Q_S = sum psi^+ sigma_z psi conservata entro %g relativo col tick intero a eps 0" % TOLL_2, ris["intero eps 0"][1] <= TOLL_2, "%.1e" % ris["intero eps 0"][1], deve=False)
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
