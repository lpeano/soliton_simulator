# -*- coding: utf-8 -*-
"""IL CALCIO DELLA MITOSI SOTTO LO SCAMBIO `a<->b`, **ISOLATO**.

*(punto 2 del mandato di Luca del 2026-10-04. Task history:
`doc/TASK_HISTORY/2026-10-04_calcio-sotto-lo-scambio-isolato.md`, committato PRIMA.)*

### PERCHE' ESISTE: due buchi, e li DICHIARANO i referti stessi
| | il buco | dove e' scritto |
|---|---|---|
| **1** | `_verso_archi` gira su **1 passo**, e in quel passo le nascite sono **ZERO** | il suo referto: *<<il calcio della mitosi NON HA AGITO>>* |
| **2** | invertire **TUTTI** gli archi mescola `memoria_hebbiana_moto` con la mitosi | `_misure_calore`: quella voce ha `sum d_Q2 = +3.8423e+05` |

### ➜ **Quindi: si arriva al passo in cui la divisione AVVIENE, e si invertono SOLO gli
### archi che si dividono.**

### COME, e ogni riga e' una condizione di validita'
1. scena del **DRIVER**, `nmasse` e `sep` **dall'argv** *(mai a mano: e' `H-P3`, ed e' il
   difetto che ha fatto sigillare al `6b` una scena da `2208` nodi invece di `~12800`)*;
2. si avanza **un passo alla volta**, e dopo ciascuno si **SONDA** `decidi_divisione` su una
   copia **usa-e-getta**: il primo passo con candidati e' il punto di misura.
   ### **NON si assume il passo: si CERCA, e si stampa quello trovato accanto all'atteso.**
3. due copie profonde: **BASE**, e **SCAMBIO** dove per i **soli archi selezionati** si
   invertono `(i,j)` e si cambia **segno a `tw`**;
4. lo **stesso stato del generatore** in entrambe *(verificato, non assunto)*;
5. in entrambe si esegue **SOLO `mitosi()`**;
6. ### **si VERIFICA che le due abbiano selezionato gli STESSI archi.** Se no, il confronto
   sarebbe fra **due eventi diversi**: ### **lo strumento si FERMA.**
7. confronto con **rinumerazione**: i nodi per indice, ### **gli archi nuovi per INSIEME
   degli estremi** -- perche' sotto lo scambio i due archi nuovi si scambiano **ruolo e
   orientamento**, e accoppiarli per posizione misurerebbe **lo scambio fatto da me**.

### IL CONTROLLO CHE PUO' FALLIRE
Una **copia del sorgente** con `FRAZ_NASCITA = 0.4` *(e una con `0.3`)*. Li'
`pos_figlio = (1-t)*pos[a] + t*pos[b]` **non e' invariante**, e nemmeno
`fm = phi[a] - t*D`. ### **Lo strumento DEVE trovare entrambe. Se non le trova e' CIECO.**
### ⚠ **E la frazione si cambia su una COPIA del file, non con un flag: `FRAZ_NASCITA`
### NON E' UN FLAG per decisione di Luca** *(un flag renderebbe la legge un'opzione)*.

USO:
  python csv/_test_fork/_calcio_sotto_scambio.py
  python csv/_test_fork/_calcio_sotto_scambio.py --collaudo
  opzioni: --max-passi=N (default 80)

USCITA: `csv/_test_fork/_calcio_sotto_scambio/_calcio_sotto_scambio.json` + `_corsa.txt`.

# ESENTE-H-P3: la frazione del CONTROLLO si cambia su una COPIA DEL SORGENTE, non
#   assegnando un attributo al modulo caricato. `FRAZ_NASCITA` non e' un flag di CLI per
#   decisione di Luca del 2026-10-03, quindi non esiste una via dal CLI; la scena invece
#   passa TUTTA dal CLI (`nmasse` e `sep` da `argv`, mai scritti a mano).
"""
import contextlib
import copy
import hashlib
import io
import json
import os
import platform
import shutil
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

import _cli_flag   # noqa: E402
import _passo      # noqa: E402

NL = chr(10)
FUORI = os.path.join(RADICE, "csv", "_test_fork", "_calcio_sotto_scambio")
SIM = os.path.join(RADICE, "soliton_simulator.py")
PASSO_ATTESO_DIV = 42        # da `doc/FATTI_dal_codice.md`, voce `decidi_divisione`
PASSO_ATTESO_SCH = 70        # dal mandato
MAX_PASSI = 80

P = []


def stampa(s=""):
    print(s)
    P.append(s)


