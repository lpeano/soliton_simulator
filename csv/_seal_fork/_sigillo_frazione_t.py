# -*- coding: utf-8 -*-
"""**IL SIGILLO DEL `COMMIT 6a`: la frazione `t` esplicita.**

### I criteri sono fissati **nel mandato del 2026-10-03** e nel task history, **prima di
girare**. ### Se un criterio fallisce: **si riporta, non si aggiusta il criterio.**

| | braccio | che cosa decide |
|---|---|---|
| **`0`** | la patch committata applicata al *prima* committato da' ### **il blob di oggi** | la cura e' ### **recuperabile per costruzione** *(par.7)* |
| **`A`** | ### **identico al byte** su ### **QUATTRO** scene: le tre del commit 4 piu' una ### **senza `--mitosi-2lam`**. Stato ### **E** contatori, coi contatori ### **separati per nome e riportati** | e' un riordino |
| **`A-tr`** | i quattro ### **`_sm_tr*`** per ### **tutte** le scene. ### ⛔ **Se uno e' zero DAPPERTUTTO, il braccio sui `_sm_lun` e' VUOTO: si FERMA e si dice** | ### **senza troncamenti, `_fab` vale zero da entrambe le parti e il braccio non prova nulla** |
| **`B`** | il censimento rigirato: ### **0 siti `FRAZIONE` col letterale**, ### **13 occorrenze invece di 19**, e tutte e sei le formule ### **leggono `t`** | il valore e' davvero in **un solo posto** |
| **`C`** | una copia con ### **`t = 0.4`**, verificata ### **SUI VALORI** e non sul *<<differisce>>*, al ### **primo evento di ciascun tipo** | `t` arriva davvero a tutti e sei |
| **`C-bis`** | ### **SEI copie**, una per sito, ciascuna col suo sito al letterale `0.5`. ### **Sei bocciature: se anche una passa, il sigillo non discrimina** | il controllo del controllo |

**COMANDO:** `python csv/_seal_fork/_sigillo_frazione_t.py`
**USCITA:** `csv/_seal_fork/_sigillo_frazione_t/`
"""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import pickle
import platform
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
FUORI = os.path.join(_QUI, "_sigillo_frazione_t")
PATCH = os.path.join(_QUI, "_frazione_t_patch.py")
CENS = os.path.join(RADICE, "csv", "_test_fork", "_censimento_punto_medio.py")
NL = chr(10)
# ### L'ANCORA DEL *PRIMA* E' IL NOME STORICO, e il motivo e' preciso.
#   `sim_prima_del_flag` prende il commit PIU' VECCHIO che introduce la stringa e
#   poi il suo PADRE. Con `FRAZ_NASCITA` quel commit sarebbe LA RINOMINA, e il
#   padre conterrebbe `T_NASCITA` -- cioe' il `6a` GIA' FATTO: il *prima* non
#   sarebbe il prima, e la patch non attaccherebbe.
#   ### Con `T_NASCITA` il commit piu' vecchio e' quello che ha introdotto il `6a`,
#   e il padre e' il blob PRE-6a -- che e' il *prima* vero. ### E
#   `sim_prima_del_flag` ASSERISCE che il file estratto NON contenga l'ancora,
#   quindi se un giorno questa scelta diventasse sbagliata il sigillo SI FERMEREBBE
#   invece di misurare niente.
ANCORA = "T_NASCITA"
# ### LE TRE SCENE DEL COMMIT 4, PIU' LA QUARTA senza `--mitosi-2lam` (mandato)
SCENE = (("corta", 11, 72, True), ("lunga", 11, 150, True),
         ("altro_seme", 12, 72, True), ("senza_2lam", 11, 72, False))
SITI = ("pos_div", "dh", "fm", "fm_bias", "pos_sch", "dd")
# ### QUALE CHIAVE DI `C` VERIFICA QUALE SITO, e in quale copia.
#   ### Serve a rispondere a una domanda che il referto non poteva porre: *<<ogni sito e'
#   stato verificato SUI VALORI da almeno una copia?>>*
#   ### IL BUCO CHE L'HA RESA NECESSARIA (errore del guardiano, dichiarato da lui): la
#   copia di `C` girava ### **SOLO con `--mitosi-dir=1.0`**, quindi il ramo normale
#   `fm = phi[a] - FRAZ_NASCITA*D` *(`:8554`)* ### **non girava in NESSUNA copia con la
#   formula giusta.** Un errore come `(1-t)*D` in quel ramo sarebbe passato: ### **`B`** lo
#   vede leggere `FRAZ_NASCITA` *(e basta)*, ### **`C`** non esegue il ramo, ### **`C-bis`**
#   prova solo che il LETTERALE viene scoperto -- ### **non che la formula sia giusta.**
CHIAVI_DEL_SITO = {
    "pos_div": ("pos_figlio convesso",),
    "dh": ("dh_a = t*d[sel]", "dh_b = (1-t)*d[sel]"),
    "fm": ("fm = (phi[a] - t*D) mod",),
    "fm_bias": ("fm = (phi[a]-(t+bias)*D)",),
    "pos_sch": ("pos antinodo convesso",),
    "dd": ("dd_a = max(t*L, 0.05)", "dd_b = max((1-t)*L, 0.05)"),
}
TR = ("_sm_trd_mitosi", "_sm_trd0_mitosi", "_sm_trd_schwinger", "_sm_trd0_schwinger")
T_PROVA = 0.4


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def carica(percorso, nome):
    spec = importlib.util.spec_from_file_location(nome, percorso)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def copia_patchata(sorgente, dest, argomenti):
    """La SORGENTE e' SEMPRE il *prima*: le ancore della patch descrivono il codice
    PRIMA della cura *(lezione del sigillo del commit 5, che cadde proprio su questo)*."""
    io.open(dest, "wb").write(io.open(sorgente, "rb").read())
    q = subprocess.run([sys.executable, PATCH, "--file=%s" % dest] + list(argomenti),
                       capture_output=True, text=True)
    assert q.returncode == 0, (q.stdout or "")[-1500:] + (q.stderr or "")[-1500:]
    return dest


