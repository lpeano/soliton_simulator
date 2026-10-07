# -*- coding: utf-8 -*-
"""`A-S1` — **IL TEST `H1` DI `SCIOGLIMENTO-FASE`: solo la SCENA cambia, nessuna legge.**

### ⛔ **L'IPOTESI `H1`, verificata sul sorgente di `b8c21049` e non ripresa da un
documento:** `_semina_masse_coerenti` *(`:9916`)* scrive ### **`net.phi[idx]`** e
### **`net.phi0[idx]`** e ### **NIENTE ALTRO** — `phivel` ### **non compare nella
funzione.** I nodi delle masse tengono il `phivel` che la ### **semina** ha dato a tutti
*(`:5068`-`:5077`)*.
### ➜ **Le masse nascono IN FASE e con VELOCITA' DI FASE CASUALI, e si sfasano per
costruzione.**

### ⭐ **L'INTERVENTO, ed e' `S1b` del task history del 2026-09-27, mai eseguita:** dopo la
costruzione e ### **PRIMA del passo `1`**, per ogni massa

```
net.phivel[idx] = media(net.phivel[idx])
```

### ✔ **Toglie SOLO la DISPERSIONE e NON cambia la velocita' media della massa**, e
### **non introduce nessun numero nuovo** *(`A1`: la legge, non il numero)*.
### ✔ **E' una modifica della CONDIZIONE INIZIALE, fatta NELLO STRUMENTO e dichiarata**:
### **nessun file del simulatore viene toccato.**

### ✔ **E NIENTE NELLA COSTRUZIONE DIPENDE DA QUELLE `phivel`** *(la verifica che il
mandato chiede, fatta col censimento)*: nel percorso di costruzione `phivel` e'
### **SCRITTA in coda** e ### **mai LETTA** per derivarne una grandezza immagazzinata --
`chi_nuovi` e' assegnata ### **PRIMA** *(`:5062`, e il commento lo dice)*, quindi la
dipendenza va ### **da `chi` a `phivel`**, non al contrario. ### **Sovrascrivere dopo la
costruzione non lascia stato incoerente, e NON consuma RNG** *(si sovrascrive, non si
ri-estrae)*.

### ⛔ **MA DUE ACCOPPIAMENTI DINAMICI, SCRITTI PRIMA DELLA CORSA**

`(1)` ### **IL CONFONDENTE.** `_tau_tw_locale` *(`:610`-`:627`)* calcola
`dom = |phivel[i] - phivel[j]| + 1e-3` e `tau_tw = max(2 pi / dom, 1e-3)`.
### ➜ **Azzerare la dispersione DENTRO una massa porta `dom` al PAVIMENTO `1e-3` sugli
archi intra-massa**, quindi `tau_tw -> 2 pi / 1e-3 = 6283.2` contro una mediana
### **MISURATA** di `2.4055` al passo `50`: ### **un fattore ~`2600`.**
### ⚠ **Quindi il braccio `H1` non cambia una cosa sola nelle sue CONSEGUENZE**, e
### **l'asimmetria e' scritta nel task history:** se l'`AUC` resta bassa `H1 NON BASTA`
vale ### **di piu'**; se risale, la causa e' ### **AMBIGUA** e il referto dira'
### **CONFONDUTO.**
### ✔ **E il confondente SI MISURA:** `tau_tw` mediana ### **intra-massa** e su
### **tutti** gli archi, a ogni passo misurato.

`(2)` ### **LA DISPERSIONE SI RI-INIETTA.** `scuoti_vuoto` sta nella
`PASSO_COMPOSIZIONE` *(`:965`)*, `SCUOTIMENTO` vale ### **sempre `True`** *(`:867`)*, il
registro lo dichiara *<<scrive `phivel` e nient'altro>>* *(`:1010`)* e il calcio e'
`net.phivel[:net.n] += calcio` *(`:938`)*.
### ➜ **L'equalizzazione e' una CONDIZIONE INIZIALE, non uno stato mantenuto.**

### 📌 **CRITERI E PREVISIONI: `doc/TASK_HISTORY/2026-10-07_as1-test-h1-scioglimento.md`**,
committato ### **PRIMA** di questo file *(`840a98d`)*.
"""
import contextlib
import io
import json
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
for _p in (os.path.join(RADICE, "csv"), _QUI):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import _presidio                                   # noqa: E402
_presidio.avvia(__file__)