def riga(c="-"):
    stampa(c * 104)


def blob(percorso):
    return hashlib.sha1(io.open(percorso, "rb").read()).hexdigest()


# ------------------------------------------------------------------ la scena
def carica(nome, sim=None):
    """La scena del DRIVER. ### `nmasse` e `sep` vengono dall'ARGV, mai scritti a mano."""
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                              dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome=nome, sim=sim)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    return S, S.net, a


def un_passo(S, net):
    with contextlib.redirect_stdout(io.StringIO()):
        _passo.passo_pieno(S, net)


# --------------------------------------------------------------- lo scambio
def sonda_sel(net):
    """`sel` SENZA toccare la rete vera: `decidi_divisione` ESTRAE dal generatore."""
    q = copy.deepcopy(net)
    with contextlib.redirect_stdout(io.StringIO()):
        sel, _perche = q.decidi_divisione()
    return None if sel is None else np.asarray(sel).copy()


def scambia(net, sel):
    """`(i,j) -> (j,i)` e `tw -> -tw` **sui soli archi `sel`**, e nient'altro."""
    i = np.asarray(net.i).copy()
    j = np.asarray(net.j).copy()
    i[sel], j[sel] = j[sel].copy(), i[sel].copy()
    net.i, net.j = i, j
    tw = np.asarray(net.tw, float).copy()
    tw[sel] = -tw[sel]
    net.tw = tw
    return {"archi_invertiti": int(len(sel)),
            "grandezze_cambiate_di_segno": ["tw"]}


# ------------------------------------------------- le grandezze, per lunghezza
def vettori(net, n):
    """Gli attributi ndarray la cui PRIMA dimensione e' `n`. Li SCOPRE, non li elenca:
    un elenco a mano dimentica le grandezze nuove, ed e' il difetto che il
    `COMMIT 3` ha reso facile da fare (sei `_rn_*` nuovi in un colpo)."""
    fuori = {}
    for k in sorted(vars(net)):
        v = getattr(net, k, None)
        if isinstance(v, np.ndarray) and v.ndim >= 1 and v.shape[0] == n:
            fuori[k] = v
    return fuori


def stesso(x, y):
    """Uguaglianza fra ELEMENTI, non distanza.

    ### I due difetti che `_verso_archi` ha pagato il 2026-10-01, e non li rifaccio:
    `inf - inf` da' `NaN` *(che non e' mai `== 0`)*, quindi la distanza mente; e
    `NaN` contro `NaN` qui si dichiara **UGUALE**, perche' la domanda e'
    *<<e' lo stesso stato?>>* e non *<<quanto distano?>>*.
    """
    x = np.asarray(x)
    y = np.asarray(y)
    if x.shape != y.shape:
        return False, float("nan"), -1
    ug = (x == y) | (np.isnan(x) & np.isnan(y) if x.dtype.kind == "f" else False)
    diff = int(np.sum(~ug))
    if x.dtype.kind == "f":
        fin = np.isfinite(x) & np.isfinite(y)
        scarto = float(np.max(np.abs(x[fin] - y[fin]))) if np.any(fin) else 0.0
    else:
        scarto = float(diff)
    return diff == 0, scarto, diff


def confronta_nodi(A, B, indici, etichetta):
    """Tutte le grandezze PER NODO, ai soli `indici`."""
    fuori = []
    va, vb = vettori(A, A.n), vettori(B, B.n)
    for k in sorted(set(va) | set(vb)):
        if k not in va or k not in vb:
            fuori.append({"grandezza": k, "stato": "presente in uno solo",
                          "dove": etichetta})
            continue
        try:
            ok, scarto, nd = stesso(va[k][indici], vb[k][indici])
        except Exception as e:
            fuori.append({"grandezza": k, "stato": "non confrontabile: %r" % (e,),
                          "dove": etichetta})
            continue
        fuori.append({"grandezza": k, "dove": etichetta, "simmetrica": bool(ok),
                      "scarto_max": scarto, "elementi_diversi": nd})
    return fuori


def archi_nuovi(net, n0, archi0):
    """Gli archi nati in questo `mitosi`: indice >= `archi0`, con i loro estremi."""
    i = np.asarray(net.i)
    j = np.asarray(net.j)
    out = []
    for k in range(archi0, len(i)):
        out.append({"idx": k, "i": int(i[k]), "j": int(j[k]),
                    "estremi": frozenset((int(i[k]), int(j[k])))})
    return out


