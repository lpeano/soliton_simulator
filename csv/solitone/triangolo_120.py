# -*- coding: utf-8 -*-
r"""**IL TRIANGOLO A `120` GRADI, LA FASE 1** *(Luca `2026-11-15` `10:29`, B3; la decisione `01:11`; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `23`)*.

    python csv/solitone/triangolo_120.py corsa --registro legati-t120-a > <scratchpad>/triangolo_t120.txt     (poi doc/referti_l2/mattone/triangolo_t120.txt)
    (la fase 2, da k 2000 a 6000: csv/solitone/legati.py triangolo; la lettura: csv/solitone/legati.py lettura)

### **`mattone_triangolo.corsa` COSI' COM'E'** *(la scena di S162, il bordo da `R_A 60`, G+U, `2000` tick, il tetto `28800 s`, le misure di (T-fase); `mattone_triangolo.py` NON si tocca)* **con IN MEMORIA:**
**(1) il francobollo del mattone di `L 162`** *(`L162_MGU_03000`: `triangolo_video.francobollo_L162`)*; **(2) i vertici ESATTAMENTE equilateri** *(`triangolo_equilatero.vertici`, `(a, b) = (13, 0)`, il lato `39`; il primo
vertice `P` il nodo buono piu' vicino a `c0 - (26, 13)`, cosi' il baricentro `P + (26, 13)` cade sul centro del bordo)*; **(3) dopo l'incollatura del `j`-esimo francobollo `psi_h` per `exp(i 2 pi j / 3)`**
*(A `0`, B `120`, C `240` gradi; i vertici `P`, `P + 3 (a, b)`, `P + 3 R(a, b)` in senso ANTIORARIO: controllato)*; **(4) `mattone_cottura.Corsa`: una sottoclasse che salva le TRE MAPPE ogni `20` tick** *(la funzione
del video)*, **la massa totale e la massa oltre `R_A` ogni `50`, ogni `100` IL GIRO DELLA FASE e la densita' al centro, e lo stato a `k = 450, 950, ...`** *(`50` tick prima di quelli di `mattone_triangolo`: la
ripartenza di `50` tick, Luca `10:29`)*.
### **IL GIRO** *(mio, dichiarato)*: **`24` punti su un cerchio attorno al baricentro dei tre centri, di raggio la distanza media dal baricentro alle meta' dei lati; in ogni punto la SOMMA di `psi` su un disco di
raggio `2`** *(come `triangolo_dentro.py`)*; **il giro = la somma delle `24` differenze di fase ridotte in `(-pi, pi]`, in multipli di `2 pi`; per ognuna delle `12` componenti, per la piu' grande** *(la norma su
tutto lo stato)* **e per la SOMMA delle `12`.** **La densita' al centro: la media di `rho` sul disco di raggio `2` attorno al baricentro.**
### **DEVE** *(il mandato)*: **i tre lati uguali entro `1e-9` al tick `0`; le tre masse dei francobolli incollati DA SOLI uguali entro `1e-10` relativo; il giro della componente PIU' GRANDE al tick `0` = `+1`
(mia lettura di «il giro della fase»: le altre si stampano); Gauss sotto `1e-10` a ogni controllo** *(quello di `mattone_triangolo`)*. **In piu' (miei): i vertici in senso antiorario; il vuoto senza materia.**
**I DEVE del tick `0` si controllano PRIMA dei `2000` tick: se uno fallisce, la corsa si ferma li'.**
"""
import argparse
import json
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
import triangolo_equilatero as TE  # noqa: E402
import triangolo_video as TV  # noqa: E402

FASI = (0.0, 2.0 * math.pi / 3.0, 4.0 * math.pi / 3.0)     # ### Luca 01:11: 0, 120, 240 gradi
AB = (13, 0)                                                # ### B3: il lato 39
OGNI_FOTO, OGNI_GIRO, OGNI_M = 20, 100, 50                  # ### B3: le mappe ogni 20 fino a 2000
N_CERCHIO, R_DISCO = 24, 2.0                                # ### miei, dichiarati
TOLL_LATI, TOLL_MASSE = 1e-9, 1e-10                         # ### il mandato
FOTO = TV.FOTO                                              # ### le mappe le scrive TV.CorsaVideo.foto (la stessa funzione del video)
GIRO = {"k": [], "comp": [], "grande": [], "somma": [], "dens": [], "r": [], "Mtot_k": [], "Mtot": [], "fuori_k": [], "fuori": []}
INC = {"j": 0, "masse": [], "vuoto_psi": None}
OK = [0, 0]
FALLITE = []
_Corsa = CT.Corsa
_incolla = MT.incolla


