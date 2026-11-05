# -*- coding: utf-8 -*-
r"""**LE TRE CARTE STATICHE: IL VUOTO, LA COPPIA, LA DIMENSIONE** *(Luca `2026-11-05` `15:28`, l'ordine delle `15:42`; il task history `doc/TASK_HISTORY/2026-11-05_carte_statiche.md`)* -- **nessuna corsa**
    python csv/solitone/carta_statiche.py --vuoto > doc/referti_l2/statica_vuoto.txt
    python csv/solitone/carta_statiche.py --coppia > doc/referti_l2/statica_coppia.txt
    python csv/solitone/carta_statiche.py --dimensione > doc/referti_l2/statica_dimensione.txt
    python csv/solitone/carta_statiche.py --coppia-matura > doc/referti_l2/statica_coppia_matura.txt   # (Luca 2026-11-05 21:01) gli stati maturi di TBS
### **La scena con `N` e `L` espliciti** *(`scena_con`: `V.N`, `V.L` in memoria e rimessi; poi `V.scena` e `V.partenza` come nella corsa)*; `CS0` *(mio)*: a `N 1e6`, `L 81` la partenza = quella senza
`scena_con`, al bit. ### **`--vuoto`:** la risposta REALE-lineare di un tick vivo intero *(`AC.tick` dopo la rampa)* a un disturbo del vuoto `F3` con `psi = 0`, nel riferimento che gira *(`e^{-i omega}`)*;
`12` gradi di liberta' reali per cella *(le `6` estremita' di un nodo, etichettate per direzione e lato)*; `T(k)` per `k` qualsiasi; i DEVE `VD-L` *(la linearita': `AMP` e `2 AMP` entro `TOLL_L`)*, `VD-T`, `VD-G`,
`VD-0` *(il Goldstone: la rotazione globale `i F3` a `Gamma` autovettore con autovalore `1`)*; il gap, la curvatura, il `lambda` statico proposto `sqrt(a / Delta)`. ### **`--coppia`:** `L_COPPIA`, la partenza `p1`, la copia
`p2` traslata di `d` lungo `A1` *(per `+1` o `-1`)*; `E_int(d) = E[p1 + p2] - E[p1] - E[p2] + E[0]` *(il vuoto una volta)*, la forma del mandato accanto; `F_s = -dE_int/dd`; i DEVE `EI-T`, `EI-0`, `EI-F`.
### **`--dimensione`:** a ogni `N` di `NN`, la scena *(`w0` del continuo)*, la partenza, `w`, lo spessore del bordo e l'esagonalita' a `t 0` *(le soglie scalate per `N / 1e6`)*; il DEVE `DM-F`.
"""
import contextlib
import hashlib
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

DIR_REF = os.path.join(solitone.RADICE, "doc", "referti_l2")   # ### --coppia-matura: legge statica_coppia.txt per la colonna di t 0

NN = (2.5e5, 5e5, 1e6, 2e6, 4e6)   # ### Luca 15:28: la dimensione a N da 2.5e5 a 4e6
L_COPPIA = 162                 # ### il task history 1.0: L multiplo di 3 (159 o 162: la proposta 162, la scelta di Luca per le corse)
DD = tuple(range(24, 81, 2))   # ### Luca 15:28: da 24 a 80 ogni 2 nodi, centri sui nodi
AMP = 1e-7                     # ### --vuoto: l'ampiezza del disturbo (protocollo; 2 AMP per VD-L)
TOLL_L = 1e-6                  # ### il task history 1.1: VD-L
TOLL_A = 1e-12                 # ### VD-G (due conti sulle STESSE risposte); per VD-T era il mio errore (799ab1cc: sotto il pavimento eps / AMP)
AMP_T = (1e-7, 1e-6, 1e-5)     # ### Luca 2026-11-05 20:20: VD-T a tre ampiezze
PEND_T, TOLL_PEND_T = -1.0, 0.3   # ### Luca 20:20: lo scarto di VD-T scende come 1 / ampiezza (la pendenza in log attesa -1 entro 0.3)
PAV_T = 10.0 * 1e-16           # ### Luca 20:20: a ogni ampiezza lo scarto sotto 10 x (1e-16 / ampiezza)
TOLL_G = 1e-6                  # ### VD-0: il Goldstone (la risposta lineare con AMP: l'errore O(AMP))
TOLL_E = 1e-12                 # ### EI-T
GAP_ZERO = 1e-6                # ### --vuoto: le fasi per tick sotto questo sono zero (il Goldstone e il suo compagno), escluse dal gap
KAPPA = (0.01, 0.02, 0.04, 0.06, 0.08, 0.1)   # ### --vuoto: |k| lungo A1 per la curvatura del ramo del gap
SOGLIE = (1.0, 10.0, 100.0, 300.0)            # ### le soglie della forma a N 1e6 (scalate per N / 1e6)

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-120s %s   %s" % (che[:120], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


