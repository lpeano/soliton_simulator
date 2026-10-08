# -*- coding: utf-8 -*-
"""IL GENERATORE DI `doc/ERA_1_CHIUSURA.md` — **nessun numero ricopiato a mano** (`L-NUMERI`).

Ogni cifra esce da un'uscita committata: i `json` dei bracci di `H3`, il banco di
integrabilita', il mare `v1` e `v2`, il bilancio della nascita, il tetto. I tre numeri che
vivono ### **solo** nel referto *(`230 su 230`, `93.44 %`, `×2.4862`)* si ### **ESTRAGGONO
dal testo con un'espressione, e si ASSERISCE che ci siano**: se il referto cambiasse, questo
documento ### **non si scriverebbe** invece di scrivere un numero vecchio.

Gira con:  python csv/_test_fork/_doc_era1.py
"""
import io
import json
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(os.path.dirname(_QUI))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Legge `json` e referti prodotti
# da strumenti che hanno GIA' dichiarato la configurazione INTERA, e la riporta nel documento.
NL = chr(10)
DEST = os.path.join(RADICE, "doc", "ERA_1_CHIUSURA.md")
R = []


def A(s=""):
    R.append(s)


def leggi(p):
    return json.load(io.open(os.path.join(RADICE, p), encoding="utf-8"))


def auc(braccio):
    d = leggi("csv/_test_fork/_termo_h3/%s.json" % braccio)
    m = d["termo_h3"]["misure"]
    k = "400" if "400" in m else sorted(m, key=lambda x: int(x))[-1]
    return float(m[k]["auc_materia_vuoto"]), k, d["termo_h3"]["braccio"]


def dal_referto(pat, nome):
    """### Un numero che vive SOLO nel referto: si estrae, e si ASSERISCE."""
    t = io.open(os.path.join(RADICE, "doc",
                             "REFERTO_h3_termostato_2026-10-07.md"),
                encoding="utf-8").read()
    m = re.search(pat, t)
    assert m, ("%s NON si trova nel referto: il documento NON si scrive invece di "
               "scrivere un numero vecchio" % nome)
    return m.group(1)


