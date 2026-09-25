# -*- coding: utf-8 -*-
"""**INVENTARIO: chi avanza con `net.step()` SENZA le altre chiamate del passo.**

> **Decisione di Luca, 2026-09-25:** *«INVENTARIO (come per `ramp`): ogni script in `csv/` che
> avanza con `net.step()` senza le altre `4` chiamate. Per ciascuno: STRUTTURALE (identità di
> byte, non dipende dal ciclo) o MISURA; per le misure, quale conclusione registrata ne dipende.
> **Tabella generata, non ricopiata.**»*

**L'ORDINE DEL PASSO SI LEGGE DA `csv/_passo.py`**, che a sua volta lo legge per AST da
`update()` e lo verifica contro il driver. **Non è ricopiato qui.**

**COME CLASSIFICA, e il criterio è dichiarato:**

```
STRUTTURALE   il file contiene segni di confronto BYTE/IDENTITA' -- `tobytes`, `sha1`,
              `firma_byte`, `byte-identic`, `array_equal`, `max|A-B|` -- e NON contiene
              segni di misura statistica. Un'identita' di byte fra due bracci che avanzano
              ALLO STESSO MODO non dipende dal ciclo: se sbaglia il ciclo, sbaglia in
              entrambi, e l'identita' regge o cade per altre ragioni.
MISURA        il file contiene percentili/medie/correlazioni/pendenze -- `percentile`,
              `median`, `mean`, `corrcoef`, `polyfit`, `std` -- su grandezze fisiche.
ENTRAMBI      li ha tutti e due: **va letto a mano**, e la tabella lo dice invece di scegliere.
```

**⚠ E IL LIMITE DEL CRITERIO SI DICHIARA:** è un'euristica **sui nomi presenti nel file**, non
una dimostrazione. **Un file marcato STRUTTURALE potrebbe contenere una misura**, e la colonna
«conclusioni» serve proprio a farlo vedere. **Non è un inventario CERTIFICATO: è la prima
tabella generata, e va letta come tale** *(è la stessa onestà che par.9 impone al conteggio dei
blob nelle voci: *«non è un presidio: è una MISURA»*)*.

**LE CONCLUSIONI CHE DIPENDONO:** per ogni script si cerca **il suo nome** in `doc/` e in
`RELAZIONE_PER_CLAUDE.md`, e si riportano i file che lo citano. **È il legame che il mandato
chiede**, e viene da una ricerca, non dalla memoria.
"""
import ast
import io
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _passo
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
DEST = os.path.join(RADICE, "doc", "INVENTARIO_passo_incompleto.md")

NOMI = [n for _, n in _passo.ordine()]
ALTRI = [n for n in NOMI if n != "step"]

SEGNI_STRUTT = ("tobytes", "sha1", "firma_byte", "byte-identic", "byte-ident", "array_equal",
                "max|A-B|", "identita'", "IDENTICO", "hexdigest")
SEGNI_MISURA = ("percentile", "np.median", "np.mean", "corrcoef", "polyfit", ".std(",
                "np.std", "pendenza", "quantil")

ESCLUSI = ("_old_sim_pre_", "._sim.py", "_sim_vecchio.py", "_passo.py", "_inventario_passo.py")
# ⚠ I FIGLI GENERATI NON SI INVENTARIANO: `csv/**/_tmp/_br_*.py` sono scritti DAI SIGILLI a
#   ogni corsa, e contarli GONFIA il conto senza aggiungere un file da curare -- si cura il
#   GENITORE. **Si escludono per PERCORSO, e si dichiara quanti sono.**
ESCLUSI_DIR = ("/_tmp/", chr(92) + "_tmp" + chr(92))


def _chiamate(src):
    """I nomi EFFETTIVAMENTE CHIAMATI nel file, per AST.

    ❌❌ LA PRIMA STESURA CERCAVA `(nome + "(")` NEL TESTO, e **un file che MENZIONA `mitosi`
       in un commento veniva contato come se la CHIAMASSE.** È `STANDARD 9` al contrario: *una
       PRESENZA dedotta da un `in` sul testo è lo stesso errore di un'ASSENZA dedotta così*.
       **E qui il difetto non è teorico:** ogni referto che spiega «la mitosi resta morta»
       contiene la parola `mitosi(`, e quei file risultavano «completi».
    """
    try:
        arb = ast.parse(src)
    except Exception:
        return None
    out = set()
    for n in ast.walk(arb):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Attribute):
                out.add(f.attr)
            elif isinstance(f, ast.Name):
                out.add(f.id)
    return out


