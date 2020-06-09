[![Build Status](http://ec2-54-185-170-151.us-west-2.compute.amazonaws.com:8000/buildStatus/icon?job=capstone-project%2Fmaster)](http://ec2-54-185-170-151.us-west-2.compute.amazonaws.com:8000/job/capstone-project/job/master/)
[![license](https://img.shields.io/github/license/y-martinez/capstone-project.svg)](https://github.com/y-martinez/machine-learning-microservices/blob/master/LICENSE)

# Capstone Project

## Project Overview

In this project you will apply the skills and knowledge which were developed throughout the Cloud DevOps Nanodegree program. These include:

Working in AWS
- Using Jenkins to implement Continuous Integration and Continuous Deployment
- Building pipelines
- Working with Ansible and CloudFormation to deploy clusters
- Building Kubernetes clusters
- Building Docker containers in pipelines

As a capstone project, the directions are rather more open-ended than they were in the previous projects in the program. You will also be able to make some of your own choices in this capstone, for the type of deployment you implement, which services you will use, and the nature of the application you develop.

You will develop a CI/CD pipeline for micro services applications with either blue/green deployment or rolling deployment. You will also develop your Continuous Integration steps as you see fit, but must at least include typographical checking (aka “linting”). To make your project stand out, you may also choose to implement other checks such as security scanning, performance testing, integration testing, etc.!

Once you have completed your Continuous Integration you will set up Continuous Deployment, which will include:

- Pushing the built Docker container(s) to the Docker repository (you can use AWS ECR, create your own custom Registry within your cluster, or another 3rd party Docker repository) ; and
- Deploying these Docker container(s) to a small Kubernetes cluster. For your Kubernetes cluster you can either use AWS Kubernetes as a Service, or build your own Kubernetes cluster. To deploy your Kubernetes cluster, use either Ansible or Cloudformation. Preferably, run these from within Jenkins as an independent pipeline.

### Project Tasks

> #### Step 1: Propose and Scope the Project

- Plan what your pipeline will look like.
- Decide which options you will include in your Continuous Integration phase.
- Use Jenkins.
- Pick a deployment type - either rolling deployment or blue/green deployment.
- For the Docker application you can either use an application which you come up with, or use an open-source application pulled from the Internet, or if you have no idea, you can use an Nginx “Hello World, my name is (student name)” application.


> #### Step 2: Use Jenkins, and implement blue/green or rolling deployment.

- Create your Jenkins master box with either Jenkins and install the plugins you will need.
- Set up your environment to which you will deploy code.


> #### Step 3: Pick AWS Kubernetes as a Service, or build your own Kubernetes cluster.

- Use Ansible or CloudFormation to build your “infrastructure”; i.e., the Kubernetes Cluster.
- It should create the EC2 instances (if you are building your own), set the correct networking settings, and deploy software to these instances.
- As a final step, the Kubernetes cluster will need to be initialized. The Kubernetes cluster initialization can either be done by hand, or with Ansible/Cloudformation at the student’s discretion.

> #### Step 4: Build your pipeline

- Construct your pipeline in your GitHub repository.
- Set up all the steps that your pipeline will include.
- Configure a deployment pipeline.
- Include your Dockerfile/source code in the Git repository.
- Include with your Linting step both a failed Linting screenshot and a successful Linting screenshot to show the Linter working properly.

> #### Step 5: Test your pipeline
- Perform builds on your pipeline.
- Verify that your pipeline works as you designed it.
- Take a screenshot of the Jenkins pipeline showing deployment and a screenshot of your AWS EC2 page showing the newly created (for blue/green) or modified (for rolling) instances. Make sure you name your instances differently between blue and green deployments.

You can find a detailed [project rubric, here](https://review.udacity.com/#!/rubrics/2577/view).

## File structure

> ### Application:

- `app` application folder
- `requirements.txt` dependencies of app

> ### CI/CD:

- `Jenkinsfile` file with Pipeline configuration
- `kubernetes/deployment.yml` file used for deploy to cluster k8s
- `kubernetes/aws-auth-cm.yaml` used to allow auth into k8s in `aws eks`

> ### Infrastructure

- `infra/stacks` folder with stacks templates in CloudFormation
- `infra/parameters` folder with parameter use in stacks templates

> ### Outputs:

- `outputs`  folder with screenshots
- `outputs/capstone1.png` show the stacks successfully deployed with CloudFormation
- `outputs/capstone2.png` show the fail linter hadolint
- `outputs/capstone3.png` show the fail linter pylint(Errors)
- `outputs/capstone4.png` show the fail linter pylint(Warnings)
- `outputs/capstone5.png` show successfully linter pass with 10/10
- `outputs/capstone6.png` show successfully build docker images
- `outputs/capstone7-1.png` show successfully push docker hub(Part1)
- `outputs/capstone7-2.png` show successfully push docker hub(Part2)
- `outputs/capstone8.png` show successfully push to  EKS cluster
- `outputs/capstone9.png` show successfully the page with ELB running without problems
- `outputs/capstone10.png` show successfully new deploy to show the Rolling Deployment method - Creathing/Starting new pods
- `outputs/capstone11.png` show the new pods created and running successfully
- `outputs/capstone12.png` show two versions of application, modify using Rolling Deployment

> ### Docker:

- `Dockerfile` use this file to deploy an image for the app to be runned on a container

> ### Utils/Tools:

- `Makefile`  useful commands to make setup, install, test, lint, run_docker, run_kubernetes, upload_docker, all
- `run_docker.sh` script to build and start container locally
- `run_kubernetes.sh` script to run on Kubernetes locally
- `create-stack.sh` script to create stack with CloudFormation
- `update-stack.sh` script to update stack with CloudFormation
- `delete-stack.sh` script to delete stack with CloudFormation

---

## Setup the Environment

* Create a virtualenv and activate it
* Run `make install` to install the necessary dependencies

## Running application

You can run in different ways this app,these are Standalone, Docker, Kubernetes(locally) or in AWS

1. Standalone:  `make run_standalone`

> You will now access the app on localhost port 8000. [http://localhost:8000](http://localhost:8000)

2. Run in Docker:  `utils/run_docker.sh`

The script will:
- Build an docker image
- List images to verify that this app is dockerized
- Run a container with this specified image and map port 8000 (host) to 8000 (container)

> You can now access the app on localhost port 8000. [http://localhost:8000](http://localhost:8000)

1. Run in Kubernetes:  `utils/run_kubernetes.sh`

The script will:
- Start to run a container in Kubernetes cluster (make sure to have one ready the best option to locally is use `minikube`)
- Wait for the pod to be running
- List pod to verify your pod is up
- Forward port 8000 (host) to 8000 (container)

> You can now access the app on localhost port 8000. [http://localhost:8000](http://localhost:8000)

You can delete when you've finished the pod with the command `kubectl delete pod prediction` and if you use `minikube` to test locally you should clean up your resources and delete the kubernetes cluster with a call to `minikube delete` to delete it or `minikube stop` for pause it.

1. Run in AWS:

You need create the whole infrastructure to deploy the app

```

utils/create-stack.sh network-stack infra/stacks/network.yml infra/parameters/network.json

utils/create-stack.sh iam-stack-jenkins infra/stacks/iam.yml infra/parameters/iam.json

utils/create-stack.sh server-stack infra/stacks/server.yml infra/parameters/server.json 

utils/create-stack.sh eks-stack infra/stacks/eks.yml infra/parameters/eks.json

utils/create-stack.sh eks-nodes-stack infra/stacks/eks-nodes.yml infra/parameters/eks-nodes.json

```

Now you can access to Jenkins to deploy using the pipeline.

You can access the demo using this [link](http://ab61939fd7bf446139fc1752a884b09f-308296604.us-west-2.elb.amazonaws.com:8000/) 

