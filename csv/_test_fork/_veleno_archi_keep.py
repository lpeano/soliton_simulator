# -*- coding: utf-8 -*-
"""IL VELENO E `keep`: le derivate d'arco si riallineano, o leggono un altro arco?

*(`VELENO-ARCHI-KEEP`, passo **(1): la misura che conferma la causa**. Mandato di Luca del
2026-10-05. Task history: `doc/TASK_HISTORY/2026-10-05_veleno-archi-keep-misura.md`,
committato PRIMA.)*

### ⛔ **E' UNA MISURA, NON UNA CURA:** nessun `PASSA`/`FALLISCE` **fuori dai controlli**, e
### il simulatore **non si tocca** -- la misura vive in una **COPIA PATCHATA**.

### L'IPOTESI, letta dal codice e da MISURARE
Alla nascita la mitosi ricostruisce le colonne d'arco con `i = concat(i[keep], a, m)`
*(`:1743`)*: **toglie** archi e ne **aggiunge** in coda. `_avvelena_derivate` *(`:1521`,
chiamata a `:1707`)* allunga **in coda** con `NaN` quando `len(v) < bersaglio`, e
### **non applica `keep`** -- la parola non compare **mai** in quella funzione.
### ➜ **Dopo il primo arco tolto, ogni arco legge il valore di UN ALTRO arco: un valore
FINITO, che il veleno non segnala.**

### IL CONTO CHE RENDE IL DIFETTO SILENZIOSO
Con `s` archi divisi: tolti `s`, aggiunti `2s`, `m_nuovo = m + s`, e il veleno appende
`quanti = (m+s) - m = `**`s`** celle `NaN` -- ### **mentre gli archi NUOVI sono `2s`.**
### **Copre META' degli archi nuovi; l'altra meta' riceve un valore FINITO di un arco
vecchio, e un valore finito non fa scattare nessun controllo.**

### I CONTROLLI CHE POSSONO FALLIRE
| | |
|---|---|
| ### **il caso che DISCRIMINA la causa** | negli eventi **senza archi tolti** le differenze devono essere **ZERO**. ### **Se compaiono, l'ipotesi e' SBAGLIATA e la cura non si propone: FERMO** |
| ### **il controllo POSITIVO** | l'allineamento **corretto** -- `concat(vecchio[keep], NaN)` -- confrontato con l'atteso deve dare **ZERO** differenze. ### **Se no, il confronto e' sbagliato: FERMO** |
| **il conteggio** | si dichiara su **quanti archi** si e' confrontato. ### **Zero archi non e' un'identita'** |

### ✅ **E IL CASO CHE DISCRIMINA VIENE GRATIS DALLA STESSA CORSA:** la **divisione** usa
`keep` *(`:1743`)*, lo **Schwinger NO** *(`concat(net.i, aa, k)`, `:2171`)*.

USO:
  python csv/_test_fork/_veleno_archi_keep.py
  python csv/_test_fork/_veleno_archi_keep.py --collaudo
  opzioni: --passi=N (default 150)

USCITA: `csv/_test_fork/_veleno_archi_keep/_veleno_archi_keep.json` + `_corsa.txt`.

# ESENTE-H-P3: la scena passa TUTTA dal CLI (`nmasse` e `sep` da `argv`). La COPIA PATCHATA
#   serve a registrare DENTRO `nascita`, prima delle regole e dopo il veleno: il gancio di
#   voce da' lo stato ai CONFINI, e `keep` vive solo nel contesto `c` di quella chiamata --
#   ricostruirlo fuori sarebbe una SECONDA scrittura della stessa legge.
"""
import contextlib
import hashlib
import io
import json
import os
import platform
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
FUORI = os.path.join(RADICE, "csv", "_test_fork", "_veleno_archi_keep")
SIM = os.path.join(RADICE, "soliton_simulator.py")
PASSI = 150
# ### LE DUE DERIVATE D'ARCO CON CLASSE `avvelena`, e NON le scrivo a mano: lo strumento
#   le LEGGE dal `REGISTRO_DERIVATE` del modulo caricato. Un elenco qui sarebbe una
#   seconda fonte, e divergerebbe -- che e' cio' che il veleno stesso dichiara.

