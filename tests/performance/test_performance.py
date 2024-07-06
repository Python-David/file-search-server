import logging
import os

import pytest

# Ensure the log directory exists
log_dir = "tests/performance/reports"
os.makedirs(log_dir, exist_ok=True)

# Set up logging
log_file = os.path.join(log_dir, "performance.log")
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(message)s")

# Clear any existing loggers to prevent duplicate logs
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(filename=log_file, level=logging.INFO, format="%(message)s")


@pytest.mark.parametrize("file_size", [10000, 50000, 100000, 500000, 1000000])
def test_performance(
    setup_server, prepare_test_files, measure_execution_time, file_size
):
    """
    Test the performance of the server with different file sizes.
    """
    # Get the path to the test file for the given size
    test_files = prepare_test_files
    test_file_path = next(file for file in test_files if str(file_size) in file)

    # Set up the server with the test file path
    server_process = setup_server(test_file_path)

    try:
        # Measure the execution time for a number of queries
        num_queries = 1
        execution_time = (
            measure_execution_time(test_file_path, num_queries) * 1000
        )  # convert to milliseconds

        # Log the results to both console and file
        result_message = f"Average execution time for file size {file_size}: {execution_time:.3f} milliseconds per query"
        print(result_message)
        logging.info(result_message)
    finally:
        # Teardown the server
        server_process.terminate()
        server_process.wait()
