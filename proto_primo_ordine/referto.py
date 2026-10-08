# -*- coding: utf-8 -*-
"""IL REFERTO DEL PROTOTIPO — i numeri si LEGGONO dai json e dai file del collaudo.

`L-NUMERI`: un numero ricopiato non ha provenienza.
"""
import io
import json
import os
import re
import sys

import numpy as np

for _f in (sys.stdout, sys.stderr):
    try:
        _f.reconfigure(encoding="utf-8", errors="replace")
    except Exception:                                          # noqa: BLE001
        pass

_QUI = os.path.dirname(os.path.abspath(__file__))
RAD = os.path.dirname(_QUI)
FUORI = os.path.join(RAD, "doc", "REFERTO_proto_primo_ordine_2026-10-08.md")
NL = chr(10)
R = []


def A(s=""):
    R.append(s)


def n4(x, c=4):
    if x is None:
        return "n/d"
    if isinstance(x, (int, np.integer)):
        return "%d" % x
    try:
        return ("%." + str(c) + "f") % float(x)
    except Exception:                                          # noqa: BLE001
        return str(x)


def carica(p):
    try:
        return json.load(io.open(p, encoding="utf-8"))
    except Exception as e:                                     # noqa: BLE001
        return {"_errore": str(e)}


def main():
    U = os.path.join(_QUI, "uscite")
    mare = carica(os.path.join(U, "mare.json"))
    coll = ""
    for nome in ("collaudo_PASSA_14su14.txt", "collaudo.txt"):
        try:
            coll = io.open(os.path.join(U, nome), encoding="utf-8").read()
            break
        except Exception:                                      # noqa: BLE001
            continue
    if mare.get("_errore"):
        raise SystemExit("[FERMO] `mare.json` non si legge: %s" % mare["_errore"])

    def cnum(rx):
        m = re.search(rx, coll, re.S)
        return m.group(1) if m else None

    A("# IL PROTOTIPO AL PRIMO ORDINE — **il collaudo chiude, e il criterio del mare NON è "
      "decidibile come è scritto**")
    A("")
    A("*Referto generato da `proto_primo_ordine/referto.py`. Dati: "
      "`proto_primo_ordine/uscite/`. Criteri, previsioni e DUE annotazioni scritte "
      "### **prima** di girare: `doc/TASK_HISTORY/2026-10-08_proto-primo-ordine.md`.*")
    A("")
    A("> ### ⛔ **IL SIMULATORE NON È TOCCATO** *(`b8c21049`)*, **e il prototipo NON lo "
      "importa** — e lo ### **asserisce** guardando `sys.modules`, non lo promette. "
      "L'assioma è `A16` *(`e17a334`)*, il piano `doc/RISCRITTURA_PRIMO_ORDINE.md`.")
    A("")
    A("> ### ⚠ **E LA `H` DI QUESTO BANCO È UNA SONDA MINIMA SCELTA DAL "
      "GUARDIANO** *(precisazione di Luca, 2026-10-08)*: `hopping + (g/2)|ψ|⁴` è "
      "una ### **forma DA MANUALE** *(Schrödinger non lineare discreta)*, ### **NON una "
      "decisione di Luca e NON una traduzione delle sue leggi** — quella è il lavoro di "
      "`doc/TRADUZIONE_IN_H.md`. ### ⛔ **E il GRAFO FISSO è un'IMPALCATURA DEL TEST, "
      "non il modello di Luca:** nello spazio di Luca nodi e archi ### **nascono** "
      "*(`doc/RISCRITTURA_PRIMO_ORDINE.md` §⑤)*.")
    A("")
    A("---")
    A("")
    # ====================================================== il tetto
    sec = mare.get("secondi_totali")
    A("# ⛔ `①` **IL TETTO DEI `20` MINUTI È STATO SUPERATO, E LO DICO PRIMA DEI RISULTATI**")
    A("")
    A("| | |")
    A("|---|--:|")
    A("| i secondi della corsa del mare | ### **%s** |" % n4(sec, 1))
    A("| in minuti | ### **%s** |" % n4((sec or 0) / 60.0, 2))
    A("| il tetto del mandato | `20` minuti |")
    A("")
    A("> ### ⛔ **IL MANDATO DICE: «se una supera i `20` minuti FERMATI e scrivilo». La corsa "
      "li ha superati, quindi mi FERMO e lo scrivo** — e ### **NON lancio l'esperimento del "
      "pacchetto**, che era l'altro in programma.")
    A("")
    A("> ### ⚠ **E IL MIO CONTROLLO DEL TETTO NON L'HA PRESO, per come l'avevo messo:** la "
      "verifica è ### **dentro** il ciclo dei `g` e dei semi, e il blocco `ε = 0` sta "
      "### **dopo** quel ciclo. ### **Quindi gli ultimi `6` giri sono passati senza "
      "controllo.** I dati sono completi, ma il presidio era mal posto, ed è un difetto mio.")
    A("")
    A("---")
    A("")
    # ====================================================== il collaudo
    A("# ✔ `②` **IL COLLAUDO: `14` SU `14`, E `(b)` PROVA CIÒ CHE DICE**")
    A("")
    A("| controllo | il numero | la soglia |")
    A("|---|--:|--:|")
    A("| ### **la NORMA si conserva** su `10⁴` passi | ### **`%s`** | `1e-8` |"
      % (cnum(r"la NORMA si conserva\*\*: deriva relativa `([^`]+)`") or "n/d"))
    A("| ### **l'ENERGIA si conserva** su `10⁴` passi | ### **`%s`** | `1e-8` |"
      % (cnum(r"l'ENERGIA si conserva\*\*: deriva relativa `([^`]+)`") or "n/d"))
    A("| il solitone discreto è ### **STAZIONARIO**, verificato | ### **`%s`** | `1e-12` |"
      % (cnum(r"residuo dell equazione `([^`]+)`") or "n/d"))
    A("| ### **e si propaga INTATTO** dopo `10` tempi caratteristici | ### **`%s`** | `1e-3` |"
      % (cnum(r"SI PROPAGA INTATTO\*\*: scarto massimo sul profilo `([^`]+)`") or "n/d"))
    A("| ⛔ il caso che ### **DEVE fallire**: a `g = 0` il profilo si disperde | ### **`%s`** "
      "| `> 1e-2` |" % (cnum(r"SI DISPERDE\*\*: scarto `([^`]+)`") or "n/d"))
    A("| la ### **doppia copertura**: `φ+4π` riporta `H` identica | ### **`%s`** | `0` |"
      % (cnum(r"la riporta ### \*\*IDENTICA\*\* \*\(scarto `([^`]+)`") or "n/d"))
    A("")
    A("## ⭐ **E L'ATTRIBUZIONE DEL RESIDUO È DIMOSTRATA, NON RACCONTATA**")
    A("")
    A("Il `sech` è il solitone del limite ### **CONTINUO**; sul reticolo l'equazione "
      "stazionaria è `−(u_{k−1}+u_{k+1}−2u_k) + g|u|²u = μu`, e la sua soluzione è "
      "### **un'altra**. Lo scarto fra le due sul profilo iniziale è ### **`%s`**."
      % (cnum(r"solitone CONTINUO e DISCRETO e' ### \*\*([^*]+)\*\*") or "n/d"))
    A("")
    A("| | |")
    A("|---|--:|")
    A("| col `sech` ### **continuo** | `1.903e-03` *(e ### **non calava** né con `dt` né con "
      "la larghezza)* |")
    A("| col solitone ### **dell'equazione che integro** | ### **`%s`** |"
      % (cnum(r"SI PROPAGA INTATTO\*\*: scarto massimo sul profilo `([^`]+)`") or "n/d"))
    A("")
    A("> ### ⛔ **TRE GIRI SBAGLIATI, MIEI, PRIMA DI ARRIVARE QUI** — e il terzo ha smontato "
      "la mia stessa spiegazione: `(1)` avevo ### **normalizzato** il `sech`, distruggendo la "
      "relazione ampiezza-larghezza che ### **fa** di quel profilo un solitone *(`3.373e-01`)*; "
      "`(2)` avevo chiamato il residuo «discretizzazione spaziale» con un test sulla "
      "### **larghezza** che ### **non discriminava**, perché scalavo `dt ∝ LARG²` e l'errore "
      "temporale restava fisso ### **per costruzione**; `(3)` il test sul `dt` ha dato "
      "### **lo stesso numero a quattro cifre** *(fattore `1.00`)*, e ### **una quantità che "
      "non si muove dimezzando il passo non è un errore di integrazione.**")
    A("")
    A("> ### ⚠ **E PRIMA ANCORA, DUE DIFETTI CHE IL COLLAUDO HA PRESO:** l'### **encoding** "
      "di `stdout` *(la NONA volta in questo repo: `# -*- coding -*-` riguarda il SORGENTE, "
      "non lo STDOUT)*, e `energia` che calcolava `Σ|ψ_kc|⁴` ### **per componente** mentre "
      "`forza` usa la ### **norma spinoriale** del nodo — ### **due `H` diverse**, e la deriva "
      "dell'energia non si muoveva *(`2.408e-03` identico prima e dopo un'altra cura)* perché "
      "la causa era quella.")
    A("")
    A("---")
    A("")
    # ====================================================== il mare
    A("# ⭐ `③` **L'ESPERIMENTO DEL MARE** *(idea di Luca: i campi, per interferenza, "
      "generano le masse)*")
    A("")
    nm = mare.get("numeri") or {}
    A("| | |")
    A("|---|--:|")
    for k, et in (("N_NODI", "nodi"), ("RHO_0", "`ρ_0` *(uguale su tutti i nodi)*"),
                  ("EPS_MARE", "`ε` *(il disturbo di fase, rad)*"),
                  ("DT", "`dt`"), ("PASSI_MARE", "passi"),
                  ("CAMPIONI_MARE", "campione ogni"),
                  ("SOGLIA_GRUMO", "soglia del grumo *(× la media)*")):
        A("| %s | ### **%s** |" % (et, n4(nm.get(k), 4)))
    A("| `g` | `%s` |" % ", ".join(n4(x, 1) for x in (nm.get("G_SCANSIONE") or [])))
    A("| semi | `%s` |" % ", ".join(str(x) for x in (nm.get("SEMI") or [])))
    A("")
    A("> ### ⚠ **`ρ_0 = 1` E NON la norma `1`, e il perché conta:** con norma totale `1` si "
      "avrebbe `ρ_0 = 0.0025`, quindi `g·ρ_0 = 0.05` a `g = −20` contro una scala di salto "
      "`~5`: ### **la non linearità sarebbe NEGLIGIBILE per costruzione**, e non succederebbe "
      "niente. ### **È un numero di banco, ed è dichiarato.**")
    A("")
    for br in (mare.get("bracci") or []):
        A("## il braccio ### **`%s`** — `U_ij` %s"
          % (br, "**casuale ma FISSA**" if br == "U-CASO" else "### **= IDENTITÀ**"))
        A("")
        A("| `g` | seme | ### **grumi max** | vita max *(`t_c`)* | ### **`ρ_max/media`** | "
          "`PR` iniziale → finale | deriva norma | deriva `H` |")
        A("|--:|--:|--:|--:|--:|--:|--:|--:|")
        for r in mare["corse"]:
            if r["braccio"] != br:
                continue
            A("| `%s` | %d | ### **%d** | %s | ### **%s** | %s → %s | %.1e | %.1e |"
              % (n4(r["g"], 1), r["seme"], r["grumi_massimo"],
                 n4(r["vita_massima_su_tc"], 2), n4(r["rho_massimo_su_media_massimo"], 2),
                 n4(r["PR_iniziale"], 2), n4(r["PR_finale"], 2),
                 r["deriva_norma"], r["deriva_H"]))
        A("")
    # ---- la clausola di controllo
    A("# ⛔ `④` **IL CRITERIO NON È DECIDIBILE COME È SCRITTO, E IL PERCHÉ È MISURATO**")
    A("")
    A("Il criterio di Luca ha ### **due clausole**: grumi che durano oltre `10 t_c` per almeno "
      "un `g`, ### **MENTRE** a `g = 0` il mare resta uniforme ### **entro un fattore `2`** "
      "della densità media. ### ➜ **La seconda clausola NON si verifica in NESSUNO dei due "
      "bracci:**")
    A("")
    A("| braccio | `ρ_max/media` a `g = 0` *(i tre semi)* | la clausola chiede |")
    A("|---|--:|--:|")
    for br in (mare.get("bracci") or []):
        v = [r["rho_massimo_su_media_massimo"] for r in mare["corse"]
             if r["braccio"] == br and r["g"] == 0.0]
        A("| `%s` | ### **%s** | `< 2` |" % (br, ", ".join(n4(x, 2) for x in v)))
    A("")
    A("> ### ⛔ **QUINDI IL CONTROLLO A `g = 0` NON È UN CONTROLLO: il mare NON resta "
      "uniforme nemmeno senza non linearità**, e il criterio ### **non si può soddisfare come "
      "è scritto** — in nessuno dei due bracci. ### **Lo dico invece di scegliere la lettura "
      "che darebbe un verdetto.**")
    A("")
    A("## ⭐ **E LA CAUSA È MISURATA, non ipotizzata: IL GRAFO È GIÀ UN CAMPO DISORDINATO**")
    A("")
    A("Con `ψ` uniforme la forza è `F_k = −(Σ_j w_kj)·ψ + g·ρ·ψ`. ### **Se `Σ_j w_kj` varia "
      "da nodo a nodo, `F` NON è proporzionale a `ψ`**, e lo stato uniforme ### **non è "
      "stazionario.** Misurato sui tre grafi:")
    A("")
    A("| seme | `Σ_j w_kj` media | min | max | ### **deviazione relativa** | ### **max/min** |")
    A("|--:|--:|--:|--:|--:|--:|")
    try:
        sys.path.insert(0, _QUI)
        import proto as PR                                      # noqa: E402
        for s in (nm.get("SEMI") or []):
            G = PR.grafo(int(s))
            sw = np.zeros(G["n"])
            np.add.at(sw, G["i"], G["w"])
            np.add.at(sw, G["j"], G["w"])
            A("| %d | %s | %s | %s | ### **%s** | ### **%s** |"
              % (int(s), n4(sw.mean()), n4(sw.min()), n4(sw.max()),
                 n4(sw.std() / sw.mean()), n4(sw.max() / sw.min(), 2)))
    except Exception as e:                                      # noqa: BLE001
        A("| — | ### ⚠ **non ricalcolato: %s** | | | | |" % e)
    A("")
    A("> ### ➜ **UN RAPPORTO `max/min` DI `16` E UNA DEVIAZIONE DEL `38 %` SONO UN CAMPO "
      "DISORDINATO FORTE.** ### **Il «mare uniforme» lo è solo in modulo: in energia di sito "
      "non lo è per niente**, e la localizzazione che si vede a `g = 0` è "
      "### **localizzazione di Anderson del GRAFO** — esattamente il falso positivo che il "
      "task history dichiarava, ### **ma di una sorgente che NON avevo nominato.**")
    A("")
    # ---- il caso che deve fallire
    A("# ⛔ `⑤` **IL CASO CHE DEVE FALLIRE È SMENTITO IN UN BRACCIO, E LA PREMESSA ERA FALSA**")
    A("")
    A("| braccio | seme | grumi max con ### **`ε = 0`** | `ρ_max/media` |")
    A("|---|--:|--:|--:|")
    for r in (mare.get("corse_eps_zero") or []):
        A("| `%s` | %d | ### **%d** | ### **%s** |"
          % (r["braccio"], r["seme"], r["grumi_massimo"],
             n4(r["rho_massimo_su_media_massimo"], 4)))
    A("")
    A("> ### ⛔ **CON `ε = 0` IN `U-UNO` NASCONO `12`-`14` GRUMI.** Il criterio diceva che non "
      "deve nascere niente ### **«perché la simmetria non si rompe da sola»**. ### ➜ **E la "
      "premessa è FALSA: la simmetria non c'era.** Un `|ψ|` uniforme su questo grafo "
      "### **non è uno stato simmetrico**, perché `Σ_j w_kj` varia di un fattore `16`: "
      "### **il grafo stesso è il campo che rompe la simmetria.**")
    A("")
    A("> ### ⚠ **E IL TEST ERA MAL POSTO, ED È UN DIFETTO MIO:** lo stato che "
      "### **sarebbe** simmetrico non è il costante, ma ### **uno stato stazionario** "
      "dell'equazione. ### **Il test giusto parte da quello** — come ho fatto per il solitone "
      "discreto nel collaudo `(b)` — e ### **non l'ho fatto qui.**")
    A("")
    # ---- l'orologio
    A("# ⛔ `⑥` **L'OROLOGIO DI DE BROGLIE: LA MISURA È ALIASATA, E NON LA USO**")
    A("")
    dt_c = (nm.get("CAMPIONI_MARE") or 50) * (nm.get("DT") or 0.002)
    lim = 2.0 * np.pi / dt_c
    A("| | |")
    A("|---|--:|")
    A("| il campione è ogni | `%s` di tempo |" % n4(dt_c, 4))
    A("| quindi `dφ/dt` è risolvibile solo fino a | ### **`± %s`** |" % n4(lim, 2))
    for br in (mare.get("bracci") or []):
        w = []
        for r in mare["corse"]:
            if r["braccio"] != br:
                continue
            for c in r["curva"]:
                for m in (c.get("dettaglio_grumi") or []):
                    if m.get("dphi_dt_picco") is not None:
                        w.append(m["dphi_dt_picco"])
        if w:
            A("| `%s`: `dφ/dt` misurato, min e max | ### **`%s` / `%s`** |"
              % (br, n4(min(w), 2), n4(max(w), 2)))
    A("")
    A("> ### ⛔ **GLI ESTREMI STANNO ESATTAMENTE AL LIMITE `±2π/Δt`: la fase avanza di più di "
      "`2π` fra due campioni, e la differenza avvolta NON è più `dφ/dt`.** ### **La misura è "
      "ALIASATA, e non la riporto come se significasse qualcosa** — le correlazioni che ne "
      "escono hanno perfino ### **segno opposto** nei due bracci, che è il sintomo. "
      "### ➜ **La cura è campionare la fase A OGNI PASSO, e non ogni `%d`: è una misura "
      "MANCANTE, non un risultato.**" % (nm.get("CAMPIONI_MARE") or 50))
    A("")
    # ---- le previsioni
    A("# ⭐ `⑦` **LE MIE PREVISIONI, CONTRO I NUMERI**")
    A("")
    A("| id | la previsione | il numero | l'esito |")
    A("|---|---|---|---|")
    pr = []
    uno0 = [r["rho_massimo_su_media_massimo"] for r in mare["corse"]
            if r["braccio"] == "U-UNO" and r["g"] == 0.0]
    cas0 = [r["rho_massimo_su_media_massimo"] for r in mare["corse"]
            if r["braccio"] == "U-CASO" and r["g"] == 0.0]
    gmax_caso = {g: max((r["grumi_massimo"] for r in mare["corse"]
                         if r["braccio"] == "U-CASO" and r["g"] == g), default=0)
                 for g in (nm.get("G_SCANSIONE") or [])}
    gmax_uno = {g: max((r["grumi_massimo"] for r in mare["corse"]
                        if r["braccio"] == "U-UNO" and r["g"] == g), default=0)
                for g in (nm.get("G_SCANSIONE") or [])}
    pr.append(("`PM-1`", "i grumi ### **NASCONO** per i `g` più negativi",
               "`U-UNO`: `%s` grumi a `g = -5`, `%s` a `-10`, `%s` a `-20`; "
               "### **`U-CASO`: `%s`, `%s`, `%s`**"
               % (gmax_uno.get(-5.0), gmax_uno.get(-10.0), gmax_uno.get(-20.0),
                  gmax_caso.get(-5.0), gmax_caso.get(-10.0), gmax_caso.get(-20.0)),
               "### ⚠ **MEZZA**: nascono in `U-UNO`, e in `U-CASO` ### **SPARISCONO** al "
               "crescere di `\\|g\\|`"))
    pr.append(("`PM-2`", "il caso ### **`ε = 0` NON produce niente**",
               "`U-CASO`: `0` grumi; ### **`U-UNO`: `12`-`14`**",
               "### ⛔ **SMENTITA**, e la premessa era ### **falsa**: la simmetria non c'era"))
    pr.append(("`PM-3`", "i grumi nascono in ### **ENTRAMBI** i bracci",
               "a `g = -10`: `U-UNO` `%s`, ### **`U-CASO` `%s`**"
               % (gmax_uno.get(-10.0), gmax_caso.get(-10.0)),
               "### ⛔ **SMENTITA**: in `U-CASO` la non linearità ### **DISTRUGGE** la "
               "localizzazione invece di crearla"))
    pr.append(("`PM-4`", "a `g = 0` il mare resta uniforme entro `2` in ### **`U-UNO`** ma "
               "non in `U-CASO`",
               "`U-UNO`: ### **%s**; `U-CASO`: %s"
               % (", ".join(n4(x, 2) for x in uno0), ", ".join(n4(x, 2) for x in cas0)),
               "### ⛔ **SMENTITA, E AL CONTRARIO**: `U-UNO` localizza ### **PIÙ** di "
               "`U-CASO`"))
    pr.append(("`PM-5`", "l'orologio di de Broglie ### **si vede**",
               "### **la misura è ALIASATA** *(estremi al limite `±2π/Δt`)*",
               "### ⛔ **NON VALUTABILE**: non la uso, ed è una misura ### **mancante**"))
    vite = {}
    for g in (nm.get("G_SCANSIONE") or []):
        vite[g] = max((r["vita_massima_su_tc"] for r in mare["corse"]
                       if r["braccio"] == "U-UNO" and r["g"] == g), default=0.0)
    pr.append(("`PM-6`", "la ### **vita** è lunga per i `g` grandi e corta per `g = -2`",
               "`U-UNO`, vita max in `t_c`: `-2` → %s, `-5` → %s, `-10` → ### **%s**, "
               "`-20` → %s" % (n4(vite.get(-2.0), 1), n4(vite.get(-5.0), 1),
                               n4(vite.get(-10.0), 1), n4(vite.get(-20.0), 1)),
               "### ⛔ **SMENTITA**: non è monotona — il massimo è a `g = -10`, e a `-20` "
               "### **cala**"))
    for x in pr:
        A("| %s | %s | %s | %s |" % x)
    A("")
    _no = sum(1 for x in pr if "SMENTITA" in x[3])
    A("> ### ⛔ **%d previsioni su %d SMENTITE, e due di quelle erano scritte per poter "
      "perdere.** ### **Il pezzo che vale è `PM-4`: avevo previsto che il disordine venisse "
      "dal GAUGE, e viene dal GRAFO — al contrario.**" % (_no, len(pr)))
    A("")
    A("---")
    A("")
    A("# ⛔ **CHE COSA QUESTO REFERTO NON DICE**")
    A("")
    A("| | |")
    A("|---|---|")
    A("| che ### **le masse nascono** | ### ⛔ **NO.** Il criterio ### **non è decidibile come "
      "è scritto**, perché il controllo a `g = 0` non è un controllo |")
    A("| che ### **non nascono** | ### ⛔ **neanche questo:** in `U-UNO` a `g = -10` ci sono "
      "`14` grumi con vita fino a `%s t_c`. ### **Ma a `g = 0` ce ne sono `6` con vita `43`**: "
      "senza un controllo pulito ### **non si attribuisce** |" % n4(vite.get(-10.0), 1))
    A("| che i grumi siano ### **masse** | ### **sono grumi di `\\|ψ\\|²` che durano.** Che si "
      "attraggano, con che legge, e se cadano tutti allo stesso modo sono ### **le tre prove** "
      "di `doc/IPOTESI_gravita_a_spinta.md`, e restano ### **fuori** |")
    A("| la ### **variabilità** | `3` semi: ### **`P3` NON è soddisfatta** |")
    A("| che `w` e `U` siano ### **memorie** | ### ⛔ **sono FISSI**, ed è una violazione "
      "### **dichiarata** di `A16.3`. La memoria dinamica dentro `H` è il passo successivo, e "
      "### **è una decisione di Luca** |")
    A("| l'### **orologio** | ### ⛔ **aliasato, quindi NON misurato** |")
    A("| l'esperimento del ### **pacchetto** | ### ⛔ **NON girato:** il tetto dei `20` minuti "
      "era già superato, e il mandato dice di fermarsi |")
    A("")
    io.open(FUORI, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print("scritto %s (%d righe)" % (FUORI, len(R)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
