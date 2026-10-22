# -*- coding: utf-8 -*-
r"""**LA RACCOLTA SU `cs` E `Lambda_c`: la ricerca DICHIARATA del task history, ripetibile.**

> ### ⛔ **Il task history e' `2026-10-22_raccolta_cs.md`** *(il metodo: le parole, i sei luoghi, come si conta)*. ### **Lo script cerca e conta:
> NON decide niente** *(il documento e' `doc/RACCOLTA_CS.md`)*.

Gira con:  python csv/_raccolta_cs.py
"""
import glob
import io
import json
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)

PAROLE = re.compile(r"(?<![A-Za-z_])cs(?![A-Za-z_])|Lambda_c|LAMBDA-C|CAMM-FASE-VUOTO|cs_al_centro|accendi_cs|(?<![A-Z])CS(?=-)",
                    re.I)
REFERTI = re.compile(r"cs|lambda_c|fase_vuoto|strada_d", re.I)
JSONL = os.path.join(RADICE, "doc", "referti_l2", "raccolta_cs.jsonl")


def leggi(p):
    return io.open(os.path.join(RADICE, p), encoding="utf-8").read()


def main(argv):
    del argv
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 100)
    print("LA RACCOLTA SU cs E Lambda_c (il metodo del task history 2026-10-22_raccolta_cs.md)")
    print("=" * 100)
    out = {}
    # ---------------------------------------------------------------- A. le voci
    V = [json.loads(r) for r in leggi("doc/indice/voci.jsonl").splitlines() if r.strip()]
    A = [v for v in V if PAROLE.search(v["id"] + " " + v["titolo"]) or "CAMM-FASE-VUOTO" in v.get("leggi", [])]
    ida = {v["id"] for v in A}
    Ad = [v for v in V if v["id"] not in ida and PAROLE.search(v.get("descrizione", ""))]
    print("### A. LE VOCI: %d per ID, titolo o leggi; %d SOLO nella descrizione" % (len(A), len(Ad)))
    for era in ("2", "ENTRAMBE", "1", "DA_CLASSIFICARE"):
        sel = sorted([v for v in A if v["era"] == era], key=lambda v: v["id"])
        if not sel:
            continue
        print("  -- era %s: %d" % (era, len(sel)))
        for v in sel:
            cr = v.get("creata", {})
            print("  %-48s %-10s %-9s creata %s %s | %s" % (v["id"], v["classe"], v["stato"], cr.get("data", ""),
                                                           cr.get("commit", "")[:8], v["titolo"]))
    print("  -- solo nella descrizione (gli ID): %s" % ", ".join(sorted(v["id"] for v in Ad)))
    out["voci"] = [{"id": v["id"], "classe": v["classe"], "era": v["era"], "stato": v["stato"], "titolo": v["titolo"],
                    "creata": v.get("creata", {}), "aggiornata": v.get("aggiornata", {}), "fonte": v.get("fonte", ""),
                    "descrizione": v.get("descrizione", ""), "chiusura": v.get("chiusura", {}),
                    "superata_da": v.get("superata_da", "")} for v in A]
    out["voci_solo_descrizione"] = sorted(v["id"] for v in Ad)
    # ---------------------------------------------------------------- B. i nodi
    t = leggi("doc/ALBERO_era2.yaml")
    blocchi = re.split(r"\n  - id: ", t)[1:]
    B = [b.split("\n", 1)[0].strip() for b in blocchi if PAROLE.search(b)]
    print("### B. I NODI DI DECISIONE: %d su %d -- %s" % (len(B), len(blocchi), ", ".join(B)))
    out["nodi"] = B
    # ---------------------------------------------------------------- C. la mappa
    m = leggi("doc/MAPPA_DIPENDENZE.md").split("\n")
    C = [(i + 1, l.strip()) for i, l in enumerate(m) if l.startswith("#") and PAROLE.search(l)]
    print("### C. LE SEZIONI DELLA MAPPA: %d" % len(C))
    for i, l in C:
        print("  riga %4d  %s" % (i, l[:150]))
    out["mappa"] = C
    # ---------------------------------------------------------------- D. i task history
    D = []
    for f in sorted(glob.glob(os.path.join(RADICE, "doc", "TASK_HISTORY", "*.md"))):
        s = io.open(f, encoding="utf-8").read()
        if PAROLE.search(s.split("\n", 1)[0] + " " + s[:3000]):
            D.append((os.path.basename(f), s.split("\n", 1)[0][:140]))
    print("### D. I TASK HISTORY: %d" % len(D))
    for f, tit in D:
        print("  %-52s %s" % (f, tit))
    out["task_history"] = D
    # ---------------------------------------------------------------- E. i referti
    E = sorted(os.path.basename(f) for f in glob.glob(os.path.join(RADICE, "doc", "referti_l2", "*.txt"))
               if REFERTI.search(os.path.basename(f)))
    print("### E. I REFERTI (per nome): %d -- %s" % (len(E), ", ".join(E)))
    out["referti"] = E
    # ---------------------------------------------------------------- F. le leggi
    L = leggi("primo_ordine/leggi/leggi.yaml")
    F = sorted(set(re.findall(r"- id: (\S+)", L)))
    citano = [i for i in F if i != "CAMM-FASE-VUOTO"
              and "CAMM-FASE-VUOTO" in L.split("- id: " + i, 1)[1].split("\n  - id: ", 1)[0]]
    print("### F. LE LEGGI: CAMM-FASE-VUOTO in tabella? %s; le leggi la cui scheda la cita: %s"
          % ("CAMM-FASE-VUOTO" in F, ", ".join(citano) or "nessuna"))
    out["leggi"] = {"fase_vuoto": "CAMM-FASE-VUOTO" in F, "citano": citano}
    io.open(JSONL, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False) + "\n")
    print("=" * 100)
    print("LA RACCOLTA: A %d (+%d solo descrizione), B %d, C %d, D %d, E %d" % (len(A), len(Ad), len(B), len(C), len(D),
                                                                             len(E)))
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
