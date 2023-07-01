#!/bin/bash
docker run -d -it --memory="100m" --name container1 -v $(pwd)/Judge:/src --security-opt seccomp=$(pwd)/seccomp/script.json python bash
docker run -d -it --name container2 -v $(pwd)/Judge:/src --security-opt seccomp=$(pwd)/seccomp/script.json python bash



# container1 with 6mb memory limit
# container2 without memory limit