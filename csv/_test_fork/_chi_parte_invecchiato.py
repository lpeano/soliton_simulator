# -*- coding: utf-8 -*-
"""`PASSO-2` — **quali run partivano da un vuoto INVECCHIATO col passo incompleto?**

> **Mandato di Luca, 2026-09-25:** *«prima di curarlo, dalla tabella delle campagne
> (`_RICOSTRUZIONE_config`) e dai `CONFIGURAZIONE.txt`: quali run passavano `--seed` o
> `--nodi != default`, quindi partivano da un vuoto invecchiato col passo incompleto?
> Verifica che con `--nodi 0` (scena `(ii)`) il ciclo giri su ZERO nodi (misurato, non dedotto).»*

**IL SITO, letto dal codice** *(`soliton_simulator.py`, la guardia della ricostruzione)*:

```python
net = Rete(a.seed if a.seed is not None else 42)
net.semina(a.nodi)
if a.seed is not None or a.nodi != SEME_INIZIALE:
    for _ in range(300): net.step()          # <- TRECENTO PASSI INCOMPLETI
    net.rilassa_disegno(30)
```

**LA CONDIZIONE E' UN `or`:** basta **`--seed`** *(qualunque valore)* **oppure** `--nodi` diverso
da `SEME_INIZIALE`. **Quindi un run con `--seed 42` la fa scattare ugualmente**, anche se `42` è il
default del costruttore: `a.seed is not None` è vero.

**SI CERCA NEI FILE, non a memoria:** `csv/_test_fork/_RICOSTRUZIONE_config.txt` e ogni
`CONFIGURAZIONE*` sotto `csv/`. **La tabella è generata.**

**E IL CASO `--nodi 0` SI MISURA, non si deduce:** si costruisce la rete come fa il codice e si
guarda **`net.n` prima del ciclo** e **quante volte il ciclo gira**.
"""
import io
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
DEST = os.path.join(_QUI, "_chi_parte_invecchiato", "CHI_PARTE_INVECCHIATO.txt")
os.makedirs(os.path.dirname(DEST), exist_ok=True)

R = []


def P(s=""):
    R.append(s)
    print(s)


import importlib.util as iu

_sp = iu.spec_from_file_location("sim_pi", os.path.join(RADICE, "soliton_simulator.py"))
S = iu.module_from_spec(_sp)
_sp.loader.exec_module(S)

P("=" * 112)
P("`PASSO-2` -- CHI PARTIVA DA UN VUOTO INVECCHIATO CON 300 PASSI INCOMPLETI")
P("=" * 112)
P()
P("LA CONDIZIONE, letta dal codice:  `if a.seed is not None or a.nodi != SEME_INIZIALE:`")
P("  SEME_INIZIALE = %s   (il default di `--nodi`)" % getattr(S, "SEME_INIZIALE", "?"))
P("  ⚠ E' un `or`: BASTA `--seed`, con QUALUNQUE valore. Un run con `--seed 42` la fa scattare")
P("    ugualmente, anche se 42 e' il default del costruttore, perche' `a.seed is not None`.")
P()

# ------------------------------------------------------- i file di configurazione
FILES = []
tab = os.path.join(RADICE, "csv", "_test_fork", "_RICOSTRUZIONE_config.txt")
if os.path.isfile(tab):
    FILES.append(tab)
for r, _d, fs in os.walk(os.path.join(RADICE, "csv")):
    for f in fs:
        if f.startswith("CONFIGURAZIONE"):
            FILES.append(os.path.join(r, f))

RE_SEED = re.compile(r"--seed[= ]+(-?\d+)")
RE_NODI = re.compile(r"--nodi[= ]+(-?\d+)")

P("-" * 112)
P("I FILE CERCATI: %d  (la tabella delle campagne + ogni `CONFIGURAZIONE*` sotto `csv/`)" % len(FILES))
P("-" * 112)
P()
righe = []
for p in FILES:
    try:
        src = io.open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    rel = os.path.relpath(p, RADICE).replace(chr(92), "/")
    for k, linea in enumerate(src.split(chr(10)), start=1):
        s_ = RE_SEED.search(linea)
        n_ = RE_NODI.search(linea)
        if not s_ and not n_:
            continue
        nodi = int(n_.group(1)) if n_ else None
        seed = int(s_.group(1)) if s_ else None
        scatta = (seed is not None) or (nodi is not None
                                        and nodi != getattr(S, "SEME_INIZIALE", None))
        righe.append((rel, k, seed, nodi, scatta, linea.strip()[:120]))

