# -*- coding: utf-8 -*-
"""IL SIGILLO DI **κ = 1 E DEL MESSAGGIO DI `--chi-basc`** — `K0` e `K1`.

*(Decisione di Luca del 2026-10-06 sera: ### **κ = 1 E' LA LEGGE**, e il messaggio di
`--chi-basc` deve dire **quale array scrive in ciascun caso**.)*

### ⛔ **IL BLOB DEL SIMULATORE CAMBIA, QUINDI IL CODICE COMPILATO VA CONFRONTATO.**

| | che cosa pretende |
|---|---|
| **`K0`** | i **code object** di tutto il modulo sono **IDENTICI** prima e dopo: `co_code`, `co_names`, e `co_consts` **elemento per elemento** — e una differenza e' ammessa **SOLO se entrambi gli elementi sono STRINGHE** *(docstring o messaggio)*. **Ricorsivo sulle funzioni annidate.** ### ⛔ **Una sola differenza che NON sia fra due stringhe: si FERMA.** |
| **`K1`** | il blob nuovo riproduce **AL BIT** i conteggi per passo di `amp0.json` sui primi `150` passi |

### ✔ **E `K1` SI APPOGGIA A `S1` DEL SIGILLO PRECEDENTE** *(`6d7107b`)*, che ha gia' stabilito
### che `30e18cdd` riproduce `amp0.json` al bit su `230` passi: **se il blob nuovo lo riproduce
### ancora, allora e' identico a `30e18cdd` su quei passi** — e **non serve una seconda corsa
### del blob vecchio.**

# ESENTE-H-P3: `S._MIS = m` NON e' una configurazione: e' un GANCIO DI SOLA LETTURA, e la
#   configurazione del modulo viene INTERAMENTE dal CLI, perche' `carica()` passa da
#   `_cli_flag` con l'argv del driver. Il sigillo prova LA LEGGE (il codice compilato e i
#   conteggi per passo), non un flag: non c'e' nessun flag nuovo da provare.

# ESENTE-H-P8: il codice di prima si prende dal PADRE del commit, col `git log`, e NON da
#   `HEAD`. La stringa qui sotto lo documenta.

USO:  python csv/_seal_fork/_sigillo_kappa_e_messaggio.py  [--passi=N]
"""
import contextlib
import io
import json
import os
import subprocess
import sys
import types

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
sys.path.insert(0, os.path.join(RADICE, "csv", "_test_fork"))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

import _passo                                    # noqa: E402
import _tors_w8_lunga as LUNGA                   # noqa: E402

blob, carica = LUNGA.blob, LUNGA.carica
stampa, riga = LUNGA.stampa, LUNGA.riga

NL = chr(10)
FUORI = os.path.join(RADICE, "csv", "_seal_fork", "_sigillo_kappa_e_messaggio")
SIM = os.path.join(RADICE, "soliton_simulator.py")
D_MZD = os.path.join(RADICE, "csv", "_test_fork", "_mitosi_zero_dove")
PASSI = 150
CAMPI = ("n", "archi", "nati_tot", "schwinger_tot")


def dal_padre(dst):
    """Il simulatore del PADRE di questo commit, ### **in BINARIO** *(mai `git checkout`)*."""
    r = subprocess.run(["git", "log", "--format=%H", "-1", "--",
                        "csv/_seal_fork/_sigillo_kappa_e_messaggio.py"],
                       capture_output=True, text=True, cwd=RADICE)
    c = r.stdout.strip()
    # ### se lo script non e' ancora committato, il padre e' `HEAD` -- e si DICHIARA.
    pad = (c + "~1") if c else "HEAD"
    g = subprocess.run(["git", "cat-file", "-p", "%s:soliton_simulator.py" % pad],
                       capture_output=True, cwd=RADICE)
    if g.returncode or not g.stdout:
        raise SystemExit("[FERMO] non leggo il simulatore dal padre `%s`." % pad)
    io.open(dst, "wb").write(g.stdout)
    return pad


def _consts(co):
    """I `co_consts`, ### **senza i code object annidati** *(confrontati a parte)*."""
    return [x for x in co.co_consts if not isinstance(x, types.CodeType)]


def _figli(co):
    return [x for x in co.co_consts if isinstance(x, types.CodeType)]


