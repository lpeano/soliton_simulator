# -*- coding: utf-8 -*-
"""`CRESCITA-DOPO-Z43`: **perche' la rete quasi non cresce piu'** con `r = cs/CS_M`.

*(Mandato di Luca del 2026-10-05. I **cancelli**, i **quattro controlli** e la
**STELLA POLARE** sono fissati in
`doc/TASK_HISTORY/2026-10-05_crescita-dopo-z43-misura.md`, committato **prima**
in `9a11cda`.)*

### IL FATTO DA SPIEGARE
Al passo `150`: `n = 12827` nella `PARTE B` contro **`14328`** nella `PARTE A`, da `12802`.
### **~25 nascite contro ~1500**, e nella `PARTE B` concentrate in **13 passi su 150**.
### ⚠ **E il rallentamento uniforme NON lo spiega:** `r` mediano `0.815`, e il fattore di
tempo entra nella probabilita' **una volta sola**, quindi gli eventi attesi scalano di
`~0.815`. ### **Un fattore `0.815` non fa un fattore `~60`.**

### LA CATENA DEI CANCELLI, **censita dal sorgente e in ordine**
| # | il cancello | che cosa lo chiude |
|--:|---|---|
| `0` | `if not len(self.tw)` | rete senza archi |
| — | **la MODULAZIONE:** `soglia = soglia0*(1 - 0.3*tanh(|r_i - r_j|))` | ### **e' l'ipotesi** |
| `1` | **sopra soglia:** `max(avv/soglia - 1, 0)` | `avv <= soglia` |
| `2` | **sotto `4pi`:** `clip(1 - avv/4pi, 0, 1)` | `avv >= 4pi` |
| `3` | **segno di CREAZIONE:** `-tanh(3*(pos_torsione - centro))` | `segno <= 0` (repulsivo) |
| — | `ampiezza = salita*discesa*_ft`, `_ft = dt_e/DT` | ### **il rallentamento uniforme** |
| `4` | **l'estrazione:** `1 - exp(-max(resp,0))` contro `rng` | il dado |
| `5` | il tetto `MITMAX` | ### **inerte: `MITMAX = 0`** |
| `6` | la densita': `0.5*(I[a]+I[b]) >= QMIN_M*median(peq)` | ### **`QMIN_M = 0.000`** |
| `7` | `A13`/`2LAM`: `FRAZ*d >= LAM` **e** `(1-FRAZ)*d >= LAM` | archi corti |

> ### 📌 **DUE CANCELLI SONO DICHIARATI QUASI-INERTI *PRIMA* DI MISURARLI** -- `MITMAX = 0`
> *(`:3065`)* e `QMIN_M = 0.000` *(`:3058`)*, che rende il `6` sempre vero per densita' non
> negative. ### **Si misurano comunque** *(un cancello che credo inerte e non misuro e' un
> cancello che non so)*, ### **ma dichiararlo prima e' l'unico modo di non spacciarlo per
> una scoperta dopo.**

### I TRE BRACCI CHE GIRANO
| | | |
|---|---|---|
| **`Ap`** | la `PARTE A` patchata | dal tag `pre-z43-cura2-r-da-cs`, blob `062172d3` |
| **`Bp`** | la `PARTE B` patchata | il simulatore di oggi, `f7237563` |
| **`Bc`** | il **CONTROFATTUALE**, ### **dichiarato FINTO** | `r` moltiplicato per `1/mediana(r)` |

### ⚠ **IL CONTROFATTUALE: <<GRADIENTI INTATTI>> NON E' LETTERALMENTE VERO**
Riscalare `r` per `1/mediana(r) ~ 1.227` moltiplica **anche** `|r_i - r_j|` per `1.227`:
### **il gradiente CRESCE del 23 %.** ### ✔ **E questo rende il controfattuale CONSERVATIVO
nella direzione giusta:** un gradiente maggiorato **abbassa** la soglia, cioe' spinge le
nascite **verso l'alto**. Se restano basse **nonostante** questo, la conclusione *<<non e' il
rallentamento>>* e' **piu' forte**. ### **Se risalgono, quel `23 %` e' una causa confondente
e lo dico.** ### **Applico la prescrizione di Luca alla lettera e ne dichiaro il limite.**

### I QUATTRO CONTROLLI CHE POSSONO FALLIRE
| | | se fallisce |
|---|---|---|
| **`C1`** | `somma(ammessi) + _g_nati_schwinger` **==** `n_fin - n_0`, in **ciascun** braccio | ### **FERMO** |
| **`C2`** | zero candidati non e' un confronto | si **dichiara** |
| **`C3`** | i ganci non cambiano la fisica: `n` e archi finali **==** quelli del **sigillo committato** | ### **FERMO** |
| **`C4`** | la separazione cade su **UN** cancello nominato | si **riporta quale** |

### ✔ **`C3` SI VERIFICA CONTRO NUMERI GIA' COMMITTATI, non contro due bracci nudi in piu':**
il `sigillo.json` della `PARTE B` *(`5a2ddd9`)* porta `n_A = 14328`, `n_B = 12827`,
`archi_A = 473397`, `archi_B = 471596`. ### **E' un confronto fra DUE CORSE DIVERSE, quindi
piu' forte di un auto-confronto** -- e costa zero.

# ESENTE-H-P3: le COPIE PATCHATE servono perche' `grad_modula`, `soglia`, `ecc`, `salita`,
#   `discesa`, `_ft`, `segno`, `prob`, `nasce`, `c`, `ok`, `_no_dens`, `_no_lam` sono LOCALI
#   di `decidi_divisione`, e `_dt_e_ultimo` viene RISCRITTO nello stesso passo: da fuori non
#   si possono leggere. Ricalcolarli sarebbe una SECONDA scrittura della stessa legge
#   (`9-ter`), ed e' l'errore che la PARTE B ha gia' pagato (`aafb3eb`). La scena passa TUTTA
#   dal CLI e la configurazione INTERA si DICHIARA.

USO:  python csv/_test_fork/_crescita_dopo_z43.py  [--passi=N]  [--collaudo]
"""
import contextlib
import hashlib
import io
import json
import os
import platform
import subprocess
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
FUORI = os.path.join(RADICE, "csv", "_test_fork", "_crescita_dopo_z43")
SIM = os.path.join(RADICE, "soliton_simulator.py")
TAG = "pre-z43-cura2-r-da-cs"
SIGILLO_B = os.path.join(RADICE, "csv", "_seal_fork", "_sigillo_z43_cura2", "sigillo.json")
PASSI = 150
TW_TETTO = 4.0 * np.pi
# ### IL PASSO A CUI SI SALVANO LE DISTRIBUZIONI PIENE, scelto QUI e non dai dati: `10` sta
#   DOPO il raccordo (i passi con `r = 1` per sicurezza) e PRIMA della prima nascita della
#   `PARTE B` (misurata al passo `99` nel sigillo), quindi la rete NON e' ancora cresciuta.
PASSO_DIST = 10
QUANTILI = (0, 1, 5, 25, 50, 75, 95, 99, 100)

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


