# -*- coding: utf-8 -*-
"""I CONTROLLI DEL MANDATO DEL `0.3` A ZERO: `C0`, `C-letture`, `C1`, `C-fallisce`.

*(Mandato di Luca del 2026-10-06. I quattro controlli sono fissati in
`doc/TASK_HISTORY/2026-10-06_mitosi-zero-dopo-la-cura.md`, committato **prima** in `b56141c`.)*

### ⛔ **OGNI CONTROLLO DICE ANCHE QUANTA MATERIA HA.** Un `PASSA` su zero passi confrontati
### non e' un `PASSA`: e' **un'assenza letta come un esito** *(`STANDARD 3`)*, ed e' il difetto
### che ha fatto stampare *«l'ipotesi NON e' refutata»* con tutti i valori `n/d`.

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Confronta i `json` di corse che
#   hanno GIA' dichiarato la propria configurazione INTERA.

USO:  python csv/_test_fork/_controlli_mzd.py
      python csv/_test_fork/_controlli_mzd.py --collaudo
"""
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
D_MZD = os.path.join(RADICE, "csv", "_test_fork", "_mitosi_zero_dove")
D_LUNGA = os.path.join(RADICE, "csv", "_test_fork", "_tors_w8_lunga")

# ### I CAMPI DI `C0`, dal mandato: *«`n`, archi, divisioni, Schwinger, quantili di `|tw|`»*.
CAMPI_C0 = ("n", "archi", "nati_tot", "schwinger_tot")

# ### ⛔ **I CONTATORI CHE ESISTONO SOLO PERCHE' I GANCI CI SONO**, e che quindi
#   ### **`C-letture` NON puo' pretendere** dal braccio senza ganci: pretenderli e' un
#   ### **FALSO FALLIMENTO**, e il 2026-10-06 `C-letture` e' fallito proprio cosi'
#   *(`1b5b651`: `3` differenze su `8841`, ### **tutte e tre qui dentro**)*.
#   ### ✔ **E SI LEGGONO DALLA CLASSE, NON SI ELENCANO A MANO:** cosi' un contatore
#   ### **futuro e' escluso da solo**, e nessuno deve ricordarsi di aggiungerlo.
def _esclusi():
    sys.path.insert(0, _QUI)
    import _mitosi_zero_dove as MZD
    e = set(MZD.Misura(0.01, 0.0).p)
    # ### ⛔ **E LA GUARDIA CHE RENDE L'ESCLUSIONE ONESTA:** se un giorno un contatore si
    #   chiamasse come un campo del simulatore, l'esclusione lo nasconderebbe. ### **Qui si
    #   FERMA invece di nascondere.**
    cattivi = e & set(CAMPI_C0)
    if cattivi:
        raise SystemExit("[FERMO] un contatore dei ganci si chiama come un campo del "
                         "simulatore: %s. L'esclusione lo NASCONDEREBBE." % sorted(cattivi))
    return e


ESCLUSI = _esclusi()


def leggi(p):
    if not os.path.isfile(p):
        return None
    return json.loads(io.open(p, encoding="utf-8").read())


def per_passo(d):
    return {int(x["passo"]): x for x in (d.get("passi_dati") or [])}


def trova(amp, senza_ganci=False):
    """Il `json` del braccio, trovato ### **dal campo `amp` DENTRO il file**, non dal nome.

    ### ⛔ **IL NOME NON SI INDOVINA:** lo strumento lo costruisce con
    `("%g" %% amp).replace(".", "_")`, e `"%g" %% 0.0` da' ### **`"0"`** -- quindi il braccio
    zero sta in ### **`amp0.json`**, non in `amp0_0.json`. ### **I miei due lettori cercavano
    `amp0_0.json`**, cioe' ### **un nome ASSUNTO invece che letto**, ed e' la stessa classe di
    `P1` che mi e' gia' costata il gancio sul ramo morto.

    ### ✔ **Leggere il campo `amp` DENTRO il file e' piu' forte di indovinare il nome:**
    vale anche se un giorno la regola del nome cambiasse.
    """
    if not os.path.isdir(D_MZD):
        return None
    for f in sorted(os.listdir(D_MZD)):
        if not (f.startswith("amp") and f.endswith(".json")):
            continue
        if ("_senza_ganci" in f) != bool(senza_ganci):
            continue
        try:
            d = json.loads(io.open(os.path.join(D_MZD, f),
                                   encoding="utf-8").read())
        except Exception:
            continue
        if d.get("amp") is not None and abs(float(d["amp"]) - float(amp)) < 1e-12:
            d["_file"] = f
            return d
    return None


