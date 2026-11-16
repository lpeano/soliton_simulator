# -*- coding: utf-8 -*-
r"""**IL MATTONE BEN COTTO** *(Luca `2026-11-14` `09:34`, A1-A2, C6; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `15`)*.

    python csv/solitone/mattone_cottura.py cuoci --caso MGU --registro cottura-<caso> > <scratchpad>/cottura_<caso>.txt   (poi doc/referti_l2/mattone/cottura_<caso>.txt)
    python csv/solitone/mattone_cottura.py letture > doc/referti_l2/mattone/s5p_letture.txt        (S5' dalle serie salvate; nessuna corsa)
    python csv/solitone/mattone_cottura.py raggio_rhoc > doc/referti_l2/mattone/rhoc_raggio.txt    (C6, n.156: la lettura sul raggio; nessuna corsa)

### **`cuoci`:** **(1) il DEVE della ripartenza: da `<caso>_04000` `1000` tick = `<caso>_05000` AL BIT** *(tutte le chiavi, e `campo_A`, `campo_E`)*; **(2) da `<caso>_05000` a pezzi di `1000` tick a
campi pieni** *(la stessa legge, lo stesso `rho_c`, `e*`)*, **lo stato a fine pezzo su E:; «COTTO» quando fra due pezzi consecutivi DELLA COTTURA la media del picco cambia meno del `2%` E quella del
raggio meno dell'`1%`; al piu' `10` pezzi.** **Il tick e' quello di `mattone.Campi.tick` COPIATO in `Corsa.passo`** *(per misurare `tot` PRIMA e DOPO il bordo: il DEVE della ripartenza ne prova la
fedelta')*. **Il respiro, il picco, il raggio, il centro ogni `10` tick; `tot` e i pezzi a ogni tick** *(R-CONTI; l'energia come MEDIA sugli ultimi `100` tick)*.
### **S5'** *(A2)*: **in ogni finestra di `250` tick** *(estremi compresi)* **si toglie la retta dei minimi quadrati di quella finestra, poi il picco-picco; il respiro = il MASSIMO delle ultime quattro.**
"""
import argparse
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
import conti as CO  # noqa: E402
import mattone as MT  # noqa: E402
import mattone_rhoc as MR  # noqa: E402

CASI = ("MGU",)                         # ### Luca 09:38: SOLO il mondo G+U ((MG) tolto); (MU) si salta (09:34)
K_VER, K0 = 4000, 5000                  # ### il DEVE della ripartenza: 04000 -> 05000
PEZZO, MAX_PEZZI = 1000, 10             # ### A1: pezzi di 1000 tick, al piu' 10000 in piu'
SOGLIA_PICCO, SOGLIA_RAGGIO = 0.02, 0.01   # ### A1: «COTTO»
OGNI = 10                               # ### mia scelta (sez. 15): il respiro ogni 10 tick
FIN = 250                               # ### A2: le finestre di S5'
MEDIA_E = 100                           # ### C5: l'energia in MEDIA su 100 tick
OGNI_CONTI = 500                        # ### R-CONTI: le tabelle ogni 500 tick
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
#   S5'
# =====================================================================================
def finestre_s5(kk, R, inizio, fine):
    """### **S5':** per ogni finestra `[a, a + 250]` *(estremi compresi)* da `inizio` a `fine`: il picco-picco del respiro SENZA la retta della finestra. `[(a, b, ampiezza)]`."""
    kk, R = np.asarray(kk, dtype=float), np.asarray(R, dtype=float)
    out = []
    for a in range(int(inizio), int(fine), FIN):
        ii = (kk >= a) & (kk <= a + FIN)
        p = np.polyfit(kk[ii], R[ii], 1)
        q = R[ii] - np.polyval(p, kk[ii])
        out.append((a, a + FIN, float(q.max() - q.min())))
    return out


def s5p(kk, R, fine):
    """### **Il respiro S5':** il MASSIMO delle ultime quattro finestre prima di `fine`."""
    ff = finestre_s5(kk, R, fine - 4 * FIN, fine)
    return max(f[2] for f in ff), ff


