# -*- coding: utf-8 -*-
"""**IL SIGILLO DEL `COMMIT 4`: il VELENO alle derivate.**

Criteri ### **fissati PRIMA dei numeri** *(par.(d) del piano, piu' il mandato del
2026-10-03)*:

| | il braccio | che cosa deve dire |
|---|---|---|
| **A** | lo ### **STATO e' byte-identico** sulle tre scene | e le ### **DERIVATE NO**, ed e' il prezzo ### **dichiarato e accettato** da Luca |
| **B** | il ### **CASO CHE DEVE FALLIRE** | si ### **toglie l'esenzione** a `_xi_rumore` ⇒ il veleno deve ### **ROMPERE** il run, ### **nel sito dichiarato, con voce e riga** |
| **C** | le ### **due esenti NON sono avvelenate** | dopo una nascita restano ### **CORTE**, senza `NaN` aggiunto |
| **D** | il ### **verdetto della COPERTURA** | citato dal referto ### **committato**, col suo blob — non ricalcolato a parole |

### ⚠ **PERCHE' `A` ESCLUDE LE DERIVATE, e non e' un allentamento**
Il veleno ### **cambia** le derivate: una che prima restava ### **CORTA** ora e' lunga e
piena di `NaN`. ### **Era prevedibile e Luca l'ha ACCETTATO**: *<<al passo della nascita il
sigillo del commit 4 confronta al byte lo STATO, NON le derivate -- e' il solo criterio
del piano che si restringe, ed e' una DECISIONE>>*.
### ✅ **E il braccio `A` NON si limita a escluderle: VERIFICA CHE DIFFERISCANO.** Se
le derivate fossero identiche, il veleno ### **non avrebbe fatto niente** e lo zero sullo
stato non significherebbe nulla — e' il ### **controllo positivo** del braccio.

**COMANDO:** `python csv/_seal_fork/_sigillo_veleno.py`
**USCITA:** `csv/_seal_fork/_sigillo_veleno/`
"""
import contextlib
import hashlib
import io
import json
import os
import sys
import traceback

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_QUI, ".."))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import numpy as np                 # noqa: E402
import _cli_flag                   # noqa: E402
import _passo                      # noqa: E402
import _confronto_nascita as CN    # noqa: E402

