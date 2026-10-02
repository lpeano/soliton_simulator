# -*- coding: utf-8 -*-
"""**I TRE CASI CHE DEVONO FALLIRE** del `COMMIT 3` *(par.(c), criteri fissati PRIMA)*.

Un sigillo che dice *<<passa>>* senza un caso che lo faccia cadere non e' un sigillo
*(`STANDARD 1`)*. Il piano ne chiede ### **tre**, e sono tre cose diverse:

| | il caso | che cosa deve succedere |
|---|---|---|
| ### **①** | si ### **TOGLIE** una grandezza dalla tabella | il run ### **SI FERMA** con *<<regola di nascita non dichiarata>>* |
| ### **②** | si ### **CAMBIA** la regola di UNA grandezza *(`psi` da **media** a **eredita**)* | il sigillo ### **DEVE VEDERE** la differenza |
| ### **③** | si lascia una ### **SCRITTURA SPARSA** a valle | deve essere ### **IMPOSSIBILE**, cioe' il presidio deve ### **NOMINARLA** |

## -- E IL CASO ③ NON ERA COPERTO, e lo dico prima di tutto

Il presidio del punto unico verifica che ### **ogni grandezza ABBIA una regola.**
### **Non verifica che nessun ALTRO la scriva.** Quindi una riga aggiunta ### **dopo**
la chiamata a `nascita()` sarebbe passata ### **in silenzio**, e il caso ③ del piano
### **non aveva un presidio.** Questo file lo costruisce.

### **LA FORMA DEL PRESIDIO ③, e la distinzione e' il punto:** dentro il perimetro
della nascita, una grandezza del registro non deve essere ### **ESTESA** fuori dalle
regole — ma puo' essere ### **MODIFICATA SU INDICE**, perche' quello non e' una
nascita: ### **e' IL CALCIO ai genitori**, che agisce su nodi che esistono gia'.

| forma | dentro `mitosi`, fuori dalle regole |
|---|---|
| `self.phi = np.concatenate([...])` | ### **VIETATA**: allunga, cioe' fa nascere |
| `self.phi[a] = ...` | ### **AMMESSA**: tocca nodi che ci sono |

**COMANDO:** `python csv/_seal_fork/_sigillo_tre_casi.py`
*(il caso ② vuole due run da 72 passi: `--salta-2` lo dichiara non eseguito.)*

**USCITA:** `csv/_seal_fork/_sigillo_tre_casi/` — `_sigillo_tre_casi.json` + `_corsa.txt`.
"""
import ast
import contextlib
import hashlib
import io
import json
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_QUI, ".."))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _cli_flag                   # noqa: E402
import _passo                      # noqa: E402
import _confronto_nascita as CN    # noqa: E402

SIM = os.path.join(RADICE, "soliton_simulator.py")
FUORI = os.path.join(_QUI, "_sigillo_tre_casi")
NL = chr(10)
# il perimetro in cui una nascita puo' avvenire: le funzioni che chiamano `nascita()`.
# ### SI DERIVA dall'AST, non si scrive a mano (`FALSO-ZERO`: nessun insieme scelto a mano).
PREFISSO_REGOLE = "_rn_"


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def ordine_e_regole(sorgente):
    """`(ORDINE_DI_NASCITA, nomi delle regole, funzioni che chiamano nascita())` dall'AST."""
    t = ast.parse(io.open(sorgente, encoding="utf-8").read())
    registri = {}
    for n in ast.walk(t):
        if (isinstance(n, ast.Assign) and len(n.targets) == 1
                and isinstance(n.targets[0], ast.Name)
                and n.targets[0].id.startswith("REGISTRO")):
            nomi = []
            if isinstance(n.value, (ast.Tuple, ast.List)):
                for e in n.value.elts:
                    if (isinstance(e, (ast.Tuple, ast.List)) and e.elts
                            and isinstance(e.elts[0], ast.Constant)):
                        nomi.append(e.elts[0].value)
            registri[n.targets[0].id] = nomi
    ordine = []
    for k in ("REGISTRO_METRI", "REGISTRO_STATO", "REGISTRO_FINESTRA"):
        for v in registri.get(k, ()):
            if v not in ordine:
                ordine.append(v)
                if v == "peq":
                    ordine.append("_peqn_idx")
    regole = sorted(n.name for n in ast.walk(t)
                    if isinstance(n, ast.FunctionDef) and n.name.startswith(PREFISSO_REGOLE))
    chiamanti = []
    for n in ast.walk(t):
        if not isinstance(n, ast.FunctionDef):
            continue
        for x in ast.walk(n):
            if (isinstance(x, ast.Call) and isinstance(x.func, ast.Name)
                    and x.func.id == "nascita"):
                if n.name not in chiamanti:
                    chiamanti.append(n.name)
    return ordine, regole, chiamanti


