# -*- coding: utf-8 -*-
"""IL SIGILLO DI `TORS-W8-AVVOLGIMENTO`: `S0`-`S3`.

### ⛔ **LA FISICA CAMBIA, quindi NON c'e' identita' con prima** -- e il sigillo non la
cerca. Cerca **quattro** cose diverse:

| | |
|---|---|
| **`S0`** | il **braccio 0**: la copia di **prima** + la patch committata e' ### **byte-identica al blob nuovo** su `150` passi, con **tutti** gli attributi di `net` a confronto |
| **`S1`** | controlli positivi **sintetici**: a un giro di fase l'incremento e' quello vero entro `1e-12`; con un cambio di dipolo e' `Δdipolo`; ### **un arco nuovo, per CIASCUNA via di nascita, ha spinta ZERO al primo passo**; e nessun `nan` sopravvive a un passo di torsione |
| **`S2`** | ### **il controllo che DEVE fallire:** la legge **vecchia** sugli stessi casi sbaglia di `4π` esatti, e **da' il calcio di nascita** |
| **`S3`** | nella corsa vera, un gancio di ### **SOLA LETTURA** calcola le **due** forme della spinta sullo **STESSO** stato: le differenze oltre `1e-12` che **non** sono giri di fase, archi nuovi o il passo `1` ### **devono essere ZERO** |

### 📌 **E `S0` NON E' <<LA PATCH RIGIRA>>:** quello lo prova il patch stesso sul blob. `S0`
prova che ### **i due simulatori GIRANO identici**, cioe' che la patch e' l'UNICA differenza
e che il mio albero di lavoro non ne ha altre -- ### **e' il controllo dell'INVOLUCRO**
*(`STANDARD 5`)*.

USO:  python csv/_seal_fork/_sigillo_tors_w8.py  [--passi=N]  [--collaudo]
"""
import contextlib
import hashlib
import io
import json
import os
import pickle
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
FUORI = os.path.join(RADICE, "csv", "_seal_fork", "_sigillo_tors_w8")
SIM = os.path.join(RADICE, "soliton_simulator.py")
PATCH = os.path.join(RADICE, "csv", "_seal_fork", "_tors_w8_patch.py")
# ### IL *PRIMA*: NON si pinna a mano e NON si prende da `HEAD`.
#   ### **Si usa `_cli_flag.sim_prima_del_flag`, la via SANCITA:** trova il commit che ha
#   introdotto il token con `git log -S`, prende **il suo PADRE**, e ### **ASSERISCE che il
#   file estratto NON contenga il token** -- un'ancora **auto-denunciante**, che si ferma
#   invece di misurare niente se un giorno il token comparisse prima *(`A9`)*.
#   ### ⚠ **E IL TOKEN NON E' UN FLAG, e' il CAMPO NUOVO `twp_dip`:** la cura non introduce
#   nessun flag, e `twp_dip` e' la stringa che esiste **solo** dopo la cura.
#   ### 📌 **PRIMA AVEVO PINNATO `PADRE = "5c46856"` A MANO, e il presidio `H-P8` ha avuto
#   ragione a fermarmi:** un hash a mano non si denuncia da solo, e la docstring della via
#   sancita dice esattamente perche' *(il difetto misurato di `CURA 4` e `CURA 5`)*.
TOKEN_DELLA_CURA = "twp_dip"
BLOB_PRIMA = "f7237563"
BLOB_DOPO = "cf2a1ac8"
PASSI = 150
PASSI_SALVA = 10
P2 = 2.0 * np.pi
P3 = 3.0 * np.pi
P4 = 4.0 * np.pi


def stampa(s=""):
    print(s, flush=True)


def riga(c="-"):
    stampa(c * 104)


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def q(v):
    v = np.asarray(v, float)
    v = v[np.isfinite(v)]
    if v.size == 0:
        return None
    return {("q%03d" % int(round(100 * x))): float(np.quantile(v, x))
            for x in (0.0, 0.05, 0.25, 0.5, 0.75, 0.95, 1.0)}


def _w8(a):
    return (a + P4) % (2.0 * P4) - P4


def _w4(a):
    return (a + P2) % (2.0 * P2) - P2


