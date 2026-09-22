# -*- coding: utf-8 -*-
"""TRE MISURE: `phi` contro l'azimut dello spinore, I TRE TEMPI, e CHI LEGGE COSA.

Mandato di Luca, 2026-09-22 sera. **SOLA LETTURA: snapshot gia' scritti e sorgente. Nessun run.**

① `phi` CONTRO L'AZIMUT DELLO SPINORE.
  Il docstring di `_passo_spinoriale` dice: *«ogni nodo e' uno spinore, rappresentato dal
  vettore di Bloch `n_i(phi, phi_s)`»*. **Si verifica invece di crederci.**
  L'azimut del Bloch e' `atan2(nb_y, nb_x)`. Se `phi` E' quell'azimut, allora
  `delta = wrap2pi(azimut - phi)` dev'essere **una costante**.
  **LA STATISTICA GIUSTA E' CIRCOLARE, non lineare:** `R = |media(exp(i*delta))|`.
      `R = 1`  -> `delta` costante: `phi` E' l'azimut (a meno di una costante)
      `R = 0`  -> `delta` uniforme: nessuna relazione
  ⚠ **IL NULLO NON E' ZERO:** per `N` angoli UNIFORMI `E[R] ~ sqrt(pi/(4N))`. Con `N ~ 2900`
    vale **`~0.0165`**. **Si stampa accanto**, senno' un `R = 0.02` sembrerebbe un effetto.
  I CRITERI, SCRITTI PRIMA:
      `R >= 0.90`            -> COINCIDONO (a meno di una costante)
      `R <= 5 * nullo`       -> NESSUNA RELAZIONE
      in mezzo               -> RELAZIONE PARZIALE, e si scrive cosi'
  E LA TERZA DOMANDA DI LUCA: **`R` cala nel tempo?** Si riporta snapshot per snapshot.
  ⚠ Si confronta anche con **`phi_s`**, che e' l'ALTRO angolo dichiarato dello spinore:
    se `phi_s` fosse l'azimut e `phi` no, il docstring avrebbe i due scambiati.

② I TRE TEMPI, sugli stessi nodi e archi.
      `r`       = `_r_corrente`, per NODO       -> `dt_n = DT*r`, il tic dei processi locali
      `tau_pp`  = `1 + |tw|/PHI_CRIT`, per ARCO -> mitosi, repulsione, memoria `_rep`
      `d/cs`    = per ARCO                      -> il tempo-luce, lo Strato 1
  **`:1319` DICHIARA GIA' CHE SONO SCOLLEGATI**, e ne nomina DUE. **Con `tau_pp` sono TRE.**
  Per confrontarli sugli STESSI oggetti si proietta sugli ARCHI: `r_arco = 0.5*(r_i + r_j)`.
  ⚠ E SI RIPORTA IL NULLO DELLA CORRELAZIONE: `~1/sqrt(N)`.

③ CHI LEGGE COSA, dall'AST: per ogni funzione, quale dei tre tempi usa.

⚠ NESSUNA UNIFICAZIONE, NESSUNA PROPOSTA: si misura, si registra, e decide Luca al `CHK3`.
ASCII PURO.
"""
import ast
import gzip
import hashlib
import io
import os
import pickle
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SORGENTE = os.path.join(RADICE, "soliton_simulator.py")
OUT = os.path.join(_QUI, "_diag_D", "TRE_TEMPI.md")
PASSI = (120, 240, 360, 480, 600)
BRACCI = [("ACCESO", "_g4_riferimento"), ("SOLO-SCRITTURA", "_g4_senza_memmoto"),
          ("INTERO-BLOCCO", "_g4bis_senza_blocco")]
PHI_CRIT = 2 * np.pi


def leggi(cart, passo):
    p = os.path.join(RADICE, "csv", "_test_fork", cart, "scena_%06d.pkl.gz" % passo)
    if not os.path.exists(p):
        return None
    with gzip.open(p, "rb") as f:
        return pickle.load(f)["attrs"]


