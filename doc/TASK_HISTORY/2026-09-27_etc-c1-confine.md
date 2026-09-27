# `(c)1` — **il confine del passo: la fotografia si apre a inizio PASSO PIENO** *(2026-09-27)*

> **Mandato (cura `(c)`, primo punto):** *«fotografia unica dello stato fisico a inizio `PASSO_PIENO`
> (non di `step`): sposta `_smp_apri` lì.»*
>
> ### ✅ **SIGILLO PASSATO su DUE criteri.** **Blob: `7439d5c3` → `b5a713d1`.**
>
> **E la faccio UN PEZZO PER COMMIT, non tutta insieme:** `(c)` ha **sette** punti, e la regola
> d'oro non permette di accendere tutto in una volta.

---

# 1. COME, e perché non nel chiamante

**`_smp_apri()` diventa IDEMPOTENTE** e la chiamano **tutte e cinque le leggi**, in testa:
`scuoti_vuoto :787` · `step :5089` · `mitosi :5886` · `rilassa_disegno :6483` ·
`memoria_hebbiana_moto :6584`. ### **La prima che gira apre; le altre quattro escono subito.**

### **Così il confine è a inizio passo QUALUNQUE SIA L'ORDINE** — che è esattamente ciò che
`H-ETC-2` permuta.

## L'alternativa che **non** ho scelto, e va detta

**Mettere l'apertura nel chiamante** sarebbe più diretta. **Ma i chiamanti sono SEI:**

| | |
|---|---|
| `update()` *(`:7806`)* | il runtime vero, per frame |
| il benchmark *(`:7068`)* | 300 passi con timing per legge |
| due costruttori di scena *(`:9462`, `:9486`)* | il warm-up e `_passo(net)` di `MASSE-COERENTI` |
| `csv/_test_fork/_scena_video.py:37` | **la copia del driver** |
| `csv/_passo.py` | li **legge per AST** e verifica che coincidano |

> ### 📌 **Una divergenza fra due di loro sarebbe invisibile.** L'idempotenza mette il confine
> **dentro** la cosa che deve rispettarlo, invece di chiedere a sei posti di ricordarselo.

---

# 2. ⚠ UN DIFETTO CURATO DI PASSAGGIO, e non lo cercavo

In `step()` l'apertura stava **DOPO** la guardia:

```
def step(self):
    if self.n < 2 or not len(self.i): return      # <-- prima
    self._smp_apri()                              # <-- l'apertura era QUI
```

### **Un passo con meno di 2 nodi NON APRIVA la fotografia**, e quindi **il freno del passo non
chiudeva**. Ora l'apertura sta **prima**.
**Lo stesso in `scuoti_vuoto`**, dove precede `if not SCUOTIMENTO ... return`: **se la prima legge
esce subito, il passo deve cominciare comunque**, e la legge dopo non deve accorgersene.

> **E il commento che stava su quella riga diceva già la cosa giusta:** *«il passo, per il freno, è
> il ciclo INTERO del driver»*. ### **Lo diceva e non lo faceva:** la fotografia si apriva
> all'inizio di `step`, cioè **dopo** `scuoti_vuoto`. **Ora il commento e il codice dicono la stessa
> cosa.**

---

# 3. IL SIGILLO, **due criteri e non uno**

**Referto:** `csv/_seal_fork/_sig_etc_c1.json`. **Condizioni:** scena `(ii)(a)`, seme `11`,
`n = 2107`, `m = 70199`, 3 passi pieni, ordine canonico, nessuna iniezione di `rng`, nessun presidio.

| criterio | atteso | esito |
|---|---|---|
| **① lo stato** | **byte-identico** | ### **23 grandezze su 23, 0 elementi diversi** |
| **② i contatori del confine** | `aperture = 3`, `gia_aperta = 12` | ### **`3` e `12` esatti** |

*(più `_g_smp_chiusure = 3`, `_g_smp_disallineati = 0`, `_g_sm_patol = 0`.)*

## 3.1 — **Perché il byte-identico DA SOLO non bastava**

> ### **Un'apertura che non fosse avvenuta darebbe lo STESSO stato.**
> La fotografia serve **al freno**, e il freno **chiude solo se è aperta**: se l'apertura fosse
> sparita, `_smp_chiudi` non avrebbe frenato e — su 3 passi con `dx` piccolo — lo stato sarebbe
> potuto restare **identico entro i byte**. **Il byte-identico avrebbe detto «tutto bene» mentre il
> confine non esisteva più.**
>
> **`_g_smp_aperture = 3` e `_g_smp_gia_aperta = 12` sono ciò che distingue «la fisica non è
> cambiata» da «la fisica non è cambiata E il confine si è spostato».**

