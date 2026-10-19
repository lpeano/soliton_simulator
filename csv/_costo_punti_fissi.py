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
### ⛔⛔ **IL CRITERIO E' QUELLO DI `652eeb52`** *(decisione di Luca del `2026-10-19`,
scritta nel task history PRIMA di questa versione)*, che sostituisce quello di
`a43eb14a` *(caduto in due versi, `ec0d5f7f`)*:
### ✅ **statistica ROBUSTA:** `1 + 5` ripetizioni, ### **la prima di riscaldamento
SCARTATA**; la ### **MEDIANA** delle `5`, la dispersione ### **`1.4826 * MAD`**, e
`|T - T_previsto| <= 3 sqrt(s_T^2 + s_prev^2)` *(`s_prev` del costo di un giro, per i
giri, diviso la radice dei campioni -- come prima)*.
### ⛔ **UN BRACCIO E' INFORMATIVO solo se la soglia e' MINORE della distanza** fra il
previsto giusto e ### **il previsto del caso che deve fallire** *(il conto di `C5`)*; se
no e' ### **NON INFORMATIVO**, si conta a parte e ### **non vale MAI come <<torna>>.**
### **IL VERDETTO**, per punto fisso e per taglia: ### **TORNA** se tutti gli informativi
tornano e in tutti il conto di `C5` fallisce; ### **NON DECIDIBILE** se nessun braccio e'
informativo *(e non vale come PASSA)*.
### ⛔ **IL CASO CHE DEVE FALLIRE, il conto di `C5`** *(`_misura_strada_d.informazione_
costo`)*: per ### **`Omega`** i giri letti da `mot.giri_omega` ### **una volta per tick**
*(l'ultima applicazione)*; per ### **`cs`** ### **<<un giro costa MEZZO TICK>>**, cioe'
mezzo tick ### **SPENTO** della stessa taglia per giro *(ignora il punto fisso di `Omega`
dentro ogni mezzo palindromo)*.
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
RISCALDAMENTO = 1            # 652eeb52: la prima ripetizione e' di riscaldamento, SCARTATA
SIGMA = 3.0                  # la soglia: 3 volte la dispersione (652eeb52)
MAD_SCALA = 1.4826           # 652eeb52: la MAD scalata alla sigma di una normale


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
        fuori["giro_cs"] = [costo_giro_cs(st0, mot, par, lc)
                            for _ in range(RISCALDAMENTO + TICK)]
        FP.accendi_cs(mot, lc, st0)
        fuori["giro_om"] = [costo_giro_om(st0, mot, par)
                            for _ in range(RISCALDAMENTO + TICK)]
        FP.spegni_cs(mot)
    ripetizioni = []
    firme = set()
    try:
        if inv is not None:
            inv.installa()
        for _r in range(RISCALDAMENTO + RIPETIZIONI if inv is not None else 1):
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
#   LA LETTURA -- il criterio ROBUSTO di `652eeb52` (decisione di Luca, 2026-10-19)
# =====================================================================================
#   ### ⛔⛔ **IL CRITERIO E' SCRITTO NEL TASK HISTORY PRIMA DI QUESTA CORSA** *(par.`2`,
#   ### annotazione del `2026-10-19`)*, e qui ### **si applica, non si sceglie**:
#   ### la MEDIANA delle ripetizioni dopo il RISCALDAMENTO, la dispersione `1.4826 MAD`,
#   ### la soglia `3` volte quella dispersione combinata fra misura e previsto, e un
#   ### braccio ### **INFORMATIVO solo se la soglia e' minore della distanza fra il
#   ### previsto giusto e quello del caso che deve fallire.**
# =====================================================================================
def _ms(x):
    return 1e3 * x


def mediana_e_s(v):
    """### `(mediana, 1.4826 * MAD)`: ### **la statistica robusta del criterio.**"""
    v = np.asarray(v, dtype=float)
    m = float(np.median(v))
    return m, MAD_SCALA * float(np.median(np.abs(v - m)))


def leggi(b, t_spento):
    """### Le quote, i giri, e i TRE previsti ### **per il controllo.**

    `t_spento` e' `(mediana, s)` del tick SPENTO della stessa taglia, ### **per tick**:
    serve al conto di `C5` per `cs`.
    """
    rr = b["ripetizioni"][RISCALDAMENTO:]
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
        gcs = np.array(b["giro_cs"][RISCALDAMENTO:])
        gom = np.array(b["giro_om"][RISCALDAMENTO:])
        n_cs = float(sum(giri_cs))
        n_om = float(sum(g + 1 for g in giri_om if g > 0))
        # ### ⛔ **IL CASO CHE DEVE FALLIRE PER `Omega`, il conto di `C5`:** i giri
        # ### letti ### **una volta per tick** dall'ultima applicazione, coi confini dei
        # ### tick registrati *(le applicazioni per tick non sono uguali)*.
        ultima = [giri_om[f - 1] for f in rr[0]["fine_tick"]]
        n_c5 = float(sum(g + 1 for g in ultima if g > 0))

        # ### ⚠ **l'incertezza del previsto e' quella del costo di UN giro, per il
        # ### numero di giri, divisa per la radice dei campioni** -- ### **come prima**
        # ### *(<<combinata come oggi>>)*, con la statistica robusta al posto di quella
        # ### normale.
        def prev(n, c):
            m, s = mediana_e_s(c)
            return n * m, n * s / float(np.sqrt(len(c)))
        L["prev_cs"] = prev(n_cs, gcs)
        L["prev_om"] = prev(n_om, gom)
        L["prev_c5_om"] = prev(n_c5, gom)
        # ### ⛔ **IL CASO CHE DEVE FALLIRE PER `cs`, il conto di `C5`:**
        # ### `_misura_strada_d.informazione_costo` scrive ### **<<UN GIRO DI `cs` COSTA
        # ### MEZZO TICK>>** *(`lavoro = g_cs * 0.5 + ...`)*, cioe' ### **mezzo tick
        # ### SENZA punti fissi per giro** -- e ignora che ogni mezzo palindromo contiene
        # ### il punto fisso di `Omega`. ### **Il tick senza punti fissi e' quello SPENTO
        # ### della stessa taglia, misurato.**
        L["prev_c5_cs"] = (n_cs * 0.5 * t_spento[0], n_cs * 0.5 * t_spento[1])
    return L


def giudica(misura, previsto, previsto_c5):
    """### Il giudizio di UN braccio, ### **col criterio di `652eeb52`.**

    ### `misura`: le ripetizioni *(gia' senza il riscaldamento)*; `previsto` e
    `previsto_c5`: `(valore, s)`. ### Torna un dizionario: `r`, `soglia`, `distanza`,
    ### **`informativo`**, `torna` *(solo se informativo)*, `c5_fallisce`.
    """
    m, sm = mediana_e_s(misura)
    p, sp = previsto
    c, sc = previsto_c5
    soglia = SIGMA * float(np.sqrt(sm * sm + sp * sp))
    soglia_c5 = SIGMA * float(np.sqrt(sm * sm + sc * sc))
    distanza = abs(p - c)
    informativo = soglia < distanza
    return {"misura": m, "previsto": p, "previsto_c5": c, "r": m / p if p else float("nan"),
            "soglia": soglia, "distanza": distanza, "informativo": informativo,
            "torna": informativo and abs(m - p) <= soglia,
            "c5_fallisce": abs(m - c) > soglia_c5}


def collaudo_del_criterio():
    """### `P1-sexies`: ### **il criterio su TRE casi a risposta NOTA**, prima del vero.

    ### ✅ **giusto:** misura attorno al previsto, previsto di `C5` lontano -> informativo,
    torna. ### ⛔ **sbagliato:** misura lontana dal previsto -> informativo, NON torna.
    ### ⚠ **non informativo:** la stessa misura giusta ma con ### **una soglia larga
    apposta** *(dispersione piu' grande della distanza fra i due previsti)* -> etichettato
    ### **NON INFORMATIVO**, e ### **mai** <<torna>>.
    """
    r = np.random.default_rng(0)
    rumore = r.standard_normal(RIPETIZIONI)
    giusto = giudica(1.0 + 0.01 * rumore, (1.0, 0.01), (0.5, 0.005))
    sbagliato = giudica(1.5 + 0.01 * rumore, (1.0, 0.01), (0.5, 0.005))
    largo = giudica(1.0 + 0.01 * rumore, (1.0, 0.5), (0.5, 0.005))
    ok = (giusto["informativo"] and giusto["torna"]
          and sbagliato["informativo"] and not sbagliato["torna"]
          and not largo["informativo"] and not largo["torna"])
    return ok, giusto, sbagliato, largo


def _etichetta(g):
    if not g["informativo"]:
        return "NON INFORMATIVO"
    return "torna" if g["torna"] else "### NON TORNA"


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
    print("  taglie %s   tick per braccio %d   ripetizioni %d + %d di riscaldamento SCARTATA"
          % (list(taglie), TICK, RIPETIZIONI, RISCALDAMENTO))
    print("  il criterio (652eeb52): MEDIANA, dispersione %.4f*MAD, soglia %.0f volte;"
          " INFORMATIVO se soglia < |previsto - previsto di C5|" % (MAD_SCALA, SIGMA))
    print("  Lambda_c: D2.SPAZZATA = %s (valori di C5 sulla taglia %d; sull'altra lo stesso"
          " RAPPORTO)" % (list(D2.SPAZZATA), MB2.NN))
    print("  il passo: l'ordine della tabella, impronta %s; regola_punto_medio = None"
          " (default)" % CM.IMPRONTA)
    print("  il tick acceso: tick.tick_con_cs(st, mot, par, Lambda_c, ());  spento: tick.tick")
    print("  il caso che DEVE fallire (il conto di C5): per `cs` mezzo tick SPENTO per giro;"
          " per `Omega` i giri dell'ULTIMA applicazione per tick")
    percorso = sorted(CPF.chiusura_import(CPF.RADICI_TICK))
    print("  i file del percorso del tick, sha1 dei BYTE:")
    for rel in percorso:
        d = io.open(os.path.join(RADICE, rel), "rb").read()
        print("     %-36s %s" % (rel, hashlib.sha1(d).hexdigest()[:8]))
    sys.stdout.flush()
    print("-" * 100)
    ok, g1, g2, g3 = collaudo_del_criterio()
    print("### IL CRITERIO SU TRE CASI NOTI (P1-sexies)")
    for che, g in (("giusto (deve tornare)", g1), ("sbagliato (NON deve tornare)", g2),
                   ("soglia larga (deve essere NON INFORMATIVO)", g3)):
        print("     %-44s r=%.3f soglia=%.4f distanza=%.4f  %s"
              % (che, g["r"], g["soglia"], g["distanza"], _etichetta(g)))
    print("     %s" % ("PASSA" if ok else "### FALLISCE"))
    if not ok:
        print("### ⛔ IL CRITERIO E' ROTTO: niente misura.")
        return 1
    print("-" * 100)
    esito = {"inerte": True, "spento_zero": True, "righe": 0, "verdetti": []}
    for taglia in taglie:
        print()
        print("### TAGLIA %d" % taglia)
        # ---------------------------------------------------------- il braccio spento
        sp = lancia(taglia, irapporti[0], "spento", "strumentato")
        sn = lancia(taglia, irapporti[0], "spento", "nudo")
        Ls = leggi(sp, None)
        t_sp = mediana_e_s(Ls["T"] / TICK)
        inerte = sp["firme"] == sn["firme"] and len(sp["firme"]) == 1
        zero = (len(Ls["giri_cs"]) == 0 and float(np.max(Ls["om_iter"])) == 0.0
                and float(np.max(Ls["pm"])) == 0.0)
        esito["inerte"] &= inerte
        esito["spento_zero"] &= zero
        print("  `cs` SPENTO (riferimento): T tick %.3f ms (mediana; %.4f ms per tick)"
              "   chiamate cs %d   applica %d (tutte con giri 0: %s, il loro tempo %.4f ms"
              " = %.2f%%)   punto medio %d"
              % (_ms(np.median(Ls["T"])), _ms(t_sp[0]), len(Ls["giri_cs"]), Ls["n_om"],
                 all(gg == 0 for gg in Ls["giri_om"]), _ms(np.median(Ls["om_tutte"])),
                 100 * np.median(Ls["om_tutte"]) / np.median(Ls["T"]), Ls["n_pm"]))
        print("     quota dei tre nelle chiamate che ITERANO: %s   involucro inerte: %s"
              % ("0 esatto -- PASSA" if zero else "### NON ZERO -- FALLISCE",
                 "PASSA" if inerte else "### FALLISCE (%s / %s)" % (sp["firme"],
                                                                    sn["firme"])))
        print("  ### le quote sono MEDIANE delle ripetizioni")
        print("  %-8s %-7s %-9s %-15s %-10s %-17s %-12s %s"
              % ("Lc", "Lc/Lm", "T tick", "cs: giri m/max", "cs: quota", "Omega: giri m/max",
                 "Omega: quota", "dentro cs / fuori"))
        sys.stdout.flush()
        controlli = []
        for ir in irapporti:
            b = lancia(taglia, ir, "acceso", "strumentato")
            bn = lancia(taglia, ir, "acceso", "nudo")
            if "non_converge" in b or "non_converge" in bn:
                print("  %-8.2f %-7.3f ### NON CONVERGE: %s"
                      % (b["lambda_c"], b["rapporto"],
                         (b.get("non_converge") or bn["non_converge"])[:90]))
                sys.stdout.flush()
                continue
            inerte = b["firme"] == bn["firme"] and len(b["firme"]) == 1
            esito["inerte"] &= inerte
            L = leggi(b, t_sp)
            Tm = float(np.median(L["T"]))
            gom = [x for x in L["giri_om"] if x > 0]
            print("  %-8.2f %-7.3f %-9.3f %-15s %-10s %-17s %-12s %s%s"
                  % (b["lambda_c"], b["rapporto"], _ms(Tm),
                     "%.2f/%d" % (np.mean(L["giri_cs"]), max(L["giri_cs"])),
                     "%.1f%%" % (100 * np.median(L["cs"]) / Tm),
                     "%.2f/%d" % (np.mean(gom), max(gom)),
                     "%.1f%%" % (100 * np.median(L["om_iter"]) / Tm),
                     "%.1f%% / %.1f%%" % (100 * np.median(L["om_in"]) / Tm,
                                          100 * np.median(L["om_fu"]) / Tm),
                     "" if inerte else "   ### INVOLUCRO NON INERTE"))
            sys.stdout.flush()
            controlli.append((b, L))
            esito["righe"] += 1
        print("  ### il punto medio per pezzo: chiamate %s -> SPENTO in questa configurazione"
              % sorted(set(len(L["giri_pm"]) for _b, L in controlli)))
        print("  ### IL CONTROLLO (criterio di 652eeb52): misura contro giri * c(giro)  [ms]")
        print("  ### r = misura/previsto; soglia = 3*1.4826*MAD combinata; distanza ="
              " |previsto - previsto di C5|")
        print("  %-8s %-6s %-48s %s" % ("Lc", "", "r / soglia / distanza  etichetta",
                                       "il conto di C5 (DEVE fallire)"))
        for chi, k_mis, k_prev, k_c5 in (("cs", "cs", "prev_cs", "prev_c5_cs"),
                                         ("Omega", "om_iter", "prev_om", "prev_c5_om")):
            informativi, tornano, c5_ok = 0, 0, 0
            for b, L in controlli:
                g = giudica(L[k_mis], L[k_prev], L[k_c5])
                if g["informativo"]:
                    informativi += 1
                    tornano += 1 if g["torna"] else 0
                    c5_ok += 1 if g["c5_fallisce"] else 0
                print("  %-8.2f %-6s %-48s %s"
                      % (b["lambda_c"], chi,
                         "r=%.3f  %.1f / %.1f  %s" % (g["r"], _ms(g["soglia"]),
                                                     _ms(g["distanza"]), _etichetta(g)),
                         "previsto %.1f ms: %s" % (_ms(g["previsto_c5"]),
                                                   "fallisce" if g["c5_fallisce"]
                                                   else "### TORNA")))
            if informativi == 0:
                v = "NON DECIDIBILE"
            elif tornano == informativi and c5_ok == informativi:
                v = "TORNA"
            else:
                v = "### NON TORNA"
            esito["verdetti"].append((taglia, chi, v, informativi, len(controlli),
                                      tornano, c5_ok))
            print("  ### taglia %d, %s: %d bracci informativi su %d, di cui %d tornano e in %d"
                  " il conto di C5 fallisce -> %s"
                  % (taglia, chi, informativi, len(controlli), tornano, c5_ok, v))
            sys.stdout.flush()
    print()
    print("=" * 100)
    print("### I VERDETTI")
    for k, che in (("inerte", "l'involucro e' inerte (sha1 dello stato finale, ogni braccio)"),
                   ("spento_zero", "cs SPENTO: quota 0 esatto per i tre (chiamate che iterano)")):
        print("  %-66s %s" % (che, "PASSA" if esito[k] else "### FALLISCE"))
    for taglia, chi, v, inf, tot, tor, c5 in esito["verdetti"]:
        print("  %-66s %s" % ("il controllo, taglia %d, %s (%d informativi su %d)"
                              % (taglia, chi, inf, tot), v))
    print("  righe misurate: %d" % esito["righe"])
    tutti = [v for (_t, _c, v, _i, _n, _r, _5) in esito["verdetti"]]
    if any(v.startswith("###") for v in tutti):
        print("### ⛔ C'E' UN COSTO NON CAPITO: il par.2 del task history dice di FERMARSI.")
    if any(v == "NON DECIDIBILE" for v in tutti):
        print("### ⚠ C'E' UN VERDETTO NON DECIDIBILE: non vale come PASSA.")
    print("=" * 100)
    ok = (esito["inerte"] and esito["spento_zero"] and all(v == "TORNA" for v in tutti))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
