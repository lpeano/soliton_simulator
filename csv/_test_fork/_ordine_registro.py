# -*- coding: utf-8 -*-
"""**IN CHE ORDINE SI POSSONO SCRIVERE LE GRANDEZZE DELLA NASCITA?** - la domanda che
lo strumento dello STOP 4 **non** ha misurato.

`csv/_test_fork/_punto_unico_fattibile.py` ha misurato una cosa diversa: se le
scritture della nascita si possono rendere **CONTIGUE**, cioe' se il codice che sta
*fra* loro si puo' spostare fuori. ### **Questo strumento misura se le scritture si
possono PERMUTARE FRA LORO**, che e' la forma che il piano chiede
*(`doc/PIANO_riordino_mitosi.md` par.(c): <<per OGNI voce del registro, **nell'ordine
del registro**>>)*.

### **SONO DUE DOMANDE DIVERSE, e la seconda puo' avere risposta NO con la prima SI.**

## -- E LA PRIMA VERSIONE DI QUESTO STRUMENTO HA DATO UN FALSO ZERO (2026-10-02)

La versione `1fb6ac63` ha risposto ### **<<zero dipendenze, l'ordine del registro e'
raggiungibile>>**. ### **Era falso, ed e' il QUINTO zero di questa forma nella
sessione.** Il motivo: ### **faceva girare l'analisi sul solo `REGISTRO_STATO`** (30
voci), e cosi' ### **escludeva proprio le grandezze piu' intrecciate** -

| grandezza | dove sta | che cosa l'esclusione nascondeva |
|---|---|---|
| `phi`, `i`, `j` | ### **`REGISTRO_METRI`**, non `STATO` | `i`/`j` sono la **topologia**, `phi` la fase che `twp` **legge** |
| `_peqn_idx` | ### **in NESSUN registro** | il suo commento al sorgente ### **DICHIARA** la dipendenza: *<<la marca va QUI, DOPO il `concatenate`: gli indici si riferiscono all'array FINALE>>* |

### **LA CURA: nessun insieme scelto a mano.** Si prendono **TUTTE** le scritture del
perimetro, si costruisce il **grafo delle dipendenze**, e l'ordine della tabella deve
essere ### **un ordine TOPOLOGICO di quel grafo.** I contatori non leggono e non sono
letti: ### **escono da se'**, senza che io li debba classificare.

## IL CRITERIO, ed e' quello di un compilatore

Due scritture `W_p` *(prima nel sorgente)* e `W_q` *(dopo)* **NON si possono invertire**
se c'e' una dipendenza:

| | |
|---|---|
| **flusso** | `W_q` **legge** cio' che `W_p` **scrive** => invertirle fa leggere a `W_q` il valore VECCHIO |
| **anti** | `W_p` **legge** cio' che `W_q` **scrive** => invertirle fa leggere a `W_p` il valore NUOVO |

- **L'autolettura NON e' un vincolo fra due scritture:** `self.phi =
  concatenate([self.phi, fm])` legge se stessa.
- ### **E OGNI ARCO SI CLASSIFICA, perche' un arco conservativo non e' un ostacolo:**
  un arco e' ### **GENUINO** solo se la lettura puo' davvero cambiare valore. Se la
  scrittura letta e' una ### **PURA ESTENSIONE** *(`concatenate([x, nuovo])`, che non
  tocca i primi `n0` elementi)* e la lettura e' ### **sui GENITORI** *(indici `< n0`)*,
  allora ### **l'ordine NON cambia il valore** - e l'arco e' **inerte**. E' lo stesso
  criterio di `e_pura_estensione` nello strumento dello STOP 4.
- **E LE CHIAMATE CON EFFETTO NON SONO REGOLE:** `_nasce`, `_smp_chirurgia`, `_grado`
  scrivono o contano, ma non sono *<<la regola di nascita di una grandezza>>*. Si
  elencano a parte: vanno collocate **a mano e dichiarate**.
"""
import ast
import hashlib
import io
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SIM = os.path.join(RADICE, "soliton_simulator.py")
# le funzioni che oggi scrivono le grandezze della nascita: `mitosi` piu' i due
# `_eredita_*` che il commit 3 ASSORBE (par.(c): <<i due `_eredita_*` SPARISCONO>>).
ASSORBITE = ("_eredita_psi_figli", "_eredita_spinore_figli")
SERVIZIO = ("_nasce", "_smp_chirurgia", "_grado", "_traccia_d0", "_rho_sorgente")
# letture che NON sono stato: funzioni pure, o il generatore (che si conta altrove).
PURE = ("_wphi", "_dphi", "rng")
# i nomi che nel sorgente indicano i GENITORI, cioe' indici `< n0`.
GENITORI = ("a", "b", "aa", "bb", "g", "src", "kk", "gk", "pick")


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def registri_dal_sorgente(albero):
    """Tutti i `REGISTRO_*`, in ordine di dichiarazione, col loro contenuto."""
    fuori = {}
    for n in ast.walk(albero):
        if (isinstance(n, ast.Assign) and len(n.targets) == 1
                and isinstance(n.targets[0], ast.Name)
                and n.targets[0].id.startswith("REGISTRO")):
            nomi = []
            if isinstance(n.value, (ast.Tuple, ast.List)):
                for e in n.value.elts:
                    if (isinstance(e, (ast.Tuple, ast.List)) and e.elts
                            and isinstance(e.elts[0], ast.Constant)):
                        nomi.append(e.elts[0].value)
                    elif isinstance(e, ast.Constant):
                        nomi.append(e.value)
            fuori[n.targets[0].id] = nomi
    return fuori


