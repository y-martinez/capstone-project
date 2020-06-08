pipeline {
  agent any

  environment {
    dockerhubCredentials = 'docker-hub-credentials'
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
          app = docker.build("project-final-udacity")
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
          docker.withRegistry('https://registry.hub.docker.com', dockerhubCredentials) {
            app.push("${env.BUILD_NUMBER}")
            app.push("latest")
          }
        }
      }
    }
  }
}