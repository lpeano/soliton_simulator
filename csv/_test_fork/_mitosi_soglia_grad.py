# -*- coding: utf-8 -*-
"""`MITOSI-SOGLIA-GRAD` **a ampiezza zero**: il `0.3` serve o no?

*(Mandato di Luca del 2026-10-05. Previsioni, criteri `K1`/`K2`/`K2b` e i cinque controlli
sono fissati in `doc/TASK_HISTORY/2026-10-05_mitosi-soglia-grad-ampiezza-zero.md`,
committato **prima** in `bb1fece`, annotato in `1362672`.)*

### IL SIMULATORE NON SI TOCCA: si misura con una **patch**, e la patch tocca **UNA RIGA**
`soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_modula))` *(`:8376`)* diventa
`... (1.0 - _AMP * np.tanh(grad_modula))`, con `_AMP` iniettata.
### **Cosi' `_AMP = 0.3` E' L'ESPRESSIONE ORIGINALE** e `_AMP = 0.0` la annulla.

### I QUATTRO BRACCI
| | | a che serve |
|---|---|---|
| **`Ap0`** | la `PARTE A` *(`062172d3`)*, ampiezza `0` | `K1` |
| **`Bp0`** | la `PARTE B` *(`f7237563`)*, ampiezza `0` | le nascite senza modulazione |
| **`B03`** | la `PARTE B`, ampiezza `0.3` | ### **solo `C0`** |
| **`Bg`** | la `PARTE B`, ampiezza invariata, coi **due termini di `tw` separati** | `K2`, `K2b` |

### ✔ **`Ap` e `Bp` NON SI RIGIRANO:** vengono dal `crescita.json` committato in `12e2ca7`.
### **Confrontare con numeri gia' committati e' piu' forte che rigirarli**, ed e' anche cio'
che rende `C0` severo: il confronto non e' sul solo `n` finale, ma su ### **tutti i conteggi
dei cancelli, a tutti e 150 i passi.**

### LA SEPARAZIONE SPINTA / SCARICA *(obiezione del guardiano)*
```
self.tw  +=  _w8(dph + twist_dip - twp)   -   dt_e * self.tw / _ttw
             \\_________ SPINTA _________/       \\______ SCARICA ______/
```
### **L'ipotesi del doppio conteggio riguarda la SPINTA.** La **SCARICA** cresce col
gradiente per un'altra ragione *(`dt_e = DT*0.5*(r_i+r_j)`)* e ### **va nel verso OPPOSTO**:
correlare il totale ### **mescolerebbe le due cose.**

### I CINQUE CONTROLLI
| | | se fallisce |
|---|---|---|
| **`C0`** *(deve **passare**)* | `B03` riproduce `Bp` **su tutti i conteggi, tutti i passi** | ### **FERMO** |
| **`C-fallisce`** *(deve **fallire**)* | `Bp0` **DEVE** differire da `Bp` | ### **FERMO** |
| **`C1`** | `divisioni + schwinger == nati`, in **ciascun** braccio | ### **FERMO** |
| **`C-rng`** | `len(avv)` identico fra i bracci, e **da quale passo divergono** | ### **FERMO** |
| **`C0-tw`** *(deve **passare**)* | `Bg` riproduce `Bp` *(il solo **nome** dato ai due termini)* | ### **FERMO** |

# ESENTE-H-P3: le COPIE PATCHATE servono perche' `grad_modula`, `soglia`, `_ft`, `nasce`,
#   `ok`, `_no_dens`, `_no_lam` e i due termini di `tw` sono LOCALI, e `_dt_e_ultimo` viene
#   riscritto nello stesso passo: da fuori non si leggono. La scena passa TUTTA dal CLI e la
#   configurazione INTERA si DICHIARA.
# ESENTE-H-P5: la configurazione si dichiara sul braccio `Bg`, che e' la `PARTE B` con la
#   sola separazione dei nomi: l'unico braccio IN configurazione per costruzione.

USO:  python csv/_test_fork/_mitosi_soglia_grad.py  [--passi=N]  [--collaudo]
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
FUORI = os.path.join(RADICE, "csv", "_test_fork", "_mitosi_soglia_grad")
SIM = os.path.join(RADICE, "soliton_simulator.py")
TAG = "pre-z43-cura2-r-da-cs"
# ### il `crescita.json` della corsa committata in `12e2ca7`: `Ap` e `Bp` vengono DA LI'.
CRESCITA = os.path.join(RADICE, "csv", "_test_fork", "_crescita_dopo_z43", "crescita.json")
PASSI = 150
PASSI_SALVA = 10
PASSI_CORR = (50, 100, 140)      # i passi della misura (2), fissati dal mandato
SOGLIA_K1 = 0.8                  # `Ap0 >= 0.8x Ap` -> l'ipotesi su `A` e' REFUTATA
SOGLIA_K2 = 0.05                 # `|Spearman| <= 0.05` a tutti e tre i passi -> REFUTATA
SOGLIA_K2B = 2.0                 # quintile alto / quintile basso della SPINTA
QUANTILI = (0, 1, 5, 25, 50, 75, 95, 99, 100)
# ### i conteggi su cui `C0` confronta B03 con Bp: TUTTI quelli del censimento dei cancelli.
CAMPI_C0 = ("archi", "g1_sopra_soglia", "g1_e_g2", "g1_e_g2_e_g3", "prob_positiva",
            "g4_nasce", "n")

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
    a = np.asarray(v, float)
    a = a[np.isfinite(a)]
    if not a.size:
        return None
    return {("q%03d" % k): float(np.quantile(a, k / 100.0)) for k in QUANTILI}


def _ranghi(x):
    """I ranghi CON LA CORREZIONE PER I PARI MERITO *(ranghi medi)*.

    ### **Serve:** la `SCARICA` e la `SPINTA` hanno molti valori uguali *(zeri)*, e i ranghi
    ### <<ordinali>> darebbero una correlazione **falsa**. Con i ranghi medi la Spearman e'
    la Pearson sui ranghi anche in presenza di pari merito.
    """
    a = np.asarray(x, float)
    n = a.size
    o = np.argsort(a, kind="mergesort")
    r = np.empty(n, float)
    r[o] = np.arange(1, n + 1, dtype=float)
    # i pari merito prendono il rango MEDIO del loro blocco
    s = a[o]
    i = 0
    while i < n:
        j = i
        while j + 1 < n and s[j + 1] == s[i]:
            j += 1
        if j > i:
            r[o[i:j + 1]] = 0.5 * (i + 1 + j + 1)
        i = j + 1
    return r


def spearman(x, y):
    """Spearman = Pearson **sui ranghi medi**. `None` se una delle due e' costante."""
    a, b = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(a) & np.isfinite(b)
    if int(np.sum(m)) < 10:
        return None, int(np.sum(m))
    ra, rb = _ranghi(a[m]), _ranghi(b[m])
    ra = ra - ra.mean()
    rb = rb - rb.mean()
    da = float(np.sqrt(np.sum(ra * ra)))
    db = float(np.sqrt(np.sum(rb * rb)))
    if da <= 0.0 or db <= 0.0:
        return None, int(np.sum(m))
    return float(np.sum(ra * rb) / (da * db)), int(np.sum(m))


