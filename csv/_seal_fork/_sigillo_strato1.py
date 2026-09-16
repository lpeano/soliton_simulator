# -*- coding: utf-8 -*-
"""SIGILLO STRATO 1 — connessione con MEMORIA (ritardazione tau = d/cs), flag --fork-su2-mem.

PERCHE' ESISTE QUESTO PEZZO
---------------------------
Lo Strato 0 (PEZZO 3) e' INERTE per TEOREMA, non per bug: la connessione N_ij e' costruita dai
Bloch DEGLI STESSI spinori che trasporta, nello STESSO istante, quindi |psi_i> e' autovettore di
(n_i.sigma) e <psi_i|N_ij|psi_j> = 2<psi_i|psi_j> esatto (misurato 1.570e-15, _reperto_inerzia.py).
La forza non cambia di un bit.

La causa e' la SIMULTANEITA': una mappa costruita ORA, dagli stati di ORA, non puo' muovere gli
stati di ORA. La cura e' la CAUSALITA' (cono di luce), non una taratura: la connessione nasce dai
Bloch a t-tau, con tau = d/cs (tempo-luce dell'arco, zero parametri nuovi). Con il ritardo psi(t)
NON e' piu' autovettore di n(t-tau).sigma -> il teorema non si applica -> la forza cambia.

I SIGILLI (CLAUDE.md par.2)
---------------------------
  S1  OFF byte-identico            flag MEM spento -> max|A-B| = 0.000e+00 vs il codice pre-modifica
  S2  riduzione allo Strato 0      tau -> 0 (alpha -> 1) -> il ritardato E' il corrente, esatto
  S3  IL DECISIVO                  _nb_ret != _nb_cur -> la forza DIFFERISCE dal ramo scalare
  S3b IL DECISIVO, NEL CICLO VERO  stessa domanda posta alla dinamica reale, non a stati sintetici
  S4  stabilita' / unitarieta'     |_nb_ret| = 1, nessun NaN/inf, nessun runaway (run vero)
  S5  azione-reazione              la somma della coppia resta nulla (N_ji = N_ij^dag)
  S6  a riposo = scalare           Bloch fermi -> _nb_ret = _nb_cur -> nessuna forza inventata
  S7  il tic e' il TEMPO PROPRIO   alpha = 1-exp(-DT*r/tau): col DT globale S7 FALLISCE, S1..S6 no

COSA QUESTO SIGILLO NON DICE (par.8, verbo onesto)
--------------------------------------------------
S3 dice che la forza CAMBIA, non che sia FISICA. Rompere il teorema e' garantito per costruzione;
che la dinamica risultante sia sensata (olonomia, stabilita' lunga, verso della gravita') lo dice
un RUN, non l'algebra. Nessuna conclusione fisica sotto ~2000 passi e mai su un solo seme (par.2.7):
qui si conclude solo sul MECCANISMO.
"""
import io
import os
import pickle
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
NEW = os.path.join(ROOT, "soliton_simulator.py")
OLD = os.path.join(HERE, "_old_sim_pre_strato1.py")
# Riferimento ancorato a un commit FISSO, MAI a HEAD: appena il lavoro viene committato, un sigillo
# ancorato a HEAD confronta il nuovo codice con SE STESSO e si auto-assolve (bug gia' preso una
# volta in _sigillo_pezzo3.py, 2026-09-13). In piu' si verifica che il blob estratto sia proprio
# quello certificato del PEZZO 3: il commit puo' "mentire", il blob no (par.2.6).
PRE = "af003c2"                                   # ultimo commit PRIMA dello Strato 1
BLOB_PRE = "968fba34dedfcfb7faf2209a15ebf145c21f52e8"
PY = sys.executable
# [2026-09-16] `--cs-dinamico` AGGIUNTO. Senza, `cs = CS_M` costante e `_cs_nodo_prev` non viene
# MAI scritta: il ritardo girava su `tau = d/CS_M`, cioe' su `tau ∝ d`, e la dipendenza da `cs`
# non era esercitata. E' il MARCHIO di CLAUDE.md par.9 sul 23/23 di questo stesso sigillo.
BASE = ["--batch", "--nmasse", "3", "--sep", "8", "--seed", "1", "--passi", "150",
        "--ogni", "150", "--db-ogni", "150",
        "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto", "--chi-core",
        "--calore-scal", "--deparam-orologio", "--verlet", "--cs-dinamico"]

esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-48s %s" % ("PASS" if ok else "FAIL", nome, misura))


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
    """max|A-B| su tutti gli array numerici COMUNI; segnala le shape diverse."""
    worst = 0.0
    bad = {}
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


