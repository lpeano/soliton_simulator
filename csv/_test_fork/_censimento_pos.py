# -*- coding: utf-8 -*-
"""IL CENSIMENTO DI `pos` -- **chi legge il DISEGNO** *(`A17`)*.

### ⛔ **IL PUNTO:** `A17` dice che ### **nelle formule della fisica non ci deve essere `pos`**.
Questo strumento ### **non lo assume: lo MISURA**, per forma e non per nome.

**IL METODO, dichiarato prima dei risultati:**

1. si cercano, nell'AST del simulatore, ### **tutte le LETTURE** di `self.pos` *(e di tutto
   cio' che la presuppone: `cKDTree`, `np.linalg.norm` su differenze di `pos`, un centro di
   massa pesato su `pos`)*, con la ### **riga**;
2. per ogni ### **legge** della tavola di `doc/TRADUZIONE_IN_H.md` si parte dalla sua
   ### **funzione d'ancora** e si ### **chiude il grafo delle chiamate**: la legge
   «legge `pos`» se `pos` compare ### **in una qualunque funzione raggiunta**;
3. si distingue ### **DIRETTO** *(la funzione stessa legge `pos`)* da ### **INDIRETTO**
   *(lo legge una funzione che chiama)*, perche' sono due difetti diversi;
4. si guarda anche il ### **PROTOTIPO**, che `A17` dichiara violato da subito.

### ⚠ **CIO' CHE NON VEDE:** un alias *(`p = self.pos`)* passato ad altra funzione. Il
censimento e' ### **per DIFETTO**, come quello delle leggi.

Gira con:  python csv/_test_fork/_censimento_pos.py
"""
import ast
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(os.path.dirname(_QUI))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)
import _cli_flag                                             # noqa: E402

# ### ⚠ **L'ESENZIONE E' DECADUTA, e lo dichiaro:** dal 2026-10-08 questo strumento
# ### CARICA il modulo passando dall'argv del DRIVER, perche' deve dire se una guardia e'
# ### ACCESA -- e <<una violazione dietro un flag spento non e' viva>>. Quindi dichiara la
# ### configurazione INTERA come ogni misura (`P5`), e NON e' piu' esente.
SIM = os.path.join(RADICE, "soliton_simulator.py")
PROTO = os.path.join(RADICE, "proto_primo_ordine", "proto.py")
FUORI = os.path.join(_QUI, "_censimento_pos")
NL = chr(10)
P = []

# ### LE LEGGI, con la loro ancora: gli STESSI nomi della tavola di doc/TRADUZIONE_IN_H.md
LEGGI = [
    ("la coppia d'interferenza, ramo SCALARE", "_coppia_interferenza"),
    ("il legame elastico delle lunghezze", "step"),
    ("la repulsione", "decidi_divisione"),
    ("il rilassamento della torsione", "step"),
    ("il rilassamento della lunghezza di riposo", "step"),
    ("il rilassamento della pressione di equilibrio", "step"),
    ("la precessione dello spinore e l'orologio", "_passo_spinoriale"),
    ("la memoria hebbiana del moto", "memoria_hebbiana_moto"),
    ("la dinamica dei pesi e delle distanze", "step"),
    ("la mitosi", "mitosi"),
    ("la creazione di coppia (Schwinger)", "mitosi"),
    ("la creazione degli archi", "_allaccia"),
    ("la scomparsa degli archi", "step"),
    ("la sincronizzazione", "step"),
    ("la coppia d'interferenza del DRIVER", "_coppia_interferenza"),
    ("il termostato", "step"),
    ("lo scuotimento del vuoto", "scuoti_vuoto"),
    ("il freno `_smorza`", "_smorza"),
    ("lo smorzamento anisotropo", "step"),
    ("la massa critica", "massa_critica_adattiva"),
]

# ### le forme che PRESUPPONGONO `pos`, anche senza nominarla
PRESUPPONGONO = ("cKDTree", "KDTree", "cdist", "distance_matrix", "ConvexHull")

