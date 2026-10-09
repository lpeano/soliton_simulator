# -*- coding: utf-8 -*-
"""LA CHIUSURA DEI SEGNALI DEI PRESIDI — **un punto per volta.**

| punto | che cosa |
|---|---|
| `1` | `F1` piu' stretto *(**la formulazione era mia**: citare un assioma non e' essere gemelle)*, `C5` **omonimo**, `Z100` e `C5-INVARIANTI` con l'eccezione |
| `2` | ### **la classe `CRITERIO` e' una cosa sola:** un criterio **dice come si giudica** ⇒ `METODO`. Gli **esiti misurati** ⇒ `MISURA`/`FISICA` |
| `3` | gli `8` di `F2` con l'eccezione **che cita il «sostituisce»**; `ENERGIA-NON-DEFINITA` ### **solo la nota** |
| `4` | `F3`: le cure chiuse col sigillo con l'eccezione, gli altri **letti per intero** |

Gira con:  python csv/_segnali_chiusura.py <1|2|3|4>
"""
import io
import json
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Costruisce lotti per l'indice.
NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
LOTTI = os.path.join(D, "_lotti")
DATA = "2026-10-09"


def carica():
    return [json.loads(r) for r in io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8")
            if r.strip()]


def testo(v):
    return " ".join([v.get("titolo") or "", v.get("descrizione") or "",
                     v.get("fonte") or ""])


def pezzo(v, n=44):
    """### Un pezzo LETTERALE del testo della voce: l'eccezione deve CITARE, e `valida` lo
    pretende *(almeno `20` caratteri)*."""
    t = " ".join(testo(v).split())
    return t[:n]


def scrivi(nome, lotto):
    os.makedirs(LOTTI, exist_ok=True)
    p = os.path.join(LOTTI, nome)
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in lotto) + NL)
    print("  scritto %s: %d voci" % (os.path.relpath(p, RADICE).replace(chr(92), "/"),
                                     len(lotto)))


# ==========================================================================
#   PUNTO 1
# ==========================================================================
# ### I DUE SIGNIFICATI DI `C5`, letti dai testi -- non supposti.
C5_DUE = [("doc/RAMIFICAZIONI.md -- la VOCE `C5`, una MISURA: <<tauluce = d/cs e' PIATTO "
           "=> la sostituzione rompe la...>>"),
          ("doc/STATO_RUN.md e doc/RAMIFICAZIONI.md -- il <<mandato C5>>, cioe' GLI "
           "INVARIANTI: <<INVARIANTI (C5): il programma si ferma quando una grandezza "
           "esce...>>")]


def punto1():
    voci = carica()
    per = {v["id"]: v for v in voci}
    lotto = [{"id": "C5", "quando": DATA, "campi": {},
              "meta": {"omonimo": C5_DUE,
                       "nota_guardiano": "OMONIMO: <<C5>> nomina DUE OGGETTI DIVERSI -- la "
                                         "MISURA su tauluce e il MANDATO degli invarianti. "
                                         "NON si scegli: la scelta e' di Luca"},
              "motivo": ("(1) OMONIMO, e il guardiano l'ha visto leggendo F1: il titolo di "
                         "questa voce dice <<%s>>, cioe' una MISURA su tauluce, mentre Z100 "
                         "e C5-INVARIANTI citano il <<mandato C5>>, che e' GLI INVARIANTI. "
                         "Due oggetti, lo stesso ID" % pezzo(per["C5"], 70))}]
    for i in ("Z100", "C5-INVARIANTI"):
        v = per[i]
        lotto.append({"id": i, "quando": DATA, "campi": {},
                      "meta": {"eccezione_presidio":
                               ["F1: il titolo dice <<%s>> -- il `C5` che cita e' IL MANDATO "
                                "DEGLI INVARIANTI, non la voce `C5` (la misura su tauluce). "
                                "E' un OMONIMO, dichiarato in meta.omonimo di `C5`, non una "
                                "mescolanza di dominio" % pezzo(v, 60)]},
                      "motivo": ("(1) SEGNALE CHIUSO CON ECCEZIONE: F1 segnalava perche' il "
                                 "titolo <<%s>> cita `C5`, ma quel `C5` e' IL MANDATO DEGLI "
                                 "INVARIANTI, un OMONIMO della voce `C5`" % pezzo(v, 60))})
    scrivi("v3_p1.jsonl", lotto)
    print()
    print("  ### I SEGNALI DI `F1` CHE RESTANO, e il mandato chiede di ELENCARLI:")
    sys.path.insert(0, _QUI)
    import indice as IX
    for i, m in IX._f1_gemelle(voci):
        v = per[i]
        print("      %-22s %-10s %-14s %-8s %-8s %s"
              % (i, v["classe"], v["dominio"], v["era"], v["stato"],
                 re.sub(r"il titolo cita ", "cita ", m)[:62]))


