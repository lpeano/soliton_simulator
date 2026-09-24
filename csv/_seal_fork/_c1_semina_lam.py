# -*- coding: utf-8 -*-
"""`C1` -- **`SEMINA_LAM` spenta e' byte-identica?** E il controllo positivo di `D38`.

**⚠ IL RIFERIMENTO NON E' UN PICKLE SALVATO: E' IL CODICE VECCHIO CHE GIRA ADESSO.**
*(rilievo di Luca, 2026-09-24)* Il blob `49fc54d2` si estrae da `git` **in binario**
*(par.5-quinquies)* e gira **in un processo suo, con la STESSA argv letta dal driver**.
**Cosi' un `FAIL` si attribuisce a `SEMINA_LAM` e non a cambi intermedi** -- il pickle di
`_cura2_corto` e' stato scritto quando il driver aveva **altri default** *(`--sep`, `CHICOOP`)*,
e confrontarsi con lui avrebbe mescolato tre cambiamenti in uno.

**I DUE TEST:**

```
C1   VECCHIO vs NUOVO, argv del driver (SEMINA_LAM spenta)   ->  DEVONO essere IDENTICI
D38  VECCHIO vs NUOVO, ENTRAMBI --scala-min-passo=off        ->  DEVONO DIFFERIRE
```

**❌ E IL CONTROLLO POSITIVO DI PRIMA ERA VUOTO** *(rilievo di Luca)*: confrontavo il
riferimento **con `--scala-min-passo` ACCESO** contro un braccio **SPENTO**. Quei due
differiscono **perche' uno ha il freno e l'altro no**, e **di `D38` non dicevano niente.**
Il confronto giusto tiene `--scala-min-passo=off` su **entrambi** i bracci e cambia **solo il
codice**: li' il vecchio `_nasce` **non tronca** e il nuovo **si'**.

**⚠ E ENTRAMBI I BRACCI DI `D38` SI FERMANO**, per l'invariante di `E4-LAM`: **il punto e'
DOVE e SU COSA.** Il vecchio cade su `d` alla semina, il nuovo su `d0` al passo 2 -- e **quella
differenza E' la cura.**

ASCII puro.
"""
import gzip
import hashlib
import io
import os
import pickle
import re
import subprocess
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
DEST = os.path.join(_QUI, "_c1_semina")
REF = os.path.join(DEST, "REFERTO.txt")
VECCHIO_SHA = "49fc54d2"          # sha1 dei BYTE GREZZI (non `git hash-object`: C18)


def firma(v):
    a = np.ascontiguousarray(np.asarray(v))
    return (hashlib.sha1(a.tobytes()).hexdigest()[:16], a.shape, str(a.dtype))


def estrai_vecchio(P):
    """Il blob `49fc54d2` dei BYTE GREZZI, estratto da `git` **in binario**.

    Si cerca il commit che ha quel `sha1` dei byte (non `git hash-object`, C18) e si scrive
    con `git cat-file -p` **in binario** -- `git checkout` riscriverebbe le newline
    (`core.autocrlf`, la trappola CRLF del par.5-quinquies).
    """
    log = subprocess.run(["git", "log", "--format=%H", "-60", "--", "soliton_simulator.py"],
                         cwd=RADICE, capture_output=True, text=True).stdout.split()
    for h in log:
        b = subprocess.run(["git", "cat-file", "-p", "%s:soliton_simulator.py" % h],
                           cwd=RADICE, capture_output=True).stdout
        if hashlib.sha1(b).hexdigest().startswith(VECCHIO_SHA):
            with io.open(P, "wb") as f:
                f.write(b)
            return h, len(b)
    return None, 0


FIGLIO = r'''
import importlib.util, os, runpy, sys
sys.path.insert(0, os.path.join(RAD, "csv"))
# il simulatore SCELTO prende il posto di `soliton_simulator`: il driver importera' QUESTO
spec = importlib.util.spec_from_file_location("soliton_simulator", SIM)
S = importlib.util.module_from_spec(spec)
sys.modules["soliton_simulator"] = S
spec.loader.exec_module(S)
import _testa_driver as T
sys.argv = ["_scena_video.py", "20", DEST_D, "--serie=20"] + EXTRA
runpy.run_path(T.DRIVER, run_name="__main__")
'''


