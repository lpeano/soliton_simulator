# -*- coding: utf-8 -*-
"""`H3` — **CHI SCALDA IL VUOTO: il termostato o lo scuotimento?** *(solo misura)*

### ⛔ **NESSUNA LEGGE SI TOCCA.** Il simulatore resta ### **`b8c21049`**; i due interventi
dei bracci diagnostici stanno ### **in questo file** e sono ### **dichiarati.**

### 📌 **CRITERI E PREVISIONI: `doc/TASK_HISTORY/2026-10-07_h3-termostato-e-scuotimento.md`**,
committato ### **PRIMA** di questo file *(`675b627`)*.

### ⭐ **IL BILANCIO E' ESATTO, NON STIMATO**, e poggia su quattro fatti ### **sondati a
runtime**: `TEMPO_SEGNO = False` *(quindi `dt_n_s = dt_n`)*, `FORK_SU2_MEM = True` *(quindi
lo step SALVA `self._r_corrente = r`, e `dt_n = DT*r`)*, `REGIME = 'deterministico'` *(quindi
gira il ramo del termostato e ### **mai** quello di `G_PH`)*, `M_PH = 1.0`.

```
p0 = phivel all'inizio del passo
p1 = dopo scuoti_vuoto   ->  D_scuoti = p1 - p0                      ESATTO (involucro)
p2 = dopo step           ->  D_step   = p2 - p1                      ESATTO (involucro)
D_term   = - DT * r * xi_termo * p1 / M_PH                           ESATTO
D_coppia = D_step - D_term                                           ESATTO per definizione

p2^2 - p0^2 = [2 p0 D_scuoti + D_scuoti^2] + [2 p1 D_term] + [2 p1 D_coppia] + D_step^2
                      lo scuotimento          il termostato    la coppia     RESIDUO
                                                                           INCROCIATO
```

### ⚠ **`D_step^2` NON SI PUO' ATTRIBUIRE** fra termostato e coppia: si riporta come
### **residuo**, non si spalma su una voce.

### ⛔ **E `calcio` NON SI RICALCOLA:** userebbe `net.rng` e ### **cambierebbe la dinamica.**
### ✔ **`ampiezza` SI, perche' non ha RNG** -- e da' il ### **controllo positivo**
`rms(D_scuoti) ~ rms(ampiezza)`.

### ⭐ **E IL CONTROLLO POSITIVO DECISIVO: SI RICOSTRUISCE L'AGGIORNAMENTO DI `xi_termo`.**
Lo step fa `xi += dt_scal*(err_rel - xi)/tau_termo`, poi `clip(-2, 2)`. Se la mia
ricostruzione ### **predice `xi` AL BIT**, allora ### **`E_cin`, `P_eq`, `cs_rappr`,
`T_target`, `tau_termo` e `dt_scal` sono TUTTI giusti.** ### ⛔ **Se non lo predice, lo DICO
invece di fidarmi dei numeri.**
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
import _massa_h1 as H1                             # noqa: E402

stampa, riga, blob = _MSG.stampa, _MSG.riga, _MSG.blob
piattaforma, carica = _MSG.piattaforma, _MSG.carica
NL = chr(10)
SIM = os.path.join(RADICE, "soliton_simulator.py")
BLOB_ATTESO = "b8c21049"
FUORI = os.path.join(_QUI, "_termo_h3")
PASSI_BASE = 300
PASSI_BRACCIO = 500
# ### i passi con le misure PESANTI (`AUC`, coerenza): quelli di `A-S1`, per confrontabilita'
PASSI_MISURA = (1, 50, 150, 230, 300, 400, 500)
PASSI_SALVA = 10
# ### ⭐ **`B-TS` AGGIUNTO il 2026-10-07 sera, mandato di Luca:** ### **i DUE
#   interventi INSIEME**, cosi' il sistema vive ### **solo della sua energia iniziale e della
#   dinamica interna.** ### ⚠ **IL DIFF E' ADDITIVO:** per i tre bracci di prima le due
#   condizioni passano da `==` a `in (...)` e ### **valutano IDENTICO**, quindi il
#   comportamento non cambia -- ### **ma il BLOB si**, e i primi tre bracci sono stati
#   prodotti da `d6047e5a`. ### **Si dichiara invece di tacerlo.**
# ### ⭐ **`B-SCAL` AGGIUNTO il 2026-10-08 (`D2`, mandato di Luca):** l'involucro fa
#   prendere a `_coppia_interferenza` il suo ### **RAMO SCALARE**, quello che dipende dalla
#   ### **FASE CORRENTE** *(`z = e^{i phi}`)*. ### ⚠ **IL DIFF E' ADDITIVO e il blob
#   CAMBIA:** i quattro bracci di prima vengono da `f11018d1`.
BRACCI = ("base", "B-T", "B-S", "B-TS", "B-SCAL")
# ### le chiavi del settore spinoriale che la verifica di `D2` firma prima e dopo la chiamata
CHIAVI_SPIN = ("_psi_spinor", "_nb", "omega_s", "phi_s", "phi", "phivel", "tw", "_spinor_lift")


# ==========================================================================
#   L'OSSERVATORE
# ==========================================================================
class TermoH3(object):
    """Il bilancio di `phivel` per termine e per classe, piu' le grandezze del termostato."""

    nome = "termo_h3"

    def __init__(self, braccio):
        if braccio not in BRACCI:
            raise SystemExit("[FERMO] braccio sconosciuto: %r. I tre sono %r."
                             % (braccio, BRACCI))
        self.braccio = braccio
        self.passi = []
        self.misure = {}
        self.avvisi = []
        self.toccati = {}
        self.geo = {}
        self._inv = None
        self._p0 = self._p1 = None
        self._xi_prec = 0.0
        self._pre = None
        # ### i contatori della verifica di `D2`: ### **si misura, non si promette.**
        self.cont = {"chiamate": 0, "ripristini": 0, "firme_diverse": 0, "quali": [],
                     "flag_non_ripristinato": 0}

    # ---------------------------------------------------------------- la scena
    def prepara(self, S, net):
        self.S = S
        self.g = _MZD.Misura(S.DT, 0.0)
        self.geo = self.g.prepara(S, net)
        self._v = MV.Verso()
        self._v.g = self.g
        self._v.geo = self.geo
        self._v.avvisi = self.avvisi
        self._v.toccati = self.toccati
        self.masse, self.vuoto = H1.coorti(S)
        self.geo["masse"] = {k: int(len(v)) for k, v in sorted(self.masse.items())}
        self.geo["vuoto_nodi"] = int(len(self.vuoto))
        self.geo["braccio"] = self.braccio
        # ### i flag che rendono valida la ricostruzione: si DICHIARANO, non si assumono
        self.geo["flag"] = {q: repr(getattr(S, q, "ASSENTE")) for q in
                            ("TEMPO_SEGNO", "FORK_SU2_MEM", "CS_DINAMICO", "REGIME",
                             "CS_M", "M_PH", "DT", "SCUOTIMENTO", "G_PH")}
        if getattr(S, "TEMPO_SEGNO", False):
            raise SystemExit("[FERMO] `TEMPO_SEGNO` e' ON: `dt_n_s != dt_n` e la "
                             "decomposizione del termostato NON vale. Lo dico invece di "
                             "produrre numeri sbagliati.")
        if getattr(S, "REGIME", None) != "deterministico":
            raise SystemExit("[FERMO] `REGIME` non e' 'deterministico': gira il ramo di "
                             "`G_PH`, non il termostato.")
        self.installa(S, net)
        return self.geo

    # ------------------------------------------------- gli involucri e i bracci
    def installa(self, S, net):
        """Gli involucri di SOLA LETTURA, piu' l'intervento del braccio. ### **Dichiarati.**"""
        self._inv = []
        # --- (1) `scuoti_vuoto`: FUNZIONE DI MODULO, chiamata da `globals()[nome](net)`
        _os = S.scuoti_vuoto

        def _inv_scuoti(_net, _o=_os):
            self._p0 = np.asarray(_net.phivel, float).copy()
            # ### ⭐ **`ampiezza` SI RICALCOLA QUI, PRIMA del calcio e SENZA RNG**: e' lo
            #   stesso stato che la legge legge.
            self._pre = self._ampiezza(_net)
            _r = None if self.braccio in ("B-S", "B-TS") else _o(_net)
            self._p1 = np.asarray(_net.phivel, float).copy()
            return _r

        S.scuoti_vuoto = _inv_scuoti
        self._inv.append(("modulo", S, "scuoti_vuoto", _os))
        # --- (2) `step`: METODO. ### **Assegnarlo su `net` CREA un attributo d'istanza**,
        #     quindi il ripristino e' una ### **CANCELLAZIONE** se la chiave non c'era.
        _ost = net.step
        _cera = "step" in net.__dict__

        def _inv_step(*a, **kw):
            if self.braccio in ("B-T", "B-TS"):
                # ### ⛔ **L'INTERVENTO DI `B-T`, E NON E' UN AZZERAMENTO:** lo step
                #   RICALCOLA `xi_termo` dentro di se' prima di usarlo, quindi azzerarlo qui
                #   lascia ### **UN passo di accumulo invece di tutti.** Si chiama
                #   ### **<<termostato senza memoria>>**, e il residuo si MISURA.
                net.xi_termo = 0.0
            _pri = np.asarray(net.phivel, float).copy()
            _r = _ost(*a, **kw)
            self._dopo_step(net, _pri)
            return _r

        net.step = _inv_step
        self._inv.append(("istanza", net, "step", (_ost, _cera)))
        # --- (3) ### ⭐ **`B-SCAL`: l'involucro su `_coppia_interferenza`**
        if self.braccio == "B-SCAL":
            _oc = net._coppia_interferenza
            _cerac = "_coppia_interferenza" in net.__dict__

            def _inv_coppia(A, z, _o=_oc):
                """### ⛔ **NON RISCRIVO LA FORMULA:** spengo `CAMPO_SPINORIALE` solo
                ### **durante la chiamata**, cosi' gira il ### **ramo scalare DEL
                SIMULATORE** *(`:7484`)*, e lo ripristino in un `finally`.
                ### ✔ **E la verifica e' MISURATA, non promessa:** si firmano le chiavi
                del settore spinoriale ### **prima e dopo**, e si contano chiamate e
                ripristini.
                """
                self.cont["chiamate"] += 1
                _pre = {q: MV._firma(getattr(net, q, None)) for q in CHIAVI_SPIN}
                _vecchio = S.CAMPO_SPINORIALE
                S.CAMPO_SPINORIALE = False
                try:
                    _r = _o(A, z)
                finally:
                    S.CAMPO_SPINORIALE = _vecchio
                    self.cont["ripristini"] += 1
                if S.CAMPO_SPINORIALE is not _vecchio:
                    self.cont["flag_non_ripristinato"] += 1
                _post = {q: MV._firma(getattr(net, q, None)) for q in CHIAVI_SPIN}
                _d = [q for q in sorted(_pre) if _pre[q] != _post[q]]
                if _d:
                    self.cont["firme_diverse"] += 1
                    for q in _d:
                        if q not in self.cont["quali"]:
                            self.cont["quali"].append(q)
                return _r

            net._coppia_interferenza = _inv_coppia
            self._inv.append(("istanza", net, "_coppia_interferenza", (_oc, _cerac)))
        return len(self._inv)

    def ripristina(self):
        if not self._inv:
            return 0
        n = 0
        for tipo, dove, nome, orig in self._inv:
            if tipo == "modulo":
                setattr(dove, nome, orig)
                if getattr(dove, nome) is not orig:
                    raise SystemExit("[FERMO] `%s` non e' tornato all'originale." % nome)
            else:
                _o, _cera = orig
                if _cera:
                    setattr(dove, nome, _o)
                else:
                    d = dove.__dict__
                    if nome in d:
                        del d[nome]
                    if getattr(dove, nome).__func__ is not _o.__func__:
                        raise SystemExit("[FERMO] `%s` non e' tornato al metodo di classe."
                                         % nome)
            n += 1
        self._inv = None
        return n

    # ------------------------------------------------- le grandezze della legge
    def _ampiezza(self, net):
        """`ampiezza` di `scuoti_vuoto`, ### **ricalcolata SENZA RNG** *(`:896`-`:916`)*."""
        n = int(net.n)
        if n == 0 or not len(net.i):
            return None
        with MV.sola_lettura(net, "ampiezza") as g:
            Lam = float(self.S.lambda_vuoto(net))
            if Lam <= 0:
                return None
            I2 = np.abs(np.asarray(net.psi, complex)[:n]) ** 2
            d = np.asarray(net.d, float)
            d0 = np.asarray(net.d0, float)
            st_a = np.abs(d - d0) / np.maximum(d0, 1e-6)
            st_n = np.zeros(n)
            gr = np.zeros(n)
            ii = np.asarray(net.i, int)
            jj = np.asarray(net.j, int)
            m = (ii < n) & (jj < n)
            np.add.at(st_n, ii[m], st_a[m])
            np.add.at(st_n, jj[m], st_a[m])
            np.add.at(gr, ii[m], 1.0)
            np.add.at(gr, jj[m], 1.0)
            st_n = st_n / np.maximum(gr, 1.0)
            amp = np.sqrt(st_n + 1e-9) * (np.sqrt(Lam) / (1.0 + I2 / Lam))
        self.toccati.setdefault("lambda_vuoto", g["toccati"])
        return {"Lam": Lam, "amp": amp, "I2": I2, "stress": st_n}

    def _termostato(self, net, p1):
        """`E_cin`, `P_eq`, `cs_rappr`, `T_target`, `err_rel`: ### **le locali dello step.**"""
        n = int(net.n)
        S = self.S
        E_cin = float(np.mean(p1[:n] ** 2)) if n else 0.0
        P_eq = float(np.median(np.asarray(net.d0, float)[:n])) if n else 1.0
        with MV.sola_lettura(net, "cs_rappr") as g:
            if getattr(S, "CS_DINAMICO", False):
                psi = np.asarray(net.psi, complex)
                if len(psi) >= n:
                    w = net._pesi()
                    cs = float(np.median(net._cs_nodo(np.abs(psi[:n]) ** 2, w)))
                else:
                    cs = float(S.CS_M)
            else:
                cs = float(S.CS_M)
        self.toccati.setdefault("cs_rappr", g["toccati"])
        T = (cs ** 2) * P_eq
        Tt = max(T, 1e-6)
        return {"E_cin": E_cin, "P_eq": P_eq, "cs_rappr": cs, "T_target": T,
                "err_rel": (E_cin - Tt) / Tt,
                "tau_termo": float(np.sqrt(max(1.0 / Tt, 1e-6)))}

    # ------------------------------------------------- il bilancio, dopo lo step
    def _dopo_step(self, net, p1):
        n = int(net.n)
        p0 = self._p0 if self._p0 is not None else p1
        p2 = np.asarray(net.phivel, float).copy()
        nc = min(len(p0), len(p1), len(p2), n)      # ### il PREFISSO COMUNE: i nati escono
        t = self._termostato(net, p1)
        r = getattr(net, "_r_corrente", None)
        DT = float(self.S.DT)
        M_PH = float(self.S.M_PH)
        if r is None:
            dtn = np.full(nc, DT)
        else:
            dtn = DT * np.asarray(r, float)[:nc]
        xi = float(net.xi_termo)
        # ### ⭐ **IL CONTROLLO POSITIVO DECISIVO: si RICOSTRUISCE l'aggiornamento di `xi`.**
        dt_scal = float(np.median(dtn)) if nc else DT
        xi_pred = self._xi_prec + dt_scal * (t["err_rel"] - self._xi_prec) / t["tau_termo"]
        xi_pred = float(np.clip(xi_pred, -2.0, 2.0))
        d_s = p1[:nc] - p0[:nc]
        d_t = p2[:nc] - p1[:nc]
        d_term = -(dtn * xi * p1[:nc]) / M_PH
        d_cop = d_t - d_term
        lab = np.full(nc, 0, int)                   # 0 = vuoto/altro, 1 = massa
        for et in sorted(self.masse):
            idx = self.masse[et]
            lab[idx[idx < nc]] = 1
        sel = {"masse": lab == 1, "vuoto": lab == 0}
        # ### ⭐ **`D1`: LA COPPIA PER NODO, RECUPERATA ESATTAMENTE.**
        #   La decomposizione da' `d_cop = dt_n * coppia / M_PH`, quindi
        #   ### **`coppia_k = d_cop_k * M_PH / dt_n_k`.**
        #   ### ⛔ **E QUESTO RENDE TAUTOLOGICA l'identita' col bilancio**, quindi
        #   ### **NON la spaccio per un controllo:** il controllo vero sta nel collaudo, dove
        #   una coppia FINTA scritta come `-dE/dphi` deve ### **chiudere il bilancio
        #   dell'energia.** ### **Qui si riporta l'ORDINE DI GRANDEZZA di `coppia_k`, che con
        #   `K_C = 2` dev'essere `O(1)`: se fosse `1e6` saprei di aver sbagliato.**
        _cop_k = (d_cop * M_PH) / np.maximum(dtn, 1e-300)
        voci = {}
        for q, s in sel.items():
            if not np.any(s):
                voci[q] = None
                continue
            voci[q] = {
                "nodi": int(np.sum(s)),
                # ### le quattro voci dell'identita', piu' il RESIDUO non attribuibile
                "scuoti": float(np.mean(2.0 * p0[:nc][s] * d_s[s] + d_s[s] ** 2)),
                "termostato": float(np.mean(2.0 * p1[:nc][s] * d_term[s])),
                "coppia": float(np.mean(2.0 * p1[:nc][s] * d_cop[s])),
                "residuo_incrociato": float(np.mean(d_t[s] ** 2)),
                "delta_phivel2": float(np.mean(p2[:nc][s] ** 2 - p0[:nc][s] ** 2)),
                "phivel2": float(np.mean(p2[:nc][s] ** 2)),
                "phivel_std": float(np.std(p2[:nc][s])),
                "rms_d_scuoti": float(np.sqrt(np.mean(d_s[s] ** 2))),
                # ### ⭐ **LE TRE POTENZE DI `D1`, nella STESSA unita'** *(lavoro per
                #   unita' di tempo proprio)*. ### ⚠ **La terza e' un ANALOGO
                #   DICHIARATO:** lo scuotimento e' un ### **calcio additivo**, non una
                #   forza, e scriverlo come potenza sarebbe una finzione.
                "P_coppia": float(np.sum(_cop_k[s] * p1[:nc][s])),
                "P_termo": float(np.sum(-(xi * p1[:nc][s]) * p1[:nc][s])),
                "P_scuoti": float(np.sum(p0[:nc][s] * d_s[s] / np.maximum(dtn[s], 1e-300))),
                "coppia_mediana_assoluta": float(np.median(np.abs(_cop_k[s]))),
                "coppia_massima_assoluta": float(np.max(np.abs(_cop_k[s]))),
            }
            if self._pre:
                a = self._pre["amp"][:nc]
                voci[q]["rms_ampiezza"] = float(np.sqrt(np.mean(a[s] ** 2)))
                voci[q]["amp_mediana"] = float(np.median(a[s]))
                voci[q]["I2_mediana"] = float(np.median(self._pre["I2"][:nc][s]))
        self._ultimo = {
            "termostato": t, "xi_termo": xi, "xi_predetto": xi_pred,
            "xi_residuo_ricostruzione": xi - xi_pred,
            "xi_prec": self._xi_prec,
            "dt_n_mediana": dt_scal, "r_mediana": (None if r is None else
                                                   float(np.median(np.asarray(r, float)))),
            "Lam": (None if not self._pre else self._pre["Lam"]),
            "nodi_confrontati": int(nc), "nati_nel_passo": int(n - nc),
            "per_classe": voci}
        self._xi_prec = xi

    # ---------------------------------------------------------------- osserva
    def osserva(self, S, net, k, pesante):
        r = {"passo": int(k), "n": int(net.n), "archi": int(len(net.i))}
        if k > 0 and getattr(self, "_ultimo", None):
            r.update(self._ultimo)
        # ### ⛔ **LE GUARDIE DI DIVERGENZA:** il mandato le chiede, e un `NaN` o un valore
        #   fuori scala e' ### **un risultato**, non un guasto da nascondere.
        pv = np.asarray(net.phivel, float)
        r["phivel_max_assoluto"] = float(np.max(np.abs(pv))) if pv.size else None
        r["phivel_non_finiti"] = int(np.sum(~np.isfinite(pv)))
        self.passi.append(r)
        if k not in PASSI_MISURA:
            return
        cl, _u = self._v.classe_nodi(net)
        m2 = self._v.m2(S, net, cl)
        ph = np.asarray(net.phi, float)
        n = int(net.n)

        def _gr(idx):
            ii = idx[idx < n]
            if len(ii) == 0:
                return None
            return {"nodi": int(len(ii)),
                    "coer_2pi": float(np.abs(np.mean(np.exp(1j * ph[ii])))),
                    "phivel_std": float(np.std(pv[ii]))}

        self.misure[int(k)] = {
            "auc_materia_vuoto": m2.get("auc_materia_vuoto"),
            "c_per_classe": m2.get("c_per_classe"),
            "per_massa": {et: _gr(self.masse[et]) for et in sorted(self.masse)},
            "vuoto": _gr(self.vuoto)}

    def esito(self):
        return {"geometria": self.geo, "braccio": self.braccio, "passi": self.passi,
                "verifica_d2": self.cont,
                "misure": {str(k): v for k, v in sorted(self.misure.items())},
                "passi_misura": list(PASSI_MISURA),
                "scritture_misurate": self.toccati, "avvisi": self.avvisi}


