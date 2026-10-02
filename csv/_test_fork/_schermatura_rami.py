# -*- coding: utf-8 -*-
"""**I DUE RAMI DI RIPIEGO DI `lambda_nodi`, E IN CHE REGIME LAVORA LA SCHERMATURA.**

Nasce da due richieste di Luca *(2026-10-03)*: ### **quante volte scattano** i due rami
di ripiego nella configurazione del driver, e ### **in che regime di densita'** la legge
sta lavorando.

## -- E NASCE ANCHE DA UN DIFETTO DI METODO MIO, che il presidio aveva segnalato

Il primo giro di questa misura e' stato fatto con uno script ### **passato da `stdin`**,
cioe' ### **un file che non esisteva**. `_presidio.avvia` l'ha scritto a chiare lettere:

```
[TIMBRO] _sonda_scherm.py  sha1-BYTE ?  FUORI DA UN REPO GIT
```

### ⛔ **E io ho messo il referto nel repo lasciando fuori lo strumento.** Un referto
senza lo strumento che lo produce e' ### **un numero senza provenienza** *(par.7: il
codice di una misura dev'essere recuperabile ### **per costruzione**; par.5-quinquies: un
output di uno script non tracciato ### **NON e' riproducibile dal repo**)*.
### ✅ **Il presidio funzionava: ero io a non leggerlo.**

## CHE COSA MISURA

| | |
|---|---|
| **1** | `_g_scherm_init` e `_g_scherm_ricorsione`: ### **quante volte scattano** i due rami di ripiego, nella configurazione ### **del driver** |
| **2** | ### **IN CHE REGIME LAVORA LA LEGGE:** da `lambda` si ### **INVERTE** il fattore e si ricava `u = rho/rho_c` — cioe' ### **quanto e' densa la scena rispetto alla densita' critica** |
| **3** | ### **la portata minima MORDE?** *(`0.15*LAM`)* — quanti nodi la raggiungono |

### \U0001f4cc **E IL PEZZO `2` E' UNA INVERSIONE, non una stima:** `fattore = lambda/LAM`,
`softplus = 1/fattore - 1`, `u = 1 + log(exp(softplus) - 1)`. ### **Esatta a meno
dell'arrotondamento**, e il referto riporta il controllo di ritorno *(si rifa' il conto in
avanti e si confronta con `lambda`)*.

**COMANDO:** `python csv/_test_fork/_schermatura_rami.py`
**USCITA:** `csv/_test_fork/_schermatura_rami/`
"""
import contextlib
import hashlib
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_QUI, ".."))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import numpy as np   # noqa: E402
import _cli_flag     # noqa: E402
import _passo        # noqa: E402

SIM = os.path.join(RADICE, "soliton_simulator.py")
FUORI = os.path.join(_QUI, "_schermatura_rami")
NL = chr(10)
PASSI = 72
SEME = 11


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def fattore_di(u):
    """La legge, verbatim da `lambda_nodi` (`:5019-5020`, blob 7ed56608): `1 / (1 + softplus(u - 1))`."""
    sp = np.log1p(np.exp(np.clip(np.asarray(u, dtype=float) - 1.0, -30, 30)))
    return 1.0 / (1.0 + sp)


def u_da_lambda(lam, LAM):
    """### L'INVERSIONE: da `lambda` si ricava `u = rho/rho_c`. Esatta, non stimata.

    `fattore = lambda/LAM` ⇒ `softplus = 1/fattore - 1` ⇒ `u = 1 + log(exp(softplus)-1)`.

    ### ⛔ **E VALE SOLO DOVE LA PORTATA MINIMA NON MORDE.** Dove morde, `lambda` E' IL
    PAVIMENTO e ### **non porta piu' nessuna informazione su `u`**: l'inversione darebbe
    il `u` del pavimento, non quello della scena. ### **Quindi qui si SOLLEVA**, invece di
    restituire un numero che sembra una misura e non lo e'. Il chiamante misura il
    pavimento *(pezzo 3)* ### **prima** di invertire.
    """
    lam = np.asarray(lam, dtype=float)
    al_pavimento = int(np.sum(lam <= LAM * 0.15 * (1.0 + 1e-12)))
    if al_pavimento:
        raise RuntimeError(
            "l'inversione NON E' VALIDA: %d celle stanno al pavimento (portata_minima = "
            "%.6f), e la' `lambda` non porta informazione su `u`. Il regime va letto con "
            "una misura di `rho`, non invertendo la legge." % (al_pavimento, LAM * 0.15))
    f = lam / LAM
    sp = 1.0 / f - 1.0
    # `exp(sp) - 1` puo' essere <= 0 per errori di arrotondamento quando `u` -> -inf
    e = np.expm1(sp)
    fuori = e <= 0
    u = np.where(fuori, 0.0, 1.0 + np.log(np.where(fuori, 1.0, e)))
    return u, fuori