def _cmp_q(a, b):
    """Due dizionari di quantili, confrontati ### **chiave per chiave e AL BIT.**"""
    a, b = (a or {}), (b or {})
    ch = sorted(set(a) | set(b))
    return [k for k in ch if a.get(k) != b.get(k)], len(ch)


def c0(mzd, lunga):
    """`C0`: il braccio `_AMP = 0.3` riproduce ### **ESATTAMENTE** la misura lunga.

    ### ⛔ **SU TUTTI I PASSI REGISTRATI DA ENTRAMBI**, che e' quello che il mandato chiede --
    non su un campione.
    """
    A, B = per_passo(mzd), per_passo(lunga)
    com = sorted(set(A) & set(B))
    diff, nq = [], 0
    for p in com:
        for c in CAMPI_C0:
            if A[p].get(c) != B[p].get(c):
                diff.append((p, c, A[p].get(c), B[p].get(c)))
        d, k = _cmp_q(A[p].get("q_tw"), B[p].get("q_tw"))
        nq += k
        for z in d:
            diff.append((p, "q_tw." + z, (A[p].get("q_tw") or {}).get(z),
                         (B[p].get("q_tw") or {}).get(z)))
    return {"passi_confrontati": len(com), "campi_per_passo": len(CAMPI_C0),
            "quantili_confrontati": nq, "differenze": diff[:40],
            "n_differenze": len(diff),
            "passa": bool(com) and not diff,
            "materia": len(com) * len(CAMPI_C0) + nq}


def c_letture(con, senza):
    """`C-letture`: la copia ### **CON** i ganci riproduce ### **AL BIT** quella ### **SENZA.**

    ### ⛔ **E' IL CONTROLLO CHE `C0` NON DA':** `C0` confronta col `json` della misura lunga,
    che era prodotto da uno strumento ### **che aveva GIA' due ganci.** Senza questo, due
    ganci nuovi potrebbero cambiare la misura ### **e `C0` passerebbe comunque.**
    """
    A, B = per_passo(con), per_passo(senza)
    com = sorted(set(A) & set(B))
    # ### i campi da confrontare sono quelli che il braccio SENZA ganci registra: i NUOVI non
    #   ci sono, e pretenderli sarebbe un falso fallimento.
    base = set()
    for p in com:
        base |= set(k for k, v in B[p].items() if not isinstance(v, dict))
    # ### il braccio SENZA ganci quei contatori li ha, ma a ZERO per costruzione: sono
    #   ### **inizializzati e mai scritti.** Confrontarli ### **misura la presenza dei
    #   ganci, non il loro effetto sul SISTEMA** -- ed e' l'unica cosa che `C-letture`
    #   ### **non deve** chiedere.
    esclusi_visti = sorted(base & ESCLUSI)
    base = sorted(base - {"passo"} - ESCLUSI)
    diff, nq = [], 0
    for p in com:
        for c in base:
            if A[p].get(c) != B[p].get(c):
                diff.append((p, c, A[p].get(c), B[p].get(c)))
        for qn in ("q_tw", "q_spinta"):
            d, k = _cmp_q(A[p].get(qn), B[p].get(qn))
            nq += k
            for z in d:
                diff.append((p, qn + "." + z, (A[p].get(qn) or {}).get(z),
                             (B[p].get(qn) or {}).get(z)))
    return {"passi_confrontati": len(com), "campi_per_passo": len(base),
            "campi": base, "quantili_confrontati": nq, "differenze": diff[:40],
            "n_differenze": len(diff), "passa": bool(com) and not diff,
            "materia": len(com) * len(base) + nq,
            # ### ⛔ **L'ESCLUSIONE SI DICHIARA NELL'ESITO:** un'esclusione taciuta e'
            #   un insabbiamento, e chi legge deve poter contare quanti campi sono rimasti
            #   fuori e come si chiamano.
            "esclusi": esclusi_visti, "n_esclusi": len(esclusi_visti)}