def estensioni_sparse(sorgente):
    """### IL PRESIDIO ③: le grandezze del registro ESTESE fuori dalle regole, nel perimetro.

    Restituisce l'elenco delle scritture che ### **allungano** una grandezza di
    `ORDINE_DI_NASCITA` dentro una funzione che chiama `nascita()`. ### **Le scritture
    su INDICE non contano**: quelle toccano nodi che esistono gia' (e' il calcio).
    """
    ordine, regole, chiamanti = ordine_e_regole(sorgente)
    t = ast.parse(io.open(sorgente, encoding="utf-8").read())
    trovate = []
    for n in ast.walk(t):
        if not (isinstance(n, ast.FunctionDef) and n.name in chiamanti):
            continue
        for x in ast.walk(n):
            if not isinstance(x, (ast.Assign, ast.AugAssign)):
                continue
            mire = x.targets if isinstance(x, ast.Assign) else [x.target]
            for m in mire:
                base, su_indice = m, False
                while isinstance(base, ast.Subscript):
                    base, su_indice = base.value, True
                if not (isinstance(base, ast.Attribute) and isinstance(base.value, ast.Name)
                        and base.value.id in ("self", "net")):
                    continue
                if base.attr not in ordine or su_indice:
                    continue
                trovate.append({"grandezza": base.attr, "dentro": n.name, "riga": x.lineno,
                                "codice": ast.unparse(x)[:160]})
    return trovate, ordine, regole, chiamanti


def copia_con(sorgente, dest, vecchio, nuovo, etichetta):
    """Scrive una copia con UNA sostituzione, e ASSERISCE che l'ancora sia unica."""
    t = io.open(sorgente, encoding="utf-8", newline="").read()
    n = t.count(vecchio)
    if n != 1:
        raise SystemExit("** [%s] l'ancora e' presente %d volte (attesa 1). NON scrivo la "
                         "copia. **" % (etichetta, n))
    io.open(dest, "wb").write(t.replace(vecchio, nuovo).encode("utf-8"))
    a, b = t.split(NL), io.open(dest, encoding="utf-8", newline="").read().split(NL)
    # ### SE L'INIEZIONE AGGIUNGE UNA RIGA, il confronto riga-per-riga SLITTA TUTTO:
    #   il caso 3 inserisce una riga, e la prima stesura stampava 4800 numeri di riga
    #   -- un referto di 29 KB che NESSUNO legge. ### Era un difetto del REFERTO, non
    #   del test, e un referto illeggibile e' un referto che non serve.
    #   ### Quando le lunghezze DIFFERISCONO si riporta cio' che conta: quante righe
    #   prima, quante dopo, e DOVE comincia la differenza.
    if len(a) != len(b):
        k = next((i + 1 for i, (x, y) in enumerate(zip(a, b)) if x != y), len(a) + 1)
        return {"righe_prima": len(a), "righe_dopo": len(b),
                "aggiunte": len(b) - len(a), "prima_riga_diversa": k}
    return {"righe_prima": len(a), "righe_dopo": len(b), "aggiunte": 0,
            "righe_diverse": [k + 1 for k, (x, y) in enumerate(zip(a, b)) if x != y]}


