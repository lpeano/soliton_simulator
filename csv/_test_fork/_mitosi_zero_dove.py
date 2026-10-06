# -*- coding: utf-8 -*-
"""IL `0.3` A ZERO DOPO LA CURA, **DOVE** cresce la rete, e il **CIRCOLO del dipolo**.

*(Mandato di Luca del 2026-10-06. Previsioni, classe `MATERIA`/`BORDO`/`VUOTO` e criteri sono
fissati in `doc/TASK_HISTORY/2026-10-06_mitosi-zero-dopo-la-cura.md`, committato **prima**.)*

### ⛔ **QUESTO STRUMENTO *IMPORTA* QUELLO DELLA MISURA LUNGA, NON LO COPIA.** Le
### registrazioni che il controllo `C0` deve riprodurre sono quindi ### **LETTERALMENTE LO
### STESSO CODICE**, non una copia che potrebbe divergere -- e questo e' piu' forte di un
### confronto fra due sorgenti.

**TRE DOMANDE, dal mandato:** `(1)` la crescita e' del **modello** o dipende ancora dal `0.3`?
`(2)` **DOVE** cresce la rete -- materia, bordo o vuoto? `(3)` **perche' accelera** --
l'ipotesi del **basculamento chirale**.

### ⛔ **IL BLOB SI VERIFICA ALL'AVVIO:** la misura vale per `cf2a1ac8` e per nessun altro, e
### su un blob diverso lo strumento **SI FERMA**.

# ESENTE-H-P3: lo strumento passa dal CLI (`_cli_flag.carica`) per la configurazione. Le
#   SEI ANCORE sulla copia patchata non configurano niente: cinque sono ganci di SOLA LETTURA
#   e la sesta rende INIETTABILE l'ampiezza `0.3` che e' gia' nel codice.

USO:  python csv/_test_fork/_mitosi_zero_dove.py --amp=0.0   [--passi=N]
      python csv/_test_fork/_mitosi_zero_dove.py --amp=0.3   [--passi=N]
      python csv/_test_fork/_mitosi_zero_dove.py --collaudo
      python csv/_test_fork/_mitosi_zero_dove.py --senza-ganci --amp=0.3 --passi=150
          *(il braccio di `C-letture`: la copia SENZA i ganci nuovi)*
"""
import contextlib
import io
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
sys.path.insert(0, _QUI)
import _presidio   # noqa: E402

_presidio.avvia(__file__)

import _passo                                    # noqa: E402,F401
import _cli_flag                                 # noqa: E402
import _tors_w8_lunga as LUNGA                   # noqa: E402

blob, q, carica = LUNGA.blob, LUNGA.q, LUNGA.carica
piattaforma, n4 = LUNGA.piattaforma, LUNGA.n4
stampa, riga = LUNGA.stampa, LUNGA.riga

NL = chr(10)
FUORI = os.path.join(RADICE, "csv", "_test_fork", "_mitosi_zero_dove")
SIM = LUNGA.SIM
BLOB_ATTESO = LUNGA.BLOB_ATTESO            # ### lo STESSO della misura lunga: `cf2a1ac8`
PASSI = LUNGA.PASSI                        # ### `1000`
PASSI_SALVA = LUNGA.PASSI_SALVA            # ### ogni `10`, e a ogni caduta
PASSI_PIENI = LUNGA.PASSI_PIENI
FINESTRA_DOVE = 100                        # ### le finestre del DOVE: `100` passi (mandato)
P2 = 2.0 * math.pi
P3 = 3.0 * math.pi
P4 = 4.0 * math.pi

# ### ⛔ **LE CLASSI, e la soglia e' DERIVATA dalla scena, non scelta** *(`A1`)*. `u` e' la
#   distanza dal baricentro della coorte piu' vicina, ### **in unita' di `r_regione`**:
#     `MATERIA` `u <= 1`            -- ### il test di appartenenza DELLA SCENA, verbatim
#     `BORDO`   `u <= 1 + R_CONN/r` -- ### `R_CONN` e' IL VARCO della scena
#     `VUOTO`   il resto
#   ### **Nessun numero nuovo:** `r_regione` e `R_CONN` sono gia' nella scena.
CLASSI = ("MATERIA", "BORDO", "VUOTO")


def classe(u, u_bordo):
    """La classe di un `u`. ### **`<=` su ENTRAMBE le soglie**, cosi' un nodo esattamente
    sulla superficie e' `MATERIA` -- che e' il test della scena *(`<= r`)*, verbatim."""
    u = np.asarray(u, float)
    return np.where(u <= 1.0, 0, np.where(u <= u_bordo, 1, 2))


