# -*- coding: utf-8 -*-
"""`MEM-HEBB-VERSO`: LA FORMA DI `proj` E IL SITO DELLA FASE, MISURATI A LATO.

*(`MEM-HEBB-VERSO`, passo **(1): decisione registrata e misura**. Mandato di Luca del
2026-10-04, eseguito il 2026-10-05 sul blob `e2940b3c`. Task history:
`doc/TASK_HISTORY/2026-10-04_mem-hebb-verso-misura.md`, committato PRIMA.)*

### ⛔ **E' UNA MISURA, NON UNA CURA:** nessun `PASSA`/`FALLISCE` **fuori dai controlli**, e
### il simulatore **non si tocca** -- le forme nuove si calcolano in una **COPIA PATCHATA**.

### LE DUE DECISIONI DI LUCA, registrate e NON reinterpretate
**(1) LA FORMA DI `proj`**, oggi a `:9132-9134`:

    oggi    proj = sum( 0.5*(m_i*I_i + m_j*I_j)/Imed . dir(i->j) )
    DECISA  proj = 0.5*(I_i+I_j)/Imed * (m_j - m_i) . dir(i->j)

con `m = mem_mot`. ### **E' invariante per scambio `i<->j`, nulla per traslazione rigida,
positiva se i nodi si allontanano.** ### **Il peso sta sull'ARCO, non sul nodo:** col peso
per nodo la traslazione rigida di masse diverse **non** da' zero.

**(2) IL SITO DELLA FASE** *(`:9506-9531`)* **si SPEGNE con un flag proprio**, e
`MEM_MOTO_TUTTO`/`MEM_MOTO` **restano come sono**. I tre difetti: solo l'estremo `ii`
riceve; `phi[ii] = ...` con indici ripetuti tiene **l'ultima** scrittura;
`dir_laterale = (-y, x, 0)` privilegia l'asse `z` del **laboratorio** mentre i nodi stanno
in 3D *(`:4940`)*. ### **La terza e' la voce nuova `FASE-TRASCINAMENTO-3D`, ed e' LEGGE
NUOVA: non si scrive adesso.**

### I TRE CONTROLLI CHE POSSONO FALLIRE
| | |
|---|---|
| **`C1`** | la forma **vecchia** ricalcolata a lato coincide ### **AL BIT** col `proj` del simulatore, ### **dopo il taglio**, su ogni arco. ### **Se no, misuro un'altra cosa: FERMO** |
| **`C2`** | forma **decisa** con `mem_mot` sostituita da un **vettore costante**: `proj = 0` ### **esatto**. ### **E la VECCHIA sullo stesso ingresso deve dare NON zero** -- senno' il caso non discrimina: ### **FERMO** |
| **`C3`** | **scambio `i<->j` su tutti gli archi**: la decisa ### **identica al bit**, la vecchia ### **cambia segno**. ### **Se non discrimina: FERMO** |

### ✅ **`C2` HA DENTRO IL SUO CONTROLLO POSITIVO, ed e' la parte che conta:** uno zero puo'
venire da uno strumento che **non calcola niente**. Serve che la vecchia, sullo **stesso**
ingresso, dia **non zero**. ### **Senza quella meta', `C2` sarebbe un FALSO-ZERO.**

### ⚠ **`C1` PRETENDE L'IDENTITA' AL BIT, e lo dichiaro come rischio:** `proj` passa da
`np.sum` su un prodotto, e **l'ordine delle somme cambia gli ultimi bit**.
### ⛔ **Il mandato dice <<AL BIT>> e NON lo ammorbidisco:** se fallisce per `1e-16`, il
referto porta **il numero e la causa** a Luca. **Ammorbidire un controllo perche' ha fallito
e' il modo di non avere controlli.**

USO:
  python csv/_test_fork/_mem_hebb_verso.py
  python csv/_test_fork/_mem_hebb_verso.py --collaudo
  opzioni: --passi=N (default 150; il mandato chiede 72 e 150)

USCITA: `csv/_test_fork/_mem_hebb_verso/_mem_hebb_verso.json` + `_corsa.txt`.

# ESENTE-H-P3: la scena passa TUTTA dal CLI (`nmasse` e `sep` da `argv`), e la
#   configurazione INTERA si DICHIARA (`_cli_flag.dichiara_configurazione`). La COPIA
#   PATCHATA serve perche' `ii`, `jj`, `dirarc`, `I`, `Imed` e `proj` vivono SOLO dentro
#   `memoria_hebbiana_moto`: ricostruirli fuori sarebbe una SECONDA scrittura della stessa
#   legge, cioe' le <<due leggi>> che `9-ter` vieta.
"""
import ast
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
FUORI = os.path.join(RADICE, "csv", "_test_fork", "_mem_hebb_verso")
SIM = os.path.join(RADICE, "soliton_simulator.py")
PASSI = 150

P = []


def stampa(s=""):
    print(s)
    P.append(s)


def riga(c="-"):
    stampa(c * 104)


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def piattaforma():
    return {"python": platform.python_version(), "numpy": np.__version__,
            "sistema": platform.system() + " " + platform.release(),
            "macchina": platform.machine()}


# =============================================================== LE DUE FORME
# ### UNA SOLA DEFINIZIONE PER FORMA, usata SIA dalla misura SIA dai controlli.
#   Due copie divergerebbero, ed e' esattamente cio' che `9-ter` chiama <<due leggi>>.