def importa_isolato(percorso, nome):
    """Importa un simulatore da un percorso, come modulo privato. Restituisce l'eccezione."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(nome, percorso)
    mod = importlib.util.module_from_spec(spec)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            spec.loader.exec_module(mod)
        return None, mod
    except Exception as e:
        return e, None


def carica(nome, seme, sim=None):
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=%d" % seme],
                                              dest=os.path.join(FUORI, "_scarto_" + nome))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome=nome, sim=sim)
        S._applica_regime(a)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    return S, S.net


def avanza(S, net, passi):
    with contextlib.redirect_stdout(io.StringIO()):
        for _ in range(passi):
            _passo.passo_pieno(S, net)
    return net


def principale():
    seme, passi, salta2 = 11, 72, False
    for x in sys.argv[1:]:
        if x.startswith("--seme="):
            seme = int(x.split("=", 1)[1])
        elif x.startswith("--passi="):
            passi = int(x.split("=", 1)[1])
        elif x == "--salta-2":
            salta2 = True
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    P = []

    def stampa(*x):
        r = " ".join(str(y) for y in x)
        P.append(r)
        print(r)

    stampa("=" * 104)
    stampa("I TRE CASI CHE DEVONO FALLIRE  --  `COMMIT 3`, la nascita come evento unico")
    stampa("=" * 104)
    stampa("simulatore ..... %s (sha1 byte grezzi)" % blob(SIM)[:8])
    stampa("questo sigillo . %s" % blob(os.path.abspath(__file__))[:8])
    stampa("seme %d   passi %d" % (seme, passi))
    stampa("")

    ref = {"blob_sim_sha1_byte": blob(SIM), "blob_sigillo": blob(os.path.abspath(__file__)),
           "seme": seme, "passi": passi}

    # ---------- CASO ① : si TOGLIE una grandezza dalla tabella --------------------------------
    stampa("=" * 104)
    stampa("CASO 1 -- SI TOGLIE UNA GRANDEZZA DALLA TABELLA: il run deve FERMARSI")
    stampa("=" * 104)
    d1 = os.path.join(FUORI, "_sim_senza_peq.py")
    ANC1 = ('@_nascita_regola("divisione", "peq", "eredita dall\'arco che si spezza",')
    try:
        diverse1 = copia_con(SIM, d1, ANC1, '@_nascita_regola("divisione", "peq_TOLTA", '
                             '"eredita dall\'arco che si spezza",', "caso 1")
        stampa("  copia: una grandezza RINOMINATA nella tabella: %s" % diverse1)
        err1, _m = importa_isolato(d1, "_sim_caso1")
        atteso = "regola di nascita non dichiarata per `peq` all'evento `divisione`"
        ok1 = err1 is not None and atteso in str(err1)
        stampa("  l'import ha alzato ... %s" % (type(err1).__name__ if err1 else "### NIENTE"))
        if err1:
            stampa("  il messaggio ......... %s" % str(err1)[:150])
        stampa("  nomina la grandezza E l'evento? %s" % ("SI" if ok1 else "NO"))
        stampa("  ### E SI FERMA ALL'IMPORT, non al primo run: il processo non parte nemmeno.")
    except SystemExit as e:
        stampa("  ### CASO 1 NON ESEGUIBILE: %s" % e)
        ok1, diverse1, err1 = False, {}, None
    stampa("  ### CASO 1: %s" % ("PASSA" if ok1 else "FALLISCE"))
    ref["caso_1"] = {"passa": bool(ok1), "righe_diverse": diverse1,
                     "eccezione": (str(err1) if err1 else None)}
    stampa("")

    # ---------- CASO ③ : una scrittura SPARSA a valle -----------------------------------------
    stampa("=" * 104)
    stampa("CASO 3 -- UNA SCRITTURA SPARSA A VALLE: il presidio deve NOMINARLA")
    stampa("=" * 104)
    sparse, ordine, regole, chiamanti = estensioni_sparse(SIM)
    stampa("  grandezze governate %d   regole `%s*` %d   funzioni che chiamano `nascita()` %s"
           % (len(ordine), PREFISSO_REGOLE, len(regole), ", ".join(chiamanti)))
    stampa("  ### estensioni SPARSE nel perimetro, fuori dalle regole: %d" % len(sparse))
    for s in sparse:
        stampa("      ### %s dentro `%s` :%d   %s"
               % (s["grandezza"], s["dentro"], s["riga"], s["codice"]))
    # ### IL CONTROLLO POSITIVO, e senza di lui lo zero sopra non vale niente (`STANDARD 2`).
    d3 = os.path.join(FUORI, "_sim_sparsa.py")
    ANC3 = '        nascita(self, "divisione", c)'
    INIETTA = (ANC3 + NL
               + "        self.phi = np.concatenate([self.phi, fm])   # SCRITTURA SPARSA INIETTATA")
    try:
        diverse3 = copia_con(SIM, d3, ANC3, INIETTA, "caso 3")
        sparse3, _o, _r, _c = estensioni_sparse(d3)
        trovata = [s for s in sparse3 if s["grandezza"] == "phi"]
        stampa("")
        stampa("  CONTROLLO POSITIVO: iniettata `self.phi = np.concatenate([self.phi, fm])`")
        stampa("      subito DOPO la chiamata al punto unico: %s" % diverse3)
        stampa("      ### il presidio la trova? %s" % ("SI" if trovata else "### NO"))
        for s in trovata:
            stampa("      ### NOMINATA: %s dentro `%s` :%d   %s"
                   % (s["grandezza"], s["dentro"], s["riga"], s["codice"]))
        ok3 = (len(sparse) == 0) and (len(trovata) == 1)
    except SystemExit as e:
        stampa("  ### CONTROLLO POSITIVO NON ESEGUIBILE: %s" % e)
        ok3, diverse3, trovata = False, {}, []
    stampa("")
    stampa("")
    stampa("  ### ⛔ IL LIMITE DI QUESTO PRESIDIO, e si legge PRIMA dello zero di sopra")
    stampa("      (rilievo del guardiano, 2026-10-03):")
    stampa("      La ricerca gira SOLO dentro le funzioni che CHIAMANO `nascita()`, e oggi")
    stampa("      quella e' UNA SOLA: %s." % ", ".join(chiamanti))
    stampa("      ### QUINDI un'estensione di una grandezza del registro fatta in `step()`,")
    stampa("      ### o in un'altra voce del passo, NON VIENE NOMINATA.")
    stampa("      Il presidio prova che la nascita e' in un punto solo DENTRO il suo")
    stampa("      perimetro; NON prova che nessun ALTRO posto del simulatore allunghi")
    stampa("      quelle grandezze. ### E' una differenza vera, e lo zero di sopra si legge")
    stampa("      con questo limite davanti.")
    stampa("      Allargare la ricerca a TUTTO il file e' la stessa cosa del cablaggio nel")
    stampa("      `pre-commit`, ed e' IN CODA (`NASCITA-PUNTO-UNICO`).")
    stampa("")
    stampa("  ### E IL PRESIDIO NON E' CABLATO IN UN HOOK: e' uno SCRIPT (`A9`).")
    stampa("      Finche' non gira nel `pre-commit`, NON IMPEDISCE NIENTE -- lo dico.")
    stampa("  ### CASO 3: %s" % ("PASSA" if ok3 else "FALLISCE"))
    ref["caso_3"] = {"passa": bool(ok3), "sparse_nel_simulatore": sparse,
                     "controllo_positivo_trovate": trovata, "righe_diverse": diverse3,
                     "grandezze_governate": len(ordine), "regole": len(regole),
                     "chiamanti": chiamanti,
                     "LIMITE": ("la ricerca gira SOLO dentro le funzioni che chiamano "
                                "nascita() (oggi: %s). Un'estensione di una grandezza del "
                                "registro in step() o in un'altra voce del passo NON viene "
                                "nominata. Rilievo del guardiano, 2026-10-03; allargarla a "
                                "tutto il file e' IN CODA come il cablaggio."
                                % ", ".join(chiamanti)),
                     "NON_CABLATO": "e' uno script, non un hook (A9)"}
    stampa("")

    # ---------- CASO ② : si CAMBIA la regola di `psi` -----------------------------------------
    stampa("=" * 104)
    stampa("CASO 2 -- SI CAMBIA LA REGOLA DI `psi` (da MEDIA a EREDITA): il sigillo deve VEDERLA")
    stampa("=" * 104)
    ok2, diff2, diverse2 = None, [], {}
    if salta2:
        stampa("  ### NON ESEGUITO (`--salta-2`), e lo dichiaro: due run da %d passi." % passi)
    else:
        d2 = os.path.join(FUORI, "_sim_psi_eredita.py")
        ANC2 = ('        net.psi = np.concatenate([cur[:c["n0"]], '
                '0.5 * (cur[c["src_a"]] + cur[c["src_b"]])])')
        MEDIA_VIA = ('        net.psi = np.concatenate([cur[:c["n0"]], cur[c["src_a"]]])'
                     '   # REGOLA CAMBIATA: eredita invece di media')
        try:
            diverse2 = copia_con(SIM, d2, ANC2, MEDIA_VIA, "caso 2")
            stampa("  copia: `psi` EREDITA da `a` invece di MEDIARE. %s" % diverse2)
            stampa("      ### ed e' il cambio di UNA regola, non di un numero: e' il tipo di")
            stampa("      ### difetto che un riordino puo' introdurre senza accorgersene.")
            SA, nA = carica("tre_casi_sano", seme)
            avanza(SA, nA, passi)
            fa, _q = CN.foto(SA, nA, sorgente=SIM)
            SB, nB = carica("tre_casi_psi", seme, sim=d2)
            avanza(SB, nB, passi)
            fb, _q2 = CN.foto(SB, nB, sorgente=d2)
            diff2 = CN.confronta(fa, fb)
            stampa("  ### il sigillo vede %d differenze" % len(diff2))
            for d in diff2[:14]:
                stampa("      ### %s" % json.dumps(d, ensure_ascii=False, default=str)[:220])
            nomi2 = sorted(d["nome"] for d in diff2)
            stampa("  le grandezze diverse: %s" % ", ".join(nomi2[:20]))
            stampa("  `psi` e' fra loro? %s" % ("SI" if "psi" in nomi2 else "### NO"))
            nati = int(getattr(nA, "_g_nati_mitosi_ev", 0))
            stampa("  eventi di mitosi nel run: %d" % nati)
            if not nati:
                stampa("  ### NESSUNA MITOSI: il caso 2 non misura niente. NON MISURATO.")
            ok2 = bool(diff2) and ("psi" in nomi2) and bool(nati)
        except SystemExit as e:
            stampa("  ### CASO 2 NON ESEGUIBILE: %s" % e)
            ok2 = False
        stampa("  ### CASO 2: %s" % ("PASSA" if ok2 else "FALLISCE"))
    ref["caso_2"] = {"passa": ok2, "eseguito": not salta2, "differenze": diff2,
                     "righe_diverse": diverse2}
    stampa("")

    stampa("=" * 104)
    passa = bool(ok1) and bool(ok3) and (ok2 is not False)
    stampa("### I TRE CASI %s   (1 %s · 2 %s · 3 %s)"
           % ("PASSANO" if passa else "NON PASSANO",
              "OK" if ok1 else "NO",
              ("OK" if ok2 else ("NO" if ok2 is False else "NON ESEGUITO")),
              "OK" if ok3 else "NO"))
    stampa("=" * 104)
    ref["passa"] = bool(passa)
    io.open(os.path.join(FUORI, "_sigillo_tre_casi.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(ref, indent=1, default=str))
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(P) + NL)
    return 0 if passa else 1


if __name__ == "__main__":
    sys.exit(principale())
