# -*- coding: utf-8 -*-
"""**SIGILLO di `PSI-FLASH`: la schermatura non si spegne piu' alla nascita.**

**I cinque bracci, e i criteri erano fissati nel task history PRIMA dei numeri** *(mandato del
guardiano, 2026-09-28)*:

| | braccio | passa se |
|---|---|---|
| **A** | **passi SENZA nascite**, scena PICCOLA, driver, 3 passi, seme 11 | ### **byte-identico** col blob PRE-CURA |
| **B** | al **passo di nascita**, scena GRANDE: `lambda` degli archi | ### **resta nell'intervallo dei passi normali, NON `0.8`** |
| **C** | al **passo di nascita**: `mean(phi_g)` | ### **resta vicino alla base**, non a `366` |
| **D** | ### **IL CASO CHE DEVE FALLIRE** | sul blob **PRE-CURA** `lambda = 0.8` ### **SI DEVE VEDERE** |
| **E** | i due ripieghi | `len(psi) < n` ### **non scatta mai**; il contatore della **ricorsione** si RIPORTA, **stesso numero** prima e dopo nei passi senza nascite |

**E un'IPOTESI da verificare, non da assumere** *(decisione ④ di Luca)*: i passi **sotto** la base
sono il passo **DOPO** un flash, con la schermatura che riparte su una densita' gonfiata.
### **Dopo la cura il flash non c'e' piu', quindi il sotto-base NON DEVE PIU' ESSERCI:** se ci fosse
ancora, l'ipotesi **cade** e il sotto-base ha un'altra causa.

### ⚠ E DISTINGUE I DUE RIPIEGHI, che la sonda precedente contava INSIEME
`csv/_test_fork/_lambda_al_flash.py` aveva **un solo campo** per `not hasattr` e `len(psi) < n`, e
**quella fusione mi ha fatto attribuire al ramo sbagliato l'occorrenza del passo 1** *(correzione in
`e3fda4b`)*. **Qui i contatori del simulatore li separano per costruzione:** `_g_scherm_init`,
`_g_scherm_ricorsione`, e l'eccezione `SchermaturaSpenta` per il terzo caso.

**COMANDO:**
```
python csv/_seal_fork/_sig_nascita_psi.py [--passi=46]
```
**USCITA:** `0` se tutti i bracci passano, `1` altrimenti.
"""
import hashlib
import io
import json
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)
import numpy as np  # noqa: E402
import _cli_flag  # noqa: E402
import _passo  # noqa: E402

SIM = os.path.join(RADICE, "soliton_simulator.py")
BLOB = hashlib.sha1(io.open(SIM, "rb").read()).hexdigest()
FUORI = os.path.join(_QUI, "_sig_nascita_psi")
# IL NOME CHE LA CURA INTRODUCE: da qui `sim_prima_del_flag` RISALE al commit e prende il PADRE.
# NESSUN COMMIT PINNATO A MANO (`H-P8`).
ANCORA_CURA = "_eredita_psi_figli"
PRECURA = os.path.join(FUORI, "_sim_prima_della_cura.py")
PROVA = os.path.join(RADICE, "csv", "_test_fork", "_hashseed_prova.py")


def _t(x):
    return x if isinstance(x, str) else x.decode("utf-8", "replace")