# ==========================================================================
#   PUNTO 2  --  la classe CRITERIO e' UNA COSA SOLA
# ==========================================================================
# ### ⛔ **UN CRITERIO PRESCRIVE**, e si riconosce dal verbo o dalla formula del giudizio.
PRESCRIVE = ("deve", "devono", "si verifica", "basta", "serve", "byte-identico",
             "byte identico", "controllo positivo", "caso che deve fallire", "criterio",
             "si misura", "si confronta", "non deve", "va verificato", "si pretende",
             "soglia", "firma dei byte", "DEVE")
# ### **UN ESITO riporta una MISURA come risultato.**
# ### `==` NON E- UNA MISURA: e- un CONFRONTO, e la prima stesura lo contava.
# ### `REGISTRO_FISICA:S3` (<<sum(d < LAM) == 0 E sum(d == LAM) == 0>>) e
# ### `REGISTRO_FISICA:S5` (<<nodi isolati == 0>>) finivano fra i candidati a ESITO,
# ### ### **e sono due CONTROLLI.** Il `=` singolo resta, perche- <<il fattore = 1>> e-
# ### una misura -- ma ### **due voci passano comunque solo per la lettura**, e stanno
# ### in `DECISO_CRITERIO`.
MISURATO = re.compile(r"\d+[.,]\d+|\d+\s*%|(?<!=)=(?!=)\s*-?\d")


# ==========================================================================
#   LA DECISIONE DEL PUNTO 2, LETTA VOCE PER VOCE
# ==========================================================================
# ### ⛔ **La regola SELEZIONA, la lettura DECIDE**, e sta nel task history *prima*.
# ### Queste due tabelle sono ### **la decisione**, e ciascuna riga porta ### **la frase
# ### che l-ha decisa** -- il mandato chiede proprio quello.
#
# ### ✔ **ESITI MISURATI** -> classe `MISURA`, dominio `FISICA`.
DECISO_ESITO = {
    "COMPONENTI:D1": "fallback 71.88 % -> ... | 5/5 PASS: e- IL NUMERO MISURATO di una "
        "componente sigillata",
    "COMPONENTI:D2": "guardia 4pi fallita nel 95.33 % | 6/6 PASS: idem, un numero "
        "misurato",
    "COMPONENTI:S3b": "l-orologio rallenta dove cs e- basso | 0.0100 volte a cs = "
        "0.1*CSM: un VALORE, non una prescrizione",
    "COMPONENTI:S3c": "a cs = CSM il fattore e- 1 esatto | 1.000000000000000: un valore "
        "misurato al bit",
    "REGISTRO_FISICA:C3": "frazione di impacchettamento 0.384 NELLA SFERA INTERNA: una "
        "frazione MISURATA",
    "REGISTRO_FISICA:D33": "Il segno si inverte oltre 3.5pi: un FATTO misurato sul difetto, "
        "non un criterio di giudizio",
    "REGISTRO_FISICA:P1": "somma dei pesi per nodo | 50 | 9 | 0.18: una riga di TAVOLA di "
        "misure (prima | dopo | valore)",
    "REGISTRO_FISICA:P2": "contrasto Imassa / Ivuoto | 13 | 27 | 2.1: idem",
    "REGISTRO_FISICA:P3": "Lambda | 140 | 5 | 0.036: idem",
    "REGISTRO_FISICA:P3b": "ampiezza dello scuotimento | - | 5x piu- bassa | 0.2: idem",
    "REGISTRO_FISICA:P4": "csfloor dentro le masse | 0.9 | 0.55 | 0.61: idem",
    "REGISTRO_FISICA:P5": "lambdanodi | - | quasi COSTANTE, 0.74-0.76 LAM ovunque | -: e- "
        "L-ESEMPIO CHE IL MANDATO DA-",
    "REGISTRO_FISICA:T2": "-0.15 ... +0.44 | fa cio- che la geometria impone: un INTERVALLO "
        "misurato",
}
# ### ⛔ **CANDIDATI RIFIUTATI: la regola li aveva presi, e LEGGENDO sono CONTROLLI.**
# ### Il numero c-e-, ma ### **non e- una misura: e- il valore CONTRO CUI si confronta.**
DECISO_CRITERIO = {
    "REGISTRO_FISICA:A3": "un nodo nato da MITOSI parte da ramp = 0 e arriva a 1 nel suo "
        "tempo-luce: <<parte da ... e arriva a>> e- CIO- CHE SI VERIFICA, "
        "non cio- che si e- misurato",
    "REGISTRO_FISICA:A4": "contrasto massa/vuoto e Lam al passo 1, CONTRO P2 = 27 e P3 = 5: "
        "<<contro>> dice che 27 e 5 sono i valori DI RIFERIMENTO, cioe- il "
        "criterio",
    "REGISTRO_FISICA:S3": "passo ZERO: sum(d < LAM) == 0 E sum(d == LAM) == 0: due CONTROLLI, "
        "e `==` non e- una misura",
    "REGISTRO_FISICA:S5": "nodi isolati == 0: un CONTROLLO",
}