def q(v):
    """I quantili di un vettore, o `None` se e' vuoto. ### Si riporta la FORMA, non un
    numero solo: una mediana non distingue una distribuzione ripida da una piatta."""
    a = np.asarray(v, float)
    a = a[np.isfinite(a)]
    if not a.size:
        return None
    return {("q%03d" % k): float(np.quantile(a, k / 100.0)) for k in QUANTILI}


# =============================================================== LA COPIA PATCHATA
def copia_patchata(sorgente, dst, controfattuale=False):
    """`TRE` ganci che **LEGGONO** i valori che la legge ha calcolato, piu' -- solo nel
    braccio `Bc` -- **il riscalamento DICHIARATO FINTO** di `r`.

    ### Ogni ancora si **CONTA** e deve essere **UNICA** (`P1-quater`): se non lo e', si
    ### ferma e non scrive niente.
    """
    t = io.open(sorgente, encoding="utf-8").read()
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
        + "_MIS = None   # [CRESCITA-DOPO-Z43] lo riempie lo strumento" + NL,
        "il gancio di modulo `_MIS`")
    # --- H1: la MODULAZIONE della soglia (l'ipotesi del guardiano)
    uno("            soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_modula))" + NL,
        "            soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_modula))" + NL
        + "            if _MIS is not None:" + NL
        + "                _MIS.modulazione(self, rn=_rn, grad=grad_modula," + NL
        + "                                 soglia0=soglia0, soglia=soglia)" + NL,
        "H1: la modulazione della soglia dal gradiente di `r`")
    # --- H2: tutta la catena fino all'estrazione
    uno("        c = np.where(nasce)[0]" + NL,
        "        if _MIS is not None:" + NL
        + "            _MIS.catena(self, avv=avv, soglia=soglia, ecc=ecc, salita=salita," + NL
        + "                        discesa=discesa, ft=_ft, segno=segno, resp=resp," + NL
        + "                        prob=prob, nasce=nasce)" + NL
        + "        c = np.where(nasce)[0]" + NL,
        "H2: la catena dei cancelli fino all'estrazione")
    # --- H3: i due cancelli finali (densita' e `2LAM`)
    uno("            ok = ok & _conforme" + NL,
        "            if _MIS is not None:" + NL
        + "                _MIS.finali(self, c=c, ok=ok, no_dens=_no_dens," + NL
        + "                            no_lam=_no_lam, I=I, dc=_dc)" + NL
        + "            ok = ok & _conforme" + NL,
        "H3: i cancelli della densita' e di `2LAM`")
    if controfattuale:
        # ### IL BRACCIO `Bc`, DICHIARATO FINTO: `r` moltiplicato per `1/mediana(r)`. Si
        #   applica SUBITO DOPO che `ritmo()` ha restituito `r`, cosi' TUTTO cio' che sta a
        #   valle (`dt_n`, `dt_e`, il gradiente della mitosi) vede `r` riscalato.
        #   ⚠ E il gradiente CRESCE del 23 %: non resta intatto. Dichiarato nella docstring.
        uno("            self._r_corrente = r" + NL,
            "            if r is not None and np.ndim(r) and len(np.atleast_1d(r)):" + NL
            + "                _m = float(np.median(np.asarray(r, float)))" + NL
            + "                if _m > 0.0:" + NL
            + "                    r = np.asarray(r, float) / _m" + NL
            + "                    if _MIS is not None:" + NL
            + "                        _MIS.riscalato(_m)" + NL
            + "            self._r_corrente = r" + NL,
            "Bc: il riscalamento DICHIARATO FINTO di `r`")
    io.open(dst, "w", encoding="utf-8", newline=NL).write(t)
    return fatte


