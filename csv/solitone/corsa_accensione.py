# -*- coding: utf-8 -*-
r"""**L'ACCENSIONE LENTA DEL VUOTO: LE CORSE E IL REFERTO** *(il mandato di Luca delle `01:13` del `2026-11-02`, con le decisioni dopo `25614c34`; il task history
`doc/TASK_HISTORY/2026-11-02_accensione_lenta.md`)*: ### **BG-F-0.15 dalla sua partenza, il vuoto acceso con la rampa `sin^2` su `T_acc`, poi il tick intero;**
### **le misure di `_vuoto_vivo_B` col libro col `par`; `D` rispetto alla partenza e, dopo la rampa, rispetto allo stato a `T_acc`.**
### **Dalla decisione di Luca dopo `bfee5330`:** `TA1000` fino a `16000`; la corsa si interrompe **solo nella rampa** *(`A6`)*, dopo registra il primo cuore
### sotto meta' e prosegue; nel referto la vita dal cuore a blocchi, l'alone al `10%`, la barra sulla finestra comune: **due processi.**
### **Dalla decisione di Luca dopo `455b9a95`:** in ogni campione nuovo le misure sul TORO *(`solitone.toro`: il centro periodico, l'alone per settore, il libro per
### settore ogni `LIBRO_SETTORI` tick)*; la corsa `TP1000` *(`TA1000` rifatta da `0`, al bit)*; nel referto `sul_toro`.

    python csv/solitone/corsa_accensione.py --corsa TA1000     # un pezzo; si ripete finche' dice "finita" (dopo bfee5330: fino a 16000)
    python csv/solitone/corsa_accensione.py --corsa TA2000
    python csv/solitone/corsa_accensione.py --corsa TP1000     # (Luca dopo 455b9a95) TA1000 rifatta da 0 col centro periodico; ogni pezzo al bit con TA1000
    python csv/solitone/corsa_accensione.py --corsa TM1000     # (Luca 15:49, dopo 3e3277a2) TP1000 ripetuta con le mappe e gli stati su E:; al bit con TP1000
    python csv/solitone/corsa_accensione.py --mappe > doc/referti_l2/mappe_TM1000.txt
    python csv/solitone/corsa_accensione.py --indice > doc/referti_l2/mappe_indice.txt
    python csv/solitone/corsa_accensione.py --corsa DG1000     # (Luca 18:05) due giri del toro: TP1000 continuata da 16000; i dati su E:, nel repo la versione rada
    python csv/solitone/corsa_accensione.py --indice DG1000 > doc/referti_l2/due_giri_indice.txt
    python csv/solitone/corsa_accensione.py --referto > doc/referti_l2/accensione_lenta.txt
"""
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))

import solitone  # noqa: E402,F401  (i percorsi)

NOME = "BG-F-0.15"             # ### la corsa di _vuoto_vivo_B da cui si parte
CORSE = {"TA1000": (1000.0, 16000.0), "TA2000": (2000.0, 7000.0)}  # ### nome: (T_acc, fine), il mandato; TA1000 fino a 16000 (Luca dopo bfee5330, punto 2)
CONFRONTO = {"TA1000": 6000.0, "TA2000": 7000.0}                   # ### la fine delle finestre del confronto di bfee5330 (i numeri gia' committati)
FINESTRA = (2000.0, 7000.0)    # ### la finestra comune della barra dell'alone: dopo le due rampe, dentro le tre corse (punto 4)
QUOTA_ALONE = 0.1              # ### la vita dell'emissione: l'alone al 10% della materia (Luca, punto 3)
CORSE["TP1000"] = (1000.0, 16000.0)   # ### (Luca dopo 455b9a95) TA1000 rifatta da 0 col centro periodico: in db/ non c'e' lo stato a 9000
GEMELLE = {"TP1000": "TA1000"}       # ### ogni pezzo DEVE dare lo sha_fine della gemella con lo stesso t0
LIBRO_SETTORI = 100            # ### il libro per settore ogni 100 tick (5 OGNI_D): un numero di protocollo, dichiarato (task history, sez. 11)
TP_CENTRI = 9000.0             # ### Luca: prima di 9000 il centro periodico e l'euclideo coincidono ...
TOLL_CENTRI = 0.1              # ### ... entro 0.1
CORSE["TM1000"] = (1000.0, 16000.0)   # ### (Luca 15:49, dopo 3e3277a2) TP1000 ripetuta con le mappe e gli stati: ogni pezzo DEVE essere quello di TP1000
GEMELLE["TM1000"] = "TP1000"
MAPPE = ("TM1000",)            # ### le corse che salvano le mappe (mappe.OGNI tick) su E:
STATI = {"TM1000": (2000.0, 6000.0, 10000.0)}   # ### Luca dopo 3e3277a2: lo stato completo a questi tempi (il tick piu' vicino)
DOPO_STATO = 100               # ### Luca dopo 3e3277a2: ripartendo da ogni stato per 100 tick si ritrova lo stato della corsa al bit
RADICE_E = r"E:\soliton_simulator"   # ### Luca 15:49: il disco esterno degli archivi
DIRS = {"TM1000": os.path.join(RADICE_E, "mappe", "TM1000", "campioni")}   # ### i campioni di TM1000 su E: (doppioni al bit di TP1000; sez. 12)
CORSE["DG1000"] = (1000.0, 40000.0)   # ### (Luca 18:05) due giri del toro: TP1000 continuata da 16000; il tetto: t 40000 dalla partenza (sez. 13)
CONTINUA = {"DG1000": "TP1000"}      # ### il primo pezzo parte dall'ultimo di TP1000 (al bit, ogni chiave)
MAPPE = ("TM1000", "DG1000")
STATI["DG1000"] = (20000.0, 30000.0, 40000.0)   # ### Luca: lo stato completo ogni 10000 unita' (il tick piu' vicino)
BASE_E = {"TM1000": RADICE_E, "DG1000": os.path.join(RADICE_E, "due_giri")}   # ### Luca 18:05: E:\soliton_simulator\due_giri\
DIRS["DG1000"] = os.path.join(RADICE_E, "due_giri", "campioni")
RADA = {"DG1000": os.path.join(solitone.RADICE, "doc", "referti_l2", "due_giri")}   # ### nel repo la versione rada
OGNI_RADA = 100                # ### Luca 18:05: un campione ogni 100 tick
CAMMINO = {"DG1000": 162.0}    # ### Luca 18:05: (a) lo spostamento srotolato dalla partenza arriva a 2 x 81
CENTRO_LIBRO = ("DG1000",)     # ### Luca 18:12 e 18:18: il libro attorno al centro periodico (E_cen) e l'alone a 3 w(t) (sez. 13-bis, 13-ter)
BLOCCO = 1000.0                # ### i blocchi del confronto (come _respiro_congelato)
META = 0.5                     # ### la vita: il cuore a meta' (Luca; dopo bfee5330, della media del primo blocco dopo T_acc)
CODA = 3000.0                  # ### l'estrapolazione dichiarata: la pendenza degli ultimi 3000 (come _respiro_congelato)
DIR_JSON = os.path.join(solitone.RADICE, "doc", "referti_l2", "accensione_lenta")
DIR_NPZ = os.path.join(solitone.RADICE, "db", "accensione_lenta")
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


def dir_json(nome):
    return DIRS.get(nome, DIR_JSON)


def base_e(nome):
    return BASE_E.get(nome, RADICE_E)


