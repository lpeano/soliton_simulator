# -*- coding: utf-8 -*-
r"""**IL TRIFOGLIO, DOMANDA 1: E' LEGATO? E LA FASE RELATIVA NEL TEMPO** *(Luca `2026-11-14` `23:32`, L1; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `21`)*.

    python csv/solitone/legame.py vuota --registro scena-vuota > <scratchpad>/scena_vuota.txt          (la corsa della scena VUOTA: E0)
    python csv/solitone/legame.py lettura > doc/referti_l2/mattone/legame.txt                          (solo lettura)
    python csv/solitone/legame.py fase > doc/referti_l2/mattone/fase_nel_tempo.txt                     (solo lettura)

### **`vuota`:** **la scena di S162, il bordo da `R_A = 60`, il vuoto fresco al tick `60000`, `psi = 0`** *(`rho = 0`: `N = 1`)*, **G+U** *(`e*`; il campo di Gauss di `rho = 0` e' zero)*, **`2000` tick col tick di
`mattone_cottura.Corsa`; `tot + K + V` a ogni tick in una serie** *(su `E:/soliton_simulator/mattone/lavoro` e nel repo)*.
### **`lettura`:** **`B = E3 - 3 E1 + 2 E0`** *(l'energia = `tot + K + V`; `E3` la MEDIA sugli ultimi `100` tick della tabella R-CONTI di (T-fase) e di (T-sfasati); `E1` quello di (T-solo-60); `E0` della scena vuota, mediato allo stesso modo)*,
**a `0`, `500`, `1000`, `1500`, `2000`; l'errore: la deviazione delle `20` medie da `100` tick della scena vuota, per `sqrt(1 + 9 + 4 + 1)`** *(MIA STIMA: le corse non hanno salvato `tot` per tick; dichiarata)*;
**`B < 0` oltre `3` errori: LEGATO; `B > 0` oltre `3`: NON LEGATO; dentro: INDECISO** *(le soglie del mandato)*; **e `B / M3`.**
### **`fase`:** **negli stati salvati di (T-fase), (T-sfasati)** *(e del video, se c'e')* **a `500`, ..., `2000` e allo stato `0` ricostruito: `arg <psi_i, psi_j>` col pezzo di `i` SPOSTATO sul vertice di `j`**
*(la differenza fra i vertici e' un multiplo di `3`: il disegno del vuoto combacia; i pezzi: i nodi entro `14` nodi dal centro del solitone, mia scelta)*.
"""
import io
import json
import math
import os
import re
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone as MT  # noqa: E402
import mattone_cottura as CT  # noqa: E402
import mattone_triangolo as MTR  # noqa: E402

N_TICK, MEDIA = 2000, 100
PUNTI = (0, 500, 1000, 1500, 2000)
R_PEZZO_FASE = 14.0
DIR_LAVORO = os.path.join(MT.DIR_E, "lavoro")
N_ERR = 3.0


