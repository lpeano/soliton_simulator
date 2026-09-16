# -*- coding: utf-8 -*-
"""SIGILLO delle DUE CORREZIONI DI DIFETTO del 2026-09-16 — M0..M5.

LE DUE CORREZIONI (categoria D del registro: un bug curato NON ha un interruttore)
----------------------------------------------------------------------------------
  (1) `_xi_rumore` NON si eredita alla mitosi: `xi` e' un campione dell'AMBIENTE, non una
      proprieta' del nodo. Il figlio riceve un campione FRESCO dalla stazionaria.
  (2) `inerzia = max(rho * (CS_M/cs_nodo)^2, 1e-6)`: il fattore `cs^-2` che la derivazione
      `inerzia = (d/cs)^2` impone e che MANCAVA.

PERCHE' IL RIFERIMENTO E' UN BLOB E NON UN FLAG
-----------------------------------------------
Senza flag non esiste la byte-identita' «a flag spento». Il riferimento e' il CODICE PRECEDENTE,
blob **a467fd9a**, salvato in `_old_sim_pre_correzioni.py`. Il confronto e' sui **BYTE GREZZI**
(`sha1("blob <len>\\0" + byte)`), **MAI** `git hash-object`: quello applica il filtro `clean` e
nasconde proprio la differenza che si sta certificando (trappola CRLF, commit `ebeb027`).

M2 E' IL SIGILLO DECISIVO, e la ragione e' precisa
---------------------------------------------------
`(CS_M/cs_nodo)^2` vale **esattamente 1** dove `cs = CS_M`, e `rho * 1.0 == rho` **bit per bit**
in IEEE. Quindi senza `--cs-dinamico` (cache mai scritta -> fallback a CS_M) il codice NUOVO deve
essere **byte-identico** al vecchio. Se non lo e', **la FORMA del fattore e' sbagliata**.

USO
---
python csv/_seal_fork/_sigillo_correzioni.py
"""
import contextlib
import hashlib
import io as _io
import os
import pickle
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PY = sys.executable
NEW = os.path.join(ROOT, "soliton_simulator.py")
OLD = os.path.join(HERE, "_old_sim_pre_correzioni.py")
BLOB_PRE = "a467fd9a4862f41d92d4483a135ff3bdd33d4f4c"
PASSI = 150
BASE = ["--batch", "--nmasse", "3", "--sep", "8", "--seed", "1", "--passi", str(PASSI),
        "--ogni", str(PASSI), "--db-ogni", str(PASSI),
        "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto", "--chi-core",
        "--calore-scal", "--deparam-orologio", "--verlet",
        "--fork-su2", "--fork-su2-mem"]

esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-50s %s" % ("PASS" if ok else "FAIL", nome, misura))


def blob_grezzo(percorso):
    """sha1 dei BYTE GREZZI, come lo calcola git ma SENZA i filtri di checkout."""
    with open(percorso, "rb") as f:
        b = f.read()
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest(), len(b), b.count(b"\r\n")


def run(sim, dbpath, extra=()):
    cmd = [PY, sim] + BASE + list(extra) + ["--csv", dbpath + ".cond.csv",
                                            "--sync-db", dbpath, "--db-cleanup"]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-1500:])
        print("STDERR:", r.stderr[-1500:])
        raise SystemExit("run FALLITO: " + " ".join(cmd[1:6]))
    with open(dbpath, "rb") as f:
        return pickle.load(f)["attrs"]


def diff(A, B):
    worst, bad = 0.0, {}
    for k in A:
        if k in B and isinstance(A[k], np.ndarray) and isinstance(B[k], np.ndarray) \
                and A[k].dtype != object:
            if A[k].shape != B[k].shape:
                bad[k] = ("SHAPE", A[k].shape, B[k].shape)
                continue
            if A[k].size:
                d = float(np.max(np.abs(A[k].astype(np.complex128) - B[k].astype(np.complex128))))
                if d > 0:
                    bad[k] = d
                worst = max(worst, d)
    return worst, bad


# ============================================================ M0: il riferimento
print("=" * 106)
print("M0 — IL RIFERIMENTO: blob PRE-correzioni, certificato sui BYTE GREZZI (non git hash-object)")
print("=" * 106)
h_old, n_old, crlf_old = blob_grezzo(OLD)
h_new, n_new, crlf_new = blob_grezzo(NEW)
verdetto("M0 il riferimento e' il blob a467fd9a", h_old == BLOB_PRE,
         "sha1 grezzo = %s  (atteso %s);  %d byte, %d CRLF" % (h_old[:12], BLOB_PRE[:12], n_old, crlf_old))
