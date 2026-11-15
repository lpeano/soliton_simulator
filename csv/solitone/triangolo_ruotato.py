# -*- coding: utf-8 -*-
r"""**LA PROVA DEL TRIANGOLO RUOTATO: IL VUOTO E' BLOCCATO DAL RETICOLO O DALLA SCATOLA?** *(Luca `2026-11-15` `18:45`; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `24.23`)*.

    E:\python\py3132\python.exe csv/solitone/triangolo_ruotato.py corsa --registro triangolo-ruotato > <scratchpad>/triangolo_ruotato.txt   (poi doc/referti_l2/mattone/triangolo_ruotato.txt)
    E:\python\py3132\python.exe csv/solitone/triangolo_ruotato.py lettura > doc/referti_l2/mattone/triangolo_ruotato_lettura.txt

### **`corsa`:** **il triangolo a `120` gradi di `triangolo_120.py`** *(il mattone di `L 162`, A `0`, B `120`, C `240`, la scena di S162, `R_A 60`, G+U, `2000` tick)* **con i TRE VERTICI RUOTATI di `+15` gradi** *(antiorario, la
convenzione del codice)* **attorno al baricentro, ciascuno al NODO BUONO piu' vicino** *(lo spostamento multiplo di `3` dal centro del francobollo)*: **SOLO LE POSIZIONI** *(il francobollo NON si ruota di `15` gradi: il reticolo
triangolare ha le simmetrie di `60` gradi; dichiarato)*; **i lati e l'angolo VERI stampati** *(il triangolo non e' piu' esattamente equilatero)*. **Le misure di `triangolo_120`** *(il giro e la densita' ogni `100`, la massa ogni `50`)*;
**le mappe ogni `60`** *(Luca)*; **i nomi `triangolo_t120r_*`** *(`triangolo_120.py` NON toccato, i suoi file NON sovrascritti: la classe della corsa e' QUESTA)*. **L'interprete di E:** *(una corsa nuova, R-AMBIENTE)*.
### **`lettura`:** **dalle mappe ogni `60` tick, l'orientamento a tre punte `arg(somma f e^{3 i theta}) / 3`** *(come `girandola.py`)* **del vuoto `|phi - phi0|` entro `40` nodi e dei TRE CENTRI** *(`arg(somma_j e^{3 i theta_j}) / 3`)*,
**attorno al baricentro dei centri al tick `0`; la previsione (L)/(S) della sez. `24.23`.**
### **DEVE** *(come `triangolo_120`)*: **le tre masse dei francobolli da soli uguali entro `1e-10` relativo; il giro della componente piu' grande al tick `0` `+1`; il vuoto senza materia; Gauss sotto `1e-10`.**
"""
import argparse
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone as MT  # noqa: E402
import mattone_cottura as CT  # noqa: E402
import mattone_triangolo as MTR  # noqa: E402
import triangolo_120 as T120  # noqa: E402
import triangolo_video as TV  # noqa: E402

ROT = 15.0                                   # ### Luca 18:45: 15 gradi (il verso: +, antiorario, mio)
OGNI_FOTO = 60                               # ### Luca 18:45: le mappe ogni 60
NOME = "t120r"
R_VUOTO = 40.0                               # ### Luca: entro 40 nodi
OK = [0, 0]
FALLITE = []
_Corsa = CT.Corsa


def esito(che, passa, nota):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  DEVE PASSARE: %-100s %s   %s" % (che[:100], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def vertici_ruotati(c0, fr, L):
    """### I vertici di `triangolo_120.vertici` ruotati di `ROT` gradi attorno al loro baricentro, ciascuno al nodo buono piu' vicino."""
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    B = np.column_stack([A1, A2])
    V0 = T120.vertici(c0, fr, L)
    P = np.array([V0[0][0], V0[0][1]], dtype=float)
    rel = [np.array(TO.scarti(np.array([v[0]]), np.array([v[1]]), P[0], P[1], L)[0][:2]) for v in V0]       # ### xy da A
    bar = sum(rel) / 3.0
    c, s = math.cos(math.radians(ROT)), math.sin(math.radians(ROT))
    out = []
    for r in rel:
        d = r - bar
        q = bar + np.array([c * d[0] - s * d[1], s * d[0] + c * d[1]])
        a = np.linalg.solve(B, q)
        tgt = (P[0] + a[0], P[1] + a[1])
        best = None
        for n1 in range(int(math.floor(tgt[0])) - 3, int(math.floor(tgt[0])) + 4):
            for n2 in range(int(math.floor(tgt[1])) - 3, int(math.floor(tgt[1])) + 4):
                if (n1 - fr["centro"][0]) % 3 or (n2 - fr["centro"][1]) % 3:
                    continue
                pp = (n1 - tgt[0]) * A1 + (n2 - tgt[1]) * A2
                dd = float(np.hypot(pp[0], pp[1]))
                if best is None or dd < best[0]:
                    best = (dd, n1 % L, n2 % L)
        out.append([best[1], best[2]])
    return V0, out


