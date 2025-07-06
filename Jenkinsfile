pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-ecommerce-app"
        DOCKER_IMAGE_TAG = "latest"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                pip install pylint pytest
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                . venv/bin/activate
                pylint app/ run.py || true
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                . venv/bin/activate
                pytest tests/
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME:$DOCKER_IMAGE_TAG .
                '''
            }
        }
    }
}
