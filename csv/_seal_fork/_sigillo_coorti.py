# -*- coding: utf-8 -*-
"""SIGILLO S0-S6 -- la PERSISTENZA delle coorti nello snapshot (mandato par.1(2)).

Progettazione e letture fissate PRIMA: doc/TASK_HISTORY/2026-09-18_coorti-tracking.md (695ced0)

S1 e' il DECISIVO: la modifica dev'essere BYTE-INERTE SULLA FISICA. Se cambia un bit, e' sbagliata.
  E S1 NON si accontenta di "salva_stato non e' sul percorso di integrazione": CHIAMA salva_stato
  DURANTE il run in ENTRAMBI i bracci, cosi' la funzione modificata viene davvero esercitata.

Il blob VECCHIO si estrae con `git cat-file -p` IN BINARIO, ANCORATO AL SUO SHA, mai `HEAD:`
(HEAD si sposta col lavoro: al primo commit della cura il "vecchio" diventerebbe il NUOVO, e il
sigillo confronterebbe il codice curato CON SE STESSO -- successo, commit c818208).
ASCII PURO.
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import _presidio
_presidio.avvia(__file__)

import hashlib
import importlib.util
import pickle
import time

import numpy as np

QUI = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(QUI, "..", ".."))
os.chdir(ROOT)

BLOB_RIF = "a1ae5090"   # git blob del simulatore PRE-CURA. ANCORATO, non "HEAD".
PASSI = 60
SEME = 5
SNAP = (20, 45)         # i passi in cui si chiama salva_stato IN ENTRAMBI i bracci
ESITI = []
TMP = os.path.join(QUI, "_tmp_coorti")
if not os.path.isdir(TMP):
    os.makedirs(TMP)


def ok(nome, cond, det=""):
    ESITI.append((nome, bool(cond)))
    print("  [%s] %-6s %s" % ("PASS" if cond else "FAIL", nome, det))


def sha_blob(p):
    b = open(p, "rb").read()
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def carica(path, nome):
    spec = importlib.util.spec_from_file_location(nome, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[nome] = m
    _argv = sys.argv
    sys.argv = ["soliton_simulator.py"]
    try:
        spec.loader.exec_module(m)
    finally:
        sys.argv = _argv
    for f in ("CAMPO_SPINORIALE", "CS_DINAMICO", "CHI_CORE", "FORK_SU2", "FORK_SU2_MEM",
              "SPINORE_CORRETTO"):
        setattr(m, f, True)
    return m


print("=" * 118)
print("SIGILLO COORTI -- S0..S6. S1 E' IL DECISIVO: BYTE-INERZIA DELLA FISICA.")
print("=" * 118)

# ------------------------------------------------------------------ S0
vecchio = os.path.join(QUI, "_old_sim_pre_coorti.py")
with open(vecchio, "wb") as fh:
    fh.write(subprocess.check_output(["git", "cat-file", "-p", BLOB_RIF]))
sv = sha_blob(vecchio)
sn = sha_blob(os.path.join(ROOT, "soliton_simulator.py"))
print("")
print("--- S0 -- i due blob ---")
ok("S0", sv[:8] == BLOB_RIF and sn[:8] != BLOB_RIF,
   "vecchio %s (atteso %s)   nuovo %s  -> DEVONO DIFFERIRE" % (sv[:8], BLOB_RIF, sn[:8]))

VEC = carica(vecchio, "_sim_vec_coorti")
NUO = carica(os.path.join(ROOT, "soliton_simulator.py"), "_sim_nuo_coorti")


def costruisci(M):
    r = M.Rete(SEME)
    r.semina(80)
    for _ in range(6):
        M.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
    Nc = M.N_CRITICO() if callable(getattr(M, "N_CRITICO", None)) else 200
    for k in range(3):
        a = 2 * np.pi * k / 3
        r.nuova_massa(int(Nc * 0.6), raggio=M._size_video(k, 0.8),
                      centro=(8.0 * np.cos(a), 8.0 * np.sin(a), 0.0), fase=0.0)
    r.aggiorna_pesi_concorrenza()
    return r


def gira(M, tag, passi=PASSI, snapshot=SNAP):
    """Gira e CHIAMA salva_stato ai passi indicati: la funzione modificata va ESERCITATA."""
    r = costruisci(M)
    t0 = time.perf_counter()
    for k in range(passi):
        M.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
        if (k + 1) in snapshot:
            r.salva_stato(os.path.join(TMP, "%s_p%d.pkl" % (tag, k + 1)))
    return r, time.perf_counter() - t0


def confronta(a, b, eti):
    """LA RIGA DELLE SHAPE PRIMA DI TUTTO: max|A-B| = 0 puo' significare NESSUN CONFRONTO."""
    campi = ["psi", "phi", "phivel", "eta", "d", "d0", "omega_s", "_nb", "pos"]
    print("    %-12s n: %d contro %d   %s" % (eti, a.n, b.n,
                                              "UGUALE" if a.n == b.n else "<- DIVERSO"))
    diverse = 0
    mx = 0.0
    conf = 0
    for c in campi:
        A = np.asarray(getattr(a, c, np.zeros(0)))
        B = np.asarray(getattr(b, c, np.zeros(0)))
        if A.shape != B.shape:
            diverse += 1
            print("      %-9s SHAPE DIVERSE %s contro %s  <- NESSUN CONFRONTO" % (c, A.shape, B.shape))
            continue
        conf += 1
        d = float(np.max(np.abs(A - B))) if A.size else 0.0
        mx = max(mx, d)
        print("      %-9s shape %-14s max|A-B| = %.3e" % (c, str(A.shape), d))
    return mx, diverse, conf


