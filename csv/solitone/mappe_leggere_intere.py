# -*- coding: utf-8 -*-
r"""**LE MAPPE LEGGERE DELLE CORSE INTERE** *(Luca `2026-11-11` `23:31`; per i video del guardiano; il task history `doc/TASK_HISTORY/2026-11-11_mappe_leggere_intere.md`)*. [[PIANO-2D-3D]] [[VUOTO-SUL-FONDO]]

    python csv/solitone/mappe_leggere_intere.py --corsa C35-0  > doc/referti_l2/mappe_leggere_intere_C35-0.txt
    python csv/solitone/mappe_leggere_intere.py --corsa C35-pi > doc/referti_l2/mappe_leggere_intere_C35-pi.txt
    python csv/solitone/mappe_leggere_intere.py --corsa S162   > doc/referti_l2/mappe_leggere_intere_S162.txt
    python csv/solitone/mappe_leggere_intere.py --corsa C50-0  > doc/referti_l2/mappe_leggere_intere_C50-0.txt

**Nessuna corsa: `E:` solo in lettura.** Dalle mappe complete *(`rho`, `Lambda` in `float32`, ogni `100` tick)* **un fotogramma ogni `2000` tick, da `0` a `200000`**, nello stesso formato
di `mappe_leggere.npz` *(`carta_campo.py`: `rho` e `Lambda - Lambda(t 0)` in `float16`, il centro da `toro.centro` sulla `rho` in `float64`, `d1`, `d2`, `L`, `ogni`; e per le corse di
`L 162` `centro_bordo`, `R_A`, `g_max` dal `bordo` del jsonl)*, con `np.savez_compressed`, in `doc/referti_l2/campo_<corsa>/mappe_leggere_intere.npz`.
### **I DEVE:** `F0` lo `sha1` di ogni file = l'indice; `101` fotogrammi da `0` a `200000`; **ai tick comuni con `mappe_leggere.npz` gli stessi `rho`, `dLambda`, `centro` entro la precisione
di `float16`** *(Luca)*, e lo stesso confronto spostato di un fotogramma **DEVE FALLIRE**; il file sotto `15 MB`.
"""
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

CORSE = ("C35-0", "C35-pi", "S162", "C50-0")   # ### Luca 23:31
PASSO = 2000                  # ### Luca 23:31: un fotogramma ogni 2000 tick
T_FINE = 200000               # ### Luca 23:31: da 0 a 200000
TETTO_MB = 15.0               # ### Luca 23:31: ogni file sotto i 15 MB
EPS16 = 2.0 ** -10            # ### la precisione relativa di float16 (10 bit di mantissa)
MIN16 = 2.0 ** -24            # ### il passo minimo di float16 (i subnormali)
DIR_REF = os.path.join(solitone.RADICE, "doc", "referti_l2")
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-110s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return buono


def dentro16(a, b):
    """### `|a - b| <= EPS16 |b| + MIN16`, elemento per elemento, e lo scarto relativo piu' grande."""
    a, b = np.asarray(a, dtype=np.float64), np.asarray(b, dtype=np.float64)
    d = np.abs(a - b)
    return bool(np.all(d <= EPS16 * np.abs(b) + MIN16)), float(np.max(d / (np.abs(b) + MIN16)))


