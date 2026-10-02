# -*- coding: utf-8 -*-
"""**GENERA LA TABELLA DELLE REGOLE DI NASCITA** dal codice, non a mano.

### LA FONTE E' `REGOLE_NASCITA` nel simulatore, e questo script la RENDE LEGGIBILE.
Non il contrario: una tabella scritta a mano accanto a un codice che decide e' una
### **copia che scade** -- ed e' `L-NUMERI`, *ogni numero scritto in un referto esce
da uno script*.

**Produce due file:**

| | |
|---|---|
| `doc/REGOLE_NASCITA_generata.tsv` | una riga per `(evento, grandezza)`, **nell'ordine in cui la nascita scrive** |
| `doc/TABELLA_nascita.md` | la stessa cosa leggibile, con le **derivazioni** |

### E NON TOCCA `doc/REGOLE_nascita.tsv`, che e' il documento **a mano** del par.(c):
quello era ### **il punto di partenza** *(32 righe, verificate per ancora)*, questo e'
### **l'arrivo** -- e tenerli separati dice quale dei due il codice garantisce.

**COMANDO:** `python csv/_tabella_nascita.py`
"""
import hashlib
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio   # noqa: E402

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
sys.path.insert(0, RADICE)
NL = chr(10)
TAB = chr(9)


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def principale():
    import soliton_simulator as S
    sim = os.path.join(RADICE, "soliton_simulator.py")
    b = blob(sim)
    ordine = S.ORDINE_DI_NASCITA
    eventi = S.EVENTI_CONVERTITI
    righe_tsv = [TAB.join(("evento", "posizione", "grandezza", "classe", "regola",
                           "ancora", "derivazione"))]
    conta = {}
    for ev in eventi:
        for k, nome in enumerate(ordine):
            v = S.REGOLE_NASCITA[(ev, nome)]
            cl = v["classe"] if v["regola"] is None else "regola"
            conta[(ev, cl)] = conta.get((ev, cl), 0) + 1
            campi = (ev, str(k), nome, cl, v["classe"],
                     v["ancora"], v["derivazione"])
            pulito = [str(x).replace(TAB, " ").replace(NL, " ") for x in campi]
            righe_tsv.append(TAB.join(pulito))
    p_tsv = os.path.join(RADICE, "doc", "REGOLE_NASCITA_generata.tsv")
    io.open(p_tsv, "w", encoding="utf-8", newline=NL).write(NL.join(righe_tsv) + NL)

    M = []

    def w(s=""):
        M.append(s)

    w("# **LE REGOLE DI NASCITA** — *generato da `csv/_tabella_nascita.py`, NON a mano*")
    w()
    w("> ### **La FONTE e' `REGOLE_NASCITA` in `soliton_simulator.py`** *(blob `%s`, sha1 "
      "byte grezzi)*. ### **Questo file e' una VISTA: non si modifica a mano.**" % b[:8])
    w()
    w("### 📌 **E IL PRESIDIO NON E' QUESTO DOCUMENTO, E' IL CODICE:** una grandezza del "
      "registro che non compare nella tabella dell'evento ### **ferma il run** con *«regola "
      "di nascita non dichiarata per `<nome>` all'evento `<evento>`»*. Il collaudo a secco "
      "gira ### **all'import**, cosi' una riga che manca ferma il processo ### **prima** che "
      "un run cominci.")
    w()
    w("| | |")
    w("|---|---|")
    w("| **grandezze governate** | ### **%d** *(i %d registri `METRI`+`STATO`+`FINESTRA`, "
      "piu' `_peqn_idx` DICHIARATO dopo `peq`)* |"
      % (len(ordine), len(ordine) - 1))
    w("| **eventi APPROVATI** | `%s` — ### **approvati da Luca il 2026-10-01** |"
      % "` · `".join(S.EVENTI_DI_NASCITA))
    w("| ### **eventi CONVERTITI** | ### **`%s`** — gli altri due vivono nelle loro "
      "funzioni, e `nascita()` ### **si RIFIUTA di girare** per loro invece di far finta |"
      % "` · `".join(eventi))
    w("| **righe in tabella** | ### **%d** |" % len(S.REGOLE_NASCITA))
    w()
    for ev in eventi:
        w("| classe, evento `%s` | quante |" % ev)
        w("|---|---|")
        for cl in ("regola", "collocata", "non si tocca"):
            if conta.get((ev, cl)):
                w("| `%s` | **%d** |" % (cl, conta[(ev, cl)]))
        w()
    w("### ⚠ **E L'ORDINE E' PARTE DEL CONTRATTO, MISURATO** "
      "*(`csv/_test_fork/_ordine_registro.py`)*: `phi` prima di `twp` · `peq` prima di "
      "`_peqn_idx` · `n0` nel **contesto** · le **6 chiamate con effetto** collocate a mano. "
      "### **4 vincoli genuini, 0 violazioni dall'ordine del registro.**")
    w()
    w("---")
    for ev in eventi:
        w()
        w("# **EVENTO `%s`**" % ev)
        w()
        w("| # | grandezza | classe | regola | ancora |")
        w("|---|---|---|---|---|")
        for k, nome in enumerate(ordine):
            v = S.REGOLE_NASCITA[(ev, nome)]
            cl = v["classe"] if v["regola"] is None else "regola"
            segno = {"collocata": "🔧", "non si tocca": "—"}.get(cl, "✅")
            w("| %d | **`%s`** | %s %s | %s | `%s` |"
              % (k, nome, segno, cl, v["classe"],
                 str(v["ancora"]).replace("|", "\\|")[:150]))
        w()
        w("## Le derivazioni, evento `%s`" % ev)
        w()
        for nome in ordine:
            v = S.REGOLE_NASCITA[(ev, nome)]
            w("- **`%s`** — *%s*: %s" % (nome, v["classe"],
                                         str(v["derivazione"]).replace("|", "\\|")))
        w()
    p_md = os.path.join(RADICE, "doc", "TABELLA_nascita.md")
    io.open(p_md, "w", encoding="utf-8", newline=NL).write(NL.join(M) + NL)

    print("=" * 92)
    print("  simulatore ...... blob %s (sha1 byte grezzi)" % b[:8])
    print("  grandezze ....... %d" % len(ordine))
    print("  eventi convertiti %s" % ", ".join(eventi))
    print("  righe ........... %d" % len(S.REGOLE_NASCITA))
    for ev in eventi:
        print("    %-12s %s" % (ev, ", ".join("%s=%d" % (c, n) for (e, c), n
                                              in sorted(conta.items()) if e == ev)))
    print("  scritti:")
    for p in (p_tsv, p_md):
        print("    %-42s blob %s" % (os.path.relpath(p, RADICE).replace(chr(92), "/"),
                                     blob(p)[:8]))


if __name__ == "__main__":
    principale()