import _passo                                      # noqa: E402
import _cli_flag                                   # noqa: E402
import _mitosi_soglia_grad as _MSG                 # noqa: E402
import _mitosi_zero_dove as _MZD                   # noqa: E402
import _misura_verso as MV                         # noqa: E402

stampa, riga, blob = _MSG.stampa, _MSG.riga, _MSG.blob
piattaforma, carica = _MSG.piattaforma, _MSG.carica
NL = chr(10)
SIM = os.path.join(RADICE, "soliton_simulator.py")
BLOB_ATTESO = "b8c21049"
FUORI = os.path.join(_QUI, "_massa_h1")
PASSI = 500
PASSI_MISURA = (1, 50, 150, 230, 300, 400, 500)
PASSI_SALVA = 10
# ### ⚠ **AL PASSO `50` IL CONTROLLO (`A1`) NON HA L'`AUC`**: i suoi passi pesanti sono
#   `1, 150, 230, 300, 400, 500, 700, 1000`. ### **Gli altri SEI hanno il controllo, e i due
#   su cui i criteri DECIDONO -- `400` e `500` -- ce l'hanno.** Si dichiara, non si tace.
PASSI_SENZA_CONTROLLO = (50,)
# ### I CRITERI DI LUCA, fissati nel task history PRIMA della corsa.
CRIT_BASTA = {400: 0.90, 500: 0.85}
CRIT_NON_BASTA = {400: 0.60}
SOGLIA_CURVA = 0.60


# ==========================================================================
#   LE COORTI E L'INTERVENTO
# ==========================================================================
def coorti(S):
    """Le coorti che la ### **scena** registra: `massa_0/1/2` e `vuoto`.

    ### ⛔ **NON le ricostruisco dalla geometria:** la scena le scrive in
    `test["dati"]["coorti"]` *(`:9988`)*, e ### **ricostruirle sarebbe una seconda
    definizione** *(`9-ter`)*. ### **Se mancano o sono vuote: FERMO.**
    """
    c = ((getattr(S, "test", None) or {}).get("dati") or {}).get("coorti") or {}
    masse = {k: np.asarray(v, int) for k, v in c.items() if str(k).startswith("massa_")}
    vuoto = np.asarray(c.get("vuoto", []), int)
    if not masse:
        raise SystemExit("[FERMO] nessuna coorte `massa_*` in `test['dati']['coorti']`: "
                         "le chiavi presenti sono %r." % (sorted(c.keys()),))
    vuote = [k for k, v in masse.items() if len(v) == 0]
    if vuote:
        raise SystemExit("[FERMO] coorti di massa VUOTE: %r." % (sorted(vuote),))
    if len(vuoto) == 0:
        raise SystemExit("[FERMO] la coorte `vuoto` e' vuota: senza di lei non c'e' il "
                         "NULLO, e ogni numero per massa si leggerebbe contro ZERO.")
    return masse, vuoto


def equalizza(S, net, sabota=None):
    """### ⭐ **L'INTERVENTO: `phivel` dei nodi di ogni massa = la MEDIA delle loro.**

    `sabota` esiste ### **solo per il collaudo**: serve a provare che il controllo del
    passo `0` ### **SI FERMA** se l'intervento tocca qualcosa che non deve toccare.
    ### **Un controllo che non si e' mai visto fallire non e' un controllo.**
    """
    masse, _vuoto = coorti(S)
    pv = np.asarray(net.phivel, float)
    rapp = {}
    for et, idx in sorted(masse.items()):
        ii = idx[idx < len(pv)]
        v = pv[ii]
        m = float(np.mean(v))
        rapp[et] = {"nodi": int(len(ii)), "media": m,
                    "std_prima": float(np.std(v)),
                    "min_prima": float(np.min(v)), "max_prima": float(np.max(v))}
        net.phivel[ii] = m
    if sabota == "fase":
        net.phi[masse[sorted(masse)[0]][0]] += 0.1       # tocca `phi`: NON deve passare
    elif sabota == "vuoto":
        net.phivel[int(_vuoto[0])] += 0.1                # tocca il VUOTO: NON deve passare
    return rapp