def forma_vecchia(m, ii, jj, dirarc, I, Imed):
    """La forma DI OGGI (`:9132-9134`), ricalcolata a lato, riga per riga."""
    memedge = 0.5 * (m[ii] * (I[ii, None] / Imed) + m[jj] * (I[jj, None] / Imed))
    return np.sum(memedge * dirarc, axis=1)


def forma_decisa(m, ii, jj, dirarc, I, Imed):
    """LA FORMA DECISA DA LUCA: moto RELATIVO, con peso d'ARCO."""
    peso = 0.5 * (I[ii] + I[jj]) / Imed
    return peso * np.sum((m[jj] - m[ii]) * dirarc, axis=1)


def forma_peso_per_nodo(m, ii, jj, dirarc, I, Imed):
    """LA VARIANTE CHE IL MANDATO SCARTA, e si misura per MOSTRARE perche'.

    ### Il peso per NODO: `0.5*(m_j*I_j - m_i*I_i)/Imed . dir`. Sotto traslazione rigida
    resta `0.5*m*(I_j - I_i)/Imed . dir`, che ### **NON e' zero** perche' le `I` sono
    diverse. ### **Non e' una forma candidata: e' la prova che il peso va sull'ARCO.**
    """
    return np.sum((m[jj] * I[jj, None] - m[ii] * I[ii, None]) * 0.5 / Imed * dirarc,
                  axis=1)


def quantili(x):
    x = np.asarray(x, float)
    fin = x[np.isfinite(x)]
    if not len(fin):
        return {"n": 0, "non_finiti": int(len(x))}
    return {"n": int(len(fin)), "non_finiti": int(len(x) - len(fin)),
            "min": float(np.min(fin)), "mediana": float(np.median(fin)),
            "p99": float(np.percentile(fin, 99)), "max": float(np.max(fin))}


# =============================================================== LA PATCH
def copia_patchata():
    """Una COPIA del sorgente con TRE punti di registrazione.

    ### Ogni sostituzione si asserisce per se' e FALLISCE se l'ancora non e' unica
    ### (`P1-quater`); ancore ASCII, nessun escape.
    """
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    dst = os.path.join(FUORI, "_sim_mem_hebb.py")
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
        "import numpy as np" + NL
        + "_MIS = None   # [MISURA MEM-HEBB-VERSO] lo riempie lo strumento" + NL,
        "il gancio di modulo `_MIS`")

    # --- il sito di `d0`: PRIMA del taglio (tutti gli ingredienti) e DOPO il taglio
    uno("            proj = np.clip(proj, -passo_max, passo_max)" + NL,
        "            if _MIS is not None:" + NL
        + "                _MIS(self, 'd0_prima', ii=ii, jj=jj, dirarc=dirarc, I=I," + NL
        + "                     Imed=Imed, proj=proj, passo_max=passo_max, mask=mask)" + NL
        + "            proj = np.clip(proj, -passo_max, passo_max)" + NL
        + "            if _MIS is not None:" + NL
        + "                _MIS(self, 'd0_dopo', proj=proj)" + NL,
        "il sito di `d0`, attorno al taglio `passo_max`")

    # --- il sito della fase: PRIMA del taglio pi/4 e DOPO (con `ii`)
    uno("                    shift_fase_dinamico = np.clip(shift_fase_dinamico, "
        "-np.pi * 0.25, np.pi * 0.25)" + NL,
        "                    if _MIS is not None:" + NL
        + "                        _MIS(self, 'fase_prima', ii=ii, jj=jj," + NL
        + "                             shift=shift_fase_dinamico," + NL
        + "                             dir_laterale=dir_laterale)" + NL
        + "                    shift_fase_dinamico = np.clip(shift_fase_dinamico, "
        "-np.pi * 0.25, np.pi * 0.25)" + NL
        + "                    if _MIS is not None:" + NL
        + "                        _MIS(self, 'fase_dopo', ii=ii, shift=shift_fase_dinamico)"
        + NL,
        "il sito della FASE, attorno al taglio pi/4")

    io.open(dst, "w", encoding="utf-8", newline=NL).write(t)
    return dst, fatte