def accoppia(na, nb):
    """Accoppia gli archi nuovi per **INSIEME degli estremi**.

    ### ⛔ **E NON PER POSIZIONE, e il perche' e' il punto della misura:** la nascita
    scrive `i = [i[keep], a, m]` e `j = [j[keep], m, b]`, quindi i due archi nuovi sono
    `a-m` e `m-b`. ### **Sotto lo scambio diventano `b-m` e `m-a`: si scambiano RUOLO e
    ORIENTAMENTO.** Accoppiarli per posizione misurerebbe **lo scambio fatto da me**.
    """
    resta = list(nb)
    coppie, spaiati_a = [], []
    for x in na:
        trovato = None
        for y in resta:
            if y["estremi"] == x["estremi"]:
                trovato = y
                break
        if trovato is None:
            spaiati_a.append(x)
        else:
            resta.remove(trovato)
            coppie.append((x, trovato))
    return coppie, spaiati_a, resta


def confronta_archi(A, B, coppie):
    """Le grandezze PER ARCO sui nuovi, accoppiati per estremi."""
    fuori = []
    va, vb = vettori(A, len(np.asarray(A.i))), vettori(B, len(np.asarray(B.i)))
    ia = [x["idx"] for x, _ in coppie]
    ib = [y["idx"] for _, y in coppie]
    orient = [bool(x["i"] == y["i"]) for x, y in coppie]
    for k in sorted(set(va) | set(vb)):
        if k not in va or k not in vb:
            fuori.append({"grandezza": k, "stato": "presente in uno solo",
                          "dove": "archi nuovi"})
            continue
        try:
            ok, scarto, nd = stesso(va[k][ia], vb[k][ib])
        except Exception as e:
            fuori.append({"grandezza": k, "stato": "non confrontabile: %r" % (e,),
                          "dove": "archi nuovi"})
            continue
        fuori.append({"grandezza": k, "dove": "archi nuovi", "simmetrica": bool(ok),
                      "scarto_max": scarto, "elementi_diversi": nd})
    return fuori, orient


# ------------------------------------------------------------ l'attesa, dal conto
def attesa_calcio(S, net, sel, a, b):
    """`delta_phi` ATTESO sotto lo scambio, dal conto scritto nel task history:

        delta_phi(nodo nello slot a) = KICK_TW * sciolta * chi_a * mod

    ### E' un conto MIO, letto dal codice: se la misura dara' un numero diverso, prima di
    dire *<<il codice fa altro>>* va ricontrollato QUESTO.
    """
    tw = np.asarray(net.tw, float)[sel]
    sciolta = np.abs(tw) / S.PHI_CRIT
    tau = 1.0 + np.abs(tw) / S.PHI_CRIT
    mod = tau / (1.0 + tau)
    chi_a = np.asarray(net.perc_chi, float)[a]
    chi_b = np.asarray(net.perc_chi, float)[b]
    return {"sciolta": sciolta, "mod": mod, "chi_a": chi_a, "chi_b": chi_b,
            "delta_a": S.KICK_TW * sciolta * chi_a * mod,
            "delta_b": S.KICK_TW * sciolta * chi_b * mod}


