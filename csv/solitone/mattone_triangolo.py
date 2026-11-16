# -*- coding: utf-8 -*-
r"""**IL TRIANGOLO: TRE SOLITONI INSIEME PERDONO MENO DI UNO SOLO?** *(Luca `2026-11-14` `14:22`, T1-T6; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `18`)*.

    python csv/solitone/mattone_triangolo.py corsa --variante solo|fase|sfasati --registro triangolo-<variante> > <scratchpad>/triangolo_<variante>.txt   (poi doc/referti_l2/mattone/triangolo_<variante>.txt)
    python csv/solitone/mattone_triangolo.py referto > doc/referti_l2/mattone/triangolo.txt

### **`corsa`:** **tre francobolli di (MGU)** *((T-fase): tre copie di `MGU_10000`; (T-sfasati): `MGU_08000`, `MGU_09000`, `MGU_10000`; (T-solo), Luca `14:32`: UN solo `MGU_10000` al vertice A, il riferimento isolato)* **nella scena di S162** *(la scena e il bordo di S7'', il vuoto fresco al tick
`60000`)*, **in un triangolo equilatero di lato `37.6` centrato sul centro del BORDO** *(mio: il bordo assorbe fuori da `R_A` attorno a quel centro)*; ### **il bordo da `R_A = 60`** *(Luca `15:49`, n.161; quello della scena e' `47.5`)*, **i centri al nodo piu'
vicino con lo spostamento multiplo di `3`; la materia per SOMMA, il vuoto per PRODOTTO** *(`mattone_coppia`, `c1740faa`)*; **G+U a campi pieni dal tick `0`, U con Gauss** *(`A = 0`, e `U` dal campo con
`_u1_prototipo.scrivi_U`, `d9318470`: con `A = 0` e' `I`)*; **`2000` tick col tick di `mattone_cottura.Corsa`** *(i conti R-CONTI)*.
**T3:** **per ogni solitone ogni `50` tick la massa del suo pezzo** *(i nodi entro `28` dal centro PIU' VICINO: una partizione, `conti.etichette`)*, **il raggio** *(`mattone_rhoc.raggio`, entro `28`: con i vicini a `37.6`
ci entra la coda degli altri, dichiarato)*, **il centro; il picco di ogni solitone A OGNI TICK; la massa uscita dal bordo; i tre lati.**
### **(T-solo) e' anche LA COTTURA SU `L 162`** *(Luca `14:54`)*: **lo stato ogni `500` tick col prefisso `L162_MGU_`; a `2000` tick, e poi ogni `1000` fino a `4000` in piu', COTTO se il picco medio fra le ultime due finestre di `500` cambia meno del `2%`; `doc/referti_l2/mattone/cottura_L162_MGU.json`.**
### **DEVE:** **un solo francobollo: la somma e il prodotto = `mattone.incolla` AL BIT; Gauss sotto `1e-10` a ogni controllo; (T-fase) al tick `0` le masse dei tre francobolli incollati DA SOLI uguali entro
`1e-10` relativo** *(mia lettura di «la stessa massa»: le masse dei pezzi della partizione dipendono dalle code sovrapposte e dai nodi arrotondati, e si scrivono a parte)*.
"""
import argparse
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import conti as CO  # noqa: E402
import mattone as MT  # noqa: E402
import mattone_cottura as CT  # noqa: E402
import mattone_cottura_U as CU  # noqa: E402,F401  (il caricamento che ricostruisce U: qui il campo e' rifatto con A = 0)
import mattone_rhoc as MR  # noqa: E402

