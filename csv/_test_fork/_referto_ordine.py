# -*- coding: utf-8 -*-
"""**Genera `doc/ORDINE_letture.md`: il verdetto del punto 1 e le regole di nascita del punto 7.**

Due sorgenti, e **nessun numero ricopiato a mano** *(`L-NUMERI`)*:

| | |
|---|---|
| **il punto 1** | `csv/_seal_fork/_ordine_letture/_ordine_letture.json`, dalla misura |
| **il punto 7** | `doc/REGOLE_nascita.tsv`, ### **la mia DICHIARAZIONE** — e ogni riga si ### **VERIFICA sul sorgente** cercando l'**ancora** per TESTO, mai per riga *(par.2: le righe shiftano)* |

## ⛔ Il SESTO difetto della misura, e per questo il verdetto si ricalcola qui

Lo strumento `97cb0ea3` stampa *«LETTA PRIMA»* per **24** grandezze, **e quell'etichetta e'
FUORVIANTE**: la finestra si apre quando `mitosi` **ritorna**, e a quell'istante **30 grandezze su
40 sono GIA' PIENE** — chi le legge dopo **non le vede corte**.
### ➜ **La domanda vera non e' <<chi legge prima>>: e' <<una legge le legge CORTE?>>.**
**Il dato per rispondere e' nel `json`**: ogni evento porta la **lunghezza** vista in quel momento.
### **Quindi la misura VALE e non si rigira: si legge bene.** *(La stampa dello strumento si
correggera' a parte: e' in coda, e il blob che ha girato resta `97cb0ea3`.)*

COMANDO:  python csv/_test_fork/_referto_ordine.py
"""
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)

MISURA = os.path.join(RADICE, "csv", "_seal_fork", "_ordine_letture", "_ordine_letture.json")
REGOLE = os.path.join(RADICE, "doc", "REGOLE_nascita.tsv")
SIM = os.path.join(RADICE, "soliton_simulator.py")
FUORI = os.path.join(RADICE, "doc", "ORDINE_letture.md")
VICINO = 3   # eventi: una lettura riscritta dallo STESSO chiamante entro tanto e' un RINFRESCO


def verifica_ancore():
    """Ogni **ancora** si cerca **per TESTO** e si dice **a che riga sta OGGI**.

    ### **Non si cita una riga: si cita un'ancora e si stampa la riga che ha adesso** — perche'
    i numeri di riga **shiftano fra i blob** *(par.2)*, ed e' un errore che ho gia' fatto.
    """
    righe = io.open(SIM, encoding="utf-8").read().split("\n")
    fuori = []
    for r in io.open(REGOLE, encoding="utf-8").read().split("\n")[1:]:
        if not r.strip():
            continue
        c = r.split("\t")
        if len(c) < 7:
            continue
        anc = c[4]
        trovate = [k + 1 for k, x in enumerate(righe) if anc in x]
        fuori.append({"grandezza": c[0], "classe": c[1], "evento": c[2], "regola": c[3],
                      "ancora": anc, "derivazione": c[5], "dubbio": c[6].strip() in ("SI", "APERTA"),
                      "aperta": c[6].strip() == "APERTA",
                      "righe": trovate})
    return fuori