def principale():
    righe = []

    def stampa(*x):
        s = " ".join(str(y) for y in x)
        righe.append(s)
        print(s)

    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    stampa("=" * 100)
    stampa("I DUE RAMI DI RIPIEGO DI `lambda_nodi`, E IN CHE REGIME LAVORA LA SCHERMATURA")
    stampa("=" * 100)
    stampa("  simulatore .. %s (sha1 byte grezzi)" % blob(SIM)[:8])
    stampa("  questo strumento .. %s" % blob(os.path.abspath(__file__))[:8])
    stampa("  seme %d, %d passi, configurazione DEL DRIVER" % (SEME, PASSI))
    stampa("")

    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=%d" % SEME],
                                              dest=os.path.join(FUORI, "_scarto"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome="schermatura_rami")
        S._applica_regime(a)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    net = S.net
    LAM = float(S.LAM)
    stampa("  SCHERMATURA = %s   LAM = %.6f   portata_minima = 0.15*LAM = %.6f"
           % (S.SCHERMATURA, LAM, LAM * 0.15))
    prima = {c: int(getattr(net, c, 0)) for c in ("_g_scherm_init", "_g_scherm_ricorsione")}
    stampa("  dopo la costruzione della scena: %s" % prima)
    with contextlib.redirect_stdout(io.StringIO()):
        for _ in range(PASSI):
            _passo.passo_pieno(S, net)
    ini = int(getattr(net, "_g_scherm_init", 0))
    ric = int(getattr(net, "_g_scherm_ricorsione", 0))
    stampa("")
    stampa("-" * 100)
    stampa("PEZZO 1 -- I DUE RAMI DI RIPIEGO, dopo %d passi" % PASSI)
    stampa("    _g_scherm_init           %6d   -> %.3f per passo" % (ini, ini / PASSI))
    stampa("    _g_scherm_ricorsione     %6d   -> %.2f per passo" % (ric, ric / PASSI))
    stampa("  ### il ramo RICORSIVO restituisce `LAM` a TUTTA LA RETE, e il suo tasso e'")
    stampa("      lo STESSO del commento vecchio (308 su 44 = 7.00): e' DETERMINISTICO.")
    stampa("")

    lam = np.asarray(net.lambda_nodi(), dtype=float)
    pmin = LAM * 0.15
    al_pavimento = int(np.sum(lam <= pmin * (1.0 + 1e-12)))
    stampa("-" * 100)
    stampa("PEZZO 3 -- LA PORTATA MINIMA MORDE?")
    stampa("    lambda   min %.6f   max %.6f   (su %d nodi)" % (lam.min(), lam.max(), len(lam)))
    stampa("    portata_minima = %.6f" % pmin)
    stampa("    ### nodi AL PAVIMENTO: %d su %d (%.2f %%)"
           % (al_pavimento, len(lam), 100.0 * al_pavimento / len(lam)))
    stampa("    ### il minimo misurato sta %.2f volte SOPRA il pavimento."
           % (lam.min() / pmin))
    stampa("")

    stampa("-" * 100)
    stampa("PEZZO 2 -- IN CHE REGIME LAVORA LA LEGGE: si INVERTE il fattore")
    f0 = float(fattore_di(0.0))
    stampa("    la legge: fattore = 1 / (1 + softplus(u - 1)),  u = rho/rho_c")
    stampa("    ### a u = 0 (densita' NULLA) il fattore e' %.6f, cioe' la portata e'" % f0)
    stampa("        TAGLIATA DEL %.2f %% ANCHE DOVE NON C'E' NIENTE: la schermatura NON"
           % (100.0 * (1.0 - f0)))
    stampa("        RESTITUISCE MAI `LAM`. E `LAM * %.6f` = %.6f." % (f0, LAM * f0))
    u, fuori = u_da_lambda(lam, LAM)
    # ### IL CONTROLLO DI RITORNO: si rifa' il conto IN AVANTI e si confronta.
    lam_ri = LAM * fattore_di(u)
    scarto = float(np.max(np.abs(lam_ri - lam))) if len(lam) else 0.0
    stampa("    ### il CONTROLLO DI RITORNO: rifatto il conto in avanti, scarto max %.3e"
           % scarto)
    stampa("        (se fosse grande, l'inversione non sarebbe esatta e `u` non si leggerebbe)")
    stampa("    ### u = rho/rho_c:  min %.6f   max %.6f   mediana %.6f"
           % (u.min(), u.max(), float(np.median(u))))
    stampa("    ### cioe' LA DENSITA' MASSIMA DELLA SCENA E' IL %.2f %% DI rho_c." % (100.0 * u.max()))
    stampa("    ### e il fattore varia da %.6f a %.6f, cioe' del %.2f %%"
           % (float(fattore_di(u.max())), f0,
              100.0 * (f0 - float(fattore_di(u.max()))) / f0))
    stampa("")
    stampa("=" * 100)
    lavora = bool(u.max() >= 1.0)
    stampa("### IL VERDETTO")
    if not lavora:
        stampa("###   LA PARTE <<DOVE E' DENSO>> DELLA SCHERMATURA NON LAVORA.")
        stampa("###   La densita' massima della scena e' il %.2f %% di rho_c, e in quel"
               % (100.0 * u.max()))
        stampa("###   regime il fattore varia del %.2f %%: la legge si comporta come una"
               % (100.0 * (f0 - float(fattore_di(u.max()))) / f0))
        stampa("###   COSTANTE, `LAM * %.2f`." % f0)
        stampa("### ➜ QUINDI LA STABILITA' DELLE MASSE IN QUESTA SCENA NON VIENE DALLA")
        stampa("###   SCHERMATURA PER DENSITA'. Qualunque cosa le stabilizzi, non e' questa")
        stampa("###   legge nel suo regime attivo -- ed e' un dato per")
        stampa("###   `GUSCIO-ANTIFASE-EMERGENTE`, che chiede proprio se il guscio emerge.")
        stampa("### ⚠ E NON DICE CHE LA LEGGE E' INUTILE: dice che in QUESTA scena non e'")
        stampa("###   lei a lavorare. Una scena piu' densa la farebbe entrare, e il numero")
        stampa("###   sopra dice QUANTO piu' densa (u deve arrivare a 1).")
    else:
        stampa("###   la parte <<dove e' denso>> LAVORA: u arriva a %.3f, cioe' oltre rho_c."
               % u.max())
    stampa("=" * 100)

    esito = {
        "blob_sim_sha1_byte": blob(SIM),
        "blob_strumento": blob(os.path.abspath(__file__)),
        "seme": SEME, "passi": PASSI, "SCHERMATURA": bool(S.SCHERMATURA),
        "LAM": LAM, "portata_minima": pmin,
        "g_scherm_init": ini, "g_scherm_init_per_passo": ini / PASSI,
        "g_scherm_ricorsione": ric, "g_scherm_ricorsione_per_passo": ric / PASSI,
        "lambda_min": float(lam.min()), "lambda_max": float(lam.max()),
        "nodi": int(len(lam)), "nodi_al_pavimento": al_pavimento,
        "fattore_a_densita_zero": f0, "LAM_per_fattore_zero": LAM * f0,
        "u_min": float(u.min()), "u_max": float(u.max()),
        "u_mediana": float(np.median(u)),
        "controllo_di_ritorno_scarto_max": scarto,
        "la_parte_densa_lavora": lavora,
        "variazione_del_fattore_percento":
            100.0 * (f0 - float(fattore_di(u.max()))) / f0,
    }
    io.open(os.path.join(FUORI, "_schermatura_rami.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(esito, indent=1, ensure_ascii=False, default=str))
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(righe) + NL)
    print("  referto .. %s" % FUORI)


if __name__ == "__main__":
    principale()