def letture(nodo):
    """Le letture `self.<attr>` nel nodo, ognuna con GLI INDICI con cui e' letta.

    Restituisce `{attr: set(sorgente_dell_indice)}`; l'indice `""` significa
    *letta INTERA* (nessun `[...]`), che e' il caso piu' vincolante.
    """
    fuori = {}
    for n in ast.walk(nodo):
        if (isinstance(n, ast.Attribute) and isinstance(n.ctx, ast.Load)
                and isinstance(n.value, ast.Name) and n.value.id == "self"):
            if n.attr in PURE or n.attr in SERVIZIO or n.attr in ASSORBITE:
                continue
            fuori.setdefault(n.attr, set())
    # un secondo giro per gli indici: `self.x[IDX]`
    for n in ast.walk(nodo):
        if isinstance(n, ast.Subscript):
            base = n.value
            if (isinstance(base, ast.Attribute) and isinstance(base.ctx, ast.Load)
                    and isinstance(base.value, ast.Name) and base.value.id == "self"
                    and base.attr in fuori):
                fuori[base.attr].add(ast.unparse(n.slice))
    for k in fuori:
        if not fuori[k]:
            fuori[k].add("")        # letta INTERA
    return fuori


def pura_estensione(nodo):
    """La scrittura e' una PURA ESTENSIONE: `concatenate([self.x, nuovo])` / `vstack`.

    Cioe' il primo pezzo e' `self.x` **intero**, senza filtro: i primi `n0`
    elementi restano dov'erano e col valore che avevano.
    """
    if not isinstance(nodo, ast.Assign):
        return False
    v = nodo.value
    while isinstance(v, ast.IfExp):
        v = v.body
    if not (isinstance(v, ast.Call) and isinstance(v.func, ast.Attribute)
            and v.func.attr in ("concatenate", "vstack", "hstack") and v.args):
        return False
    p = v.args[0]
    if not isinstance(p, (ast.List, ast.Tuple)) or not p.elts:
        return False
    primo = p.elts[0]
    return (isinstance(primo, ast.Attribute) and isinstance(primo.value, ast.Name)
            and primo.value.id == "self")


def sul_genitore(indici):
    """La lettura e' SOLO su indici di genitori (`< n0`)? Allora un'estensione e' inerte."""
    if not indici:
        return False
    for s in indici:
        if s == "":
            return False                       # letta INTERA: l'estensione la cambia
        if s.strip() not in GENITORI:
            return False
    return True


def scritto_da(nodo):
    bersagli = []
    if isinstance(nodo, ast.Assign):
        bersagli = list(nodo.targets)
    elif isinstance(nodo, ast.AugAssign):
        bersagli = [nodo.target]
    for t in bersagli:
        base, indicizzata = t, False
        while isinstance(base, ast.Subscript):
            base, indicizzata = base.value, True
        if (isinstance(base, ast.Attribute) and isinstance(base.value, ast.Name)
                and base.value.id == "self"):
            return base.attr, indicizzata
    return None, False


