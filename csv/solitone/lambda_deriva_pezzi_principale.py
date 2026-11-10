# -*- coding: utf-8 -*-
r"""**D2-bis, IL SEGNO DELLA DERIVA SUL NUCLEO DEL PRINCIPALE** *(Luca `2026-11-10` `01:22`; il task history `doc/TASK_HISTORY/2026-11-09_d1_deriva_lambda_principale.md`, sez. `8`)*. [[PIANO-2D-3D]] [[H-NUCLEO-CONGELATO]]

    python csv/solitone/lambda_deriva_pezzi_principale.py > doc/referti_l2/lambda_deriva_pezzi_principale.txt

### **LA COPIA, SUL PRINCIPALE, di `csv/solitone/lambda_deriva_pezzi.py` del laterale** *(`cd10786c`, blob `a6201067`; l'eccezione di Luca a U1)*, **con le sei modifiche della sez. `8.1`:**
### `CORSA` qui; **i pezzi interi** *(niente sotto-pezzi)*; **i tick SENZA avvolgimento**; **D2.3 al mezzo e all'intero, e sui passi in archivio**; **D2.5 contro D1-bis**; **le letture z1/z2.** **Il testo che segue e' quello del laterale** *(D2)*:

**La scena di T1** *(il codice di `lambda_vuoto_deriva.py`: vuoto F3 di TBS, `81 x 81`, `mot.cs 0.15`, `lambda_c = None`, `1000` tick)*. **Gli operatori di `mot.operatori` e, dentro le posizioni del vuoto, `FP._grover_mezzo`
e `FP._hop_phi_mezzo` avvolti IN MEMORIA, solo per la corsa:** **dopo ogni pezzo e sotto-pezzo `Lambda` ESATTO** *(`fractions.Fraction` dai float di `phi`)* **sui nodi `0`-`8`**, **e la norma totale in virgola mobile.**
**D2.3:** i coefficienti dei pezzi del vuoto, esatti. **D2.4** *(DEVE FALLIRE)*: `phi *= fl(1 + 1e-15)` dopo la posizione `1`. **D2.5:** la chiusura contro T1. **Le letture p1/p2/p3** *(sez. `24.3`)*.
### **Il peso si legge per ETICHETTA** *(la posizione, e per `6`-`9` il sotto-pezzo `a`/`b`/`c`: la tabella della sez. `24.1`)*; **il raggruppamento per TIPO di coefficiente si stampa accanto, come informazione: non decide.**
"""
import contextlib
import os
import sys
import time
from fractions import Fraction

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

CORSA = "TBS"                  # ### D2-bis (1): carta_punto_fisso.CORSA del laterale
N_TICK = 1000                  # ### sez. 24.2 (la scena di T1)
CAMPIONE = tuple(range(9))     # ### sez. 24.2: i nodi 0-8, dichiarati prima
FATT = 1.0 + 1e-15             # ### D2.4 (Luca)
POS_INIEZIONE = 1              # ### sez. 24.2: scelta prima di vedere i numeri
SOGLIA_P = 0.90                # ### le letture di Luca: «oltre il 90%»
TOLL = 0.10                    # ### D2.4, D2.5: «entro il 10%»
T1 = ("2bb5ee52", "doc/referti_l2/lambda_vuoto_deriva_principale_nucleo.txt")   # ### D2-bis (5): D1-bis, il nucleo del principale senza avvolgimento
VUOTO = (1, 2, 6, 7, 8, 9, 13, 14)   # ### le posizioni dei pezzi che possono toccare phi (sez. 24.1); 2 e 13 ritornano subito
SOTTO = ()                     # ### D2-bis (2): sul principale grover e hop_phi sono pezzi INTERI
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-104s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:104], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return buono


def deriva_t1():
    """### La deriva media di T1 al tick `1000`, LETTA dal referto committato *(nessun numero ricopiato)*."""
    import re
    import subprocess
    radice = os.path.dirname(os.path.dirname(_QUI))
    testo = subprocess.check_output(["git", "show", "%s:%s" % T1], cwd=radice).decode("utf-8")
    m = re.search(r"al tick 1000: max [-+0-9.e]+ \([0-9.]+ ulp\), media ([-+0-9.e]+),", testo)
    assert m, "il referto di T1 non si legge"
    return float(m.group(1))


