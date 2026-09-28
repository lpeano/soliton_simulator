# -*- coding: utf-8 -*-
"""**SIGILLO di `MAX-NODI-FERMA`: la guardia di memoria FERMA il run, e a default non cambia nulla.**

**Quattro bracci, e le letture erano fissate nel task history `1b90fef` PRIMA di vedere i numeri:**

| | braccio | passa se |
|---|---|---|
| **A** | **byte-identita'** col driver, 3 passi, seme 11 | ### **23 grandezze su 23, 0 diverse** |
| **B** | ### **IL CASO CHE DEVE FALLIRE**: `--maxnodi` basso | solleva **`LimiteNodiSuperato`**, il messaggio **nomina `MAX_NODI`**, e il processo **esce diverso da 0** |
| **C** | **CONTROLLO POSITIVO**: lo stesso comando sul blob **VECCHIO** | il vecchio **NON si ferma**: esce **0** e produce uno stato |
| **D** | **lo SFORO dentro il passo** | ### **si RIPORTA, non e' un criterio** |

### **`B` e' il braccio che conta** (`P1-sexies`): **un presidio che non fallisce mai non si
distingue da uno assente** (`A9`). E ### **`C` e' quello che impedisce di aver inventato la cura:**
se anche il blob vecchio si fermasse, non ci sarebbe nulla da curare.

**COMANDO:**
```
python csv/_seal_fork/_sig_max_nodi.py
```
**USCITA:** `0` se tutti i bracci passano, `1` altrimenti.

*(Braccio interno, usato dai bracci `B` e `C` in sottoprocesso -- e in sottoprocesso perche' un
`raise` va visto **come esce il processo**, non come un'eccezione catturata nello stesso
interprete:*
```
python csv/_seal_fork/_sig_max_nodi.py --corri=<MAX_NODI> [--sim=<percorso>] [--passi=N]
```
*Esce `0` se il run **arriva in fondo**, `3` se `LimiteNodiSuperato` lo **ferma**.)*
"""
import hashlib
import io
import json
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)
import _cli_flag  # noqa: E402

SIM = os.path.join(RADICE, "soliton_simulator.py")
BLOB = hashlib.sha1(io.open(SIM, "rb").read()).hexdigest()
FUORI = os.path.join(_QUI, "_sig_max_nodi")
PRIMA = os.path.join(FUORI, "PRIMA.npz")
DOPO = os.path.join(FUORI, "DOPO.npz")
VECCHIO = os.path.join(FUORI, "_sim_prima_della_cura.py")
PROVA = os.path.join(RADICE, "csv", "_test_fork", "_hashseed_prova.py")
# IL NOME CHE LA CURA INTRODUCE: da qui `sim_prima_del_flag` RISALE al commit che lo ha
# introdotto e prende il PADRE. NESSUN COMMIT PINNATO A MANO (`H-P8`).
ANCORA_CURA = "LimiteNodiSuperato"


def _riga(x):
    return x if isinstance(x, str) else x.decode("utf-8", "replace")


# ============================================================================================
# IL BRACCIO INTERNO: UN run, e dice come esce
# ============================================================================================
def sintetico(sim):
    """**Il controllo dello SCHEDULATORE, esercitato con un `net` SINTETICO.**

    ### **Perche' sintetico e non una scena vera, ed e' una MISURA che l'ha imposto:** il
    controllo dello schedulatore scatta solo se `n` **cresce dentro il passo**, cioe' se c'e'
    una **nascita** -- e sulla scena dei sigilli `(ii)(a)` (seme 11, `n = 2107`) sono
    **misurati 40 passi con ZERO nascite**. E la strada <<una scena piu' grande del tetto>> e'
    **chiusa per costruzione**, perche' ora `semina` ferma prima. *(Il primo giro di questo
    sigillo e' FALLITO proprio su questo braccio: era il braccio a essere mal progettato, non
    la cura.)*

    **Basta un oggetto col solo `.n`**, perche' il controllo sta **prima** della validazione e
    **prima di toccare `net`** -- ed e' esattamente cio' che il braccio dimostra.
    **E il controllo positivo e' netto:**

    | blob | che cosa fa |
    |---|---|
    | **NUOVO** | solleva **`LimiteNodiSuperato`** -- e non tocca `net` |
    | **VECCHIO** | **arriva a toccare `net`** e muore di **`AttributeError`** |

    Uscita: `3` = `LimiteNodiSuperato` *(il nuovo)* · `4` = un altro errore *(il vecchio)* ·
    `0` = nessun errore *(non deve capitare a nessuno dei due)*.
    """
    S, a = _cli_flag.carica_dal_cli(list(_cli_flag.argv_del_driver(
        extra=["--seme=11"], dest=os.path.join(FUORI, "_scarto_cli"))[1]),
        nome="sim_sintetico", sim=sim)
    ECC = getattr(S, "LimiteNodiSuperato", None)
    print("[sintetico] simulatore = %s" % os.path.basename(sim))
    print("[sintetico] `LimiteNodiSuperato` %s" % ("ESISTE" if ECC else "NON ESISTE"))

    class FintoNet(object):
        """SOLO `.n`: se il controllo tocca altro, questo oggetto lo FA VEDERE."""
        n = S.MAX_NODI + 1

    print("[sintetico] MAX_NODI = %d, il finto `net` ha n = %d" % (S.MAX_NODI, FintoNet.n))
    try:
        S.esegui_passo(FintoNet())
    except Exception as e:
        nome = type(e).__name__
        print("[sintetico] SOLLEVATA %s" % nome)
        print(_riga(str(e))[:900])
        if ECC is not None and isinstance(e, ECC):
            return 3
        return 4
    print("[sintetico] NESSUN ERRORE: il passo e' girato su un `net` che ha solo `.n`")
    return 0


