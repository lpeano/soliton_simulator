# -*- coding: utf-8 -*-
"""IL CONFRONTO FRA I TRE BRACCI DELLA MEMORIA DEL MOTO. Nessun run, nessuna cura.

  ACCESO          tutto attivo                           `_g4_riferimento`
  SOLO-SCRITTURA  `MEM_MOTO = False`                     `_g4_senza_memmoto`
  INTERO-BLOCCO   `MEM_MOTO_TUTTO = False`               `_g4bis_senza_blocco`

⚠ `P1-ter`: la tabella si GENERA, non si ricopia. Le tre `LETTURE.txt` esistono gia', ma
  **parsarle sarebbe fragile**: qui si rileggono gli SNAPSHOT e si ricalcolano le stesse
  grandezze con la STESSA formula, cosi' il confronto non dipende da come e' stampato un file.

⚠ E I CRITERI `REGGE / NON REGGE` NON si ricalcolano qui: appartengono a
  `_letture_validazione.py`, che li tiene fissati. **Si LEGGE il conteggio dalle sue
  `LETTURE.txt`**, che e' un dato gia' prodotto da uno strumento sigillato. **Due strumenti,
  una sola definizione dei criteri.**

SOLA LETTURA. ASCII PURO.
"""
import gzip
import io
import os
import pickle
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
OUT = os.path.join(_QUI, "_diag_D", "TRE_BRACCI.md")
PASSI = (120, 240, 360, 480, 600)
BRACCI = [("ACCESO", "_g4_riferimento", "tutto attivo"),
          ("SOLO-SCRITTURA", "_g4_senza_memmoto", "`MEM_MOTO = False`"),
          ("INTERO-BLOCCO", "_g4bis_senza_blocco", "`MEM_MOTO_TUTTO = False`")]


def leggi(cart, passo):
    p = os.path.join(RADICE, "csv", "_test_fork", cart, "scena_%06d.pkl.gz" % passo)
    if not os.path.exists(p):
        return None
    with gzip.open(p, "rb") as f:
        return pickle.load(f)["attrs"]


def criteri(cart):
    """Il conteggio `REGGONO n criteri su 8`, LETTO dalle `LETTURE.txt` di chi li definisce."""
    p = os.path.join(RADICE, "csv", "_test_fork", cart, "LETTURE.txt")
    if not os.path.exists(p):
        return None, None
    t = io.open(p, encoding="utf-8").read()
    m = re.search(r"REGGONO (\d+) criteri su (\d+)", t)
    if not m:
        return None, None
    # ⚠ CORRETTO dopo un FALSO POSITIVO (reperto `004be56`). La prima versione era
    #   `^(.+?)\s+NON REGGE\s` e catturava L'INTESTAZIONE della sezione, che contiene la
    #   stringa "REGGE / NON REGGE". Ora si richiede contenuto sulla STESSA riga dopo
    #   "NON REGGE": le righe vere sono `<criterio>  NON REGGE  <spiegazione>`, mentre
    #   l'intestazione finisce a fine riga.
    nr = re.findall(r"^(.+?)\s+NON REGGE[ \t]+\S", t, re.M)
    return ("%s/%s" % (m.group(1), m.group(2))), [x.strip() for x in nr]


def grandezze(a):
    d = np.asarray(a["d"], float)
    d0 = np.asarray(a["d0"], float)
    return dict(n=int(len(np.asarray(a["_deg"]))), archi=int(len(d)),
                med_d=float(np.median(d)), med_d0=float(np.median(d0)),
                med_r=float(np.median(d / np.maximum(d0, 1e-12))))


