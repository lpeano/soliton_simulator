# -*- coding: utf-8 -*-
"""SIGILLO DEL RAMO D -- le tre modifiche, un sigillo solo.

Criteri fissati PRIMA in `doc/TASK_HISTORY/2026-09-21_ramo_D_tre_modifiche.md` (`81bf5d7`),
committato PRIMA del codice (`11b6431`): l'ordine e' verificabile da git, non asserito qui.

  Z0  i tre blob, in BYTE GREZZI (`sha1`), mai `git hash-object` (C18).
  Z1  [BLOCCANTE] TUTTI i flag spenti -> stato BYTE-IDENTICO al simulatore PRIMA delle due
      modifiche nuove. Una sola divergenza = STOP.
  Z2  [BLOCCANTE] OGNI FLAG DA SOLO produce un effetto, e non banale. TRE controlli positivi:
      un flag che non cambia niente e' codice morto (par.10.2).
  Z3  [BLOCCANTE] `CHI_COOP`: le chiamate della torsione ricevono `perc_geom`, quella del campo
      `B` riceve `perc_chi`; `perc_chi == segno di doppia copertura`; `chi_basc` non scrive MAI
      `perc_chi`.
  Z4  [BLOCCANTE] `SCALA_MIN`, e qui ci sono QUATTRO numeri, non uno:
      Z4a  IL SIGILLO DECISIVO -- il vincolo NON CREA MOVIMENTO. Misurato a OGNI scrittura di
           TUTTO il run, non al solo primo passo. ⚠ CRITERIO CORRETTO IL 2026-09-21 (`Z86`): la
           prima versione chiedeva `max(eff - dx) <= 0`, FALSO PER COSTRUZIONE perche' attenuare
           una discesa rende l'incremento MENO negativo. La proprieta' vera e' che il nuovo
           valore stia sempre in `[x + dx, x]`:
             `_g_sm_viol_id == 0`    un incremento >= 0 non e' MAI stato toccato: le lunghezze
                                     che non scendono non cambiano DI UN BIT;
             `_g_sm_max_giu <= 0`    il massimo di `eff` sulle sole DISCESE: il vincolo non
                                     spinge MAI verso l'alto, quindi niente inflazione;
             `_g_sm_viol_giu == 0`   il vincolo non APPROFONDISCE mai una discesa.
           ⚠ NON E' UN ALLARGAMENTO: il vecchio guardava la DIFFERENZA, il nuovo il SEGNO.
      Z4b  `min(d0) >= LAM` e `min(d) >= LAM`.
      Z4c  lo stress `|d-d0|/d0` resta FINITO.
      Z4d  `_g_sm_patol` -- il caso `dx <= -x`, CONTATO e non tappato. Si RIPORTA sempre; se
           non e' zero, `Z4b` puo' legittimamente cadere e va letto insieme a questo.
  Z5  [BLOCCANTE] `COES_ADIM`: `|delta d0|` da quel sito `<= passo_causale`, SEMPRE.
  Z6  [BLOCCANTE] tutti accesi: nessun `NaN`, nessun `inf`, lunghezze di tutti gli array = `n`.
  Z7  il sigillo interno della rigiocata -- NON e' qui, si gira a parte.

⚠ IL SIMULATORE PRIMA si estrae con `git cat-file -p` IN BINARIO, mai con `git checkout`
  (par.5-quinquies, la trappola CRLF).
ASCII PURO.
"""
import hashlib
import os
import re
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SIM_ORA = os.path.join(RADICE, "soliton_simulator.py")
COMMIT_PRIMA = "0f4fc1e"        # l ultimo commit PRIMA di SCALA_MIN e COES_ADIM
for _x in sys.argv[1:]:
    if _x.startswith("--commit-prima="):
        COMMIT_PRIMA = _x.split("=", 1)[1]
PASSI = 30
CAMPI = ("d0", "d", "vd", "psi", "phi", "eta", "perc_chi", "tw", "omega_s", "pos")

esiti = []


def segna(nome, ok, det):
    esiti.append((nome, ok))
    print("%-5s %-6s %s" % (nome, "PASS" if ok else "FAIL", det))