# =============================================================== IL RACCOGLITORE
class Raccoglitore(object):
    """Registra a ogni passo le due forme a lato, e i tre controlli."""

    def __init__(self, S):
        self.S = S
        self.passo = 0
        self.passi = []
        self.d0_attesa = None       # il `proj` vecchio che IO ricalcolo, post-taglio
        self.c1 = {"confronti": 0, "diversi": 0, "max_scarto": 0.0, "archi": 0,
                   "peggiore": None}
        self.c2 = {"confronti": 0, "decisa_non_zero": 0, "vecchia_zero": 0,
                   "max_decisa": 0.0, "min_vecchia_max": None, "archi": 0}
        self.c3 = {"confronti": 0, "decisa_diversa": 0, "vecchia_non_opposta": 0,
                   "max_scarto_decisa": 0.0, "max_scarto_vecchia": 0.0, "archi": 0}
        self.fase_prima = None

    def __call__(self, net, quando, **kw):
        getattr(self, "_" + quando)(net, **kw)

    # ----------------------------------------------------------- il sito di `d0`
    def _d0_prima(self, net, ii, jj, dirarc, I, Imed, proj, passo_max, mask):
        m = np.asarray(net.mem_mot)
        ii = np.asarray(ii)
        jj = np.asarray(jj)
        dirarc = np.asarray(dirarc, float)
        I = np.asarray(I, float)
        Imed = float(Imed)
        pm = float(passo_max)

        vecchia = forma_vecchia(m, ii, jj, dirarc, I, Imed)
        decisa = forma_decisa(m, ii, jj, dirarc, I, Imed)
        self.d0_attesa = np.clip(vecchia, -pm, pm)

        vc = np.clip(vecchia, -pm, pm)
        dc = np.clip(decisa, -pm, pm)
        # ### SATURO = il taglio MORDE, cioe' |proj| > passo_max PRIMA del taglio.
        sat_v = int(np.sum(np.abs(vecchia) > pm))
        sat_d = int(np.sum(np.abs(decisa) > pm))
        # ### IL SEGNO: si conta solo dove ENTRAMBE sono non nulle, perche' lo zero non
        #   ha segno e contarlo come <<cambio>> sarebbe un numero gonfiato.
        viva = (vecchia != 0.0) & (decisa != 0.0)
        segno_cambia = int(np.sum(viva & (np.sign(vecchia) != np.sign(decisa))))
        riga_passo = {
            "passo": self.passo, "archi": int(len(ii)), "passo_max": pm,
            "proj_simulatore_prima": quantili(np.abs(np.asarray(proj, float))),
            "vecchia_prima": quantili(np.abs(vecchia)),
            "decisa_prima": quantili(np.abs(decisa)),
            "saturi_vecchia": sat_v, "saturi_decisa": sat_d,
            "frazione_saturi_vecchia": (sat_v / len(ii)) if len(ii) else None,
            "frazione_saturi_decisa": (sat_d / len(ii)) if len(ii) else None,
            "segno_cambia": segno_cambia, "archi_vivi": int(np.sum(viva)),
            "frazione_segno_cambia": ((segno_cambia / int(np.sum(viva)))
                                      if int(np.sum(viva)) else None),
            # ### `SCALA_MIN_PASSO` acceso rende `_sd0` un PASSANTE (`:6754-6756`), quindi
            #   Delta d0 E' il `proj` post-taglio. Lo VERIFICO sul modulo e lo dichiaro:
            #   non chiamo `_sd0`, perche' incrementerebbe un contatore del simulatore.
            "somma_segnata_dd0_vecchia": float(np.sum(vc)),
            "somma_segnata_dd0_decisa": float(np.sum(dc)),
        }
        self.passi.append(riga_passo)
        self._controlli(m, ii, jj, dirarc, I, Imed, pm)

    def _d0_dopo(self, net, proj):
        """`C1`: la mia forma vecchia post-taglio contro quella del simulatore, AL BIT."""
        if self.d0_attesa is None:
            return
        att = self.d0_attesa
        self.d0_attesa = None
        vero = np.asarray(proj, float)
        self.c1["confronti"] += 1
        if vero.shape != att.shape:
            self.c1["diversi"] += 1
            self.c1["peggiore"] = {"passo": self.passo, "nota": "forme diverse",
                                   "vero": list(vero.shape), "atteso": list(att.shape)}
            return
        self.c1["archi"] += int(len(vero))
        ug = (vero == att) | (np.isnan(vero) & np.isnan(att))
        nd = int(np.sum(~ug))
        if nd:
            self.c1["diversi"] += 1
            sc = float(np.nanmax(np.abs(vero - att)))
            if sc > self.c1["max_scarto"]:
                self.c1["max_scarto"] = sc
                self.c1["peggiore"] = {"passo": self.passo, "archi_diversi": nd,
                                       "archi": int(len(vero)), "max_scarto": sc}

    def _controlli(self, m, ii, jj, dirarc, I, Imed, pm):
        """`C2` (traslazione rigida) e `C3` (scambio del verso), sui dati VERI del passo."""
        # --- C2: `mem_mot` sostituita da un VETTORE COSTANTE.
        # ### LA COSTANTE E' DERIVATA DALLO STATO, non scelta: il `mem_mot` del nodo di
        #   norma MASSIMA. Un vettore scelto da me sarebbe un numero nuovo (`A1`); e
        #   prendere il piu' grande e' la scelta che ### MENO rischia di degenerare.
        n = min(len(m), int(self.S.net.n) if hasattr(self.S, "net") else len(m))
        mm = np.asarray(m[:n], float)
        if not len(mm):
            return
        k = int(np.argmax(np.linalg.norm(mm, axis=1)))
        c = np.tile(mm[k], (len(m), 1))
        v_rig = forma_vecchia(c, ii, jj, dirarc, I, Imed)
        d_rig = forma_decisa(c, ii, jj, dirarc, I, Imed)
        self.c2["confronti"] += 1
        self.c2["archi"] += int(len(ii))
        mx_d = float(np.max(np.abs(d_rig))) if len(d_rig) else 0.0
        mx_v = float(np.max(np.abs(v_rig))) if len(v_rig) else 0.0
        if mx_d != 0.0:
            self.c2["decisa_non_zero"] += 1
        if mx_v == 0.0:
            self.c2["vecchia_zero"] += 1
        self.c2["max_decisa"] = max(self.c2["max_decisa"], mx_d)
        if self.c2["min_vecchia_max"] is None or mx_v < self.c2["min_vecchia_max"]:
            self.c2["min_vecchia_max"] = mx_v

        # --- C3: scambio `i<->j` su TUTTI gli archi. `dir(j->i) = -dir(i->j)`.
        v_sc = forma_vecchia(m, jj, ii, -dirarc, I, Imed)
        d_sc = forma_decisa(m, jj, ii, -dirarc, I, Imed)
        v_or = forma_vecchia(m, ii, jj, dirarc, I, Imed)
        d_or = forma_decisa(m, ii, jj, dirarc, I, Imed)
        self.c3["confronti"] += 1
        self.c3["archi"] += int(len(ii))
        sd = float(np.max(np.abs(d_sc - d_or))) if len(d_or) else 0.0
        sv = float(np.max(np.abs(v_sc + v_or))) if len(v_or) else 0.0
        if sd != 0.0:
            self.c3["decisa_diversa"] += 1
        if sv != 0.0:
            self.c3["vecchia_non_opposta"] += 1
        self.c3["max_scarto_decisa"] = max(self.c3["max_scarto_decisa"], sd)
        self.c3["max_scarto_vecchia"] = max(self.c3["max_scarto_vecchia"], sv)

    # ----------------------------------------------------------- il sito della fase
    def _fase_prima(self, net, ii, jj, shift, dir_laterale):
        self.fase_prima = {"shift": np.asarray(shift, float).copy(),
                           "dl_z": float(np.max(np.abs(np.asarray(dir_laterale)[:, 2])))}

    def _fase_dopo(self, net, ii, shift):
        pr = self.fase_prima
        self.fase_prima = None
        ii = np.asarray(ii)
        sh = np.asarray(shift, float)
        pre = pr["shift"] if pr is not None else sh
        taglio = float(np.pi * 0.25)
        # ### <<L'ULTIMO VINCE>>: con `phi[ii] = ...` e `ii` CHE CONTIENE RIPETIZIONI,
        #   numpy applica, per ogni nodo, SOLO l'ULTIMA occorrenza nell'array.
        #   Si trova senza indovinare: l'ultima occorrenza di ogni valore di `ii`.
        ultimo = {}
        for pos, nodo in enumerate(ii.tolist()):
            ultimo[nodo] = pos
        applicati = np.zeros(len(ii), bool)
        applicati[np.fromiter(ultimo.values(), int, len(ultimo))] = True
        scartati = ~applicati
        d = {"passo": self.passo, "archi": int(len(ii)),
             "nodi_primo_estremo": int(len(ultimo)),
             "contributi_scartati": int(np.sum(scartati)),
             "contributi_applicati": int(np.sum(applicati)),
             "somma_moduli_scartati": float(np.sum(np.abs(sh[scartati]))),
             "somma_moduli_applicati": float(np.sum(np.abs(sh[applicati]))),
             "shift_assoluto": quantili(np.abs(sh)),
             "saturati_pi4": int(np.sum(np.abs(pre) > taglio)),
             "frazione_saturati_pi4": ((float(np.sum(np.abs(pre) > taglio)) / len(ii))
                                       if len(ii) else None),
             "dir_laterale_z_max": pr["dl_z"] if pr is not None else None}
        # ### i nodi con PIU' DI UN ARCO come primo estremo: si contano sulle ripetizioni.
        conte = np.bincount(ii)
        d["nodi_con_piu_di_un_arco"] = int(np.sum(conte > 1))
        d["max_archi_su_un_nodo"] = int(np.max(conte)) if len(conte) else 0
        self.passi[-1]["fase"] = d if self.passi else None
        if not self.passi:
            self.passi.append({"passo": self.passo, "fase": d})


