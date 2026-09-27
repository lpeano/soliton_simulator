# -*- coding: utf-8 -*-
"""**SCHEDULATORE DEL PASSO: i tre inventari che il piano richiede.**

**Mandato di Luca del 2026-09-27** *(il passo pieno diventa uno SCHEDULATORE)*: prima del codice,
**solo analisi e piano**. Questo strumento produce **i dati**, il piano sta in
`doc/PIANO_schedulatore_passo.md`.

**① IL TIPO DI OGNI FUNZIONE del passo**, dedotto da **cio' che scrive**, non da come si chiama:

| tipo | criterio |
|---|---|
| `disegno` | scrive **solo `pos`** *(ed eventuali cache di rendering)* |
| `osservatore` | **non scrive stato**: solo contatori `_g_*` / `_*_log` / niente |
| `strutturale` | scrive la **STRUTTURA** (`i`, `j`, `n`, `conc_*`) o **estende** array |
| `vincolo` | scrive stato **solo** applicando un limite al valore corrente *(`_pav_*`, `_smorza`, wrap, normalizzazione)* |
| `dinamica` | scrive stato fisico in altro modo |
| ### `AMBIGUA` | scrive **struttura E stato fisico**, oppure `pos` **e** stato fisico |

**② CHE COSA SCRIVE OGNI LEGGE, e se puo' diventare <<restituisce variazioni>>**: si riusa la
classificazione della FASE 0-bis *(`A` incremento, `A-bis` mescola, `S` estensione, `C`
assegnazione indipendente, `B` vincolo)*, ricalcolata sul blob di oggi.

**③ TUTTE LE LETTURE DI `pos` NELLE LEGGI FISICHE**, con riga e sorgente: e' il lavoro di `T4`.
**Il criterio di <<legge fisica>>:** la funzione **non** e' di tipo `disegno`.

**⚠ I LIMITI (`A9`), gli stessi della FASE 0:** analisi **statica e per nome**. Alias, `getattr` e
rami mai eseguiti non si vedono; un tipo dedotto dalle scritture **statiche** puo' sbagliare su una
funzione che scrive tramite un alias. **Quindi i tipi sono una PROPOSTA da confermare leggendo, non
un verdetto**, e le `AMBIGUA` sono esattamente quelle che il mandato chiede di segnalare.

COMANDO:  python csv/_test_fork/_etc_schedulatore.py
"""
import ast
import hashlib
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)
import _passo  # noqa: E402

SIM = os.path.join(RADICE, "soliton_simulator.py")
SRC = io.open(SIM, encoding="utf-8").read()
RIG = SRC.split(chr(10))
ARB = ast.parse(SRC)
BLOB = hashlib.sha1(io.open(SIM, "rb").read()).hexdigest()

STATO = ["d", "d0", "phi", "phi_s", "phivel", "psi", "psi_spin", "_psi_spinor", "_psi_prec",
         "_spinor_lift", "omega_s", "_nb", "_nb_prec", "eta", "tw", "twp", "vd", "peq",
         "mem_mot", "perc_chi", "perc_geom"]
STRUTTURA = ["i", "j", "n", "conc_nodi", "conc_archi", "_rep", "perc_tw", "phi0", "nati",
             "negate", "coppie_nate"]
DISEGNO = ["pos"]
VINCOLO_FN = ("_pav_d0", "_floor_d0", "_smorza", "_sd0", "_nasce", "_smp_chiudi", "satura")

METODI, FUNZIONI = {}, {}
for _n in ast.walk(ARB):
    if isinstance(_n, ast.ClassDef) and _n.name == "Rete":
        for _k in _n.body:
            if isinstance(_k, (ast.FunctionDef, ast.AsyncFunctionDef)):
                METODI[_k.name] = _k
for _n in ARB.body:
    if isinstance(_n, ast.FunctionDef):
        FUNZIONI[_n.name] = _n


def corpo(nome):
    return METODI.get(nome) or FUNZIONI.get(nome)


def _radice(n):
    while isinstance(n, (ast.Attribute, ast.Subscript)):
        n = n.value
    return n.id if isinstance(n, ast.Name) else None


