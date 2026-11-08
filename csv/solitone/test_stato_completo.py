# -*- coding: utf-8 -*-
r"""**I1 (i2): LE PROVE DEL REGISTRO DELLO STATO COMPLETO SU UNA CORSA CORTA** *(il task history `doc/TASK_HISTORY/2026-11-07_stato_completo.md`, sez. `5`)*.

    python csv/solitone/test_stato_completo.py > doc/referti_l2/stato_completo.txt

### **La corsa corta:** la scena di `TBS` dallo stato completo `TBS_100000_completo.npz`, `N 100` tick col ciclo della corsa *(`AC.tick`, poi `BO.assorbi` con `c(t) F3`)*
**e gli accumulatori del bordo aggiornati come li aggiorna la corsa** *(`M_ass`, `V_ass`, `E_ass`)*; il salvataggio a meta'.
### **I DEVE:** `R1` *(il salvataggio non tocca la corsa)*, `R2` *(sporcato, ricaricato, `50` tick: AL BIT)*, `R2-F` *(a: senza `phi_h`; b: senza gli accumulatori)*, `R3` *(i registrati
nel file; uno in piu', uno in meno, una tabella cambiata: ALZA)*.
"""
import os
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

CORSA = "TBS"
TICK0 = 100000
N_SC = 100                     # ### mio, dichiarato (= DOPO_STATO)
META_SC = 50                   # ### il salvataggio a meta' (mio, dichiarato)
FILE_LIB = os.path.join("E:" + os.sep, "soliton_simulator", "libreria", "TBS_%06d_completo.npz" % TICK0)
DIR_PROVA = os.path.join("E:" + os.sep, "soliton_simulator", "stati_prova")
ACC = ("M_ass", "V_ass", "E_ass")

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-118s %s   %s" % (che[:118], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def alza(fai):
    """`(alzato, messaggio)`."""
    try:
        fai()
    except AssertionError as e:
        return True, str(e)[:160]
    return False, ""


