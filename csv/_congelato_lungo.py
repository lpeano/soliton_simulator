# -*- coding: utf-8 -*-
r"""**IL CONGELATO LUNGO** *(la risposta di Luca delle `15:49` del `2026-10-28`, punto `2`; [[VUOTO-SUL-FONDO]], [[PROGETTO-MASSA-COLLETTIVA]];
il task history `doc/TASK_HISTORY/2026-10-28_congelato_lungo_e_fasi_del_vuoto.md`)*: ### **il solo congelato VERO** *(i pezzi del vuoto saltati, `phi` rimesso a fine tick: quello di `74f99039`; Luca `16:15`)*, ### **`N 1e6`, `s 0.3`, lo zero simmetrico, `S1`, `cs` spento;**
### **`L 81` e `L 120`, il vuoto uniforme e il fondo; `3000` di tempo fisico, A PEZZI:** ### **la larghezza, la frazione entro `w_in`, il picco ogni `3` di tempo fisico.**

> ### **In memoria; nessun file del nucleo.** ### **Lo stato a fine pezzo in `db/congelato_lungo/*.npz`** *(ignorato da git: il dato e' il comando)*; ### **i punti in un file
> per pezzo in `doc/referti_l2/congelato_lungo/`, mai riscritto;** ### **la continuita' si controlla con lo `sha1` dello stato.**

    python csv/_congelato_lungo.py --controlli
    python csv/_congelato_lungo.py --pezzo <81|120> <uniforme|fondo>      (da ripetere: ogni volta il pezzo dopo)
    python csv/_congelato_lungo.py --referto > doc/referti_l2/congelato_lungo.txt
"""
import hashlib
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

S = 0.3
TAGLIE = (81, 120)
SCENE = ("uniforme", "fondo")
T_MAX = 10000                  # ### 3000 di tempo fisico a s 0.3
PEZZO = 2000
OGNI = 10                      # ### 3 di tempo fisico
FINESTRA = 500.0               # ### le finestre della lettura, in tempo fisico
TICK_KP = 40
TOLL_NORMA = 1e-10
STATI = os.path.join(RADICE, "db", "congelato_lungo")
PUNTI = os.path.join(RADICE, "doc", "referti_l2", "congelato_lungo")
# ### le corse col congelato A FINE TICK (lo script di 8dddef5a, fermate alle 16:15): tenute e lette accanto (Luca 16:39)
PUNTI_FT = os.path.join(RADICE, "doc", "referti_l2", "congelato_lungo_fine_tick")
RIF_74 = os.path.join(RADICE, "doc", "referti_l2", "solitone_vuoto_congelato.jsonl")
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


def iniziale(L, scena):
    """### **Lo stato del risolutore a `s 0.3` sul toro `L`** *(le righe di `_deriva_congelato`, con `fattore` per `L`)*."""
    import _deriva_congelato as DC
    rec = DC.prepara(S)
    rec["fattore"] = (L - 0.1) / rec["larghezza"]
    z = DC.nuovo(rec, scena)
    assert z["L"] == L, (z["L"], L)
    return rec, z


def sha(psi):
    return hashlib.sha1(psi.tobytes()).hexdigest()


def punto(z, t, w_in, w0):
    import _energia_del_legame as EL
    rho, _l = EL.densita(z["inc"], z["st"])
    M = float(rho.sum())
    c = (rho @ z["pos"]) / M
    d = np.hypot(z["pos"][:, 0] - c[0], z["pos"][:, 1] - c[1])
    w = math.sqrt(float(rho @ np.sum((z["pos"] - c) ** 2, axis=1)) / M)    # ### la stessa espressione delle corse: il confronto e' al bit
    return {"t": t, "tau": t * S, "w": w, "f_win": float(rho[d <= w_in].sum()) / M, "f_3w0": float(rho[d <= 3.0 * w0].sum()) / M, "picco": float(rho.max()), "M": M}


