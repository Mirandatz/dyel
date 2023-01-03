import io

import pydantic
import typer
from loguru import logger
from minio import Minio

import dyel.riot_api as riot_api


class RiotSettings(pydantic.BaseSettings):
    region_url: str = pydantic.Field(
        default="https://americas.api.riotgames.com",
        env="DYEL_RIOT_REGION_URL",
    )
    country_url: str = pydantic.Field(
        default="https://br1.api.riotgames.com",
        env="DYEL_RIOT_COUNTRY_URL",
    )
    api_key: str = pydantic.Field(env="DYEL_RIOT_API_KEY")


class StorageSettings(pydantic.BaseSettings):
    endpoint: str = pydantic.Field(
        default="dyel-minio:9000",
        env="DYEL_STORAGE_ENDPOINT",
    )
    bucket: str = pydantic.Field(
        default="dev_bucket",
        env="DYEL_STORAGE_BUCKET",
    )
    user: str = pydantic.Field(env="DYEL_STORAGE_USER")
    password: str = pydantic.Field(env="DYEL_STORAGE_PASSWORD")


app = typer.Typer()


@app.command(name="match-id")
def download_match_data() -> None:
    raise NotImplementedError()


@app.command(name="summoner-data")
def download_summoner_data(
    summoner_name: str = typer.Option(..., envvar="DYEL_SUMMONER_NAME")
) -> None:
    riot_settings = RiotSettings()
    storage_settings = StorageSettings()

    client = Minio(
        endpoint=storage_settings.endpoint,
        access_key=storage_settings.user,
        secret_key=storage_settings.password,
        secure=False,
    )

    summoner = riot_api.get_summoner_data(
        summoner_name=summoner_name,
        country_url=riot_settings.country_url,
        api_key=riot_settings.api_key,
    )

    summoner_as_json = summoner.json()
    summoner_as_bytes = summoner_as_json.encode("utf8")
    summoner_as_stream = io.BytesIO(summoner_as_bytes)

    filename = f"summoner_data_by_name/{summoner.name}.json"

    logger.info(
        f"saving summoner data... summoner_name={summoner.name}, path={filename}, bucket={storage_settings.bucket}"
    )

    client.put_object(
        bucket_name=storage_settings.bucket,
        object_name=filename,
        data=summoner_as_stream,
        length=len(summoner_as_bytes),
    )


if __name__ == "__main__":
    app()