def costruisci(m, seme, dest, con_2lam=True):
    """Scena `MASSE-COERENTI`, dal CLI del driver: nessun attributo a mano *(`H-P3`)*.

    ### `con_2lam=False` TOGLIE `--mitosi-2lam` dall'argv del driver — e' la QUARTA
    scena del mandato, che serve a ### **far nascere troncamenti**: con `MITOSI_2LAM`
    acceso la mitosi non tronca, e il braccio sui `_sm_lun` sarebbe ### **vuoto**.
    """
    _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=%d" % seme], dest=dest)
    argv = list(argv)
    if not con_2lam:
        argv = [x for x in argv if x != "--mitosi-2lam"]
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


def _dig(x):
    """Un digest di QUALUNQUE struttura picklabile."""
    return hashlib.sha1(pickle.dumps(x, protocol=4)).hexdigest()[:16]


def stato(net):
    """### TUTTO cio' che sta in `__dict__`, non solo gli ndarray e gli scalari.

    ### ⛔ **LA STESURA PRECEDENTE CONFRONTAVA SOLO ndarray E SCALARI, ED ERA
    UN FALSO-ZERO STRUTTURALE** *(rilievo del guardiano, 2026-10-03, ed e' giusto)*: in
    `net` ci sono ### **16 attributi** che ne restavano fuori -- fra cui `conc_nodi` e
    `conc_archi` *(liste)*, `masse_info` *(dict)*, ### **`_S` (una matrice SPARSA)** e
    ### **`rng` (lo stato del generatore)**. ### **Uno zero su un insieme scelto da me
    non e' uno zero sulla legge.**

    | classe | come si confronta |
    |---|---|
    | `ndarray`, scalari | ### **direttamente, al bit** |
    | matrice ### **SPARSA** | `data`, `indices`, `indptr`, `shape` |
    | ### **`rng`** | `bit_generator.state` |
    | liste, tuple, dict, `None` | ### **digest pickle** |
    | ### **non picklabile** | ### **DICHIARATO nel referto**, non saltato in silenzio |

    ### UN'ECCEZIONE DICHIARATA: **`_calcpsi_origini`**. Le sue chiavi sono
    `"funzione:RIGA"` con la ### **riga del chiamante**, che cambia ### **a ogni modifica
    del codice** -- quindi un confronto diretto darebbe una differenza ### **garantita**
    e non direbbe niente sulla fisica. ### **Si confronta AGGREGATO per nome di
    funzione**, e il referto lo scrive.
    """
    fuori = {}
    for k, v in vars(net).items():
        if isinstance(v, np.ndarray):
            fuori[k] = v
        elif isinstance(v, (int, float, bool, np.integer, np.floating)):
            fuori[k] = v
        elif k == "_calcpsi_origini" and isinstance(v, dict):
            agg = {}
            for kk, vv in v.items():
                nome = str(kk).split(":")[0]
                agg[nome] = agg.get(nome, 0) + (
                    float(vv) if isinstance(vv, (int, float)) else 1)
            fuori[k] = "AGGREGATO:" + _dig(sorted(agg.items()))
        elif hasattr(v, "bit_generator"):
            fuori[k] = "RNG:" + _dig(v.bit_generator.state)
        elif hasattr(v, "indptr") or hasattr(v, "tocsr"):
            sp = v.tocsr() if hasattr(v, "tocsr") else v
            fuori[k] = "SPARSA:" + _dig((sp.data, sp.indices, sp.indptr, sp.shape))
        else:
            try:
                fuori[k] = "PICKLE:" + _dig(v)
            except Exception as _e:
                fuori[k] = "NON-CONFRONTABILE:%s:%s" % (type(v).__name__, _e)
    return fuori


def classi_di(net):
    """Quanti attributi per classe: serve al referto, perche' uno zero va letto
    sapendo ### **su quante cose** e' stato calcolato."""
    c = {"ndarray": 0, "scalare": 0, "sparsa": 0, "rng": 0, "pickle": 0,
         "aggregato": 0, "NON-CONFRONTABILE": 0}
    for v in stato(net).values():
        if isinstance(v, np.ndarray):
            c["ndarray"] += 1
        elif isinstance(v, str) and v.startswith("SPARSA:"):
            c["sparsa"] += 1
        elif isinstance(v, str) and v.startswith("RNG:"):
            c["rng"] += 1
        elif isinstance(v, str) and v.startswith("PICKLE:"):
            c["pickle"] += 1
        elif isinstance(v, str) and v.startswith("AGGREGATO:"):
            c["aggregato"] += 1
        elif isinstance(v, str) and v.startswith("NON-CONFRONTABILE"):
            c["NON-CONFRONTABILE"] += 1
        else:
            c["scalare"] += 1
    return c


def confronta(s1, s2):
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
            elif not np.array_equal(a, b, equal_nan=True):
                diff.append((k, "celle diverse"))
        else:
            if a != b and not (a != a and b != b):
                diff.append((k, "%r contro %r" % (a, b)))
    return diff


