# REFERTO — **I nodi senza campo NON c'erano prima. Il TEMPO 2 li ha creati.** E il sospetto `Z9` è smentito.

**Blob confrontati:** `9dfd91c4` (PRE-TEMPO 2, byte grezzi `31fe9013`) e **`a8f1b2f4`** (attuale,
byte grezzi `cf6722ff`). **Copia del vecchio estratta con `git cat-file -p`, mai `git checkout`**
(trappola CRLF, C18); `git hash-object` della copia = **`9dfd91c4`**, verificato.
**Nessuna riparazione, nessun revert, nessun pavimento.** `Z9` non toccata.

---

## 1. LA MISURA, DUE BLOB AFFIANCATI

**La sonda è ESTERNA e identica per i due blob** — il vecchio non ha i contatori cablati, e una
strumentazione aggiunta solo a uno dei due non sarebbe un confronto.

| | **VECCHIO `9dfd91c4`** | **ATTUALE `a8f1b2f4`** |
|---|---|---|
| invocazioni con nodi `rho_sorgente ≤ 0` | **0** | **26** su 66 |
| prima / ultima invocazione | — | **1 / 63** |
| nodi-invocazione `rho ≤ 0` | **0** | **488** |
| di cui **ZERO ESATTO** | 0 | **488** |
| di cui `0 < rho < 1e-300` | 0 | **0** |
| di cui non finiti | 0 | **0** |

> **PRIMA DEL TEMPO 2 NON CE N'ERA NESSUNO. È la seconda lettura del mandato: il TEMPO 2 li ha
> creati.**

### ⚠ Una correzione alla sonda, prima di leggere i numeri
**La prima versione usava una scena MIA** (tre `nuova_massa`, raggio 2.0) e dava **60 invocazioni**
contro le **66** del batch. **La differenza erano i SEI passi di riscaldamento** che il batch fa dopo
`semina(80)`. **Una sonda che non riproduce la scena misura un altro sistema**, e il primo risultato
(«1 sola invocazione») era di quel sistema. La scena è ora **riprodotta dal sorgente** (`~:5993-6014`),
non inventata, e i conteggi combaciano: **66 invocazioni su entrambi i blob.**

---

## 2. ⚠ IL SOSPETTO `Z9` È SMENTITO — da tre misure indipendenti

Il mandato sospettava che `Y5` fosse **un sintomo di `Z9`**: pesi al 9 %, quindi `psi` che arriva a
zero macchina per i nodi periferici con vicini immaturi. **Tre misure lo escludono:**

**① Sono ZERO ESATTO, non denormali.**
```
zero esatto: 488 / 488        0 < rho < 1e-300:  0
```
**Se fosse maturazione lenta del kernel, i valori sarebbero piccolissimi ma NON nulli.**
**Un prodotto che "arriva a zero macchina" lascia denormali. Qui non ce n'è nemmeno uno.**

**② Il `ramp` dei loro vicini è quello di tutti.**
```
ramp dei VICINI dei nodi senza campo : 0.0039742
ramp mediano di TUTTI i nodi         : 0.0038639
```
**Non hanno vicini più immaturi della media: hanno vicini normali.**

**③ E il `ramp` è IDENTICO nei due blob** — il TEMPO 2 non tocca `ramp`. **Se la causa fosse `Z9`,
i nodi senza campo ci sarebbero stati anche PRIMA. Non c'erano.**

---

## 3. CHI SONO — **hanno la firma della MITOSI**

```
GRADO   dei nodi SENZA campo :   2.00      dei nodi CON campo : 119.00
ETA     dei nodi SENZA campo : 0.01364     dei nodi CON campo : 0.1936
```

**Grado esattamente 2**, e CLAUDE.md §9 lo dice: *«Il figlio nasce al PUNTO MEDIO dell'arco con
ESATTAMENTE due archi, verso entrambi i genitori»*. **Ed hanno un'età 14 volte minore.**

**E la distribuzione nel tempo conferma:**
```
inv  1  passo  0   n= 80   ko= 80    <- il setup: semina(80), campo non ancora calcolato
inv  7  passo  0   n=440   ko=360    <- la creazione delle tre masse
inv 14  passo  7   n=443   ko=  3        poi un RIVOLO di 1-5 nodi per invocazione,
inv 21  passo 14   n=451   ko=  1        e `n` che cresce da 443 a 488:
inv 63  passo 56   n=488   ko=  2        SONO LE NASCITE DA MITOSI
```

> **I nodi senza campo sono i FIGLI DELLA MITOSI, al loro primo passo.**

---

## 4. ⚠ COSA NON DICO — **il meccanismo**

**So CHI sono** (figli della mitosi), **QUANDO** (dal primo passo, in modo continuo), **e che PRIMA
del TEMPO 2 non c'erano.** **NON so ancora PERCHÉ il TEMPO 2 li produca**, e non lo invento.

**L'ipotesi ovvia — *«`calcola_psi()` ricalcolava i pesi e così popolava `psi_spin` per i nodi
nuovi, ora non più»* — NON l'ho verificata**, e c'è un fatto che la complica: **la verifica
preliminare del TEMPO 2 aveva misurato la topologia INVARIATA nel 100 % delle chiamate dentro
`step`**, perché la mitosi avviene **fuori** da `step`. **Le due cose non tornano da sole**, e il
mandato è esplicito: *«NON inventare una quarta spiegazione: riporta e fermati.»*

**È la stessa disciplina che ha già evitato tre spiegazioni sbagliate in una notte.**

---

## 5. IL VERDETTO, contro le tre letture fissate PRIMA

| lettura | esito |
|---|---|
| *c'erano già, stessa quantità* → sintomo di `Z9` | **NO.** Prima: **zero** |
| *non c'erano → il TEMPO 2 li ha creati* | **SÌ. È questa.** |
| *c'erano ma il conteggio cambia* | **NO.** Non è sensibilità del criterio: è presenza contro assenza |

**`Q8` non ha reso visibile un difetto preesistente: ha intercettato una REGRESSIONE.**
**E l'ha fatta vedere prima che entrasse in una campagna** — che è esattamente ciò per cui il rigiro
dei sigilli esiste.

**La decisione è di Luca**, fra le vie già elencate: rimisurare `Y5`, trattare `rho_sorgente ≤ 0`
come caso a sé, o revertire il TEMPO 2 — **ma Q4 ha dimostrato che il difetto che il TEMPO 2 corregge
è REALE**, quindi un revert riporterebbe letture miste `t`/`t+1` note.

> **E una via che NON propongo, perché il mandato la vieta e ha ragione: il pavimento su
> `rho_sorgente`. Sarebbe la QUINTA rete sopra lo stesso buco.** Se quei nodi non hanno campo, **il
> problema è perché non ce l'hanno** — e ora sappiamo che è qualcosa che il TEMPO 2 ha cambiato,
> **non la maturazione del kernel.**
