# -*- coding: utf-8 -*-
"""**IL SIGILLO DEL COMMIT `6b`: `MITOSI_2LAM` diventa LEGGE, in forma GENERALE.**

| braccio | che cosa prova |
|---|---|
| **`0`** | la patch committata, applicata al *prima*, da' **il blob di oggi** |
| **`A`** | **IDENTICO AL BYTE** sulle tre scene **con** `--mitosi-2lam`, stato **e** contatori |
| **`B`** | la scena **senza** il flag: **NON identica, ed e' ATTESO** — `B1` i troncamenti a zero, `B2` la legge evento per evento, `B3` i numeri |
| **`C`** | `FRAZ_NASCITA = 0.4` su tutte le scene: nessun troncamento, e **ogni** `d` ammesso ha `0.4*d >= LAM` |
| **`C-bis`** | **TRE copie che DEVONO fallire** |
| **`D`** | il flag fra i `[flag-inerti]`, e l'archivio col cancello vecchio **verbatim** |

### ⛔ **I CONTATORI NUOVI SI SEPARANO PER NOME ATTESO, NON PER <<STA SOLO NELL'OGGI>>.**
Un attributo nuovo che ### **non ho previsto FA FALLIRE il braccio `A`**: altrimenti
l'esclusione diventa ### **un buco in cui passa qualunque cosa**, cioe' un `FALSO-ZERO`.

**COMANDO:** `python csv/_seal_fork/_sigillo_legge_2lam.py`
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

import numpy as np   # noqa: E402
import _cli_flag     # noqa: E402
import _passo        # noqa: E402

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SIM = os.path.join(RADICE, "soliton_simulator.py")
PATCH = os.path.join(_QUI, "_legge_2lam_patch.py")
ARCHIVIO = os.path.join(RADICE, "csv", "_archivio", "_rami_off_cura2.py")
FUORI = os.path.join(_QUI, "_sigillo_legge_2lam")
NL = chr(10)

# ### L'ANCORA DEL *PRIMA*: una stringa che il `6b` INTRODUCE. `sim_prima_del_flag` prende il
#   commit piu' VECCHIO che la introduce e poi il suo PADRE (`H-P8`): il *prima* non si
#   prende da `HEAD`.
ANCORA = "_g_m2l_rif_solo_lam"
SCENE = (("corta", 11, 72), ("lunga", 11, 150), ("altro_seme", 12, 72))
T_PROVA = 0.4
# ### I CONTATORI CHE IL `6b` AGGIUNGE, dichiarati PER NOME. Il braccio `A` li separa da
#   questa lista e ### **non** da <<quelli che stanno solo nell'oggi>>.
NUOVI_ATTESI = ("_g_m2l_rif_solo_dens", "_g_m2l_rif_solo_lam", "_g_m2l_rif_entrambi",
                "_g_m2l_tw_rif")


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def carica(percorso, nome):
    spec = importlib.util.spec_from_file_location(nome, percorso)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def copia_patchata(sorgente, dest, argomenti):
    """La SORGENTE e' SEMPRE il *prima*: le ancore della patch descrivono il codice
    **prima** della cura *(lezione del sigillo del commit 5, che cadde proprio su questo)*."""
    io.open(dest, "wb").write(io.open(sorgente, "rb").read())
    q = subprocess.run([sys.executable, PATCH, "--file=%s" % dest] + list(argomenti),
                       capture_output=True, text=True)
    assert q.returncode == 0, (q.stdout or "")[-1500:] + (q.stderr or "")[-1500:]
    return dest


def costruisci(m, seme, dest, con_2lam=True):
    """Scena `MASSE-COERENTI`, dal CLI del driver: nessun attributo a mano *(`H-P3`)*."""
    _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=%d" % seme], dest=dest)
    argv = [x for x in argv if con_2lam or x != "--mitosi-2lam"]
    vecchia = list(sys.argv)
    sys.argv = list(argv)
    try:
        a = m._cli()
        m._applica_flag(a)
    finally:
        sys.argv = vecchia
    m._applica_regime(a)
    m._NMASSE_VIDEO["n"] = 2
    m._NMASSE_VIDEO["sep"] = 3.0
    m._NMASSE_VIDEO["size"] = None
    m.avvia_test("MASSE-COERENTI")()
    return m.net


def _dig(x):
    return hashlib.sha1(pickle.dumps(x, protocol=4)).hexdigest()[:16]


def stato(net, senza=()):
    """TUTTO cio' che sta in `__dict__`, non solo ndarray e scalari.

    `senza` toglie i contatori NUOVI, e la lista e' ### **dichiarata per nome**.
    """
    fuori = {}
    for k, v in vars(net).items():
        if k in senza:
            continue
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
            a, b = np.asarray(a), np.asarray(b)
            if a.shape != b.shape:
                diff.append((k, "FORMA %s contro %s" % (a.shape, b.shape)))
            elif not np.array_equal(a, b, equal_nan=True):
                diff.append((k, "celle diverse"))
        else:
            if a != b and not (a != a and b != b):
                diff.append((k, "%r contro %r" % (a, b)))
    return diff


class SpiaLegge:
    """Registra, PER OGNI divisione ammessa, `min(t, 1-t) * d >= LAM` e il `d` del padre.

    ### **Evento per evento, non in media:** una media passerebbe anche con una violazione
    sola, ed e' ### **proprio la violazione sola** che il braccio `B2` cerca.
    """

    def __init__(self, m, t):
        self.m = m
        self.t = t
        self.eventi = []
        self.soglie = []
        self._nascita_vera = m.nascita
        self._decidi_vera = m.Rete.decidi_divisione
        spia = self

        def _decidi(selfr):
            sel, perche = spia._decidi_vera(selfr)
            if isinstance(perche, dict) and "soglia" in perche:
                _s = np.asarray(perche["soglia"], float).ravel()
                if _s.size:
                    spia.soglie.append((float(_s.min()), float(_s.max())))
            return sel, perche

        m.Rete.decidi_divisione = _decidi

        def _nascita(net, evento, c):
            if evento == "divisione" and "sel" in c:
                d = np.asarray(net.d, float)[c["sel"]]
                lam = float(getattr(spia.m, "LAM"))
                corto = min(spia.t, 1.0 - spia.t) * d
                spia.eventi.append({"quante": int(np.size(d)),
                                    "d_min": float(d.min()) if d.size else None,
                                    "corto_min": float(corto.min()) if corto.size else None,
                                    "lam": lam,
                                    "ok": bool(np.all(corto >= lam))})
            return spia._nascita_vera(net, evento, c)

        m.nascita = _nascita


def gira(percorso, nome, seme, passi, con_2lam, t, stampa=None):
    """Una corsa sola, con la spia della legge. Da' `(net, modulo, spia)`."""
    with contextlib.redirect_stdout(io.StringIO()):
        m = carica(percorso, "_s6b_%s" % nome)
        spia = SpiaLegge(m, t)
        net = costruisci(m, seme, os.path.join(FUORI, "_sc_%s" % nome), con_2lam)
        for _ in range(passi):
            _passo.passo_pieno(m, net)
    return net, m, spia


