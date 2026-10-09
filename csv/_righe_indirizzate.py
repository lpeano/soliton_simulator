# -*- coding: utf-8 -*-
"""IL PUNTO `2`: **le `10` righe con la citazione a `file:riga`.**

> ### ⭐ **E' LA CURA DI UN MIO DIFETTO DI RITROVAMENTO.** Le citazioni erano ### **giuste**:
> ### **io cercavo nel file della `fonte`**, che per quelle voci ### **non è il file dove la
> frase sta.** ### ⛔ **Dichiaravo «NON COMPARE» una frase che c'era**, e il referto la
> metteva fra le *«non applicate»*.

**Il controllo del mandato è più STRETTO del mio, non più largo:** *«per ognuna verifica che
la frase sia ### **ESATTAMENTE alla riga indicata** (`file:riga`); se sì, applica; se no,
elenca»*.

### ⛔ **E un INDIRIZZO SBAGLIATO NON SI CORREGGE A MANO:** se la riga `N` non porta la
frase, ### **non si cerca alla riga `N±1` e non si cerca altrove.** ### **Si elenca.**

Gira con:  python csv/_righe_indirizzate.py
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
import _applica_correzioni_guardiano as AP                   # noqa: E402
import _commit_di_chiusura as CC                             # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Costruisce un lotto.
NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
DATA = "2026-10-09"

# ### LE `10` RIGHE, ### **con l'INDIRIZZO che il guardiano ha dato.** Formato:
# ### `(id, {campo: valore}, frase, file, riga)`.
LE10 = (
    ("DRIVER-SCENA-II", {"classe": "CURA", "stato": "CHIUSA"},
     "il SIGILLO di `DRIVER-SCENA-II`", "doc/INVENTARIO_strumenti.md", 927),
    ("M0a", {"classe": "MISURA", "stato": "CHIUSA"},
     "MISURA 0", "doc/INVENTARIO_strumenti.md", 924),
    ("REGISTRO_FISICA:V8", {"stato": "CHIUSA"},
     "LA MISURA CHE L'HA DECISA", "doc/REGISTRO_FISICA.md", 435),
    ("REGISTRO_FISICA:V9", {"stato": "CHIUSA"},
     "LA MISURA CHE L'HA DECISA", "doc/REGISTRO_FISICA.md", 435),
    ("Z119", {"classe": "MISURA"},
     "`Z119`: letto dal sorgente", "doc/STATO_RUN.md", 653),
    ("ETC-PASSO", {"stato": "SUPERATA", "superata_da": "SCHED-PASSO"},
     "chiusa come superata il 2026-09-28", "doc/SMISTAMENTO_run_base.md", 216),
    ("P6", {"classe": "STANDARD", "stato": "SUPERATA", "superata_da": "P3"},
     "fuse dentro", "doc/PATTERN_DI_PROVA.md", 141),
    ("STANDARD-8", {"stato": "SUPERATA", "superata_da": "A12"},
     "e non si duplica", "doc/PATTERN_DI_PROVA.md", 140),
    ("P3", {"classe": "STANDARD"},
     "del hook", "doc/PATTERN_DI_PROVA.md", 143),
    ("M-SPINORE", {"classe": "FRONTE"},
     "un fronte, non una cura", "doc/MEMORIE_MANCANTI.md", 362),
)


def alla_riga(file_, n, frase):
    """### La frase e- ### **ESATTAMENTE alla riga `n`** *(`1`-based)*?

    ### ⛔ **Si normalizza come nel punto `3` del mandato precedente** *(senza markdown,
    accenti piegati, spazi normalizzati)*, perche- ### **il guardiano scrive la frase a
    mano** e il file la porta con i backtick e gli accenti suoi. ### ⚠ **Ma la RIGA e-
    quella**: ### **non `n-1`, non `n+1`, non altrove.**
    """
    rr = AP.righe_file(file_)
    if not rr:
        return (False, "il file `%s` non si legge" % file_)
    if n < 1 or n > len(rr):
        return (False, "il file `%s` ha %d righe, e la %d non esiste" % (file_, len(rr), n))
    riga = rr[n - 1]
    if AP.pulisci(frase).upper() in AP.pulisci(riga).upper():
        return (True, " ".join(riga.split())[:200])
    return (False, ("### LA RIGA %d DI `%s` NON PORTA LA FRASE. La riga e-: <<%s>>"
                    % (n, file_, " ".join(riga.split())[:140])))


def main():
    voci = [json.loads(x) for x in
            io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8").read().split(NL)
            if x.strip()]
    per = {v["id"]: v for v in voci}
    import indice as IX
    _vv, reg = IX.carica()
    tag = CC.sha_del_tag()
    lotto, fatte, non_fatte = [], [], []
    for i, cambi, frase, file_, n in LE10:
        v = per[i]
        ok, dove = alla_riga(file_, n, frase)
        if not ok:
            non_fatte.append((i, frase, "%s:%d" % (file_, n), dove))
            continue
        # ### ⭐ **IL MOTIVO LO DETTA IL MANDATO, ALLA LETTERA:**
        # ### *<<verifica completa del guardiano: <frase> (<file:riga>)>>*.
        mot = "verifica completa del guardiano: %s (%s:%d)" % (frase, file_, n)
        campi = dict(cambi)
        salta = [k for k in list(campi) if str(v[k]) == campi[k]]
        for k in salta:
            del campi[k]
        if not campi:
            non_fatte.append((i, frase, "%s:%d" % (file_, n),
                              "NIENTE DA FARE: i campi sono gia- quelli"))
            continue
        # ### ⛔ **`SUPERATA` pretende `superata_da`, e lo schema lo verifica:** qui il file
        # ### lo porta, e ### **viene col suo stato** -- la stessa lezione di due commit fa.
        if campi.get("stato") == "SUPERATA":
            s = campi.get("superata_da") or v["superata_da"]
            assert s and (s in reg["decisioni"] or s in reg["assiomi"] or s in per), (
                "`%s`: `superata_da` %r non e- ne- decisione, ne- assioma, ne- voce" % (i, s))
        # ### ⛔ **E CHIUDERE PRETENDE IL COMMIT, che SI RICAVA** *(il punto `1` del mandato
        # ### precedente)*: ### **la frase e- quella, e il file adesso e- QUELLO GIUSTO.**
        if campi.get("stato") == "CHIUSA":
            ago, dv = CC.riga_grezza(file_, frase, n)
            sha = CC.commit_che_introduce(file_, ago) if ago else None
            campi["chiusura"] = {
                "criterio": ("%s [COMMIT %s: %s]"
                             % (mot, "RICAVATO" if sha else "DAL TAG",
                                dv if sha else ("la frase e- a %s:%d ma `git log -S` non la "
                                                "trova nella storia" % (file_, n))))[:400],
                "commit": sha or tag, "data": DATA}
        # ### ⛔ **E SE LO STATO ESCE DA `CHIUSA`, la `chiusura` SI SVUOTA** (`F12`).
        if (campi.get("stato") and campi["stato"] != "CHIUSA"
                and (v["chiusura"] or {}) and "chiusura" not in campi):
            campi["chiusura"] = {}
        st = campi.get("stato")
        if st and st != v["stato"] and st not in IX.TRANSIZIONI.get(v["stato"], set()):
            lotto.append({"id": i, "quando": DATA, "campi": {"stato": "APERTA"},
                          "motivo": ("(2) PONTE OBBLIGATO da `%s` a `%s`: TRANSIZIONI non "
                                     "passa. %s" % (v["stato"], st, mot))[:1200]})
        lotto.append({"id": i, "quando": DATA, "campi": campi, "motivo": mot[:1200]})
        fatte.append((i, campi, "%s:%d" % (file_, n), dove))
    p = os.path.join(D, "_lotti", "v3_indirizzate.jsonl")
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in lotto) + NL)
    io.open(os.path.join(D, "_p2_indirizzate.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(
                {"fatte": [{"id": a, "campi": b, "indirizzo": c, "riga": d}
                           for a, b, c, d in fatte],
                 "non_fatte": [{"id": a, "frase": b, "indirizzo": c, "perche": d}
                               for a, b, c, d in non_fatte]},
                ensure_ascii=False, indent=1))
    print("  scritto doc/indice/_lotti/v3_indirizzate.jsonl: %d righe" % len(lotto))
    print("  ### LA FRASE E- ALLA RIGA INDICATA -> APPLICATE: %d su %d"
          % (len(fatte), len(LE10)))
    for i, campi, ind, dove in fatte:
        print("   %-22s %-34s %s" % (i, json.dumps(campi, ensure_ascii=True)[:34], ind))
        print("        %s" % dove[:150])
    print("  ### NON APPLICATE: %d" % len(non_fatte))
    for i, frase, ind, perche in non_fatte:
        print("   %-22s <<%s>>  %s" % (i, frase[:34], ind))
        print("        %s" % perche[:160])
    return 0


if __name__ == "__main__":
    sys.exit(main())
