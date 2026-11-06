# -*- coding: utf-8 -*-
r"""**LE TRE CARTE STATICHE: IL VUOTO, LA COPPIA, LA DIMENSIONE** *(Luca `2026-11-05` `15:28`, l'ordine delle `15:42`; il task history `doc/TASK_HISTORY/2026-11-05_carte_statiche.md`)* -- **nessuna corsa**
    python csv/solitone/carta_statiche.py --vuoto > doc/referti_l2/statica_vuoto.txt
    python csv/solitone/carta_statiche.py --coppia > doc/referti_l2/statica_coppia.txt
    python csv/solitone/carta_statiche.py --dimensione > doc/referti_l2/statica_dimensione.txt
    python csv/solitone/carta_statiche.py --coppia-matura > doc/referti_l2/statica_coppia_matura.txt   # (Luca 2026-11-05 21:01) gli stati maturi di TBS
    python csv/solitone/carta_statiche.py --circolazione > doc/referti_l2/statica_circolazione.txt   # (Luca 2026-11-05 21:20, 2026-11-06) B: la circolazione della materia dagli stati di TBS
    python csv/solitone/carta_statiche.py --vortici > doc/referti_l2/statica_vortici.txt   # (Luca 2026-11-05 21:20, 2026-11-06) C: i vortici della fase del vuoto e di psi
    python csv/solitone/carta_statiche.py --olonomia > doc/referti_l2/statica_olonomia.txt   # (Luca 2026-11-05 21:39, 2026-11-06) E: l'olonomia di U attorno ai triangoli
    python csv/solitone/carta_statiche.py --brezzi > doc/referti_l2/statica_brezzi.txt   # (Luca 2026-11-06 19:41) IS1: la visibilita' dei rami del vuoto dalla materia (inf-sup)
    python csv/solitone/carta_statiche.py --passo > doc/referti_l2/statica_passo.txt   # (Luca 2026-11-06 19:41) IS2: il ramo piatto e il Goldstone a s 0.10, 0.15, 0.20
    python csv/solitone/carta_statiche.py --cs-onde > doc/referti_l2/statica_cs_onde.txt   # (Luca 2026-11-06 19:41-20:00) IS3: cs (tick_con_cs, Lambda_c dal vuoto) sulle onde del vuoto
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
KAPPA_G = (0.005, 0.01, 0.02, 0.04, 0.08)     # ### --goldstone (Luca 2026-11-05 21:20, la misura A): |k| piccoli; una scelta di protocollo mia, dichiarata (il task history della rotazione, 1)
DIREZIONI_G = (("A1", 0.0), ("30 gradi", 30.0))   # ### Luca 21:20: lungo A1 e a 30 gradi
N_GOLD = 6                     # ### a Gamma sei fasi zero (statica_vuoto.txt): il Goldstone e i suoi compagni, seguiti INSIEME (le sei |fasi| piu' piccole a ogni k)
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


def vuoto(goldstone=False):
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
    if goldstone:
        goldstone_carta(T, ev, a if nonzero else None, s)
    cm.__exit__(None, None, None)


def goldstone_carta(T, ev0, a_oggi, s):
    """### **La misura A** *(Luca 2026-11-05 21:20; il task history `2026-11-05_rotazione_triangoli`, 1)*: il ramo del Goldstone *(le `N_GOLD` fasi zero a `Gamma`)* lungo `A1` e a `30` gradi."""
    print("-" * 130)
    print("### A. IL GOLDSTONE (Luca 21:20): le %d |fasi| piu' piccole di T(k) a ogni k (a Gamma sono zero: il Goldstone e i suoi compagni), per |k| %s; il pavimento della fase per tick %.1e (10 x 1e-16 / AMP)"
          % (N_GOLD, KAPPA_G, PAV_T / AMP))
    g0 = np.sort(np.abs(np.angle(ev0)))
    print("  a Gamma le %d piu' piccole: %s; la prossima %.6e" % (N_GOLD, " ".join("%.3e" % x for x in g0[:N_GOLD]), g0[N_GOLD]))
    pav_w = PAV_T / AMP / s
    for nome_d, gradi in DIREZIONI_G:
        u = np.array([math.cos(math.radians(gradi)), math.sin(math.radians(gradi))])
        wmax = []
        for kap in KAPPA_G:
            fs = np.sort(np.abs(np.angle(np.linalg.eigvals(T(kap * u)))))
            wmax.append(float(fs[N_GOLD - 1]) / s)
            print("  %-9s |k| %.3f: le %d omega (per unita' di tempo) %s; la prossima %.6e" % (nome_d, kap, N_GOLD, " ".join("%.3e" % (x / s) for x in fs[:N_GOLD]), fs[N_GOLD] / s))
        kk, ww = np.array(KAPPA_G), np.array(wmax)
        v_or = float(np.sum(kk * ww) / np.sum(kk * kk))
        cf = np.polyfit(kk, ww, 2)
        print("  ### %-9s la omega piu' grande delle %d: %s; la velocita' (la pendenza per l'origine) %.6e; il fit omega = c0 + v |k| + b |k|^2: c0 %+.3e, v %+.6e, b %+.6e; il pavimento in omega %.1e (in velocita' a |k| %.3f: %.1e)"
              % (nome_d, N_GOLD, " ".join("%.3e" % x for x in wmax), v_or, cf[2], cf[1], cf[0], pav_w, KAPPA_G[0], pav_w / KAPPA_G[0]))
        print("  ### %-9s la lettura scritta prima (Luca): %s" % (nome_d, "SOPRA il pavimento a ogni |k|: il Goldstone PROPAGA" if all(w > 10 * pav_w for w in wmax)
              else "ENTRO 10 x il pavimento a ogni |k|: il vuoto e' RIGIDO anche li'" if all(w <= 10 * pav_w for w in wmax) else "misto: sopra a qualche |k|, entro ad altri (dichiarato)"))
    lam0 = None
    nz = [i for i in range(len(ev0)) if abs(np.angle(ev0[i])) > GAP_ZERO]
    if nz:
        ig = min(nz, key=lambda i: abs(np.angle(ev0[i])))
        Dr = abs(np.angle(ev0[ig])) / s
        prev = ev0[ig]
        rr = []
        for kap in KAPPA:
            e2 = np.linalg.eigvals(T(np.array([kap, 0.0])))
            prev = e2[int(np.argmin(np.abs(e2 - prev)))]
            rr.append(abs(np.angle(prev)) / s)
        lam0 = float(np.polyfit(np.array(KAPPA) ** 2, np.array(rr) - Dr, 1)[0])
    rif = None
    f_rif = os.path.join(DIR_REF, "statica_vuoto.txt")
    if os.path.exists(f_rif):
        for l in open(f_rif, encoding="utf-8"):
            if "la curvatura a = d omega / d k^2 =" in l:
                rif = l.split("=")[2].split()[0]   # ### "la curvatura a = d omega / d k^2 = <numero> ..."
    esito("DEVE PASSARE: GA-PI la stessa misura sul ramo a pi ridà la curvatura di 60de22ec (%s, statica_vuoto.txt), e quella di questa corsa" % rif,
          lam0 is not None and rif is not None and ("%+.6e" % lam0) == rif and lam0 == a_oggi, "%+.6e" % lam0 if lam0 is not None else "nessun ramo")


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


PAV_C = 10.0 * 1e-16           # ### --circolazione (il task history della rotazione, 9.1): il pavimento di J e di C_T, per max rho
N_ANELLI = 41                  # ### anelli di larghezza 1 nodo da 0 a 40 (9.1)
R_GAMMA = tuple(range(4, 41, 4))   # ### Gamma(R), la somma di C_T dentro R (9.1)
FASCE_S = (0, 10, 20, 30, 40)  # ### il segno per settore: 6 settori di 60 gradi, fasce di 10 nodi (9.1)
CONTIGUI = 3                   # ### la lettura (r4) di B (9.3): almeno 3 anelli contigui con un verso preferito dello stesso segno


def _tick_correnti(z, t, K):
    """### **Il tick `AC.tick(z, t, K)` della corsa, con le voci di `mot.operatori` avvolte IN MEMORIA** *(rimesse all'uscita)*: per ogni applicazione di
    `spostamento_trasporto` la corrente dell'arco `J_a = |psi'_{2a+1}|^2 - |psi_{2a+1}|^2` *(dal nodo proprietario al vicino)* e lo scarto dalla coda;
    per ogni altro pezzo la variazione della norma per nodo *(il task history della rotazione, 9.1)*."""
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    from solitone import accensione as AC
    inc, mot = z["inc"], z["mot"]
    nodo = np.asarray(inc.nodo)
    n = inc.n
    rec = {"J": [], "unit": 0.0, "altri": {}}
    veri = dict(mot.operatori)

    def avvolgi(nome, f):
        def g(s, p, fr):
            a = np.sum(np.abs(s["psi_h"]) ** 2, axis=1)
            out = f(s, p, fr)
            d = np.sum(np.abs(s["psi_h"]) ** 2, axis=1) - a
            if nome == "spostamento_trasporto":
                rec["J"].append(d[1::2].copy())
                rec["unit"] = max(rec["unit"], float(np.max(np.abs(d[1::2] + d[0::2]))))
            else:
                dn = float(np.max(np.abs(np.bincount(nodo, weights=d, minlength=n))))
                rec["altri"][nome] = max(rec["altri"].get(nome, 0.0), dn)
            return out
        return g

    for k_, f_ in veri.items():
        mot.operatori[k_] = avvolgi(k_, f_)
    try:
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            AC.tick(z, t, K)
    finally:
        for k_, f_ in veri.items():
            mot.operatori[k_] = f_
    return rec