def main(argv):
    corsa = argv[argv.index("--corsa") + 1]
    assert corsa in CORSE, "la corsa %s NON e' fra %s" % (corsa, CORSE)
    import _presidio
    import _vuoto_vivo_B as V
    from solitone import corsa_accensione as CA
    from solitone import mappe as MP
    from solitone import toro as TO
    for m in ("__init__", "toro", "mappe", "corsa_accensione"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    _sol, _vuoto, s = V.CORSE[CA.NOME]
    print("=" * 130)
    print("LE MAPPE LEGGERE INTERE (Luca 23:31) di %s: da E: (solo lettura), un fotogramma ogni %d tick da 0 a %d; s %g; float16 (eps %g); il tetto %g MB" % (corsa, PASSO, T_FINE, s, EPS16, TETTO_MB))
    print("=" * 130)
    # ------------------------------------------------------------------ F0: i file e l'indice
    with open(os.path.join(DIR_REF, "mappe_indice_%s.txt" % corsa), encoding="utf-8") as f:
        idx = {}
        for riga in f:
            m = re.search(r"(E:\\soliton_simulator\\mappe\\%s\\%s_\d+\.npz)\s+(\d+) byte\s+sha1 ([0-9a-f]{40})" % (re.escape(corsa), re.escape(corsa)), riga)
            if m:
                idx[m.group(1)] = m.group(3)
    files = list(idx)
    cartella = os.path.join(MP.RADICE, corsa)
    presenti = sorted(os.path.join(cartella, x) for x in os.listdir(cartella) if x.endswith(".npz"))
    sha = {f: MP.sha1(f) for f in files}
    esito("F0 lo sha1 di ogni file delle mappe = l'indice, e i file su E: sono quelli dell'indice", all(sha[f] == idx[f] for f in files) and presenti == sorted(files), "%d file" % len(files))
    # ------------------------------------------------------------------ i fotogrammi (il calcolo di carta_campo.py)
    legg_t, legg_r, legg_l, legg_c = [], [], [], []
    L0 = None
    L = m1 = m2 = d1 = d2 = None
    for f in files:
        with np.load(f) as d:
            T, RH, LA = d["t"], d["rho"], d["Lambda"]
            if L is None:
                L, d1, d2 = int(d["L"]), d["d1"].copy(), d["d2"].copy()
                m1, m2 = d1.astype(np.int64) + L // 2, d2.astype(np.int64) + L // 2
            assert np.array_equal(d["d1"], d1) and np.array_equal(d["d2"], d2), "l'ordine dei nodi cambia fra i file"
        for i in range(len(T)):
            t = int(T[i])
            if L0 is None:
                assert t == 0, "la prima istantanea NON e' a t 0"
                L0 = LA[i].astype(np.float64)
            if t % PASSO or t > T_FINE:
                continue
            rho = RH[i].astype(np.float64)
            la = LA[i].astype(np.float64)
            c1, c2, _x, _y = TO.centro(rho, m1, m2, L)
            legg_t.append(t)
            legg_r.append(rho.astype(np.float16))
            legg_l.append((la - L0).astype(np.float16))
            legg_c.append((c1, c2))
    tt = np.array(legg_t)
    esito("i fotogrammi: %d, da 0 a %d ogni %d" % (T_FINE // PASSO + 1, T_FINE, PASSO), np.array_equal(tt, np.arange(0, T_FINE + 1, PASSO)), "%d, da %d a %d" % (len(tt), tt[0], tt[-1]))
    rr = CA.serie(corsa)[0]
    bor0 = rr[0]["bordo"]
    dati = dict(t=tt, tempo=(tt * s).astype(np.float32), rho=np.stack(legg_r), dLambda=np.stack(legg_l), centro=np.array(legg_c, dtype=np.float32),
                d1=d1.astype(np.int16), d2=d2.astype(np.int16), L=np.int64(L), ogni=np.int64(PASSO // 100),
                centro_bordo=np.array(bor0["c0"], dtype=np.float32), R_A=np.float64(bor0["R_A"]), g_max=np.float64(bor0["g_max"]))
    # ------------------------------------------------------------------ il DEVE di Luca: i tick comuni con mappe_leggere.npz
    vecchio = os.path.join(DIR_REF, "campo_%s" % corsa, "mappe_leggere.npz")
    if os.path.exists(vecchio):
        with np.load(vecchio) as v:
            vt, vr, vl, vc = v["t"], v["rho"], v["dLambda"], v["centro"]
            stessi = [k for k in v.files if k not in ("t", "tempo", "rho", "dLambda", "centro", "ogni")]
            uguali_extra = all(np.array_equal(v[k], dati[k]) for k in stessi)
        comuni = [int(x) for x in vt if x % PASSO == 0 and x <= T_FINE]
        jn = [int(np.where(tt == x)[0][0]) for x in comuni]
        jv = [int(np.where(vt == x)[0][0]) for x in comuni]
        er, sr = dentro16(dati["rho"][jn], vr[jv])
        el, sl = dentro16(dati["dLambda"][jn], vl[jv])
        ec, sc = dentro16(dati["centro"][jn], vc[jv])
        print("  i tick comuni con mappe_leggere.npz: %d (da %d a %d); lo scarto relativo piu' grande rho %.3e, dLambda %.3e, centro %.3e; al bit: rho %s, dLambda %s, centro %s"
              % (len(comuni), comuni[0], comuni[-1], sr, sl, sc, np.array_equal(dati["rho"][jn], vr[jv]), np.array_equal(dati["dLambda"][jn], vl[jv]), np.array_equal(dati["centro"][jn], vc[jv])))
        esito("(Luca) ai tick comuni rho, dLambda e centro = mappe_leggere.npz entro la precisione di float16", er and el and ec, "rho %.2e dLambda %.2e centro %.2e" % (sr, sl, sc))
        esito("d1, d2, L, centro_bordo, R_A, g_max = mappe_leggere.npz (%s)" % ", ".join(stessi), uguali_extra, "")
        fr, _x = dentro16(dati["rho"][jn[1:]], vr[jv[:-1]])
        fl, _x = dentro16(dati["dLambda"][jn[1:]], vl[jv[:-1]])
        esito("lo stesso confronto spostato di un fotogramma (t contro t - %d)" % PASSO, fr and fl, "", deve=False)
    else:
        print("  ### nessun mappe_leggere.npz per %s: il confronto ai tick comuni NON si puo' fare (dichiarato)" % corsa)
    # ------------------------------------------------------------------ il file
    out = os.path.join(DIR_REF, "campo_%s" % corsa, "mappe_leggere_intere.npz")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = out + ".tmp.npz"
    np.savez_compressed(tmp, **dati)
    os.replace(tmp, out)
    b = os.path.getsize(out)
    print("  il file %s: %d byte (%.2f MB); %d fotogrammi; rho fino a %.4e; |dLambda| fino a %.4e" % (os.path.relpath(out, solitone.RADICE), b, b / 1e6, len(tt), float(dati["rho"].max()), float(np.abs(dati["dLambda"]).max())))
    esito("il file sotto %g MB" % TETTO_MB, b <= TETTO_MB * 1e6, "%d byte" % b)
    print("  lo sha1 del file: %s" % MP.sha1(out))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