# =============================================================== IL CENSIMENTO AST
def censimento_ast(path, S):
    """`(c)`: il sito (2) gira DAVVERO nella configurazione del driver?"""
    src = io.open(path, encoding="utf-8").read()
    albero = ast.parse(src)
    siti = []
    for nodo in ast.walk(albero):
        if isinstance(nodo, ast.If):
            nomi = sorted({x.id for x in ast.walk(nodo.test) if isinstance(x, ast.Name)})
            if "MEM_MOTO_TUTTO" in nomi or "MEM_MOTO" in nomi:
                siti.append({"riga": nodo.lineno, "flag_nel_test": nomi})
    fuori = {"siti_con_MEM_MOTO": siti, "quanti": len(siti)}
    for f in ["MEM_MOTO", "MEM_MOTO_TUTTO", "MEM_HEBB", "SCALA_MIN_PASSO", "SCALA_MIN",
              "TRACCIA_D0", "K_FRANGE"]:
        fuori[f] = (bool(getattr(S, f)) if isinstance(getattr(S, f, None), bool)
                    else getattr(S, f, None))
    return fuori


# =============================================================== IL COLLAUDO
def collaudo():
    riga("=")
    stampa("IL COLLAUDO: i casi costruiti, dove la risposta e' NOTA PRIMA")
    riga("=")
    rng = np.random.default_rng(7)
    N, M = 40, 120
    pos = rng.normal(size=(N, 3))
    m = rng.normal(size=(N, 3))
    I = np.abs(rng.normal(size=N)) + 0.1
    Imed = float(np.median(I))
    ii = rng.integers(0, N, M)
    jj = rng.integers(0, N, M)
    ok = ii != jj
    ii, jj = ii[ok], jj[ok]
    v = pos[jj] - pos[ii]
    d = v / np.linalg.norm(v, axis=1, keepdims=True)
    esiti = []

    def caso(et, val, atteso, zero):
        ok2 = (val == 0.0) if zero else (val != 0.0)
        esiti.append((et, val, atteso, ok2))
        stampa("  %-54s %-13.6e  atteso %-12s %s"
               % (et, val, atteso, "OK" if ok2 else "### NO"))

    caso("(1) scambio i<->j: max|decisa(i,j) - decisa(j,i)|",
         float(np.max(np.abs(forma_decisa(m, jj, ii, -d, I, Imed)
                             - forma_decisa(m, ii, jj, d, I, Imed)))),
         "0 esatto", True)
    caso("(2) scambio i<->j: max|vecchia(i,j) + vecchia(j,i)|",
         float(np.max(np.abs(forma_vecchia(m, jj, ii, -d, I, Imed)
                             + forma_vecchia(m, ii, jj, d, I, Imed)))),
         "0 esatto", True)
    caso("(3) scambio i<->j: max|vecchia(i,j) - vecchia(j,i)|  DISCRIMINA",
         float(np.max(np.abs(forma_vecchia(m, jj, ii, -d, I, Imed)
                             - forma_vecchia(m, ii, jj, d, I, Imed)))),
         "NON zero", False)
    c = np.tile(rng.normal(size=3), (N, 1))
    caso("(4) traslazione rigida: max|decisa|",
         float(np.max(np.abs(forma_decisa(c, ii, jj, d, I, Imed)))), "0 esatto", True)
    caso("(5) traslazione rigida: max|vecchia|   IL POSITIVO",
         float(np.max(np.abs(forma_vecchia(c, ii, jj, d, I, Imed)))), "NON zero", False)
    caso("(6) traslazione rigida, PESO PER NODO: max|proj|",
         float(np.max(np.abs(forma_peso_per_nodo(c, ii, jj, d, I, Imed)))),
         "NON zero", False)
    stampa()
    stampa("  ### IL (6) E' LA PROVA CHE IL PESO VA SULL'ARCO, e non una forma candidata:")
    stampa("      col peso per NODO la traslazione rigida resta 0.5*m*(I_j - I_i)/Imed . dir,")
    stampa("      che NON e' zero perche' le I sono diverse. Il mandato lo afferma; qui si")
    stampa("      misura.")
    stampa()

    # --- <<l'ultimo vince>>, su un caso dove la risposta si conta a mano
    iiq = np.array([0, 1, 0, 2, 0, 1])
    shq = np.array([1.0, 2.0, 4.0, 8.0, 16.0, 32.0])
    ultimo = {}
    for pos2, nodo in enumerate(iiq.tolist()):
        ultimo[nodo] = pos2
    app = np.zeros(len(iiq), bool)
    app[list(ultimo.values())] = True
    sc_at, ap_at = 1.0 + 4.0 + 2.0, 16.0 + 32.0 + 8.0
    sc, ap = float(np.sum(shq[~app])), float(np.sum(shq[app]))
    stampa("  (7) <<l'ultimo vince>> su ii = [0,1,0,2,0,1], shift = [1,2,4,8,16,32]")
    stampa("      applicati  %6.1f   atteso %6.1f   %s"
           % (ap, ap_at, "OK" if ap == ap_at else "### NO"))
    stampa("      scartati   %6.1f   atteso %6.1f   %s"
           % (sc, sc_at, "OK" if sc == sc_at else "### NO"))
    stampa("      nodi con piu' di un arco: %d   atteso 2   %s"
           % (int(np.sum(np.bincount(iiq) > 1)),
              "OK" if int(np.sum(np.bincount(iiq) > 1)) == 2 else "### NO"))
    esiti.append(("(7) l'ultimo vince", ap, "16+32+8", ap == ap_at and sc == sc_at))
    stampa()
    quanti = sum(1 for e in esiti if e[3])
    stampa("  COLLAUDO: %d casi su %d tornano." % (quanti, len(esiti)))
    if quanti != len(esiti):
        raise SystemExit("[FERMO] il collaudo NON torna: lo strumento non si usa.")
    # --- le ancore della patch
    dst, fatte = copia_patchata()
    stampa("  la patch: %d ancore, tutte UNICHE  (copia %s)" % (len(fatte), blob(dst)[:8]))
    for f in fatte:
        stampa("      - " + f)
    return 0


