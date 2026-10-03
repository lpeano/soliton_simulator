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
ANCORA = "T_NASCITA"
# ### LE TRE SCENE DEL COMMIT 4, PIU' LA QUARTA senza `--mitosi-2lam` (mandato)
SCENE = (("corta", 11, 72, True), ("lunga", 11, 150, True),
         ("altro_seme", 12, 72, True), ("senza_2lam", 11, 72, False))
SITI = ("pos_div", "dh", "fm", "fm_bias", "pos_sch", "dd")
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


def stato(net):
    """TUTTI gli ndarray e gli scalari di `__dict__`: non un insieme scelto da me.

    ### Nessuna copia: il confronto e' IMMEDIATO e i due stati vengono da oggetti
    DIVERSI. Uno `stato()` non si puo' conservare fra i passi.
    """
    fuori = {}
    for k, v in vars(net).items():
        if isinstance(v, np.ndarray) or isinstance(
                v, (int, float, bool, np.integer, np.floating)):
            fuori[k] = v
    return fuori


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
        self._nasce_vero = m.Rete._nasce
        self._nascita_vera = m.nascita
        spia = self

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
                    d["d_sel"] = np.array(net.d[c["sel"]], dtype=float, copy=True)
                    d["pos_a"] = np.array(net.pos[c["a"]], dtype=float, copy=True)
                    d["pos_b"] = np.array(net.pos[c["b"]], dtype=float, copy=True)
                    d["pos_figlio"] = np.array(c["pos_figlio"], dtype=float, copy=True)
                    d["phi_a"] = np.array(net.phi[c["a"]], dtype=float, copy=True)
                    d["phi_b"] = np.array(net.phi[c["b"]], dtype=float, copy=True)
                    d["dphi"] = float(net._dphi())
                    d["fm"] = np.array(c["fm"], dtype=float, copy=True)
                    d["dh"] = np.array(c["dh"], dtype=float, copy=True)
                else:
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
        d0 = confronta(stato(n1), stato(n2))
        primo = None
        for p in range(1, passi + 1):
            with contextlib.redirect_stdout(io.StringIO()):
                _passo.passo_pieno(m1, n1)
                _passo.passo_pieno(m2, n2)
            d = confronta(stato(n1), stato(n2))
            if d and primo is None:
                primo = (p, list(d))
        trs = {c: [int(getattr(n1, c, 0)), int(getattr(n2, c, 0))] for c in TR}
        stampa("    alla costruzione: %d differenze" % len(d0))
        if primo is None and not d0:
            stampa("    ### PASSA: ZERO differenze su %d passi, su TUTTI gli attributi di" % passi)
            stampa("    ###   `net` (ndarray e scalari di `__dict__`), CONTATORI COMPRESI.")
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
                           "sm_tr": trs}
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
    q = subprocess.run([sys.executable, CENS], capture_output=True, text=True, cwd=RADICE)
    jj = os.path.join(RADICE, "csv", "_test_fork", "_censimento_punto_medio",
                      "_censimento.json")
    cj = json.load(io.open(jj, encoding="utf-8"))
    occ = len(cj["trovate"])
    fraz = [x for x in cj["trovate"] if x.get("classe") == "FRAZIONE"]
    stampa("  occorrenze del numero nel perimetro .. %d  (attese 13, erano 19)" % occ)
    stampa("  siti di classe FRAZIONE col LETTERALE . %d  (attesi 0)" % len(fraz))
    for x in fraz:
        stampa("    ### RESTA UN LETTERALE: :%s  %s  %s"
               % (x["riga"], x["dentro"], x["testo"][:70]))
    b_ok = (occ == 13 and not fraz)
    stampa("  ### %s" % ("PASSA" if b_ok else "FALLISCE"))
    esito["braccio_B"] = {"occorrenze": occ, "frazione_letterali": len(fraz),
                          "passa": bool(b_ok),
                          "righe_letterali": [x["riga"] for x in fraz]}

    # ======================================================== BRACCIO C
    stampa("")
    stampa("-" * 100)
    stampa("BRACCIO `C` -- t = %g, VERIFICATO SUI VALORI al primo evento di ciascun tipo" % T_PROVA)
    p_c = copia_patchata(p_prima, os.path.join(FUORI, "_sim_t04.py"),
                         ["--t=%g" % T_PROVA])
    c_esito = misura_valori(p_c, "c", stampa, T_PROVA)
    esito["braccio_C"] = c_esito

    # ======================================================== BRACCIO C-bis
    stampa("")
    stampa("-" * 100)
    stampa("BRACCIO `C-bis` -- SEI copie, una per sito al letterale. SEI bocciature.")
    cb = {}
    for sito in SITI:
        pp = copia_patchata(p_prima, os.path.join(FUORI, "_sim_let_%s.py" % sito),
                            ["--t=%g" % T_PROVA, "--letterale=%s" % sito])
        # (B) il censimento sulla copia
        qb = subprocess.run([sys.executable, "-c", (
            "import ast,io,sys;sys.path.insert(0,r'%s');"
            "src=io.open(r'%s',encoding='utf-8').read();"
            "print(sum(1 for s in ('(0.5 + bias)','- 0.5 * D','0.5 * self.pos[a]',"
            "'0.5 * self.d[sel]','0.5 * _L_sch','0.5 * net.pos[c[') if s in src))"
            % (os.path.join(RADICE, "csv"), pp))], capture_output=True, text=True)
        letterali = int((qb.stdout or "0").strip() or 0)
        v = misura_valori(pp, "cbis_%s" % sito, None, T_PROVA)
        sbagliate = [k for k, x in v.items() if isinstance(x, dict) and not x.get("ok")]
        # ### ⛔ UN SITO CHE `C` NON PUO' RAGGIUNGERE, e si DICHIARA invece di
        #   aggiustare il criterio: con `MITOSI_DIR = 0.0` nella configurazione del
        #   driver, il ramo `fm = (0.5 + bias)*D` ### **NON GIRA MAI**. Quindi la copia
        #   `--letterale=fm_bias` ### **non puo'** essere scoperta da `C`: la scopre
        #   ### **B**, che legge l'AST e vede anche i rami spenti.
        #   ### 📌 Non e' un'eccezione comoda: e' la ragione per cui `B` esiste.
        irraggiungibile = (sito == "fm_bias")
        scoperta = (letterali >= 1) and (bool(sbagliate) or irraggiungibile)
        cb[sito] = {"letterali_B": letterali, "grandezze_sbagliate": sbagliate,
                    "C_irraggiungibile": bool(irraggiungibile),
                    "scoperta": bool(scoperta)}
        stampa("  %-9s B: %d letterale  ·  C: %s  ->  %s"
               % (sito, letterali,
                  ("ramo SPENTO (MITOSI_DIR = 0): C non lo raggiunge, lo scopre B"
                   if irraggiungibile else
                   ("sbagliate %s" % sbagliate) if sbagliate else "NESSUNA sbagliata"),
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
    stampa("###   braccio C ........ %s"
           % ("PASSA" if all(x.get("ok") for x in c_esito.values()
                             if isinstance(x, dict)) else "FALLISCE"))
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
        _D = np.asarray(m.Rete._wphi(cd["phi_a"] - cd["phi_b"]), dtype=float)
        controlla("fm = (phi[a] - t*D) mod",
                  (cd["phi_a"] - t * _D) % cd["dphi"], cd["fm"],
                  "D = _wphi(phi[a]-phi[b]), ricostruito")
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
