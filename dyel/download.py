import io

import pydantic
import typer
from loguru import logger

import dyel.riot_api as riot_api
from minio import Minio, S3Error  # type: ignore


class RiotSettings(pydantic.BaseSettings):
    region_url: str = pydantic.Field(
        default="https://americas.api.riotgames.com",
        env="RIOT_REGION_URL",
    )
    country_url: str = pydantic.Field(
        default="https://br1.api.riotgames.com",
        env="RIOT_COUNTRY_URL",
    )
    api_key: str = pydantic.Field(env="RIOT_API_KEY")


class StorageSettings(pydantic.BaseSettings):
    endpoint: str = pydantic.Field(
        default="dyel-minio:9000",
        env="MINIO_ENDPOINT",
    )
    bucket_name: str = pydantic.Field(
        default="dev-bucket",
        env="MINIO_BUCKET",
    )
    user: str = pydantic.Field(env="MINIO_ROOT_USER")
    password: str = pydantic.Field(env="MINIO_ROOT_PASSWORD")


app = typer.Typer()


@app.command(name="match-id")
def download_match_data() -> None:
    raise NotImplementedError()


def is_object_stored(client: Minio, bucket_name: str, object_name: str) -> bool:
    try:
        client.stat_object(
            bucket_name=bucket_name,
            object_name=object_name,
        )
        return True

    except S3Error as ex:
        if ex.code == "NoSuchKey":
            return False
        else:
            raise


@app.command(name="summoner-data")
def download_summoner_data(
    summoner_name: str = typer.Option(..., envvar="DYEL_SUMMONER_NAME"),
    force_download: bool = typer.Option(False, envvar="DYEL_FORCE_DOWNLOAD"),
) -> None:
    riot_settings = RiotSettings()
    storage_settings = StorageSettings()

    client = Minio(
        endpoint=storage_settings.endpoint,
        access_key=storage_settings.user,
        secret_key=storage_settings.password,
        secure=False,
    )

    object_name = f"summoner_data_by_name/{summoner_name}.json"

    if is_object_stored(
        client,
        bucket_name=storage_settings.bucket_name,
        object_name=object_name,
    ):
        if force_download:
            logger.info(
                "summoner data already exists, but the force_download flag is set. redownloading..."
            )
        else:
            logger.info("summoner data already stored, download skipped")
            return

    summoner_data = riot_api.get_summoner_data(
        summoner_name=summoner_name,
        country_url=riot_settings.country_url,
        api_key=riot_settings.api_key,
    )

    summoner_as_json = summoner_data.json()
    summoner_as_bytes = summoner_as_json.encode("utf8")
    summoner_as_stream = io.BytesIO(summoner_as_bytes)

    object_name = f"summoner_data_by_name/{summoner_data.name}.json"

    logger.info(
        f"saving summoner data... summoner_name={summoner_data.name}, path={object_name}, bucket={storage_settings.bucket_name}"
    )

    client.put_object(
        bucket_name=storage_settings.bucket_name,
        object_name=object_name,
        data=summoner_as_stream,
        length=len(summoner_as_bytes),
    )


if __name__ == "__main__":
    app()
