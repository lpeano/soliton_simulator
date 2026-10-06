# -*- coding: utf-8 -*-
"""IL TETTO DELLA TORSIONE: la soglia di mitosi `3pi` sta sul tetto?

Mandato di Luca del 2026-10-06. Previsioni, criteri e controlli sono fissati in
`doc/TASK_HISTORY/2026-10-06_tetto-torsione.md`, committato **prima** in `bbb2dda` e
annotato in `c3546e6`.

### ⛔ **IL SIMULATORE NON SI TOCCA.** Si gira una **COPIA** con due ganci di
### **SOLA LETTURA**: uno nel blocco della torsione di `step()`, uno in `decidi_divisione`.
`C0` **DIMOSTRA** che la copia e' byte-identica a `Bp` su tutti i conteggi e tutti i passi,
invece di lasciarlo dedurre.

### 📌 **DIPENDE DA `_mitosi_soglia_grad.py`** per `q`, `spearman`, `quintili`, `blob`,
`piattaforma` e `carica`. ### **E' una scelta, e la dichiaro:** duplicare la Spearman a
**ranghi medi** vorrebbe dire due copie della stessa legge che possono divergere *(par.9-ter)*.
### **Il suo blob entra nel `json`**, cosi' il numero resta attribuibile.

USO:  python csv/_test_fork/_tetto_torsione.py  [--passi=N]  [--collaudo]
"""
import contextlib
import io
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
sys.path.insert(0, _QUI)
import _presidio   # noqa: E402

_presidio.avvia(__file__)

import _passo                                    # noqa: E402
import _cli_flag                                 # noqa: E402
import _mitosi_soglia_grad as _MSG               # noqa: E402

q, spearman, quintili = _MSG.q, _MSG.spearman, _MSG.quintili
blob, piattaforma, carica = _MSG.blob, _MSG.piattaforma, _MSG.carica
stampa, riga, n4 = _MSG.stampa, _MSG.riga, _MSG.n4

NL = chr(10)
FUORI = os.path.join(RADICE, "csv", "_test_fork", "_tetto_torsione")
SIM = os.path.join(RADICE, "soliton_simulator.py")
CRESCITA = os.path.join(RADICE, "csv", "_test_fork", "_crescita_dopo_z43", "crescita.json")

PASSI = 150
PASSI_SALVA = 10
PASSI_MIS = (50, 100, 140)        # i passi della misura, FISSATI DAL MANDATO
# --- i criteri, FISSATI DAL MANDATO e non ritoccati
MEDIANA_M1 = (0.3, 2.0)           # fuori da qui -> l'ipotesi del TETTO e' REFUTATA
SOGLIA_M2 = 0.3                   # Spearman sotto a tutti e tre i passi -> REFUTATA
FRAZ_DIP0 = 0.30                  # meno del 30 % con twist_dip = 0 -> la SECONDA refutata
# --- le costanti della legge, LETTE e non scelte
P2 = 2.0 * np.pi
P3 = 3.0 * np.pi
P4 = 4.0 * np.pi
KAPPA = 1.0                       # ### `KAPPA-TW-COMMENTO`: il CODICE da' 1, il commento 3.1831
PAV_TAU = 1e-3                    # il pavimento ESTERNO di `_tau_tw_locale`
PAV_DOM = 1e-3                    # il pavimento DENTRO `dom`


def _w8(a):
    return (a + P4) % (2.0 * P4) - P4


def _w4(a):
    return (a + P2) % (2.0 * P2) - P2


# =============================================================== LA COPIA PATCHATA
def copia_patchata(sorgente, dst):
    """Due ganci di SOLA LETTURA. Le ancore si **CONTANO** e devono essere **UNICHE**
    *(`P1-quater`)*."""
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
        + "_MIS = None   # [TETTO-TORSIONE] lo riempie lo strumento" + NL,
        "il gancio di modulo `_MIS`")
    # ### IL GANCIO `A`: nel blocco della torsione, PRIMA dell'aggiornamento, cosi' `self.tw`
    #   e `self.twp` sono i valori di INGRESSO. ### **L'ancora e' di TRE righe** perche' la
    #   riga di `_ttw` da sola compare **due** volte (i due rami di `TORS_4PI`).
    uno("            _ttw = _tau_tw_locale(self) if TAU_LOCALI else TAU_TW" + NL
        + "            self.tw += self._w8(dph + twist_dip - self.twp)"
          " - dt_e * self.tw / _ttw" + NL
        + "            self.twp = self._w8(dph + twist_dip)" + NL,
        "            _ttw = _tau_tw_locale(self) if TAU_LOCALI else TAU_TW" + NL
        + "            if _MIS is not None:" + NL
        + "                _MIS.torsione(self, dph=dph, twp=self.twp," + NL
        + "                              twist_dip=twist_dip, ttw=_ttw, dt_e=dt_e," + NL
        + "                              dt_n=dt_n, r=r, dsync=delta_sync_phi, i=i, j=j)" + NL
        + "            self.tw += self._w8(dph + twist_dip - self.twp)"
          " - dt_e * self.tw / _ttw" + NL
        + "            self.twp = self._w8(dph + twist_dip)" + NL,
        "A: il blocco della torsione (ramo `TORS_4PI`), PRIMA dell'aggiornamento")
    # ### IL GANCIO `B`: la STESSA ancora di `_crescita_dopo_z43` e `_mitosi_soglia_grad`.
    uno("        c = np.where(nasce)[0]" + NL,
        "        if _MIS is not None:" + NL
        + "            _MIS.catena(self, avv=avv, soglia=soglia, segno=segno," + NL
        + "                        prob=prob, nasce=nasce)" + NL
        + "        c = np.where(nasce)[0]" + NL,
        "B: la catena dei cancelli di `decidi_divisione`")
    io.open(dst, "w", encoding="utf-8", newline=NL).write(t)
    return fatte


# =============================================================== LA MISURA
def tw_stella(r_i, r_j, w_i, w_j, kappa=KAPPA):
    """Il tetto di equilibrio, nella forma CHIUSA del mandato.

    `tw* = kappa*2pi*(r_i*w_i - r_j*w_j) / (r_medio*(|w_i - w_j| + 1e-3))`

    ### ✔ **E con `r` UNIFORME il `r` si CANCELLA:** `|tw*| -> 2pi*kappa` per qualunque arco
    a deriva costante. ### **Verificato nel collaudo, non asserito.**
    """
    rm = 0.5 * (r_i + r_j)
    dom = np.abs(w_i - w_j) + PAV_DOM
    return kappa * P2 * (r_i * w_i - r_j * w_j) / (rm * dom)


def tw_stella_fedele(r_i, r_j, w_i, w_j, dt, kappa=KAPPA):
    """Lo STESSO tetto, ma con `tau` come il codice lo calcola: col **pavimento esterno**.

    ### ⚠ **Differisce dalla forma chiusa SOLO dove il pavimento VINCOLA**, e la differenza
    ### **E' la misura `M8`.**
    """
    rm = 0.5 * (r_i + r_j)
    dom = np.abs(w_i - w_j) + PAV_DOM
    tau = np.maximum(kappa * P2 / dom, PAV_TAU)
    dte = dt * rm
    return dt * (r_i * w_i - r_j * w_j) * tau / dte