# ==========================================================================
#   IL CONTROLLO DEL PASSO `0`
# ==========================================================================
def confronta_passo_zero(N_nudo, N_eq, masse, rapp):
    """Le reti al passo `0` devono differire ### **SOLO in `phivel` dei nodi delle masse.**

    ### ✔ **Si confronta con la `_firma` del presidio su TUTTO `net.__dict__`**, come la
    byte-inerzia. ### ⛔ **E la verifica NON e' <<phivel differisce>>:** un nodo la cui
    `phivel` era GIA' la media ### **non differisce**, e pretenderlo darebbe un falso
    allarme. ### **Le due affermazioni VERE sono:**
      `(1)` fuori dai nodi delle masse `phivel` e' ### **identica AL BIT**;
      `(2)` dentro, vale ### **ESATTAMENTE la media dichiarata**.
    """
    guai = []
    f1 = {k: MV._firma(v) for k, v in N_nudo.__dict__.items()}
    f2 = {k: MV._firma(v) for k, v in N_eq.__dict__.items()}
    solo1 = sorted(set(f1) - set(f2))
    solo2 = sorted(set(f2) - set(f1))
    if solo1:
        guai.append("attributi solo nel NUDO: %r" % (solo1,))
    if solo2:
        guai.append("attributi solo nell'EQUALIZZATO: %r" % (solo2,))
    diversi = sorted(k for k in set(f1) & set(f2) if f1[k] != f2[k])
    altri = [k for k in diversi if k != "phivel"]
    if altri:
        guai.append("attributi diversi OLTRE `phivel`: %r" % (altri,))
    if "phivel" not in diversi:
        guai.append("`phivel` NON e' cambiata: l'intervento non ha fatto niente, e un "
                    "confronto fra due reti identiche sarebbe un FALSO-UNO")
    # --- le due affermazioni vere
    p1 = np.asarray(N_nudo.phivel, float)
    p2 = np.asarray(N_eq.phivel, float)
    if p1.shape != p2.shape:
        guai.append("`phivel` ha forme diverse: %r contro %r" % (p1.shape, p2.shape))
        return guai, {"nodi_di_massa": 0, "fuori_identici": 0}
    dentro = np.zeros(len(p1), bool)
    for et, idx in sorted(masse.items()):
        dentro[idx[idx < len(p1)]] = True
    fuori = ~dentro
    n_fuori_div = int(np.sum(p1[fuori] != p2[fuori]))
    if n_fuori_div:
        guai.append("`phivel` DIVERSA su %d nodi FUORI dalle masse: l'intervento ha "
                    "toccato il vuoto" % n_fuori_div)
    for et, idx in sorted(masse.items()):
        ii = idx[idx < len(p1)]
        m = rapp[et]["media"]
        if not np.all(p2[ii] == m):
            guai.append("`%s`: %d nodi non valgono ESATTAMENTE la media dichiarata"
                        % (et, int(np.sum(p2[ii] != m))))
    return guai, {"nodi_di_massa": int(np.sum(dentro)),
                  "fuori_identici": int(np.sum(p1[fuori] == p2[fuori])),
                  "attributi": len(f1), "diversi": diversi}