def punto2():
    """### Seleziona i candidati a ESITO; ### **la decisione la prendo LEGGENDO**, e la frase
    di ciascuno finisce nel referto."""
    voci = carica()
    cand = [v for v in voci if v["classe"] == "CRITERIO" and v["dominio"] == "FISICA"]
    print("  le voci `CRITERIO`/`FISICA`: %d" % len(cand))
    esiti, criteri = [], []
    for v in cand:
        t = " ".join(testo(v).split())
        tl = t.lower()
        pres = [s for s in PRESCRIVE if s.lower() in tl]
        num = MISURATO.search(t)
        (esiti if (num and not pres) else criteri).append((v, t, pres, num))
    print("  -> candidati a ESITO MISURATO (numero, e NESSUN verbo prescrittivo): %d"
          % len(esiti))
    print("  -> criteri veri:                                                    %d"
          % len(criteri))
    print()
    for v, t, _p, num in esiti:
        print("      %-24s %s" % (v["id"], t[:104]))
        print("      %-24s ^ il numero: %r" % ("", num.group(0)))
    io.open(os.path.join(D, "_p2_esiti.json"), "w", encoding="utf-8", newline=NL).write(
        json.dumps({"esiti": [{"id": v["id"], "frase": t, "numero": num.group(0)}
                              for v, t, _p, num in esiti],
                    "criteri": [v["id"] for v, _t, _p, _n in criteri]},
                   ensure_ascii=False, indent=1))
    print()
    print("  scritto doc/indice/_p2_esiti.json -- ### la frase di ciascuno, per il referto")
    return esiti, criteri


def punto2_lotto():
    """### Il LOTTO del punto `2`: ### **la classe `CRITERIO` torna una cosa sola.**

    ### ⛔ **`era` e `stato` NON si toccano**, e il mandato lo dice: *<<era invariata, stato
    invariato (`SOSPESA` resta `SOSPESA`, `CHIUSA` resta `CHIUSA`)>>*. Si cambia
    ### **solo il dominio** -- e per i `13` esiti ### **anche la classe.**
    """
    voci = carica()
    cand = [v for v in voci if v["classe"] == "CRITERIO" and v["dominio"] == "FISICA"]
    lotto = []
    for v in cand:
        i = v["id"]
        if i in DECISO_ESITO:
            lotto.append({"id": i, "quando": DATA,
                          "campi": {"classe": "MISURA"},
                          "meta": {"nota_guardiano":
                                   "punto 2: NON e- un criterio ma un ESITO MISURATO, e "
                                   "resta FISICA. La frase che decide: " +
                                   DECISO_ESITO[i]},
                          "motivo": ("(2) ESITO MISURATO, non criterio: resta `FISICA` e la "
                                     "classe passa a `MISURA`. La frase che decide e- <<%s>>"
                                     % DECISO_ESITO[i])})
        else:
            nota = ("punto 2: un criterio DICE COME SI GIUDICA, quindi METODO. era e stato "
                    "INVARIATI")
            if i in DECISO_CRITERIO:
                nota = ("punto 2: la regola l-aveva preso per un ESITO e LEGGENDO e- un "
                        "CONTROLLO -- " + DECISO_CRITERIO[i])
            lotto.append({"id": i, "quando": DATA,
                          "campi": {"dominio": "METODO"},
                          "meta": {"nota_guardiano": nota},
                          "motivo": ("(2) UN CRITERIO DICE COME SI GIUDICA, quindi METODO "
                                     "(criterio di classificazione del guardiano, NON una "
                                     "decisione di fisica). era e stato INVARIATI. Il testo "
                                     "dice <<%s>>" % pezzo(v, 80))})
    scrivi("v3_p2.jsonl", lotto)
    print("  (2) %d a `METODO`, %d a classe `MISURA` restando `FISICA`"
          % (len(cand) - len(DECISO_ESITO), len(DECISO_ESITO)))
    print("  ### I 4 CANDIDATI RIFIUTATI, e il perche- sta nella loro nota:")
    for i in sorted(DECISO_CRITERIO):
        print("      %-24s %s" % (i, DECISO_CRITERIO[i][:92]))