class Misura(object):
    """### **LEGGE: non ricalcola nessuna legge del simulatore.** Registra e misura."""

    def __init__(self, dt):
        self.dt = float(dt)
        self.passo = 0
        self.passi = []
        self._tor = None
        self._cat = None
        self._prec = None          # le COPIE di `r`, `phivel`, `dph`, `twist_dip` del passo t-1
        self.mis = {}              # passo -> M1..M8
        self.cont = {"passi_con_gancio": 0, "avvolgimenti": 0, "ripiegamenti": 0,
                     "calci_oltre_pi": 0, "coppie": 0, "twp_fuori_3pi": 0,
                     "pavimento_tau": 0, "archi_pavimento": 0}

    # ---------------------------------------------------------------- gancio A
    def torsione(self, net, dph, twp, twist_dip, ttw, dt_e, dt_n, r, dsync, i, j):
        i = np.asarray(i, int)
        j = np.asarray(j, int)
        dph = np.asarray(dph, float)
        twp = np.asarray(twp, float)
        td = np.asarray(twist_dip, float) * np.ones_like(dph)
        tw_in = np.asarray(net.tw, float)[:dph.size]
        pv = np.asarray(net.phivel, float)
        rr = (np.ones(net.n) if r is None else np.asarray(r, float))
        ds = np.asarray(dsync, float)
        dn = (np.ones(net.n) * self.dt if np.isscalar(dt_n)
              else np.asarray(dt_n, float))
        self.cont["passi_con_gancio"] += 1

        # ### L'INVARIANTE DERIVATO: |dph + twist_dip| <= 3pi, quindi `twp` NON avvolge MAI.
        #   ### **Si VERIFICA, non si assume** -- se fallisse, la derivazione del task history
        #   sarebbe falsa e il referto lo direbbe.
        self.cont["twp_fuori_3pi"] += int(np.sum(np.abs(twp) > P3 + 1e-9))

        D = dph + td
        arg = D - twp
        spinta = _w8(arg)
        d = {"n_archi": int(dph.size),
             "q_dph": q(np.abs(dph)), "q_twist_dip": q(np.abs(td)),
             "q_tw_ingresso": q(np.abs(tw_in)), "q_spinta": q(np.abs(spinta)),
             "q_ttw": q(np.asarray(ttw, float) * np.ones_like(dph)),
             "q_dt_e": q(np.asarray(dt_e, float) * np.ones_like(dph))}
        # ### `M5`: i cinque valori di `twist_dip` (perc_chi e' INTERO -> 0, +-pi/2, +-pi)
        at = np.abs(td)
        d["m5"] = {"n": int(at.size),
                   "fraz_zero": float(np.mean(at < 1e-12)),
                   "fraz_mezzo_pi": float(np.mean(np.abs(at - np.pi / 2) < 1e-9)),
                   "fraz_pi": float(np.mean(np.abs(at - np.pi) < 1e-9)),
                   "fraz_altro": float(np.mean((at >= 1e-12)
                                               & (np.abs(at - np.pi / 2) >= 1e-9)
                                               & (np.abs(at - np.pi) >= 1e-9)))}
        # ### `M8`: il pavimento ESTERNO di `tau` vincola?
        dom = np.abs(pv[i] - pv[j]) + PAV_DOM
        vinc = (KAPPA * P2 / dom) < PAV_TAU
        d["m8"] = {"n": int(dom.size), "vincolati": int(np.sum(vinc)),
                   "fraz": float(np.mean(vinc)), "dom_max": float(np.max(dom))}
        self.cont["archi_pavimento"] += int(np.sum(vinc))
        self.cont["pavimento_tau"] += int(np.any(vinc))
        # ### `M7`: il termine che la formula IGNORA, e che e' ATTIVO (`K_SYNC = 1.0`)
        avanz = dn[i] * pv[i] - dn[j] * pv[j]
        dsy = ds[i] - ds[j]
        _ok = np.abs(avanz) > 0
        d["m7"] = {"n": int(np.sum(_ok)),
                   "q_avanzamento": q(np.abs(avanz)), "q_dsync": q(np.abs(dsy)),
                   "q_rapporto": q(np.abs(dsy[_ok]) / np.abs(avanz[_ok]))
                   if np.any(_ok) else None}
        # ### `M7b`: IL SEGNO, che `M7` non vede perche' confronta MODULI.
        #   `delta_sync_phi = dt_n_s*forza*sin(media - _phi_t)` e' un termine di **Kuramoto**:
        #   ### **se RICHIAMA la fase verso la media locale, la sua differenza sull'arco si
        #   OPPONE a `dph`**, e allora ### **SMORZA la spinta invece di aggiungersi** -- e il
        #   tetto vero sta **sotto** `2pi`. ### ⚠ **Aggiunto DOPO il giro corto e PRIMA della
        #   corsa vera, perche' il giro corto ha mostrato che quel termine e' DOMINANTE
        #   (mediana del rapporto `1.79`).**
        _fin = np.isfinite(dsy) & np.isfinite(dph)
        d["m7b"] = {"n": int(np.sum(_fin)),
                    "spearman_dsync_dph": (spearman(dph[_fin], dsy[_fin])
                                           if np.sum(_fin) > 25 else None),
                    "fraz_segno_opposto": (float(np.mean((dsy[_fin] * dph[_fin]) < 0))
                                           if np.any(_fin) else None),
                    "q_prodotto": q(dsy[_fin] * dph[_fin]) if np.any(_fin) else None}

        # ### `M6`: GLI AVVOLGIMENTI, contati in DUE modi che devono coincidere
        if self._prec is not None and self._prec["n_archi"] == dph.size:
            dp0 = self._prec["dph"]
            td0 = self._prec["td"]
            salto = dph - dp0
            avvolto = np.abs(salto) > P2                 # un salto di ~4pi
            ripiega = np.abs(arg) > P4                   # il `_w8` RIPIEGA davvero
            # ### LA CURA PROPOSTA (non applicata): avvolgere la differenza di `dph` col
            #   periodo GIUSTO e sommare la differenza del dipolo NON avvolta.
            riparata = _w4(salto) + (td - td0)
            errore = spinta - riparata
            grosso = np.abs(errore) > np.pi
            self.cont["coppie"] += int(dph.size)
            self.cont["avvolgimenti"] += int(np.sum(avvolto))
            self.cont["ripiegamenti"] += int(np.sum(ripiega))
            self.cont["calci_oltre_pi"] += int(np.sum(grosso))
            # ### ⛔ **LA MEDIANA FIRMATA SU UNA DISTRIBUZIONE BIMODALE E' INGANNEVOLE:**
            #   il giro corto ha dato `0.0 pi` con `318` calci sopra `pi`, che letto da solo
            #   sembra una contraddizione. ### **Non lo era: l'insieme e' a `±4pi` e la
            #   mediana FIRMATA di due picchi opposti e' ZERO.** Si riporta
            #   ### **la mediana del MODULO** e ### **lo spacco dei SEGNI.**
            #   ### ⚠ **E il collaudo non l'avrebbe preso: il suo caso iniettava un
            #   avvolgimento di UN SOLO segno.**
            d["m6"] = {"n": int(dph.size),
                       "avvolgimenti": int(np.sum(avvolto)),
                       "ripiegamenti": int(np.sum(ripiega)),
                       "calci_oltre_pi": int(np.sum(grosso)),
                       "q_errore": q(np.abs(errore[grosso])) if np.any(grosso) else None,
                       "errore_MODULO_mediano_su_pi": (
                           float(np.median(np.abs(errore[grosso])) / np.pi)
                           if np.any(grosso) else None),
                       "errore_firmato_mediano_su_pi": (
                           float(np.median(errore[grosso]) / np.pi)
                           if np.any(grosso) else None),
                       "calci_positivi": int(np.sum(grosso & (errore > 0))),
                       "calci_negativi": int(np.sum(grosso & (errore < 0))),
                       "sopra_4pi_e_ripiega": int(np.sum(ripiega
                                                         & (np.abs(tw_in) >= P4))),
                       "sopra_4pi": int(np.sum(np.abs(tw_in) >= P4))}
        else:
            d["m6"] = {"stato": "nessun passo precedente confrontabile"}

        # ### `M1` / `M2` / `M3` / `M4`: il TETTO, sui valori CAUSALI del passo `t-1`
        #   ### ⚠ **E' la lezione di `99782e1`:** la spinta del passo `t` e' stata prodotta
        #   DURANTE il passo `t-1`, quindi `r` e `phivel` sono quelli di allora.
        if self._prec is not None:
            r0, w0 = self._prec["r"], self._prec["pv"]
            buoni = (i < r0.size) & (j < r0.size) & (i < w0.size) & (j < w0.size)
            if np.any(buoni):
                ri, rj = r0[i[buoni]], r0[j[buoni]]
                wi, wj = w0[i[buoni]], w0[j[buoni]]
                ts = tw_stella(ri, rj, wi, wj)
                tf = tw_stella_fedele(ri, rj, wi, wj, self.dt)
                d["tetto"] = {"n": int(np.sum(buoni)), "causale": True,
                              "passo_del_predittore": self.passo - 1,
                              "q_tw_stella": q(np.abs(ts)),
                              "q_tw_stella_fedele": q(np.abs(tf)),
                              "max_scarto_forme": float(np.max(np.abs(ts - tf))),
                              "q_grad_r": q(np.abs(ri - rj)),
                              "q_dom": q(np.abs(wi - wj))}
                self._tetto_grezzo = {"sel": buoni, "ts": ts, "td": np.abs(td[buoni]),
                                      "tw": np.abs(tw_in[buoni]),
                                      "dom": np.abs(wi - wj),
                                      "grad_r": np.abs(ri - rj)}
            else:
                d["tetto"] = {"n": 0, "causale": False,
                              "stato": "nessun arco con entrambi i nodi nel passo t-1"}
                self._tetto_grezzo = None
        else:
            d["tetto"] = {"n": 0, "causale": False, "stato": "primo passo"}
            self._tetto_grezzo = None

        self._tor = d
        self._prec = {"r": rr.copy(), "pv": pv.copy(), "dph": dph.copy(),
                      "td": td.copy(), "n_archi": int(dph.size)}

    # ---------------------------------------------------------------- gancio B
    def catena(self, net, avv, soglia, segno, prob, nasce):
        a = np.asarray(avv, float)
        s = np.asarray(soglia, float)
        g1 = a > s
        g2 = a < P4
        g3 = np.asarray(segno, float) > 0.0
        self._cat = {"archi": int(a.size),
                     "g1_sopra_soglia": int(np.sum(g1)),
                     "g2_sotto_tetto": int(np.sum(g2)),
                     "g3_segno_creazione": int(np.sum(g3)),
                     "g1_e_g2": int(np.sum(g1 & g2)),
                     "g1_e_g2_e_g3": int(np.sum(g1 & g2 & g3)),
                     "prob_positiva": int(np.sum(np.asarray(prob, float) > 0.0)),
                     "g4_nasce": int(np.sum(np.asarray(nasce, bool))),
                     "len_avv": int(a.size),
                     "q_soglia": q(s), "q_avv": q(a)}
        self._g1 = g1
        self._soglia = s

    # ---------------------------------------------------------------- fine passo
    def chiudi(self, net):
        d = {"passo": self.passo, "n": int(net.n), "archi": int(len(net.i)),
             "nati_tot": int(getattr(net, "nati", 0)),
             "schwinger_tot": int(getattr(net, "_g_nati_schwinger", 0))}
        d.update(self._cat or {"archi": 0, "g4_nasce": 0, "len_avv": 0})
        d["passo"] = self.passo
        d["n"] = int(net.n)
        if self._tor is not None:
            d["tor"] = self._tor
        self.passi.append(d)
        if self.passo in PASSI_MIS:
            self.mis[self.passo] = self._misura_piena()
        self._tor = self._cat = None
        self._g1 = self._soglia = None

    def _misura_piena(self):
        """`M1`-`M4` sulle distribuzioni, ai soli passi del mandato."""
        g = getattr(self, "_tetto_grezzo", None)
        if not g:
            return {"stato": "nessun dato causale a questo passo"}
        tw, ts, td, dom = g["tw"], np.abs(g["ts"]), g["td"], g["dom"]
        out = {"n": int(tw.size)}
        # ### `M1`: SOLO dove la deriva e' definita -- sopra il `q25` di `|dw|`, come il
        #   mandato chiede. ### **E il `q25` si calcola sul PREDITTORE, non sul bersaglio.**
        q25 = float(np.quantile(dom, 0.25))
        sel = dom > q25
        rap = tw[sel] / np.maximum(ts[sel], 1e-300)
        out["m1"] = {"n": int(np.sum(sel)), "q25_dom": q25,
                     "q_rapporto": q(rap),
                     "mediana": float(np.median(rap)) if rap.size else None,
                     "fraz_sopra_2": float(np.mean(rap > 2.0)) if rap.size else None,
                     "fraz_sopra_1": float(np.mean(rap > 1.0)) if rap.size else None}
        # ### `M2` col dipolo (il mandato) e `M2b` SENZA (la correzione della sezione (c))
        out["m2"] = spearman(ts + td, tw)
        out["m2b"] = spearman(ts, tw)
        out["quintili_m2"] = quintili(ts + td, tw)
        out["quintili_m2b"] = quintili(ts, tw)
        # ### `M3` / `M3b`: la frazione che ARRIVA alla soglia
        sog = getattr(self, "_soglia", None)
        g1 = getattr(self, "_g1", None)
        sm = None
        if sog is not None and len(sog) == len(g["sel"]):
            sm = np.asarray(sog, float)[g["sel"]]
        out["m3"] = {"fraz_oltre_3pi": float(np.mean((ts + td) >= P3)),
                     "fraz_oltre_soglia_modulata": (float(np.mean((ts + td) >= sm))
                                                    if sm is not None else None),
                     "q_soglia_modulata": q(sm) if sm is not None else None}
        out["m3b"] = {"fraz_oltre_3pi": float(np.mean(ts >= P3)),
                      "fraz_oltre_soglia_modulata": (float(np.mean(ts >= sm))
                                                     if sm is not None else None)}
        # ### `M4`: gli archi in `g1` contro gli altri
        if g1 is not None and len(g1) == len(g["sel"]):
            m = np.asarray(g1, bool)[g["sel"]]
            out["m4"] = {"n_g1": int(np.sum(m)), "n_altri": int(np.sum(~m))}
            for et, mm in (("g1", m), ("altri", ~m)):
                out["m4"][et] = {
                    "q_tw_stella": q(ts[mm]) if np.any(mm) else None,
                    "q_tw_stella_piu_dip": q((ts + td)[mm]) if np.any(mm) else None,
                    "q_twist_dip": q(td[mm]) if np.any(mm) else None,
                    "q_grad_r": q(g["grad_r"][mm]) if np.any(mm) else None,
                    "q_tw": q(tw[mm]) if np.any(mm) else None}
        else:
            out["m4"] = {"stato": "g1 non allineato: lunghezze %s contro %s"
                         % (None if g1 is None else len(g1), len(g["sel"]))}
        return out

    def totali(self):
        return {"divisioni_g4": int(sum(r.get("g4_nasce", 0) for r in self.passi)),
                "nati_tot": int(self.passi[-1]["nati_tot"]) if self.passi else 0,
                "schwinger": int(self.passi[-1]["schwinger_tot"]) if self.passi else 0,
                "contatori": dict(self.cont)}