def esito(che, passa, nota, deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-100s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:100], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def ridotta(x):
    y = (x + math.pi) % (2.0 * math.pi) - math.pi
    return math.pi if y == -math.pi else y


def vertici(c0, fr, L):
    """### Il primo vertice: il nodo buono piu' vicino a `c0 - (26, 13)`; poi `triangolo_equilatero.vertici`."""
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    a, b = AB
    ra, rb = TE.R(a, b)
    tgt = (c0[0] - (a + ra), c0[1] - (b + rb))
    best = None
    for n1 in range(int(math.floor(tgt[0])) - 3, int(math.floor(tgt[0])) + 4):
        for n2 in range(int(math.floor(tgt[1])) - 3, int(math.floor(tgt[1])) + 4):
            if (n1 - fr["centro"][0]) % 3 or (n2 - fr["centro"][1]) % 3:
                continue
            p = (n1 - tgt[0]) * A1 + (n2 - tgt[1]) * A2
            dd = float(np.hypot(p[0], p[1]))
            if best is None or dd < best[0]:
                best = (dd, n1, n2)
    return TE.vertici((best[1], best[2]), a, b, L)


def giro_di(psi_n, m1, m2, L, centro, r):
    """### Il giro della fase su `N_CERCHIO` punti a distanza `r` da `centro` *(nodi)*, per ogni colonna di `psi_n` *(nodi x componenti)*."""
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    B = np.column_stack([A1, A2])
    somme = []
    for i in range(N_CERCHIO):
        th = 2.0 * math.pi * i / N_CERCHIO
        d = np.linalg.solve(B, np.array([r * math.cos(th), r * math.sin(th)]))
        dd = np.hypot(*TO.scarti(m1, m2, centro[0] + d[0], centro[1] + d[1], L).T[:2])
        somme.append(psi_n[dd <= R_DISCO].sum(axis=0))
    f = np.angle(np.array(somme))
    return np.array([sum(ridotta(f[(i + 1) % N_CERCHIO, c] - f[i, c]) for i in range(N_CERCHIO)) / (2.0 * math.pi) for c in range(f.shape[1])])


def misura_dentro(Z, centri):
    """### Il giro per le `12` componenti, la piu' grande e la somma; la densita' al centro; il raggio del cerchio."""
    from solitone import toro as TO
    L, m1, m2 = Z["L"], Z["m1"], Z["m2"]
    psi = Z["st"]["psi_h"][Z["righe"]].reshape(Z["n"], -1)
    grande = int(np.argmax(np.sum(np.abs(psi) ** 2, axis=0)))
    cen = (sum(c[0] for c in centri) / 3.0, sum(c[1] for c in centri) / 3.0)
    mezzi = [((centri[a][0] + centri[b][0]) / 2.0, (centri[a][1] + centri[b][1]) / 2.0) for a, b in ((0, 1), (1, 2), (2, 0))]
    r = float(np.mean([MT.distanza(L, cen, q) for q in mezzi]))
    g = giro_di(np.concatenate([psi, psi.sum(axis=1, keepdims=True)], axis=1), m1, m2, L, cen, r)
    rho = MT.rho_di(Z)
    dd = np.hypot(*TO.scarti(m1, m2, cen[0], cen[1], L).T[:2])
    return g[:-1], grande, float(g[-1]), float(rho[dd <= R_DISCO].mean()), r


def misura_extra(Z, C, k, t, lab, n_sol, foto, registra_giro):
    """### Le misure di B3 in piu' di `mattone_triangolo`: la massa totale e oltre `R_A` ogni `50`; il giro e la densita' ogni `100`; le mappe (`foto`)."""
    from solitone import toro as TO
    if k % OGNI_M == 0:
        if "r_c0" not in Z:
            c0 = Z["bordo"]["c0"]
            Z["r_c0"] = np.hypot(*TO.scarti(Z["m1"], Z["m2"], c0[0], c0[1], Z["L"]).T[:2])
        rho = MT.rho_di(Z)
        GIRO["Mtot_k"].append(k)
        GIRO["Mtot"].append(float(np.sum(np.abs(Z["st"]["psi_h"]) ** 2)))
        GIRO["fuori_k"].append(k)
        GIRO["fuori"].append(float(rho[Z["r_c0"] > MTR.R_A_SCENA].sum() / rho.sum()))
    if foto:
        foto(k, t)
    if registra_giro and k % OGNI_GIRO == 0 and n_sol == 3:
        rho = MT.rho_di(Z)
        centri = [TO.centro(np.where(lab == j, rho, 0.0), Z["m1"], Z["m2"], Z["L"])[:2] for j in range(3)]
        g, grande, gs, dens, r = misura_dentro(Z, centri)
        GIRO["k"].append(k)
        GIRO["comp"].append(g)
        GIRO["grande"].append(float(g[grande]))
        GIRO["somma"].append(gs)
        GIRO["dens"].append(dens)
        GIRO["r"].append(r)
        print("    [giro] k %5d: la componente piu' grande (%d) %+.3f; la somma %+.3f; le 12 %s; la densita' al centro %.4e; il cerchio r %.3f; oltre R_A %.3e"
              % (k, grande, g[grande], gs, " ".join("%+.0f" % x for x in g), dens, r, GIRO["fuori"][-1] if GIRO["fuori"] else float("nan")))
        sys.stdout.flush()