# ------------------------------------------------------------------ S4 (strumentazione, PRIMA di girare)
_rip = {"vec": 0, "nuo": 0}
for M, key in ((VEC, "vec"), (NUO, "nuo")):
    if hasattr(M.Rete, "_ripara_tracking"):
        _orig = M.Rete._ripara_tracking

        def _wrap(self, *a, __o=_orig, __k=key, **kw):
            _rip[__k] += 1
            return __o(self, *a, **kw)
        M.Rete._ripara_tracking = _wrap

# ------------------------------------------------------------------ S1 [DECISIVO]
print("")
print("--- S1 [DECISIVO] -- BYTE-INERZIA DELLA FISICA, con salva_stato CHIAMATO ai passi %s ---" % (SNAP,))
rv, tv = gira(VEC, "vec")
rn, tn = gira(NUO, "nuo")
mx, div, conf = confronta(rv, rn, "vec/nuo")
ok("S1", div == 0 and conf == 9 and mx == 0.0,
   "shape diverse = %d, campi confrontati = %d/9, max|A-B| = %.3e" % (div, conf, mx))
if div:
    print("      ^^ ATTENZIONE: con shape diverse uno zero NON sarebbe identita' (C18 di par.9).")

# ------------------------------------------------------------------ S2
print("")
print("--- S2 -- le coorti sopravvivono alla MITOSI? (si misura sui DUE bracci: era la lettura fissata) ---")


def frazione_coorte(r):
    cn = getattr(r, "conc_nodi", None)
    if not cn:
        return float("nan"), 0, 0
    m = min(len(cn), r.n)
    piene = sum(1 for k in range(m) if cn[k])
    return piene / float(m) if m else float("nan"), piene, m


for r, eti in ((rv, "VECCHIO"), (rn, "NUOVO  ")):
    f, p, m = frazione_coorte(r)
    print("    %s  n = %-6d len(conc_nodi) = %-6d  nodi con coorte NON VUOTA = %d  frazione = %.4f"
          % (eti, r.n, len(getattr(r, "conc_nodi", [])), p, f))
fv = frazione_coorte(rv)[0]
fn = frazione_coorte(rn)[0]
ok("S2", abs(fv - fn) < 1e-12 and fn > 0.5,
   "vecchio %.4f contro nuovo %.4f -> se UGUALI e ALTE, l'ereditarieta' c'era GIA' (par.1.1)" % (fv, fn))

