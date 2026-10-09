# -*- coding: utf-8 -*-
"""LA CHIUSURA DEI SEGNALI DEI PRESIDI — **un punto per volta.**

| punto | che cosa |
|---|---|
| `1` | `F1` piu' stretto *(**la formulazione era mia**: citare un assioma non e' essere gemelle)*, `C5` **omonimo**, `Z100` e `C5-INVARIANTI` con l'eccezione |
| `2` | ### **la classe `CRITERIO` e' una cosa sola:** un criterio **dice come si giudica** ⇒ `METODO`. Gli **esiti misurati** ⇒ `MISURA`/`FISICA` |
| `3` | gli `8` di `F2` con l'eccezione **che cita il «sostituisce»**; `ENERGIA-NON-DEFINITA` ### **solo la nota** |
| `4` | `F3`: le cure chiuse col sigillo con l'eccezione, gli altri **letti per intero** |

Gira con:  python csv/_segnali_chiusura.py <1|2|3|4>
"""
import io
import json
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Costruisce lotti per l'indice.
NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
LOTTI = os.path.join(D, "_lotti")
DATA = "2026-10-09"


def carica():
    return [json.loads(r) for r in io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8")
            if r.strip()]


def testo(v):
    return " ".join([v.get("titolo") or "", v.get("descrizione") or "",
                     v.get("fonte") or ""])


def pezzo(v, n=44):
    """### Un pezzo LETTERALE del testo della voce: l'eccezione deve CITARE, e `valida` lo
    pretende *(almeno `20` caratteri)*."""
    t = " ".join(testo(v).split())
    return t[:n]


def scrivi(nome, lotto):
    os.makedirs(LOTTI, exist_ok=True)
    p = os.path.join(LOTTI, nome)
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in lotto) + NL)
    print("  scritto %s: %d voci" % (os.path.relpath(p, RADICE).replace(chr(92), "/"),
                                     len(lotto)))


# ==========================================================================
#   PUNTO 1
# ==========================================================================
# ### I DUE SIGNIFICATI DI `C5`, letti dai testi -- non supposti.
C5_DUE = [("doc/RAMIFICAZIONI.md -- la VOCE `C5`, una MISURA: <<tauluce = d/cs e' PIATTO "
           "=> la sostituzione rompe la...>>"),
          ("doc/STATO_RUN.md e doc/RAMIFICAZIONI.md -- il <<mandato C5>>, cioe' GLI "
           "INVARIANTI: <<INVARIANTI (C5): il programma si ferma quando una grandezza "
           "esce...>>")]


def punto1():
    voci = carica()
    per = {v["id"]: v for v in voci}
    lotto = [{"id": "C5", "quando": DATA, "campi": {},
              "meta": {"omonimo": C5_DUE,
                       "nota_guardiano": "OMONIMO: <<C5>> nomina DUE OGGETTI DIVERSI -- la "
                                         "MISURA su tauluce e il MANDATO degli invarianti. "
                                         "NON si scegli: la scelta e' di Luca"},
              "motivo": ("(1) OMONIMO, e il guardiano l'ha visto leggendo F1: il titolo di "
                         "questa voce dice <<%s>>, cioe' una MISURA su tauluce, mentre Z100 "
                         "e C5-INVARIANTI citano il <<mandato C5>>, che e' GLI INVARIANTI. "
                         "Due oggetti, lo stesso ID" % pezzo(per["C5"], 70))}]
    for i in ("Z100", "C5-INVARIANTI"):
        v = per[i]
        lotto.append({"id": i, "quando": DATA, "campi": {},
                      "meta": {"eccezione_presidio":
                               ["F1: il titolo dice <<%s>> -- il `C5` che cita e' IL MANDATO "
                                "DEGLI INVARIANTI, non la voce `C5` (la misura su tauluce). "
                                "E' un OMONIMO, dichiarato in meta.omonimo di `C5`, non una "
                                "mescolanza di dominio" % pezzo(v, 60)]},
                      "motivo": ("(1) SEGNALE CHIUSO CON ECCEZIONE: F1 segnalava perche' il "
                                 "titolo <<%s>> cita `C5`, ma quel `C5` e' IL MANDATO DEGLI "
                                 "INVARIANTI, un OMONIMO della voce `C5`" % pezzo(v, 60))})
    scrivi("v3_p1.jsonl", lotto)
    print()
    print("  ### I SEGNALI DI `F1` CHE RESTANO, e il mandato chiede di ELENCARLI:")
    sys.path.insert(0, _QUI)
    import indice as IX
    for i, m in IX._f1_gemelle(voci):
        v = per[i]
        print("      %-22s %-10s %-14s %-8s %-8s %s"
              % (i, v["classe"], v["dominio"], v["era"], v["stato"],
                 re.sub(r"il titolo cita ", "cita ", m)[:62]))


# ==========================================================================
#   PUNTO 2  --  la classe CRITERIO e' UNA COSA SOLA
# ==========================================================================
# ### ⛔ **UN CRITERIO PRESCRIVE**, e si riconosce dal verbo o dalla formula del giudizio.
PRESCRIVE = ("deve", "devono", "si verifica", "basta", "serve", "byte-identico",
             "byte identico", "controllo positivo", "caso che deve fallire", "criterio",
             "si misura", "si confronta", "non deve", "va verificato", "si pretende",
             "soglia", "firma dei byte", "DEVE")
# ### **UN ESITO riporta una MISURA come risultato.**
MISURATO = re.compile(r"\d+[.,]\d+|\d+\s*%|=\s*-?\d")


def punto2():
    """### Seleziona i candidati a ESITO; ### **la decisione la prendo LEGGENDO**, e la frase
    di ciascuno finisce nel referto."""
    voci = carica()
    cand = [v for v in voci if v["classe"] == "CRITERIO" and v["dominio"] == "FISICA"]
    print("  le voci `CRITERIO`/`FISICA`: %d" % len(cand))
    esiti, criteri = [], []
    for v in cand:
        t = " ".join(testo(v).split())
        tl = t.lower()
        pres = [s for s in PRESCRIVE if s.lower() in tl]
        num = MISURATO.search(t)
        (esiti if (num and not pres) else criteri).append((v, t, pres, num))
    print("  -> candidati a ESITO MISURATO (numero, e NESSUN verbo prescrittivo): %d"
          % len(esiti))
    print("  -> criteri veri:                                                    %d"
          % len(criteri))
    print()
    for v, t, _p, num in esiti:
        print("      %-24s %s" % (v["id"], t[:104]))
        print("      %-24s ^ il numero: %r" % ("", num.group(0)))
    io.open(os.path.join(D, "_p2_esiti.json"), "w", encoding="utf-8", newline=NL).write(
        json.dumps({"esiti": [{"id": v["id"], "frase": t, "numero": num.group(0)}
                              for v, t, _p, num in esiti],
                    "criteri": [v["id"] for v, _t, _p, _n in criteri]},
                   ensure_ascii=False, indent=1))
    print()
    print("  scritto doc/indice/_p2_esiti.json -- ### la frase di ciascuno, per il referto")
    return esiti, criteri


def main(argv):
    assert argv and argv[0] in ("1", "2", "3", "4"), __doc__
    {"1": punto1, "2": punto2}[argv[0]]()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
