# -*- coding: utf-8 -*-
"""Il braccio `--fase-2pi` in `_g4_prova.py`. Una sostituzione per volta (`P1-quater`)."""
import io
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

N = 0


def s1(t, v, nu):
    global N
    assert t.count(v) == 1, "occ=%d per %r" % (t.count(v), v[:70])
    N += 1
    return t.replace(v, nu)


P = "csv/_test_fork/_g4_prova.py"
t = io.open(P, encoding="utf-8", newline="").read()

# --- 1. la firma di `installa`
t = s1(t,
       "def installa(S, spegni_mem, spegni_tutto=False, wrap2pi=False):",
       "def installa(S, spegni_mem, spegni_tutto=False, wrap2pi=False, fase2pi=False):")

# --- 2. il flag, dentro l'involucro, DOPO che il driver ha applicato i suoi
t = s1(t,
       "        if spegni_tutto:\n"
       "            # [G4-bis, 2026-09-22] L'INTERO blocco",
       "        if fase2pi:\n"
       "            # [FASE_2PI, 2026-09-22] `phi` come fase ORDINARIA su [0, 2pi). Sigillo\n"
       "            # `_sigillo_fase_2pi.py` **6/6** sul blob `445e2896`: byte-inerte spenta\n"
       "            # (206 campi identici), e accesa `max(phi)` passa da 12.565546 a 6.282066.\n"
       "            S.FASE_2PI = True\n"
       "        if spegni_tutto:\n"
       "            # [G4-bis, 2026-09-22] L'INTERO blocco")

# --- 3. il modo, fra quelli riconosciuti
t = s1(t,
       '        if a in ("--controllo", "--riferimento", "--spegni", "--spegni-tutto",\n'
       '                 "--ritmo-wrap"):',
       '        if a in ("--controllo", "--riferimento", "--spegni", "--spegni-tutto",\n'
       '                 "--ritmo-wrap", "--fase-2pi", "--fase-2pi-corto"):')

# --- 4. la destinazione
t = s1(t,
       '    elif modo == "--ritmo-wrap":',
       '    elif modo in ("--fase-2pi", "--fase-2pi-corto"):\n'
       '        # [FASE_2PI] LA PROVA DELLA CURA DELLA FASE. Nient\'altro e\' spento: il\n'
       '        # confronto e\' con `_g4_riferimento`, STESSI flag e STESSO seme.\n'
       '        # `--fase-2pi-corto` e\' lo STANDARD 7: un giro CORTO prima del giro vero,\n'
       '        # perche\' la soglia della mitosi scende da 3pi a 2pi e la finestra della\n'
       '        # campana e\' 49.5 volte piu\' popolata (17113 archi contro 346, passo 600):\n'
       '        # se la mitosi accelera di quel fattore, gli ARCHI e il TEMPO esplodono, e\n'
       '        # va saputo su 120 passi invece che su 600.\n'
       '        corto = (modo == "--fase-2pi-corto")\n'
       '        dest = os.path.join(RADICE, "csv", "_test_fork",\n'
       '                            "_f2p_corto" if corto else "_f2p_prova")\n'
       '        if corto and os.path.isdir(dest):\n'
       '            for _f in os.listdir(dest):\n'
       '                if _f.endswith(".pkl.gz"):\n'
       '                    os.remove(os.path.join(dest, _f))\n'
       '        nfr, spegni = (passi or (20 if corto else 100)), False\n'
       '    elif modo == "--ritmo-wrap":')

# --- 5. l'installazione
t = s1(t,
       '    stato, visto = installa(S, spegni, spegni_tutto=(modo == "--spegni-tutto"),\n'
       '                            wrap2pi=(modo == "--ritmo-wrap"))',
       '    stato, visto = installa(S, spegni, spegni_tutto=(modo == "--spegni-tutto"),\n'
       '                            wrap2pi=(modo == "--ritmo-wrap"),\n'
       '                            fase2pi=modo.startswith("--fase-2pi"))')

# --- 6. LA GUARDIA DELL'INVOLUCRO: se il flag non ha attaccato, si FERMA.
#     E' la parte che rende la prova una prova: senza, girerebbe il ramo spento
#     e il confronto sarebbe ON contro ON (il falso PASS di `STEP2_OROLOGIO`).
t = s1(t,
       '            or (modo == "--ritmo-wrap" and not S.RITMO_WRAP_2PI)):',
       '            or (modo == "--ritmo-wrap" and not S.RITMO_WRAP_2PI)\n'
       '            or (modo.startswith("--fase-2pi") and not S.FASE_2PI)):')

# --- 7. il docstring dei modi
t = s1(t,
       "  --spegni-tutto 600 passi, `MEM_MOTO_TUTTO = False`: **L'INTERO BLOCCO**, spostamento di",
       "  --fase-2pi     600 passi, `FASE_2PI = True`: `phi` su [0, 2pi). La CURA di `D35`.\n"
       "  --fase-2pi-corto  120 passi, lo STESSO braccio: **STANDARD 7**, il giro corto prima\n"
       "                 del giro vero, per misurare il COSTO prima di spenderlo.\n"
       "  --spegni-tutto 600 passi, `MEM_MOTO_TUTTO = False`: **L'INTERO BLOCCO**, spostamento di")

io.open(P, "w", encoding="utf-8", newline="\n").write(t)
print("%d sostituzioni in %s" % (N, P))
