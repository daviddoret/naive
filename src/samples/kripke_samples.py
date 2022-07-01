import src.naive.binary_algebra as ba
import src.naive.kripke_structure as ks


def get_sample_1():
    s = ba.get_state_set(5)
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
