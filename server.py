from shopping import __version__
import argparse
import logging
import os
import pathlib
from typing import Optional
import connexion
from flask_sqlalchemy import SQLAlchemy

# from bobcat_common.connexion_common import (
#     connexion_error_handler,
#     log_request,
#     log_response,
#     register_server_info,
#     set_connexion_error_handler,
# )
from flask.app import Flask
from flask.testing import FlaskClient


DEFAULT_CONFIG = os.path.join("examples", "config.yaml")


def app_factory() -> Flask:
    """Add routes app"""
    connexion_app = connexion.App(__name__, specification_dir="openapi/")
    # API from /openapi/*
    connexion_app.add_api(pathlib.Path("api.yaml"))

    #connexion_app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.sqlite'
    return connexion_app.app


def generate_app(config_file: Optional[str] = None) -> Flask:
    """Generate app"""
    # if config_file is None:
    #     try:
    #         config_file = os.environ["BOBCAT_INVOICE_CONFIG"]
    #     except KeyError:
    #         config_file = DEFAULT_CONFIG
    # shared.init(config_file)
    return app_factory()


def generate_test_client(config_file: str) -> FlaskClient:
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

    app = generate_app(args.config)

    logging.info(f"Starting Shopping List System version {__version__}")

    if args.port is None:
        args.port = 8080
    app.run(port=args.port, host=args.host)


if __name__ == "__main__":
    main()
