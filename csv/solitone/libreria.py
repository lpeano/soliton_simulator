# -*- coding: utf-8 -*-
r"""**LA LIBRERIA DEI SOLITONI MATURI** *(Luca `2026-11-07` `00:32`; le decisioni delle `10:06`; l'avvio delle `16:01`-`16:04`, un processo separato; il task history
`doc/TASK_HISTORY/2026-11-07_libreria_solitoni_cluster.md`)*

    python csv/solitone/libreria.py > doc/referti_l2/libreria_solitoni.txt

### **Un solo processo, in ordine:** `LIB0` *(il ritaglio dello stato di `TBS` a `t 15000`, il tick `100000`, per `R_t` in `16 .. 40` a passi di `4`)*; **la scelta di `R_t`**
*(Luca `10:06`: il piu' piccolo con la massa fuori, l'energia fuori e i due salti sotto `1e-6`; se nessuno: FERMO)*; **la costruzione** *(sette oggetti dagli stati di `TBS`
ai tick `100000 .. 160000`, su `E:\soliton_simulator\libreria\`, l'indice `doc/referti_l2/libreria_solitoni/indice.json`)*; **`R2`** *(Luca `16:01`: salvato, riletto,
ripartito al bit; il DEVE FALLIRE senza il disturbo del vuoto)*; **`LIB1`** *(`LIB1-0` il ciclo della corsa ridà gli `sha` di `dopo_stato`; `LIB1-1`, `LIB1-C`, `LIB1-F`, `LIB1-U`,
`LIB1-U-F`, `LIB1-P`)*; **`LIB2`** *(il transitorio, `1000` unita' di tempo, la materia assorbita per blocchi contro `TBS`)*.
### **L'oggetto si conserva nel riferimento della corsa d'origine** *(gli array interi, zero fuori da `R_t`, col centro)*: **per incollarlo altrove si trasla con `roll`
di `(L, L, -1, ...)`** *(esatto)*. **Dichiarato:** il task history (2.1) diceva «in coordinate relative»; questa e' la forma piu' semplice ed esatta.
"""
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

CORSA = "TBS"
T_LIB0 = 100000                                   # ### t 15000 (il task history 2.2)
TICK_LIB = tuple(range(100000, 160001, 10000))    # ### t 15000 .. 24000: sette (2.1)
GRIGLIA = (16, 20, 24, 28, 32, 36, 40)            # ### Luca 10:06
SOGLIA = 1e-6                                     # ### Luca 10:06
FATTORE_1 = 1.0 + 1e-2                            # ### LIB1-1, Luca 10:06
TOLL_C = 0.2                                      # ### LIB1-C (Luca 00:32): nodi
N_LIB1 = 2000                                     # ### 2.3
DOPO = 100                                        # ### corsa_accensione.DOPO_STATO: LIB1-0
SFASA = 7                                         # ### LIB1-F: il vuoto c(T0 + 7) F3 (2.3, mia)
N_LIB2 = 6667                                     # ### 2.4: 1000 unita' di tempo
BLOCCO2 = 100.0                                   # ### 2.4: unita' di tempo
N_R2 = 100                                        # ### R2: i tick dopo la rilettura (mio)
TOLL_U = 1e-12                                    # ### LIB1-U (2.3)
DIR_E = os.path.join("E:" + os.sep, "soliton_simulator", "libreria")
DIR_REPO = os.path.join(solitone.RADICE, "doc", "referti_l2", "libreria_solitoni")
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-118s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))


def sha1_file(f):
    import hashlib
    return hashlib.sha1(open(f, "rb").read()).hexdigest()


