# REFERTO — **`nsub = 206` dal vivo, un NUCLEO CHE RECLUTA, e i nati hanno grado 2**

> Criteri **fissati prima** in `doc/TASK_HISTORY/2026-09-20_venti-archi-e-nsub.md` (`11e043a`);
> strumento committato prima di girarlo (`_venti_archi.py`, `cee10eb5`, `beca015`).
> **Dagli snapshot e dallo stack, a run VIVI e non toccati.**
> Dati grezzi: `csv/_test_fork/_venti_archi.txt`, `_venti_archi_nodi.txt`,
> `csv/_test_fork/_diag_B/locals_*.txt`, `stack_B_1809.txt`.

---

## 1. PARTE ① — **`nsub` LETTO DAL VIVO, e il buco di `A8` si chiude per il presente**

`py-spy dump --locals` stampa le locali di ogni frame: **`nsub` diventa leggibile senza toccare
una riga di codice e senza fermare i run.** Tre campioni per ramo, tutti concordi:

```
ramo A    n1=1   n2=1   n3=1     ->  nsub =   4      (il PAVIMENTO di max(4, ...))
ramo B    n1=1   n2=3   n3=206   ->  nsub = 206      n3 VINCE DA SOLO
```

> **`n1` (la sorgente) e `n2` (`beta`) sono INERTI: valgono `1` e `3`.**
> **La fuga e' governata da `|vd|` e da nient'altro** — e non e' piu' una deduzione dagli snapshot:
> **e' letto dal processo.**

**`n3` era `52` allo snapshot del passo 360: adesso e' `206`. E' quadruplicato da allora.**

**E una differenza QUALITATIVA:** in A **6 campioni su 8 cadono FUORI** dal blocco CFL
*(`_pesi`, `chiralita_core_locale`, `_passo_spinoriale`)*; in B **tutti** cadono **dentro** il ciclo
dei sottopassi.
> **A spende il tempo nella fisica. B lo spende a tenere insieme l'integratore.**

**Controllo di coerenza:** `206/4 = 51.5` contro un rapporto di costo osservato `>21`
(`>600 s/frame` contro `28.6`). **Stesso ordine, e non uguali** — perche' il ciclo CFL non e' il
100 % di un passo. **Che siano dello stesso ordine e non identici e' cio' che ci si aspetta.**

---

## 2. PARTE ②② — **la formula di `vd`, LETTA e non dedotta**

```python
:3934   med   = sm / self._deg                     # <-- LA DIVISIONE
:3935   lap   = 0.5*(med[i] + med[j]) - q          # q = d - d0
:3936   acc_t = cs_arco**2 * lap + src - beta*self.vd
:3967   self.vd = vd_half + 0.5*dts*acc_next
```

**LA RISPOSTA ALLA DOMANDA DEL MANDATO E' NO: nessuna divisione per una grandezza che possa andare
a zero.** `_grado()` (`:1171`) definisce `self._deg = np.maximum(bincount + bincount, 1)`:
**il pavimento e' gia' dentro `_deg`.**

**⚠ MA C'E' UN'INCOERENZA, e va detta come tale e non come difetto:**
```
SEI siti dividono per  np.maximum(self._deg, 1)   -> :2636 :3763 :3782 :4073 :4140 :4279 :4646
CINQUE dividono per    self._deg  NUDO            -> :3850 :3934 :3942 :3975 :4551 :4655
```
**Oggi sono equivalenti.** Lo sono **finche' `_grado()` resta com'e'**: la protezione vive in **UN
punto solo**, e cinque siti vi si appoggiano **senza dichiararlo**.

---

## 3. PARTE ②①③ — **LE VENTI RIGHE, e il nucleo che recluta**

### 3.1 Cosa sono i venti archi peggiori di B

| passo | `\|vd\|` max | `d/d0` max | nodi distinti su 20 archi | **NATI** |
|---|---|---|---|---|
| 120 | 2.923 | 7.02 | **38** — sparsi | **0** |
| 240 | 79.15 | 48.5 | **12** — concentrati | **0** |
| 360 | **531.6** | **178.6** | **16** | **0** |

**Al passo 360 l'arco peggiore e' `16—867`: `d = 98.5` contro `d0 = 0.81`, cioe' `d/d0 = 121.7`.**
**E il record di stiramento e' `1396—867`: `d/d0 = 178.6`.**

### 3.2 ⚠ IL REPERTO CHE SMENTISCE LA MIA ASPETTATIVA

**Avevo scritto, prima di misurare, che mi aspettavo i NATI al centro della fuga** *(task history
par.1.4, e il sospetto veniva dal grado basso)*.

> **MISURATO: NEI VENTI ARCHI PEGGIORI DI B, AI TRE ISTANTI, I NATI SONO `0`. TUTTI E ZERO.**
> **Sono tutti nodi ORIGINALI, con grado fra `569` e `663`.**

**L'aspettativa e' REFUTATA, e non si riscrive: si annota.** La fuga vive nel **cuore denso**, fra i
nodi piu' connessi — **non alla periferia scollegata.**

### 3.3 L'IDENTITA': gli ARCHI cambiano, i NODI RESTANO