# ==========================================================================
#   PUNTO 3  --  `F2`: la frase in cui la voce dice che cosa SOSTITUISCE o PRESCRIVE
# ==========================================================================
# ### ⛔ **LA CITAZIONE NON SI RICOPIA: SI ESTRAE DAL TESTO VIVO.** Per ogni voce ho
# ### ### **letto** il testo e scelto ### **un marcatore**; la frase la ritaglia il codice
# ### ### **attorno a quel marcatore, dal testo della voce**. Cosi- la citazione e-
# ### ### **letterale PER COSTRUZIONE**, e non per mia diligenza nel copiare -- e se il
# ### marcatore non c-e-, ### **il codice si ferma** invece di scrivere un-eccezione falsa.
F2_MARCATORE = {
    "CONSERVAZIONE-LOCALE": "SI CONSERVANO LOCALMENTE",
    "FRECCE-IMPOSTE": "deve EMERGERE dalla dinamica",
    "GRAVITA-POTENZIALE": "Poisson e un VINCOLO DI SCALA",
    "INVARIANZA-LOCALE-CS": "MISURA LA SUA c_s COSTANTE SUL POSTO",
    "M-FLUSSO": "al posto di mem_mot",
    "M-ISTERESI": "COMPLEMENTO di MEM-VERSO",
    "MASSE-PESI-SOVRAPPOSTE": "E UNA CONFIGURAZIONE DEL CAMPO",
    "VUOTO-LOCALE-DETERMINISTICO": "UNA legge per nodo",
}
# ### ⛔ **`ENERGIA-NON-DEFINITA` NON SI TOCCA**, e il mandato lo dice: prende
# ### ### **solo la nota**, perche- la domanda e- di Luca. ### **Il guardiano scrive che
# ### secondo lui e- superata** *(«con `A16` l-energia c-e-, ed e- `H`»)*, ### **e lo dice
# ### come opinione, non come decisione.**
F2_NOTA = ("da decidere da Luca: superata da A16 (H definita)?")


def punto3():
    import indice as IX
    voci = carica()
    per = {v["id"]: v for v in voci}
    segn = {i for i, _m in IX._f2_era2(voci)}
    assert segn == set(F2_MARCATORE) | {"ENERGIA-NON-DEFINITA"}, (
        "i segnali di F2 NON sono i 9 che ho letto: %s" % sorted(segn))
    lotto = []
    for i in sorted(F2_MARCATORE):
        v = per[i]
        t = " ".join(testo(v).split())
        k = t.find(F2_MARCATORE[i])
        assert k >= 0, "`%s`: il marcatore %r NON e- nel testo" % (i, F2_MARCATORE[i])
        # ### la finestra: ### **dal testo vivo**, mai ricopiata
        frase = t[max(0, k - 46):k + len(F2_MARCATORE[i]) + 46]
        assert len(frase) >= 20
        lotto.append({"id": i, "quando": DATA, "campi": {},
                      "meta": {"eccezione_presidio":
                               ["F2: la voce e- di PROGRAMMA e nomina l-era 1 perche- dice "
                                "CHE COSA SOSTITUISCE o PRESCRIVE: <<%s>>" % frase]},
                      "motivo": ("(3) SEGNALE CHIUSO CON ECCEZIONE: F2 ha ragione a vedere "
                                 "l-era 1, ma la voce e- AL POSTO GIUSTO -- e- di programma, "
                                 "e nomina il vecchio codice per dire che cosa sostituisce: "
                                 "<<%s>>" % frase)})
    v = per["ENERGIA-NON-DEFINITA"]
    lotto.append({"id": "ENERGIA-NON-DEFINITA", "quando": DATA, "campi": {},
                  "meta": {"nota_guardiano": F2_NOTA},
                  "motivo": ("(3) NON SI TOCCA, per mandato: resta `%s`/era `%s`/`%s` e "
                             "prende SOLO la nota. Il testo dice <<%s>>, e il guardiano scrive "
                             "che con A16 l-energia c-e- ed e- H: LA DECISIONE E- DI LUCA"
                             % (v["dominio"], v["era"], v["stato"], pezzo(v, 80)))})
    scrivi("v3_p3.jsonl", lotto)
    print("  (3) %d eccezioni che CITANO il <<sostituisce>>, piu- la nota di "
          "ENERGIA-NON-DEFINITA" % len(F2_MARCATORE))
    for x in lotto:
        e = x["meta"].get("eccezione_presidio")
        print("      %-30s %s" % (x["id"], (e[0] if e else "NOTA: " + F2_NOTA)[:88]))


def main(argv):
    assert argv and argv[0] in ("1", "2", "2b", "3", "4"), __doc__
    {"1": punto1, "2": punto2, "2b": punto2_lotto, "3": punto3}[argv[0]]()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
