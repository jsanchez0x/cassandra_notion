#!/bin/bash
DOCKER_IMAGE="jsanchez0x/cassandra-notion"
DOCKER_TAG="local"
DOCKER_CONTAINER_NAME="cassandra-notion"
TRACKER_HOME="/cassandra"

if [ "$1" == "image" ]; then
    docker build --rm --tag ${DOCKER_IMAGE}:${DOCKER_TAG} .

elif [ "$1" == "run" ]; then
    docker run -d -it \
    --env-file utils/env.list \
    --restart=unless-stopped \
    --name ${DOCKER_CONTAINER_NAME} ${DOCKER_IMAGE}:${DOCKER_TAG}

elif [ "$1" == "cassandra" ] || [ "$1" == "scheduling" ]; then
    docker exec ${DOCKER_CONTAINER_NAME} $1

elif [ "$1" == "sh" ]; then
    docker exec -it ${DOCKER_CONTAINER_NAME} $1

else
    echo "v1.0"
    echo "Helper for run commands in the container."
    echo "PARAMETERS:"
    echo "    image                       Create the Docker image."
    echo "    run                         Run the Docker container."
    echo "    cassandra                   Run Cassandra manually."
    echo "    scheduling                  Activate or deactivate Cassandra cronjob."
    echo "    sh                          SH prompt."
fi