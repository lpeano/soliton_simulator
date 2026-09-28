# -*- coding: utf-8 -*-
"""**ARCHIVIO: `_togli_rotazione_rigida` e il ramo di `L_CONSERVA`, usciti il 2026-09-28.**

**NON GIRA E NON SI IMPORTA.** Testo estratto con `git cat-file -p` dal tag
**`pre-archivio-lconserva`** (simulatore blob sha1-BYTE **`fe00b48a`**), non ricopiato.

    git cat-file -p pre-archivio-lconserva:soliton_simulator.py

**PERCHE' E' USCITO** *(decisione di Luca del 2026-09-28, strada `(b)`)*:

  - **il codice stesso lo marcava <<ERRATA, NON usare>>**: *<<doveva rimuovere la rotazione
    spuria del rilassamento, ma AZZERA tutta la rotazione rigida a ogni passo -> distrugge la
    PRECESSIONE FISICA REALE del sistema>>*;
  - **`L_CONSERVA` e' `False`** e **non ha nemmeno un flag CLI**: per accenderlo bisognava
    modificare il sorgente;
  - ### **e faceva dichiarare il FALSO al tipo di `rilassa_disegno`:** la catena
    `rilassa_disegno -> _togli_rotazione_rigida -> calcola_psi` le faceva scrivere `psi` e
    `psi_spin`, quindi il tipo `disegno` -- *<<scrive solo `pos`>>* -- **non era coerente**.
    **Archiviandolo il tipo diventa vero PER COSTRUZIONE invece che scusato.**

**⚠ E IL RAMO AGIVA DAVVERO, misurato PRIMA di toglierlo:** con `L_CONSERVA` acceso contro
spento, **17 grandezze su 23 differivano**. ### **Non e' una pulizia: e' una decisione.**

**`L_CONSERVA` NON e' stato tolto** *(decisione 3: si conserva tutto)*: e' un **no-op
accettato**, e **lo dichiara all'avvio** se qualcuno lo accende.
"""

raise SystemExit(__doc__)   # non si importa e non si gira: e' un ARCHIVIO


# ==========================================================================
# il metodo `_togli_rotazione_rigida`
# righe 6668-6695 del blob fe00b48a
# ==========================================================================
_ARCHIVIO_6668 = r"""
    def _togli_rotazione_rigida(self, pos0):
        """rimuove la rotazione rigida netta introdotta dallo spostamento pos0->pos, pesata per
        l'inerzia |Psi|^2. ITERATIVA: ripete finche' L residuo e' trascurabile (~conservazione
        completa). Conserva il momento angolare senza alterare la deformazione metrica."""
        n = self.n
        if not hasattr(self, "psi") or len(self.psi) < n:
            try: self.calcola_psi()
            except Exception: return
        w = np.abs(self.psi[:n]) ** 2
        if w.sum() < 1e-9: return
        P0 = pos0[:n]
        c = np.average(P0, axis=0, weights=w)      # centro pesato (inerzia), fisso
        r = P0 - c                                  # posizioni rispetto al centro (riferimento)
        I = np.sum(w * (r**2).sum(axis=1)) + 1e-9   # momento d'inerzia (fisso)
        for _ in range(12):                         # itero: la rimozione lineare e' approssimata
            P = self.pos[:n]
            d = P - P0                              # spostamento residuo dal riferimento
            Lz = np.sum(w * (r[:,0]*d[:,1] - r[:,1]*d[:,0]))
            Lx = np.sum(w * (r[:,1]*d[:,2] - r[:,2]*d[:,1]))
            Ly = np.sum(w * (r[:,2]*d[:,0] - r[:,0]*d[:,2]))
            Lnorm = abs(Lz)+abs(Lx)+abs(Ly)
            if Lnorm < 1e-6: break
            oz, ox, oy = Lz/I, Lx/I, Ly/I
            rot = np.empty_like(P)
            rot[:,0] = oy*r[:,2] - oz*r[:,1]
            rot[:,1] = oz*r[:,0] - ox*r[:,2]
            rot[:,2] = ox*r[:,1] - oy*r[:,0]
            self.pos[:n] = P - rot
"""

# ==========================================================================
# il ramo `if L_CONSERVA and pos0 is not None` in `rilassa_disegno`
# righe 6660-6666 del blob fe00b48a
# ==========================================================================
_ARCHIVIO_6660 = r"""
        if L_CONSERVA and pos0 is not None:
            # CONSERVAZIONE DEL MOMENTO ANGOLARE: il rilassamento fa inseguire le coordinate alla
            # metrica (fisica, si mantiene), ma la media sui vicini introduce una ROTAZIONE RIGIDA
            # spuria (non-centrale) che rompe L. La rimuovo proiettando via la sola rotazione rigida
            # netta dello spostamento, pesata per |Psi|^2 (l'inerzia = materia). NON tocca la
            # deformazione (la metrica che si realizza), solo la rotazione globale parassita.
            self._togli_rotazione_rigida(pos0)
"""
