# -*- coding: utf-8 -*-
"""PUNTO `5` DELLA TERZA PARTE — **I HOOK LOCALI SONO LA BARRIERA, LA CI E' UNA RETE.**

> ### ⛔ **La decisione di Luca (2026-10-09):** *«**NESSUNA protezione del ramo su
> GitHub**»* — quindi ### **la CI non può impedire niente: gira DOPO il push.** ### **I
> hook LOCALI sono la barriera**, e il mandato chiede che *«ogni strumento dell'era `2`
> verifica all'avvio che siano ATTIVI *(`core.hooksPath` giusto, hook presenti,
> **impronta attesa**)* e **si RIFIUTA di partire** se non lo sono»*.

### ⛔ **E IL MANDATO, PRESO ALLA LETTERA, ROMPEREBBE LA CI — l'ho scritto nel task history
PRIMA di toccare niente.** Nella CI i hook ### **non sono attivi**: `core.hooksPath` non è
impostato in un `checkout` pulito, quindi ### **ogni strumento si rifiuterebbe di partire e
la CI fallirebbe SEMPRE.** ### ⭐ **Non è un dettaglio di configurazione: è una
contraddizione dentro il mandato.**

### ✅ **LA MIA INFERENZA, DICHIARATA: la barriera è LOCALE, e il controllo deve
RICONOSCERE DI NON ESSERE IN LOCALE.** Fuori dal PC — `CI=true`, che GitHub dichiara da sé
— ### **la barriera TACE, perché là la sua ragione non esiste:** là ### **non si committa**,
si ### **guarda.** ### ⚠ **E il mandato non lo dice: questa è una scelta mia, e la scrivo
qui invece di nasconderla in un `if`.**

| | che cosa guarda | che cosa fa se non torna |
|---|---|---|
| `a` | `core.hooksPath` è ### **`.githooks`** | ### **FERMA** |
| `b` | i ### **due** hook ci sono | ### **FERMA** |
| `c` | la loro ### **impronta** è quella attesa | ### **FERMA** |
| `d` | in `.git/hooks/` ### **non restano copie** | ### **SEGNALA** *(non girano più: `core.hooksPath` sostituisce quella cartella)* |

### ⛔ **E CIO' CHE QUESTA BARRIERA NON PUO' FARE, detto qui e non in fondo a un referto.**

### ⚠ **`(1)` `git commit --no-verify` NON E' IMPEDIBILE IN LOCALE.** Nessun hook gira, e
nessun controllo in uno strumento può accorgersene — perché ### **lo strumento non viene
chiamato.** ### ✅ **Quello lo trova la CI**, che è appunto ### **una rete**: non impedisce,
### **fa vedere.**

### ⚠ **`(2)` L'IMPRONTA E' IN UN FILE TRACCIATO, quindi chi cambia un hook può cambiare
anche lei.** ### ⛔ **Questa barriera NON impedisce quella mossa: la rende VISIBILE IN UNA
DIFF.** ### ⭐ **E la differenza fra <<impedire>> e <<rendere visibile>> è esattamente ciò
che `A9` chiede di non confondere** — ed è la stessa correzione che Luca mi ha fatto sulla
CI.
"""
import hashlib
import io
import json
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)

NL = chr(10)
PRESIDIO = "P-BARRIERA"

GITHOOKS = ".githooks"
HOOK = ("pre-commit", "commit-msg")
IMPRONTE = os.path.join(_QUI, "_barriera.lock")

# ### ⛔ **LE VARIABILI CHE DICHIARANO <<NON SEI IN LOCALE>>.** `CI` la mette
# ### ### **GitHub Actions**, e non la scrivo io: ### **e- una dichiarazione
# ### dell-ambiente**, non una mia supposizione.
FUORI_DAL_PC = ("CI", "GITHUB_ACTIONS", "CONTINUOUS_INTEGRATION")


def in_locale():
    """### `False` se siamo ### **fuori dal PC** *(CI)*. ### **Dichiarato, non dedotto.**"""
    return not any(str(os.environ.get(v, "")).lower() in ("1", "true", "yes")
                   for v in FUORI_DAL_PC)