# =============================================================== LA CORSA
def corsa(passi):
    riga("=")
    stampa("MEM-HEBB-VERSO passo (1): LA FORMA DI `proj` E IL SITO DELLA FASE, A LATO")
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
        S, a = _cli_flag.carica_dal_cli(list(argv), nome="sim_mem_hebb", sim=dst)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    net = S.net

    # ### LA CONFIGURAZIONE INTERA (`H-P5`): non i flag toccati, TUTTI. E nessuno dei due
    #   strumenti fratelli la dichiarava -- e' la lacuna `SIGILLO-SENZA-CONFIGURAZIONE`,
    #   che qui NON si ripete.
    in_conf = _cli_flag.dichiara_configurazione(S, stampa)

    R = Raccoglitore(S)
    S._MIS = R

    cens = censimento_ast(dst, S)
    riga()
    stampa("(c) IL CENSIMENTO DALL'AST: il sito (2) gira nella configurazione del driver?")
    riga()
    stampa("  siti il cui `if` nomina MEM_MOTO o MEM_MOTO_TUTTO: %d" % cens["quanti"])
    for s in cens["siti_con_MEM_MOTO"]:
        stampa("      riga %-6d test su %s" % (s["riga"], ", ".join(s["flag_nel_test"])))
    for f in ["MEM_HEBB", "MEM_MOTO", "MEM_MOTO_TUTTO", "SCALA_MIN_PASSO", "SCALA_MIN",
              "TRACCIA_D0", "K_FRANGE"]:
        stampa("  %-18s %s" % (f, cens.get(f)))
    gira = bool(cens.get("MEM_HEBB")) and bool(cens.get("MEM_MOTO_TUTTO"))
    stampa("  ### IL SITO (2) GIRA DAVVERO: %s   (serve MEM_HEBB e MEM_MOTO_TUTTO)" % gira)
    stampa("  ### E `SCALA_MIN_PASSO` = %s: con acceso, `_sd0` e' un PASSANTE (`:6754`),"
           % cens.get("SCALA_MIN_PASSO"))
    stampa("      quindi Delta d0 E' il `proj` post-taglio. NON chiamo `_sd0`: incrementerebbe")
    stampa("      un contatore del simulatore, e una misura non muove cio' che misura.")
    stampa("  scena: nmasse=%s sep=%s  ->  n = %d, archi = %d"
           % (getattr(a, "nmasse", "?"), getattr(a, "sep", "?"), net.n, len(net.i)))
    stampa()

    riga("=")
    stampa("IL RUN: %d passi, col BATTITO per passo" % passi)
    riga("=")
    for k in range(1, passi + 1):
        R.passo = k
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(S, net)
        ult = R.passi[-1] if R.passi else {}
        print("[battito] passo %d/%d  n=%d archi=%d sat_vecchia=%s sat_decisa=%s"
              % (k, passi, net.n, len(net.i),
                 ult.get("frazione_saturi_vecchia"), ult.get("frazione_saturi_decisa")),
              flush=True)
    stampa("  passi girati: %d   n finale = %d, archi = %d" % (passi, net.n, len(net.i)))
    stampa("  passi con il sito di `d0` registrato: %d" % len(R.passi))
    con_fase = [p for p in R.passi if p.get("fase")]
    stampa("  passi con il sito della FASE registrato: %d" % len(con_fase))
    if not R.passi:
        stampa("  ### ATTENZIONE: nessun passo registrato. Un referto di zeri qui NON")
        stampa("      significa <<non c'e' differenza>>: significa che la misura NON e'")
        stampa("      avvenuta. LO DICO invece di riportare zeri.")
    stampa()

    agg = aggrega(R, con_fase)
    rapporto(R, agg, cens, in_conf)

    fuori = {"piattaforma": pf, "blob_sim": blob(SIM), "blob_copia": blob(dst),
             "ancore_patch": fatte, "passi": passi,
             "in_configurazione_del_driver": bool(in_conf),
             "scena": {"nmasse": getattr(a, "nmasse", None),
                       "sep": getattr(a, "sep", None),
                       "n_finale": int(net.n), "archi_finali": int(len(net.i))},
             "censimento_ast": cens, "per_passo": R.passi, "aggregati": agg,
             "controlli": {"C1": R.c1, "C2": R.c2, "C3": R.c3},
             "timbro_strumento": _timbro()}
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    jp = os.path.join(FUORI, "_mem_hebb_verso.json")
    io.open(jp, "w", encoding="utf-8", newline=NL).write(
        json.dumps(fuori, indent=1, sort_keys=True, default=str))
    stampa("scritto: " + jp)
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(P) + NL)
    return 0


