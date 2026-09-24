# -*- coding: utf-8 -*-
"""IL REFERTO DI CONFIGURAZIONE DI UN RUN -- `CONFIGURAZIONE.txt` e `.json`.

Decisione di Luca, 2026-09-24. **Nessun run parte senza.**

PERCHE' ESISTE, e sono due casi reali dello STESSO giorno:
  * **`S10`** e' nato deducendo dal sorgente quale ramo di `ritmo()` girasse. La deduzione
    era **sbagliata** (il contatore stava PRIMA del controllo del flag), e per accorgersene
    e' servito rileggere il sorgente invece del referto -- **che non esisteva**.
  * **`SPINORE_CORRETTO` ha default `False` nel sorgente e vale `True` in ogni run del
    fork**, perche' il driver cabla `--spinore-corretto` in `sys.argv` (`:187`). Chi legge il
    sorgente conclude il contrario di chi legge il run.

**L'ELENCO DEI FLAG NON E' A MANO: si ricava dall'AST** -- gli assegnamenti a livello di
MODULO con nome MAIUSCOLO. Una lista scritta a mano invecchia in silenzio, e nel driver ce
n'era gia' una di 24 nomi su 123 (MISURATO dal collaudo, non stimato).

**SI LEGGE DAL MODULO, DOPO `_applica_flag`.** Il valore che conta e' quello che GIRA, non
quello scritto nel sorgente: sono due cose diverse, ed e' l'intero motivo di questo file.

!! E L'ORDINE E' UN PRESIDIO STRUTTURALE, non una raccomandazione: `collaudo()` verifica
  DALL'AST che nel driver la chiamata a `scrivi()` venga DOPO quella a `_applica_flag`.
  Letta prima, la tabella mostrerebbe i DEFAULT -- cioe' esattamente la bugia che questo
  file esiste per impedire.

SOLA LETTURA sulla fisica. ASCII PURO.
"""
import ast
import datetime
import hashlib
import io
import json
import os
import subprocess
import sys

NOME_TXT = "CONFIGURAZIONE.txt"
NOME_JSON = "CONFIGURAZIONE.json"


# ------------------------------------------------------------------ i NOMI, dall'AST
def _corpo_modulo(albero):
    """Le istruzioni a livello di MODULO, entrando negli `if`/`try` di modulo.

    Serve perche' alcuni flag sono assegnati dentro un `if` di modulo, e fermarsi a
    `albero.body` li perderebbe **in silenzio** -- che e' il difetto di una lista a mano.
    """
    fuori = []
    resto = list(albero.body)
    while resto:
        n = resto.pop(0)
        fuori.append(n)
        if isinstance(n, (ast.If, ast.Try)):
            resto = list(n.body) + list(getattr(n, "orelse", [])) \
                + list(getattr(n, "finalbody", [])) + resto
            for h in getattr(n, "handlers", []):
                resto = list(h.body) + resto
    return fuori


def _letterale(nodo):
    """Il valore se e' un letterale semplice, altrimenti `None` (dichiarato, non inventato)."""
    try:
        return ast.literal_eval(nodo)
    except Exception:
        return None


def nomi_flag(sorgente):
    """{NOME: default_letterale_o_None} dagli assegnamenti di MODULO con nome MAIUSCOLO.

    `isupper()` accetta `MAX_NODI` e `P_LAM` (le cifre e gli underscore non sono cased).
    Si escludono i nomi che cominciano con `_`: sono interni, non configurazione.
    """
    albero = ast.parse(io.open(sorgente, encoding="utf-8").read())
    out = {}
    for n in _corpo_modulo(albero):
        if isinstance(n, ast.Assign):
            bersagli = n.targets
            valore = n.value
        elif isinstance(n, ast.AnnAssign):
            bersagli = [n.target]
            valore = n.value
        else:
            continue
        for b in bersagli:
            if isinstance(b, ast.Name) and b.id.isupper() and not b.id.startswith("_"):
                out.setdefault(b.id, _letterale(valore) if valore is not None else None)
    return out


