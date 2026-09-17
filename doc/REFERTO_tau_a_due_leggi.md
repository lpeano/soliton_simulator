# REFERTO — **`TAU_A` governa DUE leggi, non una.** E la sostituzione proposta ne fa una terza, già bocciata da un sigillo.

**Blob:** `69ee540` (byte grezzi `ee0c2a60`), HEAD `cdc0e41` — **coincide con quello del mandato**
(`69ee5403`). **Nessun codice toccato.**

Il mandato §1.1 dice: *«**`TAU_A` compare ALTROVE?** Enumera OGNI uso… **Se è usato in più punti con
significati diversi, cambiarlo lì tocca tutti: FERMATI e riporta la mappa prima di cablare.**»*
**È il caso.**

---

## 1. LA MAPPA — due leggi fisiche distinte, un solo numero

| riga | uso | che cos'è |
|---|---|---|
| **`:2429`** | `ramp = min(1, self.eta / TAU_A)` | **maturazione del kernel** — *quanto tempo perché un nodo pesi* (il difetto **Z9**) |
| **`:2226`** | `_tau = TAU_A * max(_dens/_dens_rif, 0.05)` | **vita media della MEMORIA SPINORIALE** — il rilassamento di `omega_s` |
| **`:2229`** | `_tau = TAU_A` | lo stesso, ramo non-locale |
| `:6950/:6952` | `--regime` lo sovrascrive | **insieme** a `G_PH`, `SCUOTIMENTO`, `_CALORE_INIT` |

**Sono due tempi che non hanno niente in comune se non il nome:** uno dice *«quando un insieme di
punti diventa un oggetto»*, l'altro *«quanto a lungo un nodo ricorda la propria rotazione»*.
**Condividono un numero per accidente storico, non per legge.**

**Sostituire `TAU_A = LAM/cs` li cambierebbe ENTRAMBI**, e il secondo è quello su cui poggia buona
parte della letteratura del repo: `omega_eq ∝ sqrt(tau)`, il random walk smorzato, il plateau di
`|omega_s|`, il «tempo di dissipazione fissato da un pavimento» (CLAUDE.md §9). **Non è un effetto
collaterale: è una seconda modifica di regime, non richiesta e non sigillata.**

---

## 2. ⚠ IL FATTO CHE DECIDE — **quella sostituzione ESISTE GIÀ, e il suo sigillo è FALLITO**

```python
:2218   if TAU_LUCE:
:2222       _tau = self._tempo_luce_nodo(i, j)[:, None]      # d_nodo / cs_nodo
:2223   elif TAU_A_LOCALE:
:2226       _tau = TAU_A * np.maximum(_dens / _dens_rif, 0.05)
```

**`--tau-luce` fa ESATTAMENTE questo**: sostituisce `_tau = TAU_A·max(dens/dens_rif, 0.05)` con un
**tempo-luce**. È la **FASE 2**, e:

> **il suo sigillo NON È PASSATO** — `doc/SIGILLO_tau_luce_FALLITO.md`, ed è la voce **A** del
> registro, dichiarata in CLAUDE.md §0 **«il collo di bottiglia del programma»**. È la ragione per
> cui **il gate è indietro rispetto al disco e resta indietro**.

**Quindi cablare `TAU_A = LAM/cs` senza flag significherebbe applicare a `_tau` una sostituzione
equivalente a quella di `--tau-luce`, ma:**
- **senza flag** (mentre `--tau-luce` è OFF di default, proprio perché non certificato);
- **senza sigillo** (mentre quello di `--tau-luce` è stato scritto **e fallito**);
- **come categoria D**, cioè dichiarandola *«correzione di difetto»* — mentre la stessa sostituzione,
  fatta esplicitamente, è un **ramo non certificato**.

**Questo non è un dettaglio procedurale: è il presidio di §2.6 di CLAUDE.md.** *«Un timbro si mette
DOPO il sigillo, mai prima.»*

---

## 3. E `LAM` NON È «DI STATO»

Il mandato scrive: *«**A1** (zero parametri: `LAM` e `cs` sono **di stato**)»*. **Metà è vero.**

```
:146    LAM      = 0.8          <- COSTANTE DI MODULO, e --lam la cambia (:5257, :5435)
```

`cs` **è** di stato. **`LAM` no: è un numero scelto**, esattamente come `TAU_A = 50`.
`TAU_A = LAM/cs` **non elimina il numero scelto: lo sposta**, e in cambio lo lega a `cs`.

**Questo NON la squalifica**, e va detto con equilibrio: CLAUDE.md §3 elenca `LAM` fra **le scale che
esistono già** (*«`tau = d/cs`, `G(rho)` …, `LAM`, `K_C`»*), e A1 vieta le costanti **nuove**, non
l'uso di quelle presenti. **Ma la formula corretta è «nessun parametro NUOVO», non «zero
parametri»** — e la differenza conta, perché `LAM` resta spostabile da riga di comando.

---

## 4. IL `git blame` **NON** CONFERMA L'IPOTESI DELLA «COMPENSAZIONE SCADUTA»

Il mandato chiedeva di verificarlo, e la verifica è stata fatta:

```
670310fc  2026-08-28   _TAU_A_REGIME = 50.0       # alta persistenza memoria spinoriale
670310fc  2026-08-28   ramp = np.minimum(1.0, self.eta / TAU_A)
```

**Entrambe le righe vengono dallo STESSO commit**, `670310fc`, il cui messaggio è
*«Implement code changes to enhance functionality and improve performance»* — **non dice nulla**.

> **Quindi NON c'è evidenza che `TAU_A = 50` sia stato alzato per stabilizzare `omega`.**
> **La modifica NON si può descrivere come «rimozione di una compensazione scaduta»:** quella
> descrizione richiederebbe una prova che il `blame` non fornisce. *(P1: se rileggendo non si trova
> nulla sul punto, si dice che non si è trovato nulla.)*

---

## 5. COSA RESTA VERO — **Z9 non è toccato da nulla di quanto sopra**

**Il difetto misurato resta esattamente quello:** `ramp` matura in **~5526 passi**, i run sono
**300-500**, a 500 passi `ramp` mediano vale **~0.09** e il peso d'arco tipico è **~1 %** di quello
maturo. **La diagnosi del mandato sul `ramp` è giusta.** Ciò che non regge è il **veicolo** della
correzione: `TAU_A` non è una manopola del solo `ramp`.

---

## 6. LE VIE, e sono decisioni di regime — **non ne cablo nessuna**

1. **Separare le due leggi.** Introdurre una scala **distinta** per la maturazione del kernel
   (`TAU_MAT = LAM/cs`) e **lasciare `TAU_A` dov'è**. **È la via che fa solo ciò che il mandato
   vuole fare**, e non tocca la memoria spinoriale. **Ma "separare" significa riconoscere che oggi
   due leggi condividono un numero, e stabilire che è un accidente — è una decisione, non una
   deduzione.**
2. **Cambiare `TAU_A` per intero**, accettando che tocchi anche `_tau`. **Allora non è categoria D:
   è la FASE 2 per un'altra strada, e va sotto il sigillo di `--tau-luce`, che è fallito.**
3. **Non toccare `TAU_A` e affrontare Z9 altrove** — p.es. chiedendosi se `eta` debba crescere col
   tempo proprio o col tempo di coordinata. *(Non l'ho analizzato: lo nomino, non lo propongo.)*

**La ① è quella che vedo più pulita**, e lo dico perché serve una raccomandazione, non un elenco.
**Ma introduce un nome nuovo per una scala, e la scelta di separare due leggi finora unite non è
mia.**