class SpiaValori:
    """### Registra i VALORI che entrano in `_nasce` e quelli del CONTESTO, al PRIMO
    evento di ciascun tipo. ### Il braccio `C` li verifica UNO PER UNO, non col
    *<<differisce>>*.
    """

    def __init__(self, m):
        self.m = m
        self.pre_nasce = {}
        self.ctx = {}
        # ### LO SCATTO ALL'INGRESSO DI `mitosi`, e serve: `fm` si calcola PRIMA DEL
        #   CALCIO ai genitori, quindi il `phi` letto all'ingresso di `nascita` e' GIA'
        #   CALCIATO e `fm` NON si ricostruisce da li'.
        #   ### MISURATO: con `MITOSI_DIR = 1.0`, ricostruendo `fm` dal `phi` di `nascita`
        #   lo scarto massimo e' 4.96 -- il confronto fallirebbe PER IL MOTIVO SBAGLIATO.
        #   Il fatto e' gia' nel repo: <<fm si calcola PRIMA del calcio, twp DOPO>>.
        self.pre_mitosi = {}
        self._nasce_vero = m.Rete._nasce
        self._nascita_vera = m.nascita
        self._mitosi_vera = m.Rete.mitosi
        spia = self

        def _mitosi(selfr, *aa, **kk):
            # ### SI SOVRASCRIVE A OGNI CHIAMATA, e non si tiene la PRIMA: `mitosi` gira
            #   a ### **ogni passo**, e la nascita arriva al 42. ### Tenendo la prima si
            #   ricostruirebbe `fm` dal `phi` del ### **passo 1** -- misurato: scarto 2.33.
            #   ### Chi serve e' lo scatto della chiamata CHE PRODUCE la nascita, e
            #   `_nascita` lo copia nel contesto quando l'evento scatta.
            if True:
                spia.pre_mitosi = {
                    "phi": np.array(selfr.phi, dtype=float, copy=True),
                    "tw": np.array(selfr.tw, dtype=float, copy=True),
                    "i": np.array(selfr.i, dtype=int, copy=True),
                    "j": np.array(selfr.j, dtype=int, copy=True),
                    "deg": np.array(selfr._deg, dtype=float, copy=True),
                    "n": int(selfr.n), "dphi": float(selfr._dphi())}
            return spia._mitosi_vera(selfr, *aa, **kk)

        m.Rete.mitosi = _mitosi

        def _nasce(selfr, v, dove="?", md=1, md0=1, meta=None):
            if dove not in spia.pre_nasce:
                spia.pre_nasce[dove] = {"v": np.array(v, dtype=float, copy=True),
                                        "md": md, "md0": md0, "meta": meta}
            return spia._nasce_vero(selfr, v, dove, md, md0, meta)

        def _nascita(net, evento, c):
            if evento not in spia.ctx:
                d = {"n0": int(c["n0"]), "quante": int(c["quante"])}
                # ### il `d` dei genitori PRIMA che le regole scrivano
                if evento == "divisione":
                    # ### GLI INDICI, e senza di loro il braccio `C` CADE: `misura_valori`
                    #   ricostruisce `fm` come `pm["phi"][cd["a"]]`, cioe' dal `phi`
                    #   ### **pre-calcio** dello scatto `pm`, e per indicizzarlo servono
                    #   gli INDICI. ### \u26d4 Il 2026-10-03 il contesto conteneva `phi_a`
                    #   e `phi_b` ### **ma non `a` e `b`**, e il braccio e' morto con
                    #   `KeyError: 'a'`. ### **E `phi_a` non serviva comunque: e' letto
                    #   all'ingresso di `nascita`, cioe' DOPO il calcio** -- che e'
                    #   esattamente il motivo per cui lo scatto `pm` esiste.
                    d["a"] = np.array(c["a"], dtype=int, copy=True)
                    d["b"] = np.array(c["b"], dtype=int, copy=True)
                    d["d_sel"] = np.array(net.d[c["sel"]], dtype=float, copy=True)
                    d["pos_a"] = np.array(net.pos[c["a"]], dtype=float, copy=True)
                    d["pos_b"] = np.array(net.pos[c["b"]], dtype=float, copy=True)
                    d["pos_figlio"] = np.array(c["pos_figlio"], dtype=float, copy=True)
                    d["phi_a"] = np.array(net.phi[c["a"]], dtype=float, copy=True)
                    d["phi_b"] = np.array(net.phi[c["b"]], dtype=float, copy=True)
                    d["dphi"] = float(net._dphi())
                    d["fm"] = np.array(c["fm"], dtype=float, copy=True)
                    d["dh"] = np.array(c["dh"], dtype=float, copy=True)
                    # ### lo scatto PRE-CALCIO della chiamata CHE STA PRODUCENDO questa
                    #   nascita: dopo, `mitosi` gira di nuovo e lo sovrascrive.
                    d["pm"] = dict(spia.pre_mitosi)
                else:
                    # ### e gli indici dello Schwinger, per simmetria: il braccio li
                    #   usa per ricostruire `L` dagli stessi indici che il codice ha usato,
                    #   invece di fidarsi delle posizioni GIA' estratte.
                    d["aa"] = np.array(c["aa"], dtype=int, copy=True)
                    d["bb"] = np.array(c["bb"], dtype=int, copy=True)
                    d["pos_aa"] = np.array(net.pos[c["aa"]], dtype=float, copy=True)
                    d["pos_bb"] = np.array(net.pos[c["bb"]], dtype=float, copy=True)
                    d["dd"] = np.array(c["dd"], dtype=float, copy=True)
                    d["k"] = np.array(c["k"], dtype=int, copy=True)
                spia.ctx[evento] = d
            fuori = spia._nascita_vera(net, evento, c)
            if evento == "schwinger" and "pos_k" not in spia.ctx[evento]:
                kk = spia.ctx[evento]["k"]
                spia.ctx[evento]["pos_k"] = np.array(net.pos[kk], dtype=float, copy=True)
            return fuori

        m.Rete._nasce = _nasce
        m.nascita = _nascita


