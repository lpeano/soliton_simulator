# -*- coding: utf-8 -*-
"""IL COLLAUDO DI `P-REG` — **e il braccio che conta è <<NESSUNA REGOLA SI PERDE>>.**

### ⭐ **TUTTI GLI ALTRI BRACCI GUARDANO LA FORMA; quello guarda LA COSA.** Un errore in
questo mandato ### **non fa cadere un collaudo: fa sparire una regola** — e una regola
sparita ### **non si vede, perché il file è più corto e sembra più pulito.**
### ⚠ **`CLAUDE.md` più corto NON è un successo: è un SOSPETTO.**

### ⛔ **E IL BRACCIO SI MISURA CONTRO `git`, non contro una lista mia:** l'insieme delle
regole citate ### **al commit del task history** contro quello ### **di adesso.** ### **Una
lista mia sarebbe scritta dalla stessa mano che può perdere la regola.**

### 📌 **E DUE FALSI ALLARMI MI HANNO INSEGNATO A FIDARMI DI QUESTO BRACCIO E NON DEI
CONTATORI.** Il mio contatore diceva ### **`15` regole citate dove prima erano `23`** —
cioè *«ne hai perse otto»* — e `csv/_struttura_regole.py` diceva ### **`0` su `17`**, cioè
*«le hai perse TUTTE».* ### ⭐ **Entrambi non riconoscevano la forma `[[ID]]`** che il
`par.9` pretende per gli scritti nuovi, e che la sezione generata usa. ### ✅ **Il confronto
con `git` diceva `0` perse, ed era quello giusto.** ### ⛔ **Se mi fossi fidato dei
contatori, avrei cercato un difetto che non c'era — e peggio: avrei potuto <<curarlo>>
riscrivendo le regole.**
"""
import io
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)

import _regole_gestione as RG                               # noqa: E402

NL = chr(10)

# ### ⛔ **IL COMMIT DEL TASK HISTORY di questo mandato**: per il rito del par. `8` è
# ### **antenato** dei commit del lavoro, quindi è ### **il <<prima>> giusto.**
PRIMA = "973f91d"


