# -*- coding: utf-8 -*-
"""IL PUNTO `5`: le etichette che `F4` segnala, **decise dopo aver cercato TUTTE le
definizioni** *(`python csv/_cerca_definizioni.py --f4`)*.

| esito | quante | il criterio del mandato |
|---|--:|---|
| ### **RIPRISTINA come voce** | `7` | *«definita in un solo posto e con un contenuto *(una corsa, un sigillo, una legge, una misura)*»* |
| ### **OMONIMO**, `NON_DEFINITA` | `6` | *«definita in piu' posti con significati diversi -> non scegliere»* |
| ### **resta etichetta** | `1` | con l'eccezione, e il motivo e' ### **che la sua unica definizione dice che l'ID NON ESISTE** |
| ### ⚠ **il QUARTO caso** | `3` | ### **non e' nessuno dei tre**, ed e' elencato a parte *(lo avevo previsto nel task history)* |
| ### **zero definizioni** | `2` | `TEMPO-LUCE` e `MASSE-COERENTI`: il guardiano le dava per candidate, e ### **nel repo non sono definite da nessuna parte** |

### ⚠ **DUE LETTURE MIE, dichiarate:**
**①** il primo esito dice *«in un solo POSTO»*; `H1` e `H3` sono definite in ### **quattro
posti con UN SOLO SIGNIFICATO**. ### **Il cancello esiste per non FAR SCEGLIERE**, e con un
solo significato ### **non c'e' niente da scegliere**: le ripristino, e lo dico.
**②** il contenuto deve essere *«una corsa, un sigillo, una legge, una misura»*. ### **Una
REGOLA DI LAVORO non e' una legge** *(`AUTO-MANUTENZIONE`)* e ### **una FAMIGLIA di difetti
che punta a un'altra voce non e' nessuna delle quattro** *(`F4`, `F5`)*: ### **quarto caso.**

Gira con:  python csv/_p5_etichette.py
"""
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)
import migra_indice_v2 as MG                                 # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Costruisce lotti per l'indice.
NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
DATA = "2026-10-09"

