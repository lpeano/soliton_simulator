# IL REGISTRO DELLE CORSE DELL'ERA 2

> **APPEND-ONLY. Si scrive SOLO con `csv/solitone/_registro_corse.py`** *(`apri`, `tappa`, `chiudi`)*, **mai a mano.** Il task history: `doc/TASK_HISTORY/2026-11-13_registro_corse.md`; la skill: `.claude/skills/registro-corse/SKILL.md`.
>
> - **una riga per evento, `- {json}`:** `ev` = `APERTO` *(l'ora, `HEAD`, l'impronta dei file del nucleo di `doc/NUCLEO_CONGELATO.md`, il comando verbatim)*, `TAPPA` *(il punto raggiunto)*, `CHIUSO` *(`FINITO`, `FERMATO`, `FALLITO`, il punto esatto)*;
> - **al piu' UNA `lunga` e UNA `breve` aperte insieme; mai lo stesso nome aperto due volte; `forza` solo con una decisione di Luca, scritta nella voce;**
> - **dopo un riavvio una voce rimasta APERTA si chiude `FERMATO (riavvio)` all'ultima tappa SOLO dopo che Luca l'ha vista: fino ad allora blocca le corse del suo tipo.**

## GLI EVENTI

