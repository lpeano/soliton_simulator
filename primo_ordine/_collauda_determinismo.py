# -*- coding: utf-8 -*-
"""IL COLLAUDO DEL DETERMINISMO — **punto `1` della terza parte, nei DUE VERSI.**

### ⭐ **IL BRACCIO CHE CONTA E' L'ULTIMO: DUE PROCESSI, BYTE IDENTICI.** Tutti gli altri
guardano ### **le condizioni** del determinismo *(l'RNG, i thread, le versioni)*; quello
guarda ### **il determinismo.** ### ⛔ **E se passa, dice una cosa che nessuna condizione
può dire: che QUALUNQUE sia il numero di thread, NON sta rompendo la riproducibilità** —
che è esattamente ciò che non posso verificare in altro modo, perché `threadpoolctl`
### **non è installato.**

### ⚠ **E STA IN UN MODULO SUO per la ragione che `P-MOD` mi ha insegnato col grafo:** fa
girare ### **il driver**, e il driver importa `determinismo`. ### **Dentro
`determinismo.py` sarebbe un CICLO.**
"""
import ast
import io
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
# ### ⚠ **`schema_config` vive in `primo_ordine/config/`**, e il percorso si aggiunge
# ### come fa `_collauda_passo.py`: ### **un modulo si trova dove sta, non dove mi
# ### farebbe comodo.**
sys.path.insert(0, os.path.join(_QUI, "config"))

import determinismo as DET                                   # noqa: E402
import schema_config as CFG                                  # noqa: E402

NL = chr(10)
CONFIG = os.path.join("primo_ordine", "config", "prova.yaml")


def ordine_avvia(percorso):
    """### `(riga_avvia, riga_numpy)` in un file: ### **l-ORDINE E- UN PRESIDIO.**

    ### ⛔ **VIA AST:** <<`DET.avvia()` prima di `import numpy`>> e- una proprieta-
    ### **dell-ordine delle istruzioni**, e una regex ### **non sa che cosa sia un
    ### import.**
    """
    a = ast.parse(io.open(percorso, encoding="utf-8").read())
    r_avvia = r_numpy = None
    for n in ast.walk(a):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) \
                and n.func.attr == "avvia" and r_avvia is None:
            r_avvia = n.lineno
        if isinstance(n, ast.Import):
            for al in n.names:
                if al.name == "numpy" and r_numpy is None:
                    r_numpy = n.lineno
    return r_avvia, r_numpy


