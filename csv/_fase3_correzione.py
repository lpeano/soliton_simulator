# -*- coding: utf-8 -*-
"""INDICE `v3`: LA CORREZIONE DOPO LA VERIFICA DEL GUARDIANO.

### ⛔ **E' una CORREZIONE CHIESTA**, quindi ### **le liste del guardiano si aggiornano di
conseguenza** -- non sono un vincolo da difendere.

| blocco | che cosa |
|---|---|
| `A` | la ### **lista `2`** *(errore del guardiano)*: `14` voci da `era 2/AGENDA` a `FISICA/1/SOSPESA`, piu' `RISCRITTURA-GO`, `AUDIT-CURE`, `LOSCHMIDT-ECO`; e `5` ### **NON si toccano** |
| `B` | le ### **GEMELLE e i fuori posto**, piu' `D13`/`Z11` *(lo stesso fatto)* |
| `C` | le ### **etichette rimosse PER SBAGLIO**, e ### **la regola corretta**: una ### **riga di tabella** o un'### **intestazione** che definisce l'ID ### **E' UNA DEFINIZIONE** |

Gira con:  python csv/_fase3_correzione.py <A|B|C>
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

# ==========================================================================
#   BLOCCO A -- la lista 2 del guardiano era sbagliata
# ==========================================================================
A_FISICA = ("CARICA-ROTAZIONE", "CARICA-SIMMETRIA-FASE", "CARICA-DI-GAUGE",
            "CARICA-PERCORSO", "D03", "D15", "D35", "D38", "FASE-TRASCINAMENTO-3D",
            "MEM-HEBB-PIANO-XY", "SCHW-SOTTO-LAM", "SCHWINGER-UN-NODO",
            "TETTO-CAUSALE-TEMPO-COORDINATO", "Y1")
A_ALTRO = {
    "RISCRITTURA-GO": ("INFRASTRUTTURA", "ENTRAMBE", "APERTA"),
    "AUDIT-CURE": ("METODO", "ENTRAMBE", "APERTA"),
    "LOSCHMIDT-ECO": ("METODO", "ENTRAMBE", "APERTA"),
}
A_NON_TOCCARE = ("M-LEGAMI", "M-ISTERESI", "MEM-VERSO", "M-FLUSSO", "M-MASSA")

# ==========================================================================
#   BLOCCO B
# ==========================================================================
B_METODO = ("Z31", "Z100", "Z11", "C28", "Z20", "Z86", "Z145", "CHI-TORS-ZERO-FALSO",
            "H-ETC-1", "REGISTRO_FISICA:A5", "REGISTRO_FISICA:U2-6", "COMPONENTI:S2",
            "COMPONENTI:S3")
B_DOC = ("CENS-A6", "CENS-A7", "SMP-APRI-COMMENTO", "MITOSI-2LAM-ACCESO")
B_INFRA = ("C25", "PERC-TW-MORTA")
B_FISICA = ("TRATTI-INTERNI", "CHK2", "CHK3", "CHK3-D", "E3", "B7")

# ==========================================================================
#   BLOCCO C -- le etichette da ripristinare
# ==========================================================================
C_RIPRISTINA = {}
for _k in range(1, 7):
    C_RIPRISTINA["TS-%d" % _k] = ("CRITERIO", "METODO", "1", "SOSPESA",
                                  "doc/LETTURA_accensione_e_torsione.md")
    C_RIPRISTINA["TW-%d" % _k] = ("CRITERIO", "METODO", "1", "SOSPESA",
                                  "doc/SCALE_TW_lettura.md")
C_RIPRISTINA["O4"] = ("FRONTE", "FISICA", "1", "SOSPESA",
                      "doc/IPOTESI_gravita_a_spinta.md")
C_RIPRISTINA["SHAKE-THEN-FREEZE"] = ("MISURA", "FISICA", "1", "CHIUSA",
                                     "STATO_CLAUDE_fork-su2.md")
# ### ⛔ **GLI OMONIMI: NON SI SCEGLIE.** Due definizioni, due oggetti diversi, lo stesso ID.
C_OMONIMI = {
    "D5": ["doc/CENSIMENTO_intenzioni.md:315 -- `:936` (`SYNC_UPDATE`) e le sue motivazioni "
           "sparse nei documenti",
           "doc/MAPPA_accoppiamenti_spin.md:70 -- `omega_s`, `- omega_src/_tau`: IL POZZO"],
    "D6": ["doc/CENSIMENTO_intenzioni.md:316 -- `Checkpoint.md` nel suo insieme (~640 "
           "righe), ~40 voci [TODO]/[IN VERIFICA]",
           "doc/MAPPA_accoppiamenti_spin.md:71 -- `calcio_omega` in `semina()`: punto zero "
           "ALLA NASCITA, non per passo"],
}


# ==========================================================================
#   LA REGOLA CORRETTA: che cos'e' una DEFINIZIONE
# ==========================================================================
def e_definito(idv, percorso):
    """### ⛔ **LA REGOLA CHE AVEVO SBAGLIATO.** La fase `2` diceva: *se tutte le citazioni
    stanno in documenti, e' un'etichetta*. ### **FALSO:** un documento e' ### **esattamente
    il posto in cui un ID si DEFINISCE.**

    ### ✔ **Una DEFINIZIONE e':**
      * una ### **RIGA DI TABELLA** che apre con l'ID -- `| **` + backtick + `ID` + ... + `|`;
      * un'### **INTESTAZIONE** *(`#`, `##`, `###`)* che contiene l'ID.
    ### ⚠ **Una citazione nel corpo del testo NON e' una definizione**, ed e' la distinzione
    che mancava.
    """
    p = os.path.join(RADICE, percorso)
    if not os.path.exists(p):
        return None
    q = re.escape(idv)
    riga_tab = re.compile(r"^\s*\|\s*\**\s*`?" + q + r"`?\s*\**\s*\|")
    intest = re.compile(r"^#{1,6}\s.*(?<![A-Za-z0-9_:-])" + q + r"(?![A-Za-z0-9_:-])")
    for n, r in enumerate(io.open(p, encoding="utf-8", errors="replace").read().split(NL),
                          1):
        if riga_tab.match(r):
            return ("riga di tabella", percorso, n, " ".join(r.split())[:150])
        if intest.match(r):
            return ("intestazione", percorso, n, " ".join(r.split())[:150])
    return None


def cit(s, q=90):
    return " ".join((s or "").split())[:q]


def carica():
    voci = [json.loads(r) for r in io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8")
            if r.strip()]
    et = [json.loads(r) for r in
          io.open(os.path.join(D, "etichette_rimosse.jsonl"), encoding="utf-8") if r.strip()]
    return voci, et


def scrivi_lotto(nome, lotto):
    os.makedirs(LOTTI, exist_ok=True)
    p = os.path.join(LOTTI, nome)
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in lotto) + NL)
    print("  scritto %s: %d voci" % (os.path.relpath(p, RADICE).replace(chr(92), "/"),
                                     len(lotto)))


def blocco_a():
    voci, _et = carica()
    per = {v["id"]: v for v in voci}
    lotto = []
    for i in A_FISICA:
        v = per[i]
        lotto.append({"id": i, "quando": DATA,
                      "campi": {"dominio": "FISICA", "era": "1", "stato": "SOSPESA"},
                      "meta": {"nota_guardiano": "difetto del codice dell'era 1; lezione "
                                                 "per l'era 2"},
                      "motivo": ("(A) CORREZIONE CHIESTA: la lista 2 del guardiano la dava "
                                 "era 2/AGENDA, ed e' un ERRORE SUO. Il testo dice <<%s>>: "
                                 "e' un DIFETTO DEL CODICE DELL'ERA 1, e la sua lezione "
                                 "passa all'era 2" % cit(v["descrizione"] or v["titolo"]))})
    for i, (dom, era, st) in sorted(A_ALTRO.items()):
        v = per[i]
        lotto.append({"id": i, "quando": DATA,
                      "campi": {"dominio": dom, "era": era, "stato": st},
                      "meta": {"nota_guardiano": "correzione della lista 2 del guardiano: "
                                                 "%s/%s" % (dom, era)},
                      "motivo": ("(A) CORREZIONE CHIESTA: da era 2/AGENDA a %s/%s/%s. Il "
                                 "testo dice <<%s>>" % (dom, era, st,
                                                        cit(v["descrizione"]
                                                            or v["titolo"])))})
    for i in A_NON_TOCCARE:
        v = per[i]
        lotto.append({"id": i, "quando": DATA, "campi": {},
                      "meta": {"nota_guardiano": "da decidere da Luca: era 1 o 2"},
                      "motivo": ("(A) NON SI TOCCA, per mandato: resta `%s`/era `%s`/`%s`, e "
                                 "la nota dice che l'era la decide Luca. Il testo dice <<%s>>"
                                 % (v["dominio"], v["era"], v["stato"],
                                    cit(v["descrizione"] or v["titolo"], 70)))})
    scrivi_lotto("v3_A.jsonl", lotto)
    print("  (A) %d a FISICA/1/SOSPESA, %d riclassificate, %d NON toccate (solo la nota)"
          % (len(A_FISICA), len(A_ALTRO), len(A_NON_TOCCARE)))


def blocco_b():
    voci, _et = carica()
    per = {v["id"]: v for v in voci}
    lotto = []

    def agg(i, dom, era, stato=None, nota=None, perche=""):
        """### ⚠ **DUE REGOLE DI STATO DIVERSE, e il mandato le distingue:**
          * le ### **GEMELLE** vanno a `METODO/ENTRAMBE` con *<<lo stato attuale ### **se
            CHIUSA**, altrimenti ### **APERTA**>>*  ->  `stato="SE_CHIUSA"`;
          * `DOCUMENTAZIONE` e `INFRASTRUTTURA` vanno *<<era `1`, ### **stato attuale**>>*
            ->  `stato=None`, e ### **lo stato NON si tocca**.
        ### ⛔ **Avevo scritto la prima regola per tutte**, e avrebbe portato `5` voci da
        `SOSPESA` ad `APERTA` ### **senza che il mandato lo chieda.**
        """
        v = per[i]
        st = v["stato"] if stato is None else (
            ("CHIUSA" if v["stato"] == "CHIUSA" else "APERTA") if stato == "SE_CHIUSA"
            else stato)
        campi = {"dominio": dom, "era": era, "stato": st}
        lotto.append({"id": i, "quando": DATA, "campi": campi,
                      "meta": ({"nota_guardiano": nota} if nota else {}),
                      "motivo": ("(B) CORREZIONE CHIESTA: `%s` -> %s/era %s/%s. %sIl testo "
                                 "dice <<%s>>" % (i, dom, era, st,
                                                  (perche + ". ") if perche else "",
                                                  cit(v["descrizione"] or v["titolo"])))})
    for i in B_METODO:
        agg(i, "METODO", "ENTRAMBE", "SE_CHIUSA")
    for i in B_DOC:
        agg(i, "DOCUMENTAZIONE", "1")
    for i in B_INFRA:
        agg(i, "INFRASTRUTTURA", "1")
    for i in B_FISICA:
        agg(i, "FISICA", "1", "SOSPESA")
    # ---------------------------------------------- `D13` e `Z11`: LO STESSO FATTO
    # ### ⛔ **`superata_da` NON si puo' usare:** lo schema vuole ### **un id di DECISIONE o
    # ### di ASSIOMA**, non di un'altra voce. ### ➜ **Si ALLINEA LO STATO e si COLLEGA**, e
    # ### si allinea ### **su APERTA**, perche' il testo di `Z11` dice <<lavoro PREVISTO, NON
    # ### ANCORA FATTO>>: il fatto NON e' chiuso.
    for a, b in (("D13", "Z11"), ("Z11", "D13")):
        v = per[a]
        lotto = [x for x in lotto if x["id"] != a]
        lotto.append({"id": a, "quando": DATA,
                      "campi": {"dominio": "METODO", "era": "ENTRAMBE", "stato": "APERTA",
                                "collegate": sorted(set(v["collegate"] + [b])),
                                "chiusura": {}},
                      "meta": {"nota_guardiano":
                               "`D13` e `Z11` sono LO STESSO FATTO (i sigilli storici non "
                               "rigirati): stato ALLINEATO su APERTA, perche' Z11 dice "
                               "<<lavoro PREVISTO, non ancora fatto>>. Collegate, NON "
                               "superate: `superata_da` vuole una DECISIONE o un ASSIOMA"},
                      "motivo": ("(B) `D13` e `Z11` sono LO STESSO FATTO: `D13` dice <<I "
                                 "sigilli storici non sono stati rigirati sul blob corrente "
                                 "| Z11>> e `Z11` dice <<RIGIRO DEI SIGILLI STORICI -- "
                                 "lavoro PREVISTO, non ancora fatto>>. ALLINEO SU APERTA "
                                 "perche' il lavoro NON e' fatto, e le COLLEGO: "
                                 "`superata_da` non si puo' usare, vuole una decisione o un "
                                 "assioma")})
    scrivi_lotto("v3_B.jsonl", lotto)
    print("  (B) %d METODO, %d DOCUMENTAZIONE, %d INFRASTRUTTURA, %d FISICA, piu' D13/Z11"
          % (len(B_METODO), len(B_DOC), len(B_INFRA), len(B_FISICA)))


def blocco_c():
    """### Il RIPASSO delle 53 etichette con la REGOLA CORRETTA."""
    voci, et = carica()
    per = {v["id"]: v for v in voci}
    nuove = [e for e in et if str(e.get("regola", "")).startswith("(fase2")]
    print("  le etichette della fase 2 da ripassare: %d" % len(nuove))
    definite, restano = [], []
    for e in nuove:
        trovata = None
        for f in (e.get("file_citanti") or []):
            trovata = e_definito(e["id"], f)
            if trovata:
                break
        (definite if trovata else restano).append((e, trovata))
    print("  -> DEFINITE da una riga di tabella o da un'intestazione: %d" % len(definite))
    print("  -> restano etichette:                                   %d" % len(restano))
    d = {"definite": [{"id": e["id"], "come": t[0], "file": t[1], "riga": t[2],
                       "testo": t[3]} for e, t in definite],
         "restano": [{"id": e["id"], "citazioni_n": e.get("citazioni_n"),
                      "file_citanti": e.get("file_citanti")} for e, _t in restano]}
    io.open(os.path.join(D, "_ripasso_etichette.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(d, ensure_ascii=False, indent=1))
    print("  scritto doc/indice/_ripasso_etichette.json")
    for x in d["definite"]:
        print("      %-20s %-16s %s:%d" % (x["id"], x["come"], x["file"].split("/")[-1],
                                           x["riga"]))
    return d


def main(argv):
    assert argv and argv[0] in ("A", "B", "C"), __doc__
    {"A": blocco_a, "B": blocco_b, "C": blocco_c}[argv[0]]()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
