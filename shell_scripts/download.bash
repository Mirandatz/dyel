#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

network_name="dyel-net"
runtime_tag="mirandatz/dyel:runtime"

if [ ! -f ".dyel_project_root" ]; then
    echo "script must be run from project root"
    exit 1
fi

if [ "$(docker images -q $runtime_tag 2> /dev/null)" == "" ]; then
    docker build \
        -f Dockerfile \
        -t mirandatz/dyel:runtime .
fi

docker run \
    --rm \
    --network "$network_name" \
    --env-file secrets/secrets.env \
    --env-file <(env | grep DYEL_) \
    mirandatz/dyel:runtime python -m dyel.download "$*"
