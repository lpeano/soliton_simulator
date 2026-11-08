# -*- coding: utf-8 -*-
r"""**IL REGISTRO DELLO STATO COMPLETO** *(I1, Luca `2026-11-07` `16:01` e `2026-11-08` `03:47`, la strada (i2); il task history `doc/TASK_HISTORY/2026-11-07_stato_completo.md`)*.

### **«Completo» = tutto cio' che serve a ripartire AL BIT**, anche cio' che NON sta in `z["st"]` *(gli accumulatori del bordo, `acc`, il campo `U(1)`)*:
**chi ha stato lo REGISTRA** *(`registra(nome, prendi, metti)`)*, **e il file contiene ESATTAMENTE i registrati.** ### **`carica` ALZA** se i registrati del file e quelli del
registro non coincidono *(una grandezza registrata e non salvata, o salvata e non registrata)*, se uno `sha1` non torna, se una tabella costante e' cambiata.

**Il formato** *(R4)*: un `.npz` con le chiavi `<nome>/<chiave>` e `meta` *(un json: la corsa, il tick, `t`, il commit, i registrati, lo `sha1` di ogni chiave e delle tabelle)*,
scritto in un file temporaneo e poi `os.replace`. ### **Il nucleo non si tocca; `corsa_accensione.py` non lo usa ancora** *(il flag a fine allungamenti, Luca `03:47`)*.
"""
import hashlib
import json
import os

import numpy as np

SEP = "/"


def sha1(a):
    """### Lo `sha1` dei byte dell'array *(contiguo)*, col tipo e la forma: due array con gli stessi byte ma forma diversa NON sono uguali."""
    a = np.ascontiguousarray(a)
    h = hashlib.sha1(("%s|%s|" % (a.dtype.str, a.shape)).encode("ascii"))
    h.update(a.tobytes())
    return h.hexdigest()


class Registro:
    """### **Chi ha stato lo registra; il file contiene ESATTAMENTE i registrati.**"""

    def __init__(self):
        self.voci = {}
        self.tabelle = {}

    def registra(self, nome, prendi, metti):
        """`prendi() -> {chiave: array}`; `metti({chiave: array})` rimette lo stato *(in posto)*. ### Un nome registrato due volte ALZA."""
        assert SEP not in nome and nome not in self.voci and nome != "meta", "il nome %r e' gia' registrato, o non e' un nome valido" % (nome,)
        self.voci[nome] = (prendi, metti)

    def tabella(self, nome, array):
        """### **Una COSTANTE** *(per esempio la tabella di `c(t)`)*: **non si salva, se ne registra lo `sha1`**, e `carica` ALZA se e' cambiata."""
        assert nome not in self.tabelle, "la tabella %r e' gia' registrata" % (nome,)
        self.tabelle[nome] = sha1(array)

    def prendi(self):
        """`{nome/chiave: array}` di tutti i registrati *(copie)*."""
        out = {}
        for nome, (prendi, _m) in sorted(self.voci.items()):
            for k, v in sorted(prendi().items()):
                assert SEP not in k, "la chiave %r di %r contiene %r" % (k, nome, SEP)
                out[nome + SEP + k] = np.array(v, copy=True)
        return out

    def impronta(self):
        """`{nome/chiave: sha1}` dello stato di adesso."""
        return {k: sha1(v) for k, v in self.prendi().items()}

    def salva(self, f, meta):
        """### Scrive `f` *(un `.npz`)*: le chiavi dei registrati e `meta` *(json)*. Ritorna l'impronta."""
        dati = self.prendi()
        imp = {k: sha1(v) for k, v in dati.items()}
        m = dict(meta)
        m.update({"registrati": sorted(self.voci), "sha1": imp, "tabelle": dict(self.tabelle)})
        tmp = f + ".tmp.npz"
        np.savez(tmp, meta=np.array(json.dumps(m, sort_keys=True)), **dati)
        os.replace(tmp, f)
        return imp

    def carica(self, f):
        """### Rimette lo stato dei registrati dal file `f`. ### **ALZA** se i registrati non coincidono, se uno `sha1` non torna, se una tabella e' cambiata. Ritorna `meta`."""
        with np.load(f) as d:
            meta = json.loads(str(d["meta"]))
            assert sorted(meta["registrati"]) == sorted(self.voci), (
                "i registrati del file %s NON sono quelli del registro: nel file %s, nel registro %s -- una grandezza non registrata (o non salvata) non passa in silenzio"
                % (f, sorted(meta["registrati"]), sorted(self.voci)))
            assert meta["tabelle"] == self.tabelle, "una tabella COSTANTE e' cambiata: nel file %s, oggi %s" % (meta["tabelle"], self.tabelle)
            dati = {k: d[k].copy() for k in d.files if k != "meta"}
        for k, v in dati.items():
            assert sha1(v) == meta["sha1"][k], "lo sha1 di %s nel file NON e' quello registrato" % k
        assert sorted(dati) == sorted(meta["sha1"]), "le chiavi del file non sono quelle del suo meta"
        for nome, (_p, metti) in self.voci.items():
            pre = nome + SEP
            metti({k[len(pre):]: v for k, v in dati.items() if k.startswith(pre)})
        return meta


def di_z(z, salvo=()):
    """### `(prendi, metti)` per `z["st"]`: **ogni chiave array**, tranne quelle in `salvo` *(serve SOLO al DEVE FALLIRE R2-F: un registro che dimentica una chiave)*."""
    st = z["st"]
    chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray) and k not in salvo)

    def prendi():
        return {k: st[k] for k in chiavi}

    def metti(d):
        assert sorted(d) == chiavi, "le chiavi di z[st] nel file %s non sono quelle di oggi %s" % (sorted(d), chiavi)
        for k in chiavi:
            st[k][...] = d[k]
    return prendi, metti


def di_dict(dd, chiavi):
    """### `(prendi, metti)` per un dizionario di grandezze **scalari o liste** *(gli accumulatori del bordo)*: `float` -> array di dimensione `0`, rimessi col LORO tipo."""
    tipi = {k: type(dd[k]) for k in chiavi}

    def prendi():
        return {k: np.asarray(dd[k], dtype=float) for k in chiavi}

    def metti(d):
        assert sorted(d) == sorted(chiavi), "le chiavi nel file %s non sono %s" % (sorted(d), sorted(chiavi))
        for k in chiavi:
            v = d[k]
            dd[k] = float(v) if tipi[k] is float else v.tolist()
    return prendi, metti