# ------------------------------------------------- il lavoratore di Z8 (neutralita')
if "--z8" in sys.argv:
    # Z8: LA RICOSTRUZIONE DEL MONDO E' NEUTRA? Con OGNI flag al default di MODULO, il mondo
    # ricostruito dev'essere BYTE-IDENTICO a quello dell' `import`. Isola il MECCANISMO dalla
    # FISICA: se qui passa, la cura non aggiunge NIENTE da sola, e ogni differenza vista altrove
    # e' un flag che finalmente AGISCE sul vuoto invece di essere inerte.
    os.chdir(RADICE)
    sys.argv = ["soliton_simulator.py"]
    import importlib.util as _iu8
    _sp8 = _iu8.spec_from_file_location("_sim_z8", SIM_ORA)
    S8 = _iu8.module_from_spec(_sp8); sys.modules["_sim_z8"] = S8
    _sp8.loader.exec_module(S8)
    _k = ("d", "d0", "i", "j", "pos", "phi", "eta", "omega_s", "perc_chi")
    _imp = {k: np.array(getattr(S8.net, k), copy=True) for k in _k}
    _r = S8.Rete(42); _r.semina(S8.SEME_INIZIALE)
    _df = []
    for k, v in _imp.items():
        w = np.asarray(getattr(_r, k))
        if v.shape != w.shape:
            _df.append("%s(shape)" % k)
        elif not np.array_equal(v, w):
            _df.append("%s(max|d|=%.3e)" % (k, float(np.nanmax(np.abs(v - w)))))
    print("Z8DATI campi=%d diversi=%d nodi=%d archi=%d dettaglio=%s"
          % (len(_imp), len(_df), S8.net.n, len(S8.net.i),
             ("|".join(_df[:5]) if _df else "nessuno")))
    raise SystemExit(0)


