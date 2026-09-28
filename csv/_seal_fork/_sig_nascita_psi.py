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
| **E** | i due ripieghi | `len(psi) < n` ### **non scatta mai**; le ricorsioni ### **PER PASSO** sono uguali nei due giri **nei passi PRIMA della prima nascita** *(lo stesso dominio)*. **Il totale si RIPORTA, non si confronta** |
| **F** | ### **NESSUN SALTO** | in tutta la corsa `|phi_g(k)/phi_g(k-1) - 1|` ### **non supera il massimo misurato nei passi PRIMA della prima nascita** della stessa corsa. **Sul PRE-CURA deve FALLIRE** |

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
    # ⚠⚠ IL BRACCIO E, RISCRITTO **PER PASSO** (decisione di Luca, 2026-09-28). La prima stesura
    #   sommava le chiamate a LAM sui passi SENZA nascite e confrontava i due totali: 421 contro
    #   449. ### Ma i due giri hanno nascite in PASSI DIVERSI, quindi <<i passi senza nascite>> sono
    #   DUE INSIEMI DIVERSI: sommava su DOMINI DIVERSI, e non misurava cio' che diceva.
    #   ### Ora si confronta PER PASSO, e SOLO nei passi PRIMA DELLA PRIMA NASCITA -- dove i due
    #   giri percorrono la STESSA traiettoria, quindi il confronto e' definito.
    #   **Il totale si RIPORTA, non si confronta.**
    def _ric_per_passo(r):
        q = {}
        for k, lst in r["lam"].items():
            q[k] = sum(1 for v in lst if v["tutti_LAM"])
        return q
    rp, rd = _ric_per_passo(pre), _ric_per_passo(dopo)
    k0 = min(pre["nascita"] or 10 ** 9, dopo["nascita"] or 10 ** 9)
    comuni = sorted(k for k in set(rp) & set(rd) if k < k0)
    diversi = [(k, rp[k], rd[k]) for k in comuni if rp[k] != rd[k]]
    print("  passi PRIMA della prima nascita (dominio comune): %d, dal %s al %s"
          % (len(comuni), comuni[0] if comuni else "?", comuni[-1] if comuni else "?"))
    _campione = sorted({rp[k] for k in comuni})
    print("  chiamate a LAM per passo, PRE: %s   DOPO: %s"
          % (_campione, sorted({rd[k] for k in comuni})))
    print("  passi in cui i due giri DIFFERISCONO: %d %s" % (len(diversi), diversi[:6]))
    print("  ### E IL TOTALE SI RIPORTA, NON SI CONFRONTA: PRE %d, DOPO %d -- i domini sono"
          % (sum(rp.values()), sum(rd.values())))
    print("      diversi appena le traiettorie divergono, e confrontarli sarebbe l'errore di prima.")
    esiti["E"] = bool(mai and not diversi and comuni)
    REF["E"] = {"mai_fermato": bool(mai), "passi_comuni": comuni,
                "per_passo_pre": {str(k): rp[k] for k in comuni},
                "per_passo_dopo": {str(k): rd[k] for k in comuni},
                "differenti": diversi, "totale_pre": sum(rp.values()),
                "totale_dopo": sum(rd.values()), "passa": esiti["E"]}
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

    # ============ BRACCIO F: **NESSUN SALTO** ==============================================
    print("=" * 92)
    print("BRACCIO F -- NESSUN SALTO: nessun passo salta piu' dell'oscillazione NATURALE")
    print("=" * 92)
    print("  ⚠⚠ RISCRITTO (decisione di Luca, 2026-09-28). La prima stesura misurava lo")
    print("     scostamento dalla BASE, cioe' da una MEDIA GLOBALE -- e la serie DERIVA, quindi")
    print("     quello misurava anche la deriva: il 10.48 % che faceva fallire il braccio ERA LA")
    print("     DERIVA, non un gradino. Ora si misura IL SALTO FRA DUE PASSI CONSECUTIVI, e il")
    print("     metro e' l'oscillazione naturale della STESSA corsa, PRIMA di ogni nascita.")
    print("")
    F = {}
    for nome, r in (("PRE-CURA", pre), ("CURATO", dopo)):
        ks = sorted(r["serie"])
        salti = []
        for i in range(1, len(ks)):
            a, b = r["serie"][ks[i - 1]]["mean_phi_g"], r["serie"][ks[i]]["mean_phi_g"]
            if a:
                salti.append((ks[i], abs(b / a - 1.0)))
        kn = r["nascita"] or (ks[-1] + 1)
        prima = [(k, s) for k, s in salti if k < kn]
        poi = [(k, s) for k, s in salti if k >= kn]
        mp = max((s for _k, s in prima), default=0.0)
        kmp = max(prima, key=lambda x: x[1])[0] if prima else None
        mq = max((s for _k, s in poi), default=0.0)
        kmq = max(poi, key=lambda x: x[1])[0] if poi else None
        F[nome] = {"nascita": r["nascita"], "max_prima": mp, "al_passo_prima": kmp,
                   "max_dopo": mq, "al_passo_dopo": kmq,
                   "supera": bool(mq > mp),
                   "peggiori": [{"passo": k, "salto": s}
                                for k, s in sorted(poi, key=lambda x: -x[1])[:5]]}
        print("  %-9s prima nascita al passo %s" % (nome, r["nascita"]))
        print("      oscillazione NATURALE (prima della nascita): max %.4f %% al passo %s"
              % (100.0 * mp, kmp))
        print("      salto MASSIMO dal passo di nascita in poi: %.4f %% al passo %s"
              % (100.0 * mq, kmq))
        for v in F[nome]["peggiori"][:4]:
            print("        passo %-4d salto %8.4f %%%s"
                  % (v["passo"], 100.0 * v["salto"],
                     "   <== SUPERA l'oscillazione naturale" if v["salto"] > mp else ""))
        print("")
    esiti["F"] = bool(not F["CURATO"]["supera"])
    REF["F"] = F
    print("  BRACCIO F: %s" % ("PASSA -- nessun salto oltre l'oscillazione naturale"
                               if esiti["F"] else "FALLISCE"))
    print("  E IL CASO CHE DEVE FALLIRE: sul PRE-CURA il salto massimo e' %.2f %% contro un'"
          % (100.0 * F["PRE-CURA"]["max_dopo"]))
    print("  oscillazione naturale di %.2f %%  ->  %s"
          % (100.0 * F["PRE-CURA"]["max_prima"],
             "SUPERA, e il difetto si vede" if F["PRE-CURA"]["supera"] else "NON SUPERA"))
    esiti["F"] = bool(esiti["F"] and F["PRE-CURA"]["supera"])
    print("")

    # ============ SI RIPORTA, NON E' UN CRITERIO ==========================================
    print("=" * 92)
    print("SI RIPORTA, NON E' UN CRITERIO: le nascite e la traiettoria dopo il 42")
    print("=" * 92)
    print("  ### La cura CAMBIA LA DINAMICA, ed e' ATTESO: `psi` non viene piu' gonfiata, quindi")
    print("  ### le decisioni di mitosi a valle cambiano. Confrontare il passo k di un giro col")
    print("  ### passo k dell'altro, dopo la prima nascita, NON confronta la stessa cosa.")
    RIP = {}
    for nome, r in (("PRE-CURA", pre), ("CURATO", dopo)):
        nasc = sorted(k for k, v in r["serie"].items() if v["nati"] > 0)
        tot = sum(v["nati"] for v in r["serie"].values())
        RIP[nome] = {"passi_con_nascite": nasc, "nati_totali": tot,
                     "n_finale": max(v["n"] for v in r["serie"].values()) if r["serie"] else None}
        print("  %-9s nascite ai passi %s" % (nome, nasc[:14]))
        print("            nati in tutto %d, n finale %s" % (tot, RIP[nome]["n_finale"]))
    REF["riportati"] = RIP
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