def _timbro():
    t = getattr(_presidio, "timbro", None)
    if t is None:
        return {"nota": "il presidio non espone `timbro`"}
    try:
        d = t(__file__)
        return d if isinstance(d, dict) else {"timbro": str(d)}
    except Exception as e:
        return {"nota": "timbro non leggibile: %r" % (e,)}


def aggrega(R, con_fase):
    """Gli aggregati su tutti i passi. Le frazioni si pesano sugli ARCHI, non sui passi."""
    pa = R.passi
    if not pa:
        return {}
    archi = float(sum(p["archi"] for p in pa))
    def somma(k):
        return float(sum(p.get(k) or 0 for p in pa))
    out = {
        "passi_registrati": len(pa), "archi_passo_totali": int(archi),
        "saturi_vecchia": int(somma("saturi_vecchia")),
        "saturi_decisa": int(somma("saturi_decisa")),
        "frazione_saturi_vecchia": (somma("saturi_vecchia") / archi) if archi else None,
        "frazione_saturi_decisa": (somma("saturi_decisa") / archi) if archi else None,
        "archi_vivi": int(somma("archi_vivi")),
        "segno_cambia": int(somma("segno_cambia")),
        "frazione_segno_cambia": ((somma("segno_cambia") / somma("archi_vivi"))
                                  if somma("archi_vivi") else None),
        "somma_segnata_dd0_vecchia": somma("somma_segnata_dd0_vecchia"),
        "somma_segnata_dd0_decisa": somma("somma_segnata_dd0_decisa"),
        "passo_max_min": float(min(p["passo_max"] for p in pa)),
        "passo_max_max": float(max(p["passo_max"] for p in pa)),
    }
    for et, k in [("vecchia", "vecchia_prima"), ("decisa", "decisa_prima"),
                  ("simulatore", "proj_simulatore_prima")]:
        med = [p[k]["mediana"] for p in pa if p[k].get("n")]
        mx = [p[k]["max"] for p in pa if p[k].get("n")]
        p99 = [p[k]["p99"] for p in pa if p[k].get("n")]
        mn = [p[k]["min"] for p in pa if p[k].get("n")]
        out["abs_proj_" + et] = {
            "mediana_delle_mediane": float(np.median(med)) if med else None,
            "min_dei_min": float(min(mn)) if mn else None,
            "mediana_dei_p99": float(np.median(p99)) if p99 else None,
            "max_dei_max": float(max(mx)) if mx else None}
    if con_fase:
        f = [p["fase"] for p in con_fase]
        tot = float(sum(x["archi"] for x in f))
        out["fase"] = {
            "passi": len(f), "archi_passo_totali": int(tot),
            "nodi_con_piu_di_un_arco_min": int(min(x["nodi_con_piu_di_un_arco"] for x in f)),
            "nodi_con_piu_di_un_arco_max": int(max(x["nodi_con_piu_di_un_arco"] for x in f)),
            "max_archi_su_un_nodo": int(max(x["max_archi_su_un_nodo"] for x in f)),
            "contributi_scartati": int(sum(x["contributi_scartati"] for x in f)),
            "contributi_applicati": int(sum(x["contributi_applicati"] for x in f)),
            "frazione_scartati": (float(sum(x["contributi_scartati"] for x in f)) / tot)
                                 if tot else None,
            "somma_moduli_scartati": float(sum(x["somma_moduli_scartati"] for x in f)),
            "somma_moduli_applicati": float(sum(x["somma_moduli_applicati"] for x in f)),
            "saturati_pi4": int(sum(x["saturati_pi4"] for x in f)),
            "frazione_saturati_pi4": (float(sum(x["saturati_pi4"] for x in f)) / tot)
                                     if tot else None,
            "dir_laterale_z_max": float(max(x["dir_laterale_z_max"] or 0.0 for x in f)),
            "shift_mediana_delle_mediane": float(np.median(
                [x["shift_assoluto"]["mediana"] for x in f
                 if x["shift_assoluto"].get("n")])) if f else None,
            "shift_max_dei_max": float(max(
                [x["shift_assoluto"]["max"] for x in f
                 if x["shift_assoluto"].get("n")] or [0.0])),
        }
    return out


