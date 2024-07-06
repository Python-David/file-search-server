from config.settings import get_settings
from project.search_scripts.linear_search import get_logger
from server import start_server

settings = get_settings()
logger = get_logger(__name__)


if __name__ == "__main__":
    """
    Main entry point for starting the server. Reads the necessary configuration from config
    and starts the server with the specified parameters.
    """

    try:
        path = settings.linuxpath
        start_server(
            bind_address=settings.bind_address,
            port=settings.port,
            file_path=path,
            server_backlog=settings.server_backlog,
            reread_on_query=settings.reread_on_query,
        )
    except Exception as e:
        logger.error(f"An error occurred while starting the server: {e}")