SALTATI = []
NON_PARSABILI = []


def scandisci():
    out = []
    for radice, _dirs, files in os.walk(os.path.join(RADICE, "csv")):
        for f in sorted(files):
            if not f.endswith(".py") or any(x in f for x in ESCLUSI):
                continue
            p = os.path.join(radice, f)
            rel = os.path.relpath(p, RADICE).replace(chr(92), "/")
            if any(x in ("/" + rel) for x in ("/_tmp/",)):
                SALTATI.append(rel)
                continue
            try:
                src = io.open(p, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            ch = _chiamate(src)
            if ch is None:
                NON_PARSABILI.append(rel)
                continue
            if "step" not in ch:
                continue
            # quali altre chiamate del passo sono EFFETTIVAMENTE CHIAMATE (AST, non testo)?
            presenti = [n for n in ALTRI if n in ch]
            # usa il modulo condiviso?
            usa_modulo = ("passo_pieno" in ch) or ("_passo" in src and "import _passo" in src)
            # quante volte `.step()` compare
            n_step = len(re.findall(r"\.step\(\)", src))
            strutt = sum(1 for s in SEGNI_STRUTT if s in src)
            mis = sum(1 for s in SEGNI_MISURA if s in src)
            if strutt and mis:
                classe = "ENTRAMBI"
            elif strutt:
                classe = "STRUTTURALE"
            elif mis:
                classe = "MISURA"
            else:
                classe = "NON CLASSIFICATO"
            out.append(dict(file=rel,
                            n_step=n_step, presenti=presenti,
                            mancanti=[n for n in ALTRI if n not in presenti],
                            usa_modulo=usa_modulo, classe=classe,
                            segni_strutt=strutt, segni_mis=mis))
    return out


def citazioni(nome_file):
    """Chi CITA questo script, in `doc/` e nella relazione. E' il legame alle conclusioni."""
    base = os.path.basename(nome_file)
    stem = base[:-3] if base.endswith(".py") else base
    trovati = []
    da_guardare = [os.path.join(RADICE, "RELAZIONE_PER_CLAUDE.md")]
    dd = os.path.join(RADICE, "doc")
    for r, _d, fs in os.walk(dd):
        for f in fs:
            if f.endswith(".md"):
                da_guardare.append(os.path.join(r, f))
    for p in da_guardare:
        try:
            s = io.open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        if stem in s:
            trovati.append(os.path.relpath(p, RADICE).replace(chr(92), "/"))
    return trovati


V = scandisci()
# INCOMPLETI = avanzano con `step()` e NON hanno tutte le altre chiamate, e non usano il modulo
INC = [x for x in V if x["mancanti"] and not x["usa_modulo"]]
OK_ = [x for x in V if not x["mancanti"] or x["usa_modulo"]]

R = []


def P(s=""):
    R.append(s)


P("# INVENTARIO — **chi avanza con `net.step()` senza le altre chiamate del passo**")
P()
P("> **Generato da `csv/_inventario_passo.py`. Non ricopiato.**")
P("> **L'ordine del passo è letto da `csv/_passo.py`**, che lo legge per AST da `update()` e lo")
P("> verifica contro il driver.")
P()
P("```")
P(_passo.descrivi())
P("```")
P()
P("**Trovati `%d` file sotto `csv/` che CHIAMANO `step()`** *(per AST, non per testo)*." % len(V))
P()
P("**⚠ DUE CORREZIONI AL PRIMO CONTEGGIO, ed erano difetti miei:**")
P("1. **i nomi erano cercati NEL TESTO** *(`(nome + \"(\") in src`)*: **un file che MENZIONA")
P("   `mitosi` in un commento veniva contato come se la CHIAMASSE.** È `STANDARD 9` al")
P("   contrario, e **non era teorico**: ogni referto che spiega «la mitosi resta morta»")
P("   contiene `mitosi(`, e quei file risultavano «completi». **Ora è AST.**")
P("2. **i figli GENERATI erano contati:** `csv/**/_tmp/_br_*.py` sono scritti dai sigilli a ogni")
P("   corsa. **Contarli gonfia il conto senza aggiungere un file da curare** — si cura il")
P("   GENITORE. **Saltati `%d`**, e il numero è detto invece di essere nascosto." % len(SALTATI))
if NON_PARSABILI:
    P()
    P("**⚠ `%d` file NON si sono potuti analizzare** *(sintassi non valida per l'AST di questa"
      % len(NON_PARSABILI))
    P("   versione di Python)*: `%s`. **Non contano né come completi né come incompleti, e va"
      % ", ".join("`%s`" % x for x in NON_PARSABILI[:6]))
    P("   detto.**")
P("**Di questi, `%d` NON hanno tutte le altre chiamate e NON usano il modulo condiviso.**" % len(INC))
P()
P("## IL CRITERIO DI CLASSIFICAZIONE, dichiarato — e il suo LIMITE")
P()
P("`STRUTTURALE` = contiene segni di identità di byte *(`tobytes`, `sha1`, `firma_byte`,")
P("`array_equal`, …)* e non di statistica. **Un'identità di byte fra due bracci che avanzano ALLO")
P("STESSO MODO non dipende dal ciclo:** se il ciclo è sbagliato, è sbagliato in entrambi.")
P()
P("`MISURA` = contiene percentili, medie, correlazioni, pendenze.")
P()
P("> **⚠ È UN'EURISTICA SUI NOMI PRESENTI NEL FILE, NON UNA DIMOSTRAZIONE.** Un file marcato")
P("> `STRUTTURALE` potrebbe contenere una misura. **Non è un inventario certificato: è la prima")
P("> tabella generata**, e va letta come tale — la stessa onestà che par.9 impone al conteggio")
P("> dei blob nelle voci *(«non è un presidio: è una MISURA»)*.")
P()
P("## LA TABELLA — i file che avanzano in modo INCOMPLETO")
P()
P("| file | `.step()` | manca | classe | chi lo cita |")
P("|---|--:|---|---|---|")
for x in sorted(INC, key=lambda z: (z["classe"], z["file"])):
    cit = citazioni(x["file"])
    P("| `%s` | %d | %s | **%s** | %s |"
      % (x["file"], x["n_step"], ", ".join("`%s`" % m for m in x["mancanti"]) or "—",
         x["classe"], ", ".join("`%s`" % c for c in cit) or "*nessuno*"))
P()
P("## E I FILE CHE VANNO BENE, o che usano il modulo condiviso")
P()
P("| file | `.step()` | come avanza |")
P("|---|--:|---|")
for x in sorted(OK_, key=lambda z: z["file"]):
    P("| `%s` | %d | %s |" % (x["file"], x["n_step"],
                              "usa `_passo`/`passo_pieno`" if x["usa_modulo"]
                              else "ha tutte le chiamate"))
P()
P("## ❗ E DUE SITI **NEL SIMULATORE STESSO**")
P()
P("| riga | sequenza spezzata? | altri nomi vicini | testo |")
P("|--:|---|---|---|")
for s in _passo.soli():
    P("| `%d` | %s | %s | `%s` |"
      % (s["riga"], "**sì** *(è il passo completo, interrotto dalle assegnazioni)*"
         if s["spezzata"] else "**NO — È UN AVANZAMENTO INCOMPLETO**",
         ", ".join("`%s`" % a for a in s["altri_vicini"]) or "nessuno",
         s["testo"].replace("|", "\\|")))
P()
P("> ### ❗ **`:8404` È UN DIFETTO VERO, E STA NEL SIMULATORE:**")
P("> `for _ in range(300): net.step()` nel percorso di ricostruzione con `--seed`/`--nodi`.")
P("> **Trecento passi senza mitosi, senza scuotimento e senza memoria del moto**, per")
P("> «invecchiare» la rete. **È lo stesso difetto delle sonde, dentro il codice che le sonde")
P("> imitano.** → va in coda.")
P()
P("## RIEPILOGO PER CLASSE")
P()
from collections import Counter

cc = Counter(x["classe"] for x in INC)
P("| classe | quanti |")
P("|---|--:|")
for k, v in sorted(cc.items()):
    P("| **%s** | %d |" % (k, v))
P()
P("**I `MISURA` e gli `ENTRAMBI` sono quelli le cui conclusioni possono dipendere dal ciclo.**")
P("La colonna «chi lo cita» dice **dove cercare quelle conclusioni**; il legame è una ricerca")
P("per NOME, non una lettura del merito — e va detto.")

T = chr(10).join(R) + chr(10)
io.open(DEST, "w", encoding="utf-8", newline="\n").write(T)
print(T[:3000])
print("...")
print("scritto in %s" % os.path.relpath(DEST, RADICE))
