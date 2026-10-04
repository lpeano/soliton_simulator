# -*- coding: utf-8 -*-
"""IL TETTO CAUSALE: tempo COORDINATO (`DT`) contro tempo PROPRIO dell'arco (`dt_e`).

*(`TETTO-CAUSALE-TEMPO-COORDINATO`, passo **(1): LA MISURA**. Mandato di Luca del
2026-10-04. Task history: `doc/TASK_HISTORY/2026-10-04_tetto-causale-tempo-coordinato-misura.md`,
committato PRIMA.)*

### ⛔ **E' UNA MISURA, NON UNA CURA.** Nessun `PASSA`/`FALLISCE` **oltre al controllo**:
### solo numeri. Il simulatore **non si tocca** -- la misura vive in una **COPIA PATCHATA**.

### I SITI, censiti DALL'AST e non per riga *(par.2)*, coi rami spenti
| sito | che cos'e' | guardia | gira col driver |
|---|---|---|---|
| `:9203` | **CLIP** `clip(spinta, +-c_sistema*DT)` | `GRAV_BIFASE and len(proj)` + `VIRIALE` | **SI** |
| `:9209` | `clip(grav, ...)` | **ELSE di `VIRIALE`** | **NO** |
| `:9340` | **SCALA** `_delta_coes = (_csa*DT) * _F_adim` | `COES_ADIM` + `COES_CAUSALE` | **SI** |
| `:9341` | il **confronto** `_glob` | idem | **SI** |
| `:9351` | `LAM*sqrt(K_C)*DT` | **ELSE di `COES_CAUSALE`** | **NO** |

### ⛔ **I DUE SITI CHE GIRANO HANNO NATURA DIVERSA, e misurarli con la stessa domanda
### sarebbe un errore che produce numeri invece di vedersi.**
`:9203` e' un **CLIP**: *«quanti archi LIMITA»* e' ben definito *(`|spinta| > p`)*.
`:9340` e' una **SCALA**: `|_F_adim| <= 1` per costruzione, quindi il tetto **non limita, lo
FISSA** -- cambiare `DT -> dt_e` li' moltiplica `_delta_coes` per `dt_e/DT` su **OGNI** arco.
### ➜ Per `:9340` le domande giuste sono la **distribuzione di `dt_e/DT`** e il conteggio di
`|_F_adim| > 0.99` *(l'analogo di <<al tetto>> per un fattore di scala)*.

### LA FONTE DI `dt_e`, e il fatto che decide il passo (2)
`dt_e` nasce in **`step`** e si porta su `self._dt_e_ultimo`. L'ordine delle voci e'
`scuoti_vuoto, step, mitosi, rilassa_disegno, memoria_hebbiana_moto`:
### ⛔ **fra chi scrive `dt_e` e chi lo leggerebbe c'e' `mitosi`, CHE CREA ARCHI** -- e
`_dt_e_ultimo` e' **avvelenata** dal `COMMIT 4` *(il veleno e' `NaN`)*, dichiarata inerte
perche' *«la legge la trova GIA' RISCRITTA (`step`)»* -- ### **vero per il `step` del passo
DOPO, non per `memoria_hebbiana_moto` dello STESSO passo.**
### ➜ **Lo strumento CONTA i `NaN` e verifica l'allineamento, invece di assumerlo.**

### IL CONTROLLO CHE PUO' FALLIRE
Con `r = 1` ovunque, `dt_e = DT*0.5*(1+1)` deve dare `DT` **al bit**, quindi i due tetti
**coincidono su ogni arco**. ### ⛔ **E NON si fa spegnendo `TAU_LOC`:** li' `ritmo()` da'
`None` e `dt_e = DT` **scalare** -- coinciderebbe **senza eseguire l'aritmetica controllata**,
che e' un `FALSO-ZERO` del controllo. ### **Si fa sui VALORI VERI di `_csa` con `r` forzato a
`1`, e si DICHIARA su quanti archi** *(perche' `0` differenze su `0` archi non e'
un'identita': presidio di `FATTI_dal_codice.md`)*.

USO:
  python csv/_test_fork/_tetto_causale_tempo.py
  python csv/_test_fork/_tetto_causale_tempo.py --collaudo
  opzioni: --passi=N (default 150; il referto riporta anche il taglio a 72)

USCITA: `csv/_test_fork/_tetto_causale_tempo/_tetto_causale_tempo.json` + `_corsa.txt`.

# ESENTE-H-P3: la misura NON configura il modulo a mano -- la scena passa TUTTA dal CLI
#   (`nmasse` e `sep` da `argv`). La COPIA PATCHATA del sorgente serve a REGISTRARE ai siti
#   del tetto, che vivono DENTRO `memoria_hebbiana_moto`: il gancio di voce da' lo stato ai
#   CONFINI, e ricostruire `spinta` fuori sarebbe una SECONDA scrittura della stessa legge.
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
# ### I CONTATORI CHE SPIEGANO `r`, e non sono un extra.
#   La prova di fumo ha misurato `r = 1.0` ESATTO nei primi due passi, e con
#   `r = 1` i due tetti sono IDENTICI. Ma `r = 1` puo venire da DUE posti:
#   (a) la FISICA (nessuna dilatazione in quel passo), oppure
#   (b) un RAMO DEGENERE GIA NOTO -- `_ritmo_sicurezza` (nessuno stato
#       precedente con cui confrontarsi) o `_ritmo_snap_identico` (`Z33`: lo
#       snapshot non e avanzato, quindi `f = 0` PER COSTRUZIONE).
#   ### Nel caso (b) <<la cura non cambia nulla>> sarebbe un FALSO-ZERO prodotto
#   da un difetto noto, NON una proprieta della legge. Quindi si CONTANO.
# ### I CONTATORI DI `ritmo()` sono CORRENTI al gancio di `step` (voce 2),
#   perche `ritmo()` gira dentro `step` prima del gancio.
CONT_RITMO = ('_ritmo_chiamate', '_ritmo_sicurezza', '_ritmo_snap_identico',
              '_ritmo_guard4pi_ko', '_ritmo_med_non_promosso')
# ### QUESTI INVECE NO: li incrementa `memoria_hebbiana_moto` (voce 5), quindi al
#   gancio di `step` sarebbero cumulativi fino al passo PRECEDENTE.
#   ### MISURATO sulla prova di fumo: dopo 2 passi `_g_cct_tot` valeva 1, non 2.
#   Si leggono AL SITO, dove sono correnti.
CONT_COES = ('_g_cct_salti', '_g_cct_stringe', '_g_cct_allarga',
             '_g_cct_tot', '_g_cct_usi')
FUORI = os.path.join(RADICE, "csv", "_test_fork", "_tetto_causale_tempo")
SIM = os.path.join(RADICE, "soliton_simulator.py")
PASSI = 150
TAGLIO = 72          # il secondo orizzonte, LETTO dalla stessa corsa

P = []


def stampa(s=""):
    print(s)
    P.append(s)


def riga(c="-"):
    stampa(c * 104)


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def q3(v):
    """min / mediana / max, piu' il conteggio. ### `None` se VUOTO, e non `0`:
    ### un minimo di un insieme vuoto non e' una misura (presidio di FATTI_dal_codice)."""
    v = np.asarray(v, float)
    v = v[np.isfinite(v)]
    if not len(v):
        return {"n": 0, "min": None, "med": None, "max": None}
    return {"n": int(len(v)), "min": float(np.min(v)),
            "med": float(np.median(v)), "max": float(np.max(v))}


