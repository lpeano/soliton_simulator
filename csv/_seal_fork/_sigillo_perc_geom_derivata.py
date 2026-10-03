# -*- coding: utf-8 -*-
"""**IL SIGILLO DEL `COMMIT 5`: `perc_geom` del nato come DERIVAZIONE.**

### CINQUE BRACCI, e due non erano nel mandato.

| | braccio | che cosa decide |
|---|---|---|
| **A** | il ### **RIORDINO DA SOLO** *(vincolo 4, eredita' INVARIATA)* deve essere ### **BYTE-IDENTICO** | separa *<<ho spostato una riga>>* da *<<ho cambiato una legge>>*. ### **Senza questo braccio i due effetti sono MESCOLATI** |
| **B** | la ### **CURA INTERA** contro il *prima*, sulle ### **TRE scene** | il criterio `(a)`-`(d)` del mandato |
| **C** | il ### **contatore `-1`/`+1`** della derivazione, ### **misurato** | il mandato lo pretende |
| **D** | ### **IL CASO CHE DEVE FALLIRE, per i DUE EVENTI SEPARATAMENTE** | ### **riformulato**, vedi sotto |
| **E** | ### **IL CONTROLLO POSITIVO: `tw` sopra soglia ⇒ `+1`** | ### **senza, un *<<sempre -1>>* non distingue una DERIVAZIONE da una COSTANTE** |

## ⛔ **PERCHE' IL BRACCIO `D` E' RIFORMULATO, e lo dico invece di aggiustarlo in silenzio**

Il mandato chiede: *<<una copia che lascia l'eredita' in UN evento deve essere vista dal sigillo
nel primo passo con nascita di quell'evento>>*. ### **OGGI QUELLA FORMA NON PUO' DISCRIMINARE:**
il censimento *(`e12158b`)* ha misurato ### **`1225` nati con eredita' `-1` E derivazione `-1`** --
cioe' le due regole ### **danno lo stesso valore**, e lasciare l'eredita' ### **non produce
NESSUNA differenza.** ### **Un controllo che non PUO' fallire non e' un controllo: e' un allarme
fisso.**

### ✅ **LA FORMA CHE DISCRIMINA: SI COSTRUISCE IL CASO.** Nelle copie `D` e `E` si inietta
`tw = 20` *(sopra `PHI_CRIT = 2π ≈ 6.283`)* sui nuovi archi, cosi' la ### **derivazione da' `+1`**
mentre l'### **eredita' resta `-1`** -- e allora *<<lasciare l'eredita' in un evento>>* si
### **vede.** ### 📌 **E' la tecnica dell'ulp iniettato: il caso che serve NON SI SPERA, SI
COSTRUISCE.**

## IL *PRIMA* NON VIENE DA `HEAD` *(`H-P8`)*

Si usa `_cli_flag.sim_prima_del_flag("_derivazione_perc_geom", …)`, che ### **trova il commit che
introduce l'ancora e prende il suo PADRE** -- e ### **asserisce che il file estratto NON contenga
l'ancora.** Prendere *<<il prima>>* da `HEAD` sarebbe, dal commit della cura in poi, ### **il
braccio OFF di se stesso.**

**COMANDO:** `python csv/_seal_fork/_sigillo_perc_geom_derivata.py`
**USCITA:** `csv/_seal_fork/_sigillo_perc_geom_derivata/`
"""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_QUI, ".."))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import numpy as np   # noqa: E402
import _cli_flag     # noqa: E402
import _passo        # noqa: E402