def conta(net):
    f = {}
    for k in ("_g_m2l_tot", "_g_m2l_negati", "_g_m2l_dmin", "_g_m2l_rif_solo_dens",
              "_g_m2l_rif_solo_lam", "_g_m2l_rif_entrambi", "_sm_trd_mitosi",
              "_sm_trd0_mitosi", "_sm_trd_schwinger", "_sm_trd0_schwinger", "negate"):
        f[k] = getattr(net, k, None)
    f["_g_m2l_tw_rif"] = list(getattr(net, "_g_m2l_tw_rif", []))
    f["n"] = int(net.n)
    f["archi"] = int(np.size(net.i))
    return f


def principale():
    out = []

    def stampa(*x):
        s = " ".join(str(y) for y in x)
        out.append(s)
        print(s)

    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    esito = {"blob_sim": blob(SIM), "blob_sigillo": blob(os.path.abspath(__file__)),
             "blob_patch": blob(PATCH),
             "piattaforma": {"sistema": platform.system(), "macchina": platform.machine(),
                             "python": platform.python_version(), "numpy": np.__version__}}
    stampa("=" * 100)
    stampa("IL SIGILLO DEL COMMIT 6b: `MITOSI_2LAM` diventa LEGGE, in forma GENERALE")
    stampa("=" * 100)
    stampa("  simulatore di OGGI .. %s" % blob(SIM)[:8])
    stampa("  questo sigillo ...... %s" % blob(os.path.abspath(__file__))[:8])
    stampa("  la patch ............ %s" % blob(PATCH)[:8])
    stampa("  piattaforma ......... %s %s" % (platform.system(), platform.machine()))
    stampa("  Python .............. %s" % platform.python_version())
    stampa("  numpy ............... %s" % np.__version__)
    stampa("  ### I CONTEGGI VALGONO PER QUESTA PIATTAFORMA. Cio' che NON dipende dalla")
    stampa("  ###   piattaforma e' l'IDENTITA' fra il *prima* e l'*oggi*.")
    stampa("  ### E su questa macchina il PRIMO CANDIDATO con il flag arriva al passo 74:")
    stampa("  ###   le scene da 72 passi NON portano statistica del cancello, e i numeri")
    stampa("  ###   del braccio B3 vengono da `lunga` (150 passi). MISURATO, non supposto.")

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

    # ======================================================== BRACCIO A
    stampa("")
    stampa("-" * 100)
    stampa("BRACCIO `A` -- BYTE-IDENTICO sulle TRE scene CON `--mitosi-2lam`")
    stampa("  ### I due blob girano IN LOCKSTEP e si confrontano DOPO OGNI PASSO.")
    stampa("  ### I contatori NUOVI si separano PER NOME ATTESO: %s"
           % ", ".join(NUOVI_ATTESI))
    stampa("  ### ⛔ Un attributo nuovo NON PREVISTO fa FALLIRE il braccio: altrimenti")
    stampa("  ###   l'esclusione sarebbe un buco in cui passa qualunque cosa.")
    per_scena = {}
    for nome, seme, passi in SCENE:
        stampa("")
        stampa("  " + "=" * 96)
        stampa("  SCENA `%s` -- seme %d, %d passi, --mitosi-2lam: SI" % (nome, seme, passi))
        with contextlib.redirect_stdout(io.StringIO()):
            m1 = carica(p_prima, "_s6b_pr_%s" % nome)
            m2 = carica(SIM, "_s6b_nu_%s" % nome)
            n1 = costruisci(m1, seme, os.path.join(FUORI, "_sc1_%s" % nome), True)
            n2 = costruisci(m2, seme, os.path.join(FUORI, "_sc2_%s" % nome), True)
        d0 = confronta(stato(n1), stato(n2, senza=NUOVI_ATTESI))
        primo = None
        for p in range(1, passi + 1):
            with contextlib.redirect_stdout(io.StringIO()):
                _passo.passo_pieno(m1, n1)
                _passo.passo_pieno(m2, n2)
            d = confronta(stato(n1), stato(n2, senza=NUOVI_ATTESI))
            if d and primo is None:
                primo = (p, list(d))
        # ### GLI ATTRIBUTI NUOVI NON PREVISTI: si cercano, e se ci sono il braccio FALLISCE.
        soli_oggi = [k for k in vars(n2) if k not in vars(n1)]
        imprevisti = [k for k in soli_oggi if k not in NUOVI_ATTESI]
        stampa("    attributi solo nell'OGGI: %s" % (sorted(soli_oggi) or "nessuno"))
        stampa("    di cui NON PREVISTI ....: %s" % (sorted(imprevisti) or "nessuno"))
        passa = bool(primo is None and not d0 and not imprevisti)
        if passa:
            stampa("    ### PASSA: ZERO differenze su %d passi, su OGNI voce di `__dict__`"
                   % passi)
            stampa("    ###   (ndarray, scalari, liste, dict, matrice SPARSA, stato del")
            stampa("    ###   generatore), CONTATORI COMPRESI -- meno i NUOVI, dichiarati.")
        else:
            q = primo or (0, d0)
            stampa("    ### FALLISCE: prima differenza al passo %d, %d voci:"
                   % (q[0], len(q[1])))
            for k, w in q[1][:15]:
                stampa("    ###   %-30s %s" % (k, w))
            if imprevisti:
                stampa("    ### *** E %d ATTRIBUTI NUOVI NON PREVISTI: %s ***"
                       % (len(imprevisti), imprevisti))
        c1, c2 = conta(n1), conta(n2)
        stampa("    i contatori, prima / oggi:")
        for k in sorted(set(c1) | set(c2)):
            if k == "_g_m2l_tw_rif":
                stampa("      %-22s %s / %s (lunghezza)" % (k, len(c1[k]), len(c2[k])))
            else:
                stampa("      %-22s %s / %s" % (k, c1.get(k), c2.get(k)))
        per_scena[nome] = {"seme": seme, "passi": passi, "passa": passa,
                           "prima_differenza": (primo[0] if primo else None),
                           "differenze": ([[k, w] for k, w in primo[1]] if primo
                                          else [[k, w] for k, w in d0]),
                           "attributi_solo_oggi": sorted(soli_oggi),
                           "attributi_imprevisti": sorted(imprevisti),
                           "contatori_prima": c1, "contatori_oggi": c2}
    esito["scene"] = per_scena

    # ======================================================== BRACCIO B
    stampa("")
    stampa("-" * 100)
    stampa("BRACCIO `B` -- la scena SENZA `--mitosi-2lam`: NON identica, ed e' ATTESO")
    stampa("  ### E qui si misura il CALO di `n`, che il piano prevedeva.")
    stampa("  ### ⛔ E VA DETTO COME VA DETTO: quel calo e' IMPOSTO PER COSTRUZIONE --")
    stampa("  ###   meno nascite ammesse, meno nodi -- e NON e' un fenomeno emergente.")
    b = {}
    for nome, seme, passi in (("senza_2lam_corta", 11, 72), ("senza_2lam_lunga", 11, 150)):
        stampa("")
        stampa("  SCENA `%s` -- seme %d, %d passi, senza il flag" % (nome, seme, passi))
        n1, m1, s1 = gira(p_prima, "pr_%s" % nome, seme, passi, False, 0.5)
        n2, m2, s2 = gira(SIM, "nu_%s" % nome, seme, passi, False, 0.5)
        c1, c2 = conta(n1), conta(n2)
        # B1
        b1 = (c2["_sm_trd_mitosi"] in (0, None)) and (c2["_sm_trd0_mitosi"] in (0, None))
        stampa("    B1  i troncamenti della MITOSI, prima / oggi:")
        for k in ("_sm_trd_mitosi", "_sm_trd0_mitosi"):
            stampa("          %-20s %s / %s" % (k, c1.get(k), c2.get(k)))
        stampa("        ### uno ZERO atteso vale solo se accanto c'e' il numero che ERA.")
        stampa("        ### %s" % ("PASSA" if b1 else "FALLISCE"))
        # B2
        tutti = s2.eventi
        b2 = all(e["ok"] for e in tutti) if tutti else None
        stampa("    B2  la legge EVENTO PER EVENTO, su %d divisioni ammesse:" % len(tutti))
        for e in tutti[:8]:
            stampa("          %2d archi, d_min %.6f, corto_min %.6f, LAM %.6f  %s"
                   % (e["quante"], e["d_min"], e["corto_min"], e["lam"],
                      "OK" if e["ok"] else "*** VIOLATA ***"))
        if len(tutti) > 8:
            stampa("          ... e altri %d eventi" % (len(tutti) - 8))
        stampa("        ### %s" % ("PASSA: min(t,1-t)*d >= LAM su OGNI evento." if b2
                                   else ("FALLISCE: almeno un evento viola la legge."
                                         if b2 is False else
                                         "VUOTO: nessuna divisione ammessa -- NON PROVA NULLA")))
        # B3
        stampa("    B3  i numeri:")
        stampa("          %-24s %s / %s" % ("n al passo %d" % passi, c1["n"], c2["n"]))
        stampa("          %-24s %s / %s" % ("archi", c1["archi"], c2["archi"]))
        for k in ("_g_m2l_tot", "_g_m2l_negati", "_g_m2l_dmin", "_g_m2l_rif_solo_dens",
                  "_g_m2l_rif_solo_lam", "_g_m2l_rif_entrambi", "negate"):
            stampa("          %-24s %s / %s" % (k, c1.get(k), c2.get(k)))
        tw = np.asarray(c2["_g_m2l_tw_rif"], float)
        if tw.size:
            _pc = float(getattr(m2, "PHI_CRIT", float("nan")))
            stampa("          |tw| dei rifiutati per LAM: %d valori" % tw.size)
            stampa("            min %.6f  mediana %.6f  max %.6f"
                   % (tw.min(), float(np.median(tw)), tw.max()))
            stampa("            sopra PHI_CRIT (%.4f): %d   sopra 3*pi (%.4f): %d"
                   % (_pc, int(np.sum(tw > _pc)), 3 * np.pi,
                      int(np.sum(tw > 3 * np.pi))))
        else:
            stampa("          |tw| dei rifiutati per LAM: NESSUN rifiuto in questa scena")
        if s2.soglie:
            _mn = min(x[0] for x in s2.soglie)
            _mx = max(x[1] for x in s2.soglie)
            stampa("          le SOGLIE locali: da %.6f a %.6f, su %d chiamate"
                   % (_mn, _mx, len(s2.soglie)))
        stampa("          il ramo di soglia, DAI FLAG e non indovinato:")
        stampa("            TORS_4PI = %s   PHI_CRIT = %s"
               % (getattr(m2, "TORS_4PI", "ASSENTE"), getattr(m2, "PHI_CRIT", "ASSENTE")))
        b[nome] = {"B1": bool(b1), "B2": b2, "eventi": tutti,
                   "contatori_prima": c1, "contatori_oggi": c2,
                   "soglie": s2.soglie[:200]}
    esito["braccio_B"] = b
    b_ok = all(v["B1"] and (v["B2"] is not False) for v in b.values())

    # ======================================================== BRACCIO C
    stampa("")
    stampa("-" * 100)
    stampa("BRACCIO `C` -- FRAZ_NASCITA = %g su TUTTE le scene" % T_PROVA)
    p_c = copia_patchata(p_prima, os.path.join(FUORI, "_sim_t04.py"),
                         ["--t=%g" % T_PROVA])
    cc = {}
    for nome, seme, passi in SCENE:
        n, m, s = gira(p_c, "c_%s" % nome, seme, passi, True, T_PROVA)
        c = conta(n)
        ok_tr = (c["_sm_trd_mitosi"] in (0, None))
        ok_ev = all(e["ok"] for e in s.eventi) if s.eventi else None
        cc[nome] = {"trd_mitosi": c["_sm_trd_mitosi"], "eventi": s.eventi,
                    "passa": bool(ok_tr and (ok_ev is not False))}
        stampa("  %-12s _sm_trd_mitosi = %-6s  divisioni ammesse: %-3d  %s"
               % (nome, c["_sm_trd_mitosi"], len(s.eventi),
                  "OK" if cc[nome]["passa"] else "*** FALLISCE ***"))
        for e in s.eventi[:4]:
            stampa("                 d_min %.6f  0.4*d_min %.6f  LAM %.6f  %s"
                   % (e["d_min"], T_PROVA * e["d_min"], e["lam"],
                      "OK" if e["ok"] else "VIOLATA"))
    c_ok = all(v["passa"] for v in cc.values())
    stampa("  ### %s" % ("PASSA" if c_ok else "FALLISCE"))
    esito["braccio_C"] = cc

    # ======================================================== LA FINESTRA di C-bis (i)
    stampa("")
    stampa("-" * 100)
    stampa("LA FINESTRA DI `C-bis (i)`: esistono candidati con 1.6 <= d < 2.0?")
    stampa("  ### SENZA DI LORO quel caso <<che deve fallire>> passerebbe PER ASSENZA DI")
    stampa("  ###   MATERIA: un FALSO-ZERO. Si MISURA, e se manca si DICHIARA.")
    n_f, m_f, s_f = gira(p_c, "finestra", 11, 150, True, T_PROVA)
    lam = float(getattr(m_f, "LAM"))
    dmin = getattr(n_f, "_g_m2l_dmin", None)
    stampa("  LAM = %.6f   2*LAM = %.6f   LAM/%g = %.6f"
           % (lam, 2 * lam, T_PROVA, lam / T_PROVA))
    stampa("  _g_m2l_dmin sulla scena `lunga` con t=%g: %s" % (T_PROVA, dmin))
    finestra = (dmin is not None and 2 * lam <= float(dmin) < lam / T_PROVA)
    stampa("  ### il `d` minimo cade nella finestra [2*LAM, LAM/t)? %s" % finestra)
    stampa("  ### ⚠ QUESTO E' UN INDIZIO, NON LA MISURA: `_g_m2l_dmin` e' il MINIMO, e la")
    stampa("  ###   finestra puo' contenere candidati anche se il minimo sta sotto. Il")
    stampa("  ###   VERDETTO vero e' se `C-bis (i)` FALLISCE: se passa, la finestra era")
    stampa("  ###   vuota e il caso va COSTRUITO.")
    esito["finestra_cbis_i"] = {"lam": lam, "dmin": dmin, "indizio": bool(finestra)}

    # ======================================================== BRACCIO C-bis
    stampa("")
    stampa("-" * 100)
    stampa("BRACCIO `C-bis` -- TRE copie che DEVONO fallire")
    casi = (("(i) cancello VECCHIO d >= 2*LAM", ["--t=0.4", "--cancello-vecchio"], 0.4),
            ("(ii) solo (1-t)*d >= LAM", ["--t=0.4", "--solo-destra"], 0.4),
            ("(iii) solo t*d >= LAM", ["--t=0.6", "--solo-sinistra"], 0.6))
    cb = {}
    for et, opz, tt in casi:
        pp = copia_patchata(p_prima, os.path.join(FUORI, "_sim_cbis_%d.py" % len(cb)), opz)
        n, m, s = gira(pp, "cbis_%d" % len(cb), 11, 150, True, tt)
        c = conta(n)
        viol = [e for e in s.eventi if not e["ok"]]
        trd = c["_sm_trd_mitosi"] or 0
        bocciato = bool(viol or trd > 0)
        cb[et] = {"troncamenti": trd, "eventi": len(s.eventi),
                  "violazioni": len(viol), "bocciato": bocciato,
                  "primo_violato": (viol[0] if viol else None)}
        stampa("  %-34s eventi %-3d  violazioni %-3d  troncamenti %-3s  ->  %s"
               % (et, len(s.eventi), len(viol), trd,
                  "BOCCIATO" if bocciato else "*** NON BOCCIATO ***"))
        if viol:
            e = viol[0]
            stampa("        primo violato: d_min %.6f  corto_min %.6f  LAM %.6f"
                   % (e["d_min"], e["corto_min"], e["lam"]))
        elif not s.eventi:
            stampa("        ### ⛔ NESSUNA DIVISIONE AMMESSA: il caso non prova nulla")
            stampa("        ###   (FALSO-ZERO: passerebbe per ASSENZA DI MATERIA)")
    cb_ok = all(v["bocciato"] for v in cb.values())
    stampa("  ### %s" % ("PASSA: tre copie, tre bocciature." if cb_ok else
                         "FALLISCE: una copia NON e' bocciata, e il sigillo non discrimina."))
    esito["braccio_Cbis"] = cb

    # ======================================================== BRACCIO D
    stampa("")
    stampa("-" * 100)
    stampa("BRACCIO `D` -- il flag fra i `[flag-inerti]`, e l'archivio VERBATIM")
    cat = io.StringIO()
    with contextlib.redirect_stdout(cat):
        m_d = carica(SIM, "_s6b_d")
        costruisci(m_d, 11, os.path.join(FUORI, "_sc_d"), True)
    testo = cat.getvalue()
    d1 = ("[flag-inerti]" in testo and "MITOSI_2LAM" in testo)
    stampa("  l'avvio stampa `MITOSI_2LAM` fra i [flag-inerti]? %s" % d1)
    for r in testo.split(NL):
        if "flag-inerti" in r and "MITOSI_2LAM" in r:
            stampa("    %s" % r.strip()[:140])
    stampa("  e l'avviso `[cura5]` NON compare piu'? %s" % ("[cura5]" not in testo))
    # l'archivio contiene il cancello vecchio VERBATIM
    arc = io.open(ARCHIVIO, encoding="utf-8").read()
    atteso = ("if MITOSI_2LAM and len(c):", "_conforme = _dc >= 2.0 * LAM",
              "ok = ok & _conforme")
    d2 = all(x in arc for x in atteso)
    stampa("  l'archivio contiene il cancello vecchio VERBATIM? %s" % d2)
    for x in atteso:
        stampa("    %-44s %s" % (x[:44], "c'e'" if x in arc else "*** MANCA ***"))
    d_ok = bool(d1 and d2 and "[cura5]" not in testo)
    stampa("  ### %s" % ("PASSA" if d_ok else "FALLISCE"))
    esito["braccio_D"] = {"flag_inerti": bool(d1), "archivio_verbatim": bool(d2),
                          "cura5_tolto": bool("[cura5]" not in testo), "passa": d_ok}

    # ======================================================== IL RIEPILOGO
    a_ok = all(per_scena[n]["passa"] for n in per_scena)
    stampa("")
    stampa("=" * 100)
    stampa("### IL RIEPILOGO")
    stampa("###   braccio 0 ........ %s" % ("PASSA" if esito["braccio_0"] else "FALLISCE"))
    for n in per_scena:
        stampa("###   braccio A `%-11s` %s"
               % (n, "PASSA" if per_scena[n]["passa"] else "FALLISCE"))
    stampa("###   braccio B ........ %s" % ("PASSA" if b_ok else "FALLISCE"))
    stampa("###   braccio C ........ %s" % ("PASSA" if c_ok else "FALLISCE"))
    stampa("###   braccio C-bis .... %s" % ("PASSA" if cb_ok else "FALLISCE"))
    stampa("###   braccio D ........ %s" % ("PASSA" if d_ok else "FALLISCE"))
    stampa("=" * 100)
    esito["riepilogo"] = {"0": esito["braccio_0"], "A": a_ok, "B": b_ok, "C": c_ok,
                          "C-bis": cb_ok, "D": d_ok}

    io.open(os.path.join(FUORI, "_sigillo.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(esito, indent=1, ensure_ascii=False, default=str))
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(out) + NL)
    print("  referto .. %s" % FUORI)


if __name__ == "__main__":
    principale()
