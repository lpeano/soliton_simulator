# -*- coding: utf-8 -*-
r"""**LO STRUMENTO DELLA NOTTE: LE CORSE CHE SI FERMANO E RIPARTONO** *(Luca `2026-11-16` `20:35`; la carta `doc/TASK_HISTORY/2026-11-16_notte_verifica.md`)*.

    E:\python\py3132\python.exe csv/solitone/notte.py avvio --nome V-B2 --tipo coppia --L 297 --d 35 --fase 0 --R_A 85.06
    E:\python\py3132\python.exe csv/solitone/notte.py avvio --nome V-T120 --tipo triangolo --L 339 --R_A 97.16
    E:\python\py3132\python.exe csv/solitone/notte.py corsa --nome V-B2 --da ultimo --fino 12000 --ferma-alle 2026-11-17T08:00 --registro notte-V-B2

### **`avvio`:** **la costruzione di `mattone_coppia_L162.main`** *(la coppia, con le sostituzioni di `verifica_coppie`: la scena di `L`, il bordo da `R_A`, i centri a `d/2` lungo `A1`, per `pi` il francobollo B con `psi -> -psi`)* **o di `triangolo_120.corsa`** *(il triangolo: la scena di `L` per la CORSA, la scena VERA di `L 162` per il FRANCOBOLLO; `mattone_triangolo.R_A_SCENA = R_A`)*, **intercettata in `Corsa.inizio(0)`:** **R-SCATOLA al `5%` a tre clausole** *(se cade: niente stato, la corsa NON parte; N5)*, **poi lo stato a `k 0` nell'archivio, e si esce senza un tick.**
### **`corsa`:** **il ciclo di `legati.coppia` / `legati.triangolo` COPIATO** *(le stesse misure; la coppia in piu' `d` ogni `10` tick come `mattone_coppia_L162`)*; **lo stato ogni `--ogni` tick** *(`250`)* **con lo sha1 accanto; a ogni stato il PEZZO** *(la serie, le mappe, i conti dei tick `(k_prima, k]`)*; **le etichette alla cadenza ASSOLUTA e, alla ripresa, quelle del `meta`; la fermata a ora o sotto `MEM_MIN_GB`: lo stato a quel `k`, il pezzo, la voce del registro chiusa «SOSPESA».**
### **L'archivio:** `E:\soliton_simulator\notte\<nome>\` *(`scena.json`, `stato_<k>.npz` + `.sha1`, `pezzo_<da>_<a>.npz`)*.
"""
import argparse
import datetime
import glob
import hashlib
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
import mattone as MT  # noqa: E402
import mattone_cottura as CT  # noqa: E402

ARCHIVIO = r"E:\soliton_simulator\notte"
OGNI_MISURA, OGNI_MAPPA, R_FORMA = 50, 100, 60.0
FATTORE_GAUSS = 10.0
TIENI = 2
CODICE = "csv/solitone/notte.py"
_Corsa = CT.Corsa


class Avviato(Exception):
    pass


class FermoScatola(Exception):
    pass


def cartella(nome):
    return os.path.join(ARCHIVIO, nome)


def sha1_file(f):
    h = hashlib.sha1()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def f_stato(nome, k):
    return os.path.join(cartella(nome), "stato_%05d.npz" % k)


def salva_stato(nome, Z, C, k, t, centri, lab_cen):
    """### Lo stato completo *(le chiavi della scena, il campo, il `meta`)*, poi lo sha1 dei byte ACCANTO *(R3)*."""
    import _vuoto_vivo_B as V
    f = f_stato(nome, k)
    np.savez(f, meta=np.array(json.dumps({"k": k, "t": t, "sha": V.shas(Z["z"]), "codice": CODICE, "centri": centri, "lab_cen": lab_cen})),
             campo_A=C.campo.A, campo_E=C.campo.E, **{x: Z["st"][x] for x in Z["chiavi"]})
    s = sha1_file(f)
    with open(f + ".sha1", "w", encoding="utf-8", newline=chr(10)) as fh:
        fh.write(s + chr(10))
    return f, s


