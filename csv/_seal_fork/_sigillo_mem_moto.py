# -*- coding: utf-8 -*-
"""SIGILLO — `MEM_MOTO`: BYTE-INERTE acceso, CHIRURGICO spento. [G4, prima della prova]

⚠ SCRITTO SUI CINQUE PATTERN STANDARD di `doc/PATTERN_DI_PROVA.md`:
  **1** un processo per braccio · **2** firme dei byte, non `max|delta|` · **3** le
  assenze STRUTTURALI non sono dati mancanti · **4** snapshot contro snapshot allo stesso
  istante · **5** il controllo dell'involucro *(qui e' `T7`, che confronta col riferimento
  prodotto dal blob PRIMA del flag)*.

DUE AFFERMAZIONI DIVERSE, e nessuna sostituisce l'altra:
  **A. BYTE-INERTE A FLAG ACCESO** -- col flag `True` il run e' **identico bit per bit** a quello
     di prima che il flag esistesse. Si misura contro **`_val600`**, che e' stato prodotto dal
     blob **`9557a867`**, cioe' **prima** di questa modifica. **`T7`.**
  **B. CHIRURGICO A FLAG SPENTO** -- sparisce **solo** `S08_proj`; ogni altro scrittore conserva
     le sue invocazioni e tutto cio' che sta **a monte** resta byte-identico. **`T1`-`T3`.**

⚠ `P1-sexies`: i criteri si collaudano PRIMA su casi a risposta nota, **e il piu' importante e'
  quello che DEVE fallire** -- uno spegnimento che tocca ANCHE un altro scrittore. Girato **sul
  codice vero**: `MEM_HEBB = False`, che il mandato VIETA, e che infatti ne tocca cinque.
ASCII PURO.
"""
import ast
import hashlib
import io
import json
import os
import subprocess
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, RADICE)
DEST = os.path.join(_QUI, "_sig_mem_moto")
OUT = os.path.join(DEST, "REFERTO.txt")
DRIVER = os.path.join(RADICE, "csv", "_test_fork", "_scena_video.py")
RIF120 = os.path.join(RADICE, "csv", "_test_fork", "_val600", "scena_000120.pkl.gz")
DEST_INERZIA = os.path.join(RADICE, "csv", "_test_fork", "_g4_inerzia")

PASSI = 3
BRACCIO = None
SALTA_T7 = False
for _a in sys.argv[1:]:
    if _a.startswith("--passi="):
        PASSI = int(_a.split("=", 1)[1])
    if _a.startswith("--braccio="):
        BRACCIO = _a.split("=", 1)[1]
    if _a == "--senza-t7":
        SALTA_T7 = True

ARGV = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
        "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
        "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
        "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
        "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--chi-coop",
        "--coes-adim", "--plast-din", "--viriale", "--olon-part",
        "--peq-esatto", "--peq-nascita-locale", "--scala-min-passo", "--coes-causale",
        "--anom-simm", "--invarianti=on"]
COMUNE = ["--sep=4.0", "--serie=20", "--chi-basc=on", "--chi-coop=on", "--scala-min=off",
          "--coes-adim=on", "--peq-esatto=on", "--peq-nascita-locale=on",
          "--scala-min-passo=on", "--coes-causale=on", "--anom-simm=on", "--invarianti=on"]

# L'ordine dei siti, VERIFICATO dal sorgente. `S08_proj` e' l'undicesimo: tutto cio' che lo
# precede e' "A MONTE" e a flag spento deve restare BYTE-IDENTICO.
A_MONTE = ("S01_archi_nuovi", "S02_rilass_visco", "S03_diff_guscio", "S04_rilass_TAU_P",
           "P1_dopo_rilass", "S05_spinta_locale", "P2_dopo_spinta", "S06_mitosi",
           "S07_schwinger")
SPENTI = ("S08_proj",)          # gli UNICI siti che il flag puo' togliere
CONCATENANO = ("S01_archi_nuovi", "S06_mitosi", "S07_schwinger")
BRACCI = (("ON", False, False), ("ON-bis", False, False),
          ("OFF", True, False), ("HEBB", False, True))