def centri_lab(Z, lab, n_sol):
    from solitone import toro as TO
    rho = MT.rho_di(Z)
    return [[float(x) for x in TO.centro(np.where(lab == j, rho, 0.0), Z["m1"], Z["m2"], Z["L"])[:2]] for j in range(n_sol)]


def salva_stato(Z, C, k, t, nome, codice, centri):
    """### Lo stato col campo; nel `meta` anche i centri dei solitoni *(le etichette dei conti alla ripartenza)*."""
    import _vuoto_vivo_B as V
    np.savez(os.path.join(MT.DIR_E, "%s_%05d.npz" % (nome, k)), meta=np.array(json.dumps({"k": k, "t": t, "sha": V.shas(Z["z"]), "codice": codice, "centri": centri})),
             campo_A=C.campo.A, campo_E=C.campo.E, **{x: Z["st"][x] for x in Z["chiavi"]})


class CorsaT120(_Corsa):
    """### `mattone_cottura.Corsa` com'e'; in piu' le misure di B3 e lo stato a `k = 450, 950, ...`."""

    def extra(self, k, t):
        if k % 500 == 450:
            salva_stato(self.Z, self.C, k, t, "triangolo_t120", "csv/solitone/triangolo_120.py", centri_lab(self.Z, self.lab, self.n_sol))
        misura_extra(self.Z, self.C, k, t, self.lab, self.n_sol, (lambda kk, tt: TV.CorsaVideo.foto(self, kk, tt)) if k % OGNI_FOTO == 0 else None, True)

    def inizio(self, k):
        _Corsa.inizio(self, k)
        self.extra(k, MT.G2.T0 + k)
        mm = INC["masse"]                                          # ### i DEVE del tick 0 PRIMA dei 2000 tick: se uno fallisce la corsa si ferma qui
        sc = (max(mm) - min(mm)) / max(mm)
        esito("le tre masse dei francobolli da soli uguali entro %g relativo al tick 0" % TOLL_MASSE, sc <= TOLL_MASSE, "%.3e (%s)" % (sc, ["%.15e" % m for m in mm]))
        g0 = GIRO["grande"][0] if GIRO["k"] and GIRO["k"][0] == 0 else float("nan")
        esito("il giro della componente piu' grande al tick 0 = +1", abs(g0 - 1.0) < 1e-9, "%+.6f (la somma %+.6f)" % (g0, GIRO["somma"][0] if GIRO["somma"] else float("nan")))
        esito("il vuoto senza materia (max |psi_h| = 0 prima dell'incollatura)", INC["vuoto_psi"] == 0.0, "%.3e" % INC["vuoto_psi"])
        if FALLITE:
            raise RuntimeError("un DEVE del tick 0 fallisce: %s" % FALLITE)

    def passo(self, k, t, r, e):
        _Corsa.passo(self, k, t, r, e)
        self.extra(k, t)


def incolla_fase(Z, fr, centro, allinea):
    """### `mattone.incolla` com'e'; poi `psi_h` per `exp(i FASI[j])` *(il `j`-esimo francobollo)*; la massa del francobollo da solo."""
    if INC["vuoto_psi"] is None:
        INC["vuoto_psi"] = float(np.max(np.abs(Z["st"]["psi_h"])))
    D = _incolla(Z, fr, centro, allinea)
    j = INC["j"]
    if FASI[j] != 0.0:
        Z["st"]["psi_h"][...] = Z["st"]["psi_h"] * np.exp(1j * FASI[j])
    INC["masse"].append(float(np.sum(np.abs(Z["st"]["psi_h"]) ** 2)))
    INC["j"] = j + 1
    return D


def geometria(Z):
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    xy = Z["m1"][:, None] * A1[None, :] + Z["m2"][:, None] * A2[None, :]
    return dict(m1=Z["m1"].astype(np.int16), m2=Z["m2"].astype(np.int16), x=xy[:, 0].astype(np.float32), y=xy[:, 1].astype(np.float32), L=np.int16(Z["L"]))


