# TASK HISTORY — le metriche del settore chirale. E `chi_basc` non RIBALTA: RISCRIVE

**Data** 2026-09-20 · **branch** `fork-su2` · **HEAD** `3a35aa1` · **blob** `27f1ab03`
*(sha1 byte grezzi; git `3437e260`)* · albero **pulito** · **nessun run.**

> **L'ordine si allunga:** **① le cure** *(fatte)* **→ ② il PANNELLO FEDELE → ③ QUESTE METRICHE +
> un giro breve → ④ il RUN a `sep = 4.0`.**
> **Questa task history è scritta PRIMA**, e il lavoro delle metriche viene **dopo il pannello**.
> **Le metriche devono essere BYTE-INERTI: leggono, non toccano.**

---

## 1. ⚠ IL FATTO CHE CAMBIA IL SENSO DELLA METRICA ④ — **verificato dal codice, prima di costruire**

**Il mandato dice che `chi_basc` *«RIBALTA i segni esistenti»*. Dal disco è più forte di così:**

```python
:3765   self.perc_chi[:self.n] = np.where(twn > soglia, 1, -1).astype(...)
        con  soglia = PHI_CRIT   e   twn = media sui vicini di |tw|
```

> **Non ribalta ALCUNI segni: RISCRIVE L'INTERO ARRAY, a ogni passo, da una soglia sulla
> torsione.** **`perc_chi` non è un lignaggio: è un OSSERVABILE DERIVATO del campo di torsione.**

**E l'ordine del ciclo lo rende definitivo:**

```
driver:   scuoti_vuoto  ->  step()  ->  mitosi()  ->  rilassa_disegno  ->  memoria_hebbiana_moto
                             ^ qui dentro sta chi_basc (:3765)   ^ qui nascono i nodi (:4294, :4415)
```

**La mitosi appende i segni ereditati (`:4294`, uguale al genitore) e la coppia di Schwinger
(`:4415`, `-perc_chi[aa]`) DOPO `chi_basc`. Al passo successivo `chi_basc` li SOVRASCRIVE TUTTI.**

> **Con `CHI_BASC = 1` — ed è `1` nel run (`P6`) — l'eredità chirale sopravvive ESATTAMENTE ZERO
> passi completi.**
> **Quindi `N(+1) − N(-1)` NON è una carica: è `#{nodi con twn > PHI_CRIT}` meno il resto.**
> **Non «`chi_basc` domina»: `chi_basc` SOSTITUISCE.**

**⚠ E UNA CONSEGUENZA SULL'`83 %` DEL PASSO 2700, più netta di quella del mandato:** non è che *non
valga per via delle quattro componenti* — **non è affatto una statistica di chiralità.** È
**la frazione di nodi che NON hanno completato un giro di olonomia** *(`twn <= PHI_CRIT`)*. È un
dato sulla **torsione**, letto come se fosse un dato sulla **chiralità**.

**⚠ E C'È UN SECONDO RISCRITTORE, che il mandato non nomina:** `:3786`, sotto `CHI_DA_SPINORE`
*(`= False` di default, e spento nel run)*, fa la stessa cosa dal segno di doppia copertura.
**Due leggi diverse riscrivono lo stesso array, e sono mutuamente esclusive per costruzione**
*(`chi_basc` ha `not CHI_DA_SPINORE` nella guardia)*.

## 2. I PUNTI DEL SETTORE CHIRALE, con le righe VERE

**⚠ Le righe del mandato sono SLITTATE** *(i contatori di `Z68`/`Z69` hanno spostato tutto)*.
**Ritrovate per CONTENUTO, non per numero:**

```
:602    calcio = calcio * net.perc_chi              violazione di C (candidato Sakharov)
:1927   semina:    perc_chi = concat([.., chi_nuovi])
:2060   opposti = perc_chi[a] != perc_chi[b]        COMPAT_CHI, spento
:3612   twn = (pi*0.5*(perc_chi[i] - perc_chi[j]))/PHI_CRIT     LA DIFFERENZA -> simmetria Z2
:3765   chi_basc:  perc_chi[:n] = where(twn > PHI_CRIT, 1, -1)  RISCRIVE TUTTO
:3786   chi_da_spinore: perc_chi[:n] = where(real(_ov) >= 0, 1, -1)   il SECONDO riscrittore
:4294   mitosi:    perc_chi = concat([.., perc_chi[a]])     EREDITA UGUALE -> romperebbe
:4415   Schwinger: perc_chi = concat([.., -perc_chi[aa]])   COPPIA OPPOSTA -> conserva
```

## 3. LE QUATTRO METRICHE, e come cambiano alla luce del §1

| # | metrica | cosa dice **oggi** |
|---|---|---|
| **①** | `N(+1)`, `N(-1)`, **e la DIFFERENZA** | con `CHI_BASC` on **non è una carica**: è una soglia sulla torsione. **Si misura lo stesso, ma si legge così** |
| **②** | `Sum \|psi\|^2` per segno, **e la loro differenza** | la differenza **non** cresce con l'espansione: **è il discriminante fra espansione e SCAMBIO** |
| **③** | **nati per ramo**: `:4294` contro `:4415` | resta un conteggio di NASCITE valido — **ma il suo effetto su ① è cancellato al passo dopo** |
| **④** | **l'effetto di `chi_basc`** | **riformulata**: non «quanti flip», ma **quanti nodi CAMBIANO SEGNO attraversando `:3765`** — si confronta `perc_chi` **prima e dopo**, nello stesso passo |

> **④ nella forma del mandato («quanti segni ribalta») non è misurabile come scritta**, perché il
> codice non ribalta: **assegna**. **La forma misurabile è il confronto prima/dopo**, ed è anche
> più informativa: dà **quanti** e **in quale verso**, che è ciò che il mandato voleva.

## 4. I VINCOLI, e la trappola
- **BYTE-INERTI. Il sigillo di byte-identità è BLOCCANTE;**
- **⚠ LA TRAPPOLA:** *«la metrica LEGGE gli attributi, MAI chiama una funzione che li SCRIVE»* —
  è il precedente di `lambda_vuoto`, che sembrava di sola lettura e chiamava `calcola_psi()`.
  **Per ciascuna delle quattro si verifica e si dichiara** quali attributi legge e che **non**
  chiama nulla che scriva;
- **nel CSV di progresso E negli snapshot** *(servono a run finito, non solo durante)*;
- **niente numeri scelti:** sono conteggi e somme;
- **i contatori dei nati per ramo devono POTER SCATTARE: si dimostra.**

## 5. COSA MI FA FERMARE
- **byte-identità che non torna** → una metrica sta toccando la fisica: **STOP**;
- **una metrica che richiede di chiamare una funzione che scrive** → **non si fa**, e si dichiara
  perché;
- **`N(-1)` identicamente zero, o i nati tutti su un ramo solo** → **è un reperto**, si riporta.

## 6. TODO
1. [fatto] il §1 verificato dal codice **prima** di costruire;
2. **il PANNELLO FEDELE** *(è il ②, viene prima)*;
3. le metriche byte-inerti, committate prima del sigillo;
4. sigillo di byte-identità → giro breve a `sep = 4.0` → riporto;
5. la voce nel registro *(la `Z2`, i tre punti, Sakharov e il **perché non basta**)* → checkpoint.
