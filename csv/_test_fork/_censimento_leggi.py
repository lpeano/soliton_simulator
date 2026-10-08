# -*- coding: utf-8 -*-
"""IL CENSIMENTO DELLE LEGGI CHE MUOVONO LO STATO -- cercate **PER FORMA, NON PER NOME**.

### ⛔ **IL METODO, dichiarato prima dei risultati** *(e' il punto del mandato)*:

1. si parte da `Rete.step` e si chiude il **grafo delle chiamate** -- i metodi chiamati su
   `self` e le funzioni di modulo -- cosi' l'elenco **non dipende** da quali nomi conosco;
2. dentro ogni funzione raggiunta si cerca **OGNI SCRITTURA DI STATO**, per FORMA:
   `self.X = ...` · `self.X[...] = ...` · `self.X += ...` · `self.X[...] += ...` ·
   `np.add.at(self.X, ...)` · `self.X[...] = np.where(...)` · i `setattr`;
3. per ciascuna si registra: **riga**, **funzione**, **la GUARDIA** -- cioe' i flag di modulo
   (nome MAIUSCOLO) che la dominano negli `if` che la racchiudono -- e **i nomi letti a
   destra**, che sono *da che cosa dipende*;
4. **lo stato del flag si legge DAL DRIVER**, non dal default del modulo: si passa da
   `csv/_cli_flag.argv_del_driver()`, che esegue il testo del driver fino a
   `S._applica_flag(a)` e **cattura** la `sys.argv` che il driver ha costruito.

### ⚠ **CIO' CHE QUESTO METODO NON VEDE, e lo dico PRIMA:** le scritture per **mutazione**
*(un `dict` aggiornato dentro una funzione chiamata con l'oggetto come argomento)* -- e' il
falso positivo gia' preso su `conc_nodi` in `doc/MEMORIE_MANCANTI.md`. Per quelle il
censimento e' **per difetto**, e la tavola lo dichiara.

Gira con:  python csv/_test_fork/_censimento_leggi.py
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

SIM = os.path.join(RADICE, "soliton_simulator.py")
FUORI = os.path.join(_QUI, "_censimento_leggi")
NL = chr(10)
P = []


def stampa(s=""):
    P.append(s)
    print(s, flush=True)


# ============================================================ l'albero e il grafo di chiamata
def analizza():
    sorgente = io.open(SIM, encoding="utf-8").read()
    albero = ast.parse(sorgente)
    funzioni = {}                      # nome -> nodo
    for n in ast.walk(albero):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funzioni.setdefault(n.name, n)
    # ### i FLAG: assegnamenti di MODULO con nome MAIUSCOLO (lo stesso criterio di
    # ### `_configurazione.py`, che e' il presidio gia' in uso)
    flag = set()
    for n in albero.body:
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name) and t.id.isupper():
                    flag.add(t.id)
    return sorgente, albero, funzioni, flag


def chiamate(nodo):
    """I nomi chiamati dentro `nodo`: `self.f(...)`, `f(...)`, `Rete.f(...)`."""
    fuori = set()
    for n in ast.walk(nodo):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Attribute):
                fuori.add(f.attr)
            elif isinstance(f, ast.Name):
                fuori.add(f.id)
    return fuori


# ### LE RADICI. ### ⚠ **`step` NON BASTA, ed e' un difetto che il censimento ha preso da
# ### se': il grafo da `step` raggiunge 44 funzioni e NON contiene mitosi, Schwinger,
# ### scuoti_vuoto ne' la memoria hebbiana** -- quelle le chiama **il DRIVER**, non lo step.
# ### Un censimento con la sola radice `step` avrebbe perso TUTTA la classe CRESCITA.
RADICI = ("step", "mitosi", "decidi_divisione", "scuoti_vuoto", "memoria_hebbiana_moto",
          "rilassa_disegno", "massa_critica_adattiva", "_smorza", "_allaccia", "semina")

# ### Le variabili di stato GIA' CENSITE in doc/MEMORIE_MANCANTI.md: servono da INCROCIO,
# ### non da filtro -- una variabile fuori da questa lista non si scarta, si GUARDA.
GIA_CENSITE = (
    "_cs_nodo_prev", "_deg", "_fattore_tempo_arco", "_nb", "_nb_prec", "_nb_ret",
    "_psi_prec", "_psi_spin_prec", "_psi_spinor", "_rep", "_spinor_lift",
    "_tempo_luce_nodo", "conc_nodi", "d", "d0", "dt_e", "dt_n", "eta", "i", "j",
    "lambda_nodi", "mem_mot", "omega_s", "peq", "perc_chi", "perc_geom", "perc_tw",
    "phi", "phi0", "phi_s", "phivel", "pos", "psi", "psi_spin", "rho_spin", "tau",
    "tw", "twp", "twp_dip", "vd")


def raggiungibili(funzioni, radici=RADICI):
    """### Il grafo delle chiamate CHIUSO dalle RADICI: cosi' l'elenco non dipende dai nomi
    che conosco."""
    visti, coda = set(), list(radici)
    while coda:
        k = coda.pop()
        if k in visti or k not in funzioni:
            continue
        visti.add(k)
        for c in chiamate(funzioni[k]):
            if c in funzioni and c not in visti:
                coda.append(c)
    return visti


# ============================================================ LE SCRITTURE DI STATO, PER FORMA
def base(n):
    """Il nome dell'attributo di `self` scritto da un bersaglio, oppure `None`."""
    while isinstance(n, ast.Subscript):
        n = n.value
    if (isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)
            and n.value.id in ("self", "net", "r")):
        return n.attr
    return None


