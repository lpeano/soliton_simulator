# -*- coding: utf-8 -*-
"""**`D32`: i nomi dicono cio' che la grandezza E'.** *(mandato di Luca, 2026-09-27)*

> **Decisione di Luca:** *«il tempo proprio del sistema e' `r` (e `dt_e` sull'arco); `d/cs` e' il
> TEMPO-LUCE, grandezza diversa e legittima.»* Quindi **`tau_pp` non e' un tempo proprio**, e il
> nome va corretto.

| da | a | che cos'e' DAVVERO |
|---|---|---|
| `tau_pp` | **`pos_torsione`** | `1 + avv/PHI_CRIT`: una **posizione sull'asse della torsione**, numero puro |
| `tau_soglia` | **`pos_soglia`** | la stessa posizione **alla soglia** |
| `tau_tetto` | **`pos_tetto`** | la stessa posizione **al tetto `4pi`** *(= 3)* |
| `grad_tau` | **`grad_modula`** | **vedi il blocco qui sotto: NON e' `grad_torsione`** |
| `tau_nodo` | **`tors_nodo`** | `1 + |tw|/deg/PHI_CRIT`: torsione per nodo *(ramo a flag SPENTO)* |

> ### ❗ **`grad_tau` NON PUO' DIVENTARE `grad_torsione`, E IL PERCHE' E' NEL RAMO ATTIVO.**
> Luca ha chiesto `grad_tau -> grad_torsione`. **Col flag `TEMPO_UNICO_MITOSI` ACCESO -- cioe' nel
> codice che gira -- `grad_tau` e' `|r_nodo[i] - r_nodo[j]|`: il gradiente di `r`, IL TEMPO PROPRIO
> VERO** *(`:5942`, ramo `if`)*. **Solo a flag SPENTO** e' il gradiente della torsione *(`:5949`,
> ramo `else`)*. **Un nome vale per un ramo e mente sull'altro**, ed e' esattamente il difetto che
> `D32` descrive: **chiamarlo `grad_torsione` lo ripeterebbe col segno opposto.**
> **Scelta:** il nome al punto d'uso dice **il RUOLO** (`grad_modula`: modula la soglia), e **ogni
> ramo DICHIARA il suo contenuto** nel commento. **Se Luca preferisce il suo nome, si cambia con
> una riga di questa tabella.**

**COSA NON SI RINOMINA, di proposito:** i contatori `_rep_taupp_clamp` e `_rep_taupp_tot`.
**Sono REPERTI:** compaiono nei `json` e nei referti gia' scritti, e **i reperti non si riscrivono**
(`CLAUDE.md` par.9). *(E il loro numero, a flag ACCESO, conta un clamp che **non gira**: e' nel ramo
`else`. Va in coda, non qui.)*

**Ogni sostituzione e' asserita per se'** (`P1-quater`), col **conteggio atteso** scritto.

    python csv/_patch_d32_nomi.py --prova
    python csv/_patch_d32_nomi.py

ASCII puro.
"""
import io
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Rinomina variabili in un sorgente.

NL = chr(10)
_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
SIM = "soliton_simulator.py"

