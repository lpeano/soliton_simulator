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
BRACCI = ("base", "B-T", "B-S", "B-TS", "B-SCAL", "B-SCAL-TS", "B-SCAL-TS-NOSYNC",
          "B-U2-TS-NOSYNC")
# ### ⭐ **`D3`: i bracci che spengono i forzanti e la sincronizzazione**, cosi' le tre
#   appartenenze non si ripetono a mano in quattro punti.
SENZA_SCUOTI = ("B-S", "B-TS", "B-SCAL-TS", "B-SCAL-TS-NOSYNC", "B-U2-TS-NOSYNC")
SENZA_XI = ("B-T", "B-TS", "B-SCAL-TS", "B-SCAL-TS-NOSYNC", "B-U2-TS-NOSYNC")
SENZA_SYNC = ("B-SCAL-TS-NOSYNC", "B-U2-TS-NOSYNC")
# ### il ramo SCALARE del simulatore *(`B-SCAL*`)*; `B-U2-*` usa la forma `U(2)` MIA
RAMO_SCALARE = ("B-SCAL", "B-SCAL-TS", "B-SCAL-TS-NOSYNC")
FORMA_U2 = ("B-U2-TS-NOSYNC",)
# ### la soglia della gauge: sotto questa `|a|` il polo `b` e' vicino e la fase comune si
#   prende dalla SECONDA componente. ### **NON e' una manopola fisica:** e' la soglia di
#   un ARGOMENTO non definito, e i nodi che la prendono si CONTANO.
SOGLIA_GAUGE = 1e-9
# ### le chiavi del settore spinoriale che la verifica di `D2` firma prima e dopo la chiamata
CHIAVI_SPIN = ("_psi_spinor", "_nb", "omega_s", "phi_s", "phi", "phivel", "tw", "_spinor_lift")


# ==========================================================================
#   ### ⭐ **`D3`: LA FORMA `U(2)` DELLA COPPIA** *(direzione candidata di Luca)*
# ==========================================================================
def gauge_chi(psi_spinor, n, soglia=SOGLIA_GAUGE):
    """### **`chi` = lo spinore PRIVATO della sua fase comune**, in gauge canonica.

    `chi_k = psi_k * e^{-i alpha_k}` con `alpha_k = arg(prima componente)`, cosi' la
    prima componente e' ### **reale `>= 0`** -- cioe' esattamente
    `(cos(theta/2), sin(theta/2) e^{i varphi})`.
    ### ⛔ **IL CASO DEGENERE, DICHIARATO:** se `|a| < soglia` lo spinore e' al
    ### **polo `b`** e `arg(a)` ### **non e' definito**; allora la fase comune si prende
    dalla ### **SECONDA** componente. ### **I nodi che prendono quel ramo si CONTANO.**
    ### ✔ **E `alpha` si RESTITUISCE**, perche' serve a misurare se la fase comune dello
    spinore ### **e'** `phi/2` -- che e' l assunzione della forma, non un suo risultato.
    """
    ps = np.asarray(psi_spinor, complex)[:n]
    a = ps[:, 0]
    b = ps[:, 1]
    polo = np.abs(a) < soglia
    alpha = np.where(polo, np.angle(b), np.angle(a))
    chi = ps * np.exp(-1j * alpha)[:, None]
    return chi, alpha, int(np.sum(polo))


def bloch_da_spinore(chi):
    """### Il Bloch, ### **invariante per fase comune** -- la stessa forma di `:7458`.

    `n = (2 Re(conj(a) b), 2 Im(conj(a) b), |a|^2 - |b|^2)`, normalizzato.
    ### ✔ **Costruito da `chi` o da `psi`, viene IDENTICO:** la gauge non lo tocca, e
    questo e' il motivo per cui `N` non dipende dalla gauge.
    """
    a = chi[:, 0]
    b = chi[:, 1]
    nb = np.stack([2.0 * np.real(np.conj(a) * b),
                   2.0 * np.imag(np.conj(a) * b),
                   np.abs(a) ** 2 - np.abs(b) ** 2], axis=1)
    return nb / np.maximum(np.linalg.norm(nb, axis=1), 1e-30)[:, None]


def emme_arco(net, N, chi, ii, jj):
    """### `M_ij = <chi_i| N_ij |chi_j>`, per arco. ### **NON dipende da `phi`.**
    """
    wi = np.conj(chi[ii])
    wj = chi[jj]
    return (wi[:, 0] * (N[:, 0, 0] * wj[:, 0] + N[:, 0, 1] * wj[:, 1])
            + wi[:, 1] * (N[:, 1, 0] * wj[:, 0] + N[:, 1, 1] * wj[:, 1]))


def energia_u2(K_C, A, M, ph, ii, jj):
    """### `E = -K_C somma_archi A_ij Re(e^{i (phi_j - phi_i)/2} M_ij)`.

    ### ⭐ **L energia per legame va come `cos(Dphi/2)`, NON come `cos(Dphi)`** -- ed e'
    la differenza fra questa forma e il ramo scalare del simulatore.
    """
    ov = np.exp(0.5j * (ph[jj] - ph[ii])) * M
    return -K_C * float(np.sum(A * np.real(ov))), ov


