import json
import os
from pathlib import Path

from kaggle.api.kaggle_api_extended import KaggleApi

from csiro.logging_config import get_logger

logger = get_logger(__name__)


class CsiroDataset:
    competition_name: str = "csiro-biomass"

    kaggle_config: Path = (
        Path(os.path.expanduser("~")).joinpath(".kaggle").joinpath("kaggle.json")
    )

    def __init__(self, username: str | None = None, key: str | None = None):
        logger.info("Attempting to download the csiro dataset")

        self.username = username
        self.key = key
        self.build_kaggle_credentials()

        logger.info("Configured kaggle credentials")

    def download_dataset(self, output: Path) -> None:
        try:
            api = KaggleApi()
            api.authenticate()
            logger.info("Kaggle authentication complete")
            api.competition_download_files(
                CsiroDataset.competition_name,
                path=output,
                quiet=False,
            )
            logger.info("dataset download complete")
        except Exception as e:
            logger.error("Failed to download kaggle dataset: ", e)

    def build_kaggle_credentials(self) -> None:
        if not CsiroDataset.kaggle_config.exists():
            os.makedirs(CsiroDataset.kaggle_config.parent, exist_ok=True)
            kaggle_json = {"username": self.username, "key": self.key}
            with open(CsiroDataset.kaggle_config, "w") as fh:
                json.dump(kaggle_json, fh)