SIM = os.path.join(RADICE, "soliton_simulator.py")
FUORI = os.path.join(_QUI, "_sigillo_veleno")
NL = chr(10)
# ### L'ANCORA del <<prima>>: la CHIAMATA del veleno nel punto unico. E' il BERSAGLIO
#   (cio' che il commit 4 introduce), non il modo in cui e' scritta -- la lezione di
#   `6ab31f7`, dove un'ancora nominava la FORMULA e si e' rotta appena la formula
#   e' cambiata.
ANCORA = "_avvelena_derivate(net)"
# ### I CONTATORI DEL PRESIDIO, e si SEPARANO PER NOME e si RIPORTANO -- non si
#   escludono in silenzio. Il piano lo prescriveva e il primo giro non l'ha fatto:
#   *<<i contatori della MARCA sono <<del presidio>> e cambiano PER COSTRUZIONE: si
#   separano per NOME e si RIPORTANO, come gia' fatto per `_g_registro_*`>>*.
#   ### Nel simulatore di PRIMA questi nomi NON ESISTONO, quindi compaiono come
#   <<presente in UNO solo>> -- cinque in tutte e tre le scene, ed e' per questo che
#   il braccio `A` falliva.
#   ### \u26a0 E SI RIPORTANO, NON SI NASCONDONO: il referto li elenca a parte, e se
#   una differenza NON corrisponde a questi prefissi allora e' una differenza VERA
#   dello stato. Escluderli senza dirlo sarebbe indebolire il criterio.
PREFISSI_CONTATORI_VELENO = ("_g_veleno_", "_g_inv_veleno_")
# il caso che DEVE fallire: si toglie l'esenzione a `_g_rampa_prec`.
# ### E NON A `_xi_rumore`, e il motivo e' MISURATO: `_xi_rumore` ha shape (12802, 3),
#   cioe' DUE ASSI, quindi ### il ramo `multiasse` del veleno la salterebbe COMUNQUE --
#   e togliere la sua esenzione NON CAMBIEREBBE NIENTE. Il primo giro l'ha fatto, e il
#   braccio ha detto PASSA per DUE CONTATORI DEL VELENO: un caso che non discrimina.
#   ### `_g_rampa_prec` invece e' (12802,) 1-D float64, cioe' DAVVERO avvelenabile.
#   *(Il mandato diceva <<togli l'esenzione a UNA DELLE DUE>>.)*
# ### E L'EFFETTO ATTESO NON E' UNA CADUTA, e va previsto PRIMA: `_g_rampa_prec` e' la
#   SOLA derivata che NON sta in `DOMINI`, quindi il controllo di dominio non la guarda.
#   Avvelenarla rende VERA la guardia `len(_prec) == len(ramp)` al :5704, quindi
#   `ramp < _prec` confronta con `nan` e da' ### False IN SILENZIO -- e i contatori
#   diagnostici `_g_rampa_cali`, `_g_rampa_calo_somma`, `_g_rampa_calo_max` ### SMETTONO
#   DI SALIRE. ### Quella e' la differenza che il braccio deve vedere, e NON e' un
#   contatore del veleno: e' un contatore della DIAGNOSTICA, cioe' stato vero.
ESENZIONE = '("_g_rampa_prec", "nodo", "auto-rinfresco",'
SENZA_ESENZIONE = '("_g_rampa_prec", "nodo", "avvelena",'
# ### IL BRACCIO `E`: una legge scrive UNA CELLA AVVELENATA senza riscrivere l'array.
#   L'iniezione e' IN POSTO, quindi ### CONSERVA L'IDENTITA' dell'oggetto -- cioe' il
#   registro del veleno resta ### VIVO, ed e' esattamente il caso che l'esenzione per
#   cella deve NOMINARE: un NUMERO in una cella avvelenata.
ANCORA_CELLA = "    _avvelena_derivate(net)"
SCRITTURA_DI_CELLA = (
    "    _rt = (getattr(net, \'_veleno_registro\', None) or {}).get(\'_dt_e_ultimo\')\n"
    "    if _rt is not None and _rt[\'inizio\'] < len(net._dt_e_ultimo):\n"
    "        net._dt_e_ultimo[_rt[\'inizio\']] = 1.0   # CELLA SCRITTA, array NO")
# ### IL BRACCIO `F`: il veleno NON registra le celle. Allora il controllo non ha
#   niente a cui ancorare l'esenzione, e il run deve cadere ### COME CADEVA PRIMA
#   della via (a): al passo 42, su `_dt_e_ultimo`.
ANCORA_REGISTRO = ('        _vreg[nome] = {"arr": _nuovo, "inizio": int(_inizio), '
                   '"fine": int(bersaglio)}')
SENZA_REGISTRO = "        pass   # REGISTRO DEL VELENO TOLTO (caso che deve fallire)"
# le tre scene, le STESSE della misura della copertura.
SCENE = (("corta", 11, 72), ("lunga", 11, 150), ("altro_seme", 12, 72))
# il referto della copertura, da CITARE col suo blob (braccio `D`).
COPERTURA = os.path.join(RADICE, "csv", "_test_fork", "_copertura_derivate",
                         "_copertura_derivate.json")


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def carica(nome, seme, sim=None):
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=%d" % seme],
                                              dest=os.path.join(FUORI, "_scarto_" + nome))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome=nome, sim=sim)
        S._applica_regime(a)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    return S, S.net


def avanza(S, net, passi):
    """Avanza, e se CADE restituisce il passo, il tipo e la RIGA."""
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            for k in range(passi):
                _passo.passo_pieno(S, net)
        return None
    except Exception as e:
        tb = traceback.extract_tb(sys.exc_info()[2])
        dentro = [x for x in tb if "soliton_simulator" in (x.filename or "")]
        ultimo = dentro[-1] if dentro else (tb[-1] if tb else None)
        return {"passo": k + 1, "tipo": type(e).__name__, "messaggio": str(e)[:600],
                "voce": (ultimo.name if ultimo else None),
                "riga": (ultimo.lineno if ultimo else None),
                "codice": (ultimo.line if ultimo else None)}


