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

        # check if there is transition for current state and input signal
        states_signals = [(state, signal) for state in self.current_state]
        if not (set(states_signals) & set(self.b.keys())):
            return False

        result = [self.b[key] for key in states_signals if key in self.b.keys()]
        self.current_state = result
        return result

    def max_string(self, string, l):
        self.current_state = self.s
        m, flag = 0, False

        for i, char in enumerate(string[l:]):
            char = transform_input(char)

            # check if automation didn't broke
            if not self.change_state(char):
                break

            # check if one of the current states can be final state
            if set(self.current_state) & set(self.f):
                flag = True
                m = i + 1

        return flag, m


def transform_input(c):
    if c in "0123456789":
        return "inp_num"
    if c in "-+":
        return "inp_sign"
    if c in "eеEЕ":
        return "inp_e"
    if c in ".":
        return "inp_dot"
    return None


def create_auto_for_float_numbers():
    q = ["empty", "sign", "int", "fract", "e_int", "e_int_num", "e_int_sign", "e_fract",
         "e_fract_num", "e_fract_sign", "dot", "first_dot"]
    e = ["inp_num", "inp_sign", "inp_e", "inp_dot"]
    b = {("empty", "inp_sign"): "sign", ("empty", "inp_num"): "int", ("empty", "inp_dot"): "first_dot",
         ("sign", "inp_num"): "int", ("sign", "inp_dot"): "first_dot",
         ("int", "inp_dot"): "dot", ("int", "inp_num"): "int", ("int", "inp_e"): "e_int",
         ("dot", "inp_num"): "fract", ("dot", "inp_e"): "e_fract",
         ("first_dot", "inp_num"): "fract", ("first_dot", "inp_e"): "e_fract",
         ("fract", "inp_num"): "fract", ("fract", "inp_e"): "e_fract",
         ("e_int", "inp_num"): "e_int_num", ("e_int", "inp_sign"): "e_int_sign",
         ("e_int_sign", "inp_num"): "e_int_num",
         ("e_int_num", "inp_num"): "e_int_num", ("e_int_num", "inp_dot"): "dot",
         ("e_fract", "inp_num"): "e_fract_num", ("e_fract", "inp_sign"): "e_fract_sign",
         ("e_fract_sign", "inp_num"): "e_fract_num",
         ("e_fract_num", "inp_num"): "e_fract_num"}
    s = ["empty"]
    f = ["int", "dot", "fract", "e_int_num", "e_fract_num"]

    return Automatic(q, e, b, s, f)


def test_auto_float_numbers(test_strings=None):
    auto = create_auto_for_float_numbers()
    if not test_strings:
        test_strings = ["0.23e5 test", "e5.23 test", ".", "34."]
    for test_str in test_strings:
        print(auto.max_string(test_str, 0))


test_auto_float_numbers()