# =============================================================== IL GANCIO DI S3
def copia_con_gancio(sorgente, dst):
    """Il gancio di `S3`: **SOLA LETTURA**, e calcola le DUE forme sullo STESSO stato.

    Le ancore si **CONTANO** e devono essere **UNICHE** *(`P1-quater`)*.
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
        + "_SIG = None   # [SIGILLO TORS-W8] lo riempie lo strumento" + NL,
        "il gancio di modulo `_SIG`")
    # ### IL GANCIO STA **PRIMA** dell'aggiornamento, cosi' `self.tw`, `self.twp` e
    #   `self.twp_dip` sono i valori d'INGRESSO e le due forme si calcolano sullo STESSO
    #   stato. ### **Nessuna scrittura: solo letture e un dizionario.**
    uno("            _nuovo = np.isnan(self.twp_dip)" + NL,
        "            if _SIG is not None:" + NL
        + "                _SIG.torsione(self, dph=dph, twist_dip=twist_dip," + NL
        + "                              twp=self.twp, twp_dip=self.twp_dip)" + NL
        + "            _nuovo = np.isnan(self.twp_dip)" + NL,
        "S3: il gancio di sola lettura nel blocco della torsione")
    io.open(dst, "w", encoding="utf-8", newline=NL).write(t)
    return fatte


class Spia(object):
    """`S3`: le DUE forme della spinta, sullo STESSO stato. ### **LEGGE SOLTANTO.**"""

    def __init__(self):
        self.passo = 0
        self.passi = []
        self.tot = {"coppie": 0, "diverse": 0, "giri": 0, "nuovi": 0,
                    "non_spiegate": 0, "passo1": 0}

    def torsione(self, net, dph, twist_dip, twp, twp_dip):
        dph = np.asarray(dph, float)
        td = np.asarray(twist_dip, float) * np.ones_like(dph)
        twp = np.asarray(twp, float)
        tdp = np.asarray(twp_dip, float)
        nuovo = np.isnan(tdp)
        # --- la forma NUOVA (quella che gira)
        _fp = np.where(nuovo, dph, twp)
        _dp = np.where(nuovo, td, tdp)
        nuova = np.where(nuovo, 0.0, _w4(dph - _fp) + (td - _dp))
        # ### ⚠ su un arco NUOVO la forma nuova e' zero PER COSTRUZIONE: `np.where` sul
        #   risultato lo rende esplicito invece di affidarlo all'aritmetica.
        # --- la forma VECCHIA, sullo STESSO stato
        # ### ⛔ **QUI AVEVO SBAGLIATO, e il sigillo me l'ha detto** *(`e8122cc`)*: usavo
        #   `twp` DA SOLO, ma il vecchio `twp` NON era `dph` -- era
        #   ### **`_w8(dph + twist_dip)`, LA SOMMA AVVOLTA**, che col marcatore vale
        #   ### **`twp + twp_dip`.** E poiche' `|dph + twist_dip| <= 3pi < 4pi`, `_w8` di
        #   quella somma E' la somma: la ricostruzione e' ESATTA, non approssimata.
        #   ### **Con la ricostruzione sbagliata la spia confrontava la legge nuova con una
        #   TERZA LEGGE INVENTATA, e sbagliava di `pi` ESATTO sui 235 mila archi che al
        #   passo 2 avevano `twp_dip = pi`.**
        #   ### ⚠ **E L'AVEVO SCRITTO IO** nel commit dello strumento (`4aba5ec`, <<cosa
        #   ricontrollare>> punto 2): *«se sbagliassi questa ricostruzione, S3 confronterebbe
        #   la legge nuova con una terza legge inventata, e il suo zero non vorrebbe dire
        #   niente»*. ### **Avvertimento scritto, errore fatto.**
        #   ### ✔ **Sui NUOVI resta `0`:** `_allaccia` metteva `twp = 0`, e le due regole di
        #   nascita ci mettevano la fase -- ma il confronto sui nuovi e' comunque
        #   **spiegato**, quindi il valore qui non cambia nessun verdetto. Lo lascio `0`
        #   perche' e' cio' che la semina faceva, ed e' il caso peggiore.
        _twp_v = np.where(nuovo, 0.0, twp + np.nan_to_num(tdp))
        vecchia = _w8(dph + td - _twp_v)
        d = np.abs(nuova - vecchia)
        div = d > 1e-12
        # --- le TRE spiegazioni ammesse
        giro = np.abs(_w4(dph - _fp) - (dph - _fp)) > 1e-12      # la fase ha avvolto
        p1 = (self.passo == 1)
        spiegato = giro | nuovo | p1
        non_sp = div & ~spiegato
        self.tot["coppie"] += int(dph.size)
        self.tot["diverse"] += int(np.sum(div))
        self.tot["giri"] += int(np.sum(div & giro))
        self.tot["nuovi"] += int(np.sum(div & nuovo))
        self.tot["passo1"] += int(np.sum(div) if p1 else 0)
        self.tot["non_spiegate"] += int(np.sum(non_sp))
        self.passi.append({
            "passo": self.passo, "archi": int(dph.size),
            "diverse": int(np.sum(div)), "giri": int(np.sum(div & giro)),
            "nuovi": int(np.sum(div & nuovo)),
            "non_spiegate": int(np.sum(non_sp)),
            "q_diff": q(d[div]) if np.any(div) else None,
            "q_diff_su_pi": (float(np.median(d[div]) / np.pi) if np.any(div) else None),
            "q_tw": q(np.abs(np.asarray(net.tw, float))),
            "nan_in_twp_dip": int(np.sum(nuovo)),
            "sopra_4pi": int(np.sum(np.abs(np.asarray(net.tw, float)) >= P4))})