def c1(d):
    """`C1`: `divisioni + Schwinger == nati`, e `n` cresce ### **esattamente** di quanto
    dicono i nati."""
    A = per_passo(d)
    com = sorted(A)
    bad = []
    tot_div = sum((A[p].get("nati_div") or 0) for p in com)
    tot_sch = sum((A[p].get("nati_sch") or 0) for p in com)
    nati = (A[com[-1]].get("nati_tot") if com else None)
    sch_sim = (A[com[-1]].get("schwinger_tot") if com else None)
    if nati is not None and tot_div + tot_sch != nati:
        bad.append(("nati", tot_div + tot_sch, nati))
    if sch_sim is not None and tot_sch != sch_sim:
        bad.append(("schwinger", tot_sch, sch_sim))
    # ### e `n` cresce ESATTAMENTE di quanto dicono i nati, passo per passo
    for a, b in zip(com, com[1:]):
        dn = (A[b].get("n") or 0) - (A[a].get("n") or 0)
        dnat = (A[b].get("nati_tot") or 0) - (A[a].get("nati_tot") or 0)
        if dn != dnat:
            bad.append(("n al passo %d" % b, dn, dnat))
    return {"passi": len(com), "divisioni": tot_div, "schwinger": tot_sch,
            "nati_simulatore": nati, "schwinger_simulatore": sch_sim,
            "differenze": bad[:40], "n_differenze": len(bad),
            "passa": bool(com) and not bad, "materia": len(com)}


def c_fallisce(zero, lunga):
    """`C-fallisce`: il braccio `_AMP = 0` ### **DEVE DIFFERIRE**, e si riporta
    ### **il primo passo** in cui succede.

    ### ⛔ **SENZA QUESTO, `_AMP` POTREBBE ESSERE INERTE e la misura un falso-zero.**
    """
    A, B = per_passo(zero), per_passo(lunga)
    com = sorted(set(A) & set(B))
    primo, quale = None, None
    for p in com:
        for c in CAMPI_C0:
            if A[p].get(c) != B[p].get(c):
                primo, quale = p, (c, A[p].get(c), B[p].get(c))
                break
        if primo is None:
            d, _k = _cmp_q(A[p].get("q_tw"), B[p].get("q_tw"))
            if d:
                primo, quale = p, ("q_tw." + d[0],
                                   (A[p].get("q_tw") or {}).get(d[0]),
                                   (B[p].get("q_tw") or {}).get(d[0]))
        if primo is not None:
            break
    return {"passi_confrontati": len(com), "primo_passo_diverso": primo,
            "quale": quale, "passa": primo is not None, "materia": len(com)}


def riga(c="="):
    print(c * 104)


def _dillo(et, r, cosa):
    print()
    riga("-")
    print("%-14s %s" % (et, cosa))
    riga("-")
    if r is None:
        print("  ### IL JSON NON C'E'. Il controllo NON si puo' fare, e questo NON e' un")
        print("      PASSA: un'assenza non e' un esito (STANDARD 3).")
        return None
    print("  materia confrontata: %s valori" % r.get("materia"))
    for k in sorted(r):
        if k in ("differenze", "passa", "materia", "campi"):
            continue
        print("    %-24s %s" % (k, r[k]))
    if r.get("differenze"):
        print("  le prime differenze (passo, campo, questo, altro):")
        for z in r["differenze"][:10]:
            print("      %s" % (z,))
    if not r.get("materia"):
        print("  ### ⛔ MATERIA ZERO: il controllo non ha confrontato NIENTE, e un PASSA")
        print("      su zero confronti sarebbe un FALSO-ZERO.")
        return False
    print("  ### %s" % ("✔ PASSA" if r["passa"] else "⛔ FALLISCE"))
    return bool(r["passa"])


