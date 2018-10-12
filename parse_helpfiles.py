import heapq
import os

end_spell_help = "Hit <return> to continue: \n"
start_spell_help = "Spell: "

clas_list = ("bard", "cleric", "druid", "mage", "mage/sorc", "monk", "paladin", "psion", "psywarrior", "ranger", "warlock")

def find_index(value, container):
    for idx, val in enumerate(container):
        if val == value:
            return (idx, val)
    return (-1, "")

class Spell(object):

    def __init__(self, clas, level, desc):
        self._clas = clas
        self._level = level # int
        self._desc = desc

    def __lt__(self, other):
        if self._clas == other._clas:
            return self._level < other._level
        else:
            return self._clas < other._clas

    def __gt__(self, other):
        return self > other

    def __str__(self):
        return "Class: {}\nLevel: {}\nDescription:\n{}".format(self._clas, self._level, self._desc)

class Parser(object):

    def __init__(self):
        self._parse_state_inside = False
        self._output_string = str()
        self._this_help_string = str()
        self._this_help_cl_lev = list() # list of tuples (str, int)
        self._help_dictionary = dict() # "classname": Spell
        for clas in clas_list:
            self._help_dictionary[clas] = list()
            heapq.heapify(self._help_dictionary[clas])

    def _parse_level_token(self, token):
        trail_comma = False
        if token[-1] == ",":
            trail_comma = True
        # Cases: smallest is len 2, e.g. L9. Biggest is len 4, e.g. L15,
        if trail_comma:
            return token[1:(len(token) - 1)]
        else:
            return token[1:len(token)]

    def _track_cl_lev(self, line):
        tokens = line.split()
        this_cl_lev = ["", -1]
        for tok in tokens:
            idx, clasname = find_index(tok, clas_list)
            # print("Found idx={} clasname={}".format(idx, clasname))
            if idx == -1 and tok[0] != "L":
                continue # Because either we encounter "classname" or we encounter "L1,"/"L1"
            if clasname == "mage/sorc":
                clasname = "mage"
            if this_cl_lev[1] >= 0:
                # We've previously set the level, so we were previously done: now append and reset
                this_cl_lev[0] = ""
                this_cl_lev[1] = -1
            if this_cl_lev[0] == "":
                # I've just encountered the class string token. Next token will be a Level
                this_cl_lev[0] = clasname # e.g. "mage"
            elif len(this_cl_lev[0]) > 0:
                # This is a Level corresponding to a classname in previous token
                level = self._parse_level_token(tok)
                this_cl_lev[1] = int(level)
                self._this_help_cl_lev.append(this_cl_lev)

    def _record_spell(self):
        # this_help_cl_lev is a list(list(classname, level)), i.e. list of pairs
        # this_help_string is a string of the spell description
        # Insert key, value into self._help_dictionary, where key = "mage", value = Spell()
        # print("Called _record_spell")
        for ll in self._this_help_cl_lev:
            clasname, level = ll[0], ll[1]
            spell = Spell(clasname, level, self._this_help_string)
            # print("Recording {} spell: {}".format(clasname, str(spell)))
            heapq.heappush(self._help_dictionary[clasname], spell)

    def load_helpfiles(self):
        with open("spells_helpfiles.txt", "r") as f:
            for line in f:
                if line == end_spell_help:
                    # print("End of spell help")
                    self._record_spell()
                    self._parse_state_inside = False
                    self._this_help_string = ""
                    self._this_help_cl_lev.clear()
                elif line.startswith(start_spell_help):
                    # print("Start of spell help")
                    self._parse_state_inside = True
                if self._parse_state_inside:
                    # Copy the line across to my output string
                    # print("Copied line to output: {}".format(line))
                    self._output_string += line
                    self._this_help_string += line
                    if line.startswith("Class: "):
                        # print("Found a class line: {}".format(line))
                        self._track_cl_lev(line)

    def write_output(self):
        with open("clean_helpfiles.txt", "w") as f:
            f.write(self._output_string)

    def write_spell_dictionary(self, output_dir):
        for clasname, heap in self._help_dictionary.items():
            for spell in heap:
                levelstr = "L" + str(spell._level)
                fname = levelstr + ".txt"
                out_dir = os.path.join(output_dir, clasname)
                os.makedirs(out_dir, exist_ok=True)
                out_path = os.path.join(out_dir, fname)
                with open(out_path, "a") as f:
                    f.write(spell._desc)

def main():
    parser = Parser()
    parser.load_helpfiles()
    parser.write_output()
    parser.write_spell_dictionary("spells")

if __name__ == "__main__":
    main()