# =====================================================================================
#   LA CORSA: il tick di mattone.Campi COPIATO, coi conti prima e dopo il bordo
# =====================================================================================
class Corsa(object):
    """### **Il tick e i conti per tick** *(R-CONTI)*: `passo(k, t, r, e)` = `mattone.Campi.tick` COPIATO, con `tot`, `K + V` e la massa PRIMA e DOPO il bordo, e i pezzi *(per le etichette `lab`)*."""

    def __init__(self, Z, C):
        self.Z, self.C = Z, C
        self.lab = None
        self.n_sol = 1
        self.T = {k: [] for k in ("k", "totp", "totd", "KVp", "KVd", "Mp", "Md", "mat", "vuo")}

    def kv(self):
        return (self.C.campo.K() + self.C.campo.V()) if self.C.campo is not None else 0.0

    def etichette(self, centri):
        self.n_sol = len(centri)
        self.lab = CO.etichette(self.Z, centri)

    def pezzi(self, c):
        idx = np.where(self.lab < 0, self.n_sol, self.lab)          # ### i solitoni 0 ... n-1, poi FUORI
        mat = np.bincount(idx, weights=c["cost"] + c["cin"] + c["leg"], minlength=self.n_sol + 1)
        vuo = np.bincount(idx, weights=c["vuo"], minlength=self.n_sol + 1)
        return mat, vuo

    def registra(self, k, totp, KVp, Mp):
        c = CO.conti_nodo(self.Z)
        mat, vuo = self.pezzi(c)
        T = self.T
        T["k"].append(k)
        T["totp"].append(totp)
        T["totd"].append(float(np.sum(c["tot"])))
        T["KVp"].append(KVp)
        T["KVd"].append(self.kv())
        T["Mp"].append(Mp)
        T["Md"].append(float(np.sum(np.abs(self.Z["st"]["psi_h"]) ** 2)))
        T["mat"].append(mat)
        T["vuo"].append(vuo)

    def inizio(self, k):
        """### lo stato di partenza: prima = dopo."""
        tot = float(np.sum(CO.conti_nodo(self.Z)["tot"]))
        self.registra(k, tot, self.kv(), float(np.sum(np.abs(self.Z["st"]["psi_h"]) ** 2)))

    def passo(self, k, t, r, e):
        """### **`mattone.Campi.tick` COPIATO** *(le stesse righe, nello stesso ordine)*, **coi conti prima e dopo il bordo.**"""
        from solitone import _u1_oggi as UO
        from solitone import bordo as BO
        from solitone import tick_lapse as TL
        C, Z = self.C, self.Z
        if C.campo is not None:
            if e > 0.0 and C.e_prec == 0.0:
                rho = MT.rho_di(Z)
                C.campo.A[...] = 0.0
                C.campo.E[...] = C.gauss(e * (rho - rho.mean()))
            elif C.e_prec > 0.0:
                C.campo.E *= e / C.e_prec
            C.campo.e = e
            C.e_prec = e
        if C.caso == "MG":
            with MT.PBR.con_rampa(r):
                TL.tick(Z["mot"], Z["st"], Z["par"], Z["s"], C.legge, eps_a=C.e0)
        elif C.caso == "MU":
            UO.tick(Z["z"], t, Z["K"], C.campo, True)
        else:
            with MT.PBR.con_rampa(r):
                MT.PBR.tick_GU(Z["z"], Z["s"], C.legge, C.e0, C.campo)
        totp = float(np.sum(CO.conti_nodo(Z)["tot"]))                  # ### IN PIU': i conti PRIMA del bordo
        KVp, Mp = self.kv(), float(np.sum(np.abs(Z["st"]["psi_h"]) ** 2))
        rho_prima = MT.rho_di(Z) if C.campo is not None and C.campo.e > 0.0 else None
        BO.assorbi(Z["st"], Z["g_e"], BO.c_di(t, Z["tab_c"], Z["K"], Z["omega"]) * Z["phi_v"])
        if rho_prima is not None:
            drho = MT.rho_di(Z) - rho_prima
            C.campo.E += C.gauss(C.campo.e * (drho - drho.mean()))
        self.registra(k, totp, KVp, Mp)                                # ### IN PIU': i conti DOPO il bordo

    def tabella(self, nomi, ogni=OGNI_CONTI):
        """### **La TABELLA DEI CONTI** *(R-CONTI-1)*: all'inizio, ogni `500` tick e alla fine; **l'energia come MEDIA sugli ultimi `100` tick** *(C5; all'inizio il valore dello stato)*."""
        T = {k: np.array(v) for k, v in self.T.items()}
        kk = T["k"]
        E = T["totd"] + T["KVd"]
        bordoE = np.cumsum(T["totp"] + T["KVp"] - T["totd"] - T["KVd"])
        bordoM = np.cumsum(T["Mp"] - T["Md"])
        res = E - E[0] + bordoE
        k0 = int(kk[0])
        punti = [k0] + [k for k in range(k0 + ogni, int(kk[-1]) + 1, ogni)]
        if punti[-1] != int(kk[-1]):
            punti.append(int(kk[-1]))
        print("### LA TABELLA DEI CONTI (R-CONTI-1; l'energia MEDIA sugli ultimi %d tick, C5; la materia = cost + cin + leg, il vuoto = vuo, per pezzo entro %g nodi; il bordo cumulato)" % (MEDIA_E, CO.R_PEZZO))
        print("    %7s  %s  %s  %10s  %16s  %12s  %12s  %12s" % ("k", "  ".join("%13s" % ("materia " + x) for x in nomi + ["fuori"]), "  ".join("%11s" % ("vuoto " + x) for x in nomi + ["lontano"]),
                                                              "K + V", "tot", "bordo E", "residuo", "bordo M"))
        for p in punti:
            i = int(np.nonzero(kk == p)[0][0])
            ii = slice(max(1, i - MEDIA_E + 1), i + 1) if i > 0 else slice(0, 1)
            mat = T["mat"][ii].mean(axis=0)
            vuo = T["vuo"][ii].mean(axis=0)
            print("    %7d  %s  %s  %10.4e  %16.6f  %+12.4f  %+12.4f  %12.4e" % (p, "  ".join("%13.6e" % v for v in mat), "  ".join("%11.4e" % v for v in vuo), float(T["KVd"][ii].mean()),
                                                                          float(T["totd"][ii].mean()), bordoE[i], float(res[ii].mean()), bordoM[i]))
        return res