# ### ⛔ **I NUMERI DI RIGA SI SPOSTANO, E NON SONO UNA DIFFERENZA DI CODICE.**
#   Python 3.13 mette `__firstlineno__` fra i `co_consts` del corpo di OGNI classe. Aggiungere
#   righe a un docstring li sposta TUTTI dello stesso numero. ### **E' la stessa famiglia di
#   `_calcpsi_origini`**, le cui chiavi contengono numeri di riga -- e che l'altro sigillo
#   aggrega per nome ### **per la stessa ragione.**
#   ### ✔ **LO SCARTO SI MISURA, NON SI ASSUME:** e' la differenza di righe fra i due
#   file, e una differenza intera e' ammessa ### **SOLO se vale ESATTAMENTE quello.**
#   ### **Qualunque altro intero diverso FERMA il sigillo.**
DELTA_RIGHE = [0]


def confronta(a, b, dove, fuori):
    """Confronta due code object ### **ricorsivamente**, e accumula in `fuori` ogni
    differenza che ### **NON** sia fra due stringhe."""
    if a.co_code != b.co_code:
        fuori.append((dove, "co_code", "bytecode diverso", ""))
    if a.co_names != b.co_names:
        fuori.append((dove, "co_names", str(a.co_names)[:60], str(b.co_names)[:60]))
    if a.co_varnames != b.co_varnames:
        fuori.append((dove, "co_varnames", str(a.co_varnames)[:60],
                      str(b.co_varnames)[:60]))
    ca, cb = _consts(a), _consts(b)
    stringhe = []
    if len(ca) != len(cb):
        fuori.append((dove, "co_consts", "lunghezze %d != %d" % (len(ca), len(cb)), ""))
    else:
        for k, (x, y) in enumerate(zip(ca, cb)):
            if x == y and type(x) is type(y):
                continue
            # ### ✔ **AMMESSA SOLO SE ENTRAMBE SONO STRINGHE:** docstring o messaggio.
            if isinstance(x, str) and isinstance(y, str):
                stringhe.append((dove, k, x[:70], y[:70]))
            elif (isinstance(x, int) and isinstance(y, int)
                  and not isinstance(x, bool) and not isinstance(y, bool)
                  and DELTA_RIGHE[0] and (y - x) == DELTA_RIGHE[0]):
                # ### un NUMERO DI RIGA spostato ESATTAMENTE dal delta misurato
                stringhe.append((dove + " [riga]", k, str(x), str(y)))
            else:
                fuori.append((dove, "co_consts[%d]" % k, repr(x)[:60], repr(y)[:60]))
    fa, fb = _figli(a), _figli(b)
    if len(fa) != len(fb):
        fuori.append((dove, "funzioni annidate", "%d != %d" % (len(fa), len(fb)), ""))
    else:
        for x, y in zip(fa, fb):
            stringhe += confronta(x, y, dove + "/" + (x.co_name or "?"), fuori)
    return stringhe


def k0():
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    prima = os.path.join(FUORI, "_prima.py")
    pad = dal_padre(prima)
    ta = io.open(prima, encoding="utf-8").read()
    tb = io.open(SIM, encoding="utf-8").read()
    # ### lo SCARTO DI RIGHE si misura PRIMA del confronto, e si riporta nell'esito
    DELTA_RIGHE[0] = len(tb.split(NL)) - len(ta.split(NL))
    ca = compile(ta, "sim", "exec")
    cb = compile(tb, "sim", "exec")
    fuori = []
    stringhe = confronta(ca, cb, "<modulo>", fuori)
    return {"padre": pad, "delta_righe": DELTA_RIGHE[0],
            "blob_prima": blob(prima)[:8], "blob_oggi": blob(SIM)[:8],
            "differenze_fuori_dalle_stringhe": fuori[:20], "n_fuori": len(fuori),
            "stringhe_cambiate": [(d, k, x, y) for d, k, x, y in stringhe][:20],
            "n_stringhe": len(stringhe), "passa": not fuori}