def giro_iniziale(da, L):
    """### **Lo stato del cammino e dei blocchi alla fine della corsa `da`** *(sez. `13`)*: il centro periodico srotolato dalla partenza, il riferimento del cuore a
    blocchi *(il primo blocco dopo `T_acc`)*, il blocco aperto."""
    import _vuoto_vivo_B as V
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    s = V.CORSE[NOME][2]
    _rr, camp, _d, _a = serie(da)
    c1 = np.array([c["per"]["c1"] for c in camp])
    c2 = np.array([c["per"]["c2"] for c in camp])
    u1 = np.concatenate([[0.0], np.cumsum(((np.diff(c1) + 0.5 * L) % L) - 0.5 * L)])
    u2 = np.concatenate([[0.0], np.cumsum(((np.diff(c2) + 0.5 * L) % L) - 0.5 * L)])
    X = u1[:, None] * A1 + u2[:, None] * A2
    tt = np.array([c["t"] for c in camp]) * s
    fl = np.array([c["per"]["f_liscia"] for c in camp])
    T_acc = CORSE[da][0]
    rif = float(fl[(tt >= T_acc) & (tt < T_acc + BLOCCO)].mean())
    a = math.floor(tt[-1] / BLOCCO) * BLOCCO
    m = tt >= a
    return {"X0": X[0].tolist(), "X": X[-1].tolist(), "c": [float(c1[-1]), float(c2[-1])], "rif": rif, "a": a, "somma": float(fl[m].sum()), "n": int(m.sum()), "chiusi": []}


def nomi(nome):
    pre = "%s_" % nome
    d = dir_json(nome)
    return sorted(n for n in os.listdir(d) if n.startswith(pre) and n.endswith(".jsonl") and n[len(pre):-6].isdigit()) if os.path.isdir(d) else []


def righe_D(bande, D, n0, t):
    cf = bande.coeff(D)
    pk = np.abs(cf) ** 2
    tot = float(pk.sum())
    return {"t": t, "nD": float(np.linalg.norm(D)) / n0, "bande": {gn: float(pk[..., list(idx)].sum()) / tot for gn, idx in bande.gruppi.items()}}


