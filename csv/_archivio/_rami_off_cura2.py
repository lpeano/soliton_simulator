# -*- coding: utf-8 -*-
"""`RAMI-OFF-CURA2` — IL CANCELLO VECCHIO DELLA MITOSI, uscito dal sorgente col `6b`.

### **QUESTO FILE NON SI IMPORTA E NON GIRA.** E' un ARCHIVIO: il testo del ramo
che il commit `6b` ha ### **tolto dal sorgente**, conservato ### **verbatim** perche'
sia leggibile senza un `git show`.

### **PERCHE' SI CONSERVA invece di cancellarlo** *(decisione 3 di Luca: si conserva
tutto)*: il flag `--mitosi-2lam` ### **RESTA** e il driver continua a passarlo, ma
### **non fa piu' niente** -- e' dichiarato fra i `[flag-inerti]`, come `PAV_COM` e
`SYNC_UPDATE`. ### **Un flag che non fa niente e che qualcuno accende e'
un'ASPETTATIVA TRADITA**, quindi il blocco dei flag inerti dice ### **dove e' finito
il suo ramo**, e questo file e' quel posto.

## IL CANCELLO VECCHIO, dal blob `c18c9bf6` (commit `716b3c0`)

```python
        #   Il figlio nasce a `d/2` dai genitori, quindi `d/2 >= LAM` <=> `d >= 2 LAM`.
        #   LA CONDIZIONE VA **QUI**, accanto alla soglia di densita': e' lo STESSO punto dove il
        #   codice decide «questo candidato si divide o no». **NON in `nasce`** (la' si decide una
        #   PROBABILITA', e `A13` non e' una probabilita'), **NON in `_nasce`** (la' si RIPARA, e
        #   la cura e' proprio togliere la riparazione).
        self._g_m2l_tot = getattr(self, "_g_m2l_tot", 0) + int(np.size(c))
        if MITOSI_2LAM and len(c):
            _dc = np.asarray(self.d, float)[c]
            _conforme = _dc >= 2.0 * LAM
            self._g_m2l_negati = getattr(self, "_g_m2l_negati", 0) + int(np.sum(~_conforme))
            self._g_m2l_dmin = min(getattr(self, "_g_m2l_dmin", float("inf")),
                                   float(_dc.min()) if _dc.size else float("inf"))
            ok = ok & _conforme
        self.negate += int((~ok).sum()); sel = c[ok]
```

### **CHE COSA DICEVA:** un arco si divide solo se `d >= 2.0 * LAM`,
### **e SOLO SE il flag era acceso.** Il `2.0` veniva dal fatto che il figlio
nasceva ### **a meta'**: `d/2 >= LAM` equivale a `d >= 2*LAM`.

### ⛔ **PERCHE' NON BASTAVA PIU', e non e' una questione di stile:** dal commit
`6a` la frazione di nascita e' ### **`FRAZ_NASCITA`, dichiarata in un solo posto** e
non necessariamente `0.5`. Con una frazione diversa da meta' ### **il cancello
vecchio guarda la grandezza SBAGLIATA**: a `t = 0.4` il troncone corto e' `0.4*d`,
e `d >= 2*LAM` lo ammette anche quando `0.4*d < LAM`. ### **La forma generale chiede
DUE disuguaglianze, una per troncone.**

### ✅ **E A `t = 0.5` LE DUE FORME COINCIDONO AL BIT**, perche' moltiplicare per
`0.5` e per `2.0` e' ### **esatto in IEEE-754**: e' per questo che il braccio `A`
del sigillo del `6b` e' ### **identico al byte** con il flag acceso.
"""

raise SystemExit("RAMI-OFF-CURA2: questo file e' un ARCHIVIO, non si esegue.")