# =============================================================== LA PATCH
def copia_patchata():
    """Una COPIA del sorgente con i punti di REGISTRAZIONE ai siti del tetto.

    ### Ogni sostituzione si asserisce per se' e FALLISCE se l'ancora non e' unica
    ### (`P1-quater`), e non c'e' nessun escape nelle ancore (ASCII puro).
    """
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    dst = os.path.join(FUORI, "_sim_misura_tetto.py")
    t = io.open(SIM, encoding="utf-8").read()
    fatte = []

    def uno(a, b, et):
        nonlocal t
        n = t.count(a)
        if n != 1:
            raise SystemExit("[FERMO] l'ancora di `%s` compare %d volte, non 1." % (et, n))
        t = t.replace(a, b)
        fatte.append(et)

    # (0) il gancio di modulo: lo STRUMENTO lo riempie, la patch non duplica la misura
    uno("import numpy as np" + NL,
        "import numpy as np" + NL + "_MIS = None   # [MISURA TETTO] riempito dallo strumento"
        + NL, "il gancio di modulo `_MIS`")

    # (1) `r` e il contesto del passo, REGISTRATI DOVE NASCONO
    uno("        self._dt_e_ultimo = dt_e" + NL,
        "        self._dt_e_ultimo = dt_e" + NL
        + "        if _MIS is not None:" + NL
        + "            _MIS(self, 'step', r=r, dt_e=dt_e, n_al_passo=self.n," + NL
        + "                 archi_al_passo=len(self.i))" + NL,
        "`r` e `dt_e` registrati in `step`")

    # (2) il CLIP di `spinta`, PRIMA del clip
    uno("                passo_causale = c_sistema * DT" + NL
        + "                spinta = np.clip(spinta, -passo_causale, passo_causale)" + NL,
        "                passo_causale = c_sistema * DT" + NL
        + "                if _MIS is not None:" + NL
        + "                    _MIS(self, 'clip_spinta', spinta=spinta," + NL
        + "                         p_oggi=passo_causale, c=c_sistema, ii=ii, jj=jj," + NL
        + "                         mask=mask)" + NL
        + "                spinta = np.clip(spinta, -passo_causale, passo_causale)" + NL,
        "il clip di `spinta` al sito :9203")

    # (3) la SCALA della coesione, dopo `_glob`
    uno("                    _glob = LAM * np.sqrt(K_C) * DT" + NL,
        "                    _glob = LAM * np.sqrt(K_C) * DT" + NL
        + "                    if _MIS is not None:" + NL
        + "                        _MIS(self, 'coes', csa=_csa, F=_F_adim," + NL
        + "                             p_oggi=_passo_causale, glob=_glob, ii=ii, jj=jj," + NL
        + "                             mask=mask, salti=getattr(self, '_g_cct_salti', 0))"
        + NL, "la scala della coesione al sito :9340")

    io.open(dst, "w", encoding="utf-8", newline=NL).write(t)
    return dst, fatte


