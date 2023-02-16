# Secrets
The `docker compose up` and the scripts stored inside `./shell_scripts` assume that a .env file with secrets is stored in `./secrets/secrets.env`. This file must contain the following key-value pairs: 
- RIOT_API_KEY=insert_your_riot_api_key_here
- MINIO_ROOT_USER=insert_your_minio_ user_here
- MINIO_ROOT_PASSWORD=insert_your_minio_password_here

The containers storage are mounted at `./container_storage`:
- minio database is mounted at `./container_storage/minio`
- temporary file storage, used for long inputs and/or outputs, is mounted at `./container_storage/dyel`
