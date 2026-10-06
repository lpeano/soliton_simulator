# -*- coding: utf-8 -*-
"""IL RAMO CHE ESCE con **<<VIA IL `0.3`>>** -- `MITOSI-SOGLIA-GRAD`.

*(Decisione di Luca del 2026-10-06. Il ragionamento e' in
`doc/TASK_HISTORY/2026-10-06_via-il-03-mitosi-soglia-grad.md`; la patch e'
`csv/_seal_fork/_mitosi_soglia_grad_via_patch.py`; il sigillo
`csv/_seal_fork/_sigillo_mitosi_soglia_grad_via.py`.)*

### ⛔ **QUESTO FILE NON GIRA E NON SI IMPORTA: e' un ARCHIVIO.**
### I due blocchi sono copiati **VERBATIM** dal blob del PADRE `71eddc4b~1`
### *(preso con `git cat-file -p`, **in binario** -- mai `git checkout`, per la
### trappola `CRLF` del `par.7`)*, e la copia e' **verificata**: ciascuno compare
### **esattamente UNA volta** in quel blob.

**SI RILANCIA dal tag `pre-mitosi-soglia-grad-via`.**

**IL PERCHE' E' USCITO, misurato** *(referto `27c10bd`, `1000` passi, due bracci)*:
`R = 0.1616` sulle divisioni e `0.3417` sulla popolazione nella finestra, quindi
**la crescita NON era creata dalla modulazione**; e **senza di lei la crescita e'
STABILE** *(`48`-`150` nascite ogni `100` passi)* mentre **con lei ACCELERA fino a
`1044`**. **Non una differenza di quantita': una differenza di FORMA.**
"""

# ============================================================ IL BLOCCO (1)
# LA MODULAZIONE DELLA SOGLIA, in `decidi_divisione`. Leggeva `|r_i - r_j|`, il
# gradiente del tempo proprio lungo l'arco, e abbassava la soglia fino al ~30%.
MODULAZIONE = '''
        if TORS_4PI and len(self.i) == len(avv):
            # gradiente di tempo proprio LUNGO l'arco: differenza del tempo proprio nodale
            # fra i due estremi. tau_nodo alto = tempo lento = materia. Dove il gradiente
            # e' forte, la soglia si abbassa (la mitosi e' agevolata verso il tempo lento).
            # [CURA 2 STRUTTURALE, 2026-09-27] IL RAMO `if TEMPO_UNICO_MITOSI:` E' STATO TOLTO: la legge e' SEMPRE questa.
            #   Il ramo `else` e' ARCHIVIATO in `csv/_archivio/rami_off_cura2.py` e si rilancia dal tag `pre-cura2-strutturale`.
            # [CURA 2] IL GRADIENTE DI TEMPO SI PRENDE DALL'OROLOGIO, non da `|tw|`.
            # Il commento qui sopra dice "gradiente di TEMPO PROPRIO", ma `tau_nodo` e'
            # `1 + mean(|tw|)/PHI_CRIT`, cioe' ESATTAMENTE la formula del ramo
            # `TEMPO_SEGNO` di `ritmo()` -- CHE NON GIRA (`TEMPO_SEGNO = False` in 9 run
            # su 11, `Z130`). Intenzione TEMPO, implementazione TORSIONE.
            # SI PRENDE `r` E NON `1/r`, e la ragione e' un conto, non una preferenza:
            #   r    in [1.4142e-6, 1.4142]  -> tanh(grad) <= 0.8884 -> la soglia MODULA
            #   1/r  in [0.707, 707107]      -> tanh(grad) -> 1 ESATTO -> la modulazione
            #                                   diventerebbe un RISCALAMENTO COSTANTE
            #                                   della soglia, cioe' un PARAMETRO NASCOSTO
            #                                   (`A1`), e `A11` cor.6 dice che un limite
            #                                   che satura e' un allarme.
            _rn = self._r_nodo_mitosi()
            # `grad_modula` qui e' il gradiente di `r`: IL TEMPO PROPRIO VERO.
            grad_modula = np.abs(_rn[self.i] - _rn[self.j])
            # modulazione limitata: la soglia scende di al piu' ~30% dove il gradiente e' forte
            soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_modula))
'''

# ============================================================ IL BLOCCO (2)
# `_r_nodo_mitosi`, l'orologio per NODO che la modulazione leggeva. Dopo il blocco
# (1) restava SENZA CHIAMANTI nel simulatore, e con lei escono i quattro contatori
# `A8` `_tum_r_tot`, `_tum_r_salti`, `_tum_r_forma`, `_tum_r_quando`.
FUNZIONE = '''
    def _r_nodo_mitosi(self):
        """L'OROLOGIO per NODO, per il gradiente di tempo della mitosi. Guardia CONTATA (`A8`).

        Il fallback e' `1` = "nessuna dilatazione", **la stessa convenzione che `ritmo()` usa
        quando non c'e' un passato** (`np.ones`): non una convenzione nuova.
        `_r_corrente` e' un array PER NODO attraversato da un punto di crescita, cioe' la
        classe `A8b` di `_cs_nodo_prev` (71.88 %) e `_psi_spin_prec` (95.33 %): si contano
        QUATTRO cose, non una -- invocazioni, salti, la FORMA al fallimento, e QUANDO.
        """
        n = self.n
        self._tum_r_tot = getattr(self, "_tum_r_tot", 0) + 1
        r = getattr(self, "_r_corrente", None)
        if r is None or len(r) < n:
            self._tum_r_salti = getattr(self, "_tum_r_salti", 0) + 1
            self._tum_r_forma = (-1 if r is None else len(r), n)
            self._tum_r_quando = self._tum_r_tot
            return np.ones(n)
        return np.asarray(r, dtype=float)[:n]
'''

# ### ⚠ **E CINQUE STRUMENTI VIVI LEGGEVANO `_tum_r_*`:**
#   `_riverifica_t4`, `_sig_decisione_separata`, `_m7_potenza_termostato`,
#   `_soglia_alla_divisione`, `_referto_cura2`. ### **Restano legati ai blob
#   vecchi**, e si rigirano col `git checkout` del commit che ha sigillato
#   (`par.6`). ### **Non e' un difetto: il difetto sarebbe un sigillo non piu'
#   ri-girabile AL SUO COMMIT.**
