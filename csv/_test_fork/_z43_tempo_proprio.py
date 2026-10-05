# -*- coding: utf-8 -*-
"""`Z43`: LA DEFINIZIONE DEL TEMPO PROPRIO `r`, MISURATA A LATO.

*(`Z43`, passo **(1): la misura**. Mandato di Luca del 2026-10-05, sul blob `e2940b3c`.
Task history: `doc/TASK_HISTORY/2026-10-05_z43-definizione-tempo-proprio-misura.md`,
committato PRIMA in `12ab7f4`.)*

### ⛔ **E' UNA MISURA, NON UNA CURA:** nessun `PASSA`/`FALLISCE` **fuori dai controlli**, il
### simulatore **non si tocca**, e ### **NESSUNA LEGGE NUOVA si scrive: la forma la decide
### Luca dopo il referto.**

### LA DEFINIZIONE DI OGGI, letta dal codice *(`ritmo()`, `:5260`)*

    a      = angle(psi_spin[:,0]) - angle(_psi_spin_prec[:,0])      :5308
    signed = ((a + pi) % (2pi) - pi) / DT                           :5313
    f      = |signed|                                               :5318
    med    = _med_f_prec      (il gauge, del passo PRECEDENTE)      :5358 / :5366
    x      = f / med                                                :5371
    r      = (x/sqrt(1+x^2) + 1e-6) / (1/sqrt(2) + 1e-6)            :5372-5374
    out    = 1 + TAU_LOC*(r - 1)                                    :5375

**I TRE DIFETTI DI DEFINIZIONE:** `(D1)` frequenza usata come tempo **senza una frequenza
propria del nodo**; `(D2)` riferimento **NON locale** *(mediana su tutti i nodi)*; `(D3)`
dipende dalla **BASE** dello spinore *(componente `0`)* e **contiene la fase globale**.

### L'ANELLO, verificato dall'AST e non assunto
`r_node = dtn/DT` *(`:5904`)* -> `omega_clk = coerenza * r_node` *(`:5926`)* ->
`* (cs_prec/CS_M)^2` *(`:5970`)* -> `_phc = exp(-0.5j*_sk*omega_clk*_dts)` con `_dts = DT*r`
*(`:5971`)*. ### **La fase dell'orologio avanza di `r^2`**, e `psi_spin` la riporta a `f`.
### **Sfasato di un passo** *(`_psi_spin_prec` e `_med_f_prec` sono snapshot)*: non viola
`A6`, ed e' il candidato all'**altalena**.

### ⛔ L'OROLOGIO DI COMPTON VIVE IN `C2`, NON IN `C1`
*(correzione del guardiano del 2026-10-05.)* `_phc = exp(-0.5j*_sk*omega_clk*_dts)`
*(`:5971`)* e' una **fase globale**, e `C1` e' ### **cio' che una fase LASCIA INVARIATO.**
### **Quindi la coerenza di Compton si misura su `C2`**, e si misura anche
### **quanto `C2` segue la legge che l'orologio GIA' scrive:**

    attesa = -0.5*_sk*omega_clk*_dts/DT = -0.5*coerenza*(cs/CS_M)^2*r^2

### **E l'attesa NON si ricalcola: si LEGGE dalle variabili della legge stessa** al sito
di `:5971` — ricostruirla sarebbe una **seconda scrittura**.
### ⚠ **E `psi_spin` e' il campo EMESSO** *(somma sui vicini, `:6240`)*, quindi
### **la relazione puo' valere solo IN MEDIA LOCALE, non per nodo.**

### I CINQUE CONTROLLI CHE POSSONO FALLIRE
| | |
|---|---|
| **`POSITIVO`** | uno spinore sintetico ruotato di un angolo **noto** restituisce quell'angolo in `C1` |
| **`BASE`** | una rotazione `SU(2)` comune a **entrambi** gli snapshot lascia `C1` invariato. ### **CASO CHE DEVE FALLIRE: `C3` CAMBIA.** Se non cambia, non discrimina: **FERMO** |
| **`FASE GLOBALE`** | lo stesso `e^{i alpha}` su entrambi lascia `C1` **e** `C2` invariati |
| **`FEDELTA'`** | il mio `C0` coincide ### **AL BIT** col `r` di `ritmo()`, nei passi **senza rami di sicurezza** |
| **`CONTEGGIO`** | ### **zero nodi confrontati NON e' un'identita'** |

USO:
  python csv/_test_fork/_z43_tempo_proprio.py
  python csv/_test_fork/_z43_tempo_proprio.py --collaudo
  opzioni: --passi=N (default 150) · --braccio-a (omega_clk con r_node = 1)

USCITA: `csv/_test_fork/_z43_tempo_proprio/_z43_tempo_proprio.json` + `_corsa.txt`.

# ESENTE-H-P3: la scena passa TUTTA dal CLI (`nmasse` e `sep` da `argv`), e la
#   configurazione INTERA si DICHIARA (`_cli_flag.dichiara_configurazione`). La COPIA
#   PATCHATA serve perche' `psi_spin`, `_psi_spin_prec` e `_med_f_prec` vanno letti
#   ESATTAMENTE dove `ritmo()` li legge, e `I`/`w`/`cs_nodo` esattamente dove il settore
#   metrico li calcola: ricostruirli fuori sarebbe una SECONDA scrittura delle stesse
#   leggi, cioe' le <<due leggi>> che `9-ter` vieta.
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
FUORI = os.path.join(RADICE, "csv", "_test_fork", "_z43_tempo_proprio")
SIM = os.path.join(RADICE, "soliton_simulator.py")
PASSI = 150
# ### I CONTATORI DEI RAMI DI SICUREZZA DI `ritmo()`: il controllo `FEDELTA'` esclude i
#   passi in cui uno di questi avanza, e li riconosce DAI CONTATORI e non dal numero del
#   passo (i rami tornano `np.ones` SENZA passare dalla formula).
RAMI = ["_ritmo_sicurezza", "_ritmo_med_assente", "_ritmo_guard4pi_ko",
        "_ritmo_f_tutto_nullo", "_ritmo_f_mediana_nulla"]

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


def q(x, nome=None):
    """mediana, p5, p95 -- e il CONTEGGIO, perche' zero non e' un'identita'."""
    x = np.asarray(x, float)
    fin = x[np.isfinite(x)]
    if not len(fin):
        return {"n": 0, "non_finiti": int(len(x))}
    return {"n": int(len(fin)), "non_finiti": int(len(x) - len(fin)),
            "mediana": float(np.median(fin)), "p5": float(np.percentile(fin, 5)),
            "p95": float(np.percentile(fin, 95)),
            "min": float(np.min(fin)), "max": float(np.max(fin))}


# =============================================================== LE FORME, UNA SOLA VOLTA
def _wrap2pi(a):
    """L'avvolgimento di `:5313`, nella STESSA forma."""
    return (a + np.pi) % (2 * np.pi) - np.pi


def r_di_oggi(ps, psp, med, DT, TAU_LOC):
    """`C0`: `r` RICALCOLATO a lato, nell'ORDINE ESATTO di `:5308-5375`.

    ### L'ordine conta: `FEDELTA'` pretende l'identita' AL BIT, e `x**2` non e' `x*x`
    ### per il compilatore di numpy.
    """
    a = np.angle(ps[:, 0]) - np.angle(psp[:, 0])
    signed = _wrap2pi(a) / DT
    f = np.abs(signed)
    x = f / med
    r = x / np.sqrt(1.0 + x**2) + 1.0e-6
    r_unit = 1.0 / np.sqrt(2.0) + 1.0e-6
    return 1.0 + TAU_LOC * (r / r_unit - 1.0), f, signed


def angolo_invariante(ps, psp, DT):
    """`C1`: l'angolo di Fubini-Study fra due spinori, diviso `DT`.

    ### **E' INVARIANTE per fase globale E per una rotazione `SU(2)` COMUNE**, perche'
    `<U a|U b> = <a|b>` e `|e^{i al} z| = |z|`.
    ### ⛔ **E MISURA LO SPOSTAMENTO DEL VETTORE DI BLOCH, NON L'ANGOLO DI UNA
    ### ROTAZIONE:** una rotazione **attorno al Bloch stesso** e' pura **FASE** e
    ### **lascia `C1` a ZERO.** *(Correzione del guardiano del 2026-10-05, scoperta dal
    collaudo di `d190dd5`.)*
    ### ⛔ **E L'OROLOGIO DI COMPTON E' UNA FASE** *(`_phc`, `:5971`)*: ### **vive in
    ### `C2`, NON qui.**
    """
    ov = np.sum(np.conj(psp) * ps, axis=1)
    na = np.sqrt(np.sum(np.abs(psp) ** 2, axis=1))
    nb = np.sqrt(np.sum(np.abs(ps) ** 2, axis=1))
    den = na * nb
    fid = np.where(den > 0, np.abs(ov) / np.maximum(den, 1e-300), 1.0)
    return 2.0 * np.arccos(np.minimum(1.0, fid)) / DT, ov


def fase_globale(ov, DT):
    """`C2`: `arg(<psi_prec|psi>)/DT`."""
    return np.angle(ov) / DT


