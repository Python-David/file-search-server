import logging
import os

import pytest

# Ensure the log directory exists
log_dir = "tests/performance/reports"
os.makedirs(log_dir, exist_ok=True)

# Set up logging
log_file = os.path.join(log_dir, "performance_limit.log")
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
        # Increase the load gradually
        for num_queries in [10, 50, 100, 200, 500, 1000, 2000, 5000, 10000]:
            try:
                execution_time_seconds = measure_execution_time(
                    test_file_path, num_queries
                )
                execution_time_milliseconds = execution_time_seconds * 1000
                qps = num_queries / execution_time_seconds

                # Log the results
                result_message = (
                    f"File size: {file_size}, Queries: {num_queries}, "
                    f"Avg. execution time: {execution_time_milliseconds:.3f} ms, "
                    f"Queries per second (QPS): {qps:.2f}"
                )
                print(result_message)
                logging.info(result_message)

                # Check if the server is still handling the load well
                if (
                    execution_time_seconds > 1
                ):  # If average response time exceeds 1 second
                    raise RuntimeError("Server response time too high")
            except Exception as e:
                # Document the limitation
                limitation_message = (
                    f"Server limitation reached for file size {file_size} "
                    f"at {num_queries} queries: {str(e)}"
                )
                print(limitation_message)
                logging.info(limitation_message)
                break
    finally:
        # Teardown the server
        server_process.terminate()
        server_process.wait()