def collaudo(W):
    """`P1-sexies`: il lettore dei criteri su file sintetici a risposta NOTA."""
    W("COLLAUDO (`P1-sexies`), PRIMA di confrontare\n" + "-" * 92 + "\n")
    import tempfile
    d = tempfile.mkdtemp()
    e = []
    os.makedirs(os.path.join(d, "buono"))
    # ⚠ IL FILE SINTETICO PORTA L'INTESTAZIONE VERA, ed e' il punto: il primo collaudo NON
    #   ce l'aveva, quindi non poteva prendere il falso positivo che poi e' successo.
    #   **Un caso a risposta nota piu' POVERO dell'input vero collauda un input che non
    #   esiste** (reperto `004be56`).
    io.open(os.path.join(d, "buono", "LETTURE.txt"), "w", encoding="utf-8").write(
        "=" * 96 + "\n"
        "ESITO CONTRO I CRITERI -- REGGE / NON REGGE\n"
        + "=" * 96 + "\n"
        "`d0` NON scappa             NON REGGE  bla\n"
        "stress finito               REGGE      bla\n"
        "\nREGGONO 7 criteri su 8.\n")
    _vecchio = globals()["RADICE"]
    globals()["RADICE"] = d
    try:
        os.makedirs(os.path.join(d, "csv", "_test_fork"))
    except OSError:
        pass
    os.rename(os.path.join(d, "buono"), os.path.join(d, "csv", "_test_fork", "buono"))
    c, nr = criteri("buono")
    ok1 = (c == "7/8") and (nr == ["`d0` NON scappa"])
    W("K1 legge `7/8` e IL NOME del criterio che non regge -> %s  (%s, %s)\n"
      % ("OK" if ok1 else "*** NO ***", c, nr))
    e.append(ok1)
    os.makedirs(os.path.join(d, "csv", "_test_fork", "vuoto"))
    c2, nr2 = criteri("vuoto")
    ok2 = (c2 is None)
    W("K2 IL CASO CHE DEVE FALLIRE: `LETTURE.txt` ASSENTE -> deve dare `None`, NON `0/8`\n")
    W("     *(un file che manca non e' \"zero criteri\": e' ASSENZA DI DATO, pattern 3)* -> %s\n"
      % ("OK" if ok2 else "*** un'assenza verrebbe letta come uno ZERO ***"))
    e.append(ok2)
    globals()["RADICE"] = _vecchio
    import shutil
    shutil.rmtree(d, ignore_errors=True)
    ok = all(e)
    W("-" * 92 + "\n  -> %s\n\n" % ("i criteri PASSANO" if ok else "*** NON PASSANO ***"))
    return ok


def main():
    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    W = o.write
    W("# I TRE BRACCI DELLA MEMORIA DEL MOTO — **il confronto**\n\n")
    W("> Generato da `csv/_test_fork/_tre_bracci.py`. **Nessun run:** rilegge i 15 snapshot gia'\n")
    W("> scritti. Seme `42`, 600 passi, stessa scena. Blob `ab685eac` per i primi due, "
      "`21e3a3dc` per il terzo *(che aggiunge SOLO il flag, sigillato byte-inerte `10/10`)*.\n\n")
    if not collaudo(W):
        o.close(); print(io.open(OUT, encoding="utf-8").read()); return 1

    W("## L'ESITO CONTRO I CRITERI ASSOLUTI\n\n")
    W("| braccio | cosa spegne | **criteri** | quali NON reggono |\n|---|---|--:|---|\n")
    cnt = {}
    for nome, cart, cosa in BRACCI:
        c, nr = criteri(cart)
        cnt[nome] = c
        W("| **%s** | %s | **%s** | %s |\n"
          % (nome, cosa, c or "— **assente**",
             ", ".join("`%s`" % x for x in nr) if nr else "—"))

    W("\n## LE GRANDEZZE, snapshot per snapshot\n\n")
    for campo, eti, fmt in (("med_d0", "`med d0`", "%.4f"), ("med_d", "`med d`", "%.4f"),
                            ("med_r", "**`med d/d0`**", "%.4f"), ("n", "`n`", "%d")):
        # ⚠ il separatore ha UNA colonna in piu' delle intestazioni: quella del `passo`.
        #   La prima versione aggiungeva un `|` di troppo in fondo (difetto cosmetico, 18:36).
        W("### %s\n\n| passo | %s |\n|--:|%s\n"
          % (eti, " | ".join("**%s**" % b[0] for b in BRACCI),
             "--:|" * len(BRACCI)))
        for passo in PASSI:
            riga = []
            for _n, cart, _c in BRACCI:
                a = leggi(cart, passo)
                riga.append((fmt % grandezze(a)[campo]) if a else "—")
            W("| %d | %s |\n" % (passo, " | ".join(riga)))
        W("\n")

    W("## IL RAPPORTO MEDIANO DI `med d0` FRA SNAPSHOT — **la fuga**\n\n")
    W("| braccio | rapporto mediano | `med d0` finale | lettura |\n|---|--:|--:|---|\n")
    for nome, cart, _c in BRACCI:
        v = []
        for passo in PASSI:
            a = leggi(cart, passo)
            v.append(grandezze(a)["med_d0"] if a else np.nan)
        v = np.asarray(v, float)
        rap = float(np.median(v[1:] / v[:-1])) if np.all(np.isfinite(v)) else float("nan")
        W("| **%s** | **%.4f** | %.4f | %s |\n"
          % (nome, rap, v[-1],
             "costante `> 1` = **ESPONENZIALE**" if rap > 1.0 else "non cresce"))
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