# =============================================================== LA COPIA PATCHATA
def copia_patchata(sorgente, dst, amp, ganci=True):
    """I ganci della misura lunga **piu'** i cinque di questo mandato.

    ### ⛔ **NON COPIA `_tors_w8_lunga.copia_patchata`: LA CHIAMA.** Le tre ancore della
    misura lunga sono quindi ### **le stesse**, e se cambiassero cambierebbero per entrambi.

    `ganci=False` applica ### **solo** `_AMP` e la soglia: e' il braccio di `C-letture`, che
    pretende che i cinque ganci nuovi siano ### **di SOLA LETTURA**.
    """
    fatte = list(LUNGA.copia_patchata(sorgente, dst))
    t = io.open(dst, encoding="utf-8", newline="").read()

    def uno(a, b, et):
        nonlocal t
        k = t.count(a)
        if k != 1:
            raise SystemExit("[FERMO] l'ancora di `%s` compare %d volte, non 1." % (et, k))
        t = t.replace(a, b)
        fatte.append(et)

    def dopo(prefisso, righe, et):
        """Inserisce `righe` DOPO la riga che comincia con `prefisso`.

        ### STOPX **L'ANCORA E' UN PREFISSO ASCII** *(`P1-quater`: ancore ASCII)*: la riga di
        `twist_dip` finisce con un commento che contiene ### **`chiralita'` con l'accento**, e
        metterlo in un'ancora significherebbe far dipendere la patch da una codifica.
        """
        nonlocal t
        k = t.count(prefisso)
        if k != 1:
            raise SystemExit("[FERMO] il prefisso di `%s` compare %d volte, non 1."
                             % (et, k))
        a = t.index(prefisso)
        b = t.index(NL, a) + 1
        t = t[:b] + righe + t[b:]
        fatte.append(et)

    # --- ① `_AMP`, iniettata accanto al gancio di modulo della misura lunga
    uno("_MIS = None   # [TORS-W8 LUNGA] lo riempie lo strumento" + NL,
        "_MIS = None   # [TORS-W8 LUNGA] lo riempie lo strumento" + NL
        + ("_AMP = %r   # [MITOSI-ZERO] l'ampiezza della modulazione, INIETTATA" % (amp,))
        + NL,
        "C: `_AMP = %r` iniettata" % (amp,))
    # --- ② la soglia: ### `_AMP = 0.3` E' L'ESPRESSIONE ORIGINALE, `0.0` la annulla
    uno("            soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_modula))" + NL,
        "            soglia = soglia0 * (1.0 - _AMP * np.tanh(grad_modula))" + NL,
        "D: la soglia usa `_AMP` invece del `0.3` cablato")
    if ganci:
        # --- ③ il BASCULAMENTO. ### STOPX **SCRIVE `perc_geom`, NON `perc_chi`:**
        #     l'argv del driver ha ### **`--chi-coop`**, e con la cooperazione il
        #     basculamento scrive ### **la GEOMETRIA** mentre lo spinore scrive la carica
        #     *(`:7905`)*. ### **La mia prima versione hookava il ramo `else`, che in questa
        #     scena NON VIENE MAI ESEGUITO** -- e il giro corto l'ha mostrato subito:
        #     ### **`chi = 0` a ogni passo mentre il dipolo cambiava su `90854` archi.**
        uno("                self.perc_geom[:self.n] = np.where(twn > soglia, 1, -1)"
            ".astype(self.perc_geom.dtype)" + NL,
            "                if _MIS is not None:" + NL
            + "                    _MIS.geom(self, twn, soglia)" + NL
            + "                self.perc_geom[:self.n] = np.where(twn > soglia, 1, -1)"
            ".astype(self.perc_geom.dtype)" + NL,
            "E: il basculamento chirale, PRIMA della scrittura di `perc_geom`")
        # --- ③-bis ### STOPX **E IL GANCIO CHE CONTA DAVVERO: `chi_torsione`.**
        #     L'argv ha ### **ANCHE `--chi-core`**, quindi `chi_torsione` non e' `perc_geom`
        #     ma la ### **chiralita' CORE-LOCALE calcolata da `perc_geom`**, in cache in
        #     `_chi_geom_nodi` *(`:7849`-`:7855`)*. ### **Questo e' l'array che ENTRA nel
        #     dipolo**, e si misura DOVE il dipolo lo legge invece di indovinare chi
        #     l'ha scritto.
        dopo("                twist_dip = np.pi * 0.5 * (chi_torsione[i] - "
             "chi_torsione[j])",
             "                if _MIS is not None:" + NL
             + "                    _MIS.chi_tors(self, chi_torsione)" + NL,
             "E-bis: `chi_torsione`, l'array che ENTRA nel dipolo")
        # --- ④ la MITOSI: `self.n` e' una PROPRIETA' (`len(self.phi)`), quindi qui e' GIA'
        #     aggiornata e i nodi nuovi sono gli ULTIMI `len(sel)`.
        uno("        self._grado(); self.nati += len(sel)" + NL,
            "        if _MIS is not None:" + NL
            + "            _MIS.nati(self, 'divisione', len(sel))" + NL
            + "        self._grado(); self.nati += len(sel)" + NL,
            "F: le nascite per DIVISIONE")
        # --- ⑤ lo SCHWINGER
        uno("                self._grado(); self.nati += nc; self.coppie_nate += nc" + NL,
            "                if _MIS is not None:" + NL
            + "                    _MIS.nati(self, 'schwinger', int(nc))" + NL
            + "                self._grado(); self.nati += nc; self.coppie_nate += nc" + NL,
            "G: le nascite per SCHWINGER")
        # --- ⑥ il CALCIO di fase ai genitori (`KICK_TW`): ### DOPO, cosi' i due calci
        #     esistono.
        uno("            self.phi[b] = (self.phi[b] + calcio_b) % self._dphi()" + NL,
            "            self.phi[b] = (self.phi[b] + calcio_b) % self._dphi()" + NL
            + "            if _MIS is not None:" + NL
            + "                _MIS.calcio(self, calcio_a, calcio_b)" + NL,
            "H: il calcio di fase ai genitori (`KICK_TW`)")
    io.open(dst, "w", encoding="utf-8", newline="").write(t)
    return fatte