class Strumento(object):
    """### Gli avvolgimenti IN MEMORIA. `reg[etichetta]` = lista per tick di array `(9,)` di `Delta Lambda / Lambda` esatti *(float della differenza esatta)*; `nor[etichetta]` = la norma totale in float, relativa."""

    def __init__(self, st, mot, inietta):
        import flussi_parziali as FP
        self.st, self.mot, self.FP, self.inietta = st, mot, FP, inietta
        off, est = mot.inc.offset, mot.inc.estremita
        self.mezze = [np.array(est[off[k]:off[k + 1]]) for k in CAMPIONE]
        self.reg, self.nor = {}, {}
        self.pos, self.cur, self.sub = [0], [None], []
        self.tick_reg = {}

    def lam(self):
        phi = self.st["phi_h"]
        out = []
        for h in self.mezze:
            s = Fraction(0)
            for x in phi[h]:
                re_, im_ = Fraction(float(x.real)), Fraction(float(x.imag))
                s += re_ * re_ + im_ * im_
            out.append(s)
        return out

    def norma(self):
        return float(np.sum(np.abs(self.st["phi_h"]) ** 2))

    def scrivi(self, et, L0, L1, n0, n1):
        self.tick_reg.setdefault(et, (np.array([float((b - a) / a) for a, b in zip(L0, L1)]), (n1 - n0) / n0))

    def avvolgi(self):
        mot, FP = self.mot, self.FP
        self.veri = dict(mot.operatori)
        self.gm = self.hm = None        # ### D2-bis (2): niente mezzi pezzi sul principale
        io = self

        def esterno(orig):
            def f(st, par, fr):
                io.pos[0] += 1
                p = io.pos[0]
                L0, n0 = io.lam(), io.norma()
                io.cur[0], io.sub[:] = p, []
                out = orig(st, par, fr)
                if io.inietta and p == POS_INIEZIONE:
                    st["phi_h"] *= FATT
                io.cur[0] = None
                L1, n1 = io.lam(), io.norma()
                if p in SOTTO:
                    assert len(io.sub) == 2, (p, len(io.sub))
                    for lettera, (a0, a1, m0, m1) in zip("ab", io.sub):
                        io.scrivi("%d%s" % (p, lettera), a0, a1, m0, m1)
                    io.scrivi("%dc" % p, io.sub[1][1], L1, io.sub[1][3], n1)
                else:
                    io.scrivi("%d" % p, L0, L1, n0, n1)
                return out
            return f

        def interno(orig):
            def f(mot_, x, fr):
                if io.cur[0] not in SOTTO:
                    return orig(mot_, x, fr)
                L0, n0 = io.lam(), io.norma()
                out = orig(mot_, x, fr)
                io.sub.append((L0, io.lam(), n0, io.norma()))
                return out
            return f

        for k, v in self.veri.items():
            mot.operatori[k] = esterno(v)
        del interno                     # ### D2-bis (2)

    def ripristina(self):
        self.mot.operatori.clear()
        self.mot.operatori.update(self.veri)

    def tick(self, par):
        import tick as TK
        self.pos[0], self.tick_reg = 0, {}
        TK.tick(self.st, self.mot, par)
        assert self.pos[0] == 14, self.pos[0]
        for k, (a, b) in self.tick_reg.items():
            self.reg.setdefault(k, []).append(a)
            self.nor.setdefault(k, []).append(b)


def etichette():
    out = []
    for p in range(1, 15):
        out += ["%d%s" % (p, c) for c in "abc"] if p in SOTTO else ["%d" % p]
    return out


TIPO = {"1": "materia_vuoto", "14": "materia_vuoto", "2": "fase_vuoto (spenta)", "13": "fase_vuoto (spenta)"}
TIPO["6"] = TIPO["9"] = "Grover (intero)"          # ### D2-bis (2)
TIPO["7"] = TIPO["8"] = "spostamento (intero)"     # ### D2-bis (2)
for _p in (3, 4, 5, 10, 11, 12):
    TIPO["%d" % _p] = "solo psi"