# ------------------------------------------------------------------ la misura
def misura(S, net, a_cli, t_dichiarato, max_passi, voce):
    """Trova il primo passo con candidati, poi confronta BASE e SCAMBIO."""
    out = {"frazione": t_dichiarato, "n_iniziale": int(net.n),
           "archi_iniziali": int(len(np.asarray(net.i))),
           "nmasse": getattr(a_cli, "nmasse", None), "sep": getattr(a_cli, "sep", None)}
    stampa("  scena: nmasse=%s sep=%s  ->  n = %d, archi = %d"
           % (out["nmasse"], out["sep"], net.n, out["archi_iniziali"]))
    stampa("  FRAZ_NASCITA = %r   MITOSI_DIR = %r   ANTIFASE_ADD = %r   REGIME = %r"
           % (S.FRAZ_NASCITA, S.MITOSI_DIR, S.ANTIFASE_ADD, S.REGIME))
    stampa("  KICK_TW = %r   PHI_CRIT = %r   COPPIA_MIT = %r"
           % (S.KICK_TW, S.PHI_CRIT, S.COPPIA_MIT))

    # --- si CERCA il passo, non si assume
    sel = None
    k = 0
    while k < max_passi:
        k += 1
        un_passo(S, net)
        sel = sonda_sel(net)
        if sel is not None and len(sel):
            break
    if sel is None or not len(sel):
        stampa("  ### NESSUN CANDIDATO in %d passi: la misura NON si puo' fare." % max_passi)
        out["stato"] = "nessun candidato"
        return out
    out["passo_trovato"] = k
    out["atteso"] = PASSO_ATTESO_DIV
    out["archi_selezionati"] = int(len(sel))
    stampa("  primo passo con CANDIDATI: %d   (atteso dai fatti: %d)   archi selezionati: %d"
           % (k, PASSO_ATTESO_DIV, len(sel)))
    if k != PASSO_ATTESO_DIV:
        stampa("  ### IL PASSO NON E' QUELLO ATTESO, e lo dico invece di adattarmi: il")
        stampa("      mandato dice <<il passo PRIMA della prima divisione (il 42)>>, cioe'")
        stampa("      LO STATO DA CUI mitosi() divide. Questo e' quello stato, trovato")
        stampa("      sondando. Se il numero differisce, differisce la SCENA o l'ISTANTE.")

    a = np.asarray(net.i)[sel].copy()
    b = np.asarray(net.j)[sel].copy()
    n0 = int(net.n)
    archi0 = int(len(np.asarray(net.i)))
    att = attesa_calcio(S, net, sel, a, b)
    out["genitori"] = [{"arco": int(s), "a": int(x), "b": int(y),
                        "tw": float(np.asarray(net.tw, float)[s]),
                        "d": float(np.asarray(net.d, float)[s]),
                        "chi_a": float(ca), "chi_b": float(cb),
                        "sciolta": float(sc), "mod": float(mo),
                        "delta_phi_atteso_a": float(da), "delta_phi_atteso_b": float(db)}
                       for s, x, y, ca, cb, sc, mo, da, db
                       in zip(sel, a, b, att["chi_a"], att["chi_b"], att["sciolta"],
                              att["mod"], att["delta_a"], att["delta_b"])]

    stampa()
    stampa("  I GENITORI, arco per arco -- e `chi_a`/`chi_b` SI RIPORTANO, perche' se")
    stampa("  fossero uguali l'asimmetria misurata sarebbe solo quella del SEGNO")
    stampa("  %-6s %-7s %-7s %11s %9s %9s %13s" % ("arco", "a", "b", "tw", "chi_a", "chi_b",
                                                   "d_phi atteso"))
    for g in out["genitori"][:12]:
        stampa("  %-6d %-7d %-7d %11.4e %9.3f %9.3f %13.6e"
               % (g["arco"], g["a"], g["b"], g["tw"], g["chi_a"], g["chi_b"],
                  g["delta_phi_atteso_a"]))
    if len(out["genitori"]) > 12:
        stampa("  ... e altri %d archi" % (len(out["genitori"]) - 12))
    nz = int(np.sum(np.abs(att["chi_a"]) > 0) + np.sum(np.abs(att["chi_b"]) > 0))
    out["chi_non_nulle"] = nz
    out["chi_uguali"] = int(np.sum(att["chi_a"] == att["chi_b"]))
    stampa()
    stampa("  chiralita' NON nulle fra i %d genitori: %d" % (2 * len(sel), nz))
    if nz == 0:
        stampa("  ### ⚠ TUTTE LE CHIRALITA' SONO NULLE: l'attesa darebbe ZERO, e un")
        stampa("      calcio <<simmetrico>> qui sarebbe un FALSO-ZERO -- simmetrico perche'")
        stampa("      chi = 0, non perche' la legge sia simmetrica. LO DICO.")
    stampa("  archi con chi_a == chi_b: %d su %d  (dove sono uguali resta solo il SEGNO)"
           % (out["chi_uguali"], len(sel)))

    # --- il taglio di `_wphi`
    D = S._wphi(np.asarray(net.phi, float)[a] - np.asarray(net.phi, float)[b])
    sul_taglio = int(np.sum(np.abs(np.abs(D) - S._dphi() / 2.0) < 1e-12))
    out["archi_sul_taglio_wphi"] = sul_taglio
    stampa("  archi sul TAGLIO di _wphi (|D| = dphi/2): %d" % sul_taglio)
    if sul_taglio:
        stampa("  ### ⚠ SUL TAGLIO `fm` puo' differire di dphi senza che sia")
        stampa("      un'asimmetria fisica: e' una convenzione di wrap. DICHIARATO.")

    # --- le due copie, stesso generatore
    BASE = copy.deepcopy(net)
    SCA = copy.deepcopy(net)
    out["scambio"] = scambia(SCA, sel)
    sb = BASE.rng.bit_generator.state
    ss = SCA.rng.bit_generator.state
    out["generatore_identico"] = bool(sb == ss)
    stampa()
    stampa("  stato del generatore identico nelle due copie: %s" % out["generatore_identico"])
    if not out["generatore_identico"]:
        stampa("  ### FERMO: senza lo stesso generatore ogni scarto sarebbe rumore.")
        out["stato"] = "generatore diverso"
        return out

    # --- la condizione di validita': stessa selezione
    sel_b = sonda_sel(BASE)
    sel_s = sonda_sel(SCA)
    ugual = (sel_b is not None and sel_s is not None
             and len(sel_b) == len(sel_s) and bool(np.array_equal(np.sort(sel_b),
                                                                  np.sort(sel_s))))
    out["selezione_invariante"] = bool(ugual)
    stampa("  la SELEZIONE e' invariante allo scambio: %s   (%s archi contro %s)"
           % (ugual, len(sel_b) if sel_b is not None else None,
              len(sel_s) if sel_s is not None else None))
    if not ugual:
        stampa("  ### FERMO: BASE e SCAMBIO dividono archi DIVERSI. Il confronto sarebbe")
        stampa("      fra DUE EVENTI DIVERSI, e non e' un risultato: e' un confronto nullo.")
        out["stato"] = "selezione non invariante"
        return out

    # --- solo mitosi()
    with contextlib.redirect_stdout(io.StringIO()):
        nb = BASE.mitosi()
        ns = SCA.mitosi()
    out["nati_base"] = int(nb) if nb is not None else None
    out["nati_scambio"] = int(ns) if ns is not None else None
    stampa("  mitosi(): nati BASE = %s, nati SCAMBIO = %s" % (out["nati_base"],
                                                              out["nati_scambio"]))
    out["n_dopo_base"] = int(BASE.n)
    out["n_dopo_scambio"] = int(SCA.n)
    if BASE.n != SCA.n:
        stampa("  ### FERMO: n diverso dopo la mitosi (%d contro %d)." % (BASE.n, SCA.n))
        out["stato"] = "n diverso"
        return out

    figli = list(range(n0, int(BASE.n)))
    out["figli"] = figli
    stampa("  figli nati: %d  (indici %s)" % (len(figli), figli[:6]))

    # --- i confronti
    res = []
    res += confronta_nodi(BASE, SCA, np.concatenate([a, b]), "genitori")
    if figli:
        res += confronta_nodi(BASE, SCA, np.asarray(figli), "figlio")
    na = archi_nuovi(BASE, n0, archi0)
    nbq = archi_nuovi(SCA, n0, archi0)
    coppie, sp_a, sp_b = accoppia(na, nbq)
    out["archi_nuovi"] = {"base": len(na), "scambio": len(nbq),
                          "accoppiati": len(coppie),
                          "spaiati_base": len(sp_a), "spaiati_scambio": len(sp_b)}
    stampa("  archi nuovi: %d in BASE, %d in SCAMBIO, %d ACCOPPIATI per estremi, "
           "%d+%d spaiati" % (len(na), len(nbq), len(coppie), len(sp_a), len(sp_b)))
    if coppie:
        ra, orient = confronta_archi(BASE, SCA, coppie)
        res += ra
        out["orientamento_conservato"] = int(sum(orient))
        stampa("  archi accoppiati con lo STESSO orientamento (i==i): %d su %d"
               % (sum(orient), len(orient)))
    out["confronti"] = res

    # --- la tabella
    stampa()
    riga()
    stampa("  %-28s %-10s %-12s %12s %10s" % ("grandezza", "dove", "esito",
                                              "scarto max", "diversi"))
    riga()
    asim = []
    for r in res:
        if "simmetrica" not in r:
            stampa("  %-28s %-10s %-12s" % (r["grandezza"][:28], r["dove"][:10],
                                            r.get("stato", "?")[:12]))
            continue
        et = "SIMMETRICA" if r["simmetrica"] else "ASIMMETRICA"
        if not r["simmetrica"]:
            asim.append(r)
        stampa("  %-28s %-10s %-12s %12.5e %10d"
               % (r["grandezza"][:28], r["dove"][:10], et, r["scarto_max"],
                  r["elementi_diversi"]))
    riga()
    out["n_asimmetriche"] = len(asim)
    out["asimmetriche"] = [{"grandezza": r["grandezza"], "dove": r["dove"],
                            "scarto_max": r["scarto_max"],
                            "elementi_diversi": r["elementi_diversi"]} for r in asim]
    stampa("  ASIMMETRICHE: %d su %d grandezze confrontate" % (len(asim), len(res)))
    out["stato"] = "fatto"

    # --- il confronto fra lo scarto MISURATO su phi e quello ATTESO dal conto
    pa = np.asarray(BASE.phi, float)
    ps = np.asarray(SCA.phi, float)
    dmis_a = np.abs(S._wphi(pa[a] - ps[a]))
    dmis_b = np.abs(S._wphi(pa[b] - ps[b]))
    out["phi_misurato_vs_atteso"] = {
        "delta_a_misurato_max": float(np.max(dmis_a)) if len(dmis_a) else 0.0,
        "delta_a_atteso_max": float(np.max(np.abs(att["delta_a"]))) if len(sel) else 0.0,
        "delta_b_misurato_max": float(np.max(dmis_b)) if len(dmis_b) else 0.0,
        "delta_b_atteso_max": float(np.max(np.abs(att["delta_b"]))) if len(sel) else 0.0,
        "scarto_relativo_a": [float(x) for x in
                              (dmis_a - np.abs(att["delta_a"]))[:12]],
    }
    stampa()
    stampa("  LO SCARTO DI `phi` SUI GENITORI: misurato contro ATTESO dal conto")
    stampa("  %-10s %16s %16s %14s" % ("", "misurato", "atteso", "mis - att"))
    for et, dm, da in [("slot a", dmis_a, np.abs(att["delta_a"])),
                       ("slot b", dmis_b, np.abs(att["delta_b"]))]:
        if len(dm):
            stampa("  %-10s %16.9e %16.9e %14.3e"
                   % (et, float(np.max(dm)), float(np.max(da)),
                      float(np.max(np.abs(dm - da)))))
    return out