# ----------------------------------------------------------------- il lavoratore
if "--lavoro" in sys.argv:
    simp = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--sim=")][0]
    outp = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--out=")][0]
    fl = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--flag=")]
    fl = fl[0].split(",") if fl and fl[0] else []
    os.chdir(RADICE)
    base = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
            "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
            "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
            "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
            "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--plast-din",
            "--viriale", "--olon-part"]
    sys.argv = base + ["--" + f for f in fl if f]
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("_sim_x", simp)
    S = _iu.module_from_spec(_sp)
    sys.modules["_sim_x"] = S
    _sp.loader.exec_module(S)
    for f in fl:
        nome = f.replace("-", "_").upper()
        if f and not hasattr(S, nome):
            raise SystemExit("questo simulatore non ha %s" % nome)
    a = S._cli(); S._applica_regime(a); S._applica_flag(a)
    S._NMASSE_VIDEO["n"] = 3; S._NMASSE_VIDEO["sep"] = 4.0; S._NMASSE_VIDEO["size"] = None
    S.avvia_test("N-MASSE")()
    net = S.net
    S.stato["nframe"] = 0
    LAMv = float(S.LAM)

    min_d = min_d0 = np.inf
    max_stress = 0.0
    car_bad = car_tot = 0
    n_passi = 0
    for _f in range(PASSI // int(S.PASSI_PER_FRAME)):
        S.passo_test()
        for _ in range(int(S.PASSI_PER_FRAME)):
            S.scuoti_vuoto(net); net.step()
            n_passi += 1
            nn = net.n
            if len(net.d0):
                min_d0 = min(min_d0, float(np.min(net.d0)))
                min_d = min(min_d, float(np.min(net.d)))
                st = np.abs(net.d - net.d0) / np.maximum(net.d0, 1e-300)
                if np.all(np.isfinite(st)):
                    max_stress = max(max_stress, float(np.max(st)))
                else:
                    max_stress = np.inf
            if "chi-coop" in fl and len(getattr(net, "_psi_spinor", [])) >= nn:
                _c = net._bloch_a_spinore(net._nb[:nn])
                _o = np.sum(np.conj(_c) * net._psi_spinor[:nn], axis=1)
                car_tot += 1
                if not np.array_equal(np.asarray(net.perc_chi[:nn]),
                                      np.where(np.real(_o) >= 0.0, 1, -1)):
                    car_bad += 1
            net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()

    d = {k: np.asarray(getattr(net, k)) for k in CAMPI if hasattr(net, k)}
    np.savez(outp, **d)
    g = lambda k, dflt=0: getattr(net, k, dflt)
    print("LAM %.12f" % LAMv)
    print("MIN d=%.12f d0=%.12f" % (min_d, min_d0))
    print("STRESS max=%s" % ("inf" if not np.isfinite(max_stress) else "%.6e" % max_stress))
    print("SM tot=%d discese=%d patol=%d pav_saltati=%d viol_id=%d viol_giu=%d nascite=%d"
          % (g("_g_sm_tot"), g("_g_sm_discese"), g("_g_sm_patol"),
             g("_g_sm_pav_saltati"), g("_g_sm_viol_id"), g("_g_sm_viol_giu"),
             g("_g_sm_nascite")))
    print("SMGIU max_giu=%s" % repr(g("_g_sm_max_giu", None)))
    print("COES usi=%d tetto=%.12e max=%.12e satura=%d archi=%d"
          % (g("_g_coes_adim_usi"), g("_g_coes_tetto", 0.0), g("_g_coes_max", 0.0),
             g("_g_coes_satura"), g("_g_coes_archi")))
    print("COOP ccl_geom=%d ccl_chi=%d bas_geom=%d bas_chi=%d"
          % (g("_g_ccl_geom"), g("_g_ccl_chi"), g("_g_chibasc_su_geom"), g("_g_chibasc_su_chi")))
    print("CARICA bad=%d controllati=%d" % (car_bad, car_tot))
    # Z6: tutte le lunghezze dei vettori PER NODO pari a n
    pern = ("psi", "phi", "eta", "perc_chi", "perc_geom", "perc_tw", "pos", "omega_s")
    male = [k for k in pern if hasattr(net, k) and len(getattr(net, k)) != net.n]
    print("LEN n=%d male=%s" % (net.n, ",".join(male) if male else "nessuno"))
    nan = [k for k, v in d.items() if v.dtype.kind in "fc" and not np.all(np.isfinite(v))]
    print("NAN campi=%s" % (",".join(nan) if nan else "nessuno"))
    raise SystemExit(0)


def gira(sim, out, flag=()):
    cmd = [sys.executable, os.path.abspath(__file__), "--lavoro",
           "--sim=%s" % sim, "--out=%s" % out, "--flag=%s" % ",".join(flag)]
    pr = subprocess.run(cmd, cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    if pr.returncode != 0:
        print(pr.stdout[-1500:]); print(pr.stderr[-2500:])
        raise SystemExit("lavoratore uscito con %d  (flag: %s)" % (pr.returncode, flag))
    return pr.stdout


def num(out, chiave, campo, tipo=int):
    m = re.search(r"^%s .*\b%s=(\S+)" % (chiave, campo), out, re.M)
    if not m:
        return None
    v = m.group(1)
    try:
        return tipo(v)
    except ValueError:
        return v


def diff(x, y):
    f = []
    for k in CAMPI:
        if k not in x or k not in y:
            f.append("%s(assente)" % k); continue
        a, b = x[k], y[k]
        if a.shape != b.shape:
            f.append("%s(shape %s vs %s)" % (k, a.shape, b.shape))
        elif not np.array_equal(a, b):
            f.append("%s(max|d|=%.3e)" % (k, float(np.nanmax(np.abs(a - b)))))
    return f


def main():
    base = os.path.join(RADICE, "csv", "_seal_fork", "_sig_ramo_D")
    os.makedirs(base, exist_ok=True)
    vecchio = os.path.join(base, "_sim_prima.py")
    q = subprocess.run(["git", "cat-file", "-p", "%s:soliton_simulator.py" % COMMIT_PRIMA],
                       cwd=RADICE, capture_output=True)
    if q.returncode != 0:
        raise SystemExit("non riesco a estrarre il simulatore di %s" % COMMIT_PRIMA)
    with open(vecchio, "wb") as f:
        f.write(q.stdout)
    with open(SIM_ORA, "rb") as f:
        dn = f.read()
    print("Z0  simulatore PRIMA (%s): sha1 GREZZO %s"
          % (COMMIT_PRIMA, hashlib.sha1(q.stdout).hexdigest()[:8]))
    print("Z0  simulatore ORA            : sha1 GREZZO %s" % hashlib.sha1(dn).hexdigest()[:8])
    print("Z0  (NB: NON e' `git hash-object`. Sono due numeri diversi per lo stesso file, C18.)")
    print("")

    prz8 = subprocess.run([sys.executable, os.path.abspath(__file__), "--z8"], cwd=RADICE,
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    if prz8.returncode != 0:
        print(prz8.stdout[-800:]); print(prz8.stderr[-1500:])
        raise SystemExit("il lavoratore Z8 e' uscito con %d" % prz8.returncode)
    z8 = prz8.stdout
    z8d = num(z8, "Z8DATI", "diversi")
    segna("Z8", z8d == 0,
          "LA RICOSTRUZIONE DEL MONDO E' NEUTRA: con ogni flag al DEFAULT, il mondo ricostruito "
          "e' %s a quello dell'import (%s campi, %s nodi, %s archi) -> %s"
          % ("BYTE-IDENTICO" if z8d == 0 else "DIVERSO", num(z8, "Z8DATI", "campi"),
             num(z8, "Z8DATI", "nodi"), num(z8, "Z8DATI", "archi"),
             num(z8, "Z8DATI", "dettaglio", str)))
    print("")

    bracci = [("A_prima", vecchio, ()),
              ("B_spenti", SIM_ORA, ()),
              ("C1_scalamin", SIM_ORA, ("scala-min",)),
              ("C2_coesadim", SIM_ORA, ("coes-adim",)),
              ("C3_chicoop", SIM_ORA, ("chi-coop",)),
              ("D_tutti", SIM_ORA, ("scala-min", "coes-adim", "chi-coop"))]
    out = {}
    dat = {}
    for nome, sim, fl in bracci:
        print("braccio %-14s flag: %s" % (nome, ", ".join(fl) if fl else "(nessuno)"))
        p = os.path.join(base, nome + ".npz")
        out[nome] = gira(sim, p, fl)
        dat[nome] = np.load(p)
    print("")

    # ------------------------------------------------------------------ Z1
    f1 = diff(dat["A_prima"], dat["B_spenti"])
    segna("Z1", not f1, "tutti i flag spenti: %d campi -> %s"
          % (len(CAMPI), "BYTE-IDENTICI" if not f1 else "DIVERSI: %s" % f1[:6]))
    if f1:
        print("  *** Z1 e' BLOCCANTE: le modifiche toccano il ramo spento. FERMO. ***")
        return 1

    # ------------------------------------------------------------------ Z2
    tutti_ok = True
    for nome, etich in (("C1_scalamin", "scala-min"), ("C2_coesadim", "coes-adim"),
                        ("C3_chicoop", "chi-coop")):
        d2 = diff(dat["B_spenti"], dat[nome])
        ok = len(d2) > 0
        tutti_ok = tutti_ok and ok
        print("      %-12s da solo: %d campi su %d differiscono da tutto-spento"
              % (etich, len(d2), len(CAMPI)))
    segna("Z2", tutti_ok, "ogni flag DA SOLO produce un effetto (nessuno e' codice morto)")

    # ------------------------------------------------------------------ Z3
    oD = out["D_tutti"]
    gg, gc = num(oD, "COOP", "ccl_geom"), num(oD, "COOP", "ccl_chi")
    bg, bc = num(oD, "COOP", "bas_geom"), num(oD, "COOP", "bas_chi")
    cb, ct = num(oD, "CARICA", "bad"), num(oD, "CARICA", "controllati")
    segna("Z3", (gg or 0) > 0 and (gc or 0) > 0 and bc == 0 and (bg or 0) > 0
          and cb == 0 and (ct or 0) > 0,
          "torsione su perc_geom %s, campo B su perc_chi %s; chi_basc -> perc_geom %s volte e "
          "perc_chi %s; carica == doppia copertura in %s passi su %s"
          % (gg, gc, bg, bc, (ct or 0) - (cb or 0), ct))

    # --------------------------------------------------------------- Z4a (IL DECISIVO)
    oC1 = out["C1_scalamin"]
    vi = num(oC1, "SM", "viol_id")
    vg = num(oC1, "SM", "viol_giu")
    mg = num(oC1, "SMGIU", "max_giu", float)
    segna("Z4a", vi == 0 and vg == 0 and (mg is None or mg <= 0.0),
          "IL VINCOLO NON CREA MOVIMENTO: incrementi >= 0 toccati %s volte (0); max(dx_eff) "
          "sulle DISCESE = %s (<= 0: non spinge mai verso l'alto); discese APPROFONDITE %s (0)"
          % (vi, mg, vg))

    # ------------------------------------------------------------------ Z4b/c/d
    lam = float(re.search(r"^LAM (\S+)", oC1, re.M).group(1))
    md = num(oC1, "MIN", "d", float)
    md0 = num(oC1, "MIN", "d0", float)
    pat = num(oC1, "SM", "patol")
    pav = num(oC1, "SM", "pav_saltati")
    segna("Z4b", md >= lam and md0 >= lam,
          "min(d) = %.9f, min(d0) = %.9f, LAM = %.9f" % (md, md0, lam))
    stz = num(oC1, "STRESS", "max", str)
    segna("Z4c", stz != "inf", "stress |d-d0|/d0 massimo: %s" % stz)
    segna("Z4d", True,
          "[SI RIPORTA SEMPRE] casi patologici dx <= -x: %s; pavimenti vecchi SALTATI: %s"
          % (pat, pav))
    if pat:
        print("      ⚠ _g_sm_patol NON e' zero: su quelle scritture la proprieta' (3) non vale,")
        print("        e Z4b va letto INSIEME a questo numero. Riportato, non tappato.")

    # ------------------------------------------------------------------ Z5
    oC2 = out["C2_coesadim"]
    tet = num(oC2, "COES", "tetto", float)
    mx = num(oC2, "COES", "max", float)
    sat = num(oC2, "COES", "satura")
    arc = num(oC2, "COES", "archi")
    segna("Z5", mx is not None and tet is not None and mx <= tet * (1 + 1e-12),
          "|delta d0| massimo %.6e  <=  passo_causale %.6e   (saturi: %s su %s = %.2f%%)"
          % (mx, tet, sat, arc, 100.0 * sat / max(arc, 1)))

    # ------------------------------------------------------------------ Z6
    male = num(oD, "LEN", "male", str)
    nan = re.search(r"NAN campi=(\S+)", oD)
    segna("Z6", male == "nessuno" and bool(nan) and nan.group(1) == "nessuno",
          "tutti accesi: array con lunghezza != n -> %s ; NaN/inf -> %s"
          % (male, nan.group(1) if nan else "?"))

    print("")
    print("  (informazione, non criterio) con tutti e tre accesi:")
    print("    min(d) = %s   min(d0) = %s   stress max = %s"
          % (num(oD, "MIN", "d", float), num(oD, "MIN", "d0", float),
             num(oD, "STRESS", "max", str)))
    print("    _g_sm_patol = %s   _g_sm_viol_id = %s   max(dx_eff sulle discese) = %s"
          % (num(oD, "SM", "patol"), num(oD, "SM", "viol_id"),
             num(oD, "SMGIU", "max_giu", float)))

    print("")
    n_pass = sum(1 for _, o in esiti if o)
    print("ESITO: %d/%d" % (n_pass, len(esiti)))
    print("")
    if n_pass == len(esiti):
        print("VERDETTO: i tre flag sono INERTI a default, ognuno FA QUALCOSA da solo, la scala")
        print("  minima NON CREA MOVIMENTO (nessun incremento non-negativo toccato), le lunghezze")
        print("  restano sopra LAM, la coesione non supera il passo causale, e tutti e tre accesi")
        print("  insieme non producono NaN. Il ramo D si puo' lanciare.")
    else:
        print("VERDETTO: IL SIGILLO NON PASSA. Il ramo D NON si lancia.")
    print("")
    print("⚠ LIMITI: UN seme, UNA scena, %d passi. In %d passi la coppia di SCHWINGER puo' non" % (PASSI, PASSI))
    print("  essere MAI scattata: la terza via di nascita puo' essere NON ESERCITATA.")
    print("⚠ E Z7 NON E' QUI: e' il sigillo interno della rigiocata, e si gira a parte.")
    return 0 if n_pass == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