# =============================================================== LA MISURA
class Misura(LUNGA.Misura):
    """### **LEGGE SOLTANTO.** Estende quella della misura lunga: ### **non ne riscrive
    niente**, e `C-letture` misura al bit che i ganci nuovi non cambino il sistema."""

    def __init__(self, dt, amp):
        LUNGA.Misura.__init__(self, dt)
        self.amp = float(amp)
        self.u_bordo = None          # lo riempie `prepara()`, DALLA SCENA
        self.r_regione = None
        self.coorti = None
        self._azzera_passo()
        self.dove_nascite = []       # una riga per NASCITA
        self.dove_chi = []           # una riga per passo: i quantili dei nodi che cambiano
        self.dove_sopra4pi = {}      # ai passi pieni: la popolazione sopra `4pi`
        self._chi_prec = None
        self._perc_chi_prec = None
        self.cont.update({"cambi_geom_tot": 0, "cambi_chi_tors_tot": 0,
                          "cambi_perc_chi_tot": 0, "chi_tors_non_confrontabili": 0,
                          "nati_div_tot": 0, "nati_sch_tot": 0,
                          "spinta_pi_fase": 0, "spinta_pi_dip": 0,
                          "spinta_pi_entrambe": 0, "spinta_pi_tot": 0,
                          "spinta_pi_esatto": 0})

    def _azzera_passo(self):
        # ### ⛔ **`cambi_chi_tors` NASCE `None`, e NON `0`** *(`CHI-TORS-ZERO-FALSO`,
        #   curato il 2026-10-06 su decisione di Luca)*. ### **Il valore di partenza e' la
        #   risposta onesta quando il gancio non ha potuto misurare: <<non lo so>>.**
        #   ### ⚠ **Prima nasceva `0`**, e in `392` passi su `1000` *(braccio zero)* e
        #   ### **`731` su `1000`** *(acceso)* quello `0` ### **non era <<zero cambi>>: era
        #   <<non misurato>>** -- e la correlazione del criterio del dipolo ci cadeva dentro.
        self.p = {"cambi_geom": 0, "cambi_chi_tors": None, "cambi_perc_chi": 0,
                  "chi_tors_non_confrontabile": 0,
                  "spinta_pi_fase": 0, "spinta_pi_dip": 0,
                  "spinta_pi_entrambe": 0, "spinta_pi_tot": 0, "spinta_pi_esatto": 0,
                  "somma_dipolo": 0.0, "calcio_somma": 0.0, "calcio_n": 0,
                  "nati_div": 0, "nati_sch": 0}

    # ------------------------------------------------------------ la scena
    def prepara(self, S, net):
        """Legge la geometria ### **DALLA SCENA**, non la assume *(lo chiede il mandato)*."""
        d = (getattr(S, "test", {}) or {}).get("dati", {}) or {}
        sc = d.get("scena_ii") or {}
        self.r_regione = float(sc["r_regione"])
        rc = float(sc["R_CONN"])
        self.u_bordo = 1.0 + rc / self.r_regione
        co = d.get("coorti") or {}
        self.coorti = [np.asarray(co["massa_%d" % k], int) for k in range(3)
                       if ("massa_%d" % k) in co]
        if len(self.coorti) != 3 or not self.r_regione:
            raise SystemExit("[FERMO] la scena non ha le TRE coorti o `r_regione`: %s"
                             % sorted(co))
        return {"r_regione": self.r_regione, "R_CONN": rc, "u_bordo": self.u_bordo,
                "sep": float(sc.get("sep", -1)),
                "raggio_vuoto": float(sc.get("raggio_vuoto", -1)),
                "n_coorti": [int(x.size) for x in self.coorti]}

    def _u(self, net, idx):
        """`u` = distanza dal BARICENTRO della coorte piu' vicina, in unita' di `r_regione`.

        ### **Il baricentro si ricalcola a OGNI passo**: la scena definisce la regione come
        un insieme di INDICI, e ### **le masse possono muoversi** -- che e' la prima delle
        tre prove di Luca. ### **`r_regione` resta quello della scena**, perche'
        ricalcolarlo farebbe deriva alla classe insieme alla misura.
        """
        pos = np.asarray(net.pos, float)
        idx = np.asarray(idx, int)
        if idx.size == 0:
            return np.zeros(0), np.zeros((0, 3))
        cen = []
        for c in self.coorti:
            c = c[c < len(pos)]
            cen.append(pos[c].mean(axis=0) if c.size else np.array([np.nan] * 3))
        cen = np.asarray(cen, float)
        d = np.stack([np.linalg.norm(pos[idx] - cen[k], axis=1) for k in range(len(cen))])
        return np.nanmin(d, axis=0) / self.r_regione, cen

    def _grandezze(self, net, idx):
        """Le grandezze del punto `E` per un insieme di nodi. ### **SOLA LETTURA.**"""
        idx = np.asarray(idx, int)
        u, _c = self._u(net, idx)
        cl = classe(u, self.u_bordo)
        # ### ⛔ **`rho_spin` NON E' `|psi|^2`:** la riga `:1057` del simulatore registra come
        #   DIFETTO un `_rho_sorgente` che restituiva `|psi|^2` invece di `rho_spin`.
        #   ### **Registro ENTRAMBE**, perche' sceglierne una in silenzio rifarebbe quel
        #   difetto.
        rs = np.asarray(getattr(net, "rho_spin", []), float)
        ps = np.abs(np.asarray(getattr(net, "psi", []), complex)) ** 2
        med_rs = float(np.median(rs)) if rs.size else float("nan")
        med_ps = float(np.median(ps)) if ps.size else float("nan")
        try:
            rt = net.ritmo()
        except Exception:
            rt = None
        rt = (np.ones(net.n) if rt is None or len(rt) < net.n
              else np.asarray(rt, float)[:net.n])
        def _r(a, m):
            if a.size <= np.max(idx, initial=-1) or not np.isfinite(m) or m == 0:
                return np.full(idx.size, np.nan)
            return a[idx] / m
        return {"u": u, "classe": cl, "rho_spin_rel": _r(rs, med_rs),
                "psi2_rel": _r(ps, med_ps),
                "ritmo": rt[idx] if rt.size > np.max(idx, initial=-1) else
                         np.full(idx.size, np.nan)}

    # ------------------------------------------------------------ i ganci NUOVI
    def geom(self, net, twn, soglia):
        """### **GANCIO `E`: i nodi in cui il BASCULAMENTO cambia `perc_geom`.**

        ### ⛔ **E' `perc_geom`, NON `perc_chi`:** l'argv del driver ha `--chi-coop`, e con
        la cooperazione il basculamento scrive ### **la GEOMETRIA** mentre lo spinore scrive
        ### **la carica** *(`:7905`)*. ### **Contare `perc_chi` qui avrebbe misurato un ramo
        che in questa scena non viene mai eseguito.**

        ### ⛔ **E NON si <<ribalta>>: `perc_geom` e' RICALCOLATO da zero a ogni passo**,
        quindi un nodo *«cambia»* quando ### **ATTRAVERSA** la soglia, in un verso o
        nell'altro. Il gancio ricalcola `where(twn > soglia, 1, -1)` e lo confronta col
        corrente: ### **non scrive niente.**
        """
        nuovo = np.where(np.asarray(twn, float) > float(soglia), 1, -1)
        vecchio = np.asarray(net.perc_geom, int)[:net.n]
        k = min(len(nuovo), len(vecchio))
        camb = np.where(nuovo[:k] != vecchio[:k])[0]
        self.p["cambi_geom"] += int(camb.size)
        self.cont["cambi_geom_tot"] += int(camb.size)
        self._dove(net, camb, "geom")

    def chi_tors(self, net, chi_torsione):
        """### ⛔ **IL GANCIO CHE CONTA DAVVERO: `chi_torsione`, l'array che ENTRA nel
        dipolo.**

        L'argv del driver ha ### **`--chi-core` E `--chi-coop`**, quindi `chi_torsione` non e'
        ne' `perc_chi` ne' `perc_geom`: e' la ### **chiralita' CORE-LOCALE calcolata da
        `perc_geom`**, in cache in `_chi_geom_nodi` *(`:7849`-`:7855`)*.

        ### ✔ **E SI MISURA DOVE IL DIPOLO LO LEGGE, non da chi l'ha scritto:** cosi' il
        conto vale ### **qualunque** sia il flag che governa la cache, e non va rifatto se un
        giorno cambiasse. ### **E' la lezione del giro corto: avevo hookato lo scrittore
        SBAGLIATO, e contavo zero mentre il dipolo cambiava su 90854 archi.**
        """
        a = np.asarray(chi_torsione, float)
        pr = self._chi_prec
        self._chi_prec = a.copy()
        if pr is None or len(pr) != len(a):
            # ### il PRIMO passo, o un passo in cui `n` e' cambiato: ### **non si confronta**,
            #   e il contatore dice QUANTE volte e' successo invece di inventare uno zero.
            self.p["chi_tors_non_confrontabile"] = 1
            self.cont["chi_tors_non_confrontabili"] += 1
            # ### ✔ **SI SCRIVE `None` ESPLICITAMENTE, invece di contare sul reset di
            #   `chiudi`.** Il collaudo me l'ha mostrato: senza questa riga il valore restava
            #   ### **quello del passo PRIMA**, e in un ciclo dove `chiudi` non venisse
            #   chiamato -- o dove il gancio girasse due volte -- sarebbe ### **un valore
            #   VECCHIO presentato come quello di questo passo.** ### **Togliere una
            #   dipendenza e' meglio che fidarsi che sia rispettata.**
            self.p["cambi_chi_tors"] = None
            # ### ⛔ **E `cambi_chi_tors` RESTA `None`: NON MISURATO.** ### **Non si
            #   scrive `0`**, perche' uno zero qui sarebbe ### **indistinguibile da una
            #   misura** -- ed e' esattamente il difetto `CHI-TORS-ZERO-FALSO`.
            return
        camb = np.where(pr != a)[0]
        # ### OKX **ASSEGNA, non accumula:** il gancio gira ### **una volta per passo**, e
        #   un `+=` su `None` solleverebbe. ### **L'assegnazione e' anche piu' onesta:** dice
        #   *<<questo passo vale `k`>>* invece di *<<aggiungi `k` a quello che c'era>>*.
        self.p["cambi_chi_tors"] = int(camb.size)
        self.cont["cambi_chi_tors_tot"] += int(camb.size)
        self._dove(net, camb, "chi_tors")

    def _dove(self, net, camb, et):
        """Le grandezze del punto `E` per i nodi che cambiano. ### **SOLA LETTURA.**"""
        camb = np.asarray(camb, int)
        if camb.size == 0 or not self.u_bordo:
            return
        g = self._grandezze(net, camb)
        self.dove_chi.append({
            "passo": self.passo, "quale": et, "n_cambi": int(camb.size),
            "per_classe": [int(np.sum(g["classe"] == c)) for c in range(3)],
            "q_u": q(g["u"]), "q_rho_spin_rel": q(g["rho_spin_rel"]),
            "q_psi2_rel": q(g["psi2_rel"]), "q_ritmo": q(g["ritmo"])})

    def nati(self, net, via, k):
        """### **GANCI `F` e `G`: le nascite, e DOVE.**

        `self.n` e' una ### **proprieta'** *(`len(self.phi)`)*, quindi qui e' ### **gia'
        aggiornata** e i nodi nuovi sono gli ### **ULTIMI `k`.**
        """
        k = int(k)
        if k <= 0:
            return
        self.p["nati_div" if via == "divisione" else "nati_sch"] += k
        self.cont["nati_div_tot" if via == "divisione" else "nati_sch_tot"] += k
        if not self.u_bordo:
            return
        idx = np.arange(net.n - k, net.n)
        g = self._grandezze(net, idx)
        for z in range(k):
            self.dove_nascite.append({
                "passo": self.passo, "via": via, "nodo": int(idx[z]),
                "u": float(g["u"][z]), "classe": CLASSI[int(g["classe"][z])],
                "rho_spin_rel": float(g["rho_spin_rel"][z]),
                "psi2_rel": float(g["psi2_rel"][z]),
                "ritmo": float(g["ritmo"][z])})

    def calcio(self, net, ca, cb):
        """### **GANCIO `H`: il calcio di fase ai genitori** *(`KICK_TW`)*, somma dei moduli.

        ### ⛔ **`KICK_TW = 0.35`, non `~0.5`:** il mandato dice `~0.5` e il codice dice
        `0.35` *(`:617`)*. ### **Lo MISURO invece di assumerlo.**
        """
        a = np.abs(np.asarray(ca, float))
        b = np.abs(np.asarray(cb, float))
        self.p["calcio_somma"] += float(a.sum() + b.sum())
        self.p["calcio_n"] += int(a.size + b.size)

    # ------------------------------------------------------------ il gancio ESTESO
    def torsione(self, net, dph, twist_dip, twp, twp_dip, ttw, dt_e, r, i, j):
        """### **La decomposizione della spinta PER SORGENTE**, poi il gancio della misura
        lunga ### **invariato**.

        ### ✔ **Le due parti NON si stimano: sono SEPARATE PER COSTRUZIONE** nella legge
        curata, che somma `_w4(dph - _fp) + (twist_dip - _dp)`.
        """
        self.decomponi(dph, twist_dip, twp, twp_dip)
        LUNGA.Misura.torsione(self, net, dph, twist_dip, twp, twp_dip, ttw, dt_e, r, i, j)

    def decomponi(self, dph, twist_dip, twp, twp_dip):
        """La spinta, DIVISA PER SORGENTE. ### **Un metodo SUO perche' il collaudo possa
        chiamarlo** senza costruire una rete intera -- la lezione di `LUNGA-BATTITO-CADUTA`.

        ### ⛔ **E IL CONTATORE DELLA SPINTA ESATTAMENTE `pi` NON E' UN DETTAGLIO:** un
        nodo che ribalta la chiralita' su ### **UN SOLO estremo** cambia `twist_dip` di
        ### **`pi` ESATTO**, quindi la spinta vale `pi` e ### **`> pi` NON la conta.**
        ### **Cioe' il criterio del mandato, preso alla lettera, mancherebbe PROPRIO il
        meccanismo del guardiano quando la fase e' nulla.** Il criterio ### **resta
        `> pi`** -- era fissato prima -- ma il contatore `spinta_pi_esatto` rende
        ### **VISIBILE** l'accumulo al bordo invece di lasciarlo cadere in silenzio.
        """
        d = np.asarray(dph, float)
        td = np.asarray(twist_dip, float) * np.ones_like(d)
        tp = np.asarray(twp, float)
        tdp = np.asarray(twp_dip, float)
        nuovo = np.isnan(tdp)
        fp = np.where(nuovo, d, tp)
        dp = np.where(nuovo, td, tdp)
        fase = LUNGA._w4(d - fp)
        dip = td - dp
        sp = np.abs(fase + dip)
        oltre = sp > math.pi
        f_oltre = np.abs(fase) > math.pi
        d_oltre = np.abs(dip) > 0.0
        self.p["spinta_pi_tot"] += int(np.sum(oltre))
        self.p["spinta_pi_fase"] += int(np.sum(oltre & f_oltre & ~d_oltre))
        self.p["spinta_pi_dip"] += int(np.sum(oltre & d_oltre & ~f_oltre))
        self.p["spinta_pi_entrambe"] += int(np.sum(oltre & f_oltre & d_oltre))
        self.p["spinta_pi_esatto"] += int(np.sum(np.abs(sp - math.pi) <= 1e-9))
        self.p["somma_dipolo"] += float(np.abs(dip).sum())
        return {"fase": fase, "dip": dip, "spinta": sp}

    # ------------------------------------------------------------ la chiusura del passo
    def chiudi(self, net):
        LUNGA.Misura.chiudi(self, net)
        d = self.passi[-1]
        # ### ⛔ **`perc_chi` E' QUELLO CHE IL MANDATO NOMINA, e si conta -- ma in questa
        #   scena NON E' QUELLO CHE ENTRA NEL DIPOLO.** Lo registro ### **a parte** e lo
        #   dichiaro, invece di far passare un numero per un altro.
        pc = np.asarray(getattr(net, "perc_chi", []), int)[:net.n]
        if self._perc_chi_prec is not None and len(self._perc_chi_prec) == len(pc):
            self.p["cambi_perc_chi"] = int(np.sum(self._perc_chi_prec != pc))
            self.cont["cambi_perc_chi_tot"] += self.p["cambi_perc_chi"]
        self._perc_chi_prec = pc.copy()
        d.update(dict(self.p))
        for k in ("spinta_pi_tot", "spinta_pi_fase", "spinta_pi_dip",
                  "spinta_pi_entrambe", "spinta_pi_esatto"):
            self.cont[k] += int(self.p[k])
        if self.u_bordo:
            # ### ⛔ **LE FRAZIONI DI NODI, a OGNI passo:** senza queste *«nascono nel
            #   vuoto»* direbbe soltanto *«il vuoto e' piu' grande»*. Lo dice il mandato.
            u, cen = self._u(net, np.arange(net.n))
            cl = classe(u, self.u_bordo)
            d["nodi_per_classe"] = [int(np.sum(cl == c)) for c in range(3)]
            d["fraz_nodi"] = [float(np.mean(cl == c)) for c in range(3)]
            d["nati_per_classe"] = [0, 0, 0]
            d["nati_div_per_classe"] = [0, 0, 0]
            d["nati_sch_per_classe"] = [0, 0, 0]
            for z in self.dove_nascite:
                if z["passo"] == self.passo:
                    c = CLASSI.index(z["classe"])
                    d["nati_per_classe"][c] += 1
                    d["nati_div_per_classe" if z["via"] == "divisione"
                      else "nati_sch_per_classe"][c] += 1
            # ### un PRODOTTO LATERALE che non costa niente e serve alla prima delle tre
            #   prove di Luca: le distanze fra i baricentri delle tre masse.
            if cen is not None and len(cen) == 3 and np.all(np.isfinite(cen)):
                d["dist_baricentri"] = [float(np.linalg.norm(cen[a] - cen[b]))
                                        for a, b in ((0, 1), (1, 2), (0, 2))]
        self._azzera_passo()
        return d

    def piena_dove(self, net):
        """Ai passi `300`, `600`, `1000`: la popolazione degli archi con `|tw| >= 4π`.

        ### ⛔ **SOLO COME POPOLAZIONE -- distribuzioni, MAI indici:** `ARCHI-OLTRE-4PI` e'
        ### **<<da non indagare>> per decisione di Luca**, e il mandato lo ripete.
        """
        if not self.u_bordo:
            return
        tw = np.abs(np.asarray(net.tw, float))
        sel = np.where(tw >= P4)[0]
        if sel.size == 0:
            self.dove_sopra4pi[self.passo] = {"n": 0}
            return
        nodi = np.unique(np.concatenate([np.asarray(net.i)[sel],
                                         np.asarray(net.j)[sel]]))
        g = self._grandezze(net, nodi)
        self.dove_sopra4pi[self.passo] = {
            "n": int(sel.size), "n_nodi": int(nodi.size),
            "per_classe": [int(np.sum(g["classe"] == c)) for c in range(3)],
            "q_u": q(g["u"]), "q_rho_spin_rel": q(g["rho_spin_rel"]),
            "q_psi2_rel": q(g["psi2_rel"]), "q_ritmo": q(g["ritmo"]),
            "q_tw_sopra": q(tw[sel])}

    def finestre_dove(self):
        """Il DOVE per finestre di `100` passi: la frazione di ### **nascite** in ciascuna
        classe ### **contro** la frazione di ### **nodi.**"""
        out = []
        for a in range(0, len(self.passi), FINESTRA_DOVE):
            bl = self.passi[a:a + FINESTRA_DOVE]
            if not bl:
                continue
            nat = [sum(x.get("nati_per_classe", [0, 0, 0])[c] for x in bl)
                   for c in range(3)]
            dv = [sum(x.get("nati_div_per_classe", [0, 0, 0])[c] for x in bl)
                  for c in range(3)]
            sc = [sum(x.get("nati_sch_per_classe", [0, 0, 0])[c] for x in bl)
                  for c in range(3)]
            tot = float(sum(nat))
            fn = [float(np.mean([x.get("fraz_nodi", [0, 0, 0])[c] for x in bl]))
                  for c in range(3)]
            out.append({
                "da": bl[0]["passo"], "a": bl[-1]["passo"], "nascite": int(tot),
                "per_classe": nat, "divisioni_per_classe": dv,
                "schwinger_per_classe": sc,
                "fraz_nascite": [(n / tot if tot else None) for n in nat],
                "fraz_nodi": fn,
                # ### il RAPPORTO e' la grandezza del criterio: >= 2 = SOVRARAPPRESENTATA
                "rapporto": [((n / tot) / f if tot and f else None)
                             for n, f in zip(nat, fn)]})
        return out