def fase_componente(ps, psp, k, DT):
    """`C3`: la fase della componente `k`, da sola. ### NON invariante per base."""
    return _wrap2pi(np.angle(ps[:, k]) - np.angle(psp[:, k])) / DT


def mediana_sui_vicini(val, ii, jj, n):
    """La mediana di `val` sui soli VICINI, per nodo. VETTORIALE.

    ### PERCHE' NON UN CICLO: 12 800 nodi x 150 passi sarebbero 1.9 milioni di mediane.
    ### E PERCHE' NON LA MEDIA al posto della mediana: il mandato dice **mediana**, e
    ### sostituirla in silenzio sarebbe misurare un'altra cosa.
    LA FORMA: si ordina per `(nodo, valore)` con `lexsort`, poi si prende l'elemento di
    mezzo di ogni blocco dagli offset cumulativi. Conte PARI -> media dei due centrali,
    che e' la definizione di mediana.
    """
    nodo = np.concatenate([ii, jj])
    v = np.concatenate([val[jj], val[ii]])
    buoni = np.isfinite(v)
    nodo, v = nodo[buoni], v[buoni]
    out = np.full(n, np.nan)
    if not len(nodo):
        return out, np.zeros(n, int)
    ordine = np.lexsort((v, nodo))
    nodo_s, v_s = nodo[ordine], v[ordine]
    conte = np.bincount(nodo_s, minlength=n)
    inizio = np.concatenate([[0], np.cumsum(conte)[:-1]])
    vivi = conte > 0
    idx = inizio[vivi] + (conte[vivi] - 1) // 2
    bassa = v_s[idx]
    idx2 = inizio[vivi] + conte[vivi] // 2
    alta = v_s[np.minimum(idx2, len(v_s) - 1)]
    out[vivi] = 0.5 * (bassa + alta)
    return out, conte


def pendenza_loglog(y, x):
    """La pendenza log-log di `y` contro `x`, ai minimi quadrati. `None` se non si puo'."""
    y = np.asarray(y, float)
    x = np.asarray(x, float)
    m = np.isfinite(x) & np.isfinite(y) & (x > 0) & (y > 0)
    if int(np.sum(m)) < 10:
        return None
    lx, ly = np.log(x[m]), np.log(y[m])
    sx = lx - lx.mean()
    den = float(np.sum(sx * sx))
    if den <= 0:
        return None
    return float(np.sum(sx * (ly - ly.mean())) / den)


# =============================================================== LA PATCH
def copia_patchata(braccio_a=False):
    """Una COPIA con TRE punti di registrazione (QUATTRO con `BRACCIO A`)."""
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    dst = os.path.join(FUORI,
                       "_sim_z43_braccioA.py" if braccio_a else "_sim_z43.py")
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
        + "_MIS = None   # [MISURA Z43] lo riempie lo strumento" + NL,
        "il gancio di modulo `_MIS`")

    # --- in TESTA a `ritmo()`, PRIMA di qualunque mutazione
    uno("        if TAU_LOC == 0.0: return None" + NL,
        "        if _MIS is not None:" + NL
        + "            _MIS(self, 'ritmo_in')" + NL
        + "        if TAU_LOC == 0.0: return None" + NL,
        "in TESTA a `ritmo()`, prima di ogni mutazione")

    # --- in `step()`, subito DOPO il `r` restituito
    uno("        r = self.ritmo()                       # None se l'orologio e' globale"
        + NL,
        "        r = self.ritmo()                       # None se l'orologio e' globale"
        + NL
        + "        if _MIS is not None:" + NL
        + "            _MIS(self, 'ritmo_out', r=r)" + NL,
        "in `step()`, subito dopo il `r` restituito")

    # --- al sito di `cs`, con `I` e `w` dello STESSO istante
    uno("            cs_nodo = self._cs_nodo(I, w)" + NL,
        "            cs_nodo = self._cs_nodo(I, w)" + NL
        + "            if _MIS is not None:" + NL
        + "                _MIS(self, 'cs', I=I, w=w, cs_nodo=cs_nodo)" + NL,
        "al sito di `cs`, con `I` e `w` dello stesso istante")

    # --- l'ATTESA DELL'OROLOGIO, letta dalle variabili della legge stessa
    uno("                _phc = np.exp(-0.5j * _sk * omega_clk * _dts)" + NL,
        "                _phc = np.exp(-0.5j * _sk * omega_clk * _dts)" + NL
        + "                if _MIS is not None:" + NL
        + "                    _MIS(self, 'fase_attesa', omega_clk=omega_clk," + NL
        + "                         dts=_dts, sk=_sk)" + NL,
        "al sito di `_phc`: l'attesa dell'orologio")

    if braccio_a:
        # ### BRACCIO A: `r_node` -> 1 in `omega_clk`. TOGLIE UNA POTENZA di `r`, da
        #   `r^2` a `r^1`. ### NON spezza l'anello: `r` resta in `_dts` (`:5939`).
        uno("                omega_clk = (_num / np.maximum(_den, 1e-12)) * r_node",
            "                omega_clk = (_num / np.maximum(_den, 1e-12)) "
            "* np.ones_like(r_node)",
            "BRACCIO A: `r_node` -> 1 in `omega_clk`")

    io.open(dst, "w", encoding="utf-8", newline=NL).write(t)
    return dst, fatte


