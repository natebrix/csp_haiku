# csp_haiku
Solves a constraint satisfaction to generate haiku equations of the form A + B = C.

In English, the equation 77 + 123 = 200 is a 5/7/5 haiku:

    seventy-seven
    plus one hundred twenty three
    equals two hundred
  
Using constraint satisfaction (CSP) we can find all such haikus for numbers below a reasonable threshold. If s\[n\] is the number of syllables in the English-language words for an integer n, and the numbers in the three lines of the haiku are l_1, l_2, l_3, then the model is:

    s[l_1] = 5
    1 + s[l_2] = 7
    2 + s[l_3] = 5
    l_1 + l_2 + l_3

Call make_haikus() to get the haikus and solution_to_text() to print them out.

This code uses Python 3.X and the [constraint](https://labix.org/python-constraint) package.
