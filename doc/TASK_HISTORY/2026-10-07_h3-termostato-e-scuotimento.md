# `H3` — **CHI SCALDA IL VUOTO: il termostato o lo scuotimento?** *(2026-10-07 sera, mandato di Luca + integrazione)*

> ### ⛔ **SOLO MISURA E DIAGNOSI. Nessuna legge si tocca**, il simulatore resta
> ### **`b8c21049`**, e i due interventi dei bracci diagnostici stanno ### **nello
> strumento** e sono ### **dichiarati**.

> ### 📌 **Committato e pushato PRIMA dello strumento e PRIMA delle corse.**

---

## 0. ✔ **IL FATTO, VERIFICATO DAI JSON DI `A-S1`** *(non ripreso dal mandato)*

`std(phivel)`, nei **due** bracci di `A-S1` *(`55a7edc`)*:

| passo | VUOTO `H1` | masse `H1` | VUOTO controllo | masse controllo |
|--:|--:|--:|--:|--:|
| `1` | `0.4339` | `0.2063` | `0.4339` | `0.4641` |
| ### **`50`** | ### **`3.5176`** | `1.0930` | ### **`3.5157`** | `1.2564` |
| `150` | `3.7198` | `1.7392` | `3.6622` | `1.8082` |
| ### **`400`** | `4.4323` | ### **`3.8415`** | `4.3904` | ### **`4.2214`** |
| `500` | `4.9182` | `4.6856` | `4.8188` | `5.1832` |

### ✔ **IL FATTO REGGE, ED È IDENTICO NEI DUE BRACCI:** il vuoto va `0.43 → 3.52` in
### **`50` passi** *(`×8.1`)* e poi `4.82–4.92`; le masse restano sotto e lo
### **raggiungono verso il `400`** — ### **dove l'AUC scende sotto `0.5`.**
### ⭐ **La lettura del guardiano è compatibile con i numeri: le masse non si sfasano per un
difetto LORO, vengono TERMALIZZATE da un vuoto che si scalda.**

---

## 1. ⛔ **I DATI NON ESISTONO GIÀ — e l'ho cercato, non supposto**

| grandezza | dove vive nel codice | esiste già da qualche parte? |
|---|---|---|
| `xi_termo` | ### **attributo di `net`** *(`:4064`)*, e ha una ### **colonna CSV** *(`:12248`, `:12811`)* | ### ⛔ **NO:** la colonna la scrive ### **`_diag_completa`** *(`:12168`)*, che il nostro percorso *(`_passo.passo_pieno`)* ### **non chiama mai** — e ### **nessun CSV del repo ha `xi_termo` in intestazione** *(cercato in tutti i `.csv` tracciati e su disco)* |
| `E_cin` | ### **variabile LOCALE** di `step` *(`:7711`)* | ### ⛔ **NO** |
| `T_target`, `cs_rappr`, `err_rel` | ### **variabili LOCALI** *(`:7738`-`:7753`)* | ### ⛔ **NO** |
| `P_eq = median(d0[:n])` | ### **variabile LOCALE** *(`:7735`)* | ### ⛔ **NO** |
| `Lam = mean(\|psi\|²)` | `lambda_vuoto(net)`, ricalcolata a ogni `scuoti_vuoto` | ### ⛔ **NO** |

### ✔ **E nei json di `A1` e `A-S1`: nessuna delle sette è presente** *(cercate per nome nel
testo completo dei due file)*.
### ➜ **La misura va costruita.**

---

## 2. ⭐ **COME SI LEGGONO SENZA TOCCARE NIENTE — e il bilancio è ESATTO, non stimato**

### I QUATTRO FATTI DI CODICE CHE LO RENDONO POSSIBILE *(sondati a runtime, non assunti)*

| | |
|---|---|
| ### **`TEMPO_SEGNO = False`** | ### ➜ **`dt_n_s = dt_n`** esattamente *(`:7547`; il ramo `:7561` non gira)* |
| ### **`FORK_SU2_MEM = True`** | ### ➜ lo step ### **SALVA `self._r_corrente = r`** *(`:7544`)*, e `dt_n = DT · r` *(`:7500`)* |
| ### **`REGIME = 'deterministico'`** | ### ➜ gira il ramo del ### **termostato** *(`:7760`)*, ### **mai quello di `G_PH`** *(`:7762`)* |
| `M_PH = 1.0`, `DT = 0.01`, `CS_DINAMICO = True` | letti a runtime |

