pipeline {
    agent any
    stages {

        stage('Install dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh 'source venv/bin/activate && make install'
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
    }
}