# ------------------------------------------------------------------------------------------------ la corsa
def corsa(nome):
    """### **Un pezzo di `V.PEZZO` tick;** ### **la ripresa al bit** *(ogni chiave di `z["st"]`, e lo stato a `T_acc`)*."""
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _libro_dei_conti as LC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import misure as MI
    from solitone import protetto as P
    T_acc, tau_fine = CORSE[nome]
    sol, vuoto, s = V.CORSE[NOME]
    K = int(round(T_acc / s))
    t_fine = int(round(tau_fine / s))
    testa_v = V.LP.leggi(os.path.join(V.DIR_JSON, V.nomi(NOME)[0]))
    fatti = nomi(nome)
    da = CONTINUA.get(nome)
    radice = da if da else nome          # ### la corsa da cui viene la testa (la partenza e il cuore iniziale)
    fatti_r = nomi(radice) if da else fatti
    testa = V.LP.leggi(os.path.join(dir_json(radice), fatti_r[0])) if fatti_r else None
    if fatti:
        prec = V.LP.leggi(os.path.join(dir_json(nome), fatti[-1]))
    else:
        prec = V.LP.leggi(os.path.join(dir_json(da), fatti_r[-1])) if da and fatti_r else None
    if prec is not None and (prec["t1"] >= t_fine or (prec["t_dis"] is not None and prec["t_dis"] <= K) or prec.get("fermata")):
        print("  la corsa %s: finita (%d pezzi)" % (nome, len(fatti)))
        return 0
    os.makedirs(dir_json(nome), exist_ok=True)
    os.makedirs(DIR_NPZ, exist_ok=True)
    f_rip = os.path.join(DIR_NPZ, nome + ".npz")
    f_rip_da = os.path.join(DIR_NPZ, (da if da and not fatti else nome) + ".npz")   # ### il primo pezzo di una continuazione legge lo stato di da
    f_acc = os.path.join(DIR_NPZ, (da if da else nome) + "_acc.npz")
    s0 = time.time()
    with V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        w0 = rec["larghezza"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            w_in = DC.forma(z, w0)[0]
        h = MI.lunghezza_arco(z)
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        p0, info = V.partenza(sol, z, phi0, pK, s)
        e_K = P.e_K(z)
        _ph, Z = DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        bande = MI.Bande(Z, z["L"])
        for k, v in salvato.items():
            z["st"][k][...] = v
        mu = info["mu"]
        assert testa_v["info"]["mu"] == mu and testa_v["w_in"] == w_in, "la scena NON e' quella di BG-F-0.15"
        par = z["par"]
        assert par["eps"] == V.EPS != 0.0, "il libro dei conti deve passare il par della corsa (eps acceso)"
        acc = None
        if prec is None:
            t0 = 0
            z["st"]["psi_h"][...] = p0
        else:
            t0 = prec["t1"]
            assert testa["info"]["mu"] == mu and testa["w_in"] == w_in and testa["e_K"] == e_K, "la scena NON e' quella del primo pezzo"
            with np.load(f_rip_da) as dati:
                assert int(dati["t"]) == t0
                for k in z["st"]:
                    if isinstance(z["st"][k], np.ndarray):
                        z["st"][k][...] = dati[k]
            assert V.shas(z) == prec["sha_fine"], "lo stato di ripresa NON e' la fine del pezzo prima (al bit, ogni chiave)"
            fonti = ([os.path.join(dir_json(da), n) for n in nomi(da)] if da else []) + [os.path.join(dir_json(nome), n) for n in fatti]
            accs = [r["acc"] for r in (V.LP.leggi(f) for f in fonti) if r.get("acc")]
            if accs:
                acc = dict(accs[0])
                with np.load(f_acc) as dati:
                    acc["psi"] = dati["psi_h"].copy()
                assert SFM.sha(acc["psi"]) == acc["sha"], "lo stato a T_acc NON e' quello registrato"
        vic = z["rr"] <= V.R_VICINO * w_in
        mas = {"vicino": vic, "lontano": ~vic, "totale": np.ones(z["inc"].n, dtype=bool)}
        t1 = min(t0 + V.PEZZO, t_fine)
        camp, dd, da_ = [], [], []
        t_dis = None
        acc_nuovo = None
        n0 = float(np.linalg.norm(p0))
        mappe_on = nome in MAPPE
        ist, stati, dopo, disco = [], [], {}, None
        tick_stati = {int(round(x / s)) for x in STATI.get(nome, ())}
        if mappe_on:
            from solitone import mappe as MP
            assert MP.OGNI % V.OGNI == 0, "le mappe cadono sui campioni"
            gem = GEMELLE.get(nome) or CONTINUA.get(nome)
            ff = [os.path.join(dir_json(gem), n) for n in nomi(gem)]
            fine_g = V.LP.leggi(ff[-1])["t1"]
            byte_j = int(sum(os.path.getsize(f) for f in ff) * max(t_fine - t0, 0) / fine_g)   # ### i jsonl, in proporzione ai tick di quella corsa
            byte_s = len(tick_stati) * sum(v.nbytes for v in z["st"].values() if isinstance(v, np.ndarray))
            stima = MP.stima(z["inc"].n, max(t_fine - t0, 0) // MP.OGNI + 1) + byte_s + byte_j
            ok, _lib, nota = MP.controlla_disco(base_e(nome), stima)
            disco = {"ok": ok, "nota": nota, "stima": stima}
            if not ok:
                print("  la corsa %s: ### IL DISCO NON BASTA (%s): FERMO" % (nome, nota))
                return 1
        giro, fermata = None, None
        if nome in CAMMINO:
            from solitone import toro as TO
            A1, A2 = TO.vettori()
            Lg = z["L"]
            giro = dict(prec["giro"]) if prec and prec.get("giro") else giro_iniziale(da, Lg)
            giro["chiusi"] = []
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            if t0 == 0:
                conti = LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO, par)
                c = V.misura(z, 0, w_in, w0, h, LC, conti, mas)
                periodiche(z, c, conti, w_in, w0, h, 0, LC, nome in CENTRO_LIBRO)
                c["lam"] = 0.0
                camp.append(c)
                if mappe_on:
                    ist.append(MP.istantanea(z, 0, 0.0, (c["per"]["x"], c["per"]["y"])))
            f_lis0 = camp[0]["f_liscia"] if t0 == 0 else testa["campioni"][0]["f_liscia"]
            for t in range(t0 + 1, t1 + 1):
                AC.tick(z, t, K)
                if t == K:
                    mu_a, res_a = AC.mu_rayleigh(z, s)
                    psi_a = z["st"]["psi_h"].copy()
                    acc = {"t": t, "mu": mu_a, "residuo": res_a, "sha": SFM.sha(psi_a), "psi": psi_a}
                    acc_nuovo = acc
                    np.savez(f_acc.replace(".npz", "_tmp.npz"), psi_h=psi_a)
                    os.replace(f_acc.replace(".npz", "_tmp.npz"), f_acc)
                if t % V.OGNI == 0:
                    conti = LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO, par)
                    c = V.misura(z, t, w_in, w0, h, LC, conti, mas)
                    periodiche(z, c, conti, w_in, w0, h, t, LC, nome in CENTRO_LIBRO)
                    if giro is not None:
                        p = c["per"]
                        e1 = ((p["c1"] - giro["c"][0] + 0.5 * Lg) % Lg) - 0.5 * Lg
                        e2 = ((p["c2"] - giro["c"][1] + 0.5 * Lg) % Lg) - 0.5 * Lg
                        giro["X"] = (np.asarray(giro["X"]) + e1 * A1 + e2 * A2).tolist()
                        giro["c"] = [p["c1"], p["c2"]]
                        ts = t * s
                        if ts >= giro["a"] + BLOCCO:
                            media = giro["somma"] / giro["n"]
                            giro["chiusi"].append([giro["a"], media])
                            if media < META * giro["rif"]:
                                fermata = "(b) il cuore a blocchi sotto meta' (il blocco %g .. %g: %.5f contro %.5f)" % (giro["a"], giro["a"] + BLOCCO, media, META * giro["rif"])
                            giro["a"] += BLOCCO * math.floor((ts - giro["a"]) / BLOCCO)
                            giro["somma"], giro["n"] = 0.0, 0
                        giro["somma"] += p["f_liscia"]
                        giro["n"] += 1
                        cam = float(np.hypot(*(np.asarray(giro["X"]) - np.asarray(giro["X0"]))))
                        giro["cammino"] = cam
                        if fermata is None and cam >= CAMMINO[nome]:
                            fermata = "(a) lo spostamento srotolato dalla partenza arriva a %.2f (>= %g)" % (cam, CAMMINO[nome])
                    c["lam"] = AC.lam_di(t, K)
                    camp.append(c)
                    if c["f_liscia"] < META * f_lis0 and t_dis is None:
                        t_dis = t          # ### il primo; si interrompe solo nella rampa (A6)
                if mappe_on and t % MP.OGNI == 0:
                    ist.append(MP.istantanea(z, t, AC.lam_di(t, K), (camp[-1]["per"]["x"], camp[-1]["per"]["y"])))
                if t in tick_stati:
                    f_st = os.path.join(base_e(nome), "stati", nome, "%s_stato_%06d.npz" % (nome, t))
                    os.makedirs(os.path.dirname(f_st), exist_ok=True)
                    np.savez(f_st + ".tmp.npz", t=t, **{k: v for k, v in z["st"].items() if isinstance(v, np.ndarray)})
                    os.replace(f_st + ".tmp.npz", f_st)
                    stati.append({"t": t, "file": f_st, "sha": V.shas(z)})
                if t - DOPO_STATO in tick_stati:
                    dopo[str(t - DOPO_STATO)] = V.shas(z)
                if t % V.OGNI_D == 0:
                    dd.append(righe_D(bande, np.exp(1j * mu * s * t) * z["st"]["psi_h"] - p0, n0, t))
                    if acc is not None and t > acc["t"]:
                        da_.append(righe_D(bande, np.exp(1j * acc["mu"] * s * (t - acc["t"])) * z["st"]["psi_h"] - acc["psi"], float(np.linalg.norm(acc["psi"])), t))
                if (t_dis is not None and t_dis <= K) or fermata:
                    t1 = t
                    break
        mappe = None
        if mappe_on and ist:
            f_m = os.path.join(base_e(nome), "mappe", nome, "%s_%06d.npz" % (nome, t0))
            dim, sha = MP.scrivi(f_m, ist, np.asarray(z["m1"]), np.asarray(z["m2"]), z["L"])
            mappe = {"file": f_m, "byte": dim, "sha1": sha, "istantanee": len(ist)}
        sha_fine = V.shas(z)
        tmp = f_rip.replace(".npz", "_tmp.npz")
        np.savez(tmp, t=t1, **{k: v for k, v in z["st"].items() if isinstance(v, np.ndarray)})
    os.replace(tmp, f_rip)
    riga = {"nome": nome, "da": NOME, "sol": sol, "vuoto": vuoto, "s": s, "eps": V.EPS, "N": V.N, "L": V.L, "T_acc": T_acc, "K": K, "t0": t0, "t1": t1, "t_fine": t_fine,
            "t_dis": t_dis, "w_in": w_in, "h": h, "e_K": e_K, "info": info, "campioni": camp, "D": dd, "D_acc": da_, "sha_fine": sha_fine, "secondi": time.time() - s0,
            "acc": {k: v for k, v in acc_nuovo.items() if k != "psi"} if acc_nuovo else None,
            "tick": "accensione (sin^2 su T_acc, poi tick.percorri_tick)", "libro": "col par della corsa", "rampa": "lam_k = sin^2(pi k/(2 K))"}
    if mappe_on:
        riga.update({"mappe": mappe, "stati": stati, "dopo_stato": dopo, "disco": disco})
    if giro is not None:
        riga.update({"giro": giro, "fermata": fermata})
    f_int = os.path.join(dir_json(nome), "%s_%06d.jsonl" % (nome, t0))
    V.LP.scrivi_nuovo(f_int, riga)
    if nome in RADA:
        from solitone import mappe as MP
        rada = dict(riga)
        rada["campioni"] = [c for c in camp if c["t"] % OGNI_RADA == 0]
        rada["D"] = [d for d in dd if d["t"] % OGNI_RADA == 0]
        rada["D_acc"] = [d for d in da_ if d["t"] % OGNI_RADA == 0]
        rada["intera"] = {"file": f_int, "byte": os.path.getsize(f_int), "sha1": MP.sha1(f_int)}
        rada["rada"] = "un campione ogni %d tick dell'intera" % OGNI_RADA
        os.makedirs(RADA[nome], exist_ok=True)
        V.LP.scrivi_nuovo(os.path.join(RADA[nome], "%s_%06d.jsonl" % (nome, t0)), rada)
    print("  la corsa %s: il pezzo %d -> %d%s; lam %.4f; f_liscia %.5f (all'inizio %.5f), w %.4f, alone %.5f; %.0f s%s"
          % (nome, t0, t1, (", SCIOLTO NELLA RAMPA (f_liscia sotto meta')" if t_dis <= K else ", il cuore istantaneo sotto meta' della partenza a tempo %.1f" % (t_dis * s)) if t_dis is not None else "", camp[-1]["lam"], camp[-1]["f_liscia"], f_lis0, camp[-1]["w"], camp[-1]["alone"], time.time() - s0,
             ("; il cammino %.2f%s" % (giro.get("cammino", float("nan")), ("; FERMATA: " + fermata) if fermata else "")) if giro is not None else ""))
    gem = GEMELLE.get(nome)
    if gem:
        fg = os.path.join(dir_json(gem), "%s_%06d.jsonl" % (gem, t0))
        rg = V.LP.leggi(fg) if os.path.exists(fg) else None
        uguale = rg is not None and rg["sha_fine"] == V.LP.leggi(os.path.join(dir_json(nome), "%s_%06d.jsonl" % (nome, t0)))["sha_fine"] and rg["t1"] == t1
        print("  la corsa %s: lo sha_fine del pezzo %d %s" % (nome, t0, ("e' quello di %s, al bit" % gem) if uguale else "### NON e' quello di %s: FERMO" % gem))
        if not uguale:
            return 1
    return 0


