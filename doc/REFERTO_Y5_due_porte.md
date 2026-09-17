# REFERTO — **`Y5` rosso: nessuna delle due porte. La causa è `rho_sorgente ≤ 0`.**

**Blob:** `b66e4c5c` → strumentato (**byte-inerte verificato**). **Nessuna riparazione, nessun
revert, nessuna logica toccata.** `Z9` non toccata.

---

## 1. LA STRUMENTAZIONE È BYTE-INERTE — **bloccante, passa**

```
PRESIDIO, conteggi PER PRIMI: nodi SENZA strum. 2025, nodi CON strum. 2025
array con SHAPE UGUALI confrontati: 38   (shape diverse: 0)
[PASS] 1b BYTE-INERTE: max|A-B| = 0.000e+00
```

---

## 2. IL VERDETTO: **nessuna delle tre letture del mandato. È una quarta.**

```
PORTA A  (len(peq) != len(i))       :  0        MAI
PORTA B  (peq NaN o <= 0)           :  4 / 66   ultima invocazione 8
   -> _peq_nodo NON valido          :  2392 nodi-invocazione,  ultima 8
   -> rho_sorgente NON valido       :  2019 nodi-invocazione,  ultima 66   <---
fallback totale sui nodi            :  3215,    ultima invocazione 66
   di cui nodi CON archi (grado>0)  :  3215     <- tutti
   di cui nodi SENZA archi          :  0
```

**PORTA A non scatta mai:** le lunghezze combaciano sempre. **Nessun difetto di lunghezza, e A8b in
quella forma non si applica.**

**PORTA B scatta solo fino all'invocazione 8** — il transitorio — **e il suo conteggio (2392) è
ESATTAMENTE il fallback totale del blob PRE-TEMPO 2.** **Quindi la componente `peq` è INVARIATA dal
TEMPO 2.**

> **La causa del `Y5` rosso è la TERZA condizione di `_ok_n`: `rho_sorgente ≤ 0`**, che cade **fino
> all'invocazione 66** su **2019** nodi-invocazione. `rho_sorgente` è `rho_spin` — il campo
> **EMESSO** — con `CAMPO_SPINORIALE` ON.
> **Il TEMPO 2 ha cambiato `psi` (Q4: 1669 nodi contro 1850), e con esso `psi_spin`: ha prodotto
> nodi in cui IL CAMPO EMESSO SI ANNULLA, dove prima non accadeva.**

**Esito operativo:** è la **lettura ②** del referto precedente — un difetto introdotto dal TEMPO 2 —
**ma con una causa diversa da quella che il mandato ipotizzava**. **Non lo riparo:** il mandato dice
di misurare, e la decisione è di Luca.

---

## 3. I DUE RILIEVI DEL GUARDIANO — **verificati dal codice, non accettati**

### 3.1 — *«`peq` letto dall'inerzia è quello DOPO la diffusione di questo passo? Sarebbe A5.»*
**FALSO, e lo decide l'ordine delle righe:**

```
:2986   _peq_t = self.peq.copy()          <- la fotografia a t
:3217   self._passo_spinoriale(...)       <- l'inerzia legge `self.peq` (:2161)
:3302   nuovi = np.isnan(self.peq)        <- la CALIBRAZIONE, cento righe DOPO
:3320   self.peq += dt_e * (... flusso/TAU_DIFF)   <- la DIFFUSIONE, DOPO
```

**L'inerzia legge `peq` PRIMA sia della calibrazione sia della diffusione di questo passo.**
**Non c'è violazione di A5: l'informazione dei vicini di questo passo non è ancora entrata.**

### 3.2 — *«`_peq_t` esiste e l'inerzia non lo usa: legge lo stato vivo, non la fotografia.»*
**VERO nella forma, ma SENZA CONSEGUENZA oggi** — ed è la stessa verifica a dirlo: **fra `:2986` e
`:3217` nulla modifica `self.peq`**, quindi in quel punto **lo stato vivo È la fotografia**.
**Sostituire `self.peq` con `_peq_t` non cambierebbe un bit.**

**Ma il rilievo coglie una cosa vera, e vale la pena scriverla:** **la garanzia viene dall'ORDINE,
non dalla struttura.** Se qualcuno spostasse `_passo_spinoriale` dopo `:3320`, **A6 si romperebbe in
silenzio**. Usare `_peq_t` la renderebbe vera **per costruzione**. *(È lo stesso ragionamento che ho
scritto nel commento dell'inerzia: «A6 è soddisfatto PER COSTRUZIONE, non da uno snapshot aggiunto»
— e qui si vede il limite di quella formulazione: è soddisfatto **dall'ordine**, che è una
proprietà più fragile.)*
**⚠ E `_peq_t` è locale a `step`: non è raggiungibile da `_passo_spinoriale` senza passarlo** — il
guardiano lo sospettava, ed è confermato.

### 3.3 — **Il parallelo con `_psi_spin_prec` e `_cs_nodo_prev` NON regge**
Quelli erano **cache INERTI**: il fallback scattava nel **95.33 %** e nel **71.88 %** dei casi, e la
legge dichiarata **non girava**. **Qui lo snapshot non è inerte: è EQUIVALENTE.** Chiamarla «la
terza volta nello stesso settore» **sovrappone due cose diverse** — un meccanismo morto e una
garanzia che dipende dall'ordine. **La seconda va irrobustita; la prima era un difetto.**

---

## 4. COSA RESTA APERTO, e non lo decido io

**`Y5` è rosso perché il TEMPO 2 produce nodi con campo emesso nullo.** Le vie, tutte decisioni:

1. **Rimisurare `Y5`** — se i nodi con `rho_spin = 0` sono un comportamento legittimo del sistema
   (il vuoto profondo), il criterio va riscritto sul comportamento vero;
2. **Trattare `rho_sorgente ≤ 0`** nell'inerzia come caso a sé, distinto dallo sfondo mancante;
3. **Revertire il TEMPO 2** — ma Q4 ha dimostrato che quel difetto era **reale**, quindi si
   tornerebbe a letture miste `t`/`t+1` note.

**E una quarta, che il rilievo del guardiano suggerisce e che è indipendente da `Y5`:** far leggere
all'inerzia **`_peq_t`** invece di `self.peq`, per rendere A6 vero **per costruzione** invece che per
ordine. **Oggi sarebbe byte-identico** (§3.2), quindi è **irrobustimento, non correzione** — e va
deciso come tale.
