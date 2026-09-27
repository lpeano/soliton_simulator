# -*- coding: utf-8 -*-
"""**`T2` (i tipi) — IL TIPO DICHIARATO E' COERENTE CON CIO' CHE LA FUNZIONE SCRIVE?**

**Che cosa certifica:** che `_PASSO_TIPI` **non sia una dichiarazione a vuoto**. Per ogni voce del
registro si guarda **che cosa la funzione scrive DAVVERO** *(AST, ricorsivo sulle chiamate a metodi
di `Rete`)* e si confronta col tipo dichiarato.

**LE REGOLE, quelle che Luca ha chiesto piu' quelle che servono per chiudere la tabella:**

| tipo | deve scrivere |
|---|---|
| `osservatore` | ### **NESSUNO stato fisico, NESSUNA struttura, NESSUN `pos`** (solo contatori/tracce) |
| `disegno` | ### **solo `pos`** (e nessuno stato fisico) |
| `fase` | **solo lo snapshot** (`_smp_d0`, `_smp_d`): non e' una legge |
| `vincolo` | stato fisico, **ma solo applicando un limite al valore corrente** |
| `dinamica` | stato fisico, e **NON** struttura |
| `AMBIGUA` | ### **struttura E stato insieme** -- se non fosse cosi', l'ambiguita' non ci sarebbe |

**⚠ E il limite (`A9`), lo stesso della FASE 0:** analisi **statica e per nome**. Un alias o un
`getattr` non si vedono, e un ramo mai eseguito conta. ### **Quindi questo certifica la COERENZA
DELLA DICHIARAZIONE, non il comportamento.** Chi certifica il comportamento e' `H-ETC-2`.

COMANDO:  python csv/_seal_fork/_sig_sched_t2b.py
USCITA:   0 se tutte le voci sono coerenti, 1 altrimenti.
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

SIM = os.path.join(RADICE, "soliton_simulator.py")
SRC = io.open(SIM, encoding="utf-8").read()
ARB = ast.parse(SRC)
BLOB = hashlib.sha1(io.open(SIM, "rb").read()).hexdigest()

STATO = ("d", "d0", "phi", "phi_s", "phivel", "psi", "psi_spin", "_psi_spinor", "_psi_prec",
         "_spinor_lift", "omega_s", "_nb", "_nb_prec", "eta", "tw", "twp", "vd", "peq",
         "mem_mot", "perc_chi", "perc_geom")
STRUTTURA = ("i", "j", "n", "conc_nodi", "conc_archi", "_rep", "perc_tw", "phi0")
SNAPSHOT = ("_smp_d0", "_smp_d")
VINCOLO_FN = ("_pav_d0", "_smorza", "_sd0", "_nasce", "satura", "_dphi")

METODI, FUNZIONI = {}, {}
for _n in ast.walk(ARB):
    if isinstance(_n, ast.ClassDef) and _n.name == "Rete":
        for _k in _n.body:
            if isinstance(_k, (ast.FunctionDef, ast.AsyncFunctionDef)):
                METODI[_k.name] = _k
for _n in ARB.body:
    if isinstance(_n, ast.FunctionDef):
        FUNZIONI[_n.name] = _n


def _lit(nome):
    """Il valore di un `dict`/`frozenset` di modulo, letto dall'AST (non si importa il modulo)."""
    for n in ARB.body:
        if isinstance(n, ast.Assign):
            for b in n.targets:
                if isinstance(b, ast.Name) and b.id == nome:
                    try:
                        return ast.literal_eval(n.value)
                    except Exception:
                        if isinstance(n.value, ast.Call):   # frozenset((...))
                            return set(ast.literal_eval(n.value.args[0]))
                        raise
    raise SystemExit("[t2b] `%s` non si trova in %s" % (nome, SIM))


def _radice(n):
    while isinstance(n, (ast.Attribute, ast.Subscript)):
        n = n.value
    return n.id if isinstance(n, ast.Name) else None


def _attr(n):
    while isinstance(n, ast.Subscript):
        n = n.value
    return n.attr if isinstance(n, ast.Attribute) else None


def scrive(nome, visti=None):
    """Gli attributi che `nome` scrive, seguendo le chiamate. `(attributi, vincolate)`."""
    visti = visti or set()
    if nome in visti:
        return set(), set()
    visti = visti | {nome}
    c = METODI.get(nome) or FUNZIONI.get(nome)
    if c is None:
        return set(), set()
    rice = "self" if nome in METODI else "net"
    attr, vinc, chiam = set(), set(), set()
    for n in ast.walk(c):
        bers = []
        if isinstance(n, ast.Assign):
            bers = [(x, n.value) for x in n.targets]
        elif isinstance(n, ast.AugAssign):
            bers = [(n.target, n.value)]
        for b, val in bers:
            if _radice(b) != rice:
                continue
            a = _attr(b)
            if not a or a.startswith("__"):
                continue
            attr.add(a)
            testo = ""
            try:
                testo = ast.unparse(val) if val is not None else ""
            except Exception:
                pass
            if (any(v in testo for v in VINCOLO_FN) or "np.maximum" in testo
                    or "np.clip" in testo or "%" in testo):
                vinc.add(a)
        if isinstance(n, ast.Call):
            f = n.func
            nm = f.attr if isinstance(f, ast.Attribute) else (
                f.id if isinstance(f, ast.Name) else None)
            if nm and (nm in METODI or nm in FUNZIONI):
                chiam.add(nm)
    for k in chiam:
        a2, v2 = scrive(k, visti)
        attr |= a2
        vinc |= v2
    return attr, vinc


