# -*- coding: utf-8 -*-
"""**IL FLAG ERA EFFETTIVAMENTE ACCESO?** — tabella, non deduzione *(Luca, 2026-09-25)*.

> *«Per ogni misura di oggi dichiarata «campo maturo» o «cura 5 ON»: il flag era EFFETTIVAMENTE
> acceso? Leggilo dai referti o dagli strumenti (impostazione del modulo, `ramp p50 == 1`,
> `_g_cura4_maturati > 0`, `_g_m2l_tot > 0`). **Tabella, non deduzione.**»*

**PERCHÉ LA DOMANDA È GIUSTA:** `--semina-matura` e `--mitosi-2lam` **erano MORTI dal CLI**
*(assegnazione in `esegui_headless`, `global` in `_applica_flag`)*. **Le mie sonde impostavano il
modulo DIRETTAMENTE** — `S.SEMINA_MATURA = True` — **che è un'altra strada**, e quella strada
funziona. **Ma «funziona» va MISURATO, non dedotto**, ed è esattamente il punto.

**LE TRE PROVE, in ordine di forza** *(e si riportano TUTTE, non la prima che torna)*:

```
(a) COME il flag e' stato impostato          -> dall'AST del sorgente della sonda
(b) UN EFFETTO NEL REFERTO                   -> `ramp p50 == 1`, `_g_cura4_maturati > 0`,
                                                `_g_m2l_tot > 0`, `_sm_lund_mitosi == 0`
(c) LA STAMPA DEL FLAG nel referto           -> se la sonda l'ha scritta
```

> **(a) da sola non basta:** dice che il codice *intendeva* accenderlo. **(b) è la prova**: un
> effetto che esiste **solo** a flag acceso.
> **E dove (b) manca, la riga dice NON VERIFICATO** — non «probabilmente sì».

**Sola lettura sui file già committati. Nessun run.**
"""
import ast
import io
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
DEST = os.path.join(_QUI, "_verifica_flag", "VERIFICA_FLAG_ACCESI.txt")
os.makedirs(os.path.dirname(DEST), exist_ok=True)

# le misure di oggi, col loro strumento e il loro referto
MISURE = [
    ("SCALE-TW passo pieno", "csv/_test_fork/_scale_tw2.py",
     "csv/_test_fork/_scale_tw2/SCALE_TW_passo_pieno.txt", ("SEMINA_MATURA",)),
    ("chi comprime d0", "csv/_test_fork/_chi_comprime_d0.py",
     "csv/_test_fork/_chi_comprime_d0/CHI_COMPRIME_d0.txt", ("SEMINA_MATURA",)),
    ("figli della mitosi", "csv/_test_fork/_figli_della_mitosi.py",
     "csv/_test_fork/_figli_della_mitosi/FIGLI_DELLA_MITOSI.txt", ("SEMINA_MATURA",)),
    ("limite di accoppiamento", "csv/_test_fork/_limite_accoppiamento.py",
     "csv/_test_fork/_limite_accoppiamento/LIMITE_ACCOPPIAMENTO.txt", ("SEMINA_MATURA",)),
    ("A13 relazionale", "csv/_test_fork/_a13_relazionale.py",
     "csv/_test_fork/_a13_relazionale/A13_RELAZIONALE.txt", ("SEMINA_MATURA",)),
    ("dove sta omega", "csv/_test_fork/_dove_sta_omega.py",
     "csv/_test_fork/_dove_sta_omega/DOVE_STA_OMEGA.txt", ("SEMINA_MATURA",)),
    ("rimisura |dx|/d", "csv/_test_fork/_rimisura_dxd.py",
     "csv/_test_fork/_rimisura_dxd/RIMISURA_dxd.txt", ("SEMINA_MATURA",)),
    ("sigillo CURA 4", "csv/_seal_fork/_sigillo_cura4_accensione.py",
     "csv/_seal_fork/_sig_cura4/SIGILLO_cura4_accensione.txt", ("SEMINA_MATURA",)),
    ("sigillo CURA 5", "csv/_seal_fork/_sigillo_cura5_a13nascita.py",
     "csv/_seal_fork/_sig_cura5/SIGILLO_cura5_a13nascita.txt", ("MITOSI_2LAM",)),
    ("passo zero scena (ii)", "csv/_seal_fork/_passo_zero_scena_ii.py",
     "csv/_seal_fork/_sig_scena_ii/PASSO_ZERO_scena_ii.txt", ()),
]

# gli effetti che PROVANO il flag: solo a flag ACCESO possono valere cosi'
PROVE = {
    "SEMINA_MATURA": [
        (r"ramp\s*(?:finale\s*)?p50\s+1\.0{4,}", "`ramp p50 == 1` nel referto"),
        (r"_g_cura4_maturati['\"]?\s*:\s*(\d+)", "`_g_cura4_maturati > 0`"),
        (r"_g_rampa_tot", "i contatori `_g_rampa*` esistono (girano SOLO a flag acceso)"),
        (r"ramp\s*==\s*1.*4252\s+su\s+4252", "`ramp == 1` su tutti i nodi"),
        (r"ramp1_iniz|ramp_fine_p50\s+1\.000000", "`ramp` a 1 nel referto"),
    ],
    "MITOSI_2LAM": [
        (r"_g_m2l_tot", "il contatore `_g_m2l_tot` esiste (gira SOLO a flag acceso)"),
        (r"negati\s+\d+", "`negati` (candidati rifiutati dalla condizione)"),
        (r"trd_mitosi\s*\[0,\s*0\]", "`_sm_trd_mitosi == 0` nel braccio ON"),
    ],
}