class Misura(object):
    """Accumula i conteggi dei cancelli e le distribuzioni. ### **LEGGE: non ricalcola.**"""

    def __init__(self, nome):
        self.nome = nome
        self.passo = 0
        self.passi = []
        self._mod = None
        self._cat = None
        self.riscalamenti = []
        # i valori dei CANDIDATI, accumulati su tutta la corsa (sono pochi)
        self.cand_grad = []
        self.cand_ft = []
        self.cand_soglia = []
        self.cand_avv = []
        self.cand_I = []
        self.cand_d = []
        self.dist_piene = {}

    # ---- H1
    def modulazione(self, net, rn, grad, soglia0, soglia):
        g = np.asarray(grad, float)
        self._mod = {
            "soglia0": float(soglia0),
            "grad": q(g),
            "r_nodo": q(rn),
            "soglia": q(soglia),
            # ### QUANTO LA MODULAZIONE MORDE DAVVERO: `1 - soglia/soglia0` in [0, 0.3]
            "morso": q(1.0 - np.asarray(soglia, float) / float(soglia0)),
            "tanh_grad": q(np.tanh(g)),
        }

    def riscalato(self, m):
        self.riscalamenti.append(float(m))

    # ---- H2: la catena
    def catena(self, net, avv, soglia, ecc, salita, discesa, ft, segno, resp, prob, nasce):
        avv = np.asarray(avv, float)
        sog = np.asarray(soglia, float)
        sg = np.asarray(segno, float)
        pb = np.asarray(prob, float)
        ns = np.asarray(nasce, bool)
        g1 = avv > sog                       # cancello 1: sopra soglia
        g2 = avv < TW_TETTO                  # cancello 2: sotto il tetto 4pi
        g3 = sg > 0.0                        # cancello 3: regime di CREAZIONE
        g123 = g1 & g2 & g3
        d = {
            "archi": int(avv.size),
            "g1_sopra_soglia": int(np.sum(g1)),
            "g2_sotto_tetto": int(np.sum(g2)),
            "g3_segno_creazione": int(np.sum(g3)),
            "g1_e_g2": int(np.sum(g1 & g2)),
            "g1_e_g2_e_g3": int(np.sum(g123)),
            "prob_positiva": int(np.sum(pb > 0.0)),
            "g4_nasce": int(np.sum(ns)),
            "ft": q(ft),
            "avv": q(avv),
            "soglia": q(sog),
            "segno": q(sg),
            # ### le distribuzioni SUGLI ARCHI CHE PASSANO IL CANCELLO 1: e' l'insieme
            #   interessante, e sull'insieme totale la coda lo nasconderebbe.
            "avv_su_g1": q(avv[g1]),
            "soglia_su_g1": q(sog[g1]),
            "prob_su_g123": q(pb[g123]),
            "resp_su_g123": q(np.asarray(resp, float)[g123]),
            # ### IL RAPPORTO avv/soglia: dice QUANTO SIAMO LONTANI dal cancello 1, ed e'
            #   la grandezza che distingue <<la soglia e' salita>> da <<avv e' scesa>>.
            "rapporto_avv_soglia": q(avv / np.maximum(sog, 1e-30)),
        }
        self._cat = d
        self._cat_sel = ns
        if ns.any():
            self.cand_ft.append(np.asarray(ft, float)[ns] if np.ndim(ft) else None)
            self.cand_soglia.append(sog[ns])
            self.cand_avv.append(avv[ns])

    # ---- H3: i cancelli finali
    def finali(self, net, c, ok, no_dens, no_lam, I, dc):
        o = np.asarray(ok, bool)
        self._fin = {
            "g5_candidati_dopo_mitmax": int(np.size(c)),
            "g6_passa_densita": int(np.sum(~np.asarray(no_dens, bool))),
            "g7_passa_2lam": int(np.sum(~np.asarray(no_lam, bool))),
            "rifiutati_solo_densita": int(np.sum(np.asarray(no_dens, bool)
                                                 & ~np.asarray(no_lam, bool))),
            "rifiutati_solo_2lam": int(np.sum(~np.asarray(no_dens, bool)
                                              & np.asarray(no_lam, bool))),
            "rifiutati_entrambi": int(np.sum(np.asarray(no_dens, bool)
                                             & np.asarray(no_lam, bool))),
            "ammessi": int(np.sum(o)),
            "I_candidati": q(np.asarray(I, float)[np.asarray(c, int)]
                             if np.size(c) else []),
            "d_candidati": q(dc),
        }
        if np.size(c):
            self.cand_I.append(np.asarray(I, float)[np.asarray(c, int)])
            self.cand_d.append(np.asarray(dc, float))

    # ---- fine passo
    def chiudi(self, net, n_prec):
        d = {"passo": self.passo, "n": int(net.n), "archi": int(len(net.i)),
             "nati_nel_passo": int(net.n) - int(n_prec),
             "schwinger_tot": int(getattr(net, "_g_nati_schwinger", 0)),
             "nati_tot": int(getattr(net, "nati", 0))}
        d.update(self._cat or {"archi": 0, "g4_nasce": 0})
        d["passo"] = self.passo
        if self._mod is not None:
            d["mod"] = self._mod
        if getattr(self, "_fin", None) is not None:
            d["fin"] = self._fin
        else:
            # ### H3 sta DENTRO `if len(c):`: nei passi senza candidati non scatta, e quei
            #   passi hanno ZERO nascite da divisione PER COSTRUZIONE. Si DICHIARA invece
            #   di apparire come un dato mancante.
            d["fin"] = {"ammessi": 0, "stato": "nessun candidato: H3 non scatta"}
        self.passi.append(d)
        if self.passo == PASSO_DIST:
            self.dist_piene = {"mod": self._mod, "catena": self._cat,
                               "finali": getattr(self, "_fin", None)}
        self._mod = None
        self._cat = None
        self._fin = None

    # ---- i totali
    def totali(self):
        div = sum(r["fin"].get("ammessi", 0) for r in self.passi)
        return {"divisioni": int(div),
                "schwinger": int(self.passi[-1]["schwinger_tot"]) if self.passi else 0,
                "nati_tot": int(self.passi[-1]["nati_tot"]) if self.passi else 0}


# =============================================================== LA SCENA
def carica(nome, sim):
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                              dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome=nome, sim=sim)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    return S, S.net, a


def _scrivi(d):
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    io.open(os.path.join(FUORI, "crescita.json"), "w", encoding="utf-8").write(
        json.dumps(d, indent=1, default=str))
    io.open(os.path.join(FUORI, "crescita.txt"), "w", encoding="utf-8").write(
        NL.join(P) + NL)