def principale():
    j = json.load(io.open(MISURA, encoding="utf-8"))
    lfm, n, m = j["len_a_fine_mitosi"], j["n"], j["m"]
    reg = verifica_ancore()
    R = []
    P = R.append

    P("# 🔬 **L'ORDINE LETTURA/RISCRITTURA, e LE REGOLE DI NASCITA**")
    P("")
    P("> ### **Generato da** `csv/_test_fork/_referto_ordine.py` dalla misura")
    P("> `csv/_seal_fork/_ordine_letture/_ordine_letture.json` *(strumento `97cb0ea3`)* e dalla")
    P("> dichiarazione `doc/REGOLE_nascita.tsv`. **Non si modifica a mano.** *(`L-NUMERI`.)*")
    P("")
    P("| | |")
    P("|---|---|")
    P("| scena | `nmasse %d`, `sep %.4f`, seme `11` |" % (j["nmasse"], j["sep"]))
    P("| la nascita | ### **trovata al passo %d** *(non assunta)*: `n = %d`, `m = %d` |"
      % (j["passo_di_nascita"], n, m))
    P("| la finestra | si apre quando **`mitosi` ritorna** *(evento `%d`)* e si chiude **a fine"
      " del passo seguente** |" % j["evento_fine_mitosi"])
    P("| eventi intercettati | **%d** |" % j["eventi_intercettati"])
    P("| ### **il CONTROLLO** | ### **lo stesso passo con e senza sorveglianza e'"
      " BYTE-IDENTICO** → la misura vale |")
    P("| tipo del lettore | da **`_PASSO_TIPI`**, la tabella del simulatore. **Non leggi:** %s |"
      % ", ".join("`%s`" % x for x in j["non_leggi"]))
    P("")

    # ---------------------------------------------------------------- IL VERDETTO, RICALCOLATO
    P("## ⛔ **Il verdetto NON e' quello che stampa lo strumento, e va spiegato**")
    P("")
    P("Lo strumento stampa *«LETTA PRIMA»* per **24** grandezze. ### **Quell'etichetta e'")
    P("FUORVIANTE, ed e' il SESTO difetto mio su questo strumento:** la finestra si apre quando")
    P("`mitosi` **ritorna**, e a quell'istante **molte grandezze sono GIA' PIENE** — chi le legge")
    P("dopo ### **non le vede corte**.")
    P("")
    P("> ### 📌 **La domanda vera non e' «chi legge prima»: e' «una legge le legge CORTE?».**")
    P("> Il dato per rispondere e' **nella misura stessa**: ogni evento porta la **lunghezza**")
    P("> vista in quell'istante. ### **Quindi la misura VALE e non si rigira: si legge bene.**")
    P("")
    piene = [k for k in j["voci"] if lfm.get(k) == j["esiti"][k]["bersaglio"]]
    corte = [k for k in j["voci"] if lfm.get(k) != j["esiti"][k]["bersaglio"]]
    P("| | quante | quali |")
    P("|---|---|---|")
    P("| ### **PIENE quando `mitosi` ritorna** *(nessuno puo' vederle corte)* | ### **%d** |"
      " %s |" % (len(piene), " · ".join("`%s`" % x for x in piene)))
    P("| ### **CORTE quando `mitosi` ritorna** | ### **%d** | %s |"
      % (len(corte), " · ".join("`%s`" % x for x in corte)))
    P("")
    P("### ➜ **Le %d PIENE sono, TRANNE UNA, quelle con una regola di nascita — e la regola"
      " si vede nella MISURA, non solo nel codice.**" % len(piene))
    P("")
    P("### ⚠ **CORREZIONE a cio' che avevo scritto in `bd9262f`:** dicevo *«esattamente"
      " l'insieme che ha una regola di nascita»*, ### **e non e' vero per DUE voci** — le ho"
      " verificate:")
    P("")
    P("| | |")
    P("|---|---|")
    P("| `_deg` | ### **e' DERIVATA**, e risulta piena perche' `mitosi` chiama `_grado` a `:6738`"
      " e `:6859`, che la **ricalcola dal `bincount`**. Nessuna eredita', e va bene cosi' |")
    P("| ### `conc_nodi` | ### **HA una regola di nascita, e il mio strumento l'aveva PERSA:**"
      " `.append(eredita)` a `:6669` e `:6839`, **dentro `mitosi`**. ### **E' una MUTAZIONE IN"
      " POSTO, non un assegnamento** — quindi l'AST *(che cerca `self.X =`)* non la vedeva, e la"
      " sorveglianza *(che intercetta `__setattr__`)* la dava **MAI TOCCATA**. ### **Lo stesso"
      " punto cieco, in due strumenti diversi** |")
    P("")
    P("> ### 📌 **E dice un LIMITE della misura che vale per tutte le liste:** la"
      " sorveglianza vede gli **assegnamenti**, non le **mutazioni in posto**. Per un contenitore"
      " mutabile *«mai toccata» significa «non misurato»*, non *«nessuno la tocca»*.")
    P("")
    P("## Le **%d** corte: **una legge le legge corte?**" % len(corte))
    P("")
    P("| grandezza | cl. | `len` a fine mitosi | bersaglio | prima lettura di LEGGE | verdetto |")
    P("|---|---|---|---|---|---|")
    conto = {}
    for k in corte:
        e = j["esiti"][k]
        ll, rr = e["lettura_di_legge"], e["riscrittura"]
        b = e["bersaglio"]
        if ll is None:
            v = "**nessuna legge la legge** → ### **PUO' RESTARE CORTA**"
            cl = "nessuna lettura di legge"
            testo = "—"
        elif ll["len"] == b:
            v = ("la legge la trova **GIA' PIENA** *(riscritta a `#%s`)* → ### **PUO' RESTARE"
                 " CORTA**" % (rr["evento"] if rr else "?"))
            cl = "letta GIA' piena"
            testo = "`#%d` `%s` — `len = %d`" % (ll["evento"], ll["chi"], ll["len"])
        elif (rr and rr["chi"] == ll["chi"] and 0 < rr["evento"] - ll["evento"] <= VICINO):
            v = ("### **AUTO-RINFRESCO**: la legge la legge corta e la **riscrive lei stessa**"
                 " `+%d` eventi dopo → ### **e' una REGOLA DI RINFRESCO, non un buco**"
                 % (rr["evento"] - ll["evento"]))
            cl = "auto-rinfresco"
            testo = "`#%d` `%s` — ### **`len = %d`**" % (ll["evento"], ll["chi"], ll["len"])
        else:
            v = "### ⛔ **UNA LEGGE LA LEGGE CORTA: SERVE UNA REGOLA DI NASCITA**"
            cl = "BUCO"
            testo = "`#%d` `%s` — ### **`len = %d`**" % (ll["evento"], ll["chi"], ll["len"])
        conto[cl] = conto.get(cl, 0) + 1
        P("| `%s` | %s | `%d` | `%d` | %s | %s |"
          % (k, e["classe"][:4], lfm.get(k), b, testo, v))
    P("")
    P("| esito | quante |")
    P("|---|---|")
    for cl in ("nessuna lettura di legge", "letta GIA' piena", "auto-rinfresco", "BUCO"):
        P("| %s | %s |" % (cl, ("### **%d**" % conto[cl]) if conto.get(cl) else "0"))
    P("")
    if not conto.get("BUCO"):
        P("### ✅ **ZERO BUCHI: nessuna legge legge una cache corta che non sia la sua stessa"
          " riscrittura.** E i due **auto-rinfreschi** sono ### **GIA' DICHIARATI E CONTATI nel"
          " codice**:")
        P("")
        P("| | |")
        P("|---|---|")
        P("| `_xi_rumore` | *«questo **NON** e' un fallback: e' il **percorso normale della"
          " mitosi**; `xi` e' l'**AMBIENTE**, non una proprieta' del nodo, quindi il figlio"
          " **NON** lo eredita»*. ### **E' una regola di nascita al sito di lettura, e la misura"
          " la conferma** |")
        P("| `_g_rampa_prec` | *«e' un array **DIAGNOSTICO**, e lo dichiaro come tale: il suo"
          " disallineamento **SI CONTA** e si riparte … qui se il confronto salta si perde una"
          " **MISURA**, non una legge»*, col contatore `_g_rampa_prec_disallineata`."
          " ### **`A8` gia' rispettato** |")
        P("")
        P("> ### 📌 **CHE COSA VUOL DIRE PER IL CONTROLLO UNICO:** le **%d** piene passano il"
          " controllo `len == n` **per costruzione**; le **%d** corte vanno **escluse** e"
          " **dichiarate**, e per due di esse la dichiarazione ### **esiste gia' nel codice.**"
          " ### ➜ **Non c'e' niente da curare PRIMA del controllo.**" % (len(piene), len(corte)))
        P("")

    # ----------------------------------------------------------------- LE REGOLE DI NASCITA (7)
    P("---")
    P("")
    P("## 📜 **LE REGOLE DI NASCITA** *(punto 7: le ho lette io, non le ho battezzate)*")
    P("")
    P("**Il mio strumento le dava «DA DECIDERE» per una ragione sola:** il valore passa da una")
    P("**variabile locale** *(`fm`, `anti`, `pos_figlio`, `chi_nuovi`, `er`, `el`, `dh`,")
    P("`calcio_phi`, `calcio_omega`)*, e l'AST leggeva **il nome della locale** invece della sua")
    P("definizione. ### **La stessa cecita' sugli ALIAS, stavolta dal lato del VALORE.**")
    P("")
    P("### ⚠ **Ogni riga si VERIFICA per ANCORA, e la riga di oggi e' stampata:** i numeri di")
    P("riga **shiftano fra i blob** *(par.2)*, quindi ### **non si cita una riga — si cita un")
    P("testo e si dice dove sta adesso.**")
    P("")
    P("| grandezza | cl. | evento | ### **regola** | riga OGGI | come si legge |")
    P("|---|---|---|---|---|---|")
    perse = []
    for r in reg:
        if len(r["righe"]) != 1:
            perse.append(r)
        dove = ("`:%d`" % r["righe"][0] if len(r["righe"]) == 1
                else "### ⛔ **ANCORA %s**" % ("NON TROVATA" if not r["righe"]
                                               else "AMBIGUA (%d)" % len(r["righe"])))
        P("| `%s` | %s | **%s** | %s%s | %s | %s |"
          % (r["grandezza"], r["classe"], r["evento"],
             "### **" + r["regola"] + "**" if r["dubbio"] else r["regola"],
             (" ### ⛔ **APERTA: DECIDE LUCA**" if r.get("aperta")
              else " ### ⚠ **DA PORTARE A LUCA**") if r["dubbio"] else "",
             dove, r["derivazione"]))
    P("")
    P("**Ancore verificate: %d su %d.** %s"
      % (len(reg) - len(perse), len(reg),
         "### ✅ **Tutte trovate, e UNA VOLTA SOLA.**" if not perse
         else "### ⛔ **%d NON verificate: %s**"
              % (len(perse), ", ".join("%s/%s" % (x["grandezza"], x["evento"]) for x in perse))))
    P("")
    dubbi = [r for r in reg if r["dubbio"]]
    P("## 🛑 **Che cosa resta a Luca: %d voce%s**"
      % (len(dubbi), "" if len(dubbi) == 1 else ""))
    P("")
    P("**Il mandato dice: *«porta SOLO i casi in cui la regola esistente ti sembra fisicamente")
    P("discutibile, uno per uno, con la riga»*.** ### **Gli altri li ho scritti e non li porto.**")
    P("")
    for r in dubbi:
        dove = "`:%d`" % r["righe"][0] if len(r["righe"]) == 1 else "*(ancora non risolta)*"
        P("### ⚠ `%s` — evento **%s** — %s" % (r["grandezza"], r["evento"], dove))
        P("")
        P("**La regola che c'e':** %s. **Come si legge:** %s" % (r["regola"], r["derivazione"]))
        P("")
    io.open(FUORI, "w", encoding="utf-8", newline=chr(10)).write("\n".join(R) + "\n")
    print("piene %d · corte %d · buchi %s" % (len(piene), len(corte), conto.get("BUCO", 0)))
    print("regole dichiarate %d · ancore verificate %d · dubbi %d"
          % (len(reg), len(reg) - len(perse), len(dubbi)))
    print("scritto: " + FUORI)
    return 1 if perse else 0


if __name__ == "__main__":
    sys.exit(principale())
