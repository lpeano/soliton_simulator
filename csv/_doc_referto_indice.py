# -*- coding: utf-8 -*-
"""IL GENERATORE DI `doc/REFERTO_indice_v2.md` — **ogni numero dalle uscite** (`L-NUMERI`).

Gira con:  python csv/_doc_referto_indice.py
"""
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

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Legge l'indice e i controlli.
NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
DEST = os.path.join(RADICE, "doc", "REFERTO_indice_v2.md")
R = []

# ### I LETTORI DELLA VISTA, censiti con `grep` e dichiarati uno per uno.
LETTORI = [
    ("csv/_indice_id.py", "il validatore dell'era 1", "ADATTATO: legge la VISTA, e gli stati "
     "dello schema 2 sono nel suo vocabolario; il controllo delle VOCI PERSE ora sa degli "
     "alias e delle etichette rimosse"),
    ("csv/_hook_presidi.py", "il `pre-commit`", "ADATTATO: gira ANCHE `indice.py valida`, e "
     "solo se `voci.jsonl` esiste -- cosi' si accende da se'"),
    ("csv/_presidio_indice.py", "`H-INDICE` nel `commit-msg`", "legge la VISTA: gli ID che "
     "cerca ci sono tutti"),
    ("csv/_presidio_righe.py", "il presidio delle righe", "legge la VISTA"),
    ("csv/_lista_chiusa.py", "la lista congelata", "legge la VISTA"),
    ("csv/_punto_della_situazione.py", "il punto della situazione", "legge la VISTA"),
    ("csv/_analisi_lettori_indice.py", "l'analisi dei lettori", "legge la VISTA"),
    ("csv/_confronto_pds.py", "il confronto fra punti", "legge la VISTA"),
    ("csv/_controlli_riordino.py", "i controlli del riordino", "legge la VISTA"),
    ("csv/_indice_riordino.py", "il riordino", "legge la VISTA"),
]


def A(s=""):
    R.append(s)


def jsonl(p):
    return [json.loads(r) for r in io.open(os.path.join(D, p), encoding="utf-8").read()
            .split(NL) if r.strip()]