def principale():
    TIPI = _lit("_PASSO_TIPI")
    REG = _lit("_PASSO_REGISTRO")
    FASI = _lit("_PASSO_FASI")
    print("simulatore blob sha1-BYTE %s" % BLOB[:8])
    print("registro: %d voci   tipi dichiarati: %d" % (len(REG), len(TIPI)))
    senza = sorted(set(REG) - set(TIPI))
    extra = sorted(set(TIPI) - set(REG))
    if senza or extra:
        print("### REGISTRO E TIPI DIVERGENTI: senza tipo %s, tipi in piu' %s" % (senza, extra))
        return 1
    print("")
    print("  %-24s %-13s %-8s %s" % ("voce", "tipo", "esito", "che cosa SCRIVE"))
    righe, falliti = [], 0
    for voce in sorted(REG):
        fn = FASI.get(voce, voce)
        attr, vinc = scrive(fn)
        st = sorted(set(attr) & set(STATO))
        sr = sorted(set(attr) & set(STRUTTURA))
        sn = sorted(set(attr) & set(SNAPSHOT))
        ds = ["pos"] if "pos" in attr else []
        tipo = TIPI[voce]
        motivo = None
        if tipo == "osservatore":
            if st or sr or ds:
                motivo = "un `osservatore` NON deve scrivere stato/struttura/pos: %s" % (st + sr + ds)
        elif tipo == "disegno":
            if st or sr:
                motivo = "un `disegno` deve scrivere SOLO `pos`, e scrive anche %s" % (st + sr)
            elif not ds:
                motivo = "un `disegno` deve scrivere `pos`, e non lo scrive"
        elif tipo == "fase":
            if st or sr or ds:
                motivo = "una `fase` deve scrivere solo lo snapshot, e scrive %s" % (st + sr + ds)
            elif not sn:
                motivo = "una `fase` deve scrivere lo snapshot, e non lo scrive"
        elif tipo == "vincolo":
            if not st:
                motivo = "un `vincolo` deve scrivere stato, e non lo scrive"
            elif not (set(st) & set(vinc)):
                motivo = "un `vincolo` deve scrivere applicando un LIMITE, e %s non lo fa" % st
        elif tipo == "dinamica":
            if not st:
                motivo = "una `dinamica` deve scrivere stato, e non lo scrive"
            elif sr:
                motivo = "una `dinamica` NON deve scrivere struttura, e scrive %s" % sr
        elif tipo == "AMBIGUA":
            if not (st and sr):
                motivo = ("`AMBIGUA` significa struttura E stato: qui stato=%s struttura=%s, "
                          "quindi l'ambiguita' NON c'e' piu' e il tipo va cambiato" % (st, sr))
        else:
            motivo = "tipo SCONOSCIUTO: %r" % tipo
        ok = motivo is None
        falliti += 0 if ok else 1
        print("  %-24s %-13s %-8s stato=%d struttura=%d pos=%d snapshot=%d"
              % (voce, tipo, "ok" if ok else "### NO", len(st), len(sr), len(ds), len(sn)))
        if motivo:
            print("      %s" % motivo)
        righe.append({"voce": voce, "funzione": fn, "tipo": tipo, "coerente": ok,
                      "motivo": motivo, "stato": st, "struttura": sr, "pos": bool(ds),
                      "snapshot": sn})
    print("")
    print("=" * 78)
    if falliti:
        print("### %d VOCI NON COERENTI: il tipo dichiarato non e' quello che la funzione fa." % falliti)
    else:
        print("### TUTTE E %d LE VOCI SONO COERENTI col codice di oggi." % len(righe))
    print("=" * 78)
    OUT = os.path.join(_QUI, "_sig_sched_tipi.json")
    io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(json.dumps(
        {"blob_sim": BLOB, "registro": sorted(REG), "tipi": TIPI, "righe": righe,
         "non_coerenti": falliti, "passa": not falliti}, indent=1, ensure_ascii=False,
        sort_keys=True))
    print("")
    print("scritto: " + OUT)
    return 1 if falliti else 0


if __name__ == "__main__":
    sys.exit(principale())
