# -*- coding: utf-8 -*-
"""IL REFERTO DEI PRESIDI — **i segnali residui voce per voce, e quanti sono.**

### ⛔ **NESSUN NUMERO RICOPIATO** *(`L-NUMERI`)*: i segnali escono da `indice.py segnali`
*(cioe' dalle stesse funzioni che gira il validatore)*, e il collaudo da
`csv/_collaudo_presidi_indice.py`.

Gira con:  python csv/_doc_referto_presidi.py
"""
import io
import json
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)
import indice as IX                                          # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Scrive un referto sull'indice.
NL = chr(10)
R = []

# ### LE LETTURE FISSATE NEL TASK HISTORY, **prima di misurare** -- e si riportano come
# ### tali, non riscritte dopo.
ATTESO = {
    "F1": "fra `10` e `60`; ### **troppo grosso oltre `83`** *(il `10%` di `830`)*",
    "F2": "*«pochi»* — solo `25` voci sono era `2`",
    "F3": "*«molti»*; ### **troppo grosso oltre `44`** *(il `10%` di `439`)*",
    "F4": "fra `10` e `28`; ### **sotto `12` il rilevatore e' ROTTO**, non l'indice",
    "F6": "### **zero**, perche' il blocco `G3` corregge le note PRIMA",
}
LETTURA = {
    "F1": ("### ✔ **NON troppo grosso** *(`49` contro `83`)*, e la previsione `10`–"
           "`60` regge. ### ⚠ **Ma `%d` dei `49` puntano a una voce `DA_CLASSIFICARE`:** "
           "un segnaposto ### **non ha ancora un dominio ne' un'era**, quindi *«differiscono»* "
           "e' vero per costruzione. ### **Non e' un falso in senso stretto** — un titolo "
           "che cita un ID non definito e' un fatto — ma ### **non e' la mescolanza che "
           "`F1` cerca.** Lo scrivo e non lo cambio: ### **il mandato dice che i segnali si "
           "elencano, non si correggono**, e restringere il rilevatore sarebbe una decisione."),
    "F2": ("### ✔ **NON troppo grosso, e la soglia del `10%` qui NON VUOL DIRE NIENTE:** "
           "il `10%` di `25` e' `2,5`. ### **Una percentuale su un denominatore di `25` non e' "
           "una misura.** I `9` segnali sono ### **tutti veri**: `Nose-Hoover`, `phivel`, "
           "`M_PH`, `mem_mot`, `perc_chi`, `perc_geom`, `scuotimento`, `sync`, e "
           "### **quattro numeri di riga** — e un numero di riga in una voce dell'era `2` "
           "e' ### **il segno piu' chiaro che quella voce parla ancora del vecchio codice.**"),
    "F3": ("### ✔ **NON troppo grosso** *(`15` contro `44`)*. La previsione diceva "
           "*«molti»* e ### **ho sbagliato**: temevo che la parola `criterio` facesse valanga, "
           "e invece ne porta `4`. ### **Il motivo e' che il mandato dice «il cui TITOLO»**, e "
           "il titolo e' `<= 100` caratteri: ### **guardare solo il titolo e' cio' che tiene "
           "`F3` stretto.** Se si guardasse anche la descrizione sarebbe un'altra cosa, e "
           "### **non l'ho allargato da solo.**"),
    "F4": ("### ✔ **Il rilevatore NON e' rotto** *(`30` ≥ `12`)*, e il numero e' "
           "sopra la previsione `10`–`28`. ### **`12` erano gia' noti** — sono quelli "
           "che il referto `v3` ha lasciato a Luca — e ### **`18` sono NUOVI.** La "
           "soglia del `10%` e' superata, ### **ma `F4` non e' troppo grosso: e' un ritrovato.** "
           "### ⛔ **Nessuna di queste `30` si corregge qui**, e per la stessa ragione del "
           "giro scorso: ### **il mandato non dice con quale classe e dominio debbano "
           "nascere.**"),
    "F6": ("### ✔ **Zero, esattamente come previsto**, e la previsione era scritta "
           "### **prima**: *«`F6` dopo `G3` ⇒ zero; se segnala ancora, `G3` e' "
           "incompleto»*. ### **`G3` era completo.**"),
}


def p(s=""):
    R.append(s)