def principale():
    out = []

    def stampa(*x):
        s = " ".join(str(y) for y in x)
        out.append(s)
        print(s)

    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    esito = {"blob_sim": blob(SIM), "blob_sigillo": blob(os.path.abspath(__file__)),
             "blob_patch": blob(PATCH)}
    stampa("=" * 100)
    stampa("IL SIGILLO DEL COMMIT 6a: la frazione `t` esplicita")
    stampa("=" * 100)
    stampa("  simulatore di OGGI .. %s" % blob(SIM)[:8])
    stampa("  questo sigillo ...... %s" % blob(os.path.abspath(__file__))[:8])
    stampa("  la patch ............ %s" % blob(PATCH)[:8])
    # ### LA PIATTAFORMA FA PARTE DEL REFERTO, e non e' burocrazia: il guardiano, su
    #   Linux con numpy 2.5.3, misura sulla scena `senza_2lam` `_sm_tr* = 16/14/6/6`;
    #   questa macchina, Windows con numpy 2.3.0, misura `14/12/4/4`.
    #   ### \u26d4 **L'IDENTITA' *prima / dopo* VALE SU CIASCUNA MACCHINA; I CONTEGGI
    #   ASSOLUTI NO.** Un referto che non dichiara la piattaforma invita a confrontare
    #   due numeri che non sono confrontabili -- ed e' lo stesso errore del json di un
    #   altro blob, spostato dal file alla macchina.
    stampa("  piattaforma ......... %s %s" % (platform.system(), platform.machine()))
    stampa("  Python .............. %s" % platform.python_version())
    stampa("  numpy ............... %s" % np.__version__)
    stampa("  ### I CONTEGGI DEI RUN (`_sm_tr*`, numero di nascite, passi) VALGONO PER")
    stampa("  ###   QUESTA PIATTAFORMA. Cio' che NON dipende dalla piattaforma e'")
    stampa("  ###   l'IDENTITA' fra il *prima* e l'*oggi*, che e' quello che il sigillo")
    stampa("  ###   misura. ### Su un'altra macchina i conteggi cambiano e l'identita' no.")
    esito["piattaforma"] = {"sistema": platform.system(), "macchina": platform.machine(),
                            "python": platform.python_version(), "numpy": np.__version__}

    # ------------------------------------------------- il PRIMA, dal PADRE (H-P8)
    p_prima = os.path.join(FUORI, "_sim_prima.py")
    introduce = _cli_flag.sim_prima_del_flag(ANCORA, p_prima, radice=RADICE)
    stampa("  il PRIMA ............ %s  (dal PADRE di %s, che introduce `%s`)"
           % (blob(p_prima)[:8], str(introduce)[:8], ANCORA))
    esito["blob_prima"] = blob(p_prima)

    # ======================================================== BRACCIO 0
    p_rif = copia_patchata(p_prima, os.path.join(FUORI, "_sim_rifatta.py"), [])
    uguale = (blob(p_rif) == blob(SIM))
    stampa("")
    stampa("-" * 100)
    stampa("BRACCIO `0` -- LA CURA E' RIPRODUCIBILE DAL REPO?")
    stampa("  il *prima* + la patch .. %s" % blob(p_rif)[:8])
    stampa("  il simulatore di oggi .. %s" % blob(SIM)[:8])
    stampa("  ### %s" % ("PASSA: stesso blob. La cura e' recuperabile PER COSTRUZIONE (par.7)."
                         if uguale else
                         "FALLISCE: il simulatore contiene qualcosa che la patch NON produce."))
    esito["braccio_0"] = bool(uguale)

    # ======================================================== BRACCIO A + A-tr
    stampa("")
    stampa("-" * 100)
    stampa("BRACCIO `A` -- BYTE-IDENTICO su QUATTRO scene, stato E contatori")
    stampa("  ### I due blob girano IN LOCKSTEP e si confrontano DOPO OGNI PASSO: cosi' la")
    stampa("  ###   PRIMA differenza e' quella vera, non la prima che si nota a fine run.")
    per_scena = {}
    for nome, seme, passi, con2 in SCENE:
        stampa("")
        stampa("  " + "=" * 96)
        stampa("  SCENA `%s` -- seme %d, %d passi, --mitosi-2lam: %s"
               % (nome, seme, passi, "SI" if con2 else "NO"))
        with contextlib.redirect_stdout(io.StringIO()):
            m1 = carica(p_prima, "_s6a_pr_%s" % nome)
            m2 = carica(SIM, "_s6a_nu_%s" % nome)
            n1 = costruisci(m1, seme, os.path.join(FUORI, "_sc1_%s" % nome), con2)
            n2 = costruisci(m2, seme, os.path.join(FUORI, "_sc2_%s" % nome), con2)
        cls = classi_di(n2)
        # ### IL NUMERO DI ATTRIBUTI SI CONTA DUE VOLTE: alla costruzione E all'ultimo
        #   passo. ### **`net` ne ACQUISTA durante il run** -- `_calcpsi_origini` non
        #   esiste alla costruzione -- quindi un solo conteggio dichiara un insieme che
        #   al passo N non e' piu' quello. ### Il referto riporta entrambi.
        stampa("    attributi confrontati, per classe: %s"
               % (" | ".join("%s %d" % (k, v)
                               for k, v in sorted(cls.items()) if v)))
        if cls["NON-CONFRONTABILE"]:
            stampa("    ### %d NON CONFRONTABILI: un LIMITE DICHIARATO, non saltati in"
                   % cls["NON-CONFRONTABILE"])
            stampa("    ###   silenzio. Sono nel json.")
        d0 = confronta(stato(n1), stato(n2))
        primo = None
        for p in range(1, passi + 1):
            with contextlib.redirect_stdout(io.StringIO()):
                _passo.passo_pieno(m1, n1)
                _passo.passo_pieno(m2, n2)
            d = confronta(stato(n1), stato(n2))
            if d and primo is None:
                primo = (p, list(d))
        cls_fine = classi_di(n2)
        stampa("    attributi confrontati ALL'ULTIMO PASSO (%d): %s"
               % (passi, " | ".join("%s %d" % (k, w)
                                    for k, w in sorted(cls_fine.items()) if w)))
        if sum(cls_fine.values()) != sum(cls.values()):
            stampa("    ### \u26a0 SONO %d alla costruzione e %d all'ultimo passo: `net`"
                   % (sum(cls.values()), sum(cls_fine.values())))
            stampa("    ###   ACQUISTA attributi durante il run. Dichiararne uno solo")
            stampa("    ###   descriverebbe un insieme che al passo %d non e' piu' quello."
                   % passi)
        trs = {c: [int(getattr(n1, c, 0)), int(getattr(n2, c, 0))] for c in TR}
        stampa("    alla costruzione: %d differenze" % len(d0))
        if primo is None and not d0:
            stampa("    ### PASSA: ZERO differenze su %d passi, su TUTTI gli attributi di" % passi)
            stampa("    ###   `net` -- OGNI voce di `__dict__`, non solo gli ndarray e gli")
            stampa("    ###   scalari: anche liste, dict, la matrice SPARSA e lo stato del")
            stampa("    ###   generatore. CONTATORI COMPRESI.")
            stampa("    ### \u26d4 LA FRASE DI PRIMA DICEVA *<<ndarray e scalari di __dict__>>*")
            stampa("    ###   ED ERA FALSA da quando `stato()` confronta anche pickle,")
            stampa("    ###   sparse e `rng`: descriveva l'insieme VECCHIO, piu' piccolo.")
            stampa("    ###   Un referto che dichiara un insieme piu' piccolo di quello")
            stampa("    ###   davvero confrontato fa sembrare lo zero piu' DEBOLE di quanto")
            stampa("    ###   sia -- e la volta prima era il contrario. Entrambe bugie.")
        else:
            q = primo or (0, d0)
            stampa("    ### FALLISCE: prima differenza al passo %d, %d voci:" % (q[0], len(q[1])))
            for k, w in q[1][:15]:
                stampa("    ###   %-30s %s" % (k, w))
        stampa("    I QUATTRO `_sm_tr*` (prima / oggi):")
        for c in TR:
            stampa("      %-22s %8d / %8d" % (c, trs[c][0], trs[c][1]))
        per_scena[nome] = {"seme": seme, "passi": passi, "mitosi_2lam": con2,
                           "passa": bool(primo is None and not d0),
                           "prima_differenza": (primo[0] if primo else None),
                           "differenze": ([[k, w] for k, w in primo[1]] if primo
                                          else [[k, w] for k, w in d0]),
                           "sm_tr": trs,
                           "attributi_costruzione": cls,
                           "attributi_ultimo_passo": cls_fine}
    esito["scene"] = per_scena

    stampa("")
    stampa("-" * 100)
    stampa("BRACCIO `A-tr` -- I TRONCAMENTI: il braccio sui `_sm_lun` e' VUOTO o no?")
    vuoti = []
    for c in TR:
        tot = sum(per_scena[n]["sm_tr"][c][1] for n in per_scena)
        stampa("  %-22s somma su tutte le scene: %d" % (c, tot))
        if tot == 0:
            vuoti.append(c)
    if vuoti:
        stampa("  ### *** %d CONTATORI SONO ZERO DAPPERTUTTO: %s ***"
               % (len(vuoti), ", ".join(vuoti)))
        stampa("  ### Per QUEI siti il braccio `A` NON PROVA NIENTE su `_sm_lun`: `_fab` vale")
        stampa("  ###   zero da entrambe le parti, quindi la somma per meta' non e' messa")
        stampa("  ###   alla prova. ### SI FERMA E SI DICE, come dice il mandato.")
    else:
        stampa("  ### NESSUNO e' zero dappertutto: il braccio `A` mette alla prova `_sm_lun`")
        stampa("  ###   su tutti e quattro i siti.")
    esito["A_tr_vuoti"] = vuoti

    # ======================================================== BRACCIO B
    stampa("")
    stampa("-" * 100)
    stampa("BRACCIO `B` -- IL CENSIMENTO RIGIRATO: 0 letterali, 13 occorrenze, sei siti con `t`")
    # ### \u26d4 DUE CONTROLLI CHE NON C'ERANO, E L'ASSENZA DEL SECONDO HA PRODOTTO UN
    #   FALSO-UNO. ### Il 2026-10-03 questo braccio ha dichiarato ### **FALLISCE** con sei
    #   siti <<al letterale>> che nel file in esame ### **non esistevano**: il censimento
    #   aveva ### **rifiutato** di scrivere il json *(giustamente)*, `q.returncode` ### **non
    #   era letto**, e il json rimasto sul disco era quello di ### **un altro blob**.
    #   ### **Un braccio che legge un artefatto senza verificare su quale blob e' stato
    #   prodotto non sta sigillando: sta CITANDO.** ### E il dato per smascherarlo era
    #   DENTRO il json (`blob_sim`).
    q = subprocess.run([sys.executable, CENS], capture_output=True, text=True, cwd=RADICE)
    jj = os.path.join(RADICE, "csv", "_test_fork", "_censimento_punto_medio",
                      "_censimento.json")
    b_rc = (q.returncode == 0)
    if not b_rc:
        stampa("  ### *** IL CENSIMENTO E' FALLITO: returncode %d ***" % q.returncode)
        for _r in ((q.stdout or "").rstrip() + NL + (q.stderr or "").rstrip()).split(NL)[-12:]:
            if _r.strip():
                stampa("  ###   %s" % _r[:140])
        stampa("  ### Il json sul disco NON e' di questa corsa: non si legge.")
    cj = json.load(io.open(jj, encoding="utf-8"))
    # ### DUE BLOB, NON UNO, e il secondo l'ha chiesto il guardiano per una ragione
    #   concreta: ### **la coppia COMMITTATA era incoerente in DUE modi, non uno.**
    #   ### \u26d4 MISURATO su `HEAD` al 2026-10-03: il json committato dichiarava
    #   `blob_sim 6d306976` *(il simulatore PRIMA della cura)* ### **e**
    #   `blob_strumento ec0a03e3` *(il censimento PRIMA della riparazione)*, con `19`
    #   occorrenze; e `_corsa.txt` committato dichiarava `strumento ec0a03e3` su
    #   `simulatore c18c9bf6`. ### **Cioe' i due pezzi della coppia venivano da DUE
    #   CORSE DIVERSE, su due coppie (simulatore, strumento) diverse.**
    #   ### \u2705 **Controllare solo `blob_sim` avrebbe lasciato passare un json prodotto
    #   dallo strumento VECCHIO sul simulatore giusto** -- cioe' esattamente il caso in
    #   cui la tabella era ancora indicizzata per riga.
    b_bsim = (cj.get("blob_sim") == blob(SIM))
    b_bstr = (cj.get("blob_strumento") == blob(CENS))
    b_blob = (b_bsim and b_bstr)
    stampa("  l'artefatto letto viene dagli STESSI DUE blob? .. %s"
           % ("SI" if b_blob else "NO"))
    stampa("    blob_sim       dal json .. %s   il file in esame .. %s   %s"
           % (str(cj.get("blob_sim"))[:8], blob(SIM)[:8], "OK" if b_bsim else "DIVERSO"))
    stampa("    blob_strumento dal json .. %s   il censimento ..... %s   %s"
           % (str(cj.get("blob_strumento"))[:8], blob(CENS)[:8],
              "OK" if b_bstr else "DIVERSO"))
    stampa("    ### E QUESTI DUE NUMERI FINISCONO NEL COMMIT DEL REFERTO INSIEME ALLA")
    stampa("    ###   COPPIA che li dichiara: `_corsa.txt` E `_censimento.json`. ### Un")
    stampa("    ###   referto che dichiara un blob e una coppia che ne dichiara un altro")
    stampa("    ###   e' la stessa bugia, spostata di un file.")
    if not b_blob:
        stampa("  ### *** ARTEFATTO DI UN ALTRO BLOB: il braccio FALLISCE. ***")
        stampa("  ###   Qualunque numero preso da questo json parlerebbe di un altro")
        stampa("  ###   file. Non si cita un artefatto rimasto sul disco.")
    occ = len(cj["trovate"])
    fraz = [x for x in cj["trovate"] if x.get("classe") == "FRAZIONE"]
    stampa("  occorrenze del numero nel perimetro .. %d  (attese 13, erano 19)" % occ)
    stampa("  siti di classe FRAZIONE col LETTERALE . %d  (attesi 0)" % len(fraz))
    for x in fraz:
        stampa("    ### RESTA UN LETTERALE: :%s  %s  %s"
               % (x["riga"], x["dentro"], x["testo"][:70]))
    b_ok = (occ == 13 and not fraz and b_rc and b_blob)
    stampa("  ### %s" % ("PASSA" if b_ok else "FALLISCE"))
    esito["braccio_B"] = {"occorrenze": occ, "frazione_letterali": len(fraz),
                          "passa": bool(b_ok),
                          "censimento_returncode": int(q.returncode),
                          "artefatto_stesso_blob": bool(b_blob),
                          "artefatto_blob_sim_ok": bool(b_bsim),
                          "artefatto_blob_strumento_ok": bool(b_bstr),
                          "blob_sim_artefatto": cj.get("blob_sim"),
                          "blob_strumento_artefatto": cj.get("blob_strumento"),
                          "blob_censimento_sul_disco": blob(CENS),
                          "righe_letterali": [x["riga"] for x in fraz]}

    # ======================================================== BRACCIO C
    stampa("")
    stampa("-" * 100)
    stampa("BRACCIO `C` -- t = %g, VERIFICATO SUI VALORI al primo evento di ciascun tipo" % T_PROVA)
    # ### DUE COPIE, E SERVONO ENTRAMBE.
    #   ### **`C0`** con `MITOSI_DIR = 0` *(il valore del sorgente)*: verifica il ramo
    #     NORMALE di `fm`, che nessun'altra copia con la formula giusta esegue.
    #   ### **`C1`** con `--mitosi-dir=1.0`: verifica il ramo del `bias`, che con il
    #     valore del sorgente ### **non girerebbe mai.**
    #   ### \u26d4 Con la sola `C1` il ramo normale restava SCOPERTO -- errore del
    #     guardiano, dichiarato da lui.
    stampa("  --- COPIA `C0`: t = %g, MITOSI_DIR = 0 (il valore del sorgente)" % T_PROVA)
    p_c0 = copia_patchata(p_prima, os.path.join(FUORI, "_sim_t04_md0.py"),
                          ["--t=%g" % T_PROVA])
    c0 = misura_valori(p_c0, "c0", stampa, T_PROVA)
    stampa("")
    stampa("  --- COPIA `C1`: t = %g, MITOSI_DIR = 1.0 (il ramo del bias ACCESO)" % T_PROVA)
    stampa("      ### Verificato PRIMA di scriverlo: il ramo gira al PRIMO evento di")
    stampa("      ###   divisione e |bias| vale 0.1135, NON zero.")
    p_c = copia_patchata(p_prima, os.path.join(FUORI, "_sim_t04.py"),
                         ["--t=%g" % T_PROVA, "--mitosi-dir=1.0"])
    c1 = misura_valori(p_c, "c1", stampa, T_PROVA)
    # ### LA COPERTURA PER SITO: ogni sito deve essere verificato SUI VALORI da almeno
    #   una delle due copie, e il referto dice DA QUALE.
    stampa("")
    stampa("  LA COPERTURA PER SITO: chi ha verificato che cosa, sui VALORI")
    stampa("    %-9s %-28s %-9s %-9s %s" % ("sito", "chiave", "C0", "C1", "esito"))
    cop = {}
    for _s in SITI:
        _ch = CHIAVI_DEL_SITO[_s]
        _in0 = [k for k in _ch if isinstance(c0.get(k), dict)]
        _in1 = [k for k in _ch if isinstance(c1.get(k), dict)]
        _ok0 = all(c0[k]["ok"] for k in _in0) if _in0 else None
        _ok1 = all(c1[k]["ok"] for k in _in1) if _in1 else None
        cop[_s] = {"chiavi": list(_ch), "in_C0": _in0, "in_C1": _in1,
                   "ok_C0": _ok0, "ok_C1": _ok1,
                   "coperto": bool(_in0 or _in1),
                   "passa": bool((_ok0 is not False) and (_ok1 is not False)
                                 and (_in0 or _in1))}
        stampa("    %-9s %-28s %-9s %-9s %s"
               % (_s, ", ".join(_ch)[:28],
                  ("OK" if _ok0 else "DIVERSO") if _in0 else "-",
                  ("OK" if _ok1 else "DIVERSO") if _in1 else "-",
                  "PASSA" if cop[_s]["passa"] else "*** FALLISCE ***"))
    _scoperti = [s for s in SITI if not cop[s]["coperto"]]
    if _scoperti:
        stampa("    ### *** %d SITI NON VERIFICATI SUI VALORI DA NESSUNA COPIA: %s ***"
               % (len(_scoperti), ", ".join(_scoperti)))
        stampa("    ### Il braccio `C` NON copre quei siti, e va detto invece di")
        stampa("    ###   dichiararlo passato.")
    else:
        stampa("    ### ogni sito e' verificato sui VALORI da almeno una copia.")
    stampa("    ### E le due attese del mandato: `fm` in `C0` (%s), `fm_bias` in `C1` (%s)."
           % (bool(cop["fm"]["in_C0"]), bool(cop["fm_bias"]["in_C1"])))
    c_esito = {"C0": c0, "C1": c1, "copertura": cop,
               "siti_scoperti": _scoperti,
               "fm_in_C0": bool(cop["fm"]["in_C0"]),
               "fm_bias_in_C1": bool(cop["fm_bias"]["in_C1"])}
    esito["braccio_C"] = c_esito

    # ======================================================== IL CASO ROVESCIO
    stampa("")
    stampa("-" * 100)
    stampa("CASO ROVESCIO -- il ramo normale di `fm` scritto `(1-t)*D`: `C0` deve BOCCIARLO")
    stampa("  ### E' il controllo che PUO' fallire: se `C0` non lo boccia, non sta")
    stampa("  ###   verificando la formula ma soltanto la sua presenza.")
    p_rov = copia_patchata(p_prima, os.path.join(FUORI, "_sim_fm_rovescio.py"),
                           ["--t=%g" % T_PROVA, "--fm-rovescio"])
    rov = misura_valori(p_rov, "rovescio", None, T_PROVA)
    _k = CHIAVI_DEL_SITO["fm"][0]
    _bocciato = isinstance(rov.get(_k), dict) and not rov[_k]["ok"]
    _dm = rov.get("_D_max")
    stampa("  `D` massimo nella scena: %s  ### %s"
           % ("%.6f" % _dm if _dm is not None else "NON MISURATO",
              "la distinzione fra le due formule e' REALE"
              if (_dm or 0.0) > 0 else
              "*** D ~ 0: le due formule coincidono, la bocciatura NON "
              "proverebbe nulla ***"))
    esito.setdefault("caso_rovescio_D", _dm)
    stampa("  la chiave `%s`: %s" % (_k, "DIVERSA (bocciato)" if _bocciato else
                                     ("OK -- *** NON BOCCIATO ***"
                                      if isinstance(rov.get(_k), dict)
                                      else "*** ASSENTE: il ramo non e' stato eseguito ***")))
    stampa("  ### %s" % ("PASSA: `C0` boccia la formula rovesciata." if _bocciato else
                         "FALLISCE: `C0` non distingue la formula giusta da quella rovesciata."))
    esito["caso_rovescio"] = {"chiave": _k, "bocciato": bool(_bocciato),
                              "esito": rov.get(_k)}

    # ======================================================== BRACCIO C-bis
    stampa("")
    stampa("-" * 100)
    stampa("BRACCIO `C-bis` -- SEI copie, una per sito al letterale. SEI bocciature.")
    cb = {}
    for sito in SITI:
        # ### la copia `fm_bias` accende `MITOSI_DIR`, cosi' ANCHE `C` la raggiunge:
        #   senza, sarebbe scoperta dal SOLO TESTO del braccio `B`.
        _opz = ["--t=%g" % T_PROVA, "--letterale=%s" % sito]
        if sito == "fm_bias":
            _opz.append("--mitosi-dir=1.0")
        pp = copia_patchata(p_prima, os.path.join(FUORI, "_sim_let_%s.py" % sito), _opz)
        # (B) il censimento sulla copia
        qb = subprocess.run([sys.executable, "-c", (
            "import ast,io,sys;sys.path.insert(0,r'%s');"
            "src=io.open(r'%s',encoding='utf-8').read();"
            "print(sum(1 for s in ('(0.5 + bias)','- 0.5 * D','0.5 * self.pos[a]',"
            "'0.5 * self.d[sel]','0.5 * _L_sch','0.5 * net.pos[c[') if s in src))"
            % (os.path.join(RADICE, "csv"), pp))], capture_output=True, text=True)
        # ### ANCHE QUESTO returncode SI LEGGE: un sottoprocesso che muore darebbe
        #   `letterali = 0`, cioe' ### **la copia sembrerebbe pulita** -- il falso-zero
        #   piu' comodo possibile, proprio nel braccio che deve BOCCIARE.
        if qb.returncode != 0:
            stampa("    ### *** il conteggio dei letterali su `%s` e' FALLITO "
                   "(returncode %d): il braccio non puo' concludere ***"
                   % (sito, qb.returncode))
            stampa("    ###   %s" % ((qb.stderr or "").strip().split(NL) or [""])[-1][:130])
        letterali = int((qb.stdout or "0").strip() or 0) if qb.returncode == 0 else -1
        v = misura_valori(pp, "cbis_%s" % sito, None, T_PROVA)
        sbagliate = [k for k, x in v.items() if isinstance(x, dict) and not x.get("ok")]
        # ### ⛔ UN SITO CHE `C` NON PUO' RAGGIUNGERE, e si DICHIARA invece di
        #   aggiustare il criterio: con `MITOSI_DIR = 0.0` nella configurazione del
        #   driver, il ramo `fm = (0.5 + bias)*D` ### **NON GIRA MAI**. Quindi la copia
        #   `--letterale=fm_bias` ### **non puo'** essere scoperta da `C`: la scopre
        #   ### **B**, che legge l'AST e vede anche i rami spenti.
        #   ### 📌 Non e' un'eccezione comoda: e' la ragione per cui `B` esiste.
        # ### NON C'E' PIU' UN SITO IRRAGGIUNGIBILE: la copia `fm_bias` accende
        #   `MITOSI_DIR`, quindi ANCHE `C` deve scoprirla. ### Il criterio e' lo stesso
        #   per tutti e sei, SENZA ECCEZIONI.
        scoperta = (letterali >= 1) and bool(sbagliate)
        cb[sito] = {"letterali_B": letterali, "grandezze_sbagliate": sbagliate,
                    "mitosi_dir_acceso": bool(sito == "fm_bias"),
                    "scoperta": bool(scoperta)}
        stampa("  %-9s B: %d letterale  ·  C: %s  ->  %s"
               % (sito, letterali,
                  ("sbagliate %s" % sbagliate) if sbagliate else "NESSUNA sbagliata",
                  "SCOPERTA" if scoperta else "*** NON SCOPERTA ***"))
    tutte = all(cb[s]["scoperta"] for s in SITI)
    stampa("  ### %s" % ("PASSA: sei copie, sei bocciature." if tutte else
                         "FALLISCE: una copia NON e' scoperta, e il sigillo non discrimina."))
    esito["braccio_C_bis"] = cb

    # ======================================================== IL RIEPILOGO
    stampa("")
    stampa("=" * 100)
    stampa("### IL RIEPILOGO")
    stampa("###   braccio 0 ........ %s" % ("PASSA" if esito["braccio_0"] else "FALLISCE"))
    for n in per_scena:
        stampa("###   braccio A `%-11s` %s"
               % (n, "PASSA" if per_scena[n]["passa"] else "FALLISCE"))
    stampa("###   braccio A-tr .... %s"
           % ("PASSA" if not vuoti else "FERMA: %s a zero dappertutto" % ", ".join(vuoti)))
    stampa("###   braccio B ........ %s" % ("PASSA" if b_ok else "FALLISCE"))
    _cpassa = (not c_esito["siti_scoperti"]
               and all(c_esito["copertura"][s]["passa"] for s in SITI))
    stampa("###   braccio C0+C1 .... %s  (siti scoperti: %s)"
           % ("PASSA" if _cpassa else "FALLISCE",
              c_esito["siti_scoperti"] or "nessuno"))
    stampa("###   caso ROVESCIO .... %s"
           % ("PASSA" if esito["caso_rovescio"]["bocciato"] else "FALLISCE"))
    stampa("###   braccio C-bis .... %s" % ("PASSA" if tutte else "FALLISCE"))
    stampa("=" * 100)

    io.open(os.path.join(FUORI, "_sigillo.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(esito, indent=1, ensure_ascii=False, default=str))
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(out) + NL)
    print("  referto .. %s" % FUORI)


def misura_valori(percorso, nome, stampa, t):
    """### I VALORI, uno per uno, al PRIMO evento di ciascun tipo. NON il *<<differisce>>*."""
    with contextlib.redirect_stdout(io.StringIO()):
        m = carica(percorso, "_s6a_%s" % nome)
        spia = SpiaValori(m)
        net = costruisci(m, 11, os.path.join(FUORI, "_sc_%s" % nome), True)
        for _ in range(72):
            _passo.passo_pieno(m, net)
    fuori = {}
    cd = spia.ctx.get("divisione")
    cs = spia.ctx.get("schwinger")
    pn = spia.pre_nasce

    def controlla(chiave, atteso, avuto, nota=""):
        a = np.asarray(atteso, dtype=float).ravel()
        b = np.asarray(avuto, dtype=float).ravel()
        ok = (a.shape == b.shape) and np.array_equal(a, b)
        fuori[chiave] = {"ok": bool(ok), "n": int(a.size), "nota": nota,
                         "max_scarto": (float(np.max(np.abs(a - b)))
                                        if a.shape == b.shape and a.size else None)}
        if stampa:
            stampa("    %-26s %s  (%d voci%s)"
                   % (chiave, "OK" if ok else "*** DIVERSO ***", a.size,
                      "" if ok else ", scarto max %.3e" % fuori[chiave]["max_scarto"]
                      if fuori[chiave]["max_scarto"] is not None else ""))
    if cd is not None:
        q = cd["quante"]
        # i VALORI che entrano in `_nasce` (PRIMA del pavimento)
        vm = pn.get("mitosi", {}).get("v")
        if vm is not None and len(vm) == 2 * q:
            controlla("dh_a = t*d[sel]", t * cd["d_sel"], vm[:q], "prima del pavimento")
            controlla("dh_b = (1-t)*d[sel]", (1.0 - t) * cd["d_sel"], vm[q:],
                      "prima del pavimento")
        controlla("pos_figlio convesso",
                  (1.0 - t) * cd["pos_a"] + t * cd["pos_b"], cd["pos_figlio"])
        # ### `fm` SI RICOSTRUISCE, non si confronta con se stesso: `D` e'
        #   `_wphi(phi[a] - phi[b])` *(letto dal codice, `:8522`)*, e il ramo che gira
        #   con `MITOSI_DIR = 0` e' `fm = (phi[a] - t*D) % dphi`.
        pm = cd.get("pm") or {}
        if pm:
            _phia = pm["phi"][cd["a"]]
            _phib = pm["phi"][cd["b"]]
            _D = np.asarray(m.Rete._wphi(_phia - _phib), dtype=float)
            _md = float(getattr(m, "MITOSI_DIR", 0.0))
            # ### `D` VA DICHIARATO, e non e' un dettaglio: se `D` fosse ~0 le due
            #   formule `phi[a] - t*D` e `phi[a] - (1-t)*D` ### **coinciderebbero**, e
            #   sia il confronto di `C0` sia la bocciatura del caso ROVESCIO sarebbero
            #   ### **veri per fortuna, non per la formula.** ### Un `FALSO-ZERO`.
            fuori["_D_max"] = float(np.max(np.abs(_D))) if np.size(_D) else 0.0
            if _md != 0.0:
                # ### il `bias` RICALCOLATO dal sigillo, non letto dal contesto:
                #   `twn` e' la media di `|tw|` sugli archi del nodo, come in `mitosi`.
                _n = pm["n"]
                _twn = np.zeros(_n)
                _ii, _jj, _tw = pm["i"], pm["j"], np.abs(pm["tw"])
                np.add.at(_twn, _ii[_ii < _n], _tw[_ii < _n])
                np.add.at(_twn, _jj[_jj < _n], _tw[_jj < _n])
                _twn = _twn / np.maximum(pm["deg"][:_n], 1)
                _bias = 0.5 * np.tanh(_md * (_twn[cd["a"]] - _twn[cd["b"]]))
                controlla("fm = (phi[a]-(t+bias)*D)",
                          (_phia - (t + _bias) * _D) % pm["dphi"], cd["fm"],
                          "ramo MITOSI_DIR = %g ACCESO, bias ricalcolato" % _md)
                fuori["_bias_non_nullo"] = bool(np.any(_bias != 0))
            else:
                controlla("fm = (phi[a] - t*D) mod",
                          (_phia - t * _D) % pm["dphi"], cd["fm"],
                          "ramo senza MITOSI_DIR")
    if cs is not None:
        nc = cs["quante"]
        L = np.linalg.norm(cs["pos_aa"] - cs["pos_bb"], axis=1)
        vs = pn.get("schwinger", {}).get("v")
        if vs is not None and len(vs) == 2 * nc:
            controlla("dd_a = max(t*L, 0.05)", np.maximum(t * L, 0.05), vs[:nc])
            controlla("dd_b = max((1-t)*L, 0.05)", np.maximum((1.0 - t) * L, 0.05), vs[nc:])
        if "pos_k" in cs:
            controlla("pos antinodo convesso",
                      (1.0 - t) * cs["pos_aa"] + t * cs["pos_bb"], cs["pos_k"])
    fuori["_eventi"] = {"divisione": cd is not None, "schwinger": cs is not None}
    return fuori


if __name__ == "__main__":
    principale()