# ------------------------------------------------------------------ Schwinger
def misura_schwinger(S, net, max_passi, da_passo):
    """Il PRIMO passo in cui `mitosi()` fa nascere uno Schwinger, con `aa`/`bb`.

    ### Il ramo Schwinger ESTRAE dal generatore DENTRO `mitosi`, quindi non si puo'
    sondare senza eseguire: si esegue su una copia **usa-e-getta** e si guarda il
    contatore. ### **Un passo di sonda costa una `mitosi`, e lo dichiaro.**
    """
    out = {"da_passo": da_passo}
    k = da_passo
    trovato = None
    while k < max_passi:
        k += 1
        un_passo(S, net)
        q = copy.deepcopy(net)
        prima = int(getattr(q, "_g_nati_schwinger", 0))
        with contextlib.redirect_stdout(io.StringIO()):
            q.mitosi()
        dopo = int(getattr(q, "_g_nati_schwinger", 0))
        if dopo > prima:
            trovato = (k, dopo - prima)
            break
    if trovato is None:
        stampa("  ### NESSUN evento Schwinger fino al passo %d." % max_passi)
        out["stato"] = "nessuno schwinger"
        return out
    k, quanti = trovato
    out["passo_trovato"] = k
    out["atteso"] = PASSO_ATTESO_SCH
    out["nati_schwinger"] = quanti
    stampa("  primo evento SCHWINGER al passo %d   (atteso dal mandato: %d)   nati: %d"
           % (k, PASSO_ATTESO_SCH, quanti))

    sel = sonda_sel(net)
    if sel is None or not len(sel):
        out["stato"] = "nessun candidato al passo dello schwinger"
        stampa("  ### nessun candidato: non si puo' invertire niente.")
        return out
    a = np.asarray(net.i)[sel].copy()
    b = np.asarray(net.j)[sel].copy()
    n0, archi0 = int(net.n), int(len(np.asarray(net.i)))
    BASE = copy.deepcopy(net)
    SCA = copy.deepcopy(net)
    out["scambio"] = scambia(SCA, sel)
    out["generatore_identico"] = bool(BASE.rng.bit_generator.state
                                      == SCA.rng.bit_generator.state)
    sb, ss = sonda_sel(BASE), sonda_sel(SCA)
    out["selezione_invariante"] = bool(sb is not None and ss is not None
                                       and np.array_equal(np.sort(sb), np.sort(ss)))
    stampa("  generatore identico: %s   selezione invariante: %s"
           % (out["generatore_identico"], out["selezione_invariante"]))
    if not (out["generatore_identico"] and out["selezione_invariante"]):
        out["stato"] = "condizioni di validita' non soddisfatte"
        stampa("  ### FERMO sulle condizioni di validita'.")
        return out
    pb = int(getattr(BASE, "_g_nati_schwinger", 0))
    psq = int(getattr(SCA, "_g_nati_schwinger", 0))
    with contextlib.redirect_stdout(io.StringIO()):
        BASE.mitosi()
        SCA.mitosi()
    out["schwinger_base"] = int(getattr(BASE, "_g_nati_schwinger", 0)) - pb
    out["schwinger_scambio"] = int(getattr(SCA, "_g_nati_schwinger", 0)) - psq
    stampa("  nati Schwinger: BASE = %d, SCAMBIO = %d"
           % (out["schwinger_base"], out["schwinger_scambio"]))
    if out["schwinger_base"] != out["schwinger_scambio"]:
        stampa("  ### E QUESTA E' GIA' UNA RISPOSTA: lo SCHWINGER non e' invariante allo")
        stampa("      scambio nemmeno nel NUMERO di coppie create.")
    if BASE.n != SCA.n:
        stampa("  ### n diverso dopo la mitosi (%d contro %d): lo riporto e NON confronto"
               % (BASE.n, SCA.n))
        out["stato"] = "n diverso"
        out["n_base"], out["n_scambio"] = int(BASE.n), int(SCA.n)
        return out
    res = confronta_nodi(BASE, SCA, np.concatenate([a, b]), "genitori")
    figli = list(range(n0, int(BASE.n)))
    if figli:
        res += confronta_nodi(BASE, SCA, np.asarray(figli), "nati")
    na, nbq = archi_nuovi(BASE, n0, archi0), archi_nuovi(SCA, n0, archi0)
    coppie, sp_a, sp_b = accoppia(na, nbq)
    stampa("  archi nuovi: %d / %d, accoppiati %d, spaiati %d+%d"
           % (len(na), len(nbq), len(coppie), len(sp_a), len(sp_b)))
    if coppie:
        ra, _o = confronta_archi(BASE, SCA, coppie)
        res += ra
    asim = [r for r in res if r.get("simmetrica") is False]
    stampa()
    stampa("  %-28s %-10s %-12s %12s" % ("grandezza", "dove", "esito", "scarto max"))
    riga()
    for r in res:
        if "simmetrica" not in r:
            continue
        stampa("  %-28s %-10s %-12s %12.5e"
               % (r["grandezza"][:28], r["dove"][:10],
                  "SIMMETRICA" if r["simmetrica"] else "ASIMMETRICA", r["scarto_max"]))
    riga()
    stampa("  ASIMMETRICHE: %d su %d" % (len(asim), len(res)))
    out["n_asimmetriche"] = len(asim)
    out["asimmetriche"] = [{"grandezza": r["grandezza"], "dove": r["dove"],
                            "scarto_max": r["scarto_max"]} for r in asim]
    out["confronti"] = res
    out["stato"] = "fatto"
    out["archi_nuovi"] = {"base": len(na), "scambio": len(nbq),
                          "accoppiati": len(coppie)}
    return out


