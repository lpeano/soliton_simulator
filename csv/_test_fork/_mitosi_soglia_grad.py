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
# ### I TRE SEMI DELLA PERMUTAZIONE, fissati PRIMA della corsa (task history `70b89c5`).
#   ### **Tre e non uno**, perche' con `18` divisioni di riferimento la deviazione di
#   Poisson da sola e' `~sqrt(18) ~ 4.2`, cioe' il `24 %`: un seme solo ### **non distingue
#   `0.5x` da `0.8x`.**
SEMI_PERM = (101, 202, 303)
SOGLIA_P1 = 0.5                  # `>= 0.5` -> il legame NON e' portante
SOGLIA_P2 = 0.2                  # `<= 0.2` -> il legame E' portante
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
def copia_patchata(sorgente, dst, amp=None, tw_split=False, perm_seme=None,
                   perm_identica=False):
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
           if amp is not None else "") + (NL if amp is not None else "")
        + ("_PRNG = np.random.default_rng(%r)   # [Bperm] generatore SEPARATO, MAI self.rng"
           % (perm_seme,) + NL if perm_seme is not None else ""),
        "il gancio di modulo `_MIS`" + ("" if amp is None else " e `_AMP`")
        + ("" if perm_seme is None else " e `_PRNG` (seme %r)" % (perm_seme,)))
    # --- i tre ganci del censimento dei cancelli: LE STESSE ANCORE di `_crescita_dopo_z43`
    if perm_seme is None and not perm_identica:
        uno("            soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_modula))" + NL,
            ("            soglia = soglia0 * (1.0 - %s * np.tanh(grad_modula))"
             % ("_AMP" if amp is not None else "0.3")) + NL
            + "            if _MIS is not None:" + NL
            + "                _MIS.modulazione(self, rn=_rn, grad=grad_modula," + NL
            + "                                 soglia0=soglia0, soglia=soglia)" + NL,
            ("H1 + ### **L'AMPIEZZA**: `0.3` -> `_AMP = %r`" % (amp,)) if amp is not None
            else "H1 (ampiezza INVARIATA)")
    else:
        # ### IL BRACCIO `Bperm`: il MORSO si calcola COME OGGI e poi si PERMUTA.
        #   ### **La distribuzione per passo resta IDENTICA** -- e' la stessa array
        #   riordinata, quindi il multiinsieme e' conservato **per costruzione** -- e
        #   ### **il legame arco-gradiente e' DISTRUTTO.**
        #   ### ⚠ **IL GENERATORE E' SEPARATO** (`_PRNG`), **MAI `self.rng`**: se usasse
        #   quello del simulatore, ogni permutazione CONSUMEREBBE estrazioni e le
        #   `rng.random(len(avv))` della mitosi si sposterebbero -- il confronto non sarebbe
        #   piu' a parita' di dado.
        #   ### ✔ **E con `perm_identica` la permutazione e' `arange`, cioe' un NO-OP
        #   ARITMETICO:** serve a `C-perm-0`, che pretende il byte-identico con `Bp`.
        uno("            soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_modula))" + NL,
            "            _bite = 0.3 * np.tanh(grad_modula)" + NL
            + ("            _p = np.arange(len(_bite))" + NL if perm_identica
               else "            _p = _PRNG.permutation(len(_bite))" + NL)
            + "            _bite_perm = _bite[_p]" + NL
            + "            soglia = soglia0 * (1.0 - _bite_perm)" + NL
            + "            if _MIS is not None:" + NL
            + "                _MIS.modulazione(self, rn=_rn, grad=grad_modula," + NL
            + "                                 soglia0=soglia0, soglia=soglia," + NL
            + "                                 bite=_bite, bite_perm=_bite_perm)" + NL,
            ("### **IL MORSO PERMUTATO** (%s)"
             % ("permutazione IDENTICA: no-op" if perm_identica
                else "generatore SEPARATO, seme %r" % (perm_seme,))))
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

    def modulazione(self, net, rn, grad, soglia0, soglia, bite=None, bite_perm=None):
        g = np.asarray(grad, float)
        self._mod = {"soglia0": float(soglia0), "grad": q(g), "r_nodo": q(rn),
                     "soglia": q(soglia),
                     "morso": q(1.0 - np.asarray(soglia, float) / float(soglia0))}
        # ### `C-distr`: IL MULTIINSIEME DELLE SOGLIE, verificato con un ORDINAMENTO e un
        #   confronto ESATTO. Si tiene un'IMPRONTA per passo -- la somma e lo sha1 dei byte
        #   dell'array ORDINATO -- invece dell'array intero: ### **un confronto esatto su
        #   471 mila valori per 150 passi non entra in un json**, e lo sha1 dei byte
        #   ordinati e' ESATTO (non una statistica).
        _s = np.sort(np.asarray(soglia, float))
        self._mod["soglie_impronta"] = hashlib.sha1(
            np.ascontiguousarray(_s).tobytes()).hexdigest()[:16]
        self._mod["soglie_n"] = int(_s.size)
        if bite is not None:
            _b, _bp = np.asarray(bite, float), np.asarray(bite_perm, float)
            self._mod["bite_impronta"] = hashlib.sha1(
                np.ascontiguousarray(np.sort(_b)).tobytes()).hexdigest()[:16]
            self._mod["bite_perm_impronta"] = hashlib.sha1(
                np.ascontiguousarray(np.sort(_bp)).tobytes()).hexdigest()[:16]
            # ### LA PROVA DIRETTA, per passo: il multiinsieme PRIMA e DOPO la permutazione
            self._mod["bite_multiinsieme_uguale"] = bool(
                _b.size == _bp.size and np.array_equal(np.sort(_b), np.sort(_bp)))

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
        # ### LA GUARDIA E' PER ARCO, NON PER RETE, e la prima corsa ha mostrato perche':
        #   pretendendo `prec["n"] == n` il predittore causale e' uscito SOLO al passo `50`
        #   -- ai passi `100` e `140` la rete era cresciuta nel passo prima e la fotografia
        #   risultava <<non allineata>>, pur essendo valida per quasi tutti gli archi.
        # ### ✔ **ED E' VALIDA, e il perche' si legge dalle regole di nascita:** i NODI si
        #   APPENDONO (`self.phi = concatenate([self.phi, fm])`, `self.phivel` idem:
        #   **nessun `keep` sulle colonne di nodo**), quindi ### **gli indici dei nodi che
        #   c'erano restano QUELLI**. Gli ARCHI invece si filtrano
        #   (`self.i = concatenate([self.i[keep], a, m])`), ma qui non importa: il
        #   predittore indicizza `prec["r"]` con gli indici di NODO CORRENTI, e per un nodo
        #   che esisteva quel valore e' esattamente il suo di allora.
        # ### ⚠ **QUINDI SI USANO GLI ARCHI I CUI DUE ESTREMI ESISTEVANO**, e quelli
        #   esclusi si CONTANO (A8).
        _lp = 0 if prec is None else min(len(prec["r"]), len(prec["phivel"]))
        _vive = ((a_ < _lp) & (b_ < _lp)) if _lp else np.zeros(a_.size, bool)
        if (prec is not None and prec["passo"] == self.passo - 1
                and int(np.sum(_vive)) >= 10):
            d["causale"] = True
            d["passo_del_predittore"] = prec["passo"]
            d["archi_causali"] = int(np.sum(_vive))
            d["archi_esclusi_nati"] = int(a_.size - np.sum(_vive))
            d["n_al_passo_prec"] = int(prec["n"])
            _a2, _b2 = a_[_vive], b_[_vive]
            _rp, _pp = prec["r"], prec["phivel"]
            _g = np.abs(_rp[_a2] - _rp[_b2])
            _PR = (("gradiente_nudo", _g),
                   ("proxy_grad_per_phivel",
                    _g * 0.5 * (np.abs(_pp[_a2]) + np.abs(_pp[_b2]))),
                   ("forma_esatta", np.abs(_rp[_a2] * _pp[_a2] - _rp[_b2] * _pp[_b2])))
            _BE = (("incremento_TOTALE", tot[_vive]), ("SPINTA", sp[_vive]),
                   ("SCARICA", sc[_vive]))
            for np_, pv_ in _PR:
                for nb_, bv_ in _BE:
                    rho, nn = spearman(pv_, bv_)
                    d["spearman"]["%s|%s" % (np_, nb_)] = {"rho": rho, "n": nn}
                    d["quintili"]["%s|%s" % (np_, nb_)] = quintili(pv_, bv_)
        else:
            # ### SI DICHIARA invece di cadere in silenzio sul passo sbagliato (A8).
            d["causale"] = False
            d["perche_non_causale"] = (
                "fotografia assente o troppo pochi archi con due estremi preesistenti: "
                "prec=%s, archi vivi=%s su %d"
                % (None if prec is None else prec["passo"],
                   int(np.sum(_vive)) if _lp else 0, int(a_.size)))
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
    # ### OGNI MODO SCRIVE IL SUO FILE: i json delle corse precedenti sono COMMITTATI, e
    #   ### **un dato committato non si sovrascrive con una corsa diversa.**
    if d.get("perm"):
        _nome, _txt = "soglia_perm.json", "soglia_perm.txt"
    elif d.get("solo_bg"):
        _nome, _txt = "soglia_bg.json", "soglia_bg.txt"
    else:
        _nome, _txt = "soglia.json", "soglia.txt"
    io.open(os.path.join(FUORI, _nome), "w", encoding="utf-8").write(
        json.dumps(d, indent=1, default=str))
    io.open(os.path.join(FUORI, _txt), "w", encoding="utf-8").write(
        NL.join(P) + NL)


