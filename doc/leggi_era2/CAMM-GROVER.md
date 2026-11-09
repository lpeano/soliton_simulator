# `CAMM-GROVER`

> ### ⛔ **QUESTA SCHEDA E' GENERATA** da `primo_ordine/leggi/leggi.yaml` *(`primo_ordine/_genera.py`)*: ### **non si modifica a mano.**

| | |
|---|---|
| **tipo** | `pezzo_unitario` |
| **operatore** | `grover`, azione `nodo` |
| **ambito** | `psi_h` |
| **impronta della riga** | `1518e0ab958f5fc2` |
| **assiomi soddisfatti** | `A16` |


## LA SCHEDA, dalla tabella

`G(theta) = P_u + e^{i theta} (I - P_u)` nel NODO (punto `F1`), con `theta = pi dtau_nodo/dtau_rif`: mescola le estremita' di uno stesso nodo. ### ⭐ DAL 2026-10-15 E' UN FLUSSO PARZIALE (strada `(B)`, decisioni `B-3` e `B-4` di Luca): `G = 2 P_u - I = exp(i pi (I - P_u))`, quindi il Grover di prima E' questo flusso ALL'ANGOLO `pi` -- e a `theta = pi` torna AL BIT (`M-B1`, misurato su 250 tick contro `717bb60`). ### ⚠ E NON E' PIU' UN'INVOLUZIONE PER OGNI `theta`: lo e' SOLO a `theta = pi`. La frase <<la radice di una riflessione non e' una riflessione>>, che prima vietava una frazione, era VERA e NON LO E' PIU': la radice e' il flusso a `pi/2`. ### NON HA PARAMETRI, e non e' una semplificazione: il `2/d` viene dal GRADO del nodo, cioe' da una proprieta' del grafo -- `A1` e' rispettato perche' non c'e' nessun numero da tarare. ### AZIONE `nodo`: e' il SOLO pezzo che mescola estremita' diverse dello stesso nodo, ed e' per questo che NON si puo' scrivere come espressione in questo formato (un termine di nodo non vede i vicini): e' il posto `P4` del piano.

