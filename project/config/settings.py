import os
from functools import lru_cache

from pydantic_settings import BaseSettings

base_dir: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))


class Settings(BaseSettings):
    """
    Configuration settings for the server.

    :param linuxpath: Path to the data file.
    :param port: Port number for the server to listen on.
    :param bind_address: Address to bind the server to.
    :param server_backlog: Maximum backlog of connections.
    :param max_payload_size: Maximum payload size for incoming requests.
    :param reread_on_query: Whether to re-read the file on each query.
    :param ssl_enabled: Whether SSL/TLS is enabled.
    :param ssl_key: Password for the SSL private key.
    :param ip_address: IP address for the server.
    :param certfile_path: Path to the SSL certificate file.
    :param keyfile_path: Path to the SSL key file.
    :param max_requests: Maximum number of requests allowed within the time window.
    :param window_size: Size of the time window in seconds.
    :param base_backoff: Base backoff time for exponential backoff in seconds.
    :param log_level: Log level.
    :param log_format: Log format.
    :param log_datefmt: Log date format.
    """

    # Server config
    linuxpath: str = os.path.join(base_dir, "project/data/200k.txt")
    port: int = 9999
    bind_address: str = "0.0.0.0"
    server_backlog: int = 5
    max_payload_size: int = 1024
    reread_on_query: bool = True
    query_string: str = "13;0;23;11;0;16;5;0;"

    # SSL config
    ssl_enabled: bool = True
    ssl_key: str = "pass"
    certfile_path: str = os.path.join(base_dir, "project/certificates/server.crt")
    keyfile_path: str = os.path.join(base_dir, "project/certificates/private.key")

    # IP config
    ip_address: str = "192.168.0.137"

    # Rate Limiting config
    max_requests: int = 5
    window_size: int = 10
    base_backoff: int = 1

    # Logging config
    log_level: str = os.getenv("LOG_LEVEL", "DEBUG")
    log_format: str = os.getenv(
        "LOG_FORMAT", "%(asctime)s - %(levelname)s - %(message)s"
    )
    log_datefmt: str = os.getenv("LOG_DATEFMT", "%Y-%m-%d %H:%M:%S")

    # Test config
    base_port: int = 8888

    class Config:
        env_file = os.path.join(base_dir, "project/config/.env")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