if not righe:
    P("  NESSUNA riga con `--seed` o `--nodi` trovata nei file cercati.")
else:
    P("  %-46s %-6s %-8s %-8s %-8s" % ("file", "riga", "--seed", "--nodi", "INVECCHIA?"))
    for rel, k, seed, nodi, scatta, linea in righe:
        P("  %-46s %-6d %-8s %-8s %-8s"
          % (rel[-46:], k, seed if seed is not None else "-",
             nodi if nodi is not None else "-", "SI'" if scatta else "no"))
    P()
    P("  le righe per esteso:")
    for rel, k, seed, nodi, scatta, linea in righe:
        P("    [%s:%d] %s" % (rel[-40:], k, linea))
P()
n_si = sum(1 for x in righe if x[4])
P("  RIGHE CHE FAREBBERO SCATTARE L'INVECCHIAMENTO: %d su %d" % (n_si, len(righe)))
P()

# ------------------------------------------------------- `--nodi 0`: MISURATO
P("-" * 112)
P("`--nodi 0` (la scena `(ii)`): IL CICLO GIRA SU ZERO NODI? -- MISURATO, non dedotto")
P("-" * 112)
P()
for nodi, seed in ((0, None), (0, 11), (getattr(S, "SEME_INIZIALE", 80), None)):
    net = S.Rete(seed if seed is not None else 42)
    net.semina(nodi)
    n_prima = int(net.n)
    archi_prima = int(len(net.d))
    scatta = (seed is not None) or (nodi != getattr(S, "SEME_INIZIALE", None))
    giri = 0
    n_dopo, archi_dopo = n_prima, archi_prima
    if scatta:
        for _ in range(300):
            net.step()
            giri += 1
        net.rilassa_disegno(30)
        n_dopo, archi_dopo = int(net.n), int(len(net.d))
    P("  --nodi %-5s --seed %-5s  ->  invecchia: %-4s  n prima %-6d archi prima %-8d"
      % (nodi, seed if seed is not None else "(assente)", "SI'" if scatta else "no",
         n_prima, archi_prima))
    P("      giri del ciclo = %-5d   n dopo %-6d archi dopo %-8d" % (giri, n_dopo, archi_dopo))
    if scatta and n_prima == 0:
        P("      -> IL CICLO GIRA %d VOLTE SU ZERO NODI. Nessun effetto possibile: `step()` su una" % giri)
        P("         rete vuota non ha nulla da muovere. **MISURATO, non dedotto.**")
    elif scatta:
        P("      -> il ciclo gira su %d nodi: QUI l'invecchiamento INCOMPLETO agisce." % n_prima)
    P()

P("=" * 112)
P("LA CONCLUSIONE")
P("=" * 112)
P("  * con `--nodi 0` (la scena `(ii)`) il ciclo gira su ZERO NODI: `PASSO-2` **non tocca la")
P("    scena `(ii)`**, ed e' MISURATO qui sopra.")
P("  * `PASSO-2` tocca **solo** i run che seminano un vuoto E passano `--seed` o un `--nodi`")
P("    diverso dal default. La tabella qui sopra dice quali sono, e viene dai FILE.")
P("  * ⚠ E la condizione e' un `or` su `a.seed is not None`: **un run con `--seed` uguale al")
P("    default lo fa scattare ugualmente**. Chi legge «ho passato il seme di default, quindi non")
P("    cambia niente» sbaglia.")
P()
P("COSA QUESTO NON DICE:")
P("  - la ricerca e' sui file di configurazione TROVATI: un run lanciato a mano e non")
P("    registrato in nessun `CONFIGURAZIONE*` non compare. **Non e' un inventario dei run:")
P("    e' un inventario dei run DOCUMENTATI.**")
P("  - non dice se quell'invecchiamento abbia CAMBIATO una conclusione: dice quali run lo")
P("    hanno subito.")

io.open(DEST, "w", encoding="utf-8", newline="\n").write(chr(10).join(R) + chr(10))