def stati_integri(nome):
    """### Gli stati dal piu' recente, con lo sha1 RICALCOLATO: `[(k, file, sha1, integro)]`."""
    out = []
    for f in sorted(glob.glob(os.path.join(cartella(nome), "stato_*.npz")), reverse=True):
        k = int(os.path.basename(f)[6:11])
        try:
            with open(f + ".sha1", encoding="utf-8") as fh:
                atteso = fh.read().strip()
        except OSError:
            atteso = None
        s = sha1_file(f)
        out.append((k, f, s, atteso is not None and s == atteso))
    return out


def scegli_stato(nome, da):
    """### R3: lo stato da cui si riparte. `da` un numero: quello, se integro, altrimenti il precedente integro; `ultimo`: il piu' recente integro."""
    tutti = stati_integri(nome)
    for k, f, s, ok in tutti:
        if da != "ultimo" and k > int(da):
            continue
        if ok:
            return k, f, s
        print("### R3: lo stato %s NON e' integro (lo sha1 %s non coincide con quello scritto): NON si riparte da li', si prende quello prima" % (os.path.basename(f), s[:8]))
    return None


def pota(nome, k_ora, ogni):
    """### Tiene gli ultimi `TIENI` stati e i multipli di `1000`."""
    ks = sorted(int(os.path.basename(f)[6:11]) for f in glob.glob(os.path.join(cartella(nome), "stato_*.npz")))
    for k in ks[:-TIENI]:
        if k % 1000 != 0 and k < k_ora:
            for g in (f_stato(nome, k), f_stato(nome, k) + ".sha1"):
                if os.path.exists(g):
                    os.remove(g)


def leggi_scena(nome):
    with open(os.path.join(cartella(nome), "scena.json"), encoding="utf-8") as fh:
        return json.load(fh)


def presidi():
    import _presidio
    for m in ("mattone", "mattone_cottura", "mattone_coppia_L162", "legati", "triangolo_120", "mattone_triangolo", "triangolo_video", "convergenza", "prova_scatola5"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)