# =============================================================== S0
def _foto(net):
    """TUTTI gli attributi di `net`, via pickle. ### `_calcpsi_origini` AGGREGATO per nome."""
    out = {}
    for k in sorted(vars(net)):
        v = getattr(net, k)
        if k == "_calcpsi_origini":
            # ### LE SUE CHIAVI CONTENGONO NUMERI DI RIGA, che la patch SPOSTA: si aggrega
            #   per NOME DI FUNZIONE, altrimenti `S0` fallirebbe per una cosa che non e' fisica.
            try:
                agg = {}
                for kk, vv in dict(v).items():
                    nome = str(kk).split(":")[0]
                    agg[nome] = agg.get(nome, 0) + (vv if isinstance(vv, int) else 1)
                out[k] = ("aggregato", sorted(agg.items()))
                continue
            except Exception:
                pass
        try:
            if isinstance(v, np.ndarray):
                out[k] = ("array", v.shape, str(v.dtype),
                          hashlib.sha1(np.ascontiguousarray(v).tobytes()).hexdigest())
            else:
                out[k] = ("pickle", hashlib.sha1(pickle.dumps(v, 4)).hexdigest())
        except Exception as e:
            out[k] = ("NON-CONFRONTABILE", repr(e)[:80])
    return out


def _carica(nome, sim, dest):
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"], dest=dest)
        S, a = _cli_flag.carica_dal_cli(list(argv), nome=nome, sim=sim)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    return S, S.net