# =============================================================== IL RACCOGLITORE
class Raccoglitore(object):
    """Calcola il RIASSUNTO ai siti, e tiene SOLO scalari e quantili.

    ### Non accumula array per arco: `150` passi x `~470000` archi sarebbero gigabyte,
    ### e il riassunto e' cio' che il mandato chiede (min, mediana, max).
    """

    def __init__(self, S):
        self.S = S
        self.DT = float(S.DT)
        self.passo = 0
        self.ctx = {}
        self.per_passo = []
        self.contesti = []
        self.controllo = []

    # ---------------------------------------------------------- il gancio
    def __call__(self, net, sito, **kw):
        if sito == "step":
            r = kw.get("r")
            dte = kw.get("dt_e")
            self.ctx = {
                "r": None if r is None else np.asarray(r, float).copy(),
                "dt_e_scalare": bool(np.ndim(dte) == 0),
                "dt_e": (None if np.ndim(dte) == 0
                         else np.asarray(dte, float).copy()),
                "n_al_passo": int(kw.get("n_al_passo", -1)),
                "archi_al_passo": int(kw.get("archi_al_passo", -1)),
                "contatori": {c: int(getattr(net, c, 0)) for c in CONT_RITMO},
                "r_tutti_uno": (None if r is None else
                                bool(np.all(np.asarray(r, float) == 1.0))),
                "r_q3": (None if r is None else q3(r)),
            }
            self.contesti.append(dict(self.ctx, passo=self.passo))
            return
        if sito == "clip_spinta":
            self._clip(net, kw)
        elif sito == "coes":
            self._coes(net, kw)

    # ---------------------------------------------------------- dt_e allineato
    def _dte(self, net, mask):
        """`dt_e` sugli archi MASCHERATI, dalla fonte `_dt_e_ultimo`, con lo STATO
        dell'allineamento DICHIARATO invece che assunto."""
        src = getattr(net, "_dt_e_ultimo", None)
        L = int(len(np.asarray(net.i)))
        info = {"fonte": "_dt_e_ultimo",
                "scalare": bool(np.ndim(src) == 0) if src is not None else None,
                "len_src": (-1 if src is None or np.ndim(src) == 0
                            else int(len(np.asarray(src)))),
                "len_archi_ora": L,
                "archi_al_passo": self.ctx.get("archi_al_passo", -1)}
        if src is None:
            info["stato"] = "assente"
            return None, info
        if np.ndim(src) == 0:
            info["stato"] = "scalare (orologio globale): dt_e == DT"
            return np.full(int(np.sum(mask)), float(src)), info
        a = np.asarray(src, float)
        if len(a) != L:
            info["stato"] = "LUNGHEZZA DIVERSA dagli archi di ADESSO"
            return None, info
        info["stato"] = "allineato agli archi di adesso"
        v = a[mask]
        info["nan_su_mascherati"] = int(np.sum(~np.isfinite(v)))
        info["nan_totali"] = int(np.sum(~np.isfinite(a)))
        return v, info

    def _rij(self, net, ii, jj):
        """`r_i` e `r_j`, se `r` e' allineato ai nodi di ADESSO."""
        r = self.ctx.get("r")
        if r is None:
            return None, None, {"stato": "r e' None (orologio globale)"}
        n = int(net.n)
        if len(r) != n:
            return None, None, {"stato": "r NON allineato: len=%d, n=%d" % (len(r), n),
                                "len_r": int(len(r)), "n_ora": n}
        a = np.asarray(ii, int)
        b = np.asarray(jj, int)
        ok = (a < n) & (b < n)
        return r[a[ok]], r[b[ok]], {"stato": "allineato", "fuori_range": int(np.sum(~ok))}

    # ---------------------------------------------------------- :9203
    def _clip(self, net, kw):
        sp = np.abs(np.asarray(kw["spinta"], float))
        p_oggi = float(kw["p_oggi"])
        c = float(kw["c"])
        mask = np.asarray(kw["mask"])
        ii, jj = np.asarray(kw["ii"], int), np.asarray(kw["jj"], int)
        dte, info = self._dte(net, mask)
        out = {"passo": self.passo, "sito": "clip_spinta (:9203)",
               "n_archi": int(len(sp)), "p_oggi_scalare": p_oggi, "c_sistema": c,
               "mask_tutta_vera": bool(np.all(mask)),
               "archi_non_mascherati": int(np.sum(~mask)),
               "dt_e": info}
        lim_oggi = sp > p_oggi
        out["limitati_oggi"] = int(np.sum(lim_oggi))
        out["spinta"] = q3(sp)
        if dte is None:
            out["stato"] = "dt_e non utilizzabile: %s" % info.get("stato")
            self.per_passo.append(out)
            return
        rap = dte / self.DT
        p_cura = c * dte
        fin = np.isfinite(p_cura)
        lim_cura = np.zeros(len(sp), bool)
        lim_cura[fin] = sp[fin] > p_cura[fin]
        out["finiti"] = int(np.sum(fin))
        out["non_finiti"] = int(np.sum(~fin))
        out["limitati_cura"] = int(np.sum(lim_cura))
        out["da_lim_a_nonlim"] = int(np.sum(lim_oggi & ~lim_cura & fin))
        out["da_nonlim_a_lim"] = int(np.sum(~lim_oggi & lim_cura & fin))
        out["stringe_archi"] = int(np.sum((p_cura < p_oggi) & fin))
        out["allarga_archi"] = int(np.sum((p_cura > p_oggi) & fin))
        out["uguali_archi"] = int(np.sum((p_cura == p_oggi) & fin))
        out["rap_tutti"] = q3(rap)
        out["rap_sui_limitati_oggi"] = q3(rap[lim_oggi])
        ri, rj, rinfo = self._rij(net, ii, jj)
        out["r"] = rinfo
        if ri is not None:
            out["r_i_tutti"] = q3(ri)
            out["r_j_tutti"] = q3(rj)
            m = lim_oggi[:len(ri)]
            out["r_i_sui_limitati"] = q3(ri[m])
            out["r_j_sui_limitati"] = q3(rj[m])
        out["stato"] = "fatto"
        self.per_passo.append(out)
        self._controllo_allineamento(net, mask, ii, jj, "clip_spinta")

    # ---------------------------------------------------------- :9340
    def _coes(self, net, kw):
        csa = np.asarray(kw["csa"], float)
        F = np.abs(np.asarray(kw["F"], float))
        p_oggi = np.asarray(kw["p_oggi"], float)
        glob = float(kw["glob"])
        mask = np.asarray(kw["mask"])
        ii, jj = np.asarray(kw["ii"], int), np.asarray(kw["jj"], int)
        dte, info = self._dte(net, mask)
        out = {"passo": self.passo, "sito": "coes (:9340)", "n_archi": int(len(csa)),
               "glob": glob, "cs_m_per_dt": float(self.S.CS_M) * self.DT,
               "mask_tutta_vera": bool(np.all(mask)),
               "archi_non_mascherati": int(np.sum(~mask)),
               "salti_cs_m": int(kw.get("salti", 0)),
               "contatori_al_sito": {c: int(getattr(net, c, 0))
                                     for c in CONT_COES},
               "csa": q3(csa), "p_oggi": q3(p_oggi),
               "satura_F_099": int(np.sum(F > 0.99)), "F": q3(F), "dt_e": info}
        out["stringe_vs_glob"] = int(np.sum(p_oggi < glob))
        out["allarga_vs_glob"] = int(np.sum(p_oggi > glob))
        if dte is None:
            out["stato"] = "dt_e non utilizzabile: %s" % info.get("stato")
            self.per_passo.append(out)
            return
        rap = dte / self.DT
        p_cura = csa * dte
        fin = np.isfinite(p_cura)
        out["finiti"] = int(np.sum(fin))
        out["non_finiti"] = int(np.sum(~fin))
        out["p_cura"] = q3(p_cura)
        out["stringe_archi"] = int(np.sum((p_cura < p_oggi) & fin))
        out["allarga_archi"] = int(np.sum((p_cura > p_oggi) & fin))
        out["uguali_archi"] = int(np.sum((p_cura == p_oggi) & fin))
        out["rap_tutti"] = q3(rap)
        out["rap_sui_saturi"] = q3(rap[F > 0.99])
        # ### il `_glob` del confronto, se diventasse tempo proprio
        out["glob_cura"] = q3(float(self.S.LAM) * float(np.sqrt(self.S.K_C)) * dte)
        ri, rj, rinfo = self._rij(net, ii, jj)
        out["r"] = rinfo
        if ri is not None:
            out["r_i_tutti"] = q3(ri)
            out["r_j_tutti"] = q3(rj)
            out["r_i_sui_saturi"] = q3(ri[(F > 0.99)[:len(ri)]])
            out["r_j_sui_saturi"] = q3(rj[(F > 0.99)[:len(rj)]])
        out["stato"] = "fatto"
        self.per_passo.append(out)
        self._controllo_allineamento(net, mask, ii, jj, "coes")

    # ---------------------------------------------------------- il controllo
    def _controllo_allineamento(self, net, mask, ii, jj, sito):
        """### IL CONTROLLO: LA LEGGE CONTRO CIO CHE LA LEGGE HA SCRITTO.

        `(A)` con gli `r` registrati in `step` **dello stesso passo** e gli `ii`,
        `jj` di **ADESSO** al sito, si ricalcola `DT*0.5*(r[ii]+r[jj])` **solo** sugli
        archi con entrambi gli estremi `< len(r)`, e si confronta **AL BIT** con
        `_dt_e_ultimo[mask]` sugli **stessi** archi.
        ### Cosi si controllano la **FONTE**, l **ALLINEAMENTO** e la **MASCHERA** --
        e non e una copia della legge usata come misura: e un confronto fra la legge
        e **cio che la legge ha scritto**.

        `(B)` **IL CASO CHE DEVE FALLIRE, nella stessa corsa:** lo stesso confronto
        con `ii` spostato di uno *(`np.roll`)* deve dare **elementi diversi > 0**.
        ### Se da `0`, il confronto `(A)` **non discrimina**.

        `(C)` se gli archi confrontati sono **0**, quel passo ### **NON PASSA**: si
        dichiara, e **non si conta come identita**.

        ### PERCHE IL VECCHIO ERA UN FALSO-UNO *(rilievo del guardiano su `0b3af63`)*:
        ricalcolava `DT*0.5*(1+1)*c` e lo confrontava con `c*DT`, e in IEEE
        `0.5*(1+1)` e `1.0` e `DT*1.0` e `DT` -- quindi passava **sempre**, su
        qualunque dato, senza mai toccare `_dt_e_ultimo`.
        """
        out = {"passo": self.passo, "sito": sito}
        r = self.ctx.get("r")
        src = getattr(net, "_dt_e_ultimo", None)
        L = int(len(np.asarray(net.i)))
        if r is None:
            out["archi_confrontati"] = 0
            out["stato"] = "r e None (orologio globale): dt_e e DT scalare"
            self.controllo.append(out)
            return
        if src is None or np.ndim(src) == 0:
            out["archi_confrontati"] = 0
            out["stato"] = "la fonte _dt_e_ultimo e assente o SCALARE"
            self.controllo.append(out)
            return
        a = np.asarray(src, float)
        if len(a) != L:
            out["archi_confrontati"] = 0
            out["stato"] = ("la fonte NON e lunga come gli archi di adesso: %d vs %d"
                            % (len(a), L))
            self.controllo.append(out)
            return
        dte = a[mask]
        rr = np.asarray(r, float)
        nr = int(len(rr))
        I = np.asarray(ii, int)
        J = np.asarray(jj, int)
        in_range = (I < nr) & (J < nr)
        finito = np.isfinite(dte)
        ok = in_range & finito
        out.update({"archi_mascherati": int(len(dte)), "len_r": nr,
                    "n_ora": int(net.n),
                    "esclusi_estremo_oltre_r": int(np.sum(~in_range)),
                    "esclusi_dt_e_non_finito": int(np.sum(in_range & ~finito)),
                    "archi_confrontati": int(np.sum(ok))})
        if not np.any(ok):
            out["stato"] = "ZERO archi confrontabili: questo passo NON PASSA"
            self.controllo.append(out)
            return
        atteso = self.DT * 0.5 * (rr[I[ok]] + rr[J[ok]])
        scritto = dte[ok]
        diversi = int(np.sum(atteso != scritto))
        out["elementi_diversi"] = diversi
        out["scarto_max"] = float(np.max(np.abs(atteso - scritto)))
        # ### (B) IL CASO CHE DEVE FALLIRE, nella STESSA corsa e sugli STESSI dati.
        Ir = np.roll(I, 1)
        okr = (Ir < nr) & (J < nr) & finito
        if np.any(okr):
            att_r = self.DT * 0.5 * (rr[Ir[okr]] + rr[J[okr]])
            out["spostato_diversi"] = int(np.sum(att_r != dte[okr]))
            out["spostato_archi"] = int(np.sum(okr))
        else:
            out["spostato_diversi"] = -1
            out["spostato_archi"] = 0
        # ### `r` ERA DEGENERE A QUESTO PASSO? La domanda decide se (A) e (B)
        #   abbiano POTERE. Con `r == 1` ovunque, `dt_e` e un array COSTANTE pari
        #   a `DT`: nessuna permutazione degli indici e rilevabile, quindi ne (A)
        #   ne (B) provano niente. ### Si DICHIARA, non si spaccia per identita.
        out["r_degenere"] = bool(np.all(rr == 1.0))
        out["dt_e_costante"] = bool(np.all(scritto == scritto[0]))
        out["potere"] = not (out["r_degenere"] or out["dt_e_costante"])
        out["stato"] = ("coincide al bit" if diversi == 0
                        else "### NON COINCIDE")
        if not out["potere"]:
            out["stato"] += " (ma INVERIFICABILE: dt_e e costante)"
        self.controllo.append(out)