# ### I TRE GRUPPI *(classificazione chiesta da Luca, 2026-10-08)*. ### ⚠ **E' un GIUDIZIO
# ### MIO sul RUOLO della funzione, non una misura**, e si dichiara: l'appartenenza si legge
# ### dal nome e dal contesto, non da un test.
RENDERING = ("update", "_render_vista_rete_sola", "rilassa_disegno", "campo_spaziale")
DIAGNOSTICA = ("batch_condensazione", "_diag_completa", "_ordine", "_gusci_esterni",
               "_regione_centrale", "_picchi_nuovi", "classifica_topologia")
INIZIALI = ("semina", "_semina_lam", "_semina_masse_coerenti", "_celle_vive")
NASCITA = ("_rn_sch_pos", "_rn_div_pos")


def gruppo(nome):
    if nome in RENDERING:
        return "RENDERING"
    if nome in DIAGNOSTICA:
        return "DIAGNOSTICA"
    if nome in INIZIALI:
        return "CONDIZIONI INIZIALI"
    if nome in NASCITA:
        return "EREDITA' ALLA NASCITA"
    return "LEGGE FISICA"


def stampa(s=""):
    P.append(s)
    print(s, flush=True)


def riga(c="-", n=104):
    stampa(c * n)


def funzioni_di(sorgente):
    albero = ast.parse(sorgente)
    f = {}
    for n in ast.walk(albero):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            f.setdefault(n.name, n)
    return albero, f


def guardie_di(nodo, bersaglio):
    """### ⚠ **LA GUARDIA DI UNA LETTURA, e serve perche' senza di essa la misura MENTE:**
    `step` e' UNA funzione lunghissima, quindi ### **ogni legge ancorata a `step` risulta
    <<DIRETTO>> sulle STESSE righe** -- che e' un'attribuzione falsa. Qui si risale agli `if`
    che racchiudono la riga e si prendono i ### **flag di modulo** che li governano.
    """
    fuori = {}

    def cammina(n, pila):
        for c in ast.iter_child_nodes(n):
            p2 = pila
            if isinstance(n, ast.If) and c in (n.body + n.orelse):
                nomi = [x.id for x in ast.walk(n.test)
                        if isinstance(x, ast.Name) and x.id.isupper()]
                p2 = pila + nomi
            ln = getattr(c, "lineno", None)
            if ln in bersaglio:
                fuori.setdefault(ln, [])
                for k in p2:
                    if k not in fuori[ln]:
                        fuori[ln].append(k)
            cammina(c, p2)

    cammina(nodo, [])
    return fuori


def legge_pos(nodo):
    """### Le LETTURE di `pos` dentro `nodo`, per FORMA: `self.pos`, `net.pos`, `.pos[`,
    piu' le forme che la PRESUPPONGONO."""
    fuori = []
    for n in ast.walk(nodo):
        if isinstance(n, ast.Attribute) and n.attr == "pos":
            # ### si esclude il bersaglio di un assegnamento: quella e' una SCRITTURA
            fuori.append(("pos", n.lineno))
        elif isinstance(n, ast.Name) and n.id in PRESUPPONGONO:
            fuori.append((n.id, n.lineno))
        elif isinstance(n, ast.Attribute) and n.attr in PRESUPPONGONO:
            fuori.append((n.attr, n.lineno))
    return fuori


def chiamate(nodo):
    f = set()
    for n in ast.walk(nodo):
        if isinstance(n, ast.Call):
            x = n.func
            if isinstance(x, ast.Attribute):
                f.add(x.attr)
            elif isinstance(x, ast.Name):
                f.add(x.id)
    return f


def chiusura(funzioni, radice):
    visti, coda = set(), [radice]
    while coda:
        k = coda.pop()
        if k in visti or k not in funzioni:
            continue
        visti.add(k)
        for c in chiamate(funzioni[k]):
            if c in funzioni and c not in visti:
                coda.append(c)
    return visti


