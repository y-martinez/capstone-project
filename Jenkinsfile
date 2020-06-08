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
            sh '"Setup Kubernetes Cluster"'
            sh "aws eks --region us-west-2 update-kubeconfig --name UdacityFinalProject-EKS-CLUSTER"
        }
    }
  }
}