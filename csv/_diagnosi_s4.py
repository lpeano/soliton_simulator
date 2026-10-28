# -*- coding: utf-8 -*-
r"""**LA DIAGNOSI DEL SOLITONE S4** *(il mandato di Luca delle `19:18` del `2026-10-28`, parte `2`; [[DECISIONE-L1-NATURA-A-SIMULATORE-B]], [[PIANO-2D-3D]];
il task history `doc/TASK_HISTORY/2026-10-28_requisiti_legame.md`)*: ### **una DIAGNOSI, non un candidato** *(S4 resta con R2 e R3 contrari)*.
### **Lo strumento del congelato lungo** *(`_congelato_lungo`: il congelato VERO, a pezzi)* ### **con la forma, `s` e `N` in memoria** *(`VC.FORMA`, `VC.S`, `DC.N`, rimessi alla fine)*;
### **il vuoto uniforme** *(col congelato vero fondo e uniforme sono identici: `40061005`)*; ### **la lettura con le funzioni di `_cuore_e_alone`.**

> ### **Lo stato a fine pezzo in `db/diagnosi_s4/*.npz`** *(ignorato da git: il dato e' il comando)*; ### **i punti in un file per pezzo in `doc/referti_l2/diagnosi_s4/`.**

    python csv/_diagnosi_s4.py --controlli
    python csv/_diagnosi_s4.py --pezzo <0|1|2>          (da ripetere: ogni volta il pezzo dopo)
    python csv/_diagnosi_s4.py --referto > doc/referti_l2/diagnosi_s4.txt
"""
import contextlib
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

# ### le corse, dichiarate PRIMA (il task history): (forma, s, N, L)
CORSE = (("S4", 0.3, 1e7, 81), ("S4", 0.3, 1e7, 120), ("S4", 0.99, 1e7, 81))
SCENA = "uniforme"
T_FIS = 3000.0                 # ### il tempo fisico di ogni corsa
PEZZO = 2000
PASSO_FIS = 3.0                # ### un punto ogni ~3 di tempo fisico: OGNI = round(3 / s) tick
FINESTRA = 500.0
TICK_KP = 40
TICK_K40 = 200                 # ### il controllo contro 40061005: i primi 200 tick di S1, s 0.3, N 1e6, L 81
TOLL_NORMA = 1e-10
STATI = os.path.join(RADICE, "db", "diagnosi_s4")
PUNTI = os.path.join(RADICE, "doc", "referti_l2", "diagnosi_s4")
RIF_K40 = os.path.join(RADICE, "doc", "referti_l2", "congelato_lungo", "L81_uniforme_00000.jsonl")
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


@contextlib.contextmanager
def configura(forma, s, N):
    """### **La forma, `s` e `N` in memoria** *(i globali di `_solitone_vuoto_congelato` e `_deriva_congelato`)*, ### **rimessi all'uscita.**"""
    import _deriva_congelato as DC
    import _solitone_vuoto_congelato as VC
    vero = (VC.FORMA, VC.S, DC.N)
    VC.FORMA, VC.S, DC.N = forma, s, N
    try:
        yield
    finally:
        VC.FORMA, VC.S, DC.N = vero


def ogni(s):
    return max(1, int(round(PASSO_FIS / s)))


def t_max(s):
    return int(round(T_FIS / s))


def nome(c):
    return "%s_s%.2f_L%d" % (c[0], c[1], c[3])


def iniziale(forma, s, L):
    """### **Lo stato del risolutore a `s` sul toro `L`** *(le righe di `_congelato_lungo.iniziale`, con la forma e `N` di `configura`)*."""
    import _deriva_congelato as DC
    rec = DC.prepara(s)
    rec["fattore"] = (L - 0.1) / rec["larghezza"]
    z = DC.nuovo(rec, SCENA)
    assert z["L"] == L, (z["L"], L)
    return rec, z


def avanza(z, phi0, quanti, forma):
    import _congelato_lungo as CL
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _triangoli_bassa_energia as BE
    with SF.forma(forma), BE.conv(DC.ZERO):
        CL.avanza(z, phi0, quanti)


def w_iniziale(z, w0, forma):
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _triangoli_bassa_energia as BE
    with SF.forma(forma), BE.conv(DC.ZERO):
        return DC.forma(z, w0)[0]


