# -*- coding: utf-8 -*-
"""**ARCHIVIO: `SYNC_UPDATE` e i suoi rami parziali, usciti il 2026-09-27.**

**NON GIRA E NON SI IMPORTA.** E' il testo dei blocchi rimossi, **estratto dall'AST del
file mentre veniva modificato** -- non ricopiato a mano.

**DA DOVE VIENE:** tag **`pre-archivio-sync`**, simulatore blob sha1-BYTE **`f845d30d`**.
Per rileggere l'originale intero:

    git cat-file -p pre-archivio-sync:soliton_simulator.py

**PERCHE' E' USCITO** *(passo `(b)2` di `ETC-PASSO`, decisione di Luca)*: il suo RAGGIO era
**una legge su cinque**. Misurato nella FASE 0: `7` usi in `_passo_spinoriale`, `6` in
`step`, e **ZERO** in `scuoti_vuoto`, `mitosi`, `rilassa_disegno`, `memoria_hebbiana_moto`.
**Prometteva Jacobi e lo dava a un quinto del passo**, e la cura `ETC-PASSO` lo rimpiazza
sul passo INTERO. `--sync` **resta accettato** come no-op che si dichiara.
"""

raise SystemExit(__doc__)   # non si importa e non si gira: e' un ARCHIVIO


# ==========================================================================
# in `_passo_spinoriale`:  if SYNC_UPDATE
# azione: via  --  le copie nb_t/nb_prec_t/omega_t della snapshot spinoriale
# righe 3172-3177 del blob f845d30d
# ==========================================================================
_ARCHIVIO_passo_spinoriale_3172 = r"""
        if SYNC_UPDATE:
            nb_t = self._nb.copy()
            nb_prec_t = (self._nb_prec.copy()
                         if hasattr(self, "_nb_prec") and self._nb_prec is not None
                         and len(self._nb_prec) == n else nb_t.copy())
            omega_t = self.omega_s.copy()
"""

# ==========================================================================
# in `_passo_spinoriale`:  if SCUOTIMENTO and (not SYNC_UPDATE)
# azione: togli-test  --  lo scuotimento del vuoto sullo spinore: resta SEMPRE attivo
# righe 3177-3227 del blob f845d30d
# ==========================================================================
_ARCHIVIO_passo_spinoriale_3177 = r"""
        if SCUOTIMENTO and not SYNC_UPDATE:
            Lam = lambda_vuoto(self)
            if Lam > 0:
                if not hasattr(self, "psi") or len(self.psi) < n:
                    self.calcola_psi()
                I2 = np.abs(self.psi[:n]) ** 2
                amp = np.sqrt(Lam) / (1.0 + I2 / Lam)   # sqrt(Lam)/(1+|Psi|^2/Lam): come lo scalare
                _g = self.rng.normal(0, 1.0, (n, 3))
                if RUMORE_COLORATO:
                    # TAGLIO SPETTRALE: il calcio non e' piu' indipendente fra un passo e l'altro,
                    # ma correlato su `tau_c = LAM/CS_M` (il tempo-luce del solitone, DERIVATO).
                    # `dt_n`, non `DT`: processo LOCALE, altrimenti frame preferito (par.9).
                    _tauc = LAM / max(CS_M, 1e-12)
                    _dtl = dt_n if np.isscalar(dt_n) else np.asarray(dt_n, float)[:n]
                    # VALORE ASSOLUTO, e non e' pignoleria: `_passo_spinoriale` riceve `dt_n_s`,
                    # che sotto `--tempo-segno` (MOD 5.3a, Feynman-Stuckelberg) puo' essere
                    # NEGATIVO per l'antimateria. Con `dt_n < 0` verrebbe `a > 1` e la ricorsione
                    # DIVERGEREBBE IN SILENZIO. Il tempo di correlazione e' una durata, quindi
                    # dipende dal MODULO del tic, non dal suo verso. Nessun numero nuovo.
                    _a = np.exp(-np.abs(_dtl) / _tauc)
                    _b = np.sqrt(np.maximum(1.0 - _a * _a, 0.0))
                    _xi = getattr(self, "_xi_rumore", None)
                    self._xi_chiamate = getattr(self, "_xi_chiamate", 0) + 1
                    if _xi is None or len(_xi) < n:
                        # ESTRAZIONE FRESCA DALLA DISTRIBUZIONE STAZIONARIA (N(0,1)) PER I NODI
                        # NUOVI. Zero transitorio, zero parametri: partire da zero darebbe un
                        # primo calcio attenuato di b = sqrt(1-a^2), cioe' un artefatto.
                        # [2026-09-16] QUESTO NON E' UN FALLBACK: E' IL PERCORSO NORMALE della
                        # mitosi. `xi` e' l'AMBIENTE, non una proprieta' del nodo, quindi il
                        # figlio NON lo eredita (vedi `_eredita_spinore_figli`). I nodi ESISTENTI
                        # conservano il proprio `xi` - il `vstack` tiene la testa intatta - e solo
                        # i NUOVI ricevono un campione fresco, perche' un nodo appena nato non ha
                        # un passato del rumore che lo ha spintonato.
                        self._xi_esteso = getattr(self, "_xi_esteso", 0) + 1
                        self._xi_nuovi = (getattr(self, "_xi_nuovi", 0)
                                          + max(n - (0 if _xi is None else len(_xi)), 0))
                        _base = np.asarray(_xi, float) if _xi is not None else np.zeros((0, 3))
                        _manca = n - len(_base)
                        _xi = (np.vstack([_base, self.rng.normal(0, 1.0, (_manca, 3))])
                               if _manca > 0 else _base[:n])
                    else:
                        _xi = np.asarray(_xi, float)[:n]
                    _ac = _a if np.isscalar(_a) else _a[:, None]
                    _bc = _b if np.isscalar(_b) else _b[:, None]
                    _xi = _xi * _ac + _bc * _g
                    self._xi_rumore = _xi
                    _calcio = _xi
                else:
                    _calcio = _g
                self._nb = self._nb + _calcio * amp[:, None]
                self._nb = self._nb / np.maximum(np.linalg.norm(self._nb, axis=1, keepdims=True), 1e-9)
"""

