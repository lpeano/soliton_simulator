# -*- coding: utf-8 -*-
r"""GLI EMETTITORI DELLA CAMMINATA — **i LEGAMI e l'ORDINE.**

> ### ⛔ **QUESTO FILE NASCE DA UN PRESIDIO, come il suo gemello dello schema.**
> Con questi due emettitori dentro, `_genera.py` arrivava a **`745` righe** contro un
> tetto di **`700`**, e la regola e' *<<oltre SI DIVIDE, NON SI ALLUNGA>>*.

### ⭐ **E LA DIVISIONE SEGUE UN MODELLO CHE IL REPO HA GIA':** `_genera_stato.py`
e' l'emettitore dello stato, e sta a parte per la stessa ragione. ### **Questo e'
l'emettitore della camminata.**

### ⚠ **E NON IMPORTA `_genera.py`:** riceve cio' che serve **come argomenti**,
perche' un ciclo di import fra l'orchestratore e un suo emettitore renderebbe
**l'ordine di caricamento una proprieta' del generato.**
"""

NL = chr(10)


def modulo_legame(legge, imp):
    """### Il modulo di un `pezzo_unitario` o di un `flusso`: ### **un LEGAME, non uno
    stub.**

    ### ⛔ **E LA DIFFERENZA CONTA.** Un *stub* finge di fare una cosa e non la fa; un
    ### **legame** dichiara ### **che cosa va fatto e da chi**, e ### **non finge niente**:
    `applica()` chiede l-operatore ### **al motore**, e se il motore non ce l-ha
    ### **ALZA** invece di tornare un risultato finto.

    ### ⭐ **PERCHE- IL CODICE NON CONTIENE LA FORMULA:** un `pezzo_unitario` non e-
    un-espressione *(e- il posto `P4`)*, e un `flusso` ha il suo generatore ### **in
    tabella** -- quindi il modulo generato porta ### **i DATI della legge** e la
    ### **chiamata**, e la formula resta ### **dove e- l-unica fonte.**
    """
    tipo = legge["tipo"]
    L = ["# -*- coding: utf-8 -*-",
         '"""GENERATO da `primo_ordine/leggi/leggi.yaml` - NON si modifica a mano.',
         "",
         "### **%s** -- `%s`" % (legge["id"], tipo),
         "",
         (legge.get("scheda") or "").strip(),
         "",
         "### ⛔ **QUESTO MODULO E- UN LEGAME, non uno stub:** `applica()` chiede",
         "l-operatore ### **al motore**, e se il motore non ce l-ha ### **ALZA** -- non",
         "torna un risultato finto.",
         '"""',
         "",
         "IMPRONTA = %r" % imp,
         # ### ⚠ **LA COSTANTE SI CHIAMA `LEGGE` E NON `ID`, ed e- la CONVENZIONE
         # ### DEL REPO:** la biiezione riconosce un file generato ### **leggendo la
         # ### costante `LEGGE` via AST.** ### **Chiamandola `ID` i miei sette moduli
         # ### erano INVISIBILI alla biiezione**, e il presidio diceva <<manca un file
         # ### generato>> su file che esistevano.
         "LEGGE = %r" % legge["id"],
         "TIPO = %r" % tipo,
         # ### ⚠ **LA TUPLA VA INCAPSULATA, e il `%` me l-ha insegnato:** a destra
         # ### di un `%` ### **una tupla e- la LISTA DEGLI ARGOMENTI**, non un valore --
         # ### quindi `%r % (a, b)` cerca ### **due** segnaposti e ne trova ### **uno.**
         "AMBITO = %r" % (tuple(legge.get("ambito") or ()),),
         "PARAMETRI = %r" % ({k: v.get("valore")
                              for k, v in (legge.get("parametri") or {}).items()},),
         "POSTO = %r" % (legge.get("posto") or None),
         "VOCE_DECISIONE = %r" % (legge.get("voce_decisione") or None),
         ""]
    if tipo == "pezzo_unitario":
        L += ["OPERATORE = %r" % legge["operatore"],
              "AZIONE = %r" % legge["azione"],
              ""]
    else:
        L += ["GENERATORE = %r" % legge["generatore"],
              "ESATTO = %r" % bool(legge.get("esatto")),
              ""]
    L += ["",
          "def applica(st, motore, frazione):",
          '    """### Applica questo pezzo allo stato, ### **tramite il MOTORE.**',
          "",
          "    ### ⛔ **NON fa la fisica qui dentro:** la fisica e- ### **un",
          "    operatore del motore**, e questo modulo e- ### **il legame fra la tabella",
          "    e lui.**",
          '    """',
          "    quale = %s" % ("OPERATORE" if tipo == "pezzo_unitario" else "LEGGE"),
          "    fai = getattr(motore, 'operatori', {}).get(quale)",
          "    if fai is None:",
          # ### ⚠ **E QUESTE RIGHE LE HO SBAGLIATE AL PRIMO GIRO:** il messaggio
          # ### dell-eccezione era spezzato ### **lasciando una stringa APERTA**, e il
          # ### modulo GENERATO non compilava. ### **L-ha preso il collaudo del grafo**,
          # ### che importa i termini -- cioe- ### **un errore nel generatore si vede
          # ### dove il generato viene USATO**, non dove viene scritto.
          "        raise NotImplementedError(",
          "            'il motore non ha l-operatore ' + repr(quale)",
          "            + ': questo modulo e- un LEGAME, e un legame senza il suo'",
          "            + ' operatore ALZA invece di tornare un risultato finto')",
          "    return fai(st, PARAMETRI, frazione)",
          ""]
    return NL.join(L) + NL


def modulo_composizione(ordine, leggi, imp):
    """### L-ORDINE come ### **DATO**, e non come un secondo esecutore.

    ### ⛔ **E IL MOTIVO E- UN PRESIDIO:** `P-ES1` dice che l-esecutore e-
    ### **UNO SOLO** *(`primo_ordine/passo.py`)*, quindi generare qui una seconda
    funzione `passo()` ### **lo violerebbe.** ### ✅ **Il passo e- l-ordine della
    tabella**, e l-esecutore ### **lo legge.**
    """
    per_id = {x["id"]: x for x in leggi}
    L = ["# -*- coding: utf-8 -*-",
         '"""GENERATO da `primo_ordine/leggi/leggi.yaml` - NON si modifica a mano.',
         "",
         "### ⭐ **L-ORDINE DI COMPOSIZIONE, come DATO.** Il passo ### **E-** questa",
         "lista, e l-esecutore unico la legge: generare qui una seconda funzione",
         "`passo()` violerebbe il presidio che dice ### **un solo esecutore.**",
         "",
         "### ⛔ **E le RIPETIZIONI sono il punto:** la composizione di Strang usa",
         "### **lo stesso pezzo DUE VOLTE**, e la somma delle frazioni di una legge",
         "### **fa `1` esatto** -- lo schema lo verifica.",
         '"""',
         "",
         "IMPRONTA = %r" % imp,
         "",
         "# ### `(id della legge, frazione di passo, tipo)`",
         "ORDINE = ("]
    for e in ordine:
        idl = str(e["legge"])
        L.append("    (%r, %r, %r)," % (idl, e["frazione"],
                                        per_id[idl]["tipo"]))
    L += [")",
          "",
          "",
          "def leggi_in_ordine():",
          '    """### Gli `id` nell-ordine, ### **con le ripetizioni.**"""',
          "    return tuple(x[0] for x in ORDINE)",
          ""]
    return NL.join(L) + NL
