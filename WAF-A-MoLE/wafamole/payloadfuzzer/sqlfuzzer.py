"""Strategies and fuzzer class module"""

import random
import re
import string
from wafamole.payloadfuzzer.fuzz_utils import (
    replace_random,
    filter_candidates,
    random_string,
    num_tautology,
    string_tautology,
    num_contradiction,
    string_contradiction,
)


def reset_inline_comments(payload: str):
    """Remove randomly chosen multi-line comment content.
    Arguments:
        payload: query payload string

    Returns:
        str: payload modified
    """
    positions = list(re.finditer(r"/\*[^(/\*|\*/)]*\*/", payload))

    if not positions:
        return payload

    pos = random.choice(positions).span()

    replacements = ["/**/"]

    replacement = random.choice(replacements)

    new_payload = payload[: pos[0]] + replacement + payload[pos[1] :]

    return new_payload


def logical_invariant(payload):
    """logical_invariant

    Adds an invariant boolean condition to the payload

    E.g., something OR False


    :param payload:
    """

    pos = re.search("(#|-- )", payload)

    if not pos:
        # No comments found
        return payload

    pos = pos.start()

    replacement = random.choice(
        [
            # AND True
            " AND 1",
            " AND True",
            " AND " + num_tautology(),
            " AND " + string_tautology(),
            # OR False
            " OR 0",
            " OR False",
            " OR " + num_contradiction(),
            " OR " + string_contradiction(),
        ]
    )

    new_payload = payload[:pos] + replacement + payload[pos:]

    return new_payload


def change_tautologies(payload):

    results = list(re.finditer(r'((?<=[^\'"\d\wx])\d+(?=[^\'"\d\wx]))=\1', payload))
    if not results:
        return payload
    candidate = random.choice(results)

    replacements = [num_tautology(), string_tautology()]

    replacement = random.choice(replacements)

    new_payload = (
        payload[: candidate.span()[0]] + replacement + payload[candidate.span()[1] :]
    )

    return new_payload


def spaces_to_comments(payload):
    # TODO: make it selectable (can be mixed with other strategies)
    symbols = {" ": ["/**/"], "/**/": [" "]}

    symbols_in_payload = filter_candidates(symbols, payload)

    if not symbols_in_payload:
        return payload

    # Randomly choose symbol
    candidate_symbol = random.choice(symbols_in_payload)
    # Check for possible replacements
    replacements = symbols[candidate_symbol]
    # Choose one replacement randomly
    candidate_replacement = random.choice(replacements)

    # Apply mutation at one random occurrence in the payload
    return replace_random(payload, candidate_symbol, candidate_replacement)


def spaces_to_whitespaces_alternatives(payload):

    symbols = {
        " ": ["\t", "\n", "\f", "\v", "\xa0"],
        "\t": [" ", "\n", "\f", "\v", "\xa0"],
        "\n": ["\t", " ", "\f", "\v", "\xa0"],
        "\f": ["\t", "\n", " ", "\v", "\xa0"],
        "\v": ["\t", "\n", "\f", " ", "\xa0"],
        "\xa0": ["\t", "\n", "\f", "\v", " "],
    }

    symbols_in_payload = filter_candidates(symbols, payload)

    if not symbols_in_payload:
        return payload

    # Randomly choose symbol
    candidate_symbol = random.choice(symbols_in_payload)
    # Check for possible replacements
    replacements = symbols[candidate_symbol]
    # Choose one replacement randomly
    candidate_replacement = random.choice(replacements)

    # Apply mutation at one random occurrence in the payload
    return replace_random(payload, candidate_symbol, candidate_replacement)


def random_case(payload):
    new_payload = []

    for c in payload:
        if random.random() > 0.5:
            c = c.swapcase()
        new_payload.append(c)

    return "".join(new_payload)


def comment_rewriting(payload):

    p = random.random()

    if p < 0.5 and ("#" in payload or "-- " in payload):
        return payload + random_string(2)
    elif p >= 0.5 and ("*/" in payload):
        return replace_random(payload, "*/", random_string() + "*/")
    else:
        return payload


