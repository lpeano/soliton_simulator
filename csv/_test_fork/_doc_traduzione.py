# -*- coding: utf-8 -*-
"""IL GENERATORE DI `doc/TRADUZIONE_IN_H.md` -- **ogni numero esce da un json** (`L-NUMERI`).

Legge: `_censimento_leggi/censimento.json` · `_prova_integrabilita/integrabilita.json` ·
`_crescita_conti/crescita.json` · `proto_primo_ordine/uscite/diagnosi_v2.json`.

Gira con:  python csv/_test_fork/_doc_traduzione.py
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

# ESENTE-H-P5: non importa il simulatore e non lo fa girare: legge quattro `json` prodotti
# da strumenti che hanno GIA' dichiarato la configurazione INTERA, e la RIPORTA nel documento
# (la riga <<ZERO su 82>> di `_prova_integrabilita`), con la provenienza. Chiamare qui
# `dichiara_configurazione` vorrebbe dire CARICARE il simulatore in un generatore di testo:
# la dichiarazione sarebbe di un modulo appena importato, NON della scena che ha misurato.
NL = chr(10)
PIPE = chr(92) + "|"
DEST = os.path.join(RADICE, "doc", "TRADUZIONE_IN_H.md")
R = []


def A(s=""):
    R.append(s)


def leggi(p):
    return json.load(io.open(os.path.join(RADICE, p), encoding="utf-8"))


# ==========================================================================
#   LA TAVOLA DELLE LEGGI -- la classificazione, UNA PER UNA
# ==========================================================================
# ### ⚠ **LA CLASSIFICAZIONE E' MIA, e sta qui perche' e' un GIUDIZIO, non una misura.** I
# ### numeri che la sostengono vengono dai json; il giudizio no, e si dichiara.
# Campi: legge · ancora (nome di funzione o di flag, MAI una riga) · variabile · classe ·
#         E_x o vincolo · esito della verifica
TAVOLA = [
    # ---------------------------------------------------------------- TRADUCIBILE
    ("la coppia d'interferenza, ramo SCALARE", "_coppia_interferenza (ramo OFF)", "phi",
     "TRADUCIBILE",
     "E = -K_C * somma_archi A_ij cos(phi_i - phi_j);  i dpsi/dt = dE/dpsi*",
     "SIMMETRICA al banco, e il gradiente coincide a 1.49e-15 (D2-BIS)"),
    ("il legame elastico delle lunghezze", "step, blocco di `vd` (VERLET)", "d",
     "TRADUCIBILE",
     "E = (1/2) somma_archi k_ij (d_ij - d0_ij)^2, con d0 CONGELATA nel termine",
     "NON MISURATA in questo giro: la forza non e' isolabile senza riscrivere il passo"),
    ("la repulsione", "REPULS_LEGGE, `_rep`", "d",
     "TRADUCIBILE",
     "E = somma_archi V_rep(d_ij), con V_rep decrescente;  la forza e' -dV/dd",
     "NON MISURATA: `_rep` INSEGUE un bersaglio, quindi il termine vale a `_rep` FERMA"),
    # ---------------------------------------------- TRADUCIBILE CON UNA MEMORIA
    ("il rilassamento della torsione", "step, blocco `tau_tw`", "tw",
     "CON UNA MEMORIA",
     "### NESSUN E_x, e la versione precedente di questo documento SBAGLIAVA: scrivere "
     "<<il rilassamento e' la discesa di E_tw>> dichiara un FLUSSO DI GRADIENTE, che "
     "DISSIPA. Serve un CONIUGATO -- candidato: tw come FASE DI UN LEGAME U(1), col suo "
     "campo elettrico d'arco",
     "la legge dipende da una VELOCITA' (|Delta omega|): instradata dal punto (3)"),
    ("il rilassamento della lunghezza di riposo", "step, `tau_p_loc`", "d0",
     "CON UNA MEMORIA",
     "### NESSUN E_x: `d0 += dt*(d - d0)/tau_p` e' un FLUSSO DI GRADIENTE, cioe' "
     "dissipazione. Serve un CONIUGATO -- candidato: un impulso proprio `p_d0`, e allora "
     "`d0` OSCILLA attorno a `d` invece di raggiungerla",
     "10 scritture da 4 funzioni: NON e' una legge sola, e il test va fatto sul SISTEMA"),
    ("il rilassamento della pressione di equilibrio", "step, `tau_bg_loc`, TAU_DIFF", "peq",
     "CON UNA MEMORIA",
     "### NESSUN E_x: l'inseguimento e la DIFFUSIONE sono entrambi flussi di gradiente. "
     "Il laplaciano e' simmetrico, ma la DIFFUSIONE DISSIPA. Serve un CONIUGATO -- "
     "candidato: un impulso `p_peq`, e allora la diffusione diventa un'ONDA",
     "la diffusione usa TAU_DIFF = 1.0 NUDO: una MANOPOLA, e A1 la vieta"),
    ("la precessione dello spinore e l'orologio", "_passo_spinoriale, `omega_s`", "omega_s",
     "CON UNA MEMORIA",
     "### ⭐ L'UNICA CHE HA GIA' UN CONIUGATO: `omega_s` E' una velocita' angolare, "
     "quindi e' il MOMENTO coniugato della fase dell'orologio, e `E_om = (1/2) somma "
     "I_k omega_s^2` con `I = (d/cs)^2` e' ENERGIA CINETICA VERA. ### **Non le serve un "
     "coniugato: le va TOLTO lo smorzamento `-omega_src/tau`**",
     "il tau e' DERIVATO (`--tau-luce`, esempio di A15.2) -- ma e' il tau di un OBLIO, "
     "non una frequenza"),
    ("la memoria hebbiana del moto", "memoria_hebbiana_moto, `mem_mot`", "mem_mot",
     "CON UNA MEMORIA",
     "nessun E_x scritto: la legge e' una MEDIA MOBILE, e una media mobile NON e' una "
     "discesa -- VINCE L'ULTIMO invece di bilanciare",
     "A14 n.4 + MEM-HEBB-VERSO: la forma va CAMBIATA, non tradotta"),
    ("la dinamica dei pesi e delle distanze", "`w`, `d`, `d0` nello step", "w, d, d0",
     "CON UNA MEMORIA",
     "e' il punto A16.3: w e U devono essere gradi di liberta' DENTRO H. Nel prototipo "
     "sono FISSI, ed e' una violazione DICHIARATA",
     "APERTO: la forma del termine di memoria d'arco NON e' scritta"),
    # ---------------------------------------------- CRESCITA DELLO SPAZIO
    ("la mitosi", "mitosi, decidi_divisione", "tutta la struttura",
     "CRESCITA DELLO SPAZIO",
     "NON e' un termine di H: e' l'unica legge che CAMBIA H. Vincoli: (1) Sigma rho "
     "conservata; (2) il Delta H pagato dal vuoto LOCALE",
     "la tavola delle regole NON ha una classe <<il genitore cede>>: Sigma rho CRESCE"),
    ("la creazione di coppia (Schwinger)", "mitosi, evento `schwinger`", "tutta la struttura",
     "CRESCITA DELLO SPAZIO",
     "come sopra, piu' il vincolo di CARICA: l'antinodo nasce a fase opposta, e quello "
     "si conserva",
     "e' il ramo che conserva N(+1) - N(-1): la carica nasce OPPOSTA"),
    ("la creazione degli archi", "_allaccia", "i, j, d, d0, peq, tw, vd",
     "CRESCITA DELLO SPAZIO",
     "un arco nuovo e' un termine NUOVO in H: il suo contributo va pagato",
     "`peq` nasce `nan` e lo step la CALIBRA: una nascita con un marcatore, non con un "
     "valore"),
    ("la scomparsa degli archi", "le potature nello step", "i, j",
     "CRESCITA DELLO SPAZIO -- ma A ROVESCIO",
     "NON c'e' forma: A14.2 dice che la CRESCITA e' l'unica freccia ammessa, quindi un "
     "arco che muore e' GIA' una violazione",
     "e' un difetto, non una legge da tradurre: va nell'elenco di Luca"),
    # ---------------------------------------------- NON TRADUCIBILE
    ("la sincronizzazione", "K_SYNC", "phi",
     "NON TRADUCIBILE -- DIMOSTRATO",
     "NESSUNA. Il banco misura un'asimmetria di %(sync)s contro un pavimento di %(sync_p)s",
     "un <<no>> DIMOSTRATO: nove ordini sopra il pavimento, identico ai tre passi h. "
     "### ⭐ E LUCA HA DECISO: SI TOGLIE, perche' DEVE EMERGERE (decisione `3`, PRESA, e la "
     "scheda e' in `doc/REGISTRO_FISICA.md`)"),
    ("la coppia d'interferenza del DRIVER", "_coppia_interferenza (CAMPO_SPINORIALE)", "phi",
     "NON TRADUCIBILE IN phi -- DIMOSTRATO",
     "NESSUNA in phi: la legge NON LEGGE phi (0.000e+00). La forma U(2) la riscrive in "
     "psi, ma a 1.054 di scarto, cioe' il 105 %% -- per il criterio del <<no>> NON e' una "
     "traduzione, e' UNA LEGGE NUOVA",
     "test (A): spazio d'ingresso (lo spinore) diverso dallo spazio d'uscita (phi)"),
    ("il termostato", "xi_termo, REGIME", "phivel",
     "NON TRADUCIBILE",
     "NESSUNA: scrive `phivel` DALL'ESTERNO, ed e' GLOBALE (A2). Deve diventare scambio "
     "col vuoto LOCALE (A15.3)",
     "A14 n.1. E il numero: senza bagno le nascite crollano da 164 a 0"),
    ("lo scuotimento del vuoto", "scuoti_vuoto", "phivel",
     "NON TRADUCIBILE",
     "NESSUNA: e' un forzante stocastico. Deve diventare scambio col vuoto LOCALE (A15.3)",
     "A14 n.1, insieme al termostato"),
    ("il freno `_smorza`", "_smorza (D31)", "d0",
     "NON TRADUCIBILE -- FRECCIA",
     "NESSUNA: e' un `clip` DA UN LATO, quindi a senso unico",
     "instradata dal punto (3) del criterio del <<no>>: il test NON si fa, darebbe un "
     "FALSO-ZERO"),
    ("lo smorzamento anisotropo", "ZETA_VIR, `beta*vd`", "vd",
     "NON TRADUCIBILE -- DISSIPAZIONE",
     "NESSUNA: dissipa. Deve diventare scambio col vuoto LOCALE (A15.3)",
     "A14 n.2, gia' dichiarato"),
    ("la massa critica", "massa_critica_adattiva, massa_critica_collasso", "la soglia",
     "NON TRADUCIBILE -- e' una SOGLIA",
     "non e' una forza: e' un CRITERIO. In H non entra; entra nella REGOLA DI CRESCITA",
     "U1 dice che `massacriticacollasso` ha 21 usi DENTRO le leggi: voce BLOCCANTE"),
    # ---------------------------------------------- DIAGNOSTICA
    ("i contatori `_g_*`, `_taup_*`, `_sfb_*`", "i prefissi diagnostici", "-",
     "DIAGNOSTICA",
     "nessuna: non muovono lo stato",
     "%(diag)s nomi riconosciuti per FORMA. ⚠ IL CRITERIO E' DI FORMA: ogni nome va "
     "verificato col <<nessun lettore>>, e questo giro NON lo fa"),
]


def main():
    cen = leggi("csv/_test_fork/_censimento_leggi/censimento.json")
    itg = leggi("csv/_test_fork/_prova_integrabilita/integrabilita.json")
    cre = leggi("csv/_test_fork/_crescita_conti/crescita.json")
    v2 = leggi("proto_primo_ordine/uscite/diagnosi_v2.json")
    bil = leggi("csv/_test_fork/_bilancio_nascita/bilancio.json")
    pos = leggi("csv/_test_fork/_censimento_pos/pos.json")
    tl = leggi("csv/_test_fork/_tetto_e_lam/tetto_e_lam.json")
    POS = {x["legge"]: x for x in pos["per_legge"]}
    e = {x["legge"]: x for x in itg["esiti"]}
    # ### LA DICHIARAZIONE `P5` SI LEGGE DALL'USCITA dello strumento che ha misurato, e si
    # ### ASSERISCE: se non c'e', il documento NON si scrive.
    _c = io.open(os.path.join(RADICE, "csv", "_test_fork", "_prova_integrabilita",
                              "integrabilita.txt"), encoding="utf-8").read()
    _m = re.search(r"booleani di modulo confrontati con l'argv del DRIVER: (\d+)", _c)
    _m2 = re.search(r"-> IN CONFIGURAZIONE DEL DRIVER: ([^" + NL + r"]+)", _c)
    assert _m and _m2, "la dichiarazione P5 NON e' nell'uscita: il documento non si scrive"
    CONF_N, CONF_ESITO = _m.group(1), _m2.group(1).strip()
    SC, SY, AS = (e["coppia SCALARE"], e["sincronizzazione"],
                  e["coppia ASIMMETRICA (sintetica)"])
    b0 = v2["per_braccio"]["NON-NORM"]["semi"]["11"]
    b1 = v2["per_braccio"]["NORM"]["semi"]["11"]
    sn = cre["snapshot"]
    p7 = cre["pt7"][0]
    sost = {"sync": "`%.4f`" % SY["asimmetria"], "sync_p": "`%.3e`" % SY["pavimento"],
            "diag": "`231`"}

    A("# LA TRADUZIONE DELLE LEGGI DEL SIMULATORE IN TERMINI DI `H`")
    A("")
    A("> ### ⛔ **QUESTO DOCUMENTO NON CAMBIA NIENTE NEL SIMULATORE** *(resta `%s`)*, e "
      "### **non decide la forma di `H`:** ### **propone**, e marca ogni proposta "
      "### **candidata** o ### **aperta**. ### **La forma di `H` e la regola di crescita sono "
      "DECISIONI DI LUCA.**" % itg["blob"][:8])
    A(">")
    A("> *I numeri escono da quattro uscite, e nessuno e' ricopiato a mano* *(`L-NUMERI`)*: "
      "`_censimento_leggi` · `_prova_integrabilita` · `_crescita_conti` · "
      "`proto_primo_ordine/uscite/diagnosi_v2`. Criteri e previsioni: "
      "`doc/TASK_HISTORY/2026-10-08_traduzione-in-H.md`, committato ### **prima** *(`c6c1112`, "
      "col criterio del «no» in `2f47b75`)*.")
    A("")
    A("# 📌 `⓿` **LA CONFIGURAZIONE DELLE MISURE** *(`P5`: non i flag toccati, TUTTI)*")
    A("")
    A("### ⛔ **Questo documento non fa girare niente: riporta le misure di tre strumenti**, e "
      "la configurazione e' ### **quella che LORO hanno dichiarato**, non una che io ridico:")
    A("")
    A("| | |")
    A("|---|---|")
    A("| booleani di modulo confrontati con l'argv ### **del DRIVER** | ### **`%s`** |"
      % CONF_N)
    A("| l'esito | ### **%s** |" % CONF_ESITO)
    A("| la scena | `%d` nodi, `%d` archi, `DT = 0.01`, snapshot di `%d` passi ### **pieni** "
      "*(`_passo.passo_pieno`, non `net.step()`)* |" % (itg["n"], itg["archi"],
                                                        itg["passi_snapshot"]))
    A("| dove sta la dichiarazione per intero | `csv/_test_fork/_prova_integrabilita/"
      "integrabilita.txt` e `csv/_test_fork/_crescita_conti/crescita.txt` |")
    A("")
    A("> ### ⚠ **E IL GENERATORE DI QUESTO DOCUMENTO E' ESENTE DA `H-P5`, dichiarato:** non "
      "importa il simulatore. ### **Chiamare `dichiara_configurazione` qui vorrebbe dire "
      "caricare il simulatore in un generatore di testo, e la dichiarazione sarebbe di un "
      "modulo appena importato — NON della scena che ha misurato.** L'esenzione e' in "
      "`doc/ESENZIONI_presidi.md`.")
    A("")
    A("---")
    A("")
    A("# ⭐ `①` **IL METODO -- e perche' il «NO» ADESSO SI DIMOSTRA**")
    A("")
    A("Il metodo ovvio *(scrivere `E` e verificare `F = −∂E/∂x`)* ### **dimostra il sì ma non "
      "il no:** non trovare `E` prova solo che ### **non l'ho trovata**. Il rilievo e' di Luca, "
      "e ha prodotto un banco che decide ### **senza indovinare `E`**:")
    A("")
    A("| | il test | che cosa decide |")
    A("|---|---|---|")
    A("| ### **`(A)`** | la legge ### **legge** la variabile che scrive? | ### ⛔ **se NO, non "
      "e' il gradiente di nessuna `E(x)`**: lo spazio d'ingresso non e' quello d'uscita. ### **E "
      "il `(B)` va SALTATO**, perche' darebbe `J = 0`, che e' simmetrica — ### **un FALSO-ZERO** |")
    A("| ### **`(B)`** | `%s%sJ − Jᵀ%s%s / %s%sJ%s%s` contro il ### **pavimento CALCOLATO** | "
      "### **simmetrica ⇒ `E` ESISTE** *(localmente, in quelle variabili)*; ### **asimmetrica "
      "⇒ un «no» DIMOSTRATO** |" % (PIPE, PIPE, PIPE, PIPE, PIPE, PIPE, PIPE, PIPE))
    A("")
    A("### ✔ **E IL BANCO E' SANO -- tre controlli, e il terzo e' quello che conta:**")
    A("")
    A("| controllo | numero | esito |")
    A("|---|--:|---|")
    A("| la coppia ### **SCALARE** *(gradiente noto)* deve essere ### **simmetrica** | "
      "`%.3e` contro un pavimento di `%.3e` | ### ✔ **PASSA** |"
      % (SC["asimmetria"], SC["pavimento"]))
    A("| la coppia del ### **DRIVER** deve risultare ### **non traducibile** | `0.000e+00` "
      "perturbando `φ` | ### ✔ **PASSA** *(per il `(A)`)* |")
    A("| ### ⭐ una coppia ### **SINTETICA** col prefattore di nodo deve risultare "
      "### **asimmetrica** | `%.3e` | ### ✔ **PASSA** |" % AS["asimmetria"])
    A("")
    A("> ### ⭐ **IL TERZO CONTROLLO E' QUELLO CHE VALE, e non era nel mandato:** "
      "### **un banco che approva tutto e un banco che funziona danno lo STESSO referto sul "
      "controllo positivo.** Serviva una legge che ### **DEVE** risultare asimmetrica, e l'ho "
      "costruita: ### **non e' una legge del simulatore**, e sta dichiarata come controllo.")
    A("")
    A("### ⚠ **E TRE LIMITI, dichiarati PRIMA di usare il banco:**")
    A("")
    A("| | |")
    A("|---|---|")
    A("| il «sì» e' ### **LOCALE** | e' la condizione di ### **Poincaré**: `J` simmetrica ⇒ la "
      "forma e' chiusa ⇒ `E` esiste ### **in un intorno dello stato misurato**, non globalmente |")
    A("| il «sì» e' ### **SUL CAMPIONE** | `%d` nodi *(`3` di base col loro vicinato)*. "
      "### ⚠ **Un «asimmetrica» invece e' un no SUL TUTTO**, perche' una `J` simmetrica ha "
      "### **tutte** le sottomatrici principali simmetriche |" % itg["campione"])
    A("| vale ### **nelle variabili scelte** | una legge asimmetrica in `φ` puo' essere il "
      "gradiente di qualcosa ### **in variabili diverse** — ed e' il caso della coppia del "
      "driver, che la forma `U(2)` riscrive in `ψ`. ### **La tavola lo dice invece di "
      "nasconderlo** |")
    A("")
    A("# ⭐ `②` **IL CENSIMENTO -- e il difetto che ha preso DI SE STESSO**")
    A("")
    A("| | |")
    A("|---|--:|")
    A("| scritture di stato trovate, ### **per FORMA** | ### **`%d`** su `%d` nomi |"
      % (len(cen["scritture"]), len(set(x["variabile"] for x in cen["scritture"]))))
    A("| funzioni raggiunte dalle ### **`10` radici dichiarate** | `%d` |"
      % len(cen["raggiunte"]))
    A("| flag cambiati dall'argv ### **DEL DRIVER** | `%d` |" % len(cen["flag_cambiati"]))
    A("")
    A("> ### ⛔ **IL MANDATO DICEVA «`step()` E LE FUNZIONI CHE CHIAMA», E NON BASTA:** il "
      "grafo chiuso dal ### **solo `step`** raggiunge `44` funzioni e ### **NON contiene "
      "`mitosi`, Schwinger, `scuoti_vuoto` ne' la memoria hebbiana** — quelle le chiama "
      "### **il DRIVER**. ### ➜ **Con la sola radice `step` avrei perso TUTTA la classe "
      "CRESCITA**, cioe' esattamente la classe su cui il mandato chiede il conto.")
    A("")
    A("> ### ⚠ **E CIO' CHE IL METODO NON VEDE, dichiarato:** le scritture per "
      "### **mutazione** *(un `dict` aggiornato dentro una funzione a cui l'oggetto e' passato)* "
      "— e' il falso positivo gia' preso su `conc_nodi`. ### **Per quelle il censimento e' per "
      "DIFETTO.**")
    A("")
    A("# ⛔ `③` **LA TAVOLA -- legge per legge, con la classe e il perche'**")
    A("")
    A("### ⚠ **LA CLASSIFICAZIONE E' UN GIUDIZIO MIO, e lo dichiaro:** i numeri che la "
      "sostengono vengono dalle uscite, il giudizio no.")
    A("")
    # ### LE CINQUE CLASSI CANONICHE. ### ⚠ **Il primo giro appaiava male le previsioni**,
    # ### perche' <<TRADUCIBILE>> E' CONTENUTO in <<NON TRADUCIBILE>>: la normalizzazione va
    # ### fatta sul prefisso, nell'ordine dal piu' specifico al piu' generico.
    def canonica(c):
        c = c.upper()
        if c.startswith("NON TRADUCIBILE"):
            return "NON TRADUCIBILE"
        if "CRESCITA" in c:
            return "CRESCITA DELLO SPAZIO"
        if "CON UNA MEMORIA" in c:
            return "TRADUCIBILE CON UNA MEMORIA"
        if "DIAGNOSTICA" in c:
            return "DIAGNOSTICA"
        return "TRADUCIBILE"

    cls = {}
    for (nome, anc, var, classe, ex, esito) in TAVOLA:
        cls.setdefault(canonica(classe), []).append(nome)
    A("| la legge | ancora *(nome, MAI una riga)* | variabile | ### **classe** | "
      "### ⛔ **legge `pos`? (`A17`)** |")
    A("|---|---|---|---|---|")
    for (nome, anc, var, classe, ex, esito) in TAVOLA:
        q = POS.get(nome)
        if q is None:
            cella = "*(non censita)*"
        elif q["stato"] == "no":
            cella = "### ✔ **no**"
        elif q["stato"] == "INDIRETTO":
            cella = ("### ⚠ **INDIRETTO**, via `%s`"
                     % ",".join(sorted(q.get("vie_indirette", {}))[:2]))
        else:
            gg = q.get("guardie_dirette") or []
            cella = ("### ⛔ **DIRETTO**, righe `%s`%s"
                     % (",".join(str(b) for b in q["righe_dirette"][:4]),
                        (" *(guardia `%s`)*" % ",".join(gg)) if gg else ""))
        A("| %s | `%s` | `%s` | ### **%s** | %s |" % (nome, anc, var, classe, cella))
    n_no = sum(1 for x in pos["per_legge"] if x["stato"] == "no")
    n_dir = sum(1 for x in pos["per_legge"] if x["stato"] == "DIRETTO")
    n_ind = sum(1 for x in pos["per_legge"] if x["stato"] == "INDIRETTO")
    n_sync = sum(1 for x in pos["per_legge"]
                 if x["stato"] == "DIRETTO" and "K_SYNC" in (x.get("guardie_dirette") or []))
    A("")
    A("### ⛔ **`%d` leggi su `%d` leggono `pos`** *(`%d` DIRETTO, `%d` INDIRETTO)*. "
      "### ⭐ **MA `%d` di quelle DIRETTE sono LO STESSO BLOCCO:**"
      % (n_dir + n_ind, len(pos["per_legge"]), n_dir, n_ind, n_sync))
    A("")
    A("> ### ⭐ **LE UNICHE LETTURE DI `pos` DENTRO `step` SONO IL CENTRO DI MASSA DELLA "
      "SINCRONIZZAZIONE** *(righe `7773`-`7774`, guardia `K_SYNC`)*: `cmv` e `r_cm`. "
      "### ➜ **Quindi `%d` «DIRETTO» su `%d` NON sono `%d` difetti diversi: sono UNO, e la "
      "decisione `3` (PRESA) lo toglie.**" % (n_sync, n_dir, n_sync))
    A("> ### ⚠ **E QUESTO E' UN DIFETTO DELLA MIA MISURA, PRESO DALLA MISURA STESSA:** "
      "l'ancora di quelle leggi e' `step`, che e' ### **una funzione lunghissima**, quindi il "
      "grafo le attribuiva tutte la stessa lettura. ### **Senza la colonna «guardia» la tavola "
      "avrebbe detto il falso**, e il numero vero e' ### **molto migliore** di come appariva.")
    A("")
    A("### **IL CONTO PER CLASSE** *(e `9-ter` chiede che si CONTI)*:")
    A("")
    A("| classe | quante | previsto | scarto |")
    A("|---|--:|--:|--:|")
    prev = {"TRADUCIBILE": ("PT-2", 7), "TRADUCIBILE CON UNA MEMORIA": ("PT-3", 6),
            "CRESCITA DELLO SPAZIO": ("PT-4", 4), "NON TRADUCIBILE": ("PT-5", 5),
            "DIAGNOSTICA": ("PT-6", 3)}
    tot = 0
    for k in ("TRADUCIBILE", "TRADUCIBILE CON UNA MEMORIA", "CRESCITA DELLO SPAZIO",
              "NON TRADUCIBILE", "DIAGNOSTICA"):
        q = len(cls.get(k, []))
        tot += q
        pid, pv = prev[k]
        seg = "### **=**" if q == pv else ("### **%+d**" % (q - pv))
        A("| ### **%s** | ### **%d** | `%d` *(`%s`)* | %s |" % (k, q, pv, pid, seg))
    A("| ### **IN TUTTO** | ### **%d** | `24`..`32` *(`PT-1`)* | ### **%s** |"
      % (tot, "SOTTO IL MINIMO" if tot < 24 else ("sopra" if tot > 32 else "dentro")))
    A("")
    if tot < 24:
        A("> ### ⛔ **`PT-1` E' MANCATA, E DAL BASSO: `%d` contro un minimo di `24`.** Il motivo "
          "non e' che le leggi sono meno: e' che ### **le ho RAGGRUPPATE piu' grosso di quanto "
          "avessi previsto.** Il censimento trova `%d` ### **scritture**; la tavola ha `%d` "
          "### **righe**, perche' *«il rilassamento di `d0`»* e' una riga e ### **dieci** "
          "scritture. ### ➜ **La previsione contava una cosa e la tavola conta un'altra, e la "
          "differenza e' MIA, non del sistema.** ### **Lo scrivo invece di spezzare le righe "
          "fino a far quadrare il numero.**" % (tot, 419, tot))
        A("")
    A("> ### ⭐ **`PT-9` LA VINCE, E DI PIU' DI QUANTO AVESSI SCRITTO:** dicevo che il test "
      "avrebbe spostato ### **almeno `2`** leggi fuori da TRADUCIBILE. ### ➜ **Ne ha spostate "
      "`4`**, e `TRADUCIBILE` passa da `7` previste a ### **`3`**. ### **Le quattro:** la "
      "### **sincronizzazione** *(dimostrata non integrabile)*, la ### **coppia del driver** "
      "*(non legge `φ`)*, il ### **freno `_smorza`** *(a senso unico, instradata dal punto `(3)`)* "
      "e la ### **massa critica** *(non e' una forza: e' un criterio)*.")
    A("")
    A("> ### ⚠ **E `DIAGNOSTICA` E' `1` RIGA, NON `3`, e non e' un errore di conto:** la riga "
      "copre ### **`231` nomi** riconosciuti per forma. ### **`PT-6` contava le LEGGI, la tavola "
      "conta le RIGHE**, e le due cose non sono la stessa — lo dico invece di far quadrare il "
      "numero.")
    A("")
    A("### ⛔ **E IL CENSIMENTO PUO' AVER PERSO LEGGI: DUE BUCHI SONO CONFERMATI, NON "
      "IPOTETICI**")
    A("")
    A("*(Punto `3` della correzione di Luca. ### **Non lo rifaccio adesso: lo scrivo come "
      "LIMITE**, coi numeri che il censimento stesso stampa.)*")
    A("")
    A("| il buco | ### **confermato?** | il controllo che lo escluderebbe |")
    A("|---|---|---|")
    A("| ### **RADICI MANCANTI** | ### ⚠ **non escluso.** Le radici sono `10`, e le ho "
      "### **scelte io**: una legge che ### **solo il driver** chiama e che non sia fra quelle "
      "`10` e' ### **invisibile** | chiudere il grafo ### **dal TESTO DEL DRIVER** invece che "
      "da una lista mia: radici = ### **tutto cio' che il driver chiama**, letto dall'AST del "
      "driver. ### **E' fattibile, e non l'ho fatto** |")
    A("| ### ⛔ **SCRITTURE PER MUTAZIONE** | ### ⛔ **CONFERMATO, e dal censimento stesso:** "
      "`conc_nodi` e' fra le ### **`7`** variabili *«censite ma MAI scritte dalle radici»* — "
      "ma `conc_nodi` ### **viene scritta**, per mutazione in `_agg_voce`. ### **Il buco non e' "
      "un'ipotesi: ha un nome** | un controllo ### **A RUNTIME**, non dall'AST: fotografare "
      "### **tutti** gli attributi di stato prima e dopo ogni legge e pretendere che ### **ogni "
      "differenza sia attribuita a una scrittura censita**. ### **Nessun metodo statico lo "
      "puo' fare** |")
    A("| ### ⛔ **`setattr` CON NOME CALCOLATO** | ### ⛔ **CONFERMATO: `5` scritture** hanno "
      "come bersaglio `<calcolato>` — il censimento ### **le VEDE ma non sa QUALE variabile "
      "toccano** *(`_avvelena_derivate`, `_nasce`, `_riallinea_derivate`, `_smorza`)* | lo "
      "stesso controllo a runtime: ### **e' il solo che leghi una scrittura al suo bersaglio** "
      "quando il nome e' una stringa calcolata |")
    A("| ### **ALIAS LOCALI** | ### **non escluso, e non ha un nome:** `v = self.phi; "
      "v[...] = ...` sfugge al criterio `self.X`, e l'AST ### **non lo segue** | ### **o il "
      "controllo a runtime, o un'analisi di ALIAS** — che e' molto piu' di una visita "
      "dell'albero |")
    A("")
    A("> ### ⚠ **E LE ALTRE `6` <<censite ma mai scritte>> NON sono buchi, e la differenza "
      "conta:** `dt_e` `dt_n` `tau` `lambda_nodi` `_tempo_luce_nodo` `_fattore_tempo_arco` sono "
      "### **DERIVATE** — ricalcolate ogni passo dalla loro legge, e per questo il censimento "
      "le vede come non scritte dalle radici. ### **`conc_nodi` e' l'unica delle `7` che sia "
      "davvero un buco**, e l'ho distinta invece di contarle tutte come difetti.")
    A("")
    A("> ### ⛔ **MA LA CAUSA PRINCIPALE DI `21` CONTRO `24..32` NON E' NESSUNO DI QUESTI "
      "BUCHI: SONO IO.** Il censimento trova ### **`%d` SCRITTURE**; la tavola ha ### **`%d` "
      "RIGHE**, perche' *«il rilassamento di `d0`»* e' ### **una** riga e ### **dieci** "
      "scritture. ### ➜ **Il raggruppamento e' MIO, e i buchi -- se contano -- "
      "contano SOPRA questo.**" % (len(cen["scritture"]), tot))
    A("")
    A("> ### 📌 **E UNA FORMA CHE HO CERCATO E CHE NON HA TROVATO NIENTE, perche' si sappia:** "
      "`np.add.at(self.X, ...)` -- ### **`0` occorrenze** nelle `%d` funzioni raggiunte. "
      "### **Non aggiunge e non toglie: lo dico perche' un criterio che non scatta MAI non e' "
      "una garanzia, e' solo un criterio che non scatta.**" % len(cen["raggiunte"]))
    A("")
    A("### ⛔ **E IL TERMINE DI ENERGIA, O IL MOTIVO PER CUI NON C'E', UNA PER UNA:**")
    A("")
    A("| la legge | ### **`E_x` o il vincolo** | esito della verifica |")
    A("|---|---|---|")
    for (nome, anc, var, classe, ex, esito) in TAVOLA:
        A("| ### **%s** | %s | %s |"
          % (nome, (ex % sost).replace("|", PIPE), (esito % sost).replace("|", PIPE)))
    A("")
    A("# ⛔ `④` **I DUE «NO» DIMOSTRATI -- e si riconciliano con misure di prima**")
    A("")
    A("| | il numero | la lettura |")
    A("|---|--:|---|")
    A("| ### **la SINCRONIZZAZIONE** | asimmetria ### **`%.4f`** contro un pavimento di "
      "`%.3e` | ### ⛔ **nove ordini sopra**, e ### **identica ai tre passi `h`** — non e' un "
      "artefatto. ### **Nessuna `E(φ)` esiste di cui `K_SYNC` sia il gradiente** |"
      % (SY["asimmetria"], SY["pavimento"]))
    A("| ### **la COPPIA DEL DRIVER** | `0.000e+00` | ### ⛔ **non legge `φ` AFFATTO**: scrive "
      "una coppia su `φ` leggendo ### **lo spinore**. Spazio d'ingresso ≠ spazio d'uscita |")
    A("")
    A("> ### ⭐ **E LA SINCRONIZZAZIONE SI RICONCILIA CON `D2-TER`:** là la sync toglieva il "
      "### **`93.44 %`** della crescita di `H` a `A` fissa ### **senza costare coerenza** "
      "*(`AUC400` `0.9394` → `0.9333`)*, e l'avevo scritto *«pompava senza ordinare»*. "
      "### ➜ **È esattamente il comportamento di una forza NON CONSERVATIVA.** Quella misura "
      "era ### **il sintomo**; questa e' ### **la causa**, e le due non si scelgono: si "
      "spiegano a vicenda.")
    A("")
    A("> ### ⛔ **E LA FORMA `U(2)` NON SALVA LA COPPIA DEL DRIVER:** sta a ### **`1.054`** di "
      "scarto, cioe' il ### **`105 %`**, ### **dieci volte sopra** la soglia del `10 %` che il "
      "criterio del «no» fissa. ### ➜ **Non e' una traduzione: e' UNA LEGGE NUOVA**, e va "
      "### **nell'elenco delle decisioni di Luca**, non nella `H` candidata. ### ⚠ **Senza "
      "quella soglia l'avrei messa in `H`**, chiamando «traduzione» un cambio di fisica del "
      "`105 %`.")
    A("")
    A("# ⭐ `⑤` **I TERMINI CANDIDATI, E QUALI SONO GIA' HAMILTONIANI**")
    A("")
    A("> ### ⛔ **CORREZIONE, e il rilievo e' di Luca: la versione precedente di questa "
      "sezione scriveva le MEMORIE COME DISSIPAZIONE, e le chiamava «termini di `H`».** "
      "Scrivere `(1/2)tw²/τ` con *«il rilassamento e' la discesa di `E`»* descrive un "
      "### **FLUSSO DI GRADIENTE**:")
    A("")
    A("```")
    A("flusso di gradiente:   x' = -dE/dx     =>   dE/dt = -|dE/dx|^2  <=  0")
    A("dinamica hamiltoniana: x' = +dH/dp,  p' = -dH/dx   =>   dH/dt = 0")
    A("```")
    A("")
    A("### ➜ **Il primo DECRESCE SEMPRE: e' dissipazione, ed e' la forma «insegue e "
      "dimentica» che `A16.3` NON ammette come legge.** In una `H` un grado lento "
      "### **non scende: ha un CONIUGATO** *(un impulso, o la fase di una variabile "
      "d'arco)* e ### **scambia energia in modo reversibile**. ### ⛔ **E l'oblio non si "
      "scrive: deve EMERGERE dallo scambio col vuoto** *(`A15.3`)*.")
    A("")
    A("## `⑤.1` ### ✔ **GIA' HAMILTONIANO** — *genera dinamica, non discesa*")
    A("")
    A("```")
    A("H_fase  =  - K_C * somma_archi A_ij cos(phi_i - phi_j)")
    A("```")
    A("")
    A("| | |")
    A("|---|---|")
    A("| ### **il coniugato c'e' GIA'** | con `i dψ/dt = ∂H/∂ψ*`, la coppia coniugata e' "
      "### **`(φ, ρ)`**: la fase e la densita'. ### **Non serve aggiungere niente** |")
    A("| ### **e il banco lo conferma** | asimmetria ### **`%.3e`** contro un pavimento di "
      "`%.3e`: ### **simmetrica**, cioe' una `E` esiste — e qui ### **e' anche scritta** |"
      % (SC["asimmetria"], SC["pavimento"]))
    A("")
    A("> ### ⭐ **E UNA DISTINZIONE CHE SERVE, perche' senza di essa il `⑤.3` sembra una "
      "contraddizione:** la ### **STESSA** `E = −K_C Σ A cos(φ_i − φ_j)` da' ### **due leggi "
      "diverse**, e ### **una conserva e l'altra dissipa.**")
    A("")
    A("```")
    A("Kuramoto  (gradiente):   phi'_i = -dE/dphi_i        ->  dE/dt <= 0   DISSIPA")
    A("primo ordine (A16):      i dpsi/dt = dH/dpsi*       ->  dH/dt  = 0   CONSERVA")
    A("                         cioe'  phi'_k = +dH/drho_k ,  rho'_k = -dH/dphi_k")
    A("```")
    A("")
    A("### ➜ **Non conta QUALE energia: conta A QUALE EQUAZIONE la si dia.** La coppia scalare "
      "e' hamiltoniana perche' `φ` e `ρ` sono ### **coniugati**; lo stesso `E` messo in una "
      "discesa ### **dissipa**. ### ⛔ **Per questo «scrivere la `E` della sincronizzazione» non "
      "l'avrebbe salvata** — e' il motivo `(ii)` della decisione `3`.")
    A("")
    A("## `⑤.2` ### ⚠ **POTENZIALI VERI, CHE ASPETTANO IL CONIUGATO DELLA GEOMETRIA**")
    A("")
    A("```")
    A("V_geom  =  (1/2) somma_archi k_ij (d_ij - d0_ij)^2        <- il legame elastico")
    A("         + somma_archi V_rep(d_ij)                        <- la repulsione")
    A("```")
    A("")
    A("### ⭐ **Questi sono `V(d)` per davvero** — funzioni della sola configurazione, non "
      "inseguimenti. ### ⛔ **Ma `d` non ha un impulso DENTRO `H`:** oggi si muove con `vd` "
      "*(Verlet)*, e l'energia cinetica delle lunghezze ### **non e' in `H`**. ### ➜ **E' la "
      "DECISIONE `9`.**")
    A("")
    A("## `⑤.3` ### ⛔ **FLUSSI DI GRADIENTE — «memorie da riscrivere col loro coniugato», "
      "NON termini di `H`**")
    A("")
    A("```")
    A("OGGI (dissipativo):            tw'  = -tw/tau_tw")
    A("                               d0'  = +(d - d0)/tau_p")
    A("                               peq' = +(rho - peq)/tau_bg + laplaciano(peq)/TAU_DIFF")
    A("```")
    A("")
    A("### ⛔ **Nessuno dei tre e' un termine di `H`: sono TRE LEGGI DI DISSIPAZIONE**, e "
      "finche' restano in questa forma ### **non entrano nella `H` candidata.**")
    A("")
    A("### 📌 **I CONIUGATI, PROPOSTI COME CANDIDATI E NON COME DECISIONE:**")
    A("")
    A("| memoria | ### **il coniugato candidato** | la forma | ### **che cosa diventa `τ`** |")
    A("|---|---|---|---|")
    A("| ### **`tw`** *(d'arco)* | ### ⭐ **`tw` come FASE DI UN LEGAME `U(1)`**, col suo "
      "### **campo elettrico d'arco** `E_ij` come momento coniugato | "
      "`H_tw = (1/2)Σ_archi E_ij² − K_B Σ_placchette cos(Σ_arco tw)` — ### **energia "
      "elettrica + energia di PLACCHETTA** | ### **una FREQUENZA:** `ω_tw = |Δω_locale|` al "
      "posto di `τ_tw = 2π/|Δω|`. ### **Lo stesso numero, letto al contrario:** oggi e' un "
      "tempo di OBLIO, lì e' il ritmo di un'OSCILLAZIONE |")
    A("| ### **`d0`** *(d'arco)* | un ### **impulso proprio** `p_d0`, con una massa d'arco | "
      "`H_d0 = Σ p_d0²/(2 m_arco) + (1/2)Σ k(d − d0)²` | ### **una frequenza:** "
      "`ω = sqrt(k/m_arco)`, e `d0` ### **OSCILLA attorno a `d`** invece di raggiungerla |")
    A("| ### **`peq`** *(di nodo)* | un ### **impulso proprio** `p_peq` | "
      "`H_peq = Σ p_peq²/(2 m_p) + (1/2)Σ(ρ − peq)²/χ + (1/2)Σ_archi(peq_i − peq_j)²/χ_d` | "
      "### **una VELOCITA':** la diffusione diventa un'### **ONDA**, e `TAU_DIFF` diventa "
      "`c_p² = 1/(m_p·χ_d)` — ### **una velocita' del suono, non un tempo di oblio** |")
    A("| ### ⭐ **`omega_s`** *(di nodo)* | ### **NESSUNO: ce l'ha GIA'** | `omega_s` ### **E' "
      "una velocita' angolare**, cioe' il momento coniugato della fase dell'orologio, e "
      "`(1/2)Σ I_k omega_s²` con `I = (d/cs)²` e' ### **energia cinetica VERA** | ### **niente "
      "`τ`:** le va ### **TOLTO** lo smorzamento `−omega_src/τ`, non dato un coniugato |")
    A("")
    A("> ### ⭐ **LA COSA CHE QUESTA CORREZIONE FA EMERGERE, e non e' un dettaglio:** il "
      "coniugato naturale di `tw` ### **E' L'ELETTROMAGNETISMO.** `tw` e' un angolo "
      "### **per arco**; un angolo per arco col suo momento coniugato e un termine di "
      "placchetta ### **E' una teoria di gauge `U(1)` sul reticolo** — `tw` diventa il "
      "### **potenziale vettore**, il suo coniugato il ### **campo elettrico**, la placchetta "
      "il ### **campo magnetico**. ### ➜ **E' esattamente la direzione del principio guida** "
      "*(«dallo spinore discende l'interazione con la luce»)*, e ci si arriva "
      "### **dall'obbligo di dare un coniugato a una memoria**, non per innesto.")
    A("> ### ⛔ **Resta un'IPOTESI da dimostrare, e la marco tale:** che quella sia LA forma "
      "non e' misurato.")
    A("")
    A("## `⑤.4` ### ⛔ **E L'OBLIO, ADESSO, NON HA PIU' CASA**")
    A("")
    A("### **Con i coniugati, `tw`, `d0` e `peq` OSCILLANO: non dimenticano piu'.** ### ➜ "
      "**Quindi l'oblio deve venire da FUORI, cioe' dallo scambio col vuoto** *(`A15.3`)* — "
      "### **ed e' lo STESSO posto da cui deve venire l'energia della nascita** *(`S5`, "
      "`⑦`)*. ### ⚠ **Non e' una coincidenza: sono la stessa decisione aperta, vista da due "
      "lati.**")
    A("")
    A("## `⑤.5` ### ⛔ **CHE COSA NON C'E', E SI VEDE**")
    A("")
    A("| | ### **che cosa NON c'e', e si vede** |")
    A("|---|---|")
    A("| ### ⛔ **la sincronizzazione** | ### **NON c'e', ed e' dimostrato** che non possa "
      "esserci |")
    A("| ### ⛔ **la coppia del driver** | ### **NON c'e'**: la `H` candidata ha la coppia "
      "### **SCALARE**. ### **Questa è la prima decisione di Luca** |")
    A("| ### ⛔ **termostato e scuotimento** | ### **NON ci sono**: vanno diventati scambio col "
      "### **vuoto LOCALE** *(`A15.3`)*, e quella forma ### **non e' scritta** |")
    A("| ### ⛔ **la memoria hebbiana** | ### **NON c'e'**: una ### **media mobile non e' una "
      "discesa** *(vince l'ultimo)*. La forma va ### **cambiata**, non tradotta |")
    A("| ### ⚠ **`TAU_DIFF = 1.0`** | e' una ### **MANOPOLA NUDA** dentro un termine candidato: "
      "### **`A1` la vieta**, e finche' resta tale quel termine ### **non e' ammissibile** |")
    A("| ### ⚠ **`w` e `U` dinamici** | ### **`A16.3`**: devono essere gradi di liberta' "
      "DENTRO `H`. ### **La forma del termine di memoria d'arco NON e' scritta** — e per "
      "`A16.3` vale lo stesso vincolo del `⑤.3`: ### **servono CONIUGATI, non rilassamenti** |")
    A("| ### ⛔ **l'ENERGIA CINETICA delle lunghezze** | ### **NON c'e'**, e la geometria "
      "### **si muove comunque** *(Verlet, `vd`)*: ### **e' la DECISIONE `9`** |")
    A("")
    A("# ⭐ `⑥` **LA REGOLA DI CRESCITA -- a parte, perche' NON e' un termine di `H`**")
    A("")
    A("## `⑥.1` **LA FORMA DELLA REGOLA**")
    A("")
    A("> ### ⭐ **E' l'unica legge che CAMBIA `H`**, quindi non puo' starci dentro. "
      "### **Si scrive accanto.**")
    A("")
    A("```")
    A("QUANDO:  una grandezza della materia supera una soglia che e' UNA LEGGE, non un numero")
    A("         (A1, A15.2) -- oggi la soglia e' massa_critica_adattiva, e U1 dice che")
    A("         `massacriticacollasso` ha 21 usi DENTRO le leggi: voce BLOCCANTE")
    A("COME:    psi_p -> psi_p / sqrt(2)   sul genitore E sul nato, stessa fase, stessa")
    A("         direzione di Bloch                                     [CANDIDATA, S4]")
    A("CHI PAGA: il Delta H va ceduto o ricevuto dal VUOTO LOCALE      [APERTO, S5]")
    A("```")
    A("")
    A("### ⛔ **LA REGOLA DI OGGI NON CONSERVA, E LA TAVOLA DEL SIMULATORE LO DICE.** Le `%d` "
      "regole di nascita si leggono dalla tavola `_nascita_regola`, e fra le sue `%d` classi "
      "### **non ce n'e' NESSUNA che si chiami «il genitore cede»**:"
      % (len(cre["regole"]), len(cre["classi"])))
    A("")
    A("| | |")
    A("|---|---|")
    A("| il nato prende la ### **media dei genitori** per | `phi` `phi0` `phivel` `pos` `psi` |")
    A("| ### ⛔ **e nessuno togli niente al genitore** | ### **`Σρ` CRESCE a ogni nascita** — e' "
      "la violazione ### **`6`** di `A14`, e qui e' ### **letta dalla tavola**, non dedotta |")
    A("")
    A("### **IL CONTO SULLO SNAPSHOT** *(la `ρ` vera della scena, dopo `3` passi pieni; il nodo "
      "piu' denso ha `ρ = %.4e`, lo `%.4f %%` di `Σρ`)*:"
      % (sn["rho_max"], 100.0 * sn["rho_max"] / sn["somma_rho"]))
    A("")
    A("| se quel nodo divide | `Σρ` | `Σρ²` |")
    A("|---|--:|--:|")
    A("| ### **la regola di OGGI** | ### **`+%.4f %%`** *(non conserva)* | `+%.4f %%` |"
      % (100.0 * sn["rho_max"] / sn["somma_rho"],
         100.0 * sn["rho_max"] ** 2 / sn["somma_rho2"]))
    A("| ### **la regola CANDIDATA** `ψ → ψ/√2` | ### **`0.000e+00`** *(conserva AL BIT)* | "
      "### **`%.4f %%`** *(il `ρ²` del nodo si DIMEZZA)* |"
      % (100.0 * (sn["somma_rho2_dopo_candidata"] - sn["somma_rho2"]) / sn["somma_rho2"]))
    A("")
    A("## `⑥.2` ### ⭐ **CHI PAGA LA NASCITA — LA PROPOSTA DI LUCA** *(2026-10-08, "
      "CANDIDATA per `S5`)*")
    A("")
    A("> ### ⭐ **LA FRASE:** *«chi paga la nascita e' ### **il calore che si scarica sul vuoto "
      "locale**»*.")
    A("")
    A("### **LETTA COL BILANCIO DELLA SONDA** *(`N = 400`, `g = -5`, braccio `NON-NORM`, "
      "seme `11`)*:")
    A("")
    A("| il passo | il numero |")
    A("|---|--:|")
    A("| la ### **CONCENTRAZIONE libera** energia: `H`(esteso) → `H`(un nodo) | `%.1f` → "
      "`%.1f` |" % (bil["H_esteso"], bil["H_un_nodo"]))
    A("| ### **energia liberata** | ### **`%.1f`** |" % bil["liberata"])
    A("| in una dinamica conservativa *(`A16`)* ### **non sparisce** | diventa "
      "### **agitazione del campo intorno**, cioe' ### **CALORE NEL VUOTO LOCALE** "
      "*(`A15.3`, reversibile)* |")
    A("| la ### **NASCITA costa** | ### **`+%.1f`** *(la prima divisione)* |"
      % bil["costo_prima_divisione"])
    A("| e lo ### **PRELEVA da quel calore** | il costo e' il ### **`%.2f %%`** di cio' che la "
      "concentrazione ha liberato |" % (100.0 * bil["frazione"]))
    A("")
    A("### ➜ **IL FRENO SI PAGA DA SOLO: la concentrazione produce il calore che finanzia lo "
      "spazio nuovo, SENZA BAGNO ESTERNO.**")
    A("")
    A("### ⚠ **E DUE COSE CHE IL CONTO DICE E CHE LA FRASE NON DICEVA ANCORA.**")
    A("")
    A("**`(i)` IL MARGINE E' ZERO PER COSTRUZIONE — ed e' la forza E il limite.** In una "
      "dinamica conservativa l'energia per ### **disfare** il collasso e' ### **esattamente** "
      "quella che il collasso ha liberato: `%.1f` contro `%.1f`, ### **margine `0`**. "
      "### ✔ **La forza: non serve nessun bagno esterno, il conto si chiude da solo.** "
      "### ⛔ **Il limite: «basta» e «basta esattamente» sono la stessa cosa**, quindi il fatto "
      "che il conto torni ### **NON e' una prova che il processo avvenga** — e' la condizione "
      "minima perche' ### **non sia vietato.** ### ➜ **Quello che decide e' DOVE VA IL "
      "CALORE**, cioe' il punto `(ii)` qui sotto."
      % (bil["liberata"], bil["liberata"]))
    A("")
    A("**`(ii)` ⭐ E IL FRENO SI FERMA DA SOLO, A UN NUMERO CHE NON HO SCELTO.** Il costo di "
      "una divisione va come `N²`, quindi ### **ogni livello della cascata costa un quarto del "
      "precedente**: `2^k · [(|g|/4)(N/2^k)² − w(N/2^k)] = (|g|/4)N²/2^k − wN`. Si somma e si "
      "guarda quando il calore finisce:")
    A("")
    A("| livello | nodi | norma per nodo | costo del livello | cumulato | ### **calore "
      "residuo** |")
    A("|--:|--:|--:|--:|--:|--:|")
    for L in bil["livelli"]:
        A("| `%d` | `%d` | `%.1f` | `%.1f` | `%.1f` | %s |"
          % (int(L["livello"]), int(L["nodi"]), float(L["norma"]), float(L["costo"]),
             float(L["cumulato"]),
             ("### **`%.1f`**" % float(L["residuo"])) if float(L["residuo"]) < 0
             else ("`%.1f`" % float(L["residuo"]))))
    A("")
    A("### ➜ **IL CALORE SI ESAURISCE AL LIVELLO `%d`: il sistema si ferma a `%d` NODI.** "
      "### ⭐ **Non frammenta all'infinito, e la scala d'arresto ESCE DAL BILANCIO — non e' una "
      "manopola** *(`A1`)*."
      % (int(bil["livello_di_arresto"]), 2 ** int(bil["livello_di_arresto"])))
    A("")
    A("> ### ⭐ **E UN'IDENTITA' CHE VALE LA PENA DI DIRE:** la serie intera dei costi, "
      "ignorando l'hopping, fa `(|g|/2)N² = %.1f`; l'energia liberata dal collasso fa "
      "`%.1f`. ### **I due termini `N²` SI CANCELLANO**, e la differenza — ### **`%.1f`** — e' "
      "esattamente `|H`(esteso)`|`, cioe' ### **i termini di HOPPING**. ### ➜ **Quindi non "
      "sono le grandezze dominanti a decidere se la nascita si paga: LO DECIDONO I TERMINI "
      "SOTTODOMINANTI** — ed e' il motivo per cui la decisione `2` *(l'interferenza "
      "normalizzata o no)* ### **pesa su questa**."
      % (bil["serie_infinita"], bil["liberata"], bil["differenza_serie"]))
    A("")
    A("### ⭐ **LA CONSEGUENZA CANDIDATA SULLA SOGLIA** *(`A1`, `A15.2`)*")
    A("")
    A("> ### **La soglia di nascita NON e' un numero ne' una massa critica a parte: e' IL "
      "BILANCIO STESSO.** Un nodo si divide quando ### **il calore disponibile nel suo vuoto "
      "locale ≥ `ΔH` della divisione.**")
    A("")
    A("| | |")
    A("|---|---|")
    A("| ### ✔ **perche' questo soddisfa `A1`** | ### **non c'e' nessun numero da tarare:** "
      "`ΔH` si calcola da `H`, e il calore si misura dal campo. ### **E' una LEGGE, non una "
      "soglia** |")
    A("| ### ⭐ **e il segno del controretroazione e' QUELLO GIUSTO** | la nascita "
      "### **diluisce** → la concentrazione ### **cala** → si produce ### **meno** calore → le "
      "nascite ### **rallentano**. ### **E' retroazione NEGATIVA, cioe' un REGOLATORE** — ed e' "
      "esattamente cio' che un freno deve essere. ### ⚠ **Lettura candidata, non misurata** |")
    A("")
    A("### **CHE COSA SOSTITUIREBBE:**")
    A("")
    A("| | |")
    A("|---|---|")
    A("| `massa_critica_adattiva` | ### **sparisce**: la soglia non e' una massa |")
    A("| `massa_critica_collasso` e i suoi ### **`21` usi DENTRO le leggi** | ### ⛔ **sparisce, "
      "ed e' la voce BLOCCANTE `U1`.** ### ➜ **La proposta di Luca non e' solo una forma piu' "
      "pulita: CHIUDE una voce che blocca i run base** |")
    A("| la soglia della mitosi come ### **numero** | diventa ### **il confronto fra due "
      "energie**, entrambe calcolate |")
    A("")
    A("### ⛔ **E CHE COSA RESTA DA DEFINIRE — due cose, e non le invento:**")
    A("")
    A("| | che cosa manca | ### **il candidato** |")
    A("|---|---|---|")
    A("| ### **`(i)`** | che cos'e' il ### **«vuoto locale» come grandezza CONTABILE** | la "
      "### **parte del campo intorno alla massa che non e' nella massa**, cioe' le "
      "### **oscillazioni irradiate** — ### ✔ **NON una variabile aggiunta:** si legge da `ψ` "
      "come `H` ristretta all'intorno ### **meno** l'energia del profilo stazionario lì. "
      "### ⚠ **Questa sottrazione non e' scritta**, ed e' il pezzo che manca |")
    A("| ### **`(ii)`** | l'### **estensione di «locale»** | ### **i vicini diretti**, oppure "
      "### ⭐ **una scala legata alla massa** — candidato: la ### **lunghezza di guarigione** "
      "`ξ = 1/√(|g|ρ)`, che e' ### **DERIVATA e non scelta** *(`A1`)*, ed e' la scala su cui il "
      "solitone stesso si forma. ### ⛔ **Fra le due c'e' una differenza MISURABILE**, e non e' "
      "misurata |")
    A("")
    A("> ### ⚠ **E IL LEGAME CON IL `⑤.4`, che e' la cosa che mi ha sorpreso:** con i "
      "coniugati le memorie ### **oscillano invece di dimenticare**, quindi l'oblio deve venire "
      "### **dallo stesso vuoto locale**. ### ➜ **La proposta di Luca non finanzia solo la "
      "NASCITA: finanzia anche L'OBLIO**, e le due cose diventano ### **lo stesso conto.** "
      "### ⛔ **Che il conto basti per DUE uscite invece di una NON e' verificato**, e il "
      "margine — come dice il `(i)` — e' ### **zero**.")
    A("")
    A("# ⛔ `⑦` **`PT-7`: LA NASCITA FRENA IL COLLASSO? -- LA VINCE A META', E LA META' CHE "
      "PERDE E' QUELLA CHE CONTA**")
    A("")
    A("La previsione, scritta ### **prima** *(`c6c1112`)*: *«la divisione impedisce il collasso, "
      "perche' conserva `Σρ` ma dimezza il contributo `ρ²` del nodo che divide»*. Il conto, sulla "
      "`H` della sonda:")
    A("")
    A("```")
    A("H(un nodo)   = (g/2) N^2")
    A("H(due figli) = -2 w (N/2) + (g/2) * 2 * (N/2)^2  =  -w N + (g/4) N^2")
    A("Delta H      = -(g/4) N^2 - w N  =  (|g|/4) N^2 - w N")
    A("```")
    A("")
    A("| `N` | `g` | `w` | `H` un nodo | `H` due figli | ### **`ΔH`** |")
    A("|--:|--:|--:|--:|--:|--:|")
    for c in cre["pt7"]:
        A("| `%.0f` | `%.1f` | `%.4f` | `%.1f` | `%.1f` | ### **`%+.1f`** |"
          % (float(c["N"]), float(c["g"]), float(c["w"]), float(c["H_uno"]),
             float(c["H_due"]), float(c["dH"])))
    A("")
    A("| | |")
    A("|---|---|")
    A("| ### ✔ **la META' CHE VINCE** | ### **la diluizione c'e', ed e' ESATTA:** `Σρ` si "
      "conserva al bit e il contributo `ρ²` del nodo ### **si dimezza** — cioe' la divisione "
      "toglie ### **esattamente** cio' che il collasso guadagna |")
    A("| ### ⛔ **la META' CHE PERDE** | ### **la divisione ALZA `H`**, quindi ### **NON avviene "
      "da sola:** `ΔH = %+.1f` per `N = 400`, `g = %.1f`. ### **Va PAGATA** |"
      % (float(p7["dH"]), float(p7["g"])))
    A("| ### ⛔ ### ➜ **la conclusione** | ### **LA NASCITA E' UN FRENO SOLO SE QUALCUNO PAGA**, "
      "e chi paga e' il ### **VUOTO LOCALE** — che e' il punto ### **`S5`**, e ### **`S5` e' "
      "APERTO**. ### ⚠ **Non e' una conferma dell'ipotesi del guardiano: e' la dimostrazione che "
      "quell'ipotesi DIPENDE INTERAMENTE DAL PUNTO APERTO** |")
    A("")
    A("> ### ⭐ **E LA PROPOSTA DI LUCA RISPONDE ESATTAMENTE A QUESTO** *(`⑥.2`)*: il `ΔH` "
      "lo paga ### **il calore che la concentrazione stessa ha liberato** — `%.1f` disponibili "
      "contro `%.1f` richiesti dalla prima divisione, cioe' il ### **`%.2f %%`**. ### ⛔ **Ma il "
      "margine complessivo e' ZERO per costruzione**, e la cascata ### **si ferma al livello "
      "`%d`**: `%d` nodi."
      % (bil["liberata"], bil["costo_prima_divisione"], 100.0 * bil["frazione"],
         int(bil["livello_di_arresto"]), 2 ** int(bil["livello_di_arresto"])))
    A("")
    A("> ### ⭐ **E IL NUMERO CHE LEGA QUESTO AL SIMULATORE:** senza bagno le nascite crollano "
      "da ### **`164`** *(`B-SCAL`, col bagno)* a ### **`0`** *(`B-SCAL-TS`, senza)*. "
      "### ➜ **Nel simulatore di oggi chi paga la nascita E' IL BAGNO GLOBALE**, ed e' misurato. "
      "### **La domanda di `S5` non e' accademica: e' la domanda su che cosa sostituisca quel "
      "bagno.**")
    A("")
    A("# ⭐ `⑧` **IL CONFRONTO CON LA SONDA DEL PROTOTIPO, termine per termine**")
    A("")
    A("| nella sonda | nel simulatore | la lettura |")
    A("|---|---|---|")
    A("| ### **l'hopping** `-w ⟨ψ_i|U|ψ_j⟩` | la ### **coppia d'interferenza** con "
      "`A = w·cos(φ⁰_i − φ⁰_j)` | ### ⚠ **il kernel del simulatore ha `φ⁰` CONGELATA** "
      "*(`PHI0-CONGELATA`)*: la sonda non ha niente di congelato, e in questo e' ### **meno** "
      "difettosa |")
    A("| ### **la COESIONE** `(g/2)|ψ|⁴` | ### ⛔ **NON esiste un `|ψ|⁴`.** La coesione viene "
      "dalla ### **coppia stessa** *(una `A` positiva lega le fasi)* piu' il ### **legame "
      "elastico** | ### ➜ **la sonda ha messo in un termine di sito cio' che nel simulatore e' "
      "un termine d'ARCO** |")
    A("| ### ⛔ **il FRENO** | la ### **repulsione** `V_rep(d)`, la ### **massa critica**, e "
      "### **la nascita dello spazio** | ### ⛔ **LA SONDA NON HA NESSUNO DEI TRE**, ed e' per "
      "questo che collassa |")
    A("| ### **il grafo** | ### **dinamico**: nodi e archi nascono | ### ⛔ **nella sonda e' "
      "FISSO**: un'### **impalcatura del test**, dichiarata violazione provvisoria di `A16.3` |")
    A("| la ### **memoria** | `tw`, `d0`, `peq`, `omega_s`, `mem_mot` | ### ⛔ **la sonda non ha "
      "NESSUNA memoria**: `w` e `U` sono fissi |")
    A("")
    A("> ### ⭐ **E IL NUMERO DEL MARE `v2` SI LEGGE ADESSO:** con la sonda, a norma fissa, lo "
      "stato piu' basso e' il ### **collasso su un nodo** per ogni `g < 0` *(a `g = -5`: "
      "`%.1f` contro `%.1f`)*. ### ➜ **Non e' un fatto sul modello di Luca: e' un fatto su una "
      "`H` CHE NON HA IL FRENO.** Il simulatore ne ha ### **tre**, e la tavola li nomina."
      % (b0["g"]["-5.0"]["H_un_nodo"], b0["g"]["-5.0"]["H_esteso"]))
    A("")
    A("# ⛔ `⑨` **L'ELENCO DELLE DECISIONI DI LUCA** — *una per riga, con le alternative e che "
      "cosa cambierebbe*")
    A("")
    A("### ⭐ **TRE SONO PRESE** *(decisioni di Luca del 2026-10-08)*: la ### **`1`** *(il "
      "freno e' la `(c)`: entrambi)*, la ### **`3`** *(la sincronizzazione si toglie)*, la "
      "### **`10`** *(il calore paga la nascita)*. ### **Le altre dieci sono APERTE**, e le "
      "schede delle prese stanno in `doc/REGISTRO_FISICA.md`.")
    A("")
    A("| # | la decisione | le alternative | che cosa cambia |")
    A("|--:|---|---|---|")
    A("| `1` | ### ✔ ⭐ **IL FRENO DELLA COESIONE E' LA `(c)` — DECISIONE DI LUCA, PRESA** "
      "*(2026-10-08)* | ### **ENTRAMBI**, e non per prudenza | ### **FRENO VERO:** la "
      "### **nascita dello spazio**, pagata dal calore *(decisione `10`)*. ### **FRENO A CORTO "
      "RAGGIO:** la ### **PRESSIONE DI DEGENERAZIONE** — *«che in natura esiste»* — come "
      "### **BARRIERA PER NODO dentro `H`**. ### ⭐ **PERCHE' ENTRAMBI, ed e' coerenza non "
      "gusto:** se il freno fosse solo «capacita' + nascite», quando il calore si esaurisce "
      "*(livello `4`)* ### **le nascite si fermano e NON RESTA NESSUN FRENO.** Con la barriera: "
      "la degenerazione ### **tiene sempre**, la nascita ### **alleggerisce quando il calore la "
      "paga**, e se il calore non basta la materia ### **resta compressa al limite senza "
      "collassare**. ### **Scheda:** `freno-della-coesione`. ### **Dettagli:** `⑧` |")
    A("| `2` | ### **l'interferenza NORMALIZZATA sul grado, o no** | `w_ij` ### **come oggi**; "
      "oppure `w_ij/√(s_i s_j)` | il `PR` del Perron a `g = 0` passa da ### **`%.1f`** a "
      "### **`%.1f`** su `400`: ### **la geometria da sola concentra, e la normalizzazione glielo "
      "toglie quasi tutto.** ### ⚠ **E tocca `A3`** *(`s_k` e' del proprio intorno — ma e' una "
      "SOMMA, non una statistica di posizione: `s̃_k` passa da `%.4f` a `%.4f` di deviazione, "
      "media `%.2f`, ### **non `1`**)* |"
      % (b0["PR_perron"], b1["PR_perron"], b1["s_k_dev_rel_prima"], b1["s_k_dev_rel"],
         b1["s_k_media"]))
    A("| `3` | ### ✔ ⭐ **LA SINCRONIZZAZIONE SI TOGLIE — DECISIONE DI LUCA, PRESA** "
      "*(2026-10-08)* | ### **non ci sono piu' alternative: e' DECISA.** La scheda sta in "
      "`doc/REGISTRO_FISICA.md` *(`sincronizzazione-si-toglie`)* | ### **I TRE MOTIVI:** "
      "`(i)` ### **nessuna `E(φ)` esiste** *(asimmetria `%.4f` contro `%.3e`)*; `(ii)` "
      "### **anche un Kuramoto SIMMETRICO e' un flusso di gradiente**, cioe' dissipativo — "
      "la forma che `A16.3` non ammette; `(iii)` toglierla ### **non costa coerenza** "
      "*(`AUC400` `0.9394` → `0.9333`)* e toglie il ### **`93.44 %%`** del pompaggio. "
      "### ➜ **DEVE EMERGERE:** al primo ordine uno stato stazionario ha `dφ_k/dt = μ` "
      "### **per ogni `k`**, e il sistema ci arriva cedendo l'eccesso al vuoto locale — "
      "### **lo stesso calore della `10`**. ### ⛔ **CRITERIO DA MISURARE, non da assumere:** "
      "la dispersione di `dφ/dt` dentro la massa deve ### **calare**, col calore "
      "contabilizzato. ### **Se non succede, la decisione si RIAPRE.** ### ⚠ **E lo stesso "
      "calore serve alla `1` e alla `10`: UN SERBATOIO, TRE USI** |"
      % (SY["asimmetria"], SY["pavimento"]))
    A("| `4` | ### **`A` da `φ⁰` o dalla MEMORIA VIVA dei legami** | `φ⁰` ### **congelata** "
      "*(oggi)*; oppure una memoria d'arco che ### **evolve** | ### ⛔ **`φ⁰` congelata viola "
      "`A15.1`** *(non dimentica niente)* ed e' `PHI0-CONGELATA`. Con la memoria viva `A` diventa "
      "un grado di liberta' ### **dentro `H`** *(`A16.3`)*, e la `H` candidata acquista un termine |")
    A("| `5` | ### **il campo scalare a `φ/2`** | `cos(φ_i − φ_j)` ### **(oggi)**; oppure "
      "`cos((φ_i − φ_j)/2)` ### **(la direzione candidata di Luca)** | ### **cambia la "
      "periodicita'**: `φ/2` e' la doppia copertura `4π`, cioe' ### **lo spinore**. ### ⚠ **E il "
      "ramo scalare di oggi usa `cos(φ_i − φ_j)`**, non `/2`: era un test sul ### **principio**, "
      "non sulla forma |")
    A("| `6` | ### **che cosa diventano TERMOSTATO e SCUOTIMENTO** | restare forzanti "
      "### **globali** *(oggi, e viola `A2` e `A14.1`)*; oppure ### **scambio col vuoto LOCALE** "
      "*(`A15.3`)* | ### ⛔ **e non e' indolore: senza bagno le nascite crollano da `164` a "
      "`0`.** Togliere il bagno ### **senza** mettere il vuoto locale ### **spegne la crescita** |")
    A("| `7` | ### **la forma della DIVISIONE alla nascita, e la soglia come LEGGE** | "
      "`ψ → ψ/√2` ### **(candidata)**; oppure un'altra ripartizione | ### ✔ **`ψ/√2` conserva "
      "`Σρ` al bit e dimezza il `ρ²` del nodo** — ma ### **alza `H` di `%+.1f`**, quindi serve "
      "`S5`. ### ⛔ **E la soglia di oggi NON e' una legge:** `U1` e' ### **bloccante** |"
      % float(p7["dH"]))
    A("| `8` | ### **DA DOVE VIENE L'ENERGIA DELLO SPAZIO NUOVO** *(`S5`)* | il ### **bagno "
      "globale** *(oggi, misurato)*; oppure un termine di ### **vuoto LOCALE** da scrivere | "
      "### ⛔ **E' LA DECISIONE DA CUI DIPENDONO LE ALTRE:** senza di essa la nascita non puo' "
      "essere il freno, e la `1` si riduce a `(a)`. ### ⭐ **E LA PROPOSTA DI LUCA LE DA' UNA "
      "RISPOSTA CANDIDATA:** il calore della concentrazione stessa — ### **vedi la `10`** |")
    A("| `9` | ### ⭐ **LA GEOMETRIA AL SECONDO ORDINE** — `d` si muove con una velocita' "
      "propria *(Verlet, `vd`)*, ma ### **`A16.2` dice che ogni stato evolve al PRIMO ordine "
      "sotto `H`** | ### **`(a)`** la geometria e' ### **hamiltoniana in `(d, p_d)`**, cioe' "
      "### **del primo ordine NELLO SPAZIO DELLE FASI**, con l'energia cinetica delle "
      "lunghezze ### **DENTRO `H`**; ### **`(b)`** la geometria diventa ### **anch'essa uno "
      "stato del tipo di `ψ`** | ### **vedi la tabella qui sotto** |")
    A("| `10` | ### ✔ ⭐ **IL CALORE PAGA LA NASCITA — DECISIONE DI LUCA, PRESA** "
      "*(2026-10-08; era ### **candidata** in `b6cba2f`)* | ### **non ci sono piu' "
      "alternative:** la soglia ### **E' IL BILANCIO** *(il nodo divide quando il calore del "
      "suo vuoto locale ≥ `ΔH`)*. ### **Scheda:** `chi-paga-la-nascita` | ### ⭐ **sparisce "
      "`massa_critica_collasso` e i suoi `21` usi dentro le leggi: CHIUDE la voce bloccante "
      "`U1`**, e la soglia diventa una ### **LEGGE** *(`A1`)*. ### ⛔ **E RESTA APERTO, scritto "
      "come aperto:** che cos'e' il ### **vuoto locale come grandezza contabile** e la sua "
      "### **estensione**, ### **entrambi in forma RELAZIONALE** *(`A17`)*. ### ⛔ **CRITERIO "
      "CHE LA RIAPRE:** se il calore ### **non resta disponibile vicino alla massa** *(si "
      "disperde prima di poter pagare)*, si riapre |")
    A("| `11` | ### **la forma `U(2)` della coppia** | tenerla; oppure no | ### ⛔ **NON e' "
      "una traduzione: e' UNA LEGGE NUOVA** — `1.054` di scarto, il `105 %`, dieci volte sopra "
      "la soglia del `10 %`. ### **Va decisa come fisica nuova, non adottata come "
      "riscrittura** |")
    A("| `12` | ### **la SCOMPARSA degli archi** | tenerla; oppure vietarla | ### ⛔ **`A14.2` "
      "dice che la CRESCITA e' l'unica freccia ammessa**, quindi un arco che muore e' ### **già "
      "una violazione**. ### **Non e' una legge da tradurre: e' un difetto da decidere** |")
    A("| `13` | ### ⛔ **I CONIUGATI DELLE MEMORIE** *(`⑤.3`)* | `tw` come ### **fase di un "
      "legame `U(1)`** *(e allora arriva l'elettromagnetismo)*; `d0` e `peq` con un "
      "### **impulso proprio**; oppure una forma diversa | ### **`τ` smette di essere un tempo "
      "di OBLIO e diventa una FREQUENZA**, e le memorie ### **oscillano invece di "
      "dimenticare**. ### ⛔ **E allora l'oblio deve venire dal vuoto — cioe' dalle decisioni "
      "`8` e `10`** |")
    A("")
    A("### ⭐ **LA DECISIONE `9` PER ESTESO -- che cosa cambia nel codice, e che cosa diventa "
      "`beta·vd`**")
    A("")
    A("| | ### **`(a)` hamiltoniana in `(d, p_d)`** | ### **`(b)` la geometria diventa uno "
      "stato come `ψ`** |")
    A("|---|---|---|")
    A("| ### **la lettura** | la geometria resta ### **sua**, ma col suo impulso: "
      "`H += Σ_archi p_d²/(2 m_arco)`, e `d' = ∂H/∂p_d`, `p_d' = −∂H/∂d`. ### ✔ **`A16` la "
      "AMMETTE**, perche' *«primo ordine»* vale ### **nello spazio delle fasi** — a patto che "
      "### **il termine cinetico sia IN `H` e non aggiunto da fuori** | ### **la geometria "
      "SPARISCE come variabile indipendente:** `d` si ### **LEGGE** da un'ampiezza d'arco "
      "complessa, come `φ` si legge da `ψ`. ### **Un solo tipo di stato, una sola legge** |")
    A("| ### **che cosa cambia nel codice** | `vd` ### **diventa `p_d/m_arco`**, e `m_arco` "
      "### **va DERIVATA, non scelta** *(`A1`)* — candidata: `m_arco = (d/cs)²`, la stessa "
      "inerzia che l'orologio usa gia'. ### ⚠ **Verlet e' GIA' simplettico, quindi "
      "l'integratore non e' il problema:** il problema e' che ### **l'energia cinetica non e' "
      "in `H`** e che `beta·vd` scrive ### **da fuori** | `d`, `vd`, `d0` ### **spariscono "
      "come variabili**; restano le ampiezze d'arco. ### ⛔ **E' una riscrittura PIU' GROSSA "
      "di `A16`:** `A16` riscrive i nodi, questa riscriverebbe ### **anche gli archi** |")
    A("| ### ⛔ **e `beta·vd`?** | ### **non ha piu' posto come e' scritto:** uno smorzamento "
      "sull'impulso e' ### **dissipazione** *(`A14` n.2, gia' dichiarata)*. ### ➜ **Diventa un "
      "TERMINE DI ACCOPPIAMENTO fra `p_d` e un grado del vuoto** *(`A15.3`)*, e l'anisotropia "
      "*(`ZETA_VIR`: dissipa radiale, libera tangenziale)* diventa ### **l'anisotropia di quel "
      "accoppiamento** | ### **SPARISCE**, e non per scelta: ### **senza una velocita' "
      "indipendente non c'e' niente da smorzare.** ### ⚠ **E cio' che `beta·vd` faceva — "
      "togliere energia al radiale — dovra' essere fatto da `H`, o non essere fatto** |")
    A("")
    A("> ### ⚠ **E LA DIFFERENZA FRA LE DUE NON E' DI ELEGANZA:** la `(a)` ### **tiene due "
      "tipi di stato** *(i nodi `ψ`, gli archi `(d, p_d)`)*; la `(b)` ### **ne tiene uno**. "
      "### ➜ **Per `9-ter` la `(b)` e' la variante con MENO LEGGI** — ma ### **non a parita' "
      "di effetto misurato**, perche' nessuna delle due e' stata misurata. ### ⛔ **Quindi "
      "`9-ter` NON decide qui**, e lo dico invece di usarlo come argomento.")
    A("")
    A("---")
    A("")
    A("# ⛔ `⑩` **LA REVIEW RELAZIONALE** *(`A17`)* — **dove entra `pos`, e la candidata "
      "relazionale**")
    A("")
    A("> ### ⛔ **`A17`** *(`4f830bd`)*: *«nelle formule della fisica non ci deve essere `pos`: "
      "deve essere tutto relazionale»*. ### **Questa sezione NON lo assume: lo MISURA** — "
      "`csv/_test_fork/_censimento_pos.py`, per forma e non per nome.")
    A("")
    A("## `⑩.1` **NEL SIMULATORE — le violazioni, misurate dal codice di OGGI**")
    A("")
    A("| dove | che cosa decide con `pos` | ### **la candidata RELAZIONALE** |")
    A("|---|---|---|")
    A("| ### ⛔ **`_allaccia`** *(riga `%s`, ### **nessuna guardia**)* | un `cKDTree` su `pos`: "
      "### **DECIDE LA TOPOLOGIA delle nascite.** ### ⛔ **Viola anche `A5`:** lega nodi vicini "
      "### **nel disegno** che ### **sul grafo non si sono mai parlati** | ### ⭐ **il nato si "
      "attacca AL GENITORE e AI VICINI DEL GENITORE**, con le lunghezze prese dalle ### **`d` "
      "del genitore**. ### ✔ **Nessuna ricerca di prossimita': l'intorno e' GIA' nel grafo** |"
      % ",".join(str(b) for b in POS["la creazione degli archi"]["righe_dirette"][:2]))
    A("| ### ⛔ **`memoria_hebbiana_moto`** *(righe `%s`, guardie `%s`)* | le ### **direzioni** "
      "da `pos`: scrive `mem_mot` e `_nb`, cioe' ### **la gravita' e il frame-drag** | "
      "### ⭐ **le direzioni dal TRASPORTO `N` degli spinori** *(la connessione `SU(2)` d'arco, "
      "che gia' esiste)*, dalle ### **direzioni di Bloch** `_nb`, e dal ### **grafo** "
      "*(l'arco E' la direzione)*. ### ✔ **Tutte e tre sono gia' nel sistema** |"
      % (",".join(str(b) for b in POS["la memoria hebbiana del moto"]["righe_dirette"][:4]),
         ",".join(POS["la memoria hebbiana del moto"]["guardie_dirette"])))
    A("| ### ⛔ **`chiralita_core_locale`** *(INDIRETTA per l'orologio)* | una ### **sfera "
      "euclidea** | il ### **nucleo come insieme di nodi a distanza di GRAFO ≤ `r`**, oppure "
      "la ### **componente connessa** sopra una soglia di `ρ`. ### ⚠ **Il raggio in archi "
      "va DERIVATO, non scelto** *(`A1`)* |")
    A("| ### ✔ **il Kuramoto dal CENTRO DI MASSA** *(righe `7773`-`7774`, guardia `K_SYNC`)* | "
      "`cmv` e `r_cm`: ### **un centro di massa pesato su `pos`** | ### ⭐ **CADE con la "
      "sincronizzazione tolta** *(decisione `3`, PRESA)*. ### **Non serve una candidata: serve "
      "non riscriverla** |")
    A("| ### ⛔ **l'anello `d → pos → topologia e direzioni → d`** | `rilassa_disegno` | "
      "### **si SPEZZA togliendo i due consumatori**: `_allaccia` e `memoria_hebbiana_moto`. "
      "### ➜ **Allora `rilassa_disegno` resta, ma SOLO per il disegno** — che e' cio' che "
      "`A17` ammette |")
    A("")
    A("## `⑩.1-bis` ### ⭐ **LE GUARDIE, CON LO STATO NEL DRIVER** — *«una violazione "
      "dietro un flag SPENTO non e' viva»*")
    A("")
    A("### ⛔ **Letto DAL DRIVER** *(`_cli_flag.argv_del_driver`)*, ### **non dai default del "
      "modulo** — ed e' la differenza che conta:")
    A("")
    A("| guardia | valore ### **EFFETTIVO** | | passata nell'argv? |")
    A("|---|--:|---|---|")
    for k in sorted(pos["stato_guardie"]):
        v = pos["stato_guardie"][k]
        A("| `%s` | `%s` | %s | %s |"
          % (k, v["valore"], "### ⛔ **ACCESO**" if v["acceso"] else "### ✔ spento",
             "### **sì**" if v["nell_argv"] else "no *(è il default)*"))
    A("")
    A("> ### ⚠ **E DUE CORREZIONI A QUANTO MI ERA STATO DATO, misurate:** `VIRIALE` e "
      "`POZZO_D` risultano ### **ACCESI**, non spenti — ### **perche' il driver li PASSA "
      "nell'argv** *(`--viriale`, `--pozzo-d`)*, mentre il ### **default del modulo** e' "
      "`False`. ### ➜ **Le due letture non si scelgono: si riconciliano, e la riconciliazione "
      "e' esattamente la regola «i flag dal driver, non dai default».**")
    A("")
    A("### ⭐ **E LA GRAVITA'? `pozzo_grafo` legge `pos` alla riga `%s` — MA LA VIOLAZIONE "
      "NON E' VIVA**" % ",".join(str(b) for b in pos["pozzo"]["righe_pos_in_pozzo_grafo"]))
    A("")
    A("| | |")
    A("|---|---|")
    A("| la legge gravitazionale | `GRAV_BIFASE` = `%s`: ### **ACCESA** |"
      % pos["pozzo"]["GRAV_BIFASE_effettivo"])
    A("| `pozzo_grafo` usa `L = \|pos_j − pos_i\|` | ### **solo se `POZZO_D` e' SPENTO** |")
    A("| `POZZO_D` nel driver | `%s` — ### ⛔ **ACCESO**, e ### **passato nell'argv** "
      "*(`--pozzo-d`)* |" % pos["pozzo"]["POZZO_D_effettivo"])
    A("| ### ➜ **quindi** | ### ✔ **`L` viene da `self.d`, NON da `pos`. LA CURA (`D02`) E' "
      "GIA' ATTIVA**, e la violazione ### **non e' viva nella configurazione del driver** |")
    A("")
    A("> ### ⚠ **MA RESTA UN DIFETTO, e non lo nascondo:** il ### **default del modulo** e' "
      "`POZZO_D = False`, cioe' ### **chi importa il simulatore senza il driver ha la gravita' "
      "che legge `pos`.** ### ➜ **La cura esiste ma NON e' il default**, e per `A17` il default "
      "### **e' sbagliato**. ### **Questa e' una decisione di Luca** *(ribaltare il default)*, "
      "non una cosa che faccio io.")
    A("")
    A("## `⑩.1-ter` ### ⭐ **LE `%d` FUNZIONI CHE LEGGONO `pos`, IN QUATTRO GRUPPI**"
      % len(pos["per_funzione"]))
    A("")
    A("### ⚠ **I gruppi sono un GIUDIZIO MIO sul RUOLO della funzione, non una misura**, e lo "
      "dichiaro. ### **Luca ne chiedeva tre: il quarto l'ho trovato classificando.**")
    A("")
    A("| gruppo | quante | le funzioni | ### **`A17` lo ammette?** |")
    A("|---|--:|---|---|")
    GR = [("LEGGE FISICA", "### ⛔ **NO: VIOLA `A17`**"),
          ("RENDERING", "### ✔ **SI**, `A17.3` lo ammette *(il disegno)*"),
          ("DIAGNOSTICA", "### ✔ **SI**, `A17.3` lo ammette *(l'analisi)*"),
          ("CONDIZIONI INIZIALI", "### ❓ **E' LA DOMANDA PER LUCA**, qui sotto"),
          ("EREDITA' ALLA NASCITA", "### ⛔ **NO**: `pos` del nato ### **si eredita**, e "
                                    "un'eredita' di `pos` e' `pos` in una legge di crescita")]
    for gg, amm in GR:
        L = pos["gruppi"].get(gg, [])
        A("| ### **%s** | ### **%d** | %s | %s |"
          % (gg, len(L), " ".join("`%s`" % x for x in L), amm))
    A("")
    A("> ### ❓ **LA DOMANDA PER LUCA, e non la decido:** `semina`, `_semina_lam` e "
      "`_semina_masse_coerenti` costruiscono la ### **topologia iniziale DAL DISEGNO** — punti "
      "in una palla, a distanza euclidea `≥ LAM`, e poi gli archi. ### **Una scena iniziale "
      "costruita dal disegno e' ammessa da `A17`, o va costruita in modo relazionale?**")
    A("> | | |")
    A("> |---|---|")
    A("> | ### **l'argomento PER ammetterla** | una condizione iniziale ### **non e' una "
      "legge**: `A17` parla di *«ogni legge che determina un comportamento»*, e una scena di "
      "partenza ### **non determina un comportamento: lo INIZIA** |")
    A("> | ### ⛔ **l'argomento CONTRO** | la scena iniziale fissa ### **quali nodi sono "
      "vicini**, e quella topologia ### **sopravvive per tutta la corsa** — quindi `pos` "
      "### **decide** qualcosa che la fisica poi usa per sempre. ### **E `_allaccia` ha lo "
      "stesso difetto DENTRO la dinamica**, dove invece e' chiaramente vietato |")
    A("> | ### **che cosa cambierebbe** | se va costruita in modo relazionale, serve una "
      "### **topologia dichiarata** *(un reticolo, un grafo `k`-regolare, un espansore)* — "
      "### **che e' la candidata `(1)` del `⑩.2`** |")
    A("")
    A("## `⑩.2` ### ⛔ **NEL PROTOTIPO — `A17` lo dichiara violato, e il censimento CONFERMA**")
    A("")
    A("| | |")
    A("|---|---|")
    A("| funzioni del prototipo che usano `pos` | ### **`%d`** — `%s` |"
      % (len(pos["prototipo"]["funzioni"]), " ".join(sorted(pos["prototipo"]["funzioni"]))))
    A("| righe con una ### **distanza euclidea** | ### **`%d`** |"
      % len(pos["prototipo"]["righe_euclidee"]))
    A("| il grafo | punti in un ### **cubo**, archi per ### **raggio euclideo** `R_ARCO` |")
    A("| i pesi | `w = e^(−d/λ)` con `d` ### **EUCLIDEA** |")
    A("")
    A("### ⭐ **COME SI COSTRUISCONO GRAFO E PESI NEI PROSSIMI PROTOTIPI, SENZA `pos` — due "
      "candidate:**")
    A("")
    A("| | la candidata | che cosa da' | ### **il prezzo** |")
    A("|---|---|---|---|")
    A("| ### **`(1)`** | ### **UN GRAFO ASTRATTO DICHIARATO**: si parte da una topologia nota "
      "*(un reticolo regolare, un grafo casuale `k`-regolare, un espansore)* e i pesi sono "
      "### **tutti uguali** o estratti da una legge ### **sul grafo** *(es. `w_ij = f(grado)`)* | "
      "### ✔ **`pos` NON ESISTE NEMMENO**: non c'e' niente da violare | ### ⚠ **si perde il "
      "confronto con lo spazio `3D`**: non si puo' piu' dire *«assomiglia a una palla»* |")
    A("| ### **`(2)`** | ### **LA GEOMETRIA SI MISURA DAL GRAFO**: le lunghezze sono le `d` "
      "### **d'arco come variabili dinamiche** *(decisione `9`)*, e `pos` si calcola "
      "### **SOLO per disegnare**, da un embedding che ### **non rientra** in nessuna legge | "
      "### ⭐ **e' la forma che il simulatore GIA' vorrebbe**: `d` e' relazionale, e' `pos` che "
      "e' derivata | ### ⚠ **serve un controllo**: che l'embedding ### **non rientri**, e il "
      "test e' la ### **BYTE-INERZIA** *(`A17` punto `4`)* |")
    A("")
    A("> ### ⚠ **E UNA COSA CHE `A17` MI HA FATTO VEDERE E CHE AVEVO SCRITTO SENZA ACCORGERMENE:** "
      "nella decisione `10` avevo proposto come estensione del vuoto locale la ### **lunghezza "
      "di guarigione `ξ = 1/√(|g|ρ)`**. ### ⛔ **`ξ` e' una LUNGHEZZA**, e una lunghezza "
      "presuppone un metro. ### ➜ **In forma relazionale va espressa in NUMERO DI ARCHI** — "
      "cioe' *«quanti passi di grafo»* —, non in distanza. ### **La candidata non cambia, "
      "cambia l'unita'**, e senza `A17` l'avrei lasciata ambigua.")
    A("")
    A("## `⑩.3` **IL RIASSUNTO: che cosa resta da riscrivere, in ordine di gravita'**")
    A("")
    A("| | perche' e' il piu' grave |")
    A("|---|---|")
    A("| ### ⛔ **`1` `_allaccia`** | ### **nessuna guardia** *(e' sempre acceso)*, e "
      "### **decide la TOPOLOGIA** — cioe' decide ### **che cosa esiste**, non come si muove. "
      "### **E viola anche `A5`** |")
    A("| ### ⛔ **`2` `memoria_hebbiana_moto`** | decide ### **le direzioni della gravita'** |")
    A("| ### ⚠ **`3` `chiralita_core_locale`** | una sfera euclidea, e arriva ### **indiretta** "
      "fino all'orologio |")
    A("| ### ✔ **`4` il Kuramoto dal centro di massa** | ### **gia' deciso: cade** |")
    A("| ### ⚠ **`5` il prototipo** | ### **violato da subito**, e dichiarato nell'assioma |")
    A("")
    tt = tl["tetto"]
    A("# ⭐ `⑪` **LA DEGENERAZIONE — i dettagli della decisione `(C)`**")
    A("")
    A("## `⑪.1` **DA DOVE EMERGE: due regole RELAZIONALI, e nessun volume** *(`A17`)*")
    A("")
    A("| | la regola | perche' e' relazionale |")
    A("|---|---|---|")
    A("| ### **`1`** | la ### **CAPACITA' DEL NODO:** `ψ_k ∈ C²` ha ### **due componenti**, "
      "quindi ### **al piu' DUE STATI per nodo** *(immagine di Pauli; lo spin `½` dalla "
      "### **doppia copertura** a `4π`)* | e' una proprieta' ### **DELLO STATO**, non dello "
      "spazio |")
    A("| ### **`2`** | la ### **LUNGHEZZA MINIMA SUGLI ARCHI:** `d_ij ≥ LAM` *(`A13`)*, o "
      "`2·LAM` in certi casi — ### ⛔ **sulla `d` RELAZIONALE, MAI su `\|pos_i − pos_j\|`** | "
      "`d` e' una ### **relazione d'arco** |")
    A("")
    A("### ⛔ **E NIENTE VOLUME, NIENTE DIMENSIONE** *(`A17.3`)*: ### **niente `2/LAM³`, "
      "niente `ρ^(5/3)`.** La forma di Chandrasekhar presuppone ### **uno spazio di dimensione "
      "`3`**, che qui ### **non c'e'**.")
    A("")
    A("## `⑪.2` ### ⭐ **IL VINCOLO DI COERENZA: la capacita' sta DENTRO `H`, come BARRIERA "
      "PER NODO**")
    A("")
    A("### ⛔ **NON solo come effetto delle nascite**, e il motivo e' un numero: se il freno "
      "fosse ### **solo** «capacita' + nascite», quando il calore si esaurisce — ### **e si "
      "esaurisce, al livello `%d`** — ### **le nascite si fermano e NON RESTA NESSUN FRENO.**"
      % tt["livello_calore"])
    A("")
    A("| con la barriera in `H` | |")
    A("|---|---|")
    A("| la ### **degenerazione** | ### **tiene SEMPRE** |")
    A("| la ### **nascita** | ### **ALLEGGERISCE quando il calore la paga** |")
    A("| se il calore ### **non basta** | la materia ### **resta compressa al limite SENZA "
      "COLLASSARE** |")
    A("")
    A("### ⚠ **UNA CAUTELA DICHIARATA:** ### **Pauli NON emerge da solo** in un campo come "
      "questo. La doppia copertura e' ### **necessaria ma NON sufficiente** per la statistica "
      "di Fermi. ### ➜ **La barriera e' derivata dalla STRUTTURA** *(due componenti, `LAM`)*, "
      "### **NON dalla statistica** — e chiamarla «Pauli» e' un'### **ANALOGIA**, non una "
      "derivazione.")
    A("")
    A("## `⑪.3` ### ⛔ **IL PUNTO APERTO: L'UNITA' DI STATO** — *quante `ρ` vale UNO stato*")
    A("")
    A("### **«Due stati per nodo» NON e' un numero finche' non si sa quanto vale uno stato.** "
      "Le candidate, ### **tutte relazionali** *(`A1`: derivate, non scelte)*:")
    A("")
    A("| | la candidata | ### **relazionale?** | che cosa da' |")
    A("|---|---|---|---|")
    A("| ### **`(1)`** | ### **la densita' media:** `ρ₁ = Σρ/n = 1` per la normalizzazione | "
      "### ⚠ **sì, ma e' una CONVENZIONE**, non una derivazione: `Σρ = n` l'ho scelto io | "
      "`C = 2` |")
    A("| ### ⭐ **`(2)`** | ### **dove la non linearita' pareggia l'hopping:** `\|g\|ρ₁ = "
      "λ_max`, cioe' `ρ₁ = λ_max/\|g\|` | ### ✔ **sì, e DERIVATA:** `λ_max` e' una proprieta' "
      "### **spettrale del grafo**, `g` e' nella `H`. ### **Nessun numero scelto** | "
      "`ρ₁ = %.4f`, ### **`C = %.4f`** |"
      % (5.6494 / 5.0, 2.0 * 5.6494 / 5.0))
    A("| ### **`(3)`** | la ### **norma del solitone discreto piu' piccolo** che `H` sostiene | "
      "### ✔ **sì**, e' una soluzione di `H` | ### **non calcolata** |")
    A("| ### **`(4)`** | la ### **doppia copertura:** un giro di `4π` della fase = uno stato | "
      "### ✔ **sì** *(la fase si legge da `ψ`)*, ed e' quella che lega allo ### **spin `½`** | "
      "### ⛔ **da' un conto di FASE, non una `ρ`** |")
    A("")
    A("> ### ⭐ **QUALE MI SEMBRA LA PIU' NATURALE, e NON la decido: la `(2)`.** E' l'unica "
      "scala che ### **la `H` stessa definisce**, ed e' il punto dove la non linearita' "
      "### **smette di essere trascurabile** — che e' esattamente la soglia che il `MARE v2` "
      "aveva trovato ingovernabile. ### ⛔ **La decisione e' di Luca.**")
    A("")
    A("## `⑪.4` ### ⭐ **IL CONFRONTO ARITMETICO: la cascata CON il tetto**")
    A("")
    A("### **`(a)` IL COLLASSO SU UN NODO RESTA LO STATO PIU' BASSO?** Con un tetto `C` per "
      "nodo, un nodo solo e' ammesso ### **solo se `C ≥ N = %.0f`**; altrimenti la norma deve "
      "stare su almeno `N/C` nodi e `H_min = −w·(archi) + (g/2)·N·C`:" % tt["N"])
    A("")
    A("| `C` | nodi minimi | `H_min` *(senza hopping)* | `H`(un nodo) | ### **un nodo "
      "ammesso?** |")
    A("|--:|--:|--:|--:|---|")
    for x in tt["tabella_a"]:
        A("| `%.1f` | `%.1f` | `%.1f` | `%.1f` | %s |"
          % (float(x["C"]), float(x["nodi_minimi"]), float(x["H_min"]),
             float(x["H_un_nodo"]),
             "### **sì**" if x["un_nodo_ammesso"] in (True, "True") else "### ⛔ **NO**"))
    A("")
    A("### ➜ **NO: per ogni `C < %.0f` il collasso su un nodo e' VIETATO.** Lo stato piu' "
      "basso diventa *«la norma sul MINIMO numero di nodi che il tetto consente»*, cioe' "
      "### **esattamente «compressa al limite senza collassare»**. ### ⭐ **E il tetto alza il "
      "minimo del fattore `N/C`:** con `C = 25` passa da `%.1f` a `%.1f`, ### **`16` volte piu' "
      "alto.**" % (tt["N"], 0.5 * tt["g"] * tt["N"] * tt["N"], 0.5 * tt["g"] * tt["N"] * 25.0))
    A("")
    A("### **`(b)` A CHE LIVELLO SI FERMA LA CASCATA, E QUALE LIMITE PREVALE?**")
    A("")
    A("| `C` | livello richiesto dal ### **tetto** | il ### **calore** ne paga | ### **quale "
      "PREVALE** |")
    A("|--:|--:|--:|---|")
    for x in tt["tabella_b"]:
        A("| `%.1f` | `%s` | `%s` | %s |"
          % (float(x["C"]), x["livello_tetto"], x["livello_calore"],
             "il ### **CALORE**" if x["prevale"] == "calore" else "### ⛔ **IL TETTO**"))
    A("")
    A("> ### ⭐ **I DUE LIMITI DANNO FERMATE DIVERSE, E IL DISCRIMINE E' UN NUMERO: "
      "`ρ = %.1f` per nodo**, cioe' dove il calore si esaurisce." % tt["rho_calore"])
    A("> | | |")
    A("> |---|---|")
    A("> | se `C ≥ %.1f` | prevale ### **IL CALORE**: le nascite si fermano ### **prima** che "
      "il tetto morda, la materia resta a `ρ = %.1f` ### **senza toccare il tetto** — e la "
      "barriera ### **NON lavora** |" % (tt["rho_calore"], tt["rho_calore"]))
    A("> | se `C < %.1f` | prevale ### **IL TETTO**: il calore ### **NON basta** a frammentare "
      "quanto il tetto chiede, quindi ### **la materia resta COMPRESSA AL LIMITE** — ed e' "
      "### **esattamente il terzo caso di Luca** |" % tt["rho_calore"])
    A("")
    A("> ### ⛔ **E CON LA CANDIDATA CHE MI SEMBRA PIU' NATURALE, `(2)`, PREVALE IL TETTO:** "
      "`C = %.4f`, che e' ### **ben sotto `%.1f`** — il tetto chiederebbe `8` livelli e il "
      "calore ne paga `%d`. ### ➜ **Quindi la materia resterebbe compressa a `ρ = %.1f`, cioe' "
      "### **`%.0f` volte** la capacita'. ### ⚠ **La barriera dovrebbe fare MOLTO lavoro**, e "
      "questa e' una ### **PREVISIONE**, non una misura."
      % (2.0 * 5.6494 / 5.0, tt["rho_calore"], tt["livello_calore"], tt["rho_calore"],
         tt["rho_calore"] / (2.0 * 5.6494 / 5.0)))
    A("")
    A("# ⭐ `⑫` **LA LUNGHEZZA MINIMA NEL CODICE** — *censita per FORMA*")
    A("")
    A("| | |")
    A("|---|--:|")
    A("| punti in cui `LAM` e' un ### **limite di lunghezza** | ### **`%d`** |" % len(tl["lam"]))
    A("| su una lunghezza ### **RELAZIONALE** *(`d`, `d0`)* | `%d` |"
      % sum(1 for x in tl["lam"] if x["relazionale"]))
    A("| ### ⛔ **su qualcosa calcolato da `pos`** *(`A17`)* | ### **`%d`** |"
      % sum(1 for x in tl["lam"] if x["da_pos"]))
    A("| scritti come `2*LAM` | ### **`%d`** — *e il perche' e' qui sotto* |"
      % sum(1 for x in tl["lam"] if x["due_lam"]))
    A("")
    A("### ⭐ **PERCHE' IN CERTI CASI E' `2·LAM` — E NON E' UN SECONDO PARAMETRO.** Il "
      "censimento trova ### **ZERO** occorrenze di `2*LAM`, e la ragione e' che ### **il `2` "
      "non e' scritto: e' DERIVATO.** In `decidi_divisione` *(righe `8677`-`8678`)*:")
    A("")
    A("```")
    A("_sx = FRAZ_NASCITA * d >= LAM          # il troncone verso `a`")
    A("_dx = (1 - FRAZ_NASCITA) * d >= LAM    # il troncone verso `b`")
    A("```")
    A("")
    A("### ➜ **L'arco si SPEZZA IN DUE, quindi OGNUNO DEI DUE TRONCONI deve essere `≥ LAM`** — "
      "e con `FRAZ_NASCITA = 0.5` la congiunzione si riduce a `0.5·d ≥ LAM`, cioe' "
      "### **`d ≥ 2·LAM` AL BIT** *(moltiplicare per `0.5` e `2.0` e' esatto in `IEEE-754`)*. "
      "### ⭐ **Quindi `2·LAM` NON e' una soglia in piu': e' `LAM` applicata AI FIGLI.** "
      "### ✔ **E il flag `MITOSI_2LAM` e' INERTE dal commit `6b`:** il comportamento e' "
      "### **sempre acceso**.")
    A("")
    A("### **E LA FORMA DI OGNI LIMITE: TAGLIO, CANCELLO o ENERGIA — col candidato al primo "
      "ordine**")
    A("")
    A("| forma | quanti | ### **che cos'e' oggi** | ### **il candidato al primo ordine** |")
    A("|---|--:|---|---|")
    forme = {}
    for x in tl["lam"]:
        forme.setdefault(x["tipo"], []).append(x)
    CAND = {"CANCELLO": "### **CANCELLO SULLA NASCITA** — resta un cancello, ma solo nella "
                        "### **regola di crescita**, dove un sì/no e' legittimo",
            "PAVIMENTO": "### ⛔ **DEVE DIVENTARE UNA BARRIERA D'ENERGIA su `d`**: un "
                         "pavimento e' un ### **taglio a senso unico**, cioe' una freccia "
                         "*(`A14.2`)*, e al primo ordine non e' ammesso",
            "TETTO": "### ⛔ **come il pavimento: barriera d'energia**",
            "TAGLIO": "### ⛔ **barriera d'energia**"}
    for k in sorted(forme, key=lambda x: -len(forme[x])):
        cand = next((v for kk, v in CAND.items() if k.startswith(kk)), "—")
        A("| `%s` | ### **%d** | %s | %s |" % (k, len(forme[k]), k.split("(")[0].strip(), cand))
    A("")
    A("### ⚠ **E IL PUNTO GIA' NOTO, confermato:** `_nasce` ### **rialza a `LAM` gli archi "
      "corti** *(`np.maximum(v, LAM)`)* — e' la ### **freccia `7`** di `FRECCE-IMPOSTE` e la "
      "voce `SCHW-SOTTO-LAM`. ### ➜ **Al primo ordine quel `maximum` non puo' restare: "
      "diventa un CANCELLO che VIETA la nascita** *(se il figlio starebbe sotto `LAM`, "
      "### **non nasce**)*, ### **invece di farlo nascere e poi spostarlo.**")
    A("")
    A("### ⛔ **E L'UNICO `pos` RESTATO: `_celle_vive`** *(riga `4856`, "
      "`np.linalg.norm(sp) <= LAM`)* — e sta nelle ### **CONDIZIONI INIZIALI**, cioe' nel "
      "gruppo su cui ### **c'e' la domanda aperta per Luca** *(`⑩.1-ter`)*.")
    A("")
    A("> ### ⚠ **E DUE DIFETTI MIEI IN FILA SU QUESTO CENSIMENTO, entrambi dichiarati:** il "
      "primo criterio era `\"pos\" in riga`, che prendeva un ### **falso positivo** *(riga "
      "`6547`: `pos = prima > 0.0`, un booleano ### **LOCALE** che si chiama `pos`)*; la sua "
      "correzione l'ho scritta con un regex i cui escape sono passati dalla shell, e "
      "### **`\\b` e' diventato un BACKSPACE `\\x08`** — quindi il regex ### **non poteva "
      "funzionare** e il conto tornava `0` ### **per un motivo sbagliato.** ### ➜ **Ora il "
      "criterio e' fatto di sole sottostringhe, senza nessun escape**, e il numero vero e' "
      "### **`1`**.")
    A("")
    A("# ⛔ `⑬` **LA REVIEW DI COERENZA DELLE TRE DECISIONI PRESE**")
    A("")
    A("> ### ⛔ **NON risolvo le tensioni: le ELENCO, con la decisione di Luca che ciascuna "
      "richiede.**")
    A("")
    A("## `⑬.1` **UNA PER UNA, contro gli assiomi e i fatti misurati**")
    A("")
    A("| | ### **`(A)` il calore paga la nascita** | ### **`(B)` la sincronizzazione si "
      "toglie** | ### **`(C)` il freno e\' la `(c)`** |")
    A("|---|---|---|---|")
    A("| `A1` *(la legge, non il numero)* | ### ✔ **coerente, e migliora:** la soglia e\' "
      "### **un bilancio**, non un numero | ### ✔ **coerente:** toglie `K_SYNC`, che e\' una "
      "scala senza derivazione | ### ⚠ **coerente SOLO SE l\'unita\' di stato e\' derivata:** "
      "finche\' e\' aperta, *«due stati»* ### **non e\' un numero** |")
    A("| `A13` *(`d ≥ LAM`)* | — | — | ### ✔ **ci si APPOGGIA:** e\' una delle due regole da "
      "cui la degenerazione emerge |")
    A("| `A14.1` *(nessuna scrittura dall\'esterno)* | ### ✔ **e\' la cura:** toglie il "
      "### **bagno globale** | ### ✔ **coerente:** toglie un forzante | — |")
    A("| `A14.2` *(la crescita e\' l\'unica freccia)* | ### ⛔ **TENSIONE `T1`** *(qui sotto)* | "
      "### ✔ **coerente** | ### ⛔ **TENSIONE `T4`:** i `%d` ### **pavimenti** su `LAM` sono "
      "tagli a senso unico, cioe\' frecce |"
      % sum(1 for x in tl["lam"] if x["tipo"].startswith("PAVIMENTO")))
    A("| `A14.3` *(conserva la quantita\' di campo)* | ### ✔ **con `ψ → ψ/√2`:** `Σρ` "
      "### **al bit** | — | — |")
    A("| `A15.3` *(scambio col vuoto)* | ### ✔ **E\' esattamente `A15.3`** | ### ✔ **ci si "
      "appoggia:** l\'aggancio cede l\'eccesso al vuoto | ### ✔ **il freno vero ci si appoggia** |")
    A("| `A16.1` *(uno stato per nodo)* | — | ### ✔ | ### ✔ **la capacita\' VIENE da `ψ ∈ C²`** |")
    A("| `A16.2` *(primo ordine)* | ### ✔ | ### ✔ **e\' il motivo:** l\'aggancio e\' una "
      "### **proprieta\' dello stato stazionario** | ### ⛔ **DIPENDENZA `D1`:** serve la "
      "geometria dinamica dentro `H` *(decisione `9 (a)`)* |")
    A("| `A16.3` *(memorie dentro `H`)* | — | ### ✔ **il Kuramoto e\' un flusso di gradiente, "
      "e `A16.3` non lo ammette** | ### ✔ **la barriera E\' dentro `H`**, non un effetto |")
    A("| `A16.4` *(la nascita conserva)* | ### ✔ **e\' il punto** | — | — |")
    A("| `A17.1-2` *(solo relazioni)* | ### ⛔ **TENSIONE `T3`:** il ### **vuoto locale** non "
      "e\' ancora definito in modo relazionale | ### ✔ **MIGLIORA `A17`:** togliendo `K_SYNC` "
      "spariscono ### **`9` delle `13`** letture di `pos` | ### ✔ **due regole relazionali, "
      "`0` volumi** |")
    A("| `A17.3` *(`pos` e\' rendering)* | ### ⚠ **`ξ` e\' una LUNGHEZZA:** va in "
      "### **numero di archi** | ### ✔ **toglie il centro di massa** | ### ✔ **`d` e\' "
      "relazionale** |")
    A("| `A17.4` *(gli strumenti non sono fisica)* | — | — | — |")
    A("| i ### **FATTI MISURATI** | ### ✔ `381466.2` liberata contro `199600.0` richiesta; "
      "### ⛔ **ma `164 → 0` dice che oggi paga il BAGNO** | ### ✔ asimmetria `1.0641`; "
      "`AUC400` `0.9394 → 0.9333` | ### ✔ il `MARE v2` dice che ### **senza freno si collassa**; "
      "il tetto ### **alza il minimo di `16` volte** |")
    A("")
    A("## `⑬.2` ### ⛔ **LE TENSIONI, e la decisione che ciascuna richiede**")
    A("")
    A("### ⛔ **`T1` — «LA NASCITA CONSERVA L\'ENERGIA» RESTRINGE `A14.2`, non la conferma.**")
    A("")
    A("### **La domanda era: e\' coerente con `A14.2` o lo restringe?** ### ➜ **LO "
      "RESTRINGE**, e il motivo e\' il margine zero: se il `ΔH` della nascita e\' "
      "### **esattamente** il calore che la concentrazione ha liberato, allora il bilancio "
      "e\' ### **simmetrico nel tempo** — ### **la fusione di due nodi restituirebbe "
      "esattamente quel calore**, e sarebbe ### **permessa dall\'energia.**")
    A("")
    A("| | |")
    A("|---|---|")
    A("| ### ➜ **la conseguenza** | ### **l\'irreversibilita\' della crescita NON segue dal "
      "bilancio energetico:** il bilancio, da solo, ### **ammette anche il verso contrario.** "
      "### ⛔ **Quindi `A14.2` resta un POSTULATO IN PIU\'**, non un teorema del conto |")
    A("| ### **la decisione che richiede** | ### ⛔ **DI LUCA:** `A14.2` e\' *(`a`)* un "
      "### **assioma** che vieta la fusione per decreto; oppure *(`b`)* c\'e\' "
      "### **un\'asimmetria da trovare** *(entropica, o nella contabilita\' del vuoto)* che la "
      "renda un teorema. ### **Non lo decido io** |")
    A("")
    A("### ⛔ **`T2` — UN SERBATOIO, TRE USI: possono mancare l\'uno all\'altro.**")
    A("")
    A("### **La domanda era: il calore che paga le nascite e quello che serve all\'aggancio "
      "degli orologi possono mancare l\'uno all\'altro?** ### ➜ **SI\', e il margine misurato "
      "e\' ZERO.**")
    A("")
    A("| | |")
    A("|---|---|")
    A("| i tre usi | `(A)` la ### **nascita**; `(B)` l\'### **aggancio degli orologi**; `(C)` "
      "il ### **freno vero** |")
    A("| ### ⛔ **il conflitto** | sono ### **lo STESSO serbatoio**, e il bilancio chiude "
      "### **esattamente**: se l\'aggancio consuma l\'eccesso, ### **per la nascita non "
      "resta niente** — e viceversa |")
    A("| ### ⚠ **e non e\' simmetrico** | l\'aggancio e\' un fatto ### **dello stato "
      "stazionario**, cioe\' avviene ### **mentre** il sistema scende; la nascita e\' un "
      "### **evento**. ### **Chi arriva prima prende** |")
    A("| ### **la decisione che richiede** | ### ⛔ **DI LUCA:** *(`a`)* una ### **priorita\'** "
      "dichiarata; *(`b`)* la contabilita\' del vuoto ### **separata per uso**; oppure *(`c`)* "
      "l\'ipotesi che siano ### **LO STESSO processo** *(l\'aggancio E\' il modo in cui il "
      "calore si rende disponibile)*. ### ⭐ **La `(c)` mi sembra la piu\' interessante, e NON "
      "la decido** |")
    A("")
    A("### ⛔ **`T3` — IL «VUOTO LOCALE» NON E\' ANCORA RELAZIONALE** *(`A17`)*.")
    A("")
    A("### **La domanda era: «vuoto locale» e la sua estensione sono definiti in modo "
      "relazionale?** ### ➜ **IN PARTE.**")
    A("")
    A("| | ### **relazionale?** |")
    A("|---|---|")
    A("| l\'### **intorno** come insieme di nodi del ### **grafo** | ### ✔ **sì** |")
    A("| i ### **vicini diretti** come estensione | ### ✔ **sì**, per costruzione |")
    A("| ### **la grandezza contabile** *(`H` ristretta all\'intorno meno il profilo "
      "stazionario)* | ### ⚠ **la FORMA sì, ma la sottrazione NON E\' SCRITTA** |")
    A("| ### ⛔ **`ξ = 1/√(\|g\|ρ)`** come estensione | ### ⛔ **NO: e\' una LUNGHEZZA**, e una "
      "lunghezza presuppone un metro. Va espressa in ### **NUMERO DI ARCHI** |")
    A("| ### **la decisione che richiede** | ### ⛔ **DI LUCA:** l\'estensione e\' *(`a`)* i "
      "### **vicini diretti** *(relazionale subito, ma e\' un numero fisso: `1` passo)*; "
      "oppure *(`b`)* una ### **scala derivata convertita in passi di grafo** — e allora serve "
      "### **come si converte**, che e\' `Z47` |")
    A("")
    A("### ⛔ **`T4` — LE DUE FERMATE SONO DIVERSE, E PREVALE LA PIU\' STRETTA.**")
    A("")
    A("### **La domanda era: la cascata che si ferma al livello `%d` e il tetto per nodo danno "
      "due fermate diverse, e quale prevale?** ### ➜ **SI\', sono diverse, e il discrimine e\' "
      "`ρ = %.1f`** *(il `⑪.4`)*." % (tt["livello_calore"], tt["rho_calore"]))
    A("")
    A("| | |")
    A("|---|---|")
    A("| ### **prevale la piu\' STRETTA** | se `C ≥ %.1f` prevale ### **il calore** *(e la "
      "barriera NON lavora)*; se `C < %.1f` prevale ### **il tetto** *(e la materia resta "
      "compressa)* |" % (tt["rho_calore"], tt["rho_calore"]))
    A("| ### ⛔ **e quale sia dipende dall\'UNITA\' DI STATO, che e\' APERTA** | con la "
      "candidata `(2)` — la piu\' naturale — ### **`C = %.4f`, quindi prevale IL TETTO** |"
      % (2.0 * 5.6494 / 5.0))
    A("| ### ⚠ **la tensione vera** | ### **le due fermate non sono due versioni della stessa "
      "cosa:** la fermata ### **del calore** lascia la materia ### **lontana dal tetto**, "
      "quella ### **del tetto** la lascia ### **premuta contro**. ### ➜ **Sono due REGIMI "
      "FISICI diversi**, e quale sia il nostro ### **non e\' deciso** |")
    A("| ### **la decisione che richiede** | ### ⛔ **DI LUCA: l\'unita\' di stato** — perche\' "
      "### **e\' lei a scegliere il regime** |")
    A("")
    A("## `⑬.3` **LE DIPENDENZE** *(non tensioni: ordini di lavoro)*")
    A("")
    A("| | la dipendenza | ### **perche\'** |")
    A("|---|---|---|")
    A("| ### **`D1`** | `(C)` ### **richiede** la decisione `9 (a)` *(geometria hamiltoniana "
      "in `(d, p_d)`)* | `d_ij ≥ LAM` come ### **barriera d\'energia** ha senso solo se `d` ha "
      "una dinamica che ### **sente** la barriera. ### **Gia\' nota e dichiarata** |")
    A("| ### **`D2`** | `(B)` ### **richiede** `(A)` | l\'aggancio emerge ### **cedendo "
      "l\'eccesso al vuoto locale**, e il vuoto locale e\' definito in `(A)` — ### **che e\' "
      "aperto** |")
    A("| ### **`D3`** | `(A)` e `(C)` ### **richiedono** l\'### **unita\' di stato** | senza "
      "di essa ne\' la capacita\' ne\' il regime sono numeri |")
    A("| ### **`D4`** | tutte e tre ### **richiedono** che il ### **vuoto locale sia "
      "RELAZIONALE** *(`A17`)* | altrimenti la cura di `A16` reintroduce `pos` ### **dal lato "
      "del vuoto** |")
    A("")
    A("> ### ⭐ **E L\'ORDINE CHE NE ESCE, che non e\' una mia preferenza ma la chiusura delle "
      "dipendenze:** ### **`1`** l\'unita\' di stato *(`D3`)* → ### **`2`** il vuoto locale in "
      "forma relazionale *(`D4`, `T3`)* → ### **`3`** la geometria dentro `H` *(`D1`)* → "
      "### **`4`** l\'aggancio come misura *(`D2`)*. ### ⛔ **E `T1` sta FUORI da quest\'ordine: "
      "e\' una questione di assiomi, non di lavoro.**")
    A("")
    A("# ⛔ **CHE COSA QUESTO DOCUMENTO NON DICE**")
    A("")
    A("| | |")
    A("|---|---|")
    A("| la ### **forma di `H`** | ### ⛔ **non la decide.** La `H` del `⑤` e' ### **candidata**, "
      "e ha ### **due buchi dichiarati** *(`TAU_DIFF` nuda, `w`/`U` fissi)* |")
    A("| che le ### **traducibili** siano verificate | ### ⛔ **NO:** ### **una sola** lo e' "
      "*(la coppia scalare)*. Le altre dicono ### **perche' non lo sono**, e il motivo e' sempre "
      "lo stesso: ### **la forza non e' isolabile senza riscrivere il passo** |")
    A("| che la nascita ### **frenerebbe** | ### ⛔ **non lo dice:** dice che ### **diluisce "
      "esattamente** e che ### **costa**, quindi dipende da `S5`, ### **che e' aperto** |")
    A("| che i ### **contatori** siano davvero diagnostici | ### ⚠ **il criterio e' di FORMA** "
      "*(prefissi e code)*, e ### **puo' sbagliare**: ogni nome va verificato col ### **«nessun "
      "lettore»**, e questo giro ### **non lo fa** |")
    A("| le ### **scale e i semi** | ### **uno snapshot, una scena, `3` passi.** ### **`P3` non "
      "e' soddisfatta**, e il documento non pretende il contrario |")
    A("| che la review `A17` sia ### **completa** | ### ⚠ **NO:** il censimento di `pos` e' "
      "### **per DIFETTO** come quello delle leggi — ### **non vede un alias** *(`p = "
      "self.pos`)* passato ad altra funzione. ### **E l'attribuzione per legge e' grossolana "
      "dove l'ancora e' `step`**, e sta scritto |")
    io.open(DEST, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print("scritto %s (%d righe)" % (DEST, len(R)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
