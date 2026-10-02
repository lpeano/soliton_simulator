# -*- coding: utf-8 -*-
"""**IL SETACCIO DELLE DERIVAZIONI: quale frase afferma un BILANCIO che nessuno ha misurato?**

Nasce da un rilievo del guardiano *(2026-10-03)* su ### **una frase mia, falsa**, nella
regola `_rn_div_tw`:

> *<<i due tronconi nascono senza torsione: la torsione dell'arco e' stata ### **SCIOLTA**
> dalla divisione, ed e' cio' che ### **il calcio ha SPESO**>>*

### ⛔ **E' FALSA.** Il calcio ### **USA `|tw|`** come misura di quanto colpire, ma
### **NON trasferisce l'avvolgimento**: `DIVISIONE-AUTOCONSISTENTE:M1` ha misurato
### **~1.2 giri persi per arco diviso, senza bilancio.** La frase ### **dava per risolta
una domanda aperta** — ed e' la forma d'errore piu' insidiosa in questo repo, perche'
### **una derivazione si legge come un fatto.**

## CHE COSA FA QUESTO STRUMENTO, e che cosa NON fa

| | |
|---|---|
| **fa** | scorre ### **tutte** le derivazioni di `REGOLE_NASCITA` *(e le loro `classe`)* e segnala ogni frase che contiene una parola del ### **VOCABOLARIO DICHIARATO** di bilancio/conservazione |
| ### **NON fa** | ### **non decide se la frase e' vera.** Quello e' un ### **giudizio**, e lo scrivo io nel referto accanto a ogni segnalazione — con la ragione |

### \U0001f4cc **L'ELENCO NON LO SCELGO IO, il giudizio SI** — ed e' la divisione giusta:
un elenco scelto a mano e' la forma `FALSO-ZERO`; un giudizio nascosto dentro uno script
e' peggio, perche' sembra una misura.

**COMANDO:** `python csv/_test_fork/_setaccio_derivazioni.py`
**USCITA:** `csv/_test_fork/_setaccio_derivazioni/` — `_setaccio.json` + `_corsa.txt`.
"""
import hashlib
import io
import json
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_QUI, ".."))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, RADICE)
SIM = os.path.join(RADICE, "soliton_simulator.py")
FUORI = os.path.join(_QUI, "_setaccio_derivazioni")
NL = chr(10)