### ⛔ **E UNA STRADA CHE HO PROVATO E SCARTATO, perché è giusto dirlo:** `self.eta += dt_n`
*(`:7562`)* sembrava dare `dt_n = Δeta` gratis. ### **È FALSO su questa scena:** `:5147` mette
### **`eta = inf`** sui nodi del vuoto DATO, e il sondaggio dice ### **`12802` su `12802`
infiniti.** ### **`inf − inf` con `np.seterr(invalid='raise')` SOLLEVA**, e infatti la mia prima
sonda è caduta lì.

### ✔ **LA DECOMPOSIZIONE, con involucri di SOLA LETTURA** *(la tecnica già collaudata e
byte-inerte su `220` passi attraverso una nascita)*

```
p0 = phivel all'INIZIO del passo
p1 = dopo scuoti_vuoto      ->  D_scuoti = p1 - p0          ESATTO (involucro)
p2 = dopo step              ->  D_step   = p2 - p1          ESATTO (involucro)
D_termostato = - DT * r * xi_termo * p1 / M_PH               ESATTO (r e xi letti da net)
D_coppia     = D_step - D_termostato                         ESATTO per definizione
```

### **E l'attribuzione di `Δ(phivel²)` è un'identità, non un'approssimazione:**

```
p2^2 - p0^2 = [2*p0*D_scuoti + D_scuoti^2] + [2*p1*D_term] + [2*p1*D_coppia] + D_step^2
```

### ⚠ **I termini quadratici si riportano SEPARATI e DICHIARATI**, non spalmati su una voce:
`D_scuoti²` sta con lo scuotimento *(è la varianza che inietta)*, e ### **`D_step²` è un
RESIDUO INCROCIATO** fra termostato e coppia, che ### **non si può attribuire** e si scrive
come tale.

### ✔ **E UN CONTROLLO POSITIVO CHE NON COSTA NIENTE:** `ampiezza` di `scuoti_vuoto` si
ricalcola ### **senza RNG**, e `D_scuoti = normal(0,1)·ampiezza`, quindi
### **`rms(D_scuoti) ≈ rms(ampiezza)`.** ### ⛔ **Se non coincidessero, avrei ricostruito male
la legge, e lo saprei.**

### ⛔ **`calcio` NON si ricalcola:** userebbe `net.rng` e ### **cambierebbe la dinamica.**

---

## 3. ⭐ **IL PUNTO `1` DELL'INTEGRAZIONE: `Λ` È GLOBALE, E AGISCE DUE VOLTE**

La legge, letta dal codice *(`:915`-`:920`)*:

```
Lam      = lambda_vuoto(net) = mean(|psi[:n]|^2)        <-- GLOBALE
I2       = |psi[:n]|^2                                   <-- locale
ampiezza = sqrt(stress_nodo + 1e-9) * sqrt(Lam) / (1 + I2/Lam)
calcio   = normal(0,1,n) * ampiezza
```

### ⛔ **`Λ` ENTRA DUE VOLTE, E NELLO STESSO VERSO:**

| | |
|---|---|
| `× √Λ` | ### **un `Λ` che cresce ALZA il calcio ovunque** |
| `/ (1 + I2/Λ)` | ### **un `Λ` che cresce INDEBOLISCE la soppressione** — la protezione delle masse *(dove `I2` è alto)* ### **si scioglie quando `Λ` sale** |

### ➜ **Quindi, SE lo scuotimento è la voce principale, la causa non è «il termostato»: è
### la COPPIA «obiettivo globale» + «riferimento globale».** ### **Si misura `Λ` a ogni
passo, e `ampiezza` mediana per classe.**

---

## 4. ⛔ **I CRITERI, FISSATI ADESSO** *(mandato di Luca)*