# =============================================================== IL RACCOGLITORE
class Raccoglitore(object):
    """Calcola TUTTO al volo e tiene solo AGGREGATI: 150 passi x 12 800 nodi x (n,2)
    complessi non si conservano, e un referto che non entra in memoria non e' un referto."""

    def __init__(self, S):
        self.S = S
        self.DT = float(S.DT)
        self.TAU_LOC = float(S.TAU_LOC)
        self.CS_M = float(S.CS_M)
        self.passo = 0
        self.passi = []
        self.n_prec = 0
        self.attesa = None          # il `C0` che IO ricalcolo, da confrontare con `r`
        self.fed = {"confronti": 0, "diversi": 0, "nodi": 0, "max_scarto": 0.0,
                    "saltati_per_ramo": 0, "peggiore": None}
        self.rami_prec = {}
        # --- accumulatori PER NODO (crescono con `n`)
        self.acc = {}
        for k in ["c1_somma", "c1_conta", "c1_q", "rap_somma", "rap_conta", "rap_q",
                  "inc_somma", "inc_q", "inc_conta", "inc_cross", "inc_prec"]:
            self.acc[k] = np.zeros(0)
        self.ps_t1 = None           # psi_spin del passo precedente
        self.ps_t2 = None           # e di due passi prima
        self.alt = {"d1": [], "d2": [], "passi": 0}
        self.cs_corrente = None     # da `cs`: `cs_nodo` e `cs_spin` dello stesso istante
        self.cs_spin = None
        self.cs_salti_lam = 0
        # ### L'ATTESA DELL'OROLOGIO, e LO SFASAMENTO DI UN PASSO, dichiarato:
        #   `_phc` del passo `t-1` muove `_psi_spinor` nell'intervallo che `C2` misura al
        #   `ritmo_in` del passo `t`. Quindi l'attesa si CONSERVA e si confronta DOPO.
        self.attesa_fase = None
        self.c2_vs_attesa = []
        for k in ["c2_somma", "c2_conta", "c2_q", "r2_somma", "r2_conta", "r2_q",
                  "r2s_somma", "r2s_conta", "r2s_q"]:
            self.acc[k] = np.zeros(0)

    def _estendi(self, n):
        for k, a in self.acc.items():
            if len(a) < n:
                self.acc[k] = np.concatenate([a, np.zeros(n - len(a))])

    def __call__(self, net, quando, **kw):
        getattr(self, "_" + quando)(net, **kw)

    # --------------------------------------------------- l'attesa dell'orologio
    def _fase_attesa(self, net, omega_clk, dts, sk):
        """L'incremento di fase che l'OROLOGIO scrive, LETTO dalla legge stessa.

        ### `_phc = exp(-0.5j*_sk*omega_clk*_dts)` *(`:5971`)*, quindi l'incremento e'
        ### `-0.5*_sk*omega_clk*_dts`, e il RITMO corrispondente e' quello diviso `DT` --
        ### le stesse unita' di `C2 = arg(<psi_prec|psi>)/DT`.
        ### **NON si ricalcola da `coerenza`, `cs` e `r`: sarebbe una SECONDA scrittura
        ### della stessa legge** *(`9-ter`)*.
        """
        o = np.asarray(omega_clk, float)
        d = (np.asarray(dts, float) if not np.isscalar(dts)
             else np.full(len(o), float(dts)))
        s = (np.asarray(sk, float) if not np.isscalar(sk)
             else np.full(len(o), float(sk)))
        self.attesa_fase = (-0.5 * s * o * d) / self.DT

    # ------------------------------------------------------------- il sito di `cs`
    def _cs(self, net, I, w, cs_nodo):
        """`C4` e `C4s`: la STESSA legge `_cs_nodo`, con le DUE densita', allo STESSO
        istante. ### E `_cs_nodo` incrementa un contatore se `mean(I) <= 1e-30`: lo
        ### VERIFICO PRIMA di chiamarla, e se non torna REGISTRO E SALTO."""
        self.cs_corrente = np.asarray(cs_nodo, float).copy()
        rs = getattr(net, "rho_spin", None)
        self.cs_spin = None
        if rs is None or len(rs) < net.n:
            return
        rs = np.asarray(rs, float)[:net.n]
        if not (float(np.mean(np.maximum(rs, 0.0))) > 1e-30):
            self.cs_salti_lam += 1
            return
        self.cs_spin = np.asarray(net._cs_nodo(rs, w), float).copy()

    # ------------------------------------------------------------- `ritmo()` in entrata
    def _ritmo_in(self, net):
        n = int(net.n)
        self._estendi(n)
        ps = getattr(net, "psi_spin", None)
        psp = getattr(net, "_psi_spin_prec", None)
        medp = getattr(net, "_med_f_prec", None)
        self.rami_prec = {k: int(getattr(net, k, 0)) for k in RAMI}
        d = {"passo": self.passo, "n": n, "nuovi": max(0, n - self.n_prec),
             "med_f_prec": (None if medp is None else float(medp))}
        self.attesa = None
        if (ps is None or psp is None or len(ps) != n or len(psp) != n
                or medp is None):
            d["stato"] = "snapshot o gauge assenti: il ramo di sicurezza"
            self.passi.append(d)
            self.n_prec = n
            return
        ps = np.asarray(ps)[:n]
        psp = np.asarray(psp)[:n]
        med = float(medp)

        c0, f, signed = r_di_oggi(ps, psp, med, self.DT, self.TAU_LOC)
        self.attesa = c0
        c1, ov = angolo_invariante(ps, psp, self.DT)
        c2 = fase_globale(ov, self.DT)
        c3a = fase_componente(ps, psp, 0, self.DT)
        c3b = fase_componente(ps, psp, 1, self.DT)

        # --- S1: riferimento a SE STESSO, sui passi PRECEDENTI (mai il corrente): `A6`
        conta = self.acc["c1_conta"][:n]
        somma = self.acc["c1_somma"][:n]
        media_prec = np.where(conta > 0, somma / np.maximum(conta, 1), np.nan)
        s1 = c1 / np.where(np.isfinite(media_prec) & (media_prec > 0), media_prec, np.nan)

        # --- V1: riferimento ai VICINI
        ii = np.asarray(net.i)
        jj = np.asarray(net.j)
        m = (ii < n) & (jj < n)
        med_vic, gradi = mediana_sui_vicini(c1, ii[m], jj[m], n)
        v1 = c1 / np.where(np.isfinite(med_vic) & (med_vic > 0), med_vic, np.nan)
        disp_vic, _ = mediana_sui_vicini(np.abs(c1 - np.median(c1[np.isfinite(c1)]))
                                         if np.any(np.isfinite(c1)) else c1, ii[m], jj[m], n)

        # --- C4 / C5 dalla CACHE che l'OROLOGIO usa davvero (un passo fa)
        csc = getattr(net, "_cs_nodo_prev", None)
        c4_cache = None
        if csc is not None and len(csc) >= n:
            cc = np.asarray(csc, float)[:n]
            cmv, _ = mediana_sui_vicini(cc, ii[m], jj[m], n)
            c4_cache = {
                "cs_su_CS_M": q(cc / self.CS_M),
                "cs_su_mediana_vicini": q(cc / np.where(np.isfinite(cmv) & (cmv > 0),
                                                        cmv, np.nan)),
                "C5_esp2": q((cc / self.CS_M) ** 2),
                "C5_esp05": q((cc / self.CS_M) ** 0.5),
                "al_floor": None}

        # --- C4 / C4s dallo STESSO istante (dal sito di `cs` del passo precedente)
        c4 = c4s = None
        if self.cs_corrente is not None and len(self.cs_corrente) >= n:
            cc = self.cs_corrente[:n]
            c4 = {"cs_su_CS_M": q(cc / self.CS_M),
                  "C5_esp2": q((cc / self.CS_M) ** 2),
                  "C5_esp05": q((cc / self.CS_M) ** 0.5),
                  "frazione_al_tetto": float(np.mean(cc >= self.CS_M * (1 - 1e-12)))}
        if self.cs_spin is not None and len(self.cs_spin) >= n:
            cs2 = self.cs_spin[:n]
            c4s = {"cs_su_CS_M": q(cs2 / self.CS_M),
                   "C5_esp2": q((cs2 / self.CS_M) ** 2),
                   "C5_esp05": q((cs2 / self.CS_M) ** 0.5),
                   "frazione_al_tetto": float(np.mean(cs2 >= self.CS_M * (1 - 1e-12)))}

        # --- C6: la via di `Z41`, con `dt_n` del passo PRECEDENTE (`A6`)
        c6 = None
        rc = getattr(net, "_r_corrente", None)
        if rc is not None and len(rc) >= n:
            rr = np.asarray(rc, float)[:n]
            dtn = self.DT * np.where(rr > 0, rr, np.nan)
            c6 = np.abs(_wrap2pi(np.angle(ps[:, 0]) - np.angle(psp[:, 0]))) / dtn

        # --- materia / vuoto, e i nodi NEL LORO PRIMO PASSO
        psi = getattr(net, "psi", None)
        I = (np.abs(np.asarray(psi)[:n]) ** 2 if psi is not None and len(psi) >= n
             else np.zeros(n))
        rs = getattr(net, "rho_spin", None)
        RS = (np.asarray(rs, float)[:n] if rs is not None and len(rs) >= n
              else np.zeros(n))
        soglia = float(np.percentile(I, 95)) if n else 0.0
        materia = I >= soglia
        nuovi = np.zeros(n, bool)
        if n > self.n_prec:
            nuovi[self.n_prec:] = True

        def perclasse(v):
            return {"tutti": q(v), "materia": q(v[materia]), "vuoto": q(v[~materia]),
                    "nuovi": q(v[nuovi]) if np.any(nuovi) else {"n": 0}}

        d.update({
            "stato": "misurato",
            "C0": perclasse(c0), "C1": perclasse(c1), "C2": perclasse(c2),
            "C2_abs": perclasse(np.abs(c2)),
            "C3_comp0": perclasse(c3a), "C3_comp1": perclasse(c3b),
            "f": perclasse(f), "mediana_f": float(np.median(np.abs(f))),
            "S1": perclasse(s1), "V1": perclasse(v1),
            "dispersione_C1_fra_vicini": q(disp_vic),
            "C4_stesso_istante": c4, "C4s_stesso_istante": c4s,
            "C4_cache_orologio": c4_cache,
            "C6": (perclasse(c6) if c6 is not None else None),
            "frazione_C0_al_tetto": float(np.mean(c0 >= 1.41421 - 1e-5)),
            "frazione_C0_al_pavimento": float(np.mean(c0 <= 1e-5)),
            "frazione_x_maggiore_1": float(np.mean((f / med) > 1.0)),
            "gradi": q(gradi.astype(float)),
            "pendenza_loglog": {
                "C1_vs_psi2": pendenza_loglog(c1, I),
                "C1_vs_rho_spin": pendenza_loglog(c1, RS),
                "C2_vs_psi2": pendenza_loglog(np.abs(c2), I),
                "C2_vs_rho_spin": pendenza_loglog(np.abs(c2), RS)},
        })

        # --- `C2` CONTRO L'ATTESA DELL'OROLOGIO, con lo SFASAMENTO DI UN PASSO
        att = self.attesa_fase
        self.attesa_fase = None
        if att is not None and len(att) >= n:
            aa = att[:n]
            m2 = np.isfinite(aa) & np.isfinite(c2)
            if int(np.sum(m2)) >= 10:
                x_, y_ = aa[m2], c2[m2]
                sx, sy = x_ - x_.mean(), y_ - y_.mean()
                den = float(np.sqrt(np.sum(sx * sx) * np.sum(sy * sy)))
                cor = (float(np.sum(sx * sy) / den) if den > 0 else None)
                dd = float(np.sum(sx * sx))
                pen = (float(np.sum(sx * sy) / dd) if dd > 0 else None)
                # ### E IN MEDIA LOCALE, perche' `psi_spin` e' il campo EMESSO (somma sui
                #   vicini, `:6240`): la relazione puo' valere SOLO in media locale, e la
                #   media locale e' la STESSA mediana-sui-vicini che usa `V1`.
                av, _ = mediana_sui_vicini(aa, ii[m], jj[m], n)
                cvv, _ = mediana_sui_vicini(c2, ii[m], jj[m], n)
                ml = np.isfinite(av) & np.isfinite(cvv)
                corl = penl = None
                if int(np.sum(ml)) >= 10:
                    xl, yl = av[ml], cvv[ml]
                    sxl, syl = xl - xl.mean(), yl - yl.mean()
                    dl = float(np.sqrt(np.sum(sxl * sxl) * np.sum(syl * syl)))
                    corl = (float(np.sum(sxl * syl) / dl) if dl > 0 else None)
                    ddl = float(np.sum(sxl * sxl))
                    penl = (float(np.sum(sxl * syl) / ddl) if ddl > 0 else None)
                d["C2_contro_attesa"] = {
                    "nodi": int(np.sum(m2)), "correlazione": cor, "pendenza": pen,
                    "correlazione_media_locale": corl, "pendenza_media_locale": penl,
                    "attesa": q(aa[m2]), "C2": q(c2[m2])}
                self.c2_vs_attesa.append(d["C2_contro_attesa"])

        # --- gli accumulatori PER NODO
        fin1 = np.isfinite(c1)
        self.acc["c1_somma"][:n] = np.where(fin1, somma + c1, somma)
        self.acc["c1_conta"][:n] = np.where(fin1, conta + 1, conta)
        self.acc["c1_q"][:n] = np.where(fin1, self.acc["c1_q"][:n] + c1 * c1,
                                        self.acc["c1_q"][:n])
        # ### `C2`: LA COERENZA DI COMPTON NEL POSTO GIUSTO (correzione del guardiano)
        a2 = np.abs(c2)
        f2 = np.isfinite(a2)
        self.acc["c2_somma"][:n] = np.where(f2, self.acc["c2_somma"][:n] + a2,
                                            self.acc["c2_somma"][:n])
        self.acc["c2_conta"][:n] = np.where(f2, self.acc["c2_conta"][:n] + 1,
                                            self.acc["c2_conta"][:n])
        self.acc["c2_q"][:n] = np.where(f2, self.acc["c2_q"][:n] + a2 * a2,
                                        self.acc["c2_q"][:n])
        for ch, sorg in [("r2", self.cs_corrente), ("r2s", self.cs_spin)]:
            if sorg is None or len(sorg) < n:
                continue
            cc2 = sorg[:n]
            rp = a2 / np.where(cc2 > 0, cc2, np.nan)
            fp = np.isfinite(rp)
            self.acc[ch + "_somma"][:n] = np.where(fp, self.acc[ch + "_somma"][:n] + rp,
                                                   self.acc[ch + "_somma"][:n])
            self.acc[ch + "_conta"][:n] = np.where(fp, self.acc[ch + "_conta"][:n] + 1,
                                                   self.acc[ch + "_conta"][:n])
            self.acc[ch + "_q"][:n] = np.where(fp, self.acc[ch + "_q"][:n] + rp * rp,
                                               self.acc[ch + "_q"][:n])

        if c4s is not None and self.cs_spin is not None:
            rap = c1 / np.where(self.cs_spin[:n] > 0, self.cs_spin[:n], np.nan)
            fr = np.isfinite(rap)
            self.acc["rap_somma"][:n] = np.where(fr, self.acc["rap_somma"][:n] + rap,
                                                 self.acc["rap_somma"][:n])
            self.acc["rap_conta"][:n] = np.where(fr, self.acc["rap_conta"][:n] + 1,
                                                 self.acc["rap_conta"][:n])
            self.acc["rap_q"][:n] = np.where(fr, self.acc["rap_q"][:n] + rap * rap,
                                             self.acc["rap_q"][:n])
        # --- autocorrelazione a ritardo 1 degli INCREMENTI DI FASE, per nodo
        inc = c3a
        fi = np.isfinite(inc)
        pr = self.acc["inc_prec"][:n]
        hp = self.acc["inc_conta"][:n] > 0
        usa = fi & hp
        self.acc["inc_cross"][:n] = np.where(usa, self.acc["inc_cross"][:n] + inc * pr,
                                             self.acc["inc_cross"][:n])
        self.acc["inc_somma"][:n] = np.where(fi, self.acc["inc_somma"][:n] + inc,
                                            self.acc["inc_somma"][:n])
        self.acc["inc_q"][:n] = np.where(fi, self.acc["inc_q"][:n] + inc * inc,
                                         self.acc["inc_q"][:n])
        self.acc["inc_conta"][:n] = np.where(fi, self.acc["inc_conta"][:n] + 1,
                                            self.acc["inc_conta"][:n])
        self.acc["inc_prec"][:n] = np.where(fi, inc, pr)

        # --- `psi_spin` ALTERNA fra passi consecutivi?
        if self.ps_t1 is not None and len(self.ps_t1) >= n:
            d1 = np.sqrt(np.sum(np.abs(ps - self.ps_t1[:n]) ** 2, axis=1))
            self.alt["d1"].append(float(np.median(d1)))
            if self.ps_t2 is not None and len(self.ps_t2) >= n:
                d2 = np.sqrt(np.sum(np.abs(ps - self.ps_t2[:n]) ** 2, axis=1))
                self.alt["d2"].append(float(np.median(d2)))
                self.alt["passi"] += 1
        self.ps_t2 = self.ps_t1
        self.ps_t1 = ps.copy()

        self.passi.append(d)
        self.n_prec = n

    # ------------------------------------------------------------- `FEDELTA'`
    def _ritmo_out(self, net, r):
        att = self.attesa
        self.attesa = None
        rami_ora = {k: int(getattr(net, k, 0)) for k in RAMI}
        scattato = [k for k in RAMI if rami_ora.get(k, 0) > self.rami_prec.get(k, 0)]
        if self.passi:
            self.passi[-1]["rami_scattati"] = scattato
        if scattato or att is None or r is None:
            self.fed["saltati_per_ramo"] += 1
            return
        vero = np.asarray(r, float)
        if vero.shape != att.shape:
            self.fed["confronti"] += 1
            self.fed["diversi"] += 1
            self.fed["peggiore"] = {"passo": self.passo, "nota": "forme diverse",
                                    "vero": list(vero.shape), "atteso": list(att.shape)}
            return
        self.fed["confronti"] += 1
        self.fed["nodi"] += int(len(vero))
        ug = (vero == att) | (np.isnan(vero) & np.isnan(att))
        nd = int(np.sum(~ug))
        if nd:
            self.fed["diversi"] += 1
            sc = float(np.nanmax(np.abs(vero - att)))
            if sc > self.fed["max_scarto"]:
                self.fed["max_scarto"] = sc
                self.fed["peggiore"] = {"passo": self.passo, "nodi_diversi": nd,
                                        "nodi": int(len(vero)), "max_scarto": sc}