# =============================================================== il collaudo
def collaudo():
    riga("=")
    stampa("COLLAUDO -- i casi che decidono se la misura e' leggibile")
    riga("=")
    ok = True

    DT = 0.01
    # (1) ### ARITMETICA IEEE, NON UN CONTROLLO DELLO STRUMENTO.
    #   Questa riga NON prova niente sullo strumento: `0.5*(1+1)` e `1.0` e `DT*1.0`
    #   e `DT` **per definizione di IEEE-754**, quindi passa su qualunque dato.
    #   ### ERA IL VECCHIO CONTROLLO, ed era un FALSO-UNO (rilievo del guardiano su
    #   `0b3af63`): resta qui SOLO come promemoria di che cosa non e un controllo.
    stampa("  (1) aritmetica IEEE, NON un controllo dello strumento:")
    for et, c in [("c scalare", 1.1313708498984762),
                  ("c per arco", np.array([0.566, 1.1313708498984762, 2.0]))]:
        uno_ = np.ones(3)
        dte = DT * 0.5 * (uno_ + uno_)
        a = np.asarray(c, float) * dte
        b = np.broadcast_to(np.asarray(c, float) * DT, a.shape)
        stampa("      %-12s dt_e==DT %-5s tetti identici %-5s  <- vero PER"
               % (et, bool(np.all(dte == DT)), int(np.sum(a != b)) == 0))
        stampa("                   DEFINIZIONE, non perche lo strumento funzioni")

    # (2) ### IL CONTROLLO VERO, su dati sintetici: la legge contro CIO CHE E SCRITTO.
    #   `scritto` imita `_dt_e_ultimo`; se coincide con il ricalcolo, (A) passa.
    rr = np.array([0.5, 1.0, 1.4, 0.8])
    I = np.array([0, 1, 2, 3])
    J = np.array([1, 2, 3, 0])
    scritto = DT * 0.5 * (rr[I] + rr[J])
    att = DT * 0.5 * (rr[I] + rr[J])
    d0 = int(np.sum(att != scritto))
    buono = d0 == 0
    ok = ok and buono
    stampa("  (2) (A) allineato: %d elementi diversi su 4 (atteso 0)   %s"
           % (d0, "OK" if buono else "FALLITO"))

    # (3) ### IL CASO CHE DEVE FALLIRE: con `ii` spostato di uno, (A) DEVE trovare
    #   differenze. Se non le trovasse, (A) non discriminerebbe -- cioe sarebbe
    #   un altro FALSO-UNO, e non lo saprei.
    Ir = np.roll(I, 1)
    att_r = DT * 0.5 * (rr[Ir] + rr[J])
    dr = int(np.sum(att_r != scritto))
    buono = dr > 0
    ok = ok and buono
    stampa("  (3) (B) con ii spostato: %d elementi diversi su 4 (attesi > 0)   %s"
           % (dr, "OK" if buono else "FALLITO -- (A) NON DISCRIMINA"))

    # (4) ### UNA FONTE SBAGLIATA DEVE ESSERE SCOPERTA: se `scritto` venisse da un
    #   `r` diverso (per esempio quello del passo precedente), (A) deve vederlo.
    scritto_vecchio = DT * 0.5 * (np.array([0.6, 1.0, 1.4, 0.8])[I]
                                  + np.array([0.6, 1.0, 1.4, 0.8])[J])
    dv = int(np.sum(att != scritto_vecchio))
    buono = dv > 0
    ok = ok and buono
    stampa("  (4) fonte di un ALTRO passo: %d elementi diversi (attesi > 0)   %s"
           % (dv, "OK" if buono else "FALLITO"))

    # (5) ### ZERO ARCHI NON E UN IDENTITA: lo stato deve dirlo.
    vuoto = int(np.sum(np.array([], float) != np.array([], float)))
    buono = vuoto == 0
    ok = ok and buono
    stampa("  (5) su 0 archi il confronto da %d differenze -- ed e proprio per questo"
           % vuoto)
    stampa("      che lo stato <<ZERO archi confrontabili>> NON conta come identita")

    # (3) ### `q3` di un insieme VUOTO non deve dare 0 (presidio di FATTI_dal_codice)
    v = q3([])
    buono = v["min"] is None and v["n"] == 0
    ok = ok and buono
    stampa("  q3 di un insieme VUOTO -> min=%r n=%d (atteso None, 0)   %s"
           % (v["min"], v["n"], "OK" if buono else "FALLITO"))

    # (4) ### `q3` scarta i NON FINITI invece di propagarli
    v = q3([1.0, np.nan, 3.0, np.inf])
    buono = v["n"] == 2 and v["max"] == 3.0
    ok = ok and buono
    stampa("  q3 con nan e inf -> n=%d max=%r (attesi 2, 3.0)   %s"
           % (v["n"], v["max"], "OK" if buono else "FALLITO"))

    # (5) la patch attacca, e tutte le ancore sono UNICHE
    try:
        dst, fatte = copia_patchata()
        stampa("  la patch attacca: %d ancore, tutte uniche   OK" % len(fatte))
        for f in fatte:
            stampa("      %s" % f)
        stampa("  copia: %s  blob %s" % (os.path.basename(dst), blob(dst)[:8]))
    except SystemExit as e:
        ok = False
        stampa("  la patch NON attacca: %s   FALLITO" % (e,))

    # (6) ### il gancio della copia e' DAVVERO chiamato: altrimenti la misura sarebbe
    #     un referto di zeri, e uno zero da <<mai chiamato>> si legge come <<niente>>.
    stampa("  (il caso <<il gancio e' chiamato>> si prova nel run, e il referto riporta")
    stampa("   il numero di chiamate per sito: se fosse 0, NON e' un risultato)")
    stampa()
    stampa("  ### %s" % ("tutti i casi passano." if ok else "*** COLLAUDO FALLITO ***"))
    riga("=")
    return 0 if ok else 1


