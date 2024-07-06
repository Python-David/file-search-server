import os
import random
import socket
import ssl
import string
import subprocess
import time

import pytest

from project.config.settings import get_settings
from project.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()

current_port = settings.base_port


def is_server_running(ip_address, port):
    """Check if the server is ready to accept connections."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        time.sleep(5)
        sock.connect((ip_address, port))
        return True
    except (ConnectionRefusedError, OSError):
        return False
    finally:
        sock.close()


@pytest.fixture(scope="module")
def setup_server():
    """
    Fixture to set up and tear down the server for performance tests.
    """
    global current_port
    processes = []

    def _setup_server(test_file_path):
        global current_port
        # Set the environment variable for the file path
        os.environ["linuxpath"] = test_file_path
        os.environ["port"] = str(current_port)

        # Start the server
        command = "python project/main.py"
        process = subprocess.Popen(command, shell=True)
        processes.append(process)

        # Wait for the server to start and be ready to accept connections
        max_attempts = 10
        for attempt in range(max_attempts):
            if is_server_running(settings.ip_address, current_port):
                logger.info("Server is running and ready to accept connections")
                break
            logger.info("Waiting for the server to be ready...")
            time.sleep(5)
        else:
            process.terminate()
            process.wait()
            raise RuntimeError("Server failed to start within the expected time")

        current_port += 5

        return process

    yield _setup_server

    # Teardown
    for process in processes:
        process.terminate()
        process.wait()


@pytest.fixture(scope="module")
def prepare_test_files():
    """
    Fixture to prepare test files with different sizes.
    """
    file_sizes = [10000, 50000, 100000, 500000, 1000000]
    test_files = []
    test_dir = "tests/performance/test_files"

    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    for size in file_sizes:
        file_path = f"{test_dir}/test_file_{size}.txt"
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                for _ in range(size):
                    line = ";".join(str(random.randint(0, 28)) for _ in range(8)) + ";"
                    f.write(line + "\n")
        test_files.append(file_path)

    return test_files


@pytest.fixture(scope="function")
def query_server():
    """
    Fixture to query the server.
    """

    def _query_server(query):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if settings.ssl_enabled:
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.load_verify_locations(settings.certfile_path)
            client_socket = context.wrap_socket(
                sock, server_hostname=settings.ip_address
            )
        else:
            client_socket = sock

        try:
            port = int(os.getenv("port"))
            client_socket.connect((settings.ip_address, port))
            client_socket.sendall(query.encode("utf-8"))
            response = client_socket.recv(1024).decode("utf-8")
            return response
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            return None
        finally:
            client_socket.close()

    return _query_server


@pytest.fixture(scope="function")
def measure_execution_time(query_server):
    """
    Fixture to measure execution time of queries to the server.
    """

    def _measure_execution_time(file_path, num_queries):
        with open(file_path, "r") as file:
            lines = file.readlines()

        file_size = len(lines)
        if num_queries > file_size:
            raise ValueError(
                "Number of queries requested exceeds the number of lines in the file."
            )

        # Sample lines from different parts of the file
        query_indices = random.sample(range(file_size), num_queries)
        queries = [lines[idx].strip() for idx in query_indices]

        start_time = time.perf_counter()
        for query in queries:
            query_server(query)
        end_time = time.perf_counter()

        return (end_time - start_time) / num_queries

    return _measure_execution_time
