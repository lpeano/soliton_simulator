# TASK HISTORY — `PASSO 2`, tre gruppi. E i salti SONO solo all'avvio: dimostrato, non assunto

**Data** 2026-09-20 · **branch** `fork-su2` · **HEAD** `c84aefc` · **blob** `7e6b839b`
(**sha1 dei BYTE GREZZI**; blob git `09e25872`) · albero **pulito** · **nessun run**.

> **⚠ IL MANDATO CITA `2a369526`: era il blob PRIMA della cura di `scala_p`.** Quella cura è
> **già cablata e sigillata `5/5`** (`dcb776a`), quindi il riferimento è cambiato. **Il §2 del
> mandato — *«manca SOLO cablare `|dpozzo|/phi_arc`»* — è già fatto.**

---

## 1. ⚠ LA VERIFICA CHE IL MANDATO CHIEDE PER PRIMA: **i salti sono solo all'avvio?**

**SÌ, ed è una DIMOSTRAZIONE, non un'assunzione.** Non serve un run nuovo: i due numeri che ho già
bastano, perché `quando` è l'indice dell'**ultima** invocazione saltata e `salti` è il **numero**
di salti.

```
zeta_vir_a :  salti = 1    ultimo salto = invocazione 1  di 12
zeta_vir_b :  salti = 11   ultimo salto = invocazione 11 di 55
```

**Gli indici di salto sono DISTINTI** *(uno per invocazione)*, **tutti `>= 1`**, e **tutti `<=` il
massimo**. Quindi:

```
11 indici distinti, ognuno >= 1, il piu' grande vale 11
  =>  sono ESATTAMENTE {1, 2, ..., 11}          (non c'e' altro modo di disporli)
```

> **I salti sono i PRIMI `11` di `55`, consecutivi, e dopo non accade mai più.** **Stessa cosa per
> `zeta_vir_a`: l'unico salto è l'invocazione `1`.**
> **È un TRANSITORIO DI AVVIO, e la causa è l'ORDINE** — `_sin2_vir` lo scrive
> `memoria_hebbiana_moto`, che gira **dopo** `step`.
> **Se fossero stati SPARSI, questo conto non tornerebbe**, e la causa sarebbe un'altra.

*(`zeta_vir_b` ha 55 invocazioni contro 12 passi perché il ramo Verlet gira a sottopassi CFL: ~4.6
per passo.)*

## 2. LE TRE CURE, e **sono tutte BYTE-INERTI**

### GRUPPO A — le due `ZETA_VIR`: **la via ①, e il perché**

**Si sceglie ① — `else` esplicito che DICHIARA che al primo giro non c'è freno anisotropo.**

**Perché non la ②** *(dare a `_sin2_vir` un valore iniziale)*: **`0` significa freno PIENO, `1`
freno NULLO, e qualunque valore in mezzo è un NUMERO SCELTO — `A1`.** **E non c'è niente da cui
derivarlo:** al primo giro `sin2` non esiste **perché non è ancora stato calcolato**, non perché
manchi un dato. **Inventare un valore iniziale significherebbe far credere che la legge abbia
girato quando non poteva.**

> **La ① non cambia il comportamento di un bit: rende ESPLICITO ciò che già accade.** Il codice
> oggi *fa* la cosa giusta **in silenzio**; dopo la cura la *dichiara*. **È `A8` — un ramo
> silenzioso non è un ramo — e `A9`: un presidio che non si vede non è un presidio.**

### GRUPPO B — le tre inerti: **`else` esplicito, comportamento invariato**
`kernel_alpha` *(0 su 145)*, `tempo_luce` *(0 su 34)*, `tors4pi` *(0 su 12)*.
**Si curano anche se oggi non scattano: sono difetti per FORMA, non per frequenza** *(precedente
`Z25`)*. **Il modello è `:3182`**, che il fallback ce l'ha già esplicito e derivato.

### GRUPPO C — il default `np.zeros` di `s2full`
```python
s2full = np.zeros(len(self.i));  s2full[mask] = sin2
```
**Gli archi fuori dal `mask` prendono `sin2 = 0`, cioè FRENO PIENO: una decisione fisica presa da
un'allocazione, e non contata.** **Si CONTA quanti archi restano fuori, e si DICHIARA il default
con la ragione.**

## 3. I SIGILLI
- **riduzione al limite [BLOCCANTE]:** **tutte e tre le cure sono byte-inerti**, quindi il sigillo
  è **byte-identità contro il commit precedente**, su `psi`, `d`, `phi`, `eta`, `n`, `pos`, `tw`;
- **i contatori RESTANO e DEVONO POTER SCATTARE** — si ri-dimostra (`V3`);
- **la frazione di salti del GRUPPO A DOPO la cura:** **resta quella**, perché la ① non cambia
  comportamento. **E va detto così, invece di far credere che la cura l'abbia azzerata;**
- **stabilità** + **si rigirano i sigilli del giro.**

## 4. COSA MI FA FERMARE
- **la byte-identità che non torna** → una delle tre cure sta cambiando comportamento: **STOP**;
- **un contatore che non scatta più** dopo la cura → l'`else` ha spostato il conteggio;
- **il conto del GRUPPO C che dà molti archi fuori dal `mask`** → il default `0` non è una
  formalità ma una legge, e va **derivato**, non dichiarato.

## 5. COSA NON SI TOCCA
`:2378` *(già misurata, `4f2a6b7`)* · `:3974` *(è il modello)* · le **19 di ESTENSIONE** *(sono la
cura ad `A8b`)* · le **26 di PRECONDIZIONE** e i **~10 `zeros` altrove** *(registrati col conto,
non in questo giro)* · `L_CONSERVA`.

## 6. TODO
1. [fatto] la verifica «solo all'avvio»: **dimostrata dai numeri**;
2. GRUPPO A → GRUPPO B → GRUPPO C, ciascuno col sigillo;
3. registro + relazione + checkpoint.
