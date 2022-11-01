import math

"""
Credits & Acknowledgement
https://towardsdatascience.com/huffman-encoding-python-implementation-8448c3654328c
https://www.section.io/engineering-education/huffman-coding-python/
"""

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
node_probs = dict()


class Node:
    def __init__(self, freq, symbol, left_child=None, right_child=None):
        self.freq = freq
        self.symbol = symbol
        self.left_child = left_child
        self.right_child = right_child
        self.code = ''
        self.prob = 0


codes = dict()


def do_code(node, code=''):
    new_code = code + str(node.code)

    if node.left_child:
        do_code(node.left_child, new_code)
    if node.right_child:
        do_code(node.right_child, new_code)
    if not node.left_child and not node.right_child:
        codes[node.symbol] = new_code

    return codes


def get_frequency(source):
    char_freq = dict()
    for char in source:
        if char_freq.get(char) is None:
            char_freq[char] = 1
        else:
            char_freq[char] += 1
    return char_freq


def get_codeword(source, code):
    output = []
    for char in source:
        output.append(code[char])
    out_string = ''.join([str(item) for item in output])
    return out_string


def encode(source):
    symbol_freq = get_frequency(source)
    symbols = symbol_freq.keys()

    nodes = []
    avg_exp_len = 0.0
    entropy = 0.0

    for symbol in symbols:
        nodes.append(Node(symbol_freq.get(symbol), symbol))

    for node in nodes:
        node.prob = node.freq / len(STRING)
        node_probs.update({node.symbol: node.prob})

    while len(nodes) > 1:
        # since probability is directly proportional to frequency
        nodes = sorted(nodes, key=lambda x: x.prob)

        right_node = nodes[0]
        left_node = nodes[1]

        left_node.code = 0
        right_node.code = 1

        new_node = Node(left_node.freq + right_node.freq, left_node.symbol + right_node.symbol, left_node, right_node)

        nodes.remove(left_node)
        nodes.remove(right_node)
        nodes.append(new_node)

    huffman_code = do_code(nodes[0])

    # Format the Output
    print("Symbol - Code")
    for char in huffman_code:
        print(char, "-", huffman_code.get(char))

    for char in huffman_code:
        avg_exp_len += len(huffman_code[char]) * node_probs.get(char)
        entropy -= node_probs.get(char) * math.log2(node_probs.get(char))

    print("Average Expected Length =", avg_exp_len)
    print("Entropy =", entropy)
    output = get_codeword(STRING, huffman_code)

    return output, nodes[0]


out, tree = encode(STRING)
print("\nWhole paragraph encoded:", out)
