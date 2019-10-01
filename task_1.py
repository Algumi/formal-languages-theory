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
        self.current_state = self.s
        for i, char in enumerate(string):
            self.change_state(char)
            if self.current_state in self.f:
                return flag, i - l + 1


def test():
    q = ["empty", "sign", "int", "fract", "e_int", "e_int_num", "e_int_sign", "e_fract",
         "e_fract_num", "e_fract_sign", "dot"]

    e = ["inp_num", "inp_sign", "inp_e", "inp_dot"]
    b = {("empty", "inp_sign"): "sign", ("empty", "inp_num"): "int", ("empty", "inp_dot"): "dot",
         ("sign", "inp_num"): "int", ("sign", "inp_dot"): "dot",
         ("int", "inp_dot"): "dot", ("int", "inp_num"): "int", ("int", "inp_e"): "e_int",
         ("dot", "inp_num"): "fract", ("dot", "inp_e"): "e_fract",
         ("fract", "inp_num"): "fract", ("fract", "inp_e"): "e_fract",
         ("e_int", "inp_num"): "e_int_num", ("e_int", "inp_sign"): "e_int_sign",
         ("e_int_sign", "inp_num"): "e_int_num",
         ("e_int_num", "inp_num"): "e_int_num", ("e_int_num", "inp_dot"): "dot",
         ("e_fract", "inp_num"): "e_fract_num", ("e_fract", "inp_sign"): "e_fract_sign",
         ("e_fract_sign", "inp_num"): "e_fract_num",
         ("e_fract_num", "inp_num"): "e_fract_num"}
    s = ["empty"]
    f = ["int", "dot", "fract", "e_int_num", "e_fract_num"]
    auto = Automatic(q, e, b, s, f)
    


