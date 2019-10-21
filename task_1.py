class Automatic:
    def __init__(self, **kwargs):
        if "filename" in kwargs.keys():
            q, e, b, s, f = self.read_from_file(kwargs["filename"])
        else:
            q, e, b, s, f = kwargs["q"], kwargs["e"], kwargs["b"], kwargs["s"], kwargs["f"]
        self.q = q
        self.e = e
        self.b = b
        self.s = set(s)
        self.f = set(f)
        self.current_state = set(s)

    @staticmethod
    def read_from_file(filename):
        inp_file = open(filename, encoding="utf-8").read().replace("\n", "").split("-----")
        q = inp_file[0].split()
        e = inp_file[1].split()
        s = inp_file[3].split()
        f = inp_file[4].split()

        b = dict()
        for line in inp_file[2].split(";"):
            if len(line):
                cur_st, pairs = line.split(": ")
                for pair in pairs.split(", "):
                    signal, new_state = pair.split()
                    b[cur_st, signal] = new_state

        return q, e, b, s, f

    def change_state(self, signal):
        if signal not in self.e:
            return False

        # check if there is transition for current state and input signal
        states_signals = [(state, signal) for state in self.current_state]
        if not (set(states_signals) & set(self.b.keys())):
            return False

        result = set([self.b[key] for key in states_signals if key in self.b.keys()])
        self.current_state = result
        return result

    def max_string(self, string, l):
        self.current_state = self.s
        m, flag = 0, False
        if self.current_state & self.f:
            flag = True

        for i, char in enumerate(string[l:]):
            char = transform_input(char)

            # check if automation didn't broke
            if not self.change_state(char):
                break

            # check if one of the current states can be final state
            if self.current_state & self.f:
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
    q = ["empty", "sign", "int", "fract", "e", "e_num", "e_sign", "dot", "first_dot"]
    e = ["inp_num", "inp_sign", "inp_e", "inp_dot"]
    b = {("empty", "inp_sign"): "sign", ("empty", "inp_num"): "int", ("empty", "inp_dot"): "first_dot",
         ("sign", "inp_num"): "int", ("sign", "inp_dot"): "first_dot",
         ("int", "inp_dot"): "dot", ("int", "inp_num"): "int", ("int", "inp_e"): "e",
         ("dot", "inp_num"): "fract", ("dot", "inp_e"): "e",
         ("first_dot", "inp_num"): "fract",
         ("fract", "inp_num"): "fract", ("fract", "inp_e"): "e",
         ("e", "inp_num"): "e_num", ("e", "inp_sign"): "e_sign",
         ("e_sign", "inp_num"): "e_num",
         ("e_num", "inp_num"): "e_num"}
    s = ["empty"]
    f = ["int", "dot", "fract", "e_num"]

    return Automatic(q=q, e=e, b=b, s=s, f=f)


def create_auto_from_file(filename):
    return Automatic(filename=filename)


def search_float_numbers_in_text(filename):
    f_input = open(filename, encoding="utf-8").read()
    f_output_name = filename[:-4] + "_output.txt"
    f_output = open(f_output_name, "w+", encoding="utf-8")
    # auto = create_auto_for_float_numbers()
    auto = create_auto_from_file("test_data/task_1/automation_floats.txt")

    k = 0
    while k < len(f_input):
        res, m = auto.max_string(f_input, k)
        if res:
            f_output.write(f_input[k:(k + m)] + "\n")
            k += max(1, m)
        else:
            k += 1


def test_auto_float_numbers(test_strings=None):
    auto = create_auto_for_float_numbers()
    if not test_strings:
        test_strings = ["0.23e5 test", "e5.23 test", ".", "34."]
    for test_str in test_strings:
        print(auto.max_string(test_str, 0))


def test_search_float_numbers_in_text(file_names=None):
    path = "test_data/task_1/"
    if not file_names:
        file_names = [path + "text_with_float_numbers_1.txt"]
    else:
        file_names = [path + name for name in file_names]

    for name in file_names:
        search_float_numbers_in_text(name)


# test_auto_float_numbers()
test_search_float_numbers_in_text()
