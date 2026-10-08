# -*- coding: utf-8 -*-
"""I CONTROLLI DELLA MIGRAZIONE — **devono passare PRIMA del commit** *(punto `6`)*.

| | il controllo |
|---|---|
| **`C1`** | ### **CONSERVAZIONE:** ogni ID del vecchio indice compare in ### **UNO E UNO SOLO** di: `voci.jsonl::id`, `voci.jsonl::alias`, `etichette_rimosse.jsonl` |
| **`C2`** | `migrazione_era1.jsonl` porta, per ### **ogni** ID vecchio, ### **dove e' andato e per quale REGOLA** |
| **`C3`** | ### **LE LISTE DEL GUARDIANO:** ogni voce ha la classificazione indicata, oppure sta nel rapporto dei ### **conflitti** |
| **`C4`** | ### **IDEMPOTENZA:** la seconda esecuzione produce ### **gli stessi byte** |
| **`C5`** | `python csv/indice.py valida` ### **passa** |
| **`C6`** | la ### **vista TSV compatibile** fa girare `python csv/_indice_id.py --blocca SI` |
| **`C7`** | i ### **CONTEGGI** per classe, dominio, era, stato, e dove sono andati i segnaposto |

Gira con:  python csv/_controlli_indice_v2.py
"""
import hashlib
import io
import json
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)
import migra_indice_v2 as MG                                 # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Controlla una migrazione.
NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
P = []
ESITI = []


def stampa(s=""):
    P.append(s)
    print(s, flush=True)


def riga(c="-", n=104):
    stampa(c * n)


def esito(nome, ok, dettaglio=""):
    ESITI.append((nome, bool(ok), dettaglio))
    stampa("  %-56s %s   %s" % (nome, "PASSA" if ok else "### FALLISCE", dettaglio))


def jsonl(p):
    return [json.loads(r) for r in io.open(p, encoding="utf-8").read().split(NL) if r.strip()]