def main():
    os.makedirs(FUORI, exist_ok=True)
    # ### ⛔ **LO STATO DEI FLAG SI LEGGE DAL DRIVER, non dai default del modulo:** una
    # ### violazione dietro un flag ### **spento** non e' viva. Si passa da
    # ### `_cli_flag.argv_del_driver()`, che esegue il TESTO del driver fino a
    # ### `S._applica_flag(a)` e CATTURA la sys.argv che il driver ha costruito.
    import contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        S, argv_driver = _cli_flag.argv_del_driver()
    sorgente = io.open(SIM, encoding="utf-8").read()
    albero, funz = funzioni_di(sorgente)
    riga("=")
    stampa("IL CENSIMENTO DI `pos` -- chi legge il DISEGNO (A17)")
    riga("=")
    stampa("  sorgente: %d righe, %d funzioni" % (len(sorgente.split(NL)), len(funz)))
    _cli_flag.dichiara_configurazione(S, stampa)

    # ---------------------------------------------- tutte le letture, per funzione
    per_funzione = {}
    guardie = {}
    for nome, nodo in funz.items():
        L = legge_pos(nodo)
        if L:
            per_funzione[nome] = sorted(set(L))
            guardie[nome] = guardie_di(nodo, set(b for _, b in L))
    tot = sum(len(v) for v in per_funzione.values())
    stampa("  FUNZIONI che leggono `pos` o una forma che la presuppone: %d  (%d occorrenze)"
           % (len(per_funzione), tot))
    stampa()
    for k in sorted(per_funzione, key=lambda x: -len(per_funzione[x])):
        v = per_funzione[k]
        quali = sorted(set(a for a, _ in v))
        gg = sorted(set(x for L in guardie.get(k, {}).values() for x in L))
        stampa("    %-30s %2d occorr.  righe %s  [%s]  guardie: %s"
               % (k, len(v), ",".join(str(b) for _, b in v[:5]), ",".join(quali),
                  ",".join(gg) if gg else "(nessuna)"))

    # ---------------------------------------------- LE GUARDIE, CON LO STATO NEL DRIVER
    riga("=")
    stampa("LE GUARDIE DELLA TAVOLA `pos`, CON LO STATO NEL DRIVER")
    stampa("### <<Una violazione dietro un flag SPENTO non e' viva>>")
    riga("=")
    tutte = sorted(set(x for L in guardie.values() for g in L.values() for x in g))
    stato_g = {}
    for k in tutte:
        v = getattr(S, k, "(assente)")
        acceso = bool(v) if v != "(assente)" else None
        stato_g[k] = {"valore": v, "acceso": acceso,
                      "nell_argv": ("--" + k.lower().replace("_", "-")) in argv_driver}
        stampa("  %-18s valore EFFETTIVO %-8s -> %s   %s"
               % (k, repr(v), "### ACCESO" if acceso else "spento",
                  "(passato nell'argv)" if stato_g[k]["nell_argv"] else ""))

    # ---------------------------------------------- LA GRAVITA' E `pozzo_grafo`
    riga("=")
    stampa("LA GRAVITA' LEGGE `pos`? -- `pozzo_grafo` e la cura `POZZO_D` (D02)")
    riga("=")
    _pd = getattr(S, "POZZO_D", None)
    _gb = getattr(S, "GRAV_BIFASE", None)
    pozzo = {"POZZO_D_effettivo": _pd, "GRAV_BIFASE_effettivo": _gb,
             "pozzo_d_nell_argv": "--pozzo-d" in argv_driver,
             "righe_pos_in_pozzo_grafo": [b for _, b in
                                          per_funzione.get("pozzo_grafo", [])]}
    stampa("  `pozzo_grafo` legge `pos` alle righe: %s"
           % (",".join(str(b) for b in pozzo["righe_pos_in_pozzo_grafo"]) or "(nessuna)"))
    stampa("  `GRAV_BIFASE` effettivo: %r   `POZZO_D` effettivo: %r" % (_gb, _pd))
    stampa("  `--pozzo-d` nell'argv del driver: %s" % pozzo["pozzo_d_nell_argv"])
    if _pd:
        stampa("  ### -> LA VIOLAZIONE **NON E' VIVA**: `POZZO_D` e' ACCESO nel driver, quindi")
        stampa("  ###    `L` viene da `self.d` e NON da `|pos_j - pos_i|`. ### LA CURA (D02)")
        stampa("  ###    E' GIA' ATTIVA.")
    else:
        stampa("  ### -> LA VIOLAZIONE E' VIVA: `POZZO_D` e' SPENTO, quindi `L` viene da `pos`.")
    pozzo["viva"] = not bool(_pd)

    # ---------------------------------------------- I TRE GRUPPI
    riga("=")
    stampa("LA CLASSIFICAZIONE IN TRE GRUPPI (chiesta da Luca) -- e il quarto che ho trovato")
    riga("=")
    per_gruppo = {}
    for k in per_funzione:
        per_gruppo.setdefault(gruppo(k), []).append(k)
    for gg in ("LEGGE FISICA", "RENDERING", "DIAGNOSTICA", "CONDIZIONI INIZIALI",
               "EREDITA' ALLA NASCITA"):
        L = sorted(per_gruppo.get(gg, []))
        stampa("  %-22s %2d  %s" % (gg, len(L), " ".join(L)))

    # ---------------------------------------------- per LEGGE
    riga("=")
    stampa("PER LEGGE: la legge <<legge pos>>? -- chiudendo il grafo dalla sua ANCORA")
    riga("=")
    esiti = []
    for nome, anc in LEGGI:
        if anc not in funz:
            esiti.append({"legge": nome, "ancora": anc, "stato": "ANCORA NON TROVATA"})
            stampa("  %-44s  ancora `%s` NON TROVATA" % (nome, anc))
            continue
        diretto = per_funzione.get(anc, [])
        rag = chiusura(funz, anc)
        indiretti = {k: per_funzione[k] for k in rag if k in per_funzione and k != anc}
        if diretto:
            stato = "DIRETTO"
        elif indiretti:
            stato = "INDIRETTO"
        else:
            stato = "no"
        gd = guardie.get(anc, {})
        esiti.append({"legge": nome, "ancora": anc, "stato": stato,
                      "guardie_dirette": sorted(set(x for L in gd.values() for x in L)),
                      "righe_dirette": [b for _, b in diretto],
                      "vie_indirette": {k: [b for _, b in v]
                                        for k, v in sorted(indiretti.items())},
                      "funzioni_raggiunte": len(rag)})
        via = ("righe %s" % ",".join(str(b) for _, b in diretto[:4])) if diretto else (
            "via %s" % ",".join(sorted(indiretti)[:3]) if indiretti else "-")
        gg = sorted(set(x for L in gd.values() for x in L)) if diretto else []
        stampa("  %-44s  %-10s  %-26s  guardie: %s"
               % (nome, stato, via, ",".join(gg) if gg else "-"))

    # ---------------------------------------------- il PROTOTIPO
    riga("=")
    stampa("IL PROTOTIPO -- A17 lo dichiara violato da subito: si CONTROLLA")
    riga("=")
    sp = io.open(PROTO, encoding="utf-8").read()
    _a, fp = funzioni_di(sp)
    rp = {}
    for nome, nodo in fp.items():
        L = []
        for n in ast.walk(nodo):
            if isinstance(n, ast.Attribute) and n.attr in ("pos",):
                L.append(("pos", n.lineno))
            elif isinstance(n, ast.Name) and n.id in ("pos", "x"):
                L.append((n.id, n.lineno))
        if L:
            rp[nome] = sorted(set(L))
    stampa("  funzioni del prototipo che usano `pos`: %d  -- %s"
           % (len(rp), " ".join(sorted(rp))))
    eucl = [(i + 1, r.strip()) for i, r in enumerate(sp.split(NL))
            if "norm(" in r and ("pos" in r or "x[" in r)]
    stampa("  righe con una NORMA su posizioni (distanza euclidea): %d" % len(eucl))
    for ln, r in eucl[:6]:
        stampa("      riga %4d: %s" % (ln, r[:84]))

    d = {"per_funzione": {k: [[a, b] for a, b in v] for k, v in per_funzione.items()},
         "gruppi": {k: sorted(v) for k, v in per_gruppo.items()},
         "stato_guardie": stato_g, "pozzo": pozzo, "argv_driver": list(argv_driver),
         "per_legge": esiti,
         "prototipo": {"funzioni": {k: [[a, b] for a, b in v] for k, v in rp.items()},
                       "righe_euclidee": [[ln, r] for ln, r in eucl]}}
    io.open(os.path.join(FUORI, "pos.json"), "w", encoding="utf-8").write(
        json.dumps(d, ensure_ascii=False, default=str))
    io.open(os.path.join(FUORI, "pos.txt"), "w", encoding="utf-8").write(NL.join(P) + NL)
    stampa()
    stampa("scritto %s" % os.path.join(FUORI, "pos.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
