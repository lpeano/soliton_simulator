# -*- coding: utf-8 -*-
"""LA RIGA D'ORIGINE DI UNA VOCE — **intera, non il titolo troncato.**

> ### ⛔ **Il mandato dice: «leggi la RIGA D'ORIGINE intera (non il titolo troncato)».**
> I titoli dell'indice sono `<= 100` caratteri, e ### **un troncamento taglia esattamente
> dove la riga dice lo stato** — *«… ⏳[EPOCA 1 · MISURA] | DO…»*. ### **La riverifica
> precedente non aveva aperto le righe troncate**, e il guardiano lo dichiara come
> ### **errore (d)**.

**Come si ritrova:** `fonte` e' `<file>::<prefisso del testo>`. Si cerca nel file
### **la riga che CONTIENE quel prefisso**, e ### **se ce n'e' piu' d'una o nessuna si
dichiara**, non si indovina.

Gira con:  python csv/_righe_origine.py            # quante si ritrovano
           python csv/_righe_origine.py <ID> ...   # la riga di quegli ID
"""
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Legge documenti.
NL = chr(10)
BT = chr(96)
EMOJI = (chr(0x1F7E9), chr(0x1F7E8), chr(0x1F7E5), chr(0x1F7E6), chr(0x23F3), chr(0x2705), chr(0x26D4), chr(0x26A0))
D = os.path.join(RADICE, "doc", "indice")
_CACHE = {}


def voci():
    return [json.loads(r) for r in io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8")
            if r.strip()]


def righe_di(f):
    if f not in _CACHE:
        p = os.path.join(RADICE, f)
        _CACHE[f] = (io.open(p, encoding="utf-8", errors="replace").read().split(NL)
                     if os.path.exists(p) else [])
    return _CACHE[f]


def norm(s):
    """### ⛔ **Il prefisso di `fonte` e- SENZA le decorazioni della riga vera:** il titolo
    dell-indice e- stato ripulito dei `**` e dei backtick quando la voce e- nata.
    ### **Quindi si confronta su una forma SPOGLIA**, da entrambi i lati -- altrimenti
    ### **nessuna riga si ritrova**, e la prima stesura ne ritrovava `1` su `7`.
    """
    # ### ⚠ **E le EMOJI DI STATO vanno via dal confronto**, perche- alcuni titoli le
    # ### hanno perse e altri no: `Z25` tiene il suo `🟨`, `Z47` ha perso il `🟩`.
    # ### ### **Si spogliano solo per CONFRONTARE**: la regola dello stato legge la riga
    # ### ### **VERA**, dove il `✅` conta.
    s = (s or "").replace("*", "").replace(BT, "")
    for _e in EMOJI:
        s = s.replace(_e, "")
    return " ".join(s.split())


def blocco(rr, k):
    """### La riga, ### **piu- la SEZIONE che la segue se e- un-intestazione.**

    ### ⛔ **Serve per il caso che il mandato nomina:** `CURA1-CORTO` ha come riga
    d-origine `## APERTO CURA1-CORTO` -- ### **un-intestazione di un REGISTRO DI CORSE** --
    e il *<<chiuso 2026-09-24 ... FINITO>>* sta ### **SOTTO.** Leggere la sola riga direbbe
    ### **APERTA**, ed e- ### **l-errore (a) che il guardiano dichiara.**

    ### ⚠ **Solo per le INTESTAZIONI**, e per al massimo `40` righe o fino alla prossima:
    una riga di tabella ### **si chiude da se-.**
    """
    r = rr[k]
    if not r.lstrip().startswith("#"):
        return r
    fuori = [r]
    for x in rr[k + 1:k + 41]:
        if x.lstrip().startswith("#"):
            break
        fuori.append(x)
    return NL.join(fuori)


