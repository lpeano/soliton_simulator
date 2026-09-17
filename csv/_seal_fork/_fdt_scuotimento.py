# -*- coding: utf-8 -*-
"""FDT DELLO SCUOTIMENTO — il rumore porta con se' una dissipazione ALLINEANTE?

Vedi `doc/PREDIZIONE_fdt_scuotimento.md` (scritta e committata PRIMA di questo script).

NON tocca `soliton_simulator.py`: lo IMPORTA per usarne le costanti e riprodurne ESATTAMENTE le
due operazioni sotto esame, cosi' come sono scritte nel sorgente:

    scuotimento  (`:1803-1804`)  n -> (n + amp*g) / |n + amp*g|      g ~ N(0, I_3) per componente
    precessione  (`:2021`)       n -> n cos(th) + (u x n) sin(th) + u (u.n)(1 - cos th)   [Rodrigues]

TEST
  3a  solo rumore + normalizzazione       -> allinea, isotropizza, o resta?
  3b  precessione + rumore + normaliz.    -> l'accoppiamento ai vicini (via B) cambia la risposta?
  3c  verifica dell'ESPANSIONE ANALITICA  -> E[n'] - n a O(amp^2): il numerico deve coincidere.

Riferimenti stampati SEMPRE accanto al misurato: allineato = 0 gradi, isotropo = 90.000 gradi
(media della densita' sin(chi)/2), antipodale = 180.
PURE-READ: seed fisso, nessuna scrittura, nessun effetto sul simulatore.
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
import sys

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
os.chdir(ROOT)
sys.path.insert(0, ROOT)
sys.argv = ["soliton_simulator.py"]
import soliton_simulator as S  # noqa: E402

SEED = 20260914
ISO = 90.0          # media di chi per direzioni casuali indipendenti


def norm(v):
    return v / np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), 1e-30)


def scuoti(n, amp, g):
    """ESATTAMENTE `:1803-1804`: somma rumore gaussiano isotropo, poi normalizza."""
    return norm(n + amp * g)


def precedi(n, omega, dt):
    """ESATTAMENTE `:2016-2021` (Rodrigues): ruota n ATTORNO a omega. Conserva |n| e l'angolo n-omega."""
    on = np.linalg.norm(omega, axis=-1, keepdims=True)
    u = omega / np.maximum(on, 1e-9)
    ang = on * dt
    cA, sA = np.cos(ang), np.sin(ang)
    dot = np.sum(u * n, axis=-1, keepdims=True)
    return n * cA + np.cross(u, n) * sA + u * dot * (1.0 - cA)


def ang_deg(a, b):
    return np.degrees(np.arccos(np.clip(np.sum(a * b, axis=-1), -1.0, 1.0)))


print("=" * 100)
print("FDT DELLO SCUOTIMENTO — il rumore contiene una dissipazione allineante?")
print("=" * 100)
print("RIFERIMENTI:  allineato = 0.000 gradi   |   isotropo = %.3f gradi   |   antipodale = 180" % ISO)
print("Costanti dal simulatore: DT = %.4g, LAM = %.4g, CS_M = %.4g" % (S.DT, S.LAM, S.CS_M))

# ---------------------------------------------------------------- 3c: l'ESPANSIONE ANALITICA
print()
print("=" * 100)
print("TEST 3c — l'espansione analitica a O(amp^2) regge?")
print("=" * 100)
print("""  Sviluppo di n' = (n + a g)/|n + a g| con g ~ N(0, I_3), mediato su g:
    |n+ag|^-1 = 1 - a s - a^2 G/2 + (3/2) a^2 s^2 + O(a^3)     con s = n.g , G = |g|^2
    n'        = n + a g - a s n - a^2 s g - a^2 (G/2) n + (3/2) a^2 s^2 n + O(a^3)
  Medie: E[g] = 0, E[s] = 0, E[s g] = n, E[G] = 3, E[s^2] = 1  ->

      E[n'] - n  =  -a^2 n  +  O(a^3)          <--- IL DRIFT

  Cioe': (i) il drift e' PARALLELO a n, nessuna componente trasversa -> nessuna rotazione media;
         (ii) dipende dal SOLO n: nessuna traccia dei vicini;
         (iii) |E[n']| = 1 - a^2 : e' la CONTRAZIONE DEL RISULTANTE, cioe' DIFFUSIONE PURA.""")
g0 = np.random.default_rng(SEED)
print("\n   amp      |E[n']| misurato   atteso 1 - amp^2    |differenza|   componente TRASVERSA")
for amp in (0.3, 0.1, 0.03, 0.013):
    n0 = norm(g0.normal(size=3))
    M = 4000000
    gg = g0.normal(size=(M, 3))
    npr = scuoti(n0[None, :], amp, gg)
    m = npr.mean(axis=0)
    par = float(np.dot(m, n0))
    trasv = float(np.linalg.norm(m - par * n0))
    err_stat = 1.0 / np.sqrt(M)
    print("  %6.3f      %.8f        %.8f      %.2e       %.2e  (err.stat. %.1e)"
          % (amp, float(np.linalg.norm(m)), 1.0 - amp ** 2,
             abs(float(np.linalg.norm(m)) - (1.0 - amp ** 2)), trasv, err_stat))
