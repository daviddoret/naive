_toto = None


def test():
    global _toto
    if _toto is None:
        _toto = "hello world"


test()
print(_toto)
