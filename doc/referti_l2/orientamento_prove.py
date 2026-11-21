# -*- coding: utf-8 -*-
r"""**LE PROVE DELL'ORIENTAMENTO EREDITATO** *(C3 del mandato di Luca `2026-11-21` `23:13`; la carta `doc/TASK_HISTORY/2026-11-21_orientamento_combinatorio.md`, sez. `4.4`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/orientamento_prove.py senza_tick > doc/referti_l2/orientamento_o1_o4_o7.txt
    E:\python\py3132\python.exe doc/referti_l2/orientamento_prove.py corse > doc/referti_l2/orientamento_o2_o3_o5.txt

**`senza_tick`:** **O1** *(l'orientamento del toro ricostruito lungo le `9` nascite = quello di oggi a `k 36250`, triangolo per triangolo; `k`, `l` dall'ordine ciclico = quelli registrati)*; **O4** *(deve fallire: un ciclo invertito a mano nel candidato -> le placchette NON coerenti)*; **O7** *(i due candidati degeneri noti col codice nuovo: nessun AssertionError)*.
**`corse`:** **O2** *(dal tronco `k 35976` col codice nuovo fino a `k 36250`: lo stato AL BIT con `stato_36250` del ramo)*; **O3** *(da `k 36250` fino a `k 36350`: la decima nascita passa; P1, P3, P9, F3 a ogni nascita)*; **O5** *(P8 col codice nuovo: lo scatto forzato dell'arco `40445` a `k 36251`, `10` tick di fila contro `5` + salva + riprendi + `5`; un byte cambiato -> la ripresa rifiuta)*.
"""
import json
import os
import shutil
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import mitosi_rami_v2 as R2  # noqa: E402

