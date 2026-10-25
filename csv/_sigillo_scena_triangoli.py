# -*- coding: utf-8 -*-
r"""**IL SIGILLO DELLA SCENA A TRIANGOLI NEL NUCLEO** *([[DECISIONE-SOLO-TRIANGOLI]], [[N-DIREZIONI-DI-MOTO]], [[CENSIMENTO-DECISIONI]])*.

> ### ⛔ **Il task history e' `2026-10-25_scena_triangoli_nucleo.md`** *(`6ea2ba20`: i criteri fissati prima)*. ### **Il nucleo: `primo_ordine/corrente.py` (`toro_spostamenti`) e `primo_ordine/scena_l2.py`
> (`GRIGLIE`, `GRIGLIA_DEL_MODELLO`, `versori`, `scena_toro`).** ### **Lo strumento di confronto: `csv/_triangoli.py`, NON cambiato.** ### **Il quadrato di prima: `scena_l2.py` al commit `RIF`, letto con
> `git show` ed eseguito in memoria** *(il padre del cambiamento, `H-P8`)*.

Gira con:  python csv/_sigillo_scena_triangoli.py > doc/referti_l2/sigillo_scena_triangoli.txt
"""
import contextlib
import io
import json
import os
import subprocess
import sys
import types

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

RIF = "6ea2ba20"                 # ### il padre del cambiamento: il task history della parte A
LATI = ((6, 6), (12, 12), (48, 48), (96, 6))
LATI_QUADRATO = ((7, 7), (6, 6))
LATI_TORO = ((7, 7), (6, 6), (5, 4, 3))
LATO_MATRICE = 48
S_MATRICE = 0.05
S_LIVELLI = (0.05, 0.1, 0.3)
EPS_LIVELLI = (0.0, 0.5)
RIF_BASSA = "8781162c"
IMPRONTA = "2e7f795d2a52fbe7"
TOLL_LIV = 1e-12
JSONL = os.path.join(RADICE, "doc", "referti_l2", "sigillo_scena_triangoli.jsonl")
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if deve and not passa:
        FALLITE.append(che)
    print("  %-100s %s   %s" % (che[:100], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scrivi(r):
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def git_show(rel):
    return subprocess.run(["git", "show", "%s:%s" % (RIF, rel)], capture_output=True, cwd=RADICE, check=True).stdout


def modulo_al(rel, nome):
    m = types.ModuleType(nome)
    m.__file__ = os.path.join(RADICE, rel)
    exec(compile(git_show(rel).decode("utf-8"), m.__file__, "exec"), m.__dict__)
    return m


def diversi(a, b):
    import _triangoli_forza as TF
    ba, bb = TF.byte_attr(a), TF.byte_attr(b)
    return sorted(k for k in set(ba) | set(bb) if ba.get(k) != bb.get(k)), len(ba)


def st_diversi(s1, s2):
    return sorted(k for k in set(s1) | set(s2) if k not in s1 or k not in s2 or s1[k].tobytes() != s2[k].tobytes())


@contextlib.contextmanager
def scena_del_nucleo():
    """### **`_triangoli.scena_toro` sostituita IN MEMORIA dalla scena del nucleo** *(per `matrice_tick`)*: ### **la griglia per tuple diventa il suo NOME.**"""
    import _triangoli as T
    import scena_l2 as SC
    vero = T.scena_toro
    nomi = {tuple(map(tuple, v[0])): k for k, v in SC.GRIGLIE.items()}

    def scena_toro(griglia, lati, dtau, x):
        # ### ⚠ **la moneta:** gli strumenti di `csv/` la cambiano con la globale `_triangoli.EPS_MONETA`, il nucleo la prende dalla tabella (`0.5`): ### **qui si passa quella dello strumento**
        inc, mot, st, par = SC.scena_toro(nomi[tuple(map(tuple, griglia[0]))], lati, dtau, x)
        return inc, mot, st, dict(par, eps=T.EPS_MONETA)
    T.scena_toro = scena_toro
    try:
        yield
    finally:
        T.scena_toro = vero


def main(argv):
    del argv
    import _presidio
    import _triangoli as T
    import _triangoli_bassa_energia as BE
    import _universalita_massa as UM
    import composizione as CM
    import corrente as CO
    import scena_l2 as SC
    _presidio.avvia(__file__)
    print("=" * 110)
    print("IL SIGILLO DELLA SCENA A TRIANGOLI NEL NUCLEO (DECISIONE-SOLO-TRIANGOLI)")
    print("=" * 110)
    blobs = {p: UM.blob(p) for p in ("primo_ordine/corrente.py", "primo_ordine/scena_l2.py", "primo_ordine/leggi/leggi.yaml", "csv/_triangoli.py", "csv/_sigillo_scena_triangoli.py",
                                     "soliton_simulator.py")}
    print("  i blob nel repo: %s" % "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items()))
    print("  la configurazione: RIF %s; LATI %s; LATI_QUADRATO %s; LATI_TORO %s; LATO_MATRICE %d S_MATRICE %g; S_LIVELLI %s EPS_LIVELLI %s RIF_BASSA %s; TOLL_LIV %g"
          % (RIF, LATI, LATI_QUADRATO, LATI_TORO, LATO_MATRICE, S_MATRICE, S_LIVELLI, EPS_LIVELLI, RIF_BASSA, TOLL_LIV))
    print("-" * 110)
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs, "rif": RIF})
    # ### (a) i triangoli al bit contro lo strumento
    for lati in LATI:
        iN, mN, sN, pN = SC.scena_toro("triangoli", lati, 1.0, 0.1)
        iT, mT, sT, pT = T.scena_toro(T.TRIANGOLI, lati, 1.0, 0.1)
        di, ni = diversi(iN, iT)
        dm, nm = diversi(mN, mT)
        ds = st_diversi(sN, sT)
        T.camminata(sN, mN, pN)
        T.camminata(sT, mT, pT)
        dt = st_diversi(sN, sT)
        ok = not di and not dm and not ds and not dt and pN == pT
        esito("DEVE PASSARE (a): i triangoli del nucleo = csv/_triangoli.scena_toro al bit, lati %s (incidenza, motore, stato, un tick)" % (lati,), ok,
              "attributi %d + %d; diversi %s %s %s, dopo un tick %s" % (ni, nm, di[:2], dm[:2], ds, dt))
        scrivi({"tipo": "a", "lati": list(lati), "incidenza": di, "motore": dm, "stato": ds, "tick": dt, "n_attributi": ni + nm})
    # ### (b) la matrice del tick e i livelli
    A_T = T.matrice_tick(T.TRIANGOLI, LATO_MATRICE, S_MATRICE)
    with scena_del_nucleo():
        A_N = T.matrice_tick(T.TRIANGOLI, LATO_MATRICE, S_MATRICE)
    esito("DEVE PASSARE (b): la matrice del tick con la scena del nucleo = quella dello strumento AL BIT (lato %d, s %g)" % (LATO_MATRICE, S_MATRICE),
          A_T.tobytes() == A_N.tobytes(), "%.1e" % float(np.max(np.abs(A_T - A_N))))
    liv = {}
    for l in subprocess.run(["git", "show", "%s:doc/referti_l2/triangoli_bassa_energia.jsonl" % RIF_BASSA], capture_output=True, cwd=RADICE, check=True).stdout.decode("utf-8").splitlines():
        r = json.loads(l)
        if r.get("tipo") == "livelli":
            liv[(r["eps"], r["s"])] = r["livelli"]["K"]
    peg = 0.0
    with scena_del_nucleo():
        for eps in EPS_LIVELLI:
            for s in S_LIVELLI:
                A = BE.matrice(eps, s, LATO_MATRICE, "simm")
                W = -np.angle(np.linalg.eigvals(A[16, 16, :12, :12]))
                w = np.sort(np.array([float((x + np.pi) % (2 * np.pi) - np.pi) for x in W]))
                lv = []
                for x in w:
                    if lv and abs(x - lv[-1][0]) < 1e-9:
                        lv[-1][1] += 1
                    else:
                        lv.append([float(x), 1])
                r = liv[(eps, s)]
                assert [m for _, m in lv] == [m for _, m in r]
                peg = max(peg, max(abs(a[0] - b[0]) for a, b in zip(lv, r)))
    esito("DEVE PASSARE (b): i livelli a K con la scena del nucleo contro %s entro %g (eps %s, s %s)" % (RIF_BASSA, TOLL_LIV, EPS_LIVELLI, S_LIVELLI), peg <= TOLL_LIV, "%.1e" % peg)
    scrivi({"tipo": "b", "livelli": peg})
    # ### (c) il quadrato
    for lati in LATI_QUADRATO:
        iN, mN, sN, pN = SC.scena_toro("quadrato_di_servizio", lati, 1.0, 0.1)
        iT, mT, sT, pT = T.scena_toro(T.QUADRATO, lati, 1.0, 0.1)
        di, _ = diversi(iN, iT)
        dm, _ = diversi(mN, mT)
        ds = st_diversi(sN, sT)
        esito("DEVE PASSARE (c): il quadrato di servizio del nucleo = csv/_triangoli.scena_toro(QUADRATO) al bit, lati %s" % (lati,), not di and not dm and not ds, "%s %s %s" % (di[:2], dm[:2], ds))
    peg = []
    for lati in LATI_TORO:
        a = CO.toro(lati)
        assi = tuple(tuple(1 if j == i else 0 for j in range(len(lati))) for i in range(len(lati)))
        b = CO.toro_spostamenti(lati, assi)
        peg.append(a[0].tobytes() == b[0].tobytes() and a[1].tobytes() == b[1].tobytes() and a[2] == b[2])
    esito("DEVE PASSARE (c): corrente.toro = toro_spostamenti sugli assi AL BIT, lati %s" % (LATI_TORO,), all(peg), str(peg))
    vecchio = modulo_al("primo_ordine/scena_l2.py", "_scena_l2_prima")
    args = (0.5, 1.0, 1.0, 2, True, True, False, 7, 1)
    o = vecchio.scena(*args)
    n = SC.scena(*args)
    dif = []
    for x, y in zip(o[:3], n[:3]):
        dif += diversi(x, y)[0] if not isinstance(x, dict) else st_diversi(x, y)
    esito("DEVE PASSARE (c): scena_l2.scena (il quadrato di oggi) identica al bit prima (%s) e dopo" % RIF, not dif and o[3] == n[3] and o[4] == n[4] and o[5] == n[5], "%s" % dif[:3])
    # ### (d) la griglia del modello
    iD, mD, sD, pD = SC.scena_toro(SC.GRIGLIA_DEL_MODELLO, (12, 12), 1.0, 0.1)
    gradi = sorted(set(int(g) for g in iD.grado))
    esito("DEVE FALLIRE, PER LA CHIAVE GIUSTA: <<la griglia del modello e' il quadrato>>; la chiave: e' %r e la sua scena ha grado 6 a ogni nodo" % SC.GRIGLIA_DEL_MODELLO,
          SC.GRIGLIA_DEL_MODELLO != "quadrato_di_servizio" and SC.GRIGLIA_DEL_MODELLO == "triangoli" and gradi == [6], "i gradi %s" % gradi)
    # ### (e) la trappola dello zip
    alzato = ""
    try:
        CO.toro_spostamenti((6, 6), ((1, 0, 0),))
    except AssertionError as e:
        alzato = str(e)[:70]
    esito("DEVE FALLIRE: toro_spostamenti con lati di 2 elementi e spostamenti di 3 ALZA (la trappola dello zip chiusa)", bool(alzato), alzato)
    # ### (f) la tabella e l'impronta
    lb = git_show("primo_ordine/leggi/leggi.yaml") == io.open(os.path.join(RADICE, "primo_ordine", "leggi", "leggi.yaml"), "rb").read()
    esito("DEVE PASSARE (f): leggi.yaml identico a %s e l'impronta %s" % (RIF, IMPRONTA), lb and CM.IMPRONTA == IMPRONTA, "leggi.yaml %s, impronta %s" % (lb, CM.IMPRONTA))
    print("-" * 110)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