# =============================================================== IL CENSIMENTO AST
def censimento_ast(path, S):
    """I consumatori di `r`, `dt_n`, `dt_e` -- PER PROVENIENZA, non per nome.

    ### ⛔ IL NOME `r` E' SOVRACCARICO: in `_semina_lam`, `semina`, `_massa`,
    ### `_gusci_esterni`, `chiralita_core_locale` e' un RAGGIO, e in
    ### `batch_condensazione` e' una RIGA DI CSV. Un censimento per NOME conterebbe 14
    ### funzioni invece di 5: un numero gonfiato di 9.
    LA REGOLA: `r` conta come RITMO solo se, nella stessa funzione, e' assegnato da
    `self.ritmo()` oppure da `getattr(self, '_r_corrente', ...)`.
    """
    src = io.open(path, encoding="utf-8").read()
    alb = ast.parse(src)
    dentro = {}
    for nodo in ast.walk(alb):
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for k in range(nodo.lineno, (nodo.end_lineno or nodo.lineno) + 1):
                dentro[k] = nodo.name
    sorgenti = {}       # funzione -> da dove viene `r`
    for nodo in ast.walk(alb):
        if isinstance(nodo, ast.Assign):
            bers = [t.id for t in nodo.targets if isinstance(t, ast.Name)]
            if "r" not in bers:
                continue
            testo = ast.dump(nodo.value)
            fn = dentro.get(nodo.lineno, "<modulo>")
            if "'ritmo'" in testo:
                sorgenti[fn] = ("ritmo()", nodo.lineno)
            elif "_r_corrente" in testo:
                sorgenti[fn] = ("_r_corrente", nodo.lineno)
            else:
                sorgenti.setdefault(fn, ("ALTRO (non il ritmo)", nodo.lineno))
    usi = {}
    for nodo in ast.walk(alb):
        if isinstance(nodo, ast.Name) and nodo.id in ("r", "dt_n", "dt_e", "dtn", "dte",
                                                      "r_node"):
            fn = dentro.get(nodo.lineno, "<modulo>")
            usi.setdefault((nodo.id, fn), []).append(nodo.lineno)
    ritmo_veri, scartati = {}, {}
    for (nome, fn), rr in sorted(usi.items()):
        if nome == "r":
            org = sorgenti.get(fn, ("NON ASSEGNATO qui", None))
            (ritmo_veri if org[0] in ("ritmo()", "_r_corrente") else scartati)[
                (nome, fn)] = {"righe": sorted(rr)[:10], "provenienza": org[0]}
        else:
            ritmo_veri[(nome, fn)] = {"righe": sorted(rr)[:10], "provenienza": "nome di tempo"}
    return {
        "consumatori_del_ritmo": {("%s@%s" % k): v for k, v in ritmo_veri.items()},
        "scartati_perche_NON_sono_il_ritmo": {("%s@%s" % k): v
                                              for k, v in scartati.items()},
        "quanti_veri": len(ritmo_veri), "quanti_scartati": len(scartati),
        "flag": {f: (bool(getattr(S, f)) if isinstance(getattr(S, f, None), bool)
                     else getattr(S, f, None))
                 for f in ["TAU_LOC", "TEMPO_SEGNO", "CAMPO_SPINORIALE", "RITMO_WRAP_2PI",
                           "TEMPO_PROPRIO_ORIENTATO", "SPINORE_CORRETTO",
                           "DEPARAM_OROLOGIO", "STEP2_OROLOGIO", "OROLOGIO_SEGNO",
                           "CS_DINAMICO", "FORK_SU2_MEM", "CS_M", "GAMMA", "GAMMA_TURBO",
                           "DT", "PHI_CRIT"]},
    }