ML, MR, MR2, CO, PS = R2.ML, R2.MR, R2.MR2, R2.CO, R2.PS
D_M = os.path.join(R2.BASE, "MITOSI")
F36250 = os.path.join(D_M, "stato_36250.npz")
F_TR = os.path.join(R2.BASE, "TRONCO", "prima_nascita_35976.npz")
D_P = os.path.join(R2.BASE, "PROVA_V2")
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append((che, bool(ok)))
    print("  %-112s %s   %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def fine():
    print("-" * 130)
    for c, ok in ESITI:
        print("  DEVE: %-110s %s" % (c, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _c, ok in ESITI) else 1


def senza_tick():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "mitosi_rami_v2.py"))
    _presidio.avvia(__file__)
    PS.presidi()
    MT = PS.MT
    rho_c, e = MT.rho_c_assoluto(), MT.PB.E_DECISO
    print("=" * 130)
    print("O1, O4, O7 DELL'ORIENTAMENTO EREDITATO (Luca 2026-11-21 23:13; la carta sez. 4.4): senza tick, dallo stato %s" % F36250)
    print("=" * 130)
    with open(os.path.join(D_M, "nascite_36250.json"), encoding="utf-8") as fh:
        B = json.load(fh)
    with PS.CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        ori0 = R2.ori_toro(Z)
        C, NS, meta, cs = ML.riprendi(Z, F36250, rho_c, e, True)
        PS.PO.accendi(cs)
        try:
            oggi = CO.orientamento_da_vec(C.campo)
            ori, dkl = MR2.ricostruisci(ori0, B)
            diversi = [x for x in set(ori) | set(oggi) if ori.get(x) != oggi.get(x)]
            print("### O1: il toro %d triangoli; lungo le %d nascite: %d triangoli ricostruiti, %d oggi (dal prodotto vettoriale); diversi %d; k/l dall'ordine ciclico diversi da quelli registrati: %s" % (
                len(ori0), len(B), len(ori), len(oggi), len(diversi), dkl or "nessuno"))
            esito("O1: l'orientamento ereditato lungo le 9 nascite = quello di oggi, triangolo per triangolo (0 diversi)", not diversi and len(ori) == len(oggi), "%d" % len(diversi))
            esito("O1: k e l dall'ordine ciclico = quelli registrati, nascita per nascita (0 diversi)", not dkl, "%d" % len(dkl))
            C.campo = CO.orientato_da(C.campo, ori)
            import _u1_prototipo as U1
            U1.scrivi_U(Z["mot"], C.campo)
            ii, jj = np.asarray(Z["mot"].inc.nodo[0::2]), np.asarray(Z["mot"].inc.nodo[1::2])
            # ### O7: i due candidati degeneri noti
            for a, q in ((40445, 0), (103798, 3)):
                i, j, k, l = MR2.indici_nascita_v2(ii, jj, C.campo.ori, a)
                lati = ((i, k), (j, k), (j, l), (i, l))
                try:
                    S = MR2.candidato(Z, C, a, lati[q], "stella")
                    n = S["nodi"]["n"]
                    nuovi = sorted(v for kk, v in S["ori"].items() if n in kk)
                    eu, dp, tri, _g = MR.grafo_ok(S["ii"], S["jj"], n + 1)
                    print("### O7: l'arco %d (%d -> %d), la stella i %d j %d k %d l %d, il flip %d %s: NESSUN AssertionError; i triangoli col nodo nuovo %d (cicli ereditati): %s; F3 Eulero %s, doppi no %s, due triangoli %s, coerenti %s; il residuo di Gauss %.2e" % (
                        a, ii[a], jj[a], i, j, k, l, q, lati[q], n, nuovi, eu, dp, tri, S["coerenti"], S["res"]))
                    esito("O7: il candidato degenere noto (l'arco %d, il flip %d) passa senza AssertionError, F3 vero" % (a, q), eu and dp and tri and S["coerenti"])
                except AssertionError as ex:
                    print("### O7: l'arco %d il flip %d: ### AssertionError: %s" % (a, q, ex))
                    esito("O7: il candidato degenere noto (l'arco %d, il flip %d) passa senza AssertionError, F3 vero" % (a, q), False)
            # ### O4: deve fallire
            a = 40445
            i, j, k, l = MR2.indici_nascita_v2(ii, jj, C.campo.ori, a)
            n = int(Z["mot"].inc.n)
            try:
                S = MR2.candidato(Z, C, a, None, "stella", inverti=(i, n, k))
                cade = (not S["coerenti"]) or S["res"] > 10 * MR.residuo(C.campo, MT.rho_di(Z))
                print("### O4 (deve fallire): il ciclo del triangolo (%d, %d, %d) invertito a mano: coerenti %s, il residuo %.2e" % (i, n, k, S["coerenti"], S["res"]))
            except AssertionError as ex:
                cade = True
                print("### O4 (deve fallire): il ciclo invertito a mano: ALZA (%s)" % ex)
            esito("O4 DEVE FALLIRE: un ciclo invertito a mano -> F3 (le placchette non coerenti) o P3 cadono", cade)
        finally:
            PS.LC.spegni()
    return fine()


def confronta(fine_, f_vecchio):
    with np.load(f_vecchio) as d:
        X = {x: d[x] for x in d.files}
        meta = json.loads(str(X.pop("meta")))
    diversi = []
    for x in ("Lambda", "h_int", "phi_h", "psi", "psi_h", "rho"):
        if not np.array_equal(fine_[x], X[x]):
            diversi.append(x)
    for a, b in (("A", "campo_A"), ("E", "campo_E"), ("theta", "theta_a"), ("ii", "ii"), ("jj", "jj"), ("geo", "geo_n"), ("m1", "m1"), ("m2", "m2"), ("gauss_acc", "gauss_acc"), ("cs_prec", "cs_prec")):
        if fine_[a] is None or b not in X or not (np.shape(fine_[a]) == np.shape(X[b]) and np.array_equal(fine_[a], X[b])):
            diversi.append(a)
    if float(fine_["E_persa"][0]) != float(meta["E_persa"]):
        diversi.append("E_persa")
    return diversi


