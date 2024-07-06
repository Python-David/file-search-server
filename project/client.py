import socket
import ssl

from config.settings import get_settings
from project.search_scripts.linear_search import get_logger

settings = get_settings()
logger = get_logger(__name__)

ip_address = settings.ip_address
port = settings.port
use_ssl = settings.ssl_enabled


def query_server(query):
    """
    Connect to the server, send a query, and return the response.

    :param query: The query string to send to the server.
    :return: The response from the server.
    """

    # Create a plain (non-SSL) socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if use_ssl:
        # Wrap the socket with SSL
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_verify_locations(
            settings.certfile_path
        )  # Ensure the client trusts the server certificate
        client_socket = context.wrap_socket(sock, server_hostname=ip_address)
    else:
        client_socket = sock

    try:
        # Connect to the server
        client_socket.connect((ip_address, port))
        logger.debug(f"Successfully connected to {ip_address} on port {port}")

        # Send the query string
        client_socket.sendall(query.encode("utf-8"))

        # Receive the response from the server
        response = client_socket.recv(1024).decode("utf-8")
        logger.debug(f"Received from server: {response}")

        return response

    except Exception as e:
        logger.error(f"Failed to connect: {e}")
        return None

    finally:
        # Close the socket
        client_socket.close()
        logger.info("Connection closed...")


# Example usage
example_query = settings.query_string
server_response = query_server(example_query)
