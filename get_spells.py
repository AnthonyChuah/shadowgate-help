def main():
    list_all_spells = list()
    with open("helpspells.txt", "r") as f:
        for line in f:
            split_by_space = line.split()
            list_all_spells.extend(split_by_space)
    print("Got all spells: printing list now")
    print(list_all_spells)
    with open("newline_delim.txt", "w") as f:
        for line in list_all_spells:
            f.write(line + "\n\n")

if __name__ == "__main__":
    main()
