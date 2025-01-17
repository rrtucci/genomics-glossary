from string import ascii_uppercase
import re

def remove_parenthetical_remark(text):
    return re.sub(r'\s*\([^)]*\)', '', text)


def find_substring(s):
    # Find the substring after the last hashtag
    last_hashtag_index = s.rfind('#')
    if last_hashtag_index != -1 and last_hashtag_index + 1 < len(s):
        substring = s[last_hashtag_index + 1:]
        if substring:  # Check if the substring is non-empty
            return substring

    # If the substring after the last hashtag is empty or no hashtag exists, check for the last backslash
    last_slash_index = s.rfind('/')
    if last_slash_index != -1 and last_slash_index + 1 < len(s):
        substring = s[last_slash_index + 1:]
        return substring

    # If neither condition is met, assert error
    assert False, "could not find string"

def read_link_file(path):
    letter_to_list = {}
    for letter in ascii_uppercase:
        letter_to_list[letter] = []
    with open(path, "r") as f:
        for line in f:
            word = find_substring(line)
            letter_to_list[word[0]].append([word.strip(), line.strip()])
    for letter in ascii_uppercase:
        letter_to_list[letter] = sorted(letter_to_list[letter],
                                        key=lambda tup: tup[0])
    return letter_to_list

def write_latex_glossary(folder):
    letter_to_list = read_link_file(folder + "\\wiki-link-list.txt")
    with open(folder + "\\latex_glossary.tex", "w") as f:
        f.write("\\documentclass{article}\n")
        f.write("\\usepackage{multicol}\n")
        f.write("\\usepackage{hyperref}\n")
        f.write("\\begin{document}\n")
        f.write("\n\n")
        f.write("\\setlength{\\columnsep}{3cm}\n")
        f.write("\\begin{multicols}{3}\n")
        f.write("\\noindent\n")
        for letter, lst in letter_to_list.items():
            f.write("---{\\bf " + letter + "}---\\newline\n")
            for word, link in lst:
                w = remove_parenthetical_remark(word)
                if w[-1]=="_":
                    w = w[:-1]
                w = w.replace("_", "\_")
                f.write("\\href{" + link + "}{" + w + "}\\newline\n")
        f.write("\\end{multicols}\n")
        f.write("\n\n")
        f.write("\\end{document}\n")

if __name__ == "__main__":

    write_latex_glossary("genomics")