def k1(passi):
    dst = os.path.join(FUORI, "_sim_nuovo.py")
    LUNGA.copia_patchata(SIM, dst)
    S, N, _a = carica("sig_kappa", dst)
    m = LUNGA.Misura(S.DT)
    S._MIS = m
    for k in range(1, passi + 1):
        m.passo = k
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(S, N)
        m.chiudi(N)
    rif = json.loads(io.open(os.path.join(D_MZD, "amp0.json"), encoding="utf-8").read())
    A = {int(x["passo"]): x for x in m.passi}
    B = {int(x["passo"]): x for x in rif["passi_dati"]}
    com = sorted(set(A) & set(B))
    diff, nq = [], 0
    for p in com:
        for c in CAMPI:
            if A[p].get(c) != B[p].get(c):
                diff.append((p, c, A[p].get(c), B[p].get(c)))
        qa, qb = A[p].get("q_tw") or {}, B[p].get("q_tw") or {}
        for z in sorted(set(qa) | set(qb)):
            nq += 1
            if qa.get(z) != qb.get(z):
                diff.append((p, "q_tw." + z, qa.get(z), qb.get(z)))
    return {"passi_confrontati": len(com), "quantili_confrontati": nq,
            "materia": len(com) * len(CAMPI) + nq, "n_differenze": len(diff),
            "differenze": diff[:20], "passa": bool(com) and not diff,
            "blob_copia": blob(dst)[:8]}


def main(argv):
    passi = PASSI
    for a in argv[1:]:
        if a.startswith("--passi="):
            passi = int(a.split("=", 1)[1])
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    riga("=")
    stampa("IL SIGILLO DI kappa = 1 E DEL MESSAGGIO DI --chi-basc")
    riga("=")
    stampa("  simulatore di oggi: %s" % blob(SIM)[:8])
    stampa()
    riga("-")
    stampa("K0: i CODE OBJECT di tutto il modulo, ricorsivamente")
    riga("-")
    A = k0()
    for k in ("padre", "delta_righe", "blob_prima", "blob_oggi", "n_stringhe", "n_fuori"):
        stampa("   %-32s %s" % (k, A[k]))
    stampa()
    stampa("   LE STRINGHE CAMBIATE (dove, indice, prima -> dopo):")
    for d, k, x, y in A["stringhe_cambiate"]:
        stampa("      %s [%d]" % (d, k))
        stampa("         - %s" % x.replace(NL, " ")[:88])
        stampa("         + %s" % y.replace(NL, " ")[:88])
    if A["differenze_fuori_dalle_stringhe"]:
        stampa()
        stampa("   ### ⛔ DIFFERENZE FUORI DALLE STRINGHE:")
        for z in A["differenze_fuori_dalle_stringhe"]:
            stampa("      %s" % (z,))
    stampa("   ### %s" % ("✔ PASSA" if A["passa"] else "⛔ FALLISCE"))
    if not A["passa"]:
        _scrivi({"K0": A, "esito": 1})
        stampa()
        stampa("### ⛔ K0 FALLISCE: il codice compilato NON e' identico. MI FERMO.")
        return 1
    stampa()
    riga("-")
    stampa("K1: il blob NUOVO riproduce AL BIT i conteggi di amp0.json su %d passi" % passi)
    riga("-")
    B = k1(passi)
    for k in ("passi_confrontati", "quantili_confrontati", "materia", "n_differenze"):
        stampa("   %-32s %s" % (k, B[k]))
    if B["differenze"]:
        for z in B["differenze"][:10]:
            stampa("      %s" % (z,))
    stampa("   ### %s" % ("✔ PASSA" if B["passa"] else "⛔ FALLISCE"))
    stampa()
    riga("=")
    stampa("GLI ESITI")
    riga("=")
    stampa("  K0 (code object)   %s" % ("✔ PASSA" if A["passa"] else "⛔ FALLISCE"))
    stampa("  K1 (al bit)        %s" % ("✔ PASSA" if B["passa"] else "⛔ FALLISCE"))
    riga("=")
    _scrivi({"K0": A, "K1": B, "passi": passi, "blob_oggi": blob(SIM),
             "esito": 0 if (A["passa"] and B["passa"]) else 1})
    return 0 if (A["passa"] and B["passa"]) else 1


def _scrivi(d):
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    io.open(os.path.join(FUORI, "sigillo.json"), "w", encoding="utf-8").write(
        json.dumps(d, indent=1, default=str))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
