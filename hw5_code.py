import sys
import math
import random

# Global variables
STRING = "Information theory studies the transmission, processing, extraction, and utilization of information. " \
         "Abstractly, information can be thought of as the resolution of uncertainty. In the case of communication of " \
         "information over a noisy channel, this abstract concept was formalized by Claude Shannon in a paper " \
         "entitled A Mathematical Theory of Communication, in which information is thought of as a set of possible " \
         "messages, and the goal is to send these messages over a noisy channel, and to have the receiver reconstruct " \
         "the message with low probability of error, in spite of the channel noise. Shannon main result, " \
         "the noisy-channel coding theorem showed that, in the limit of many channel uses, the rate of information " \
         "that is asymptotically achievable is equal to the channel capacity, a quantity dependent merely on the " \
         "statistics of the channel over which the messages are sent. Coding theory is concerned with finding " \
         "explicit methods, called codes, for increasing the efficiency and reducing the error rate of data " \
         "communication over noisy channels to near the channel capacity. These codes can be roughly subdivided into " \
         "data compression and error-correction techniques. In the latter case, it took many years to find the " \
         "methods Shannon work proved were possible. The recent development of various methods of modulation such as " \
         "PCM and PPM which exchange bandwidth for signal-to-noise ratio has intensified the interest in a general " \
         "theory of communication. A basis for such a theory is contained in the important papers of Nyquist and " \
         "Hartley on this subject. "
codeword = dict()
probability = dict()
symbols = dict()


# helpers
def get_distribution(string):
    for element in string:
        if symbols.get(element) == None:
            symbols[element] = 1
        else:
            symbols[element] += 1
    return symbols


def get_probability():
    for element in symbols:
        probability[element] = symbols.get(element) / len(STRING)
    return probability


def get_codeword(node, parent_code=''):
    this_code = parent_code + str(node.code)
    if (node.l_child):
        get_codeword(node.r_child, this_code)
    if (node.r_child):
        get_codeword(node.r_child, this_code)
    if (not node.l_child and not node.r_child):
        codeword[node.symbol] = this_code
    return codeword


class Node:
    def __init__(self, freq, symbol, l_child=None, r_child=None):
        self.freq = freq
        self.symbol = symbol
        self.l_child = l_child
        self.r_child = r_child
        self.code = ''


# Program Entrance
def huffman_code():
    entropy = 0.0
    avg_code_len = 0.0

    get_distribution(STRING)
    get_probability()
    print(probability)

    nodes = []
    for symbol in symbols:
        nodes.append(Node(symbols.get(symbol), symbol, None, None))

    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.freq)

        right = nodes[0]
        left = nodes[1]

        left.code = 0
        right.code = 1

        new_node = Node(left.freq + right.freq, left.symbol + right.symbol, left, right)

        nodes.remove(left)
        nodes.remove(right)
        nodes.append(new_node)

    tree = get_codeword(nodes[0])
    print(tree)


huffman_code()
print(symbols)
print("Average Code Length =", avg_code_len)
print("Entropy =", entropy)