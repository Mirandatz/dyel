#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

network_name="dyel-net"

docker network create --driver bridge "$network_name"