def corse():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "mitosi_rami_v2.py"))
    _presidio.avvia(__file__)
    PS.presidi()
    if os.path.isdir(D_P):
        shutil.rmtree(D_P)
    print("=" * 130)
    print("O2, O3, O5 DELL'ORIENTAMENTO EREDITATO (Luca 2026-11-21 23:13; la carta sez. 4.4): le corse col codice nuovo")
    print("=" * 130)
    # ### O2
    _c, k, fin = R2.ciclo("O2", "mitosi", F_TR, 36250, None, d_out=os.path.join(D_P, "o2"))
    dd = confronta(fin, F36250)
    print("### O2: dal tronco k 35976 col codice nuovo fino a k %d contro %s (sha1 %s): %s" % (k, os.path.basename(F36250), ML.sha1(F36250)[:8], "AL BIT (ogni array, il grafo, i versori, Theta, le posizioni, gauss_acc, cs_prec, E_persa)" if not dd else "### DIVERSE: %s" % dd))
    esito("O2: lo stato a k 36250 col codice nuovo = quello del ramo AL BIT", not dd)
    if dd:
        print("### O2 non passa: FERMO (il mandato)")
        return fine()
    # ### O3
    _c, k, fin = R2.ciclo("O3", "mitosi", F36250, 36350, None, d_out=os.path.join(D_P, "o3"))
    with open(os.path.join(D_P, "o3", "nascite_%05d.json" % 36350), encoding="utf-8") as fh:
        B = json.load(fh)
    dopo = [b for b in B if b["k"] > 36250]
    for b in dopo:
        print("    la nascita (k %d, l'arco %d): r %.2f, %d passi; P9 %.1e; F3 %s; il residuo di Gauss %.2e; E_persa %+.6e" % (b["k"], b["a"], b["r"], b["passi"], b["P9"], b["F3"], b["res"], b["E_persa"]))
    ok3 = len(B) >= 10 and all(b["P9"] == 0.0 and b["F3"] for b in dopo)
    print("### O3: da k 36250 fino a k 36350: %d nascite in tutto (%d dopo k 36250); la decima %s" % (len(B), len(dopo), ("a k %d, r %.2f (l'arco %d)" % (B[9]["k"], B[9]["r"], B[9]["a"])) if len(B) >= 10 else "### NON c'e'"))
    esito("O3: la decima nascita passa; P9 a 0 e F3 a ogni nascita", ok3)
    # ### O5
    KF, KM, KE = 36251, 36255, 36260
    _c, _k, fila = R2.ciclo("O5_fila", "mitosi", F36250, KE, None, forza=(KF, 40445), d_out=os.path.join(D_P, "o5_fila"))
    _c, _k, _p = R2.ciclo("O5_prima", "mitosi", F36250, KM, None, forza=(KF, 40445), d_out=os.path.join(D_P, "o5_spezza"))
    fm = os.path.join(D_P, "o5_spezza", "stato_%05d.npz" % KM)
    with np.load(fm) as d:
        ha_ori = "ori_cicli" in d.files
    _c, _k, rip = R2.ciclo("O5_dopo", "mitosi", fm, KE, None, d_out=os.path.join(D_P, "o5_spezza"))
    dd = ML.diverse({x: fila[x] for x in fila}, {x: rip[x] for x in rip})
    print("### O5: %d tick di fila contro la ripresa da %s (ori_cicli nello stato %s): %s" % (KE - 36250, os.path.basename(fm), ha_ori, "AL BIT" if not dd else "### DIVERSE: %s" % dd))
    esito("O5: la ripresa dopo una nascita col codice nuovo AL BIT (l'orientamento nello stato)", not dd and ha_ori)
    fr = os.path.join(D_P, "o5_rotto", "stato_%05d.npz" % KM)
    os.makedirs(os.path.dirname(fr), exist_ok=True)
    shutil.copyfile(fm, fr)
    shutil.copyfile(fm + ".sha1", fr + ".sha1")
    with open(fr, "r+b") as fh:
        fh.seek(os.path.getsize(fr) // 2)
        x = fh.read(1)
        fh.seek(os.path.getsize(fr) // 2)
        fh.write(bytes([x[0] ^ 0x01]))
    rifiuta = False
    with PS.CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        try:
            R2.riprendi_v2(Z, fr, PS.MT.rho_c_assoluto(), PS.MT.PB.E_DECISO, True)
        except AssertionError as ex:
            rifiuta = "sha1" in str(ex)
            print("### O5 DEVE FALLIRE: un byte cambiato: %s" % ex)
    esito("O5 DEVE FALLIRE: un byte dello stato cambiato -> la ripresa RIFIUTA (lo sha1)", rifiuta)
    return fine()


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else ""
    sys.exit({"senza_tick": senza_tick, "corse": corse}[q]())