# ============================================================ S1: OFF = BYTE-IDENTICO (run veri)
print("=" * 96)
print("SIGILLO 1 — FLAG MEM OFF = BYTE-IDENTICO al codice pre-Strato 1 (run veri, 150 passi, seed 1)")
print("=" * 96)
if not os.path.exists(OLD):
    # ESTRAZIONE BINARIA, non testuale: con text=True git restituisce newline universali (\n) e il
    # file riscritto avrebbe un BLOB DIVERSO dall'originale (CRLF). Il blob e' il timbro (par.2.6):
    # va conservato byte per byte, altrimenti il controllo S1.0 qui sotto non vale nulla.
    src = subprocess.run(["git", "show", PRE + ":soliton_simulator.py"], cwd=ROOT,
                         capture_output=True)
    with open(OLD, "wb") as f:
        f.write(src.stdout)
    print("  (creato %s da %s = codice PRIMA dello Strato 1)" % (os.path.basename(OLD), PRE))
blob_old = subprocess.run(["git", "hash-object", OLD], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
verdetto("S1.0 il riferimento e' il blob certificato del PEZZO 3", blob_old == BLOB_PRE,
         "blob(%s) = %s  (atteso %s)" % (os.path.basename(OLD), blob_old[:8], BLOB_PRE[:8]))

A = run(OLD, os.path.join(HERE, "_s1_old.pkl"), extra=["--fork-su2"])
B = run(NEW, os.path.join(HERE, "_s1_off.pkl"), extra=["--fork-su2"])
worst, bad = diff(A, B)
verdetto("S1a fork ON, MEM OFF vs codice pre-Strato 1", worst == 0.0 and not bad,
         "max|A-B| = %.3e%s" % (worst, "" if not bad else "  DIVERGENTI: " + str(list(bad)[:5])))

A0 = run(OLD, os.path.join(HERE, "_s1_old_base.pkl"))
B0 = run(NEW, os.path.join(HERE, "_s1_off_base.pkl"))
worst0, bad0 = diff(A0, B0)
verdetto("S1b baseline (fork OFF) vs codice pre-Strato 1", worst0 == 0.0 and not bad0,
         "max|A-B| = %.3e%s" % (worst0, "" if not bad0 else "  DIVERGENTI: " + str(list(bad0)[:5])))

# ============================================================ run con MEM ON (serve a S4)
print()
print("=" * 96)
print("RUN CON MEMORIA ACCESA (150 passi, seed 1) — materiale per S4")
print("=" * 96)
C = run(NEW, os.path.join(HERE, "_s1_mem.pkl"), extra=["--fork-su2", "--fork-su2-mem"])
w_mem, bad_mem = diff(B, C)
n_s0 = len(B.get("phi", ()))
n_s1 = len(C.get("phi", ()))
print("  nodi a fine run: Strato 0 = %d, Strato 1 = %d" % (n_s0, n_s1))
print("  array con SHAPE DIVERSA fra i due run: %d su %d confrontabili"
      % (sum(1 for v in bad_mem.values() if isinstance(v, tuple) and v[0] == "SHAPE"), len(bad_mem)))
print("  max|Strato0 - Strato1| sugli array di shape UGUALE = %.3e" % w_mem)
print("""  ATTENZIONE ALLA LETTURA DI QUESTI NUMERI (trappola gia' scattata una volta, 2026-09-14):
      se i due run divergono abbastanza da cambiare il NUMERO DI NODI, nessun array e' piu'
      confrontabile per shape e "max|A-B|" resta 0.000e+00 per MANCANZA DI CONFRONTO, non per
      identita'. Guardare sempre PRIMA la riga delle shape. E comunque:
      questo NON e' un sigillo. Su 150 passi il sistema e' caotico e anche un arrotondamento a
      1e-16 si amplifica fino a cambiare le mitosi (lezione del 2026-09-13). Le prove che il
      meccanismo si e' acceso sono S3 (forza, orizzonte ZERO) e S3b (ciclo dinamico vero).""")

# ============================================================ S4: stabilita' / unitarieta'
print()
print("=" * 96)
print("SIGILLO 4 — |_nb_ret| = 1, nessun NaN/inf, nessun runaway (run con MEM ON)")
print("=" * 96)
nbr = C.get("_nb_ret")
if nbr is not None and len(nbr):
    nor = np.linalg.norm(np.asarray(nbr, float), axis=1)
    err = float(np.max(np.abs(nor - 1.0)))
    verdetto("S4a |_nb_ret| = 1 su tutti i nodi", err < 1e-12,
             "max| |n_ret| - 1 | = %.3e su %d nodi" % (err, len(nor)))
else:
    verdetto("S4a |_nb_ret| = 1 su tutti i nodi", False,
             "_nb_ret ASSENTE nello stato salvato: la memoria non e' mai nata")
psp = C.get("_psi_spinor")
nps = np.linalg.norm(np.asarray(psp), axis=1) if psp is not None and len(psp) else np.array([])
verdetto("S4b norma |psi| = 1 sullo spinore", nps.size and np.max(np.abs(nps - 1.0)) < 1e-9,
         "max| |psi| - 1 | = %.3e su %d nodi" % (float(np.max(np.abs(nps - 1.0))) if nps.size
                                                 else float("nan"), nps.size))
finiti = all(np.all(np.isfinite(v)) for v in C.values()
             if isinstance(v, np.ndarray) and v.dtype != object
             and np.issubdtype(v.dtype, np.number))
verdetto("S4c nessun NaN/inf in tutto lo stato", finiti, "tutti finiti")
pos = C.get("x", C.get("pos"))
scala = float(np.max(np.abs(np.asarray(pos, float)))) if pos is not None and len(pos) else float("nan")
verdetto("S4d nessun runaway di scala nella finestra", np.isfinite(scala) and scala < 1e6,
         "max|x| = %.4g" % scala)

# ============================================================ S2/S3/S5/S6: in-process, sul PERCORSO REALE
print()
print("=" * 96)
print("SIGILLI 2, 3, 5, 6 — in-process sui METODI REALI (_bloch_ritardato + _coppia_interferenza)")
print("=" * 96)
sys.path.insert(0, ROOT)
import soliton_simulator as S  # noqa: E402


class FintaRete(object):
    """Guscio minimo: espone solo cio' che `_coppia_interferenza` e `_bloch_ritardato` usano
    (n, i, j, d, _psi_spinor, _nb_ret, _cs_nodo_prev, struttura sparsa). Non fa fisica: serve a
    confrontare i RAMI sullo STESSO stato, chiamando le funzioni VERE del simulatore."""
    _S = None
    _perm = None
    n = 0
    i = None
    j = None
    d = None
    _nb_ret = None
    _cs_nodo_prev = None

    _costruisci_struttura = S.Rete._costruisci_struttura
    _mat = S.Rete._mat
    _mat2 = S.Rete._mat2
    _link_su2_N = staticmethod(S.Rete._link_su2_N)
    _bloch_ritardato = S.Rete._bloch_ritardato
    _coppia_interferenza = S.Rete._coppia_interferenza
    # [FIX 2026-09-16] SENZA QUESTA RIGA IL SIGILLO NON ARRIVA IN FONDO.
    # `_bloch_ritardato` calcolava `tau = d/cs` INLINE; dal blob `f7051c3` (cablaggio di
    # `--tau-luce`) la legge e' stata ESTRATTA nel metodo condiviso `_tempo_luce_nodo`, che
    # `_bloch_ritardato` ora CHIAMA (`:2490`). `FintaRete` espone i metodi uno per uno, quindi da
    # quel momento S2 muore con `AttributeError` e **S2..S8 non girano affatto**.
    # NESSUNO SE N'E' ACCORTO PER UN GIORNO, perche' nessuno ha ri-eseguito il sigillo: un sigillo
    # che non viene rigirato non protegge nulla, e questo non FALLIVA — si SCHIANTAVA.
    _tempo_luce_nodo = S.Rete._tempo_luce_nodo


def bloch(ps):
    """Bloch dei _psi_spinor, con la STESSA formula del ramo ON (n = psi^dag sigma psi)."""
    a, b = ps[:, 0], ps[:, 1]
    nb = np.stack([2.0 * np.real(np.conj(a) * b), 2.0 * np.imag(np.conj(a) * b),
                   np.abs(a) ** 2 - np.abs(b) ** 2], axis=1)
    return nb / np.maximum(np.linalg.norm(nb, axis=1), 1e-30)[:, None]


def prepara(nodi, seed, d_arco=S.LAM, cs=None):
    """Rete sintetica con spinori generici. `d_arco` e `cs` fissano tau = d/cs: sono STATO del
    sistema (lunghezze d'arco e velocita' metrica), non parametri nuovi del meccanismo."""
    g = np.random.default_rng(seed)
    r = FintaRete()
    r.n = nodi
    ii, jj = np.triu_indices(nodi, 1)
    sel = g.random(len(ii)) < 0.45
    r.i, r.j = ii[sel], jj[sel]
    r._S = None
    r.d = np.full(len(r.i), float(d_arco))
    r._cs_nodo_prev = None if cs is None else np.full(nodi, float(cs))
    ps = g.normal(size=(nodi, 2)) + 1j * g.normal(size=(nodi, 2))
    ps /= np.linalg.norm(ps, axis=1)[:, None]
    r._psi_spinor = ps
    A = g.normal(size=len(r.i))
    z = np.exp(1j * g.random(nodi) * 2 * np.pi)
    # PASSATO diverso dal presente: e' il "sistema in movimento". Bloch indipendenti, normalizzati.
    passato = g.normal(size=(nodi, 3))
    passato /= np.linalg.norm(passato, axis=1)[:, None]
    return r, A, z, passato


def coppia(r, A, z, fork, mem):
    vf, vm = S.FORK_SU2, S.FORK_SU2_MEM
    S.FORK_SU2, S.FORK_SU2_MEM = fork, mem
    try:
        return np.asarray(S.Rete._coppia_interferenza(r, A, z)).copy()
    finally:
        S.FORK_SU2, S.FORK_SU2_MEM = vf, vm


S.CAMPO_SPINORIALE = True

# ---------------------------------------------------------------- S2: tau -> 0 => Strato 0
# tau = d/cs: cs enorme (cono di luce infinitamente veloce) => tau -> 0 => alpha = 1 => il ritardato
# INSEGUE istantaneamente il corrente. Nessuna manopola: si spinge al limite una grandezza di STATO.
r, A, z, passato = prepara(60, 4242, d_arco=S.LAM, cs=1e30)
r._nb_ret = passato.copy()                 # un passato ben diverso: alpha=1 deve cancellarlo del tutto
c_s0 = coppia(r, A, z, fork=True, mem=False)
r._nb_ret = passato.copy()
c_t0 = coppia(r, A, z, fork=True, mem=True)
d_t0 = float(np.max(np.abs(c_t0 - c_s0)))
nret_t0 = np.asarray(r._nb_ret, float)
verdetto("S2 tau->0: MEM == Strato 0 (byte-identico)", d_t0 == 0.0,
         "max|MEM_tau0 - Strato0| = %.3e" % d_t0)
verdetto("S2b tau->0: il ritardato E' il corrente",
         float(np.max(np.abs(nret_t0 - bloch(r._psi_spinor)))) == 0.0,
         "max|n_ret - n_cur| = %.3e" % float(np.max(np.abs(nret_t0 - bloch(r._psi_spinor)))))

# ---------------------------------------------------------------- S3: IL DECISIVO
# tau REALISTICO: d = LAM = %.2g, cs = CS_M = %.2g  =>  tau = d/cs, alpha = 1-exp(-DT/tau).
r3, A3, z3, passato3 = prepara(60, 909, d_arco=S.LAM, cs=None)   # cs=None -> fallback CS_M
c_scal = coppia(r3, A3, z3, fork=False, mem=False)                # ramo SCALARE (abeliano)
r3._nb_ret = None
c_str0 = coppia(r3, A3, z3, fork=True, mem=False)                 # STRATO 0 (inerte per teorema)
r3._nb_ret = passato3.copy()                                      # sistema IN MOVIMENTO: passato != presente
c_mem = coppia(r3, A3, z3, fork=True, mem=True)                   # STRATO 1
tau_ = S.LAM / S.CS_M
alpha_ = 1.0 - np.exp(-S.DT / tau_)
d_inerzia = float(np.max(np.abs(c_str0 - c_scal)))
d_mem = float(np.max(np.abs(c_mem - c_scal)))
scala_ = float(np.max(np.abs(c_scal))) or 1.0
print("  contesto: d = %.3g, cs = %.3g -> tau = %.4g, alpha = %.4g (memoria di ~%.0f tic); |coppia| ~ %.3g"
      % (S.LAM, S.CS_M, tau_, alpha_, 1.0 / alpha_, scala_))
verdetto("S3.0 (controprova) Strato 0 e' INERTE, come da teorema", d_inerzia < 1e-9,
         "max|Strato0 - scalare| = %.3e" % d_inerzia)
verdetto("S3 LA FORZA CAMBIA: MEM != scalare", d_mem > 1e-6,
         "max|MEM - scalare| = %.3e  (%.2f%% di |coppia|)" % (d_mem, 100.0 * d_mem / scala_))

# ---------------------------------------------------------------- S5: azione-reazione
print()
for nome, cc in (("ramo scalare", c_scal), ("Strato 0", c_str0), ("Strato 1 (MEM)", c_mem)):
    tot = float(np.sum(cc))
    sc = float(np.max(np.abs(cc))) or 1.0
    verdetto("S5 somma coppia ~ 0 — %s" % nome, abs(tot) < 1e-9 * max(sc, 1.0) * len(cc),
             "sum = %+.3e  (max|c| = %.3e)" % (tot, sc))

# ---------------------------------------------------------------- S6: a riposo = scalare
# Sistema STATICO: gli spinori non evolvono fra una chiamata e l'altra. Il ritardato nasce uguale
# al corrente e non ha nulla da inseguire -> nessuna forza inventata dal nulla.
print()
r6, A6, z6, _ = prepara(60, 31337, d_arco=S.LAM, cs=None)
c6_scal = coppia(r6, A6, z6, fork=False, mem=False)
r6._nb_ret = None
for _ in range(200):                          # 200 tic a spinori FERMI
    c6_mem = coppia(r6, A6, z6, fork=True, mem=True)
d6 = float(np.max(np.abs(c6_mem - c6_scal)))
drift = float(np.max(np.abs(np.asarray(r6._nb_ret, float) - bloch(r6._psi_spinor))))
sc6 = float(np.max(np.abs(c6_scal))) or 1.0
verdetto("S6 a riposo: MEM == scalare (nessuna forza inventata)", d6 < 1e-9 * max(sc6, 1.0),
         "max|MEM - scalare| = %.3e dopo 200 tic  (|coppia| ~ %.3g)" % (d6, sc6))
verdetto("S6b a riposo: il ritardato resta sul corrente", drift < 1e-12,
         "max|n_ret - n_cur| = %.3e" % drift)
nor6 = np.linalg.norm(np.asarray(r6._nb_ret, float), axis=1)
verdetto("S6c |n_ret| = 1 dopo 200 tic", float(np.max(np.abs(nor6 - 1.0))) < 1e-12,
         "max| |n_ret| - 1 | = %.3e" % float(np.max(np.abs(nor6 - 1.0))))

# ============================================================ S7: il tic e' il TEMPO PROPRIO
# NESSUN ALTRO SIGILLO CATTURA QUESTO. S1..S6 provano la STRUTTURA del ritardo (che ci sia, che si
# riduca al limite, che resti unitario): passerebbero IDENTICI anche con alpha = 1-exp(-DT/tau),
# cioe' col tic di COORDINATA globale al posto del tempo proprio del nodo. Ma tau = d/cs e' tempo
# PROPRIO: rilassarlo con DT cancella la dipendenza dall'orologio locale, cioe' impone a un
# processo locale la foliazione sincrona globale (un frame preferito, un "etere"). Qui si misura
# esattamente quella dipendenza.
print()
print("=" * 96)
print("SIGILLO 7 — il rilassamento vive nel TEMPO PROPRIO dt_n = DT*r, non nel tic globale DT")
print("=" * 96)
NODI7 = 4
RITMI = np.array([0.5, 1.0, 2.0, 4.0])       # orologi locali diversi, TUTTO il resto identico
r7 = FintaRete()
r7.n = NODI7
_i7, _j7 = np.triu_indices(NODI7, 1)
r7.i, r7.j = _i7, _j7
r7._S = None
r7.d = np.full(len(r7.i), float(S.LAM))       # stessa lunghezza d'arco -> STESSO tau per tutti
r7._cs_nodo_prev = None                       # -> cs = CS_M per tutti
# stato IDENTICO su tutti i nodi: presente = +z, passato = +x  (Omega = pi/2, ben dentro lo slerp)
r7._psi_spinor = np.tile(np.array([1.0 + 0j, 0.0 + 0j]), (NODI7, 1))
passato7 = np.tile(np.array([1.0, 0.0, 0.0]), (NODI7, 1))
tau7 = S.LAM / S.CS_M
att = 1.0 - np.exp(-S.DT * RITMI / tau7)      # alpha ATTESO per nodo, in tempo proprio
bug = 1.0 - np.exp(-S.DT / tau7)              # alpha che si avrebbe col BUG (DT nudo): uguale per tutti

r7._nb_ret = passato7.copy()
r7._r_corrente = RITMI.copy()
out7 = np.asarray(S.Rete._bloch_ritardato(r7, bloch(r7._psi_spinor), r7.i, r7.j), float)
# lo slerp avanza di alpha*Omega lungo la geodetica: l'angolo percorso DAL PASSATO misura alpha
Om7 = np.pi / 2.0
mis = np.arccos(np.clip(np.sum(out7 * passato7, axis=1), -1.0, 1.0)) / Om7
print("  tau = %.4g,  DT = %.4g,  Omega = pi/2" % (tau7, S.DT))
print("   r      alpha atteso (dt_n)   alpha misurato        alpha col BUG (DT)")
for k in range(NODI7):
    print("  %4.1f   %18.12f   %18.12f   %18.12f" % (RITMI[k], att[k], mis[k], bug))
err7 = float(np.max(np.abs(mis - att)))
verdetto("S7 alpha = 1-exp(-DT*r/tau) per nodo", err7 < 1e-9,
         "max|alpha_mis - alpha_atteso| = %.3e" % err7)
rap_mis = float(mis[2] / mis[1])                      # r=2 contro r=1
rap_att = float(att[2] / att[1])
verdetto("S7b il rapporto r=2 / r=1 e' quello del tempo proprio",
         abs(rap_mis - rap_att) < 1e-9,
         "misurato %.9f, atteso %.9f  (col BUG sarebbe esattamente 1.000000000)"
         % (rap_mis, rap_att))
verdetto("S7c il ritmo locale CONTA (il bug darebbe tutti uguali)",
         abs(rap_mis - 1.0) > 1e-3,
         "|rapporto - 1| = %.3e" % abs(rap_mis - 1.0))
# orologio globale (TAU_LOC = 0 -> ritmo() = None): dt_n deve tornare DT
r7._nb_ret = passato7.copy()
r7._r_corrente = None
out7g = np.asarray(S.Rete._bloch_ritardato(r7, bloch(r7._psi_spinor), r7.i, r7.j), float)
mis_g = np.arccos(np.clip(np.sum(out7g * passato7, axis=1), -1.0, 1.0)) / Om7
verdetto("S7d orologio globale (r = None) -> alpha = 1-exp(-DT/tau)",
         float(np.max(np.abs(mis_g - bug))) < 1e-9,
         "max|alpha_mis - %.12f| = %.3e" % (bug, float(np.max(np.abs(mis_g - bug)))))

# ============================================================ S8: `tau` SEGUE `cs` — MAI TESTATO
# IL MARCHIO CHE QUESTO SIGILLO ESISTE PER TOGLIERE (CLAUDE.md par.9, 2026-09-15):
#   «il sigillo 23/23 dello STRATO 1 NON HA MAI ESERCITATO LA DIPENDENZA DA `cs`».
# E non e' stato un caso: l'argv di S1 non conteneva `--cs-dinamico` (quindi `cs = CS_M` costante
# e `_cs_nodo_prev` non veniva nemmeno scritta), e in tutti i test in-process `_cs_nodo_prev` e'
# `None` oppure `np.full(nodi, cs)` — cioe' **COSTANTE**. Un `cs` costante non esercita `tau = d/cs`:
# lo rende indistinguibile da `tau ∝ d`. S7 misura la dipendenza da `r`, non quella da `cs`.
# QUI si da' a ogni nodo un `cs` DIVERSO, a parita' di tutto il resto, e si verifica che `alpha`
# lo segua nodo per nodo. E' l'unico sigillo del lotto che fallirebbe se `cs` fosse ignorato.
print()
print("=" * 96)
print("SIGILLO 8 — `tau = d/cs` SEGUE `cs` PER NODO (la dipendenza mai esercitata)")
print("=" * 96)
NODI8 = 4
CS_NODO = np.array([1.0, 2.0, 4.0, 8.0])     # velocita' metriche locali diverse, resto IDENTICO
r8 = FintaRete()
r8.n = NODI8
_i8, _j8 = np.triu_indices(NODI8, 1)
r8.i, r8.j = _i8, _j8
r8._S = None
r8.d = np.full(len(r8.i), float(S.LAM))       # stessa lunghezza d'arco: l'UNICA differenza e' cs
r8._cs_nodo_prev = CS_NODO.copy()
r8._psi_spinor = np.tile(np.array([1.0 + 0j, 0.0 + 0j]), (NODI8, 1))
passato8 = np.tile(np.array([1.0, 0.0, 0.0]), (NODI8, 1))
tau8 = S.LAM / CS_NODO                        # tau PER NODO
att8 = 1.0 - np.exp(-S.DT / tau8)             # alpha atteso per nodo (r = 1 per tutti)
bug8 = 1.0 - np.exp(-S.DT / (S.LAM / S.CS_M))  # alpha se `cs` fosse IGNORATO: uguale per tutti

r8._nb_ret = passato8.copy()
r8._r_corrente = np.ones(NODI8)               # ritmo IDENTICO: isola `cs` da `r` (S7 fa l'opposto)
out8 = np.asarray(S.Rete._bloch_ritardato(r8, bloch(r8._psi_spinor), r8.i, r8.j), float)
Om8 = np.pi / 2.0
mis8 = np.arccos(np.clip(np.sum(out8 * passato8, axis=1), -1.0, 1.0)) / Om8
print("  d = LAM = %.4g,  DT = %.4g,  r = 1 su TUTTI i nodi,  Omega = pi/2" % (S.LAM, S.DT))
print("   cs      tau = d/cs    alpha atteso        alpha misurato      alpha se cs IGNORATO")
for k in range(NODI8):
    print("  %4.1f   %10.6f   %18.12f   %18.12f   %18.12f"
          % (CS_NODO[k], tau8[k], att8[k], mis8[k], bug8))
err8 = float(np.max(np.abs(mis8 - att8)))
verdetto("S8 alpha = 1-exp(-dt_n*cs/d) PER NODO", err8 < 1e-9,
         "max|alpha_mis - alpha_atteso| = %.3e" % err8)
rap8_mis = float(mis8[3] / mis8[0])            # cs=8 contro cs=1
rap8_att = float(att8[3] / att8[0])
verdetto("S8b il rapporto cs=8 / cs=1 e' quello di d/cs",
         abs(rap8_mis - rap8_att) < 1e-9,
         "misurato %.9f, atteso %.9f  (se cs fosse ignorato sarebbe esattamente 1.000000000)"
         % (rap8_mis, rap8_att))
verdetto("S8c il `cs` LOCALE conta (con cs ignorato sarebbero tutti uguali)",
         abs(rap8_mis - 1.0) > 1e-3,
         "|rapporto - 1| = %.3e" % abs(rap8_mis - 1.0))
# CONTROPROVA: con `cs` COSTANTE si deve tornare ESATTAMENTE al valore del "bug". Serve a
# dimostrare che S8 non passa per un artefatto dello slerp: e' proprio `cs` a muoverlo.
r8._nb_ret = passato8.copy()
r8._cs_nodo_prev = np.full(NODI8, float(S.CS_M))
out8c = np.asarray(S.Rete._bloch_ritardato(r8, bloch(r8._psi_spinor), r8.i, r8.j), float)
mis8c = np.arccos(np.clip(np.sum(out8c * passato8, axis=1), -1.0, 1.0)) / Om8
verdetto("S8d controprova: cs COSTANTE = CS_M -> alpha uguale per tutti",
         float(np.max(np.abs(mis8c - bug8))) < 1e-9,
         "max|alpha_mis - %.12f| = %.3e" % (bug8, float(np.max(np.abs(mis8c - bug8)))))

# ============================================================ S3b: IL DECISIVO, NEL CICLO VERO
# S3 misura la forza su stati SINTETICI. Qui la stessa domanda viene posta alla DINAMICA REALE:
# si gira un batch vero con la memoria accesa e, a ogni passo, si calcolano ENTRAMBI i rami sullo
# STESSO stato (prima lo Strato 0, che non tocca _nb_ret; poi il ramo vero, che lo aggiorna).
# Serve perche' S3 potrebbe passare su stati inventati e restare inerte sugli stati che il sistema
# visita davvero (se i Bloch non si muovono entro tau, n_ret ~ n_cur e l'inerzia ritorna).
print()
print("=" * 96)
print("SIGILLO 3b — LA FORZA CAMBIA ANCHE NEL CICLO DINAMICO REALE (batch vero, 30 passi)")
print("=" * 96)
_argv = list(sys.argv)
sys.argv = ["soliton_simulator.py",
            "--batch", "--nmasse", "3", "--sep", "8", "--seed", "1", "--passi", "30",
            "--ogni", "30", "--db-ogni", "30",
            "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto", "--chi-core",
            "--calore-scal", "--deparam-orologio", "--verlet", "--cs-dinamico",
            "--fork-su2", "--fork-su2-mem",
            "--csv", os.path.join(HERE, "_s3b.csv"),
            "--sync-db", os.path.join(HERE, "_s3b.pkl"), "--db-cleanup"]
_a = S._cli()
S._applica_regime(_a)
_orig_ci = S.Rete._coppia_interferenza
_orig_br = S.Rete._bloch_ritardato
_reg = []
_stacco = []
_reset = {"n": 0, "tot": 0}


def _da_applica_flag(salti):
    """_applica_flag gira 300 step di riscaldamento su un'ALTRA rete (quella interattiva globale):
    va ESCLUSA, altrimenti le misure mescolano due sistemi diversi."""
    f = sys._getframe(salti)
    for _ in range(7):
        if f is None:
            return False
        if f.f_code.co_name == "_applica_flag":
            return True
        f = f.f_back
    return False


def _spia_br(self, nb_cur, ii, jj):
    mio = not _da_applica_flag(2)
    if mio:
        prev = getattr(self, "_nb_ret", None)
        _reset["tot"] += 1
        _reset["n"] += int(prev is None or len(prev) != self.n)
    out = _orig_br(self, nb_cur, ii, jj)
    if mio:
        _stacco.append(float(np.max(np.abs(np.asarray(out, float)
                                           - np.asarray(nb_cur, float)[:self.n]))))
    return out


def _spia_ci(self, A_, z_):
    if _da_applica_flag(1):
        return _orig_ci(self, A_, z_)
    vm = S.FORK_SU2_MEM
    S.FORK_SU2_MEM = False
    c0 = np.asarray(_orig_ci(self, A_, z_)).copy()      # Strato 0: non tocca _nb_ret (pure-read)
    S.FORK_SU2_MEM = vm
    c1 = np.asarray(_orig_ci(self, A_, z_)).copy()      # ramo VERO (MEM): aggiorna _nb_ret
    sc = float(np.max(np.abs(c0)))
    _reg.append((self.n, float(np.max(np.abs(c1 - c0))), sc))
    return c1


S.Rete._bloch_ritardato = _spia_br
S.Rete._coppia_interferenza = _spia_ci
try:
    import contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        S.batch_condensazione(_a)
finally:
    S.Rete._bloch_ritardato = _orig_br
    S.Rete._coppia_interferenza = _orig_ci
    sys.argv = _argv

_st = np.array(_stacco) if _stacco else np.array([np.nan])
_rap = np.array([d_ / sc_ for (_n, d_, sc_) in _reg if sc_ > 0.0]) if _reg else np.array([np.nan])
_ult = _rap[-10:] if len(_rap) >= 10 else _rap
print("  passi misurati: %d   reset della memoria (len != n): %d su %d chiamate"
      % (len(_reg), _reset["n"], _reset["tot"]))
print("  max|n_ret - n_cur| (stacco passato/presente): mediana %.3e  max %.3e"
      % (float(np.median(_st)), float(np.max(_st))))
print("  |MEM - Strato0| / |coppia| : mediana %.3e   negli ultimi 10 passi %.3e   max %.3e"
      % (float(np.median(_rap)), float(np.median(_ult)), float(np.max(_rap))))
verdetto("S3b la forza cambia nel ciclo reale", float(np.max(_rap)) > 1e-6,
         "max |MEM - Strato0|/|coppia| = %.3e su %d passi" % (float(np.max(_rap)), len(_reg)))
verdetto("S3b2 la memoria NON viene resettata a ogni passo", _reset["n"] < 0.5 * _reset["tot"],
         "reset %d su %d chiamate (la mitosi deve EREDITARE _nb_ret, non azzerarlo)"
         % (_reset["n"], _reset["tot"]))

print("=" * 96)
tot_, ok_ = len(esiti), sum(esiti)
print("SIGILLO STRATO 1: %d/%d PASS -> %s" % (ok_, tot_, "PASS" if ok_ == tot_ else "FAIL"))
print("""
COSA QUESTO SIGILLO NON DICE (par.8)
------------------------------------
S3 dice che la forza CAMBIA, non che sia FISICA. Il teorema di inerzia si rompe per COSTRUZIONE
(era prevedibile); che la dinamica che ne esce sia sensata - olonomia W(r) non banale, stabilita'
su orizzonti lunghi, verso corretto per la gravita' - lo dice un RUN, non l'algebra, e non sotto
~2000 passi ne' su un solo seme (par.2.7).
Inoltre: l'effetto e' proporzionale a quanto i Bloch cambiano ENTRO tau. Dove il sistema e'
quasi-statico, n_ret ~ n_cur e l'inerzia quasi ritorna: la forza-memoria morde solo dove la
configurazione evolve entro il tempo-luce. E finche' cs non e' vivo (I~0.05 contro soglia ~400),
tau ~ d/CS_M: il ritardo c'e', ma la sua VARIAZIONE spaziale - la curvatura - e' debole.
Il flag resta OFF di default.
""")
sys.exit(0 if ok_ == tot_ else 1)