def _attr(n):
    while isinstance(n, ast.Subscript):
        n = n.value
    return n.attr if isinstance(n, ast.Attribute) else None


def raggiungibili(leggi):
    visti, coda = set(), list(leggi)
    while coda:
        x = coda.pop()
        if x in visti:
            continue
        visti.add(x)
        c = corpo(x)
        if c is None:
            continue
        for n in ast.walk(c):
            if isinstance(n, ast.Call):
                f = n.func
                nm = f.attr if isinstance(f, ast.Attribute) else (
                    f.id if isinstance(f, ast.Name) else None)
                if nm and (nm in METODI or nm in FUNZIONI) and nm not in visti:
                    coda.append(nm)
    return visti


def scritture(nome):
    """Gli attributi che il CORPO di `nome` scrive, con la forma. Non ricorsivo."""
    c = corpo(nome)
    if c is None:
        return []
    rice = "self" if nome in METODI else "net"
    out = []
    for n in ast.walk(c):
        bersagli = []
        if isinstance(n, ast.Assign):
            bersagli = [(x, "[]=" if isinstance(x, ast.Subscript) else "=", n.value)
                        for x in n.targets]
        elif isinstance(n, ast.AugAssign):
            bersagli = [(n.target, "[]+=" if isinstance(n.target, ast.Subscript) else "+=",
                         n.value)]
        for b, forma, val in bersagli:
            if _radice(b) != rice:
                continue
            a = _attr(b)
            if not a or a.startswith("__"):
                continue
            testo = ""
            try:
                testo = ast.unparse(val) if val is not None else ""
            except Exception:
                pass
            out.append({"attributo": a, "forma": forma, "riga": b.lineno,
                        "vincolo": any(v in testo for v in VINCOLO_FN)
                                   or ("% self._dphi()" in testo) or ("np.maximum" in testo[:14])
                                   or ("np.clip" in testo[:10]),
                        "sorgente": RIG[b.lineno - 1].strip()[:110]})
    return out


def tipo_di(nome):
    """Il TIPO proposto, dedotto da cio' che la funzione SCRIVE."""
    W = scritture(nome)
    attr = {w["attributo"] for w in W}
    st = attr & set(STATO)
    sr = attr & set(STRUTTURA)
    ds = attr & set(DISEGNO)
    altro = attr - st - sr - ds
    diag = {a for a in altro if a.startswith("_g_") or a.endswith("_log")
            or a.startswith("_ritmo_") or a.startswith("_calcpsi")}
    if not st and not sr and not ds:
        return ("osservatore", W, sorted(attr), sorted(diag))
    if ds and (st or sr):
        return ("AMBIGUA", W, sorted(attr), sorted(diag))
    if ds:
        return ("disegno", W, sorted(attr), sorted(diag))
    if sr and st:
        return ("AMBIGUA", W, sorted(attr), sorted(diag))
    if sr:
        return ("strutturale", W, sorted(attr), sorted(diag))
    if st and all(w["vincolo"] for w in W if w["attributo"] in st):
        return ("vincolo", W, sorted(attr), sorted(diag))
    return ("dinamica", W, sorted(attr), sorted(diag))


LEGGI = [n for _t, n in _passo.ordine()]
VIVE = sorted(raggiungibili(LEGGI))
print("simulatore blob sha1-BYTE %s" % BLOB[:8])
print("le cinque leggi: " + " -> ".join(LEGGI))
print("funzioni eseguite nel passo pieno: %d" % len(VIVE))
print("")

# ------------------------------------------------------------------ ① i tipi
TIPI = {}
for nome in VIVE:
    t, W, attr, diag = tipo_di(nome)
    TIPI[nome] = {"tipo": t, "scrive": attr, "n_scritture": len(W),
                  "solo_diagnostici": sorted(diag),
                  "siti": sorted(W, key=lambda x: x["riga"])}
CONTA = {}
for v in TIPI.values():
    CONTA[v["tipo"]] = CONTA.get(v["tipo"], 0) + 1