# ------------------------------------------------------------------------------------------------ il referto
def serie(nome):
    rr = [__import__("_vuoto_vivo_B").LP.leggi(os.path.join(dir_json(nome), n)) for n in nomi(nome)]
    for a, b in zip(rr, rr[1:]):
        assert a["t1"] == b["t0"], "un buco fra i pezzi di %s" % nome
    return rr, [c for r in rr for c in r["campioni"]], [d for r in rr for d in r["D"]], [d for r in rr for d in r["D_acc"]]


def tabella(nome, camp, s):
    """### **La tabella a blocchi di `_respiro_congelato.blocchi`, fino all'ultimo campione** *(quella si ferma al suo `TAU_FINE`, e l'ultimo blocco prende il resto)*."""
    tt = np.array([c["t"] for c in camp]) * s
    fl = np.array([c["f_liscia"] for c in camp])
    ww = np.array([c["w"] for c in camp])
    al = np.array([c["alone"] for c in camp])
    xx = np.array([c["x"] for c in camp])
    yy = np.array([c["y"] for c in camp])
    print("### %s, a blocchi di %g (le medie; le pendenze per 1000 unita' di tempo; il baricentro: la distanza dalla posizione iniziale)" % (nome, BLOCCO))
    print("    %-17s %-9s %-9s %-11s %-10s %-14s %-14s %-9s" % ("il tempo", "cuore", "w", "cuore x w", "alone", "pend. alone", "pend. w", "baric."))
    a = 0.0
    while a <= tt[-1]:
        m = (tt >= a) & (tt < a + BLOCCO)
        if m.any():
            print("    %7.0f .. %7.0f %.5f   %.4f    %.5f     %.5f    %+.4e    %+.4e    %.4f"
                  % (a, a + BLOCCO, fl[m].mean(), ww[m].mean(), (fl[m] * ww[m]).mean(), al[m].mean(), 1000 * pendenza(tt[m], al[m]), 1000 * pendenza(tt[m], ww[m]),
                     math.hypot(xx[m].mean() - xx[0], yy[m].mean() - yy[0])))
        a += BLOCCO
    return tt, fl, ww, al


def pendenza(x, y):
    return float(np.polyfit(x, y, 1)[0]) if len(x) >= 3 else float("nan")


def bande_D(che, dd, s, istanti):
    if not dd:
        return
    td = np.array([d["t"] for d in dd]) * s
    for ist in istanti:
        d = dd[int(np.argmin(np.abs(td - ist)))]
        print("    %-26s a tempo %7.1f: |D|/|psi| %.4e; le bande %s" % (che, d["t"] * s, d["nD"], " ".join("%s %.4f" % (k, v) for k, v in sorted(d["bande"].items()))))


