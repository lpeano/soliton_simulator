# -*- coding: utf-8 -*-
"""**`DIVISIONE-AUTOCONSISTENTE:M7`: LA POTENZA DEL SOLO TERMINE DEL TERMOSTATO.**

**Mandato di Luca del 2026-10-01.** Serve alla ### **decisione 4** del piano del calore: ### **il
vuoto COPRE il termostato, oppure no?**

### IL TERMINE, e dove vive
Dentro `step`, il settore di fase si aggiorna con **una** riga:
```
delta_phivel = dt_n_s * (coppia - self.xi_termo * _phivel_t) / M_PH
```
### ➜ **Il termine del termostato e' `−dt_n_s · xi · _phivel_t / M_PH`**, e il suo ### **lavoro**
sulla cinetica di fase `K = 0.5·Σ phivel²` e'
```
W_termo = Σ phivel_t · Δphivel_termo = −(xi / M_PH) · Σ (dt_n_s · phivel_t²)
```

### ⚠ **E `beta` NON STA IN QUESTA EQUAZIONE, quindi i tre termini non sono tre**
Il mandato chiede *«separata dalla coppia e dall'attrito `beta`»*. ### **Ma `beta` agisce su `vd`**,
cioe' sul **settore metrico** *(`acc = cs²·lap + src − beta·vd`)*, ### **non su `phivel`.**
### ➜ **Dentro `step` ci sono DUE settori, non tre termini:** nel settore di **fase** si separano
### **coppia** e **termostato**; `beta` vive nell'altro. ### **Si riportano entrambi, e si dice
che agiscono su grandezze DIVERSE** invece di fingere una somma unica.

### ✅ **COME SI MISURA, rispettando la regola di oggi**
### **DENTRO il passo, alla voce giusta, e senza ricostruire nulla di incerto.**

| ingrediente | da dove viene |
|---|---|
| `_phivel_t` | ### **la fotografia di `phivel` al confine di voce PRIMA di `step`** — e `step` fa `_phivel_t = self.phivel.copy()` **come prima cosa**, quindi e' lo **stesso** array |
| `xi` | ### **`net.xi_termo` al confine DOPO `step`**: `step` lo aggiorna **prima** di usarlo, quindi quello e' il valore **usato** |
| `dt_n` | `DT · r` con ### **`r = ritmo()`, la funzione DEL SIMULATORE** |
| `dt_n_s` | ### **`= dt_n` quando `TEMPO_SEGNO` e' spento**, e lo strumento ### **verifica il flag e riporta il contatore `_g_temposegno_salti`** |
| `M_PH` | letto dal modulo *(misurato `1.0` uniforme)* |

### ⛔ **E `ritmo()` SI CHIAMA SU UNA COPIA PROFONDA, perche' SCRIVE**
`ritmo()` aggiorna `_ritmo_chiamate`, `_ritmo_sicurezza`, e ### **nel suo ripiego scrive
`_psi_prec`**. ### **Chiamarla sulla rete vera cambierebbe il run.** Quindi si chiama su una
`deepcopy`, ### **e si controlla sulla copia che il ripiego NON sia scattato** — se e' scattato,
### **quel passo si dichiara NON MISURABILE** invece di riportare un numero.
*(Il prezzo e' una copia profonda per passo: dichiarato.)*

### ⚠ **E IL CONFINE SI RICAVA DALLA COMPOSIZIONE, non si cabla**
La voce *«prima di `step`»* e' `comp[comp.index('step') − 1]`: ### **se `H-ETC-2` permuta
l'ordine, lo strumento segue.** *(E' la lezione di `_finestra_aperta`.)*

### 🧾 **IL TERMINE DI SECONDO ORDINE, dichiarato e NON nascosto**
`K_dopo − K_prima = Σ phivel_t·Δ + 0.5·Σ Δ²` con `Δ = Δ_coppia + Δ_termo`. ### **Il pezzo
`0.5·ΣΔ²` NON si divide fra i due termini**, quindi si riporta ### **`resto = ΔK_step − W_termo`**
e si dichiara che contiene ### **la coppia PIU' il secondo ordine.** ### **Non lo chiamo «la
coppia».**

COMANDO:  python csv/_test_fork/_m7_potenza_termostato.py [--passi=150] [--seme=11]
USCITA:   `csv/_test_fork/_m7_potenza_termostato/_m7_potenza_termostato.json` + stdout.
"""
import contextlib
import copy
import hashlib
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)
import numpy as np  # noqa: E402
import _cli_flag  # noqa: E402
import _passo  # noqa: E402