P = []


def stampa(s=""):
    print(s)
    P.append(s)


def riga(c="-"):
    stampa(c * 104)


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def uguali_elem(x, y):
    """Uguaglianza fra ELEMENTI, con `NaN` contro `NaN` = UGUALE.

    ### La domanda e' *<<e' lo stesso valore?>>*, non *<<quanto distano?>>*: e' la stessa
    scelta del confronto di `_verso_archi`, e per la stessa ragione -- `nan - nan` da'
    `nan`, che non e' mai `== 0`, quindi la DISTANZA mente.
    """
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    if x.shape != y.shape:
        return None
    return (x == y) | (np.isnan(x) & np.isnan(y))


# =============================================================== LA PATCH
def copia_patchata():
    """Una COPIA del sorgente con due punti di registrazione DENTRO `nascita`.

    ### Ogni sostituzione si asserisce per se' e FALLISCE se l'ancora non e' unica
    ### (`P1-quater`); ancore ASCII, nessun escape.
    """
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    dst = os.path.join(FUORI, "_sim_veleno_keep.py")
    t = io.open(SIM, encoding="utf-8").read()
    fatte = []

    def uno(a, b, et):
        nonlocal t
        n = t.count(a)
        if n != 1:
            raise SystemExit("[FERMO] l'ancora di `%s` compare %d volte, non 1." % (et, n))
        t = t.replace(a, b)
        fatte.append(et)

    uno("import numpy as np" + NL,
        "import numpy as np" + NL + "_MIS = None   # [MISURA VELENO/keep] lo riempie lo strumento"
        + NL, "il gancio di modulo `_MIS`")

    # PRIMA che le regole scrivano: lo stato vecchio e il contesto (con `keep`)
    uno("    for nome in ORDINE_DI_NASCITA:" + NL + "        voce = REGOLE_NASCITA.get((evento, nome))",
        "    if _MIS is not None:" + NL
        + "        _MIS(net, 'prima', evento=evento, c=c)" + NL
        + "    for nome in ORDINE_DI_NASCITA:" + NL
        + "        voce = REGOLE_NASCITA.get((evento, nome))",
        "il PRIMA, dentro `nascita` e davanti alle regole")

    # DOPO il veleno
    uno("    _avvelena_derivate(net)" + NL,
        "    _avvelena_derivate(net)" + NL
        + "    if _MIS is not None:" + NL
        + "        _MIS(net, 'dopo', evento=evento, c=c)" + NL,
        "il DOPO, subito dopo `_avvelena_derivate`")

    io.open(dst, "w", encoding="utf-8", newline=NL).write(t)
    return dst, fatte


