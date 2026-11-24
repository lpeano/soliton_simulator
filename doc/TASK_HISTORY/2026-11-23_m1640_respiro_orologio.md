# [M1640] IL RESPIRO COME OROLOGIO SENZA ZERO: LO SPECCHIO ALLA PROVA *(Luca, 2026-11-23; letto alle `16:54` da `date`)* [[PROGETTO-MITOSI]]

> **[M1633] NON si fa** *(la precedenza in coda: vale l'ultima versione, e [M1640] lo dice mal posto, n.239)*. `git log --all --fixed-strings --grep "[M1640"` e `"[M1633"` alle `16:54`: **nessun commit.**

## 1. LE PREMESSE DAL CODICE

- **La carta:** `doc/CARTA_respiro_orologio.md` *(lo specchio coi numeri, le lenti, le righe del tick, S1-S4 con le righe, tre premesse del mandato dette prima: K1 contro un bin, K2 sugli sha1 degli stati impossibile, K3 allo `0.15%`)*.
- **Cosa NON so:** se la fase di V3 a `N` uniforme e' globale per la fisica *(tocca `psi`, non `phi`)*; se V2 a `N` uniforme riscala il tempo di tutto *(`cs` e' solo nel cammino)*; se il fit arriva allo `0.15%`; quanto costa un tick *(la tenuta FH: `10000` tick dalle `03:54` alle `05:07`, con altre corse insieme)*.

## 2. PROGETTAZIONE

- **`doc/referti_l2/respiro_N.py`:** `corsa --riga {N1, V2, V3, CTRL} --N x`; `casi_noti` *(N1 contro la tenuta S1 al bit fino a `k 500`, prima delle corse)*; `lettura` *(i fit, il battimento, K2 con CTRL)*. **Le cartelle:** `E:/soliton_simulator/controllo/M1640/<riga>_<N>`.
- **Cosa mi fa FERMARE:** il caso noto N1 = tenuta S1 cade; V2 non riscala *(K4)*.

## 3. TODO

1. la carta e questo task history, commit;
2. lo script, i casi noti, commit; le sei voci in coda a priorita' `0`, commit;
3. a corse finite: il referto, S20, la voce 6-STELLA, la relazione con processi e CPU; FERMO.