print("=" * 96)
print("(1) IL TIPO DI OGNI FUNZIONE DEL PASSO, dedotto da CIO' CHE SCRIVE")
print("=" * 96)
print("")
for k in ("dinamica", "vincolo", "strutturale", "disegno", "osservatore", "AMBIGUA"):
    print("  %-14s %3d" % (k, CONTA.get(k, 0)))
print("")
for k in ("AMBIGUA", "dinamica", "vincolo", "strutturale", "disegno"):
    v = sorted(n for n in VIVE if TIPI[n]["tipo"] == k)
    if not v:
        continue
    print("  --- %s (%d)" % (k, len(v)))
    for n in v:
        print("      %-30s scrive: %s" % (n, ", ".join(TIPI[n]["scrive"])[:62]))
print("")
print("  --- osservatore (%d): %s"
      % (CONTA.get("osservatore", 0),
         ", ".join(sorted(n for n in VIVE if TIPI[n]["tipo"] == "osservatore"))[:300]))

# ------------------------------------------------------------------ ② le cinque leggi
print("")
print("=" * 96)
print("(2) LE CINQUE LEGGI: che cosa scrivono DIRETTAMENTE, e la forma delle scritture")
print("=" * 96)
print("")
FORME = {}
for nome in LEGGI:
    W = [w for w in scritture(nome) if w["attributo"] in STATO]
    per = {}
    for w in W:
        k = ("incremento" if w["forma"].endswith("+=")
             else "vincolo" if w["vincolo"] else "assegnazione")
        per[k] = per.get(k, 0) + 1
    FORME[nome] = {"tipo": TIPI[nome]["tipo"], "scritture_di_stato": len(W), "forme": per,
                   "attributi": sorted({w["attributo"] for w in W})}
    print("  %-24s %-12s scritture di STATO %3d   %s"
          % (nome, TIPI[nome]["tipo"], len(W),
             ", ".join("%s=%d" % (a, b) for a, b in sorted(per.items()))))
    print("      %s" % ", ".join(FORME[nome]["attributi"])[:88])

# ------------------------------------------------------------------ ③ le letture di pos
print("")
print("=" * 96)
print("(3) LE LETTURE DI `pos` NELLE LEGGI FISICHE  (il lavoro di T4)")
print("=" * 96)
POS = []
for nome in VIVE:
    if TIPI[nome]["tipo"] == "disegno":
        continue
    c = corpo(nome)
    if c is None:
        continue
    rice = "self" if nome in METODI else "net"
    scritte = {w["riga"] for w in scritture(nome) if w["attributo"] == "pos"}
    for n in ast.walk(c):
        if isinstance(n, ast.Attribute) and n.attr == "pos" and _radice(n) == rice:
            if n.lineno in scritte:
                continue
            POS.append({"funzione": nome, "tipo": TIPI[nome]["tipo"], "riga": n.lineno,
                        "sorgente": RIG[n.lineno - 1].strip()[:118]})
vis = set()
POSU = []
for p in POS:
    k = (p["funzione"], p["riga"])
    if k in vis:
        continue
    vis.add(k)
    POSU.append(p)
print("")
print("  letture di `pos` in funzioni NON di disegno: %d siti, in %d funzioni"
      % (len(POSU), len({p["funzione"] for p in POSU})))
print("")
print("  %-6s %-28s %-12s %s" % ("riga", "dentro", "tipo", "sorgente"))
for p in sorted(POSU, key=lambda x: x["riga"]):
    print("  :%-5d %-28s %-12s %s" % (p["riga"], p["funzione"], p["tipo"], p["sorgente"][:60]))

OUT = os.path.join(_QUI, "_etc_schedulatore.json")
io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(json.dumps(
    {"blob_sim": BLOB, "leggi": LEGGI, "funzioni": len(VIVE), "conta_tipi": CONTA,
     "tipi": TIPI, "forme_delle_cinque": FORME, "letture_pos": POSU},
    indent=1, ensure_ascii=False, sort_keys=True))
print("")
print("scritto: " + OUT)
