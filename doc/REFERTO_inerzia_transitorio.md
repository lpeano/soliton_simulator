# REFERTO — ①: **la diagnosi dimensionale è CONFERMATA, e più forte. Ma la verifica ② blocca il cablaggio.**

**Blob al momento della verifica:** `2d54ba3` (byte grezzi `4eee4610`), HEAD `231a8a5` — **coincide
con quello del mandato** (`2d54ba3a`). **Nessun cablaggio di ①.**

Il mandato §2.2 dice: *«Se `inerzia` si calcola PRIMA di `:3137`, i nuovi archi hanno `peq`
indefinito: **misuralo, e se accade FERMATI e riporta — non inventare una via**.»* **Accade.**

---

## 1. LA DIAGNOSI DEL §1 È GIUSTA — e la misura è **più severa** di come il mandato la scrive

Il mandato sostiene che `_fatt_cs` (il fattore `cs⁻²`) **non arriva a destinazione** perché il
pavimento `1e-6` lo mangia. **Misurato, dentro `_passo_spinoriale`, sui valori veri:**

| passo | mediana `rho_s` | mediana `_fatt_cs` | max `_fatt_cs` | **al pavimento** | mediana `inerzia` | mediana `T²` |
|---|---|---|---|---|---|---|
| 2 | 7.28e-12 | 1.126 | 1.168 | **100.00 %** | **1e-06** | 0.7505 |
| 12 | 5.40e-11 | 1.535 | **6.430** | **100.00 %** | **1e-06** | 1.029 |
| 24 | 1.15e-09 | 1.588 | 5.585 | **100.00 %** | **1e-06** | 1.084 |

> **Il mandato dice «99.7 %». La misura dice 100.00 %, a ogni passo.**
> **`inerzia` non è «quasi sempre al pavimento»: È il pavimento. È la costante `1e-6`.**
> `_fatt_cs` sale fino a **6.43** — **il fattore `cs⁻²` è vivo e non serve a nulla.**

**E il divario dimensionale è quello previsto:**
```
T^2 mediano                  = 1.029
inerzia mediana OGGI         = 1e-06
rapporto                     = 1.03e+06
```
**Un fattore un milione fra ciò che l'inerzia è e ciò che, per dimensione, dovrebbe essere.**

**Questo è il risultato principale del giro, e non dipende dal cablaggio:** la diagnosi del mandato
non è un'ipotesi, **è misurata**.

---

## 2. LE QUATTRO VERIFICHE PRELIMINARI

### ① `peq` disponibile? — **SÌ**
`self.i`/`self.j` sono allineati agli archi e `_deg` ai nodi **in tutti i passi osservati**: la
proiezione del GATE B usa una topologia **aggiornata**, non vecchia.

### ② `peq` può essere `NaN` o `<= 0` lì? — **SÌ. ED È IL BLOCCO.**

`_passo_spinoriale` è chiamato a **`:3062`**; la calibrazione di `peq` è a **`:3147`**. L'inerzia si
calcola **prima**, nello stesso passo. Misurato:

```
passo   archi     peq NaN        peq <= 0        peq_nodo <= 0
  0     14134     14134 (100%)        0            360 / 360     <- TUTTI i nodi
  1     14134         0          14134 (100%)      360 / 360     <- TUTTI i nodi
  2+    14134         0              0                  0        <- pulito, sempre
```

**Non sono «i nuovi archi»: sono TUTTI, per due passi.** E `peq_nodo` è **zero su tutti i nodi**,
quindi `rho_sorgente / peq_nodo` è **`0/0` = NaN** (passo 0-1, dove anche `rho` è ~0).

**Perché è grave, e non è lo stesso caso di `peq` alla nascita:**
`inerzia` entra in `omega_new`, che finisce in **`self.omega_s`** — la **memoria persistente**. Un
`NaN` lì **non è un valore sbagliato per due passi: contamina il run per sempre.**

**E il pavimento non protegge:** `np.maximum(NaN, 1e-6)` **è `NaN`**, non `1e-6`. Oggi il pavimento
salva il transitorio perché `rho * _fatt_cs` vale `0`, e `max(0, 1e-6) = 1e-6`. Con un rapporto che
produce `NaN`, quella rete **non c'è più**.

### ③ `_tempo_luce_nodo` chiamabile lì? — **SÌ, senza ricalcoli**
Restituisce valori sani in ogni passo: `T` da **0.74** a **1.82**, mediana **0.82 → 1.04**.
`T² ~ 0.67 → 1.08`, **coerente con la stima `~0.77` del mandato.** Nessuno snapshot necessario.

### ④ `_fatt_cs` va rimosso? — **SÌ, e c'è un FATTO NUOVO**