# ------------------------------------------------------------------ S3
print("")
print("--- S3 -- ROUND-TRIP: le coorti entrano nel .pkl e tornano intere? ---")
pv = os.path.join(TMP, "vec_p45.pkl")
pn = os.path.join(TMP, "nuo_p45.pkl")
av = pickle.load(open(pv, "rb"))["attrs"]
an = pickle.load(open(pn, "rb"))["attrs"]
chiavi = ("conc_nodi", "conc_archi", "masse_info")
print("    VECCHIO  chiavi presenti in attrs: %s" % [k for k in chiavi if k in av])
print("    NUOVO    chiavi presenti in attrs: %s" % [k for k in chiavi if k in an])
assenti_vec = all(k not in av for k in chiavi)
presenti_nuo = all(k in an for k in chiavi)
ok("S3a", assenti_vec, "nel VECCHIO le tre chiavi sono ASSENTI -> il difetto e' DIMOSTRATO, non dedotto")
ok("S3b", presenti_nuo, "nel NUOVO ci sono tutte e tre")

# il round-trip vero: si ricarica in una Rete NUOVA dello STESSO codice
r2 = NUO.Rete(SEME)
r2.carica_stato(pn)
cn_disco = an["conc_nodi"]
uguale = (len(r2.conc_nodi) == len(cn_disco) and
          all(r2.conc_nodi[k] == cn_disco[k] for k in range(len(cn_disco))))
lun = len(r2.conc_nodi) >= r2.n
print("    ricaricato: len(conc_nodi) = %d, n = %d, len(conc_archi) = %d, masse_info = %d voci"
      % (len(r2.conc_nodi), r2.n, len(r2.conc_archi), len(r2.masse_info)))
ok("S3c", uguale and lun,
   "contenuto IDENTICO al disco = %s, len >= n = %s" % (uguale, lun))

# ------------------------------------------------------------------ S4
print("")
print("--- S4 -- quante volte scatta `_ripara_tracking` (un fallback mai contato e' sconosciuto, P5) ---")
print("    vecchio %d chiamate   nuovo %d chiamate   su %d passi per braccio" % (_rip["vec"], _rip["nuo"], PASSI))
ok("S4", _rip["vec"] == _rip["nuo"],
   "DEVONO essere uguali: se il nuovo ne chiama di piu', la dimensione non e' mantenuta")

# ------------------------------------------------------------------ S5
print("")
print("--- S5 -- IL COSTO: dimensione del .pkl e tempo per passo (CPU libera) ---")
zv = os.path.getsize(pv)
zn = os.path.getsize(pn)
print("    .pkl  vecchio %9d byte   nuovo %9d byte   -> +%.3f %%  (n = %d)"
      % (zv, zn, 100.0 * (zn - zv) / zv, rn.n))
print("    tempo vecchio %8.3f s      nuovo %8.3f s     -> x%.4f  (%d passi + %d snapshot)"
      % (tv, tn, tn / tv, PASSI, len(SNAP)))
print("    ATTENZIONE: il tempo su %d passi include il rumore di sistema; e' un ORDINE DI GRANDEZZA," % PASSI)
print("    non una misura fine. La lettura fissata prima era 'costo che ESPLODE', non 'costo diverso'.")
ok("S5", (zn - zv) / float(zv) < 1.0,
   "il .pkl non raddoppia (soglia dichiarata: crescita < 100 %%)")

# ------------------------------------------------------------------ S6
print("")
print("--- S6 -- il sigillo dell'ANELLO (`Z42`) regge sul blob NUOVO? ---")
print("    si rilancia `_sigillo_anello.py`, che e' ancorato al blob f8f46683 e confronta col DISCO.")
q = subprocess.run([sys.executable, os.path.join(QUI, "_sigillo_anello.py")],
                   capture_output=True, text=True)
coda = [l for l in q.stdout.splitlines() if "PASS" in l or "FAIL" in l or "/" in l][-6:]
for l in coda:
    print("      %s" % l.strip()[:110])
ok("S6", q.returncode == 0 and "FAIL" not in q.stdout,
   "returncode %d, nessun FAIL nello stdout = %s" % (q.returncode, "FAIL" not in q.stdout))

# ------------------------------------------------------------------ esito
print("")
print("=" * 118)
np_ = sum(1 for _, c in ESITI if c)
print("ESITO: %d/%d PASS   %s" % (np_, len(ESITI), " ".join("%s=%s" % (n, "P" if c else "F") for n, c in ESITI)))
print("S1 e' il decisivo: se FALLISCE, la modifica e' sbagliata e si FERMA (lettura fissata in 695ced0).")
print("=" * 118)
sys.exit(0 if np_ == len(ESITI) else 1)
