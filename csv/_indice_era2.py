# -*- coding: utf-8 -*-
"""LA VIA DI SCRITTURA DEI REGISTRI DELL'ERA `2` — **una sola, come per le voci.**

> ### ⛔ **`doc/indice/leggi.jsonl` e `doc/indice/variabili.jsonl` si scrivono SOLO da qui**
> *(e `python csv/indice.py era2-lotto <file>` è il comando)*. ### **A mano, mai** — è la
> stessa regola del par.9 per `voci.jsonl`.

### ⭐ **E LO STORICO STA IN UN FILE SUO** *(`doc/indice/storico_era2.jsonl`)*, non in
`storico.jsonl`: quello porta ### **righe di VOCE** *(`prima`/`dopo` dei campi di una
voce)*, e `F5` e `F11` le leggono così. ### ⛔ **Mescolare due forme di riga in un file
solo è il difetto che questo repo chiama «due cose in un posto»** — e `F11`, che
ricostruisce l'indice dal suo storico, ### **leggerebbe una riga che non è una voce.**

### ⚠ **LE `21` RIGHE VECCHIE DI `leggi.jsonl` NON HANNO IL CAMPO `era`:** sono
### **ancore di traduzione dell'era `1`**, e ### **non si toccano.** La validazione
dell'era `2` guarda ### **solo le righe che dichiarano `era: "2"`.**

Gira con:  python csv/indice.py era2-lotto doc/indice/_lotti/<file>.jsonl
           python csv/_indice_era2.py --valida
           python csv/_indice_era2.py --collaudo
"""
import io
import json
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)

NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
LEGGI = os.path.join(D, "leggi.jsonl")
VARIA = os.path.join(D, "variabili.jsonl")
STORICO = os.path.join(D, "storico_era2.jsonl")

# ### I CAMPI di una riga dell-era `2`, a vocabolario CHIUSO.
CAMPI_LEGGE = ("id", "era", "titolo", "voce", "scheda", "prova", "impronta", "fonte")
CAMPI_VARIABILE = ("id", "era", "nome", "tipo", "voce", "scheda", "fonte")
_ID = re.compile(r"^[A-Z][A-Z0-9:_-]{3,}$")


def righe(p):
    if not os.path.exists(p):
        return []
    return [json.loads(r) for r in io.open(p, encoding="utf-8").read().split(NL)
            if r.strip()]


def era2(rr):
    """### Le sole righe che ### **dichiarano `era: "2"`.** Le altre non si guardano."""
    return [x for x in rr if str(x.get("era")) == "2"]


def valida(verboso=True):
    """### Gli errori dei registri dell-era `2`, o `[]`."""
    err = []
    lg, vr = era2(righe(LEGGI)), era2(righe(VARIA))
    for nome, dati, campi in (("leggi", lg, CAMPI_LEGGE),
                              ("variabili", vr, CAMPI_VARIABILE)):
        visti = set()
        for x in dati:
            i = x.get("id") or "<senza id>"
            if not _ID.match(str(i)):
                err.append("`%s`: l-id non ha la forma attesa (almeno 4 caratteri)" % i)
            if i in visti:
                err.append("`%s`: ID DOPPIO in %s.jsonl" % (i, nome))
            visti.add(i)
            manca = sorted(set(campi) - set(x))
            if manca:
                err.append("`%s` (%s): mancano i campi %s" % (i, nome, manca))
            extra = sorted(set(x) - set(campi))
            if extra:
                err.append("`%s` (%s): campi NON previsti %s: il vocabolario e- CHIUSO"
                           % (i, nome, extra))
            if not str(x.get("scheda") or "").strip():
                err.append("`%s` (%s): `scheda` vuota" % (i, nome))
    if verboso:
        print("  i registri dell-era 2: %d leggi, %d variabili" % (len(lg), len(vr)))
        if err:
            for e in err[:12]:
                print("   ### %s" % e)
        else:
            print("  ### TUTTO A POSTO")
    return err


def _scrivi(p, rr):
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in rr) + NL)