def controllo_passo_zero():
    """Costruisce DUE reti, equalizza UNA, e confronta. ### **Se trova guai: FERMO.**"""
    riga("=")
    stampa("IL CONTROLLO DEL PASSO 0: le due reti differiscono SOLO in `phivel` delle masse")
    riga("=")
    b = blob(SIM)
    stampa("  simulatore %s   atteso %s" % (b[:8], BLOB_ATTESO))
    if not b.startswith(BLOB_ATTESO):
        raise SystemExit("[FERMO] il blob del simulatore NON e' quello atteso.")
    with contextlib.redirect_stdout(io.StringIO()):
        S1, N1, _a1 = carica("h1_nudo", SIM)
        S2, N2, _a2 = carica("h1_eq", SIM)
    masse, vuoto = coorti(S2)
    stampa("  masse: %s   vuoto: %d nodi"
           % (", ".join("%s %d" % (k, len(v)) for k, v in sorted(masse.items())), len(vuoto)))
    rapp = equalizza(S2, N2)
    for et in sorted(rapp):
        r = rapp[et]
        stampa("    %-8s nodi %5d   media %+.6f   std PRIMA %.6f   [%+.4f, %+.4f]"
               % (et, r["nodi"], r["media"], r["std_prima"], r["min_prima"], r["max_prima"]))
    guai, conta = confronta_passo_zero(N1, N2, masse, rapp)
    stampa()
    stampa("  attributi firmati: %d   diversi: %r" % (conta["attributi"], conta["diversi"]))
    stampa("  nodi delle masse: %d   nodi FUORI con `phivel` IDENTICA al bit: %d"
           % (conta["nodi_di_massa"], conta["fuori_identici"]))
    riga("-")
    if guai:
        for g in guai:
            stampa("  ### ⛔ %s" % g)
        stampa("  ### ⛔ IL CONTROLLO DEL PASSO 0 FALLISCE. LA CORSA NON PARTE.")
    else:
        stampa("  ### ✔ IL CONTROLLO PASSA: differisce SOLO `phivel`, e SOLO sui nodi "
               "delle masse.")
    riga("=")
    d = {"piattaforma": piattaforma(), "blob_sim": b, "blob_atteso": BLOB_ATTESO,
         "blob_strumento": blob(__file__),
         "masse": {k: int(len(v)) for k, v in sorted(masse.items())},
         "vuoto": int(len(vuoto)), "intervento": rapp,
         "conteggi": conta, "guai": guai,
         "esito": "PASSA" if not guai else "FALLISCE"}
    os.makedirs(FUORI, exist_ok=True)
    io.open(os.path.join(FUORI, "passo0.json"), "w", encoding="utf-8").write(
        json.dumps(d, indent=1, ensure_ascii=False))
    io.open(os.path.join(FUORI, "passo0.txt"), "w", encoding="utf-8").write(
        NL.join(_MSG.P) + NL)
    return 0 if not guai else 1


