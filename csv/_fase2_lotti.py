# -*- coding: utf-8 -*-
"""FASE 2, PUNTO 2: I LOTTI DELLA CLASSIFICAZIONE PER CONTENUTO.

### ⛔ **OGNI REGOLA LEGGE UN CAMPO O UN MARCATORE *DICHIARATO*, e il motivo lo CITA.**
### **Nessuna parola chiave, e mai il solo titolo.**

| regola | che cosa legge | esito |
|---|---|---|
| `R1` | `motivo_era1` dice *«fronte di epoca 1-2 o «vale per quella scena»: e' una **MISURA DA RIFARE**»*, e la descrizione porta il marcatore ### **`[EPOCA 1 · …]`** o ### **`[EPOCA 2 · …]`** | `FISICA`; ### **era DAL MARCATORE**, per voce; `SOSPESA` *(era `1`)* o `AGENDA` *(era `2`)* |
| `R2` | `motivo_era1` dice *«nessuna prova la lega al run base»*, e sono ### **cure e difetti su flag e variabili dell'era `1`** *(`PEQ_ESATTO`, `ANOM_SIMM`, `SCALA_MIN_PASSO`, `COES_CAUSALE`, `d0`, `phi` su `2π`)* | `FISICA`, era `1`, `SOSPESA` |
| `R4` | la ### **fonte** e' `doc/COMPONENTI_PROMOSSE.md`: sono i ### **criteri di promozione** di componenti dell'era `1` a fisica di default | `FISICA`, era `1`, `SOSPESA` |
| `R5` | la ### **fonte** e' `doc/CENSIMENTO_intenzioni.md`: una ### **dichiarazione del codice che il codice stesso smentisce** | `DOCUMENTAZIONE`, era `1`, `APERTA` |

### ⛔ **E UNA REGOLA SCARTATA, perche' sarebbe stata una trappola:** avevo pensato che
`fonte = doc/REGISTRO_FISICA.md` implicasse `FISICA` *(`55` voci)*. ### **FALSO:** lì stanno
### **sia** criteri di fisica *(«`A13` dice che sotto `LAM` non esiste niente»)* ### **sia**
criteri di ### **VERIFICA** *(«flag SPENTO = BYTE-IDENTICO al codice precedente, firma dei
byte»)*, che sono ### **METODO**. ### ➜ **Quelle `55` SI LEGGONO.**

Gira con:  python csv/_fase2_lotti.py
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

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Costruisce lotti per l'indice.
NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
LOTTI = os.path.join(D, "_lotti")
DATA = "2026-10-09"
PER_LOTTO = 50


def M(v, k):
    return (v["meta"] or {}).get(k, "") or ""


def testo(v):
    return (v["descrizione"] or "") + " " + v["titolo"]


def cit(s, quanti=90):
    """### La CITAZIONE: un pezzo del testo vero, senza tab e senza capo."""
    return " ".join((s or "").split())[:quanti]


def main():
    os.makedirs(LOTTI, exist_ok=True)
    voci = [json.loads(r) for r in io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8")
            if r.strip()]
    res = [v for v in voci if v["stato"] == "DA_CLASSIFICARE"
           and "MAI definito in un registro" not in v["titolo"]]
    lotto = []

    def agg(v, dominio, era, stato, motivo, meta=None):
        lotto.append({"id": v["id"], "quando": DATA,
                      "campi": {"dominio": dominio, "era": era, "stato": stato},
                      "meta": meta or {}, "motivo": motivo})

    n = {"R1": 0, "R2": 0, "R4": 0, "R5": 0}
    for v in sorted(res, key=lambda x: x["id"]):
        mo, f, t = M(v, "motivo_era1"), v["fonte"], testo(v)
        if "MISURA DA RIFARE" in mo:
            # ### ⛔ **UN ERRORE MIO, PRESO LEGGENDO LE VOCI CHIUSE:** avevo mappato
            # ### `[EPOCA 2` sull'### **era 2 dello schema**. ### **E' FALSO.** Le
            # ### <<epoche>> `1`, `2`, `3` sono ### **FASI DI LAVORO sul simulatore del
            # ### SECONDO ordine** *(`Z87`: <<d SCENDE A DIECI VOLTE SOTTO LAM>>; `Z91`:
            # ### <<SCALA_MIN FRENA OGNI SCRITTURA>>)*, mentre l'### **era `2` dello schema
            # ### e' la RISCRITTURA al primo ordine** -- e quella e' ### **la lista `L2` di
            # ### Luca**, non un marcatore nel testo. ### ➜ **Tutte le epoche vanno nell'era
            # ### `1`**, e le `4` voci che avevo messo in `AGENDA` sono state corrette.
            m2 = [x for x in ("[EPOCA 1", "[EPOCA 2", "[EPOCA 3") if x in t]
            marc = m2[0] if m2 else "(senza marcatore d'epoca)"
            agg(v, "FISICA", "1", "SOSPESA",
                "(R1) `motivo_era1` dice <<%s>>, e il testo porta `%s`: e' una MISURA del "
                "sistema, quindi FISICA. ### E L'<<EPOCA>> NON E' L'ERA: le epoche sono fasi "
                "di lavoro sul SECONDO ordine, quindi era 1"
                % (cit(mo, 60), marc))
            n["R1"] += 1
        elif "non blocca fino a prova contraria" in mo:
            agg(v, "FISICA", "1", "SOSPESA",
                "(R2) `motivo_era1` dice <<%s>>, e la voce e' su un flag o una variabile "
                "dell'era 1: <<%s>>" % (cit(mo, 60), cit(t, 70)))
            n["R2"] += 1
        elif f.startswith("doc/COMPONENTI_PROMOSSE"):
            agg(v, "FISICA", "1", "SOSPESA",
                "(R4) la fonte e' `doc/COMPONENTI_PROMOSSE.md`, il registro che promuove una "
                "componente a fisica di DEFAULT: <<%s>>" % cit(t, 80))
            n["R4"] += 1
        elif f.startswith("doc/CENSIMENTO_intenzioni"):
            agg(v, "DOCUMENTAZIONE", "1", "APERTA",
                "(R5) la fonte e' `doc/CENSIMENTO_intenzioni.md`: una DICHIARAZIONE del "
                "codice che il codice stesso smentisce -- <<%s>>" % cit(t, 80))
            n["R5"] += 1

    # ### i lotti da `PER_LOTTO`, e ciascuno si committa a se'
    nomi = []
    for k in range(0, len(lotto), PER_LOTTO):
        p = os.path.join(LOTTI, "contenuto_%02d.jsonl" % (k // PER_LOTTO + 1))
        io.open(p, "w", encoding="utf-8", newline=NL).write(
            NL.join(json.dumps(x, ensure_ascii=False) for x in lotto[k:k + PER_LOTTO]) + NL)
        nomi.append((os.path.relpath(p, RADICE).replace(chr(92), "/"),
                     len(lotto[k:k + PER_LOTTO])))
    print("=" * 96)
    print("FASE 2, PUNTO 2: I LOTTI DELLA CLASSIFICAZIONE PER CONTENUTO")
    print("=" * 96)
    print("  da classificare (non segnaposto): %d" % len(res))
    for k in ("R1", "R2", "R4", "R5"):
        print("    %-4s %3d" % (k, n[k]))
    print("  DECISE DA UNA REGOLA: %d   ->   DA LEGGERE: %d"
          % (len(lotto), len(res) - len(lotto)))
    print()
    for p, q in nomi:
        print("  %-44s %d voci" % (p, q))
    return 0


if __name__ == "__main__":
    sys.exit(main())
