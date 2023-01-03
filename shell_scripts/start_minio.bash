#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

network_name="dyel-net"

if [ ! -f ".dyel_project_root" ]; then
    echo "script must be run from project root directory"
    exit 1
fi

storage_path=$(pwd)"/minio/data"

mkdir -p "$storage_path"

docker run \
    --rm \
    --name dyel-minio \
    --network "$network_name" \
    -p 9000:9000 \
    -p 9090:9090 \
    -v "$storage_path":/data \
    --env-file secrets/secrets.env \
    quay.io/minio/minio server /data --console-address ":9090"
