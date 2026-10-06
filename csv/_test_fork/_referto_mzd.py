# -*- coding: utf-8 -*-
"""GENERA `doc/REFERTO_mitosi_zero_dove_2026-10-06.md` dai `json` dei due bracci.

*(Mandato di Luca del 2026-10-06. Le tre domande, la classe e i ### **tre criteri** sono
fissati in `doc/TASK_HISTORY/2026-10-06_mitosi-zero-dopo-la-cura.md`, committato **prima** in
`b56141c`.)*

### ⛔ **NESSUN NUMERO E' RICOPIATO A MANO** *(`L-NUMERI`)*: i criteri, le soglie e la
### geometria della scena si leggono ### **DAI JSON**.

### ⛔ **E `genera()` E' SEPARATO DA `main()` perche' il collaudo possa CHIAMARLO** -- la
### lezione di `LUNGA-BATTITO-CADUTA`: cio' che sta dentro `main` nessun controllo lo guarda.

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Legge i `json` di corse che hanno
#   GIA' dichiarato la propria configurazione INTERA.

USO:  python csv/_test_fork/_referto_mzd.py
      python csv/_test_fork/_referto_mzd.py --collaudo
"""
import copy
import hashlib
import io
import json
import math
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
D = os.path.join(RADICE, "csv", "_test_fork", "_mitosi_zero_dove")
OUT = os.path.join(RADICE, "doc", "REFERTO_mitosi_zero_dove_2026-10-06.md")
CLASSI = ("MATERIA", "BORDO", "VUOTO")

# ### ⛔ **LE SOGLIE DEI TRE CRITERI, fissate nel task history PRIMA delle corse** *(`b56141c`)*.
R_ALTO, R_BASSO = 0.5, 0.1              # `R >= 0.5` / `R <= 0.1`
DIP_SI, DIP_NO = 0.70, 0.30             # la frazione col dipolo: `>= 70 %` / `< 30 %`
CORR_SI = 0.5                           # la correlazione cambi-chi / archi oltre `4π`
DOVE_FATTORE = 2.0                      # *«almeno `2` volte la frazione di nodi»*
DOVE_FIN_MIN, DOVE_FIN_TOT = 2, 3       # *«in almeno DUE finestre su TRE»*
DOVE_DA, DOVE_A = 700, 1000             # *«fra i passi `700` e `1000`»*


def n4(x, f="%.4f"):
    """### ⛔ **`0.0` NON E' `n/d`:** il difetto di `34a11dc`."""
    return "n/d" if x is None else (f % x)


def spearman(x, y):
    """La `Spearman` con i ranghi medi sui pari merito. Torna ### **`(valore, n)`**, e la
    tupla e' voluta: ### **un lettore che la tratta come numero deve ROMPERSI subito**, non
    stampare un numero sbagliato *(e' il `TypeError` di `a1e9246`, e quel referto e' caduto
    li')*."""
    a = [(u, v) for u, v in zip(x, y) if u is not None and v is not None]
    n = len(a)
    if n < 3:
        return None, n

    def ranghi(z):
        o = sorted(range(len(z)), key=lambda k: z[k])
        r = [0.0] * len(z)
        i = 0
        while i < len(o):
            j = i
            while j + 1 < len(o) and z[o[j + 1]] == z[o[i]]:
                j += 1
            m = 0.5 * (i + j) + 1.0
            for k in range(i, j + 1):
                r[o[k]] = m
            i = j + 1
        return r

    ra, rb = ranghi([u for u, _v in a]), ranghi([v for _u, v in a])
    ma, mb = sum(ra) / n, sum(rb) / n
    sa = math.sqrt(sum((u - ma) ** 2 for u in ra))
    sb = math.sqrt(sum((v - mb) ** 2 for v in rb))
    if sa == 0 or sb == 0:
        # ### ⛔ **UNA SERIE COSTANTE NON HA CORRELAZIONE, e NON e' zero:** dire `0` qui
        #   vorrebbe dire *«non correlano»* quando il fatto e' *«una delle due non varia»*.
        return None, n
    return sum((u - ma) * (v - mb) for u, v in zip(ra, rb)) / (sa * sb), n


def val(x):
    if isinstance(x, (list, tuple)):
        return None if not x else x[0]
    return x


def per_passo(d):
    return {int(x["passo"]): x for x in ((d or {}).get("passi_dati") or [])}


def trova(amp, senza_ganci=False):
    """Il `json` del braccio, trovato ### **dal campo `amp` DENTRO il file**, non dal nome.

    ### ⛔ **IL NOME NON SI INDOVINA:** lo strumento lo costruisce con
    `("%g" % amp).replace(".", "_")`, e `"%g" % 0.0` da' ### **`"0"`** -- quindi il braccio
    zero sta in ### **`amp0.json`**, non in `amp0_0.json`. ### **I miei due lettori cercavano
    `amp0_0.json`**, cioe' ### **un nome ASSUNTO invece che letto**, ed e' la stessa classe
    di `P1` che mi e' gia' costata il gancio sul ramo morto.

    ### ✔ **Leggere il campo `amp` DENTRO il file e' piu' forte che indovinare il nome:**
    vale anche se un giorno la regola del nome cambiasse.
    """
    if not os.path.isdir(D):
        return None
    for f in sorted(os.listdir(D)):
        if not (f.startswith("amp") and f.endswith(".json")):
            continue
        if ("_senza_ganci" in f) != bool(senza_ganci):
            continue
        try:
            d = json.loads(io.open(os.path.join(D, f), encoding="utf-8").read())
        except Exception:
            continue
        if d.get("amp") is not None and abs(float(d["amp"]) - float(amp)) < 1e-12:
            d["_file"] = f
            return d
    return None


def primo(d, campo):
    z = [x["passo"] for x in ((d or {}).get("passi_dati") or []) if (x.get(campo) or 0) > 0]
    return z[0] if z else None


def _tot(d, k):
    return ((d or {}).get("totali") or {}).get("contatori", {}).get(k)