def main(argv):
    passi = PASSI
    if "--collaudo" in argv[1:]:
        riga("=")
        stampa("IL COLLAUDO DI _crescita_dopo_z43.py")
        riga("=")
        return collaudo()
    for a in argv[1:]:
        if a.startswith("--passi="):
            passi = int(a.split("=", 1)[1])
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    riga("=")
    stampa("CRESCITA-DOPO-Z43: perche' la rete quasi non cresce piu' con r = cs/CS_M")
    riga("=")
    stampa()
    pf = piattaforma()
    for k in ["python", "numpy", "sistema", "macchina"]:
        stampa("  %-10s %s" % (k, pf[k]))
    stampa("  simulatore OGGI (PARTE B) %s   strumento %s"
           % (blob(SIM)[:8], blob(__file__)[:8]))
    stampa()

    # --- il braccio A dal TAG, in BINARIO (par.7)
    sa = os.path.join(FUORI, "_sim_a.py")
    g = subprocess.run(["git", "cat-file", "-p", TAG + ":soliton_simulator.py"],
                       capture_output=True, cwd=RADICE)
    if g.returncode != 0:
        stampa("### IL BRACCIO A NON SI E' POTUTO ESTRARRE: %r" % (g.stderr[:200],))
        _scrivi({"esito": 1, "piattaforma": pf})
        return 1
    io.open(sa, "wb").write(g.stdout)
    blob_a = blob(sa)[:8]
    stampa("  braccio A dal tag %s: blob %s  (atteso 062172d3)" % (TAG, blob_a))
    if blob_a != "062172d3":
        stampa("### IL BLOB DEL BRACCIO A NON E' QUELLO ATTESO. MI FERMO.")
        _scrivi({"esito": 1, "blob_a": blob_a, "piattaforma": pf})
        return 1

    ap = os.path.join(FUORI, "_sim_ap.py")
    bp = os.path.join(FUORI, "_sim_bp.py")
    bc = os.path.join(FUORI, "_sim_bc.py")
    f_ap = copia_patchata(sa, ap)
    f_bp = copia_patchata(SIM, bp)
    f_bc = copia_patchata(SIM, bc, controfattuale=True)
    stampa("  Ap %s (%d ancore)   Bp %s (%d)   Bc %s (%d)"
           % (blob(ap)[:8], len(f_ap), blob(bp)[:8], len(f_bp), blob(bc)[:8], len(f_bc)))
    for f in f_bc:
        stampa("      - " + f)
    stampa()

    SA, nA, a = carica("cre_Ap", ap)
    SB, nB, _ = carica("cre_Bp", bp)
    SC, nC, _ = carica("cre_Bc", bc)
    in_conf = _cli_flag.dichiara_configurazione(SB, stampa)
    mA, mB, mC = Misura("Ap"), Misura("Bp"), Misura("Bc")
    SA._MIS, SB._MIS, SC._MIS = mA, mB, mC
    n0 = {"Ap": int(nA.n), "Bp": int(nB.n), "Bc": int(nC.n)}
    stampa("  scena: nmasse=%s sep=%s  ->  n = %d, archi = %d"
           % (getattr(a, "nmasse", "?"), getattr(a, "sep", "?"), nA.n, len(nA.i)))
    stampa("  ### TRE BRACCI: Ap la PARTE A (062172d3) patchata, Bp la PARTE B (%s)"
           % blob(SIM)[:8])
    stampa("      patchata, Bc il CONTROFATTUALE -- r moltiplicato per 1/mediana(r),")
    stampa("      ### DICHIARATO FINTO: non e' una cura e non entra nel simulatore.")
    stampa("  ### E I GRADIENTI DEL CONTROFATTUALE NON RESTANO INTATTI: crescono del 23 %,")
    stampa("      perche' riscalare r per 1/mediana(r) riscala anche |r_i - r_j|.")
    stampa("      ### E' CONSERVATIVO NELLA DIREZIONE GIUSTA: un gradiente maggiorato")
    stampa("      ABBASSA la soglia, quindi spinge le nascite VERSO L'ALTO.")
    stampa()
    riga("=")
    stampa("LA CORSA: %d passi, TRE bracci, col BATTITO per passo" % passi)
    riga("=")
    npA, npB, npC = int(nA.n), int(nB.n), int(nC.n)
    for k in range(1, passi + 1):
        mA.passo = mB.passo = mC.passo = k
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(SA, nA)
            _passo.passo_pieno(SB, nB)
            _passo.passo_pieno(SC, nC)
        mA.chiudi(nA, npA)
        mB.chiudi(nB, npB)
        mC.chiudi(nC, npC)
        npA, npB, npC = int(nA.n), int(nB.n), int(nC.n)
        print("[battito] passo %d/%d  n: A=%d B=%d C=%d  nasce: A=%d B=%d C=%d"
              % (k, passi, nA.n, nB.n, nC.n,
                 mA.passi[-1].get("g4_nasce", 0), mB.passi[-1].get("g4_nasce", 0),
                 mC.passi[-1].get("g4_nasce", 0)), flush=True)

    # ### I DATI SI SCRIVONO PRIMA DEL RAPPORTO: una caduta nella post-elaborazione non
    #   deve costare la corsa. E' la lezione di `aafb3eb`, pagata con 150 passi.
    comune = {"piattaforma": pf, "passi": passi, "blob_sim_b": blob(SIM),
              "blob_sim_a": blob(sa), "blob_strumento": blob(__file__),
              "ancore": {"Ap": f_ap, "Bp": f_bp, "Bc": f_bc},
              "in_configurazione_del_driver": bool(in_conf),
              "passo_dist": PASSO_DIST, "n0": n0,
              "bracci": {m.nome: {"passi": m.passi, "totali": m.totali(),
                                  "dist_piene": m.dist_piene,
                                  "riscalamenti": q(m.riscalamenti) if m.riscalamenti
                                  else None,
                                  "n_fin": None} for m in (mA, mB, mC)},
              "a_valle": {"n_Ap": int(nA.n), "n_Bp": int(nB.n), "n_Bc": int(nC.n),
                          "archi_Ap": int(len(nA.i)), "archi_Bp": int(len(nB.i)),
                          "archi_Bc": int(len(nC.i))}}
    d = dict(comune)
    d.update({"esito": None, "stato": "DATI SALVATI, rapporto NON ancora girato"})
    _scrivi(d)
    stampa("  ### I DATI SONO GIA' SALVATI in crescita.json, PRIMA del rapporto.")
    stampa()
    try:
        esito, guasti = rapporto(mA, mB, mC, nA, nB, nC, n0, in_conf, passi)
    except Exception as e:
        import traceback
        stampa("### IL RAPPORTO E' CADUTO, MA I DATI CI SONO: %r" % (e,))
        stampa(traceback.format_exc())
        d = dict(comune)
        d.update({"esito": 1, "guasti": ["il rapporto e' caduto: %r" % (e,)],
                  "stato": "DATI SALVATI, rapporto CADUTO",
                  "traccia": traceback.format_exc()})
        _scrivi(d)
        return 1
    d = dict(comune)
    d.update({"esito": esito, "guasti": guasti, "stato": "fatto"})
    _scrivi(d)
    return esito