def firma(a):
    """`sha1` dei byte piu' cinque scalari. Pattern 2: piu' forte di `max|delta| = 0`."""
    if a is None:
        return None
    a = np.ascontiguousarray(np.asarray(a))
    fin = a[np.isfinite(a)] if a.size else a
    return {"sha1": hashlib.sha1(a.tobytes()).hexdigest()[:12],
            "forma": list(a.shape), "dtype": str(a.dtype),
            "somma": float(np.sum(fin)) if fin.size else 0.0,
            "somma_abs": float(np.sum(np.abs(fin))) if fin.size else 0.0,
            "min": float(np.min(fin)) if fin.size else 0.0,
            "max": float(np.max(fin)) if fin.size else 0.0,
            "n_non_finiti": int(a.size - fin.size)}


def identiche(fa, fb):
    """Pattern 3. TRE casi: due FIRME (byte) · due CONCATENA (lunghezze + coda + intero)
    · una di ciascuna o un `None` -> NON e' identita'."""
    if fa is None or fb is None:
        return False
    ca, cb = fa.get("concatena"), fb.get("concatena")
    if ca or cb:
        if not (ca and cb):
            return False
        _ka, _kb = fa.get("coda"), fb.get("coda")
        coda_ok = (_ka is None and _kb is None) or identiche(_ka, _kb)
        return (fa.get("da") == fb.get("da") and fa.get("a") == fb.get("a")
                and coda_ok and identiche(fa.get("tutto"), fb.get("tutto")))
    return fa["sha1"] == fb["sha1"] and fa["forma"] == fb["forma"]


def solo_quello(cnt_a, cnt_b, esenti):
    """I siti NON esenti hanno le stesse invocazioni? Ritorna i colpevoli."""
    fuori = []
    for s in sorted(set(cnt_a) | set(cnt_b)):
        if s in esenti:
            continue
        if cnt_a.get(s, 0) != cnt_b.get(s, 0):
            fuori.append((s, cnt_a.get(s, 0), cnt_b.get(s, 0)))
    return fuori


def gate_unico(percorso, nome):
    """Quante RAMIFICAZIONI dipendono da `nome`? Una sola = nessun'altra legge puo' esserne gated."""
    with io.open(percorso, encoding="utf-8") as f:
        albero = ast.parse(f.read(), percorso)
    rami, assegn, tutti = [], [], []
    for nodo in ast.walk(albero):
        if isinstance(nodo, (ast.If, ast.IfExp)):
            if any(isinstance(x, ast.Name) and x.id == nome for x in ast.walk(nodo.test)):
                rami.append(nodo.lineno)
        elif isinstance(nodo, ast.Assign):
            for t in nodo.targets:
                if isinstance(t, ast.Name) and t.id == nome:
                    assegn.append(nodo.lineno)
        elif isinstance(nodo, ast.Name) and nodo.id == nome:
            tutti.append(nodo.lineno)
    return sorted(rami), sorted(assegn), sorted(set(tutti))


def confronta_snap(p_a, p_b, W):
    """Pattern 4: SNAPSHOT contro SNAPSHOT, e niente cast dei complessi a `float`."""
    import gzip
    import pickle

    def leggi(p):
        with gzip.open(p, "rb") as f:
            return pickle.load(f)["attrs"]
    a, b = leggi(p_a), leggi(p_b)
    ug = dv = assenti = 0
    nomi = []
    for k in sorted(set(a) | set(b)):
        if k not in a or k not in b:
            assenti += 1; nomi.append("%s(in uno solo)" % k); continue
        aa = np.asarray(a[k]); bb = np.asarray(b[k])
        if aa.shape != bb.shape:
            dv += 1; nomi.append("%s(shape %s!=%s)" % (k, aa.shape, bb.shape)); continue
        if aa.dtype.kind in "fc" or bb.dtype.kind in "fc":
            d = float(np.max(np.abs(aa - bb))) if aa.size else 0.0
            if d == 0.0:
                ug += 1
            else:
                dv += 1; nomi.append("%s(max|d|=%.3e)" % (k, d))
        else:
            if np.array_equal(aa, bb):
                ug += 1
            else:
                dv += 1; nomi.append(k)
    W("  campi UGUALI %d   DIVERSI %d   non confrontati %d\n" % (ug, dv, assenti))
    if nomi:
        W("  i diversi: %s\n" % ", ".join(nomi[:10]))
    return ug, dv