def letti(n):
    """I nomi letti a destra: attributi di `self` e flag di modulo."""
    fuori = set()
    for x in ast.walk(n):
        if isinstance(x, ast.Attribute) and isinstance(x.value, ast.Name) \
                and x.value.id in ("self", "net", "r"):
            fuori.add(x.attr)
        elif isinstance(x, ast.Name) and x.id.isupper():
            fuori.add(x.id)
    return fuori


def guardie(pila, flag):
    """I flag di modulo che dominano la riga, dagli `if` che la racchiudono."""
    fuori = []
    for t in pila:
        for x in ast.walk(t):
            if isinstance(x, ast.Name) and x.id in flag and x.id not in fuori:
                fuori.append(x.id)
    return fuori


def scritture(nodo, flag):
    """### OGNI scrittura di stato dentro `nodo`, cercata PER FORMA."""
    fuori = []

    def cammina(n, pila, dentro_ciclo):
        for c in ast.iter_child_nodes(n):
            pila2, cic = pila, dentro_ciclo
            if isinstance(n, ast.If) and c in (n.body + n.orelse):
                pila2 = pila + [n.test]
            if isinstance(n, (ast.For, ast.While)) and c in getattr(n, "body", []):
                cic = True
            if isinstance(c, ast.Assign):
                for t in c.targets:
                    b = base(t)
                    if b:
                        fuori.append(("=", b, c.lineno, guardie(pila2, flag),
                                      sorted(letti(c.value)), cic))
            elif isinstance(c, ast.AugAssign):
                b = base(c.target)
                if b:
                    fuori.append(("op=", b, c.lineno, guardie(pila2, flag),
                                  sorted(letti(c.value)), cic))
            elif isinstance(c, ast.Call):
                f = c.func
                # ### `np.add.at(self.X, ...)` -- una scrittura che NON e' un assegnamento
                if isinstance(f, ast.Attribute) and f.attr == "at" and c.args:
                    b = base(c.args[0])
                    if b:
                        fuori.append(("add.at", b, c.lineno, guardie(pila2, flag),
                                      sorted(letti(c)), cic))
                elif isinstance(f, ast.Name) and f.id == "setattr" and len(c.args) >= 2:
                    nm = c.args[1]
                    b = nm.value if isinstance(nm, ast.Constant) else "<calcolato>"
                    fuori.append(("setattr", b, c.lineno, guardie(pila2, flag),
                                  sorted(letti(c)), cic))
            cammina(c, pila2, cic)

    cammina(nodo, [], False)
    return fuori


