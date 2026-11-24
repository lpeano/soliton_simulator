# -*- coding: utf-8 -*-
r"""**L0 DEL LORENTZ LOCALE: CHI SENTE `N`** *(il mandato di Luca `2026-11-21` sera; la carta `doc/TASK_HISTORY/2026-11-21_lorentz_locale.md`, sez. `2.1`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/lorentz_censimento.py --radice C:\Users\lpeano\wt_lapse_u
    E:\python\py3132\python.exe doc/referti_l2/lorentz_censimento.py --radice C:\Users\lpeano\wt_mitosi_chi

**La macchina di `censimento_a17_era2.py`** *(ramo `mitosi`, `9af98467`; copiata qui: quel file non c'e' su questo ramo)*: le LETTURE nell'AST *(gli attributi `.cs`, `.dtau`, `.s_a`, `.w`, `.lambda_c`, `.c2`, `.m2`; le chiamate `s_arco`, `dtau_nodo`, `dtau_arco`, `cs_di`, `N_di`, `cs_prec`; i nomi `N`, `C_CHI`)*; DIRETTO / INDIRETTO *(per nome semplice, chiuso: SOVRA-approssimato, dichiarato)*; **la TABELLA a mano per funzione DIRETTA: il settore e «segue `N`»** *(`SI`: legge `cs` mentre `tick_chi` lo ha messo a `s N`; `NO`: una costante o un valore congelato; `-`: fuori dal tick)*; **fuori tabella: ALZA** *(uscita `1`, dopo aver stampato tutto)*; le ANCORE del tick per settore; **le letture (1)-(3) della carta, CONFERMATE o no.**
"""
import argparse
import ast
import os
import sys

FILES = ["doc/referti_l2/chi_tick.py", "doc/referti_l2/chi_mattone_v2.py", "doc/referti_l2/chi_tronco.py", "doc/referti_l2/mitosi_chi_v4.py",
         "primo_ordine/motore.py", "primo_ordine/tick.py", "primo_ordine/flussi_parziali.py", "primo_ordine/energia_pesata.py",
         "csv/solitone/_u1_oggi.py", "csv/solitone/porto.py", "csv/solitone/mattone.py", "csv/solitone/conti.py", "csv/solitone/u1_generico.py",
         "csv/solitone/contatore.py", "csv/_u1_prototipo.py"]
