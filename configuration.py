"""Configuration management"""

import logging
import os
from typing import Dict, Optional

import yaml

DEFAULT_CONFIG = "config.yaml"
logger = logging.getLogger(__name__)


class Configuration:
    def __init__(self, conf: Dict) -> None:
        self.sqlite = conf.get("sqlite", {})
        
        logger.debug(f"Loaded {''.join([i for i in conf.keys()])} ")

    @classmethod
    def create_from_config_file(cls, filename: Optional[str]):
        """Load configuration as YAML"""
        if filename is None:
            default_file = os.environ.get("SYSTEM_CONFIG", DEFAULT_CONFIG)
            if os.path.exists(default_file):
                filename = default_file
        if filename:
            f = open(filename, "r")
            config_dict = yaml.safe_load(f)
        else:
            logging.debug("No configuration file, use default")
            config_dict = {}
        return cls(config_dict)


config: Configuration


def init(config_file: Optional[str] = None) -> None:
    """Initialize shared resources"""
    global config

    try:
        config = Configuration.create_from_config_file(config_file)
    except Exception as e:
        logger.critical(f"Init failed {e}")
        raise