**A livello di ARCHI** *(il criterio che avevo fissato)*:
```
passo 120 -> 240   in comune  0/20   -> "RICAMBIO"
passo 240 -> 360   in comune  2/20   -> "RICAMBIO"
```
**A livello di NODI** *(la misura che mancava, fatta dopo aver visto che gli archi non bastavano)*:
```
passo 120 -> 240   nodi 38 -> 12   IN COMUNE  0   (Jaccard 0.000)
passo 240 -> 360   nodi 12 -> 16   IN COMUNE  5   (Jaccard 0.217)    NULLO: 0.005
      persistenti: 16, 481, 621, 627, 837
```
**`0.217` contro un nullo di `0.005` e' `43` volte il caso.**

**E l'HUB ruota, mentre il nucleo resta:**
```
passo 120   nodo 556 -> 3 archi su 20     (nessun hub: e' il regime normale)
passo 240   nodo 481 -> 11 archi su 20    <- un hub
passo 360   nodo 867 -> 11 archi su 20    <- un hub NUOVO;  481 scende a 6, 16 resta a 4
```

> **VERDETTO: «NUCLEO CHE RECLUTA» — la terza lettura, quella che il mandato diceva di dichiarare
> invece di forzarne una delle due.**
> **Un nucleo di nodi originali ad alto grado (`16`, `481`, `621`, `627`, `837`) persiste; un nuovo
> hub (`867`) viene reclutato e prende il sopravvento; gli ARCHI si rinnovano attorno ai nodi.**
> **E il passo 120 non ne fa parte: `0` nodi in comune col 240 — l'evento NASCE fra i due.**

### 3.4 La controprova su A — **la coda non esiste affatto**

```
ramo A passo 1680:  |vd| max = 3.333    d/d0 max = 5.19    nodi distinti 31 su 20 archi
```
**Non e' «piu' bassa»: e' `160` volte piu' bassa, ed e' il regime normale** — gli stessi valori che
A aveva al passo 120.

**⚠ E UNA COSA CHE IN A C'E' E IN B NO:** fra i venti di A compaiono **4 NATI**, tutti di grado `2`,
con **`|omega_s|` fra `3.4e+03` e `3.5e+04`** — contro `~0.01` dei nodi originali.
**Sei ordini di grandezza.** *(E `d/d0 = 1.000` esatto su due di essi: archi appena nati, a riposo.)*
**Non e' la fuga di `vd` — e' un'altra cosa, e va misurata a parte.**

---

## 4. PARTE ③ — **I NATI HANNO GRADO 2, E SONO LA MAGGIORANZA**

```
ramo A  passo  120   ORIGINALI n=2391  deg p50 549   <=4:   0.0 %
                     NATI      n= 281  deg p50   2   <=4: 100.0 %   (max 3)
ramo A  passo 1680   ORIGINALI n=2391  deg p50 551   <=4:   0.0 %
                     NATI      n=4932  deg p50   2   <=4:  99.9 %   (max 6)
ramo B  passo  360   ORIGINALI n=2391  deg p50 549   <=4:   0.0 %
                     NATI      n= 838  deg p50   2   <=4: 100.0 %   (max 4)
```

> **La distribuzione e' BIMODALE e la separazione e' NETTA: `2` contro `549`.**
> **Nessun originale scende sotto `59`. Nessun nato sale sopra `6`.**
> **Al passo 1680 i nati sono `4932` su `7323`: il `67 %` del sistema ha DUE archi.**

**E la diluizione si misura:** `archi/nodo` in A passa da **`197.40`** (passo 120) a **`72.84`**
(passo 1680), mentre gli archi crescono solo da `527 441` a `533 379` (**`+1.1 %`**) e i nodi
**triplicano**.

**Il rilievo del mandato — *«un nodo senza archi non ha fisica: non sente, non e' sentito, non
contribuisce»* — e' MISURATO, e la maggioranza e' superata.**

**⚠ MA «grado 2» NON E' «senza archi», e la differenza va tenuta:** un nodo di grado 2 **e'**
connesso, ai suoi due genitori *(la mitosi crea il figlio al punto medio dell'arco, con esattamente
due archi — par.9)*. **Cio' che NON ha e' il vicinato denso degli originali.** **Se questo lo renda
inerte o no NON e' misurato qui**, ed e' la voce che si apre.

---

## 5. ⚠ E `Z73` VA CORRETTA UNA SECONDA VOLTA — **`chi_basc` NON BLOCCA LA MITOSI**

L'A/B corto diceva: *«con `chi_basc` ACCESO, in 60 passi non nasce niente»*. Era gia' stato ritirato
il 2026-09-20 perche' **era la finestra**. **Ora cade dai fatti del run lungo, ed e' definitivo:**

```
ramo A (chi_basc ACCESO):   n  2672 -> 7323   fra il passo 120 e il 1680     (x2.7)
                            di cui NATI: 281 -> 4932
```
**Con `chi_basc` acceso sono nati 4651 nodi in 1560 passi.** **La mitosi non e' bloccata, e non e'
nemmeno ritardata oltre il transitorio.**

---

## 6. COSA QUESTO REFERTO **NON** DICE

- **NON decide l'A/B di `chi_basc`.** Un seme per ramo: il nullo di un confronto fra bracci non e'
  zero, e' la dispersione **FRA SEMI**, **non misurata**;
- **NON estende la diagnosi al blocco del passo 2700** — li' il processo era **fermo e non
  scriveva**, qui **avanza**. Restano due fenomeni distinti;
- **NON dice se il grado 2 dei nati sia un difetto** — dice che e' **la condizione della
  maggioranza**, e che nessuno l'aveva misurata;
- **NON spiega `|omega_s| ~ 3e4` sui nati di A.** E' un secondo reperto, e va misurato a parte.
