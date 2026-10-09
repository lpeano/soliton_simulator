# -*- coding: utf-8 -*-
"""IL BLOCCO `G`: i tre residui della verifica del guardiano.

| | che cosa |
|---|---|
| `G1` | `5` voci che ### **verificano flag dell'era `1`** vanno a `METODO/1/SOSPESA`, come `TS-*` e `TW-*`. ### ⛔ **L'errore era nel prompt del guardiano** *(«altrimenti `APERTA`»)*, ### **e io l'ho applicato alla lettera** |
| `G2` | la voce `G1` — *«`Ldisegno/d` per arco»* — e' ### **una misura sull'era `1`**: `FISICA/1/SOSPESA`. Era un'### **omissione del guardiano dal blocco `A`** |
| `G3` | `8` note `nota_guardiano` ### **SUPERATE**: dicono *«lista `3` del guardiano: fisica dell'era `1`, sospesa»* su voci che oggi ### **non sono `FISICA`** |

Gira con:  python csv/_fase3_residui.py
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

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Costruisce un lotto per l'indice.
NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
DATA = "2026-10-09"

# ==========================================================================
#   `G1`  --  verificano FLAG DELL'ERA 1, non sono lavoro di entrambe le ere
# ==========================================================================
G1 = ("REGISTRO_FISICA:A5", "REGISTRO_FISICA:U2-6", "COMPONENTI:S2", "COMPONENTI:S3",
      "H-ETC-1")
NOTA_G1 = ("correzione v3 blocco G1: METODO/era 1/SOSPESA -- verifica un flag dell'era 1, "
           "come TS-* e TW-*. La regola <<altrimenti APERTA>> era un errore del prompt del "
           "guardiano, e io l'ho applicata alla lettera")

# ==========================================================================
#   `G2`  --  una MISURA sull'era 1, dimenticata dal blocco `A`
# ==========================================================================
G2 = "G1"
NOTA_G2 = ("correzione v3 blocco G2: FISICA/era 1/SOSPESA -- <<Ldisegno/d per arco>> e' una "
           "MISURA SULL'ERA 1. Omissione del guardiano dal blocco A, dove le altre 14 voci "
           "della lista 2 sono passate all'era 1")

# ==========================================================================
#   `G3`  --  le note SUPERATE
# ==========================================================================
NOTA_DOC = ("correzione v3 blocco B: DOCUMENTAZIONE/era 1 -- la voce parla di un DOCUMENTO "
            "CHE MENTE sul codice, non di fisica. La nota precedente diceva <<lista 3 del "
            "guardiano: fisica dell'era 1, sospesa>>, ed e' SUPERATA")
G3 = {}
for _i in ("CENS-A6", "CENS-A7", "SMP-APRI-COMMENTO", "MITOSI-2LAM-ACCESO"):
    G3[_i] = NOTA_DOC
for _i in ("H-ETC-1", "REGISTRO_FISICA:A5", "REGISTRO_FISICA:U2-6", "COMPONENTI:S3"):
    G3[_i] = NOTA_G1
# ### ⚠ **`COMPONENTI:S2` NON e' nell'elenco di `G3`**, e il motivo e' che ### **non aveva
# ### alcuna nota da sostituire.** Gliela metto comunque, ### **uguale alle sue quattro
# ### sorelle**: non e' una decisione sulla classificazione *(quella la da' `G1`)*, e' la
# ### stessa frase che spiega perche' sta dov'e'. ### **Lo dichiaro nel commit.**
G3["COMPONENTI:S2"] = NOTA_G1
# ### Una coda che ESISTEVA e che NON si butta: `CENS-A6` portava anche questa.
CODA = {"CENS-A6": " -- candidata SUPERATA dalla decisione sulla sincronizzazione"}


def cit(s, q=90):
    return " ".join((s or "").split())[:q]


def main():
    voci = [json.loads(r) for r in io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8")
            if r.strip()]
    per = {v["id"]: v for v in voci}
    lotto = []
    for i in G1:
        v = per[i]
        lotto.append({"id": i, "quando": DATA,
                      "campi": {"dominio": "METODO", "era": "1", "stato": "SOSPESA"},
                      "meta": {"nota_guardiano": G3[i] + CODA.get(i, "")},
                      "motivo": ("(G1) CORREZIONE CHIESTA: da METODO/ENTRAMBE/APERTA a "
                                 "METODO/era 1/SOSPESA, come TS-* e TW-*. VERIFICA UN FLAG "
                                 "DELL'ERA 1, e il testo dice <<%s>>. La regola "
                                 "<<altrimenti APERTA>> era un errore del prompt del "
                                 "guardiano, E IO L'HO APPLICATA ALLA LETTERA"
                                 % cit(v["titolo"] or v["descrizione"]))})
    v = per[G2]
    lotto.append({"id": G2, "quando": DATA,
                  "campi": {"dominio": "FISICA", "era": "1", "stato": "SOSPESA"},
                  "meta": {"nota_guardiano": NOTA_G2},
                  "motivo": ("(G2) CORREZIONE CHIESTA: da FISICA/era 2/AGENDA a FISICA/era "
                             "1/SOSPESA. E' UNA MISURA SULL'ERA 1, e il testo dice <<%s>>. "
                             "Omissione del guardiano dal blocco A"
                             % cit(v["titolo"] or v["descrizione"]))})
    for i in sorted(G3):
        if i in G1:
            continue                      # ### gia' fatto sopra, nota compresa
        v = per[i]
        vecchia = v["meta"].get("nota_guardiano", "")
        lotto.append({"id": i, "quando": DATA, "campi": {},
                      "meta": {"nota_guardiano": G3[i] + CODA.get(i, "")},
                      "motivo": ("(G3) NOTA SUPERATA: diceva <<%s>>, e la voce oggi e' "
                                 "`%s`/era `%s`/`%s`. Una nota che dice <<fisica dell'era "
                                 "1>> su una voce che NON e' FISICA e' una MESCOLANZA, ed e' "
                                 "esattamente cio' che il presidio F6 segnalera'"
                                 % (cit(vecchia, 80), v["dominio"], v["era"], v["stato"]))})
    p = os.path.join(D, "_lotti", "v3_G.jsonl")
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in lotto) + NL)
    print("  scritto doc/indice/_lotti/v3_G.jsonl: %d voci" % len(lotto))
    print("  (G1) %d a METODO/1/SOSPESA   (G2) 1 a FISICA/1/SOSPESA   (G3) %d note"
          % (len(G1), len(G3)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