# (vecchio, nuovo, quante volte ATTESE) -- l'ordine conta: i nomi lunghi PRIMA dei corti, senno'
#   `tau_pp` mangerebbe un pezzo di `tau_ppXYZ`. Qui non succede, ma l'ordine resta dichiarato.
COPPIE = [
    # i commenti che dicono il FALSO, corretti UNO PER UNO (sono la sostanza di `D32`)
    ("        tau_pp = 1.0 + avv / PHI_CRIT                     # tempo proprio locale (>=1)",
     "        # [D32, 2026-09-27] NON E' UN TEMPO PROPRIO: e' una POSIZIONE sull'asse della" + NL
     + "        #   torsione, un numero puro `1 + avv/PHI_CRIT`. Il tempo proprio del sistema e'" + NL
     + "        #   `r` (e `dt_e` sull'arco); `d/cs` e' il TEMPO-LUCE, un'altra grandezza." + NL
     + "        #   Decisione di Luca, 2026-09-27. Il nome vecchio era `tau_pp`.", 1),
    ("        tau_soglia = 1.0 + soglia / PHI_CRIT              # tempo proprio ALLA soglia (locale)",
     "        pos_soglia = 1.0 + soglia / PHI_CRIT              # la stessa POSIZIONE, alla soglia",
     1),
    ("        tau_tetto = 1.0 + TW_TETTO / PHI_CRIT             # tempo proprio al tetto 4pi (=3)",
     "        pos_tetto = 1.0 + TW_TETTO / PHI_CRIT             # la stessa POSIZIONE, al tetto 4pi",
     1),
    ("        centro = 0.5 * (tau_soglia + tau_tetto)", "        centro = 0.5 * (pos_soglia + pos_tetto)", 1),
    ("        segno = -np.tanh(3.0 * (tau_pp - centro))",
     "        pos_torsione = 1.0 + avv / PHI_CRIT" + NL
     + "        segno = -np.tanh(3.0 * (pos_torsione - centro))", 1),
    ("            tau_locale = 1.0 / tau_pp                      # ritmo (sempre positivo)",
     "            # ⚠ RAMO A FLAG SPENTO: qui `pos_torsione` E' USATA COME TEMPO (il suo" + NL
     + "            #   reciproco come ritmo), ed e' il difetto di `D32`. Proposto per la" + NL
     + "            #   rimozione (`STANDARD 10`), NON tolto senza il si' di Luca." + NL
     + "            tau_locale = 1.0 / pos_torsione                # ritmo (sempre positivo)", 1),
    ('        self._rep_taupp_clamp = getattr(self, "_rep_taupp_clamp", 0) + int(np.sum(np.asarray(tau_pp) < 1e-12))',
     "        # ⚠ IL NOME DEL CONTATORE NON SI RINOMINA: e' un REPERTO, sta nei `json` gia'" + NL
     + "        #   scritti (`CLAUDE.md` par.9). E a flag ACCESO conta un clamp che NON GIRA:" + NL
     + "        #   vive nel ramo `else`. In coda come `D32-CONTATORE`, non qui." + NL
     + '        self._rep_taupp_clamp = getattr(self, "_rep_taupp_clamp", 0) + int(np.sum(np.asarray(pos_torsione) < 1e-12))',
     1),
    ('        self._rep_taupp_tot = getattr(self, "_rep_taupp_tot", 0) + int(np.size(tau_pp))',
     '        self._rep_taupp_tot = getattr(self, "_rep_taupp_tot", 0) + int(np.size(pos_torsione))',
     1),
    ("            self._rep = self._rep + _dte * (rep - self._rep) / np.maximum(tau_pp, 1e-12)",
     "            # ⚠ RAMO A FLAG SPENTO: `pos_torsione` USATA COME COSTANTE DI TEMPO. Difetto di" + NL
     + "            #   `D32`, proposto per la rimozione, NON tolto senza il si' di Luca." + NL
     + "            self._rep = self._rep + _dte * (rep - self._rep) / np.maximum(pos_torsione, 1e-12)",
     1),
    # i tre commenti che chiamano `tau_pp` un tempo
    ("        # tempo `tau_pp` -- il tempo proprio locale GIA' calcolato qui sopra, non un tempo nuovo.",
     "        # tempo d'arco `dt_e` -- NON `pos_torsione`, che non e' un tempo (`D32`).", 1),
    ("        # ASSIOMA A5, livello 1 (rilassamento esponenziale): lecito perche' `tau_pp` e' un tempo",
     "        # ASSIOMA A5, livello 1 (rilassamento esponenziale): lecito perche' `dt_e` e' un tempo", 1),
    ("        # locale dello stesso arco. ZERO PARAMETRI: `tau_pp` e `dt_e` esistono gia'.",
     "        # locale dello stesso arco. ZERO PARAMETRI: `dt_e` esiste gia'.", 1),
    ("        # A8: il clamp 1e-12 su tau_pp e' un ramo silenzioso. CONTATO.",
     "        # A8: il clamp 1e-12 su `pos_torsione` e' un ramo silenzioso. CONTATO.", 1),
    ("        #       e dividere ANCHE per `tau_pp` la conta di nuovo;",
     "        #       e dividere ANCHE per `pos_torsione` la conta di nuovo;", 1),
    ("        #   (2) `tau_pp` NON E' UNA DURATA: e' un numero puro. Una costante di tempo deve",
     "        #   (2) `pos_torsione` NON E' UNA DURATA: e' un numero puro (`D32`). Una costante"
     + " di tempo deve", 1),
    # `grad_tau` -> `grad_modula`, e ogni ramo DICHIARA il suo contenuto
    ("                grad_tau = np.abs(_rn[self.i] - _rn[self.j])",
     "                # `grad_modula` qui e' il gradiente di `r`: IL TEMPO PROPRIO VERO." + NL
     + "                grad_modula = np.abs(_rn[self.i] - _rn[self.j])", 1),
    ("                tau_nodo = np.zeros(self.n)", "                tors_nodo = np.zeros(self.n)", 1),
    ("                np.add.at(tau_nodo, self.i[self.i < self.n], aw[self.i < self.n])",
     "                np.add.at(tors_nodo, self.i[self.i < self.n], aw[self.i < self.n])", 1),
    ("                np.add.at(tau_nodo, self.j[self.j < self.n], aw[self.j < self.n])",
     "                np.add.at(tors_nodo, self.j[self.j < self.n], aw[self.j < self.n])", 1),
    ("                tau_nodo = 1.0 + tau_nodo / np.maximum(self._deg, 1) / PHI_CRIT",
     "                tors_nodo = 1.0 + tors_nodo / np.maximum(self._deg, 1) / PHI_CRIT", 1),
    ("                grad_tau = np.abs(tau_nodo[self.i] - tau_nodo[self.j])   # gradiente lungo l'arco",
     "                # a flag SPENTO `grad_modula` e' il gradiente della TORSIONE: un'altra" + NL
     + "                #   grandezza. **Un nome unico mentirebbe su un ramo dei due** (`D32`)." + NL
     + "                grad_modula = np.abs(tors_nodo[self.i] - tors_nodo[self.j])", 1),
    ("            soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_tau))",
     "            soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_modula))", 1),
    # il commento a valle che dice "gradiente di tempo proprio"
    ("        # massima alla SOGLIA LOCALE (soglia critica emergente, pilotata dal gradiente di",
     "        # massima alla SOGLIA LOCALE (soglia critica emergente, pilotata da `grad_modula`:"
     + " il gradiente di", 1),
    ("        # tempo proprio), e si SPEGNE al tetto della doppia copertura 4pi. Tra i due, la",
     "        # `r` a flag acceso, della torsione a flag spento -- `D32`), e si SPEGNE al tetto"
     + " 4pi. Tra i due, la", 1),
]


