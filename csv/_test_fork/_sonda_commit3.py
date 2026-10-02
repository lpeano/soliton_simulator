# -*- coding: utf-8 -*-
"""**SONDA USA-E-GETTA del `COMMIT 3`** — il punto unico cambia un bit?

### NON E' IL SIGILLO, ed e' importante dirlo: il *<<prima>>* lo prende da una
### **copia nello scratchpad**, non da `git`. Quindi ### **NON vale come prova**
*(`ANCORE-1`: un *<<prima>>* che non viene dalla storia e' un *<<prima>>* che
nessuno puo' rifare)*. Serve a una cosa sola: ### **non committare codice che non
ha mai girato.**

### La prova vera e' il braccio `E` di `csv/_seal_fork/_sigillo_confronto_esteso.py`,
che estrae il *<<prima>>* dal **PADRE del commit 3** con `sim_prima_del_flag`.

**Referto:** `csv/_test_fork/_sonda_commit3/`.
"""
import contextlib
import hashlib
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_QUI, ".."))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _cli_flag        # noqa: E402
import _passo           # noqa: E402
import _confronto_nascita as CN   # noqa: E402

SIM = os.path.join(RADICE, "soliton_simulator.py")
FUORI = os.path.join(_QUI, "_sonda_commit3")


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


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
    seme, passi = 11, 72
    prima_path = None
    for x in sys.argv[1:]:
        if x.startswith("--seme="):
            seme = int(x.split("=", 1)[1])
        elif x.startswith("--passi="):
            passi = int(x.split("=", 1)[1])
        elif x.startswith("--prima="):
            prima_path = x.split("=", 1)[1]
    if prima_path is None or not os.path.isfile(prima_path):
        raise SystemExit("** serve `--prima=<percorso del simulatore di PRIMA>` **")
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    righe = []

    def stampa(*x):
        r = " ".join(str(y) for y in x)
        righe.append(r)
        print(r)

    stampa("=" * 100)
    stampa("SONDA DEL COMMIT 3 -- il punto unico cambia un bit?")
    stampa("  ### NON E' IL SIGILLO: il <<prima>> viene da una COPIA, non da git.")
    stampa("  ### Non vale come prova. Serve a non committare codice che non ha mai girato.")
    stampa("=" * 100)
    stampa("  DOPO  (il punto unico) ... %s" % blob(SIM)[:8])
    stampa("  PRIMA (dalla copia) ...... %s   %s" % (blob(prima_path)[:8], prima_path))
    stampa("  seme %d   passi %d" % (seme, passi))
    stampa("")

    SA, nA = carica("sonda_dopo", seme)
    avanza(SA, nA, passi)
    fa, quali = CN.foto(SA, nA, sorgente=SIM)
    stampa("  DOPO:  %d grandezze nell'insieme, %d scattate" % (len(quali), len(fa)))
    nati_a = (getattr(nA, "_g_nati_mitosi", 0), getattr(nA, "_g_nati_schwinger", 0),
              getattr(nA, "nati", 0), getattr(nA, "coppie_nate", 0))
    stampa("  DOPO:  nati_mitosi=%d nati_schwinger=%d nati=%d coppie=%d" % nati_a)
    stampa("  DOPO:  eventi di nascita contati dal punto unico (_g_nascite) = %s"
           % getattr(nA, "_g_nascite", "### ASSENTE"))
    if not nati_a[0]:
        raise SystemExit("** NESSUNA NASCITA in %d passi: la sonda non misura niente. "
                         "E' un NON MISURATO, non un <<nessuna differenza>>. **" % passi)

    SB, nB = carica("sonda_prima", seme, sim=prima_path)
    avanza(SB, nB, passi)
    fb, _ = CN.foto(SB, nB, sorgente=prima_path)
    nati_b = (getattr(nB, "_g_nati_mitosi", 0), getattr(nB, "_g_nati_schwinger", 0),
              getattr(nB, "nati", 0), getattr(nB, "coppie_nate", 0))
    stampa("  PRIMA: nati_mitosi=%d nati_schwinger=%d nati=%d coppie=%d" % nati_b)
    stampa("")

    diff = CN.confronta(fa, fb)
    # `_g_nascite` NON esisteva prima: e' il contatore del punto unico, e la sua
    # comparsa e' ATTESA. Si dichiara invece di nasconderla.
    attese = {"_g_nascite"}
    vere = [d for d in diff if d["nome"] not in attese]
    comparse = [d for d in diff if d["nome"] in attese]
    stampa("  ### DIFFERENZE: %d in tutto, di cui %d ATTESE (contatori nuovi) e %d VERE"
           % (len(diff), len(comparse), len(vere)))
    for d in comparse:
        stampa("      attesa:  %s" % json.dumps(d, ensure_ascii=False, default=str)[:200])
    for d in vere:
        stampa("      ### VERA: %s" % json.dumps(d, ensure_ascii=False, default=str)[:300])
    passa = not vere
    stampa("")
    stampa("=" * 100)
    stampa("### %s" % ("LA SONDA PASSA: zero differenze vere su %d grandezze confrontate."
                       % len(set(fa) & set(fb)) if passa
                       else "LA SONDA FALLISCE: %d differenze vere." % len(vere)))
    stampa("###   (e resta una SONDA: la prova e' il braccio `E` del sigillo.)")

    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=chr(10)).write(chr(10).join(righe) + chr(10))
    io.open(os.path.join(FUORI, "_sonda_commit3.json"), "w", encoding="utf-8",
            newline=chr(10)).write(json.dumps(
                {"passa": bool(passa), "blob_dopo": blob(SIM), "blob_prima": blob(prima_path),
                 "seme": seme, "passi": passi, "confrontate": len(set(fa) & set(fb)),
                 "differenze_vere": vere, "differenze_attese": comparse,
                 "nati_dopo": nati_a, "nati_prima": nati_b,
                 "NON_E_UNA_PROVA": "il <<prima>> viene da una copia, non da git"},
                indent=2, ensure_ascii=False, default=str))
    print("  referto .. %s" % FUORI)
    return 0 if passa else 1


if __name__ == "__main__":
    sys.exit(principale())