def quintili(pred, bers):
    """Gli incrementi MEDIANI del bersaglio per quintile del PREDITTORE.

    ### ⚠ **I quintili si fanno sul PREDITTORE, non sul bersaglio:** ordinare per la
    grandezza che si misura renderebbe il rapporto alto/basso ### **vero per costruzione.**
    """
    a, b = np.asarray(pred, float), np.asarray(bers, float)
    m = np.isfinite(a) & np.isfinite(b)
    a, b = a[m], b[m]
    if a.size < 25:
        return None
    bordi = np.quantile(a, [0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    out = []
    for k in range(5):
        lo, hi = bordi[k], bordi[k + 1]
        sel = (a >= lo) & (a <= hi) if k == 4 else (a >= lo) & (a < hi)
        out.append({"quintile": k + 1, "nodi": int(np.sum(sel)),
                    "pred_mediano": float(np.median(a[sel])) if np.any(sel) else None,
                    "bers_mediano": float(np.median(b[sel])) if np.any(sel) else None})
    return out


# =============================================================== LA COPIA PATCHATA
def copia_patchata(sorgente, dst, amp=None, tw_split=False):
    """Le ancore si **CONTANO** e devono essere **UNICHE** (`P1-quater`)."""
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
        + "_MIS = None   # [MITOSI-SOGLIA-GRAD] lo riempie lo strumento" + NL
        + ("_AMP = %r   # [MITOSI-SOGLIA-GRAD] l'ampiezza della modulazione" % (amp,)
           if amp is not None else "") + (NL if amp is not None else ""),
        "il gancio di modulo `_MIS`" + ("" if amp is None else " e `_AMP`"))
    # --- i tre ganci del censimento dei cancelli: LE STESSE ANCORE di `_crescita_dopo_z43`
    uno("            soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_modula))" + NL,
        ("            soglia = soglia0 * (1.0 - %s * np.tanh(grad_modula))"
         % ("_AMP" if amp is not None else "0.3")) + NL
        + "            if _MIS is not None:" + NL
        + "                _MIS.modulazione(self, rn=_rn, grad=grad_modula," + NL
        + "                                 soglia0=soglia0, soglia=soglia)" + NL,
        ("H1 + ### **L'AMPIEZZA**: `0.3` -> `_AMP = %r`" % (amp,)) if amp is not None
        else "H1 (ampiezza INVARIATA)")
    uno("        c = np.where(nasce)[0]" + NL,
        "        if _MIS is not None:" + NL
        + "            _MIS.catena(self, avv=avv, soglia=soglia, ecc=ecc, salita=salita," + NL
        + "                        discesa=discesa, ft=_ft, segno=segno, resp=resp," + NL
        + "                        prob=prob, nasce=nasce)" + NL
        + "        c = np.where(nasce)[0]" + NL,
        "H2: la catena dei cancelli")
    uno("            ok = ok & _conforme" + NL,
        "            ok = ok & _conforme" + NL
        + "            if _MIS is not None:" + NL
        + "                _MIS.finali(self, c=c, ok=ok, no_dens=_no_dens," + NL
        + "                            no_lam=_no_lam, I=I, dc=_dc, a=a, b=b)" + NL,
        "H3: i cancelli finali, DOPO la congiunzione")
    if tw_split:
        # ### LA SEPARAZIONE: gli STESSI due sotto-espressioni, con un NOME.
        #   `+=` su un ndarray valuta TUTTO il membro destro prima di scrivere, quindi
        #   `_spinta - _scarica` e' la STESSA sottrazione fra gli stessi due valori, e
        #   `self.tw` dentro `_scarica` e' ancora quello di prima. ### BYTE-IDENTICA --
        #   e `C0-tw` lo DIMOSTRA invece di lasciarlo dedurre.
        uno("            self.tw += self._w8(dph + twist_dip - self.twp)"
            " - dt_e * self.tw / _ttw" + NL,
            "            _spinta = self._w8(dph + twist_dip - self.twp)" + NL
            + "            _scarica = dt_e * self.tw / _ttw" + NL
            + "            if _MIS is not None:" + NL
            + "                _MIS.torsione(self, spinta=_spinta, scarica=_scarica," + NL
            + "                              r=r, i=i, j=j)" + NL
            + "            self.tw += _spinta - _scarica" + NL,
            "### **la SEPARAZIONE SPINTA / SCARICA** del ramo `4pi`")
    io.open(dst, "w", encoding="utf-8", newline=NL).write(t)
    return fatte


class Misura(object):
    """Il censimento dei cancelli *(le stesse grandezze di `_crescita_dopo_z43`)* piu' la
    misura `(2)`. ### **LEGGE: non ricalcola nessuna legge.**"""

    def __init__(self, nome):
        self.nome = nome
        self.passo = 0
        self.passi = []
        self._mod = None
        self._cat = None
        self._fin = None
        self.corr = {}          # passo -> le correlazioni
        self._prec = None       # la FOTOGRAFIA di r e phivel del passo PRECEDENTE (COPIE)

    def modulazione(self, net, rn, grad, soglia0, soglia):
        g = np.asarray(grad, float)
        self._mod = {"soglia0": float(soglia0), "grad": q(g), "r_nodo": q(rn),
                     "soglia": q(soglia),
                     "morso": q(1.0 - np.asarray(soglia, float) / float(soglia0))}

    def catena(self, net, avv, soglia, ecc, salita, discesa, ft, segno, resp, prob, nasce):
        avv = np.asarray(avv, float)
        sog = np.asarray(soglia, float)
        sg = np.asarray(segno, float)
        pb = np.asarray(prob, float)
        ns = np.asarray(nasce, bool)
        g1 = avv > sog
        g2 = avv < 4.0 * np.pi
        g3 = sg > 0.0
        self._cat = {"archi": int(avv.size),
                     "g1_sopra_soglia": int(np.sum(g1)),
                     "g2_sotto_tetto": int(np.sum(g2)),
                     "g3_segno_creazione": int(np.sum(g3)),
                     "g1_e_g2": int(np.sum(g1 & g2)),
                     "g1_e_g2_e_g3": int(np.sum(g1 & g2 & g3)),
                     "prob_positiva": int(np.sum(pb > 0.0)),
                     "g4_nasce": int(np.sum(ns)),
                     "len_avv": int(avv.size),
                     "soglia_su_g1": q(sog[g1]),
                     "ft": q(ft), "avv": q(avv), "soglia": q(sog)}

    def finali(self, net, c, ok, no_dens, no_lam, I, dc, a, b):
        _ia, _ib = np.asarray(a, int), np.asarray(b, int)
        _In = np.asarray(I, float)
        rho = 0.5 * (_In[_ia] + _In[_ib]) if _ia.size else np.zeros(0)
        nd = np.asarray(no_dens, bool)
        nl = np.asarray(no_lam, bool)
        self._fin = {"g5_candidati_dopo_mitmax": int(np.size(c)),
                     "rifiutati_solo_densita": int(np.sum(nd & ~nl)),
                     "rifiutati_solo_2lam": int(np.sum(~nd & nl)),
                     "rifiutati_entrambi": int(np.sum(nd & nl)),
                     "ammessi": int(np.sum(np.asarray(ok, bool))),
                     "rho_arco_candidati": q(rho)}

    # ---- LA MISURA (2): i due termini della torsione contro il gradiente
    def torsione(self, net, spinta, scarica, r, i, j):
        """### IL PREDITTORE CAUSALE E' QUELLO DEL PASSO `t-1`, e la prima corsa lo leggeva
        al passo `t` *(difetto annotato in `99782e1`)*.

        ### **IL PERCHE', verificato sull'ordine delle righe di `step()`:** `:7772` calcola
        `dph` dalla **fotografia** `_phi_t`, cioe' dallo stato di **INIZIO** passo, e
        `twp` viene dal passo prima. Quindi
        `spinta_t = _w8(dph_t + twist_dip_t - twp_{t-1})` misura l'avanzamento di fase
        prodotto ### **DURANTE il passo `t-1`** (a `:7769`, con l'`r` e la `phivel` di
        allora). ### **Si salvano le COPIE e si correla col passo dopo.**

        ### ⚠ **COPIE, NON RIFERIMENTI:** un riferimento verrebbe mutato dal passo
        successivo, ed e' esattamente la classe `A8b` di questo repo.
        ### ✔ **E la versione ALLO STESSO PASSO resta, per confronto:** se le due dessero
        risposte diverse, vale solo quella causale -- e il referto mostra entrambe.
        """
        n = int(net.n)
        rr = np.asarray(r, float)
        pv = np.asarray(getattr(net, "phivel", np.zeros(n)), float)
        ii, jj = np.asarray(i, int), np.asarray(j, int)
        # ### LA FOTOGRAFIA PER IL PASSO DOPO: si salva SEMPRE, non solo ai passi di misura.
        #   `self.phivel` qui e' GIA' quella aggiornata (il gancio sta a `:7795`, dopo
        #   `:7768`), cioe' ESATTAMENTE quella che ha prodotto l'avanzamento a `:7769`.
        prec = self._prec
        self._prec = {"passo": self.passo, "n": n,
                      "r": rr.copy(), "phivel": pv.copy()}
        if self.passo not in PASSI_CORR:
            return
        m = (ii < n) & (jj < n) & (ii < len(rr)) & (jj < len(rr)) \
            & (ii < len(pv)) & (jj < len(pv))
        sp = np.abs(np.asarray(spinta, float))[m]
        sc = np.abs(np.asarray(scarica, float))[m]
        tot = np.abs(np.asarray(spinta, float) - np.asarray(scarica, float))[m]
        a_, b_ = ii[m], jj[m]
        BERS = (("incremento_TOTALE", tot), ("SPINTA", sp), ("SCARICA", sc))

        def _pred(rv, pvv):
            g = np.abs(rv[a_] - rv[b_])
            return (("gradiente_nudo", g),
                    ("proxy_grad_per_phivel", g * 0.5 * (np.abs(pvv[a_]) + np.abs(pvv[b_]))),
                    ("forma_esatta", np.abs(rv[a_] * pvv[a_] - rv[b_] * pvv[b_])))

        d = {"archi": int(sp.size), "q_spinta": q(sp), "q_scarica": q(sc),
             "q_totale": q(tot), "spearman": {}, "quintili": {},
             "spearman_stesso_passo": {}, "quintili_stesso_passo": {}}
        # --- (a) LO STESSO PASSO: la versione della prima corsa, tenuta per CONFRONTO
        for np_, pv_ in _pred(rr, pv):
            for nb_, bv_ in BERS:
                rho, nn = spearman(pv_, bv_)
                d["spearman_stesso_passo"]["%s|%s" % (np_, nb_)] = {"rho": rho, "n": nn}
                d["quintili_stesso_passo"]["%s|%s" % (np_, nb_)] = quintili(pv_, bv_)
        # --- (b) IL PASSO PRECEDENTE: ### IL PREDITTORE CAUSALE
        if (prec is not None and prec["passo"] == self.passo - 1
                and prec["n"] == n and len(prec["r"]) >= n and len(prec["phivel"]) >= n):
            d["causale"] = True
            d["passo_del_predittore"] = prec["passo"]
            for np_, pv_ in _pred(prec["r"], prec["phivel"]):
                for nb_, bv_ in BERS:
                    rho, nn = spearman(pv_, bv_)
                    d["spearman"]["%s|%s" % (np_, nb_)] = {"rho": rho, "n": nn}
                    d["quintili"]["%s|%s" % (np_, nb_)] = quintili(pv_, bv_)
        else:
            # ### SI DICHIARA invece di cadere in silenzio sul passo sbagliato (A8).
            d["causale"] = False
            d["perche_non_causale"] = (
                "la fotografia del passo precedente non e' allineata: prec=%s, n=%s contro %s"
                % (None if prec is None else prec["passo"],
                   None if prec is None else prec["n"], n))
            d["spearman"] = dict(d["spearman_stesso_passo"])
            d["quintili"] = dict(d["quintili_stesso_passo"])
        self.corr[self.passo] = d

    def chiudi(self, net, n_prec):
        d = {"passo": self.passo, "n": int(net.n), "archi": int(len(net.i)),
             "nati_tot": int(getattr(net, "nati", 0)),
             "schwinger_tot": int(getattr(net, "_g_nati_schwinger", 0))}
        d.update(self._cat or {"archi": 0, "g4_nasce": 0, "len_avv": 0})
        d["passo"] = self.passo
        d["n"] = int(net.n)
        d["archi_rete"] = int(len(net.i))
        if self._mod is not None:
            d["mod"] = self._mod
        d["fin"] = self._fin or {"ammessi": 0, "stato": "nessun candidato: H3 non scatta"}
        self.passi.append(d)
        self._mod = self._cat = self._fin = None

    def totali(self):
        div = sum(r["fin"].get("ammessi", 0) for r in self.passi)
        return {"divisioni": int(div),
                "schwinger": int(self.passi[-1]["schwinger_tot"]) if self.passi else 0,
                "nati_tot": int(self.passi[-1]["nati_tot"]) if self.passi else 0}


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
    # ### CON `--solo-bg` SI SCRIVE UN FILE A PARTE: il `soglia.json` della corsa a
    #   quattro bracci e' COMMITTATO (`dd86933`), e sovrascriverlo cancellerebbe `K1` e i
    #   controlli. ### **Un dato committato non si sovrascrive con una corsa parziale.**
    _nome = "soglia_bg.json" if d.get("solo_bg") else "soglia.json"
    _txt = "soglia_bg.txt" if d.get("solo_bg") else "soglia.txt"
    io.open(os.path.join(FUORI, _nome), "w", encoding="utf-8").write(
        json.dumps(d, indent=1, default=str))
    io.open(os.path.join(FUORI, _txt), "w", encoding="utf-8").write(
        NL.join(P) + NL)


def main(argv):
    passi = PASSI
    solo_bg = "--solo-bg" in argv[1:]
    if "--collaudo" in argv[1:]:
        riga("=")
        stampa("IL COLLAUDO DI _mitosi_soglia_grad.py")
        riga("=")
        return collaudo()
    for a in argv[1:]:
        if a.startswith("--passi="):
            passi = int(a.split("=", 1)[1])
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    riga("=")
    stampa("MITOSI-SOGLIA-GRAD a ampiezza zero: il 0.3 serve o no?")
    riga("=")
    stampa()
    pf = piattaforma()
    for k in ["python", "numpy", "sistema", "macchina"]:
        stampa("  %-10s %s" % (k, pf[k]))
    stampa("  simulatore (PARTE B) %s   strumento %s" % (blob(SIM)[:8], blob(__file__)[:8]))
    stampa()

    # --- i numeri di `Ap` e `Bp` dal json COMMITTATO
    cre = json.loads(io.open(CRESCITA, encoding="utf-8").read())
    rifA, rifB = cre["bracci"]["Ap"], cre["bracci"]["Bp"]

    def _div(b):
        return sum(r["fin"].get("g5_candidati_dopo_mitmax", 0) for r in b["passi"]) - sum(
            r["fin"].get("rifiutati_solo_densita", 0) + r["fin"].get("rifiutati_solo_2lam", 0)
            + r["fin"].get("rifiutati_entrambi", 0) for r in b["passi"])
    divA, divB = _div(rifA), _div(rifB)
    stampa("  I RIFERIMENTI, dal crescita.json committato (12e2ca7):")
    stampa("      Ap: divisioni %d  schwinger %d  nati %d  n_fin %d  archi %d"
           % (divA, rifA["totali"]["schwinger"], rifA["totali"]["nati_tot"],
              cre["a_valle"]["n_Ap"], cre["a_valle"]["archi_Ap"]))
    stampa("      Bp: divisioni %d  schwinger %d  nati %d  n_fin %d  archi %d"
           % (divB, rifB["totali"]["schwinger"], rifB["totali"]["nati_tot"],
              cre["a_valle"]["n_Bp"], cre["a_valle"]["archi_Bp"]))
    stampa("  ### E NON SI RIGIRANO: confrontare con numeri GIA' COMMITTATI e' piu' forte")
    stampa("      che rigirarli, e rende C0 severo -- il confronto e' su TUTTI i conteggi")
    stampa("      dei cancelli, a TUTTI i passi, non sul solo n finale.")
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
    if blob(sa)[:8] != "062172d3":
        stampa("### IL BLOB DEL BRACCIO A NON E' QUELLO ATTESO (%s). MI FERMO." % blob(sa)[:8])
        _scrivi({"esito": 1, "piattaforma": pf})
        return 1
    stampa("  braccio A dal tag %s: blob %s" % (TAG, blob(sa)[:8]))

    BR = [("Ap0", sa, 0.0, False), ("Bp0", SIM, 0.0, False),
          ("B03", SIM, 0.3, False), ("Bg", SIM, None, True)]
    # ### `--solo-bg`: si rigira SOLO il braccio della misura (2). Gli altri tre non
    #   c'entrano col predittore sfasato, e rigirarli sarebbero due ore buttate.
    if solo_bg:
        BR = [("Bg", SIM, None, True)]
        stampa("  ### SOLO IL BRACCIO Bg: gli altri tre non usano il gancio `torsione`,")
        stampa("      quindi il difetto del predittore non li tocca e i loro numeri")
        stampa("      restano quelli committati in dd86933.")
    sorg, mis, S_, N_, anc = {}, {}, {}, {}, {}
    for nome, src, amp, tws in BR:
        dst = os.path.join(FUORI, "_sim_%s.py" % nome.lower())
        anc[nome] = copia_patchata(src, dst, amp=amp, tw_split=tws)
        sorg[nome] = dst
        stampa("  %-5s da %-10s ampiezza %-5s tw_split %-5s -> blob %s  (%d ancore)"
               % (nome, os.path.basename(src), amp, tws, blob(dst)[:8], len(anc[nome])))
    stampa()
    for f in anc["Bg"]:
        stampa("      Bg: " + f)
    stampa()
    for nome, _s, _a, _t in BR:
        S_[nome], N_[nome], a_cli = carica("msg_" + nome, sorg[nome])
        mis[nome] = Misura(nome)
        S_[nome]._MIS = mis[nome]
    in_conf = _cli_flag.dichiara_configurazione(S_["Bg"], stampa)
    stampa("  ### LA CONFIGURAZIONE SI DICHIARA SU `Bg`: e' la PARTE B con la SOLA")
    stampa("      separazione dei nomi, quindi l'unico braccio IN configurazione per")
    stampa("      costruzione. Ap0, Bp0 e B03 hanno l'ampiezza CAMBIATA DI PROPOSITO.")
    n0 = {k: int(N_[k].n) for k in N_}
    stampa("  scena: n = %d, archi = %d" % (N_["Bg"].n, len(N_["Bg"].i)))
    stampa()
    riga("=")
    stampa("LA CORSA: %d passi, QUATTRO bracci" % passi)
    riga("=")

    def _istantanea(stato, k, err=None):
        d = {"piattaforma": pf, "passi": passi, "passi_girati": k, "stato": stato,
             "solo_bg": bool(solo_bg),
             "predittore_causale": all(
                 (mis["Bg"].corr.get(p) or {}).get("causale", False) for p in PASSI_CORR)
             if ("Bg" in mis and mis["Bg"].corr) else False,
             "blob_sim_b": blob(SIM), "blob_sim_a": blob(sa),
             "blob_strumento": blob(__file__), "ancore": anc, "n0": n0,
             "in_configurazione_del_driver": bool(in_conf),
             "passi_corr": list(PASSI_CORR),
             "soglie": {"K1": SOGLIA_K1, "K2": SOGLIA_K2, "K2b": SOGLIA_K2B},
             "riferimenti": {"Ap": {"divisioni": divA,
                                    "schwinger": rifA["totali"]["schwinger"],
                                    "nati": rifA["totali"]["nati_tot"],
                                    "n_fin": cre["a_valle"]["n_Ap"],
                                    "archi": cre["a_valle"]["archi_Ap"]},
                             "Bp": {"divisioni": divB,
                                    "schwinger": rifB["totali"]["schwinger"],
                                    "nati": rifB["totali"]["nati_tot"],
                                    "n_fin": cre["a_valle"]["n_Bp"],
                                    "archi": cre["a_valle"]["archi_Bp"]}},
             "bracci": {k2: {"passi": m.passi, "totali": m.totali(), "corr": m.corr}
                        for k2, m in mis.items()},
             "a_valle": {k2: {"n": int(N_[k2].n), "archi": int(len(N_[k2].i))}
                         for k2 in N_}}
        if err is not None:
            d["errore"] = err
        _scrivi(d)
        return d

    npre = {k: int(N_[k].n) for k in N_}
    for k in range(1, passi + 1):
        for nome in mis:
            mis[nome].passo = k
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                for nome, _s, _a, _t in BR:
                    _passo.passo_pieno(S_[nome], N_[nome])
            for nome, _s, _a, _t in BR:
                mis[nome].chiudi(N_[nome], npre[nome])
        except Exception as e:
            import traceback
            stampa("### LA CORSA E' CADUTA AL PASSO %d: %r" % (k, e))
            stampa(traceback.format_exc())
            stampa("### MA I DATI DEI %d PASSI PRIMA SONO SALVATI." % (k - 1))
            _istantanea("CADUTA al passo %d" % k, k - 1,
                        err={"passo": k, "errore": repr(e),
                             "traccia": traceback.format_exc()})
            return 1
        npre = {kk: int(N_[kk].n) for kk in N_}
        print("[battito] passo %d/%d  n: %s  nasce: %s"
              % (k, passi,
                 " ".join("%s=%d" % (x, N_[x].n) for x in ("Ap0", "Bp0", "B03", "Bg")),
                 " ".join("%s=%d" % (x, mis[x].passi[-1].get("g4_nasce", 0))
                          for x in ("Ap0", "Bp0", "B03", "Bg"))), flush=True)
        if k % PASSI_SALVA == 0:
            _istantanea("IN CORSO", k)

    comune = _istantanea("DATI SALVATI, rapporto NON ancora girato", passi)
    stampa("  ### I DATI SONO GIA' SALVATI in soglia.json, PRIMA del rapporto.")
    stampa()
    if solo_bg:
        stampa("  ### CON --solo-bg NON SI STAMPA IL RAPPORTO: K1 e i controlli vivono")
        stampa("      nella corsa a quattro bracci (dd86933), e il referto li legge DA LI'.")
        stampa("      Qui si producono SOLO le correlazioni del braccio Bg col predittore")
        stampa("      CAUSALE, e il referto le unisce.")
        for p in PASSI_CORR:
            c = mis["Bg"].corr.get(p) or {}
            stampa("      passo %-4d causale=%-6s predittore dal passo %s"
                   % (p, c.get("causale"), c.get("passo_del_predittore")))
        d = dict(comune)
        d.update({"esito": 0, "guasti": [], "stato": "fatto (solo Bg)"})
        _scrivi(d)
        return 0
    try:
        esito, guasti = rapporto(mis, N_, n0, cre, rifA, rifB, divA, divB, in_conf, passi)
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


def _divisioni(m):
    return m.totali()["divisioni"]


def rapporto(mis, N_, n0, cre, rifA, rifB, divA, divB, in_conf, passi):
    guasti = []
    riga("=")
    stampa("LE NASCITE: i bracci a ampiezza ZERO contro i riferimenti committati")
    riga("=")
    d0 = {k: _divisioni(mis[k]) for k in mis}
    stampa("  %-6s %12s %12s %12s %12s" % ("", "divisioni", "schwinger", "nati", "n finale"))
    for k in ("Ap0", "Bp0", "B03", "Bg"):
        t = mis[k].totali()
        stampa("  %-6s %12d %12d %12d %12d"
               % (k, d0[k], t["schwinger"], t["nati_tot"], int(N_[k].n)))
    stampa("  %-6s %12d %12d %12d %12d  (RIFERIMENTO, da 12e2ca7)"
           % ("Ap", divA, rifA["totali"]["schwinger"], rifA["totali"]["nati_tot"],
              cre["a_valle"]["n_Ap"]))
    stampa("  %-6s %12d %12d %12d %12d  (RIFERIMENTO, da 12e2ca7)"
           % ("Bp", divB, rifB["totali"]["schwinger"], rifB["totali"]["nati_tot"],
              cre["a_valle"]["n_Bp"]))
    stampa()
    rA = (d0["Ap0"] / divA) if divA else None
    rB = (d0["Bp0"] / divB) if divB else None
    stampa("  Ap0/Ap = %s        Bp0/Bp = %s"
           % (("%.4f" % rA) if rA is not None else "n/d",
              ("%.4f" % rB) if rB is not None else "n/d"))
    stampa()
    riga("=")
    stampa("K1 -- se Ap0 >= %.1fx Ap, l'ipotesi <<le nascite di A si reggevano sul 0.3>>"
           % SOGLIA_K1)
    stampa("      e' REFUTATA")
    riga("=")
    k1_ref = (rA is not None and rA >= SOGLIA_K1)
    stampa("  Ap0/Ap = %s   soglia %.1f" % (("%.4f" % rA) if rA is not None else "n/d",
                                            SOGLIA_K1))
    stampa("  ### K1: %s"
           % ("### L'IPOTESI E' REFUTATA: togliere il 0.3 NON abbatte le nascite di A"
              if k1_ref else
              "l'ipotesi NON e' refutata: togliere il 0.3 ABBATTE le nascite di A"))
    stampa("  ### E LA PREVISIONE DEL GUARDIANO era Ap0 < 0.5x Ap: %s"
           % ("CONFERMATA" if (rA is not None and rA < 0.5) else "### NON confermata"))
    stampa("  ### E quella su Bp0 era fra 0.5x e 1.0x di Bp: %s"
           % ("CONFERMATA" if (rB is not None and 0.5 <= rB <= 1.0) else "### NON confermata"))
    stampa()

    # ---------- K2 e K2b ----------
    riga("=")
    stampa("K2 (ESISTENZA) e K2b (ENTITA') -- la misura (2) sul braccio Bg")
    riga("=")
    stampa("  ### K2 DA SOLO E' DEBOLE, e il task history lo dichiara: con ~470 mila archi")
    stampa("      l'errore standard di una Spearman nulla e' ~1/sqrt(N) ~ 0.0015, quindi")
    stampa("      0.05 sta a oltre TRENTA deviazioni standard dallo zero. K2 e' un test di")
    stampa("      ESISTENZA con potenza enorme. ### K2b e' il criterio di ENTITA'.")
    stampa()
    corr = mis["Bg"].corr
    BERS = ("incremento_TOTALE", "SPINTA", "SCARICA")
    PRED = ("gradiente_nudo", "proxy_grad_per_phivel", "forma_esatta")
    stampa("  LE SPEARMAN, per passo (3 predittori x 3 bersagli):")
    stampa("  %-24s %-22s %10s %10s %10s" % ("predittore", "bersaglio", "passo 50",
                                             "passo 100", "passo 140"))
    sp_spinta = {}
    for p_ in PRED:
        for b_ in BERS:
            vals = []
            for k in PASSI_CORR:
                c = corr.get(k) or corr.get(str(k)) or {}
                v = ((c.get("spearman") or {}).get("%s|%s" % (p_, b_)) or {}).get("rho")
                vals.append(v)
            if p_ == "gradiente_nudo" and b_ == "SPINTA":
                sp_spinta = dict(zip(PASSI_CORR, vals))
            stampa("  %-24s %-22s %10s %10s %10s"
                   % (p_, b_,
                      *[("%.6f" % v) if v is not None else "n/d" for v in vals]))
    stampa()
    # K2: sulla SPINTA, col gradiente NUDO (quello che la soglia legge)
    vals = [v for v in sp_spinta.values() if v is not None]
    k2_ref = bool(vals) and all(abs(v) <= SOGLIA_K2 for v in vals)
    stampa("  ### K2 si applica alla SPINTA contro il GRADIENTE NUDO -- il predittore che")
    stampa("      la soglia legge. |rho| ai tre passi: %s"
           % ", ".join(("%.6f" % abs(v)) if v is not None else "n/d"
                       for v in sp_spinta.values()))
    stampa("  ### K2: %s"
           % ("### L'IPOTESI DEL DOPPIO CONTEGGIO E' REFUTATA -- e allora togliere la "
              "modulazione toglierebbe DEL TUTTO l'effetto del gradiente sulla mitosi"
              if k2_ref else "l'ipotesi NON e' refutata: la correlazione ESISTE"))
    stampa()
    stampa("  I QUINTILI DELLA SPINTA per quintile del GRADIENTE NUDO (il predittore):")
    k2b = {}
    for k in PASSI_CORR:
        c = corr.get(k) or corr.get(str(k)) or {}
        qq = (c.get("quintili") or {}).get("gradiente_nudo|SPINTA")
        if not qq:
            stampa("      passo %-4d n/d" % k)
            continue
        lo = qq[0]["bers_mediano"]
        hi = qq[-1]["bers_mediano"]
        rap = (hi / lo) if (lo and lo > 0) else None
        k2b[k] = rap
        stampa("      passo %-4d  q1=%.6e  q2=%.6e  q3=%.6e  q4=%.6e  q5=%.6e   q5/q1 = %s"
               % (k, *[x["bers_mediano"] if x["bers_mediano"] is not None else float("nan")
                       for x in qq],
                  ("%.4f" % rap) if rap is not None else "n/d"))
    ok_k2b = sum(1 for v in k2b.values() if v is not None and v >= SOGLIA_K2B)
    stampa()
    stampa("  ### K2b: il rapporto q5/q1 della SPINTA e' >= %.1f in %d passi su %d"
           % (SOGLIA_K2B, ok_k2b, len(PASSI_CORR)))
    k2b_ril = (ok_k2b >= 2)
    stampa("  ### K2b: %s" % ("### IL DOPPIO CONTEGGIO E' RILEVANTE" if k2b_ril
                              else "il doppio conteggio NON e' rilevante"))
    stampa()
    stampa("  ### LA LETTURA COMBINATA, dalla tavola fissata PRIMA:")
    if k2_ref:
        stampa("      K2 refutato -> ### L'IPOTESI DEL DOPPIO CONTEGGIO E' REFUTATA, e")
        stampa("      togliere la modulazione toglierebbe DEL TUTTO l'effetto del gradiente")
        stampa("      sulla mitosi.")
    elif k2b_ril:
        stampa("      K2 passa, K2b passa -> ### IL DOPPIO CONTEGGIO ESISTE ED E' RILEVANTE.")
    else:
        stampa("      K2 passa, K2b NON passa -> ### <<IL DOPPIO CONTEGGIO ESISTE MA E'")
        stampa("      PICCOLO>>, e la decisione sul 0.3 si legge da K1 e dalle nascite di Bp0.")
    stampa()

    # ---------- I CONTROLLI ----------
    riga("=")
    stampa("I CINQUE CONTROLLI")
    riga("=")
    perB = {r["passo"]: r for r in rifB["passi"]}

    def confronta_con_Bp(nome):
        """Tutti i conteggi dei cancelli, TUTTI i passi, contro `Bp` committato."""
        diff = []
        for r in mis[nome].passi:
            s = perB.get(r["passo"])
            if s is None:
                continue
            for c in CAMPI_C0:
                if int(r.get(c, -1)) != int(s.get(c, -1)):
                    diff.append((r["passo"], c, r.get(c), s.get(c)))
        return diff

    for nome, deve in (("B03", "PASSARE"), ("Bg", "PASSARE")):
        dd = confronta_con_Bp(nome)
        et = "C0" if nome == "B03" else "C0-tw"
        stampa("  %-6s %-5s differenze dai conteggi di Bp su %d passi: %d"
               % (et, nome, len(mis[nome].passi), len(dd)))
        stampa("          n finale %d contro %d   archi %d contro %d"
               % (int(N_[nome].n), cre["a_valle"]["n_Bp"],
                  int(len(N_[nome].i)), cre["a_valle"]["archi_Bp"]))
        ok = (not dd and int(N_[nome].n) == cre["a_valle"]["n_Bp"]
              and int(len(N_[nome].i)) == cre["a_valle"]["archi_Bp"])
        stampa("          ### %s: %s" % (et, "PASSA" if ok else "### FALLISCE"))
        for x in dd[:5]:
            stampa("              passo %s  %s: %s contro %s" % x)
        if not ok:
            guasti.append("%s (%s)" % (et, nome))
    # C-fallisce
    dd = confronta_con_Bp("Bp0")
    diverso = bool(dd) or int(N_["Bp0"].n) != cre["a_valle"]["n_Bp"]
    stampa("  C-fallisce  Bp0 DEVE differire da Bp: differenze %d, n %d contro %d  -> %s"
           % (len(dd), int(N_["Bp0"].n), cre["a_valle"]["n_Bp"],
              "DIFFERISCE (giusto)" if diverso else "### COINCIDE: la patch NON e' agganciata"))
    if dd:
        p0, c0, v0, v1 = dd[0]
        stampa("              la PRIMA differenza: passo %s, %s: %s contro %s"
               % (p0, c0, v0, v1))
    if not diverso:
        guasti.append("C-fallisce: Bp0 coincide con Bp")
    # C1
    for nome in ("Ap0", "Bp0", "B03", "Bg"):
        t = mis[nome].totali()
        ric = t["divisioni"] + t["schwinger"]
        att = t["nati_tot"]
        per_n = int(N_[nome].n) - int(n0[nome])
        ok = (ric == att)
        stampa("  C1 %-5s divisioni %6d + schwinger %5d = %6d   nati %6d   %s   "
               "(n_fin - n_0 = %d)"
               % (nome, t["divisioni"], t["schwinger"], ric, att,
                  "COINCIDE" if ok else "### NON COINCIDE", per_n))
        if not ok:
            guasti.append("C1 %s" % nome)
    # C-rng
    stampa("  C-rng  len(avv) per passo, contro Bp committato:")
    for nome in ("Ap0", "Bp0", "B03", "Bg"):
        primo = None
        for r in mis[nome].passi:
            s = perB.get(r["passo"])
            if s is None:
                continue
            if int(r.get("len_avv", -1)) != int(s.get("archi", -2)):
                primo = r["passo"]
                break
        stampa("          %-5s primo passo con len(avv) DIVERSO da Bp: %s"
               % (nome, primo if primo is not None else "nessuno"))
    stampa("  ### C-rng NON dice <<stesso dado per sempre>>: dice <<stesso dado finche' la")
    stampa("      topologia e' la stessa>>. Il passo in cui divergono E' il numero sopra.")
    stampa()
    riga("=")
    stampa("IL VERDETTO")
    riga("=")
    stampa("  configurazione dichiarata INTERA (braccio Bg): %s" % bool(in_conf))
    if guasti:
        stampa("  ### FERMO. I GUASTI:")
        for g in guasti:
            stampa("      - " + g)
        return 1, guasti
    stampa("  ### I CONTROLLI PASSANO.")
    stampa("  ### E QUESTA E' UNA MISURA, NON UN SIGILLO: la rimozione del 0.3 dal")
    stampa("      simulatore e' UNA DECISIONE DI LUCA, e sara' un prompt a parte.")
    return 0, []


# =============================================================== IL COLLAUDO
def collaudo():
    esiti = []

    def prova(nome, ok, dett=""):
        esiti.append((nome, bool(ok), dett))
        print("  %-6s %-62s %s" % ("OK" if ok else "### KO", nome, dett))

    # --- 1. i ranghi coi PARI MERITO
    r = _ranghi(np.asarray([10.0, 20.0, 20.0, 30.0]))
    prova("ranghi: i pari merito prendono il rango MEDIO (2.5, non 2 e 3)",
          list(r) == [1.0, 2.5, 2.5, 4.0], str(list(r)))
    prova("ranghi: tutti uguali -> tutti lo stesso rango medio",
          list(_ranghi(np.ones(4))) == [2.5] * 4)

    # --- 2. Spearman su casi a risposta NOTA
    x = np.arange(100.0)
    rho, _n = spearman(x, 2.0 * x + 1.0)
    prova("spearman: monotona crescente -> +1 ESATTO", abs(rho - 1.0) < 1e-12, "%.17g" % rho)
    rho, _n = spearman(x, -x)
    prova("spearman: monotona decrescente -> -1 ESATTO", abs(rho + 1.0) < 1e-12,
          "%.17g" % rho)
    rho, _n = spearman(x, x ** 3)
    prova("spearman: monotona NON lineare -> ancora +1 (e' sui RANGHI)",
          abs(rho - 1.0) < 1e-12, "%.17g" % rho)
    rho, _n = spearman(x, np.ones(100))
    prova("spearman: bersaglio COSTANTE -> None, non uno zero finto", rho is None, str(rho))
    rho, _n = spearman(np.arange(5.0), np.arange(5.0))
    prova("spearman: meno di 10 punti -> None (non si inventa una correlazione)",
          rho is None, "n=%d" % _n)

    # --- 3. i quintili: SUL PREDITTORE, e il rapporto q5/q1
    pred = np.arange(1000.0)
    bers = pred * 3.0
    qq = quintili(pred, bers)
    prova("quintili: cinque blocchi, e si fanno sul PREDITTORE", len(qq) == 5,
          "nodi: %s" % [x["nodi"] for x in qq])
    rap = qq[-1]["bers_mediano"] / qq[0]["bers_mediano"]
    prova("quintili: bersaglio = 3*predittore -> q5/q1 = 9.0 (899.5/99.5)",
          abs(rap - 9.0) < 0.2, "%.4f" % rap)
    qq2 = quintili(pred, np.ones(1000))
    rap2 = qq2[-1]["bers_mediano"] / qq2[0]["bers_mediano"]
    prova("quintili: bersaglio COSTANTE -> q5/q1 = 1.0, cioe' K2b NON scatterebbe",
          abs(rap2 - 1.0) < 1e-12, "%.6f" % rap2)
    prova("### e il rapporto 1.0 e' SOTTO la soglia di K2b", rap2 < SOGLIA_K2B,
          "%.2f < %.1f" % (rap2, SOGLIA_K2B))

    # --- 4. LE ANCORE: uniche in ENTRAMBI i bracci
    src_b = io.open(SIM, encoding="utf-8").read()
    g = subprocess.run(["git", "cat-file", "-p", TAG + ":soliton_simulator.py"],
                       capture_output=True, cwd=RADICE)
    src_a = g.stdout.decode("utf-8") if g.returncode == 0 else ""
    ANC = ["import numpy as np" + NL,
           "            soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_modula))" + NL,
           "        c = np.where(nasce)[0]" + NL,
           "            ok = ok & _conforme" + NL,
           "            self.tw += self._w8(dph + twist_dip - self.twp)"
           " - dt_e * self.tw / _ttw" + NL]
    prova("ancore: tutte UNICHE nel braccio B", all(src_b.count(a) == 1 for a in ANC),
          str([src_b.count(a) for a in ANC]))
    prova("ancore: tutte UNICHE anche nel braccio A (il blob del tag)",
          bool(src_a) and all(src_a.count(a) == 1 for a in ANC),
          str([src_a.count(a) for a in ANC]) if src_a else "A non estratto")
    prova("### e il blob del braccio A e' 062172d3",
          bool(src_a) and hashlib.sha1(g.stdout).hexdigest()[:8] == "062172d3",
          hashlib.sha1(g.stdout).hexdigest()[:8] if src_a else "n/d")

    # --- 5. LA PATCH: `_AMP = 0.3` deve ridare L'ESPRESSIONE ORIGINALE
    import tempfile
    d_ = tempfile.mkdtemp()
    p03 = os.path.join(d_, "a03.py")
    p00 = os.path.join(d_, "a00.py")
    pgg = os.path.join(d_, "agg.py")
    copia_patchata(SIM, p03, amp=0.3)
    copia_patchata(SIM, p00, amp=0.0)
    copia_patchata(SIM, pgg, amp=None, tw_split=True)
    t03 = io.open(p03, encoding="utf-8").read()
    t00 = io.open(p00, encoding="utf-8").read()
    tgg = io.open(pgg, encoding="utf-8").read()
    prova("patch: con amp=0.3 il sorgente contiene `_AMP = 0.3`", "_AMP = 0.3" in t03)
    prova("patch: con amp=0.0 il sorgente contiene `_AMP = 0.0`", "_AMP = 0.0" in t00)
    prova("patch: la riga della soglia usa `_AMP` in entrambi",
          t03.count("1.0 - _AMP * np.tanh(grad_modula)") == 1
          and t00.count("1.0 - _AMP * np.tanh(grad_modula)") == 1)
    prova("patch: ### il `0.3` LETTERALE non resta nella riga della soglia",
          t03.count("1.0 - 0.3 * np.tanh(grad_modula)") == 0)
    # ### LA PRIMA VERSIONE DI QUESTA PROVA CERCAVA `"_AMP" not in tgg` E FALLIVA:
    #   `_AMP` e' SOTTOSTRINGA di nomi che il simulatore ha gia' -- `SCALA_AMP` (`:341`),
    #   `GRAV_AMPIEZZA` (`:3175`). ### **Il codice era giusto e l'asserzione era larga.**
    #   Si cerca il TESTO INIETTATO, non una sottostringa.
    prova("patch: con tw_split l'ampiezza resta il `0.3` LETTERALE (braccio Bg)",
          tgg.count("1.0 - 0.3 * np.tanh(grad_modula)") == 1
          and "_AMP * np.tanh" not in tgg
          and "[MITOSI-SOGLIA-GRAD] l'ampiezza" not in tgg,
          "Bg non tocca l'ampiezza")
    prova("patch: con tw_split ci sono `_spinta` e `_scarica`, e la somma e' invariata",
          tgg.count("_spinta = self._w8(dph + twist_dip - self.twp)") == 1
          and tgg.count("_scarica = dt_e * self.tw / _ttw") == 1
          and tgg.count("self.tw += _spinta - _scarica") == 1)
    prova("patch: ### senza tw_split la riga di `tw` NON si tocca",
          t03.count("self.tw += self._w8(dph + twist_dip - self.twp)"
                    " - dt_e * self.tw / _ttw") == 1)
    # ### E LA PROVA CHE CONTA: i due sorgenti differiscono SOLO per l'ampiezza
    _a = t03.replace("_AMP = 0.3", "_AMP = X")
    _b = t00.replace("_AMP = 0.0", "_AMP = X")
    prova("### patch: amp=0.3 e amp=0.0 differiscono SOLO nella riga di `_AMP`",
          _a == _b, "il resto del sorgente e' IDENTICO")
    # e l'aritmetica: 1 - 0.3*tanh(x) deve essere IDENTICA al bit
    xx = np.linspace(0.0, 3.0, 100001)
    _AMP = 0.3
    prova("### patch: `1 - _AMP*tanh(x)` con _AMP=0.3 e' IDENTICO AL BIT a `1 - 0.3*tanh(x)`",
          bool(np.all((1.0 - _AMP * np.tanh(xx)) == (1.0 - 0.3 * np.tanh(xx)))),
          "su 100001 punti")
    prova("### patch: con _AMP=0.0 la soglia e' soglia0 ESATTO",
          bool(np.all((1.0 - 0.0 * np.tanh(xx)) == 1.0)), "su 100001 punti")

    # --- 6. la Misura: i cancelli e i due termini
    m = Misura("prova")
    m.passo = PASSI_CORR[0]

    class FintaRete(object):
        n = 4
        phivel = np.asarray([1.0, 2.0, 3.0, 4.0])
    m.torsione(FintaRete(), spinta=np.asarray([1.0, 2.0, 3.0]),
               scarica=np.asarray([0.5, 0.5, 0.5]),
               r=np.asarray([0.1, 0.4, 0.9, 1.0]),
               i=np.asarray([0, 1, 2]), j=np.asarray([1, 2, 3]))
    c = m.corr[PASSI_CORR[0]]
    prova("torsione: registra SPINTA, SCARICA e TOTALE separati",
          all(k in c for k in ("q_spinta", "q_scarica", "q_totale")))
    prova("torsione: ### il TOTALE e' |spinta - scarica|, non |spinta| + |scarica|",
          abs(c["q_totale"]["q050"] - 1.5) < 1e-12, "%.6f" % c["q_totale"]["q050"])
    prova("torsione: tre predittori x tre bersagli = 9 combinazioni",
          len(c["spearman"]) == 9, "%d" % len(c["spearman"]))
    prova("torsione: ### e NON registra ai passi fuori da PASSI_CORR",
          (lambda: (setattr(m, "passo", 7),
                    m.torsione(FintaRete(), np.ones(3), np.ones(3),
                               np.ones(4), np.asarray([0, 1, 2]), np.asarray([1, 2, 3])),
                    7 not in m.corr)[-1])())

    # --- 7. IL PREDITTORE CAUSALE: deve venire dal passo t-1
    # ### LA PROVA E' COSTRUITA PERCHE' LE DUE VERSIONI DIANO SEGNI OPPOSTI: al passo `t-1`
    #   il gradiente CRESCE con l'indice dell'arco, al passo `t` DECRESCE, e la `spinta`
    #   cresce. ### **Quindi il predittore causale da' Spearman +1 e quello allo stesso
    #   passo -1:** se il gancio leggesse il passo sbagliato, ### **il SEGNO si
    #   rovescerebbe**, e nessun valore intermedio puo' confondere i due casi.
    # ### ⚠ **E I QUINTILI VOGLIONO UN PREDITTORE NON COSTANTE:** con un gradiente costante
    #   i cinque bordi coincidono e i primi quattro quintili restano VUOTI. La prima
    #   versione di questa prova usava un gradiente costante e `pred_mediano` veniva `None`.
    _NA = 30
    class R2(object):
        n = _NA + 1
        phivel = np.ones(_NA + 1)
    m2 = Misura("causale")
    _i = np.arange(_NA)
    _j = np.arange(1, _NA + 1)
    _sp = 1.0 + np.arange(_NA, dtype=float)                 # la spinta CRESCE
    # passo t-1: i salti sono 1, 2, 3, ... -> il gradiente CRESCE con l'indice
    r_prec = np.concatenate([[0.0], np.cumsum(1.0 + np.arange(_NA, dtype=float))])
    m2.passo = PASSI_CORR[0] - 1
    m2.torsione(R2(), spinta=_sp, scarica=np.zeros(_NA), r=r_prec, i=_i, j=_j)
    prova("causale: al passo t-1 salva la fotografia e NON registra la correlazione",
          m2._prec is not None and (PASSI_CORR[0] - 1) not in m2.corr,
          "prec al passo %s" % m2._prec["passo"])
    prova("causale: ### e la fotografia e' una COPIA, non un riferimento",
          m2._prec["r"] is not r_prec and bool(np.all(m2._prec["r"] == r_prec)))
    # passo t: i salti sono 30, 29, 28, ... -> il gradiente DECRESCE
    r_ora = np.concatenate([[0.0], np.cumsum(float(_NA) - np.arange(_NA, dtype=float))])
    m2.passo = PASSI_CORR[0]
    m2.torsione(R2(), spinta=_sp, scarica=np.zeros(_NA), r=r_ora, i=_i, j=_j)
    c2 = m2.corr[PASSI_CORR[0]]
    prova("causale: al passo di misura registra, e DICHIARA di essere causale",
          c2.get("causale") is True
          and c2.get("passo_del_predittore") == PASSI_CORR[0] - 1,
          "predittore dal passo %s" % c2.get("passo_del_predittore"))
    prova("causale: ### e tiene ENTRAMBE le versioni, per confronto",
          bool(c2.get("spearman")) and bool(c2.get("spearman_stesso_passo")))
    _rc = c2["spearman"]["gradiente_nudo|SPINTA"]["rho"]
    _rs = c2["spearman_stesso_passo"]["gradiente_nudo|SPINTA"]["rho"]
    prova("causale: ### il predittore CAUSALE (passo t-1) da' Spearman +1",
          _rc is not None and abs(_rc - 1.0) < 1e-12, "%.17g" % _rc)
    prova("causale: ### e quello ALLO STESSO PASSO da' -1: IL SEGNO SI ROVESCIA",
          _rs is not None and abs(_rs + 1.0) < 1e-12, "%.17g" % _rs)
    prova("causale: ### quindi un gancio sul passo sbagliato sarebbe VISIBILE dal segno",
          _rc * _rs < 0, "+1 contro -1")
    # il caso che DEVE dichiararsi NON causale: fotografia non allineata
    m3 = Misura("salto")
    m3.passo = PASSI_CORR[0]
    m3.torsione(R2(), spinta=_sp, scarica=np.zeros(_NA), r=r_ora, i=_i, j=_j)
    prova("causale: ### senza la fotografia del passo prima si DICHIARA non causale",
          m3.corr[PASSI_CORR[0]].get("causale") is False
          and "perche_non_causale" in m3.corr[PASSI_CORR[0]],
          m3.corr[PASSI_CORR[0]].get("perche_non_causale", "")[:46])
    prova("causale: ### e in quel caso ricade sullo STESSO PASSO, dichiarandolo",
          m3.corr[PASSI_CORR[0]]["spearman"]
          == m3.corr[PASSI_CORR[0]]["spearman_stesso_passo"])

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