def main(argv):
    passi = PASSI
    solo_bg = "--solo-bg" in argv[1:]
    perm = "--perm" in argv[1:]
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
    if perm:
        # ### I QUATTRO BRACCI DI `Bperm`: tre semi piu' la permutazione IDENTICA per
        #   `C-perm-0`. ### **L'ampiezza resta `0.3`**: si randomizza la FORMA, non
        #   l'ampiezza.
        BR = [("Bperm-s%d" % (k + 1), SIM, None, False) for k in range(len(SEMI_PERM))]
        BR.append(("Bperm-id", SIM, None, False))
        stampa("  ### I MORSI RIMESCOLATI: tre semi (%s) piu' la permutazione IDENTICA."
               % ", ".join(str(s) for s in SEMI_PERM))
        stampa("      ### L'AMPIEZZA RESTA 0.3: si randomizza la FORMA, non l'ampiezza.")
        stampa("      ### E il generatore della permutazione e' SEPARATO: mai self.rng,")
        stampa("          cosi' le estrazioni del simulatore restano a parita' di dado.")
    elif solo_bg:
        BR = [("Bg", SIM, None, True)]
        stampa("  ### SOLO IL BRACCIO Bg: gli altri tre non usano il gancio `torsione`,")
        stampa("      quindi il difetto del predittore non li tocca e i loro numeri")
        stampa("      restano quelli committati in dd86933.")
    sorg, mis, S_, N_, anc = {}, {}, {}, {}, {}
    for nome, src, amp, tws in BR:
        dst = os.path.join(FUORI, "_sim_%s.py" % nome.lower().replace("-", "_"))
        if perm:
            _id = nome.endswith("-id")
            _sm = None if _id else SEMI_PERM[int(nome[-1]) - 1]
            anc[nome] = copia_patchata(src, dst, amp=None, tw_split=False,
                                       perm_seme=_sm, perm_identica=_id)
        else:
            anc[nome] = copia_patchata(src, dst, amp=amp, tw_split=tws)
        sorg[nome] = dst
        stampa("  %-5s da %-10s ampiezza %-5s tw_split %-5s -> blob %s  (%d ancore)"
               % (nome, os.path.basename(src), amp, tws, blob(dst)[:8], len(anc[nome])))
    stampa()
    for _nm, _s, _a, _t in BR:
        for f in anc[_nm]:
            stampa("      %s: %s" % (_nm, f))
    stampa()
    for nome, _s, _a, _t in BR:
        S_[nome], N_[nome], a_cli = carica("msg_" + nome, sorg[nome])
        mis[nome] = Misura(nome)
        S_[nome]._MIS = mis[nome]
    # ### IL BRACCIO DI RIFERIMENTO viene da `BR`, non da un nome scritto a mano: e'
    #   l'ULTIMO, cioe' quello piu' vicino a `Bp` in ogni modo (`Bg` col solo nome dei due
    #   termini; `Bperm-id` con la permutazione identica). ### **E' la SECONDA volta che un
    #   nome fisso fa cadere la corsa:** ora la prova del collaudo guarda LA CLASSE.
    _RIF = BR[-1][0]
    in_conf = _cli_flag.dichiara_configurazione(S_[_RIF], stampa)
    stampa("  ### LA CONFIGURAZIONE SI DICHIARA SU `Bg`: e' la PARTE B con la SOLA")
    stampa("      separazione dei nomi, quindi l'unico braccio IN configurazione per")
    stampa("      costruzione. Ap0, Bp0 e B03 hanno l'ampiezza CAMBIATA DI PROPOSITO.")
    n0 = {k: int(N_[k].n) for k in N_}
    stampa("  scena: n = %d, archi = %d" % (N_[_RIF].n, len(N_[_RIF].i)))
    stampa()
    riga("=")
    stampa("LA CORSA: %d passi, %d bracci (%s)"
           % (passi, len(BR), ", ".join(x[0] for x in BR)))
    riga("=")

    def _istantanea(stato, k, err=None):
        d = {"piattaforma": pf, "passi": passi, "passi_girati": k, "stato": stato,
             "solo_bg": bool(solo_bg), "perm": bool(perm),
             "semi_perm": list(SEMI_PERM) if perm else None,
             "soglie_p": {"P1": SOGLIA_P1, "P2": SOGLIA_P2} if perm else None,
             "predittore_causale": all(
                 (mis[_RIF].corr.get(p) or {}).get("causale", False)
                 for p in PASSI_CORR)
             if (_RIF in mis and mis[_RIF].corr) else False,
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
        _nomi = [x[0] for x in BR]
        print("[battito] passo %d/%d  n: %s  nasce: %s"
              % (k, passi,
                 " ".join("%s=%d" % (x, N_[x].n) for x in _nomi),
                 " ".join("%s=%d" % (x, mis[x].passi[-1].get("g4_nasce", 0))
                          for x in _nomi)), flush=True)
        if k % PASSI_SALVA == 0:
            _istantanea("IN CORSO", k)

    comune = _istantanea("DATI SALVATI, rapporto NON ancora girato", passi)
    stampa("  ### I DATI SONO GIA' SALVATI in soglia.json, PRIMA del rapporto.")
    stampa()
    if perm:
        esito, guasti = rapporto_perm(mis, N_, n0, cre, rifB, divB, in_conf, passi)
        d = dict(comune)
        d.update({"esito": esito, "guasti": guasti, "stato": "fatto (perm)"})
        _scrivi(d)
        return esito
    if solo_bg:
        stampa("  ### CON --solo-bg NON SI STAMPA IL RAPPORTO: K1 e i controlli vivono")
        stampa("      nella corsa a quattro bracci (dd86933), e il referto li legge DA LI'.")
        stampa("      Qui si producono SOLO le correlazioni del braccio Bg col predittore")
        stampa("      CAUSALE, e il referto le unisce.")
        for p in PASSI_CORR:
            c = mis[_RIF].corr.get(p) or {}
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


def rapporto_perm(mis, N_, n0, cre, rifB, divB, in_conf, passi):
    """Il rapporto del braccio `Bperm`: `P1`/`P2`/`P3` applicati ### **ALLA MEDIA** dei tre
    semi, piu' la dichiarazione ### **se i tre semi cadono in letture diverse.**"""
    guasti = []
    perB = {r["passo"]: r for r in rifB["passi"]}
    nomi_s = [k for k in mis if k.startswith("Bperm-s")]
    nomi_s.sort()
    fin_B = sum(r.get("g1_e_g2_e_g3", 0) for r in rifB["passi"])

    def _fin(m):
        return sum(r.get("g1_e_g2_e_g3", 0) for r in m.passi)

    riga("=")
    stampa("I MORSI RIMESCOLATI: tre semi contro Bp (18 divisioni, %d nella finestra)"
           % fin_B)
    riga("=")
    stampa("  %-12s %12s %16s %12s %12s"
           % ("braccio", "divisioni", "Sum g1^g2^g3", "div/Bp", "fin/Bp"))
    dv, fn = [], []
    for k in nomi_s:
        d_ = _divisioni(mis[k])
        f_ = _fin(mis[k])
        dv.append(d_)
        fn.append(f_)
        stampa("  %-12s %12d %16d %12s %12s"
               % (k, d_, f_, ("%.4f" % (d_ / divB)) if divB else "n/d",
                  ("%.4f" % (f_ / fin_B)) if fin_B else "n/d"))
    k_id = [k for k in mis if k.endswith("-id")]
    if k_id:
        stampa("  %-12s %12d %16d %12s %12s   (permutazione IDENTICA: deve dare Bp)"
               % (k_id[0], _divisioni(mis[k_id[0]]), _fin(mis[k_id[0]]),
                  ("%.4f" % (_divisioni(mis[k_id[0]]) / divB)) if divB else "n/d",
                  ("%.4f" % (_fin(mis[k_id[0]]) / fin_B)) if fin_B else "n/d"))
    stampa("  %-12s %12d %16d %12s %12s   (RIFERIMENTO, da dd86933)"
           % ("Bp", divB, fin_B, "1.0000", "1.0000"))
    stampa()
    import statistics as _st
    m_dv = sum(dv) / len(dv) if dv else 0.0
    m_fn = sum(fn) / len(fn) if fn else 0.0
    sd_dv = _st.pstdev(dv) if len(dv) > 1 else 0.0
    sd_fn = _st.pstdev(fn) if len(fn) > 1 else 0.0
    stampa("  MEDIA sui %d semi:  divisioni %.2f (dispersione %.2f)   "
           "Sum g1^g2^g3 %.1f (dispersione %.1f)" % (len(dv), m_dv, sd_dv, m_fn, sd_fn))
    r_dv = (m_dv / divB) if divB else None
    r_fn = (m_fn / fin_B) if fin_B else None
    stampa("  RAPPORTI SULLA MEDIA:  divisioni %s   finestra %s"
           % (("%.4f" % r_dv) if r_dv is not None else "n/d",
              ("%.4f" % r_fn) if r_fn is not None else "n/d"))
    stampa()

    def _letto(r):
        if r is None:
            return "n/d"
        if r >= SOGLIA_P1:
            return "P1 (il legame NON e' portante)"
        if r <= SOGLIA_P2:
            return "P2 (il legame E' portante)"
        return "P3 (intermedia)"

    riga("=")
    stampa("P1 / P2 / P3, applicati ALLA MEDIA")
    riga("=")
    stampa("  sulle DIVISIONI (%d eventi di riferimento): %s" % (divB, _letto(r_dv)))
    stampa("  sulla FINESTRA  (%d passi-arco):            %s" % (fin_B, _letto(r_fn)))
    stampa()
    # ### I TRE SEMI CADONO IN LETTURE DIVERSE?
    let_s = [_letto(d_ / divB if divB else None) for d_ in dv]
    let_f = [_letto(f_ / fin_B if fin_B else None) for f_ in fn]
    stampa("  LE LETTURE SEME PER SEME, sulle divisioni: %s" % ", ".join(let_s))
    stampa("  LE LETTURE SEME PER SEME, sulla finestra:  %s" % ", ".join(let_f))
    if len(set(let_s)) > 1:
        stampa("  ### I TRE SEMI CADONO IN LETTURE DIVERSE sulle DIVISIONI: la media va letta")
        stampa("      CON QUESTA RISERVA ACCANTO. Una media che sta fra due letture NON e'")
        stampa("      una terza lettura: e' UN'INCERTEZZA.")
    else:
        stampa("  ### I TRE SEMI CADONO NELLA STESSA LETTURA sulle divisioni: %s" % let_s[0])
    if len(set(let_f)) > 1:
        stampa("  ### E IN LETTURE DIVERSE sulla FINESTRA: %s" % ", ".join(let_f))
    else:
        stampa("  ### E NELLA STESSA LETTURA sulla finestra: %s" % let_f[0])
    if _letto(r_dv) != _letto(r_fn):
        stampa("  ### ⚠ E I DUE CRITERI DISCORDANO -- divisioni contro finestra. VALE QUELLO")
        stampa("      CON PIU' STATISTICA (la finestra, %d contro %d), e LA DISCORDANZA SI"
               % (fin_B, divB))
        stampa("      RIPORTA come risultato, non si risolve scegliendo il piu' comodo.")
    stampa()
    # ### E LA LETTURA VA DETTA NELLA FORMA GIUSTA
    stampa("  ### E SE LE NASCITE RESTANO, LA LETTURA E' <<NON CONTA QUALE ARCO>>, NON")
    stampa("      <<IL GRADIENTE NON CONTA>>: Bperm conserva la distribuzione dei morsi NEL")
    stampa("      TEMPO, quindi il gradiente decide ancora QUANTI morsi grandi ci sono a")
    stampa("      ogni passo. (Limite dichiarato nel task history, 70b89c5.)")
    stampa()
    riga("=")
    stampa("I CONTROLLI")
    riga("=")
    CAMPI = ("archi", "g1_sopra_soglia", "g1_e_g2", "g1_e_g2_e_g3", "prob_positiva",
             "g4_nasce", "n")
    # C-perm-0
    if k_id:
        dd = []
        for r in mis[k_id[0]].passi:
            s = perB.get(r["passo"])
            if s is None:
                continue
            for c in CAMPI:
                if int(r.get(c, -1)) != int(s.get(c, -1)):
                    dd.append((r["passo"], c, r.get(c), s.get(c)))
        ok = (not dd and int(N_[k_id[0]].n) == cre["a_valle"]["n_Bp"])
        stampa("  C-perm-0  %s contro Bp: differenze %d su %d passi, n %d contro %d  -> %s"
               % (k_id[0], len(dd), len(mis[k_id[0]].passi), int(N_[k_id[0]].n),
                  cre["a_valle"]["n_Bp"], "PASSA" if ok else "### FALLISCE"))
        for x in dd[:5]:
            stampa("            passo %s  %s: %s contro %s" % x)
        if not ok:
            guasti.append("C-perm-0")
    # C-distr
    stampa("  C-distr   il multiinsieme dei MORSI, prima e dopo la permutazione:")
    for k in nomi_s + k_id:
        tot = 0
        ug = 0
        for r in mis[k].passi:
            m_ = r.get("mod") or {}
            if "bite_multiinsieme_uguale" in m_:
                tot += 1
                ug += 1 if m_["bite_multiinsieme_uguale"] else 0
        okd = (tot > 0 and ug == tot)
        stampa("            %-12s passi verificati %3d, identici %3d  -> %s"
               % (k, tot, ug, "PASSA" if okd else "### FALLISCE"))
        if not okd:
            guasti.append("C-distr %s" % k)
    # ### E L'IMPRONTA DELLE SOGLIE contro Bp, passo per passo
    stampa("  C-distr   l'impronta delle SOGLIE ordinate contro Bp:")
    for k in nomi_s + k_id:
        div_i = 0
        tot_i = 0
        for r in mis[k].passi:
            s = perB.get(r["passo"])
            m_ = r.get("mod") or {}
            sm = (s or {}).get("mod") or {}
            if "soglie_impronta" in m_ and "soglie_impronta" in sm:
                tot_i += 1
                if m_["soglie_impronta"] != sm["soglie_impronta"]:
                    div_i += 1
        stampa("            %-12s passi confrontati %3d, impronte DIVERSE %3d  -> %s"
               % (k, tot_i, div_i,
                  "identiche" if (tot_i and not div_i) else
                  ("### DIVERSE" if tot_i else "n/d: Bp non porta l'impronta")))
    # C1
    for k in nomi_s + k_id:
        tt_ = mis[k].totali()
        ric = _divisioni(mis[k]) + tt_["schwinger"]
        ok1 = (ric == tt_["nati_tot"])
        stampa("  C1 %-12s %d + %d = %d contro nati %d   %s"
               % (k, _divisioni(mis[k]), tt_["schwinger"], ric, tt_["nati_tot"],
                  "COINCIDE" if ok1 else "### NON COINCIDE"))
        if not ok1:
            guasti.append("C1 %s" % k)
    # C-rng
    stampa("  C-rng     len(avv) contro Bp:")
    for k in nomi_s + k_id:
        primo = None
        for r in mis[k].passi:
            s = perB.get(r["passo"])
            if s is None:
                continue
            if int(r.get("len_avv", -1)) != int(s.get("archi", -2)):
                primo = r["passo"]
                break
        stampa("            %-12s primo passo DIVERSO: %s"
               % (k, primo if primo is not None else "nessuno"))
    stampa()
    riga("=")
    stampa("IL VERDETTO")
    riga("=")
    stampa("  configurazione dichiarata INTERA: %s" % bool(in_conf))
    if guasti:
        stampa("  ### FERMO. I GUASTI:")
        for g in guasti:
            stampa("      - " + g)
        return 1, guasti
    stampa("  ### I CONTROLLI PASSANO.")
    stampa("  ### E QUESTA E' UNA MISURA, NON UN SIGILLO: che fare del 0.3 e' UNA DECISIONE")
    stampa("      DI LUCA.")
    return 0, []


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
    corr = mis[nomi[-1]].corr if (nomi := sorted(mis)) else {}
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
    # ### E IL CASO CHE LA PRIMA CORSA HA TROVATO: LA RETE CRESCE FRA t-1 e t.
    #   La guardia e' PER ARCO, quindi gli archi i cui due estremi esistevano restano
    #   causali, e quelli nati si CONTANO.
    m4 = Misura("crescita")
    m4.passo = PASSI_CORR[0] - 1
    m4.torsione(R2(), spinta=_sp, scarica=np.zeros(_NA), r=r_prec, i=_i, j=_j)

    class R3(object):          # un nodo IN PIU' al passo dopo
        n = _NA + 2
        phivel = np.ones(_NA + 2)
    _i3 = np.concatenate([_i, [_NA]])
    _j3 = np.concatenate([_j, [_NA + 1]])      # un arco NUOVO verso il nodo nato
    r_ora3 = np.concatenate([r_ora, [r_ora[-1] + 1.0]])
    m4.passo = PASSI_CORR[0]
    m4.torsione(R3(), spinta=np.concatenate([_sp, [1.0]]),
                scarica=np.zeros(_NA + 1), r=r_ora3, i=_i3, j=_j3)
    c4 = m4.corr[PASSI_CORR[0]]
    prova("crescita: ### con la rete CRESCIUTA il predittore resta CAUSALE",
          c4.get("causale") is True, "archi causali %s" % c4.get("archi_causali"))
    prova("crescita: ### e l'arco NATO si ESCLUDE e si CONTA",
          c4.get("archi_causali") == _NA and c4.get("archi_esclusi_nati") == 1,
          "%s causali, %s esclusi" % (c4.get("archi_causali"),
                                      c4.get("archi_esclusi_nati")))
    prova("crescita: ### e il segno resta quello causale (+1), non quello sfasato",
          c4["spearman"]["gradiente_nudo|SPINTA"]["rho"] is not None
          and c4["spearman"]["gradiente_nudo|SPINTA"]["rho"] > 0.9,
          "%.6f" % c4["spearman"]["gradiente_nudo|SPINTA"]["rho"])

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

    # --- 8. IL BATTITO: i nomi vengono da `BR`, non da una tupla scritta a mano
    # ### LA PRIMA CORSA CON `--solo-bg` E' CADUTA AL PASSO 1 PER QUESTO: la tupla
    #   `("Ap0", "Bp0", "B03", "Bg")` era fissa, e con un braccio solo `N_["Ap0"]` ALZAVA
    #   `KeyError`. ### **Una prova STRUTTURALE, perche' e' li' che il difetto vive.**
    _tutto = io.open(os.path.abspath(__file__), encoding="utf-8").read()
    _mk = "# " + "=" * 63 + " IL COLLAUDO"
    prova("il marcatore del collaudo e' unico", _tutto.count(_mk) == 1)
    _src = _tutto.split(_mk)[0]
    # ### E L'ASSERZIONE SI LIMITA AL CICLO DEI PASSI: la tupla fissa resta -- e DEVE --
    #   dentro `rapporto()`, che gira SOLO sulla corsa a quattro bracci e li elenca tutti.
    #   ### **La prima versione di questa prova la cercava in TUTTO il sorgente e falliva su
    #   ### un uso LEGITTIMO.**
    _ciclo = _src.split("for k in range(1, passi + 1):")[1].split("comune = _istantanea")[0]
    # ### E LA PROVA GENERALE DELLA CLASSE: in `main` nessun dizionario dei bracci si
    #   indicizza con un NOME SCRITTO A MANO. ### **E' la SECONDA volta che un nome fisso fa
    #   cadere la corsa al primo passo** (prima il battito con la tupla, poi `anc["Bg"]`),
    #   quindi la prova non guarda piu' un punto solo: guarda LA CLASSE.
    _main = _src.split("def main(argv):")[1].split("def _divisioni")[0]
    import re as _re
    _fissi = _re.findall(r'(?:anc|mis|N_|S_|sorg)\["(?:Ap0|Bp0|B03|Bg|Bperm[^"]*)"\]', _main)
    prova("main: ### nessun dizionario dei bracci si indicizza con un nome SCRITTO A MANO",
          not _fissi, "trovati: %s" % (sorted(set(_fissi))[:4] if _fissi else "nessuno"))
    prova("battito: ### nel CICLO DEI PASSI i nomi vengono da `BR`, non da una tupla fissa",
          "_nomi = [x[0] for x in BR]" in _ciclo
          and '("Ap0", "Bp0", "B03", "Bg")' not in _ciclo,
          "con --solo-bg i bracci sono UNO")

    # --- 9. LA PERMUTAZIONE DEI MORSI: conserva il multiinsieme, l'identica e' un no-op
    _g = np.random.default_rng(101)
    _b = _g.random(1000)
    _p = _g.permutation(len(_b))
    prova("perm: il multiinsieme dei morsi e' CONSERVATO (stessa array riordinata)",
          bool(np.array_equal(np.sort(_b), np.sort(_b[_p]))))
    prova("perm: ### e il LEGAME e' distrutto: l'array permutato NON e' quello di partenza",
          not bool(np.array_equal(_b, _b[_p])))
    prova("perm: la permutazione IDENTICA e' un NO-OP ARITMETICO",
          bool(np.array_equal(_b[np.arange(len(_b))], _b)),
          "b[arange(len(b))] E' b")
    # ### E IL GENERATORE SEPARATO NON TOCCA QUELLO DEL SIMULATORE: due `default_rng` con lo
    #   stesso seme danno la stessa sequenza anche se in mezzo un TERZO generatore gira.
    _r1 = np.random.default_rng(11)
    _v1 = [float(_r1.random()) for _ in range(5)]
    _r2 = np.random.default_rng(11)
    _mezzo = np.random.default_rng(999)
    _v2 = []
    for _ in range(5):
        _mezzo.permutation(10000)          # il generatore della permutazione LAVORA
        _v2.append(float(_r2.random()))
    prova("perm: ### un generatore SEPARATO non sposta le estrazioni dell'altro",
          _v1 == _v2, "le due sequenze coincidono")
    # ### LA PATCH: i tre modi danno sorgenti diversi nel modo giusto
    import tempfile
    _d2 = tempfile.mkdtemp()
    _pp = os.path.join(_d2, "p.py")
    _pi = os.path.join(_d2, "i.py")
    copia_patchata(SIM, _pp, amp=None, tw_split=False, perm_seme=101)
    copia_patchata(SIM, _pi, amp=None, tw_split=False, perm_identica=True)
    _tp = io.open(_pp, encoding="utf-8").read()
    _ti = io.open(_pi, encoding="utf-8").read()
    prova("perm: col seme il sorgente ha `_PRNG = np.random.default_rng(101)`",
          "_PRNG = np.random.default_rng(101)" in _tp)
    prova("perm: ### e usa `_PRNG.permutation`, MAI `self.rng`",
          "_PRNG.permutation(len(_bite))" in _tp
          and "self.rng.permutation" not in _tp)
    prova("perm: con la permutazione IDENTICA usa `np.arange` e NON ha `_PRNG`",
          "_p = np.arange(len(_bite))" in _ti
          and "_PRNG = np.random.default_rng" not in _ti)
    prova("perm: ### il morso si calcola COME OGGI, `0.3 * np.tanh(grad_modula)`",
          _tp.count("_bite = 0.3 * np.tanh(grad_modula)") == 1
          and _ti.count("_bite = 0.3 * np.tanh(grad_modula)") == 1)
    prova("perm: ### e la riga originale della soglia NON resta",
          _tp.count("soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_modula))") == 0
          and _ti.count("soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_modula))") == 0)
    # ### i due sorgenti differiscono SOLO per la riga della permutazione
    _a2 = _tp.replace("_PRNG = np.random.default_rng(101)   # [Bperm] generatore SEPARATO, "
                      "MAI self.rng" + NL, "").replace(
        "            _p = _PRNG.permutation(len(_bite))", "            _p = X")
    _b2 = _ti.replace("            _p = np.arange(len(_bite))", "            _p = X")
    prova("perm: ### i due modi differiscono SOLO nella riga della permutazione",
          _a2 == _b2, "il resto del sorgente e' IDENTICO")
    # --- il controllo che DEVE fallire: un morso permutato NON e' quello originale
    _s0 = 3.0 * np.pi
    _so = _s0 * (1.0 - _b)
    _sp = _s0 * (1.0 - _b[_p])
    prova("perm: ### le SOGLIE permutate hanno lo STESSO multiinsieme di quelle originali",
          bool(np.array_equal(np.sort(_so), np.sort(_sp))))
    prova("perm: ### ma NON sono le stesse arco per arco (il legame e' rotto)",
          not bool(np.array_equal(_so, _sp)))
    prova("perm: l'impronta sha1 dei byte ORDINATI coincide, ed e' ESATTA non statistica",
          hashlib.sha1(np.ascontiguousarray(np.sort(_so)).tobytes()).hexdigest()
          == hashlib.sha1(np.ascontiguousarray(np.sort(_sp)).tobytes()).hexdigest())

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
