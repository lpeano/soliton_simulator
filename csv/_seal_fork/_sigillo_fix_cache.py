# -*- coding: utf-8 -*-
"""SIGILLO della PATCH `_cs_nodo_prev` (eredita' alla mitosi) - P1..P4.

IL DIFETTO: la cache `_cs_nodo_prev` e' scritta a fine passo con l'`n` di quel passo (riga ~2918);
la mitosi AGGIUNGE nodi, quindi al passo dopo `len(csp) >= n` fallisce e `_tempo_luce_nodo` cade nel
ramo `else` -> `cs_nodo = CS_M` costante. Cioe' `tau = d/cs` calcolava in realta' `tau = d/CS_M`.
Tocca DUE chiamanti: `_bloch_ritardato` (STRATO 1) e il rilassamento sotto `--tau-luce`.

P1  flag OFF (TAU_LUCE, FORK_SU2_MEM, STEP2_OROLOGIO tutti OFF) -> byte-identico + stesso N.
P1b CONTROLLO NECESSARIO: col flag ON i due file devono DIFFERIRE. Una patch morta passerebbe P1.
P2  IL CONTATORE: % di chiamate che cadono nel fallback, PRIMA e DOPO, sugli stessi passi.
    Atteso ~80% -> ~0% (solo il primo passo, in cui un passato non esiste ancora).
P3  coerenza della cache: `len(_cs_nodo_prev) == n` a OGNI passo dopo il primo (verifica esplicita).
P4  stabilita': niente NaN/inf, `cs_nodo` positivo e finito, |nb| = 1.
"""
import contextlib, importlib.util, io, os, sys
import numpy as np

RAD = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(RAD); sys.path.insert(0, RAD)
BASE = ["--batch", "--nmasse", "3", "--sep", "8", "--passi", "1", "--ogni", "100000",
        "--db-ogni", "100000", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
        "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--cs-dinamico",
        "--fork-su2", "--csv", os.path.join(os.environ.get("TMP", "."), "_sigfix.csv")]
CAMPI = ("pos", "phi", "phi0", "phivel", "eta", "d", "d0", "vd", "peq", "tw", "twp", "i", "j",
         "perc_chi", "perc_tw", "_nb", "_nb_prec", "_nb_ret", "_psi_spinor", "omega_s", "psi")
VECCHIO = os.path.join("csv", "_seal_fork", "_old_sim_pre_fixcache.py")


def carica(percorso, nome, extra=()):
    spec = importlib.util.spec_from_file_location(nome, percorso)
    M = importlib.util.module_from_spec(spec); sys.modules[nome] = M
    sys.argv = ["soliton_simulator.py"] + BASE + list(extra)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(M)
        a = M._cli(); M._applica_regime(a); M._applica_flag(a)
    return M


def conta_fallback(M):
    """Strumenta il ramo else ANCHE nel file vecchio, senza toccarne la fisica.

    Il wrapper valuta la STESSA condizione della guardia (sola lettura) e poi delega al metodo
    originale: non cambia un byte del risultato, non consuma RNG. Serve perche' il file PRIMA della
    patch non ha contatori, e senza un PRIMA il DOPO non dimostra niente.
    """
    orig = M.Rete._tempo_luce_nodo
    stato = {"tot": 0, "fb": 0}

    def wrap(self, ii, jj):
        stato["tot"] += 1
        csp = getattr(self, "_cs_nodo_prev", None)
        if not (csp is not None and len(csp) >= self.n):
            stato["fb"] += 1
        return orig(self, ii, jj)
    M.Rete._tempo_luce_nodo = wrap
    return stato


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


def evolvi(M, seed, n, traccia=None):
    net = scena(M, seed)
    for k in range(n):
        passo(M, net)
        if traccia is not None:
            csp = getattr(net, "_cs_nodo_prev", None)
            traccia.append((k + 1, net.n, -1 if csp is None else len(csp)))
    return net


def confronta(a, b):
    print("  PRESIDIO: uno zero con N DIVERSO e' MANCANZA DI CONFRONTO, non identita'.")
    print("    n_A = %d   n_B = %d   ->  %s" % (a.n, b.n, "CONFRONTABILI" if a.n == b.n else "NON CONFRONTABILI"))
    if a.n != b.n:
        return False, float("nan")
    ok = True
    peggio = 0.0
    for c in CAMPI:
        va, vb = getattr(a, c, None), getattr(b, c, None)
        if va is None or vb is None:
            continue
        va, vb = np.asarray(va), np.asarray(vb)
        if va.shape != vb.shape:
            print("    %-14s SHAPE diversa" % c)
            ok = False
            continue
        d = float(np.max(np.abs(va.astype(complex) - vb.astype(complex)))) if va.size else 0.0
        peggio = max(peggio, d)
        if d != 0.0:
            ok = False
            print("    %-14s max|A-B| = %.3e" % (c, d))
    rng = (a.rng.bit_generator.state == b.rng.bit_generator.state)
    print("    %d campi, PEGGIOR max|A-B| = %.3e   stato RNG %s"
          % (len(CAMPI), peggio, "identico" if rng else "DIVERSO"))
    return (ok and rng), peggio