def pezzo(i):
    import _congelato_lungo as CL
    c = CORSE[i]
    forma, s, N, L = c
    with configura(forma, s, N):
        rec, z = iniziale(forma, s, L)
        phi0 = z["st"]["phi_h"].copy()
        w0 = rec["larghezza"]
        w_in = w_iniziale(z, w0, forma)
        os.makedirs(STATI, exist_ok=True)
        os.makedirs(PUNTI, exist_ok=True)
        f_stato = os.path.join(STATI, nome(c) + ".npz")
        t0 = 0
        punti = []
        if os.path.exists(f_stato):
            dati = np.load(f_stato)
            t0 = int(dati["t"])
            z["st"]["psi_h"][...] = dati["psi_h"]
            prec = json.loads(io.open(os.path.join(PUNTI, "%s_%05d.jsonl" % (nome(c), t0 - PEZZO)), encoding="utf-8").read())
            assert prec["sha_fine"] == CL.sha(z["st"]["psi_h"]), "lo stato salvato NON e' quello della fine del pezzo prima"
        else:
            punti.append(CL.punto(z, 0, w_in, w0))
        tm = t_max(s)
        if t0 >= tm:
            print("  %s: finita (t %d)" % (nome(c), t0))
            return False
        t1 = min(t0 + PEZZO, tm)
        s0 = time.time()
        for t in range(t0 + 1, t1 + 1):
            avanza(z, phi0, 1, forma)
            if t % ogni(s) == 0:
                punti.append(CL.punto(z, t, w_in, w0))
        riga = {"forma": forma, "s": s, "N": N, "L": L, "scena": SCENA, "t0": t0, "t1": t1, "w0": w0, "w_in": w_in, "mu": rec["mu"], "verdetto": rec["verdetto"],
                "c": rec["c"], "punti": punti, "sha_fine": CL.sha(z["st"]["psi_h"]), "secondi": time.time() - s0}
    f_punti = os.path.join(PUNTI, "%s_%05d.jsonl" % (nome(c), t0))
    assert not os.path.exists(f_punti), ("il pezzo c'e' gia'", f_punti)
    dati = (json.dumps(riga, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
    with open(f_punti, "xb") as f:
        f.write(dati)
    tmp = os.path.join(STATI, nome(c) + "_tmp.npz")
    np.savez(tmp, psi_h=z["st"]["psi_h"], t=t1)
    os.replace(tmp, f_stato)
    print("  %s: tick %d -> %d, w/w_in %.5f (%.0f s)" % (nome(c), t0, t1, punti[-1]["w"] / w_in, riga["secondi"]))
    return True


def controlli():
    """### **`(kp)`** *(`S4`, `s 0.3`, `L 81`)*: ### **`TICK_KP` tick di fila = due meta' con lo stato salvato e ricaricato, AL BIT;**
    ### **`(k40)`:** ### **con `S1`, `s 0.3`, `N 1e6`, `L 81` i punti dei primi `TICK_K40` tick = quelli di `40061005`, AL BIT.**"""
    import _congelato_lungo as CL
    import tempfile
    forma, s, N, L = CORSE[0]
    with configura(forma, s, N):
        _r, za = iniziale(forma, s, L)
        pa = za["st"]["phi_h"].copy()
        avanza(za, pa, TICK_KP, forma)
        _r, zb = iniziale(forma, s, L)
        pb = zb["st"]["phi_h"].copy()
        avanza(zb, pb, TICK_KP // 2, forma)
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, "kp.npz")
            np.savez(f, psi_h=zb["st"]["psi_h"], t=TICK_KP // 2)
            _r, zc = iniziale(forma, s, L)
            pc = zc["st"]["phi_h"].copy()
            zc["st"]["psi_h"][...] = np.load(f)["psi_h"]
        avanza(zc, pc, TICK_KP - TICK_KP // 2, forma)
        kp = za["st"]["psi_h"].tobytes() == zc["st"]["psi_h"].tobytes()
    rif = json.loads(io.open(RIF_K40, encoding="utf-8").read())
    with configura("S1", 0.3, 1e6):
        rec, z = iniziale("S1", 0.3, 81)
        phi0 = z["st"]["phi_h"].copy()
        w0 = rec["larghezza"]
        w_in = w_iniziale(z, w0, "S1")
        mio = {0: CL.punto(z, 0, w_in, w0)}
        for t in range(1, TICK_K40 + 1):
            avanza(z, phi0, 1, "S1")
            if t % ogni(0.3) == 0:
                mio[t] = CL.punto(z, t, w_in, w0)
    suo = {p["t"]: p for p in rif["punti"] if p["t"] <= TICK_K40}
    k40 = sorted(mio) == sorted(suo) and all(mio[t] == suo[t] for t in suo)
    return {"kp": kp, "k40": k40, "k40_punti": len(suo)}


def serie(c):
    righe = []
    if os.path.isdir(PUNTI):
        for n in sorted(os.listdir(PUNTI)):
            if n.startswith(nome(c) + "_") and n.endswith(".jsonl"):
                righe.append(json.loads(io.open(os.path.join(PUNTI, n), encoding="utf-8").read()))
    righe.sort(key=lambda r: r["t0"])
    for a, b in zip(righe, righe[1:]):
        assert a["t1"] == b["t0"], ("un buco fra i pezzi", a["t1"], b["t0"])
    return righe, [p for r in righe for p in r["punti"]]


def finale(c):
    import _energia_del_legame as EL
    forma, s, N, L = c
    rec, z = iniziale(forma, s, L)
    rho0 = EL.densita(z["inc"], z["st"])[0].copy()
    zeri = int(np.sum(rho0 == 0.0))
    dati = np.load(os.path.join(STATI, nome(c) + ".npz"))
    z["st"]["psi_h"][...] = dati["psi_h"]
    return rec, z, rho0, int(dati["t"]), zeri


def referto():
    import _congelato_lungo as CL
    import _cuore_e_alone as CE
    import _energia_del_legame as EL
    print("=" * 130)
    print("LA DIAGNOSI DEL SOLITONE S4 (Luca 19:18, parte 2; una DIAGNOSI, non un candidato): il congelato vero, zero simmetrico, cs spento, il vuoto %s" % SCENA)
    print("=" * 130)
    print("  la configurazione: CORSE %s SCENA %s T_FIS %g PEZZO %d PASSO_FIS %g FINESTRA %g TICK_KP %d TICK_K40 %d TOLL_NORMA %g" % (CORSE, SCENA, T_FIS, PEZZO, PASSO_FIS, FINESTRA, TICK_KP, TICK_K40, TOLL_NORMA))
    print("  LE LETTURE, SCRITTE PRIMA: il cuore di S4 si stabilizza o si svuota; la larghezza in archi cambia o no fra s 0.3 e s 0.99. S4 resta con R2 e R3 contrari")
    f = os.path.join(PUNTI, "controlli.json")
    k = json.loads(io.open(f, encoding="utf-8").read()) if os.path.exists(f) else {}
    esito("DEVE PASSARE (kp): S4, s 0.3, L 81: %d tick di fila = due meta' con lo stato salvato e ricaricato, AL BIT" % TICK_KP, k.get("kp") is True, "")
    esito("DEVE PASSARE (k40): S1, s 0.3, N 1e6, L 81: i punti dei primi %d tick = 40061005, AL BIT" % TICK_K40, k.get("k40") is True, "%s punti" % k.get("k40_punti"))
    sintesi = []
    for c in CORSE:
        forma, s, N, L = c
        print("-" * 130)
        righe, pts = serie(c)
        if not pts:
            print("### %s: nessun pezzo" % nome(c))
            continue
        r0 = righe[0]
        l_env = math.sqrt(abs(r0["c"]) / s)
        print("### %s: %d pezzi, fino al tick %d (tempo fisico %.0f); il risolutore: %s, w0 %.4f archi, l = sqrt(|c|/s) %.4f (w0/l %.4f), mu %+.6f; w_in %.4f; %.0f s"
              % (nome(c), len(righe), righe[-1]["t1"], righe[-1]["t1"] * s, r0["verdetto"], r0["w0"], l_env, r0["w0"] / l_env, r0["mu"], r0["w_in"], sum(r["secondi"] for r in righe)))
        dM = max(abs(p["M"] - pts[0]["M"]) / pts[0]["M"] for p in pts)
        esito("DEVE PASSARE (n): %s, M entro %g relativo" % (nome(c), TOLL_NORMA), dM <= TOLL_NORMA, "%.1e" % dM)
        esito("DEVE PASSARE: %s, la corsa e' completa (%d tick)" % (nome(c), t_max(s)), righe[-1]["t1"] == t_max(s), "")
        w_in, p0 = r0["w_in"], pts[0]["picco"]
        tau = np.array([p["tau"] for p in pts]) * (s / 0.3)          # ### CL.punto scrive tau = t * 0.3: il tempo fisico vero e' t * s
        q = np.array([p["w"] / w_in for p in pts])
        pk = np.array([p["picco"] / p0 for p in pts])
        cu = np.array([p["f_win"] for p in pts])
        al = np.array([1.0 - p["f_3w0"] for p in pts])
        a = 0.0
        while a < tau[-1] - 1e-9:
            m = (tau >= a - 1e-9) & (tau <= a + FINESTRA + 1e-9)
            if m.sum() > 2:
                pw = np.polyfit(tau[m], q[m], 1)[0]
                pc = np.polyfit(tau[m], cu[m], 1)[0]
                print("  tau [%6.0f, %6.0f]: w/w_in da %.5f a %.5f (pendenza %+.3e); cuore da %.5f a %.5f (pendenza %+.3e); alone da %.5f a %.5f; picco relativo medio %.5f"
                      % (a, a + FINESTRA, q[m][0], q[m][-1], pw, cu[m][0], cu[m][-1], pc, al[m][0], al[m][-1], pk[m].mean()))
            a += FINESTRA
        with configura(forma, s, N):
            rec, z, rho0, t, zeri = finale(c)
            esito("DEVE PASSARE: %s, lo stato finale = sha_fine dell'ultimo pezzo" % nome(c), t == righe[-1]["t1"] and CL.sha(z["st"]["psi_h"]) == righe[-1]["sha_fine"], "t %d" % t)
            rho1 = EL.densita(z["inc"], z["st"])[0]
            _M0, _c0, d0 = CE.baricentro(z, rho0)
            M1, c1, d1 = CE.baricentro(z, rho1)
            pr0, pr1 = CE.anelli(rho0, d0), CE.anelli(rho1, d1)
            N_c = pts[-1]["f_win"] * M1
            ls, _q, r_c, u_c = CE.risolutore(rec, N_c)
            rs_c = CE.sul_toro(z, r_c, u_c, N_c)
            _a, _b, ds_c = CE.baricentro(z, rs_c)
            prs_c = CE.anelli(rs_c, ds_c)
        f0, f1, fc = CE.fwhm(pr0), CE.fwhm(pr1), CE.fwhm(prs_c)
        print("  i nodi con rho = 0 esatto al tick 0: %d (alpha_4 li' vale 0, non -pi: _screening_forme_s3.pezzi_di)" % zeri)
        print("  la FWHM (anelli di 1): all'inizio %.4f, alla fine %.4f archi (x%.4f; in unita' di l %.4f e %.4f); il picco per nodo x%.4f; il baricentro finale (%+.2e, %+.2e)"
              % (f0, f1, f1 / f0, f0 / l_env, f1 / l_env, rho1.max() / rho0.max(), c1[0], c1[1]))
        print("  il cuore finale N_c %.1f (%.5f M); il risolutore a N_c: %s, larghezza %.4f, FWHM %.4f (il cuore finale / il risolutore x%.4f), picco per nodo x%.4f"
              % (N_c, N_c / M1, ls["verdetto"], ls["larghezza"], fc, f1 / fc, rho1.max() / rs_c.max()))
        print("  il profilo per anelli, r 0..8: inizio %s" % " ".join("%.4g" % v for v in pr0[:9]))
        print("                                  fine   %s" % " ".join("%.4g" % v for v in pr1[:9]))
        sintesi.append((nome(c), s, r0["w0"], l_env, f0, f1, pts[-1]["w"], cu[0], cu[-1]))
    print("-" * 130)
    print("### LA LARGHEZZA IN ARCHI E IN l = sqrt(|c|/s), alle due s (la convergenza: DECISIONE-L1-NATURA-A-SIMULATORE-B)")
    for (n, s, w0, l_env, f0, f1, w1, c0, c1) in sintesi:
        print("  %-16s s %.2f: w0 del risolutore %.4f archi (%.4f l); FWHM %.4f -> %.4f archi (%.4f -> %.4f l); w finale %.4f archi; cuore %.5f -> %.5f" % (n, s, w0, w0 / l_env, f0, f1, f0 / l_env, f1 / l_env, w1, c0, c1))
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import _solitone_vuoto_congelato as VC
    import _deriva_congelato as DC
    vero = (VC.FORMA, VC.S, DC.N)
    try:
        if argv[:1] == ["--controlli"]:
            e = controlli()
            print("  (kp) %s; (k40) %s su %d punti" % (e["kp"], e["k40"], e["k40_punti"]))
            os.makedirs(PUNTI, exist_ok=True)
            f = os.path.join(PUNTI, "controlli.json")
            assert not os.path.exists(f), f
            dati = (json.dumps(e, sort_keys=True) + "\n").encode("utf-8")
            with open(f, "xb") as fh:
                fh.write(dati)
        elif argv[:1] == ["--pezzo"]:
            pezzo(int(argv[1]))
        elif argv[:1] == ["--referto"]:
            referto()
        else:
            raise SystemExit(__doc__)
    finally:
        VC.FORMA, VC.S, DC.N = vero
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