| | condizione |
|---|---|
| ### ✔ **`H3` CONFERMATA** | nei primi `50` passi: `E_cin < T_target` ### **per la maggior parte dei passi**, `xi_termo` ### **negativo** *(rifornente)*, ### **E** il termine del termostato è la ### **voce PRINCIPALE** dell'aumento di `<phivel²>` nel VUOTO |
| ### ⛔ **`H3` SMENTITA** | la voce principale è ### **un'altra** — e ### **si dice QUALE** |
| in più | se ### **`T_target` cresce** nel tempo, e ### **quanto di quella crescita viene da `median(d0)`** |
| ### **`IL TERMOSTATO SCIOGLIE LE MASSE`** | in ### **`B-T`** l'AUC al `400` è ### **`>= 0.85`** *(controllo `0.4679`)* |
| ### **`LO SCUOTIMENTO SCIOGLIE LE MASSE`** | in ### **`B-S`** l'AUC al `400` è ### **`>= 0.85`** |
| entrambi | ### **si dice** |
| nessuno dei due | ### **`H3` è SMENTITA come CAUSA**, e si torna ad `A-S2` *(`H2`)* |

---

## 5. ⭐ **LE PREVISIONI, PRIMA DELLE CORSE — e questa volta con l'ARITMETICA**

### ⛔ **`PH3-1`: `H3` SARÀ SMENTITA SULLA TERZA CLAUSOLA — il termostato NON è la voce principale.**