# =============================================================== IL COLLAUDO
def collaudo():
    riga("=")
    stampa("IL COLLAUDO: i casi dove la risposta e' NOTA PRIMA")
    riga("=")
    rng = np.random.default_rng(43)
    DT = 0.01
    esiti = []

    def caso(et, val, atteso, ok):
        esiti.append((et, val, ok))
        stampa("  %-56s %-13.6e  atteso %-14s %s"
               % (et, val, atteso, "OK" if ok else "### NO"))

    # --- POSITIVO: rotazione SU(2) di un angolo NOTO, piu' taglie
    stampa("  POSITIVO -- uno spinore ruotato di un angolo NOTO")
    ok_pos = True
    for N in (7, 100, 5000):
        for ang in (1e-4, 0.01, 0.3, 1.0, 2.0):
            psp = rng.normal(size=(N, 2)) + 1j * rng.normal(size=(N, 2))
            psp /= np.sqrt(np.sum(np.abs(psp) ** 2, axis=1))[:, None]
            # U = exp(-i ang/2 n.sigma) attorno a un asse casuale, PER NODO
            nh = rng.normal(size=(N, 3))
            nh /= np.linalg.norm(nh, axis=1, keepdims=True)
            c, s = np.cos(ang / 2.0), np.sin(ang / 2.0)
            a0, b0 = psp[:, 0], psp[:, 1]
            nx, ny, nz = nh[:, 0], nh[:, 1], nh[:, 2]
            a1 = (c - 1j * s * nz) * a0 + (-1j * s * (nx - 1j * ny)) * b0
            b1 = (-1j * s * (nx + 1j * ny)) * a0 + (c + 1j * s * nz) * b0
            ps = np.stack([a1, b1], axis=1)
            c1, _ = angolo_invariante(ps, psp, DT)
            # ### L'ANGOLO DI FUBINI-STUDY NON E' `ang`: una rotazione SU(2) di `ang`
            #   attorno a un asse generico sposta lo STATO di un angolo che dipende
            #   dall'allineamento fra l'asse e lo spinore. L'invariante VERO e':
            #   2*arccos(|<psp|U psp>|), e |<psp|U psp>| = |cos(ang/2) - i sin(ang/2) n.P|
            #   con P = il vettore di Bloch. Il controllo e' che C1 coincida con QUESTO.
            P = np.stack([2 * np.real(np.conj(a0) * b0),
                          2 * np.imag(np.conj(a0) * b0),
                          np.abs(a0) ** 2 - np.abs(b0) ** 2], axis=1)
            nP = np.sum(nh * P, axis=1)
            fid = np.abs(c - 1j * s * nP)
            att = 2.0 * np.arccos(np.minimum(1.0, fid)) / DT
            sc = float(np.max(np.abs(c1 - att)))
            if not (sc < 1e-6 * max(1.0, float(np.max(att)))):
                ok_pos = False
            stampa("      N=%-6d ang=%-7.4g   max|C1 - atteso| = %.3e   %s"
                   % (N, ang, sc, "OK" if sc < 1e-6 * max(1.0, float(np.max(att)))
                      else "### NO"))
    esiti.append(("POSITIVO: C1 e' l'angolo invariante", 0.0, ok_pos))
    stampa()

    # --- BASE: una rotazione SU(2) COMUNE lascia C1 invariato; C3 DEVE cambiare
    N = 4000
    psp = rng.normal(size=(N, 2)) + 1j * rng.normal(size=(N, 2))
    ps = rng.normal(size=(N, 2)) + 1j * rng.normal(size=(N, 2))
    th = 0.7
    nh = np.array([0.3, -0.5, 0.81])
    nh = nh / np.linalg.norm(nh)
    c, s = np.cos(th / 2.0), np.sin(th / 2.0)
    U = np.array([[c - 1j * s * nh[2], -1j * s * (nh[0] - 1j * nh[1])],
                  [-1j * s * (nh[0] + 1j * nh[1]), c + 1j * s * nh[2]]])
    psR = ps @ U.T
    pspR = psp @ U.T
    c1a, ova = angolo_invariante(ps, psp, DT)
    c1b, ovb = angolo_invariante(psR, pspR, DT)
    caso("BASE -- max|C1 - C1 dopo una SU(2) comune|",
         float(np.max(np.abs(c1a - c1b))), "~0", float(np.max(np.abs(c1a - c1b))) < 1e-9)
    d3 = float(np.max(np.abs(fase_componente(ps, psp, 0, DT)
                             - fase_componente(psR, pspR, 0, DT))))
    caso("BASE -- CASO CHE DEVE FALLIRE: max|C3 - C3 ruotato|", d3, "NON zero", d3 > 1e-6)
    caso("BASE -- e C2 (fase globale) resta invariato",
         float(np.max(np.abs(fase_globale(ova, DT) - fase_globale(ovb, DT)))),
         "~0", float(np.max(np.abs(fase_globale(ova, DT) - fase_globale(ovb, DT)))) < 1e-9)
    stampa()

    # --- FASE GLOBALE: lo stesso e^{i alpha} su ENTRAMBI
    al = 1.234
    c1c, ovc = angolo_invariante(ps * np.exp(1j * al), psp * np.exp(1j * al), DT)
    caso("FASE GLOBALE -- max|C1 - C1 con e^{i alpha} su entrambi|",
         float(np.max(np.abs(c1a - c1c))), "~0",
         float(np.max(np.abs(c1a - c1c))) < 1e-9)
    caso("FASE GLOBALE -- max|C2 - C2 con e^{i alpha} su entrambi|",
         float(np.max(np.abs(fase_globale(ova, DT) - fase_globale(ovc, DT)))), "~0",
         float(np.max(np.abs(fase_globale(ova, DT) - fase_globale(ovc, DT)))) < 1e-9)
    stampa()

    # --- la mediana sui vicini, su un grafo CONTATO A MANO
    ii = np.array([0, 0, 1, 2])
    jj = np.array([1, 2, 3, 3])
    val = np.array([10.0, 20.0, 30.0, 40.0])
    mv, gr = mediana_sui_vicini(val, ii, jj, 4)
    att = np.array([25.0, 10.0, 10.0, 25.0])
    stampa("  MEDIANA SUI VICINI, su un grafo contato a mano")
    stampa("      archi (0-1,0-2,1-3,2-3), val = [10,20,30,40]")
    stampa("      vicini di 0 = {1,2} -> mediana(20,30) = 25    ottenuto %.4f" % mv[0])
    stampa("      vicini di 1 = {0,3} -> mediana(10,40) = 25    ottenuto %.4f" % mv[1])
    att = np.array([25.0, 25.0, 25.0, 25.0])
    ok_mv = bool(np.allclose(mv, att))
    stampa("      atteso [25,25,25,25]  ottenuto %s   %s"
           % (np.round(mv, 4).tolist(), "OK" if ok_mv else "### NO"))
    esiti.append(("mediana sui vicini", 0.0, ok_mv))
    # conte DISPARI
    ii2 = np.array([0, 0, 0])
    jj2 = np.array([1, 2, 3])
    val2 = np.array([0.0, 5.0, 100.0, 7.0])
    mv2, _ = mediana_sui_vicini(val2, ii2, jj2, 4)
    ok_mv2 = abs(mv2[0] - 7.0) < 1e-12
    stampa("      conta DISPARI: vicini di 0 = {1,2,3} val (5,100,7) -> mediana 7"
           "   ottenuto %.4f   %s" % (mv2[0], "OK" if ok_mv2 else "### NO"))
    esiti.append(("mediana sui vicini, conta dispari", 0.0, ok_mv2))
    stampa()

    # --- `r_di_oggi`: la riduzione al gauge, e i due estremi
    stampa("  `r_di_oggi`: i tre valori che il task history ha CALCOLATO prima")
    for et, fv, atteso in [("x -> 0   (f nullo)", 0.0, 0.000001414),
                           ("x = 1    (al gauge)", 1.0, 1.0),
                           ("x -> inf (saturazione)", 1e18, 1.414212977)]:
        psp0 = np.ones((3, 2), complex)
        ang = fv * 1.0 * 0.01       # f = ang/DT = fv  con DT = 0.01
        ps0 = psp0.copy()
        ps0[:, 0] = np.exp(1j * ang)
        got = r_di_oggi(ps0, psp0, 1.0, 0.01, 1.0)[0][0] if fv < 1e17 else None
        if got is None:
            x = 1e18
            rr = x / np.sqrt(1.0 + x**2) + 1.0e-6
            got = 1.0 + 1.0 * (rr / (1.0 / np.sqrt(2.0) + 1.0e-6) - 1.0)
        ok = abs(got - atteso) < 5e-9
        stampa("      %-24s r = %.9f   atteso %.9f   %s"
               % (et, got, atteso, "OK" if ok else "### NO"))
        esiti.append((et, got, ok))
    stampa()

    # --- la pendenza log-log su una legge di potenza NOTA
    xx = np.exp(rng.normal(size=4000))
    yy = 3.0 * xx ** 1.75
    pp = pendenza_loglog(yy, xx)
    ok_p = abs(pp - 1.75) < 1e-9
    stampa("  PENDENZA LOG-LOG su y = 3*x^1.75   ottenuta %.9f   atteso 1.75   %s"
           % (pp, "OK" if ok_p else "### NO"))
    esiti.append(("pendenza log-log", pp, ok_p))
    stampa()

    quanti = sum(1 for e in esiti if e[2])
    stampa("  COLLAUDO: %d casi su %d tornano." % (quanti, len(esiti)))
    if quanti != len(esiti):
        raise SystemExit("[FERMO] il collaudo NON torna: lo strumento non si usa.")
    for ba in (False, True):
        dst, fatte = copia_patchata(ba)
        stampa("  la patch%s: %d ancore, tutte UNICHE  (copia %s)"
               % (" BRACCIO A" if ba else "", len(fatte), blob(dst)[:8]))
        for f in fatte:
            stampa("      - " + f)
    return 0