print("""
  LETTURA: |E[n']| segue 1 - amp^2 e la componente TRASVERSA e' al livello dell'errore statistico.
  L'espansione e' confermata: il drift e' radiale, cioe' NON e' un moto sulla sfera. Sulla sfera il
  drift a O(amp^2) e' NULLO: il rumore+normalizzazione e' DIFFUSIONE ISOTROPA PURA.""")

# ---------------------------------------------------------------- 3a: solo rumore
print()
print("=" * 100)
print("TEST 3a — SOLO rumore + normalizzazione: due Bloch a 60 gradi, molti passi")
print("=" * 100)
g = np.random.default_rng(SEED)
M = 200000
th0 = np.radians(60.0)
a_vuoto = 0.013     # amp misurata nel vuoto (doc/INDAGINE_scuotimento.md §3)
nA = np.tile(np.array([0.0, 0.0, 1.0]), (M, 1))
nB = np.tile(np.array([np.sin(th0), 0.0, np.cos(th0)]), (M, 1))
print("  amp = %.4g (quella misurata nel vuoto).  Atteso analitico per l'angolo:" % a_vuoto)
print("  diffusione pura -> <cos chi> decade come (1-amp^2)^(2k) e chi -> %.3f gradi (isotropo)" % ISO)
print("\n   passo    chi medio (gradi)    <cos chi>     atteso (1-amp^2)^(2k) * cos(60)")
for k in range(0, 3001):
    if k in (0, 10, 50, 100, 300, 1000, 2000, 3000):
        cc = float(np.mean(np.sum(nA * nB, axis=1)))
        att = (1.0 - a_vuoto ** 2) ** (2 * k) * np.cos(th0)
        print("  %6d      %8.3f          %+.6f        %+.6f" % (k, np.degrees(np.arccos(np.clip(cc, -1, 1))), cc, att))
    if k == 3000:
        break
    nA = scuoti(nA, a_vuoto, g.normal(size=(M, 3)))
    nB = scuoti(nB, a_vuoto, g.normal(size=(M, 3)))
print("""
  LETTURA: l'angolo SALE da 60 verso 90 (isotropo). NON scende verso 0. Nessun allineamento.
  E <cos chi> segue la legge della diffusione pura, coerente con 3c.""")

# ---------------------------------------------------------------- 3b: precessione + rumore
print()
print("=" * 100)
print("TEST 3b — PRECESSIONE (Rodrigues, campo B dai vicini) + rumore + normalizzazione")
print("=" * 100)
print("""  Due nodi vicini: ciascuno precede attorno al campo dell'ALTRO (B_A = k*nB, B_B = k*nA), che e'
  la forma del campo nel codice (somma pesata dei Bloch dei vicini). E' QUI che l'accoppiamento ai
  vicini esiste: se una dissipazione allineante emerge, emerge da questa combinazione.""")
for kB in (0.5, 2.0, 10.0):
    for amp in (0.0, 0.013):
        g = np.random.default_rng(SEED)
        M = 200000
        nA = np.tile(np.array([0.0, 0.0, 1.0]), (M, 1))
        nB = np.tile(np.array([np.sin(th0), 0.0, np.cos(th0)]), (M, 1))
        traccia = []
        for k in range(2001):
            if k in (0, 100, 500, 1000, 2000):
                traccia.append(float(np.mean(ang_deg(nA, nB))))
            if k == 2000:
                break
            BA = kB * nB
            BB = kB * nA
            nA2 = precedi(nA, BA, S.DT)
            nB2 = precedi(nB, BB, S.DT)
            if amp > 0:
                nA2 = scuoti(nA2, amp, g.normal(size=(M, 3)))
                nB2 = scuoti(nB2, amp, g.normal(size=(M, 3)))
            nA, nB = nA2, nB2
        mod_n = float(np.linalg.norm(0.5 * (nA.mean(axis=0) + nB.mean(axis=0))))
        print("  |B|=%5.1f amp=%.3f | chi ai passi 0/100/500/1000/2000: %s | |<n>| finale = %.4f"
              % (kB, amp, " ".join("%7.3f" % t for t in traccia), mod_n))
print("""
  LETTURA (CORRETTA il 2026-09-14 DOPO aver visto i dati: la prima versione di questa riga diceva
  "con amp=0 la precessione CONSERVA l'angolo esattamente" ed era FALSA. L'avevo scritta prima di
  girare, ed e' proprio il commento stale contro cui mette in guardia il par.0 di CLAUDE.md.)

  Rodrigues conserva l'angolo fra UN vettore e il SUO asse. Ma qui i due nodi ruotano l'uno attorno
  all'altro SIMULTANEAMENTE: la coppia (nA, nB) NON e' angolo-conservante, ed e' un sistema
  dinamico non lineare a se'. Infatti con amp = 0 (rumore SPENTO) l'angolo si muove eccome:
       |B| = 0.5  ->  60 -> 62.5 gradi     (deriva lenta)
       |B| = 2.0  ->  60 -> 104.2 gradi    (supera l'isotropo)
       |B| = 10.0 ->  60 -> 180.000 gradi  (ANTIPODALE esatto)
  Cioe': la precessione mutua non e' neutra, e' ATTIVAMENTE DISORDINANTE, e a campo forte ha un
  punto fisso ANTI-allineante a chi = 180.

  IL VERDETTO NON CAMBIA, anzi si rafforza: in nessuna configurazione chi scende verso 0. Non solo
  manca il "tira verso" (dissipazione allineante): c'e' uno "spinge via". La combinazione
  precessione + rumore NON produce alcuna dissipazione allineante.""")
print("=" * 100)