class CorsaR(_Corsa):
    """### `mattone_cottura.Corsa`; le misure di `triangolo_120` *(la massa, il giro, la densita')*, le mappe ogni `OGNI_FOTO`, lo stato col nome `triangolo_t120r` a `k % 500 == 450`."""

    def extra(self, k, t):
        if k % 500 == 450:
            T120.salva_stato(self.Z, self.C, k, t, "triangolo_%s" % NOME, "csv/solitone/triangolo_ruotato.py", T120.centri_lab(self.Z, self.lab, self.n_sol))
        T120.misura_extra(self.Z, self.C, k, t, self.lab, self.n_sol, (lambda kk, tt: TV.CorsaVideo.foto(self, kk, tt)) if k % OGNI_FOTO == 0 else None, True)

    def inizio(self, k):
        _Corsa.inizio(self, k)
        self.extra(k, MT.G2.T0 + k)
        mm = T120.INC["masse"]
        sc = (max(mm) - min(mm)) / max(mm)
        esito("le tre masse dei francobolli da soli uguali entro 1e-10 relativo al tick 0", sc <= 1e-10, "%.3e" % sc)
        g0 = T120.GIRO["grande"][0] if T120.GIRO["k"] and T120.GIRO["k"][0] == 0 else float("nan")
        esito("il giro della componente piu' grande al tick 0 = +1", abs(g0 - 1.0) < 1e-9, "%+.6f (la somma %+.6f)" % (g0, T120.GIRO["somma"][0] if T120.GIRO["somma"] else float("nan")))
        esito("il vuoto senza materia (max |psi_h| = 0 prima dell'incollatura)", T120.INC["vuoto_psi"] == 0.0, "%.3e" % T120.INC["vuoto_psi"])
        if FALLITE:
            raise RuntimeError("un DEVE del tick 0 fallisce: %s" % FALLITE)

    def passo(self, k, t, r, e):
        _Corsa.passo(self, k, t, r, e)
        self.extra(k, t)