# ------------------------------------------------------------------ il controllo
def copia_con_frazione(t):
    """Una COPIA del sorgente con `FRAZ_NASCITA = t`.

    ### **Una sostituzione sola, e FALLISCE se l'ancora non e' unica** (`P1-quater`).
    ### ⚠ **E si cambia il SORGENTE di una copia, non un attributo del modulo:**
    `FRAZ_NASCITA` **non e' un flag** per decisione di Luca del 2026-10-03.
    """
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    dst = os.path.join(FUORI, "_sim_frazione_%s.py" % str(t).replace(".", "_"))
    testo = io.open(SIM, encoding="utf-8").read()
    ancora = "FRAZ_NASCITA = 0.5" + NL
    n = testo.count(ancora)
    if n != 1:
        raise SystemExit("[FERMO] l'ancora `FRAZ_NASCITA = 0.5` compare %d volte, non 1." % n)
    io.open(dst, "w", encoding="utf-8", newline=NL).write(
        testo.replace(ancora, "FRAZ_NASCITA = %r%s" % (float(t), NL)))
    return dst


def collaudo(max_passi):
    """### IL CONTROLLO CHE PUO' FALLIRE, con DUE valori e non uno.

    A `FRAZ_NASCITA != 0.5` **`pos_figlio` e `fm` NON sono invarianti**, e lo strumento
    **deve trovarli**. ### **Un controllo che passa solo a `0.4` non prova che lo strumento
    vede le asimmetrie: prova che vede `0.4`.**
    """
    riga("=")
    stampa("IL CONTROLLO CHE PUO' FALLIRE -- due frazioni, non una")
    riga("=")
    esiti = []
    for t in (0.4, 0.3):
        stampa()
        riga()
        stampa("  FRAZ_NASCITA = %r  (copia del sorgente, il simulatore NON si tocca)" % t)
        riga()
        dst = copia_con_frazione(t)
        stampa("  copia: %s  blob %s" % (os.path.basename(dst), blob(dst)[:8]))
        S, net, a = carica("sim_fraz_%s" % str(t).replace(".", "_"), sim=dst)
        if float(S.FRAZ_NASCITA) != float(t):
            stampa("  ### FERMO: la copia dichiara FRAZ_NASCITA = %r, non %r."
                   % (S.FRAZ_NASCITA, t))
            return 1
        r = misura(S, net, a, t, max_passi, "controllo t=%s" % t)
        nomi = {x["grandezza"] for x in r.get("asimmetriche", [])}
        trovato_pos = "pos" in nomi
        trovato_phi = "phi" in nomi
        stampa()
        stampa("  `pos` ASIMMETRICA trovata: %s     `phi` (cioe' `fm`) asimmetrica: %s"
               % (trovato_pos, trovato_phi))
        buono = bool(trovato_pos and trovato_phi)
        esiti.append((t, buono, sorted(nomi)))
        stampa("  ### %s" % ("OK: lo strumento VEDE l'asimmetria indotta."
                             if buono else
                             "*** CIECO: a t=%r doveva trovare pos E phi asimmetriche. ***" % t))
    stampa()
    riga("=")
    ok = all(b for _t, b, _n in esiti)
    for t, b, nomi in esiti:
        stampa("  t=%-4s  %s   asimmetriche trovate: %s"
               % (t, "OK " if b else "CIECO", ", ".join(nomi[:10]) or "nessuna"))
    stampa("  ### %s" % ("i due controlli passano: lo strumento NON e' cieco."
                         if ok else "*** CONTROLLO FALLITO: FERMATI (lo dice il mandato). ***"))
    riga("=")
    return 0 if ok else 1


