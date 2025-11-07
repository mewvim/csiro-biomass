import os
import random
from argparse import ArgumentParser, Namespace

import numpy as np
from csiro.logging_config import get_logger, setup_logging


def get_config() -> Namespace:
    # parses global level arguments, accessible to any subparser
    # i.e. log-level
    global_parser = ArgumentParser(add_help=False)
    global_parser.add_argument("--seed", type=int, default=4, help="seed randomizers")
    global_parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level",
    )

    parser = ArgumentParser(prog="csiro", description="csiro biomass project")
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands", required=True
    )

    dataset_parser = subparsers.add_parser(
        "dataset", help="how to obtain dataset", parents=[global_parser]
    )
    dataset_parser.add_argument(
        "--download", type=str, required=True, help="kaggle username/dataset-name path"
    )

    config = parser.parse_args()

    return config


def reproduceability(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


def main() -> None:
    # setup application config
    config = get_config()

    # setup application logging
    setup_logging(config.log_level)
    logger = get_logger(__name__)

    # setup reproduceability
    reproduceability(config.seed)

    logger.debug(f"All configuration: {config}")

    # downloading data
    if config.command == "dataset":
        print("going to try to download dataset")