def corri(max_nodi, sim, passi):
    # ⚠ `extra` di `argv_del_driver` va nella `sys.argv` DEL DRIVER, non del simulatore: il
    #   driver legge dei POSIZIONALI, e un `--maxnodi=` li' finisce dentro `int(...)` e muore.
    #   Quindi `--maxnodi` si aggiunge all'argv CHE IL DRIVER HA COSTRUITO PER IL SIMULATORE.
    S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                         dest=os.path.join(FUORI, "_scarto_cli"))
    argv = list(argv) + ["--maxnodi=%d" % max_nodi]
    print("[corri] maxnodi = %d   passi = %d" % (max_nodi, passi))
    print("[corri] simulatore = %s" % os.path.basename(sim))
    # l'eccezione esiste SOLO dopo la cura: sul blob vecchio non c'e', e allora non si cattura
    # niente -- che e' esattamente il punto del controllo positivo.
    try:
        S, a = _cli_flag.carica_dal_cli(list(argv), nome="sim_maxnodi", sim=sim)
    except Exception as e:
        if type(e).__name__ == "LimiteNodiSuperato":
            print("[corri] FERMATO durante la CONFIGURAZIONE (la semina del vuoto):")
            print(_riga(str(e)))
            return 3
        raise
    ECC = getattr(S, "LimiteNodiSuperato", None)
    print("[corri] l'eccezione `LimiteNodiSuperato` %s in questo simulatore"
          % ("ESISTE" if ECC else "NON ESISTE"))
    S._NMASSE_VIDEO["n"] = 2
    S._NMASSE_VIDEO["sep"] = 3.0
    S._NMASSE_VIDEO["size"] = None
    try:
        S.avvia_test("MASSE-COERENTI")()
    except Exception as e:
        if ECC is not None and isinstance(e, ECC):
            print("[corri] FERMATO durante la SCENA:")
            print(_riga(str(e)))
            return 3
        raise
    net = S.net
    print("[corri] scena: n = %d, m = %d   MAX_NODI = %d" % (net.n, len(net.i), S.MAX_NODI))
    for k in range(passi):
        try:
            S.esegui_passo(net)
        except Exception as e:
            if ECC is not None and isinstance(e, ECC):
                print("[corri] FERMATO al passo %d, con n = %d:" % (k + 1, net.n))
                print(_riga(str(e)))
                print("[corri] SFORO = %d nodi oltre MAX_NODI" % max(0, net.n - S.MAX_NODI))
                return 3
            raise
        print("[corri] passo %d fatto, n = %d" % (k + 1, net.n))
    print("[corri] ARRIVATO IN FONDO senza fermarsi: n = %d" % net.n)
    return 0


# ============================================================================================
# IL SIGILLO
# ============================================================================================
def _sotto(max_nodi=None, sim=None, passi=3, sint=False):
    """Lancia un braccio interno IN SOTTOPROCESSO e restituisce `(codice, testo)`."""
    cmd = [sys.executable, os.path.abspath(__file__)]
    cmd.append("--sintetico" if sint else "--corri=%d" % max_nodi)
    cmd.append("--passi=%d" % passi)
    if sim:
        cmd.append("--sim=" + sim)
    p = subprocess.run(cmd, capture_output=True, cwd=RADICE)
    return p.returncode, _riga(p.stdout) + _riga(p.stderr)


def _stampa(testo):
    for r in testo.split(chr(10)):
        if r.strip():
            print("      " + r.rstrip()[:104])