# ==========================================================================
#   L'OSSERVATORE
# ==========================================================================
class MassaH1(object):
    """Le misure di `A-S1`. ### **`m2` di `A1` non si ricopia: si CHIAMA.**"""

    nome = "massa_h1"

    def __init__(self, equalizza_si):
        self.equalizza_si = bool(equalizza_si)
        self.passi = []
        self.misure = {}
        self.avvisi = []
        self.toccati = {}
        self.geo = {}

    # ---------------------------------------------------------------- la scena
    def prepara(self, S, net):
        """### ⭐ **E' QUI CHE L'INTERVENTO AVVIENE: dopo la costruzione, PRIMA del passo 1.**

        `MV.corsa` chiama `prepara` subito dopo `carica` e ### **prima di ogni passo**,
        quindi questo e' esattamente lo slot che il mandato chiede -- e sta
        ### **nello strumento**, non nel simulatore.
        """
        self.g = _MZD.Misura(S.DT, 0.0)
        self.geo = self.g.prepara(S, net)
        # ### ⛔ **`MV.Verso` SI USA SOLO PER `m2` E `classe_nodi`, e NON si `prepara`:**
        #   `Verso.prepara` installerebbe gli ### **involucri di nascita**, che qui non
        #   servono *(non misuro l'origine degli archi)*. ### **Gli attributi che `m2` e
        #   `classe_nodi` leggono sono TRE, e li passo a mano.**
        self._v = MV.Verso()
        self._v.g = self.g
        self._v.geo = self.geo
        self._v.avvisi = self.avvisi
        self._v.toccati = self.toccati
        self.masse, self.vuoto = coorti(S)
        self.geo["masse"] = {k: int(len(v)) for k, v in sorted(self.masse.items())}
        self.geo["vuoto_nodi"] = int(len(self.vuoto))
        self.geo["braccio"] = "H1 (phivel equalizzata)" if self.equalizza_si else "CONTROLLO"
        self.geo["intervento"] = equalizza(S, net) if self.equalizza_si else None
        return self.geo

    # ---------------------------------------------------------------- le misure
    def _tau(self, S, net):
        """`tau_tw` per arco, ### **dentro il presidio** e col ramo scalare gestito."""
        with MV.sola_lettura(net, "_tau_tw_locale") as g:
            t = np.asarray(S._tau_tw_locale(net), float) * np.ones(len(net.i))
        self.toccati.setdefault("_tau_tw_locale", g["toccati"])
        return t

    def _etichetta_nodi(self, net):
        """Da nodo a indice di massa, ### **`-1` fuori.** Le coorti sono insiemi FISSI."""
        lab = np.full(int(net.n), -1, int)
        for q, et in enumerate(sorted(self.masse)):
            idx = self.masse[et]
            lab[idx[idx < net.n]] = q
        return lab

    def osserva(self, S, net, k, pesante):
        r = {"passo": int(k), "n": int(net.n), "archi": int(len(net.i))}
        tw = np.asarray(net.tw, float)
        r["fraz_tw_oltre_2pi"] = (float(np.mean(np.abs(tw) > MV.P2PI))
                                  if tw.size else None)
        self.passi.append(r)
        if k not in PASSI_MISURA:
            return
        cl, _u = self._v.classe_nodi(net)
        fuori = {"n": int(net.n), "archi": int(len(net.i))}
        # --- (1) l'AUC e `c_k`: ### **LO STESSO CALCOLO DI `A1`**
        m2 = self._v.m2(S, net, cl)
        fuori["auc_materia_vuoto"] = m2.get("auc_materia_vuoto")
        fuori["c_per_classe"] = m2.get("c_per_classe")
        fuori["senza_controllo"] = bool(k in PASSI_SENZA_CONTROLLO)
        # --- (2) la coerenza di fase e la dispersione di `phivel`, PER MASSA e nel VUOTO
        ph = np.asarray(net.phi, float)
        pv = np.asarray(net.phivel, float)

        def _gruppo(idx):
            ii = idx[idx < int(net.n)]
            if len(ii) == 0:
                return None
            return {"nodi": int(len(ii)),
                    # ### ⚠ **DUE COERENZE, e la differenza NON e' pedanteria:** `phi` vive
                    #   su ### **`4 pi`**, quindi `e^{i phi}` identifica `phi` con
                    #   `phi + 2 pi`. ### **Il campo del simulatore usa `exp(1j*phi)`**
                    #   *(`:5195`)*, quindi la PRIMA e' quella che il codice VEDE; la
                    #   seconda e' quella fedele al dominio. ### **Si riportano entrambe.**
                    "coer_2pi": float(np.abs(np.mean(np.exp(1j * ph[ii])))),
                    "coer_4pi": float(np.abs(np.mean(np.exp(0.5j * ph[ii])))),
                    "phivel_std": float(np.std(pv[ii])),
                    "phivel_media": float(np.mean(pv[ii]))}

        fuori["per_massa"] = {et: _gruppo(self.masse[et]) for et in sorted(self.masse)}
        # ### ⛔ **IL NULLO, e non e' lo zero:** la stessa misura sul VUOTO.
        fuori["vuoto"] = _gruppo(self.vuoto)
        _vv = fuori["vuoto"]
        if _vv and _vv["phivel_std"] > 0:
            fuori["disp_rel_per_massa"] = {
                et: (None if not x else x["phivel_std"] / _vv["phivel_std"])
                for et, x in fuori["per_massa"].items()}
        else:
            fuori["disp_rel_per_massa"] = None
        # --- (3) ### ⭐ **IL CONFONDENTE, MISURATO: `tau_tw` intra-massa contro tutti**
        if len(net.i):
            tau = self._tau(S, net)
            lab = self._etichetta_nodi(net)
            ii = np.asarray(net.i, int)
            jj = np.asarray(net.j, int)
            mm = (ii < net.n) & (jj < net.n)
            intra = np.zeros(len(ii), bool)
            intra[mm] = (lab[ii[mm]] >= 0) & (lab[ii[mm]] == lab[jj[mm]])
            fuori["tau_tw"] = {
                "mediana_tutti": float(np.median(tau[mm])) if np.any(mm) else None,
                "mediana_intra_massa": (float(np.median(tau[intra]))
                                        if np.any(intra) else None),
                "archi_intra_massa": int(np.sum(intra)),
                "archi_confrontabili": int(np.sum(mm))}
            _t = fuori["tau_tw"]
            _a, _b = _t["mediana_intra_massa"], _t["mediana_tutti"]
            _t["rapporto_intra_su_tutti"] = (None if not (_a and _b) else _a / _b)
        else:
            fuori["tau_tw"] = None
        self.misure[int(k)] = fuori

    # ---------------------------------------------------------------- l'esito
    def esito(self):
        return {"geometria": self.geo, "braccio_h1": self.equalizza_si,
                "passi": self.passi,
                "misure": {str(k): v for k, v in sorted(self.misure.items())},
                "passi_misura": list(PASSI_MISURA),
                "passi_senza_controllo": list(PASSI_SENZA_CONTROLLO),
                "scritture_misurate": self.toccati,
                "avvisi": self.avvisi}


