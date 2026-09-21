# -*- coding: utf-8 -*-
"""DERIVAZIONE di `ANOM_SIMM` PRIMA di scriverla -- come chiede il mandato del 2026-09-21 §3②.

FORMA PROPOSTA:  anom = 2*(rho - peq) / (rho + peq)
FORMA IN VIGORE: anom = (rho - peq) / max(peq, 1e-9)                       (`:4215`)

⚠ NON e' un test: e' una DERIVAZIONE su casi limite, fatta da codice invece che a mano (`P1-ter`).
  I numeri del caso MISURATO vengono dalla rigiocata dal 1080, passo 1126, arco `3352-506`.
ASCII PURO.
"""
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

PAV = 1e-9


def vecchia(rho, peq):
    return (rho - peq) / max(peq, PAV)


def simm(rho, peq):
    den = rho + peq
    return float("inf") if den == 0.0 else 2.0 * (rho - peq) / den


CASI = [
    ("anomalia PICCOLA", 1.0e-1, 8.0e-2, "le due forme devono COINCIDERE"),
    ("anomalia GRANDE", 1.0e-1, 1.0e-2, "ancora vicine"),
    ("peq -> 0 (positivo)", 1.0e-1, 0.0, "il caso che la cura deve risolvere"),
    ("rho -> 0", 0.0, 1.0e-1, "limite inferiore"),
    ("0/0  rho = peq = 0", 0.0, 0.0, "il caso che il mandato chiede di trattare"),
    ("MISURATO: arco 3352-506", 1.32e-3, -4.85e-4, "peq NEGATIVO, passo 1126"),
    ("POLO: peq = -rho", 1.32e-3, -1.32e-3, "denominatore ESATTAMENTE zero"),
    ("oltre il polo", 1.32e-3, -1.4e-3, "il segno si ROVESCIA"),
]


def main():
    print("DERIVAZIONE DI `ANOM_SIMM` -- casi limite, generati da codice\n")
    print("%-28s %10s %11s | %14s %14s" % ("caso", "rho", "peq", "anom VECCHIA", "anom SIMM"))
    print("-" * 84)
    for nome, r, p, _ in CASI:
        print("%-28s %10.4g %11.4g | %14.4g %14.4g" % (nome, r, p, vecchia(r, p), simm(r, p)))

    print("""
--------------------------------------------------------------------------------
COSA DICE LA DERIVAZIONE -- TRE ESITI, e due sono OBIEZIONI

(1) LA FORMA SIMMETRICA FA CIO' CHE PROMETTE, DOVE `peq >= 0`.
    Per anomalie piccole coincide con la vecchia (0.25 contro 0.2222), e il caso che oggi
    esplode -- `peq -> 0` con `rho` ordinario -- passa da `1e+08` a ESATTAMENTE `+2`.
    Li' il pavimento `1e-9` diventa INUTILE, ed e' il punto della cura.

(2) ⚠ IL LIMITE `[-2, +2]` VALE SOLO SE `rho >= 0` **E** `peq >= 0`.
    `rho = 0.5*(I[i]+I[j])` con `I = |psi|^2` e' SEMPRE `>= 0`. **`peq` NO: Z94 lo misura
    NEGATIVO** (`-4.85e-04` al passo 1126). Allora il denominatore `rho + peq` SI ANNULLA in
    `peq = -rho`: **e' un POLO, non un limite.**
    * sul caso MISURATO la forma simmetrica vale **4.32**, cioe' GIA' FUORI da `[-2, +2]`;
    * al polo vale **infinito**;
    * oltre il polo vale **-68**: il SEGNO SI ROVESCIA.
    ⚠ **NON e' un'obiezione teorica: il punto in cui la forma si rompe e' ESATTAMENTE la
    regione che questa cura vuole coprire.**
    > **CONSEGUENZA SUL DISEGNO: le due cure NON sono indipendenti.** `ANOM_SIMM` e' corretta
    > **solo a valle** di una garanzia `peq >= 0` (`Z94`). Accesa da sola sostituirebbe un
    > pavimento con un polo.

(3) ⚠ IL CASO `0/0` E' UNA REGRESSIONE SE NON LO SI DEFINISCE.
    Oggi `rho = peq = 0` da' `0 / 1e-9 = 0`: il pavimento, per quanto arbitrario, DEFINISCE
    quel caso. La forma simmetrica da' `0/0`, cioe' **`nan`**.
    E NON e' un caso di scuola: l'arco `2773-4158` ha `rho = 1.38e-81` e archi di soli nodi
    NEONATI (`A7b`, `ramp = eta/TAU_A`) hanno `I` numericamente nulla.

    PROPOSTA, e NON introduce un pavimento scelto: **`0/0` si DEFINISCE ZERO**, come gia' fatto
    in questo stesso file per `scala_p` (`Z67`: *«`0/0` e' definito ZERO, dichiarato»*).
    E' una DEFINIZIONE, non una regolarizzazione: non c'e' nessun numero da scegliere, e il
    valore e' quello giusto -- dove non c'e' densita' non c'e' anomalia.
    FORMA:  `anom = where(rho + peq > 0, 2*(rho-peq)/(rho+peq), 0.0)`
    ⚠ e quel `> 0` (non `!= 0`) copre ANCHE il denominatore negativo -- ma lo copre
      MASCHERANDOLO, il che e' accettabile solo se `peq >= 0` e' gia' garantito. Senno' si
      sta zittendo il sintomo di (2).
--------------------------------------------------------------------------------""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
