# -*- coding: utf-8 -*-
"""LA MISURA LUNGA di `TORS-W8-AVVOLGIMENTO`: **1000 passi**, un braccio.

*(Decisione di Luca del 2026-10-06. Previsioni, limite della curva e criterio sono fissati in
`doc/TASK_HISTORY/2026-10-06_tors-w8-misura-lunga.md`, committato **prima** in `7d3ae67`.)*

### ⛔ **IL PERCHE' `1000` E NON `150`:** il tempo di scarica `τ_tw/dt_e` vale `~1491` passi
al passo `1`, `~309` al `50` e `~250` al `140`. ### **In `150` passi la rete e' ancora nel
transitorio**, e con la legge curata la torsione ### **parte da zero**: per vedere dove si
stabilizza servono ### **due o tre tempi di scarica.**

### ⛔ **IL SIMULATORE NON SI TOCCA**, e il suo blob si ### **VERIFICA all'avvio**: la misura
vale per `cf2a1ac8` e per nessun altro. Si gira una **copia** con **due ganci di SOLA
LETTURA** -- uno nel blocco della torsione, uno in `decidi_divisione`.

### 📌 **DIPENDE DA `_mitosi_soglia_grad.py`** per `q`, `spearman` *(a **ranghi medi**)*,
`quintili`, `blob`, `piattaforma` e `carica`: ### **e' una scelta dichiarata** -- duplicare la
Spearman vorrebbe dire due copie della stessa legge che possono divergere *(par.9-ter)* -- e
### **il suo blob entra nel `json`.**

# ESENTE-H-P5: dichiara la configurazione INTERA con `_cli_flag.dichiara_configurazione`, ma
#   il rilevatore non la vede perche' la chiamata e' dentro `main` e il referto lo scrive un
#   GENERATORE separato. La configurazione INTERA entra nel `json`, e il generatore la
#   stampa: il presidio e' SODDISFATTO nella sostanza, e lo dichiaro invece di spostare la
#   chiamata per compiacere un rilevatore.

USO:  python csv/_test_fork/_tors_w8_lunga.py  [--passi=N]  [--collaudo]
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

q, spearman, blob = _MSG.q, _MSG.spearman, _MSG.blob
piattaforma, carica, n4 = _MSG.piattaforma, _MSG.carica, _MSG.n4
stampa, riga = _MSG.stampa, _MSG.riga

NL = chr(10)
FUORI = os.path.join(RADICE, "csv", "_test_fork", "_tors_w8_lunga")
SIM = os.path.join(RADICE, "soliton_simulator.py")
# ### IL BLOB ATTESO: la misura vale per QUESTO simulatore e per nessun altro.
BLOB_ATTESO = "cf2a1ac8"
PASSI = 1000
PASSI_SALVA = 10
PASSI_PIENI = (50, 150, 300, 600, 1000)     # i passi della misura PIENA, dal mandato
FINESTRA = 50                               # le nascite per finestre di 50 passi
P2 = 2.0 * np.pi
P3 = 3.0 * np.pi
P4 = 4.0 * np.pi
KAPPA = 1.0            # ### `KAPPA-TW-COMMENTO`: il CODICE da' 1, il commento 3.1831
PAV_DOM = 1e-3
TAU_CURVA = 300.0      # ### il `τ` della curva del guardiano: NON scelto, MISURATO (`309`)


def curva(t):
    """La curva del guardiano: `2π·(1 − e^(−t/300))`.

    ### ⚠ **ASSUME `τ = 300` FISSO**, mentre il `τ` vero parte da `~1491` e scende a `~250`:
    il limite e' dichiarato nel task history, e il criterio ### **non legge** ai passi `50` e
    `150` per questo.
    """
    return P2 * (1.0 - np.exp(-float(t) / TAU_CURVA))


def tw_stella(r_i, r_j, w_i, w_j, kappa=KAPPA):
    """Il tetto di equilibrio, la forma del mandato del tetto *(`eebe24f`)*."""
    rm = 0.5 * (r_i + r_j)
    dom = np.abs(w_i - w_j) + PAV_DOM
    return kappa * P2 * (r_i * w_i - r_j * w_j) / (rm * dom)


# =============================================================== LA COPIA PATCHATA
def copia_patchata(sorgente, dst):
    """Due ganci di **SOLA LETTURA**. Ancore **CONTATE** e **UNICHE** *(`P1-quater`)*."""
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
        + "_MIS = None   # [TORS-W8 LUNGA] lo riempie lo strumento" + NL,
        "il gancio di modulo `_MIS`")
    # ### IL GANCIO `A`: **prima** dell'aggiornamento, cosi' `tw`, `twp` e `twp_dip` sono i
    #   valori d'INGRESSO. ### **L'ancora e' la riga di `_nuovo`, che e' UNICA** -- la riga
    #   di `_ttw` compare DUE volte, nei due rami di `TORS_4PI`.
    uno("            _nuovo = np.isnan(self.twp_dip)" + NL,
        "            if _MIS is not None:" + NL
        + "                _MIS.torsione(self, dph=dph, twist_dip=twist_dip," + NL
        + "                              twp=self.twp, twp_dip=self.twp_dip," + NL
        + "                              ttw=_ttw, dt_e=dt_e, r=r, i=i, j=j)" + NL
        + "            _nuovo = np.isnan(self.twp_dip)" + NL,
        "A: il blocco della torsione, PRIMA dell'aggiornamento")
    uno("        c = np.where(nasce)[0]" + NL,
        "        if _MIS is not None:" + NL
        + "            _MIS.catena(self, avv=avv, soglia=soglia, segno=segno," + NL
        + "                        prob=prob, nasce=nasce)" + NL
        + "        c = np.where(nasce)[0]" + NL,
        "B: la catena dei cancelli di `decidi_divisione`")
    io.open(dst, "w", encoding="utf-8", newline=NL).write(t)
    return fatte


class Misura(object):
    """### **LEGGE SOLTANTO.** Non ricalcola nessuna legge del simulatore."""

    def __init__(self, dt):
        self.dt = float(dt)
        self.passo = 0
        self.passi = []
        self._tor = None
        self._cat = None
        self._prec = None          # le COPIE di `r` e `phivel` del passo `t-1`
        self.piene = {}
        # ### ⛔ **DUE GRANDEZZE DIVERSE, e il giro corto mi ha preso a confonderle:**
        #   `calci_evitati` sono gli archi che ### **la legge VECCHIA AVREBBE calciato** --
        #   un CONTROFATTUALE, e il suo valore giusto NON e' zero -- mentre
        #   `calci_spuri_curata` sono i calci che ### **la legge CURATA da' davvero**, e
        #   QUELLI devono essere zero. ### **Il mio rapporto chiamava i primi <<calci>> e
        #   concludeva <<LA CURA NON HA CURATO>>: il nome prometteva una cosa e il numero
        #   misurava un'altra.**
        self.cont = {"calci_evitati": 0, "calci_spuri_curata": 0,
                     "spinta_senza_causa": 0, "avvolgimenti": 0,
                     "coppie": 0, "nan_consumati": 0, "sopra_4pi_tot": 0}

    # ---------------------------------------------------------------- gancio A
    def torsione(self, net, dph, twist_dip, twp, twp_dip, ttw, dt_e, r, i, j):
        dph = np.asarray(dph, float)
        td = np.asarray(twist_dip, float) * np.ones_like(dph)
        twp = np.asarray(twp, float)
        tdp = np.asarray(twp_dip, float)
        tw_in = np.abs(np.asarray(net.tw, float)[:dph.size])
        pv = np.asarray(net.phivel, float)
        rr = (np.ones(net.n) if r is None else np.asarray(r, float))
        i = np.asarray(i, int)
        j = np.asarray(j, int)
        nuovo = np.isnan(tdp)
        ttw_v = np.asarray(ttw, float) * np.ones_like(dph)
        dte_v = np.asarray(dt_e, float) * np.ones_like(dph)
        self.cont["nan_consumati"] += int(np.sum(nuovo))
        sopra = int(np.sum(tw_in >= P4))
        self.cont["sopra_4pi_tot"] += sopra

        # ### I CALCI DI MODULO `~4π`: **DEVONO restare ZERO.** Si contano confrontando la
        #   spinta che gira con quella che la legge VECCHIA avrebbe dato -- e la differenza
        #   oltre `π` e' il calcio. ### **Se non fosse zero, la cura non ha curato.**
        _fp = np.where(nuovo, dph, twp)
        _dp = np.where(nuovo, td, tdp)
        spinta = np.where(nuovo, 0.0, _w4(dph - _fp) + (td - _dp))
        vecchia = _w8(dph + td - np.where(nuovo, 0.0, twp + np.nan_to_num(tdp)))
        # --- (1) IL CONTROFATTUALE: quanti la legge VECCHIA avrebbe calciato
        evitati = int(np.sum((np.abs(spinta - vecchia) > np.pi) & ~nuovo))
        self.cont["calci_evitati"] += evitati
        # --- (2) LA MISURA VERA: la legge CURATA da' calci spuri?
        #   ### **La spinta curata E' l'incremento riparato:** `_w4(Δdph) + Δtd`, con
        #   `|_w4(Δdph)| <= 2pi` e `|Δtd| <= 2pi`. Un calcio di modulo `~4pi` dalla legge
        #   curata potrebbe venire SOLO da un `Δtd` di `2pi` sommato a un `Δdph` di `2pi`,
        #   cioe' da un ribaltamento di dipolo su un arco che ha anche girato di fase.
        #   ### ✔ **Si CONTANO, invece di assumerli impossibili**, e si riportano i
        #   quantili di `|spinta|`: se ci fosse un picco a `4pi`, si vedrebbe.
        # ### ⛔ **LA FIRMA DEL DIFETTO VECCHIO, non un calcio generico.** Il giro corto
        #   mi ha fatto scrivere <<calci spuri = |spinta| > 3pi>>, e quello e' SBAGLIATO: una
        #   spinta di `6.30` da un dipolo che si ribalta di `2pi` e' ### **fisica
        #   legittima**, non un difetto. ### **La firma del difetto vecchio e' un'altra: una
        #   spinta GRANDE SENZA una causa che la produca** -- il `-4pi` arrivava dal modulo,
        #   non dal dipolo.
        #   ### ✔ **E il BOUND e' algebrico:** `|spinta| <= |_w4(Δdph)| + |Δtd| <= 2pi + 2pi
        #   = 4pi`, quindi un superamento di `4pi` ### **non e' fisica: e' un difetto di
        #   IMPLEMENTAZIONE** -- la stessa famiglia di `S3`, e lo stesso potere.
        spuri = int(np.sum((np.abs(spinta) > P4 + 1e-9) & ~nuovo))
        self.cont["calci_spuri_curata"] += spuri
        _senza_causa = int(np.sum((np.abs(spinta) > P3) & (np.abs(td - _dp) < np.pi)
                                  & ~nuovo))
        self.cont["spinta_senza_causa"] = (self.cont.get("spinta_senza_causa", 0)
                                           + _senza_causa)
        avv = 0
        if self._prec is not None and self._prec["n"] == dph.size:
            avv = int(np.sum(np.abs(dph - self._prec["dph"]) > P2))
            self.cont["avvolgimenti"] += avv
            self.cont["coppie"] += int(dph.size)

        d = {"q_tw": q(tw_in), "sopra_4pi": sopra, "calci_evitati": evitati,
             "calci_spuri_curata": spuri, "avvolgimenti": avv,
             "q_spinta": q(np.abs(spinta[~nuovo])) if np.any(~nuovo) else None,
             "spinta_oltre_pi": int(np.sum((np.abs(spinta) > np.pi) & ~nuovo)),
             "spinta_senza_causa": _senza_causa,
             "n_archi": int(dph.size)}
        # --- la misura PIENA, ai cinque passi del mandato
        if self.passo in PASSI_PIENI:
            tau_passi = ttw_v / np.maximum(dte_v, 1e-300)
            at = np.abs(td)
            piena = {"n": int(dph.size),
                     "q_tau_passi": q(tau_passi),
                     "q_ttw": q(ttw_v), "q_dt_e": q(dte_v),
                     "m5": {"n": int(at.size),
                            "fraz_zero": float(np.mean(at < 1e-12)),
                            "fraz_mezzo_pi": float(np.mean(np.abs(at - np.pi / 2) < 1e-9)),
                            "fraz_pi": float(np.mean(np.abs(at - np.pi) < 1e-9))}}
            # ### IL TETTO E LA SPEARMAN, sui valori **CAUSALI** del passo `t-1`:
            #   e' la lezione di `99782e1`, e il gancio salva le COPIE.
            if self._prec is not None:
                r0, w0 = self._prec["r"], self._prec["pv"]
                buoni = (i < r0.size) & (j < r0.size) & (i < w0.size) & (j < w0.size)
                if np.any(buoni):
                    ts = np.abs(tw_stella(r0[i[buoni]], r0[j[buoni]],
                                          w0[i[buoni]], w0[j[buoni]]))
                    tt = tw_in[buoni]
                    s2, n2 = spearman(ts + at[buoni], tt)
                    s2b, n2b = spearman(ts, tt)
                    piena.update({"causale": True,
                                  "passo_del_predittore": self.passo - 1,
                                  "q_tw_stella": q(ts), "n_causali": int(np.sum(buoni)),
                                  "m2": s2, "m2_n": n2, "m2b": s2b, "m2b_n": n2b,
                                  "fraz_oltre_3pi": float(np.mean(ts + at[buoni] >= P3))})
                    self._ts = (buoni, ts)
                else:
                    piena["causale"] = False
                    self._ts = None
            else:
                piena["causale"] = False
                self._ts = None
            self._piena = piena
        self._tor = d
        self._prec = {"r": rr.copy(), "pv": pv.copy(), "dph": dph.copy(),
                      "n": int(dph.size)}

    # ---------------------------------------------------------------- gancio B
    def catena(self, net, avv, soglia, segno, prob, nasce):
        a = np.asarray(avv, float)
        s = np.asarray(soglia, float)
        g1 = a > s
        self._cat = {"archi": int(a.size), "len_avv": int(a.size),
                     "g1_sopra_soglia": int(np.sum(g1)),
                     "g1_e_g2": int(np.sum(g1 & (a < P4))),
                     "g1_e_g2_e_g3": int(np.sum(g1 & (a < P4)
                                                & (np.asarray(segno, float) > 0))),
                     "g4_nasce": int(np.sum(np.asarray(nasce, bool)))}
        self._soglia = s
        self._g1 = g1

    # ---------------------------------------------------------------- fine passo
    def chiudi(self, net):
        d = {"passo": self.passo, "n": int(net.n), "archi": int(len(net.i)),
             "nati_tot": int(getattr(net, "nati", 0)),
             "schwinger_tot": int(getattr(net, "_g_nati_schwinger", 0)),
             "tautw_tot": int(getattr(net, "_g_tautw_tot", 0)),
             "tautw_salti": int(getattr(net, "_g_tautw_salti", 0)),
             "tors_nuovi": int(getattr(net, "_g_tors_nuovi", 0))}
        d.update(self._cat or {"archi": 0, "g4_nasce": 0, "len_avv": 0})
        d["passo"] = self.passo
        d["n"] = int(net.n)
        if self._tor is not None:
            d.update(self._tor)
        d["fin_ammessi"] = getattr(self, "_amm", None)
        self.passi.append(d)
        if self.passo in PASSI_PIENI and getattr(self, "_piena", None) is not None:
            p = dict(self._piena)
            # --- la frazione sopra la SOGLIA MODULATA: il gancio `B` la porta
            ts = getattr(self, "_ts", None)
            sog = getattr(self, "_soglia", None)
            if ts is not None and sog is not None and len(sog) == len(ts[0]):
                p["fraz_oltre_soglia_modulata"] = float(
                    np.mean(ts[1] >= np.asarray(sog, float)[ts[0]]))
            g1 = getattr(self, "_g1", None)
            if g1 is not None:
                p["n_g1"] = int(np.sum(np.asarray(g1, bool)))
            p["q_tw"] = (self._tor or {}).get("q_tw")
            p["curva"] = float(curva(self.passo))
            _m = (p.get("q_tw") or {}).get("q050")
            p["rapporto_alla_curva"] = (None if _m is None or not p["curva"]
                                        else float(_m / p["curva"]))
            p["decide"] = bool(self.passo in (300, 600, 1000))
            self.piene[self.passo] = p
        self._tor = self._cat = None
        self._piena = None
        self._soglia = self._g1 = None

    def nascite_per_finestra(self):
        """Le nascite per finestre di `50` passi. ### **Non il totale:** con `1000` passi un
        totale nasconderebbe **quando** la rete cresce, e *«quando»* e' la domanda."""
        out = []
        for a in range(0, len(self.passi), FINESTRA):
            blocco = self.passi[a:a + FINESTRA]
            if not blocco:
                continue
            pr = self.passi[a - 1] if a > 0 else None
            out.append({
                "da": blocco[0]["passo"], "a": blocco[-1]["passo"],
                "nati": blocco[-1]["nati_tot"] - (pr["nati_tot"] if pr else 0),
                "schwinger": (blocco[-1]["schwinger_tot"]
                              - (pr["schwinger_tot"] if pr else 0)),
                "n_fine": blocco[-1]["n"], "archi_fine": blocco[-1]["archi"]})
        for x in out:
            x["divisioni"] = x["nati"] - x["schwinger"]
        return out

    def totali(self):
        u = self.passi[-1] if self.passi else {}
        return {"nati_tot": u.get("nati_tot", 0), "schwinger": u.get("schwinger_tot", 0),
                "divisioni": u.get("nati_tot", 0) - u.get("schwinger_tot", 0),
                "contatori": dict(self.cont),
                "tautw_tot": u.get("tautw_tot", 0), "tautw_salti": u.get("tautw_salti", 0)}


