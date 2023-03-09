#!/bin/bash 

VERSION=$(git log -1 --pretty=%h)
REPO="pwaldi/airbyte-source-teamtailor"
TAG="$REPO:$VERSION"
LATEST="${REPO}:latest"
docker build -t "$TAG" -t "$LATEST" .
