# TASK HISTORY — **VIA IL `0.3`: `MITOSI-SOGLIA-GRAD` esce**

*(Decisione di Luca del 2026-10-06, sul referto `27c10bd`. ### **Si committa DA SOLO e PRIMA
della patch**, cosi' l'ordine e' ### **verificabile da git** invece che asserito da me.)*

---

## 1. RAGIONAMENTO PRELIMINARE — *perche' esce, e cosa so*

### I NUMERI CHE LO DECIDONO, **riverificati da me dai `json` di `6cfcc4e`**

| | |
|---|--:|
| `R` sulle divisioni | ### **`0.1616`** |
| `R` sulla popolazione nella finestra | ### **`0.3417`** |

**Entrambe nella banda intermedia.** E le ### **nascite per `100` passi**, che il mandato cita
e che ### **ho ricontato io:**

| braccio | la serie |
|---|---|
| `_AMP = 0` | `0`, `0`, `48`, `55`, `104`, `150`, `94`, `120`, `138`, `118` |
| `_AMP = 0.3` | `0`, `0`, `143`, `298`, `374`, `649`, `628`, `789`, `836`, ### **`1044`** |

> ### ✔ **IL FATTO, e si legge senza statistica:** senza il `0.3` la crescita e'
> ### **STABILE** — fra `48` e `150`, e ### **non sale** dopo il passo `600`. Con il `0.3`
> ### **ACCELERA fino all'ultimo passo.** ### **Non e' una differenza di quantita': e' una
> differenza di FORMA.**

### CHE COSA GUARDA IL `0.3`, **letto dal codice**

```
_rn = self._r_nodo_mitosi()
grad_modula = np.abs(_rn[self.i] - _rn[self.j])
soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_modula))
```

Guarda ### **`|r_i − r_j|`**, il gradiente del tempo proprio lungo l'arco.

> ### ⚠ **E IL MANDATO DICE CHE QUELLA GRANDEZZA CORRELA `0.04` CON LA SPINTA.**
> ### **Quel numero NON l'ho rimisurato io**, e nessuna delle misure di questa settimana lo
> produce: ### **lo riporto come numero del GUARDIANO, non come un mio riscontro.**
> ### **Se contasse per la decisione andrebbe rifatto** — ma ### **non conta**, perche' la
> decisione si regge sui due `R` e sulla forma della crescita, che ### **ho verificato.**

### IL CENSIMENTO, **col comando e non a memoria**

*(perimetro: il simulatore e gli strumenti ### **vivi** — escluse `csv/_archivio/` e le copie
patchate `_sim_*.py`, che sono ### **derivate e gitignorate**)*

| nome | nel simulatore | negli strumenti vivi |
|---|--:|---|
| `grad_modula` | `4` citazioni *(### **`2` di codice**)* | `_patch_d32_nomi` `9` · `_mitosi_soglia_grad` `22` · `_mitosi_zero_dove` `7` · `_crescita_dopo_z43` `5` · `_soglia_alla_divisione` `2` · `_sig_decisione_separata` `1` |
| `_r_nodo_mitosi` | ### **`2`**: la `def` e ### **UNA SOLA chiamata** | `_quadro_unico` `1` · `_copertura_derivate` `2` · `_lettura_tau_a` `1` · `_referto_soglia` `1` · `_soglia_alla_divisione` `2` · `_sig_decisione_separata` `2` |
| `_tum_r_*` *(i quattro contatori `A8` dentro `_r_nodo_mitosi`)* | `7` *(`4` di codice)* | ### **`5` strumenti li LEGGONO** |
| `_g_tors4pi_*` *(la guardia della modulazione)* | `4` | ### **NESSUNO** |

### ⛔ **E QUATTRO STRUMENTI VIVI ANCORANO SULLA RIGA CHE ESCE**

`_patch_d32_nomi`, `_crescita_dopo_z43`, `_mitosi_soglia_grad` *(`6` volte)*, e
### **`_mitosi_zero_dove`** — ### **quello che ho curato stamattina.**

---

## 2. PROGETTAZIONE — *la patch, e cosa si rompe*

### LA PATCH E' UNA **RIMOZIONE**, con ### **ZERO codice nuovo**

`soglia` e' ### **gia'** `np.full(len(avv), soglia0, float)` a `:8426`: il blocco della
modulazione ### **la sovrascrive.** Togliere il blocco lascia ### **`soglia = soglia0` su
ogni arco**, che e' esattamente cio' che il mandato chiede.

> ### ✔ **`9-ter` E' SODDISFATTO NEL MODO PIU' FORTE: la cura TOGLIE una legge e non ne
> aggiunge nessuna**, e non c'e' nemmeno una riga da scrivere.

| esce | resta |
|---|---|
| il blocco `if TORS_4PI and len(self.i) == len(avv):` *(la modulazione)* | `soglia = np.full(len(avv), soglia0)` |
| ### **`_r_nodo_mitosi`**, che resta ### **senza chiamanti nel simulatore** | il resto della catena dei cancelli |
| i quattro contatori ### **`_tum_r_*`**, che vivono dentro quella funzione | |

### ⚠ E LA GUARDIA `_g_tors4pi_*` **RESTA, e dico perche'**

Contava i salti ### **della modulazione**, quindi dopo la patch ### **non guarda piu'
niente.** ### **Nessuno strumento vivo la legge**, quindi toglierla sarebbe sicuro —
### **ma il mandato non lo chiede**, e ### **fare piu' di quello che un mandato chiede e'
il modo in cui una cura diventa due.** ### **La annoto nel codice** perche' nessuno la legga
come viva, e ### **toglierla resta una decisione di Luca.**

### ⛔ COSA SI ROMPE, **e va detto prima**

| chi | perche' | che cosa resta vero |
|---|---|---|
| `_mitosi_soglia_grad` *(`1279c6fb`)*, `_mitosi_zero_dove` *(`c206bd4b`)*, `_crescita_dopo_z43`, `_patch_d32_nomi` | ### **l'ancora della loro patch SPARISCE** | ### **girano al LORO commit** *(`par.6`)*, e i loro `json` restano attribuibili |
| `_riverifica_t4`, `_sig_decisione_separata`, `_m7_potenza_termostato`, `_soglia_alla_divisione`, `_referto_cura2` | leggono ### **`_tum_r_*`**, che esce | idem |

> ### ⚠ **NOVE STRUMENTI RESTANO LEGATI AI BLOB VECCHI**, e questo ### **non e' un
> incidente**: `par.6` dice che ### **un sigillo si rigira col `git checkout` del commit che
> ha sigillato.** ### **Il difetto sarebbe un sigillo non piu' ri-girabile AL SUO COMMIT**, e
> ### **non e' questo il caso.**
>
> ### ⛔ **MA `_mitosi_zero_dove` E' LO STRUMENTO DELLA MISURA DI OGGI**, e dopo questa patch
> ### **non gira piu' sul blob nuovo.** ### **Se servisse rimisurare il `DOVE` sulla legge
> senza `0.3`, andrebbe riancorato** — e ### **non lo faccio qui.**

### ⛔ LA SOGLIA `3π` **NON SI TOCCA**

`soglia0 = PHI_CRIT + twist_max = 2π + π = 3π`. ### **Il `π` di dipolo che in questa scena non
esiste e' una decisione SEPARATA di Luca, e resta in coda.** ### **Questa patch toglie la
MODULAZIONE, non la soglia.**

### I TRE BRACCI DEL SIGILLO, **e cosa decide ciascuno**

| | che cosa pretende | che cosa decide |
|---|---|---|
| **`S0`** | la copia di prima ### **+ la patch** e' ### **byte-identica** al blob nuovo, e i due girano `150` passi con ### **tutti gli attributi di `net` identici** *(`_calcpsi_origini` ### **aggregato per nome**)* | che la patch sia ### **quella e solo quella** |
| **`S1`** | il blob nuovo riproduce ### **AL BIT** i conteggi per passo di `amp0.json` *(il braccio `_AMP = 0` di `6cfcc4e`)* sui primi `150` passi | ### **il controllo FORTE.** `soglia0·(1 − 0·tanh(x)) = soglia0` ### **esattamente**, e la riga ### **non tocca il generatore casuale** |
| **`S2`** | il blob nuovo ### **DEVE differire** da `amp0_3.json`, e si riporta ### **il primo passo diverso** *(in `27c10bd` era il ### **`212`**)* | che la patch ### **faccia qualcosa** |

> ### ⛔ **SE `S1` NON COINCIDE, LA PATCH FA ALTRO: mi FERMO e lo scrivo.** Non e' una
> formalita': ### **e' l'unico braccio che puo' smentire il ragionamento algebrico**, e il
> ragionamento e' ### **l'unica ragione per cui mi aspetto l'identita'.**

---

## 3. LA STELLA POLARE — **le cinque risposte** *(`L-STELLA`)*

| | la risposta |
|--:|---|
| **1** *(`A14`)* | ### **NON SI APPLICA:** la patch ### **non introduce nessuna legge**, ne toglie una. Non tocca energia ne' carica |
| **2** *(i tre gradini)* | ### **gradino `(b)`: <<regge togliendo la legge pratica>>**, ed e' ### **gia' MISURATO** *(`27c10bd`: `R` intermedia, crescita stabile senza)*. ### **Non `(a)`** *(un seme solo)* ### **ne' `(c)`** *(nessun limite noto)* |
| **3** *(aggiunge un numero o una legge?)* | ### **NE TOGLIE UNA, e del tipo peggiore:** il `0.3` era ### **una TOPPA** — modulava una soglia ### **per far accadere la mitosi** — e `9-ter` dice che a parita' di effetto si preferisce ### **togliere un'eccezione.** Qui l'effetto ### **non e' pari**, ed e' il punto: la crescita ### **cambia FORMA**, e si sceglie quella ### **senza la toppa** |
| **4** *(`rho`, `c_s`, il SEGNO?)* | ### **NO.** Tocca ### **la soglia di una decisione di nascita.** ### ⚠ **Ma TOGLIE il solo punto in cui `r = cs/CS_M` entrava nella MITOSI**, e questo va detto: dopo la patch ### **il tempo proprio non modula piu' la nascita** |
| **5** *(emergente o imposto)* | ### **E' LA RAGIONE DELLA CURA:** `27c10bd` ha mostrato che la crescita ### **sopravvive** senza il `0.3` *(`R = 0.16`/`0.34`, non `0`)*, quindi ### **non era imposta da lui.** ### **Toglierlo rende la risposta PULITA invece che condizionata** |

---

## 4. TODO

1. **commit di questo task history**, ### **DA SOLO**;
2. la **patch**, ### **commit a se'**;
3. il **sigillo** `S0` / `S1` / `S2`, ### **commit a se'** — e ### **se `S1` fallisce,
   FERMO**;
4. l'**archivio** del ramo che esce, col tag ### **`pre-mitosi-soglia-grad-via`**;
5. la **chiusura** di `MITOSI-SOGLIA-GRAD`, ### **coi numeri**, e ### **scrivendo che la
   chiusura e' decisione di Luca.**