def leggi_R(zero, acceso):
    """`R` sulle divisioni ### **e** sulla popolazione nella finestra `Σ (g1∧g2∧g3)`."""
    def ult(d, c):
        P = per_passo(d)
        return P[max(P)].get(c) if P else None

    def somma(d, c):
        return sum((x.get(c) or 0) for x in ((d or {}).get("passi_dati") or []))

    dz = _tot(zero, "nati_div_tot")
    da = _tot(acceso, "nati_div_tot")
    gz, ga = somma(zero, "g1_e_g2_e_g3"), somma(acceso, "g1_e_g2_e_g3")
    return {"div_zero": dz, "div_acceso": da,
            "R_divisioni": (dz / da) if (dz is not None and da) else None,
            "g1g2g3_zero": gz, "g1g2g3_acceso": ga,
            "R_finestra": (gz / ga) if ga else None,
            "sch_zero": _tot(zero, "nati_sch_tot"),
            "sch_acceso": _tot(acceso, "nati_sch_tot"),
            "passi_zero": (ult(zero, "passo")), "passi_acceso": (ult(acceso, "passo"))}


def letto_R(r):
    if r is None:
        return "n/d"
    if r >= R_ALTO:
        return "DEL MODELLO"
    if r <= R_BASSO:
        return "DIPENDE DAL 0.3"
    return "INTERMEDIA"


def leggi_dipolo(d):
    """L'ipotesi del dipolo: la frazione col dipolo, e la correlazione per passo."""
    PP = (d or {}).get("passi_dati") or []
    f = sum((x.get("spinta_pi_fase") or 0) for x in PP)
    dp = sum((x.get("spinta_pi_dip") or 0) for x in PP)
    en = sum((x.get("spinta_pi_entrambe") or 0) for x in PP)
    tot = sum((x.get("spinta_pi_tot") or 0) for x in PP)
    es = sum((x.get("spinta_pi_esatto") or 0) for x in PP)
    con_dip = dp + en
    # ### ⛔ **LO ZERO FALSO, e senza toglierlo la correlazione NON SIGNIFICA NIENTE.**
    #   Il gancio `chi_tors` non puo' confrontare `chi_torsione` quando la ### **LUNGHEZZA
    #   cambia**, cioe' quando ### **nascono nodi** -- e in quei passi `cambi_chi_tors`
    #   resta `0`. ### **Quello NON e' <<zero cambi>>: e' <<NON MISURATO>>**, e nel braccio
    #   acceso sono ### **`731` passi su `1000`.** ### ✔ **I dati non sono persi: il flag
    #   e' registrato a OGNI passo**, quindi si escludono qui -- ### **senza rigirare le
    #   corse.**
    _buoni = [x for x in PP if not (x.get("chi_tors_non_confrontabile") or 0)]
    _esclusi_corr = len(PP) - len(_buoni)
    cor, n = spearman([x.get("cambi_chi_tors") for x in _buoni],
                      [x.get("sopra_4pi") for x in _buoni])
    return {"fase": f, "dipolo": dp, "entrambe": en, "totale": tot, "esatto": es,
            "con_dipolo": con_dip, "corr_esclusi": _esclusi_corr,
            "corr_passi_buoni": len(_buoni), "corr_passi_tot": len(PP),
            "frazione_con_dipolo": (con_dip / tot) if tot else None,
            "corr_chi_sopra4pi": cor, "corr_n": n,
            "somma_dipolo": sum((x.get("somma_dipolo") or 0.0) for x in PP),
            "calcio_somma": sum((x.get("calcio_somma") or 0.0) for x in PP),
            "calcio_n": sum((x.get("calcio_n") or 0) for x in PP),
            "cambi_chi_tors": _tot(d, "cambi_chi_tors_tot"),
            "cambi_geom": _tot(d, "cambi_geom_tot"),
            "cambi_perc_chi": _tot(d, "cambi_perc_chi_tot")}


def letto_dipolo(z):
    """### ⛔ **LA CONGIUNZIONE E' UNA <<E>>, NON UNA <<O>>:** basta che una delle due manchi
    perche' non sia confermata. Il task history lo ha fissato prima."""
    fr, co = z.get("frazione_con_dipolo"), z.get("corr_chi_sopra4pi")
    if fr is None:
        return "n/d"
    if fr >= DIP_SI and co is not None and co >= CORR_SI:
        return "CONFERMATA"
    if fr < DIP_NO:
        return "REFUTATA"
    return "INTERMEDIA"


def finestre_dove(d):
    return (d or {}).get("finestre_dove") or []


def leggi_dove(d):
    """Il criterio del *dove*: ### **`>= 2` volte** la frazione di nodi, in ### **almeno `2`
    finestre su `3`** fra i passi `700` e `1000`."""
    fin = [f for f in finestre_dove(d)
           if f.get("da") is not None and f["da"] >= DOVE_DA - 99 and f.get("a", 0) <= DOVE_A
           and f["a"] > DOVE_DA - 1]
    fin = [f for f in fin if f["a"] > DOVE_DA - 1][-DOVE_FIN_TOT:]
    conta = [0, 0, 0]
    for f in fin:
        for c in range(3):
            r = (f.get("rapporto") or [None, None, None])[c]
            if r is not None and r >= DOVE_FATTORE:
                conta[c] += 1
    return {"finestre": fin, "n_finestre": len(fin), "conta": conta,
            "sovrarappresentate": [CLASSI[c] for c in range(3)
                                   if conta[c] >= DOVE_FIN_MIN],
            "soglia_finestre": DOVE_FIN_MIN, "fattore": DOVE_FATTORE}