# ============================================================ DIAGNOSTICA o STATO
# ### Le forme dei CONTATORI: `_g_*` e `_taup_*` sono i prefissi diagnostici del simulatore,
# ### e le CODE (`_tot`, `_salti`, `_shape`, `_quando`, ...) sono la forma di un contatore.
# ### ⚠ **E' un criterio di FORMA, quindi puo' sbagliare:** la tavola dichiara il criterio, e
# ### ogni variabile dichiarata diagnostica va verificata col <<nessun lettore>>.
PREFISSI_DIAG = ("_g_", "_taup_", "_sfb_", "_calcpsi_", "_smp_", "_peqn_")
CODE_DIAG = ("_tot", "_salti", "_shape", "_quando", "_chiamate", "_conteggi", "_cal",
             "_max", "_som", "_n", "_idx", "_fallback", "_clamp", "_passi", "_ultimo",
             "_scatti", "_degenere", "_nsub", "_chiusure", "_rho", "_med", "_vs_med")


def e_diagnostica(v):
    if v.startswith(PREFISSI_DIAG):
        return True
    return any(v.endswith(c) for c in CODE_DIAG)


# ============================================================ le frecce: forme a SENSO UNICO
SENSO_UNICO = ("where", "clip", "maximum", "minimum", "abs", "sign")


def a_senso_unico(sorgente, riga):
    """### `(3)` del criterio del <<no>>: una riga che usa `np.where` su un segno o un `clip`
    da un lato e' **a senso unico** e NON si testa -- misurarne la jacobiana sarebbe un
    FALSO-ZERO *(nel ramo dove non agisce `J = 0`, che e' simmetrica)*."""
    r = sorgente.split(NL)
    t = r[riga - 1] if 0 < riga <= len(r) else ""
    if riga < len(r) and t.rstrip().endswith(("(", ",", "+", "-", "*", "/")):
        t += r[riga]
    return [k for k in SENSO_UNICO if (k + "(") in t]