def _triangoli(z, dirs, A1, A2):
    """### **I triangoli su e giu' in `(m1, m2)`, con gli archi e il segno del giro ANTIORARIO** *(dall'area con le posizioni vere, non scritto a mano)*."""
    inc, L = z["inc"], z["L"]
    n = inc.n
    nodo = np.asarray(inc.nodo)
    v = np.arange(n)
    m1, m2 = v // L, v % L

    def nd(a, b):
        return ((m1 + a) % L) * L + (m2 + b) % L

    def arco(base, d):
        a = 3 * base + dirs.index(d)
        verso = ((base // L + d[0]) % L) * L + (base % L + d[1]) % L
        assert np.array_equal(nodo[2 * a], base) and np.array_equal(nodo[2 * a + 1], verso), "l'arco NON va dove dice la direzione"
        return a

    out = {}
    for nome, (p1, p2) in (("su", ((1, 0), (1, 1))), ("giu'", ((0, 1), (1, 1)))):
        e1 = arco(v, p1)                                            # v -> v + p1
        e2 = arco(nd(*p1), (p2[0] - p1[0], p2[1] - p1[1]))          # v + p1 -> v + p2
        e3 = arco(v, p2)                                            # v -> v + p2 (percorso all'indietro)
        o1 = p1[0] * A1 + p1[1] * A2
        o2 = p2[0] * A1 + p2[1] * A2
        area = float(o1[0] * o2[1] - o1[1] * o2[0])
        assert area != 0.0
        out[nome] = {"archi": (e1, e2, e3), "verso": 1.0 if area > 0 else -1.0, "off": (o1 + o2) / 3.0}
    return out


def _per_anelli(C, r, th, pav):
    """### **Per anello** *(larghezza `1`)*: la media col segno, la media dei moduli, `N`, `sigma` della media, il verso preferito *(9.3)*."""
    righe = []
    for k in range(N_ANELLI):
        m = (r >= k) & (r < k + 1)
        if not m.any():
            righe.append((k, 0, 0.0, 0.0, 0.0, 0))
            continue
        c = C[m]
        me = float(np.mean(c))
        sg = float(np.std(c) / math.sqrt(len(c))) if len(c) > 1 else float("inf")
        pref = int(np.sign(me)) if (abs(me) > 3.0 * sg and abs(me) > pav) else 0
        righe.append((k, int(m.sum()), me, float(np.mean(np.abs(c))), sg, pref))
    return righe


def _contigui(righe):
    """### **Il massimo numero di anelli CONTIGUI con un verso preferito dello stesso segno, e il segno** *(9.3)*."""
    best, seg, cur, cs = 0, 0, 0, 0
    for _k, _n, _me, _ma, _sg, p in righe:
        if p != 0 and p == cs:
            cur += 1
        else:
            cur, cs = (1, p) if p != 0 else (0, 0)
        if cur > best:
            best, seg = cur, cs
    return best, seg


def _circola(z, dirs, A1, A2, tri, st, t, K, nome, stampa=True):
    """### **La circolazione di uno stato:** il tick della corsa con le correnti, i DEVE dell'unitarieta', degli altri pezzi e della continuita', poi `C_T`."""
    import _energia_del_legame as EL
    from solitone import carta_forma as CF
    from solitone import toro as TO
    inc, L = z["inc"], z["L"]
    n = inc.n
    nodo = np.asarray(inc.nodo)
    for k_, v_ in st.items():
        z["st"][k_][...] = v_
    rho0 = np.bincount(nodo, weights=np.sum(np.abs(z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
    rho_d, _lam = EL.densita(inc, {"psi_h": z["st"]["psi_h"], "phi_h": z["st"]["phi_h"]})
    v = np.arange(n)
    m1, m2 = v // L, v % L
    rmax = float(rho0.max()) if rho0.max() > 0 else 1.0
    pav = PAV_C * rmax
    rec = _tick_correnti(z, t, K)
    rho1 = np.bincount(nodo, weights=np.sum(np.abs(z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
    assert len(rec["J"]) == 2, "lo spostamento NON e' applicato due volte nel tick (il palindromo)"
    J = rec["J"][0] + rec["J"][1]
    pred = -np.bincount(nodo[0::2], weights=J, minlength=n) + np.bincount(nodo[1::2], weights=J, minlength=n)
    e_cont = float(np.max(np.abs((rho1 - rho0) - pred)))
    e_altri = max(rec["altri"].values()) if rec["altri"] else 0.0
    c1, c2 = TO.centro(rho0, m1, m2, L)[:2] if rho0.sum() > 0 else (0.0, 0.0)
    cen = c1 * A1 + c2 * A2
    P = CF.posizioni(m1, m2, A1, A2)
    res = {"pav": pav, "unit": rec["unit"], "altri": rec["altri"], "cont": e_cont, "rho_d": float(np.max(np.abs(rho_d - rho0))), "centro": (c1, c2)}
    for meta, JJ in (("tick", J), ("prima meta'", rec["J"][0]), ("seconda meta'", rec["J"][1])):
        Cs, rs, ths = [], [], []
        for tn in ("su", "giu'"):
            d = tri[tn]
            e1, e2, e3 = d["archi"]
            C = d["verso"] * (JJ[e1] + JJ[e2] - JJ[e3])
            r, th = CF.spost(P + d["off"], cen, L, A1, A2)
            Cs.append(C)
            rs.append(r)
            ths.append(th)
            res[(meta, tn)] = _per_anelli(C, r, th, pav)
        C, r, th = np.concatenate(Cs), np.concatenate(rs), np.concatenate(ths)
        res[(meta, "tutti")] = _per_anelli(C, r, th, pav)
        res[(meta, "Gamma")] = [(R, float(np.sum(C[r < R])), int(np.sum(r < R))) for R in R_GAMMA]
        res[(meta, "settori")] = [(a, b, [float(np.mean(C[(r >= a) & (r < b) & (th >= s_ * math.pi / 3) & (th < (s_ + 1) * math.pi / 3)]))
                                          if np.any((r >= a) & (r < b) & (th >= s_ * math.pi / 3) & (th < (s_ + 1) * math.pi / 3)) else float("nan") for s_ in range(6)])
                                  for a, b in zip(FASCE_S[:-1], FASCE_S[1:])]
        res[(meta, "max")] = float(np.max(np.abs(C)))
    if stampa:
        print("  ### %s: il centro (%.4f, %.4f); max rho %.6e; il pavimento di C_T %.3e; |J testa + J coda| max %.3e; gli altri pezzi, max |d rho_nodo| %s; la continuita' %.3e; rho dal libro - rho per nodo %.3e"
              % (nome, c1, c2, rmax, pav, rec["unit"], ", ".join("%s %.2e" % kv for kv in sorted(rec["altri"].items())), e_cont, res["rho_d"]))
        for meta in ("tick", "prima meta'", "seconda meta'"):
            print("    %s: max |C_T| %.6e" % (meta, res[(meta, "max")]))
        print("    %4s %6s %16s %14s %12s %5s | %16s %5s | %16s %5s   (tick intero; su, giu' a parte)" % ("anel", "N", "media C_T", "media |C_T|", "sigma", "verso", "su: media", "verso", "giu': media", "verso"))
        for i, (k, nn, me, ma, sg, p) in enumerate(res[("tick", "tutti")]):
            su, gi = res[("tick", "su")][i], res[("tick", "giu'")][i]
            print("    %4d %6d %+16.6e %14.6e %12.3e %+5d | %+16.6e %+5d | %+16.6e %+5d" % (k, nn, me, ma, sg, p, su[2], su[5], gi[2], gi[5]))
        for meta in ("prima meta'", "seconda meta'"):
            print("    %s, la media per anello: %s" % (meta, " ".join("%+.2e" % x[2] for x in res[(meta, "tutti")])))
        print("    Gamma(R) (tick): %s" % "; ".join("R %d: %+.6e (%d triangoli)" % g for g in res[("tick", "Gamma")]))
        print("    il segno per settore (tick; i settori di 60 gradi da theta 0, la media di C_T):")
        for a, b, ss in res[("tick", "settori")]:
            print("      r %2d-%2d: %s" % (a, b, " ".join("%+.3e" % x for x in ss)))
        cn, sg = _contigui(res[("tick", "tutti")])
        print("    gli anelli contigui con un verso preferito dello stesso segno: %d (il segno %+d)" % (cn, sg))
    return res


R_SERIE = 12                   # ### Luca 2026-11-06 11:08: il segno di Gamma(12) su tutti gli stati salvati di TBS


def _serie_verso(z, dirs, A1, A2, tri, K, reg, s):
    """### **Luca `11:08`: il segno di `Gamma(12)` su TUTTI gli stati salvati di `TBS`** *(stabile, nasce, cambia: le letture del task history della rotazione, 11)*; **e i
    DEVE `CI-U`, `CI-A`, `CI-C` su ogni stato.** ### **E `TB3`: gli stati registrati nei suoi jsonl, CONTATI.**"""
    import _vuoto_vivo_B as V
    import composizione as CM
    from solitone import corsa_accensione as CA
    NP = len(CM.ORDINE)
    tt = sorted(reg)
    print("  ### LA SERIE DEL VERSO (Luca 11:08): %d stati di TBS, i tick %s" % (len(tt), tt))
    print("  %7s %7s %5s %16s %12s %5s %16s %12s %12s %12s %10s %10s %10s" % ("t", "tick", "sha", "Gamma(12)", "pavimento", "segno", "Gamma(16)", "anello 0", "anello 1", "anello 2", "unit", "altri", "cont"))
    serie, eS, eU, eA, eC = [], [], [], [], []
    for t in tt:
        f = reg[t]["file"]
        with np.load(f) as d:
            st = {k: d[k].copy() for k in d.files if k != "t"}
        ok_s = all(SFM_sha(st[k]) == reg[t]["sha"][k] for k in reg[t]["sha"])
        r = _circola(z, dirs, A1, A2, tri, st, t + 1, K, "", stampa=False)
        g = {R_: (G_, N_) for R_, G_, N_ in r[("tick", "Gamma")]}
        G12, N12 = g[R_SERIE]
        pav = N12 * r["pav"]
        sg = int(np.sign(G12)) if abs(G12) > pav else 0
        an = [x[2] for x in r[("tick", "tutti")][:3]]
        altri = max(r["altri"].values())
        eS.append(ok_s)
        eU.append(r["unit"] <= r["pav"])
        eA.append(altri <= r["pav"])
        eC.append(r["cont"] <= NP * r["pav"])
        serie.append((t, sg))
        print("  %7.0f %7d %5s %+16.6e %12.3e %+5d %+16.6e %+12.4e %+12.4e %+12.4e %10.2e %10.2e %10.2e" % (t * s, t, "ok" if ok_s else "NO", G12, pav, sg, g[16][0], an[0], an[1], an[2], r["unit"], altri, r["cont"]))
    esito("DEVE PASSARE: CI-S21 ogni stato di TBS da' gli sha per chiave registrati nella corsa", all(eS), "%d/%d" % (sum(eS), len(eS)))
    esito("DEVE PASSARE: CI-U21 (mio) l'unitarieta' del blocco su ogni stato", all(eU), "%d/%d" % (sum(eU), len(eU)))
    esito("DEVE PASSARE: CI-A21 (mio) gli altri pezzi non cambiano la norma dei nodi, ogni stato", all(eA), "%d/%d" % (sum(eA), len(eA)))
    esito("DEVE PASSARE: CI-C21 (mio; il pavimento di Luca 11:08) la continuita' entro %d x il pavimento, ogni stato" % NP, all(eC), "%d/%d" % (sum(eC), len(eC)))
    dopo = [(t, sg) for t, sg in serie if t > 0]
    sopra = [i for i, (_t, sg) in enumerate(dopo) if sg != 0]
    if not sopra:
        lett = "altro: Gamma(12) sotto il pavimento a ogni t > 0"
        t1 = None
    else:
        i1 = sopra[0]
        t1 = dopo[i1][0]
        coda = [sg for _t, sg in dopo[i1:]]
        interr = sum(1 for x in coda if x == 0)
        segni = [x for x in coda if x != 0]
        nc = sum(1 for a, b in zip(segni[:-1], segni[1:]) if a != b)
        primo = dopo[0][0]
        if nc >= 1:
            lett = "CAMBIA (%d cambi di segno da t %.0f; %d interruzioni)" % (nc, t1 * s, interr)
        elif interr == 0 and t1 == primo:
            lett = "STABILE (il segno %+d da t %.0f, il primo stato dopo t 0)" % (segni[0], t1 * s)
        elif interr == 0:
            lett = "NASCE a t %.0f (il segno %+d, poi stabile)" % (t1 * s, segni[0])
        else:
            lett = "altro: nessun cambio di segno, %d interruzioni sotto il pavimento dopo t %.0f" % (interr, t1 * s)
    print("  ### LA LETTURA DELLA SERIE (il task history 11): t_1 %s; i segni %s" % ("%.0f" % (t1 * s) if t1 is not None else "-", " ".join("%+d" % sg for _t, sg in serie)))
    print("  ### IL VERSO NEL TEMPO: %s" % lett)
    righe = [V.LP.leggi(os.path.join(CA.dir_json("TB3"), f)) for f in sorted(os.listdir(CA.dir_json("TB3"))) if f.startswith("TB3_") and f.endswith(".jsonl")]
    n3 = sum(len(r.get("stati") or []) for r in righe)
    print("  ### TB3: %d jsonl, %d stati registrati; nella corsa STATI ha la voce TB3: %s -- %s" % (len(righe), n3, "TB3" in CA.STATI,
          "il conto su TB3 NON si puo' fare (nessuno stato con la fase di psi)" if n3 == 0 else "### CI SONO STATI: il conto va fatto"))


def circolazione():
    """### **B** *(Luca `2026-11-05` `21:20`; `2026-11-06`: avanti)*: **la circolazione della materia attorno ai triangoli, dagli stati di `TBS`** *(il task history della rotazione, 9)*."""
    import _vuoto_vivo_B as V
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    _sol, _v, s = V.CORSE[CA.NOME]
    K = int(round(CA.CORSE["TF3"][0] / s))
    righe = [V.LP.leggi(os.path.join(CA.dir_json("TBS"), f)) for f in sorted(os.listdir(CA.dir_json("TBS"))) if f.startswith("TBS_") and f.endswith(".jsonl")]
    reg = {x["t"]: x for r in righe for x in (r.get("stati") or [])}
    _r8, z, _p8, F3, _i8, cm = costruisci(V.N, 81)
    A1, A2 = TO.vettori()
    dirs = _ordine_archi(z)
    tri = _triangoli(z, dirs, A1, A2)
    print("  le direzioni degli archi %s; il verso antiorario: su %+d, giu' %+d; K %d; PAV_C %g; N_ANELLI %d; R_GAMMA %s; FASCE_S %s; CONTIGUI %d"
          % (dirs, tri["su"]["verso"], tri["giu'"]["verso"], K, PAV_C, N_ANELLI, R_GAMMA, FASCE_S, CONTIGUI))
    salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
    stati = {}
    eS = []
    for t in STATI_MATURI:
        f = reg[t]["file"]
        with np.load(f) as d:
            st = {k: d[k].copy() for k in d.files if k != "t"}
        eS.append(all(SFM_sha(st[k]) == reg[t]["sha"][k] for k in reg[t]["sha"]))
        stati[t] = st
        print("  lo stato a t %.0f (tick %d): %s sha1 %s" % (t * s, t, f, hashlib.sha1(open(f, "rb").read()).hexdigest()))
    esito("DEVE PASSARE: CI-S ogni stato caricato da' gli sha per chiave registrati nella corsa", all(eS), "%s" % eS)
    # ### il DEVE di Luca: il vuoto F3 da solo (psi = 0) -- uno zero PER COSTRUZIONE (9.2)
    st0 = {k: v.copy() for k, v in salvato.items()}
    st0["psi_h"][...] = 0.0
    st0["phi_h"][...] = F3
    r0 = _circola(z, dirs, A1, A2, tri, st0, K + 1, K, "il vuoto F3 da solo", stampa=False)
    esito("DEVE PASSARE: CI-0 (Luca) il vuoto F3 da solo (psi = 0, dopo la rampa) da' C_T = 0 -- uno zero PER COSTRUZIONE: controlla il percorso del codice", r0[("tick", "max")] == 0.0, "max |C_T| %.3e" % r0[("tick", "max")])
    res = {}
    for t in STATI_MATURI:
        res[t] = _circola(z, dirs, A1, A2, tri, stati[t], t + 1, K, "TBS a t %.0f (il tick %d della corsa)" % (t * s, t + 1))
    esito("DEVE PASSARE: CI-U (mio) l'unitarieta' del blocco: J dalla testa = -J dalla coda entro il pavimento, ogni applicazione, ogni stato",
          all(res[t]["unit"] <= res[t]["pav"] for t in STATI_MATURI), "; ".join("%.3e (pav %.1e)" % (res[t]["unit"], res[t]["pav"]) for t in STATI_MATURI))
    esito("DEVE PASSARE: CI-A (mio) i pezzi diversi dallo spostamento non cambiano la norma di nessun nodo, entro il pavimento",
          all(max(res[t]["altri"].values()) <= res[t]["pav"] for t in STATI_MATURI), "; ".join("%.3e" % max(res[t]["altri"].values()) for t in STATI_MATURI))
    import composizione as CM
    NP = len(CM.ORDINE)               # ### Luca 2026-11-06 11:08: il pavimento di CI-C = i pezzi del tick x PAV_C x max rho (gli errori si sommano al piu' linearmente)
    esito("DEVE PASSARE: CI-C (mio; il pavimento di Luca 11:08) la continuita': rho(t + 1) - rho(t) = -div J entro %d (i pezzi del tick) x il pavimento, ogni nodo, ogni stato" % NP,
          all(res[t]["cont"] <= NP * res[t]["pav"] for t in STATI_MATURI), "; ".join("%.3e (pav %.1e)" % (res[t]["cont"], NP * res[t]["pav"]) for t in STATI_MATURI))
    # ### il DEVE FALLIRE di Luca: lo stato di t 0 per e^{+i theta} attorno al centro (9.2)
    L = z["L"]
    nodo = np.asarray(z["inc"].nodo)
    v = np.arange(z["inc"].n)
    from solitone import carta_forma as CF
    c1, c2 = res[0]["centro"]
    _r, thn = CF.spost(CF.posizioni(v // L, v % L, A1, A2), c1 * A1 + c2 * A2, L, A1, A2)
    gam = {}
    for sg in (+1, -1):
        sts = {k: x.copy() for k, x in stati[0].items()}
        sts["psi_h"] = sts["psi_h"] * np.exp(1j * sg * thn[nodo])[:, None]
        rs = _circola(z, dirs, A1, A2, tri, sts, 1, K, "il sintetico: lo stato di t 0 per e^{%si theta}" % ("+" if sg > 0 else "-"))
        gam[sg] = rs[("tick", "Gamma")]
        if sg > 0:
            cn, segno = _contigui(rs[("tick", "tutti")])
            esito("DEVE FALLIRE: CI-F (Luca) il sintetico e^{+i theta}: \"nessun verso preferito\" (meno di %d anelli contigui con lo stesso verso)" % CONTIGUI,
                  not (cn < CONTIGUI), "%d anelli contigui (il segno %+d)" % (cn, segno))
    pavG = [res[0]["pav"] * g[2] for g in gam[1]]
    ok = [(a[1] * b[1] < 0) for a, b, p in zip(gam[1], gam[-1], pavG) if abs(a[1]) > p and abs(b[1]) > p]
    esito("DEVE PASSARE: CI-V (mio) Gamma(R) col sintetico e^{-i theta} ha il segno opposto a quello con e^{+i theta}, a ogni R dove entrambi sono sopra il pavimento",
          len(ok) > 0 and all(ok), "%d raggi confrontati: %s" % (len(ok), "; ".join("R %d %+.3e / %+.3e" % (a[0], a[1], b[1]) for a, b in zip(gam[1], gam[-1]))))
    _serie_verso(z, dirs, A1, A2, tri, K, reg, s)
    for k_, v_ in salvato.items():
        z["st"][k_][...] = v_
    cm.__exit__(None, None, None)
    print("  ### LA LETTURA (r4) DI B (il task history 9.3): gli anelli contigui con un verso preferito dello stesso segno, t 0 / 15000 / 30000: %s; la soglia %d"
          % (" / ".join("%d (%+d)" % _contigui(res[t][("tick", "tutti")]) for t in STATI_MATURI), CONTIGUI))
    print("  ### (r4) per B: %s" % ("SI'" if any(_contigui(res[t][("tick", "tutti")])[0] >= CONTIGUI for t in STATI_MATURI[1:]) else "NO"))
    _numeri_di_prima()


PRIMA_CIRC = "9b8a0e5f"          # ### Luca 11:08: il referto rifatto stampa accanto i numeri di prima (il referto di B col pavimento vecchio di CI-C)


def _numeri_di_prima():
    """### **I numeri di prima** *(Luca 11:08)*: le righe dei DEVE e della lettura dal referto di `PRIMA_CIRC`, **letti con `git show`, non ricopiati.**"""
    import subprocess
    t = subprocess.check_output(["git", "show", PRIMA_CIRC + ":doc/referti_l2/statica_circolazione.txt"], cwd=solitone.RADICE).decode("utf-8")
    print("  ### I NUMERI DI PRIMA (il referto a %s, il pavimento di CI-C per un C_T):" % PRIMA_CIRC)
    for l in t.splitlines():
        if "DEVE" in l or "(r4)" in l or l.startswith("ESITO"):
            print("    prima | %s" % l.strip()[:300])


MOD_FASE = 1e-12               # ### --vortici (il task history della rotazione, 13.1): una fase per nodo non e' definita sotto 1e-12 del massimo del modulo della proiezione
R_VORT = 20.0                  # ### 13.2: il vortice sintetico si conta dentro r < 20 (sul toro il compagno sta sul taglio dell'immagine minima)
SOGLIA_ANELLO_V = 5            # ### 13.3: un anello con 5 o piu' vortici di un segno solo


def _vortici(z, tri, A1, A2, chi, buono, cen):
    """### **I vortici dei triangoli** *(13.1)*: `w_T` dalle tre differenze di `chi` ridotte in `(-pi, pi]` lungo il giro antiorario; esclusi i triangoli con una fase non definita."""
    from solitone import carta_forma as CF
    inc, L = z["inc"], z["L"]
    n = inc.n
    nodo = np.asarray(inc.nodo)
    v = np.arange(n)
    m1, m2 = v // L, v % L
    P = CF.posizioni(m1, m2, A1, A2)
    ws, rs, ok = [], [], []
    for tn in ("su", "giu'"):
        d = tri[tn]
        e1, e2, e3 = d["archi"]
        a, b, c = nodo[2 * e1], nodo[2 * e1 + 1], nodo[2 * e3 + 1]     # v, v + p1, v + p2
        assert np.array_equal(nodo[2 * e2], b) and np.array_equal(nodo[2 * e2 + 1], c)

        def dd(x, y):
            return np.angle(np.exp(1j * (chi[y] - chi[x])))
        w = (dd(a, b) + dd(b, c) + dd(c, a)) / (2 * math.pi)
        w = d["verso"] * w
        r, _th = CF.spost(P + d["off"], cen, L, A1, A2)
        ws.append(np.rint(w).astype(int))
        rs.append(r)
        ok.append(buono[a] & buono[b] & buono[c])
        assert float(np.max(np.abs(w - np.rint(w)))) < 1e-9, "una somma di tre differenze ridotte NON e' un multiplo di 2 pi"
    return np.concatenate(ws), np.concatenate(rs), np.concatenate(ok)


def _conta(nome, w, r, ok, stampa=True):
    w = np.where(ok, w, 0)
    dentro = r < R_VORT
    piu, meno = int(np.sum((w == 1) & dentro)), int(np.sum((w == -1) & dentro))
    altri = int(np.sum((np.abs(w) > 1) & dentro))
    an = []
    for k in range(N_ANELLI):
        m = (r >= k) & (r < k + 1)
        an.append((k, int(np.sum((w == 1) & m)), int(np.sum((w == -1) & m)), int(np.sum(~ok & m))))
    net = [(R_, int(np.sum(w[r < R_]))) for R_ in R_GAMMA]
    if stampa:
        print("    %s: dentro r < %g: +1 %d, -1 %d, |w| > 1 %d; esclusi (fase non definita) %d su %d; fuori: +1 %d, -1 %d"
              % (nome, R_VORT, piu, meno, altri, int(np.sum(~ok)), len(ok), int(np.sum((w == 1) & ~dentro)), int(np.sum((w == -1) & ~dentro))))
        print("      la carica netta dentro R: %s" % "; ".join("R %d: %+d" % x for x in net))
        nz = [x for x in an if x[1] or x[2]]
        print("      gli anelli con vortici (anello, +1, -1, esclusi): %s" % (" ".join("(%d %d %d %d)" % x for x in nz) if nz else "nessuno"))
    return {"piu": piu, "meno": meno, "net": dict(net), "anelli": an}


def vortici():
    """### **C** *(Luca `2026-11-05` `21:20`; `2026-11-06`: dopo B)*: **i vortici della fase del vuoto e di `psi` attorno ai triangoli, dagli stati di `TBS`** *(il task history della rotazione, 13)*."""
    import _vuoto_vivo_B as V
    from solitone import bordo as BO
    from solitone import carta_forma as CF
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab_c, omega = d["c"].copy(), float(d["omega"])
    _sol, _v, s = V.CORSE[CA.NOME]
    K = int(round(CA.CORSE["TF3"][0] / s))
    righe = [V.LP.leggi(os.path.join(CA.dir_json("TBS"), f)) for f in sorted(os.listdir(CA.dir_json("TBS"))) if f.startswith("TBS_") and f.endswith(".jsonl")]
    reg = {x["t"]: x for r in righe for x in (r.get("stati") or [])}
    _r8, z, _p8, F3, _i8, cm = costruisci(V.N, 81)
    A1, A2 = TO.vettori()
    dirs = _ordine_archi(z)
    tri = _triangoli(z, dirs, A1, A2)
    inc, L = z["inc"], z["L"]
    n = inc.n
    nodo = np.asarray(inc.nodo)
    v = np.arange(n)
    m1, m2 = v // L, v % L
    stati, eS = {}, []
    for t in STATI_MATURI:
        f = reg[t]["file"]
        with np.load(f) as d:
            st = {k: d[k].copy() for k in d.files if k != "t"}
        eS.append(all(SFM_sha(st[k]) == reg[t]["sha"][k] for k in reg[t]["sha"]))
        stati[t] = st
        print("  lo stato a t %.0f (tick %d): %s sha1 %s" % (t * s, t, f, hashlib.sha1(open(f, "rb").read()).hexdigest()))
    esito("DEVE PASSARE: VX-S ogni stato caricato da' gli sha per chiave registrati nella corsa", all(eS), "%s" % eS)
    psi0 = stati[0]["psi_h"]
    rho0 = np.bincount(nodo, weights=np.sum(np.abs(psi0) ** 2, axis=1), minlength=n)
    c1, c2 = TO.centro(rho0, m1, m2, L)[:2]
    cen = c1 * A1 + c2 * A2
    print("  il centro di t 0 (%.4f, %.4f); MOD_FASE %g; R_VORT %g; SOGLIA_ANELLO_V %d; la parte di psi SENZA U (13.1)" % (c1, c2, MOD_FASE, R_VORT, SOGLIA_ANELLO_V))

    def chi_vuoto(phi, ct):
        p = np.bincount(nodo, weights=(np.conj(ct * F3) * phi).real, minlength=n) + 1j * np.bincount(nodo, weights=(np.conj(ct * F3) * phi).imag, minlength=n)
        a = np.abs(p)
        return np.angle(p), a > MOD_FASE * a.max()

    def chi_psi(psi):
        q = np.sum(np.conj(psi0) * psi, axis=1)
        p = np.bincount(nodo, weights=q.real, minlength=n) + 1j * np.bincount(nodo, weights=q.imag, minlength=n)
        a = np.abs(p)
        return np.angle(p), a > MOD_FASE * a.max()

    # ### i DEVE sintetici (13.2): il centro del vortice nel baricentro del triangolo "su" piu' vicino al centro
    P = CF.posizioni(m1, m2, A1, A2)
    rT, _t = CF.spost(P + tri["su"]["off"], cen, L, A1, A2)
    cv = P[int(np.argmin(rT))] + tri["su"]["off"]
    _r, thn = CF.spost(P, cv, L, A1, A2)
    c0 = BO.c_di(0, tab_c, K, omega)
    x, b = chi_vuoto(c0 * F3, c0)
    r0 = _conta("il vuoto F3 da solo", *_vortici(z, tri, A1, A2, x, b, cen))
    esito("DEVE PASSARE: VX-0 (Luca) il vuoto F3 da solo da' zero vortici (per costruzione: chi = 0)", r0["piu"] == 0 and r0["meno"] == 0 and all(v_ == 0 for v_ in r0["net"].values()), "+1 %d, -1 %d" % (r0["piu"], r0["meno"]))
    for sg in (+1, -1):
        x, b = chi_vuoto(c0 * F3 * np.exp(1j * sg * thn[nodo]), c0)
        rv = _conta("il vuoto sintetico e^{%si theta}" % ("+" if sg > 0 else "-"), *_vortici(z, tri, A1, A2, x, b, cen))
        x, b = chi_psi(psi0 * np.exp(1j * sg * thn[nodo])[:, None])
        rp = _conta("psi sintetico e^{%si theta}" % ("+" if sg > 0 else "-"), *_vortici(z, tri, A1, A2, x, b, cen))
        if sg > 0:
            esito("DEVE PASSARE: VX-V (Luca) il vuoto sintetico e^{+i theta}: esattamente un +1 e nessun -1 dentro r < %g" % R_VORT, rv["piu"] == 1 and rv["meno"] == 0, "+1 %d, -1 %d" % (rv["piu"], rv["meno"]))
            esito("DEVE PASSARE: VX-P (mio) psi sintetico e^{+i theta}: esattamente un +1 e nessun -1 dentro r < %g" % R_VORT, rp["piu"] == 1 and rp["meno"] == 0, "+1 %d, -1 %d" % (rp["piu"], rp["meno"]))
        else:
            esito("DEVE PASSARE: VX-M (mio) e^{-i theta}: esattamente un -1 e nessun +1 dentro r < %g, nel vuoto e in psi" % R_VORT,
                  rv["meno"] == 1 and rv["piu"] == 0 and rp["meno"] == 1 and rp["piu"] == 0, "vuoto +1 %d -1 %d; psi +1 %d -1 %d" % (rv["piu"], rv["meno"], rp["piu"], rp["meno"]))
    x, b = chi_psi(psi0)
    rf = _conta("psi di t 0 senza la fase", *_vortici(z, tri, A1, A2, x, b, cen))
    esito("DEVE FALLIRE: VX-F (Luca) senza la fase (psi di t 0): \"esattamente un +1 dentro r < %g\"" % R_VORT, not (rf["piu"] == 1 and rf["meno"] == 0), "+1 %d, -1 %d" % (rf["piu"], rf["meno"]))
    lett = []
    for t in STATI_MATURI:
        st = stati[t]
        ct = BO.c_di(t, tab_c, K, omega)
        print("  ### TBS a t %.0f: c(t) %+.12f %+.12fi" % (t * s, ct.real, ct.imag))
        x, b = chi_vuoto(st["phi_h"], ct)
        rv = _conta("il vuoto", *_vortici(z, tri, A1, A2, x, b, cen))
        x, b = chi_psi(st["psi_h"])
        rp = _conta("psi (rispetto alla partenza, senza U)", *_vortici(z, tri, A1, A2, x, b, cen))
        if t > 0:
            for nm, rr in (("vuoto", rv), ("psi", rp)):
                si = rr["net"][20] != 0 or any(max(a_[1], a_[2]) >= SOGLIA_ANELLO_V and min(a_[1], a_[2]) == 0 for a_ in rr["anelli"])
                lett.append((t, nm, rr["net"][20], si))
    cm.__exit__(None, None, None)
    print("  ### LA LETTURA (r4) DI C (il task history 13.3): %s" % "; ".join("t %.0f %s: netto dentro 20 %+d, %s" % (t * s, nm, q, "si'" if si else "no") for t, nm, q, si in lett))
    print("  ### (r4) per C: %s" % ("SI'" if any(si for _t, _n, _q, si in lett) else "NO"))


TOLL_W = 1e-12                 # ### --olonomia (il task history della rotazione, 15.2-15.3): W = I entro 1e-12


def _olonomia(z, tri, U):
    """### **`W` per triangolo** *(15.1)*: `W = U_e3^dagger U_e2 U_e1` lungo `v -> v + p1 -> v + p2 -> v`, `W^dagger` se quel giro e' orario; ### **`{su, giu'}: (W, max |W - I|, phi, a)`.**"""
    out = {}
    for tn in ("su", "giu'"):
        d = tri[tn]
        e1, e2, e3 = d["archi"]
        W = np.einsum("aji,ajk,akl->ail", np.conj(U[e3]), U[e2], U[e1])
        if d["verso"] < 0:
            W = np.conj(np.transpose(W, (0, 2, 1)))
        dW = float(np.max(np.abs(W - np.eye(2))))
        det = np.linalg.det(W)
        phi = np.angle(det) / 2.0
        S = W / np.sqrt(det)[:, None, None]
        a = 2.0 * np.arccos(np.clip(np.abs(np.real(np.trace(S, axis1=1, axis2=2))) / 2.0, 0.0, 1.0))
        out[tn] = (W, dW, phi, a)
    return out


def _u2_casuale(rng, k):
    X = rng.normal(size=(k, 2, 2)) + 1j * rng.normal(size=(k, 2, 2))
    Q, Rr = np.linalg.qr(X)
    dg = np.diagonal(Rr, axis1=1, axis2=2)
    return Q * (dg / np.abs(dg))[:, None, :]


def olonomia():
    """### **E** *(Luca `2026-11-05` `21:39`; `2026-11-06`)*: **l'olonomia di `U` attorno ai triangoli, sul vuoto e nella scena del solitone** *(il task history della rotazione, 15)*."""
    import _vuoto_vivo_B as V
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    _sol, _v, s = V.CORSE[CA.NOME]
    K = int(round(CA.CORSE["TF3"][0] / s))
    righe = [V.LP.leggi(os.path.join(CA.dir_json("TBS"), f)) for f in sorted(os.listdir(CA.dir_json("TBS"))) if f.startswith("TBS_") and f.endswith(".jsonl")]
    reg = {x["t"]: x for r in righe for x in (r.get("stati") or [])}
    _r8, z, _p8, F3, _i8, cm = costruisci(V.N, 81)
    A1, A2 = TO.vettori()
    dirs = _ordine_archi(z)
    tri = _triangoli(z, dirs, A1, A2)
    inc = z["inc"]
    nodo = np.asarray(inc.nodo)
    U = z["mot"].geo.U
    print("  U: forma %s; |U - I| max %.3e; il verso antiorario: su %+d, giu' %+d; TOLL_W %g" % (U.shape, float(np.max(np.abs(U - np.eye(2)))), tri["su"]["verso"], tri["giu'"]["verso"], TOLL_W))
    # ### i controlli (15.2)
    rng = np.random.default_rng(1)
    g = _u2_casuale(rng, inc.n)
    Ug = np.einsum("aij,akj->aik", g[nodo[1::2]], np.conj(g[nodo[0::2]]))     # U_e = g_testa g_coda^dagger
    og = _olonomia(z, tri, Ug)
    eg = max(og[t][1] for t in og)
    esito("DEVE PASSARE: OL-G (mio) una U di pura gauge casuale (seme 1) da' W = I entro %g su ogni triangolo -- il controllo dell'ordine e del verso" % TOLL_W, eg <= TOLL_W, "max |W - I| %.3e" % eg)
    Ur = _u2_casuale(np.random.default_rng(2), inc.m)
    orr = _olonomia(z, tri, Ur)
    er = max(orr[t][1] for t in orr)
    esito("DEVE FALLIRE: OL-F (mio) una U casuale per arco, non di gauge (seme 2): \"W = I entro %g\"" % TOLL_W, not (er <= TOLL_W), "max |W - I| %.3e" % er)
    # ### la U della scena: sul vuoto F3 e nella scena del solitone (la stessa U), e dopo il tick della corsa da t 15000
    U0 = U.copy()
    t = STATI_MATURI[1]
    f = reg[t]["file"]
    with np.load(f) as d:
        st = {k: d[k].copy() for k in d.files if k != "t"}
    salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
    for k_, v_ in st.items():
        z["st"][k_][...] = v_
    _tick_correnti(z, t + 1, K)
    for k_, v_ in salvato.items():
        z["st"][k_][...] = v_
    esito("DEVE PASSARE: OL-T (mio) U della scena uguale al bit prima e dopo il tick della corsa dallo stato di TBS a t %.0f" % (t * s), np.array_equal(U0, z["mot"].geo.U), "sha1 %s / %s" % (SFM_sha(U0), SFM_sha(z["mot"].geo.U)))
    o = _olonomia(z, tri, z["mot"].geo.U)
    for tn in ("su", "giu'"):
        _W, dW, phi, a = o[tn]
        print("    %s: max |W - I| %.3e; il flusso U(1) phi media %+.3e, dispersione %.3e; l'angolo SU(2) a media %.3e, dispersione %.3e" % (tn, dW, float(np.mean(phi)), float(np.std(phi)), float(np.mean(a)), float(np.std(a))))
    dmax = max(o[tn][1] for tn in o)
    if dmax <= TOLL_W:
        lett = "BANALE (max |W - I| %.3e): la parte di psi di C, senza U, E' gia' quella con U" % dmax
    elif max(float(np.std(o[tn][2])) for tn in o) <= TOLL_W and max(float(np.std(o[tn][3])) for tn in o) <= TOLL_W:
        lett = "UNIFORME NON BANALE"
    else:
        lett = "NON UNIFORME"
    cm.__exit__(None, None, None)
    print("  ### LA LETTURA DI E (il task history 15.3): %s" % lett)
    print("  ### ATTENZIONE (15.1): U = I e' costruita dalla scena (csv/_triangoli.scena_toro) e nessun pezzo del tick la scrive: uno zero PER COSTRUZIONE, non una misura della fisica")


KAPPA_IS = (0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5)   # ### --brezzi (il task history 2026-11-06_brezzi_modi_vuoto, 2.1): fino al bordo della zona; una scelta di protocollo mia, dichiarata
PASSO_SEGUI = 0.005            # ### 2.1: i rami seguiti per continuita' a passi di |k| di 0.005 fra i punti della griglia
GRUPPI_IS = (("Z", 4), ("G", 2), ("P", 4), ("D", 2))   # ### 2.1: per |fase| crescente a |k| 0.005: i 4 zeri piatti, il Goldstone, il ramo a pi, il ramo a 2 pi
TOLL_MUTO = 1e-15              # ### IS1-0: il modo muto
TOLL_N = 1e-6                  # ### IS1-N: |T^H T - I| (il TOLL_G di VD-0)
PASSI_S = (0.10, 0.15, 0.20)   # ### Luca 19:41: IS2 a tre s
TOLL_E2 = 1e-12                # ### IS2-E: F3 autovettore del tick (il TOLL_C0)
TOLL_W15 = 1e-15               # ### IS2-15: omega misurato a s 0.15 = quello di fase_F3.npz
TOLL_SEGUE = 1e-6              # ### IS2, la lettura del ramo piatto (l'annotazione 4.2 del task history, scritta prima della carta)


def _cella(z):
    """### **`dove[nodo, l]`**: l'estremita' del nodo con l'etichetta `l` *(direzione e lato; le righe di `vuoto`)*."""
    import _solitone_dal_fondo as SD
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
    return dove


def _T_vuoto(z, F3, K, rot, dove, tk):
    """### **`T(k)` del vuoto `F3` con `psi = 0`, nel riferimento `rot`, col tick `tk(z)`** *(le righe di `vuoto.risposta` col riferimento «oggi» e di `T`)*: `(T, R)`."""
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    from solitone import toro as TO
    L = z["L"]
    n = z["inc"].n
    salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
    R = np.empty((12, n, 12))
    try:
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            for k_, v in salvato.items():
                z["st"][k_][...] = v
            z["st"]["psi_h"][...] = 0.0
            z["st"]["phi_h"][...] = F3
            tk(z)
            base = z["st"]["phi_h"].copy()
            for c in range(12):
                for k_, v in salvato.items():
                    z["st"][k_][...] = v
                z["st"]["psi_h"][...] = 0.0
                ph = F3.copy()
                ph[dove[0, c // 2]] += AMP * (1.0 if c % 2 == 0 else 1j)
                z["st"]["phi_h"][...] = ph
                tk(z)
                per = ((z["st"]["phi_h"] - base) * rot / AMP)[dove]
                R[c] = np.stack([per.real, per.imag], axis=2).reshape(n, 12)
    finally:
        for k_, v in salvato.items():
            z["st"][k_][...] = v
    A1, A2 = TO.vettori()
    nz = np.flatnonzero(np.any(np.abs(R) > 0.0, axis=(0, 2)))
    rs = ((nz // L + L // 2) % L - L // 2)[:, None] * A1 + ((nz % L + L // 2) % L - L // 2)[:, None] * A2
    Rs = R[:, nz, :]

    def T(k):
        return np.einsum("cra,r->ac", Rs, np.exp(-1j * (rs @ k)))
    return T, R


def _reali(v6):
    """### le `6` estremita' complesse -> i `12` reali *(`Re`, `Im` alternati, l'ordine di `risposta`)*."""
    out = np.empty(12)
    out[0::2], out[1::2] = v6.real, v6.imag
    return out


def _coseno(Q, x):
    """### **`|Pi x| / |x|`**, `Pi` il proiettore ortogonale sullo spazio delle colonne ortonormali di `Q`."""
    return float(np.linalg.norm(Q.conj().T @ x) / np.linalg.norm(x))


def _rami(T, u, kk):
    """### **I gruppi seguiti per continuita'** lungo la direzione `u` *(2.1)*: per ogni `|k|` di `kk` `{nome: (fasi, Q, gap)}`."""
    from scipy.optimize import linear_sum_assignment
    ev, V = np.linalg.eig(T(kk[0] * u))
    o = np.argsort(np.abs(np.angle(ev)))
    etich = np.empty(12, dtype=object)
    i0 = 0
    for nome, quanti in GRUPPI_IS:
        etich[o[i0:i0 + quanti]] = nome
        i0 += quanti
    prev = ev.copy()
    out = {}
    passi = [kk[0]]
    for a, b in zip(kk[:-1], kk[1:]):
        m = max(1, int(math.ceil((b - a) / PASSO_SEGUI)))
        passi += [a + (b - a) * (j + 1) / m for j in range(m)]
    salto = 0.0
    for kap in passi:
        ev, V = np.linalg.eig(T(kap * u))
        D = np.abs(prev[:, None] - ev[None, :])
        r_, c_ = linear_sum_assignment(D)
        salto = max(salto, float(D[r_, c_].max()))
        nuovo = np.empty(12, dtype=object)
        nuovo[c_] = etich[r_]
        etich, prev = nuovo, ev
        if any(abs(kap - x) < 1e-12 for x in kk):
            gr = {}
            for nome, _q in GRUPPI_IS:
                sel = np.flatnonzero(etich == nome)
                Q, _r = np.linalg.qr(V[:, sel])
                altri = np.flatnonzero(etich != nome)
                gap = float(np.min(np.abs(ev[sel][:, None] - ev[altri][None, :])))
                gr[nome] = (np.angle(ev[sel]), Q, gap, len(sel))
            out[min(kk, key=lambda x: abs(x - kap))] = gr
    return out, salto


def _pendenza(x, y):
    x, y = np.asarray(x), np.asarray(y)
    ok = y > 0
    return float(np.polyfit(np.log(x[ok]), np.log(y[ok]), 1)[0]) if ok.sum() >= 2 else float("nan")


def brezzi():
    """### **IS1, la visibilita'** *(Luca `2026-11-06 19:41`; il task history `2026-11-06_brezzi_modi_vuoto`, sez. `2.1`-`2.3`)*."""
    import _screening_forme_s3 as SF
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import corsa_accensione as CA
    _sol, _v, s = V.CORSE[CA.NOME]
    K = int(round(CA.CORSE["TF3"][0] / s))
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        omega = float(d["omega"])
    _rec, z, p0, F3, _info, cm = costruisci(V.N, V.L)
    dove = _cella(z)
    pav = PAV_T / AMP
    print("### IS1, LA VISIBILITA' (Luca 19:41): per ogni ramo del vuoto F3 e |k| %s lungo A1 e a 30 gradi, (a) |Pi J f| / |J f| (un delta rho eccita il ramo), (b) |Pi f| / |f| (il ramo cambia Lambda);"
          " f = F3 sul nodo 0; il pavimento %.1e / gap; s %g, AMP %g" % (KAPPA_IS, pav, s, AMP))
    T, _R = _T_vuoto(z, F3, K, np.exp(-1j * omega), dove, lambda z_: AC.tick(z_, K + 1, K))
    f = _reali(F3[dove[0]])
    Jf = _reali(1j * F3[dove[0]])
    print("  |F3_h| sul nodo 0: %s; Lambda %.15f" % (" ".join("%.15f" % x for x in np.abs(F3[dove[0]])), float(np.sum(np.abs(F3[dove[0]]) ** 2))))
    # IS1-N
    eN = 0.0
    for _nd, gradi in DIREZIONI_G:
        u = np.array([math.cos(math.radians(gradi)), math.sin(math.radians(gradi))])
        for kap in (0.0,) + KAPPA_IS:
            Tk = T(kap * u)
            eN = max(eN, float(np.max(np.abs(Tk.conj().T @ Tk - np.eye(12)))))
    esito("DEVE PASSARE: IS1-N T(k) unitaria (|T^H T - I| entro %g) a Gamma e a ogni |k| della griglia, nelle due direzioni: il proiettore ortogonale e' lo spettrale" % TOLL_N, eN <= TOLL_N, "%.3e" % eN)
    # IS1-C, IS1-C-F: il canale
    import _deriva_congelato as DC
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}

    def psi_dopo(phi):
        try:
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                for k_, v in salvato.items():
                    z["st"][k_][...] = v
                z["st"]["psi_h"][...] = p0
                z["st"]["phi_h"][...] = phi
                AC.tick(z, K + 1, K)
                return z["st"]["psi_h"].copy()
        finally:
            for k_, v in salvato.items():
                z["st"][k_][...] = v
    q0 = psi_dopo(F3)
    eC = float(np.linalg.norm(psi_dopo(F3 * np.exp(1j * AMP)) - q0) / np.linalg.norm(q0)) / AMP
    eCF = float(np.linalg.norm(psi_dopo(F3 * (1.0 + AMP)) - q0) / np.linalg.norm(q0)) / AMP
    esito("DEVE PASSARE: IS1-C il tick intero con psi = la partenza di TF3 e phi = F3 e^{i AMP} (non tocca Lambda): psi' = quello con phi = F3, lo scarto / AMP entro %.1e" % pav, eC <= pav, "%.3e" % eC)
    esito("DEVE FALLIRE: IS1-C-F lo stesso con phi = (1 + AMP) F3 (tocca Lambda): lo scarto / AMP entro %.1e" % pav, not eCF <= pav, "%.3e" % eCF)
    # IS1-0, IS1-L-F, IS1-R
    eps = np.array([1.0, -1.0, 1.0, -1.0, 1.0, -1.0])
    w = np.abs(F3[dove[0]]) ** 2
    eps = eps - np.sum(eps * w) / np.sum(w)
    u_m = _reali(1j * eps * F3[dove[0]])
    qm = (u_m / np.linalg.norm(u_m))[:, None].astype(complex)
    a_m, b_m = _coseno(qm, Jf), _coseno(qm, f)
    esito("DEVE PASSARE: IS1-0 il modo costruito u = J(eps f), somma eps |F3|^2 = 0 (non tocca ne' Lambda ne' la fase): a e b entro %g" % TOLL_MUTO, max(a_m, b_m) <= TOLL_MUTO, "a %.3e b %.3e" % (a_m, b_m))
    v_l = np.zeros(12)
    v_l[0:2] = f[0:2]
    b_l = _coseno((v_l / np.linalg.norm(v_l))[:, None].astype(complex), f)
    esito("DEVE FALLIRE: IS1-L-F Lambda locale (f su una sola estremita'): b entro %g" % TOLL_MUTO, not b_l <= TOLL_MUTO, "b %.6f" % b_l)
    qr_ = (Jf / np.linalg.norm(Jf))[:, None].astype(complex)
    print("  IS1-R la rotazione globale i F3 (la premessa 3, dichiarata): b %.3e, a %.15f" % (_coseno(qr_, f), _coseno(qr_, Jf)))
    # il fattore scalare (2.2): sui rho della partenza
    rho = np.zeros(z["inc"].n)
    np.add.at(rho, z["inc"].nodo, np.sum(np.abs(p0.reshape(2 * z["inc"].m, -1)) ** 2, axis=1))
    Lam = float(np.sum(np.abs(F3[dove[0]]) ** 2))
    rv = np.sort(rho[rho > 1e-6 * rho.max()])
    for nome_r, r_ in (("il massimo", float(rho.max())), ("la mediana sopra 1e-6 del massimo", float(np.median(rv)))):
        x = r_ / Lam
        h = 1e-6 * x
        da = (SF._ab("S1", x + h)[0] - SF._ab("S1", x - h)[0]) / (2 * h)
        db = (SF._ab("S1", x + h)[1] - SF._ab("S1", x - h)[1]) / (2 * h)
        print("  il fattore scalare (uguale per ogni ramo) a rho %s %.6e: x %.6e; d alpha / d Lambda %.6e, d beta / d rho %.6e (dalle espressioni di _screening_forme_s3._ab(S1), alle differenze centrali)"
              % (nome_r, r_, x, -da * x / Lam, db / Lam))
    # i rami
    for nome_d, gradi in DIREZIONI_G:
        u = np.array([math.cos(math.radians(gradi)), math.sin(math.radians(gradi))])
        gr, salto = _rami(T, u, KAPPA_IS)
        print("-" * 130)
        print("  %s: il seguimento per continuita' (passi di |k| %g): il salto piu' grande di un autovalore fra due passi %.3e" % (nome_d, PASSO_SEGUI, salto))
        for nome, quanti in GRUPPI_IS:
            aa, bb, pp = [], [], []
            for kap in KAPPA_IS:
                fasi, Q, gap, nq = gr[kap][nome]
                assert nq == quanti, (nome_d, nome, kap, nq)
                a_, b_ = _coseno(Q, Jf), _coseno(Q, f)
                aa.append(a_)
                bb.append(b_)
                pp.append(pav / gap)
                print("    %s %-2s |k| %.3f: |fase| per tick %s; a %.3e b %.3e (max |delta Lambda| / |v| = 2 |f| b %.3e); il gap %.3e, il pavimento %.3e"
                      % (nome_d, nome, kap, " ".join("%.3e" % abs(x) for x in np.sort(np.abs(fasi))), a_, b_, 2.0 * np.linalg.norm(f) * b_, gap, pav / gap))
            ia, ib = int(np.argmin(aa)), int(np.argmin(bb))
            sopra = [max(a_, b_) > p_ for a_, b_, p_ in zip(aa, bb, pp)]
            print("  ### %s %-2s inf a %.3e (|k| %.3f), sup a %.3e; inf b %.3e (|k| %.3f), sup b %.3e; la pendenza in ln |k| sui primi 4: a %+.3f, b %+.3f"
                  % (nome_d, nome, aa[ia], KAPPA_IS[ia], max(aa), bb[ib], KAPPA_IS[ib], max(bb), _pendenza(KAPPA_IS[:4], aa[:4]), _pendenza(KAPPA_IS[:4], bb[:4])))
            print("  ### %s %-2s la lettura scritta prima (Luca): %s" % (nome_d, nome, "max(a, b) ENTRO il pavimento a ogni |k|: il ramo NON E' VISTO dalla materia (il segnale di un modo spurio)" if not any(sopra)
                  else "SOPRA il pavimento a %d |k| su %d: il ramo E' VISTO, partecipa alla dinamica" % (sum(sopra), len(sopra))))
            if nome == "G":
                print("  ### %s IS1-G il Goldstone a k -> 0 (Luca): a %s; b %s; le pendenze in ln |k| a %+.3f b %+.3f"
                      % (nome_d, " ".join("%.3e" % x for x in aa[:5]), " ".join("%.3e" % x for x in bb[:5]), _pendenza(KAPPA_IS[:4], aa[:4]), _pendenza(KAPPA_IS[:4], bb[:4])))
        # il Goldstone e gli zeri insieme (il gap verso P e' grande)
        for kap in KAPPA_IS[:5]:
            Qg, Qz = gr[kap]["G"][1], gr[kap]["Z"][1]
            Qgz, _r = np.linalg.qr(np.hstack([Qg, Qz]))
            print("    %s G+Z |k| %.3f: a %.6e b %.6e" % (nome_d, kap, _coseno(Qgz, Jf), _coseno(Qgz, f)))
    cm.__exit__(None, None, None)


def passo():
    """### **IS2, il passo di tempo** *(Luca `19:41`; il task history, sez. `2.4`)*: il vuoto `F3` da solo a `s` di `PASSI_S`, `mot.cs` in memoria e rimesso *(l'annotazione `4.1`)*."""
    import re
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import corsa_accensione as CA
    _sol, _v, s0 = V.CORSE[CA.NOME]
    K = int(round(CA.CORSE["TF3"][0] / s0))
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        omega_npz = float(d["omega"])
    _rec, z, _p0, F3, _info, cm = costruisci(V.N, V.L)
    dove = _cella(z)
    cs_vero = z["mot"].cs.copy()
    assert np.all(cs_vero == s0), "la scena deve avere cs uniforme = s della corsa"
    salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
    pav = PAV_T / AMP
    f_v = os.path.join(DIR_REF, "statica_vuoto.txt")
    f_g = os.path.join(DIR_REF, "statica_goldstone.txt")
    rif_fasi = rif_b = None
    for l in open(f_v, encoding="utf-8"):
        m = re.match(r"\s*oggi\s+a Gamma le 12 fasi per tick: (.*?); i moduli", l)
        if m:
            rif_fasi = m.group(1).split()
    for l in open(f_g, encoding="utf-8"):
        m = re.match(r"\s*### A1\s+la omega piu' grande .* b ([+-][0-9.e+-]+);", l)
        if m:
            rif_b = m.group(1)
    print("### IS2, IL PASSO DI TEMPO (Luca 19:41): il vuoto F3 da solo, psi = 0, a s %s (mot.cs in memoria, rimesso); omega(s) misurato da un tick; T(k) nel riferimento che gira con omega(s)" % (PASSI_S,))
    print("  i riferimenti letti dai referti: le 12 fasi di statica_vuoto.txt %s; b del Goldstone lungo A1 di statica_goldstone.txt %s" % (rif_fasi, rif_b))
    tab = {}
    try:
        for s in PASSI_S:
            z["mot"].cs[...] = s
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                for k_, v in salvato.items():
                    z["st"][k_][...] = v
                z["st"]["psi_h"][...] = 0.0
                z["st"]["phi_h"][...] = F3
                AC.tick(z, K + 1, K)
                ph = z["st"]["phi_h"].copy()
            lam = complex(np.vdot(F3, ph) / np.vdot(F3, F3))
            om = -math.atan2(lam.imag, lam.real)
            res = float(np.linalg.norm(ph - np.exp(-1j * om) * F3) / np.linalg.norm(F3))
            esito("DEVE PASSARE: IS2-E a s %.2f F3 e' un autovettore del tick: |tick F3 - e^{-i omega} F3| / |F3| entro %g" % (s, TOLL_E2), res <= TOLL_E2, "omega %.17e per tick (pi s %.17e), |lambda| %.15f, il residuo %.3e" % (om, math.pi * s, abs(lam), res))
            T, _R = _T_vuoto(z, F3, K, np.exp(-1j * om), dove, lambda z_: AC.tick(z_, K + 1, K))
            ev0 = np.linalg.eigvals(T(np.zeros(2)))
            fasi0 = np.sort(np.angle(ev0))
            Pk, Dk = [], []
            gr, _salto = _rami(T, np.array([1.0, 0.0]), KAPPA_IS)
            for kap in KAPPA_IS:
                Pk.append(float(np.mean(np.abs(gr[kap]["P"][0]))))
                Dk.append(float(np.mean(np.abs(gr[kap]["D"][0]))))
            wmax = []
            for kap in KAPPA_G:
                fs = np.sort(np.abs(np.angle(np.linalg.eigvals(T(np.array([kap, 0.0]))))))
                wmax.append(float(fs[N_GOLD - 1]) / s)
            cf = np.polyfit(np.array(KAPPA_G), np.array(wmax), 2)
            tab[s] = {"om": om, "fasi0": fasi0, "P": Pk, "D": Dk, "b": float(cf[0]), "v": float(cf[1]), "c0": float(cf[2])}
            print("  s %.2f: le 12 fasi per tick a Gamma %s" % (s, " ".join("%+.6e" % x for x in fasi0)))
            print("  s %.2f: il ramo piatto P lungo A1, |fase| per tick da %.9e a %.9e, per unita' di tempo da %.9e a %.9e; theta = pi s %.9e per tick"
                  % (s, min(Pk), max(Pk), min(Pk) / s, max(Pk) / s, math.pi * s))
            print("  s %.2f: il ramo D lungo A1, |fase| per tick da %.9e a %.9e, per unita' di tempo da %.9e a %.9e" % (s, min(Dk), max(Dk), min(Dk) / s, max(Dk) / s))
            print("  s %.2f: il Goldstone lungo A1 (in unita' di tempo), la omega piu' grande delle %d: %s; il fit c0 %+.3e v %+.6e b %+.6e"
                  % (s, N_GOLD, " ".join("%.3e" % x for x in wmax), cf[2], cf[1], cf[0]))
    finally:
        z["mot"].cs[...] = cs_vero
        for k_, v in salvato.items():
            z["st"][k_][...] = v
    t15 = tab[0.15]
    esito("DEVE PASSARE: IS2-15 a s 0.15 omega misurato = quello di fase_F3.npz entro %g" % TOLL_W15, abs(t15["om"] - omega_npz) <= TOLL_W15, "%.3e" % abs(t15["om"] - omega_npz))
    e15 = float(np.max(np.abs(t15["fasi0"] - np.array([float(x) for x in rif_fasi])))) if rif_fasi is not None and len(rif_fasi) == 12 else float("inf")
    esito("DEVE PASSARE: IS2-15 a s 0.15 le 12 fasi a Gamma = la riga oggi di statica_vuoto.txt al pavimento (%.1e per tick; l'annotazione 4.4)" % pav, e15 <= pav, "lo scarto massimo %.3e" % e15)
    pav_b = pav / 0.15 / KAPPA_G[-1] ** 2
    e_b = abs(t15["b"] - float(rif_b)) if rif_b is not None else float("inf")
    esito("DEVE PASSARE: IS2-15 a s 0.15 la b del Goldstone lungo A1 = statica_goldstone.txt al pavimento (%.1e = il pavimento in omega / |k|^2 piu' grande; 4.4)" % pav_b, e_b <= pav_b, "%+.6e, lo scarto %.3e" % (t15["b"], e_b))
    print("-" * 130)
    for nome in ("P", "D"):
        pt = {s: float(np.mean(tab[s][nome])) for s in PASSI_S}
        pu = {s: pt[s] / s for s in PASSI_S}
        dt = (max(pt.values()) - min(pt.values())) / max(pt.values())
        du = (max(pu.values()) - min(pu.values())) / max(pu.values())
        print("  ### il ramo %s (la media lungo A1): per tick %s (lo scarto relativo %.3e); per unita' di tempo %s (lo scarto relativo %.3e); omega(s) / s %s"
              % (nome, " ".join("%.9e" % pt[s] for s in PASSI_S), dt, " ".join("%.9e" % pu[s] for s in PASSI_S), du, " ".join("%.9e" % (tab[s]["om"] / s) for s in PASSI_S)))
        print("  ### il ramo %s, la lettura scritta prima (Luca; la tolleranza %g: l'annotazione 4.2): %s" % (nome, TOLL_SEGUE, "FISSO PER UNITA' DI TEMPO, segue omega(s): proprieta' del vuoto (la premessa 5: atteso per costruzione, theta = pi s)" if du <= TOLL_SEGUE
              else "FISSO PER TICK: artefatto del passo" if dt <= TOLL_SEGUE else "ne' l'uno ne' l'altro entro %g (dichiarato)" % TOLL_SEGUE))
    bs = {s: tab[s]["b"] for s in PASSI_S}
    db = (max(bs.values()) - min(bs.values())) / abs(bs[0.15])
    print("  ### il Goldstone: b in unita' di tempo %s; lo scarto relativo %.3e; la pendenza di ln b contro ln s %+.4f" % (" ".join("%+.6e" % bs[s] for s in PASSI_S), db, _pendenza(PASSI_S, [abs(bs[s]) for s in PASSI_S])))
    print("  ### il Goldstone, la lettura scritta prima (mia, proposta): %s" % ("la stessa b entro l'1%: proprieta' della legge" if db <= 0.01 else "b cambia col passo oltre l'1%: dipende dal passo"))
    cm.__exit__(None, None, None)


def cs_onde():
    """### **IS3, `cs` sulle onde del vuoto** *(Luca `2026-11-06 19:41-20:00`; il task history `2026-11-06_brezzi_modi_vuoto`, sez. `5.2`)*: `T_cs(k)` col tick `tick_con_cs`, `Lambda_c` dal vuoto, contro `T(k)`."""
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    import tick as TK
    from solitone import accensione as AC
    from solitone import corsa_accensione as CA
    _sol, _v, s = V.CORSE[CA.NOME]
    K = int(round(CA.CORSE["TF3"][0] / s))
    _rec, z, _p0, F3, _info, cm = costruisci(V.N, V.L)
    dove = _cella(z)
    pav = PAV_T / AMP
    mot = z["mot"]
    cs_vero, lc_vero = mot.cs.copy(), mot.lambda_c
    lam = np.bincount(z["inc"].nodo, weights=np.abs(F3) ** 2, minlength=z["inc"].n)
    assert float(np.max(lam) - np.min(lam)) <= 1e-12 * float(np.max(lam)), "Lambda del vuoto NON e' uniforme: Lambda_c non si ricava cosi'"
    lam0 = float(np.mean(lam))
    lc = lam0 * (1.0 - s) / s
    giri = []

    def tk(z_):
        AC.tick(z_, K + 1, K)

    def tk_cs(z_):
        try:
            giri.append(TK.tick_con_cs(z_["st"], z_["mot"], z_["par"], lc, ()))
        finally:
            z_["mot"].cs[...] = cs_vero
            z_["mot"].lambda_c = lc_vero
    salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}

    def un_tick(fai):
        try:
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                for k_, v in salvato.items():
                    z["st"][k_][...] = v
                z["st"]["psi_h"][...] = 0.0
                z["st"]["phi_h"][...] = F3
                fai(z)
                return z["st"]["phi_h"].copy()
        finally:
            for k_, v in salvato.items():
                z["st"][k_][...] = v
    print("### IS3, cs SULLE ONDE DEL VUOTO (Luca 19:41-20:00): il tick tick_con_cs (cs dinamico e CAMM-FASE-VUOTO insieme) contro il tick di oggi, linearizzati attorno a F3; Lambda del vuoto %.15f, s %g -> Lambda_c %.15f; nel vuoto cs %.17f"
          % (lam0, s, lc, lam0 / (lam0 + lc)))
    oms = {}
    phs = {}
    for nome, fai in (("oggi", tk), ("cs", tk_cs)):
        ph = un_tick(fai)
        lam_ = complex(np.vdot(F3, ph) / np.vdot(F3, F3))
        oms[nome] = -math.atan2(lam_.imag, lam_.real)
        phs[nome] = ph
        res = float(np.linalg.norm(ph - np.exp(-1j * oms[nome]) * F3) / np.linalg.norm(F3))
        if nome == "cs":
            esito("DEVE PASSARE: IS3-E F3 e' un autovettore del tick con cs: |tick F3 - e^{-i omega} F3| / |F3| entro %g" % TOLL_E2, res <= TOLL_E2, "omega_cs %.17e per tick, il residuo %.3e; i giri del punto fisso %s" % (oms[nome], res, giri[-1:]))
        else:
            print("  il tick di oggi: omega %.17e per tick, il residuo %.3e" % (oms[nome], res))
    print("  IS3-0 (stampato): |tick_cs F3 - tick F3| / |F3| %.3e; omega_cs - omega %+.3e" % (float(np.linalg.norm(phs["cs"] - phs["oggi"]) / np.linalg.norm(F3)), oms["cs"] - oms["oggi"]))
    T, _R = _T_vuoto(z, F3, K, np.exp(-1j * oms["oggi"]), dove, tk)
    del giri[:]
    Tc, _Rc = _T_vuoto(z, F3, K, np.exp(-1j * oms["cs"]), dove, tk_cs)
    print("  i giri del punto fisso nei 13 tick della risposta con cs: da %s a %s" % (min(giri), max(giri)))
    assert np.all(mot.cs == cs_vero) and mot.lambda_c == lc_vero, "mot.cs e mot.lambda_c rimessi"
    f = _reali(F3[dove[0]])
    Jf = _reali(1j * F3[dove[0]])
    T0, Tc0 = T(np.zeros(2)), Tc(np.zeros(2))
    eR = float(np.linalg.norm(Tc0 @ Jf - T0 @ Jf) / np.linalg.norm(Jf))
    eL = float(np.linalg.norm(Tc0 @ f - T0 @ f) / np.linalg.norm(f))
    esito("DEVE PASSARE: IS3-R la rotazione globale J f non vede cs: |T_cs(0) J f - T(0) J f| / |J f| entro %.1e" % pav, eR <= pav, "%.3e" % eR)
    esito("DEVE FALLIRE: IS3-L-F f (cambia Lambda, quindi cs): |T_cs(0) f - T(0) f| / |f| entro %.1e" % pav, not eL <= pav, "%.3e" % eL)
    print("  a Gamma le 12 fasi per tick, senza cs: %s" % " ".join("%+.6e" % x for x in np.sort(np.angle(np.linalg.eigvals(T0)))))
    print("  a Gamma le 12 fasi per tick, con cs:   %s" % " ".join("%+.6e" % x for x in np.sort(np.angle(np.linalg.eigvals(Tc0)))))
    for nome_d, gradi in DIREZIONI_G:
        u = np.array([math.cos(math.radians(gradi)), math.sin(math.radians(gradi))])
        gr, s0 = _rami(T, u, KAPPA_IS)
        grc, s1 = _rami(Tc, u, KAPPA_IS)
        print("-" * 130)
        print("  %s: il salto piu' grande del seguimento senza cs %.3e, con cs %.3e" % (nome_d, s0, s1))
        for nome, quanti in GRUPPI_IS:
            w0, w1 = [], []
            for kap in KAPPA_IS:
                assert gr[kap][nome][3] == quanti and grc[kap][nome][3] == quanti, (nome_d, nome, kap)
                w0.append(float(np.mean(np.abs(gr[kap][nome][0]))))
                w1.append(float(np.mean(np.abs(grc[kap][nome][0]))))
            print("    %s %-2s |fase| media per unita' di tempo, senza cs: %s" % (nome_d, nome, " ".join("%.6e" % (x / s) for x in w0)))
            print("    %s %-2s |fase| media per unita' di tempo, con cs:   %s" % (nome_d, nome, " ".join("%.6e" % (x / s) for x in w1)))
            print("    %s %-2s la differenza (con - senza) per tick: %s; il massimo %.3e" % (nome_d, nome, " ".join("%+.2e" % (b - a) for a, b in zip(w0, w1)), max(abs(b - a) for a, b in zip(w0, w1))))
            if nome == "P":
                p0_, p1_ = max(w0) - min(w0), max(w1) - min(w1)
                print("  ### %s P la pendenza (max - min della |fase| per tick lungo la griglia): senza cs %.3e, con cs %.3e; 10 x il pavimento %.1e" % (nome_d, p0_, p1_, 10 * pav))
                print("  ### %s P la lettura scritta prima (Luca): %s" % (nome_d, "il ramo piatto ACQUISTA PENDENZA con cs: cs lo cura" if (p1_ > 10 * pav and p0_ <= 10 * pav)
                      else "RESTA PIATTO con cs: no" if p1_ <= 10 * pav else "non piatto gia' senza cs (%.3e): la lettura non si applica (dichiarato)" % p0_))
        for nome_t, TT in (("senza cs", T), ("con cs", Tc)):
            wmax = []
            for kap in KAPPA_G:
                fs = np.sort(np.abs(np.angle(np.linalg.eigvals(TT(kap * u)))))
                wmax.append(float(fs[N_GOLD - 1]) / s)
            cf = np.polyfit(np.array(KAPPA_G), np.array(wmax), 2)
            print("  ### %s il Goldstone %-8s la omega piu' grande delle %d: %s; il fit c0 %+.3e v %+.6e b %+.6e" % (nome_d, nome_t, N_GOLD, " ".join("%.3e" % x for x in wmax), cf[2], cf[1], cf[0]))
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
    modo = "--cs-onde" if "--cs-onde" in argv else "--brezzi" if "--brezzi" in argv else "--passo" if "--passo" in argv else "--olonomia" if "--olonomia" in argv else "--vortici" if "--vortici" in argv else "--circolazione" if "--circolazione" in argv else "--goldstone" if "--goldstone" in argv else "--vuoto" if "--vuoto" in argv else "--coppia-matura" if "--coppia-matura" in argv else "--coppia" if "--coppia" in argv else "--dimensione" if "--dimensione" in argv else None
    assert modo, "uso: --cs-onde | --brezzi | --passo | --vuoto | --goldstone | --circolazione | --vortici | --olonomia | --coppia | --coppia-matura | --dimensione"
    print("=" * 130)
    print("LE CARTE STATICHE (Luca 2026-11-05 15:28, 15:42): %s; nessuna corsa; NN %s L_COPPIA %d DD %d .. %d; AMP %g TOLL_L %g TOLL_A %g TOLL_G %g TOLL_E %g GAP_ZERO %g"
          % (modo, NN, L_COPPIA, DD[0], DD[-1], AMP, TOLL_L, TOLL_A, TOLL_G, TOLL_E, GAP_ZERO))
    print("=" * 130)
    cs0()
    {"--cs-onde": cs_onde, "--brezzi": brezzi, "--passo": passo, "--vuoto": vuoto, "--goldstone": lambda: vuoto(goldstone=True), "--circolazione": circolazione, "--vortici": vortici, "--olonomia": olonomia, "--coppia": coppia, "--coppia-matura": coppia_matura, "--dimensione": dimensione}[modo]()
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