def corri_grande(sim, passi):
    """Gira la scena GRANDE e misura, per passo: `lambda` degli archi, `mean(phi_g)`, i contatori.

    **La scena si prende DA `a`**, come fa il pilota: `nmasse` e `sep` scritti a mano sono
    l'errore che ha fatto misurare tutto sulla scena piccola.
    """
    import contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                            dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome="sim_sig_psi", sim=sim)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
        net = S.net
    LAM = float(getattr(S, "LAM"))
    ECC = getattr(S, "SchermaturaSpenta", None)
    stato = {"passo": 0, "lam": {}}
    _lam = net._lam_archi

    def lam_spiato():
        v = _lam()
        arr = np.atleast_1d(np.asarray(v, float))
        stato["lam"].setdefault(stato["passo"], []).append(
            {"media": float(arr.mean()), "min": float(arr.min()), "max": float(arr.max()),
             "tutti_LAM": bool(np.all(np.abs(arr - LAM) < 1e-12))})
        return v
    net._lam_archi = lam_spiato

    serie, nascita, fermato = {}, None, None
    for k in range(1, passi + 1):
        stato["passo"] = k
        n_prima = int(net.n)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                _passo.passo_pieno(S, net)
                _I = (np.abs(net.psi[:net.n]) ** 2 if hasattr(net, "psi")
                      and len(net.psi) >= net.n else np.zeros(int(net.n)))
                _g = net.pozzo_grafo(_I)[0]
        except Exception as e:
            fermato = {"passo": k, "tipo": type(e).__name__, "messaggio": _t(str(e))[:400],
                       "e_schermatura": bool(ECC is not None and isinstance(e, ECC))}
            break
        serie[k] = {"n": int(net.n), "mean_phi_g": float(np.mean(np.abs(_g))),
                    "nati": int(net.n) - n_prima}
        if nascita is None and int(net.n) > n_prima:
            nascita = k
        pass
    net._lam_archi = _lam
    return {"LAM": LAM, "serie": serie, "lam": stato["lam"], "nascita": nascita,
            "fermato": fermato, "n0": int(net.n),
            "g_scherm_init": int(getattr(net, "_g_scherm_init", 0)),
            "g_scherm_ricorsione": int(getattr(net, "_g_scherm_ricorsione", 0)),
            "g_eredpsi_tot": int(getattr(net, "_g_eredpsi_tot", 0)),
            "g_eredpsi_salti": int(getattr(net, "_g_eredpsi_salti", 0)),
            "nmasse": S._NMASSE_VIDEO["n"], "sep": S._NMASSE_VIDEO["sep"]}


def _intervallo_normali(r):
    """L'intervallo di `lambda` nei passi SENZA nascite, escluse le chiamate a `LAM`."""
    q = [v["media"] for k, lst in r["lam"].items() for v in lst
         if not v["tutti_LAM"] and r["serie"].get(k, {}).get("nati", 0) == 0]
    return (min(q), max(q)) if q else (None, None)