# =============================================================== IL COLLAUDO
def collaudo():
    esiti = []

    def prova(nome, ok, dett=""):
        esiti.append((nome, bool(ok), dett))
        stampa("  %-6s %-70s %s" % ("OK" if ok else "FALLITA", nome, dett))

    riga("=")
    stampa("1. IL CONTROLLO POSITIVO E QUELLO CHE DEVE FALLIRE (dal mandato)")
    riga("=")

    def evolvi(kappa, passi=200000, dt=0.01, r=0.8, wi=3.0, wj=1.0, td=0.0):
        """L'arco SINTETICO, evoluto con la LEGGE VERA della torsione.

        ### **Nessun avvolgimento:** `twist_dip` e' costante e la differenza di `dph` e'
        `delta` a ogni passo, quindi `_w8` non ripiega. ### **E' il regime in cui la formula
        del mandato DEVE valere.**
        """
        dte = dt * r
        dom = abs(wi - wj) + PAV_DOM
        tau = max(kappa * P2 / dom, PAV_TAU)
        delta = dt * (r * wi - r * wj)
        tw = 0.0
        for _ in range(passi):
            tw += _w8(delta + 0.0 * td) - dte * tw / tau
        return tw

    tw1 = evolvi(1.0)
    sc1 = abs(abs(tw1) - P2) / P2
    prova("positivo: con kappa = 1 l'arco sintetico converge a |tw| = 2pi entro l'1 %",
          sc1 < 0.01, "|tw| = %.6f, 2pi = %.6f, scarto %.4f %%" % (abs(tw1), P2, 100 * sc1))
    tw2 = evolvi(2.0)
    sc2 = abs(abs(tw2) - P2) / P2
    prova("### CHE DEVE FALLIRE: con kappa = 2 NON converge a 2pi",
          sc2 > 0.01, "|tw| = %.6f, cioe' il %.1f %% fuori" % (abs(tw2), 100 * sc2))
    prova("### e con kappa = 2 converge a 2*2pi, che e' la stessa legge con un altro kappa",
          abs(abs(tw2) - 2.0 * P2) / (2.0 * P2) < 0.01,
          "|tw| = %.6f contro 4pi = %.6f" % (abs(tw2), 2.0 * P2))

    riga("=")
    stampa("2. LA FORMA CHIUSA: con r UNIFORME il r si CANCELLA")
    riga("=")
    for rr in (0.1, 0.5, 0.8, 1.0):
        ts = tw_stella(rr, rr, 3.0, 1.0)
        prova("tw_stella: con r_i = r_j = %.1f vale 2pi a meno del pavimento" % rr,
              abs(abs(ts) - P2) / P2 < 1e-3, "%.6f" % abs(ts))
    prova("tw_stella: ### e con r DIVERSI agli estremi si SPOSTA da 2pi",
          abs(abs(tw_stella(0.5, 1.0, 3.0, 1.0)) - P2) / P2 > 0.1,
          "%.6f contro %.6f" % (abs(tw_stella(0.5, 1.0, 3.0, 1.0)), P2))
    prova("tw_stella: ### il segno segue (r_i*w_i - r_j*w_j), non il modulo",
          tw_stella(1.0, 1.0, 1.0, 3.0) < 0 < tw_stella(1.0, 1.0, 3.0, 1.0))
    prova("tw_stella: la forma CHIUSA e quella FEDELE coincidono dove il pavimento non "
          "vincola",
          abs(tw_stella(0.8, 0.9, 3.0, 1.0)
              - tw_stella_fedele(0.8, 0.9, 3.0, 1.0, 0.01)) < 1e-9)
    _dom_rotto = 1e4
    prova("tw_stella: ### e DIVERGONO dove il pavimento VINCOLA (|dw| oltre 6283)",
          abs(tw_stella(1.0, 1.0, _dom_rotto, 0.0)
              - tw_stella_fedele(1.0, 1.0, _dom_rotto, 0.0, 0.01)) > 1e-6,
          "|dw| = %.0f: il pavimento 1e-3 taglia tau" % _dom_rotto)

    riga("=")
    stampa("3. L'AVVOLGIMENTO: _w8 ha periodo 8pi e NON ripara un salto di 4pi")
    riga("=")
    _wphi = lambda a: (a + P2) % (2.0 * P2) - P2       # noqa: E731  (FASE_2PI = False)
    delta = 0.013
    d0 = _wphi(P2 - delta / 2)
    d1 = _wphi(P2 + delta / 2)
    # ### LA MIA ASSERZIONE ERA SBAGLIATA, non il codice: il salto grezzo e'
    #   `delta - 4pi`, NON `-4pi`. ### **E il collaudo l'ha presa**, che e' il motivo per cui
    #   un criterio si collauda su un caso a risposta NOTA prima di puntarlo sul codice vero
    #   *(`P1-sexies`)*.
    prova("avvolgimento: dph SALTA, e il salto grezzo e' delta - 4pi",
          abs((d1 - d0) - (delta - P4)) < 1e-9,
          "%.6f contro %.6f" % (d1 - d0, delta - P4))
    prova("### avvolgimento: il ramo che GIRA (_w8) sbaglia di -4pi ESATTI",
          abs(_w8(d1 - d0) - delta + P4) < 1e-6,
          "_w8 da' %.6f invece di %.6f" % (_w8(d1 - d0), delta))
    prova("### avvolgimento: il ramo non-4pi (_w4) lo ripara ESATTO",
          abs(_w4(d1 - d0) - delta) < 1e-9, "_w4 da' %.6f" % _w4(d1 - d0))
    prova("avvolgimento: ### e senza salto i DUE rami coincidono",
          abs(_w8(delta) - delta) < 1e-12 and abs(_w4(delta) - delta) < 1e-12)
    prova("avvolgimento: la cura proposta ripara ANCHE col dipolo che cambia",
          abs((_w4(d1 - d0) + (np.pi / 2 - 0.0)) - (delta + np.pi / 2)) < 1e-9,
          "_w4(salto) + (td - td0)")
    prova("### avvolgimento: e il _w8 su quello stesso caso sbaglia ancora di -4pi",
          abs(_w8(d1 - d0 + np.pi / 2) - (delta + np.pi / 2) + P4) < 1e-6)

    riga("=")
    stampa("4. L'INVARIANTE DERIVATO: |dph + twist_dip| <= 3pi, quindi twp NON avvolge")
    riga("=")
    _rng = np.random.default_rng(7)
    _dp = _rng.uniform(-P2, P2, 200000)
    _td = _rng.choice([-np.pi, -np.pi / 2, 0.0, np.pi / 2, np.pi], 200000)
    prova("invariante: |dph + twist_dip| <= 3pi su 200000 casi",
          bool(np.all(np.abs(_dp + _td) <= P3 + 1e-12)),
          "max %.6f contro 3pi = %.6f" % (np.max(np.abs(_dp + _td)), P3))
    prova("### invariante: quindi _w8(dph + twist_dip) E' dph + twist_dip (nessun "
          "avvolgimento)",
          bool(np.allclose(_w8(_dp + _td), _dp + _td, atol=1e-12)))
    prova("invariante: ### e il controllo che DEVE fallire -- a 5pi _w8 AVVOLGE",
          not np.isclose(_w8(5.0 * np.pi), 5.0 * np.pi),
          "_w8(5pi) = %.6f" % _w8(5.0 * np.pi))

    riga("=")
    stampa("5. I CINQUE VALORI DI twist_dip, e M5")
    riga("=")
    _chi = np.asarray([-1, 0, 1], int)
    _vals = sorted(set(float(np.pi * 0.5 * (a - b)) for a in _chi for b in _chi))
    prova("M5: con perc_chi in {-1, 0, 1} i valori di twist_dip sono CINQUE",
          len(_vals) == 5, "%s" % ["%.4f" % v for v in _vals])
    prova("M5: ### e i moduli sono TRE: 0, pi/2, pi",
          sorted(set(round(abs(v), 9) for v in _vals))
          == [0.0, round(np.pi / 2, 9), round(np.pi, 9)])

    riga("=")
    stampa("6. LA PATCH: due ganci, e NESSUNA legge toccata")
    riga("=")
    import tempfile
    _d = tempfile.mkdtemp()
    _p = os.path.join(_d, "s.py")
    fatte = copia_patchata(SIM, _p)
    tt = io.open(_p, encoding="utf-8").read()
    t0 = io.open(SIM, encoding="utf-8").read()
    prova("patch: le tre ancore sono state sostituite", len(fatte) == 3,
          "%d: %s" % (len(fatte), fatte))
    prova("patch: il gancio A sta PRIMA dell'aggiornamento di tw",
          tt.index("_MIS.torsione(self, dph=dph")
          < tt.index("self.tw += self._w8(dph + twist_dip - self.twp)"))
    prova("patch: la riga della torsione resta IDENTICA, una volta sola",
          tt.count("self.tw += self._w8(dph + twist_dip - self.twp)"
                   " - dt_e * self.tw / _ttw") == 1
          and t0.count("self.tw += self._w8(dph + twist_dip - self.twp)"
                       " - dt_e * self.tw / _ttw") == 1)
    prova("patch: ### e la riga del ramo non-4pi NON si tocca",
          tt.count("self.tw += self._w4(dph - self.twp) - dt_e * self.tw / _ttw") == 1)
    # ### LA PROVA CHE CONTA: togliendo le righe INIETTATE si torna al sorgente vero
    _inj = ["_MIS = None   # [TETTO-TORSIONE] lo riempie lo strumento" + NL,
            "            if _MIS is not None:" + NL,
            "                _MIS.torsione(self, dph=dph, twp=self.twp," + NL,
            "                              twist_dip=twist_dip, ttw=_ttw, dt_e=dt_e," + NL,
            "                              dt_n=dt_n, r=r, dsync=delta_sync_phi, i=i, j=j)"
            + NL,
            "        if _MIS is not None:" + NL,
            "            _MIS.catena(self, avv=avv, soglia=soglia, segno=segno," + NL,
            "                        prob=prob, nasce=nasce)" + NL]
    _ri = tt
    for x in _inj:
        _ri = _ri.replace(x, "", 1)
    prova("### patch: togliendo le SOLE righe iniettate si torna al sorgente VERO",
          _ri == t0, "carattere per carattere")

    riga("=")
    stampa("7. LA MISURA: i casi a risposta NOTA")
    riga("=")
    m = Misura(0.01)
    m.passo = PASSI_MIS[0]

    class FintaRete(object):
        pass

    fr = FintaRete()
    # ### GLI ARCHI DEVONO INDICIZZARE NODI CHE ESISTONO: `j = arange(NA) + NA` arriva a
    #   `2*NA - 1`, quindi serve `NN >= 2*NA`. ### **Il primo caso che avevo scritto non ce
    #   l'aveva e il collaudo e' caduto con un IndexError** -- lo stesso errore di `I[c]`
    #   di `12e2ca7`: un caso di prova troppo piccolo per la sua stessa indicizzazione.
    NN, NA = 60, 25
    fr.n = NN
    fr.i = np.arange(NA)
    fr.j = np.arange(NA) + NA
    fr.tw = np.linspace(0.1, 10.0, NA)
    fr.phivel = np.linspace(0.0, 6.0, NN)
    fr.nati = 0
    fr._g_nati_schwinger = 0
    _r = np.linspace(0.6, 1.0, NN)
    _dn = 0.01 * _r
    _ds = np.zeros(NN)
    _arg = {"dph": np.linspace(-1.0, 1.0, NA),
            "twp": np.zeros(NA),
            "twist_dip": np.zeros(NA),
            "ttw": 2.0, "dt_e": 0.008, "dt_n": _dn, "r": _r, "dsync": _ds,
            "i": fr.i, "j": fr.j}
    m.torsione(fr, **_arg)                     # primo passo: nessun precedente
    prova("misura: al primo passo `tetto` dichiara causale = False",
          m._tor["tetto"]["causale"] is False, m._tor["tetto"].get("stato"))
    prova("misura: ### e M6 dichiara che non c'e' un passo precedente",
          "stato" in m._tor["m6"])
    m.catena(fr, avv=np.abs(fr.tw), soglia=np.full(NA, P3), segno=np.ones(NA),
             prob=np.full(NA, 0.5), nasce=np.zeros(NA, bool))
    m.chiudi(fr)
    m.passo = PASSI_MIS[0]
    m.torsione(fr, **_arg)                     # secondo passo: ora c'e'
    prova("misura: al secondo passo `tetto` e' CAUSALE e punta al passo t-1",
          m._tor["tetto"]["causale"] is True
          and m._tor["tetto"]["passo_del_predittore"] == PASSI_MIS[0] - 1)
    prova("misura: M5 conta il dipolo a ZERO come 1.0 quando e' tutto zero",
          abs(m._tor["m5"]["fraz_zero"] - 1.0) < 1e-12)
    prova("misura: M8 non vincola con phivel di scala O(1)",
          m._tor["m8"]["vincolati"] == 0, "dom_max %.4f" % m._tor["m8"]["dom_max"])
    prova("misura: l'invariante su twp non e' mai violato nel caso finto",
          m.cont["twp_fuori_3pi"] == 0)
    # ### IL CASO NULLO si fotografa ADESSO: `chiudi()` azzera `_tor`, e leggerlo dopo
    #   darebbe `None`. ### **Il collaudo l'ha preso con un TypeError.**
    _nullo = dict(m._tor["m6"])
    m.catena(fr, avv=np.abs(fr.tw), soglia=np.full(NA, P3), segno=np.ones(NA),
             prob=np.full(NA, 0.5), nasce=np.zeros(NA, bool))
    m.chiudi(fr)
    mm = m.mis.get(PASSI_MIS[0])
    prova("misura: al passo del mandato la misura PIENA c'e'",
          mm is not None and "m1" in mm, "%s" % (sorted(mm.keys()) if mm else None))
    prova("misura: ### M1 usa SOLO gli archi sopra il q25 di |dw| (non tutti)",
          mm["m1"]["n"] < mm["n"], "%d su %d" % (mm["m1"]["n"], mm["n"]))
    prova("misura: M3b (senza dipolo) non e' MAI maggiore di M3 (con dipolo)",
          mm["m3b"]["fraz_oltre_3pi"] <= mm["m3"]["fraz_oltre_3pi"] + 1e-12,
          "%.6f <= %.6f" % (mm["m3b"]["fraz_oltre_3pi"], mm["m3"]["fraz_oltre_3pi"]))
    prova("misura: M4 separa g1 dagli altri e i due conteggi sommano a n",
          mm["m4"]["n_g1"] + mm["m4"]["n_altri"] == mm["n"],
          "%d + %d = %d" % (mm["m4"]["n_g1"], mm["m4"]["n_altri"], mm["n"]))
    # ### IL CASO CHE DEVE FALLIRE: un avvolgimento INIETTATO si DEVE vedere
    m2 = Misura(0.01)
    m2.passo = 2
    _a0 = dict(_arg)
    _a0["dph"] = np.full(NA, P2 - 0.01)
    m2.torsione(fr, **_a0)
    m2.catena(fr, avv=np.abs(fr.tw), soglia=np.full(NA, P3), segno=np.ones(NA),
              prob=np.full(NA, 0.5), nasce=np.zeros(NA, bool))
    m2.chiudi(fr)
    m2.passo = 3
    _a1 = dict(_arg)
    _a1["dph"] = np.full(NA, -(P2 - 0.01))
    _a1["twp"] = np.full(NA, P2 - 0.01)
    m2.torsione(fr, **_a1)
    prova("### M6: un AVVOLGIMENTO iniettato viene CONTATO su tutti gli archi",
          m2._tor["m6"]["avvolgimenti"] == NA, "%d su %d"
          % (m2._tor["m6"]["avvolgimenti"], NA))
    prova("### M6: e il CALCIO che ne risulta e' circa -4pi su ogni arco",
          m2._tor["m6"]["calci_oltre_pi"] == NA
          and abs(m2._tor["m6"]["errore_MODULO_mediano_su_pi"] - 4.0) < 0.01
          and abs(m2._tor["m6"]["errore_firmato_mediano_su_pi"] + 4.0) < 0.01,
          "MODULO %.4f pi, firmato %.4f pi"
          % (m2._tor["m6"]["errore_MODULO_mediano_su_pi"],
             m2._tor["m6"]["errore_firmato_mediano_su_pi"]))
    prova("### M6: e il caso iniettato ha UN SOLO segno -- tutti negativi",
          m2._tor["m6"]["calci_negativi"] == NA
          and m2._tor["m6"]["calci_positivi"] == 0,
          "ed e' PROPRIO per questo che il collaudo vecchio non vedeva il difetto")
    # ### IL CASO BIMODALE: il difetto che il giro corto ha trovato e il collaudo NO.
    #   ### **Il suo caso iniettava un avvolgimento di UN SOLO segno**, quindi la mediana
    #   firmata coincideva col modulo e il difetto era invisibile.
    _e = np.concatenate([np.full(50, -4.0 * np.pi), np.full(50, 4.0 * np.pi)])
    prova("M6: ### la mediana FIRMATA di una distribuzione a +-4pi e' circa ZERO",
          abs(float(np.median(_e))) < 1e-9, "%.6f" % float(np.median(_e)))
    prova("M6: ### mentre quella del MODULO e' 4pi -- ed e' quella che conta",
          abs(float(np.median(np.abs(_e))) / np.pi - 4.0) < 1e-12,
          "%.4f pi" % (float(np.median(np.abs(_e))) / np.pi))
    prova("M6: ### e lo spacco dei segni e' 50 e 50, che la mediana firmata NASCONDE",
          int(np.sum(_e > 0)) == 50 and int(np.sum(_e < 0)) == 50)
    prova("M6: ### e con UN SOLO segno le due mediane coincidono: ecco perche' il collaudo "
          "vecchio non lo prendeva",
          abs(float(np.median(_e[:50])) - float(-np.median(np.abs(_e[:50])))) < 1e-12)
    prova("M6: ### e SENZA avvolgimento i calci sono ZERO (il caso nullo)",
          _nullo["calci_oltre_pi"] == 0 and _nullo["avvolgimenti"] == 0,
          "e' la domanda <<quanto varrebbe questo criterio se non ci fosse niente?>>")

    riga("=")
    ko = [n for n, o, _d in esiti if not o]
    stampa("COLLAUDO: %d su %d" % (len(esiti) - len(ko), len(esiti)))
    if ko:
        stampa("### FALLITI:")
        for n in ko:
            stampa("    - " + n)
    riga("=")
    return 1 if ko else 0