def carica(Z, caso, rho_c, k):
    """### Lo stato `<caso>_<k>` su E:, nella scena; i campi di `mattone.Campi` con `e = e*` e `e_prec = e*` *(come `prepara` a campi pieni)*."""
    f = os.path.join(MT.DIR_E, "%s_%05d.npz" % (caso, k))
    with np.load(f) as d:
        Z["metti"]({kk: d[kk].copy() for kk in Z["chiavi"]})
        campo = (d["campo_A"].copy(), d["campo_E"].copy()) if "campo_A" in d.files else None
    C = MT.Campi(Z, caso, rho_c, MT.PB.E_DECISO)
    if C.campo is not None:
        C.campo.A[...] = campo[0]
        C.campo.E[...] = campo[1]
        C.campo.e = MT.PB.E_DECISO
        C.e_prec = MT.PB.E_DECISO
    return C, f


def uguale_al_file(Z, C, f):
    with np.load(f) as d:
        div = [k for k in Z["chiavi"] if not np.array_equal(Z["st"][k], d[k])]
        if C.campo is not None:
            div += [k for k, a in (("campo_A", C.campo.A), ("campo_E", C.campo.E)) if not np.array_equal(a, d[k])]
    return div


def cuoci(caso, nome_reg):
    import _presidio
    import _vuoto_vivo_B as V
    for m in ("mattone", "mattone_rhoc", "conti"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    assert caso in CASI
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO if caso == "MGU" else 0.0
    print("=" * 130)
    print("LA COTTURA (%s; Luca 09:34, A1): da %s_%05d a campi pieni su L 81, pezzi di %d tick, al piu' %d; COTTO: il picco medio entro %g e il raggio medio entro %g fra due pezzi; rho_c %.6f; e %.7e"
          % (caso, caso, K0, PEZZO, MAX_PEZZI, SOGLIA_PICCO, SOGLIA_RAGGIO, rho_c, e))
    print("=" * 130)
    S = {k: [] for k in ("k", "rmax", "resp", "raggio", "c1", "c2", "M")}
    fermo = None
    with MT.scena(MT.CORSA_BASE, MT.T_BASE) as Z:
        # ---------------------------------------------------------------- (1) il DEVE della ripartenza
        C, f4 = carica(Z, caso, rho_c, K_VER)
        R = Corsa(Z, C)
        R.etichette([MT.centro_di(Z, MT.rho_di(Z))])
        R.inizio(K_VER)
        t1 = time.time()
        for k in range(K_VER + 1, K0 + 1):
            rr = MT.r_di(k)
            R.passo(k, MT.T_BASE + k, rr, rr * MT.PB.E_DECISO if caso == "MGU" else 0.0)
            if k % OGNI == 0:
                R.etichette([MT.centro_di(Z, MT.rho_di(Z))])
        f5 = os.path.join(MT.DIR_E, "%s_%05d.npz" % (caso, K0))
        div = uguale_al_file(Z, C, f5)
        print("### la ripartenza: %s -> %d tick (%.0f s) -> confrontato con %s" % (f4, K0 - K_VER, time.time() - t1, f5))
        esito("la ripartenza da %s_%05d per %d tick = %s_%05d AL BIT (tutte le chiavi%s)" % (caso, K_VER, K0 - K_VER, caso, K0, " e il campo" if C.campo is not None else ""), not div,
              "diverse: %s" % div, True)
        if div:
            print("ESITO: ### FERMO: la ripartenza NON e' esatta; %d/%d" % (OK[0], OK[1]))
            return 1
        # ---------------------------------------------------------------- (2) la cottura
        C, _f = carica(Z, caso, rho_c, K0)
        R = Corsa(Z, C)

        def misura(k):
            rho = MT.rho_di(Z)
            c = MT.centro_di(Z, rho)
            S["k"].append(k)
            S["rmax"].append(float(rho.max()))
            S["resp"].append(MT.respiro(rho))
            S["raggio"].append(MR.raggio(Z, rho, c))
            S["c1"].append(c[0])
            S["c2"].append(c[1])
            S["M"].append(float(rho.sum()))
            R.etichette([c])
        misura(K0)
        R.inizio(K0)
        pezzi = []
        cotto, k = False, K0
        t1 = t_tappa = time.time()
        for j in range(1, MAX_PEZZI + 1):
            for k in range(K0 + (j - 1) * PEZZO + 1, K0 + j * PEZZO + 1):
                R.passo(k, MT.T_BASE + k, 1.0, e)
                if k % OGNI == 0:
                    misura(k)
                adesso = time.time()
                if adesso - t_tappa >= MT.TAPPA_S:
                    mem = MT.memoria_gb()
                    MT.tappa(nome_reg, "k %d; %.3f s per tick; la memoria libera %.2f GB" % (k, (adesso - t1) / (k - K0), mem))
                    t_tappa = adesso
                    if mem < MT.MEM_MIN_GB:
                        fermo = "la memoria libera %.2f GB sotto %g GB a k %d" % (mem, MT.MEM_MIN_GB, k)
                if adesso - t1 > MT.TETTO_S:
                    fermo = "il tetto di %g s a k %d" % (MT.TETTO_S, k)
                if fermo:
                    break
            if fermo:
                print("### FERMO: %s" % fermo)
                break
            f = os.path.join(MT.DIR_E, "%s_%05d.npz" % (caso, k))
            dati = {kk: Z["st"][kk] for kk in Z["chiavi"]}
            if C.campo is not None:
                dati.update(campo_A=C.campo.A, campo_E=C.campo.E)
            np.savez(f, meta=np.array(json.dumps({"caso": caso, "k": k, "t": MT.T_BASE + k, "r": 1.0, "e": e, "rho_c": rho_c, "sha": V.shas(Z["z"]), "codice": "csv/solitone/mattone_cottura.py"})), **dati)
            kk = np.array(S["k"])
            ii = (kk > k - PEZZO) & (kk <= k)
            mp, mr = float(np.mean(np.array(S["rmax"])[ii])), float(np.mean(np.array(S["raggio"])[ii]))
            s5, _ff = s5p(kk, S["resp"], k)
            pezzi.append((k, mp, mr, s5))
            riga = "### il pezzo %d (fino a k %d, %.0f s): il picco medio %.4e, il raggio medio %.4f, S5' %.4f; lo stato %s" % (j, k, time.time() - t1, mp, mr, s5, f)
            if j >= 2:
                dp, dr = abs(mp - pezzi[-2][1]) / pezzi[-2][1], abs(mr - pezzi[-2][2]) / pezzi[-2][2]
                cotto = dp < SOGLIA_PICCO and dr < SOGLIA_RAGGIO
                riga += "; contro il pezzo prima: il picco %.4f, il raggio %.4f -> %s" % (dp, dr, "COTTO" if cotto else "non ancora")
            print(riga)
            sys.stdout.flush()
            if cotto:
                break
        print("-" * 130)
        R.tabella(["sol"])
    # ---------------------------------------------------------------- il referto
    kk = np.array(S["k"])
    os.makedirs(MT.DIR_REF, exist_ok=True)
    np.savez_compressed(os.path.join(MT.DIR_REF, "cottura_%s_serie.npz" % caso), **{x: np.array(v) for x, v in S.items()})
    print("### R-CONTI-3: la deriva del centro, il picco, il raggio ogni %d tick" % OGNI_CONTI)
    for p in range(K0, int(kk[-1]) + 1, OGNI_CONTI):
        i = int(np.nonzero(kk == p)[0][0])
        print("    k %6d  il centro (%.4f, %.4f), la deriva da k %d %.4f nodi; il picco %.4e; il raggio %.4f; la massa %.10e"
              % (p, S["c1"][i], S["c2"][i], K0, MT.distanza(81, (S["c1"][i], S["c2"][i]), (S["c1"][0], S["c2"][0])), S["rmax"][i], S["raggio"][i], S["M"][i]))
    kf = int(kk[-1])
    s5, ff = s5p(kk, S["resp"], kf)
    k50 = kk % 50 == 0
    s5_50, _ff = s5p(kk[k50], np.array(S["resp"])[k50], kf)
    print("### S5' del mattone cotto (le ultime quattro finestre): %s -> %.4f; sulla serie presa ogni 50 tick %.4f" % (" ".join("%d-%d %.4f" % f for f in ff), s5, s5_50))
    esito_cotto = cotto and fermo is None
    with open(os.path.join(MT.DIR_REF, "cottura_%s.json" % caso), "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"caso": caso, "k": kf, "file": os.path.join(MT.DIR_E, "%s_%05d.npz" % (caso, kf)), "cotto": esito_cotto, "s5p": s5, "s5p_50": s5_50,
                   "pezzi": pezzi, "fermo": fermo, "codice": "csv/solitone/mattone_cottura.py"}, fh, indent=1)
    print("=" * 130)
    print("ESITO: %s a k %d (%d tick in piu'); %d/%d controlli come devono; fallite %s; %.0f s in tutto" % ("COTTO" if esito_cotto else "### NON COTTO", kf, kf - K0, OK[0], OK[1], FALLITE, time.time() - t00))
    return 0 if (esito_cotto and not FALLITE) else 1


