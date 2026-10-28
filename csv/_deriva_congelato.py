# -*- coding: utf-8 -*-
r"""**LA DERIVA DEL CONGELATO** *(la risposta di Luca delle `14:27` del `2026-10-28`, parte `2`; [[VUOTO-SUL-FONDO]], [[PROGETTO-MASSA-COLLETTIVA]];
il task history `doc/TASK_HISTORY/2026-10-28_rilettura_buca_e_deriva.md`)*: ### **lo stato del risolutore d'inviluppo e' lo stazionario del passo discreto?**
### **Corse BREVI col vuoto congelato** *(il tick intero, `phi` rimesso a `phi0` a fine tick)*, ### **`N 1e6`, lo zero simmetrico, `S1`, `cs` spento, a `s 0.075` e a `s 0.3`.**

> ### **In memoria; nessun file del nucleo.**

    python csv/_deriva_congelato.py > doc/referti_l2/deriva_congelato.txt
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

N = 1e6
L_TORO = 81
ZERO = "simm"
S_MISURA = (0.075, 0.3)
TICK = 100                     # ### il mandato: il profilo dopo 100 tick
TICK_C0 = 20
TICK_ONDA = 20
TAU_UGUALE = 7.5               # ### a s 0.3 anche il profilo allo stesso tempo fisico di 100 tick a s 0.075
RIF = os.path.join(RADICE, "doc", "referti_l2", "solitone_con_la_buca", "grande_fondo_congelato.jsonl")
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def prepara(s):
    """### **Le righe di `_solitone_con_la_buca.prepara` a questo `s`** *(`VC.S` in memoria)*: `rec` e il verdetto del risolutore."""
    import _modi_pi_e_solitoni as MPS
    import _solitoni_triangoli as STR
    import _solitone_vuoto_congelato as VC
    VC.S = s
    vero = MPS.LAM0
    MPS.LAM0 = STR.LAM0_TRI
    try:
        cc, _cy, _w0 = STR.c_triangoli(s)
        ls = MPS.largo(VC.FORMA, cc, s, N)
    finally:
        MPS.LAM0 = vero
    return {"larghezza": ls["larghezza"], "c": cc, "mu": ls["mu"], "verdetto": ls["verdetto"], "fattore": (L_TORO - 0.1) / ls["larghezza"]}


def nuovo(rec, scena):
    import _energia_del_legame as EL
    import _solitone_con_la_buca as B
    L, inc, mot, st, par, pos, rr, Q, m1, m2, r_mat = EL.stato(N, rec["fattore"], rec)
    st["phi_h"][...] = B.vuoto_iniziale(scena, inc, L)
    return {"L": L, "inc": inc, "mot": mot, "st": st, "par": par, "pos": pos, "rr": rr, "Q": Q, "m1": m1, "m2": m2}


def tick_congelato(z, phi0, salta=()):
    import composizione as CM
    import tick as TK
    TK.percorri_tick(z["st"], z["mot"], z["par"], salta, None, len(CM.ORDINE))
    z["st"]["phi_h"][...] = phi0


def forma(z, w0):
    """### **Le righe di `forma_m` di `_solitone_con_la_buca.corsa`.**"""
    import _energia_del_legame as EL
    import _solitoni_triangoli as STR
    rho, lam = EL.densita(z["inc"], z["st"])
    M = float(rho.sum())
    c = (rho @ z["pos"]) / M
    w2 = float(rho @ np.sum((z["pos"] - c) ** 2, axis=1)) / M
    fr = float(rho[np.hypot(z["pos"][:, 0] - c[0], z["pos"][:, 1] - c[1]) <= STR.RAGGIO_FRAZ * w0].sum()) / M
    return math.sqrt(w2), fr, rho, lam


def ampiezze(z):
    n = z["inc"].n
    return z["st"]["psi_h"].reshape(n, -1) @ np.conj(z["Q"])


