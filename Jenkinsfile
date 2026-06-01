pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_IMAGE_BACKEND = 'todo-backend'
        DOCKER_IMAGE_FRONTEND = 'todo-frontend'
        K8S_NAMESPACE = 'default'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend - Test') {
            steps {
                dir('backend') {
                    sh '''
                        pip install -r requirements.txt
                        pytest -v
                    '''
                }
            }
        }

        stage('Frontend - Install & Test') {
            steps {
                dir('frontend') {
                    sh '''
                        npm install
                        npm run test
                    '''
                }
            }
        }

        stage('Backend - Build & Push') {
            steps {
                dir('backend') {
                    sh """
                        docker build -t ${DOCKER_IMAGE_BACKEND}:${BUILD_NUMBER} .
                        docker tag ${DOCKER_IMAGE_BACKEND}:${BUILD_NUMBER} ${DOCKER_IMAGE_BACKEND}:latest
                    """
                }
            }
        }

        stage('Frontend - Build & Push') {
            steps {
                dir('frontend') {
                    sh """
                        docker build -t ${DOCKER_IMAGE_FRONTEND}:${BUILD_NUMBER} .
                        docker tag ${DOCKER_IMAGE_FRONTEND}:${BUILD_NUMBER} ${DOCKER_IMAGE_FRONTEND}:latest
                    """
                }
            }
        }

        stage('Deploy to K8s') {
            steps {
                dir('k8s') {
                    sh """
                        sed -i 's|latest|${BUILD_NUMBER}|g' backend-deployment.yaml
                        sed -i 's|latest|${BUILD_NUMBER}|g' frontend-deployment.yaml
                        kubectl apply -f backend-deployment.yaml
                        kubectl apply -f frontend-deployment.yaml
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
            echo "Frontend: http://frontend.${K8S_NAMESPACE}.svc.cluster.local"
            echo "Backend: http://backend.${K8S_NAMESPACE}.svc.cluster.local"
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
