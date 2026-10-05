# -*- coding: utf-8 -*-
"""LA PATCH DI `Z43` CURA (1): `r` va UNA VOLTA SOLA, e nella FREQUENZA no.

*(Il **braccio 0** del sigillo: applicata al blob di **prima** deve ridare il blob di
**oggi**, al byte.)*

### ⛔ **GLI HUNK VENGONO DAL DIFF VERO** *(`difflib`)*, non da cio' che credevo di
aver cambiato -- e il generatore ha ### **VERIFICATO la ricostruzione confrontando i
blob PRIMA di scrivere questo file.**

### ⚠ **DUE TENTATIVI SBAGLIATI, e li dichiaro perche' sono la ragione di questa
### forma:** `(1)` ancora = la riga **precedente** -> `else:` compare **42 volte**, e
un'ancora che non e' unica ### **non e' un'ancora** *(`P1-quater`)*; `(2)` ancora = la
riga sostituita, col blocco preso **camminando a ritroso** sui commenti -> ha incluso
### **commenti che c'erano GIA'**, e la ricostruzione ha dato `f8ce6859` invece di
`062172d3`.
### **La patch non e' cio' che credo di aver cambiato: e' cio' che E' cambiato.**

USO:  python csv/_seal_fork/_z43_cura1_patch.py <partenza> <uscita>
"""
import hashlib
import io
import sys

NL = chr(10)
BLOB_PRIMA = "1feb9b0a"
BLOB_DOPO = "062172d3"

# ### Ogni hunk: (etichetta, il VECCHIO testo, il NUOVO). Il vecchio e' ASSERITO
#   UNICO a ogni applicazione.
HUNK = [
    ("hunk 1 (insert)",
     NL.join([
    "            r_node = (np.asarray(dtn) / DT if not np.isscalar(dtn) else np.full(n, dtn / DT))",
     ]),
     NL.join([
    "            # [Z43 CURA (1), 2026-10-05] ⛔ `r_node` NON E' PIU' LETTO DA NESSUNO, e NON e'",
    "            #   un residuo da pulire: e' il RISULTATO della cura. Prima moltiplicava",
    "            #   `omega_clk` in ENTRAMBI i rami (`:5970` e `:5982`), e quello era il DOPPIO",
    "            #   CONTEGGIO di `r` -- la fase avanza di `omega_clk * _dts` con `_dts = DT*r`.",
    "            #   ⚠ CHI LA TOGLIE DEVE SAPERE CHE NON STA PULENDO: sta cancellando la traccia",
    "            #   di una legge che c'era. La decisione di Luca era <<si toglie `r_node` DALLA",
    "            #   FREQUENZA>>, non <<si toglie `r_node`>>: l'assegnazione resta, e questo",
    "            #   commento e' la ragione per cui resta.",
    "            #   E `r` vive dove deve: in `_dts`, cioe' nel TEMPO.",
    "            r_node = (np.asarray(dtn) / DT if not np.isscalar(dtn) else np.full(n, dtn / DT))",
     ])),
    ("hunk 2 (replace)",
     NL.join([
    "                omega_clk = (_num / np.maximum(_den, 1e-12)) * r_node   # coerenza d'arco [-1,1] * ritmo proprio",
     ]),
     NL.join([
    "                # [Z43 CURA (1), decisione di Luca del 2026-10-05] `r` VA UNA VOLTA SOLA.",
    "                # ⛔ PRIMA ERA `* r_node`, e la fase avanzava di `omega_clk * _dts` con",
    "                #   `_dts = DT*r`: quindi `r` AL QUADRATO. Un orologio avanza di FREQUENZA",
    "                #   PROPRIA per TEMPO PROPRIO -- contare il ritmo anche nella frequenza e'",
    "                #   contare lo stesso fattore DUE VOLTE (analisi dimensionale, non estetica).",
    "                # ⛔ IL MOTIVO E' MISURATO: il `BRACCIO A` del referto `66a798d` ha tolto",
    "                #   PROPRIO questo fattore su una copia, e l'altalena e' CROLLATA --",
    "                #   `|f|` da 5.283 a 1.034, `C0` da 7.185 a 1.031.",
    "                # `r` resta dov'e' deve stare: in `_dts`, qui sotto.",
    "                omega_clk = (_num / np.maximum(_den, 1e-12))   # coerenza d'arco [-1,1]",
     ])),
    ("hunk 3 (replace)",
     NL.join([
    "                omega_clk = (rho / max(rho_c, 1e-12)) * r_node          # legacy: densita' estensiva / rho_c globale",
     ]),
     NL.join([
    "                # [Z43 CURA (1)] LA STESSA CORREZIONE NEL RAMO LEGACY, e il mandato lo dice",
    "                # esplicitamente: <<e' la stessa legge>>. Qui il doppio conteggio passava",
    "                # per un'altra via -- `omega_tot += omega_clk*nb` e poi",
    "                # `theta = norm(omega_tot)*_dts` -- ma era LO STESSO ERRORE in due forme.",
    "                # ⚠ E VA DICHIARATO: QUESTO RAMO NON GIRA (`DEPARAM_OROLOGIO = True`),",
    "                #   quindi NESSUN SIGILLO PUO' MISURARE QUESTA RIGA GIRANDO. La sua cura e'",
    "                #   verificabile solo dall'AST e dalla lettura, NON da un numero.",
    "                omega_clk = (rho / max(rho_c, 1e-12))          # legacy: densita' / rho_c globale",
     ])),
]


def applica(t):
    """Ogni hunk si asserisce UNICO (`P1-quater`), uno alla volta."""
    for et, vecchio, nuovo in HUNK:
        n = t.count(vecchio)
        if n != 1:
            raise SystemExit("[FERMO] %s compare %d volte, non 1." % (et, n))
        t = t.replace(vecchio, nuovo, 1)
    return t


def main(argv):
    src, dst = argv[1], argv[2]
    b = hashlib.sha1(io.open(src, "rb").read()).hexdigest()[:8]
    print("  partenza: %s  (atteso %s)" % (b, BLOB_PRIMA))
    out = applica(io.open(src, encoding="utf-8").read())
    io.open(dst, "w", encoding="utf-8", newline=NL).write(out)
    bd = hashlib.sha1(io.open(dst, "rb").read()).hexdigest()[:8]
    print("  uscita:   %s  (atteso %s)   %s"
          % (bd, BLOB_DOPO, "COINCIDE" if bd == BLOB_DOPO
             else "### NON COINCIDE"))
    return 0 if bd == BLOB_DOPO else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
