# -*- coding: utf-8 -*-
r"""**LA CARTA DELLA DERIVA** *(l'aggiunta di Luca delle `15:54` del `2026-11-02`; il task history `doc/TASK_HISTORY/2026-11-02_accensione_lenta.md`, sez. `11-ter`)*:
### **(i) il logaritmo dello spostamento del centro contro il tempo, dalla fine della rampa, con la pendenza a tratti; (ii) la velocita' contro `w` per blocco;
(iii) l'ampiezza dell'oscillazione del cuore a finestre di `500`, accanto alla velocita'.** ### **Per `TP1000`** *(il centro periodico)*, **il vivo e `TA2000`** *(il centro
euclideo: il loro baricentro resta vicino alla partenza, e `TP2` del referto dell'accensione misura la differenza fra i due centri)*.

    python csv/solitone/carta_deriva.py > doc/referti_l2/deriva_solitone.txt
    python csv/solitone/carta_deriva.py --prova TA1000          # la prova sui pezzi di TA1000 (il centro euclideo), al posto di TP1000
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))

import solitone  # noqa: E402,F401  (i percorsi)

FIN_AMPIEZZA = 500.0           # ### (iii) le finestre dell'ampiezza del cuore (Luca 15:54)
TAGLIO = 9000.0                # ### (i) Luca: "se e' una retta gia' prima di 9000"


def pendenza(x, y):
    return float(np.polyfit(x, y, 1)[0]) if len(x) >= 3 else float("nan")


def dati(nome):
    """### **`(tt, X, w, cuore, T_acc, che)`:** `X` la traiettoria del centro *(srotolata se periodico)*; per il vivo `T_acc = 0`."""
    import _respiro_congelato as RC
    import _vuoto_vivo_B as V
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    s = V.CORSE[CA.NOME][2]
    if nome == "VIVO":
        camp, _dd = RC.serie_viva()
        T_acc = 0.0
    else:
        _rr, camp, _dd, _da = CA.serie(nome)
        T_acc = CA.CORSE[nome][0]
    tt = np.array([c["t"] for c in camp]) * s
    if all("per" in c for c in camp):
        L = _rr[0]["L"]
        A1, A2 = TO.vettori()
        c1 = np.array([c["per"]["c1"] for c in camp])
        c2 = np.array([c["per"]["c2"] for c in camp])
        u1 = np.concatenate([[0.0], np.cumsum(((np.diff(c1) + 0.5 * L) % L) - 0.5 * L)])
        u2 = np.concatenate([[0.0], np.cumsum(((np.diff(c2) + 0.5 * L) % L) - 0.5 * L)])
        X = u1[:, None] * A1 + u2[:, None] * A2
        ww = np.array([c["per"]["w"] for c in camp])
        fl = np.array([c["per"]["f_liscia"] for c in camp])
        return tt, X, ww, fl, T_acc, "il centro PERIODICO, srotolato", TO.meta_periodo(L)
    X = np.array([[c["x"], c["y"]] for c in camp])
    ww = np.array([c["w"] for c in camp])
    fl = np.array([c["f_liscia"] for c in camp])
    return tt, X, ww, fl, T_acc, "il centro EUCLIDEO", None


def fine_valida(tt, ww, R, blocco):
    """### **L'inizio del primo blocco con `3 w >= R`** *(il criterio di Luca dopo `8e425771`)*; senza `R` *(il centro euclideo)*, la fine dei dati."""
    if R is None:
        return tt[-1] + 1.0
    a = 0.0
    while a <= tt[-1]:
        m = (tt >= a) & (tt < a + blocco)
        if m.any() and 3.0 * ww[m].max() >= R:
            return a
        a += blocco
    return tt[-1] + 1.0


def logaritmo(nome, tt, X, T_acc, fine, blocco):
    rif = X[(tt >= T_acc) & (tt < T_acc + blocco)].mean(axis=0)
    sp = np.hypot(X[:, 0] - rif[0], X[:, 1] - rif[1])
    print("  (i) %s: lo spostamento s = |X - X_rif|, X_rif la media sul blocco %g .. %g = (%.4f, %.4f); per blocco: s medio, ln s medio, la pendenza di ln s (per 1000)"
          % (nome, T_acc, T_acc + blocco, rif[0], rif[1]))
    a = T_acc
    while a + blocco <= fine + 1e-9 and a < tt[-1]:
        m = (tt >= a) & (tt < a + blocco) & (sp > 0)
        if m.sum() >= 3:
            print("    %7.0f .. %7.0f  s %.4e  ln s %+.4f  la pendenza di ln s %+.4e" % (a, a + blocco, sp[m].mean(), np.log(sp[m]).mean(), 1000 * pendenza(tt[m], np.log(sp[m]))))
        a += blocco
    for t0, t1 in ((T_acc + blocco, min(TAGLIO, fine)), (TAGLIO, fine)):
        if t1 <= t0:
            print("    LA RETTA LUNGA %g .. : non c'e' (i dati validi finiscono a %g)" % (t0, t1))
            continue
        m = (tt >= t0) & (tt < t1) & (sp > 0)
        if m.sum() >= 3:
            print("    LA RETTA LUNGA %g .. %g: la pendenza di ln s %+.4e per 1000 (%d campioni)" % (t0, t1, 1000 * pendenza(tt[m], np.log(sp[m])), int(m.sum())))
        else:
            print("    LA RETTA LUNGA %g .. %g: nessun dato" % (t0, t1))


