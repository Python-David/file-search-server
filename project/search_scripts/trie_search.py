from functools import lru_cache
from time import perf_counter

from utils.logger import get_logger

logger = get_logger(__name__)


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word


@lru_cache(maxsize=1)
def build_trie_from_file(file_path: str) -> Trie:
    trie = Trie()
    try:
        with open(file_path, "r") as file:
            for line in file:
                trie.insert(line.strip())
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except IOError as e:
        logger.error(f"IO error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error reading file: {e}")
        return None
    return trie


def search_string_in_file(file_path: str, search_string: str) -> bool:
    """
    Search for a specific string in a file using a TRIE. The function builds a Trie from the file lines
    and then searches the Trie for the search string.

    :param file_path: The path to the file to be searched.
    :param search_string: The string to search for within the file.
    :return: True if the search string is found in the file, False otherwise.
    """
    start_time = perf_counter()
    trie = build_trie_from_file(file_path)

    if trie is None:
        return False

    try:
        result = trie.search(search_string)
    except Exception as e:
        logger.error(f"Unexpected error during search: {e}")
        return False
    finally:
        end_time = perf_counter()
        execution_time = (end_time - start_time) * 1e3  # Convert to milliseconds
        logger.info(
            f"search_string_in_file execution time: {execution_time:.3f} milliseconds"
        )

    return result
