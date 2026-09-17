# -*- coding: utf-8 -*-
"""SONDA: da dove viene il rapporto |feedback|/|coppia| = 2.706?  (mandato par.1)

LE TRE DOMANDE, e nessuna si risponde con un'ipotesi:
 1.1  E' un rapporto SENSATO o un artefatto di confronto (A3c)?
      - stessa POPOLAZIONE? (entrambe per-nodo, lunghezza n?)
      - stesso STATISTICO? (mediana di |.| con mediana di |.|)
      - `coppia` misurata a :3117 e' la coppia TOTALE o solo quella accumulata FIN LI'?
 1.2  Se e' vero, da COSA viene l'ampiezza? `imag(ov)` e' limitato a [-1, 1] per costruzione
      (overlap di spinori normalizzati), quindi l'ampiezza puo' venire solo da `w/grado`
      oppure dal fatto che `coppia` sia PICCOLA. Sono DIAGNOSI OPPOSTE.
      -> si riportano le DISTRIBUZIONI di |imag(ov)|, di w/grado, e di |coppia|.
 1.3  Dove e' applicato? `coppia += _fb` a :3129. Prima o dopo la divisione per l'inerzia?

⚠ E UNA COSA CHE SI VERIFICA QUI, NON SI ASSUME: `_spinor_lift` e' normalizzato? Se non lo e',
  `imag(ov)` NON e' limitato a [-1, 1] e la premessa 1.2 del mandato cade.

La sonda OSSERVA e DELEGA: avvolge il metodo, registra, e restituisce il valore originale.
Nessuna legge toccata, nessun RNG toccato.
ASCII PURO.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import _presidio                                    # PRESIDIO: encoding + timbro git (Z22)
_presidio.avvia(__file__)

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
sys.argv = ["soliton_simulator.py"]
import soliton_simulator as S

for _f in ("CS_DINAMICO", "CAMPO_SPINORIALE", "SPINORE_VIVO", "CHI_CORE",
           "FORK_SU2", "FORK_SU2_MEM", "SPINORE_CORRETTO", "SPIN_FEEDBACK"):
    setattr(S, _f, True)

print("=" * 118)
print("SONDA DEL 2.706 -- |feedback| / |coppia|")
print("=" * 118)

# ---------------------------------------------------------------- 1.3 DAL SORGENTE
src = open(os.path.join(ROOT, "soliton_simulator.py"), encoding="utf-8", errors="replace").read()
righe = src.splitlines()


def trova(frammento, da=0):
    for k in range(da, len(righe)):
        if frammento in righe[k].split("#")[0]:
            return k + 1
    return -1


print("\n--- (1.3) LA CATENA DI `coppia`, dal sorgente ---")
punti = [
    ("coppia = self._coppia_interferenza(A, z)", "la coppia PRINCIPALE"),
    ("coppia = coppia - fattore * dHdphi", "repulsione (ramo REPULS_LEGGE)"),
    ("coppia = coppia + MU_PSI * dHdphi", "vecchia repulsione (ramo elif, MORTO)"),
    ("_cm = float(np.median(np.abs(coppia)))", "<-- QUI si MISURA `coppia`"),
    ("coppia += _fb", "<-- QUI si APPLICA il feedback"),
    ("coppia = coppia + twist_nodo", "twist TW/Hall (DOPO la misura)"),
]
for fr, eti in punti:
    print("   :%-6s %-46s %s" % (trova(fr), fr[:44], eti))
k = trova("delta_phivel = dt_n_s * (coppia")
print("   :%-6s %s" % (k, righe[k - 1].strip()[:100] if k > 0 else "?"))
print("""
  LETTURA: `coppia` e `_fb` finiscono nella STESSA somma e attraversano la STESSA divisione.
  Il divisore e' `M_PH` (%s), una COSTANTE -- NON `inerzia`. Questo e' il settore della FASE
  (`phivel`), non quello dello SPIN (`omega_s`): la correzione dell'inerzia di sei ordini vive
  in `_passo_spinoriale` e NON tocca questa catena. La premessa del mandato su questo punto
  va corretta.""" % getattr(S, "M_PH", "?"))

# ---------------------------------------------------------------- la sonda
reg = []
orig_fb = S.Rete._feedback_spinoriale_archi
orig_ci = S.Rete._coppia_interferenza
ultimo = {"coppia": None}


def spia_ci(self, A, z):
    out = orig_ci(self, A, z)
    ultimo["coppia"] = np.asarray(out, float).copy()
    return out


def spia_fb(self, i, j, w):
    out = orig_fb(self, i, j, w)
    n = self.n
    lift = np.asarray(self._spinor_lift)
    if len(lift) < n or not S.SPIN_FEEDBACK:
        return out
    mask = (np.asarray(i) < n) & (np.asarray(j) < n)
    if not mask.any():
        return out
    ii, jj, ww = np.asarray(i)[mask], np.asarray(j)[mask], np.asarray(w)[mask]
    ov = np.sum(np.conj(lift[ii]) * lift[jj], axis=1)
    flusso = ww * np.imag(ov)
    grado = np.zeros(n)
    np.add.at(grado, ii, ww); np.add.at(grado, jj, ww)
    # NORMA del lift: se non e' 1, `imag(ov)` NON e' limitato a [-1, 1]
    norme = np.linalg.norm(lift[:n], axis=1) if lift.ndim == 2 else np.abs(lift[:n])
    cp = ultimo["coppia"]
    rec = dict(
        n=n, archi=int(mask.sum()),
        # popolazione e statistico
        len_out=len(out), len_coppia=(len(cp) if cp is not None else -1),
        out_zeri=int(np.sum(out == 0.0)),
        # 1.2 -- le tre distribuzioni
        ov_med=float(np.median(np.abs(np.imag(ov)))), ov_max=float(np.max(np.abs(np.imag(ov)))),
        w_med=float(np.median(ww)), w_max=float(np.max(ww)),
        gr_med=float(np.median(grado[grado > 0])) if np.any(grado > 0) else 0.0,
        wg_med=float(np.median(ww / np.maximum(grado[ii], 1e-9))),
        wg_max=float(np.max(ww / np.maximum(grado[ii], 1e-9))),
        fb_med=float(np.median(np.abs(out))), fb_max=float(np.max(np.abs(out))),
        cp_med=(float(np.median(np.abs(cp))) if cp is not None else float("nan")),
        cp_max=(float(np.max(np.abs(cp))) if cp is not None else float("nan")),
        lift_norma_min=float(np.min(norme)), lift_norma_max=float(np.max(norme)),
        # F3 in anticipo: la somma del feedback e' zero? (antisimmetria)
        somma=float(np.sum(out)), scala=float(np.max(np.abs(out))) if len(out) else 0.0,
    )
    reg.append(rec)
    return out


S.Rete._feedback_spinoriale_archi = spia_fb
S.Rete._coppia_interferenza = spia_ci

# scena del batch, la stessa dell'esperimento
r = S.Rete(5)
r.semina(80)
for _ in range(6):
    S.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
Nc = S.N_CRITICO() if callable(getattr(S, "N_CRITICO", None)) else 200
for k in range(3):
    ang = 2 * np.pi * k / 3
    r.nuova_massa(int(Nc * 0.6), raggio=S._size_video(k, 0.8),
                  centro=(8.0 * np.cos(ang), 8.0 * np.sin(ang), 0.0), fase=0.0)
r.aggiorna_pesi_concorrenza()
for kk in range(60):
    S.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()

if not reg:
    print("\n  NESSUNA invocazione osservata: la sonda non ha misurato nulla.")
    sys.exit(1)

# ---------------------------------------------------------------- 1.1 popolazione e statistico
print("\n--- (1.1) STESSA POPOLAZIONE? STESSO STATISTICO? ---")
a = reg[-1]
print("  len(feedback) = %d   len(coppia) = %d   n = %d   -> stessa lunghezza: %s"
      % (a["len_out"], a["len_coppia"], a["n"], a["len_out"] == a["len_coppia"] == a["n"]))
print("  entrambe per-NODO, entrambe misurate con `median(|.|)`: stesso statistico.")
zz = [x["out_zeri"] for x in reg]
print("  nodi con feedback ESATTAMENTE zero: mediana %d su %d  (%.2f %%)"
      % (int(np.median(zz)), a["n"], 100.0 * np.median(zz) / max(a["n"], 1)))
print("  -> se molti nodi hanno feedback zero, la MEDIANA del feedback e' abbassata, non alzata:")
print("     l'artefatto andrebbe nella direzione di SOTTOSTIMARE il rapporto, non di gonfiarlo.")

print("\n  LA NORMA DEL LIFT (se non e' 1, `imag(ov)` non e' limitato a [-1,1]):")
print("     min %.6f   max %.6f   su %d invocazioni"
      % (min(x["lift_norma_min"] for x in reg), max(x["lift_norma_max"] for x in reg), len(reg)))

# ---------------------------------------------------------------- 1.2 le tre distribuzioni
print("\n--- (1.2) DA COSA VIENE L'AMPIEZZA? Le tre distribuzioni ---")
print("  %-8s %-13s %-13s %-13s %-13s %-13s" %
      ("passo", "|imag(ov)| med", "w/grado med", "|feedback| med", "|coppia| med", "rapporto"))
for k in (0, 1, len(reg) // 4, len(reg) // 2, len(reg) - 1):
    x = reg[k]
    rap = x["fb_med"] / x["cp_med"] if x["cp_med"] > 0 else float("nan")
    print("  %-8d %-13.5g %-13.5g %-13.5g %-13.5g %-13.5g"
          % (k, x["ov_med"], x["wg_med"], x["fb_med"], x["cp_med"], rap))
rr = [x["fb_med"] / x["cp_med"] for x in reg if x["cp_med"] > 0]
print("\n  rapporto MEDIO su %d invocazioni : %.5g    (riferimento del referto: 2.706)"
      % (len(rr), float(np.mean(rr))))
print("  |imag(ov)| mediana, su tutto      : %.5g   max %.5g   <- limitato a [0,1]?"
      % (float(np.median([x["ov_med"] for x in reg])), max(x["ov_max"] for x in reg)))
print("  w/grado    mediana, su tutto      : %.5g   max %.5g"
      % (float(np.median([x["wg_med"] for x in reg])), max(x["wg_max"] for x in reg)))
print("  |coppia|   mediana, su tutto      : %.5g   max %.5g"
      % (float(np.median([x["cp_med"] for x in reg])), max(x["cp_max"] for x in reg)))
print("  |feedback| mediana, su tutto      : %.5g   max %.5g"
      % (float(np.median([x["fb_med"] for x in reg])), max(x["fb_max"] for x in reg)))
print("""
  COME SI DISTINGUONO LE TRE DIAGNOSI -- il valore sotto ipotesi nulla:
    se `imag(ov)` fosse in media ~0.5 (spinori scorrelati) e w/grado ~1/grado, il feedback
    varrebbe ~0.5/grado. Con grado ~4-6 sarebbe ~0.1. Se il rapporto e' grande CON un feedback
    di quell'ordine, allora e' `coppia` a essere piccola -- e il fatto NON e' sul feedback.""")

# ---------------------------------------------------------------- F3 in anticipo
print("\n--- (bonus, e' il futuro F3) LA SOMMA DEL FEEDBACK E' ZERO? (antisimmetria, A7) ---")
rel = [abs(x["somma"]) / max(x["scala"], 1e-300) for x in reg if x["scala"] > 0]
print("  |sum(out)| / max|out| :  mediana %.3e   MAX %.3e   su %d invocazioni"
      % (float(np.median(rel)), float(np.max(rel)), len(rel)))
print("  (se la forma e' antisimmetrica per costruzione, deve stare all'errore macchina ~1e-14)")

print("\n" + "=" * 118)