def rapporto(R, agg, cens, in_conf):
    if not agg:
        return
    riga("=")
    stampa("(a) `d0`: LA FORMA VECCHIA CONTRO LA FORMA DECISA")
    riga("=")
    stampa("  passi registrati: %d   archi-passo: %d"
           % (agg["passi_registrati"], agg["archi_passo_totali"]))
    stampa("  ### E IL NUMERO SI DICHIARA: zero archi NON e' un'identita'.")
    stampa()
    stampa("  distribuzione di |proj| PRIMA del taglio, aggregata sui passi")
    stampa("  %-12s %-14s %-14s %-14s %-14s" % ("forma", "min dei min", "mediana",
                                                "mediana p99", "max dei max"))
    for et in ["simulatore", "vecchia", "decisa"]:
        q = agg["abs_proj_" + et]
        stampa("  %-12s %-14.6e %-14.6e %-14.6e %-14.6e"
               % (et, q["min_dei_min"] or 0.0, q["mediana_delle_mediane"] or 0.0,
                  q["mediana_dei_p99"] or 0.0, q["max_dei_max"] or 0.0))
    stampa()
    stampa("  il taglio passo_max = 0.01*mediana(d0):  da %.6e a %.6e"
           % (agg["passo_max_min"], agg["passo_max_max"]))
    stampa("  archi SATURI (|proj| > passo_max PRIMA del taglio)")
    stampa("      forma vecchia  %12d su %d   frazione %s"
           % (agg["saturi_vecchia"], agg["archi_passo_totali"],
              _f(agg["frazione_saturi_vecchia"])))
    stampa("      forma decisa   %12d su %d   frazione %s"
           % (agg["saturi_decisa"], agg["archi_passo_totali"],
              _f(agg["frazione_saturi_decisa"])))
    stampa()
    stampa("  il SEGNO cambia fra le due forme: %d su %d archi VIVI   frazione %s"
           % (agg["segno_cambia"], agg["archi_vivi"], _f(agg["frazione_segno_cambia"])))
    stampa("      (<<vivi>> = entrambe non nulle: lo zero non ha segno, e contarlo come")
    stampa("       cambio gonfierebbe il numero)")
    stampa()
    stampa("  somma CON SEGNO di Delta d0, su tutti i passi")
    stampa("      forma vecchia  %+.6e" % agg["somma_segnata_dd0_vecchia"])
    stampa("      forma decisa   %+.6e" % agg["somma_segnata_dd0_decisa"])
    stampa()

    if "fase" in agg:
        f = agg["fase"]
        riga("=")
        stampa("(b) LA FASE: <<l'ultimo vince>>, il taglio pi/4 e l'asse z")
        riga("=")
        stampa("  passi col sito registrato: %d   archi-passo: %d"
               % (f["passi"], f["archi_passo_totali"]))
        stampa("  nodi con PIU' DI UN ARCO come primo estremo: da %d a %d per passo"
               % (f["nodi_con_piu_di_un_arco_min"], f["nodi_con_piu_di_un_arco_max"]))
        stampa("  il massimo di archi su UN solo nodo: %d" % f["max_archi_su_un_nodo"])
        stampa()
        stampa("  CONTRIBUTI SCARTATI da <<l'ultimo vince>>")
        stampa("      scartati   %12d   applicati %12d   frazione scartati %s"
               % (f["contributi_scartati"], f["contributi_applicati"],
                  _f(f["frazione_scartati"])))
        stampa("      somma dei MODULI:  scartati %.6e   applicati %.6e"
               % (f["somma_moduli_scartati"], f["somma_moduli_applicati"]))
        rap = (f["somma_moduli_scartati"] / f["somma_moduli_applicati"]
               if f["somma_moduli_applicati"] else None)
        stampa("      rapporto scartati/applicati: %s" % _f(rap))
        stampa()
        stampa("  |shift|: mediana delle mediane %.6e   max dei max %.6e"
               % (f["shift_mediana_delle_mediane"] or 0.0, f["shift_max_dei_max"]))
        stampa("  saturati dal taglio pi/4 (%.6f): %d su %d   frazione %s"
               % (np.pi * 0.25, f["saturati_pi4"], f["archi_passo_totali"],
                  _f(f["frazione_saturati_pi4"])))
        stampa()
        stampa("  la terza componente di `dir_laterale`, in modulo massimo: %.6e"
               % f["dir_laterale_z_max"])
        stampa("      ### E' ZERO PER COSTRUZIONE (`np.zeros_like`), e il numero lo conferma:")
        stampa("          la direzione trasversale sta SEMPRE nel piano xy del LABORATORIO,")
        stampa("          mentre i nodi stanno in 3D. E' `FASE-TRASCINAMENTO-3D`.")
        stampa()

    riga("=")
    stampa("I TRE CONTROLLI CHE POSSONO FALLIRE")
    riga("=")
    c1, c2, c3 = R.c1, R.c2, R.c3
    stampa("  C1  la mia forma VECCHIA post-taglio contro il `proj` del simulatore, AL BIT")
    stampa("      confronti %d   con DIFFERENZE %d   archi confrontati %d   max scarto %.3e"
           % (c1["confronti"], c1["diversi"], c1["archi"], c1["max_scarto"]))
    if c1["peggiore"]:
        stampa("      il peggiore: %s" % (c1["peggiore"],))
    stampa()
    stampa("  C2  traslazione rigida (`mem_mot` = il vettore del nodo di norma MASSIMA)")
    stampa("      confronti %d   la DECISA non e' zero in %d   max|decisa| %.3e"
           % (c2["confronti"], c2["decisa_non_zero"], c2["max_decisa"]))
    stampa("      IL POSITIVO: la VECCHIA e' zero in %d   il MINIMO dei suoi max %s"
           % (c2["vecchia_zero"], _f(c2["min_vecchia_max"])))
    stampa()
    stampa("  C3  scambio i<->j su TUTTI gli archi")
    stampa("      la DECISA differisce in %d   max scarto %.3e"
           % (c3["decisa_diversa"], c3["max_scarto_decisa"]))
    stampa("      la VECCHIA non e' opposta in %d   max|v(i,j)+v(j,i)| %.3e"
           % (c3["vecchia_non_opposta"], c3["max_scarto_vecchia"]))
    stampa()
    guasti = []
    if c1["confronti"] == 0:
        guasti.append("C1 non ha mai confrontato: zero confronti NON e' un'identita'")
    if c1["diversi"]:
        guasti.append("C1: la mia forma vecchia NON coincide al bit in %d passi su %d "
                      "(max scarto %.3e)" % (c1["diversi"], c1["confronti"],
                                             c1["max_scarto"]))
    if c2["confronti"] == 0:
        guasti.append("C2 non ha mai confrontato")
    if c2["decisa_non_zero"]:
        guasti.append("C2: la forma DECISA non da' zero sotto traslazione rigida in %d "
                      "passi (max %.3e)" % (c2["decisa_non_zero"], c2["max_decisa"]))
    if c2["vecchia_zero"]:
        guasti.append("C2: la forma VECCHIA da' ZERO sotto traslazione rigida in %d "
                      "passi: IL CASO NON DISCRIMINA" % c2["vecchia_zero"])
    if c3["confronti"] == 0:
        guasti.append("C3 non ha mai confrontato")
    if c3["decisa_diversa"]:
        guasti.append("C3: la forma DECISA non e' identica al bit sotto scambio in %d "
                      "passi (max %.3e)" % (c3["decisa_diversa"], c3["max_scarto_decisa"]))
    if c3["vecchia_non_opposta"]:
        guasti.append("C3: la forma VECCHIA non cambia segno esattamente in %d passi "
                      "(max %.3e)" % (c3["vecchia_non_opposta"], c3["max_scarto_vecchia"]))
    if not in_conf:
        guasti.append("la configurazione NON e' quella del driver: la misura e' di un "
                      "ALTRO sistema")
    if guasti:
        stampa("  ### I CONTROLLI NON PASSANO, e mi FERMO. Che cosa non torna:")
        for g in guasti:
            stampa("      - " + g)
        stampa()
        stampa("  ### NON AMMORBIDISCO IL CONTROLLO: il mandato dice AL BIT, e un controllo")
        stampa("      ammorbidito perche' ha fallito non e' un controllo.")
        riga("=")
        return 1
    stampa("  ### I TRE CONTROLLI PASSANO: la forma vecchia coincide AL BIT col simulatore")
    stampa("      su %d archi, la decisa e' ZERO ESATTO sotto traslazione rigida mentre la"
           % c1["archi"])
    stampa("      vecchia NON lo e', e sotto scambio i<->j la decisa e' identica al bit")
    stampa("      mentre la vecchia cambia segno ESATTAMENTE.")
    riga("=")
    return 0


def _f(x):
    return "n/d" if x is None else ("%.6f" % x)


def main(argv):
    passi = PASSI
    for a in argv[1:]:
        if a.startswith("--passi="):
            passi = int(a.split("=", 1)[1])
    if "--collaudo" in argv[1:]:
        r = collaudo()
    else:
        r = corsa(passi)
    return r


if __name__ == "__main__":
    sys.exit(main(sys.argv) or 0)
