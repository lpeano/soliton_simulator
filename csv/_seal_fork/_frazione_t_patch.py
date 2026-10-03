# -*- coding: utf-8 -*-
"""**LA PATCH DEL `COMMIT 6a`: la frazione `t` esplicita, e serve anche a COSTRUIRE i casi.**

### Una sostituzione alla volta, con l'### **ancora CONTATA** e il fallimento se non e'
unica *(`P1-quater`)*. ### E niente escape nei letterali: dove serve un carattere si usa
`chr()`.

## LE OPZIONI

| | |
|---|---|
| *(nessuna)* | ### **la cura intera**: `FRAZ_NASCITA = 0.5` dichiarato una volta + i ### **sei siti** + `_fab` per meta' sui ### **due** percorsi + le ### **tre regole** che consumavano `dh`/`dd` due volte |
| `--t=N` | ### **`FRAZ_NASCITA = N`** invece di `0.5` — il braccio `C` del sigillo |
| `--letterale=<sito>` | ### **QUEL sito resta al letterale `0.5`** — il braccio `C-bis`. I sei nomi: `pos_div`, `dh`, `fm`, `fm_bias`, `pos_sch`, `dd` |

### ⛔ **E `--letterale` NON e' un comodo: e' il controllo del controllo.** Con `--t=0.4` e
un sito al letterale, il braccio `B` deve ### **nominare la riga** e il braccio `C` deve
### **trovare la grandezza che manca**. ### **Sei copie, sei bocciature: se anche una passa, il
sigillo non discrimina.**

## ⚠ **UNA CONSEGUENZA CHE IL MANDATO NON NOMINA, e va dichiarata**

Se `dh` diventa l'array ### **raddoppiato**, la regola `_rn_div_d` che fa
`concatenate([d[keep], dh, dh])` darebbe ### **`4n` archi.** ### ➜ **Quindi il `6a` tocca
anche TRE REGOLE della tabella** — `_rn_div_d`, `_rn_sch_d`, `_rn_sch_d0` — che devono
consumare `dh`/`dd` ### **una volta sola.** Le loro ### **ancore dichiarate** si aggiornano
insieme al corpo *(sono parte della regola, non un commento)*.

**USO:** `python csv/_seal_fork/_frazione_t_patch.py --file=<copia> [opzioni]`
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
NL = chr(10)

P = None
T = 0.5
LETTERALE = None
# ### `--mitosi-dir=N` ACCENDE il ramo del `bias`, e serve SOLO alle copie del sigillo.
#   ### ⛔ PERCHE' ESISTE: con `MITOSI_DIR = 0.0` (il valore del sorgente, archiviato al
#   commit 0 del riordino) il ramo `fm = (t + bias)*D` ### **NON GIRA MAI**, quindi il braccio
#   `C` non lo raggiunge e la copia `--letterale=fm_bias` sarebbe scoperta ### **dal solo
#   testo** (il braccio `B`). ### ✅ **La lezione del commit 5 e' che il caso che serve
#   SI COSTRUISCE**, e questa opzione lo costruisce. ### ⚠ **Non tocca il sorgente: la
#   usano soltanto le copie di `C` e della `C-bis fm_bias`.**
MITOSI_DIR = None
SITI = ("pos_div", "dh", "fm", "fm_bias", "pos_sch", "dd")
for _a in sys.argv[1:]:
    if _a.startswith("--file="):
        P = _a.split("=", 1)[1]
    elif _a.startswith("--t="):
        T = float(_a.split("=", 1)[1])
    elif _a.startswith("--mitosi-dir="):
        MITOSI_DIR = float(_a.split("=", 1)[1])
    elif _a.startswith("--letterale="):
        LETTERALE = _a.split("=", 1)[1]
        if LETTERALE not in SITI:
            raise SystemExit("** sito sconosciuto: %s. I sei: %s **"
                             % (LETTERALE, ", ".join(SITI)))
    else:
        raise SystemExit("** opzione sconosciuta: %s **" % _a)
if not P or not os.path.isfile(P):
    raise SystemExit("** serve `--file=<copia del simulatore>` **")

t = io.open(P, encoding="utf-8").read()
fatte = []


def sost(ancora, nuovo, etichetta):
    global t
    n = t.count(ancora)
    if n != 1:
        raise SystemExit("** %s: ancora trovata %d volte, non 1 **" % (etichetta, n))
    t = t.replace(ancora, nuovo)
    fatte.append(etichetta)


def frazione(sito):
    """La frazione da scrivere in QUEL sito: `FRAZ_NASCITA` oppure il letterale `0.5`."""
    return "0.5" if LETTERALE == sito else "FRAZ_NASCITA"


def uno_meno(sito):
    return "0.5" if LETTERALE == sito else "(1.0 - FRAZ_NASCITA)"


# ============================================= 1. LA COSTANTE, DICHIARATA UNA VOLTA
sost('''TAU_TW   = 20.0''',
     '''# ### LA FRAZIONE DELLA NASCITA, DICHIARATA UNA VOLTA SOLA (`COMMIT 6a`, decisione di
#   Luca del 2026-10-03). ### IL NOME E' `FRAZ_NASCITA` E NON `T_NASCITA`, per decisione
#   di Luca: e' una ### **FRAZIONE dell'arco**, un numero puro in `[0,1]` misurato dal
#   genitore `a`/`aa` -- e nel simulatore ### **`t` e `dt` sono TEMPI** (`dt_e`, il tempo
#   proprio dell'arco). ### Chiamarla `t` avrebbe messo una lunghezza adimensionale nello
#   stesso alfabeto dei tempi.
#   Luca del 2026-10-03). ### Il figlio sta a `FRAZ_NASCITA * d` dal genitore `a` e a
#   `(1 - FRAZ_NASCITA) * d` da `b`, ### **e lo STESSO valore vale per DOVE nasce (`pos`), per
#   QUANTO sono lunghi i suoi archi (`d`, `d0`, `dd`) e per la sua FASE (`fm`).**
#   ### ⛔ **NON E' UN FLAG, ed e' una scelta:** un flag renderebbe la frazione
#   ### **un'opzione**, e dove nasce un figlio non e' un'opzione -- e' la legge. E' il
#   difetto `E4-LAM`, gia' pagato una volta.
#   ### \U0001f4cc **PRIMA ERANO SEI FORMULE INDIPENDENTI che per caso dicevano tutte
#   *<<meta'>>***, in tre funzioni diverse: `mitosi` (la preparazione e il ramo Schwinger)
#   e la regola `_rn_sch_pos`. Con `0.5` ### **non cambia un bit**; cambia ### **dove
#   vive**, e da li' una decisione di fisica potra' cambiarla ### **in un posto solo.**
#   ### ⚠ **E le EREDITA' DI STATO NON la leggono** (decisione di Luca): `psi` e
#   `phivel` restano ### **medie**, la famiglia dello spinore resta una ### **copia**, e
#   `rho_sel` del cancello resta com'e'. Si decidono nella ### **LEGGE** di
#   `DIVISIONE-AUTOCONSISTENTE`, che viene ### **dopo la definizione dell'energia** perche'
#   deve rispettare `A14`.
FRAZ_NASCITA = %r

TAU_TW   = 20.0''' % T,
     "la costante `FRAZ_NASCITA = %r`, dichiarata una volta" % T)

# ============================================= 2. `_nasce`: `_fab` PER META'
sost('''    def _nasce(self, v, dove="?", md=1, md0=1):''',
     '''    def _nasce(self, v, dove="?", md=1, md0=1, meta=None):''',
     "`_nasce`: il parametro `meta`")

sost('''        _fab = float(np.sum(LAM - _v[_sotto])) if _ntr else 0.0''',
     '''        if meta is None:
            _fab = float(np.sum(LAM - _v[_sotto])) if _ntr else 0.0
        else:
            # ### `_fab` PER META', e non e' un'eleganza: `np.sum` su `2n` elementi
            #   ### **NON e' identica al bit** a `2 * np.sum` su `n` -- MISURATO, 4043
            #   differenze su 14000 *(`csv/_test_fork/_somma_meta/`)*. La somma calcolata
            #   ### **per meta' e poi sommata** a `t = 0.5` e' `s + s`, e ### **`s + s ==
            #   2*s` e' ESATTO** perche' il raddoppio e' uno scalamento per una potenza di
            #   due. ### ➜ **Cosi' il contatore `_sm_lun` resta identico al bit quando
            #   una chiamata con `md = 2` su `n` voci diventa una con `md = 1` su `2n`.**
            #   ### ⚠ `meta` e' il numero di voci della PRIMA meta'.
            _a = _v[:meta]
            _b = _v[meta:]
            _sa = _a < LAM
            _sb = _b < LAM
            _fab = ((float(np.sum(LAM - _a[_sa])) if _sa.any() else 0.0)
                    + (float(np.sum(LAM - _b[_sb])) if _sb.any() else 0.0))''',
     "`_nasce`: `_fab` per META' quando `meta` e' dato")

# ============================================= 3. I SEI SITI
# --- (a) il bias e i due rami di `fm`, piu' `pos_figlio`
sost('''            bias = 0.5 * np.tanh(MITOSI_DIR * (twn[a] - twn[b]))
            fm = (self.phi[a] - (0.5 + bias) * D) % self._dphi()
        else:
            fm = (self.phi[a] - 0.5 * D) % self._dphi()
        pos_figlio = 0.5 * (self.pos[a] + self.pos[b])''',
     '''            bias = 0.5 * np.tanh(MITOSI_DIR * (twn[a] - twn[b]))
            # ### IL `bias` E' UNO SCOSTAMENTO *SOPRA* `FRAZ_NASCITA`, e il suo `0.5` di
            #   AMPIEZZA (la riga qui sopra) ### **NON si tocca**: sono due `0.5` con
            #   ### **due ruoli diversi** sulla stessa legge, e distinguerli e' il punto.
            fm = (self.phi[a] - (%s + bias) * D) %% self._dphi()
        else:
            fm = (self.phi[a] - %s * D) %% self._dphi()
        # ### LA FORMA CONVESSA, E NON LA LERP: `(1-t)*x + t*y` e' ### **identica al bit** a
        #   `0.5*(x+y)` a `t = 0.5` *(0 differenze su 2 000 000)*, mentre `x + t*(y-x)`
        #   ### **NO** *(576 135 su 2 000 000)*. ### Misurato prima di scrivere.
        pos_figlio = %s * self.pos[a] + %s * self.pos[b]'''
     % (frazione("fm_bias"), frazione("fm"), uno_meno("pos_div"), frazione("pos_div")),
     "i tre siti della preparazione: `fm` nei due rami e `pos_figlio`")

# --- (b) `dh` si sdoppia, e `d0h` con lui
sost('''        dh = self.d[sel] / 2''',
     '''        # ### `dh` SI SDOPPIA, e l'ordine e' quello di `i = [keep, a, m]`: ### **il
        #   PRIMO blocco e' `a`-`m` e vale `t * d`**, il secondo e' `m`-`b` e vale
        #   `(1-t) * d`. ### A `t = 0.5` i due blocchi sono IDENTICI, ed e' per questo che
        #   oggi una sola `dh` bastava per entrambi.
        dh_a = %s * self.d[sel]
        dh_b = %s * self.d[sel]''' % (frazione("dh"), uno_meno("dh")),
     "`dh` si sdoppia nei due blocchi")

sost('''            d0h = dh * (1.0 + fattore_plastico)
            d0new = np.concatenate([d0h, d0h])
        elif PLAST_MIT > 0.0:
            d0h = dh * (1.0 + PLAST_MIT * sciolta)   # sciolta = |tw|/PHI_CRIT >= 1
            d0new = np.concatenate([d0h, d0h])
        else:
            d0new = np.concatenate([dh, dh])''',
     '''            # ### `d0new` DERIVA DAI DUE MEZZI, con lo STESSO ordine, e resta calcolato
            #   dai valori ### **PRIMA** della chiamata a `_nasce` su `dh` -- come oggi.
            d0new = np.concatenate([dh_a * (1.0 + fattore_plastico),
                                    dh_b * (1.0 + fattore_plastico)])
        elif PLAST_MIT > 0.0:
            d0new = np.concatenate([dh_a * (1.0 + PLAST_MIT * sciolta),
                                    dh_b * (1.0 + PLAST_MIT * sciolta)])
        else:
            d0new = np.concatenate([dh_a, dh_b])''',
     "`d0new` dai DUE mezzi, nello stesso ordine")

sost('''        # `md=2, md0=0`: `dh` finisce in `concatenate([d[keep], dh, dh])`, quindi ogni voce
        #   diventa DUE archi di `d`; su `d0` non entra (ci pensa `d0new`, gia' raddoppiato).
        dh = self._nasce(dh, 'mitosi', 2, 0)   # [SCALA_MIN] i tronconi d/2 della mitosi''',
     '''        # ### `md=1, md0=0` E NON `2, 0`: `dh` e' ora GIA' l'array dei due blocchi, quindi
        #   ogni voce e' ### **un arco vero** e non due. ### ⛔ **E la chiamata resta UNA,
        #   di proposito:** `_g_sm_nascite` conta le INVOCAZIONI, e spezzarla in due lo
        #   farebbe salire di 2 invece di 1. ### `meta` dice dove finisce il primo blocco,
        #   cosi' `_fab` si calcola PER META' e `_sm_lun` resta identico al bit.
        dh = np.concatenate([dh_a, dh_b])
        dh = self._nasce(dh, 'mitosi', 1, 0, meta=len(dh_a))   # [SCALA_MIN] i due tronconi''',
     "la chiamata di `dh`: `md = 1` sull'array raddoppiato, con `meta`")

# --- (c) `dd` dello Schwinger si sdoppia
sost('''                dd = self._nasce(np.maximum(
                    0.5 * np.linalg.norm(self.pos[aa] - self.pos[bb], axis=1), 0.05),
                    'schwinger', 2, 2)''',
     '''                # ### `dd` SI SDOPPIA, e l'ordine e' quello di `i = [.., aa, k]`: il
                #   PRIMO blocco e' `aa`-`k` e vale `max(t*L, 0.05)`, il secondo e' `k`-`bb`
                #   e vale `max((1-t)*L, 0.05)`. ### ⚠ **Il pavimento `0.05` resta
                #   com'e': e' un `A11` e NON e' del `6a`.**
                #   ### ⚠ **E LA LUNGHEZZA VIENE DA `pos`, NON DA `d`** -- nella
                #   divisione viene da `d`. ### **E' `SCHW-CORTI`, e il `6a` la DICHIARA
                #   senza cambiarla.**
                _L_sch = np.linalg.norm(self.pos[aa] - self.pos[bb], axis=1)
                _dd_a = np.maximum(%s * _L_sch, 0.05)
                _dd_b = np.maximum(%s * _L_sch, 0.05)
                dd = self._nasce(np.concatenate([_dd_a, _dd_b]),
                                 'schwinger', 1, 1, meta=len(_dd_a))'''
     % (frazione("dd"), uno_meno("dd")),
     "`dd` si sdoppia, con `meta` e il pavimento intatto")

# --- (d) `pos` dello Schwinger
sost('''                 "self.pos = np.vstack([self.pos, 0.5 * (self.pos[aa] + self.pos[bb])])",''',
     '''                 "self.pos = np.vstack([self.pos, (1-FRAZ_NASCITA) * self.pos[aa] + "
                 "FRAZ_NASCITA * self.pos[bb]])",''',
     "l'ancora dichiarata di `_rn_sch_pos`")

sost('''def _rn_sch_pos(net, c):
    net.pos = np.vstack([net.pos, 0.5 * (net.pos[c["aa"]] + net.pos[c["bb"]])])''',
     '''def _rn_sch_pos(net, c):
    # ### LA FORMA CONVESSA, come nella divisione.
    net.pos = np.vstack([net.pos,
                         %s * net.pos[c["aa"]] + %s * net.pos[c["bb"]]])'''
     % (uno_meno("pos_sch"), frazione("pos_sch")),
     "`_rn_sch_pos`: la forma convessa")

# ============================================= 4. LE TRE REGOLE che consumavano due volte
sost('''                 "self.d = np.concatenate([self.d[keep], dh, dh])",''',
     '''                 "self.d = np.concatenate([self.d[keep], dh])  # `dh` e' GIA' i due "
                 "blocchi",''',
     "l'ancora di `_rn_div_d`")

sost('''def _rn_div_d(net, c):
    net.d = np.concatenate([net.d[c["keep"]], c["dh"], c["dh"]])''',
     '''def _rn_div_d(net, c):
    # ### UNA VOLTA SOLA: `dh` e' GIA' l'array dei due blocchi (`a`-`m` e `m`-`b`). Con
    #   `dh, dh` darebbe ### **4n archi**.
    net.d = np.concatenate([net.d[c["keep"]], c["dh"]])''',
     "`_rn_div_d`: `dh` una volta sola")

sost('''                 "self.d = np.concatenate([self.d, dd, dd])",''',
     '''                 "self.d = np.concatenate([self.d, dd])  # `dd` e' GIA' i due blocchi",''',
     "l'ancora di `_rn_sch_d`")

sost('''def _rn_sch_d(net, c):
    net.d = np.concatenate([net.d, c["dd"], c["dd"]])''',
     '''def _rn_sch_d(net, c):
    # ### UNA VOLTA SOLA: `dd` e' GIA' i due blocchi (`aa`-`k` e `k`-`bb`).
    net.d = np.concatenate([net.d, c["dd"]])''',
     "`_rn_sch_d`: `dd` una volta sola")

sost('''                 "self.d0 = np.concatenate([self.d0, dd, dd])",''',
     '''                 "self.d0 = np.concatenate([self.d0, dd])  # `dd` e' GIA' i due blocchi",''',
     "l'ancora di `_rn_sch_d0`")

sost('''def _rn_sch_d0(net, c):
    net.d0 = np.concatenate([net.d0, c["dd"], c["dd"]])''',
     '''def _rn_sch_d0(net, c):
    # ### UNA VOLTA SOLA, come `_rn_sch_d`.
    net.d0 = np.concatenate([net.d0, c["dd"]])''',
     "`_rn_sch_d0`: `dd` una volta sola")

# ===================== 5. LA QUARTA CONSUMATRICE DI `dd`, e l'ha trovata IL PRESIDIO
# ### \u26d4 IL BUG DEL PRIMO GIRO, e non era fra le tre REGOLE: la CHIAMATA CON EFFETTO
#   del ramo Schwinger faceva `_smp_chirurgia(nuovi=np.concatenate([dd, dd]))` -- e con
#   `dd` ### **gia' raddoppiato** dava ### **4n invece di 2n**, facendo crescere lo
#   snapshot `_smp_d0` del DOPPIO. ### Il presidio `RIPIEGHI-ZERO` del simulatore si e'
#   fermato al PRIMO passo con uno Schwinger *(reperto
#   `_sigillo_frazione_t/_corsa_2026-10-03_BUG_SMP_CHIRURGIA.txt`)*.
# ### \U0001f4cc E IL MIO COLLAUDO NON POTEVA VEDERLA: 45 passi, scelti perche' la prima
#   MITOSI e' al 42 -- ma il primo SCHWINGER e' al 70. ### Un collaudo tarato sul primo
#   evento di UN tipo non dice niente sull'altro.
sost('''                self._smp_chirurgia(nuovi=np.concatenate([dd, dd]))   # [C3] Schwinger''',
     '''                # ### UNA VOLTA SOLA: `dd` e' GIA' i due blocchi. Con
                #   `concatenate([dd, dd])` lo snapshot crescerebbe del DOPPIO, e il
                #   presidio `RIPIEGHI-ZERO` ferma il run -- lo ha fatto davvero.
                self._smp_chirurgia(nuovi=dd)   # [C3] Schwinger''',
     "la QUARTA consumatrice: `_smp_chirurgia` del ramo Schwinger")

sost('''                       "self._smp_chirurgia(nuovi=np.concatenate([dd, dd]))",''',
     '''                       "self._smp_chirurgia(nuovi=dd)  # `dd` e\' GIA\' i due blocchi",''',
     "l'ancora dichiarata di quella chiamata con effetto")

# ===================== 6. I COMMENTI SCADUTI DALLA PATCH STESSA
sost('''                 "`dh = d[sel]/2`, passato per `_nasce('mitosi', 2, 0)` nella preparazione: "''',
     '''                 "`dh` e\' ora i DUE BLOCCHI (`t*d[sel]` per `a`-`m` e `(1-t)*d[sel]` per "
                 "`m`-`b`), passati per `_nasce(\'mitosi\', 1, 0, meta=len(dh_a))`: `md = 1` "
                 "e non 2 perche\' ogni voce e\' ora UN arco vero, e `meta` fa calcolare "
                 "`_fab` PER META\' cosi\' `_sm_lun` resta identico al bit. Nella preparazione: "''',
     "la derivazione di `_rn_div_d`: i due blocchi, `md = 1`, `meta`")

sost('''                 "altrimenti e' `dh` nudo. `d0new` e' GIA' `[d0h, d0h]`, cioe' i due "''',
     '''                 "altrimenti e\' `dh` nudo. `d0new` e\' GIA\' i DUE BLOCCHI (dai due mezzi "
                 "`dh_a` e `dh_b`, nello stesso ordine), cioe\' i due "''',
     "la derivazione di `_rn_div_d0`: `d0h` non esiste piu', sono i due mezzi")

sost('''                 "`dd = max(0.5 * norm(pos[aa] - pos[bb]), 0.05)`, per `_nasce('schwinger', "''',
     '''                 "`dd` e\' ora i DUE BLOCCHI: `max(t*L, 0.05)` per `aa`-`k` e "
                 "`max((1-t)*L, 0.05)` per `k`-`bb`, con `L = norm(pos[aa]-pos[bb])`, per "
                 "`_nasce(\'schwinger\', "''',
     "la derivazione di `_rn_sch_d`: i due blocchi")

sost('''                # `md=2, md0=2`: `concatenate([d, dd, dd])` E `concatenate([d0, dd, dd])`.''',
     '''                # ### `md=1, md0=1` E NON `2, 2`: `dd` e' ora GIA' i due blocchi, quindi
                #   `concatenate([d, dd])` E `concatenate([d0, dd])` -- e `meta` fa
                #   calcolare `_fab` PER META'.''',
     "il commento dei moltiplicatori dello Schwinger")

# ===================== 7. `--mitosi-dir`: ACCENDE il ramo del bias (solo nelle copie)
if MITOSI_DIR is not None:
    sost("MITOSI_DIR = 0.0        #",
         "MITOSI_DIR = %r        #" % MITOSI_DIR,
         "caso costruito: `MITOSI_DIR = %r`, cosi' il ramo del bias GIRA" % MITOSI_DIR)

io.open(P, "w", encoding="utf-8", newline=NL).write(t)
print("=" * 92)
for f in fatte:
    print("  OK  " + f)
print("  ### FRAZ_NASCITA = %r" % T)
if LETTERALE:
    print("  ### E IL SITO `%s` RESTA AL LETTERALE 0.5: e' il braccio C-bis, e DEVE essere"
          % LETTERALE)
    print("  ###   scoperto da B (con la riga) e da C (con la grandezza che manca).")