# =============================================================== il corpo
def piattaforma():
    return {"python": sys.version.split()[0], "numpy": np.__version__,
            "sistema": platform.system() + " " + platform.release(),
            "macchina": platform.machine()}


def aggrega(righe, sito, fino):
    """Il riassunto su tutti i passi <= `fino`, per un sito."""
    r = [x for x in righe if x["sito"].startswith(sito) and x["passo"] <= fino
         and x.get("stato") == "fatto"]
    if not r:
        return {"passi": 0}
    def s(k):
        return [x[k] for x in r if k in x]
    def tot(k):
        v = [x for x in s(k) if isinstance(x, (int, float))
             and not isinstance(x, bool)]
        return int(sum(v)) if v else 0
    out = {"passi": len(r), "archi_tot": tot("n_archi")}
    for k in ["limitati_oggi", "limitati_cura", "da_lim_a_nonlim", "da_nonlim_a_lim",
              "stringe_archi", "allarga_archi", "uguali_archi", "satura_F_099",
              "non_finiti", "stringe_vs_glob", "allarga_vs_glob"]:
        if s(k):
            out[k] = tot(k)
    for k in ["rap_tutti", "rap_sui_limitati_oggi", "rap_sui_saturi", "r_i_tutti",
              "r_j_tutti", "r_i_sui_limitati", "r_j_sui_limitati", "r_i_sui_saturi",
              "r_j_sui_saturi", "csa", "p_oggi", "p_cura", "glob_cura", "spinta"]:
        # ### SI CONTROLLA IL TIPO, non il nome: una chiave puo' portare uno
        #   SCALARE in un sito e un dizionario di quantili in un altro, e
        #   quella collisione ha fatto cadere la prova di fumo DOPO che la
        #   misura era gia' fatta -- il modo peggiore di cadere.
        v = [x[k] for x in r
             if k in x and isinstance(x[k], dict)
             and x[k].get("min") is not None]
        if v:
            out[k] = {"min": min(y["min"] for y in v),
                      "med_delle_mediane": float(np.median([y["med"] for y in v])),
                      "max": max(y["max"] for y in v),
                      "passi_con_dato": len(v)}
    nan = [x["dt_e"].get("nan_su_mascherati", 0) for x in r if "dt_e" in x]
    out["nan_in_dt_e_tot"] = int(sum(nan))
    out["passi_con_nan"] = int(sum(1 for x in nan if x))
    out["mask_sempre_vera"] = all(x.get("mask_tutta_vera", True) for x in r)
    sal = s("salti_cs_m")
    if sal:
        out["salti_cs_m_finale"] = int(max(sal))
    return out