def corsa(argv):
    import _presidio
    from solitone import toro as TO
    for m in ("mattone_triangolo", "mattone_cottura", "mattone", "triangolo_equilatero", "triangolo_video"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    fr = TV.francobollo_L162(0)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        c0, L = Z["bordo"]["c0"], Z["L"]
    V = vertici(c0, fr, L)
    lati = [MT.distanza(L, V[a], V[b]) for a, b in ((0, 1), (1, 2), (2, 0))]
    pb = TO.scarti(np.array([V[1][0]]), np.array([V[1][1]]), V[0][0], V[0][1], L)[0][:2]
    pc = TO.scarti(np.array([V[2][0]]), np.array([V[2][1]]), V[0][0], V[0][1], L)[0][:2]
    area = 0.5 * float(pb[0] * pc[1] - pb[1] * pc[0])
    cen = ((V[0][0] + V[1][0] + V[2][0]) / 3.0, (V[0][1] + V[1][1] + V[2][1]) / 3.0)
    print("=" * 130)
    print("IL TRIANGOLO A 120 GRADI, LA FASE 1 (Luca 10:29, B3): il francobollo %s; i vertici %s (A 0, B 120, C 240 gradi); i lati %s; l'area con segno %+.4f (positiva: ANTIORARIO); il baricentro %s, il centro del bordo %s (a %.3f)"
          % (fr["file"], V, ["%.12f" % x for x in lati], area, cen, c0, MT.distanza(L, cen, c0)))
    print("=" * 130)
    esito("i tre lati uguali entro %g al tick 0 (il lato atteso %.9f)" % (TOLL_LATI, TE.lato(*AB)), max(lati) - min(lati) <= TOLL_LATI and abs(lati[0] - TE.lato(*AB)) <= TOLL_LATI, "max - min %.3e" % (max(lati) - min(lati)))
    esito("i vertici A, B, C in senso antiorario (l'area con segno positiva)", area > 0.0, "%+.4f" % area)
    if FALLITE:
        print("### FERMO: un DEVE prima della corsa fallisce (%s)" % FALLITE)
        return 1
    MTR.VARIANTI["t120"] = (0, 0, 0)                                # ### i numeri non contano: il francobollo e' quello di L 162
    MTR.francobollo = TV.francobollo_L162
    MTR.posti = (lambda c0_, frs, L_: [list(v) for v in V[:len(frs)]])
    MT.incolla = incolla_fase
    CT.Corsa = CorsaT120
    print("### mattone_triangolo.corsa con la variante t120, il francobollo di L 162, i vertici equilateri, le fasi 0, 120, 240 e la Corsa con le misure di B3, SOSTITUITI in memoria")
    try:
        ok = MTR.main(["corsa", "--variante", "t120"] + list(argv))
    except RuntimeError as x:
        print("### FERMO: %s" % x)
        ok = 1
    finally:
        CT.Corsa = _Corsa
        MT.incolla = _incolla
    print("=" * 130)
    if FOTO["k"]:
        with MT.scena(MT.CORSA_162, MT.T_162) as Z:
            geo = geometria(Z)
        f = os.path.join(MT.DIR_REF, "triangolo_t120_mappe.npz")
        np.savez_compressed(f, tick=np.array(FOTO["k"], dtype=np.int16), rho=np.stack(FOTO["rho"]), dphi=np.stack(FOTO["dphi"]), E=np.stack(FOTO["E"]), centri=np.stack(FOTO["centri"]), **geo)
        print("### LE MAPPE: %d fotogrammi in %s, %.1f MB" % (len(FOTO["k"]), f, os.path.getsize(f) / 1e6))
    f = os.path.join(MT.DIR_REF, "triangolo_t120_giro.npz")
    np.savez_compressed(f, **{x: np.array(v) for x, v in GIRO.items()})
    print("### IL GIRO, LA MASSA TOTALE E OLTRE R_A in %s; oltre R_A %g il massimo %.3e (Luca 10:29, B4: qui solo scritta)" % (f, MTR.R_A_SCENA, max(GIRO["fuori"]) if GIRO["fuori"] else float("nan")))
    print("=" * 130)
    print("ESITO (triangolo_120): %d/%d controlli come devono; fallite %s; mattone_triangolo.corsa ha reso %s" % (OK[0], OK[1], FALLITE, ok))
    return 0 if (not FALLITE and ok == 0) else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("azione", choices=("corsa",))
    ap.add_argument("--registro")
    x = ap.parse_args(argv)
    return corsa(["--registro", x.registro] if x.registro else [])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
