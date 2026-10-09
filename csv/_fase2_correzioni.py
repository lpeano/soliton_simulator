# -*- coding: utf-8 -*-
"""FASE 2, PUNTO 1: LE CORREZIONI — il lotto, con un motivo che CITA per ciascuna.

`(a)` i ### **segnaposto** prendono la classe ### **`NON_DEFINITA`** *(schema `3`)*: un
      segnaposto ### **non e' un difetto.**
`(b)` le ### **`51` voci `TEORIA`**: la classe viene dal ### **`tipo_era1`**, che e' un campo
      ### **dichiarato** -- `TEORIA` era il ### **vecchio STATO `teoria`** trasportato come
      ### **classe**, ed e' il difetto della migrazione.
`(c)` gli ### **assiomi e i principi**: `FISICA` o `METODO` secondo la proposta del guardiano,
      con ### **`nota_guardiano` «da confermare da Luca»**.
`(d)` la divisione ### **`METODO`/`INFRASTRUTTURA`** della lista `1`, corretta.

Gira con:  python csv/_fase2_correzioni.py            *(scrive il lotto)*
           python csv/indice.py aggiorna-lotto doc/indice/_lotti/correzioni.jsonl
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
LOTTI = os.path.join(D, "_lotti")
DATA = "2026-10-09"

# ---------------------------------------------- `(c)` gli assiomi e i principi
C_FISICA = ("A1", "A2", "A3", "A3c", "A4", "A5", "A6", "A7", "A7b", "A10", "A11", "A13",
            "A14", "A15", "P-DECADIMENTO", "P-MEMORIA")
C_METODO = ("A8", "A8b", "A9", "A12")
# ---------------------------------------------- `(d)` da INFRASTRUTTURA a METODO
D_METODO = {
    "C21": "parla della VALIDITA' di una misura, non del codice come strumento",
    "MASSA-ID": "l'identita' di una massa e' cio' che rende una misura confrontabile",
    "CONTA-RIGHE": "un conteggio sbagliato falsa un NUMERO DI REFERTO",
    "PIATTAFORMA-NON-TIMBRATA": "senza la piattaforma un numero non ha provenienza",
    "CONFIG-1": "la configurazione dichiarata e' la premessa di ogni misura (`P5`)",
    "ANCORE-1": "un'ancora non unica fa una sostituzione che NON si asserisce (`P1-quater`)",
    "COLLAUDO-NON-ESEGUITO": "un collaudo che non gira non prova niente",
    "IMPL-2": "riguarda se una misura dice cio' che si crede",
    "H-ETC-2": "e' il principio causale di `A6`, non un dettaglio di hook",
}
# ---------------------------------------------- `(b)` i cinque nominati dal mandato
B_SPECIALI = {
    "K2a": ("CRITERIO", "METODO", "OSSERVABILE-P1"),
    "K2b": ("CRITERIO", "METODO", "OSSERVABILE-P1"),
    "T3a": ("CRITERIO", "METODO", "DRIVER-SCENA-II"),
    "T3b": ("CRITERIO", "METODO", "DRIVER-SCENA-II"),
    "M0a": ("DIFETTO", "INFRASTRUTTURA", ""),
}
# ### `(b)` LE ALTRE 46 `TEORIA`: la classe dal `tipo_era1` DICHIARATO, e il dominio dal
# ### tipo. ### ⛔ **NESSUNA parola chiave: `tipo_era1` e' un CAMPO.**
CLASSE_DA_TIPO = {"assioma": "STANDARD", "presidio": "PRESIDIO", "standard": "STANDARD",
                  "criterio-locale": "CRITERIO", "fronte": "FRONTE"}
DOMINIO_DA_TIPO = {"presidio": "METODO", "standard": "METODO", "criterio-locale": "METODO"}


def main():
    os.makedirs(LOTTI, exist_ok=True)
    voci = {v["id"]: v for v in (json.loads(r) for r in
                                 io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8")
                                 if r.strip())}
    lotto = []

    def agg(idv, campi=None, meta=None, motivo=""):
        assert idv in voci, "`%s` non e' una voce" % idv
        lotto.append({"id": idv, "campi": campi or {}, "meta": meta or {},
                      "motivo": motivo, "quando": DATA})

    # ============================================== `(a)` I SEGNAPOSTO
    seg = [v for v in voci.values() if "MAI definito in un registro" in v["titolo"]]
    # ### ⛔ **UNA ECCEZIONE, e il validatore l'ha presa: `ESENTE-P3`.** E' un segnaposto PER
    # ### TITOLO, ma ### **la LISTA 1 DI LUCA lo ha fatto una voce vera** *(`METODO`, era
    # ### `ENTRAMBE`, stato dall'era `1`)*. ### ➜ **UNA DECISIONE DICHIARATA BATTE IL
    # ### TITOLO**, quindi NON prende `NON_DEFINITA`: i segnaposto sono `234` per titolo e
    # ### ### **`233` da classificare**, ed e' il numero che il mandato anticipava.
    fuori = [v["id"] for v in seg if v["stato"] != "DA_CLASSIFICARE"]
    seg = [v for v in seg if v["stato"] == "DA_CLASSIFICARE"]
    print("  ### segnaposto per titolo: %d; ESCLUSI perche' una LISTA li ha decisi: %s"
          % (len(seg) + len(fuori), " ".join(fuori) or "nessuno"))
    for v in sorted(seg, key=lambda x: x["id"]):
        agg(v["id"], {"classe": "NON_DEFINITA"},
            motivo=("(a) il titolo dice <<%s>>: un ID citato e non definito NON E' UN "
                    "DIFETTO, e la classe DIFETTO della migrazione era sbagliata"
                    % v["titolo"][:60]))

    # ============================================== `(b)` LE 51 `TEORIA`
    teo = [v for v in voci.values() if v["classe"] == "TEORIA"]
    for v in sorted(teo, key=lambda x: x["id"]):
        i, m = v["id"], (v["meta"] or {})
        tipo = m.get("tipo_era1", "")
        if i in B_SPECIALI:
            cl, dom, padre = B_SPECIALI[i]
            campi = {"classe": cl, "dominio": dom, "era": "ENTRAMBE"}
            if padre:
                campi["padre"] = padre
            agg(i, campi,
                motivo=("(b) la fonte e' <<%s>>: %s. E la classe TEORIA veniva dal VECCHIO "
                        "STATO `teoria`, non dal contenuto"
                        % (v["fonte"][:64],
                           ("e' il CRITERIO di un sigillo, quindi METODO, col padre `%s`"
                            % padre) if padre else
                           "e' un difetto del DRIVER, cioe' INFRASTRUTTURA")))
            continue
        cl = CLASSE_DA_TIPO.get(tipo)
        if not cl:
            continue
        campi = {"classe": cl}
        if tipo in DOMINIO_DA_TIPO:
            campi["dominio"] = DOMINIO_DA_TIPO[tipo]
            campi["era"] = "ENTRAMBE"
        agg(i, campi,
            motivo=("(b) `tipo_era1` = `%s` e fonte <<%s>>: la classe viene dal TIPO "
                    "DICHIARATO. TEORIA era il vecchio STATO `teoria` trasportato come "
                    "classe, ed e' un difetto della migrazione"
                    % (tipo, v["fonte"][:60])))

    # ============================================== `(c)` ASSIOMI E PRINCIPI
    for i in C_FISICA + C_METODO:
        dom = "FISICA" if i in C_FISICA else "METODO"
        v = voci[i]
        agg(i, {"dominio": dom, "era": "ENTRAMBE"},
            {"nota_guardiano": ("(c) %s: da confermare da Luca -- %s"
                                % (dom, "vincola la FORMA DELLE LEGGI o descrive il "
                                        "comportamento del sistema" if dom == "FISICA"
                                   else "parla di COME SI LAVORA e si verifica"))},
            motivo=("(c) proposta del guardiano, DA CONFERMARE: `%s` -> %s, perche' la fonte "
                    "<<%s>> %s" % (i, dom, v["fonte"][:60],
                                   "vincola la forma delle leggi" if dom == "FISICA"
                                   else "parla di come si lavora")))

    # ============================================== `(d)` INFRASTRUTTURA -> METODO
    for i, perche in sorted(D_METODO.items()):
        v = voci[i]
        agg(i, {"dominio": "METODO"},
            {"nota_guardiano": "(d) da INFRASTRUTTURA a METODO: %s" % perche},
            motivo=("(d) correzione della lista 1: `%s` %s. La fonte e' <<%s>>"
                    % (i, perche, v["fonte"][:60])))

    p = os.path.join(LOTTI, "correzioni.jsonl")
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in lotto) + NL)
    print("=" * 96)
    print("FASE 2, PUNTO 1: IL LOTTO DELLE CORREZIONI")
    print("=" * 96)
    print("  (a) segnaposto -> classe NON_DEFINITA:            %d"
          % sum(1 for x in lotto if x["motivo"].startswith("(a)")))
    print("  (b) TEORIA -> la classe dal `tipo_era1`:           %d"
          % sum(1 for x in lotto if x["motivo"].startswith("(b)")))
    print("  (c) assiomi e principi, FISICA o METODO:           %d"
          % sum(1 for x in lotto if x["motivo"].startswith("(c)")))
    print("  (d) da INFRASTRUTTURA a METODO:                    %d"
          % sum(1 for x in lotto if x["motivo"].startswith("(d)")))
    print("  IN TUTTO: %d voci" % len(lotto))
    print("  scritto %s" % p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
