pipeline {
    agent any

    environment {
        APP_NAME = 'flask-ecommerce-app'
        IMAGE_NAME = "abhirammanoj/${APP_NAME}:latest"
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
                    docker build --no-cache -t $IMAGE_NAME .
                '''
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $IMAGE_NAME
                    '''
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(['ec2-ssh-key']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ubuntu@51.20.252.149 << EOF
                        docker pull $IMAGE_NAME
                        docker stop flask-app || true
                        docker rm flask-app || true
                        docker run -d -p 5000:5000 --name flask-app $IMAGE_NAME
                        EOF
                    '''
                }
            }
        }
    }

    post {
        success {
            withCredentials([string(credentialsId: 'slack-webhook', variable: 'SLACK_URL')]) {
                script {
                    def payload = [
                        text: "✅ Build SUCCESS: Job ${env.JOB_NAME} [#${env.BUILD_NUMBER}]"
                    ]
                    httpRequest httpMode: 'POST',
                                contentType: 'APPLICATION_JSON',
                                requestBody: groovy.json.JsonOutput.toJson(payload),
                                url: SLACK_URL
                }
            }
        }

        failure {
            withCredentials([string(credentialsId: 'slack-webhook', variable: 'SLACK_URL')]) {
                script {
                    def payload = [
                        text: "❌ Build FAILED: Job ${env.JOB_NAME} [#${env.BUILD_NUMBER}]"
                    ]
                    httpRequest httpMode: 'POST',
                                contentType: 'APPLICATION_JSON',
                                requestBody: groovy.json.JsonOutput.toJson(payload),
                                url: SLACK_URL
                }
            }
        }
    }
}
