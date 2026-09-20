# TASK HISTORY — `sep = 4.0`: interazione MEDIATA DAL VUOTO. Il pilota, poi i 10.000 passi

**Data** 2026-09-20 · **branch** `fork-su2` · **HEAD** `f491377` · **blob** `775ceab7`
(sha1 dei byte grezzi verificato) · albero **pulito** · nessun processo in esecuzione.

> **Nessuna cura, nessuna promozione, nessun cambio di default. Nessun verdetto di fisica.**
> **Il simulatore e il driver non si toccano finche' il run non e' finito.**

---

## 1. LA SCENA SCELTA, e i numeri che la definiscono *(dalla scansione, `f491377`)*

```
sep = 4.0    bordi massa-massa  +5.53    archi massa-massa      0
             bordi massa-vuoto  -0.635   archi massa-vuoto  97590
             componenti 1        archi totali 527088   (x1.23 contro il run vecchio)
```

**Le masse sono separate fra loro e tutte immerse nel vuoto: l'interazione passa ATTRAVERSO il
vuoto.** Il run vecchio a `sep = 8` non aveva nemmeno questo: **quattro componenti, zero archi.**

## 2. ⚠ DUE COSE VERIFICATE DAL CODICE PRIMA DI SCRIVERE LO STRUMENTO

### (a) `conc_nodi` E' VUOTO IN QUESTA SCENA — il mandato chiede una strada che non c'e'
Il mandato dice *«gli archi diretti fra nodi di masse DIVERSE (per coorte, via `conc_nodi`)»*.
**Misurato: `conc_nodi` ha 2391 liste e sono TUTTE VUOTE.**
**Dal codice il perche' e' netto:** `semina()` chiama `_registra_concorrenza` **solo se
`mass_id is not None`** (`:1878-1879`), e `mass_id` viene passato **solo da `nuova_massa()`**.
**`_massa()` — quello che la scena usa — chiama `semina()` SENZA `mass_id`.**

**La strada che ESISTE:** `_massa()` registra le coorti in `test["dati"]["coorti"]`
*(`massa_0`/`massa_1`/`massa_2`, 497 nodi ciascuna — verificato)*, e il vuoto sono i primi
`SEME_INIZIALE = 900`. **Ma sono gli indici dei soli nodi SEMINATI: i nati dopo non ci entrano**,
e l'eredita' alla mitosi (`:4052`, `:4177`) riguarda **`conc_nodi`**, che qui e' vuoto.

**Quindi il lignaggio dei nati me lo costruisco, e dichiaro come:** un nodo nasce **al punto medio
di un arco, con esattamente due archi verso i due genitori**, entrambi di indice **minore**
(`CLAUDE.md` §9). **Una sola passata in ordine di indice** assegna a ogni nato l'etichetta dei
genitori; **se i due genitori hanno etichette DIVERSE il nodo e' `MISTO`, e si conta a parte.**
**Non si sceglie una delle due: un nodo nato da un arco massa-vuoto non appartiene a nessuna delle
due, e fingere il contrario gonfierebbe proprio il numero che decide.**

### (b) IL CRITERIO DELLA LETTURA `C` E' RITIRATO **PER MANDATO**, e sostituito
Il mandato dice: *«NON usare "componenti < 4" come criterio: e' scaduto»*, e *«sara' UNA dal primo
passo»*. **La fermata del pilota su `nc == 1` va tolta.**
> **Lo scrivo qui e non nel codice soltanto, perche' e' un criterio che cambia DOPO aver visto i
> dati, e l'unica cosa che lo rende legittimo e' che **lo cambia Luca, non io**, e che
> **l'osservabile sostitutivo e' migliore**: il **segno del bordo massa-massa**. Negativo =
> compenetrate = scena sbagliata. **A `sep = 4.0` vale `+5.53`.**

## 3. IL PILOTA — 300 passi a `sep = 4.0`, cosa misura

1. **archi DIRETTI fra coorti diverse** *(massa A - massa B)*: **restano zero o ne nascono?**
   **E' il criterio vero;**
2. **archi MASSA-VUOTO** *(partono da 97 590)*: **crescono, calano, si rompono?**
3. **numero di componenti e taglie**: **resta 1?**
4. **durata per 100 passi** *(misurata a 100, non estrapolata dal totale)* e **dimensione del primo
   snapshot compresso**, per derivare `--db-ogni` e la stima totale;
5. **e i nodi `MISTO`**, che sono la popolazione nuova di questa scena: **quanti sono?**

### LE QUATTRO LETTURE, fissate PRIMA
| # | esito | conclusione |
|---|---|---|
| **A** | archi m-vuoto **robusti**, archi m-m **zero**, **una** componente | **la scena e' quella: si procede** |
| **B** | archi m-vuoto **CROLLANO** nei primi passi | il contatto col vuoto non regge: **`sep = 4.0` e' troppo largo**, si riporta e si propone un `sep` piu' stretto **dalla scansione** |
| **C** | **nascono archi m-m** | le masse si sono **avvicinate**: **e' un fenomeno, non un errore.** Si riporta |
| **D** | il grafo **si spezza** | si riporta **col passo esatto** |

## 4. IL DRIVER — il cambiamento, e quando
**`_scena_video.py` ha `--sep 8` CABLATO.** **Non si tocca per il pilota** *(che e' uno script a
parte)*. **Per il run serve**, e sara' **un commit solo, col suo sigillo**: **`--sep=X` NOMINALE,
default `8`**, cioe' l'idioma che il driver gia' usa e documenta per `--serie` e `--csv-progresso`
*(«NOMINALI e non posizionali di proposito... il comando di `Z49` deve restare riproducibile
VERBATIM»)*. **Il sigillo: a default il driver fa esattamente quello che faceva.**
**Il run non parte finche' quel commit non e' sigillato.**

## 5. I PRESIDI
- **il pilota non e' il run:** i suoi numeri decidono se lanciare, **non entrano in un referto**;
- **A3c:** distribuzioni bimodali -> popolazioni separate, **mai una mediana**;
- **A8:** ogni contatore stampato, **inclusi `_db_scritti`/`_saltati`/`_falliti`** nel run;
- **`--tau-luce` ha il sigillo `6/7` con `T3` dichiarato**: va **in testa al referto**;
- **la cartella non si cancella** (`Z31`); **un seme, una scena.**

## 6. COSA MI FA FERMARE
- **lettura `B`** -> si riporta e **non si lancia**;
- **durata o spazio fuori scala** -> **cadenza piu' rada, MAI meno passi**, e si riporta prima;
- **il driver non ancora sigillato** -> **non si lancia.**

## 7. TODO DEL NEXT STEP
1. [fatto] blob/branch; `conc_nodi` verificato vuoto e strada sostitutiva dichiarata;
2. il pilota aggiornato (lignaggio dei nati, criterio `C` sostituito), **committato prima**;
3. **300 passi a `sep = 4.0`** -> archi m-m, m-vuoto, componenti, durata, spazio -> **STOP**;
4. il commit del driver con `--sep` nominale **e il suo sigillo**;
5. previsioni qualitative -> `STATO_RUN.md` -> il run da 10.000 passi.
