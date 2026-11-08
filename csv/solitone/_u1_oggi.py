# -*- coding: utf-8 -*-
r"""**IL PROTOTIPO `U(1)` SUL TICK DI OGGI** *(Luca `2026-11-07` `12:52`, l'alternativa (a); il task history `doc/TASK_HISTORY/2026-11-07_u1_prototipo_verificato.md`, T2)*

### **RIPRESO, NON RISCRITTO:** **`Campo`, `scrivi_U`, `avvolto`, `tick_campo`, `rovescia` vengono da `_u1_prototipo`** *(`PROGETTO_U1.md` sez. `4`-`6`)*:
il campo `A`, `E` per arco fuori da `stato.py`; il leapfrog in due mezzi pezzi reversibili *(la spinta a meta' ai due estremi del tick, la deriva dopo il PRIMO
`spostamento_scalare`, al centro del palindromo)*; ### **la sorgente `J_a = |v0'|^2 - |v0|^2`, `E <- E - e J`** *(Ampere discreta, dentro `spostamento_trasporto`)*;
`U_a = e^{i e A_a} I` *(`V_a = I`)*; **il tempo d'arco `F1`** *(la decisione di Luca dopo `u1_secondo`: `w = s_a^2 l / l*`)*; ### **il compatto E il non compatto,
DICHIARATI per argomento** *(`forma`: `"compatto"` o `"noncompatto"`, nessun valore predefinito)*.

### **CIO' CHE QUI E' NUOVO** *(la premessa `3` del task history: il prototipo girava SENZA `CAMM-MATERIA-VUOTO` e sul vuoto NULLO)*:
- **`tick(z, t, K, campo, sorgente)`:** ### **il tick INTERO della corsa** *(`accensione.tick`: `percorri_tick` con le `14` posizioni)* **avvolto**, ### **solo dopo la rampa**
  *(`t >= K`: nella rampa la corsa usa `tick_acceso`, un altro percorso -- ALZA invece di avvolgerlo)*; **il chiamante apre `SF.forma(VC.FORMA)` e `BE.conv(DC.ZERO)`**, come la corsa;
- **`scena(e, forma)`:** ### **la scena della corsa** *(`V.scena` col vuoto della corsa, `V.partenza`, `P.e_K`: le chiamate di `corsa_accensione.ripartenza`)* **col campo `A = E = 0`
  costruito sui SUOI archi** *(`Campo` controlla che siano `a1`, `a2`, `a1 + a2`: se no ALZA)*.

### ⛔ **`e` NON HA UN VALORE QUI:** **e' un argomento obbligatorio** *(`A1`: lo sceglie Luca, la domanda T6)*; **le prove di T3 e T4 lo prendono come parametro DICHIARATO e controllano di non dipenderne.**
### ⛔ **Il nucleo non si tocca:** `mot.operatori` e `mot.geo.U` sono avvolti in memoria e **rimessi all'uscita** *(`avvolto`)*.
"""
import contextlib
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)   # ### dal 2026-11-08 in csv/solitone/ (la cassetta, D6: nessuno script FUORI importa la libreria); _u1_prototipo e gli strumenti in csv/
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import _u1_prototipo as U1  # noqa: E402  (Campo, scrivi_U, avvolto, tick_campo, rovescia: RIPRESI)

Campo = U1.Campo
scrivi_U = U1.scrivi_U
avvolto = U1.avvolto
tick_campo = U1.tick_campo
rovescia = U1.rovescia
FORME = U1.FORME


def tick(z, t, K, campo, sorgente):
    """### **Un tick della corsa col campo:** `spinta(1/2)`, il tick INTERO avvolto *(la sorgente se `sorgente`)*, `spinta(1/2)`. ### **Solo `t >= K`.**"""
    from solitone import accensione as AC
    assert t >= K, ("il tick %d e' nella rampa (K %d): la corsa la' usa tick_acceso, un altro percorso, e l'innesto del campo NON e' collaudato su quello" % (t, K))
    assert isinstance(sorgente, bool), "`sorgente` va dato esplicito (True o False)"
    campo.spinta(0.5)
    with avvolto(z["mot"], campo, sorgente):
        AC.tick(z, t, K)
    campo.spinta(0.5)


def campo_della_scena(z, e, forma):
    """### **Il campo `A = E = 0` sugli archi della scena** *(`ii`, `jj` dalle estremita': l'arco `a` ha le estremita' `2a` e `2a + 1`)*, **`s_a` il tempo d'arco del passo** *(`FP.s_arco`)*."""
    import flussi_parziali as FP
    assert forma in FORME, "la forma del campo va dichiarata: %s" % (FORME,)
    inc, mot = z["inc"], z["mot"]
    L = int(z["L"])
    ii, jj = inc.nodo[0::2].astype(np.int64), inc.nodo[1::2].astype(np.int64)
    s_a = FP.s_arco(mot).copy()
    campo = Campo(ii, jj, (L, L), float(e), forma, s_a)
    scrivi_U(mot, campo)
    return campo


@contextlib.contextmanager
def scena(e, forma):
    """### **La scena della corsa** *(le chiamate di `corsa_accensione.ripartenza`)* **col campo:** `(z, campo, K, s)`; ### **`mot.geo.U` rimesso a `I` all'uscita.**"""
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import corsa_accensione as CA
    from solitone import protetto as P
    sol, vuoto, s = V.CORSE[CA.NOME]
    K = int(round(CA.CORSE["TB3"][0] / s))
    with V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        P.e_K(z)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        for k, v in salvato.items():
            z["st"][k][...] = v
        U0 = z["mot"].geo.U.copy()
        assert float(np.max(np.abs(U0 - np.eye(2)[None, :, :]))) == 0.0, "la scena NON ha U = I: il campo partirebbe da un'altra U"
        campo = campo_della_scena(z, e, forma)
        try:
            yield z, campo, K, s
        finally:
            z["mot"].geo.U[...] = U0