def main(argv):
    if "--collaudo" in argv[1:]:
        return collaudo()
    L = leggi(os.path.join(D_LUNGA, "lunga.json"))
    # ### ⛔ **I NOMI PRESERVATI VENGONO PRIMA:** le corse da `1000` passi
    #   ### **sovrascrivono** `amp0_3.json`, e `C0`/`C-letture` sono misurati a `150`.
    #   ### **Leggere il file sbagliato farebbe passare o fallire il controllo per la
    #   ragione sbagliata.**
    CON = (leggi(os.path.join(D_MZD, "c0_150.json"))
           or leggi(os.path.join(D_MZD, "amp0_3.json")))
    SENZA = (leggi(os.path.join(D_MZD, "cletture_150.json"))
             or leggi(os.path.join(D_MZD, "amp0_3_senza_ganci.json")))
    ZERO = trova(0.0)
    LUNGO_ACCESO = trova(0.3)
    riga()
    print("I CONTROLLI DEL MANDATO DEL `0.3` A ZERO")
    riga()
    for et, d in (("lunga.json (1000 passi)", L),
                  ("c0_150.json (C0, con ganci)", CON),
                  ("cletture_150.json (senza ganci)", SENZA),
                  ("il braccio ZERO -> %s" % (ZERO or {}).get("_file"), ZERO),
                  ("il braccio ACCESO -> %s"
                   % (LUNGO_ACCESO or {}).get("_file"), LUNGO_ACCESO)):
        print("  %-26s %s" % (et, ("%s passi, stato %s"
                                   % (d.get("passi_girati"), d.get("stato")))
                              if d else "### NON C'E'"))
    esiti = {}
    esiti["C0"] = _dillo("C0", c0(CON, L) if (CON and L) else None,
                         "`_AMP = 0.3` riproduce ESATTAMENTE la misura lunga")
    esiti["C-letture"] = _dillo("C-letture", c_letture(CON, SENZA)
                                if (CON and SENZA) else None,
                                "i ganci nuovi sono di SOLA LETTURA, al bit")
    esiti["C1"] = _dillo("C1", c1(CON) if CON else None,
                         "divisioni + Schwinger == nati, e `n` cresce di quanto dicono")
    esiti["C1 (zero)"] = _dillo("C1 (zero)", c1(ZERO) if ZERO else None,
                                "lo stesso, sul braccio `_AMP = 0`")
    _na = (LUNGO_ACCESO or {}).get("passi_girati")
    esiti["C1 (acceso %s)" % _na] = _dillo(
        "C1 (acceso %s)" % _na, c1(LUNGO_ACCESO) if LUNGO_ACCESO else None,
        "lo stesso, su `amp0_3.json` -- ### %s passi, LETTI DAL JSON e non assunti" % _na)
    esiti["C-fallisce"] = _dillo("C-fallisce", c_fallisce(ZERO, L)
                                 if (ZERO and L) else None,
                                 "`_AMP = 0` DEVE differire dalla misura lunga")
    print()
    riga()
    print("GLI ESITI")
    riga()
    for k in ("C0", "C-letture", "C1", "C1 (zero)",
              "C1 (acceso %s)" % _na, "C-fallisce"):
        v = esiti.get(k)
        print("  %-12s %s" % (k, "✔ PASSA" if v else
                              ("⛔ FALLISCE" if v is False else
                               "### NON FATTO (manca il json)")))
    riga()
    # ### ⛔ **UN `None` NON E' UN PASSA, e l'USCITA deve dirlo:** si torna `1` anche
    #   quando un controllo ### **non si e' potuto fare**, perche' *<<non fatto>>* e
    #   *<<passato>>* non sono la stessa cosa.
    #   ### ⚠ **E LA PRIMA VERSIONE TORNAVA `0` guardando solo tre controlli su cinque**,
    #   cioe' ### **diceva <<tutto a posto>> con due controlli mancanti** -- esattamente cio'
    #   che la riga sopra prometteva di non fare. ### **Trovato rileggendo l'uscita contro il
    #   messaggio che stavo scrivendo.**
    _mancanti = [k for k, v in esiti.items() if v is None]
    _falliti = [k for k, v in esiti.items() if v is False]
    if _mancanti:
        print("  ### ⚠ NON FATTI: %s -- e questo NON e' un PASSA." % ", ".join(_mancanti))
    if _falliti:
        print("  ### ⛔ FALLITI: %s" % ", ".join(_falliti))
    return 0 if not (_mancanti or _falliti) else 1


