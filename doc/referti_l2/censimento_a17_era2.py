# -*- coding: utf-8 -*-
r"""**IL CENSIMENTO A17 DELL'ERA 2: CHI LEGGE LA GEOMETRIA** *(il mandato di Luca `2026-11-21` `22:12` e l'aggiunta: T0; la carta `doc/TASK_HISTORY/2026-11-21_orientamento_combinatorio.md`, sez. `2.2`; sul modello di `csv/_test_fork/_censimento_pos.py`, `A17`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/censimento_a17_era2.py --radice C:\Users\lpeano\wt_mitosi_chi > doc/referti_l2/degenere_diagnosi_parte2.txt

**IL METODO** *(dichiarato prima dei risultati)*:
1. nell'AST dei file del cammino delle due corse *(il ramo `mitosi` e il ramo `mitosi-chi`: `--radice` e' l'albero da leggere; i file che mancano si dicono)* **si cercano le LETTURE** di: **`vec`** *(l'attributo `.vec`, il nome `vec`, la chiave `"campo_vec"`)*, **`geo.n`** *(`.geo.n`, la chiave `"geo_n"`, `Geometria(`)*, **le posizioni** *(`Z["m1"]`, `Z["m2"]`, `raggi(`, `centro_di(`, `scarti(`)*; con il file, la riga, la funzione;
2. **DIRETTO** = la funzione stessa legge; **INDIRETTO** = chiama *(per NOME semplice)* una funzione che legge, chiudendo il grafo delle chiamate su tutti i file letti. ### **Il nome semplice e' una SOVRA-approssimazione** *(due funzioni con lo stesso nome si confondono)*: dichiarato;
3. **«decide fisica si'/no»** e' un CAMPO scritto a mano in `TABELLA`, per funzione DIRETTA, col perche' *(DECISIONE-VUOLE-UN-CAMPO)*: **lo strumento TROVA, la tabella DICE; una funzione DIRETTA fuori tabella fa ALZARE lo strumento** *(uscita `1`, dopo aver stampato tutto)*;
4. **le ANCORE della fisica** *(il passo, l'energia, la regola)*: per ognuna, se e attraverso che cosa raggiunge una lettura;
5. **LA REGOLA DEL FERMO** *(la carta sez. `2.2`)*: una funzione che decide fisica e legge `geo.n` o le posizioni, oltre all'orientamento delle placchette.
### ⚠ **CIO' CHE NON VEDE:** un alias *(`n = self.geo.n` passato altrove)*, una chiamata per variabile; il censimento e' **per DIFETTO** sulle letture e **per ECCESSO** sull'indiretto.
"""
import argparse
import ast
import os
import sys

FILES = [
    "primo_ordine/motore.py", "primo_ordine/tick.py", "primo_ordine/flussi_parziali.py", "primo_ordine/energia_pesata.py", "primo_ordine/energia.py",
    "primo_ordine/corrente.py", "primo_ordine/crescita_dati.py", "primo_ordine/checkpoint.py", "primo_ordine/segno.py", "primo_ordine/composizione.py",
    "csv/solitone/u1_generico.py", "csv/solitone/posizioni.py", "csv/solitone/contatore.py", "csv/solitone/conti.py", "csv/solitone/_u1_oggi.py",
    "csv/solitone/p6_u_breve.py", "csv/solitone/porto.py", "csv/solitone/mattone.py", "csv/solitone/tick_lapse.py", "csv/_u1_prototipo.py", "csv/_libro_dei_conti.py",
    "doc/referti_l2/mitosi_regola.py", "doc/referti_l2/mitosi_corsa.py", "doc/referti_l2/mitosi_lunga.py", "doc/referti_l2/mitosi_rami.py",
    "doc/referti_l2/controllo_senza_bordo.py", "doc/referti_l2/chi_tick.py", "doc/referti_l2/chi_mattone_v2.py", "doc/referti_l2/chi_tronco.py",
    "doc/referti_l2/mitosi_chi_v4.py",
]
TERMINI = "primo_ordine/termini"