def _scrivi(d, nome):
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    io.open(os.path.join(FUORI, nome), "w", encoding="utf-8").write(
        json.dumps(d, indent=1, default=str))


def main(argv):
    passi, amp, ganci = PASSI, None, True
    for a in argv[1:]:
        if a.startswith("--passi="):
            passi = int(a.split("=", 1)[1])
        elif a.startswith("--amp="):
            amp = float(a.split("=", 1)[1])
        elif a == "--senza-ganci":
            ganci = False
    if "--collaudo" in argv[1:]:
        return collaudo()
    if amp is None:
        stampa("### SERVE `--amp=0.0` o `--amp=0.3`. MI FERMO: l'ampiezza NON ha un default,")
        stampa("    perche' un default qui vorrebbe dire scegliere il braccio in silenzio.")
        return 1
    nome = "amp%s%s.json" % (("%g" % amp).replace(".", "_"),
                             "" if ganci else "_senza_ganci")
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    riga("=")
    stampa("IL `0.3` A ZERO E IL DOVE -- `_AMP = %r`, %d passi, UN braccio%s"
           % (amp, passi, "" if ganci else "   (SENZA i ganci nuovi: C-letture)"))
    riga("=")
    pf = piattaforma()
    for k in ["python", "numpy", "sistema", "macchina"]:
        stampa("  %-10s %s" % (k, pf[k]))
    b = blob(SIM)[:8]
    stampa("  simulatore %s   atteso %s   strumento %s   _tors_w8_lunga %s"
           % (b, BLOB_ATTESO, blob(__file__)[:8], blob(LUNGA.__file__)[:8]))
    if b != BLOB_ATTESO:
        stampa("  ### IL BLOB DEL SIMULATORE NON E' QUELLO ATTESO. MI FERMO.")
        _scrivi({"esito": 1, "stato": "BLOB SBAGLIATO", "blob_trovato": b,
                 "blob_atteso": BLOB_ATTESO, "piattaforma": pf}, nome)
        return 1
    stampa("  ### il blob COINCIDE: la misura vale per questo simulatore.")
    stampa()
    dst = os.path.join(FUORI, "_sim_%s.py" % nome.replace(".json", ""))
    anc = copia_patchata(SIM, dst, amp, ganci=ganci)
    stampa("  la copia patchata: blob %s  (%d ancore)" % (blob(dst)[:8], len(anc)))
    for a in anc:
        stampa("      %s" % a)
    stampa()
    S, N, _a = carica("mzd_%s" % nome.replace(".json", ""), dst)
    m = Misura(S.DT, amp)
    S._MIS = m
    sc = m.prepara(S, N)
    in_conf = _cli_flag.dichiara_configurazione(S, stampa)
    stampa("  scena: n = %d, archi = %d, DT = %r" % (N.n, len(N.i), S.DT))
    stampa("  LA GEOMETRIA, letta DALLA SCENA: r_regione %.6f  R_CONN %.6f  u_bordo %.4f"
           % (sc["r_regione"], sc["R_CONN"], sc["u_bordo"]))
    stampa("  le tre coorti: %s nodi" % sc["n_coorti"])
    stampa()
    riga("=")
    stampa("LA CORSA")
    riga("=")

    def _ist(stato, k, err=None):
        d = {"piattaforma": pf, "passi": passi, "passi_girati": k, "stato": stato,
             "amp": amp, "ganci": ganci, "blob_sim": blob(SIM),
             "blob_atteso": BLOB_ATTESO, "blob_strumento": blob(__file__),
             "blob_tors_w8_lunga": blob(LUNGA.__file__), "blob_copia": blob(dst),
             "ancore": anc, "scena": sc, "finestra_dove": FINESTRA_DOVE,
             "passi_pieni": list(PASSI_PIENI), "classi": list(CLASSI),
             "in_configurazione_del_driver": in_conf,
             "passi_dati": m.passi, "piene": m.piene,
             "dove_nascite": m.dove_nascite, "dove_chi": m.dove_chi,
             "dove_sopra4pi": m.dove_sopra4pi,
             "finestre_dove": m.finestre_dove(),
             "nascite_per_finestra": m.nascite_per_finestra(),
             "totali": m.totali(), "a_valle": {"n": int(N.n), "archi": int(len(N.i))}}
        if err is not None:
            d["errore"] = err
        _scrivi(d, nome)
        return d

    for k in range(1, passi + 1):
        m.passo = k
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                _passo.passo_pieno(S, N)
            m.chiudi(N)
            if k in PASSI_PIENI:
                m.piena_dove(N)
            u = m.passi[-1]
            print("[battito] passo %d/%d  n=%d archi=%d  div=%d sch=%d  |tw| q50=%.4f  "
                  "sopra4pi=%d  chiT=%s  pi:f=%d d=%d e=%d  nodi=%s"
                  % (k, passi, u["n"], u["archi"], m.cont["nati_div_tot"],
                     m.cont["nati_sch_tot"],
                     (u.get("q_tw") or {}).get("q050", float("nan")),
                     u.get("sopra_4pi", -1),
                     # ### ⛔ **<<n/m>> e NON `-1`:** un numero di ripiego si confonde
                     #   con una misura, una parola no.
                     ("n/m" if u.get("cambi_chi_tors") is None
                      else u["cambi_chi_tors"]),
                     u.get("spinta_pi_fase", -1), u.get("spinta_pi_dip", -1),
                     u.get("spinta_pi_entrambe", -1),
                     u.get("nodi_per_classe")), flush=True)
            if k % PASSI_SALVA == 0:
                _ist("IN CORSO", k)
        except Exception as e:
            import traceback
            _tb = traceback.format_exc()
            _reg = len(m.passi)
            stampa("### LA CORSA E' CADUTA AL PASSO %d: %r" % (k, e))
            stampa(_tb)
            stampa("### I PASSI REGISTRATI SONO %d, e si salvano." % _reg)
            try:
                _ist("CADUTA al passo %d" % k, _reg,
                     err={"passo": k, "errore": repr(e), "traccia": _tb,
                          "passi_registrati": _reg})
            except Exception as e2:
                stampa("### ⛔ E IL SALVATAGGIO E' CADUTO ANCHE LUI: %r" % (e2,))
                stampa(traceback.format_exc())
            return 1
    _ist("fatto", passi)
    stampa("  ### I DATI SONO SALVATI in %s." % nome)
    stampa()
    riga("=")
    stampa("I NUMERI, in breve -- IL REFERTO LO SCRIVE IL GENERATORE, dal json")
    riga("=")
    t = m.totali()
    stampa("  divisioni %d   Schwinger %d   nati %d"
           % (m.cont["nati_div_tot"], m.cont["nati_sch_tot"], t.get("nati_tot")))
    _pn = [x["passo"] for x in m.dove_nascite]
    stampa("  la PRIMA nascita: passo %s" % (min(_pn) if _pn else "MAI"))
    stampa("  cambi di chi_torsione (QUELLO CHE ENTRA NEL DIPOLO), somma: %d"
           % m.cont["cambi_chi_tors_tot"])
    stampa("  cambi di perc_geom (il basculamento), somma: %d" % m.cont["cambi_geom_tot"])
    stampa("  cambi di perc_chi (quello che il mandato NOMINA, e NON entra nel dipolo"
           " in questa scena), somma: %d" % m.cont["cambi_perc_chi_tot"])
    stampa("  passi in cui chi_torsione NON era confrontabile: %d"
           % m.cont["chi_tors_non_confrontabili"])
    stampa("  spinta oltre pi: tot %d   fase %d   dipolo %d   entrambe %d"
           % (m.cont["spinta_pi_tot"], m.cont["spinta_pi_fase"],
              m.cont["spinta_pi_dip"], m.cont["spinta_pi_entrambe"]))
    stampa("  archi sopra 4pi, somma su tutti i passi: %d" % m.cont["sopra_4pi_tot"])
    stampa()
    return 0