# =====================================================================================
#   AVVIO
# =====================================================================================
def avvio(nome, tipo, L, R_A, d, fase):
    import convergenza as CV
    import prova_scatola5 as PS5
    from solitone import bordo as BO
    presidi()
    os.makedirs(cartella(nome), exist_ok=True)
    if glob.glob(os.path.join(cartella(nome), "stato_*.npz")):
        print("### FERMO: l'archivio %s ha gia' degli stati: l'avvio NON si rifa' (si riprende con corsa --da)" % cartella(nome))
        return 1
    vera_scena, vera_g = MT.scena, BO.g_estremita
    salvati = [(MT, "scena", MT.scena), (BO, "g_estremita", BO.g_estremita), (CT, "Corsa", CT.Corsa), (MT, "incolla", MT.incolla), (MT, "tappa", MT.tappa)]
    stato = {"francobollo": 0, "c0": None, "incollature": 0, "prima": True}
    esito = {}

    def g_estremita(z, c1, c2, R_A_, g_max):
        return vera_g(z, c1, c2, R_A if z["L"] == L else R_A_, g_max)

    def scena_nuova():
        ctx = CV.scena_L(L, R_A)

        class Avvolto(object):
            def __enter__(self_):
                Z = ctx.__enter__()
                stato["c0"] = Z["bordo"]["c0"]
                return Z

            def __exit__(self_, *a):
                return ctx.__exit__(*a)
        return Avvolto()

    def controlla_e_salva(R, k, t, centri, lab_cen):
        Z = R.Z
        Rm, rr, b = PS5.r5(Z, t)
        print("### l'oggetto incollato: i raggi %s attorno al baricentro (%.2f, %.2f); R_ogg al 5%% %.1f" % (", ".join("%g%% %s" % (100 * s, rr[s]) for s in sorted(rr, reverse=True)), b[0], b[1], Rm))
        if not PS5.regola(Z, Rm, "a k %d, %s" % (k, nome)):
            raise FermoScatola("R-SCATOLA al 5%% NON rispettata a k 0 (R_ogg %.1f): la corsa NON parte (N5)" % Rm)
        g0 = R.C.residuo()
        f, s = salva_stato(nome, Z, R.C, k, t, centri, lab_cen)
        esito.update(R_ogg5=Rm, g0=g0, file=f, sha1=s)
        print("### LO STATO A k 0: %s, sha1 %s; il residuo di Gauss %.3e" % (f, s, g0))
        raise Avviato()

    MT.tappa = lambda n_, testo: None
    BO.g_estremita = g_estremita
    try:
        if tipo == "coppia":
            import mattone_coppia_L162 as MCL
            from solitone import carta_coppia as CC
            from solitone import toro as TO
            mondo = "N%dd%d%s" % (L, int(round(d)), "pi" if fase == "pi" else "")
            MCL.MONDI[mondo] = "MGU"
            MT.scena = lambda corsa, t: scena_nuova() if corsa == MCL.CORSA_C else vera_scena(corsa, t)
            vero_cs = CC.centri_semipiani
            salvati.append((CC, "centri_semipiani", vero_cs))

            def centri_semipiani(rho, m1, m2, L_, xx, soglia):
                if stato["prima"]:
                    stato["prima"] = False
                    c0 = stato["c0"]
                    A1, A2 = TO.vettori()
                    a1 = np.linalg.solve(np.column_stack([A1, A2]), A1 * (d / 2.0))
                    return np.array([c0[0] - a1[0], c0[1] - a1[1]]), np.array([c0[0] + a1[0], c0[1] + a1[1]])
                return vero_cs(rho, m1, m2, L_, xx, soglia)
            CC.centri_semipiani = centri_semipiani
            vero_inc = MT.incolla

            def incolla(Z, fr, c, allinea):
                stato["incollature"] += 1
                if fase == "pi" and stato["incollature"] == 2:
                    fr = dict(fr)
                    fr["psi"] = -fr["psi"]
                return vero_inc(Z, fr, c, allinea)
            MT.incolla = incolla

            class CorsaAvvio(_Corsa):
                def inizio(self, k):
                    _Corsa.inizio(self, k)
                    Z = self.Z
                    c0 = Z["bordo"]["c0"]
                    xs = TO.scarti(Z["m1"], Z["m2"], c0[0], c0[1], Z["L"])[:, 0]
                    a, b = vero_cs(MT.rho_di(Z), Z["m1"], Z["m2"], Z["L"], xs, 0.0)
                    ab = [list(map(float, a)), list(map(float, b))]
                    controlla_e_salva(self, k, MCL.T_C + k, ab, ab)
            CT.Corsa = CorsaAvvio
            T_BASE = MCL.T_C
            print("### L'AVVIO DI %s: la coppia d %g, fase %s, L %d, il bordo da R_A %g; mattone_coppia_L162.main col mondo %s, intercettata in Corsa.inizio(0)" % (nome, d, fase, L, R_A, mondo))
            sys.stdout.flush()
            MCL.main(["--mondo", mondo])
        else:
            import mattone_triangolo as MTR
            import triangolo_120 as T120
            import triangolo_video as TV
            salvati += [(MTR, "R_A_SCENA", MTR.R_A_SCENA), (TV, "francobollo_L162", TV.francobollo_L162), (T120, "CorsaT120", T120.CorsaT120), (T120, "vertici", T120.vertici)]
            MTR.R_A_SCENA = R_A
            vero_fr, vero_vert = TV.francobollo_L162, T120.vertici

            def francobollo_L162(k):
                stato["francobollo"] += 1
                try:
                    return vero_fr(k)
                finally:
                    stato["francobollo"] -= 1
            TV.francobollo_L162 = francobollo_L162
            MT.scena = lambda corsa, t: scena_nuova() if (corsa == MT.CORSA_162 and stato["francobollo"] == 0) else vera_scena(corsa, t)

            def vertici(c0, fr, L_):
                V = vero_vert(c0, fr, L_)
                stato["V"] = [list(map(float, v)) for v in V]
                return V
            T120.vertici = vertici
            Base = T120.CorsaT120

            class CorsaAvvio(Base):
                def inizio(self, k):
                    Base.inizio(self, k)
                    cen, _lab = MTR.centri_pezzi(self.Z, MT.rho_di(self.Z), stato["V"])
                    cen = [list(map(float, c)) for c in cen]
                    controlla_e_salva(self, k, MT.G2.T0 + k, cen, cen)
            T120.CorsaT120 = CorsaAvvio
            T_BASE = MT.G2.T0
            print("### L'AVVIO DI %s: il triangolo a 120, L %d, il bordo da R_A %g; triangolo_120.corsa (mattone_triangolo.main) intercettata in Corsa.inizio(0)" % (nome, L, R_A))
            sys.stdout.flush()
            T120.corsa([])
        print("### FERMO: la costruzione e' finita SENZA arrivare a Corsa.inizio(0)")
        return 1
    except Avviato:
        pass
    except FermoScatola as z:
        print("### FERMO: %s" % z)
        return 2
    finally:
        for mod, att, v in salvati:
            setattr(mod, att, v)
    sc = {"nome": nome, "tipo": tipo, "L": L, "R_A": R_A, "d": d, "fase": fase, "t_base": T_BASE, "g0": esito["g0"], "soglia_gauss": FATTORE_GAUSS * esito["g0"],
          "R_ogg5_k0": esito["R_ogg5"], "stato_k0": esito["file"], "sha1_k0": esito["sha1"], "codice": CODICE}
    with open(os.path.join(cartella(nome), "scena.json"), "w", encoding="utf-8", newline=chr(10)) as fh:
        json.dump(sc, fh, indent=1)
    print("### L'AVVIO FATTO: %s" % json.dumps(sc))
    return 0


