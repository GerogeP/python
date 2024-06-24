#!/bin/bash

if [ -n "$(docker network ls -q --filter "name=MTA")" ]; then  
    echo "Docker network MTA exists."   
else
    docker network create \
      --driver=bridge \
      --subnet=172.18.0.0/16 \
      --ip-range=172.18.5.0/24 \
      --gateway=172.18.5.254 \
      MTA  
    echo "Docker network MTA create."  
fi

if [ -n "$(docker network ls -q --filter "name=my-multihost-network")" ]; then  
    echo "Docker network my-multihost-network exists."   
else
    docker network create -d overlay \
      --subnet=192.168.10.0/25 \
      --subnet=192.168.20.0/25 \
      --gateway=192.168.10.100 \
      --gateway=192.168.20.100 \
      --aux-address="my-router=192.168.10.5" --aux-address="my-switch=192.168.10.6" \
      --aux-address="my-printer=192.168.20.5" --aux-address="my-nas=192.168.20.6" \
      my-multihost-network
    echo "Docker network my-multihost-network create."  
fi