@contextlib.contextmanager
def scena_con(N, L):
    """### **`V.N`, `V.L` in memoria, rimessi all'uscita:** `V.scena` e `V.partenza` li leggono *(la norma della partenza, il `fattore`, il controllo su `L`)*."""
    import _vuoto_vivo_B as V
    vero = (V.N, V.L)
    V.N, V.L = N, L
    try:
        yield
    finally:
        V.N, V.L = vero


def costruisci(N, L):
    """### **La scena, la partenza di `TF3`, il vuoto `F3`:** `(rec, z, p0, phi_v, info)`; la scena resta col vuoto `F3` e `psi = 0` nello stato."""
    import _vuoto_vivo_B as V
    from solitone import corsa_accensione as CA
    sol, vuoto, s = V.CORSE[CA.NOME]
    with scena_con(N, L):
        cm = V.scena(s, vuoto, V.EPS)
        rec, z, phi0, pK = cm.__enter__()
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        p0, info = V.partenza(sol, z, phi0, pK, s)
        for k, v in salvato.items():
            z["st"][k][...] = v
    phi_v = CA.vuoto_della_corsa(z, "TF3")
    return rec, z, p0, phi_v, info, cm


def energia(z, psi, phi, e_K):
    import _libro_dei_conti as LC
    import _vuoto_vivo_B as V
    z["st"]["psi_h"][...] = psi
    z["st"]["phi_h"][...] = phi
    return math.fsum(LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO, z["par"])["tot"].tolist())


def cs0():
    import _stato_fermo as SFM
    import _vuoto_vivo_B as V
    from solitone import corsa_accensione as CA
    sol, vuoto, s = V.CORSE[CA.NOME]
    with V.scena(s, vuoto, V.EPS) as (_rec, z, phi0, pK):
        p_rif, _i = V.partenza(sol, z, phi0, pK, s)
    _rec, _z, p0, _phi, _info, cm = costruisci(V.N, V.L)
    cm.__exit__(None, None, None)
    esito("DEVE PASSARE: CS0 a N %g, L %d la partenza costruita con scena_con = quella di V.scena / V.partenza, al bit" % (V.N, V.L), SFM.sha(p0) == SFM.sha(p_rif), SFM.sha(p0))