def main():
    os.makedirs(FUORI, exist_ok=True)
    sorgente, albero, funzioni, flag = analizza()
    glo = globals()
    glo["sorgente"] = sorgente
    rag = raggiungibili(funzioni)
    manca = [k for k in RADICI if k not in funzioni]
    assert not manca, "radici non trovate nel sorgente: %s" % manca
    stampa("=" * 104)
    stampa("IL CENSIMENTO DELLE LEGGI CHE MUOVONO LO STATO -- per FORMA, non per nome")
    stampa("=" * 104)
    stampa("  sorgente            %s righe, %d funzioni, %d flag di modulo"
           % (len(sorgente.split(NL)), len(funzioni), len(flag)))
    solo_step = raggiungibili(funzioni, ("step",))
    stampa("  grafo da `step`     %d funzioni -- e NON contiene mitosi/scuoti_vuoto: le "
           "chiama IL DRIVER" % len(solo_step))
    stampa("  grafo dalle %2d radici dichiarate: %d funzioni raggiunte  (+%d)"
           % (len(RADICI), len(rag), len(rag) - len(solo_step)))

    # ------------------------------------------------ i flag EFFETTIVI, DAL DRIVER
    S, argv = _cli_flag.argv_del_driver()
    eff = {k: getattr(S, k, None) for k in sorted(flag)}
    dif = {}
    for n in albero.body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) \
                and n.targets[0].id in flag:
            try:
                dif[n.targets[0].id] = ast.literal_eval(n.value)
            except Exception:                                  # noqa: BLE001
                pass
    cambiati = [k for k in sorted(dif) if k in eff and eff[k] != dif[k]]
    stampa("  argv del driver     %s" % " ".join(argv[1:]))
    stampa("  flag CAMBIATI dall'argv rispetto al default del sorgente: %d" % len(cambiati))
    for k in cambiati:
        stampa("      %-28s default %-14s EFFETTIVO %s" % (k, dif[k], eff[k]))

    # ------------------------------------------------ LE SCRITTURE
    righe = []
    for f in sorted(rag):
        for (modo, var, ln, g, dip, cic) in scritture(funzioni[f], flag):
            righe.append({"funzione": f, "modo": modo, "variabile": var, "riga": ln,
                          "guardie": g, "dipende_da": dip, "in_ciclo": cic,
                          "senso_unico": a_senso_unico(sorgente, ln),
                          "guardie_effettive": {k: bool(eff.get(k)) for k in g}})
    stampa("  SCRITTURE DI STATO trovate: %d, su %d variabili distinte"
           % (len(righe), len(set(r["variabile"] for r in righe))))

    # ------------------------------------------------ cio' che il driver SPEGNE
    spente = [r for r in righe if r["guardie"] and
              not all(bool(eff.get(k)) for k in r["guardie"])]
    vive = [r for r in righe if r not in spente]
    stampa("      di cui SPENTE nel driver (una guardia e' falsa): %d" % len(spente))
    stampa("      VIVE nella scena del driver:                     %d" % len(vive))
    su = [r for r in vive if r["senso_unico"]]
    stampa("      fra le VIVE, a SENSO UNICO (np.where/clip/max/min): %d" % len(su))

    stampa()
    stampa("-" * 104)
    stampa("LE VARIABILI DI STATO SCRITTE NELLA SCENA DEL DRIVER, e da dove")
    stampa("-" * 104)
    per_var = {}
    for r in vive:
        if not e_diagnostica(r["variabile"]):
            per_var.setdefault(r["variabile"], []).append(r)
    diag = sorted(set(r["variabile"] for r in vive if e_diagnostica(r["variabile"])))
    stampa("      di cui DIAGNOSTICHE per forma (prefisso o coda da contatore): %d variabili"
           % len(diag))
    stampa("      VARIABILI DI STATO vere, che restano da classificare:        %d"
           % len(per_var))
    stampa()
    for v in sorted(per_var, key=lambda k: -len(per_var[k])):
        rr = per_var[v]
        fn = sorted(set(x["funzione"] for x in rr))
        gg = sorted(set(k for x in rr for k in x["guardie"]))
        stampa("  %-18s %2d scritture  %-4s in %-40s  guardie: %s"
               % (v, len(rr), "" if v in GIA_CENSITE else "NEW",
                  ",".join(fn)[:40], ",".join(gg) if gg else "(nessuna)"))
    fuori_lista = sorted(v for v in per_var if v not in GIA_CENSITE)
    stampa()
    stampa("  FUORI dal censimento di doc/MEMORIE_MANCANTI.md: %d variabili -- e NON si "
           "scartano, si GUARDANO" % len(fuori_lista))
    stampa("      %s" % " ".join(fuori_lista))
    mai_scritte = sorted(v for v in GIA_CENSITE if v not in per_var)
    stampa("  CENSITE ma MAI scritte dalle radici: %d  -- %s"
           % (len(mai_scritte), " ".join(mai_scritte)))

    io.open(os.path.join(FUORI, "censimento.json"), "w", encoding="utf-8").write(
        json.dumps({"argv": argv,
                    "flag_cambiati": {k: [str(dif[k]), str(eff[k])] for k in cambiati},
                    "raggiunte": sorted(rag), "scritture": righe}, ensure_ascii=False,
                   default=str))
    io.open(os.path.join(FUORI, "censimento.txt"), "w", encoding="utf-8").write(
        NL.join(P) + NL)
    stampa()
    stampa("scritto %s" % os.path.join(FUORI, "censimento.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
