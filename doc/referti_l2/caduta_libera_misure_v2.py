# -*- coding: utf-8 -*-
r"""**[M0908-M] [M1052-S] LE MISURE DELLA CADUTA LIBERA -- LA V2: IN PIU' LA SPINTA PER REGIONE** *(la richiesta di Luca delle `10:40`, il mandato [M1052] delle `10:52`; la carta sez. `4`: l'impulso `P_R = somma Jy` negli anelli dal baricentro DELLO STATO, nucleo `r < 15`, guscio `15-21`, bordo `21-25`, fuori `>= 25`; la variazione fra stati, la cumulata, al netto di V0; il caso noto di V0 e della somma; il bivio; la v1, 54b1ab48, non e' girata; il resto la v1 riga per riga)*. **IL TITOLO DELLA V1: LE MISURE DELLA CADUTA LIBERA E IL FILM LEGGERO** *(il mandato di Luca [M0908] `2026-11-22` `09:08`; la carta `doc/TASK_HISTORY/2026-11-22_caduta_libera.md`, sez. `2.3`; SOLA LETTURA)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/caduta_libera_misure_v2.py > doc/referti_l2/caduta_libera.txt

**Per ogni variante** *(`CHI/caduta/<V>`, gli stati `0, 250, ..., 2000`, lo sha1 controllato)*: il baricentro di `rho` *(tutto il toro, l'immagine piu' vicina al centro del `meta`)* e il nodo di `rho` massimo lisciato sui `7` nodi; **la componente `y`** *(lungo il gradiente)* e, per controllo, la `x`; il fit `y0 + v k + a k^2/2` *(`gravita_due_corpi_misure.fit`)*; **`a - a(V0)`** con l'errore in quadratura; **il verso:** VERSO `N` piu' basso se `a - a(V0)` ha il segno di `segno_chi` *(con `A > 0` `chi` cresce verso `+y` sotto il mattone)*; **lo specchio** `a(V1) + a(V1m)` *(al netto di V0)*; il confronto con `c^2 |dN/dy|` per `c = 0.588 s` e `c = s`. **Il film:** `rho`, `Jx`, `Jy` per stato *(lo strumento del flusso di `gravita_due_corpi_misure`, col `cs` e la fase della variante)*, `chi` una volta: `doc/referti_l2/film/caduta_<V>.npz`.
"""
import hashlib
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import chi_tick as CT  # noqa: E402
import caduta_libera as CL  # noqa: E402
import gravita_due_corpi_misure as GM  # noqa: E402

ORDINE = ("V0", "V1", "V2", "V3", "V4", "V1m")
KS = tuple(range(0, 2001, 250))
FILM = os.path.join(_QUI, "film")
C_MATERIA = 0.588              # ### il mandato: v_max della materia = 0.588 s
REGIONI = ((0.0, 15.0, "nucleo"), (15.0, 21.0, "guscio"), (21.0, 25.0, "bordo"), (25.0, float("inf"), "fuori"))      # ### Luca 10:40


def sha1(f):
    return hashlib.sha1(open(f, "rb").read()).hexdigest()


def leggi(f):
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == sha1(f), "lo sha1 di %s NON coincide" % f
    z = np.load(f)
    X = {x: z[x] for x in z.files}
    return X, json.loads(str(X.pop("meta")))


