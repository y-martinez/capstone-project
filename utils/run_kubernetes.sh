#!/usr/bin/env bash

# This tags and uploads an image to Docker Hub

# Step 1:
# This is your Docker ID/path
dockerpath=ybrahinmartinez/project-final-udacity:latest

# Step 2
# Run the Docker Hub container with kubernetes
kubectl run project-final-udacity\
    --image=$dockerpath\
    --port=8000 --labels app=capstone-udacity

# Wait to pod status will be ready
kubectl wait pod/project-final-udacity --for=condition=Ready --timeout=-1s

# Step 3:
# List kubernetes pods
kubectl get pods

# Step 4:
# Forward the container port to a host
kubectl port-forward project-final-udacity 8000:8000

# Step 5:
# See the output of app running into pods
kubectl logs project-final-udacity  