VARIANTI = {"fase": (10000, 10000, 10000), "sfasati": (8000, 9000, 10000), "solo": (10000,)}   # ### T1; (T-solo): Luca 14:32, il riferimento isolato (al vertice A)
LATO = 37.6                              # ### T2
N_TICK, OGNI, FIN = 2000, 50, 250
FINESTRA_LETTURA = (250, 1250)           # ### T4: la finestra di S7''
PROTEGGE, PEGGIORA = 0.70, 1.30          # ### T4: le soglie del guardiano
TOLL_MASSA0 = 1e-10                      # ### il DEVE di (T-fase)
COTTO_L162, PIU_L162, PEZZO_L162 = 0.02, 4000, 1000   # ### Luca 14:54: (T-solo) e' anche la COTTURA SU L 162 (il picco medio fra le ultime due finestre di 500 entro il 2%; al piu' 4000 tick in piu', a pezzi di 1000)
NOMI = ("A", "B", "C")
R_A_SCENA = 60.0                         # ### Luca 15:49 (n.161): il bordo da R_A 60 dal centro del bordo della scena (R_B la meta' del periodo, 81); bordo.py NON si tocca
TETTO_S = 28800.0                        # ### Luca 15:22: le corse col lapse in parallelo, il tetto 8 ore
DIR_LAVORO = os.path.join(MT.DIR_E, "lavoro")   # ### il json della cottura su L 162 FUORI dal repo (copiato a corsa chiusa)
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota, deve):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-100s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:100], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def francobollo(k):
    """### Il francobollo dello stato `MGU_<k>` *(come `mattone.controllo`)*."""
    f = os.path.join(MT.DIR_E, "MGU_%05d.npz" % k)
    with MT.scena(MT.CORSA_BASE, MT.T_BASE) as Z81:
        with np.load(f) as d:
            Z81["metti"]({x: d[x] for x in Z81["chiavi"]})
        rho81 = MT.rho_di(Z81)
        c81 = MT.centro_di(Z81, rho81)
        st81 = {x: Z81["st"][x].copy() for x in Z81["chiavi"]}
        MT.vuoto_fresco(Z81, MT.T_BASE + k)
        phi_rif81 = Z81["st"]["phi_h"].copy()
        Z81["metti"](st81)
        fr = MT.ritaglia(Z81, c81, phi_rif81)
        fr["raggio81"] = MR.raggio(Z81, rho81, c81)
        fr["file"] = f
    return fr


def posti(c0, frs, L):
    """### **T2:** i tre vertici di un triangolo equilatero di lato `LATO` attorno a `c0` *(gli indici)*; per ognuno il nodo piu' vicino con `(nodo - centro del francobollo) % 3 == 0`."""
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    B = np.column_stack([A1, A2])
    R = LATO / math.sqrt(3.0)
    out = []
    for j, fr in enumerate(frs):
        th = math.pi / 2.0 + 2.0 * math.pi * j / 3.0
        a = np.linalg.solve(B, np.array([R * math.cos(th), R * math.sin(th)]))
        tgt = (c0[0] + a[0], c0[1] + a[1])
        best = None
        for n1 in range(int(math.floor(tgt[0])) - 3, int(math.floor(tgt[0])) + 4):
            for n2 in range(int(math.floor(tgt[1])) - 3, int(math.floor(tgt[1])) + 4):
                if (n1 - fr["centro"][0]) % 3 or (n2 - fr["centro"][1]) % 3:
                    continue
                p = (n1 - tgt[0]) * A1 + (n2 - tgt[1]) * A2
                dd = float(np.hypot(p[0], p[1]))
                if best is None or dd < best[0]:
                    best = (dd, n1 % L, n2 % L)
        out.append([best[1], best[2]])
    return out


def copie_oltre(centri, L):
    """### La distanza minima fra un solitone e una COPIA oltre il bordo *(di se' o degli altri: le immagini diverse dalla piu' vicina)*."""
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    pos = [c[0] * A1 + c[1] * A2 for c in centri]
    im = TO.immagini(L)
    m = float("inf")
    for i in range(len(centri)):
        for j in range(len(centri)):
            D = pos[i] - pos[j]
            dd = np.hypot(*(D[None, :] + im).T)
            dd = np.sort(dd)
            m = min(m, float(dd[1] if i == j else dd[1]))       # ### la piu' vicina e' la «vera» (o zero per se'): si prende la seconda
    return m


