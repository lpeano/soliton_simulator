# -*- coding: utf-8 -*-
r"""**LA GEOMETRIA NASCOSTA: PERDITA VERA O SOLO RIPARTENZA?** *(Luca `2026-11-14` `11:26`, G1-G4; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `16`)*.

    python csv/solitone/geometria_nascosta.py perdita > doc/referti_l2/mattone/geometria_perdita.txt
    python csv/solitone/geometria_nascosta.py ripartenza --caso MG|MU|MGU [--ricostruisci] > doc/referti_l2/mattone/geometria_ripartenza_<caso>[_U].txt
    python csv/solitone/geometria_nascosta.py peso --variante oggi|C --registro geometria-peso-<variante> > doc/referti_l2/mattone/geometria_peso_<variante>.txt

### **`perdita`** *(G3)*: **da `MGU_05000` su `L 81`, G+U a campi pieni, `20` tick, quattro bracci dallo stesso stato:** **(oggi)** `mattone.Campi.tick`; **(oggi+contatore)** lo stesso con
`tick_lapse.cs_al_centro` avvolto da un CONTATORE *(le chiamate e i giri in cui le copie del punto fisso vedono `U != I`)*; **(R)** dopo ogni tick vero `U` rimesso al valore di prima del tick;
**(C)** *(mia)* SOLO le copie del punto fisso con `U = I`. **DEVE: (oggi+contatore) = (oggi) AL BIT; il contatore in (R) zero.** **Il bivio: (R) = (oggi) al bit E il contatore di (oggi) zero: (a); se no (b).**
### **`ripartenza`** *(G4)*: **da `<caso>_04000` `1000` tick col tick di `mattone.Campi`, contro `<caso>_05000` chiave per chiave; `--ricostruisci`: `U` rifatto dal campo salvato al caricamento**
*(`_u1_prototipo.scrivi_U`: l'`U` che `avvolto` lascia dopo l'ultimo tick)*.
### **`peso`** *(il ramo (b))*: **`200` tick di `GUrampa`** *(la scena di C35-pi a `60000`, il campo di Gauss, la rampa `min(1, k/500)`, `p6_bracci.tick_GU`)*, **`d` e `rho max` ogni `50`;**
**DEVE: (oggi) = `GUrampa.npz` di `8ca61a34` AL BIT a quei tick; (C) contro `GUrampa.npz`: la differenza.**
**Nessun file esistente cambia: le varianti avvolgono le funzioni IN MEMORIA, e le rimettono.**
"""
import argparse
import contextlib
import io
import json
import os
import subprocess
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

N_PERDITA = 20                          # ### G3
K_DA, K_A = 4000, 5000                  # ### G4
N_PESO, OGNI_PESO, RAMPA = 200, 50, 500   # ### il ramo (b): 200 tick di GUrampa
REF_GURAMPA = ("8ca61a34", "doc/referti_l2/p6_bracci/GUrampa.npz")
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


# =====================================================================================
#   LE VARIANTI, IN MEMORIA
# =====================================================================================
@contextlib.contextmanager
def contatore(mot, U0, conta):
    """### **Il contatore:** `tick_lapse.cs_al_centro` avvolto; **conta le chiamate e i giri in cui `mot.geo.U != U0`** *(le copie del punto fisso girano con l'`U` di quel momento)*; **non cambia i conti.**"""
    from solitone import tick_lapse as TL
    vero = TL.cs_al_centro

    def cs(*a, **kw):
        diverso = not np.array_equal(mot.geo.U, U0)
        out = vero(*a, **kw)
        conta["chiamate"] += 1
        conta["giri"] += out[1]
        if diverso:
            conta["chiamate_U"] += 1
            conta["giri_U"] += out[1]
            conta["max_U"] = max(conta["max_U"], float(np.max(np.abs(mot.geo.U - U0))))
        return out
    TL.cs_al_centro = cs
    try:
        yield
    finally:
        TL.cs_al_centro = vero


@contextlib.contextmanager
def copie_con_I(mot, U0):
    """### **(C)** *(mia)*: **le copie del punto fisso con `U = U0`** *(`I`)*, **il tick vero com'e'.**"""
    from solitone import tick_lapse as TL
    vero = TL.cs_al_centro

    def cs(*a, **kw):
        salvo = mot.geo.U.copy()
        mot.geo.U[...] = U0
        try:
            return vero(*a, **kw)
        finally:
            mot.geo.U[...] = salvo
    TL.cs_al_centro = cs
    try:
        yield
    finally:
        TL.cs_al_centro = vero


