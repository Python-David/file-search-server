import socket
import ssl
import threading
from time import perf_counter
from typing import Optional

from config.settings import get_settings
from project.search_scripts.hash_set_search import initialize_searcher, search_string_in_file_hash_set
from project.search_scripts.linear_search import read_file_contents, search_string_in_file
from utils.logger import get_logger

settings = get_settings()
logger = get_logger(__name__)

# # Initialize the rate limiter
# rate_limiter = RateLimiter(
#     max_requests=settings.max_requests,
#     window_size=settings.window_size,
#     base_backoff=settings.base_backoff,
# )


def handle_client_connection(
    client_socket: socket.socket,
    client_address: str,
    file_path: str,
    reread_on_query: bool,
    file_contents: Optional[str] = None,
) -> None:
    client_ip = client_address[0]

    try:
        # if not rate_limiter.is_allowed(client_ip):
        #     response = "Too many requests, please try again later.\n"
        #     client_socket.send(response.encode("utf-8"))
        #     logger.warning(f"Rate limit exceeded for {client_address}")
        #     return

        request_start_time = perf_counter()
        request = (
            client_socket.recv(settings.max_payload_size)
            .decode("utf-8", errors="ignore")
            .rstrip("\x00")
            .strip()
        )
        request_end_time = perf_counter()
        logger.debug(
            f"Time to receive and decode request: {(request_end_time - request_start_time) * 1e3:.3f} milliseconds"
        )

        search_start_time = perf_counter()

        if reread_on_query:
            exists = search_string_in_file(file_path, request)
        else:
            exists = search_string_in_file_hash_set(request, reread_on_query)

        search_end_time = perf_counter()
        logger.debug(
            f"Total search time: {(search_end_time - search_start_time) * 1e3:.3f} milliseconds"
        )

        response_start_time = perf_counter()
        response = "STRING EXISTS\n" if exists else "STRING NOT FOUND\n"
        client_socket.send(response.encode("utf-8"))
        response_end_time = perf_counter()
        logger.debug(
            f"Time to prepare and send response: {(response_end_time - response_start_time) * 1e3:.3f} milliseconds"
        )

        total_end_time = perf_counter()
        execution_time = (
            total_end_time - request_start_time
        ) * 1e3  # Convert to milliseconds for higher precision
        logger.debug(f"Execution time: {execution_time:.3f} milliseconds")
        logger.debug(f"Request handled successfully from {client_ip}")
    except socket.timeout as e:
        logger.error(f"Connection timed out: {e}")
    except OSError as e:
        logger.error(f"OS error handling client connection: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during client connection handling: {e}")
    finally:
        client_socket.close()
        logger.info(f"Closed client connection from {client_address}")


def start_server(
    bind_address: str,
    port: int,
    file_path: str,
    server_backlog: int,
    reread_on_query: bool,
) -> None:
    """
    Start a server.

    :param bind_address: The address to bind the server to.
    :param port: The port to listen on.
    :param file_path: The path to the configuration file.
    :param server_backlog: The maximum backlog of connections.
    :param reread_on_query: Boolean indicating whether to re-read the file on each query.
    :return: None
    """

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((bind_address, port))
        server.listen(server_backlog)
        logger.info(
            f"Server listening on {bind_address}:{port} with backlog {server_backlog} and file_path {file_path}"
        )

        if settings.ssl_enabled:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(
                certfile=settings.certfile_path,
                keyfile=settings.keyfile_path,
                password=settings.ssl_key,
            )
            server = context.wrap_socket(server, server_side=True)

    except (socket.timeout, OSError) as e:
        logger.error(f"Socket error during server setup: {e}")
        return
    except Exception as e:
        logger.error(f"Unexpected error during server setup: {e}")
        return

    # TODO CATCH SSL ERRORS AND NOT SOCKET ERRORS

    initialize_searcher(file_path, reread_on_query)

    # Read file contents if not rereading on each query
    file_contents = None
    if not reread_on_query:
        file_contents = read_file_contents(file_path)

    try:
        while True:
            try:
                client_sock, client_address = server.accept()
                logger.info(f"Accepted connection from {client_address}")
                client_handler = threading.Thread(
                    target=handle_client_connection,
                    args=(
                        client_sock,
                        client_address,
                        file_path,
                        reread_on_query,
                        file_contents,
                    ),
                )
                client_handler.start()
            except (socket.timeout, OSError) as e:
                logger.error(f"Socket error accepting client connection: {e}")
            except Exception as e:
                logger.error(f"Unexpected error during client handling: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in the server loop: {e}")
    finally:
        server.close()
        logger.info("Server closed")