```
occorrenze di `_fatt_cs_ultimo` nel CODICE: 1  ->  SOLO LA SCRITTURA
```
Il commento dice *«per la metrica (solo lettura a valle)»*. **A valle non c'è nessuno.**
**Quarto caso della stessa famiglia** (`_passo_spinoriale` con docstring «ORFANO» ma **vivo**;
`VERSO_CHI` cablato ma **muto**; `spin_locale` definita e **mai chiamata**): **lo stato di vita del
codice non è leggibile dal codice.**
**Conseguenza operativa:** togliere `_fatt_cs` dall'inerzia **non rompe nessun consumatore**, e
lasciarlo darebbe `cs⁻⁴`. **Va rimosso** — e `self._fatt_cs_ultimo` può restare come diagnostico,
dichiarandolo tale.

### ⑤ *(non chiesta dal mandato, imposta da un riscontro già committato — voce Z1)*

```
correlazione rho_sorgente <-> |psi|^2, per passo:
  1.000  1.000  0.992  0.487  0.612  0.683  0.718  0.472
```
`_rho_sorgente()` restituisce `rho_spin` (campo **emesso**) con `CAMPO_SPINORIALE` ON, mentre `peq`
insegue `|psi|²`. **Ai primi passi coincidono; poi divergono e la correlazione crolla a ~0.5.**

**⚠ MA DEVO CORREGGERE COME AVEVO ETICHETTATO QUESTA OBIEZIONE.** Nel giro precedente l'avevo
chiamata **violazione di A3, «errore di popolazione»**. **Non lo è:** dopo la proiezione arco→nodo,
`rho_sorgente` e `peq_nodo` vivono **entrambi sui nodi** — la popolazione **è** la stessa, e su
questo **il mandato ha ragione**. L'obiezione vera è diversa e va detta col suo nome: **è una
questione di COERENZA DI GRANDEZZA**, non di popolazione statistica. **Più debole di come l'avevo
scritta**, e va corretta.

**E una seconda mia obiezione CADE del tutto.** Avevo scritto che togliendo il pavimento l'inerzia
**si annulla** (`min = 0` su 6 nodi). **Questo mandato NON toglie il pavimento** — lo dice
esplicitamente e ne spiega la ragione (`omega = coppia/inerzia`: inerzia minore = omega maggiore).
**Con il pavimento mantenuto, quella obiezione non si applica.** Era corretta contro un'altra
proposta, non contro questa.

---

## 3. DOVE SIAMO — **lo stesso difetto a monte ha ora fermato DUE correzioni**

| correzione | fermata da |
|---|---|
| `peq` alla nascita *(mandato precedente)* | `psi` è **zero** quando gli archi nascono |
| **① `inerzia`** *(questo mandato)* | `peq_nodo` è **zero su tutti i nodi** ai passi 0-1 |

**È la stessa radice:** `psi` non viene calcolato prima del primo `step`, quindi **nel transitorio
di accensione ogni grandezza derivata è zero** — e ogni correzione che costruisca un **rapporto fra
grandezze di stato** ci inciampa.

**Questo promuove il transitorio da curiosità a BLOCCO STRUTTURALE.** Non è più «due passi su
sessanta, irrilevante»: è **il muro contro cui si ferma la bonifica**.

---

## 4. COSA LO SBLOCCHEREBBE — **e non lo decido io**

1. **Calcolare `psi` una volta alla costruzione della scena**, prima del primo `step`. Renderebbe
   `rho`, `peq` e il rapporto **definiti fin dal passo 0**, e sbloccherebbe **entrambe** le
   correzioni ferme. **Ma è un cambio del percorso di inizializzazione, non una bonifica**, e
   cambia il seme di ogni run esistente. *(Lo avevo già indicato in `doc/REFERTO_peq_nascita.md`
   §5.1; ora ha una **seconda** prova a sostegno.)*
2. **Oppure**: una convenzione esplicita per il rapporto quando lo sfondo non è definito — p.es.
   *«un nodo senza sfondo misurabile è al proprio sfondo»*, cioè rapporto `= 1`, da cui
   `inerzia = T²`, il valore **dimensionalmente puro**, senza parametri. **È una scelta di
   convenzione, non una deduzione**, e il mandato vieta di inventarla: **la propongo, non la cablo.**
3. **Oppure**: si accetta che ① valga **dal passo 2** e si dichiara il transitorio come dominio
   escluso, con un ramo **contato** (P5). **È la via meno invasiva, ma introduce un ramo che scatta
   al 100 % per due passi** — ed è esattamente la forma che **A3b** condanna, anche se su una
   finestra breve.

**Nessuna delle tre è una bonifica**, ed è per questo che mi fermo.

---

## 5. COSA NON HO GUARDATO

Il mandato §5 vieta di misurare, riportare o commentare `chi`, `|<n>|`, autocorrelazione,
**`theta`**, `omega/sqrt(n)`, `L_tot`, MISURA U, `cs_std/cs`. **Non compaiono in questo referto e
non sono stati calcolati.** In particolare **`theta` non è stato guardato**, ed è corretto così:
è il numero che ① punta a muovere, e si guarderà a bonifica finita contro una predizione scritta
prima.