def nuovo_conto():
    return {"chiamate": 0, "giri": 0, "chiamate_U": 0, "giri_U": 0, "max_U": 0.0}


def fotografia(Z, C):
    out = {k: Z["st"][k].copy() for k in Z["chiavi"]}
    if C.campo is not None:
        out["campo_A"], out["campo_E"] = C.campo.A.copy(), C.campo.E.copy()
    out["geo_U"] = Z["mot"].geo.U.copy()
    return out


def confronta(a, b, senza=()):
    """### Per chiave: `(uguale al bit, max |a - b| / max |b|)`."""
    out = {}
    for k in sorted(b):
        if k in senza:
            continue
        den = float(np.max(np.abs(b[k]))) or 1.0
        out[k] = (bool(np.array_equal(a[k], b[k])), float(np.max(np.abs(a[k] - b[k]))) / den)
    return out


def stampa_confronto(nome, c):
    diverse = [k for k, (u, _r) in c.items() if not u]
    print("    %s: %d chiavi, diverse %d %s" % (nome, len(c), len(diverse), diverse))
    for k in diverse:
        print("        %-10s la differenza relativa massima %.3e" % (k, c[k][1]))
    return diverse


# =====================================================================================
#   G3: LA PERDITA
# =====================================================================================
def perdita():
    import _presidio
    for m in ("mattone", "mattone_cottura", "p6_bracci", "tick_lapse"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(os.path.join(_CSV, "_u1_prototipo.py"))
    _presidio.avvia(__file__)
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    print("=" * 130)
    print("G3, LA PERDITA (Luca 11:26): da MGU_%05d su L 81, G+U a campi pieni, %d tick; (oggi), (oggi+contatore), (R) U rimesso dopo ogni tick, (C) le copie con U = I" % (K_A, N_PERDITA))
    print("=" * 130)
    with MT.scena(MT.CORSA_BASE, MT.T_BASE) as Z:
        mot = Z["mot"]
        U0 = mot.geo.U.copy()
        dI = float(np.max(np.abs(U0 - np.eye(2)[None, :, :])))
        print("### la scena: %d archi; max |U - I| %r" % (U0.shape[0], dI))
        assert dI == 0.0, "la scena NON ha U = I"
        foto, conti = {}, {}
        for braccio in ("oggi", "oggi+contatore", "R", "C"):
            C, _f = CT.carica(Z, "MGU", rho_c, K_A)
            assert np.array_equal(mot.geo.U, U0), "dopo il caricamento U NON e' quello della scena"
            conta = nuovo_conto()
            t1 = time.time()
            for k in range(K_A + 1, K_A + N_PERDITA + 1):
                U_prima = mot.geo.U.copy()
                if braccio == "oggi":
                    C.tick(k, MT.T_BASE + k, 1.0, e)
                elif braccio == "C":
                    with copie_con_I(mot, U0):
                        C.tick(k, MT.T_BASE + k, 1.0, e)
                else:
                    with contatore(mot, U0, conta):
                        C.tick(k, MT.T_BASE + k, 1.0, e)
                    if braccio == "R":
                        mot.geo.U[...] = U_prima                     # ### (R): U rimesso al valore di prima del tick
            foto[braccio], conti[braccio] = fotografia(Z, C), conta
            print("### (%s) %d tick in %.0f s; max |U - I| alla fine %.3e; max |e A| %.3e; il contatore %s"
                  % (braccio, N_PERDITA, time.time() - t1, float(np.max(np.abs(mot.geo.U - U0))), float(np.max(np.abs(e * C.campo.A))), conta if braccio in ("oggi+contatore", "R") else "--"))
            sys.stdout.flush()
    print("-" * 130)
    print("### I CONFRONTI CON (oggi), chiave per chiave (geo_U compreso dove ha senso):")
    stampa_confronto("(oggi+contatore)", confronta(foto["oggi+contatore"], foto["oggi"]))
    dR = stampa_confronto("(R)", confronta(foto["R"], foto["oggi"], senza=("geo_U",)))
    stampa_confronto("(C)", confronta(foto["C"], foto["oggi"]))
    print("-" * 130)
    ug = [k for k, (u, _r) in confronta(foto["oggi+contatore"], foto["oggi"]).items() if not u]
    esito("lo strumento senza variante (oggi+contatore) = mattone.Campi.tick (oggi) AL BIT, %d tick" % N_PERDITA, not ug, "diverse: %s" % ug, True)
    esito("il contatore conta: in (R) le copie del punto fisso vedono sempre U = I (zero chiamate con U diverso)", conti["R"]["chiamate_U"] == 0 and conti["R"]["chiamate"] > 0,
          "%s" % conti["R"], True)
    co = conti["oggi+contatore"]
    print("### IL CONTATORE di (oggi): %d chiamate di cs_al_centro, %d con U != I (%d giri su %d); max |U - I| visto dalle copie %.3e" % (co["chiamate"], co["chiamate_U"], co["giri_U"], co["giri"], co["max_U"]))
    ramo = "(a) SOLO RIPARTENZA" if (not dR and co["chiamate_U"] == 0) else "(b) PERDITA VERA"
    print("=" * 130)
    print("### IL BIVIO DEL GUARDIANO: (R) = (oggi) al bit: %s; il contatore di (oggi) zero: %s -> %s" % (not dR, co["chiamate_U"] == 0, ramo))
    print("ESITO: %d/%d controlli come devono; fallite %s; %.0f s in tutto" % (OK[0], OK[1], FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


# =====================================================================================
#   G4: LE RIPARTENZE
# =====================================================================================
def ripartenza(caso, ricostruisci):
    import _presidio
    import _u1_prototipo as U1
    for m in ("mattone", "mattone_cottura", "p6_bracci", "tick_lapse"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(os.path.join(_CSV, "_u1_prototipo.py"))
    _presidio.avvia(__file__)
    assert caso in MT.CASI and not (ricostruisci and caso == "MG")
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    print("=" * 130)
    print("G4, LA RIPARTENZA (%s%s; Luca 11:26): da %s_%05d %d tick col tick di mattone.Campi, contro %s_%05d chiave per chiave" % (caso, ", U RICOSTRUITO dal campo (mio)" if ricostruisci else "", caso, K_DA, K_A - K_DA, caso, K_A))
    print("=" * 130)
    with MT.scena(MT.CORSA_BASE, MT.T_BASE) as Z:
        C, f4 = CT.carica(Z, caso, rho_c, K_DA)
        if ricostruisci:
            U1.scrivi_U(Z["mot"], C.campo)                            # ### l'U che avvolto lascia dopo l'ultimo tick: exp(i e A_finale)
            print("### U ricostruito dal campo salvato: max |U - I| %.3e" % float(np.max(np.abs(Z["mot"].geo.U - np.eye(2)[None, :, :]))))
        t1 = time.time()
        for k in range(K_DA + 1, K_A + 1):
            r = MT.r_di(k)
            C.tick(k, MT.T_BASE + k, r if caso in ("MG", "MGU") else 1.0, r * MT.PB.E_DECISO if caso in ("MU", "MGU") else 0.0)
        print("### %d tick in %.0f s" % (K_A - K_DA, time.time() - t1))
        f5 = os.path.join(MT.DIR_E, "%s_%05d.npz" % (caso, K_A))
        with np.load(f5) as d:
            rif = {k: d[k].copy() for k in d.files if k != "meta"}
        mia = fotografia(Z, C)
        c = confronta(mia, rif)
        diverse = stampa_confronto("contro %s" % f5, c)
    esito("(%s%s) la ripartenza da %s_%05d per %d tick = %s_%05d AL BIT" % (caso, ", U ricostruito" if ricostruisci else "", caso, K_DA, K_A - K_DA, caso, K_A), not diverse, "diverse: %s" % diverse, True)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite %s; %.0f s in tutto" % (OK[0], OK[1], FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


# =====================================================================================
#   IL PESO (il ramo (b))
# =====================================================================================
def peso(variante, nome_reg):
    import _presidio
    from solitone import _u1_oggi as UO
    from solitone import bordo as BO
    from solitone import carta_coppia as CC
    from solitone import toro as TO
    for m in ("mattone", "p6_bracci", "tick_lapse", "_u1_oggi", "carta_coppia"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(os.path.join(_CSV, "_u1_prototipo.py"))
    _presidio.avvia(__file__)
    assert variante in ("oggi", "C")
    t00 = time.time()
    dati = subprocess.check_output(["git", "show", "%s:%s" % REF_GURAMPA], cwd=MT.RADICE)
    with np.load(io.BytesIO(dati)) as d:
        meta = json.loads(str(d["meta"]))
        ref = {"t": d["t"].copy(), "d": d["d"].copy(), "rmax": d["rmax"].copy()}
    e = MT.PB.E_DECISO
    e0 = MT.G2.eps_top_tl4b()
    legge = ("rho_c", meta["rho_c"])
    print("=" * 130)
    print("IL PESO (%s; Luca 11:26, il ramo (b)): %d tick di GUrampa dalla scena di %s a %d; la rampa min(1, k/%d); rho_c %r (il meta di %s:%s); e %.7e" % (variante, N_PESO, MT.G2.CORSA, MT.G2.T0, RAMPA, legge[1], REF_GURAMPA[0], REF_GURAMPA[1], e))
    print("=" * 130)
    S = {"t": [], "d": [], "rmax": []}
    with MT.scena(MT.G2.CORSA, MT.G2.T0) as Z:
        z, st, mot, L = Z["z"], Z["st"], Z["mot"], Z["L"]
        U0 = mot.geo.U.copy()
        assert float(np.max(np.abs(U0 - np.eye(2)[None, :, :]))) == 0.0, "la scena NON ha U = I"
        x = TO.scarti(Z["m1"], Z["m2"], Z["bordo"]["c0"][0], Z["bordo"]["c0"][1], L)[:, 0]
        r0 = MT.rho_di(Z)
        campo = UO.campo_della_scena(z, e, MT.PB.FORMA)
        campo.E[...], _D = MT.PB.gauss_sparso(campo, e * (r0 - r0.mean()))

        def misura(k):
            rho = MT.rho_di(Z)
            a, b = CC.centri_semipiani(rho, Z["m1"], Z["m2"], L, x, 0.0)
            S["t"].append(MT.G2.T0 + k)
            S["d"].append(float(np.hypot(*CC.vettore(a, b, L))))
            S["rmax"].append(float(rho.max()))
        misura(0)
        t1 = t_tappa = time.time()
        for k in range(1, N_PESO + 1):
            with MT.PBR.con_rampa(min(1.0, k / float(RAMPA))):
                if variante == "C":
                    with copie_con_I(mot, U0):
                        MT.PBR.tick_GU(z, Z["s"], legge, e0, campo)
                else:
                    MT.PBR.tick_GU(z, Z["s"], legge, e0, campo)
            BO.assorbi(st, Z["g_e"], BO.c_di(MT.G2.T0 + k, Z["tab_c"], Z["K"], Z["omega"]) * Z["phi_v"])
            if k % OGNI_PESO == 0:
                misura(k)
                print("    t %d  d %.10f  rmax %.10e  (%.0f s)" % (S["t"][-1], S["d"][-1], S["rmax"][-1], time.time() - t1))
                sys.stdout.flush()
            if time.time() - t_tappa >= MT.TAPPA_S:
                MT.tappa(nome_reg, "k %d; %.3f s per tick" % (k, (time.time() - t1) / k))
                t_tappa = time.time()
        mot.geo.U[...] = U0
    print("-" * 130)
    print("### %d tick in %.0f s" % (N_PESO, time.time() - t1))
    print("### CONTRO GUrampa (%s): %-8s %-20s %-20s %-12s %-20s %-20s %-12s" % (REF_GURAMPA[0], "t", "d", "d GUrampa", "d - rif", "rmax", "rmax GUrampa", "relativa"))
    uguali = True
    for i, t in enumerate(S["t"]):
        j = int(np.nonzero(ref["t"] == t)[0][0])
        dd, dr = S["d"][i] - ref["d"][j], S["rmax"][i] / ref["rmax"][j] - 1.0
        uguali = uguali and dd == 0.0 and dr == 0.0
        print("    %8d %.12f %.12f %+.3e %.12e %.12e %+.3e" % (t, S["d"][i], ref["d"][j], dd, S["rmax"][i], ref["rmax"][j], dr))
    if variante == "oggi":
        esito("(oggi) = GUrampa.npz AL BIT (d e rho max a %s)" % S["t"], uguali, "", True)
    else:
        print("### (C) contro GUrampa: %s" % ("UGUALE AL BIT" if uguali else "DIVERSO (le differenze sopra)"))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite %s; %.0f s in tutto" % (OK[0], OK[1], FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("azione", choices=("perdita", "ripartenza", "peso"))
    ap.add_argument("--caso", choices=MT.CASI)
    ap.add_argument("--ricostruisci", action="store_true")
    ap.add_argument("--variante", choices=("oggi", "C"))
    ap.add_argument("--registro")
    x = ap.parse_args(argv)
    if x.azione == "perdita":
        return perdita()
    if x.azione == "ripartenza":
        return ripartenza(x.caso, x.ricostruisci)
    return peso(x.variante, x.registro)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
