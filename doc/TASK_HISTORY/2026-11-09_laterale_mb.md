# 2026-11-09 -- IL RAMO LATERALE `zero-nel-nucleo`: (m-b), I CONTI COL NUCLEO NUOVO CONTRO IL VECCHIO, DALLO STESSO STATO

> **Il ramo laterale** *(Luca `2026-11-08` `21:47`-`21:49`; `doc/NUCLEO_CONGELATO.md` sul principale)*: **il nucleo CON v2.** **Questo task history e i
> referti di questo ramo sono SUOI** *(la regola `2`)*: **sul principale va una riga che rimanda al commit di qui.** [[PIANO-2D-3D]] [[VUOTO-SUL-FONDO]]

## 1. LE PREMESSE DAL CODICE

- ### **La decisione** *(Luca `21:49`, (m-b))*: **«i conti per nodo e `E + E_ass` di un pezzo con il nucleo nuovo contro il vecchio, dallo stesso stato. Lettura scritta prima: UGUALI entro l'arrotondamento A MENO DELLA COSTANTE `pi` per norma.»** **Serve a preparare la riunione.**
- **Che cosa so** *(dal principale, `de46816d` e il task history di v2)*: **la DINAMICA e' identica al bit** *(il braccio 0, `6` chiavi)*; **`e_K` si sposta di `+pi` esatto** *(`-4.7122750003546425` -> `-1.5706823467648499`)*.
- **Dal codice** *(`csv/solitone/c0_cucitura.py` del principale, il ciclo della corsa: `AC.tick`, poi `BO.assorbi` con `c(t) F3`; `E_ass += e_pr - e_dopo` coi `conti_per_nodo` prima e dopo l'assorbimento)*: **`LC.conti_per_nodo(inc, mot, st, e_K, LAM_ZERO, par)` prende `e_K`: quindi lo spostamento di `e_K` entra nei conti, e se l'energia e `e_K` si spostano INSIEME la costante puo' cancellarsi in qualche termine.** ### **NON SO in quale termine sta la costante, ne' se si cancella.**
- **Il ramo laterale e' a `7c181cc4`** *(prima del merge)*: **`csv/solitone/corsa_accensione.py` identico al principale** *(controllato col `diff`)*; **`c0_cucitura.py` qui non c'e': il ciclo si ricopia nello script nuovo.**

## 2. LA MISURA E LE LETTURE, PRIMA DEI NUMERI

- ### **Lo script `csv/solitone/mb_costante.py`** *(su questo ramo)*: **lo stato completo di `TBS` a `100000`** *(la libreria, `E:`)*, **`N = 200` tick del ciclo della corsa** *(gli accumulatori del bordo dal pezzo prima)*; **a `t0` e alla fine: i conti per nodo per TERMINE, la norma `M`, `E + E_ass`, `e_K`, gli sha dello stato** *(in un `npz` fuori dal repo)*. **`--confronta A B`: i due `npz`.**
- **Si gira DUE volte, lo stesso blob:** **qui** *(il nucleo nuovo)* **e nel worktree del principale `wt_zero_padre`** *(il nucleo vecchio; il file copiato e tolto dopo, dichiarato)*.
- ### **LE LETTURE** *(Luca, e mie per i dettagli, dichiarate)*:
  - **(L0) la dinamica: gli sha dello stato alla fine UGUALI** *(se no, FERMO: il braccio 0 sarebbe smentito)*.
  - **(L1) `e_K` nuovo - vecchio = `pi` alla macchina** *(`|diff - pi| <= 4 eps pi`)*.
  - **(L2) per ogni termine dei conti, `(nuovo - vecchio)` sommato sui nodi, diviso `M`: o `0` o `pi`** *(entro `64 eps` relativi al termine: mia)* **-- cioe' la costante sta in UN termine, ed e' `pi` per norma; lo stampo per termine.**
  - **(L3) `E + E_ass` nuovo - vecchio, a `t0` e alla fine: la STESSA costante** *(`pi M0` o `0`, entro `64 eps` relativi)*, **cioe' costante NEL TEMPO: e' la condizione perche' la riunione possa dichiarare lo spostamento e confrontare le corse vecchie.**
  - **Se L2 o L3 non tornano: FERMO, e lo scrivo** *(la riunione non si prepara senza capire dove sta la costante)*.
- ### **IL DEVE FALLIRE:** **lo stesso confronto con `N` diverso nei due bracci** *(`200` contro `199`)*: **L0 DEVE fallire** *(il confronto sa dire «diverso»)*.
