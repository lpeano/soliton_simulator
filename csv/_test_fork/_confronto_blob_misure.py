# -*- coding: utf-8 -*-
"""CONFRONTO fra i referti di DUE blob del simulatore, grandezza per grandezza.

PERCHE':  tre misure (`_misure_calore`, `_pos_contro_d`, `_verso_archi`) girarono il
          2026-10-01 sul simulatore `287154f3`. Da allora TREDICI commit lo hanno
          cambiato, fino a `0f060670`. Le misure vanno rilette sul blob di oggi, e
          cio' che interessa non e' il numero nuovo: e' LO SCARTO, e la sua causa.

### QUESTO NON E' UN SIGILLO, ed e' un criterio fissato nel mandato, non una scelta mia:
### non stampa PASSA ne' FALLISCE. Stampa NUMERI e, per cio' che cambia, i CANDIDATI
### alla causa -- i commit che hanno toccato il simulatore fra i due blob.

COME:     ogni referto e' un json annidato. Lo strumento lo APPIATTISCE in un dizionario
          di percorsi-foglia (`M3.xi_frena`, `per_nodo[4].voce`, ...) e confronta i due
          dizionari foglia per foglia. ### Appiattire invece di confrontare i json interi
          serve a una cosa sola: **dire QUALE grandezza e' cambiata**, non *«i referti
          differiscono»*.

### LA PIATTAFORMA SI DICHIARA, e c'e' un motivo preciso: i referti del 2026-10-01
### NON HANNO un campo per la piattaforma -- lo strumento lo VERIFICA e lo dice. Quindi
### per le grandezze sensibili alla piattaforma (i CONTEGGI ASSOLUTI: la stella polare
### documenta `16/14/6/6` su Linux contro `14/12/4/4` su Windows) lo scarto **non si
### puo' attribuire al simulatore**. Il limite e' stampato, non sottinteso.

USO:      python csv/_test_fork/_confronto_blob_misure.py
          python csv/_test_fork/_confronto_blob_misure.py --collaudo

USCITA:   `csv/_test_fork/_confronto_blob_misure/_confronto.json` + `_corsa.txt` + stdout.

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Legge due referti json
#   gia' scritti e li confronta. La configurazione di ciascun run e' dichiarata DENTRO
#   il referto che confronta, e questo strumento la RIPORTA (blob_sim, blob_strumento).
"""
import hashlib
import io
import json
import os
import platform
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
FUORI = os.path.join(RADICE, "csv", "_test_fork", "_confronto_blob_misure")
VECCHIO = "287154f3"
NUOVO = "0f060670"
STRUMENTI = ["_misure_calore", "_pos_contro_d", "_verso_archi"]

P = []


def stampa(s=""):
    print(s)
    P.append(s)


def riga(c="-"):
    stampa(c * 104)


# ---------------------------------------------------------------------- appiattimento
def appiattisci(v, pre="", fuori=None):
    """json annidato -> {percorso-foglia: valore}. Le liste prendono l'indice."""
    if fuori is None:
        fuori = {}
    if isinstance(v, dict):
        for k in v:
            appiattisci(v[k], (pre + "." + str(k)) if pre else str(k), fuori)
    elif isinstance(v, list):
        for i, x in enumerate(v):
            appiattisci(x, "%s[%d]" % (pre, i), fuori)
    else:
        fuori[pre] = v
    return fuori


def uguali(a, b):
    """uguaglianza che NON confonde 1 con 1.0 ne' True con 1, e che su float
    distingue IDENTICO da VICINO: lo scarto si riporta, non si assorbe."""
    if type(a) is bool or type(b) is bool:
        return (type(a) is type(b)) and a == b
    if isinstance(a, float) or isinstance(b, float):
        try:
            return float(a) == float(b)
        except (TypeError, ValueError):
            return False
    return type(a) is type(b) and a == b


def confronta(vecchio, nuovo):
    """-> (identiche, cambiate, solo_vecchio, solo_nuovo)"""
    A, B = appiattisci(vecchio), appiattisci(nuovo)
    ident, camb = [], []
    for k in A:
        if k not in B:
            continue
        (ident if uguali(A[k], B[k]) else camb).append(k)
    return (sorted(ident), sorted(camb),
            sorted(k for k in A if k not in B), sorted(k for k in B if k not in A))


# ---------------------------------------------------------------------- i candidati
def commit_fra_i_blob():
    """I commit che hanno toccato il simulatore DOPO il blob vecchio, fino a oggi.
    Li legge da git: la lista non e' ricopiata da un mandato (`L-NUMERI`)."""
    def sh(*a):
        return subprocess.run(["git", "-C", RADICE] + list(a),
                              capture_output=True).stdout
    out, visti = [], False
    testo = sh("log", "--format=%h|%ad|%s", "--date=short",
               "--", "soliton_simulator.py").decode("utf-8", "replace")
    for r in testo.strip().split(NL):
        if not r.strip():
            continue
        h, d, s = r.split("|", 2)
        b = sh("show", h + ":soliton_simulator.py")
        sha = hashlib.sha1(b).hexdigest()[:8]
        if sha == VECCHIO:
            visti = True
            out.append((h, d, sha, s))
            break
        out.append((h, d, sha, s))
    return out, visti