def principale():
    passi = 72
    for x in sys.argv[1:]:
        if x.startswith("--passi="):
            passi = int(x.split("=", 1)[1])
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    esiti, REF = {}, {}
    print("simulatore blob sha1-BYTE %s" % BLOB[:8])
    introduce = _cli_flag.sim_prima_del_flag(ANCORA_CURA, PRECURA)
    B_PRE = hashlib.sha1(io.open(PRECURA, "rb").read()).hexdigest()
    print("`%s` introdotto da %s; il PADRE e' il blob PRE-CURA %s"
          % (ANCORA_CURA, introduce[:8], B_PRE[:8]))
    if B_PRE == BLOB:
        raise SystemExit("[ANCORA] i due blob COINCIDONO: non c'e' niente da confrontare")
    print("")

    # ============ BRACCIO A: passi SENZA nascite, scena PICCOLA, byte-identico ============
    print("=" * 92)
    print("BRACCIO A -- PASSI SENZA NASCITE: byte-identico col blob PRE-CURA")
    print("=" * 92)
    A = os.path.join(FUORI, "PRIMA.npz")
    B = os.path.join(FUORI, "DOPO.npz")
    # il blob PRE-CURA si mette DOVE IL SIMULATORE STA, in una copia accanto: `_hashseed_prova`
    # carica dal disco. Si passa da un sotto-processo con `--sim`, che lo strumento NON ha:
    # allora si confrontano DUE dump prodotti dallo stesso strumento su DUE alberi -- e l'unico
    # modo onesto senza toccare il file vero e' `git stash`-free: si usa `git worktree`.
    lav = os.path.join(FUORI, "_albero_precura")
    if not os.path.isdir(lav):
        p = subprocess.run(["git", "worktree", "add", "--detach", lav, introduce + "^"],
                           cwd=RADICE, capture_output=True)
        print("  git worktree add -> %s" % ("ok" if p.returncode == 0 else _t(p.stderr)[:200]))
    p1 = subprocess.run([sys.executable, os.path.join(lav, "csv", "_test_fork",
                                                      "_hashseed_prova.py"),
                         "--out=" + A, "--seme=11", "--passi=3"],
                        cwd=lav, capture_output=True)
    p2 = subprocess.run([sys.executable, PROVA, "--out=" + B, "--seme=11", "--passi=3"],
                        cwd=RADICE, capture_output=True)
    p3 = subprocess.run([sys.executable, PROVA, "--confronta", A, B],
                        cwd=RADICE, capture_output=True)
    testo_a = _t(p3.stdout) + _t(p3.stderr)
    for r in testo_a.split(chr(10)):
        if "IDENTIC" in r.upper() or "DIVERS" in r.upper():
            print("  " + r.strip()[:150])
    esiti["A"] = (p1.returncode == 0 and p2.returncode == 0 and p3.returncode == 0
                  and "IDENTIC" in testo_a.upper())
    REF["A"] = {"ritorni": [p1.returncode, p2.returncode, p3.returncode], "passa": esiti["A"]}
    print("  BRACCIO A: %s" % ("PASSA" if esiti["A"] else "FALLISCE"))
    print("")

    # ============ i due giri sulla scena GRANDE ==========================================
    print("=" * 92)
    print("SCENA GRANDE: il blob PRE-CURA e quello CURATO, fino a due passi dopo la nascita")
    print("=" * 92)
    pre = corri_grande(PRECURA, passi)
    dopo = corri_grande(None, passi)
    for nome, r in (("PRE-CURA", pre), ("CURATO", dopo)):
        print("  %-9s nascita al passo %s   fermato: %s   ric.=%d  init=%d  ered.=%d(salti %d)"
              % (nome, r["nascita"], (r["fermato"] or {}).get("tipo", "-"),
                 r["g_scherm_ricorsione"], r["g_scherm_init"],
                 r["g_eredpsi_tot"], r["g_eredpsi_salti"]))
    REF["pre"], REF["dopo"] = pre, dopo
    print("")

    # ============ BRACCIO D: il caso che DEVE fallire ====================================
    print("=" * 92)
    print("BRACCIO D -- IL CASO CHE DEVE FALLIRE: sul PRE-CURA `lambda = 0.8` al passo di nascita")
    print("=" * 92)
    kn_pre = pre["nascita"]
    lam_pre = pre["lam"].get(kn_pre, [])
    d_ok = any(v["tutti_LAM"] for v in lam_pre)
    lo_p, hi_p = _intervallo_normali(pre)
    print("  passo di nascita PRE-CURA: %s   chiamate con lam = LAM: %d su %d"
          % (kn_pre, sum(1 for v in lam_pre if v["tutti_LAM"]), len(lam_pre)))
    print("  lambda nei passi normali PRE-CURA: %s - %s   (LAM = %.6f)"
          % (("%.6f" % lo_p) if lo_p else "?", ("%.6f" % hi_p) if hi_p else "?", pre["LAM"]))
    print("  mean(phi_g) al passo di nascita PRE-CURA: %.4f"
          % pre["serie"].get(kn_pre, {}).get("mean_phi_g", float("nan")))
    esiti["D"] = bool(d_ok)
    REF["D"] = {"passa": bool(d_ok)}
    print("  BRACCIO D: %s" % ("PASSA -- il difetto si vede" if d_ok else "FALLISCE"))
    print("")

    # ============ BRACCIO B e C: dopo la cura ============================================
    print("=" * 92)
    print("BRACCIO B e C -- dopo la cura: `lambda` normale e `mean(phi_g)` vicino alla base")
    print("=" * 92)
    kn = dopo["nascita"]
    lam_n = dopo["lam"].get(kn, [])
    # le chiamate a LAM restano SOLO per la ricorsione: quelle NON ricorsive non devono esserci
    lo, hi = _intervallo_normali(dopo)
    fuori_int = [v["media"] for v in lam_n if not v["tutti_LAM"]
                 and lo is not None and not (lo * 0.99 <= v["media"] <= hi * 1.01)]
    base = None
    q = [v["mean_phi_g"] for k, v in dopo["serie"].items() if v["nati"] == 0 and k >= 4]
    if q:
        base = sum(q) / len(q)
    phi_n = dopo["serie"].get(kn, {}).get("mean_phi_g")
    print("  passo di nascita CURATO: %s   chiamate: %d, di cui a LAM: %d"
          % (kn, len(lam_n), sum(1 for v in lam_n if v["tutti_LAM"])))
    print("  lambda nei passi normali CURATO: %s - %s"
          % (("%.6f" % lo) if lo else "?", ("%.6f" % hi) if hi else "?"))
    print("  chiamate NON ricorsive al passo di nascita FUORI dall'intervallo: %d %s"
          % (len(fuori_int), fuori_int[:4]))
    esiti["B"] = (len(fuori_int) == 0) and lo is not None
    print("  BRACCIO B: %s" % ("PASSA" if esiti["B"] else "FALLISCE"))
    if base and phi_n:
        print("  mean(phi_g): base %.4f   al passo di nascita %.4f   ->  %.4f x la base"
              % (base, phi_n, phi_n / base))
        esiti["C"] = abs(phi_n / base - 1.0) < 0.10
    else:
        esiti["C"] = False
    print("  BRACCIO C: %s  (criterio: entro il 10 %% dalla base)"
          % ("PASSA" if esiti["C"] else "FALLISCE"))
    REF["B"] = {"lam_normali": [lo, hi], "fuori_intervallo": fuori_int, "passa": esiti["B"]}
    REF["C"] = {"base": base, "al_passo_di_nascita": phi_n,
                "rapporto": (phi_n / base) if (base and phi_n) else None, "passa": esiti["C"]}
    print("")

    # ============ BRACCIO E: i due ripieghi =============================================
    print("=" * 92)
    print("BRACCIO E -- `len(psi) < n` non scatta mai; il contatore della ricorsione si RIPORTA")
    print("=" * 92)
    mai = dopo["fermato"] is None or not dopo["fermato"].get("e_schermatura")
    print("  la cura si e' fermata per `SchermaturaSpenta`? %s"
          % ("NO" if mai else "SI -- e allora la cura non tiene"))
    # lo STESSO numero di ricorsioni nei passi SENZA nascite: si contano le chiamate a LAM nei
    # passi con `nati == 0`, prima e dopo
    def _ric_senza_nascite(r):
        return sum(1 for k, lst in r["lam"].items() for v in lst
                   if v["tutti_LAM"] and r["serie"].get(k, {}).get("nati", 0) == 0)
    rp, rd = _ric_senza_nascite(pre), _ric_senza_nascite(dopo)
    print("  chiamate a LAM nei passi SENZA nascite:  PRE %d   DOPO %d   ->  %s"
          % (rp, rd, "STESSO NUMERO" if rp == rd else "DIVERSO"))
    esiti["E"] = bool(mai and rp == rd)
    REF["E"] = {"mai_fermato": bool(mai), "ricorsioni_senza_nascite_pre": rp,
                "ricorsioni_senza_nascite_dopo": rd, "passa": esiti["E"]}
    print("  BRACCIO E: %s" % ("PASSA" if esiti["E"] else "FALLISCE"))
    print("")

    # ============ L'IPOTESI ④, da verificare e non da assumere ===========================
    print("=" * 92)
    print("IPOTESI 4 -- il passo DOPO la nascita era SOTTO la base. Dopo la cura c'e' ancora?")
    print("=" * 92)
    ip = {}
    for nome, r in (("PRE-CURA", pre), ("CURATO", dopo)):
        kk = r["nascita"]
        b = [v["mean_phi_g"] for k, v in r["serie"].items() if v["nati"] == 0 and k >= 4]
        bb = (sum(b) / len(b)) if b else None
        dopo_n = r["serie"].get((kk or 0) + 1, {}).get("mean_phi_g")
        ip[nome] = {"base": bb, "passo_dopo": dopo_n,
                    "rapporto": (dopo_n / bb) if (bb and dopo_n) else None}
        print("  %-9s base %s   passo dopo la nascita %s   ->  %s"
              % (nome, ("%.4f" % bb) if bb else "?", ("%.4f" % dopo_n) if dopo_n else "?",
                 ("%.4f x" % (dopo_n / bb)) if (bb and dopo_n) else "?"))
    REF["ipotesi4"] = ip
    print("  ### SI RIPORTA, NON E' UN CRITERIO: se il sotto-base resta anche dopo la cura,")
    print("  ### l'ipotesi CADE e il sotto-base ha un'altra causa.")
    print("")

    # ============ BRACCIO F: IL PASSO DOPO OGNI NASCITA, entro il 5 % dalla base =========
    print("=" * 92)
    print("BRACCIO F -- IL PASSO DOPO OGNI NASCITA: entro il 5 % dalla base (CRITERIO)")
    print("=" * 92)
    print("  ⚠ E' IL BRACCIO CHE MANCAVA: il primo sigillo guardava SOLO il passo di")
    print("    nascita, ed e' passato lasciando un gradino del +11 % al passo DOPO --")
    print("    visibile nei suoi stessi numeri. Ora il passo dopo E' UN CRITERIO.")
    print("")
    F = {}
    for nome, r in (("PRE-CURA", pre), ("CURATO", dopo)):
        b = [v["mean_phi_g"] for k, v in r["serie"].items() if v["nati"] == 0 and k >= 4]
        bb = (sum(b) / len(b)) if b else None
        nasc = sorted(k for k, v in r["serie"].items() if v["nati"] > 0)
        peggio, dove = 0.0, None
        righe = []
        for kn in nasc:
            vd = r["serie"].get(kn + 1)
            if not vd or not bb:
                continue
            sc = abs(vd["mean_phi_g"] / bb - 1.0)
            righe.append((kn + 1, vd["mean_phi_g"], vd["mean_phi_g"] / bb))
            if sc > peggio:
                peggio, dove = sc, kn + 1
        F[nome] = {"base": bb, "nascite": nasc, "peggio_scostamento": peggio,
                   "peggio_al_passo": dove,
                   "righe": [{"passo": a, "mean_phi_g": c, "su_base": d}
                             for a, c, d in righe]}
        print("  %-9s base %s   nascite ai passi %s" % (nome, ("%.4f" % bb) if bb else "?",
                                                       nasc[:14]))
        for a, c, d in righe[:14]:
            print("      passo %-4d dopo una nascita: %10.4f  ->  %.4f x la base%s"
                  % (a, c, d, "   <== FUORI dal 5 %" if abs(d - 1.0) > 0.05 else ""))
        print("      ### scostamento PEGGIORE: %.4f (%.2f %%) al passo %s"
              % (peggio, 100.0 * peggio, dove))
        print("")
    esiti["F"] = bool(F["CURATO"]["peggio_scostamento"] <= 0.05)
    REF["F"] = F
    print("  BRACCIO F: %s" % ("PASSA" if esiti["F"] else "FALLISCE"))
    print("  (sul PRE-CURA lo scostamento peggiore e' %.2f %%: il difetto SI DEVE vedere)"
          % (100.0 * F["PRE-CURA"]["peggio_scostamento"]))
    print("")

    print("=" * 92)
    for k in ("A", "B", "C", "D", "E", "F"):
        print("  braccio %s: %s" % (k, "PASSA" if esiti.get(k) else "FALLISCE"))
    passa = all(esiti.get(k) for k in ("A", "B", "C", "D", "E", "F"))
    print("=" * 92)
    print("### SIGILLO `PSI-FLASH`: %s" % ("PASSA" if passa else "FALLISCE"))
    print("=" * 92)
    OUT = os.path.join(_QUI, "_sig_nascita_psi.json")
    io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(json.dumps(
        {"blob_sim": BLOB, "blob_pre_cura": B_PRE, "commit_che_introduce": introduce,
         "ancora_cura": ANCORA_CURA, "bracci": REF, "esiti": esiti, "passa": passa},
        indent=1, ensure_ascii=False, sort_keys=True, default=float))
    print("")
    print("scritto: " + OUT)
    return 0 if passa else 1


if __name__ == "__main__":
    sys.exit(principale())
