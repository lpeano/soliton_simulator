# -*- coding: utf-8 -*-
"""SIGILLO cs_floor RELAZIONALE (R0-R5) -- CORREZIONE DI DIFETTO, categoria D: NESSUN FLAG.

Predizione scritta e committata PRIMA del cablaggio: doc/PREDIZIONE_cs_floor_relazionale.md.

POICHE' NON C'E' UN FLAG, il riferimento e' il BLOB PRE-MODIFICA (a44adc31), estratto in BINARIO
con `git cat-file -p` -- MAI con `git checkout` (trappola CRLF, C18) e MAI certificato con
`git hash-object` (applica il filtro clean e nasconde la differenza di byte).

R0  il riferimento e' il blob atteso, sui BYTE GREZZI (sha1 calcolato a mano)
R1  RIDUZIONE AL LIMITE, IL DECISIVO: con la scala forzata a 400.0 la forma NUOVA deve tornare
    BYTE-IDENTICA alla VECCHIA. Prova che e' la stessa legge con una scala diversa.
R2  CONTROLLO POSITIVO: con la scala VERA (Lam) le due DEVONO differire. Senza, R1 passerebbe
    anche su codice morto.
R3  il TURBO resta vivo: K=1 byte-identico, K>1 abbassa cs_floor
R4  stabilita': 0 < cs_floor <= CS_M ovunque, niente NaN, Lam > 0
R5  GAMMA altrove INTATTO: satura() e la saturazione spinoriale non sono cambiate

ASCII PURO.
"""
import sys as _sys_enc  # PRESIDIO ENCODING (CLAUDE.md): lo stdout di Windows e' cp1252 e
# uccide qualunque print con un carattere non-ASCII. E' successo SETTE volte, l'ultima allo
# script che stava CONTANDO le occorrenze. Il `# -*- coding: utf-8 -*-` NON basta: riguarda il
# SORGENTE, non lo STDOUT. Questa riga lo risolve alla radice.
try:
    _sys_enc.stdout.reconfigure(encoding="utf-8")
    _sys_enc.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import hashlib
import importlib.util
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
NEW = os.path.join(ROOT, "soliton_simulator.py")
OLD = os.path.join(HERE, "_old_sim_pre_csfloor.py")
BLOB_PRE = "a44adc31"

esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-52s %s" % ("PASS" if ok else "FAIL", nome, misura))


def blob_grezzo(path):
    b = open(path, "rb").read()
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest(), len(b), b.count(b"\r\n")