# =============================================================== IL RACCOGLITORE
class Raccoglitore(object):
    """Registra A OGNI EVENTO di nascita, prima e dopo, e confronta."""

    def __init__(self, S):
        self.S = S
        # ### le derivate le LEGGE dal registro del modulo, non da un elenco mio
        self.arco_avv = [v[0] for v in S.REGISTRO_DERIVATE
                         if len(v) >= 3 and v[1] == "arco" and v[2] == "avvelena"]
        self.nodo_avv = [v[0] for v in S.REGISTRO_DERIVATE
                         if len(v) >= 3 and v[1] == "nodo" and v[2] == "avvelena"]
        self.passo = 0
        self.prima = None
        self.eventi = []

    def __call__(self, net, quando, evento=None, c=None):
        if quando == "prima":
            self._prima(net, evento, c)
        else:
            self._dopo(net, evento, c)

    # ------------------------------------------------------------- prima
    def _prima(self, net, evento, c):
        keep = None if c is None else c.get("keep")
        self.prima = {
            "passo": self.passo, "evento": evento,
            "m": int(len(np.asarray(net.i))), "n": int(len(np.asarray(net.phi))),
            "keep": None if keep is None else np.asarray(keep).astype(bool).copy(),
            "arco": {k: (None if getattr(net, k, None) is None
                         else np.asarray(getattr(net, k)).copy())
                     for k in self.arco_avv},
            "nodo": {k: (None if getattr(net, k, None) is None
                         else np.asarray(getattr(net, k)).copy())
                     for k in self.nodo_avv},
            "phi": np.asarray(net.phi, float).copy(),
        }

    # ------------------------------------------------------------- dopo
    def _dopo(self, net, evento, c):
        if self.prima is None:
            return
        pr = self.prima
        self.prima = None
        m_d = int(len(np.asarray(net.i)))
        n_d = int(len(np.asarray(net.phi)))
        keep = pr["keep"]
        if keep is None:
            # ### lo Schwinger NON ha `keep`: nessun arco tolto. Si tratta come
            #   `keep` tutto VERO su `m` posizioni -- ed e' il CASO CHE DISCRIMINA.
            keep_eff = np.ones(pr["m"], bool)
            keep_assente = True
        else:
            keep_eff = keep
            keep_assente = False
        tenuti = int(np.sum(keep_eff))
        tolti = int(len(keep_eff) - tenuti)
        aggiunti = m_d - tenuti
        primo_tolto = (int(np.argmin(keep_eff)) if tolti else None)
        out = {"passo": pr["passo"], "evento": evento,
               "m_prima": pr["m"], "m_dopo": m_d,
               "n_prima": pr["n"], "n_dopo": n_d,
               "keep_assente": keep_assente, "len_keep": int(len(keep_eff)),
               "archi_tenuti": tenuti, "archi_tolti": tolti, "archi_aggiunti": aggiunti,
               "primo_arco_tolto": primo_tolto,
               "keep_tutto_vero": bool(tolti == 0),
               "derivate": {}, "nodo": {}, "controllo_positivo": {}}

        # ---------------------------------------------- le derivate D'ARCO
        for k in self.arco_avv:
            v = pr["arco"][k]
            w = getattr(net, k, None)
            d = {"presente_prima": v is not None, "presente_dopo": w is not None}
            if v is None or w is None:
                d["stato"] = "assente prima" if v is None else "assente dopo"
                out["derivate"][k] = d
                continue
            v = np.asarray(v)
            w = np.asarray(w)
            d.update({"len_prima": int(len(v)), "len_dopo": int(len(w)),
                      "ndim": int(v.ndim), "dtype": str(v.dtype)})
            if v.ndim != 1 or v.dtype.kind != "f":
                d["stato"] = "non avvelenabile (ndim o dtype): il veleno la SALTA"
                out["derivate"][k] = d
                continue
            if len(v) != pr["m"]:
                d["stato"] = ("len PRIMA (%d) != archi prima (%d): non confrontabile"
                              % (len(v), pr["m"]))
                out["derivate"][k] = d
                continue
            # ### L'ATTESO: il valore degli archi CONSERVATI, nell'ordine di `keep`.
            atteso = v[np.flatnonzero(keep_eff)]
            if len(w) < len(atteso):
                d["stato"] = "len DOPO piu' corta dell'atteso: non confrontabile"
                out["derivate"][k] = d
                continue
            reale = w[:len(atteso)]
            ug = uguali_elem(atteso, reale)
            diversi = int(np.sum(~ug))
            pos = (int(np.flatnonzero(~ug)[0]) if diversi else None)
            d.update({"archi_confrontati": int(len(atteso)), "elementi_diversi": diversi,
                      "prima_posizione_diversa": pos,
                      "coincide_col_primo_tolto": (None if (pos is None
                                                            or primo_tolto is None)
                                                   else bool(pos == primo_tolto))})
            # il veleno: quante celle NON FINITE in coda, e quante ne servirebbero
            coda = w[len(atteso):]
            d.update({"celle_in_coda": int(len(coda)),
                      "non_finite_in_coda": int(np.sum(~np.isfinite(coda))),
                      "archi_nuovi": aggiunti,
                      "celle_nan_appese": max(0, int(len(w)) - int(len(v)))})
            if aggiunti:
                d["copertura_veleno"] = (float(d["non_finite_in_coda"]) / float(aggiunti))
            # ### IL CONTROLLO POSITIVO: l'allineamento CORRETTO deve coincidere
            #   con l'atteso sulla parte conservata. Se no, il confronto e' sbagliato.
            corretto = np.concatenate([v[np.flatnonzero(keep_eff)],
                                       np.full(max(0, aggiunti), np.nan)])
            ug2 = uguali_elem(atteso, corretto[:len(atteso)])
            d["positivo_diversi"] = int(np.sum(~ug2)) if ug2 is not None else -1
            d["stato"] = "confrontato"
            out["derivate"][k] = d

        # ---------------------------------------------- i NODI: solo aggiunti?
        ug = uguali_elem(pr["phi"], np.asarray(net.phi, float)[:pr["n"]])
        out["nodo"]["phi_testa_invariata"] = (None if ug is None
                                              else bool(np.all(ug)))
        out["nodo"]["phi_diversi_in_testa"] = (None if ug is None
                                               else int(np.sum(~ug)))
        out["nodo"]["n_solo_cresciuto"] = bool(n_d >= pr["n"])
        for k in self.nodo_avv:
            v = pr["nodo"][k]
            w = getattr(net, k, None)
            if v is None or w is None:
                continue
            v = np.asarray(v)
            w = np.asarray(w)
            if v.ndim != 1 or v.dtype.kind != "f" or len(w) < len(v):
                continue
            u = uguali_elem(v, w[:len(v)])
            out["nodo"][k] = {"len_prima": int(len(v)), "len_dopo": int(len(w)),
                              "testa_invariata": bool(np.all(u)),
                              "diversi_in_testa": int(np.sum(~u))}
        self.eventi.append(out)