R = []


def P(s=""):
    R.append(s)
    print(s)


def come_impostato(percorso, flag):
    """(a) COME il flag e' impostato, dall'AST del sorgente della sonda. Anche dentro le stringhe
    dei figli generati: le sonde scrivono il figlio come TESTO, quindi l'AST del genitore non lo
    vede -- e va detto."""
    p = os.path.join(RADICE, percorso)
    if not os.path.isfile(p):
        return "FILE ASSENTE", None
    src = io.open(p, encoding="utf-8", errors="replace").read()
    # nel testo (anche dentro la stringa del figlio)
    m = re.findall(r"S\.%s\s*=\s*([A-Za-z0-9_().]+)" % flag, src)
    if m:
        return "modulo DIRETTO: `S.%s = %s`" % (flag, m[0]), m[0]
    if ("--" + flag.lower().replace("_", "-")) in src:
        return "da CLI (`--%s`)" % flag.lower().replace("_", "-"), "CLI"
    return "NESSUNA impostazione trovata", None


P("=" * 120)
P("**IL FLAG ERA EFFETTIVAMENTE ACCESO?** — tabella, non deduzione")
P("=" * 120)
P()
P("  PERCHE' LA DOMANDA E' GIUSTA: `--semina-matura` e `--mitosi-2lam` ERANO MORTI DAL CLI")
P("  (assegnazione in `esegui_headless`, `global` in `_applica_flag`). Le mie sonde impostavano")
P("  il modulo DIRETTAMENTE, che e' un'ALTRA strada -- e quella funziona. Ma \"funziona\" va")
P("  MISURATO, non dedotto.")
P()
P("  (a) COME e' impostato  -> dal sorgente della sonda")
P("  (b) UN EFFETTO nel referto -> vale SOLO a flag acceso. **E' la prova.**")
P("  Dove (b) manca, la riga dice NON VERIFICATO. Non \"probabilmente si'\".")
P()
P("-" * 120)
P("%-26s %-12s %-34s %-44s" % ("misura", "flag", "(a) come impostato", "(b) effetto nel referto"))
P("-" * 120)
ESITI = []
for nome, strum, ref, flags in MISURE:
    if not flags:
        P("%-26s %-12s %-34s %-44s" % (nome[:26], "—", "non dichiara campo maturo",
                                       "n/a (e' il PASSO ZERO)"))
        continue
    for flag in flags:
        modo, val = come_impostato(strum, flag)
        rp = os.path.join(RADICE, ref)
        testo = io.open(rp, encoding="utf-8", errors="replace").read() if os.path.isfile(rp) else ""
        trovate = []
        for pat, et in PROVE.get(flag, []):
            mm = re.search(pat, testo)
            if mm:
                # se il pattern cattura un numero, si controlla che sia > 0
                g = mm.groups()
                if g and g[0].isdigit() and int(g[0]) == 0:
                    continue
                trovate.append(et)
        ok = bool(trovate)
        ESITI.append((nome, flag, modo, trovate, ok, os.path.isfile(rp)))
        P("%-26s %-12s %-34s %-44s"
          % (nome[:26], flag[:12], modo[:34],
             (trovate[0][:44] if trovate else ("NON VERIFICATO" if os.path.isfile(rp)
                                               else "REFERTO ASSENTE"))))
        for t2 in trovate[1:]:
            P("%-26s %-12s %-34s %-44s" % ("", "", "", "+ " + t2[:42]))
P()
P("-" * 120)
P("L'ESITO, per misura")
P("-" * 120)
_ko = [x for x in ESITI if not x[4]]
for nome, flag, modo, trovate, ok, ha_ref in ESITI:
    P("  %-26s %-12s  %s" % (nome[:26], flag[:12],
                             "✅ ACCESO (provato da %d effetto/i)" % len(trovate) if ok
                             else ("⚠ NON VERIFICATO dal referto" if ha_ref
                                   else "⚠ REFERTO ASSENTE")))
    if not ok:
        P("       (a) dice: %s" % modo)
        P("       -> il sorgente INTENDE accenderlo, ma nel referto non c'e' un effetto che lo")
        P("          PROVI. **Non concludo che fosse spento: concludo che NON E' VERIFICATO.**")
P()
P("=" * 120)
P("%d misure verificate ACCESE, %d NON verificate su %d"
  % (len(ESITI) - len(_ko), len(_ko), len(ESITI)))
P("=" * 120)
P()
P("❗ E IL FATTO CHE VALE PER TUTTE, letto dal codice e non dedotto:")
P("   `S.SEMINA_MATURA = True` su un modulo importato **FUNZIONA**: e' un'assegnazione di")
P("   ATTRIBUTO DI MODULO, e `_pesi` legge la globale del modulo. **Il difetto dei flag morti")
P("   stava SOLO nel percorso CLI** (`esegui_headless` invece di `_applica_flag`), che le sonde")
P("   NON usano. **Ma questa e' un'argomentazione, e la colonna (b) e' la MISURA.**")
P()
P("COSA QUESTO NON DICE:")
P("  - non rifa' le misure: verifica che il flag fosse acceso QUANDO sono state fatte.")
P("  - la colonna (a) guarda anche DENTRO le stringhe dei figli generati, perche' le sonde")
P("    scrivono il figlio come TESTO: l'AST del genitore non lo vedrebbe. E' una ricerca per")
P("    ESPRESSIONE, non per AST, e va detto.")

io.open(DEST, "w", encoding="utf-8", newline="\n").write(chr(10).join(R) + chr(10))