def _sha(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def impronte_ora():
    """Le impronte dei due hook ### **sul disco**, o `None` se manca."""
    fuori = {}
    for h in HOOK:
        p = os.path.join(RADICE, GITHOOKS, h)
        fuori[h] = _sha(p) if os.path.exists(p) else None
    return fuori


def attese():
    """Le impronte ### **dichiarate**, da `csv/_barriera.lock`."""
    if not os.path.exists(IMPRONTE):
        return {}
    return (json.loads(io.open(IMPRONTE, encoding="utf-8").read()) or {}).get(
        "impronte", {})


def errori():
    """### Gli errori della barriera, o `[]`. ### **Vuoto se non siamo in locale.**"""
    if not in_locale():
        return []
    err = []
    q = subprocess.run(["git", "config", "--get", "core.hooksPath"], cwd=RADICE,
                       capture_output=True, text=True)
    via = (q.stdout or "").strip()
    if via != GITHOOKS:
        err.append("`P-BARRIERA`: `core.hooksPath` e- `%s` e non `%s`. ### I hook di "
                   "`.git/hooks/` NON VIAGGIANO COL REPO: senza questo comando -- "
                   "`git config core.hooksPath .githooks` -- chi clona NON HA NESSUN "
                   "PRESIDIO, e per `A9` un presidio che dipende da un comando dato a "
                   "mano E- UNA TENDA" % (via or "<non impostato>", GITHOOKS))
        return err
    ora = impronte_ora()
    att = attese()
    for h in HOOK:
        if ora.get(h) is None:
            err.append("`P-BARRIERA`: l-hook `%s` NON C-E- in `%s/`. ### `core.hooksPath` "
                       "e- impostato, quindi git cerca LA- e non trova niente: la "
                       "barriera SEMBRA attiva e non lo e-" % (h, GITHOOKS))
            continue
        if not att.get(h):
            err.append("`P-BARRIERA`: l-hook `%s` non ha un-IMPRONTA ATTESA in "
                       "`csv/_barriera.lock`. ### Senza impronta, un hook SOSTITUITO DA "
                       "UN GUSCIO VUOTO passerebbe: c-e-, e non fa niente" % h)
            continue
        if ora[h] != att[h]:
            err.append("`P-BARRIERA`: l-hook `%s` ha impronta `%s` e l-attesa e- `%s`. "
                       "### Se il cambiamento e- VOLUTO: `python csv/_barriera.py "
                       "--scrivi`, e la diff del `.lock` LO MOSTRA -- che e- tutto cio- "
                       "che questa barriera puo- fare (non impedisce: RENDE VISIBILE)"
                       % (h, ora[h][:8], str(att[h])[:8]))
    return err


def segnali():
    """Le copie rimaste in `.git/hooks/`: ### **non girano piu-**, e vanno dette."""
    if not in_locale():
        return []
    d = os.path.join(RADICE, ".git", "hooks")
    resti = [h for h in HOOK if os.path.exists(os.path.join(d, h))]
    if not resti:
        return []
    return ["`P-BARRIERA` segnale: in `.git/hooks/` restano copie di %s. "
            "### `core.hooksPath` SOSTITUISCE quella cartella, quindi quelle copie NON "
            "GIRANO PIU- -- e due verita- sono peggio di una" % ", ".join(resti)]


def controlla():
    """### **FERMA** se la barriera non e- in piedi *(e solo in locale)*."""
    err = errori()
    assert not err, ("### LA BARRIERA DEI HOOK NON E- IN PIEDI:"
                     + "".join(NL + "  " + x for x in err))


def scrivi():
    """Scrive `csv/_barriera.lock` con le impronte ### **di adesso.**

    ### ⚠ **Si lancia A MANO:** un `.lock` che si riscrive da se- ### **non
    dichiara niente** -- coinciderebbe sempre.
    """
    d = {"impronte": impronte_ora(),
         "perche": ("le impronte dei due hook. ### NON IMPEDISCONO che qualcuno li "
                    "cambi: lo RENDONO VISIBILE IN UNA DIFF, perche- questo file e- "
                    "TRACCIATO. ### La differenza fra <<impedire>> e <<rendere "
                    "visibile>> e- cio- che `A9` chiede di non confondere."),
         "come_si_riscrive": "python csv/_barriera.py --scrivi",
         "e_in_ci": ("la barriera TACE fuori dal PC (`CI=true`): la- non si committa, si "
                     "GUARDA, e il mandato preso alla lettera farebbe FALLIRE SEMPRE la "
                     "CI. ### E- una MIA INFERENZA, dichiarata.")}
    io.open(IMPRONTE, "w", encoding="utf-8", newline=NL).write(
        json.dumps(d, indent=1, sort_keys=True, ensure_ascii=False) + NL)
    return d


def collaudo():
    """### La barriera, ### **nei DUE VERSI**, e col ramo ### **END-TO-END.**

    ### ⛔ **IL CASO CHE DEVE FALLIRE TOCCA LA CONFIGURAZIONE DI GIT**, e la rimette
    in un `finally` ### **verificandola** -- perche- un collaudo che lascia
    `core.hooksPath` sbagliato ### **spegne la barriera che sta collaudando.**
    """
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-62s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL COLLAUDO DELLA BARRIERA -- nei DUE VERSI   (punto 5)")
    print("=" * 100)
    ora, att = impronte_ora(), attese()
    print("  in locale: %s" % in_locale())
    for h in HOOK:
        print("     %-12s ora %s   attesa %s"
              % (h, (ora.get(h) or "### MANCA")[:16], str(att.get(h))[:16]))
    esito("### il collaudo ha MATERIA: i due hook ci sono, con le loro impronte",
          all(ora.get(h) and att.get(h) for h in HOOK),
          "### senza di loro ogni braccio sotto passerebbe PER VACUITA-")
    esito("NON deve scattare: la barriera e- in piedi adesso",
          errori() == [],
          "### se scattasse, sarebbe LA BARRIERA a essere giu-, non il collaudo")
    # ------------------------------------------------- ### fuori dal PC: DEVE TACERE
    _vero = {v: os.environ.get(v) for v in FUORI_DAL_PC}
    try:
        os.environ["CI"] = "true"
        esito("NON deve scattare: fuori dal PC (`CI=true`) la barriera TACE",
              errori() == [] and not in_locale(),
              "### la- non si committa, si GUARDA -- e il mandato preso alla lettera "
              "farebbe FALLIRE SEMPRE la CI. E- UNA MIA INFERENZA, dichiarata")
    finally:
        for v, x in _vero.items():
            if x is None:
                os.environ.pop(v, None)
            else:
                os.environ[v] = x
    esito("### e rimesso l-ambiente, siamo di nuovo in locale",
          in_locale(), "### un collaudo che lascia l-ambiente storto non e- un collaudo")
    # ------------------------------------------------- ### l-impronta che non torna
    _att_vere = dict(att)
    try:
        globals()["attese"] = lambda: dict(_att_vere, **{HOOK[0]: "0" * 40})
        e = errori()
        esito("### DEVE scattare: un hook con l-IMPRONTA che non torna",
              any("impronta" in x and HOOK[0] in x for x in e),
              "### un hook SOSTITUITO DA UN GUSCIO VUOTO c-e- e non fa niente: senza "
              "l-impronta passerebbe")
        globals()["attese"] = lambda: {}
        esito("### DEVE scattare: un hook SENZA impronta attesa",
              any("non ha un-IMPRONTA ATTESA" in x for x in errori()),
              "### senza impronta la barriera guarda solo che il FILE CI SIA")
    finally:
        globals()["attese"] = lambda: dict(_att_vere)
    esito("### e le impronte attese sono tornate quelle vere",
          attese() == _att_vere, "### si tocca la FUNZIONE, non il file sul disco")
    # ------------------------------------------------- ### il ramo END-TO-END
    import subprocess
    q = subprocess.run(["git", "config", "--get", "core.hooksPath"], cwd=RADICE,
                       capture_output=True, text=True)
    via0 = (q.stdout or "").strip()
    try:
        subprocess.run(["git", "config", "core.hooksPath", ".githooks-NON-ESISTE"],
                       cwd=RADICE, capture_output=True)
        esito("### DEVE scattare: `core.hooksPath` SBAGLIATO",
              any("core.hooksPath" in x for x in errori()),
              "### i hook di `.git/hooks/` NON VIAGGIANO COL REPO: senza il comando, chi "
              "clona NON HA NESSUN PRESIDIO (`A9`: una tenda)")
        r = subprocess.run([sys.executable, os.path.join("csv", "_metodi_era2.py")],
                           cwd=RADICE, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        fuori = (r.stdout or "") + (r.stderr or "")
        esito("### DEVE scattare END-TO-END: uno STRUMENTO VERO si RIFIUTA di partire",
              r.returncode == 3 and "RIFIUTO DI GIRARE" in fuori,
              "codice %d: ### la barriera sta in `_presidio.avvia()`, che OGNI strumento "
              "chiama -- metterla in ognuno vorrebbe dire ricordarsela ogni volta, e il "
              "primo che la dimentica NON HA NESSUNA BARRIERA" % r.returncode)
    finally:
        if via0:
            subprocess.run(["git", "config", "core.hooksPath", via0], cwd=RADICE,
                           capture_output=True)
        else:
            subprocess.run(["git", "config", "--unset", "core.hooksPath"], cwd=RADICE,
                           capture_output=True)
    q2 = subprocess.run(["git", "config", "--get", "core.hooksPath"], cwd=RADICE,
                        capture_output=True, text=True)
    esito("### e `core.hooksPath` e- tornato `%s`" % (via0 or "<non impostato>"),
          (q2.stdout or "").strip() == via0,
          "### un collaudo che lascia `core.hooksPath` storto SPEGNE LA BARRIERA CHE STA "
          "COLLAUDANDO")
    esito("NON deve scattare: alla fine la barriera e- di nuovo in piedi",
          errori() == [], "### e il repo e- come l-ho trovato")
    print("=" * 100)
    print("IL COLLAUDO DELLA BARRIERA: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


def main(argv):
    if "--collaudo" in argv:
        return collaudo()
    if "--scrivi" in argv:
        d = scrivi()
        print("  scritto %s" % IMPRONTE)
        for h in HOOK:
            print("     %-12s %s" % (h, d["impronte"][h]))
        return 0
    print("  `P-BARRIERA`: in locale: %s" % in_locale())
    for h, v in sorted(impronte_ora().items()):
        print("     %-12s ora %s   attesa %s"
              % (h, (v or "### MANCA")[:16], str(attese().get(h))[:16]))
    err = errori()
    for x in err + segnali():
        print("  " + x)
    if err:
        print("  ### `P-BARRIERA` FALLISCE: %d errori" % len(err))
        return 1
    print("  ### `P-BARRIERA`: LA BARRIERA E- IN PIEDI"
          if in_locale() else "  ### `P-BARRIERA`: fuori dal PC, TACE")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