# =====================================================================================
#   CORSA
# =====================================================================================
def corsa(nome, da, k_fino, ogni, ferma_alle, ferma_al_k, reg):
    import convergenza as CV
    import legati as LG
    import prova_scatola5 as PS5
    from solitone import _registro_corse as RC
    from solitone import bordo as BO
    from solitone import toro as TO
    presidi()
    t00 = time.time()
    sc = leggi_scena(nome)
    tipo, L, R_A, T_BASE = sc["tipo"], sc["L"], sc["R_A"], sc["t_base"]
    scelto = scegli_stato(nome, da)
    if scelto is None:
        print("### FERMO: nessuno stato integro da cui ripartire (--da %s)" % da)
        return 1
    k_da, f_da, s_da = scelto
    if da != "ultimo" and k_da != int(da):
        print("### R3: lo stato %d chiesto NON c'e' o non e' integro: si riparte da %d" % (int(da), k_da))
    with np.load(f_da) as dd:
        meta = json.loads(str(dd["meta"]))
    print("=" * 130)
    print("LA NOTTE (Luca 20:35), %s: %s su L %d, il bordo da R_A %g; da k %d (%s, sha1 %s, ricontrollato) a k %d; lo stato ogni %d; la fermata %s; la soglia di Gauss %.3e (%g volte il residuo a k 0)"
          % (nome, tipo, L, R_A, k_da, os.path.basename(f_da), s_da[:8], k_fino, ogni, ferma_alle or (("al k %d (prova)" % ferma_al_k) if ferma_al_k else "nessuna"), sc["soglia_gauss"], FATTORE_GAUSS))
    print("=" * 130)
    sys.stdout.flush()
    for f in glob.glob(os.path.join(cartella(nome), "pezzo_*.npz")):
        a = int(os.path.basename(f)[6:11])
        if a >= k_da:
            os.replace(f, f + ".scartato")
            print("### il pezzo %s comincia a/oltre k %d: SCARTATO (rinominato)" % (os.path.basename(f), k_da))
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    if tipo == "triangolo":
        import mattone_triangolo as MTR
        import triangolo_120 as T120
        import triangolo_video as TV
        MTR.R_A_SCENA = R_A
    limite = None
    if ferma_alle:
        limite = datetime.datetime.fromisoformat(ferma_alle)
    with CV.scena_L(L, R_A) as Z:
        m1, m2, n, righe = Z["m1"], Z["m2"], Z["n"], Z["righe"]
        c0 = Z["bordo"]["c0"]
        Z["g_e"] = BO.g_estremita(Z["z"], c0[0], c0[1], R_A, Z["bordo"]["g_max"])[0]
        xs = TO.scarti(m1, m2, c0[0], c0[1], L)[:, 0]
        r_c0 = np.hypot(*TO.scarti(m1, m2, c0[0], c0[1], L).T[:2])
        C, _m = LG.carica(Z, f_da, rho_c, e)
        R = CT.Corsa(Z, C)
        R.etichette([np.array(c) for c in meta["lab_cen"]] if tipo == "coppia" else meta["lab_cen"])
        vivo = {"cen": meta["centri"], "lab_cen": meta["lab_cen"], "k_pezzo": k_da, "T0": 0}
        B = {}

        def nuovo_buffer():
            B.clear()
            B["S"] = {}
            B["PK"] = []
            B["MP"] = {"k": [], "rho": [], "dphi": [], "E": []}
            B["regola"] = []
            vivo["T0"] = len(R.T["k"])
            if tipo == "triangolo":
                vivo["giro0"] = {x: len(v) for x, v in T120.GIRO.items()}
                vivo["foto0"] = {x: len(v) for x, v in TV.FOTO.items()}

        def metti(x, v):
            B["S"].setdefault(x, []).append(v)

        def misura(k):
            rho = MT.rho_di(Z)
            if tipo == "coppia":
                B["PK"].append(float(rho.max()))
                if k % CT.OGNI == 0:
                    a, b = _cs(rho, m1, m2, L, xs)
                    metti("t10", k)
                    metti("d10", float(np.hypot(*_vettore(a, b, L))))
                fare, mappa = k % OGNI_MISURA == 0, k % OGNI_MAPPA == 0
                if fare or mappa:
                    phi0 = BO.c_di(T_BASE + k, Z["tab_c"], Z["K"], Z["omega"]) * Z["phi_v"]
                    dphi = np.sqrt(np.sum(np.abs(Z["st"]["phi_h"] - phi0).reshape(n * 6, -1) ** 2, axis=1))
                    dphi_n = np.sqrt(np.sum(dphi[righe] ** 2, axis=1))
                if fare:
                    a, b = _cs(rho, m1, m2, L, xs)
                    bc = TO.centro(rho, m1, m2, L)[:2]
                    pos = TO.scarti(m1, m2, bc[0], bc[1], L)[:, :2]
                    r = np.hypot(pos[:, 0], pos[:, 1])
                    th = np.arctan2(pos[:, 1], pos[:, 0])
                    dentro = r <= R_FORMA
                    metti("k", k)
                    metti("d", float(np.hypot(*_vettore(a, b, L))))
                    metti("b1", bc[0])
                    metti("b2", bc[1])
                    metti("raggio", float(math.sqrt(np.sum(rho[dentro] * r[dentro] ** 2) / np.sum(rho[dentro]))))
                    metti("A2", float(abs(np.sum(rho[dentro] * np.exp(2j * th[dentro]))) / np.sum(rho[dentro])))
                    metti("M", float(rho.sum()))
                    metti("fuori", float(rho[r_c0 > R_A].sum() / rho.sum()))
                    metti("gauss", C.residuo() if k % MT.OGNI_GAUSS == 0 else float("nan"))
                    msk = xs < 0.0
                    for q, sel in (("A", msk), ("B", ~msk)):
                        u = TO.centro(np.where(sel, dphi_n, 0.0), m1, m2, L)[:2]
                        metti("u1_" + q, u[0])
                        metti("u2_" + q, u[1])
                    if k % 500 == 0:
                        print("    k %5d  d %.4f  il raggio %.4f  A2 %.4f  il picco %.4e  la massa %.6e  oltre R_A %.3e  Gauss %s  (%.0f s)" % (k, B["S"]["d"][-1], B["S"]["raggio"][-1], B["S"]["A2"][-1], B["PK"][-1], B["S"]["M"][-1],
                              B["S"]["fuori"][-1], "%.2e" % B["S"]["gauss"][-1] if B["S"]["gauss"][-1] == B["S"]["gauss"][-1] else "--", time.time() - t00))
                        sys.stdout.flush()
                if mappa:
                    B["MP"]["k"].append(k)
                    B["MP"]["rho"].append(rho.astype(np.float32))
                    B["MP"]["dphi"].append(dphi_n.astype(np.float32))
                    B["MP"]["E"].append(np.sqrt(np.sum(C.campo.E.reshape(n, 3) ** 2, axis=1)).astype(np.float32))
            else:
                vivo["cen"], lab = MTR.centri_pezzi(Z, rho, vivo["cen"])
                B["PK"].append([float(rho[lab == j].max()) for j in range(3)])
                if k % OGNI_MISURA == 0:
                    c_ = vivo["cen"]
                    metti("k", k)
                    for j, nn in enumerate("ABC"):
                        metti("M_" + nn, float(rho[lab == j].sum()))
                        metti("raggio_" + nn, MTR.MR.raggio(Z, rho, c_[j]))
                        metti("c1_" + nn, c_[j][0])
                        metti("c2_" + nn, c_[j][1])
                    metti("l_AB", MT.distanza(L, c_[0], c_[1]))
                    metti("l_BC", MT.distanza(L, c_[1], c_[2]))
                    metti("l_CA", MT.distanza(L, c_[2], c_[0]))
                    metti("gauss", C.residuo() if k % MT.OGNI_GAUSS == 0 else float("nan"))
                T120.misura_extra(Z, C, k, T_BASE + k, R.lab, R.n_sol, (lambda kk, tt: TV.CorsaVideo.foto(R, kk, tt)) if k % OGNI_MAPPA == 0 else None, k % T120.OGNI_GIRO == 0)
                if k % 500 == 0 and k % OGNI_MISURA == 0:
                    print("    k %5d  lati %.4f %.4f %.4f  masse %s  oltre R_A %.3e  Gauss %s  (%.0f s)" % (k, B["S"]["l_AB"][-1], B["S"]["l_BC"][-1], B["S"]["l_CA"][-1], " ".join("%.6e" % B["S"]["M_" + nn][-1] for nn in "ABC"),
                          T120.GIRO["fuori"][-1], "%.2e" % B["S"]["gauss"][-1] if B["S"]["gauss"][-1] == B["S"]["gauss"][-1] else "--", time.time() - t00))
                    sys.stdout.flush()

        def salva(k, perche):
            Rm, _rr, _b = PS5.r5(Z, T_BASE + k)
            ok_r = PS5.regola(Z, Rm, "%s a k %d" % (nome, k))
            B["regola"].append([k, Rm, 1.0 if ok_r else 0.0])
            f, s = salva_stato(nome, Z, C, k, T_BASE + k, vivo["cen"] if tipo == "triangolo" else meta["centri"], vivo["lab_cen"])
            pz = {("S_" + x): np.array(v) for x, v in B["S"].items()}
            pz["PK"] = np.array(B["PK"])
            pz["regola"] = np.array(B["regola"])
            for x, v in R.T.items():
                pz["T_" + x] = np.array(v[vivo["T0"]:])
            if B["MP"]["k"]:
                pz.update(MP_k=np.array(B["MP"]["k"], dtype=np.int32), MP_rho=np.stack(B["MP"]["rho"]), MP_dphi=np.stack(B["MP"]["dphi"]), MP_E=np.stack(B["MP"]["E"]))
            if tipo == "triangolo":
                for x, v in T120.GIRO.items():
                    if len(v) > vivo["giro0"][x]:
                        pz["GIRO_" + x] = np.array(v[vivo["giro0"][x]:])
                for x, v in TV.FOTO.items():
                    if len(v) > vivo["foto0"].get(x, 0):
                        pz["FOTO_" + x] = np.stack(v[vivo["foto0"].get(x, 0):]) if x != "k" else np.array(v[vivo["foto0"].get(x, 0):])
                for x in list(TV.FOTO):
                    del TV.FOTO[x][:]
            fp = os.path.join(cartella(nome), "pezzo_%05d_%05d.npz" % (vivo["k_pezzo"], k))
            np.savez_compressed(fp, **pz)
            pota(nome, k, ogni)
            print("    [stato] k %d (%s): %s sha1 %s; il pezzo %s; R_ogg al 5%% %.1f" % (k, perche, os.path.basename(f), s[:8], os.path.basename(fp), Rm))
            sys.stdout.flush()
            vivo["k_pezzo"] = k
            vivo["ultimo"] = (k, f, s)
            nuovo_buffer()

        R.inizio(k_da)
        nuovo_buffer()
        if k_da == 0:
            vivo["T0"] = 0                      # ### la riga di inizio(0) e' della corsa; alla ripresa quella di inizio(k_da) NON entra nel pezzo (c'e' gia' nel pezzo prima)
            misura(0)
        t1 = t_tappa = time.time()
        fine = "finita a k %d" % k_fino
        codice = 0
        k = k_da
        for k in range(k_da + 1, k_fino + 1):
            R.passo(k, T_BASE + k, 1.0, e)
            if k % CT.OGNI == 0:
                if tipo == "coppia":
                    a, b = _cs(MT.rho_di(Z), m1, m2, L, xs)
                    vivo["lab_cen"] = [list(map(float, a)), list(map(float, b))]
                    R.etichette([a, b])
                else:
                    vivo["lab_cen"] = [list(map(float, c)) for c in vivo["cen"]]
                    R.etichette(vivo["cen"])
            misura(k)
            adesso = time.time()
            ora = datetime.datetime.now()
            sospendi = (limite is not None and ora >= limite) or (ferma_al_k is not None and k == ferma_al_k)
            if k % ogni == 0 or k == k_fino or sospendi:
                salva(k, "la fermata" if sospendi and k % ogni and k != k_fino else "il passo")
            if reg and adesso - t_tappa >= MT.TAPPA_S:
                mem = MT.memoria_gb()
                u = vivo.get("ultimo")
                t_tappa = adesso
                try:
                    RC.tappa(reg, "k %d; %.3f s per tick; la memoria libera %.2f GB; l'ultimo stato %s" % (k, (adesso - t1) / max(1, k - k_da), mem, ("k %d %s sha1 %s" % u) if u else "nessuno dopo la partenza"))
                except RC.Rifiuto as z:
                    if not (k % ogni == 0 or k == k_fino or sospendi):
                        salva(k, "la voce chiusa")
                    fine, codice = "la voce %s del registro rifiuta la tappa (%s): salvato e uscito a k %d" % (reg, z, k), 5
                    break
                if mem < MT.MEM_MIN_GB:
                    if not (k % ogni == 0 or k == k_fino or sospendi):
                        salva(k, "la memoria")
                    fine, codice = "la memoria libera %.2f GB sotto %g GB a k %d" % (mem, MT.MEM_MIN_GB, k), 4
                    break
            if sospendi:
                fine, codice = ("SOSPESA alle %s a k %d" % (ora.strftime("%H:%M:%S"), k)) if limite is not None and ora >= limite else ("fermata di prova a k %d" % k), 3
                break
        print("-" * 130)
        print("### %d tick in %.0f s (%.3f s per tick); %s" % (k - k_da, time.time() - t1, (time.time() - t1) / max(1, k - k_da), fine))
        sys.stdout.flush()
    u = vivo.get("ultimo")
    if reg and u and (codice == 4 or (codice == 3 and limite is not None)):
        RC.chiudi(reg, "FERMATO", "%s per ordine di Luca (20:33), da riprendere: %s; l'ultimo stato k %d, %s, sha1 %s; si riprende con notte.py corsa --nome %s --da %d"
                  % ("SOSPESA" if codice == 3 else "FERMATA (la memoria)", fine, u[0], u[1], u[2], nome, u[0]))
    print("### L'ULTIMO STATO: k %d, %s, sha1 %s" % u if u else "### nessuno stato salvato dopo la partenza")
    return codice