# ### LA TABELLA: per funzione DIRETTA, (decide fisica, il perche'). ### Scritta a mano, letta dallo strumento.
SI, NO = "SI", "NO"
TABELLA = {
    "primo_ordine/motore.py::Motore.cresci": (NO, "segue la crescita: i versori dei nati entrano nello stato (trasporto, non decisione)"),
    "primo_ordine/motore.py::Motore._moneta_spin": (SI, "LA MONETA DI SPIN del passo (CAMM-MONETA-SPIN, due volte nell'ordine): exp(-i ang sigma.n)"),
    "primo_ordine/motore.py::Motore._ruota_attorno_a_n": (SI, "la rotazione exp(-i ang sigma.n) della moneta: i versori sono l'ASSE"),
    "primo_ordine/motore.py::Motore.elicita": (SI, "h = s.n per nodo: il termine eps h dell'energia pesata (la scelta del flip, la Q di chi, E_persa)"),
    "primo_ordine/corrente.py::_scena": (NO, "una scena di collaudo"),
    "primo_ordine/crescita_dati.py::geometria": (NO, "copia i versori dei nati (iniziali['geo_n']): trasporto"),
    "primo_ordine/checkpoint.py::riprendi": (NO, "la ripresa: rimette i versori salvati"),
    "primo_ordine/checkpoint.py::main": (NO, "un collaudo"),
    "primo_ordine/segno.py::_coniugato": (NO, "l'operatore coniugato per la prova del segno (collaudo)"),
    "csv/solitone/u1_generico.py::CampoGenerico.__init__": (NO, "memorizza i vettori d'arco"),
    "csv/solitone/u1_generico.py::CampoGenerico._placchetta": (SI, "L'ORIENTAMENTO DELLE PLACCHETTE (il verso del giro, la sorgente, i segni del flusso di A): l'oggetto della cura (a)"),
    "csv/solitone/u1_generico.py::CampoGenerico.cresci": (NO, "segue la crescita: i vettori d'arco dei nati"),
    "csv/solitone/u1_generico.py::_verso": (NO, "il vettore d'arco col verso: lo legge _placchetta"),
    "csv/solitone/posizioni.py::cresci": (NO, "le posizioni dei nati (B4): disegno e misure"),
    "csv/solitone/conti.py::etichette": (NO, "le etichette delle misure (il nodo piu' vicino ai centri)"),
    "csv/solitone/conti.py::moto": (NO, "una misura del moto del centro"),
    "csv/solitone/p6_u_breve.py::main": (NO, "uno script di prova"),
    "csv/solitone/porto.py::metti_bordo": (NO, "il bordo (r_c0 -> g_e): nelle corse senza bordo g_e e' azzerato subito dopo (controllo_senza_bordo.riprendi, mitosi_lunga.riprendi)"),
    "csv/solitone/porto.py::r_ogg": (NO, "la misura di R_ogg"),
    "csv/solitone/porto.py::cuoci": (NO, "la cottura del mattone (non nel cammino delle due corse)"),
    "csv/solitone/porto.py::francobollo_L324": (NO, "la preparazione di un francobollo (non nel cammino)"),
    "csv/solitone/porto.py::corsa": (NO, "un'altra corsa (non nel cammino)"),
    "csv/solitone/mattone.py::centro_di": (NO, "il centro della materia: misure ed etichette"),
    "csv/solitone/mattone.py::distanza": (NO, "una misura"),
    "csv/solitone/mattone.py::ritaglia": (NO, "il ritaglio del mattone alla preparazione (k 0)"),
    "csv/solitone/mattone.py::prepara.misura": (NO, "una misura della preparazione"),
    "csv/solitone/mattone.py::controllo": (NO, "un controllo"),
    "csv/_u1_prototipo.py::energia": (SI, "un'ENERGIA: il termine della moneta EPS_MONETA s_n s.n con i versori"),
    "doc/referti_l2/mitosi_regola.py::indici_nascita": (SI, "QUALE vicino comune e' k (a sinistra di i -> j): un prodotto vettoriale sui vettori d'arco; se e' 0 sceglie in silenzio"),
    "doc/referti_l2/mitosi_regola.py::_v": (NO, "il vettore d'arco col verso: lo usa candidato"),
    "doc/referti_l2/mitosi_regola.py::candidato": (SI, "i vettori d'arco e i versori del CANDIDATO: le sue placchette, la sua energia (l'elicita' coi versori nati) -> la SCELTA del flip"),
    "doc/referti_l2/mitosi_regola.py::applica": (NO, "un controllo (ok_geo)"),
    "doc/referti_l2/mitosi_regola.py::caso": (NO, "la prova"),
    "doc/referti_l2/mitosi_corsa.py::p6": (NO, "la prova"),
    "doc/referti_l2/mitosi_corsa.py::campo_generico": (NO, "i vettori d'arco del toro a k 0 dal reticolo regolare (a1, a2, a1 + a2): la sorgente UNA volta, come il mandato permette"),
    "doc/referti_l2/chi_tick.py::parametri": (SI, "KAPPA si tara sul nodo piu' vicino (per POSIZIONE) al centro della materia di C2: una posizione sceglie il nodo che fissa una costante"),
    "doc/referti_l2/mitosi_lunga.py::raggi": (NO, "le distanze dal centro: misure"),
    "doc/referti_l2/mitosi_lunga.py::Nascite.nasci": (NO, "la posizione del nato nel bilancio (registro)"),
    "doc/referti_l2/mitosi_lunga.py::salva": (NO, "salva lo stato"),
    "doc/referti_l2/mitosi_lunga.py::riprendi": (NO, "riprende lo stato"),
    "doc/referti_l2/mitosi_lunga.py::stato_di": (NO, "fotografa lo stato (le prove)"),
    "doc/referti_l2/mitosi_lunga.py::misure_su": (NO, "le misure"),
    "doc/referti_l2/mitosi_lunga.py::nasce": (NO, "la prova"),
    "doc/referti_l2/mitosi_lunga.py::corsa": (NO, "le misure (gli anelli, il centro, la sorgente dei passi D1)"),
    "doc/referti_l2/mitosi_rami.py::Rami.nasci": (NO, "il luogo della nascita (D3): registro"),
    "doc/referti_l2/mitosi_rami.py::Rami.centro_materia": (NO, "il centro: la sorgente dei passi (misura)"),
    "doc/referti_l2/mitosi_rami.py::salva": (NO, "salva lo stato"),
    "doc/referti_l2/mitosi_rami.py::ciclo": (NO, "le misure (anelli, centro, D1, E1)"),
    "doc/referti_l2/controllo_senza_bordo.py::Misure.__init__": (NO, "le misure"),
    "doc/referti_l2/controllo_senza_bordo.py::corsa": (NO, "il centro delle misure"),
    "doc/referti_l2/controllo_senza_bordo.py::caso.venti": (NO, "la prova"),
    "doc/referti_l2/controllo_senza_bordo.py::costo": (NO, "la misura del costo"),
    "doc/referti_l2/chi_mattone_v2.py::corsa": (NO, "le misure per anello"),
    "doc/referti_l2/chi_tronco.py::corsa": (NO, "le misure per anello"),
    "doc/referti_l2/mitosi_chi_v4.py::ciclo": (NO, "le misure (anelli, centro, D1, E1)"),
    "doc/referti_l2/mitosi_chi_v4.py::ciclo.rigeometria": (NO, "i raggi per le misure per anello"),
    "doc/referti_l2/mitosi_chi_v4.py::NascitaChi.nasci": (NO, "il luogo della nascita (D3): registro"),
    "doc/referti_l2/mitosi_chi_v4.py::salva": (NO, "salva lo stato"),
    "doc/referti_l2/mitosi_chi_v4.py::stato_di": (NO, "fotografa lo stato (le prove)"),
    "doc/referti_l2/mitosi_chi_v4.py::nascite": (NO, "la prova (la scelta dell'arco forzato per raggio)"),
}
ANCORE = [
    ("il passo: la moneta di spin", "primo_ordine/motore.py::Motore._moneta_spin"),
    ("il passo: i pezzi della tabella", TERMINI + "/*"),
    ("l'energia pesata (il conto di chi, la Q)", "primo_ordine/energia_pesata.py::termini_di_h"),
    ("il conto della corsa (la mitosi)", "csv/_libro_dei_conti.py::conti_per_nodo"),
    ("la regola: il candidato", "doc/referti_l2/mitosi_regola.py::candidato"),
    ("la regola: la scelta", "doc/referti_l2/mitosi_regola.py::regola"),
    ("la regola: applica", "doc/referti_l2/mitosi_regola.py::applica"),
    ("chi: la sorgente Q", "doc/referti_l2/chi_tick.py::Q_di"),
    ("chi: l'energia", "doc/referti_l2/chi_tick.py::energia_chi"),
    ("chi: il tick", "doc/referti_l2/chi_tick.py::tick_chi"),
    ("chi: la regola col suo H", "doc/referti_l2/mitosi_chi_v4.py::regola_chi"),
]


