pipeline {
    agent any

    environment {
        REGISTRY = "docker.io"
        BACKEND_IMAGE = "yourusername/flask-backend"
        FRONTEND_IMAGE = "yourusername/flask-frontend"
        TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                sh """
                docker build -t $BACKEND_IMAGE:$TAG backend/
                docker build -t $FRONTEND_IMAGE:$TAG frontend/
                """
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh """
                docker run --rm $BACKEND_IMAGE:$TAG python -m unittest discover
                """
            }
        }

        stage('Security Scan (Trivy)') {
            steps {
                sh """
                trivy image --severity HIGH,CRITICAL $BACKEND_IMAGE:$TAG
                trivy image --severity HIGH,CRITICAL $FRONTEND_IMAGE:$TAG
                """
            }
        }

        stage('Tag Images') {
            steps {
                sh """
                docker tag $BACKEND_IMAGE:$TAG $BACKEND_IMAGE:latest
                docker tag $FRONTEND_IMAGE:$TAG $FRONTEND_IMAGE:latest
                """
            }
        }

        stage('Push Images') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push $BACKEND_IMAGE:$TAG
                    docker push $BACKEND_IMAGE:latest
                    docker push $FRONTEND_IMAGE:$TAG
                    docker push $FRONTEND_IMAGE:latest
                    """
                }
            }
        }

        stage('Deploy') {
            steps {
                sh """
                docker-compose pull
                docker-compose up -d
                """
            }
        }
    }

    post {
        success {
            echo "Deployment successful"
        }
        failure {
            echo "Pipeline failed"
        }
        always {
            sh "docker system prune -f"
        }
    }
}