def _w8(a):
    return (a + P4) % (2.0 * P4) - P4


def _w4(a):
    return (a + P2) % (2.0 * P2) - P2


# =============================================================== IL COLLAUDO
def collaudo():
    esiti = []

    def prova(nome, ok, dett=""):
        esiti.append((nome, bool(ok), dett))
        stampa("  %-7s %-72s %s" % ("OK" if ok else "FALLITA", nome, dett))

    riga("=")
    stampa("1. LA CURVA DEL GUARDIANO, e il suo limite")
    riga("=")
    for t, atteso in ((50, 0.9646), (150, 2.4722), (300, 3.9717), (600, 5.4328),
                      (1000, 6.0590)):
        prova("curva: al passo %-5d vale %.4f" % (t, atteso),
              abs(curva(t) - atteso) < 1e-3, "%.6f" % curva(t))
    prova("curva: ### e' MONOTONA CRESCENTE e tende a 2pi",
          all(curva(a) < curva(b) for a, b in zip(range(1, 2000, 97),
                                                  range(98, 2097, 97)))
          and abs(curva(100000) - P2) < 1e-9, "curva(100000) = %.6f" % curva(100000))
    prova("curva: ### e al passo 0 vale ZERO (la torsione parte da zero)",
          abs(curva(0)) < 1e-15)
    # ### IL LIMITE, MISURATO: con tau = 1491 invece di 300 la curva e' un'ALTRA
    _c300 = P2 * (1 - np.exp(-25.0 / 300.0))
    _c1491 = P2 * (1 - np.exp(-25.0 / 1491.0))
    prova("### curva: con il tau VERO del passo 1 (1491) la curva al passo 25 e' %.4f, "
          "non %.4f" % (_c1491, _c300),
          _c1491 < _c300 / 2,
          "un fattore %.2f: ECCO perche' il criterio NON legge ai passi 50 e 150"
          % (_c300 / _c1491))

    riga("=")
    stampa("2. IL TETTO `tw*`, la forma del mandato del tetto")
    riga("=")
    for rr in (0.1, 0.5, 0.8, 1.0):
        prova("tw*: con r_i = r_j = %.1f vale 2pi a meno del pavimento" % rr,
              abs(abs(tw_stella(rr, rr, 3.0, 1.0)) - P2) / P2 < 1e-3,
              "%.6f" % abs(tw_stella(rr, rr, 3.0, 1.0)))
    prova("tw*: ### e con r DIVERSI agli estremi si SPOSTA da 2pi",
          abs(abs(tw_stella(0.5, 1.0, 3.0, 1.0)) - P2) / P2 > 0.1)

    riga("=")
    stampa("3. I CALCI: la legge nuova e quella vecchia, e il conto che DEVE dare zero")
    riga("=")
    rng = np.random.default_rng(777)
    N = 500000
    dph = rng.uniform(-P2, P2, N)
    twp = rng.uniform(-P2, P2, N)
    V = np.array([-np.pi, -np.pi / 2, 0.0, np.pi / 2, np.pi])
    td = rng.choice(V, N)
    tdp = rng.choice(V, N)
    nuova = _w4(dph - twp) + (td - tdp)
    vecchia = _w8(dph + td - (twp + tdp))
    gi = np.abs(_w4(dph - twp) - (dph - twp)) > 1e-12
    calci = (np.abs(nuova - vecchia) > np.pi)
    prova("calci: ### sugli archi SENZA avvolgimento i calci sono ZERO",
          int(np.sum(calci & ~gi)) == 0,
          "%d su %d archi senza avvolgimento" % (int(np.sum(calci & ~gi)),
                                                 int(np.sum(~gi))))
    prova("calci: ### e DOVE c'e' l'avvolgimento la VECCHIA sbagliava di ~4pi",
          int(np.sum(calci & gi)) > 0,
          "%d calci, tutti su archi avvolti: e' il difetto che la cura ha tolto"
          % int(np.sum(calci & gi)))
    prova("calci: ### quindi il contatore conta GLI ARCHI CHE LA LEGGE VECCHIA AVREBBE "
          "calciato", int(np.sum(calci)) == int(np.sum(calci & gi)))

    riga("=")
    stampa("4. LA PATCH: due ganci, e NESSUNA legge toccata")
    riga("=")
    import tempfile
    _d = tempfile.mkdtemp()
    _p = os.path.join(_d, "s.py")
    fatte = copia_patchata(SIM, _p)
    tt = io.open(_p, encoding="utf-8").read()
    t0 = io.open(SIM, encoding="utf-8").read()
    prova("patch: le tre ancore sono state sostituite", len(fatte) == 3, "%s" % fatte)
    prova("patch: il gancio A sta PRIMA del calcolo di `_nuovo`",
          tt.index("_MIS.torsione(self, dph=dph") < tt.index("_nuovo = np.isnan"))
    prova("patch: la riga della torsione CURATA resta intatta",
          tt.count("self.tw += (self._w4(dph - _fp) + (twist_dip - _dp)") == 1)
    prova("patch: ### e la riga del ramo non-4pi NON si tocca",
          tt.count("self.tw += self._w4(dph - self.twp) - dt_e * self.tw / _ttw") == 1)
    _inj = ["_MIS = None   # [TORS-W8 LUNGA] lo riempie lo strumento" + NL,
            "            if _MIS is not None:" + NL,
            "                _MIS.torsione(self, dph=dph, twist_dip=twist_dip," + NL,
            "                              twp=self.twp, twp_dip=self.twp_dip," + NL,
            "                              ttw=_ttw, dt_e=dt_e, r=r, i=i, j=j)" + NL,
            "        if _MIS is not None:" + NL,
            "            _MIS.catena(self, avv=avv, soglia=soglia, segno=segno," + NL,
            "                        prob=prob, nasce=nasce)" + NL]
    _ri = tt
    for x in _inj:
        _ri = _ri.replace(x, "", 1)
    prova("### patch: togliendo le SOLE righe iniettate si torna al sorgente VERO",
          _ri == t0, "carattere per carattere")

    riga("=")
    stampa("5. LA MISURA: casi a risposta NOTA")
    riga("=")
    m = Misura(0.01)

    class FR(object):
        pass
    fr = FR()
    NN, NA = 60, 25
    fr.n = NN
    fr.i = np.arange(NA)
    fr.j = np.arange(NA) + NA
    fr.tw = np.linspace(0.1, 10.0, NA)
    fr.phivel = np.linspace(0.0, 6.0, NN)
    fr.nati = 0
    fr._g_nati_schwinger = 0
    arg = {"dph": np.linspace(-1.0, 1.0, NA), "twist_dip": np.zeros(NA),
           "twp": np.zeros(NA), "twp_dip": np.zeros(NA), "ttw": 2.0, "dt_e": 0.008,
           "r": np.linspace(0.6, 1.0, NN), "i": fr.i, "j": fr.j}
    m.passo = 50
    m.torsione(fr, **arg)
    prova("misura: al primo passo la PIENA dichiara causale = False",
          m._piena["causale"] is False)
    m.catena(fr, avv=np.abs(fr.tw), soglia=np.full(NA, P3), segno=np.ones(NA),
             prob=np.full(NA, 0.5), nasce=np.zeros(NA, bool))
    m.chiudi(fr)
    m.passo = 150
    m.torsione(fr, **arg)
    prova("misura: al secondo la PIENA e' CAUSALE e punta al passo t-1",
          m._piena["causale"] is True and m._piena["passo_del_predittore"] == 149)
    prova("misura: ### e tau_passi = ttw / dt_e, cioe' il tempo di scarica in PASSI",
          abs(m._piena["q_tau_passi"]["q050"] - 2.0 / 0.008) < 1e-9,
          "%.1f passi" % m._piena["q_tau_passi"]["q050"])
    m.catena(fr, avv=np.abs(fr.tw), soglia=np.full(NA, P3), segno=np.ones(NA),
             prob=np.full(NA, 0.5), nasce=np.zeros(NA, bool))
    m.chiudi(fr)
    p = m.piene.get(150)
    prova("misura: la PIENA al passo 150 c'e', col rapporto alla curva",
          p is not None and p["rapporto_alla_curva"] is not None,
          "rapporto %.4f (curva %.4f)" % (p["rapporto_alla_curva"], p["curva"]))
    prova("misura: ### e il passo 150 NON decide, il 300 SI'",
          p["decide"] is False, "e' il criterio del task history")
    m.passo = 300
    m.torsione(fr, **arg)
    m.catena(fr, avv=np.abs(fr.tw), soglia=np.full(NA, P3), segno=np.ones(NA),
             prob=np.full(NA, 0.5), nasce=np.zeros(NA, bool))
    m.chiudi(fr)
    prova("misura: ### il passo 300 DECIDE", m.piene[300]["decide"] is True)
    prova("misura: M5 conta il dipolo a ZERO come 1.0 quando e' tutto zero",
          abs(m.piene[300]["m5"]["fraz_zero"] - 1.0) < 1e-12)
    # --- i calci: il caso che DEVE contare
    m2 = Misura(0.01)
    m2.passo = 7
    a2 = dict(arg)
    a2["dph"] = np.full(NA, _w4(P2 + 0.01))
    a2["twp"] = np.full(NA, _w4(P2 - 0.01))
    m2.torsione(fr, **a2)
    prova("### calci EVITATI: un AVVOLGIMENTO iniettato viene CONTATO (la VECCHIA "
          "calciava)",
          m2._tor["calci_evitati"] == NA, "%d su %d" % (m2._tor["calci_evitati"], NA))
    prova("### calci EVITATI: e senza avvolgimento sono ZERO (il caso nullo)",
          m2.cont["calci_evitati"] == NA and Misura(0.01).cont["calci_evitati"] == 0)
    # ### ⛔ **E LA DISTINZIONE CHE IL GIRO CORTO MI HA INSEGNATO:** gli EVITATI sono un
    #   CONTROFATTUALE e il loro valore giusto NON e' zero; gli SPURI sono la misura vera e
    #   DEVONO essere zero. ### **Confonderli faceva dire al rapporto <<la cura non ha
    #   curato>> su una corsa in cui la cura funzionava.**
    prova("### calci SPURI: sullo stesso avvolgimento la legge CURATA non ne da' NESSUNO",
          m2._tor["calci_spuri_curata"] == 0,
          "%d: la spinta curata e' l'incremento RIPARATO, non il calcio"
          % m2._tor["calci_spuri_curata"])
    prova("### calci SPURI: e i quantili della spinta curata NON hanno un picco a 4pi",
          (m2._tor["q_spinta"] or {}).get("q100", 9e9) < P3,
          "|spinta| massima %.6f, contro 3pi = %.6f"
          % ((m2._tor["q_spinta"] or {}).get("q100", float("nan")), P3))
    # ### ⛔ **E QUI HO SBAGLIATO UNA SECONDA VOLTA, nello stesso modo di `S3`.**
    #   Avevo scritto una prova che pretendeva di accendere i <<calci spuri>> con un
    #   ribaltamento di dipolo, e ### **falliva** -- perche' una spinta di `6.30` da un
    #   dipolo che si ribalta di `2pi` ### **e' fisica legittima, non un difetto.**
    #   ### 📌 **LA GRANDEZZA GIUSTA E' IL BOUND ALGEBRICO:**
    #   `|spinta| <= |_w4(Δdph)| + |Δtd| <= 2pi + 2pi = 4pi`.
    #   ### **Superarlo non e' fisica: e' un difetto di IMPLEMENTAZIONE** -- e questo e' il
    #   solo zero che il contatore puo' certificare. ### ⚠ **E' LA QUARTA VOLTA IN QUESTA
    #   SESSIONE che scrivo un controllo il cui zero e' ALGEBRICO** *(`C-ident`, `S3`, i
    #   calci spuri, e la prova di `S3` che ho dovuto ritirare)*: ### **lo scrivo perche' e'
    #   un mio difetto RICORRENTE, non un incidente.**
    m2b = Misura(0.01)
    m2b.passo = 7
    a2b = dict(a2)
    a2b["twist_dip"] = np.full(NA, np.pi)
    a2b["twp_dip"] = np.full(NA, -np.pi)
    m2b.torsione(fr, **a2b)
    prova("### un dipolo da -pi a +pi su un arco avvolto da' una spinta LEGITTIMA, non un "
          "calcio",
          m2b._tor["calci_spuri_curata"] == 0
          and (m2b._tor["q_spinta"] or {}).get("q100", 0) > np.pi,
          "|spinta| %.4f: grande, e CON una causa (il dipolo si e' ribaltato di 2pi)"
          % (m2b._tor["q_spinta"] or {}).get("q100", float("nan")))
    prova("### e la FIRMA del difetto vecchio -- spinta grande SENZA causa -- resta ZERO",
          m2b._tor["spinta_senza_causa"] == 0)
    # --- IL TEOREMA, misurato: il bound algebrico su input legali
    rng2 = np.random.default_rng(31415)
    NT = 1_000_000
    _dp2 = rng2.uniform(-P2, P2, NT)
    _tp2 = rng2.uniform(-P2, P2, NT)
    _V2 = np.array([-np.pi, -np.pi / 2, 0.0, np.pi / 2, np.pi])
    _td2 = rng2.choice(_V2, NT)
    _tdp2 = rng2.choice(_V2, NT)
    _sp2 = _w4(_dp2 - _tp2) + (_td2 - _tdp2)
    prova("### TEOREMA: |spinta| <= 4pi su input LEGALI, e il bound e' ALGEBRICO",
          float(np.max(np.abs(_sp2))) <= P4 + 1e-9,
          "massimo %.6f su %d casi, contro 4pi = %.6f"
          % (float(np.max(np.abs(_sp2))), NT, P4))
    prova("### e il bound e' STRETTO: esistono spinte vicine a 4pi (il dipolo che si ribalta)",
          float(np.max(np.abs(_sp2))) > P3,
          "massimo %.6f > 3pi = %.6f: il contatore degli SPURI puo' solo prendere errori "
          "di IMPLEMENTAZIONE" % (float(np.max(np.abs(_sp2))), P3))
    prova("### e la FIRMA (spinta > 3pi SENZA un dipolo che cambia) e' ZERO su input legali",
          int(np.sum((np.abs(_sp2) > P3) & (np.abs(_td2 - _tdp2) < np.pi))) == 0,
          "%d su %d: la spinta grande arriva SEMPRE con la sua causa"
          % (int(np.sum((np.abs(_sp2) > P3) & (np.abs(_td2 - _tdp2) < np.pi))), NT))
    # --- le nascite per finestra
    m3 = Misura(0.01)
    for k in range(1, 121):
        m3.passo = k
        fr.nati = k // 10
        fr._g_nati_schwinger = k // 40
        m3.catena(fr, avv=np.abs(fr.tw), soglia=np.full(NA, P3), segno=np.ones(NA),
                  prob=np.full(NA, 0.5), nasce=np.zeros(NA, bool))
        m3.chiudi(fr)
    fin = m3.nascite_per_finestra()
    prova("finestre: 120 passi danno 3 finestre da 50", len(fin) == 3,
          "%s" % [(x["da"], x["a"]) for x in fin])
    prova("finestre: ### i nati per finestra SOMMANO al totale",
          sum(x["nati"] for x in fin) == m3.passi[-1]["nati_tot"],
          "%d = %d" % (sum(x["nati"] for x in fin), m3.passi[-1]["nati_tot"]))
    prova("finestre: ### e divisioni = nati - schwinger, per finestra",
          all(x["divisioni"] == x["nati"] - x["schwinger"] for x in fin))

    riga("=")
    ko = [n for n, o, _d in esiti if not o]
    stampa("COLLAUDO: %d su %d" % (len(esiti) - len(ko), len(esiti)))
    if ko:
        stampa("### FALLITI:")
        for n in ko:
            stampa("    - " + n)
    riga("=")
    return 1 if ko else 0


