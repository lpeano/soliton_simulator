# -*- coding: utf-8 -*-
r"""**IL CONTROLLO DI `matrice` SUI REFERTI GIA' FATTI** *(UNA PROVA E UNA CORREZIONE DI STRUMENTO IN `csv/`, NESSUNA MODIFICA AL NUCLEO; il mandato di Luca delle `21:03` del `2026-10-31`;
[[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il task history `doc/TASK_HISTORY/2026-11-01_controllo_matrice.md`)*:
### **l'elenco AST di chi chiama `_dove_va_la_materia.matrice` (o `un_tick`, o una funzione che le chiama), con le righe che leggono lo stato DOPO la chiamata** *(la classe la do a mano, nel referto)*.

    python csv/_controllo_matrice.py --elenco > doc/referti_l2/controllo_matrice_elenco.txt
    python csv/_controllo_matrice.py --stato > doc/referti_l2/controllo_matrice_stato.txt
"""
import ast
import glob
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

SRC = "_dove_va_la_materia"
RADICI = ((SRC, "matrice"), (SRC, "un_tick"))   # ### un_tick: la causa; matrice la chiama (un'estensione dichiarata nel task history)
# ### le letture dello stato: `z["st"]`, e le misure che lo leggono (il task history, criterio 1); la riga si STAMPA, la classe si da' a mano
LETTURE = re.compile(r'\[\s*"st"\s*\]|\.st\b|\bst\s*\[|\bforma\s*\(|\bpunto\s*\(|\banelli\s*\(|\bdensita\s*\(|\bmisure\s*\(|baricentro|\bcarica\w*\s*\(|\bpartenza\w*\s*\(')


def moduli():
    mm = {}
    for f in sorted(glob.glob(os.path.join(_QUI, "*.py"))):
        n = os.path.basename(f)[:-3]
        testo = open(f, encoding="utf-8").read()
        mm[n] = (ast.parse(testo), testo.splitlines())
    return mm


def alias(tree):
    am = {}
    for nd in ast.walk(tree):
        if isinstance(nd, ast.Import):
            for a in nd.names:
                am[a.asname or a.name] = a.name
        elif isinstance(nd, ast.ImportFrom) and nd.module:
            for a in nd.names:
                am[a.asname or a.name] = (nd.module, a.name)
    return am


def bersaglio(c, n, am):
    """### **`(modulo, funzione)` di una chiamata**, risolti gli alias; `None` se non si risolve."""
    if isinstance(c.func, ast.Attribute) and isinstance(c.func.value, ast.Name):
        m = am.get(c.func.value.id)
        return (m, c.func.attr) if isinstance(m, str) else None
    if isinstance(c.func, ast.Name):
        m = am.get(c.func.id)
        return m if isinstance(m, tuple) else (n, c.func.id)
    return None


def funzioni(tree):
    return [x for x in ast.walk(tree) if isinstance(x, ast.FunctionDef)]


def chiusura(mm):
    """### **Le funzioni che chiamano le RADICI, transitivamente** *(punto fisso)*."""
    sp = set(RADICI)
    cambiato = True
    while cambiato:
        cambiato = False
        for n, (t, _r) in mm.items():
            am = alias(t)
            for fn in funzioni(t):
                if (n, fn.name) in sp:
                    continue
                if any(isinstance(c, ast.Call) and bersaglio(c, n, am) in sp for c in ast.walk(fn)):
                    sp.add((n, fn.name))
                    cambiato = True
    return sp


