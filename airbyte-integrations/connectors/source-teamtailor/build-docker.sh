#!/bin/bash 

VERSION=$(git log -1 --pretty=%h)
REPO="pwaldi/airbyte-source-teamtailor:"
TAG="$REPO$VERSION"
LATEST="${REPO}latest"
BUILD_TIMESTAMP=$( date '+%F_%H:%M:%S' )
docker build -t "$TAG" -t "$LATEST" .
docker push "$TAG" 
docker push "$LATEST"
