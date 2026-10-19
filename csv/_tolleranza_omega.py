# -*- coding: utf-8 -*-
r"""**LE PROVE DEL TETTO DI `Omega`** — *`Q2`-`Q7` dell'annotazione del task history.*

> ### ⛔ **Il task history e' `2026-10-19_tolleranza_omega.md`**, con l'annotazione della
> strada `(b)` *(`ce37a148`)*: la scala e' ### **il TETTO dei termini di `Omega`**
> *(`energia_pesata.tetto_omega`, codice `418546c8`)*, e un controllo dentro il codice lo
> verifica. ### **`Q0` (`M-B1`) e `Q1` (`C1`) girano coi loro script.**
> ### ⚠ **La versione di `bfb80c6f` provava la scala di `7395cd9a`** *(che NON era un tetto,
> errore `n.17`)*, e si fermava a meta' perche' ### **non intercettava la non convergenza VERA
> di `cs`**: questa e' la cura chiesta da Luca.

- `Q2` ### **`C5` sui sette `Lambda_c`, NON REGRESSIONE braccio per braccio:** la scena di
  `C1`, `dtau 0.25`, `8` tick, col criterio di `fab82ed2` *(`energia_pesata` a quel blob,
  caricato da `git show`)* e con quello di adesso: ### **converge ovunque convergeva prima.**
- `Q3` ### **il braccio debole di `D4`** *(rapporto `1`, `dtau 0.5`, `x 0.01`, `20` tick)*:
  ### **converge**, e la stagnazione e' `<= 8` ulp del tetto.
- `Q4` ### **il controllo positivo**, sui `6` bracci di `D4` *(`x 0.01` e `x 1`, tre rapporti,
  `dtau 0.5`, `20` tick)*: per ogni applicazione il punto fisso si itera ### **fino a
  `GIRI_MAX_OMEGA`** *(una copia DICHIARATA del corpo del ciclo di `applica`)*, e la
  stagnazione *(mediana degli ultimi `10` scarti)* e' ### **`<= 8` ulp del tetto.**
  ### **La non convergenza VERA di `cs` si intercetta, si registra e si va avanti.**
- `Q5` ### **i due casi sintetici:** il rumore ### **converge**, un ciclo di periodo `2` di
  ampiezza `1e-6` ### **ALZA**.
- `Q6` ### **il braccio reale che deve ALZARE:** `applica` a frazione `16` *(`tau = 8`)* sul
  grumo a `x = 1`.
- `Q7` ### **il caso che deve fallire DEL CONTROLLO:** la scala di `7395cd9a` *(solo il nodo)*,
  messa APPOSTA, ### **fa ALZARE `controlla_tetto`** sulla scena di `C5` a `Lambda_c = 0.8`.

Gira con:  python csv/_tolleranza_omega.py
"""
import hashlib
import importlib.util
import io
import os
import subprocess
import sys
import tempfile

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

PRIMA = "fab82ed2"            # il criterio di PRIMA, come la decisione di Luca lo nomina
TICK_P2 = 20
FRAZIONE_Q6 = 16.0
TICK_C5 = 8                   # come C5 (_misura_strada_d.informazione_costo)
EPS = float(np.finfo(float).eps)
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-64s %s   %s" % (che[:64], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def _copia(st):
    return {k: (v.copy() if hasattr(v, "copy") else v) for k, v in st.items()}