def riga_origine(v):
    """### La riga INTERA da cui la voce viene, oppure ### **il motivo per cui non c'e'.**

    ### ⛔ **Non si indovina:** se il prefisso di `fonte` compare in ### **piu' di una riga**,
    si restituisce ### **`AMBIGUA`** con quante; se in ### **nessuna**, `NON TROVATA`.
    ### **Un prefisso che non identifica una riga non e' una fonte.**
    """
    f = v["fonte"] or ""
    if "::" not in f:
        return (None, "la fonte non ha `::`: %r" % f[:60], 0)
    file_, _, pref = f.partition("::")
    pref = norm(pref)
    if not pref:
        return (None, "il prefisso della fonte e' vuoto", 0)
    rr = righe_di(file_)
    if not rr:
        return (None, "il file `%s` non c'e'" % file_, 0)
    # ### ⚠ **Il prefisso e' TRONCATO nel `fonte`**, quindi si cerca per CONTENIMENTO; e si
    # ### accorcia finche' non identifica una riga sola, ### **ma non sotto i 24 caratteri.**
    # ### ⛔ **UN PREFISSO CORTO E- UN PREFISSO VALIDO:** `APERTO CURA1-CORTO` ha `18`
    # ### caratteri, e la prima stesura si fermava sotto i `24` ### **senza nemmeno
    # ### provare** -- quindi `CURA1-CORTO`, che il mandato nomina fra i casi di collaudo,
    # ### ### **risultava NON TROVATA.** Si parte dal prefisso INTERO e si accorcia solo
    # ### se trova PIU- di una riga.
    tagli = [len(pref)] + [k for k in (90, 70, 50, 36, 24) if k < len(pref)]
    ultima = None
    for taglio in tagli:
        q = pref[:taglio]
        trovate = [(n, r) for n, r in enumerate(rr, 1) if q in norm(r)]
        if len(trovate) == 1:
            return (blocco(rr, trovate[0][0] - 1), file_, trovate[0][0])
        if trovate:
            # ### ⛔ **LO SPAREGGIO, e serve per un caso vero:** il prefisso di
            # ### `SIGILLO-CURA2` e- contenuto anche in `## APERTO
            # ### SIGILLO-CURA2-RIPARATO`, quindi due righe lo contengono.
            # ### ✔ **Vince la riga PIU- CORTA**, perche- la- il prefisso e- ### **tutto
            # ### il contenuto** e non un pezzo di un nome piu- lungo -- e ### **solo se
            # ### la piu- corta e- UNICA**, altrimenti resta AMBIGUA.
            corte = sorted(trovate, key=lambda x: len(norm(x[1])))
            if len(norm(corte[0][1])) < len(norm(corte[1][1])):
                return (blocco(rr, corte[0][0] - 1), file_, corte[0][0])
            ultima = trovate
    if ultima:
        return (None, "AMBIGUA in `%s`: %d righe contengono il prefisso"
                % (file_, len(ultima)), 0)
    return (None, "NON TROVATA in `%s`" % file_, 0)


def main(argv):
    vv = voci()
    per = {v["id"]: v for v in vv}
    if argv:
        for i in argv:
            v = per.get(i)
            if v is None:
                print("### `%s` NON E' UNA VOCE" % i)
                continue
            r, dove, n = riga_origine(v)
            print("### `%s`   [%s/%s/era %s/%s]"
                  % (i, v["classe"], v["dominio"], v["era"], v["stato"]))
            if r is None:
                print("    ### %s" % dove)
            else:
                print("    %s:%d" % (dove, n))
                print("    %s" % norm(r)[:600])
            print()
        return 0
    ok, no = 0, {}
    for v in vv:
        r, dove, _n = riga_origine(v)
        if r is None:
            no.setdefault(dove.split(":")[0], []).append(v["id"])
        else:
            ok += 1
    print("=" * 100)
    print("LA RIGA D'ORIGINE: ritrovata per %d voci su %d" % (ok, len(vv)))
    print("=" * 100)
    for k in sorted(no, key=lambda x: -len(no[x])):
        print("  %-52s %4d   %s" % (k[:52], len(no[k]), " ".join(no[k][:5])))
    p = os.path.join(D, "_righe_origine.json")
    io.open(p, "w", encoding="utf-8", newline=NL).write(json.dumps(
        {v["id"]: norm(riga_origine(v)[0]) for v in vv if riga_origine(v)[0] is not None},
        ensure_ascii=False, indent=1))
    print()
    print("  scritto doc/indice/_righe_origine.json")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