TERMINI = "primo_ordine/termini"
ATTR = {"cs": "cs", "dtau": "dtau", "s_a": "s_a", "w": "w", "lambda_c": "lambda_c", "c2": "c2", "m2": "m2"}
CHIAMATE = {"s_arco": "s_arco()", "dtau_nodo": "dtau_nodo()", "dtau_arco": "dtau_arco()", "cs_di": "cs_di()", "N_di": "N_di()", "cs_prec": "cs_prec()"}
NOMI = {"N": "N", "C_CHI": "C_CHI"}
SI, NO, FUORI = "SI", "NO", "-"
# ### (il settore, segue N, il perche')
TABELLA = {
    "csv/_u1_prototipo.py::Campo.K": ("U1", NO, "l'energia elettrica con w = s_a^2 l/l*: s_a CONGELATO alla costruzione"),
    "csv/_u1_prototipo.py::Campo.__init__": ("U1", NO, "s_a si copia UNA volta: w = s_a^2 L_SU_LS"),
    "csv/_u1_prototipo.py::Campo.deriva": ("U1", NO, "LA DERIVA A += f w E: w congelato"),
    "csv/_u1_prototipo.py::campo_gradiente": ("prova", FUORI, "la parte G: s_a da un cs statico dato a mano"),
    "csv/_u1_prototipo.py::energia": ("U1", FUORI, "l'energia del prototipo (s_a del campo)"),
    "csv/_u1_prototipo.py::energia_nodi": ("U1", FUORI, "un'energia per nodo (misura)"),
    "csv/_u1_prototipo.py::gauss_energia": ("prova", FUORI, "una prova"),
    "csv/_u1_prototipo.py::scena_materia": ("prova", FUORI, "una scena di prova"),
    "csv/solitone/_u1_oggi.py::campo_della_scena": ("U1", NO, "s_a = s_arco(mot) ALLA COSTRUZIONE: il cs di quel momento, poi congelato"),
    "csv/solitone/contatore.py::ritmo": ("mitosi", SI, "Theta: pi (dtau cs_i - dtau cs_j) col cs del tick"),
    "csv/solitone/conti.py::scena": ("misura", FUORI, "la scena delle misure"),
    "csv/solitone/mattone.py::scena": ("misura", FUORI, "la scena"),
    "csv/solitone/porto.py::salva": ("misura", FUORI, "salva cs_prec"),
    "csv/solitone/u1_generico.py::CampoGenerico.K": ("U1", NO, "come Campo.K: w congelato"),
    "csv/solitone/u1_generico.py::CampoGenerico.__init__": ("U1", NO, "s_a si copia UNA volta"),
    "csv/solitone/u1_generico.py::CampoGenerico.cresci": ("U1", NO, "s_a dei nati: il valore uniforme (congelato)"),
    "csv/solitone/u1_generico.py::CampoGenerico.deriva": ("U1", NO, "LA DERIVA: w congelato"),
    "doc/referti_l2/chi_tick.py::Laplaciano.statico": ("chi", FUORI, "il profilo statico (la taratura)"),
    "doc/referti_l2/chi_tick.py::Parametri.__init__": ("chi", NO, "c2 = C_CHI^2 = 0.25 COSTANTE"),
    "doc/referti_l2/chi_tick.py::Parametri.__repr__": ("chi", FUORI, "la stampa"),
    "doc/referti_l2/chi_tick.py::Q_di": ("chi", SI, "la sorgente Q coi pesi di cs = s N"),
    "doc/referti_l2/chi_tick.py::energia_chi": ("chi", SI, "l'energia: i pesi di cs = s N; H_chi con c2 e m2 costanti"),
    "doc/referti_l2/chi_tick.py::energia_oggi": ("misura", FUORI, "l'energia del tick di oggi (confronto)"),
    "doc/referti_l2/chi_tick.py::fase_a": ("psi", SI, "la fase (a) e^{+i e0 (N - 1)/2}"),
    "doc/referti_l2/chi_tick.py::forza": ("chi", NO, "LA FORZA DI CHI: c2 Delta chi - m2 chi COSTANTI; N solo nella sorgente"),
    "doc/referti_l2/chi_tick.py::tick_chi": ("chi", NO, "il tick: chi avanza con dt = mot.dtau[0] (il tick, non dtau cs); mot.cs = s N UNA volta (il N di meta' tick)"),
    "doc/referti_l2/mitosi_chi_v4.py::applica_chi": ("mitosi", SI, "cs del nodo nato da chi"),
    "doc/referti_l2/mitosi_chi_v4.py::nascite": ("prova", FUORI, "la prova K4"),
    "doc/referti_l2/mitosi_chi_v4.py::salva": ("misura", FUORI, "salva cs_prec"),
    "primo_ordine/energia_pesata.py::applica": ("phi", SI, "la fase del vuoto (Omega): legge cs e lambda_c; con chi lambda_c = None, quindi spenta"),
    "primo_ordine/energia_pesata.py::d_peso_arco": ("chi", SI, "dw/dcs coi cs = s N (la Q)"),
    "primo_ordine/energia_pesata.py::g_dello_stato": ("misura", FUORI, "G dello stato"),
    "primo_ordine/energia_pesata.py::g_pesata": ("misura", FUORI, "G pesata"),
    "primo_ordine/energia_pesata.py::omega": ("phi", FUORI, "Omega: lambda_c None con chi"),
    "primo_ordine/energia_pesata.py::pesi": ("chi", SI, "i pesi cs e s_arco (l'energia, la Q)"),
    "primo_ordine/energia_pesata.py::pesi_dello_stato": ("misura", FUORI, "i pesi dello stato"),
    "primo_ordine/energia_pesata.py::termini_di_h": ("chi", SI, "i termini di H coi cs (la Q)"),
    "primo_ordine/energia_pesata.py::tetto_omega": ("phi", FUORI, "il tetto di Omega"),
    "primo_ordine/flussi_parziali.py::accendi_cs": ("psi", FUORI, "accende il lapse N(rho): NON con chi"),
    "primo_ordine/flussi_parziali.py::dtau_nodo": ("psi", SI, "IL TEMPO PROPRIO PER NODO dtau cs: l'unico posto da cui il passo lo legge"),
    "primo_ordine/flussi_parziali.py::s_arco": ("psi", SI, "la media armonica di dtau_nodo per arco: lo spostamento"),
    "primo_ordine/flussi_parziali.py::s_nodo": ("psi", SI, "dtau_nodo per nodo: il Grover"),
    "primo_ordine/flussi_parziali.py::z_arco": ("psi", SI, "e^{i pi s_arco f}: lo spostamento"),
    "primo_ordine/motore.py::Motore._moneta_spin": ("psi", SI, "la moneta: ang = eps dtau_nodo"),
    "primo_ordine/motore.py::Motore._saturazione": ("psi", FUORI, "la saturazione: fuori dall'ordine (superata)"),
    "primo_ordine/motore.py::Motore.cresci": ("mitosi", FUORI, "segue la crescita: cs e dtau dei nati"),
    "primo_ordine/tick.py::cs_al_centro": ("psi", FUORI, "il punto fisso del lapse N(rho): NON con chi (lambda_c None)"),
}
ANCORE = [
    ("psi: lo spostamento", "primo_ordine/flussi_parziali.py::hop_psi"),
    ("psi: il Grover", "primo_ordine/flussi_parziali.py::grover"),
    ("psi: la moneta", "primo_ordine/motore.py::Motore._moneta_spin"),
    ("psi: la fase (a)", "doc/referti_l2/chi_tick.py::fase_a"),
    ("phi: lo spostamento del vuoto", "primo_ordine/flussi_parziali.py::hop_phi"),
    ("phi: il materia-vuoto", "primo_ordine/motore.py::Motore._materia_vuoto"),
    ("phi: la fase del vuoto", "primo_ordine/motore.py::Motore._fase_vuoto"),
    ("U1: la deriva", "csv/_u1_prototipo.py::Campo.deriva"),
    ("U1: la spinta", "csv/_u1_prototipo.py::Campo.spinta"),
    ("U1: il campo generico, la deriva", "csv/solitone/u1_generico.py::CampoGenerico.deriva"),
    ("chi: la forza", "doc/referti_l2/chi_tick.py::forza"),
    ("chi: il tick", "doc/referti_l2/chi_tick.py::tick_chi"),
    ("il contatore", "csv/solitone/contatore.py::ritmo"),
]