def collaudo():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-62s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL COLLAUDO DEL DETERMINISMO -- nei DUE VERSI   (punto 1)")
    print("=" * 100)

    # ------------------------------------------------------------------ (a) l-RNG
    usi = DET.usi_di_random()
    globali = DET.rng_globale()
    print("  gli usi di `random` sotto `primo_ordine/`: %d" % len(usi))
    for rel, riga, attr in usi:
        print("     %-40s riga %-4d  .%s" % (rel, riga, attr))
    esito("### il collaudo ha MATERIA: ci sono usi di `random`",
          len(usi) > 0,
          "%d: ### senza di loro il braccio sotto non proverebbe niente" % len(usi))
    esito("NON deve scattare: ZERO RNG globali",
          globali == [],
          "%d su %d sono `default_rng`: ### un RNG globale non ha un seme esplicito, "
          "quindi la corsa NON SI PUO- RIPETERE" % (len(usi), len(usi)))
    # ### ⛔ **IL CASO CHE DEVE FALLIRE: un sorgente FINTO, in una cartella a parte.**
    # ### ⚠ **Non si tocca nessun file del repo**, e il presidio si chiama
    # ### ### **su quella radice** -- cosi- il braccio ### **non puo- lasciare danno.**
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        fin = os.path.join(tmp, "primo_ordine")
        os.makedirs(fin)
        io.open(os.path.join(fin, "finto.py"), "w", encoding="utf-8").write(
            "import numpy as np" + NL + "x = np.random.normal(size=3)" + NL)
        e = DET.rng_globale(fin)
        esito("### DEVE scattare: `np.random.normal` -- l-RNG GLOBALE",
              any("L-RNG GLOBALE" in x and "normal" in x for x in e),
              "### su un sorgente FINTO in una cartella temporanea: il braccio NON TOCCA "
              "NESSUN FILE DEL REPO")

    # ------------------------------------------------------------------ (b) i THREAD
    print()
    t = DET.per_il_timbro()
    esito("NON deve scattare: le CINQUE variabili dei thread sono fissate",
          len(t["un_thread"]) == 5 and all(
              os.environ.get(v) == "1" for v in DET.UN_THREAD),
          "### cinque e non una: ogni libreria numerica legge LA SUA, e fissarne una sola "
          "lascia le altre LIBERE DI MULTITHREADARE")
    ra, rn = ordine_avvia(os.path.join(RADICE, "primo_ordine", "driver.py"))
    esito("NON deve scattare: nel DRIVER `avvia()` sta PRIMA di `import numpy`",
          ra is not None and rn is not None and ra < rn,
          "riga %s contro %s: ### le BLAS leggono quelle variabili AL CARICAMENTO, e "
          "scriverle dopo NON SERVE A NIENTE" % (ra, rn))
    with tempfile.TemporaryDirectory() as tmp:
        fin = os.path.join(tmp, "storto.py")
        io.open(fin, "w", encoding="utf-8").write(
            "import numpy as np" + NL + "import determinismo as DET" + NL
            + "DET.avvia()" + NL)
        ra2, rn2 = ordine_avvia(fin)
        esito("### DEVE scattare: l-ordine ROVESCIATO si vede",
              ra2 is not None and rn2 is not None and ra2 > rn2,
              "riga %s contro %s: ### e- il braccio che dice che il controllo guarda "
              "L-ORDINE e non la presenza" % (ra2, rn2))

    # ------------------------------------------------------------------ (c) le VERSIONI
    print()
    bl = DET.blocco()
    esito("### il blocco `versioni.lock` ESISTE e ha delle versioni",
          bool((bl or {}).get("versioni")),
          "%d pacchetti: %s" % (len((bl or {}).get("versioni") or {}),
                                "  ".join("%s=%s" % (k, v) for k, v in
                                          sorted(((bl or {}).get("versioni")
                                                  or {}).items()))))
    # ### ⛔ **QUESTO BRACCIO PRETENDEVA <<NESSUNA DIFFERENZA>>, E ERA SBAGLIATO
    # ### -- me lo ha detto il guardiano, su un clone Linux.** In CI la piattaforma e-
    # ### ### **Linux** e `requirements.txt` installa con ### **`>=`**, quindi le
    # ### versioni sono ### **PIU- NUOVE del blocco** e `scarti()[1]` ### **non e- mai
    # ### vuoto.** ### ⚠ **Quindi il braccio FALLIVA SEMPRE in CI**, e
    # ### ### **contraddiceva il braccio qui sotto**, che dice *<<una versione PIU- NUOVA
    # ### NON ferma>>*: ### **due bracci dello stesso collaudo pretendevano cose
    # ### opposte.**
    # ### ✅ **CIO- CHE IL BLOCCO PROMETTE E- <<NIENTE FERMA>>, non <<niente
    # ### cambia>>:** la promessa e- che una versione ### **piu- vecchia** fermi e che le
    # ### differenze ### **finiscano NEL TIMBRO** -- e il timbro e- il posto dove una
    # ### corsa dichiara di ### **non essere confrontabile al bit** con un-altra.
    _ferma, _diff = DET.scarti()
    esito("NON deve scattare: NIENTE FERMA, qualunque siano le differenze dal blocco",
          _ferma == [],
          "%d differenze dal blocco, e NESSUNA ferma. ### In CI ce ne sono SEMPRE "
          "(Linux, e `requirements.txt` installa con `>=`): un braccio che pretendesse "
          "ZERO differenze FALLIREBBE SEMPRE la- -- ed e- quello che faceva"
          % len(_diff))
    _t = DET.per_il_timbro()
    esito("### e le differenze dal blocco FINISCONO NEL TIMBRO",
          _t.get("versioni_differenze") == _diff
          and "versioni_blocco" in _t and "versioni" in _t,
          "%s. ### E- qui che una corsa dichiara di NON ESSERE CONFRONTABILE AL BIT con "
          "un-altra: il blocco non serve a impedire, serve a DIRE DOVE SI E- MISURATO"
          % (_diff or "nessuna differenza su questa macchina"))
    # ### ⛔ **IL CASO CHE DEVE FERMARE: un blocco che chiede una versione PIU- NUOVA**
    # ### *(cioe- quella di adesso e- PIU- VECCHIA del blocco)*. ### ⚠ **Si costruisce
    # ### IN MEMORIA**, passando il blocco finto: ### **il file sul disco non si tocca.**
    ora = DET.versioni()
    piu_nuovo = dict(ora)
    piu_nuovo["numpy"] = "99.0.0"
    ferma, diff = DET.scarti(ora, {"versioni": piu_nuovo})
    esito("### DEVE scattare: una versione PIU- VECCHIA del blocco FERMA",
          any("PIU- VECCHIO del blocco" in x and "numpy" in x for x in ferma),
          "blocco `99.0.0` contro `%s`: ### il blocco registra CIO- CHE E- STATO "
          "VERIFICATO, e una versione piu- vecchia NON lo e-" % ora.get("numpy"))
    # ### ✅ **E IL ROVESCIO: una versione PIU- NUOVA NON ferma, ma si VEDE.**
    piu_vecchio = dict(ora)
    piu_vecchio["numpy"] = "0.1.0"
    ferma2, diff2 = DET.scarti(ora, {"versioni": piu_vecchio})
    esito("NON deve scattare: una versione PIU- NUOVA del blocco NON ferma",
          ferma2 == [] and any("numpy" in x for x in diff2),
          "### ma la differenza VA NEL TIMBRO: fermare su qualunque differenza "
          "romperebbe la CI (installa con `>=` e gira su Linux), e il repo ha GIA- "
          "MISURATO che la piattaforma cambia i numeri assoluti")

    # ------------------------------------------------------- (d) ### DUE PROCESSI
    print()
    print("-" * 100)
    print("IL BRACCIO CHE CONTA: DUE PROCESSI, STESSA CONFIGURAZIONE, BYTE IDENTICI")
    print("-" * 100)
    c = CFG.carica(os.path.join(RADICE, CONFIG))
    imp = CFG.impronta(c)[:10]
    dati = os.path.join(RADICE, "db_era2", "stato_%s.npz" % imp)
    tim = dati + ".timbro.json"
    byte = []
    for giro in (1, 2):
        r = subprocess.run([sys.executable, os.path.join("primo_ordine", "driver.py"),
                            CONFIG], cwd=RADICE, capture_output=True)
        assert r.returncode == 0, (r.stdout or b"").decode("utf-8", "replace") + \
            (r.stderr or b"").decode("utf-8", "replace")
        byte.append((io.open(dati, "rb").read(), io.open(tim, "rb").read()))
        print("  giro %d: %d byte di dati, %d byte di timbro"
              % (giro, len(byte[-1][0]), len(byte[-1][1])))
    esito("NON deve scattare: i DATI dei due processi sono BYTE-IDENTICI",
          byte[0][0] == byte[1][0],
          "### e NON e- fortuna: `numpy.savez` scrive `date_time = (1980,1,1,0,0,0)` "
          "nello ZIP, cioe- AZZERA L-ORA -- verificato leggendo l-intestazione")
    esito("NON deve scattare: i TIMBRI dei due processi sono BYTE-IDENTICI",
          byte[0][1] == byte[1][1],
          "### il timbro porta le versioni, il conto delle leggi e il determinismo: se "
          "cambiasse, cambierebbe LA DICHIARAZIONE della corsa")
    esito("### e questo braccio dice cio- che i THREAD non posso misurare",
          byte[0][0] == byte[1][0],
          "### `threadpoolctl` NON e- installato, quindi il numero di thread EFFETTIVO "
          "non lo verifico. ### Ma se due processi danno byte identici, i thread NON "
          "stanno rompendo il determinismo -- qualunque sia il loro numero")

    print("=" * 100)
    print("IL COLLAUDO DEL DETERMINISMO: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(collaudo())
