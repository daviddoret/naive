import naive.kripke_structure as ks


def get_sample_1():
    s = ks.get_state_set(5)
    i = [s[0], s[3], s[4]]
    tm = [
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1]]
    ap = ['red', 'green', 'blue']
    lm = [
        [1, 1, 0, 0, 1],
        [0, 1, 1, 0, 1],
        [0, 0, 1, 1, 1]]
    m = ks.KripkeStructure(s, i, tm, ap, lm)
    return m