def main():
    import _presidio
    import _u1_prototipo as U1
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "caduta_libera.py"))
    _presidio.avvia(os.path.join(_QUI, "gravita_due_corpi_misure.py"))
    _presidio.avvia(__file__)
    MT = TC.moduli()[0]
    rho_c, e = MT.rho_c_assoluto(), MT.PB.E_DECISO
    print("=" * 130)
    print("[M0908-M] LA CADUTA LIBERA (la carta sez. 2.3): le sei varianti, gli stati 0 ... 2000 ogni 250; y lungo il gradiente (0, 1)")
    print("=" * 130)
    RIS, REG = {}, {}
    with TC.scena() as Z:
        mot = Z["mot"]
        n, L = mot.inc.n, Z["L"]
        nodo = np.asarray(mot.inc.nodo)
        A1, A2 = TO.vettori()
        A1, A2 = np.asarray(A1, float)[:2], np.asarray(A2, float)[:2]
        vett = np.stack([A1, A2, A1 + A2])
        m1, m2 = np.asarray(Z["m1"], float), np.asarray(Z["m2"], float)
        cam = MT.Campi(Z, "MGU", rho_c, e).campo
        sp = mot.operatori["spostamento_trasporto"]
        cs0 = mot.cs
        for nome in ORDINE:
            d = os.path.join(CL.BASE, nome)
            fs = [os.path.join(d, "stato_%06d.npz" % k) for k in KS]
            if not all(os.path.exists(f + ".sha1") for f in fs):
                print("### %s: gli stati non ci sono tutti (la corsa non e' finita): saltata" % nome)
                continue
            print("-" * 130)
            X0, meta0 = leggi(fs[0])
            c = meta0["centro"]
            dxy = TO.scarti(m1, m2, c[0], c[1], L)[:, :2]
            N = X0["N"]
            cs_N, segno, segno_chi = bool(meta0["cs_N"]), int(meta0["segno_fase"]), float(meta0["segno_chi"])
            s, e0, kappa, A, Ly = float(meta0["s"]), float(meta0["e0"]), float(meta0["kappa"]), float(meta0["A"]), float(meta0["L_y"])
            gN = kappa * A * 2.0 * math.pi / Ly if meta0["acceso"] else 0.0
            print("### %s: il centro %s, y_c %.6f; cs %s, la fase (a) %+d, chi x %+g; A %.6e; |dN/dy| allo zero %.6e; N da %.10f a %.10f" % (
                nome, c, float(meta0["y_c"]), "s N" if cs_N else "s", segno, segno_chi, A, gN, float(N.min()), float(N.max())))
            yb, xb, ym, F, righe = [], [], [], {}, []
            PR, MR, PT = [], [], []                                                    # ### V2: l'impulso e la massa per regione, l'impulso totale
            for k, f in zip(KS, fs):
                X, meta = leggi(f)
                rho = np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
                bari = (dxy * rho[:, None]).sum(axis=0) / rho.sum()
                g = rho.reshape(L, L)
                lis = ((g + sum(np.roll(np.roll(g, a, 0), b, 1) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)))) / 7.0).reshape(-1)
                mx = dxy[int(np.argmax(lis))]
                yb.append(float(bari[1]))
                xb.append(float(bari[0]))
                ym.append(float(mx[1]))
                righe.append((k, bari, mx, float(rho.sum())))
                # ### il flusso (lo strumento di gravita_due_corpi_misure, col cs e la fase della variante)
                Z["metti"]({x: X[x] for x in Z["chiavi"]})
                cam.A[...] = X["campo_A"]
                mot.cs = s * N if cs_N else np.full(n, s)
                mot.lambda_c = None
                if segno:
                    CT.fase_a(mot, Z["st"], float(segno) * e0, N)
                U1.scrivi_U(mot, cam)
                mm = cam.m
                prima = np.sum(np.abs(Z["st"]["psi_h"].reshape(mm, 2, 2)[:, 0, :]) ** 2, axis=1).copy()
                sp(Z["st"], Z["par"], 0.5)
                J = np.sum(np.abs(Z["st"]["psi_h"].reshape(mm, 2, 2)[:, 0, :]) ** 2, axis=1) - prima
                Z["metti"]()
                Jn = (J.reshape(n, 3)[:, :, None] * vett[None, :, :]).sum(axis=1)
                rb = np.hypot(*(dxy - bari).T)                                         # ### V2: r dal baricentro DELLO STATO
                PR.append([float(Jn[(rb >= a) & (rb < b), 1].sum()) for a, b, _n in REGIONI])
                MR.append([float(rho[(rb >= a) & (rb < b)].sum()) for a, b, _n in REGIONI])
                PT.append(float(Jn[:, 1].sum()))
                sfx = "_%06d" % k
                F["rho" + sfx] = rho.astype(np.float32)
                F["Jx" + sfx], F["Jy" + sfx] = Jn[:, 0].astype(np.float32), Jn[:, 1].astype(np.float32)
            mot.cs = cs0
            mot.lambda_c = None
            for k, b, mx, M in righe:
                print("    k %4d  il baricentro (x, y) %+.5f %+.5f   il rho massimo lisciato (x, y) %+.4f %+.4f   la norma %.6f" % (k, b[0], b[1], mx[0], mx[1], M))
            fy, fx, fm = GM.fit(KS, np.array(yb)), GM.fit(KS, np.array(xb)), GM.fit(KS, np.array(ym))
            print("    il fit sul baricentro, y: y0 %+.5f, v %+.4e, a %+.4e +- %.2e (il residuo rms %.3e); x (il controllo): a %+.4e +- %.2e; sul rho massimo, y: a %+.4e +- %.2e (il residuo rms %.3e)" % (
                fy[0], fy[1], fy[2], fy[3], fy[4], fx[2], fx[3], fm[2], fm[3], fm[4]))
            RIS[nome] = (fy, fm, fx, segno_chi, gN, s)
            REG[nome] = (np.array(PR), np.array(MR), np.array(PT), np.array(yb), float(righe[0][3]))     # ### V2
            F.update(k=np.array(KS, dtype=np.int32), L=np.array(L), m1=m1.astype(np.float32), m2=m2.astype(np.float32), chi=X0["chi"].astype(np.float32), variante=np.array(nome))
            ff = os.path.join(FILM, "caduta_%s.npz" % nome)
            np.savez_compressed(ff, **F)
            print("    il film %s: %.2f MB (sha1 %s)" % (os.path.relpath(ff, _QUI), os.path.getsize(ff) / 1e6, sha1(ff)[:8]))
            assert os.path.getsize(ff) <= 50e6, "sopra i 50 MB: FERMO"
        Z["metti"]()
    print("=" * 130)
    print("IL CONFRONTO: a - a(V0) lungo y, l'incertezza in quadratura; VERSO N piu' basso se ha il segno di chi x; fuori dall'incertezza se |a - a(V0)| > 2 sigma")
    print("=" * 130)
    netti = {}
    if "V0" in RIS:
        for i, che in ((0, "il baricentro"), (1, "il rho massimo")):
            a0, s0 = RIS["V0"][i][2], RIS["V0"][i][3]
            print("  V0, %-15s a %+.4e +- %.2e: %s" % (che, a0, s0, "entro 3 sigma da 0" if abs(a0) <= 3.0 * s0 else "### OLTRE 3 sigma da 0"))
            for nome in ORDINE[1:]:
                if nome not in RIS:
                    print("  %s: manca" % nome)
                    continue
                fy, fm, fx, segno_chi, gN, s = RIS[nome]
                a, sg = RIS[nome][i][2], RIS[nome][i][3]
                da, sd = a - a0, math.hypot(sg, s0)
                netti[(nome, i)] = (da, sd)
                verso = "VERSO N piu' basso (la caduta)" if da * segno_chi > 0 else "VIA da N piu' basso (la repulsione)"
                print("  %-3s %-15s a %+.4e +- %.2e; a - a(V0) %+.4e +- %.2e: %s%s; |a - a(V0)| / (c^2 |dN/dy|) = %.3f (c = %.3f s), %.3f (c = s)" % (
                    nome, che, a, sg, da, sd, verso, " (fuori dall'incertezza)" if abs(da) > 2.0 * sd else " (DENTRO l'incertezza)",
                    abs(da) / ((C_MATERIA * s) ** 2 * gN), C_MATERIA, abs(da) / (s * s * gN)))
            if ("V1", i) in netti and ("V1m", i) in netti:
                (p, sp_), (q, sq) = netti[("V1", i)], netti[("V1m", i)]
                sm, ss = p + q, math.hypot(sp_, sq)
                print("  LO SPECCHIO, %s: (a - a(V0)) di V1 + di V1m = %+.4e +- %.2e: %s" % (che, sm, ss, "opposti entro l'incertezza" if abs(sm) <= 2.0 * ss else "### NON opposti"))
    else:
        print("  V0 manca: nessun confronto")
    return regioni(REG, RIS, netti)