# ==========================================================================
#   LA CORSA
# ==========================================================================
def _scrivi(d):
    os.makedirs(FUORI, exist_ok=True)
    io.open(os.path.join(FUORI, "h1.json"), "w", encoding="utf-8").write(
        json.dumps(d, ensure_ascii=False))


def corsa(passi, osservatore):
    """Il ciclo. ### **Non riuso `MV.corsa` e il motivo e' dichiarato:** le sue costanti
    *(`PASSI_PESANTI`, `PASSI_SALVA`)* sono quelle di ### **`A1`**, e ### **ri-legarle a
    quelle di `A-S1` vorrebbe dire patchare un modulo e ripristinarlo** -- piu' fragile
    delle trenta righe qui sotto. ### **Tutto cio' che e' SOSTANZIALE, invece, si
    CHIAMA:** `carica`, `dichiara_configurazione`, `passo_pieno`, `sola_lettura`, `m2`.
    """
    b = blob(SIM)
    riga("=")
    stampa("`A-S1` -- IL TEST H1: %d passi, braccio %s"
           % (passi, "H1" if osservatore.equalizza_si else "CONTROLLO"))
    riga("=")
    stampa("  simulatore %s   atteso %s" % (b[:8], BLOB_ATTESO))
    if not b.startswith(BLOB_ATTESO):
        raise SystemExit("[FERMO] il blob del simulatore NON e' quello atteso.")
    with contextlib.redirect_stdout(io.StringIO()):
        S, N, _a = carica("as1_h1", SIM)
    in_conf = _cli_flag.dichiara_configurazione(S, stampa)
    stampa("  scena: n = %d, archi = %d, DT = %r" % (N.n, len(N.i), S.DT))
    g = osservatore.prepara(S, N)
    stampa("  geometria: %s" % {k: v for k, v in g.items() if k != "intervento"})
    if g.get("intervento"):
        for et in sorted(g["intervento"]):
            x = g["intervento"][et]
            stampa("  INTERVENTO %-8s nodi %5d  media %+.6f  std PRIMA %.6f"
                   % (et, x["nodi"], x["media"], x["std_prima"]))
    stampa()
    t0 = time.time()

    def _ist(stato, k, err=None):
        d = {"piattaforma": piattaforma(), "passi": passi, "passi_girati": k,
             "stato": stato, "blob_sim": b, "blob_atteso": BLOB_ATTESO,
             "blob_strumento": blob(__file__), "blob_misura_verso": blob(MV.__file__),
             "in_configurazione_del_driver": bool(in_conf),
             "secondi": round(time.time() - t0, 1),
             "a_valle": {"n": int(N.n), "archi": int(len(N.i))},
             osservatore.nome: osservatore.esito()}
        if err is not None:
            d["errore"] = err
        _scrivi(d)
        return d

    osservatore.osserva(S, N, 0, True)
    for k in range(1, passi + 1):
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                _passo.passo_pieno(S, N)
            pes = k in PASSI_MISURA
            t1 = time.time()
            osservatore.osserva(S, N, k, pes)
            print("  passo %4d/%d  n %5d  archi %7d  %s%s"
                  % (k, passi, N.n, len(N.i), "MISURA " if pes else "",
                     ("%.1fs" % (time.time() - t1)) if pes else ""), flush=True)
            if k % PASSI_SALVA == 0:
                _ist("IN CORSO", k)
        except SystemExit:
            raise
        except Exception as e:                        # noqa: BLE001
            import traceback
            tb = traceback.format_exc()
            stampa("### LA CORSA E' CADUTA AL PASSO %d: %r" % (k, e))
            stampa(tb)
            _ist("CADUTA al passo %d" % k, k,
                 err={"passo": k, "errore": repr(e), "traccia": tb})
            return 1
    _ist("DATI SALVATI", passi)
    stampa("  ### I DATI SONO SALVATI.")
    return 0


