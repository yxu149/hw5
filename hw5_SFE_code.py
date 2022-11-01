# hw5_SFE_code.py
# Shannon–Fano–Elias coding for HW5

"""
Credits & Acknowledgement
https://en.wikipedia.org/wiki/Shannon%E2%80%93Fano%E2%80%93Elias_coding
https://www.youtube.com/watch?v=u0BZe9vh_RU
"""

import math

file = open("string.txt", "r")
STRING = file.read()
MAGIC = 10000000000


def get_frequency(source, symbol_freq=None):
    """
    Gets frequency of each symbol within source string.

    :param source: text string to be analyzed
    :param symbol_freq: a dictionary of (symbol, frequency).
        Null by default.
    :return: a dictionary pair, (symbol, frequency)
    """
    if symbol_freq is None:
        symbol_freq = dict()
    for char in source:
        if symbol_freq.get(char) is None:
            symbol_freq[char] = 1
        else:
            symbol_freq[char] += 1
    return symbol_freq


def get_probability(source, symbol_freq, symbol_prob=None):
    """
    Given source text string and dictionary of symbols
    and frequencies, outputs a dictionary of
    (symbol, probability)

    :param source: source text string
    :param symbol_freq: dictionary of (symbol, frequency)
    :param symbol_prob: dictionary of (symbol, probability).
        Null by default.
    :return: a dictionary pair (symbol, probability)
    """
    if symbol_prob is None:
        symbol_prob = dict()
    for char in source:
        symbol_prob[char] = symbol_freq.get(char) / len(source)

    return symbol_prob


def f_bar(symbol_prob, symbol_z_val=None):
    """
    F-Bar function of the original algorithm.

    :param symbol_prob: dictionary of (symbol, frequency)
    :param symbol_z_val: dictionary of (symbol, Z(symbol)),
        Null by default.
    :return: dictionary of (symbol, Z(symbol)) in base 10
    """
    if symbol_z_val is None:
        symbol_z_val = dict()

    # Special Case: First iteration
    symbol, f_prob = symbol_prob.popitem()
    symbol_z_val[symbol] = f_prob * (1 / 2)

    # General Case: 2nd to 2nd from the last item
    while len(symbol_prob) > 0:
        prev_symbol = symbol
        symbol, f_prob = symbol_prob.popitem()
        symbol_z_val[symbol] = symbol_z_val.get(prev_symbol) * 2 \
            + f_prob * (1 / 2)

    return symbol_z_val


def to_binary(symbol_z_val):
    """
    Parse Z(symbol) into binary values

    :param symbol_z_val: Z(symbol) in decimal
    :return: symbol_z_val dictionary with binary Z values
    """
    for symbol in symbol_z_val:
        symbol_z_val[symbol] = bin(int(symbol_z_val.get(symbol) * MAGIC))

    return symbol_z_val


def encode(symbol_prob, symbol_z_val, symbol_code=None):
    """
    Encoder function. Calculate L(symbol) then concat binary values
    inside symbol_z_val by L(symbol).

    :param symbol_prob: dictionary (symbol, probability)
    :param symbol_z_val: dictionary (symbol, Z(symbol))
    :param symbol_code: dictionary (symbol, SFE code)
    :return:
    """
    if symbol_code is None:
        symbol_code = dict()
    for symbol in symbol_prob:
        symbol_length = math.ceil(math.log2(1 / (symbol_prob.get(symbol)))) + 1
        raw_code = str(symbol_z_val.get(symbol))
        out_code = raw_code[2:symbol_length+2]
        symbol_code[symbol] = out_code

    return symbol_code


# DRIVER CODE BELOW
freq = dict()
prob = dict()
z_val = dict()
code = dict()

freq = get_frequency(STRING, freq)
print("Freq:", freq)
prob = get_probability(STRING, freq, prob)
print("Prob:", prob)
cpy_prob = prob.copy()
z_val = f_bar(cpy_prob, z_val)
print("Z:", z_val)
z_val = to_binary(z_val)
print("Binary Z:", z_val)
code = encode(prob, z_val, code)
print(code)

avg_len = 0.0
entropy = 0.0
for char in code:
    avg_len += len(code.get(char)) * prob.get(char)
    entropy -= prob.get(char) * math.log2(prob.get(char))
print("Average Expected Length =", avg_len)
print("Entropy =", entropy)

file.close()