def main():
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _libro_dei_conti as LC
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import bordo as BO
    from solitone import corsa_accensione as CA
    from solitone import protetto as P
    from solitone import stato_completo as SC
    for m in ("__init__", "bordo", "accensione", "corsa_accensione", "protetto", "stato_completo"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    commit = subprocess.check_output(["git", "rev-parse", "--short=8", "HEAD"], cwd=solitone.RADICE).decode().strip()
    sol, vuoto, s = V.CORSE[CA.NOME]
    rr = CA.serie(CORSA)[0]
    stati = {x["t"]: x for r in rr for x in (r.get("stati") or [])}
    bor0 = rr[0]["bordo"]
    K = int(round(CA.CORSE[CORSA][0] / s))
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab_c, omega = d["c"].copy(), float(d["omega"])
    os.makedirs(DIR_PROVA, exist_ok=True)
    print("=" * 130)
    print("I1 (i2), IL REGISTRO DELLO STATO COMPLETO (Luca 03:47): %s da %s, N %d tick, il salvataggio dopo %d; i file in %s; HEAD %s" % (CORSA, FILE_LIB, N_SC, META_SC, DIR_PROVA, commit))
    print("=" * 130)
    with CA.con_L(CA.LCORSA.get(CORSA)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        e_K = P.e_K(z)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        phi_v = CA.vuoto_della_corsa(z, CORSA)
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, inc, mot, par = z["st"], z["inc"], z["mot"], z["par"]
        g_e, _gn, _r = BO.g_estremita(z, bor0["c0"][0], bor0["c0"][1], bor0["R_A"], bor0["g_max"])
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        bor = {}

        def carica_lib():
            with np.load(FILE_LIB) as d:
                assert int(d["t"]) == TICK0
                for k in chiavi:
                    st[k][...] = d[k]
            bor.update({k: 0.0 for k in ACC})

        def ciclo(t):
            """### Il ciclo della corsa *(le righe di `corsa_accensione.corsa`)*: il tick, poi il bordo e gli accumulatori col libro dei conti prima e dopo."""
            AC.tick(z, t, K)
            e_pr = float(np.sum(LC.conti_per_nodo(inc, mot, st, e_K, V.LAM_ZERO, par)["tot"]))
            dM, dV = BO.assorbi(st, g_e, BO.c_di(t, tab_c, K, omega) * phi_v)
            bor["M_ass"] += dM
            bor["V_ass"] += dV
            bor["E_ass"] += e_pr - float(np.sum(LC.conti_per_nodo(inc, mot, st, e_K, V.LAM_ZERO, par)["tot"]))

        def corri(da, a):
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                for t in range(da + 1, a + 1):
                    ciclo(t)

        def impronta():
            return V.shas(z), {k: bor[k] for k in ACC}

        def registro(senza_phi=False, senza_acc=False, in_piu=False):
            R = SC.Registro()
            R.registra("st", *SC.di_z(z, ("phi_h",) if senza_phi else ()))
            if not senza_acc:
                R.registra("bordo", *SC.di_dict(bor, ACC))
            if in_piu:
                R.registra("campo_finto", lambda: {"A": np.zeros(3)}, lambda d: None)
            R.tabella("c_t", tab_c)
            return R

        def sporca():
            """### Lo stato VECCHIO della libreria a `TICK0` e gli accumulatori a zero: valido, ma non quello da cui ripartire *(una chiave dimenticata resterebbe COSI')*."""
            carica_lib()

        def meta(t):
            return {"corsa": CORSA, "tick": t, "t": t * s, "commit": commit}
        # ------------------------------------------------------------------ la corsa mai interrotta, senza salvataggio
        carica_lib()
        esito("DEVE PASSARE: R0 lo stato della libreria = lo stato di TBS registrato a %d (al bit, ogni chiave)" % TICK0, V.shas(z) == stati[TICK0]["sha"], "")
        corri(TICK0, TICK0 + N_SC)
        A_sha, A_acc = impronta()
        print("  la corsa mai interrotta: M_ass %.17e, V_ass %.17e, E_ass %.17e" % (A_acc["M_ass"], A_acc["V_ass"], A_acc["E_ass"]))
        # ------------------------------------------------------------------ R1: con il salvataggio a meta'
        carica_lib()
        corri(TICK0, TICK0 + META_SC)
        f_ok = os.path.join(DIR_PROVA, "R_%06d.npz" % (TICK0 + META_SC))
        imp = registro().salva(f_ok, meta(TICK0 + META_SC))
        dimezzo_sha, dimezzo_acc = impronta()
        f_np = os.path.join(DIR_PROVA, "R_senza_phi_%06d.npz" % (TICK0 + META_SC))
        registro(senza_phi=True).salva(f_np, meta(TICK0 + META_SC))
        f_na = os.path.join(DIR_PROVA, "R_senza_bordo_%06d.npz" % (TICK0 + META_SC))
        registro(senza_acc=True).salva(f_na, meta(TICK0 + META_SC))
        corri(TICK0 + META_SC, TICK0 + N_SC)
        B_sha, B_acc = impronta()
        esito("DEVE PASSARE: R1 %d tick con il salvataggio a %d = %d tick senza: ogni chiave di z[st] e gli accumulatori del bordo AL BIT" % (N_SC, META_SC, N_SC),
              B_sha == A_sha and B_acc == A_acc, "%d chiavi salvate, %d byte" % (len(imp), os.path.getsize(f_ok)))
        # ------------------------------------------------------------------ R2: sporcato, ricaricato, il resto
        sporca()
        m_ = registro().carica(f_ok)
        ric_sha, ric_acc = impronta()
        corri(TICK0 + META_SC, TICK0 + N_SC)
        C_sha, C_acc = impronta()
        esito("DEVE PASSARE: R2 sporcato (z[st] allo stato vecchio a TICK0, gli accumulatori a zero), ricaricato dal file a %d, %d tick: = la corsa mai interrotta, ogni chiave e ogni accumulatore AL BIT" % (TICK0 + META_SC, N_SC - META_SC),
              ric_sha == dimezzo_sha and ric_acc == dimezzo_acc and C_sha == A_sha and C_acc == A_acc, "il meta: tick %d, commit %s, registrati %s" % (m_["tick"], m_["commit"], m_["registrati"]))
        # ------------------------------------------------------------------ R2-F (a), (b)
        sporca()
        registro(senza_phi=True).carica(f_np)
        corri(TICK0 + META_SC, TICK0 + N_SC)
        Fa_sha, _Fa = impronta()
        esito("DEVE FALLIRE: R2-F (a) il registro SENZA phi_h (la fase del vuoto): la ripartenza = la corsa mai interrotta", not Fa_sha == A_sha,
              "le chiavi diverse: %s" % sorted(k for k in A_sha if Fa_sha[k] != A_sha[k]))
        sporca()
        registro(senza_acc=True).carica(f_na)
        corri(TICK0 + META_SC, TICK0 + N_SC)
        Fb_sha, Fb_acc = impronta()
        MA = float(np.sum(np.abs(st["psi_h"]) ** 2))
        print("  R2-F (b): M + M_ass a %d con gli accumulatori ripartiti da zero %.17e; nella corsa mai interrotta %.17e (lo stato z[st] e' lo stesso: %s)"
              % (TICK0 + N_SC, MA + Fb_acc["M_ass"], MA + A_acc["M_ass"], Fb_sha == A_sha))
        esito("DEVE FALLIRE: R2-F (b) il registro SENZA gli accumulatori del bordo: M + M_ass a %d = quello della corsa mai interrotta" % (TICK0 + N_SC), not MA + Fb_acc["M_ass"] == MA + A_acc["M_ass"], "")
        # ------------------------------------------------------------------ R3
        with np.load(f_ok) as d:
            import json
            mt = json.loads(str(d["meta"]))
        esito("DEVE PASSARE: R3 il file elenca i registrati (st, bordo) e lo sha1 di ogni chiave, e la tabella c_t", mt["registrati"] == ["bordo", "st"] and sorted(mt["sha1"]) == sorted(imp) and "c_t" in mt["tabelle"],
              "%d sha1" % len(mt["sha1"]))
        a1, n1 = alza(lambda: registro(in_piu=True).carica(f_ok))
        a2, n2 = alza(lambda: registro(senza_acc=True).carica(f_ok))
        R4 = registro()
        R4.tabelle["c_t"] = SC.sha1(tab_c * (1.0 + 1e-15))
        a3, n3 = alza(lambda: R4.carica(f_ok))
        esito("DEVE PASSARE: R3 carica ALZA con una grandezza registrata in PIU', con una in MENO, e con una tabella cambiata", a1 and a2 and a3, "%s | %s | %s" % (n1[:50], n2[:50], n3[:50]))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