def swap_int_repr(payload):

    candidates = list(re.finditer(r'(?<=[^\'"\d\wx])\d+(?=[^\'"\d\wx])', payload))

    if not candidates:
        return payload

    candidate_pos = random.choice(candidates).span()

    candidate = payload[candidate_pos[0] : candidate_pos[1]]

    replacements = [
        hex(int(candidate)),
        "(SELECT {})".format(candidate),
        # "({})".format(candidate),
    ]

    replacement = random.choice(replacements)

    return payload[: candidate_pos[0]] + replacement + payload[candidate_pos[1] :]


def swap_keywords(payload):

    symbols = {
        # OR
        "||": [" OR ", " || "],
        " || ": [" OR ", "||"],
        "OR": [" OR ", "||"],
        "  OR  ": [" OR ", "||", " || "],
        # AND
        "&&": [" AND ", " && "],
        " && ": ["AND", " AND ", " && "],
        "AND": [" AND ", "&&", " && "],
        "  AND  ": [" AND ", "&&"],
        # Not equals
        "<>": ["!=", " NOT LIKE "],
        "!=": [" != ", "<>", " <> ", " NOT LIKE "],
        # Equals
        " = ": [" LIKE ", "="],
        "LIKE": [" LIKE ", "="],
    }

    symbols_in_payload = filter_candidates(symbols, payload)

    if not symbols_in_payload:
        return payload

    # Randomly choose symbol
    candidate_symbol = random.choice(symbols_in_payload)
    # Check for possible replacements
    replacements = symbols[candidate_symbol]
    # Choose one replacement randomly
    candidate_replacement = random.choice(replacements)

    # Apply mutation at one random occurrence in the payload
    return replace_random(payload, candidate_symbol, candidate_replacement)

def shuffle_integers(payload):
    """shuffle_integers

    Replace number=number or number LIKE number cases with a digit + letter combination of the number's size

    e.g. SELECT admins FROM (SELECT * FROM user WHERE 1782 LIKE 1782) WHERE 999=122
    could become SELECT admins FROM (SELECT * FROM user WHERE a1H9 LIKE a1H9) WHERE 999=122

    :param payload:
    """

    candidates = list(re.finditer(r'[0-9]+', payload))

    if not candidates:
        return payload

    possible_equal_pairs = []
    for i in range(len(candidates)):
        candidate_pos = candidates[i].span()
        # Don't test for = or LIKE in last candidate for out of bounds index
        if (i == len(candidates) - 1):
            continue
        elif (payload[candidate_pos[1]] == '=' 
            or payload[candidate_pos[1]+1:candidate_pos[1]+5] == 'LIKE' ):
            candidate_pair = [candidates[i].span(), candidates[i+1].span()]
            possible_equal_pairs.append(candidate_pair)

    definite_equal_pairs = []
    for pair in possible_equal_pairs:
        first_candidate_pos = pair[0]
        second_candidate_pos = pair[1]

        # Verify that an equal pair of numbers exist
        if (payload[first_candidate_pos[0]:first_candidate_pos[1]] 
            == payload[second_candidate_pos[0]:second_candidate_pos[1]]):
            definite_equal_pairs.append(pair)

    # Nothing gets replaced if no equal pairs are confirmed
    if (len(definite_equal_pairs) < 1 or not definite_equal_pairs):
        return payload 

    pair_to_replace = random.choice(definite_equal_pairs)

    # Build a digit/letter replacement with the size of the paired numbers
    single_replacements = list(string.ascii_letters) + list(range(0,10))
    replacement_size = pair_to_replace[0][1] - pair_to_replace[0][0]
    replacement = ''
    for i in range(replacement_size):
        replacement_unit = str(random.choice(single_replacements))    
        replacement += replacement_unit

    for candidate_pos in pair_to_replace:
        payload = payload[:candidate_pos[0]] + replacement + payload[candidate_pos[1]:]
    
    return payload


class SqlFuzzer(object):
    """SqlFuzzer class"""

    strategies = [
        spaces_to_comments,
        random_case,
        swap_keywords,
        swap_int_repr,
        spaces_to_whitespaces_alternatives,
        comment_rewriting,
        change_tautologies,
        logical_invariant,
        reset_inline_comments,
        shuffle_integers,
    ]

    def __init__(self, payload):
        self.initial_payload = payload
        self.payload = payload

    def fuzz(self):
        strategy = random.choice(self.strategies)

        self.payload = strategy(self.payload)
        # print(self.payload)

        return self.payload

    def current(self):
        return self.payload

    def reset(self):
        self.payload = self.initial_payload
        return self.payload