# =====================================================================================
#   LE LETTURE (A2) E IL RAGGIO (C6): nessuna corsa
# =====================================================================================
def letture():
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("S5' DALLE SERIE SALVATE (Luca 09:34, A2; n.155): in ogni finestra di %d tick la retta tolta, poi il picco-picco; il respiro = il MASSIMO delle ultime quattro; accanto il vecchio (picco-picco su 1000 tick)" % FIN)
    print("=" * 130)
    vecchio_MG = None
    for caso in ("MG", "MU", "MGU", "MGdoppio", "MGmezzo"):
        s = np.load(os.path.join(MT.DIR_REF, "%s_serie.npz" % caso))
        kk, R = s["k"], s["resp"]
        ult = kk >= kk[-1] - MT.N_PIENO
        old = float(R[ult].max() - R[ult].min())
        v, ff = s5p(kk, R, int(kk[-1]))
        if caso == "MG":
            vecchio_MG = (old, v)
        print("    (%-8s) a k %d: S5' %.4f (le finestre %s); il vecchio %.4f" % (caso, int(kk[-1]), v, " ".join("%d-%d %.4f" % f for f in ff), old))
    s = np.load(os.path.join(MT.DIR_REF, "ctrl2_MG_serie.npz"))
    v, ff = s5p(s["k"], s["respiro"], 1250)
    ii = (s["k"] >= 250) & (s["k"] <= 1250)
    print("    (ctrl2_MG) S7' sui tick 250-1250: S5' %.4f (le finestre %s); il vecchio picco-picco %.4f" % (v, " ".join("%d-%d %.4f" % f for f in ff), float(s["respiro"][ii].max() - s["respiro"][ii].min())))
    print("    ### con S5' il controllo S7' di (MG) darebbe il rapporto %.3f (descrittivo: S7' e' chiuso, il giudizio nuovo e' S7'' sul mattone COTTO)" % (v / vecchio_MG[1]))
    print("-" * 130)
    esito("S5' di (MG) a 5000 ricalcolato dalla serie salvata, accanto al vecchio 0.0711 (il vecchio riletto dalla stessa serie)", "%.4f" % vecchio_MG[0] == "0.0711" and vecchio_MG[1] == vecchio_MG[1],
          "il vecchio %.4f, S5' %.4f" % vecchio_MG, True)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite %s" % (OK[0], OK[1], FALLITE))
    return 0 if not FALLITE else 1