def referto():
    import _respiro_congelato as RC
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import misure as MI
    sol, vuoto, s = V.CORSE[NOME]
    print("=" * 130)
    print("L'ACCENSIONE LENTA DEL VUOTO (Luca 01:13, con le decisioni dopo 25614c34): %s dalla sua partenza, il vuoto acceso con lam = sin^2 su T_acc, poi il tick intero; confrontato con %s vivo"
          % (NOME, NOME))
    print("  la configurazione: CORSE %s BLOCCO %g META %g CODA %g; di _vuoto_vivo_B: PEZZO %d OGNI %d OGNI_D %d R_VICINO %g LAM_ZERO %g TOLL_NORMA %g; s %g eps %g N %.0e L %d; la soglia accessoria %g"
          % (CORSE, BLOCCO, META, CODA, V.PEZZO, V.OGNI, V.OGNI_D, V.R_VICINO, V.LAM_ZERO, V.TOLL_NORMA, s, V.EPS, V.N, V.L, MI.SOGLIA_VITA))
    print("  la vita principale (Luca, la precisazione della decisione 9): il tempo a cui il cuore liscio scende a META' del suo valore a T_acc, misurato o estrapolato (dichiarato); la soglia |D|/|psi| >= %g accessoria" % MI.SOGLIA_VITA)
    print("  ### il libro di BG-F-0.15 vivo e' a eps 0 blocco per blocco (_vuoto_vivo_B.corsa non passa il par): il confronto del libro e' fra conti diversi (Luca: si dichiara)")
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: (a1) dopo la rampa si assesta e perde piu' lentamente di BG-F; (a2) perde come BG-F: la perdita e' del vuoto vivo; (a3) T_acc 1000 e 2000 diversi: non ancora lenta; (a4) altro")
    print("=" * 130)
    cv, dv = RC.serie_viva()
    print("### %s VIVO (il riferimento: _vuoto_vivo_B + _respiro_sul_fondo)" % NOME)
    tv, flv, wwv, alv = RC.blocchi("VIVO", cv, s)
    res = {}
    for nome, (T_acc, tau_fine) in ((n, CORSE[n]) for n in CONFRONTO):
        print("-" * 130)
        rr, camp, dd, da = serie(nome)
        if not rr:
            print("### %s: NESSUN PEZZO" % nome)
            continue
        ult = rr[-1]
        sciolto = ult["t_dis"] is not None and ult["t_dis"] <= ult["K"]      # ### solo nella rampa la corsa si interrompe (dopo bfee5330)
        fatta = ult["t1"] >= ult["t_fine"] or sciolto
        acc = next((r["acc"] for r in rr if r.get("acc")), None)
        print("### %s (T_acc %g, fino a %g): %s; %d pezzi, %d campioni, %.0f s" % (nome, T_acc, tau_fine, ("SCIOLTO a tempo %.1f" % (ult["t_dis"] * s)) if sciolto
                                                                              else ("arriva a %g" % (ult["t1"] * s) if fatta else "### NON FINITA"), len(rr), len(camp), sum(r["secondi"] for r in rr)))
        if acc:
            print("    lo stato a T_acc (tick %d): mu di Rayleigh del tick intero %+.9f (la partenza %+.9f), il residuo per tick %.3e" % (acc["t"], acc["mu"], rr[0]["info"]["mu"], acc["residuo"]))
        tt, fl, ww, al = tabella(nome, camp, s)
        sciolto_rampa = ult["t_dis"] is not None and ult["t_dis"] <= rr[0]["K"]
        esito("DEVE PASSARE: A6 %s non si scioglie durante la rampa (altrimenti FERMO)" % nome, not sciolto_rampa, "")
        M = np.array([c["E"]["totale"]["M"] for c in camp])
        Vv = np.array([c["E"]["totale"]["V"] for c in camp])
        dM, dV = float(np.max(np.abs(M / M[0] - 1.0))), float(np.max(np.abs(Vv / Vv[0] - 1.0)))
        esito("DEVE PASSARE: A3 %s M e V entro %g" % (nome, V.TOLL_NORMA), dM <= V.TOLL_NORMA and dV <= V.TOLL_NORMA, "dM %.1e dV %.1e" % (dM, dV))
        esito("DEVE PASSARE: A4 %s il libro col par della corsa (eps %g)" % (nome, V.EPS), all(r.get("libro") == "col par della corsa" and r["eps"] == V.EPS for r in rr), "")
        esito("DEVE PASSARE: %s arriva alla fine o si scioglie" % nome, fatta, "")
        t_sotto = next((r["t_dis"] for r in rr if r["t_dis"] is not None), None)
        if t_sotto is not None and t_sotto > rr[0]["K"]:
            print("  il cuore ISTANTANEO scende sotto meta' di quello della partenza a tempo %.1f (dopo la rampa: la corsa prosegue, la decisione dopo bfee5330)" % (t_sotto * s))
        mc = tt <= CONFRONTO[nome]
        vm = AC.vita_a_meta(tt[mc], fl[mc], T_acc, META, CODA)
        res[nome] = {"vita": vm, "tt": tt, "fl": fl, "al": al, "T_acc": T_acc}
        m = (tt >= T_acc) & mc
        print("  (IL CRITERIO DI bfee5330, ISTANTANEO, SUPERATO DALLA DECISIONE DI LUCA; fino a %g) LA VITA PRINCIPALE: il cuore liscio" % CONFRONTO[nome] + " a T_acc %.5f; sotto %g x: %s; la pendenza del cuore negli ultimi %g %+.4e per 1000"
              % (vm["f0"], META, ("MISURATA a tempo %.1f" % vm["misurata"]) if vm["misurata"] else (("ESTRAPOLATA (non una misura) a tempo ~%.0f" % vm["estrapolata"]) if vm["estrapolata"] else "il cuore non cala: nessuna estrapolazione"), CODA, vm["pendenza"]))
        print("  le pendenze dopo la rampa (%g .. %g), per 1000: il cuore %+.4e, l'alone %+.4e, w %+.4e" % (T_acc, tt[m][-1], 1000 * pendenza(tt[m], fl[m]), 1000 * pendenza(tt[m], al[m]), 1000 * pendenza(tt[m], ww[m])))
        tdd = np.array([d["t"] for d in dd]) * s
        nd = np.array([d["nD"] for d in dd])
        ram = tdd <= T_acc
        v_r = MI.vita(tdd[ram], nd[ram])
        print("  LA SOGLIA ACCESSORIA (|D|/|psi| >= %g): sulla rampa, D rispetto alla partenza: %s" % (MI.SOGLIA_VITA, ("tempo %.1f" % v_r) if v_r is not None else "mai"))
        if da:
            tda = np.array([d["t"] for d in da]) * s
            nda = np.array([d["nD"] for d in da])
            v_a = MI.vita(tda, nda)
            print("                                         dopo, D rispetto allo stato a T_acc: %s (il primo campione %.4e a tempo %.1f)" % (("tempo %.1f" % v_a) if v_a is not None else "mai", nda[0], tda[0]))
        bande_D("D dalla partenza", dd, s, (0.25 * T_acc, 0.5 * T_acc, T_acc))
        bande_D("D dallo stato a T_acc", da, s, (T_acc + 500.0, T_acc + 2500.0, tau_fine))
    print("-" * 130)
    print("### IL CONFRONTO CON %s VIVO SULLE STESSE FINESTRE (le pendenze per 1000; la vita con lo stesso criterio, dal valore del vivo a T_acc)" % NOME)
    for nome, r in res.items():
        T_acc = r["T_acc"]
        mc = r["tt"] <= CONFRONTO[nome]
        tt = r["tt"][mc]
        mv = (tv >= T_acc) & (tv <= tt[-1])
        vv = AC.vita_a_meta(tv[tv <= tt[-1]], flv[tv <= tt[-1]], T_acc, META, CODA)
        m = tt >= T_acc
        print("  %s, %g .. %g: il cuore %+.4e (VIVO %+.4e); l'alone %+.4e (VIVO %+.4e); la vita a meta': %s (VIVO, dal suo cuore a T_acc %.5f: %s)"
              % (nome, T_acc, tt[-1], 1000 * pendenza(tt[m], r["fl"][mc][m]), 1000 * pendenza(tv[mv], flv[mv]), 1000 * pendenza(tt[m], r["al"][mc][m]), 1000 * pendenza(tv[mv], alv[mv]),
                 ("misurata %.1f" % r["vita"]["misurata"]) if r["vita"]["misurata"] else ("estrapolata ~%.0f" % r["vita"]["estrapolata"]) if r["vita"]["estrapolata"] else "--",
                 vv["f0"], ("misurata %.1f" % vv["misurata"]) if vv["misurata"] else ("estrapolata ~%.0f" % vv["estrapolata"]) if vv["estrapolata"] else "--"))
    vv0 = AC.vita_a_meta(tv, flv, 0.0, META, CODA)
    print("  VIVO dalla partenza (il cuore a 0 %.5f, fino a %g): %s" % (vv0["f0"], tv[-1], ("misurata %.1f" % vv0["misurata"]) if vv0["misurata"] else ("estrapolata ~%.0f" % vv0["estrapolata"]) if vv0["estrapolata"] else "--"))
    due_processi(res, tv, flv, alv)
    sul_toro()
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def periodiche(z, c, conti, w_in, w0, h, t, LC, centro_libro=False):
    """### **Le misure sul toro** *(Luca dopo `455b9a95`, punto `1`)* **accanto a quelle euclidee del campione `c`:** il centro periodico, cuore, `w`, alone,
    l'alone per settore; ### **il libro per settore ogni `LIBRO_SETTORI` tick** *(dichiarato nel task history, sez. `11`)*."""
    import _energia_del_legame as EL
    from solitone import toro as TO
    rho, _l = EL.densita(z["inc"], z["st"])
    p, D, M = TO.misure(rho, np.asarray(z["m1"]), np.asarray(z["m2"]), z["L"], w_in, w0, h)
    p["alone_set"] = TO.alone_settori(rho, D, M, w0)
    if t % LIBRO_SETTORI == 0:
        p["E_set"] = LC.per_regione(conti, TO.maschere_settori(D))
    if centro_libro:
        import _vuoto_vivo_B as V
        d = np.hypot(D[:, 0], D[:, 1])
        vic = d <= V.R_VICINO * w_in
        p["E_cen"] = LC.per_regione(conti, {"vicino": vic, "lontano": ~vic})     # ### Luca 18:12: il libro attorno al centro periodico
        p["alone_3w"] = 1.0 - float(rho[d <= 3.0 * p["w"]].sum()) / M          # ### Luca 18:18: l'alone a 3 w(t)
    c["per"] = p