verdetto("M0b il codice corrente e' DIVERSO dal riferimento", h_new != BLOB_PRE,
         "corrente = %s;  %d byte, %d CRLF" % (h_new[:12], n_new, crlf_new))
verdetto("M0c nessuno dei due ha CRLF (.gitattributes in vigore)", crlf_old == 0 and crlf_new == 0,
         "CRLF: riferimento %d, corrente %d" % (crlf_old, crlf_new))

# ============================================================ M2: IL DECISIVO
print()
print("=" * 106)
print("M2 — IL DECISIVO: con cs = CS_M il fattore vale ESATTAMENTE 1 -> BYTE-IDENTICO al riferimento")
print("=" * 106)
print("  Senza `--cs-dinamico` la cache `_cs_nodo_prev` non viene MAI scritta, quindi il fallback")
print("  da' cs = CS_M per tutti, `(CS_M/cs)^2 = 1.0` e `rho * 1.0 == rho` bit per bit.")
print("  E senza `--rumore-colorato` la correzione (1) e' un no-op: `_xi_rumore` non esiste.")
A = run(OLD, os.path.join(HERE, "_m2_old.pkl"))
B = run(NEW, os.path.join(HERE, "_m2_new.pkl"))
nA, nB = len(A.get("phi", ())), len(B.get("phi", ()))
# PRESIDIO (2026-09-14): PRIMA le shape. Uno zero su shape diverse e' MANCANZA DI CONFRONTO.
verdetto("M2.0 stesso numero di nodi (il confronto ESISTE)", nA == nB and nA > 0,
         "nodi: PRE = %d, POST = %d" % (nA, nB))
w2, b2 = diff(A, B)
verdetto("M2 cs = CS_M -> byte-identico al blob a467fd9a", w2 == 0.0 and not b2,
         "max|A-B| = %.3e%s" % (w2, "" if not b2 else "  DIVERGENTI: " + str(list(b2)[:5])))

print()
print("  M2b — CONTROLLO POSITIVO: con `--cs-dinamico` il fattore NON e' 1 e i due DEVONO differire")
Ad = run(OLD, os.path.join(HERE, "_m2_old_cs.pkl"), extra=["--cs-dinamico"])
Bd = run(NEW, os.path.join(HERE, "_m2_new_cs.pkl"), extra=["--cs-dinamico"])
w2b, b2b = diff(Ad, Bd)
verdetto("M2b con cs VIVO il fattore MORDE (i due differiscono)", bool(b2b),
         "nodi PRE = %d, POST = %d;  array divergenti %d;  max|A-B| = %.3e"
         % (len(Ad.get("phi", ())), len(Bd.get("phi", ())), len(b2b), w2b))

# ============================================================ in-process: M1, M3, M4, M5
print()
print("=" * 106)
print("M1, M3, M4, M5 — in-process, con spie PURE-READ su `_eredita_spinore_figli` e `rng`")
print("=" * 106)
sys.path.insert(0, ROOT)
os.chdir(ROOT)


def carica(percorso, nome, extra=()):
    """Carica un modulo (vecchio o nuovo) con l'argv giusto. Copia da `_rimisura_t3.py`."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(nome, percorso)
    M = importlib.util.module_from_spec(spec)
    sys.modules[nome] = M
    sys.argv = ["soliton_simulator.py"] + BASE + list(extra) + [
        "--passi", "1", "--csv", os.path.join(HERE, "_mcorr.csv")]
    with contextlib.redirect_stdout(_io.StringIO()):
        spec.loader.exec_module(M)
        a = M._cli(); M._applica_regime(a); M._applica_flag(a)
    return M


def passo(M, net):
    M.scuoti_vuoto(net); net.step(); net.mitosi()
    net.rilassa_disegno(); net.memoria_hebbiana_moto()


def scena(M, seed, n_passi):
    net = M.Rete(seed); net.semina(80)
    for _ in range(6):
        passo(M, net)
    Nc = M.massa_critica_collasso()
    for k in range(3):
        ang = 2 * np.pi * k / 3
        net.nuova_massa(int(Nc * 0.6), raggio=0.8,
                        centro=(8.0 * np.cos(ang), 8.0 * np.sin(ang), 0.0), fase=0.0)
    for _ in range(n_passi):
        passo(M, net)
    return net


def L_tot(M, net):
    """L = somma(inerzia_i * |omega_i|). LA QUANTITA' CHE DOVREBBE CONSERVARSI.
    L'inerzia si ricostruisce come la calcola il modulo CHE STA GIRANDO, fattore incluso se c'e'."""
    n = net.n
    om = np.asarray(getattr(net, "omega_s", np.zeros((0, 3))), float)
    if len(om) < n:
        return float("nan")
    rho = np.asarray(net._rho_sorgente(), float)[:n]
    f = np.ones(n)
    csp = getattr(net, "_cs_nodo_prev", None)
    if getattr(M, "_HA_FATTORE_CS", None) is None:
        # il modulo NUOVO scrive `_fatt_cs_ultimo`; il vecchio no
        ha = hasattr(net, "_fatt_cs_ultimo")
    else:
        ha = bool(M._HA_FATTORE_CS)
    if ha and csp is not None and len(csp) >= n:
        f = (M.CS_M / np.maximum(np.asarray(csp, float)[:n], 1e-12)) ** 2
    inz = np.maximum(rho * f, 1e-6)
    return float(np.sum(inz * np.linalg.norm(om[:n], axis=1)))


