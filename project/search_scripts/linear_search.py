from time import perf_counter

from utils.logger import get_logger

logger = get_logger(__name__)


def search_string_in_file(file_path: str, search_string: str) -> bool:
    """
    Search for a specific string in a file using a LINEAR SEARCH ALGORITHM. The function reads the file line by line
    and checks if any line, stripped of leading and trailing whitespace, exactly matches the search string.

    This is a linear search algorithm because it goes through each line of the file one by one and compares it to
    the search string.

    :param file_path: The path to the file to be searched.
    :param search_string: The string to search for within the file.
    :return: True if the search string is found in the file, False otherwise.
    """
    start_time = perf_counter()
    try:
        with open(file_path, "r") as file:
            for line in file:
                if search_string in line.strip():
                    return True
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return False
    except IOError as e:
        logger.error(f"IO error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error reading file: {e}")
        return False
    finally:
        end_time = perf_counter()
        execution_time = (end_time - start_time) * 1e3  # Convert to milliseconds
        logger.info(
            f"search_string_in_file execution time: {execution_time:.3f} milliseconds"
        )
    return False


def read_file_contents(file_path: str) -> str:
    """
    Read the contents of a file and return it as a string.

    :param file_path: The path to the file to be read.
    :return: The contents of the file as a string.
    """
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return ""
    except IOError as e:
        logger.error(f"IO error: {e}")
        return ""
    except Exception as e:
        logger.error(f"Unexpected error reading file: {e}")
        return ""