def corsa(argv):
    import _presidio
    for m in ("mattone_triangolo", "mattone_cottura", "mattone", "triangolo_120", "triangolo_video"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    print("### L'INTERPRETE: %s (Python %s); PYTHONNOUSERSITE %s; TMP %s (R-AMBIENTE)" % (sys.executable, sys.version.split()[0], os.environ.get("PYTHONNOUSERSITE"), os.environ.get("TMP")))
    fr = TV.francobollo_L162(0)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        c0, L = Z["bordo"]["c0"], Z["L"]
    V0, V = vertici_ruotati(c0, fr, L)
    lati = [MT.distanza(L, V[a], V[b]) for a, b in ((0, 1), (1, 2), (2, 0))]
    print("=" * 130)
    print("IL TRIANGOLO RUOTATO (Luca 18:45): i vertici equilateri %s ruotati di %+g gradi attorno al baricentro -> %s (i nodi buoni); i lati VERI %s; A 0, B 120, C 240" % (V0, ROT, V, ["%.4f" % x for x in lati]))
    print("=" * 130)
    MTR.VARIANTI[NOME] = (0, 0, 0)
    MTR.francobollo = TV.francobollo_L162
    MTR.posti = (lambda c0_, frs, L_: [list(v) for v in V[:len(frs)]])
    MT.incolla = T120.incolla_fase
    CT.Corsa = CorsaR
    try:
        ok = MTR.main(["corsa", "--variante", NOME] + list(argv))
    except RuntimeError as x:
        print("### FERMO: %s" % x)
        ok = 1
    finally:
        CT.Corsa = _Corsa
        MT.incolla = T120._incolla
    FO = TV.FOTO
    if FO["k"]:
        with MT.scena(MT.CORSA_162, MT.T_162) as Z:
            geo = T120.geometria(Z)
        f = os.path.join(MT.DIR_REF, "triangolo_%s_mappe.npz" % NOME)
        np.savez_compressed(f, tick=np.array(FO["k"], dtype=np.int16), rho=np.stack(FO["rho"]), dphi=np.stack(FO["dphi"]), E=np.stack(FO["E"]), centri=np.stack(FO["centri"]), **geo)
        print("### LE MAPPE: %d fotogrammi in %s, %.1f MB" % (len(FO["k"]), f, os.path.getsize(f) / 1e6))
    f = os.path.join(MT.DIR_REF, "triangolo_%s_giro.npz" % NOME)
    np.savez_compressed(f, **{x: np.array(v) for x, v in T120.GIRO.items()})
    print("=" * 130)
    print("ESITO (triangolo_ruotato): %d/%d controlli come devono; fallite %s; mattone_triangolo.corsa ha reso %s" % (OK[0], OK[1], FALLITE, ok))
    return 0 if (not FALLITE and ok == 0) else 1


def lettura():
    import _presidio
    from solitone import toro as TO
    _presidio.avvia(__file__)
    mp = np.load(os.path.join(MT.DIR_REF, "triangolo_%s_mappe.npz" % NOME))
    tk = np.array(mp["tick"])
    m1, m2, L = np.array(mp["m1"], dtype=float), np.array(mp["m2"], dtype=float), int(mp["L"])
    c3 = np.asarray(mp["centri"][0], dtype=float)
    c = (float(c3[:, 0].mean()), float(c3[:, 1].mean()))
    xy = TO.scarti(m1, m2, c[0], c[1], L)[:, :2]
    r = np.hypot(xy[:, 0], xy[:, 1])
    e3 = np.exp(3j * np.arctan2(xy[:, 1], xy[:, 0]))
    dentro = r <= R_VUOTO
    import girandola as GI
    vu, ce = [], []
    for i in range(len(tk)):
        vu.append(math.degrees(np.angle(np.sum(np.asarray(mp["dphi"][i], dtype=float)[dentro] * e3[dentro]))) / 3.0)
        cc = np.asarray(mp["centri"][i], dtype=float)
        th = [math.atan2(*TO.scarti(np.array([q[0]]), np.array([q[1]]), c[0], c[1], L)[0][:2][::-1]) for q in cc]
        ce.append(math.degrees(np.angle(np.sum(np.exp(3j * np.array(th))))) / 3.0)
    vu, ce = GI.srotola(vu), GI.srotola(ce)
    print("=" * 130)
    print("IL TRIANGOLO RUOTATO, LA LETTURA (Luca 18:45): l'orientamento a tre punte del vuoto (entro %g) e dei centri, ogni 60 tick, attorno al baricentro dei centri al tick 0 (%.3f, %.3f)" % (R_VUOTO, c[0], c[1]))
    print("=" * 130)
    for i in range(len(tk)):
        if i % 5 == 0 or i == len(tk) - 1:
            print("    k %5d: il vuoto %+8.2f   i centri %+8.2f" % (tk[i], vu[i], ce[i]))
    dv = vu[-1] - vu[0]
    print("-" * 130)
    print("### il vuoto da %+.2f a %+.2f (%+.2f gradi); i centri da %+.2f a %+.2f (%+.2f)" % (vu[0], vu[-1], dv, ce[0], ce[-1], ce[-1] - ce[0]))
    print("### LA PREVISIONE (sez. 24.23, nella convenzione del codice): (S) il vuoto resta entro 2 gradi dalla partenza -> %s; (L) il vuoto va verso le direzioni del reticolo di almeno 5 gradi -> %s"
          % ("SI'" if abs(dv) <= 2.0 else "NO", "SI'" if abs(dv) >= 5.0 else "NO"))
    print("=" * 130)
    return 0


def main(argv):
    if argv and argv[0] == "lettura":
        return lettura()
    ap = argparse.ArgumentParser()
    ap.add_argument("azione", choices=("corsa",))
    ap.add_argument("--registro")
    x = ap.parse_args(argv)
    return corsa(["--registro", x.registro] if x.registro else [])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