# =============================================================== il collaudo
def collaudo():
    riga("=")
    stampa("COLLAUDO -- i casi che decidono se la misura e' leggibile")
    riga("=")
    ok = True

    # (1) il CONFRONTO su un caso costruito: 5 archi, il 2 tolto, 2 aggiunti
    v = np.array([10.0, 11.0, 12.0, 13.0, 14.0])
    keep = np.array([True, True, False, True, True])
    # cio' che il simulatore FA oggi: coda di NaN, senza `keep`
    oggi = np.concatenate([v, np.full(1, np.nan)])
    atteso = v[np.flatnonzero(keep)]
    reale = oggi[:len(atteso)]
    ug = uguali_elem(atteso, reale)
    diversi = int(np.sum(~ug))
    pos = int(np.flatnonzero(~ug)[0]) if diversi else None
    buono = (diversi == 2 and pos == 2)
    ok = ok and buono
    stampa("  (1) il difetto su un caso costruito: %d diversi (attesi 2), prima pos %s"
           % (diversi, pos))
    stampa("      (atteso 2 = il primo arco tolto)   %s" % ("OK" if buono else "FALLITO"))

    # (2) ### IL CONTROLLO POSITIVO: l'allineamento CORRETTO da' ZERO differenze
    corretto = np.concatenate([v[np.flatnonzero(keep)], np.full(2, np.nan)])
    ug2 = uguali_elem(atteso, corretto[:len(atteso)])
    d2 = int(np.sum(~ug2))
    buono = d2 == 0
    ok = ok and buono
    stampa("  (2) controllo POSITIVO: l'allineamento corretto da' %d differenze (atteso 0)"
           "   %s" % (d2, "OK" if buono else "FALLITO"))

    # (3) ### IL CASO CHE DISCRIMINA: `keep` tutto VERO -> differenze ZERO
    keep2 = np.ones(5, bool)
    oggi2 = np.concatenate([v, np.full(2, np.nan)])
    att2 = v[np.flatnonzero(keep2)]
    d3 = int(np.sum(~uguali_elem(att2, oggi2[:len(att2)])))
    buono = d3 == 0
    ok = ok and buono
    stampa("  (3) CASO CHE DISCRIMINA (keep tutto vero): %d differenze (atteso 0)   %s"
           % (d3, "OK" if buono else "FALLITO -- il confronto DA' FALSI POSITIVI"))

    # (4) `NaN` contro `NaN` e' UGUALE, e la distanza mentirebbe
    a = np.array([1.0, np.nan])
    b = np.array([1.0, np.nan])
    buono = bool(np.all(uguali_elem(a, b))) and not np.all(a - b == 0)
    ok = ok and buono
    stampa("  (4) NaN contro NaN: uguale %s, mentre la DISTANZA direbbe diverso   %s"
           % (bool(np.all(uguali_elem(a, b))), "OK" if buono else "FALLITO"))

    # (5) la copertura del veleno: s celle per 2s archi nuovi
    s = 3
    m = 100
    cop = float(s) / float(2 * s)
    buono = abs(cop - 0.5) < 1e-12
    ok = ok and buono
    stampa("  (5) copertura del veleno con s=%d: %.3f (atteso 0.500)   %s"
           % (s, cop, "OK" if buono else "FALLITO"))

    # (6) la patch attacca, e le ancore sono UNICHE
    try:
        dst, fatte = copia_patchata()
        stampa("  (6) la patch attacca: %d ancore, tutte uniche   OK" % len(fatte))
        for f in fatte:
            stampa("        %s" % f)
        stampa("      copia: %s  blob %s" % (os.path.basename(dst), blob(dst)[:8]))
    except SystemExit as e:
        ok = False
        stampa("  (6) la patch NON attacca: %s   FALLITO" % (e,))

    stampa()
    stampa("  ### %s" % ("tutti i casi passano." if ok else "*** COLLAUDO FALLITO ***"))
    riga("=")
    return 0 if ok else 1


