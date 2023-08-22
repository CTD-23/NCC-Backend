#!/bin/bash

docker run -d -it --memory="512m" --name container1 -v $(pwd)/Judge:/src --security-opt seccomp=$(pwd)/seccomp/script.json python bash
docker run -d -it --memory="512m" --name container2 -v $(pwd)/Judge:/src --security-opt seccomp=$(pwd)/seccomp/script.json python bash
docker run -d -it --memory="512m" --name container3 -v $(pwd)/Judge:/src --security-opt seccomp=$(pwd)/seccomp/script.json python bash
docker run -d -it --memory="512m" --name container4 -v $(pwd)/Judge:/src --security-opt seccomp=$(pwd)/seccomp/script.json python bash
docker run -d -it --memory="512m" --name container5 -v $(pwd)/Judge:/src --security-opt seccomp=$(pwd)/seccomp/script.json python bash
docker run -d -it --memory="512m" --name container6 -v $(pwd)/Judge:/src --security-opt seccomp=$(pwd)/seccomp/script.json python bash
docker run -d -it --memory="512m" --name container7 -v $(pwd)/Judge:/src --security-opt seccomp=$(pwd)/seccomp/script.json python bash
docker run -d -it --memory="512m" --name container8 -v $(pwd)/Judge:/src --security-opt seccomp=$(pwd)/seccomp/script.json python bash
docker run -d -it --memory="512m" --name container9 -v $(pwd)/Judge:/src --security-opt seccomp=$(pwd)/seccomp/script.json python bash
docker run -d -it --memory="512m" --name container10 -v $(pwd)/Judge:/src --security-opt seccomp=$(pwd)/seccomp/script.json python bash
# docker run -d -it --name container4 -v $(pwd)/Judge:/src --security-opt seccomp=$(pwd)/seccomp/script.json python bash



# To Spawn container for isolation environment