FUORI = os.path.join(RADICE, "csv", "_test_fork", "_m7_potenza_termostato")
SIM = os.path.join(RADICE, "soliton_simulator.py")
# i contatori di RIPIEGO che questa misura deve dichiarare a ZERO per essere leggibile.
RIPIEGHI = ("_ritmo_sicurezza", "_ritmo_snap_identico", "_g_temposegno_salti", "_tum_r_salti",
            "_g_registro_assenti", "_rep_dte_fallback", "_rep_realloc")


def blob(percorso):
    return hashlib.sha1(io.open(percorso, "rb").read()).hexdigest()


def carica(nome, seme):
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=%d" % seme],
                                              dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome=nome)
        S._applica_regime(a)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    return S, S.net


def k_fase(net):
    pv = np.asarray(net.phivel, float)[:int(net.n)]
    return float(0.5 * np.sum(pv ** 2))


def k_metr(net):
    vd = np.asarray(net.vd, float)
    return float(0.5 * np.sum(vd ** 2))


def principale():
    seme, passi = 11, 150
    for x in sys.argv[1:]:
        if x.startswith("--seme="):
            seme = int(x.split("=", 1)[1])
        elif x.startswith("--passi="):
            passi = int(x.split("=", 1)[1])
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    P = []

    def stampa(*x):
        r = " ".join(str(y) for y in x)
        P.append(r)
        print(r)

    stampa("=" * 104)
    stampa("M7 -- LA POTENZA DEL SOLO TERMINE DEL TERMOSTATO (-xi*phivel)")
    stampa("=" * 104)
    stampa("simulatore ..... %s" % blob(SIM)[:8])
    stampa("questo strumento %s" % blob(os.path.abspath(__file__))[:8])
    stampa("seme %d   passi %d" % (seme, passi))
    stampa("")
    S, net = carica("m7", seme)
    _cli_flag.dichiara_configurazione(S, stampa)
    stampa("")

    M_PH = float(getattr(S, "M_PH", 1.0))
    DT = float(getattr(S, "DT", float("nan")))
    TS = bool(getattr(S, "TEMPO_SEGNO", False))
    stampa("=" * 104)
    stampa("LE PREMESSE DELLA MISURA, dichiarate PRIMA dei numeri")
    stampa("=" * 104)
    stampa("  M_PH = %s   DT = %s   TEMPO_SEGNO = %s" % (M_PH, DT, TS))
    if TS:
        stampa("  ### ⚠ `TEMPO_SEGNO` E' ACCESO: `dt_n_s` NON e' `dt_n`, e questa misura")
        stampa("      NON si puo' leggere come scritta. Si ferma qui.")
        return 1
    stampa("  -> `dt_n_s = dt_n` (una riga del codice, col flag spento), quindi")
    stampa("     W_termo = -(xi/M_PH) * sum(dt_n * phivel_t^2)")
    stampa("")

    serie = []
    stato = {"passo": 0, "prima": None}
    vero = S._ferma_se_registro_incoerente

    def spia(nt, dove, voce=None, comp=None):
        c = list(comp) if comp else list(getattr(S, "PASSO_COMPOSIZIONE", ()))
        # ### il confine si RICAVA dalla composizione, non si cabla.
        prima_di_step = (c[c.index("step") - 1] if "step" in c and c.index("step") > 0 else None)
        if voce == "apri":
            stato["K_apri"] = k_fase(nt)
        if voce is not None and voce == prima_di_step:
            # ### la fotografia che `step` usera' come `_phivel_t`
            pv = np.asarray(nt.phivel, float)[:int(nt.n)].copy()
            # ### `ritmo()` SCRIVE: si chiama su una COPIA PROFONDA.
            cop = copy.deepcopy(nt)
            prima_rip = {k: int(getattr(cop, k, 0)) for k in RIPIEGHI}
            try:
                r = cop.ritmo()
            except Exception as e:
                r = "ECCEZIONE: %s" % type(e).__name__
            dopo_rip = {k: int(getattr(cop, k, 0)) for k in RIPIEGHI}
            scattati = {k: dopo_rip[k] - prima_rip[k] for k in RIPIEGHI
                        if dopo_rip[k] != prima_rip[k]}
            if isinstance(r, str):
                stato["prima"] = {"errore": r}
            elif r is None:
                stato["prima"] = {"phivel_t": pv, "dt_n": np.full(len(pv), DT),
                                  "orologio": "GLOBALE (ritmo() = None)", "ripieghi": scattati,
                                  "K_prima": k_fase(nt), "K_metr_prima": k_metr(nt)}
            else:
                rr = np.asarray(r, float)[:len(pv)]
                stato["prima"] = {"phivel_t": pv, "dt_n": DT * rr,
                                  "orologio": "PER NODO", "ripieghi": scattati,
                                  "r_min": float(rr.min()), "r_max": float(rr.max()),
                                  "K_prima": k_fase(nt), "K_metr_prima": k_metr(nt)}
            stato["K_prima_step"] = k_fase(nt)
            stato["K_scuot"] = k_fase(nt) - stato.get("K_apri", k_fase(nt))
        if voce == "step" and stato.get("prima") is not None:
            p = stato["prima"]
            riga = {"passo": stato["passo"], "xi": float(getattr(nt, "xi_termo", 0.0))}
            if "errore" in p:
                riga["non_misurabile"] = p["errore"]
            else:
                dt_n = p["dt_n"]
                pv = p["phivel_t"]
                m = min(len(dt_n), len(pv))
                W = float(-(riga["xi"] / M_PH) * np.sum(dt_n[:m] * pv[:m] ** 2))
                dK = k_fase(nt) - p["K_prima"]
                riga.update({"W_termo": W, "dK_step": dK, "resto": dK - W,
                             "K_prima": p["K_prima"], "K_dopo": k_fase(nt),
                             "dK_metr_step": k_metr(nt) - p["K_metr_prima"],
                             "dK_scuotimento": stato.get("K_scuot"),
                             "orologio": p["orologio"], "ripieghi_scattati": p["ripieghi"],
                             "r_min": p.get("r_min"), "r_max": p.get("r_max")})
            serie.append(riga)
            stato["prima"] = None
        return vero(nt, dove, voce=voce, comp=comp)

    S._ferma_se_registro_incoerente = spia
    for k in range(1, passi + 1):
        stato["passo"] = k
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(S, net)
    S._ferma_se_registro_incoerente = vero

    # ------------------------------------------------------------ il referto
    # ### UN RIPIEGO SQUALIFICA IL PASSO IN CUI E' SCATTATO, NON LA MISURA INTERA.
    #   (Prima lo dichiaravo globalmente: troppo grossolano, e buttava via 149 passi buoni
    #    per uno in cui `ritmo()` e' caduto nel suo ramo di sicurezza.)
    buoni = [r for r in serie if "W_termo" in r and not r.get("ripieghi_scattati")]
    squalificati = [r for r in serie if r.get("ripieghi_scattati")]
    rip = {}
    for r in serie:
        for k, v in (r.get("ripieghi_scattati") or {}).items():
            rip[k] = rip.get(k, 0) + v
    stampa("=" * 104)
    stampa("I RIPIEGHI: questa misura e' leggibile SOLO se sono tutti a ZERO")
    stampa("=" * 104)
    stampa("  passi misurati: %d su %d" % (len(buoni), passi))
    if rip:
        stampa("  ### ⚠ RIPIEGHI SCATTATI, in totale: %s" % rip)
        stampa("  ### -> I PASSI SQUALIFICATI SONO %d, e NON entrano nei totali:"
               % len(squalificati))
        for r in squalificati:
            stampa("      passo %d: %s" % (r["passo"], r.get("ripieghi_scattati")))
        stampa("      ⚠ `_ritmo_sicurezza` vuol dire che `ritmo()` e' caduto nel suo ramo di")
        stampa("        sicurezza e ha restituito UN OROLOGIO UNIFORME (`np.ones`): e' LA STESSA")
        stampa("        trappola del braccio C del sigillo del commit 2 -- ma qui IL CONTATORE")
        stampa("        L'HA VISTA, ed e' esattamente per questo che il mandato chiede di")
        stampa("        controllarli.")
    else:
        stampa("  ### NESSUN RIPIEGO SCATTATO su %d chiamate a `ritmo()`." % len(serie))
        stampa("      (controllati: %s)" % ", ".join(RIPIEGHI))
    if buoni:
        stampa("  orologio: %s   r in [%s, %s]"
               % (buoni[-1]["orologio"], buoni[-1].get("r_min"), buoni[-1].get("r_max")))
    stampa("")

    if not buoni:
        stampa("### NESSUN PASSO MISURABILE. Il referto si ferma qui.")
        return 1

    W = np.array([r["W_termo"] for r in buoni])
    dK = np.array([r["dK_step"] for r in buoni])
    resto = np.array([r["resto"] for r in buoni])
    scu = np.array([(r["dK_scuotimento"] or 0.0) for r in buoni])
    rifornisce = int(np.count_nonzero(W > 0))
    frena = int(np.count_nonzero(W < 0))

    stampa("=" * 104)
    stampa("LA POTENZA DEL SOLO TERMOSTATO, per passo")
    stampa("=" * 104)
    stampa("  %6s %14s %14s %14s %14s %10s"
           % ("passo", "W_termo", "dK_step", "resto", "scuotimento", "xi"))
    _righe = (buoni if len(buoni) <= 10 else buoni[:5] + [None] + buoni[-5:])
    for r in _righe:
        if r is None:
            stampa("  %6s" % "...")
            continue
        stampa("  %6d %+14.4e %+14.4e %+14.4e %+14.4e %+10.4f"
               % (r["passo"], r["W_termo"], r["dK_step"], r["resto"],
                  r["dK_scuotimento"] or 0.0, r["xi"]))
    stampa("")
    stampa("  ### IL TERMOSTATO: RIFORNISCE in %d passi, FRENA in %d, su %d misurati"
           % (rifornisce, frena, len(buoni)))
    stampa("  W_termo: somma %+.6e   mediana %+.6e   min %+.6e   max %+.6e"
           % (float(W.sum()), float(np.median(W)), float(W.min()), float(W.max())))
    stampa("  dK_step: somma %+.6e      resto (coppia + 2 ordine): somma %+.6e"
           % (float(dK.sum()), float(resto.sum())))
    stampa("  scuotimento: somma %+.6e" % float(scu.sum()))

    stampa("")
    stampa("=" * 104)
    stampa("LA DOMANDA DELLA DECISIONE 4: IL VUOTO COPRE IL TERMOSTATO?")
    stampa("=" * 104)
    rif = W[W > 0]
    somma_rif = float(rif.sum()) if rif.size else 0.0
    somma_scu = float(scu.sum())
    rapporto = (somma_scu / somma_rif) if somma_rif else None
    stampa("  energia RIFORNITA dal termostato (solo i passi con W>0): %+.6e" % somma_rif)
    stampa("  energia IMMESSA dallo scuotimento (tutti i passi) ......: %+.6e" % somma_scu)
    if rapporto is not None:
        stampa("  ### RAPPORTO scuotimento / rifornimento del termostato: %.4f" % rapporto)
        if rapporto >= 1.0:
            stampa("  ### -> SI': il vuoto immette PIU' di quanto il termostato rifornisce,")
            stampa("      quindi in TOTALE lo COPRE. ⚠ Ma <<in totale>> non e' <<passo per")
            stampa("      passo>>, e nemmeno <<nello stesso LUOGO>>: il vuoto e' locale, il")
            stampa("      termostato e' globale. La copertura TOTALE non garantisce quella LOCALE.")
        else:
            stampa("  ### -> NO: il vuoto immette MENO di quanto il termostato rifornisce.")
            stampa("      Togliere il termostato lascerebbe un deficit, e il calore locale")
            stampa("      da solo NON basta a sostituirlo.")
    copre_sempre = int(np.count_nonzero(scu >= np.maximum(W, 0.0)))
    stampa("  passi in cui lo scuotimento copre il termostato DA SOLO: %d su %d"
           % (copre_sempre, len(buoni)))

    fuori = {"blob_sim_sha1_byte": blob(SIM), "blob_strumento": blob(os.path.abspath(__file__)),
             "seme": seme, "passi": passi, "M_PH": M_PH, "DT": DT, "TEMPO_SEGNO": TS,
             "ripieghi_scattati": rip, "passi_misurati": len(buoni),
             "passi_squalificati": [{"passo": r["passo"],
                                     "ripieghi": r.get("ripieghi_scattati")}
                                    for r in squalificati],
             "W_termo_somma": float(W.sum()), "W_termo_mediana": float(np.median(W)),
             "rifornisce": rifornisce, "frena": frena,
             "dK_step_somma": float(dK.sum()), "resto_somma": float(resto.sum()),
             "scuotimento_somma": somma_scu, "rifornimento_termostato": somma_rif,
             "rapporto_scuotimento_su_rifornimento": rapporto,
             "passi_in_cui_il_vuoto_copre_da_solo": copre_sempre,
             "serie": [{k: v for k, v in r.items() if k != "ripieghi_scattati"} for r in buoni]}
    json.dump(fuori, io.open(os.path.join(FUORI, "_m7_potenza_termostato.json"), "w",
                             encoding="utf-8"), indent=1, ensure_ascii=False)
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8").write(chr(10).join(P))
    stampa("")
    stampa("scritto: %s" % os.path.join(FUORI, "_m7_potenza_termostato.json"))
    return 0


if __name__ == "__main__":
    sys.exit(principale())