def elenco():
    mm = moduli()
    sp = chiusura(mm)
    print("=" * 130)
    print("IL CONTROLLO DI matrice (Luca 21:03): L'ELENCO -- chi chiama %s.matrice o %s.un_tick, anche transitivamente; le righe DOPO la chiamata che leggono lo stato" % (SRC, SRC))
    print("  le letture cercate (la regex): %s" % LETTURE.pattern)
    print("  ### la riga si stampa, la classe (PULITO / SOSPETTO) la do a mano nel referto")
    print("=" * 130)
    dirette, trans = [], []
    for n, (t, righe) in mm.items():
        am = alias(t)
        for fn in funzioni(t):
            fine = max(getattr(x, "end_lineno", fn.lineno) or fn.lineno for x in ast.walk(fn) if hasattr(x, "lineno"))
            for c in ast.walk(fn):
                if not isinstance(c, ast.Call):
                    continue
                b = bersaglio(c, n, am)
                if b not in sp or (n, fn.name) in RADICI:
                    continue
                dopo = [(i + 1, righe[i].strip()) for i in range(c.lineno, fine) if LETTURE.search(righe[i]) and not righe[i].strip().startswith("#")]
                (dirette if b in RADICI else trans).append((n, c.lineno, fn.name, b, dopo))
    for titolo, lista in (("### LE CHIAMATE DIRETTE (a matrice o un_tick)", dirette), ("### LE CHIAMATE TRANSITIVE (a una funzione che le chiama)", trans)):
        print(titolo)
        file_ = sorted(set(x[0] for x in lista))
        print("  %d chiamate in %d file" % (len(lista), len(file_)))
        for n, ln, fnome, b, dopo in sorted(lista):
            print("  %s.py:%d  %s -> %s.%s   (letture dopo, nella stessa funzione: %d)" % (n, ln, fnome, b[0], b[1], len(dopo)))
            for i, r in dopo:
                print("      %d: %s" % (i, r[:150]))
        print("-" * 130)
    print("### LE ALTRE FUNZIONI `matrice` (non %s.matrice: elencate, NON controllate; il task history, Cosa NON so)" % SRC)
    altre = sorted(n for n, (t, _r) in mm.items() if n != SRC and any(fn.name == "matrice" for fn in funzioni(t)))
    print("  %d: %s" % (len(altre), " ".join(altre)))
    print("=" * 130)


# ====================================================================== LO STATO: che cosa lascia matrice, e chi lo legge
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def istantanea(z):
    """### **ogni chiave di `z["st"]`**: gli array copiati, il resto per `repr`."""
    import numpy as np
    return {k: (np.array(v, copy=True) if isinstance(v, np.ndarray) else repr(v)) for k, v in z["st"].items()}


def confronta(a, b):
    """### **`{chiave: (uguale al bit, max |a - b|)}`**."""
    import numpy as np
    out = {}
    for k in sorted(set(a) | set(b)):
        x, y = a.get(k), b.get(k)
        if isinstance(x, np.ndarray) and isinstance(y, np.ndarray) and x.shape == y.shape:
            out[k] = (x.tobytes() == y.tobytes(), float(np.max(np.abs(x - y))) if x.size else 0.0)
        else:
            out[k] = (x == y if not isinstance(x, np.ndarray) and not isinstance(y, np.ndarray) else False, float("nan"))
    return out


def letture(z, phi0, rec, p, w_in):
    """### **i lettori dei siti dell'elenco, dopo aver ricaricato `p`:** `DC.forma`, `EL.densita`, `CL.punto`, `SL.anelli`, e lo sha1 dopo UN tick (`CL.avanza`)."""
    import _consolida_B as CO
    import _congelato_lungo as CL
    import _deriva_congelato as DC
    import _energia_del_legame as EL
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    LP = CO.CB.LP
    w0 = rec["larghezza"]
    z["st"]["psi_h"][...] = p
    out = {}
    with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
        f = DC.forma(z, w0)
        out["DC.forma (w, fr)"] = (f[0], f[1])
        rho, lam = EL.densita(z["inc"], z["st"])
        out["EL.densita (rho, lam)"] = (SFM.sha(rho), SFM.sha(lam))
        pt = CL.punto(z, 0, w_in, w0)
        out["CL.punto (w, f_win, f_3w0, picco, M)"] = tuple(pt[k] for k in ("w", "f_win", "f_3w0", "picco", "M"))
    ra, am = LP.SL.anelli(z, p, LP.FORMA)
    out["SL.anelli"] = (SFM.sha(ra), SFM.sha(am))
    with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
        CL.avanza(z, phi0, 1)
    out["un tick (CL.avanza): lo sha1 di psi_h"] = SFM.sha(z["st"]["psi_h"])
    return out