def piattaforma():
    return {"python": sys.version.split()[0], "numpy": np.__version__,
            "sistema": platform.system() + " " + platform.release(),
            "macchina": platform.machine()}


def principale(max_passi):
    riga("=")
    stampa("IL CALCIO DELLA MITOSI SOTTO LO SCAMBIO a<->b, ISOLATO")
    riga("=")
    stampa()
    stampa("### NON E' UN SIGILLO: il mandato dice SOLO MISURE, e il punto 3 dice NIENTE CURE.")
    stampa()
    pf = piattaforma()
    for k in ["python", "numpy", "sistema", "macchina"]:
        stampa("  %-10s %s" % (k, pf[k]))
    stampa("  simulatore %s  (sha1 dei byte grezzi, NON toccato)" % blob(SIM)[:8])
    stampa()
    riga("=")
    stampa("PARTE 1 -- LA DIVISIONE")
    riga("=")
    S, net, a = carica("sim_calcio")
    div = misura(S, net, a, float(S.FRAZ_NASCITA), max_passi, "divisione")
    stampa()
    riga("=")
    stampa("PARTE 2 -- LO SCHWINGER, con `aa` e `bb`")
    riga("=")
    sch = {}
    if div.get("stato") == "fatto":
        S2, net2, a2 = carica("sim_calcio_sch")
        k0 = 0
        # si riparte da zero e si avanza fino al passo della divisione, poi si cerca
        # lo Schwinger: ### la rete di PARTE 1 e' stata consumata dalle sonde.
        while k0 < div["passo_trovato"]:
            k0 += 1
            un_passo(S2, net2)
        sch = misura_schwinger(S2, net2, max_passi, k0)
    else:
        stampa("  salto: la parte 1 non e' arrivata a un confronto.")
    fuori = {"piattaforma": pf, "blob_sim": blob(SIM),
             "timbro_strumento": _presidio.timbro(__file__),
             "divisione": div, "schwinger": sch}
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    json.dump(fuori, io.open(os.path.join(FUORI, "_calcio_sotto_scambio.json"), "w",
                             encoding="utf-8"),
              indent=1, ensure_ascii=False, sort_keys=True, default=str)
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8").write(NL.join(P))
    print("scritto: %s" % os.path.join(FUORI, "_calcio_sotto_scambio.json"))
    return 0


if __name__ == "__main__":
    mp = MAX_PASSI
    for _a in sys.argv[1:]:
        if _a.startswith("--max-passi="):
            mp = int(_a.split("=", 1)[1])
    if "--collaudo" in sys.argv[1:]:
        _r = collaudo(mp)
        if not os.path.isdir(FUORI):
            os.makedirs(FUORI)
        io.open(os.path.join(FUORI, "_collaudo.txt"), "w", encoding="utf-8").write(NL.join(P))
        sys.exit(_r)
    sys.exit(principale(mp))
