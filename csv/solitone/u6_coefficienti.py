# -*- coding: utf-8 -*-
r"""**U6 DELL'UNIFICAZIONE: LE FORME DEI COEFFICIENTI DELLO SPOSTAMENTO, SUL BANCO** *(Luca `2026-11-12` `10:39`; il task history `doc/TASK_HISTORY/2026-11-12_unificazione.md`, sez. `8`)*. [[PIANO-2D-3D]] [[H-NUCLEO-CONGELATO]]

    python csv/solitone/u6_coefficienti.py --forma <oggi|k1|k2|k3|sbagliata> --esegui <script> [argomenti]
    python csv/solitone/u6_coefficienti.py --forma <...> --tbs --uscita <file.npz>
    python csv/solitone/u6_coefficienti.py --confronta <cartella> > doc/referti_l2/u6_coefficienti.txt

### **FUORI DAL NUCLEO:** **un avvolgimento IN MEMORIA di `flussi_parziali`** *(una seconda fonte di sola prova, dichiarata; il nucleo non cambia)*:
- **oggi:** nessun avvolgimento;
- **(k1) `|z| = 1`:** `_alfa_beta` con `z / |z|`;
- **(k2) `alpha + beta = 1`:** `beta = (1 - z)/2`, `alpha = 1 - beta`;
- **(k3) `I - beta (I - S)`:** `_hop_psi_mezzo` e `_hop_phi_mezzo` riscritti: `nuovo_0 = v0 - beta (v0 - U^dag v1)`, `nuovo_1 = v1 - beta (v1 - U v0)` *(per `phi` senza `U`)*;
- **sbagliata** *(il DEVE FALLIRE)*: `alpha` di oggi per `1 + 1e-12`.
**`--esegui`:** lo script dato gira NELLO STESSO PROCESSO dopo l'avvolgimento *(`runpy`; T1 `lambda_vuoto_deriva.py`, la cassetta `collauda.py`)*. ### **M-B1 NON si misura cosi':** **lancia
sottoprocessi su alberi materializzati, e l'avvolgimento in memoria non ci arriva** *(dichiarato: si misura sulla forma scelta da Luca, applicata a un albero temporaneo)*.
**`--tbs`:** `1000` tick da TBS a `10000` col ciclo della corsa *(`riproduzione_unificazione.misura` sul nucleo di questo albero)*, **cronometrati.**
**`--confronta`:** **la deriva di `Lambda` per tick** *(dall'uscita di T1: la media della deriva al tick `1000` / `1000` / `Lambda` del vuoto)*, **la rms di `rho` dopo `1000` tick contro oggi, gli sha,
il tempo per tick, l'esito della cassetta;** **le letture della sez. `8.4`;** **DEVE FALLIRE: la forma sbagliata con una deriva entro `100` volte quella di oggi** *(«visibile» = oltre: mio, dichiarato)*.
"""
import contextlib
import json
import math
import os
import re
import runpy
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

FORME = ("oggi", "k1", "k2", "k3", "sbagliata")
SBAGLIO = 1e-12                # ### il DEVE FALLIRE (la carta, sez. 8.2)
SOGLIA_CURA = 3.7e-17          # ### Luca 17:37 (sez. 8.5): un decimo della deriva di oggi (3.7e-16 relativa); la carta diceva 1e-17, un errore mio
SOGLIA_FISICA = 1e-10          # ### la carta, sez. 8.4: la rms di rho relativa
VISIBILE = 100.0               # ### mio (dichiarato): «visibile» = oltre 100 volte la deriva di oggi
LAMBDA_V = 6.0                 # ### Lambda del vuoto F3 per nodo (T1: «Lambda 6»)
OK = [0, 0]
FALLITE = []


def prendi(argv, nome):
    return argv[argv.index(nome) + 1] if nome in argv else None


@contextlib.contextmanager
def avvolgi(forma):
    import flussi_parziali as FP
    ab0, hp0, hf0 = FP._alfa_beta, FP._hop_psi_mezzo, FP._hop_phi_mezzo

    def ab_k1(mot, z):
        zn = z / np.abs(z)
        return (1.0 + zn) / 2.0, (1.0 - zn) / 2.0

    def ab_k2(mot, z):
        be = (1.0 - z) / 2.0
        return 1.0 - be, be

    def ab_sb(mot, z):
        al, be = ab0(mot, z)
        return al * (1.0 + SBAGLIO), be

    def hp_k3(mot, psi, frazione):
        m = mot.inc.m
        v = psi.reshape(m, 2, 2)
        U = mot.geo.U
        be = (1.0 - FP.z_arco(mot, frazione)) / 2.0
        v0, v1 = v[:, 0, :].copy(), v[:, 1, :].copy()
        Ud1 = np.einsum("aji,aj->ai", np.conj(U), v1)
        U0 = np.einsum("aij,aj->ai", U, v0)
        v[:, 0, :] = v0 - be * (v0 - Ud1)
        v[:, 1, :] = v1 - be * (v1 - U0)
        return psi

    def hf_k3(mot, phi, frazione):
        m = mot.inc.m
        v = phi.reshape(m, 2)
        be = ((1.0 - FP.z_arco(mot, frazione)) / 2.0).reshape(-1)
        v0, v1 = v[:, 0].copy(), v[:, 1].copy()
        v[:, 0] = v0 - be * (v0 - v1)
        v[:, 1] = v1 - be * (v1 - v0)
        return phi
    try:
        if forma == "k1":
            FP._alfa_beta = ab_k1
        elif forma == "k2":
            FP._alfa_beta = ab_k2
        elif forma == "sbagliata":
            FP._alfa_beta = ab_sb
        elif forma == "k3":
            FP._hop_psi_mezzo, FP._hop_phi_mezzo = hp_k3, hf_k3
        else:
            assert forma == "oggi", forma
        print("[U6] la forma %s: flussi_parziali._alfa_beta %s, _hop_psi_mezzo %s, _hop_phi_mezzo %s" % (
            forma, FP._alfa_beta.__name__, FP._hop_psi_mezzo.__name__, FP._hop_phi_mezzo.__name__))
        sys.stdout.flush()
        yield
    finally:
        FP._alfa_beta, FP._hop_psi_mezzo, FP._hop_phi_mezzo = ab0, hp0, hf0


