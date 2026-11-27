# -*- coding: utf-8 -*-
r"""**[M2245-27] A3, IL RITMO DELLE NASCITE** *(DECISIONE DI LUCA, 2026-11-27 22:45; la carta `doc/CARTA_mitosi.md`, A3; solo letture)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_ritmo.py > doc/referti_l2/mitosi_ritmo.txt

**Finestre di `250`** da `k 36250` a `46000`; in ognuna le nascite in `10` sottofinestre di `25` tick *(`25` = il primo intervallo,
`mitosi_dati.txt`)* e **il rapporto varianza/media** dei conteggi. **La soglia (del guardiano, adottata):** **A GRADINI** se il rapporto
supera `2` in **oltre meta'** delle finestre con almeno `2` nascite; **LISCIO** se sta fra `0.5` e `2` in oltre meta'; **ALTRO** se no.
Stampati: il rapporto delle finestre di `250` su tutta la fiammata; le sottofinestre di `10` e `50` tick *(sensibilita': il verdetto resta su `25`)*.
**Casi noti** *(seme fisso)*: (K1) una nascita ogni `25` tick: rapporto `0`; (K2) Poisson: rapporto mediano fra `0.5` e `2`;
(K3) pacchetti di `5` nascite nello stesso tick: rapporto sopra `2`.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
for _p in (_QUI, os.path.join(_RADICE, "csv")):
    if os.path.abspath(_p) not in sys.path:
        sys.path.insert(0, os.path.abspath(_p))
import mitosi_costo_nodo as A1  # noqa: E402

K_INI, K_FIN, FIN = 36250, 46000, 250
OK = {}


def esito(che, ok, nota=""):
    OK[che] = bool(ok)
    print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def rapporti(ks, sub):
    """### `[(inizio, nascite, varianza/media)]` per finestra di `FIN`, con `FIN // sub` sottofinestre di `sub` tick."""
    out = []
    for a in range(K_INI, K_FIN, FIN):
        c = np.histogram(ks, bins=np.arange(a, a + FIN + 1, sub))[0].astype(float)
        m = float(c.mean())
        out.append((a, int(c.sum()), float(c.var()) / m if m > 0 else float("nan")))
    return out


def verdetto(rr):
    v = np.array([r for _, nn, r in rr if nn >= 2])
    alti, medi = int((v > 2).sum()), int(((v >= 0.5) & (v <= 2)).sum())
    if alti > len(v) / 2:
        return "A GRADINI", alti, medi, len(v)
    if medi > len(v) / 2:
        return "LISCIO", alti, medi, len(v)
    return "ALTRO", alti, medi, len(v)


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "mitosi_dati.py"))
    _presidio.avvia(os.path.join(_QUI, "mitosi_costo_nodo.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M2245-27] A3, IL RITMO DELLE NASCITE (la carta doc/CARTA_mitosi.md, A3): varianza/media per finestra di %d, sottofinestre di 25" % FIN)
    print("=" * 130)
    rng = np.random.default_rng(20261127)
    reg = np.arange(K_INI, K_FIN, 25)
    rr = rapporti(reg, 25)
    esito("(K1) una nascita ogni 25 tick: rapporto 0 in ogni finestra", all(r == 0 for _, _, r in rr), "max %.3e" % max(r for _, _, r in rr))
    poi = np.sort(rng.uniform(K_INI, K_FIN, 538))
    rr = rapporti(poi, 25)
    med = float(np.nanmedian([r for _, nn, r in rr if nn >= 2]))
    esito("(K2) Poisson (538 nascite uniformi, seme 20261127): rapporto mediano fra 0.5 e 2", 0.5 <= med <= 2.0, "mediana %.3f; il verdetto %s" % (med, verdetto(rr)[0]))
    pac = np.repeat(np.sort(rng.uniform(K_INI, K_FIN, 108)).astype(int), 5)
    rr = rapporti(pac, 25)
    med = float(np.nanmedian([r for _, nn, r in rr if nn >= 2]))
    esito("(K3) pacchetti di 5 nascite nello stesso tick: rapporto mediano sopra 2", med > 2.0, "mediana %.3f; il verdetto %s" % (med, verdetto(rr)[0]))
    # ### i dati
    ks = np.array([int(x["k"]) for x in A1.nascite()], dtype=float)
    print("-" * 130)
    print("  le nascite: %d, da k %d a %d; nella finestra [%d, %d): %d" % (len(ks), ks.min(), ks.max(), K_INI, K_FIN, int(((ks >= K_INI) & (ks < K_FIN)).sum())))
    R = {s: rapporti(ks, s) for s in (10, 25, 50)}
    print("  la finestra    nascite   var/media (sotto 10)   (sotto 25, IL VERDETTO)   (sotto 50)")
    for i, (a, nn, r25) in enumerate(R[25]):
        print("  [%5d, %5d)   %3d        %8.3f              %8.3f                 %8.3f" % (a, a + FIN, nn, R[10][i][2], r25, R[50][i][2]))
    c = np.histogram(ks, bins=np.arange(K_INI, K_FIN + 1, FIN))[0].astype(float)
    print("  le finestre di %d su tutta la fiammata: media %.3f, varianza %.3f, varianza/media %.3f" % (FIN, c.mean(), c.var(), c.var() / c.mean()))
    dt = np.diff(np.sort(ks))
    print("  gli intervalli fra nascite: medio %.2f, mediano %.1f; uguali a 0 (stesso tick) %d su %d; il coefficiente di variazione %.3f" % (
        dt.mean(), float(np.median(dt)), int((dt == 0).sum()), len(dt), dt.std() / dt.mean()))
    print("-" * 130)
    for s in (10, 50):
        v = verdetto(R[s])
        print("  sensibilita', sottofinestre di %d: %s (sopra 2 in %d, fra 0.5 e 2 in %d, su %d)" % (s, v[0], v[1], v[2], v[3]))
    v = verdetto(R[25])
    print("### IL VERDETTO (sottofinestre di 25): %s -- sopra 2 in %d finestre, fra 0.5 e 2 in %d, su %d con almeno 2 nascite" % v)
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


if __name__ == "__main__":
    sys.exit(main())