def tipo(node):
    if isinstance(node, ast.Attribute):
        if node.attr == "vec":
            return "vec"
        if node.attr == "n" and isinstance(node.value, ast.Attribute) and node.value.attr == "geo":
            return "geo.n"
    if isinstance(node, ast.Name) and node.id == "vec" and isinstance(node.ctx, ast.Load):
        return "vec"
    if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant) and node.slice.value in ("m1", "m2", "geo_n", "campo_vec"):
        return {"m1": "pos", "m2": "pos", "geo_n": "geo.n", "campo_vec": "vec"}[node.slice.value]
    if isinstance(node, ast.Call):
        f = node.func
        nm = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else None)
        if nm in ("raggi", "centro_di", "scarti"):
            return "pos"
        if nm == "Geometria":
            return "geo.n"
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
    src = open(os.path.join(radice, p), encoding="utf-8").read()
    t = ast.parse(src)
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
    ap.add_argument("--radice", default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    x = ap.parse_args(argv)
    R = x.radice
    files = list(FILES) + sorted(TERMINI + "/" + f for f in os.listdir(os.path.join(R, TERMINI)) if f.endswith(".py"))
    print("=" * 140)
    print("IL CENSIMENTO A17 DELL'ERA 2 (Luca 2026-11-21 22:12, l'aggiunta; la carta sez. 2.2): la radice %s, %d file" % (R, len(files)))
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
    # ### DIRETTO
    dirette = {}
    for p, riga, fn, k in letture:
        dirette.setdefault(p + "::" + fn, {}).setdefault(k, []).append(riga)
    # ### INDIRETTO: per nome semplice, chiuso
    nome = {q: q.split("::")[1].split(".")[-1] for q in funz}
    porta = {q: set(v) for q, v in dirette.items()}
    cambia = True
    while cambia:
        cambia = False
        per_nome = {}
        for q, ks in porta.items():
            per_nome.setdefault(nome.get(q, q.split("::")[1].split(".")[-1]), set()).update(ks)
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
        dec = TABELLA.get(q)
        if dec is None:
            fuori.append(q)
        print("  %-70s %-40s decide fisica: %-3s %s" % (q, ", ".join("%s r.%s" % (k, ",".join(map(str, sorted(set(v))))) for k, v in sorted(dirette[q].items())),
                                                         dec[0] if dec else "###", dec[1] if dec else "### NON IN TABELLA"))
    print("### LE ANCORE DELLA FISICA (raggiunge una lettura? DIRETTO o INDIRETTO, per nome semplice):")
    for desc, anc in ANCORE:
        if anc.endswith("/*"):
            qs = [q for q in funz if q.startswith(anc[:-1])]
            ks = set().union(*[porta.get(q, set()) for q in qs]) if qs else set()
            via = sorted(q.split("::")[1] for q in qs if porta.get(q))
            print("  %-45s %-55s %s %s" % (desc, anc, ", ".join(sorted(ks)) or "nessuna", ("(" + ", ".join(via[:6]) + ")") if via else ""))
            continue
        if anc not in funz:
            print("  %-45s %-55s ### NON TROVATA in questa radice" % (desc, anc))
            continue
        ks = porta.get(anc, set())
        dd = "DIRETTO" if anc in dirette else ("INDIRETTO" if ks else "")
        tramite = sorted(c for c in funz[anc] if any(nome.get(q) == c and porta.get(q) for q in funz) or any(q.endswith("." + c) or q.endswith("::" + c) for q in dirette))
        print("  %-45s %-55s %s %s %s" % (desc, anc, dd, ", ".join(sorted(ks)) or "nessuna", ("tramite " + ", ".join(tramite[:8])) if tramite and dd == "INDIRETTO" else ""))
    # ### LA REGOLA DEL FERMO
    scatta = [(q, sorted(dirette[q])) for q in sorted(dirette) if TABELLA.get(q, (None,))[0] == SI and (set(dirette[q]) & {"geo.n", "pos"})]
    altro_vec = [q for q in sorted(dirette) if TABELLA.get(q, (None,))[0] == SI and q != "csv/solitone/u1_generico.py::CampoGenerico._placchetta" and "vec" in dirette[q]]
    print("-" * 140)
    print("### LA REGOLA DEL FERMO (una funzione che decide fisica legge geo.n o le posizioni): %s" % ("SCATTA: %s" % scatta if scatta else "non scatta"))
    print("### i vettori d'arco decidono fisica anche FUORI da _placchetta: %s" % (altro_vec or "no"))
    if fuori:
        print("### ALZA: %d funzioni DIRETTE NON IN TABELLA: %s" % (len(fuori), fuori))
    print("=" * 140)
    return 1 if fuori else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