**L'attesa era dichiarata nel commit del codice**, prima di girare: *«il sigillo verificherà anche
`_g_smp_aperture == passi` e `_g_smp_gia_aperta == 4*passi`»*. **Il contatore `_g_smp_gia_aperta`
nasce con questa cura** *(`A8`)*, e serve proprio a rendere quel numero **leggibile invece che
supposto**.

---

# 4. ⛔ LA CHIUSURA **NON** È TOCCATA, ed è una decisione

`_smp_chiudi()` sta in fondo a `memoria_hebbiana_moto`, e **subito dopo c'è
`verifica_invarianti()`**.

> ### **Spostare la chiusura fuori dalla legge farebbe girare il controllo degli invarianti su `d0`
> NON ANCORA FRENATA.** Cambierebbe **quando** il controllo guarda, non solo dove sta il freno.
> ### **È un SECONDO meccanismo, e va in un secondo commit** *(regola d'oro: un interruttore alla
> volta)*.

**Verificato dal codice** che `verifica_invarianti` **legge soltanto** — lo dichiara *(«Legge
soltanto»)* e lo fa *(l'unica scrittura è il contatore `_g_inv_giri`)*. **Quindi lo stato non
cambierebbe: cambierebbe su quali valori il controllo scatta.** E `INVARIANTI` è **acceso** nel
driver, quindi non è un'ipotesi: il controllo gira davvero.

---

# 5. E DUE SCHEDE DI FISICA CHE NON C'ERANO

**`H-REG-R` ha rifiutato il commit quattro volte**, e la prima diceva la cosa più grossa:

> ### **`scuoti_vuoto` e `rilassa_disegno` — la PRIMA e la QUARTA delle cinque leggi del passo —
> NON AVEVANO UNA SCHEDA.**

**Create entrambe**, con la forma letta dal codice, cosa leggono, cosa scrivono, le dimensioni e i
limiti classificati con `A11`:

| scheda | e la cosa che ci ho messo dentro |
|---|---|
| **`scuotimento-vuoto`** | ### **`scuoti_vuoto` scrive `phivel` e NIENT'ALTRO** — ed **è il fatto che rende `(c)1` byte-identico**: fra lei e `step` non c'è nessuna scrittura di `d` o `d0`, quindi spostare la fotografia **non la cambia**. *(Il sigillo lo verifica invece di fidarsi della riga.)* |
| **`rilassamento-disegno`** | **non è fisica: è il DISEGNO**, e ci vive `A3-DISEGNO` — `pos` scritto qui è **riletto dalla fisica** a `:6622` *(senza guardia)* e `:7010`. **La cura NON lo chiude**, e la scheda lo dice. E `L_CONSERVA` è morto, con la sua `calcola_psi()` che `H-ETC-1` conta fra le 8: **l'unico degli 8 in un ramo morto** |

**Aggiornate anche quattro schede esistenti:** `freno-scala-min`, `memoria-del-moto`,
`mitosi-schwinger`, `fase-phi`.

> ### ⚠ **Due delle cinque leggi del passo sono vissute senza forma scritta fino al commit che le
> rende sincrone.** Non è un dettaglio di processo: **la cura `(c)` deve riscriverle**, e fino a
> stamattina **non c'era niente da cui derivarla.**

---

# TODO DEL NEXT STEP

> ### 🛑 **STOP, un pezzo per commit.**

1. ### **`(c)2` — la CHIUSURA:** `_smp_chiudi()` dopo l'ultima legge, **e con lei
   `verifica_invarianti()`**, così il controllo guarda lo stato **committato**. **Due movimenti
   legati, un commit.** *(E il sigillo dovrà avere un braccio che li distingue: byte-identico non
   basta, perché il controllo invarianti non scrive.)*
2. `(c)3` le cinque leggi leggono **solo** la fotografia e producono **variazioni**.
3. `(c)4` il freno di scala minima **una volta** sul totale *(già così per `d` e `d0`: `C3` esteso)*.
4. `(c)5` `phi` avvolta e `_nb` normalizzato **una volta** a fine passo.
5. `(c)6` mitosi **dopo** le variazioni, decisa sulla fotografia.
6. `(c)7` `psi` e `psi_spin` **estese ai nati**, calcolate **solo per loro**.
7. `(c)8` i **flussi casuali per legge**.

## LE VOCI D'INDICE CHE QUESTO DOCUMENTO TOCCA

`ETC-C1-CONFINE` · `ETC-PASSO` · `H-ETC-1` · `H-ETC-2` · `A3-DISEGNO` · `PSI-FLASH` · `A8` · `A11`