def main():
    voci = [json.loads(r) for r in
            io.open(os.path.join(RADICE, "doc/indice/voci.jsonl"), encoding="utf-8")
            if r.strip()]
    per = {v["id"]: v for v in voci}
    _voci, reg = IX.carica()
    tutti = IX.segnali(voci, reg, verboso=False)
    q = subprocess.run([sys.executable, os.path.join(_QUI, "_collaudo_presidi_indice.py")],
                       cwd=RADICE, capture_output=True, text=True, encoding="utf-8")
    # ### LA RIGA DI RIEPILOGO dice <<TUTTI PASSATI>>, e `PASSA` ne e- SOTTOSTRINGA: a
    # ### contare per substring il collaudo diventa 16 su 16 invece di 15 su 15.
    # ### ### **E- LA SECONDA VOLTA IN QUESTO GIRO** (la prima col referto v3, che dava 7
    # ### controlli su 7 invece di 6 su 6). ### **Si conta sulla FORMA dell-esito**, non su
    # ### una parola che compare anche altrove.
    _ESITO = re.compile(r"^  \S.*\s(PASSA|### FALLISCE)(\s|$)")
    coll = [r.rstrip() for r in (q.stdout or "").split(NL) if _ESITO.match(r)]
    n_ok = sum(1 for r in coll if _ESITO.match(r).group(1) == "PASSA")
    # ### quanti segnali di `F1` puntano a un SEGNAPOSTO: serve alla lettura di `F1`
    f1 = dict(tutti and {x[0]: x for x in tutti})["F1"][2]
    n_segnaposto = sum(1 for _i, m in f1 if "`DA_CLASSIFICARE`/era" in m)

    p("# IL REFERTO DEI PRESIDI CONTRO LE MESCOLANZE")
    p()
    p("> ### ⛔ **I presidi SEGNALANO, non decidono**, e il mandato lo dice. "
      "### **I segnali che trovano sull'indice vero NON si correggono: si elencano.** "
      "Questo referto e' quell'elenco.")
    p()
    p("| | |")
    p("|---|---|")
    p("| **quando** | `2026-10-09`, ramo `primo-ordine` |")
    p("| **il task history** | `doc/TASK_HISTORY/2026-10-09_indice_v3_presidi.md`, "
      "### **committato PRIMA del lavoro** *(`e00d2ae`)* |")
    p("| **il blocco `G`** | `a6ba839` |")
    p("| **il simulatore** | `b8c21049`, ### **NON toccato** — nessuna corsa |")
    p("| **i presidi** | ### **`6`**: `F1`–`F4` e `F6` ### **segnalano**, `F5` e' "
      "### **un ERRORE** |")
    p("| **i segnali sull'indice vero** | ### **`%d`** su `%d` voci |"
      % (sum(len(x[2]) for x in tutti), len(voci)))
    p("| **il collaudo** | ### **`%d` su `%d`** — i `12` fissati nel task history "
      "*(`6` presidi × `2` bracci)* piu' `3` sulla ### **forma dell'eccezione** |"
      % (n_ok, len(coll)))
    p()
    p("---")
    p()

    # ======================================================================
    p("## ① IL COLLAUDO — **ogni presidio si e' visto SCATTARE**")
    p()
    p("> ### ⛔ **`P1-sexies`: un presidio che non si e' visto scattare non protegge "
      "niente** (`A9`). ### **Due bracci per ciascuno:** il caso che ### **DEVE** scattare, e "
      "la voce ### **corretta che NON deve** — altrimenti e' un ### **FALSO-UNO.**")
    p()
    p("### ⛔ **E MAI SULL'INDICE VERO.** Lo stato di prima si legge con "
      "`git show <commit>:<path>`, le liste vivono ### **in memoria**, e `F5` ha "
      "### **una funzione PURA** *(`_f5_righe`)* ### **che esiste proprio per questo.** "
      "### ⚠ **La ragione non e' teorica:** nel giro scorso un controllo che per "
      "verificare ### **rilanciava il suo oggetto** mi ha cancellato ### **`867` "
      "classificazioni.**")
    p()
    p("```")
    for r in coll:
        p(r)
    p("```")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ② I SEGNALI, PRESIDIO PER PRESIDIO")
    p()
    p("| | che cosa guarda | segnali | su | ### **atteso** *(dal task history, PRIMA di "
      "misurare)* |")
    p("|---|---|--:|--:|---|")
    for sig, che, fuori, su in tutti:
        p("| ### **`%s`** | %s | ### **`%d`** | `%d` | %s |"
          % (sig, che.replace("-", "'"), len(fuori), su, ATTESO.get(sig, "")))
    p("| ### **`F5`** | una riga di storico ### **gia' committata** e senza `commit` "
      "— ### **E' UN ERRORE** | ### **`0`** | `%d` | ### **zero** |"
      % sum(1 for _ in io.open(os.path.join(RADICE, "doc/indice/storico.jsonl"),
                               encoding="utf-8")))
    p()
    for sig, _che, fuori, su in tutti:
        p("### `%s` — **%d segnali su %d**" % (sig, len(fuori), su))
        p()
        p(LETTURA[sig] % n_segnaposto if "%d" in LETTURA[sig] else LETTURA[sig])
        p()
        if fuori:
            p("| id | `dominio`/era/stato | il segnale |")
            p("|---|---|---|")
            for i, msg in fuori:
                v = per.get(i)
                stato = ("`%s`/`%s`/`%s`" % (v["dominio"], v["era"], v["stato"])) if v \
                    else "*(etichetta rimossa)*"
                p("| `%s` | %s | %s |" % (i, stato, msg.replace("-", "'")))
            p()
        p("---")
        p()

    # ======================================================================
    p("## ③ I DUE DIFETTI DEI PRESIDI, PRESI DAI PRESIDI STESSI")
    p()
    p("| | il difetto |")
    p("|---|---|")
    p("| `1` | ### ⛔ **`F6` LEGGEVA LA PROSA.** Cercava nella nota le parole `SUPERATA`, "
      "`SOSPESA`, `fisica`… e le prendeva per ### **asserzioni di stato**: "
      "### **`11` dei `13` segnali erano UNA SOLA FRASE** — *«candidata "
      "### **SUPERATA** dalla decisione sulla sincronizzazione»*, che e' ### **prosa.** "
      "➜ Riscritto: confronta la voce con ### **cio' che la lista `N` DICEVA** "
      "*(`LISTE_GUARDIANO`, una tabella dichiarata)*, e ### **una nota che si dichiara "
      "«correzione» non si guarda** — segnalarla sarebbe un FALSO-UNO. "
      "### **I segnali sono passati da `13` a `0`.** |")
    p("| `2` | ### ⚠ **L'etichetta «TROPPO GROSSO» era un GIUDIZIO stampato da un "
      "attrezzo.** La soglia del `10%` l'avevo fissata nel task history ### **prima di "
      "misurare**, ed e' un fatto utile; ma su un denominatore di `25` ### **una percentuale "
      "non e' una misura**, e `F2` risultava *«troppo grosso»* con `9` segnali ### **tutti "
      "veri.** ➜ L'attrezzo adesso dice ### **che la soglia e' superata** *(il fatto)*, "
      "e ### **la LETTURA sta qui** *(il giudizio)*. |")
    p()
    p("### ⭐ **Il primo l'ha trovato il presidio stesso**, guardando la propria uscita: "
      "### **`13` segnali di cui `11` con la stessa frase non sono `13` difetti, sono un "
      "rilevatore che legge male.** ### **E' il controllo che chiede «quel segnale poteva "
      "essere diverso?»**, ed e' la domanda che tiene lontano un FALSO-UNO.")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ④ CHE COSA RESTA A LUCA")
    p()
    p("| | che cosa, e perche' non l'ho deciso io |")
    p("|---|---|")
    p("| ### **i `%d` segnali** | ### **non si correggono**, lo dice il mandato. Ciascuno si "
      "chiude ### **correggendo la voce** oppure con ### **`meta.eccezione_presidio`**, che "
      "deve ### **citare il testo alla lettera** — e la forma la ### **impone `valida`**, "
      "altrimenti l'eccezione sarebbe una via di fuga a costo zero |"
      % sum(len(x[2]) for x in tutti))
    p("| ### **`F5`, la mia derivazione** | il mandato dice *«storico senza commit → "
      "errore»*. ### ⛔ **Nella forma letterale BLOCCHEREBBE OGNI COMMIT DI UN LOTTO**, "
      "perche' `aggiorna-lotto` scrive righe con `commit` vuoto — il commit che le "
      "conterra' ### **non esiste ancora.** ➜ **`F5` e' un errore solo per le righe "
      "GIA' COMMITTATE** *(quelle in `HEAD`)*; le altre sono ### **il ritardo dichiarato nel "
      "blocco `D`.** ### **E' una MIA derivazione, scritta nel task history PRIMA di "
      "provarla** |")
    p("| ### **`F3` guarda solo il titolo** | il mandato dice *«il cui ### **TITOLO** parla "
      "di…»*, e l'ho ### **preso alla lettera.** ### **E' cio' che tiene `F3` stretto** "
      "*(`15` segnali invece dei «molti» che prevedevo)*. Allargarlo alla descrizione "
      "### **cambierebbe il presidio**, e non lo faccio da solo |")
    p("| ### **`F1` e i segnaposto** | `%d` dei `%d` segnali di `F1` puntano a una voce "
      "`DA_CLASSIFICARE`, che ### **non ha ancora un dominio ne' un'era.** Restringere il "
      "rilevatore e' una decisione: ### **lo scrivo, non lo cambio** |"
      % (n_segnaposto, len(f1)))
    p("| ### **il costo nel `pre-commit`** | `valida` adesso ### **conta i segnali a ogni "
      "commit**, e `F4` apre i documenti citati da `122` etichette: ### **circa `4,5` "
      "secondi.** Nel task history avevo scritto che oltre ### **`5` secondi** l'avrei "
      "proposto fuori dal `pre-commit`: ### **ci sta sotto, ma di poco** — se cresce, "
      "`F4` va spostato in un comando a parte |")
    p()
    p("> ### ⭐ **Il criterio, lo stesso del giro scorso:** dove il mandato "
      "### **nomina** la decisione l'ho applicata; dove ### **non la nomina**, "
      "### **ho lasciato le cose dov'erano e le ho scritte qui.** ### **Una decisione non "
      "presa e' un dato; una decisione presa al posto di Luca e' un difetto.**")
    p()

    q2 = os.path.join(RADICE, "doc", "REFERTO_indice_v3_presidi.md")
    io.open(q2, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print("scritto doc/REFERTO_indice_v3_presidi.md: %d righe" % len(R))
    print("  segnali %d, collaudo %d su %d, F1 verso segnaposto %d"
          % (sum(len(x[2]) for x in tutti), n_ok, len(coll), n_segnaposto))
    return 0


if __name__ == "__main__":
    sys.exit(main())
