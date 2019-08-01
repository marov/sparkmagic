#!/bin/bash -xe

docker build . -t docker.intuit.com/data/mlplatform/sbsegml/service/jupyterhub:latest -f Dockerfile.jupyter
docker push docker.intuit.com/data/mlplatform/sbsegml/service/jupyterhub:latest