def main():
    SEED, PASSI = 1, 30
    esiti = {}
    print("=" * 104)
    print("P1 - flag OFF (no --fork-su2-mem, no --step2-orologio, no --tau-luce): la cache non nasce")
    print("=" * 104)
    v_off = carica(VECCHIO, "sim_v_off")
    n_off = carica("soliton_simulator.py", "sim_n_off")
    print("  nuovo: FORK_SU2_MEM=%s  STEP2_OROLOGIO=%s  TAU_LUCE=%s"
          % (n_off.FORK_SU2_MEM, n_off.STEP2_OROLOGIO, n_off.TAU_LUCE))
    ok1, _ = confronta(evolvi(v_off, SEED, PASSI), evolvi(n_off, SEED, PASSI))
    esiti["P1"] = ok1
    print("  P1: %s" % ("PASS" if ok1 else "FAIL"))

    print()
    print("=" * 104)
    print("P1b - CONTROLLO: col flag ON i due file DEVONO differire (una patch morta passerebbe P1)")
    print("=" * 104)
    v_on = carica(VECCHIO, "sim_v_on", ["--fork-su2-mem"])
    n_on = carica("soliton_simulator.py", "sim_n_on", ["--fork-su2-mem"])
    tr_v, tr_n = [], []
    st_v = conta_fallback(v_on)
    st_n = conta_fallback(n_on)
    net_v = evolvi(v_on, SEED, PASSI, tr_v)
    net_n = evolvi(n_on, SEED, PASSI, tr_n)
    uguali, peggio = confronta(net_v, net_n)
    esiti["P1b"] = (not uguali)
    print("  P1b (devono DIFFERIRE): %s   (peggior scarto %.3e)"
          % ("PASS" if esiti["P1b"] else "FAIL - la patch non ha effetto", peggio))

    print()
    print("=" * 104)
    print("P2 - IL CONTATORE del ramo else, PRIMA e DOPO, sugli STESSI passi")
    print("=" * 104)
    fv = 100.0 * st_v["fb"] / max(st_v["tot"], 1)
    fn = 100.0 * st_n["fb"] / max(st_n["tot"], 1)
    print("  PRIMA  (file pre-patch): fallback %4d su %4d chiamate = %6.2f %%" % (st_v["fb"], st_v["tot"], fv))
    print("  DOPO   (file patchato) : fallback %4d su %4d chiamate = %6.2f %%" % (st_n["fb"], st_n["tot"], fn))
    print("  contatori interni del file patchato: _cs_fallback=%s  _cs_chiamate=%s  ultimo(n,len)=%s"
          % (getattr(net_n, "_cs_fallback", None), getattr(net_n, "_cs_chiamate", None),
             getattr(net_n, "_cs_fallback_ultimo", None)))
    esiti["P2"] = (fv > 50.0) and (fn <= 5.0)
    print("  P2 (prima > 50 %%, dopo <= 5 %%): %s" % ("PASS" if esiti["P2"] else "FAIL"))

    print()
    print("=" * 104)
    print("P3 - coerenza della cache passo per passo: len(_cs_nodo_prev) == n")
    print("=" * 104)
    print("  passo |     n | len PRIMA | len DOPO | DOPO usabile?")
    male_n = male_v = 0
    for (k, nv, lv), (k2, nn, ln) in zip(tr_v, tr_n):
        if ln < nn:
            male_n += 1
        if lv < nv:
            male_v += 1
        if k in (1, 2, 6, 12, 20, 30):
            print("  %5d | %5d | %9d | %8d | %s" % (k, nn, lv, ln, "SI" if ln >= nn else "NO"))
    print("  passi con cache INUSABILE: PRIMA %d/%d    DOPO %d/%d"
          % (male_v, len(tr_v), male_n, len(tr_n)))
    esiti["P3"] = (male_n == 0)
    print("  P3: %s" % ("PASS" if esiti["P3"] else "FAIL"))

    print()
    print("=" * 104)
    print("P4 - stabilita'")
    print("=" * 104)
    nb = np.asarray(net_n._nb[:net_n.n], float)
    nrm = np.linalg.norm(nb, axis=1)
    nan = int(np.sum(~np.isfinite(nb))) + int(np.sum(~np.isfinite(net_n.psi[:net_n.n])))
    csp = np.asarray(net_n._cs_nodo_prev, float)
    tau = n_on.Rete._tempo_luce_nodo(net_n, net_n.i, net_n.j)
    print("  |nb| max scostamento da 1: %.3e    NaN/inf su nb+psi: %d"
          % (float(np.max(np.abs(nrm - 1.0))), nan))
    print("  cs cache: min %.6g  max %.6g  finiti %s   (CS_M = %.6g)"
          % (float(csp.min()), float(csp.max()), bool(np.all(np.isfinite(csp))), n_on.CS_M))
    print("  cs DISPERSIONE: max/min = %.6f   -> %s"
          % (float(csp.max() / max(csp.min(), 1e-300)),
             "cs VARIA davvero (il fallback lo appiattiva a CS_M)" if csp.max() > csp.min() * 1.0000001
             else "cs e' costante: qui la patch non cambia nulla di fisico"))
    print("  tau = d/cs: min %.6g  max %.6g  finiti %s"
          % (float(tau.min()), float(tau.max()), bool(np.all(np.isfinite(tau)))))
    esiti["P4"] = (nan == 0) and float(np.max(np.abs(nrm - 1.0))) < 1e-9 and \
                  bool(np.all(np.isfinite(csp))) and float(csp.min()) > 0.0 and \
                  bool(np.all(np.isfinite(tau))) and float(tau.min()) > 0.0
    print("  P4: %s" % ("PASS" if esiti["P4"] else "FAIL"))

    print()
    print("=" * 104)
    print("ESITO: " + "   ".join("%s=%s" % (k, "PASS" if v else "FAIL") for k, v in esiti.items()))
    print("SIGILLO PATCH CACHE: %s" % ("PASS" if all(esiti.values()) else "FAIL"))
    print("=" * 104)
    return 0 if all(esiti.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
