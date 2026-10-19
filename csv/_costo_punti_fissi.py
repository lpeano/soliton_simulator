# -*- coding: utf-8 -*-
r"""**IL COSTO DEI PUNTI FISSI DEL TICK, MISURATO A TEMPO** — *il passo `B` della memoria.*

> ### ⛔ **PERCHE' ESISTE** *(`2026-10-19`)*: il task history
> `2026-10-18_memoria_e_punti_fissi.md` vuole ### **la quota del tempo del tick** di
> ciascuno dei `3` punti fissi del percorso del tick *(il passo `A`, `ce338b9c`)*, e il
> suo punto `(a)` dice che ### **i contatori dei giri NON bastano**: un giro di `cs` e un
> giro di `Omega` non costano uguale, e ### **`mot.giri_omega` conta solo l'ULTIMA
> applicazione.** ### **Quindi si misura il TEMPO.**

## ⛔ LA CONFIGURAZIONE E' QUELLA DI `C5`, NON UNA MIA

### **Col passo di default la forma `cs` e' SPENTA** *(`mot.cs is None`)* e ### **nessuno
dei tre gira**: misurarla darebbe ### **tre zeri, che sono un FALSO ZERO.** Si misura
quindi ### **con `cs` acceso**, sulla scena e sui `Lambda_c` di `C5`
*(`_misura_strada_d.informazione_costo`)*: `DV.scena(MB2.NN, MB2.SEME, 0.25, ...)`, lo
stato della pre-corsa, ### **`8` tick**, e `Lambda_c` presi da `D2.SPAZZATA`.
### ⚠ **Sulla seconda taglia** (`32`, come `_misura_punto_medio.TAGLIE`) si tengono
### **gli STESSI RAPPORTI** `Lambda_c/Lambda_medio` di `C5`, e lo stato e' quello della
### **stessa pre-corsa** sulla rete di quella taglia *(la costruzione di
`_misura_punto_medio.pendenza_di_g`)*.

## ⭐ CHE COSA SI MISURA, PER OGNI PUNTO FISSO

### **acceso o spento** *(ha iterato almeno una volta?)*, ### **giri medi e massimi** per
chiamata, e ### **la quota del tempo del tick**. ### ⚠ **E i due punti fissi accesi sono
ANNIDATI** *(il mezzo palindromo di `cs_al_centro` contiene `CAMM-FASE-VUOTO`)*: il tempo
di `Omega` si riporta ### **dentro `cs` e fuori**, e la quota di `cs` ### **lo contiene.**

## ⛔ IL CONTROLLO CHE PUO' FALLIRE, E LA SUA SOGLIA NON SI SCEGLIE

### **Il tempo misurato deve tornare coi giri per il costo di UN giro**, misurato a parte:
```
cs_al_centro      T  ~  somma sulle chiamate  giri * c(giro di cs)
applica (Omega)   T  ~  somma sulle chiamate  (giri + 1) * c(giro di Omega)
```
*(il `+1` di `Omega` e' la valutazione iniziale piu' la fase finale, che il corpo del
ciclo fa una volta in piu'; `cs` fa la prima ipotesi FUORI dal ciclo, ed e' un costo per
chiamata che si riporta a parte)*.
### ✅ **La soglia e' la dispersione delle ripetizioni** *(`P1-sexies`: si deriva dal
nullo)*: `|T - T_previsto| <= 3 sqrt(s_T^2 + s_prev^2)`, con `s` la deviazione standard
su ### **`5` ripetizioni** *(`P3`: almeno `4`)*.
### ⛔ **IL CASO CHE DEVE FALLIRE e' il conto di `C5`:** i giri di `Omega` letti da
`mot.giri_omega` ### **una volta per tick** *(l'ultima applicazione)*. Se il criterio
**non** lo boccia, ### **il criterio non distingue niente.**
### ⛔ **E SE IL CONTROLLO VERO NON TORNA, c'e' un costo non capito:** si scrive e ### **ci
si FERMA** *(par.`2` del task history)*.

## ⭐ I DUE BRACCI DI RIFERIMENTO

### **`cs` SPENTO:** lo stesso tick *(`tick.tick`)*, e ### **i tre devono dare quota `0`**
*(nessuna iterazione)*. ### ⚠ **`applica` viene CHIAMATA anche la'** e torna subito: il
suo tempo **non e' zero** *(e' la chiamata)*, e si riporta a parte da quello delle chiamate
che ### **hanno iterato**, che deve essere ### **zero esatto.**
### **L'involucro inerte** *(`STANDARD 5`)*: ogni braccio strumentato ha ### **un braccio
NUDO** nella stessa configurazione, e lo stato finale ### **deve coincidere al byte**
*(`sha1` di `psi_h`, `phi_h` e `mot.cs`)*.
### **Un processo per braccio** *(`STANDARD 1`)*.

Gira con:  python csv/_costo_punti_fissi.py
Un braccio da solo (lo usa il driver):
           python csv/_costo_punti_fissi.py --braccio TAGLIA IRAPPORTO MODO INVOLUCRO
           (IRAPPORTO = indice in D2.SPAZZATA; MODO = acceso|spento;
            INVOLUCRO = strumentato|nudo)
Il giro corto (STANDARD 7):  python csv/_costo_punti_fissi.py --corto
"""
import hashlib
import io
import json
import os
import subprocess
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