# ==========================================================================
# in `_passo_spinoriale`:  if SYNC_UPDATE and SCUOTIMENTO
# azione: via  --  il rumore sul primario complesso, ramo sincrono
# righe 3771-3778 del blob f845d30d
# ==========================================================================
_ARCHIVIO_passo_spinoriale_3771 = r"""
            if SYNC_UPDATE and SCUOTIMENTO:
                # eccitazione del vuoto sul PRIMARIO complesso (t->t+1): perturba psi, non il B letto
                Lam = lambda_vuoto(self)
                if Lam > 0:
                    I2 = (np.abs(psi_snapshot[:n]) ** 2 if psi_snapshot is not None else np.zeros(n))
                    amp = np.sqrt(Lam) / (1.0 + I2 / Lam)
                    a1 = a1 + (self.rng.normal(0, 1.0, n) + 1j * self.rng.normal(0, 1.0, n)) * amp
                    b1 = b1 + (self.rng.normal(0, 1.0, n) + 1j * self.rng.normal(0, 1.0, n)) * amp
"""

# ==========================================================================
# in `_passo_spinoriale`:  if SYNC_UPDATE and SCUOTIMENTO
# azione: via  --  il rumore sul Bloch ruotato, ramo sincrono
# righe 3786-3794 del blob f845d30d
# ==========================================================================
_ARCHIVIO_passo_spinoriale_3786 = r"""
            if SYNC_UPDATE and SCUOTIMENTO:
                # Il rumore e' un aggiornamento t -> t+1: non puo' contaminare il
                # campo B letto dalla snapshot. Usa comunque la stessa psi_t.
                Lam = lambda_vuoto(self)
                if Lam > 0:
                    I2 = (np.abs(psi_snapshot[:n]) ** 2
                          if psi_snapshot is not None else np.zeros(n))
                    amp = np.sqrt(Lam) / (1.0 + I2 / Lam)
                    nb_new = nb_new + self.rng.normal(0, 1.0, (n, 3)) * amp[:, None]
"""

# ==========================================================================
# in `step`:  if SYNC_UPDATE
# azione: via  --  il calcolo di psi_t dalla snapshot
# righe 5152-5154 del blob f845d30d
# ==========================================================================
_ARCHIVIO_step_5152 = r"""
        if SYNC_UPDATE:
            psi_t = self.satura(self._mat(w) @ np.exp(1j * _phi_t))
            self.psi = psi_t.copy()
"""

# ==========================================================================
# in `step`:  if SYNC_UPDATE
# azione: tieni-else  --  la materia della metrica: resta il percorso storico
# righe 5480-5486 del blob f845d30d
# ==========================================================================
_ARCHIVIO_step_5480 = r"""
        if SYNC_UPDATE:
            # Il campo della metrica resta quello della snapshot t, uguale a
            # quello usato da repulsione, sync, spinore e pozzo del passo.
            self.psi = psi_t.copy()
        else:
            F = Mw @ np.exp(1j * self.phi)
            self.psi = self.satura(F)
"""

# ==========================================================================
# in `_passo_spinoriale`:  if SYNC_UPDATE
# azione: tieni-elif  --  nb_vic = nb_prec_t: via, l'elif diventa if
# righe 3231-3232 del blob f845d30d
# ==========================================================================
_ARCHIVIO_passo_spinoriale_3231 = r"""
        if SYNC_UPDATE:
            nb_vic = nb_prec_t
"""
