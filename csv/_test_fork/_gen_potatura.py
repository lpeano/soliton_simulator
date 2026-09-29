# -*- coding: utf-8 -*-
"""Genera `doc/POTATURA_guardie.md`: la lista dei 57 siti, IN CODA alla potatura generale."""
import collections
import io
import re

TAB = "doc/RIPIEGHI_classi.md"
SRC = "soliton_simulator.py"
OUT = "doc/POTATURA_guardie.md"

src = io.open(SRC, encoding="utf-8").read().split(chr(10))
siti = []
for r in io.open(TAB, encoding="utf-8"):
    m = re.match(r"^\|\s*`:(\d+)`\s*\|\s*`([^`]*)`\s*\|\s*`([^`]*)`\s*\|\s*([A-Z]+)\s*\|\s*(.*?)\s*\|", r)
    if m and "(d)" in m.group(5):
        siti.append((int(m.group(1)), m.group(2), m.group(3)))

per_fn = collections.Counter(x[1] for x in siti)
fusi = [x for x in siti if re.search(r"is None|not hasattr", src[x[0] - 1])]
soli = [x for x in siti if x not in fusi]

R = []
P = R.append
P("# ✂ **`POTATURA-GUARDIE`: i %d rami MORTI, in coda alla potatura generale**" % len(siti))
P("")
P("> ### **Generato da uno script dalla tabella `doc/RIPIEGHI_classi.md`** *(`L-NUMERI`)*: la lista")
P("> non e' scritta a mano. **Si rigenera quando la tabella si rigenera.**")
P("")
P("> ### 🛑 **DECISIONE DI LUCA, 2026-09-29: la pulizia SI RIMANDA alla POTATURA GENERALE, dopo lo")
P("> ### schedulatore** — perche' ### **il riordino della mitosi tocchera' molte di queste righe**,")
P("> e potarle adesso vorrebbe dire farlo **due volte**. ### **Questa voce e' la lista, non il")
P("> lavoro.**")
P("")
P("## Perche' sono rami MORTI, e perche' nessuna misura lo verifica")
P("")
P("| | |")
P("|---|---|")
P("| **sono morti** | con il **controllo unico** acceso, ai due punti del passo ogni grandezza di"
  " **STATO** ha lunghezza **esattamente** `n` o `m`: ### **la condizione di lunghezza di questi"
  " siti non puo' piu' essere falsa** |")
P("| ### **e nessuna misura li verifica** | la prova a guasto trova **solo** cio' che il controllo"
  " **non** copre: per questi ### **il controllo spara PRIMA**. ➜ **«Zero ripieghi silenziosi» e'"
  " gia' raggiunto senza toccarli** |")
P("| ### **quindi il rischio e' a SENSO UNICO** | un errore nella potatura puo' rompere il"
  " **percorso VIVO**, e ### **nessun braccio del sigillo lo distinguerebbe da un errore di"
  " battitura** |")
P("")
P("## ⭐ **LA REGOLA, e vale anche per la potatura futura**")
P("")
P("> # **IL CONTROLLO UNICO POSSIEDE LE LUNGHEZZE.**")
P("> # **I SITI POSSIEDONO SOLO «ESISTE ANCORA?».**")
P("")
P("| forma del sito | che cosa se ne fa |")
P("|---|---|")
P("| **condizione FUSA** *(`is None` / `not hasattr` **e** un test di lunghezza)* — ### **%d siti**"
  " | si **tiene** il test di **esistenza** *(e' un'inizializzazione vera, e resta)*;"
  " ### **la LUNGHEZZA SOLLEVA** |" % len(fusi))
P("| **sola LUNGHEZZA** — ### **%d siti** | ### **si TOGLIE**: il controllo la garantisce, e una"
  " guardia che non guarda niente e' `A9` |" % len(soli))
P("")
P("### ⚠ **E si confrontano ANCHE I CONTATORI, non solo le grandezze**")
P("Questi rami **si contano** *(`A8`)*: `_ritmo_sicurezza`, `_ritmo_guard4pi_ko`,")
P("`_ritmo_snap_identico`, `_g_zeta_vir_*`, `_cs_in_fallback`… ### **Un contatore che cambia di UNO")
P("e' un difetto, e le 23 grandezze del sigillo NON lo vedrebbero** — lo stato puo' restare")
P("identico mentre il **percorso** e' cambiato. *(Il sigillo di `_sin2_vir` li confronta gia'.)*")
P("")
P("## I %d siti, per funzione" % len(siti))
P("")
P("| funzione | siti |")
P("|---|---|")
for fn, q in per_fn.most_common():
    P("| `%s` | **%d** |" % (fn, q))
P("")
P("### ⚠ **I numeri di riga sono quelli del blob di OGGI e SHIFTERANNO** *(par.2)*: la tabella si")
P("**rigenera**, non si aggiorna a mano.")
P("")
P("| riga | funzione | cache | forma |")
P("|---|---|---|---|")
for l, fn, cache in siti:
    forma = ("FUSA" if re.search(r"is None|not hasattr", src[l - 1]) else "sola lunghezza")
    P("| `:%d` | `%s` | `%s` | %s |" % (l, fn, cache, forma))
P("")
io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(R) + chr(10))
print("siti %d  (fuse %d, sola lunghezza %d)  in %d funzioni"
      % (len(siti), len(fusi), len(soli), len(per_fn)))
print("scritto: " + OUT)
