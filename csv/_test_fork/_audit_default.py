# -*- coding: utf-8 -*-
"""§1 DEL MANDATO — COSA E' GIA' DEFAULT? Dal DISCO, non dalla memoria.

«Una cura sigillata che non gira e' una cura che non esiste» -- la famiglia «cablato ma muto»
(`VERSO_CHI`, `_passo_spinoriale` «ORFANO», `spin_locale`, `TW_SPINORE`, la FASE 5 inerte al
95.33 %). Quindi per ogni cura di questo giro si chiede: **e' dietro un flag? con quale default?**

E si chiede anche la cosa che quella famiglia insegna: **il flag che la governa e' a sua volta
gated su un altro flag?** Un `SPIN_FEEDBACK = True` sotto un `SPINORE_VIVO = False` e' un flag
acceso che NON GIRA.

Lo script legge i DEFAULT DI MODULO importando il simulatore con `argv` vuoto -- cioe' esattamente
lo stato in cui si trova un run che non passa nessun flag.
ASCII PURO.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import _presidio
_presidio.avvia(__file__)

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
sys.argv = ["soliton_simulator.py"]
import soliton_simulator as S

src = open(os.path.join(ROOT, "soliton_simulator.py"), encoding="utf-8", errors="replace").read()
righe = src.splitlines()


def riga(fr):
    for k, l in enumerate(righe, 1):
        if fr in l:
            return k
    return -1


print("=" * 118)
print("AUDIT DEI DEFAULT -- cosa gira in un run che non passa nessun flag")
print("=" * 118)

# (nome, frammento che identifica il codice curato, flag che lo governa oppure None)
CURE = [
    ("d_arco (bug di indicizzazione)", "d_arco = self.d", None, "V1 8/8"),
    ("plasticita' viscoelastica causale", "tau_p_loc = np.maximum(t_luce, t_visco)", None, "V2-V5 8/8"),
    ("inerzia dimensionale", "inerzia = np.maximum(_contrasto * _T2", None, "Y 11/11"),
    ("(2) spinta LOCALE", "spinta = 0.02 * self.d0", None, "V6-V10 12/12"),
    ("(3) _rep come MEMORIA", "self._rep = self._rep + _dte", None, "V6-V10 12/12"),
    ("(5) spin_locale RIMOSSA", "def spin_locale", None, "V9 4/4  (assenza = curato)"),
    ("TEMPO 2 (calcola_psi con w)", "psi_forces = psi_t if SYNC_UPDATE else self.calcola_psi(w)", None, "Q 7/7"),
    ("Z25  denominatore del feedback", "np.add.at(out, jj, flusso)", "SPIN_FEEDBACK", "F/G 12/12"),
    ("Z27  /grado tolta da twist_nodo", "coppia = coppia + twist_nodo[:self.n]", "FRAME_DRAG", "H 8/8"),
    ("contatori A8 del feedback", "self._sfb_chiamate", "SPIN_FEEDBACK", "-"),
    ("presidio ENCODING + timbro git", None, None, "-"),
]

print("\n  %-36s %-9s %-16s %-9s %-16s" % ("cura", "nel file", "flag che governa", "default", "sigillo"))
print("  " + "-" * 110)
muti = []
for nome, fr, flag, sig in CURE:
    presente = "-" if fr is None else ("SI' :%d" % riga(fr) if riga(fr) > 0 else "!! NO")
    if nome.startswith("(5)"):
        presente = "ASSENTE" if riga(fr) < 0 else "!! ANCORA PRESENTE"
    if flag is None:
        d = "-"; f = "nessuno (cat. D)"
    else:
        f = flag; d = str(getattr(S, flag, "?"))
        if getattr(S, flag, False) is False:
            muti.append((nome, flag))
    print("  %-36s %-9s %-16s %-9s %-16s" % (nome[:36], presente, f, d, sig))

print("\n--- I FLAG DI MODULO CITATI, coi loro default (argv vuoto) ---")
for f in ("SPINORE", "SPINORE_VIVO", "SPIN_FEEDBACK", "FRAME_DRAG", "REPULS_LEGGE",
          "CHI_CORE", "TAU_A_LOCALE", "PAV_COM", "TW_SPINORE", "CHI_DA_SPINORE", "STEP2_OROLOGIO"):
    v = getattr(S, f, "ASSENTE")
    print("  %-18s = %-8s  :%d" % (f, v, riga("%s = " % f)))

print("\n--- ⚠ LA CATENA DI GATE DEL FEEDBACK (la lezione «cablato ma muto») ---")
k = riga("if SPINORE_VIVO and SPINORE and SPIN_FEEDBACK")
print("  :%d   if SPINORE_VIVO and SPINORE and SPIN_FEEDBACK:" % k)
print("  SPINORE_VIVO = %-6s   SPINORE = %-6s   SPIN_FEEDBACK = %-6s"
      % (S.SPINORE_VIVO, S.SPINORE, S.SPIN_FEEDBACK))
attivo = bool(S.SPINORE_VIVO and S.SPINORE and S.SPIN_FEEDBACK)
print("  -> il feedback GIRA nel default? %s" % ("SI'" if attivo else "NO"))
if not attivo:
    manca = [f for f in ("SPINORE_VIVO", "SPINORE", "SPIN_FEEDBACK") if not getattr(S, f, False)]
    print("     manca: %s" % manca)
    print("""
  ⚠ CONSEGUENZA OPERATIVA, ED E' IL PUNTO DEL par.2.3 DEL MANDATO:
     mettere `SPIN_FEEDBACK = True` NON BASTA. Con `SPINORE_VIVO = False` il ramo resta SPENTO,
     e resta spento IN SILENZIO -- nessun avviso, nessun contatore che scatti, perche' il metodo
     non viene nemmeno chiamato. Sarebbe ESATTAMENTE la famiglia «cablato ma muto» che questo
     audit esiste per intercettare.""")

if muti:
    print("\n--- CURE DIETRO UN FLAG SPENTO (una cura che non gira e' una cura che non esiste) ---")
    for nome, flag in muti:
        print("  %-38s dietro %-16s = False" % (nome[:38], flag))

print("\n" + "=" * 118)