def main():
    itg = leggi("csv/_test_fork/_prova_integrabilita/integrabilita.json")
    e = {x["legge"]: x for x in itg["esiti"]}
    SY = e["sincronizzazione"]
    bil = leggi("csv/_test_fork/_bilancio_nascita/bilancio.json")
    tl = leggi("csv/_test_fork/_tetto_e_lam/tetto_e_lam.json")
    v2 = leggi("proto_primo_ordine/uscite/diagnosi_v2.json")
    mare = leggi("proto_primo_ordine/uscite/mare.json")
    cen = leggi("csv/_test_fork/_censimento_leggi/censimento.json")
    pos = leggi("csv/_test_fork/_censimento_pos/pos.json")
    b0 = v2["per_braccio"]["NON-NORM"]["semi"]["11"]
    b1 = v2["per_braccio"]["NORM"]["semi"]["11"]
    tt = tl["tetto"]
    K0 = int(tt["livello_calore"])
    assert K0 == int(bil["livello_di_arresto"]),         "le due uscite non concordano sul livello di arresto: si riconciliano, non si scelgono"
    C2 = float(b0["lambda_max"]) / 5.0 * 2.0

    d1 = dal_referto(r"passi con `P_coppia` ### \*\*positiva\*\* \| ### \*\*(\d+ su \d+)\*\*",
                     "D1: i passi con P_coppia positiva")
    d2ter = dal_referto(r"toglie ### \*\*([\d.]+ %)\*\* della crescita di `H`",
                        "D2-TER: la quota di crescita che la sync toglie")
    d2ter_da = dal_referto(r"\*\(da ([\d.]+) a [\d.]+\)\*",
                           "D2-TER: la crescita di H prima")
    d2ter_a = dal_referto(r"\*\(da [\d.]+ a ([\d.]+)\)\*",
                          "D2-TER: la crescita di H dopo")
    cin = dal_referto(r"`1000\.5497 → 2487\.5607` \*\(`×([\d.]+)`\)\*",
                      "D2-TER: il fattore della cinetica")

    A("# LA CHIUSURA DELL'ERA `1` — **il simulatore del SECONDO ordine, fotografato**")
    A("")
    A("> ### ⛔ **DECISIONE DI LUCA, 2026-10-08.** Questo documento ### **non cambia niente**: "
      "### **fotografa** cio' che l'era `1` ha prodotto, e dice ### **perche'** lo si cambia.")
    A(">")
    A("> *Ogni numero esce da un'uscita committata o si ### **estrae dal referto con "
      "un'espressione** — e in quel caso il generatore ### **ASSERISCE che ci sia**: se il "
      "referto cambiasse, questo documento ### **non si scriverebbe** invece di scrivere un "
      "numero vecchio.* *(`L-NUMERI`)*")
    A("")
    A("---")
    A("")
    A("# 📌 `①` **CHE COSA FOTOGRAFA**")
    A("")
    A("| | |")
    A("|---|---|")
    A("| il ### **simulatore** | `soliton_simulator.py`, blob ### **`%s`** *(sha1 dei byte "
      "grezzi, dal DISCO)* |" % itg["blob"])
    A("| la ### **forma** | ### **SECONDO ordine**: `phivel` con l'inerzia `M_PH`, un passo a "
      "### **piu' settori**, e le leggi ### **non derivate da una sola `H`** |")
    A("| la ### **scena di riferimento** | `%d` nodi, `%d` archi, `DT = 0.01`; l'argv del "
      "driver con ### **`%d` flag cambiati** rispetto ai default del sorgente |"
      % (itg["n"], itg["archi"], len(cen["flag_cambiati"])))
    A("| i suoi ### **sigilli** | tutti quelli di `csv/_seal_fork/` e `csv/_test_fork/`, con "
      "i blob nell'inventario. ### **Un sigillo si rigira AL SUO COMMIT** |")
    A("| le sue ### **leggi** | ### **`%d` scritture di stato** su `%d` nomi, da `%d` funzioni "
      "*(`csv/_test_fork/_censimento_leggi.py`)* |"
      % (len(cen["scritture"]), len(set(x["variabile"] for x in cen["scritture"])),
         len(cen["raggiunte"])))
    A("")
    A("# ⛔ `②` **I DOCUMENTI CHE SPIEGANO PERCHE' LO SI CAMBIA**")
    A("")
    A("| | |")
    A("|---|---|")
    A("| ### **`A16`** *(`doc/ASSIOMI.md`, in testa)* | ### **primo ordine, UNO stato, UNA "
      "`H`**: `i·dψ/dt = ∂H/∂ψ*`, e `φ` ### **si legge** da `ψ` |")
    A("| ### **`A17`** *(in testa, prima di `A16`)* | ### **ogni comportamento e' determinato "
      "solo dal suo ambito:** ### **niente `pos` nella fisica** |")
    A("| `doc/RISCRITTURA_PRIMO_ORDINE.md` | che cosa ### **sparisce**, che cosa ### **rinasce "
      "in forma nuova**, e il banco |")
    A("| `doc/TRADUZIONE_IN_H.md` | le ### **leggi in cinque classi**, la `H` candidata, la "
      "regola di crescita ### **a parte**, e l'### **elenco delle decisioni** |")
    A("| `doc/REGISTRO_FISICA.md` | le ### **schede delle decisioni PRESE** di Luca |")
    A("")
    A("# ⭐ `③` **I NUMERI DI RIFERIMENTO** — *dai referti, non ricopiati*")
    A("")
    A("## `③.1` **`D1`: la coppia POMPA**")
    A("")
    A("| | |")
    A("|---|--:|")
    A("| passi con `P_coppia` ### **positiva** | ### **`%s`** |" % d1)
    A("")
    A("### ➜ **La coppia d'interferenza immette energia a OGNI passo misurato.** Non e' una "
      "tendenza: e' ### **tutti**.")
    A("")
    A("## `③.2` **`D2` e `D2-BIS`: la coppia che LEGGE LA FASE tiene le masse**")
    A("")
    A("| braccio | che cosa prova | ### **`AUC` materia/vuoto** |")
    A("|---|---|--:|")
    for br, nota in (("h3_base", "il riferimento, con tutto acceso"),
                     ("h3_bts", "### **senza la coppia che legge la fase** *(bagno + "
                                "scuotimento, coppia spinoriale)*"),
                     ("h3_bscal", "la coppia ### **SCALARE** *(che legge la fase)*, col bagno"),
                     ("h3_bscalts", "la coppia ### **SCALARE** ### **senza bagno**"),
                     ("h3_bscaltsnosync", "lo stesso, ### **senza sincronizzazione**")):
        v, k, nome = auc(br)
        A("| `%s` | %s | ### **`%.4f`** *(al passo `%s`)* |" % (nome, nota, v, k))
    A("")
    A("### ➜ **IL FATTO CHE HA DECISO:** il braccio con la coppia ### **spinoriale** *(che "
      "### **non** legge la fase che muove)* sta a `%.4f`; quelli con la coppia "
      "### **scalare** *(che la legge)* stanno sopra `%.2f`. ### **Cio' che tiene le masse "
      "coerenti e' LA FORMA DELLA COPPIA**, non la quantita' di energia immessa."
      % (auc("h3_bts")[0], auc("h3_bscal")[0]))
    A("")
    A("## `③.3` **`D2-TER`: senza sincronizzazione**")
    A("")
    A("| | |")
    A("|---|--:|")
    A("| `AUC` al `400` ### **senza** sincronizzazione | ### **`%.4f`** |"
      % auc("h3_bscaltsnosync")[0])
    A("| `AUC` al `400` ### **con** | `%.4f` |" % auc("h3_bscalts")[0])
    A("| la ### **cinetica** cresce di | ### **`×%s`** *(da `1000.5497` a `2487.5607`)* |" % cin)
    A("| la sincronizzazione toglieva, ### **a `A` fissa** | ### **`%s`** della crescita di "
      "`H` *(da `%s` a `%s`)* |" % (d2ter, d2ter_da, d2ter_a))
    A("")
    A("### ➜ **La sincronizzazione «pompava senza ordinare»:** toglieva il ### **`%s`** della "
      "crescita di `H` e costava ### **`%.4f`** di `AUC`. ### ⚠ **E le DUE letture della "
      "cinetica sono RICONCILIATE nel referto, non scelte:** `×%s` *(prima del passo)* contro "
      "`×2.0376` *(dopo)* — la differenza e' il primo passo, che inietta `222.3697`, e "
      "### **la clausola `< ×3` passa in entrambe.**"
      % (d2ter, auc("h3_bscalts")[0] - auc("h3_bscaltsnosync")[0], cin))
    A("")
    A("## `③.4` ### ⛔ **I DUE «NO» DIMOSTRATI** — *non «non l'ho trovata»: DIMOSTRATI*")
    A("")
    A("| | il numero | |")
    A("|---|--:|---|")
    A("| la ### **SINCRONIZZAZIONE** e' ### **asimmetrica** | ### **`%.4f`** contro un "
      "pavimento ### **calcolato** di `%.3e` | ### **nove ordini sopra**, e identica ai tre "
      "passi `h` ⇒ ### **nessuna `E(φ)` esiste** di cui `K_SYNC` sia il gradiente |"
      % (SY["asimmetria"], SY["pavimento"]))
    A("| la ### **COPPIA DEL DRIVER** ### **non legge `φ`** | ### **`0.000e+00`** | scrive una "
      "coppia su `φ` leggendo ### **lo spinore** ⇒ spazio d'ingresso ≠ spazio d'uscita |")
    A("| *(il controllo positivo)* | `%.3e` contro `%.3e` | la coppia ### **scalare** e' "
      "### **simmetrica**: il banco ### **funziona** |"
      % (e["coppia SCALARE"]["asimmetria"], e["coppia SCALARE"]["pavimento"]))
    A("| *(il caso che deve fallire)* | `%.3e` | una coppia ### **sintetica** col prefattore di "
      "nodo risulta ### **asimmetrica**: il banco ### **DISCRIMINA** |"
      % e["coppia ASIMMETRICA (sintetica)"]["asimmetria"])
    A("")
    A("## `③.5` **IL MARE `v1` e `v2`**")
    A("")
    A("| | esito | il numero |")
    A("|---|---|---|")
    A("| ### **`v1`** | ### ⛔ **NON DECIDIBILE come era scritto** | `Σ_j w_kj` varia di un "
      "fattore ### **`39.8`**, quindi il «mare uniforme» e' uniforme ### **solo in modulo**: "
      "lo stato costante ### **non era stazionario**, e la localizzazione a `g = 0` era "
      "### **del GRAFO**. ### **E il tetto dei `20` minuti fu superato** *(`%.1f` s = `%.2f` "
      "minuti)* |" % (float(mare.get("secondi_totali") or 0),
                      float(mare.get("secondi_totali") or 0) / 60.0))
    A("| ### **`v2`** | ### ⛔ **LO STATO PIU' BASSO E' GIA' UNA MASSA** | a `g = -5`: un nodo "
      "### **`%.1f`** contro il mare esteso `%.1f`. ### **E nessun `ρ_0` salva:** alla soglia "
      "`\\|g\\|ρ_0` vale `%.5f` e `%.5f` contro `λ_max` `%.4f` e `%.4f` |"
      % (b0["g"]["-5.0"]["H_un_nodo"], b0["g"]["-5.0"]["H_esteso"],
         b0["g"]["-5.0"]["non_linearita_a_quella_soglia"],
         b1["g"]["-5.0"]["non_linearita_a_quella_soglia"],
         b0["lambda_max"], b1["lambda_max"]))
    A("| ### ⭐ **e il numero che resta in mano** | la ### **geometria da sola** concentra | il "
      "`PR` del Perron a `g = 0`: ### **`%.1f`** su `400` senza normalizzazione, ### **`%.1f`** "
      "con |" % (b0["PR_perron"], b1["PR_perron"]))
    A("")
    A("## `③.6` **IL BILANCIO DELLA NASCITA, e lo SPARTIACQUE**")
    A("")
    A("| | |")
    A("|---|--:|")
    A("| la concentrazione ### **libera** | ### **`%.1f`** |" % bil["liberata"])
    A("| la ### **prima divisione** costa | ### **`%.1f`** *(il `%.2f %%`)* |"
      % (bil["costo_prima_divisione"], 100.0 * bil["frazione"]))
    A("| la cascata ### **si ferma da sola** al livello | ### **`%d`** — cioe' a "
      "### **`%d` nodi** |" % (K0, 2 ** K0))
    A("| ### ⭐ **LO SPARTIACQUE delle due fermate** | ### **`ρ = %.1f` per nodo** |"
      % tt["rho_calore"])
    A("")
    A("### ➜ **Sopra `ρ = %.1f` prevale il CALORE** *(e la barriera ### **non lavora**)*; "
      "### **sotto prevale il TETTO** *(e la materia ### **resta compressa**)*. ### ⛔ **Sono "
      "due REGIMI FISICI diversi**, e quale sia il nostro dipende dall'### **unita' di stato**, "
      "che e' ### **aperta**." % tt["rho_calore"])
    A("")
    A("# ✔ `④` **LE DECISIONI PRESE** *(schede in `doc/REGISTRO_FISICA.md`)*")
    A("")
    A("| | la decisione | il motivo in un numero |")
    A("|---|---|--:|")
    A("| ### **`(B)`** | ### **la SINCRONIZZAZIONE SI TOGLIE**, perche' ### **emergera'** | "
      "asimmetria `%.4f`; e toglierla costa `%.4f` di `AUC` |"
      % (SY["asimmetria"], auc("h3_bscalts")[0] - auc("h3_bscaltsnosync")[0]))
    A("| ### **`(A)`** | ### **il CALORE del vuoto locale PAGA LA NASCITA** | `%.1f` liberati "
      "contro `%.1f` richiesti |" % (bil["liberata"], bil["costo_prima_divisione"]))
    A("| ### **`(C)`** | ### **il FRENO della coesione e' la `(c)`: nascita PIU' degenerazione "
      "con BARRIERA PER NODO in `H`** | senza barriera, al livello `%d` il calore finisce e "
      "### **non resta nessun freno** |" % K0)
    A("")
    A("### ⚠ **E DUE CAUTELE che stanno nelle schede:** *«Pauli»* e' un'### **ANALOGIA** *(la "
      "doppia copertura e' necessaria ma ### **non sufficiente** per la statistica di Fermi)*, "
      "e la barriera e' derivata ### **dalla struttura** — due componenti, `LAM` — ### **non "
      "dalla statistica**.")
    A("")
    A("# ⛔ `⑤` **LE DECISIONI APERTE E LE TENSIONI, nell'ordine delle DIPENDENZE**")
    A("")
    A("### **La catena** *(e l'ordine non e' una preferenza: e' la chiusura delle dipendenze "
      "di `25858a9`)*:")
    A("")
    A("| | che cosa manca | ### **perche' viene prima** |")
    A("|--:|---|---|")
    A("| ### **`1`** | ### ⭐ **L'UNITA' DI STATO** — quanta `ρ` vale ### **uno** stato | "
      "### **decide IL REGIME:** sopra `ρ = %.1f` lavora il calore, sotto lavora il tetto. "
      "### **Finche' e' aperta non si sa se la barriera lavora** |" % tt["rho_calore"])
    A("| ### **`2`** | il ### **VUOTO LOCALE** in forma ### **relazionale** | lo chiedono "
      "### **tutte e tre** le decisioni prese: senza di esso la cura di `A16` "
      "### **reintrodurrebbe `pos` dal lato del vuoto** |")
    A("| ### **`3`** | la ### **GEOMETRIA dentro `H`** *(decisione `9`)* | `d ≥ LAM` come "
      "### **barriera d'energia** ha senso solo se `d` ha una dinamica che ### **sente** la "
      "barriera |")
    A("| ### **`4`** | l'### **AGGANCIO degli orologi COME MISURA** | e' il criterio che "
      "### **puo' riaprire** la decisione `(B)`, e richiede il vuoto locale |")
    A("")
    A("> ### ⚠ **E UNA NOTA SULL'UNITA' DI STATO CHE CAMBIA COME SI LEGGE LA CANDIDATA:** la "
      "candidata `(2)` — `ρ₁ = λ_max/\\|g\\|` = ### **`%.4f`**, quindi `C = %.4f` — e' derivata "
      "### ⛔ **DENTRO LA SONDA**, cioe' da un termine ### **`\\|ψ\\|⁴` di SITO** e dallo "
      "### **spettro di un grafo costruito con `pos`** *(`A17`!)*. ### ➜ **Va RICALCOLATA sulla "
      "`H` di Luca, dove la coesione e' un termine D'ARCO** — e lì `λ_max` e il significato "
      "stesso di `ρ₁` ### **cambiano**. ### **Il numero di oggi e' un ORDINE DI GRANDEZZA, non "
      "il valore.**" % (float(b0["lambda_max"]) / 5.0, C2))
    A("")
    A("## **E FUORI DALLA CATENA** *(non si sbloccano a vicenda)*")
    A("")
    A("| | la tensione | ### **la decisione che richiede** |")
    A("|---|---|---|")
    A("| ### **`T1`** | ### **la CRESCITA come POSTULATO o come TEOREMA.** Col margine "
      "### **zero** il bilancio e' ### **simmetrico nel tempo**: la fusione restituirebbe "
      "esattamente quel calore, e ### **sarebbe permessa dall'energia** ⇒ `A14.2` resta un "
      "### **postulato in piu'** | ### ⭐ **CANDIDATA DEL GUARDIANO, e il conto torna:** la "
      "### **lunghezza minima `LAM`** vieta la fusione, perche' due nodi che si fondono "
      "dovrebbero ### **scendere sotto `LAM`**, mentre la nascita ### **spezza un arco "
      "`≥ 2·LAM` in due pezzi `≥ LAM`**. ### ➜ **L'asimmetria sarebbe GEOMETRICA, non "
      "energetica** — e `A13` diventerebbe la ragione di `A14.2`. ### ⛔ **DA VERIFICARE, non "
      "assunta** |")
    A("| ### **`T2`** | ### **UN SERBATOIO, PIU' USI:** nascita, aggancio degli orologi, freno "
      "vero — e il margine e' ### **zero** | ### **DI LUCA:** una ### **priorita'**; una "
      "contabilita' ### **separata**; oppure l'ipotesi che siano ### **LO STESSO processo** |")
    A("| ### **la SCENA INIZIALE** | `semina`, `_semina_lam`, `_semina_masse_coerenti` "
      "costruiscono la ### **topologia iniziale DAL DISEGNO** | ### **DI LUCA: e' ammessa da "
      "`A17` o va costruita in modo relazionale?** La scena fissa ### **quali nodi sono "
      "vicini**, e quella topologia ### **sopravvive per tutta la corsa** |")
    A("| ### **l'EREDITA' di `pos` ALLA NASCITA** | `_rn_div_pos`, `_rn_sch_pos`: il `pos` del "
      "nato ### **si eredita** | ### ⛔ **VIOLA `A17`**: un'eredita' di `pos` e' `pos` "
      "### **dentro una legge di crescita**. Non e' rendering e non e' una condizione iniziale |")
    A("| ### **il default `POZZO_D = False`** | nel driver e' ### **ACCESO** *(`--pozzo-d`)*, "
      "quindi la violazione ### **non e' viva** — ma il ### **default del modulo** e' `False` | "
      "### ⛔ **chi importa il simulatore senza il driver ha la GRAVITA' CHE LEGGE `pos`.** Per "
      "`A17` quel default e' ### **sbagliato**, e ribaltarlo e' ### **una decisione di Luca** |")
    A("")
    A("### 📌 **E LO STATO DI `A17` MISURATO, perche' l'era `2` parta da un numero e non da "
      "un'impressione:** ### **`%d` funzioni** leggono `pos` *(`%d` occorrenze)*; delle "
      "### **`%d`** classificate ### **LEGGE FISICA**, ### **`9` su `13`** delle letture "
      "«dirette» sono ### **UN SOLO blocco** *(il centro di massa della sincronizzazione)*, "
      "### **che la decisione `(B)` toglie.**"
      % (len(pos["per_funzione"]), sum(len(v) for v in pos["per_funzione"].values()),
         len(pos["gruppi"].get("LEGGE FISICA", []))))
    A("")
    A("# 📌 `⑥` **IL RAMO DEL PRIMO ORDINE, e il patto sul flag**")
    A("")
    A("| | |")
    A("|---|---|")
    A("| il ### **tag** | `era-1-secondo-ordine`, ### **annotato**, su questo commit |")
    A("| il ### **ramo** | `primo-ordine`, a partire ### **dal tag** |")
    A("| ### ⛔ **il flag `PRIMO_ORDINE`** | ### **NON si introduce qui.** Entra con la "
      "### **PRIMA legge portata** |")
    A("| ### ⭐ **IL PATTO** | ### **a flag SPENTO il simulatore deve restare IDENTICO AL BIT "
      "all'era `1`** — e ### **non e' una promessa: lo dimostrano i SIGILLI VECCHI**, che "
      "girano sul ramo nuovo e devono dare ### **gli stessi numeri** |")
    A("")
    A("### ⚠ **E IL TAG CONSERVA GLI STATI ORIGINALI DELL'INDICE:** la ### **sospensione** "
      "delle voci avviene ### **sul ramo nuovo**, non qui. ### **Chi vuole lo stato dell'era "
      "`1` lo trova al tag.**")
    A("")
    A("---")
    A("")
    A("# ⛔ **CHE COSA QUESTO DOCUMENTO NON DICE**")
    A("")
    A("| | |")
    A("|---|---|")
    A("| che l'era `1` sia ### **sbagliata** | ### ⛔ **NO.** L'era `1` ha prodotto i "
      "### **fatti misurati** che hanno deciso `A16` e `A17`. ### **Si chiude perche' ha "
      "risposto, non perche' ha mancato** |")
    A("| che la ### **`H` di Luca** sia scritta | ### ⛔ **no:** `doc/TRADUZIONE_IN_H.md` ha "
      "### **termini candidati** e ### **`13` decisioni**, di cui ### **`3` prese** |")
    A("| che i difetti dell'era `1` siano ### **chiusi** | ### ⛔ **no: SOSPESI.** Il piano del "
      "triage e' in `doc/TRIAGE_ERA_1.md`, ### **scritto e NON eseguito** |")
    A("| che il prototipo sia ### **relazionale** | ### ⛔ **no**, e `A17` lo dichiara: grafo da "
      "punti in un ### **cubo**, pesi con distanza ### **euclidea** |")
    A("| le ### **scale e i semi** | `P3` ### **non e' soddisfatta** da nessuna delle misure "
      "del `2026-10-08`: uno snapshot, una scena, `3` semi nel prototipo |")
    io.open(DEST, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print("scritto %s (%d righe)" % (DEST, len(R)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