def sha(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()[:12]


def main():
    vecchie = MG.vecchio_indice()
    voci = jsonl(os.path.join(D, "voci.jsonl"))
    etich = jsonl(os.path.join(D, "etichette_rimosse.jsonl"))
    tracce = jsonl(os.path.join(D, "migrazione_era1.jsonl"))
    confl = jsonl(os.path.join(D, "conflitti_era1.jsonl")) \
        if os.path.exists(os.path.join(D, "conflitti_era1.jsonl")) else []
    riga("=")
    stampa("I CONTROLLI DELLA MIGRAZIONE ALLO SCHEMA 2")
    riga("=")
    stampa("  al tag: %d ID vecchi   ->   voci %d, etichette %d, tracce %d, conflitti %d"
           % (len(vecchie), len(voci), len(etich), len(tracce), len(confl)))
    stampa()

    # ---------------------------------------------- C1 CONSERVAZIONE
    ids = {v["id"] for v in voci}
    alias = {}
    for v in voci:
        for a in v["alias"]:
            alias.setdefault(a, []).append(v["id"])
    etic = {e["id"] for e in etich}
    persi, doppi = [], []
    for i in vecchie:
        dove = [x for x, c in (("id", i in ids), ("alias", i in alias),
                               ("etichetta", i in etic)) if c]
        if not dove:
            persi.append(i)
        elif len(dove) > 1:
            doppi.append((i, dove))
    esito("C1 CONSERVAZIONE: ogni ID vecchio in UNO E UNO SOLO posto",
          not persi and not doppi,
          "persi %d, doppi %d%s" % (len(persi), len(doppi),
                                    ("  " + " ".join(persi[:6])) if persi else ""))

    # ---------------------------------------------- C2 LA TRACCIA
    tracciati = {t["id_vecchio"] for t in tracce}
    senza = sorted(set(vecchie) - tracciati)
    esito("C2 la TRACCIA copre ogni ID vecchio, con la REGOLA",
          not senza and all(t.get("regola") for t in tracce),
          "senza traccia %d%s" % (len(senza), ("  " + " ".join(senza[:6])) if senza else ""))

    # ---------------------------------------------- C3 LE LISTE DEL GUARDIANO
    per = {v["id"]: v for v in voci}
    for v in voci:
        for a in v["alias"]:
            per.setdefault(a, v)
    guai = []
    for idv, (dom, _p) in MG.L1.items():
        v = per.get(idv)
        if v is None or v["dominio"] != dom or str(v["era"]) != "ENTRAMBE":
            guai.append("L1 " + idv)
    for idv in MG.L2:
        v = per.get(idv)
        if v is None or v["dominio"] != "FISICA" or str(v["era"]) != "2" \
                or v["stato"] != "AGENDA":
            guai.append("L2 " + idv)
    for idv in MG.L3:
        v = per.get(idv)
        if v is None or v["dominio"] != "FISICA" or str(v["era"]) != "1" \
                or v["stato"] != "SOSPESA":
            guai.append("L3 " + idv)
    nei_conflitti = {x["id"] for x in confl}
    guai = [g for g in guai if g.split(" ", 1)[1] not in nei_conflitti]
    esito("C3 LE LISTE DEL GUARDIANO: classificazione come indicata",
          not guai, "fuori posto %d%s" % (len(guai),
                                          ("  " + " ".join(guai[:6])) if guai else ""))

    # ---------------------------------------------- C4 IDEMPOTENZA
    files = ["voci.jsonl", "etichette_rimosse.jsonl", "migrazione_era1.jsonl",
             "_indice_meta.json"]
    prima = {f: sha(os.path.join(D, f)) for f in files}
    q = subprocess.run([sys.executable, os.path.join(_QUI, "migra_indice_v2.py")],
                       cwd=RADICE, capture_output=True, text=True)
    dopo = {f: sha(os.path.join(D, f)) for f in files}
    diff = [f for f in files if prima[f] != dopo[f]]
    esito("C4 IDEMPOTENZA: la seconda esecuzione da' gli STESSI BYTE",
          q.returncode == 0 and not diff,
          "diversi: %s" % (" ".join(diff) if diff else "nessuno"))

    # ---------------------------------------------- C5 VALIDA
    q5 = subprocess.run([sys.executable, os.path.join(_QUI, "indice.py"), "valida"],
                        cwd=RADICE, capture_output=True, text=True)
    esito("C5 `indice.py valida` passa", q5.returncode == 0,
          (q5.stdout or "").strip().split(NL)[-1][:60])

    # ---------------------------------------------- C6 LA VISTA COMPATIBILE
    q6 = subprocess.run([sys.executable, os.path.join(_QUI, "_indice_id.py"),
                         "--blocca", "SI"], cwd=RADICE, capture_output=True, text=True)
    m = re.search(r"blocca_run_base `SI`: (\d+) voci su (\d+)", q6.stdout or "")
    esito("C6 la VISTA compatibile fa girare `_indice_id.py --blocca SI`",
          q6.returncode == 0 and bool(m),
          ("%s bloccanti su %s voci" % (m.group(1), m.group(2))) if m
          else (q6.stdout or q6.stderr or "")[:60])

    # ---------------------------------------------- C7 I CONTEGGI
    riga("=")
    stampa("C7 I CONTEGGI")
    riga("=")
    for campo in ("classe", "dominio", "era", "stato"):
        c = {}
        for v in voci:
            c[str(v[campo])] = c.get(str(v[campo]), 0) + 1
        stampa("  %-9s %s" % (campo, "  ".join("%s=%d" % (k, c[k])
                                               for k in sorted(c, key=lambda x: -c[x]))))
    seg = {}
    for t in tracce:
        r = t["regola"].split(")")[0] + ")"
        seg[r] = seg.get(r, 0) + 1
    stampa()
    stampa("  LE REGOLE DELLA MIGRAZIONE, per quante volte hanno deciso:")
    for k in sorted(seg, key=lambda x: -seg[x]):
        stampa("      %-8s %4d" % (k, seg[k]))
    stampa()
    stampa("  bloccanti fra le voci: %d" % sum(1 for v in voci if v["blocca"]))
    stampa("  etichette rimosse: %d, con %d citazioni in tutto"
           % (len(etich), sum(e.get("citazioni_n", 0) for e in etich)))

    riga("=")
    tutti = all(x[1] for x in ESITI)
    stampa("I CONTROLLI: %d su %d   ### %s"
           % (sum(1 for x in ESITI if x[1]), len(ESITI),
              "TUTTI PASSATI" if tutti else "QUALCUNO FALLISCE: NON SI VA AVANTI"))
    io.open(os.path.join(D, "_controlli.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(P) + NL)
    return 0 if tutti else 1


if __name__ == "__main__":
    sys.exit(main())