# =============================================================== IL COLLAUDO
def _finto(passi=3, n0=100, nati=None, q=0.5, extra=None):
    out = []
    nt = 0
    for k in range(1, passi + 1):
        d = (nati or {}).get(k, 0)
        nt += d
        x = {"passo": k, "n": n0 + nt, "archi": 500 + nt, "nati_tot": nt,
             "schwinger_tot": 0, "nati_div": d, "nati_sch": 0,
             "q_tw": {"q050": q, "q095": q * 2}, "q_spinta": {"q050": 0.1}}
        if extra:
            x.update(extra)
        out.append(x)
    return {"passi": passi, "passi_girati": passi, "stato": "fatto", "passi_dati": out}


def collaudo():
    esiti = []

    def prova(nome, ok, dett=""):
        esiti.append((nome, bool(ok), dett))
        print("  %-7s %-74s %s" % ("OK" if ok else "FALLITA", nome, dett))

    riga()
    print("IL COLLAUDO DI _controlli_mzd.py -- su `json` SINTETICI")
    riga()
    A = _finto()
    prova("C0: ### due json IDENTICI passano, e la materia NON e' zero",
          c0(A, _finto())["passa"] and c0(A, _finto())["materia"] > 0,
          "materia %d" % c0(A, _finto())["materia"])
    B = _finto(q=0.5000000001)
    r = c0(A, B)
    prova("C0: ### DEVE FALLIRE -- una differenza nel DECIMO decimale di `q_tw` lo prende",
          not r["passa"] and r["n_differenze"] > 0, "%d differenze" % r["n_differenze"])
    r = c0(A, _finto(nati={2: 1}))
    prova("C0: ### DEVE FALLIRE -- un nato in piu' lo prende", not r["passa"],
          "%d differenze" % r["n_differenze"])
    r = c0(_finto(passi=3), {"passi_dati": []})
    prova("C0: ### DEVE FALLIRE -- senza passi in comune NON passa (materia zero)",
          not r["passa"] and r["materia"] == 0, "materia %d" % r["materia"])
    # ### C-letture
    r = c_letture(_finto(extra={"cambi_chi_tors": 7}), _finto())
    prova("C-letture: ### i campi NUOVI non si pretendono dal braccio senza ganci",
          r["passa"] and "cambi_chi_tors" not in r["campi"], "%s" % r["campi"])
    prova("C-letture: ### e la materia non e' zero", r["materia"] > 0,
          "materia %d" % r["materia"])
    r = c_letture(_finto(q=0.5000000001, extra={"cambi_chi_tors": 7}), _finto())
    prova("C-letture: ### DEVE FALLIRE -- se i ganci cambiano `q_tw`, lo prende",
          not r["passa"], "%d differenze" % r["n_differenze"])
    r = c_letture(_finto(extra={"n": 999}), _finto())
    prova("C-letture: ### DEVE FALLIRE -- se i ganci cambiano `n`, lo prende",
          not r["passa"], "%d differenze" % r["n_differenze"])
    prova("C-letture: ### l'esclusione e' DERIVATA dalla classe, non elencata a mano",
          "cambi_chi_tors" in ESCLUSI and "cambi_geom" in ESCLUSI
          and "spinta_pi_esatto" in ESCLUSI, "%d contatori" % len(ESCLUSI))
    prova("C-letture: ### e NON contiene NESSUN campo del simulatore (la guardia)",
          not (ESCLUSI & set(CAMPI_C0)), "%s" % sorted(ESCLUSI & set(CAMPI_C0)))
    _b = _finto(extra={"cambi_chi_tors": 0, "cambi_geom": 0})
    r = c_letture(_finto(extra={"cambi_chi_tors": 6419, "cambi_geom": 6419}), _b)
    # ### l'attesa si DERIVA dal json sintetico, non si scrive a mano: la prima versione
    #   pretendeva `2` e il json sintetico ne ha ### **4** (`nati_div` e `nati_sch` sono
    #   anch'essi prodotti dai ganci). ### **Il controllo era giusto e la mia attesa no.**
    _att = sorted(set(_b["passi_dati"][0]) & ESCLUSI)
    prova("C-letture: ### il caso VERO di 1b5b651 ora PASSA, e dichiara gli esclusi",
          r["passa"] and r["esclusi"] == _att,
          "esclusi %s, attesi %s" % (r["esclusi"], _att))
    prova("C-letture: ### e i conti DEL SIMULATORE restano confrontati, non esclusi",
          all(c not in ESCLUSI for c in ("nati_tot", "schwinger_tot", "n", "archi")))
    r = c_letture(_finto(extra={"cambi_chi_tors": 6419, "n": 999}),
                  _finto(extra={"cambi_chi_tors": 0}))
    prova("C-letture: ### DEVE FALLIRE -- un campo del SIMULATORE diverso lo prende ANCORA",
          not r["passa"] and any(z[1] == "n" for z in r["differenze"]),
          "%d differenze" % r["n_differenze"])
    r = c_letture(_finto(extra={"cambi_chi_tors": 6419, "q_tw": {"q050": 0.5000000001}}),
                  _finto(extra={"cambi_chi_tors": 0}))
    prova("C-letture: ### DEVE FALLIRE -- e un quantile diverso nel decimo decimale pure",
          not r["passa"], "%d differenze" % r["n_differenze"])
    # ### C1
    r = c1(_finto(nati={2: 3}))
    prova("C1: ### con i conti coerenti passa", r["passa"],
          "div %s nati %s" % (r["divisioni"], r["nati_simulatore"]))
    bad = _finto(nati={2: 3})
    bad["passi_dati"][1]["nati_div"] = 2
    r = c1(bad)
    prova("C1: ### DEVE FALLIRE -- se divisioni + Schwinger != nati, lo prende",
          not r["passa"], "%s" % r["differenze"][:2])
    bad = _finto(nati={2: 3})
    bad["passi_dati"][2]["n"] += 5
    r = c1(bad)
    prova("C1: ### DEVE FALLIRE -- se `n` cresce piu' dei nati, lo prende",
          not r["passa"], "%s" % r["differenze"][:2])
    # ### C-fallisce
    r = c_fallisce(_finto(nati={2: 1}), _finto())
    prova("C-fallisce: ### trova il PRIMO passo diverso, e lo dice",
          r["passa"] and r["primo_passo_diverso"] == 2,
          "passo %s, %s" % (r["primo_passo_diverso"], r["quale"]))
    r = c_fallisce(_finto(), _finto())
    prova("C-fallisce: ### DEVE FALLIRE -- se i due bracci sono IDENTICI, `_AMP` e' INERTE",
          not r["passa"] and r["primo_passo_diverso"] is None)
    # ### ⛔ **IL NOME ERA ASSUNTO, E LO STRUMENTO SCRIVE `amp0.json`:** `"%g" % 0.0`
    #   da' `"0"`, non `"0_0"`. ### **Ora si legge il campo `amp` DENTRO il file.**
    import tempfile as _tf
    global D_MZD
    _vero, _tmp = D_MZD, _tf.mkdtemp()
    try:
        D_MZD = _tmp
        io.open(os.path.join(_tmp, "amp0.json"), "w", encoding="utf-8").write(
            json.dumps({"amp": 0.0, "passi_dati": [], "stato": "fatto"}))
        io.open(os.path.join(_tmp, "amp0_3.json"), "w", encoding="utf-8").write(
            json.dumps({"amp": 0.3, "passi_dati": [], "stato": "fatto"}))
        io.open(os.path.join(_tmp, "amp0_3_senza_ganci.json"), "w",
                encoding="utf-8").write(json.dumps({"amp": 0.3, "passi_dati": []}))
        prova("trova: ### il braccio ZERO si trova in `amp0.json`, non in `amp0_0.json`",
              (trova(0.0) or {}).get("_file") == "amp0.json",
              "%s" % (trova(0.0) or {}).get("_file"))
        prova("trova: ### e il braccio acceso NON prende quello `_senza_ganci`",
              (trova(0.3) or {}).get("_file") == "amp0_3.json",
              "%s" % (trova(0.3) or {}).get("_file"))
        prova("trova: ### e col flag prende PROPRIO quello `_senza_ganci`",
              (trova(0.3, senza_ganci=True) or {}).get("_file")
              == "amp0_3_senza_ganci.json")
        prova("trova: ### DEVE TACERE -- un'ampiezza che non c'e' torna `None`",
              trova(0.7) is None)
    finally:
        D_MZD = _vero
    riga()
    ko = [n for n, o, _d in esiti if not o]
    print("COLLAUDO: %d su %d" % (len(esiti) - len(ko), len(esiti)))
    if ko:
        print("### FALLITI:")
        for n in ko:
            print("    - " + n)
    riga()
    return 1 if ko else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
