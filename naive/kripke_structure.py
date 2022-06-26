import typing
import type_library as tl


class KripkeStructure:
    def __init__(self, s, i, tm, ap, lm):
        # Initialize properties from inside __init__
        self._s = None
        self._i = None
        self._tm = None
        self._ap = None
        self._lm = None
        # Call properties to assure consistency
        self.s = s
        self.i = i
        self.tm = tm
        self.ap = ap
        self.lm = lm

    @property
    def s(self):
        """The state set"""
        return self._s

    @s.setter
    def s(self, x):
        x = tl.coerce_set(x)
        self._s = x

    @property
    def i(self):
        """The initial set that is a subset of the state set"""
        return self._i

    @i.setter
    def i(self, x):
        x = tl.coerce_subset(x, self.s)
        self._i = x

    @property
    def tm(self):
        """The transition square matrix"""
        return self._tm

    @tm.setter
    def tm(self, x):
        x = tl.coerce_binary_square_matrix(x)
        self._tm = x

    @property
    def ap(self):
        """The atomic property set"""
        return self._ap

    @ap.setter
    def ap(self, x):
        x = tl.coerce_set(x)
        self._ap = x

    @property
    def lm(self):
        """The labeling function mapping matrix"""
        return self._lm

    @lm.setter
    def lm(self, x):
        x = tl.coerce_binary_matrix(x)
        self._lm = x


KripkeStructureInput = typing.TypeVar(
    'KripkeStructureInput',
    KripkeStructure,
    dict)


def coerce_kripke_structure(m: KripkeStructureInput) -> KripkeStructure:
    if isinstance(m, KripkeStructure):
        return m
    elif isinstance(m, dict):
        s = m.get('s', None)
        i = m.get('i', None)
        tm = m.get('tm', None)
        ap = m.get('ap', None)
        lm = m.get('lm', None)
        coerced_m = KripkeStructure(s, i, tm, ap, lm)
        logging.debug(f'Coerce {m}[{type(m)}] to Kripke structure {coerced_m}')
        return coerced_m
    else:
        raise ValueError