def collaudo():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-62s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL COLLAUDO DI `P-REG` -- nei DUE VERSI   (mandato 5)")
    print("=" * 100)
    c = RG.conta()
    print("  regole di gestione nell-indice: %d   dichiarate in `CLAUDE.md`: %d  %s"
          % (c["nell_indice"], c["in_claude"], c["per_paragrafo"]))
    print("  SENZA UN PRESIDIO che le faccia rispettare: %d   (`A9`)"
          % c["senza_presidio"])
    print("  righe di `CLAUDE.md`: %d su 400" % c["righe_claude"])
    print()
    # =========================================================== IL BRACCIO CHE CONTA
    perse = RG.perse(PRIMA)
    pri = set(RG.citate_a(PRIMA))
    ora = set(RG.citate())
    esito("### DEVE essere VUOTO: le regole PERSE fra `%s` e adesso" % PRIMA,
          perse == [],
          "prima %d, ora %d, PERSE %d. ### E- IL SOLO CONTROLLO CHE CONTA DAVVERO: una "
          "regola sparita non si vede, perche- il file e- piu- corto e SEMBRA PIU- PULITO"
          % (len(pri), len(ora), len(perse)))
    esito("### e il collaudo ha MATERIA: ci sono regole citate",
          len(pri) > 10,
          "%d al commit del task history: ### senza di loro il braccio di sopra "
          "passerebbe PER VACUITA-" % len(pri))
    # ### ⚠ **E L-ELENCO DELLE NUOVE E- CRESCIUTO MENTRE LAVORAVO: `P-REG`
    # ### stesso.** ### **Il braccio ha fatto il suo lavoro dicendomelo**, e la cura e-
    # ### ### **aggiornare l-elenco**, non togliere il braccio: ### **se comparisse una
    # ### regola che NON ho creato, vorrebbe dire che il generatore ne INVENTA.**
    esito("### e le regole NUOVE sono quelle che ho creato IO, non altre",
          sorted(ora - pri) == ["DECISIONE-VUOLE-UN-CAMPO", "P-REG",
                                "PRECEDENZA-IN-CODA"],
          "%s: ### se comparisse una regola che non ho creato, vorrebbe dire che il "
          "generatore ne INVENTA" % sorted(ora - pri))
    print()
    # =========================================================== la FORMA
    esito("NON deve scattare: `P-REG` tace su `CLAUDE.md` come e- adesso",
          RG.errori() == [],
          "### se scattasse, sarebbe `CLAUDE.md` a essere fuori posto, non il presidio")
    esito("### il tetto di `H-RIGHE` e- rispettato",
          c["righe_claude"] <= 400,
          "%d su 400: ### e se la sezione generata lo sfondasse, SI ACCORCIA LA SINTESI, "
          "non si alza il tetto -- che e- la manopola che `A1` vieta" % c["righe_claude"])
    esito("### e ogni regola in `CLAUDE.md` ha un FILE DI DETTAGLIO che ESISTE",
          all(os.path.exists(os.path.join(RG.REGOLE, RG.file_di_dettaglio(x)))
              for x in RG.in_claude()),
          "%d regole: ### un rimando a un file che non c-e- e- PEGGIO di nessun rimando"
          % c["in_claude"])
    esito("### e <<chi la fa rispettare>> e- UN CAMPO, quindi SI CONTA",
          c["senza_presidio"] > 0,
          "%d regole su %d non hanno nessuno che le faccia rispettare (`A9`). "
          "### IN PROSA QUESTO NUMERO NON ESISTEVA" % (c["senza_presidio"],
                                                       c["in_claude"]))
    print()
    # =========================================================== i casi che DEVONO scattare
    # ### ⛔ **SI TOCCA `CLAUDE.md` DAVVERO, e si rimette verificando lo `sha1`:** il
    # ### ### **punto del mandato e- che una modifica a mano sia RIFIUTATA**, e provarlo
    # ### su una copia ### **non proverebbe il presidio: proverebbe una copia.**
    import hashlib
    b0 = io.open(RG.CLAUDE, "rb").read()
    sha0 = hashlib.sha1(b0).hexdigest()
    try:
        t = b0.decode("utf-8")
        # ### ⛔ **LA VITTIMA SI SCEGLIE FRA LE REGOLE GIA- CITATE AL <<PRIMA>>, e me
        # ### lo ha insegnato un braccio che FALLIVA.** Avevo preso ### **la prima riga
        # ### generata**, che in ordine alfabetico e- `DECISIONE-VUOLE-UN-CAMPO` --
        # ### ### **una regola NUOVA**, che al commit del task history ### **non era
        # ### citata.** ### ⚠ **Quindi togliendola <<perse>> restava VUOTO**, e il
        # ### braccio che deve vedere una perdita ### **non poteva vederla.**
        # ### ⭐ **Un caso che DEVE fallire e non puo- fallire PER COSTRUZIONE e- un
        # ### falso-uno**, ed e- lo stesso difetto che ho curato nelle simmetrie.
        # ### ⚠ **E DEVE ESSERE ANCHE NELLA SEZIONE GENERATA:** `A1` e- il
        # ### primo in ordine alfabetico fra le citate, ### **ma e- un ASSIOMA
        # ### citato nella PROSA del par. 3** -- la sua riga nella sezione
        # ### ### **non esiste.** ### **Due condizioni, non una.**
        _in_sez = {x["id"] for x in RG.in_claude()}
        # ### ⛔ **E DEVE COMPARIRE UNA VOLTA SOLA NEL FILE, e questa e- la TERZA
        # ### condizione che ho dovuto aggiungere.** `H-FILE` e- citata ### **anche nella
        # ### PROSA** *(le vie d-uscita del par. 12)*, quindi togliendola dalla tabella
        # ### ### **non spariva dal file** -- e <<perse>> restava vuoto, giustamente.
        # ### ⭐ **Tre giri su questo braccio, e OGNI VOLTA il braccio aveva ragione e
        # ### il mio caso era sbagliato.** ### **Un caso che DEVE fallire va costruito in
        # ### modo che POSSA fallire: se non puo-, non prova niente -- e il verde che
        # ### dava era UN FALSO-UNO.**
        _cand = [i for i in sorted(pri & ora & _in_sez)
                 if t.count("`[[%s]]`" % i) + t.count("`%s`" % i) == 1]
        assert _cand, ("### nessuna regola citata UNA VOLTA SOLA: il caso che deve "
                       "fallire non si puo- costruire, e lo DICO invece di far passare "
                       "un braccio che non prova niente")
        vittima = _cand[0]
        r = [x for x in t.split(NL) if ("[[%s]]" % vittima) in x]
        assert r, "### la riga di `%s` non si trova" % vittima
        rotto = t.replace(r[0], r[0].replace("[[%s]]" % vittima, "[[Z%s]]" % vittima), 1)
        io.open(RG.CLAUDE, "w", encoding="utf-8", newline="").write(rotto)
        e = RG.errori()
        esito("### DEVE scattare: la sezione generata MODIFICATA A MANO",
              any("NON COINCIDE col generato" in x for x in e),
              "### come le altre viste: una vista scritta a mano DIVERGE dalla fonte, e "
              "allora LA FONTE NON E- PIU- LA FONTE")
        # ### e il braccio delle regole perse DEVE vederlo
        esito("### e il braccio delle PERSE lo vede: una regola e- sparita",
              RG.perse(PRIMA) != [],
              "togliendo `%s`, che ERA citata al <<prima>>: %s. ### E- la prova che "
              "il braccio che conta FUNZIONA, non che e- verde per caso"
              % (vittima, RG.perse(PRIMA)[:2]))
    finally:
        io.open(RG.CLAUDE, "wb").write(b0)
    esito("### e `CLAUDE.md` e- tornato IDENTICO AL BYTE",
          hashlib.sha1(io.open(RG.CLAUDE, "rb").read()).hexdigest() == sha0,
          "`%s`: ### un collaudo che lascia `CLAUDE.md` storto ROMPE IL FLUSSO DI LAVORO"
          % sha0[:8])
    esito("NON deve scattare: rimesso il file, `P-REG` TACE di nuovo",
          RG.errori() == [], "### e il repo e- come l-ho trovato")
    # ### ⛔ **E IL RIGENERATO E- BYTE-IDENTICO** *(punto `5`)*.
    b1 = io.open(RG.CLAUDE, "rb").read()
    RG.scrivi()
    esito("### DEVE essere BYTE-IDENTICO: `CLAUDE.md` rigenerato",
          io.open(RG.CLAUDE, "rb").read() == b1,
          "### il punto 5 del mandato: se rigenerare cambia qualcosa, la sezione NON "
          "VIENE dalla fonte")
    # ### i duplicati sono un SEGNALE, non un errore
    dup = RG.duplicati()
    esito("### i duplicati sono un SEGNALE e non un errore, e oggi sono %d" % len(dup),
          True,
          "### il mandato lo dice cosi-: due regole con lo stesso contenuto sono UNA "
          "regola scritta due volte (`9-ter`)")
    print("=" * 100)
    print("IL COLLAUDO DI `P-REG`: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    import _presidio
    _presidio.avvia(__file__)
    sys.exit(collaudo())