# ==========================================================================
#   ① RIPRISTINA  --  (classe, dominio, era, stato, che cos'e' il contenuto)
# ==========================================================================
RIPRISTINA = {
    "CURA1-CORTO": ("MISURA", "FISICA", "1", "APERTA",
                    "UNA CORSA: l-intestazione `## APERTO CURA1-CORTO` apre una sezione con "
                    "avvio, blob, HEAD e il comando che la rigira. E lo stato APERTA non "
                    "l-ho scelto: lo dice l-intestazione"),
    "CURA2-CORTO": ("MISURA", "FISICA", "1", "APERTA",
                    "UNA CORSA: stessa forma di CURA1-CORTO, stessa sezione di "
                    "doc/STATO_RUN.md"),
    "SIGILLO-CURA2": ("MISURA", "FISICA", "1", "APERTA",
                      "UN SIGILLO: `## APERTO SIGILLO-CURA2` in doc/STATO_RUN.md, con la "
                      "corsa che lo esegue"),
    "SIGILLO-CURA2-RIPARATO": ("MISURA", "FISICA", "1", "APERTA",
                               "UN SIGILLO: idem, il ri-giro riparato"),
    "DE-ACCOPPIABILITA": ("MISURA", "FISICA", "1", "SOSPESA",
                          "UNA MISURA: `## 4. DE-ACCOPPIABILITA- -- analisi, non piano`, e "
                          "il contenuto e- un FATTO letto dal codice -- <<la legge GIA- GIRA "
                          "in entrambi gli schemi>>"),
    "H1": ("MISURA", "FISICA", "1", "SOSPESA",
           "UNA MISURA, e in QUATTRO POSTI CON UN SOLO SIGNIFICATO: <<la scena NON tocca "
           "phivel>>, confermata per struttura"),
    "H3": ("MISURA", "FISICA", "1", "SOSPESA",
           "UNA MISURA, e in QUATTRO POSTI CON UN SOLO SIGNIFICATO: <<chi scalda il vuoto, "
           "il termostato o lo scuotimento>> -- il fatto regge, la causa no"),
}
# ==========================================================================
#   ② OMONIMI  --  si dichiarano, NON si scelgono
# ==========================================================================
OMONIMI = {
    "D3": "le stesse DUE TAVOLE di D4, D5 e D6: doc/CENSIMENTO_intenzioni.md (una voce del "
          "censimento) e doc/MAPPA_accoppiamenti_spin.md (un TERMINE di accoppiamento), piu- "
          "la forma U(2) della coppia",
    "D4": "le stesse DUE TAVOLE: doc/CENSIMENTO_intenzioni.md (l-evoluzione SU(2) congelata) "
          "e doc/MAPPA_accoppiamenti_spin.md (il RUMORE DEL VUOTO, `_nb`)",
    "H2": "DUE oggetti: l-ipotesi dello scioglimento (<<la coppia non legge la fase "
          "corrente>>) e un CRITERIO LOCALE del sigillo del twist (<<H2 e H3: forma "
          "algebrica>>)",
    "S1": "e- UN CRITERIO LOCALE DI SIGILLO, e ogni sigillo gli da- un senso suo: <<il "
          "controllo forte, il blob nuovo riproduce AL BIT>>, <<riduzione al limite: "
          "allineati -> U = I>>, <<controlli positivi sintetici>>, <<FAIL ATTESO>>",
    "S3": "idem: <<`d` sotto LAM>>, <<riduzione DETERMINISTICA: spengo il rumore del "
          "vuoto>>, <<0 differenze non spiegate>>",
    "T1": "idem: <<lo SCHEDULATORE DEL PASSO>>, <<T1 e- BYTE-IDENTICO>>, <<la nascita "
          "conserva -- RESTRINGE A14.2>>",
}
# ==========================================================================
#   ③ RESTA ETICHETTA, con l'eccezione
# ==========================================================================
RESTA = {
    "GLOBALE-DIS": "la sua UNICA definizione dice che l-ID NON ESISTE: "
                   "doc/relazioni/2026-09-26.md:1068, <<GLOBALE-DIS NON ESISTE: L-HO "
                   "INVENTATO IO TRONCANDO>>. Ripristinarla come voce sarebbe dare un posto "
                   "nell-indice a UN TRONCAMENTO",
}
# ==========================================================================
#   ④ IL QUARTO CASO  --  non e' nessuno dei tre, e si ELENCA
# ==========================================================================
QUARTO = {
    "AUTO-MANUTENZIONE": "da decidere da Luca: definita in UN SOLO POSTO "
                         "(doc/STORIA_REGOLE.md:479) ma il contenuto e- UNA REGOLA DI "
                         "LAVORO, non una corsa ne- un sigillo ne- una legge ne- una "
                         "misura. Il mandato non dice che farne",
    "F4": "da decidere da Luca: definita in UN SOLO POSTO "
          "(doc/relazioni/2026-09-21.md:3572) ma il contenuto e- UNA FAMIGLIA DI DIFETTI che "
          "punta a un-altra voce (<<scritture di stato senza traccia | D04>>), non una "
          "corsa ne- un sigillo ne- una legge ne- una misura",
    "F5": "da decidere da Luca: idem, <<fasi col periodo sbagliato | D34>>",
}
# ### ⚠ **E DUE CHE IL GUARDIANO DAVA PER CANDIDATE, e il repo dice NO:** `TEMPO-LUCE` e
# ### `MASSE-COERENTI` hanno ### **ZERO definizioni in tutto il repo.** `F4` le segnalava da
# ### un'intestazione in cui l'ID sta ### **dentro la prosa**, e con la regola nuova
# ### ### **non le segnala piu'**: non serve nessuna eccezione, e vanno nel referto.
ZERO = ("TEMPO-LUCE", "MASSE-COERENTI")


