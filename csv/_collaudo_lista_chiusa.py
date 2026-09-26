r"""**IL COLLAUDO DEL PRESIDIO DI `_lista_chiusa.py`** — i DUE rami, `P1-sexies`.

> **Un collaudo che prova solo il ramo che passa non prova niente** (`A9`, `P1-sexies`: *«il caso che
> DEVE fallire e' il piu' importante»*).

**I DUE RAMI:**

```
RAMO CHE DEVE PASSARE    il generatore vero gira                -> uscita 0, il documento c'e'
RAMO CHE DEVE FALLIRE    una copia con una voce che NON ESISTE   -> uscita 3, il documento NON si
                         nell'elenco `DEVONO`                      scrive e il suo sha1 NON cambia
```

**La copia truccata sta in `csv/`**, e non altrove, perche' il generatore calcola la radice del
repo **dalla propria posizione**: da un'altra cartella non troverebbe ne' `_presidio` ne' le fonti,
e fallirebbe **per il motivo sbagliato** — che e' esattamente il modo in cui un collaudo passa senza
provare nulla *(misurato: al primo tentativo usciva `1` con `ModuleNotFoundError`, e il collaudo si
era dichiarato `FAIL` — giustamente, ma per un'altra ragione)*. La copia viene **rimossa** alla fine.

**NESSUN RUN, nessun simulatore.**
"""
# ESENTE-P5: non importa il simulatore e non lo fa girare. Collauda un generatore di documenti.
import hashlib
import io
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
SRC = os.path.join(_QUI, "_lista_chiusa.py")
TRUCCO = os.path.join(_QUI, "_lc_collaudo_tmp.py")
DOC = os.path.join(RADICE, "doc", "LISTA_CHIUSA.md")
DEST = os.path.join(RADICE, "doc", "COLLAUDO_lista_chiusa.txt")
NL = chr(10)
R = []


def P(s=""):
    R.append(s)
    print(s)


def sha(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()[:8]


def gira(path):
    return subprocess.run([sys.executable, path], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", cwd=RADICE)


P("=" * 100)
P("COLLAUDO DEL PRESIDIO DI `_lista_chiusa.py` -- I DUE RAMI   (2026-09-26)")
P("=" * 100)
P()

# ------------------------------------------------------------------ ramo che DEVE passare
_a = gira(SRC)
_c1 = os.path.exists(DOC)
_h1 = sha(DOC) if _c1 else "-"
P("RAMO CHE DEVE PASSARE -- il generatore vero")
P("  uscita %d   documento presente: %s   sha1 %s" % (_a.returncode, _c1, _h1))
_ok_a = (_a.returncode == 0 and _c1)
P("  esito: %s" % ("PASS" if _ok_a else "FAIL"))
P()

# ------------------------------------------------------------------ ramo che DEVE fallire
t = io.open(SRC, encoding="utf-8", newline="").read()
A = ' ("i 24 script che avanzano con step() da solo", r"'
assert t.count(A) == 1, "l'ancora dell'elenco DEVONO non e' unica: %d" % t.count(A)
_fine = t.index(NL + "]", t.index(A)) + 1
io.open(TRUCCO, "w", encoding="utf-8", newline=NL).write(
    # ⚠ TRE campi: da quando la vista legge l'indice, `DEVONO` porta anche il MOTIVO della
    #   copertura. Con DUE campi la copia truccata si schiantava in `ValueError` -- uscita `1`
    #   invece di `3` -- e il collaudo dava `FAIL` **per la ragione sbagliata**.
    t[:_fine]
    + ' ("COLLAUDO: una voce che NON esiste", r"QUESTA-VOCE-NON-ESISTE-DAVVERO", ""),' + NL
    + t[_fine:])
try:
    _prima = sha(DOC)
    _b = gira(TRUCCO)
    _dopo = sha(DOC)
finally:
    os.remove(TRUCCO)

P("RAMO CHE DEVE FALLIRE -- la copia con una voce che NON esiste")
P("  uscita %d   *(3 = si e' fermato per il collaudo)*" % _b.returncode)
for _r in (_b.stdout or "").strip().split(NL)[-3:]:
    P("     %s" % _r)
if _b.returncode not in (0, 3):
    P("     STDERR: %s" % (_b.stderr or "").strip().split(NL)[-1][:150])
P("  sha1 del documento   PRIMA %s   DOPO %s   -> %s"
  % (_prima, _dopo, "INVARIATO" if _prima == _dopo else "*** MODIFICATO: il presidio NON blocca"))
_ok_b = (_b.returncode == 3 and _prima == _dopo)
P("  esito: %s" % ("PASS" if _ok_b else "FAIL"))
P()
P("=" * 100)
P("ESITO: %s" % ("2/2 PASS -- il presidio IMPEDISCE, non avvisa" if (_ok_a and _ok_b)
               else "FAIL: il presidio non fa cio' che dichiara"))
P("=" * 100)
P()
P("COSA QUESTO COLLAUDO *NON* DICE:")
P("  - **non dice che la LISTA sia completa**: dice che le quindici voci dell'elenco `DEVONO`")
P("    compaiono nella parte IN LISTA, e che il generatore si FERMA se una manca.")
P("  - **l'elenco `DEVONO` l'ha dettato Luca**, non l'ho ricavato io dai registri: una voce che")
P("    manca e che nessuno ha nominato **questo collaudo non la vede**.")

io.open(DEST, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
sys.exit(0 if (_ok_a and _ok_b) else 1)
