def find_common_prefix(s1: str, s2: str) -> str:
    """
    Finds a common prefix that is shared between two strings, if there is one.
    Order of arguments is NOT important.

    This function is provided as a UTILITY for extracting information from JSON
    generated by partial_json_parser, to help in ensuring that the right tokens
    are returned in streaming, so that close-quotes, close-brackets and
    close-braces are not returned prematurely.

    e.g. find_common_prefix('{"fruit": "ap"}', '{"fruit": "apple"}') ->
    '{"fruit": "ap'
    """
    prefix = ''
    min_length = min(len(s1), len(s2))
    for i in range(0, min_length):
        if s1[i] == s2[i]:
            prefix += s1[i]
        else:
            break
    return prefix


def find_common_suffix(s1: str, s2: str) -> str:
    """
    Finds a common suffix shared between two strings, if there is one. Order of
    arguments is NOT important.
    Stops when the suffix ends OR it hits an alphanumeric character

    e.g. find_common_suffix('{"fruit": "ap"}', '{"fruit": "apple"}') -> '"}'
    """
    suffix = ''
    min_length = min(len(s1), len(s2))
    for i in range(1, min_length + 1):
        if s1[-i] == s2[-i] and not s1[-i].isalnum():
            suffix = s1[-i] + suffix
        else:
            break
    return suffix


def extract_intermediate_diff(curr: str, old: str) -> str:
    """
    Given two strings, extract the difference in the middle between two strings
    that are known to have a common prefix and/or suffix.

    This function is provided as a UTILITY for extracting information from JSON
    generated by partial_json_parser, to help in ensuring that the right tokens
    are returned in streaming, so that close-quotes, close-brackets and
    close-braces are not returned prematurely. The order of arguments IS
    important - the new version of the partially-parsed JSON must be the first
    argument, and the secnod argument must be from the previous generation.

    What it returns, is tokens that should be streamed to the client.

    e.g. extract_intermediate_diff('{"fruit": "apple"}', '{"fruit": "ap"}')
        -> 'ple'

    """
    suffix = find_common_suffix(curr, old)

    old = old[::-1].replace(suffix[::-1], '', 1)[::-1]
    prefix = find_common_prefix(curr, old)
    diff = curr
    if len(suffix):
        diff = diff[::-1].replace(suffix[::-1], '', 1)[::-1]

    if len(prefix):
        diff = diff.replace(
            prefix, '',
            1)  # replace the prefix only once in case it's mirrored

    return diff


def find_all_indices(string, substring):
    """
    Find all (starting) indices of a substring in a given string. Useful for
    tool call extraction
    """
    indices = []
    index = -1
    while True:
        index = string.find(substring, index + 1)
        if index == -1:
            break
        indices.append(index)
    return indices
