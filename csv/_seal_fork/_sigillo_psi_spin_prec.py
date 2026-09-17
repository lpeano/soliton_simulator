# -*- coding: utf-8 -*-
"""SIGILLO della cura di `_psi_spin_prec` (eredita' alla mitosi) — S1..S5.

IL DIFETTO (FASE A, `doc/REPERTO_psi_spin_prec.md`): `_psi_spin_prec` e' scritto a fine passo con
l'`n` di quel passo e **non era esteso alla mitosi**, quindi la guardia ESATTA di `ritmo()`
(`len(_ps) == n and len(_psp) == n`) scartava il ramo a 4pi nel **95.33 %** delle chiamate. `r`
veniva dal ritmo **SCALARE a 2pi**, quello storico: la **FASE 5 era inerte**.

S1  `--campo-spinoriale` OFF -> byte-identico + stesso N (li' `_psi_spin_prec` non nasce nemmeno).
S1b CONTROLLO NECESSARIO: con `--campo-spinoriale` ON i due file DEVONO differire. Una cura morta
    passerebbe S1, S3 e S5.
S2  IL CONTATORE: % di fallimento della guardia 4pi, PRIMA e DOPO, sugli stessi passi. Atteso
    95.33 % -> ~0 %.
S3  coerenza: `len(_psi_spin_prec) == n` a ogni passo dopo il primo. Verifica ESPLICITA.
S4  **QUI LA FISICA CAMBIA, ED E' ATTESO.** `r` ricomincia ad aggiornarsi col 4pi -> `dt_n = DT*r`
    cambia -> il run ON **non sara' byte-identico, e non deve esserlo**. Si QUANTIFICA di quanto:
    mediana di `r`, dispersione fra nodi, SE della mediana, e lo scarto fra i due rami con la sua
    barra. *Nessuna statistica senza barra d'errore (par.9).*
S5  stabilita': niente NaN/inf, `r` positivo e finito.
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
import contextlib, importlib.util, io, os, sys
import numpy as np

RAD = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(RAD); sys.path.insert(0, RAD)
COMUNE = ["--batch", "--nmasse", "3", "--sep", "8", "--passi", "1", "--ogni", "100000",
          "--db-ogni", "100000", "--spinore-vivo", "--spinore-corretto",
          "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--cs-dinamico",
          "--fork-su2", "--fork-su2-mem", "--csv", os.path.join(os.environ.get("TMP", "."), "_sps.csv")]
CAMPI = ("pos", "phi", "phi0", "phivel", "eta", "d", "d0", "vd", "peq", "tw", "twp", "i", "j",
         "perc_chi", "perc_tw", "_nb", "_nb_prec", "_nb_ret", "_psi_spinor", "omega_s", "psi")
VECCHIO = os.path.join("csv", "_seal_fork", "_old_sim_pre_psispin.py")
SEED, PASSI = 1, 60


def carica(percorso, nome, spin=True):
    spec = importlib.util.spec_from_file_location(nome, percorso)
    M = importlib.util.module_from_spec(spec); sys.modules[nome] = M
    extra = ["--campo-spinoriale"] if spin else []
    sys.argv = ["soliton_simulator.py"] + COMUNE + extra
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(M)
        a = M._cli(); M._applica_regime(a); M._applica_flag(a)
    return M


def strumenta(M):
    """Wrapper PURE-READ su `ritmo()`: conta gli esiti della guardia e registra `r`.

    Valuta le STESSE condizioni in sola lettura, poi delega. Non consuma RNG, non muta stato.
    """
    orig = M.Rete.ritmo
    st = {"tot": 0, "ko": 0, "ok": 0, "ant": 0, "len_ko": 0, "r": [], "coer": []}

    def wrap(self):
        n = self.n
        _pp = getattr(self, "_psi_prec", None)
        _ps = getattr(self, "psi_spin", None)
        _psp = getattr(self, "_psi_spin_prec", None)
        st["tot"] += 1
        if _pp is None or len(_pp) != n:
            st["ant"] += 1
        elif (M.CAMPO_SPINORIALE and _ps is not None and _psp is not None
              and len(_ps) == n and len(_psp) == n):
            st["ok"] += 1
        else:
            st["ko"] += 1
            if _psp is not None and len(_psp) != n:
                st["len_ko"] += 1
        r = orig(self)
        if r is not None:
            ra = np.asarray(r, float)
            st["r"].append((float(np.median(ra)), float(np.std(ra)), int(ra.size)))
        return r
    M.Rete.ritmo = wrap
    return st


def passo(M, net):
    M.scuoti_vuoto(net); net.step(); net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()


def evolvi(M, seed, n, st=None):
    net = M.Rete(seed); net.semina(80)
    for _ in range(6):
        passo(M, net)
    Nc = M.massa_critica_collasso()
    for k in range(3):
        ang = 2 * np.pi * k / 3
        net.nuova_massa(int(Nc * 0.6), raggio=0.8,
                        centro=(8.0 * np.cos(ang), 8.0 * np.sin(ang), 0.0), fase=0.0)
    if st is not None:
        for k in ("tot", "ko", "ok", "ant", "len_ko"):
            st[k] = 0
        st["r"].clear(); st["coer"].clear()
    for _ in range(n):
        passo(M, net)
        if st is not None:
            _p = getattr(net, "_psi_spin_prec", None)
            st["coer"].append((net.n, -1 if _p is None else len(_p)))
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
            print("    %-14s SHAPE diversa" % c); ok = False; continue
        d = float(np.max(np.abs(va.astype(complex) - vb.astype(complex)))) if va.size else 0.0
        peggio = max(peggio, d)
        if d != 0.0:
            ok = False
            print("    %-14s max|A-B| = %.3e" % (c, d))
    rng = (a.rng.bit_generator.state == b.rng.bit_generator.state)
    print("    %d campi, PEGGIOR max|A-B| = %.3e   stato RNG %s"
          % (len(CAMPI), peggio, "identico" if rng else "DIVERSO"))
    return (ok and rng), peggio


def stat_r(net, M, eti):
    """Mediana/dispersione/SE di `r` a fine run. Snapshot/restore: `ritmo()` puo' toccare
    `_psi_prec` sul ramo di return anticipato, e un diagnostico non deve mutare lo stato."""
    snap = {k: (None if getattr(net, k, None) is None else np.array(getattr(net, k), copy=True))
            for k in ("_psi_prec", "_psi_spin_prec")}
    rngst = net.rng.bit_generator.state
    r = M.Rete.ritmo(net)
    for k, v in snap.items():
        setattr(net, k, v)
    net.rng.bit_generator.state = rngst
    ra = np.asarray(r, float) if r is not None else np.ones(net.n)
    med = float(np.median(ra)); sd = float(np.std(ra)); nn = int(ra.size)
    se = 1.2533 * sd / np.sqrt(nn)          # SE della MEDIANA (normale): 1.2533*sigma/sqrt(n)
    print("  %-10s r: mediana %.6f +- %.6f (SE)   dev.std fra nodi %.6f   n %d   min %.6f  max %.6f"
          % (eti, med, se, sd, nn, float(ra.min()), float(ra.max())))
    return med, se, sd, nn, ra


def main():
    esiti = {}
    print("=" * 108)
    print("S1 - --campo-spinoriale OFF: `_psi_spin_prec` non nasce, la cura e' un no-op esatto")
    print("=" * 108)
    v_off = carica(VECCHIO, "sps_v_off", spin=False)
    n_off = carica("soliton_simulator.py", "sps_n_off", spin=False)
    print("  CAMPO_SPINORIALE nel modulo nuovo (deve essere False): %s" % n_off.CAMPO_SPINORIALE)
    ok1, _ = confronta(evolvi(v_off, SEED, PASSI), evolvi(n_off, SEED, PASSI))
    esiti["S1"] = ok1
    print("  S1: %s" % ("PASS" if ok1 else "FAIL"))

    print()
    print("=" * 108)
    print("S1b - CONTROLLO: con --campo-spinoriale ON i due file DEVONO differire")
    print("=" * 108)
    v_on = carica(VECCHIO, "sps_v_on", spin=True)
    n_on = carica("soliton_simulator.py", "sps_n_on", spin=True)
    st_v = strumenta(v_on); st_n = strumenta(n_on)
    net_v = evolvi(v_on, SEED, PASSI, st_v)
    net_n = evolvi(n_on, SEED, PASSI, st_n)
    uguali, peggio = confronta(net_v, net_n)
    esiti["S1b"] = (not uguali)
    print("  S1b (devono DIFFERIRE): %s   (peggior scarto %.3e)"
          % ("PASS" if esiti["S1b"] else "FAIL - la cura non ha effetto", peggio))

    print()
    print("=" * 108)
    print("S2 - IL CONTATORE della guardia 4pi, PRIMA e DOPO, sugli STESSI passi")
    print("=" * 108)
    for eti, st in (("PRIMA", st_v), ("DOPO ", st_n)):
        t = max(st["tot"], 1)
        print("  %s  4pi passa %4d   4pi FALLISCE %4d = %6.2f %%   anticipato %3d   (di cui len != n: %d)"
              % (eti, st["ok"], st["ko"], 100.0 * st["ko"] / t, st["ant"], st["len_ko"]))
    fv = 100.0 * st_v["ko"] / max(st_v["tot"], 1)
    fn = 100.0 * st_n["ko"] / max(st_n["tot"], 1)
    esiti["S2"] = (fv > 50.0) and (fn <= 5.0)
    print("  S2 (prima > 50 %%, dopo <= 5 %%): %s" % ("PASS" if esiti["S2"] else "FAIL"))

    print()
    print("=" * 108)
    print("S3 - coerenza passo per passo: len(_psi_spin_prec) == n")
    print("=" * 108)
    male_v = sum(1 for n, l in st_v["coer"] if l != n)
    male_n = sum(1 for n, l in st_n["coer"] if l != n)
    print("  passo |     n | len PRIMA | len DOPO")
    for k in (1, 2, 5, 20, 40, PASSI):
        if k <= len(st_n["coer"]):
            print("  %5d | %5d | %9d | %8d" % (k, st_n["coer"][k - 1][0],
                                               st_v["coer"][k - 1][1], st_n["coer"][k - 1][1]))
    print("  passi con len != n:  PRIMA %d/%d    DOPO %d/%d"
          % (male_v, len(st_v["coer"]), male_n, len(st_n["coer"])))
    esiti["S3"] = (male_n == 0)
    print("  S3: %s" % ("PASS" if esiti["S3"] else "FAIL"))

    print()
    print("=" * 108)
    print("S4 - DI QUANTO CAMBIA `r` (e quindi dt_n = DT*r). LA FISICA CAMBIA, ED E' ATTESO.")
    print("=" * 108)
    mv, sev, sdv, nv, rav = stat_r(net_v, v_on, "PRIMA")
    mn, sen, sdn, nn_, ran = stat_r(net_n, n_on, "DOPO ")
    dm = mn - mv
    sed = float(np.hypot(sev, sen))
    print("  scarto sulla mediana di r: %+.6f +- %.6f   ->  %.3f %% del valore, z = %.2f"
          % (dm, sed, 100.0 * dm / max(abs(mv), 1e-12), abs(dm) / max(sed, 1e-12)))
    print("  dispersione fra nodi:  PRIMA %.6f   DOPO %.6f   (rapporto %.4f)"
          % (sdv, sdn, sdn / max(sdv, 1e-12)))
    print("  traiettoria della mediana di r (ultimi 5 passi):")
    print("    PRIMA %s" % "  ".join("%.5f" % x[0] for x in st_v["r"][-5:]))
    print("    DOPO  %s" % "  ".join("%.5f" % x[0] for x in st_n["r"][-5:]))
    print("  NB: S4 non ha una soglia PASS/FAIL - e' una QUANTIFICAZIONE. Il numero qui sopra e' il")
    print("      contenuto fisico della cura, e va riportato, non giudicato.")
    esiti["S4"] = True

    print()
    print("=" * 108)
    print("S5 - stabilita'")
    print("=" * 108)
    nb = np.asarray(net_n._nb[:net_n.n], float)
    nrm = np.linalg.norm(nb, axis=1)
    nan = int(np.sum(~np.isfinite(nb))) + int(np.sum(~np.isfinite(net_n.psi[:net_n.n])))
    print("  |nb| max scostamento da 1: %.3e    NaN/inf su nb+psi: %d"
          % (float(np.max(np.abs(nrm - 1.0))), nan))
    print("  r: finito %s   positivo %s   min %.6f" % (bool(np.all(np.isfinite(ran))),
                                                       bool(np.all(ran > 0)), float(ran.min())))
    print("  N nodi: PRIMA %d   DOPO %d" % (net_v.n, net_n.n))
    esiti["S5"] = (nan == 0) and float(np.max(np.abs(nrm - 1.0))) < 1e-9 \
        and bool(np.all(np.isfinite(ran))) and bool(np.all(ran > 0))
    print("  S5: %s" % ("PASS" if esiti["S5"] else "FAIL"))

    print()
    print("=" * 108)
    print("ESITO: " + "   ".join("%s=%s" % (k, "PASS" if v else "FAIL") for k, v in esiti.items()))
    print("SIGILLO _psi_spin_prec: %s" % ("PASS" if all(esiti.values()) else "FAIL"))
    print("PROMEMORIA: S4 non dice che questo chiuda T3. Non e' stato misurato qui, e un difetto")
    print("            grande non implica un effetto grande (la cache cs lo ha appena dimostrato).")
    print("=" * 108)
    return 0 if all(esiti.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