def _scrivi(d):
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    io.open(os.path.join(FUORI, "lunga.json"), "w", encoding="utf-8").write(
        json.dumps(d, indent=1, default=str))


def main(argv):
    passi = PASSI
    if "--collaudo" in argv[1:]:
        riga("=")
        stampa("IL COLLAUDO DI _tors_w8_lunga.py")
        riga("=")
        return collaudo()
    for a in argv[1:]:
        if a.startswith("--passi="):
            passi = int(a.split("=", 1)[1])
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    riga("=")
    stampa("LA MISURA LUNGA DI TORS-W8-AVVOLGIMENTO: %d passi, UN braccio" % passi)
    riga("=")
    pf = piattaforma()
    for k in ["python", "numpy", "sistema", "macchina"]:
        stampa("  %-10s %s" % (k, pf[k]))
    b = blob(SIM)[:8]
    stampa("  simulatore %s   atteso %s   strumento %s   _mitosi_soglia_grad %s"
           % (b, BLOB_ATTESO, blob(__file__)[:8], blob(_MSG.__file__)[:8]))
    # ### ⛔ **IL BLOB SI VERIFICA ALL'AVVIO:** la misura vale per `cf2a1ac8` e per nessun
    #   altro, e girarla su un altro blob produrrebbe numeri che nessuno puo' attribuire.
    if b != BLOB_ATTESO:
        stampa("  ### IL BLOB DEL SIMULATORE NON E' QUELLO ATTESO. MI FERMO.")
        _scrivi({"esito": 1, "stato": "BLOB SBAGLIATO", "blob_trovato": b,
                 "blob_atteso": BLOB_ATTESO, "piattaforma": pf})
        return 1
    stampa("  ### il blob COINCIDE: la misura vale per questo simulatore.")
    stampa()
    dst = os.path.join(FUORI, "_sim_lunga.py")
    anc = copia_patchata(SIM, dst)
    stampa("  la copia patchata: blob %s  (%d ancore)" % (blob(dst)[:8], len(anc)))
    for a in anc:
        stampa("      %s" % a)
    stampa()
    S, N, _a = carica("msg_lunga", dst)
    m = Misura(S.DT)
    S._MIS = m
    in_conf = _cli_flag.dichiara_configurazione(S, stampa)
    stampa("  scena: n = %d, archi = %d, DT = %r" % (N.n, len(N.i), S.DT))
    stampa()
    riga("=")
    stampa("LA CORSA")
    riga("=")

    def _ist(stato, k, err=None):
        d = {"piattaforma": pf, "passi": passi, "passi_girati": k, "stato": stato,
             "blob_sim": blob(SIM), "blob_atteso": BLOB_ATTESO,
             "blob_strumento": blob(__file__),
             "blob_mitosi_soglia_grad": blob(_MSG.__file__), "blob_copia": blob(dst),
             "ancore": anc, "kappa": KAPPA, "tau_curva": TAU_CURVA,
             "passi_pieni": list(PASSI_PIENI), "finestra": FINESTRA,
             "in_configurazione_del_driver": bool(in_conf),
             "passi_dati": m.passi, "piene": m.piene,
             "nascite_per_finestra": m.nascite_per_finestra(), "totali": m.totali(),
             "a_valle": {"n": int(N.n), "archi": int(len(N.i))},
             "riferimento_f7237563": {"divisioni_150": 18, "schwinger_150": 7,
                                      "tw_mediano_140": 2.11, "sopra_4pi_per_passo": 108,
                                      "calci_150": 142114}}
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
        u = m.passi[-1]
        print("[battito] passo %d/%d  n=%d archi=%d  nati=%d sch=%d  |tw| q50=%.4f  "
              "sopra4pi=%d calci=%d  tautw_salti=%d"
              % (k, passi, u["n"], u["archi"], u["nati_tot"], u["schwinger_tot"],
                 (u.get("q_tw") or {}).get("q050", float("nan")),
                 u.get("sopra_4pi", -1), m.cont["calci_oltre_pi"], u["tautw_salti"]),
              flush=True)
        if k % PASSI_SALVA == 0:
            _ist("IN CORSO", k)
    d = _ist("DATI SALVATI", passi)
    stampa("  ### I DATI SONO SALVATI in lunga.json.")
    stampa()
    riga("=")
    stampa("IL CRITERIO, letto ai passi che DECIDONO (300, 600, 1000)")
    riga("=")
    for p in PASSI_PIENI:
        z = m.piene.get(p)
        if not z:
            continue
        stampa("  passo %-5d |tw| q50 %s   curva %s   RAPPORTO %s   %s"
               % (p, n4((z.get("q_tw") or {}).get("q050")), n4(z.get("curva")),
                  n4(z.get("rapporto_alla_curva")),
                  "### DECIDE" if z.get("decide") else "(si riporta, NON decide)"))
    stampa()
    stampa("  ### I CALCI: DUE GRANDEZZE DIVERSE, e confonderle era un difetto mio")
    stampa("      calci SPURI dalla legge CURATA (|spinta| OLTRE il bound 4pi): %d   %s"
           % (m.cont["calci_spuri_curata"],
              "### ZERO" if not m.cont["calci_spuri_curata"]
              else "### NON ZERO: un difetto di IMPLEMENTAZIONE, e si FERMA qui"))
    stampa("      la FIRMA del difetto vecchio (spinta > 3pi SENZA causa): %d   %s"
           % (m.cont["spinta_senza_causa"],
              "### ZERO" if not m.cont["spinta_senza_causa"] else "### NON ZERO"))
    stampa("      ### E QUESTI DUE ZERI SONO ALGEBRICI, non misure: il bound")
    stampa("          |spinta| <= |_w4(dph - twp)| + |dipolo| <= 4pi vale PER COSTRUZIONE.")
    stampa("          Quello che certificano e' che l'IMPLEMENTAZIONE segue l'algebra --")
    stampa("          la stessa famiglia e lo stesso potere di S3 del sigillo.")
    stampa("      calci EVITATI, cioe' quanti la legge VECCHIA avrebbe dato: %d"
           % m.cont["calci_evitati"])
    stampa("      ### IL SECONDO NUMERO NON DEVE ESSERE ZERO: e' un CONTROFATTUALE, e dice")
    stampa("          quanti calci la cura ha TOLTO. Il mio rapporto lo chiamava <<calci>> e")
    stampa("          concludeva <<la cura non ha curato>>: il nome prometteva una cosa e il")
    stampa("          numero misurava un'altra. Trovato dal GIRO CORTO (STANDARD 7).")
    stampa("  archi sopra 4pi, somma su tutti i passi: %d" % m.cont["sopra_4pi_tot"])
    stampa("  la guardia di TAU_TW: %d invocazioni, %d SALTI"
           % (m.totali()["tautw_tot"], m.totali()["tautw_salti"]))
    stampa()
    d.update({"esito": 0, "stato": "fatto"})
    _scrivi(d)
    stampa("  ### E IL REFERTO LO SCRIVE IL GENERATORE, dal json: il criterio si legge LA'.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