if __name__ == "__main__":
    scrivi = "--prova" not in sys.argv[1:]
    p = os.path.join(RADICE, SIM)
    t = io.open(p, encoding="utf-8", newline="").read()
    print("=" * 92)
    print("`D32`: i nomi dicono cio' che la grandezza E'%s"
          % ("" if scrivi else "   (PROVA: non scrivo)"))
    print("=" * 92)
    fatte = 0
    for vecchio, nuovo, attese in COPPIE:
        if nuovo in t and vecchio not in t:
            print("  gia' applicata: %s" % vecchio.strip()[:64])
            continue
        n = t.count(vecchio)
        if n != attese:
            raise SystemExit("ancora attesa %d volte, trovata %d:%s  %s"
                             % (attese, n, NL, vecchio.strip()[:110]))
        t = t.replace(vecchio, nuovo)
        fatte += 1
    resti = t.count("tau_pp")
    print("  sostituzioni asserite .............. %d su %d" % (fatte, len(COPPIE)))
    print("  occorrenze di `tau_pp` RESTANTI .... %d" % resti)
    for r in t.split(NL):
        if "tau_pp" in r:
            print("      %s" % r.strip()[:98])
    print("  occorrenze di `grad_tau` restanti .. %d" % t.count("grad_tau"))
    if scrivi and fatte:
        io.open(p, "w", encoding="utf-8", newline=NL).write(t)
        print("  SCRITTO %s" % SIM)
    sys.exit(0)
