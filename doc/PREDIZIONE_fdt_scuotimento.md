# PREDIZIONE — lo scuotimento contiene gia' una DISSIPAZIONE ALLINEANTE? (Kuramoto emergente?)

> **Scritta e committata PRIMA dell'analisi e dei test.** Branch `fork-su2`, blob **2277e9a0**.
> Data: 2026-09-14. **Nessuna modifica a `soliton_simulator.py`**: qui non si aggiunge niente al
> sistema, si misura cosa c'e' gia' dentro.

---

## 0. LA DOMANDA

Misurato finora: la dinamica dei Bloch e' **precessione pura** (Rodrigues, `:2021` — ruota
*attorno* al campo, **conserva** l'angolo fra `n` e l'asse, non allinea) **+ rumore + normalizzazione**.
Manca il termine **dissipativo** `n -> B` (il "tira verso", tipo Gilbert / Kuramoto). Senza quello:
congelato o rumore, e nient'altro.

**Ipotesi (fluttuazione-dissipazione):** un rumore porta con se' una dissipazione compagna, col
coefficiente **fissato dal rumore**, non scelto. Lo scuotimento fa `_nb += rumore` e **poi
normalizza** (`:1803-1804`). La normalizzazione di un versore perturbato **non e' neutra**: puo'
introdurre un drift sistematico. La domanda e' se quel drift **allinea ai vicini** (= Kuramoto
emergente, zero manopole) o se e' solo contrazione/isotropizzazione.

---

## 1. I TRE ESITI (definiti prima)

- **A (EMERGENTE):** il drift e' `~ -(coef)(n - <n_vicini>)`, cioe' un rilassamento **verso la media
  dei vicini**, col coefficiente fissato da `amp^2`. -> Kuramoto emergente, zero manopole.
- **B (CONTRAZIONE ISOTROPA):** il drift e' funzione **del solo `n`** (es. `-(coef)n`), senza
  direzione privilegiata dai vicini. -> nessuna dissipazione allineante nel rumore.
- **C (NESSUN DRIFT):** neutro all'ordine dominante. -> il FDT non morde qui.

> **DICHIARAZIONE: "Kuramoto emergente" e' confermato SOLO nell'esito A, e solo se il coefficiente
> ha SEGNO allineante e scala non trascurabile.** Un drift che esiste ma non guarda i vicini non e'
> un Kuramoto, comunque lo si chiami.

---

## 2. LA MIA PREDIZIONE, E UNA DICHIARAZIONE DI ONESTA' SUL "PRIMA"

**Sul rumore da solo (Test 3a) non ho un vero dubbio, e devo dirlo.** L'espansione a `O(amp^2)` di
`(n + a g)/|n + a g|` e' un calcolo di poche righe che so gia' fare, e soprattutto **c'e' un
argomento strutturale che non richiede nemmeno il calcolo**:

> Nel codice lo scuotimento del singolo nodo **non legge i vicini** (`:1803`: rumore locale
> indipendente per nodo, ampiezza da `I2` del nodo, poi normalizzazione). Il drift e' quindi per
> forza **funzione del solo `n`**. Una cosa che non guarda i vicini **non puo'** allinearli.

Quindi **predico B/C per il rumore da solo**, e lo predico con sicurezza, non per intuizione. Sarebbe
disonesto presentare come incerta una cosa che l'algebra decide in anticipo. Scrivo comunque
l'espansione per intero (§3 dell'esito) perche' la **forma** del drift e il suo **coefficiente**
sono informativi anche quando il verdetto e' B.