def vuota(nome_reg):
    import _presidio
    import _u1_prototipo as U1
    from solitone import bordo as BO
    for m in ("mattone", "mattone_cottura", "mattone_triangolo"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    t0 = MT.G2.T0
    print("=" * 130)
    print("LA SCENA VUOTA (Luca 23:32, L1): S162, il bordo da R_A %g, il vuoto fresco al tick %d, psi = 0, G+U, %d tick" % (MTR.R_A_SCENA, t0, N_TICK))
    print("=" * 130)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        c0 = Z["bordo"]["c0"]
        Z["g_e"] = BO.g_estremita(Z["z"], c0[0], c0[1], MTR.R_A_SCENA, Z["bordo"]["g_max"])[0]
        MT.vuoto_fresco(Z, t0)
        C = MT.Campi(Z, "MGU", rho_c, e)
        rho = MT.rho_di(Z)
        print("### la massa %.3e (zero); il massimo di rho %.3e" % (float(rho.sum()), float(rho.max())))
        C.campo.E[...] = C.gauss(e * (rho - rho.mean()))
        C.campo.e = e
        C.e_prec = e
        U1.scrivi_U(Z["mot"], C.campo)
        R = CT.Corsa(Z, C)
        R.etichette([c0])
        R.inizio(0)
        t1 = t_tappa = time.time()
        for k in range(1, N_TICK + 1):
            R.passo(k, t0 + k, 1.0, e)
            if k % 250 == 0:
                print("    k %5d  tot %.6f  K+V %.4e  (%.0f s)" % (k, R.T["totd"][-1], R.T["KVd"][-1], time.time() - t1))
                sys.stdout.flush()
            if time.time() - t_tappa >= MT.TAPPA_S:
                MT.tappa(nome_reg, "k %d; %.3f s per tick" % (k, (time.time() - t1) / k))
                t_tappa = time.time()
        R.tabella(["vuoto"])
        T = {x: np.array(v) for x, v in R.T.items()}
    os.makedirs(DIR_LAVORO, exist_ok=True)
    for d in (DIR_LAVORO, MT.DIR_REF):
        np.savez_compressed(os.path.join(d, "scena_vuota_serie.npz"), k=T["k"], E=T["totd"] + T["KVd"], tot=T["totd"], KV=T["KVd"], Mp=T["Mp"], Md=T["Md"])
    print("=" * 130)
    print("ESITO: finita; %.0f s in tutto" % (time.time() - t00))
    return 0


def tabella(f):
    """### Le righe della TABELLA DEI CONTI di un'uscita: `{k: tot + K + V}` *(le medie sugli ultimi `100` tick)*."""
    out, dentro = {}, False
    for r in io.open(f, encoding="utf-8"):
        if "LA TABELLA DEI CONTI" in r:
            dentro = True
            continue
        if dentro:
            m = re.match(r"\s+(\d+)\s+(.*)$", r)
            if not m:
                if r.strip().startswith("k"):
                    continue
                if out:
                    break
                continue
            campi = m.group(2).split()
            out[int(m.group(1))] = float(campi[-4]) + float(campi[-5])     # ### ... K + V, tot, bordo E, residuo, bordo M: l'energia = tot + K + V
    return out


def lettura():
    import _presidio
    _presidio.avvia(__file__)
    ref = MT.DIR_REF
    E1 = tabella(os.path.join(ref, "triangolo_solo.txt"))
    E3 = {v: tabella(os.path.join(ref, "triangolo_%s.txt" % v)) for v in ("fase", "sfasati")}
    s0 = np.load(os.path.join(ref, "scena_vuota_serie.npz"))
    k0, Ev = np.array(s0["k"]), np.array(s0["E"])
    E0 = {p: (float(Ev[k0 == 0][0]) if p == 0 else float(Ev[(k0 > p - MEDIA) & (k0 <= p)].mean())) for p in PUNTI}
    medie = Ev[1:].reshape(-1, MEDIA).mean(axis=1)
    s_m = float(np.std(medie))
    err = s_m * math.sqrt(1 + 9 + 4 + 1)
    print("=" * 130)
    print("IL TRIFOGLIO, DOMANDA 1: E' LEGATO? (Luca 23:32, L1) -- B = E3 - 3 E1 + 2 E0, le energie MEDIE sugli ultimi %d tick; l'errore %.4f (la deviazione delle %d medie della scena vuota %.4f x sqrt(15): MIA STIMA)"
          % (MEDIA, err, len(medie), s_m))
    print("    E1 (T-solo-60): %s" % {p: E1.get(p) for p in PUNTI})
    print("    E0 (la scena vuota): %s" % E0)
    print("=" * 130)
    for v in ("fase", "sfasati"):
        sv = np.load(os.path.join(ref, "triangolo_%s_serie.npz" % v))
        print("### (T-%s)" % v)
        for p in PUNTI:
            if p not in E3[v] or p not in E1:
                print("    k %4d: manca un valore" % p)
                continue
            B = E3[v][p] - 3.0 * E1[p] + 2.0 * E0[p]
            j = int(np.nonzero(sv["k"] == p)[0][0])
            M3 = float(sv["M_A"][j] + sv["M_B"][j] + sv["M_C"][j])
            lett = "LEGATO" if B < -N_ERR * err else ("NON LEGATO" if B > N_ERR * err else "INDECISO")
            print("    k %4d: E3 %.6f  E1 %.6f  E0 %.6f  B %+.4f (%.1f errori)  B / M3 %+.3e  -> %s" % (p, E3[v][p], E1[p], E0[p], B, abs(B) / err, B / M3, lett))
    print("=" * 130)
    return 0


def fase():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "mattone_triangolo.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA FASE RELATIVA NEL TEMPO (Luca 23:32, «ma sono tutti in fase?»; solo lettura): arg <psi_i, psi_j> col pezzo di i (entro %g nodi dal suo centro) SPOSTATO sul vertice di j" % R_PEZZO_FASE)
    print("=" * 130)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L, n, righe = Z["L"], Z["n"], Z["righe"]
        m1, m2 = Z["m1"], Z["m2"]
        for v in ("fase", "sfasati", "video"):
            fs = os.path.join(MT.DIR_REF, "triangolo_%s_serie.npz" % v)
            if not os.path.exists(fs):
                print("### (T-%s): la serie non c'e'" % v)
                continue
            sv = np.load(fs)
            stati = [(k, os.path.join(MT.DIR_E, "triangolo_%s_%05d.npz" % (v, k))) for k in (500, 1000, 1500, 2000)]
            if v not in MTR.VARIANTI:
                print("### (T-%s): i vertici non si rifanno da qui (la variante e' in memoria in triangolo_video.py): saltato" % v)
                continue
            frs = [MTR.francobollo(k) for k in MTR.VARIANTI[v]]
            vertici = MTR.posti(Z["bordo"]["c0"], frs, L)
            print("### (T-%s): i vertici %s" % (v, vertici))
            for k, f in stati:
                if not os.path.exists(f):
                    print("    k %4d: manca %s" % (k, f))
                    continue
                with np.load(f) as d:
                    psi = d["psi_h"]
                j = int(np.nonzero(sv["k"] == k)[0][0])
                cen = [(float(sv["c1_" + q][j]), float(sv["c2_" + q][j])) for q in "ABC"]
                riga = []
                for a, b in ((0, 1), (1, 2), (0, 2)):
                    from solitone import toro as TO
                    dd = np.hypot(*TO.scarti(m1, m2, cen[b][0], cen[b][1], L).T[:2])
                    vb = np.nonzero(dd <= R_PEZZO_FASE)[0]
                    s1, s2 = vertici[b][0] - vertici[a][0], vertici[b][1] - vertici[a][1]
                    va = ((m1[vb] - s1) % L) * L + (m2[vb] - s2) % L
                    z = complex(np.sum(np.conj(psi[righe[va]]) * psi[righe[vb]]))
                    riga.append("%s-%s %+7.1f" % ("ABC"[a], "ABC"[b], math.degrees(math.atan2(z.imag, z.real))))
                print("    k %4d: %s gradi" % (k, "  ".join(riga)))
    print("=" * 130)
    return 0


def main(argv):
    if argv and argv[0] == "vuota":
        return vuota(argv[argv.index("--registro") + 1] if "--registro" in argv else None)
    if argv and argv[0] == "lettura":
        return lettura()
    if argv and argv[0] == "fase":
        return fase()
    raise SystemExit("uso: vuota --registro <nome> | lettura | fase")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
