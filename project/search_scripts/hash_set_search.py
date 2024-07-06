# searcher.py
class HashSetSearcher:
    def __init__(self, file_path):
        self.file_path = file_path
        self.lines_set = set()
        self.cached = False

    def build_hash_set(self):
        lines_set = set()
        with open(self.file_path, "r") as file:
            for line in file:
                lines_set.add(line.strip())
        return lines_set

    def initialize_cache(self):
        if not self.cached:
            self.lines_set = self.build_hash_set()
            self.cached = True

    def search(self, query, reread=False):
        if reread:
            # Build the hash set for each query
            lines_set = self.build_hash_set()
        else:
            # Use the cached hash set
            lines_set = self.lines_set

        return query in lines_set


# Global searcher instance
searcher = None


def initialize_searcher(file_path, reread_on_query):
    global searcher
    searcher = HashSetSearcher(file_path)
    if not reread_on_query:
        searcher.initialize_cache()


def search_string_in_file_hash_set(query, reread_on_query):
    return searcher.search(query, reread_on_query)