**Dove invece NON so, ed e' il vero esperimento: il Test 3b (precessione + rumore).** Li'
l'accoppiamento ai vicini **c'e'**, attraverso il campo `B`. E c'e' un meccanismo noto in fisica per
cui una rotazione ad **asse fluttuante** produce un drift medio che non e' una rotazione (il
*motional narrowing*): le componenti perpendicolari all'asse medio decadono piu' in fretta di quella
parallela. Se quel decadimento agisse come un rilassamento `n -> B`, sarebbe una dissipazione
allineante **emergente dalla combinazione**, non dal rumore da solo.
**Non ho calcolato se sopravvive qui**, e non voglio scommettere per non incorniciare la lettura.
Le due baseline gia' misurate (`chi = 0` congelato, `chi = 90` rumore) dicono che **nel sistema
completo non succede** — ma il sistema completo ha anche mitosi, crescita, densita' variabile: un
test isolato a due nodi puo' rivelare un effetto debole che li' e' sommerso. **E' per questo che 3b
si fa.**

---

## 3. IL CRITERIO NUMERICO (fissato prima)

Riferimenti sempre accanto al misurato:

| stato | angolo medio fra due Bloch |
|---|---|
| allineato | **0 gradi** |
| isotropo (casuale) | **90.000 gradi** (media di `sin(chi)/2`) |
| antipodale | 180 gradi |

- **3a (solo rumore+norm):** due Bloch a 60 gradi, iterare `n -> (n + a g)/|n + a g|`. L'angolo
  medio -> 0 (allinea), -> 90 (isotropizza), o resta?
  **Analitico e numerico DEVONO coincidere**: se non coincidono, la discrepanza e' essa stessa il
  reperto e ci si ferma (par.5 di CLAUDE.md).
- **3b (precessione + rumore + norm):** stessa cosa piu' la precessione di Rodrigues con `B` dai
  vicini. Allinea, disordina, o resta?