def rapporto(mA, mB, mC, nA, nB, nC, n0, in_conf, passi):
    guasti = []
    bracci = [(mA, nA, "Ap"), (mB, nB, "Bp"), (mC, nC, "Bc")]

    riga("=")
    stampa("(a) LA CATENA DEI CANCELLI, per braccio -- TOTALI sui %d passi" % passi)
    riga("=")
    CH = [("archi", "archi"),
          ("g1_sopra_soglia", "1 sopra soglia"),
          ("g1_e_g2", "1+2 sotto il tetto 4pi"),
          ("g1_e_g2_e_g3", "1+2+3 segno di CREAZIONE"),
          ("prob_positiva", "prob > 0"),
          ("g4_nasce", "4 l'estrazione")]
    stampa("  %-30s %14s %14s %14s" % ("cancello", "Ap (PARTE A)", "Bp (PARTE B)",
                                       "Bc (controfatt.)"))
    for k, et in CH:
        v = [sum(r.get(k, 0) for r in m.passi) for m, _n, _s in bracci]
        stampa("  %-30s %14d %14d %14d" % (et, v[0], v[1], v[2]))
    for k, et in [("g5_candidati_dopo_mitmax", "5 dopo MITMAX"),
                  ("g6_passa_densita", "6 la densita'"),
                  ("g7_passa_2lam", "7 A13/2LAM"),
                  ("ammessi", "-> AMMESSI (divisioni)")]:
        v = [sum(r["fin"].get(k, 0) for r in m.passi) for m, _n, _s in bracci]
        stampa("  %-30s %14d %14d %14d" % (et, v[0], v[1], v[2]))
    v = [m.totali()["schwinger"] for m, _n, _s in bracci]
    stampa("  %-30s %14d %14d %14d" % ("(c) nascite SCHWINGER", v[0], v[1], v[2]))
    stampa()

    # --- DOVE SI SEPARANO (C4)
    riga("=")
    stampa("(a) DOVE I BRACCI SI SEPARANO -- il cancello, non <<piu' o meno tutti>>")
    riga("=")
    tA = {k: sum(r.get(k, 0) for r in mA.passi) for k, _e in CH}
    tB = {k: sum(r.get(k, 0) for r in mB.passi) for k, _e in CH}
    stampa("  %-30s %12s %12s %10s %s"
           % ("cancello", "Ap", "Bp", "Bp/Ap", "il salto rispetto al cancello prima"))
    prec = None
    separa = []
    for k, et in CH:
        rap = (tB[k] / tA[k]) if tA[k] else None
        salto = (None if (prec is None or prec[1] is None or rap is None)
                 else (rap / prec[1] if prec[1] else None))
        stampa("  %-30s %12d %12d %10s %s"
               % (et, tA[k], tB[k],
                  ("%.4f" % rap) if rap is not None else "n/d",
                  ("x%.4f" % salto) if salto is not None else "-"))
        if salto is not None and salto < 0.5:
            separa.append((et, salto))
        prec = (k, rap)
    stampa()
    if separa:
        stampa("  ### I CANCELLI SU CUI IL RAPPORTO Bp/Ap CROLLA (fattore < 0.5 rispetto al")
        stampa("      cancello precedente):")
        for et, s in separa:
            stampa("      - %-32s x%.4f" % (et, s))
        if len(separa) == 1:
            stampa("  ### C4: LA SEPARAZIONE CADE SU **UN** CANCELLO: %s" % separa[0][0])
        else:
            stampa("  ### C4: LA SEPARAZIONE CADE SU %d CANCELLI, e LO DICO invece di"
                   % len(separa))
            stampa("      nominarne uno solo.")
    else:
        stampa("  ### C4: NESSUN cancello fa crollare il rapporto di piu' di 2x rispetto al")
        stampa("      precedente. ### LA SEPARAZIONE E' DIFFUSA, e va detto.")
    stampa()

    # --- (b) LE DISTRIBUZIONI
    riga("=")
    stampa("(b) LE GRANDEZZE CHE I CANCELLI LEGGONO, al passo %d" % PASSO_DIST)
    riga("=")
    stampa("  ### E SI RIPORTANO COME DISTRIBUZIONI E NON COME MEDIANE: una mediana NON")
    stampa("      distingue una distribuzione RIPIDA da una PIATTA, ed e' esattamente la")
    stampa("      cosa da cui dipende se l'ipotesi del gradiente tiene.")
    stampa()
    for m, _n, et in bracci:
        dp = m.dist_piene or {}
        stampa("  --- braccio %s ---" % et)
        mod = dp.get("mod")
        if mod:
            stampa("      soglia0 = %.9f" % mod["soglia0"])
            for nome in ("r_nodo", "grad", "tanh_grad", "soglia", "morso"):
                _q = mod.get(nome)
                if _q:
                    stampa("      %-12s q01=%.6e q25=%.6e q50=%.6e q75=%.6e q99=%.6e max=%.6e"
                           % (nome, _q["q001"], _q["q025"], _q["q050"], _q["q075"],
                              _q["q099"], _q["q100"]))
        cat = dp.get("catena")
        if cat:
            for nome in ("avv", "soglia", "rapporto_avv_soglia", "ft", "segno",
                         "avv_su_g1"):
                _q = cat.get(nome)
                if _q:
                    stampa("      %-20s q01=%.6e q25=%.6e q50=%.6e q75=%.6e q99=%.6e"
                           % (nome, _q["q001"], _q["q025"], _q["q050"], _q["q075"],
                              _q["q099"]))
            stampa("      cancelli al passo %d: archi=%d g1=%d g1+2=%d g1+2+3=%d nasce=%d"
                   % (PASSO_DIST, cat["archi"], cat["g1_sopra_soglia"], cat["g1_e_g2"],
                      cat["g1_e_g2_e_g3"], cat["g4_nasce"]))
        fin = dp.get("finali")
        if fin:
            stampa("      finali: candidati=%d densita'=%d 2LAM=%d ammessi=%d"
                   % (fin["g5_candidati_dopo_mitmax"], fin["g6_passa_densita"],
                      fin["g7_passa_2lam"], fin["ammessi"]))
        stampa()

    # --- (d) IL CONTROFATTUALE
    riga("=")
    stampa("(d) IL CONTROFATTUALE: il rallentamento uniforme contro il gradiente")
    riga("=")
    tot = {et: m.totali() for m, _n, et in bracci}
    stampa("  divisioni:  Ap=%d  Bp=%d  Bc=%d"
           % (tot["Ap"]["divisioni"], tot["Bp"]["divisioni"], tot["Bc"]["divisioni"]))
    stampa("  schwinger:  Ap=%d  Bp=%d  Bc=%d"
           % (tot["Ap"]["schwinger"], tot["Bp"]["schwinger"], tot["Bc"]["schwinger"]))
    dA, dB, dC = (tot["Ap"]["divisioni"], tot["Bp"]["divisioni"], tot["Bc"]["divisioni"])
    stampa("  Bp/Ap = %s     Bc/Ap = %s     Bc/Bp = %s"
           % (("%.4f" % (dB / dA)) if dA else "n/d",
              ("%.4f" % (dC / dA)) if dA else "n/d",
              ("%.4f" % (dC / dB)) if dB else "n/d"))
    if mC.riscalamenti:
        _q = q(mC.riscalamenti)
        stampa("  il fattore 1/mediana(r) applicato: q01=%.6f q50=%.6f q99=%.6f"
               % (1.0 / _q["q099"], 1.0 / _q["q050"], 1.0 / _q["q001"]))
        stampa("      ### e QUINDI il gradiente del braccio Bc e' maggiorato di quel")
        stampa("      fattore: NON e' intatto, e la direzione dell'errore e' VERSO PIU'")
        stampa("      NASCITE.")
    stampa()
    if dA:
        if dC >= 0.5 * dA:
            stampa("  ### LETTURA: le nascite TORNANO VERSO LA PARTE A togliendo il")
            stampa("      rallentamento uniforme -> LA CAUSA E' IL RALLENTAMENTO.")
        elif dC <= 2.0 * dB:
            stampa("  ### LETTURA: le nascite RESTANO BASSE anche senza il rallentamento")
            stampa("      uniforme (e con un gradiente MAGGIORATO) -> LA CAUSA NON E' IL")
            stampa("      RALLENTAMENTO. ### Ed e' la lettura FORTE, perche' il")
            stampa("      controfattuale sbaglia nella direzione opposta.")
        else:
            stampa("  ### LETTURA: INTERMEDIA -- le nascite risalgono ma non tornano alla")
            stampa("      PARTE A. ### Il controfattuale NON separa le due cause, e il")
            stampa("      23 %% di gradiente in piu' e' una causa confondente DICHIARATA.")
    stampa()

    # --- I CONTROLLI
    riga("=")
    stampa("I CONTROLLI CHE POSSONO FALLIRE")
    riga("=")
    # C1
    for m, net, et in bracci:
        t = m.totali()
        atteso = int(net.n) - int(n0[et])
        ric = t["divisioni"] + t["schwinger"]
        ok = (ric == atteso)
        stampa("  C1 %-4s divisioni %6d + schwinger %6d = %6d   n_fin - n_0 = %6d   %s"
               % (et, t["divisioni"], t["schwinger"], ric, atteso,
                  "COINCIDE" if ok else "### NON COINCIDE"))
        if not ok:
            guasti.append("C1 %s: ricostruzione %d contro %d" % (et, ric, atteso))
    # C2
    for m, _net, et in bracci:
        cand = sum(r["fin"].get("g5_candidati_dopo_mitmax", 0) for r in m.passi)
        stampa("  C2 %-4s candidati su tutta la corsa: %d   %s"
               % (et, cand,
                  "ok" if cand else "### ZERO: per questo braccio il confronto NON esiste"))
    # C3: contro i numeri GIA' COMMITTATI del sigillo
    try:
        sg = json.loads(io.open(SIGILLO_B, encoding="utf-8").read())
        av = sg["a_valle"]
        prove = [("Ap", "n", int(nA.n), av["n_A"]), ("Ap", "archi", len(nA.i), av["archi_A"]),
                 ("Bp", "n", int(nB.n), av["n_B"]), ("Bp", "archi", len(nB.i), av["archi_B"])]
        for et, gr, mio, suo in prove:
            ok = (mio == suo)
            stampa("  C3 %-4s %-6s questo strumento %8d   il sigillo committato %8d   %s"
                   % (et, gr, mio, suo, "COINCIDE" if ok else "### NON COINCIDE"))
            if not ok:
                guasti.append("C3 %s %s: %d contro %d" % (et, gr, mio, suo))
        stampa("      ### E' UN CONFRONTO FRA DUE CORSE DIVERSE, quindi piu' forte di un")
        stampa("          auto-confronto: se i ganci cambiassero la fisica, questi numeri")
        stampa("          non coinciderebbero.")
    except Exception as e:
        stampa("  C3  NON VERIFICABILE: %r" % (e,))
        guasti.append("C3 non verificabile: %r" % (e,))
    stampa()
    riga("=")
    stampa("IL VERDETTO")
    riga("=")
    stampa("  configurazione del driver dichiarata INTERA (braccio Bp): %s" % bool(in_conf))
    if guasti:
        stampa("  ### FERMO. I GUASTI:")
        for g in guasti:
            stampa("      - " + g)
        return 1, guasti
    stampa("  ### I CONTROLLI CHE FERMANO (C1, C3) PASSANO.")
    stampa("  ### E QUESTO E' UNA MISURA, NON UN SIGILLO: non c'e' niente da promuovere.")
    stampa("      La crescita e la soglia di mitosi sono DECISIONI DI LUCA.")
    return 0, []