def collaudo(W):
    """`P1-sexies`, su casi a risposta NOTA. Quattro di essi DEVONO fallire."""
    W("COLLAUDO DEI CRITERI su casi a RISPOSTA NOTA (`P1-sexies`), PRIMA di sigillare\n")
    W("-" * 100 + "\n")
    e = []
    base = {"S07_schwinger": 3, "S08_proj": 3, "S09_spinta_med": 3, "S12_coesione": 3}
    es = set(SPENTI)

    bene = dict(base); bene["S08_proj"] = 0
    f1 = solo_quello(base, bene, es)
    ok1 = (len(f1) == 0)
    W("K1 spegnimento CHIRURGICO (solo `S08_proj` sparisce) -> nessun colpevole -> %s\n"
      % ("OK" if ok1 else "*** FALSO ALLARME ***"))
    e.append(ok1)

    male = dict(base); male["S08_proj"] = 0; male["S09_spinta_med"] = 0
    f2 = solo_quello(base, male, es)
    ok2 = any(s == "S09_spinta_med" for s, _a, _b in f2)
    W("K2 IL CASO CHE DEVE FALLIRE: tocca ANCHE `S09_spinta_med` -> %s  (colpevoli %s)\n"
      % ("OK: il criterio lo VEDE" if ok2 else "*** CIECO ***", f2))
    e.append(ok2)

    a = np.linspace(0.0, 1.0, 50)
    ok3 = identiche(firma(a), firma(a.copy()))
    z1 = np.array([0.0, 1.0]); z2 = np.array([-0.0, 1.0])
    md = float(np.max(np.abs(z1 - z2)))
    ok4 = (not identiche(firma(z1), firma(z2))) and (md == 0.0)
    W("K3 FIRMA: due array identici -> stessa firma -> %s\n" % ("OK" if ok3 else "*** NO ***"))
    W("K4 IL CASO CHE `max|delta|` SBAGLIEREBBE: `+0.0` contro `-0.0`, max|delta| = %.1e\n" % md)
    W("     le firme sono DIVERSE -> %s\n"
      % ("OK: la firma e' piu' stretta" if ok4 else "*** non e' piu' stretta ***"))
    e += [ok3, ok4]

    def _cc(da, a_, coda, tutto):
        return {"concatena": True, "da": da, "a": a_,
                "coda": firma(np.asarray(coda, dtype=float)),
                "tutto": firma(np.asarray(tutto, dtype=float))}
    c1 = _cc(100, 104, [1., 2., 3., 4.], np.arange(104, dtype=float))
    c2 = _cc(100, 104, [1., 2., 3., 4.], np.arange(104, dtype=float))
    c3 = _cc(100, 104, [1., 2., 3., 9.], np.arange(104, dtype=float))
    _t = np.arange(104, dtype=float); _t[7] = -1.0
    c4 = _cc(100, 104, [1., 2., 3., 4.], _t)
    ok5 = identiche(c1, c2)
    ok6 = (not identiche(c1, c3))
    ok7 = (not identiche(c1, c4))
    ok8 = (not identiche(None, None))
    W("K5 CONCATENA identici (lunghezze + coda + intero) -> %s\n" % ("OK" if ok5 else "*** NO ***"))
    W("K6 IL CASO CHE DEVE FALLIRE: stesse lunghezze, CODA diversa -> %s\n"
      % ("OK" if ok6 else "*** guarderebbe solo i CONTI ***"))
    W("K7 IL CASO CHE DEVE FALLIRE: stessa coda, cambia la parte CONSERVATA -> %s\n"
      % ("OK" if ok7 else "*** sfuggirebbe un cambiamento dentro `d0[keep]` ***"))
    W("K8 due ASSENZE non sono un'identita' -> %s\n" % ("OK" if ok8 else "*** NO ***"))
    e += [ok5, ok6, ok7, ok8]

    ok = all(e)
    W("-" * 100 + "\n")
    W("  -> i criteri %s\n\n" % ("PASSANO: si sigilla" if ok else "*** NON PASSANO ***"))
    return ok