# ### IL VOCABOLARIO E' DICHIARATO QUI, e si legge come parte del criterio.
#   Due famiglie, perche' affermano cose diverse:
VOCABOLARIO = {
    "conservazione": ("conserva", "conservazione", "conservata", "conservano", "neutra",
                      "invariante", "si mantiene"),
    "bilancio": ("bilancio", "speso", "spende", "spesa", "trasferisc", "pareggio",
                 "cede", "scambia", "drena", "paga", "compensa", "sottrae",
                 "sciolta", "sciolto", "SCIOLTA"),
}
# le parole che, se presenti, dicono che la frase E' GIA' un rilievo o una misura:
# non la assolvono, ma cambiano la lettura, e il referto lo riporta.
MARCATORI = ("MISURATO", "misurato", "RILIEVO", "DICHIARATA", "dichiarata", "aperta",
             "APERTA", "domanda", "NON MISURATO")


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def principato():
    righe = []

    def stampa(*x):
        s = " ".join(str(y) for y in x)
        righe.append(s)
        print(s)

    import soliton_simulator as S
    b = blob(SIM)
    stampa("=" * 100)
    stampa("IL SETACCIO DELLE DERIVAZIONI -- quale frase afferma un BILANCIO non misurato?")
    stampa("=" * 100)
    stampa("  simulatore .. %s (sha1 byte grezzi)" % b[:8])
    stampa("  regole ...... %d  (%d grandezze x %d eventi convertiti)"
           % (len(S.REGOLE_NASCITA), len(S.ORDINE_DI_NASCITA), len(S.EVENTI_CONVERTITI)))
    stampa("  ### IL VOCABOLARIO E' DICHIARATO, e si legge come parte del criterio:")
    for fam, par in sorted(VOCABOLARIO.items()):
        stampa("      %-16s %s" % (fam, ", ".join(par)))
    stampa("")
    stampa("  ### E LO STRUMENTO NON DECIDE SE LA FRASE E' VERA: elenca. Il GIUDIZIO e' mio,")
    stampa("      e sta nel referto accanto a ogni segnalazione, con la ragione.")
    stampa("")

    segnalate = []
    for (ev, nome), v in sorted(S.REGOLE_NASCITA.items()):
        testo = "%s || %s" % (v["classe"], v["derivazione"])
        colpi = {}
        for fam, par in VOCABOLARIO.items():
            # ### IL CONFINE DI PAROLA, e lo ha chiesto il referto dello strumento stesso:
            #   al primo giro `cede` ha preso ### **pre-CEDE** (<<`METRI` precede `STATO`>>),
            #   cioe' ha segnalato una frase che parla di ORDINE DELLE SCRITTURE come se
            #   parlasse di un trasferimento di torsione. ### Un falso positivo in uno
            #   strumento che serve a trovare frasi false e' particolarmente brutto.
            #   ### `\b` davanti: i PREFISSI VOLUTI (`trasferisc`) continuano a prendere.
            # ### E IL PRIMO TENTATIVO DI QUESTA CURA HA DATO *ZERO SEGNALATE*,
            #   ed era l'OTTAVO falso zero (`FALSO-ZERO`): nel patch avevo scritto
            #   l'escape direttamente, e si e' MANGIATO -- il file conteneva `r""`,
            #   cioe' una regex SENZA confine di parola che non prendeva niente.
            #   ### E' ESATTAMENTE CIO' CHE `P1-quater` VIETA, con QUESTO escape
            #   citato come esempio: *nei patch script niente escape, si usa
            #   `chr()` o `replace`*. Ora e' `chr(92)`.
            trovate = sorted({p for p in par
                              if re.search(r"\b" + re.escape(p), testo, re.IGNORECASE)})
            if trovate:
                colpi[fam] = trovate
        if not colpi:
            continue
        marc = sorted({m for m in MARCATORI if m in testo})
        segnalate.append({"evento": ev, "grandezza": nome, "colpi": colpi,
                          "marcatori": marc, "classe": v["classe"],
                          "derivazione": v["derivazione"]})
    stampa("-" * 100)
    stampa("### SEGNALATE: %d regole su %d" % (len(segnalate), len(S.REGOLE_NASCITA)))
    stampa("")
    for s in segnalate:
        stampa("  ### `%s` / `%s`" % (s["evento"], s["grandezza"]))
        stampa("      parole ...... %s"
               % "; ".join("%s: %s" % (k, ",".join(v)) for k, v in sorted(s["colpi"].items())))
        stampa("      marcatori ... %s" % (", ".join(s["marcatori"]) or "### NESSUNO"))
        for pezzo in re.findall(r".{1,96}(?:\s|$)", s["derivazione"]):
            if pezzo.strip():
                stampa("      | %s" % pezzo.strip())
        stampa("")

    d = {"blob_sim_sha1_byte": b, "vocabolario": VOCABOLARIO, "marcatori": list(MARCATORI),
         "regole_totali": len(S.REGOLE_NASCITA), "segnalate": segnalate,
         "NON_E_UN_VERDETTO": ("lo strumento ELENCA; il giudizio su ciascuna frase e' nel "
                               "referto di chi legge, non qui")}
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    io.open(os.path.join(FUORI, "_setaccio.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(d, indent=1, ensure_ascii=False, default=str))
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(righe) + NL)
    print("  referto .. %s" % FUORI)


if __name__ == "__main__":
    principato()