def corsa(st, mot, par, foto, inietta):
    for k, v in foto.items():
        st[k][...] = v
    mot.lambda_c = None
    S = Strumento(st, mot, inietta)
    lam0 = mot.densita_vuoto(st).copy()
    S.avvolgi()
    try:
        for _t in range(N_TICK):
            S.tick(par)
    finally:
        S.ripristina()
    lam1 = mot.densita_vuoto(st).copy()
    tab = {}
    for et in etichette():
        a = np.array(S.reg[et])            # (N_TICK, 9)
        per_tick = a.mean(axis=1)
        tab[et] = {"media": float(a.mean()), "pos": float(np.mean(per_tick > 0)), "neg": float(np.mean(per_tick < 0)),
                   "zero": bool(np.all(a == 0)), "nodi": (float(a.mean(axis=0).min()), float(a.mean(axis=0).max())), "norma": float(np.mean(S.nor[et]))}
    return tab, float(np.mean(lam1 - lam0)) / N_TICK, float(lam0.mean())


def coefficienti(mot, st):
    """### D2-bis (4): **i coefficienti come li calcola il codice, poi ESATTI in `Fraction`**, **al mezzo `h = 0.25` e all'intero `f = 0.5`;** **e `|alpha + beta|^2 - 1` sui passi in archivio.**"""
    import mpmath
    import _vuoto_vivo_B as V
    import flussi_parziali as FP
    import materia_vuoto as MV
    mpmath.mp.dps = 50

    def fr(c):
        return Fraction(float(c.real)), Fraction(float(c.imag))

    def m2(c):
        a, b = c
        return a * a + b * b

    def somma(c1, c2, k=1):
        return c1[0] + k * c2[0], c1[1] + k * c2[1]

    def riga(nome, valori):
        q = [m2(v) - 1 for v in valori]
        nmax = max(abs(x) for x in q)
        smax = max(mpmath.sqrt(mpmath.mpf(x.numerator) / x.denominator + 1) for x in q) - 1
        print("    %-48s |lambda|^2 - 1: %s; ||U^dag U - I|| = %.3e; sigma_max - 1 = %s" % (nome, ", ".join("%+.3e" % float(x) for x in q), float(nmax), mpmath.nstr(smax, 4)))
        return float(smax), [float(x) for x in q]

    def ab(z):
        zz = np.array([[z]])
        be = np.empty_like(zz)            # ### le operazioni di FP._alfa_beta, nello stesso ordine, SENZA i buffer del motore
        np.subtract(1.0, zz, out=be)
        np.divide(be, 2.0, out=be)
        al = zz.copy()
        np.add(1.0, zz, out=al)
        np.divide(al, 2.0, out=al)
        return fr(al[0, 0]), fr(be[0, 0])

    out = {}
    gr = np.unique(mot.inc.grado)
    for h, chi in ((0.25, "mezzo, h 0.25 (il laterale)"), (0.5, "intero, f 0.5 (il principale)")):
        zn = np.unique(FP.z_nodo(mot, h).copy().reshape(-1))
        za = np.unique(FP.z_arco(mot, h).copy().reshape(-1))
        print("  D2.3, %s: i valori distinti nella scena z_nodo %d, z_arco %d, gradi %s" % (chi, zn.size, za.size, [int(d) for d in gr]))
        sg, sh = [], []
        for z in zn:
            for d in gr:
                w = np.empty(1, complex)
                np.subtract(1.0, np.array([z]), out=w)
                np.divide(w.reshape(1, 1), np.array([[d]]), out=w.reshape(1, 1))
                zf, wf = fr(z), fr(w[0])
                sg.append(riga("Grover, z %.6f%+.6fj, d %d" % (z.real, z.imag, d), [somma(zf, wf, int(d)), zf])[0])
            riga("la fase |z| (nodo), z %.6f%+.6fj" % (z.real, z.imag), [fr(z)])
        for z in za:
            af, bf = ab(z)
            v, q = riga("spostamento, z %.6f%+.6fj (alpha+beta, alpha-beta)" % (z.real, z.imag), [somma(af, bf), somma(af, bf, -1)])
            sh.append(v)
            if h == 0.5:
                out["ab_intero"] = q[0]
        if h == 0.5:
            out["Grover (intero)"] = max(sg)
            out["spostamento (intero)"] = max(sh)
    al, be = MV.pezzi(mot.densita_materia(st), mot.densita_vuoto(st))
    fas = np.asarray(be) * FP.dtau_nodo(mot) * 0.5   # ### le operazioni di materia_vuoto.applica per phi, nello stesso ordine (f = 0.5)
    fat = np.unique(np.exp(np.multiply(fas, -1j)))
    out["materia_vuoto"] = max(riga("materia_vuoto, il fattore di phi (beta %s)" % np.unique(np.asarray(be)), [fr(f)])[0] for f in fat)
    print("  D2-bis (4), |alpha+beta|^2 - 1 SUI PASSI DELLE CORSE IN ARCHIVIO (_vuoto_vivo_B.CORSE; s_arco = s al bit; nessuna lettura):")
    for s in sorted({float(v[2]) for v in V.CORSE.values()}):
        for f in (0.5, 0.25):
            sa = np.array([s])
            np.multiply(sa, f, out=sa)
            z = FP.espi(sa.reshape(-1, 1), np.empty((1, 1), complex), np.empty((1, 1)))[0, 0]
            af, bf = ab(z)
            q = [m2(somma(af, bf)) - 1, m2(somma(af, bf, -1)) - 1]
            print("    s %-6g f %-5g z %.15f%+.15fj: |alpha+beta|^2 - 1 %+.3e, |alpha-beta|^2 - 1 %+.3e" % (s, f, z.real, z.imag, float(q[0]), float(q[1])))
    return out

