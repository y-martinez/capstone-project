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

    stage('Lint') {
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

    stage('Scan image') {
      steps {
        aquaMicroscanner(imageName: 'project-final-udacity', notCompliesCmd: 'exit 4', onDisallowed: 'ignore', outputFormat: 'html')
      }
    }

    stage('Publish docker') {
      steps {
        script {
          docker.withRegistry('', dockerhubCredentials) {
            app.push("${env.BUILD_NUMBER}")
            app.push("latest")
          }
        }
      }
    }

    stage('Deploy to Kubernetes') {
        steps {
            retry(3) {
                withAWS(region:'us-west-2',credentials:'aws-credentials-udacity') {
                    sh '"Setup Kubernetes Cluster"'
                    sh "aws eks --region us-west-2 update-kubeconfig --name UdacityFinalProject-EKS-CLUSTER"
                    sh 'echo "Deploying to Kubernetes"'
                    sh 'sed -ie "s/latest/${GIT_COMMIT}/g" kubernetes/deployment.yml'
                    sh "kubectl apply -f kubernetes/deployment.yml"
                }
            }
        }
    }
  }
}