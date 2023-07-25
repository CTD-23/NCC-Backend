#!/bin/bash


# running_containers=$(docker ps --format "{{.Names}}")

# # Loop through each container
# for container_name in $running_containers; do
#   # Check if the container is running any processes
#   process_count=$(docker exec -it $container_name bash -c "ps aux | wc -l")

#   # If the container has no running processes, allocate it to another user
#   if [ $process_count -le 1 ]; then
#     # Perform the allocation operation for the container
#     # Replace this line with the appropriate allocation logic

#     echo "Container '$container_name' has no running processes and has been allocated to another user."
#   else
#     echo "Container '$container_name' is running processes and cannot be allocated at the moment."
#   fi
# done



# Get the container ID or name
container_id_or_name="container1"

# Use docker inspect to retrieve detailed information for the container
mounts=$(docker inspect --format='{{ json .Mounts }}' $container_id_or_name)

# Check if the Mounts section is empty
if [ -z "$mounts" ]; then
  echo "false"
else
  echo "true"
fi