def main():
    vecchie = MG.vecchio_indice()
    defi = json.loads(io.open(os.path.join(D, "_definizioni.json"),
                              encoding="utf-8").read())
    etich = {json.loads(r)["id"]: json.loads(r) for r in
             io.open(os.path.join(D, "etichette_rimosse.jsonl"),
                     encoding="utf-8").read().split(NL) if r.strip()}
    nuove, aggiorna = [], []
    for i, (cl, dom, era, st, perche) in sorted(RIPRISTINA.items()):
        d = defi[i]
        assert d, i
        y = d[0] if len(d) == 1 else [x for x in d if x["tipo"] == "documento"][0] \
            if any(x["tipo"] == "documento" for x in d) else d[0]
        tit = " ".join(y["testo"].lstrip("#| ").replace("**", "").split())[:100]
        nuove.append({"campi": {
            "id": i, "titolo": tit, "descrizione": y["testo"], "classe": cl,
            "dominio": dom, "era": era, "stato": st,
            "fonte": "%s::%s" % (y["file"], tit[:60]),
            "stato_era_1": (vecchie.get(i) or {}).get("stato", "da-decidere"),
            "meta": {"tipo_era1": (vecchie.get(i) or {}).get("tipo", "altro"),
                     "nota_guardiano": "punto 5: RIPRISTINATA -- " + perche}},
            "quando": DATA, "togli_da_etichette": True,
            "motivo": ("(5) RIPRISTINATA: cercate TUTTE le definizioni nel repo, e ce n-e- "
                       "%d. %s. La definisce %s:%d, che dice <<%s>>"
                       % (len(d), perche, y["file"], y["riga"], tit[:70]))})
    for i, perche in sorted(OMONIMI.items()):
        d = defi[i]
        due = ["%s:%d -- %s" % (x["file"], x["riga"], " ".join(x["testo"].split())[:110])
               for x in d[:6]]
        if len(d) > 6:
            due.append("... e altre %d definizioni: la lista INTERA sta in "
                       "doc/indice/_definizioni.json" % (len(d) - 6))
        nuove.append({"campi": {
            "id": i, "titolo": "OMONIMO `%s`: %d definizioni con significati DIVERSI"
                               % (i, len(d)),
            "descrizione": perche, "classe": "NON_DEFINITA",
            "dominio": "DA_CLASSIFICARE", "era": "DA_CLASSIFICARE",
            "stato": "DA_CLASSIFICARE", "fonte": "%s::%s" % (d[0]["file"], i),
            "stato_era_1": (vecchie.get(i) or {}).get("stato", "da-decidere"),
            "meta": {"tipo_era1": (vecchie.get(i) or {}).get("tipo", "altro"),
                     "omonimo": due,
                     "nota_guardiano": "punto 5: OMONIMO, e NON SI SCEGLIE -- " + perche}},
            "quando": DATA, "togli_da_etichette": True,
            "motivo": ("(5) OMONIMO, e NON SI SCEGLIE: cercate TUTTE le definizioni nel "
                       "repo, e sono %d in %d file, con significati DIVERSI. %s"
                       % (len(d), len({x["file"] for x in d}), perche))})
    # ### ③ e ④ restano ETICHETTE: non sono voci, e un-etichetta NON ha un `meta`.
    # ### ⛔ **Quindi la loro chiusura non puo- passare da `eccezione_presidio`:** quella
    # ### chiave vive ### **nelle voci**. ### ➜ **Si scrive nel file delle etichette**, e il
    # ### presidio `F4` la legge da la-.
    for i, perche in sorted(list(RESTA.items()) + list(QUARTO.items())):
        e = etich[i]
        e["eccezione_presidio" if i in RESTA else "nota_guardiano"] = (
            ("F4: " + perche) if i in RESTA else perche)
        aggiorna.append(e)
    p = os.path.join(D, "_lotti", "v3_p5.jsonl")
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in nuove) + NL)
    q = os.path.join(D, "_lotti", "v3_p5_etichette.jsonl")
    io.open(q, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in aggiorna) + NL)
    print("  scritto doc/indice/_lotti/v3_p5.jsonl: %d voci NUOVE (%d ripristinate, %d "
          "omonimi)" % (len(nuove), len(RIPRISTINA), len(OMONIMI)))
    print("  scritto doc/indice/_lotti/v3_p5_etichette.jsonl: %d etichette che RESTANO"
          % len(aggiorna))
    for i in sorted(RIPRISTINA):
        print("      RIPRISTINA  %-24s %-8s %-8s %d definizioni"
              % (i, RIPRISTINA[i][0], RIPRISTINA[i][3], len(defi[i])))
    for i in sorted(OMONIMI):
        print("      OMONIMO     %-24s %d definizioni in %d file"
              % (i, len(defi[i]), len({x["file"] for x in defi[i]})))
    for i in sorted(RESTA):
        print("      ETICHETTA   %-24s eccezione" % i)
    for i in sorted(QUARTO):
        print("      QUARTO CASO %-24s nota: da decidere da Luca" % i)
    for i in ZERO:
        print("      ZERO DEFIN. %-24s il guardiano la dava per candidata: NEL REPO NON "
              "C-E-" % i)
    return 0


if __name__ == "__main__":
    sys.exit(main())
