# boyer_moore.py


def bad_character_heuristic(pattern):
    """Generate the bad character heuristic table."""
    bad_char = [-1] * 256
    for i in range(len(pattern)):
        bad_char[ord(pattern[i])] = i
    return bad_char


def good_suffix_heuristic(pattern):
    """Generate the good suffix heuristic table."""
    m = len(pattern)
    good_suffix = [0] * (m + 1)
    border_pos = [0] * (m + 1)

    i = m
    j = m + 1
    border_pos[i] = j

    while i > 0:
        while j <= m and pattern[i - 1] != pattern[j - 1]:
            if good_suffix[j] == 0:
                good_suffix[j] = j - i
            j = border_pos[j]
        i -= 1
        j -= 1
        border_pos[i] = j

    j = border_pos[0]
    for i in range(m + 1):
        if good_suffix[i] == 0:
            good_suffix[i] = j
        if i == j:
            j = border_pos[j]

    return good_suffix


def boyer_moore_search(text, pattern):
    """Perform Boyer-Moore search for the pattern in the text."""
    m = len(pattern)
    n = len(text)

    if m == 0:  # Edge case: empty pattern
        return False

    bad_char = bad_character_heuristic(pattern)
    good_suffix = good_suffix_heuristic(pattern)

    s = 0  # s is the shift of the pattern with respect to text
    while s <= n - m:
        j = m - 1

        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            return True  # Pattern found at position s
        else:
            bad_char_shift = j - bad_char[ord(text[s + j])]
            good_suffix_shift = good_suffix[j + 1]
            s += max(bad_char_shift, good_suffix_shift)

    return False  # Pattern not found