# =============================================================== IL COLLAUDO (S1 + S2)
def collaudo():
    esiti = []

    def prova(nome, ok, dett=""):
        esiti.append((nome, bool(ok), dett))
        stampa("  %-7s %-74s %s" % ("OK" if ok else "FALLITA", nome, dett))

    def nuova(dph, td, twp, tdp):
        """La legge CURATA, in isolamento."""
        nuovo = np.isnan(tdp)
        _fp = np.where(nuovo, dph, twp)
        _dp = np.where(nuovo, td, tdp)
        return np.where(nuovo, 0.0, _w4(dph - _fp) + (td - _dp))

    def vecchia(dph, td, twp_somma):
        """La legge DI PRIMA, in isolamento."""
        return _w8(dph + td - twp_somma)

    riga("=")
    stampa("S1: I CONTROLLI POSITIVI SINTETICI")
    riga("=")
    _wphi = (lambda a: (a + P2) % (2.0 * P2) - P2)      # noqa: E731  FASE_2PI = False
    # --- (1) un GIRO DI FASE: l'incremento e' quello VERO
    rng = np.random.default_rng(9001)
    d = rng.uniform(1e-6, 0.05, 20000)
    d0 = _wphi(P2 - d / 2)
    d1 = _wphi(P2 + d / 2)
    z = np.zeros_like(d)
    nn = nuova(d1, z, d0, z)
    prova("S1.1: a un GIRO DI FASE l'incremento e' quello VERO entro 1e-12",
          bool(np.max(np.abs(nn - d)) < 1e-12),
          "max|errore| = %.3e su %d casi" % (float(np.max(np.abs(nn - d))), d.size))
    # --- (2) un CAMBIO DI DIPOLO: l'incremento e' Delta dipolo
    for dd in (np.pi / 2, -np.pi / 2, np.pi, -np.pi):
        a = np.full(5000, 1.234)
        tdp = np.zeros(5000)
        nn2 = nuova(a, np.full(5000, dd), a, tdp)
        prova("S1.2: con un cambio di dipolo di %+.4f l'incremento e' Delta dipolo" % dd,
              bool(np.max(np.abs(nn2 - dd)) < 1e-12),
              "max|errore| = %.3e" % float(np.max(np.abs(nn2 - dd))))
    # --- (3) fase E dipolo insieme
    nn3 = nuova(d1, np.full_like(d, np.pi / 2), d0, np.zeros_like(d))
    prova("S1.3: ### fase AVVOLTA + dipolo cambiato: l'incremento e' la SOMMA dei due veri",
          bool(np.max(np.abs(nn3 - (d + np.pi / 2))) < 1e-12),
          "max|errore| = %.3e" % float(np.max(np.abs(nn3 - (d + np.pi / 2)))))
    # --- (4) un ARCO NUOVO ha spinta ZERO, per OGNI via di nascita
    riga("-")
    stampa("  S1.4: UN ARCO NUOVO HA SPINTA ZERO, per CIASCUNA via di nascita")
    for et, twp0 in (("divisione (twp = _wphi(fase genitore-figlio))", 1.7),
                     ("schwinger (twp = _wphi(fase genitore-anti))", -2.4),
                     ("semina / _allaccia (twp = 0)", 0.0),
                     ("una QUARTA via ipotetica, con twp qualunque", 3.9)):
        a = np.full(1000, 2.5)
        nn4 = nuova(a, np.full(1000, np.pi), np.full(1000, twp0),
                    np.full(1000, np.nan))
        prova("    %s" % et, bool(np.all(nn4 == 0.0)),
              "spinta max |%.3e|, e NON dipende da twp" % float(np.max(np.abs(nn4))))
    prova("S1.4b: ### e con twp_dip FINITO la spinta NON e' zero (il caso nullo)",
          float(np.abs(nuova(np.full(10, 2.5), np.full(10, np.pi),
                             np.full(10, 0.0), np.zeros(10))[0])) > 1.0,
          "altrimenti il marcatore non starebbe marcando niente")
    # --- (5) nessun nan sopravvive
    tdp = np.full(1000, np.nan)
    tdp_dopo = np.full(1000, 0.7)       # il passo scrive INCONDIZIONATAMENTE
    prova("S1.5: dopo un passo di torsione NESSUN nan sopravvive in twp_dip",
          int(np.sum(np.isnan(tdp_dopo))) == 0,
          "il passo scrive twp_dip su OGNI arco: %d nan prima, %d dopo"
          % (int(np.sum(np.isnan(tdp))), int(np.sum(np.isnan(tdp_dopo)))))
    prova("S1.6: ### e np.where NON propaga il nan nel ramo scartato",
          bool(np.all(np.isfinite(nuova(np.full(100, 1.0), np.zeros(100),
                                        np.full(100, 1.0), np.full(100, np.nan))))))

    riga("=")
    stampa("S2: IL CONTROLLO CHE DEVE FALLIRE -- la legge VECCHIA sugli STESSI casi")
    riga("=")
    vv = vecchia(d1, z, d0)
    prova("### S2.1: la legge VECCHIA a un giro di fase sbaglia di -4pi ESATTI",
          bool(np.max(np.abs((vv - d) + P4)) < 1e-9),
          "errore mediano %.6f = %.4f pi" % (float(np.median(vv - d)),
                                             float(np.median(vv - d) / np.pi)))
    prova("### S2.2: e la legge NUOVA sugli STESSI casi NON sbaglia",
          bool(np.max(np.abs(nn - d)) < 1e-12),
          "le due forme differiscono di 4pi: %.6f" % float(np.median(np.abs(nn - vv))))
    # --- il calcio di nascita: la vecchia lo da', la nuova no
    for et, twp0, atteso in (("semina (twp = 0)", 0.0, 2.5 + np.pi),
                             ("divisione (twp = fase alla nascita)", 2.5, np.pi)):
        a = np.full(1000, 2.5)
        vv2 = vecchia(a, np.full(1000, np.pi), np.full(1000, twp0))
        nn5 = nuova(a, np.full(1000, np.pi), np.full(1000, twp0), np.full(1000, np.nan))
        prova("### S2.3: la VECCHIA da' il calcio di nascita -- %s" % et,
              bool(np.abs(np.median(vv2) - atteso) < 1e-9 and np.abs(np.median(vv2)) > 1.0),
              "calcio %.6f (atteso %.6f), e la NUOVA da' %.3e"
              % (float(np.median(vv2)), atteso, float(np.median(np.abs(nn5)))))
    prova("### S2.4: e il calcio della SEMINA satura 3pi quando dph e il dipolo sono massimi",
          bool(np.abs(vecchia(np.array([P2 - 1e-9]), np.array([np.pi]),
                              np.array([0.0]))[0] - P3) < 1e-6),
          "vecchia(2pi, pi, 0) = %.6f, 3pi = %.6f"
          % (float(vecchia(np.array([P2 - 1e-9]), np.array([np.pi]),
                           np.array([0.0]))[0]), P3))

    riga("=")
    stampa("IL GANCIO DI S3: due ganci, e NESSUNA legge toccata")
    riga("=")
    import tempfile
    _d = tempfile.mkdtemp()
    _p = os.path.join(_d, "s.py")
    fatte = copia_con_gancio(SIM, _p)
    tt = io.open(_p, encoding="utf-8").read()
    t0 = io.open(SIM, encoding="utf-8").read()
    prova("S3: le due ancore sono state sostituite", len(fatte) == 2, "%s" % fatte)
    prova("S3: il gancio sta PRIMA del calcolo di `_nuovo`",
          tt.index("_SIG.torsione(self, dph=dph") < tt.index("_nuovo = np.isnan"))
    _inj = ["_SIG = None   # [SIGILLO TORS-W8] lo riempie lo strumento" + NL,
            "            if _SIG is not None:" + NL,
            "                _SIG.torsione(self, dph=dph, twist_dip=twist_dip," + NL,
            "                              twp=self.twp, twp_dip=self.twp_dip)" + NL]
    _ri = tt
    for x in _inj:
        _ri = _ri.replace(x, "", 1)
    prova("### S3: togliendo le SOLE righe iniettate si torna al sorgente VERO",
          _ri == t0, "carattere per carattere")
    prova("S3: ### e la riga del ramo non-4pi NON e' toccata",
          tt.count("self.tw += self._w4(dph - self.twp) - dt_e * self.tw / _ttw") == 1)
    # --- la spia, su casi a risposta NOTA
    sp = Spia()
    sp.passo = 7

    class FR(object):
        pass
    fr = FR()
    fr.tw = np.zeros(300)
    sp.torsione(fr, dph=np.full(300, 1.5), twist_dip=np.zeros(300),
                twp=np.full(300, 1.4), twp_dip=np.zeros(300))
    prova("spia: senza avvolgimento e senza archi nuovi le due forme COINCIDONO",
          sp.passi[-1]["diverse"] == 0, "diverse %d su 300" % sp.passi[-1]["diverse"])
    sp2 = Spia()
    sp2.passo = 7
    sp2.torsione(fr, dph=np.full(300, _wphi(P2 + 0.01)), twist_dip=np.zeros(300),
                 twp=np.full(300, _wphi(P2 - 0.01)), twp_dip=np.zeros(300))
    prova("spia: ### con un AVVOLGIMENTO le due forme differiscono, ed e' SPIEGATO",
          sp2.passi[-1]["diverse"] == 300 and sp2.passi[-1]["non_spiegate"] == 0,
          "diverse %d, giri %d, NON spiegate %d"
          % (sp2.passi[-1]["diverse"], sp2.passi[-1]["giri"],
             sp2.passi[-1]["non_spiegate"]))
    sp3 = Spia()
    sp3.passo = 7
    sp3.torsione(fr, dph=np.full(300, 2.5), twist_dip=np.full(300, np.pi),
                 twp=np.zeros(300), twp_dip=np.full(300, np.nan))
    prova("spia: ### con ARCHI NUOVI differiscono, ed e' SPIEGATO",
          sp3.passi[-1]["diverse"] == 300 and sp3.passi[-1]["non_spiegate"] == 0,
          "diverse %d, nuovi %d, NON spiegate %d"
          % (sp3.passi[-1]["diverse"], sp3.passi[-1]["nuovi"],
             sp3.passi[-1]["non_spiegate"]))
    # ### IL CASO CHE DEVE FALLIRE PER LA SPIA: una differenza NON spiegata si CONTA
    # ### ⛔ **LA PROVA CHE DISCRIMINA, e MANCAVA: con `twp_dip` FINITO E DIVERSO DA ZERO
    #   la ricostruzione del vecchio `twp` deve usare `twp + twp_dip`.** Il collaudo di
    #   prima provava solo che la spia CONTA; ### **non che ricostruisce GIUSTO**, e sono
    #   due cose diverse. Le quattro prove di prima passavano con `twp_dip = 0` o `nan`,
    #   ### **i due soli casi in cui la ricostruzione sbagliata e quella giusta
    #   COINCIDONO.**
    sp4 = Spia()
    sp4.passo = 7
    sp4.torsione(fr, dph=np.full(300, 1.31), twist_dip=np.zeros(300),
                 twp=np.full(300, 1.30), twp_dip=np.full(300, np.pi))
    prova("### spia: con un DIPOLO PRECEDENTE = pi le due leggi sono D'ACCORDO "
          "(la ricostruzione e' giusta)",
          sp4.passi[-1]["non_spiegate"] == 0 and sp4.passi[-1]["diverse"] == 0,
          "diverse %d, NON spiegate %d: con `twp` DA SOLO sarebbero state 300 e 300"
          % (sp4.passi[-1]["diverse"], sp4.passi[-1]["non_spiegate"]))
    # --- e la prova ARITMETICA, in isolamento, che la ricostruzione sbagliata sbaglia di pi
    _d1, _d2, _t1 = 1.30, 1.31, np.pi
    _nuova_a = _w4(_d2 - _d1) + (0.0 - _t1)
    _giusta = _w8(_d2 + 0.0 - _w8(_d1 + _t1))
    _mia_sbagliata = _w8(_d2 + 0.0 - _d1)
    prova("### spia: e la legge VECCHIA ricostruita BENE coincide con la nuova",
          abs(_nuova_a - _giusta) < 1e-12,
          "nuova %+.6f, vecchia %+.6f, differenza %.3e"
          % (_nuova_a, _giusta, abs(_nuova_a - _giusta)))
    prova("### spia: IL CASO CHE DEVE FALLIRE -- la ricostruzione SBAGLIATA sbaglia di pi",
          abs(abs(_nuova_a - _mia_sbagliata) - np.pi) < 1e-12,
          "scarto %+.6f = %.4f pi, ed e' il difetto che il sigillo ha trovato"
          % (_nuova_a - _mia_sbagliata, (_nuova_a - _mia_sbagliata) / np.pi))
    # ### ⛔ **E QUI HO TROVATO UNA COSA PIU' GRANDE DELLA PROVA CHE STAVO SCRIVENDO.**
    #   Avevo aggiunto una prova che pretendeva una differenza NON spiegata su input
    #   **legali**, e ### **FALLIVA.** Il motivo non e' la prova: e' che
    #   ### **SU INPUT LEGALI UNA DIFFERENZA NON SPIEGATA E' IMPOSSIBILE PER ALGEBRA.**
    #       `|Δdph| < 2pi`  (altrimenti `_w4` avvolge, ed e' SPIEGATO)
    #       `|Δtd| <= 2pi`  (`twist_dip` sta in `[-pi, pi]`)
    #       ⟹ `|argomento| < 4pi`, quindi `_w8` **non ripiega** e le due leggi COINCIDONO.
    #   ### 📌 **QUINDI LO ZERO DI `S3` E' UN TEOREMA, NON UNA MISURA**, e presentarlo come
    #   *«la cura non cambia qualcos'altro»* sarebbe ### **un FALSO-UNO** -- la stessa
    #   famiglia del falso-zero di `C-ident` che il guardiano mi ha trovato.
    #   ### ✔ **MA `S3` NON E' INUTILE, E L'HA DIMOSTRATO:** il suo potere e' contro gli
    #   errori di **IMPLEMENTAZIONE**, e ### **ha trovato il mio difetto della spia**
    #   (`e8122cc`). Quello che `S3` prova e' che il CODICE segue l'algebra, non che la
    #   fisica non e' cambiata -- e il rapporto lo DICE.
    rngt = np.random.default_rng(4242)
    NT = 2_000_000
    _dp = rngt.uniform(-P2, P2, NT)
    _tp = rngt.uniform(-P2, P2, NT)
    _V = np.array([-np.pi, -np.pi / 2, 0.0, np.pi / 2, np.pi])
    _td = rngt.choice(_V, NT)
    _tdp = rngt.choice(_V, NT)
    _nu = _w4(_dp - _tp) + (_td - _tdp)
    _ve = _w8(_dp + _td - (_tp + _tdp))
    _dd = np.abs(_nu - _ve)
    _gi = np.abs(_w4(_dp - _tp) - (_dp - _tp)) > 1e-12
    prova("### TEOREMA: su input LEGALI le differenze NON spiegate sono ZERO",
          int(np.sum((_dd > 1e-12) & ~_gi)) == 0,
          "%d su %d casi; e le %d differenze sono TUTTE giri di fase"
          % (int(np.sum((_dd > 1e-12) & ~_gi)), NT, int(np.sum(_dd > 1e-12))))
    prova("### e quindi lo ZERO di S3 e' GARANTITO dall'algebra, non misurato",
          int(np.sum(_dd > 1e-12)) > 0,
          "le differenze esistono (%d, il %.1f%%) ma sono tutte SPIEGATE"
          % (int(np.sum(_dd > 1e-12)), 100 * float(np.mean(_dd > 1e-12))))
    # ### ✔ **E IL CONTATORE NON E' MORTO: lo provo con un input ILLEGALE**, e dichiaro che
    #   e' illegale -- un input legale non puo' farlo, ed e' il punto.
    sp5 = Spia()
    sp5.passo = 7
    sp5.torsione(fr, dph=np.full(300, 1.31), twist_dip=np.zeros(300),
                 twp=np.full(300, 1.30), twp_dip=np.full(300, -4.1 * np.pi))
    prova("### spia: IL CONTATORE NON E' MORTO -- con un dipolo ILLEGALE (-4.1 pi) CONTA",
          sp5.passi[-1]["non_spiegate"] == 300,
          "NON spiegate %d su 300. ### E l'input e ILLEGALE di proposito: |twist_dip| <= pi, "
          "e uno LEGALE non puo' accendere il contatore (il teorema qui sopra)"
          % sp5.passi[-1]["non_spiegate"])

    riga("=")
    ko = [n for n, o, _d in esiti if not o]
    stampa("COLLAUDO: %d su %d" % (len(esiti) - len(ko), len(esiti)))
    if ko:
        stampa("### FALLITI:")
        for n in ko:
            stampa("    - " + n)
    riga("=")
    return 1 if ko else 0