# ------------------------------------------------------------------ i TIMBRI
def sha1_byte(percorso):
    """sha1 dei BYTE GREZZI, **non** `git hash-object` (trappola CRLF, `C18`)."""
    try:
        return hashlib.sha1(io.open(percorso, "rb").read()).hexdigest()
    except Exception:
        return None


def _git(*argomenti):
    try:
        return subprocess.check_output(("git",) + argomenti,
                                       stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return None


# ------------------------------------------------------------------ LA SCRITTURA
def raccogli(modulo, sorgente, argv_interno, argv_esterno=None, driver=None, seme=None):
    """Lo stato EFFETTIVO, letto dal MODULO. Da chiamare DOPO `_applica_flag`."""
    difetti = nomi_flag(sorgente)
    vivi = {}
    for nome in sorted(difetti):
        v = getattr(modulo, nome, "__ASSENTE__")
        if v != "__ASSENTE__" and not isinstance(v, (bool, int, float, str, type(None))):
            v = "<%s>" % type(v).__name__      # un dict o un array non si serializza qui
        vivi[nome] = v
    return {
        "quando": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "simulatore": {"percorso": os.path.relpath(sorgente),
                       "sha1_byte": sha1_byte(sorgente)},
        "driver": ({"percorso": os.path.relpath(driver), "sha1_byte": sha1_byte(driver)}
                   if driver else None),
        "git": {"head": _git("rev-parse", "HEAD"),
                "branch": _git("rev-parse", "--abbrev-ref", "HEAD"),
                "pulito": (_git("status", "--porcelain") == "")},
        "seme": seme,
        "argv_interno": list(argv_interno) if argv_interno else None,
        "argv_esterno": list(argv_esterno) if argv_esterno else None,
        "default_dal_sorgente": {k: difetti[k] for k in sorted(difetti)},
        "effettivo_dal_modulo": vivi,
    }


def _tabella(dati):
    d, v = dati["default_dal_sorgente"], dati["effettivo_dal_modulo"]
    # !! SI CONFRONTA SOLO FRA SCALARI, e non e' pedanteria: un default `[]` contro un
    #   effettivo stringificato `<list>` comparirebbe fra i CAMBIATI SEMPRE. `BOTTONI` lo
    #   faceva, ed era un FALSO POSITIVO -- trovato dal primo giro di prova, non da un test.
    #   Un referto che segnala trenta cambi fra cui uno falso insegna a non fidarsi del referto.
    _SCAL = (bool, int, float, str)

    def _confrontabile(x):
        return isinstance(x, _SCAL) or x is None

    cambiati = [k for k in sorted(v)
                if k in d and d[k] is not None
                and _confrontabile(d[k]) and _confrontabile(v[k]) and v[k] != d[k]]
    non_confrontabili = [k for k in sorted(v)
                         if k in d and not (_confrontabile(d.get(k)) and _confrontabile(v[k]))]
    r = []
    r.append("# REFERTO DI CONFIGURAZIONE DEL RUN")
    r.append("#")
    r.append("# Lo stato EFFETTIVO dei flag, letto DAL MODULO dopo `_applica_flag`.")
    r.append("# I nomi vengono dall'AST (assegnamenti di MODULO, nome MAIUSCOLO), non da una")
    r.append("# lista a mano: una lista a mano invecchia in silenzio.")
    r.append("#")
    r.append("quando           %s" % dati["quando"])
    r.append("simulatore       %s  sha1-BYTE %s"
             % (dati["simulatore"]["percorso"], dati["simulatore"]["sha1_byte"]))
    if dati["driver"]:
        r.append("driver           %s  sha1-BYTE %s"
                 % (dati["driver"]["percorso"], dati["driver"]["sha1_byte"]))
    g = dati["git"]
    r.append("git              HEAD %s  branch %s  albero %s"
             % (g["head"], g["branch"], "PULITO" if g["pulito"] else "*** SPORCO ***"))
    r.append("seme             %s" % dati["seme"])
    r.append("")
    r.append("ARGV VERBATIM -- quello passato al SIMULATORE:")
    r.append("  %s" % (" ".join(dati["argv_interno"]) if dati["argv_interno"] else "(assente)"))
    if dati["argv_esterno"]:
        r.append("ARGV VERBATIM -- quello con cui e' stato invocato il processo:")
        r.append("  %s" % " ".join(dati["argv_esterno"]))
    r.append("")
    r.append("=" * 96)
    r.append("I FLAG CHE L'ARGV HA CAMBIATO rispetto al default del sorgente: %d"
             % len(cambiati))
    r.append("=" * 96)
    r.append("%-30s %-18s %-18s" % ("nome", "default sorgente", "EFFETTIVO"))
    r.append("-" * 96)
    for k in cambiati:
        r.append("%-30s %-18s %-18s" % (k, d[k], v[k]))
    if not cambiati:
        r.append("(nessuno -- e se il run usa un driver con dei flag, questo e' un ALLARME)")
    r.append("")
    r.append("NON CONFRONTABILI (default non scalare: lista, dict, array): %d -- %s"
             % (len(non_confrontabili), ", ".join(non_confrontabili) or "nessuno"))
    r.append("  Per questi il referto riporta il valore EFFETTIVO nella tabella completa, ma NON")
    r.append("  dice se e' cambiato: dirlo richiederebbe un confronto che non ho fatto.")
    r.append("")
    r.append("=" * 96)
    r.append("TUTTI I FLAG E LE COSTANTI DI MODULO: %d" % len(v))
    r.append("=" * 96)
    r.append("%-30s %-18s %-18s %s" % ("nome", "default sorgente", "EFFETTIVO", ""))
    r.append("-" * 96)
    for k in sorted(v):
        marchio = "  <-- CAMBIATO" if k in cambiati else ""
        r.append("%-30s %-18s %-18s%s"
                 % (k, "" if d.get(k) is None else d[k], v[k], marchio))
    r.append("")
    return "\n".join(r) + "\n"


def scrivi(dest, modulo, sorgente, argv_interno, argv_esterno=None, driver=None, seme=None):
    """Scrive i due file. **SOLLEVA** se non riesce: il chiamante deve RIFIUTARE DI PARTIRE."""
    dati = raccogli(modulo, sorgente, argv_interno, argv_esterno, driver, seme)
    p_txt = os.path.join(dest, NOME_TXT)
    p_json = os.path.join(dest, NOME_JSON)
    io.open(p_txt, "w", encoding="utf-8", newline="\n").write(_tabella(dati))
    io.open(p_json, "w", encoding="utf-8", newline="\n").write(
        json.dumps(dati, indent=1, sort_keys=True, default=str) + "\n")
    # SI RILEGGE: un file scritto e non rileggibile non e' un referto.
    assert io.open(p_txt, encoding="utf-8").read().strip(), "CONFIGURAZIONE.txt e' VUOTO"
    json.loads(io.open(p_json, encoding="utf-8").read())
    return p_txt, p_json


# ------------------------------------------------------------------ IL COLLAUDO (`P1-sexies`)
def ordine_nel_driver(percorso_driver):
    """DALL'AST: la riga di `scrivi(...)` viene DOPO quella di `_applica_flag(...)`?

    E' il presidio STRUTTURALE: non verifica un valore, verifica l'ORDINE -- che e' cio'
    da cui dipende la verita' di tutta la tabella.
    """
    albero = ast.parse(io.open(percorso_driver, encoding="utf-8").read())
    r_flag, r_scrivi = [], []
    for n in ast.walk(albero):
        if not isinstance(n, ast.Call):
            continue
        f = n.func
        nome = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", None)
        if nome == "_applica_flag":
            r_flag.append(n.lineno)
        elif nome == "scrivi":
            r_scrivi.append(n.lineno)
    return r_flag, r_scrivi


def collaudo(W, driver=None):
    """Casi a RISPOSTA NOTA, col caso che DEVE fallire."""
    W("COLLAUDO DEL REFERTO DI CONFIGURAZIONE (`P1-sexies`)\n")
    W("-" * 96 + "\n")
    e = []
    qui = os.path.dirname(os.path.abspath(__file__))
    radice = os.path.abspath(os.path.join(qui, ".."))
    sorgente = os.path.join(radice, "soliton_simulator.py")

    # K1 -- i nomi dall'AST: ci sono, e sono MOLTI PIU' della lista a mano del driver
    nomi = nomi_flag(sorgente)
    ok1 = len(nomi) > 100 and "SPINORE_CORRETTO" in nomi and "FASE_2PI" in nomi
    W("K1 i nomi dall'AST: %d, con SPINORE_CORRETTO e FASE_2PI -> %s\n"
      % (len(nomi), "OK" if ok1 else "*** NO ***"))
    e.append(ok1)

    # K2 -- il default LETTO DALL'AST di un flag che il driver accende
    ok2 = (nomi.get("SPINORE_CORRETTO") is False)
    W("K2 default di SPINORE_CORRETTO dal sorgente = %r (atteso False) -> %s\n"
      % (nomi.get("SPINORE_CORRETTO"), "OK" if ok2 else "*** NO ***"))
    e.append(ok2)

    # K3 -- IL CASO CHE DEVE FALLIRE: l'argv lo ACCENDE, quindi leggere il DEFAULT
    #       invece del modulo darebbe la risposta SBAGLIATA.
    sys.path.insert(0, radice)
    vecchio_argv = list(sys.argv)
    try:
        import soliton_simulator as S
        prima = getattr(S, "SPINORE_CORRETTO", None)
        sys.argv = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "2",
                    "--spinore-corretto", "--campo-spinoriale", "--spinore-vivo"]
        a = S._cli()
        S._applica_flag(a)
        dopo = getattr(S, "SPINORE_CORRETTO", None)
    finally:
        sys.argv = vecchio_argv
    ok3 = (prima is False and dopo is True)
    W("K3 IL CASO CHE DEVE FALLIRE: PRIMA di `_applica_flag` = %r, DOPO = %r -> %s\n"
      % (prima, dopo, "OK: letto PRIMA darebbe il DEFAULT, cioe' la risposta sbagliata"
         if ok3 else "*** il flag non cambia: il collaudo non prova niente ***"))
    e.append(ok3)

    # K4 -- e la tabella costruita DOPO deve mostrarlo fra i CAMBIATI
    dati = raccogli(S, sorgente, sys.argv, seme=42)
    testo = _tabella(dati)
    ok4 = ("SPINORE_CORRETTO" in testo
           and dati["effettivo_dal_modulo"]["SPINORE_CORRETTO"] is True)
    W("K4 la tabella costruita DOPO mostra SPINORE_CORRETTO = %r -> %s\n"
      % (dati["effettivo_dal_modulo"]["SPINORE_CORRETTO"], "OK" if ok4 else "*** NO ***"))
    e.append(ok4)

    # K5 -- SECONDO CASO CHE DEVE FALLIRE: una `dest` inesistente deve SOLLEVARE,
    #       perche' il chiamante deve poter rifiutare di partire.
    try:
        scrivi(os.path.join(radice, "_cartella_che_non_esiste_mai"), S, sorgente, sys.argv)
        ok5 = False
    except Exception:
        ok5 = True
    W("K5 SECONDO CASO CHE DEVE FALLIRE: `dest` inesistente -> SOLLEVA -> %s\n"
      % ("OK: il driver puo' rifiutare di partire" if ok5 else "*** non solleva ***"))
    e.append(ok5)

    # K6 -- L'ORDINE NEL DRIVER, dall'AST
    if driver:
        r_flag, r_scrivi = ordine_nel_driver(driver)
        ok6 = bool(r_flag) and bool(r_scrivi) and min(r_scrivi) > max(r_flag)
        W("K6 ORDINE nel driver (AST): `_applica_flag` alle righe %s, `scrivi` alle %s -> %s\n"
          % (r_flag, r_scrivi,
             "OK: il referto e' scritto DOPO" if ok6 else "*** SCRITTO PRIMA O ASSENTE ***"))
        e.append(ok6)

    ok = all(e)
    W("-" * 96 + "\n  -> %s\n\n" % ("i criteri PASSANO" if ok else "*** NON PASSANO ***"))
    return ok


if __name__ == "__main__":
    _qui = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, _qui)
    import _presidio
    _presidio.avvia(__file__)
    _drv = os.path.join(_qui, "_test_fork", "_scena_video.py")
    sys.exit(0 if collaudo(sys.stdout.write, _drv if os.path.exists(_drv) else None) else 1)