### **Le prime due clausole le do per vere**, e il sondaggio a `5` passi le mostra già:
`T_target ≈ 5.44` contro `E_cin ≈ 0.156` → ### **l'energia è `35 ×` SOTTO l'obiettivo**,
`err_rel ≈ −0.97`, e `xi_termo` accumula ### **negativo**: `−0.0227, −0.0415, −0.0598,
−0.0774, −0.0945`.

### ⛔ **MA IL TERMOSTATO È MOLTIPLICATIVO, E L'ARITMETICA NON TORNA:**

```
il suo effetto per passo e'  -dt_n * xi * phivel,  cioe' una crescita RELATIVA di (-dt_n*xi)
dt_n = DT * r = 0.01 * 0.85 = 0.0085        (r mediana MISURATA al sondaggio)
al passo 5:  -0.0085 * (-0.0945) = +0.0008  ->  +0.08 % per passo
su 50 passi:  (1.0008)^50 = 1.04            ->  +4 %
AL TETTO |xi| = 2 (la guardia):  -0.0085*(-2) = 0.017  ->  (1.017)^50 = 2.3
```

### ➜ ### **NEMMENO SATURANDO LA GUARDIA il termostato arriva a `×8.1`.**
### **Il fattore misurato è `3.5176 / 0.4339 = 8.11`.**

### ⭐ **`PH3-2`: la voce principale sarà `scuoti_vuoto`**, che è ### **ADDITIVO** e inietta
varianza: `std` dopo `N` passi `≈ √N · rms(ampiezza)`, cioè
### **`√50 · a = 7.07 a`**, e per arrivare a `3.5` basta ### **`a ≈ 0.50`** — plausibile con
`√Λ ≈ 1.6` *(`Λ` misurata `1.68 → 2.58` in `5` passi)*.

### ⭐ **`PH3-3`: `B-S` mostrerà l'effetto grande, `B-T` quello piccolo.** AUC al `400`:
### **`B-S >= 0.85`** *(criterio soddisfatto)*, ### **`B-T < 0.85`.**

### ⚠ **`PH3-4`: `T_target` cresce POCO e per via di `median(d0)`.** Misurato al sondaggio:
`P_eq` va `1.86552 → 1.87058` in `5` passi *(`+0.27 %`)*, mentre `cs_rappr` ### **cala**
`1.7072 → 1.6960`. ### **Quindi la crescita di `T_target` sarà lenta e NON sarà il motore
del riscaldamento dei primi `50` passi.**

### ⚠ **`PH3-5`: `Λ` cresce**, e ### **la soppressione delle masse si indebolisce**: la
mediana di `ampiezza` nelle masse si avvicinerà a quella del vuoto ### **prima** che le `std`
si incontrino.

> ### ⛔ **E SE MI SBAGLIO SU `PH3-1`, È UN RISULTATO MIGLIORE DI UNA CONFERMA:** vorrebbe
> dire che `xi_termo` satura la guardia `±2`, e ### **una guardia saturata è un difetto a
> sé** *(`A11`)*.

---

## 6. ⛔ **I DUE BRACCI DIAGNOSTICI — e uno dei due NON fa quello che il suo nome dice**

### `B-S` *(senza scuotimento)* — ### ✔ **PULITO**

`scuoti_vuoto` è ### **una funzione di MODULO**, e lo schedulatore la chiama con
### **`globals()[_nome](net)`** *(`:3046`, `_PASSO_MODULO = ('scuoti_vuoto',)`)*.
### ➜ **Sostituirla dallo strumento con una funzione della STESSA FIRMA che non fa niente
è esatto e reversibile**, e non tocca nessun file del simulatore.

### ⛔ `B-T` — **NON È «SENZA TERMOSTATO», E LO DICO PRIMA DI GIRARLO**

### **Verificato dal codice, come il mandato chiede: porre `xi_termo = 0` NON attiva `G_PH`.**
Il ramo è scelto da ### **`if REGIME == "deterministico"`** *(`:7705`)*, non da `xi_termo`:
`G_PH` vive ### **solo nell'`else`** *(`:7762`)*, e `REGIME` ### **non si tocca.**

### ⚠ **MA LO STEP RICALCOLA `xi_termo` DENTRO DI SÉ**, prima di usarlo:

```
self.xi_termo += dt_scal * (err_rel - self.xi_termo) / tau_termo     (:7758)
delta_phivel   = dt_n_s * (coppia - self.xi_termo * _phivel_t)/M_PH  (:7760)
```

### ➜ **Azzerarlo DA FUORI prima di ogni passo non dà `xi = 0` DURANTE il passo:** dà
### **`xi = dt_scal·err_rel/tau_termo`**, cioè ### **UN passo di accumulo invece di tutti.**
Con i numeri del sondaggio *(`dt_scal ≈ 0.0085`, `tau_termo = √(1/5.44) ≈ 0.43`,
`err_rel ≈ −0.97`)*: ### **`xi ≈ −0.019` per passo**, contro un valore accumulato che tende a
### **`−0.97`.** ### ➜ **Una soppressione di circa `50 ×`, non un azzeramento.**

> ### ⛔ **QUINDI `B-T` SI CHIAMA «TERMOSTATO SENZA MEMORIA», NON «SENZA TERMOSTATO»**, e il
> referto riporterà ### **il `xi_termo` RESIDUO che lo step ha davvero usato.** ### **Un vero
> zero non è raggiungibile da fuori senza toccare la legge, e quella sarebbe una CURA.**

### ⚠ **IL RISCHIO, DICHIARATO** *(dal mandato)*: senza freno l'energia può salire, o la rete
bloccarsi. ### **Se una corsa diverge — `NaN`, valori fuori scala, una guardia che scatta —
la fermo e lo riporto: anche quello è un risultato.** ### ⭐ **E qui il freno è
`−xi·phivel` con `xi` NEGATIVO, cioè già RIFORNENTE: toglierlo dovrebbe RAFFREDDARE, non
scaldare.**

---

## 7. ⭐ **LA STELLA POLARE** *(`L-STELLA`)*

| | |
|---|---|
| `A14` | ### **NON SI APPLICA:** nessun termine di nessuna legge è aggiunto, tolto o cambiato. I due bracci spengono/azzerano ### **dall'esterno**, per vedere, e il simulatore gira identico |
| `ROBUSTEZZA-FISICA` | ### **NON SI APPLICA:** nessuna legge nuova. ### ⚠ **Ma c'è un gradino di robustezza della MISURA, dichiarato:** `B-T` non è un azzeramento |
| numeri o leggi aggiunti | ### **ZERO.** `xi_termo = 0` non è un numero tarato: è ### **l'assenza** del termine |
| verso EM-curvatura | ### **NON SI APPLICA** |
| ### **emergente o imposto** | ### ⛔ **IMPOSTO, e dichiarato:** i due bracci sono ### **amputazioni**, non modelli. Servono a ### **nominare il colpevole**, non a proporre una cura — e ### **la cura è decisione di Luca** |

---

## 8. TODO

- [ ] **(a)** questo task history, ### **committato PRIMA**;
- [ ] **(b)** `csv/_test_fork/_termo_h3.py` + collaudo, col caso che ### **DEVE fallire**;
- [ ] **(c)** la ### **byte-inerzia** degli osservatori *(già collaudata)* sul braccio base;
- [ ] **(d)** le tre corse: ### **base `300`**, ### **`B-T` `500`**, ### **`B-S` `500`**;
- [ ] **(e)** ### **UN SOLO referto** per il bilancio, `B-T` e `B-S`;
- [ ] **(f)** ### **`H3` registrata nella voce `SCIOGLIMENTO-FASE`** accanto a `H1` e `H2`;
- [ ] **(g)** poi ### **FERMO. Nessuna cura: la decisione è di Luca.**