def vuoto():
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_dal_fondo as SD
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import bordo as BO
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    _sol, _v, s = V.CORSE[CA.NOME]
    K = int(round(CA.CORSE["TF3"][0] / s))
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        omega = float(d["omega"])
    _rec, z, _p0, F3, _info, cm = costruisci(V.N, V.L)
    inc, L = z["inc"], z["L"]
    n = inc.n
    m1, m2 = np.arange(n) // L, np.arange(n) % L
    lab = np.empty(2 * inc.m, dtype=int)
    for a in range(inc.m):
        i, j = int(inc.nodo[2 * a]), int(inc.nodo[2 * a + 1])
        dd = ((int(m1[j] - m1[i]) + L // 2) % L - L // 2, (int(m2[j] - m2[i]) + L // 2) % L - L // 2)
        pos = dd if (dd[0] > 0 or (dd[0] == 0 and dd[1] > 0)) else (-dd[0], -dd[1])
        k = SD.DIREZIONI.index(pos)
        lab[2 * a], lab[2 * a + 1] = (2 * k, 2 * k + 1) if pos == dd else (2 * k + 1, 2 * k)
    dove = np.full((n, 6), -1)
    dove[inc.nodo, lab] = np.arange(2 * inc.m)
    assert np.all(dove >= 0) and len(np.unique(dove)) == 2 * inc.m, "ogni nodo deve avere le sue 6 estremita', una per etichetta"
    salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
    rot = np.exp(-1j * omega)

    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab_c = d["c"].copy()
    cK, cK1 = BO.c_di(K, tab_c, K, omega), BO.c_di(K + 1, tab_c, K, omega)
    # ### Luca 20:20, il riferimento: (la base, il fattore del disturbo prima del tick, il fattore della risposta dopo il tick)
    # ### "oggi": la base F3, il disturbo com'e', la risposta per e^{-i omega} (il riferimento che gira, ATTORNO A F3: la carta di 799ab1cc)
    # ### "corotante": eta = c(t)* phi; la base c(K) F3, il disturbo per c(K), la risposta per c(K+1)* (Luca: moltiplicare per c(t)* prima di linearizzare)
    # ### "fisso": la base c(K) F3, il disturbo com'e', la risposta senza fattore (il riferimento di laboratorio)
    RIF = {"oggi": (1.0 + 0j, 1.0 + 0j, rot), "corotante": (cK, cK, np.conj(cK1)), "fisso": (cK, 1.0 + 0j, 1.0 + 0j)}
    fuori = []

    def risposta(nodo, amp, rif="oggi"):
        """`(12, n, 12)`: per ogni grado di liberta' reale `c` del nodo, la risposta reale per nodo (Re, Im delle 6 estremita')."""
        f_base, f_dist, f_dopo = RIF[rif]
        R = np.empty((12, n, 12))
        del fuori[:]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            for k_, v in salvato.items():
                z["st"][k_][...] = v
            z["st"]["psi_h"][...] = 0.0
            z["st"]["phi_h"][...] = f_base * F3
            AC.tick(z, K + 1, K)
            base = z["st"]["phi_h"].copy()
            for c in range(12):
                for k_, v in salvato.items():
                    z["st"][k_][...] = v
                z["st"]["psi_h"][...] = 0.0
                ph = f_base * F3
                e_ = dove[nodo, c // 2]
                ph[e_] += f_dist * amp * (1.0 if c % 2 == 0 else 1j)
                z["st"]["phi_h"][...] = ph
                AC.tick(z, K + 1, K)
                dl = (z["st"]["phi_h"] - base) * f_dopo / amp
                arco = np.zeros(dl.shape[0], dtype=bool)
                arco[[e_, e_ ^ 1]] = True          # ### l'estremita' disturbata e l'altra dello stesso arco (2a, 2a + 1)
                fuori.append((float(np.max(np.abs(dl[~arco]))), float(np.max(np.abs(dl[arco])))))
                per = dl[dove]                       # (n, 6) complesso
                R[c] = np.stack([per.real, per.imag], axis=2).reshape(n, 12)
        for k_, v in salvato.items():
            z["st"][k_][...] = v
        return R
    R1 = risposta(0, AMP)
    R2 = risposta(0, 2 * AMP)
    eL = float(np.max(np.abs(R2 - R1)) / np.max(np.abs(R1)))
    esito("DEVE PASSARE: VD-L la risposta a AMP %g e a 2 AMP uguali entro %g relativo (il vuoto lineare a quell'ampiezza)" % (AMP, TOLL_L), eL <= TOLL_L, "%.3e" % eL)
    j0 = 5 * L + 7
    da = ((m1 - j0 // L) % L) * L + (m2 - j0 % L) % L
    eTs = []
    for amp_t in AMP_T:                    # ### Luca 20:20: VD-T a tre ampiezze, la pendenza dello scarto in log e il pavimento a ogni ampiezza
        R0t = R1 if amp_t == AMP else risposta(0, amp_t)
        Rj = risposta(j0, amp_t)
        eTs.append(float(np.max(np.abs(Rj - R0t[:, da, :])) / np.max(np.abs(R0t))))
    pend_t = float(np.polyfit(np.log(np.array(AMP_T)), np.log(np.array(eTs)), 1)[0])
    print("  VD-T: lo scarto per ampiezza %s; il pavimento 10 x 1e-16 / ampiezza %s; la pendenza di ln scarto contro ln ampiezza %+.4f"
          % (", ".join("%g: %.3e" % (a, e) for a, e in zip(AMP_T, eTs)), ", ".join("%.1e" % (PAV_T / a) for a in AMP_T), pend_t))
    sotto = all(e <= PAV_T / a for a, e in zip(AMP_T, eTs))
    esito("DEVE PASSARE: VD-T la risposta da un altro nodo (%d), riportata indietro: lo scarto scende come 1 / ampiezza (pendenza %g entro %g) e sta sotto 10 x 1e-16 / ampiezza"
          % (j0, PEND_T, TOLL_PEND_T), abs(pend_t - PEND_T) <= TOLL_PEND_T and sotto, "pendenza %+.4f; sotto il pavimento a ogni ampiezza: %s" % (pend_t, sotto))
    if abs(pend_t - PEND_T) > TOLL_PEND_T:
        print("  ### LO SCARTO NON SCENDE COME 1 / AMPIEZZA: non e' il pavimento (Luca 20:20: FERMO)")
    A1, A2 = TO.vettori()
    nz = np.flatnonzero(np.any(np.abs(R1) > 0.0, axis=(0, 2)))
    d1 = (nz // L + L // 2) % L - L // 2
    d2 = (nz % L + L // 2) % L - L // 2
    rs = d1[:, None] * A1 + d2[:, None] * A2
    Rs = R1[:, nz, :]
    print("  il supporto della risposta di un tick: %d nodi; |d1|, |d2| fino a %d, %d" % (len(nz), int(np.abs(d1).max()), int(np.abs(d2).max())))

    def T(k):
        return np.einsum("cra,r->ac", Rs, np.exp(-1j * (rs @ k)))
    Bm = 2.0 * np.pi * np.linalg.inv(np.array([A1, A2])).T
    eG = 0.0
    for i1, i2 in ((0, 0), (3, 7), (40, 11), (80, 80), (17, 64)):
        kq = (i1 * Bm[0] + i2 * Bm[1]) / L
        Tg = np.empty((12, 12), dtype=complex)
        for c in range(12):
            Tg[:, c] = np.fft.fft2(R1[c].reshape(L, L, 12), axes=(0, 1))[i1, i2]
        eG = max(eG, float(np.max(np.abs(T(kq) - Tg))))
    esito("DEVE PASSARE: VD-G T(k) per k qualsiasi = fft2 della risposta su 5 k della griglia, entro %g" % TOLL_A, eG <= TOLL_A, "%.3e" % eG)
    gv = np.zeros(12)
    for l in range(6):
        val = 1j * F3[dove[0, l]]
        gv[2 * l], gv[2 * l + 1] = val.real, val.imag
    T0 = T(np.zeros(2))
    eg = float(np.linalg.norm(T0 @ gv - gv) / np.linalg.norm(gv))
    esito("DEVE PASSARE: VD-0 il Goldstone: la rotazione globale i F3 a Gamma e' un autovettore con autovalore 1, entro %g" % TOLL_G, eg <= TOLL_G, "%.3e" % eg)
    ev = np.linalg.eigvals(T0)
    o = np.argsort(np.angle(ev))
    print("  a Gamma i 12 autovalori (nel riferimento che gira): la fase per tick e il modulo:")
    print("    " + "; ".join("%+.6e |%.9f|" % (np.angle(ev[i]), abs(ev[i])) for i in o))
    nonzero = [i for i in range(12) if abs(np.angle(ev[i])) > GAP_ZERO]
    if not nonzero:
        print("  ### nessuna fase sopra GAP_ZERO a Gamma: il gap non si legge")
    else:
        ig = min(nonzero, key=lambda i: abs(np.angle(ev[i])))
        Delta = abs(np.angle(ev[ig])) / s
        lam0 = ev[ig]
        rami = []
        prev = lam0
        for kap in KAPPA:
            e2 = np.linalg.eigvals(T(np.array([kap, 0.0])))
            prev = e2[int(np.argmin(np.abs(e2 - prev)))]
            rami.append(abs(np.angle(prev)) / s)
        kk = np.array(KAPPA)
        a = float(np.polyfit(kk ** 2, np.array(rami) - Delta, 1)[0])
        print("  ### il gap a Gamma (il ramo con la fase piu' piccola sopra %g per tick): Delta %.6e per unita' di tempo (|lambda| %.9f)" % (GAP_ZERO, Delta, abs(lam0)))
        print("    il ramo lungo A1: |k| %s -> omega %s" % (" ".join("%.2f" % x for x in KAPPA), " ".join("%.6e" % x for x in rami)))
        print("  ### la curvatura a = d omega / d k^2 = %+.6e (nodi^2 per unita' di tempo); la PROPOSTA di lettura: lambda = sqrt(|a| / Delta) = %.4f nodi" % (a, math.sqrt(abs(a) / Delta) if Delta > 0 else float("nan")))
        print("  ### non so a quale frequenza il solitone eccita il vuoto (il task history 1.1): il lambda statico puo' non essere quello giusto")
    mods = [abs(x) for x in ev]
    print("  i moduli a Gamma da %.9f a %.9f (1: il vuoto neutro)" % (min(mods), max(mods)))
    # ### IL RIFERIMENTO (Luca 2026-11-05 20:20, la domanda del guardiano): la stessa misura in tre riferimenti, a confronto; il gap e lambda si leggono solo dopo
    print("-" * 130)
    print("### IL RIFERIMENTO (Luca 20:20): c(K) %+.15f %+.15fi, c(K+1) %+.15f %+.15fi (fase_F3.npz); la risposta ad AMP %g dal nodo 0 in tre riferimenti" % (cK.real, cK.imag, cK1.real, cK1.imag, AMP))
    print("  oggi: la base F3, la risposta per e^{-i omega}; corotante: eta = c(t)* phi (la base c(K) F3, il disturbo per c(K), la risposta per c(K+1)*); fisso: la base c(K) F3, nessun fattore")
    Rf, fu = {}, {}
    for rif in ("oggi", "corotante", "fisso"):
        Rf[rif] = risposta(0, AMP, rif)
        fu[rif] = list(fuori)
    e_r0 = float(np.max(np.abs(Rf["oggi"] - R1)))
    esito("DEVE PASSARE: VD-R0 la risposta di oggi rifatta col riferimento esplicito = quella di sopra, al bit", e_r0 == 0.0, "%.3e" % e_r0)
    e_rf = float(np.max(np.abs(Rf["fisso"] - R1)) / np.max(np.abs(R1)))
    esito("DEVE FALLIRE: VD-R-F la risposta nel riferimento fisso = quella di oggi entro %g relativo (il confronto vede il riferimento)" % TOLL_L, not e_rf <= TOLL_L, "%.3e" % e_rf)   # ### un DEVE FALLIRE: la condizione NEGATA (60de22ec: il mio errore, il verdetto rovesciato)
    print("  la risposta corotante contro quella di oggi: lo scarto relativo %.3e (il pavimento ad AMP %g: %.1e)"
          % (float(np.max(np.abs(Rf["corotante"] - R1)) / np.max(np.abs(R1))), AMP, PAV_T / AMP))
    for rif in ("oggi", "corotante", "fisso"):
        Rr = Rf[rif]
        nz_r = np.flatnonzero(np.any(np.abs(Rr) > 0.0, axis=(0, 2)))
        rs_r = ((nz_r // L + L // 2) % L - L // 2)[:, None] * A1 + ((nz_r % L + L // 2) % L - L // 2)[:, None] * A2
        Rs_r = Rr[:, nz_r, :]

        def Tr(k, Rs_r=Rs_r, rs_r=rs_r):
            return np.einsum("cra,r->ac", Rs_r, np.exp(-1j * (rs_r @ k)))
        evr = np.linalg.eigvals(Tr(np.zeros(2)))
        orr = np.argsort(np.angle(evr))
        print("  %-9s a Gamma le 12 fasi per tick: %s; i moduli da %.9f a %.9f" % (rif, " ".join("%+.6e" % np.angle(evr[i]) for i in orr), min(abs(evr)), max(abs(evr))))
        nzr = [i for i in range(12) if abs(np.angle(evr[i])) > GAP_ZERO]
        if nzr:
            ig = min(nzr, key=lambda i: abs(np.angle(evr[i])))
            Dr = abs(np.angle(evr[ig])) / s
            prev = evr[ig]
            rr = []
            for kap in KAPPA:
                e2 = np.linalg.eigvals(Tr(np.array([kap, 0.0])))
                prev = e2[int(np.argmin(np.abs(e2 - prev)))]
                rr.append(abs(np.angle(prev)) / s)
            ar = float(np.polyfit(np.array(KAPPA) ** 2, np.array(rr) - Dr, 1)[0])
            print("  %-9s il ramo con la fase piu' piccola sopra %g: Delta %.6e per unita' di tempo; lungo A1 %s; la curvatura %+.6e; sqrt(|a| / Delta) %.4f nodi"
                  % (rif, GAP_ZERO, Dr, " ".join("%.6e" % x for x in rr), ar, math.sqrt(abs(ar) / Dr)))
        else:
            print("  %-9s nessuna fase sopra %g a Gamma: il gap non si legge" % (rif, GAP_ZERO))
        print("  %-9s la risposta FUORI dalle due estremita' dell'arco disturbato: il massimo %.3e, contro dentro %.3e (il rapporto peggiore sui 12 gradi %.3e)"
              % (rif, max(f for f, _ in fu[rif]), max(d_ for _, d_ in fu[rif]), max(f / d_ for f, d_ in fu[rif])))
    print("  ### la lettura (Luca 20:20): se il gap a pi sparisce o si sposta nel corotante, era la rotazione vista da fuori; il gap e lambda si leggono solo dopo")
    cm.__exit__(None, None, None)


def coppia():
    import _vuoto_vivo_B as V
    from solitone import protetto as P
    _rec, z, p1, F3, _info, cm = costruisci(V.N, L_COPPIA)
    L = z["L"]
    n = z["inc"].n
    e_K = P.e_K(z)
    sh = p1.shape
    q1 = p1.reshape(L, L, -1)
    zero = np.zeros_like(p1)
    E0 = energia(z, zero, F3, e_K)
    E1 = energia(z, p1, F3, e_K)
    print("  la scena: L %d (%d nodi); E[0] (il vuoto) %.12e; E[p1] %.12e; M di p1 %.6f" % (L, n, E0, E1, float(np.sum(np.abs(p1) ** 2))))
    e00 = abs(energia(z, p1 + 0.0 * np.roll(q1, DD[0], axis=0).reshape(sh), F3, e_K) - E1)
    esito("DEVE PASSARE: EI-0 E[p1 + 0 p2] = E[p1] al bit", e00 == 0.0, "%.3e" % e00)
    print("  %4s %20s %20s %16s %16s %16s" % ("d", "E_int fase 0", "E_int fase pi", "la forma del mandato (0)", "E[p2]/E[p1] - 1", "F_s fase 0"))
    Ei = {0: [], 1: []}
    mand, rel2 = [], []
    for d in DD:
        p2 = np.roll(q1, d, axis=0).reshape(sh)
        E2 = energia(z, p2, F3, e_K)
        rel2.append(E2 / E1 - 1.0)
        for f, segno in ((0, 1.0), (1, -1.0)):
            Ep = energia(z, p1 + segno * p2, F3, e_K)
            Ei[f].append(Ep - E1 - E2 + E0)
            if f == 0:
                mand.append(Ep - 2.0 * E1)
    Fs = {f: [-(Ei[f][i + 1] - Ei[f][i - 1]) / (DD[i + 1] - DD[i - 1]) if 0 < i < len(DD) - 1 else float("nan") for i in range(len(DD))] for f in (0, 1)}
    for i, d in enumerate(DD):
        print("  %4d %+20.10e %+20.10e %+16.6e %+16.3e %+16.6e" % (d, Ei[0][i], Ei[1][i], mand[i], rel2[i], Fs[0][i]))
    eT = max(abs(x) for x in rel2)
    esito("DEVE PASSARE: EI-T E[p2] = E[p1] (la traslazione e' una simmetria) entro %g relativo, per ogni d" % TOLL_E, eT <= TOLL_E, "il peggiore %.3e" % eT)
    diff = max(abs(mand[i] - Ei[0][i]) for i in range(len(DD)))
    esito("DEVE FALLIRE: EI-F la forma del mandato E[p1 + p2] - 2 E[p1] = E_int (il vuoto contato due volte)", not diff <= 1e-9 * abs(E0), "la differenza %.6e (E[0] %.6e)" % (diff, E0))
    print("  la forza statica in fase pi: %s" % " ".join("%d %+.3e" % (DD[i], Fs[1][i]) for i in range(1, len(DD) - 1)))
    cm.__exit__(None, None, None)


STATI_MATURI = (0, 100000, 200000)   # ### Luca 2026-11-05 21:01: gli stati di TBS a t 15000 e 30000 (il tick nel nome), piu' t 0 per il confronto
TOLL_IMM = 1e-9                # ### Luca 21:01: E[1] su L 162 = E su L 81 + il vuoto aggiunto, entro 1e-9 relativo
SOGLIA_INT = 1e-6              # ### Luca 21:01: la distanza a cui |E_int| scende sotto 1e-6 E[1]
TOLL_CM = 1e-12                # ### CM-E (mio): l'energia dello stato caricato = quella del campione della corsa


def _ordine_archi(z):
    """### **L'array delle estremita' e' per arco, gli archi per nodo proprietario** *(3 archi, 6 estremita' per nodo, le stesse direzioni ovunque)*: ASSERITO *(il task history 10.1)*."""
    inc, L = z["inc"], z["L"]
    n = inc.n
    nodo = np.asarray(inc.nodo)
    assert np.array_equal(nodo[0::2], np.repeat(np.arange(n), 3)), "l'estremita' 2a NON e' del nodo proprietario dell'arco a"
    m1, m2 = np.arange(n) // L, np.arange(n) % L
    dd = np.stack([((m1[nodo[1::2]] - m1[nodo[0::2]]) + L // 2) % L - L // 2, ((m2[nodo[1::2]] - m2[nodo[0::2]]) + L // 2) % L - L // 2], 1)
    assert np.array_equal(dd.reshape(n, 3, 2), np.broadcast_to(dd[:3], (n, 3, 2))), "le direzioni degli archi NON sono le stesse per ogni nodo"
    return [tuple(int(v) for v in x) for x in dd[:3]]


def coppia_matura():
    """### **Luca 2026-11-05 21:01:** la coppia con gli stati maturi di `TBS` *(il task history 10)*."""
    import _vuoto_vivo_B as V
    from solitone import bordo as BO
    from solitone import corsa_accensione as CA
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab_c, omega = d["c"].copy(), float(d["omega"])
    _sol, _v, s = V.CORSE[CA.NOME]
    K = int(round(CA.CORSE["TF3"][0] / s))
    righe = [V.LP.leggi(os.path.join(CA.dir_json("TBS"), f)) for f in sorted(os.listdir(CA.dir_json("TBS"))) if f.startswith("TBS_") and f.endswith(".jsonl")]
    e_K = righe[0]["e_K"]
    reg = {x["t"]: x for r in righe for x in (r.get("stati") or [])}
    camp = {c["t"]: c for r in righe for c in r["campioni"]}
    _r8, z8, _p8, F3_8, _i8, cm8 = costruisci(V.N, 81)
    dir8 = _ordine_archi(z8)
    print("  e_K della corsa %.16f; il centro di partenza di TBS (40.5, 40.5); le direzioni degli archi per nodo %s" % (e_K, dir8))
    stati = {}
    eS, eE = [], []
    for t in STATI_MATURI:
        f = reg[t]["file"]
        with np.load(f) as d:
            st = {k: d[k].copy() for k in d.files if k != "t"}
        sha_f = hashlib.sha1(open(f, "rb").read()).hexdigest()
        ok_s = all(SFM_sha(st[k]) == reg[t]["sha"][k] for k in reg[t]["sha"])
        eS.append(ok_s)
        E8 = energia(z8, st["psi_h"], st["phi_h"], e_K)
        Ec = camp[t]["E"]["totale"]["tot"]
        eE.append(abs(E8 / Ec - 1.0))
        c_t = BO.c_di(t, tab_c, K, omega)
        E8_0 = energia(z8, np.zeros_like(st["psi_h"]), c_t * F3_8, e_K)
        stati[t] = {"st": st, "E8": E8, "E8_0": E8_0, "c": c_t, "sha": sha_f}
        print("  lo stato a t %.0f (tick %d): %s sha1 %s; E su L 81 %.12e (il campione %.12e); c(t) %+.12f %+.12fi; E[0] su L 81 %.12e"
              % (t * s, t, f, sha_f, E8, Ec, c_t.real, c_t.imag, E8_0))
    cm8.__exit__(None, None, None)
    esito("DEVE PASSARE: CM-S ogni stato caricato da' gli sha per chiave registrati nella corsa", all(eS), "%s" % eS)
    esito("DEVE PASSARE: CM-E l'energia dello stato su L 81 = quella del campione della corsa allo stesso tick, entro %g relativo" % TOLL_CM, max(eE) <= TOLL_CM, "il peggiore %.3e" % max(eE))
    _r, z, _p1, F3, _info, cm = costruisci(V.N, L_COPPIA)
    L = z["L"]
    assert _ordine_archi(z) == dir8, "le direzioni degli archi di L 162 NON sono quelle di L 81"
    ePh = float(np.max(np.abs(F3.reshape(L, L, 6)[:81, :81] - F3_8.reshape(81, 81, 6))))
    esito("DEVE PASSARE: CM-V F3 su L 162 nel rombo = F3 su L 81, al bit", ePh == 0.0, "%.3e" % ePh)
    cop0 = {}
    if os.path.exists(os.path.join(DIR_REF, "statica_coppia.txt")):
        for l in open(os.path.join(DIR_REF, "statica_coppia.txt"), encoding="utf-8"):
            p = l.split()
            if len(p) >= 3 and p[0].isdigit() and int(p[0]) in DD:
                cop0[int(p[0])] = (float(p[1]), float(p[2]))
    dist = {}
    for t in STATI_MATURI:
        x = stati[t]
        ph0 = x["c"] * F3
        ps1 = np.zeros((L, L, 6) + x["st"]["psi_h"].shape[1:], dtype=complex)
        ps1[:81, :81] = x["st"]["psi_h"].reshape((81, 81, 6) + x["st"]["psi_h"].shape[1:])
        ps1 = ps1.reshape((-1,) + x["st"]["psi_h"].shape[1:])
        ph1 = ph0.reshape(L, L, 6).copy()
        ph1[:81, :81] = x["st"]["phi_h"].reshape(81, 81, 6)
        ph1 = ph1.reshape(-1)
        D1 = ph1 - ph0
        zero = np.zeros_like(ps1)
        E0 = energia(z, zero, ph0, e_K)
        E1 = energia(z, ps1, ph1, e_K)
        atteso = x["E8"] + (E0 - x["E8_0"])
        e_imm = abs(E1 / atteso - 1.0)
        esito("DEVE PASSARE: CM-1 (Luca 21:01) t %.0f: E[1] su L 162 = E su L 81 + il vuoto aggiunto (E[0] su 162 - E[0] su 81), entro %g relativo" % (t * s, TOLL_IMM), e_imm <= TOLL_IMM,
              "%.3e (E[1] %.12e, atteso %.12e)" % (e_imm, E1, atteso))
        E1m = energia(z, ps1, ph0, e_K)
        E0v1 = energia(z, zero, ph1, e_K)
        print("  t %.0f su L %d: E[0] %.12e; E[1] %.12e; M %.6f; il disturbo del vuoto |D1| %.6e" % (t * s, L, E0, E1, float(np.sum(np.abs(ps1) ** 2)), float(np.linalg.norm(D1))))
        print("  %4s %18s %18s %16s %16s %16s %16s %16s %16s" % ("d", "E_int fase 0", "E_int fase pi", "materia 0", "vuoto", "resto 0", "materia pi", "resto pi", "t 0 TF3 (fase 0)"))
        rel2 = []
        Ei = {0: [], 1: []}
        q1 = ps1.reshape((L, L, -1))
        d1r = D1.reshape(L, L, -1)
        for dd_ in DD:
            ps2 = np.roll(q1, dd_, axis=0).reshape(ps1.shape)
            D2 = np.roll(d1r, dd_, axis=0).reshape(D1.shape)
            ph2 = ph0 + D2
            E2 = energia(z, ps2, ph2, e_K)
            rel2.append(abs(E2 / E1 - 1.0))
            E2m = energia(z, ps2, ph0, e_K)
            Ev = energia(z, zero, ph0 + D1 + D2, e_K) - E0v1 - energia(z, zero, ph2, e_K) + E0
            riga = [dd_]
            for f_, sg in ((0, 1.0), (1, -1.0)):
                Ec_ = energia(z, ps1 + sg * ps2, ph0 + D1 + D2, e_K)
                Ein = Ec_ - E1 - E2 + E0
                Em = energia(z, ps1 + sg * ps2, ph0, e_K) - E1m - E2m + E0
                Ei[f_].append(Ein)
                riga += [Ein, Em, Ein - Em - Ev]
            print("  %4d %+18.10e %+18.10e %+16.6e %+16.6e %+16.6e %+16.6e %+16.6e %16s"
                  % (dd_, riga[1], riga[4], riga[2], Ev, riga[3], riga[5], riga[6], ("%+.6e" % cop0[dd_][0]) if dd_ in cop0 else "-"))
        eT = max(rel2)
        esito("DEVE PASSARE: EI-T t %.0f E[2] = E[1] (la traslazione), entro %g relativo, per ogni d" % (t * s, TOLL_E), eT <= TOLL_E, "il peggiore %.3e" % eT)
        for f_ in (0, 1):
            sotto = [dd_ for i, dd_ in enumerate(DD) if all(abs(v) < SOGLIA_INT * abs(E1) for v in Ei[f_][i:])]
            dist[(t, f_)] = sotto[0] if sotto else None
        print("  t %.0f: |E_int| sotto %g E[1] (%.3e) da d = %s (fase 0), %s (fase pi), e per ogni d dopo" % (t * s, SOGLIA_INT, SOGLIA_INT * abs(E1), dist[(t, 0)], dist[(t, 1)]))
    print("  ### LA DISTANZA SOTTO %g E[1], per t 0, 15000, 30000: fase 0 %s; fase pi %s" % (SOGLIA_INT, [dist[(t, 0)] for t in STATI_MATURI], [dist[(t, 1)] for t in STATI_MATURI]))
    print("  ### le definizioni (il task history 10.1): materia = E[psi1 + psi2, phi0] - E[psi1, phi0] - E[psi2, phi0] + E[0]; vuoto = E[0, phi0 + D1 + D2] - E[0, phi0 + D1] - E[0, phi0 + D2] + E[0];"
          " il resto = E_int - materia - vuoto; la fase pi cambia segno solo a psi2; t 0 TF3 = la colonna di statica_coppia.txt (la partenza di TF3, non lo stato di TBS)")
    cm.__exit__(None, None, None)


def SFM_sha(x):
    import _stato_fermo as SFM
    return SFM.sha(x)


def dimensione():
    import _energia_del_legame as EL
    import _vuoto_vivo_B as V
    from solitone import carta_forma as CF
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    print("  %8s %9s %9s %10s %12s %10s %10s %10s %10s %s" % ("N", "w0", "w", "3w / 40.5", "rho max", "spessore", "esag 100", "esag 300", "verdetto", "R(soglie scalate)"))
    ww = {}
    for N in NN:
        rec, z, p0, F3, _info, cm = costruisci(N, V.L)
        L = z["L"]
        st = {"psi_h": p0, "phi_h": F3}
        rho, _lam = EL.densita(z["inc"], st)
        v = np.arange(z["inc"].n)
        m1, m2 = v // L, v % L
        c1, c2 = TO.centro(rho, m1, m2, L)[:2]
        P = CF.posizioni(m1, m2, A1, A2)
        r, th = CF.spost(P, c1 * A1 + c2 * A2, L, A1, A2)
        w = math.sqrt(float(np.sum(rho * r ** 2) / rho.sum()))
        ww[N] = w
        sc = N / 1e6
        Rmax = TO.meta_periodo(L)
        ff = {sg: CF.forma(rho, r, th, sg * sc, Rmax) for sg in SOGLIE}
        sp = float(np.mean(ff[1.0]["R"] - ff[300.0]["R"])) if ff[1.0] and ff[300.0] else float("nan")
        print("  %8.2e %9.4f %9.4f %10.3f %12.4e %10.3f %10.4f %10.4f %10s %s" % (N, rec["larghezza"], w, 3 * w / 40.5, float(rho.max()), sp, ff[100.0]["esag"] if ff[100.0] else float("nan"),
                                                                                ff[300.0]["esag"] if ff[300.0] else float("nan"), str(rec.get("verdetto"))[:10],
                                                                                " ".join("%.2f" % f["R0"] if f else "-" for f in ff.values())))
        cm.__exit__(None, None, None)
    esito("DEVE FALLIRE: DM-F w a N 2e6 = w a N 1e6 (se fossero uguali, la carta non vedrebbe N)", not ww[2e6] == ww[1e6], "%.6f contro %.6f" % (ww[2e6], ww[1e6]))
    print("  ### le soglie della forma scalate per N / 1e6; lo spessore = R(rho >= 1 scal.) - R(rho >= 300 scal.); 3w / 40.5 sopra 1: il solitone tocca la meta' del periodo (la riga non conta)")


def main(argv):
    import _presidio
    for m in ("__init__", "corsa_accensione", "accensione", "toro", "carta_forma", "protetto"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    modo = "--vuoto" if "--vuoto" in argv else "--coppia-matura" if "--coppia-matura" in argv else "--coppia" if "--coppia" in argv else "--dimensione" if "--dimensione" in argv else None
    assert modo, "uso: --vuoto | --coppia | --coppia-matura | --dimensione"
    print("=" * 130)
    print("LE CARTE STATICHE (Luca 2026-11-05 15:28, 15:42): %s; nessuna corsa; NN %s L_COPPIA %d DD %d .. %d; AMP %g TOLL_L %g TOLL_A %g TOLL_G %g TOLL_E %g GAP_ZERO %g"
          % (modo, NN, L_COPPIA, DD[0], DD[-1], AMP, TOLL_L, TOLL_A, TOLL_G, TOLL_E, GAP_ZERO))
    print("=" * 130)
    cs0()
    {"--vuoto": vuoto, "--coppia": coppia, "--coppia-matura": coppia_matura, "--dimensione": dimensione}[modo]()
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