def lotto(percorso):
    """### Applica un lotto di righe ai registri dell-era `2`, ### **atomicamente.**

    Ogni riga del lotto: `{dove: leggi|variabili, riga: {...}, motivo: "..."}`.
    ### ⛔ **Se la validazione non passa, NON SI SCRIVE NIENTE** -- la stessa promessa di
    `aggiorna_lotto`, e ### **la stessa cura**: si valida ### **prima** di toccare il disco.
    """
    import subprocess
    dati = [json.loads(r) for r in io.open(percorso, encoding="utf-8").read().split(NL)
            if r.strip()]
    lg, vr = righe(LEGGI), righe(VARIA)
    per = {"leggi": {x["id"]: k for k, x in enumerate(lg) if str(x.get("era")) == "2"},
           "variabili": {x["id"]: k for k, x in enumerate(vr) if str(x.get("era")) == "2"}}
    tab = {"leggi": lg, "variabili": vr}
    storia = []
    for d in dati:
        dove = d["dove"]
        assert dove in tab, dove
        r = d["riga"]
        mot = d.get("motivo", "")
        assert len(mot) >= 20, "il motivo e- troppo corto per CITARE qualcosa: %r" % mot[:40]
        assert str(r.get("era")) == "2", ("una riga scritta da qui DEVE dichiarare "
                                          "`era: \"2\"`: %r" % r.get("id"))
        k = per[dove].get(r["id"])
        prima = json.loads(json.dumps(tab[dove][k])) if k is not None else None
        if k is None:
            tab[dove].append(r)
        else:
            tab[dove][k] = r
        storia.append({"quando": d.get("quando") or "", "dove": dove, "id": r["id"],
                       "motivo": mot, "commit": d.get("commit", ""),
                       "commit_base": subprocess.run(
                           ["git", "rev-parse", "--short", "HEAD"], cwd=RADICE,
                           capture_output=True, text=True).stdout.strip(),
                       "prima": prima, "dopo": json.loads(json.dumps(r))})
    # ### ⛔ **SI VALIDA PRIMA DI SCRIVERE**, e la ragione e- un difetto pagato: un lotto che
    # ### non passa ### **lasciava l-indice CORROTTO sul disco.**
    _scrivi(LEGGI + ".prova", tab["leggi"])
    _scrivi(VARIA + ".prova", tab["variabili"])
    try:
        g_l, g_v = LEGGI, VARIA
        globals()["LEGGI"], globals()["VARIA"] = LEGGI + ".prova", VARIA + ".prova"
        err = valida(verboso=False)
    finally:
        globals()["LEGGI"], globals()["VARIA"] = g_l, g_v
    os.remove(LEGGI + ".prova")
    os.remove(VARIA + ".prova")
    assert not err, ("IL LOTTO NON PASSA LA VALIDAZIONE, e NON SI SCRIVE NIENTE:" + NL
                     + NL.join(err[:10]))
    _scrivi(LEGGI, tab["leggi"])
    _scrivi(VARIA, tab["variabili"])
    with io.open(STORICO, "a", encoding="utf-8", newline=NL) as f:
        f.write(NL.join(json.dumps(x, ensure_ascii=False) for x in storia) + NL)
    print("  lotto dell-era 2 applicato: %d righe; e la validazione passa" % len(storia))
    return 0


def collaudo():
    import _presidio
    _presidio.avvia(__file__)
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-64s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("COLLAUDO DEI REGISTRI DELL-ERA 2 -- nei DUE VERSI")
    print("=" * 100)
    g_l, g_v = LEGGI, VARIA
    try:
        globals()["LEGGI"] = os.path.join(_QUI, "_prova_leggi.jsonl")
        globals()["VARIA"] = os.path.join(_QUI, "_prova_varia.jsonl")

        def metti(rr):
            _scrivi(globals()["LEGGI"], rr)
            _scrivi(globals()["VARIA"], [])

        sana = {"id": "PROVA-UNO", "era": "2", "titolo": "t", "voce": "V-X",
                "scheda": "s", "prova": True, "impronta": "abc", "fonte": "f"}
        metti([sana])
        esito("il caso SANO", valida(verboso=False) == [])
        metti([sana, dict(sana)])
        esito("### DEVE scattare: ID DOPPIO",
              any("DOPPIO" in e for e in valida(verboso=False)))
        metti([{k: v for k, v in sana.items() if k != "scheda"}])
        esito("### DEVE scattare: manca `scheda`",
              any("mancano i campi" in e for e in valida(verboso=False)))
        metti([dict(sana, zzz=1)])
        esito("### DEVE scattare: un campo NON previsto",
              any("vocabolario e- CHIUSO" in e for e in valida(verboso=False)),
              "il vocabolario e- chiuso")
        metti([dict(sana, id="AB")])
        esito("### DEVE scattare: id troppo corto",
              valida(verboso=False) != [])
        # ### ⚠ **E LE RIGHE SENZA `era` NON SI GUARDANO:** sono le `21` dell-era `1`.
        metti([sana, {"id": "L-VECCHIA", "titolo": "t", "ancora": "a", "variabile": "-",
                      "classe_traduzione": "DIAGNOSTICA", "fonte": "f"}])
        esito("NON deve scattare: una riga SENZA `era` (le 21 dell-era 1)",
              valida(verboso=False) == [],
              "la validazione dell-era 2 guarda SOLO le righe che dichiarano era: 2")
    finally:
        for p in (globals()["LEGGI"], globals()["VARIA"]):
            if os.path.exists(p):
                os.remove(p)
        globals()["LEGGI"], globals()["VARIA"] = g_l, g_v
    print("=" * 100)
    print("COLLAUDO DEI REGISTRI DELL-ERA 2: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1]
             else "### QUALCUNO FALLISCE"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


def main(a):
    if "--collaudo" in a:
        return collaudo()
    if "--valida" in a:
        import _presidio
        _presidio.avvia(__file__)
        return 1 if valida() else 0
    if "--lotto" in a:
        import _presidio
        _presidio.avvia(__file__)
        return lotto(a[a.index("--lotto") + 1])
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
