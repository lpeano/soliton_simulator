# TASK HISTORY — **cablare la regola del TASK HISTORY**

**Data:** 2026-09-18 · **Branch** `fork-su2` · **HEAD al momento della scrittura** `aa23e40`
**Task:** rendere operativa la regola di Luca — *ragionamento preliminare → progettazione →
entrambi in un task history → il task history nel TODO del next step → commit e push*.

> **Questo è il primo task history, e descrive il task di crearlo.** È volutamente
> auto-referenziale: **è il modo di provare la regola invece di dichiararla.** Se la regola non
> reggesse al suo stesso caso, non reggerebbe a nessuno.

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare*

**Cosa la regola risolve, e non è la documentazione.** In questo repo il ragionamento è già stato
la parte più preziosa, e più volte quella che stava per andare persa:

- la strada **scartata** è risultata più informativa di quella presa — le quattro varianti del
  denominatore, le **due** rotture del punto 1 di `Z24`, i tre nulli letti con risoluzioni diverse;
- un riavvio ha cancellato lo scratchpad e con esso il termine di paragone di **quattro sigilli**
  (`Z31`);
- **quattro errori di popolazione in due giorni** sono stati trovati **rileggendo il proprio
  ragionamento**, non i risultati.

**La mia premessa, che dichiaro perché potrebbe essere sbagliata:** credo che il valore stia
nell'**ordine temporale** (prima di misurare), non nella forma del documento. Se fosse solo forma,
sarebbe l'ennesima nota — e `Regola 9` dice che una nota che non impedisce il ripetersi non è un
presidio.

**Cosa NON so, e lo scrivo adesso:**
- **non so se la regola reggerà ai task corti.** Un task da due comandi potrebbe non meritare tre
  sezioni, e allora la regola verrebbe aggirata — che è il modo in cui le regole muoiono. **Lo
  saprò solo usandola, e va riverificato fra qualche giro.**
- **non so se riuscirò a renderla un MECCANISMO.** Un file si può scrivere dopo e antidatare nel
  testo. L'unica cosa che git rende verificabile è **l'ORDINE dei commit**.

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *come intendo arrivarci, e cosa mi fermerebbe*

**I passi, e cosa decide ciascuno:**

1. **Definire la struttura** — tre sezioni nell'ordine che Luca ha dato. *Decide:* se il documento
   ha un posto per «cosa non so», che è la parte che si perde per prima.
2. **Legarla a ciò che esiste già**, invece di aggiungere un rito parallelo: par.5 (*commit prima
   del run*), le **previsioni ex ante**, i **criteri dei sigilli scritti prima**. *Decide:* se è
   una regola nuova o la stessa regola applicata al pensiero. **Credo la seconda.**
3. **Renderla verificabile** — il commit del task history dev'essere **antenato** dei commit del
   lavoro. *Decide:* se posso chiamarla presidio o devo chiamarla controllo.
4. **Applicarla a questo stesso task.** *Decide:* se funziona.

**Cosa mi farebbe fermare e riportare invece di procedere:**
- se non trovassi **nessun** modo di verificarla da git → allora è una nota, e **va detto**, non
  camuffato da presidio;
- se la struttura duplicasse `PREVISIONI_qualitative.md` senza aggiungere nulla → allora la regola
  giusta sarebbe **estendere quel file**, non crearne un altro.

**Esito della progettazione, prima di eseguire:** il punto 3 mi dà un **controllo** (`git
merge-base --is-ancestor`), **non un impedimento** — non impedisce di scrivere dopo e antidatare,
impedisce di farlo **senza che git lo mostri**. **Per Regola 9 è meno di un meccanismo e più di una
nota, e va scritto così.** Sul punto 4: le previsioni riguardano **l'esito di una misura**, il task
history riguarda **il percorso**; non si duplicano, e il secondo copre anche i task che **non hanno
una misura**.

---

## 3. TODO DEL NEXT STEP

- [x] `doc/TASK_HISTORY/README.md` — la convenzione, con la dichiarazione onesta su cosa NON è
- [x] questo file — il primo task history, che descrive il task di crearlo
- [x] `CLAUDE.md` par.5-septies — la regola, legata a par.5, alle previsioni e ai criteri
- [x] **commit e push del task history PRIMA del resto** *(è il punto della regola)*
- [ ] **⚠ DA RIVERIFICARE FRA QUALCHE GIRO:** la regola regge ai **task corti**? Se comincio ad
      aggirarla sui task da due comandi, **la regola è sbagliata, non io** — e va cambiata invece
      che ignorata. **Criterio:** se in tre giri consecutivi un task salta il task history, la
      regola va rivista.
- [ ] **rimasto aperto dal giro precedente, non toccato qui:** `Z30` — `nudo` (36.2×) contro
      `linea` (16.9×), **e la domanda a monte: l'estensività è un difetto?** *(non misurato)*
- [ ] **`Z31`:** il meccanismo per i quattro sigilli non ri-girabili è **proposto, non cablato**
