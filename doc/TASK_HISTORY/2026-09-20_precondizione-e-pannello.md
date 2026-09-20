# TASK HISTORY — le guardie di PRECONDIZIONE, poi il pannello fedele. In quest'ordine

**Data** 2026-09-20 · **branch** `fork-su2` · **HEAD** `e403e15` · **blob** `f81c4fe1`
(**sha1 dei BYTE GREZZI**; blob git `af8a96f1`) · albero **pulito** · **nessun run**.

> **L'ORDINE, deciso da Luca:** **① le guardie di PRECONDIZIONE → ② il PANNELLO FEDELE → ③ il RUN
> a `sep = 4.0`, per ultimo.** **Nessun run finché ① e ② non sono chiusi.**
> **NIENTE NUMERI SCELTI. Una correzione, un sigillo.**

---

## 1. ⚠ UNA PREMESSA DEL MANDATO NON COMBACIA COI MIEI NUMERI, e lo dico prima

**Il mandato riporta:** `FISICA 112`, di cui `19 ESTENSIONE + 7 SALTO SILENZIOSO + 26 PRECONDIZIONE`
*(= 52, non 112)*. **La mia scansione — `csv/_test_fork/_scansione_schemi.txt`, prodotta da uno
strumento committato — dà:**

```
A  91 guardie       di cui FISICA 64
B   9 default       di cui FISICA  7
C  59 saturazioni   di cui FISICA 35
D  10 memorie
```

**Le guardie `len(...)` su percorso fisico sono `64`, non 52 né 112.** **Non uso i numeri del
mandato: li ricavo dal disco**, che è ciò che il mandato stesso ordina *(«NON fidarti della triage
di Claude web: rileggi tutto dal disco»)*.

## 2. LA CLASSIFICAZIONE, e la faccio col CODICE non a occhio

**Per ciascuna delle 64, si guarda COSA SUCCEDE QUANDO LA CONDIZIONE FALLISCE** *(dall'`AST`, non
dal testo)*:

| classe | forma | giudizio |
|---|---|---|
| **TERNARIO** | `x = A if len(..) == n else B` | **il default è INLINE e VISIBILE**: è già un `else` esplicito |
| **PRECONDIZIONE** | al fallimento `return` / `raise` | **legittima** — *non ho i dati, non calcolo* — **ma il silenzio no: serve il contatore** |
| **ESTENSIONE** | il corpo **allunga o tronca** l'array testato | **è LA CURA ad `A8b`** *(`_cs_nodo_prev` 71.88 %, `_psi_spin_prec` 95.33 %)*: **non si toccano** |
| **DEFAULT** | al fallimento si prosegue con un valore di comodo | **difetto**: una decisione fisica presa da un fallback non dichiarato |
| **SALTO** | al fallimento **non succede niente** e la legge è saltata | **la famiglia già curata** (`Z68`) |
| **GIÀ CURATA** | ha già il contatore e la ragione | si registra e si salta |

## 3. LA VERIFICA STORICA — **`git log -S`, e la PRIMA riga**

**Per ogni sito: `git log -S "<la riga>" --reverse`** → **il commit che l'ha INTRODOTTA**, non
quello che l'ha toccata per ultimo.
> **⚠ È l'errore già preso: `git blame` dava `f7051c3` per `:3182`, mentre `-S` dà `94c2609` — un
> commit intero di differenza.** E sulla provenienza dei cinque siti del giro scorso la lettura di
> Claude web era **falsa su entrambe le affermazioni**.

**Poi si cerca la ragione in `RAMIFICAZIONI.md`, `COMPONENTI_PROMOSSE.md`, i referti e i task
history:** una guardia può avere la sua ragione lì dentro.

### I TRE ESITI, fissati PRIMA
- **(a) nessuna ragione dichiarata** → **si cura;**
- **(b) ragione dichiarata e ANCORA VALIDA** → **eccezione: si LASCIA e si REGISTRA il perché**,
  così nessuno ci ritorna. **⚠ Ma resta un ramo, e `A8` vale anche per lei: CONTATORE SÌ,
  comportamento invariato;**
- **(c) ragione dichiarata ma SCADUTA** *(il difetto che proteggeva è stato curato)* → **quello è
  il reperto: la guardia protegge da qualcosa che non c'è più.**

**STOP e riporto la tabella PRIMA di curare.**

## 4. LE CURE — lo stesso metodo che ha funzionato due volte
**PASSO 1** i contatori, **byte-inerti**, committati e girati prima — *per sito col nome,
invocazioni, forma al fallimento, e **QUANDO***. **PASSO 2** `else` esplicito con la ragione, e
dove la guardia fallisce **la causa si trova A MONTE**.
**Sigilli:** byte-identità **[BLOCCANTE]** · i contatori **possono scattare** *(dimostrato)* ·
riduzione al limite · rigiro dei sigilli del giro.

## 5. POI IL PANNELLO FEDELE
**Il problema è misurato:** `campo_spaziale` somma su **tutti i nodi** con la FFT, `calcola_psi`
solo **sugli archi**. **Il costo è già stato pagato:** nel run a `sep = 8` il pannello mostrava
interferenza **fra masse che stavano in quattro componenti con ZERO archi fra loro**.
**Si AGGIUNGE un pannello** che **interpola `psi`** sulla stessa griglia. **Entrambi restano.**
**Vincoli:** non si tocca `campo_spaziale` né la FFT · **il blob del simulatore non cambia: è
rendering** · **l'interpolazione LEGGE `psi`, non lo RICALCOLA** *(precedente `lambda_vuoto`)* ·
i buchi si **dichiarano** · uno smoothing, se serve, ha la scala **derivata** · **si misura il
costo.**

**E la regola che sarebbe servita due giorni fa, da mettere in `STATO_RUN.md`:**
> **prima di interpretare QUALUNQUE struttura vista in un pannello, verificare che ci siano ARCHI
> in quella regione.**

## 6. COSA MI FA FERMARE
- **la tabella che trova molte `(c)`** *(guardie che proteggono da difetti già curati)* → **è un
  reperto, e si riporta prima di curare;**
- **una classe numerosa** → si riporta e si aspetta, invece di curare venti punti in un commit;
- **il pannello che dovesse RICALCOLARE `psi`** → **STOP**: sarebbe fisica dentro il rendering.

## 7. TODO
1. [fatto] task history + l'ordine ①②③ in `STATO_RUN.md`;
2. lo **strumento** di classificazione + storia, committato prima;
3. **la tabella dei siti** → **STOP e riporto**;
4. le cure a gruppi, col sigillo;
5. il pannello: **prima la voce TODO, poi l'esecuzione.**