def principale(passi):
    riga("=")
    stampa("IL TETTO CAUSALE: tempo COORDINATO (DT) contro tempo PROPRIO (dt_e)")
    riga("=")
    stampa()
    stampa("### E' UNA MISURA, NON UNA CURA: nessun PASSA/FALLISCE oltre al controllo.")
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
        S, a = _cli_flag.carica_dal_cli(list(argv), nome="sim_tetto", sim=dst)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    net = S.net
    R = Raccoglitore(S)
    S._MIS = R

    riga()
    stampa("LA CONFIGURAZIONE CHE DECIDE LA MISURA, letta dal CLI (mai a mano)")
    riga()
    cfg = {}
    for k in ["TAU_LOC", "TEMPO_SEGNO", "COES_CAUSALE", "COES_ADIM", "VIRIALE",
              "GRAV_BIFASE", "CS_DINAMICO", "CS_M", "LAM", "K_C", "DT", "MEM_HEBB"]:
        cfg[k] = getattr(S, k, None)
        stampa("  %-14s %r" % (k, cfg[k]))
    stampa("  scena: nmasse=%s sep=%s  ->  n = %d, archi = %d"
           % (getattr(a, "nmasse", "?"), getattr(a, "sep", "?"), net.n, len(net.i)))
    stampa("  c_sistema*DT = %.10f     CS_M*DT = %.10f"
           % (float(S.LAM) * float(np.sqrt(S.K_C)) * float(S.DT),
              float(S.CS_M) * float(S.DT)))
    if float(cfg["TAU_LOC"]) == 0.0:
        stampa("  ### FERMO: TAU_LOC = 0 -> ritmo() da' None -> dt_e = DT ESATTAMENTE.")
        stampa("      La cura non cambierebbe un bit e la misura non ha oggetto.")
        return 1
    stampa()

    riga("=")
    stampa("IL RUN: %d passi (il referto riporta anche il taglio a %d)" % (passi, TAGLIO))
    riga("=")
    for k in range(1, passi + 1):
        R.passo = k
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(S, net)
    stampa("  passi girati: %d    n finale = %d, archi = %d" % (passi, net.n, len(net.i)))
    chiam = {}
    for x in R.per_passo:
        chiam[x["sito"]] = chiam.get(x["sito"], 0) + 1
    stampa("  chiamate del gancio per sito: %s" % (chiam or "NESSUNA"))
    if not chiam:
        stampa("  ### ATTENZIONE: il gancio NON e' stato chiamato. Un referto di zeri")
        stampa("      qui NON significa <<il tetto non limita>>: significa che la misura")
        stampa("      non e' avvenuta. LO DICO invece di riportare zeri.")
    stampa()

    fuori = {"piattaforma": pf, "blob_sim": blob(SIM), "blob_copia": blob(dst),
             "timbro_strumento": _presidio.timbro(__file__),
             "configurazione": {k: (float(v) if isinstance(v, (int, float))
                                    and not isinstance(v, bool) else v)
                                for k, v in cfg.items()},
             "scena": {"nmasse": getattr(a, "nmasse", None),
                       "sep": getattr(a, "sep", None),
                       "n_iniziale": int(net.n), "passi": passi},
             "ancore_patch": fatte, "chiamate_per_sito": chiam,
             "per_passo": R.per_passo, "contesti": R.contesti,
             "controllo": R.controllo}

    riga("=")
    stampa("DA DOVE VIENE `r`: la FISICA o un RAMO DEGENERE GIA NOTO?")
    riga("=")
    uno_sempre = [c for c in R.contesti if c.get("r_tutti_uno")]
    stampa("  passi con r == 1.0 ESATTO su OGNI nodo: %d su %d"
           % (len(uno_sempre), len(R.contesti)))
    stampa("  ### E CONTA: con r = 1 i due tetti sono IDENTICI, quindi un esito")
    stampa("      <<la cura non cambia nulla>> NON sarebbe una proprieta della")
    stampa("      legge, ma la conseguenza di un r degenere. Per questo si contano")
    stampa("      i rami che producono r = 1 senza che sia fisica.")
    if R.contesti:
        ult = R.contesti[-1]["contatori"]
        for c in CONT_RITMO:
            stampa("      %-26s %12d  (cumulativo a fine corsa)" % (c, ult[c]))
        rq = [c["r_q3"] for c in R.contesti if c.get("r_q3")]
        if rq:
            stampa("  r sui nodi: min dei min %.6e, max dei max %.6e"
                   % (min(x["min"] for x in rq), max(x["max"] for x in rq)))
            div = [i + 1 for i, c in enumerate(R.contesti)
                   if c.get("r_q3") and (c["r_q3"]["min"] != 1.0
                                         or c["r_q3"]["max"] != 1.0)]
            stampa("  primi passi in cui r NON e 1 ovunque: %s"
                   % (div[:10] if div else "NESSUNO"))
    stampa()
    for sito, et in [("clip_spinta", "IL CLIP DI `spinta` -- cono GLOBALE (:9203)"),
                     ("coes", "LA SCALA DELLA COESIONE -- cono LOCALE (:9340)")]:
        riga("=")
        stampa(et)
        riga("=")
        for fino, nome in [(TAGLIO, "72 passi"), (passi, "%d passi" % passi)]:
            A = aggrega(R.per_passo, sito, fino)
            fuori.setdefault("aggregati", {})["%s@%d" % (sito, fino)] = A
            stampa("  --- %s ---" % nome)
            if not A.get("passi"):
                stampa("      nessun passo con dato utilizzabile")
                continue
            stampa("      passi con dato %d, archi-passo totali %d"
                   % (A["passi"], A["archi_tot"]))
            for k in ["limitati_oggi", "limitati_cura", "da_lim_a_nonlim",
                      "da_nonlim_a_lim", "stringe_archi", "allarga_archi",
                      "uguali_archi", "satura_F_099", "stringe_vs_glob",
                      "allarga_vs_glob", "non_finiti"]:
                if k in A:
                    stampa("      %-22s %12d" % (k, A[k]))
            for k in ["rap_tutti", "rap_sui_limitati_oggi", "rap_sui_saturi",
                      "r_i_tutti", "r_j_tutti", "r_i_sui_limitati", "r_i_sui_saturi",
                      "csa", "p_oggi", "p_cura", "glob_cura", "spinta"]:
                if k in A:
                    v = A[k]
                    stampa("      %-22s min %12.6e  med %12.6e  max %12.6e"
                           % (k, v["min"], v["med_delle_mediane"], v["max"]))
            stampa("      nan in dt_e: %d su %d passi   mask sempre vera: %s"
                   % (A["nan_in_dt_e_tot"], A["passi_con_nan"], A["mask_sempre_vera"]))
            if "salti_cs_m_finale" in A:
                stampa("      ripieghi CS_M (cumulativo): %d" % A["salti_cs_m_finale"])
        stampa()

    riga("=")
    stampa("IL CONTROLLO: la LEGGE contro CIO CHE LA LEGGE HA SCRITTO")
    riga("=")
    stampa("  (A) DT*0.5*(r[ii]+r[jj]), con gli r di `step` DELLO STESSO PASSO e gli")
    stampa("      ii/jj di ADESSO al sito, confrontato AL BIT con _dt_e_ultimo[mask]")
    stampa("      sugli STESSI archi. Controlla FONTE, ALLINEAMENTO e MASCHERA.")
    stampa("  (B) lo stesso confronto con ii SPOSTATO DI UNO deve dare differenze.")
    stampa("  (C) zero archi confrontabili = il passo NON PASSA.")
    stampa("  ### E IL VECCHIO CONTROLLO ERA UN FALSO-UNO (guardiano, su 0b3af63):")
    stampa("      ricalcolava DT*0.5*(1+1)*c contro c*DT, che in IEEE coincidono")
    stampa("      SEMPRE, senza mai toccare _dt_e_ultimo.")
    stampa()
    tot = len(R.controllo)
    archi = int(sum(x.get("archi_confrontati", 0) for x in R.controllo))
    vuoti = [x for x in R.controllo if x.get("archi_confrontati", 0) == 0]
    diff = [x for x in R.controllo if x.get("elementi_diversi", 0)]
    # ### DUE INSIEMI DIVERSI, e tenerli insieme sarebbe l'errore:
    #   `senza_potere` = (B) non discrimina perche `dt_e` e COSTANTE (r degenere):
    #       nessun test di permutazione potrebbe, e il passo e INVERIFICABILE;
    #   `nondisc` = (B) non discrimina MENTRE `dt_e` VARIA: li (A) non prova niente,
    #       ed e un FERMO vero.
    con_potere = [x for x in R.controllo if x.get("potere")]
    senza_potere = [x for x in R.controllo
                    if x.get("archi_confrontati", 0) and not x.get("potere", False)]
    nondisc = [x for x in con_potere if x.get("spostato_diversi", 0) <= 0]
    escl_r = int(sum(x.get("esclusi_estremo_oltre_r", 0) for x in R.controllo))
    escl_n = int(sum(x.get("esclusi_dt_e_non_finito", 0) for x in R.controllo))
    masch = int(sum(x.get("archi_mascherati", 0) for x in R.controllo))
    stampa("  verifiche %d   archi mascherati %d   CONFRONTATI %d"
           % (tot, masch, archi))
    stampa("  esclusi perche un estremo e oltre len(r) (nodo nato in mitosi): %d"
           % escl_r)
    stampa("  esclusi perche dt_e NON e finito (il veleno del COMMIT 4):          %d"
           % escl_n)
    stampa("  verifiche con ZERO archi confrontabili (NON passano):               %d"
           % len(vuoti))
    stampa("  verifiche con DIFFERENZE in (A):                                   %d"
           % len(diff))
    stampa("  verifiche con POTERE (dt_e VARIA fra gli archi):                   %d"
           % len(con_potere))
    stampa("  verifiche INVERIFICABILI (dt_e COSTANTE: r degenere):              %d"
           % len(senza_potere))
    stampa("      ### su queste nessun test di permutazione puo discriminare, e NON")
    stampa("          le conto come identita: lo dico. E il guardiano lo aveva")
    stampa("          scritto nel mandato.")
    stampa("  verifiche CON POTERE in cui (B) NON ha discriminato:                %d"
           % len(nondisc))
    fuori["controllo_riassunto"] = {
        "verifiche": tot, "archi_mascherati": masch, "archi_confrontati": archi,
        "esclusi_estremo_oltre_r": escl_r, "esclusi_dt_e_non_finito": escl_n,
        "vuote": len(vuoti), "con_differenze": len(diff),
        "con_potere": len(con_potere), "inverificabili": len(senza_potere),
        "senza_discriminazione": len(nondisc)}
    if archi == 0:
        stampa("  ### FERMO: ZERO archi confrontati in tutta la corsa. Il controllo")
        stampa("      non ha avuto oggetto, e NON si legge come identita.")
        esito = 1
    elif diff:
        stampa("  ### FERMO: (A) trova DIFFERENZE. Su quei passi la misura e INVALIDA.")
        stampa("      passi con differenze: %s"
               % sorted({x["passo"] for x in diff})[:20])
        for x in diff[:5]:
            stampa("      passo %s sito %s: %d diversi su %d, scarto max %.3e"
                   % (x["passo"], x["sito"], x["elementi_diversi"],
                      x["archi_confrontati"], x["scarto_max"]))
        esito = 1
    elif nondisc:
        stampa("  ### FERMO: (B) non discrimina in %d verifiche IN CUI dt_e VARIA."
               % len(nondisc))
        stampa("      Li il confronto (A) non proverebbe niente: un altro FALSO-UNO.")
        esito = 1
    elif not con_potere:
        stampa("  ### FERMO, e NON perche lo strumento sbagli: in TUTTE le %d verifiche"
               % tot)
        stampa("      dt_e e COSTANTE (r == 1 su ogni nodo), quindi l allineamento NON")
        stampa("      E VERIFICABILE -- nessuna permutazione degli indici e rilevabile.")
        stampa("      ### E DALLO STESSO FATTO SEGUE LA MISURA: con dt_e == DT i due")
        stampa("          tetti COINCIDONO, quindi <<la cura non cambia nulla>> su")
        stampa("          questa traiettoria -- ma per r DEGENERE, non per la legge.")
        stampa("      ### Questo E un risultato, e va letto con i contatori di ritmo().")
        esito = 1
    elif vuoti:
        stampa("  ### ATTENZIONE: %d verifiche con ZERO archi confrontabili." % len(vuoti))
        stampa("      Quei passi NON passano, e li dichiaro invece di contarli come")
        stampa("      identita. Le altre %d passano." % (tot - len(vuoti)))
        esito = 0
    else:
        stampa("  ### IL CONTROLLO PASSA su tutte le %d verifiche: %d archi confrontati,"
               % (tot, archi))
        stampa("      ZERO differenze, e (B) ha discriminato ovunque.")
        esito = 0
    riga("=")

    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    json.dump(fuori, io.open(os.path.join(FUORI, "_tetto_causale_tempo.json"), "w",
                             encoding="utf-8"),
              indent=1, ensure_ascii=False, sort_keys=True, default=str)
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8").write(NL.join(P))
    print("scritto: %s" % os.path.join(FUORI, "_tetto_causale_tempo.json"))
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