# =============================================================== IL COLLAUDO
def collaudo():
    esiti = []

    def prova(nome, ok, dett=""):
        esiti.append((nome, bool(ok), dett))
        stampa("  %-7s %-76s %s" % ("OK" if ok else "FALLITA", nome, dett))

    import inspect as _insp0
    riga("=")
    stampa("IL COLLAUDO DI _mitosi_zero_dove.py")
    riga("=")

    # ---------------------------------------------- 1. le ancore
    import tempfile
    _d = tempfile.mkdtemp()
    orig = io.open(SIM, encoding="utf-8", newline="").read()
    for amp in (0.0, 0.3):
        p = os.path.join(_d, "s%g.py" % amp)
        anc = copia_patchata(SIM, p, amp)
        t = io.open(p, encoding="utf-8", newline="").read()
        # ### 3 della misura lunga + `_AMP` + soglia + i 5 ganci nuovi = DIECI.
        #   ### **Avevo scritto OTTO, poi NOVE: il collaudo mi ha corretto DUE volte**, la
        #   seconda quando il giro corto ha mostrato che serviva il gancio su
        #   ### **`chi_torsione`.**
        prova("ancore: ### con `_AMP = %r` sono DIECI, tutte UNICHE" % amp, len(anc) == 10,
              "%d" % len(anc))
        prova("ancore: ### `_AMP = %r` e' nel sorgente patchato" % amp,
              ("_AMP = %r" % amp) in t)
        prova("ancore: ### la soglia usa `_AMP`, e il `0.3` cablato NON c'e' piu'",
              "(1.0 - _AMP * np.tanh(grad_modula))" in t
              and "(1.0 - 0.3 * np.tanh(grad_modula))" not in t)
        # ### togliendo le sole righe INIETTATE si torna al sorgente VERO, carattere per
        #   carattere: e' il controllo che la patch non abbia toccato altro.
        # ### ⛔ **E SI FA PER RIGHE INTERE, NON CON `replace` SU STRINGHE:** la prima
        #   versione cancellava `"        if _MIS is not None:"` *(otto spazi)*, che e'
        #   ### **una SOTTOSTRINGA** della riga a dodici spazi -- e lasciava indietro
        #   ### **quattro spazi per ognuna.** ### **Scarto misurato: 8 caratteri**, e il
        #   collaudo l'ha preso. ### **Un confronto per RIGHE non ha quel modo di
        #   sbagliare.**
        _inj = set(["_MIS = None   # [TORS-W8 LUNGA] lo riempie lo strumento",
                    "_AMP = %r   # [MITOSI-ZERO] l'ampiezza della modulazione, INIETTATA"
                    % amp,
                    "            if _MIS is not None:",
                    "                _MIS.torsione(self, dph=dph, twist_dip=twist_dip,",
                    "                              twp=self.twp, twp_dip=self.twp_dip,",
                    "                              ttw=_ttw, dt_e=dt_e, r=r, i=i, j=j)",
                    "        if _MIS is not None:",
                    "            _MIS.catena(self, avv=avv, soglia=soglia, segno=segno,",
                    "                        prob=prob, nasce=nasce)",
                    "                if _MIS is not None:",
                    "                    _MIS.geom(self, twn, soglia)",
                    "                    _MIS.chi_tors(self, chi_torsione)",
                    "            _MIS.nati(self, 'divisione', len(sel))",
                    "                    _MIS.nati(self, 'schwinger', int(nc))",
                    "                _MIS.calcio(self, calcio_a, calcio_b)"])
        _rig = [x for x in t.split(NL) if x not in _inj]
        rip = NL.join(_rig).replace("(1.0 - _AMP * np.tanh(grad_modula))",
                                    "(1.0 - 0.3 * np.tanh(grad_modula))")
        prova("ancore: ### togliendo le SOLE righe iniettate si torna al sorgente VERO",
              rip == orig, "%d caratteri di scarto" % abs(len(rip) - len(orig)))
    p0 = os.path.join(_d, "sg.py")
    anc0 = copia_patchata(SIM, p0, 0.3, ganci=False)
    t0 = io.open(p0, encoding="utf-8", newline="").read()
    prova("ancore: ### `--senza-ganci` ne applica solo CINQUE (le 3 lunghe + `_AMP` + soglia)",
          len(anc0) == 5, "%d" % len(anc0))
    prova("ancore: ### DEVE TACERE -- senza ganci NON c'e' nessuno dei cinque nuovi",
          all(x not in t0 for x in ("_MIS.geom(", "_MIS.chi_tors(", "_MIS.nati(",
                                    "_MIS.calcio(")))
    prova("ancore: ### ma la soglia usa `_AMP` anche senza ganci (serve a C-letture)",
          "(1.0 - _AMP * np.tanh(grad_modula))" in t0)

    # ---------------------------------------------- 2. la classe, DERIVATA
    ub = 1.0 + 2.4 / 4.096438
    prova("classe: ### `u_bordo = 1 + R_CONN/r_regione` vale 1.5859, e viene dalla SCENA",
          abs(ub - 1.5859) < 1e-4, "%.6f" % ub)
    cl = classe(np.array([0.0, 0.5, 1.0, 1.0001, 1.5, ub, ub + 1e-9, 2.0, 3.0]), ub)
    prova("classe: ### `u <= 1` e' MATERIA, e l'UGUALE ci sta (e' il test della scena)",
          list(cl[:3]) == [0, 0, 0], "%s" % list(cl))
    prova("classe: ### DEVE FALLIRE -- `u = 1.0001` NON e' piu' MATERIA", cl[3] == 1)
    prova("classe: ### `u = u_bordo` e' ancora BORDO, e appena sopra e' VUOTO",
          cl[5] == 1 and cl[6] == 2)
    prova("classe: ### e `u = 2` e `u = 3` sono VUOTO", cl[7] == 2 and cl[8] == 2)
    prova("classe: ### le tre classi hanno i nomi del mandato",
          CLASSI == ("MATERIA", "BORDO", "VUOTO"))

    # ---------------------------------------------- 3. i ganci, su dati SINTETICI
    class _Net(object):
        pass

    m = Misura(0.01, 0.3)
    m.r_regione, m.u_bordo = 2.0, 1.5
    m.coorti = [np.array([0]), np.array([1]), np.array([2])]
    net = _Net()
    net.pos = np.array([[0.0, 0, 0], [10.0, 0, 0], [20.0, 0, 0],
                        [1.0, 0, 0], [13.0, 0, 0], [40.0, 0, 0]])
    net.n = 6
    net.perc_chi = np.array([1, 1, -1, -1, 1, 1])
    net.rho_spin = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    net.psi = np.array([1 + 0j] * 6)
    net.ritmo = lambda: np.ones(6)
    g = m._grandezze(net, np.array([0, 3, 4, 5]))
    prova("grandezze: ### `u` e' la distanza dal baricentro piu' vicino / r_regione",
          abs(g["u"][0] - 0.0) < 1e-12 and abs(g["u"][1] - 0.5) < 1e-12,
          "%s" % np.round(g["u"], 4).tolist())
    prova("grandezze: ### e la classe segue: MATERIA, MATERIA, BORDO, VUOTO",
          list(g["classe"]) == [0, 0, 1, 2], "%s" % list(g["classe"]))
    prova("grandezze: ### `rho_spin` e `|psi|^2` sono DUE grandezze, non una",
          "rho_spin_rel" in g and "psi2_rel" in g)
    # ### ⛔ **IL GANCIO E' SU `perc_geom`, NON SU `perc_chi`:** l'argv del driver ha
    #   `--chi-coop`, e il ramo che scrive `perc_chi` ### **in questa scena NON GIRA.**
    net.perc_geom = np.array([1, 1, -1, -1, 1, 1])
    m.passo = 7
    m.geom(net, np.array([3.0, 3.0, 3.0, 1.0, 1.0, 1.0]), 2.0)
    prova("geom: ### conta i nodi che ATTRAVERSANO la soglia, nei DUE versi",
          m.p["cambi_geom"] == 3,
          "atteso 3 (il nodo 2 sale a +1, i nodi 4 e 5 scendono a -1); avuto %d"
          % m.p["cambi_geom"])
    m2 = Misura(0.01, 0.3)
    m2.r_regione, m2.u_bordo, m2.coorti = 2.0, 1.5, m.coorti
    m2.passo = 7
    m2.geom(net, np.where(net.perc_geom > 0, 3.0, 1.0), 2.0)
    prova("geom: ### DEVE TACERE -- se il segno non cambia, ZERO cambi",
          m2.p["cambi_geom"] == 0, "%d" % m2.p["cambi_geom"])
    prova("geom: ### e NON SCRIVE: `perc_geom` e' quello di prima",
          list(net.perc_geom) == [1, 1, -1, -1, 1, 1])
    prova("geom: ### DEVE ESSERE SU `perc_geom`: il sorgente NON legge `perc_chi` qui",
          "net.perc_geom" in _insp0.getsource(Misura.geom)
          and "net.perc_chi" not in _insp0.getsource(Misura.geom))
    # ### ⛔ **E IL GANCIO CHE CONTA DAVVERO: `chi_tors`**, che confronta `chi_torsione`
    #   fra due passi -- ### **l'array che ENTRA nel dipolo**, qualunque flag l'abbia scritto.
    m7 = Misura(0.01, 0.3)
    m7.r_regione, m7.u_bordo, m7.coorti = 2.0, 1.5, m.coorti
    m7.passo = 1
    m7.chi_tors(net, np.array([1.0, 1.0, -1.0, -1.0, 1.0, 1.0]))
    prova("chi_tors: ### al PRIMO passo NON confronta, e lo DICE invece di dire zero",
          m7.p["chi_tors_non_confrontabile"] == 1
          and m7.p["cambi_chi_tors"] is None,
          "non confrontabili: %d, valore %r"
          % (m7.cont["chi_tors_non_confrontabili"], m7.p["cambi_chi_tors"]))
    # ### STOPX **LA CURA DI `CHI-TORS-ZERO-FALSO`** *(2026-10-06, decisione di Luca)*: dove
    #   il gancio ### **non ha potuto misurare** il contatore vale ### **`None`**, non `0`.
    prova("chi_tors: ### CURA -- dove non misura il contatore e' `None`, NON `0`",
          m7.p["cambi_chi_tors"] is None and m7.p["cambi_chi_tors"] != 0,
          "%r" % m7.p["cambi_chi_tors"])
    m7.passo = 2
    m7.chi_tors(net, np.array([1.0, -1.0, -1.0, 1.0, 1.0, 1.0]))
    prova("chi_tors: ### DEVE ACCENDERSI -- al secondo passo conta i DUE che sono cambiati",
          m7.p["cambi_chi_tors"] == 2, "%d" % m7.p["cambi_chi_tors"])
    m7.passo = 3
    m7.p["cambi_chi_tors"] = 0
    m7.chi_tors(net, np.array([1.0, -1.0, -1.0, 1.0, 1.0, 1.0]))
    prova("chi_tors: ### DEVE TACERE -- se `chi_torsione` non cambia, ZERO",
          m7.p["cambi_chi_tors"] == 0, "%d" % m7.p["cambi_chi_tors"])
    # ### IL CASO COSTRUITO: la LUNGHEZZA cambia, come quando NASCONO NODI.
    m7.passo = 4
    m7.chi_tors(net, np.array([1.0, -1.0, -1.0]))
    prova("chi_tors: ### e se la LUNGHEZZA cambia non confronta, e lo conta",
          m7.cont["chi_tors_non_confrontabili"] == 2,
          "%d" % m7.cont["chi_tors_non_confrontabili"])
    prova("chi_tors: ### e in quel passo il contatore e' `None`, non `0`",
          m7.p["cambi_chi_tors"] is None, "%r" % m7.p["cambi_chi_tors"])
    # ### ⛔ **IL CASO CHE DEVE FALLIRE CON LA FORMA VECCHIA.** La forma vecchia lasciava
    #   `0`; il controllo qui sotto ### **distingue `0` da `None`**, quindi ### **con la
    #   forma vecchia FALLIREBBE.** ### **Lo si prova DAVVERO**, ricostruendo la forma
    #   vecchia a mano invece di affermare che fallirebbe.
    def _vecchia(mm):
        """La forma VECCHIA: dove non misura, lascia `0`."""
        mm.p["cambi_chi_tors"] = 0
        return mm.p["cambi_chi_tors"] is None

    m8 = Misura(0.01, 0.3)
    m8.r_regione, m8.u_bordo, m8.coorti = 2.0, 1.5, m.coorti
    m8.passo = 1
    m8.chi_tors(net, np.array([1.0, 1.0, -1.0, -1.0, 1.0, 1.0]))
    prova("chi_tors: ### DEVE FALLIRE CON LA FORMA VECCHIA -- con `0` il controllo NON passa",
          _vecchia(m8) is False and m8.p["cambi_chi_tors"] == 0,
          "la forma vecchia da' %r, e il controllo la RESPINGE" % m8.p["cambi_chi_tors"])
    # ### e la prova che il DANNO era reale: una serie con `0` e una con `None` danno due
    #   medie DIVERSE, e la prima e' quella sbagliata.
    _serie_0 = [5, 0, 7, 0, 9, 0]
    _serie_n = [5, None, 7, None, 9, None]
    _m0 = sum(_serie_0) / float(len(_serie_0))
    _buoni = [x for x in _serie_n if x is not None]
    _mn = sum(_buoni) / float(len(_buoni))
    prova("chi_tors: ### e il DANNO era reale -- con gli zeri la media e' %.2f invece di %.2f"
          % (_m0, _mn), abs(_m0 - _mn) > 1e-9 and _m0 < _mn,
          "gli zeri ABBASSANO la media del %.0f %%" % (100 * (1 - _m0 / _mn)))
    # ### il gancio `nati`: gli ULTIMI `k` indici
    m.dove_nascite = []
    m.nati(net, "divisione", 2)
    prova("nati: ### i nodi nuovi sono gli ULTIMI `k` (n=6, k=2 -> 4 e 5)",
          [z["nodo"] for z in m.dove_nascite] == [4, 5],
          "%s" % [z["nodo"] for z in m.dove_nascite])
    prova("nati: ### e la via si distingue", all(z["via"] == "divisione"
                                                 for z in m.dove_nascite))
    m.nati(net, "schwinger", 1)
    prova("nati: ### Schwinger e divisione sono contate SEPARATE",
          m.p["nati_div"] == 2 and m.p["nati_sch"] == 1)
    # ### il gancio `calcio`
    m.calcio(net, np.array([0.1, -0.2]), np.array([0.3, -0.4]))
    prova("calcio: ### somma i MODULI, non i valori", abs(m.p["calcio_somma"] - 1.0) < 1e-12,
          "%.6f" % m.p["calcio_somma"])

    # ---------------------------------------------- 4. la decomposizione della spinta
    m3 = Misura(0.01, 0.3)
    m3.passo = 1
    # ### QUATTRO archi, uno per caso. ### **`decomponi` si chiama DIRETTAMENTE**, senza
    #   costruire una rete intera: e' la ragione per cui e' un metodo suo.
    #   fase sola       `dph - twp = 4.0 > pi`, dipolo IDENTICO
    #   dipolo solo     `dph = twp`, e il dipolo va da `-pi` a `+pi`, cioe' ### **2 pi**
    #   entrambe        tutte e due
    #   nessuna delle due
    dph = np.array([4.0, 0.0, 4.0, 0.0])
    tdp_prec = np.array([0.0, -math.pi, -math.pi, 0.0])
    td = np.array([0.0, math.pi, math.pi, 0.0])
    twp = np.array([0.0, 0.0, 0.0, 0.0])
    try:
        _dec = m3.decomponi(dph, td, twp, tdp_prec)
        _e = None
    except Exception as _x:
        _dec, _e = None, repr(_x)
    prova("spinta: ### `decomponi` si chiama DA SOLO, senza una rete, e NON solleva",
          _e is None, _e or "")
    prova("spinta: ### e torna le due parti SEPARATE, piu' la spinta",
          bool(_dec) and sorted(_dec) == ["dip", "fase", "spinta"])
    prova("spinta: ### la FASE sola e' contata come fase", m3.p["spinta_pi_fase"] == 1,
          "%d" % m3.p["spinta_pi_fase"])
    prova("spinta: ### il DIPOLO solo e' contato come dipolo", m3.p["spinta_pi_dip"] == 1,
          "%d" % m3.p["spinta_pi_dip"])
    prova("spinta: ### ENTRAMBE e' contato a parte", m3.p["spinta_pi_entrambe"] == 1,
          "%d" % m3.p["spinta_pi_entrambe"])
    prova("spinta: ### e la somma delle tre e' il totale oltre pi",
          m3.p["spinta_pi_fase"] + m3.p["spinta_pi_dip"] + m3.p["spinta_pi_entrambe"]
          == m3.p["spinta_pi_tot"], "%d" % m3.p["spinta_pi_tot"])
    prova("spinta: ### DEVE TACERE -- il quarto arco (niente fase, niente dipolo) NON conta",
          m3.p["spinta_pi_tot"] == 3, "%d" % m3.p["spinta_pi_tot"])
    # ### ⛔ **IL BORDO ESATTO A `pi`, e il collaudo me l'ha fatto trovare:** un
    #   ribaltamento su UN SOLO estremo da' `Delta dipolo = pi` ESATTO, quindi la spinta
    #   vale `pi` e ### **`> pi` NON la conta** -- cioe' il criterio mancherebbe PROPRIO il
    #   meccanismo del guardiano quando la fase e' nulla.
    m5 = Misura(0.01, 0.3)
    m5.passo = 1
    _d5 = m5.decomponi(np.array([0.0]), np.array([math.pi]), np.array([0.0]),
                       np.array([0.0]))
    prova("spinta: ### un ribaltamento su UN estremo da' spinta `pi` ESATTA",
          abs(_d5["spinta"][0] - math.pi) < 1e-12, "%.12f" % _d5["spinta"][0])
    prova("spinta: ### e `> pi` NON la conta: il criterio del mandato la MANCA",
          m5.p["spinta_pi_tot"] == 0, "%d" % m5.p["spinta_pi_tot"])
    prova("spinta: ### DEVE ACCENDERSI -- `spinta_pi_esatto` la VEDE, e per questo esiste",
          m5.p["spinta_pi_esatto"] == 1, "%d" % m5.p["spinta_pi_esatto"])
    m6 = Misura(0.01, 0.3)
    m6.passo = 1
    m6.decomponi(np.array([0.0]), np.array([0.0]), np.array([0.0]), np.array([0.0]))
    prova("spinta: ### DEVE TACERE -- senza spinta, `spinta_pi_esatto` e' ZERO",
          m6.p["spinta_pi_esatto"] == 0, "%d" % m6.p["spinta_pi_esatto"])
    # ### e il gancio VERO chiama `decomponi`: altrimenti le prove qui sopra proverebbero
    #   un metodo che nessuno usa.
    import inspect as _insp
    prova("spinta: ### e il gancio `torsione` CHIAMA `decomponi` (non un metodo morto)",
          "self.decomponi(" in _insp.getsource(Misura.torsione))
    prova("spinta: ### e `somma_dipolo` e' la somma dei MODULI di Delta dipolo",
          abs(m3.p["somma_dipolo"] - 4 * math.pi) < 1e-9, "%.6f" % m3.p["somma_dipolo"])

    # ---------------------------------------------- 5. le finestre del DOVE
    m4 = Misura(0.01, 0.0)
    m4.r_regione, m4.u_bordo, m4.coorti = 2.0, 1.5, m.coorti
    for k in range(1, 201):
        m4.passi.append({"passo": k, "fraz_nodi": [0.1, 0.3, 0.6],
                         "nati_per_classe": [0, 2, 0] if k > 100 else [1, 0, 0],
                         "nati_div_per_classe": [0, 2, 0] if k > 100 else [1, 0, 0],
                         "nati_sch_per_classe": [0, 0, 0]})
    f = m4.finestre_dove()
    prova("finestre: ### due finestre da 100 passi", len(f) == 2 and f[0]["da"] == 1
          and f[1]["da"] == 101, "%s" % [(x["da"], x["a"]) for x in f])
    prova("finestre: ### il rapporto e' frazione di NASCITE / frazione di NODI",
          abs(f[1]["rapporto"][1] - (1.0 / 0.3)) < 1e-9,
          "%.4f" % f[1]["rapporto"][1])
    prova("finestre: ### e nella prima finestra la MATERIA e' sovrarappresentata 10x",
          abs(f[0]["rapporto"][0] - 10.0) < 1e-9, "%.4f" % f[0]["rapporto"][0])
    prova("finestre: ### DEVE TACERE -- una classe senza nascite ha rapporto ZERO, non None",
          f[1]["rapporto"][0] == 0.0, "%s" % f[1]["rapporto"][0])

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
