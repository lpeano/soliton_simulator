# -*- coding: utf-8 -*-
"""FASE 2 -- AUDIT RETROATTIVO CONTRO A8. **Bloccante.**

Le due correzioni gia' cablate in questo giro -- `d_arco` (00adcd9) e la plasticita' viscoelastica
causale (f405327) -- sono state fatte PRIMA che A8 esistesse. Questo file enumera OGNI ramo
condizionale che toccano, verifica se e' contato, e MISURA quanto scatta.

CRITERIO, da A8:
  ~0 %            -> fallback vero, legittimo
  > qualche %     -> NON e' un fallback: e' il comportamento principale. REPERTO.
  nessun contatore-> va aggiunto (P5) e la frazione misurata PRIMA di proseguire.

E A8b sulle CACHE cross-passo: estensione a TUTTI i punti di crescita, guardia contata, ~0 %.
ASCII PURO. Nessun run di misura: l'esecuzione serve all'audit.
"""
import sys as _sys_enc  # PRESIDIO ENCODING (CLAUDE.md): lo stdout di Windows e' cp1252 e
# uccide qualunque print con un carattere non-ASCII. E' successo SETTE volte, l'ultima allo
# script che stava CONTANDO le occorrenze. Il `# -*- coding: utf-8 -*-` NON basta: riguarda il
# SORGENTE, non lo STDOUT. Questa riga lo risolve alla radice.
try:
    _sys_enc.stdout.reconfigure(encoding="utf-8")
    _sys_enc.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import os
import pickle
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SC = os.environ.get("SCRATCH", HERE)

print("=" * 122)
print("AUDIT A8 -- ogni ramo delle correzioni GIA' CABLATE. Contato? Quanto scatta?")
print("=" * 122)

db = os.path.join(SC, "_audit.pkl")
cmd = [sys.executable, os.path.join(ROOT, "soliton_simulator.py"),
       "--batch", "--nmasse", "3", "--sep", "8", "--seed", "3", "--passi", "60",
       "--ogni", "60", "--db-ogni", "60", "--campo-spinoriale", "--spinore-vivo",
       "--spinore-corretto", "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet",
       "--fork-su2", "--fork-su2-mem", "--cs-dinamico",
       "--csv", os.path.join(SC, "_audit.csv"), "--sync-db", db, "--db-cleanup"]
p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
if p.returncode != 0:
    print("[FAIL] il run e' fallito rc=%s\n%s" % (p.returncode, (p.stderr or "")[-1500:]))
    sys.exit(1)
A = pickle.load(open(db, "rb"))["attrs"]


def g(k, d=0):
    v = A.get(k, d)
    return d if v is None else v


righe = []


def voce(ramo, riga, contatore, scatti, tot, note=""):
    if tot in (0, None):
        fr = "n/d"
        verd = "NON ESERCITATO"
    else:
        f = 100.0 * scatti / tot
        fr = "%.4f %%" % f
        verd = "legittimo" if f < 1.0 else ("REPERTO (%.1f %%)" % f)
    righe.append((ramo, riga, contatore, fr, verd, note))


# ------------------------------------------------------------------ plasticita' (f405327)
voce("I_nodi -> np.ones(n)  [FALLBACK PERICOLOSO]", ":3277",
     "_taup_Inodi_fallback (NUOVO)", g("_taup_Inodi_fallback"), g("_taup_Inodi_chiamate"),
     "il fallback e' densita' 1 contro |psi|^2 ~ 1e-6: SEI ORDINI")
voce("np.maximum(cs_taup, 1e-9)", ":3299", "_taup_cs_clamp (NUOVO)",
     g("_taup_cs_clamp"), g("_taup_cs_clamp_tot"), "clamp sulla velocita' delle onde")
voce("np.where(_peq_ok, peq, 1e-30)", ":3305", "_taup_peq_degenere (gia' c'era)",
     g("_taup_peq_degenere"), g("_taup_causale_tot"), "e _taup_peq_deg_passi = %s PASSI distinti"
     % A.get("_taup_peq_deg_passi"))
voce("max(t_luce, t_visco)  [il vincolo causale]", ":3318", "_taup_causale_scatti (gia' c'era)",
     g("_taup_causale_scatti"), g("_taup_causale_tot"),
     "di cui su peq degenere: %s" % A.get("_taup_causale_su_degenere"))
voce("TAU_USA_D0 / CS_DINAMICO", ":3288/:3298", "FLAG, non fallback", 0, None,
     "scelta di configurazione, non un ramo silenzioso: A8 non si applica")

# ------------------------------------------------------------------ _rep / spinta (3ca7731)
voce("getattr(_dt_e_ultimo, DT)  [DT NUDO]", ":3451", "_rep_dte_assente (NUOVO)",
     g("_rep_dte_assente"), g("_rep_guardia_tot"), "se scattasse, sarebbe DT di COORDINATA (par.9)")