# =============================================================== IL COLLAUDO
def collaudo():
    esiti = []

    def prova(nome, ok, dett=""):
        esiti.append((nome, bool(ok), dett))
        print("  %-6s %-58s %s" % ("OK" if ok else "### KO", nome, dett))

    # --- 1. `q`: la FORMA, non un numero
    _q = q([1.0, 2.0, 3.0, 4.0, 5.0])
    prova("q: restituisce i nove quantili chiesti", len(_q) == len(QUANTILI),
          "%d chiavi" % len(_q))
    prova("q: q050 di 1..5 e' 3.0 ESATTO", _q["q050"] == 3.0, "%.17g" % _q["q050"])
    prova("q: q000 e q100 sono min e max",
          _q["q000"] == 1.0 and _q["q100"] == 5.0)
    prova("q: un vettore VUOTO da' None, non uno zero", q([]) is None)
    prova("q: i NON FINITI si escludono invece di propagare NaN",
          q([1.0, np.nan, 3.0, np.inf])["q050"] == 2.0,
          "%.17g" % q([1.0, np.nan, 3.0, np.inf])["q050"])

    # --- 2. la catena: i cancelli su valori COSTRUITI a mano
    m = Misura("prova")
    m.passo = 1
    # ### I VALORI SONO SCELTI PERCHE' DUE CADANO NELLA FINESTRA, e il primo giro di
    #   questo collaudo FALLI' proprio per questo: avevo scritto [1, 7, 13, 20] e NESSUNO
    #   stava fra 3pi e 4pi -- i cancelli 1 e 2 sono una FINESTRA, non due tagli dallo
    #   stesso lato, e l'avevo contato male IO, non il codice.
    #   soglia0 = 3pi = 9.424778,  tetto = 4pi = 12.566371
    avv = np.asarray([1.0, 10.0, 11.0, 20.0])
    sog = np.full(4, 3.0 * np.pi)
    segno = np.asarray([1.0, 1.0, -1.0, -1.0])
    prob = np.asarray([0.0, 0.5, 0.0, 0.0])
    nasce = np.asarray([False, True, False, False])
    m.catena(None, avv=avv, soglia=sog, ecc=None, salita=None, discesa=None,
             ft=np.ones(4), segno=segno, resp=np.zeros(4), prob=prob, nasce=nasce)
    c = m._cat
    prova("cancello 1: sopra soglia (3pi) = 3 archi: 10, 11, 20",
          c["g1_sopra_soglia"] == 3, "%d" % c["g1_sopra_soglia"])
    prova("cancello 2: sotto il tetto 4pi = 3 archi: 1, 10, 11",
          c["g2_sotto_tetto"] == 3, "%d" % c["g2_sotto_tetto"])
    prova("### i cancelli 1 e 2 sono una FINESTRA: insieme passano 2 archi (10 e 11)",
          c["g1_e_g2"] == 2, "%d" % c["g1_e_g2"])
    prova("cancello 3: segno > 0 su 2 archi", c["g3_segno_creazione"] == 2,
          "%d" % c["g3_segno_creazione"])
    prova("cancello 1+2+3: UN arco solo (10, che ha segno +)",
          c["g1_e_g2_e_g3"] == 1, "%d" % c["g1_e_g2_e_g3"])
    prova("l'estrazione: 1 nasce", c["g4_nasce"] == 1)
    prova("il rapporto avv/soglia distingue i due regimi",
          abs(c["rapporto_avv_soglia"]["q100"] - 20.0 / (3 * np.pi)) < 1e-12,
          "%.6f" % c["rapporto_avv_soglia"]["q100"])

    # --- 3. la modulazione: `morso` e' 0 con gradiente ZERO e 0.3 con gradiente INFINITO
    m2 = Misura("mod")
    s0 = 3.0 * np.pi
    m2.modulazione(None, rn=np.ones(3), grad=np.zeros(3), soglia0=s0,
                   soglia=s0 * (1.0 - 0.3 * np.tanh(np.zeros(3))))
    prova("modulazione: gradiente ZERO -> morso ZERO (la soglia NON si abbassa)",
          abs(m2._mod["morso"]["q050"]) < 1e-15, "%.3e" % m2._mod["morso"]["q050"])
    gg = np.full(3, 50.0)
    m2.modulazione(None, rn=np.ones(3), grad=gg, soglia0=s0,
                   soglia=s0 * (1.0 - 0.3 * np.tanh(gg)))
    prova("modulazione: gradiente ENORME -> morso 0.3 (il tetto della legge)",
          abs(m2._mod["morso"]["q050"] - 0.3) < 1e-12,
          "%.9f" % m2._mod["morso"]["q050"])
    # ### IL NUMERO CHE DECIDE L'IPOTESI: col gradiente della PARTE A (r in [1.4e-6, 1.414])
    #   il morso arriva a ~0.3; con quello della PARTE B (r in (0,1], liscio) a ~0.
    gA = np.asarray([1.414])      # il gradiente massimo possibile nella PARTE A
    m2.modulazione(None, rn=np.ones(1), grad=gA, soglia0=s0,
                   soglia=s0 * (1.0 - 0.3 * np.tanh(gA)))
    prova("modulazione: col gradiente MASSIMO della PARTE A il morso e' ~0.27",
          0.25 < m2._mod["morso"]["q050"] < 0.30,
          "%.6f -> soglia %.4f invece di %.4f"
          % (m2._mod["morso"]["q050"],
             s0 * (1 - m2._mod["morso"]["q050"]), s0))

    # --- 4. i cancelli finali
    m3 = Misura("fin")
    m3.finali(None, c=np.asarray([0, 1, 2]), ok=np.asarray([True, False, True]),
              no_dens=np.asarray([False, True, False]),
              no_lam=np.asarray([False, False, True]),
              I=np.asarray([1.0, 2.0, 3.0]), dc=np.asarray([2.0, 2.0, 1.0]))
    prova("finali: i rifiuti si SEPARANO per cancello",
          m3._fin["rifiutati_solo_densita"] == 1
          and m3._fin["rifiutati_solo_2lam"] == 1
          and m3._fin["rifiutati_entrambi"] == 0,
          "dens=%d lam=%d entrambi=%d" % (m3._fin["rifiutati_solo_densita"],
                                          m3._fin["rifiutati_solo_2lam"],
                                          m3._fin["rifiutati_entrambi"]))
    prova("finali: `ammessi` viene da `ok`, non dalla mia somma",
          m3._fin["ammessi"] == 2, "%d" % m3._fin["ammessi"])

    # --- 5. H3 NON scatta senza candidati, e il passo si DICHIARA
    class FintaRete(object):
        n = 10
        i = np.arange(3)
        nati = 0
    m4 = Misura("vuoto")
    m4.passo = 1
    m4.catena(None, avv=np.zeros(3), soglia=np.ones(3), ecc=None, salita=None,
              discesa=None, ft=np.ones(3), segno=np.ones(3), resp=np.zeros(3),
              prob=np.zeros(3), nasce=np.zeros(3, bool))
    m4.chiudi(FintaRete(), 10)
    prova("H3 non scatta senza candidati: il passo lo DICHIARA invece di mancare",
          m4.passi[0]["fin"].get("stato", "").startswith("nessun candidato"),
          m4.passi[0]["fin"].get("stato", ""))
    prova("e quel passo ha ZERO ammessi, non None",
          m4.passi[0]["fin"]["ammessi"] == 0)

    # --- 6. le ancore della patch sono UNICHE in ENTRAMBI i bracci
    src_b = io.open(SIM, encoding="utf-8").read()
    g = subprocess.run(["git", "cat-file", "-p", TAG + ":soliton_simulator.py"],
                       capture_output=True, cwd=RADICE)
    src_a = g.stdout.decode("utf-8") if g.returncode == 0 else ""
    ANC = ["import numpy as np" + NL,
           "            soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_modula))" + NL,
           "        c = np.where(nasce)[0]" + NL,
           "            ok = ok & _conforme" + NL,
           "            self._r_corrente = r" + NL]
    prova("le 5 ancore sono UNICHE nel braccio B (il simulatore di oggi)",
          all(src_b.count(a) == 1 for a in ANC),
          str([src_b.count(a) for a in ANC]))
    prova("le 5 ancore sono UNICHE anche nel braccio A (il blob del tag)",
          bool(src_a) and all(src_a.count(a) == 1 for a in ANC),
          str([src_a.count(a) for a in ANC]) if src_a else "braccio A non estratto")
    prova("### e il blob del braccio A e' quello atteso",
          bool(src_a) and hashlib.sha1(g.stdout).hexdigest()[:8] == "062172d3",
          hashlib.sha1(g.stdout).hexdigest()[:8] if src_a else "n/d")

    # --- 7. il controfattuale: il riscalamento porta la mediana a 1 ESATTO
    r = np.asarray([0.5, 0.8, 1.0, 0.9, 0.7])
    mm = float(np.median(r))
    rr = r / mm
    prova("controfattuale: dopo il riscalamento la mediana di r e' 1.0",
          abs(float(np.median(rr)) - 1.0) < 1e-15, "%.17g" % float(np.median(rr)))
    g0 = abs(r[0] - r[1])
    g1 = abs(rr[0] - rr[1])
    prova("controfattuale: ### il GRADIENTE NON resta intatto, cresce di 1/mediana",
          abs(g1 / g0 - 1.0 / mm) < 1e-12,
          "x%.6f (1/mediana = %.6f)" % (g1 / g0, 1.0 / mm))

    riga("=")
    ko = [n for n, o, _d in esiti if not o]
    stampa("COLLAUDO: %d su %d" % (len(esiti) - len(ko), len(esiti)))
    if ko:
        stampa("### FALLITI:")
        for n in ko:
            stampa("    - " + n)
    riga("=")
    return 1 if ko else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