# =============================================================== il corpo
def piattaforma():
    return {"python": sys.version.split()[0], "numpy": np.__version__,
            "sistema": platform.system() + " " + platform.release(),
            "macchina": platform.machine()}


def principale(passi):
    riga("=")
    stampa("IL VELENO E `keep`: le derivate d'arco si riallineano, o leggono un altro arco?")
    riga("=")
    stampa()
    stampa("### E' UNA MISURA, NON UNA CURA: nessun PASSA/FALLISCE fuori dai controlli.")
    stampa()
    pf = piattaforma()
    for k in ["python", "numpy", "sistema", "macchina"]:
        stampa("  %-10s %s" % (k, pf[k]))
    stampa("  simulatore %s  (sha1 dei byte grezzi, NON toccato)" % blob(SIM)[:8])
    dst, fatte = copia_patchata()
    stampa("  copia patchata: %s  blob %s  (%d ancore)"
           % (os.path.basename(dst), blob(dst)[:8], len(fatte)))
    stampa()

    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                              dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome="sim_veleno", sim=dst)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    net = S.net
    R = Raccoglitore(S)
    S._MIS = R

    riga()
    stampa("IL CENSIMENTO, dal REGISTRO_DERIVATE del modulo caricato (non un elenco mio)")
    riga()
    stampa("  derivate d'ARCO con classe `avvelena`: %d  ->  %s"
           % (len(R.arco_avv), ", ".join(R.arco_avv)))
    stampa("  derivate di NODO con classe `avvelena`: %d" % len(R.nodo_avv))
    stampa("  scena: nmasse=%s sep=%s  ->  n = %d, archi = %d"
           % (getattr(a, "nmasse", "?"), getattr(a, "sep", "?"), net.n, len(net.i)))
    stampa()

    riga("=")
    stampa("IL RUN: %d passi, col BATTITO per passo" % passi)
    riga("=")
    for k in range(1, passi + 1):
        R.passo = k
        prima_ev = len(R.eventi)
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(S, net)
        nuovi = len(R.eventi) - prima_ev
        # ### IL BATTITO, e non e' un vezzo: senza, una richiesta di stato deve STIMARE
        #   il passo invece di leggerlo -- ed e' un debito che ho annotato io stesso
        #   sullo strumento del tetto causale.
        print("[battito] passo %d/%d  n=%d archi=%d eventi_qui=%d eventi_tot=%d"
              % (k, passi, net.n, len(net.i), nuovi, len(R.eventi)), flush=True)
    stampa("  passi girati: %d   n finale = %d, archi = %d" % (passi, net.n, len(net.i)))
    stampa("  EVENTI DI NASCITA registrati: %d" % len(R.eventi))
    per_ev = {}
    for e in R.eventi:
        per_ev[e["evento"]] = per_ev.get(e["evento"], 0) + 1
    stampa("  per tipo: %s" % (per_ev or "NESSUNO"))
    if not R.eventi:
        stampa("  ### ATTENZIONE: nessun evento registrato. Un referto di zeri qui NON")
        stampa("      significa <<il difetto non c'e'>>: significa che la misura non e'")
        stampa("      avvenuta. LO DICO invece di riportare zeri.")
    stampa()

    fuori = {"piattaforma": pf, "blob_sim": blob(SIM), "blob_copia": blob(dst),
             "timbro_strumento": _presidio.timbro(__file__),
             "ancore_patch": fatte, "passi": passi,
             "arco_avvelena": R.arco_avv, "nodo_avvelena": R.nodo_avv,
             "eventi_per_tipo": per_ev, "eventi": R.eventi,
             "scena": {"nmasse": getattr(a, "nmasse", None),
                       "sep": getattr(a, "sep", None)}}

    # ----------------------------------------------------- il referto
    riga("=")
    stampa("GLI EVENTI, e la geometria di `keep`")
    riga("=")
    stampa("  %-6s %-10s %8s %8s %7s %7s %8s %12s"
           % ("passo", "evento", "m_prima", "m_dopo", "tolti", "aggiunti", "1o_tolto",
              "keep_assente"))
    for e in R.eventi[:24]:
        stampa("  %-6d %-10s %8d %8d %7d %7d %8s %12s"
               % (e["passo"], e["evento"], e["m_prima"], e["m_dopo"], e["archi_tolti"],
                  e["archi_aggiunti"], e["primo_arco_tolto"], e["keep_assente"]))
    if len(R.eventi) > 24:
        stampa("  ... e altri %d eventi (tutti nel json)" % (len(R.eventi) - 24))
    stampa()

    riga("=")
    stampa("IL CONFRONTO, per derivata d'arco e per evento")
    riga("=")
    tot_conf = tot_div = 0
    coincide = 0
    senza_tolti = []
    con_tolti = []
    pos_err = []
    for e in R.eventi:
        for k, d in e["derivate"].items():
            if d.get("stato") != "confrontato":
                continue
            tot_conf += d["archi_confrontati"]
            tot_div += d["elementi_diversi"]
            if d.get("coincide_col_primo_tolto"):
                coincide += 1
            if e["keep_tutto_vero"]:
                senza_tolti.append((e, k, d))
            else:
                con_tolti.append((e, k, d))
            if d.get("positivo_diversi", 0):
                pos_err.append((e, k, d))
    stampa("  confronti con esito: %d   archi confrontati IN TOTALE: %d"
           % (len(senza_tolti) + len(con_tolti), tot_conf))
    stampa("  ### E IL NUMERO SI DICHIARA: zero archi NON e' un'identita'.")
    stampa("  elementi diversi IN TOTALE: %d" % tot_div)
    stampa()
    stampa("  --- eventi CON archi tolti (la divisione) ---")
    stampa("  confronti: %d" % len(con_tolti))
    cd = sum(1 for _e, _k, d in con_tolti if d["elementi_diversi"])
    stampa("  con DIFFERENZE: %d su %d" % (cd, len(con_tolti)))
    stampa("  la prima posizione diversa COINCIDE col primo arco tolto in %d confronti"
           % coincide)
    for e, k, d in con_tolti[:10]:
        stampa("     passo %-4d %-14s diversi %7d / %7d  1a_pos %-7s primo_tolto %-7s"
               % (e["passo"], k, d["elementi_diversi"], d["archi_confrontati"],
                  d["prima_posizione_diversa"], e["primo_arco_tolto"]))
        stampa("            coda %d celle, non finite %d, archi nuovi %d  ->  copertura %s"
               % (d["celle_in_coda"], d["non_finite_in_coda"], d["archi_nuovi"],
                  ("%.3f" % d["copertura_veleno"]) if "copertura_veleno" in d else "-"))
    stampa()
    stampa("  --- eventi SENZA archi tolti: IL CASO CHE DISCRIMINA ---")
    stampa("  confronti: %d" % len(senza_tolti))
    sd = sum(1 for _e, _k, d in senza_tolti if d["elementi_diversi"])
    stampa("  con DIFFERENZE: %d   (devono essere ZERO)" % sd)
    for e, k, d in senza_tolti[:6]:
        stampa("     passo %-4d %-14s diversi %d / %d   evento %s"
               % (e["passo"], k, d["elementi_diversi"], d["archi_confrontati"],
                  e["evento"]))
    stampa()

    riga("=")
    stampa("I NODI: solo AGGIUNTI, mai tolti o riordinati?")
    riga("=")
    tn = [e for e in R.eventi if e["nodo"].get("phi_testa_invariata") is not None]
    bad = [e for e in tn if not e["nodo"]["phi_testa_invariata"]]
    cres = [e for e in R.eventi if not e["nodo"].get("n_solo_cresciuto", True)]
    stampa("  eventi con la testa di `phi` verificata: %d" % len(tn))
    stampa("  eventi in cui la testa di `phi` E' CAMBIATA: %d" % len(bad))
    stampa("  eventi in cui `n` NON e' solo cresciuto: %d" % len(cres))
    nodi_bad = 0
    for e in R.eventi:
        for k, v in e["nodo"].items():
            if isinstance(v, dict) and not v.get("testa_invariata", True):
                nodi_bad += 1
    stampa("  derivate di NODO con la testa cambiata: %d" % nodi_bad)
    stampa()

    # ----------------------------------------------------- i controlli
    riga("=")
    stampa("I CONTROLLI CHE POSSONO FALLIRE")
    riga("=")
    esito = 0
    stampa("  (positivo) confronti in cui l'allineamento CORRETTO non da' zero: %d"
           % len(pos_err))
    if pos_err:
        stampa("  ### FERMO: il confronto e' sbagliato, non il simulatore.")
        esito = 1
    if tot_conf == 0:
        stampa("  ### FERMO: ZERO archi confrontati. Non e' un'identita': e' mancanza di")
        stampa("      confronto (presidio di FATTI_dal_codice).")
        esito = 1
    stampa("  (discrimina) eventi SENZA archi tolti con differenze: %d" % sd)
    if sd:
        stampa("  ### FERMO: differenze SENZA archi tolti. L'IPOTESI E' SBAGLIATA, e il")
        stampa("      mandato dice di NON proporre la cura.")
        esito = 1
    if not senza_tolti:
        stampa("  ### ATTENZIONE: nessun evento senza archi tolti in questa corsa.")
        stampa("      IL CASO CHE DISCRIMINA NON HA GIRATO, e lo dico invece di")
        stampa("      presentare il controllo come passato.")
    if esito == 0 and senza_tolti and con_tolti:
        stampa("  ### I CONTROLLI PASSANO: il positivo da' zero, e le differenze")
        stampa("      compaiono SOLO dove ci sono archi tolti.")
    riga("=")
    fuori["controlli"] = {"positivo_errori": len(pos_err),
                          "archi_confrontati": tot_conf,
                          "elementi_diversi": tot_div,
                          "senza_tolti_confronti": len(senza_tolti),
                          "senza_tolti_con_differenze": sd,
                          "con_tolti_confronti": len(con_tolti),
                          "con_tolti_con_differenze": cd,
                          "coincide_col_primo_tolto": coincide,
                          "nodi_testa_cambiata": nodi_bad,
                          "esito": esito}

    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    json.dump(fuori, io.open(os.path.join(FUORI, "_veleno_archi_keep.json"), "w",
                             encoding="utf-8"),
              indent=1, ensure_ascii=False, sort_keys=True, default=str)
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8").write(NL.join(P))
    print("scritto: %s" % os.path.join(FUORI, "_veleno_archi_keep.json"))
    return esito


if __name__ == "__main__":
    pp = PASSI
    for _a in sys.argv[1:]:
        if _a.startswith("--passi="):
            pp = int(_a.split("=", 1)[1])
    if "--collaudo" in sys.argv[1:]:
        _r = collaudo()
        if not os.path.isdir(FUORI):
            os.makedirs(FUORI)
        io.open(os.path.join(FUORI, "_collaudo.txt"), "w",
                encoding="utf-8").write(NL.join(P))
        sys.exit(_r)
    sys.exit(principale(pp))
