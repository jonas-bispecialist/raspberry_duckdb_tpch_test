# Docker Commands Reference

## Build Container
```bash
# Build the compute container
docker build -t tpch-compute .
```

## Start Container for Development
```bash
# Start container with current directory mounted
docker run -d --name tpch-kernel -v ${PWD}:/workspace -p 8888:8888 tpch-compute

# Get Jupyter token if needed
docker logs tpch-kernel
```

## Container Management
```bash
# Stop the container
docker stop tpch-kernel

# Remove the container
docker rm tpch-kernel

# Stop and remove in one command
docker rm -f tpch-kernel

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a
```

## Debugging
```bash
# View container logs
docker logs tpch-kernel

# Enter container shell
docker exec -it tpch-kernel bash

# Check container resource usage
docker stats tpch-kernel
```

## VS Code Usage
1. Start container using command above
2. In VS Code:
   - Open notebook/Python file
   - Click "Select Kernel" (top-right)
   - Choose "Existing Jupyter Server"
   - Enter `http://localhost:8888`

## Clean Up
```bash
# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove container and its image
docker rm -f tpch-kernel
docker rmi tpch-compute
``` 