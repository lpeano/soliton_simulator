# -*- coding: utf-8 -*-
r"""**LA PROVA DELLA RIPRESA** *(Luca `2026-11-16` `20:35`, R2-R3; la carta `doc/TASK_HISTORY/2026-11-16_notte_verifica.md`, sez. `2.2`)*.

    E:\python\py3132\python.exe csv/solitone/notte_prova.py --nome PR-coppia --tipo coppia --L 297 --d 35 --fase 0 --R_A 85.06 --log <scratchpad> --paralleli 2
    E:\python\py3132\python.exe csv/solitone/notte_prova.py --nome PR-t120 --tipo triangolo --L 339 --R_A 97.16 --log <scratchpad> --paralleli 2

### **Sulla SCENA VERA dello strumento:** **`notte.py avvio`** *(lo stato a `k 0`)*, **copiato in quattro archivi; poi, ognuno in un PROCESSO NUOVO:** **(a) `0 -> 40`; (b) `0 -> 20`, poi `--da 20 -> 40`; (c) `0 -> 40` fermato a `25`** *(fuori dal passo, come le `08:00`)*, **poi `--da 25 -> 40`; (d) DEVE FALLIRE: l'archivio di (b) con UN BYTE CAMBIATO nello stato `40`, `--da ultimo -> 40`: lo stato `40` va RIFIUTATO, si riparte da `20`.**
### **IL CRITERIO** *(scritto prima)*: **lo stato a `k 40` di (b), (c), (d) = quello di (a), OGNI chiave, la differenza massima `0`; le serie unite = quelle di (a)** *(tutte le chiavi dei pezzi tranne `regola`, il registro dei controlli fatti ai salvataggi)*; **il controllo del comparatore** *(DEVE FALLIRE: lo stato `40` di (a) contro il suo stato `20`)*.
"""
import argparse
import concurrent.futures as CF
import glob
import os
import shutil
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import notte as N  # noqa: E402

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota, deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-110s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def lancia(args, log):
    with open(log, "w", encoding="utf-8") as fh:
        r = subprocess.run([sys.executable, os.path.join(_QUI, "notte.py")] + args, stdout=fh, stderr=subprocess.STDOUT, cwd=os.path.dirname(_CSV))
    return r.returncode


def ondata(lavori, paralleli):
    with CF.ThreadPoolExecutor(max_workers=paralleli) as ex:
        fut = {ex.submit(lancia, a, lg): (a, lg) for a, lg in lavori}
        out = {}
        for f in CF.as_completed(fut):
            a, lg = fut[f]
            out[lg] = f.result()
    for lg in sorted(out):
        print("    il processo %s: uscito con %d" % (os.path.basename(lg), out[lg]))
    sys.stdout.flush()
    return out


def stato(nome, k):
    with np.load(N.f_stato(nome, k)) as d:
        return {x: d[x].copy() for x in d.files}


def confronta_stati(A, B):
    """### `[(chiave, uguale, differenza massima)]` su TUTTE le chiavi; il `meta` come testo."""
    out = []
    for x in sorted(set(A) | set(B)):
        if x not in A or x not in B:
            out.append((x, False, float("inf")))
        elif x == "meta":
            out.append((x, str(A[x]) == str(B[x]), 0.0 if str(A[x]) == str(B[x]) else float("inf")))
        else:
            a, b = A[x], B[x]
            ug = a.shape == b.shape and a.dtype == b.dtype and np.array_equal(a, b, equal_nan=np.issubdtype(a.dtype, np.inexact))
            dm = float(np.max(np.abs(a.astype(complex) - b.astype(complex)))) if a.shape == b.shape and a.size else (0.0 if a.shape == b.shape else float("inf"))
            out.append((x, ug, dm))
    return out


def unita(nome):
    """### La serie unita: la catena dei pezzi da `k 0`."""
    pezzi = {}
    for f in glob.glob(os.path.join(N.cartella(nome), "pezzo_*.npz")):
        b = os.path.basename(f)
        pezzi[int(b[6:11])] = (int(b[12:17]), f)
    k, catena, S = 0, [], {}
    while k in pezzi:
        a, f = pezzi[k]
        catena.append((k, a))
        with np.load(f) as d:
            for x in d.files:
                if x != "regola" and d[x].size:
                    S.setdefault(x, []).append(d[x])
        k = a
    return catena, {x: np.concatenate(v) if v[0].ndim else np.array(v) for x, v in S.items()}