def main():
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _libro_dei_conti as LCO
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import bordo as BO
    from solitone import campo as CP
    from solitone import corsa_accensione as CA
    from solitone import protetto as P
    from solitone import toro as TO
    for m in ("__init__", "toro", "campo", "bordo", "accensione", "corsa_accensione", "protetto"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    rr = CA.serie(CORSA)[0]
    camp = [c for r in rr for c in r["campioni"]]
    stati = {x["t"]: x for r in rr for x in (r.get("stati") or [])}
    dopo = {}
    for r in rr:
        dopo.update(r.get("dopo_stato") or {})
    bor = rr[0]["bordo"]
    e_K = rr[0]["e_K"]
    K = int(round(CA.CORSE[CORSA][0] / s))
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab_c, omega = d["c"].copy(), float(d["omega"])
    print("=" * 130)
    print("LA LIBRERIA DEI SOLITONI MATURI (Luca 00:32, 10:06, 16:01): dagli stati di %s; R_t %s, la soglia %g, LIB1-1 x %g, LIB1-C %g nodi; il bordo c0 %s R_A %g g_max %g; K %d"
          % (CORSA, list(GRIGLIA), SOGLIA, FATTORE_1, TOLL_C, bor["c0"], bor["R_A"], bor["g_max"], K))
    print("=" * 130)
    with CA.con_L(CA.LCORSA.get(CORSA)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        P.e_K(z)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        phi_v = CA.vuoto_della_corsa(z, CORSA)
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, inc, mot, par, L = z["st"], z["inc"], z["mot"], z["par"], int(z["L"])
        nodo = np.asarray(inc.nodo)
        n = inc.n
        v_ = np.arange(n)
        m1, m2 = v_ // L, v_ % L
        g_e, gn, _r = BO.g_estremita(z, bor["c0"][0], bor["c0"][1], bor["R_A"], bor["g_max"])
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))

        def carica(t):
            x = stati[t]
            with np.load(x["file"]) as d:
                assert int(d["t"]) == t
                for k in chiavi:
                    st[k][...] = d[k]
            return V.shas(z) == x["sha"]

        def rif(t):
            return BO.c_di(t, tab_c, K, omega) * phi_v

        def ciclo(t):
            """### Un tick della corsa: `AC.tick`, poi il bordo con `c(t) F3` *(le righe di `corsa_accensione`)*."""
            AC.tick(z, t, K)
            BO.assorbi(st, g_e, rif(t))

        def rho_n():
            r = np.zeros(n)
            np.add.at(r, nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
            return r

        def centro():
            return np.array(TO.centro(rho_n(), m1, m2, L)[:2])

        def dist(cA, cB):
            A1, A2 = TO.vettori()
            q = ((cB - cA + 0.5 * L) % L) - 0.5 * L
            return float(np.hypot(*(q[0] * A1 + q[1] * A2)))

        def energia():
            return math.fsum(LCO.conti_per_nodo(inc, mot, st, e_K, V.LAM_ZERO, par)["tot"].tolist())

        def ritaglio(t, R):
            """### `(psi_t, D_t, centro, r per nodo)`: dentro `R` dal centro periodico dello stato, zero fuori; `D = phi - c(t) F3`."""
            c = centro()
            _k, r = CP.anelli(m1, m2, c[0], c[1], L, float("inf"))
            dentro = (r < R)[nodo]
            psi_t = st["psi_h"] * dentro[:, None]
            D = st["phi_h"] - rif(t)
            return psi_t, D * dentro, D, c, r

        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            # ---------------------------------------------------------- LIB0
            esito("DEVE PASSARE: L0-S lo stato di %s al tick %d ha gli sha del jsonl" % (CORSA, T_LIB0), carica(T_LIB0), stati[T_LIB0]["file"])
            psi0, phi0s = st["psi_h"].copy(), st["phi_h"].copy()
            M = float(np.sum(np.abs(psi0) ** 2))
            E_int = energia()
            print("### LIB0: il ritaglio dello stato al tick %d (t %g): M %.10e, E %.10e" % (T_LIB0, T_LIB0 * s, M, E_int))
            print("  %-5s %-12s %-12s %-12s %-12s %-12s %-12s" % ("R_t", "M fuori/M", "E fuori", "salto psi", "salto D", "|psi-psi_t|", "|D-D_t|"))
            scelto, tabella = None, {}
            for R in GRIGLIA:
                st["psi_h"][...], st["phi_h"][...] = psi0, phi0s
                psi_t, D_t, D, c, r = ritaglio(T_LIB0, R)
                anello = ((r >= R - 1) & (r < R))[nodo]
                Mf = 1.0 - float(np.sum(np.abs(psi_t) ** 2)) / M
                sp = float(np.max(np.abs(psi_t[anello]))) / float(np.max(np.abs(psi0)))
                sd = float(np.max(np.abs(D_t[anello]))) / float(np.max(np.abs(D)))
                npsi = float(np.linalg.norm(psi0 - psi_t) / np.linalg.norm(psi0))
                nD = float(np.linalg.norm(D - D_t) / np.linalg.norm(D))
                st["psi_h"][...], st["phi_h"][...] = psi_t, rif(T_LIB0) + D_t
                Ef = 1.0 - energia() / E_int
                tabella[R] = {"M_fuori": Mf, "E_fuori": Ef, "salto_psi": sp, "salto_D": sd, "pezzo_psi": npsi, "pezzo_D": nD}
                print("  %-5d %.6e %+.6e %.6e %.6e %.6e %.6e" % (R, Mf, Ef, sp, sd, npsi, nD))
                if scelto is None and max(abs(Mf), abs(Ef), sp, sd) < SOGLIA:
                    scelto = R
            if scelto is None:
                print("### NESSUN R_t della griglia passa il criterio (la massa fuori, l'energia fuori e i due salti sotto %g): FERMO (Luca 10:06: lo si dice, non lo si nasconde)" % SOGLIA)
                print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
                return 2
            print("### R_t scelto col criterio di Luca (10:06): %d" % scelto)
            # ---------------------------------------------------------- la costruzione e l'indice
            os.makedirs(DIR_E, exist_ok=True)
            os.makedirs(DIR_REPO, exist_ok=True)
            indice = {"corsa": CORSA, "R_t": scelto, "criterio": "il piu' piccolo R_t con M fuori, E fuori, salti sotto %g (Luca 10:06)" % SOGLIA, "lib0": {str(k): v for k, v in tabella.items()},
                      "bordo_origine": bor, "oggetti": []}
            print("### LA COSTRUZIONE: %d oggetti a R_t %d su %s" % (len(TICK_LIB), scelto, DIR_E))
            for t in TICK_LIB:
                assert carica(t), "lo stato al tick %d NON ha gli sha del jsonl" % t
                psi_t, D_t, _D, c, _r = ritaglio(t, scelto)
                f = os.path.join(DIR_E, "%s_%06d_R%02d.npz" % (CORSA, t, scelto))
                np.savez(f + ".tmp.npz", psi_h=psi_t, D=D_t, centro=c, t=t, R_t=scelto, L=L, c_t=np.array(BO.c_di(t, tab_c, K, omega)))
                os.replace(f + ".tmp.npz", f)
                Mo = float(np.sum(np.abs(psi_t) ** 2))
                cc = [x for x in camp if x["t"] == t]
                ogg = {"file": f, "byte": os.path.getsize(f), "sha1": sha1_file(f), "tick": t, "t": t * s, "sha_stato": stati[t]["sha"], "centro": [float(c[0]), float(c[1])],
                       "M": Mo, "w": cc[0]["per"]["w"] if cc else None, "cuore": cc[0]["f_liscia"] if cc else None, "c_t": [float(np.real(BO.c_di(t, tab_c, K, omega))), float(np.imag(BO.c_di(t, tab_c, K, omega)))],
                       "sha_psi": SFM.sha(psi_t), "sha_D": SFM.sha(D_t)}
                indice["oggetti"].append(ogg)
                print("  tick %6d (t %g): %s, %d byte, sha1 %s; centro (%.4f, %.4f), M %.6e, w %s, il cuore %s" % (t, t * s, os.path.basename(f), ogg["byte"], ogg["sha1"][:12], c[0], c[1], Mo, ogg["w"], ogg["cuore"]))
            fi = os.path.join(DIR_REPO, "indice.json")
            with open(fi, "w", encoding="utf-8", newline="\n") as h:
                json.dump(indice, h, ensure_ascii=False, indent=1)
            # ---------------------------------------------------------- R2
            o = indice["oggetti"][0]
            T0 = o["tick"]

            def incolla(f_obj, t_vuoto, senza_D=False):
                """### L'oggetto nel vuoto `c(t_vuoto) F3`; ### **le altre chiavi dello stato** *(`Lambda`, `rho`, `h_int`, `psi`)* **dallo stato d'origine** *(dichiarato)*."""
                assert carica(T0)
                with np.load(f_obj) as d:
                    st["psi_h"][...] = d["psi_h"]
                    st["phi_h"][...] = rif(t_vuoto) + (0.0 if senza_D else d["D"])
            assert sha1_file(o["file"]) == o["sha1"]
            incolla(o["file"], T0)
            for t in range(T0 + 1, T0 + N_R2 + 1):
                ciclo(t)
            sha_a = V.shas(z)
            incolla(o["file"], T0)
            for t in range(T0 + 1, T0 + N_R2 + 1):
                ciclo(t)
            sha_b = V.shas(z)
            incolla(o["file"], T0, senza_D=True)
            for t in range(T0 + 1, T0 + N_R2 + 1):
                ciclo(t)
            sha_f = V.shas(z)
            esito("DEVE PASSARE: R2 l'oggetto riletto dal file (sha1 = l'indice) e ripartito due volte per %d tick: gli sha di ogni chiave coincidono al bit" % N_R2, sha_a == sha_b, "%d chiavi" % len(sha_a))
            esito("DEVE FALLIRE: R2-F lo stesso SENZA il disturbo del vuoto D: gli sha coincidono", not (sha_f == sha_a), "")
            # ---------------------------------------------------------- LIB1-P, LIB1-U, LIB1-0
            fasi = [complex(BO.c_di(t, tab_c, K, omega)) for t in TICK_LIB]
            dfa = max(abs(math.remainder(math.atan2(f.imag, f.real) - math.atan2(fasi[0].imag, fasi[0].real), 2 * math.pi)) for f in fasi)
            lim_p = abs(omega - 3.0 * math.pi / 20.0) * (TICK_LIB[-1] - TICK_LIB[0]) + 1e-14
            print("### LIB1: c(t) ai tick %s: le fasi %s" % (list(TICK_LIB), " ".join("%+.12f" % math.atan2(f.imag, f.real) for f in fasi)))
            esito("DEVE PASSARE: LIB1-P tutti gli stati della libreria alla stessa fase di c(t) entro |omega - 3 pi/20| x (t_max - t_min) = %.3e" % lim_p, dfa <= lim_p, "%.3e" % dfa)
            assert carica(T0)
            st0 = {k: st[k].copy() for k in chiavi}
            a = 0.7
            ciclo(T0 + 1)
            dopo_a = {k: st[k].copy() for k in ("psi_h", "phi_h")}
            for k in chiavi:
                st[k][...] = st0[k]
            st["psi_h"] *= np.exp(1j * a)
            st["phi_h"] *= np.exp(1j * a)
            AC.tick(z, T0 + 1, K)
            BO.assorbi(st, g_e, rif(T0 + 1) * np.exp(1j * a))
            eU = max(float(np.max(np.abs(st[k] - dopo_a[k] * np.exp(1j * a)))) / float(np.max(np.abs(dopo_a[k]))) for k in ("psi_h", "phi_h"))
            for k in chiavi:
                st[k][...] = st0[k]
            st["psi_h"] *= np.exp(1j * a)
            AC.tick(z, T0 + 1, K)
            BO.assorbi(st, g_e, rif(T0 + 1))
            eUF = max(float(np.max(np.abs(st[k] - dopo_a[k] * np.exp(1j * a)))) / float(np.max(np.abs(dopo_a[k]))) for k in ("psi_h", "phi_h"))
            esito("DEVE PASSARE: LIB1-U la fase globale e^{i 0.7} su psi e phi (e sul vuoto di riferimento) commuta con un tick entro %g" % TOLL_U, eU <= TOLL_U, "%.3e" % eU)
            esito("DEVE FALLIRE: LIB1-U-F la fase solo su psi: entro %g" % TOLL_U, not (eUF <= TOLL_U), "%.3e" % eUF)
            for k in chiavi:
                st[k][...] = st0[k]
            for t in range(T0 + 1, T0 + DOPO + 1):
                ciclo(t)
            esito("DEVE PASSARE: LIB1-0 il ciclo della corsa (AC.tick e il bordo) dallo stato al tick %d per %d tick ridà gli sha di dopo_stato al bit" % (T0, DOPO), V.shas(z) == dopo[str(T0)], "")
            # ---------------------------------------------------------- LIB1: l'originale e l'incollato
            for k in chiavi:
                st[k][...] = st0[k]
            orig_c, orig_psi1 = [], None
            for j, t in enumerate(range(T0 + 1, T0 + N_LIB1 + 1)):
                ciclo(t)
                if j == 0:
                    orig_psi1 = st["psi_h"].copy()
                if j % 10 == 9:
                    orig_c.append(centro())
            M_orig = float(np.sum(np.abs(st["psi_h"]) ** 2))
            pezzo = tabella[scelto]["pezzo_psi"]
            incolla(o["file"], T0 + SFASA)
            ciclo(T0 + 1)
            eF = float(np.linalg.norm(st["psi_h"] - orig_psi1) / np.linalg.norm(orig_psi1))
            incolla(o["file"], T0)
            dc, ass_inc = [], []
            M_in0 = float(np.sum(np.abs(st["psi_h"]) ** 2))
            e1 = None
            for j, t in enumerate(range(T0 + 1, T0 + N_LIB2 + 1)):
                AC.tick(z, t, K)
                dM, _dV = BO.assorbi(st, g_e, rif(t))
                ass_inc.append(dM)
                if j == 0:
                    e1 = float(np.linalg.norm(st["psi_h"] - orig_psi1) / np.linalg.norm(orig_psi1))
                if j < N_LIB1 and j % 10 == 9:
                    dc.append(dist(centro(), orig_c[j // 10]))
            esito("DEVE PASSARE: LIB1-1 lo scarto relativo di psi al tick 1 entro il pezzo tolto di LIB0 (%.3e) x %g" % (pezzo, FATTORE_1), e1 <= pezzo * FATTORE_1, "%.3e" % e1)
            esito("DEVE PASSARE: LIB1-C la distanza dei centri incollato / originale entro %g nodi per %d tick (ogni 10)" % (TOLL_C, N_LIB1), max(dc) <= TOLL_C, "il massimo %.4f" % max(dc))
            esito("DEVE FALLIRE: LIB1-F nel vuoto c(T0 + %d) F3 lo scarto di psi al tick 1 entro lo stesso limite" % SFASA, not (eF <= pezzo * FATTORE_1), "%.3e" % eF)
            print("  l'originale dopo %d tick: M %.10e; l'incollato all'inizio M %.10e" % (N_LIB1, M_orig, M_in0))
            # ---------------------------------------------------------- LIB2
            cT = {x["t"]: x["bordo"]["M_ass"] for x in camp if "bordo" in x}
            print("### LIB2: la materia assorbita per blocchi di %g unita' di tempo dopo l'incollo, contro %s agli stessi tick (dai campioni); nessun verdetto" % (BLOCCO2, CORSA))
            nb = int(round(BLOCCO2 / s))
            for b in range(0, N_LIB2 // nb):
                ta, tb = T0 + b * nb, T0 + (b + 1) * nb
                inc_b = float(np.sum(ass_inc[b * nb:(b + 1) * nb]))
                ka = min(cT, key=lambda q: abs(q - ta))
                kb = min(cT, key=lambda q: abs(q - tb))
                tbs_b = cT[kb] - cT[ka]
                print("  t %8.1f .. %8.1f: l'incollato %.6e, %s %.6e (tick %d .. %d), la differenza %+.6e" % (ta * s, tb * s, inc_b, CORSA, tbs_b, ka, kb, inc_b - tbs_b))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