def braccio(nome):
    """Pattern 1: un processo TUTTO SUO. Scrive la cattura in JSON."""
    if nome == "INERZIA":
        # `T7`: il run a flag ACCESO, attraverso il DRIVER, per confrontarlo col riferimento
        # prodotto dal blob PRIMA del flag. Non si tocca nulla: `MEM_MOTO` resta `True`.
        import runpy
        try:
            os.makedirs(DEST_INERZIA)
        except OSError:
            pass
        os.chdir(RADICE)
        sys.argv = ["_scena_video.py", "20", DEST_INERZIA] + COMUNE
        runpy.run_path(DRIVER, run_name="__main__")
        return 0

    _sp = dict((n, (g, h)) for n, g, h in BRACCI)
    spegni_mem, spegni_hebb = _sp[nome]
    os.chdir(RADICE)
    sys.argv = list(ARGV)
    import soliton_simulator as S
    S.TRACCIA_D0 = False
    a = S._cli(); S._applica_regime(a); S._applica_flag(a)
    S.MEM_MOTO = (not spegni_mem)
    S.MEM_HEBB = (not spegni_hebb)
    np.random.seed(20260922)
    S._NMASSE_VIDEO["n"] = 3; S._NMASSE_VIDEO["sep"] = 4.0; S._NMASSE_VIDEO["size"] = None
    S.avvia_test("N-MASSE")()
    net = S.net
    S.stato["nframe"] = 0
    cnt, primo = {}, {}
    stato = {"passo": 0}

    def traccia(self, sito, prima, pavimento=None):
        cnt[sito] = cnt.get(sito, 0) + 1
        if stato["passo"] == 1 and sito not in primo:
            dopo = np.asarray(self.d0, dtype=float)
            pri = np.asarray(prima, dtype=float)
            if len(pri) == len(dopo):
                primo[sito] = firma(dopo - pri)
            else:
                primo[sito] = {"concatena": True, "da": len(pri), "a": len(dopo),
                               "coda": firma(dopo[len(pri):]) if len(dopo) > len(pri) else None,
                               "tutto": firma(dopo)}
    S.Rete._traccia_d0 = traccia
    S.TRACCIA_D0 = True
    PPF = int(S.PASSI_PER_FRAME)
    mm1 = d01 = None
    for k in range(1, PASSI + 1):
        stato["passo"] = k
        if (k - 1) % PPF == 0:
            S.passo_test()
        S.scuoti_vuoto(net); net.step(); net.mitosi()
        net.rilassa_disegno(); net.memoria_hebbiana_moto()
        if k == 1:
            mm1 = firma(np.asarray(net.mem_mot, dtype=float))
            d01 = firma(np.asarray(net.d0, dtype=float))
    cap = {"nome": nome, "mem": bool(S.MEM_MOTO), "hebb": bool(S.MEM_HEBB),
           "n": int(net.n), "archi": int(len(net.i)), "passi": PASSI,
           "cnt": cnt, "primo": primo, "mem_mot": mm1, "d0": d01}
    with io.open(os.path.join(DEST, "cap_%s.json" % nome), "w", encoding="utf-8") as f:
        f.write(json.dumps(cap, indent=1))
    print("[braccio %s] n=%d archi=%d siti=%d" % (nome, net.n, len(net.i), len(cnt)))
    return 0


