class Automatic:
    def __init__(self, q, e, b, s, f):
        self.q = q
        self.e = e
        self.b = b
        self.s = s
        self.f = f
        self.current_state = s

    def change_state(self, signal):
        if signal not in self.e:
            return False

        result = [self.b[state, signal] for state in self.current_state]
        self.current_state = [elem[0] for elem in result]
        return result

    def max_string(self, string, l):
        i, m, flag = l, 0, False