- In entrambi: controllare **`|<n>|` globale**, perche' `chi -> 0` da solo non distingue *domini* da
  *collasso* (lezione dell'esperimento Kuramoto, `doc/PREDIZIONE_kuramoto.md`).

---

## 4. SE L'ESITO E' B/C — il messaggio onesto, scritto prima

Non e' un fallimento, e non va presentato come tale:

> **"Lo scuotimento NON contiene una dissipazione allineante. Un Kuramoto in questo sistema sarebbe
> IMPOSTO, non emergente."**

E' un risultato **pulito e definitivo** su una domanda ben posta, e chiude una via: dice che la
struttura non si puo' ottenere gratis dal rumore che c'e' gia'. Sapere che una porta e' chiusa vale
quanto trovarla aperta — di piu', se evita di cercarci dietro per settimane.

---

## 5. COSA QUESTO TEST NON FARA'

Non aggiunge un termine `n -> B` al simulatore: sarebbe **Kuramoto imposto con un altro nome**, cioe'
esattamente cio' che il test deve saper distinguere. Non accende `KURAMOTO_SU2`. Non modifica lo
scuotimento. Non conclude su olonomia o gravita'. E un test a due nodi **non e' il sistema**: dice
cosa fa il meccanismo isolato, non cosa fa dentro la dinamica completa — dove infatti ci sono gia'
tre stati misurati, tutti senza struttura.


---

# 6. ESITO — aggiunto il 2026-09-14 DOPO l'analisi e i test

> Tutto sopra questa riga e' stato scritto e committato (`ad96669`) **prima**. Qui solo il risultato.

## 6.1 — Il drift: la forma esatta

Per `n' = (n + a g)/|n + a g|` con `g ~ N(0, I_3)`:

```
|n+ag|^-1 = 1 - a s - a^2 G/2 + (3/2) a^2 s^2 + O(a^3)        s = n.g ,  G = |g|^2
E[g]=0 , E[s]=0 , E[s g]=n , E[G]=3 , E[s^2]=1
                          ==>   E[n'] - n  =  -a^2 n  +  O(a^3)
```

Tre letture, tutte decisive:
1. il drift e' **parallelo a `n`**: nessuna componente trasversa, **nessuna rotazione media**;
2. dipende dal **solo `n`**: **nessuna traccia dei vicini `{n_k}`**;
3. `|E[n']| = 1 - a^2` e' la contrazione del **risultante** -> **diffusione isotropa pura**.
   Sulla sfera il drift a `O(a^2)` e' **NULLO**.

Verifica numerica (4·10^6 campioni, errore statistico 5.0e-04):

| amp | \|E[n']\| misurato | atteso `1-amp^2` | differenza | componente **trasversa** |
|---|---|---|---|---|
| 0.300 | 0.91010933 | 0.91000000 | 1.09e-04 | 2.32e-04 |
| 0.100 | 0.99001025 | 0.99000000 | 1.03e-05 | 6.37e-05 |
| 0.030 | 0.99909921 | 0.99910000 | 7.91e-07 | 8.98e-06 |
| 0.013 | 0.99983113 | 0.99983100 | **1.28e-07** | 8.20e-06 |

## 6.2 — Test 3a: solo rumore. L'angolo SALE.

Due Bloch a 60 gradi, `amp = 0.013`, 200000 campioni:

| passo | 0 | 10 | 50 | 100 | 300 | 1000 | 2000 | 3000 |
|---|---|---|---|---|---|---|---|---|
| chi (gradi) | 60.000 | 60.105 | 60.551 | 61.085 | 63.196 | 69.188 | 75.336 | 79.559 |

Sale verso 90 (isotropo). **Non scende mai verso 0.** E `<cos chi>` segue la legge della diffusione
pura `(1-amp^2)^(2k) cos(60)` entro ~1e-3.

## 6.3 — Test 3b: **il reperto che non aveva previsto nessuno**

| \|B\| | amp | chi ai passi 0 / 100 / 500 / 1000 / 2000 |
|---|---|---|
| 0.5 | **0.000** | 60.000 → 60.124 → 60.622 → 61.248 → **62.511** |
| 0.5 | 0.013 | 60.000 → 60.669 → 63.650 → 67.565 → 74.628 |
| 2.0 | **0.000** | 60.000 → 62.004 → 70.378 → 81.472 → **104.208** |
| 2.0 | 0.013 | 60.000 → 62.510 → 72.484 → 84.090 → 102.215 |
| 10.0 | **0.000** | 60.000 → 114.799 → 178.677 → 179.991 → **180.000** |
| 10.0 | 0.013 | 60.000 → 114.412 → 170.506 → 170.625 → 170.613 |

**Con il rumore SPENTO l'angolo non si conserva affatto.** Rodrigues conserva l'angolo fra **un**
vettore e il **suo** asse; qui i due nodi ruotano **l'uno attorno all'altro simultaneamente**, e la
coppia `(nA, nB)` non conserva nulla: e' un sistema dinamico non lineare a se', con un **punto fisso
ANTI-allineante a chi = 180** a campo forte.

> **La precessione mutua non e' neutra: e' attivamente DISORDINANTE.**

## 6.4 — VERDETTO: **ESITO B**, come predetto

Non solo manca il **"tira verso"** (dissipazione allineante): c'e' uno **"spinge via"**.

> **Lo scuotimento NON contiene una dissipazione allineante. Un Kuramoto in questo sistema sarebbe
> IMPOSTO, non emergente.**

Ed e' escluso **per dimostrazione**, non solo per misura: una cosa che non legge i vicini non puo'
allinearli, e l'espansione lo conferma nella forma esatta del drift.

## 6.5 — Errore mio, corretto e non nascosto

La riga di lettura che lo script stampava diceva *"con amp=0 la precessione CONSERVA l'angolo
esattamente"*. **Falsa**, smentita da tutte e tre le configurazioni. L'avevo scritta nello script
**prima** di girare: e' il commento stale contro cui mette in guardia il par.0 di CLAUDE.md, e
l'ho prodotto io. Corretta nel sorgente **dichiarando la correzione** invece di cancellarla, e lo
script rigirato da zero (seed fissi -> numeri identici).

## 6.6 — Una pista aperta, non verificata

Il vuoto si isotropizza in **~50 passi**, ma la sola diffusione a `amp = 0.013` ha tempo di
decorrelazione `~1/amp^2 ~ 5900` passi. **Non torna di due ordini.** Il §6.3 suggerisce la
spiegazione: **non e' il rumore a randomizzare in fretta, e' la precessione mutua.** Registrato
come pista, **non verificato**.