def main():
    try:
        os.makedirs(DEST)
    except OSError:
        pass
    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    W = o.write
    W("# SIGILLO -- `MEM_MOTO`: BYTE-INERTE acceso, CHIRURGICO spento\n")
    W("# scritto sui CINQUE PATTERN STANDARD di `doc/PATTERN_DI_PROVA.md`.\n")
    W("# %d passi per braccio, un PROCESSO per braccio.\n#\n" % PASSI)
    if not collaudo(W):
        o.close(); print(io.open(OUT, encoding="utf-8").read()); return 1

    blob = hashlib.sha1(
        open(os.path.join(RADICE, "soliton_simulator.py"), "rb").read()).hexdigest()[:8]
    W("blob simulatore ORA (sha1 byte grezzi) %s\n" % blob)
    W("riferimento `_val600`, prodotto dal blob PRIMA del flag: 9557a867\n\n")

    t0 = time.time()
    W("I BRACCI, ciascuno in un processo suo:\n")
    cap = {}
    for nome, _g, _h in BRACCI:
        p = os.path.join(DEST, "cap_%s.json" % nome)
        if os.path.exists(p):
            os.remove(p)
        r = subprocess.run([sys.executable, os.path.abspath(__file__),
                            "--braccio=%s" % nome, "--passi=%d" % PASSI],
                           cwd=RADICE, capture_output=True, text=True)
        if not os.path.exists(p):
            W("  *** il braccio %s NON ha prodotto la cattura. uscita=%d ***\n%s\n"
              % (nome, r.returncode, (r.stderr or "")[-2000:]))
            o.close(); print(io.open(OUT, encoding="utf-8").read()); return 1
        with io.open(p, encoding="utf-8") as f:
            cap[nome] = json.load(f)
        c = cap[nome]
        W("  %-8s MEM_MOTO=%-5s MEM_HEBB=%-5s  n=%-6d archi=%-7d siti=%d\n"
          % (nome, c["mem"], c["hebb"], c["n"], c["archi"], len(c["cnt"])))
    W("  (%.1f s)\n\n" % (time.time() - t0))

    ON, ONB, OFF, HEBB = cap["ON"], cap["ON-bis"], cap["OFF"], cap["HEBB"]
    esiti = []

    def esito(n, ok, riga):
        esiti.append((n, ok))
        W("%-5s %-4s %s\n" % (n, "PASS" if ok else "FAIL", riga))

    W("=" * 100 + "\nI CRITERI\n" + "=" * 100 + "\n")

    f0 = solo_quello(ON["cnt"], ONB["cnt"], set())
    div = [s for s in ON["primo"] if not identiche(ON["primo"][s], ONB["primo"].get(s))]
    ok0 = (len(f0) == 0 and not div and identiche(ON["mem_mot"], ONB["mem_mot"])
           and identiche(ON["d0"], ONB["d0"]) and ON["n"] == ONB["n"])
    esito("T0", ok0, "RIPRODUCIBILITA': due bracci ON separati -> invocazioni diverse=%d, firme "
                     "diverse=%d, n %d==%d" % (len(f0), len(div), ON["n"], ONB["n"]))
    if not ok0:
        W("\n*** T0 FALLISCE: sotto, qualunque differenza sarebbe indistinguibile dalla "
          "deriva. IL SIGILLO SI FERMA. ***\n")
        if div:
            W("    siti con firma diversa: %s\n" % div[:10])
        o.close(); print(io.open(OUT, encoding="utf-8").read()); return 1

    on8 = ON["cnt"].get("S08_proj", 0); off8 = OFF["cnt"].get("S08_proj", 0)
    ok1 = (on8 > 0) and (off8 == 0)
    esito("T1", ok1, "LO SPEGNIMENTO SPEGNE: S08_proj ON=%d -> OFF=%d" % (on8, off8))

    f2 = solo_quello(ON["cnt"], OFF["cnt"], set(SPENTI))
    ok2 = (len(f2) == 0)
    esito("T2", ok2, "SPEGNE SOLO QUELLO: siti diversi da `S08_proj` con invocazioni diverse = "
                     "%d %s" % (len(f2), f2 if f2 else ""))

    fuori = [s for s in A_MONTE
             if s in ON["primo"] and not identiche(ON["primo"][s], OFF["primo"].get(s))]
    ok3 = (len(fuori) == 0)
    esito("T3", ok3, "BYTE-IDENTITA' A MONTE al passo 1: confrontati=%d, DIVERSI=%d %s"
                     % (len([s for s in A_MONTE if s in ON["primo"]]), len(fuori),
                        fuori if fuori else ""))
    for s in A_MONTE:
        fa = ON["primo"].get(s)
        if fa is None:
            W("      %-20s non invocato al passo 1\n" % s); continue
        ug = "IDENTICO" if identiche(fa, OFF["primo"].get(s)) else "*** DIVERSO ***"
        if fa.get("concatena"):
            fb = OFF["primo"].get(s) or {}
            W("      %-20s CONCATENA ON %s->%s OFF %s->%s  coda %s/%s  %s\n"
              % (s, fa.get("da"), fa.get("a"), fb.get("da"), fb.get("a"),
                 (fa.get("coda") or {}).get("sha1", "-"),
                 (fb.get("coda") or {}).get("sha1", "-"), ug))
        else:
            W("      %-20s sha1 %s  somma %+.6e  %s\n" % (s, fa["sha1"], fa["somma"], ug))

    ok4 = identiche(ON["mem_mot"], OFF["mem_mot"])
    esito("T4", ok4, "`mem_mot` RESTA AGGIORNATO anche a flag spento: ON sha1 %s vs OFF %s -> %s"
                     % (ON["mem_mot"]["sha1"], OFF["mem_mot"]["sha1"],
                        "IDENTICO" if ok4 else "DIVERSO"))
    W("      -> e' VOLUTO: il flag toglie la SCRITTURA SU `d0`, non la grandezza di stato.\n")

    rami, assegn, tutti = gate_unico(os.path.join(RADICE, "soliton_simulator.py"), "MEM_MOTO")
    ok5 = (len(rami) == 1)
    esito("T5", ok5, "GATE UNICO (AST): ramificazioni che dipendono da MEM_MOTO = %d, righe %s"
                     % (len(rami), rami))
    W("      assegnamenti: %s ; occorrenze del NOME: %s\n" % (assegn, tutti))

    f6 = solo_quello(ON["cnt"], HEBB["cnt"], set(SPENTI))
    ok6 = (len(f6) > 0)
    esito("T6", ok6, "IL CASO CHE DEVE FALLIRE -- `MEM_HEBB=False`: siti toccati OLTRE "
                     "`S08_proj` = %d" % len(f6))
    for s, a_, b_ in f6:
        W("      %-20s ON=%-4d HEBB=%-4d\n" % (s, a_, b_))

    # ---- T7: LA BYTE-INERZIA A FLAG ACCESO, contro il blob PRIMA del flag
    if SALTA_T7:
        W("\nT7    SALTATO su richiesta (`--senza-t7`): la BYTE-INERZIA NON e' dimostrata.\n")
        esiti.append(("T7", False))
    else:
        W("\n" + "-" * 100 + "\n")
        W("T7 -- LA BYTE-INERZIA A FLAG ACCESO (120 passi attraverso il DRIVER)\n")
        W("  confronto SNAPSHOT contro SNAPSHOT col riferimento `_val600/scena_000120.pkl.gz`,\n")
        W("  prodotto dal blob `9557a867`, cioe' PRIMA che questo flag esistesse.\n")
        W("-" * 100 + "\n")
        p_in = os.path.join(DEST_INERZIA, "scena_000120.pkl.gz")
        if os.path.exists(p_in):
            os.remove(p_in)
        t1 = time.time()
        r = subprocess.run([sys.executable, os.path.abspath(__file__), "--braccio=INERZIA"],
                           cwd=RADICE, capture_output=True, text=True)
        W("  (%.1f s)\n" % (time.time() - t1))
        if not os.path.exists(p_in):
            W("  *** il braccio INERZIA non ha prodotto lo snapshot. uscita=%d ***\n%s\n"
              % (r.returncode, (r.stderr or "")[-1500:]))
            esiti.append(("T7", False))
        elif not os.path.exists(RIF120):
            W("  *** manca il riferimento %s ***\n" % RIF120)
            esiti.append(("T7", False))
        else:
            ug7, dv7 = confronta_snap(RIF120, p_in, W)
            ok7 = (dv7 == 0 and ug7 > 0)
            esiti.append(("T7", ok7))
            W("T7    %-4s BYTE-INERTE a flag ACCESO: %d campi identici, %d diversi\n"
              % ("PASS" if ok7 else "FAIL", ug7, dv7))

    n_ok = sum(1 for _n, k in esiti if k)
    W("\n" + "=" * 100 + "\nESITO: %d/%d\n" % (n_ok, len(esiti)) + "=" * 100 + "\n")
    if n_ok == len(esiti):
        W("*** SIGILLO PASSATO. `MEM_MOTO` e' BYTE-INERTE acceso e CHIRURGICO spento.\n")
        W("    La prova di spegnimento `G4` puo' partire. ***\n")
    else:
        W("*** SIGILLO FALLITO: la prova di spegnimento NON parte. ***\n")
    W("\nLIMITI: %d passi per braccio per `T1`-`T6`, UN seme, UNA scena. Cio' che li rende\n" % PASSI)
    W("  conclusivi non e' il numero di passi ma `T5` (strutturale) e `T7` (120 passi contro il\n")
    W("  riferimento vero).\n")
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0 if n_ok == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(braccio(BRACCIO) if BRACCIO else main())