def misura(s):
    """### **`TICK` tick congelati dallo stato del risolutore:** ### **la rotazione al centro e per nodo, il profilo, la fedelta'; l'onda piana a `K` per la previsione.**"""
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    rec = prepara(s)
    z = nuovo(rec, "fondo")
    phi0 = z["st"]["phi_h"].copy()
    w0 = rec["larghezza"]
    psi0 = z["st"]["psi_h"].copy()
    # ### l'onda piana a K: gli stessi pezzi, SENZA il legame; uniforme, norma N.
    # ### COSTRUITA FUORI DA BE.conv: dentro, coppia_K trova i gruppi [2, 4, 2] e l'assert ferma tutto (f2c646e3)
    zo = nuovo(rec, "fondo")
    cel = zo["Q"][None, :] * np.exp(2j * np.pi * (zo["m1"] + zo["m2"]) / 3.0)[:, None]
    cel *= math.sqrt(N / float(np.sum(np.abs(cel) ** 2)))
    zo["st"]["psi_h"][...] = cel.reshape(zo["st"]["psi_h"].shape)
    po = zo["st"]["psi_h"].copy()
    out = {"s": s, "L": z["L"], "mu": rec["mu"], "verdetto": rec["verdetto"], "w0": w0}
    with SF.forma(VC.FORMA), BE.conv(ZERO):
        w_in, _f, rho0, _l = forma(z, w0)
        i_c = int(np.argmin(z["rr"]))
        dentro = z["rr"] <= w_in
        a_prec = ampiezze(z)
        rot_c, rot_nodi = [], []
        prof = {}
        t_eq = int(round(TAU_UGUALE / s))
        t0 = time.time()
        for t in range(1, TICK + 1):
            tick_congelato(z, phi0)
            a = ampiezze(z)
            rot = -np.angle(a / a_prec)
            rot_c.append(float(rot[i_c]))
            rot_nodi.append(rot)
            a_prec = a
            if t in (t_eq, TICK):
                w, fr, rho, _l = forma(z, w0)
                prof[t] = {"w/w_in": w / w_in, "frazione": fr, "drho": float(np.linalg.norm(rho - rho0) / np.linalg.norm(rho0)),
                           "fedelta": float(abs(np.vdot(psi0.ravel(), z["st"]["psi_h"].ravel()))) / N}
        out["secondi_per_tick"] = (time.time() - t0) / TICK
        R = np.mean(np.array(rot_nodi), axis=0)
        p = rho0[dentro] / rho0[dentro].sum()
        media = float(p @ R[dentro])
        out.update({"w_in": w_in, "rot_centro": float(np.mean(rot_c)), "rot_centro_dev": float(np.std(rot_c)), "rot_pesata": media,
                    "rot_dispersione": float(math.sqrt(p @ (R[dentro] - media) ** 2)), "rot_min_max": (float(R[dentro].min()), float(R[dentro].max())), "profilo": prof, "t_eq": t_eq})
        ac = ampiezze(zo)
        ro = []
        for _t in range(TICK_ONDA):
            tick_congelato(zo, phi0, ("CAMM-MATERIA-VUOTO",))
            a = ampiezze(zo)
            ro.append(float(np.mean(-np.angle(a / ac))))
            ac = a
        out["onda_rot"] = float(np.mean(ro))
        out["onda_rot_dev"] = float(np.std(ro))
        out["onda_sovrapposizione"] = float(abs(np.vdot(po.ravel(), zo["st"]["psi_h"].ravel()))) / N
    out["rot_prevista"] = out["onda_rot"] + out["mu"]
    return out


def c0():
    """### **`(c0)`: col vuoto congelato `psi` dopo `TICK_C0` tick e' lo stesso AL BIT col fondo e con l'uniforme;** ### **e `Lambda` per nodo uguale al bit.**"""
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _energia_del_legame as EL
    rec = prepara(0.075)
    stati, lams = [], []
    for sc in ("fondo", "uniforme"):
        z = nuovo(rec, sc)
        phi0 = z["st"]["phi_h"].copy()
        lams.append(EL.densita(z["inc"], z["st"])[1].tobytes())
        with SF.forma(VC.FORMA), BE.conv(ZERO):
            for _t in range(TICK_C0):
                tick_congelato(z, phi0)
        stati.append(z["st"]["psi_h"].tobytes())
    return lams[0] == lams[1], stati[0] == stati[1]


def c1():
    """### **`(c1)`: la larghezza del congelato ai tick `40` e `80` ridata AL BIT dalla serie di `grande_fondo_congelato`.**"""
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    rif = json.loads(io.open(RIF, encoding="utf-8").read())
    wr = {x["t"]: x["larghezza"] for x in rif["serie"]}
    rec = prepara(0.075)
    z = nuovo(rec, "fondo")
    phi0 = z["st"]["phi_h"].copy()
    w = {}
    with SF.forma(VC.FORMA), BE.conv(ZERO):
        for t in range(1, 81):
            tick_congelato(z, phi0)
            if t in (40, 80):
                w[t] = forma(z, rec["larghezza"])[0]
    return all(w[t] == wr[t] for t in (40, 80)), w, {t: wr[t] for t in (40, 80)}