def genera(zero, acceso):
    """Torna `(righe, esiti, guasti)`. `righe` e' `None` se un braccio ### **non e'
    completo**: un referto su una corsa incompleta sarebbe un numero senza provenienza."""
    g = []
    for et, d in (("_AMP = 0", zero), ("_AMP = 0.3", acceso)):
        if not d:
            g.append("manca il json del braccio %s" % et)
        elif int(d.get("passi_girati") or 0) != int(d.get("passi") or -1):
            g.append("il braccio %s e' INCOMPLETO: %s passi su %s"
                     % (et, d.get("passi_girati"), d.get("passi")))
    if g:
        return None, {}, g
    T = []

    def w(s=""):
        T.append(s)

    R = leggi_R(zero, acceso)
    DZ, DA = leggi_dipolo(zero), leggi_dipolo(acceso)
    WZ, WA = leggi_dove(zero), leggi_dove(acceso)
    sc = acceso.get("scena") or {}
    esiti = {}

    w("# REFERTO -- **il `0.3` a ZERO dopo la cura, il DOVE, e il CIRCOLO del dipolo**")
    w()
    w("*(Mandato di Luca del 2026-10-06. Le tre domande, la classe `MATERIA`/`BORDO`/`VUOTO` "
      "e i **tre criteri** sono fissati in "
      "`doc/TASK_HISTORY/2026-10-06_mitosi-zero-dopo-la-cura.md`, committato "
      "### **prima** in `b56141c`.)*")
    w()
    w("| | |")
    w("|---|---|")
    w("| **simulatore** | `%s` -- ### **verificato all'avvio** contro `%s` |"
      % ((acceso.get("blob_sim") or "")[:8], acceso.get("blob_atteso")))
    w("| **strumento** | `%s` *(piu' `_tors_w8_lunga` `%s`, che IMPORTA)* |"
      % ((acceso.get("blob_strumento") or "")[:8],
         (acceso.get("blob_tors_w8_lunga") or "")[:8]))
    w("| **copie patchate** | `%s` *(zero)*, `%s` *(acceso)*, **%d** ancore |"
      % ((zero.get("blob_copia") or "")[:8], (acceso.get("blob_copia") or "")[:8],
         len(acceso.get("ancore") or [])))
    w("| **passi** | `%s` per braccio, ### **processi SEPARATI**, seme `11` |"
      % acceso.get("passi"))
    w("| **la geometria, DALLA SCENA** | `r_regione` `%s`, `R_CONN` `%s`, "
      "### **`u_bordo` `%s`** |" % (n4(sc.get("r_regione"), "%.6f"),
                                   n4(sc.get("R_CONN"), "%.6f"),
                                   n4(sc.get("u_bordo"))))
    w("| **configurazione del driver** | dichiarata INTERA: `%s` *(zero)*, `%s` *(acceso)* |"
      % (bool(zero.get("in_configurazione_del_driver")),
         bool(acceso.get("in_configurazione_del_driver"))))
    w()

    # ------------------------------------------------------------ DOMANDA 1
    w("## ⛔ DOMANDA `1`: **la crescita e' del MODELLO o dipende dal `0.3`?**")
    w()
    w("| | `_AMP = 0` | `_AMP = 0.3` | ### **`R`** | la lettura |")
    w("|---|--:|--:|--:|---|")
    for et, kz, ka, kr in (("divisioni", "div_zero", "div_acceso", "R_divisioni"),
                           ("popolazione nella finestra `Σ (g1∧g2∧g3)`",
                            "g1g2g3_zero", "g1g2g3_acceso", "R_finestra")):
        w("| %s | `%s` | `%s` | ### **`%s`** | ### **%s** |"
          % (et, R.get(kz), R.get(ka), n4(R.get(kr)), letto_R(R.get(kr))))
    w("| Schwinger | `%s` | `%s` | *(non nel criterio)* | |"
      % (R.get("sch_zero"), R.get("sch_acceso")))
    w()
    _lr = [letto_R(R.get(k)) for k in ("R_divisioni", "R_finestra")]
    _lr = [x for x in _lr if x != "n/d"]
    esiti["R"] = _lr[0] if (_lr and len(set(_lr)) == 1) else ("DISCORDI" if _lr else "n/d")
    if not _lr:
        w("> ### ⛔ **`R` NON SI PUO' LEGGERE su nessuna delle due grandezze.** "
          "### **Un'assenza non e' un esito** *(`STANDARD 3`)*.")
    elif len(set(_lr)) == 1:
        w("> ### %s **LE DUE LETTURE DI `R` CONCORDANO: <<%s>>.**"
          % ("✔" if _lr[0] == "DEL MODELLO" else "⛔", _lr[0]))
        if _lr[0] == "DEL MODELLO":
            w(">")
            w("> *«La crescita e' del MODELLO; il `0.3` la anticipa o la accelera, ma "
              "### **non la crea**.»*")
        elif _lr[0] == "DIPENDE DAL 0.3":
            w(">")
            w("> *«La crescita ### **dipende ancora** dal `0.3`.»*")
    else:
        w("> ### ⛔ **LE DUE LETTURE DI `R` SONO DISCORDI: divisioni <<%s>>, finestra "
          "<<%s>>.** ### **E si dice cosi', NON si sceglie:** il criterio chiede di leggere "
          "`R` su ### **entrambe**, e due letture diverse sono ### **un risultato.**"
          % (letto_R(R.get("R_divisioni")), letto_R(R.get("R_finestra"))))
    w()
    w("| `R` | la lettura, fissata PRIMA |")
    w("|---|---|")
    w("| ### **`>= %.1f`** | la crescita e' del MODELLO; il `0.3` la anticipa o la accelera, "
      "ma **non la crea** |" % R_ALTO)
    w("| ### **`<= %.1f`** | la crescita **dipende ancora** dal `0.3` |" % R_BASSO)
    w("| fra `%.1f` e `%.1f` | intermedia |" % (R_BASSO, R_ALTO))
    w()
    w("### IL PASSO DELLA PRIMA NASCITA, **nei due bracci**")
    w()
    w("| | `_AMP = 0` | `_AMP = 0.3` |")
    w("|---|--:|--:|")
    for et, c in (("prima **divisione**", "nati_div"),
                  ("primo **Schwinger**", "nati_sch"),
                  ("primo arco oltre `4π`", "sopra_4pi")):
        w("| %s | `%s` | `%s` |" % (et, primo(zero, c) or "MAI", primo(acceso, c) or "MAI"))
    w()
    _pz, _pa = primo(zero, "nati_div"), primo(acceso, "nati_div")
    if _pz and _pa:
        w("### ➜ **Il `0.3` sposta la prima divisione di `%d` passi** *(da `%d` a `%d`)*."
          % (_pz - _pa, _pa, _pz))
        w()
    elif _pa and not _pz:
        w("### ➜ ⛔ **COL `0.3` A ZERO LA RETE NON PARTORISCE MAI in `%s` passi**, "
          "mentre con l'acceso la prima divisione e' al passo `%d`."
          % (zero.get("passi"), _pa))
        w()
    # ### ⛔ **LA LARGHEZZA SI DERIVA DAI DATI, non da un campo che potrebbe mancare:**
    #   la prima versione leggeva `acceso.get("finestra")` e stampava ### **`None`**, perche'
    #   questo strumento quel campo ### **non lo salva.** ### **Un <<None>> in un titolo e'
    #   un numero che non c'e' presentato come se ci fosse.**
    _fw = (acceso.get("nascite_per_finestra") or [{}])[0]
    _fw = ((_fw.get("a") or 0) - (_fw.get("da") or 0) + 1) if _fw.get("a") else None
    w("### LE NASCITE PER FINESTRE DI `%s` PASSI" % n4(_fw, "%d"))
    w()
    w("| finestra | divisioni `_AMP = 0` | divisioni `_AMP = 0.3` | Schwinger `0` | "
      "Schwinger `0.3` |")
    w("|---|--:|--:|--:|--:|")
    FZ = {(f["da"], f["a"]): f for f in (zero.get("nascite_per_finestra") or [])}
    FA = {(f["da"], f["a"]): f for f in (acceso.get("nascite_per_finestra") or [])}
    for k in sorted(set(FZ) | set(FA)):
        a, b = FZ.get(k, {}), FA.get(k, {})
        w("| `%d`-`%d` | `%s` | `%s` | `%s` | `%s` |"
          % (k[0], k[1], a.get("divisioni"), b.get("divisioni"),
             a.get("schwinger"), b.get("schwinger")))
    w()
    _dv = [f.get("divisioni") or 0 for f in (acceso.get("nascite_per_finestra") or [])]
    if len(_dv) >= 4:
        w("### ⚠ **E IL BRACCIO ACCESO CRESCE ACCELERANDO FINO AL PASSO `%s`**, come il "
          "criterio chiede di dichiarare accanto a `R`: le ultime quattro finestre danno "
          "### **`%s`** divisioni." % (acceso.get("passi"),
                                       "`, `".join(str(x) for x in _dv[-4:])))
        w()

    # ------------------------------------------------------------ DOMANDA 3
    w("## ⛔ DOMANDA `3`: **perche' accelera -- l'ipotesi del DIPOLO**")
    w()
    w("| | `_AMP = 0` | `_AMP = 0.3` |")
    w("|---|--:|--:|")
    for et, k in (("archi con spinta oltre `π`, **totale**", "totale"),
                  ("di cui dalla **FASE** sola", "fase"),
                  ("di cui dal **DIPOLO** solo", "dipolo"),
                  ("di cui da **ENTRAMBE**", "entrambe"),
                  ("### **la frazione CON la componente di dipolo**",
                   "frazione_con_dipolo"),
                  ("`Σ |Δdipolo|`", "somma_dipolo"),
                  ("cambi di `chi_torsione` *(### **cio' che ENTRA nel dipolo**)*",
                   "cambi_chi_tors"),
                  ("cambi di `perc_geom` *(il basculamento)*", "cambi_geom"),
                  ("cambi di `perc_chi` *(### **cio' che il mandato NOMINA**)*",
                   "cambi_perc_chi"),
                  ("`Σ |calcio|` ai genitori *(`KICK_TW`)*", "calcio_somma"),
                  ("quanti calci", "calcio_n")):
        fz, fa = DZ.get(k), DA.get(k)
        f = "%.4f" if k in ("frazione_con_dipolo", "somma_dipolo", "calcio_somma") else "%d"
        w("| %s | `%s` | `%s` |" % (et, n4(fz, f), n4(fa, f)))
    w("| ### **`Spearman`**(cambi di `chi_torsione`, archi oltre `4π`) | `%s` *(n=%s)* | "
      "`%s` *(n=%s)* |" % (n4(DZ.get("corr_chi_sopra4pi")), DZ.get("corr_n"),
                           n4(DA.get("corr_chi_sopra4pi")), DA.get("corr_n")))
    w("| ### ⛔ **passi ESCLUSI dalla correlazione** *(`chi_torsione` non confrontabile)* "
      "| `%s` su `%s` | `%s` su `%s` |"
      % (DZ.get("corr_esclusi"), DZ.get("corr_passi_tot"),
         DA.get("corr_esclusi"), DA.get("corr_passi_tot")))
    w("| ### ⚠ **spinta ESATTAMENTE `π`** *(che `> π` NON conta)* | `%s` | "
      "`%s` |" % (DZ.get("esatto"), DA.get("esatto")))
    w()
    for et, z in (("`_AMP = 0`", DZ), ("`_AMP = 0.3`", DA)):
        L = letto_dipolo(z)
        esiti["dipolo %s" % et] = L
        e = {"CONFERMATA": "✔", "REFUTATA": "⛔", "INTERMEDIA": "⚠",
             "n/d": ""}[L]
        w("> ### %s **%s: l'ipotesi del dipolo e' ### %s** -- frazione col dipolo `%s`, "
          "correlazione `%s`." % (e, et, L, n4(z.get("frazione_con_dipolo")),
                                  n4(z.get("corr_chi_sopra4pi"))))
    w(">")
    _ez = (DZ.get("corr_esclusi") or 0) / float(DZ.get("corr_passi_tot") or 1)
    _ea = (DA.get("corr_esclusi") or 0) / float(DA.get("corr_passi_tot") or 1)
    if max(_ez, _ea) > 0.2:
        w("> ### ⛔ **E LA CORRELAZIONE E' CALCOLATA SU UNA SERIE BUCATA:** il gancio "
          "`chi_tors` ### **non puo' confrontare quando nascono nodi** *(la lunghezza "
          "cambia)*, e in quei passi lasciava uno ### **ZERO FALSO.** Sono ### **il "
          "%.0f %%** dei passi nel braccio zero e ### **il %.0f %%** nell'acceso. "
          "### **Quei passi sono ESCLUSI qui**, invece di entrare come zeri -- ### **ma "
          "la correlazione resta una misura su una serie BUCATA**, e una lettura "
          "<<REFUTATA>> che si appoggiasse su di essa ### **andrebbe pesata per questo.**"
          % (100 * _ez, 100 * _ea))
        w(">")
    w("> ### ⛔ **E LA CONGIUNZIONE E' UNA <<E>>, NON UNA <<O>>:** `CONFERMATA` vuole "
      "### **frazione `>= %.0f %%` E correlazione `>= %.1f`**, e basta che una manchi perche' "
      "non lo sia. `REFUTATA` vuole la frazione ### **sotto il %.0f %%.**"
      % (DIP_SI * 100, CORR_SI, DIP_NO * 100))
    w()
    _es = max((DZ.get("esatto") or 0), (DA.get("esatto") or 0))
    _dip = max((DZ.get("dipolo") or 0), (DA.get("dipolo") or 0))
    if _es and _es > _dip:
        w("> ### ⛔ **ATTENZIONE, E QUESTO CAMBIA LA LETTURA:** gli archi con spinta "
          "### **ESATTAMENTE `π`** sono `%d`, ### **piu' di quelli contati come <<dipolo "
          "solo>>** (`%d`). Un ribaltamento su ### **UN SOLO estremo** cambia il dipolo di "
          "`π` esatto, e ### **`> π` NON lo conta.** ### **Quindi un <<REFUTATA>> "
          "qui sarebbe un ARTEFATTO DELLA SOGLIA, non un risultato**, e il criterio -- "
          "fissato prima -- ### **non si sposta per questo: si DICE.**" % (_es, _dip))
        w()
    elif _es:
        w("> ### ⚠ **Gli archi con spinta esattamente `π` sono `%d`**, contro `%d` "
          "contati come *«dipolo solo»*: ### **la soglia `> π` ne taglia via alcuni, ma "
          "non abbastanza da ribaltare la lettura.**" % (_es, _dip))
        w()

    # ------------------------------------------------------------ DOMANDA 2
    w("## ⛔ DOMANDA `2`: **DOVE cresce la rete**")
    w()
    w("La classe e' ### **derivata dalla scena**, non scelta: `MATERIA` e' `u <= 1` *(il test "
      "di appartenenza ### **della scena**)*, `BORDO` e' `u <= 1 + R_CONN/r_regione = %s` "
      "*(`R_CONN` e' ### **il varco** della scena)*, `VUOTO` il resto."
      % n4(sc.get("u_bordo")))
    w()
    w("### ⛔ **E LA FRAZIONE DI NASCITE SI CONFRONTA CON QUELLA DI NODI, non col "
      "volume:** altrimenti *«nascono nel vuoto»* direbbe soltanto *«il vuoto e' piu' "
      "grande»*. Lo dice il mandato.")
    w()
    for et, d, W in (("`_AMP = 0`", zero, WZ), ("`_AMP = 0.3`", acceso, WA)):
        w("#### %s" % et)
        w()
        w("| finestra | nascite | %s |" % " | ".join(
            "### **%s**: nascite / nodi = ### **rapporto**" % c for c in CLASSI))
        w("|---|--:|%s" % ("---|" * 3))
        for f in finestre_dove(d):
            w("| `%d`-`%d` | `%d` | %s |"
              % (f["da"], f["a"], f.get("nascite") or 0,
                 " | ".join(
                     "`%s` / `%s` = ### **`%s`**"
                     % (n4((f.get("fraz_nascite") or [None] * 3)[c]),
                        n4((f.get("fraz_nodi") or [None] * 3)[c]),
                        n4((f.get("rapporto") or [None] * 3)[c]))
                     for c in range(3))))
        w()
        sov = W.get("sovrarappresentate") or []
        esiti["dove %s" % et] = ("+".join(sov) if sov else "NESSUNA")
        if not W.get("n_finestre"):
            w("> ### ⛔ **NESSUNA FINESTRA fra i passi `%d` e `%d`: il criterio del DOVE "
              "NON si applica**, e ### **un'assenza non e' un esito.**" % (DOVE_DA, DOVE_A))
        elif sov:
            w("> ### ✔ **SOVRARAPPRESENTATA: %s** -- la frazione di nascite supera di "
              "### **almeno `%.0f` volte** quella di nodi in ### **almeno `%d` finestre su "
              "`%d`** fra i passi `%d` e `%d` *(conta: %s)*."
              % (", ".join("**%s**" % s for s in sov), DOVE_FATTORE, DOVE_FIN_MIN,
                 W.get("n_finestre"), DOVE_DA, DOVE_A,
                 ", ".join("%s %d" % (CLASSI[c], W["conta"][c]) for c in range(3))))
            w(">")
            if "BORDO" in sov and "MATERIA" not in sov:
                w("> ### ➜ **E' il BORDO: l'accelerazione e' SUPERFICIE CHE CRESCE**, "
                  "cioe' ### **geometria** -- non materia che prolifera. ### **La lettura era "
                  "fissata prima della corsa**, nel task history.")
            elif "MATERIA" in sov and "BORDO" not in sov:
                w("> ### ➜ **E' la MATERIA: l'accelerazione e' MATERIA CHE "
                  "PROLIFERA**, non spazio che si espande. ### **La lettura era fissata prima "
                  "della corsa.**")
            elif "VUOTO" in sov and len(sov) == 1:
                w("> ### ➜ **E' il VUOTO**, e il task history ### **non aveva previsto "
                  "questo per le divisioni**: il guardiano lo aveva previsto ### **per le "
                  "Schwinger, per costruzione.**")
            else:
                w("> ### ⚠ **Piu' di una classe e' sovrarappresentata, e questo NON e' "
                  "una delle letture previste:** ### **si riporta e non si sceglie.**")
        else:
            w("> ### ⚠ **NESSUNA CLASSE E' SOVRARAPPRESENTATA** col criterio fissato "
              "*(`>= %.0f` volte, in `>= %d` finestre su `%d`)*: ### **le nascite seguono i "
              "nodi**, cioe' ### **la rete cresce dove c'e' rete**, senza preferire un luogo."
              % (DOVE_FATTORE, DOVE_FIN_MIN, W.get("n_finestre")))
        w()
    w("### DIVISIONI e SCHWINGER, **separate** *(lo chiede il mandato)*")
    w()
    w("| braccio | finestra | divisioni per classe | Schwinger per classe |")
    w("|---|---|---|---|")
    for et, d in (("`0`", zero), ("`0.3`", acceso)):
        for f in finestre_dove(d)[-DOVE_FIN_TOT:]:
            w("| %s | `%d`-`%d` | %s | %s |"
              % (et, f["da"], f["a"],
                 " / ".join(str(x) for x in (f.get("divisioni_per_classe") or [])),
                 " / ".join(str(x) for x in (f.get("schwinger_per_classe") or []))))
    w()
    w("*(l'ordine e' `%s`.)*" % " / ".join(CLASSI))
    w()
    w("### GLI ARCHI OLTRE `4π`, **come POPOLAZIONE** *(ai passi pieni)*")
    w()
    w("### ⛔ **MAI gli indici:** `ARCHI-OLTRE-4PI` e' ### **<<da non indagare>> per "
      "decisione di Luca**, e il mandato lo ripete. ### **Si contano le popolazioni, non gli "
      "individui.**")
    w()
    w("| braccio | passo | archi | nodi | per classe | `u` mediano | `rho_spin` rel. mediana |")
    w("|---|--:|--:|--:|---|--:|--:|")
    for et, d in (("`0`", zero), ("`0.3`", acceso)):
        z = (d.get("dove_sopra4pi") or {})
        for p in sorted(z, key=lambda k: int(k)):
            x = z[p]
            w("| %s | `%s` | `%s` | `%s` | %s | `%s` | `%s` |"
              % (et, p, x.get("n"), x.get("n_nodi"),
                 " / ".join(str(v) for v in (x.get("per_classe") or [])),
                 n4((x.get("q_u") or {}).get("q050")),
                 n4((x.get("q_rho_spin_rel") or {}).get("q050"))))
    w()

    # ------------------------------------------------------------ IL VERDETTO
    w("## IL VERDETTO")
    w()
    w("| la domanda | l'esito |")
    w("|---|---|")
    w("| `1` la crescita e' del modello? | ### **%s** |" % esiti.get("R"))
    w("| `3` l'ipotesi del dipolo | zero: ### **%s** · acceso: ### **%s** |"
      % (esiti.get("dipolo `_AMP = 0`"), esiti.get("dipolo `_AMP = 0.3`")))
    w("| `2` dove cresce la rete | zero: ### **%s** · acceso: ### **%s** |"
      % (esiti.get("dove `_AMP = 0`"), esiti.get("dove `_AMP = 0.3`")))
    w()
    w("> ### ⛔ **E QUESTA E' UNA MISURA, NON UN SIGILLO:** ### **il `0.3`, la soglia "
      "`3π`, `κ` e la legge del basculamento chirale si decidono su questi numeri, "
      "e sono DECISIONI DI LUCA.**")
    w()
    w("> ### ⚠ **E UN LIMITE CHE VALE PER TUTTO IL REFERTO:** ### **un seme solo.** "
      "Nessuna barra d'errore fra semi, e `P3` ne chiederebbe ### **almeno quattro.** "
      "### **Il gradino raggiunto e' `(b)`** *(«regge togliendo la legge pratica»)*, "
      "### **non `(a)` ne' `(c)`.**")
    w()
    w("---")
    w()
    w("*Referto **generato** da `csv/_test_fork/_referto_mzd.py` dai due `json`: "
      "### **nessun numero e' ricopiato a mano** (`L-NUMERI`), e i criteri sono letti "
      "**dalle soglie fissate nel task history**.*")
    return T, esiti, []