def corpo_piatto(lista, ev, funzioni, racc, prof=0):
    for st in lista:
        if isinstance(st, ast.Expr) and isinstance(st.value, ast.Call):
            f = st.value.func
            if (isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name)
                    and f.value.id == "self"):
                if f.attr in ASSORBITE:
                    g = funzioni.get(f.attr)
                    if g is not None:
                        corpo_piatto(g.body, ev, funzioni, racc, prof + 1)
                    continue
                if f.attr in SERVIZIO:
                    racc.append({"tipo": "servizio", "scrive": f.attr,
                                 "riga": st.lineno, "evento": ev})
                    continue
        a, indicizzata = scritto_da(st)
        if a is not None:
            racc.append({"tipo": "scrittura", "scrive": a, "riga": st.lineno,
                         "evento": ev, "assorbita": prof > 0,
                         "indicizzata": indicizzata,
                         "estensione": pura_estensione(st),
                         "legge": {k: sorted(v) for k, v in letture(
                             st.value if isinstance(st, ast.Assign) else st).items()}})
        for campo in ("body", "orelse", "finalbody"):
            dentro = getattr(st, campo, None)
            if dentro:
                e2 = ev
                if campo == "body" and isinstance(st, ast.If):
                    t = ast.unparse(st.test)
                    if "COPPIA_MIT > 0.0" in t or "estratto.any()" in t:
                        e2 = "schwinger"
                corpo_piatto(dentro, e2, funzioni, racc, prof)


