def serviceAddress = ""

pipeline {
  agent any

  environment {
    dockerhubCredentials = 'dockerhubCredentials'
  }

  stages {

    stage('Install dependencies') {
        steps {
            sh 'python3 -m venv venv'
            sh '. venv/bin/activate && make install'
        }
    }

    stage('Lint with pylint and hadolint') {
        steps {
            sh '. venv/bin/activate && make lint'
        }
    }

    stage('Build docker') {
        steps {
            script {
                app = docker.build("ybrahinmartinez/project-final-udacity")
            }
        }
    }

    stage('Scan image with Aqua') {
        steps {
            aquaMicroscanner(imageName: 'ybrahinmartinez/project-final-udacity', notCompliesCmd: 'exit 4', onDisallowed: 'ignore', outputFormat: 'html')
        }
    }

    stage('Publish docker to Dockerhub') {
        steps {
            script {
                docker.withRegistry('', dockerhubCredentials) {
                    app.push("${env.BUILD_NUMBER}")
                    app.push("latest")
                }
            }
        }
    }

    stage('Deploy to Kubernetes (EKS Cluster)') {
        steps {
            retry(3) {
                withAWS(credentials: 'aws-credentials-udacity', region: 'us-west-2') {
                    sh 'echo "Setup Kubernetes Cluster"'
                    sh "aws eks --region us-west-2 update-kubeconfig --name UdacityFinalProject-EKS-CLUSTER"
                    sh 'echo "Deploying to Kubernetes"'
                    sh "kubectl apply -f kubernetes/aws-auth-cm.yaml"
                    sh "kubectl set image deployments/capstone capstone=ybrahinmartinez/project-final-udacity:latest"
                    sh 'sed -ie "s/latest/${GIT_COMMIT}/g" kubernetes/deployment.yml'
                    sh "kubectl apply -f kubernetes/deployment.yml"
                    sh 'echo "Showing the result of deployment"'
                    sh "kubectl get svc"
                    sh "kubectl get pods -o wide"
                    script{
                        serviceAddress = sh(script: "kubectl get svc --output=json | jq -r '.items[0] | .status.loadBalancer.ingress[0].hostname'", returnStdout: true).trim()
                    }
                    sh "echo 'Deployment Complete!'"
				    sh "echo 'View Page Here (Please Allow a Minute for Services to Refresh): http://$serviceAddress:8000'"
                }
            }
        }
    }
    stage("Cleaning up") {
        steps {
            sh 'echo "Cleaning up..."'
            sh "docker system prune -f"
        }
    }
  }
}