# =============================================================== IL RAPPORTO
def rapporto(mis, net, cre, in_conf, passi):
    guasti = []
    rifB = cre["bracci"]["Bp"]
    perB = {r["passo"]: r for r in rifB["passi"]}
    riga("=")
    stampa("C0: LA COPIA PATCHATA E' BYTE-IDENTICA A Bp?")
    riga("=")
    CAMPI = ("archi", "g1_sopra_soglia", "g1_e_g2", "g1_e_g2_e_g3", "prob_positiva",
             "g4_nasce", "n")
    dd = []
    for r in mis.passi:
        s = perB.get(r["passo"])
        if s is None:
            continue
        for c in CAMPI:
            if int(r.get(c, -1)) != int(s.get(c, -2)):
                dd.append((r["passo"], c, r.get(c), s.get(c)))
    ok0 = (not dd) and int(net.n) == cre["a_valle"]["n_Bp"]
    stampa("  differenze %d su %d passi (%d campi), n finale %d contro %d  -> %s"
           % (len(dd), len(mis.passi), len(CAMPI), int(net.n), cre["a_valle"]["n_Bp"],
              "PASSA" if ok0 else "### FALLISCE"))
    for x in dd[:5]:
        stampa("      passo %s  %s: %s contro %s" % x)
    if not ok0:
        guasti.append("C0")
        stampa("  ### I GANCI NON SONO DI SOLA LETTURA, O L'ALLINEAMENTO E' ROTTO.")
        stampa("      OGNI NUMERO DI QUESTA MISURA E' SOSPETTO. MI FERMO.")
        return 1, guasti

    c = mis.cont
    riga("=")
    stampa("M6: GLI AVVOLGIMENTI, su tutta la corsa")
    riga("=")
    stampa("  coppie (passo, arco) confrontate       %d" % c["coppie"])
    stampa("  AVVOLGIMENTI di dph (|salto| > 2pi)    %d   (%s per coppia)"
           % (c["avvolgimenti"],
              n4(c["avvolgimenti"] / c["coppie"]) if c["coppie"] else "n/d"))
    stampa("  RIPIEGAMENTI del _w8 (|arg| > 4pi)     %d" % c["ripiegamenti"])
    stampa("  CALCI oltre pi (|spinta - riparata|)   %d" % c["calci_oltre_pi"])
    stampa("  ### E I DUE CONTEGGI SONO LO STESSO EVENTO VISTO DUE VOLTE: se non")
    stampa("      coincidessero, uno dei due sarebbe sbagliato.")
    # ### IL MODULO E I SEGNI, passo per passo ai passi del mandato
    for p in PASSI_MIS:
        _r = [x for x in mis.passi if x["passo"] == p and "tor" in x]
        if not _r:
            continue
        z = (_r[0]["tor"].get("m6") or {})
        if "errore_MODULO_mediano_su_pi" not in z:
            continue
        stampa("      passo %-4d calci %5s   MODULO mediano %s pi   firmato %s pi   "
               "+ %s / - %s"
               % (p, z.get("calci_oltre_pi"),
                  n4(z.get("errore_MODULO_mediano_su_pi")),
                  n4(z.get("errore_firmato_mediano_su_pi")),
                  z.get("calci_positivi"), z.get("calci_negativi")))
    stampa("  ### LA MEDIANA DEL MODULO E' QUELLA CHE CONTA: la FIRMATA su una distribuzione")
    stampa("      a due picchi opposti da' ZERO anche con calci enormi, ed e' il difetto di")
    stampa("      referto che il giro corto ha trovato.")
    stampa("  invariante |twp| <= 3pi violato        %d   %s"
           % (c["twp_fuori_3pi"],
              "(la derivazione del task history TIENE)" if not c["twp_fuori_3pi"]
              else "### LA DERIVAZIONE E' FALSA"))
    if c["twp_fuori_3pi"]:
        guasti.append("invariante twp")
    stampa("  M8: archi col pavimento esterno di tau VINCOLANTE   %d" % c["archi_pavimento"])
    stampa()
    for p in PASSI_MIS:
        d = mis.mis.get(p)
        riga("=")
        stampa("IL PASSO %d" % p)
        riga("=")
        if not d or "m1" not in d:
            stampa("  ### NESSUN DATO: %s" % (d or {}).get("stato"))
            continue
        m1 = d["m1"]
        stampa("  M1  |tw|/|tw*| sugli archi con |dw| > q25 (%d su %d, q25 = %.6f)"
               % (m1["n"], d["n"], m1["q25_dom"]))
        stampa("      mediana %s   q05 %s  q50 %s  q95 %s   frazione > 1: %s   > 2: %s"
               % (n4(m1["mediana"]), n4((m1["q_rapporto"] or {}).get("q050")),
                  n4((m1["q_rapporto"] or {}).get("q050")),
                  n4((m1["q_rapporto"] or {}).get("q095")),
                  n4(m1["fraz_sopra_1"]), n4(m1["fraz_sopra_2"])))
        stampa("  M2  Spearman(|tw*| + |twist_dip|, |tw|)  %s" % n4(d["m2"]))
        stampa("  M2b Spearman(|tw*|, |tw|)  SENZA il dipolo  %s   -> %s"
               % (n4(d["m2b"]),
                  "il dipolo NON aiuta" if (d["m2b"] or 0) >= (d["m2"] or 0)
                  else "il dipolo AIUTA"))
        stampa("  M3  frazione con |tw*| + |twist_dip| >= 3pi        %s"
               % n4(d["m3"]["fraz_oltre_3pi"]))
        stampa("      frazione oltre la SOGLIA MODULATA              %s"
               % n4(d["m3"]["fraz_oltre_soglia_modulata"]))
        stampa("  M3b frazione con |tw*| >= 3pi, SENZA il dipolo     %s"
               % n4(d["m3b"]["fraz_oltre_3pi"]))
        if "n_g1" in d["m4"]:
            stampa("  M4  g1 (%d archi) contro gli altri (%d):"
                   % (d["m4"]["n_g1"], d["m4"]["n_altri"]))
            for et in ("g1", "altri"):
                z = d["m4"][et]
                stampa("        %-6s |tw*| mediano %s   |twist_dip| mediano %s   "
                       "|r_i-r_j| mediano %s"
                       % (et, n4((z["q_tw_stella"] or {}).get("q050")),
                          n4((z["q_twist_dip"] or {}).get("q050")),
                          n4((z["q_grad_r"] or {}).get("q050"))))
        else:
            stampa("  M4  ### %s" % d["m4"].get("stato"))
        stampa()
    riga("=")
    stampa("M5: LA DISTRIBUZIONE DI |twist_dip| (dal passo %d)" % PASSI_MIS[-1])
    riga("=")
    _ult = [r for r in mis.passi if r["passo"] == PASSI_MIS[-1] and "tor" in r]
    if _ult:
        z = _ult[0]["tor"]["m5"]
        stampa("  archi %d   a ZERO %s   a pi/2 %s   a pi %s   altro %s"
               % (z["n"], n4(z["fraz_zero"]), n4(z["fraz_mezzo_pi"]), n4(z["fraz_pi"]),
                  n4(z["fraz_altro"])))
    else:
        stampa("  ### nessun dato al passo %d" % PASSI_MIS[-1])
    stampa()
    riga("=")
    stampa("M7: IL TERMINE CHE LA FORMULA IGNORA (delta_sync_phi, K_SYNC = 1.0)")
    riga("=")
    if _ult and "m7" in _ult[0]["tor"]:
        z = _ult[0]["tor"]["m7"]
        stampa("  |avanzamento| mediano  %s" % n4((z["q_avanzamento"] or {}).get("q050")))
        stampa("  |delta sync| mediano   %s" % n4((z["q_dsync"] or {}).get("q050")))
        stampa("  RAPPORTO mediano       %s   q95 %s"
               % (n4((z["q_rapporto"] or {}).get("q050")),
                  n4((z["q_rapporto"] or {}).get("q095"))))
        stampa("  ### SE IL RAPPORTO NON E' PICCOLO, LA FORMULA DEL MANDATO IGNORA UN")
        stampa("      TERMINE CHE CONTA, e il tetto misurato non e' quello calcolato.")
        zb = _ult[0]["tor"].get("m7b") or {}
        stampa("  M7b IL SEGNO:  Spearman(dph, Delta dsync) %s   frazione a segno OPPOSTO %s"
               % (n4(zb.get("spearman_dsync_dph")), n4(zb.get("fraz_segno_opposto"))))
        stampa("      ### SE LA SPEARMAN E' NEGATIVA, IL TERMINE RICHIAMA: smorza la spinta")
        stampa("      invece di aggiungersi, e il tetto vero sta SOTTO 2pi.")
    stampa()
    riga("=")
    stampa("I CRITERI, FISSATI DAL MANDATO")
    riga("=")
    med = [(p, (mis.mis.get(p) or {}).get("m1", {}).get("mediana")) for p in PASSI_MIS]
    sp = [(p, (mis.mis.get(p) or {}).get("m2")) for p in PASSI_MIS]
    fuori = [(p, v) for p, v in med if v is not None
             and not (MEDIANA_M1[0] <= v <= MEDIANA_M1[1])]
    sotto = [(p, v) for p, v in sp if v is not None and abs(v) < SOGLIA_M2]
    stampa("  mediane di M1: %s" % ", ".join("passo %d: %s" % (p, n4(v)) for p, v in med))
    stampa("  Spearman M2:   %s" % ", ".join("passo %d: %s" % (p, n4(v)) for p, v in sp))
    _ref_tetto = bool(fuori) or (len(sotto) == len([x for x in sp if x[1] is not None])
                                 and sotto)
    stampa("  ### L'IPOTESI DEL TETTO e': %s"
           % ("REFUTATA" if _ref_tetto else "NON refutata"))
    if fuori:
        stampa("      perche' la mediana cade fuori da [%.1f, %.1f] ai passi %s"
               % (MEDIANA_M1[0], MEDIANA_M1[1], [p for p, _ in fuori]))
    if sotto and len(sotto) == len([x for x in sp if x[1] is not None]):
        stampa("      perche' la Spearman e' sotto %.2f a TUTTI i passi" % SOGLIA_M2)
    z0 = (_ult[0]["tor"]["m5"]["fraz_zero"] if _ult else None)
    stampa("  frazione con twist_dip = 0: %s   (soglia %.2f)" % (n4(z0), FRAZ_DIP0))
    stampa("  ### LA SECONDA IPOTESI e': %s"
           % ("n/d" if z0 is None
              else ("REFUTATA" if z0 < FRAZ_DIP0 else "NON refutata")))
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
    stampa("  ### E QUESTA E' UNA MISURA, NON UN SIGILLO: kappa, la soglia, il dipolo")
    stampa("      locale e il 0.3 sono DECISIONI DI LUCA.")
    return 0, []