def centri_pezzi(Z, rho, centri_prec):
    """### I centri dei tre solitoni: il centro periodico di `rho` sul pezzo di ciascuno *(la partizione attorno ai centri di prima)*."""
    from solitone import toro as TO
    lab = CO.etichette(Z, centri_prec)
    return [TO.centro(np.where(lab == j, rho, 0.0), Z["m1"], Z["m2"], Z["L"])[:2] for j in range(len(centri_prec))], lab


def corsa(variante, nome_reg):
    import _presidio
    import _u1_prototipo as U1
    import _vuoto_vivo_B as V
    for m in ("mattone", "mattone_cottura", "mattone_cottura_U", "mattone_rhoc", "conti"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(os.path.join(_CSV, "_u1_prototipo.py"))
    _presidio.avvia(__file__)
    assert variante in VARIANTI
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    stati = VARIANTI[variante]
    frs = [francobollo(k) for k in stati]
    print("=" * 130)
    print("IL TRIANGOLO (T-%s; Luca 14:22): %s nella scena di %s (il vuoto fresco al tick %d); il lato %g; G+U a campi pieni; rho_c %.6f, e %.7e; %d tick"
          % (variante, ["MGU_%05d" % k for k in stati], MT.CORSA_162, MT.G2.T0, LATO, rho_c, e, N_TICK))
    print("=" * 130)
    for j, fr in enumerate(frs):
        print("### il francobollo %s (%s): R_t %.1f; %d nodi; il centro d'origine %s; il raggio a L 81 %.4f" % (NOMI[j], fr["file"], fr["R_t"], len(fr["w"]), fr["centro"], fr["raggio81"]))
    if variante == "sfasati":
        rr = [fr["raggio81"] for fr in frs]
        print("    i raggi diversi: dal minimo al massimo %.3f%%" % (100.0 * (max(rr) - min(rr)) / min(rr)))
    nomi = NOMI[:len(stati)]
    tre = len(stati) == 3
    S = {x: [] for x in ("k", "l_AB", "l_BC", "l_CA", "gauss") + tuple("%s_%s" % (q, n) for q in ("M", "raggio", "c1", "c2") for n in nomi)}
    PK = {n: [] for n in nomi}
    t0 = MT.G2.T0
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        st, L = Z["st"], Z["L"]
        c0 = Z["bordo"]["c0"]
        from solitone import bordo as BO
        from solitone import toro as TO
        print("### IL BORDO (Luca 15:49): quello della scena di S162 ha R_A %.3f; QUI R_A %g attorno allo STESSO centro, R_B %g, g_max %g (bordo.g_estremita, l'argomento)" % (Z["bordo"]["R_A"], R_A_SCENA, TO.meta_periodo(L), Z["bordo"]["g_max"]))
        Z["g_e"] = BO.g_estremita(Z["z"], c0[0], c0[1], R_A_SCENA, Z["bordo"]["g_max"])[0]
        centri = posti(c0, frs, L)
        lati = [MT.distanza(L, centri[a], centri[b]) for a, b in ((0, 1), (1, 2), (2, 0))] if tre else []
        print("### il centro del bordo %s (R_A %.3f); i vertici (i nodi, lo spostamento multiplo di 3): %s; i lati VERI %s; la distanza minima dalle copie oltre il bordo %.3f"
              % (c0, Z["bordo"]["R_A"], centri, ["%.4f" % x for x in lati], copie_oltre(centri, L)))
        MT.vuoto_fresco(Z, t0)
        phi_F3 = st["phi_h"].copy()
        vuoto = {x: st[x].copy() for x in Z["chiavi"]}
        soli, Delte = [], []
        for fr, c in zip(frs, centri):
            for x in Z["chiavi"]:
                st[x][...] = vuoto[x]
            Delte.append(MT.incolla(Z, fr, c, True))
            soli.append((st["psi_h"].copy(), st["phi_h"].copy()))
        psi1 = soli[0][0].copy()
        phi1 = soli[0][1].copy()
        div = [x for x, a, b in (("psi", psi1, soli[0][0]), ("phi", phi1, soli[0][1])) if not np.array_equal(a, b)]
        esito("un solo francobollo: la somma e il prodotto = l'incollatura di S6 AL BIT (come c1740faa)", not div, "diverse: %s" % div, True)
        m_soli = [float(np.sum(np.abs(s_[0]) ** 2)) for s_ in soli]
        print("### le masse dei francobolli incollati DA SOLI: %s" % ["%.12e" % m for m in m_soli])
        if variante == "fase":
            sc = (max(m_soli) - min(m_soli)) / max(m_soli)
            esito("(T-fase) al tick 0 le tre masse (i francobolli da soli) uguali entro %g relativo" % TOLL_MASSA0, sc <= TOLL_MASSA0, "%.3e" % sc, True)
        psi = soli[0][0].copy()
        phi = soli[0][1].copy()
        for s_ in soli[1:]:
            psi = psi + s_[0]                                           # ### la materia per SOMMA
            phi = phi * (s_[1] / phi_F3)                                # ### il vuoto per PRODOTTO
        st["psi_h"][...] = psi
        st["phi_h"][...] = phi
        C = MT.Campi(Z, "MGU", rho_c, e)
        rho = MT.rho_di(Z)
        C.campo.A[...] = 0.0
        C.campo.E[...] = C.gauss(e * (rho - rho.mean()))
        C.campo.e = e
        C.e_prec = e
        U1.scrivi_U(Z["mot"], C.campo)                                  # ### d9318470: U dal campo (A = 0: e' I)
        assert np.array_equal(Z["mot"].geo.U, np.broadcast_to(np.eye(2, dtype=complex), Z["mot"].geo.U.shape)), "con A = 0 U NON e' I"
        g0 = C.residuo()
        print("### Delta %s; il residuo di Gauss iniziale %.3e" % (["%.6f" % d for d in Delte], g0))
        R = CT.Corsa(Z, C)
        cen = [list(map(float, c)) for c in centri]

        def misura(k):
            nonlocal cen
            rho = MT.rho_di(Z)
            cen, lab = centri_pezzi(Z, rho, cen)
            for j, n in enumerate(nomi):
                PK[n].append(float(rho[lab == j].max()))
            if k % CT.OGNI == 0:
                R.etichette(cen)
            if k % OGNI == 0:
                S["k"].append(k)
                for j, n in enumerate(nomi):
                    S["M_" + n].append(float(rho[lab == j].sum()))
                    S["raggio_" + n].append(MR.raggio(Z, rho, cen[j]))
                    S["c1_" + n].append(cen[j][0])
                    S["c2_" + n].append(cen[j][1])
                S["l_AB"].append(MT.distanza(L, cen[0], cen[1]) if tre else float("nan"))
                S["l_BC"].append(MT.distanza(L, cen[1], cen[2]) if tre else float("nan"))
                S["l_CA"].append(MT.distanza(L, cen[2], cen[0]) if tre else float("nan"))
                S["gauss"].append(C.residuo() if k % MT.OGNI_GAUSS == 0 else float("nan"))
        misura(0)
        print("### le masse dei tre pezzi al tick 0 (la partizione, descrittive): %s" % ["%.10e" % S["M_" + n][0] for n in nomi])
        R.inizio(0)
        t1 = t_tappa = time.time()
        fermo = None
        solo = variante == "solo"
        cotto162, picchi162 = None, None
        for k in range(1, N_TICK + (PIU_L162 if solo else 0) + 1):
            R.passo(k, t0 + k, 1.0, e)
            misura(k)
            if k % 250 == 0:
                print("    k %5d  lati %.4f %.4f %.4f  masse %s  raggi %s  Gauss %s  (%.0f s)" % (k, S["l_AB"][-1], S["l_BC"][-1], S["l_CA"][-1], " ".join("%.6e" % S["M_" + n][-1] for n in nomi),
                      " ".join("%.4f" % S["raggio_" + n][-1] for n in nomi), "%.2e" % S["gauss"][-1] if S["gauss"][-1] == S["gauss"][-1] else "--", time.time() - t1))
                sys.stdout.flush()
            if k % 500 == 0:
                f = os.path.join(MT.DIR_E, ("L162_MGU_%05d.npz" % k) if solo else ("triangolo_%s_%05d.npz" % (variante, k)))     # ### Luca 14:54: il prefisso L162_
                dati = {x: st[x] for x in Z["chiavi"]}
                dati.update(campo_A=C.campo.A, campo_E=C.campo.E)
                np.savez(f, meta=np.array(json.dumps({"variante": variante, "k": k, "t": t0 + k, "sha": V.shas(Z["z"]), "codice": "csv/solitone/mattone_triangolo.py"})), **dati)
            if solo and k >= N_TICK and (k - N_TICK) % PEZZO_L162 == 0:
                pk = np.array(PK["A"])                                  # ### il picco a ogni tick: PK[0] e' il tick 0
                p1, p2 = float(pk[k - 999:k - 499].mean()), float(pk[k - 499:k + 1].mean())
                cotto162 = abs(p2 - p1) / p1 < COTTO_L162
                picchi162 = (p1, p2)
                print("### LA COTTURA SU L 162 (Luca 14:54) a k %d: il picco medio %d-%d %.4e, %d-%d %.4e: %.4f (la soglia %g) -> %s; lo stato %s"
                      % (k, k - 999, k - 500, p1, k - 499, k, p2, abs(p2 - p1) / p1, COTTO_L162, "COTTO SU L 162" if cotto162 else "non ancora", f))
                sys.stdout.flush()
                if cotto162:
                    break
            adesso = time.time()
            if adesso - t_tappa >= MT.TAPPA_S:
                mem = MT.memoria_gb()
                MT.tappa(nome_reg, "k %d; %.3f s per tick; la memoria libera %.2f GB" % (k, (adesso - t1) / k, mem))
                t_tappa = adesso
            if adesso - t1 > TETTO_S:
                fermo = "il tetto di %g s a k %d" % (TETTO_S, k)
                print("### FERMO: %s" % fermo)
                break
        print("-" * 130)
        print("### %d tick in %.0f s" % (S["k"][-1], time.time() - t1))
        R.tabella(list(nomi))
        T = {x: np.array(v) for x, v in R.T.items()}
        bordoM = float(np.sum(T["Mp"] - T["Md"]))
    g = np.array(S["gauss"])
    g = g[g == g]
    esito("il residuo di Gauss sotto %g a ogni controllo (ogni %d tick)" % (MT.TOLL_GAUSS, MT.OGNI_GAUSS), len(g) > 0 and float(g.max()) < MT.TOLL_GAUSS and g0 < MT.TOLL_GAUSS,
          "il massimo %.3e (l'iniziale %.3e)" % (float(g.max()) if len(g) else float("nan"), g0), True)
    print("### la massa uscita dal bordo in tutto %.6e" % bordoM)
    if variante == "solo":
        kf = int(S["k"][-1])
        os.makedirs(DIR_LAVORO, exist_ok=True)
        with open(os.path.join(DIR_LAVORO, "cottura_L162_MGU.json"), "w", encoding="utf-8", newline=chr(10)) as fh:
            json.dump({"caso": "MGU", "scena": MT.CORSA_162, "k": kf, "t": t0 + kf, "file": os.path.join(MT.DIR_E, "L162_MGU_%05d.npz" % kf), "cotto": bool(cotto162), "picchi": picchi162,
                       "da": frs[0]["file"], "codice": "csv/solitone/mattone_triangolo.py"}, fh, indent=1)
        print("### (T-solo) LA COTTURA SU L 162: %s a k %d (%s)" % ("COTTO" if cotto162 else "### NON COTTO dopo %d tick in piu'" % PIU_L162, kf, picchi162))
    os.makedirs(MT.DIR_REF, exist_ok=True)
    np.savez_compressed(os.path.join(MT.DIR_REF, "triangolo_%s_serie.npz" % variante), bordoM=np.array(T["Mp"] - T["Md"]), **{("picco_" + n): np.array(v) for n, v in PK.items()},
                        **{x: np.array(v) for x, v in S.items()})
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite %s; %s; %.0f s in tutto" % (OK[0], OK[1], FALLITE, "FERMO " + fermo if fermo else "finita", time.time() - t00))
    return 0 if not FALLITE else 1


# =====================================================================================
#   IL REFERTO UNICO (T4)
# =====================================================================================
def pendenza(t, y):
    """### La retta ai minimi quadrati: `(pendenza, errore)`."""
    t, y = np.asarray(t, dtype=float), np.asarray(y, dtype=float)
    A = np.vstack([t - t.mean(), np.ones_like(t)]).T
    p, res, _r, _s = np.linalg.lstsq(A, y, rcond=None)
    s2 = float(res[0]) / max(1, len(t) - 2) if len(res) else 0.0
    return float(p[0]), math.sqrt(s2 / float(np.sum((t - t.mean()) ** 2)))


def fase_relativa(a, b, maxlag=150):
    """### Il ritardo della massima correlazione incrociata dei picchi *(senza la retta)* entro `+-maxlag` tick, e la correlazione a ritardo `0`."""
    t = np.arange(len(a), dtype=float)
    a = a - np.polyval(np.polyfit(t, a, 1), t)
    b = b - np.polyval(np.polyfit(t, b, 1), t)
    a, b = a / (a.std() or 1.0), b / (b.std() or 1.0)
    best = (None, -2.0)
    for lag in range(-maxlag, maxlag + 1):
        if lag >= 0:
            c = float(np.mean(a[lag:] * b[:len(b) - lag]))
        else:
            c = float(np.mean(a[:lag] * b[-lag:]))
        if c > best[1]:
            best = (lag, c)
    return best[0], best[1], float(np.mean(a * b))


def referto():
    import _presidio
    _presidio.avvia(__file__)
    a, b = FINESTRA_LETTURA
    print("=" * 130)
    print("IL TRIANGOLO, IL REFERTO UNICO (Luca 14:22, T4; 14:32: contro (T-solo)): la perdita e il raggio sui tick %d-%d contro l'isolato; la fase dei respiri; il moto del triangolo; le soglie %g e %g" % (a, b, PROTEGGE, PEGGIORA))
    print("=" * 130)
    s0 = np.load(os.path.join(MT.DIR_REF, "triangolo_solo_serie.npz"))
    k0 = np.array(s0["k"], dtype=float)
    j0 = (k0 >= a) & (k0 <= b)
    rif_M, rif_eM = pendenza(k0[j0], s0["M_A"][j0])
    rif_r, rif_er = pendenza(k0[j0], s0["raggio_A"][j0])
    bM0 = np.cumsum(s0["bordoM"])
    kb0 = np.arange(1, len(bM0) + 1, dtype=float)
    jb0 = (kb0 >= a) & (kb0 <= b)
    rif_b, rif_eb = pendenza(kb0[jb0], -bM0[jb0])
    print("### L'ISOLATO, (T-solo) (Luca 14:32: un MGU_10000 al vertice A, la stessa scena, gli stessi tick): dM/dt del pezzo %.4e +- %.1e; d raggio/dt %.4e +- %.1e; la massa uscita dal bordo per tick %.4e +- %.1e"
          % (rif_M, rif_eM, rif_r, rif_er, -rif_b, rif_eb))
    for variante in ("fase", "sfasati"):
        f = os.path.join(MT.DIR_REF, "triangolo_%s_serie.npz" % variante)
        if not os.path.exists(f):
            print("### (T-%s): la serie non c'e'" % variante)
            continue
        s = np.load(f)
        k = np.array(s["k"], dtype=float)
        jj = (k >= a) & (k <= b)
        print("-" * 130)
        print("### (T-%s)" % variante)
        tot = 0.0
        for n in NOMI:
            mM, eM = pendenza(k[jj], s["M_" + n][jj])
            mr, er = pendenza(k[jj], s["raggio_" + n][jj])
            q = mM / rif_M
            eq = abs(q) * math.sqrt((eM / mM) ** 2 + (rif_eM / rif_M) ** 2)
            lett = "IL TRIANGOLO PROTEGGE" if q < PROTEGGE else ("IL TRIANGOLO FA PERDERE DI PIU'" if q > PEGGIORA else "NESSUN EFFETTO CHIARO")
            qr = mr / rif_r
            eqr = abs(qr) * math.sqrt((er / mr) ** 2 + (rif_er / rif_r) ** 2) if mr else float("nan")
            print("    %s: dM/dt %.4e +- %.1e (il pezzo); contro (T-solo) %.3f +- %.3f -> %s; d raggio/dt %.4e +- %.1e, contro (T-solo) %.3f +- %.3f" % (n, mM, eM, q, eq, lett, mr, er, qr, eqr))
            tot += mM
        bM = np.cumsum(s["bordoM"])
        kb = np.arange(1, len(bM) + 1, dtype=float)
        jb = (kb >= a) & (kb <= b)
        mb, eb = pendenza(kb[jb], -bM[jb])
        print("    la somma delle tre perdite dei pezzi %.4e; la massa uscita dal bordo per tick %.4e +- %.1e (per solitone %.4e, contro (T-solo) %.3f)" % (tot, -mb, eb, -mb / 3.0, (mb / 3.0) / rif_b))
        print("    LA FASE DEI RESPIRI (il ritardo della massima correlazione dei picchi, in tick; la correlazione a ritardo 0):")
        for (p, q_) in (("A", "B"), ("B", "C"), ("C", "A")):
            x, y = np.array(s["picco_" + p]), np.array(s["picco_" + q_])
            i0 = fase_relativa(x[:500], y[:500])
            i1 = fase_relativa(x[-500:], y[-500:])
            print("        %s-%s: all'inizio (0-500) il ritardo %+d (corr %.3f; a 0 %.3f); alla fine (ultimi 500) %+d (corr %.3f; a 0 %.3f)" % (p, q_, i0[0], i0[1], i0[2], i1[0], i1[1], i1[2]))
        lm = (np.array(s["l_AB"]) + np.array(s["l_BC"]) + np.array(s["l_CA"])) / 3.0
        from solitone import carta_coppia as CC
        jj2 = k >= 250
        acc, ea = CC.curvatura(k[jj2], lm[jj2])
        print("    IL MOTO DEL TRIANGOLO: il lato medio da %.4f a %.4f (min %.4f, max %.4f); la parabola sui tick 250-%d: d'' %+.4e +- %.1e (%.1f errori); i lati alla fine %.4f %.4f %.4f"
              % (lm[0], lm[-1], lm.min(), lm.max(), int(k[-1]), acc, ea, abs(acc) / ea if ea else float("inf"), s["l_AB"][-1], s["l_BC"][-1], s["l_CA"][-1]))
    print("=" * 130)
    return 0


def main(argv):
    if argv and argv[0] == "referto":
        return referto()
    ap = argparse.ArgumentParser()
    ap.add_argument("azione", choices=("corsa",))
    ap.add_argument("--variante", required=True, choices=sorted(VARIANTI))
    ap.add_argument("--registro")
    x = ap.parse_args(argv)
    return corsa(x.variante, x.registro)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