def main():
    import _presidio
    _presidio.avvia(__file__)
    import _solitone_vuoto_congelato as VC
    import composizione as CM
    s_vero = VC.S
    try:
        print("=" * 130)
        print("LA DERIVA DEL CONGELATO (Luca 14:27, parte 2): lo stato del risolutore e' lo stazionario del passo? N %g, L %d, zero %s, S1, cs spento; %d tick congelati a s %s" % (N, L_TORO, ZERO, TICK, S_MISURA))
        print("=" * 130)
        print("  la configurazione: N %g L_TORO %d ZERO %s S_MISURA %s TICK %d TICK_C0 %d TICK_ONDA %d TAU_UGUALE %g; il passo: %d pezzi, impronta %s"
              % (N, L_TORO, ZERO, S_MISURA, TICK, TICK_C0, TICK_ONDA, TAU_UGUALE, len(CM.ORDINE), CM.IMPRONTA))
        print("  la rotazione PREVISTA = la rotazione dell'onda piana a K (gli stessi pezzi, senza il legame) + mu del risolutore (la regola di 74f99039, dichiarata nel task history)")
        print("-" * 130)
        lam_ok, psi_ok = c0()
        esito("DEVE PASSARE (c0): congelato, %d tick, s 0.075: psi uguale AL BIT col fondo e con l'uniforme, e Lambda per nodo uguale al bit" % TICK_C0, lam_ok and psi_ok,
              "Lambda %s, psi %s" % (lam_ok, psi_ok))
        ok1, w, wr = c1()
        esito("DEVE PASSARE (c1): la larghezza del congelato ai tick 40 e 80 = la serie di grande_fondo_congelato AL BIT", ok1, "qui %s, la serie %s" % (w, wr))
        if not ok1:
            print("FERMO: lo stato della parte 2 non e' quello delle corse")
            return 1
        print("-" * 130)
        for s in S_MISURA:
            m = misura(s)
            print("### s %g: il risolutore %s, larghezza %.4f, mu %+.6f; L %d; w_in sul toro %.4f; %.3f s per tick" % (s, m["verdetto"], m["w0"], m["mu"], m["L"], m["w_in"], m["secondi_per_tick"]))
            print("  la rotazione per tick: al centro %+.6f (dev %.2e); pesata con rho entro w_in %+.6f, la dispersione fra i nodi %.3e (min %+.6f max %+.6f)"
                  % (m["rot_centro"], m["rot_centro_dev"], m["rot_pesata"], m["rot_dispersione"], m["rot_min_max"][0], m["rot_min_max"][1]))
            print("  l'onda piana a K senza legame: rotazione %+.6f (dev %.2e), sovrapposizione dopo %d tick %.12f; la rotazione PREVISTA %+.6f; misurata al centro - prevista %+.3e"
                  % (m["onda_rot"], m["onda_rot_dev"], TICK_ONDA, m["onda_sovrapposizione"], m["rot_prevista"], m["rot_centro"] - m["rot_prevista"]))
            for t, p in sorted(m["profilo"].items()):
                print("  dopo %3d tick (tempo fisico %.2f): w/w_in %.6f, frazione %.6f, |rho - rho0|/|rho0| %.4e, la fedelta' |<psi0,psi>|/N %.8f"
                      % (t, t * s, p["w/w_in"], p["frazione"], p["drho"], p["fedelta"]))
            Tf = int(math.ceil(2.0 * math.pi / abs(m["mu"]))) if m["mu"] else None
            print("  LA PROPOSTA, IL COSTO DI UN GIRO: un filtro sul passo stesso lungo 2 pi / |mu| = %s tick, a %.3f s per tick: %s s per giro (il numero dei giri NON e' noto prima di provare)"
                  % (Tf, m["secondi_per_tick"], "%.0f" % (Tf * m["secondi_per_tick"]) if Tf else "-"))
        print("-" * 130)
        print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    finally:
        VC.S = s_vero
    return 0


if __name__ == "__main__":
    sys.exit(main())
