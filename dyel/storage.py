import pydantic

from minio import Minio, S3Error  # type: ignore


class MinIOSettings(pydantic.BaseSettings):
    endpoint: str = pydantic.Field(
        default="dyel-minio:9000",
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
    def __init__(self, settings: MinIOSettings) -> None:
        self._minio = Minio(
            endpoint=settings.endpoint,
            access_key=settings.user,
            secret_key=settings.password,
            secure=settings.secure,
        )

    def is_object_stored(self, bucket_name: str, object_name: str) -> bool:
        try:
            self._minio.stat_object(
                bucket_name=bucket_name,
                object_name=object_name,
            )
            return True

        except S3Error as ex:
            if ex.code == "NoSuchKey":
                return False
            else:
                raise

    def store_object(
        self,
        bucket_name: str,
        object_name: str,
        data: bytes,
    ) -> None:
        _ = self._minio.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=data,
            length=len(data),
        )