def _scrivi(d):
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    io.open(os.path.join(FUORI, "tetto.json"), "w", encoding="utf-8").write(
        json.dumps(d, indent=1, default=str))


def main(argv):
    passi = PASSI
    if "--collaudo" in argv[1:]:
        riga("=")
        stampa("IL COLLAUDO DI _tetto_torsione.py")
        riga("=")
        return collaudo()
    for a in argv[1:]:
        if a.startswith("--passi="):
            passi = int(a.split("=", 1)[1])
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    riga("=")
    stampa("IL TETTO DELLA TORSIONE: la soglia di mitosi 3pi sta sul tetto?")
    riga("=")
    pf = piattaforma()
    for k in ["python", "numpy", "sistema", "macchina"]:
        stampa("  %-10s %s" % (k, pf[k]))
    stampa("  simulatore %s   strumento %s   _mitosi_soglia_grad %s"
           % (blob(SIM)[:8], blob(__file__)[:8], blob(_MSG.__file__)[:8]))
    stampa("  kappa = %.1f  (### KAPPA-TW-COMMENTO: il CODICE da' 1, il commento 3.1831)"
           % KAPPA)
    stampa()
    cre = json.loads(io.open(CRESCITA, encoding="utf-8").read())
    dst = os.path.join(FUORI, "_sim_tetto.py")
    anc = copia_patchata(SIM, dst)
    stampa("  la copia patchata: blob %s  (%d ancore)" % (blob(dst)[:8], len(anc)))
    for a in anc:
        stampa("      %s" % a)
    stampa()
    S, N, _a = carica("msg_tetto", dst)
    m = Misura(S.DT)
    S._MIS = m
    in_conf = _cli_flag.dichiara_configurazione(S, stampa)
    stampa("  scena: n = %d, archi = %d, DT = %r" % (N.n, len(N.i), S.DT))
    stampa("  ### E len(tw) == len(i): %s" % (len(N.tw) == len(N.i)))
    stampa()
    riga("=")
    stampa("LA CORSA: %d passi, UN braccio" % passi)
    riga("=")

    def _ist(stato, k, err=None):
        d = {"piattaforma": pf, "passi": passi, "passi_girati": k, "stato": stato,
             "blob_sim": blob(SIM), "blob_strumento": blob(__file__),
             "blob_mitosi_soglia_grad": blob(_MSG.__file__),
             "blob_copia": blob(dst), "ancore": anc,
             "kappa": KAPPA, "passi_mis": list(PASSI_MIS),
             "criteri": {"mediana_m1": list(MEDIANA_M1), "soglia_m2": SOGLIA_M2,
                         "fraz_dip0": FRAZ_DIP0},
             "in_configurazione_del_driver": bool(in_conf),
             "passi_dati": m.passi, "misure": m.mis, "totali": m.totali(),
             "a_valle": {"n": int(N.n), "archi": int(len(N.i))},
             "riferimento_Bp": {"n_fin": cre["a_valle"]["n_Bp"],
                                "archi": cre["a_valle"]["archi_Bp"]}}
        if err is not None:
            d["errore"] = err
        _scrivi(d)
        return d

    for k in range(1, passi + 1):
        m.passo = k
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                _passo.passo_pieno(S, N)
            m.chiudi(N)
        except Exception as e:
            import traceback
            stampa("### LA CORSA E' CADUTA AL PASSO %d: %r" % (k, e))
            stampa(traceback.format_exc())
            stampa("### MA I DATI DEI %d PASSI PRIMA SONO SALVATI." % (k - 1))
            _ist("CADUTA al passo %d" % k, k - 1,
                 err={"passo": k, "errore": repr(e), "traccia": traceback.format_exc()})
            return 1
        print("[battito] passo %d/%d  n=%d archi=%d  nasce=%d  avvolgimenti=%d"
              % (k, passi, N.n, len(N.i), m.passi[-1].get("g4_nasce", 0),
                 m.cont["avvolgimenti"]), flush=True)
        if k % PASSI_SALVA == 0:
            _ist("IN CORSO", k)
    comune = _ist("DATI SALVATI, rapporto NON ancora girato", passi)
    stampa("  ### I DATI SONO GIA' SALVATI in tetto.json, PRIMA del rapporto.")
    stampa()
    try:
        esito, guasti = rapporto(m, N, cre, in_conf, passi)
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


if __name__ == "__main__":
    sys.exit(main(sys.argv))