def piattaforma():
    try:
        import numpy
        nv = numpy.__version__
    except Exception:
        nv = "?"
    return {"python": sys.version.split()[0], "numpy": nv,
            "sistema": platform.system() + " " + platform.release(),
            "macchina": platform.machine()}


# ---------------------------------------------------------------------- il collaudo
CASI = [
    ("una foglia CAMBIATA e' scoperta col percorso",
     {"a": {"b": 1}}, {"a": {"b": 2}}, 0, 1, 0, 0),
    ("due referti IDENTICI non producono cambiate",
     {"a": {"b": 1}, "c": [1, 2]}, {"a": {"b": 1}, "c": [1, 2]}, 3, 0, 0, 0),
    ("1 contro 1.0 e' IDENTICO (non un cambio)",
     {"x": 1}, {"x": 1.0}, 1, 0, 0, 0),
    ("True contro 1 e' un CAMBIO (il bool non e' un intero)",
     {"x": True}, {"x": 1}, 0, 1, 0, 0),
    ("una chiave SPARITA e una NUOVA non si contano come cambiate",
     {"x": 1, "v": 2}, {"x": 1, "n": 3}, 1, 0, 1, 1),
    ("una LISTA piu' corta: gli indici in meno sono solo_vecchio",
     {"L": [1, 2, 3]}, {"L": [1, 2]}, 2, 0, 1, 0),
    ("uno scarto float MINIMO e' un CAMBIO, non un arrotondamento",
     {"x": 1.0}, {"x": 1.0 + 1e-15}, 0, 1, 0, 0),
]


def collaudo():
    riga("=")
    stampa("COLLAUDO -- i casi che lo strumento deve distinguere")
    riga("=")
    ok = True
    for et, a, b, ni, nc, nv, nn in CASI:
        i, c, v, n = confronta(a, b)
        buono = (len(i), len(c), len(v), len(n)) == (ni, nc, nv, nn)
        ok = ok and buono
        stampa("  %-58s %s  ident=%d camb=%d solo_v=%d solo_n=%d"
               % (et, "OK  " if buono else "FALLITO", len(i), len(c), len(v), len(n)))
        if not buono:
            stampa("      atteso ident=%d camb=%d solo_v=%d solo_n=%d" % (ni, nc, nv, nn))
    stampa()
    stampa("  ### %s" % ("tutti e %d i casi passano." % len(CASI) if ok
                         else "*** COLLAUDO FALLITO ***"))
    riga("=")
    return 0 if ok else 1