# =============================================================== LA CORSA
def corsa(passi, braccio_a):
    riga("=")
    stampa("Z43 passo (1): LA DEFINIZIONE DEL TEMPO PROPRIO `r`, MISURATA A LATO%s"
           % ("   [BRACCIO A]" if braccio_a else ""))
    riga("=")
    stampa()
    stampa("### E' UNA MISURA, NON UNA CURA: nessun PASSA/FALLISCE fuori dai controlli,")
    stampa("    e NESSUNA LEGGE NUOVA. La forma la decide Luca dopo il referto.")
    stampa()
    pf = piattaforma()
    for k in ["python", "numpy", "sistema", "macchina"]:
        stampa("  %-10s %s" % (k, pf[k]))
    stampa("  simulatore %s  (sha1 dei byte grezzi, NON toccato)" % blob(SIM)[:8])
    dst, fatte = copia_patchata(braccio_a)
    stampa("  copia patchata: %s  blob %s  (%d ancore)"
           % (os.path.basename(dst), blob(dst)[:8], len(fatte)))
    if braccio_a:
        stampa("  ### BRACCIO A: `omega_clk` con `r_node` -> 1. TOGLIE UNA POTENZA di `r`,")
        stampa("      da r^2 a r^1. NON spezza l'anello: `r` resta in `_dts` (:5939).")
    stampa()

    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                              dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome="sim_z43", sim=dst)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    net = S.net
    in_conf = _cli_flag.dichiara_configurazione(S, stampa)

    R = Raccoglitore(S)
    S._MIS = R
    cens = censimento_ast(dst, S)
    riga()
    stampa("IL CENSIMENTO DALL'AST: i consumatori del RITMO, per PROVENIENZA")
    riga()
    stampa("  consumatori VERI: %d     scartati perche' NON sono il ritmo: %d"
           % (cens["quanti_veri"], cens["quanti_scartati"]))
    for k in sorted(cens["consumatori_del_ritmo"]):
        v = cens["consumatori_del_ritmo"][k]
        stampa("      %-30s %-16s righe %s" % (k[:30], v["provenienza"], v["righe"][:6]))
    stampa("  ### E GLI SCARTATI SONO LA RAGIONE PER CUI NON SI CENSISCE PER NOME:")
    for k in sorted(cens["scartati_perche_NON_sono_il_ritmo"]):
        v = cens["scartati_perche_NON_sono_il_ritmo"][k]
        stampa("      %-30s %s" % (k[:30], v["provenienza"]))
    stampa()
    for f in sorted(cens["flag"]):
        stampa("  %-26s %s" % (f, cens["flag"][f]))
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
        u = R.passi[-1] if R.passi else {}
        mf = u.get("mediana_f")
        c0 = (u.get("C0") or {}).get("tutti") or {}
        print("[battito] passo %d/%d  n=%d  mediana|f|=%s  r mediano=%s  rami=%s"
              % (k, passi, net.n,
                 ("%.4e" % mf) if mf is not None else "n/d",
                 ("%.4f" % c0["mediana"]) if c0.get("mediana") is not None else "n/d",
                 u.get("rami_scattati") or []), flush=True)
    stampa("  passi girati: %d   n finale = %d, archi = %d"
           % (passi, net.n, len(net.i)))
    stampa("  passi registrati: %d   di cui MISURATI: %d"
           % (len(R.passi), sum(1 for p in R.passi if p.get("stato") == "misurato")))
    stampa()

    agg = aggrega(R)
    esito = rapporto(R, agg, cens, in_conf, braccio_a)

    fuori = {"piattaforma": pf, "blob_sim": blob(SIM), "blob_copia": blob(dst),
             "ancore_patch": fatte, "passi": passi, "braccio_a": bool(braccio_a),
             "in_configurazione_del_driver": bool(in_conf),
             "scena": {"nmasse": getattr(a, "nmasse", None),
                       "sep": getattr(a, "sep", None),
                       "n_finale": int(net.n), "archi_finali": int(len(net.i))},
             "censimento_ast": cens, "per_passo": R.passi, "aggregati": agg,
             "controlli": {"FEDELTA": R.fed},
             "cs_salti_lam_degenere": R.cs_salti_lam,
             "timbro_strumento": _timbro()}
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    suf = "_braccioA" if braccio_a else ""
    jp = os.path.join(FUORI, "_z43_tempo_proprio%s.json" % suf)
    io.open(jp, "w", encoding="utf-8", newline=NL).write(
        json.dumps(fuori, indent=1, sort_keys=True, default=str))
    stampa("scritto: " + jp)
    io.open(os.path.join(FUORI, "_corsa%s.txt" % suf), "w", encoding="utf-8",
            newline=NL).write(NL.join(P) + NL)
    return esito


def _timbro():
    t = getattr(_presidio, "timbro", None)
    if t is None:
        return {"nota": "il presidio non espone `timbro`"}
    try:
        d = t(__file__)
        return d if isinstance(d, dict) else {"timbro": str(d)}
    except Exception as e:
        return {"nota": "timbro non leggibile: %r" % (e,)}