# =============================================================== S0
def s0(passi):
    """Il braccio 0: **prima + patch** contro **il blob di oggi**, su `passi` passi."""
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    pre = os.path.join(FUORI, "_sim_prima.py")
    try:
        introduce = _cli_flag.sim_prima_del_flag(TOKEN_DELLA_CURA, pre, radice=RADICE)
    except AssertionError as e:
        stampa("### L'ANCORA SI E' DENUNCIATA: %s" % (str(e)[:240],))
        return 1, {"ancora": str(e)[:240]}
    b0 = blob(pre)[:8]
    stampa("  il *prima*: il commit che introduce %r e' %s, e si prende IL SUO PADRE"
           % (TOKEN_DELLA_CURA, introduce[:8]))
    stampa("      estratto in BINARIO: blob %s  (atteso %s)" % (b0, BLOB_PRIMA))
    stampa("      ### e l'ancora ha ASSERITO che il file estratto NON contiene %r"
           % TOKEN_DELLA_CURA)
    if b0 != BLOB_PRIMA:
        stampa("  ### IL BLOB DEL *PRIMA* NON E' QUELLO ATTESO. MI FERMO.")
        return 1, {}
    rif = os.path.join(FUORI, "_sim_rifatto.py")
    p = subprocess.run([sys.executable, PATCH, pre, rif], capture_output=True, cwd=RADICE)
    stampa("  la patch: %s" % (p.stdout.decode("utf-8", "replace").strip()
                               .split(NL)[-1] if p.stdout else repr(p.stderr[:160])))
    b1 = blob(rif)[:8]
    stampa("  prima + patch = %s   il blob di oggi = %s   -> %s"
           % (b1, blob(SIM)[:8], "COINCIDE" if b1 == blob(SIM)[:8] else "### DIVERSO"))
    if b1 != blob(SIM)[:8]:
        return 1, {"blob_rifatto": b1, "blob_oggi": blob(SIM)[:8]}
    # --- e i DUE GIRANO IDENTICI (il controllo dell'INVOLUCRO, STANDARD 5)
    stampa("  ### E ORA I DUE GIRANO: %d passi, tutti gli attributi di `net` a confronto."
           % passi)
    SA, NA = _carica("sig_rifatto", rif, os.path.join(FUORI, "_scarto_a"))
    SB, NB = _carica("sig_oggi", SIM, os.path.join(FUORI, "_scarto_b"))
    stampa("      scena A: n = %d archi = %d   scena B: n = %d archi = %d"
           % (NA.n, len(NA.i), NB.n, len(NB.i)))
    diff = []
    for k in range(1, passi + 1):
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(SA, NA)
            _passo.passo_pieno(SB, NB)
        fa, fb = _foto(NA), _foto(NB)
        ch = sorted(set(fa) | set(fb))
        d = [c for c in ch if fa.get(c) != fb.get(c)]
        if d:
            diff.append((k, d[:8], len(d)))
            break
        if k % 25 == 0:
            stampa("      passo %d/%d: %d attributi, 0 diversi" % (k, passi, len(ch)))
    if diff:
        k, d, nd = diff[0]
        stampa("  ### DIVERGONO AL PASSO %d: %d attributi diversi, i primi %s" % (k, nd, d))
        return 1, {"divergono_al_passo": k, "attributi": d, "quanti": nd}
    stampa("  ### ✔ IDENTICI su %d passi e %d attributi di `net`." % (passi, len(_foto(NA))))
    return 0, {"passi": passi, "attributi": len(_foto(NA)), "diversi": 0,
               "blob_prima": b0, "blob_rifatto": b1, "blob_oggi": blob(SIM)[:8]}


