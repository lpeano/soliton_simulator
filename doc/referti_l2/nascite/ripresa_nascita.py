# -*- coding: utf-8 -*-
r"""**[M1751-R] S1: LA RIPRESA P8 FINO AL TICK DI UNA NASCITA, E LO STATO PRIMA E DOPO** *(Luca, 2026-11-23: «le 10 riprese P8 fino al tick della nascita sono AUTORIZZATE come corse corte, priorita' 1»; la carta `doc/CARTA_gradi_di_liberta.md`, sez. `1`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe C:/Users/lpeano/wt_mitosi/doc/referti_l2/nascite/ripresa_nascita.py --nascita 269

**`mitosi_rami_v2.ciclo` COSI' COM'E'** *(modo `mitosi`, il registro della corsa no: la voce la apre la coda)*, dallo stato salvato prima della nascita `q` fino al suo tick, nella cartella `E:/soliton_simulator/controllo/M1751/ripresa_<q>`; **in memoria `Rami.nasci` avvolta:** alla nascita numero `q` *(il conto delle nascite gia' fatte = `q - 1`)* **salva lo stato PRIMA** *(`prima_<k>.npz`, con `mitosi_rami_v2.salva`)*, poi la nascita; **lo stato DOPO** subito dopo la nascita, nello stesso tick, con `mitosi_rami_v2.salva` *(`dopo_<k>.npz`: lo stesso formato di PRIMA, che `riprendi_v2` sa riaprire)*. **Il controllo (DEVE):** `k`, l'arco, il nato, `DH` e `P9` della ripresa = la voce registrata, AL BIT. **Gli stati di partenza:** la 1 `TRONCO/prima_nascita_35976.npz`; la 2, la 3 `MITOSI/stato_36000.npz`; la 10 `MITOSI/stato_36250.npz`; le altre lo stato di MITOSI_V2 con `k` < quello della nascita.
"""
import argparse
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
_SU = os.path.dirname(_QUI)
for _p in (_QUI, _SU):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import nascite_lettura as NL  # noqa: E402
import mitosi_rami_v2 as MR2V  # noqa: E402

DIR = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1751")
CAMPIONE = (1, 2, 3, 10, 269, 270, 271, 536, 537, 538)


def partenza(q, k):
    if q == 1:
        return os.path.join(NL.D_T, "prima_nascita_35976.npz")
    if q <= 9:
        return os.path.join(NL.D_1, "stato_36000.npz")
    if q == 10:
        return os.path.join(NL.D_1, "stato_36250.npz")
    ks = [kk for kk, f in NL.elenco_stati() if kk < k and os.path.dirname(f) == NL.D_2]
    return os.path.join(NL.D_2, "stato_%05d.npz" % max(ks))


def main(argv):
    import _presidio
    ap = argparse.ArgumentParser()
    ap.add_argument("--nascita", type=int, required=True)
    a = ap.parse_args(argv)
    q = a.nascita
    assert q in CAMPIONE, "la nascita %d NON e' del campione %s (la carta)" % (q, CAMPIONE)
    _presidio.avvia(os.path.join(_SU, "mitosi_rami_v2.py"))
    _presidio.avvia(os.path.join(_SU, "mitosi_regola_v2.py"))
    _presidio.avvia(__file__)
    MR2V.PS.presidi()
    B = NL.nascite()
    b0 = B[q - 1]
    k = int(b0["k"])
    f = partenza(q, k)
    d_out = os.path.join(DIR, "ripresa_%03d" % q)
    os.makedirs(d_out, exist_ok=True)
    print("### LA RIPRESA della nascita %d: k %d, l'arco %d, il nato %d; da %s; in %s" % (q, k, b0["a"], b0["nodi"]["n"], f, d_out))
    sys.stdout.flush()
    vera = MR2V.Rami.nasci
    preso = {}

    def nasci(self, Z, C, a_, k_, perche):
        if self.nascite == q - 1 and "b" not in preso:
            fp = os.path.join(d_out, "prima_%05d.npz" % k_)
            s = MR2V.salva(Z, C, self, k_, MR2V.PS.MT.G2.T0 + k_, {"nascita": q, "k": int(k_), "centro": self.centro if self.centro is not None else [0.0, 0.0], "lab": [0.0, 0.0], "tronco_scatto": False}, fp)
            print("### lo stato PRIMA della nascita %d: %s sha1 %s" % (q, os.path.basename(fp), s[:8]))
            out = vera(self, Z, C, a_, k_, perche)
            fd = os.path.join(d_out, "dopo_%05d.npz" % k_)
            s2 = MR2V.salva(Z, C, self, k_, MR2V.PS.MT.G2.T0 + k_, {"nascita": q, "k": int(k_), "centro": self.centro if self.centro is not None else [0.0, 0.0], "lab": [0.0, 0.0], "tronco_scatto": False}, fd)
            print("### lo stato DOPO la nascita %d (subito, nello stesso tick): %s sha1 %s" % (q, os.path.basename(fd), s2[:8]))
            preso["b"] = out
            return out
        return vera(self, Z, C, a_, k_, perche)
    MR2V.Rami.nasci = nasci
    try:
        cod, kf, _fine = MR2V.ciclo("RIPRESA_%03d" % q, "mitosi", f, k, None, d_out=d_out)
    finally:
        MR2V.Rami.nasci = vera
    b = preso.get("b")
    ok = b is not None and all(b[x] == b0[x] for x in ("k", "a", "DH", "P9")) and b["nodi"] == b0["nodi"]
    print("### IL CONTROLLO: la nascita %d della ripresa = la voce registrata AL BIT (k, l'arco, i nodi, DH, P9): %s" % (q, "PASSA" if ok else "### FALLISCE"))
    if b is not None:
        print("    la ripresa: k %d, l'arco %d, il nato %d, DH %.17g, P9 %.3g; la voce: k %d, l'arco %d, il nato %d, DH %.17g, P9 %.3g" % (
            b["k"], b["a"], b["nodi"]["n"], b["DH"], b["P9"], b0["k"], b0["a"], b0["nodi"]["n"], b0["DH"], b0["P9"]))
    with open(os.path.join(d_out, "controllo.json"), "w", encoding="utf-8") as fh:
        json.dump({"nascita": q, "k": k, "ok": bool(ok), "codice": cod, "k_fine": kf}, fh)
    return 0 if ok and cod == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
