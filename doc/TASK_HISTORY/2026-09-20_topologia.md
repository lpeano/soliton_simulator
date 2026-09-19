# TASK HISTORY — **la forma del grafo: misurare, non nominare**

**Data** 2026-09-20 · **branch** `fork-su2` · **HEAD** `f5d7562` · **blob** `775ceab7` · albero
**pulito** · dati: i **45 snapshot** di `_g6000` (passi 60-2700) e il dump del 2700.

> **NESSUN RUN NUOVO. NESSUNA CURA. Il simulatore non si tocca.**
> **⚠ NESSUN NOME NEL REFERTO.** *«ragnatela», «rete cosmica», «filamenti», «ammassi»* sono
> un'**immagine**, ed è la **terza di oggi** dopo la Y e il protone — **le prime due sono cadute
> sotto misura.** **Si riporta la FORMA, coi numeri.**

---

## 1. L'ORDINE È INVERTITO DI PROPOSITO: **la QUARTA lettura per prima**

**Se i nodi di grado 2 sono semplicemente NEONATI NON ANCORA ALLACCIATI, la topologia non è una
struttura: è un transitorio demografico** — e tutte le altre misure cambiano significato.

**Il test:** si prendono i nodi con **grado 2** a un passo, e si **segue il loro grado** negli
snapshot successivi *(gli indici sono stabili: i nodi si appendono in coda, `CLAUDE.md` §9)*.

- **il grado CRESCE col tempo** → **si allacciano: è demografia, non topologia.** **Le altre misure
  vanno lette come istantanee di un transitorio;**
- **resta 2 per sempre** → **è una struttura stabile**, e le misure ①-④ hanno senso.

## 2. LE MISURE, in ordine

**① L'ISTOGRAMMA COMPLETO dei gradi** *(bin logaritmici)*, non i percentili: **quanti picchi? c'è
popolazione in mezzo? quale frazione in ciascuno?**

**② IL CLUSTERING** *(triangoli chiusi / possibili)*, **distribuzione e non media**, e **SEPARATO
per i due gruppi di grado** (A3c). *Alto sui densi = compatti; ~0 sui grado-2 = catene.*

**③ LE CATENE — la misura che decide.** I grado-2 sono collegati **fra loro**? Se sì: **lunghezza**
delle sequenze, e **i due estremi sono nodi di grado alto DIVERSI o lo STESSO?**
*Grumi diversi = ponti. Stesso grumo = code.* **È la distinzione che decide.**

**④ LA REGOLARITÀ:** la lunghezza delle catene ha **una scala caratteristica** (un picco) o è
**larga senza struttura**? E il numero di catene per grumo è **costante o distribuito**?

## 3. LE QUATTRO LETTURE, fissate PRIMA

| # | esito | conclusione |
|---|---|---|
| **A** | gradi **bimodali** + clustering alto sui densi + catene fra grumi **diversi** | la forma è **grumi collegati da catene**. Si riporta la forma, **nessun nome** |
| **B** | gradi **continui**, nessun secondo picco netto | **l'immagine cade**, e si scrive che cade |
| **C** | grado 2 **ma clustering alto** | **non sono catene: sono periferici attaccati ai grumi.** Code, non ponti |
| **D** | i grado-2 sono **neonati che si allacciano** | **non è topologia: è un transitorio demografico.** **È la più probabile, e si verifica per prima** |

## 4. I PRESIDI
- **A3c: mai una media su due popolazioni.** I due gruppi **sempre separati**;
- **il costo:** il clustering su **438 532** archi può essere caro. **Si misura il tempo su un
  campione prima di lanciarlo sull'intero grafo**, e se serve **si campiona DICHIARANDOLO**;
- **uno snapshot alla volta**, mai tutti in RAM;
- **NESSUNA IDENTIFICAZIONE, NESSUN NOME.** I numeri e la forma.

## 5. COSA MI FA FERMARE
- **la lettura `D` che scatta** → si riporta che è demografia, e **non si costruisce una topologia
  su un transitorio**;
- **nessuna delle quattro** → si riporta, senza inventarne una quinta;
- **il clustering che costa troppo** → si campiona **dichiarandolo**, non si stima.