def _vecchio():
    """### `energia_pesata` al blob di `PRIMA`, ### **come modulo a parte.**"""
    src = subprocess.check_output(["git", "show", PRIMA + ":primo_ordine/energia_pesata.py"],
                                  cwd=RADICE)
    d = tempfile.mkdtemp()
    p = os.path.join(d, "energia_pesata_prima.py")
    io.open(p, "wb").write(src)
    spec = importlib.util.spec_from_file_location("energia_pesata_prima", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m, hashlib.sha1(src).hexdigest()[:8]


# =====================================================================================
#   LA DIAGNOSI DI UNA APPLICAZIONE: la copia DICHIARATA del corpo del ciclo
# =====================================================================================
def diagnosi(mot, st, par, frazione):
    """### Lo scarto a ogni giro, ### **fino a `GIRI_MAX_OMEGA`, senza fermarsi.**"""
    import energia_pesata as EP
    tetto = float(np.max(EP.tetto_omega(mot, _copia(st), par)))
    s = _copia(st)
    tau = float(mot.dtau[0]) * float(frazione)
    phi = s["phi_h"]
    salvo = phi.copy()
    prec = EP.omega(mot, s, par).copy()
    seq = []
    for _g in range(EP.GIRI_MAX_OMEGA):
        np.multiply(salvo, np.exp(-1j * (prec * (tau * 0.5))[mot.inc.nodo]), out=phi)
        nuovo = EP.omega(mot, s, par)
        seq.append(float(np.max(np.abs(nuovo - prec))))
        prec = nuovo.copy()
    return {"seq": seq, "stagnazione": float(np.median(seq[-10:])),
            "max_omega": float(np.max(np.abs(prec))), "tetto": tetto}


def braccio_d4(rapporto, x):
    """### `(diagnosi, chi_alza)` delle applicazioni nei primi `TICK_P2` tick di un braccio."""
    import _misura_d4 as D4
    import energia_pesata as EP
    import statica_protocollo as PR
    PR.SOSTITUISCI = False
    lc = rapporto * D4.lambda_medio(PR.DTAU[0])
    vero = EP.applica
    diag = []

    def applica(mot, st, par, frazione):
        if mot.cs is not None and mot.lambda_c is not None:
            diag.append(diagnosi(mot, st, par, frazione))
        return vero(mot, st, par, frazione)
    EP.applica = applica
    alza = None
    try:
        PR.corri(PR.DTAU[0], x, "S3", TICK_P2, PR.T_ACCENSIONE[1], (0,), congela="pezzo",
                 lambda_c=lc)
    except AssertionError as e:
        # ### ⛔ **LA NON CONVERGENZA VERA DI `cs` SI INTERCETTA E SI REGISTRA**: le
        # ### applicazioni fatte fin li' restano. ### **Un `Omega` o un tetto che alzano,
        # ### invece, NON si nascondono:** il chiamante li conta come fallimento.
        alza = str(e)[:100]
    finally:
        EP.applica = vero
    return diag, alza


def q3_q4():
    import energia_pesata as EP
    print("### Q3 + Q4: la STAGNAZIONE dello scarto, in ulp del TETTO e di max|Omega|")
    print("  (i primi %d tick di 6 bracci di D4, dtau 0.5)" % TICK_P2)
    print("  %-8s %-6s %-6s %-12s %-14s %-14s %s"
          % ("rapporto", "x", "app.", "stagn. max", "ulp TETTO max", "ulp |Omega| max",
             "alzerebbero con |Omega|"))
    peggio, quanti, falsi, altri = 0.0, 0, 0, []
    q3 = None
    for r in (0.1, 1.0, 10.0):
        for x in (0.01, 1.0):
            dd, alza = braccio_d4(r, x)
            if alza is not None:
                vera = "punto fisso di `cs`" in alza
                if not vera:
                    altri.append((r, x, alza))
                print("  %-8g %-6g ### il braccio si ferma dopo %d applicazioni: %s"
                      % (r, x, len(dd), "la NON convergenza VERA di cs, registrata"
                         if vera else "### " + alza))
            if not dd:
                continue
            ut = [d["stagnazione"] / (EPS * d["tetto"]) for d in dd]
            uo = [d["stagnazione"] / (EPS * d["max_omega"]) if d["max_omega"] > 0
                  else float("inf") for d in dd]
            f = sum(1 for d in dd
                    if not any(q <= EP.EPS_OMEGA * d["max_omega"] for q in d["seq"]))
            falsi += f
            quanti += len(dd)
            peggio = max([peggio] + ut)
            print("  %-8g %-6g %-6d %-12.3e %-14.2f %-14.2f %d su %d"
                  % (r, x, len(dd), max(d["stagnazione"] for d in dd), max(ut), max(uo),
                     f, len(dd)))
            sys.stdout.flush()
            if r == 1.0 and x == 0.01:
                q3 = (dd, alza)
    print("-" * 100)
    dd, alza = q3
    u3 = [d["stagnazione"] / (EPS * d["tetto"]) for d in dd]
    print("### Q3: il braccio debole (rapporto 1, dtau 0.5, x 0.01): %d applicazioni; la prima:"
          % len(dd))
    print("     gli ultimi 10 scarti: %s" % "  ".join("%.2e" % q for q in dd[0]["seq"][-10:]))
    print("     max|Omega| = %.3e   il TETTO (max) = %.3e   max|Omega|/tetto = %.3f"
          % (dd[0]["max_omega"], dd[0]["tetto"], dd[0]["max_omega"] / dd[0]["tetto"]))
    esito("Q3 il braccio debole CONVERGE, stagnazione <= 8 ulp del tetto",
          alza is None and max(u3) <= 8.0,
          "il peggio %.2f ulp su %d applicazioni%s" % (max(u3), len(dd),
                                                      "" if alza is None else "; ### " + alza))
    esito("Q4 la stagnazione sta entro 8 ulp del TETTO, in tutte le applicazioni",
          peggio <= 8.0 and not altri,
          "%d applicazioni, il peggio %.2f ulp; con max|Omega| ne alzerebbero %d; altri"
          " che alzano: %d" % (quanti, peggio, falsi, len(altri)))


def q5():
    import energia_pesata as EP
    print("-" * 100)
    print("### Q5: il criterio sui due casi SINTETICI (scala 1)")

    def converge(seq):
        return any(EP.entro_tolleranza(q, 1.0) for q in seq[:EP.GIRI_MAX_OMEGA])
    rumore = [max(1e-2 * 0.1 ** k, 1.5 * EPS) for k in range(EP.GIRI_MAX_OMEGA)]
    ciclo = [2e-6] * EP.GIRI_MAX_OMEGA
    esito("Q5 (i) uno scarto che si ferma al rumore (1.5 ulp) CONVERGE", converge(rumore), "")
    esito("Q5 (ii) un ciclo di periodo 2 di ampiezza 1e-6 ALZA", not converge(ciclo),
          "lo scarto resta 2e-6 a ogni giro")


def q6():
    import energia_pesata as EP
    import flussi_parziali as FP
    import scena_l2 as SC
    import statica_protocollo as PR
    print("-" * 100)
    print("### Q6: il braccio REALE che deve ALZARE: applica a frazione %g (tau = %g)"
          % (FRAZIONE_Q6, PR.DTAU[0] * FRAZIONE_Q6))
    inc, mot, st, par, _c, _per = SC.scena(PR.DTAU[0], PR.VUOTO, 0.0, PR.RAGGIO, False, True,
                                           False, PR.SEME, 1, lati=PR.LATI)
    PR.metti_grumi(st, inc, PR.LATI, (0,), PR.RAGGIO, PR.VUOTO)
    FP.accendi_cs(mot, float(np.mean(mot.densita_vuoto(st))), st)
    try:
        EP.applica(mot, st, par, FRAZIONE_Q6)
        alza, nota = False, "### ha CONVERGIUTO in %d giri" % mot.giri_omega
    except AssertionError as e:
        alza, nota = "NON CONVERGE" in str(e), str(e)[:90]
    esito("Q6 una NON convergenza vera continua ad ALZARE", alza, nota)


def _scena_c5(lc):
    import _misura_hw as HW
    import _misura_mb2 as MB2
    import deriva as DV
    import flussi_parziali as FP
    _inc, mot, st, par = DV.scena(MB2.NN, MB2.SEME, 0.25, norma=MB2.NORMA,
                                  vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
    st["psi_h"][...], st["phi_h"][...] = HW.stato_non_uniforme()
    FP.accendi_cs(mot, lc, st)
    return mot, st, par


def _corsa_c5(lc, applica):
    """### `None` se gli `8` tick convergono, se no il messaggio di chi ha alzato."""
    import energia_pesata as EP
    import tick as TK
    mot, st, par = _scena_c5(lc)
    vero = EP.applica
    EP.applica = applica
    try:
        for _t in range(TICK_C5):
            TK.tick_con_cs(st, mot, par, lc, ())
        return None
    except AssertionError as e:
        return str(e)[:90]
    finally:
        EP.applica = vero


def q2():
    import _collauda_cs_centro as D2
    import energia_pesata as EP
    print("-" * 100)
    vecchio, blob = _vecchio()
    print("### Q2: C5 sui sette Lambda_c, NON REGRESSIONE -- il criterio di %s (energia_pesata"
          " sha1 %s) contro quello di adesso, %d tick per braccio" % (PRIMA, blob, TICK_C5))
    regressi = []
    for lc in D2.SPAZZATA:
        a = _corsa_c5(lc, vecchio.applica)
        b = _corsa_c5(lc, EP.applica)
        if a is None and b is not None:
            regressi.append(lc)
        print("  Lambda_c %-8g  PRIMA: %-10s  ADESSO: %s"
              % (lc, "converge" if a is None else "alza", "converge" if b is None
                 else "### ALZA: " + b))
        sys.stdout.flush()
    esito("Q2 converge ovunque convergeva col criterio di PRIMA", not regressi,
          "regressioni: %s" % (regressi or "nessuna"))


def q7():
    import energia_pesata as EP
    print("-" * 100)
    print("### Q7: il caso che deve fallire DEL CONTROLLO -- la scala di 7395cd9a (solo il"
          " nodo), messa APPOSTA, sulla scena di C5 a Lambda_c 0.8")
    vero_tetto, vero_contr = EP.tetto_omega, EP.controlla_tetto
    scattato = {"si": False}

    def tetto_vecchio(mot, st, par):
        lam = EP._per_nodo(mot, np.abs(st["phi_h"]) ** 2, np.empty(mot.inc.n))
        psi = st["psi_h"]
        rho = EP._per_nodo(mot, np.abs(psi[:, 0]) ** 2 + np.abs(psi[:, 1]) ** 2,
                           np.empty(mot.inc.n))
        csp = EP.cs_primo(lam, mot.lambda_c, np.empty(mot.inc.n))
        return np.full(mot.inc.n, float(np.max(np.abs(csp) * EP.OMEGA_H * (lam + rho))))

    def controlla(om, tt, dove):
        try:
            vero_contr(om, tt, dove)
        except AssertionError:
            scattato["si"] = True
            raise
    EP.tetto_omega, EP.controlla_tetto = tetto_vecchio, controlla
    try:
        msg = _corsa_c5(0.8, EP.applica)
    finally:
        EP.tetto_omega, EP.controlla_tetto = vero_tetto, vero_contr
    esito("Q7 con la scala VECCHIA il controllo del tetto ALZA", scattato["si"],
          msg or "### nessuno ha alzato")


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import energia_pesata as EP
    print("=" * 100)
    print("LE PROVE DEL TETTO DI `Omega` -- Q2-Q7 (Q0 e Q1 coi loro script)")
    print("=" * 100)
    print("  EPS_OMEGA = 8 eps = %.3e   GIRI_MAX_OMEGA = %d   la scala: il TETTO di Omega"
          " (energia_pesata.tetto_omega)" % (EP.EPS_OMEGA, EP.GIRI_MAX_OMEGA))
    print("-" * 100)
    q2()
    q3_q4()
    q5()
    q6()
    q7()
    print("=" * 100)
    print("LE PROVE: %d su %d" % (OK[0], OK[1]))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
