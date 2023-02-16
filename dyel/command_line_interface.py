import pathlib
import typing

import typer
from loguru import logger

from dyel.riot_api import RiotClient
from dyel.storage import MinIOClient

app = typer.Typer()


@app.command(name="match-id")
def download_match_data() -> None:
    raise NotImplementedError()


def collect_summoner_names(
    summoner_names: list[str] | None,
    summoner_names_file: pathlib.Path | None,
) -> list[str]:
    if summoner_names is None and summoner_names_file is None:
        raise ValueError(
            "summoner_names and summoner_names_file must not be simultaneously None"
        )

    names = summoner_names or []

    if summoner_names_file is not None:
        names_from_file = summoner_names_file.read_text().splitlines()
        if len(names_from_file) == 0:
            logger.warning(
                f"summoner_file_names is empty, path=<{summoner_names_file}>"
            )
        else:
            names += names_from_file

    return names


@app.command(name="download-summoner-data")
def download_summoner_data(
    summoner_name: typing.Optional[list[str]] = typer.Option(
        None, envvar="DYEL_SUMMONER_NAME"
    ),
    summoner_names_file: typing.Optional[pathlib.Path]
    | None = typer.Option(None, envvar="DYEL_SUMMONER_NAMES_FILE"),
) -> None:
    logger.info("downloading summoners data, names count=<{len(summoner_names)}>")

    summoner_name = collect_summoner_names(summoner_name, summoner_names_file)

    riot_client = RiotClient()
    storage_client = MinIOClient()

    for summoner_name in summoner_name:
        data = riot_client.download_summoner_data(summoner_name)
        storage_client.store_summoner_data(summoner_name, data)


if __name__ == "__main__":
    app()