# ---------------------------------------------------------------------- il corpo
def principale():
    riga("=")
    stampa("CONFRONTO DEI REFERTI FRA DUE BLOB DEL SIMULATORE: %s -> %s" % (VECCHIO, NUOVO))
    riga("=")
    stampa()
    stampa("### NON E' UN SIGILLO: nessun PASSA, nessun FALLISCE. Numeri e cause.")
    stampa()

    pf = piattaforma()
    stampa("LA PIATTAFORMA DI QUESTO CONFRONTO (par.5 della stella polare: i conteggi")
    stampa("assoluti ne dipendono, l'identita' prima/dopo no)")
    for k in ["python", "numpy", "sistema", "macchina"]:
        stampa("  %-10s %s" % (k, pf[k]))
    stampa()

    riga()
    stampa("I CANDIDATI ALLA CAUSA: i commit del simulatore fra i due blob")
    riga()
    cand, visti = commit_fra_i_blob()
    for h, d, sha, s in cand:
        marca = ""
        if sha == NUOVO:
            marca = "   <-- il blob di OGGI"
        if sha == VECCHIO:
            marca = "   <-- il blob dei referti VECCHI"
        stampa("  %s  %s  %s  %s%s" % (h, d, sha, s[:52], marca))
    if not visti:
        stampa("  ### ATTENZIONE: il blob %s NON e' stato trovato nella storia del" % VECCHIO)
        stampa("      simulatore. La lista dei candidati e' INCOMPLETA, e lo dico.")
    stampa()
    stampa("  %d commit fra i due blob (il primo e l'ultimo compresi)." % len(cand))
    stampa()

    fuori = {"blob_vecchio": VECCHIO, "blob_nuovo": NUOVO, "piattaforma": pf,
             "blob_strumento": _presidio.blob(__file__)
             if hasattr(_presidio, "blob") else None,
             "candidati_causa": [{"commit": h, "data": d, "blob": s, "titolo": t}
                                 for h, d, s, t in cand],
             "strumenti": {}}

    tot_i = tot_c = 0
    for nome in STRUMENTI:
        d = os.path.join(RADICE, "csv", "_test_fork", nome)
        pv = os.path.join(d, "%s.%s.json" % (nome, VECCHIO))
        pn = os.path.join(d, "%s.json" % nome)
        riga("=")
        stampa("%s" % nome)
        riga("=")
        if not (os.path.exists(pv) and os.path.exists(pn)):
            stampa("  ### REFERTO MANCANTE: %s" % (pv if not os.path.exists(pv) else pn))
            stampa("      Non confronto nulla, e NON lo chiamo <<nessuna differenza>>.")
            fuori["strumenti"][nome] = {"stato": "referto mancante"}
            continue
        V = json.load(io.open(pv, encoding="utf-8"))
        N = json.load(io.open(pn, encoding="utf-8"))

        # il blob dichiarato DENTRO i referti, non supposto dal nome del file
        bv = str(V.get("blob_sim_sha1_byte", "?"))[:8]
        bn = str(N.get("blob_sim_sha1_byte", "?"))[:8]
        stampa("  blob_sim dichiarato NEL referto:  vecchio %s   nuovo %s" % (bv, bn))
        if bv != VECCHIO or bn != NUOVO:
            stampa("  ### I BLOB DICHIARATI NON SONO QUELLI ATTESI: il confronto che segue")
            stampa("      NON e' fra %s e %s. Lo dico invece di proseguire in silenzio."
                   % (VECCHIO, NUOVO))
        sv = str(V.get("blob_strumento", "?"))[:8]
        sn = str(N.get("blob_strumento", "?"))[:8]
        stampa("  blob_strumento:                   vecchio %s   nuovo %s%s"
               % (sv, sn, "" if sv == sn else "   ### LO STRUMENTO E' CAMBIATO"))
        pv_old = "piattaforma" in V or "python" in V
        stampa("  la piattaforma e' dichiarata nel referto VECCHIO? %s"
               % ("si'" if pv_old else "NO -- quindi lo scarto dei CONTEGGI ASSOLUTI non "
                                      "si puo' attribuire al simulatore"))
        stampa()

        ident, camb, solo_v, solo_n = confronta(V, N)
        tot_i += len(ident)
        tot_c += len(camb)
        stampa("  foglie: %d identiche, %d CAMBIATE, %d solo nel vecchio, %d solo nel nuovo"
               % (len(ident), len(camb), len(solo_v), len(solo_n)))
        stampa()
        A, B = appiattisci(V), appiattisci(N)
        if camb:
            stampa("  LE GRANDEZZE CAMBIATE, una per riga:")
            stampa("  %-54s %-20s %-20s" % ("percorso", "vecchio", "nuovo"))
            for k in camb:
                stampa("  %-54s %-20s %-20s"
                       % (k[:54], repr(A[k])[:20], repr(B[k])[:20]))
        else:
            stampa("  NESSUNA grandezza cambiata fra le foglie presenti in entrambi.")
        if solo_v or solo_n:
            stampa()
            stampa("  CHIAVI PRESENTI DA UN SOLO LATO (non sono cambi: sono struttura)")
            for k in solo_v[:40]:
                stampa("    solo VECCHIO  %-50s = %s" % (k[:50], repr(A[k])[:28]))
            if len(solo_v) > 40:
                stampa("    ... e altre %d solo nel vecchio" % (len(solo_v) - 40))
            for k in solo_n[:40]:
                stampa("    solo NUOVO    %-50s = %s" % (k[:50], repr(B[k])[:28]))
            if len(solo_n) > 40:
                stampa("    ... e altre %d solo nel nuovo" % (len(solo_n) - 40))
        stampa()
        fuori["strumenti"][nome] = {
            "blob_sim_vecchio": bv, "blob_sim_nuovo": bn,
            "blob_strumento_vecchio": sv, "blob_strumento_nuovo": sn,
            "piattaforma_nel_referto_vecchio": bool(pv_old),
            "identiche": len(ident), "cambiate": len(camb),
            "solo_vecchio": len(solo_v), "solo_nuovo": len(solo_n),
            "cambiate_dettaglio": [{"percorso": k, "vecchio": A[k], "nuovo": B[k]}
                                   for k in camb],
            "solo_vecchio_elenco": solo_v, "solo_nuovo_elenco": solo_n,
        }

    riga("=")
    stampa("IL TOTALE")
    riga("=")
    stampa("  %d foglie identiche, %d cambiate, su %d strumenti."
           % (tot_i, tot_c, len(STRUMENTI)))
    stampa("  ### E il verdetto NON lo da' questo strumento: il mandato dice CONFRONTO,")
    stampa("      non sigillo. La causa di ogni scarto si attribuisce LEGGENDO i commit")
    stampa("      elencati sopra, e l'attribuzione va nel referto a mano, con la riga.")
    riga("=")

    fuori["totale"] = {"identiche": tot_i, "cambiate": tot_c}
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    json.dump(fuori, io.open(os.path.join(FUORI, "_confronto.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False, sort_keys=True)
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8").write(NL.join(P))
    print("scritto: %s" % os.path.join(FUORI, "_confronto.json"))
    return 0


if __name__ == "__main__":
    sys.exit(collaudo() if "--collaudo" in sys.argv[1:] else principale())