def finestre(nome, tt, X, ww, fl, a0, fine, passo, ampiezza):
    a = a0
    righe = []
    while a + passo <= fine + 1e-9 and a < tt[-1]:
        m = (tt >= a) & (tt < a + passo)
        if m.sum() >= 3:
            vx, vy = 1000 * pendenza(tt[m], X[m, 0]), 1000 * pendenza(tt[m], X[m, 1])
            r = fl[m] - np.polyval(np.polyfit(tt[m], fl[m], 1), tt[m])
            righe.append((a, a + passo, math.hypot(vx, vy), math.degrees(math.atan2(vy, vx)), float(ww[m].mean()), math.sqrt(2.0) * float(r.std()) if ampiezza else None))
        a += passo
    return righe


def main(argv):
    import _presidio
    from solitone import corsa_accensione as CA
    for m in ("__init__", "toro", "corsa_accensione"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    lunga = argv[argv.index("--prova") + 1] if "--prova" in argv else "TP1000"
    B = CA.BLOCCO
    print("=" * 130)
    print("LA CARTA DELLA DERIVA (Luca 15:54): (i) ln dello spostamento a tratti; (ii) la velocita' contro w per blocco di %g; (iii) l'ampiezza del cuore a finestre di %g" % (B, FIN_AMPIEZZA))
    print("  le definizioni (dichiarate nel task history, sez. 11-ter, prima dei numeri): s = |X - X_rif|, X_rif la media del primo blocco dopo T_acc; la pendenza di ln s per blocco;")
    print("  due rette lunghe, T_acc + %g .. %g e %g .. la fine valida; la velocita': le rette di x e y nella finestra; l'ampiezza: sqrt(2) x la deviazione standard del cuore" % (B, TAGLIO, TAGLIO))
    print("  liscio meno la sua retta nella finestra (l'ampiezza di un seno con quella varianza). Un esponenziale da' pendenze di ln s uguali a ogni tratto; un moto uniforme le da' calanti")
    print("  ### il tremolio (la coppia veloce ~0.99) e' aliasato dai campioni ogni 1.5: ln s campione per campione e' rumore, le rette per blocco lo mediano")
    if lunga != "TP1000":
        print("  ### PROVA: %s al posto di TP1000 (il centro euclideo): non e' il referto" % lunga)
    print("=" * 130)
    tutte = {}
    for nome in (lunga, "VIVO", "TA2000"):
        tt, X, ww, fl, T_acc, che, R = dati(nome)
        fine = fine_valida(tt, ww, R, B)
        tutte[nome] = (tt, X, ww, fl, T_acc, fine)
        print("### %s: %s; T_acc %g; i dati fino a %g; %s" % (nome, che, T_acc, tt[-1], ("il primo blocco con 3 w >= %.2f comincia a %g" % (R, fine)) if R is not None and fine <= tt[-1]
                                                                    else ("tutti i blocchi con 3 w < %.2f" % R) if R is not None else "senza il criterio di validita' (il centro euclideo)"))
        logaritmo(nome, tt, X, T_acc, min(fine, tt[-1] + 1.0), B)
    print("-" * 130)
    print("### (ii) LA VELOCITA' CONTRO w, per blocco di %g (|v| per 1000 unita' di tempo; l'angolo dall'asse x; w medio)" % B)
    for nome, (tt, X, ww, fl, T_acc, fine) in tutte.items():
        print("  %s:" % nome)
        for a, b, v, ang, w, _amp in finestre(nome, tt, X, ww, fl, 0.0, min(fine, tt[-1] + 1.0), B, False):
            print("    %7.0f .. %7.0f  w %8.4f  |v| %.4e  angolo %+6.1f" % (a, b, w, v, ang))
    print("-" * 130)
    print("### (iii) L'AMPIEZZA DEL CUORE A FINESTRE DI %g, ACCANTO ALLA VELOCITA' (dalla fine della rampa)" % FIN_AMPIEZZA)
    for nome, (tt, X, ww, fl, T_acc, fine) in tutte.items():
        print("  %s:" % nome)
        for a, b, v, ang, w, amp in finestre(nome, tt, X, ww, fl, T_acc, min(fine, tt[-1] + 1.0), FIN_AMPIEZZA, True):
            print("    %7.0f .. %7.0f  l'ampiezza del cuore %.4e  |v| %.4e  angolo %+6.1f  w %8.4f" % (a, b, amp, v, ang, w))
    print("=" * 130)


if __name__ == "__main__":
    main(sys.argv[1:])