def _cs(rho, m1, m2, L, xs):
    from solitone import carta_coppia as CC
    return CC.centri_semipiani(rho, m1, m2, L, xs, 0.0)


def _vettore(a, b, L):
    from solitone import carta_coppia as CC
    return CC.vettore(a, b, L)


def main(argv):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("avvio")
    a.add_argument("--nome", required=True)
    a.add_argument("--tipo", required=True, choices=("coppia", "triangolo"))
    a.add_argument("--L", type=int, required=True)
    a.add_argument("--R_A", type=float, required=True)
    a.add_argument("--d", type=float, default=0.0)
    a.add_argument("--fase", choices=("0", "pi"), default="0")
    c = sub.add_parser("corsa")
    c.add_argument("--nome", required=True)
    c.add_argument("--da", required=True)
    c.add_argument("--fino", type=int, required=True)
    c.add_argument("--ogni", type=int, default=250)
    c.add_argument("--ferma-alle")
    c.add_argument("--ferma-al-k", type=int)
    c.add_argument("--registro")
    x = ap.parse_args(argv)
    if x.cmd == "avvio":
        return avvio(x.nome, x.tipo, x.L, x.R_A, x.d, x.fase)
    return corsa(x.nome, x.da, x.fino, x.ogni, x.ferma_alle, x.ferma_al_k, x.registro)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
