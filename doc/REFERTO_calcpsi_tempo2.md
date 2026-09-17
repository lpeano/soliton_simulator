# REFERTO — TEMPO 2 cablato, **ma Q8 FALLISCE: `Y5` si rompe.** Committo il fallimento e mi fermo.

**Blob:** `9dfd91c4` → nuovo (due righe). Byte grezzi del riferimento `31fe9013`.
**`Z9` non toccata.** **Il terzo ramo non toccato, dichiarato.**

---

## 1. IL CABLAGGIO, E I SUOI SIGILLI PROPRI: **7/7 PASS**

```
forma: DUE chiamanti passano `w`, UNO no (l'elif)   con w: 2, senza: 1
Q4  i due DIFFERISCONO: nodi 1669 vs 1850          -> IL DIFETTO NON ERA TEORICO
Q5  `w is None` da 134 a 42; DENTRO il passo -> 0   (verificato a parte: 0 su 20 passi)
Q7  psi finito, d0 > 0, |nb| = 1 (2.2e-16), _taup_cfl_max = 0.400
```

**Q4 è la risposta alla domanda che il mandato lasciava aperta:** i pesi ricalcolati **non**
coincidevano. **Il difetto era reale**, e la sua correzione cambia il sistema.

**Q5 verificato al dettaglio:** dopo il cablaggio, in 20 passi, **zero ricalcoli dentro il passo**.
Restano **3 chiamate** da `_registra_concorrenza`, **tutte al setup** — fuori dal passo, quindi
**non violano `:2959`** e non vanno corrette per simmetria.

---

## 2. ⚠ MA Q8 FALLISCE — **`Y5` dell'inerzia si rompe**

```
                    invocazioni   fallback(nodi)   passi distinti   ULTIMA invocazione
PRE  TEMPO 2             66            2392              4                8 / 66
POST TEMPO 2             66            3215             57               66 / 66
```

> **Prima del TEMPO 2 il fallback dello sfondo dell'inerzia CESSAVA all'invocazione 8 e non
> tornava** — era il transitorio, ed era la previsione scritta prima.
> **Dopo, scatta in 57 passi su 60, fino all'ULTIMA invocazione.**

**E il pavimento `1e-6` risale:** da **324 / 93710 (0.35 %)** a **837 / 98955 (0.85 %)**.

**Gli altri tre sigilli del giro passano:** `V1 8/8`, `V2-V5 8/8`, `V6-V10 12/12`.
**E `peq` degenere della plasticità è IDENTICO** (`207509` in **2** passi, prima e dopo): **non è
`peq` per arco a essere cambiato.** Il fallback che si rompe è quello **per NODO**, cioè
`peq_nodo <= 0` **oppure** `rho_sorgente <= 0`.

### Cosa NON faccio

**Non invento la causa.** Il fatto è che il TEMPO 2 cambia `psi` — Q4 lo dimostra — e `psi` alimenta
`rho_spin` e `peq`; ma **quale dei due diventi non-valido a ogni passo non l'ho misurato**, e
dedurlo sarebbe esattamente ciò che questo repo ha già pagato tre volte in una notte.

**Il mandato è esplicito** (§3, Q8): *«Se uno fallisce, committa il reperto e FERMATI.»*
**È quello che questo commit fa.**

---

## 3. LE DUE LETTURE POSSIBILI, e non scelgo io

1. **`Y5` era un criterio scritto su un comportamento che dipendeva dal difetto.** Il fallback
   cessava all'invocazione 8 **quando i pesi venivano ricalcolati**; tolto il ricalcolo, il sistema
   evolve diversamente (**2025 nodi contro 1774**) e qualche nodo resta senza sfondo valido a ogni
   passo. **In questa lettura `Y5` va rimisurato, non il codice riparato.**
2. **Oppure il TEMPO 2 ha introdotto un difetto vero** nell'inerzia, e il fallback al 95 % dei passi
   è **A8 nella sua forma peggiore**: *«un fallback che scatta quasi sempre non è un fallback, è il
   comportamento principale»*.

**Le due letture si distinguono con UNA misura**, che non faccio ora perché il mandato dice di
fermarsi: **quale delle due condizioni cade** — `peq_nodo <= 0` o `rho_sorgente <= 0` — e **su
quanti nodi**. È un contatore da separare in due, come già fatto per
`_taup_causale_su_degenere`.

---

## 4. LO STATO DEL CODICE

**Il cablaggio del TEMPO 2 è COMMITTATO, non annullato**, come CLAUDE.md §5 prescrive: *«se il
sigillo FALLISCE, committa comunque lo stato + il fallimento e FERMATI: non "aggiustare al volo"
dentro lo stesso commit»*.

**Chi riprende deve sapere che:** `Z13` è **chiusa sul suo sigillo** (7/7) ma **aperta su Q8**, e il
blob attuale ha `Y5` **rosso**.

---

## 5. IL TERZO RAMO — dichiarato, come ordinato

`:3054` (l'`elif` sotto `REPULS_LEGGE`) **non è stato toccato**, e nel codice c'è ora un commento che
dice:

> *«Questo ramo ha lo stesso difetto ed è stato lasciato com'è, deliberatamente. Non è codice morto:
> è il comportamento alternativo di un flag. Non essendo eseguito, nessun sigillo può verificarne la
> correzione. **Se qualcuno spegne `REPULS_LEGGE`, il difetto delle letture miste torna.** Chi lo
> spegne deve saperlo.»*

**E la regola generale, che vale oltre il caso:** **un ramo sotto flag non si corregge e non si
cancella — si DICHIARA**, perché il difetto è **latente, non assente**.