def avanza(z, phi0, quanti):
    """### **IL CONGELATO VERO, quello di `74f99039`** *(`_solitone_vuoto_congelato.salta_di("congelato")`)*: ### **i pezzi del vuoto `VC.VUOTO` SALTATI, e `phi` rimesso a `phi0` a fine tick.**
    ### ⚠ **NON `DC.tick_congelato`, che fa girare i pezzi del vuoto e rimette `phi` solo a fine tick** *(il congelato «a fine tick» delle corse della buca)*: ### **con quello `(k74)` fallirebbe per la DEFINIZIONE** *(Luca, `16:15`)*."""
    import _deriva_congelato as DC
    import _solitone_vuoto_congelato as VC
    salta = VC.salta_di("congelato")
    assert salta == VC.VUOTO, salta
    for _t in range(quanti):
        DC.tick_congelato(z, phi0, salta)


def nome(L, scena):
    return "L%d_%s" % (L, scena)


def pezzo(L, scena):
    """### **Il pezzo dopo:** ### **dallo stato salvato** *(o dall'inizio)* ### **fino a `PEZZO` tick piu' avanti.**"""
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    rec, z = iniziale(L, scena)
    phi0 = z["st"]["phi_h"].copy()
    w0 = rec["larghezza"]
    os.makedirs(STATI, exist_ok=True)
    os.makedirs(PUNTI, exist_ok=True)
    f_stato = os.path.join(STATI, nome(L, scena) + ".npz")
    t0 = 0
    with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
        w_in = DC.forma(z, w0)[0]
        punti = []
        if os.path.exists(f_stato):
            dati = np.load(f_stato)
            t0 = int(dati["t"])
            z["st"]["psi_h"][...] = dati["psi_h"]
            prec = json.loads(io.open(os.path.join(PUNTI, "%s_%05d.jsonl" % (nome(L, scena), t0 - PEZZO)), encoding="utf-8").read())
            assert prec["sha_fine"] == sha(z["st"]["psi_h"]), "lo stato salvato NON e' quello della fine del pezzo prima"
        else:
            punti.append(punto(z, 0, w_in, w0))
        if t0 >= T_MAX:
            print("  %s: finita (t %d)" % (nome(L, scena), t0))
            return
        t1 = min(t0 + PEZZO, T_MAX)
        s0 = time.time()
        for t in range(t0 + 1, t1 + 1):
            avanza(z, phi0, 1)
            if t % OGNI == 0:
                punti.append(punto(z, t, w_in, w0))
    riga = {"L": L, "scena": scena, "t0": t0, "t1": t1, "w0": w0, "w_in": w_in, "mu": rec["mu"], "punti": punti, "sha_fine": sha(z["st"]["psi_h"]), "secondi": time.time() - s0}
    f_punti = os.path.join(PUNTI, "%s_%05d.jsonl" % (nome(L, scena), t0))
    assert not os.path.exists(f_punti), ("il pezzo c'e' gia'", f_punti)
    dati = (json.dumps(riga, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
    with open(f_punti, "xb") as f:
        f.write(dati)
    tmp = os.path.join(STATI, nome(L, scena) + "_tmp.npz")
    np.savez(tmp, psi_h=z["st"]["psi_h"], t=t1)
    os.replace(tmp, f_stato)
    print("  %s: tick %d -> %d, w/w_in %.5f, picco relativo %.5f (%.0f s)" % (nome(L, scena), t0, t1, punti[-1]["w"] / w_in,
                                                                             punti[-1]["picco"] / (punti[0]["picco"] if t0 == 0 else 1.0), riga["secondi"]))


def kp():
    """### **`(kp)`: `TICK_KP` tick di fila = due meta' con lo stato salvato e ricaricato in mezzo, AL BIT** *(`L 81`, l'uniforme)*."""
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import tempfile
    _r, za = iniziale(81, "uniforme")
    pa = za["st"]["phi_h"].copy()
    with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
        avanza(za, pa, TICK_KP)
    _r, zb = iniziale(81, "uniforme")
    pb = zb["st"]["phi_h"].copy()
    with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
        avanza(zb, pb, TICK_KP // 2)
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "kp.npz")
        np.savez(f, psi_h=zb["st"]["psi_h"], t=TICK_KP // 2)
        _r, zc = iniziale(81, "uniforme")
        pc = zc["st"]["phi_h"].copy()
        zc["st"]["psi_h"][...] = np.load(f)["psi_h"]
    with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
        avanza(zc, pc, TICK_KP - TICK_KP // 2)
    return za["st"]["psi_h"].tobytes() == zc["st"]["psi_h"].tobytes()


def serie(L, scena, cartella=PUNTI):
    righe = []
    if os.path.isdir(cartella):
        for n in sorted(os.listdir(cartella)):
            if n.startswith(nome(L, scena) + "_") and n.endswith(".jsonl"):
                righe.append(json.loads(io.open(os.path.join(cartella, n), encoding="utf-8").read()))
    righe.sort(key=lambda r: r["t0"])
    for a, b in zip(righe, righe[1:]):
        assert a["t1"] == b["t0"], ("un buco fra i pezzi", a["t1"], b["t0"])
    return righe, [p for r in righe for p in r["punti"]]


def referto():
    print("=" * 130)
    print("IL CONGELATO LUNGO (Luca 15:49, punto 2; il congelato VERO, i pezzi del vuoto saltati: Luca 16:15): N 1e6, s %g, zero simmetrico, S1, cs spento; L %s; il vuoto %s; %d tick (%g di tempo fisico), un punto ogni %d tick"
          % (S, TAGLIE, SCENE, T_MAX, T_MAX * S, OGNI))
    print("=" * 130)
    print("  la configurazione: S %g TAGLIE %s SCENE %s T_MAX %d PEZZO %d OGNI %d FINESTRA %g TICK_KP %d TOLL_NORMA %g" % (S, TAGLIE, SCENE, T_MAX, PEZZO, OGNI, FINESTRA, TICK_KP, TOLL_NORMA))
    print("  LA LETTURA DI LUCA, SCRITTA PRIMA: (i) un plateau: il solitone esiste; (ii) oscilla con periodo e ampiezza che restano: esiste e respira; (iii) scappa (la crescita accelera o il picco crolla): l'instabilita' del 2D")
    kpr = os.path.join(PUNTI, "kp.json")
    if os.path.exists(kpr):
        k = json.loads(io.open(kpr, encoding="utf-8").read())
        esito("DEVE PASSARE (kp): %d tick di fila = due meta' con lo stato salvato e ricaricato, AL BIT" % TICK_KP, k["esito"], "")
    else:
        esito("DEVE PASSARE (kp): %d tick di fila = due meta' con lo stato salvato e ricaricato, AL BIT" % TICK_KP, False, "il controllo non c'e'")
    b = [json.loads(y) for y in io.open(RIF_74, encoding="utf-8").read().split("\n") if y.strip()]
    tutte = {}
    for L in TAGLIE:
        for sc in SCENE:
            tutte[(L, sc)] = serie(L, sc)
    for L in TAGLIE:
        r74 = [x for x in b if x.get("tipo") == "corsa" and x.get("modo") == "congelato" and x.get("zero") == "simm" and x.get("L") == L and x.get("N") == 1e6]
        _r, pts = tutte[(L, "uniforme")]
        mio = {p["t"]: p["w"] for p in pts}
        wb = {int(x[0]): x[1] for x in r74[0]["serie"]} if len(r74) == 1 else {}
        com = sorted(set(wb) & set(mio))
        esito("DEVE PASSARE (k74): L %d, il vuoto uniforme: le larghezze ogni 20 tick fino a 2000 = 74f99039 simm congelato AL BIT" % L,
              len(r74) == 1 and len(com) == len(wb) and all(mio[t] == wb[t] for t in com), "%d tick comuni su %d" % (len(com), len(wb)))
    presenti = [(k, v) for k, v in tutte.items() if v[1]]
    dM = {k: max(abs(p["M"] - v[1][0]["M"]) / v[1][0]["M"] for p in v[1]) for k, v in presenti}
    esito("DEVE PASSARE (n): M entro %g relativo in ogni corsa" % TOLL_NORMA, bool(dM) and all(x <= TOLL_NORMA for x in dM.values()), "%s" % {"%d %s" % k: "%.1e" % x for k, x in dM.items()})
    ft = {k: serie(k[0], k[1], PUNTI_FT) for k in tutte}
    for (titolo, insieme) in (("IL CONGELATO VERO (i pezzi del vuoto saltati, phi rimesso a fine tick)", tutte),
                              ("IL CONGELATO A FINE TICK (i pezzi del vuoto girano, phi rimesso a fine tick; lo script di 8dddef5a, fermato alle 16:15)", ft)):
        print("-" * 130)
        print("### %s" % titolo)
        for (L, sc), (righe, pts) in insieme.items():
            if not pts:
                print("### L %d %s: nessun pezzo" % (L, sc))
                continue
            w_in, p0, f0 = righe[0]["w_in"], pts[0]["picco"], pts[0]["f_win"]
            print("### L %d, il vuoto %s: %d pezzi, fino al tick %d (tempo fisico %.0f); w_in %.4f, mu %+.6f; %.0f s" % (L, sc, len(righe), righe[-1]["t1"], righe[-1]["t1"] * S, w_in, righe[0]["mu"], sum(r["secondi"] for r in righe)))
            tau = np.array([p["tau"] for p in pts])
            q = np.array([p["w"] / w_in for p in pts])
            pk = np.array([p["picco"] / p0 for p in pts])
            fr = np.array([p["f_win"] / f0 for p in pts])
            a = 0.0
            while a < tau[-1] - 1e-9:
                m = (tau >= a - 1e-9) & (tau <= a + FINESTRA + 1e-9)
                if m.sum() > 2:
                    pend, inter = np.polyfit(tau[m], q[m], 1)
                    res = q[m] - (pend * tau[m] + inter)
                    print("  tau [%6.0f, %6.0f]: w/w_in da %.5f a %.5f, pendenza %+.3e per unita' di tempo fisico, ampiezza tolta la retta %.3e; picco relativo medio %.5f (min %.5f); frazione entro w_in relativa media %.5f (min %.5f)"
                          % (a, a + FINESTRA, q[m][0], q[m][-1], pend, res.max() - res.min(), pk[m].mean(), pk[m].min(), fr[m].mean(), fr[m].min()))
                a += FINESTRA
            m = tau >= tau[-1] / 2.0
            if m.sum() > 8:
                pend, inter = np.polyfit(tau[m], q[m], 1)
                res = q[m] - (pend * tau[m] + inter)
                sp = np.abs(np.fft.rfft(res)) ** 2
                fq = np.fft.rfftfreq(len(res), d=OGNI * S)
                i = 1 + int(np.argmax(sp[1:]))
                print("  la seconda meta' (tau >= %.0f) tolta la retta: il periodo dominante %.1f di tempo fisico (la frequenza %.4e), ampiezza (max - min) %.3e" % (tau[-1] / 2.0, 1.0 / fq[i], fq[i], res.max() - res.min()))
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import _solitone_vuoto_congelato as VC
    s_vero = VC.S
    try:
        if argv[:1] == ["--controlli"]:
            e = kp()
            print("  (kp) %d tick di fila = due meta' con lo stato salvato e ricaricato, al bit: %s" % (TICK_KP, e))
            os.makedirs(PUNTI, exist_ok=True)
            f = os.path.join(PUNTI, "kp.json")
            assert not os.path.exists(f), f
            dati = (json.dumps({"esito": e}, sort_keys=True) + "\n").encode("utf-8")
            with open(f, "xb") as fh:
                fh.write(dati)
        elif argv[:1] == ["--pezzo"]:
            L, sc = int(argv[1]), argv[2]
            assert L in TAGLIE and sc in SCENE, argv
            pezzo(L, sc)
        elif argv[:1] == ["--referto"]:
            referto()
        else:
            raise SystemExit(__doc__)
    finally:
        VC.S = s_vero
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
