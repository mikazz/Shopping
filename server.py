import argparse
import logging
import os
import pathlib
from typing import Optional

import connexion
from flask.app import Flask
from shopping import __version__, db_session

DEFAULT_CONFIG = os.path.join("config.yaml")
logger = logging.getLogger(__name__)


def app_factory() -> Flask:
    """Add routes app"""
    connexion_app = connexion.App(__name__, specification_dir="openapi/")
    # API from /openapi/*
    connexion_app.add_api(pathlib.Path("api.yaml"))
    return connexion_app.app


def generate_app(config_file: Optional[str] = None) -> Flask:
    """Generate app"""
    db_session.global_init('mars_db.sqlite')
    return app_factory()


def generate_test_client(config_file: Optional[str] = None):
    """Unit servertest"""
    app = generate_app(config_file)
    return app.test_client()


def main() -> None:
    """Main function"""

    parser = argparse.ArgumentParser(description="Shopping System")

    parser.add_argument("--config", dest="config", metavar="filename", help="Configuration file", default=DEFAULT_CONFIG)
    parser.add_argument("--host", dest="host", help="Host address to bind to", default="127.0.0.1")
    parser.add_argument("--port", dest="port", help="Port to listen on")
    parser.add_argument("--debug", dest="debug", action="store_true", help="Enable debugging")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    app = generate_app(args.config)
    logger.info(f"Starting Shopping List System version {__version__}")
    if args.port is None:
        args.port = 9999
    app.run(port=args.port, host=args.host)


if __name__ == "__main__":
    main()

