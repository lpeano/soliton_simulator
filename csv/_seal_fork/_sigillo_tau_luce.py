# -*- coding: utf-8 -*-
"""SIGILLO di `--tau-luce` (FASE 2) -- T0..T5. **RIPARATO il 2026-09-18.**

Il FALLIMENTO precedente e' committato COM'ERA in `_sigillo_tau_luce_RIGIRO_2026-09-18.txt` (38bd0a7)
e la diagnosi sta in `doc/TASK_HISTORY/2026-09-18_sigillo-tau-luce.md`.
**SI E' RIPARATO IL SIGILLO. LA LEGGE `--tau-luce` NON E' STATA TOCCATA** -- `T0` lo DIMOSTRA.

COSA ERA ROTTO, e perche' la riparazione ha questa forma:

T1  confrontava il DISCO DI OGGI contro il blob `f5887254` di TRE GIORNI FA. Ma fra i due ci sono
    SETTE correzioni di legge sigillate: T1 asseriva "il flag OFF e' byte-identico al comportamento
    PRIMA della modifica" ed ESEGUIVA "oggi e' uguale a tre giorni fa", che e' FALSO PER COSTRUZIONE.
    -> `T1a` si ancora alla COPPIA DI BLOB CHE RACCHIUDE IL CAMBIAMENTO (`f5887254` -> `7d484580`),
       entrambi PINNATI ed estratti con `git cat-file -p` IN BINARIO (mai `git checkout`: C18).
       E' la lezione di `c818208` rovesciata: li' era il lato NUOVO ad andare alla deriva.
    -> `T1b` e' la verifica di OGGI, e PUO' FALLIRE sul blob corrente: a flag SPENTO il ramo
       tau-luce non dev'essere preso NEMMENO UNA VOLTA. Si CONTA (P5/A8).

T2  sostituiva `Rete._tempo_luce_nodo`, che e' CONDIVISO. Il documento del fallimento diceva "lo
    chiama anche `_bloch_ritardato`": **VERIFICATO DAL DISCO, I CHIAMANTI SONO TRE, NON DUE** --
      :2337  `_passo_spinoriale`  L'INERZIA (`_T2 = T^2`), NON gated su TAU_LUCE
      :2442  `_passo_spinoriale`  il rilassamento tau-luce, DENTRO `if TAU_LUCE:`
      :3027  `_bloch_ritardato`   lo STRATO 1
    e i primi due stanno NELLA STESSA FUNZIONE, quindi `co_name` NON basta a distinguerli.
    -> il wrapper discrimina per RIGA DEL CHIAMANTE, ma la riga **NON E' PINNATA**: si TROVA a
       runtime **CERCANDO IL FLAG** (`if TAU_LUCE:` + la chiamata dentro quel blocco), che e'
       esattamente cio' che CLAUDE.md par.0 impone (*cerca per NOME di funzione/flag, non per riga*).
       **Se i siti trovati non sono ESATTAMENTE UNO, il sigillo RIFIUTA DI GIRARE: non degrada.**
    -> e i TRE contatori si stampano: se quello del sito tau-luce fosse ZERO, il discriminatore non
       sta funzionando e **T2 FALLISCE**, invece di passare in silenzio.

T3  chiedeva che la pendenza si ALLONTANASSE da zero di almeno `0.3`. Soglia e DIREZIONE venivano da
    un'attesa (`-1.03`) calcolata quando `cs` era MORTO (`cs_std/cs = 0.0079 %`). Oggi `cs` e' VIVO
    (`17.6 %`), e la baseline OFF ha dato `-0.17`, poi `-1.73`, poi `+0.34` su tre blob.
    -> il criterio nuovo NON prescrive una direzione e NON sceglie una soglia: chiede che l'effetto
       superi il NULLO **MISURATO DENTRO IL SIGILLO** come dispersione FRA SEMI (par.9 `C10`: la `SE`
       interna e' ~3 volte troppo piccola; `P3`: servono >= 4 semi). **Quattro semi APPAIATI.**
    -> **il rovesciamento del segno NON viene ne' spiegato ne' incorporato: si RIPORTA** (`T3-bis`),
       perche' riscrivere il criterio finche' T3 passa sarebbe aggiustare il criterio, non ripararlo.

T4, T5 NON sono stati toccati: passavano e passano.
ASCII PURO.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import _presidio
_presidio.avvia(__file__)

import contextlib
import hashlib
import importlib.util
import io as _io
import re
import subprocess
import time

import numpy as np

RAD = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(RAD)
sys.path.insert(0, RAD)

# I DUE BLOB CHE RACCHIUDONO IL CAMBIAMENTO. PINNATI, e non si muovono col lavoro.
BLOB_PRE = "f5887254"    # PRIMA del cablaggio di --tau-luce (non contiene TAU_LUCE)
BLOB_POST = "7d484580"   # SUBITO DOPO (contiene TAU_LUCE, flag OFF di default)
SEMI_T3 = (1, 2, 3, 4)   # P3: per una barra FRA SEMI servono >= 4. Con 2, t(0.025,1) = 12.706.
T_3GDL = 3.182           # t(0.025, 3) -- tabellato, non scelto
SEED, PASSI = 1, 25
PASSI_T3 = 300

ARGS = ["--batch", "--nmasse", "3", "--sep", "8", "--passi", "1", "--ogni", "100000",
        "--db-ogni", "100000", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
        "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--cs-dinamico",
        "--fork-su2", "--fork-su2-mem", "--csv", os.path.join(os.environ.get("TMP", "."), "_sig.csv")]
CAMPI = ("pos", "phi", "phi0", "phivel", "eta", "d", "d0", "vd", "peq", "tw", "twp", "i", "j",
         "perc_chi", "perc_tw", "_nb", "_nb_prec", "_nb_ret", "_psi_spinor", "omega_s", "psi")
ESITI = {}
CRONO = {}


def blob_git(path):
    b = open(path, "rb").read()
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest(), hashlib.sha1(b).hexdigest()


def estrai(sha, dest):
    """git cat-file -p IN BINARIO. RIFIUTA se non estraibile: NON degrada in un confronto col vuoto
    (e' il difetto `pre_src = "" if not os.path.exists(PRE)` che il mandato nomina)."""
    try:
        dati = subprocess.check_output(["git", "cat-file", "-p", sha])
    except subprocess.CalledProcessError:
        raise SystemExit("[SIGILLO] RIFIUTO DI GIRARE: il blob %s non e' estraibile dal repo.\n"
                         "          Un riferimento mancante NON si sostituisce col vuoto." % sha)
    with open(dest, "wb") as fh:
        fh.write(dati)
    ric = hashlib.sha1(b"blob %d\0" % len(dati) + dati).hexdigest()
    if not ric.startswith(sha):
        raise SystemExit("[SIGILLO] RIFIUTO: blob estratto %s != atteso %s" % (ric[:8], sha))
    return dest


def trova_sito_tau_luce(sorgente):
    """LA RIGA NON E' PINNATA: si TROVA cercando IL FLAG (par.0). Deve essere ESATTAMENTE UNA."""
    src = _io.open(sorgente, encoding="utf-8").read().split("\n")
    trovati = []
    for k, l in enumerate(src):
        if not re.match(r"^\s+if TAU_LUCE:\s*$", l):
            continue                       # solo il blocco INDENTATO (dentro un metodo), non il CLI
        base = len(l) - len(l.lstrip())
        for j in range(k + 1, min(k + 15, len(src))):
            lj = src[j]
            if lj.strip() and (len(lj) - len(lj.lstrip())) <= base:
                break
            nudo = lj.split("#", 1)[0]
            if "self._tempo_luce_nodo(" in nudo:
                trovati.append((j + 1, lj.strip()))
    if len(trovati) != 1:
        raise SystemExit("[SIGILLO] RIFIUTO DI GIRARE: siti `if TAU_LUCE:` -> `_tempo_luce_nodo` "
                         "trovati = %d, atteso 1.\n          %s\n"
                         "          Un discriminatore ambiguo NON si usa: si RIFIUTA."
                         % (len(trovati), trovati))
    return trovati[0]


def carica(percorso, nome, extra=()):
    spec = importlib.util.spec_from_file_location(nome, percorso)
    M = importlib.util.module_from_spec(spec)
    sys.modules[nome] = M
    sys.argv = ["soliton_simulator.py"] + ARGS + list(extra)
    with contextlib.redirect_stdout(_io.StringIO()):
        spec.loader.exec_module(M)
        a = M._cli(); M._applica_regime(a); M._applica_flag(a)
    return M


def conta_siti(M, registro):
    """Wrapper PURE-READ: conta le chiamate a `_tempo_luce_nodo` PER RIGA DEL CHIAMANTE.
    Non muta stato ne' RNG -- chiama attraverso e basta (par.2.3)."""
    orig = M.Rete._tempo_luce_nodo

    def w(self, ii, jj, __o=orig, __r=registro):
        __r[sys._getframe(1).f_lineno] = __r.get(sys._getframe(1).f_lineno, 0) + 1
        return __o(self, ii, jj)
    M.Rete._tempo_luce_nodo = w
    return orig


def scena(M, seed):
    net = M.Rete(seed); net.semina(80)
    for _ in range(6):
        passo(M, net)
    Nc = M.massa_critica_collasso()
    for k in range(3):
        ang = 2 * np.pi * k / 3
        net.nuova_massa(int(Nc * 0.6), raggio=0.8,
                        centro=(8.0 * np.cos(ang), 8.0 * np.sin(ang), 0.0), fase=0.0)
    return net


def passo(M, net):
    M.scuoti_vuoto(net); net.step(); net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()


def evolvi(M, seed, n):
    net = scena(M, seed)
    for _ in range(n):
        passo(M, net)
    return net


def confronta(a, b, eti):
    print("  PRESIDIO: uno zero con N DIVERSO e' MANCANZA DI CONFRONTO, non identita'.")
    print("    n_A = %d   n_B = %d   ->  %s"
          % (a.n, b.n, "CONFRONTABILI" if a.n == b.n else "NON CONFRONTABILI"))
    if a.n != b.n:
        print("  %s: FAIL" % eti)
        return False
    ok = True
    peggio = 0.0
    for c in CAMPI:
        va, vb = getattr(a, c, None), getattr(b, c, None)
        if va is None or vb is None:
            continue
        va, vb = np.asarray(va), np.asarray(vb)
        if va.shape != vb.shape:
            print("    %-14s SHAPE diversa -> FAIL" % c); ok = False; continue
        d = float(np.max(np.abs(va.astype(complex) - vb.astype(complex)))) if va.size else 0.0
        peggio = max(peggio, d)
        if d != 0.0:
            ok = False
            print("    %-14s max|A-B| = %.3e  FAIL" % (c, d))
    rng = (a.rng.bit_generator.state == b.rng.bit_generator.state)
    print("    %d campi confrontati, PEGGIOR max|A-B| = %.3e   stato RNG %s"
          % (len(CAMPI), peggio, "identico" if rng else "DIVERSO"))
    ok = ok and rng
    print("  %s: %s" % (eti, "PASS" if ok else "FAIL"))
    return ok


def pend_se(x, y):
    ok = np.isfinite(x) & np.isfinite(y) & (x > 0) & (y > 0)
    lx, ly = np.log(x[ok]), np.log(y[ok])
    b = float(np.polyfit(lx, ly, 1)[0])
    r = float(np.corrcoef(lx, ly)[0, 1])
    n = int(ok.sum())
    se = abs(b / r) * np.sqrt((1 - r * r) / (n - 2))
    return b, se, r * r, n


def pendenza(M, seed, passi):
    net = evolvi(M, seed, passi)
    n = net.n
    rs = getattr(net, "rho_spin", None)
    rho = np.asarray(rs)[:n] if (rs is not None and len(rs) >= n) else np.abs(np.asarray(net.psi[:n])) ** 2
    inz = np.maximum(rho, 1e-6)
    om = np.linalg.norm(np.asarray(net.omega_s[:n], float), axis=1)
    th = np.degrees(om * M.DT)
    v = rho > 1.0000001e-6
    b, se, r2, nn = pend_se(inz[v], th[v])
    return b, se, r2, nn, float(np.median(om)), float(np.median(th)), n


def titolo(t):
    print()
    print("=" * 110)
    print(t)
    print("=" * 110)


# ==================================================================== T0
titolo("T0 - IL BLOB DELLA FISICA. Il sigillo NON deve toccarlo: si misura PRIMA e DOPO.")
BG0, BR0 = blob_git(os.path.join(RAD, "soliton_simulator.py"))
print("  soliton_simulator.py   git-blob %s   byte grezzi %s" % (BG0[:8], BR0[:8]))
SITO, TESTO = trova_sito_tau_luce(os.path.join(RAD, "soliton_simulator.py"))
print("  sito del ramo tau-luce TROVATO CERCANDO IL FLAG (non pinnato): riga %d" % SITO)
print("    %s" % TESTO)

# ==================================================================== T1a
titolo("T1a - BYTE-IDENTITA' fra i DUE BLOB CHE RACCHIUDONO IL CAMBIAMENTO (flag OFF). BLOCCANTE.")
print("  %s (PRE, senza TAU_LUCE)  contro  %s (POST, TAU_LUCE presente ma OFF)" % (BLOB_PRE, BLOB_POST))
print("  estratti con `git cat-file -p` IN BINARIO -- mai `git checkout` (trappola CRLF, C18)")
t0 = time.perf_counter()
p_pre = estrai(BLOB_PRE, os.path.join(QUI, "_tl_pre.py"))
p_post = estrai(BLOB_POST, os.path.join(QUI, "_tl_post.py"))
M_pre = carica(p_pre, "tl_pre")
M_post = carica(p_post, "tl_post")
print("  TAU_LUCE nel POST (deve essere False): %s" % getattr(M_post, "TAU_LUCE", "ASSENTE"))
ESITI["T1a"] = confronta(evolvi(M_pre, SEED, PASSI), evolvi(M_post, SEED, PASSI), "T1a")
CRONO["T1a"] = time.perf_counter() - t0
if not ESITI["T1a"]:
    print("  >>> T1a e' BLOCCANTE: se cade, il cablaggio CAMBIO' il ramo OFF, ed e' una questione")
    print("      di LEGGE, non di sigillo. Si riporta e ci si ferma.")

# ==================================================================== T1b
titolo("T1b - SUL BLOB CORRENTE: a flag SPENTO il ramo tau-luce non dev'essere preso MAI (P5/A8).")
t0 = time.perf_counter()
reg_off = {}
M_off = carica("soliton_simulator.py", "sim_off")
conta_siti(M_off, reg_off)
print("  TAU_LUCE nel modulo (deve essere False): %s" % M_off.TAU_LUCE)
net_off = evolvi(M_off, SEED, PASSI)
print("  chiamate a `_tempo_luce_nodo`, PER RIGA DEL CHIAMANTE:")
for r in sorted(reg_off):
    print("    riga %-6d %8d chiamate%s" % (r, reg_off[r], "   <- IL SITO TAU-LUCE" if r == SITO else ""))
tot_altri = sum(v for k, v in reg_off.items() if k != SITO)
ESITI["T1b"] = (reg_off.get(SITO, 0) == 0) and (tot_altri > 0)
print("  sito tau-luce: %d chiamate (deve essere 0)   altri siti: %d (devono essere > 0, senno' il"
      % (reg_off.get(SITO, 0), tot_altri))
print("  contatore non sta funzionando e il PASS sarebbe VUOTO)")
print("  T1b: %s" % ("PASS" if ESITI["T1b"] else "FAIL"))
CRONO["T1b"] = time.perf_counter() - t0

# ==================================================================== T2
titolo("T2 - RIDUZIONE AL LIMITE, col monkeypatch che DISCRIMINA IL CHIAMANTE.")
t0 = time.perf_counter()
M_lim = carica("soliton_simulator.py", "sim_lim", ["--tau-luce"])
print("  TAU_LUCE (deve essere True): %s" % M_lim.TAU_LUCE)
_orig_lim = M_lim.Rete._tempo_luce_nodo
reg_lim = {"tau_luce": 0, "altri": 0}


def tau_discriminante(self, ii, jj, __o=_orig_lim, __M=M_lim, __r=reg_lim, __s=SITO):
    """Restituisce il tau VECCHIO **solo** al sito tau-luce. Inerzia e Strato 1 ricevono la legge
    VERA -- senza questo, il test cambierebbe TRE meccanismi invece di UNO (par.1)."""
    if sys._getframe(1).f_lineno != __s:
        __r["altri"] += 1
        return __o(self, ii, jj)
    __r["tau_luce"] += 1
    n = self.n
    dens = np.abs(self.psi[:n]) ** 2
    rif = max(float(np.median(dens[dens > 1e-6])), 1e-6) if np.any(dens > 1e-6) else 1.0
    return __M.TAU_A * np.maximum(dens / rif, 0.05)


M_lim.Rete._tempo_luce_nodo = tau_discriminante
print("  il tau VECCHIO e' iniettato SOLO alla riga %d; inerzia (:2337) e Strato 1 (:3027)" % SITO)
print("  ricevono la legge VERA. TAU_A_LOCALE = %s (il ramo OFF che si deve ritrovare)." % M_lim.TAU_A_LOCALE)
net_a = evolvi(M_off, SEED, PASSI)
net_b = evolvi(M_lim, SEED, PASSI)
print("  contatori del discriminatore: sito tau-luce %d   altri siti %d"
      % (reg_lim["tau_luce"], reg_lim["altri"]))
ok2 = confronta(net_a, net_b, "T2 (confronto)")
if reg_lim["tau_luce"] == 0:
    print("  >>> il contatore del sito tau-luce e' ZERO: il discriminatore NON sta funzionando,")
    print("      e un PASS qui sarebbe VUOTO. T2 FALLISCE.")
ESITI["T2"] = ok2 and reg_lim["tau_luce"] > 0 and reg_lim["altri"] > 0
print("  T2: %s" % ("PASS" if ESITI["T2"] else "FAIL"))
CRONO["T2"] = time.perf_counter() - t0

# ==================================================================== T3
titolo("T3 - IL FLAG PRODUCE UN EFFETTO PIU' GRANDE DEL NULLO **MISURATO**? (4 semi APPAIATI)")
print("  Il criterio vecchio chiedeva uno spostamento di 0.3 in una DIREZIONE prescritta. Soglia e")
print("  direzione venivano da un'attesa (-1.03) calcolata con `cs` MORTO. NON si usano piu'.")
print("  Il nullo si MISURA QUI come dispersione FRA SEMI (par.9 C10; P3: >= 4 semi).")
t0 = time.perf_counter()
M_on = carica("soliton_simulator.py", "sim_on", ["--tau-luce"])
R_off, R_on = {}, {}
print("  %-6s | %-24s | %-24s | %-10s" % ("seme", "OFF pendenza +- SE (r2, n)", "ON  pendenza +- SE (r2, n)", "DIFF ON-OFF"))
for s in SEMI_T3:
    bo, seo, r2o, no, omo, tho, nno = pendenza(M_off, s, PASSI_T3)
    bn, sen, r2n, nn_, omn, thn, nnn = pendenza(M_on, s, PASSI_T3)
    R_off[s] = (bo, seo, r2o, no, omo, tho, nno)
    R_on[s] = (bn, sen, r2n, nn_, omn, thn, nnn)
    print("  %-6d | %+8.4f +- %.4f (%.3f, %4d) | %+8.4f +- %.4f (%.3f, %4d) | %+10.4f"
          % (s, bo, seo, r2o, no, bn, sen, r2n, nn_, bn - bo))
dif = np.array([R_on[s][0] - R_off[s][0] for s in SEMI_T3], float)
off = np.array([R_off[s][0] for s in SEMI_T3], float)
md = float(np.mean(dif))
sd = float(np.std(dif, ddof=1))
se_d = sd / np.sqrt(len(dif))
ic = T_3GDL * se_d
print()
print("  IL NULLO MISURATO -- dispersione FRA SEMI delle pendenze OFF (codice INVARIATO):")
print("    std(OFF) = %.4f   (per confronto: la SE INTERNA tipica vale %.4f -- par.9 dice che e'"
      % (float(np.std(off, ddof=1)), float(np.mean([R_off[s][1] for s in SEMI_T3]))))
print("     ~3 volte troppo piccola, e qui si vede)")
print("  L'EFFETTO APPAIATO:")
print("    media(ON-OFF) = %+.4f   std = %.4f   SE = %.4f   IC95 = [%+.4f, %+.4f]  (t(3) = %.3f)"
      % (md, sd, se_d, md - ic, md + ic, T_3GDL))
ESITI["T3"] = bool(abs(md) > ic)
print("  T3 (l'IC95 dell'effetto appaiato ESCLUDE lo zero): %s" % ("PASS" if ESITI["T3"] else "FAIL"))
if ESITI["T3"] and abs(md) < 2.0 * ic:
    print("  >>> ATTENZIONE: passa con un margine SOTTILE (|media| < 2*IC). Si dice, non si conta")
    print("      come PASS pieno.")
CRONO["T3"] = time.perf_counter() - t0

titolo("T3-bis - IL ROVESCIAMENTO DEL SEGNO: si RIPORTA, non si giudica e non si spiega.")
print("  Storia della pendenza ON-OFF su tre blob (dal repo, non da questa corsa):")
print("    2026-09-15  blob 7d484580   OFF -0.1685   ON -0.4265   ON piu' LONTANO da zero (-0.258)")
print("    2026-09-17  blob 08784685+  OFF -1.7311   ON -1.2749   ON piu' VICINO  da zero (+0.456)")
print("    2026-09-18  blob b9e07c73   OFF +0.3370   ON +0.5218   segno POSITIVO, r2 = 0.031")
print("  QUESTA CORSA, seme %d:          OFF %+.4f   ON %+.4f" % (SEMI_T3[0], R_off[SEMI_T3[0]][0], R_on[SEMI_T3[0]][0]))
print("  NON HO UNA MISURA CHE LO SPIEGHI, E NON LA INVENTO. Non e' un criterio: e' un riscontro.")

# ==================================================================== T4
titolo("T4 - SIGILLO DI COVARIANZA: e' una LEGGE o un numero travestito? (NON TOCCATO)")
t0 = time.perf_counter()
net = evolvi(M_on, SEED, 60)
ii, jj = net.i, net.j
t_0 = M_on.Rete._tempo_luce_nodo(net, ii, jj).copy()
d0 = net.d.copy()
net.d = d0 * 2.0
t_d = M_on.Rete._tempo_luce_nodo(net, ii, jj).copy()
net.d = d0
csp = getattr(net, "_cs_nodo_prev", None)
t_c = None
if csp is not None:
    c0 = np.asarray(csp, float).copy()
    net._cs_nodo_prev = c0 * 2.0
    t_c = M_on.Rete._tempo_luce_nodo(net, ii, jj).copy()
    net._cs_nodo_prev = c0
r_d = float(np.median(t_d / np.maximum(t_0, 1e-300)))
print("  d -> 2d   : tau_nuovo/tau_vecchio = %.6f   (atteso 2.000000)" % r_d)
ok4 = abs(r_d - 2.0) < 1e-6
if t_c is not None:
    r_c = float(np.median(t_c / np.maximum(t_0, 1e-300)))
    print("  cs -> 2cs : tau_nuovo/tau_vecchio = %.6f   (atteso 0.500000)" % r_c)
    ok4 = ok4 and abs(r_c - 0.5) < 1e-6
dens = np.abs(net.psi[:net.n]) ** 2
rif = max(float(np.median(dens[dens > 1e-6])), 1e-6) if np.any(dens > 1e-6) else 1.0
tv0 = M_on.TAU_A * np.maximum(dens / rif, 0.05)
net.d = d0 * 2.0
dens2 = np.abs(net.psi[:net.n]) ** 2
rif2 = max(float(np.median(dens2[dens2 > 1e-6])), 1e-6) if np.any(dens2 > 1e-6) else 1.0
tv1 = M_on.TAU_A * np.maximum(dens2 / rif2, 0.05)
net.d = d0
print("  CONTRASTO - la legge VECCHIA con d -> 2d: rapporto = %.6f  (resta FERMA)"
      % float(np.median(tv1 / np.maximum(tv0, 1e-300))))
ESITI["T4"] = ok4
print("  T4: %s" % ("PASS - tau SEGUE lo stato da solo: e' una LEGGE" if ok4 else "FAIL - e' un NUMERO"))
CRONO["T4"] = time.perf_counter() - t0

# ==================================================================== T5
titolo("T5 - ampiezza e stabilita' (NON TOCCATO). I numeri sono del seme %d." % SEMI_T3[0])
t0 = time.perf_counter()
for eti, R in (("OFF", R_off), ("ON ", R_on)):
    b, se, r2, nn, omm, thm, n = R[SEMI_T3[0]]
    print("  %-3s  |omega| mediana %10.4g   theta %10.4g gradi/passo = %7.2f giri   n=%d"
          % (eti, omm, thm, thm / 360.0, n))
fatt = R_on[SEMI_T3[0]][5] / max(R_off[SEMI_T3[0]][5], 1e-300)
print("  fattore su theta: %.4f" % fatt)
net_on = evolvi(M_on, SEED, 60)
nb = np.asarray(net_on._nb[:net_on.n], float)
nrm = np.linalg.norm(nb, axis=1)
nan = int(np.sum(~np.isfinite(nb))) + int(np.sum(~np.isfinite(net_on.psi[:net_on.n])))
print("  |nb| max scostamento da 1: %.3e    NaN/inf: %d" % (float(np.max(np.abs(nrm - 1.0))), nan))
ESITI["T5"] = (nan == 0) and float(np.max(np.abs(nrm - 1.0))) < 1e-9
print("  T5: %s" % ("PASS" if ESITI["T5"] else "FAIL"))
CRONO["T5"] = time.perf_counter() - t0

# ==================================================================== T0 (chiusura)
titolo("T0 (chiusura) - il blob della FISICA e' ancora quello? Il sigillo NON deve aver scritto.")
BG1, BR1 = blob_git(os.path.join(RAD, "soliton_simulator.py"))
print("  PRIMA  git-blob %s  byte %s" % (BG0[:8], BR0[:8]))
print("  DOPO   git-blob %s  byte %s" % (BG1[:8], BR1[:8]))
ESITI["T0"] = (BG0 == BG1) and (BR0 == BR1)
print("  T0: %s" % ("PASS - il simulatore e' INTATTO" if ESITI["T0"] else "FAIL - IL SIGILLO HA SCRITTO SULLA FISICA"))

print()
print("=" * 110)
print("TEMPI (misurati, non stimati): " + "  ".join("%s=%.0fs" % (k, v) for k, v in CRONO.items()))
ordine = ["T0", "T1a", "T1b", "T2", "T3", "T4", "T5"]
print("ESITO: " + "   ".join("%s=%s" % (k, "PASS" if ESITI[k] else "FAIL") for k in ordine if k in ESITI))
print("SIGILLO COMPLESSIVO: %s" % ("PASS" if all(ESITI.values()) else "FAIL"))
print("=" * 110)
sys.exit(0 if all(ESITI.values()) else 1)