def esegui(forma, script, args):
    with avvolgi(forma):
        sys.argv = [script] + list(args)
        try:
            runpy.run_path(script, run_name="__main__")
        except SystemExit as ex:
            return int(ex.code or 0)
    return 0


def tbs(forma, uscita):
    from solitone import riproduzione_unificazione as RU
    radice = os.path.dirname(os.path.dirname(_QUI))
    with avvolgi(forma):
        t0 = time.time()
        RU.misura(radice, "TBS", uscita)
        dt = time.time() - t0
    with open(uscita + ".tempo.json", "w", encoding="utf-8") as f:
        json.dump({"forma": forma, "secondi": dt, "N": RU.N_TICK}, f)
    print("[U6] la forma %s: %d tick in %.1f s" % (forma, RU.N_TICK, dt))
    return 0


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-104s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:104], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def confronta(cart):
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("U6, LE FORME DEI COEFFICIENTI SUL BANCO (la carta: il task history dell'unificazione, sez. 8): %s; le uscite in %s" % (", ".join(FORME), cart))
    print("=" * 130)
    ris = {}
    for f in FORME:
        r = {}
        t1 = open(os.path.join(cart, "t1_%s.txt" % f), encoding="utf-8").read()
        m = re.search(r"al tick 1000: max \S+ \(\S+ ulp\), media ([+-][0-9.e+-]+)", t1)
        r["deriva"] = float(m.group(1)) / 1000.0 / LAMBDA_V if m else float("nan")
        cas = open(os.path.join(cart, "cassetta_%s.txt" % f), encoding="utf-8").read()
        m = re.search(r"ESITO: (\d+)/(\d+) controlli passano", cas)
        r["cassetta"] = "%s/%s" % (m.group(1), m.group(2)) if m else "?"
        z = np.load(os.path.join(cart, "tbs_%s.npz" % f))
        r["rho"] = z["rho"]
        r["meta"] = json.loads(str(z["meta"]))
        r["tempo"] = json.load(open(os.path.join(cart, "tbs_%s.npz.tempo.json" % f), encoding="utf-8"))["secondi"] / 1000.0
        ris[f] = r
    o = ris["oggi"]
    print("  %-10s %-24s %-22s %-14s %-12s %-10s" % ("la forma", "la deriva Lambda/tick", "la rms di rho vs oggi", "sha = oggi", "s per tick", "cassetta"))
    for f in FORME:
        r = ris[f]
        rms = float(np.sqrt(np.mean((r["rho"] - o["rho"]) ** 2)) / np.sqrt(np.mean(o["rho"] ** 2)))
        r["rms"] = rms
        print("  %-10s %+.4e %12s %.3e %10s %-14s %.4f %8s %s" % (f, r["deriva"], "", rms, "", r["meta"]["sha"] == o["meta"]["sha"], r["tempo"], "", r["cassetta"]))
    print("-" * 130)
    for f in ("k1", "k2", "k3"):
        r = ris[f]
        cura = abs(r["deriva"]) < SOGLIA_CURA or (r["deriva"] * o["deriva"] < 0 and abs(r["deriva"]) <= abs(o["deriva"]))
        print("  LA LETTURA (%s): la deriva %s (il rapporto con oggi %+.4f); la fisica %s; la cassetta %s; il tempo %.2f volte oggi; M-B1 non verificato in memoria" % (
            f, "CURATA (sotto %g o col segno cambiato senza crescere)" % SOGLIA_CURA if cura else "NON curata", r["deriva"] / o["deriva"],
            "CAMBIATA oltre l'arrotondamento (rms > %g)" % SOGLIA_FISICA if r["rms"] > SOGLIA_FISICA else "uguale entro l'arrotondamento (rms <= %g)" % SOGLIA_FISICA,
            r["cassetta"], r["tempo"] / o["tempo"]))
    sb = ris["sbagliata"]
    esito("la forma sbagliata: la deriva entro %g volte quella di oggi (deve essere VISIBILE, oltre)" % VISIBILE, abs(sb["deriva"]) <= VISIBILE * abs(o["deriva"]),
          "%+.3e contro %+.3e" % (sb["deriva"], o["deriva"]), deve=False)
    print("  la cassetta: D6 FALLISCE in tutte le forme, OGGI compresa (dal riferimento 6c97a2e3 sono entrati nella libreria script nuovi): il confronto fra le forme e' rispetto a oggi; la forma sbagliata la interrompe")
    print("  M-B1: NON misurato sul banco (lancia sottoprocessi su alberi materializzati; l'avvolgimento in memoria non ci arriva): sulla forma scelta da Luca, in un albero temporaneo")
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    print("### FERMO: la scelta della forma e' di Luca, sui numeri.")
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--confronta":
        sys.exit(confronta(a[1]))
    forma = prendi(a, "--forma")
    assert forma in FORME, "la forma %r non e' fra %s" % (forma, FORME)
    if "--esegui" in a:
        i = a.index("--esegui")
        sys.exit(esegui(forma, a[i + 1], a[i + 2:]))
    if "--tbs" in a:
        sys.exit(tbs(forma, prendi(a, "--uscita")))
    sys.exit("uso: vedi la docstring")
