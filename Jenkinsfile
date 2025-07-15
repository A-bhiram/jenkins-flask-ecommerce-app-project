pipeline {
    agent any

    environment {
        APP_NAME = 'flask-ecommerce-app'
        COMMIT_SHA = ''  // will be filled during build
        IMAGE_BASE = "abhirammanoj/${APP_NAME}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    COMMIT_SHA = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    env.COMMIT_SHA = COMMIT_SHA
                    env.FULL_IMAGE_NAME = "${IMAGE_BASE}:${COMMIT_SHA}"
                    env.LATEST_IMAGE_NAME = "${IMAGE_BASE}:latest"
                }
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
            options {
                timeout(time: 5, unit: 'MINUTES')
                retry(2)
            }
            steps {
                sh '''
                    . venv/bin/activate
                    pytest tests/
                '''
            }
        }

        stage('Docker Build') {
            options {
                timeout(time: 10, unit: 'MINUTES')
                retry(1)
            }
            steps {
                sh """
                    docker build --no-cache -t $LATEST_IMAGE_NAME -t $FULL_IMAGE_NAME .
                """
            }
        }

        stage('Docker Push') {
            options {
                timeout(time: 5, unit: 'MINUTES')
                retry(1)
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $LATEST_IMAGE_NAME
                        docker push $FULL_IMAGE_NAME
                    """
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(['ec2-ssh-key']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ubuntu@51.20.252.149 "
                            docker pull $LATEST_IMAGE_NAME &&
                            docker stop flask-app || true &&
                            docker rm flask-app || true &&
                            docker run -d -p 5000:5000 --name flask-app $LATEST_IMAGE_NAME
                        "
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