# ### ⛔ **I NUMERI DELLA MISURA, e da dove vengono:** nessuno e' scelto qui.
TAGLIE = (16, 32)            # _misura_punto_medio.TAGLIE: <<due taglie>> del task history
DTAU = 0.25                  # quello di C5 (_misura_strada_d.informazione_costo)
TICK = 8                     # quelli di C5
RIPETIZIONI = 5              # P3: per una barra ne servono ALMENO 4
SIGMA = 3.0                  # la soglia in deviazioni standard: P1-sexies (3 sigma)


# =====================================================================================
#   LA SCENA, uguale a quella di C5
# =====================================================================================
def scena(taglia):
    """### `(inc, mot, st, par)` con lo stato della PRE-CORSA, ### **come in `C5`.**"""
    import _misura_hw as HW
    import _misura_mb2 as MB2
    import composizione as CM
    import deriva as DV
    import tick as TK
    inc, mot, st, par = DV.scena(taglia, MB2.SEME, DTAU, norma=MB2.NORMA,
                                 vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
    if taglia == MB2.NN:
        st["psi_h"][...], st["phi_h"][...] = HW.stato_non_uniforme()
    else:
        _i2, m2, s2, p2 = DV.scena(taglia, MB2.SEME, HW.DTAU_PRE, norma=MB2.NORMA,
                                   vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
        for _t in range(int(round(MB2.TEMPO / HW.DTAU_PRE))):
            TK.percorri_tick(s2, m2, p2, ("CAMM-FASE-VUOTO",), None, len(CM.ORDINE))
        st["psi_h"][...], st["phi_h"][...] = s2["psi_h"], s2["phi_h"]
    return inc, mot, st, par


def lambda_c(taglia, irapporto):
    """### `(Lambda_c, Lambda_medio, rapporto)`: ### **il rapporto e' quello di `C5`.**

    ### ⚠ **Sulla taglia di `C5` `Lambda_c` e' il valore di `SPAZZATA` TALE E QUALE**
    *(cosi' e' al bit quello di `C5`)*; sull'altra e' ### **lo stesso rapporto** per il
    vuoto medio di quella rete.
    """
    import _collauda_cs_centro as D2
    import _misura_mb2 as MB2
    _i, m16, s16, _p = scena(MB2.NN)
    lam16 = float(np.mean(m16.densita_vuoto(s16)))
    r = D2.SPAZZATA[irapporto] / lam16
    if taglia == MB2.NN:
        return float(D2.SPAZZATA[irapporto]), lam16, r
    _i, m, s, _p = scena(taglia)
    lam = float(np.mean(m.densita_vuoto(s)))
    return r * lam, lam, r


# =====================================================================================
#   L'INVOLUCRO: tempo e giri per chiamata, IN MEMORIA
# =====================================================================================
class Involucro(object):
    """### Avvolge i tre punti fissi e conta ### **tempo e giri di OGNI chiamata.**

    ### ⛔ **Non tocca nessun file:** sostituisce tre attributi di modulo per la durata
    del braccio, e ### **`STANDARD 5` verifica che lo stato finale non cambi.**
    """

    def __init__(self):
        import energia_pesata as EP
        import flussi_parziali as FP
        import tick as TK
        self.EP, self.FP, self.TK = EP, FP, TK
        self.veri = (TK.cs_al_centro, EP.applica, FP.hop_phi_punto_medio)
        self.dentro_cs = False
        self.azzera()

    def azzera(self):
        self.cs = []          # (secondi, giri)
        self.om = []          # (secondi, giri, dentro_cs)
        self.pm = []          # (secondi, giri)

    def installa(self):
        TK, EP, FP = self.TK, self.EP, self.FP
        v_cs, v_om, v_pm = self.veri
        io_ = self

        def cs_al_centro(st, mot, par, lc, fp, salta):
            io_.dentro_cs = True
            t0 = time.perf_counter()
            try:
                c, giri = v_cs(st, mot, par, lc, fp, salta)
            finally:
                io_.dentro_cs = False
            io_.cs.append((time.perf_counter() - t0, giri))
            return c, giri

        def applica(mot, st, par, frazione):
            mot.giri_omega = 0
            t0 = time.perf_counter()
            r = v_om(mot, st, par, frazione)
            io_.om.append((time.perf_counter() - t0, mot.giri_omega, io_.dentro_cs))
            return r

        def hop_phi_punto_medio(mot, st, frazione, regola):
            mot.giri_peso = 0
            t0 = time.perf_counter()
            r = v_pm(mot, st, frazione, regola)
            io_.pm.append((time.perf_counter() - t0, mot.giri_peso))
            return r

        TK.cs_al_centro = cs_al_centro
        EP.applica = applica
        FP.hop_phi_punto_medio = hop_phi_punto_medio

    def togli(self):
        self.TK.cs_al_centro, self.EP.applica, self.FP.hop_phi_punto_medio = self.veri


def _firma(st, mot):
    h = hashlib.sha1()
    for k in ("psi_h", "phi_h"):
        h.update(np.ascontiguousarray(st[k]).tobytes())
    h.update(b"-" if mot.cs is None else np.ascontiguousarray(mot.cs).tobytes())
    return h.hexdigest()[:16]


def _copia(st):
    return {k: (v.copy() if hasattr(v, "copy") else v) for k, v in st.items()}


# =====================================================================================
#   IL COSTO DI UN GIRO, misurato A PARTE
# =====================================================================================
def costo_giro_cs(st, mot, par, lc):
    """### Il tempo del CORPO del ciclo di `cs_al_centro`, ### **una volta.**

    ### ⚠ **E' una COPIA del corpo** *(`tick.cs_al_centro`)*, dichiarata: copia, mezzo
    palindromo col `cs` dello stato, e la `cs` del centro. ### **Il mezzo palindromo
    contiene il punto fisso di `Omega`**, quindi il costo di un giro ### **lo include.**
    """
    import flussi_parziali as FP
    import tick as TK
    meta = TK.meta_del_palindromo()
    fp = mot._b("tk_cs", (mot.inc.n,), float)
    prec = FP.cs(mot.densita_vuoto(st), lc, fp).copy()
    t0 = time.perf_counter()
    copia = _copia(st)
    mot.cs = prec
    TK.percorri_tick(copia, mot, par, (), None, meta)
    nuovo = FP.cs(mot.densita_vuoto(copia), lc, fp).copy()
    float(np.max(np.abs(nuovo - prec)))
    return time.perf_counter() - t0


def costo_giro_om(st, mot, par):
    """### Il tempo del CORPO del ciclo di `energia_pesata.applica`, ### **una volta.**

    ### ⚠ **Copia del corpo**, dichiarata: mezza fase, poi `Omega` riletto.
    """
    import energia_pesata as EP
    copia = _copia(st)
    tau = float(mot.dtau[0]) * 0.5
    phi = copia["phi_h"]
    salvo = phi.copy()
    prec = EP.omega(mot, copia, par).copy()
    t0 = time.perf_counter()
    np.multiply(salvo, np.exp(-1j * (prec * (tau * 0.5))[mot.inc.nodo]), out=phi)
    nuovo = EP.omega(mot, copia, par)
    float(np.max(np.abs(nuovo - prec)))
    nuovo.copy()
    return time.perf_counter() - t0


# =====================================================================================
#   UN BRACCIO, in un processo suo
# =====================================================================================
def braccio(taglia, irapporto, modo, involucro):
    import flussi_parziali as FP
    import tick as TK
    lc, lam, rapp = lambda_c(taglia, irapporto)
    fuori = {"taglia": taglia, "irapporto": irapporto, "modo": modo,
             "involucro": involucro, "lambda_c": lc, "lambda_medio": lam,
             "rapporto": rapp}
    inc, mot, st0, par = scena(taglia)
    inv = Involucro() if involucro == "strumentato" else None
    # ### il costo di UN giro, A PARTE e PRIMA dell'involucro
    if involucro == "strumentato" and modo == "acceso":
        FP.accendi_cs(mot, lc, st0)
        fuori["giro_cs"] = [costo_giro_cs(st0, mot, par, lc) for _ in range(TICK)]
        FP.accendi_cs(mot, lc, st0)
        fuori["giro_om"] = [costo_giro_om(st0, mot, par) for _ in range(TICK)]
        FP.spegni_cs(mot)
    ripetizioni = []
    firme = set()
    try:
        if inv is not None:
            inv.installa()
        for _r in range(RIPETIZIONI if inv is not None else 1):
            st = _copia(st0)
            if inv is not None:
                inv.azzera()
            if modo == "acceso":
                FP.accendi_cs(mot, lc, st)
            else:
                FP.spegni_cs(mot)
            fine = []
            t0 = time.perf_counter()
            for _t in range(TICK):
                if modo == "acceso":
                    TK.tick_con_cs(st, mot, par, lc, ())
                else:
                    TK.tick(st, mot, par)
                if inv is not None:
                    fine.append(len(inv.om))
            T = time.perf_counter() - t0
            firme.add(_firma(st, mot))
            rip = {"T_tick": T}
            if inv is not None:
                rip["cs"] = inv.cs
                rip["om"] = inv.om
                rip["pm"] = inv.pm
                rip["fine_tick"] = fine
            ripetizioni.append(rip)
    except AssertionError as e:
        fuori["non_converge"] = str(e)[:160]
    finally:
        if inv is not None:
            inv.togli()
    fuori["ripetizioni"] = ripetizioni
    fuori["firme"] = sorted(firme)
    return fuori


def lancia(taglia, irapporto, modo, involucro):
    """### Un braccio ### **in un processo suo** *(`STANDARD 1`)*: l'ultima riga e' JSON."""
    out = subprocess.run(
        [sys.executable, os.path.abspath(__file__), "--braccio", str(taglia),
         str(irapporto), modo, involucro], capture_output=True)
    righe = out.stdout.decode("utf-8", "replace").strip().splitlines()
    assert out.returncode == 0 and righe, (
        "il braccio %r e' morto (codice %d): %s" % ((taglia, irapporto, modo, involucro),
                                                   out.returncode,
                                                   out.stderr.decode("utf-8", "replace")
                                                   [-800:]))
    return json.loads(righe[-1])


# =====================================================================================
#   LA LETTURA
# =====================================================================================
def _ms(x):
    return 1e3 * x


def leggi(b):
    """### Le quote, i giri, e il controllo ### **misurato contro previsto.**"""
    rr = b["ripetizioni"]
    T = np.array([r["T_tick"] for r in rr])
    cs_t = np.array([sum(x[0] for x in r["cs"]) for r in rr])
    om_in = np.array([sum(x[0] for x in r["om"] if x[2] and x[1] > 0) for r in rr])
    om_fu = np.array([sum(x[0] for x in r["om"] if not x[2] and x[1] > 0) for r in rr])
    om_tutte = np.array([sum(x[0] for x in r["om"]) for r in rr])
    om_iter = om_in + om_fu
    pm_t = np.array([sum(x[0] for x in r["pm"] if x[1] > 0) for r in rr])
    giri_cs = [x[1] for x in rr[0]["cs"]]
    giri_om = [x[1] for x in rr[0]["om"]]
    giri_pm = [x[1] for x in rr[0]["pm"]]
    L = {"T": T, "cs": cs_t, "om_in": om_in, "om_fu": om_fu, "om_iter": om_iter,
         "om_tutte": om_tutte, "pm": pm_t, "giri_cs": giri_cs, "giri_om": giri_om,
         "giri_pm": giri_pm, "n_om": len(giri_om), "n_pm": len(giri_pm)}
    if "giro_cs" in b:
        gcs = np.array(b["giro_cs"])
        gom = np.array(b["giro_om"])
        L["c_cs"], L["c_om"] = gcs, gom
        n_cs = float(sum(giri_cs))
        n_om = float(sum(g + 1 for g in giri_om if g > 0))
        # ### ⛔ **IL CASO CHE DEVE FALLIRE, il conto di `C5`:** `Omega` letto
        # ### ### **una volta per tick** dall'ultima applicazione.
        # ### ⚠ **le applicazioni per tick NON sono uguali** *(dipendono dai giri di
        # ### `cs`)*: si usano ### **i confini dei tick registrati.**
        ultima = [giri_om[f - 1] for f in rr[0]["fine_tick"]]
        n_c5 = float(sum(g + 1 for g in ultima if g > 0))
        # ### ⚠ **l'incertezza del previsto e' l'ERRORE STANDARD del costo di un giro**
        # ### *(`TICK` campioni)*, per il numero di giri.
        def prev(n, c):
            return (n * float(np.mean(c)),
                    n * float(np.std(c, ddof=1)) / float(np.sqrt(len(c))))
        L["prev_cs"] = prev(n_cs, gcs)
        L["prev_om"] = prev(n_om, gom)
        L["prev_c5"] = prev(n_c5, gom)
    return L


def torna(misura, previsto):
    """### `(torna?, scarto, soglia)`: ### **`3 sigma` delle due dispersioni.**"""
    m, sm = float(np.mean(misura)), float(np.std(misura, ddof=1))
    p, sp = previsto
    soglia = SIGMA * float(np.sqrt(sm * sm + sp * sp))
    return abs(m - p) <= soglia, m - p, soglia


def collaudo_del_criterio():
    """### `P1-sexies`: ### **il criterio su due casi a risposta NOTA**, prima del vero."""
    r = np.random.default_rng(0)
    base = 1.0 + 0.01 * r.standard_normal(RIPETIZIONI)
    giusto = torna(base, (1.0, 0.01))[0]
    sbagliato = torna(base, (0.5, 0.005))[0]
    return giusto, sbagliato


def main(argv):
    if argv[:1] == ["--braccio"]:
        b = braccio(int(argv[1]), int(argv[2]), argv[3], argv[4])
        sys.stdout.write(json.dumps(b) + "\n")
        return 0
    import _presidio
    _presidio.avvia(__file__)
    import _censimento_punti_fissi as CPF
    import _collauda_cs_centro as D2
    import _misura_mb2 as MB2
    import composizione as CM
    corto = argv[:1] == ["--corto"]
    taglie = TAGLIE[:1] if corto else TAGLIE
    irapporti = (3,) if corto else tuple(range(len(D2.SPAZZATA)))
    print("=" * 100)
    print("IL COSTO DEI PUNTI FISSI DEL TICK, MISURATO A TEMPO -- il passo `B` della memoria")
    print("=" * 100)
    print("### LA CONFIGURAZIONE INTERA")
    print("  la scena di `C5`: DV.scena(taglia, seme=%d, dtau=%.2f, norma=%s, vuoto_modulo=%.1f,"
          " su2=%s)" % (MB2.SEME, DTAU, MB2.NORMA, MB2.VUOTO_MODULO, MB2.SU2))
    print("  lo stato: la pre-corsa (TEMPO=%.1f, a forma spenta, senza CAMM-FASE-VUOTO)"
          % MB2.TEMPO)
    print("  taglie %s   tick per braccio %d   ripetizioni %d   soglia %.0f sigma"
          % (list(taglie), TICK, RIPETIZIONI, SIGMA))
    print("  Lambda_c: D2.SPAZZATA = %s (valori di C5 sulla taglia %d; sull'altra lo stesso"
          " RAPPORTO)" % (list(D2.SPAZZATA), MB2.NN))
    print("  il passo: l'ordine della tabella, impronta %s; regola_punto_medio = None"
          " (default)" % CM.IMPRONTA)
    print("  il tick acceso: tick.tick_con_cs(st, mot, par, Lambda_c, ());  spento: tick.tick")
    percorso = sorted(CPF.chiusura_import(CPF.RADICI_TICK))
    print("  i file del percorso del tick, sha1 dei BYTE:")
    for rel in percorso:
        d = io.open(os.path.join(RADICE, rel), "rb").read()
        print("     %-36s %s" % (rel, hashlib.sha1(d).hexdigest()[:8]))
    sys.stdout.flush()
    print("-" * 100)
    g, s = collaudo_del_criterio()
    print("### IL CRITERIO SU DUE CASI NOTI (P1-sexies): giusto torna %s   sbagliato torna %s"
          "   %s" % (g, s, "PASSA" if g and not s else "### FALLISCE"))
    if not (g and not s):
        print("### ⛔ IL CRITERIO E' ROTTO: niente misura.")
        return 1
    print("-" * 100)
    esito = {"inerte": True, "spento_zero": True, "torna": True, "c5_fallisce": True,
             "righe": 0}
    for taglia in taglie:
        print()
        print("### TAGLIA %d" % taglia)
        # ---------------------------------------------------------- il braccio spento
        sp = lancia(taglia, irapporti[0], "spento", "strumentato")
        sn = lancia(taglia, irapporti[0], "spento", "nudo")
        Ls = leggi(sp)
        inerte = sp["firme"] == sn["firme"] and len(sp["firme"]) == 1
        zero = (len(Ls["giri_cs"]) == 0 and float(np.max(Ls["om_iter"])) == 0.0
                and float(np.max(Ls["pm"])) == 0.0)
        esito["inerte"] &= inerte
        esito["spento_zero"] &= zero
        print("  `cs` SPENTO (riferimento): T tick %.3f ms   chiamate cs %d   applica %d"
              " (tutte con giri 0: %s, il loro tempo %.4f ms = %.2f%%)   punto medio %d"
              % (_ms(np.mean(Ls["T"])), len(Ls["giri_cs"]), Ls["n_om"],
                 all(gg == 0 for gg in Ls["giri_om"]), _ms(np.mean(Ls["om_tutte"])),
                 100 * np.mean(Ls["om_tutte"]) / np.mean(Ls["T"]), Ls["n_pm"]))
        print("     quota dei tre nelle chiamate che ITERANO: %s   involucro inerte: %s"
              % ("0 esatto -- PASSA" if zero else "### NON ZERO -- FALLISCE",
                 "PASSA" if inerte else "### FALLISCE (%s / %s)" % (sp["firme"],
                                                                    sn["firme"])))
        print("  %-8s %-6s %-9s %-15s %-17s %-17s %-11s %s"
              % ("Lc", "Lc/Lm", "T tick", "cs: giri m/max", "cs: quota", "Omega: giri m/max",
                 "Omega: quota", "dentro cs / fuori"))
        sys.stdout.flush()
        controlli = []
        for ir in irapporti:
            b = lancia(taglia, ir, "acceso", "strumentato")
            bn = lancia(taglia, ir, "acceso", "nudo")
            if "non_converge" in b or "non_converge" in bn:
                print("  %-8.2f ### NON CONVERGE: %s"
                      % (b["lambda_c"], (b.get("non_converge") or bn["non_converge"])[:90]))
                sys.stdout.flush()
                continue
            inerte = b["firme"] == bn["firme"] and len(b["firme"]) == 1
            esito["inerte"] &= inerte
            L = leggi(b)
            Tm = np.mean(L["T"])
            gom = [x for x in L["giri_om"] if x > 0]
            print("  %-8.2f %-6.3f %-9.3f %-15s %-17s %-17s %-11s %s%s"
                  % (b["lambda_c"], b["rapporto"], _ms(Tm),
                     "%.2f/%d" % (np.mean(L["giri_cs"]), max(L["giri_cs"])),
                     "%.1f%%" % (100 * np.mean(L["cs"]) / Tm),
                     "%.2f/%d" % (np.mean(gom), max(gom)),
                     "%.1f%%" % (100 * np.mean(L["om_iter"]) / Tm),
                     "%.1f%% / %.1f%%" % (100 * np.mean(L["om_in"]) / Tm,
                                          100 * np.mean(L["om_fu"]) / Tm),
                     "" if inerte else "   ### INVOLUCRO NON INERTE"))
            sys.stdout.flush()
            controlli.append((b, L))
            esito["righe"] += 1
        print("  ### il punto medio per pezzo: chiamate %s -> SPENTO in questa configurazione"
              % sorted(set(len(L["giri_pm"]) for _b, L in controlli)))
        print("  ### IL CONTROLLO: il tempo misurato contro giri * c(giro)  [ms, 3 sigma]")
        print("  ### r = misura/previsto: la soglia dice se TORNA, r dice DI QUANTO")
        print("  %-8s %-34s %-34s %s" % ("Lc", "cs_al_centro  misura/previsto/soglia",
                                         "Omega  misura/previsto/soglia",
                                         "C5 (DEVE fallire)"))
        for b, L in controlli:
            ok_cs, d_cs, s_cs = torna(L["cs"], L["prev_cs"])
            ok_om, d_om, s_om = torna(L["om_iter"], L["prev_om"])
            ok_c5, d_c5, s_c5 = torna(L["om_iter"], L["prev_c5"])
            esito["torna"] &= ok_cs and ok_om
            esito["c5_fallisce"] &= not ok_c5
            print("  %-8.2f %-34s %-34s %s"
                  % (b["lambda_c"],
                     "%.1f/%.1f/%.1f r=%.3f %s"
                     % (_ms(np.mean(L["cs"])), _ms(L["prev_cs"][0]), _ms(s_cs),
                        np.mean(L["cs"]) / L["prev_cs"][0],
                        "torna" if ok_cs else "### NO"),
                     "%.1f/%.1f/%.1f r=%.3f %s"
                     % (_ms(np.mean(L["om_iter"])), _ms(L["prev_om"][0]), _ms(s_om),
                        np.mean(L["om_iter"]) / L["prev_om"][0],
                        "torna" if ok_om else "### NO"),
                     "%.3f previsto: %s" % (_ms(L["prev_c5"][0]),
                                            "fallisce" if not ok_c5 else
                                            "### TORNA")))
            sys.stdout.flush()
    print()
    print("=" * 100)
    print("### I VERDETTI")
    for k, che in (("inerte", "l'involucro e' inerte (sha1 dello stato finale, ogni braccio)"),
                   ("spento_zero", "cs SPENTO: quota 0 esatto per i tre (chiamate che iterano)"),
                   ("c5_fallisce", "il caso che DEVE fallire (il conto di C5) fallisce"),
                   ("torna", "il tempo misurato torna con giri * c(giro), cs e Omega")):
        print("  %-66s %s" % (che, "PASSA" if esito[k] else "### FALLISCE"))
    print("  righe misurate: %d" % esito["righe"])
    if not esito["torna"]:
        print("### ⛔ C'E' UN COSTO NON CAPITO: il par.2 del task history dice di FERMARSI.")
    print("=" * 100)
    return 0 if all(esito[k] for k in ("inerte", "spento_zero", "c5_fallisce", "torna")) \
        else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
