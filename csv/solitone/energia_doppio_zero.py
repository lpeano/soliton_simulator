# -*- coding: utf-8 -*-
r"""**U3 DELL'UNIFICAZIONE: L'ENERGIA COL DOPPIO ZERO** *(Luca `2026-11-12` `10:39`; il task history `doc/TASK_HISTORY/2026-11-12_unificazione.md`, sez. `1.5` e `2`)*. [[PIANO-2D-3D]] [[H-NUCLEO-CONGELATO]]

    python csv/solitone/energia_doppio_zero.py --misura --radice <albero> --uscita <file.json> [--doppio]
    python csv/solitone/energia_doppio_zero.py --confronta <vecchio.json> <nuovo.json> <doppio.json> > doc/referti_l2/unificazione_doppio_zero.txt

**La misura:** `csv/solitone/mb_costante.misura` *(lo stato di TBS a `100000`, i conti per termine a `t0` e dopo `N` tick del ciclo della corsa)* **sull'albero `--radice`**
*(i suoi `csv/` e `primo_ordine/` per primi in `sys.path`, come `zero_nel_nucleo.py`: il nucleo VECCHIO col suo avvolgimento, o il NUOVO)*; **`--doppio`: tutta la misura dentro
`zero_nel_nucleo.doppio_avvolgimento`** *(l'avvolgimento di prima rimesso SOPRA il nucleo nuovo: lo zero DUE volte)*. **`mb_costante.py` e `zero_nel_nucleo.py` si caricano da QUESTO
albero** *(nel vecchio non ci sono)*, **la libreria e il nucleo da `--radice`.**
**Il confronto** *(a `t0`, `E0 = tot + E_ass`)*: **DEVE** il nuovo meno il vecchio `= pi (M + V)` **entro `1e-14` relativo** *(la tolleranza delle costanti convertite, Luca)*;
**DEVE** *(Luca)* il doppio meno il vecchio `= 2 pi (M + V)` entro la stessa; **DEVE FALLIRE:** il doppio meno il vecchio `= pi (M + V)`.
"""
import importlib.util
import json
import math
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
N_TICK = 20                    # ### mio (dichiarato): pochi tick, la misura e' a t0
TOLL = 1e-14                   # ### Luca (U0 confermato): le costanti convertite entro 1e-14 relativo
OK = [0, 0]
FALLITE = []


def prendi(argv, nome):
    return argv[argv.index(nome) + 1] if nome in argv else None


def carica(nome):
    spec = importlib.util.spec_from_file_location("_u3_" + nome, os.path.join(_QUI, nome + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def misura(radice, uscita, doppio):
    for p in (os.path.join(radice, "primo_ordine", "leggi"), os.path.join(radice, "primo_ordine"), os.path.join(radice, "csv")):
        sys.path.insert(0, p)
    import contextlib
    import flussi_parziali as FP
    assert os.path.normcase(os.path.dirname(os.path.abspath(FP.__file__))) == os.path.normcase(os.path.join(os.path.abspath(radice), "primo_ordine")), ("il nucleo NON e' quello dell'albero", FP.__file__)
    import solitone  # noqa: F401  (### dall'albero --radice, PRIMA di mb_costante: cosi' il suo «import solitone» trova questo in cache)
    MB = carica("mb_costante")
    ZN = carica("zero_nel_nucleo")
    # ### mb_costante, all'import, mette in testa la cartella csv/ di QUESTO albero: si rimettono in testa quelle di --radice (la libreria deve venire da li')
    radici = [os.path.normcase(os.path.abspath(os.path.join(radice, *q))) for q in (("primo_ordine", "leggi"), ("primo_ordine",), ("csv",))]
    questo = os.path.normcase(os.path.dirname(_QUI))
    sys.path[:] = [p for p in sys.path if os.path.normcase(os.path.abspath(p)) not in radici + [questo]]
    for p in reversed(radici):
        sys.path.insert(0, p)
    import _vuoto_vivo_B as V
    import solitone
    for mod in (V, solitone):
        assert os.path.normcase(os.path.abspath(mod.__file__)).startswith(os.path.normcase(os.path.abspath(radice))), ("la libreria NON e' quella dell'albero", mod.__file__)
    extra = ZN.doppio_avvolgimento() if doppio else contextlib.nullcontext()
    tmp = uscita + ".mb.json"
    with extra:
        MB.misura(tmp, N_TICK)
    d = json.load(open(tmp, encoding="utf-8"))
    os.remove(tmp)
    d.update({"radice": radice, "doppio": doppio, "flussi_parziali": FP.__file__})
    with open(uscita, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=1, sort_keys=True)
    print("scritto %s: E0 %r, M0 %r, V0 %r, e_K %r" % (uscita, d["E0"], d["M0"], d["V0"], d["e_K"]))
    return 0


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-104s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:104], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def confronta(fv, fn, fd):
    sys.path.insert(0, os.path.dirname(_QUI))
    import _presidio
    _presidio.avvia(__file__)
    v, n, d = (json.load(open(f, encoding="utf-8")) for f in (fv, fn, fd))
    print("=" * 130)
    print("U3, L'ENERGIA COL DOPPIO ZERO: il vecchio %s (%s), il nuovo %s (%s), il doppio %s (%s); lo stato di TBS a 100000, a t0; la tolleranza %g relativa"
          % (fv, v["radice"], fn, n["radice"], fd, d["radice"], TOLL))
    print("=" * 130)
    assert not v["doppio"] and not n["doppio"] and d["doppio"]
    M, V = n["M0"], n["V0"]
    piMV = math.pi * (M + V)
    print("  M0: vecchio %r nuovo %r doppio %r; V0: %r %r %r" % (v["M0"], n["M0"], d["M0"], v["V0"], n["V0"], d["V0"]))
    print("  E0: vecchio %+.17e, nuovo %+.17e, doppio %+.17e; pi (M + V) %+.17e" % (v["E0"], n["E0"], d["E0"], piMV))
    dn, dd = n["E0"] - v["E0"], d["E0"] - v["E0"]
    print("  (nuovo - vecchio) / (pi (M + V)) = %.15f; (doppio - vecchio) / (pi (M + V)) = %.15f" % (dn / piMV, dd / piMV))
    print("  e_K: vecchio %r nuovo %r doppio %r; nuovo - vecchio - pi %.3e" % (v["e_K"], n["e_K"], d["e_K"], n["e_K"] - v["e_K"] - math.pi))
    esito("il nuovo meno il vecchio = pi (M + V), entro %g di E0" % TOLL, abs(dn - piMV) <= TOLL * abs(n["E0"]), "scarto %.3e (soglia %.3e)" % (dn - piMV, TOLL * abs(n["E0"])))
    esito("(Luca) col doppio zero: il doppio meno il vecchio = 2 pi (M + V), entro %g di E0" % TOLL, abs(dd - 2 * piMV) <= TOLL * abs(d["E0"]), "scarto %.3e" % (dd - 2 * piMV))
    esito("col doppio zero: il doppio meno il vecchio = pi (M + V) (lo spostamento semplice)", abs(dd - piMV) <= TOLL * abs(d["E0"]), "scarto %.3e" % (dd - piMV), deve=False)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--misura":
        sys.exit(misura(prendi(a, "--radice"), prendi(a, "--uscita"), "--doppio" in a))
    if a and a[0] == "--confronta":
        sys.exit(confronta(a[1], a[2], a[3]))
    sys.exit("uso: --misura --radice <albero> --uscita <file> [--doppio] | --confronta <vecchio> <nuovo> <doppio>")