def aggrega(R):
    mis = [p for p in R.passi if p.get("stato") == "misurato"]
    if not mis:
        return {}
    out = {"passi_misurati": len(mis)}
    # --- l'ALTALENA: rapporto pari/dispari delle mediane
    def pd(chiave, sotto="tediani"):
        pass
    med_f = [(p["passo"], p["mediana_f"]) for p in mis]
    disp = [v for k, v in med_f if k % 2 == 1]
    pari = [v for k, v in med_f if k % 2 == 0]
    out["mediana_f_per_passo"] = {str(k): v for k, v in med_f}
    out["altalena_mediana_f"] = {
        "dispari_mediana": float(np.median(disp)) if disp else None,
        "pari_mediana": float(np.median(pari)) if pari else None,
        "rapporto_dispari_su_pari": (float(np.median(disp) / np.median(pari))
                                     if disp and pari and np.median(pari) > 0 else None)}
    # il rapporto consecutivo, passo per passo: e' l'ANDAMENTO che conta
    rap = []
    for a, b in zip(med_f, med_f[1:]):
        if b[1] and b[1] > 0:
            rap.append((a[0], float(a[1] / b[1])))
    out["rapporto_consecutivo"] = {str(k): v for k, v in rap}
    for et in ["C0", "C1", "C2_abs", "S1", "V1", "C6", "C3_comp0", "C3_comp1"]:
        serie = [(p["passo"], (p.get(et) or {}).get("tutti", {}).get("mediana"))
                 for p in mis if p.get(et)]
        serie = [(k, v) for k, v in serie if v is not None]
        if not serie:
            continue
        d_ = [v for k, v in serie if k % 2 == 1]
        p_ = [v for k, v in serie if k % 2 == 0]
        out[et] = {
            "mediana_sui_passi": float(np.median([v for _, v in serie])),
            "dispari": float(np.median(d_)) if d_ else None,
            "pari": float(np.median(p_)) if p_ else None,
            "rapporto_dispari_su_pari": (float(np.median(d_) / np.median(p_))
                                         if d_ and p_ and np.median(p_) != 0 else None)}
        for cl in ["materia", "vuoto", "nuovi"]:
            vv = [(p.get(et) or {}).get(cl, {}).get("mediana") for p in mis if p.get(et)]
            vv = [x for x in vv if x is not None]
            out[et][cl] = float(np.median(vv)) if vv else None
    # --- saturazione e pavimento di C0
    for k in ["frazione_C0_al_tetto", "frazione_C0_al_pavimento",
              "frazione_x_maggiore_1"]:
        vv = [p[k] for p in mis if p.get(k) is not None]
        out[k] = {"mediana": float(np.median(vv)) if vv else None,
                  "max": float(max(vv)) if vv else None}
    # --- la dispersione di C1 fra vicini: il rischio `Z37`
    vv = [p["dispersione_C1_fra_vicini"].get("mediana") for p in mis
          if p.get("dispersione_C1_fra_vicini", {}).get("n")]
    out["dispersione_C1_fra_vicini"] = (float(np.median([x for x in vv if x is not None]))
                                        if any(x is not None for x in vv) else None)
    # --- le pendenze log-log
    out["pendenza_loglog"] = {}
    for k in ["C1_vs_psi2", "C1_vs_rho_spin", "C2_vs_psi2", "C2_vs_rho_spin"]:
        vv = [p["pendenza_loglog"][k] for p in mis
              if p.get("pendenza_loglog", {}).get(k) is not None]
        out["pendenza_loglog"][k] = {
            "mediana": float(np.median(vv)) if vv else None,
            "p5": float(np.percentile(vv, 5)) if vv else None,
            "p95": float(np.percentile(vv, 95)) if vv else None,
            "passi": len(vv)}
    # --- COERENZA DI COMPTON: le due CV, per nodo
    n1 = int(np.sum(R.acc["c1_conta"] >= 3))
    nr = int(np.sum(R.acc["rap_conta"] >= 3))
    def cv(somma, quad, conta, soglia=3):
        m = conta >= soglia
        if not np.any(m):
            return None, 0
        mu = somma[m] / conta[m]
        va = np.maximum(quad[m] / conta[m] - mu * mu, 0.0)
        good = np.abs(mu) > 0
        if not np.any(good):
            return None, 0
        c = np.sqrt(va[good]) / np.abs(mu[good])
        return float(np.median(c)), int(np.sum(good))
    cv_c1, nn1 = cv(R.acc["c1_somma"], R.acc["c1_q"], R.acc["c1_conta"])
    cv_rap, nn2 = cv(R.acc["rap_somma"], R.acc["rap_q"], R.acc["rap_conta"])
    out["compton"] = {
        "nodi_con_C1": nn1, "nodi_con_rapporto": nn2,
        "CV_C1_mediana": cv_c1, "CV_rapporto_mediana": cv_rap,
        "CV_rapporto_su_CV_C1": (float(cv_rap / cv_c1)
                                 if (cv_c1 and cv_rap and cv_c1 > 0) else None)}
    # ### LA COERENZA DI COMPTON NEL POSTO GIUSTO: `C2`, non `C1`.
    cv_c2, nc2 = cv(R.acc["c2_somma"], R.acc["c2_q"], R.acc["c2_conta"])
    out["compton_C2"] = {"nodi_con_C2": nc2, "CV_C2_mediana": cv_c2}
    for ch, et in [("r2", "C2_su_C4"), ("r2s", "C2_su_C4s")]:
        cvr, nnr = cv(R.acc[ch + "_somma"], R.acc[ch + "_q"], R.acc[ch + "_conta"])
        out["compton_C2"][et] = {
            "nodi": nnr, "CV_mediana": cvr,
            "CV_su_CV_C2": (float(cvr / cv_c2) if (cv_c2 and cvr and cv_c2 > 0)
                            else None)}
    # ### E QUANTO `C2` SEGUE LA LEGGE CHE L'OROLOGIO GIA' SCRIVE
    if R.c2_vs_attesa:
        v = R.c2_vs_attesa

        def medv(k):
            x = [a[k] for a in v if a.get(k) is not None]
            return float(np.median(x)) if x else None

        out["C2_contro_attesa"] = {
            "passi": len(v),
            "correlazione_mediana": medv("correlazione"),
            "pendenza_mediana": medv("pendenza"),
            "correlazione_media_locale_mediana": medv("correlazione_media_locale"),
            "pendenza_media_locale_mediana": medv("pendenza_media_locale"),
            "attesa_mediana_delle_mediane": float(np.median(
                [a["attesa"]["mediana"] for a in v if a["attesa"].get("n")])),
            "C2_mediana_delle_mediane": float(np.median(
                [a["C2"]["mediana"] for a in v if a["C2"].get("n")]))}
    # --- autocorrelazione a ritardo 1, per nodo
    m = R.acc["inc_conta"] >= 4
    if np.any(m):
        c_, s_, q_, x_ = (R.acc["inc_conta"][m], R.acc["inc_somma"][m],
                          R.acc["inc_q"][m], R.acc["inc_cross"][m])
        mu = s_ / c_
        va = np.maximum(q_ / c_ - mu * mu, 0.0)
        # cross usa c_-1 coppie: approssimazione dichiarata
        cov = x_ / np.maximum(c_ - 1.0, 1.0) - mu * mu
        buoni = va > 0
        ac = cov[buoni] / va[buoni]
        out["autocorr_lag1_incrementi_fase"] = {
            "nodi": int(np.sum(buoni)), "mediana": float(np.median(ac)),
            "p5": float(np.percentile(ac, 5)), "p95": float(np.percentile(ac, 95)),
            "frazione_negativa": float(np.mean(ac < 0))}
    # --- psi_spin alterna?
    if R.alt["passi"] >= 3:
        d1 = np.asarray(R.alt["d1"][-R.alt["passi"]:], float)
        d2 = np.asarray(R.alt["d2"], float)
        k = min(len(d1), len(d2))
        out["psi_spin_alterna"] = {
            "passi": int(k),
            "mediana_distanza_1_passo": float(np.median(d1[-k:])),
            "mediana_distanza_2_passi": float(np.median(d2[-k:])),
            "rapporto_2passi_su_1passo": (float(np.median(d2[-k:]) / np.median(d1[-k:]))
                                          if np.median(d1[-k:]) > 0 else None)}
    return out


def _f(x, k=6):
    return "n/d" if x is None else ("%.*f" % (k, float(x)))


def _e(x, k=4):
    return "n/d" if x is None else ("%.*e" % (k, float(x)))