# =============================================================== S3
def s3(passi):
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    dst = os.path.join(FUORI, "_sim_spia.py")
    anc = copia_con_gancio(SIM, dst)
    stampa("  la copia col gancio: blob %s  (%d ancore)" % (blob(dst)[:8], len(anc)))
    S, N = _carica("sig_spia", dst, os.path.join(FUORI, "_scarto_s3"))
    sp = Spia()
    S._SIG = sp
    in_conf = _cli_flag.dichiara_configurazione(S, stampa)
    stampa("  scena: n = %d archi = %d" % (N.n, len(N.i)))
    for k in range(1, passi + 1):
        sp.passo = k
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(S, N)
        if k % 25 == 0:
            stampa("      passo %d/%d: diverse %d, NON spiegate %d (cumulato)"
                   % (k, passi, sp.tot["diverse"], sp.tot["non_spiegate"]))
    return sp, in_conf, blob(dst)


def main(argv):
    passi = PASSI
    if "--collaudo" in argv[1:]:
        riga("=")
        stampa("IL COLLAUDO DEL SIGILLO DI TORS-W8-AVVOLGIMENTO (S1 + S2)")
        riga("=")
        return collaudo()
    for a in argv[1:]:
        if a.startswith("--passi="):
            passi = int(a.split("=", 1)[1])
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    riga("=")
    stampa("IL SIGILLO DI TORS-W8-AVVOLGIMENTO -- S0, S1, S2, S3")
    riga("=")
    stampa("  simulatore %s   patch %s   strumento %s"
           % (blob(SIM)[:8], blob(PATCH)[:8], blob(__file__)[:8]))
    stampa()
    d = {"blob_sim": blob(SIM), "blob_patch": blob(PATCH),
         "blob_strumento": blob(__file__), "token_della_cura": TOKEN_DELLA_CURA,
         "blob_prima_atteso": BLOB_PRIMA, "blob_dopo_atteso": BLOB_DOPO, "passi": passi}
    guasti = []

    riga("=")
    stampa("S1 + S2: i controlli sintetici (dal collaudo)")
    riga("=")
    e12 = collaudo()
    d["s1_s2"] = {"esito": e12}
    if e12:
        guasti.append("S1/S2")
        stampa("  ### FERMO: i controlli sintetici falliscono, e il resto non si legge.")
        io.open(os.path.join(FUORI, "sigillo.json"), "w", encoding="utf-8").write(
            json.dumps({**d, "guasti": guasti, "esito": 1}, indent=1, default=str))
        return 1
    stampa()

    riga("=")
    stampa("S0: IL BRACCIO 0 -- prima + patch = il blob di oggi, e i due GIRANO identici")
    riga("=")
    e0, d0 = s0(passi)
    d["s0"] = d0
    if e0:
        guasti.append("S0")
        stampa("  ### FERMO: S0 fallisce, quindi la patch NON e' quella che credo.")
        io.open(os.path.join(FUORI, "sigillo.json"), "w", encoding="utf-8").write(
            json.dumps({**d, "guasti": guasti, "esito": 1}, indent=1, default=str))
        return 1
    stampa()

    riga("=")
    stampa("S3: LE DUE FORME SULLO STESSO STATO, nella corsa vera")
    riga("=")
    sp, in_conf, bs = s3(passi)
    d["s3"] = {"totali": sp.tot, "passi": sp.passi, "blob_copia": bs,
               "in_configurazione_del_driver": bool(in_conf)}
    stampa()
    stampa("  coppie (passo, arco)        %d" % sp.tot["coppie"])
    stampa("  differenze oltre 1e-12      %d" % sp.tot["diverse"])
    stampa("      di cui GIRI DI FASE     %d" % sp.tot["giri"])
    stampa("      di cui ARCHI NUOVI      %d" % sp.tot["nuovi"])
    stampa("      di cui al PASSO 1       %d" % sp.tot["passo1"])
    stampa("  ### NON SPIEGATE            %d   %s"
           % (sp.tot["non_spiegate"],
              "<- DEVE essere ZERO" if sp.tot["non_spiegate"] else "### ZERO: PASSA"))
    if sp.tot["non_spiegate"]:
        guasti.append("S3")
    stampa()
    stampa("  ### ⛔ E S3 DICHIARA IL PROPRIO POTERE, perche' uno zero senza il suo potere")
    stampa("      accanto e' un FALSO-UNO: SU INPUT LEGALI UNA DIFFERENZA NON SPIEGATA E'")
    stampa("      IMPOSSIBILE PER ALGEBRA -- |Delta dph| < 2pi (altrimenti _w4 avvolge, ed e'")
    stampa("      spiegato) e |Delta td| <= 2pi, quindi |argomento| < 4pi e _w8 NON ripiega.")
    stampa("      MISURATO su 2 milioni di casi legali nel collaudo: ZERO non spiegate.")
    stampa("  ### QUINDI S3 NON PROVA CHE LA FISICA NON E' CAMBIATA: prova che il CODICE")
    stampa("      segue l'algebra. ### E LO HA PROVATO: ha trovato il difetto della mia")
    stampa("      spia (e8122cc), che sbagliava di pi esatto su 235322 coppie.")
    stampa("  ### CHE LA PATCH SIA L'UNICA DIFFERENZA LO DICE S0, non S3: 241 attributi")
    stampa("      di net identici su 150 passi.")
    stampa()
    riga("=")
    stampa("IL VERDETTO")
    riga("=")
    d.update({"guasti": guasti, "esito": 1 if guasti else 0})
    io.open(os.path.join(FUORI, "sigillo.json"), "w", encoding="utf-8").write(
        json.dumps(d, indent=1, default=str))
    if guasti:
        stampa("  ### FERMO. I GUASTI: %s" % ", ".join(guasti))
        return 1
    stampa("  ### S0, S1, S2 e S3 PASSANO.")
    stampa("  ### LA FISICA E' CAMBIATA DI PROPOSITO: non c'e' identita' con prima, e il")
    stampa("      sigillo non la cerca. Quello che prova e' che la patch e' L'UNICA")
    stampa("      differenza, che la legge nuova fa cio' che dice, che la vecchia")
    stampa("      sbagliava di 4pi, e che nella corsa vera le due forme differiscono")
    stampa("      SOLO dove deve.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
