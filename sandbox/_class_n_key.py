

_NKEY_ALLOWED_CHARACTERS = 'abcdefghijklmnopqrstuvwxyz012345679'


class NKey(str):
    def __new__(cls, source: str, *args, **kwargs):
        source = str(source)
        return ''.join(c for c in source if c in _NKEY_ALLOWED_CHARACTERS)