def raggio_rhoc():
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("I MATTONI CON rho_c DIVERSO, LA LETTURA SUL RAGGIO (Luca 09:34, C6; l'errore del guardiano n.156: la lettura L4 era costruita su A, che satura a 1)")
    print("=" * 130)
    mg = np.load(os.path.join(MT.DIR_REF, "MG_raggio.npz"))["dati"]
    rag = {"MGdoppio": None, "MG": (float(mg[0, 2]), float(mg[-1, 2]))}
    for caso in ("MGdoppio", "MGmezzo"):
        s = np.load(os.path.join(MT.DIR_REF, "%s_serie.npz" % caso))
        rag[caso] = (float(s["raggio"][0]), float(s["raggio"][-1]))
    rc = {"MGdoppio": MR.CASI["MGdoppio"], "MG": MR.RHO_C_MG, "MGmezzo": MR.CASI["MGmezzo"]}
    inc = {}
    for caso in ("MGdoppio", "MG", "MGmezzo"):
        inc[caso] = rag[caso][1] - rag[caso][0]
        print("    (%-8s) rho_c %12.3f: il raggio da %.3f a %.3f, l'aumento %+.3f" % (caso, rc[caso], rag[caso][0], rag[caso][1], inc[caso]))
    q1, q2 = inc["MG"] / inc["MGdoppio"], inc["MGmezzo"] / inc["MG"]
    print("    il rapporto degli aumenti per OGNI dimezzamento di rho_c (cioe' per ogni raddoppio del lapse): (MG)/(MGx2) %.3f, (MG/2)/(MG) %.3f; la potenza log2: %.3f e %.3f"
          % (q1, q2, math.log(q1, 2), math.log(q2, 2)))
    print("    ### LA LETTURA DEL GUARDIANO (n.156): la risposta del raggio e' GRADUALE, circa %.2f volte per raddoppio (la potenza circa %.2f), molto sensibile, senza collasso; l'ipotesi «in bilico» NON e' confermata."
          % (0.5 * (q1 + q2), 0.5 * (math.log(q1, 2) + math.log(q2, 2))))
    print("=" * 130)
    return 0


def main(argv):
    if argv and argv[0] in ("letture", "raggio_rhoc"):
        return letture() if argv[0] == "letture" else raggio_rhoc()
    ap = argparse.ArgumentParser()
    ap.add_argument("azione", choices=("cuoci",))
    ap.add_argument("--caso", required=True, choices=CASI)
    ap.add_argument("--registro")
    x = ap.parse_args(argv)
    return cuoci(x.caso, x.registro)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