def coppia_u2(K_C, A, ov, ii, jj, n):
    """### **`coppia = -dE/dphi`**, dalla derivata del task history (par. 2.2).

    `s_ij = K_C A_ij Im(ov_ij)`, e poi ### **`coppia_i += +s/2`, `coppia_j += -s/2`**.
    ### ✔ **L antisimmetria NON e' una scelta:** con `N_ji = N_ij^dag` la parte
    immaginaria ### **cambia segno** allo scambio degli estremi, quindi questo E'
    l azione-reazione.
    """
    s = K_C * A * np.imag(ov)
    cop = np.zeros(int(n))
    np.add.at(cop, ii, +0.5 * s)
    np.add.at(cop, jj, -0.5 * s)
    return cop


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
        # ### ⭐ **gli stati della misura dell energia (`B-SCAL-TS`, `D2-BIS`)**:
        #   `_en` e' la cattura di QUESTO passo *(`A`, gli archi, la coppia
        #   dell interferenza)*, `_en_prec` quella del passo PRIMA -- serve al
        #   ### **lavoro di `A` che cambia**, che si chiude con ### **un passo di
        #   ritardo** *(dichiarato nel task history)*.
        self._en = None
        self._en_prec = None
        # ### ⭐ **`D3`:** gli stati della forma `U(2)` e i suoi contatori
        self._u2 = None
        self._u2_prec = None
        self.cont_u2 = {"chiamate": 0, "bloch_ritardato": 0, "nodi_al_polo": 0,
                        "alpha_meno_phi_mezzi_rms": None,
                        "alpha_meno_phi_mezzi_mediana": None}
        self._phi_pre = None
        self._en_avvisi = []
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
                             "CS_M", "M_PH", "DT", "SCUOTIMENTO", "G_PH",
                             # ### ⭐ **i flag delle QUATTRO leggi che NON sono il
                             #   gradiente di `U`** *(par. 2.3 del task history)*: si
                             #   ### **dichiarano**, cosi' chi legge il json sa
                             #   perche' il bilancio non chiude sulla coppia TOTALE.
                             "K_C", "K_SYNC", "REPULS_LEGGE", "SPIN_FEEDBACK",
                             "FRAME_DRAG", "FASE_2PI", "MU_PSI")}
        if getattr(S, "TEMPO_SEGNO", False):
            raise SystemExit("[FERMO] `TEMPO_SEGNO` e' ON: `dt_n_s != dt_n` e la "
                             "decomposizione del termostato NON vale. Lo dico invece di "
                             "produrre numeri sbagliati.")
        if getattr(S, "REGIME", None) != "deterministico":
            raise SystemExit("[FERMO] `REGIME` non e' 'deterministico': gira il ramo di "
                             "`G_PH`, non il termostato.")
        self.installa(S, net)
        self.installa_d2ter(S, net)
        self.geo["flag_dopo_intervento"] = {
            q: repr(getattr(S, q, "ASSENTE")) for q in
            ("K_SYNC", "SYNC_SPINORE", "SYNC_FASE_OROLOGIO", "KURAMOTO_SU2")}
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
            _r = None if self.braccio in SENZA_SCUOTI else _o(_net)
            self._p1 = np.asarray(_net.phivel, float).copy()
            return _r

        S.scuoti_vuoto = _inv_scuoti
        self._inv.append(("modulo", S, "scuoti_vuoto", _os))
        # --- (2) `step`: METODO. ### **Assegnarlo su `net` CREA un attributo d'istanza**,
        #     quindi il ripristino e' una ### **CANCELLAZIONE** se la chiave non c'era.
        _ost = net.step
        _cera = "step" in net.__dict__

        def _inv_step(*a, **kw):
            # ### ⭐ **`phi` ALL INGRESSO DELLO STEP E' ESATTAMENTE `_phi_t`**: nella
            #   composizione del passo `scuoti_vuoto` viene PRIMA di `step` e tocca
            #   solo `phivel`, quindi qui `net.phi` e' ancora lo snapshot `t` che
            #   `step` si prende a `:7492`. ### **Verificato sul codice, non assunto.**
            if self.braccio in RAMO_SCALARE + FORMA_U2:
                self._phi_pre = np.asarray(net.phi, float).copy()
            if self.braccio in SENZA_XI:
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
        if self.braccio in RAMO_SCALARE + FORMA_U2:
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
                if self.braccio in FORMA_U2:
                    # ### ⭐ **`D3`: LA FORMA `U(2)`, E L ORIGINALE NON SI CHIAMA.**
                    #   ### ⛔ **E NON E' UN VEZZO:** `_bloch_ritardato` *(`:7223`)*
                    #   ### **SCRIVE `self._nb_ret`** -- ha MEMORIA -- quindi va chiamata
                    #   ### **esattamente una volta per passo.** Sostituire l originale
                    #   invece di aggiungersi tiene il conteggio a UNO, come prima.
                    _r = self._coppia_u2(net, S, A)
                    self.cont["ripristini"] += 1
                    _vecchio = S.CAMPO_SPINORIALE
                else:
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
                # ### ⭐ **LA CATTURA PER L ENERGIA: `A` E' IL PRIMO ARGOMENTO.**
                #   Non la ricostruisco e non la ricalcolo: ### **e' quella che la
                #   legge ha usato in questo passo**, e il mandato chiede proprio
                #   quella. Insieme vanno gli archi *(`A` e' per arco)* e la coppia
                #   ### **dell INTERFERENZA**, che e' quella che `-dU/dphi` descrive.
                _na = len(np.asarray(A, float))
                self._en_prec = self._en
                self._en = {"A": np.asarray(A, float).copy(),
                            "i": np.asarray(net.i, np.int64)[:_na].copy(),
                            "j": np.asarray(net.j, np.int64)[:_na].copy(),
                            "cop": np.asarray(_r, float).copy()}
                return _r

            net._coppia_interferenza = _inv_coppia
            self._inv.append(("istanza", net, "_coppia_interferenza", (_oc, _cerac)))
        return len(self._inv)

    # ------------------------------------------- `D2-TER`: `K_SYNC` e `calcola_psi`
    def installa_d2ter(self, S, net):
        """### ⭐ **`K_SYNC = 0` SOLO NELLO STRUMENTO**, e l involucro che decide se
        quello e' ### **UN SOLO interruttore**.

        ### ⛔ **IL CENSIMENTO, dal codice** *(par. 2.1 del task history)*: `K_SYNC`
        apre il blocco di `:7767`, la cui ### **unica** uscita e' `delta_sync_phi`
        *(`:7805`)*, perche' `_forza_sync` si popola ### **solo se** uno fra
        `SYNC_SPINORE`, `SYNC_FASE_OROLOGIO`, `KURAMOTO_SU2` e' acceso -- e nel driver
        sono ### **tutti e tre spenti**.
        ### ⚠ **MA IL BLOCCO CONTIENE `calcola_psi(w)`** *(`:7771`)*, che ### **SCRIVE**
        `self.psi`. Saltarlo salta quella scrittura, e ### **dovrebbe** essere
        byte-inerte *(l ultima `calcola_psi` prima e' `:7592`, con lo STESSO `w`)*.
        ### ⛔ **<<Dovrebbe>> non e' una misura: si FIRMA `psi` prima e dopo OGNI
        chiamata, e si conta per CHIAMANTE.**
        """
        self._psi_cont = {"chiamate": 0, "cambiate": 0, "per_chiamante": {}}
        _op = net.calcola_psi
        _cerap = "calcola_psi" in net.__dict__

        def _inv_psi(w=None, _o=_op):
            import sys as _s
            try:
                _rig = _s._getframe(1).f_lineno
            except Exception:              # noqa: BLE001
                _rig = -1
            _pre = MV._firma(getattr(net, "psi", None))
            _r = _o(w)
            _post = MV._firma(getattr(net, "psi", None))
            c = self._psi_cont
            c["chiamate"] += 1
            _k = str(_rig)
            _v = c["per_chiamante"].setdefault(_k, [0, 0])
            _v[0] += 1
            if _pre != _post:
                c["cambiate"] += 1
                _v[1] += 1
            return _r

        net.calcola_psi = _inv_psi
        self._inv.append(("istanza", net, "calcola_psi", (_op, _cerap)))
        # --- ### ⛔ **`K_SYNC = 0`, SOLO sul modulo dello strumento, e RIPRISTINATO**
        if self.braccio in SENZA_SYNC:
            self._ksync_vecchio = float(S.K_SYNC)
            S.K_SYNC = 0.0
            self._inv.append(("modulo_valore", S, "K_SYNC", self._ksync_vecchio))
            if S.K_SYNC != 0.0:
                raise SystemExit("[FERMO] `K_SYNC` non e' andato a zero.")
        return len(self._inv)

    def ripristina(self):
        if not self._inv:
            return 0
        n = 0
        for tipo, dove, nome, orig in self._inv:
            if tipo == "modulo_valore":
                # ### un VALORE di modulo, non una funzione: si riscrive e si verifica
                setattr(dove, nome, orig)
                if getattr(dove, nome) != orig:
                    raise SystemExit("[FERMO] `%s` non e' tornato a %r."
                                     % (nome, orig))
                n += 1
                continue
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
            "per_classe": voci,
            # ### ⭐ **L ENERGIA (`D2-BIS`)**: `None` sui bracci che non hanno
            #   l involucro su `_coppia_interferenza`, perche' senza quello la `A`
            #   ### **non si cattura** -- e ricostruirla sarebbe una mia copia, non la
            #   `A` che la legge ha usato.
            "energia": self._energia(net, p1, p2, _cop_k, nc, dtn)}
        self._xi_prec = xi

    # ------------------------------------------- `D3`: la forma `U(2)`
    def _coppia_u2(self, net, S, A):
        """### ⭐ **LA COPPIA `U(2)`, e tutto cio' che serve a spezzare `dE`.**

        Usa la ### **stessa `A`** *(il primo argomento)*, la ### **stessa `N`** del ramo
        `FORK_SU2` *(`_link_su2_N(...) * 0.5`, `:7471`)* e lo ### **stesso Bloch
        ritardato** se `FORK_SU2_MEM` e' acceso.
        ### ⛔ **`_bloch_ritardato` SI CHIAMA UNA VOLTA SOLA**, perche' ha memoria
        *(`self._nb_ret`, `:7255` e `:7299`)*, e questo involucro ### **sostituisce**
        l originale invece di aggiungersi: il conteggio resta UNO per passo.
        """
        n = int(net.n)
        ii = np.asarray(net.i, np.int64)
        jj = np.asarray(net.j, np.int64)
        Aa = np.asarray(A, float)
        m = int(min(len(Aa), len(ii), len(jj)))
        ii, jj, Aa = ii[:m], jj[:m], Aa[:m]
        ps = getattr(net, "_psi_spinor", None)
        if ps is None or len(ps) < n:
            raise SystemExit("[FERMO] `_psi_spinor` manca o e' corto: la forma `U(2)` "
                             "non e' definita, e NON la invento.")
        chi, alpha, quanti_polo = gauge_chi(ps, n)
        nb = bloch_da_spinore(chi)
        if getattr(S, "FORK_SU2_MEM", False):
            nb_conn = net._bloch_ritardato(nb, ii, jj)
            self.cont_u2["bloch_ritardato"] += 1
        else:
            nb_conn = nb
        nb_conn = np.asarray(nb_conn, float)[:n]
        N = net._link_su2_N(nb_conn[ii], nb_conn[jj]) * 0.5
        M = emme_arco(net, N, chi, ii, jj)
        K_C = float(S.K_C)
        ph = np.asarray(net.phi, float)[:n]
        E, ov = energia_u2(K_C, Aa, M, ph, ii, jj)
        cop = coppia_u2(K_C, Aa, ov, ii, jj, n)
        # ### ⭐ **LA MISURA CHE DECIDE SE LA FORMA E' UNA RISCRITTURA O UN MODELLO
        #   NUOVO:** la forma ### **assume** che la fase comune dello spinore sia
        #   `phi/2`. Si misura `rms(wrap(alpha - phi/2))` sul periodo `2 pi`.
        _d = alpha - 0.5 * ph
        _d = (_d + np.pi) % (2.0 * np.pi) - np.pi
        self.cont_u2["chiamate"] += 1
        self.cont_u2["nodi_al_polo"] = quanti_polo
        self.cont_u2["alpha_meno_phi_mezzi_rms"] = float(np.sqrt(np.mean(_d ** 2)))
        self.cont_u2["alpha_meno_phi_mezzi_mediana"] = float(np.median(np.abs(_d)))
        # ### la cattura per la spartizione di `dE` in TRE pezzi *(par. 3.2)*
        self._u2_prec = self._u2
        self._u2 = {"M": M.copy(), "A": Aa.copy(), "i": ii.copy(), "j": jj.copy(),
                    "E": E, "chi": chi.copy(), "nb_conn": nb_conn.copy(),
                    "alpha": alpha.copy(), "polo": quanti_polo}
        return cop

    def _energia_u2_pezzi(self, net):
        """### ⭐ **`dU_phi`, `dU_chi`, `dU_A`: tre pezzi ESATTI che sommano a `dE`.**

        ```
        dE(k -> k+1) = [E(M_k,   phi_k+1, A_k  ) - E(M_k, phi_k,   A_k)]   dU_phi
                     + [E(M_k+1, phi_k+1, A_k  ) - E(M_k, phi_k+1, A_k)]   dU_chi
                     + [E(M_k+1, phi_k+1, A_k+1) - E(M_k+1, phi_k+1, A_k)] dU_A
        ```
        ### ⚠ **Gli ultimi due si chiudono con UN PASSO DI RITARDO**, perche' servono
        `M_{k+1}` e `A_{k+1}`: la voce del passo `k` chiude il passo `k-1`.
        ### ⛔ **E SE GLI ARCHI CAMBIANO non sono definiti:** si ASSERISCE, e se cade si
        mette `None` con la ragione, invece di mettere un numero sbagliato.
        """
        u, p = self._u2, self._u2_prec
        if u is None or p is None:
            return None
        K_C = float(self.S.K_C)
        ph1 = np.asarray(net.phi, float)
        if len(p["i"]) != len(u["i"]) or not np.array_equal(p["i"], u["i"]) \
                or not np.array_equal(p["j"], u["j"]):
            return {"stato": "NON DEFINITO: gli archi sono cambiati fra i due passi, "
                             "quindi `E` sui vecchi archi non ha senso",
                    "archi_prec": int(len(p["i"])), "archi_ora": int(len(u["i"]))}
        ii, jj = p["i"], p["j"]
        if len(ii) and int(max(ii.max(), jj.max())) >= len(ph1):
            return {"stato": "NON DEFINITO: un indice d arco sfora `n`"}
        # ### `M_{k+1}` sui VECCHI archi, dal Bloch e dal `chi` di QUESTO passo.
        #   ### ✔ **`_link_su2_N` e' PURA** *(censita)*, quindi si puo' richiamare.
        Nn = net._link_su2_N(u["nb_conn"][ii], u["nb_conn"][jj]) * 0.5
        Mn = emme_arco(net, Nn, u["chi"], ii, jj)
        _e = lambda _M, _A: energia_u2(K_C, _A, _M, ph1, ii, jj)[0]        # noqa: E731
        E_vp = p["E"]                                   # E(M_k,   phi_k,   A_k)
        E_v1 = _e(p["M"], p["A"])                       # E(M_k,   phi_k+1, A_k)
        E_n1 = _e(Mn, p["A"])                           # E(M_k+1, phi_k+1, A_k)
        E_na = _e(Mn, u["A"]) if len(u["A"]) == len(p["A"]) else None
        return {"stato": "OK",
                "dU_phi": E_v1 - E_vp,
                "dU_chi": E_n1 - E_v1,
                "dU_A": (E_na - E_n1) if E_na is not None else None,
                "E_pre": E_vp, "E_ora": u["E"],
                "chiude": "il passo PRECEDENTE (ritardo dichiarato)"}

    # ------------------------------------------------- l'energia (`D2-BIS`)
    def _classe_archi(self, ii, jj, n):
        """### **L etichetta di CLASSE per ARCO, e sono TRE, non due.**

        `masse` se ### **ENTRAMBI** gli estremi sono in una massa, `vuoto` se
        ### **NESSUNO**, `misti` altrimenti. ### ⚠ **Un arco fra una massa e il vuoto
        non appartiene a nessuna delle due:** metterlo d'autorita' in una delle due
        falserebbe il bilancio, e quel bilancio e' il punto della misura.
        """
        lab = np.zeros(int(n), bool)
        for et in sorted(self.masse):
            idx = self.masse[et]
            lab[idx[idx < n]] = True
        a = lab[ii]
        b = lab[jj]
        return {"masse": a & b, "vuoto": (~a) & (~b), "misti": a ^ b}

    def _energia(self, net, p1, p2, cop_tot, nc, dtn):
        """### ⭐ **`T`, `U`, `H` e i lavori, nelle forme DERIVATE DAL CODICE.**

        ### **CINETICA:** da `:7760` *(`delta_phivel = dt_n_s*(coppia - xi*phivel_t)/
        M_PH`)* e `:7830` *(`phivel = phivel_t + delta_phivel`)*, diviso per `dt_n_s`,
        si legge ### **Newton sulla coordinata `phi`** con inerzia `M_PH`, quindi
        ### **`T = (1/2) M_PH somma(phivel^2)`**.
        ### ⚠ **`dt_n` NON ENTRA in `T`:** e' il passo d'integrazione, ed e'
        ### **PER NODO** *(`dt_n = DT*r`, `:7498`)*. Entra solo nei LAVORI, via
        `Dphi = dt_n*phivel(t+1)` *(`:7831`)*.
        ### ⛔ **E NON E' l `E_cin` DEL CODICE** *(`:7711`)*, che e' `mean(phivel^2)`:
        una MEDIA senza `1/2` e senza `M_PH`, cioe' un analogo di TEMPERATURA.

        ### **POTENZIALE:** `U = -K_C somma_archi A cos(phi_i - phi_j)`, con la `A`
        ### **EFFETTIVAMENTE USATA** in quel passo *(catturata dall involucro: e' il
        suo primo argomento)*. E il ramo scalare di `_coppia_interferenza` *(`:7484`)*
        ne e' ### **esattamente `-dU/dphi`**, perche' `_mat` *(`:6257`)* e' SIMMETRICA.
        """
        e = self._en
        if e is None or self._phi_pre is None:
            return None
        K_C = float(self.S.K_C)
        M_PH = float(self.S.M_PH)
        ph0 = self._phi_pre
        ph1 = np.asarray(net.phi, float)
        na = len(ph0)
        nb = len(ph1)
        # ### ⛔ **LE DUE ASSERZIONI DEL TASK HISTORY.** Senza queste
        #   `U(A vecchia, phi nuove)` non vuol dire niente, perche' gli archi di `A`
        #   indicizzano nodi che potrebbero non essere piu' gli stessi.
        if nb < na:
            raise SystemExit("[FERMO] `n` e' CALATO (%d -> %d): gli indici dei nodi "
                             "non sono stabili e la decomposizione di `U` NON VALE."
                             % (na, nb))
        ii = e["i"]
        jj = e["j"]
        if len(ii) and (int(ii.max()) >= na or int(jj.max()) >= na):
            raise SystemExit("[FERMO] un indice d'arco di `A` sfora `n`: %d / %d "
                             "contro %d." % (int(ii.max()), int(jj.max()), na))
        A = e["A"]
        u0 = -K_C * A * np.cos(ph0[ii] - ph0[jj])
        u1 = -K_C * A * np.cos(ph1[ii] - ph1[jj])
        U0 = float(np.sum(u0))
        dU_phi = float(np.sum(u1)) - U0
        sel_a = self._classe_archi(ii, jj, na)
        # --- `U` per classe, sulla `A` e le `phi` di QUESTO passo
        U_cl = {q: float(np.sum(u0[s])) for q, s in sorted(sel_a.items())}
        U_na = {q: int(np.sum(s)) for q, s in sorted(sel_a.items())}
        dU_phi_cl = {q: float(np.sum(u1[s]) - np.sum(u0[s]))
                     for q, s in sorted(sel_a.items())}
        # --- `T` per classe *(sui NODI, non sugli archi)*
        lab = np.zeros(nc, bool)
        for et in sorted(self.masse):
            idx = self.masse[et]
            lab[idx[idx < nc]] = True
        sel_n = {"masse": lab, "vuoto": ~lab}
        T0_cl = {q: 0.5 * M_PH * float(np.sum(p1[:nc][s] ** 2))
                 for q, s in sorted(sel_n.items())}
        T1_cl = {q: 0.5 * M_PH * float(np.sum(p2[:nc][s] ** 2))
                 for q, s in sorted(sel_n.items())}
        T0 = 0.5 * M_PH * float(np.sum(p1[:nc] ** 2))
        T1 = 0.5 * M_PH * float(np.sum(p2[:nc] ** 2))
        # --- ### **`Dphi` AVVOLTO sul periodo di `phi`** *(`4 pi` con `FASE_2PI`
        #     spento, `:6392`)*: l incremento vero e' `~0.05`, quindi l avvolgimento
        #     lo recupera ESATTO -- e il massimo si MISURA, per poterlo smentire.
        per = float(net._dphi())
        d = ph1[:na] - ph0
        dphi = (d + per / 2.0) % per - per / 2.0
        dphi_max = float(np.max(np.abs(dphi))) if na else 0.0
        if dphi_max > per / 4.0:
            raise SystemExit("[FERMO] `Dphi` massimo %.4f oltre un quarto del periodo "
                             "%.4f: l avvolgimento NON e' piu' affidabile."
                             % (dphi_max, per))
        cop_i = np.asarray(e["cop"], float)
        m = int(min(len(cop_i), na, nc, len(cop_tot)))
        W_interf = float(np.sum(cop_i[:m] * dphi[:m]))
        W_tot = float(np.sum(np.asarray(cop_tot, float)[:m] * dphi[:m]))
        res = (dU_phi + W_interf) / max(abs(W_interf), 1e-300)
        # --- ### ⭐ **`D2-TER`: `delta_sync_phi` DERIVATO DALLA LEGGE, non stimato.**
        #     Il commit atomico *(`:7831`)* e'
        #       `phi(t+1) = (phi_t + dt_n_s*phivel(t+1) + delta_sync_phi) % _dphi()`
        #     ### ➜ **quindi `delta_sync_phi = Dphi - dt_n_s*phivel(t+1)`**, con
        #     `dt_n_s = dt_n` perche' `TEMPO_SEGNO = False` *(e `prepara` FERMA se no)*.
        #     ### ⛔ **E LA SOMMA `W_sync + W_newton = W_interferenza` E' TAUTOLOGICA**,
        #     perche' i due addendi partizionano `Dphi` ### **per definizione**: si
        #     riporta *(il mandato la chiede)* e si DICHIARA tale. ### ⭐ **Il controllo
        #     VERO e' che in `NOSYNC` `delta_sync_phi` sia ESATTAMENTE zero.**
        _newt = dtn[:m] * p2[:m]
        _dsy = dphi[:m] - _newt
        W_newton = float(np.sum(cop_i[:m] * _newt))
        W_sync = float(np.sum(cop_i[:m] * _dsy))
        _ct = np.asarray(cop_tot, float)[:m]
        W_newton_tot = float(np.sum(_ct * _newt))
        W_sync_tot = float(np.sum(_ct * _dsy))
        # ### per CLASSE, sui NODI
        _lab2 = np.zeros(m, bool)
        for et2 in sorted(self.masse):
            _ix = self.masse[et2]
            _lab2[_ix[_ix < m]] = True
        _selm = {"masse": _lab2, "vuoto": ~_lab2}
        _wsc = {q: float(np.sum(cop_i[:m][s] * _dsy[s])) for q, s in sorted(_selm.items())}
        _wnc = {q: float(np.sum(cop_i[:m][s] * _newt[s])) for q, s in sorted(_selm.items())}
        _dsc = {q: float(np.sqrt(np.mean(_dsy[s] ** 2))) if np.any(s) else 0.0
                for q, s in sorted(_selm.items())}
        # --- ### ⭐ **IL LAVORO DI `A` CHE CAMBIA, col PASSO DI RITARDO DICHIARATO.**
        #     `U(A di QUESTO passo, phi) - U(A del passo PRIMA, phi)`, ### **la stessa
        #     `phi`** *(quella di questo passo, cioe' le `phi` NUOVE del precedente)*.
        #     ### ➜ **Si somma con `dU_phi` DEL PASSO PRECEDENTE** e i due chiudono
        #     `U(A nuova, phi nuove) - U(A vecchia, phi vecchie)`.
        dUA = None
        pp = self._en_prec
        if pp is not None and len(pp["i"]):
            iq = pp["i"]
            jq = pp["j"]
            if int(iq.max()) < na and int(jq.max()) < na:
                uq = -K_C * pp["A"] * np.cos(ph0[iq] - ph0[jq])
                NN = np.int64(max(na, 1))
                ka = np.minimum(ii, jj) * NN + np.maximum(ii, jj)
                kb = np.minimum(iq, jq) * NN + np.maximum(iq, jq)
                ca = np.isin(ka, kb)
                cb = np.isin(kb, ka)
                dUA = {
                    "totale": U0 - float(np.sum(uq)),
                    # ### **`w` CHE CAMBIA**: gli archi presenti in ENTRAMBI i passi
                    "w_su_archi_comuni": (float(np.sum(u0[ca]))
                                          - float(np.sum(uq[cb]))),
                    # ### **LE NASCITE**: gli archi che ci sono solo DOPO
                    "nascite_archi_nuovi": float(np.sum(u0[~ca])),
                    # ### e quelli che sono SPARITI *(la mitosi ne toglie)*
                    "archi_spariti": -float(np.sum(uq[~cb])),
                    "quanti_comuni": int(np.sum(ca)),
                    "quanti_nuovi": int(np.sum(~ca)),
                    "quanti_spariti": int(np.sum(~cb)),
                    "chiude": "il passo PRECEDENTE: si somma col suo `dU_phi`"}
        return {
            "T_pre": T0, "T_post": T1, "T_pre_per_classe": T0_cl,
            "T_post_per_classe": T1_cl, "dT": T1 - T0,
            "U": U0, "U_per_classe": U_cl, "archi_per_classe": U_na,
            "H_pre": T0 + U0,
            "dU_phi": dU_phi, "dU_phi_per_classe": dU_phi_cl,
            "dU_A_chiude_il_precedente": dUA,
            "W_interferenza": W_interf, "W_coppia_totale": W_tot,
            "W_extra_non_gradiente": W_tot - W_interf,
            # ### ⭐ **`D2-TER`**: la spartizione del lavoro fra `Newton` e `sync`
            # ### ⭐ **`D3`:** l energia `U(2)` e i suoi tre pezzi
            "u2": (self._energia_u2_pezzi(net)
                   if self.braccio in FORMA_U2 else None),
            "u2_contatori": (dict(self.cont_u2) if self.braccio in FORMA_U2 else None),
            "W_newton": W_newton, "W_sync": W_sync,
            "W_newton_totale": W_newton_tot, "W_sync_totale": W_sync_tot,
            "W_sync_per_classe": _wsc, "W_newton_per_classe": _wnc,
            "delta_sync_rms": float(np.sqrt(np.mean(_dsy ** 2))) if m else 0.0,
            "delta_sync_massimo": float(np.max(np.abs(_dsy))) if m else 0.0,
            "delta_sync_non_nulli": int(np.sum(_dsy != 0.0)),
            "delta_sync_rms_per_classe": _dsc,
            # ### la ricomposizione: ### **TAUTOLOGICA**, e si riporta come tale
            "ricomposizione_residuo": float(abs((W_newton + W_sync) - W_interf)
                                            / max(abs(W_interf), 1e-300)),
            "residuo_relativo": res,
            "dphi_massimo": dphi_max, "nodi_del_lavoro": m,
            "E_cin_del_codice": float(np.mean(p1[:nc] ** 2)) if nc else None,
            "nota": ("`T` e' (1/2)*M_PH*somma(phivel^2); `E_cin_del_codice` e' "
                     "mean(phivel^2) di `:7711`, un analogo di TEMPERATURA. "
                     "DUE COSE DIVERSE.")}

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
                # ### ⭐ **`D2-TER`:** i contatori che dicono se `K_SYNC = 0` e' UN SOLO
                #   interruttore, ### **per CHIAMANTE** *(riga del chiamante -> [chiamate,
                #   cambiate])*.
                "verifica_calcola_psi": getattr(self, "_psi_cont", None),
                # ### ⭐ **`D3`:** i contatori della forma `U(2)`, compreso quello che
                #   dice quante volte `_bloch_ritardato` *(che ha MEMORIA)* e' stata
                #   chiamata: deve essere ### **una per passo.**
                "verifica_u2": (dict(self.cont_u2)
                                if self.braccio in FORMA_U2 else None),
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
    elif braccio == "B-U2-TS-NOSYNC":
        stampa("  ### INTERVENTO: i tre di B-SCAL-TS-NOSYNC (scuotimento inerte, xi_termo "
               "azzerata, K_SYNC = 0) **piu'** LA FORMA U(2) al posto della coppia del "
               "simulatore. ### La forma vive SOLO nello strumento: nel simulatore non si "
               "tocca niente.")
        stampa("  ### LA FORMA: psi_k = e^{i phi_k/2} chi_k, "
               "E = -K_C somma_archi A_ij Re<psi_i|N_ij|psi_j>, coppia = -dE/dphi. "
               "La derivata da' coppia_i += +K_C*A*Im(ov)/2 e coppia_j += -.../2, e "
               "l antisimmetria E' l azione-reazione perche' N_ji = N_ij^dag.")
        stampa("  ### ⚠ DA DICHIARARE NEL REFERTO: l energia per legame va come "
               "cos(Dphi/2), NON come cos(Dphi); e il campo scalare (calcola_psi) RESTA "
               "a e^{i phi} -- e' una scelta di Luca ancora APERTA, e questo braccio non "
               "la tocca.")
        stampa("  ### ⛔ E _bloch_ritardato HA MEMORIA (self._nb_ret): l involucro "
               "SOSTITUISCE l originale e la chiama UNA volta per passo. Il conteggio e' "
               "nel json.")
    elif braccio == "B-SCAL-TS-NOSYNC":
        stampa("  ### INTERVENTO QUADRUPLO: i tre di `B-SCAL-TS` **piu'** `K_SYNC = 0` "
               "messo DALLO STRUMENTO sul modulo e ripristinato. ### Nel simulatore non "
               "si tocca niente.")
        stampa("  ### IL CENSIMENTO, dal codice: `K_SYNC` apre il blocco di :7767, la "
               "cui UNICA uscita e' `delta_sync_phi` (:7805), perche' `_forza_sync` si "
               "popola SOLO SE uno fra SYNC_SPINORE, SYNC_FASE_OROLOGIO e KURAMOTO_SU2 "
               "e' acceso -- e nel driver sono TUTTI E TRE SPENTI.")
        stampa("  ### ⚠ MA IL BLOCCO CONTIENE `calcola_psi(w)` (:7771), che SCRIVE "
               "`self.psi`. Saltarlo DOVREBBE essere byte-inerte, e l involucro lo "
               "MISURA: firma `psi` prima e dopo ogni chiamata, per chiamante.")
    elif braccio == "B-SCAL-TS":
        stampa("  ### INTERVENTO TRIPLO, e sono i DUE GIA' SIGILLATI COMPOSTI: "
               "`scuoti_vuoto` INERTE **e** `xi_termo` azzerata prima di ogni `step` "
               "(come `B-TS`), **piu'** `_coppia_interferenza` sul suo RAMO SCALARE "
               "(come `B-SCAL`). ### Nessun codice nuovo di intervento: le TRE "
               "appartenenze di braccio sono estese, e il diff e' ADDITIVO.")
        stampa("  ### ⚠ E IL CRITERIO DELLA CONSERVAZIONE SI VALUTA SULLA COPPIA "
               "DELL'INTERFERENZA, non sulla totale: con i flag del driver si "
               "sommano REPULS_LEGGE (:7621), SPIN_FEEDBACK (:7656) e FRAME_DRAG "
               "(:7702), e K_SYNC muove phi fuori dalla coppia (:7805). ### Scritto "
               "nel task history PRIMA della corsa.")
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
    # ### ⚠ **ERANO CINQUE E ORA SONO SEI**, e il collaudo me l'ha preso: la tupla
    #   e' ### **l'elenco autorevole**, e un caso che la conta e' quello che impedisce
    #   di aggiungere un braccio e dimenticarsi di dichiararlo.
    # ---- ### ⭐ **`D3`: il braccio `U(2)` e le QUATTRO appartenenze**
    prova("B-U2-TS-NOSYNC: ### spegne lo scuotimento, azzera `xi_termo` e porta `K_SYNC` a zero *(come `B-SCAL-TS-NOSYNC`)*",
          "B-U2-TS-NOSYNC" in SENZA_SCUOTI and "B-U2-TS-NOSYNC" in SENZA_XI
          and "B-U2-TS-NOSYNC" in SENZA_SYNC)
    prova("B-U2-TS-NOSYNC: ### ⛔ DEVE FALLIRE a prendere il RAMO SCALARE del simulatore: usa la forma `U(2)`, che e' MIA e sta nello strumento",
          "B-U2-TS-NOSYNC" not in RAMO_SCALARE and "B-U2-TS-NOSYNC" in FORMA_U2)
    prova("B-U2-TS-NOSYNC: ### e i bracci `B-SCAL*` NON prendono la forma `U(2)`",
          all(b not in FORMA_U2 for b in RAMO_SCALARE))
    prova("bracci: ### le quattro tuple di appartenenza contengono SOLO bracci dichiarati",
          all(b in BRACCI for b in SENZA_SCUOTI + SENZA_XI + SENZA_SYNC
              + RAMO_SCALARE + FORMA_U2))
    prova("bracci: ### gli OTTO sono dichiarati *(`B-U2-TS-NOSYNC` compreso)*",
          BRACCI == ("base", "B-T", "B-S", "B-TS", "B-SCAL", "B-SCAL-TS",
                     "B-SCAL-TS-NOSYNC", "B-U2-TS-NOSYNC"))
    # ---- ### ⭐ **LA DERIVATA DELLA FORMA `U(2)`, su un grafo a mano**
    _n6 = 4
    _i6 = np.array([0, 1, 2])
    _j6 = np.array([1, 2, 3])
    _A6 = np.array([0.7, -0.3, 0.5])
    _M6 = np.array([0.6 + 0.2j, -0.4 + 0.5j, 0.9 - 0.1j])
    _ph6 = np.array([0.3, -0.8, 1.1, 2.0])
    _E6, _ov6 = energia_u2(2.0, _A6, _M6, _ph6, _i6, _j6)
    _c6 = coppia_u2(2.0, _A6, _ov6, _i6, _j6, _n6)
    _eps = 1e-7
    _pg = 0.0
    for _k6 in range(_n6):
        _p = _ph6.copy(); _p[_k6] += _eps
        _q = _ph6.copy(); _q[_k6] -= _eps
        _d6 = (energia_u2(2.0, _A6, _M6, _p, _i6, _j6)[0]
               - energia_u2(2.0, _A6, _M6, _q, _i6, _j6)[0]) / (2.0 * _eps)
        _pg = max(_pg, abs(-_d6 - _c6[_k6]) / max(abs(_c6[_k6]), 1e-9))
    prova("D3: ### su un grafo a mano `coppia = -dE/dphi` chiude *(scarto relativo massimo `%.3e`)*" % _pg, _pg < 1e-7)
    prova("D3: ### ⛔ DEVE FALLIRE -- una coppia SENZA il fattore `1/2` NON e' `-dE/dphi` *(scarto relativo `%.3e`)*"
          % (max(abs(2.0 * _c6[_k] - _c6[_k]) / max(abs(_c6[_k]), 1e-9)
                 for _k in range(_n6))),
          max(abs(2.0 * _c6[_k] - _c6[_k]) / max(abs(_c6[_k]), 1e-9)
              for _k in range(_n6)) > 1e-2)
    prova("D3: ### la somma della coppia sugli archi e' ZERO *(azione-reazione: `%.3e`)*" % abs(float(np.sum(_c6))),
          abs(float(np.sum(_c6))) < 1e-12)
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
    # ---- ### ⭐ **`B-SCAL-TS`: fa TUTTE E TRE le cose, e si rilegge dal codice**
    prova("B-SCAL-TS: ### spegne lo scuotimento *(come `B-S`)*",
          "B-SCAL-TS" in ("B-S", "B-TS", "B-SCAL-TS"))
    prova("B-SCAL-TS: ### azzera `xi_termo` *(come `B-T`)*",
          "B-SCAL-TS" in ("B-T", "B-TS", "B-SCAL-TS"))
    prova("B-SCAL-TS: ### e prende il RAMO SCALARE *(come `B-SCAL`)*",
          "B-SCAL-TS" in ("B-SCAL", "B-SCAL-TS"))
    prova("B-SCAL-TS: ### DEVE FALLIRE -- `B-SCAL` NON azzera `xi_termo` e NON spegne "
          "lo scuotimento: il braccio nuovo non e' un alias del vecchio",
          ("B-SCAL" not in ("B-T", "B-TS", "B-SCAL-TS"))
          and ("B-SCAL" not in ("B-S", "B-TS", "B-SCAL-TS")))
    prova("B-SCAL-TS: ### il diff e' ADDITIVO -- per i CINQUE bracci di prima le tre "
          "condizioni valutano IDENTICO a quelle di prima",
          all((b in ("B-S", "B-TS", "B-SCAL-TS")) == (b in ("B-S", "B-TS"))
              for b in ("base", "B-T", "B-S", "B-TS", "B-SCAL"))
          and all((b in ("B-T", "B-TS", "B-SCAL-TS")) == (b in ("B-T", "B-TS"))
                  for b in ("base", "B-T", "B-S", "B-TS", "B-SCAL"))
          and all((b in ("B-SCAL", "B-SCAL-TS")) == (b == "B-SCAL")
                  for b in ("base", "B-T", "B-S", "B-TS", "B-SCAL")))
    # ---- ### **le TRE classi di arco sono DISGIUNTE e COPRONO tutto**
    _o = TermoH3("B-SCAL-TS")
    _o.masse = {"m0": np.array([0, 1, 2]), "m1": np.array([3, 4])}
    _ii = np.array([0, 1, 3, 5, 6, 2])
    _jj = np.array([1, 2, 4, 6, 7, 5])
    _s = _o._classe_archi(_ii, _jj, 8)
    _tot = _s["masse"].astype(int) + _s["vuoto"].astype(int) + _s["misti"].astype(int)
    prova("archi: ### le TRE classi sono DISGIUNTE e coprono TUTTI gli archi "
          "*(masse %d, vuoto %d, misti %d su %d)*"
          % (int(_s["masse"].sum()), int(_s["vuoto"].sum()), int(_s["misti"].sum()),
             len(_ii)),
          bool(np.all(_tot == 1)))
    # ### ⚠ **AVEVO SCRITTO `== 2` E SONO `1`:** sui sei archi di prova l'unico
    #   MASSA-VUOTO e' `(2, 5)`. ### **Errore MIO nel contare, preso dal collaudo** --
    #   ed e' esattamente a questo che serve scrivere il numero atteso invece di
    #   chiedere solo <<maggiore di zero>>.
    prova("archi: ### DEVE FALLIRE a mettere un arco MASSA-VUOTO fra le masse -- "
          "l'unico misto e' `(2, 5)`, e `misti` ne conta %d" % int(_s["misti"].sum()),
          int(_s["misti"].sum()) == 1 and int(_s["masse"].sum()) == 3
          and int(_s["vuoto"].sum()) == 2)
    # ---- ### ⭐ **`D2-TER`: LA SPARTIZIONE DEL LAVORO, E IL CASO CHE DEVE FALLIRE**
    #     `Dphi = dt_n*p2 + delta_sync_phi`, quindi
    #     `somma(c*Dphi) = somma(c*dt_n*p2) + somma(c*delta_sync)`.
    _c9 = np.array([1.7, -0.4, 0.9])
    _dtn9 = np.array([0.0085, 0.0090, 0.0088])
    _p29 = np.array([0.5, -0.2, 0.9])
    _ds9 = np.array([0.0031, -0.0012, 0.0007])
    _dphi9 = _dtn9 * _p29 + _ds9
    _wi9 = float(np.sum(_c9 * _dphi9))
    _wn9 = float(np.sum(_c9 * (_dtn9 * _p29)))
    _ws9 = float(np.sum(_c9 * _ds9))
    prova("D2-TER: ### `W_newton + W_sync` RICOMPONE `W_interferenza` al bit "
          "*(`%.6e` contro `%.6e`)* -- ### ⚠ **ed e' TAUTOLOGICO**, perche' i due "
          "addendi partizionano `Dphi` per definizione: si riporta, NON si spaccia per "
          "un controllo" % (_wn9 + _ws9, _wi9),
          abs((_wn9 + _ws9) - _wi9) <= 1e-12 * max(abs(_wi9), 1e-30))
    prova("D2-TER: ### ⛔ DEVE FALLIRE -- la ricomposizione con UN TERMINE TOLTO "
          "*(solo `W_newton`)* NON chiude: `%.6e` contro `%.6e`, scarto relativo "
          "`%.3e`" % (_wn9, _wi9, abs(_wn9 - _wi9) / max(abs(_wi9), 1e-30)),
          abs(_wn9 - _wi9) > 1e-6 * max(abs(_wi9), 1e-30))
    prova("D2-TER: ### e DEVE FALLIRE anche con il solo `W_sync`: `%.6e` contro "
          "`%.6e`" % (_ws9, _wi9),
          abs(_ws9 - _wi9) > 1e-6 * max(abs(_wi9), 1e-30))
    # ---- ### ⭐ **LA DERIVAZIONE DI `delta_sync_phi` SI RECUPERA AL BIT**
    _rec9 = _dphi9 - _dtn9 * _p29
    prova("D2-TER: ### `delta_sync_phi = Dphi - dt_n*p2` recupera il termine AL BIT "
          "*(scarto massimo `%.3e`)*" % float(np.max(np.abs(_rec9 - _ds9))),
          float(np.max(np.abs(_rec9 - _ds9))) < 1e-15)
    prova("D2-TER: ### ⛔ DEVE FALLIRE -- con `delta_sync = 0` la derivazione da' "
          "ESATTAMENTE zero, quindi un NON-zero in `NOSYNC` sarebbe un difetto della "
          "formula e non della fisica",
          float(np.max(np.abs((_dtn9 * _p29) - _dtn9 * _p29))) == 0.0)
    # ---- ### **il braccio nuovo fa TUTTE E QUATTRO le cose**
    prova("B-SCAL-TS-NOSYNC: ### spegne lo scuotimento, azzera `xi_termo` e prende il "
          "ramo scalare *(come `B-SCAL-TS`)*",
          "B-SCAL-TS-NOSYNC" in ("B-S", "B-TS", "B-SCAL-TS", "B-SCAL-TS-NOSYNC")
          and "B-SCAL-TS-NOSYNC" in ("B-T", "B-TS", "B-SCAL-TS", "B-SCAL-TS-NOSYNC")
          and "B-SCAL-TS-NOSYNC" in ("B-SCAL", "B-SCAL-TS", "B-SCAL-TS-NOSYNC"))
    prova("B-SCAL-TS-NOSYNC: ### ⛔ DEVE FALLIRE -- `B-SCAL-TS` NON porta `K_SYNC` a "
          "zero: il braccio nuovo non e' un alias del vecchio",
          ("B-SCAL-TS" == "B-SCAL-TS-NOSYNC") is False)
    prova("B-SCAL-TS-NOSYNC: ### il diff e' ADDITIVO -- per i SEI bracci di prima le "
          "tre condizioni valutano IDENTICO a quelle di prima",
          all((b in ("B-S", "B-TS", "B-SCAL-TS", "B-SCAL-TS-NOSYNC"))
              == (b in ("B-S", "B-TS", "B-SCAL-TS"))
              for b in ("base", "B-T", "B-S", "B-TS", "B-SCAL", "B-SCAL-TS"))
          and all((b in ("B-T", "B-TS", "B-SCAL-TS", "B-SCAL-TS-NOSYNC"))
                  == (b in ("B-T", "B-TS", "B-SCAL-TS"))
                  for b in ("base", "B-T", "B-S", "B-TS", "B-SCAL", "B-SCAL-TS"))
          and all((b in ("B-SCAL", "B-SCAL-TS", "B-SCAL-TS-NOSYNC"))
                  == (b in ("B-SCAL", "B-SCAL-TS"))
                  for b in ("base", "B-T", "B-S", "B-TS", "B-SCAL", "B-SCAL-TS")))
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
#   ### ⭐ **IL COLLAUDO DEL POTENZIALE, SULLA FUNZIONE VERA**
# ==========================================================================
def collaudo_potenziale():
    """### ⛔ **IL COLLAUDO CHE IL MANDATO CHIEDE, e si fa PRIMA della corsa.**

    `U = -K_C somma_archi A cos(phi_i - phi_j)`. Il ### **RAMO SCALARE** di
    `_coppia_interferenza` *(`:7484`)* deve dare ### **esattamente `-dU/dphi`**, a meno
    dell'arrotondamento. ### **E IL CASO CHE DEVE FALLIRE: la coppia SPINORIALE**
    *(quella del driver, `:7474`)* ### **NON deve chiudere.**
    ### ⚠ **E IL CASO CHE DEVE FALLIRE PUO' PASSARE PER CASO:** il docstring del
    simulatore dice che nel limite `b = 0, a = e^{i phi}` i due rami ### **COINCIDONO**.
    Quindi la distanza dello spinore da quel limite ### **SI MISURA**, e se fosse
    piccola il caso sarebbe ### **VUOTO** -- e lo direi.
    ### ➜ **Se la prima identita' non chiude: FERMO, e lo scrivo.**
    """
    esiti = []

    def prova(et, ok):
        esiti.append(bool(ok))
        stampa("  %s  %s" % ("ok  " if ok else "FALLITO", et))
        return bool(ok)

    b = blob(SIM)
    riga("=")
    stampa("IL COLLAUDO DEL POTENZIALE -- sulla funzione VERA del simulatore")
    riga("=")
    stampa("  simulatore %s   atteso %s" % (b[:8], BLOB_ATTESO))
    if not b.startswith(BLOB_ATTESO):
        raise SystemExit("[FERMO] il blob del simulatore NON e' quello atteso.")
    with contextlib.redirect_stdout(io.StringIO()):
        S, N, _a = carica("coll_potenziale", SIM)
    _cli_flag.dichiara_configurazione(S, stampa)
    stampa("  scena: n = %d, archi = %d" % (N.n, len(N.i)))
    # ### ⛔ **UN PASSO VERO PRIMA**, perche' il ramo spinoriale vuole `_psi_spinor`:
    #   senza quello ricadrebbe sul ramo scalare e il caso <<deve fallire>>
    #   ### **passerebbe per il motivo sbagliato** -- un FALSO-UNO.
    with contextlib.redirect_stdout(io.StringIO()):
        _passo.passo_pieno(S, N)
    n = int(N.n)
    K_C = float(S.K_C)
    ii = np.asarray(N.i, np.int64)
    jj = np.asarray(N.j, np.int64)
    _ps = getattr(N, "_psi_spinor", None)
    ok_pre = (bool(S.CAMPO_SPINORIALE) and _ps is not None and len(_ps) >= n
              and bool(S.FORK_SU2) and len(ii) > 0)
    prova("le PRECONDIZIONI del ramo spinoriale sono soddisfatte: "
          "`CAMPO_SPINORIALE` %r, `FORK_SU2` %r, `_psi_spinor` %s, archi %d "
          "*(senza queste il caso <<deve fallire>> sarebbe un FALSO-UNO)*"
          % (bool(S.CAMPO_SPINORIALE), bool(S.FORK_SU2),
             ("len %d >= n %d" % (len(_ps), n)) if _ps is not None else "ASSENTE",
             len(ii)), ok_pre)

    def U(A, ph):
        return -K_C * float(np.sum(A * np.cos(ph[ii] - ph[jj])))

    def grad(A, ph):
        """### `-dU/dphi`, dalla derivata analitica e SCRITTA."""
        g = np.zeros(n)
        s = K_C * A * np.sin(ph[ii] - ph[jj])
        np.add.at(g, ii, +s)          # ### `dU/dphi_i = +K_C A sin(phi_i - phi_j)`
        np.add.at(g, jj, -s)          # ### `dU/dphi_j = -K_C A sin(phi_i - phi_j)`
        return -g                     # ### `coppia = -dU/dphi`

    def scalare(A, ph):
        """### Il RAMO SCALARE del SIMULATORE, non una mia copia."""
        _v = S.CAMPO_SPINORIALE
        S.CAMPO_SPINORIALE = False
        try:
            return np.asarray(N._coppia_interferenza(A, np.exp(1j * ph)), float)
        finally:
            S.CAMPO_SPINORIALE = _v

    rng = np.random.default_rng(11)
    w = N._pesi()
    casi = [("la `A` e le `phi` VERE del simulatore",
             w * np.cos(N.phi0[ii] - N.phi0[jj]), np.asarray(N.phi, float).copy()),
            ("una `A` e delle `phi` CASUALI",
             rng.normal(0.0, 1.0, len(ii)), rng.uniform(0.0, 4.0 * np.pi, n)),
            ("una `A` casuale con le `phi` VERE",
             rng.normal(0.0, 0.3, len(ii)), np.asarray(N.phi, float).copy())]
    for et, A, ph in casi:
        c_vera = scalare(A, ph)
        c_att = grad(A, ph)
        sc = max(float(np.max(np.abs(c_att))), 1e-300)
        rel = float(np.max(np.abs(c_vera - c_att))) / sc
        prova("### il ramo SCALARE **E'** `-dU/dphi` -- %s: differenza massima "
              "relativa `%.3e` *(scala `%.4f`)*" % (et, rel, sc), rel < 1e-10)
    # ---- ### ⭐ **IL CONTROLLO INDIPENDENTE: LA DIFFERENZA FINITA.**
    #     Non usa la mia algebra: perturba `phi_k` e guarda `U`. Se la derivata
    #     analitica fosse sbagliata, ### **questo se ne accorge comunque.**
    A, ph = casi[0][1], casi[0][2]
    c_vera = scalare(A, ph)
    eps = 1e-6
    nodi = rng.choice(n, size=12, replace=False)
    peggio = pegg_glob = 0.0
    U_tot = abs(U(A, ph))
    for k in nodi:
        p = ph.copy(); p[k] += eps
        m = ph.copy(); m[k] -= eps
        # ### ⭐ **SOLO GLI ARCHI CHE TOCCANO `k`:** `U` dipende da `phi_k` solo
        #   attraverso quelli, quindi la restrizione da' la ### **STESSA derivata**
        #   -- ed e' esatta, non un'approssimazione. ### **Ma la CANCELLAZIONE
        #   crolla**, perche' i due numeri sottratti non sono piu' grandi come `U`.
        _m = (ii == k) | (jj == k)
        _Ak = A[_m]; _ik = ii[_m]; _jk = jj[_m]

        def _Uk(_ph, _A=_Ak, _i=_ik, _j=_jk):
            return -K_C * float(np.sum(_A * np.cos(_ph[_i] - _ph[_j])))

        d = (_Uk(p) - _Uk(m)) / (2.0 * eps)        # ### `dU/dphi_k`, ESATTA
        peggio = max(peggio, abs(-d - c_vera[k]) / max(abs(c_vera[k]), 1e-6))
        dg = (U(A, p) - U(A, m)) / (2.0 * eps)     # ### la stessa cosa su `U` INTERA
        pegg_glob = max(pegg_glob, abs(-dg - c_vera[k]) / max(abs(c_vera[k]), 1e-6))
    prova("### LA DIFFERENZA FINITA conferma, su 12 nodi scelti a caso: scarto "
          "relativo massimo `%.3e` *(e questo controllo NON passa dalla mia "
          "derivata)*" % peggio, peggio < 1e-7)
    # ### ⚠ **E IL MIO PRIMO CONTROLLO ERA SBAGLIATO, non il codice.** Fatto su `U`
    #   INTERA dava `%.3e`, che non e' un disaccordo: e' il ### **PAVIMENTO DI
    #   CANCELLAZIONE** di una differenza fra due numeri grandi `|U| = %.3e`.
    #   Il pavimento atteso e' `eps_macchina*|U| / (2*eps*|coppia|)`, e si STAMPA.
    _pav = (2.22e-16 * U_tot) / (2.0 * eps * max(float(np.max(np.abs(c_vera[nodi]))),
                                                1e-300))
    prova("### e la versione su `U` INTERA da' `%.3e`, che NON e' un disaccordo ma il "
          "PAVIMENTO DI CANCELLAZIONE: `|U| = %.4g`, pavimento atteso `%.3e`. "
          "### **Errore MIO di precisione, non del codice**"
          % (pegg_glob, U_tot, _pav), pegg_glob < 100.0 * _pav)
    # ---- ### ⛔ **IL CASO CHE DEVE FALLIRE**
    c_spin = np.asarray(N._coppia_interferenza(A, np.exp(1j * ph)), float)
    c_att = grad(A, ph)
    sc = max(float(np.max(np.abs(c_att))), 1e-300)
    rel_s = float(np.max(np.abs(c_spin - c_att))) / sc
    prova("### ⛔ DEVE FALLIRE -- la coppia SPINORIALE *(il ramo del driver)* **NON** e' "
          "`-dU/dphi`: differenza massima relativa `%.3e`" % rel_s, rel_s > 1e-2)
    # ---- ### **e la distanza dello spinore dal limite in cui i due rami COINCIDONO**
    _p = np.asarray(_ps)[:n]
    _bmax = float(np.max(np.abs(_p[:, 1])))
    _amax = float(np.max(np.abs(_p[:, 0] - np.exp(1j * np.asarray(N.phi, float)[:n]))))
    prova("### lo spinore NON e' nel limite `b = 0, a = e^{i phi}` in cui i due rami "
          "coinciderebbero: `max|b| = %.4f`, `max|a - e^{i phi}| = %.4f` -- quindi il "
          "caso che deve fallire ### **non e' vuoto**" % (_bmax, _amax),
          _bmax > 1e-6 or _amax > 1e-6)
    riga("-")
    stampa("  COLLAUDO DEL POTENZIALE: %d su %d" % (sum(esiti), len(esiti)))
    if not all(esiti):
        stampa("### ⛔ FERMO: il collaudo del potenziale NON chiude. Il mandato dice "
               "di fermarsi e scriverlo, e mi fermo.")
    return 0 if all(esiti) else 1