def w2(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def concentrazione(delta):
    """`R = |media(exp(i*delta))|`. `1` = costante, `0` = uniforme."""
    if not len(delta):
        return float("nan")
    return float(np.abs(np.mean(np.exp(1j * np.asarray(delta, float)))))


def nullo_R(n):
    """Il valore di `R` sotto IPOTESI NULLA (angoli uniformi): `~sqrt(pi/(4N))`."""
    return float(np.sqrt(np.pi / (4.0 * max(n, 1))))


def collaudo(W):
    """`P1-sexies`: la statistica circolare su casi a risposta NOTA."""
    W("COLLAUDO (`P1-sexies`), PRIMA di misurare\n" + "-" * 96 + "\n")
    e = []
    rng = np.random.default_rng(20260922)
    n = 2900
    cost = np.full(n, 0.7)
    ok1 = abs(concentrazione(cost) - 1.0) < 1e-12
    W("K1 `delta` COSTANTE -> R = %.6f, atteso 1 -> %s\n"
      % (concentrazione(cost), "OK" if ok1 else "*** NO ***"))
    unif = rng.uniform(-np.pi, np.pi, n)
    R0, nl = concentrazione(unif), nullo_R(n)
    ok2 = R0 < 5 * nl
    W("K2 IL CASO CHE DEVE DARE «NIENTE»: `delta` UNIFORME -> R = %.4f, nullo = %.4f\n"
      % (R0, nl))
    W("     R sotto 5x il nullo -> %s\n"
      % ("OK: non inventa una relazione" if ok2 else "*** ne inventa una ***"))
    e += [ok1, ok2]
    # il nullo NON e' zero, e va stampato: un R di 0.02 su 2900 punti e' RUMORE
    ok3 = 0.010 < nl < 0.025
    W("K3 il NULLO su %d punti vale %.4f, NON zero -> %s\n"
      % (n, nl, "OK: si stampa accanto" if ok3 else "*** NO ***"))
    e.append(ok3)
    # una relazione DEBOLE ma vera dev'essere distinguibile dal nullo
    deb = w2(0.3 * rng.uniform(-np.pi, np.pi, n) + 0.5)
    Rd = concentrazione(deb)
    ok4 = Rd > 5 * nl and Rd < 0.90
    W("K4 relazione PARZIALE (rumore al 30%%) -> R = %.4f: sopra il nullo e sotto 0.90 -> %s\n"
      % (Rd, "OK: la terza casella esiste" if ok4 else "*** il criterio e' binario ***"))
    e.append(ok4)
    # e un `delta` costante MA con una costante diversa da zero DEVE dare R=1:
    # e' il punto del criterio ("a meno di una costante")
    ok5 = abs(concentrazione(np.full(n, 2.9)) - 1.0) < 1e-12
    W("K5 `delta` costante ma NON nulla (=2.9) -> R = 1: e' «a meno di una costante» -> %s\n"
      % ("OK" if ok5 else "*** NO ***"))
    e.append(ok5)
    ok = all(e)
    W("-" * 96 + "\n  -> %s\n\n" % ("i criteri PASSANO" if ok else "*** NON PASSANO ***"))
    return ok


def chi_legge_cosa(testo):
    """Dall'AST: per ogni funzione, quale dei tre tempi usa."""
    albero = ast.parse(testo)
    segni = {
        "r (dt_n)": ("dt_n", "_r_corrente", "r_loc", "ritmo"),
        "tau_pp": ("tau_pp", "tau_soglia", "tau_tetto", "tau_nodo", "tau_a", "tau_locale"),
        "d/cs (tempo-luce)": ("_tempo_luce_nodo", "cs_nodo", "_cs_nodo_prev", "tau_luce"),
    }
    out = []
    for fn in ast.walk(albero):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        usa = {}
        for nodo in ast.walk(fn):
            nome = None
            if isinstance(nodo, ast.Name):
                nome = nodo.id
            elif isinstance(nodo, ast.Attribute):
                nome = nodo.attr
            if nome is None:
                continue
            for etichetta, chiavi in segni.items():
                if nome in chiavi:
                    usa.setdefault(etichetta, set()).add(nome)
        if usa:
            out.append((fn.name, dict((k, sorted(v)) for k, v in usa.items())))
    return sorted(out)


def main():
    W = sys.stdout.write
    if not collaudo(W):
        return 1
    testo = io.open(SORGENTE, encoding="utf-8").read()
    blob = hashlib.sha1(open(SORGENTE, "rb").read()).hexdigest()[:8]
    try:
        os.makedirs(os.path.dirname(OUT))
    except OSError:
        pass
    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    Wf = o.write
    Wf("# `phi` CONTRO L'AZIMUT · I TRE TEMPI · CHI LEGGE COSA\n\n")
    Wf("> Generato da `csv/_test_fork/_tre_tempi.py`. **Blob `%s`.** **Nessun run:** 15 "
       "snapshot gia' scritti e il sorgente.\n\n" % blob)

    # ---------------------------------------------------------- 1
    Wf("## ① `phi` È L'AZIMUT DEL VETTORE DI BLOCH?\n\n")
    Wf("> Il docstring di `_passo_spinoriale` dice *«il vettore di Bloch `n_i(phi, phi_s)`»*.\n")
    Wf("> **`_passo_spinoriale` GIRA:** chiamato a `:4620`, con `SPINORE_VIVO = True`. "
       "*(Il suo docstring si dichiara «ORFANO»: e' STALE, e `CLAUDE.md` lo dice gia'.)*\n>\n")
    Wf("> **`R = |media(exp(i·Δ))|`** con `Δ = wrap(azimut − φ)`. **`R = 1`** → `φ` "
       "*è* l'azimut a meno di una costante · **`R = 0`** → nessuna relazione.\n")
    Wf("> **Il NULLO non è zero:** `√(π/4N)`, e sta nella tabella.\n\n")
    Wf("| braccio | passo | nodi | **`R` con `φ`** | **`R` con `phi_s`** | nullo | lettura |\n")
    Wf("|---|--:|--:|--:|--:|--:|---|\n")
    for eti, cart in BRACCI:
        for passo in PASSI:
            a = leggi(cart, passo)
            if a is None:
                continue
            nb = np.asarray(a["_nb"], float)
            phi = np.asarray(a["phi"], float)
            phs = np.asarray(a["phi_s"], float)
            n = min(len(nb), len(phi), len(phs))
            az = np.arctan2(nb[:n, 1], nb[:n, 0])
            Rp = concentrazione(w2(az - phi[:n]))
            Rs = concentrazione(w2(az - phs[:n]))
            nl = nullo_R(n)
            if Rp >= 0.90:
                let = "**COINCIDONO**"
            elif Rp <= 5 * nl:
                let = "**NESSUNA RELAZIONE**"
            else:
                let = "parziale"
            Wf("| %s | %d | %d | **%.4f** | %.4f | %.4f | %s |\n"
               % (eti, passo, n, Rp, Rs, nl, let))

    # ---------------------------------------------------------- 2
    Wf("\n## ② I TRE TEMPI, sugli stessi archi\n\n")
    Wf("> **`:1319` dichiara già che sono SCOLLEGATI**, e ne nomina **due** — *«il metrico "
       "`tau_p = d/cs` e l'orologio `dt_n = DT·r`»*. **Con `tau_pp` sono TRE.**\n")
    Wf("> `r` è per NODO: si proietta sugli archi con `r_arco = ½(r_i + r_j)`.\n")
    Wf("> **Il nullo della correlazione è `~1/√N`**, e sta nella tabella.\n\n")
    Wf("| braccio | passo | archi | `med r_arco` | `med tau_pp` | `med d/cs` | "
       "**corr(r,tau_pp)** | **corr(r,d/cs)** | **corr(tau_pp,d/cs)** | nullo |\n")
    Wf("|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|\n")
    for eti, cart in BRACCI:
        for passo in PASSI:
            a = leggi(cart, passo)
            if a is None:
                continue
            ii = np.asarray(a["i"]); jj = np.asarray(a["j"])
            rr = np.asarray(a.get("_r_corrente", []), float)
            cs = np.asarray(a.get("_cs_nodo_prev", []), float)
            d = np.asarray(a["d"], float)
            tw = np.abs(np.asarray(a["tw"], float))
            nn = min(len(rr), len(cs)) if len(rr) and len(cs) else 0
            if not nn:
                Wf("| %s | %d | — | | | | | | | `_r_corrente` o `_cs_nodo_prev` assente |\n"
                   % (eti, passo))
                continue
            m = (ii < nn) & (jj < nn)
            r_arc = 0.5 * (rr[ii[m]] + rr[jj[m]])
            cs_arc = np.minimum(cs[ii[m]], cs[jj[m]])          # il nodo PIU' LENTO
            dcs = d[m] / np.maximum(cs_arc, 1e-12)
            tpp = 1.0 + tw[m] / PHI_CRIT
            N = len(r_arc)

            def co(x, y):
                return (float(np.corrcoef(x, y)[0, 1])
                        if N > 2 and np.std(x) > 0 and np.std(y) > 0 else float("nan"))
            Wf("| %s | %d | %d | %.4f | %.4f | %.4f | **%+.4f** | **%+.4f** | **%+.4f** | "
               "`%.1e` |\n"
               % (eti, passo, N, float(np.median(r_arc)), float(np.median(tpp)),
                  float(np.median(dcs)), co(r_arc, tpp), co(r_arc, dcs), co(tpp, dcs),
                  1.0 / np.sqrt(N)))

    # ---------------------------------------------------------- 3
    Wf("\n## ③ CHI LEGGE COSA — dall'AST\n\n")
    tab = chi_legge_cosa(testo)
    Wf("**Funzioni che toccano almeno uno dei tre tempi: %d.**\n\n" % len(tab))
    Wf("| funzione | `r` / `dt_n` | `tau_pp` | `d/cs` |\n|---|---|---|---|\n")
    for nome, usa in tab:
        Wf("| `%s` | %s | %s | %s |\n"
           % (nome,
              ", ".join("`%s`" % x for x in usa.get("r (dt_n)", [])) or "—",
              ", ".join("`%s`" % x for x in usa.get("tau_pp", [])) or "—",
              ", ".join("`%s`" % x for x in usa.get("d/cs (tempo-luce)", [])) or "—"))
    solo = {}
    for _n, usa in tab:
        k = tuple(sorted(usa.keys()))
        solo[k] = solo.get(k, 0) + 1
    Wf("\n**Combinazioni:**\n\n| quali tempi | quante funzioni |\n|---|--:|\n")
    for k in sorted(solo, key=lambda z: -solo[z]):
        Wf("| %s | %d |\n" % (" + ".join("`%s`" % x for x in k), solo[k]))

    Wf("\n**LIMITI: UN seme, UNA scena, 15 snapshot. NESSUNA unificazione, nessuna proposta: "
       "si misura, si registra, e decide Luca al `CHK3`.**\n")
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