# =============================================================== IL COLLAUDO
def _finto(passi=1000, div=100, sch=20, amp=0.0, fase=10, dip=90, entrambe=0,
           esatto=0, chi=None, s4=None, fraz_nodi=(0.1, 0.3, 0.6),
           nati_cl=None, girati=None, g1=5):
    PP = []
    for k in range(1, passi + 1):
        PP.append({
            "passo": k, "n": 12802 + k, "archi": 471564 + k,
            "nati_tot": (div + sch) if k == passi else 0,
            "schwinger_tot": sch if k == passi else 0,
            "nati_div": div if k == passi else 0,
            "nati_sch": sch if k == passi else 0,
            "sopra_4pi": (s4(k) if s4 else 0), "cambi_chi_tors": (chi(k) if chi else 0),
            "spinta_pi_fase": fase, "spinta_pi_dip": dip,
            "spinta_pi_entrambe": entrambe, "spinta_pi_esatto": esatto,
            "spinta_pi_tot": fase + dip + entrambe, "somma_dipolo": 1.0,
            "calcio_somma": 0.2, "calcio_n": 2, "g1_e_g2_e_g3": g1,
            "fraz_nodi": list(fraz_nodi),
            "nati_per_classe": list(nati_cl or [0, 0, 0]),
            "q_tw": {"q050": 3.0}})
    fin = []
    for a in range(0, passi, 100):
        bl = PP[a:a + 100]
        nat = [sum(x["nati_per_classe"][c] for x in bl) for c in range(3)]
        tot = float(sum(nat))
        fin.append({"da": bl[0]["passo"], "a": bl[-1]["passo"], "nascite": int(tot),
                    "per_classe": nat, "divisioni_per_classe": nat,
                    "schwinger_per_classe": [0, 0, 0],
                    "fraz_nascite": [(x / tot if tot else None) for x in nat],
                    "fraz_nodi": list(fraz_nodi),
                    "rapporto": [((x / tot) / f if tot and f else None)
                                 for x, f in zip(nat, fraz_nodi)]})
    return {"passi": passi, "passi_girati": passi if girati is None else girati,
            "stato": "fatto", "amp": amp, "finestra": 50,
            "blob_sim": "cf2a1ac8ff", "blob_atteso": "cf2a1ac8",
            "blob_strumento": "16dced88aa", "blob_tors_w8_lunga": "bc62bcaabb",
            "blob_copia": "abcdef1234", "ancore": ["a"] * 10,
            "in_configurazione_del_driver": True,
            "scena": {"r_regione": 4.096438, "R_CONN": 2.4, "u_bordo": 1.585875},
            "passi_dati": PP, "piene": {}, "dove_nascite": [], "dove_chi": [],
            "dove_sopra4pi": {"1000": {"n": 1, "n_nodi": 2, "per_classe": [0, 1, 1],
                                       "q_u": {"q050": 1.2},
                                       "q_rho_spin_rel": {"q050": 0.9}}},
            "finestre_dove": fin,
            "nascite_per_finestra": [{"da": 1 + 50 * i, "a": 50 + 50 * i,
                                      "divisioni": 10 + i, "schwinger": 2}
                                     for i in range(passi // 50)],
            "totali": {"contatori": {"nati_div_tot": div, "nati_sch_tot": sch,
                                     "cambi_chi_tors_tot": 7, "cambi_geom_tot": 7,
                                     "cambi_perc_chi_tot": 0}}}


def collaudo():
    esiti = []

    def prova(nome, ok, dett=""):
        esiti.append((nome, bool(ok), dett))
        print("  %-7s %-76s %s" % ("OK" if ok else "FALLITA", nome, dett))

    print("=" * 104)
    print("IL COLLAUDO DI _referto_mzd.py -- su `json` SINTETICI")
    print("=" * 104)
    prova("n4: ### `0.0` si stampa `0.0000`, NON `n/d`", n4(0.0) == "0.0000", n4(0.0))
    prova("n4: ### e `None` si stampa `n/d`, e i due NON coincidono",
          n4(None) == "n/d" and n4(0.0) != n4(None))
    v, n = spearman([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
    prova("spearman: ### due serie identiche danno 1, e torna una TUPLA",
          abs(v - 1.0) < 1e-12 and n == 5, "%.4f, n=%d" % (v, n))
    v, n = spearman([1, 2, 3], [1, 1, 1])
    prova("spearman: ### DEVE DIRE `None` -- una serie COSTANTE non ha correlazione, e NON "
          "e' zero", v is None, "%s" % v)
    # --- incompleto
    r, _e, g = genera(_finto(girati=430), _finto())
    prova("incompleto: ### NESSUN referto se un braccio non e' finito, e dice QUALE",
          r is None and bool(g) and "INCOMPLETO" in g[0], (g or [""])[0])
    r, _e, g = genera(None, _finto())
    prova("incompleto: ### e se un json MANCA, nessun referto", r is None and bool(g))
    # --- R
    r, e, g = genera(_finto(div=100), _finto(div=100))
    prova("R: ### con bracci uguali `R = 1` e la lettura e' <<DEL MODELLO>>",
          e["R"] == "DEL MODELLO" and not g)
    r, e, _g = genera(_finto(div=5, g1=1), _finto(div=100, g1=100))
    prova("R: ### DEVE FALLIRE -- con `R = 0.05` la lettura e' <<DIPENDE DAL 0.3>>",
          e["R"] == "DIPENDE DAL 0.3", "%s" % e["R"])
    # ### la prima versione metteva `g1=5` contro `g1=100`, cioe' `R_finestra = 0.05`:
    #   le due letture erano DAVVERO discordi, e ### **il generatore aveva ragione.**
    #   Per provare <<INTERMEDIA>> servono le DUE grandezze allo stesso rapporto.
    r, e, _g = genera(_finto(div=30, g1=30), _finto(div=100, g1=100))
    prova("R: ### e con `0.3` su ENTRAMBE le grandezze la lettura e' INTERMEDIA",
          e["R"] == "INTERMEDIA", "%s" % e["R"])
    r, e, _g = genera(_finto(div=5, g1=100), _finto(div=100, g1=100))
    t = NL.join(r)
    # ### e l'ancora del testo si legge DAL GENERATORE: la prima versione cercava
    #   *<<non si scelgono>>* e il testo dice *<<NON si sceglie>>*. ### **La mia frase,
    #   non la sua.**
    prova("R: ### DEVE ACCENDERSI -- due letture DISCORDI si DICONO e non si scelgono",
          e["R"] == "DISCORDI" and "SONO DISCORDI" in t and "NON si sceglie" in t,
          "%s" % e["R"])
    # --- il dipolo
    r, e, _g = genera(_finto(fase=10, dip=90, chi=lambda k: k % 7,
                             s4=lambda k: k % 7), _finto())
    prova("dipolo: ### con il 90 %% dal dipolo e correlazione alta -> CONFERMATA",
          e["dipolo `_AMP = 0`"] == "CONFERMATA", "%s" % e["dipolo `_AMP = 0`"])
    r, e, _g = genera(_finto(fase=90, dip=10), _finto())
    prova("dipolo: ### DEVE FALLIRE -- col 10 %% dal dipolo -> REFUTATA",
          e["dipolo `_AMP = 0`"] == "REFUTATA", "%s" % e["dipolo `_AMP = 0`"])
    r, e, _g = genera(_finto(fase=10, dip=90, chi=None, s4=None), _finto())
    prova("dipolo: ### DEVE ACCENDERSI -- frazione alta MA correlazione assente -> NON "
          "confermata (la <<E>>)",
          e["dipolo `_AMP = 0`"] == "INTERMEDIA", "%s" % e["dipolo `_AMP = 0`"])
    r, _e, _g = genera(_finto(fase=10, dip=5, esatto=900), _finto())
    t = NL.join(r)
    prova("dipolo: ### DEVE ACCENDERSI -- con la spinta ESATTA a pi piu' grande, dice che un "
          "REFUTATA sarebbe un ARTEFATTO DELLA SOGLIA",
          "ARTEFATTO DELLA SOGLIA" in t)
    r, _e, _g = genera(_finto(fase=10, dip=900, esatto=1), _finto())
    t = NL.join(r)
    prova("dipolo: ### DEVE TACERE -- se la spinta esatta e' piccola, NON parla di artefatto",
          "ARTEFATTO DELLA SOGLIA" not in t)
    # --- il dove
    r, e, _g = genera(_finto(nati_cl=[0, 10, 0]), _finto(nati_cl=[0, 10, 0]))
    prova("dove: ### DEVE ACCENDERSI -- col BORDO a 1/0.3 = 3.33x e' SOVRARAPPRESENTATO",
          e["dove `_AMP = 0`"] == "BORDO", "%s" % e["dove `_AMP = 0`"])
    t = NL.join(r)
    prova("dove: ### e dice che e' SUPERFICIE CHE CRESCE, cioe' geometria",
          "SUPERFICIE CHE CRESCE" in t)
    r, e, _g = genera(_finto(nati_cl=[10, 0, 0]), _finto(nati_cl=[10, 0, 0]))
    t = NL.join(r)
    prova("dove: ### con la MATERIA e' MATERIA CHE PROLIFERA",
          e["dove `_AMP = 0`"] == "MATERIA" and "MATERIA CHE PROLIFERA" in t)
    r, e, _g = genera(_finto(nati_cl=[1, 3, 6]), _finto(nati_cl=[1, 3, 6]))
    t = NL.join(r)
    prova("dove: ### DEVE TACERE -- se le nascite SEGUONO i nodi, NESSUNA e' "
          "sovrarappresentata",
          e["dove `_AMP = 0`"] == "NESSUNA" and "le nascite seguono i nodi" in t,
          "%s" % e["dove `_AMP = 0`"])
    # --- lo ZERO FALSO
    _nc = _finto(chi=lambda k: 5, s4=lambda k: 5)
    for _x in _nc["passi_dati"]:
        if _x["passo"] % 2 == 0:
            _x["chi_tors_non_confrontabile"] = 1
            _x["cambi_chi_tors"] = 0
    z = leggi_dipolo(_nc)
    prova("zero falso: ### i passi non confrontabili sono ESCLUSI dalla correlazione",
          z["corr_esclusi"] == 500 and z["corr_passi_buoni"] == 500,
          "esclusi %s su %s" % (z["corr_esclusi"], z["corr_passi_tot"]))
    prova("zero falso: ### e sui RESTANTI la correlazione si calcola davvero",
          z["corr_n"] == 500, "n = %s" % z["corr_n"])
    r, _e, _g = genera(_nc, _finto())
    t = NL.join(r)
    prova("zero falso: ### DEVE ACCENDERSI -- col 50 %% escluso il referto DICE che la serie "
          "e' BUCATA", "serie BUCATA" in t and "ZERO FALSO" in t)
    prova("zero falso: ### e la tabella riporta quanti passi sono stati esclusi",
          "passi ESCLUSI dalla correlazione" in t)
    r, _e, _g = genera(_finto(chi=lambda k: 5, s4=lambda k: 5), _finto())
    t = NL.join(r)
    prova("zero falso: ### DEVE TACERE -- senza passi esclusi NON parla di serie bucata",
          "serie BUCATA" not in t)
    # --- `trova`
    import tempfile as _tf
    global D
    _vero, _tmp = D, _tf.mkdtemp()
    try:
        D = _tmp
        io.open(os.path.join(_tmp, "amp0.json"), "w", encoding="utf-8").write(
            json.dumps({"amp": 0.0}))
        io.open(os.path.join(_tmp, "amp0_3.json"), "w", encoding="utf-8").write(
            json.dumps({"amp": 0.3}))
        prova("trova: ### il braccio ZERO sta in `amp0.json`, non in `amp0_0.json`",
              (trova(0.0) or {}).get("_file") == "amp0.json",
              "%s" % (trova(0.0) or {}).get("_file"))
        prova("trova: ### DEVE TACERE -- un'ampiezza che non c'e' torna `None`",
              trova(0.7) is None)
    finally:
        D = _vero
    # --- la forma
    r, _e, _g = genera(_finto(), _finto())
    t = NL.join(r)
    prova("forma: ### nessun segnaposto `" + chr(37) + "s` o `{}` nel testo",
          (chr(37) + "s") not in t and "{}" not in t)
    prova("forma: ### nessun doppio backtick", "``" not in t)
    prova("forma: ### DEVE FALLIRE SE TORNA -- nessun `None` stampato come fosse un numero",
          "`None`" not in t and "None PASSI" not in t)
    _sf = _finto()
    del _sf["finestra"]
    t2 = NL.join(genera(_sf, _sf)[0])
    prova("forma: ### e la larghezza della finestra si DERIVA dai dati, non da un campo",
          "FINESTRE DI `50` PASSI" in t2 and "`None`" not in t2)
    prova("forma: ### il referto dichiara il LIMITE di un seme solo e il gradino `(b)`",
          "un seme solo" in t and "`(b)`" in t)
    prova("forma: ### e dice che gli INDICI degli archi oltre 4pi NON si guardano",
          "MAI gli indici" in t)
    _a, _b = _finto(), _finto()
    _pa, _pb = copy.deepcopy(_a), copy.deepcopy(_b)
    genera(_a, _b)
    prova("forma: ### e `genera` NON modifica i json che riceve", _a == _pa and _b == _pb)
    print("=" * 104)
    ko = [n for n, o, _d in esiti if not o]
    print("COLLAUDO: %d su %d" % (len(esiti) - len(ko), len(esiti)))
    if ko:
        print("### FALLITI:")
        for n in ko:
            print("    - " + n)
    print("=" * 104)
    return 1 if ko else 0


def main(argv):
    if "--collaudo" in argv[1:]:
        return collaudo()
    zero, acceso = trova(0.0), trova(0.3)
    righe, esiti, guasti = genera(zero, acceso)
    if righe is None:
        for g in guasti:
            print("### %s" % g)
        print("### MI FERMO: un referto su una corsa incompleta sarebbe un numero senza "
              "provenienza.")
        return 1
    io.open(OUT, "w", encoding="utf-8", newline=NL).write(NL.join(righe) + NL)
    print("scritto %s  (%d righe)" % (OUT, len(righe)))
    for k in sorted(esiti):
        print("  %-22s %s" % (k, esiti[k]))
    print("  blob del referto: %s"
          % hashlib.sha1(io.open(OUT, "rb").read()).hexdigest()[:8])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