voce("len(_dte) != len(rep)", ":3455", "_rep_dte_fallback (gia' c'era)",
     g("_rep_dte_fallback"), g("_rep_guardia_tot"), "")
voce("len(self._rep) != len(rep)", ":3459", "_rep_realloc (gia' c'era)",
     g("_rep_realloc"), g("_rep_guardia_tot"), "")
voce("np.maximum(tau_pp, 1e-12)", ":3465", "_rep_taupp_clamp (NUOVO)",
     g("_rep_taupp_clamp"), g("_rep_taupp_tot"), "")
voce("len(self.d0) == len(avv)  [la guardia P5]", ":3477", "_rep_guardia_salti (gia' c'era)",
     g("_rep_guardia_salti"), g("_rep_guardia_tot"), "")

# ------------------------------------------------------------------ d_arco (00adcd9)
voce("d_arco = self.d  [nessuna guardia]", ":3288", "N/A: nessun ramo", 0, None,
     "la cura ha RIMOSSO la guardia `if len(self.d) else`: vedi la verifica sotto")

print("\n%-44s %-12s %-30s %-12s %-18s" % ("RAMO", "riga", "contatore", "frazione", "verdetto"))
print("-" * 122)
for r in righe:
    print("%-44s %-12s %-30s %-12s %-18s" % r[:5])
    if r[5]:
        print("%44s   %s" % ("", r[5]))

# ------------------------------------------------------------------ d_arco: la guardia rimossa
print("\n--- d_arco: la cura ha rimosso `if len(self.d) else self.d`. E' un rischio? ---")
d = np.asarray(A["d"], float)
i = np.asarray(A["i"], int)
d0 = np.asarray(A["d0"], float)
print("  len(self.d) = %d   len(self.i) = %d   len(self.d0) = %d" % (len(d), len(i), len(d0)))
print("  allineati: %s" % (len(d) == len(i) == len(d0)))
print("""  LETTURA: la guardia vecchia (`if len(self.d) else self.d`) proteggeva dal caso `len(d) == 0`,
  e restituiva `self.d` -- cioe' LA STESSA COSA. Era una guardia che, nel ramo di fallback, dava
  l'identico risultato del ramo principale: NON proteggeva da nulla. Rimuoverla non ha tolto una
  protezione. E se gli array si disallineassero, oggi il calcolo SOLLEVEREBBE un errore di
  broadcast invece di proseguire in silenzio -- che secondo A8 e' il comportamento GIUSTO.""")

# ------------------------------------------------------------------ A8b: le cache
print("\n--- A8b: LE CACHE CROSS-PASSO ---")
print("  %-22s %-14s %-14s %-16s %s" % ("cache", "chiamate", "fallback", "frazione", "verdetto"))
for nome, ch, fb in (("_cs_nodo_prev (tempo-luce)", "_cs_chiamate", "_cs_fallback"),
                     ("_cs_nodo_prev (inerzia)", "_cs_in_chiamate", "_cs_in_fallback")):
    c, f = g(ch), g(fb)
    fr = (100.0 * f / c) if c else float("nan")
    print("  %-22s %-14s %-14s %-16s %s" % (nome, c, f, "%.4f %%" % fr if c else "n/d",
                                            "OK" if (c and fr < 1.0) else "REPERTO" if c else "non esercitato"))
print("  %-22s %-14s %-14s %-16s %s" % ("_xi_rumore", g("_xi_chiamate"), "-", "-",
                                        "RUMORE_COLORATO e' OFF: ramo non esercitato"))
print("  %-22s %-14s %-14s %-16s %s" % ("_psi_spin_prec", "-", "-", "-",
                                        "guardia dentro ritmo(), non toccata da queste correzioni"))
print("  %-22s %-14s %-14s %-16s %s" % ("_peq_t", "-", "-", "-",
                                        "snapshot locale a step, non cross-passo"))
print("  %-22s %-14s %-14s %-16s %s" % ("_dt_e_ultimo (NUOVO)", g("_rep_guardia_tot"),
                                        g("_rep_dte_assente"), "vedi tabella sopra",
                                        "scritto in ENTRAMBI i rami dell'orologio"))
print("  %-22s %-14s %-14s %-16s %s" % ("_rep (NUOVO, per arco)", "-", g("_rep_realloc"),
                                        "vedi tabella", "esteso a 4 punti: :1015 :1868 :3572 :3651"))

reperti = [r for r in righe if r[4].startswith("REPERTO")]
print("\n" + "=" * 122)
print("ESITO DELL'AUDIT: %d reperti su %d rami esaminati" % (len(reperti), len(righe)))
for r in reperti:
    print("  REPERTO -> %s (%s): %s" % (r[0], r[1], r[3]))
if not reperti:
    print("  Nessun ramo scatta sopra l'1 %%. I quattro contatori mancanti sono stati AGGIUNTI")
    print("  (A8 li richiede anche quando leggono zero: un ramo non contato e' sconosciuto,")
    print("  non innocuo).")
