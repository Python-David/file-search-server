# kmp.py
def compute_partial_match_table(pattern):
    """Compute the partial match table (prefix function) for KMP algorithm."""
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text, pattern, lps):
    """Perform KMP search using the precomputed partial match table."""
    n = len(text)
    m = len(pattern)
    i = 0  # index for text
    j = 0  # index for pattern

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            return True  # Match found
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return False  # No match found


def precompute_partial_match_tables(file_path):
    """Precompute partial match tables for each line in the file."""
    tables = {}
    with open(file_path, "r") as file:
        for line in file:
            stripped_line = line.strip()
            tables[stripped_line] = compute_partial_match_table(stripped_line)
    return tables


class KMPMatcher:
    def __init__(self, file_path):
        self.file_path = file_path
        self.pattern_tables = {}
        self.cached = False

    def initialize_cache(self):
        if not self.cached:
            self.pattern_tables = precompute_partial_match_tables(self.file_path)
            self.cached = True

    def search(self, query, reread=False):
        if reread:
            # Compute the partial match table for the query
            lps = compute_partial_match_table(query)
            with open(self.file_path, "r") as file:
                for line in file:
                    if kmp_search(line.strip(), query, lps):
                        return True
        else:
            # Use precomputed partial match tables if available
            if query not in self.pattern_tables:
                return False
            lps = self.pattern_tables[query]
            with open(self.file_path, "r") as file:
                for line in file:
                    if kmp_search(line.strip(), query, lps):
                        return True
        return False


# Global matcher instance
matcher = None


def initialize_matcher(file_path, reread_on_query):
    global matcher
    matcher = KMPMatcher(file_path)
    if not reread_on_query:
        matcher.initialize_cache()


def search_string_in_file(query, reread_on_query):
    return matcher.search(query, reread_on_query)
