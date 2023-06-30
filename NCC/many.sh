#!/bin/bash
docker run -d -it --name container1 -v $(pwd)/Judge:/src --security-opt seccomp=$(pwd)/seccomp/script.json python bash
