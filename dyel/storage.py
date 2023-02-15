import io

import pydantic
from loguru import logger

from minio import Minio, S3Error  # type: ignore


class MinIOSettings(pydantic.BaseSettings):
    endpoint: str = pydantic.Field(
        default="minio:9000",
        env="MINIO_ENDPOINT",
    )
    bucket_name: str = pydantic.Field(
        default="dev-bucket",
        env="MINIO_BUCKET",
    )
    user: str = pydantic.Field(..., env="MINIO_ROOT_USER")
    password: str = pydantic.Field(..., env="MINIO_ROOT_PASSWORD")
    secure: bool = pydantic.Field(False, env="MINIO_SECURE")

    # pydantic magic
    class Config:
        allow_mutation = False
        validate_assignment = True
        extra = pydantic.Extra.forbid
        env_file = "secrets/secrets.env"


class MinIOClient:
    def __init__(self, settings: MinIOSettings = MinIOSettings()) -> None:
        self.settings = settings or MinIOSettings()
        self._minio = Minio(
            endpoint=settings.endpoint,
            access_key=settings.user,
            secret_key=settings.password,
            secure=settings.secure,
        )

    def is_object_stored(self, object_name: str) -> bool:
        try:
            self._minio.stat_object(
                bucket_name=self.settings.bucket_name,
                object_name=object_name,
            )
            return True

        except S3Error as ex:
            if ex.code == "NoSuchKey":
                return False
            else:
                raise

    def store_object(self, object_name: str, data: bytes) -> None:
        logger.info(
            f"storing data at bucket_name=<{self.settings.bucket_name}>, object_name=<{object_name}>, byte_count=<{len(data)}>"
        )
        _ = self._minio.put_object(
            bucket_name=self.settings.bucket_name,
            object_name=object_name,
            data=io.BytesIO(data),
            length=len(data),
        )

    def store_summoner_data(self, summoner_name: str, data: bytes) -> None:
        self.store_object(
            object_name=f"summoners/{summoner_name}",
            data=data,
        )


def main() -> None:
    client = MinIOClient()
    client.store_summoner_data("test_bin", "test_bin".encode("utf8"))


if __name__ == "__main__":
    main()
