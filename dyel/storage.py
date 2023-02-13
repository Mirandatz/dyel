import pydantic


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

    # pydantic magic
    class Config:
        allow_mutation = False
        validate_assignment = True
        extra = pydantic.Extra.forbid
        env_file = "secrets/secrets.env"
