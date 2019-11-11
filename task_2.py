class Automatic:
    def __init__(self, **kwargs):
        if "filename" in kwargs.keys():
            q, e, b, s, f, priority, lexeme = self.read_from_file(kwargs["filename"])
        else:
            q, e, b, s, f = kwargs["q"], kwargs["e"], kwargs["b"], kwargs["s"], kwargs["f"]
            priority, lexeme = kwargs["priority"], kwargs["lexeme"]
        self.q = q
        self.e = e
        self.b = b
        self.s = set(s)
        self.f = set(f)
        self.priority = priority
        self.lexeme = lexeme
        self.current_state = set(s)

    @staticmethod
    def read_from_file(filename):
        inp_file = open(filename, encoding="utf-8").read().replace("\n", "").split("-----")
        lexeme = inp_file[0]
        priority = inp_file[1]
        q = inp_file[2].split()
        s = inp_file[5].split()
        f = inp_file[6].split()

        b = dict()
        for line in inp_file[4].split(";"):
            if len(line):
                cur_st, pairs = line.split(": ")
                for pair in pairs.split(", "):
                    signal, new_state = pair.split()
                    b[cur_st, signal] = new_state

        e = dict()
        for line in inp_file[3].split("==="):
            if len(line):
                inp_type, chars = line.split(": ")
                e[inp_type] = chars.split("|||")

        return q, e, b, s, f, int(priority), lexeme

    def change_state(self, signal):
        if signal not in self.e.keys():
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
            char = self.transform_special(char)
            char = self.transform_input(char)

            # check if automation didn't broke
            if not self.change_state(char):
                break

            # check if one of the current states can be final state
            if self.current_state & self.f:
                flag = True
                m = i + 1

        return flag, m

    # defines the type of input signal for entered character
    def transform_input(self, c):
        for inp_type in self.e.items():
            if c in inp_type[1]:
                return inp_type[0]
        return None

    # changes special characters, so that it will be easy to use them
    @staticmethod
    def transform_special(c):
        if c == "\n":
            return "\\n"
        if c == "\t":
            return "\\t"
        if c == "\r":
            return "\\r"
        if c == " ":
            return "\s"
        return c


def create_autos_from_file(file_names):
    autos = []
    for filename in file_names:
        autos.append(Automatic(filename=filename))
    return autos


def search_lexemes_in_text(text_filename, auto_filename):
    f_input = open(text_filename, encoding="utf-8").read()
    f_output_name = text_filename[:-4] + "_output.txt"
    f_output = open(f_output_name, "w+", encoding="utf-8")
    autos = create_autos_from_file(auto_filename)

    k = 0
    while k < len(f_input):
        cur_lex = None
        cur_pr, m = 0, 0

        for auto in autos:
            res, r = auto.max_string(f_input, k)
            # print(f"{auto.lexeme}: {res} -- {r}")
            if res:
                if m < r:
                    cur_lex = auto.lexeme
                    cur_pr = auto.priority
                    m = r
                elif m == r and cur_pr < auto.priority:
                    cur_lex = auto.lexeme
                    cur_pr = auto.priority

        if m > 0:
            ans = f_input[k:(k + m)]
            # this is needed to display characters like \n, \t or \r in correct way
            ans = "".join([Automatic.transform_special(c) for c in ans])

            f_output.write(f"<{cur_lex}, {ans}>\n")
            k += max(1, m)
        else:
            ans = f_input[k]
            # this is needed to display characters like \n, \t or \r in correct way
            ans = "".join([Automatic.transform_special(c) for c in ans])

            f_output.write(f"<error, {ans}>\n")
            k += 1


def test_search_float_numbers_in_text(text_file_names=None, auto_file_names=None):
    path = "test_data/task_2/"
    if not text_file_names:
        text_files = [path + "text_with_float_numbers_1.txt"]
    else:
        text_files = [path + name for name in text_file_names]

    if not auto_file_names:
        auto_files = [path + "automation_floats.txt"]
    else:
        auto_files = [path + name for name in auto_file_names]

    for name in text_files:
        search_lexemes_in_text(name, auto_files)


# test_auto_float_numbers()
test_search_float_numbers_in_text(["text_with_float_numbers_1.txt"],
                                  ["automation_floats.txt", "automation_spaces.txt"])