def regioni(REG, RIS, netti):
    """### V2 [M1052-S]: la spinta per regione, il caso noto, il bivio *(la carta sez. 4.2)*."""
    ESITI = []
    nomi = [r[2] for r in REGIONI]
    print("=" * 130)
    print("[M1052-S] LA SPINTA PER REGIONE: P_R = somma Jy negli anelli dal baricentro dello stato (%s)" % ", ".join("%s %g-%g" % (r[2], r[0], r[1]) for r in REGIONI))
    print("=" * 130)
    for nome in ORDINE:
        if nome not in REG:
            continue
        PR, MR, PT, yb, M = REG[nome]
        print("  %s: la massa per regione a k 0 %s (le quote %s)" % (nome, ", ".join("%s %.4e" % (a, b) for a, b in zip(nomi, MR[0])), ", ".join("%.4f" % (b / MR[0].sum()) for b in MR[0])))
        print("      k     " + "  ".join("%-24s" % ("dP %s (cumulata)" % a) for a in nomi) + "  la somma, il totale; P/M contro v del baricentro")
        for i, k in enumerate(KS):
            dP = PR[i] - PR[i - 1] if i else np.zeros(4)
            vb = (yb[min(i + 1, len(KS) - 1)] - yb[max(i - 1, 0)]) / (KS[min(i + 1, len(KS) - 1)] - KS[max(i - 1, 0)])
            print("    %5d   " % k + "  ".join("%+.3e (%+.3e)  " % (dP[j], PR[i, j] - PR[0, j]) for j in range(4)) + "  %+.4e %+.4e; %+.4e contro %+.4e" % (PR[i].sum(), PT[i], PT[i] / M, vb))
    if "V0" in REG:
        PR0 = REG["V0"][0]
        dP0 = np.diff(PR0, axis=0)
        z = [abs(float(dP0[:, j].mean())) / (float(dP0[:, j].std(ddof=1)) / np.sqrt(len(dP0))) for j in range(4)]
        print("  IL CASO NOTO (i), V0: la media delle %d variazioni per regione in errori standard: %s" % (len(dP0), ", ".join("%s %.2f" % (a, b) for a, b in zip(nomi, z))))
        ESITI.append(("S CASO NOTO (i): in V0 la spinta per regione e' zero entro il rumore (ogni regione entro 3 errori standard)", all(x <= 3.0 for x in z)))
    som = max(abs(REG[x][0].sum(axis=1) - REG[x][2]).max() / max(abs(REG[x][2]).max(), 1e-300) for x in REG)
    ESITI.append(("S CASO NOTO (ii): la somma delle regioni = la spinta totale entro l'1%% (PER COSTRUZIONE: un controllo del codice; lo scarto relativo %.2e)" % som, som <= 0.01))
    if "V0" in REG:
        print("  AL NETTO DI V0, la cumulata a k %d per regione (e la quota in valore assoluto):" % KS[-1])
        for nome in ORDINE[1:]:
            if nome not in REG:
                continue
            C = (REG[nome][0][-1] - REG[nome][0][0]) - (PR0[-1] - PR0[0])
            tot = float(C.sum())
            quota = (abs(C[1]) + abs(C[2])) / float(np.abs(C).sum())
            mq = float((REG[nome][1][0][1] + REG[nome][1][0][2]) / REG[nome][1][0].sum())
            print("    %-3s %s; il totale %+.4e; (|guscio| + |bordo|) / somma |.| = %.4f; |guscio + bordo| / |totale| = %.4f; la quota di massa del guscio e del bordo %.4f; il segno del totale lungo chi x %+g: %s" % (
                nome, ", ".join("%s %+.4e" % (a, b) for a, b in zip(nomi, C)), tot, quota, abs(C[1] + C[2]) / abs(tot), mq, RIS[nome][3], "VERSO N piu' basso" if tot * RIS[nome][3] > 0 else "VIA"))
            if nome == "V1":
                sg = [netti.get(("V1", i)) for i in (0, 1)]
                opposti = bool(sg[0] and sg[1] and sg[0][0] * sg[1][0] < 0 and abs(sg[0][0]) > 2 * sg[0][1] and abs(sg[1][0]) > 2 * sg[1][1])
                print("  IL BIVIO (V1): la quota %.4f %s 0.5; il baricentro e il rho massimo (a - a(V0)) %s e %s: %s; LA LETTURA: %s" % (
                    quota, ">" if quota > 0.5 else "<=", "%+.3e +- %.1e" % sg[0] if sg[0] else "-", "%+.3e +- %.1e" % sg[1] if sg[1] else "-",
                    "segni opposti fuori dall'incertezza" if opposti else "non opposti fuori dall'incertezza", "LA SPINTA STA ALL'INTERFACCIA" if (quota > 0.5 or opposti) else "LA SPINTA STA NEL VOLUME"))
    print("-" * 130)
    for c, ok in ESITI:
        print("  DEVE: %-110s %s" % (c, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _c, ok in ESITI) else 1


if __name__ == "__main__":
    sys.exit(main())