def stato():
    """### **(E1)** che chiavi cambia `matrice`; **(E2)** quali restano diverse dopo aver ricaricato `psi_h`; **(E3)** i lettori, con e senza `matrice` prima; **(E4)** `MB.misure` (il controllo positivo); **(E5)** un tick."""
    import _consolida_B as CO
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    CB = CO.CB
    MB = CB.MB
    print("=" * 130)
    print("IL CONTROLLO DI matrice (Luca 21:03): LO STATO -- la scena di _massimo_di_B.scena (N %.0e, L %d, eps %g), lo stato ricaricato = la p della scena (una copia)" % (CB.N, CB.L, CB.EPS_LUNGA))
    print("=" * 130)
    R = {}
    for caso in ("senza", "con"):
        with MB.scena(CB.N, CB.L, CB.EPS_LUNGA) as (rec, z, phi0, p):
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                w_in = DC.forma(z, rec["larghezza"])[0]
            s0 = istantanea(z)
            if caso == "con":
                DV.matrice(z, phi0, DV.AMP)
            s1 = istantanea(z)
            z["st"]["psi_h"][...] = p
            s2 = istantanea(z)
            m = MB.misure(z, phi0, rec, p) if caso == "senza" else None
            if caso == "con":
                z["st"]["psi_h"][...] = s1["psi_h"]   # ### lo stato come lo lascia matrice, per (E4)
                m = MB.misure(z, phi0, rec, p)
            R[caso] = {"s0": s0, "s1": s1, "s2": s2, "w_in": w_in, "misure": m, "letture": letture(z, phi0, rec, p, w_in)}
    print("### (0) IL CASO NULLO: due scene nuove sono identiche")
    c00 = confronta(R["senza"]["s0"], R["con"]["s0"])
    esito("DEVE PASSARE: lo stato iniziale delle due scene uguale al bit, chiave per chiave", all(v[0] for v in c00.values()), "%d chiavi: %s" % (len(c00), " ".join(sorted(c00))))
    esito("DEVE PASSARE: w_in delle due scene uguale al bit", R["senza"]["w_in"] == R["con"]["w_in"], "%.12f" % R["senza"]["w_in"])
    print("### (E1) CHE COSA CAMBIA matrice (lo stato prima e dopo, nella scena 'con')")
    c01 = confronta(R["con"]["s0"], R["con"]["s1"])
    for k, (ug, d) in c01.items():
        print("  %-12s %s   max |prima - dopo| %.3e" % (k, "uguale al bit" if ug else "### DIVERSO", d))
    esito("DEVE PASSARE: il controllo positivo -- matrice cambia lo stato (psi_h)", not c01["psi_h"][0], "%.3e" % c01["psi_h"][1])
    print("### (E2) DOPO AVER RICARICATO psi_h: che cosa resta diverso dallo stato iniziale")
    c02 = confronta(R["con"]["s0"], R["con"]["s2"])
    for k, (ug, d) in c02.items():
        print("  %-12s %s   max |iniziale - ricaricato| %.3e" % (k, "uguale al bit" if ug else "### DIVERSO", d))
    print("### (E3) I LETTORI DEI SITI DELL'ELENCO, dopo aver ricaricato lo stato: senza matrice prima / con matrice prima")
    for k in R["senza"]["letture"]:
        a, b = R["senza"]["letture"][k], R["con"]["letture"][k]
        print("  %-42s %s   %s | %s" % (k, "uguale al bit" if a == b else "### DIVERSO", str(a)[:80], str(b)[:80]))
    tutti = all(R["senza"]["letture"][k] == R["con"]["letture"][k] for k in R["senza"]["letture"])
    print("  ### IL CRITERIO DELLA CLASSE: i lettori dopo una ricarica sono ciechi a matrice: %s" % ("SI" if tutti else "NO"))
    print("### (E4) IL CONTROLLO POSITIVO DEI LETTORI: _massimo_di_B.misure (w_in da DC.forma PRIMA di caricare psi) sullo stato lasciato da matrice")
    ms, mc = R["senza"]["misure"], R["con"]["misure"]
    print("  senza: w_in %.6f f_win %.5f w %.5f | con: w_in %.6f f_win %.5f w %.5f" % (ms["w_in"], ms["f_win"], ms["w"], mc["w_in"], mc["f_win"], mc["w"]))
    esito("DEVE PASSARE: il controllo positivo -- misure dopo matrice (senza ricarica) da' un altro w_in (lo strumento vede l'effetto)", ms["w_in"] != mc["w_in"], "%.6f contro %.6f" % (ms["w_in"], mc["w_in"]))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--elenco" in argv:
        elenco()
    elif "--stato" in argv:
        stato()
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