# ==========================================================================
#   IL COLLAUDO
# ==========================================================================
class _FintoNet(object):
    pass


def _finta_scena(n=10, masse=((0, 1, 2), (3, 4)), vuoto=(5, 6, 7, 8, 9)):
    class _S(object):
        pass

    S = _S()
    c = {"vuoto": np.asarray(vuoto, int)}
    for q, m in enumerate(masse):
        c["massa_%d" % q] = np.asarray(m, int)
    S.test = {"dati": {"coorti": c}}
    net = _FintoNet()
    net.n = n
    net.phivel = np.arange(float(n))
    net.phi = np.linspace(0.0, 1.0, n)
    return S, net


def collaudo():
    esiti = []

    def prova(et, ok):
        esiti.append(bool(ok))
        stampa("  %s  %s" % ("ok  " if ok else "FALLITO", et))

    # ---- le coorti
    S, net = _finta_scena()
    masse, vuoto = coorti(S)
    prova("coorti: ### due masse e il VUOTO, dalla scena e non ricostruite",
          sorted(masse) == ["massa_0", "massa_1"] and len(vuoto) == 5)
    S2, _n2 = _finta_scena(masse=((0, 1), ()))
    rotto = False
    try:
        coorti(S2)
    except SystemExit:
        rotto = True
    prova("coorti: ### DEVE FALLIRE -- una coorte di massa VUOTA ferma tutto", rotto)
    S3, _n3 = _finta_scena(vuoto=())
    rotto = False
    try:
        coorti(S3)
    except SystemExit:
        rotto = True
    prova("coorti: ### DEVE FALLIRE -- senza il VUOTO non c'e' il NULLO, e ogni numero "
          "per massa si leggerebbe contro ZERO", rotto)

    # ---- l'intervento
    S, net = _finta_scena()
    pv0 = net.phivel.copy()
    rapp = equalizza(S, net)
    prova("intervento: ### `massa_0` va alla media `1.0` *(era `0,1,2`)*",
          abs(rapp["massa_0"]["media"] - 1.0) < 1e-12
          and np.all(net.phivel[[0, 1, 2]] == 1.0))
    prova("intervento: ### `massa_1` va a `3.5` *(era `3,4`)*",
          abs(rapp["massa_1"]["media"] - 3.5) < 1e-12
          and np.all(net.phivel[[3, 4]] == 3.5))
    prova("intervento: ### il VUOTO NON si tocca, al bit",
          np.all(net.phivel[5:] == pv0[5:]))
    prova("intervento: ### la MEDIA della massa e' CONSERVATA",
          abs(float(np.mean(net.phivel[[0, 1, 2]])) - float(np.mean(pv0[[0, 1, 2]]))) < 1e-12)
    prova("intervento: ### e la DISPERSIONE va a ZERO, che e' il punto",
          float(np.std(net.phivel[[0, 1, 2]])) == 0.0
          and rapp["massa_0"]["std_prima"] > 0.0)
    prova("intervento: ### `phi` NON si tocca", np.all(net.phi == np.linspace(0.0, 1.0, 10)))

    # ---- ### ⛔ **IL CONTROLLO DEL PASSO `0`, E I CASI CHE DEVONO FALLIRE**
    S, A = _finta_scena()
    _S2, B = _finta_scena()
    rapp = equalizza(S, B)
    guai, conta = confronta_passo_zero(A, B, masse, rapp)
    prova("passo0: ### con l'intervento PULITO il controllo NON trova guai: %r" % (guai,),
          guai == [])
    prova("passo0: ### e conta i nodi -- `5` di massa, `5` fuori identici",
          conta["nodi_di_massa"] == 5 and conta["fuori_identici"] == 5)
    # il caso del mandato: un attributo DIVERSO da `phivel`
    S, A = _finta_scena()
    _S3, C = _finta_scena()
    rapp = equalizza(S, C, sabota="fase")
    guai, _c = confronta_passo_zero(A, C, masse, rapp)
    prova("passo0: ### DEVE FALLIRE -- se l'intervento tocca `phi`, il controllo lo NOMINA "
          "*(ed e' il caso che il mandato chiede)*",
          any("OLTRE `phivel`" in g and "phi" in g for g in guai))
    # il caso gemello: un nodo del VUOTO
    S, A = _finta_scena()
    _S4, D = _finta_scena()
    rapp = equalizza(S, D, sabota="vuoto")
    guai, _c = confronta_passo_zero(A, D, masse, rapp)
    prova("passo0: ### DEVE FALLIRE -- se tocca un nodo del VUOTO, il controllo lo dice",
          any("FUORI dalle masse" in g for g in guai))
    # ### ⛔ **E IL FALSO-UNO: due reti IDENTICHE non devono <<passare>>**
    S, A = _finta_scena()
    _S5, E = _finta_scena()
    guai, _c = confronta_passo_zero(A, E, masse, {"massa_0": {"media": 1.0},
                                                  "massa_1": {"media": 3.5}})
    prova("passo0: ### DEVE FALLIRE -- due reti IDENTICHE: `phivel` non e' cambiata, e "
          "senza questa guardia il confronto sarebbe un FALSO-UNO",
          any("NON e' cambiata" in g for g in guai))

    # ---- la coerenza: le DUE letture, e il caso che le distingue
    _ph = np.array([0.0, 2.0 * np.pi])
    c2 = float(np.abs(np.mean(np.exp(1j * _ph))))
    c4 = float(np.abs(np.mean(np.exp(0.5j * _ph))))
    prova("coerenza: ### due fasi a `0` e `2pi` danno `1` su `2pi` e `0` su `4pi` -- "
          "### **le due letture NON sono la stessa cosa**, e per questo si riportano "
          "entrambe", abs(c2 - 1.0) < 1e-12 and c4 < 1e-12)
    prova("coerenza: ### e su fasi UGUALI valgono entrambe `1`",
          abs(float(np.abs(np.mean(np.exp(1j * np.zeros(4))))) - 1.0) < 1e-12
          and abs(float(np.abs(np.mean(np.exp(0.5j * np.zeros(4))))) - 1.0) < 1e-12)

    # ---- il confondente: il conto che lo prevede
    dom = 1e-3
    prova("confondente: ### con la dispersione a ZERO `tau_tw` va a `2pi/1e-3 = 6283.2`, "
          "contro una mediana misurata di `2.4055`: il fattore e' ~`2600`",
          abs((2 * np.pi / dom) - 6283.185307) < 1e-3
          and (2 * np.pi / dom) / 2.4055 > 2500.0)

    # ---- i criteri, come li ha fissati Luca
    prova("criteri: ### `H1 BASTA` vuole `>= 0.90` al `400` E `>= 0.85` al `500`",
          CRIT_BASTA == {400: 0.90, 500: 0.85})
    prova("criteri: ### `H1 NON BASTA` vuole `< 0.60` al `400`",
          CRIT_NON_BASTA == {400: 0.60})
    prova("criteri: ### e il passo `50` e' DICHIARATO senza controllo",
          PASSI_SENZA_CONTROLLO == (50,) and 50 in PASSI_MISURA)

    riga("-")
    stampa("  COLLAUDO: %d su %d" % (sum(esiti), len(esiti)))
    return 0 if all(esiti) else 1


# ==========================================================================
def main(argv):
    a = argv[1:]
    if "--collaudo" in a:
        riga("=")
        stampa("IL COLLAUDO DI _massa_h1.py")
        riga("=")
        return collaudo()
    if "--passo0" in a:
        return controllo_passo_zero()
    passi = PASSI
    for x in a:
        if x.startswith("--passi="):
            passi = int(x.split("=", 1)[1])
    # ### **Il braccio di CONTROLLO esiste come OPZIONE** *(`--controllo`)*, ma
    #   ### **non si gira:** il controllo e' la corsa `A1` *(`67f020e`)*. Serve per il
    #   giorno in cui servisse una grandezza che `A1` non ha registrato.
    eq = "--controllo" not in a
    e = corsa(passi, MassaH1(eq))
    io.open(os.path.join(FUORI, "h1.txt"), "w", encoding="utf-8").write(
        NL.join(_MSG.P) + NL)
    return e


if __name__ == "__main__":
    sys.exit(main(sys.argv))