def principale():
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    esiti, REF = {}, {}
    print("simulatore blob sha1-BYTE %s" % BLOB[:8])
    print("")

    # ---- il blob VECCHIO: **NON SI PINNA A MANO** (`H-P8`) -----------------------------------
    #   `sim_prima_del_flag` TROVA il commit che introduce il nome (`git log -S`, la voce piu'
    #   vecchia), ne prende il PADRE, e ASSERISCE che il file estratto NON contenga quel nome:
    #   se l'ancora fosse sbagliata **si ferma invece di misurare niente** (`A9`).
    #   *(La prima stesura di questo sigillo pinnava `95249c5~1` a mano, e `H-P8` l'ha
    #   RIFIUTATA -- giustamente: un'ancora scritta a mano non si accorge di essere sbagliata.)*
    introduce = _cli_flag.sim_prima_del_flag(ANCORA_CURA, VECCHIO)
    B_VEC = hashlib.sha1(io.open(VECCHIO, "rb").read()).hexdigest()
    print("il nome `%s` e' introdotto da %s; il suo PADRE e' il simulatore di prima"
          % (ANCORA_CURA, introduce[:8]))
    print("blob VECCHIO = %s, scritto in %s" % (B_VEC[:8], os.path.basename(VECCHIO)))
    if B_VEC == BLOB:
        raise SystemExit("[ANCORA] il blob vecchio e quello nuovo COINCIDONO: non c'e' niente "
                         "da confrontare, e il sigillo non misurerebbe nulla.")
    print("")

    # ================= BRACCIO A: byte-identita' ===========================================
    print("=" * 92)
    print("BRACCIO A -- BYTE-IDENTITA' col driver, 3 passi, seme 11")
    print("=" * 92)
    if not os.path.isfile(PRIMA):
        raise SystemExit("[A] manca %s: la dump PRIMA si prende col blob PRECEDENTE, e questo "
                         "sigillo non puo' ricostruirla da se'." % PRIMA)
    subprocess.run([sys.executable, PROVA, "--out=" + DOPO, "--seme=11", "--passi=3"],
                   capture_output=True, cwd=RADICE)
    p = subprocess.run([sys.executable, PROVA, "--confronta", PRIMA, DOPO],
                       capture_output=True, cwd=RADICE)
    testo_a = _riga(p.stdout) + _riga(p.stderr)
    print(testo_a.strip()[-1800:])
    diverse = None
    for r in testo_a.split(chr(10)):
        if "DIVERSE" in r.upper() or "diverse" in r:
            print("  [riga di verdetto] " + r.strip())
    esiti["A"] = (p.returncode == 0 and "IDENTIC" in testo_a.upper())
    REF["A"] = {"ritorno": p.returncode, "identico": esiti["A"], "prima": os.path.basename(PRIMA),
                "dopo": os.path.basename(DOPO)}
    print("")
    print("  BRACCIO A: %s" % ("PASSA -- byte-identico" if esiti["A"] else "FALLISCE"))
    print("")

    # ================= BRACCIO B: il caso che DEVE fallire =================================
    print("=" * 92)
    print("BRACCIO B -- IL CASO CHE DEVE FALLIRE: `--maxnodi` basso sul simulatore CURATO")
    print("=" * 92)
    REF["B"] = {}
    # B1: la SEMINA. B2: lo SCHEDULATORE, e li' serve un `net` SINTETICO -- vedi `sintetico()`.
    cod, testo = _sotto(100, passi=3)
    print("  --- B1 (la semina non ci sta): maxnodi = 100")
    _stampa(testo)
    b1 = (cod == 3) and ("MAX_NODI" in testo)
    print("      -> ritorno %d, il messaggio nomina MAX_NODI: %s  ==>  %s"
          % (cod, "MAX_NODI" in testo, "PASSA" if b1 else "FALLISCE"))
    REF["B"]["B1_semina"] = {"maxnodi": 100, "ritorno": cod,
                             "nomina_max_nodi": "MAX_NODI" in testo, "passa": b1}
    print("")
    cod, testo = _sotto(sint=True)
    print("  --- B2 (lo SCHEDULATORE, con un `net` SINTETICO: n = MAX_NODI + 1)")
    _stampa(testo)
    b2 = (cod == 3) and ("MAX_NODI" in testo) and ("schedulatore" in testo)
    print("      -> ritorno %d, nomina MAX_NODI: %s, dice `schedulatore`: %s  ==>  %s"
          % (cod, "MAX_NODI" in testo, "schedulatore" in testo, "PASSA" if b2 else "FALLISCE"))
    REF["B"]["B2_schedulatore_sintetico"] = {
        "ritorno": cod, "nomina_max_nodi": "MAX_NODI" in testo,
        "dice_schedulatore": "schedulatore" in testo, "passa": b2}
    print("")
    ok_b = b1 and b2
    esiti["B"] = ok_b
    print("  BRACCIO B: %s" % ("PASSA -- il run SI FERMA" if ok_b else "FALLISCE"))
    print("")

    # ================= BRACCIO C: il controllo POSITIVO ====================================
    print("=" * 92)
    print("BRACCIO C -- CONTROLLO POSITIVO: lo stesso comando sul blob VECCHIO (%s)" % B_VEC[:8])
    print("=" * 92)
    REF["C"] = {}
    cod, testo = _sotto(100, sim=VECCHIO, passi=3)
    print("  --- C1 (la semina): maxnodi = 100 sul VECCHIO")
    _stampa(testo)
    c1 = cod == 0
    print("      -> ritorno %d  ==>  %s   (il vecchio TRONCAVA e CONTINUAVA)"
          % (cod, "PASSA" if c1 else "FALLISCE"))
    REF["C"]["C1_semina"] = {"maxnodi": 100, "ritorno": cod, "passa": c1}
    print("")
    cod, testo = _sotto(sim=VECCHIO, sint=True)
    print("  --- C2 (lo SCHEDULATORE, `net` sintetico) sul VECCHIO")
    _stampa(testo)
    # il vecchio NON ha il controllo: arriva a TOCCARE `net` e muore d'altro (`AttributeError`)
    c2 = (cod == 4) and ("LimiteNodiSuperato" not in testo.replace(
        "`LimiteNodiSuperato` NON ESISTE", ""))
    print("      -> ritorno %d  ==>  %s   (il vecchio deve arrivare a TOCCARE `net`)"
          % (cod, "PASSA" if c2 else "FALLISCE"))
    REF["C"]["C2_schedulatore_sintetico"] = {"ritorno": cod, "passa": c2}
    print("")
    ok_c = c1 and c2
    esiti["C"] = ok_c
    print("  BRACCIO C: %s" % ("PASSA -- il vecchio NON si fermava" if ok_c else "FALLISCE"))
    print("")

    # ================= BRACCIO D: lo sforo, e NON E' MISURABILE QUI ========================
    print("=" * 92)
    print("BRACCIO D -- LO SFORO dentro il passo: **DICHIARATO E NON MISURATO**")
    print("=" * 92)
    print("  Il controllo dello schedulatore sta all'INIZIO del passo, quindi un passo che sfora")
    print("  FINISCE e l'errore arriva al passo DOPO. QUANTO sia lo sforo NON SI MISURA QUI:")
    print("    - sulla scena dei sigilli (ii)(a), seme 11, n = 2107: MISURATI 40 PASSI CON ZERO")
    print("      NASCITE, quindi `n` non cresce e lo sforo non si osserva;")
    print("    - e la strada <<una scena piu' grande del tetto>> e' CHIUSA PER COSTRUZIONE,")
    print("      perche' `semina` ora ferma prima.")
    print("  ### SERVE UNA SCENA CHE CRESCE (un run lungo): e' una misura A SE', e non e' questa.")
    print("  ⚠ E il primo giro di questo sigillo e' FALLITO proprio qui: il braccio B2 aspettava")
    print("    una nascita che non arriva. ERA IL BRACCIO A ESSERE MAL PROGETTATO, NON LA CURA.")
    REF["D"] = {"misurato": False, "passi_provati": 40, "nascite": 0, "n_costante": 2107,
                "perche": "sulla scena dei sigilli non ci sono nascite, e `semina` ferma prima "
                          "che una scena possa nascere oltre il tetto: serve un run lungo"}
    print("")

    # ================= IL VERDETTO =========================================================
    print("=" * 92)
    for k in ("A", "B", "C"):
        print("  braccio %s: %s" % (k, "PASSA" if esiti[k] else "FALLISCE"))
    passa = all(esiti.values())
    print("=" * 92)
    print("### SIGILLO `MAX-NODI-FERMA`: %s" % ("PASSA" if passa else "FALLISCE"))
    print("=" * 92)

    OUT = os.path.join(_QUI, "_sig_max_nodi.json")
    io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(json.dumps(
        {"blob_sim": BLOB, "blob_sim_vecchio": B_VEC, "ancora_cura": ANCORA_CURA,
         "commit_che_introduce": introduce,
         "bracci": REF, "esiti": esiti, "passa": passa}, indent=1,
        ensure_ascii=False, sort_keys=True))
    print("")
    print("scritto: " + OUT)
    return 0 if passa else 1


if __name__ == "__main__":
    _corri, _sim, _passi, _sint = None, SIM, 3, False
    for _x in sys.argv[1:]:
        if _x.startswith("--corri="):
            _corri = int(_x.split("=", 1)[1])
        elif _x.startswith("--sim="):
            _sim = _x.split("=", 1)[1]
        elif _x.startswith("--passi="):
            _passi = int(_x.split("=", 1)[1])
        elif _x == "--sintetico":
            _sint = True
    if _sint:
        sys.exit(sintetico(_sim))
    sys.exit(corri(_corri, _sim, _passi) if _corri is not None else principale())