def tipo(node):
    if isinstance(node, ast.Attribute) and node.attr in ATTR and isinstance(node.ctx, ast.Load):
        return ATTR[node.attr]
    if isinstance(node, ast.Call):
        f = node.func
        nm = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else None)
        return CHIAMATE.get(nm)
    if isinstance(node, ast.Name) and node.id in NOMI and isinstance(node.ctx, ast.Load):
        return NOMI[node.id]
    return None


def chiamati(node):
    out = set()
    for c in ast.walk(node):
        if isinstance(c, ast.Call):
            f = c.func
            nm = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else None)
            if nm:
                out.add(nm)
    return out


def leggi(radice, p):
    t = ast.parse(open(os.path.join(radice, p), encoding="utf-8").read())
    letture, funz = [], {}

    def giro(node, fn):
        for c in ast.iter_child_nodes(node):
            f2 = fn
            if isinstance(c, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                f2 = (fn + "." if fn else "") + c.name
                if not isinstance(c, ast.ClassDef):
                    funz[f2] = chiamati(c)
            k = tipo(c)
            if k:
                letture.append((p, c.lineno, f2 or "<modulo>", k))
            giro(c, f2)
    giro(t, "")
    return letture, funz


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--radice", required=True)
    x = ap.parse_args(argv)
    R = x.radice
    files = list(FILES) + sorted(TERMINI + "/" + f for f in os.listdir(os.path.join(R, TERMINI)) if f.endswith(".py"))
    print("=" * 140)
    print("L0 DEL LORENTZ LOCALE, CHI SENTE N (la carta sez. 2.1): la radice %s, %d file" % (R, len(files)))
    print("=" * 140)
    letture, funz, mancano = [], {}, []
    for p in files:
        if not os.path.exists(os.path.join(R, p)):
            mancano.append(p)
            continue
        l_, f_ = leggi(R, p)
        letture += l_
        for nm, cs in f_.items():
            funz[p + "::" + nm] = cs
    if mancano:
        print("### i file che NON ci sono in questa radice: %s" % mancano)
    dirette = {}
    for p, riga, fn, k in letture:
        dirette.setdefault(p + "::" + fn, {}).setdefault(k, []).append(riga)
    nome = {q: q.split("::")[1].split(".")[-1] for q in funz}
    porta = {q: set(v) for q, v in dirette.items()}
    cambia = True
    while cambia:
        cambia = False
        per_nome = {}
        for q, ks in porta.items():
            per_nome.setdefault(q.split("::")[1].split(".")[-1], set()).update(ks)
        for q, cs in funz.items():
            nuovi = set()
            for c in cs:
                if c in per_nome and c != nome[q]:
                    nuovi |= per_nome[c]
            if not nuovi <= porta.get(q, set()):
                porta.setdefault(q, set()).update(nuovi)
                cambia = True
    print("### LE LETTURE DIRETTE (%d letture in %d funzioni):" % (len(letture), len(dirette)))
    fuori = []
    for q in sorted(dirette):
        d = TABELLA.get(q)
        if d is None:
            fuori.append(q)
        print("  %-62s %-34s %-7s segue N: %-3s %s" % (q, ", ".join("%s r.%s" % (k, ",".join(map(str, sorted(set(v))))) for k, v in sorted(dirette[q].items())),
                                                    d[0] if d else "###", d[1] if d else "###", d[2] if d else "### NON IN TABELLA"))
    print("### LE ANCORE DEL TICK (che cosa raggiungono, DIRETTO o INDIRETTO per nome semplice):")
    for desc, anc in ANCORE:
        if anc not in funz:
            print("  %-36s %-58s ### NON TROVATA" % (desc, anc))
            continue
        ks = porta.get(anc, set())
        dd = "DIRETTO" if anc in dirette else ("INDIRETTO" if ks else "nessuna lettura")
        tramite = sorted(c for c in funz[anc] if any(nome.get(q) == c and porta.get(q) for q in funz))
        print("  %-36s %-58s %-9s %-28s %s" % (desc, anc, dd, ", ".join(sorted(ks)), ("tramite " + ", ".join(tramite[:6])) if tramite else ""))
    # ### le letture (1)-(3) della carta
    def raggiunge(anc, k):
        return k in porta.get(anc, set())
    l1 = raggiunge("primo_ordine/flussi_parziali.py::hop_psi", "cs") and raggiunge("primo_ordine/motore.py::Motore._moneta_spin", "cs") and TABELLA["primo_ordine/flussi_parziali.py::dtau_nodo"][1] == SI
    deriva = [a for a in ("csv/_u1_prototipo.py::Campo.deriva", "csv/solitone/u1_generico.py::CampoGenerico.deriva") if a in funz]
    l2 = all("w" in porta.get(a, set()) and "cs" not in porta.get(a, set()) for a in deriva) and not any(
        "s_a" in dirette.get(q, {}) for q in dirette if q.startswith("doc/referti_l2/chi_tick.py"))
    l3 = "dtau" in dirette.get("doc/referti_l2/chi_tick.py::tick_chi", {}) and "c2" in dirette.get("doc/referti_l2/chi_tick.py::forza", {}) and TABELLA["doc/referti_l2/chi_tick.py::Parametri.__init__"][1] == NO
    l1phi = raggiunge("primo_ordine/flussi_parziali.py::hop_phi", "cs")
    print("-" * 140)
    print("### (1) la materia segue N (lo spostamento e la moneta raggiungono cs, dtau_nodo = dtau cs): %s" % ("CONFERMATA" if l1 else "### NON confermata"))
    print("    e il vuoto phi (lo spostamento del vuoto raggiunge cs): %s" % ("SI'" if l1phi else "NO"))
    print("### (2) la luce non sente N (la deriva legge w e non cs; nessuna riga di chi_tick tocca s_a): %s" % ("CONFERMATA" if l2 else "### NON confermata"))
    print("### (3) chi non sente il proprio N (tick_chi legge dtau, la forza c2 costante): %s" % ("CONFERMATA" if l3 else "### NON confermata"))
    if fuori:
        print("### ALZA: %d funzioni DIRETTE NON IN TABELLA: %s" % (len(fuori), fuori))
    print("=" * 140)
    return 1 if fuori else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
