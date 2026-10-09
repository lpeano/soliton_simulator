# -*- coding: utf-8 -*-
"""L'ULTIMA PULIZIA DELL'INDICE `v3` — i punti `1`, `3` e `4`.

| punto | che cosa |
|---|---|
| `1` | le `4` voci da `APERTA` a `SOSPESA`, e l'### **«APERTO» del documento va in `stato_era_1`**, che e' il suo posto |
| `3` | gli `11` segnali di `F1`: `M1` e `C4` sono ### **OMONIMI**, gli altri `8` chiudono con un'eccezione che ### **cita la frase** |
| `4` | i `3` di `F4`, con la ### **regola dei tre esiti** del giro scorso |

### ⛔ **L'ORDINE NON E' LIBERO:** il punto `1` deve precedere `F7` *(punto `2`)*, perche'
`F7` fa ### **fallire la validazione** e la validazione gira ### **dentro `aggiorna-lotto`**.

Gira con:  python csv/_pulizia_finale.py <1|3|4>
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

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Costruisce lotti per l'indice.
NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
DATA = "2026-10-09"

# ==========================================================================
#   PUNTO 1
# ==========================================================================
P1 = ("CURA1-CORTO", "CURA2-CORTO", "SIGILLO-CURA2", "SIGILLO-CURA2-RIPARATO")

# ==========================================================================
#   PUNTO 3  --  i due OMONIMI, e le otto frasi
# ==========================================================================
# ### ⛔ **DUE OMONIMI CHE IL GUARDIANO HA VISTO LEGGENDO `F1`**, come `C5` il giro scorso.
OMONIMI_3 = {
    "M1": ["la VOCE `M1`: <<LA MATERIA E- UNO STATO, NON UNA SOSTANZA -- e non c-e- "
           "SCARICO>>, un difetto FISICA/era 2",
           "il <<M1>> citato da `E3`: ### **LA MISURA DEL RUN** -- <<M1/M4 leggere durante "
           "il run>>, cioe- una delle misure dell-epoca 3"],
    "C4": ["la VOCE `C4`: <<inerzia = T^2 -- chiude il buco dimensionale>>, una misura "
           "FISICA/era 1",
           "il <<C4>> citato da `COLLAUDO-NON-ESEGUITO`: ### **IL CONTROLLO `C4`** della "
           "migrazione -- <<un collaudo che si RIFIUTA di girare esce con 2, e il controllo "
           "C4 lo conta come PASS>>"],
}
# ### Il MARCATORE: la frase si ritaglia ### **dal testo vivo**, non si ricopia.
F1_MARCATORE = {
    "E3": ("OMONIMO", "M1/M4 leggere durante il run",
           "il <<M1>> del titolo e- LA MISURA DEL RUN, non la voce `M1`"),
    "COLLAUDO-NON-ESEGUITO": ("OMONIMO", "il controllo C4 lo conta come PASS",
                              "il <<C4>> del titolo e- IL CONTROLLO della migrazione, non "
                              "la voce `C4`"),
    "COER-4PI": ("CRITERIO", "la coerenza della massa",
                 "e- IL CRITERIO CHE VERIFICA il difetto che cita: un criterio nomina la "
                 "legge su cui gira, e questa e- la relazione normale fra un controllo e la "
                 "sua legge"),
    "REGISTRO_FISICA:E3": ("CRITERIO", "la finestra di D33",
                           "e- IL CRITERIO CHE VERIFICA il difetto che cita"),
    "REGISTRO_FISICA:S6": ("CRITERIO", "se la cura ha curato D02",
                           "e- IL CRITERIO CHE VERIFICA il difetto che cita"),
    "REGISTRO_FISICA:U2": ("CRITERIO", "ATTIVA IN ENTRAMBI I BRACCI",
                           "e- IL CRITERIO CHE VERIFICA il difetto che cita"),
    "ETICHETTA-A13": ("DOCUMENTO", "dove la regola e'",
                      "e- UN DIFETTO DI DOCUMENTAZIONE che CITA LA REGOLA GIUSTA: senza "
                      "nominarla non direbbe qual e- l-etichetta sbagliata"),
    "M-MASSA": ("DIPENDENZA", "dipende da",
                "DICHIARA DA CHE COSA DIPENDE: una cura che non nomina la sua dipendenza "
                "non si puo- ordinare"),
    "AB-CONTROLLI": ("DIPENDENZA", "A/B di W5",
                     "DICHIARA SU CHE COSA GIRAVA l-A/B: e- la voce di cui parla"),
}

# ==========================================================================
#   PUNTO 4  --  i tre del <<quarto caso>>, decisi con la regola dei tre esiti
# ==========================================================================
# ### ⛔ **La mia uscita «non e' nessuno dei tre» NON E' PIU' DISPONIBILE**, e va bene: era
# ### una domanda, e la risposta del mandato e' ### **«decidi».**
# ### ⭐ **E la via e' L'EREDITA':** `F4` e `F5` sono ### **famiglie di difetti**, e il testo
# ### dice ### **da quale difetto nascono.** `D04` e `D34` sono ### **`FISICA`, era `1`**
# ### *(misurato)*, e ### **una famiglia prende il dominio del difetto da cui nasce.**
P4 = {
    "AUTO-MANUTENZIONE": ("STANDARD", "METODO", "ENTRAMBE", "APERTA",
                          "UNA REGOLA DI LAVORO, e una regola e- UNA LEGGE DEL METODO: "
                          "`## 5-bis. AUTO-MANUTENZIONE (tieni aggiornati i documenti "
                          "vivi)` in doc/STORIA_REGOLE.md, in un solo posto. Vale per "
                          "ENTRAMBE le ere perche- il metodo non cambia con l-era"),
    "F4": ("DIFETTO", "FISICA", "1", "SOSPESA",
           "UNA FAMIGLIA DI DIFETTI, e il testo dice DA QUALE DIFETTO NASCE: <<scritture di "
           "stato senza traccia | D04>>. EREDITA il dominio da `D04`, che e- FISICA/era 1, e "
           "lo stato SOSPESA perche- `D04` e- SOSPESA"),
    "F5": ("DIFETTO", "FISICA", "1", "SOSPESA",
           "UNA FAMIGLIA DI DIFETTI: <<fasi col periodo sbagliato | D34, dal censimento in "
           "corso>>. EREDITA il dominio da `D34`, FISICA/era 1; SOSPESA e non CHIUSA perche- "
           "il testo dice <<dal censimento IN CORSO>>"),
}


def carica():
    return [json.loads(r) for r in io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8")
            if r.strip()]


def testo(v):
    return " ".join([v.get("titolo") or "", v.get("descrizione") or "",
                     v.get("fonte") or ""])


def pezzo(v, n=70):
    return " ".join(testo(v).split())[:n]


def scrivi(nome, lotto):
    p = os.path.join(D, "_lotti", nome)
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in lotto) + NL)
    print("  scritto doc/indice/_lotti/%s: %d voci" % (nome, len(lotto)))


def punto1():
    per = {v["id"]: v for v in carica()}
    lotto = []
    for i in P1:
        v = per[i]
        assert v["stato"] == "APERTA", "`%s` non e- APERTA: %s" % (i, v["stato"])
        lotto.append({"id": i, "quando": DATA,
                      "campi": {"stato": "SOSPESA", "stato_era_1": "aperto"},
                      "meta": {"nota_guardiano":
                               "punto 1: la fisica dell-era 1 NON CHIUSA e- SOSPESA. "
                               "L-<<APERTO>> dell-intestazione e- lo stato DELL-ERA 1, e sta "
                               "in stato_era_1 -- nel giro scorso l-avevo messo in `stato`, "
                               "che e- lo stato DI OGGI"},
                      "motivo": ("(1) da APERTA a SOSPESA: LA REGOLA IN VIGORE dice che la "
                                 "fisica dell-era 1 non chiusa e- SOSPESA. L-<<APERTO>> di "
                                 "`## APERTO %s` e- lo stato DELL-ERA 1 e passa in "
                                 "stato_era_1. Il testo dice <<%s>>" % (i, pezzo(v)))})
    scrivi("v3_q1.jsonl", lotto)
    print("  (1) %d voci da APERTA a SOSPESA, e l-<<APERTO>> va in stato_era_1" % len(P1))


def punto3():
    import indice as IX
    voci = carica()
    per = {v["id"]: v for v in voci}
    segn = IX._f1_gemelle(voci)
    voci_segn = {i for i, _m in segn}
    assert voci_segn == set(F1_MARCATORE), (
        "i segnali di F1 NON sono sulle 8 voci che ho letto: %s" % sorted(voci_segn))
    lotto = []
    for i, due in sorted(OMONIMI_3.items()):
        v = per[i]
        lotto.append({"id": i, "quando": DATA, "campi": {},
                      "meta": {"omonimo": due,
                               "nota_guardiano": "punto 3: OMONIMO, e NON SI SCEGLIE -- il "
                                                 "guardiano l-ha visto leggendo F1, come "
                                                 "per `C5`"},
                      "motivo": ("(3) OMONIMO, e NON SI SCEGLIE: <<%s>> nomina DUE OGGETTI "
                                 "DIVERSI. La voce dice <<%s>>, e cio- che le altre voci "
                                 "citano e- un-altra cosa" % (i, pezzo(v, 80)))})
    for i in sorted(F1_MARCATORE):
        gruppo, marc, perche = F1_MARCATORE[i]
        v = per[i]
        t = " ".join(testo(v).split())
        if marc:
            k = t.find(marc)
            assert k >= 0, "`%s`: il marcatore %r NON e- nel testo" % (i, marc)
            frase = t[max(0, k - 50):k + len(marc) + 50]
        else:
            frase = t[:100]
        assert len(frase) >= 20
        lotto.append({"id": i, "quando": DATA, "campi": {},
                      "meta": {"eccezione_presidio":
                               ["F1: %s -- %s. Il testo dice <<%s>>"
                                % (gruppo, perche, frase)]},
                      "motivo": ("(3) SEGNALE CHIUSO CON ECCEZIONE (%s): %s. Il testo dice "
                                 "<<%s>>" % (gruppo, perche, frase))})
    scrivi("v3_q3.jsonl", lotto)
    print("  (3) %d omonimi, %d eccezioni su %d segnali"
          % (len(OMONIMI_3), len(F1_MARCATORE), len(segn)))


def punto4():
    import migra_indice_v2 as MG
    vecchie = MG.vecchio_indice()
    defi = json.loads(io.open(os.path.join(D, "_definizioni.json"),
                              encoding="utf-8").read())
    nuove = []
    for i, (cl, dom, era, st, perche) in sorted(P4.items()):
        d = defi[i]
        assert len(d) == 1, "`%s`: mi aspettavo UNA definizione, ne trovo %d" % (i, len(d))
        y = d[0]
        tit = " ".join(y["testo"].lstrip("#| ").replace("**", "").split())[:100]
        nuove.append({"campi": {
            "id": i, "titolo": tit, "descrizione": y["testo"], "classe": cl,
            "dominio": dom, "era": era, "stato": st,
            "fonte": "%s::%s" % (y["file"], tit[:60]),
            "stato_era_1": (vecchie.get(i) or {}).get("stato", "da-decidere"),
            "meta": {"tipo_era1": (vecchie.get(i) or {}).get("tipo", "altro"),
                     # ### `nota_guardiano` e- `testo_breve`, regex `^.{1,300}$`: la
                     # ### nota si TAGLIA, e ### **il perche- INTERO resta nel
                     # ### `motivo`**, che non ha limite. ### **Un campo con un
                     # ### limite dichiarato non si allarga per far stare una frase.**
                     "nota_guardiano": ("punto 4: il <<quarto caso>> del giro scorso, "
                                        "DECISO con la regola dei tre esiti -- "
                                        + perche)[:300]}},
            "quando": DATA, "togli_da_etichette": True,
            "motivo": ("(4) RIPRISTINATA: nel giro scorso l-avevo messa nel <<quarto caso>>, "
                       "e il mandato dice di chiudere CON LA REGOLA DEI TRE ESITI. %s. La "
                       "definisce %s:%d, che dice <<%s>>"
                       % (perche, y["file"], y["riga"], tit[:70]))})
    scrivi("v3_q4.jsonl", nuove)
    print("  (4) %d ripristinate col criterio dell-EREDITA- (F4 da D04, F5 da D34)"
          % len(P4))
    for i in sorted(P4):
        print("      %-22s %-9s %-7s era %-9s %s" % (i, P4[i][0], P4[i][1], P4[i][2],
                                                     P4[i][3]))


def main(argv):
    assert argv and argv[0] in ("1", "3", "4"), __doc__
    {"1": punto1, "3": punto3, "4": punto4}[argv[0]]()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
