#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

network_name="dyel_minio-net"
runtime_tag="mirandatz/dyel:runtime"
shared_storage=$"$(pwd)/container_storage/dyel"

if [ ! -f ".dyel_project_root" ]; then
    echo "script must be run from project root"
    exit 1
fi

docker build \
    -f Dockerfile \
    -t "${runtime_tag}" .

docker run \
    --mount "type=bind,source=${shared_storage},target=/data" \
    --rm \
    --network "$network_name" \
    --env-file secrets/secrets.env \
    --env-file <(env | grep DYEL_) \
    "${runtime_tag}" \
    python -m dyel.command_line_interface "$@"