SIM = os.path.join(RADICE, "soliton_simulator.py")
FUORI = os.path.join(_QUI, "_sigillo_perc_geom_derivata")
PATCH = os.path.join(_QUI, "_perc_geom_patch.py")
NL = chr(10)
ANCORA = "_derivazione_perc_geom"
# ### LE TRE SCENE DEL COMMIT 4, e sono un DATO di questo sigillo
SCENE = (("corta", 11, 72), ("lunga", 11, 150), ("altro_seme", 12, 72))
# ### I CONTATORI NUOVI, dichiarati: sono le SOLE differenze ammesse nel braccio `B`
CONTATORI_NUOVI = ("_g_pgeom_der_m1", "_g_pgeom_der_p1")


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def carica(percorso, nome):
    spec = importlib.util.spec_from_file_location(nome, percorso)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def costruisci(m, seme, dest):
    """Scena `MASSE-COERENTI`, dal CLI del driver: nessun attributo a mano (`H-P3`)."""
    _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=%d" % seme], dest=dest)
    vecchia = list(sys.argv)
    sys.argv = list(argv)
    try:
        a = m._cli()
        m._applica_flag(a)
    finally:
        sys.argv = vecchia
    m._applica_regime(a)
    m._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
    m._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
    m._NMASSE_VIDEO["size"] = None
    m.avvia_test("MASSE-COERENTI")()
    return m.net


def stato(net):
    """TUTTI gli ndarray e gli scalari di `__dict__`: non un insieme scelto da me.

    ### NESSUNA COPIA, e il motivo e' che il confronto e' IMMEDIATO: i due stati
    vengono da OGGETTI DIVERSI *(due moduli caricati a parte)*, quindi non c'e'
    aliasing, e copiare ~273 array per passo per tre simulatori sarebbe
    ### **la parte piu' costosa del sigillo, per niente.**
    ### ⚠ Il prezzo e' che uno `stato()` NON si puo' conservare fra i passi:
    chi lo volesse deve copiare. Qui non serve.
    """
    fuori = {}
    for k, v in vars(net).items():
        if isinstance(v, np.ndarray):
            fuori[k] = v
        elif isinstance(v, (int, float, bool, np.integer, np.floating)):
            fuori[k] = v
    return fuori


def confronta(s1, s2):
    """Le differenze, per NOME. Separa *<<assente di qua>>* da *<<diverso>>*."""
    diff = []
    for k in sorted(set(s1) | set(s2)):
        if k not in s1:
            diff.append((k, "SOLO NEL SECONDO"))
            continue
        if k not in s2:
            diff.append((k, "SOLO NEL PRIMO"))
            continue
        a, b = s1[k], s2[k]
        if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
            a = np.asarray(a)
            b = np.asarray(b)
            if a.shape != b.shape:
                diff.append((k, "FORMA %s contro %s" % (a.shape, b.shape)))
            elif a.dtype.kind in "fc" or b.dtype.kind in "fc":
                if not np.array_equal(a, b, equal_nan=True):
                    m = ~((a == b) | (np.isnan(a) & np.isnan(b))) if a.dtype.kind == "f" \
                        else (a != b)
                    diff.append((k, "%d celle su %d" % (int(np.sum(m)), a.size)))
            elif not np.array_equal(a, b):
                diff.append((k, "%d celle su %d" % (int(np.sum(a != b)), a.size)))
        else:
            if a != b and not (a != a and b != b):
                diff.append((k, "%r contro %r" % (a, b)))
    return diff


def prima_del_flag(dest):
    """Il *prima*, dal PADRE del commit che introduce l'ancora (`H-P8`)."""
    return _cli_flag.sim_prima_del_flag(ANCORA, dest, radice=RADICE)


def copia_patchata(sorgente, dest, argomenti):
    """Una COPIA col patch applicato, e il patch e' COMMITTATO.

    ### ⛔ LA SORGENTE E' SEMPRE IL *PRIMA*, MAI IL SIMULATORE DI OGGI, e il primo
    giro del sigillo e' caduto proprio su questo: ### **le ancore della patch
    descrivono il codice PRIMA della cura**, quindi applicarla al simulatore ### **gia'
    curato** non trova niente -- e l'`assert` dell'ancora unica ha fermato il sigillo
    invece di produrre una copia a meta'. ### ✅ **Il presidio ha funzionato: era il
    disegno a essere sbagliato.**
    """
    byte = io.open(sorgente, "rb").read()
    io.open(dest, "wb").write(byte)
    q = subprocess.run([sys.executable, PATCH, "--file=%s" % dest] + list(argomenti),
                       capture_output=True, text=True)
    assert q.returncode == 0, (q.stdout or "")[-2000:] + (q.stderr or "")[-2000:]
    return dest


