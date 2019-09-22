# haiku.py / September 2019 / Nathan Brixius @natebrix
# 
# Solve a CSP model to get all English-language haikus of the form
#   A
# + B
# = C
# where A, B, C are integers less than 10000.
#

from constraint import *

# the number of syllables in the first twenty numbers in English, starting with ze-ro (2 syllables).
syl_twenty = [2, 1, 1, 1, 1, 1, 1, 2, 1, 1,
              1, 3, 1, 2, 2, 2, 2, 3, 2, 2]

# English words of interest for this problem.
w_ones = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
w_tens = ["", "ten", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
w_hundred = "hundred"
w_thousand = "thousand"
w_plus = "plus"
w_equals = "equals"

def make_syllable_counts():
    """ Returns a dictionary of syllable counts for numbers between 0 - 9999, plus symbols. """
    # 0 - 19
    s = {i: s_i for i, s_i in enumerate(syl_twenty)}
    s['hundred'] = 2
    s['thousand'] = 2
    s['+'] = 1 # "plus"
    s['='] = 2 # "e-quals"

    # 20 - 99
    for tens in range(2, 10):
        s[tens * 10] = 2
        for ones in range(1, 10):
            s[tens * 10 + ones] = s[tens * 10] + syl_twenty[ones]

    # 100 - 999
    for hundreds in range(1, 10):
        for last_two in range(1, 100):
            # "seven hundred seventy-four" -> s(7) + s('hundred') + s(74)
            s[hundreds*100 + last_two] = s[hundreds] + s['hundred'] + s[last_two]
        # "three hundred", not "three hundred zero"
        s[hundreds * 100] = s[hundreds] + s['hundred'] # so 100 will be "one hundred"
    

    # 1000 - 9999
    # you get the idea...
    for thousands in range(1, 10):
        for last_three in range(1, 1000):
            s[thousands*1000 + last_three] = s[thousands] + s['thousand'] + s[last_three]
        # "three thousand", not "three thousand zero"
        s[thousands*1000] = s[thousands] + s['thousand']

    return s

def make_csp(s):
    """ Create a CSP representing the haiku equation problem. """
    problem = Problem()
    numbers = list(range(0, 9999+1))
    problem.addVariable("line_1", numbers)
    problem.addVariable("line_2", numbers)
    problem.addVariable("line_3", numbers)
    problem.addConstraint(lambda line_1: s[line_1] == 5, ["line_1"])
    problem.addConstraint(lambda line_2: s['+'] + s[line_2] == 7, ["line_2"])
    problem.addConstraint(lambda line_3: s['='] + s[line_3] == 5, ["line_3"])
    problem.addConstraint(lambda line_1, line_2, line_3: line_1 + line_2 == line_3, ["line_1", "line_2", "line_3"])
    return problem


def solve(problem):
    """ Solve the CSP model. """
    print('Solving CSP model.')
    return problem.getSolutions()


def make_haikus():
    """ Make all haikus of the form A / + B / = C where A, B, C <= 9999. """
    s = make_syllable_counts()
    problem = make_csp(s)
    return solve(problem)


def num_to_text(n):
    """ Returns the English-language representation of a number from 0-9999. """
    special_separator = "-" if n < 100 else " "
    t = ""
    if n >= 1000:
        thousands = n // 1000
        t = t + w_ones[thousands] + " " + w_thousand + " "
        n = n % 1000
    if n >= 100:
        hundreds = n // 100
        t = t + w_ones[hundreds] + " " + w_hundred + " "
        n = n % 100
    if n > 0:
        if n < 20:
            t = t + w_ones[n]
        else:
            tens = n // 10
            n = n % 10
            t = t + w_tens[tens]
            if n > 0: # avoid "thirty zero"
                t = t + special_separator + w_ones[n]
    return t.strip()


def solution_to_text(s):
    """ Returns the haiku text represented by a CSP solution. """
    return num_to_text(s['line_1']) + "\n" \
        +  w_plus + " " + num_to_text(s['line_2']) + "\n" \
        +  w_equals + " " + num_to_text(s['line_3']) + "\n" 