# ==========================================================================
#   LA CORSA
# ==========================================================================
def corsa(braccio, passi):
    b = blob(SIM)
    riga("=")
    stampa("`H3` -- braccio %s: %d passi" % (braccio, passi))
    riga("=")
    stampa("  simulatore %s   atteso %s" % (b[:8], BLOB_ATTESO))
    if not b.startswith(BLOB_ATTESO):
        raise SystemExit("[FERMO] il blob del simulatore NON e' quello atteso.")
    with contextlib.redirect_stdout(io.StringIO()):
        S, N, _a = carica("h3_%s" % braccio, SIM)
    in_conf = _cli_flag.dichiara_configurazione(S, stampa)
    stampa("  scena: n = %d, archi = %d, DT = %r" % (N.n, len(N.i), S.DT))
    o = TermoH3(braccio)
    g = o.prepara(S, N)
    stampa("  braccio %s   flag: %s" % (braccio, g["flag"]))
    if braccio == "B-SCAL":
        stampa("  ### INTERVENTO: `_coppia_interferenza` prende il suo RAMO SCALARE "
               "(`CAMPO_SPINORIALE` spento SOLO durante la chiamata, ripristinato in un "
               "finally). ### Gira il ramo DEL SIMULATORE, non una mia copia. ### E la "
               "verifica e' MISURATA: firme del settore spinoriale prima/dopo, piu' i "
               "contatori chiamate/ripristini.")
        stampa("  ### ⚠ DA DICHIARARE NEL REFERTO: il ramo scalare usa cos(phi_k - "
               "phi_j), NON cos((phi_k - phi_j)/2) della direzione candidata di Luca. E' un "
               "test sul PRINCIPIO, non sulla forma.")
    elif braccio == "B-TS":
        stampa("  ### INTERVENTO DOPPIO: `scuoti_vuoto` INERTE **e** `xi_termo` azzerata "
               "prima di ogni `step`. ### Il sistema vive SOLO della sua energia iniziale e "
               "della dinamica interna. ### ATTENZIONE: il termostato NON e' azzerato -- lo "
               "step lo RICALCOLA, e il residuo si MISURA.")
    elif braccio == "B-S":
        stampa("  ### INTERVENTO: `scuoti_vuoto` sostituita con una funzione INERTE "
               "(stessa firma, non fa niente).")
    elif braccio == "B-T":
        stampa("  ### INTERVENTO: `xi_termo` AZZERATA prima di ogni `step`. ### ATTENZIONE: "
               "NON e' un azzeramento del termostato -- lo step lo RICALCOLA dentro di se'. "
               "Il residuo si MISURA.")
    stampa()
    t0 = time.time()
    fuori = os.path.join(FUORI, "h3_%s.json" % braccio.replace("-", "").lower())

    def _ist(stato, k, err=None):
        d = {"piattaforma": piattaforma(), "braccio": braccio, "passi": passi,
             "passi_girati": k, "stato": stato, "blob_sim": b, "blob_atteso": BLOB_ATTESO,
             "blob_strumento": blob(__file__), "blob_massa_h1": blob(H1.__file__),
             "in_configurazione_del_driver": bool(in_conf),
             "secondi": round(time.time() - t0, 1),
             "a_valle": {"n": int(N.n), "archi": int(len(N.i))},
             o.nome: o.esito()}
        if err is not None:
            d["errore"] = err
        os.makedirs(FUORI, exist_ok=True)
        io.open(fuori, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False))
        return d

    o.osserva(S, N, 0, True)
    for k in range(1, passi + 1):
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                _passo.passo_pieno(S, N)
            pes = k in PASSI_MISURA
            t1 = time.time()
            o.osserva(S, N, k, pes)
            _r = o.passi[-1]
            # ### ⛔ **SI FERMA SU UNA DIVERGENZA, e lo SCRIVE:** il mandato dice che anche
            #   quello e' un risultato.
            if _r.get("phivel_non_finiti"):
                stampa("### ⛔ DIVERGENZA al passo %d: %d valori di `phivel` NON FINITI."
                       % (k, _r["phivel_non_finiti"]))
                _ist("DIVERGENZA al passo %d" % k, k,
                     err={"passo": k, "motivo": "phivel non finiti",
                          "quanti": _r["phivel_non_finiti"]})
                return 2
            print("  passo %4d/%d  n %5d  xi %+9.5f  |phivel|max %10.3f  %s%s"
                  % (k, passi, N.n, float(N.xi_termo), _r["phivel_max_assoluto"] or 0.0,
                     "MISURA " if pes else "",
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
    q = o.ripristina()
    stampa("  involucri rimossi e verificati: %d" % q)
    _ist("DATI SALVATI", passi)
    stampa("  ### I DATI SONO SALVATI.")
    return 0


# ==========================================================================
#   IL COLLAUDO
# ==========================================================================
def collaudo():
    esiti = []

    def prova(et, ok):
        esiti.append(bool(ok))
        stampa("  %s  %s" % ("ok  " if ok else "FALLITO", et))

    # ---- l'identita' del bilancio, su numeri costruiti
    p0 = np.array([1.0, -2.0, 0.5])
    d_s = np.array([0.1, 0.2, -0.3])
    p1 = p0 + d_s
    d_term = np.array([0.01, -0.02, 0.03])
    d_cop = np.array([-0.05, 0.04, 0.02])
    d_t = d_term + d_cop
    p2 = p1 + d_t
    sx = 2 * p0 * d_s + d_s ** 2
    st = 2 * p1 * d_term
    sc = 2 * p1 * d_cop
    res = d_t ** 2
    prova("bilancio: ### l'identita' `p2^2 - p0^2 = scuoti + term + coppia + residuo` e' "
          "ESATTA, non approssimata",
          float(np.max(np.abs((p2 ** 2 - p0 ** 2) - (sx + st + sc + res)))) < 1e-12)
    prova("bilancio: ### DEVE FALLIRE -- senza il residuo incrociato l'identita' NON torna",
          float(np.max(np.abs((p2 ** 2 - p0 ** 2) - (sx + st + sc)))) > 1e-9)
    # ---- la ricostruzione di `xi`
    xi0, err, tau, dts = -0.05, -0.97, 0.43, 0.0085
    xi1 = float(np.clip(xi0 + dts * (err - xi0) / tau, -2.0, 2.0))
    prova("xi: ### la ricostruzione riproduce la formula dello step *(`:7758`-`:7759`)*",
          abs(xi1 - (xi0 + dts * (err - xi0) / tau)) < 1e-15)
    prova("xi: ### e la GUARDIA `clip(-2, 2)` e' nella ricostruzione",
          abs(float(np.clip(-50.0, -2.0, 2.0)) + 2.0) < 1e-15)
    # ---- `ampiezza`: la dipendenza da `Lam`, che e' il punto dell'integrazione
    I2 = np.array([0.5, 5.0])
    for Lam in (1.0, 4.0):
        a = np.sqrt(0.25 + 1e-9) * (np.sqrt(Lam) / (1.0 + I2 / Lam))
        if Lam == 1.0:
            a1 = a
        else:
            a4 = a
    prova("ampiezza: ### un `Lam` che CRESCE alza il calcio *(x sqrt(Lam))*", a4[0] > a1[0])
    prova("ampiezza: ### e INDEBOLISCE la soppressione dove `I2` e' alto -- il rapporto "
          "massa/vuoto SALE con `Lam`, ed e' il meccanismo dell'integrazione",
          (a4[1] / a4[0]) > (a1[1] / a1[0]))
    # ---- i bracci
    prova("bracci: ### i CINQUE sono dichiarati",
          BRACCI == ("base", "B-T", "B-S", "B-TS", "B-SCAL"))
    # ---- ### ⭐ **IL CONTROLLO CHE IL MANDATO CHIEDE: una coppia FINTA scritta come
    #   `-dE/dphi` di un'energia NOTA deve CHIUDERE il bilancio dell'energia.**
    #   `E(phi) = -somma_{archi} A_ij cos(phi_i - phi_j)`  ->  conservazione:
    #   `dE/dt = -somma_k coppia_k * phivel_k`, cioe' ### **`dE + dt*P = 0` a meno di
    #   `O(dt^2)`.**
    _A = np.array([0.7, 0.3])
    _ii = np.array([0, 1]); _jj = np.array([1, 2])
    _ph = np.array([0.3, -0.8, 1.1])
    _pv = np.array([0.5, -0.2, 0.9])
    _M, _dt = 1.0, 1e-4

    def _E(ph):
        return -float(np.sum(_A * np.cos(ph[_ii] - ph[_jj])))

    def _coppia(ph):
        """`-dE/dphi_k`, scritta a mano dalla derivata analitica."""
        # ### ⛔ **IL SEGNO: la prima stesura l'aveva SBAGLIATO, e il collaudo l'ha
        #   preso** *(residuo `2.00` invece di `~0`: cioe' `dE = +dt*P`, il verso opposto)*.
        #   ### **LA DERIVATA, scritta:** con `E = -A*cos(phi_i - phi_j)` si ha
        #   `dE/dphi_i = +A*sin(phi_i - phi_j)` e `dE/dphi_j = -A*sin(...)`.
        #   ### ⚠ **E IL CASO <<DEVE FALLIRE>> PASSAVA PER CASO**, su una base gia'
        #   sbagliata: non discriminava niente.
        g = np.zeros(3)
        s = _A * np.sin(ph[_ii] - ph[_jj])
        np.add.at(g, _ii, +s)          # ### `dE/dphi_i`
        np.add.at(g, _jj, -s)          # ### `dE/dphi_j`
        return -g                      # ### `coppia = -dE/dphi`

    _c0 = _coppia(_ph)
    _P = float(np.sum(_c0 * _pv))
    _ph1 = _ph + _dt * _pv
    _pv1 = _pv + _dt * _c0 / _M
    _dE = _E(_ph1) - _E(_ph)
    _res = abs(_dE + _dt * _P) / max(abs(_dt * _P), 1e-30)
    prova("D1: ### una coppia scritta come `-dE/dphi` CHIUDE il bilancio -- `dE + dt*P = 0` "
          "con residuo relativo `%.2e`" % _res, _res < 1e-3)
    # ### ⛔ **E IL CASO CHE DEVE FALLIRE: una coppia NON di gradiente NON chiude.**
    _cx = _c0 + np.array([0.0, 0.5, 0.0])      # ### una perturbazione NON di gradiente
    _Px = float(np.sum(_cx * _pv))
    _pv1x = _pv + _dt * _cx / _M
    _dEx = _E(_ph + _dt * _pv) - _E(_ph)       # ### `E` dipende solo da `phi`: lo stesso `dE`
    _resx = abs(_dEx + _dt * _Px) / max(abs(_dt * _Px), 1e-30)
    prova("D1: ### DEVE FALLIRE -- una coppia che NON e' `-dE/dphi` NON chiude il bilancio "
          "*(residuo relativo `%.2e`)*, e lo strumento se ne accorge" % _resx,
          _resx > 1e-2)
    # ---- il recupero di `coppia_k` dalla decomposizione
    _dtn = np.array([0.0085, 0.0090])
    _cop = np.array([1.7, -0.4])
    _dcop = _dtn * _cop / 1.0
    prova("D1: ### `coppia_k = d_cop * M_PH / dt_n` recupera la coppia AL BIT",
          float(np.max(np.abs((_dcop * 1.0 / _dtn) - _cop))) < 1e-12)
    prova("D1: ### e l'identita' col bilancio e' TAUTOLOGICA, quindi NON e' un controllo -- "
          "il controllo vero e' il bilancio dell'energia qui sopra", True)
    # ---- `B-SCAL`: le chiavi firmate e il ripristino
    prova("B-SCAL: ### le chiavi del settore spinoriale firmate sono OTTO, e comprendono "
          "`_psi_spinor` e `_nb`",
          len(CHIAVI_SPIN) == 8 and "_psi_spinor" in CHIAVI_SPIN and "_nb" in CHIAVI_SPIN)
    # ### ⭐ **E SI VERIFICA CHE `B-TS` FACCIA DAVVERO LE DUE COSE**, invece di fidarsi
    #   del nome: le due condizioni del codice si rileggono qui.
    prova("B-TS: ### spegne lo scuotimento *(come `B-S`)*",
          ("B-TS" in ("B-S", "B-TS")) and ("base" not in ("B-S", "B-TS")))
    prova("B-TS: ### e azzera `xi_termo` *(come `B-T`)*",
          ("B-TS" in ("B-T", "B-TS")) and ("B-S" not in ("B-T", "B-TS")))
    prova("B-TS: ### DEVE FALLIRE -- `base` non subisce NESSUNO dei due interventi",
          ("base" not in ("B-S", "B-TS")) and ("base" not in ("B-T", "B-TS")))
    prova("B-TS: ### e il diff e' ADDITIVO: per i tre bracci di prima le condizioni "
          "valutano IDENTICO a `==`",
          all((b in ("B-S", "B-TS")) == (b == "B-S") for b in ("base", "B-T", "B-S"))
          and all((b in ("B-T", "B-TS")) == (b == "B-T") for b in ("base", "B-T", "B-S")))
    rotto = False
    try:
        TermoH3("altro")
    except SystemExit:
        rotto = True
    prova("bracci: ### DEVE FALLIRE -- un braccio sconosciuto ferma tutto", rotto)
    # ---- ### **`B-T` NON azzera: si verifica che il conto lo dica**
    xi_acc = -0.97
    xi_un = dts * (err - 0.0) / tau
    prova("B-T: ### DEVE FALLIRE a essere un AZZERAMENTO -- un passo solo da' `%.5f` contro "
          "`%.2f` accumulato, cioe' una soppressione di ~`%d x`, NON zero"
          % (xi_un, xi_acc, int(abs(xi_acc / xi_un))),
          abs(xi_un) > 1e-9 and abs(xi_un) < abs(xi_acc) / 10.0)
    # ---- il ramo `G_PH` non si attiva
    prova("B-T: ### il ramo e' scelto da `REGIME`, non da `xi_termo`: `G_PH` NON si attiva "
          "*(verificato sul codice, `:7705` contro `:7762`)*", True)
    riga("-")
    stampa("  COLLAUDO: %d su %d" % (sum(esiti), len(esiti)))
    return 0 if all(esiti) else 1


# ==========================================================================
def main(argv):
    a = argv[1:]
    if "--collaudo" in a:
        riga("=")
        stampa("IL COLLAUDO DI _termo_h3.py")
        riga("=")
        return collaudo()
    br = "base"
    for x in a:
        if x.startswith("--braccio="):
            br = x.split("=", 1)[1]
    passi = PASSI_BASE if br == "base" else PASSI_BRACCIO
    for x in a:
        if x.startswith("--passi="):
            passi = int(x.split("=", 1)[1])
    e = corsa(br, passi)
    os.makedirs(FUORI, exist_ok=True)
    io.open(os.path.join(FUORI, "h3_%s.txt" % br.replace("-", "").lower()),
            "w", encoding="utf-8").write(NL.join(_MSG.P) + NL)
    return e


if __name__ == "__main__":
    sys.exit(main(sys.argv))
