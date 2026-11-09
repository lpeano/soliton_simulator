# -*- coding: utf-8 -*-
r"""**P3: `cs` ACCESO VIETATO SUL PRINCIPALE** *(Luca `2026-11-09` `13:16`; il task history `doc/TASK_HISTORY/2026-11-07_u1_prototipo_verificato.md`, sez. `20`)*. [[H-NUCLEO-CONGELATO]]

**Sul ramo `primo-ordine` `CAMM-FASE-VUOTO` legge l'energia SENZA lo zero simmetrico** *(v2 sta sul laterale)*: **a `cs` acceso il tick differisce da quello del laterale.**
**Finche' i rami non sono riuniti, nessuna corsa ne' prova con `cs` acceso sul principale.**

`vieta_cs()` *(chiamata all'import del pacchetto `solitone`)* **sostituisce `energia_pesata.applica` con una funzione che ALZA se `mot.cs` e `mot.lambda_c` sono tutti e due non `None`**,
e altrimenti chiama quella vera *(a `cs` spento il tick e' quello di prima AL BIT: la funzione vera ritorna subito)*. **L'interruttore e' quello di `H-NUCLEO-CONGELATO`:** il ramo `primo-ordine`
e `doc/NUCLEO_CONGELATO.md` che dice `CONGELATO` *(`csv/_nucleo_congelato.leggi_stato`)*.
### ⚠ **Il limite** *(`A9`)*: **copre solo gli script che importano `solitone`**; **una testa staccata non e' `primo-ordine`** *(come il presidio)*.
"""
import os
import subprocess

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(os.path.dirname(_QUI))
ATTIVO = [False]


class CsVietatoSulPrincipale(AssertionError):
    pass


def decidi(ramo, testo_stato):
    """### `True` = `cs` VIETATO. ### **Le righe di `_nucleo_congelato.decidi`, per il solo interruttore:** il ramo congelato e lo stato `CONGELATO`."""
    import _nucleo_congelato as NC
    if ramo != NC.RAMO_CONGELATO:
        return False
    stato, _dec = NC.leggi_stato(testo_stato)
    return stato == "CONGELATO"


def stato_del_repo():
    r = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=RADICE, capture_output=True)
    ramo = r.stdout.decode("utf-8", errors="replace").strip()
    p = os.path.join(RADICE, "doc", "NUCLEO_CONGELATO.md")
    testo = open(p, "rb").read().decode("utf-8") if os.path.exists(p) else None
    return ramo, testo


def vieta_cs():
    """### Se il repo e' sul principale congelato, `energia_pesata.applica` alza a `cs` acceso. Idempotente."""
    if ATTIVO[0]:
        return True
    ramo, testo = stato_del_repo()
    if not decidi(ramo, testo):
        return False
    import energia_pesata as EP
    vera = EP.applica

    def applica(mot, st, par, frazione):
        if mot.cs is not None and mot.lambda_c is not None:
            raise CsVietatoSulPrincipale(
                "P3 (Luca 2026-11-09 13:16): `cs` ACCESO sul ramo primo-ordine (mot.cs e mot.lambda_c non None): qui CAMM-FASE-VUOTO legge l'energia SENZA lo zero simmetrico"
                " (v2 sta su zero-nel-nucleo): nessuna corsa ne' prova con cs acceso sul principale finche' i rami non sono riuniti")
        return vera(mot, st, par, frazione)
    applica._vera = vera
    EP.applica = applica
    ATTIVO[0] = True
    return True