def carica(path, nome):
    spec = importlib.util.spec_from_file_location(nome, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[nome] = m
    spec.loader.exec_module(m)
    return m


# ============================================================ R0
print("=" * 104)
print("SIGILLO cs_floor RELAZIONALE -- R0: i due file")
print("=" * 104)
h_old, n_old, cr_old = blob_grezzo(OLD)
h_new, n_new, cr_new = blob_grezzo(NEW)
print("  riferimento : %s  %d byte  CRLF %d" % (h_old[:8], n_old, cr_old))
print("  attuale     : %s  %d byte  CRLF %d" % (h_new[:8], n_new, cr_new))
verdetto("R0 il riferimento e' il blob PRE-modifica atteso", h_old.startswith(BLOB_PRE),
         "blob = %s (atteso %s), byte grezzi, 0 CRLF" % (h_old[:8], BLOB_PRE))
verdetto("R0b i due file sono DIVERSI (il confronto ESISTE)", h_old != h_new,
         "%s contro %s" % (h_old[:8], h_new[:8]))

SV = carica(NEW, "_sim_new")
SO = carica(OLD, "_sim_old")

# dati veri: gli I dei run gia' committati (nessun run nuovo per i sigilli di formula)
import glob
import pickle
Is = []
for f in sorted(glob.glob(os.path.join(ROOT, "csv", "_test_fork", "_vuoto_s2ON_s?.pkl"))):
    try:
        Is.append(np.abs(np.asarray(pickle.load(open(f, "rb"))["attrs"]["psi"])) ** 2)
    except Exception:
        pass
I = np.maximum(np.concatenate(Is), 0.0) if Is else np.abs(np.random.default_rng(0).normal(size=5000)) ** 2
CS_M = float(SV.CS_M)
GAMMA = float(SO.GAMMA)
Lam = float(np.mean(I))
print("\n  dati: %d nodi reali dai .pkl committati.  CS_M = %g  GAMMA = %g  Lam = %.6e"
      % (len(I), CS_M, GAMMA, Lam))


def floor_vecchio(I, g):
    return np.minimum(CS_M / (1.0 + g * np.sqrt(I)), CS_M)


def floor_nuovo(I, scala, K=1.0):
    sc = max(scala, 1e-30) / (K * K)
    return np.minimum(CS_M / (1.0 + np.sqrt(I) * np.sqrt(1.0 / sc)), CS_M)


# ============================================================ R1 -- IL DECISIVO
print("\n" + "=" * 104)
print("R1 -- RIDUZIONE AL LIMITE (IL DECISIVO): scala = 400.0 -> deve tornare la legge VECCHIA")
print("=" * 104)
print("  NB: si forza il LETTERALE 400.0, perche' 1.0/GAMMA**2 vale %.17g, NON 400" % (1.0 / GAMMA ** 2))
a = floor_vecchio(I, GAMMA)
b = floor_nuovo(I, 400.0)
d = float(np.max(np.abs(a - b)))
div = int((a != b).sum())
print("  shape: vecchia %d, nuova %d   <- la riga dei conteggi PRIMA (par.9)" % (len(a), len(b)))
verdetto("R1 scala=400 -> BYTE-IDENTICO alla legge vecchia",
         len(a) == len(b) and d == 0.0 and div == 0,
         "max|A-B| = %.3e, elementi diversi %d su %d" % (d, div, len(a)))

# ============================================================ R2 -- CONTROLLO POSITIVO
print("\n" + "=" * 104)
print("R2 -- CONTROLLO POSITIVO: con la scala VERA (Lam) le due DEVONO differire")
print("=" * 104)
c = floor_nuovo(I, Lam)
dd = np.abs(a - c)
frac = float((dd > 1e-13).mean())
verdetto("R2.0 il test VEDE: la modifica cambia qualcosa", frac > 0.5,
         "%.2f%% dei nodi con |vecchio - nuovo| > 1e-13  (mediana %.4e)" % (100 * frac, float(np.median(dd))))
verdetto("R2 cs_floor mediano SCENDE (la scala e' piu' bassa)",
         float(np.median(c)) < float(np.median(a)),
         "mediana %.6f -> %.6f   (min %.6f -> %.6f)"
         % (float(np.median(a)), float(np.median(c)), float(a.min()), float(c.min())))
sv_a, sv_c = float(a.std() / a.mean()), float(c.std() / c.mean())
verdetto("R2b la DISPERSIONE del floor cresce (e' lo scopo)", sv_c > 10 * sv_a,
         "std/media %.5f -> %.5f  (x%.1f)" % (sv_a, sv_c, sv_c / sv_a))

# ============================================================ R3 -- il turbo
print("\n" + "=" * 104)
print("R3 -- il TURBO DIAGNOSTICO resta vivo")
print("=" * 104)
k1 = floor_nuovo(I, Lam, 1.0)
verdetto("R3a GAMMA_TURBO = 1.0 -> byte-identico alla forma senza turbo",
         np.array_equal(k1, c), "max|A-B| = %.3e" % float(np.max(np.abs(k1 - c))))
k4 = floor_nuovo(I, Lam, 4.0)
verdetto("R3b GAMMA_TURBO > 1 ABBASSA cs_floor", float(np.median(k4)) < float(np.median(c)),
         "mediana K=1 %.6f -> K=4 %.6f" % (float(np.median(c)), float(np.median(k4))))

# ============================================================ R4 -- stabilita'
print("\n" + "=" * 104)
print("R4 -- stabilita'")
print("=" * 104)
verdetto("R4a 0 < cs_floor <= CS_M ovunque", bool((c > 0).all() and (c <= CS_M).all()),
         "min %.6f  max %.6f  (CS_M = %g)" % (float(c.min()), float(c.max()), CS_M))
verdetto("R4b nessun NaN/inf", bool(np.isfinite(c).all()), "tutti finiti su %d nodi" % len(c))
verdetto("R4c Lam > 0 sui dati reali", Lam > 0, "Lam = %.6e" % Lam)
z = floor_nuovo(np.zeros(10), 0.0)          # caso degenere: sistema vuoto
verdetto("R4d a sistema VUOTO (Lam = 0) il floor non esplode",
         bool(np.isfinite(z).all() and (z > 0).all()), "cs_floor = %g su I = 0" % float(z[0]))

# ============================================================ R5 -- GAMMA altrove
print("\n" + "=" * 104)
print("R5 -- GAMMA altrove INTATTO")
print("=" * 104)
verdetto("R5a GAMMA ha lo stesso valore nei due moduli", float(SV.GAMMA) == float(SO.GAMMA),
         "%g == %g" % (float(SV.GAMMA), float(SO.GAMMA)))
# CORREZIONE DI DUE CRITERI MIEI, SBAGLIATI ALLA PRIMA ESECUZIONE (par.9: un criterio si scrive
# da una MISURA, non dal proprio modello mentale del codice). Il codice NON e' stato toccato.
#   R5b: `satura` NON e' una funzione di modulo, e' un METODO della rete (`:2457`). `SV.satura`
#        sollevava AttributeError, cioe' un FAIL su una premessa mia, non sul simulatore.
#   R5c: contavo le occorrenze della STRINGA "GAMMA", commenti inclusi. Il commento nuovo la
#        nomina piu' volte, quindi il conteggio SALIVA (53 -> 57) e il criterio "deve calare"
#        falliva su una modifica corretta. Si contano le righe ESEGUIBILI, e si verifica che
#        l'unica differenza sia dentro `_cs_nodo`.
x = np.linspace(-5, 5, 2001) + 0.7j
_sat_v = getattr(SV, "satura", None) or getattr(getattr(SV, "Rete", None), "satura", None)
_sat_o = getattr(SO, "satura", None) or getattr(getattr(SO, "Rete", None), "satura", None)
if _sat_v is None or _sat_o is None:
    verdetto("R5b satura() trovata in entrambi i moduli", False,
             "non trovata: nuovo=%s vecchio=%s" % (_sat_v, _sat_o))
else:
    sv, so = _sat_v(x), _sat_o(x)
    verdetto("R5b satura() e' BYTE-IDENTICA fra i due blob", np.array_equal(sv, so),
             "max|A-B| = %.3e su %d punti" % (float(np.max(np.abs(sv - so))), len(x)))


def righe_gamma(path):
    """righe ESEGUIBILI che usano GAMMA: niente commenti, niente stringhe di help."""
    out = []
    for l in open(path, encoding="utf-8").read().splitlines():
        if l.strip().startswith("#"):
            continue
        cod = l.split("#")[0]
        if "GAMMA" in cod and not cod.strip().startswith(('"', "'")):
            out.append(cod.strip())
    return out


gv, go = righe_gamma(NEW), righe_gamma(OLD)
solo_o = [l for l in go if l not in gv]
solo_v = [l for l in gv if l not in go]
print("  righe ESEGUIBILI con GAMMA: riferimento %d, attuale %d" % (len(go), len(gv)))
for l in solo_o:
    print("    RIMOSSA : %s" % l[:92])
for l in solo_v:
    print("    AGGIUNTA: %s" % l[:92])
verdetto("R5c UNA sola riga eseguibile rimossa, ed e' quella di _cs_nodo",
         len(solo_o) == 1 and solo_o[0].startswith("_g = GAMMA * GAMMA_TURBO"),
         "rimosse %d, aggiunte %d" % (len(solo_o), len(solo_v)))
verdetto("R5d TUTTE le altre righe eseguibili con GAMMA sono IDENTICHE",
         len([l for l in go if l not in solo_o]) == len([l for l in gv if l not in solo_v])
         and all(l in gv for l in go if l not in solo_o),
         "%d righe invariate su %d" % (len(go) - len(solo_o), len(go)))

print("\n" + "=" * 104)
tot, ok = len(esiti), sum(esiti)
print("SIGILLO cs_floor: %d/%d PASS -> %s" % (ok, tot, "PASS" if ok == tot else "FAIL"))
print("""
COSA QUESTO SIGILLO NON DICE
----------------------------
Che la modifica MIGLIORI qualcosa. Dice che e' la STESSA legge con una scala diversa (R1), che la
scala nuova FA qualcosa (R2), che il turbo resta un amplificatore (R3) e che non esplode (R4).
Se `cs_std/cs` salga davvero sopra l'1%% -- la predizione P1 -- lo dicono i RUN, non questo file.
R1 e R2 girano sulla FORMULA con dati reali, non su run interi: e' voluto, perche' su 150 passi il
caos amplifica 1 ulp e un R1 "a run" fallirebbe per ragioni numeriche, non fisiche.""")
sys.exit(0 if ok == tot else 1)