def sul_toro():
    """### **La corsa `TP1000` col centro periodico** *(Luca dopo `455b9a95`)*: ### **i DEVE, la tabella a blocchi col criterio di validita', la vita sui blocchi
    validi, la deriva** *(la traiettoria srotolata, la velocita' per blocco, la direzione, la velocita' contro `w`, avanti e dietro)*."""
    import _libro_dei_conti as LC
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import toro as TO
    _sol, _vuoto, s = V.CORSE[NOME]
    nome = "TP1000"
    gem = GEMELLE[nome]
    T_acc, tau_fine = CORSE[nome]
    print("=" * 130)
    print("### LE MISURE SUL TORO (Luca, dopo 455b9a95): %s = %s rifatta DA 0 (in db/ c'e' solo l'ultimo stato), con il centro periodico accanto all'euclideo" % (nome, gem))
    print("    il centro: la media circolare sugli indici del reticolo; le distanze: l'immagine piu' vicina fra le 9; le misure: le stesse espressioni, cambia la distanza")
    print("    (Luca dopo 8e425771) il toro NON ha un bordo: cio' che rompeva le misure euclidee e' il TAGLIO DELLE COORDINATE (gli indici da -40 a +40); il crollo a 13500 di %s" % gem)
    print("    e' l'effetto della misura euclidea sul taglio. Il rombo e' uguale nelle tre direzioni: nessuna direzione del moto viene dalla forma del toro")
    rr, camp, _dd, _da = serie(nome)
    if not rr:
        print("### %s: NESSUN PEZZO" % nome)
        return
    L = rr[0]["L"]
    A1, A2 = TO.vettori()
    R = TO.meta_periodo(L)
    R_Y = float((L // 2) * A2[1])
    print("    IL CRITERIO DI VALIDITA' (decisione di Luca dopo 8e425771): 3 w < %.4f, la meta' del periodo piu' corto del toro (dai vettori del toro; i periodi sono lunghi %d)" % (R, L))
    print("    SOLO COME CONFRONTO: 3 w < %.4f, l'estensione in y della rappresentazione dei nodi (l'errore di lettura n.92, il \"mezzo lato corto\" di 455b9a95)" % R_Y)
    ult = rr[-1]
    fatta = ult["t1"] >= ult["t_fine"]
    print("### %s (T_acc %g, fino a %g): %s; %d pezzi, %d campioni, %.0f s" % (nome, T_acc, tau_fine, ("arriva a %g" % (ult["t1"] * s)) if fatta else "### NON FINITA", len(rr), len(camp),
                                                                     sum(r["secondi"] for r in rr)))
    M_ = np.array([c["E"]["totale"]["M"] for c in camp])
    V_ = np.array([c["E"]["totale"]["V"] for c in camp])
    dM, dV = float(np.max(np.abs(M_ / M_[0] - 1.0))), float(np.max(np.abs(V_ / V_[0] - 1.0)))
    esito("DEVE PASSARE: A3 %s M e V entro %g" % (nome, V.TOLL_NORMA), dM <= V.TOLL_NORMA and dV <= V.TOLL_NORMA, "dM %.1e dV %.1e" % (dM, dV))
    esito("DEVE PASSARE: A4 %s il libro col par della corsa (eps %g)" % (nome, V.EPS), all(r.get("libro") == "col par della corsa" and r["eps"] == V.EPS for r in rr), "")
    esito("DEVE PASSARE: %s arriva alla fine" % nome, fatta, "")
    rg, cg, _x, _y = serie(gem)
    gg = {r["t0"]: r for r in rg}
    diversi = [r["t0"] for r in rr if r["t0"] not in gg or gg[r["t0"]]["sha_fine"] != r["sha_fine"] or gg[r["t0"]]["t1"] != r["t1"]]
    chiavi = ("t", "x", "y", "w", "f_liscia", "f_win", "alone")
    camp_ug = len(cg) == len(camp) and all(a[k] == b[k] for a, b in zip(camp, cg) for k in chiavi)
    esito("DEVE PASSARE: TP1 ogni pezzo di %s ha lo sha_fine del pezzo di %s con lo stesso t0 (AL BIT, ogni chiave), e i campioni euclidei sono gli stessi AL BIT" % (nome, gem),
          not diversi and len(rr) == len(rg) and camp_ug, "pezzi %d e %d; diversi %s; i campioni %s" % (len(rr), len(rg), diversi or "nessuno", "uguali" if camp_ug else "### DIVERSI"))
    tt = np.array([c["t"] for c in camp]) * s
    per = [c["per"] for c in camp]
    prima = tt < TP_CENTRI
    dc = np.array([TO.distanza((p["x"], p["y"]), (c["x"], c["y"]), L) for c, p in zip(camp, per)])
    esito("DEVE PASSARE: TP2 prima di %g il centro periodico e l'euclideo coincidono entro %g" % (TP_CENTRI, TOLL_CENTRI), float(dc[prima].max()) <= TOLL_CENTRI,
          "il massimo %.4e (a tempo %.1f); dopo %g il massimo %.4e" % (dc[prima].max(), tt[prima][int(np.argmax(dc[prima]))], TP_CENTRI, dc[~prima].max() if (~prima).any() else float("nan")))
    fl = np.array([p["f_liscia"] for p in per])
    ww = np.array([p["w"] for p in per])
    al = np.array([p["alone"] for p in per])
    c1 = np.array([p["c1"] for p in per])
    c2 = np.array([p["c2"] for p in per])
    u1 = np.concatenate([[0.0], np.cumsum(((np.diff(c1) + 0.5 * L) % L) - 0.5 * L)])
    u2 = np.concatenate([[0.0], np.cumsum(((np.diff(c2) + 0.5 * L) % L) - 0.5 * L)])
    X = u1[:, None] * A1 + u2[:, None] * A2
    print("### %s, a blocchi di %g, COL CENTRO PERIODICO (le medie; la traiettoria SROTOLATA dalla partenza; v per 1000 unita' di tempo; l'angolo dall'asse x, e dalla" % (nome, BLOCCO))
    print("    direzione del reticolo piu' vicina (A1 0, A1+A2 60, A2 120 gradi); max 3w nel blocco; NV = il blocco non rispetta 3 w < %.2f, il criterio; NVy = 3 w >= %.2f, solo confronto)" % (R, R_Y))
    print("    %-17s %-9s %-9s %-9s %-17s %-8s %-11s %-8s %-8s %-8s %s" % ("il tempo", "cuore", "w", "alone", "il centro (x, y)", "dist.", "|v|", "angolo", "dal ret.", "max 3w", ""))
    blocchi = []
    a = 0.0
    while a <= tt[-1]:
        m = (tt >= a) & (tt < a + BLOCCO)
        if m.any():
            vx = 1000 * pendenza(tt[m], X[m, 0])
            vy = 1000 * pendenza(tt[m], X[m, 1])
            ang = math.degrees(math.atan2(vy, vx))
            m3 = 3.0 * float(ww[m].max())
            b = {"a": a, "m": m, "v": (vx, vy), "ang": ang, "m3": m3}
            blocchi.append(b)
            print("    %7.0f .. %7.0f %.5f   %-9.4f %.5f   (%7.2f, %6.2f) %-8.3f %-11.4e %-+8.1f %-+8.1f %-8.2f %s%s"
                  % (a, a + BLOCCO, fl[m].mean(), ww[m].mean(), al[m].mean(), X[m, 0].mean(), X[m, 1].mean(), float(np.hypot(X[m, 0], X[m, 1]).mean()), math.hypot(vx, vy), ang,
                     ((ang + 30.0) % 60.0) - 30.0, m3, "NV " if m3 >= R else "", "NVy" if m3 >= R_Y else ""))
        a += BLOCCO
    ang_tot = math.degrees(math.atan2(X[-1, 1], X[-1, 0]))
    ang_p = math.degrees(math.atan2(per[0]["y"], per[0]["x"]))
    print("  LA DIREZIONE (Luca dopo 8e425771: con gli assi del reticolo e con la partenza): lo spostamento totale srotolato (%.3f, %.3f), lungo %.3f, l'angolo %+.1f, dalla direzione"
          % (X[-1, 0], X[-1, 1], math.hypot(X[-1, 0], X[-1, 1]), ang_tot))
    print("    del reticolo piu' vicina %+.1f; la partenza: il centro periodico al primo campione (%.5f, %.5f) dal nodo d'origine, l'angolo %+.1f; la differenza %+.1f gradi"
          % (((ang_tot + 30.0) % 60.0) - 30.0, per[0]["x"], per[0]["y"], ang_p, ((ang_tot - ang_p + 180.0) % 360.0) - 180.0))
    for soglia, che in ((R, "3 w < %.2f (la meta' del periodo, il criterio)" % R), (R_Y, "3 w < %.2f (l'estensione in y, solo come confronto: n.92)" % R_Y)):
        nv = next((b["a"] for b in blocchi if b["m3"] >= soglia), None)
        t_val = nv if nv is not None else tt[-1] + 1.0
        print("  CON IL CRITERIO %s: %s" % (che, ("il primo blocco NON valido comincia a %g; la vita solo prima" % nv) if nv is not None else "tutti i blocchi validi fino alla fine"))
        m = (tt >= T_acc) & (tt < t_val)
        if m.sum() < 3:
            print("    nessun blocco valido dopo T_acc")
            continue
        vb = AC.vita_a_blocchi(tt[m], fl[m], T_acc, META, BLOCCO)
        print("    (1) il cuore a blocchi: il riferimento %.5f, la meta' %.5f: %s; la pendenza delle medie %+.4e per 1000; i blocchi validi %d" % (vb["rif"], META * vb["rif"],
              ("MISURATA, il blocco centrato a %.0f" % vb["misurata"]) if vb["misurata"] is not None else ("ESTRAPOLATA (non una misura) ~%.0f" % vb["estrapolata"]) if vb["estrapolata"] is not None
              else "le medie non calano: nessuna vita", vb["pendenza"], len(vb["blocchi"])))
        t_a, p_a, mis = AC.tempo_alone(tt[m], al[m], T_acc, tt[m][-1], QUOTA_ALONE)
        print("    (2) l'alone periodico: la pendenza %+.4e per 1000 (%g .. %g); al %g: %s" % (p_a, T_acc, tt[m][-1], QUOTA_ALONE,
              ("MISURATO a %.1f" % t_a) if mis else ("ESTRAPOLATO (non una misura) ~%.0f" % t_a) if t_a is not None else "l'alone non cresce: nessun tempo"))
    m = (tt >= FINESTRA[0]) & (tt <= FINESTRA[1])
    print("  L'ALONE PERIODICO su %g .. %g: %+.4e per 1000 (l'euclideo della stessa corsa %+.4e)" % (FINESTRA[0], FINESTRA[1], 1000 * pendenza(tt[m], al[m]),
          1000 * pendenza(tt[m], np.array([c["alone"] for c in camp])[m])))
    print("### LA DERIVA, AVANTI E DIETRO (per blocco: la direzione della velocita' del blocco; avanti = i %d settori a meno di 90 gradi, dietro gli altri; la risoluzione 45 gradi;" % (TO.SETTORI // 2))
    print("    l'alone per settore a ogni campione; il libro per settore ogni %d tick, tutto il settore, il solitone compreso; con |v| piccola la direzione e' rumore)" % LIBRO_SETTORI)
    centri = (np.arange(TO.SETTORI) + 0.5) * (2.0 * math.pi / TO.SETTORI)
    for b in blocchi:
        th = math.radians(b["ang"])
        av = np.cos(centri - th) > 0
        m = b["m"]
        aset = np.array([per[i]["alone_set"] for i in np.nonzero(m)[0]])
        a_av, a_di = float(aset[:, av].sum(axis=1).mean()), float(aset[:, ~av].sum(axis=1).mean())
        ee = [per[i]["E_set"] for i in np.nonzero(m)[0] if "E_set" in per[i]]
        lib = ""
        if ee:
            sv = {k: float(np.mean([sum(e["s%d" % j][k] for j in range(TO.SETTORI) if av[j]) for e in ee])) for k in LC.CONTI}
            sd = {k: float(np.mean([sum(e["s%d" % j][k] for j in range(TO.SETTORI) if not av[j]) for e in ee])) for k in LC.CONTI}
            lib = "; il libro (%d campioni) avanti - dietro: %s; M avanti %.1f dietro %.1f" % (len(ee), " ".join("%s %+.4e" % (k, sv[k] - sd[k]) for k in LC.CONTI), sv["M"], sd["M"])
        print("  %7.0f .. %7.0f |v| %.4e angolo %+6.1f: l'alone avanti %.5f dietro %.5f%s" % (b["a"], b["a"] + BLOCCO, math.hypot(*b["v"]), b["ang"], a_av, a_di, lib))


def due_processi(res, tv, flv, alv):
    """### **La decisione di Luca dopo `bfee5330`:** la vita dal cuore a blocchi *(l'allargamento dentro `B`)* e il tempo dell'alone al `10%` *(l'emissione
    fuori)*, per il vivo, `TA1000`, `TA2000`; ### **la barra: la dispersione delle tre pendenze dell'alone sulla finestra comune.**"""
    from solitone import accensione as AC
    print("=" * 130)
    print("### LA VITA, DUE PROCESSI (Luca, dopo bfee5330): (1) L'ALLARGAMENTO DENTRO B: il cuore liscio mediato a blocchi di %g, la meta' della media del primo blocco dopo T_acc" % BLOCCO)
    print("    (il vivo: dopo 0); misurata = il centro del primo blocco sotto meta'; altrimenti ESTRAPOLATA (non una misura) dalla retta delle medie; solo i blocchi completi")
    print("    (2) L'EMISSIONE FUORI: il tempo a cui la retta dell'alone (dopo T_acc, fino alla fine della corsa) arriva al %g della materia; ESTRAPOLATO (non una misura)" % QUOTA_ALONE)
    righe = [("VIVO", 0.0, tv, flv, alv)] + [(n, r["T_acc"], r["tt"], r["fl"], r["al"]) for n, r in res.items()]
    for nome, tau0, tt, fl, al in righe:
        vb = AC.vita_a_blocchi(tt, fl, tau0, META, BLOCCO)
        print("  %s (da %g a %g): le medie del cuore a blocchi: %s" % (nome, tau0, tt[-1], "; ".join("%g..%g %.5f" % b for b in vb["blocchi"])))
        print("    (1) il riferimento %.5f, la meta' %.5f: %s; la pendenza delle medie %+.4e per 1000" % (vb["rif"], META * vb["rif"],
              ("MISURATA, il blocco centrato a %.0f" % vb["misurata"]) if vb["misurata"] is not None else ("ESTRAPOLATA (non una misura) ~%.0f" % vb["estrapolata"]) if vb["estrapolata"] is not None
              else "le medie non calano: nessuna vita", vb["pendenza"]))
        t_a, p_a, mis = AC.tempo_alone(tt, al, tau0, tt[-1], QUOTA_ALONE)
        print("    (2) l'alone: la pendenza %+.4e per 1000, l'ultimo campione %.5f; al %g: %s" % (p_a, al[-1], QUOTA_ALONE,
              ("MISURATO a %.1f" % t_a) if mis else ("ESTRAPOLATO (non una misura) ~%.0f" % t_a) if t_a is not None else "l'alone non cresce: nessun tempo"))
    pp = []
    for nome, _tau0, tt, _fl, al in righe:
        m = (tt >= FINESTRA[0]) & (tt <= FINESTRA[1])
        pp.append(1000 * pendenza(tt[m], al[m]))
        print("  LA BARRA: %s, l'alone su %g .. %g: %+.4e per 1000 (%d campioni)" % (nome, FINESTRA[0], FINESTRA[1], pp[-1], int(m.sum())))
    pp = np.array(pp)
    print("  LA BARRA (la stima, dichiarata): la media %+.4e, la deviazione standard (n - 1) %.4e, cioe' %.1f%% della media; ### e' la dispersione delle tre pendenze stesse:"
          % (pp.mean(), pp.std(ddof=1), 100 * pp.std(ddof=1) / abs(pp.mean())))
    print("    dire che stanno nella barra e' quasi vero per costruzione; tre numeri, una stima grezza")


def ripartenza(nome):
    """### **Il DEVE della ripartenza** *(Luca dopo `3e3277a2`)*: ### **da ciascuno stato salvato, `DOPO_STATO` tick col tick della corsa, e gli `sha` di ogni chiave
    contro quelli registrati in corsa.** La scena si prepara con le stesse chiamate di `corsa`, poi lo stato si carica. `[(t, letto al bit, dopo al bit)]`."""
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import protetto as P
    T_acc, _fine = CORSE[nome]
    sol, vuoto, s = V.CORSE[NOME]
    K = int(round(T_acc / s))
    rr = [V.LP.leggi(os.path.join(dir_json(nome), n)) for n in nomi(nome)]
    stati = [x for r in rr for x in (r.get("stati") or [])]
    dopo = {}
    for r in rr:
        dopo.update(r.get("dopo_stato") or {})
    out = []
    with V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        w0 = rec["larghezza"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, w0)
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        P.e_K(z)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        for k, v in salvato.items():
            z["st"][k][...] = v
        for x in stati:
            with np.load(x["file"]) as d:
                assert int(d["t"]) == x["t"]
                for k in z["st"]:
                    if isinstance(z["st"][k], np.ndarray):
                        z["st"][k][...] = d[k]
            letto = V.shas(z) == x["sha"]
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                for t in range(x["t"] + 1, x["t"] + DOPO_STATO + 1):
                    AC.tick(z, t, K)
            out.append((x["t"], letto, str(x["t"]) in dopo and V.shas(z) == dopo[str(x["t"])]))
    return out


def file_e(nome):
    """### **I file della corsa su `E:`:** `(mappe, stati, campioni)`, ciascuno ordinato."""
    import glob
    return (sorted(glob.glob(os.path.join(base_e(nome), "mappe", nome, "%s_*.npz" % nome))), sorted(glob.glob(os.path.join(base_e(nome), "stati", nome, "%s_stato_*.npz" % nome))),
            sorted(glob.glob(os.path.join(dir_json(nome), "%s_*.jsonl" % nome))))


def indice(nome="TM1000"):
    """### **L'indice dei file su `E:`** *(Luca `15:49`)*: per ogni file il percorso, la dimensione, lo `sha1`, l'intervallo di tempo."""
    import _vuoto_vivo_B as V
    from solitone import mappe as MP
    s = V.CORSE[NOME][2]
    mm, ss, cc = file_e(nome)
    print("L'INDICE DEI FILE SU E: DELLA CORSA %s (Luca 15:49 e dopo 3e3277a2): il percorso, la dimensione, lo sha1 (dei byte), l'intervallo di tempo" % nome)
    print("### LE MAPPE (rho e Lambda in float32, ogni %d tick)" % MP.OGNI)
    for f in mm:
        print("  " + MP.riga_indice(f, s))
    print("### GLI STATI COMPLETI (ogni chiave dello stato, per ripartire al bit)")
    for f in ss:
        with np.load(f) as d:
            t = int(d["t"])
        print("  %s  %d byte  sha1 %s  tempo %.2f (tick %d)" % (f, os.path.getsize(f), MP.sha1(f), t * s, t))
    print("### I PEZZI DEI CAMPIONI (jsonl interi%s)" % (", doppioni al bit di %s" % GEMELLE[nome] if nome in GEMELLE else "; nel repo la versione rada in %s" % RADA.get(nome, "--")))
    for f in cc:
        r = V.LP.leggi(f)
        print("  %s  %d byte  sha1 %s  tempo %.2f .. %.2f" % (f, os.path.getsize(f), MP.sha1(f), r["t0"] * s, r["t1"] * s))


def verifica_mappe(nome="TM1000"):
    """### **Il referto di `TM1000`:** i DEVE del mandato delle mappe e della decisione dopo `3e3277a2`."""
    import _vuoto_vivo_B as V
    from solitone import mappe as MP
    s = V.CORSE[NOME][2]
    gem = GEMELLE[nome]
    print("=" * 130)
    print("LE MAPPE E GLI STATI (Luca 15:49 e dopo 3e3277a2): %s = %s ripetuta con le mappe ogni %d tick e gli stati completi a %s su %s" % (nome, gem, MP.OGNI, STATI[nome], RADICE_E))
    print("  i campioni di %s stanno su E: (doppioni al bit di %s); nel repo l'indice doc/referti_l2/mappe_indice.txt e questo referto" % (nome, gem))
    print("=" * 130)
    rr, camp, _dd, _da = serie(nome)
    rg, cg, _x, _y = serie(gem)
    ult = rr[-1] if rr else None
    fatta = ult is not None and ult["t1"] >= ult["t_fine"]
    print("### %s: %s; %d pezzi, %d campioni, %.0f s" % (nome, "arriva a %g" % (ult["t1"] * s) if fatta else "### NON FINITA", len(rr), len(camp), sum(r["secondi"] for r in rr)))
    esito("DEVE PASSARE: %s arriva alla fine" % nome, fatta, "")
    disco = [r.get("disco") for r in rr if r.get("disco")]
    esito("DEVE PASSARE: K1 prima di cominciare il disco esiste, e' scrivibile, con lo spazio libero almeno %d volte la stima" % MP.VOLTE_SPAZIO, bool(disco) and disco[0]["ok"],
          disco[0]["nota"] if disco else "nessuna registrazione")
    M_ = np.array([c["E"]["totale"]["M"] for c in camp])
    V_ = np.array([c["E"]["totale"]["V"] for c in camp])
    dM, dV = float(np.max(np.abs(M_ / M_[0] - 1.0))), float(np.max(np.abs(V_ / V_[0] - 1.0)))
    esito("DEVE PASSARE: A3 %s M e V entro %g" % (nome, V.TOLL_NORMA), dM <= V.TOLL_NORMA and dV <= V.TOLL_NORMA, "dM %.1e dV %.1e" % (dM, dV))
    esito("DEVE PASSARE: A4 %s il libro col par della corsa (eps %g)" % (nome, V.EPS), all(r.get("libro") == "col par della corsa" and r["eps"] == V.EPS for r in rr), "")
    gg = {r["t0"]: r for r in rg}
    diversi = [r["t0"] for r in rr if r["t0"] not in gg or gg[r["t0"]]["sha_fine"] != r["sha_fine"] or gg[r["t0"]]["t1"] != r["t1"]]
    chiavi = ("t", "x", "y", "w", "f_liscia", "f_win", "alone")
    camp_ug = len(cg) == len(camp) and all(a[k] == b[k] for a, b in zip(camp, cg) for k in chiavi) and all(a["per"] == b["per"] for a, b in zip(camp, cg))
    esito("DEVE PASSARE: MP1 con il salvataggio acceso gli sha_fine dei pezzi sono quelli di %s (AL BIT, ogni chiave), e i campioni sono gli stessi AL BIT" % gem,
          not diversi and len(rr) == len(rg) and camp_ug, "pezzi %d e %d; diversi %s; i campioni %s" % (len(rr), len(rg), diversi or "nessuno", "uguali" if camp_ug else "### DIVERSI"))
    per_t = {c["t"]: c for c in camp}
    mm, ss, _cc = file_e(nome)
    eM, eV, n_ist, mancano = 0.0, 0.0, 0, 0
    for f in mm:
        d = MP.leggi(f)
        for i, t in enumerate(d["t"]):
            c = per_t.get(int(t))
            if c is None:
                mancano += 1
                continue
            eM = max(eM, abs(float(d["rho"][i].astype(np.float64).sum()) / c["E"]["totale"]["M"] - 1.0))
            eV = max(eV, abs(float(d["Lambda"][i].astype(np.float64).sum()) / c["E"]["totale"]["V"] - 1.0))
            n_ist += 1
    esito("DEVE PASSARE: K2 ogni istantanea riletta: sum rho = M e sum Lambda = V del campione allo stesso t, entro 1e-6 relativo (float32)",
          n_ist > 0 and mancano == 0 and eM <= 1e-6 and eV <= 1e-6, "%d istantanee in %d file; il peggiore M %.2e, V %.2e; senza campione %d" % (n_ist, len(mm), eM, eV, mancano))
    rip = ripartenza(nome)
    esito("DEVE PASSARE: ST1 ogni stato salvato si rilegge AL BIT (gli sha registrati), e ripartendo per %d tick ridà AL BIT lo stato della corsa" % DOPO_STATO,
          len(rip) == len(STATI[nome]) and all(a and b for _t, a, b in rip), "; ".join("tick %d: letto %s, dopo %s" % (t, "al bit" if a else "### NO", "al bit" if b else "### NO") for t, a, b in rip))
    print("  i file: %d mappe (%d byte), %d stati (%d byte); l'indice: python csv/solitone/corsa_accensione.py --indice > doc/referti_l2/mappe_indice.txt"
          % (len(mm), sum(os.path.getsize(f) for f in mm), len(ss), sum(os.path.getsize(f) for f in ss)))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def main(argv):
    import _presidio
    for m in ("__init__", "misure", "protetto", "accensione", "toro", "mappe"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    if "--corsa" in argv:
        sys.exit(corsa(argv[argv.index("--corsa") + 1]))
    elif "--referto" in argv:
        referto()
    elif "--mappe" in argv:
        verifica_mappe()
    elif "--indice" in argv:
        i = argv.index("--indice")
        indice(argv[i + 1] if len(argv) > i + 1 else "TM1000")
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