def rapporto(R, agg, cens, in_conf, braccio_a):
    if not agg:
        stampa("  ### NESSUN PASSO MISURATO: un referto di zeri qui NON significa")
        stampa("      <<non c'e' segnale>>, significa che la misura NON e' avvenuta.")
        return 1
    riga("=")
    stampa("L'ALTALENA: la mediana di |f| per passo")
    riga("=")
    al = agg["altalena_mediana_f"]
    stampa("  mediana sui passi DISPARI  %s" % _e(al["dispari_mediana"]))
    stampa("  mediana sui passi PARI     %s" % _e(al["pari_mediana"]))
    stampa("  rapporto dispari/pari      %s" % _f(al["rapporto_dispari_su_pari"], 2))
    stampa()
    stampa("  IL RAPPORTO CONSECUTIVO, e l'ANDAMENTO e' cio' che conta (non la 3a cifra):")
    rc = agg["rapporto_consecutivo"]
    for k in ["3", "4", "20", "40", "60", "80", "100", "120", "140"]:
        if k in rc:
            stampa("      passo %-4s  med|f|(k)/med|f|(k+1) = %s" % (k, _e(rc[k], 3)))
    stampa()
    riga("=")
    stampa("LE GRANDEZZE, mediana sui passi -- e il rapporto PARI/DISPARI")
    riga("=")
    stampa("  %-10s %-14s %-14s %-14s %-10s %-12s %-12s"
           % ("", "sui passi", "dispari", "pari", "disp/pari", "materia", "vuoto"))
    for et in ["C0", "C1", "C2_abs", "S1", "V1", "C6", "C3_comp0", "C3_comp1"]:
        if et not in agg:
            continue
        d = agg[et]
        stampa("  %-10s %-14s %-14s %-14s %-10s %-12s %-12s"
               % (et, _e(d["mediana_sui_passi"], 3), _e(d["dispari"], 3),
                  _e(d["pari"], 3), _f(d["rapporto_dispari_su_pari"], 2),
                  _e(d.get("materia"), 2), _e(d.get("vuoto"), 2)))
    stampa()
    for et in ["C0", "C1", "S1", "V1"]:
        if et in agg and agg[et].get("nuovi") is not None:
            stampa("  %-6s nodi NEL LORO PRIMO PASSO: mediana %s"
                   % (et, _e(agg[et]["nuovi"], 3)))
    stampa()
    riga("=")
    stampa("LE DUE LEGGI PRATICHE: quanto MORDONO")
    riga("=")
    stampa("  frazione di nodi col `r` AL TETTO (1.414212977)   mediana %s   max %s"
           % (_f(agg["frazione_C0_al_tetto"]["mediana"]),
              _f(agg["frazione_C0_al_tetto"]["max"])))
    stampa("  frazione di nodi col `r` AL PAVIMENTO (1.414e-06) mediana %s   max %s"
           % (_f(agg["frazione_C0_al_pavimento"]["mediana"]),
              _f(agg["frazione_C0_al_pavimento"]["max"])))
    stampa("  frazione di nodi con x > 1 (oltre il gauge)        mediana %s"
           % _f(agg["frazione_x_maggiore_1"]["mediana"]))
    stampa()
    riga("=")
    stampa("COERENZA DI COMPTON: `C1 / C4s` e' COSTANTE nel tempo?")
    riga("=")
    cp = agg["compton"]
    stampa("  nodi con almeno 3 misure di C1: %d    del rapporto: %d"
           % (cp["nodi_con_C1"], cp["nodi_con_rapporto"]))
    stampa("  CV(C1) mediana          %s" % _f(cp["CV_C1_mediana"], 4))
    stampa("  CV(C1/C4s) mediana      %s" % _f(cp["CV_rapporto_mediana"], 4))
    stampa("  CV(rapporto)/CV(C1)     %s" % _f(cp["CV_rapporto_su_CV_C1"], 4))
    stampa("  ### L'IPOTESI NULLA, SCRITTA PRIMA (task history 12ab7f4): se C1 e C4s sono")
    stampa("      indipendenti, CV(rapporto)^2 ~ CV(C1)^2 + CV(C4s)^2, quindi il rapporto")
    stampa("      delle due CV e' >= 1. << 1 vorrebbe dire che la divisione CANCELLA")
    stampa("      varianza, cioe' un candidato f0.")
    stampa()
    riga("=")
    stampa("COERENZA DI COMPTON NEL POSTO GIUSTO: `C2`, non `C1`")
    stampa("### correzione del guardiano del 2026-10-05: l'orologio e' una FASE (`_phc`,")
    stampa("### :5971), e `C1` e' cio' che una fase LASCIA INVARIATO.")
    riga("=")
    cc = agg.get("compton_C2") or {}
    stampa("  nodi con almeno 3 misure di |C2|: %s" % cc.get("nodi_con_C2"))
    stampa("  CV(|C2|) mediana          %s" % _f(cc.get("CV_C2_mediana"), 4))
    for et, nome in [("C2_su_C4", "|C2|/C4   (cs da |psi|^2) "),
                     ("C2_su_C4s", "|C2|/C4s  (cs da rho_spin)")]:
        d = cc.get(et) or {}
        stampa("  CV(%s) mediana %s   su %s nodi"
               % (nome, _f(d.get("CV_mediana"), 4), d.get("nodi")))
        stampa("      ### CV(rapporto)/CV(|C2|) = %s" % _f(d.get("CV_su_CV_C2"), 4))
    stampa("  ### L'IPOTESI NULLA E' LA STESSA scritta per C1 (task history 12ab7f4): se")
    stampa("      le due grandezze sono indipendenti il rapporto delle CV e' >= 1, e << 1")
    stampa("      vorrebbe dire che la divisione CANCELLA varianza, cioe' una f0.")
    stampa("  ### E LA STESSA AVVERTENZA SULLA SATURAZIONE: una CV bassa per saturazione")
    stampa("      sarebbe un FALSO-UNO, e le frazioni al tetto sono riportate sopra.")
    stampa()
    ca = agg.get("C2_contro_attesa")
    if ca:
        riga("=")
        stampa("QUANTO `C2` SEGUE LA LEGGE CHE L'OROLOGIO GIA' SCRIVE")
        riga("=")
        stampa("  attesa = -0.5*_sk*omega_clk*_dts/DT = -0.5*coerenza*(cs/CS_M)^2*r^2")
        stampa("  ### LETTA dalle variabili della legge (:5971), NON ricalcolata.")
        stampa("  ### E SFASATA DI UN PASSO, dichiarato: `_phc` del passo t-1 muove lo")
        stampa("      spinore nell'intervallo che `C2` misura al ritmo_in del passo t.")
        stampa("  passi confrontati: %d" % ca["passi"])
        stampa("  PER NODO        correlazione %s   pendenza %s"
               % (_f(ca["correlazione_mediana"], 4), _f(ca["pendenza_mediana"], 4)))
        stampa("  IN MEDIA LOCALE correlazione %s   pendenza %s"
               % (_f(ca["correlazione_media_locale_mediana"], 4),
                  _f(ca["pendenza_media_locale_mediana"], 4)))
        stampa("      ### `psi_spin` E' IL CAMPO EMESSO (somma sui vicini, :6240), quindi")
        stampa("          la relazione puo' valere SOLO in media locale: le due righe si")
        stampa("          leggono INSIEME, e la SECONDA e' quella pertinente.")
        stampa("  attesa mediana %s   contro C2 mediano %s"
               % (_e(ca["attesa_mediana_delle_mediane"]),
                  _e(ca["C2_mediana_delle_mediane"])))
        stampa()
    riga("=")
    stampa("LA CAUSA DELL'ALTALENA: autocorrelazione a ritardo 1, e `psi_spin`")
    riga("=")
    ac = agg.get("autocorr_lag1_incrementi_fase")
    if ac:
        stampa("  autocorr lag-1 degli incrementi di fase (C3 comp 0), per nodo:")
        stampa("      nodi %d   mediana %s   p5 %s   p95 %s   frazione NEGATIVA %s"
               % (ac["nodi"], _f(ac["mediana"], 4), _f(ac["p5"], 4),
                  _f(ac["p95"], 4), _f(ac["frazione_negativa"], 4)))
        stampa("      ### UN'AUTOCORRELAZIONE NEGATIVA A RITARDO 1 E' LA FIRMA DI UN")
        stampa("          PERIODO 2: il segno si alterna fra passi consecutivi.")
    ps = agg.get("psi_spin_alterna")
    if ps:
        stampa("  `psi_spin` alterna fra passi consecutivi?")
        stampa("      distanza mediana a 1 passo  %s" % _e(ps["mediana_distanza_1_passo"]))
        stampa("      distanza mediana a 2 passi  %s" % _e(ps["mediana_distanza_2_passi"]))
        stampa("      rapporto 2 passi / 1 passo  %s" % _f(ps["rapporto_2passi_su_1passo"], 4))
        stampa("      ### UN RAPPORTO << 1 VORREBBE DIRE CHE psi_spin TORNA INDIETRO: lo")
        stampa("          stato a t somiglia a quello a t-2 piu' che a quello a t-1.")
    stampa()
    riga("=")
    stampa("LA RELAZIONE DI MASSA: pendenza log-log")
    riga("=")
    for k in ["C1_vs_psi2", "C1_vs_rho_spin", "C2_vs_psi2", "C2_vs_rho_spin"]:
        d = agg["pendenza_loglog"][k]
        stampa("  %-18s mediana %s   p5 %s   p95 %s   (su %d passi)"
               % (k, _f(d["mediana"], 4), _f(d["p5"], 4), _f(d["p95"], 4), d["passi"]))
    stampa()
    stampa("  dispersione di C1 fra VICINI (il rischio `Z37`): %s"
           % _e(agg["dispersione_C1_fra_vicini"]))
    stampa("      ### SE FOSSE ~0, `V1` darebbe ~1 per tutti e IL SEGNALE SPARIREBBE --")
    stampa("          che e' esattamente il 98% di `Z37`.")
    stampa()
    riga("=")
    stampa("I CONTROLLI CHE POSSONO FALLIRE")
    riga("=")
    fd = R.fed
    stampa("  FEDELTA'  il mio C0 contro il `r` di ritmo(), AL BIT")
    stampa("      confronti %d   con DIFFERENZE %d   nodi confrontati %d   max scarto %s"
           % (fd["confronti"], fd["diversi"], fd["nodi"], _e(fd["max_scarto"], 3)))
    stampa("      passi SALTATI perche' un ramo di sicurezza e' scattato: %d"
           % fd["saltati_per_ramo"])
    if fd["peggiore"]:
        stampa("      il peggiore: %s" % (fd["peggiore"],))
    stampa("  CONTEGGIO  passi misurati %d   (zero NON e' un'identita')"
           % agg["passi_misurati"])
    stampa("  POSITIVO / BASE / FASE GLOBALE: nel --collaudo, su dati sintetici")
    stampa()
    guasti = []
    if fd["confronti"] == 0:
        guasti.append("FEDELTA' non ha mai confrontato: zero confronti NON e' un'identita'")
    if fd["diversi"]:
        guasti.append("FEDELTA': il mio C0 NON coincide al bit in %d passi su %d "
                      "(max scarto %.3e)" % (fd["diversi"], fd["confronti"],
                                             fd["max_scarto"]))
    if agg["passi_misurati"] == 0:
        guasti.append("nessun passo misurato")
    if not in_conf:
        guasti.append("la configurazione NON e' quella del driver: la misura e' di un "
                      "ALTRO sistema")
    if guasti:
        stampa("  ### I CONTROLLI NON PASSANO, e mi FERMO. Che cosa non torna:")
        for g in guasti:
            stampa("      - " + g)
        stampa("  ### NON AMMORBIDISCO IL CONTROLLO: il mandato dice AL BIT.")
        riga("=")
        return 1
    stampa("  ### I CONTROLLI PASSANO: il mio C0 coincide AL BIT col `r` del simulatore")
    stampa("      su %d nodi, in %d passi." % (fd["nodi"], fd["confronti"]))
    riga("=")
    stampa()
    stampa("### LE SEI VIE NON SI SCELGONO QUI: il referto le riporta tutte, e la forma")
    stampa("    la decide Luca. Questo strumento MISURA.")
    riga("=")
    return 0


def main(argv):
    passi = PASSI
    ba = "--braccio-a" in argv[1:]
    for a in argv[1:]:
        if a.startswith("--passi="):
            passi = int(a.split("=", 1)[1])
    if "--collaudo" in argv[1:]:
        return collaudo()
    return corsa(passi, ba)


if __name__ == "__main__":
    sys.exit(main(sys.argv) or 0)