def principale():
    righe = []

    def stampa(*x):
        s = " ".join(str(y) for y in x)
        righe.append(s)
        print(s)

    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    esito = {"blob_sim": blob(SIM), "blob_sigillo": blob(os.path.abspath(__file__))}

    stampa("=" * 100)
    stampa("IL SIGILLO DEL COMMIT 5: `perc_geom` del nato come DERIVAZIONE")
    stampa("=" * 100)
    stampa("  simulatore di OGGI (la cura) .. %s" % blob(SIM)[:8])
    stampa("  questo sigillo ................ %s" % blob(os.path.abspath(__file__))[:8])

    # --------------------------------------------------- il PRIMA, dal PADRE (H-P8)
    p_prima = os.path.join(FUORI, "_sim_prima.py")
    introduce = prima_del_flag(p_prima)
    stampa("  il PRIMA ...................... %s  (dal PADRE di %s, che introduce `%s`)"
           % (blob(p_prima)[:8], str(introduce)[:8], ANCORA))
    stampa("  ### e NON da `HEAD`: dal commit della cura in poi `HEAD` LA CONTIENE, e il")
    stampa("  ###   braccio <<prima>> diventerebbe il braccio OFF di se stesso (`H-P8`).")
    esito["blob_prima"] = blob(p_prima)
    esito["commit_che_introduce"] = str(introduce)

    # --------------------------------------------------- il SOLO RIORDINO (braccio A)
    # ======================== BRACCIO `0`: la cura e' RIPRODUCIBILE dal repo?
    #   ### Non era nel disegno, e l'ha suggerito la caduta: se la patch COMMITTATA
    #   applicata al *prima* COMMITTATO da' lo STESSO BLOB del simulatore di oggi,
    #   allora ### **la cura e' recuperabile PER COSTRUZIONE** (par.7) -- e non per
    #   la mia parola. Se i blob differissero, il simulatore committato conterrebbe
    #   ### **qualcosa che la patch non produce**, ed e' un fatto da sapere PRIMA di
    #   leggere qualunque altro braccio.
    p_rifatta = copia_patchata(p_prima, os.path.join(FUORI, "_sim_rifatta.py"), [])
    uguale = (blob(p_rifatta) == blob(SIM))
    stampa("")
    stampa("-" * 100)
    stampa("BRACCIO `0` -- LA CURA E' RIPRODUCIBILE DAL REPO?")
    stampa("  il *prima* committato + la patch committata .. %s" % blob(p_rifatta)[:8])
    stampa("  il simulatore di oggi ........................ %s" % blob(SIM)[:8])
    if uguale:
        stampa("  ### \u2705 STESSO BLOB: la cura e' recuperabile PER COSTRUZIONE (par.7),")
        stampa("  ###   non per la mia parola. Chiunque la rifa' con due comandi.")
    else:
        stampa("  ### \u26d4 BLOB DIVERSI: il simulatore committato contiene qualcosa che la")
        stampa("  ###   patch NON produce. Va trovato PRIMA di leggere gli altri bracci.")
    esito["braccio_0_riproducibile"] = bool(uguale)
    esito["blob_rifatta"] = blob(p_rifatta)
    stampa("")

    p_ord = copia_patchata(p_prima, os.path.join(FUORI, "_sim_solo_ordine.py"),
                           ["--solo-ordine"])
    stampa("  SOLO il vincolo 4 ............. %s  (eredita' INVARIATA)" % blob(p_ord)[:8])
    esito["blob_solo_ordine"] = blob(p_ord)
    stampa("")

    # ====================================================== BRACCI A, B, C: in LOCKSTEP
    stampa("-" * 100)
    stampa("BRACCI `A`, `B`, `C` -- i tre blob girano IN LOCKSTEP, scena per scena")
    stampa("  ### UN SOLO passo per scena invece di sei run: i tre moduli avanzano insieme")
    stampa("  ###   e si confrontano DOPO OGNI PASSO, cosi' la PRIMA differenza e' quella")
    stampa("  ###   vera e non la prima che si nota a fine run.")
    stampa("")
    per_scena = {}
    for nome, seme, passi in SCENE:
        stampa("  " + "=" * 96)
        stampa("  SCENA `%s` -- seme %d, %d passi" % (nome, seme, passi))
        with contextlib.redirect_stdout(io.StringIO()):
            m_pr = carica(p_prima, "_s5_pr_%s" % nome)
            m_or = carica(p_ord, "_s5_or_%s" % nome)
            m_nu = carica(SIM, "_s5_nu_%s" % nome)
            n_pr = costruisci(m_pr, seme, os.path.join(FUORI, "_sc_pr_%s" % nome))
            n_or = costruisci(m_or, seme, os.path.join(FUORI, "_sc_or_%s" % nome))
            n_nu = costruisci(m_nu, seme, os.path.join(FUORI, "_sc_nu_%s" % nome))
        d0_A = confronta(stato(n_pr), stato(n_or))
        d0_B = confronta(stato(n_pr), stato(n_nu))
        stampa("    alla COSTRUZIONE della scena:  `A` %d differenze · `B` %d differenze"
               % (len(d0_A), len(d0_B)))
        primo_A, primo_B = None, None
        tot_A, tot_B = 0, 0
        for p in range(1, passi + 1):
            with contextlib.redirect_stdout(io.StringIO()):
                _passo.passo_pieno(m_pr, n_pr)
                _passo.passo_pieno(m_or, n_or)
                _passo.passo_pieno(m_nu, n_nu)
            dA = confronta(stato(n_pr), stato(n_or))
            dB = confronta(stato(n_pr), stato(n_nu))
            if dA and primo_A is None:
                primo_A = (p, list(dA))
            if dB and primo_B is None:
                primo_B = (p, list(dB))
            tot_A = max(tot_A, len(dA))
            tot_B = max(tot_B, len(dB))
        # --- BRACCIO A
        stampa("")
        stampa("    BRACCIO `A` -- il RIORDINO DA SOLO deve essere BYTE-IDENTICO")
        if primo_A is None:
            stampa("      ### ✅ PASSA: ZERO differenze su %d passi, su TUTTI gli"
                   % passi)
            stampa("      ###   attributi di `net` (ndarray e scalari di `__dict__`).")
        else:
            stampa("      ### ⛔ FALLISCE: prima differenza al passo %d" % primo_A[0])
            for k, q in primo_A[1][:12]:
                stampa("      ###   %-28s %s" % (k, q))
            stampa("      ### ==> IL RIORDINO HA TOCCATO QUALCOS'ALTRO. Si FERMA qui: il")
            stampa("      ###   braccio `B` non si puo' interpretare se `A` non passa.")
        # --- BRACCIO B
        nati_der = int(getattr(n_nu, "_g_pgeom_der_m1", 0)) + \
            int(getattr(n_nu, "_g_pgeom_der_p1", 0))
        stampa("")
        stampa("    BRACCIO `B` -- la CURA INTERA contro il PRIMA")
        if primo_B is None:
            stampa("      ### ✅ ZERO differenze sugli attributi COMUNI su %d passi."
                   % passi)
        else:
            attesi = [x for x in primo_B[1] if x[0] in CONTATORI_NUOVI]
            inattesi = [x for x in primo_B[1] if x[0] not in CONTATORI_NUOVI]
            stampa("      prima differenza al passo %d: %d voci (%d ATTESE, %d INATTESE)"
                   % (primo_B[0], len(primo_B[1]), len(attesi), len(inattesi)))
            for k, q in attesi:
                stampa("        ATTESA   %-26s %s" % (k, q))
            for k, q in inattesi[:12]:
                stampa("        INATTESA %-26s %s" % (k, q))
            if inattesi:
                stampa("      ### ⛔ FALLISCE: ci sono differenze che NON sono i due")
                stampa("      ###   contatori dichiarati.")
            else:
                stampa("      ### ✅ PASSA: le SOLE differenze sono i due contatori")
                stampa("      ###   NUOVI dichiarati, `%s`." % ", ".join(CONTATORI_NUOVI))
        stampa("      ### \U0001f4cc E IL PUNTO `(d)` DEL MANDATO: il censimento aveva")
        stampa("      ###   misurato ZERO nati con eredita' diversa dalla derivazione,")
        stampa("      ###   quindi la BYTE-IDENTITA' E' IL RISULTATO ATTESO -- e i bracci")
        stampa("      ###   `D` e `E` sono quelli che DISCRIMINANO.")
        # --- BRACCIO C
        stampa("")
        stampa("    BRACCIO `C` -- il contatore della DERIVAZIONE, misurato")
        stampa("      _g_pgeom_der_m1 (ha deciso -1) .. %d"
               % int(getattr(n_nu, "_g_pgeom_der_m1", 0)))
        stampa("      _g_pgeom_der_p1 (ha deciso +1) .. %d"
               % int(getattr(n_nu, "_g_pgeom_der_p1", 0)))
        stampa("      nati totali (la somma) .......... %d" % nati_der)
        # --- la misura chiesta dal guardiano: perc_geom arriva mai a +1?
        pg = np.asarray(n_nu.perc_geom)
        stampa("")
        stampa("    LA MISURA CHIESTA DAL GUARDIANO -- `perc_geom` a fine run")
        stampa("      nodi a +1 .. %d su %d" % (int(np.sum(pg == 1)), pg.size))
        per_scena[nome] = {
            "seme": seme, "passi": passi,
            "A_prima_differenza": (primo_A[0] if primo_A else None),
            "A_differenze": ([[k, q] for k, q in primo_A[1]] if primo_A else []),
            "A_passa": primo_A is None,
            "B_prima_differenza": (primo_B[0] if primo_B else None),
            "B_differenze": ([[k, q] for k, q in primo_B[1]] if primo_B else []),
            "g_pgeom_der_m1": int(getattr(n_nu, "_g_pgeom_der_m1", 0)),
            "g_pgeom_der_p1": int(getattr(n_nu, "_g_pgeom_der_p1", 0)),
            "nati": nati_der,
            "perc_geom_a_piu1_fine_run": int(np.sum(pg == 1)),
            "nodi": int(pg.size),
        }
        stampa("")
    esito["scene"] = per_scena

    # ====================================================== BRACCI D ed E: il caso COSTRUITO
    stampa("-" * 100)
    stampa("BRACCI `D` ed `E` -- IL CASO COSTRUITO: `tw = 20` sui nuovi archi")
    stampa("  ### PERCHE' COSTRUITO: eredita' e derivazione danno LO STESSO valore oggi")
    stampa("  ###   (1225 nati, tutti -1), quindi la forma del mandato NON PUO' fallire.")
    stampa("  ###   Con `tw` sopra `PHI_CRIT` la derivazione da' +1 e l'eredita' resta -1:")
    stampa("  ###   allora <<lasciare l'eredita'>> SI VEDE. E' l'ulp iniettato.")
    stampa("  ### E SOLO SULLA SCENA CORTA (seme 11, 72 passi), DICHIARATO: il caso e'")
    stampa("  ###   costruito, non statistico -- una scena basta a decidere.")
    stampa("")
    copie = {
        "E  derivazione, tw iniettato": ["--inietta-tw=20"],
        "D1 eredita' nella DIVISIONE": ["--inietta-tw=20", "--solo-schwinger"],
        "D2 eredita' nello SCHWINGER": ["--inietta-tw=20", "--solo-divisione"],
    }
    de = {}
    for et, args in copie.items():
        nome_f = os.path.join(FUORI, "_sim_%s.py" % et.split()[0])
        copia_patchata(p_prima, nome_f, args)
        with contextlib.redirect_stdout(io.StringIO()):
            m = carica(nome_f, "_s5_de_%s" % et.split()[0])
            net = costruisci(m, 11, os.path.join(FUORI, "_sc_de_%s" % et.split()[0]))
            primo = None
            for p in range(1, 73):
                _passo.passo_pieno(m, net)
                if primo is None and (int(getattr(net, "_g_pgeom_der_m1", 0))
                                      + int(getattr(net, "_g_pgeom_der_p1", 0))) > 0:
                    primo = p
        m1 = int(getattr(net, "_g_pgeom_der_m1", 0))
        p1 = int(getattr(net, "_g_pgeom_der_p1", 0))
        pg = np.asarray(net.perc_geom)
        de[et] = {"blob": blob(nome_f), "der_m1": m1, "der_p1": p1,
                  "primo_passo_con_derivazione": primo,
                  "nodi_a_piu1_fine_run": int(np.sum(pg == 1))}
        stampa("  %-32s blob %s  der -1 = %-6d der +1 = %-6d  primo passo %s"
               % (et, blob(nome_f)[:8], m1, p1, primo))
    esito["D_E"] = de
    stampa("")
    e = de["E  derivazione, tw iniettato"]
    stampa("  BRACCIO `E` -- IL CONTROLLO POSITIVO")
    if e["der_p1"] > 0 and e["der_m1"] == 0:
        stampa("    ### ✅ PASSA: con `tw = 20` la derivazione ha deciso `+1` %d volte"
               % e["der_p1"])
        stampa("    ###   e `-1` ZERO volte. ### QUINDI LEGGE `tw`: NON E' UNA COSTANTE.")
    elif e["der_p1"] == 0:
        stampa("    ### ⛔ FALLISCE: con `tw = 20` la derivazione da' ANCORA `-1`.")
        stampa("    ###   ==> NON E' UNA DERIVAZIONE. Il commit 5 NON VA.")
    else:
        stampa("    ### ⚠ MISTO: `+1` %d volte, `-1` %d volte. Da spiegare: con `tw`"
               % (e["der_p1"], e["der_m1"]))
        stampa("    ###   iniettato su TUTTI i nuovi archi ci si aspetta solo `+1`.")
    stampa("")
    stampa("  BRACCIO `D` -- IL CASO CHE DEVE FALLIRE, per i DUE EVENTI SEPARATAMENTE")
    for et in ("D1 eredita' nella DIVISIONE", "D2 eredita' nello SCHWINGER"):
        d = de[et]
        atteso = e["der_p1"]
        stampa("    %-32s der +1 = %d  (la CURA INTERA ne faceva %d)"
               % (et, d["der_p1"], atteso))
        if d["der_p1"] < atteso:
            stampa("      ### ✅ VISTO: l'evento lasciato in eredita' NON passa piu'")
            stampa("      ###   dalla derivazione, e il contatore lo DICE.")
        else:
            stampa("      ### ⛔ NON VISTO: il sigillo non distingue l'evento lasciato")
            stampa("      ###   in eredita'. Il braccio `D` non discrimina.")
    stampa("")
    stampa("=" * 100)
    stampa("### IL RIEPILOGO")
    stampa("###   braccio 0 (la cura e' riproducibile dal repo) ... %s"
           % ("PASSA" if esito.get("braccio_0_riproducibile") else "FALLISCE"))
    for _n in per_scena:
        stampa("###   braccio A sulla scena `%s` ............. %s"
               % (_n, "PASSA" if per_scena[_n]["A_passa"] else "FALLISCE"))
    stampa("=" * 100)

    io.open(os.path.join(FUORI, "_sigillo.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(esito, indent=1, ensure_ascii=False, default=str))
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(righe) + NL)
    print("  referto .. %s" % FUORI)


if __name__ == "__main__":
    principale()