def copia_con(dest, vecchio, nuovo, etichetta):
    t = io.open(SIM, encoding="utf-8", newline="").read()
    n = t.count(vecchio)
    if n != 1:
        raise SystemExit("** [%s] l'ancora e' presente %d volte (attesa 1). NON scrivo la "
                         "copia. **" % (etichetta, n))
    io.open(dest, "wb").write(t.replace(vecchio, nuovo).encode("utf-8"))
    a, b = t.split(NL), io.open(dest, encoding="utf-8", newline="").read().split(NL)
    if len(a) != len(b):
        return {"righe_prima": len(a), "righe_dopo": len(b)}
    return {"righe_diverse": [k + 1 for k, (x, y) in enumerate(zip(a, b)) if x != y]}


def derivate_di(sim):
    return [(v[0], v[1], v[2]) for v in sim.REGISTRO_DERIVATE]


def principale():
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    P = []

    def stampa(*x):
        s = " ".join(str(y) for y in x)
        P.append(s)
        print(s)

    stampa("=" * 104)
    stampa("IL SIGILLO DEL COMMIT 4: il VELENO alle derivate (via A, decisione di Luca)")
    stampa("=" * 104)
    stampa("simulatore ..... %s" % blob(SIM)[:8])
    stampa("questo sigillo . %s" % blob(os.path.abspath(__file__))[:8])
    stampa("regola in ...... csv/_confronto_nascita.py  %s"
           % blob(os.path.join(RADICE, "csv", "_confronto_nascita.py"))[:8])
    stampa("")

    # ---------- il <<prima>>: il PADRE del commit che introduce il veleno -----------------
    dest_prima = os.path.join(FUORI, "_sim_prima_veleno.py")
    prima, introduce = None, None
    try:
        introduce = _cli_flag.sim_prima_del_flag(ANCORA, dest_prima)
        prima = dest_prima
        stampa("il <<prima>> .. blob %s, dal PADRE di %s (l'ancora e' `%s`)"
               % (blob(prima)[:8], introduce[:8], ANCORA))
        stampa("    *(e `sim_prima_del_flag` ASSERISCE che l'ancora NON sia nel file estratto)*")
    except Exception as e:
        stampa("### IL <<PRIMA>> NON E' ESTRAIBILE: %s: %s" % (type(e).__name__, e))
        stampa("    (il veleno non e' ancora committato: il codice si committa PRIMA del run.)")
    stampa("")

    ref = {"blob_sim_sha1_byte": blob(SIM),
           "blob_sigillo": blob(os.path.abspath(__file__)),
           "ancora": ANCORA, "commit_che_introduce": introduce,
           "blob_prima": (blob(prima) if prima else None), "scene": []}

    # ---------- BRACCIO A: lo STATO byte-identico, le DERIVATE no --------------------------
    stampa("=" * 104)
    stampa("BRACCIO A -- lo STATO e' byte-identico sulle TRE scene; le DERIVATE no")
    stampa("=" * 104)
    A_ok, C_ok = (prima is not None), True
    for etichetta, seme, passi in SCENE:
        if prima is None:
            break
        SA, nA = carica("A_dopo_%s" % etichetta, seme)
        caduto = avanza(SA, nA, passi)
        if caduto:
            stampa("  ### IL RUN COL VELENO E' CADUTO, scena `%s`: %s"
                   % (etichetta, json.dumps(caduto, ensure_ascii=False, default=str)[:300]))
            stampa("  ### E' ESATTAMENTE CIO' CHE IL VELENO DEVE TROVARE: mi fermo e lo dico,")
            stampa("  ###   con la voce e la riga. NON lo aggiusto dentro questo giro.")
            A_ok = False
            ref["scene"].append({"etichetta": etichetta, "caduto_col_veleno": caduto})
            break
        fa, quali = CN.foto(SA, nA, sorgente=SIM)
        SB, nB = carica("A_prima_%s" % etichetta, seme, sim=prima)
        caduto_b = avanza(SB, nB, passi)
        if caduto_b:
            stampa("  ### IL RUN SENZA VELENO E' CADUTO: %s" % caduto_b)
            A_ok = False
            break
        fb, _ = CN.foto(SB, nB, sorgente=prima)
        der = {d[0] for d in derivate_di(SA)}
        stato_a = {k: v for k, v in fa.items() if k not in der}
        stato_b = {k: v for k, v in fb.items() if k not in der}
        _tutte = CN.confronta(stato_a, stato_b)
        # ### SI SEPARANO PER NOME E SI RIPORTANO (il piano lo prescriveva).
        d_presidio = [x for x in _tutte
                      if str(x.get("nome", "")).startswith(PREFISSI_CONTATORI_VELENO)]
        d_stato = [x for x in _tutte if x not in d_presidio]
        d_der = CN.confronta({k: v for k, v in fa.items() if k in der},
                             {k: v for k, v in fb.items() if k in der})
        ev = (int(getattr(nA, "_g_nati_mitosi_ev", 0)),
              int(getattr(nA, "_g_nati_schwinger_ev", 0)))
        stampa("  scena `%-11s` seme %d, %d passi, nascite %d/%d"
               % (etichetta, seme, passi, ev[0], ev[1]))
        stampa("      ### differenze sullo STATO ..... %d   (atteso 0)" % len(d_stato))
        for x in d_stato[:10]:
            stampa("          ### %s" % json.dumps(x, ensure_ascii=False, default=str)[:220])
        stampa("      contatori DEL PRESIDIO, separati e RIPORTATI: %d" % len(d_presidio))
        for x in d_presidio:
            stampa("          %s" % json.dumps(x, ensure_ascii=False, default=str)[:160])
        stampa("          *(cambiano PER COSTRUZIONE: nel simulatore di PRIMA questi nomi")
        stampa("            non esistono. Si RIPORTANO, non si nascondono -- e se una")
        stampa("            differenza non avesse questi prefissi sarebbe STATO VERO.)*")
        stampa("      differenze sulle DERIVATE ...... %d   (informazione, NON un criterio)"
               % len(d_der))
        stampa("          *(il primo giro CHIEDEVA che fossero > 0, ed era SBAGLIATO: nella")
        stampa("            scena `altro_seme` sono ZERO perche' le leggi avevano riscritto")
        stampa("            TUTTE le celle avvelenate prima della fine del run. Un controllo")
        stampa("            che puo' fallire senza che ci sia un difetto NON e' un controllo.)*")
        stampa("      veleno: voci %s, celle %s, esenti %s, gia' lunghe %s"
               % tuple(getattr(nA, c, 0) for c in
                       ("_g_veleno_voci", "_g_veleno_celle", "_g_veleno_esenti",
                        "_g_veleno_gia_lunga")))
        if not ev[0]:
            stampa("      ### NESSUNA MITOSI: zero differenze NON significa niente. NON MISURATO.")
        # ### IL CONTROLLO POSITIVO E' UN CONTATORE, non cio' che resta alla fine:
        #   `_g_veleno_celle > 0` dice che il veleno HA AGITO, e non dipende da quante
        #   celle le leggi hanno riscritto prima della fine del run.
        _celle = int(getattr(nA, "_g_veleno_celle", 0))
        stampa("      ### IL CONTROLLO POSITIVO: celle avvelenate = %d   (atteso > 0)" % _celle)
        ok = (not d_stato) and bool(_celle) and bool(ev[0])
        A_ok = A_ok and ok
        # ---------- BRACCIO C, sulla stessa foto: le due esenti NON avvelenate ----------
        esenti = [d[0] for d in derivate_di(SA) if d[2] == "auto-rinfresco"]
        righe_c = []
        for nome in esenti:
            v = getattr(nA, nome, None)
            if v is None:
                righe_c.append({"grandezza": nome, "stato": "assente"})
                continue
            v = np.asarray(v)
            nonfiniti = int(np.sum(~np.isfinite(v))) if v.dtype.kind == "f" else -1
            corta = len(v) < nA.n
            righe_c.append({"grandezza": nome, "len": int(len(v)), "n": int(nA.n),
                            "corta": bool(corta), "non_finiti": nonfiniti})
            if nonfiniti:
                C_ok = False
        stampa("      ### le due ESENTI, dopo il run:")
        for x in righe_c:
            stampa("          %-18s %s" % (x["grandezza"],
                                           json.dumps(x, ensure_ascii=False)[:150]))
        ref["scene"].append({"etichetta": etichetta, "seme": seme, "passi": passi,
                             "nascite": list(ev), "diff_stato": d_stato,
                             "n_diff_derivate": len(d_der),
                             "contatori_del_presidio": d_presidio,
                             "celle_avvelenate": int(getattr(nA, "_g_veleno_celle", 0)),
                             "esenti": righe_c,
                             "veleno": {c: getattr(nA, c, 0) for c in
                                        ("_g_veleno_voci", "_g_veleno_celle",
                                         "_g_veleno_esenti", "_g_veleno_gia_lunga",
                                         "_g_veleno_assenti", "_g_veleno_multiasse",
                                         "_g_veleno_non_float")}})
    stampa("")
    stampa("  ### BRACCIO A: %s" % ("PASSA" if A_ok else "FALLISCE"))
    stampa("  ### BRACCIO C: %s (le esenti non hanno NaN aggiunti dal veleno)"
           % ("PASSA" if C_ok else "FALLISCE"))
    stampa("")

    # ---------- BRACCIO B: il caso che DEVE fallire ----------------------------------------
    stampa("=" * 104)
    stampa("BRACCIO B -- IL CASO CHE DEVE FALLIRE: si toglie l'esenzione a `_xi_rumore`")
    stampa("=" * 104)
    stampa("  Il registro dichiara `_g_rampa_prec` AUTO-RINFRESCO perche' la guardia")
    stampa("  `if _prec is not None and len(_prec) == len(ramp):` (:5704) E' IL SUO SEGNALE.")
    stampa("  ### E NON USO `_xi_rumore`, e il motivo e' MISURATO: ha shape (12802, 3), cioe'")
    stampa("  ### DUE ASSI, quindi il ramo `multiasse` del veleno la salterebbe COMUNQUE --")
    stampa("  ### togliere la sua esenzione NON CAMBIEREBBE NIENTE. Il primo giro l'ha fatto,")
    stampa("  ### e il braccio ha detto PASSA per DUE CONTATORI DEL VELENO.")
    stampa("  ### E L'EFFETTO ATTESO NON E' UNA CADUTA, e lo prevedo PRIMA: `_g_rampa_prec` e'")
    stampa("  ### la SOLA derivata che NON sta in DOMINI, quindi il controllo di dominio non")
    stampa("  ### la guarda. Avvelenarla rende VERA la guardia, quindi `ramp < _prec` confronta")
    stampa("  ### con `nan` e da' False IN SILENZIO: i contatori `_g_rampa_cali`,")
    stampa("  ### `_g_rampa_calo_somma`, `_g_rampa_calo_max` SMETTONO DI SALIRE. ### Quella e'")
    stampa("  ### la differenza che questo braccio deve vedere, e NON e' un contatore del")
    stampa("  ### veleno: e' un contatore della DIAGNOSTICA, cioe' STATO VERO.")
    dest_b = os.path.join(FUORI, "_sim_senza_esenzione.py")
    B_ok, caduto_b2 = None, None
    try:
        diverse = copia_con(dest_b, ESENZIONE, SENZA_ESENZIONE, "braccio B")
        stampa("  la copia: %s" % json.dumps(diverse, ensure_ascii=False))
        SC, nC = carica("B_senza_esenzione", 11, sim=dest_b)
        caduto_b2 = avanza(SC, nC, 72)
        if caduto_b2:
            stampa("  ### IL RUN E' CADUTO, ed e' CIO' CHE DEVE SUCCEDERE:")
            stampa("      passo ..... %s" % caduto_b2["passo"])
            stampa("      ### voce .. %s" % caduto_b2["voce"])
            stampa("      ### riga .. %s" % caduto_b2["riga"])
            stampa("      codice .... %s" % caduto_b2["codice"])
            stampa("      tipo ...... %s" % caduto_b2["tipo"])
            stampa("      messaggio . %s" % caduto_b2["messaggio"][:300])
            B_ok = True
        else:
            # non e' caduto: allora la differenza DEVE essere misurabile nello stato
            fc, _ = CN.foto(SC, nC, sorgente=dest_b)
            SA2, nA2 = carica("B_sano", 11)
            avanza(SA2, nA2, 72)
            fa2, _ = CN.foto(SA2, nA2, sorgente=SIM)
            der2 = {d[0] for d in derivate_di(SA2)}
            d2 = CN.confronta({k: v for k, v in fa2.items() if k not in der2},
                              {k: v for k, v in fc.items() if k not in der2})
            gp = np.asarray(getattr(nC, "_g_rampa_prec", []))
            nonf = int(np.sum(~np.isfinite(gp))) if gp.size and gp.dtype.kind == "f" else 0
            # ### E I CONTATORI DEL VELENO NON CONTANO COME DIFFERENZA, ed e' il difetto
            #   che ha fatto passare questo braccio al primo giro: si separano, si
            #   RIPORTANO, e il criterio guarda SOLO il resto.
            d2_pres = [x for x in d2
                       if str(x.get("nome", "")).startswith(PREFISSI_CONTATORI_VELENO)]
            d2_vere = [x for x in d2 if x not in d2_pres]
            stampa("  il run NON e' caduto. Allora la differenza deve essere MISURABILE:")
            stampa("      ### `_g_rampa_prec` non finiti: %d   (len %d, n %d)"
                   % (nonf, len(gp), nC.n))
            stampa("      contatori DEL VELENO (separati, NON contano): %d" % len(d2_pres))
            for x in d2_pres:
                stampa("          %s" % json.dumps(x, ensure_ascii=False, default=str)[:160])
            stampa("      ### differenze VERE sullo stato: %d" % len(d2_vere))
            for x in d2_vere[:12]:
                stampa("          ### %s" % json.dumps(x, ensure_ascii=False, default=str)[:200])
            B_ok = bool(nonf) or bool(d2_vere)
            if not B_ok:
                stampa("  ### NE' CADUTO NE' DIVERSO (a parte i contatori del veleno):")
                stampa("  ###   togliere l'esenzione NON CAMBIA NIENTE, quindi l'esenzione")
                stampa("  ###   NON E' GIUSTIFICATA dal sigillo -- e questo e' un difetto")
                stampa("  ###   del DISEGNO, non del run.")
            if not B_ok:
                stampa("  ### ⛔ NE' CADUTO NE' DIVERSO: togliere l'esenzione non cambia")
                stampa("  ###   NIENTE, quindi l'esenzione NON E' GIUSTIFICATA dal sigillo")
                stampa("  ###   -- e questo e' un difetto del disegno, non del run.")
            caduto_b2 = {"caduto": False, "non_finiti_g_rampa_prec": nonf,
                         "contatori_del_veleno": d2_pres, "diff_vere": d2_vere}
    except SystemExit as e:
        stampa("  ### BRACCIO B NON ESEGUIBILE: %s" % e)
        B_ok = False
    stampa("  ### BRACCIO B: %s" % ("PASSA" if B_ok else "FALLISCE"))
    stampa("")

    # ---------- BRACCIO D: il verdetto della copertura, CITATO -----------------------------
    stampa("=" * 104)
    stampa("BRACCIO D -- IL VERDETTO DELLA COPERTURA, citato dal referto COMMITTATO")
    stampa("=" * 104)
    D_ok, cop = False, None
    if os.path.isfile(COPERTURA):
        cop = json.load(io.open(COPERTURA, encoding="utf-8"))
        stampa("  referto .. csv/_test_fork/_copertura_derivate/_copertura_derivate.json")
        stampa("      blob del referto ........... %s" % blob(COPERTURA)[:8])
        stampa("      girato sul simulatore ...... %s" % cop["blob_sim_sha1_byte"][:8])
        stampa("      ### IL VERDETTO ............ %s" % cop["verdetto"])
        stampa("      letture dall'AST %d, provate %d, NON provate %d"
               % (cop["totale_letture_ast"], cop["totale_provate"],
                  len(cop["non_provate"])))
        cl = {}
        for x in cop["non_provate"]:
            cl[x["classe"]] = cl.get(x["classe"], 0) + 1
        for k in sorted(cl):
            stampa("          %-30s %d" % (k, cl[k]))
        stampa("      controllo positivo della finestra (iniettato): %s"
               % cop["controllo_positivo_finestra_INIETTATO"]["passa"])
        stampa("  ### E IL VERDETTO NON SI RISCRIVE A PAROLE: si CITA, col blob del referto")
        stampa("  ###   e col blob del simulatore su cui e' girato. Un numero ricopiato non")
        stampa("  ###   ha provenienza (`L-NUMERI`).")
        D_ok = bool(cop["controllo_positivo_finestra_INIETTATO"]["passa"])
    else:
        stampa("  ### IL REFERTO DELLA COPERTURA NON C'E': il braccio D non e' eseguibile.")
    stampa("  ### BRACCIO D: %s" % ("PASSA" if D_ok else "FALLISCE"))
    stampa("")

    # ---------- BRACCIO E: una cella avvelenata SCRITTA, l'array NO ------------------------
    stampa("=" * 104)
    stampa("BRACCIO E -- UNA CELLA AVVELENATA SCRITTA senza riscrivere l'array")
    stampa("=" * 104)
    stampa("  L'iniezione e' IN POSTO (`net._dt_e_ultimo[inizio] = 1.0`), quindi CONSERVA")
    stampa("  l'identita' dell'oggetto: il registro del veleno resta VIVO. ### E allora")
    stampa("  l'esenzione per cella DEVE NOMINARE quella cella, perche' un NUMERO li' vuol")
    stampa("  dire che qualcuno ha scritto UNA CELLA senza riscrivere la derivata.")
    stampa("  ### E' il SECONDO VERSO della strettezza: senza di lui l'esenzione")
    stampa("  ### ammetterebbe tutto, ed e' `A9` (un presidio che ammette tutto non")
    stampa("  ### impedisce niente).")
    dest_e = os.path.join(FUORI, "_sim_cella_scritta.py")
    E_ok, caduto_e = None, None
    try:
        diverse_e = copia_con(dest_e, ANCORA_CELLA,
                              ANCORA_CELLA + NL + SCRITTURA_DI_CELLA, "braccio E")
        stampa("  la copia: %s" % json.dumps(diverse_e, ensure_ascii=False))
        SE, nE = carica("E_cella_scritta", 11, sim=dest_e)
        caduto_e = avanza(SE, nE, 72)
        if caduto_e:
            nomina = "_dt_e_ultimo" in (caduto_e["messaggio"] or "")
            cella = "AVVELENATE" in (caduto_e["messaggio"] or "")
            stampa("  ### IL RUN E' CADUTO, ed e' CIO' CHE DEVE SUCCEDERE:")
            stampa("      passo %s, voce `%s`, riga %s"
                   % (caduto_e["passo"], caduto_e["voce"], caduto_e["riga"]))
            stampa("      tipo ...... %s" % caduto_e["tipo"])
            stampa("      messaggio . %s" % (caduto_e["messaggio"] or "")[:420])
            stampa("      ### nomina `_dt_e_ultimo`? %s" % ("SI" if nomina else "NO"))
            stampa("      ### e dice che e' una CELLA AVVELENATA? %s"
                   % ("SI" if cella else "NO"))
            E_ok = bool(nomina)
        else:
            stampa("  ### IL RUN NON E' CADUTO: l'esenzione per cella AMMETTE un NUMERO")
            stampa("  ###   dove deve esserci `nan`, cioe' ammette TUTTO (`A9`).")
            E_ok = False
    except SystemExit as e:
        stampa("  ### BRACCIO E NON ESEGUIBILE: %s" % e)
        E_ok = False
    stampa("  ### BRACCIO E: %s" % ("PASSA" if E_ok else "FALLISCE"))
    stampa("")

    # ---------- BRACCIO F: il veleno NON registra le celle ---------------------------------
    stampa("=" * 104)
    stampa("BRACCIO F -- IL VELENO NON REGISTRA LE CELLE: il run deve cadere COME PRIMA")
    stampa("=" * 104)
    stampa("  Senza il registro il controllo non ha niente a cui ancorare l'esenzione, e il")
    stampa("  run deve cadere come cadeva PRIMA della via (a): al passo 42, su")
    stampa("  `_dt_e_ultimo` che viola `> 0`. ### E' il CONTROLLO POSITIVO DEL REGISTRO:")
    stampa("  ### se il run passasse anche senza registro, l'esenzione non sarebbe ancorata")
    stampa("  ### a niente e il braccio A non proverebbe nulla.")
    dest_f = os.path.join(FUORI, "_sim_senza_registro.py")
    F_ok, caduto_f = None, None
    try:
        diverse_f = copia_con(dest_f, ANCORA_REGISTRO, SENZA_REGISTRO, "braccio F")
        stampa("  la copia: %s" % json.dumps(diverse_f, ensure_ascii=False))
        SF, nF = carica("F_senza_registro", 11, sim=dest_f)
        caduto_f = avanza(SF, nF, 72)
        if caduto_f:
            stampa("  ### IL RUN E' CADUTO, ed e' CIO' CHE DEVE SUCCEDERE:")
            stampa("      passo %s, voce `%s`, riga %s"
                   % (caduto_f["passo"], caduto_f["voce"], caduto_f["riga"]))
            stampa("      messaggio . %s" % (caduto_f["messaggio"] or "")[:320])
            stampa("      ### al passo 42, come prima della via (a)? %s"
                   % ("SI" if caduto_f["passo"] == 42 else
                      "### NO, al passo %s" % caduto_f["passo"]))
            F_ok = "_dt_e_ultimo" in (caduto_f["messaggio"] or "")
        else:
            stampa("  ### IL RUN NON E' CADUTO senza il registro: allora l'esenzione NON e'")
            stampa("  ###   ancorata al registro, e il braccio A non prova niente.")
            F_ok = False
    except SystemExit as e:
        stampa("  ### BRACCIO F NON ESEGUIBILE: %s" % e)
        F_ok = False
    stampa("  ### BRACCIO F: %s" % ("PASSA" if F_ok else "FALLISCE"))
    stampa("")

    passa = (bool(A_ok) and bool(C_ok) and bool(B_ok) and bool(D_ok)
             and bool(E_ok) and bool(F_ok))
    stampa("=" * 104)
    stampa("### IL SIGILLO %s   (A %s · B %s · C %s · D %s · E %s · F %s)"
           % ("PASSA" if passa else "FALLISCE",
              "OK" if A_ok else "NO", "OK" if B_ok else "NO",
              "OK" if C_ok else "NO", "OK" if D_ok else "NO",
              "OK" if E_ok else "NO", "OK" if F_ok else "NO"))
    stampa("=" * 104)
    ref.update({"passa": bool(passa), "braccio_A": bool(A_ok), "braccio_B": B_ok,
                "braccio_C": bool(C_ok), "braccio_D": bool(D_ok),
                "braccio_E": E_ok, "braccio_E_dettaglio": caduto_e,
                "braccio_F": F_ok, "braccio_F_dettaglio": caduto_f,
                "braccio_B_dettaglio": caduto_b2,
                "copertura_citata": ({"blob_referto": blob(COPERTURA),
                                      "blob_sim": cop["blob_sim_sha1_byte"],
                                      "verdetto": cop["verdetto"]} if cop else None)})
    io.open(os.path.join(FUORI, "_sigillo_veleno.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(ref, indent=1, default=str))
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(P) + NL)
    return 0 if passa else 1


if __name__ == "__main__":
    sys.exit(principale())