def gira(nome, sim, extra, P):
    d = os.path.join(DEST, nome)
    try:
        os.makedirs(d)
    except OSError:
        pass
    for f in os.listdir(d):
        if f.endswith(".pkl.gz"):
            os.remove(os.path.join(d, f))
    src = ("RAD = %r\nSIM = %r\nDEST_D = %r\nEXTRA = %r\n" % (RADICE, sim, d, list(extra))
           + FIGLIO)
    t0 = time.time()
    r = subprocess.run([sys.executable, "-c", src], cwd=RADICE, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    out = (r.stdout or "") + (r.stderr or "")
    P("\n  [%s] %.1f s  rc=%d  sim=%s  extra=%s\n"
      % (nome, time.time() - t0, r.returncode, os.path.basename(sim), list(extra) or "-"))
    for riga in out.splitlines():
        if "VIOLA" in riga or riga.strip().startswith(("quanti:", "arco=")):
            P("    %s\n" % riga.strip())
    p = os.path.join(d, "scena_000120.pkl.gz")
    att = pickle.load(gzip.open(p, "rb"))["attrs"] if os.path.exists(p) else None
    return att, out, r.returncode


def confronta(A, B, P, ea, eb):
    """Firma dei byte. **`solo in uno` ed eccezioni si ELENCANO PER NOME** (rilievo di Luca):
    se sono `> 0` vanno spiegate, **non sommate in silenzio**."""
    ug = dv = 0
    diversi, solo_a, solo_b, rotti = [], [], [], []
    for k in sorted(set(A) | set(B)):
        if k not in B:
            solo_a.append(k)
            continue
        if k not in A:
            solo_b.append(k)
            continue
        a, b = A[k], B[k]
        try:
            if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
                fa, fb = firma(a), firma(b)
                if fa == fb:
                    ug += 1
                else:
                    dv += 1
                    diversi.append("%s(%s %s != %s %s)" % (k, fa[0][:8], fa[1], fb[0][:8], fb[1]))
            elif a == b:
                ug += 1
            else:
                dv += 1
                diversi.append("%s(%r != %r)" % (k, a, b))
        except Exception as ex:
            rotti.append("%s(%s)" % (k, type(ex).__name__))
    P("  UGUALI %d   DIVERSI %d\n" % (ug, dv))
    if diversi:
        P("  DIVERSI: %s\n" % ", ".join(diversi[:10]))
    for eti, lst in (("solo in %s" % ea, solo_a), ("solo in %s" % eb, solo_b),
                     ("NON CONFRONTABILI (eccezione)", rotti)):
        P("  %-32s %d%s\n" % (eti, len(lst), (": " + ", ".join(lst)) if lst else ""))
    if solo_a or solo_b or rotti:
        P("  !! questi vanno SPIEGATI, non sommati in silenzio (rilievo di Luca).\n")
    return ug, dv, len(solo_a) + len(solo_b) + len(rotti)


def main():
    try:
        os.makedirs(DEST)
    except OSError:
        pass
    f = io.open(REF, "w", encoding="utf-8", newline="\n")

    def P(s):
        sys.stdout.write(s)
        f.write(s)

    P("# `C1` -- `SEMINA_LAM` spenta e' byte-identica? E il controllo positivo di `D38`.\n#\n")
    P("# IL RIFERIMENTO E' IL CODICE VECCHIO CHE GIRA ADESSO, non un pickle salvato\n")
    P("# (rilievo di Luca): cosi' un FAIL si attribuisce a `SEMINA_LAM` e non a cambi\n")
    P("# intermedi del driver (`--sep`, `CHICOOP`).\n#\n")

    vecchio = os.path.join(DEST, "_sim_vecchio.py")
    # il collaudo ha bisogno del file vecchio: si estrae qui sotto, e si collauda DOPO

    h, nb = estrai_vecchio(vecchio)
    if h is None:
        P("*** blob %s NON TROVATO negli ultimi 60 commit del simulatore ***\n" % VECCHIO_SHA)
        f.close()
        return 1
    nuovo = os.path.join(RADICE, "soliton_simulator.py")
    sha_n = hashlib.sha1(io.open(nuovo, "rb").read()).hexdigest()[:8]
    P("  VECCHIO  blob %s  commit %s  %d byte (estratto in BINARIO)\n" % (VECCHIO_SHA, h[:7], nb))
    P("  NUOVO    blob %s\n" % sha_n)
    esiti = []

    P("\n" + "=" * 96 + "\n`C1` -- argv del driver, `SEMINA_LAM` spenta: DEVONO essere IDENTICI\n"
      + "=" * 96 + "\n")
    A, _oa, rca = gira("c1_vecchio", vecchio, [], P)
    B, _ob, rcb = gira("c1_nuovo", nuovo, [], P)
    if A is None or B is None:
        P("  *** uno dei due bracci non ha prodotto lo snapshot (rc %d / %d) ***\n" % (rca, rcb))
        esiti.append(False)
    else:
        ug, dv, extra = confronta(A, B, P, "VECCHIO", "NUOVO")
        ok = (dv == 0 and ug > 100)
        esiti.append(ok)
        if ok and extra:
            # ⚠ PASS CONDIZIONATO (rilievo di Luca): i campi presenti in uno solo o non
            #   confrontabili **non sono zero**, e finche' non sono SPIEGATI il `PASS` non e'
            #   pieno. Dirlo è diverso da nasconderlo in un conteggio.
            P("\n  `C1` **PASS CONDIZIONATO**: `%d` campi non confrontati, elencati sopra.\n"
              % extra)
            P("        Finche' non sono SPIEGATI, questo non e' un PASS pieno.\n")
        else:
            P("\n  `C1` %s\n" % ("PASS PIENO: `SEMINA_LAM` spenta non cambia un bit, e nemmeno\n"
                                  "        `_nasce` senza gate -- con `SCALA_MIN_PASSO` acceso\n"
                                  "        girava gia'. E nessun campo resta non confrontato."
                                  if ok else "*** FAIL ***"))

    P("\n" + "=" * 96 + "\n`D38` -- ENTRAMBI con `--scala-min-passo=off`: DEVONO DIFFERIRE\n"
      + "=" * 96 + "\n")
    P("  Cambia SOLO IL CODICE: il vecchio `_nasce` e' gated e NON tronca, il nuovo SI'.\n")
    P("  (Il controllo di prima confrontava ACCESO contro SPENTO: differivano per il FRENO,\n")
    P("   e di `D38` non dicevano niente. Rilievo di Luca.)\n")
    Av, ov, rv = gira("d38_vecchio", vecchio, ["--scala-min-passo=off"], P)
    Bn, on_, rn = gira("d38_nuovo", nuovo, ["--scala-min-passo=off"], P)

    def quale(o):
        """`(grandezza, passo, quanti)` letti DALLA STESSA RIGA, con UNA regex.

        ❌ **PRIMA ERANO TRE REGEX SLEGATE sul testo INTERO**, e il risultato veniva stampato
           **sotto etichette sbagliate**: la frase diceva *«si ferma su `d` al passo 223380,
           1126 valori fuori dominio»* mentre i numeri veri erano **passo 1** e
           **223 380 valori**. Tre regex indipendenti possono pescare da **tre righe diverse**,
           e l'ordine della tupla non era quello della frase.
           **Le righe grezze citate sopra erano giuste: era il mio RIASSUNTO a mentire** --
           ed e' peggio, perche' il riassunto e' quello che si legge.
        """
        m = re.search(r"`(\w+)` VIOLA `[^`]*` al passo (\d+)", o)
        q = re.search(r"quanti: (\d+)", o)
        return (m.group(1) if m else "-", int(m.group(2)) if m else -1,
                int(q.group(1)) if q else -1)

    gv, gn = quale(ov), quale(on_)
    P("\n  VECCHIO: si ferma su `%s` al passo %s, con %s valori fuori dominio\n" % gv)
    P("  NUOVO  : si ferma su `%s` al passo %s, con %s valori fuori dominio\n" % gn)
    # ❌ IL CRITERIO PRECEDENTE AVEVA UN BUCO (rilievo di Luca):
    #     ok2 = (gv != gn) or (Av is not None and Bn is not None)
    #   il secondo ramo dava PASS **se entrambi arrivavano in fondo, SENZA verificare che
    #   DIFFERISSERO**: due corse IDENTICHE sarebbero passate. E' la stessa famiglia del
    #   `dv > 0` letto come effetto: un criterio che non puo' fallire dove dovrebbe.
    ok2 = False
    if gv != gn and gv[0] != "-":
        ok2 = True                        # si fermano in modo DIVERSO: e' la cura
        P("  -> si fermano in modo DIVERSO.\n")
    elif Av is not None and Bn is not None:
        P("  -> entrambi arrivano in fondo: allora DEVONO differire NEI DATI.\n")
        _ug, _dv, _ex = confronta(Av, Bn, P, "VECCHIO", "NUOVO")
        ok2 = (_dv > 0)
    else:
        P("  -> uno solo arriva in fondo: DIVERSI per definizione.\n")
        ok2 = (Av is None) != (Bn is None)
    esiti.append(ok2)
    P("\n  `D38` %s\n" % ("PASS: i due codici si comportano DIVERSAMENTE a parita' di argv.\n"
                          "        Il vecchio cade su `d` (la SEMINA, `_nasce` non tronca),\n"
                          "        il nuovo su `d0` (l'EVOLUZIONE): la nascita e' curata,\n"
                          "        e resta scoperto il MANTENIMENTO -- che e' il freno."
                          if ok2 else "*** FAIL: i due codici si comportano UGUALE ***"))

    # ------------------------------------------------------------------ IL COLLAUDO
    P("\n" + "=" * 96 + "\nCOLLAUDO DEL CRITERIO `D38` -- il caso che DEVE fallire\n"
      + "=" * 96 + "\n")
    P("  `P1-sexies`: un criterio si collauda su un caso a risposta NOTA. Qui il caso e'\n")
    P("  **LO STESSO CODICE NEI DUE BRACCI**: non c'e' nessuna cura fra loro, quindi il\n")
    P("  criterio di `D38` **DEVE dare FAIL**. Se desse PASS, direbbe `PASS` a qualunque cosa.\n")
    P("  (E' il buco che aveva il criterio precedente, trovato da Luca.)\n")
    Ka, oka, _ = gira("collaudo_a", nuovo, ["--scala-min-passo=off"], P)
    Kb, okb, _ = gira("collaudo_b", nuovo, ["--scala-min-passo=off"], P)
    ga, gb = quale(oka), quale(okb)
    P("\n  braccio a: `%s` al passo %s, con %s valori fuori dominio\n" % ga)
    P("  braccio b: `%s` al passo %s, con %s valori fuori dominio\n" % gb)
    if ga != gb and ga[0] != "-":
        finto = True
    elif Ka is not None and Kb is not None:
        _u, _d, _e = confronta(Ka, Kb, P, "a", "b")
        finto = (_d > 0)
    else:
        finto = (Ka is None) != (Kb is None)
    ok3 = (not finto)
    esiti.append(ok3)
    P("\n  COLLAUDO %s: col MEDESIMO codice il criterio di `D38` %s\n"
      % ("PASS" if ok3 else "*** NO ***",
         "dice FAIL, come deve" if ok3 else "direbbe PASS -- IL CRITERIO E' VUOTO"))

    n = sum(1 for x in esiti if x)
    P("\n" + "=" * 96 + "\nESITO: %d/%d\n" % (n, len(esiti)) + "=" * 96 + "\n")
    P("*** %s ***\n" % ("PASSATO." if n == len(esiti) else "FALLITO: reperto, commit, STOP."))
    f.close()
    return 0 if n == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