class SpiaNascite(object):
    """Registra (src, n0) di ogni `_eredita_spinore_figli`: da li' si sa CHI e' figlio DI CHI.
    Pure-read: inoltra la chiamata vera e non tocca nulla."""
    def __init__(self, M):
        self.M = M
        self.eventi = []
        self._orig = M.Rete._eredita_spinore_figli

    def __enter__(self):
        orig, ev = self._orig, self.eventi

        def spia(selfn, src, segno=1):
            n0 = selfn.n - len(np.asarray(src, int))
            ev.append((np.asarray(src, int).copy(), int(n0), int(selfn.n)))
            return orig(selfn, src, segno)
        self.M.Rete._eredita_spinore_figli = spia
        return self

    def __exit__(self, *e):
        self.M.Rete._eredita_spinore_figli = self._orig
        return False


def corr_xi(M, seed, n_scena=20, n_dopo=1):
    """corr(xi_figlio, xi_padre) subito dopo una mitosi. PRIMA della correzione dev'essere ~a^2,
    DOPO ~0. E' il sigillo della correzione (1)."""
    net = scena(M, seed, n_scena)
    coppie = []
    for _ in range(12):
        with SpiaNascite(M) as sp:
            passo(M, net)
        xi = getattr(net, "_xi_rumore", None)
        if xi is None:
            continue
        xi = np.asarray(xi, float)
        for src, n0, n1 in sp.eventi:
            for k, pad in enumerate(src):
                fig = n0 + k
                if fig < len(xi) and pad < len(xi):
                    coppie.append((xi[pad].copy(), xi[fig].copy()))
        if len(coppie) >= 200:
            break
    if not coppie:
        return float("nan"), 0
    P = np.array([c[0] for c in coppie]).ravel()
    F = np.array([c[1] for c in coppie]).ravel()
    if P.size < 3 or np.std(P) == 0 or np.std(F) == 0:
        return float("nan"), len(coppie)
    return float(np.corrcoef(P, F)[0, 1]), len(coppie)


print()
print("  M1 — correlazione `xi` PADRE-FIGLIO subito dopo la mitosi (serve `--rumore-colorato`)")
print("     PRIMA della correzione: il figlio COPIA xi dal padre -> dopo un passo entrambi valgono")
print("     a*xi_padre + b*g con g DIVERSI, quindi corr attesa ~ a^2 = %.4f." % (np.exp(-0.01/0.4)**2))
print("     DOPO: il figlio ha un campione FRESCO e indipendente -> corr attesa ~ 0.")
M_old = carica(OLD, "m_old_rc", ["--rumore-colorato"])
c_old, n_old_c = corr_xi(M_old, 7)
M_new = carica(NEW, "m_new_rc", ["--rumore-colorato"])
c_new, n_new_c = corr_xi(M_new, 7)
print("     PRE-correzione : corr = %+.4f  su %d coppie padre-figlio" % (c_old, n_old_c))
print("     POST-correzione: corr = %+.4f  su %d coppie padre-figlio" % (c_new, n_new_c))
verdetto("M1 PRIMA il rumore padre-figlio era CORRELATO", np.isfinite(c_old) and abs(c_old) > 0.5,
         "corr = %+.4f  (il difetto ESISTEVA: senza questo, M1b non proverebbe nulla)" % c_old)