def principale():
    righe = []

    def stampa(*x):
        s = " ".join(str(y) for y in x)
        righe.append(s)
        print(s)

    src = io.open(SIM, encoding="utf-8").read()
    albero = ast.parse(src)
    bsim = blob(SIM)
    funzioni = {}
    for n in ast.walk(albero):
        if isinstance(n, ast.FunctionDef):
            funzioni.setdefault(n.name, n)
    regs = registri_dal_sorgente(albero)
    # l'ordine del REGISTRO, per intero: METRI prima di STATO, com'e' dichiarato.
    ord_registro = []
    for k in ("REGISTRO_METRI", "REGISTRO_STATO", "REGISTRO_FINESTRA"):
        for v in regs.get(k, ()):
            if v not in ord_registro:
                ord_registro.append(v)

    stampa("=" * 100)
    stampa("IN CHE ORDINE SI POSSONO SCRIVERE LE GRANDEZZE DELLA NASCITA?")
    stampa("  simulatore  blob %s (sha1 byte grezzi)" % bsim[:8])
    for k in sorted(regs):
        stampa("  %-20s %3d voci" % (k, len(regs[k])))
    stampa("  ### l'ordine del REGISTRO, per intero: METRI + STATO + FINESTRA = %d voci"
           % len(ord_registro))
    stampa("")
    stampa("  ### E QUESTA VERSIONE CURA UN FALSO ZERO della versione 1fb6ac63:")
    stampa("      quella faceva girare l'analisi sul solo REGISTRO_STATO, e cosi'")
    stampa("      ESCLUDEVA phi/i/j (REGISTRO_METRI) e _peqn_idx (nessun registro),")
    stampa("      cioe' ESATTAMENTE le grandezze intrecciate. Qui NESSUN insieme")
    stampa("      e' scelto a mano: si prendono TUTTE le scritture del perimetro.")
    stampa("")

    racc = []
    corpo_piatto(funzioni["mitosi"].body, "divisione", funzioni, racc)
    scritture = [r for r in racc if r["tipo"] == "scrittura"]
    servizi = [r for r in racc if r["tipo"] == "servizio"]
    esito = {"blob_sim_sha1_byte": bsim, "ordine_registro": ord_registro,
             "registri": {k: len(v) for k, v in regs.items()}}

    for ev in ("divisione", "schwinger"):
        qui = [r for r in scritture if r["evento"] == ev]
        nomi, visti = [], set()
        for r in qui:
            if r["scrive"] not in visti:
                visti.add(r["scrive"])
                nomi.append(r["scrive"])
        stampa("-" * 100)
        stampa("EVENTO `%s`: %d scritture su %d grandezze DIVERSE"
               % (ev, len(qui), len(nomi)))
        nel_reg = [n for n in nomi if n in ord_registro]
        stampa("  di cui nel REGISTRO %d, FUORI dal registro %d"
               % (len(nel_reg), len(nomi) - len(nel_reg)))
        fuori = [n for n in nomi if n not in ord_registro]
        stampa("      le FUORI: %s" % ", ".join(fuori))

        # --- il grafo: arco p -> q se `p` DEVE restare prima di `q`
        archi, inerti = [], []
        for ip, p in enumerate(qui):
            for q in qui[ip + 1:]:
                if p["scrive"] == q["scrive"]:
                    continue
                for tipo, lettore, scritto in (("flusso", q, p), ("anti", p, q)):
                    idx = lettore["legge"].get(scritto["scrive"])
                    if idx is None:
                        continue
                    arco = {"prima": p["scrive"], "dopo": q["scrive"], "dipendenza": tipo,
                            "riga_prima": p["riga"], "riga_dopo": q["riga"],
                            "chi_legge": lettore["scrive"], "indici": idx,
                            "letta": scritto["scrive"]}
                    if scritto["estensione"] and sul_genitore(idx):
                        arco["perche_inerte"] = (
                            "`%s` e' una PURA ESTENSIONE e `%s` la legge solo sui "
                            "GENITORI (%s): l'ordine NON cambia il valore"
                            % (scritto["scrive"], lettore["scrive"], ",".join(idx)))
                        inerti.append(arco)
                    else:
                        archi.append(arco)

        vincoli = {}
        for a in archi:
            vincoli.setdefault(a["prima"], set()).add(a["dopo"])
        stampa("  ### ARCHI DI DIPENDENZA: %d GENUINI, %d inerti (estensione letta sui genitori)"
               % (len(archi), len(inerti)))
        gia = set()
        for a in archi:
            k = (a["prima"], a["dopo"], a["dipendenza"])
            if k in gia:
                continue
            gia.add(k)
            stampa("      ### %-14s DEVE stare prima di %-14s  (%s: `%s` legge `%s`%s)"
                   % (a["prima"], a["dopo"], a["dipendenza"], a["chi_legge"], a["letta"],
                      (" su [%s]" % ",".join(a["indici"])) if a["indici"] != [""] else " INTERA"))

        # --- l'ordine del REGISTRO rispetta i vincoli?
        pos = {}
        for n in nomi:
            pos[n] = ord_registro.index(n) if n in ord_registro else 10 ** 6 + nomi.index(n)
        violati = [a for a in archi if pos[a["prima"]] > pos[a["dopo"]]]
        stampa("  ### L'ORDINE DEL REGISTRO VIOLA %d di questi vincoli" % len(violati))
        for a in violati:
            stampa("      ### il registro mette `%s` DOPO `%s`, ma deve stare PRIMA (%s)"
                   % (a["prima"], a["dopo"], a["dipendenza"]))

        esito[ev] = {"grandezze": nomi, "fuori_registro": fuori,
                     "archi_genuini": archi, "archi_inerti": inerti,
                     "violati_dall_ordine_del_registro": violati,
                     "assorbite": sorted(set(r["scrive"] for r in qui if r["assorbita"]))}

    stampa("-" * 100)
    stampa("LE CHIAMATE CON EFFETTO, che NON sono regole e vanno collocate A MANO: %d"
           % len(servizi))
    for s in servizi:
        stampa("    %-18s :%d   evento `%s`" % (s["scrive"], s["riga"], s["evento"]))
    esito["servizio"] = [{"nome": s["scrive"], "riga": s["riga"], "evento": s["evento"]}
                         for s in servizi]

    tot = sum(len(esito[e]["archi_genuini"]) for e in ("divisione", "schwinger"))
    viol = sum(len(esito[e]["violati_dall_ordine_del_registro"])
               for e in ("divisione", "schwinger"))
    stampa("=" * 100)
    stampa("### VERDETTO")
    stampa("###   vincoli d'ordine GENUINI nel perimetro: %d" % tot)
    if viol:
        stampa("###   L'ORDINE DEL REGISTRO NON BASTA: ne viola %d." % viol)
        stampa("###   => la tabella deve dichiarare un ORDINE TOPOLOGICO, e quell'ordine")
        stampa("###      E' PARTE DEL CONTRATTO. Non si allenta il criterio: si DICHIARA")
        stampa("###      l'ordine, perche' l'ordine del registro da solo cambierebbe i byte.")
    else:
        stampa("###   l'ordine del REGISTRO li rispetta TUTTI: e' un ordine topologico valido.")
    esito["vincoli_genuini"] = tot
    esito["violati"] = viol
    esito["registro_basta"] = (viol == 0)

    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_ordine_registro")
    if not os.path.isdir(d):
        os.makedirs(d)
    io.open(os.path.join(d, "_ordine_registro.json"), "w", encoding="utf-8",
            newline=chr(10)).write(json.dumps(esito, indent=2, ensure_ascii=False))
    io.open(os.path.join(d, "_corsa.txt"), "w", encoding="utf-8",
            newline=chr(10)).write(chr(10).join(righe) + chr(10))
    print("  referto .. %s" % d)


if __name__ == "__main__":
    principale()