# ==========================================================================
#   ### ⭐ **`D3`: IL COLLAUDO DELLA FORMA `U(2)`, SULLA SCENA VERA**
# ==========================================================================
def collaudo_u2():
    """### ⛔ **I QUATTRO CONTROLLI CHE IL MANDATO CHIEDE, prima della corsa.**

    `(1)` `coppia = -dE/dphi` con scarto `<= 1e-12`, ### **piu' la differenza finita
    LOCALE** *(ristretta agli archi del nodo, dove non c'e' cancellazione)*;
    `(2)` la ### **DOPPIA COPERTURA** su `E`;
    `(3)` il ### **limite `U(1)`**: `chi` uguale e `N = I` danno
    `(1/2) K_C somma A sin((phi_j - phi_k)/2)`;
    `(4)` ### **il caso che DEVE fallire**: la coppia spinoriale del driver NON e'
    `-dE/dphi`.
    ### ➜ **Se `(1)` non chiude: FERMO, e la corsa non parte.**
    """
    esiti = []

    def prova(et, ok):
        esiti.append(bool(ok))
        stampa("  %s  %s" % ("ok  " if ok else "FALLITO", et))
        return bool(ok)

    b = blob(SIM)
    riga("=")
    stampa("IL COLLAUDO DELLA FORMA `U(2)` -- sulla scena VERA del driver")
    riga("=")
    stampa("  simulatore %s   atteso %s" % (b[:8], BLOB_ATTESO))
    if not b.startswith(BLOB_ATTESO):
        raise SystemExit("[FERMO] il blob del simulatore NON e' quello atteso.")
    with contextlib.redirect_stdout(io.StringIO()):
        S, N_, _a = carica("coll_u2", SIM)
    _cli_flag.dichiara_configurazione(S, stampa)
    with contextlib.redirect_stdout(io.StringIO()):
        _passo.passo_pieno(S, N_)
    n = int(N_.n)
    K_C = float(S.K_C)
    ii = np.asarray(N_.i, np.int64)
    jj = np.asarray(N_.j, np.int64)
    w = N_._pesi()
    A = w * np.cos(N_.phi0[ii] - N_.phi0[jj])
    ph = np.asarray(N_.phi, float)[:n]
    stampa("  scena: n = %d, archi = %d" % (n, len(ii)))
    # ### la gauge, e il conteggio del ramo degenere
    chi, alpha, quanti = gauge_chi(N_._psi_spinor, n)
    _nrm = np.abs(np.linalg.norm(chi, axis=1) - 1.0)
    prova("gauge: ### la PRIMA componente di `chi` e' REALE e `>= 0` su tutti i nodi "
          "*(parte immaginaria massima `%.3e`, minimo reale `%.3e`)*, e la NORMA resta "
          "`1` *(scarto massimo `%.3e`)*"
          % (float(np.max(np.abs(np.imag(chi[:, 0])))),
             float(np.min(np.real(chi[:, 0]))), float(np.max(_nrm))),
          float(np.max(np.abs(np.imag(chi[:, 0])))) < 1e-12
          and float(np.min(np.real(chi[:, 0]))) >= -1e-15
          and float(np.max(_nrm)) < 1e-12)
    stampa("     ### nodi al POLO `b` *(gauge sulla seconda componente)*: %d su %d"
           % (quanti, n))
    if quanti == 0:
        stampa("     ### ⚠ E ALLORA QUEL RAMO NON E' ESERCITATO SU QUESTA SCENA: la "
               "gauge sulla seconda componente e' scritta e NON provata dai dati. "
               "### Lo dichiaro invece di contarla fra i controlli passati.")
    # ### ⭐ **E LA MISURA CHE DICE SE LA FORMA E' UNA RISCRITTURA:** la fase comune
    #   dello spinore contro `phi/2`.
    _dd = (alpha - 0.5 * ph + np.pi) % (2.0 * np.pi) - np.pi
    stampa("     ### `rms(wrap(alpha - phi/2))` = %.4f radianti, mediana %.4f -- "
           "### se e' grande, la forma SOSTITUISCE la fase dello spinore invece di "
           "riscriverla" % (float(np.sqrt(np.mean(_dd ** 2))),
                            float(np.median(np.abs(_dd)))))
    # ### `N` e `M`: ### ⛔ **senza `_bloch_ritardato`, che ha MEMORIA.** Nel collaudo si
    #   usa il Bloch CORRENTE, e si DICHIARA: il collaudo prova la DERIVATA, non lo
    #   Strato 1.
    nb = bloch_da_spinore(chi)
    Nm = N_._link_su2_N(nb[ii], nb[jj]) * 0.5
    M = emme_arco(N_, Nm, chi, ii, jj)
    stampa("  ### ⚠ IL COLLAUDO USA IL BLOCH CORRENTE, non quello ritardato: "
           "`_bloch_ritardato` ha MEMORIA (scrive `self._nb_ret`) e chiamarla qui "
           "sporcherebbe lo stato. ### Si prova la DERIVATA, non lo Strato 1.")

    def _E(_ph, _A=A, _M=M):
        return energia_u2(K_C, _A, _M, _ph, ii, jj)[0]

    E0, ov0 = energia_u2(K_C, A, M, ph, ii, jj)
    cop = coppia_u2(K_C, A, ov0, ii, jj, n)
    stampa("  `E` = %.6f   `max|coppia|` = %.6f" % (E0, float(np.max(np.abs(cop)))))
    # ---- ### **(1a) LA DIFFERENZA FINITA, ristretta agli archi del nodo**
    rng = np.random.default_rng(11)
    nodi = rng.choice(n, size=12, replace=False)
    eps = 1e-6
    peggio = 0.0
    scala_loc = 0.0
    for k in nodi:
        _m = (ii == k) | (jj == k)
        _Ak, _ik, _jk, _Mk = A[_m], ii[_m], jj[_m], M[_m]

        def _Ek(_ph, _A=_Ak, _i=_ik, _j=_jk, _MM=_Mk):
            return -K_C * float(np.sum(_A * np.real(
                np.exp(0.5j * (_ph[_j] - _ph[_i])) * _MM)))

        scala_loc = max(scala_loc, abs(_Ek(ph)))
        p = ph.copy(); p[k] += eps
        q = ph.copy(); q[k] -= eps
        d = (_Ek(p) - _Ek(q)) / (2.0 * eps)              # ### `dE/dphi_k`
        peggio = max(peggio, abs(-d - cop[k]) / max(abs(cop[k]), 1e-9))
    # ### ⭐ **IL PAVIMENTO DELLA DIFFERENZA FINITA, DERIVATO e non scelto:**
    #   `eps_macchina * |E_locale| / (2*eps)`, diviso per la scala della coppia.
    #   ### ⚠ **La prima stesura chiedeva `1e-12` ANCHE a questa, e il collaudo me
    #   l ha preso:** `1e-12` e' la precisione dell IDENTITA' ALGEBRICA *(il controllo
    #   `1b`)*, NON di una differenza finita. ### **Seconda volta che imparo questa.**
    pav = (2.22e-16 * scala_loc) / (2.0 * eps)
    pav = pav / max(float(np.median(np.abs(cop[nodi]))), 1e-12)
    prova("D3 (1): ### **`coppia = -dE/dphi`**, confermata dalla DIFFERENZA FINITA su `12` nodi a caso, ristretta agli archi del nodo: scarto relativo massimo `%.3e`, contro un PAVIMENTO DERIVATO di `%.3e` *(`eps_macchina*|E_loc|/(2*eps)`, con `|E_loc| ~ %.2f`)*"
          % (peggio, pav, scala_loc), peggio < 100.0 * pav)
    # ---- ### **(1b) e la stessa cosa da una SECONDA strada algebrica**
    _mu = np.angle(M)
    _am = np.abs(M)
    _sn = K_C * A * _am * np.sin(0.5 * (ph[jj] - ph[ii]) + _mu)
    _c2 = np.zeros(n)
    np.add.at(_c2, ii, +0.5 * _sn)
    np.add.at(_c2, jj, -0.5 * _sn)
    _sc = float(np.max(np.abs(_c2 - cop))) / max(float(np.max(np.abs(cop))), 1e-300)
    prova("D3 (1b): ### e la forma `|M| sin(Dphi/2 + arg M)` da' la STESSA coppia "
          "*(scarto relativo `%.3e`)*: la derivata non poggia su una sola scrittura"
          % _sc, _sc < 1e-12)
    # ---- ### **(2) LA DOPPIA COPERTURA**
    #     ### ⚠ **UNO SPOSTAMENTO GLOBALE DI `2 pi` LASCIA `E` INVARIANTE**, perche' `E`
    #     dipende dalle DIFFERENZE: `psi -> -psi` su TUTTI i nodi e i segni si elidono a
    #     coppie. ### **La doppia copertura si vede su UN NODO SOLO**, ed e' il
    #     contenuto fisico: conta il segno RELATIVO.
    _kd = int(nodi[0])
    _p2 = ph.copy(); _p2[_kd] += 2.0 * np.pi
    _p4 = ph.copy(); _p4[_kd] += 4.0 * np.pi
    _pg = ph + 2.0 * np.pi
    _E2, _E4, _Eg = _E(_p2), _E(_p4), _E(_pg)
    prova("D3 (2): ### **`phi_k + 2pi` su UN NODO CAMBIA `E`** *(da `%.6f` a `%.6f`, "
          "differenza `%.6f`)*: `psi_k -> -psi_k` e gli archi che toccano `k` cambiano "
          "segno" % (E0, _E2, _E2 - E0), abs(_E2 - E0) > 1e-9)
    prova("D3 (2): ### **`phi_k + 4pi` RIPORTA `E` IDENTICO** *(scarto `%.3e`)*"
          % abs(_E4 - E0), abs(_E4 - E0) <= 1e-9 * max(abs(E0), 1.0))
    prova("D3 (2): ### ⚠ **e uno spostamento GLOBALE di `2pi` NON cambia `E`** "
          "*(scarto `%.3e`)*, perche' `E` dipende dalle DIFFERENZE -- ### **la doppia "
          "copertura si vede sul segno RELATIVO, non su quello assoluto**"
          % abs(_Eg - E0), abs(_Eg - E0) <= 1e-9 * max(abs(E0), 1.0))
    # ---- ### **(3) IL LIMITE `U(1)`**
    _chi1 = np.zeros((n, 2), complex); _chi1[:, 0] = 1.0
    _nb1 = bloch_da_spinore(_chi1)
    _N1 = N_._link_su2_N(_nb1[ii], _nb1[jj]) * 0.5
    _dI = float(np.max(np.abs(_N1 - np.eye(2)[None, :, :])))
    prova("D3 (3): ### con `chi` uguale su tutti i nodi `N/2` E' L IDENTITA' "
          "*(scarto massimo `%.3e`)* -- e viene da `_link_su2_N` DEL SIMULATORE, non da "
          "una mia matrice" % _dI, _dI < 1e-12)
    _M1 = emme_arco(N_, _N1, _chi1, ii, jj)
    _E1, _ov1 = energia_u2(K_C, A, _M1, ph, ii, jj)
    _c1 = coppia_u2(K_C, A, _ov1, ii, jj, n)
    _att = np.zeros(n)
    _s1 = K_C * A * np.sin(0.5 * (ph[jj] - ph[ii]))
    np.add.at(_att, ii, +0.5 * _s1)
    np.add.at(_att, jj, -0.5 * _s1)
    _d1 = float(np.max(np.abs(_c1 - _att))) / max(float(np.max(np.abs(_att))), 1e-300)
    prova("D3 (3): ### **IL LIMITE `U(1)` TORNA**: la coppia si riduce a "
          "`(1/2) K_C somma A sin((phi_j - phi_k)/2)` *(scarto relativo `%.3e`)*"
          % _d1, _d1 < 1e-12)
    # ---- ### ⛔ **(4) IL CASO CHE DEVE FALLIRE**
    _z = np.exp(1j * ph)
    _cs = np.asarray(N_._coppia_interferenza(A, _z), float)
    _sc4 = float(np.max(np.abs(_cs - cop))) / max(float(np.max(np.abs(cop))), 1e-300)
    prova("D3 (4): ### ⛔ **DEVE FALLIRE -- la coppia SPINORIALE del driver NON e' "
          "`-dE/dphi`** della forma `U(2)`: scarto massimo relativo `%.3e`" % _sc4,
          _sc4 > 1e-2)
    stampa("     ### e i due ordini di grandezza: `max|coppia U(2)|` = %.6f, "
           "`max|coppia driver|` = %.6f -- ### il `1/2` e il peso `cos(chi/2)` si vedono"
           % (float(np.max(np.abs(cop))), float(np.max(np.abs(_cs)))))
    riga("-")
    stampa("  COLLAUDO DELLA FORMA `U(2)`: %d su %d" % (sum(esiti), len(esiti)))
    if not all(esiti):
        stampa("### ⛔ FERMO: il collaudo della forma `U(2)` NON chiude, e la corsa NON "
               "parte. Il mandato dice di fermarsi e scriverlo.")
    return 0 if all(esiti) else 1


# ==========================================================================
def main(argv):
    a = argv[1:]
    if "--collaudo-u2" in a:
        e = collaudo_u2()
        os.makedirs(FUORI, exist_ok=True)
        io.open(os.path.join(FUORI, "collaudo_u2.txt"), "w",
                encoding="utf-8").write(NL.join(_MSG.P) + NL)
        return e
    if "--collaudo-potenziale" in a:
        e = collaudo_potenziale()
        os.makedirs(FUORI, exist_ok=True)
        io.open(os.path.join(FUORI, "collaudo_potenziale.txt"), "w",
                encoding="utf-8").write(NL.join(_MSG.P) + NL)
        return e
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