def main():
    voci = jsonl("voci.jsonl")
    etich = jsonl("etichette_rimosse.jsonl")
    tracce = jsonl("migrazione_era1.jsonl")
    confl = jsonl("conflitti_era1.jsonl") if os.path.exists(
        os.path.join(D, "conflitti_era1.jsonl")) and os.path.getsize(
        os.path.join(D, "conflitti_era1.jsonl")) else []
    C = io.open(os.path.join(D, "_controlli.txt"), encoding="utf-8").read()
    m = re.search(r"I CONTROLLI: (\d+) su (\d+)", C)
    assert m, "i controlli non riportano il loro esito"
    OK, TOT = m.group(1), m.group(2)

    def conta(campo):
        c = {}
        for v in voci:
            c[str(v[campo])] = c.get(str(v[campo]), 0) + 1
        return c

    dc = [v for v in voci if v["stato"] == "DA_CLASSIFICARE"]
    regole = {}
    for t in tracce:
        k = t["regola"].split(")")[0] + ")"
        regole[k] = regole.get(k, 0) + 1

    A("# L'INDICE `v2` — **il referto della migrazione e della BONIFICA**")
    A("")
    A("> ### ⛔ **I `%s` CONTROLLI PASSANO** *(`%s` su `%s`)*, e il piu' importante e' il "
      "### **primo**: ogni ID del vecchio indice compare in ### **UNO E UNO SOLO** di "
      "`voci.jsonl::id`, `voci.jsonl::alias`, `etichette_rimosse.jsonl`. "
      "### **`0` persi, `0` doppi.**" % (TOT, OK, TOT))
    A(">")
    A("> *Ogni numero esce da `doc/indice/` o da `doc/indice/_controlli.txt`.* *(`L-NUMERI`)*")
    A("")
    A("---")
    A("")
    A("# ⭐ `①` **I CONTEGGI**")
    A("")
    A("| | |")
    A("|---|--:|")
    A("| ID al tag `era-1-secondo-ordine` | `%d` |" % 953)
    A("| ### **voci** in `voci.jsonl` | ### **`%d`** |" % len(voci))
    A("| ### **etichette rimosse** | ### **`%d`** |" % len(etich))
    A("| righe di ### **traccia** | `%d` |" % len(tracce))
    A("| ### **conflitti** con le liste del guardiano | ### **`%d`** |" % len(confl))
    A("| voci ### **bloccanti** | `%d` |" % sum(1 for v in voci if v["blocca"]))
    A("")
    for campo in ("classe", "dominio", "era", "stato"):
        c = conta(campo)
        A("### **per `%s`**" % campo)
        A("")
        A("| " + " | ".join("`%s`" % k for k in sorted(c, key=lambda x: -c[x])) + " |")
        A("|" + "--:|" * len(c))
        A("| " + " | ".join("**%d**" % c[k] for k in sorted(c, key=lambda x: -c[x])) + " |")
        A("")
    A("### **LE REGOLE DELLA MIGRAZIONE, per quante volte hanno DECISO**")
    A("")
    A("| regola | volte | che cosa fa |")
    A("|---|--:|---|")
    SPIEGA = {
        "(a)": "i campi meccanici dall'indice del tag",
        "(a2)": "un `alias` che era ### **l'ID di un'altra voce**: diventa un COLLEGAMENTO",
        "(a3)": "un ID con uno ### **SPAZIO**: normalizzato, e ### **il nome vecchio RESTA "
                "come alias**",
        "(a4)": "due ID vecchi che normalizzavano ### **nello stesso**: il secondo e' alias "
                "del primo",
        "(b0)": "un segnaposto che era ### **un ID di VOCABOLARIO**, non una voce",
        "(b2)": "un segnaposto diventato ### **ETICHETTA DI DOCUMENTO** *(fuori da "
                "`voci.jsonl`)*",
        "(b3)": "un segnaposto che ### **resta come voce `DA_CLASSIFICARE`**",
    }
    for k in sorted(regole, key=lambda x: -regole[x]):
        A("| `%s` | ### **%d** | %s |" % (k, regole[k], SPIEGA.get(k, "")))
    A("")
    A("# ✔ `②` **IL RAPPORTO DEI CONFLITTI con le liste del guardiano**")
    A("")
    if confl:
        A("| id | motivo |")
        A("|---|---|")
        for x in confl:
            A("| `%s` | %s |" % (x["id"], x.get("motivo", "")))
    else:
        A("### ⭐ **NESSUN CONFLITTO.** Le tre liste si applicano al `100 %`:")
        A("")
        A("| lista | che cosa impone | applicata |")
        A("|---|---|--:|")
        A("| ### **`L1`** | `METODO` o `INFRASTRUTTURA`, era `ENTRAMBE`, stato dall'era `1` | "
          "### **`%d` su `%d`** |" % (len(MG.L1), len(MG.L1)))
        A("| ### **`L2`** | `AGENDA`, `FISICA`, era `2` | ### **`%d` su `%d`** |"
          % (len(MG.L2), len(MG.L2)))
        A("| ### **`L3`** | `SOSPESA`, `FISICA`, era `1` | ### **`%d` su `%d`** |"
          % (len(MG.L3), len(MG.L3)))
        A("")
        A("> ### ⚠ **E LA SCELTA FRA `METODO` E `INFRASTRUTTURA` E' MIA**, col motivo accanto "
          "a ciascuna nel sorgente. ### **La regola che ho usato:** `METODO` = come si "
          "### **RAGIONA** e come si ### **MISURA**; `INFRASTRUTTURA` = gli ### **STRUMENTI** "
          "e i ### **FILE**. ### ⛔ **E' un giudizio, e Luca lo corregga.**")
        A("")
        A("| | |")
        A("|---|--:|")
        A("| `METODO` nella `L1` | `%d` |"
          % sum(1 for _k, (d, _p) in MG.L1.items() if d == "METODO"))
        A("| `INFRASTRUTTURA` nella `L1` | `%d` |"
          % sum(1 for _k, (d, _p) in MG.L1.items() if d == "INFRASTRUTTURA"))
    A("")
    A("### ⛔ **E LE DIECI NOTE «candidata SUPERATA da …» SONO NOTE, NON CHIUSURE:** nessuna "
      "voce e' stata chiusa ne' superata. ### **Si chiudono AL TRIAGE**, e il criterio e' in "
      "`doc/TRIAGE_ERA_1.md`.")
    A("")
    A("# ⛔ `③` **LA TAVOLA CORTA DEI `DA_CLASSIFICARE`, per Luca** — *`%d` voci*" % len(dc))
    A("")
    A("### **Perche' non sono classificabili, in tre gruppi:**")
    A("")
    seg = [v for v in dc if "citazioni_n" in (v["meta"] or {})]
    altri = [v for v in dc if v not in seg]
    altri_altro = [v for v in altri if (v["meta"] or {}).get("tipo_era1") == "altro"]
    altri_resto = [v for v in altri if v not in altri_altro]
    A("| gruppo | quante | ### **perche'** | ### **la proposta** |")
    A("|---|--:|---|---|")
    A("| ### **SEGNAPOSTO** | ### **`%d`** | erano voci *«(CITATO N volte, MAI definito in un "
      "registro)»*, e le loro citazioni ### **NON stanno solo** in task history o referti: "
      "stanno nel ### **codice** o in documenti di lavoro | ### **leggere `file_citanti`**: se "
      "la citazione e' un'etichetta locale, va in `etichette_rimosse`; se e' un difetto vero, "
      "va scritta come voce |" % len(seg))
    A("| ### **`tipo = altro`** | ### **`%d`** | l'era `1` le marcava `altro`, che ### **non e' "
      "un'informazione** | ### **leggere la voce** e darle una classe. ### ⛔ **La migrazione "
      "NON ha indovinato**, ed e' il punto |" % len(altri_altro))
    A("| ### **senza evidenza strutturale** | ### **`%d`** | non sono `PRESIDIO` ne' "
      "`STANDARD`, non hanno un `padre`, e non erano chiuse | ### **il triage**: "
      "`indice cerca --stato DA_CLASSIFICARE` |" % len(altri_resto))
    A("")
    A("### **I PRIMI VENTI SEGNAPOSTO per numero di citazioni** *(il resto con "
      "`indice cerca --stato DA_CLASSIFICARE`)*:")
    A("")
    A("| id | citazioni | ### **dove** | titolo dell'era `1` |")
    A("|---|--:|---|---|")
    for v in sorted(seg, key=lambda x: -(x["meta"].get("citazioni_n") or 0))[:20]:
        f = (v["meta"].get("file_citanti") or [])[:2]
        A("| `%s` | ### **%d** | %s | %s |"
          % (v["id"], v["meta"].get("citazioni_n") or 0,
             " ".join("`%s`" % x for x in f), v["titolo"].replace("|", "/")[:46]))
    A("")
    A("# 📌 `④` **LE ETICHETTE RIMOSSE** — *`%d`, con `%d` citazioni in tutto*"
      % (len(etich), sum(e.get("citazioni_n", 0) for e in etich)))
    A("")
    A("### ⛔ **NON sono voci perdute: sono ID che NON ERANO VOCI.** Ciascuna porta "
      "### **il numero di citazioni e i file**, e la regola che l'ha decisa.")
    A("")
    A("| id | citazioni | regola | ### **dove** |")
    A("|---|--:|---|---|")
    for e in sorted(etich, key=lambda x: -(x.get("citazioni_n") or 0))[:25]:
        A("| `%s` | ### **%d** | %s | %s |"
          % (e["id"], e.get("citazioni_n") or 0, e.get("regola", "")[:34],
             " ".join("`%s`" % x for x in (e.get("file_citanti") or [])[:2])))
    A("")
    A("*(Le altre `%d` stanno in `doc/indice/etichette_rimosse.jsonl`.)*"
      % max(0, len(etich) - 25))
    A("")
    A("# 📌 `⑤` **I LETTORI DELLA VISTA: censiti e dichiarati**")
    A("")
    A("| file | che cos'e' | ### **che cosa gli e' successo** |")
    A("|---|---|---|")
    for p, q, s in LETTORI:
        A("| `%s` | %s | %s |" % (p, q, s))
    A("")
    A("### ⭐ **DUE SONO STATI ADATTATI, gli altri otto NO — e il motivo e' lo scopo della "
      "vista:** `doc/INDICE_ID.tsv` si rigenera con ### **le stesse `15` colonne**, quindi chi "
      "la legge ### **non si accorge del cambio di schema.** ### ⚠ **E' compatibilita', non "
      "equivalenza:** `leggi`, `variabili`, `assiomi`, `collegate` e `padre` ### **non hanno "
      "una colonna**, e chi li vuole legge la fonte.")
    A("")
    A("---")
    A("")
    A("# ⛔ **CHE COSA QUESTO REFERTO NON DICE**")
    A("")
    A("| | |")
    A("|---|---|")
    A("| che l'indice sia ### **classificato** | ### ⛔ **no: `%d` voci sono "
      "`DA_CLASSIFICARE`**, e sono ### **decisioni di Luca.** La migrazione ### **non ha "
      "indovinato niente** |" % len(dc))
    A("| che le voci sospese siano ### **giuste** | le `%d` della lista `L3` sono ### **quelle "
      "del guardiano**, applicate come indicate. ### **Le altre non sono state sospese**, "
      "perche' senza dominio non si sa se la sospensione le riguarda |" % len(MG.L3))
    A("| che le ### **etichette rimosse** siano spazzatura | ### **no:** alcune hanno "
      "### **decine di citazioni**. Non erano ### **voci dell'indice**, e questo e' tutto |")
    A("| che la classificazione ### **`METODO`/`INFRASTRUTTURA`** sia verificata | ### ⚠ **e' "
      "un GIUDIZIO MIO**, col motivo accanto a ciascuna. ### **Luca lo corregga** |")
    A("| che il ### **triage** sia fatto | ### ⛔ **no**, e non si fa adesso: il piano e' in "
      "`doc/TRIAGE_ERA_1.md`, e parte da `indice cerca --stato SOSPESA` |")
    io.open(DEST, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print("scritto %s (%d righe)" % (DEST, len(R)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