def main():
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import corsa_accensione as CA
    for m in ("__init__", "corsa_accensione", "carta_punto_fisso"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("tick", "flussi_parziali", "energia_pesata", "materia_vuoto", "motore"):
        _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    t00 = time.time()
    print("=" * 130)
    print("D2-bis, IL SEGNO DELLA DERIVA SUL NUCLEO DEL PRINCIPALE, SENZA AVVOLGIMENTO (sez. 8): il vuoto F3 della corsa %s, %d tick; Lambda esatto sui nodi %s; D2.4: fl(1+1e-15) dopo la posizione %d" % (CORSA, N_TICK, list(CAMPIONE), POS_INIEZIONE))
    print("=" * 130)
    with CA.con_L(CA.LCORSA.get(CORSA)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        phi_v = CA.vuoto_della_corsa(z, CORSA)
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, mot, par = z["st"], z["mot"], z["par"]
        st["psi_h"][...] = 0.0
        st["phi_h"][...] = phi_v
        foto = {k: v.copy() for k, v in st.items() if isinstance(v, np.ndarray)}
        print("### la scena: %d nodi; mot.cs %s; Lambda all'inizio min %.17g max %.17g; i gradi dei nodi del campione %s" % (
            mot.inc.n, "None" if mot.cs is None else "array (min %.6g, max %.6g)" % (float(np.min(mot.cs)), float(np.max(mot.cs))),
            float(mot.densita_vuoto(st).min()), float(mot.densita_vuoto(st).max()), [int(mot.inc.grado[k]) for k in CAMPIONE]))
        import flussi_parziali as FP
        with SF.forma(VC.FORMA), contextlib.nullcontext():     # ### D2-bis (3): SENZA BE.conv(DC.ZERO), che qui avvolgerebbe
            print("### dentro i tick FP.grover e' %s.%s, FP.hop_phi e' %s.%s (il controllo che nessun avvolgimento dello zero c'e')" % (FP.grover.__module__, FP.grover.__qualname__, FP.hop_phi.__module__, FP.hop_phi.__qualname__))
            sig = coefficienti(mot, st)
            for k, v in foto.items():
                st[k][...] = v
            t0 = time.time()
            tab, dfl, lam0 = corsa(st, mot, par, foto, False)
            print("### la corsa: %.0f s" % (time.time() - t0))
            t0 = time.time()
            tabi, _dfli, _l = corsa(st, mot, par, foto, True)
            print("### la corsa con l'iniezione: %.0f s" % (time.time() - t0))
    print("-" * 130)
    print("  D2.2, PER PEZZO (Delta Lambda / Lambda ESATTO, media sui %d tick e sui nodi %s; il segno; la frazione dei tick con la media sui nodi > 0 e < 0; i nodi min/max; la norma totale in float)" % (N_TICK, list(CAMPIONE)))
    tot = sum(v["media"] for v in tab.values())
    for et in etichette():
        v = tab[et]
        print("    pos %-4s %-28s %+.4e  %s  >0 %.3f  <0 %.3f  nodi [%+.3e, %+.3e]  norma %+.3e  peso %+.4f%s" % (
            et, TIPO[et], v["media"], "+" if v["media"] > 0 else ("-" if v["media"] < 0 else "0"), v["pos"], v["neg"], v["nodi"][0], v["nodi"][1], v["norma"],
            v["media"] / tot if tot else float("nan"), "   (ZERO ESATTO in ogni tick e nodo)" if v["zero"] else ""))
    print("  la somma dei contributi (relativa, per tick): %+.4e; per tick assoluta (x Lambda %.6g): %+.4e" % (tot, lam0, tot * lam0))
    tipi = {}
    for et in etichette():
        tipi[TIPO[et]] = tipi.get(TIPO[et], 0.0) + tab[et]["media"]
    print("  PER TIPO (informazione, non decide):")
    for k, v in sorted(tipi.items(), key=lambda kv: -abs(kv[1])):
        print("    %-30s %+.4e  peso %+.4f  sigma_max - 1 dei coefficienti: %s" % (k, v, v / tot if tot else float("nan"), "%.3e" % sig[k] if k in sig else "-"))
    print("-" * 130)
    d1 = deriva_t1() / N_TICK
    chiude = tot * lam0
    esito("D2.5 la somma dei contributi esatti ridà la deriva di D1-bis per tick (%+.4e, dal referto a %s) entro il %.0f%%" % (d1, T1[0], 100 * TOLL), abs(chiude / d1 - 1) <= TOLL,
          "%+.4e (il rapporto %.6f); la deriva in float di densita_vuoto di questa corsa %+.4e" % (chiude, chiude / d1, dfl))
    atteso = float(Fraction(FATT) ** 2 - 1)
    piu = max(etichette(), key=lambda e: abs(tabi[e]["media"]))
    aumento = tabi[str(POS_INIEZIONE)]["media"] - tab[str(POS_INIEZIONE)]["media"]
    visto = piu == str(POS_INIEZIONE) and abs(aumento / atteso - 1) <= TOLL
    esito("D2.4 la diagnosi NON indica la posizione %d (iniettata fl(1+1e-15)) come la piu' pesante con l'aumento atteso %.4e entro il %.0f%%" % (POS_INIEZIONE, atteso, 100 * TOLL), not visto,
          "la piu' pesante: %s; l'aumento %.4e (il rapporto %.4f)" % (piu, aumento, aumento / atteso), deve=False)
    print("-" * 130)
    sp = tipi.get("spostamento (intero)", 0.0) / tot if tot else float("nan")
    abi = sig["ab_intero"]
    print("  per le letture: |alpha+beta|^2 - 1 a f 0.5 %+.3e; il peso dello spostamento (posizioni 7 + 8) %.4f" % (abi, sp))
    if abi < 0 and sp > SOGLIA_P and abs(chiude / d1 - 1) <= TOLL:
        lett = "z1: |alpha+beta|^2 - 1 = %+.3e < 0 sul z del principale e lo spostamento pesa %.4f: il segno opposto spiegato dallo stesso meccanismo" % (abi, sp)
    else:
        lett = "z2: |alpha+beta|^2 - 1 = %+.3e, il peso dello spostamento %.4f, D2.5 %s: senza interpretare" % (abi, sp, "chiude" if abs(chiude / d1 - 1) <= TOLL else "NON chiude")
    print("  LA LETTURA: (%s)" % lett)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