verdetto("M1b DOPO il rumore padre-figlio e' INDIPENDENTE",
         np.isfinite(c_new) and abs(c_new) < 0.15,
         "corr = %+.4f  su %d coppie" % (c_new, n_new_c))

print()
print("  M3 — `len(_xi_rumore) == n` dopo ogni passo, e i contatori (P5)")
net3 = scena(M_new, 3, 5)
ok3, nodi = True, []
for _ in range(25):
    passo(M_new, net3)
    nodi.append(net3.n)
    if len(getattr(net3, "_xi_rumore", ())) != net3.n:
        ok3 = False
verdetto("M3 len(_xi_rumore) == n dopo OGNI passo", ok3,
         "25 passi, n da %d a %d;  estensioni %s, nodi con xi fresco %s, chiamate %s"
         % (nodi[0], nodi[-1], getattr(net3, "_xi_esteso", "n/d"),
            getattr(net3, "_xi_nuovi", "n/d"), getattr(net3, "_xi_chiamate", "n/d")))

print()
print("  M4 — CONSERVAZIONE: `L_tot = somma(inerzia * |omega|)` e il suo salto per mitosi")
print("     E' il test di conservazione MAI FATTO. Se L cresce col numero di nodi, la violazione")
print("     e' MISURATA, non argomentata. Qui si confronta PRE e POST correzione (2).")
for eti, M in (("PRE ", M_old), ("POST", M_new)):
    net4 = scena(M, 11, 15)
    serie, nn = [], []
    for _ in range(20):
        L0, n_0 = L_tot(M, net4), net4.n
        passo(M, net4)
        L1, n_1 = L_tot(M, net4), net4.n
        if np.isfinite(L0) and np.isfinite(L1) and L0 > 0 and n_1 > n_0:
            serie.append((L1 - L0) / L0)
            nn.append(n_1 - n_0)
    if serie:
        print("     %s  eventi di crescita %2d   Delta L / L per passo: mediana %+.4f   media %+.4f"
              "   nodi nati totali %d" % (eti, len(serie), float(np.median(serie)),
                                          float(np.mean(serie)), int(np.sum(nn))))
    else:
        print("     %s  nessun evento di crescita utilizzabile" % eti)
verdetto("M4 la metrica di conservazione e' calcolabile", True,
         "riportata sopra: NON e' un PASS/FAIL, e' una MISURA (vedi la nota in coda)")

print()
print("  M5 — stabilita' sul run con `--cs-dinamico` (dal DB di M2b)")
nbD = np.asarray(Bd.get("_nb"), float)
nrm = np.linalg.norm(nbD, axis=1) if nbD.ndim == 2 and nbD.size else np.array([np.nan])
finiti = all(np.all(np.isfinite(np.asarray(Bd[k], dtype=np.complex128)))
             for k in Bd if isinstance(Bd[k], np.ndarray) and Bd[k].dtype != object and Bd[k].size)
scala = float(np.max(np.abs(np.asarray(Bd.get("pos"), float)))) if Bd.get("pos") is not None else np.nan
verdetto("M5a |nb| = 1 su tutti i nodi", float(np.max(np.abs(nrm - 1.0))) < 1e-9,
         "max| |nb| - 1 | = %.3e su %d nodi" % (float(np.max(np.abs(nrm - 1.0))), len(nrm)))
verdetto("M5b nessun NaN/inf in tutto lo stato", finiti, "tutti finiti")
verdetto("M5c nessun runaway di scala", np.isfinite(scala) and scala < 1e6, "max|x| = %.4g" % scala)

print()
print("=" * 106)
print("SIGILLO CORREZIONI: %d/%d PASS -> %s"
      % (sum(esiti), len(esiti), "PASS" if all(esiti) else "FAIL"))
print("=" * 106)
print("""COSA QUESTO SIGILLO NON DICE
---------------------------
Che le due correzioni CAMBINO qualcosa di misurabile OGGI. Per la (2) e' scritto PRIMA che NON lo
fara': `cs_std/cs_medio` sta fra 0.0086 % e 0.24 % (C13), quindi `(CS_M/cs)^2` e' quasi 1 ovunque.
Si sono fatte perche' senza le leggi sono SBAGLIATE, non per un effetto atteso.
M4 non e' un PASS/FAIL: e' la PRIMA misura della conservazione di `L_tot` mai fatta su questo
sistema, e il suo verdetto e' un numero, non un timbro.""")
sys.exit(0 if all(esiti) else 1)