def main(argv):
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "notte.py"))
    _presidio.avvia(__file__)
    ap = argparse.ArgumentParser()
    ap.add_argument("--nome", required=True)
    ap.add_argument("--tipo", required=True, choices=("coppia", "triangolo"))
    ap.add_argument("--L", type=int, required=True)
    ap.add_argument("--R_A", type=float, required=True)
    ap.add_argument("--d", type=float, default=0.0)
    ap.add_argument("--fase", choices=("0", "pi"), default="0")
    ap.add_argument("--log", required=True)
    ap.add_argument("--paralleli", type=int, required=True)
    x = ap.parse_args(argv)
    nm = x.nome
    lg = lambda s: os.path.join(x.log, "%s_%s.txt" % (nm, s))  # noqa: E731
    print("=" * 130)
    print("LA PROVA DELLA RIPRESA (Luca 20:35, R2-R3): %s, %s su L %d, R_A %g%s; i processi a %d per volta; i log %s" % (nm, x.tipo, x.L, x.R_A, (", d %g, fase %s" % (x.d, x.fase)) if x.tipo == "coppia" else "", x.paralleli, lg("*")))
    print("=" * 130)
    for s in ("0", "a", "b", "c", "d"):
        if os.path.exists(N.cartella("%s-%s" % (nm, s))):
            print("### FERMO: l'archivio %s esiste gia' (una prova di prima): va guardato, non sovrascritto" % N.cartella("%s-%s" % (nm, s)))
            return 1
    r = ondata([(["avvio", "--nome", nm + "-0", "--tipo", x.tipo, "--L", str(x.L), "--R_A", str(x.R_A), "--d", str(x.d), "--fase", x.fase], lg("avvio"))], 1)
    if list(r.values())[0] != 0:
        print("### FERMO: l'avvio e' uscito con %d (il log %s)" % (list(r.values())[0], lg("avvio")))
        return 1
    for s in ("a", "b", "c"):
        os.makedirs(N.cartella("%s-%s" % (nm, s)))
        for f in ("scena.json", "stato_00000.npz", "stato_00000.npz.sha1"):
            shutil.copy2(os.path.join(N.cartella(nm + "-0"), f), os.path.join(N.cartella("%s-%s" % (nm, s)), f))
    c = lambda s, *a: (["corsa", "--nome", "%s-%s" % (nm, s), "--ogni", "20"] + list(a))  # noqa: E731
    ondata([(c("a", "--da", "0", "--fino", "40"), lg("a")), (c("b", "--da", "0", "--fino", "20"), lg("b1")), (c("c", "--da", "0", "--fino", "40", "--ferma-al-k", "25"), lg("c1"))], x.paralleli)
    ondata([(c("b", "--da", "20", "--fino", "40"), lg("b2")), (c("c", "--da", "25", "--fino", "40"), lg("c2"))], x.paralleli)
    shutil.copytree(N.cartella(nm + "-b"), N.cartella(nm + "-d"))
    f40 = N.f_stato(nm + "-d", 40)
    with open(f40, "r+b") as fh:
        fh.seek(os.path.getsize(f40) // 2)
        b = fh.read(1)
        fh.seek(os.path.getsize(f40) // 2)
        fh.write(bytes([b[0] ^ 1]))
    print("### (d): un byte cambiato a meta' di %s (lo sha1 scritto resta quello di prima)" % f40)
    ondata([(c("d", "--da", "ultimo", "--fino", "40"), lg("d"))], 1)
    print("-" * 130)
    print("### R1, LE CHIAVI DELLO STATO (stato_00040 di (a)): %s" % ", ".join("%s %s %s" % (k, v.dtype, v.shape) for k, v in sorted(stato(nm + "-a", 40).items())))
    A40 = stato(nm + "-a", 40)
    for s in ("b", "c", "d"):
        cf = confronta_stati(A40, stato("%s-%s" % (nm, s), 40))
        div = [(k, dm) for k, ug, dm in cf if not ug]
        print("### R2, LO STATO A k 40 DI (%s) CONTRO (a), chiave per chiave (la differenza massima): %s" % (s, "; ".join("%s %.3e%s" % (k, dm, "" if ug else " ###") for k, ug, dm in cf)))
        esito("(%s) lo stato a k 40 = quello di (a) AL BIT, OGNI chiave (%d chiavi)" % (s, len(cf)), not div, "diverse: %s" % div)
    cf = confronta_stati(A40, stato(nm + "-a", 20))
    esito("IL COMPARATORE: lo stato 40 di (a) contro il suo stato 20 risulta UGUALE", all(ug for _k, ug, _dm in cf), "%d chiavi diverse su %d" % (sum(1 for _k, ug, _dm in cf if not ug), len(cf)), deve=False)
    ca, SA = unita(nm + "-a")
    for s in ("b", "c", "d"):
        cs_, SS = unita("%s-%s" % (nm, s))
        div = [k for k in sorted(set(SA) | set(SS)) if k not in SA or k not in SS or SA[k].shape != SS[k].shape or not np.array_equal(SA[k], SS[k], equal_nan=np.issubdtype(SA[k].dtype, np.inexact))]
        print("### R2, LA SERIE UNITA DI (%s): la catena %s (di (a) %s); %d chiavi" % (s, cs_, ca, len(SS)))
        esito("(%s) la serie unita = quella di (a) da 0 a 40, AL BIT (%d chiavi, la catena fino a 40)" % (s, len(SA)), not div and cs_[-1][1] == 40, "diverse: %s" % div)
    print("### le chiavi della serie: %s" % ", ".join("%s %s" % (k, v.shape) for k, v in sorted(SA.items())))
    with open(lg("d"), encoding="utf-8") as fh:
        td = fh.read()
    esito("(d) la ripresa RIFIUTA lo stato 40 col byte cambiato (R3) e riparte da 20", "stato_00040.npz NON e' integro" in td and "da k 20" in td, "il log %s" % lg("d"))
    sc = N.leggi_scena(nm + "-0")
    print("### R3, GLI SHA1: lo stato a k 0 %s (scritto %s); a k 40: %s" % (N.sha1_file(N.f_stato(nm + "-0", 0))[:8], sc["sha1_k0"][:8],
          "; ".join("(%s) %s" % (s, N.sha1_file(N.f_stato("%s-%s" % (nm, s), 40))[:8]) for s in "abcd")))
    print("=" * 130)
    print("ESITO (%s): %d/%d controlli come devono; fallite %s" % (nm, OK[0], OK[1], FALLITE))
    print("    R-SCATOLA al 5%% a k 0: R_ogg %.1f (scena.json); il residuo di Gauss %.3e" % (sc["R_ogg5_k0"], sc["g0"]))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
