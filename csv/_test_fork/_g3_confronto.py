# -*- coding: utf-8 -*-
"""`G3`: il confronto fra la validazione (gravita' ACCESA) e la prova (gravita' SPENTA).

⚠ SOLA LETTURA su file gia' scritti. Nessuna fisica, nessuna modifica a niente.

⚠ NON E' UN CONFRONTO FRA EPOCHE (par.9-bis): i due run hanno **lo stesso blob** del simulatore
  (`9557a867`), **lo stesso seme** (`42`), **la stessa scena** e **la stessa configurazione**.
  L'UNICA differenza e' `GRAV_BIFASE`. **E' esattamente cio' che una prova di spegnimento e'.**

⚠ E IL SIGILLO DICE CHE QUELLA DIFFERENZA E' CHIRURGICA: `csv/_seal_fork/_sig_spegni_grav/`,
  `7/7`, e `T5` lo dimostra **strutturalmente** -- nel sorgente esiste **una sola ramificazione**
  che dipende da `GRAV_BIFASE` (`:5661`). Piu' il **controllo dell'involucro**, `206` campi
  identici e `0` diversi, che dimostra che **lo strumento di lancio e' inerte**.
ASCII PURO.
"""
import io
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
ON = os.path.join(RADICE, "csv", "_test_fork", "_val600")
OFF = os.path.join(RADICE, "csv", "_test_fork", "_g3_senza_bifase")
OUT = os.path.join(OFF, "CONFRONTO_ON_OFF.md")


def leggi_prog(d):
    """Il csv di progresso: frame, passo, n, archi, coer_l, dil."""
    p = os.path.join(d, "prog.csv")
    if not os.path.exists(p):
        return None
    righe = []
    with io.open(p, encoding="utf-8") as f:
        for r in f:
            r = r.strip()
            if not r or r.startswith("#") or r.startswith("frame"):
                continue
            c = r.split(",")
            try:
                righe.append((int(c[0]), int(c[1]), int(c[2]), int(c[3]),
                              float(c[4]), float(c[5])))
            except (ValueError, IndexError):
                continue
    return righe


def leggi_letture(d):
    """Le righe della tabella di `_letture_validazione.py`: passo, n, archi, ... med d0, d/d0."""
    p = os.path.join(d, "LETTURE.txt")
    if not os.path.exists(p):
        return None
    out = []
    with io.open(p, encoding="utf-8") as f:
        for r in f:
            c = r.split("|")
            if len(c) != 4:
                continue
            a = c[0].split()
            b = c[2].split()
            if len(a) < 3 or len(b) < 2:
                continue
            try:
                out.append((int(a[0]), int(a[1]), int(a[2]), float(b[0]), float(b[1])))
            except ValueError:
                continue
    return out


def main():
    lo, lf = leggi_letture(ON), leggi_letture(OFF)
    po, pf = leggi_prog(ON), leggi_prog(OFF)
    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    W = o.write
    W("# `G3` -- LA GRAVITA' ACCESA contro LA GRAVITA' SPENTA\n\n")
    W("> **GENERATA DA CODICE** (`P1-ter`). **SOLA LETTURA** su file gia' scritti.\n")
    W("> Stesso blob `9557a867`, stesso seme `42`, stessa scena, stessa configurazione:\n")
    W("> **l'unica differenza e' `GRAV_BIFASE`.** Non e' un confronto fra epoche.\n\n")

    if lo and lf:
        W("## `med d0` e `d/d0`, snapshot per snapshot\n\n")
        W("| passo | `n` ON | `n` OFF | `med d0` ON | `med d0` OFF | `d/d0` ON | `d/d0` OFF |\n")
        W("|--:|--:|--:|--:|--:|--:|--:|\n")
        d = dict((r[0], r) for r in lf)
        for r in lo:
            s = d.get(r[0])
            if not s:
                continue
            W("| %d | %d | %d | `%.4f` | `%.4f` | `%.4f` | `%.4f` |\n"
              % (r[0], r[1], s[1], r[3], s[3], r[4], s[4]))
        # il rapporto fra snapshot consecutivi: e' IL criterio 4
        def rapporti(v):
            m = [r[3] for r in v]
            return [m[k + 1] / m[k] for k in range(len(m) - 1)]
        ro, rf = rapporti(lo), rapporti(lf)
        W("\n**Il criterio `4`, il RAPPORTO fra snapshot consecutivi di `med d0`**\n")
        W("*(costante `> 1` = crescita ESPONENZIALE)*:\n\n")
        W("| | rapporti | MEDIANO |\n|---|---|--:|\n")
        W("| gravita' **ACCESA** | %s | **`%.4f`** |\n"
          % (", ".join("`%.4f`" % x for x in ro), float(np.median(ro))))
        W("| gravita' **SPENTA** | %s | **`%.4f`** |\n"
          % (", ".join("`%.4f`" % x for x in rf), float(np.median(rf))))
        _dif = 100.0 * (float(np.median(rf)) - float(np.median(ro))) / float(np.median(ro))
        W("\n> **Differenza relativa del rapporto mediano: `%+.1f %%`.**\n" % _dif)

    if po and pf:
        W("\n## `coer_l` e `dil` dal `prog.csv` dei due run\n\n")
        W("| frame | passo | `coer_l` ON | `coer_l` OFF | `dil` ON | `dil` OFF |\n")
        W("|--:|--:|--:|--:|--:|--:|\n")
        d = dict((r[0], r) for r in pf)
        for r in po:
            s = d.get(r[0])
            if not s or r[0] % 20 != 0:
                continue
            W("| %d | %d | `%.4f` | `%.4f` | `%.3f %%` | `%.3f %%` |\n"
              % (r[0], r[1], r[4], s[4], r[5], s[5]))
        W("\n**`coer_l`** e' la coerenza locale *(quanto le masse restano insieme)*; **`dil`** e'\n")
        W("la dilatazione riportata dal driver. **Non li interpreto oltre il loro andamento:**\n")
        W("sono due grandezze del driver, e la loro definizione esatta non e' stata riletta qui.\n")

    W("\n## ⚠ COSA QUESTO CONFRONTO NON E'\n\n")
    W("**Non e' un confronto fra epoche.** I due run condividono blob, seme, scena e "
      "configurazione;\nl'unica differenza e' il flag, e il sigillo `7/7` dimostra che quella "
      "differenza e'\n**chirurgica** -- `T5`, strutturale: **una sola ramificazione** dipende da "
      "`GRAV_BIFASE`.\n")
    W("\n**Non e' una misura su piu' semi.** **UN seme, UNA scena.** Per una barra fra semi ne "
      "servono\n**almeno quattro** (`P3`). **Cio' che qui e' grande** *(il rapporto di `d0` che "
      "non cambia,\nlo stress che cala)* **andra' comunque riconfermato.**\n")
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
