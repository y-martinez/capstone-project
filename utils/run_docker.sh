#!/usr/bin/env bash

## Complete the following steps to get Docker running locally

# Step 1:
# Build image and add a descriptive tag
docker build . -t project-final-udacity

# Step 2: 
# List docker images
docker images | grep project-final-udacity

# Step 3: 
# Run flask app
docker run --env-file .env -p 8000:8000 project-final-udacity